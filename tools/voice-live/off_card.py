#!/usr/bin/env python3
"""THE VOICE OFF THE CARD (proof P2, 6 October 2026;
production/research/voice-off-card/NOTE.md and RESULTS-2026-10-06.md).

Today's voice (voice-server.py) makes its sound tokens and its decoder's flow
on the graphics card, and beside the game the card gives it a third of its
idle speed (3.66 s median before the first sound, 2 October). This is the
whole voice on the processor, through ONNX Runtime, with its heavy parts in
8 bits, so the card is left to the game. Nothing in today's voice changes:
the same model, the same voices, the same sampler in the same order, the same
seeds; only where and in what precision the arithmetic is done.

  token loop  Nano's one-token step as a graph (nano_step_graph.py, 2 October),
              8-bit weights (nano-step-int8.onnx); the sentence and the voice
              go through the library's model once on the processor first.
  flow        the decoder's first half (sound tokens to a spectrogram: the
              conformer encoder and the two meanflow steps of the estimator)
              as one graph, written here (--export-flow), in 8 bits
              (--quantize: ONNX Runtime's dynamic quantization, QInt8 weights
              per channel, MatMul only; the convolutions stay at 32 bits).
  vocoder     the library's HiFT on the processor, as today.
  watermark   the library's Perth, as today.

Threads: LEDGER_VOICE_THREADS (default 4) for ONNX Runtime and torch, its
threads never spinning while they wait (they would burn the game's processor
time); LEDGER_VOICE_CORES ("8-11", default none) keeps the voice's own
process on those logical processors, leaving the rest to the game.

    env-dml\\Scripts\\python.exe tools/voice-live/off_card.py --export-flow
    env-dml\\Scripts\\python.exe tools/voice-live/off_card.py --quantize
    env-dml\\Scripts\\python.exe tools/voice-live/off_card.py --check        (graphs against the library, same noise)
    env-dml\\Scripts\\python.exe tools/voice-live/off_card.py --time [--flow nano-flow-int8.onnx] [--step nano-step-int8.onnx]
"""
import importlib.util
import os
import pathlib
import statistics
import sys
import time

HERE = pathlib.Path(__file__).resolve().parent
GRAPHS = pathlib.Path(os.environ.get("LEDGER_VOICE_GRAPHS", "F:/LedgerTools/voice-graphs/nano"))
STOP_OOV = 6561


def server():
    spec = importlib.util.spec_from_file_location("voice_server", HERE / "voice-server.py")
    vs = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(vs)
    return vs


def cores_from(text):
    """'8-11' or '8,9,10,11' -> [8, 9, 10, 11]; '' -> []."""
    out = []
    for part in [p for p in (text or "").split(",") if p.strip()]:
        if "-" in part:
            a, b = part.split("-", 1)
            out += list(range(int(a), int(b) + 1))
        else:
            out.append(int(part))
    return out


def pin_process(cores):
    """The voice's own process on those logical processors (Windows), so the
    game keeps the rest; nothing is done to the game."""
    if not cores or os.name != "nt":
        return False
    import ctypes
    mask = 0
    for c in cores:
        mask |= 1 << c
    k32 = ctypes.windll.kernel32
    # The process handle is 64 bits wide: without these types ctypes passes it as 32
    # and Windows refuses it (6 October: the first runs went unpinned for that reason).
    k32.GetCurrentProcess.restype = ctypes.c_void_p
    k32.SetProcessAffinityMask.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
    return bool(k32.SetProcessAffinityMask(k32.GetCurrentProcess(), mask))


def make_flow_graph(torch, flow):
    """The flow as one module: (all tokens with the voice's prompt tokens in
    front [1, T], the prompt's spectrogram [1, 2Tp, 80], the speaker vector
    [1, 192], the starting noise [1, 80, 2T]) -> the new spectrogram
    [1, 80, 2(T - Tp)]. The library's own modules, its finalize=True path, its
    two meanflow steps (t 0 -> 0.5 -> 1), batch one, nothing padded."""
    nn = torch.nn
    F = torch.nn.functional

    class FlowGraph(nn.Module):
        def __init__(self):
            super().__init__()
            self.f = flow

        def forward(self, token, prompt_feat, embedding, z):
            f = self.f
            emb = f.spk_embed_affine_layer(F.normalize(embedding, dim=1))
            token_len = torch.ones_like(token).sum(dim=1)
            h, _ = f.encoder(f.input_embedding(token), token_len)
            h = f.encoder_proj(h)                                    # [1, 2T, 80]
            conds = torch.cat([prompt_feat, torch.zeros_like(h[:, prompt_feat.shape[1]:, :])], dim=1).transpose(1, 2)
            mu = h.transpose(1, 2).contiguous()
            mask = torch.ones_like(mu[:, :1, :])
            est = f.decoder.estimator
            x = z
            for t0, t1 in ((0.0, 0.5), (0.5, 1.0)):
                t = torch.full((1,), t0, dtype=z.dtype)
                r = torch.full((1,), t1, dtype=z.dtype)
                x = x + (t1 - t0) * est(x, mask=mask, mu=mu, t=t, spks=emb, cond=conds, r=r)
            return x[:, :, prompt_feat.shape[1]:]
    return FlowGraph().eval()


def flow_inputs(torch, gen, tokens):
    """The graph's inputs for these sound tokens (1-D, silence already added),
    drawing the noise in the library's order: the new frames' noise first
    (flow_inference), then the whole length's (the decoder's randn_like), the
    new frames' overwriting its tail."""
    pt = gen["prompt_token"].detach().to("cpu").long()
    pf = gen["prompt_feat"].detach().to("cpu").float()
    emb = gen["embedding"].detach().to("cpu").float()
    tok = torch.atleast_2d(tokens.to("cpu").long())
    noise = torch.randn(1, 80, tok.size(-1) * 2)
    allt = torch.cat([pt, tok], dim=1)
    z = torch.randn(1, 80, allt.size(-1) * 2)
    z[..., pf.shape[1]:] = noise
    return allt, pf, emb, z


def export_flow(argv):
    vs = server()
    torch, speaker, _ = vs.load_models(True)
    conds, _ = vs.learn(torch, speaker, "rocco", vs.clip_for("rocco"))
    g = make_flow_graph(torch, speaker.s3gen.flow)
    torch.manual_seed(1)
    toks = torch.randint(0, 6561, (40,))
    allt, pf, emb, z = flow_inputs(torch, conds.gen, toks)
    GRAPHS.mkdir(parents=True, exist_ok=True)
    path = GRAPHS / "nano-flow.onnx"
    t = time.time()
    with torch.no_grad():
        torch.onnx.export(g, (allt, pf, emb, z), str(path), input_names=["token", "prompt_feat", "embedding", "z"],
                          output_names=["mel"], opset_version=17, do_constant_folding=True,
                          dynamic_axes={"token": {1: "T"}, "prompt_feat": {1: "P"}, "z": {2: "T2"}, "mel": {2: "N2"}})
    print("exported %s, %.0f MB, in %.0f s" % (path, path.stat().st_size / 1e6, time.time() - t))
    return 0


def quantize(argv):
    import onnx
    from onnxruntime.quantization import QuantType, quantize_dynamic
    names = [a for a in argv if a.endswith(".onnx")] or ["nano-flow.onnx"]
    for name in names:
        src = GRAPHS / name
        pre = GRAPHS / name.replace(".onnx", "-pre.onnx")
        dst = GRAPHS / name.replace(".onnx", "-int8.onnx")
        t = time.time()
        # No pre-processing pass (quant_pre_process): it is advised, not required.
        # reduce_range with per_channel: ONNX Runtime's advice for AVX2 without VNNI
        # (U8S8 saturation), production/research/voice-off-card/NOTE.md.
        # MatMul only: ConvInteger on x86 without VNNI is slower than 32-bit convolutions.
        # THE TWO MEANFLOW STEPS SHARE THEIR WEIGHTS, and the quantizer turns each Gemm
        # into a MatMul by transposing its weight in place, "assuming B is not used by
        # any other node" (onnxruntime/quantization/onnx_model.py): the shared ones were
        # transposed twice and the graph would not load. Each Gemm gets its own copy first.
        m = onnx.load(str(src))
        inits = {i.name: i for i in m.graph.initializer}
        seen = set()
        for n in m.graph.node:
            if n.op_type == "Gemm" and len(n.input) > 1 and n.input[1] in inits:
                if n.input[1] in seen:
                    copy = onnx.TensorProto()
                    copy.CopyFrom(inits[n.input[1]])
                    copy.name = n.input[1] + "__" + str(len(m.graph.initializer))
                    m.graph.initializer.append(copy)
                    n.input[1] = copy.name
                else:
                    seen.add(n.input[1])
        onnx.save(m, str(pre))
        del m
        quantize_dynamic(str(pre), str(dst), weight_type=QuantType.QInt8, per_channel=True, reduce_range=True,
                         op_types_to_quantize=["MatMul"], extra_options={"DefaultTensorType": onnx.TensorProto.FLOAT})
        pre.unlink()
        print("quantized %s -> %s, %.0f MB, in %.0f s" % (src.name, dst.name, dst.stat().st_size / 1e6, time.time() - t))
    return 0


def session(path, threads):
    import onnxruntime as ort
    so = ort.SessionOptions()
    so.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
    so.intra_op_num_threads = threads
    so.inter_op_num_threads = 1
    so.execution_mode = ort.ExecutionMode.ORT_SEQUENTIAL
    so.add_session_config_entry("session.intra_op.allow_spinning", "0")
    so.add_session_config_entry("session.inter_op.allow_spinning", "0")
    return ort.InferenceSession(str(path), so, providers=["CPUExecutionProvider"])


class OffCardVoice:
    """Nano on the processor: the library's model for the text, the voice's
    prefill, the vocoder and the watermark; ONNX Runtime for the step and the
    flow. speak(text, seed) -> (wav float32 numpy, timings)."""

    def __init__(self, step="nano-step-int8.onnx", flow="nano-flow-int8.onnx", threads=None):
        self.threads = int(threads or os.environ.get("LEDGER_VOICE_THREADS", "4"))
        self.vs = server()
        torch, speaker, _ = self.vs.load_models(True)
        torch.set_num_threads(self.threads)
        self.torch, self.speaker = torch, speaker
        self.step = session(GRAPHS / step, self.threads)
        self.flow = session(GRAPHS / flow, self.threads) if flow else None
        self.step_name, self.flow_name = step, flow
        self.voices = {}
        import torch.nn.functional as F
        from transformers.generation.logits_process import (LogitsProcessorList, RepetitionPenaltyLogitsProcessor,
                                                            TemperatureLogitsWarper, TopKLogitsWarper, TopPLogitsWarper)
        # The sampler exactly as t3.inference_turbo builds it, in its order.
        self.procs = LogitsProcessorList([TemperatureLogitsWarper(0.8), TopKLogitsWarper(1000), TopPLogitsWarper(0.95),
                                          RepetitionPenaltyLogitsProcessor(1.2)])
        self.F = F

    def ready(self, who, clip):
        """The character's voice (learned once, as today), with its fixed prefix
        through the token model kept: every line starts with the same speaker
        vector and reference tokens, and the model reads left to right, so their
        keys and values are the same for every line (the prefix cache: exact,
        it saves reading 300 to 375 positions again each line)."""
        if who not in self.voices:
            conds, _ = self.vs.learn(self.torch, self.speaker, who, clip)
            with self.torch.no_grad():
                cond_emb = self.speaker.t3.prepare_conditioning(conds.t3)
                past = self.speaker.t3.tfmr(inputs_embeds=cond_emb, use_cache=True).past_key_values
                layers = [(past.layers[i].keys, past.layers[i].values) if hasattr(past, "layers") else past[i]
                          for i in range(len(self.speaker.t3.tfmr.h))]
                conds.prefix = [(k.clone(), v.clone()) for k, v in layers]
                conds.prefix_len = cond_emb.shape[1]
            # LEDGER_VOICE_REF_TOKENS=N (approach B, the lighter decoder): the
            # decoder reads only the last N of the reference's 250 tokens (10 s).
            keep = int(os.environ.get("LEDGER_VOICE_REF_TOKENS", "0") or 0)
            if keep > 0:
                g = dict(conds.gen)
                g["prompt_token"] = g["prompt_token"][:, -keep:]
                g["prompt_feat"] = g["prompt_feat"][:, -2 * keep:]
                conds.gen_used = g
            else:
                conds.gen_used = conds.gen
            self.voices[who] = conds
        self.speaker.conds = self.voices[who]
        return self.voices[who]

    def tokens(self, text, conds):
        """The token loop: prefill by the library's model (after the voice's kept
        prefix), then the step graph."""
        import numpy as np
        torch, t3, F = self.torch, self.speaker.t3, self.F
        from chatterbox.tts_turbo import punc_norm
        tt = self.speaker.tokenizer(punc_norm(text), return_tensors="pt", padding=True, truncation=True).input_ids
        start = t3.hp.start_speech_token * torch.ones_like(tt[:, :1])
        embeds, len_cond = t3.prepare_input_embeds(t3_cond=conds.t3, text_tokens=tt, speech_tokens=start, cfg_weight=0.0)
        if getattr(conds, "prefix", None) is not None and len_cond == conds.prefix_len:
            from transformers import DynamicCache
            kept = DynamicCache()
            for i, (k, v) in enumerate(conds.prefix):
                kept.update(k.clone(), v.clone(), i)
            out = t3.tfmr(inputs_embeds=embeds[:, len_cond:], past_key_values=kept, use_cache=True)
        else:
            out = t3.tfmr(inputs_embeds=embeds, use_cache=True)
        past = out.past_key_values
        layers = [(past.layers[i].keys, past.layers[i].values) if hasattr(past, "layers") else past[i] for i in range(len(t3.tfmr.h))]
        cache = torch.stack([torch.stack([k, v]) for k, v in layers]).numpy()
        n = embeds.shape[1]
        first = t3.speech_head(out[0][:, -1:])[:, -1, :]
        cur = torch.multinomial(F.softmax(self.procs(start, first), dim=-1), 1)
        made = [int(cur)]
        for j in range(1000):
            scores, cache = self.step.run(["scores", "grown"], {"token": np.array([[made[-1]]], dtype=np.int64),
                                                                 "position": np.array([n + j], dtype=np.int64), "cache": cache})
            s = torch.from_numpy(scores)
            if torch.all(self.procs(torch.tensor([made]), s) == -float("inf")):
                break
            cur = torch.multinomial(F.softmax(self.procs(torch.tensor([made]), s), dim=-1), 1)
            made.append(int(cur))
            if made[-1] == t3.hp.stop_speech_token:
                break
        return torch.tensor(made)

    def decode(self, tokens, conds):
        torch = self.torch
        from chatterbox.models.s3gen.const import S3GEN_SIL
        tokens = tokens[tokens < STOP_OOV]
        tokens = torch.cat([tokens, torch.tensor([S3GEN_SIL, S3GEN_SIL, S3GEN_SIL]).long()])
        s3 = self.speaker.s3gen
        t = time.time()
        gen = getattr(conds, "gen_used", conds.gen)
        if self.flow is None:
            mel = s3.flow_inference(tokens, ref_dict=gen, n_cfm_timesteps=2, finalize=True)
        else:
            allt, pf, emb, z = flow_inputs(torch, gen, tokens)
            mel = torch.from_numpy(self.flow.run(["mel"], {"token": allt.numpy(), "prompt_feat": pf.numpy(),
                                                           "embedding": emb.numpy(), "z": z.numpy()})[0])
        t_flow = time.time() - t
        t = time.time()
        with torch.no_grad():
            wav, _ = s3.hift_inference(mel, None)
            wav[:, :len(s3.trim_fade)] *= s3.trim_fade
        t_hift = time.time() - t
        return wav.squeeze(0).numpy(), t_flow, t_hift

    def speak(self, text, seed, who=None, clip=None):
        torch = self.torch
        conds = self.ready(who, clip) if who else self.speaker.conds
        torch.manual_seed(seed)
        t0 = time.time()
        with torch.no_grad():
            toks = self.tokens(text, conds)
        t_tok = time.time() - t0
        wav, t_flow, t_hift = self.decode(toks, conds)
        t = time.time()
        wav = self.speaker.watermarker.apply_watermark(wav, sample_rate=self.speaker.sr)
        t_mark = time.time() - t
        return wav, {"tokens": int(len(toks)), "tokenS": round(t_tok, 3), "flowS": round(t_flow, 3), "hiftS": round(t_hift, 3),
                     "markS": round(t_mark, 3), "totalS": round(time.time() - t0, 3), "speechS": round(len(wav) / self.speaker.sr, 2)}


def check(argv):
    """The flow graph against the library's flow on the same tokens and noise."""
    import numpy as np
    vs = server()
    torch, speaker, _ = vs.load_models(True)
    conds, _ = vs.learn(torch, speaker, "rocco", vs.clip_for("rocco"))
    torch.manual_seed(7)
    toks = torch.randint(0, 6561, (45,))
    rows = []
    for name in [a for a in argv if a.endswith(".onnx")] or ["nano-flow.onnx", "nano-flow-int8.onnx"]:
        if not (GRAPHS / name).exists():
            continue
        sess = session(GRAPHS / name, 4)
        torch.manual_seed(11)
        allt, pf, emb, z = flow_inputs(torch, conds.gen, toks)
        got = sess.run(["mel"], {"token": allt.numpy(), "prompt_feat": pf.numpy(), "embedding": emb.numpy(), "z": z.numpy()})[0]
        torch.manual_seed(11)
        with torch.no_grad():
            want = speaker.s3gen.flow_inference(toks, ref_dict=conds.gen, n_cfm_timesteps=2, finalize=True).numpy()
        span = float(want.max() - want.min())
        d = np.abs(got - want)
        rows.append((name, float(d.max()) / span, float(d.mean()) / span))
        print("%s: shape %s against %s; largest difference %.4f%% of the range, mean %.4f%%"
              % (name, got.shape, want.shape, 100 * d.max() / span, 100 * d.mean() / span))
    return 0


def timed(argv):
    flow = argv[argv.index("--flow") + 1] if "--flow" in argv else "nano-flow-int8.onnx"
    step = argv[argv.index("--step") + 1] if "--step" in argv else "nano-step-int8.onnx"
    if flow == "torch":
        flow = None
    pin_process(cores_from(os.environ.get("LEDGER_VOICE_CORES", "")))
    v = OffCardVoice(step=step, flow=flow)
    vs = v.vs
    v.ready("rocco", vs.clip_for("rocco"))
    for _ in range(2):
        v.speak("Right.", 1)
    lines = ["Quiet one today.", "Twelve years, give or take.", "Depends who's asking.", "Couldn't tell you, pal.",
             "Ask Sheila, she keeps the book.", "Mind how you go."]
    rows = []
    for k, text in enumerate(lines):
        _, r = v.speak(text, 20260924 + k)
        rows.append(r)
        print(text, r, flush=True)
    for key in ("tokens", "tokenS", "flowS", "hiftS", "totalS", "speechS"):
        print("median %s %.3f" % (key, statistics.median(r[key] for r in rows)))
    return 0


if __name__ == "__main__":
    if "--export-flow" in sys.argv:
        sys.exit(export_flow(sys.argv))
    if "--quantize" in sys.argv:
        sys.exit(quantize(sys.argv))
    if "--check" in sys.argv:
        sys.exit(check(sys.argv))
    if "--time" in sys.argv:
        sys.exit(timed(sys.argv))
    print(__doc__)
