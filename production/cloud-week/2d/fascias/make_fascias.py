#!/usr/bin/env python
"""make_fascias.py: the finished fascia textures of Quay Street, by script, from target.json alone (unit 4.1, cloud week 42).

    /home/user/.bpyenv/bin/python make_fascias.py OUTDIR [--only mickeys,ritas,...] [--seed-base 1] [--jobs 4] [--pack none|pad|stretch]
    python make_fascias.py OUTDIR --verify            # rebuild into a scratch folder and compare every SHA-256 with OUTDIR/manifest.json

Reads  production/cloud-week/targets/fascia-signs/target.json (amended in memory by fascia_common.apply_amendments; the target is not edited),
       the OFL fonts in production/fonts/, production/specs/hook-cast.json (the hours plates).
Writes into OUTDIR (nothing else, never into git):
       fascias/<id>/<id>_{basecolour,height,orm,emissive,wear}.png     ten boards, 5410 x 550 px = 5410 x 550 mm, row 0 the TOP, column 0 the
                                                                        viewer's LEFT as the GAME shows the board
       signs/<sign>/...                                                 the four hanging signs' faces (and the three gilt balls)
       glass/<shop>/...                                                 the glass lettering rows (RGBA tiles) and the empty unit's whitewashed window
       panels/...                                                       the letting board and the five hours plates
       manifest.json                                                    every file, its size in pixels and millimetres, the board, its words, fonts, seed, SHA-256

Maps:  basecolour  sRGB 8-bit (RGBA for glass tiles; colour is straight, not premultiplied)
       height      16-bit grey, 32768 = the board face, 25600 units = 1 mm  (so the high byte is the target's 8-bit map: 128 + mm/0.01)
       orm         linear 8-bit: R = 255 (no occlusion drawn), G = roughness, B = metal
       emissive    sRGB 8-bit, only on the lit boxes (steam laundry, newsagent, the laundry's hanging box): its face colour x the level
       wear        linear 8-bit masks: R rain runs, G gull marks, B rust runs (the layers G13 counts)
Deterministic: every random draw comes from a numpy Generator seeded from (seed base, board name); the same seed gives the same pixels.
"""
import argparse
import hashlib
import json
import os
import platform
import sys
import time
from multiprocessing import Pool
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import fascia_boards as fb          # noqa: E402
import fascia_common as fc          # noqa: E402
import fascia_paint as fp           # noqa: E402
import fascia_small as fs           # noqa: E402
from fascia_common import H_MM, W_MM   # noqa: E402

SCHEMA = "ledger.cloud-week-42.fascias-manifest/1"
H_SCALE = 25600.0        # 16-bit height units per mm


# ------------------------------------------------------------------ files
def _png_path(out, rel):
    p = Path(out) / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


def _hash(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _pix_hash(arr):
    a = np.ascontiguousarray(arr)
    return hashlib.sha256(str(a.shape).encode() + str(a.dtype).encode() + a.tobytes()).hexdigest()


def save(out, rel, arr, mode_note, size_mm, extra=None):
    """write one PNG and return its manifest row"""
    p = _png_path(out, rel)
    img = Image.fromarray(arr)
    img.save(p, format="PNG", compress_level=6)
    h, w = arr.shape[:2]
    row = dict(file=str(rel).replace(os.sep, "/"), size_px=[int(w), int(h)], size_mm=[float(size_mm[0]), float(size_mm[1])], encoding=mode_note,
               bytes=int(p.stat().st_size), sha256=_hash(p), sha256_pixels=_pix_hash(arr))
    if extra:
        row.update(extra)
    return row


def u8(rgb):
    return np.clip(np.round(rgb), 0, 255).astype(np.uint8)


def height16(h_mm):
    return np.clip(np.round(32768.0 + h_mm * H_SCALE), 0, 65535).astype("<u2")


def orm8(rough, metal):
    o = np.empty(rough.shape + (3,), np.uint8)
    o[..., 0] = 255
    o[..., 1] = u8(rough * 255.0)
    o[..., 2] = u8(metal * 255.0)
    return o


def write_maps(out, folder, stem, B, size_mm, lit=False, wear=False, alpha=None):
    files = {}
    base = u8(B.rgb)
    if alpha is not None:
        base = np.dstack([base, u8(alpha * 255.0)])
    files["basecolour"] = save(out, f"{folder}/{stem}_basecolour.png", base, "sRGB 8-bit" + (" + straight alpha" if alpha is not None else ""), size_mm)
    if np.abs(B.height).max() > 0:
        files["height"] = save(out, f"{folder}/{stem}_height.png", height16(B.height), "16-bit grey; 32768 = face; 25600 units = 1 mm (up is raised)", size_mm)
    files["orm"] = save(out, f"{folder}/{stem}_orm.png", orm8(B.rough, B.metal), "linear 8-bit: R=255 (no AO), G=roughness, B=metal", size_mm)
    if B.emis is not None:
        files["emissive"] = save(out, f"{folder}/{stem}_emissive.png", u8(B.emis), "sRGB 8-bit, the lit face; zero where not lit", size_mm)
    if wear and "runs" in B.layers:
        w = np.zeros((B.H, B.W, 3), np.uint8)
        w[..., 0] = u8(np.clip(B.layers["runs"], 0, 1) * 255.0)
        w[..., 1] = u8(np.clip(B.layers["gull"], 0, 1) * 255.0)
        w[..., 2] = u8(np.clip(B.layers["rust"], 0, 1) * 255.0)
        files["wear"] = save(out, f"{folder}/{stem}_wear.png", w, "linear 8-bit masks: R rain runs, G gull marks, B rust runs", size_mm)
    return files


# ------------------------------------------------------------------ tasks (each returns a JSON-able record)
def board_seed(seed_base, name):
    return fc.seed_for("fascias", seed_base, name)


def task_fascia(args):
    out, sid, seed_base = args
    T = fc.load_target()
    s = fc.shop_by_id(T, sid)
    seed = board_seed(seed_base, sid)
    t0 = time.time()
    B, info = fb.render_fascia(T, s, seed)
    files = write_maps(out, f"fascias/{sid}", sid, B, (W_MM, H_MM), wear=True)
    rec = dict(kind="fascia", id=sid, shop=sid, side=s["side"], street_x_m=s["street_x_m"], layout_class=s["layout_class"], construction=s["construction_kind"],
               door_end_street=s["door_end_street"], board_u0_street_x_m=s["board_u0_street_x_m"], u_rule=s["board_u_rule"], seed=int(seed),
               size_px=[W_MM, H_MM], size_mm=[W_MM, H_MM], files=files, strings_drawn=info["blocks"], ghosts=info["ghosts"], wear=info["wear"],
               loss=info["loss"], shapes_drawn=info.get("shapes_drawn", []), moulding=info.get("moulding"), emissive=info.get("emissive"),
               shadow=info.get("shadow"), holes=info.get("holes"), vinyl_lift=info.get("vinyl_lift"), old_board_loss_target=info.get("old_board_loss_target"),
               geometry=geometry_rows(T, s), seconds=round(time.time() - t0, 1))
    rec["words"] = sorted({b["string"] for b in info["blocks"] if b.get("string")})
    rec["fonts"] = sorted({b["font"] for b in info["blocks"] if b.get("font")})
    return rec


def geometry_rows(T, s):
    rows = []
    for g in s["geometry"]:
        r = dict(g)
        if g.get("face_texture_rect_mm"):
            x0, y0, x1, y1 = g["face_texture_rect_mm"]
            r["uv_rect_top_left_origin"] = [round(x0 / W_MM, 5), round(1 - y1 / H_MM, 5), round(x1 / W_MM, 5), round(1 - y0 / H_MM, 5)]
            r["note"] = "the geometry's front face takes this rectangle of the fascia texture (u, v with the origin at the TOP-LEFT of the image, v down)"
        rows.append(r)
    return rows


def task_sign(args):
    out, sid, label, seed_base = args
    T = fc.load_target()
    sign = [p for p in T["projecting_signs"] if p["id"] == sid][0]
    seed = fc.seed_for("signs", seed_base, sid, label)
    S, rec = fs.render_sign_face(T, sign, label, seed)
    files = write_maps(out, f"signs/{sid}", f"{sid}_face_{label}", S.B, tuple(rec["size_mm"]), wear=False)
    rec.pop("b", None)
    return dict(kind="sign_face", id=f"{sid}.{label}", sign=sid, shop=sign["shop"], seed=int(seed), size_px=rec["size_mm"], size_mm=rec["size_mm"], files=files,
                block=rec["block"], cap_mm_target=rec["cap_mm_target"], cap_mm_built=rec["cap_mm_built"], available_mm=rec["available_mm"],
                ink_width_target_cap_mm=rec["ink_width_target_cap_mm"], wear=rec["wear"], emissive=rec.get("emissive"),
                reads="left to right from its own side (mirror-correct, not mirrored)")


def task_ball(args):
    out, k, seed_base = args
    T = fc.load_target()
    seed = fc.seed_for("signs", seed_base, "ball", k)
    S, rec = fs.render_ball(T, k, seed)
    files = write_maps(out, "signs/ritas_three_balls", f"ball_{k}", S.B, tuple(rec["size_mm"]))
    return dict(kind="ball", id=f"ritas_three_balls.ball_{k}", sign="ritas_three_balls", shop="ritas", seed=int(seed), size_px=rec["size_mm"], size_mm=rec["size_mm"], files=files, note=rec["note"])


def slug(text):
    return "".join(c.lower() if c.isalnum() else "-" for c in text).strip("-").replace("--", "-")


def task_glass(args):
    out, idx, seed_base = args
    T = fc.load_target()
    g = T["glass_lettering"][idx]
    seed = fc.seed_for("glass", seed_base, idx)
    S, A, face_alpha, rec = fs.render_glass_row(T, g, idx, seed)
    W, H = rec["size_mm"]
    base = np.dstack([u8(S.B.rgb), u8(A * 255.0)])
    stem = f"{idx:02d}_{slug(g['text'])}"
    files = {}
    files["rgba"] = save(out, f"glass/{g['shop']}/{stem}_rgba.png", base, "sRGB 8-bit + straight alpha (seen from the street)", (W, H))
    files["orm"] = save(out, f"glass/{g['shop']}/{stem}_orm.png", orm8(S.B.rough, S.B.metal), "linear 8-bit: R=255, G=roughness, B=metal", (W, H))
    ink = rec["face_alpha_ink_box_in_tile_mm"]
    # where the tile goes: street x of the ink centre, z of the baseline, the tile's own centre and size
    cx_in_tile = (ink[0] + ink[2]) / 2.0
    base_row = rec["baseline_row_from_bottom_mm"]
    place = dict(x_street_m_of_ink_centre=g["x_street_m"], z_baseline_m=g["z_m"],
                 tile_left_street_offset_mm=round(-cx_in_tile, 1), tile_baseline_from_tile_bottom_mm=base_row,
                 note="u runs from the viewer's left to right in the game; the tile's ink centre stands at x_street_m, its baseline at z_baseline_m above the pavement")
    return dict(kind="glass_row", id=f"{g['shop']}.glass.{idx}", row=idx, shop=g["shop"], surface=g["surface"], string=g["text"], font=g["font"], weight=g["weight"],
                cap_mm=g["cap_mm"], technique=g["technique"], style=rec["style"], seed=int(seed), size_px=[W, H], size_mm=[W, H], files=files, place=place,
                ink_box_in_tile_mm=ink, source=g["source"], kind_of_number=g["kind"], proposed=(g["kind"] == "Judgement"))


def task_wash(args):
    out, seed_base = args
    T = fc.load_target()
    seed = fc.seed_for("glass", seed_base, "empty_window")
    S, a = fs.render_window_wash(T, seed)
    H, W = a.shape
    base = np.dstack([u8(S.B.rgb), u8(a * 255.0)])
    files = dict(rgba=save(out, "glass/empty_unit/window_whitewash_rgba.png", base, "sRGB 8-bit + straight alpha", (W, H)),
                 orm=save(out, "glass/empty_unit/window_whitewash_orm.png", orm8(S.B.rough, S.B.metal), "linear 8-bit: R=255, G=roughness, B=metal", (W, H)))
    return dict(kind="glass_wash", id="empty_unit.glass.window", shop="empty_unit", surface="whole display window, whitewashed (ruled 3 Oct): brush arcs, nothing legible",
                string=None, seed=int(seed), size_px=[W, H], size_mm=[W, H], files=files,
                place=dict(window_glass_x_m_about_window_centre=[-1.625, 1.625], z_m=[0.60, 2.40], window_centre_street_x_m=fc.shop_by_id(T, "empty_unit")["window_centre_street_x_m"],
                           note="the kit's display glass (terrace-front.py KIT_GLASS): 3.25 m wide, z 0.60 to 2.40; the tile covers it at one pixel a millimetre (3250 x 1800)"),
                mean_alpha=round(float(a.mean()), 3))


def task_letting(args):
    out, seed_base = args
    T = fc.load_target()
    seed = fc.seed_for("panels", seed_base, "letting_board")
    S, rec = fs.render_letting_board(T, seed)
    W, H = rec["size_mm"]
    files = write_maps(out, "panels/letting_board", "letting_board", S.B, (W, H))
    return dict(kind="panel", id="letting_board", shop="empty_unit", seed=int(seed), size_px=[W, H], size_mm=[W, H], files=files, string="TO LET",
                block=dict(font=rec["block"]["font"], weight=rec["block"]["weight"], cap_mm=rec["block"]["cap_mm"], ink_box_mm=[round(v, 1) for v in rec["block"]["ink_box_mm"]]),
                screws_mm=rec["screws"], askew_deg=rec["askew_deg"], centre_on_fascia_mm=rec["centre_on_fascia_mm"],
                note="a separate board screwed over the empty unit's fascia: geometry 900 x 450 mm, turned 2 degrees; not painted into the fascia texture")


def task_hours(args):
    out, sid, seed_base = args
    T = fc.load_target()
    cast = json.loads(fc.HOOK_CAST.read_text(encoding="utf-8"))
    seed = fc.seed_for("panels", seed_base, "hours", sid)
    S, rec = fs.render_hours_plate(T, sid, cast, seed)
    W, H = rec["size_mm"]
    files = write_maps(out, "panels/hours_plates", f"hours_{sid}", S.B, (W, H))
    return dict(kind="panel", id=f"hours_plate.{sid}", shop=sid, seed=int(seed), size_px=[W, H], size_mm=[W, H], files=files, lines=rec["lines"],
                font="libre-franklin", weight=700, cap_mm=rec["cap_mm"], cap_mm_target=rec["cap_mm_target"], available_mm=rec["available_mm"], widest_line_at_target_cap_mm=rec["widest_at_target_cap_mm"],
                source="production/specs/hook-cast.json hours (read at build time)",
                where="on the shop door's glass or the pilaster, centre 1.45 m up")


def run_task(job):
    kind = job[0]
    fn = {"fascia": task_fascia, "sign": task_sign, "ball": task_ball, "glass": task_glass, "wash": task_wash, "letting": task_letting, "hours": task_hours}[kind]
    return fn(job[1:] if kind != "fascia" else job[1:])


def build_jobs(out, only, seed_base):
    T = fc.load_target()
    jobs = []
    for s in T["shops"]:
        if not only or s["id"] in only:
            jobs.append(("fascia", out, s["id"], seed_base))
    if not only or "signs" in only:
        for p in T["projecting_signs"]:
            if p["id"] == "ritas_three_balls":
                for k in (1, 2, 3):
                    jobs.append(("ball", out, k, seed_base))
            else:
                for lab in ("a", "b"):
                    jobs.append(("sign", out, p["id"], lab, seed_base))
    if not only or "glass" in only:
        for i, g in enumerate(T["glass_lettering"]):
            if g.get("existing"):
                continue
            if g["text"]:
                jobs.append(("glass", out, i, seed_base))
        jobs.append(("wash", out, seed_base))
    if not only or "panels" in only:
        jobs.append(("letting", out, seed_base))
        for sid in ("ritas", "fish_market", "steam_laundry", "newsagent", "tea_rooms"):
            jobs.append(("hours", out, sid, seed_base))
    return jobs


# ------------------------------------------------------------------ packing for Unreal (only if the 5.8.2 check says a non power of two needs it)
def pack_file(out, row, mode):
    """write a power-of-two copy of one map next to it: pad (the picture top-left, edge pixels repeated) or stretch"""
    p = Path(out) / row["file"]
    img = Image.open(p)
    w, h = img.size
    if mode == "pad":
        W2, H2 = 8192, 1024
        if (w, h) != (W_MM, H_MM):
            W2, H2 = 1 << (w - 1).bit_length(), 1 << (h - 1).bit_length()
        arr = np.asarray(img)
        pad = ((0, H2 - h), (0, W2 - w)) + (((0, 0),) if arr.ndim == 3 else ())
        big = np.pad(arr, pad, mode="edge")
        dst = p.with_name(p.stem + f"_pad{W2}x{H2}.png")
        Image.fromarray(big).save(dst)
        return dict(file=str(dst.relative_to(out)).replace(os.sep, "/"), size_px=[W2, H2], uv_scale=[round(w / W2, 5), round(h / H2, 5)], mode="pad")
    W2, H2 = (5120, 512) if (w, h) == (W_MM, H_MM) else (1 << round(np.log2(w)), 1 << round(np.log2(h)))
    if img.mode in ("I;16", "I"):
        a = np.asarray(img).astype(np.float32)
        big = np.clip(np.round(np.asarray(Image.fromarray(a, mode="F").resize((W2, H2), Image.LANCZOS))), 0, 65535).astype("<u2")
        dst = p.with_name(p.stem + f"_stretch{W2}x{H2}.png")
        Image.fromarray(big).save(dst)
    else:
        dst = p.with_name(p.stem + f"_stretch{W2}x{H2}.png")
        img.resize((W2, H2), Image.LANCZOS).save(dst)
    return dict(file=str(dst.relative_to(out)).replace(os.sep, "/"), size_px=[W2, H2], uv_scale=[1.0, 1.0], mode="stretch")


# ------------------------------------------------------------------ manifest
def environment():
    import scipy
    import PIL
    from PIL import features
    return dict(python=platform.python_version(), numpy=np.__version__, scipy=scipy.__version__, pillow=PIL.__version__,
                freetype=features.version("freetype2"), raqm=features.version("raqm"), platform=platform.platform(),
                note="the SHA-256 of a PNG matches only on the same library versions; sha256_pixels is the hash of the raw array")


def fonts_used(T):
    seen = {}
    for key, w in (("marcellus-sc", 400), ("abril-fatface", 400), ("old-standard-tt-bold", 700), ("oswald", 600), ("jost", 800), ("libre-franklin", 700), ("libre-franklin", 800),
                   ("libre-franklin", 900), ("fraunces", 900), ("alfa-slab-one", 400), ("josefin-sans", 700), ("patrick-hand", 400)):
        rel, h = fc.font_sha(key, w)
        seen[rel] = h
    return [dict(file=k, sha256=v) for k, v in sorted(seen.items())]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("outdir")
    ap.add_argument("--only", default="", help="comma list of board ids, or signs, glass, panels")
    ap.add_argument("--seed-base", type=int, default=1)
    ap.add_argument("--jobs", type=int, default=min(4, os.cpu_count() or 1))
    ap.add_argument("--pack", choices=["none", "pad", "stretch"], default="none", help="also write power-of-two copies (see NOTES.md, the 5.8.2 texture-size check)")
    ap.add_argument("--verify", action="store_true", help="rebuild and compare SHA-256 with OUTDIR/manifest.json")
    a = ap.parse_args(argv)
    out = Path(a.outdir)
    only = {x for x in a.only.split(",") if x}
    if a.verify:
        ref = json.loads((out / "manifest.json").read_text(encoding="utf-8"))
        scratch = out.parent / (out.name + "_verify")
        sub = main([str(scratch), "--seed-base", str(ref["seed_base"]), "--jobs", str(a.jobs)] + (["--only", a.only] if a.only else []))
        new = json.loads((scratch / "manifest.json").read_text(encoding="utf-8"))
        old_rows = {r["file"]: r for r in iter_files(ref)}
        bad, same = [], 0
        for r in iter_files(new):
            o = old_rows.get(r["file"])
            if o is None:
                continue
            if o["sha256"] == r["sha256"]:
                same += 1
            elif o["sha256_pixels"] == r["sha256_pixels"]:
                same += 1
            else:
                bad.append(r["file"])
        print(f"VERIFY: {same} files identical, {len(bad)} different" + (f": {bad[:6]}" if bad else ""))
        return 1 if bad else 0
    out.mkdir(parents=True, exist_ok=True)
    jobs = build_jobs(str(out), only, a.seed_base)
    t0 = time.time()
    if a.jobs > 1:
        with Pool(a.jobs) as pool:
            recs = pool.map(run_task, jobs, chunksize=1)
    else:
        recs = [run_task(j) for j in jobs]
    T = fc.load_target()
    man = dict(schema=SCHEMA, script=fc.SCRIPT_VERSION, command=f"make_fascias.py OUTDIR --seed-base {a.seed_base}" + (f" --only {a.only}" if a.only else ""),
               seed_base=a.seed_base, built_seconds=round(time.time() - t0, 1), target="production/cloud-week/targets/fascia-signs/target.json",
               target_sha256=hashlib.sha256(fc.TARGET_JSON.read_bytes()).hexdigest(), amendments=T["_amendments"], environment=environment(), fonts=fonts_used(T),
               scale="1 pixel = 1 millimetre", axis=dict(rule=T["axis"]["rule"], u="column 0 is the viewer's LEFT as the game shows the board; row 0 is the TOP", board_mm=[W_MM, H_MM]),
               board=dict(mm=[W_MM, H_MM], z_bottom_m=T["board"]["z_bottom_m"], z_top_m=T["board"]["z_top_m"], proud_of_wall_mm=T["board"]["proud_of_wall_mm"],
                          between_consoles_in_bay_m=T["board"]["between_consoles_in_bay_m"]),
               boards=[r for r in recs if r["kind"] == "fascia"], hanging_signs=[], glass_lettering=[], small_panels=[])
    man["boards"].sort(key=lambda r: [s["id"] for s in T["shops"]].index(r["id"]))
    for p in T["projecting_signs"]:
        faces = [r for r in recs if r["kind"] in ("sign_face", "ball") and r.get("sign") == p["id"]]
        faces.sort(key=lambda r: r["id"])
        man["hanging_signs"].append(dict(id=p["id"], shop=p["shop"], mount=p["mount"], parts=p["parts"], materials=p.get("materials"), lowest_m=p["lowest_m"],
                                         lowest_computed_m=p["lowest_computed_m"], faces=faces,
                                         constants_not_textured="the iron bracket, rings, chains and rods are plain materials: iron = sign_black 0.60 rough 0.50 metal (wrought_iron); "
                                                                "rust at the bolt heads is the builder's wear layer"))
    gl = [r for r in recs if r["kind"] in ("glass_row", "glass_wash")]
    gl.sort(key=lambda r: (r.get("row", 999)))
    man["glass_lettering"] = gl
    pn = [r for r in recs if r["kind"] == "panel"]
    pn.sort(key=lambda r: r["id"])
    man["small_panels"] = pn
    man["not_drawn_here"] = dict(existing_not_approved=T["existing_not_approved"],
                                 note="MINICABS · 24 HOURS and 0632 960418 on Mickey's glass are another family's and are not drawn")
    man["geometry_for_the_blender_builder"] = dict(
        mickeys_letters=[s for s in T["shops"] if s["id"] == "mickeys"][0]["geometry"],
        boxes=[dict(board=s["id"], **g) for s in T["shops"] for g in s["geometry"] if g["kind"] in ("box_sign", "flat_panel")])
    if a.pack != "none":
        for r in [x for x in man["boards"]] + [x for x in man["hanging_signs"]]:
            files = r["files"] if "files" in r else None
            if files:
                r["packed"] = {k: pack_file(out, v, a.pack) for k, v in files.items()}
    (out / "manifest.json").write_text(json.dumps(man, indent=1, ensure_ascii=False, default=lambda o: o.item() if hasattr(o, "item") else str(o)), encoding="utf-8")
    nfiles = sum(1 for _ in iter_files(man))
    print(f"made {nfiles} PNGs for {len(man['boards'])} boards, {sum(len(h['faces']) for h in man['hanging_signs'])} sign faces, {len([g for g in gl if g['kind']=='glass_row'])} glass rows, "
          f"{len(pn)} panels in {man['built_seconds']} s -> {out}")
    return 0


def iter_files(man):
    def walk(o):
        if isinstance(o, dict):
            if "sha256" in o and "file" in o and "sha256_pixels" in o:
                yield o
            else:
                for v in o.values():
                    yield from walk(v)
        elif isinstance(o, list):
            for v in o:
                yield from walk(v)
    for k in ("boards", "hanging_signs", "glass_lettering", "small_panels"):
        yield from walk(man.get(k, []))


if __name__ == "__main__":
    sys.exit(main())
