#!/usr/bin/env python3
"""NANO'S TOKEN LOOP AS ONE CALL A TOKEN (item 2, the delay; 1 October;
production/research/voice-latency/STREAMING-IN-GAME-2026-10-01.md).

Beside the running game the voice's token loop runs at half its idle speed
on the card and on the processor alike: the cost is Python issuing several
hundred small operations a token, which the game's threads slow. A compiled
step graph is one call a token. This exports Nano's step (its GPT-2: 12
layers, 768 wide, 12 heads) and runs it with ONNX Runtime on the card
(DirectML), with the stock sampler unchanged on the processor.

  Step          the one-token step written out plainly from the model's own
                modules (the speech embedding, the position table, each block's
                layers, the final norm and the speech head): the cache grows by
                one key and value per layer.
  --check       Step against the library's model at several positions, the
                same tokens fed to both: the largest difference in the scores.
  --export      writes the graph (about 720 MB, to F:, recorded as a large file).
  --time        tokens a second with ONNX Runtime on the card, and the scores
                against the library's at several positions.

    env-dml\\Scripts\\python.exe tools/voice-live/nano_step_graph.py --check
    env-dml\\Scripts\\python.exe tools/voice-live/nano_step_graph.py --export [--out F:/LedgerTools/voice-graphs/nano]
    env-dml\\Scripts\\python.exe tools/voice-live/nano_step_graph.py --time
"""
import importlib.util
import pathlib
import sys
import time

HERE = pathlib.Path(__file__).resolve().parent
OUT = pathlib.Path("F:/LedgerTools/voice-graphs/nano")
TEXT = "Couldn't tell you, pal. I keep myself to myself, me."


def load(cpu=True):
    spec = importlib.util.spec_from_file_location("voice_server", HERE / "voice-server.py")
    vs = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(vs)
    torch, speaker, dev = vs.load_models(cpu)
    conds, _ = vs.learn(torch, speaker, "rocco", vs.clip_for("rocco"))
    return vs, torch, speaker, dev, conds


def make_step(torch, t3):
    nn = torch.nn

    class Step(nn.Module):
        """One token through the model: (token [1,1], position [1], cache
        [layers, 2, 1, heads, T, 64]) -> (scores [1, 6563], cache with T+1)."""

        def __init__(self):
            super().__init__()
            g = t3.tfmr
            self.emb, self.wpe, self.blocks, self.ln_f, self.head = t3.speech_emb, g.wpe, g.h, g.ln_f, t3.speech_head
            self.heads = g.config.n_head
            self.width = g.config.n_embd
            self.hd = self.width // self.heads

        def forward(self, token, position, cache):
            x = self.emb(token) + self.wpe(position).unsqueeze(0)
            grown = []
            for i, b in enumerate(self.blocks):
                q, k, v = b.attn.c_attn(b.ln_1(x)).split(self.width, dim=2)
                q, k, v = (t.view(1, 1, self.heads, self.hd).transpose(1, 2) for t in (q, k, v))
                keys = torch.cat([cache[i, 0], k], dim=2)
                values = torch.cat([cache[i, 1], v], dim=2)
                att = torch.softmax(torch.matmul(q, keys.transpose(-1, -2)) / (self.hd ** 0.5), dim=-1)
                x = x + b.attn.c_proj(torch.matmul(att, values).transpose(1, 2).reshape(1, 1, self.width))
                x = x + b.mlp(b.ln_2(x))
                grown.append(torch.stack([keys, values]))
            return self.head(self.ln_f(x))[:, -1, :], torch.stack(grown)
    return Step().eval()


def prefill(torch, speaker, t3cond, where):
    """The sentence and the voice through the library's model once: the
    first token's scores and the cache, as [layers, 2, 1, heads, T, 64]."""
    from chatterbox.tts_turbo import punc_norm
    t3 = speaker.t3
    tt = speaker.tokenizer(punc_norm(TEXT), return_tensors="pt").input_ids.to(where)
    start = t3.hp.start_speech_token * torch.ones_like(tt[:, :1])
    embeds, _ = t3.prepare_input_embeds(t3_cond=t3cond, text_tokens=tt, speech_tokens=start, cfg_weight=0.0)
    out = t3.tfmr(inputs_embeds=embeds, use_cache=True)
    past = out.past_key_values
    layers = [(past.layers[i].keys, past.layers[i].values) if hasattr(past, "layers") else past[i] for i in range(len(t3.tfmr.h))]
    cache = torch.stack([torch.stack([k, v]) for k, v in layers])
    return t3.speech_head(out[0][:, -1:])[:, -1, :], cache, past, embeds.shape[1]


def check():
    vs, torch, speaker, dev, conds = load(True)
    t3 = speaker.t3
    step = make_step(torch, t3)
    with torch.no_grad():
        first, cache, past, n = prefill(torch, speaker, conds.t3, "cpu")
        toks = [101, 2203, 4299, 77, 6000, 15, 3333, 2000, 1, 6560]
        worst = 0.0
        for j, tok in enumerate(toks):
            cur = torch.tensor([[tok]])
            hf = t3.tfmr(inputs_embeds=t3.speech_emb(cur), past_key_values=past, use_cache=True)
            past = hf.past_key_values
            want = t3.speech_head(hf[0])[:, -1, :]
            got, cache = step(cur, torch.tensor([n + j]), cache)
            d = float((got - want).abs().max())
            worst = max(worst, d)
            print("position %d: largest score difference %.2e (scores span %.1f)" % (n + j, d, float(want.max() - want.min())))
    print("check: %s (largest %.2e)" % ("same" if worst < 1e-3 else "DIFFERENT", worst))
    return 0 if worst < 1e-3 else 1


def export(argv):
    out = pathlib.Path(argv[argv.index("--out") + 1]) if "--out" in argv else OUT
    out.mkdir(parents=True, exist_ok=True)
    vs, torch, speaker, dev, conds = load(True)
    step = make_step(torch, speaker.t3)
    with torch.no_grad():
        _, cache, _, n = prefill(torch, speaker, conds.t3, "cpu")
        path = out / "nano-step.onnx"
        torch.onnx.export(step, (torch.tensor([[101]]), torch.tensor([n]), cache), str(path),
                          input_names=["token", "position", "cache"], output_names=["scores", "grown"],
                          dynamic_axes={"cache": {4: "past"}, "grown": {4: "past1"}}, opset_version=17, do_constant_folding=True)
    print("exported", path, "%.0f MB" % (path.stat().st_size / 1e6))
    return 0


def timed(argv):
    import numpy as np
    import onnxruntime as ort
    vs, torch, speaker, dev, conds = load(True)
    t3 = speaker.t3
    path = (pathlib.Path(argv[argv.index("--out") + 1]) if "--out" in argv else OUT) / "nano-step.onnx"
    where = "cpu" if "--cpu" in argv else "dml"
    providers = ["CPUExecutionProvider"] if where == "cpu" else [("DmlExecutionProvider", {"device_id": 0}), "CPUExecutionProvider"]
    so = ort.SessionOptions()
    so.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
    if where == "cpu":
        so.intra_op_num_threads = 3
    else:
        so.enable_mem_pattern = False
        so.execution_mode = ort.ExecutionMode.ORT_SEQUENTIAL
    t = time.time()
    sess = ort.InferenceSession(str(path), so, providers=providers)
    print("session on %s in %.1f s" % (sess.get_providers()[0], time.time() - t), flush=True)
    import torch.nn.functional as F
    from transformers.generation.logits_process import (LogitsProcessorList, RepetitionPenaltyLogitsProcessor,
                                                        TemperatureLogitsWarper, TopKLogitsWarper, TopPLogitsWarper)
    procs = LogitsProcessorList([TemperatureLogitsWarper(0.8), TopKLogitsWarper(1000), TopPLogitsWarper(0.95),
                                 RepetitionPenaltyLogitsProcessor(1.2)])
    dev_name = "cpu" if where == "cpu" else "dml"
    with torch.no_grad():
        first, cache, past, n = prefill(torch, speaker, conds.t3, "cpu")
        for run in range(3):
            g = torch.Generator().manual_seed(1)
            start = t3.hp.start_speech_token * torch.ones(1, 1, dtype=torch.long)
            cur = torch.multinomial(F.softmax(procs(start, first), dim=-1), 1, generator=g)
            made = [int(cur)]
            c = ort.OrtValue.ortvalue_from_numpy(cache.numpy(), dev_name, 0)
            t = time.time()
            for j in range(1000):
                binding = sess.io_binding()      # a fresh one each step: clearing it frees the cache it returned
                binding.bind_cpu_input("token", np.array([[made[-1]]], dtype=np.int64))
                binding.bind_cpu_input("position", np.array([n + j], dtype=np.int64))
                binding.bind_ortvalue_input("cache", c)
                binding.bind_output("scores", "cpu")
                binding.bind_output("grown", dev_name, 0)
                sess.run_with_iobinding(binding)
                scores, c = binding.get_outputs()
                s = torch.from_numpy(scores.numpy())
                cur = torch.multinomial(F.softmax(procs(torch.tensor([made]), s), dim=-1), 1, generator=g)
                made.append(int(cur))
                if made[-1] == t3.hp.stop_speech_token:
                    break
            el = time.time() - t
            print("run %d: %d tokens in %.2f s (%.1f a second)" % (run, len(made), el, len(made) / el), flush=True)
        # The scores against the library's at the run's own tokens.
        worst, c = 0.0, ort.OrtValue.ortvalue_from_numpy(cache.numpy(), dev_name, 0)
        for j, tok in enumerate(made[:12]):
            hf = t3.tfmr(inputs_embeds=t3.speech_emb(torch.tensor([[tok]])), past_key_values=past, use_cache=True)
            past = hf.past_key_values
            want = t3.speech_head(hf[0])[:, -1, :].numpy()
            got, c = sess.run_with_ort_values(["scores", "grown"], {"token": ort.OrtValue.ortvalue_from_numpy(np.array([[tok]], dtype=np.int64)),
                                                                    "position": ort.OrtValue.ortvalue_from_numpy(np.array([n + j], dtype=np.int64)),
                                                                    "cache": c})
            worst = max(worst, float(np.abs(got.numpy() - want).max()))
        print("scores against the library's, 12 positions: largest difference %.2e" % worst)
    return 0


if __name__ == "__main__":
    if "--check" in sys.argv:
        sys.exit(check())
    if "--export" in sys.argv:
        sys.exit(export(sys.argv))
    if "--time" in sys.argv:
        sys.exit(timed(sys.argv))
    print(__doc__)
