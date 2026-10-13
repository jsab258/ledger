"""sd_check: the checks every street-dressing target shares, and the negative controls that prove they can fail.

A family's self_check.py calls main(...) with its own extra rows and extra controls. Everything is derived from the
target's own parts (target.json), the photographs' pixels (with --live) and the target's own text. Nothing here compares
a number with itself: the geometry is rebuilt from the parts, the photograph's edges are predicted from the drawing, and
the numbers that sources print are measured back off the parts.
"""
import copy
import json
import os
import re
import sys

import numpy as np

import sd_lib as L

ALLOWED_LICENCES = ("creativecommons.org/licenses/by-sa/2.0", "CC BY-SA 2.0", "CC0", "CC BY 4.0", "CC BY-SA 4.0", "CC BY-SA 3.0",
                    "public domain", "CC BY 2.0", "CC BY 3.0")
CONTENT_WORDS = ["beer", "lager", "ale", "wine", "whisky", "whiskey", "vodka", "cider", "brewery", "pub", "tavern", "betting",
                 "bookmaker", "bookies", "gambling", "casino", "lottery", "bingo", "racing", "child", "children", "kid", "kids",
                 "toy", "toys", "baby", "boy", "girl", "schoolchild"]
ABSTRACT_OK_IN_RULE_LINES = ["betting", "gambling", "child", "children", "kid", "kids"]
_geo_cache = {}


# ------------------------------------------------------------------------------------------------ number measuring
def measure(ps, spec):
    """Measure one named quantity off the built parts. spec: {kind, ...}"""
    k = spec["kind"]
    ax = "xyz".index(spec.get("axis", "z"))
    if k == "bbox":
        only = spec.get("parts")
        if spec.get("exclude"):
            only = [n for n in (only or ps.names) if n not in spec["exclude"]]
        lo, hi = ps.bbox(only=only)
        return float(hi[ax] - lo[ax])
    if k == "edge":
        lo, hi = ps.part_bbox(spec["part"])
        return float((hi if spec.get("side", "hi") == "hi" else lo)[ax])
    if k == "extent":
        lo, hi = ps.part_bbox(spec["part"])
        return float(hi[ax] - lo[ax])
    if k == "gap":
        la, ha = ps.part_bbox(spec["a"])
        lb, hb = ps.part_bbox(spec["b"])
        ea = (ha if spec.get("side_a", "hi") == "hi" else la)[ax]
        eb = (hb if spec.get("side_b", "lo") == "hi" else lb)[ax]
        return float(eb - ea)
    if k == "centre":
        lo, hi = ps.part_bbox(spec["part"])
        return float((lo[ax] + hi[ax]) / 2)
    if k == "span":  # from the low edge of part a to the high edge of part b
        la, ha = ps.part_bbox(spec["a"])
        lb, hb = ps.part_bbox(spec["b"])
        return float(hb[ax] - la[ax])
    if k == "centre_dx":  # centre of part b minus centre of part a
        la, ha = ps.part_bbox(spec["a"])
        lb, hb = ps.part_bbox(spec["b"])
        return float((lb[ax] + hb[ax]) / 2 - (la[ax] + ha[ax]) / 2)
    if k == "count":
        pre = spec["prefix"]
        return float(sum(1 for n in ps.names if n.startswith(pre)))
    if k == "volume_ratio":
        return float(ps.volume(spec["a"]) / ps.volume(spec["b"]))
    raise ValueError(k)


# ------------------------------------------------------------------------------------------------ geometry rows
def geometry(ps, V, vspec, rows, contacts=None):
    """The rows for one variant. vspec has: overall, joins, embeds, faces, noground (parts allowed off the ground)."""
    g = "geometry/%s" % V
    parts = ps.parts
    lo, hi = ps.bbox(only=[n for n in ps.names if n not in vspec.get("overall_exclude", [])])
    dims = hi - lo
    ov = vspec.get("overall")
    if ov:
        for k, a in (("w", 0), ("d", 1), ("h", 2)):
            if k in ov:
                rows.near(g, "%s/overall %s" % (g, k), dims[a], ov[k], vspec.get("overall_tol", 1.0))
    # ground
    key = L.jhash([parts])
    if key in _geo_cache:
        ct = _geo_cache[key]
    else:
        ct = L.contact_table(ps, tol=vspec.get("contact_tol", 2.0))
        _geo_cache[key] = ct
    ground = L.grounded(ps)
    seen, adj = L.components(ps, ct, ground)
    floating = [n for n in ps.names if n not in seen and n not in vspec.get("noground", [])]
    rows.add(g, "%s/no floating part" % g, not floating, "floating: %s" % floating[:8] if floating else "all %d parts reach the ground through their joints" % len(parts))
    alone = [n for n in ps.names if not adj[n] and n not in ground]
    lone_ground = [n for n in ps.names if not adj[n] and n in ground and len(ps.names) > 1]
    rows.add(g, "%s/every part meets a neighbour" % g, not alone and not lone_ground, "no neighbour: %s" % (alone + lone_ground)[:8])
    bad = []
    for a, b in vspec.get("joins", []):
        pair = (a, b) if (a, b) in ct else (b, a)
        if pair not in ct:
            bad.append((a, b))
    rows.add(g, "%s/declared joins meet" % g, not bad, "%d joins; missing: %s" % (len(vspec.get("joins", [])), bad[:6]))
    emb = {tuple(sorted(e[:2])): e[2] for e in vspec.get("embeds", [])}
    over = []
    for (a, b), (kind, depth) in ct.items():
        allow = emb.get(tuple(sorted((a, b))), vspec.get("overlap_allow", 5.0))
        if depth > allow:
            over.append((a, b, round(depth, 1), allow))
    rows.add(g, "%s/no part sinks into another" % g, not over, "interpenetration deeper than allowed: %s" % over[:6] if over else "deepest overlap %.1f mm" % max([d for k, d in ct.values()] + [0]))
    # thin parts
    thin = []
    for p, pcs in zip(parts, ps.pieces):
        if p.get("film"):
            continue
        sz = np.max([pc.hi - pc.lo for pc in pcs], axis=0)
        # thinnest through-dimension of the part's bbox
        lo_p, hi_p = ps.part_bbox(p["id"])
        t = float(np.min(hi_p - lo_p))
        if t < vspec.get("min_thickness", 1.5):
            thin.append((p["id"], round(t, 2)))
    rows.add(g, "%s/no sliver parts" % g, not thin, "thinner than %.1f mm: %s" % (vspec.get("min_thickness", 1.5), thin[:6]))
    # closed faces
    for fc in vspec.get("faces", []):
        fk = L.jhash([parts, fc])
        if fk in _geo_cache:
            nr, leaks = _geo_cache[fk]
        else:
            nr, leaks = L.face_rays(ps, fc)
            _geo_cache[fk] = (nr, leaks)
        rows.add(g, "%s/face %s closed" % (g, fc["id"]), not leaks,
                 "%d rays (square on and leaning to 45 degrees), %d got through%s" % (nr, len(leaks), (": first at %s" % [leaks[0]]) if leaks else ""))
    # numbers
    return ct


def numbers_rows(T, rows):
    for n in T.get("numbers", []):
        V = n.get("variant", T.get("sample"))
        parts = L.variant_parts(T, V)
        ps = _ps_cache(parts)
        try:
            got = measure(ps, n["measure"])
        except Exception as e:
            rows.add("numbers", "numbers/%s" % n["id"], False, "could not measure: %s" % e)
            continue
        rows.near("numbers", "numbers/%s" % n["id"], got, n["value"], n.get("tol", 1.0))


_ps_store = {}


def _ps_cache(parts):
    k = L.jhash(parts)
    if k not in _ps_store:
        _ps_store[k] = L.PartSet(parts)
    return _ps_store[k]


# ------------------------------------------------------------------------------------------------ photographs
def predicted_px(ps, ph, f):
    """Where the drawing puts a feature in the photograph, with the scale fitted on ONE dimension (the height) only."""
    fit = ph["fit"]
    lo_ref, hi_ref = ps.bbox(only=fit.get("parts"))
    H = hi_ref[2] - lo_ref[2]
    s = (fit["y_bottom_px"] - fit["y_top_px"]) / H
    ax, sign = L.view_axes(fit.get("view", "front"))
    cx = (lo_ref[ax] + hi_ref[ax]) / 2.0
    ref = f["ref"]
    lo, hi = ps.part_bbox(ref["part"]) if ref.get("part") else ps.bbox(only=ref.get("parts"))
    side = ref.get("side", "hi")
    if f["axis"] == "y":
        z = (hi if side == "hi" else lo)[2] + ref.get("add", 0.0)
        return fit["y_bottom_px"] - (z - lo_ref[2]) * s
    x = (hi if side == "hi" else lo)[ax] + ref.get("add", 0.0)
    return fit["x_centre_px"] + sign * (x - cx) * s


def photo_rows(T, rows, live=False, photos_dir=None):
    for ph in T.get("photos", []):
        if not ph.get("fit"):
            continue
        V = ph.get("variant", T.get("sample"))
        ps = _ps_cache(L.variant_parts(T, V))
        pid = ph["id"]
        s = None
        gray = None
        if live and photos_dir:
            p = os.path.join(photos_dir, ph["file"])
            if os.path.exists(p):
                gray = L.load_gray(p)
            else:
                rows.add("live", "live/%s/photograph present" % pid, False, "not found: %s" % p)
        for f in ph["features"]:
            if f.get("anchor"):
                continue
            try:
                pred = predicted_px(ps, ph, f)
            except KeyError as e:
                rows.add("photo", "photo/%s/%s" % (pid, f["id"]), False, "part missing: %s" % e)
                continue
            tol = f["tol_px"]
            rows.add("photo", "photo/%s/%s" % (pid, f["id"]), abs(pred - f["px"]) <= tol,
                     "drawing puts it at %.1f px, measured %.1f px, tolerance %.1f px" % (pred, f["px"], tol))
            # the measuring box lies inside the object's own box
            ob = ph["object_box"]
            bx = f["box"]
            m = 8.0 if f.get("boundary") else 0.5
            inside = bx[0] >= ob[0] - m and bx[1] >= ob[1] - m and bx[2] <= ob[2] + m and bx[3] <= ob[3] + m
            rows.add("photo", "photo/%s/%s box on the object" % (pid, f["id"]), inside, "box %s, object %s" % (bx, ob))
            if gray is not None:
                spec = f["measure"]
                pos, con, spread = L.edge_pos(gray, spec["axis"], spec["band"], spec["win"], spec.get("pol", "any"))
                rows.add("live", "live/%s/%s re-measured" % (pid, f["id"]), abs(pos - f["px"]) <= 0.75,
                         "pixels give %.2f, recorded %.2f (contrast %.1f, spread %.2f)" % (pos, f["px"], con, spread))
        # scale fitted height versus the stated object box
        fit = ph["fit"]
        rows.add("photo", "photo/%s/fitted on height only" % pid, fit.get("fitted_on") == "height",
                 "scale fitted on %s" % fit.get("fitted_on"))


# ------------------------------------------------------------------------------------------------ text rows
def text_rows(T, tdir, rows, extra_files=()):
    strs = [(p, s) for p, s in L.strings({k: v for k, v in T.items() if k not in ("self_check",)})]
    hits = []
    for p, s in strs:
        if "/content_rule_note" in p or "/blocklist" in p:
            continue
        for h in L.words_scan(s):
            hits.append((p, h))
    rows.add("names", "names/target.json has no real maker's or firm's name", not hits, "hits: %s" % hits[:6])
    docs = [("TARGET.md", os.path.join(tdir, "TARGET.md"))] + [(os.path.basename(f), f) for f in extra_files]
    for nm, pth in docs:
        if not os.path.exists(pth):
            rows.add("names", "names/%s present" % nm, False, "missing")
            continue
        txt = open(pth, encoding="utf-8").read()
        h = L.words_scan(txt)
        rows.add("names", "names/%s has no real maker's or firm's name" % nm, not h, "hits: %s" % h[:6])
        if nm == "TARGET.md":
            rows.add("doc", "doc/no em dash", "—" not in txt, "")
            rows.add("doc", "doc/no italics", not re.search(r"(?<![\*\w])\*[^\s\*][^\*\n]*\*(?![\*\w])", txt), "")
            rows.add("doc", "doc/first line is the summary", txt.splitlines()[0].startswith("# ") and len(txt.splitlines()[2]) > 60, "")
    # content rule
    bad = []
    for p, s in strs:
        if "/content_rule_note" in p or "/blocklist" in p:
            continue
        w = set(re.findall(r"[a-z]+", s.lower()))
        for c in CONTENT_WORDS:
            if c in w:
                bad.append((p, c))
    rows.add("content", "content/no alcohol, gambling or children in the data", not bad, "hits: %s" % bad[:6])
    if os.path.exists(os.path.join(tdir, "TARGET.md")):
        txt = open(os.path.join(tdir, "TARGET.md"), encoding="utf-8").read()
        bad2 = []
        for line in txt.splitlines():
            wl = set(re.findall(r"[a-z]+", line.lower()))
            rule_line = "content rule" in line.lower()
            for c in CONTENT_WORDS:
                if c in wl and not (rule_line and c in ABSTRACT_OK_IN_RULE_LINES):
                    bad2.append(c)
        rows.add("content", "content/no alcohol, gambling or children in TARGET.md", not bad2, "hits: %s" % bad2)
    # owed lines for his page
    owed = T.get("owed", [])
    badl = [o["id"] for o in owed if "—" in o["line"] or "*" in o["line"] or "_" in o["line"]]
    rows.add("owed", "owed/no em dash or italics in his lines", not badl, "bad: %s" % badl)
    rows.add("owed", "owed/each line has a recommendation and one question", all(o.get("recommended") and "?" in o["line"] for o in owed), "")
    # night
    nj = json.dumps(T)
    rows.add("night", "night/no stale lantern colour", L.STALE_NIGHT not in nj, "")
    if "night" in T:
        rows.add("night", "night/lantern colour is (1.0, 0.25, 0.0) linear", T["night"].get("lantern_linear") == L.LANTERN_LINEAR, str(T["night"].get("lantern_linear")))


def source_rows(T, rows, tdir):
    ids = set()
    for s in T.get("sources", []):
        ids.add(s["id"])
        need = ["id", "url", "read", "author", "licence", "taken", "shows", "used", "not_used_for", "period"]
        miss = [k for k in need if k not in s or s[k] in (None, "")]
        rows.add("sources", "sources/%s fields" % s["id"], not miss, "missing %s" % miss)
        lic_ok = any(a.lower() in str(s.get("licence", "")).lower() for a in ALLOWED_LICENCES)
        rows.add("sources", "sources/%s licence is free" % s["id"], lic_ok or s.get("kind") in ("book", "own", "web text", "search record", "model list") or s.get("unreached"), str(s.get("licence")))
        rows.add("sources", "sources/%s not NoAI" % s["id"], "noai" not in json.dumps(s).lower().replace("not noai", "").replace("no noai", "").replace("noai-free", ""), "")
        if s.get("unreached"):
            rows.add("sources", "sources/%s unreached is not used" % s["id"], not s.get("used"), "")
    used_photos = {ph["source"] for ph in T.get("photos", [])}
    rows.add("sources", "sources/every measured photograph is a source marked used", all(
        any(s["id"] == u and s.get("used") for s in T.get("sources", [])) for u in used_photos), "")
    for ph in T.get("photos", []):
        s = next((x for x in T["sources"] if x["id"] == ph["source"]), None)
        rows.add("sources", "sources/%s is dated" % ph["source"], bool(s and re.match(r"\d{4}", str(s.get("taken", "")))), str(s.get("taken") if s else None))


def preview_rows(T, rows, tdir, previews_dir):
    from PIL import Image
    for pv in T.get("previews", []):
        p = os.path.join(previews_dir, pv["file"])
        if not os.path.exists(p):
            rows.add("previews", "previews/%s exists" % pv["file"], False, "missing")
            continue
        im = Image.open(p)
        kb = os.path.getsize(p) / 1024
        rows.add("previews", "previews/%s size" % pv["file"], max(im.size) <= 1200 and kb < 300 and im.format == "JPEG",
                 "%dx%d, %.0f KB, %s" % (im.size[0], im.size[1], kb, im.format))
        rows.add("previews", "previews/%s says what was masked and that it was looked at" % pv["file"],
                 "masked" in pv and pv.get("looked_at_full_size") is True and pv.get("no_people_no_drink_no_betting_no_names") is True, str(pv.get("masked")))
        rows.add("previews", "previews/%s credit" % pv["file"], bool(pv.get("credit")), "")


# ------------------------------------------------------------------------------------------------ run everything
def all_rows(T, tdir, extra=None, live=False, previews=False, photos_dir=None, previews_dir=None, doc_check=None):
    rows = L.Rows()
    for V, vs in T["variants"].items():
        ps = _ps_cache(vs["parts"])
        geometry(ps, V, vs, rows)
    numbers_rows(T, rows)
    photo_rows(T, rows, live=live, photos_dir=photos_dir)
    source_rows(T, rows, tdir)
    text_rows(T, tdir, rows)
    if previews:
        preview_rows(T, rows, tdir, previews_dir or L.PREVIEWS)
    if extra:
        try:
            extra(T, rows)
        except Exception as e:  # a part the family's own rows need is gone: that is a failure, not a crash
            rows.add("family", "family/extra rows could be computed", False, "%s: %s" % (type(e).__name__, e))
    if doc_check:
        doc_check(T, rows)
    return rows.rows


# ------------------------------------------------------------------------------------------------ generic controls
def shift_part(T, V, name, d):
    for p in T["variants"][V]["parts"]:
        if p["id"] == name:
            if p["type"] in ("box",):
                p["c"] = [p["c"][i] + d[i] for i in range(3)]
            elif p["type"] == "cyl":
                p["p0"] = [p["p0"][i] + d[i] for i in range(3)]
                p["p1"] = [p["p1"][i] + d[i] for i in range(3)]
            elif p["type"] == "wire":
                p["pts"] = [[q[i] + d[i] for i in range(3)] for q in p["pts"]]
            elif p["type"] == "sphere":
                p["c"] = [p["c"][i] + d[i] for i in range(3)]
            else:
                xf = p.setdefault("xf", {})
                t = xf.setdefault("t", [0, 0, 0])
                xf["t"] = [t[i] + d[i] for i in range(3)]
            return
    raise KeyError(name)


def drop_part(T, V, name):
    T["variants"][V]["parts"] = [p for p in T["variants"][V]["parts"] if p["id"] != name]


def scale_all(T, V, axis, f):
    for p in T["variants"][V]["parts"]:
        xf = p.setdefault("xf", {})
        # a scale cannot be put in xf; scale the numbers of the primitive instead
        def sc(v):
            v = list(v)
            v[axis] = v[axis] * f
            return v
        if p["type"] == "box":
            p["c"] = sc(p["c"])
            s = list(p["s"])
            s[axis] *= f
            p["s"] = s
        elif p["type"] == "cyl":
            p["p0"], p["p1"] = sc(p["p0"]), sc(p["p1"])
        elif p["type"] == "wire":
            p["pts"] = [sc(q) for q in p["pts"]]
        elif p["type"] == "sphere":
            p["c"] = sc(p["c"])
        else:
            if "t" in xf:
                xf["t"] = sc(xf["t"])
            pl = list(p["poly"])
            ax_map = {"xz": (0, 2), "yz": (1, 2), "xy": (0, 1)}[p["plane"]]
            for i, a in enumerate(ax_map):
                if a == axis:
                    p["poly"] = [[q[0] * f, q[1]] if i == 0 else [q[0], q[1] * f] for q in p["poly"]]
                    pl = p["poly"]
            wax = {"xz": 1, "yz": 0, "xy": 2}[p["plane"]]
            if wax == axis:
                p["w"] = [p["w"][0] * f, p["w"][1] * f]


def generic_controls(T, spec):
    """spec: V (variant), leaf (a part that nothing else holds up), bridge (a part that carries another), bridge_child,
    blocker: {face_id: part that closes it}, photo_ref (part id used by a photograph feature), overlap: (part, delta),
    number_id, sliver (part to thin)."""
    V = spec["V"]
    C = []
    mv = spec.get("leaf_move", [0, -30, 0])
    C.append(("geometry: a leaf part moved 30 mm off its support", lambda t: shift_part(t, V, spec["leaf"], mv), "geometry/%s/no floating part" % V))
    C.append(("geometry: a leaf part moved 30 mm off its support (meets)", lambda t: shift_part(t, V, spec["leaf"], mv), "geometry/%s/every part meets a neighbour" % V))
    br = spec["bridge"] if isinstance(spec["bridge"], list) else [spec["bridge"]]
    C.append(("geometry: the carrying part(s) removed so the rest floats", lambda t: [drop_part(t, V, b) for b in br], "geometry/%s/no floating part" % V))
    if spec.get("join"):
        a, b = spec["join"]
        C.append(("geometry: a declared join pulled apart by 25 mm", lambda t: shift_part(t, V, b, spec["join_move"]), "geometry/%s/declared joins meet" % V))
    for fid, blk in spec.get("blocker", {}).items():
        C.append(("geometry: the part that closes face %s removed" % fid, (lambda b: lambda t: drop_part(t, V, b))(blk), "geometry/%s/face %s closed" % (V, fid)))
    if spec.get("overlap"):
        part, delta = spec["overlap"]
        C.append(("geometry: a part pushed deep into its neighbour", lambda t: shift_part(t, V, part, delta), "geometry/%s/no part sinks into another" % V))
    C.append(("geometry: the whole piece 6 percent too tall", lambda t: scale_all(t, V, 2, 1.06), "geometry/%s/overall h" % V))
    if "w" in T["variants"][V].get("overall", {}):
        C.append(("geometry: the whole piece 8 percent too wide", lambda t: scale_all(t, V, 0, 1.08), "geometry/%s/overall w" % V))
    if spec.get("number_id"):
        def tamper(t):
            for n in t["numbers"]:
                if n["id"] == spec["number_id"]:
                    n["value"] = n["value"] * 1.1 + 5
        C.append(("numbers: a printed number changed by 10 percent", tamper, "numbers/%s" % spec["number_id"]))
    for ph in T.get("photos", []):
        if not ph.get("fit"):
            continue
        fid = ph["features"][len(ph["features"]) // 2]["id"]
        # shift every part by moving the whole target 40 mm in z along the photograph's rows
        def ph_shift(t, ph_id=ph["id"]):
            for p in t["variants"][t["photos"][0].get("variant", t["sample"])]["parts"]:
                pass
        C.append(("photograph: the drawing's parts squeezed in width", lambda t: scale_all(t, ph.get("variant", T["sample"]), L.view_axes(ph.get("view", "front"))[0], spec.get("photo_squeeze", 0.92)), "photo/%s/" % ph["id"]))
        break
    C.append(("names: a real operator's name written in a part's material note", lambda t: t["variants"][V]["parts"][0].__setitem__("note", "made by " + L.BLOCKLIST[0]), "names/target.json"))
    C.append(("content: a drink word in a note", lambda t: t["variants"][V]["parts"][0].__setitem__("note", "stacks of beer crates"), "content/no alcohol, gambling or children in the data"))
    C.append(("night: the stale lantern colour put back", lambda t: t.__setitem__("night_old", L.STALE_NIGHT), "night/no stale lantern colour"))
    C.append(("owed: an em dash in a line for his page", lambda t: t["owed"][0].__setitem__("line", t["owed"][0]["line"] + " — now") if t.get("owed") else t.__setitem__("owed", [{"id": "x", "line": "a — b?", "recommended": "y"}]), "owed/no em dash or italics in his lines"))
    C.append(("sources: a source with no licence", lambda t: t["sources"][0].__setitem__("licence", ""), "sources/%s fields" % T["sources"][0]["id"] if T.get("sources") else "sources/"))
    return C


def main(family, tdir, extra=None, extra_controls=None, ctl_spec=None, doc_check=None, argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    live = "--live" in argv
    previews = "--previews" in argv
    photos_dir = None
    if "--photos" in argv:
        photos_dir = argv[argv.index("--photos") + 1]
    elif live:
        photos_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(tdir)))), "ledger-scratch", "street-dressing", family)
    tpath = os.path.join(tdir, "target.json")
    T = json.load(open(tpath))
    options = "offline" if not (live or previews) else " ".join(o for o in ("--live" if live else "", "--previews" if previews else "") if o)
    kw = dict(extra=extra, live=live, previews=previews, photos_dir=photos_dir, doc_check=doc_check, tdir=tdir)
    rows = all_rows(T, **kw)
    ctl = []
    if "--no-controls" not in argv:
        controls = generic_controls(T, ctl_spec) + (extra_controls(T) if extra_controls else [])
        ctl = L.run_controls(T, controls, lambda t, **k: all_rows(t, **k), rows, **kw)
    line, bad = L.print_and_store(family, T, tpath, rows, ctl, options)
    return bad
