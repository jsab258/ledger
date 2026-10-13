"""sd_doc: small helpers that write the tables of a TARGET.md from target.json, so the page and the data cannot drift."""
import numpy as np

import sd_lib as L


def table(headers, rows):
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    for r in rows:
        out.append("| " + " | ".join(str(c).replace("|", "/").replace("\n", " ") for c in r) + " |")
    return "\n".join(out)


def ext(ps, name):
    lo, hi = ps.part_bbox(name)
    return lo, hi


def parts_table(T, V):
    ps = L.PartSet(T["variants"][V]["parts"])
    rows = []
    for p in T["variants"][V]["parts"]:
        lo, hi = ps.part_bbox(p["id"])
        flags = []
        if p.get("transparent"):
            flags.append("transparent")
        if p.get("film"):
            flags.append("film")
        rows.append([p["id"], p["type"], p.get("material", ""), "%.0f to %.0f" % (lo[0], hi[0]), "%.0f to %.0f" % (lo[1], hi[1]),
                     "%.0f to %.0f" % (lo[2], hi[2]), p.get("edge", ""), p.get("note", "") + (" (" + ", ".join(flags) + ")" if flags else "")])
    return table(["part", "kind", "material", "x (mm)", "y (mm)", "z (mm)", "edges", "note"], rows)


def materials_table(T):
    rows = []
    for k, m in T["materials"].items():
        rows.append([k, m.get("name", ""), "%d, %d, %d" % tuple(m["srgb"]), "%.2f (%s)" % (m["rough"], m.get("rough_words", "")),
                     "metal" if m.get("metal") else "not metal", m.get("note", "")])
    return table(["id", "plain name", "sRGB", "roughness", "metal", "note"], rows)


def numbers_table(T):
    rows = []
    for n in T["numbers"]:
        rows.append([n["id"], n["what"], "%s %s" % (_f(n["value"]), n.get("unit", "mm")), n["kind"], n["source"], "+-%s" % _f(n.get("tol", 1.0))])
    return table(["id", "what", "value", "kind", "source and method", "tolerance"], rows)


def _f(x):
    return ("%.1f" % x).rstrip("0").rstrip(".")


def sources_table(T):
    rows = []
    for s in T["sources"]:
        rows.append([s["id"], s["url"], s["read"], s["author"], s["licence"], s["taken"], s["shows"], "YES" if s["used"] else "no", s["not_used_for"], s["period"]])
    return table(["id", "url", "read", "author", "licence", "taken", "what it shows", "used", "not used for", "period"], rows)


def checks_table(T):
    rows = []
    for c in T["checks"]:
        rows.append([c["name"], c["measure"], c["expect"], c["tol"]])
    return table(["check", "what to measure", "expected", "tolerance"], rows)


def photo_table(T):
    rows = []
    for ph in T.get("photos", []):
        for f in ph["features"]:
            rows.append([ph["id"], f["id"], f["axis"], "%.1f" % f["px"], f["box"], "%.1f" % f["tol_px"], "%s of %s" % (f["ref"].get("side", "hi"), f["ref"].get("part") or f["ref"].get("parts"))])
    return table(["photo", "feature", "axis", "measured px", "recorded box (x0 y0 x1 y1)", "error px", "drawn edge"], rows)


def owed_list(T):
    return "\n".join("%d. %s (recommended: %s)" % (i + 1, o["line"], o["recommended"]) for i, o in enumerate(T.get("owed", [])))


COMMON_RULINGS = [
    ["RULINGS 2 Oct", "no cars until real; skip and pallets off until real; the KX100 phone box stays", "{ruling_2oct}"],
    ["RULINGS 3 Oct (sources order)", "free assets that fit first (Poly Haven, ambientCG, CC0), else our own in Blender from real photographs", "{sources_order}"],
    ["content rule (canon D18)", "what the rule forbids is out of image and text", "{content}"],
    ["NoAI and licences", "nothing marked NoAI; photographs only free licences, for measuring, never placed in the game or traced", "{noai}"],
    ["RULINGS 1 Oct, 3 Oct (the look)", "the Hook sheet and KCD2 frames; wet, dark, glistening grime", "{look}"],
    ["RULINGS 1 Oct (night)", "pools of lamp light, not one orange wash", "the lantern colour (1.0, 0.25, 0.0) linear only; {night}"],
    ["RULINGS 8 Oct", "photographs win over books, element by element", "see 'Where the photographs win'"],
    ["RULINGS 13 Oct (RECIPE)", "a notebook entry per unit", "RECIPE.md carries unit 13's entry"],
    ["RULINGS 16 Sep, 29 Sep (money, live talk)", "nothing bought without his yes; live talk names no real make, brand or shop and nothing after 1992", "nothing bought (the photographs and the model records are free to read); every name on a part or a card is invented; nothing in the target is dated after 1992"],
    ["the rest of RULINGS.md", "read in full on 13 October for this unit (faces, voices, clothes, people, talk, story, combat, disk and git)", "none of them touches this object; the weather ruling (a grey range, never sunshine) governs how the game lights it, not the target"],
]


def std_doc(T, S):
    """The standard TARGET.md. S holds the family's own prose: title, summary, files_extra, rulings (dict), searched,
    reuse (rows), assembly (bullets), builder (bullets), placement text, lettering, etc."""
    sc = T.get("self_check", {}).get("line", "SELF-CHECK %s: not yet run" % T["family"])
    out = []
    w = out.append
    w("# " + S["title"])
    w("")
    w("**" + S["summary"] + "**")
    w("")
    w("Cloud week 42, unit 13, family %s. Written 13 October 2026, not yet reviewed. `%s`" % (S["no"], sc))
    w("")
    w("## Files in this folder")
    w("")
    w("- `target.json`: the whole target (millimetres; z up; the front faces -y; pivot at the base's centre on the ground; the .glb is metres). Parts, numbers, photograph features, checks, owed lines.")
    w("- `make_target.py` (data and this page), `measure.py` and `photo_measurements.json` (the pixel measurements), `target_drawing.py` (draws target.json alone: `target_drawing.json` and pictures), `self_check.py` (checks and negative controls), `make_previews.py` (preview crops and the overlay).")
    w("- Previews in `production/previews/cloud-week/refs/street-dressing/%s/`: %s." % (T["family"], S["previews_list"]))
    w("- Shared tools one level up: `../sd_lib.py`, `../sd_check.py`, `../sd_doc.py`, `../sd_photo.py`.")
    w("")
    w("## The rulings that bind, and how this target meets each")
    w("")
    rows = [[a, b, c.format(**S["rulings"])] for a, b, c in COMMON_RULINGS]
    rows += S.get("rulings_extra", [])
    w(table(["ruling", "what it says", "this target"], rows))
    w("")
    w("## Sources")
    w("")
    w(sources_table(T))
    w("")
    w(S["searched"])
    w("")
    w("## What already exists, and what is done with it")
    w("")
    w(table(["existing thing", "what it is", "verdict", "why"], S["reuse"]))
    w("")
    w("## The target")
    w("")
    w(S["axes"])
    w("")
    w("### Assembly in words")
    w("")
    for x in S["assembly"]:
        w("- " + x)
    w("")
    for V in T["variants"]:
        w("### Parts, variant %s: %s (millimetres)" % (V, T["variants"][V]["name"]))
        w("")
        w(parts_table(T, V))
        w("")
    w("### The numbers, with their sources and kinds (the self-check measures each back off the parts)")
    w("")
    w(numbers_table(T))
    w("")
    for ph in T.get("photos", []):
        w("### Photograph measurements (%s, %s)" % (ph["id"], ph["source"]))
        w("")
        w(ph["method"] + ".")
        w("")
        w(photo_table({"photos": [ph]}))
        w("")
    w("### Materials and colours")
    w("")
    w(materials_table(T))
    w("")
    w("### Wear")
    w("")
    for x in T["wear"]:
        w("- " + x)
    w("")
    w("### Variants the street needs")
    w("")
    for x in T["variants_note"]:
        w("- " + x)
    w("")
    w("### Where it stands on Quay Street")
    w("")
    w("**Slot:** %s" % T["placement"]["slot"])
    w("")
    for r in T["placement"]["reasons"]:
        w("- " + r)
    w("")
    for x in S.get("placement_extra", []):
        w(x)
        w("")
    if S.get("lettering"):
        w("### Lettering and text")
        w("")
        for x in S["lettering"]:
            w("- " + x)
        w("")
    w("### Where the photographs win over the books")
    w("")
    w(table(["id", "what", "the book or script", "the photograph", "chosen"], [[d["id"], d["what"], d["book"], d["photo"], d["chose"]] for d in T["disagreements"]]))
    w("")
    w("### Checks for the builder (target.json `checks`)")
    w("")
    w(checks_table(T))
    w("")
    w("### For the builder")
    w("")
    for x in T["builder_notes"]:
        w("- " + x)
    w("")
    w("## Owed to Jafar's page (one line each, with a recommendation)")
    w("")
    w(owed_list(T) or "None.")
    w("")
    if T.get("handovers"):
        w("## Handovers (for the town or the scene's owner, not for his page)")
        w("")
        for h in T["handovers"]:
            w("- %s: %s" % (h["id"], h["line"]))
        w("")
    w("## What the target could not settle")
    w("")
    for x in T["not_settled"]:
        w("- " + x)
    w("")
    w("## How the self-check is built")
    w("")
    w("`python self_check.py` (offline) rebuilds the parts' geometry from target.json and tests: the overall box against the printed numbers; every number measured back off the parts; no floating part, every part meeting a neighbour, every declared join, no part sinking into another beyond its allowance; each closed face shot with rays square on and leaning 30 and 45 degrees (fine across one direction and coarse along the other); the photograph's features predicted from the drawing with the scale fitted on the height only and compared with the pixels' measured edges; the text scanned for real makers and for what the content rule forbids; the lines for his page for em dashes and italics; the family's own rows (%s). `--live` re-reads the Geograph pages and re-measures the photographs' edges from the pixels; `--previews` checks the preview files. Each negative control is a deliberately wrong copy that must make its named row fail." % S["own_rows"])
    return "\n".join(out) + "\n"
