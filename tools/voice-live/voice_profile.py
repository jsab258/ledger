#!/usr/bin/env python3
"""WHERE THE VOICE'S TIME GOES (item 2, the delay; production/research/voice-latency/
FAST-FIRST-AUDIO-2026-10-01.md, first step: profile before changing anything).

    C:\\LedgerTools\\chatterbox-nano\\env-dml\\Scripts\\python.exe tools/voice-live/voice_profile.py [--who rocco] [--cpu] [--out F:/LedgerTools/tmp/voice-profile]

Loads Chatterbox Nano exactly as the game's voice server does (voice-server.py's
load_models and its way of readying a cast voice: the sound-token half on the
card through DirectML, the decoder and the voice's reference on the processor),
warms it once, then for the first sentences of the 30 September real-talk run
times each stage of speaker.generate separately:

  tokens   text to sound tokens (t3.inference_turbo, on the card), with how many
           tokens and tokens a second
  decode   sound tokens to audio (s3gen.inference, on the processor)
  mark     the watermark (on the processor)

and the length of speech made. The card's work is waited for before its clock
stops (the tokens are copied back to the processor), so each stage is its own.
Run it with the PC otherwise idle for the voice alone, and again beside the
running game for the real case. Writes a JSON of every line under --out (F:).
Nothing here changes the voice: same settings as the server.
"""
import importlib.util
import json
import os
import pathlib
import statistics
import sys
import time

HERE = pathlib.Path(__file__).resolve().parent
LINES = ["Morning.", "Quiet one today.", "Twelve years, give or take.", "Depends who's asking.",
         "Not that I've seen, no.", "The rank fills up about six.", "Couldn't tell you, pal.",
         "Aye, she's alright is Sheila.", "The drivers use the cafe.", "Ask Sheila, she keeps the book.",
         "Rita's had that shop years.", "Mind how you go."]


def load_server():
    spec = importlib.util.spec_from_file_location("voice_server", HERE / "voice-server.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def main():
    who = sys.argv[sys.argv.index("--who") + 1] if "--who" in sys.argv else "rocco"
    out = pathlib.Path(sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else "F:/LedgerTools/tmp/voice-profile")
    out.mkdir(parents=True, exist_ok=True)
    vs = load_server()
    t0 = time.time()
    torch, speaker, dev = vs.load_models("--cpu" in sys.argv)
    clip = vs.clip_for(who)
    if clip is None:
        print("no clip for", who)
        return 2
    conds, _ = vs.learn(torch, speaker, who, clip)
    speaker.conds = type(conds)(t3=conds.t3.to(device=dev), gen={k: (v.to("cpu") if torch.is_tensor(v) else v)
                                                              for k, v in conds.gen.items()})
    from chatterbox.tts_turbo import punc_norm
    from chatterbox.models.s3gen.const import S3GEN_SIL
    # THE DECODER IN ITS TWO HALVES: the flow (sound tokens to a spectrogram)
    # and the vocoder (spectrogram to sound), each timed.
    split = {"flow": 0.0, "hift": 0.0}
    s3 = speaker.s3gen
    flow_inf, hift_inf = s3.flow_inference, s3.hift_inference

    def timed_flow(*a, **k):
        t = time.time()
        r = flow_inf(*a, **k)
        split["flow"] = time.time() - t
        return r

    def timed_hift(*a, **k):
        t = time.time()
        r = hift_inf(*a, **k)
        split["hift"] = time.time() - t
        return r
    s3.flow_inference, s3.hift_inference = timed_flow, timed_hift
    # --flow-card: the flow on the graphics card (the vocoder stays on the
    # processor), its inputs moved there and its spectrogram brought back.
    if "--flow-card" in sys.argv and str(dev) != "cpu":
        s3.flow.to(dev)
        inner = s3.flow.inference

        def flow_on_card(**k):
            moved = {n: (v.to(dev) if torch.is_tensor(v) else v) for n, v in k.items()}
            mels, cache = inner(**moved)
            return mels.to("cpu"), cache
        s3.flow.inference = flow_on_card
        print("the flow runs on the card", flush=True)
    print("loaded in %.1f s on %s; voice %s from %s" % (time.time() - t0, dev, who, pathlib.Path(clip).name), flush=True)
    for _ in range(2):
        speaker.generate("Right.")   # warm, as the server's --prewarm does
    rows = []
    for text in LINES:
        t = time.time()
        tt = speaker.tokenizer(punc_norm(text), return_tensors="pt", padding=True, truncation=True).input_ids.to(speaker.device)
        tokens = speaker.t3.inference_turbo(t3_cond=speaker.conds.t3, text_tokens=tt, temperature=0.8, top_k=1000,
                                            top_p=0.95, repetition_penalty=1.2)
        tokens = tokens.to("cpu")                      # waits for the card
        t_tokens = time.time() - t
        n = int((tokens < 6561).sum())
        tokens = tokens[tokens < 6561]
        tokens = torch.cat([tokens, torch.tensor([S3GEN_SIL, S3GEN_SIL, S3GEN_SIL]).long()])
        t = time.time()
        wav, _ = speaker.s3gen.inference(speech_tokens=tokens, ref_dict=speaker.conds.gen, n_cfm_timesteps=2)
        wav = wav.squeeze(0).detach().cpu().numpy()
        t_decode = time.time() - t
        t = time.time()
        speaker.watermarker.apply_watermark(wav, sample_rate=speaker.sr)
        t_mark = time.time() - t
        secs = len(wav) / float(speaker.sr)
        row = {"text": text, "tokens": n, "tokenS": round(t_tokens, 3), "tokensPerS": round(n / t_tokens, 1) if t_tokens > 0 else None,
               "decodeS": round(t_decode, 3), "flowS": round(split["flow"], 3), "hiftS": round(split["hift"], 3), "markS": round(t_mark, 3), "speechS": round(secs, 2),
               "totalS": round(t_tokens + t_decode + t_mark, 3)}
        rows.append(row)
        print("%-34s tokens %3d in %.2f s (%5.1f/s)  decode %.2f s (flow %.2f, vocoder %.2f)  mark %.2f s  = %.2f s for %.2f s of speech"
              % (text, n, t_tokens, row["tokensPerS"] or 0, t_decode, row["flowS"], row["hiftS"], t_mark, row["totalS"], secs), flush=True)
    med = lambda k: statistics.median(r[k] for r in rows)
    summary = {"who": who, "device": str(dev), "median": {k: med(k) for k in ("tokens", "tokenS", "tokensPerS", "decodeS", "flowS", "hiftS", "markS", "totalS", "speechS")}, "flowCard": "--flow-card" in sys.argv}
    print("median: tokens %d in %.2f s (%.1f/s), decode %.2f s (flow %.2f, vocoder %.2f), mark %.2f s, total %.2f s for %.2f s of speech"
          % (summary["median"]["tokens"], summary["median"]["tokenS"], summary["median"]["tokensPerS"], summary["median"]["decodeS"],
             summary["median"]["flowS"], summary["median"]["hiftS"],
             summary["median"]["markS"], summary["median"]["totalS"], summary["median"]["speechS"]))
    (out / ("profile-%s-%s.json" % (who, time.strftime("%Y%m%d-%H%M%S")))).write_text(json.dumps({"summary": summary, "rows": rows}, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
