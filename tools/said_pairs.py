#!/usr/bin/env python3
"""The thinking sounds' faces, two ways, as blind pairs for the day's page (item 4, 1 October).

    python tools/said_pairs.py MADE_LOG MADE_FILM LOUD_LOG LOUD_FILM OUT_DIR KEY.json
    python tools/said_pairs.py FACEAB_LOG FILM OUT_DIR KEY.json      # one -FaceAB run, both ways in it

Two runs of the game with -MouthFilm, the same lines put to the same people:
one with -MadeFace (the face Epic's MetaHuman Animator made from its sound),
one without (the mouth following the sound's loudness, which the game plays
since his blind picks of 1 October). Each run's log names every thinking sound with
the film frame it started at and the frame it ended at ("LedgerAck: rocco
says let-me-think, 1.03 s, film frame 0, ..." then "LedgerAck: done (film
frame 11)"); MADE_FILM and LOUD_FILM are the runs' Saved/MouthFilm folders.

For each line found in both runs it writes the two sprites (tools/said_sprite.py)
under OUT_DIR, A and B drawn at random per line, and the key (which letter is
which) to KEY.json, never to the page. Prints the clips for page.json.
"""
import json
import os
import random
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import said_sprite  # noqa: E402

SAYS = re.compile(r"LedgerAck: (\w+) says ([\w-]+), ([\d.]+) s, film frame (\d+)")
ENDS = re.compile(r"LedgerAck: (?:done|cut off by the answer) \(film frame (\d+)\)")
WHO_FILM = {"rocco": "BP_MH_RoccoP2_C_0", "sam": "BP_MH_SamC5_C_0"}
WORDS = {"let-me-think": "Let me think.", "well-now": "Well now.", "hmm-well-now": "Hmm. Well now."}


def acks(log_text):
    """(card, sound, seconds, first frame, frame after the last), in the order said."""
    out, open_one = [], None
    for line in log_text.splitlines():
        m = SAYS.search(line)
        if m:
            open_one = [m.group(1), m.group(2), float(m.group(3)), int(m.group(4))]
            continue
        e = ENDS.search(line)
        if e and open_one is not None:
            out.append((open_one[0], open_one[1], open_one[2], open_one[3], int(e.group(1))))
            open_one = None
    return out


def last_takes(log_path):
    """Each sound's last time said (the film camera already running), as {(card, sound): (seconds, a, b)}."""
    got = {}
    for c, s, secs, a, b in acks(open(log_path, encoding="utf-8", errors="replace").read()):
        got[(c, s)] = (secs, a, b)
    return got


WAY = re.compile(r"LedgerFaceAB: (\w+) sound \d+, (made|loudness)")


def faceab_takes(log_text):
    """From one -FaceAB run: {way: {(card, sound): (seconds, a, b)}}, each
    take's way read from the line the game logs just before it."""
    ways, way = {"made": {}, "loudness": {}}, None
    pending = None
    for line in log_text.splitlines():
        w = WAY.search(line)
        if w:
            way = w.group(2)
            continue
        m = SAYS.search(line)
        if m and way is not None:
            pending = (way, m.group(1), m.group(2), float(m.group(3)), int(m.group(4)))
            continue
        e = ENDS.search(line)
        if e and pending is not None:
            ways[pending[0]][(pending[1], pending[2])] = (pending[3], pending[4], int(e.group(1)))
            pending, way = None, None
    return ways


def main(argv):
    if len(argv) == 4:
        log, film, out_dir, key_path = argv
        got = faceab_takes(open(log, encoding="utf-8", errors="replace").read())
        made, loud, made_film, loud_film = got["made"], got["loudness"], film, film
    else:
        made_log, made_film, loud_log, loud_film, out_dir, key_path = argv[:6]
        made, loud = last_takes(made_log), last_takes(loud_log)
    rng = random.Random(20261001)
    key, clips = {}, []
    for (card, sound) in sorted(set(made) & set(loud)):
        ways = [("made", made_film, made[(card, sound)]), ("loudness", loud_film, loud[(card, sound)])]
        rng.shuffle(ways)
        for label, (way, film, (secs, a, b)) in zip("AB", ways):
            out = os.path.join(out_dir, "%s-%s-%s.jpg" % (card, sound, label))
            # FRAMES BY NUMBER: one counter runs across everyone filmed, so a
            # person's folder holds only their own numbers.
            files = [f for f in (os.path.join(film, WHO_FILM[card], "f_%03d.png" % k) for k in range(a, b)) if os.path.exists(f)]
            sprite = said_sprite.make_files(files, out, max(1, round(len(files) / secs)))
            key["%s/%s/%s" % (card, sound, label)] = way
            clips.append({"card": card, "label": label, "line": WORDS.get(sound, sound),
                          "audio": "content/voice/acks/%s/%s.wav" % (card, sound), "sprite": sprite})
    with open(key_path, "w", encoding="utf-8") as fh:
        json.dump({"what": "which take of each thinking sound's face is which; never on the page", "key": key}, fh, indent=1)
    print(json.dumps(clips, indent=1))
    return 0


def selftest():
    log = ("x LedgerAck: rocco says let-me-think, 1.03 s, film frame 0, face its own\n"
           "x LedgerAck: done (film frame 11)\nx LedgerAck: sam says hmm-well-now, 1.25 s, film frame 40, face its own\n"
           "x LedgerAck: cut off by the answer (film frame 52)\n")
    got = acks(log)
    ok = got == [("rocco", "let-me-think", 1.03, 0, 11), ("sam", "hmm-well-now", 1.25, 40, 52)]
    ab = faceab_takes("x LedgerFaceAB: rocco sound 0, made, at D0 10:15\n" + log.splitlines()[0] + "\n" + log.splitlines()[1] + "\n"
                      "x LedgerFaceAB: rocco sound 0, loudness, at D0 10:20\n"
                      "x LedgerAck: rocco says let-me-think, 1.03 s, film frame 11, face its mouth\nx LedgerAck: done (film frame 22)\n")
    ok = ok and ab["made"] == {("rocco", "let-me-think"): (1.03, 0, 11)} and ab["loudness"] == {("rocco", "let-me-think"): (1.03, 11, 22)}
    print("said_pairs selftest: %s" % ("passed=1/1 failed=0" if ok else "FAIL " + repr(got)))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else main(sys.argv[1:]))
