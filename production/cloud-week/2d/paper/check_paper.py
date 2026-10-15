#!/usr/bin/env python
"""check_paper.py: the automatic check of the paper maker's pictures (units 4.2, 4.3 and 4.4, cloud week 42).

    /home/user/.bpyenv/bin/python check_paper.py OUTDIR [--only P01,K05] [--jobs 4] [--seeds 5] [--no-controls] [--write checks/check_v1.json]

OUTDIR is what make_paper.py wrote. The check reads the PNG files (not the maker's arrays), turns every colour picture back into the ink masks the target's reader takes
(paper_reader.py: its own flat reference, nearest-colour classification), and runs the target's own reader (`self_check.all_pixel_checks`: .words, .mask, .pos, .glyphs,
.square) on them, then its own rows:

  <ID>.files, <ID>.manifest     sizes and modes agree with the target; the glyph manifest is the approved string, inside the envelope
  <ID>.clean.read               the class-A picture before wear: every pixel check of the reader passes
  <ID>.clean.stray              ITEM.clean read from the colour picture: at most 2 mm2 differs from the flat reference outside the lettering's windows, the shapes' edges, the art and the cue patch
  <ID>.<c>.read                 each delivered class: classes A and B must pass every pixel check; C and D (weathered on purpose) are reported
  <ID>.<c>.paper, .ink, .contrast, .loss, .wear     colours, contrast and wear counts against the target's numbers for the class
  <ID>.<c>.holes                no loss of paper that does not reach the sheet's edge is over 0.2 per cent of the sheet
  <ID>.<c>.height               no height pixel clipped at 0 or 65535 (the height scale is chosen per picture: 25600, 8192 or 4096 units a mm)
  <ID>.<c>.tears                the second street review's tests on the tear lines (the maker's log): no 40 mm turning 150 degrees one way, two sharp vertices a line, no tongue
  <ID>.cue                      a hand card's tape tab or sucker reads LEFT (G.mirror.cues); the mirrored card reads RIGHT
  <ID>.relief                   a cast or pressed plate's letters and border stand the target's height above its face

then the controls (wrong things that must FAIL) and the seeded false-failure runs. Writes the rows into --write.
"""
import argparse
import json
import math
import sys
import time
from multiprocessing import Pool
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage as ndi

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import paper_common as pc          # noqa: E402
import paper_reader as rd          # noqa: E402

_G = {}


def init(out):
    sc, gl = pc.load_reader(out)
    _G["sc"], _G["gl"], _G["P"] = sc, gl, pc.Palette(sc.T)
    _G["out"] = Path(out)


def load(out, rel):
    im = Image.open(Path(out) / rel)
    arr = np.asarray(im.convert("RGBA")).astype(np.float32)
    return arr[..., :3], arr[..., 3] / 255.0, im.mode, im.size


def wcag(a, b):
    def lum(c):
        c = np.asarray(c, float) / 255.0
        c = np.where(c <= 0.03928, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
        return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
    la, lb = lum(a), lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


class Rows(object):
    def __init__(self):
        self.rows = []

    def add(self, id_, ok, detail="", reported=False):
        self.rows.append(dict(id=id_, ok=bool(ok), detail=str(detail)[:600], reported=bool(reported)))


def read_picture(sc, P, it, rgb, alpha, cls, tau=1.0, tape=True, despeckle=False):
    ref, ref_alpha = rd.flat_reference(sc, P, it, cls, tau)
    masks = rd.block_masks(sc, P, it, rgb, cls, ref, tau, alpha=alpha > 0.5, tape=tape, despeckle=despeckle)
    return ref, masks, rd.union_mask(masks, rgb.shape[:2])


def stray_mm2(sc, it, rgb, alpha, ref):
    """ITEM.clean from the colour picture: the area (mm2) that differs from the flat reference by more than 20 CIE76 outside every block's glyph window, the shapes' edges (1.5 mm), the art
    and the cue patch."""
    ppm = float(it["px_per_mm"])
    H = it["format"]["h_mm"]
    h, w = rgb.shape[:2]
    allowed = np.zeros((h, w), bool)
    for b in it["blocks"]:
        if b.get("ghost"):
            continue
        x0, x1, y0, y1 = sc.glyph_window(it, b, (h, w), ppm)
        allowed[y0:y1, x0:x1] = True
    edges = (np.abs(np.diff(ref, axis=0, prepend=ref[:1])).max(-1) > 1) | (np.abs(np.diff(ref, axis=1, prepend=ref[:, :1])).max(-1) > 1)
    edges = ndi.binary_dilation(edges, sc.gl.disk(max(1, int(round(1.5 * ppm))))) if edges.any() else edges
    boxes = [a["box_mm"] for a in it["art"]]
    mc = it.get("mirror_cue")
    if mc:
        boxes.append(mc["patch_left_mm"])
    if (it.get("fixing") or {}).get("kind") == "string":          # the sucker, the knot and the string up to the top edge are the fixing, not stray ink (K02 has no mirror cue)
        boxes.append((0.0, it["format"]["h_mm"] - 30.0, 30.0, it["format"]["h_mm"]))
    for x0, y0, x1, y1 in boxes:
        allowed[max(0, int((H - y1) * ppm)):int((H - y0) * ppm) + 1, max(0, int(x0 * ppm)):int(x1 * ppm) + 1] = True
    d = np.sqrt(((pc.lab_of(rgb).astype(np.float32) - pc.lab_of(ref).astype(np.float32)) ** 2).sum(-1))
    stray = (d > 20) & ~allowed & ~edges & (alpha > 0.5)
    return float(stray.sum()) / (ppm * ppm), stray


def core_median(rgb, mask, ppm, ink=None):
    """The colour of a block's ink: the median of the half of its pixels nearest the ideal ink (the thin strokes of small lettering have no pixel that is all ink, so the median of every
    pixel would measure the edges)."""
    if mask.sum() < 10:
        return None
    px = rgb[mask]
    if ink is not None:
        d = np.abs(px - np.asarray(ink, np.float32)).sum(-1)
        px = px[d <= np.median(d)]
    return np.median(px, axis=0)


def sc_disk(k):
    return _G["gl"].disk(k)


def inner_losses(alc, al):
    """(count, [share of the sheet of each inner loss over 0.2 per cent]): the losses of paper (card in the clean picture, gone in the weathered one) that do not reach the sheet's edge
    (the close review's finding 1: a bill is torn from its edges; a hole in the middle with paper all round is a maker's fault)."""
    card = alc > 0.5
    gone = card & (al < 0.5)
    if not gone.any():
        return 0, []
    lab, n = ndi.label(gone)
    edge = ndi.binary_dilation(~card, iterations=2)
    edge[0, :] = edge[-1, :] = edge[:, 0] = edge[:, -1] = True
    touching = set(np.unique(lab[edge & gone]).tolist()) - {0}
    sizes = ndi.sum(gone, lab, range(1, n + 1))
    area = float(card.sum())
    inner = [float(s) / area for i, s in enumerate(sizes, 1) if i not in touching]
    return len(inner), [s for s in inner if s > 0.002]


WEAR_RANGES = {   # the target's age_rules.paper_wear and wear tables: (what, class -> (lo, hi))
    "corner_lifts": {"A": (0, 0), "B": (0, 1), "C": (0, 2), "D": (0, 3)},
    "tears": {"A": (0, 0), "B": (0, 1), "C": (0, 2), "D": (0, 4)},
}
LOSS_RANGES = {"A": (0.0, 0.0), "B": (0.0, 0.05), "C": (0.03, 0.20), "D": (0.30, 0.60)}


def check_item(task):
    out, iid = task
    if not _G:
        init(out)
    sc, gl, P = _G["sc"], _G["gl"], _G["P"]
    it = sc.ITEMS[iid]
    R = Rows()
    manifest = json.loads((Path(out) / "manifest.json").read_text())
    row = [r for r in manifest["items"] if r["item"] == iid][0]
    ppm = float(it["px_per_mm"])
    W, H = it["format"]["w_mm"], it["format"]["h_mm"]
    size = (int(round(W * ppm)), int(round(H * ppm)))
    t0 = time.time()
    # --- files
    problems = []
    for cls, c in row["classes"].items():
        for k in ("basecolour", "height", "orm"):
            f = Path(out) / c[k]["file"]
            if not f.exists():
                problems.append("missing " + c[k]["file"])
                continue
            im = Image.open(f)
            if im.size != size:
                problems.append("%s is %s, the target says %s" % (c[k]["file"], im.size, size))
            if k == "height" and im.mode not in ("I;16", "I"):
                problems.append("height is not 16-bit: " + im.mode)
        if not row["classes"][cls]["basecolour"]["mode"] in ("RGB", "RGBA"):
            problems.append("basecolour mode")
    if not (Path(out) / "_check" / (iid + "_A_clean.png")).exists():
        problems.append("no clean render")
    R.add(iid + ".files", not problems and row["size_px"] == list(size), "; ".join(problems) or "%dx%d px at %g px/mm, classes %s" % (size[0], size[1], ppm, " ".join(row["classes"])))
    # --- the glyph manifest
    try:
        man = json.loads((Path(out) / iid / (iid + ".glyphs.json")).read_text())["blocks"]
    except Exception as e:     # noqa: BLE001
        man = None
        R.add(iid + ".manifest", False, "unreadable: %r" % (e,))
    if man is not None:
        ok, why = sc.words_ok(it, man)
        bad = []
        for b in it["blocks"]:
            if b.get("ghost"):
                continue
            bad += sc.envelope_problems(b, man.get(b["id"], []))
        R.add(iid + ".manifest", ok and not bad, why if not ok else (bad[:2] if bad else "%d blocks, every glyph of the approved string, inside the print or hand envelope" % len(man)))
    # --- the clean class-A picture
    rgbc, alc, _, _ = load(out, "_check/%s_A_clean.png" % iid)
    ref, masks, img = read_picture(sc, P, it, rgbc, alc, "A", tape=False)
    fails = sc.all_pixel_checks(it, img, man) if man is not None else ["no manifest"]
    fails = [f for f in fails if not f.startswith(".clean")]
    R.add(iid + ".clean.read", not fails, "; ".join(fails[:3]) if fails else "every pixel check of the reader passes (%d blocks)" % len([b for b in it["blocks"] if not b.get("ghost")]))
    s_mm2, _stray = stray_mm2(sc, it, rgbc, alc, ref)
    R.add(iid + ".clean.stray", s_mm2 <= 2.0, "%.2f mm2 outside the lettering, shapes and art (limit 2)" % s_mm2)
    # paper and inks on the clean picture
    paper_ok_row(R, iid, it, P, rgbc, alc, ref, masks, "A", ppm, "clean", 5.0, 15.0)
    # --- each delivered class
    for cls in row["classes"]:
        c = row["classes"][cls]
        rgb, al, mode, _ = load(out, c["basecolour"]["file"])
        tau = 0.7 if it["wear"].get("table") == "glass_bill" else 1.0
        ref_c, masks_c, img_c = read_picture(sc, P, it, rgb, al, cls, tau, despeckle=it["process"].startswith("photocopy"))
        f2 = sc.all_pixel_checks(it, img_c, man) if man is not None else ["no manifest"]
        imprints = [b["id"] for b in it["blocks"] if b.get("role") == "imprint" and not b.get("ghost")]
        f2 = [f for f in f2 if not f.startswith(".clean") and f.split(" ")[0] not in imprints]        # the printer's imprint is illegible by design (section 14): the weather may take it
        strict = cls in ("A", "B") and iid != "K02"          # K02 (held, not placed): the target's own sucker (centre 14, 14, 22 mm) covers the B of BACK, which starts at 12 mm
        R.add("%s.%s.read" % (iid, cls), (not f2) if strict else True, ("; ".join(f2[:4]) if f2 else "every pixel check passes on the weathered picture") + ("" if strict else (" (reported: K02 is held; the target's own sucker covers the B of BACK)" if iid == "K02" else " (reported: class %s is weathered on purpose)" % cls)), reported=not strict)
        paper_ok_row(R, iid, it, P, rgb, al, ref_c, masks_c, cls, ppm, cls, 10.0, 22.0, tau)
        lost = float(((alc > 0.5) & (al < 0.5)).sum()) / max(1.0, float((alc > 0.5).sum()))      # of the card's own clean outline (a star card's corners were counted as lost)
        lo, hi = LOSS_RANGES[cls]
        table = it["wear"].get("table")
        if table in ("bill_pasted", "sticker") and not it.get("kind") == "plate":
            lim_hi = hi + 0.01
            R.add("%s.%s.loss" % (iid, cls), lost <= lim_hi and (lost >= lo - 0.02 or lo == 0), "paper lost %.3f (the target's range for class %s: %.2f to %.2f)" % (lost, cls, lo, hi))
        else:
            R.add("%s.%s.loss" % (iid, cls), lost <= 0.30, "alpha lost %.3f (a sleeve's clear band, a dog-ear or a star's outline only)" % lost)
        n_in, big = inner_losses(alc, al)
        R.add("%s.%s.holes" % (iid, cls), not big, "%d losses inside the sheet, none over 0.2 per cent of it" % n_in if not big else "%d losses do not reach the sheet's edge, the largest %.2f per cent of it (limit 0.2)" % (len(big), 100 * max(big)))
        wl = c["wear"]
        wr = []
        for k, rng_ in WEAR_RANGES.items():
            if k in wl and not (rng_[cls][0] <= wl[k] <= rng_[cls][1]):
                wr.append("%s %s outside %s" % (k, wl[k], rng_[cls]))
        R.add("%s.%s.wear" % (iid, cls), not wr, "; ".join(wr) or "wear log %s" % json.dumps(wl))
        h16c = np.asarray(Image.open(Path(out) / c["height"]["file"]))
        n_clip = int((h16c == 0).sum() + (h16c == 65535).sum())
        R.add("%s.%s.height" % (iid, cls), n_clip == 0, "no height pixel at 0 or 65535 (%g units/mm)" % c["height"]["units_per_mm"] if not n_clip else "%d height pixels clipped at 0 or 65535 (%g units/mm)" % (n_clip, c["height"]["units_per_mm"]))
        tt = wl.get("tear_tests")
        if tt is not None:            # the second street review's tests on the tear lines, logged by the maker
            bad_t = {k: v for k, v in tt.items() if k in ("turn_over_150", "few_sharp_vertices", "tongues_left") and v}
            R.add("%s.%s.tears" % (iid, cls), not bad_t, ("failing: %s" % bad_t) if bad_t else "no 40 mm of a tear line turns 150 degrees one way, every line of 60 mm has two sharp vertices, no tongue left (%d cut)" % tt.get("tongues_cut", 0))
        # the cue
        mc = it.get("mirror_cue")
        if mc and cls == list(row["classes"])[0]:
            cue_row(R, sc, it, rgb, al, masks_c, iid)
        # height and ORM
        if cls == list(row["classes"])[0]:
            maps_row(R, sc, it, out, c, iid, masks_c, ppm)
    R.rows.append(dict(id=iid + ".seconds", ok=True, detail="%.1f" % (time.time() - t0), reported=True))
    return R.rows


def paper_ok_row(R, iid, it, P, rgb, al, ref, masks, cls, ppm, tag, de_paper, de_ink, tau=1.0):
    # the paper: the median of the pixels the flat reference calls bare stock (away from everything else)
    if it["stock"]:
        sc = _G["sc"]
        stock = np.asarray(P.stock(it["stock"], cls, tau), float)
        bare = (np.abs(ref - stock.astype(np.float32)).max(-1) < 1) & (al > 0.99)
        bare = ndi.binary_erosion(bare, _G["gl"].disk(max(1, int(round(2 * ppm))))) if bare.sum() > 1000 else bare
        if bare.sum() > 100:
            med = np.median(rgb[bare], axis=0)
            dE = float(np.sqrt(((pc.lab_of(med) - pc.lab_of(stock)) ** 2).sum()))
            R.add("%s.%s.paper" % (iid, tag), dE <= de_paper, "median bare paper %s against the aged stock %s: dE %.1f (limit %g)" % (tuple(int(v) for v in med), pc.rnd(stock), dE, de_paper))
    # the inks and the contrast, per block of cap 6 mm or more
    bad_ink, bad_con, n = [], [], 0
    for b in it["blocks"]:
        if b.get("ghost") or b["cap_mm"] < 6.0:
            continue
        m = masks[b["id"]]
        ink = np.asarray(P.ink(b["ink"], it["stock"], cls, tau), float)
        med = core_median(rgb, m, ppm, ink)
        if med is None:
            continue
        n += 1
        dE = float(np.sqrt(((pc.lab_of(med) - pc.lab_of(ink)) ** 2).sum()))
        if dE > de_ink:
            bad_ink.append("%s dE %.0f" % (b["id"], dE))
        # ground: the flat reference under the lettering's own pixels (dilated), the median
        ring = ndi.binary_dilation(m, _G["gl"].disk(max(2, int(round(2 * ppm))))) & ~ndi.binary_dilation(m, _G["gl"].disk(max(1, int(round(0.8 * ppm)))))
        ring &= (al > 0.99)
        g = ref[ring] if ring.sum() > 10 else None
        if g is None:
            continue
        gmed = np.median(g, axis=0)
        measured = wcag(med, gmed)
        want = b["contrast"][cls]
        floor = 0.45 if it["wear"].get("table") == "notice_sleeve" else 0.6          # a sleeve's fog (0.1 to 0.3 white in the lower third) lowers the contrast of what is under it
        if not (floor * want <= measured <= 1.6 * want) and want > 1.5:
            bad_con.append("%s %.1f against %.1f" % (b["id"], measured, want))
    R.add("%s.%s.ink" % (iid, tag), not bad_ink, "; ".join(bad_ink[:4]) if bad_ink else "%d blocks of 6 mm cap or more: core colour within dE %g of the aged ink" % (n, de_ink))
    R.add("%s.%s.contrast" % (iid, tag), not bad_con, "; ".join(bad_con[:4]) if bad_con else "%d blocks: measured WCAG contrast within 0.6 (0.45 under a sleeve) to 1.6 of the target's for class %s" % (n, cls))


def cue_row(R, sc, it, rgb, al, masks, iid):
    """G.mirror.cues on the delivered picture, read at 2 px/mm; the mirrored picture must read RIGHT."""
    ppm = float(it["px_per_mm"])
    k = ppm / 2.0
    W, H = it["format"]["w_mm"], it["format"]["h_mm"]
    size = (int(round(W * 2)), int(round(H * 2)))
    im = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8)).resize(size, Image.BOX)
    a2 = np.asarray(Image.fromarray((al * 255).astype(np.uint8)).resize(size, Image.BOX)) > 127
    text = np.asarray(Image.fromarray((rd.union_mask(masks) * 255).astype(np.uint8)).resize(size, Image.BOX)) > 60
    rgb2 = np.asarray(im).astype(float)
    got = sc.cue_side(it, rgb2, a2, text)
    mir = sc.cue_side(it, rgb2[:, ::-1], a2[:, ::-1], text[:, ::-1])
    R.add(iid + ".cue", got == "left" and mir == "right", "the cue reads %s; the mirrored picture reads %s (G.mirror.cues: left, then right)" % (got, mir))


def maps_row(R, sc, it, out, c, iid, masks, ppm):
    h16 = np.asarray(Image.open(Path(out) / c["height"]["file"])).astype(np.float64)
    units = c["height"]["units_per_mm"]
    hmm = (h16 - 32768) / units
    orm = np.asarray(Image.open(Path(out) / c["orm"]["file"]))
    ok = (orm[..., 0] == 255).all() and 0.05 <= orm[..., 1].mean() / 255 <= 0.95 and float(np.abs(hmm).max()) <= 65535 / units
    R.add(iid + ".maps", ok, "height %.2f to %.2f mm (%g units/mm), roughness %.2f, metal %.3f" % (hmm.min(), hmm.max(), units, orm[..., 1].mean() / 255, orm[..., 2].mean() / 255))
    if it.get("relief") and it["relief"].get("raised_mm"):
        rm = rd.union_mask(masks)
        raised = it["relief"]["raised_mm"]
        if rm.sum() > 100:
            core = ndi.binary_erosion(rm, _G["gl"].disk(max(1, int(round(0.4 * ppm)))))
            hin = float(np.median(hmm[core if core.sum() > 20 else rm]))
            face = float(np.median(hmm[(~ndi.binary_dilation(rm, _G["gl"].disk(int(round(3 * ppm))))) & (hmm > -1)][::7]))
            R.add(iid + ".relief", abs((hin - face) - raised) <= 0.35 * raised, "letters stand %.2f mm above the face (the target: %.1f mm raised)" % (hin - face, raised))


# ---------------------------------------------------------------------------------------------- controls
def control_item(task):
    out, iid = task
    if not _G:
        init(out)
    sc, gl, P = _G["sc"], _G["gl"], _G["P"]
    it = sc.ITEMS[iid]
    R = Rows()
    ppm = float(it["px_per_mm"])
    H = it["format"]["h_mm"]
    man = json.loads((Path(out) / iid / (iid + ".glyphs.json")).read_text())["blocks"]
    rgb, al, _, _ = load(out, "_check/%s_A_clean.png" % iid)
    ref, masks, img = read_picture(sc, P, it, rgb, al, "A", tape=False)
    big = max([b for b in it["blocks"] if b.get("glyph_check") and not b.get("ghost")], key=lambda b: b["cap_mm"])

    def fails_of(mask):
        return [f for f in sc.all_pixel_checks(it, mask, man) if not f.startswith(".clean")]
    # mirrored
    f = fails_of(img[:, ::-1])
    R.add("control.%s.mirror" % iid, bool(f), "mirrored picture fails: %s" % (f[:2],))
    # shifted 6 mm
    f = fails_of(np.roll(img, int(round(6 * ppm)), axis=1))
    R.add("control.%s.shift" % iid, bool(f), "picture shifted 6 mm fails: %s" % (f[:2],))
    # a tilt of 1.2 degrees
    im = Image.fromarray((img * 255).astype(np.uint8)).rotate(1.2, resample=Image.BILINEAR)
    sq = sc.square_estimate(it, np.asarray(im) > 127, man)
    R.add("control.%s.tilt" % iid, abs(sq["angle"]) > sc.SQUARE_TOL_DEG, "a picture turned 1.2 degrees is found turned %.2f degrees (limit %.1f)" % (sq["angle"], sc.SQUARE_TOL_DEG))
    # a wrong glyph (drawn in the picture, the manifest unchanged)
    ink_col = np.asarray(P.ink(big["ink"], it["stock"], "A"), np.float32)
    gl_list = man[big["id"]]
    cands = [i for i, g in enumerate(gl_list) if g["ch"] not in " .,'’-" and g["ch"].isalnum()]
    if cands:
        j = cands[len(cands) // 2]
        g = gl_list[j]
        pool = "0123456789" if g["ch"].isdigit() else "ABCDEFGHIJKLMNOPRSTUVWXYZ" if g["ch"].isupper() else "abcdefghijklmnoprstuvwxyz"
        new = [c for c in pool if c != g["ch"]]
        new_ch = new[(ord(g["ch"]) * 7) % len(new)]
        r2 = rgb.copy()
        h_, w_ = r2.shape[:2]
        win = (0, w_, 0, h_)
        pa, ox, base = sc.glyph_patch_cached(g["font"], g["weight"], g["ch"], g["em_mm"], ppm, g["rot_deg"], g["emb_mm"])
        cv = np.zeros((h_, w_), bool)
        gl.paste_or(cv, pa, ox, base, g["ox_mm"] * ppm, (H - g["baseline_mm"]) * ppm)
        cv = ndi.binary_dilation(cv, gl.disk(1))
        r2[cv] = ref[cv]
        import paper_ink
        pb, oxb, baseb = paper_ink.glyph_patch(sc, dict(g, ch=new_ch), ppm)
        cv2 = np.zeros((h_, w_), bool)
        gl.paste_or(cv2, pb, oxb, baseb, g["ox_mm"] * ppm, (H - g["baseline_mm"]) * ppm)
        r2[cv2] = ink_col
        _, _, img2 = read_picture(sc, P, it, r2, al, "A", tape=False)
        f = fails_of(img2)
        R.add("control.%s.glyph" % iid, bool(f), "%r drawn as %r in %s fails: %s" % (g["ch"], new_ch, big["id"], [x[:60] for x in f[:2]]))
    # stray ink: a 30 x 6 mm bar of the block's ink somewhere bare
    stray_pos = None
    allowed = np.zeros(rgb.shape[:2], bool)
    for b in it["blocks"]:
        if b.get("ghost"):
            continue
        x0, x1, y0, y1 = sc.glyph_window(it, b, rgb.shape[:2], ppm)
        allowed[y0:y1, x0:x1] = True
    bw, bh = int(30 * ppm), int(6 * ppm)
    for y in range(int(2 * ppm), rgb.shape[0] - bh - int(2 * ppm), max(1, int(8 * ppm))):
        for x in range(int(2 * ppm), rgb.shape[1] - bw - int(2 * ppm), max(1, int(15 * ppm))):
            if allowed[y - int(2 * ppm):y + bh + int(2 * ppm), x - int(2 * ppm):x + bw + int(2 * ppm)].any():
                continue
            reg = ref[y:y + bh, x:x + bw]
            if np.abs(reg - reg[0, 0]).max() < 1 and np.abs(ref[y - 3:y + bh + 3, x - 3:x + bw + 3] - reg[0, 0]).max() < 1 and not it["art"] and np.abs(reg[0, 0] - ink_col).max() > 40:
                stray_pos = (y, x)
                break
        if stray_pos:
            break
    if stray_pos:
        r3 = rgb.copy()
        y, x = stray_pos
        r3[y:y + bh, x:x + bw] = ink_col
        s_mm2, _ = stray_mm2(sc, it, r3, al, ref)
        R.add("control.%s.stray" % iid, s_mm2 > 2.0, "a 30 x 6 mm bar of ink on a bare margin reads %.0f mm2 (limit 2)" % s_mm2)
    # a wrong colour: the whole picture cast toward blue
    r4 = np.clip(rgb + np.asarray([-8, 0, 24], np.float32), 0, 255)
    if it["stock"]:
        stock = np.asarray(P.stock(it["stock"], "A"), float)
        bare = (np.abs(ref - stock.astype(np.float32)).max(-1) < 1)
        if bare.sum() > 100:                                  # a picture that is all art or paint has no bare paper to read
            med = np.median(r4[bare], axis=0)
            dE = float(np.sqrt(((pc.lab_of(med) - pc.lab_of(stock)) ** 2).sum()))
            R.add("control.%s.cast" % iid, dE > 5.0, "a blue cast on the paper reads dE %.1f from the aged stock (limit 5)" % dE)
    return R.rows


# ---------------------------------------------------------------------------------------------- seeded false-failure runs
def seed_item(task):
    out, iid, seed = task
    if not _G:
        init(out)
    sc, gl, P = _G["sc"], _G["gl"], _G["P"]
    import paper_ink, paper_render
    it = sc.ITEMS[iid]
    geo = paper_ink.build(sc, gl, P, it, seed)
    r = paper_render.render(P, geo, "A", seed, wear=False)
    rgb, a = paper_render.to_rgba8(r)
    rgbf, alf = rgb.astype(np.float32), a.astype(np.float32) / 255.0
    ref, masks, img = read_picture(sc, P, it, rgbf, alf, "A", tape=False)
    man = {bid: [dict(g) for g in gs] for bid, gs in geo.man.items()}
    fails = [f for f in sc.all_pixel_checks(it, img, man) if not f.startswith(".clean")]
    s_mm2, _ = stray_mm2(sc, it, rgbf, alf, ref)
    if s_mm2 > 2.0:
        fails.append("stray %.1f mm2" % s_mm2)
    # the worn B render of the same seed: classes A and B must read too
    r2 = paper_render.render(P, geo, "B", seed, wear=True)
    rgb2, a2 = paper_render.to_rgba8(r2)
    ref2, masks2, img2 = read_picture(sc, P, it, rgb2.astype(np.float32), a2.astype(np.float32) / 255.0, "B", 0.7 if it["wear"].get("table") == "glass_bill" else 1.0, despeckle=it["process"].startswith("photocopy"))
    imprints = [b["id"] for b in it["blocks"] if b.get("role") == "imprint" and not b.get("ghost")]
    f2 = [f for f in sc.all_pixel_checks(it, img2, man) if not f.startswith(".clean") and f.split(" ")[0] not in imprints]
    return dict(item=iid, seed=seed, clean_fails=fails, worn_fails=f2)


def safe(fn):
    """A per-item task that cannot vanish: an error becomes a failing row naming it (the sixth and seventh builds' checks lost a third of their items without a word)."""
    def run(task):
        try:
            return fn(task)
        except BaseException as e:     # noqa: BLE001
            import traceback
            iid = task[1]
            return [dict(id="%s.error" % iid, ok=False, detail="%s: %s" % (type(e).__name__, traceback.format_exc()[-400:]), reported=False)]
    run.__name__ = fn.__name__
    return run


def check_item_safe(task):
    return safe(check_item)(task)


def control_item_safe(task):
    return safe(control_item)(task)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--only", default="")
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--seeds", type=int, default=0)
    ap.add_argument("--no-controls", action="store_true")
    ap.add_argument("--write", default="")
    a = ap.parse_args()
    out = Path(a.out)
    init(out)
    sc = _G["sc"]
    manifest = json.loads((out / "manifest.json").read_text())
    ids = [r["item"] for r in manifest["items"]]
    print("manifest: %d items" % len(ids), flush=True)
    if a.only:
        ids = [i for i in ids if i in [s.strip() for s in a.only.split(",")]]
    t0 = time.time()
    rows = []
    with Pool(a.jobs, initializer=init, initargs=(str(out),)) as p:
        for r in p.imap_unordered(check_item_safe, [(str(out), i) for i in ids]):
            rows += r
            bad = [x for x in r if not x["ok"]]
            print("%-10s %2d rows, %d failing" % (r[0]["id"].split(".")[0], len(r), len(bad)), flush=True)
            for x in bad:
                print("    FAIL", x["id"], x["detail"][:160], flush=True)
        controls = []
        if not a.no_controls:
            for r in p.imap_unordered(control_item_safe, [(str(out), i) for i in ids]):
                controls += r
        seeds = []
        if a.seeds:
            tasks = []
            for i in ids:
                it = sc.ITEMS[i]
                hand = any(b.get("hand") for b in it["blocks"])
                reg = it["process"] in ("screen_2col", "letterpress_2col", "litho_2col")
                n = a.seeds if hand else (max(2, a.seeds // 2) if reg else 1)
                tasks += [(str(out), i, s) for s in range(2, 2 + n)]
            for r in p.imap_unordered(seed_item, tasks):
                seeds.append(r)
    seen = {r["id"].split(".")[0] for r in rows}
    missing = [i for i in ids if i not in seen]
    rows.append(dict(id="check.items", ok=not missing, detail=("every one of the %d items in the manifest has its rows" % len(ids)) if not missing else "%d of %d items have no rows: %s" % (len(missing), len(ids), ", ".join(missing)), reported=False))
    print("items checked: %d of %d in the manifest" % (len(seen), len(ids)), flush=True)
    nbad = [r for r in rows if not r["ok"]]
    cbad = [r for r in controls if not r["ok"]]
    sbad = [s for s in seeds if s["clean_fails"] or s["worn_fails"]]
    print("rows: %d, failing %d; controls: %d, not caught %d; seeded runs: %d, failing %d (%.0f s)" % (len(rows), len(nbad), len(controls), len(cbad), len(seeds), len(sbad), time.time() - t0))
    for r in cbad:
        print("  NOT CAUGHT", r["id"], r["detail"][:160])
    for s in sbad[:40]:
        print("  SEED FAIL", s["item"], s["seed"], s["clean_fails"][:2], s["worn_fails"][:2])
    if a.write:
        res = dict(rows=rows, controls=controls, seeds=seeds, made=time.strftime("%Y-%m-%d %H:%M:%S"), summary=dict(rows=len(rows), failing=len(nbad), controls=len(controls), controls_not_caught=len(cbad), seeded_runs=len(seeds), seeded_failing=len(sbad)))
        Path(a.write).parent.mkdir(parents=True, exist_ok=True)
        Path(a.write).write_text(json.dumps(res, indent=1), encoding="utf-8")
    return 1 if (nbad or cbad) else 0


if __name__ == "__main__":
    sys.exit(main())
