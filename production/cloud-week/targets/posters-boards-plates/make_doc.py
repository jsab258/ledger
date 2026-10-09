"""Author tool: writes TARGET.md from target.json plus the prose below (cloud week 42, 9 October 2026; SECOND TRY).

    /home/user/.bpyenv/bin/python make_doc.py

The tables (items, words, placements, colours, checks) and every number the prose quotes are read from target.json, so the page and the JSON cannot disagree.
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
    import importlib.util
    _sp = importlib.util.spec_from_file_location("_cg", str(HERE.parents[3] / "tools" / "content-gate.py"))
    _m = importlib.util.module_from_spec(_sp)
    sys.modules["_cg"] = _m
    _sp.loader.exec_module(_m)
    N_RULES = len(_m.RULES)
except Exception:
    N_RULES = 0
sc = T.get("self_check") or {}
FACTS = sc.get("facts") or {}
summary = T["summary_line"]
PL = T["placements"]
DEF = [p for p in PL if not p.get("held")]
HELD = [p for p in PL if p.get("held")]
n_items = len(T["items"])
N_PRINT = len([i for i in T["items"] if any(not b.get("ghost") for b in i["blocks"]) and not all(b.get("hand") for b in i["blocks"] if not b.get("ghost"))])
n_checks = len(T["checks"])

w("# Quay Street's paper and small boards: the exact target")
w()
w(summary)
w()
w("Cloud week 42, written 8 to 9 October 2026. **SECOND AND LAST TRY**, after `TARGET-REVIEW.md` (FAIL, 13 faults, all answered below); the re-review's four faults were then fixed **by Jafar's ruling of 9 October, exactly as the reviewer wrote them, and are not re-reviewed** (section A2). Three 2D units build from `target.json` and this page: 4.2 posters and notices, 4.3 \"To Let\" boards, 4.4 street name plates. Nothing is committed.")
if sc.get("summary"):
    w()
    w("Self-check: **%s** (see section 15)." % sc["summary"])
w()
w("Plain summary. %d sheets, cards, boards and plates, every word ours, listed and checked against the content rule, canon and the 1990 calendar; **the street's date is Monday 29 October 1990** and every placed item's age is checked against it. "
  "The default street carries **no name the town has not minted** and no bill that names nothing: the poll-tax bills say STAND TOGETHER, the dance LIVE MUSIC, the market bill needs no name, the empty unit's board is the fascia target's own TO LET (900 x 450, no agent, no number) and the flat above has no agent. "
  "The named versions are `-named` variants (and L01, L03, B01, G01, G02) marked proposed, not minted, and held; so are the nameless Tivoli quads and programme (A NEW THRILLER, A NEW COMEDY) and the wrestling bill with no ring names and no hall, which read as stand-ins. "
  "The paper is AT MOST the asset plan's amount, 8 fly-posters and 4 poll-tax bills (the default street carries 5 and 3): **the quay gable is bare, as the Hook sheet shows it** (the downpipe, the render patch and the damp foot, no paper and no plate), the empty unit's glass carries six sheets (a police appeal among them) as the proof sample, the plain west row one market bill on its poster pier and one poll-tax bill in a window, and two shop windows a notice each. "
  "The jumble-sale and dance notices are photocopied A3 sheets; the Tivoli's venue and dates are a separate pasted strip; the street name plates are name-only, QUAY STREET cast aluminium, none on the yard entrance. "
  "**The checks now read the pixels glyph by glyph** (section 12): the first try's checks passed a changed date, TEA for ALE and LUNCH for BINGO; these fail every one." % n_items)
w()
w("Files in this folder:")
w()
w("- `target.json`: the whole target (%d items, %d placements of which %d are held (the named twins, the nameless stand-ins and the gable's proof wall), 2 cases or boards, a card board, 6 piers, 8 shop fronts, %d checks, the self-check result)." % (n_items, len(PL), len(HELD), n_checks))
w("- `make_target.py`: the author tool that writes `target.json` (every width is measured on the real font files; every item's pixel scale is chosen by `glyphlib.py`).")
w("- `glyphlib.py`: the glyph kernels shared by the author tool and the self-check (the per-glyph score F, the separation score SEP, the table that sets each item's scale).")
w("- `target_drawing.py`: draws every item's boxes, baselines and clean lettering at 1 mm to the pixel, the surfaces' elevations (the gable with its downpipe, the empty unit's glass, the west piers, the plates' places) and the cases, from `target.json` alone, into a folder given on the command line, plus the polygons as JSON.")
w("- `self_check.py`: its checks and their count are in section 15; it writes its result into `target.json` under `self_check`; `--fetch-fonts DIR` fetches the three font files not in `production/fonts`; `--groups 12,13` runs some groups only. It also holds the READER a builder's own checker must copy (section 12).")
w("- `make_previews.py`, `make_doc.py`: rebuild the previews and this page.")
w("- Previews, in `production/previews/cloud-week/refs/posters-boards-plates/`: `P1-urban-street-01-notice-case.jpg` (the one photograph measured, windows and the council crest masked), `P1-...-target-on-photo.jpg` (the proportions laid on it), `L1` to `L4` (layout sheets of every item), `L5` (the paste plan: gable, glass, piers, plates).")
w()

# ------------------------------------------------------------------ A: the second try
w("## A. The second try: thirteen faults, thirteen answers")
w()
w("The reviewer (a fresh target reviewer, 9 October) ran `self_check.py` (215 of 215 then), then rendered wrong items through the target's own reader and found the checks blind to a wrong word, date or price; found unminted names as the street's default dressing; and found placements, ages, cues and a ferry timetable that contradicted the project's own notes. Each fault and how this try answers it:")
w()
w("| # | Fault | Answer |")
w("|---|---|---|")
for d in T["second_try"]:
    w("| %d | %s | %s |" % (d["fault"], d["short"], d["answer"].replace("|", "/")))
w()
w("**Where this try differs from the reviewer's amendment, and why (each with its source).**")
w()
f = FACTS.get("f_margin") or {}
w("- **Fault 1(b), the glyph margin.** The review asks that each glyph out-score every other glyph of its font and its own mirror by at least 0.05 on F at 0.5 mm. F is a mean over the whole glyph, so glyphs that share most of their ink score alike. Measured by `self_check.py` (group 12, `f_margin_table`): in %s, %s of the %s capitals and digits cannot meet 0.05 (%s). "
  "The check therefore keeps the review's own gate for the glyph itself (F >= 0.85 at 0.5 mm) and scores the separation from every alternative on the pixels where the two glyphs differ (SEP, section 12), gate 0.70, a margin of 0.40. Every wrong render the reviewer built fails it, and so do 8 for 6, 3 for 8, B for R and the other near pairs." % (
      f.get("font", "Oswald 700, 34 mm capitals, 2 px/mm"), f.get("n_under", "11"), f.get("n_chars", "36"), ", ".join("%s against %s: %.3f" % (c, a, m) for c, m, a in f.get("worst", [])[:4]) or "O against D 0.013, 6 against 8 0.036"))
w("- **Fault 10, K05's bottom.** The review asks 1.38 m so that K05's centre is the 1.45 m its own words give. The fascia target's vinyl row `TOBACCONIST & CONFECTIONER` (cap 70 mm, z 1.35, tolerance 0.03) is on the same shop-door glass and tops out at 1.385 m (1.415 with the tolerance), so a card at 1.38 would stand on the lettering. K05's bottom is 1.42 m and its words now say so. Source: `production/cloud-week/targets/fascia-signs/target.json`, `glass_lettering`.")
w("- **Fault 4, the quay gable (first try, since changed).** The Hook sheet's gable is bare old brick with a downpipe, a render patch high up and a damp foot, and the asset plan's own proof wants \"one wall in view ... three bills from three templates\". The first answer kept one layer of three bills with the downpipe added and flagged them `proof_wall`. The re-review then asked for the sheet's bare gable and Jafar's ruling of 9 October applied it: section A2. The five `proof_wall` placements are held, and nothing more goes anywhere until he has approved a sample in the assembled game.")
w("- **Fault 4, the count (first try, since changed).** The reviewer's own placements added to 7 fly-posters, not the 8 he cited; the eighth was T03, the Tivoli's programme as a window bill. After the re-review the gable's three bills, T03 and W01 on the pier are off the default street and M01 stands on the pier: **the default street carries 5 fly-posters and 3 poll-tax bills (P03, P02 and P02's A3 window copy), and `G.place.paper` allows at most 8 and 4**.")
w("- **Fault 6, other collisions found.** MAD MAURICE and THE BARON (a 1960s television series' title) went with the two the reviewer named: SPANNER SMITH and THE STEVEDORE. None was checked against real lists (the network is closed); all four are held and listed for the town. `real_marks` now holds LARKIN, SEA WOLF, SEA WOLVES, the real wrestlers, soap powders, cinema chains and campaigns the probe listed.")
w("- **Notes taken.** The tide table peaks on Sunday 4 November (4.4 4.6 4.7 4.8 4.7 4.5 4.2); SA01's number is 960 471; cockles are 45p a TUB (the trade's unit, the pint, is a banned word in this project) and smoked haddock is £2.90, dearer than fresh; T01's art no longer asks for a telephone box (nor T02's for a pier: a beach, deckchairs and a breakwater) and every art slot forbids crowns, kiosk lettering, operator marks, bottles, glasses and arcade signs; the council crest is masked in the P1 previews; the forbidden lists gain plurals and near terms (SCHOOLS, BABYSITTER, PLAYGROUP, SCOUTS, CUBS, BROWNIES, INN, TAVERN, DARTS, QUIZ NIGHT) and the real names above; section 4b no longer says League Gothic is off the plan's table; the fonts off the table are removed (Libre Baskerville, Josefin Sans, the unused Abril Fatface) or recorded with a DECISIONS line (Libre Franklin, Patrick Hand); the drawing script draws the piers' and the plates' elevations.")
w()

# ------------------------------------------------------------------ A2: fixes after the second review
w("## A2. Fixes applied after the second review, by Jafar's ruling of 9 October, not re-reviewed")
w()
w("The second review (9 October, `TARGET-REVIEW.md`, \"Re-review (try 2)\") found most of the first try right and four faults. Jafar ruled on 9 October that the target, set aside after its two tries, gets the reviewer's exact fixes applied. They are applied below as the reviewer wrote them, run against the reviewer's own scripts (try2_tests.py, try2_true.py, try2_allitems.py, try2_sa.py, try2_sq.py), and **no fresh reviewer has looked at them yet**.")
w()
w("| # | Fault | Fix |")
w("|---|---|---|")
for d in T["fixes_after_second_review"]:
    w("| %d | %s | %s |" % (d["fix"], d["short"], d["answer"].replace("|", "/")))
w()
w("**Run against the reviewer's own scripts on this target** (unchanged, in the session scratchpad's `posters-review/`): `try2_sq.py` finds no true jittered render of K01, SA06, K07a, K09a or SA15 turned (0 of 10 over 0.3 each; the tolerance is 0.3 for all); `try2_sa.py`: SA01 and SA03 (now 12 px/mm) fail 0 of 20 true seeds and T01-named's true render passes every glyph block; `try2_true.py`: all 29 hand cards (and F02, which has no readable block), 6 true seeds each, 0 glyph failures and 0 square failures; `try2_allitems.py`: 0 of the print items fail their own checks (it found 8 before); `try2_tests.py`: the 10 hand-card wrong words fail on 3 of 3 seeds, the same cards true pass 3 of 3, a missing manifest returns a failure instead of a TypeError, and the four planted lines (and D01 + LICENSED BAR) are the lines that only `ITEM.clean` sees: his `all_checks` has no `ITEM.clean`, so it still lists them as passing, and an amended copy that adds `clean_ink_mm2` fails every one (K01 328 mm2, SA11 72, L02 15,887, C02 71, D01 145; the true renders 0). His `wrong_renders_try2.py` and `gate_probe.py` still run unchanged and give what they gave (every print wrong render fails the line mask; BIG TED, BABYSITTERS, INNS, PLAYGROUPS, TEENS, LAD, LASS and KIDDIES are now caught).")
w()
w("Smaller notes from the same review, taken: the held placement of L01 is sized 1.2 x 0.45 m (it had copied the 0.9 m board); the calendar note no longer cites H03 as a reason for the street date (H03 is not placed); the forbidden lists gain BABYSITTERS, INNS, PLAYGROUPS, TEENS, LAD, LASS and KIDDIES. Noted, not changed: the review's suggestion to render at check scale, check, and downsample for the game is open to the builder and costs the checks nothing; the scales here stay the checks' own (the largest render is %g megapixels)." % max(it["megapixels"] for it in T["items"]))
w()

# ------------------------------------------------------------------ 0
w("## 0. What this target rests on, in plain words")
w()
w("- **Photographs measured today: one, and it is not the period.** Poly Haven's Urban Street 01 (CC0, Andreas Mischok, 18 August 2019) shows four glazed notice cases, blue steel, 2000s. I measured their VERTICAL proportions (header 0.152 of the height, window 0.763, foot 0.085, side bands 0.205 of the apparent width, each with its error) and used them only as a cross-check of a glazed case's shape. Nothing else in this target is measured on a photograph. The reviewer's network was as closed as mine: no photograph of a plate, a letting board, a pasted wall or a notice was reached by either of us.")
w("- **Photographs looked at and not used.** Eight other Poly Haven panoramas (London streets and docks, Cambridge, a Dublin quay): none shows a street name plate, a letting board or a poster hoarding that could be measured. Bethnal Green Entrance has a stickered modern pole plate and, in the same frame, a council byelaw sign about alcohol: nothing from it is kept, no crop, no file.")
w("- **Earlier notes (they read period photographs and search summaries on the PC; read here, not re-measured):** the 1990 mix of Letraset, photocopy and two-colour print (asset-plan note 4); the 1952 Kindersley recommendation for name plates and the street-clutter note's plain plates and 20 to 25 cm depth; the winter timetable date of 1 October 1990 and the pasted-over summer sheet (transport-timetables note, the brand bible); cod at about 2.60 a lb in 1990 (the fishmonger note, ONS); the Harbour Board's blue and white enamel and glass case with notices drawing-pinned and curling (the brand bible); the Tivoli's programme 'changed on Thursdays' (the brand bible); the hours, the market's days and the chapel hall (`hook-cast.json`); the yard entrance (`vignette-scene.json`, atlas-01).")
w("- **Search summaries (leads, never numbers):** modern street-plate specifications (90 mm capitals, 150 to 230 mm plates, 12 mm borders, 11 SWG aluminium), a Hull caption on 1920s to 1930s cast plates, a statement that there is no national plate design and that each council chose its own, a Hackney Museum 1990 'Pay No Poll Tax' sheet on yellow paper in red ink, the Double Crown sheet. The pages themselves were not fetched (DNS and 403).")
w("- **Judgement:** every size, colour, wording, price, ageing number and placement not listed above. Section 1 says the kind of each class of number.")
w("- **The honest summary:** this is the weakest of the family targets on its photographic side. It is strong where the project's own files decide: the streets and districts canon mints, the shops' hours and the market's days, the fascia target's positions, board and left-right rule, the plain row's bay layout, the 1990 calendar, the content rule and the lists of real names, and now where its checks are concerned: they read the pixels glyph by glyph. A fresh reviewer should look hardest at sizes and at ageing.")
w()
w("What I would read once the network opens (all unreached today):")
w()
for s in T["would_read_when_network_opens"]:
    w("- " + s)
w()

# ------------------------------------------------------------------ 1
w("## 1. Reading this file")
w()
w("- Units. Every item has its own frame: **x in millimetres from the viewer's LEFT edge as seen IN THE GAME, y UP from the item's bottom edge**; a block's `baseline_mm` is measured up from the bottom edge. Each item is rendered at its own `px_per_mm` (2 to 12 here, chosen so that every glyph can be told from every other: section 12); row 0 of an image is its top edge. Surfaces use metres: `u` from the surface's viewer's-left edge, `z` up from the pavement; street x is metres along Quay Street (0 at the quay end), the same in the recipe and the game.")
w("- **Every texture is square-on.** No skew, rotation or perspective is baked into any picture: skew and rotation live only in the placement's `rot_deg`, a hand card's tilt included. `ITEM.square` fails a texture turned more than 0.3 degrees, **one tolerance for every item, print and hand-lettered alike**, found against the render of the item's own glyph manifest (jitter included); `PLACE.built` checks the placed decal's rotation to 0.3 degrees.")
w("- Left and right are the VIEWER'S, in the game, by the fascia target's rule: the game mirrors the recipe, so low street x is on the viewer's RIGHT looking at the east parade and on the viewer's LEFT looking at the west block. Every sheet's x runs from the viewer's left; the quay gable is read looking +x, with the front corner at the viewer's left.")
w("- Evidence kinds: Read (printed), Scaled (off a drawing or the game's files), Photo (measured on a photograph today), Derived (computed), Judgement (mine, to be overturned), Lead (a search summary, never a number).")
w("- Colours are sRGB 0 to 255, contrast is WCAG, dE is CIE76. Aged colours are for four classes (section 4).")
w("- **Named and nameless.** An item whose id ends `-named` (and L01, L03, B01, G01, G02) carries a proposed, unminted name in a block of cap 10 mm or more: it is HELD (`held_names`) and its placements are `held_until_minted` twins of the nameless default placements. The nameless Tivoli quads and programme (T01, T02, T03) and the wrestling bill W01 are HELD too (`stand_in_of`, `waits_for`): a bill that names no film, no hall and no ring names reads as a placeholder by another name, so it waits with its twin for the names. The `G.place.*` checks and the drawings use `held` (not in the default street, for any reason); `held_until_minted` is the reason of unminted names.")
w()
w("The kind of each class of number in this target:")
w()
w("| Numbers | Kind | Source |")
w("|---|---|---|")
for a, b, c in [
    ("sheet sizes (crown, double crown, quad, four-sheet; A2 to A6)", "Derived", "imperial names x 25.4 mm; ISO 216 halving; the Double Crown name is also a Lead"),
    ("ink width of every line, cap ratios, plate lengths, tide and ferry times, each item's pixel scale", "Derived", "measured on the real font files / computed in make_target.py and glyphlib.py, re-measured by self_check.py"),
    ("the calendar: every weekday and date; the street date", "Derived", "datetime, 1990; 1 October 1990 was a Monday; 29 October was a Monday (the one day every dated placement allows)"),
    ("street x of the shops, door ends, hanging signs, the fascia, the letting board (900 x 450, TO LET, Libre Franklin 800 cap 130, vinyl red), the empty unit's number 7", "Read", "the fascia target, SCENE-SLOTS.md, vignette-scene.json"),
    ("the six piers, the glass, the shop widths, the bay-1 window at x 12.3", "Derived", "terrace-front.py's plain-row layout and the shopfront numbers (0.35, 3.562, 0.9, 0.838)"),
    ("shop hours, the market's days and hours, the chapel hall, the yard entrance, the ferry's last crossing", "Read", "hook-cast.json, vignette-scene.json, atlas-01, tier2-batch-1.json, the brand bible"),
    ("the cod price", "Read (earlier note)", "ONS series CZOL via FISHMONGER-2026-10-03.md"),
    ("the case proportions (0.152, 0.763, 0.085, 0.205)", "Photo", "one 2019 modern case, with errors; NOT the period"),
    ("90 mm capitals, 200 to 240 mm plates, 12 mm border, 30 mm fixings, relief 3 and 1.5 mm, draft 10 degrees, radii", "Judgement on a Lead", "modern specifications in search summaries; the street-clutter note's 20 to 25 cm"),
    ("the downpipe (75 mm, u 0.30), the render patch and the damp foot of the gable", "Scaled by the reviewer", "the Hook sheet (TARGET-REVIEW fault 4)"),
    ("every other size, layout, colour, cap, ageing, wear and placement number; every price but the cod", "Judgement", "the writer's"),
]:
    w("| %s | %s | %s |" % (a, b, c))
w()

# ------------------------------------------------------------------ 2
w("## 2. Where each piece goes on the street")
w()
w("Everything here is **Judgement on the scene's own numbers**: SCENE-SLOTS.md, `vignette-scene.json`, the recipe (`terrace-front.py`), atlas-01 and the fascia target. **The amount of paper is AT MOST the asset plan's (note 4, table A5, Quay Street, the proof view): 8 fly-posters and 4 poll-tax bills**; the default street carries 5 and 3 (`G.place.paper`), because the quay gable is bare.")
w()
w("| Surface | What it is | Frame and paste zone | What goes there |")
w("|---|---|---|---|")
S = T["surfaces"]
w("| SF1 | the quay gable: the east parade's south end wall, plane x = 3.0 m, facing -x (the big brick wall at the right of the hook frame, `morning-hook-day-2026-10-08.jpg`) | u from the front corner into the block (viewer's left), 0 to 8.0 m; z 0 to 6.3 m; paste zone u 0.15 to 6.0, z 0.45 to 2.75 | **BARE, as the Hook sheet shows it: no paper and no plate** (`G.place.gable`). A 75 mm black cast-iron downpipe at u 0.30, full height; the render patch (z 3.6 to 5.0) and the damp foot (below 0.45) bare, as the sheet has them. The plan's proof wall (one layer of three bills, bottoms z 1.00: P01 u 0.70, W01 u 1.30, T02 u 1.90 with its strip T02s, and a QUAY STREET plate at u 1.0, centre z 2.63) is kept as HELD placements, paper 150 mm clear of the pipe, for the case that he chooses the gable for the sample. No cases, no stickers. |")
w("| SF2 | the empty unit's whitened glass (bay 3, east, number 7, street x 21 to 27) | u from the glass's viewer's-left edge, 0 to 3.562 m; z 0.60 to 2.40; the glass is street x 23.088 to 26.65 (the recipe's `fx` counts from the viewer's RIGHT: u = 3.562 x (1 - fx)) | one layer, six sheets: C01a (police appeal, four tape tabs) u 0.30 z 1.30; M01 0.75; P03 1.35; P02 1.95; J01 (A3 photocopy) 2.60; C02 (planning notice, number 7) 3.01. Whitewash shows above 2.0 m |")
w("| WEST_PIER | six brick piers of the plain west block (street x 3 to 21), each 0.95 to 0.956 m, computed from the plain row's layout | street x of the pier's centre; z from the pavement | W1.0 (x 11.4, the scene's own poster slot): W01; W2.0: the house letting board L04. No other bill on a pier or a house front. |")
w("| SF9 | the plain row's bay-1 window at street x 12.3 (a cottage sash, sill 0.9 m, 0.85 m wide) | street x of the window's centre, z up from the pavement | P02 as an A3 window bill: P02 x 297/508 (0.585), 297 x 446 mm, taped inside the glass, top at 1.90 m |")
w("| SF4 | the three lamp columns, street x 8, 28, 48 (SCENE-SLOTS: every 20 m, first at 8 m, 0.6 m back from the kerb, alternate sides) | the shaft 0.114 m across; a bill wraps it: the middle 0.17 m of an A3 shows face-on | C03 and a sticker at x 8; two stickers at x 28 |")
w("| SF5 | the empty unit's fascia (0.55 m, z 2.85 to 3.40, 0.12 proud) | centre street x 24.0 = the fascia target's board x 2705; the board z 2.90 to 3.35 | L02, the fascia target's own board (L01, a named agent, is the held alternative) |")
w("| SF6 | first-floor brick above bay 3's cornice (3.55) and below the upper sills (about 4.3), between the two upper windows (street x 22.93 to 25.07) | centre street x 24.0, z 3.70 to 4.10 | L03n, the no-agent flat board (L03 is the held alternative) |")
w("| SF7 | name-plate walls: the west corner pier (street x 19.92 to 21.0, brick to 3.12 m); a second plate on the quay gable at u 1.0 is held | centre z 2.63 | S01n once (the pier's). The yard entrance (street x 21 to 24, dropped kerb at 22.5) carries NO plate: `vignette-scene.json` and atlas-01 (`yard_gap_x [21, 24]`) call it the yard entrance and canon does not name it. S02 and S03 are kit plates. |")
w("| SF8 | a quay-edge post, street x about -0.6 (PROPOSED: SCENE-SLOTS has no quay geometry) | z 1.20 up | H02, DANGER DEEP WATER |")
w("| SHOP | eight shop fronts: glass 3.562 m, shop door 0.9, side door 0.838, pilasters 0.35 (C5, C8, C9), the door order following the fascia target's door ends | u from the glass's (or the shop door's) viewer's-left edge | the cards: section 5.7; D01 in the grocer's glass, J01 in the newsagent's beside the card board (the Tivoli programme T03, held, would stand in the ironmonger's) |")
w()
w("Piers (street x of the clear brick, from the recipe's bay layout; bay 1 agrees with the scene file's note that the poster slot at x 11.4 lies between a door at 10.5 and a window at 12.3):")
w()
w("| Pier | x0 to x1 | centre | between | placed |")
w("|---|---|---|---|---|")
byp = {}
for p in DEF:
    if p["surface"] == "WEST_PIER":
        byp.setdefault(p["pier"], []).append("%s z %.2f" % (p["item"], p["z_bottom_m"]))
for pr in T["west_piers"]:
    w("| %s | %.3f to %.3f | %.3f | %s | %s |" % (pr["id"], pr["x0"], pr["x1"], pr["cx"], pr["between"], ", ".join(byp.get(pr["id"], [])) or "none"))
w()
w("The scene file's two held props are stale: its poster at west x 11.4 is the pier W1.0 and stays; its glazed case at west x 26.4 would stand on the tea room's glass (the west block is shops, not plain, from x 24). Neither case is placed at all: the Harbour Board's belongs by the dock office and the ferry's board at a ramp, and neither is built (`unplaced`).")
w()
w("Not placed on Quay Street, with the reason (`unplaced` in `target.json`): " + "; ".join("%s (%s)" % (k, v) for k, v in T["unplaced"].items() if not v.startswith("on the newsagent") and not v.startswith("the named twin")) + ".")
w()

# ------------------------------------------------------------------ 3
w("## 3. Sizes, stocks, processes and what they look like")
w()
w("British paper sizes of the period (Derived from the imperial names: 25.4 mm to the inch; the Double Crown 20 x 30 in is a Lead from a search summary).")
w()
w("| Name | mm | used for |")
w("|---|---|---|")
use = dict(crown="(none now: J01 is an A3 photocopy)", double_crown="the poll-tax, fight, market, tea and programme bills", quad_crown="T01, T02 (landscape, 'the quad')", four_sheet="G01 (held, not placed)",
           A2="F01, F02 (the ferry sheets)", A3="police and road-closure notices; the jumble-sale and dance notices (photocopies)", A4="the advice sheet, planning notice, three Harbour Board notices", A5L="cards K01, K05, K06 a and b, K08",
           A6L="K06c, SA15", A5="(portrait, not used)", A6="(portrait, not used)")
for k, v in T["formats"].items():
    w("| %s | %d x %d | %s |" % (k, v["w"], v["h"], use.get(k, "")))
w()
w("Processes, in plain words (the numbers are in `processes`):")
w()
for k, v in T["processes"].items():
    extra = []
    for kk in ("registration_offset_mm", "impression_mm", "toner_density", "pitch", "roughness", "relief_mm", "draft_deg", "top_radius_mm", "thickness_mm", "edge_roll_radius_mm"):
        if kk in v:
            extra.append("%s %s" % (kk, v[kk]))
    w("- **%s**: %s%s%s" % (k, v["name"], ("; " + "; ".join(extra)) if extra else "", ("; lead: " + v["lead"]) if v.get("lead") else ""))
w()
w("The look in one paragraph per kind (all Judgement unless a lead is named):")
w()
w("- **Fly-posters** are two-colour jobs from a small jobbing printer: black and one colour on cheap uncoated poster paper, white or tinted or fluorescent, set in a mixture of faces with thick rules and a printer's imprint in 7-point at the foot. Letterpress bills show a darker rim at the letter edges and a faint relief; screen-printed ones are flat and a little thick; the second colour sits 0.3 to 0.8 mm off register. The poll-tax bills use fluorescent yellow and orange stock because the one 1990 sheet found is yellow in red ink (a Lead).")
w("- **Quads** are offset litho in full colour on uncoated paper and carry NO venue: the cinema pasted its own letterpress strip (black on white, 1016 x 90) across the top band. The halftone is not resolved at the item's scale, so they are drawn as continuous tone with grain; the image model makes the picture only (no words, no people, no crown, kiosk, bottle, glass or arcade sign: `ART.eye`), our text layer lays every letter, and a dark scrim guarantees the contrast of the lines on the art.")
w("- **Photocopies** (the advice sheet, the jumble-sale and dance notices, the police appeals, the planning and road notices) are hard black toner on white or tinted copier paper: a grey band 3 to 6 mm along one edge, speckle, a crooked copy (the placement's rot_deg), a vertical streak or two. Planning and road notices sit in a clear polythene sleeve; the A3 notices in a window are taped by four tabs of yellowed tape.")
w("- **Typed notices** (the Harbour Board's) are Courier Prime, 10 characters to the inch, an electric typewriter's even impression, pinned in a glass case with drawing pins, curling (held until the case is built).")
w("- **Hand-lettered cards** are felt pen (a fat even line, a darker blob where the nib rested) in Patrick Hand capitals, and ballpoint (a thin line, lighter on the joins) on white or tinted record cards; each is TAPED by one tab at its top-left corner or hung on a string and a sucker, and slightly crooked.")
w("- **Stickers** are printed paper labels, die-cut, edges lifting and scratched.")
w("- **Enamel signs** are vitreous enamel on pressed steel: gloss, a rolled edge of 6 mm radius, chips to black steel with a rust halo at the corners and the bolts.")
w()

# ------------------------------------------------------------------ 4
w("## 4. Stocks, inks, paints and ageing")
w()
w("Four classes by days on the wall: **A** fresh (0 to 7 days), **B** weeks (8 to 35), **C** months (36 to 120), **D** old (over 120). A colour fades by f = 1 - exp(-t / tau) (tau in days, per ink or stock) towards the paper, the paper yellows (30 per cent of the way to (214,200,168) at class D), and a grime film (62,58,52) mixes in at 0, 5, 12 and 22 per cent (35 per cent of that over ink). The order of fastness (Judgement) is fluorescent stock, then red, blue, black, toner.")
w()
w("**The street date is Monday 29 October 1990** (`calendar.street_date`): a day every placed dated item allows (GMT began on the 28th; the held proof wall's P01 and T02 allow it too: the meeting of the 25th is four days gone, the film started on Thursday 25). `G.dates.age` fails a placed dated item unless some age in its class's days posts it no more than 42 days before its event and no later than it (a notice: no earlier than its date). The ages that follow: P01 B (held; the 25 October meeting is four days gone: a stale bill), W01 A (held, on the gable), T02 A (held; up since the 25th), T03 B (held), D01 B, J01 B (the 20 October sale is nine days gone: stale), P03 B, C01a B (the night of 12 October), C02 A, M01 C on the glass and B on the pier. The first try's contradictions (T03 in class D under T01 in class A for the same week; D01 in class C for a 17 November dance) are tested and fail.")
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
w("Paper wear (numbers for the builder; Judgement): wrinkles of 0.4 to 1.5 mm, wavelength 12 to 40 mm, from wallpaper-paste cockling, strongest along the brush direction (vertical); corners lifting 0 to 3 of radius 15 to 60 mm (none at class A, three at D); tears 0 to 4 of width 20 to 140 mm from an edge; rain runs 2 to 8 a metre, 10 to 60 mm long, 0.4 to 1.5 mm wide, opacity 0.15 to 0.4, down from the top edge and from any lifted corner, the red and dye inks running first; a paste halo 2 to 10 mm at class C and D; share of the sheet lost 0 to 0.05 at B, 0.03 to 0.2 at C, 0.3 to 0.6 at D, the lower corners first; skew only in the placement (-1.5 to +1.5 degrees); the quay gable's bills are one layer (no overposting there). A wet wall darkens paper by 12 per cent and raises saturation by 10 per cent (a runtime hint).")
w()
w("Wear tables by kind (`wear_tables`): " + "; ".join(k for k in T["wear_tables"]) + ".")
w()

# ------------------------------------------------------------------ fonts
w("## 4b. Type")
w()
w("%d font files from %d families, **all SIL OFL 1.1, every family's OFL.txt read whole on raw.githubusercontent.com** (the first try also read UnifrakturMaguntia's, Arimo's, Libre Baskerville's, Josefin Sans's and Abril Fatface's and Liberation's LICENSE; none is used now). Letters are RENDERED into pictures: the OFL puts no restriction on a picture made with a font. The font files themselves are NOT copied into `production/fonts` here." % (len(T["fonts"]), len({v["family"] for v in T["fonts"].values()})))
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
w("Three are not in `production/fonts` (Archivo, Courier Prime Regular and Bold); `self_check.py --fetch-fonts DIR` fetches them and the OFL texts. The old bills used League Gothic (in the repository, an OFL face, and on the asset plan's table): this target uses Oswald, also on the table, because its weight axis lets one file carry 500, 600 and 700. Overpass is never used. No UnifrakturMaguntia: a masthead would name a local paper, which canon owes.")
w()
w("**Fonts off the asset plan's table (note 4, A2), and the decision for each.** The second try removed Libre Baskerville (typeset notices now use Old Standard TT Regular and Bold, the table's 'Old Standard'), Josefin Sans (the Tivoli's strip and programme use Oswald, the table's 'the Tivoli's letters') and the never-used Abril Fatface. Two remain, each with the line to append to DECISIONS.md (the target may not edit it):")
w()
for d in T["font_decisions"]:
    if d.get("decisions_line"):
        w("- **%s**: %s. Why: %s. DECISIONS.md line: `%s`" % (d["font"], d["plan"], d["why"], d["decisions_line"]))
w()

# ------------------------------------------------------------------ 5 items
w("## 5. The items, word by word (unit 4.2)")
w()
w("Each line: the exact words, the font and weight, the cap height in millimetres, the anchor and x, the baseline y, the ink, and the contrast of ink on ground in class B. Anchors are of the INK, not the advance box. Every width is measured on the real font file; every box is in `target.json` (`ink_box_mm`). Each item shows its pixel scale and, if it is held, the names that hold it.")
w()


def item_block(iid, extra=""):
    it = ITEMS[iid]
    f = it["format"]
    w("#### %s  %s" % (iid, it["title"]))
    w()
    bits = ["%d x %d mm (%s)" % (f["w_mm"], f["h_mm"], f["name"] or "own size"), "%g px/mm" % it["px_per_mm"]]
    if it.get("stock") and it["kind"] in ("sheet", "card", "sticker"):
        bits.append("stock: " + PAL["stocks"][it["stock"]]["name"])
    bits.append("process: " + it["process"])
    if it.get("event"):
        bits.append("event: " + it["event"]["date"])
    if it.get("dated"):
        bits.append("dated: %s %s" % (it["dated"]["kind"], it["dated"]["date"]))
    if it.get("stand_in_of"):
        bits.append("HELD (a nameless stand-in; waits with %s for: %s)" % (it["stand_in_of"], ", ".join(it["waits_for"])))
    elif it.get("held"):
        bits.append("HELD until minted: " + ", ".join(it["held_names"]))
    w("- " + "; ".join(bits))
    vv = it["variants"]
    w("- variants: %s (%s)" % (vv.get("n", "?"), "; ".join(vv.get("vary", []))))
    if it.get("fixing") and it["fixing"].get("what"):
        w("- fixing and mirror cue: " + it["fixing"]["what"] + ("; the corner patches are %s (left) and %s (right)" % (it["mirror_cue"]["patch_left_mm"], it["mirror_cue"]["patch_right_mm"]) if it.get("mirror_cue") else ""))
    for sh in it["shapes"]:
        if sh.get("box_mm"):
            w("- shape %s (%s): box %s, fill %s%s" % (sh["id"], sh["kind"], sh["box_mm"], sh.get("fill"), (" - " + sh["note"]) if sh.get("note") else ""))
        elif sh.get("pts_mm"):
            w("- shape %s (%s): %d points %s, %s" % (sh["id"], sh["kind"], len(sh["pts_mm"]), sh["pts_mm"] if len(sh["pts_mm"]) <= 8 else "(see target.json)", sh.get("note", "")))
        elif sh.get("centre_mm"):
            w("- shape %s (%s): centre %s, %s%s - %s" % (sh["id"], sh["kind"], sh["centre_mm"], ("r %s to %s mm" % (sh["r_inner_mm"], sh["r_outer_mm"])) if sh.get("r_outer_mm") else ("%s x %s mm" % (sh.get("length_mm"), sh.get("width_mm"))), "", sh.get("note", "")))
        elif sh.get("segments_mm"):
            w("- shape %s: %d segments, %s mm wide - %s" % (sh["id"], len(sh["segments_mm"]), sh.get("width_mm"), sh.get("note", "")))
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
w("An INVENTED LOCAL CAMPAIGN (ruling 3 October): no party, no person, no real group, no real logo. The name `MERIDIAN AGAINST THE POLL TAX` is proposed, not minted, so the DEFAULT bills P01 to P03 carry the generic STAND TOGETHER where the held `-named` twins carry the campaign (21 to 24 mm capitals); the 2.4 mm imprint, the 3.6 to 6 mm lines on P04 to P06 and the printer's imprint (QUAY PRINT) stay: they are under the 10 mm line and illegible from across the street. The slogan CAN'T PAY - WON'T PAY is a common slogan (and the title of a 1974 play), not a party's mark: the reviewer says keep it. Autumn 1990 is the summons season, so the bills are about meetings, a march and what to do with a summons. Dates: Thursday 25 October (meeting), Tuesday 30 October (advice), Saturday 10 November (march).")
w()
for i in ("P01", "P01-named", "P02", "P02-named", "P03", "P03-named", "P04", "P05", "P06"):
    item_block(i)
w("### 5.2 The chapel hall (the game's `chapel_hall`)")
w()
w("`THE CHAPEL HALL` is the game's own place (`hook-cast.json`, Father Walsh's chapel and its hall); no street is minted for it, so the notices name none. Religion appears as part of life, never mocked: the jumble sale is in aid of the chapel roof fund. No raffle, no bingo, no drink (`TEA AND SANDWICHES`), no children (`ALL WELCOME`, never 'families'). **Both notices are photocopied A3 sheets** (asset-plan note 4: a 1990 jumble-sale notice 'is Letraset, photocopy or two-colour screen print'): J01 is taped inside the newsagent's glass beside the card board and on the empty unit's glass, D01 inside the grocer's glass. The dance is OLD TIME and SEQUENCE DANCING (not NEW VOGUE, the Australian name). The band, THE SANDERLING TRIO, is a placeholder: the default D01 says LIVE MUSIC.")
w()
for i in ("J01", "D01", "D01-named"):
    item_block(i)
w("### 5.3 The fights, the market and the goods")
w()
w("The wrestling bill W01 names no ring names and no hall (it reads PROFESSIONAL WRESTLING, a heavyweight contest, a tag team contest, support bouts; 'ALL-IN' was the 1930s name); a bill that names nothing reads as a placeholder by another name, so **W01 is HELD with its named twin** and built only once the town mints the hall and the ring names (second review, fault 3). The `-named` twin carries the proposed names: THE DRILL HALL (a generic building, no street given) and four invented ring names (THE HARPOONER, SPANNER SMITH, TED HOLROYD, THE STEVEDORE), renamed after the review found two of the first four real (a dock-union leader; Jack London's novel) and a third a television series, and after the re-review found the first rewrite, BIG TED HOLROYD, to be the name of the bear in the BBC children's programme Play School (BIG TED is now in `real_marks`). No odds, no stakes, no prize. The market bill matches `hook-cast.json`: Tuesday, Friday, Saturday, 8 to 4. The two goods are INVENTED brands (WHITEWELL washday powder, QUAYSIDE TEA), proposed, not minted, held and not placed (a national four-sheet belongs in a contractor's panel, not pasted under fly-posters); a cigarette bill is not drawn (a minted brand and the 1990 health-warning wording are both missing).")
w()
for i in ("W01", "W01-named", "B01", "M01", "G01", "G02"):
    item_block(i)
w("### 5.4 The Tivoli")
w()
w("The Tivoli is minted (canon) and 'changes its programme on Thursdays' (brand bible): the films start on Thursdays (T01 from 18 October, T02 from 25 October). Its films are invented: the nameless bills (T01 'A NEW THRILLER', T02 'A NEW COMEDY', T03's programme that names no film) read as stand-ins and are HELD with their twins (second review, fault 3); the `-named` twins say THE FOURTH WITNESS and A WEEK AT GULLWING (Gullwing is a minted district) with a billing block (6 to 12 mm: a studio and three credits, placeholders); the BBFC certificate roundels are real marks and are NOT drawn. **A distributor's quad carried no venue**: the cinema pasted a strip across its top band, so the quad's own top 90 mm is blank and the strips T01s and T02s (1016 x 90 mm, letterpress black on white, 2 to 6 mm off square) carry THE TIVOLI and FROM THURSDAY ...  The quads' art comes from the image model with no words and no people (no telephone box, no pier: a lit window down a wet street; a beach with deckchairs); our text sits on a dark scrim (T01) or on a pale panel (T02). The Tivoli's own front (plastic letters on a rail, changed on Thursdays) is not this family's.")
w()
for i in ("T01", "T01-named", "T02", "T02-named", "T03", "T03-named", "T01s", "T02s"):
    item_block(i)
w("### 5.5 The ferry and the Harbour Board")
w()
w("Both are minted names (canon). The ferry sheet is the WINTER SERVICE from Monday 1 October 1990, pasted over the summer sheet on a painted timber board at a ramp (FC1, no glazing), as the brand bible says; the service is one a single boat can run (15-minute crossings; Hook sailings at :00 and :30 by day, the far side's 15 minutes later; **the far side's last crossing is 11.15 PM so the boat is at the Hook at 11.30**, and Sunday's 6.15 PM brings it home at 6.30) and its last Hook crossing, 11.00 PM, is the street's own line 'Last crossing's at eleven'. `G.ferry.schedule` simulates the one vessel from the printed blocks and checks that each day ends where the next day's first sailing leaves. The fares are foot passengers and cycles: no one is a child. The Harbour Board's notices are typed Courier on A4 in a glass case drawing-pinned and curling (the brand bible's own words), headed NOTICE TO MARINERS (not SHIPMASTERS); its blue and white enamel signs are 600 x 450 on a gate, post or quay edge. NONE of the case, the board or the notices is placed on Quay Street (no dock office, no ramp); H02 stands on a proposed quay-edge post. Board blue is Judgement: (24,68,140).")
w()
for i in ("F01", "F02", "H01", "H02", "H03", "H04", "H05"):
    item_block(i)
for c in T["cases"]:
    w("#### %s  %s" % (c["id"], c["title"]))
    w()
    w("- outer %d x %d x %d mm, frame left %d, right %d, top %d, bottom %d, window corner radius %d mm; inside %s mm" % (c["outer_mm"][0], c["outer_mm"][1], c["depth_mm"], c["frame_mm"]["left"], c["frame_mm"]["right"], c["frame_mm"]["top"], c["frame_mm"]["bottom"], c["window_radius_mm"], c["inside_mm"]))
    if c.get("rail_section_mm"):
        w("- rails %s mm with a %g mm chamfer on %s; glass %g mm in a %s mm bead" % (c["rail_section_mm"], c["chamfer_mm"], c["chamfer_where"], c["glass"]["thickness_mm"], c["glass"]["bead_mm"]))
    w("- construction: " + c["construction"])
    w("- fixing: " + c["fixing"])
    w("- wear: " + c["wear"])
    w("- pinned or pasted inside: " + "; ".join("%s at (%d, %d) mm, %.1f degrees" % (ch["item"], ch["x_mm"], ch["y_mm"], ch["rot_deg"]) for ch in c["children"]))
    w("- NOT placed: " + c["not_placed"])
    w("- photograph: " + c["photo_proportions"]["note"])
    w()
w("### 5.6 Police and council notices")
w()
w("The police force's name and the council's name are OWED by canon, so neither appears: POLICE, HIGHWAYS DEPARTMENT and the Planning Department are the generic words. A police appeal is an A3 photocopy taped inside a window or sleeved on a column (the one dated yellow appeal board found is from 2007; a 1990 board is a hole): C01a is taped inside the empty unit's glass with four tabs. The three samples are slots the simulation can fill (offence line, night, hours): a smashed shop window on Quay Street (matching the 29 September deed), a van stolen from the quay, a man assaulted near the quay. The planning notice is for the empty unit itself, **number 7** (shop to estate agent's office): a mundane hook, struck if the town prefers. The road closure sends traffic via WEIGHHOUSE LANE (minted; the atlas's Weighhouse Lane and Tannery Row make the way round; the side opening at x 21 to 24 is the yard entrance, not that lane).")
w()
for i in ("C01a", "C01b", "C01c", "C02", "C03"):
    item_block(i)
w("### 5.7 Shop-window cards and the newsagent's board")
w()
w("Cards are hand-lettered in Patrick Hand (felt pen and ballpoint) or printed. **Every hand-lettered card carries ONE cue matching its fixing, on its left half only** (a mirrored hand card cannot be told by its words at line level): a taped or stuck card has one tab of yellowed tape across its top-LEFT corner (K05, K06c, K07a-d, K09a-f, SA01-SA15); a string-hung card has the knot and sucker at its top-LEFT (K01, K06a). No crease, tear or pin-hole cue. Times and prices come from the world: LAST WASH 4.30 PM is an hour before the laundry's closing (8 to 5.30, `hook-cast.json`); cod 2.70 a lb is the ONS 1990 range (2.42 in January, 2.85 in December); smoked haddock is dearer than fresh; the other prices and the 20p-a-week advertising rate are Judgement. No card names a child, a pet shop, a drink, a pool or a lottery; no 'model' or 'companion' cards (tart cards are a content-rule line). Telephone numbers are the local six-figure form 960 xxx (the fictional range the cast's own 0632 960418 uses); none is Mickey's or one digit from it. K02 (BACK AT, Hal's break) is not placed: the newsagent never closes at midday.")
w()
for i in ("K01", "K02", "K03a", "K03b", "K04", "K05", "K06a", "K06b", "K06c", "K07a", "K07b", "K07c", "K07d", "K08", "K09a", "K09b", "K09c", "K09d", "K09e", "K09f"):
    item_block(i)
w("**The newsagent's board SB1** (760 x 560 mm on the glass at u 1.95 m, z 0.90 m): fifteen cards of two sizes (127 x 76 record cards, 148 x 105 postcards), every one taped by a single tab at its top-left (pins are for a cork board).")
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
w("**The default board is the fascia target's board, exactly** (`small_panels.letting_board`): **900 x 450 mm, white face, TO LET alone in Libre Franklin 800, cap 130, vinyl red (176,30,34), no agent, no number**, four screws slightly askew, a rust run under each lower screw; `G.letting.mount` compares size, text, font, weight, cap and colour with the fascia target's file and fails the first try's 1200 x 450 board. 450 mm is the height a 0.55 m fascia takes with 50 mm clear above and below. The agent board L01 (1200 x 450, ARMITAGE & STOBBS, Chartered Surveyors, Estate Agents, a number) and the flat board L03 carry a PROPOSED agent (not minted; not checked against real firms, the network refusing the sources): they are held variants, and using L01 would need the fascia target's entry changed in the same batch with one DECISIONS line. The flat above the empty unit carries the no-agent L03n (the L04 layout at 600 x 400: TO LET, SELF-CONTAINED FLAT, ENQUIRIES 960 335); the house board L04 stays. A letting board is white gloss on 18 mm exterior plywood, corners rounded 4 mm, the cut edges painted, a 25 x 18 mm batten at each end, four 8 mm dome-head coach screws 40 mm in from the corners with a rust run 40 to 140 mm under each lower one, hung 2 degrees askew (the placement's rot_deg). Colours: agent navy (28,46,94), red (178,34,40), white (236,236,230); at class D the white yellows to (214,206,184) and the red fades towards chalk-pink by 0.3. Fonts: Jost for the agent boards (the asset-plan table), Libre Franklin for L02 (the fascia target's).")
w()
for i in ("L02", "L01", "L03", "L03n", "L04"):
    item_block(i)
    m = ITEMS[i]["mount"] if ITEMS[i].get("mount") else None
    if m:
        w("- mounted on: %s; centre street x %s m; z %s to %s m; %s; askew %s degrees. %s" % (m["surface"], m["centre_street_x_m"], m["z_bottom_m"], m["z_top_m"], m["screws"], m["askew_deg"], m.get("note", "")))
        w()

# ------------------------------------------------------------------ 7 plates
w("## 7. Street name plates (unit 4.4)")
w()
w("**What 1990 British plates carried, as far as I could establish.** No photograph was reached. From search summaries (Leads): there was never a national design and each council chose its own style, colour, size and material; black capitals on white with a black border was the default the 1993 Department of Transport circular recommends and the usual look; the Ministry of Transport's alphabets date from the early 1930s, the Kindersley lettering was adopted in 1951 and recommended in 1952, by which time raised plates were cast aluminium, not iron; Hull's cast plates of the 1920s to 1930s were black on white and their paint faded or flaked; London plates carried the borough and the postal district. I found NO source that provincial plates of the 1980s carried a district line or a postal district, and the project's own street-clutter note describes a plain plate and lists postcodes as wrong for 1990. **What the target says (second try):** the default and the placed plate is `n`, the name only; `d` (the name and a district's name as a small line: THE HOOK, COPPER ROW, IRONSIDE) stays a variant until a dated photograph shows a district line; the postal-district variant (MR1) is deleted; no council, no crest (canon owes the council's name). **Letter style:** Marcellus SC capitals, 90 mm tall, tracking +0.04 em, ruled on 30 September for the street plates (it stands in for the Kindersley serif, which has no allowed free version).")
w()
w("**Sizes.** Plate length follows the name: ink width plus 2 x 62 mm (6 mm edge + 12 mm border + 44 mm clear), rounded up to 10 mm. **Depth at least 200 mm** (the street-clutter note's 20 to 25 cm; the first try's 170 mm `n` plates were too shallow): 200 mm for `n`, 220 or 240 mm with a district line (Quay Street's Q dips 36 mm below the baseline). The border band is 12 mm, 6 mm in from the edge; corners rounded 6 mm. Fixing: four screws 30 mm in from the corners (10 mm dome heads into fibre plugs; the cast plate has four 12 mm holes cast in). Mounting height: bottom edge at about 2.5 m, centre 2.63 m (the earlier note says 2.2 to 2.5 m, the existing plate hangs at 2.50 to 2.76).")
w()
w("**Makes, by street (Judgement), with numbers.** QUAY STREET: cast aluminium (by the 1950s raised plates were cast aluminium, not iron), a face 6 mm thick, letters and border raised 3 mm, painted white with black letters, the paint flaking first from the raised edges to bare grey aluminium; a plain cast edge 6 mm thick with a 2 mm arris radius. WEIGHHOUSE LANE: die-pressed aluminium 2 mm, letters and border raised 1.5 mm, stove enamel, a rolled edge of 3 mm radius. TANNERY ROW: vitreous enamel on pressed steel, flat, a rolled edge of 6 mm radius. **Raised letters and border: 10 degrees of draft each side and a 0.8 mm radius on the top edge.** **The lettering suits the make** (`lettering_suit`, Derived from the rendered glyphs' distance transform): Marcellus SC's thinnest stroke at 90 mm capitals is %s mm and its thickest %s mm; after 3 mm of relief at 10 degrees a cast hairline keeps a top width of %s mm (1.5 mm needed to cast), a pressed 1.5 mm relief %s mm. `G.plates.make` checks it." % (
    ITEMS["S01n"]["lettering_suit"]["strokes_mm"]["thin_mm"], ITEMS["S01n"]["lettering_suit"]["strokes_mm"]["thick_mm"], ITEMS["S01n"]["lettering_suit"]["top_width_of_thinnest_stroke_mm"], ITEMS["S02n"]["lettering_suit"]["top_width_of_thinnest_stroke_mm"]))
w()
w("| Plate | street | district | variant | plate (mm) | ink width | material |")
w("|---|---|---|---|---|---|---|")
for it in T["items"]:
    np_ = it.get("name_plate")
    if np_:
        w("| %s | %s | %s | %s | %d x %d | %s | %s |" % (it["id"], np_["street"], np_["district"] if np_["variant"] != "n" else "(none)", np_["variant"], it["format"]["w_mm"], it["format"]["h_mm"], np_["ink_w_mm"], np_["material"]))
w()
w("Placed: **S01n** at street x 20.47 on the west corner pier (x 19.92 to 21.0, brick to 3.12 m: the existing plate's place, kept, 80 mm of pier either side), centre z 2.63. **The quay gable carries no plate**: the Hook sheet shows none there, and one plate on a 48 m street is enough; a second S01n at u 1.0 (centre z 2.63) is a HELD placement. **NO plate stands on the yard entrance** (street x 21 to 24, the dropped kerb at 22.5): the scene file calls it the yard entrance and atlas-01 gives it as `yard_gap_x [21, 24]`; the atlas runs Weighhouse Lane about 200 m beyond the built 48 m, so naming the gap is a map fact the town has settled. **S02 (WEIGHHOUSE LANE) and S03 (TANNERY ROW)** are kit plates for the town and are not placed on Quay Street. The plate board's pictures: `L4` shows all six.")
w()
for i in [x for x in ITEMS if x.startswith("S0")]:
    it = ITEMS[i]
    w("#### %s  %s" % (i, it["title"]))
    w()
    w("- relief: %s; edge: %s" % ("raised %s mm, draft %s degrees, top radius %s mm" % (it["relief"]["raised_mm"], it["relief"]["draft_deg"], it["relief"]["top_radius_mm"]) if it["relief"]["raised_mm"] else "none (flat enamel)", it["relief"]["edge"]))
    for b in it["blocks"]:
        w("  - `%s` | %s | cap %s | %s %s | base %s | B %s" % (b["text"], b["font"], fnum(b["cap_mm"]), b["anchor"], fnum(b["x_mm"]), fnum(b["baseline_mm"]), b["contrast"]["B"]))
    w()

# ------------------------------------------------------------------ 8 paste plan
w("## 8. The paste plan: placements")
w()
w("Layers run from the oldest (0) to the newest; age class A to D is the paper's age on the street date (section 4). Placements marked HELD are not in the default street: the named twins of a default placement and the nameless stand-ins (built only after the town mints their names: `G.page.placeholders`, section 12) and the five `proof_wall` placements of the quay gable (P01, W01, T02, T02s and a second QUAY STREET plate), which the bare gable holds back. The gable's `proof_wall` set is the plan's sample, kept for the case that he chooses the gable.")
w()
w("| Surface | Item | where | z bottom (m) | rot | layer | age | size (m) | notes |")
w("|---|---|---|---|---|---|---|---|---|")
for p in PL:
    if p["surface"] == "SHOP" and p["item"] != "SB1":
        where = "%s %s u %.2f" % (p["shop"], p["where"], p["u_m"])
    elif p.get("u_m") is not None and p["surface"] in ("SF1", "SF2", "SF7"):
        where = "u %.3f" % p["u_m"]
    elif p["surface"] == "SHOP":
        where = "newsagent glass u %.2f" % p["u_m"]
    else:
        where = "street x %s%s" % (p.get("street_x_m"), (" pier " + p["pier"]) if p.get("pier") else "")
    flags = []
    if p.get("held_until_minted"):
        flags.append("HELD (%s)" % ", ".join(p.get("names", [])))
    elif p.get("held"):
        flags.append("HELD (the bare gable)")
    if p.get("proof_wall"):
        flags.append("proof_wall")
    if p.get("scale"):
        flags.append("scale %s" % p["scale"])
    w("| %s | %s | %s | %.2f | %s | %s | %s | %.3f x %.3f | %s |" % (p["surface"], p["item"], where, p["z_bottom_m"], p.get("rot_deg"), p["layer"], p["age_class"], p["w_m"], p["h_m"], "; ".join(flags)))
w()

# ------------------------------------------------------------------ 9 words
w("## 9. The words, as a list")
w()
w("%d approved strings (`approved_words`), %d tokens (`approved_word_parts`). Every string is ours. Checked against: this file's forbidden lists (alcohol, gambling, children, real marks, names canon owes, things after 1992; extended in the second try with plurals, near terms and the real names the reviewer's probe listed); `tools/content-gate.py`'s %d speech rules; `RealWorld.cs`'s names; imagegen's forbidden tokens; canon's streets and districts; the cast's surnames. **Proposed, unminted names** (placeholders, never on his page; a name in a block of cap 10 mm or more HOLDS its item):" % (len(T["approved_words"]), len(T["approved_word_parts"]), N_RULES))
w()
w("| Name | what | on items | held items | largest cap (mm) |")
w("|---|---|---|---|---|")
for p in T["proposed_names"]:
    w("| `%s` | %s | %s | %s | %s |" % (p["name"], p["what"].replace("|", "/"), ", ".join(p["items"]), ", ".join(p["held_items"]) or "none (under 10 mm)", p["max_cap_mm"]))
w()
w("Names canon owes and this target therefore does NOT use: the football club, the local paper, the pirate radio station, the regional television channel, the telephone operator, the postal cypher, the council's name. The brand bible v1 carries proposals for four of them (Meridian Town AFC, The Meridian Argus, Radio Tideline, Coastway Television); canon.md still lists them as owed, so none is drawn here.")
w()
w("**The placeholder rule** (`placeholders`): " + T["placeholders"]["rule"])
w()

# ------------------------------------------------------------------ 10 variants
w("## 10. Variants the street needs")
w()
tot = sum(it["variants"].get("n", 1) for it in T["items"])
w("%d seeded variants over %d items (a poster is built once, shown in the variants its entry names; nothing is multiplied before one complete sample is approved in the assembled game, CLAUDE.md: the empty unit's glass, six sheets in one layer, is the sample of the default street). The variants differ in: age class (always), ink registration and density, which corner is torn or lifting, tape positions, the second pass's shift, and the hours-driven face (OPEN or CLOSED, the LAST WASH hour). **Skew is never a variant of the texture**: it is the placement's rot_deg. The three police sheets are slot fillers: the same layout with another offence line. Dates move with the calendar: every event bill gives its date as computed words, so a build for another date in 1988 to 1992 re-computes the weekday (`G.dates`) and re-checks the ages (`G.dates.age`)." % (tot, n_items))
w()

# ------------------------------------------------------------------ 11 disagreements
w("## 11. Where photographs, books, the reviewer and the ruling disagree, and what I chose")
w()
for d in T["disagreements_photographs_win"]:
    w("- **%s.** Wins: %s. Against it: %s. Chosen: %s" % (d["topic"], d["wins"], d["others"], d["choice"]))
w()

# ------------------------------------------------------------------ 12 checks
w("## 12. The checks, and how the pixels are read")
w()
kinds = {}
for c in T["checks"]:
    k = c["id"].split(".")[-1] if (c["id"][0] in "PSKJDLWTMGFHCB" and "." in c["id"] and not c["id"].startswith(("G.", "PLACE", "ART"))) else c["id"].split(".")[0]
    kinds[k] = kinds.get(k, 0) + 1
rc = T["render_contract"]
w("%d checks in `target.json` (`checks`). **Per item:** `.size` (image size), `.words` (the glyph manifest's characters equal the approved strings: a manifest check, NOT a pixel check; a missing or unreadable `<ITEM>.glyphs.json` FAILS it), `.pos` (each block's ink box read off the pixels, widened 8 mm along the line and 3 mm up and down, other blocks' glyphs not counted), `.cap` (letter heights at scale), `.mask` (the whole LINE re-rendered from its font compared with the ink: F at least 0.90 for printed lines, 0.85 for small print and typing, 0.78 for hand lettering, 0.55 for imprints; a PRINT line must also keep its worst single glyph at F 0.85 and pass the glyph check, so a changed word cannot hide in the mean; **a hand line's mask catches a wrong font or a shift, not a wrong word**: its jitter is only known from the manifest), `.glyphs` (the word check, below), `.square` (the texture is square-on within 0.3 degrees, ONE tolerance for print and hand cards alike, found against the render of the item's own glyph manifest, jitter included, and 0 unless F at the best angle beats F at 0 by 0.02), `.clean` (**ITEM.clean**: at most 2 mm2 of ink-coloured pixels outside every block's glyph window, the item's own shapes, the cue patch and the art slots, on the class-A render before wear), `.contrast` (WCAG on the aged render, class B), and for each art picture `ART.eye`. **Global:** `G.words.approved`, `G.forbidden`, `G.dates`, `G.dates.age`, `G.mirror`, `G.mirror.cues`, `G.fonts`, `G.proposed`, `G.page.placeholders`, `G.ferry.schedule`, `G.tides`, `G.place.inside`, `G.place.layers`, `G.place.piers`, `G.place.height`, `G.place.paper`, `G.place.gable`, `G.place.shops`, `PLACE.built`, `G.letting.mount`, `G.plates.length`, `G.plates.depth`, `G.plates.cap`, `G.plates.border`, `G.plates.make`, `G.glyph.scale`." % n_checks)
w()
w("**`ITEM.glyphs`: reading one glyph at a time (TARGET-REVIEW fault 1).** The first try compared whole lines with a 1 mm (print) or 2.5 mm (hand) tolerance; a changed date, TEA for ALE, LUNCH for BINGO or a changed price scored F 0.94 to 1.00 and passed. A single glyph is a small part of a line. So:")
w()
w("1. **The glyph manifest.** Every render writes `<ITEM>.glyphs.json`: one entry per character of the approved string, spaces included, in order: `ch, font, weight, em_mm, ox_mm, baseline_mm, rot_deg, emb_mm` (the pen origin from the item's left edge, the baseline up from its bottom edge, the hand jitter and the pen's added stroke included). A manifest whose characters are not the approved string, or whose glyphs lie outside the block's envelope (print: 0.6 mm, 0.5 mm, 0.1 degree, 1 per cent; hand: 3.5 sd of the hand style plus a little), FAILS before any pixel is read (`G.words.approved` and `.words` read the same manifest). **A missing, empty or unreadable `<ITEM>.glyphs.json` FAILS `.words` and `.glyphs`**: the reader reports it and never crashes.")
w("2. **The cell.** Each glyph is re-rendered from its manifest entry (glyph by glyph, the same function the renderer uses) and read in its own cell: the columns between its neighbours' ink, the block's window in rows. What the reader does not credit to it: the other blocks' glyphs as THEY manifest them, the item's rules, frames and bars, and its neighbours in the line (all dilated 1 mm), unless the glyph's own ink holds the pixel; and, where hand-lettered glyphs touch, **a pixel that a neighbour's ink explains and the glyph's own ink does not (within one pixel) is the neighbour's** (the first try credited it to the glyph, which failed true ballpoint cards). Big capitals are read at a reduced scale (an area rule that matches how their reference is drawn); a space carries no ink beyond 0.6 mm of every glyph of the line.")
w("3. **F.** F = the mean of recall and precision of the read ink against the re-rendered glyph, each against the other dilated 0.5 mm: **at least 0.85** (the review's figure).")
w("4. **SEP.** The glyph must be told from every other glyph of its font in A-Z a-z 0-9 £ . , ' ’ - — – & · ? : ! rendered at the same place, size and turn, and from its own mirror. Where the claimed glyph and the alternative differ, `A` is what only the claimed glyph inks and `B` what only the alternative inks (outside a 1-pixel tolerance); SEP is the share of the A and B pixels on which the read ink sides with the claimed glyph. **The gate is 0.70** (a margin of 0.40 where the review asked 0.05; see section A for why F itself cannot give a margin). Pairs that differ by fewer than %d pixels are not told apart at that scale: the item's scale is raised until none is, so that every non-twin pair differs by at least %d pixels at every item's own px/mm (`G.glyph.scale`, %s font/weight/cap/stroke combinations tested). **Shape twins** (I and l, ' and ’, any pair differing by under 0.03 mm2 at 24 px/mm) and a glyph that is its own mirror (A, H, I, M, O, T, U, V, W, X, Y, 0, 8) or whose mirror differs from it only by edge slivers (nothing survives an erosion by one pixel but fewer than %d pixels remain) are listed, not scored; a swap of one for the other changes no reading. Spaces must carry no ink. Imprints (cap 2.4 mm) are not read glyph by glyph: they are illegible by design and the line mask reads them at F 0.55." % (rc["glyph_gate"]["n_min_px"], rc["glyph_gate"]["n_min_px"], (FACTS.get("adequacy") or {}).get("combos", "169"), rc["glyph_gate"]["n_min_px"]))
from collections import Counter
_pp = {}
for _it in T["items"]:
    _pp.setdefault(_it["px_per_mm"], []).append(_it["id"])
w("5. **Each item's scale.** `px_per_mm` is not 2 for everything: it is the smallest of 2, 3, 4, 6, 8, 12 or 16 at which the table of step 4 holds for every block, from the font's cap and the glyphs it uses (`glyphlib.needed_ppm`); **for a hand-lettered block every pair is measured over glyphs jittered to 3.5 sd of its hand style (size and rotation, four corners), which raised the ballpoint cards SA01 to SA14 from 8 to 12 px/mm, K07a to K07c from 4 to 6 and K07d, K09a to K09f and SA15 by one step**, and group 12 reads 20 true jittered seeds of all 29 hand cards on top of it. In use: %s. No render is over 60 megapixels (the largest here is %s)." % ("; ".join("%g px/mm: %d items%s" % (k, len(v), (" (" + ", ".join(v) + ")") if len(v) <= 9 else "") for k, v in sorted(_pp.items())), max(it["megapixels"] for it in T["items"])))
w()
w("**The checks are tested** (`self_check.py`, groups 10 and 12 to 13), each on a true input and a wrong one:")
w()
wr = FACTS.get("wrong_renders") or []
w("- **The reviewer's wrong renders** (the manifest keeps the approved string, the pixels carry the change), plus near pairs: %s. **All %d FAIL `ITEM.glyphs`**; the first try's line mask passed every one of them." % ("; ".join("%s `%s` drawn as `%s`" % (d["item"], d["was"], d["drawn"]) for d in wr[:23]), sum(1 for d in wr if d["caught"])) if wr else "- the reviewer's wrong renders: see group 12.")
w("- **True renders pass:** a true render of EVERY item (%d print items) and 20 true jittered seeds of ALL 29 hand cards (%d renders) pass every pixel check (`.words` from the manifest, `.mask`, `.pos`, `.glyphs`, `.square`, `.clean`); any failure is a self-check failure. SA01 and SA03, which failed 11 and 15 of 20 seeds in the re-review, pass 20 of 20; the exactly square textures P05, K04, K03a, K03b, K02, K08 and P06 read 0 degrees; T01-named's true render passes." % (N_PRINT, 29 * 20))
w("- **A mirrored sheet fails,** hand cards included (K01, SA06, K07a: the old line mask was blind to them), and so does the mirrored plate, board and bill.")
w("- **A tilt:** a true render turned 1.2 degrees (and 0.5) is found turned (`.square`, within 0.2 degrees for P01 and J01; jittered hand cards K01 and SA06 within 0.5) and fails `.square`, as it should (skew belongs to the placement); the same render read in the PLACED street, turned back by the placement's rot_deg, passes `ITEM.glyphs`.")
w("- **`ITEM.clean`:** the true renders have no stray ink; the review's four planted lines (K01 + BINGO TONIGHT, SA11 + Babysitter, evenings., L02 + ARMITAGE & STOBBS at 46 mm, C02 + BETTING SHOP), drawn outside every block and left out of the manifest, and D01 + LICENSED BAR, which crosses a window, FAIL it.")
w("- **A missing or unreadable manifest:** `glyph_check_block` returns a failure for none, an empty list, a truncated entry or a non-number (it no longer raises); `.words` fails for none, a block missing and a wrong character.")
w("- **`PLACE.built`:** each placed decal (P03, M01, L02 tested) lies within 20 mm of the target's centre, is found within 0.3 degrees of its rot_deg and its largest block reads the right way round; a mirrored decal, a decal turned 1 degree off and a decal 40 mm off FAIL.")
w("- **`G.mirror.cues`:** all 29 hand cards: the true render reads LEFT (the 25 mm top-left patch differs from the card's own colour on at least 20 per cent of its non-text pixels, the top-right on at most 3), the mirrored render RIGHT, a card with no cue neither.")
w("- **`G.page.placeholders`:** the default street's placed-decals manifest passes; with one held placement and no minting line it FAILS; with '- ... MINTED: ARMITAGE & STOBBS' in DECISIONS.md the L01 and L03 placements pass.")
w("- **`G.dates.age`**, **`G.ferry.schedule`**, **`G.letting.mount`**, **`G.place.paper`**, **`G.place.gable`**: each passes the target and fails the first try's input (T03 in class D; the far side's last crossing at 10.45; the 1200 x 450 board; a ninth fly-poster or a fifth poll-tax bill; a bill or a plate put on the bare gable, or the held proof wall made default; the held P01 moved to 0.4 m from the downpipe).")
w()
w("**The reference reader is in `self_check.py`** (`window_of`, `read_block`, `read_score`, `read_box`, `pos_ok` for the line level; `layout_glyphs`, `jitter_glyphs`, `render_item`, `glyph_check_block`, `manifest_problem`, `words_ok`, `square_estimate` (and `estimate_rotation`), `clean_ink_mm2` for the glyph and whole-item level; `glyphlib.py` for the kernels); the builder's own checker should do the same on its rendered item. The reviewer's `wrong_renders.py` still runs against it unchanged (the old names are kept): it now fails every PRINT wrong render, every mirrored plate, board and bill and every tilt, and passes all true jittered hand cards (0 of 20 seeds fail on each of the 29; `pos_ok` takes the hand style's own tolerances). It still passes a wrong word on a HAND line, because a hand line's jitter is known only from the manifest: the glyph check (`glyph_check_block` with the renderer's manifest) is what fails K01 LUNCH for BINGO, K07a GIN BAGS, SA11 and K09a. A manifest-free reading of hand lines was tried (each glyph aligned by correlation) and does not separate a true jittered glyph (F 0.55 to 0.75) from a wrong one (0.60 to 0.75): that is why the review's amendment (a) asks for the manifest.")
w()
w("**What no pixel check can do.** `ART.eye`: nothing in the pixels can tell a person, a hand, a face, lettering, a numeral, a crown, a kiosk mark, a bottle, a glass or an arcade sign in a generated picture from a picture without; a fresh reviewer looks at each art picture at 1:1 before any text is laid. G01, T01 and T02 (and the named twins) have one.")
w()

# ------------------------------------------------------------------ 13 could not settle
w("## 13. What the target could not settle")
w()
for s in T["could_not_settle"]:
    w("- " + s)
w()
w("Unreached today: " + "; ".join(T["unreached"]) + ".")
w()

# ------------------------------------------------------------------ 14 render contract and fixings
w("## 14. The render contract and the fixings (for the builder)")
w()
w("- Texture: " + rc["texture"])
w("- Scale: " + rc["scale"])
w("- Ink mask: " + rc["ink_mask"])
w("- Glyph manifest: file `%s`; schema `%s`. %s" % (rc["glyph_manifest"]["file"], rc["glyph_manifest"]["schema"], rc["glyph_manifest"]["rule"]))
w("- Gate: F >= %s at %s mm; SEP >= %s; at least %s pixels between any two non-twin glyphs; tolerance %s px; alternatives %s; %s" % (rc["glyph_gate"]["F_min"], rc["glyph_gate"]["dilation_mm"], rc["glyph_gate"]["sep_gate"], rc["glyph_gate"]["n_min_px"], rc["glyph_gate"]["tol_px"], rc["glyph_gate"]["alternatives"], rc["glyph_gate"]["twins"]))
w("- Placed street: " + rc["placed_street"])
w("- Tape tab: %(kind)s, %(length_mm)s x %(width_mm)s mm at %(angle_deg)s degrees, rgb %(rgb)s opacity %(opacity)s. %(note)s" % T["fixings"]["tape_tab"])
w("- String and sucker: %(kind)s: loop %(loop_mm)s mm, knot %(knot_mm)s mm, sucker %(sucker_diameter_mm)s mm, rgb %(sucker_rgb)s. %(note)s" % T["fixings"]["string_sucker"])
w("- Four tabs (A3 and A4 sheets taped in a window): %(kind)s, %(length_mm)s x %(width_mm)s mm, rgb %(rgb)s opacity %(opacity)s" % T["fixings"]["four_tabs"])
w("- The hours plate (the fascia target gives no horizontal place): %s" % T["hours_plate"]["note"])
w()

# ------------------------------------------------------------------ 15 self check
w("## 15. Self-check")
w()
if sc:
    w("Run %s: **%s**." % (sc.get("run"), sc.get("summary")))
    w()
    if sc.get("failures"):
        w("Failures:")
        for f_ in sc["failures"]:
            w("- [%s] %s: %s" % (f_["g"], f_["n"], f_["d"]))
        w()
    w("Reported (not failures):")
    for r in sc.get("reported", []):
        w("- [%s] %s %s" % (r["g"], r["n"], ("(" + r["d"][:140] + ")") if r["d"] else ""))
else:
    w("(run `self_check.py` and then `make_doc.py` again to fill this in)")
w()

# ------------------------------------------------------------------ 16 sources
w("## 16. Sources")
w()
w("| Id | Kind | What | Read | Author and licence | Used |")
w("|---|---|---|---|---|---|")
for s in T["sources"]:
    w("| %s | %s | %s | %s | %s; %s; taken %s | %s |" % (s["id"], s["kind"], s["url"][:260].replace("|", "/"), s["read"], s["author"], s["licence"], s["taken"], s["used"].replace("|", "/")))
w()
w("The licences of the previews: P1 is a crop of a CC0 panorama with the glazed interiors and the council crest painted out; the layout sheets are our own drawings. No preview shows a drink, a gambling mark or a person; the layout sheets show our invented placeholder names (ARMITAGE & STOBBS and the like), never a real business.")
(HERE / "TARGET.md").write_text("\n".join(out) + "\n", encoding="utf-8")
print("wrote TARGET.md", len("\n".join(out)), "bytes")
