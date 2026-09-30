#!/usr/bin/env python3
"""SOPRO'S FIRST SOUND ON THIS PROCESSOR (item 2, the delay; the research's
first measurement, production/research/voice-latency/NOTE-2026-09-30.md).

    F:\\LedgerTools\\sopro\\.venv\\Scripts\\python.exe tools/voice-live/sopro_bench.py [--who rocco] [--threads 3]

Loads Sopro V2 Turbo on the processor with a capped number of threads, builds
the character's reference exactly as tools/voice-live/sopro-worker.py does
(the cast clip joined with the approved in-game line from voice-engines.json),
then for the 30 September first sentences prints the time to the first
streamed chunk (tts.stream, 64 frames) and the time to make the whole sentence
(tts.synthesize). Nothing else runs beside it: this is the voice alone. Writes
nothing but its reference under --out (F:).
"""
import importlib.util
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


def load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def main():
    who = sys.argv[sys.argv.index("--who") + 1] if "--who" in sys.argv else "rocco"
    threads = int(sys.argv[sys.argv.index("--threads") + 1]) if "--threads" in sys.argv else 3
    out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else "F:/LedgerTools/tmp/sopro-bench"
    os.makedirs(out, exist_ok=True)
    os.environ.setdefault("HF_HOME", "F:/LedgerTools/hf")
    os.environ["HF_HUB_OFFLINE"] = "1"
    import torch
    torch.set_num_threads(threads)
    worker = load("sopro_worker", "sopro-worker.py")
    vs = load("voice_server", "voice-server.py")
    from sopro import SoproTTS
    t0 = time.time()
    tts = SoproTTS.from_pretrained("samuel-vitorino/sopro-v2-turbo", device="cpu")
    _, extra = vs.engines()
    clip = vs.clip_for(who)
    ref = tts.prepare_reference(worker.joined_reference(clip, extra.get(who, ""), out))
    print("loaded in %.1f s, %d threads, reference from %s" % (time.time() - t0, torch.get_num_threads(), pathlib.Path(clip).name))
    for text in ("Right.", "Right."):   # warm, as the worker's prewarm does
        for _ in tts.stream(text, ref=ref, lang="en", temperature=worker.TEMPERATURE, top_k=worker.TOP_K, chunk_frames=64):
            pass
    first, whole, lengths = [], [], []
    for text in LINES:
        t = time.time()
        got = None
        samples = 0
        for chunk in tts.stream(text, ref=ref, lang="en", temperature=worker.TEMPERATURE, top_k=worker.TOP_K, chunk_frames=64):
            if got is None:
                got = time.time() - t
            samples += int(chunk.shape[-1])
        streamed = time.time() - t
        t = time.time()
        wav = tts.synthesize(text, ref=ref, lang="en", temperature=worker.TEMPERATURE, top_k=worker.TOP_K)
        made = time.time() - t
        secs = int(wav.shape[-1]) / float(tts.sample_rate)
        first.append(got)
        whole.append(made)
        lengths.append(secs)
        print("%-34s first chunk %.2f s (stream done %.2f s); whole sentence %.2f s; %.2f s of speech" % (text, got, streamed, made, secs))
    print("median first chunk %.2f s (90th %.2f s); median whole sentence %.2f s for median speech %.2f s"
          % (statistics.median(first), sorted(first)[int(0.9 * (len(first) - 1))], statistics.median(whole), statistics.median(lengths)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
