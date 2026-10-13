"""sd_family: the thin layer every family's scripts share (measure, write, self-check, previews, drawing)."""
import json
import os
import sys

import sd_lib as L
import sd_check as K
import sd_doc as D
import sd_photo as P

SCRATCH_ROOT = os.environ.get("SD_SCRATCH_ROOT", "/home/user/ledger-scratch/street-dressing")


def scratch(family):
    p = os.path.join(SCRATCH_ROOT, family)
    os.makedirs(p, exist_ok=True)
    return p


def measure_main(here, family, gid, key, object_box, features, fname="photo_measurements.json"):
    """Measure the features on a Geograph photograph and write them. Features: dicts with id, axis, band, win, pol."""
    pg, path = L.sampled_photo(gid, key, scratch(family))
    print(pg)
    g = L.load_gray(path)
    out = {}
    for f in features:
        p, c, sp = L.edge_pos(g, f["axis"], f["band"], f["win"], f.get("pol", "any"))
        out[f["id"]] = dict(px=round(p, 2), contrast=round(c, 1), spread=round(sp, 2), **f)
        print("%-16s %7.2f  contrast %5.1f  spread %4.2f" % (f["id"], p, c, sp))
    res = {"photo": key, "gid": gid, "size": list(g.shape[::-1]), "object_box": object_box, "features": out, "page": pg}
    old = {}
    pth = os.path.join(here, fname)
    if os.path.exists(pth):
        old = json.load(open(pth))
    old[key] = res
    json.dump(old, open(pth, "w"), indent=1)
    return res


def photo_entry(pm, pid, source, variant, refs, fit_parts, anchors, boundary=(), view="front", method="", fit_top="", fit_bottom="", centre_from=None, min_tol=4.0, file=None):
    """Build the T['photos'] entry from a measurement record. refs: {feature id: (axis, part, side)}."""
    F = pm["features"]
    feats = []
    for fid, f in F.items():
        if fid not in refs:
            continue
        ax, part, side = refs[fid][:3]
        extra = refs[fid][3] if len(refs[fid]) > 3 else {}
        band, win = f["band"], f["win"]
        box = [band[0], win[0], band[1], win[1]] if ax == "y" else [win[0], band[0], win[1], band[1]]
        err = max(min_tol, 3.0 * f["spread"] + 2.0)
        ref = {"part": part, "side": side}
        ref.update(extra)
        feats.append({"id": fid, "axis": ax, "px": f["px"], "box": box, "tol_px": round(err, 1), "contrast": f["contrast"],
                      "measure": {"axis": f["axis"], "band": band, "win": win, "pol": f.get("pol", "any")}, "ref": ref,
                      "anchor": fid in anchors, "boundary": fid in boundary})
    xc = centre_from(F) if centre_from else None
    return {"id": pid, "source": source, "file": (file or pm["photo"] + ".jpg"), "view": view, "variant": variant, "object_box": pm["object_box"],
            "fit": {"parts": fit_parts, "y_top_px": F[fit_top]["px"], "y_bottom_px": F[fit_bottom]["px"], "x_centre_px": round(xc, 2) if xc is not None else None,
                    "fitted_on": "height", "view": view},
            "features": feats, "method": method}


def write_all(here, T, S):
    tpath = os.path.join(here, "target.json")
    old = {}
    if os.path.exists(tpath):
        try:
            old = json.load(open(tpath)).get("self_check", {})
        except Exception:
            old = {}
    if old:
        T["self_check"] = old
    json.dump(T, open(tpath, "w"), indent=1)
    open(os.path.join(here, "TARGET.md"), "w", encoding="utf-8").write(D.std_doc(T, S))
    nparts = sum(len(v["parts"]) for v in T["variants"].values())
    print("written %s: %d variants, %d parts; TARGET.md %d bytes" % (T["family"], len(T["variants"]), nparts, os.path.getsize(os.path.join(here, "TARGET.md"))))


def selfcheck_main(here, family, extra, extra_controls, spec, argv=None):
    return K.main(family, here, extra=extra, extra_controls=extra_controls, ctl_spec=spec, argv=argv)


def previews_main(here, family, specs):
    """specs: list of dict(gid, key, crop, blur=[], fill=[], name, overlay_name=None, photo_id=None)."""
    T = json.load(open(os.path.join(here, "target.json")))
    out = os.path.join(L.PREVIEWS, family)
    from PIL import Image
    for s in specs:
        pg, path = L.sampled_photo(s["gid"], s["key"], scratch(family))
        im = Image.open(path).convert("RGB")
        m = P.blur_boxes(im, s.get("blur", []), radius=s.get("radius", 7)) if s.get("blur") else im
        m = P.fill_boxes(m, s["fill"]) if s.get("fill") else m
        r = P.save_limited(m.crop(s["crop"]), os.path.join(out, s["name"]))
        print(s["name"], r)
        if s.get("overlay_name"):
            ph = [p for p in T["photos"] if p["id"] == s["photo_id"]][0]
            ov = P.overlay(m.copy(), T, ph).crop(s["crop"])
            print(s["overlay_name"], P.save_limited(ov, os.path.join(out, s["overlay_name"])))


def drawing_main(here, argv):
    return L.drawing_main(here, argv)
