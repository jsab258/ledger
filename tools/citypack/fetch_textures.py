#!/usr/bin/env python3
"""Fetch a CC0 texture set for the surfaces `AssetLibrary` already asks for.

M17.6. The completeness audit on 2026-07-31 found zero image files in the
project: every surface in the game is a small tiling noise pattern generated at
runtime. `AssetLibrary` has resolved a real pack from
`StreamingAssets/CityPack` since it was written, with a procedural fallback, so
**a pack drops in with no code change** — the hook was built months ago and
nothing was ever put in it.

WHY THIS IS A CI JOB AND NOT A SCRIPT I RUN HERE. Every asset host is blocked
from the dev container, exactly like HuggingFace:

    ambientcg.com   000    api.polyhaven.com  000
    cc0textures.com 000    fonts.google.com   000

So this has the same shape as the voice pipeline, and it inherits that
pipeline's most expensive lesson. Fifteen CI runs went into guessing at a corpus
because I had no way to ASK it anything; the day was fixed by building an
`--inventory` mode that answered every question at once and cost one run.

    python3 tools/citypack/fetch_textures.py --inventory   # ask, decide later
    python3 tools/citypack/fetch_textures.py --fetch       # take the decisions

`--inventory` reads the catalogue and writes `tools/citypack/candidates.json`
without downloading a single image. Then the choice is made HERE, locally, in
seconds, from evidence — and `--fetch` takes named assets rather than sweeping.

QUEUE 300, 2026-09-15: THE SAME SHAPE ONE LEVEL FURTHER IN. `--inventory`
answers "what exists"; it cannot answer "which one looks right", because the
catalogue carries an id and a size list and nothing else — no tag, no
preview. Four of the first twelve surfaces turned out to be near-flat cards
picked blind on category and stable id. `--shortlist` downloads several named
CANDIDATES per surface at 1K, measures each on queue 300's three numbers
beside the surface's current file, and writes a contact sheet — so THAT
choice is also made locally, from evidence, instead of from a name:

    python3 tools/citypack/fetch_textures.py --shortlist      # see candidates
    python3 tools/citypack/fetch_textures.py --measure-pack   # print the
                                                                # current series
    python3 tools/citypack/fetch_textures.py --selftest       # no network

DESTRUCTIVE OPERATIONS ARE SCOPED TO WHAT THIS RUN PRODUCED. A CI job on this
project once deleted 24 clips Jafar had already listened to and reported
success. Nothing here removes a file it did not just write, and a run that fills
none of its targets exits non-zero — the voice pipeline's invariant 7, which was
open for a day because a `--who` run that banked nothing still saw everybody
else's clips on disk and called itself green.
"""
import argparse
import io
import json
import os
import pathlib
import sys
import urllib.parse
import urllib.request
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
PACK = ROOT / "ledger" / "Assets" / "StreamingAssets" / "CityPack"
HERE = pathlib.Path(__file__).resolve().parent

API = "https://ambientcg.com/api/v2/full_json"

# The twelve logical surfaces the pack OWES `AssetLibrary`, and what each one
# is in the language of a texture library. Search terms rather than asset ids
# on purpose: an id I typed from memory is an id that is wrong, and the whole
# point of the inventory pass is that the catalogue tells us what exists.
# (`AssetLibrary` declares more names than these: `interior` and
# `paint_yellow` are painted from the tint and want no pack file at all, and
# `setts` is optional until a pick lands, see `OPTIONAL_SURFACES` below.)
SURFACES = {
    "asphalt":    ["Asphalt"],
    "sidewalk":   ["PavingStones", "Concrete"],
    "kerb":       ["Concrete", "Rock"],
    "brick_red":  ["Bricks"],
    "brick_grey": ["Bricks", "Concrete"],
    "plaster":    ["Plaster"],
    "concrete":   ["Concrete"],
    "wood":       ["Planks", "Wood"],
    "roof":       ["RoofingTiles"],
    "metal":      ["Metal"],
    "glass":      ["Glass", "Metal"],
    "window":     ["Glass", "Metal"],
    # VARIANTS (18 Aug). A second photograph for each surface that fills a
    # street view, so 376 buildings stop wearing one brick. The logical name
    # is `<surface>_b`, which `AssetLibrary` resolves as an alternate rather
    # than as a new kind of thing — nothing in the world asks for "brick_red_b"
    # by name.
    "brick_red_b":  ["Bricks"],
    "brick_grey_b": ["Bricks", "Concrete"],
    "plaster_b":    ["Plaster"],
    "roof_b":       ["RoofingTiles"],
    "concrete_b":   ["Concrete"],
}

# A SURFACE THE PACK MAY HOLD AND IS NOT REQUIRED TO, WHICH IS A DIFFERENT
# CONTRACT FROM THE LIST ABOVE AND THEREFORE A DIFFERENT LIST.
#
# Every name in `SURFACES` is one `validate()` demands a choice for, and
# `fetch()` refuses to start on a failed validate, so putting a surface
# nobody has picked yet up there would stop the whole download for eleven
# surfaces that are fine. Leaving it out altogether is the other failure and
# the quieter one: `fetch()` filters `choices.json` by membership, so a pick
# committed under a name this file does not know is dropped without a word
# and the pack comes back exactly as it went in.
#
# So: known enough to be fetched, not required to be chosen.
#
# `setts` is the first entry. The logical name and the category are COPIED
# from `shortlist-candidates.json`, which already shortlists `PavingStones`
# ids under that name, rather than chosen again here; the constant the world
# asks for is `AssetLibrary.Setts` and the three names have to be the same
# string or the file lands where nothing looks for it.
#
# HOW MANY IDS THAT LIST HOLDS IS DELIBERATELY NOT REPEATED HERE, 2026-09-21.
# This comment said 148 until today, when the list grew to a different number
# because the filter that built it could not match a letter suffix; a count
# copied out of another file goes stale the moment that file moves, which is
# the same fault as the pinned pack constants `selftest()` was rebuilt to
# stop carrying. Read the list if you need the number.
OPTIONAL_SURFACES = {
    "setts": ["PavingStones"],
}

# EVERYTHING THE PACK CAN HOLD, required and optional together, for the three
# places that ask "is this a surface at all" rather than "is this surface
# owed": the fetch's membership filter, the inventory's search terms, and
# `--measure-pack`'s default list.
FETCHABLE = dict(SURFACES, **OPTIONAL_SURFACES)

# The DEFAULT when choices.json is silent; the committed choices carry the
# real decision. The pack started at 1K on the argument that fog and palette
# do the heavy lifting; RE-DECIDED 16 Aug ("best possible result, all
# aspects") — the target machine is an M5 with memory to spare, the camera
# walks right up to walls, and 2K is where brick stops smearing at arm's
# length. Twelve surfaces at 2K JPG is ~40MB, noise for a desktop game.
RESOLUTION = "1K-JPG"


def get(url, timeout=60):
    req = urllib.request.Request(url, headers={"User-Agent": "ledger-citypack/1"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def dig(node, *keys):
    """Walk nested dicts without assuming a shape.

    `d.get("k", {})` returns NONE, not `{}`, when the key is present with a
    null value — so the obvious chain of `.get(...)` calls raises
    AttributeError on the first asset whose `downloadFolders` is null. The
    catalogue run died on exactly that and wrote no file at all, which meant a
    five-minute run produced nothing to read: no catalogue, no candidate list,
    and an artefact upload with nothing to upload.

    The per-term inventory has the same chain and survived only because the
    query-filtered results happened not to contain a null."""
    for k in keys:
        if not isinstance(node, dict):
            return None
        node = node.get(k)
    return node


def sizes_of(asset):
    """Which download sizes this asset publishes. Empty when it publishes none,
    which is a fact about the asset rather than an error."""
    zips = dig(asset, "downloadFolders", "default",
               "downloadFiletypeCategories", "zip", "downloads")
    if not isinstance(zips, list):
        return []
    return sorted({z.get("attribute") for z in zips
                   if isinstance(z, dict) and z.get("attribute")})


def link_for(asset, resolution):
    zips = dig(asset, "downloadFolders", "default",
               "downloadFiletypeCategories", "zip", "downloads")
    if not isinstance(zips, list):
        return None
    for z in zips:
        if isinstance(z, dict) and z.get("attribute") == resolution:
            return z.get("downloadLink")
    return None


def extract_maps(blob):
    """Colour, NormalGL and Roughness bytes from a downloaded zip, plus the
    colour entry's name. Factored out of `fetch()` on 2026-09-15 (queue 300)
    so `--fetch` and `--shortlist` read a zip exactly the same way and can
    never quietly disagree about which file inside it is the colour map.

    NAMED, NOT `next()`. A bare `next()` raises StopIteration with an EMPTY
    message, which is how twelve identical failures once reached the log
    saying only "StopIteration:" and cost a CI round trip to identify. If no
    colour map is in there, ValueError carries what WAS in the zip instead."""
    with zipfile.ZipFile(io.BytesIO(blob)) as z:
        inside = z.namelist()
        name = norm_name = rough_name = None
        for n in inside:
            low = n.lower()
            if not low.endswith((".jpg", ".png")):
                continue
            if "color" in low and name is None:
                name = n
            # NormalGL, not NormalDX: Unity's tangent space is OpenGL-handed
            # (green up). The DX map inverts green and would emboss every
            # mortar line outward.
            if "normalgl" in low and norm_name is None:
                norm_name = n
            if "roughness" in low and rough_name is None:
                rough_name = n
        if name is None:
            raise ValueError("no colour map among " + ", ".join(inside[:8]))
        img = z.read(name)
        norm = z.read(norm_name) if norm_name else None
        rough = z.read(rough_name) if rough_name else None
    return img, norm, rough, name


# Rec. 709 luma on sRGB bytes, UNLINEARIZED: this is what "measured over
# every texel, sRGB bytes" in production/queue/300 means, the JPEG's own
# decoded bytes, no gamma step.
#
# CALIBRATED 2026-09-15 AGAINST THE PRE-SWAP PACK, and that pack is HISTORY,
# not a description of the files on disk now. Three candidate luma formulas
# (Rec. 601, Rec. 709, plain average) were run over the then-committed files
# and Rec. 709 was the only one that reproduced all five of the numbers queue
# 300 had published: plaster 211.7/5.8/7.2, kerb 184.3/6.6/0.0, metal
# 134.8/4.6/22.5, concrete 107.2/9.3/6.8, roof_b 49.0/4.4/5.0. The other two
# were off by up to 1.5 on plaster and metal, and would silently compare a
# shortlist candidate against a different ruler than the one queue 300 was
# written against.
#
# FOUR OF THOSE FIVE SURFACES WERE REPLACED LATER THE SAME DAY by the
# shortlist picks in choices.json (kerb, metal, concrete, plaster), so four
# of the five numbers above no longer describe anything: run --measure-pack
# for what the pack reads today. Only roof_b 49.0/4.4/5.0, which was never
# swapped, still reproduces exactly, re-measured 2026-09-21.
#
# Do not change this tuple without re-running that check. --selftest now pins
# THE TUPLE rather than the pack: solid red, green and blue print lumMean
# 54.2/182.4/18.4 under Rec. 709, a triple neither Rec. 601 (76.2/149.7/29.1)
# nor a plain average (85.0/85.0/85.0) can produce.
LUMA_R, LUMA_G, LUMA_B = 0.2126, 0.7152, 0.0722


def measure_texel_stats(image_bytes):
    """lumMean, lumSD and chromaSpread, exactly as queue 300 defines them:
    lumSD is a standard deviation OVER THE FILE, not a peak; chromaSpread is
    the MEAN OF (max channel minus min channel) PER TEXEL; both over every
    texel, sRGB bytes. Needs Pillow and numpy, which `--catalogue`,
    `--inventory`, `--validate` and `--fetch` do not — imported here, not at
    module level, so a missing package cannot break any of those four."""
    import numpy as np
    from PIL import Image
    im = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    a = np.asarray(im).astype(np.float64)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    lum = LUMA_R * r + LUMA_G * g + LUMA_B * b
    chroma = a.max(axis=-1) - a.min(axis=-1)
    return {
        "width": im.size[0],
        "height": im.size[1],
        "lumMean": round(float(lum.mean()), 1),
        "lumSD": round(float(lum.std()), 1),
        "chromaSpread": round(float(chroma.mean()), 1),
    }


def measure_pack_file(logical):
    """The CURRENT committed pack's stats for one logical surface, read from
    disk exactly where `AssetLibrary` looks (`.jpg` then `.png`). None when
    the pack has no file under that name — a fact, not an error."""
    for ext in (".jpg", ".png"):
        p = PACK / "textures" / (logical + ext)
        if p.exists():
            stats = measure_texel_stats(p.read_bytes())
            stats["file"] = p.name
            return stats
    return None


def catalogue():
    """THE WHOLE CATALOGUE, ONCE. Every material id and the sizes it publishes.

    The first inventory run was already the right idea and it was still too
    narrow: it asked eleven search terms, and two of them — `PavingStones` and
    `RoofingTiles` — came back with ZERO assets. Sidewalk and roof would have
    silently had no texture, which is precisely the class of surprise a blind
    fetch produces and the reason the voice pipeline burned fifteen runs.

    Guessing a better search term is the same mistake one notch smaller. So:
    pull the entire material list once, write it down, and every question after
    that — what is paving called here, is there a roof at all, which brick — is
    answered locally in seconds with no run at all.

    Metadata only. No image is downloaded."""
    out, offset, limit, note = [], 0, 200, "complete"
    seen = set()
    print("catalogue — every material, metadata only\n")
    try:
        while offset < 4000:
            url = (API + f"?type=Material&limit={limit}&offset={offset}"
                   + "&include=downloadData")
            try:
                data = json.loads(get(url))
            except Exception as e:                               # noqa: BLE001
                note = f"stopped at offset {offset}: {type(e).__name__}: {e}"
                print("  " + note)
                break
            assets = data.get("foundAssets") if isinstance(data, dict) else None
            if not assets:
                note = f"catalogue ended at offset {offset}"
                break
            fresh = 0
            for a in assets:
                aid = a.get("assetId") if isinstance(a, dict) else None
                if not aid or aid in seen:
                    continue
                seen.add(aid)
                fresh += 1
                # AND THE DOWNLOAD LINK, so a later fetch never has to ask a
                # second endpoint what this asset's zip is called. Recording it
                # here is what turns `--fetch` into twelve downloads from
                # committed data instead of twelve queries that can lie.
                out.append({"id": aid, "sizes": sizes_of(a),
                            "link": link_for(a, RESOLUTION)})
            print(f"  offset {offset:5d}  +{len(assets)} ({fresh} new) -> {len(out)} total")
            # AN API THAT IGNORES `offset` WOULD LOOP FOREVER returning the same
            # page. Nothing new means stop, whatever the page length says.
            if fresh == 0 or len(assets) < limit:
                note = ("offset appears to be ignored — the same page came back"
                        if fresh == 0 else "complete")
                break
            offset += limit
    except Exception as e:                                       # noqa: BLE001
        # WRITE WHAT WE HAVE REGARDLESS. The first attempt died on an
        # AttributeError mid-walk and produced no file at all, so a five-minute
        # run left nothing to read. A partial catalogue is worth having; an
        # exception that eats the evidence is not.
        note = f"aborted: {type(e).__name__}: {e}"
        print("  " + note)

    path = HERE / "catalogue.json"
    path.write_text(json.dumps({"resolution": RESOLUTION, "note": note,
                                "assets": out}, indent=1), encoding="utf-8")
    usable = sum(1 for a in out if RESOLUTION in a["sizes"])
    print(f"\n{len(out)} material(s), {usable} publish {RESOLUTION}")
    print(f"wrote {path.relative_to(ROOT)}")
    if usable == 0:
        print("NOTHING USABLE — the catalogue answered and had nothing at this "
              "resolution. A finding, not a pass.")
        return 1
    return 0


def inventory():
    """Per-term search. SUPERSEDED BY `--catalogue`, AND NOT TO BE TRUSTED.

    This asks `q=<term>`, and that endpoint has now been wrong three times: zero
    `PavingStones` against 162 in the catalogue, zero `RoofingTiles` against 31,
    and then twelve exact-id lookups that matched nothing at all. `--catalogue`
    answers the same questions from the list endpoint, which has never been
    wrong here, and `choices.json` is made from that.

    It stays because a search that disagrees with the catalogue is itself worth
    seeing, and it is cheap. But `candidates.json` is a record of what the
    search SAID, not of what the library HOLDS, and the file says so."""
    wanted = sorted({t for terms in FETCHABLE.values() for t in terms})
    out = {"resolution": RESOLUTION,
           "_": "WHAT THE SEARCH ENDPOINT SAID, which has disagreed with the "
                "library three times. catalogue.json is the evidence; this is "
                "a second opinion from a witness with a record.",
           "terms": {}}
    print(f"inventory — {len(wanted)} category term(s), metadata only")
    print("NOTE: the q= endpoint has been wrong three times; "
          "catalogue.json is the source of truth\n")
    for term in wanted:
        url = (API + "?type=Material&limit=60&include=downloadData"
               + "&q=" + urllib.parse.quote(term))
        try:
            data = json.loads(get(url))
        except Exception as e:                                   # noqa: BLE001
            print(f"  {term:<16} FAILED: {type(e).__name__}: {e}")
            out["terms"][term] = {"error": f"{type(e).__name__}: {e}"}
            continue
        assets = data.get("foundAssets", [])
        rows = []
        for a in assets:
            aid = a.get("assetId")
            if not aid:
                continue
            # Only entries that actually publish the size we want, so the fetch
            # step cannot pick something it then cannot download.
            has = sizes_of(a)
            rows.append({"id": aid, "sizes": has,
                         "hasWanted": RESOLUTION in has})
        rows.sort(key=lambda r: (not r["hasWanted"], r["id"]))
        out["terms"][term] = {"count": len(rows), "assets": rows[:40]}
        usable = sum(1 for r in rows if r["hasWanted"])
        print(f"  {term:<16} {len(rows):3d} asset(s), {usable:3d} publish {RESOLUTION}")
        for r in rows[:5]:
            print(f"      {r['id']}")

    path = HERE / "candidates.json"
    path.write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"\nwrote {path.relative_to(ROOT)}")
    # AN INVENTORY THAT FOUND NOTHING IS A FAILED RUN, not an empty one. The
    # voice pipeline shipped a green run that had produced zero clips because
    # the verdict only looked at a total that included everybody else's.
    usable = sum(1 for t in out["terms"].values()
                 for a in t.get("assets", []) if a.get("hasWanted"))
    if usable == 0:
        print("NOTHING USABLE FOUND — the catalogue answered, and it had nothing "
              "at this resolution. That is a finding, not a pass.")
        return 1
    return 0


def links_for(ids, resolution=None):
    """Download links for exactly these asset ids, from the LIST endpoint.

    THE SEARCH ENDPOINT LIED FOR THE THIRD TIME. `--fetch` used to resolve each
    choice with `?q=<assetId>` and take the entry whose `assetId` matched. Every
    one of the twelve raised a bare `StopIteration` — no match in the results —
    in six seconds flat, so the queries answered promptly and answered with the
    wrong thing. The same endpoint had already reported zero `PavingStones` when
    the catalogue held 162, and zero `RoofingTiles` against 31.

    Twice is a coincidence; three times is a rule. Nothing in the fetch path
    asks `q=` any more.

    The list endpoint — `type=Material&limit&offset&include=downloadData`, with
    no query — is the call that produced all 2,005 materials, so it is the one
    that gets used. It costs about eleven pages, which is a minute of a job that
    already budgets thirty.

    AND IT SAYS WHAT IT DID NOT FIND. A bare `StopIteration` with no message is
    why the first failure needed a CI log dug out of a truncated window to
    diagnose at all."""
    want, found = set(ids), {}
    res = resolution or RESOLUTION
    offset, limit = 0, 200
    print(f"  resolving {len(want)} link(s) from the list endpoint")
    while offset < 4000 and len(found) < len(want):
        url = (API + f"?type=Material&limit={limit}&offset={offset}"
               + "&include=downloadData")
        try:
            data = json.loads(get(url))
        except Exception as e:                                   # noqa: BLE001
            print(f"    offset {offset}: {type(e).__name__}: {e} — stopping")
            break
        assets = data.get("foundAssets") if isinstance(data, dict) else None
        if not assets:
            break
        for a in assets:
            aid = a.get("assetId") if isinstance(a, dict) else None
            if aid in want and aid not in found:
                link = link_for(a, res)
                if link:
                    found[aid] = link
        offset += limit
        if len(assets) < limit:
            break
    print(f"    {len(found)}/{len(want)} resolved")
    for aid in sorted(want - set(found)):
        print(f"    NOT FOUND in the list endpoint: {aid}")
    return found


def load_choices():
    """The decisions, made locally from `candidates.json`, committed as data."""
    path = HERE / "choices.json"
    if not path.exists():
        print(f"no {path.relative_to(ROOT)} — run --inventory first, then choose")
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def validate():
    """Every chosen id exists and publishes the wanted size — checked against
    the committed catalogue, with no network at all.

    This is the whole payoff of pulling the catalogue once. A typo in
    `choices.json` used to be discoverable only by spending a CI run and
    reading which surface came back empty; now it is a local command that takes
    a second, and the fetch refuses to start without it."""
    choices = load_choices()
    if choices is None:
        return 1
    path = HERE / "catalogue.json"
    if not path.exists():
        print("no catalogue.json — run --catalogue first; skipping validation")
        return 0
    cat = {a["id"]: a.get("sizes", [])
           for a in json.loads(path.read_text(encoding="utf-8")).get("assets", [])}
    want = choices.get("resolution", RESOLUTION)
    chosen = choices.get("surfaces", {})
    bad, bad_names = [], set()
    for surface, aid in sorted(chosen.items()):
        # A CHOICE UNDER A NAME NO LIST KNOWS IS THE SILENT ONE, and it is the
        # failure this whole optional/required split exists around: `fetch()`
        # filters by membership, so `cobbles` or `setts_01` in this file would
        # download nothing, fail nothing, and leave the pack exactly as it was.
        # Caught here instead, where it costs a second.
        if surface not in FETCHABLE:
            bad.append(f"{surface}: no list here knows that name, so --fetch "
                       "would drop it without a word")
            bad_names.add(surface)
        elif aid not in cat:
            bad.append(f"{surface}: {aid} is not in the catalogue")
            bad_names.add(surface)
        elif want not in cat[aid]:
            bad.append(f"{surface}: {aid} does not publish {want} ({cat[aid]})")
            bad_names.add(surface)
        else:
            print(f"  ok  {surface:<12} {aid}")
    for b in bad:
        print("  FAIL " + b)
    missing = [s for s in SURFACES if s not in chosen]
    if missing:
        bad.append("no choice for: " + ", ".join(missing))
        print("  FAIL no choice for: " + ", ".join(missing))
    # THE OPTIONAL HALF, PRINTED WITH ITS OWN DENOMINATOR. Absence here is not
    # a failure, and saying nothing about it is how "nobody has picked one
    # yet" and "the pick landed under a name this file does not know" come to
    # read the same on a green run.
    for s in sorted(OPTIONAL_SURFACES):
        if s not in chosen:
            print(f"  --  {s:<12} optional, no choice in choices.json yet")
    ok_required = sum(1 for s in SURFACES if s in chosen and s not in bad_names)
    ok_optional = sum(1 for s in OPTIONAL_SURFACES
                      if s in chosen and s not in bad_names)
    # COUNTED OVER THE LIST EACH NUMBER BELONGS TO. This line used to divide
    # every chosen surface by the required list, so one optional pick would
    # have printed 18/17.
    print(f"{ok_required}/{len(SURFACES)} required surface(s) chosen, existing, "
          "and available at the wanted size")
    print(f"{ok_optional}/{len(OPTIONAL_SURFACES)} optional surface(s) chosen")
    return 1 if bad else 0


def _ambientcg_attribution(asset_id, resolution):
    """The four facts every ambientCG download owes a record: id, source,
    licence and the page to verify them on. QUEUE 300 (2026-09-15): one
    implementation, so `fetch()` and `shortlist()` can never quietly
    disagree about what an ambientCG credit says, the same reasoning
    `extract_maps` above was factored out for."""
    return {
        "assetId": asset_id,
        "source": "ambientCG",
        "licence": "CC0 1.0 Universal",
        "url": f"https://ambientcg.com/view?id={asset_id}",
        "resolution": resolution,
    }


def fetch():
    choices = load_choices()
    if choices is None:
        return 1
    # REFUSE TO START ON A BAD LIST. A typo here costs a CI run and comes back
    # as a surface that silently did not arrive, which is the failure mode the
    # catalogue exists to remove.
    if validate() != 0:
        print("choices.json does not validate — not fetching anything")
        return 1
    textures = PACK / "textures"
    materials = PACK / "materials"
    textures.mkdir(parents=True, exist_ok=True)
    materials.mkdir(parents=True, exist_ok=True)

    wanted = {logical: aid
              for logical, aid in sorted(choices.get("surfaces", {}).items())
              if logical in FETCHABLE}

    # THE LINKS FIRST, ALL OF THEM, BEFORE ANY DOWNLOAD. A catalogue pulled
    # after this change already carries `link` per asset, in which case this
    # costs nothing; the committed one predates it, so the list endpoint fills
    # the gap. Either way the fetch loop below only ever downloads a URL the
    # library itself handed over.
    #
    # ONLY IF THE LINK IS AT THE WANTED RESOLUTION. The committed catalogue's
    # links are the 1K zips it was pulled at, and a resolution bump in
    # choices.json would otherwise download 1K and LABEL it 2K in the
    # attribution — a quietly-wrong answer, the exact class this file's
    # header warns about. The zip filename carries the size, so the check is
    # a substring; a mismatch just falls through to the list endpoint.
    want_res = choices.get("resolution", RESOLUTION)
    cat_path = HERE / "catalogue.json"
    links = {}
    if cat_path.exists():
        for a in json.loads(cat_path.read_text(encoding="utf-8")).get("assets", []):
            if (a.get("id") in set(wanted.values()) and a.get("link")
                    and want_res in a["link"]):
                links[a["id"]] = a["link"]
        if links:
            print(f"  {len(links)} link(s) came from the committed catalogue")
    unresolved = set(wanted.values()) - set(links)
    if unresolved:
        links.update(links_for(unresolved, want_res))

    written, failed, attribution = [], [], {}
    for logical, asset_id in wanted.items():
        link = links.get(asset_id)
        if not link:
            print(f"  {logical:<12} FAILED {asset_id}: no {want_res} download "
                  "link — the library did not offer one")
            failed.append(logical)
            continue
        try:
            blob = get(link, timeout=180)
        except Exception as e:                                   # noqa: BLE001
            print(f"  {logical:<12} FAILED {asset_id}: {type(e).__name__}: {e}")
            failed.append(logical)
            continue

        # Colour AND normal, since 16 Aug ("max polish" — the Standard
        # shader path in AssetLibrary now samples _BumpMap, so the normal
        # map stopped being weight for nothing and became the difference
        # between painted brick and brick). Roughness joined them the same
        # day, on the same rule going the other way: AssetLibrary is being
        # taught to sample it, so it stops being weight for nothing the
        # build after it lands. AO alone stays behind: nothing samples it.
        try:
            img, norm, rough, name = extract_maps(blob)
        except Exception as e:                                   # noqa: BLE001
            print(f"  {logical:<12} FAILED to read colour map from {asset_id}: "
                  f"{type(e).__name__}: {e}")
            failed.append(logical)
            continue

        ext = ".jpg" if name.lower().endswith(".jpg") else ".png"
        dest = textures / (logical + ext)
        dest.write_bytes(img)
        written.append(dest)
        norm_note = "no NormalGL in zip"
        if norm is not None:
            next_to = textures / (logical + "_n" + ext)
            next_to.write_bytes(norm)
            norm_note = f"+ {next_to.name} {len(norm) // 1024} KiB"
        rough_note = "no Roughness in zip"
        if rough is not None:
            r_to = textures / (logical + "_r" + ext)
            r_to.write_bytes(rough)
            rough_note = f"+ {r_to.name} {len(rough) // 1024} KiB"
        attribution[logical] = {
            **_ambientcg_attribution(asset_id, want_res),
            "file": dest.name,
            "normal": (logical + "_n" + ext) if norm is not None else None,
            "roughness": (logical + "_r" + ext) if rough is not None else None,
        }
        print(f"  {logical:<12} ok  {asset_id}  {len(img) // 1024} KiB  "
              f"-> {dest.name}  {norm_note}  {rough_note}")

    (PACK / "ATTRIBUTION.json").write_text(
        json.dumps({"note": "Sources for every file in this pack. "
                            "THIRD-PARTY.md is the human-readable copy and both "
                            "must agree; tools/citypack/pack_check.py enforces it.",
                    "surfaces": attribution}, indent=1), encoding="utf-8")

    print(f"\n{len(written)} written, {len(failed)} failed")
    # INVARIANT 7, from the voice pipeline. A run that filled none of its
    # targets must fail even if the directory is full of earlier successes.
    if not written:
        print("NOTHING WAS WRITTEN — this run failed whatever is on disk.")
        return 1
    if failed:
        print("PARTIAL — some surfaces did not arrive: " + ", ".join(failed))
        return 1
    return 0


# 1K is enough to SEE a material; the final pick is re-fetched at
# choices.json's own resolution (2K-JPG as of this writing) by an ordinary
# `--fetch` once choices.json names it, so this mode never ships a 1K file.
SHORTLIST_RES = "1K-JPG"


def _write_shortlist_attribution(out_root, resolution, surfaces):
    """ATTRIBUTION.json for `tools/citypack/shortlist/`, the record this
    directory owed before it could go on `WATCHED` in
    `tools/attribution-check.py` (queue 300, 2026-09-15).

    WRITTEN EVERY TIME THIS IS CALLED, never appended to and never skipped
    on a bad or empty run: `surfaces={}` still produces a file, so a run
    that downloaded nothing overwrites whatever an earlier run left rather
    than letting it be read as describing this one (ci.md: "a run that
    measured nothing must not carry forward the previous run's files under
    its own name"). Modelled on `fetch()`'s own `PACK / "ATTRIBUTION.json"`
    a few dozen lines up, and reusing `_ambientcg_attribution` so the two
    can never quietly disagree about what an ambientCG credit says.

    Only candidates this run actually WROTE TO DISK are named here: a
    candidate that failed (403, no link, a bad zip) is not an asset and
    `shortlist-results.json` is where its error lives, not here."""
    out_root.mkdir(parents=True, exist_ok=True)
    n = sum(len(v) for v in surfaces.values())
    (out_root / "ATTRIBUTION.json").write_text(
        json.dumps({"note": "Sources for every CANDIDATE tile this "
                            "shortlist pass actually wrote to disk. Nothing "
                            "under tools/citypack/shortlist/ is shipped or "
                            "read by AssetLibrary; THIRD-PARTY.md is the "
                            "human-readable copy and both must agree.",
                    "resolution": resolution,
                    "candidatesWritten": n,
                    "surfaces": surfaces}, indent=1), encoding="utf-8")
    return n


def shortlist():
    """THE PIECE QUEUE 300 NAMED AS MISSING. Download several CANDIDATES per
    flagged surface at 1K, measure every one on the three queue-300 numbers
    beside the surface's CURRENT file, and lay every candidate for a surface
    into ONE contact sheet — so the choice that follows is made from
    evidence instead of from a name, which is how kerb ended up wearing
    smooth cast concrete the first time (choices.json's own history: "PICKED
    BY NAME... No image can be seen from this container").

        python3 tools/citypack/fetch_textures.py --shortlist

    Reads `tools/citypack/shortlist-candidates.json`:
        {"resolution": "1K-JPG", "surfaces": {"kerb": ["Rock001", ...], ...}}

    Writes, and NEVER touches the shipped pack or choices.json — this is the
    look-before-you-choose pass, not the choice:
        tools/citypack/shortlist/<surface>/<assetId>.jpg   the actual pixels
        tools/citypack/shortlist/contact-<surface>.png     every candidate
            for one surface (current file first) tiled into ONE picture at
            ONE scale. The eye reads contrast and not value, and two crops
            looked at minutes apart are two memories and not a comparison
            (instruments.md) — this is the one-picture, one-scale,
            one-rectangle version of that rule, applied to a contact sheet
            instead of a before/after pair.
        tools/citypack/shortlist-results.json              the measured
            table, the surface's CURRENT file included by name so a
            candidate that is merely a DIFFERENT flat card is visible as one
            before anything is chosen.
        tools/citypack/shortlist/ATTRIBUTION.json           source, licence
            and download link for every candidate this run actually wrote to
            disk, written in this SAME run rather than by a separate step,
            so the pixels and the record cannot drift apart (LEDGER's
            provenance rule: the licence identified before the fetch,
            recorded WITH it). Overwritten every time this runs, including a
            run that downloads nothing, so a later reader can never mistake
            an earlier run's record for this one's.

    Emits no verdict key and gates nothing — flagged to Jafar in queue 300 as
    a possible new instrument rather than decided there; this stays quiet by
    the same reasoning until he rules on it."""
    path = HERE / "shortlist-candidates.json"
    if not path.exists():
        print(f"no {path.relative_to(ROOT)} — nothing to shortlist")
        _write_shortlist_attribution(HERE / "shortlist", SHORTLIST_RES, {})
        return 1
    spec = json.loads(path.read_text(encoding="utf-8"))
    surfaces = spec.get("surfaces", {})
    want_res = spec.get("resolution", SHORTLIST_RES)
    if not surfaces:
        print("shortlist-candidates.json names no surfaces — nothing to do")
        _write_shortlist_attribution(HERE / "shortlist", want_res, {})
        return 1

    # LINKS FROM THE COMMITTED CATALOGUE FIRST, exactly as --fetch does, and
    # for the same reason: the q= search endpoint has lied three times and
    # nothing in this file asks it anything any more.
    cat_path = HERE / "catalogue.json"
    cat_links = {}
    if cat_path.exists():
        for a in json.loads(cat_path.read_text(encoding="utf-8")).get("assets", []):
            if a.get("link") and want_res in (a.get("link") or ""):
                cat_links[a["id"]] = a["link"]

    all_ids = sorted({aid for ids in surfaces.values() for aid in ids})
    unresolved = [aid for aid in all_ids if aid not in cat_links]
    links = dict(cat_links)
    if unresolved:
        links.update(links_for(unresolved, want_res))

    out_root = HERE / "shortlist"
    results = {"resolution": want_res, "surfaces": {}}
    attribution = {}
    total_written, total_failed = 0, 0

    for surface, ids in sorted(surfaces.items()):
        print(f"\n{surface} — {len(ids)} candidate(s)")
        surf_dir = out_root / surface
        surf_dir.mkdir(parents=True, exist_ok=True)
        current = measure_pack_file(surface)
        row = {"current": current, "candidates": {}}
        surf_attribution = {}
        thumbs = []  # (label, jpeg/png bytes), current first
        if current is not None:
            cur_path = PACK / "textures" / current["file"]
            thumbs.append((f"CURRENT {current['file']}", cur_path.read_bytes()))
            print(f"  {'CURRENT':<16}      lumMean={current['lumMean']:<6} "
                  f"lumSD={current['lumSD']:<5} chromaSpread={current['chromaSpread']}")

        for aid in ids:
            link = links.get(aid)
            if not link:
                print(f"  {aid:<16} FAILED: no {want_res} download link")
                row["candidates"][aid] = {"error": "no download link"}
                total_failed += 1
                continue
            try:
                blob = get(link, timeout=180)
                img, _norm, _rough, name = extract_maps(blob)
            except Exception as e:                               # noqa: BLE001
                print(f"  {aid:<16} FAILED: {type(e).__name__}: {e}")
                row["candidates"][aid] = {"error": f"{type(e).__name__}: {e}"}
                total_failed += 1
                continue
            ext = ".jpg" if name.lower().endswith(".jpg") else ".png"
            dest = surf_dir / (aid + ext)
            dest.write_bytes(img)
            stats = measure_texel_stats(img)
            row["candidates"][aid] = stats
            surf_attribution[aid] = {
                **_ambientcg_attribution(aid, want_res),
                "downloadLink": link,
                "file": f"{surface}/{dest.name}",
            }
            thumbs.append((aid, img))
            total_written += 1
            print(f"  {aid:<16} ok   lumMean={stats['lumMean']:<6} "
                  f"lumSD={stats['lumSD']:<5} chromaSpread={stats['chromaSpread']}")

        _write_contact_sheet(out_root / f"contact-{surface}.png", thumbs)
        results["surfaces"][surface] = row
        if surf_attribution:
            attribution[surface] = surf_attribution

    (HERE / "shortlist-results.json").write_text(
        json.dumps(results, indent=1), encoding="utf-8")
    # WRITTEN IN THIS SAME RUN, UNCONDITIONALLY, before the invariant-7 exit
    # below, and whether that exit is about to fire or not, so ATTRIBUTION.json
    # always describes what THIS run actually wrote rather than what an
    # earlier one did (ci.md: a run that measured nothing must not carry
    # forward the previous run's files under its own name).
    n_attributed = _write_shortlist_attribution(out_root, want_res, attribution)
    print(f"\n{total_written} candidate(s) written, {total_failed} failed")
    print(f"wrote {(HERE / 'shortlist-results.json').relative_to(ROOT)}")
    print(f"wrote {(out_root / 'ATTRIBUTION.json').relative_to(ROOT)} "
          f"({n_attributed} candidate(s) attributed)")
    print("wrote contact sheets under "
          f"{out_root.relative_to(ROOT)}/contact-<surface>.png")
    # INVARIANT 7 AGAIN, BUT NOT `fetch()`'s ALL-OR-NOTHING VERSION. `fetch()`
    # fails on ANY missing surface because the shipped pack must be complete.
    # This is a gather-evidence pass, not a ship: one candidate id being
    # unavailable does not invalidate the comparison the way a missing
    # SHIPPED surface would, so this only fails when NOTHING at all arrived
    # — the "a run that fills none of its targets exits non-zero" half of
    # invariant 7, deliberately without the "and every target" half.
    if total_written == 0:
        print("NOTHING WAS WRITTEN — this run failed whatever is on disk.")
        return 1
    if total_failed:
        print(f"PARTIAL — {total_failed} candidate(s) did not arrive; the "
              "rest are still real evidence")
    return 0


def _write_contact_sheet(dest, thumbs, tile=256, cols=8):
    """One picture, one scale, one rectangle — every candidate for a surface
    side by side, because the eye reads contrast and not value and cannot
    compare two images it saw minutes apart (instruments.md). Each tile is a
    plain resize to a square, deliberately: this sheet is for material
    identity and tone, not for judging tiling or aspect ratio.

    COLS IS A LAYOUT CHOICE, NOT A RESOLUTION CHOICE — `tile` alone controls
    how many pixels a candidate gets, so widening `cols` costs no legibility.
    8 (2026-09-15, Jafar) turns metal's worst case (101 tiles: 100 candidates
    + current) from 26 rows / ~7200px at 4 columns into 13 rows / ~3620px at
    8, without shrinking a single tile below its full 256px, because the two
    numbers are independent in this function and always have been."""
    from PIL import Image, ImageDraw, ImageFont
    if not thumbs:
        return
    rows = (len(thumbs) + cols - 1) // cols
    pad, label_h = 6, 16
    sheet = Image.new("RGB", (cols * (tile + pad) + pad,
                              rows * (tile + label_h + pad) + pad),
                      (32, 32, 32))
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    for i, (label, blob) in enumerate(thumbs):
        im = Image.open(io.BytesIO(blob)).convert("RGB")
        im = im.resize((tile, tile), Image.LANCZOS)
        x = pad + (i % cols) * (tile + pad)
        y = pad + (i // cols) * (tile + label_h + pad)
        sheet.paste(im, (x, y))
        draw.text((x, y + tile + 2), label[:28], fill=(255, 255, 255), font=font)
    sheet.save(dest)
    print(f"  wrote {dest.relative_to(ROOT)}  ({len(thumbs)} tile(s))")


def measure_pack_cmd(names):
    """`--measure-pack [SURFACE ...]` — print the CURRENT committed pack's
    series, no network. This is the instrument the before/after table in
    queue 300's acceptance comes from: run it before a fetch and after, and
    the two printouts are "the new pack, printed beside the old". NO BOUND
    IS SET here and this prints no verdict key — a sourcing aid, not a gate,
    matching queue 300's own framing."""
    names = list(names) or list(FETCHABLE)
    print(f"{'file':<14} {'lumMean':>8} {'lumSD':>7} {'chromaSpread':>13}")
    found = 0
    for logical in names:
        stats = measure_pack_file(logical)
        if stats is None:
            print(f"{logical:<14} {'nothing measured — no file on disk under this name':>8}")
            continue
        found += 1
        print(f"{logical:<14} {stats['lumMean']:>8.1f} {stats['lumSD']:>7.1f} "
              f"{stats['chromaSpread']:>13.1f}   {stats['file']}")
    print(f"\n{found}/{len(names)} named surface(s) had a file to measure")
    return 0


# WHAT EACH HALF OF --selftest SEES, AND WHAT IT CANNOT. Rebuilt 2026-09-21
# after the old accepting case blocked this workflow for six days. That case
# asserted kerb.jpg == 184.3/6.6/0.0, which is a SNAPSHOT of the live pack
# and not the live pack: the shortlist route this selftest guards replaced
# the kerb (Concrete034 -> Rock048) twenty minutes after those constants were
# written, and from then on step 5 of citypack-shortlist.yml went red and
# skipped every step below it, so the first run after the swap downloaded
# zero candidates. instruments.md ends its selftest rule "so doing the work
# the tool prompts can never break the tool"; a pinned snapshot of the live
# tree is exactly how that clause gets broken, and updating the three numbers
# would re-arm it for the next pick.
#
#   DIFFERENTIAL HALF, the accepting case, self-deriving: measure_texel_stats
#   (numpy, vectorised) against _reference_texel_stats (pure python, scalar,
#   written from the docstring's definitions) over the same crop of the same
#   live file. Nothing is pinned, so no pick can make it stale. WHAT IT
#   CANNOT SEE: LUMA_R/G/B, since both sides read those three constants and a
#   changed weight moves both readings together; and a population/sample SD
#   swap, which on a 4096-texel crop shifts cropLumSD 37.0 by 0.0045 and so
#   hides under the tolerance (both measured 2026-09-21).
#
#   SYNTHETIC HALF, the rejecting/edge case: literal numbers, pinning exactly
#   what the differential half is blind to. It is written out rather than
#   computed, because the old synthetic check wrote its expectation as
#   round(LUMA_R * 255, 1), which compares the constant under test against
#   itself and therefore passed for any weight anybody typed.
#
#   WHY BOTH. A synthetic solid has lumSD 0.0 BY CONSTRUCTION, so every bug
#   in the standard-deviation path is invisible to it; real photographic data
#   at lumSD 37.0 is the only thing here that exercises that path. That is
#   why the differential half runs on the pack, and why a pack with no file
#   above lumSD 0 is reported as untested rather than clean.

# A CAP ON COST, and it announces itself on every line it prints (crop=WxH@0,0).
# Pure python over a whole 2K file takes 4.3s (measured 2026-09-21 on
# kerb.jpg, 4,194,304 texels), so all 17 pack files whole would be over a
# minute in a gate that runs before anything else; the top-left 64x64 is
# 4,096 texels and the half costs ~1.5s including the JPEG decodes. The same
# corner every run, so two runs are comparable.
SELFTEST_CROP = 64

# Both sides round to 1dp before comparing, so this tolerance admits AT MOST
# ONE DISPLAY TICK of disagreement and nothing larger. It is not zero because
# the two implementations sum in different orders (numpy's pairwise summation
# against python's left fold): over today's 51 properties the largest
# unrounded disagreement is 3.7e-12, and the closest any value comes to a .x5
# rounding boundary is 0.0017 (concrete.jpg lumSD 11.851669), so today every
# pair rounds to the same tick. A future file whose true value lands within
# 1e-12 of a boundary would round two ways with both implementations correct,
# and that is the only case this 0.1 exists for. Every fault worth catching
# is far bigger: chromaSpread as a max instead of a mean, or lumSD read as a
# peak, move these by whole units.
SELFTEST_TOL = 0.1


def _reference_texel_stats(crop):
    """The pure-python second opinion for --selftest's differential half,
    written FROM THE DEFINITIONS in `measure_texel_stats`'s docstring rather
    than from its code: the mean over every texel; lumSD a POPULATION
    standard deviation (divide by n, never n-1); chromaSpread the MEAN of
    per-texel (max channel minus min channel). No numpy here on purpose, so
    the two paths share only the three luma constants and the pixels.

    `crop` is an already-RGB PIL image. Pixel access is `tobytes()` and NOT
    `getdata()`, 2026-09-21: getdata is deprecated in Pillow 12 and removed
    in Pillow 14 (2027-10-15), and citypack-shortlist.yml pip-installs the
    newest Pillow, so getdata would print a DeprecationWarning into this
    instrument's own output today and raise inside the gate that blocks the
    whole workflow later. Checked equal on all 17 committed pack colour maps
    before choosing it: the triplets tobytes yields are exactly
    list(crop.getdata())."""
    raw = crop.tobytes()
    px = [(raw[i], raw[i + 1], raw[i + 2]) for i in range(0, len(raw), 3)]
    n = len(px)
    lums = [LUMA_R * r + LUMA_G * g + LUMA_B * b for r, g, b in px]
    mean = sum(lums) / n
    var = sum((x - mean) ** 2 for x in lums) / n     # population, /n not /(n-1)
    return {
        "texels": n,
        "lumMean": round(mean, 1),
        "lumSD": round(var ** 0.5, 1),
        "chromaSpread": round(sum(max(t) - min(t) for t in px) / n, 1),
    }


def _selftest_differential():
    """Measure every pack colour map on disk TWICE, two implementations, and
    compare. Per-file numbers go on the per-file line, whole-half numbers on
    the `differential done:` line, never one moment under the other's key."""
    from PIL import Image
    print("  differential: measure_texel_stats (numpy) against a pure-python "
          "reference,\n  same live file, printed below as measured/reference")
    examined = props = mismatched = sd_files = 0
    # PEAK lumSD over the files examined, carried with the file it came from,
    # so the done line's coverage number says which file supplied it.
    sd_peak, sd_peak_file = 0.0, "none"
    missing = []
    for logical in FETCHABLE:
        path = None
        for ext in (".jpg", ".png"):
            p = PACK / "textures" / (logical + ext)
            if p.exists():
                path = p
                break
        if path is None:
            missing.append(logical)
            continue
        im = Image.open(io.BytesIO(path.read_bytes())).convert("RGB")
        w, h = min(SELFTEST_CROP, im.size[0]), min(SELFTEST_CROP, im.size[1])
        crop = im.crop((0, 0, w, h))
        # PNG, not JPEG: a lossless re-encode, so the bytes handed to
        # measure_texel_stats decode back to the exact texels the reference
        # reads. A JPEG round trip here would compare two different images.
        buf = io.BytesIO()
        crop.save(buf, format="PNG")
        got = measure_texel_stats(buf.getvalue())
        ref = _reference_texel_stats(crop)
        examined += 1
        if ref["lumSD"] > 0:
            sd_files += 1
        if ref["lumSD"] > sd_peak:
            sd_peak, sd_peak_file = ref["lumSD"], path.name
        bad, pairs = [], []
        for k in ("lumMean", "lumSD", "chromaSpread"):
            props += 1
            # `crop` PREFIX, NOT THE BARE NAME. --shortlist already prints
            # `lumMean=` for a WHOLE candidate file (see the two prints in
            # shortlist()), and these are the top-left 64x64 only: same
            # statistic, different extent, and a reader greping lumMean=
            # across this tool's output would silently read two moments as
            # one. kerb.jpg is 136.1 whole and 129.4 on this corner.
            key = "crop" + k[0].upper() + k[1:]
            pairs.append(f"{key}={got[k]}/{ref[k]}")
            if abs(got[k] - ref[k]) > SELFTEST_TOL:
                bad.append(key)
        mismatched += len(bad)
        print(f"  {'FAIL' if bad else 'ok':<4} differential {path.name} "
              f"crop={w}x{h}@0,0 texels={ref['texels']} " + " ".join(pairs)
              + (" mismatched=" + "/".join(bad) if bad else ""))
    print(f"  differential done: filesExamined={examined}/{len(FETCHABLE)} "
          f"propsCompared={props} mismatched={mismatched} "
          f"sdCoverage={sd_files}/{examined} "
          f"cropLumSDpeak={sd_peak}@{sd_peak_file}"
          + (" noFileFor=" + "/".join(missing) if missing else ""))
    if examined == 0:
        print(f"  FAIL differential: nothing measured, no colour map on disk "
              f"under any of {len(FETCHABLE)} named surface(s)")
    elif sd_files == 0:
        print(f"  FAIL differential: nothing measured on the SD path, "
              f"0 of {examined} file(s) examined had lumSD above 0")
    return {"examined": examined, "props": props, "mismatched": mismatched,
            "sdFiles": sd_files}


def _selftest_synthetic():
    """Images built in memory whose three numbers are known by hand, pinning
    the two things the differential half cannot see: the luma weights, and
    population-versus-sample SD. Every `want` below is a literal; none is
    computed from the constants under test."""
    from PIL import Image

    def stats_of(im):
        buf = io.BytesIO()
        im.save(buf, format="PNG")
        return measure_texel_stats(buf.getvalue())

    checks = []
    # THE LUMA TRIPLE. 54.2/182.4/18.4 is Rec. 709 and only Rec. 709: Rec. 601
    # prints 76.2/149.7/29.1 and a plain average prints 85.0/85.0/85.0, so one
    # primary alone cannot tell the three apart and all three together can.
    for name, rgb, lum in (("solid-red", (255, 0, 0), 54.2),
                           ("solid-green", (0, 255, 0), 182.4),
                           ("solid-blue", (0, 0, 255), 18.4)):
        got = stats_of(Image.new("RGB", (16, 16), rgb))
        checks += [(name, "lumMean", got["lumMean"], lum, "Rec.709-weight"),
                   (name, "lumSD", got["lumSD"], 0.0, "one-colour-has-no-spread"),
                   (name, "chromaSpread", got["chromaSpread"], 255.0,
                    "one-channel-full-two-empty")]
    # THE SD DEFINITION, which nothing else here pins: the population SD of
    # {0, 255} is exactly half the range, 127.5, and the sample SD (ddof=1) of
    # the same two texels is 180.3. Two texels is the smallest image where
    # those two answers are far apart; on the 64x64 crops above the same swap
    # moves cropLumSD 37.0 by 0.0045 and would pass unseen.
    pair = Image.new("RGB", (2, 1))
    pair.putpixel((0, 0), (0, 0, 0))
    pair.putpixel((1, 0), (255, 255, 255))
    got = stats_of(pair)
    checks += [("black+white-pair", "lumMean", got["lumMean"], 127.5,
                "midpoint-of-0-and-255"),
               ("black+white-pair", "lumSD", got["lumSD"], 127.5,
                "population;ddof=1-would-print-180.3"),
               ("black+white-pair", "chromaSpread", got["chromaSpread"], 0.0,
                "grey-carries-no-chroma")]
    bad = 0
    for name, k, got_v, want, why in checks:
        # Half a tick: these numbers are exact by construction, so the two
        # sides must round to the same displayed value.
        good = abs(got_v - want) <= 0.05
        bad += 0 if good else 1
        print(f"  {'ok' if good else 'FAIL':<4} synthetic {name} {k}={got_v} "
              f"(want {want}, {why})")
    print(f"  synthetic done: imagesBuilt=4 propsCompared={len(checks)} "
          f"mismatched={bad}")
    return {"images": 4, "props": len(checks), "mismatched": bad}


def selftest():
    """`--selftest` - both halves above, no network, no fixture file.

    EXIT CODES ARE DISTINCT PER OUTCOME, so a red step says which kind of red
    it is without anybody opening the log: 0 both halves ran and agreed; 1 at
    least one property disagreed, which is a measurement fault; 3 the
    differential half had nothing to measure (no pack colour map on disk, or
    none above lumSD 0, so the SD path went untested), which is inconclusive
    rather than clean and must never read as a pass."""
    print("citypack --selftest: measure_texel_stats, two halves, no network\n")
    d = _selftest_differential()
    print()
    s = _selftest_synthetic()
    mismatched = d["mismatched"] + s["mismatched"]
    props = d["props"] + s["props"]
    tail = (f"{mismatched} mismatched of {props} prop(s) compared, over "
            f"{d['examined']} pack file(s) and {s['images']} synthetic "
            f"image(s)")
    if mismatched:
        print(f"\nSELFTEST FAIL: {tail} (differential {d['mismatched']}, "
              f"synthetic {s['mismatched']})")
        return 1
    if d["examined"] == 0 or d["sdFiles"] == 0:
        print(f"\nSELFTEST FAIL: nothing measured where it counts, so this is "
              f"not a clean run. {tail}")
        return 3
    print(f"\nSELFTEST PASS: {tail}")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--catalogue", action="store_true",
                    help="pull EVERY material id once; every later question is local")
    ap.add_argument("--inventory", action="store_true",
                    help="ask the catalogue what exists; download nothing")
    ap.add_argument("--validate", action="store_true",
                    help="check choices.json against the catalogue; no network")
    ap.add_argument("--fetch", action="store_true",
                    help="download the assets named in choices.json")
    ap.add_argument("--shortlist", action="store_true",
                    help="download tools/citypack/shortlist-candidates.json at "
                         "1K, measure each against the surface's current file, "
                         "write a contact sheet per surface; never touches the "
                         "shipped pack or choices.json")
    ap.add_argument("--measure-pack", nargs="*", metavar="SURFACE", default=None,
                    help="print the CURRENT committed pack's lumMean/lumSD/"
                         "chromaSpread for the named logical surfaces (default: "
                         "every surface AssetLibrary asks for); no network")
    ap.add_argument("--selftest", action="store_true",
                    help="check measure_texel_stats twice over: against a "
                         "pure-python reference on every pack file, and "
                         "against synthetic images that pin the luma weights; "
                         "no network; exit 1 is a disagreement, exit 3 is "
                         "nothing measured")
    args = ap.parse_args()
    if args.catalogue:
        return catalogue()
    if args.validate:
        return validate()
    if args.inventory:
        return inventory()
    if args.fetch:
        return fetch()
    if args.shortlist:
        return shortlist()
    if args.measure_pack is not None:
        return measure_pack_cmd(args.measure_pack)
    if args.selftest:
        return selftest()
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
