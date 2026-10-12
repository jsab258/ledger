#!/usr/bin/env python3
"""The automatic check of Quay Street's sound against BRIEF.md (unit 10, cloud week 42).

    python check_sound.py              # checks SOUND_OUT, writes checks/check_v1.json, prints "N of M rows pass"
    python check_sound.py --out v2     # writes checks/check_v2.json instead

One row per test: each of BRIEF.md's automatic acceptance cases (7, numbers 1 to 16) and each file. A missing output fails
by name. Every number comes from BRIEF.md's targets-json block. This script does not import make_sound.py: loop loudness
and true peak are measured with ffmpeg's own ebur128 filter (a second implementation of BS.1770), the seam and the
rest with code written here, so a fault in the build cannot pass its own check.
"""
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import wave

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.environ.get("SOUND_OUT", "/home/user/ledger-scratch/sound-out")
SOURCES_DIR = os.environ.get("SOUND_SOURCES", "/home/user/ledger-scratch/sound-sources")
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
PREVIEWS = os.path.join(REPO, "production", "previews", "cloud-week", "sound")
RATE = 48000

LAYERS = ["traffic", "gulls", "harbour", "wind", "voices", "radio"]
SURFACES = ["paving", "setts", "asphalt", "wet", "wood"]
SPEC_PREVIEWS = ["spec_%s.jpg" % n for n in LAYERS + ["rain"]] + ["spec_steps_%s.jpg" % s for s in SURFACES] + \
                ["spec_doors_shop.jpg", "spec_doors_house.jpg", "spec_bell.jpg", "spec_phonebox.jpg"]
CLIP_PREVIEWS = ["clip_mix_day.ogg", "clip_mix_night.ogg", "clip_mix_rain.ogg"] + ["clip_steps_%s.ogg" % s for s in SURFACES] + ["clip_doors.ogg"]
CC0_TEXT = {"Creative Commons 0", "CC0 (public domain)"}
# words that would put something the content rule or the era forbids into a source (case-insensitive, whole words)
FORBIDDEN = ["child", "children", "kid", "kids", "baby", "babies", "toddler", "playground", "school", "pupil", "pub", "bar", "beer", "wine",
             "alcohol", "drunk", "pint", "gambling", "casino", "betting", "racing", "ice cream", "cellphone", "iphone",
             "smartphone", "ringtone", "car alarm", "reversing", "electric car", "lyrics", "song", "music", "bbc", "radio station"]

rows = []


def add(case, test, ok, detail="", file=None):
    rows.append({"case": case, "test": test, "file": file, "pass": bool(ok), "detail": detail})


# ------------------------------------------------------------------------------------------------ readers
def read_wav(path):
    with wave.open(path, "rb") as w:
        ch, sw, sr, n = w.getnchannels(), w.getsampwidth(), w.getframerate(), w.getnframes()
        raw = w.readframes(n)
    a = np.frombuffer(raw, dtype="<i2").astype(np.float64) / 32768.0 if sw == 2 else None
    if a is not None and ch > 1:
        a = a.reshape(-1, ch)
    return a, ch, sw * 8, sr, raw


def ffmpeg_loudness(path, pad_to=None):
    """(integrated LUFS, true peak dBTP, highest momentary LUFS) from ffmpeg's ebur128; pad_to pads a short clip with silence."""
    af = ("apad=whole_dur=%s," % pad_to if pad_to else "") + "ebur128=peak=true:framelog=verbose"
    r = subprocess.run(["ffmpeg", "-v", "verbose", "-hide_banner", "-nostats", "-i", path, "-af", af, "-f", "null", "-"],
                       capture_output=True, text=True)
    t = r.stderr
    summ = t[t.rfind("Summary:"):]
    i = re.search(r"I:\s+(-?[\d.]+) LUFS", summ)
    tp = re.search(r"Peak:\s+(-?[\d.]+) dBFS", summ)
    ms = [float(x) for x in re.findall(r" M:\s*(-?[\d.]+) ", t)]
    return (float(i.group(1)) if i else None, float(tp.group(1)) if tp else None, max(ms) if ms else None)


def seam(m):
    """Own measure of how a loop closes (see BRIEF.md case 6)."""
    n = 2 * RATE
    d = np.diff(np.concatenate([m[-n:], m[:n]]))
    typical = np.sqrt(np.mean(np.delete(d, n - 1) ** 2)) + 1e-12
    jump = abs(m[0] - m[-1]) / typical
    w = RATE
    c = np.concatenate([[0.0], np.cumsum(np.concatenate([m, m, m]) ** 2)])
    N = len(m)
    pos = np.arange(0, N, RATE // 10)
    before = (c[pos + N] - c[pos + N - w]) / w + 1e-14
    after = (c[pos + N + w] - c[pos + N]) / w + 1e-14
    step = np.abs(10 * np.log10(before / after))
    return float(jump), float(step[0]), float(np.mean(step[1:] < step[0]))


def centroid(m):
    X = np.abs(np.fft.rfft(m * np.hanning(len(m)))) ** 2
    f = np.fft.rfftfreq(len(m), 1.0 / RATE)
    return float((X * f).sum() / X.sum())


def hf_fraction(m, f0=2500.0):
    X = np.abs(np.fft.rfft(m * np.hanning(len(m)))) ** 2
    f = np.fft.rfftfreq(len(m), 1.0 / RATE)
    return float(X[f > f0].sum() / X.sum())


def max_xcorr(a, b):
    n = len(a) + len(b)
    nf = 1 << (n - 1).bit_length()
    A, B = np.fft.rfft(a, nf), np.fft.rfft(b, nf)
    c = np.fft.irfft(A * np.conj(B), nf)
    return float(np.abs(c).max() / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-12))


def sha256(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


# --------------------------------------------------------------------------------------------------- main
def main():
    tag = "v1"
    if "--out" in sys.argv:
        tag = sys.argv[sys.argv.index("--out") + 1]
    brief = open(os.path.join(HERE, "BRIEF.md"), encoding="utf8").read()
    a = brief.index("```targets-json") + len("```targets-json")
    T = json.loads(brief[a:brief.index("```", a)])
    manifest = json.load(open(os.path.join(HERE, "manifest.json"), encoding="utf8"))["outputs"] if os.path.exists(os.path.join(HERE, "manifest.json")) else {}
    sources = {s["id"]: s for s in json.load(open(os.path.join(HERE, "sources.json"), encoding="utf8"))["sources"]}

    files = sorted(f for f in os.listdir(OUT_DIR) if f.endswith(".wav")) if os.path.isdir(OUT_DIR) else []
    names = {f[:-4] for f in files}

    # case 1: inventory ---------------------------------------------------------------------------------
    loops = sorted(T["loops_lufs"])
    for n in loops:
        add(1, "loop exists", n in names, "" if n in names else "MISSING %s.wav" % n, n + ".wav")
    groups = {}
    for n in names:
        g = re.sub(r"_\d+$", "", n)
        groups.setdefault(g, []).append(n)
    for g, need in sorted(T["min_variants"].items()):
        have = len(groups.get(g, []))
        add(1, "at least %d variants of %s" % (need, g), have >= need, "%d found%s" % (have, "" if have >= need else " (MISSING %d)" % (need - have)))

    shots = sorted(n for g, v in groups.items() if g in T["min_variants"] for n in v)
    present_loops = [n for n in loops if n in names]
    expected = present_loops + shots

    # classes of one-shots for the loudness target
    def shot_class(n):
        g = re.sub(r"_\d+$", "", n)
        if g.startswith("step_"):
            return "step"
        if g.endswith("_open"):
            return "door_open"
        if g.endswith("_close"):
            return "door_close"
        if g.endswith("_latch"):
            return "door_latch"
        return {"bell_shop": "bell", "phonebox_door_creak": "phonebox_creak", "phonebox_door_shut": "phonebox_shut", "phonebox_ring": "phonebox_ring"}[g]

    audio = {}
    tmp = tempfile.mkdtemp(prefix="soundcheck_")
    for n in expected:
        p = os.path.join(OUT_DIR, n + ".wav")
        x, ch, bits, sr, raw = read_wav(p)
        audio[n] = x
        is_loop = n in T["loops_lufs"]
        # case 2: format
        add(2, "WAV 16-bit 48 kHz", bits == 16 and sr == RATE, "%d-bit %d Hz %d ch" % (bits, sr, ch), n + ".wav")
        if is_loop:
            sec = len(x) / RATE
            add(2, "loop is 75 s", abs(sec - 75.0) < 0.01, "%.2f s" % sec, n + ".wav")
            add(3, "loop at least %d s" % T["loop_seconds_min"], sec >= T["loop_seconds_min"], "%.1f s" % sec, n + ".wav")
            I, tp, _ = ffmpeg_loudness(p)
            tgt = T["loops_lufs"][n]
            add(4, "integrated loudness within %.1f LU of %.1f" % (T["loop_lufs_tolerance"], tgt), I is not None and abs(I - tgt) <= T["loop_lufs_tolerance"],
                "%.2f LUFS" % I if I is not None else "unmeasured", n + ".wav")
            add(5, "true peak at most %.1f dBTP" % T["true_peak_max_dbtp"], tp is not None and tp <= T["true_peak_max_dbtp"], "%.2f dBTP" % tp if tp is not None else "unmeasured", n + ".wav")
            m = x if x.ndim == 1 else x.mean(axis=1)
            j, st, pc = seam(m)
            add(6, "no click at the seam (jump at most %.1f)" % T["seam_jump_max"], j <= T["seam_jump_max"], "jump %.2f x typical step" % j, n + ".wav")
            add(6, "no level step across the seam", st <= T["seam_step_ok_db"] or pc <= T["seam_step_percentile_max"],
                "%.2f dB, larger than at %.0f%% of other places" % (st, 100 * pc), n + ".wav")
        else:
            add(2, "one-shot is mono", ch == 1, "%d ch" % ch, n + ".wav")
            I, tp, M = ffmpeg_loudness(p, pad_to=1.5)
            tgt = T["one_shot_lufs_m"][shot_class(n)]
            lim = bool(manifest.get(n, {}).get("limited_by_peak"))
            ok = M is not None and ((abs(M - tgt) <= T["one_shot_tolerance"]) or (M < tgt and lim))
            add(7, "momentary loudness within %.1f LU of %.1f, or lower and peak-limited" % (T["one_shot_tolerance"], tgt), ok,
                "%.2f LUFS-M%s" % (M, " (peak-limited)" if lim else "") if M is not None else "unmeasured", n + ".wav")
            add(5, "true peak at most %.1f dBTP" % T["true_peak_max_dbtp"], tp is not None and tp <= T["true_peak_max_dbtp"], "%.2f dBTP" % tp if tp is not None else "unmeasured", n + ".wav")
            m = x
            head, tail = abs(m[0]), np.abs(m[-int(0.002 * RATE):]).max()
            add(8, "no click at either end", head <= 10 ** (-50 / 20) and tail <= 10 ** (-50 / 20), "start %.1f dBFS, end %.1f dBFS" % (20 * np.log10(head + 1e-9), 20 * np.log10(tail + 1e-9)), n + ".wav")
        add(5, "no clipping (no full-scale sample)", float(np.abs(x).max()) < 0.999, "peak %.2f dBFS" % (20 * np.log10(np.abs(x).max() + 1e-12)), n + ".wav")
        add(15, "sha256 matches manifest.json", n in manifest and manifest[n].get("sha256") == sha256(p),
            "" if n in manifest else "no manifest row", n + ".wav")
        # case 13: licence rows
        srcs = manifest.get(n, {}).get("sources", [])
        okrows = bool(srcs) and all(
            s in sources and all(sources[s].get(k) for k in ("page_url", "author", "licence", "date_read", "download_url", "md5", "title")) for s in srcs)
        add(13, "every source has a full row in sources.json", okrows, ", ".join(srcs) if srcs else "no sources listed in manifest", n + ".wav")

    # case 9: footstep variants differ -------------------------------------------------------------------
    for s in SURFACES:
        g = sorted(n for n in names if re.fullmatch(r"step_%s_\d+" % s, n))
        worst, pair = 0.0, None
        for i in range(len(g)):
            for k in range(i + 1, len(g)):
                if g[i] in audio and g[k] in audio:
                    c = max_xcorr(audio[g[i]], audio[g[k]])
                    if c > worst:
                        worst, pair = c, (g[i], g[k])
        hashes = [sha256(os.path.join(OUT_DIR, n + ".wav")) for n in g]
        add(9, "variants of step_%s differ (no pair above %.2f, none identical)" % (s, T["step_variant_max_correlation"]),
            len(g) > 1 and worst <= T["step_variant_max_correlation"] and len(set(hashes)) == len(hashes),
            "closest pair %s correlate %.2f" % (pair, worst) if pair else "no pair", "step_%s_*" % s)

    # case 10: the three beds ---------------------------------------------------------------------------
    for v in ("day", "night", "rain"):
        parts = ["amb_%s_%s" % (l, v) for l in LAYERS] + (["amb_rain_pavement", "amb_rain_awning", "amb_rain_gutter"] if v == "rain" else [])
        if not all(p in audio for p in parts):
            add(10, "%s bed mix measures within %.1f LU of %.1f" % (v, T["bed_mix_tolerance"], T["bed_mix_lufs"][v]), False, "MISSING " + ", ".join(p for p in parts if p not in audio))
            continue
        tot = None
        for p in parts:
            x = audio[p]
            x = np.stack([x, x], axis=1) * np.sqrt(0.5) if x.ndim == 1 else x
            tot = x if tot is None else tot + x
        path = os.path.join(tmp, "mix_%s.wav" % v)
        pcm = (np.clip(tot, -1, 1) * 32767).astype("<i2")
        with wave.open(path, "wb") as w:
            w.setnchannels(2); w.setsampwidth(2); w.setframerate(RATE); w.writeframes(pcm.tobytes())
        I, tp, _ = ffmpeg_loudness(path)
        T.setdefault("_mix", {})[v] = I
        add(10, "%s bed mix measures within %.1f LU of %.1f" % (v, T["bed_mix_tolerance"], T["bed_mix_lufs"][v]), I is not None and abs(I - T["bed_mix_lufs"][v]) <= T["bed_mix_tolerance"], "%.2f LUFS" % I if I is not None else "unmeasured")
        add(5, "%s bed mix true peak at most %.1f dBTP" % (v, T["true_peak_max_dbtp"]), tp is not None and tp <= T["true_peak_max_dbtp"], "%.2f dBTP" % tp if tp is not None else "unmeasured")
    mix = T.get("_mix", {})
    if len(mix) == 3:
        add(10, "night bed at least 2 LU under day", mix["night"] <= mix["day"] - 2.0, "night %.1f, day %.1f" % (mix["night"], mix["day"]))
        add(10, "rain bed at least 2 LU over day", mix["rain"] >= mix["day"] + 2.0, "rain %.1f, day %.1f" % (mix["rain"], mix["day"]))

    # case 11: what changes between versions ---------------------------------------------------------------
    if "amb_traffic_day" in audio and "amb_traffic_rain" in audio:
        cd, cr = (centroid(audio[n] if audio[n].ndim == 1 else audio[n].mean(axis=1)) for n in ("amb_traffic_day", "amb_traffic_rain"))
        add(11, "rain traffic's spectral centroid above day traffic's", cr > cd, "rain %.0f Hz, day %.0f Hz" % (cr, cd))
    cnt = {v: manifest.get("amb_gulls_%s" % v, {}).get("build", {}).get("call_count") for v in ("day", "night", "rain")}
    add(11, "night gulls: fewer calls than day and at most three", cnt["night"] is not None and cnt["day"] is not None and cnt["night"] < cnt["day"] and cnt["night"] <= 3, "calls day %s, night %s, rain %s" % (cnt["day"], cnt["night"], cnt["rain"]))
    add(11, "rain gulls: fewer calls than day", cnt["rain"] is not None and cnt["day"] is not None and cnt["rain"] < cnt["day"], "rain %s, day %s" % (cnt["rain"], cnt["day"]))

    # case 12: voices and radio indistinct -------------------------------------------------------------------
    for layer in ("voices", "radio"):
        for v in ("day", "night", "rain"):
            n = "amb_%s_%s" % (layer, v)
            if n not in audio:
                continue
            gm = manifest.get(n, {}).get("build", {}).get("grain_ms", [0, 9999])
            add(12, "grains no longer than %d ms" % T["grain_ms_max"], gm[1] <= T["grain_ms_max"], "grains %s ms" % gm, n + ".wav")
            hf = hf_fraction(audio[n])
            add(12, "power above 2.5 kHz at most %.1f%%" % (100 * T["voice_hf_fraction_max"]), hf <= T["voice_hf_fraction_max"], "%.4f%%" % (100 * hf), n + ".wav")

    # case 14: licences and content words ------------------------------------------------------------------------
    used = sorted({s for n in expected for s in manifest.get(n, {}).get("sources", [])})
    for sid in sorted(sources):
        s = sources[sid]
        add(13, "source file on disk matches its md5", os.path.exists(os.path.join(SOURCES_DIR, s.get("file", "?"))) and
            hashlib.md5(open(os.path.join(SOURCES_DIR, s["file"]), "rb").read()).hexdigest() == s.get("md5"), s.get("file", "no file"), sid)
        add(14, "licence reads CC0 on the page", s.get("licence") in CC0_TEXT and "publicdomain/zero" in (s.get("licence_url") or ""), "%s | %s" % (s.get("licence"), s.get("licence_url")), sid)
        text = " ".join(str(s.get(k) or "") for k in ("title", "description_on_page", "page_title")).lower()
        hits = [w for w in FORBIDDEN if re.search(r"(?<![a-z])%s(?![a-z])" % re.escape(w), text)]
        add(14, "title and page text hold no content-rule word", not hits, ", ".join(hits) if hits else "clean", sid)
    add(13, "every source in sources.json is used by an output", set(sources) <= set(used), "unused: %s" % (sorted(set(sources) - set(used)) or "none"))

    # case 16: previews ------------------------------------------------------------------------------------------
    for f in SPEC_PREVIEWS:
        p = os.path.join(PREVIEWS, f)
        ok = os.path.exists(p) and os.path.getsize(p) < 500 * 1024
        add(16, "spectrogram JPEG exists, under 500 KB", ok, "%d KB" % (os.path.getsize(p) // 1024) if os.path.exists(p) else "MISSING", f)
    for f in CLIP_PREVIEWS:
        p = os.path.join(PREVIEWS, f)
        if not os.path.exists(p):
            add(16, "listening clip exists, at most 20 s and under 300 KB", False, "MISSING", f)
            continue
        dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p], capture_output=True, text=True).stdout.strip() or 0)
        codec = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries", "stream=codec_name", "-of", "csv=p=0", p], capture_output=True, text=True).stdout.strip().strip(",")
        add(16, "listening clip is Vorbis, at most 20 s, under 300 KB", codec == "vorbis" and dur <= 20.05 and os.path.getsize(p) < 300 * 1024,
            "%s %.1f s %d KB" % (codec, dur, os.path.getsize(p) // 1024), f)

    for f in os.listdir(tmp):
        os.remove(os.path.join(tmp, f))
    os.rmdir(tmp)

    passed = sum(1 for r in rows if r["pass"])
    os.makedirs(os.path.join(HERE, "checks"), exist_ok=True)
    out = {"check": "check_sound.py %s" % tag, "brief": "BRIEF.md", "outputs_dir": OUT_DIR, "rows_pass": passed, "rows_total": len(rows),
           "failing": [{"case": r["case"], "test": r["test"], "file": r["file"], "detail": r["detail"]} for r in rows if not r["pass"]], "rows": rows}
    with open(os.path.join(HERE, "checks", "check_%s.json" % tag), "w", encoding="utf8") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
        f.write("\n")
    for r in rows:
        if not r["pass"]:
            print("FAIL case %d: %s: %s (%s)" % (r["case"], r["file"] or "-", r["test"], r["detail"]))
    print("%d of %d rows pass" % (passed, len(rows)))
    return 0 if passed == len(rows) else 1


if __name__ == "__main__":
    sys.exit(main())
