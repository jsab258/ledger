Method researched: SUMMARY-2026-09-29.md

# Target: Rita's three known shortfalls (17 Nov 2026)

Order 16 Nov, waiting item 10. What each fault is, the smallest fix, the checks; not the build. Files read 17 Nov. "Unverified" means no source read settles it. Two tries are spent on each fault; a third needs his yes.

## 1. The faults

**A. Rita's broken window** (the pawnbroker's bay).
- First report 6 Nov 5:31: "black zigzag pane edges, flat black shards, goods untouched" (production/archive/DECISIONS-to-2026-11-09.md line 1094). Again 7 Nov: "a white zigzag outline" (production/audits/phase1-exit/REHEARSAL-2026-11-07-A.md, item 3).
- Shows: packaged street after the deed, near, from the pavement and across the road; night hardly reads.
- Try 1: pane's own see-through glass, pale tilted shards: read as open. Try 2: dirty glass (opacity 0.3), 12 mm pale rim, four-to-six-sided shards: smashed by day, but "the rim reads as a drawn outline, with no glass sheet behind it", night looks whole, no glass on the ground, chips sparse and paper-white (DECISIONS line 1110, 6 Nov). Code: ue-probe/Source/LedgerProbe/Private/VignetteShot.cpp lines 7660 to 7671. NOTEBOOK 6 Nov: next, facets and varied edge thickness, a sheen from a real reflection, ground pieces lit at night, near pictures first.

**B. The wall dish's black centre.** The dish is on the cab office's wall (terrace-front.py DISH_AT 8.35, 5.60), not Rita's bay; same list.
- First report 8 Oct: "satellite dish low-poly with a flat black wedge (high)" (production/audits/phase1-exit/GATE-1.1-REVIEW-3.md, V1). 21 Oct: its bracket "shows through its face" (production/audits/gate-lamp-post-C/GATE.md).
- Shows: hook camera, day.
- Tries (6 Nov): 12 sides to 48 and a set-back bowl; the arm moved to rise from the rim. Round now, but the wedge never moved, so the arm was not the cause (DECISIONS lines 1111 to 1112; NOTEBOOK 6 Nov). Cause unread.
- Candidates from the code (terrace-front.py _dish, lines 2907 to 2937), all unverified: 48 triangles meet one centre point, so smoothed normals pinch there; by hand arithmetic the bowl face and back face wind opposite to the rim's order (the export may flip it); the dish is 0.6 m across, near the 30 cm radius below which software Lumen drops parts (street-weathering skill section 5; not measured here).

**C. Worn paint at the front's edges.**
- First report 8 Oct: "pilaster, door panel and mullion smooth even paint, well short of the Hook sheet" (GATE-1.1-REVIEW-3.md, V7); 7 Nov "joinery above the foot crisp" (REHEARSAL-2026-11-07-A.md).
- Shows: Rita's square and left views, and the hook.
- Tried: projected chips (7 Oct) landed on nothing or streaked; an edge mask on the street's shared meshes (30 Oct) lit the chandler's pier at night, cause not found; geometry flakes (7 Nov, two tries) read as jagged confetti and rust (DECISIONS line 1144; NOTEBOOK 7 Nov). Rita's baked copy carries chips only at the door's bottom and lock rails and the sill's nose (production/research/street-wear/FRONT-WEAR-BAKE-2026-10-22.md section 5); whether they show packaged: unverified.

## 2. What 1990 looked like

- **Broken pane.** production/reference holds no photographs. Historic England records DD000890 and DD001449 returned 403. A search result (not opened) described a British Library photograph of a broken window boarded from inside with posters on the plywood. Board, tape or crack in 1990: **unverified**.
- **Dish.** Sky's first service began 5 Feb 1989 and merged with its rival 2 Nov 1990 (https://en.wikipedia.org/wiki/Sky_Television_(1984%E2%80%931990), read 17 Nov); the rival's square antenna launched 25 Mar 1990 (https://terramedia.co.uk/reference/documents/BSB.htm, read 17 Nov). A dish in 1990 is therefore plausible: **verified from secondary pages only**, no primary source. The 60 cm size rests on a search result: **unverified**. Citable by his ruling of 22 Sep (production/reference/README.md); the household research it cites was not found.
- **Worn paint.** Target from Mafia's data: 3 to 10% of the joinery, within 5 cm of an edge or the handle (production/research/street-wear/MAFIA-WEAR-2026-10-28.md, O3). No 1990 photograph read: **unverified**.

## 3. Mafia and Kingdom Come II

- **Glass.** Mafia, names only, files unread (production/research/aaa-reference/BREAKABLE-GLASS-NAMES-2026-11-06.md): a destructible window as geometry-collection pieces plus a broken-glass mesh; a damaged and a destroyed window mesh; shard material M_FakeShardsGlass (subsurface; refraction, fresnel colour, grunge); a glass-shard debris mesh. No numbers. KCD2: a broken-glass material and two broken-window meshes by name; unread.
- **Edge wear.** Mafia, measured: M_General_1_Layer_Paint_Chipped on 48 instances, paint over wood from a trim sheet; medians fade 0.89, weathering opacity 0.66, dirt 1.25, dirt roughness 0.80, wood mask edge 2.3, roughness 0.32 (MAFIA-WEAR-2026-10-28.md, layer 2). The chip is a material mask, not geometry. KCD2: none found.

## 4. The smallest fixes and checks

- **A (his yes).** One glass sheet in the frame with jagged edges of varied thickness, replacing the rim; glass parameters after the shard material's names; lit pieces on sill and pavement. Photograph near views first. Check: one small review per view, near (2 m), pavement, across the road, day and night, beside the old picture.
- **B (diagnose first, at no try's cost).** Hide the dish alone; flat-shade it; flip the bowl's winding; enlarge it; film each at the hook camera. Likely fix: rim-to-hub quads with per-face normals. Check: hook crop at 100% and 200%, and from below; no black pixel inside the bowl.
- **C (his yes).** Material only, on Rita's baked copy (RULINGS line: new trims go in the material only): widen the baked chip regions to the outer arrises of pilasters, cornice and mullions, never every moulding, baked at 4,096 (street-weathering skill section 3). Check: 3 to 10% within 5 cm of an edge; clean paint within 1.5% of before; no lit pier at night; Rita's ten views beside F:/LedgerTools/gate/last-good/ritas-front; then the packaged walk.

## Unreached

Historic England DD000890 and DD001449 (403); bairdtelevision.com (no connection); the British Library record; every F: review file and picture named in DECISIONS (folders absent); any 1990 photograph; Mafia and KCD2 glass files.
