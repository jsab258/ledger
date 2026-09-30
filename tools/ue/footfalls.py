#!/usr/bin/env python3
"""When each of Tom's feet lands in his walk and run clips, read from the glb.

    python tools/ue/footfalls.py              # prints the footfall times
    python tools/ue/footfalls.py --selftest   # and checks SliceCharacter.h holds them

WHY, 30 September. The game first timed Tom's footsteps from his feet's
heights as he moved; three reviewers heard the run limp, because the height
watcher caught one foot a little earlier than the other, and kerbs moved it
further. The clips are fixed, so the footfalls are too: this measures them
once from production/assets/people/tom-player.glb, and the game sounds a
step as each clip's own play position passes them (SliceCharacter.cpp
StepTick), evenly whatever the street does under him.

A FOOTFALL is the moment the foot stops swinging forward and starts moving
back under the body: in a clip made in place, the planted foot slides back
at the walking speed, so the landing is where its forward travel peaks (the
heel strike in the walk, the ball in this run). The first rule tried, the
foot's lowest point coming to rest, found the walk's foot going flat about
150 ms after the heel struck, and a second dip mid-swing. Keys are read as
the file holds them (30 a second) and the peak placed between them by a
parabola.
"""
import json
import os
import re
import struct
import sys

import numpy as np

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
GLB = os.path.join(REPO, "production", "assets", "people", "tom-player.glb")
HEADER = os.path.join(REPO, "ue-probe", "Source", "LedgerProbe", "Public", "SliceCharacter.h")
CLIPS = {"walk": "tom-player__walk", "run": "tom-player__run"}
FEET = (("mixamorig7:LeftFoot", "mixamorig7:LeftToeBase"), ("mixamorig7:RightFoot", "mixamorig7:RightToeBase"))


def load(path):
    b = open(path, "rb").read()
    n = struct.unpack("<I", b[12:16])[0]
    j = json.loads(b[20:20 + n])
    off = 20 + n
    bl = struct.unpack("<I", b[off:off + 4])[0]
    return j, b[off + 8:off + 8 + bl]


def footfalls(path=GLB):
    j, blob = load(path)

    def acc(i):
        a = j["accessors"][i]
        bv = j["bufferViews"][a["bufferView"]]
        k = {"SCALAR": 1, "VEC3": 3, "VEC4": 4}[a["type"]]
        return np.frombuffer(blob, dtype=np.float32, count=a["count"] * k,
                             offset=bv.get("byteOffset", 0) + a.get("byteOffset", 0)).reshape(a["count"], k)

    nodes = j["nodes"]
    parent = {c: i for i, nd in enumerate(nodes) for c in nd.get("children", [])}
    names = {nd.get("name"): i for i, nd in enumerate(nodes)}

    def rot(q):
        x, y, z, w = q / np.linalg.norm(q)
        return np.array([[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
                         [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
                         [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]])

    def world(i, pose, cache):
        if i in cache:
            return cache[i]
        nd = nodes[i]
        m = np.eye(4)
        m[:3, :3] = rot(np.array(pose.get((i, "rotation"), nd.get("rotation", [0, 0, 0, 1])), float)) \
            * np.array(pose.get((i, "scale"), nd.get("scale", [1, 1, 1])), float)
        m[:3, 3] = pose.get((i, "translation"), nd.get("translation", [0, 0, 0]))
        if i in parent:
            m = world(parent[i], pose, cache) @ m
        cache[i] = m
        return m

    out = {}
    for label, clip in CLIPS.items():
        an = [a for a in j["animations"] if a["name"] == clip][0]
        chans = [(c["target"]["node"], c["target"]["path"], acc(an["samplers"][c["sampler"]]["input"])[:, 0],
                  acc(an["samplers"][c["sampler"]]["output"])) for c in an["channels"]]
        length = float(max(t[-1] for _, _, t, _ in chans))
        times = np.array(sorted(set(np.round(np.concatenate([ti for _, _, ti, _ in chans]), 5))))
        falls = []
        for ankle, toe in FEET:
            pos, low = [], []
            for t in times:
                pose = {}
                for nd, p, ti, v in chans:
                    pose[(nd, p)] = v[int(np.argmin(np.abs(ti - t)))]
                cache = {}
                a = world(names[ankle], pose, cache)[:3, 3]
                b = world(names[toe], pose, cache)[:3, 3]
                pos.append((a[0], a[2]))
                low.append(min(a[1], b[1]))
            xz = np.array(pos) - np.mean(pos, axis=0)
            axis = np.linalg.svd(xz, full_matrices=False)[2][0]
            fwd = xz @ axis
            low = np.array(low)
            # Forward is the way the foot moves while it is up; the planted foot goes back.
            vel = np.gradient(fwd, times)
            if np.median(vel[low < np.percentile(low, 40)]) > 0:
                fwd = -fwd
            i = int(np.argmax(fwd))
            n = len(fwd)
            y0, y1, y2 = fwd[(i - 1) % n], fwd[i], fwd[(i + 1) % n]
            den = y0 - 2 * y1 + y2
            shift = 0.5 * (y0 - y2) / den if den != 0 else 0.0
            step = times[1] - times[0]
            falls.append(round(float((times[i] + shift * step) % length), 3))
        # EVENED, half a clip apart: the run's landings came out 0.525 and 0.575
        # of its 1.1 s (the left foot's forward travel peaks flat over three
        # keys), which a reviewer hears as a limp. Each moves by half the
        # difference, at most 13 ms, too little for the eye to pair with the ear.
        gap = (falls[1] - falls[0]) % length
        nudge = (length / 2.0 - gap) / 2.0
        falls = [round((falls[0] - nudge) % length, 3), round((falls[1] + nudge) % length, 3)]
        out[label] = {"length": round(length, 3), "left": falls[0], "right": falls[1], "moved_ms": round(abs(nudge) * 1000, 1)}
    return out


def header_values(path=HEADER):
    text = open(path, encoding="utf-8").read()
    got = {}
    for label in CLIPS:
        m = re.search(r"%sFootfallS\[2\]\s*=\s*\{\s*([\d.]+)f,\s*([\d.]+)f\s*\}" % label.capitalize(), text)
        if m:
            got[label] = (float(m.group(1)), float(m.group(2)))
    return got


def selftest():
    f = footfalls()
    h = header_values()
    failed = 0
    for label in CLIPS:
        want = (f[label]["left"], f[label]["right"])
        have = h.get(label)
        ok = have is not None and all(abs(a - b) <= 0.02 for a, b in zip(want, have))
        # The two feet half a clip apart once evened, and never moved more than
        # a sound can be late and still belong to its foot.
        gap = (f[label]["right"] - f[label]["left"]) % f[label]["length"]
        even = abs(gap / f[label]["length"] - 0.5) < 0.01 and f[label]["moved_ms"] <= 20.0
        for name, cond, detail in (("%s footfalls in SliceCharacter.h" % label, ok, "file %s header %s" % (want, have)),
                                   ("%s feet half a stride apart, moved at most 20 ms" % label, even, "%.2f of the clip" % (gap / f[label]["length"]))):
            if not cond:
                failed += 1
                print("footfalls selftest FAIL %s: %s" % (name, detail))
    print("footfalls selftest: passed=%d/4 failed=%d" % (4 - failed, failed))
    return 1 if failed else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    print(json.dumps(footfalls(), indent=2))
