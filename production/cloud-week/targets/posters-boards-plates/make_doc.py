"""Author tool: writes TARGET.md from target.json plus the prose below (cloud week 42, 8 October 2026).

    /home/user/.bpyenv/bin/python make_doc.py

The tables (items, words, placements, colours, checks) are read from target.json so the page and the JSON cannot disagree.
"""
import json
import sys
sys.dont_write_bytecode = True
from pathlib import Path

HERE = Path(__file__).resolve().parent
T = json.loads((HERE / "target.json").read_text(encoding="utf-8"))
ITEMS = {i["id"]: i for i in T["items"]}
PAL = T["palette"]
out = []


def w(s=""):
    out.append(s)


def rgb(c):
    return "(%d,%d,%d)" % tuple(c)


def fnum(x):
    return ("%g" % x)


N_RULES = 0
try:
    import importlib.util, sys
    _sp = importlib.util.spec_from_file_location("_cg", str(HERE.parents[3] / "tools" / "content-gate.py"))
    _m = importlib.util.module_from_spec(_sp)
    sys.modules["_cg"] = _m
    _sp.loader.exec_module(_m)
    N_RULES = len(_m.RULES)
except Exception:
    N_RULES = 0
sc = T.get("self_check") or {}
summary = T["summary_line"]
w("# Quay Street's paper and small boards: the exact target")
w()
w(summary)
w()
w("Cloud week 42, written 8 to 9 October 2026. FIRST TRY. Three 2D units build from `target.json` and this page: 4.2 posters and notices, 4.3 \"To Let\" boards, 4.4 street name plates. Nothing is committed.")
if sc.get("summary"):
    w()
    w("Self-check: **%s** (see section 14)." % sc["summary"])
w()
w("Plain summary. Seventy-six sheets, cards, boards and plates, every word ours, listed and checked against the content rule, canon and the 1990 calendar. The street's biggest piece of paper is the east parade's **quay gable** (the brick end wall of Mickey's block at street x 3, the big wall at the right of the hook frame): three layers of fly-posted bills there, twelve bills and three stickers, with a ferry timetable case and a Harbour Board notice case at its far end. The empty unit's whitened glass carries eight more. The plain west terrace's six brick piers carry seven. The poll tax is an invented local campaign; the chapel hall (the game's own `chapel_hall`) holds the jumble sale, the dance and the advice evening; the Tivoli's two invented films have quads and a programme; the fights are at an invented Drill Hall; the market bill matches the cast's market days to the hour. The letting boards carry a PROPOSED agent (ARMITAGE & STOBBS, not minted) and a no-agent variant. The street plates are sized from their names, Marcellus SC capitals 90 mm tall, with the district's name as a small line and no council. What the first try could not do is stand on a photograph: see section 0.")
w()
w("Files in this folder:")
w()
w("- `target.json`: the whole target (76 items, 70 placements, 2 cases, a card board, 6 piers, 8 shop fronts, 473 checks, the self-check result).")
w("- `make_target.py`: the author tool that writes `target.json` (every width is measured on the real font files).")
w("- `target_drawing.py`: draws every item's boxes, baselines and clean lettering at 1 mm to the pixel, the surfaces' elevations and the cases, from `target.json` alone, into a folder given on the command line, plus the polygons as JSON.")
w("- `self_check.py`: its checks and their count are in section 14; it writes its result into `target.json` under `self_check`; `--fetch-fonts DIR` fetches the four fonts not in `production/fonts`.")
w("- `make_previews.py`, `make_doc.py`: rebuild the previews and this page.")
w("- Previews, in `production/previews/cloud-week/refs/posters-boards-plates/`: `P1-urban-street-01-notice-case.jpg` (the one photograph measured, windows masked), `P1-...-target-on-photo.jpg` (the proportions laid on it), `L1` to `L4` (layout sheets of every item), `L5` (the paste plan of the gable and the empty unit's glass).")
w()

# ------------------------------------------------------------------ 0
w("## 0. What this target rests on, in plain words")
w()
w("- **Photographs measured today: one, and it is not the period.** Poly Haven's Urban Street 01 (CC0, Andreas Mischok, 18 August 2019) shows four glazed notice cases, blue steel, 2000s. I measured their VERTICAL proportions (header 0.152 of the height, window 0.763, foot 0.085, side bands 0.205 of the apparent width, each with its error) and used them only as a cross-check of a glazed case's shape. Nothing else in this target is measured on a photograph.")
w("- **Photographs looked at and not used.** Eight other Poly Haven panoramas (London streets and docks, Cambridge, a Dublin quay): none shows a street name plate, a letting board or a poster hoarding that could be measured. Bethnal Green Entrance has a stickered modern pole plate and, in the same frame, a council byelaw sign about alcohol: nothing from it is kept, no crop, no file.")
w("- **Earlier notes (they read period photographs and search summaries on the PC; read here, not re-measured):** the 1990 mix of Letraset, photocopy and two-colour print (asset-plan note 4); the 1952 Kindersley recommendation for name plates (street-clutter note); the winter timetable date of 1 October 1990 and the pasted-over summer sheet (transport-timetables note, the brand bible); cod at about 2.60 a lb in 1990 (the fishmonger note, ONS); the Harbour Board's blue and white enamel and glass case with notices drawing-pinned and curling (the brand bible); the hours, the market's days and the chapel hall (`hook-cast.json`).")
w("- **Search summaries (leads, never numbers):** modern street-plate specifications (90 mm capitals, 150 to 230 mm plates, 12 mm borders, 11 SWG aluminium), a Hull caption on 1920s to 1930s cast plates, a statement that there is no national plate design and that each council chose its own, a Hackney Museum 1990 'Pay No Poll Tax' sheet on yellow paper in red ink, the Double Crown sheet. The pages themselves were not fetched (DNS and 403).")
w("- **Judgement:** every size, colour, wording, price, ageing number and placement not listed above. Section 1 says the kind of each class of number.")
w("- **The honest summary:** this is the weakest of the family targets on its photographic side. It is strong where the project's own files decide: the streets and districts canon mints, the shops' hours and the market's days, the fascia target's positions and left-right rule, the plain row's bay layout, the 1990 calendar, the content rule and the lists of real names. A fresh reviewer should look hardest at sizes and at ageing.")
w()
w("What I would read once the network opens (all unreached today):")
w()
for s in T["would_read_when_network_opens"]:
    w("- " + s)
w()

# ------------------------------------------------------------------ 1
w("## 1. Reading this file")
w()
w("- Units. Every item has its own frame: **x in millimetres from the viewer's LEFT edge as seen IN THE GAME, y UP from the item's bottom edge**; a block's `baseline_mm` is measured up from the bottom edge. Authoring scale: 2 pixels to the millimetre for paper and cards (so a 2.4 mm imprint is 4.8 px), 1 pixel to the millimetre for boards and plates. Surfaces use metres: `u` from the surface's viewer's-left edge, `z` up from the pavement; street x is metres along Quay Street (0 at the quay end), the same in the recipe and the game.")
w("- Left and right are the VIEWER'S, in the game, by the fascia target's rule: the game mirrors the recipe, so low street x is on the viewer's RIGHT looking at the east parade and on the viewer's LEFT looking at the west block. Every sheet's x runs from the viewer's left; the quay gable is read looking +x, with the front corner at the viewer's left.")
w("- Evidence kinds: Read (printed), Scaled (off a drawing or the game's files), Photo (measured on a photograph today), Derived (computed), Judgement (mine, to be overturned), Lead (a search summary, never a number).")
w("- Colours are sRGB 0 to 255, contrast is WCAG, dE is CIE76. Aged colours are for four classes (section 4).")
w()
w("The kind of each class of number in this target:")
w()
w("| Numbers | Kind | Source |")
w("|---|---|---|")
for a, b, c in [
    ("sheet sizes (crown, double crown, quad, four-sheet; A2 to A6)", "Derived", "imperial names x 25.4 mm; ISO 216 halving; the Double Crown name is also a Lead"),
    ("ink width of every line, cap ratios, plate lengths, tide and ferry times", "Derived", "measured on the real font files / computed in make_target.py, re-measured by self_check.py"),
    ("the calendar: every weekday and date", "Derived", "datetime, 1990; 1 October 1990 was a Monday"),
    ("street x of the shops, door ends, hanging signs, the fascia, the letting board's centre", "Read", "the fascia target, SCENE-SLOTS.md, vignette-scene.json"),
    ("the six piers, the glass, the shop widths", "Derived", "terrace-front.py's plain-row layout and the shopfront numbers (0.35, 3.562, 0.9, 0.838)"),
    ("shop hours, the market's days and hours, the chapel hall, Hal's break, the ferry's last crossing", "Read", "hook-cast.json, tier2-batch-1.json, the brand bible"),
    ("the cod price", "Read (earlier note)", "ONS series CZOL via FISHMONGER-2026-10-03.md"),
    ("the case proportions (0.152, 0.763, 0.085, 0.205)", "Photo", "one 2019 modern case, with errors; NOT the period"),
    ("90 mm capitals, 175 to 240 mm plates, 12 mm border, 30 mm fixings", "Judgement on a Lead", "modern specifications in search summaries"),
    ("every other size, layout, colour, cap, ageing, wear and placement number; every price but the cod", "Judgement", "the writer's"),
]:
    w("| %s | %s | %s |" % (a, b, c))
w()

# ------------------------------------------------------------------ 2
w("## 2. Where each piece goes on the street")
w()
w("Everything here is **Judgement on the scene's own numbers**: SCENE-SLOTS.md, `vignette-scene.json`, the recipe (`terrace-front.py`) and the fascia target. Where a slot in the scene file is stale, the page says so.")
w()
w("| Surface | What it is | Frame and paste zone | What goes there |")
w("|---|---|---|---|")
S = T["surfaces"]
w("| SF1 | the quay gable: the east parade's south end wall, plane x = 3.0 m, facing -x (the big brick wall at the right of the hook frame, `morning-hook-day-2026-10-08.jpg`) | u from the front corner into the block (viewer's left), 0 to 8.0 m; z 0 to 6.3 m; paste zone u 0.15 to 6.0, z 0.45 to 2.75 | 12 bills in 3 layers, 3 stickers; the ferry case FC1 at u 6.20 and the Harbour Board case HC1 at u 6.95, both z 1.20 up |")
w("| SF2 | the empty unit's whitened glass (bay 3, east, street x 21 to 27) | u from the glass's viewer's-left edge, 0 to 3.562 m; z 0.60 to 2.40; the glass is street x 23.088 to 26.65 (the recipe's `fx` counts from the viewer's RIGHT: u = 3.562 x (1 - fx)) | 8 items: five bills, a crown bill, the planning notice, a sticker; whitewash shows above 2.0 m |")
w("| WEST_PIER | six brick piers of the plain west block (street x 3 to 21), each 0.95 to 0.956 m, computed from the plain row's layout (door at bay start + 1.5 or + 4.5, windows 0.85 wide at + 3.3 and + 5.1 or + 0.9 and + 2.7) | street x of the pier's centre; z from the pavement | 7 items (below) |")
w("| SF4 | the three lamp columns, street x 8, 28, 48 (SCENE-SLOTS: every 20 m, first at 8 m, 0.6 m back from the kerb, alternate sides) | the shaft 0.114 m across; a bill wraps it: the middle 0.17 m of an A3 shows face-on | C03 and a sticker at x 8; two stickers at x 28 |")
w("| SF5 | the empty unit's fascia (0.55 m, z 2.85 to 3.40, 0.12 proud) | centre street x 24.0 = the fascia target's board x 2705; the board z 2.90 to 3.35 | the letting board L01 (or L02) |")
w("| SF6 | first-floor brick above bay 3's cornice (3.55) and below the upper sills (about 4.3), between the two upper windows (street x 22.93 to 25.07) | centre street x 24.0, z 3.70 to 4.10 | the flat board L03 |")
w("| SF7 | name-plate walls | see section 8 | S01d twice, S02d once |")
w("| SF8 | a quay-edge post, street x about -0.6 (PROPOSED: SCENE-SLOTS has no quay geometry) | z 1.20 up | H02, DANGER DEEP WATER |")
w("| SHOP | eight shop fronts: glass 3.562 m, shop door 0.9, side door 0.838, pilasters 0.35 (C5, C8, C9), the door order following the fascia target's door ends | u from the glass's (or the shop door's) viewer's-left edge | the cards: section 5.6, 5.7 |")
w()
w("Piers (street x of the clear brick, from the recipe's bay layout; bay 1 agrees with the scene file's note that the poster slot at x 11.4 lies between a door at 10.5 and a window at 12.3):")
w()
w("| Pier | x0 to x1 | centre | between | bill |")
w("|---|---|---|---|---|")
byp = {}
for p in T["placements"]:
    if p["surface"] == "WEST_PIER":
        byp.setdefault(p["pier"], []).append("%s z %.2f" % (p["item"], p["z_bottom_m"]))
for pr in T["west_piers"]:
    w("| %s | %.3f to %.3f | %.3f | %s | %s |" % (pr["id"], pr["x0"], pr["x1"], pr["cx"], pr["between"], ", ".join(byp.get(pr["id"], [])) or "none"))
w()
w("The scene file's two held props are stale: its poster at west x 11.4 is the pier W1.0 and stays; its glazed case at west x 26.4 would stand on the tea room's glass (the west block is shops, not plain, from x 24) so both cases move to the quay gable.")
w()

# ------------------------------------------------------------------ 3
w("## 3. Sizes, stocks, processes and what they look like")
w()
w("British paper sizes of the period (Derived from the imperial names: 25.4 mm to the inch; the Double Crown 20 x 30 in is a Lead from a search summary).")
w()
w("| Name | mm | used for |")
w("|---|---|---|")
use = dict(crown="J01", double_crown="the poll-tax, fight, market, dance, tea and programme bills", quad_crown="T01, T02 (landscape, 'the quad')", four_sheet="G01 (one on the gable)",
           A2="F01, F02 (the ferry sheets)", A3="police and road-closure notices", A4="the advice sheet, planning notice, three Harbour Board notices", A5L="cards K01, K05, K06 a and b, K08",
           A6L="K06c, SA15", A5="(portrait, not used)", A6="(portrait, not used)")
for k, v in T["formats"].items():
    w("| %s | %d x %d | %s |" % (k, v["w"], v["h"], use.get(k, "")))
w()
w("Processes, in plain words (the numbers are in `processes`):")
w()
for k, v in T["processes"].items():
    extra = []
    for kk in ("registration_offset_mm", "impression_mm", "toner_density", "pitch", "roughness", "relief_mm", "thickness_mm"):
        if kk in v:
            extra.append("%s %s" % (kk, v[kk]))
    w("- **%s**: %s%s%s" % (k, v["name"], ("; " + "; ".join(extra)) if extra else "", ("; lead: " + v["lead"]) if v.get("lead") else ""))
w()
w("The look in one paragraph per kind (all Judgement unless a lead is named):")
w()
w("- **Fly-posters** are two-colour jobs from a small jobbing printer: black and one colour on cheap uncoated poster paper, white or tinted or fluorescent, set in a mixture of faces with thick rules and a printer's imprint in 7-point at the foot. Letterpress bills show a darker rim at the letter edges and a faint relief; screen-printed ones are flat and a little thick; the second colour sits 0.3 to 0.8 mm off register. The poll-tax bills use fluorescent yellow and orange stock because the one 1990 sheet found is yellow in red ink (a Lead).")
w("- **Quads and the four-sheet** are offset litho in full colour on uncoated paper. The halftone is not resolved at 2 px to the millimetre, so they are drawn as continuous tone with grain; the image model makes the picture only (no words, no people), our text layer lays every letter, and a dark scrim guarantees the contrast of the lines on the art.")
w("- **Photocopies** (the advice sheet, the police appeals, the planning and road notices) are hard black toner on white or tinted copier paper: a grey band 3 to 6 mm along one edge, speckle, a crooked copy, a vertical streak or two. Planning and road notices sit in a clear polythene sleeve.")
w("- **Typed notices** (the Harbour Board's) are Courier Prime, 10 characters to the inch, an electric typewriter's even impression, pinned in a glass case with drawing pins, curling.")
w("- **Hand-lettered cards** are felt pen (a fat even line, a darker blob where the nib rested) in Patrick Hand capitals, and ballpoint (a thin line, lighter on the joins) on white or tinted record cards; each is taped or pinned and slightly crooked.")
w("- **Stickers** are printed paper labels, die-cut, edges lifting and scratched.")
w("- **Enamel signs** are vitreous enamel on pressed steel: gloss, rolled edge, chips to black steel with a rust halo at the corners and the bolts.")
w()

# ------------------------------------------------------------------ 4
w("## 4. Stocks, inks, paints and ageing")
w()
w("Four classes by days on the wall: **A** fresh (0 to 7 days), **B** weeks (8 to 35), **C** months (36 to 120), **D** old (over 120). A colour fades by f = 1 - exp(-t / tau) (tau in days, per ink or stock) towards the paper, the paper yellows (30 per cent of the way to (214,200,168) at class D), and a grime film (62,58,52) mixes in at 0, 5, 12 and 22 per cent (35 per cent of that over ink). The order of fastness (Judgement) is fluorescent stock, then red, blue, black, toner.")
w()
w("| Stock | fresh | A | B | C | D | tau |")
w("|---|---|---|---|---|---|---|")
for k, v in PAL["stocks"].items():
    w("| %s | %s | %s | %s | %s | %s | %s |" % (v["name"], rgb(v["fresh"]), rgb(v["aged"]["A"]), rgb(v["aged"]["B"]), rgb(v["aged"]["C"]), rgb(v["aged"]["D"]), v["tau_days"] or "none"))
w()
w("| Ink | fresh | tau (days) |")
w("|---|---|---|")
for k, v in PAL["inks"].items():
    if v["fresh"]:
        w("| %s | %s | %s |" % (v["name"], rgb(v["fresh"]), v["tau_days"]))
w()
w("| Paint | fresh | B | D |")
w("|---|---|---|---|")
for k, v in PAL["paints"].items():
    w("| %s | %s | %s | %s |" % (v["name"], rgb(v["fresh"]), rgb(v["aged"]["B"]), rgb(v["aged"]["D"])))
w()
ar = T["age_rules"]["paper_wear"]
w("Paper wear (numbers for the builder; Judgement): wrinkles of 0.4 to 1.5 mm, wavelength 12 to 40 mm, from wallpaper-paste cockling, strongest along the brush direction (vertical); corners lifting 0 to 3 of radius 15 to 60 mm (none at class A, three at D); tears 0 to 4 of width 20 to 140 mm from an edge; rain runs 2 to 8 a metre, 10 to 60 mm long, 0.4 to 1.5 mm wide, opacity 0.15 to 0.4, down from the top edge and from any lifted corner, the red and dye inks running first; a paste halo 2 to 10 mm at class C and D; share of the sheet lost 0 to 0.05 at B, 0.03 to 0.2 at C, 0.3 to 0.6 at D, the lower corners first; skew -1.5 to +1.5 degrees; up to three layers, each newer bill covering at most 55 per cent of an older one, overlapping edges 0 to 40 mm. A wet wall darkens paper by 12 per cent and raises saturation by 10 per cent (a runtime hint).")
w()
w("Wear tables by kind (`wear_tables`): " + "; ".join(k for k in T["wear_tables"]) + ".")
w()

# ------------------------------------------------------------------ fonts
w("## 4b. Type")
w()
w("Sixteen font files from thirteen families, **all SIL OFL 1.1, every family's OFL.txt read whole on raw.githubusercontent.com today** (UnifrakturMaguntia's and Arimo's OFL texts and Liberation's LICENSE were read too and are not used; Liberation's font files were not reached). Letters are RENDERED into pictures: the OFL puts no restriction on a picture made with a font. The font files themselves are NOT copied into `production/fonts` here.")
w()
w("| Key | Family | Used for | In production/fonts | RFN |")
w("|---|---|---|---|---|")
usedby = {}
for it in T["items"]:
    for b in it["blocks"]:
        usedby.setdefault(b["font"], set()).add(it["id"])
for k, v in T["fonts"].items():
    ids = sorted(usedby.get(k, []))
    w("| %s | %s | %s | %s | %s |" % (k, v["family"], (", ".join(ids[:8]) + (" ... (%d items)" % len(ids) if len(ids) > 8 else "")) if ids else "not used", "yes" if v["in_repo"] else "NO: add with its OFL.txt", v.get("rfn") or "none"))
w()
w("Four are not in `production/fonts` (Archivo, Courier Prime Regular and Bold, Libre Baskerville); `self_check.py --fetch-fonts DIR` fetches them and the OFL texts. The old bills used League Gothic (in the repository, an OFL face, but not on the asset plan's table): this target uses Oswald instead. Overpass is never used. No UnifrakturMaguntia: a masthead would name a local paper, which canon owes.")
w()

# ------------------------------------------------------------------ 5 items
w("## 5. The items, word by word (unit 4.2)")
w()
w("Each line: the exact words, the font and weight, the cap height in millimetres, the anchor and x, the baseline y, the ink, and the contrast of ink on ground in class B. Anchors are of the INK, not the advance box. Every width is measured on the real font file; every box is in `target.json` (`ink_box_mm`).")
w()


def item_block(iid, extra=""):
    it = ITEMS[iid]
    f = it["format"]
    w("#### %s  %s" % (iid, it["title"]))
    w()
    bits = ["%d x %d mm (%s)" % (f["w_mm"], f["h_mm"], f["name"] or "own size"), "%d px/mm" % it["px_per_mm"]]
    if it.get("stock") and it["kind"] in ("sheet", "card", "sticker"):
        bits.append("stock: " + PAL["stocks"][it["stock"]]["name"])
    bits.append("process: " + it["process"])
    if it.get("event"):
        bits.append("event: " + it["event"]["date"])
    w("- " + "; ".join(bits))
    vv = it["variants"]
    w("- variants: %s (%s)" % (vv.get("n", "?"), "; ".join(vv.get("vary", []))))
    if it.get("mirror_cue"):
        w("- mirror cue: " + it["mirror_cue"]["what"])
    for sh in it["shapes"]:
        if sh.get("box_mm"):
            w("- shape %s (%s): box %s, fill %s%s" % (sh["id"], sh["kind"], sh["box_mm"], sh.get("fill"), (" - " + sh["note"]) if sh.get("note") else ""))
        elif sh.get("pts_mm"):
            w("- shape %s (%s): %d points, %s" % (sh["id"], sh["kind"], len(sh["pts_mm"]), sh.get("note", "")))
    for a in it["art"]:
        w("- ART SLOT %s %s: %s. Forbidden: %s. %s" % (a["id"], a["box_mm"], a["describe"], a["forbidden"], a.get("zone_note", "")))
    for b in it["blocks"]:
        hand = (" hand=%s" % b["hand"]) if b.get("hand") else ""
        w("  - `%s` | %s %s | cap %s | %s %s | base %s | %s%s | B %s" % (b["text"], b["font"], b["weight"], fnum(b["cap_mm"]), b["anchor"], fnum(b["x_mm"]), fnum(b["baseline_mm"]), b["ink"], hand, b["contrast"]["B"]))
    if extra:
        w("- " + extra)
    w()


w("### 5.1 The poll-tax set")
w()
w("An INVENTED LOCAL CAMPAIGN (ruling 3 October), `MERIDIAN AGAINST THE POLL TAX` (proposed, not minted): no party, no person, no real group, no real logo. The slogan CAN'T PAY - WON'T PAY is a common slogan (and the title of a 1974 play), not a mark: it is the one phrase a reviewer may want struck. Autumn 1990 is the summons season, so the bills are about meetings, a march and what to do with a summons; DON'T REGISTER, a 1989 slogan, is gone. The sheets carry the legal imprint of a publisher and a printer. Dates: Thursday 25 October (meeting), Tuesday 30 October (advice), Saturday 10 November (march). All weekdays are computed.")
w()
for i in ("P01", "P02", "P03", "P04", "P05", "P06"):
    item_block(i)
w("### 5.2 The chapel hall (the game's `chapel_hall`)")
w()
w("`THE CHAPEL HALL` is the game's own place (`hook-cast.json`, Father Walsh's chapel and its hall); no street is minted for it, so the bills name none. Religion appears as part of life, never mocked: the jumble sale is in aid of the chapel roof fund (the content gate's own permitted sample line speaks of the chapel roof). No raffle, no bingo, no drink (`TEA AND SANDWICHES`), no children (`ALL WELCOME`, never 'families'). The band, THE SANDERLING TRIO, is a placeholder.")
w()
for i in ("J01", "D01"):
    item_block(i)
w("### 5.3 The fights, the market and the goods")
w()
w("THE DRILL HALL is a generic building (proposed). The four ring names are invented placeholders. No odds, no stakes, no prize. The market bill matches `hook-cast.json`: Tuesday, Friday, Saturday, 8 to 4. The two goods are INVENTED brands (WHITEWELL washday powder, QUAYSIDE TEA), proposed, not minted; a cigarette bill is not drawn (a minted brand and the 1990 health-warning wording are both missing).")
w()
for i in ("W01", "B01", "M01", "G01", "G02"):
    item_block(i)
w("### 5.4 The Tivoli")
w()
w("The Tivoli is minted (canon). Its films are invented (THE FOURTH WITNESS, A WEEK AT GULLWING; Gullwing is a minted district); the billing block's studio and three credits are placeholders; the BBFC certificate roundels are real marks and are NOT drawn. The quads' art comes from the image model with no words and no people; our text sits on a dark scrim (T01) or on a pale panel (T02). The Tivoli's own front (plastic letters on a rail, changed on Thursdays) is not this family's.")
w()
for i in ("T01", "T02", "T03"):
    item_block(i)
w("### 5.5 The ferry and the Harbour Board")
w()
w("Both are minted names (canon). The ferry sheet is the WINTER SERVICE from Monday 1 October 1990, pasted over the summer sheet, as the brand bible says; the service is one a single boat could run (15-minute crossings; the check proves it) and its last crossing, 11.00 PM, is the street's own line 'Last crossing's at eleven'. The fares are foot passengers and cycles: no one is a child. The Harbour Board's notices are typed Courier on A4 in a glass case drawing-pinned and curling (the brand bible's own words); its blue and white enamel signs are 600 x 450 on a gate, post or quay edge. Board blue is Judgement: (24,68,140).")
w()
for i in ("F01", "F02", "H01", "H02", "H03", "H04", "H05"):
    item_block(i)
for c in T["cases"]:
    w("#### %s  %s" % (c["id"], c["title"]))
    w()
    w("- outer %d x %d x %d mm, frame left %d, right %d, top %d, bottom %d, window corner radius %d mm; inside %s mm" % (c["outer_mm"][0], c["outer_mm"][1], c["depth_mm"], c["frame_mm"]["left"], c["frame_mm"]["right"], c["frame_mm"]["top"], c["frame_mm"]["bottom"], c["window_radius_mm"], c["inside_mm"]))
    w("- construction: " + c["construction"])
    w("- fixing: " + c["fixing"])
    w("- wear: " + c["wear"])
    w("- pinned inside: " + "; ".join("%s at (%d, %d) mm, %.1f degrees" % (ch["item"], ch["x_mm"], ch["y_mm"], ch["rot_deg"]) for ch in c["children"]))
    w("- placed on %s at u %.2f m, z %.2f m" % (c["place"]["surface"], c["place"]["u_m"], c["place"]["z_bottom_m"]))
    w("- photograph: " + c["photo_proportions"]["note"])
    w()
w("### 5.6 Police and council notices")
w()
w("The police force's name and the council's name are OWED by canon, so neither appears: POLICE, HIGHWAYS DEPARTMENT and the Planning Department are the generic words. A police appeal is an A3 photocopy taped inside a window or sleeved on a column (the one dated yellow appeal board found is from 2007; a 1990 board is a hole). The three samples are slots the simulation can fill (offence line, night, hours): a smashed shop window on Quay Street (matching the 29 September deed), a van stolen from the quay, a man assaulted near the quay. The planning notice is for the empty unit itself (shop to estate agent's office): a mundane hook, struck if the town prefers. The road closure sends traffic via WEIGHHOUSE LANE (minted; the opening at x 21 to 24 is proposed to be it).")
w()
for i in ("C01a", "C01b", "C01c", "C02", "C03"):
    item_block(i)
w("### 5.7 Shop-window cards and the newsagent's board")
w()
w("Cards are hand-lettered in Patrick Hand (felt pen and ballpoint) or printed. Times and prices come from the world: LAST WASH 4.30 PM is an hour before the laundry's closing (8 to 5.30, `hook-cast.json`); BACK AT with hands at 12 is the end of Hal's Monday break (11 to 12); cod 2.70 a lb is the ONS 1990 range (2.42 in January, 2.85 in December); the fish market's other prices and the 20p-a-week advertising rate are Judgement. No card names a child, a pet shop, a drink, a pool or a lottery; no 'model' or 'companion' cards (tart cards are a content-rule line). Telephone numbers are the local six-figure form 960 xxx (the fictional range the cast's own 0632 960418 uses); none is Mickey's.")
w()
for i in ("K01", "K02", "K03a", "K03b", "K04", "K05", "K06a", "K06b", "K06c", "K07a", "K07b", "K07c", "K07d", "K08", "K09a", "K09b", "K09c", "K09d", "K09e", "K09f"):
    item_block(i)
w("**The newsagent's board SB1** (760 x 560 mm on the glass at u 1.95 m, z 0.90 m): fifteen cards of two sizes (127 x 76 record cards, 148 x 105 postcards), taped inside the glass.")
w()
w("| Card | at (x, y) mm | size | rot | fixing |")
w("|---|---|---|---|---|")
for c in T["card_board"]["cards"]:
    w("| %s | %.0f, %.0f | %d x %d | %.1f | %s |" % (c["item"], c["x_mm"], c["y_mm"], c["w_mm"], c["h_mm"], c["rot_deg"], c["fixing"]))
w()
for i in [x for x in ITEMS if x.startswith("SA")]:
    item_block(i)

# ------------------------------------------------------------------ 6 letting boards
w("## 6. \"To Let\" boards (unit 4.3)")
w()
w("The agent is PROPOSED: **ARMITAGE & STOBBS, Chartered Surveyors, Estate Agents** (not minted; a placeholder never to reach his page; not checked against real firms, the network refusing the sources). A no-agent variant keeps the number. The number is the local six-figure form 960 335. The existing board (`board_to_let.png`, 900 x 450, PT Sans, no agent, no number) is replaced. 450 mm is the height a 0.55 m fascia takes with 50 mm clear above and below, and 1200 mm gives the agent's band, TO LET at cap 150 and the number their room; area 0.54 square metres, well under the 2.0 square metres a board could be in the 1984 regulations (a Lead from a search summary; the exact figure and the later cut are not read). A letting board is white gloss on 18 mm exterior plywood, corners rounded 4 mm, the cut edges painted, a 25 x 18 mm batten at each end, four 8 mm dome-head coach screws 40 mm in from the corners with a rust run 40 to 140 mm under each lower one, hung 2 degrees askew. Colours: agent navy (28,46,94), red (178,34,40), white (236,236,230); at class D the white yellows to (214,206,184) and the red fades towards chalk-pink by 0.3. Fonts: Jost (Futura-like, the estate agents' and chemists' 1980s face, asset-plan table).")
w()
for i in ("L01", "L02", "L03", "L04"):
    item_block(i)
    m = ITEMS[i]["mount"]
    w("- mounted on: %s; centre street x %s m; z %s to %s m; %s; askew %s degrees. %s" % (m["surface"], m["centre_street_x_m"], m["z_bottom_m"], m["z_top_m"], m["screws"], m["askew_deg"], m.get("note", "")))
    w()

# ------------------------------------------------------------------ 7 plates
w("## 7. Street name plates (unit 4.4)")
w()
w("**What 1990 British plates carried, as far as I could establish.** No photograph was reached. From search summaries (Leads): there was never a national design and each council chose its own style, colour, size and material; black capitals on white with a black border was the default the 1993 Department of Transport circular recommends and the usual look; the Ministry of Transport's alphabets date from the early 1930s, the Kindersley lettering was adopted in 1951 and recommended in 1952; Hull's cast plates of the 1920s to 1930s were black on white and their paint faded or flaked; London plates carried the borough and the postal district; councils often added a crest or their name; I found NO source that provincial plates of the 1980s carried a postal district, and the project's earlier street-clutter note lists postcodes as wrong for 1990. **What I chose (Judgement):** the street's name in capitals; below the top border a small line with the DISTRICT's name (THE HOOK, COPPER ROW, IRONSIDE: canon's minted districts); no council, no crest (canon owes the council's name); no postcode by default. Variant `n` drops the district line; variant `p` adds a placeholder postal district MR1 at the left of the district line (MR is not a real UK postcode area; never on his page). **Letter style:** Marcellus SC capitals, 90 mm tall, tracking +0.04 em, ruled on 30 September for the street plates (it stands in for the Kindersley serif, which has no allowed free version); the ruling beats the earlier note and the Hull caption (whose plates used the older MOT sans alphabets), see section 11.")
w()
w("**Sizes.** Plate length follows the name: ink width plus 2 x 62 mm (6 mm edge + 12 mm border + 44 mm clear), rounded up to 10 mm. Depth 170 mm without a district line and 225 mm with one; Quay Street's are 190 and 240 because the Q's tail dips 36 mm below the baseline. The border band is 12 mm, 6 mm in from the edge; corners rounded 6 mm. Fixing: four screws 30 mm in from the corners (10 mm dome heads into fibre plugs; the cast plate has four 12 mm holes cast in). Mounting height: bottom edge at 2.5 m, centre 2.63 m (the earlier note says 2.2 to 2.5 m, the existing plate hangs at 2.50 to 2.76).")
w()
w("**Materials by street (Judgement).** QUAY STREET: cast iron, raised letters and border 4 mm proud on an 8 mm face, painted white with black letters, repainted over the years, the paint flaking first from the raised edges to grey iron and a thin rust film (the Hook is the old port, and its plates are the oldest). WEIGHHOUSE LANE: die-pressed aluminium 2 mm, letters raised 1.5 mm, stove enamel, rolled edge. TANNERY ROW: vitreous enamel on pressed steel, rolled edge.")
w()
w("| Plate | street | district | variant | plate (mm) | ink width | material |")
w("|---|---|---|---|---|---|---|")
for it in T["items"]:
    np_ = it.get("name_plate")
    if np_:
        w("| %s | %s | %s | %s | %d x %d | %s | %s |" % (it["id"], np_["street"], np_["district"] if np_["variant"] != "n" else "(none)", np_["variant"], it["format"]["w_mm"], it["format"]["h_mm"], np_["ink_w_mm"], np_["material"]))
w()
w("Placed: **S01d** at street x 20.47 on the west corner pier (x 19.92 to 21.0, brick to 3.12 m: the existing plate's place, kept, 80 mm of pier either side), centre z 2.63; **S01d** again on the quay gable, centre 1.0 m from the front corner, z 2.63; **S02d** (WEIGHHOUSE LANE) on the near flank of the first shop beyond the side opening (the x = 24.0 wall, facing -x), centre 0.9 m from its front corner, PROPOSED because canon does not name the opening. **S03** (TANNERY ROW) is a town kit plate and is not placed on Quay Street. The plate board's pictures: `L4` shows all nine.")
w()
for i in [x for x in ITEMS if x.startswith("S0")]:
    it = ITEMS[i]
    w("#### %s  %s" % (i, it["title"]))
    w()
    for b in it["blocks"]:
        w("  - `%s` | %s | cap %s | %s %s | base %s | B %s" % (b["text"], b["font"], fnum(b["cap_mm"]), b["anchor"], fnum(b["x_mm"]), fnum(b["baseline_mm"]), b["contrast"]["B"]))
    w()

# ------------------------------------------------------------------ 8 paste plan
w("## 8. The paste plan: placements")
w()
w("Layers run from the oldest (0) to the newest; age class A to D is the paper's age. The gable's bills are laid by a seeded packer (seed %s) and kept only if every older bill keeps its share of face (layer 0 at least 0.30, layer 1 at least 0.45, the top layer all of it). The builder may re-seed; the rule must hold." % T["placements"][0].get("seed"))
w()
w("| Surface | Item | where | z bottom (m) | rot | layer | age | size (m) |")
w("|---|---|---|---|---|---|---|---|")
for p in T["placements"]:
    where = ("u %.2f" % p["u_m"]) if p.get("u_m") is not None and p["surface"] in ("SF1", "SF2", "SHOP") else ("street x %s%s" % (p.get("street_x_m"), (" pier " + p["pier"]) if p.get("pier") else ""))
    if p["surface"] == "SHOP":
        where = "%s %s u %.2f" % (p["shop"], p["where"], p["u_m"])
    w("| %s | %s | %s | %.2f | %s | %s | %s | %.3f x %.3f |" % (p["surface"], p["item"], where, p["z_bottom_m"], p.get("rot_deg"), p["layer"], p["age_class"], p["w_m"], p["h_m"]))
w()

# ------------------------------------------------------------------ 9 words
w("## 9. The words, as a list")
w()
w("%d approved strings (`approved_words`), %d tokens (`approved_word_parts`). Every string is ours. Checked against: this file's forbidden lists (alcohol, gambling, children, real marks, names canon owes, things after 1992); `tools/content-gate.py`'s %d speech rules; `RealWorld.cs`'s names; imagegen's forbidden tokens; canon's streets and districts; the cast's surnames. **Proposed, unminted names** (placeholders, never on his page):" % (len(T["approved_words"]), len(T["approved_word_parts"]), N_RULES))
w()
for p in T["proposed_names"]:
    w("- `%s`: %s (mint: %s)" % (p["name"], p["what"], p["mint"]))
w()
w("Names canon owes and this target therefore does NOT use: the football club, the local paper, the pirate radio station, the regional television channel, the telephone operator, the postal cypher, the council's name. The brand bible v1 carries proposals for four of them (Meridian Town AFC, The Meridian Argus, Radio Tideline, Coastway Television); canon.md still lists them as owed, so none is drawn here.")
w()

# ------------------------------------------------------------------ 10 variants
w("## 10. Variants the street needs")
w()
tot = sum(it["variants"].get("n", 1) for it in T["items"])
w("%d seeded variants over 76 items (a poster is built once, shown in the variants its entry names; nothing is multiplied before one complete sample is approved in the assembled game, CLAUDE.md). The variants differ in: age class (always), skew, ink registration and density, which corner is torn or lifting, tape and pin positions, the second pass's shift, and the hours-driven face (OPEN or CLOSED, the BACK AT hands, the LAST WASH hour). The three police sheets are slot fillers: the same layout with another offence line. Dates move with the calendar: every event bill gives its date as computed words, so a build for another date in 1988 to 1992 re-computes the weekday (`G.dates`)." % tot)
w()

# ------------------------------------------------------------------ 11 disagreements
w("## 11. Where photographs, books and the ruling disagree, and what I chose")
w()
for d in T["disagreements_photographs_win"]:
    w("- **%s.** Wins: %s. Against it: %s. Chosen: %s" % (d["topic"], d["wins"], d["others"], d["choice"]))
w()

# ------------------------------------------------------------------ 12 checks
w("## 12. The checks")
w()
kinds = {}
for c in T["checks"]:
    kinds.setdefault(c["id"].split(".")[-1] if "." in c["id"] and not c["id"].startswith("G.") else c["id"].split(".")[0], 0)
    kinds[c["id"].split(".")[-1] if "." in c["id"] and not c["id"].startswith("G.") else c["id"].split(".")[0]] += 1
w("%d checks in `target.json` (`checks`). Per item: `.size` (image size), `.words` (the manifest equals the approved strings), `.pos` (each block's ink box read off the pixels, widened 8 mm along the line and 3 mm up and down, pixels explained by another block's glyphs not counted), `.cap` (letter heights at scale: the cap read off flat-bottomed capitals within a stated fraction, and `cap_px` = cap x px/mm), `.mask` (the block re-rendered from its font compared with the ink pixels: F at least 0.90 for printed lines, 0.85 for small print and typing, 0.78 for hand lettering, 0.55 for imprints), `.contrast` (WCAG on the aged render, class B: not under max(2.2, min(3.0 for caps of 12 mm and over or 4.5 below, 0.9 x nominal))). Global: `G.words.approved`, `G.forbidden`, `G.dates`, `G.mirror`, `G.mirror.cues`, `G.fonts`, `G.proposed`, `G.ferry.schedule`, `G.tides`, `G.place.*`, `G.letting.mount`, `G.plates.*`." % len(T["checks"]))
w()
w("**The checks are tested** (`self_check.py`, group 10) on reference renders of thirteen items: the true render passes every mask and position check; a MIRRORED render fails at least 80 per cent of the blocks whose glyphs can tell; a render shifted 30 mm fails the position check on at least 90 per cent of blocks; the wrong font on the largest block fails its mask check. **A hand-lettered, centred card cannot be told from its mirror by its words** (the in-place flip scores within 0.15) and its font cannot be told within the hand's jitter: the 29 all-hand cards carry an asymmetric cue instead (`mirror_cue`: tape at one corner, a pin hole, a torn corner), and `G.mirror.cues` checks it.")
w()
w("The reference reader is in `self_check.py` (functions `read_pixels`, `read_score`, `read_box`); the builder's own checker should do the same on its rendered item.")
w()

# ------------------------------------------------------------------ 13 could not settle
w("## 13. What the target could not settle")
w()
for s in T["could_not_settle"]:
    w("- " + s)
w()
w("Unreached today: " + "; ".join(T["unreached"]) + ".")
w()

# ------------------------------------------------------------------ 14 self check
w("## 14. Self-check")
w()
if sc:
    w("Run %s: **%s**." % (sc.get("run"), sc.get("summary")))
    w()
    if sc.get("failures"):
        w("Failures:")
        for f in sc["failures"]:
            w("- [%s] %s: %s" % (f["g"], f["n"], f["d"]))
        w()
    w("Reported (not failures):")
    for r in sc.get("reported", []):
        w("- [%s] %s %s" % (r["g"], r["n"], ("(" + r["d"][:140] + ")") if r["d"] else ""))
else:
    w("(run `self_check.py` and then `make_doc.py` again to fill this in)")
w()

# ------------------------------------------------------------------ 15 sources
w("## 15. Sources")
w()
w("| Id | Kind | What | Read | Author and licence | Used |")
w("|---|---|---|---|---|---|")
for s in T["sources"]:
    w("| %s | %s | %s | %s | %s; %s; taken %s | %s |" % (s["id"], s["kind"], s["url"][:260].replace("|", "/"), s["read"], s["author"], s["licence"], s["taken"], s["used"].replace("|", "/")))
w()
w("The licences of the previews: P1 is a crop of a CC0 panorama with the glazed interiors painted out; the layout sheets are our own drawings. No preview shows a business's name, a drink, a gambling mark or a person.")
(HERE / "TARGET.md").write_text("\n".join(out) + "\n", encoding="utf-8")
print("wrote TARGET.md", len("\n".join(out)), "bytes")
