#!/usr/bin/env python3
"""IS THE VOICE THE SAME WITH ITS FLOW ON THE CARD? (item 2, the delay; 1 October)

    C:\\LedgerTools\\chatterbox-nano\\env-dml\\Scripts\\python.exe tools/voice-live/flow_card_same.py [--who rocco]

voice_profile.py measured the decoder's flow (sound tokens to a spectrogram)
at 1.20 s on the processor and 0.39 s on the card. Moving it must not change
the voice. This makes the sound tokens once per line, then decodes them twice
with the same random seed, flow on the processor and flow on the card (the
vocoder on the processor both times), and compares: the spectrograms' largest
and mean difference against their range, and the two sounds' correlation and
level difference. The same model on two devices differs only in rounding; a
large difference would mean the card changes the voice. Writes both sounds of
each line under --out (F:) for a listen.
"""
import importlib.util
import json
import pathlib
import sys

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
LINES = ["Depends who's asking.", "Ask Sheila, she keeps the book.", "Aye, she's alright is Sheila.", "Mind how you go."]


def main():
    who = sys.argv[sys.argv.index("--who") + 1] if "--who" in sys.argv else "rocco"
    out = pathlib.Path(sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else "F:/LedgerTools/tmp/flow-card-same")
    out.mkdir(parents=True, exist_ok=True)
    spec = importlib.util.spec_from_file_location("voice_server", HERE / "voice-server.py")
    vs = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(vs)
    torch, speaker, dev = vs.load_models(False)
    import soundfile as sf
    from chatterbox.tts_turbo import punc_norm
    from chatterbox.models.s3gen.const import S3GEN_SIL
    conds, _ = vs.learn(torch, speaker, who, vs.clip_for(who))
    speaker.conds = type(conds)(t3=conds.t3.to(device=dev), gen={k: (v.to("cpu") if torch.is_tensor(v) else v) for k, v in conds.gen.items()})
    s3 = speaker.s3gen
    rows = []
    for i, text in enumerate(LINES):
        tt = speaker.tokenizer(punc_norm(text), return_tensors="pt", padding=True, truncation=True).input_ids.to(speaker.device)
        tok = speaker.t3.inference_turbo(t3_cond=speaker.conds.t3, text_tokens=tt, temperature=0.8, top_k=1000, top_p=0.95, repetition_penalty=1.2).to("cpu")
        tok = torch.cat([tok[tok < 6561], torch.tensor([S3GEN_SIL, S3GEN_SIL, S3GEN_SIL]).long()])
        results = {}
        for where in ("cpu", "card"):
            s3.flow.to("cpu" if where == "cpu" else dev)
            torch.manual_seed(1234 + i)
            if where == "card":
                inner = s3.flow.inference

                def on_card(**k):
                    moved = {n: (v.to(dev) if torch.is_tensor(v) else v) for n, v in k.items()}
                    mels, cache = inner(**moved)
                    results["ranOn"] = str(mels.device) + "/" + str(next(s3.flow.parameters()).device)
                    return mels.to("cpu"), cache
                s3.flow.inference = on_card
            mels = s3.flow_inference(tok, ref_dict=speaker.conds.gen, n_cfm_timesteps=2, finalize=True)
            if where == "card":
                s3.flow.inference = inner
            wav, _ = s3.hift_inference(mels.to(dtype=s3.dtype), None)
            results[where] = (mels.detach().cpu().numpy(), wav.squeeze(0).detach().cpu().numpy())
            sf.write(str(out / ("%s-%02d-%s.wav" % (who, i, where))), results[where][1], speaker.sr)
        s3.flow.to("cpu")
        m_cpu, w_cpu = results["cpu"]
        m_card, w_card = results["card"]
        span = float(m_cpu.max() - m_cpu.min()) or 1.0
        n = min(len(w_cpu), len(w_card))
        corr = float(np.corrcoef(w_cpu[:n], w_card[:n])[0, 1]) if n > 10 else float("nan")
        rms = lambda w: float(np.sqrt(np.mean(np.square(w))) + 1e-12)
        row = {"text": text, "melMaxDiffOfRange": round(float(np.abs(m_cpu - m_card).max()) / span, 5),
               "melMeanDiffOfRange": round(float(np.abs(m_cpu - m_card).mean()) / span, 6),
               "waveCorrelation": round(corr, 5), "levelDiffDb": round(20 * np.log10(rms(w_card) / rms(w_cpu)), 3)}
        row["cardPassRanOn"] = results.get("ranOn", "the wrapper never ran")
        rows.append(row)
        print(json.dumps(row), flush=True)
    (out / ("same-%s.json" % who)).write_text(json.dumps(rows, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
