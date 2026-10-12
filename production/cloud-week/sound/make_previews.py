#!/usr/bin/env python3
"""Previews of Quay Street's sound, for the fresh listener and for Jafar (unit 10, cloud week 42).

    python make_previews.py            # reads the WAVs in SOUND_OUT, writes production/previews/cloud-week/sound/
    python make_previews.py --clips-only   # only the listening clips (the spectrograms take several minutes; make_sound.py runs this itself)

  spec_<layer>.jpg          a spectrogram of each layer, its day, night and rain versions stacked (spec_rain.jpg: the three rains)
  spec_steps_<surface>.jpg  the eight variants of each footstep surface in a row
  spec_doors_*.jpg, spec_bell.jpg, spec_phonebox.jpg   the door, bell and phone-box one-shots in a row
  clip_mix_{day,night,rain}.ogg   (audio is not committed: .gitignore lists *.ogg; make_clips) 20 s of each bed: its layers summed at their own levels (mono layers centred), one gain for all three
  clip_steps_<surface>.ogg        the eight variants of a surface, walked
  clip_doors.ogg                  shop door, bell, house door, phone box

Spectrograms are ffmpeg's showspectrumpic (1600 px wide, JPEG under 500 KB; the top of each picture is set by resampling, not by its `stop` option, which drew a false line, see spec_png). Clips are Ogg Vorbis, at most 20 s, under 300 KB.
The mix clips carry +10 dB over the real levels, with a peak limiter at -1 dBFS, so that they are audible at an ordinary
listening volume: they are for judging what is in each bed and how the beds differ, not the game's levels.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile
import wave

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.environ.get("SOUND_OUT", "/home/user/ledger-scratch/sound-out")
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
PREV = os.path.join(REPO, "production", "previews", "cloud-week", "sound")
RATE = 48000
LAYERS = ["traffic", "gulls", "harbour", "wind", "voices", "radio"]
SURFACES = ["paving", "setts", "asphalt", "wet", "wood"]
MIX_GAIN_DB = 10.0
CLIPS = ["clip_mix_day.ogg", "clip_mix_night.ogg", "clip_mix_rain.ogg"] + ["clip_steps_%s.ogg" % s for s in SURFACES] + ["clip_doors.ogg"]


def rd(name):
    with wave.open(os.path.join(OUT_DIR, name + ".wav"), "rb") as w:
        ch, n = w.getnchannels(), w.getnframes()
        a = np.frombuffer(w.readframes(n), dtype="<i2").astype(np.float64) / 32768.0
    return a.reshape(-1, ch) if ch > 1 else a


def wr(path, x):
    x = np.asarray(x)
    pcm = np.clip(np.round(x * 32767), -32768, 32767).astype("<i2")
    with wave.open(path, "wb") as w:
        w.setnchannels(1 if pcm.ndim == 1 else pcm.shape[1])
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(pcm.tobytes())


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        raise SystemExit("make_previews: %s\n%s" % (" ".join(cmd), r.stderr[-800:]))


def spec_png(wav, png, height, stop_hz):
    """ffmpeg's showspectrumpic, the top of the picture set by the sample rate (twice stop_hz) and not by its `stop` option:
    with `stop`, every picture carried a false bright line a tenth of the way up (960 Hz on a 10 kHz panel, 1.2 kHz on a 12 kHz one;
    pink noise shows it too; the first build's NOTES.md took it for sound). Without `stop` the line is gone (checked on pink noise)."""
    run(["ffmpeg", "-v", "error", "-y", "-i", wav, "-lavfi",
         "aresample=%d,showspectrumpic=s=1600x%d:mode=combined:legend=1:scale=log:drange=80:color=viridis" % (2 * stop_hz, height), "-update", "1", png])


def stack_jpeg(wavs, out, height, stop_hz, tmp):
    pngs = []
    for i, w in enumerate(wavs):
        p = os.path.join(tmp, "s%d.png" % i)
        spec_png(w, p, height, stop_hz)
        pngs.append(p)
    q = 4
    while True:
        cmd = ["ffmpeg", "-v", "error", "-y"]
        for p in pngs:
            cmd += ["-i", p]
        if len(pngs) > 1:
            cmd += ["-filter_complex", "".join("[%d:v]" % i for i in range(len(pngs))) + "vstack=inputs=%d,scale=1600:-2" % len(pngs)]
        else:
            cmd += ["-vf", "scale=1600:-2"]
        cmd += ["-q:v", str(q), "-update", "1", out]
        run(cmd)
        if os.path.getsize(out) < 480 * 1024 or q >= 12:
            break
        q += 2


def sequence(names, gap_s=0.45, lead_s=0.15, max_s=None):
    parts = [np.zeros(int(lead_s * RATE))]
    for n in names:
        x = rd(n)
        parts += [x, np.zeros(int(gap_s * RATE))]
    y = np.concatenate(parts)
    return y[:int(max_s * RATE)] if max_s else y


def encode_ogg(x, out, quality, tmp, limit=False, gain_db=0.0, max_kb=290):
    """Ogg Vorbis at the given quality, or the highest lower one that keeps the file under max_kb (rain is noise: it compresses badly)."""
    wav = os.path.join(tmp, "clip.wav")
    wr(wav, x)
    af = []
    if gain_db:
        af.append("volume=%gdB" % gain_db)
    if limit:
        af.append("alimiter=limit=0.89:attack=5:release=60:level=disabled")
    q = quality
    while True:
        cmd = ["ffmpeg", "-v", "error", "-y", "-i", wav]
        if af:
            cmd += ["-af", ",".join(af)]
        cmd += ["-c:a", "libvorbis", "-q:a", str(q), out]
        run(cmd)
        if os.path.getsize(out) < max_kb * 1024 or q <= -1:
            break
        q -= 1


def make_clips():
    """The nine listening clips. Audio does not go into git (the size guard refuses it): they are written beside the JPEGs in
    production/previews/cloud-week/sound/ (kept out of git by the .gitignore there: `*.ogg`) and copied to SOUND_OUT/clips/, and make_sound.py makes them
    at the end of a full run, so one command rebuilds the WAVs and the clips."""
    os.makedirs(PREV, exist_ok=True)
    tmp = tempfile.mkdtemp(prefix="soundclips_")
    allnames = sorted(f[:-4] for f in os.listdir(OUT_DIR) if f.endswith(".wav"))
    try:
        # mix clips: layers at their own levels, one gain for all three
        for v in ("day", "night", "rain"):
            parts = ["amb_%s_%s" % (l, v) for l in LAYERS] + (["amb_rain_pavement", "amb_rain_awning", "amb_rain_gutter"] if v == "rain" else [])
            tot = None
            for p in parts:
                x = rd(p)
                x = np.stack([x, x], axis=1) * np.sqrt(0.5) if x.ndim == 1 else x
                x = np.concatenate([x] * (-(-int(28 * RATE) // len(x))))[:int(28 * RATE)]     # loops of 60 and 75 s: each repeated as far as the clip needs
                tot = x if tot is None else tot + x
            clip = tot[int(8 * RATE):int(28 * RATE)]
            clip = clip * np.minimum(1.0, np.linspace(0, 1, len(clip)) * 20.0)[:, None] * np.minimum(1.0, np.linspace(1, 0, len(clip)) * 20.0)[:, None]
            encode_ogg(clip, os.path.join(PREV, "clip_mix_%s.ogg" % v), 2, tmp, limit=True, gain_db=MIX_GAIN_DB)
        # footsteps walked
        for s in SURFACES:
            names = [n for n in allnames if n.startswith("step_%s_" % s)]
            encode_ogg(sequence(names, gap_s=0.5, max_s=19.5), os.path.join(PREV, "clip_steps_%s.ogg" % s), 4, tmp)
        # doors, bell, phone box
        order = ["door_shop_latch_01", "door_shop_open_01", "bell_shop_02", "door_shop_close_02", "door_house_latch_01", "door_house_open_01",
                 "door_house_close_02", "phonebox_door_creak_01", "phonebox_door_shut_01", "phonebox_ring_01"]
        encode_ogg(sequence([n for n in order if n in allnames], gap_s=0.7, max_s=19.8), os.path.join(PREV, "clip_doors.ogg"), 4, tmp)
    finally:
        for f in os.listdir(tmp):
            os.remove(os.path.join(tmp, f))
        os.rmdir(tmp)
    dest = os.path.join(OUT_DIR, "clips")
    os.makedirs(dest, exist_ok=True)
    for f in CLIPS:
        shutil.copyfile(os.path.join(PREV, f), os.path.join(dest, f))


def main():
    os.makedirs(PREV, exist_ok=True)
    tmp = tempfile.mkdtemp(prefix="soundprev_")
    clips_only = "--clips-only" in sys.argv       # re-make only the listening clips (the spectrograms take minutes)
    try:
        w = lambda n: os.path.join(OUT_DIR, n + ".wav")
        # layer spectrograms
        for layer in ([] if clips_only else LAYERS):
            stack_jpeg([w("amb_%s_%s" % (layer, v)) for v in ("day", "night", "rain")], os.path.join(PREV, "spec_%s.jpg" % layer), 250, 10000, tmp)
        if not clips_only:
            stack_jpeg([w("amb_rain_pavement"), w("amb_rain_awning"), w("amb_rain_gutter")], os.path.join(PREV, "spec_rain.jpg"), 250, 14000, tmp)
        # one-shot sets in a row
        sets = {"spec_doors_shop.jpg": ("door_shop_", None), "spec_doors_house.jpg": ("door_house_", None), "spec_bell.jpg": ("bell_shop_", None),
                "spec_phonebox.jpg": ("phonebox_", None)}
        for s in SURFACES:
            sets["spec_steps_%s.jpg" % s] = ("step_%s_" % s, None)
        allnames = sorted(f[:-4] for f in os.listdir(OUT_DIR) if f.endswith(".wav"))
        for out, (prefix, _) in ({} if clips_only else sets).items():
            names = [n for n in allnames if n.startswith(prefix)]
            seq = sequence(names, gap_s=0.3 if prefix.startswith("step_") else 0.6)
            wav = os.path.join(tmp, "seq.wav")
            wr(wav, seq)
            stack_jpeg([wav], os.path.join(PREV, out), 360, 12000, tmp)
    finally:
        for f in os.listdir(tmp):
            os.remove(os.path.join(tmp, f))
        os.rmdir(tmp)
    make_clips()
    tot = 0
    for f in sorted(os.listdir(PREV)):
        sz = os.path.getsize(os.path.join(PREV, f))
        tot += sz
        print("%-28s %4d KB" % (f, sz // 1024))
    print("%d files, %d KB in %s" % (len(os.listdir(PREV)), tot // 1024, PREV))


if __name__ == "__main__":
    main()
