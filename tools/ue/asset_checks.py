"""THE ASSET CHECKS BEFORE ANY REVIEWER (his order of 28 October 2026, D13: "Unreal's built-in asset
validation for triangle counts, texture sizes, names, LODs, collision and missing parts, run before any
fresh reviewer, so reviewers judge only the look").

    python tools/ue/asset_checks.py --selftest      # the eleven rules on plain data, without Unreal
    python tools/ue/asset_checks.py --check-spec    # production/specs/asset-budgets.json, without Unreal
    UnrealEditor-Cmd.exe <full path>/LedgerProbe.uproject -run=pythonscript
        -script=<full path>/tools/ue/asset_checks.py -EnablePlugins=PythonScriptPlugin,GeometryScripting
        -unattended -nopause -nosplash -stdout          (LEDGER_CHECK_PIECE=tom-jacket; no -nullrhi)
    or, from an import script in its own session:  asset_checks.run("tom-jacket")

WHY (production/research/asset-checks/CHECKS-2026-10-28.md). Over 14 to 28 October the game's ten gates
took a median of 9 rounds and 26 reviews a piece; reviewers caught stale imports, placeholders, a JPEG
normal map and see-through cloth that a script can decide, and the jacket's first build drew Unreal's grey
grid because its material had not compiled. Nothing read an imported piece before the reviewers.

WHAT IT DOES. The thresholds live in one home, production/specs/asset-budgets.json (kinds, the
folder-to-kind map, the pieces' parts, the waivers); a changed number is a spec edit with a DECISIONS line,
never a code edit. The eleven rules are plain functions over one record per asset (check_asset,
check_piece), so the selftest runs them on plain data. Inside the editor:
  - each asset of the piece's folders is read into a record (editor_record);
  - rule 1 is Epic's own: each asset's IsDataValid and every registered validator, through the
    EditorValidatorSubsystem (is_asset_valid; Epic's material check works only once a validation
    platform is listed in the project's DefaultEditor.ini);
  - the same rules are registered as a Python validator (unreal.EditorValidatorBase), so the editor's
    own Validate Assets and validate-on-save run them too; their messages carry "[ledger]" and are
    left out of rule 1;
  - one line is appended to ue-material.txt beside the project, and the piece's report written to
    production/asset-checks/<piece>.json. Read the line, never the exit code: the commandlet's exit code
    is no verdict (CHECKS, section 1).

ONE LINE: assetChecks=PASS|FAIL piece=<piece> assets=<n> errors=<n> warnings=<n> waived=<n> first=<rule>:<asset>:<value>/<limit>

UNTESTED IN UNREAL (28 October 2026: the build machine was building and no editor could run). The editor
side follows the 5.8 headers read for CHECKS-2026-10-28.md; the Python names (k2_validate_loaded_asset,
is_asset_valid's out lists, Geometry Script's skeletal triangle count) are confirmed at the first run in a
scratch folder (CHECKS, First use, step 2). The rules themselves are covered by --selftest.
"""
import copy
import hashlib
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SPEC = os.path.join(REPO, "production", "specs", "asset-budgets.json")
GARMENTS = os.path.join(REPO, "production", "specs", "garments.json")
REPORTS = os.path.join(REPO, "production", "asset-checks")
RULES = ("engine", "triangles", "lods", "nanite", "texture_size", "texture_role", "placeholder", "parts",
         "see_through", "names", "collision")
TAG = "[ledger] "
SEVERITIES = ("error", "warning", "note", "waived")


def load_spec(path=SPEC):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def folder_of(path):
    return path.rsplit("/", 1)[0] if "/" in path else ""


def kind_of(spec, path):
    """The longest folder in the spec's map that holds this path (a folder boundary, not a prefix of a name)."""
    best, best_len = None, -1
    for folder, kind in spec.get("folders", []):
        if (path == folder or path.startswith(folder + "/")) and len(folder) > best_len:
            best, best_len = kind, len(folder)
    return best


def finding(rule, asset, message, severity="error", value=None, limit=None):
    return {"rule": rule, "asset": asset, "message": message, "severity": severity, "value": value, "limit": limit}


def is_pow2(n):
    return isinstance(n, int) and n > 0 and n & (n - 1) == 0


def texture_role(spec, name):
    roles = spec.get("texture_roles", {})
    for role in ("normal", "packed"):
        if any(name.endswith(s) for s in roles.get(role, [])):
            return role
    return "colour"


def check_asset(spec, rec, in_piece=True):
    """Every rule that one asset can decide alone. rec is plain data (see the selftest's clean records)."""
    out = []
    name, cls, path = rec["name"], rec["class"], rec["path"]
    kind_name = rec.get("kind") or kind_of(spec, path)
    kind = spec.get("kinds", {}).get(kind_name) if kind_name else None

    # 1. Epic's validators and IsDataValid
    for e in rec.get("engine_errors", []):
        out.append(finding("engine", name, e))
    for w in rec.get("engine_warnings", []):
        out.append(finding("engine", name, w, "warning"))

    # 4. Nanite off on every static mesh of ours (exempt folders too: the game draws no Nanite)
    if cls == "StaticMesh" and path.startswith("/Game/Ledger/") and rec.get("nanite"):
        out.append(finding("nanite", name, "Nanite is on", value="on", limit="off"))

    if kind and kind.get("exempt"):
        return out

    if cls in ("StaticMesh", "SkeletalMesh"):
        tris = list(rec.get("triangles") or [])
        cap = kind.get("triangles") if kind else None
        # 2. full-detail triangles
        if cap is None:
            out.append(finding("triangles", name, "no budget kind for this mesh's folder %s (add it to the spec's folders)"
                               % folder_of(path), value=kind_name or "none", limit="a kind with a triangle cap"))
        else:
            t0 = tris[0] if tris else None
            if t0 is None:
                out.append(finding("triangles", name, "full-detail triangles not measured", "warning"))
            elif t0 > cap:
                out.append(finding("triangles", name, "%d triangles over the %s cap" % (t0, kind_name), value=t0, limit=cap))
            elif t0 > cap * spec.get("warn_fraction", 0.9):
                out.append(finding("triangles", name, "%d triangles, above %d%% of the %s cap" % (
                    t0, round(100 * spec.get("warn_fraction", 0.9)), kind_name), "warning", value=t0, limit=cap))
        # 3. levels of detail
        want = kind.get("lods") if kind else None
        if want:
            if len(tris) < want:
                out.append(finding("lods", name, "%d levels of detail, the %s kind wants %d" % (len(tris), kind_name, want),
                                   value=len(tris), limit=want))
            step = spec.get("lod_step_max", 0.6)
            for i in range(1, len(tris)):
                a, b = tris[i - 1], tris[i]
                if a and b and b > step * a:
                    out.append(finding("lods", name, "LOD%d keeps %d of LOD%d's %d (more than %d%%)" % (
                        i, b, i - 1, a, round(100 * step)), value=b, limit=int(step * a)))
        # 7 and 9. the material slots
        glass_words = [w.lower() for w in spec.get("glass_words", [])]
        defaults = set(spec.get("default_materials", []))
        for s in rec.get("materials", []):
            slot, mat = s.get("slot", "?"), s.get("material")
            if not mat:
                out.append(finding("placeholder", name, "slot %s has no material" % slot, value="none", limit="a material"))
                continue
            if mat in defaults or s.get("default"):
                out.append(finding("placeholder", name, "slot %s draws the engine's default material %s" % (slot, mat),
                                   value=mat, limit="a material of ours"))
                continue
            glass = any(w in slot.lower() for w in glass_words)
            listed = mat in spec.get("see_through_ok", []) or ("%s:%s" % (path, slot)) in spec.get("see_through_ok", [])
            if s.get("see_through") and not glass and not listed:
                out.append(finding("see_through", name, "slot %s is see-through (%s) but is not glass" % (slot, mat),
                                   value="see-through", limit="opaque"))
            if not glass and s.get("textures", 1) == 0 and mat not in spec.get("untextured_ok", []):
                out.append(finding("placeholder", name, "slot %s's material %s samples no texture" % (slot, mat),
                                   value=0, limit="at least one texture"))
        # 11. collision, static meshes only (garments and people take the body's capsule)
        if cls == "StaticMesh" and kind:
            need = kind.get("collision")
            c = rec.get("collision") or {}
            simple, convex = c.get("simple", 0), c.get("convex", 0)
            if c.get("complex_as_simple"):
                out.append(finding("collision", name, "uses complex collision as simple", value="complex", limit="simple"))
            if need == "simple":
                if simple + convex == 0:
                    out.append(finding("collision", name, "no simple collision; the %s kind needs it" % kind_name,
                                       value=0, limit="simple shapes"))
                if convex > kind.get("max_hulls", 10):
                    out.append(finding("collision", name, "%d convex hulls, the %s kind allows %d" % (
                        convex, kind_name, kind.get("max_hulls", 10)), value=convex, limit=kind.get("max_hulls", 10)))
            elif need == "none_or_one_box":
                if convex > 0 or simple > 1:
                    out.append(finding("collision", name, "%d shapes and %d hulls; the %s kind takes none or one box" % (
                        simple, convex, kind_name), value=simple + convex, limit=1))
            elif need == "none" and simple + convex > 0:
                out.append(finding("collision", name, "collision on a %s, which wants none" % kind_name, "warning",
                                   value=simple + convex, limit=0))

    if cls in ("Texture2D",):
        w, h = (rec.get("size") or [0, 0])[:2]
        # 5. texture size
        if not (is_pow2(w) and is_pow2(h)):
            out.append(finding("texture_size", name, "%dx%d is not a power of two each side" % (w, h),
                               value="%dx%d" % (w, h), limit="powers of two"))
        big, gmax = max(w, h), spec.get("texture_max_global", 4096)
        kmax = kind.get("texture_max") if kind else None
        if big > gmax:
            out.append(finding("texture_size", name, "%d px over the %d cap" % (big, gmax), value=big, limit=gmax))
        elif kmax and big > kmax:
            out.append(finding("texture_size", name, "%d px over the %s kind's %d" % (big, kind_name, kmax), value=big, limit=kmax))
        # 6. texture role
        role = texture_role(spec, name)
        comp, srgb, src = rec.get("compression"), rec.get("srgb"), (rec.get("source_compression") or "")
        if role == "normal":
            if comp != "TC_NORMALMAP":
                out.append(finding("texture_role", name, "a normal map compressed as %s" % comp, value=comp, limit="TC_NORMALMAP"))
            if "JPEG" in src.upper() or "JPG" in src.upper():
                out.append(finding("texture_role", name, "a normal map from a JPEG source", value=src, limit="not JPEG"))
        elif role == "packed":
            if comp != "TC_MASKS":
                out.append(finding("texture_role", name, "a packed map compressed as %s" % comp, value=comp, limit="TC_MASKS"))
            if srgb:
                out.append(finding("texture_role", name, "a packed map with sRGB on", value="sRGB", limit="linear"))
        elif srgb is False:
            out.append(finding("texture_role", name, "a colour map with sRGB off", value="linear", limit="sRGB"))
        # 7. a texture of one flat colour
        if rec.get("flat"):
            out.append(finding("placeholder", name, "the texture is one flat colour", value="flat", limit="an image"))

    # 10. names, in the gated piece's own folders
    if in_piece:
        names = spec.get("names", {})
        if not re.match(names.get("allowed", r"^[A-Za-z0-9_]+$"), name):
            out.append(finding("names", name, "the name holds characters other than letters, digits and underscores",
                               value=name, limit=names.get("allowed")))
        want = names.get("prefixes", {}).get(cls)
        if want and not any(name.startswith(p) for p in want):
            out.append(finding("names", name, "a %s's name starts %s" % (cls, " or ".join(want)), value=name, limit="/".join(want)))

    # 8. freshness: the import's MD5 against its source file now
    imp = rec.get("import")
    if imp:
        md5, cur = (imp.get("md5") or "").lower(), imp.get("current_md5")
        if cur is None:
            out.append(finding("parts", name, "source %s not on this machine; freshness not checked" % imp.get("file"), "note"))
        elif md5 and md5 != cur.lower():
            out.append(finding("parts", name, "imported from an older %s (MD5 %s, the file now %s)" % (
                imp.get("file"), md5[:8], cur.lower()[:8]), value=md5[:8], limit=cur.lower()[:8]))
        elif not md5 and imp.get("time") is not None and imp.get("current_time") is not None \
                and imp["time"] < imp["current_time"]:
            out.append(finding("parts", name, "imported before %s last changed" % imp.get("file"),
                               value=imp["time"], limit=imp["current_time"]))
    return out


def waived(spec, f):
    for w in spec.get("waivers", []):
        if w.get("rule") == f["rule"] and w.get("asset") in (f["asset"],):
            return True
    return False


def check_piece(spec, piece, records):
    """Every rule over a piece's assets: the parts it must have, then each asset; waivers last."""
    out = []
    have = {r["name"] for r in records}
    for p in spec.get("pieces", {}).get(piece, {}).get("parts", []):
        if p not in have:
            out.append(finding("parts", p, "part %s is missing from the piece" % p, value="missing", limit="present"))
    for r in records:
        out.extend(check_asset(spec, r, in_piece=True))
    for f in out:
        if f["severity"] == "error" and waived(spec, f):
            f["severity"] = "waived"
    return out


def status_line(piece, records, findings):
    errors = [f for f in findings if f["severity"] == "error"]
    count = lambda s: sum(1 for f in findings if f["severity"] == s)
    first = "none"
    if errors:
        f = errors[0]
        first = "%s:%s:%s/%s" % (f["rule"], f["asset"], f["value"], f["limit"])
    return "assetChecks=%s piece=%s assets=%d errors=%d warnings=%d waived=%d first=%s" % (
        "FAIL" if errors else "PASS", piece, len(records), len(errors), count("warning"), count("waived"), first)


def report(piece, records, findings, line, when=None):
    return {"piece": piece, "line": line, "when": when, "assets": [r["path"] for r in records],
            "imports": {r["name"]: (r.get("import") or {}).get("md5") for r in records if r.get("import")},
            "findings": findings}


def check_spec(spec, garments=None):
    """The spec's own shape: every kind sourced, every folder's kind known, pieces resolvable, waivers whole."""
    bad = []
    kinds = spec.get("kinds", {})
    for k, v in kinds.items():
        if not v.get("source"):
            bad.append("kind %s has no source" % k)
        if v.get("exempt"):
            continue
        for field in ("triangles", "lods", "texture_max"):
            x = v.get(field)
            if x is not None and (not isinstance(x, int) or x <= 0):
                bad.append("kind %s: %s %r is not a positive whole number" % (k, field, x))
        hulls = v.get("max_hulls")
        if hulls is not None and (not isinstance(hulls, int) or hulls < 0):
            bad.append("kind %s: max_hulls %r is not a whole number from 0" % (k, hulls))
        if v.get("texture_max") and not is_pow2(v["texture_max"]):
            bad.append("kind %s: texture_max %r is not a power of two" % (k, v["texture_max"]))
        if v.get("texture_max") and v["texture_max"] > spec.get("texture_max_global", 4096):
            bad.append("kind %s: texture_max over the global cap" % k)
        if v.get("collision") not in (None, "none", "none_or_one_box", "simple"):
            bad.append("kind %s: collision %r unknown" % (k, v.get("collision")))
    for folder, kind in spec.get("folders", []):
        if kind not in kinds:
            bad.append("folder %s maps to unknown kind %s" % (folder, kind))
        if not folder.startswith("/Game/"):
            bad.append("folder %s is not under /Game" % folder)
    for name, p in spec.get("pieces", {}).items():
        if not p.get("folders"):
            bad.append("piece %s has no folders" % name)
        for f in p.get("folders", []):
            k = kind_of(spec, f)
            if k is None or kinds.get(k, {}).get("exempt"):
                bad.append("piece %s: folder %s has no checking kind (%s)" % (name, f, k))
            m = re.match(r"^/Game/Ledger/MetaHumans/Garments/([A-Za-z0-9]+)$", f)
            if m and garments is not None:
                if m.group(1) not in garments:
                    bad.append("piece %s: garment %s is not in garments.json" % (name, m.group(1)))
                elif "SKM_" + m.group(1) not in p.get("parts", []):
                    bad.append("piece %s: parts lack SKM_%s" % (name, m.group(1)))
    for i, w in enumerate(spec.get("waivers", [])):
        for field in ("asset", "rule", "decision", "finding"):
            if not w.get(field):
                bad.append("waiver %d has no %s" % (i, field))
        if w.get("rule") and w["rule"] not in RULES:
            bad.append("waiver %d: rule %r unknown" % (i, w["rule"]))
    for field in ("warn_fraction", "lod_step_max"):
        x = spec.get(field)
        if not isinstance(x, (int, float)) or not 0 < x < 1:
            bad.append("%s %r is not between 0 and 1" % (field, x))
    if set(spec.get("rules", {})) != set(RULES):
        bad.append("the spec's rules differ from the code's: %s" % sorted(set(spec.get("rules", {})) ^ set(RULES)))
    return bad


def garment_names(path=GARMENTS):
    try:
        with open(path, encoding="utf-8") as fh:
            d = json.load(fh)
    except OSError:
        return None
    g = d["garments"] if isinstance(d, dict) else d
    return {x["name"] for x in g}


def run_check_spec():
    spec = load_spec()
    bad = check_spec(spec, garment_names())
    if bad:
        for b in bad:
            print("assetBudgets FAULT " + b)
        print("assetBudgets=BAD faults=%d" % len(bad))
        return 1
    print("assetBudgets=OK kinds=%d folders=%d pieces=%d waivers=%d" % (
        len(spec.get("kinds", {})), len(spec.get("folders", [])), len(spec.get("pieces", {})), len(spec.get("waivers", []))))
    return 0


# ---------------------------------------------------------------- the selftest, without Unreal

JF = "/Game/Ledger/MetaHumans/Garments/TomZipJacket"
PF = "/Game/Ledger/SelftestProps"


def selftest_spec():
    spec = copy.deepcopy(load_spec())
    spec["folders"].append([PF, "prop_medium"])
    spec["pieces"]["selftest"] = {"folders": [JF, PF], "source": "selftest",
                                  "parts": list(spec["pieces"]["tom-jacket"]["parts"])}
    spec["waivers"] = []
    return spec


def ladder(cap, levels):
    t = int(cap * 0.85)
    out = [t]
    for _ in range(levels - 1):
        t = int(t * 0.5)
        out.append(t)
    return out


def clean_records(spec):
    jk, pk = spec["kinds"]["garment_jacket"], spec["kinds"]["prop_medium"]
    fresh = lambda f: {"file": f, "md5": "a1b2c3d4" * 4, "current_md5": "A1B2C3D4" * 4}

    def tex(suffix, comp, srgb):
        return {"path": "%s/T_TomZipJacket_%s" % (JF, suffix), "name": "T_TomZipJacket_" + suffix, "class": "Texture2D",
                "size": [jk["texture_max"], jk["texture_max"]], "compression": comp, "srgb": srgb,
                "source_compression": "PNG", "flat": False, "import": fresh("F:/x/%s.png" % suffix), "engine_errors": []}
    return [
        {"path": JF + "/SKM_TomZipJacket", "name": "SKM_TomZipJacket", "class": "SkeletalMesh",
         "triangles": ladder(jk["triangles"], jk["lods"]), "engine_errors": [],
         "materials": [{"slot": "cloth", "material": JF + "/MI_TomZipJacket", "see_through": False, "textures": 3}],
         "import": fresh("F:/x/zip_jacket_skinned.fbx")},
        {"path": JF + "/MI_TomZipJacket", "name": "MI_TomZipJacket", "class": "MaterialInstanceConstant", "engine_errors": []},
        tex("ColourAO", "TC_DEFAULT", True),
        tex("Normal", "TC_NORMALMAP", False),
        tex("Packed", "TC_MASKS", False),
        {"path": PF + "/SM_SelftestBin", "name": "SM_SelftestBin", "class": "StaticMesh", "nanite": False,
         "triangles": ladder(pk["triangles"], pk["lods"]), "engine_errors": [],
         "collision": {"simple": 1, "convex": 0, "complex_as_simple": False},
         "materials": [{"slot": "bin", "material": PF + "/MI_SelftestBin", "see_through": False, "textures": 2}]},
    ]


def by_name(records, name):
    return [r for r in records if r["name"] == name][0]


def selftest():
    ok = bad = 0

    def check(what, cond, detail=""):
        nonlocal ok, bad
        if cond:
            ok += 1
        else:
            bad += 1
            print("asset_checks selftest FAIL %s %s" % (what, detail))

    spec = selftest_spec()

    def errors_of(records, sp=None):
        fs = check_piece(sp or spec, "selftest", records)
        return {f["rule"] for f in fs if f["severity"] == "error"}, fs

    clean = clean_records(spec)
    rules, fs = errors_of(clean)
    check("the clean copy passes every rule", rules == set(), str([f["message"] for f in fs]))
    check("the clean copy raises no warning", not [f for f in fs if f["severity"] == "warning"], str(fs))
    check("the clean line reads PASS", status_line("selftest", clean, fs).startswith("assetChecks=PASS piece=selftest assets=6 errors=0"))

    def plant(what, rule, change):
        recs = copy.deepcopy(clean)
        change(recs)
        got, fs = errors_of(recs)
        check("plant: %s fails %s only" % (what, rule), got == {rule}, "failed %s: %s" % (sorted(got), [f["message"] for f in fs if f["severity"] == "error"]))
        return fs

    # the seven planted faults of CHECKS-2026-10-28.md, First use, step 1
    plant("a grid material", "placeholder",
          lambda r: by_name(r, "SKM_TomZipJacket")["materials"][0].update(material="/Engine/EngineMaterials/WorldGridMaterial"))
    plant("a 4096 texture on a garment", "texture_size", lambda r: by_name(r, "T_TomZipJacket_ColourAO").update(size=[4096, 4096]))
    fs = plant("a one-level garment", "lods", lambda r: by_name(r, "SKM_TomZipJacket").update(
        triangles=by_name(r, "SKM_TomZipJacket")["triangles"][:1]))
    plant("a JPEG normal map", "texture_role", lambda r: by_name(r, "T_TomZipJacket_Normal").update(source_compression="JPEG"))
    plant("a misnamed asset", "names", lambda r: by_name(r, "SM_SelftestBin").update(name="SelftestBin", path=PF + "/SelftestBin"))
    plant("an import older than its export", "parts", lambda r: by_name(r, "T_TomZipJacket_Packed")["import"].update(current_md5="ffff" * 8))
    plant("a medium prop without collision", "collision", lambda r: by_name(r, "SM_SelftestBin").update(
        collision={"simple": 0, "convex": 0, "complex_as_simple": False}))

    # the line names the first fault
    one_level = copy.deepcopy(clean)
    by_name(one_level, "SKM_TomZipJacket")["triangles"] = by_name(one_level, "SKM_TomZipJacket")["triangles"][:1]
    fs1 = check_piece(spec, "selftest", one_level)
    line = status_line("selftest", one_level, fs1)
    check("the FAIL line names rule, asset and value/limit", "assetChecks=FAIL" in line and "first=lods:SKM_TomZipJacket:1/4" in line, line)

    # each other rule, once
    plant("Nanite left on", "nanite", lambda r: by_name(r, "SM_SelftestBin").update(nanite=True))
    plant("see-through cloth", "see_through", lambda r: by_name(r, "SKM_TomZipJacket")["materials"][0].update(see_through=True))
    plant("a flat-colour texture", "placeholder", lambda r: by_name(r, "T_TomZipJacket_ColourAO").update(flat=True))
    plant("an untextured material", "placeholder", lambda r: by_name(r, "SM_SelftestBin")["materials"][0].update(textures=0))
    plant("an empty slot", "placeholder", lambda r: by_name(r, "SM_SelftestBin")["materials"][0].update(material=None))
    plant("a missing part", "parts", lambda r: r.remove(by_name(r, "T_TomZipJacket_Normal")))
    plant("an engine error", "engine", lambda r: by_name(r, "MI_TomZipJacket").update(engine_errors=["failed to compile"]))
    plant("too many triangles", "triangles", lambda r: by_name(r, "SKM_TomZipJacket")["triangles"].__setitem__(0, 30000))
    plant("a level that keeps too much", "lods", lambda r: by_name(r, "SKM_TomZipJacket")["triangles"].__setitem__(
        1, int(by_name(r, "SKM_TomZipJacket")["triangles"][0] * 0.9)))
    plant("a non-power-of-two texture", "texture_size", lambda r: by_name(r, "T_TomZipJacket_Packed").update(size=[2000, 2048]))
    plant("a packed map in sRGB", "texture_role", lambda r: by_name(r, "T_TomZipJacket_Packed").update(srgb=True))
    plant("a normal map compressed as colour", "texture_role", lambda r: by_name(r, "T_TomZipJacket_Normal").update(compression="TC_DEFAULT"))
    plant("a prefix in the wrong case", "names", lambda r: by_name(r, "SM_SelftestBin").update(name="sm_SelftestBin"))
    plant("a space in a name", "names", lambda r: by_name(r, "SM_SelftestBin").update(name="SM_Selftest Bin"))
    plant("complex collision as simple", "collision", lambda r: by_name(r, "SM_SelftestBin")["collision"].update(complex_as_simple=True))
    plant("eleven hulls on a medium prop", "collision", lambda r: by_name(r, "SM_SelftestBin")["collision"].update(convex=11))
    plant("a mesh in a folder with no kind", "triangles", lambda r: by_name(r, "SM_SelftestBin").update(path="/Game/Ledger/Nowhere/SM_SelftestBin"))

    # what must not fail
    recs = copy.deepcopy(clean)
    by_name(recs, "SKM_TomZipJacket")["materials"].append({"slot": "glass_lens", "material": JF + "/MI_Glass", "see_through": True, "textures": 0})
    check("see-through and untextured glass passes", errors_of(recs)[0] == set())
    recs = copy.deepcopy(clean)
    by_name(recs, "SKM_TomZipJacket")["triangles"][0] = int(spec["kinds"]["garment_jacket"]["triangles"] * 0.95)
    by_name(recs, "SKM_TomZipJacket")["triangles"][1] = int(by_name(recs, "SKM_TomZipJacket")["triangles"][0] * 0.5)
    got, fs = errors_of(recs)
    check("95% of the cap warns and does not fail", got == set() and any(f["rule"] == "triangles" and f["severity"] == "warning" for f in fs), str(fs))
    recs = copy.deepcopy(clean)
    recs.append({"path": "/Game/Ledger/MetaHumans/MH_TomL1/Body/body mesh", "name": "body mesh", "class": "StaticMesh",
                 "triangles": [99999], "nanite": False, "materials": []})
    check("an exempt folder's asset is not judged by our budgets", errors_of(recs)[0] == set())
    recs[-1]["nanite"] = True
    check("but Nanite is off there too", errors_of(recs)[0] == {"nanite"})
    recs = copy.deepcopy(clean)
    by_name(recs, "T_TomZipJacket_Packed")["import"]["current_md5"] = None
    got, fs = errors_of(recs)
    check("a source not on this machine is a note, not a fault", got == set() and any(f["severity"] == "note" for f in fs))

    # waivers
    wspec = copy.deepcopy(spec)
    wspec["waivers"] = [{"asset": "SKM_TomZipJacket", "rule": "lods", "decision": "DECISIONS.md test", "finding": "FINDINGS.md test"}]
    fsw = check_piece(wspec, "selftest", one_level)
    check("a waived fault fails nothing alone and is listed",
          status_line("selftest", one_level, fsw).startswith("assetChecks=PASS") and "waived=1" in status_line("selftest", one_level, fsw))

    # the folder map
    check("a garment's own folder wins over the MetaHumans' exemption", kind_of(spec, JF + "/SKM_TomZipJacket") == "garment_jacket")
    check("the garments' shared folder", kind_of(spec, "/Game/Ledger/MetaHumans/Garments/M_LedgerGarmentPacked") == "shared")
    check("a body under MetaHumans is exempt", kind_of(spec, "/Game/Ledger/MetaHumans/MH_TomL1/Body/SKM_Body") == "exempt")
    check("a folder boundary, not a name prefix", kind_of(spec, "/Game/Ledger/MetaHumans/GarmentsOld/SKM_X") == "exempt")
    check("an unmapped folder has no kind", kind_of(spec, "/Game/Ledger/Street/SM_Wall") is None)

    # the spec
    real = load_spec()
    problems = check_spec(real, garment_names())
    check("the committed spec passes its own check", problems == [], str(problems))
    broken = copy.deepcopy(real)
    broken["kinds"]["prop_small"].pop("source")
    broken["waivers"] = [{"asset": "SKM_X", "rule": "lods"}]
    broken["folders"].append(["/Game/Ledger/X", "no_such_kind"])
    p2 = check_spec(broken, garment_names())
    check("the spec check finds a kind without a source", any("prop_small has no source" in p for p in p2), str(p2))
    check("the spec check finds a waiver without its records", any("waiver 0 has no decision" in p for p in p2), str(p2))
    check("the spec check finds an unknown kind", any("no_such_kind" in p for p in p2), str(p2))

    print("asset_checks selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


# ---------------------------------------------------------------- inside the editor (untested until the first run)

def _md5(path):
    h = hashlib.md5()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def import_info(ad):
    """The import's source, time and MD5 from the hidden registry tag every mesh and texture keeps
    (StaticMesh.cpp 6230, SkeletalMesh.cpp 4631, Texture.cpp 1482; the JSON of AssetImportData.cpp 49)."""
    try:
        raw = ad.get_tag_value("AssetImportData")
    except Exception:
        raw = None
    if not raw:
        return None
    try:
        files = json.loads(raw)
    except ValueError:
        return None
    if not files:
        return None
    f = files[0]
    path = f.get("RelativeFilename", "")
    info = {"file": path, "md5": f.get("FileMD5") or None, "time": int(f["Timestamp"]) if f.get("Timestamp", "").lstrip("-").isdigit() else None}
    if os.path.isabs(path) and os.path.isfile(path):
        info["current_md5"] = _md5(path)
        info["current_time"] = int(os.path.getmtime(path))
    else:
        info["current_md5"] = None
    return info


def _out(result, n):
    """UE Python returns out parameters in a tuple after any return value; take the last n."""
    if isinstance(result, tuple):
        return result[-n:] if n > 1 else result[-1]
    return result


def material_facts(unreal, mat):
    """See-through and how many textures a slot's material samples (from its base material)."""
    if mat is None:
        return {"material": None}
    path = mat.get_path_name().split(".")[0]
    facts = {"material": path, "see_through": False, "textures": 1}
    try:
        base = mat.get_base_material()
        bm = base.get_editor_property("blend_mode")
        facts["see_through"] = bm in (unreal.BlendMode.BLEND_TRANSLUCENT, unreal.BlendMode.BLEND_ADDITIVE,
                                      unreal.BlendMode.BLEND_MODULATE)
        try:
            if base.get_editor_property("shading_model") == unreal.MaterialShadingModel.MSM_THIN_TRANSLUCENT:
                facts["see_through"] = True
        except Exception:
            pass
        facts["textures"] = len(unreal.MaterialEditingLibrary.get_used_textures(base))
    except Exception as e:
        facts["unread"] = str(e)
    return facts


def skeletal_triangles(unreal, mesh, lods):
    """Triangles per level through Geometry Script (the plugin on the command line); None where it is not there."""
    out = []
    for i in range(lods):
        try:
            dm = unreal.DynamicMesh()
            opts = unreal.GeometryScriptCopyMeshFromAssetOptions()
            lod = unreal.GeometryScriptMeshReadLOD()
            lod.set_editor_property("lod_index", i)
            res = unreal.GeometryScript_AssetUtils.copy_mesh_from_skeletal_mesh(mesh, dm, opts, lod)
            got = res[0] if isinstance(res, tuple) else res
            out.append(int(unreal.GeometryScript_MeshQueries.get_num_triangle_ids(got or dm)))
        except Exception:
            out.append(None)
    return out


def editor_record(unreal, ad, subsystem=None):
    name = str(ad.asset_name)
    path = str(ad.package_name)
    try:
        cls = str(ad.asset_class_path.asset_name)
    except Exception:
        cls = str(ad.asset_class)
    rec = {"path": path, "name": name, "class": cls, "engine_errors": [], "engine_warnings": []}
    asset = unreal.EditorAssetLibrary.load_asset(path)
    if asset is None:
        rec["engine_errors"].append("could not be loaded")
        return rec
    if subsystem is not None:
        try:
            res = subsystem.is_asset_valid(ad, [], [], unreal.DataValidationUsecase.SCRIPT)
            errs, warns = _out(res, 2)
            rec["engine_errors"] += [str(e) for e in errs if not str(e).startswith(TAG)]
            rec["engine_warnings"] += [str(w) for w in warns if not str(w).startswith(TAG)]
        except Exception as e:
            rec["engine_warnings"].append("Epic's checks not read: %s" % e)
    imp = import_info(ad)
    if imp:
        rec["import"] = imp
    if isinstance(asset, unreal.StaticMesh):
        sme = unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem)
        rec["triangles"] = [asset.get_num_triangles(i) for i in range(asset.get_num_lods())]
        rec["nanite"] = bool(asset.get_editor_property("nanite_settings").enabled)
        rec["collision"] = {"simple": sme.get_simple_collision_count(asset), "convex": sme.get_convex_collision_count(asset),
                            "complex_as_simple": sme.get_collision_complexity(asset) == unreal.CollisionTraceFlag.CTF_USE_COMPLEX_AS_SIMPLE}
        rec["materials"] = [dict(slot=str(m.material_slot_name), **material_facts(unreal, m.material_interface))
                            for m in asset.get_editor_property("static_materials")]
    elif isinstance(asset, unreal.SkeletalMesh):
        ske = unreal.get_editor_subsystem(unreal.SkeletalMeshEditorSubsystem)
        rec["triangles"] = skeletal_triangles(unreal, asset, ske.get_lod_count(asset))
        rec["materials"] = [dict(slot=str(m.material_slot_name), **material_facts(unreal, m.material_interface))
                            for m in asset.get_editor_property("materials")]
    elif isinstance(asset, unreal.Texture2D):
        rec["size"] = [asset.blueprint_get_size_x(), asset.blueprint_get_size_y()]
        rec["compression"] = str(asset.get_editor_property("compression_settings")).split(".")[-1].split(":")[0].strip("<> ")
        rec["srgb"] = bool(asset.get_editor_property("srgb"))
        try:
            rec["source_compression"] = str(ad.get_tag_value("SourceCompression") or "")
        except Exception:
            rec["source_compression"] = ""
        try:
            mn, mx = _out(asset.compute_texture_source_channel_min_max(), 2)
            rec["flat"] = all(abs(getattr(mx, c) - getattr(mn, c)) < 1.0 / 255 for c in ("r", "g", "b", "a"))
        except Exception:
            rec["flat"] = False
    return rec


_VALIDATOR = None


def register_validator(unreal, spec):
    """The same rules as a Python validator, so the editor's Validate Assets and validate-on-save run them
    (Python validators register themselves: EditorValidatorBase.h line 24)."""
    global _VALIDATOR
    if _VALIDATOR is not None:
        return _VALIDATOR

    @unreal.uclass()
    class LedgerAssetValidator(unreal.EditorValidatorBase):
        @unreal.ufunction(override=True)
        def k2_can_validate_asset(self, asset):
            return isinstance(asset, (unreal.StaticMesh, unreal.SkeletalMesh, unreal.Texture2D)) and \
                asset.get_path_name().startswith("/Game/Ledger/")

        @unreal.ufunction(override=True)
        def k2_validate_loaded_asset(self, asset):
            ar = unreal.AssetRegistryHelpers.get_asset_registry()
            ad = ar.get_asset_by_object_path(asset.get_path_name())
            fs = check_asset(spec, editor_record(unreal, ad), in_piece=False)
            errs = [f for f in fs if f["severity"] == "error" and not waived(spec, f)]
            for f in fs:
                if f["severity"] == "warning":
                    self.asset_warning(asset, unreal.Text(TAG + "%s: %s" % (f["rule"], f["message"])))
            for f in errs:
                self.asset_fails(asset, unreal.Text(TAG + "%s: %s" % (f["rule"], f["message"])))
            if errs:
                return unreal.DataValidationResult.INVALID
            self.asset_passes(asset)
            return unreal.DataValidationResult.VALID

    _VALIDATOR = LedgerAssetValidator()
    unreal.get_editor_subsystem(unreal.EditorValidatorSubsystem).add_validator(_VALIDATOR)
    return _VALIDATOR


def run(piece, folders=None):
    """Inside the editor: the piece's folders checked, one line appended, the report written. Returns the line."""
    import unreal
    import time
    spec = load_spec()
    folders = folders or spec.get("pieces", {}).get(piece, {}).get("folders", [])
    ar = unreal.AssetRegistryHelpers.get_asset_registry()
    datas = []
    for f in folders:
        datas += list(ar.get_assets_by_path(f, recursive=True))
    try:
        register_validator(unreal, spec)
    except Exception as e:
        unreal.log_warning("asset_checks: the Python validator was not registered: %s" % e)
    sub = unreal.get_editor_subsystem(unreal.EditorValidatorSubsystem)
    records = [editor_record(unreal, ad, sub) for ad in datas]
    findings = check_piece(spec, piece, records)
    line = status_line(piece, records, findings)
    when = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(os.path.join(unreal.Paths.project_dir(), "ue-material.txt"), "a", encoding="utf-8") as fh:
        fh.write(line + "\n")
    os.makedirs(REPORTS, exist_ok=True)
    with open(os.path.join(REPORTS, piece + ".json"), "w", encoding="utf-8") as fh:
        json.dump(report(piece, records, findings, line, when), fh, indent=1)
    unreal.log("asset_checks: " + line)
    return line


def main():
    piece = os.environ.get("LEDGER_CHECK_PIECE")
    if not piece:
        print("asset_checks: set LEDGER_CHECK_PIECE (a piece in production/specs/asset-budgets.json)")
        return 2
    folders = [f for f in os.environ.get("LEDGER_CHECK_FOLDERS", "").split(",") if f] or None
    run(piece, folders)
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    if "--check-spec" in sys.argv:
        sys.exit(run_check_spec())
    try:
        import unreal  # noqa: F401
    except ImportError:
        print("asset_checks: outside Unreal only --selftest and --check-spec run")
        sys.exit(2)
    main()
