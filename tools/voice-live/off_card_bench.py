#!/usr/bin/env python3
"""THE VOICE'S OWN SHARE, AND THE GAME'S FRAMES WHILE IT SPEAKS (proof P2, 6 October 2026;
production/research/voice-off-card/RESULTS-2026-10-06.md).

    python tools/voice-live/off_card_bench.py --engine today|A|B [--lines 24] [--out F:/LedgerTools/tmp/voice-off-card/RUN]
    python tools/voice-live/off_card_bench.py --engine A --game [--frames 22000]
    python tools/voice-live/off_card_bench.py --selftest

THE VOICE'S SHARE: from handing a line to the voice server (as the game hands the
checked first sentence) to the server's line naming the first piece's sound
file; the game reads that line on its next frame and plays it. The cast's real
lines (content/dialogue/crime-witness-v1.json, the 24 spoken lines), handed one
at a time, each after the last piece of the one before, across Ron, Lena and
Darren's voices (rocco, lena, sam). The server's processor time over the
speaking stretch, as logical processors busy on average, is kept beside it.

  today  voice-server.py as the game runs it (token loop and flow on the card)
  A      voice-server-off-card.py: the whole voice on the processor, 8-bit token
         step and 8-bit flow (nano-flow-int8.onnx), the voice's full reference
  B      the same with the decoder lighter: full-precision flow reading only the
         last 100 of the reference's 250 tokens (4 s of the 10)
  Both A and B: 4 threads, never spinning, the voice's process kept to logical
  processors 8 to 11 (LEDGER_VOICE_CORES); the game is not touched.

--game: BESIDE THE GAME. The packaged game standing in the street exactly as the
build machine times it (tools/slice-perf.py's step in ledger-probe-unreal.yml:
-LedgerSlice, 3440 by 1440 drawn at half, uncapped, off screen, the engine's CSV
profiler) with its own voice off (-NoVoice), the voice server started first and
ready. Then: settle, quiet 25 s, 12 lines, quiet 25 s, 12 lines, quiet until the
capture ends. Each frame is placed in time by adding up the frame times from the
moment the profile file appears; frames within a second of a change are left
out. Frame median and slowest 1% are given for the quiet stretches and the
speaking ones.
"""
import csv
import glob
import json
import os
import pathlib
import shutil
import statistics
import subprocess
import sys
import threading
import time

ROOT = pathlib.Path(__file__).resolve().parents[2]
VOICE_PY = r"C:\LedgerTools\chatterbox-nano\env-dml\Scripts\python.exe"
GAME = r"F:\LedgerTools\played-game\Windows\LedgerProbe\Binaries\Win64\LedgerProbe.exe"
CSV_DIR = r"F:\LedgerTools\played-game\Windows\LedgerProbe\Saved\Profiling\CSV"
WHO = ("rocco", "lena", "sam")


FIRST_CHARS = 0   # --first N (7 October): hand only each line's opening words, at most N characters


def opening(text, n):
    """THE OPENING WORDS of a line, at most n characters, cut at a word and ended with a full stop:
    what a shorter first piece would give the voice (the speech ruling of 7 October: how short can
    the first piece be, beside the game, and what does the voice then take)."""
    if n <= 0 or len(text) <= n:
        return text
    cut = text.rfind(" ", 0, n + 1)
    head = text[:cut if cut > 0 else n].rstrip(" ,;:-")
    return head + ("" if head.endswith((".", "!", "?")) else ".")


def lines():
    d = json.loads((ROOT / "content" / "dialogue" / "crime-witness-v1.json").read_text(encoding="utf-8"))
    return [opening(x["text"], FIRST_CHARS) for x in d["lines"] if isinstance(x, dict) and x.get("text")]


def engine_cmd(name):
    env = dict(os.environ, HF_HUB_OFFLINE="1")
    env.pop("ANTHROPIC_API_KEY", None)
    if name == "today":
        return [VOICE_PY, str(ROOT / "tools" / "voice-live" / "voice-server.py"), "--prewarm"], env
    env.update({"LEDGER_VOICE_THREADS": "4", "LEDGER_VOICE_CORES": os.environ.get("LEDGER_VOICE_CORES", "8-11"),
                "LEDGER_VOICE_STEP_GRAPH": "nano-step-int8.onnx"})
    if name == "A":
        env.update({"LEDGER_VOICE_FLOW_GRAPH": "nano-flow-int8.onnx", "LEDGER_VOICE_REF_TOKENS": "0"})
    elif name == "B":
        env.update({"LEDGER_VOICE_FLOW_GRAPH": "nano-flow.onnx", "LEDGER_VOICE_REF_TOKENS": "100"})
    else:
        raise SystemExit("unknown engine " + name)
    return [VOICE_PY, str(ROOT / "tools" / "voice-live" / "voice-server-off-card.py"), "--prewarm"], env


class Pipe:
    def __init__(self, args, env):
        self.p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                                  env=env, cwd=str(ROOT), text=True, encoding="utf-8", bufsize=1)
        self.lines, self.cv = [], threading.Condition()
        threading.Thread(target=self._read, daemon=True).start()

    def _read(self):
        for line in self.p.stdout:
            line = line.strip()
            if line.startswith("{"):
                try:
                    d = json.loads(line)
                except ValueError:
                    continue
                with self.cv:
                    self.lines.append((time.perf_counter(), d))
                    self.cv.notify_all()

    def send(self, d):
        self.p.stdin.write(json.dumps(d) + "\n")
        self.p.stdin.flush()

    def wait(self, test, timeout):
        end = time.perf_counter() + timeout
        with self.cv:
            while True:
                for i, (t, d) in enumerate(self.lines):
                    if test(d):
                        del self.lines[i]
                        return t, d
                left = end - time.perf_counter()
                if left <= 0:
                    return None, None
                self.cv.wait(left)

    def stop(self):
        try:
            self.p.stdin.close()
            self.p.wait(15)
        except Exception:
            self.p.kill()


def cpu_seconds(pid):
    import psutil
    # The voice environment's python.exe is a launcher: the interpreter doing the
    # work is its child, so the children are counted too.
    try:
        p = psutil.Process(pid)
        total = 0.0
        for q in [p] + p.children(recursive=True):
            try:
                c = q.cpu_times()
                total += c.user + c.system
            except psutil.Error:
                pass
        return total
    except Exception:
        return None


def speak_lines(voice, texts, base_id, rows, keep_dir=None, keep=0):
    """Hands each line, waits for its first piece and then its last; returns (start, end) perf_counter."""
    t_start = time.perf_counter()
    for k, text in enumerate(texts):
        who = WHO[k % len(WHO)]
        rid = base_id + k
        t0 = time.perf_counter()
        voice.send({"id": rid, "who": who, "text": text})
        tf, first = voice.wait(lambda d: d.get("id") == rid and (d.get("part") == 0 or "error" in d), 120)
        row = {"who": who, "text": text}
        if first is None or "error" in first:
            row["error"] = (first or {}).get("error", "timeout")
            rows.append(row)
            continue
        row.update({"firstSoundS": round(tf - t0, 3), "firstPieceSeconds": first.get("seconds"),
                    "firstPieceText": None, "serverMs": first.get("ms")})
        for key in ("tokens", "tokenS", "flowS", "hiftS", "markS"):
            if key in first:
                row[key] = first[key]
        if keep_dir and k < keep and first.get("wav"):
            dst = pathlib.Path(keep_dir) / ("%s-%02d-%s.wav" % (who, k, "first"))
            try:
                shutil.copyfile(first["wav"], dst)
                row["kept"] = str(dst)
            except OSError:
                pass
        last = first
        while not last.get("last"):
            _, last = voice.wait(lambda d: d.get("id") == rid, 120)
            if last is None:
                row["error"] = "no-last"
                break
        row["wholeS"] = round(time.perf_counter() - t0, 3)
        rows.append(row)
        print(json.dumps({k2: row.get(k2) for k2 in ("who", "firstSoundS", "firstPieceSeconds", "tokens", "tokenS", "flowS", "hiftS")}), flush=True)
    return t_start, time.perf_counter()


def stats(xs):
    xs = sorted(x for x in xs if x is not None)
    if not xs:
        return None
    return {"n": len(xs), "median": round(statistics.median(xs), 3), "p90": round(xs[min(len(xs) - 1, int(0.9 * len(xs)))], 3),
            "slowest": round(xs[-1], 3), "fastest": round(xs[0], 3)}


def pct(xs, p):
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(len(xs) * p))] if xs else None


def frames_by_phase(csv_path, phases, margin=1.0):
    """phases: [(label, start_s, end_s)] in seconds from the profile's start."""
    rows = list(csv.reader(open(csv_path, encoding="utf-8", errors="ignore")))
    header, body = rows[0], [r for r in rows[1:] if r and r[0] != "EVENTS" and len(r) > 10]
    fi = header.index("FrameTime")
    gi = header.index("GPUTime") if "GPUTime" in header else None
    mi = header.index("GPUMem/LocalUsedMB") if "GPUMem/LocalUsedMB" in header else None
    t, out = 0.0, {}
    for r in body:
        try:
            ft = float(r[fi])
        except (ValueError, IndexError):
            continue
        t += ft / 1000.0
        for label, a, b in phases:
            if a + margin <= t <= b - margin:
                o = out.setdefault(label, {"ft": [], "gpu": [], "mem": []})
                o["ft"].append(ft)
                if gi is not None:
                    try:
                        o["gpu"].append(float(r[gi]))
                    except (ValueError, IndexError):
                        pass
                if mi is not None:
                    try:
                        o["mem"].append(float(r[mi]))
                    except (ValueError, IndexError):
                        pass
    res = {"profiledS": round(t, 1), "frames": len(body)}
    for label, o in out.items():
        ft = o["ft"]
        res[label] = {"frames": len(ft), "medianMs": round(statistics.median(ft), 2), "p99Ms": round(pct(ft, 0.99), 2),
                      "worstMs": round(max(ft), 2), "over25": sum(1 for x in ft if x > 25.0),
                      "gpuMedianMs": round(statistics.median(o["gpu"]), 2) if o["gpu"] else None,
                      "gpuMemMB": round(statistics.median(o["mem"])) if o["mem"] else None}
    return res


def busy():
    """Graphics work that would spoil the frame times: the build machine's job, an
    editor, another copy of the game, Blender itself (not its connection helper,
    blender-mcp.exe, which draws nothing)."""
    import psutil
    found = []
    for p in psutil.process_iter(["name"]):
        n = (p.info["name"] or "").lower()
        if n in ("runner.worker.exe", "blender.exe") or n.startswith(("unrealeditor", "ledgerprobe")):
            found.append(p.info["name"])
    return found


def run(engine, n, out, game=False, frames=22000, keep=6):
    out = pathlib.Path(out)
    out.mkdir(parents=True, exist_ok=True)
    texts = lines()
    texts = (texts * ((n // len(texts)) + 1))[:n]
    args, env = engine_cmd(engine)
    t_load = time.perf_counter()
    voice = Pipe(args, env)
    _, ready = voice.wait(lambda d: d.get("ready"), 600)
    if ready is None:
        voice.stop()
        return {"engine": engine, "error": "voice did not start"}
    res = {"engine": engine, "ready": ready, "readyS": round(time.perf_counter() - t_load, 1), "lines": [],
           "date": time.strftime("%Y-%m-%d %H:%M"), "game": game}
    print("ready", json.dumps(ready), flush=True)
    rows = res["lines"]
    if not game:
        c0, w0 = cpu_seconds(voice.p.pid), time.perf_counter()
        a, b = speak_lines(voice, texts, 1000, rows, keep_dir=out, keep=len(texts))   # every first piece, for the gate and the ear
        c1 = cpu_seconds(voice.p.pid)
        res["cpuBusyAvg"] = round((c1 - c0) / (b - a), 2) if c0 is not None and c1 is not None else None
        res["speakingS"] = round(b - a, 1)
    else:
        # ONLY WHEN NO OTHER GRAPHICS WORK RUNS (the brief): checked every two
        # minutes for at most an hour before the game starts, and every five
        # seconds while it runs; anything seen is kept with its time, and the
        # stretches it touched are marked.
        waited = 0
        while busy():
            if waited >= 60:
                voice.stop()
                return {"engine": engine, "error": "graphics work running for an hour: " + ",".join(busy())}
            print("graphics work running (%s), waiting two minutes" % ",".join(busy()), flush=True)
            time.sleep(120)
            waited += 2
        intrusions, watching = [], [True]

        def watch():
            while watching[0]:
                b = busy()
                b = [x for x in b if not x.lower().startswith("ledgerprobe")]   # the game itself
                if b:
                    intrusions.append((round(time.perf_counter() - t_csv, 1), b))
                time.sleep(5)
        os.makedirs(CSV_DIR, exist_ok=True)
        for f in glob.glob(os.path.join(CSV_DIR, "*.csv")):
            os.remove(f)
        gargs = [GAME, "-LedgerSlice", "-NoVoice", "-RenderOffScreen", "-ResX=3440", "-ResY=1440", "-windowed", "-ForceRes",
                 "-nosplash", "-unattended", "-dpcvars=r.ScreenPercentage=50,t.MaxFPS=0,r.VSync=0",
                 "-ExecCmds=csvprofile frames=%d" % frames, "-ExitAfterCsvProfiling"]
        genv = dict(os.environ)
        genv.pop("ANTHROPIC_API_KEY", None)
        g = subprocess.Popen(gargs, env=genv, stdout=open(out / "game.log", "w"), stderr=subprocess.STDOUT)
        t_csv = None
        w = time.perf_counter()
        while time.perf_counter() - w < 240 and t_csv is None and g.poll() is None:
            if glob.glob(os.path.join(CSV_DIR, "*.csv")):
                t_csv = time.perf_counter()
            time.sleep(0.1)
        if t_csv is None:
            g.kill()
            voice.stop()
            return {"engine": engine, "error": "no profile appeared"}
        threading.Thread(target=watch, daemon=True).start()
        phases = []

        def quiet(label, secs):
            a = time.perf_counter()
            time.sleep(secs)
            phases.append((label, a - t_csv, time.perf_counter() - t_csv))
        time.sleep(40)                                         # the street loads and settles
        quiet("quiet1", 25)
        half = len(texts) // 2
        c0 = cpu_seconds(voice.p.pid)
        a, b = speak_lines(voice, texts[:half], 2000, rows, keep_dir=out, keep=keep)
        phases.append(("speak1", a - t_csv, b - t_csv))
        quiet("quiet2", 25)
        a2, b2 = speak_lines(voice, texts[half:], 3000, rows)
        c1 = cpu_seconds(voice.p.pid)
        phases.append(("speak2", a2 - t_csv, b2 - t_csv))
        res["cpuBusyAvg"] = round((c1 - c0) / ((b - a) + (b2 - a2) + 25), 2) if c0 is not None and c1 is not None else None
        while g.poll() is None and time.perf_counter() - t_csv < frames * 0.03:
            time.sleep(1)
        phases.append(("quiet3", b2 - t_csv + 1, time.perf_counter() - t_csv))
        if g.poll() is None:
            g.kill()
            res["gameKilled"] = True
        time.sleep(2)
        csvs = sorted(glob.glob(os.path.join(CSV_DIR, "*.csv")), key=os.path.getmtime)
        watching[0] = False
        res["phases"] = [(lb, round(x, 1), round(y, 1)) for lb, x, y in phases]
        res["intrusions"] = intrusions
        res["touched"] = sorted({lb for lb, x, y in phases for t, _ in intrusions if x - 5 <= t <= y + 5})
        if csvs:
            shutil.copyfile(csvs[-1], out / "frames.csv")
            fr = frames_by_phase(csvs[-1], phases)
            res["frames"] = fr
            q = [fr[k] for k in ("quiet1", "quiet2", "quiet3") if k in fr]
            s = [fr[k] for k in ("speak1", "speak2") if k in fr]
            res["framesSummary"] = {"quietMedianMs": [x["medianMs"] for x in q], "speakMedianMs": [x["medianMs"] for x in s],
                                    "quietP99Ms": [x["p99Ms"] for x in q], "speakP99Ms": [x["p99Ms"] for x in s]}
        else:
            res["frames"] = None
    voice.stop()
    ok = [r for r in rows if "error" not in r]
    res["summary"] = {k: stats([r.get(k) for r in ok]) for k in ("firstSoundS", "firstPieceSeconds", "tokens", "tokenS", "flowS", "hiftS", "wholeS")}
    res["errors"] = sum(1 for r in rows if "error" in r)
    (out / "result.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
    print("SUMMARY", json.dumps({"engine": engine, "firstSoundS": res["summary"]["firstSoundS"], "cpuBusyAvg": res.get("cpuBusyAvg"),
                                 "framesSummary": res.get("framesSummary"), "errors": res["errors"]}), flush=True)
    return res


def selftest():
    ok = bad = 0

    def check(name, cond):
        nonlocal ok, bad
        if cond:
            ok += 1
        else:
            bad += 1
            print("off_card_bench selftest FAIL " + name)
    check("the cast's 24 lines", len(lines()) == 24)
    s = stats([3.0, 1.0, 2.0])
    check("median and slowest", s["median"] == 2.0 and s["slowest"] == 3.0)
    import tempfile
    d = tempfile.mkdtemp()
    p = os.path.join(d, "x.csv")
    with open(p, "w", encoding="utf-8") as f:
        f.write("FrameTime,GPUTime,a,b,c,d,e,f,g,h,i,j\n")
        for k in range(400):
            f.write("%s,10,0,0,0,0,0,0,0,0,0,0\n" % ("10" if k < 200 else "20"))
    fr = frames_by_phase(p, [("a", 0.0, 2.0), ("b", 2.0, 6.0)], margin=0.1)
    check("frames are placed by their summed times", fr["a"]["medianMs"] == 10.0 and fr["b"]["medianMs"] == 20.0)
    print("off_card_bench selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


def _opening_checks():
    return (opening("Dark coat, moving quick, didn't stop for anyone.", 20) == "Dark coat, moving." and
            opening("Short one.", 20) == "Short one." and
            opening("Nobody saw a thing round here, love.", 0) == "Nobody saw a thing round here, love.")


if __name__ == "__main__":
    a = sys.argv[1:]
    if "--selftest" in a:
        if not _opening_checks():
            print("off_card_bench selftest FAIL opening words")
            sys.exit(1)
        sys.exit(selftest())
    engine = a[a.index("--engine") + 1] if "--engine" in a else "A"
    n = int(a[a.index("--lines") + 1]) if "--lines" in a else 24
    game = "--game" in a
    out = a[a.index("--out") + 1] if "--out" in a else "F:/LedgerTools/tmp/voice-off-card/%s-%s-%s" % (
        engine, "game" if game else "idle", time.strftime("%H%M"))
    frames = int(a[a.index("--frames") + 1]) if "--frames" in a else 22000
    if "--first" in a:
        FIRST_CHARS = int(a[a.index("--first") + 1])
        out += "-first%d" % FIRST_CHARS
    r = run(engine, n, out, game=game, frames=frames)
    if "error" in r:
        print("ERROR", r["error"], flush=True)
    sys.exit(0 if "error" not in r else 1)
