#!/usr/bin/env python3
"""THE GUARD A COMMENT PROMISED AND NOBODY HAD WRITTEN.

    python3 tools/surface-tint-check.py
    python3 tools/surface-tint-check.py --selftest

WHY IT EXISTS. ue-probe/Source/LedgerProbe/Public/SurfaceBind.h carries a
SECOND COPY of the procedural surface tints, whose first copy is the switch
in ledger/Assets/Scripts/Game/AssetLibrary.cs. The comment beside the copy
says, in its own words, that this tool "parses both files and refuses any
disagreement" and that the check "is the only thing that makes this table
trustworthy; a copied constant with no check over it is a constant that
drifts". THE TOOL DID NOT EXIST. The builder that added the table said so
plainly rather than leaving it, which is the only reason it is here.

A COMMENT PROMISING A GUARD IS NOT A GUARD. Until this ran, the two copies
of 0.18/0.13/0.08 and 0.78/0.66/0.18 were unguarded while the file claimed
they were guarded, which is worse than an ordinary duplicate: a reader who
believed the comment would not check.

WHICH SIDE IS AUTHORITATIVE. Unity's switch. D1 is a comparison between two
engines and the Unity street is the one that has shipped, so the C# value is
the fact and the C++ table is the copy. A disagreement is therefore reported
as the UE table being wrong, whichever was edited last.

WHAT IT DOES NOT CHECK, said so nobody reads more into a pass than is there:
only the TINTS of the procedural surfaces. Smoothness, emission, tiling and
pattern are copied too and are not compared here; the same shape of check
would cover them and the next hand to touch this file should widen it rather
than trust a green line about a narrower thing.

SINCE QUEUE 186 A SECOND LINE COMPARES THE WETNESS COPIES: the dry
smoothness of the four ground surfaces against AssetLibrary.SurfaceSpec,
and the 0.92 ceiling and 0.45 albedo slope against Core/LightModel.cs,
each with its own denominator. The smoothness of the two procedural
surfaces is still not compared, and the tint line's tintsOnly token is
about that table alone.
"""
import argparse
import pathlib
import re
import sys

# PATHS RESOLVE AGAINST THE REPOSITORY, NEVER THE WORKING DIRECTORY, and this
# file is the reason the rule is written down twice in this project. The first
# wiring of this tool into ledger/verify.py failed instantly with NOTHING
# MEASURED, because verify runs it from a different cwd and these were relative
# strings. The gate caught the tool's own bug the hour the tool was wired, which
# is the argument for wiring a guard immediately rather than "next session".
ROOT = pathlib.Path(__file__).resolve().parent.parent
UE = "ue-probe/Source/LedgerProbe/Public/SurfaceBind.h"
UNITY = "ledger/Assets/Scripts/Game/AssetLibrary.cs"
# THE THIRD FILE, ADDED BY QUEUE 186's WETNESS RUNG. SurfaceBind.h now carries
# a second copy of TWO MORE THINGS, and an unguarded copy is the fault this
# whole tool exists for. The docstring above says the next hand to touch this
# file should WIDEN it rather than trust a green line about a narrower thing;
# this is that widening.
#   the dry smoothness of the four ground surfaces -> AssetLibrary.SurfaceSpec
#   the 0.92 wet ceiling and the 0.45 albedo slope -> Core/LightModel.cs
UNITY_LIGHT = "ledger/Assets/Scripts/Core/LightModel.cs"
# The C# names are CamelCase, the C++ names are the spec's snake_case. The
# mapping is stated here rather than derived because it is the one thing the
# two files legitimately spell differently.
NAME_MAP = {"Interior": "interior", "PaintYellow": "paint_yellow"}


def parse_ue(text):
    """The C++ copy: an index-to-name array and a parallel tint table."""
    names = re.search(r'ProceduralSurfaceName\(int I\).*?\{.*?\{(.*?)\}',
                      text, re.S)
    tints = re.search(r'ProceduralSurfaceTint\(.*?const double T\[\d+\]\[3\]'
                      r'\s*=\s*\{(.*?)\};', text, re.S)
    if not names or not tints:
        return None, "the UE table did not parse"
    order = re.findall(r'"([a-z_]+)"', names.group(1))
    rows = re.findall(r'\{\s*([0-9.]+)\s*,\s*([0-9.]+)\s*,\s*([0-9.]+)\s*\}',
                      tints.group(1))
    if len(order) != len(rows):
        return None, ("the UE name list and tint table are different lengths: "
                      "%d name(s) against %d row(s)" % (len(order), len(rows)))
    return {n: tuple(float(v) for v in r) for n, r in zip(order, rows)}, None


def parse_unity(text):
    """The C# original: one case per surface, the tint its first Color."""
    out = {}
    for cs_name, spec_name in NAME_MAP.items():
        m = re.search(r'case\s+AssetLibrary\.' + cs_name +
                      r'\s*:.*?Make\(\s*new\s+Color\(\s*([0-9.]+)f\s*,\s*'
                      r'([0-9.]+)f\s*,\s*([0-9.]+)f\s*\)', text, re.S)
        if m:
            out[spec_name] = tuple(float(g) for g in m.groups())
    return out


def compare(ue, unity):
    """Findings, and the denominator is what was COMPARED, not what exists."""
    findings, compared = [], 0
    for name, u in sorted(unity.items()):
        if name not in ue:
            findings.append("%s: in the Unity switch and NOT in the UE table"
                            % name)
            continue
        compared += 1
        if ue[name] != u:
            findings.append(
                "%s: unity=%s ue=%s -- the UE table is the copy and is wrong"
                % (name, "/".join("%.4f" % v for v in u),
                   "/".join("%.4f" % v for v in ue[name])))
    for name in sorted(ue):
        if name not in unity:
            findings.append("%s: in the UE table and NOT in the Unity switch"
                            % name)
    return findings, compared


# ---- THE WETNESS CONSTANTS, QUEUE 186 --------------------------------------
#
# WHICH SIDE IS AUTHORITATIVE is unchanged and is the same argument: the C#
# has shipped, the C++ is the copy, and a disagreement is reported as the UE
# side being wrong whichever was edited last.

# The four surfaces rain lands on. C# name -> the spec's snake_case, exactly
# the shape NAME_MAP has, kept separate because these four are a DIFFERENT
# table in the same switch and merging them would make one denominator mean
# two things.
GROUND_MAP = {"Asphalt": "asphalt", "Sidewalk": "sidewalk",
              "Kerb": "kerb", "Concrete": "concrete"}


def parse_ue_ground(text):
    """The C++ copy: a name array and a parallel dry-smoothness table."""
    names = re.search(r'GroundDryName\(int I\).*?\{.*?\{(.*?)\}', text, re.S)
    vals = re.search(r'GroundDrySmoothnessAt\(.*?const double S\[\d+\]'
                     r'\s*=\s*\{(.*?)\};', text, re.S)
    if not names or not vals:
        return None, "the UE ground table did not parse"
    order = re.findall(r'"([a-z_]+)"', names.group(1))
    rows = re.findall(r'([0-9.]+)', vals.group(1))
    if len(order) != len(rows):
        return None, ("the UE ground name list and smoothness table are "
                      "different lengths: %d name(s) against %d row(s)"
                      % (len(order), len(rows)))
    return {n: float(v) for n, v in zip(order, rows)}, None


def parse_unity_ground(text):
    """The C# original: Make(new Color(...), <smoothness>f, ...) per case."""
    out = {}
    for cs_name, spec_name in GROUND_MAP.items():
        m = re.search(r'case\s+AssetLibrary\.' + cs_name +
                      r'\s*:.*?Make\(\s*new\s+Color\([^)]*\)\s*,\s*'
                      r'([0-9.]+)f', text, re.S)
        if m:
            out[spec_name] = float(m.group(1))
    return out


def parse_ue_wet_constants(text):
    """The two scalars of the wetness arithmetic, off the UE side."""
    out = {}
    m = re.search(r'WetSmoothnessCeiling\(\)\s*\{\s*return\s*([0-9.]+)\s*;',
                  text)
    if m:
        out["ceiling"] = float(m.group(1))
    m = re.search(r'WetClamp\(1\.0\s*-\s*([0-9.]+)\s*\*\s*Rain', text)
    if m:
        out["albedoSlope"] = float(m.group(1))
    return out


def parse_unity_wet_constants(text):
    """The same two out of Core/LightModel.cs, which is where they were
    written first: the 0.92 inside Smoothness and the 0.45 inside
    AlbedoScale."""
    out = {}
    m = re.search(r'Clamp01\(dry\s*\+\s*\(([0-9.]+)\s*-\s*dry\)\s*\*\s*rain\)',
                  text)
    if m:
        out["ceiling"] = float(m.group(1))
    m = re.search(r'Clamp\(1\.0\s*-\s*([0-9.]+)\s*\*\s*rain', text)
    if m:
        out["albedoSlope"] = float(m.group(1))
    return out


def compare_numbers(ue, unity, what):
    """Findings and the denominator is what was COMPARED, the same rule the
    tint comparison follows. Floats compared with a tolerance, because both
    sides are decimal literals read out of source and 0.18f is not 0.18."""
    findings, compared = [], 0
    for name in sorted(unity):
        if name not in ue:
            findings.append("%s %s: in the Unity source and NOT in the UE copy"
                            % (what, name))
            continue
        compared += 1
        if abs(ue[name] - unity[name]) > 1e-9:
            findings.append("%s %s: unity=%.6f ue=%.6f -- the UE copy is wrong"
                            % (what, name, unity[name], ue[name]))
    for name in sorted(ue):
        if name not in unity:
            findings.append("%s %s: in the UE copy and NOT in the Unity source"
                            % (what, name))
    return findings, compared


def run(root=None):
    root = pathlib.Path(root) if root else ROOT
    up, np_ = root / UE, root / UNITY
    for p in (up, np_):
        if not p.exists():
            print("surface-tint-check: NOTHING MEASURED, %s is not on disk" % p)
            return 2
    ue_text = up.read_text(encoding="utf-8")
    unity_text = np_.read_text(encoding="utf-8")
    ue, err = parse_ue(ue_text)
    if err:
        print("surface-tint-check: NOTHING MEASURED, %s" % err)
        return 2
    unity = parse_unity(unity_text)
    if not unity:
        print("surface-tint-check: NOTHING MEASURED, the Unity switch did not "
              "parse")
        return 2
    findings, compared = compare(ue, unity)
    if findings:
        print("surface-tint-check: FAIL %d disagreement(s) over %d surface(s) "
              "compared" % (len(findings), compared))
        for f in findings:
            print("   ", f)
        return 1
    print("surface-tint-check: ok - %d surface(s) compared, 0 disagreement(s), "
          "tintsOnly=yes/smoothness-emission-tiling-pattern-not-compared"
          % compared)
    # ---- AND THE WETNESS COPIES, ON THEIR OWN LINE WITH THEIR OWN
    # DENOMINATOR. A separate line because one key may not mean two things:
    # "surface(s) compared" already names the tint table and ledger/verify.py
    # reads that number off this output.
    lm = root / UNITY_LIGHT
    ue_ground, gerr = parse_ue_ground(ue_text)
    wet_findings, wet_compared = [], 0
    if gerr:
        print("surface-tint-check: NOTHING MEASURED for the ground table, %s"
              % gerr)
        return 2
    f, c = compare_numbers(ue_ground, parse_unity_ground(unity_text),
                           "drySmoothness")
    wet_findings += f
    wet_compared += c
    if not lm.exists():
        print("surface-tint-check: NOTHING MEASURED for the wetness scalars, "
              "%s is not on disk" % lm)
        return 2
    lm_text = lm.read_text(encoding="utf-8")
    ue_wet = parse_ue_wet_constants(ue_text)
    unity_wet = parse_unity_wet_constants(lm_text)
    if len(unity_wet) != 2:
        print("surface-tint-check: NOTHING MEASURED for the wetness scalars, "
              "Core/LightModel.cs gave %d of 2" % len(unity_wet))
        return 2
    f, c = compare_numbers(ue_wet, unity_wet, "wetConstant")
    wet_findings += f
    wet_compared += c
    if wet_findings:
        print("surface-tint-check: FAIL %d disagreement(s) over %d wetness "
              "constant(s) compared" % (len(wet_findings), wet_compared))
        for x in wet_findings:
            print("   ", x)
        return 1
    print("surface-tint-check: ok - %d wetness constant(s) compared, 0 "
          "disagreement(s), wetCovers=drySmoothness-of-the-four-ground-"
          "surfaces/the-0.92-ceiling/the-0.45-albedo-slope"
          % wet_compared)
    return 0


def selftest():
    checks, fails = 0, []

    def ck(name, ok, why=""):
        nonlocal checks
        checks += 1
        if not ok:
            fails.append("%s: %s" % (name, why))

    # ACCEPTING CASE FIRST, and the live repository is the fixture, so doing
    # the work this tool prompts can never break the tool.
    rc = run()
    ck("accept/the live tree agrees", rc == 0, "run() returned %d" % rc)

    live_ue, err = parse_ue((ROOT / UE).read_text(encoding="utf-8"))
    ck("accept/the UE table parses", err is None and live_ue, err or "empty")
    live_unity = parse_unity((ROOT / UNITY).read_text(encoding="utf-8"))
    ck("accept/the Unity switch parses", len(live_unity) == len(NAME_MAP),
       "got %d of %d" % (len(live_unity), len(NAME_MAP)))

    # REJECTING CASES, synthetic, so the fixture cannot be broken by real work.
    bad = dict(live_unity)
    first = sorted(bad)[0]
    bad[first] = (bad[first][0] + 0.01, bad[first][1], bad[first][2])
    f, c = compare(live_ue, bad)
    ck("reject/a drifted tint is caught", len(f) == 1 and "wrong" in f[0],
       "findings=%r" % f)
    ck("reject/the denominator counts what was compared", c == len(NAME_MAP),
       "compared=%d" % c)

    f, _ = compare({}, live_unity)
    ck("reject/a surface missing from the UE table is caught",
       len(f) == len(live_unity), "findings=%r" % f)
    f, _ = compare(live_unity, {})
    ck("reject/a surface missing from the Unity switch is caught",
       len(f) == len(live_unity), "findings=%r" % f)

    ue2, err2 = parse_ue("nothing that looks like the table")
    ck("reject/an unparseable UE table says nothing measured",
       ue2 is None and err2, "err=%r" % err2)

    # ---- THE WETNESS COPIES, QUEUE 186. ACCEPTING CASE FIRST, and the live
    # tree is the fixture for the same reason it is above.
    ue_text = (ROOT / UE).read_text(encoding="utf-8")
    unity_text = (ROOT / UNITY).read_text(encoding="utf-8")
    lm_text = (ROOT / UNITY_LIGHT).read_text(encoding="utf-8")
    live_g, gerr = parse_ue_ground(ue_text)
    ck("accept/the UE ground table parses", gerr is None and len(live_g) == 4,
       gerr or "got %r" % live_g)
    live_gu = parse_unity_ground(unity_text)
    ck("accept/the Unity ground smoothness parses", len(live_gu) == 4,
       "got %r" % live_gu)
    live_wc = parse_ue_wet_constants(ue_text)
    live_wu = parse_unity_wet_constants(lm_text)
    ck("accept/both wetness scalars parse on both sides",
       len(live_wc) == 2 and len(live_wu) == 2,
       "ue=%r unity=%r" % (live_wc, live_wu))
    ck("accept/the ceiling is 0.92 and the slope 0.45 on the Unity side",
       live_wu.get("ceiling") == 0.92 and live_wu.get("albedoSlope") == 0.45,
       "unity=%r" % live_wu)
    f, c = compare_numbers(live_g, live_gu, "drySmoothness")
    ck("accept/the four ground smoothness values agree",
       not f and c == 4, "findings=%r compared=%d" % (f, c))

    # REJECTING CASES, SYNTHETIC, so real work cannot break the fixture.
    drift = dict(live_gu)
    drift["kerb"] = drift["kerb"] + 0.01
    f, c = compare_numbers(live_g, drift, "drySmoothness")
    ck("reject/a drifted ground smoothness is caught",
       len(f) == 1 and "wrong" in f[0] and c == 4, "findings=%r" % f)
    f, _ = compare_numbers({}, live_gu, "drySmoothness")
    ck("reject/a surface missing from the UE ground table is caught",
       len(f) == 4, "findings=%r" % f)
    f, _ = compare_numbers(live_g, {}, "drySmoothness")
    ck("reject/a surface missing from the Unity switch is caught",
       len(f) == 4, "findings=%r" % f)
    f, _ = compare_numbers({"ceiling": 0.90, "albedoSlope": 0.45}, live_wu,
                           "wetConstant")
    ck("reject/a drifted 0.92 ceiling is caught",
       len(f) == 1 and "ceiling" in f[0], "findings=%r" % f)
    g2, gerr2 = parse_ue_ground("nothing that looks like the ground table")
    ck("reject/an unparseable UE ground table says nothing measured",
       g2 is None and gerr2, "err=%r" % gerr2)
    ck("reject/an unparseable LightModel gives fewer than two scalars",
       len(parse_unity_wet_constants("no arithmetic here")) == 0,
       "got %r" % parse_unity_wet_constants("no arithmetic here"))

    print("surface-tint-check selftest: %d ok, %d failed, over %d check(s) "
          "(accepting first: 8 of them)"
          % (checks - len(fails), len(fails), checks))
    for f in fails:
        print("  FAIL", f)
    return 1 if fails else 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    sys.exit(selftest() if a.selftest else run())
