---
name: slate-roofs
description: The one way LEDGER builds and dresses a slate roof and its roof line, as phase 1 proved it on Quay Street and the corner. Covers the target first (the Hook sheet, period numbers), the roof geometry in the street recipe (both slopes, one slope and gutter per row, the ridge capping, lead strips at the party walls, stacks, caps, pots, aerials), the slate's real values, the slate scan tile and how to hold down its pale, glossy flecks, the views that see roofs (the street cameras and the hill), the review and the packaged pass. Use it whenever a roof, ridge, chimney stack or pot, gutter, eaves or party-wall break is built, changed or judged; whenever a roof reads as a flat slab, a hole, a black bar, a dark seam, paint splashes, snow, chalk or one long roof over many houses; whenever a new row, house or shop is added under a pitched roof; and before any change to the slate, flashing or roof rows, even if nobody says "roof".
---

# Slate roofs and the roof line

What phase 1 proved: the corner's step 9d (5 November 2026: the slate scan, two tries; the roof's breaks, two tries), the 7 October seam fix, the 22 September and 3 October roof-line work, all in tools/art-recipes/terrace-front.py and tools/art-recipes/dressing_tiles.py. Plan: production/art/corner/STEP9-PLAN-2026-11-03.md ("9d", from the midweek review's "the roof one flat grey slab, no slate courses, ridge or party-wall breaks, chimneys without pots"). Evidence: F:/LedgerTools/gate/new/corner-9d-2026-11-05 (r2, r3, r5 reviews) and F:/LedgerTools/gate/new/corner-packaged-2026-11-06 (the packaged reviews). Not repeated here, used from: .claude/skills/street-weathering/SKILL.md (bands, wet ground, wear, night), .claude/skills/asset-import/SKILL.md (fetching a scan, licence, catalogue, game inputs, re-import), .claude/skills/gate/SKILL.md and .claude/skills/packaged-walk/SKILL.md. Sources: production/research/skills/SLATE-ROOFS-SKILL-SOURCES-2026-11-08.md; review: SLATE-ROOFS-SKILL-REVIEW-2026-11-08.md (PASS WITH FIXES, applied). "Check first" marks what the sources do not settle.

**Reference first** (CLAUDE.md, "his rule, 28 October"): Mafia bakes its roofs from a hand-made shape through a Houdini building generator (585 roof meshes game-wide; production/research/aaa-reference/studies/04-street-world.md); its joinery and ironwork "sample fixed strips of a sheet at one scale", at a cooked street median of about 575 px a metre (production/research/phase5-procedural/MAFIA-KIT-2026-10-28.md §2). Our roofs follow the second (a scan row on the roof at a fixed density); the first is phase 5's (MAFIA-KIT §5.1: a house family with end, party-wall and chimney pieces). Neither game gives a slate albedo (SURFACE-BANDS-2026-11-02.md §7: none found). No Kingdom Come II roof method was found in the files read: unverified; look in its study before a new roof kind.

**Values live in their homes, not here** (CLAUDE.md, one home per fact): each block's pitch in production/specs/vignette-scene.json's blocks ("roof.pitch_deg", overridden by the block's "drawn" numbers, DECISIONS 3 Oct; read at terrace-front.py line 1169); the roof line's chimney and downpipe sizes in the same file's "roofline". That "roofline" also holds gutter (0.112 m) and aerial rows the recipe does not read: the code's GUTTER_* and AERIAL_* win. In terrace-front.py: GUTTER_*, RIDGE_CAP_*, PARTY_LEAD_*, STACK_CAP_*, POT_*, AERIAL_* and the slate and flashing palette rows. The scan's cut and hold values in dressing_tiles.py TILES; the scan row in production/specs/ps5-corner.json "scanned" (base slate). Change a value in its home and re-export, never in prose.

**Always:**
- Look at the target before choosing the detail (RECIPE 5 Nov, "Breaks in a long roof": an upstand wall was assumed; the Hook sheet shows only a thin line).
- Measure a scan's tone and gloss together before changing either (RECIPE 5 Nov, "Pale, glossy patches").
- Give any new roof part its own material row; never borrow a shared row (the near-black lead row drew the flashing as black bars; the "lead" and "stone" rows also hold gutters, letterplates, sills and the backdrop's lead bay roofs: STEP9-PLAN 9b).
- Two tries per fault; a third needs his yes first (CLAUDE.md). Each roof fault on 5 Nov passed on its second try.
- A roof change reaches every roof in the street (one mesh per material row: STEP9-PLAN, measurement): gate every view that sees a roof, not only the corner's.

## 1. The target

- The Hook sheet: wet dark slate that mirrors the sky; no brick upstands at the party walls, but a thin pale lead line down from each stack and a dark ridge (DECISIONS 5 Nov 15:53); a black cast-iron gutter over a dentil course, nothing pale at the eaves (terrace-front.py, eaves note of 22 Sep); three or four pots a stack, terracotta with the odd buff replacement (terrace-front.py plan_pots, 4 Oct). Its slate read 61/58/61 on the near parade and about 117/112/107 on the hill (terrace-front.py palette note, 22 Sep; check first whether 8-bit sRGB).
- Period numbers, all unverified against a measured photograph (TERRACE-KIT-TABLE-2026-10-29.md §2, status U): pitch 35 degrees (single-storey cottages drawn at 40, DECISIONS 3 Oct); stack 0.90 x 0.45 m, about 1.0 m above the ridge; cap two courses stepping out about 56 to 60 mm; pots 600 mm high, 280 to 240 mm across; gutter 112 to 115 mm half-round. Photographs win over trade sizes (RULINGS 8 Oct, as the table cites it).
- Held pot meshes at 0.67 and 0.95 m across are whole stacks, not pots: build pots at a pot's size (terrace-front.py, 22 Sep note).
- Aerials: a yagi about 1 m across with 0.27 m elements (half-wave at 550 MHz), on two stacks of five, elements across the street so they read as a comb (terrace-front.py AERIAL_ON_STACKS).

## 2. The geometry, in the street recipe

- terrace-front.py _roof_and_rainwater: two slopes to a ridge along the street, both built (a half roof reads as a fault from the eye camera); the eaves course and a black gutter; the downpipe at a party wall, never a row end; a parapet row gets a coping and no stack.
- One slope each side and one gutter per row, end to end (ROW_CONTINUOUS, _one_per_row; DECISIONS 7 Oct). Per-house slopes overlapping 0.3 m in one plane flickered into a dark seam at every party wall. Climbing, stepped rows keep per-house roofs. A self-test fails without it.
- The breaks between houses: a ridge capping 0.18 m wide, 0.03 m high on the slate row; a lead strip 0.10 m wide, 15 mm proud of each slope at each party wall on its own "flashing" row (DECISIONS 5 Nov 15:53). Proud of the slope, so no new mesh kind is needed (RECIPE 5 Nov).
- Stacks on party walls; a building standing alone gets an end stack (end_stack) or reads wrong; caps oversail 0.06 m, 0.15 m high; pots stand on the cap's top so nothing floats.
- Houses turned on a curve or ending a row need their own sides and gables, or the room box's side and the roof's underside show as a black block (DECISIONS 7 Oct). A front taller than its host is cut at the eave, a thin bed moulding kept under the gutter (RECIPE 23 Oct). No sign bracket on a single-storey roof (RECIPE, the ironmonger).
- After the export: re-import the street (tools/ue/import_street.py, by the asset-import skill; memory note reimport-street-after-export) before any picture.

## 3. Real values

- Slate band (SURFACE-BANDS-2026-11-02.md §4, reviewed PASS WITH FIXES): dry base colour 0.06 to 0.15, centre 0.09; wet base colour 0.045 to 0.09, the water film's 0.02 giving the shine. Welsh or Westmorland tint not found: unverified.
- The slate row (0.060, 0.058, 0.062), roughness 0.70, read 0.061 on 2 Nov, in band at the bottom (production/art/corner/BASELINE-2026-11-02.md); not re-read since the scan went on: check first.
- A roof faces the bright overcast sky, so a mid-dark albedo reads light in the frame: 0.15 came back pale against the sheet (terrace-front.py palette note, 22 Sep). Judge in the lit frame as well as by band.
- Flashing: weathered lead grey, linear 0.19 to 0.215, roughness 0.55 (terrace-front.py "flashing"). How the street's wet film reaches the roof rows was not read: check first in the look file before calling a roof dry.

## 4. The slate scan

- Source: Poly Haven roof_slates_03, CC0, 3 m a tile, looked at before use (dressing_tiles.py docstring; asset-import skill for licence and catalogue lines).
- It is a trim sheet: a ridge and hip course across its top. Cut only the rows between two course lines where it wraps cleanly (366 to 1,995 of 2,048, found by searching for the least difference); keep the full width, already periodic; never cross-blend it, which smears regular courses (dressing_tiles.py TILES note). Seam limit 3.0, since its seam lies on a naturally darker course line.
- Size: squeezed to a 1,536 px square over 3.9 m, so slates read 26 cm wide at a 17 cm margin; the source's 20 x 10 cm read small. That this is "a Welsh terrace's" size rests on a code comment only: unverified (no slate size in TERRACE-KIT-TABLE; SURFACE-BANDS found nothing on Welsh slate). Maps come packed (a GL normal, roughness in the green channel).
- Density, measured: 1,536 px over 3.9 m is about 394 px a metre, 23% under the floor of street-weathering's C6 band (410 to 614); the slate's side_px overrides dressing_tiles.py's "512 px a metre by construction". The scaling is uneven, about 1.3 across against 1.63 down (2.39 m of source rows stretched over 3.9 m). No exception is recorded in DECISIONS, RECIPE or ps5-corner.json, and the reviews judged size only by eye. A known shortfall: the next change to the tile either records the exception in DECISIONS or brings it inside the band.
- Colour brought to the row's palette by match_rgb, as the other scan rows (ps5-corner.json).
- The trap of 5 Nov, try 1: the scan as photographed read as white flecks, "paint splashes or snow", on the near roof in the reverse view (r2-review.md). Measured: the pale worn patches were also the glossiest (roughness 0.35 against 0.56), so they flashed at the roof's grazing angle. Try 2: tone above the tile's median keeps 30% of its lift and loses half its colour at the top (hold_pale 0.3, hold_pale_grey 0.5); roughness under the median keeps 20% of its drop (hold_gloss 0.2). Darks and rough parts untouched; regrade after (DECISIONS 5 Nov 15:30; r3-review.md PASS).

## 5. The views that see roofs

- Roofs show most in the reverse view (the near right roof decides) and cam_A; cam_B is nearly edge-on and crops the pots; in the hook view the roofs are mostly out of frame (r5-review.md; DECISIONS 5 Nov 14:52). Take day and night of every page view: 9d's reviews used five views by day and night.
- The hill's far roofs carry the roof line against the sky: in the reverse view they read paler, bluer and a little chalky (r3-review.md, listed). Dark triangles seen on hill roofs in November were the hill trees' large leaves, not the slate (RECIPE, hill trees; DECISIONS 4 and 5 Nov): look at what lies on a roof before changing it.
- No chimney smoke: the Hook sheet shows none at this distance, and local fog volumes drew nothing in two tries; if it is ever wanted, the method is sprite particles that take the height fog (chimney-smoke/NOTE-2026-10-03.md; DECISIONS 3 Oct).

## 6. The checks, the review, the packaged pass

- Readings first, by the street-weathering skill's step 2 (a box on the slate in the base-colour view, in band), then the gate skill, each view beside its last good picture and the Hook sheet. Reviews are sized to the piece (RULINGS 3 Nov): only a small texture or setting fix goes to one small reviewer as a batch, as 9d's editor rounds did; a roof change reaching every roof in the street is a medium piece, one view per fresh reviewer, never a bundle (the gate skill), and the packaged final reviews go one view per reviewer, as on 6 Nov.
- The bar used on 5 Nov: no flecks or blotches by day or night; no visible repeat; courses along the eaves, the right way, not stretched; each house reads as its own roof; strips run eave to ridge and stop at it, nothing past a gable or row end, no strip through a wall, a parapet row or a stack; nothing glows at night (r3-review.md, r5-review.md).
- Editor passes are screens: the corner's roofs passed packaged on 6 Nov (build 3641d53, hook and reverse by day and night, fresh final reviewers, matching the editor within 0.2 of 255; DECISIONS 6 Nov 6:01). Then the packaged walk skill.

## What it cost, and what is still short

- Cost (RECIPE 5 Nov): the first scan try about 0.5 h, shared with the upper walls' wash and the kiosk; the second about 10 minutes; the breaks about 25 minutes. The 7 Oct seam fix: not recorded.
- Known shortfalls, listed, not failing alone. In the editor (r3-review.md, r5-review.md): the strips darker than the sheet's pale line where the light misses them; no broken or ragged ridge ends, no gaps at stacks; the slate pattern flat against the bar; the near roof's upper part flat with faint courses; far roofs chalky; no moss; slate size not measurable at game distance. Packaged, 6 Nov: the lead strips and ridge capping read as hard, even, near-black lines on both roofs (review-reverse.json); the quay-end roof's strip reads pale and clean, like a painted line (review-hook-day.json); a thin orange fringe where the slate meets the near left gutter (review-hook-day.json). The tile's density, under C6's band (step 4).

## Records, every piece

DECISIONS.md: one entry per choice and per try, the try count named, its evidence folder. RECIPE.md: a few setting-free lines when the unit ends. CATALOGUE.md and THIRD-PARTY.md lines for any new scan (asset-import skill). Pictures stay on F:; previews only as JPEG in production/previews/.
