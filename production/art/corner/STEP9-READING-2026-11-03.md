# Step 9 reading, 3 November 2026

Read from the project's own files on 3 November 2026. Plan line: CORNER-PLAN-2026-11-02.md line 33 (1.0 h; check: 512 px a metre within 20%, worn paint 3 to 10% at edges, asset_checks.py, no lit pier at night).

## 1. The chandler's timber sheet and painted wood
- Sheet: tools/art-recipes/wood_trim.py lines 18-28. 2,048 px square, Poly Haven kitchen_wood (CC0) tiled 7 times, 4.2 m a side, 487.6 px/m (inside 512 within 20%, i.e. 410 to 614). Three strips: boards (v 0 to 0.75), narrow members (to 0.875), end grain (last eighth). Three maps: colour, normal, masks (bare-wood roughness R, chip noise G, dirt B).
- Mapping: tools/art-recipes/front_joinery.py lines 12-19. Each loose part gets a second UV set (TEXCOORD_2) laid flat at the sheet's 487.6 px/m, grain along the part's longest side, strip chosen by part width or end-grain facing, seeded position per part. UV 0 stays the paint picture; UV 1 is left to Unreal's lightmap. The chip picture is baked on UV 0 (lines 20-28). ChipAmount is solved so worn/bare paint falls at 5% (target 3 to 10%; lines 32-34).
- Material: tools/ue/make_kit_materials.py lines 376-395, M_LedgerKitPaintWood. Samplers PaintMap/PaintORM/PaintNormal/EdgeMask on UV 0; WoodColour/WoodMasks/WoodNormal on UV 2. EdgeFromBox mode for repeating-UV parts (fascia lettering).
- Spec: production/specs/shop-fronts/chandler-front-joinery.json (made-values in chandler-front-joinery-made.json). Settings read: WornWidth 1.6, target_note says aimed at 5%.
- Result on the chandler: RECIPE.md lines 167-178: worn 7.9%, cost about 2.7 h (helper plus waits); one check not met (a brick strip lit at night on the rebuilt mesh, cause not found).
- Not found: a "timber sheet" entry in production/specs/kit-materials.json (only a note "painted steel, aluminium or timber" at line 14).

## 2. How Mickey's front is made
- tools/art-recipes/terrace-front.py. MATERIALS rows: frame_painted (0.0625, 0.0875, 0.119) rough 0.35, line 287; paint_fascia (0.030, 0.022, 0.030) rough 0.45, line 307; stone (sills, lintels, coping) line 167; lead (downpipe) line 318. Mickey's is bay ("east_parade", 0): frame frame_painted, stall tile_patterned (line 847); fascia sign fascia_mickeys_plain with raised letters (lines 887-888). Pilasters come from the shopfront kit (line 3211; KIT_REPLACES line 3234); the cornice and console brackets are fascia_cornice_01 and fascia_console_01 (lines 59-64).
- Line 716 comment: these paints read in Unreal as rough stucco on every sash, fascia, pilaster and door.
- No Mickey's file in production/specs/shop-fronts (only chandler, Rita's, tea rooms, grocer, ironmonger, newsagent, launderette). So no Mickey's joinery or wear spec exists (not found).
- What would move onto the sheet (inferred): frame, pilasters, door, fascia board and cornice parts, by the chandler's route: a joinery spec for Mickey's, front_joinery.py to add UV 2 and chip pictures, import_front_joinery.py, the PaintWood material.

## 3. Trim sheets in the research; stone and metal sheets
- MAFIA-KIT-2026-10-28.md lines 89-100: 35 trim sets; wood sheet on 21 meshes (3,513 slot placements); blinds 171; paving 108; library 3,792 of 35,423 (11%); ironwork trim 5,321 (15%); together 26%. Wood sheet about 1,000 px/m authored, 490-500 cooked. The strip layout was not read (line 240).
- Our target: lines 166-167: three 4096 x 2048 sheets at 512 px/m (timber; stone and stucco; metal for railings, gutters, pipes), each piece within 5% of its sheet's density. Line 217 costs "render" wall kind and three sheets at 8 to 12 h.
- TERRACE-KIT-TABLE-2026-10-29.md line 77: T, S, M are the timber, stone-and-stucco and metal sheets; line 116: gutter 1350, half-round 112, sheet M, candidate Poly Haven modular_metal_gutter (CC0); line 101: door sheet T.
- Existence: only the wood sheet exists (wood_trim.py). Grep of tools and specs (json, py) for stone/metal trim sheet found nothing. Not found.

## 4. Pieces in the 30 m
- Sills and lintels: terrace-front.py builds them as boxes with the flat "stone" row (line 167, 0.24/0.225/0.20, rough 0.8): e.g. gf_sill boxes, lines 1491-1492; sill/lintel thickness and projection from the spec (lines 1173-1176); the window heads on the terraces are segmental brick arches (line 1524).
- Downpipe: "lead" row (line 318), diameter from the spec (line 1180); three downpipes leaning (line 1032).
- Gutters: no gutter piece found by grep in terrace-front.py beyond a roofline spec; the kit-table lists a gutter mesh as planned only. Not confirmed. Which of these sit within the corner's 30 m (Mickey's, fish shop, Rita's, kiosk) was not counted: unverified.
- All use flat colour rows, no sheet and no UV density.

## 5. Smallest useful first part (inferred)
- One sheet, one set: Mickey's frame, door, pilasters and fascia onto the existing wood sheet and M_LedgerKitPaintWood. No new sheet to build; the chandler's route is proven.
- Files: new production/specs/shop-fronts/mickeys-front-joinery.json (from the chandler's), a Mickey's wear spec if needed, front_joinery.py run, import_front_joinery.py, kit-materials.json row, asset_checks.py case.
- Checks: density 410 to 614 px/m; worn/bare paint 3 to 10% at edges; asset_checks.py; no lit pier at night (the one the chandler failed).
- Estimate: 2 to 3 h, from the chandler's 2.7 h (RECIPE.md line 177) with the sheet and material already built, less setup, plus risk from the night-pier fault. The plan's 1.0 h looks short for this (inferred). The time log (production/time-log.jsonl) was searched; no per-step trim figure found beyond the chandler entry.
- Stone and metal sheets are separate, each larger (the plan's research gives 8 to 12 h for all three sheets plus render wall).

## Not reached
None needed; web not used.

## The session's correction (3 November, 22:05)

front_joinery.py works on a cloud shopfront's own glb (front_for_game.py, then front_wear.py: "chandler-front-worn"), and Mickey's front is part of the street's own mesh (terrace-front.py, bay east_parade 0), with no front glb, joinery or wear spec. So the smallest part first means making Mickey's frontage its own front piece, placed in the street's stead (KIT_REPLACES-like), before any trim sheet: far more than the plan's 1.0 h or this note's 2 to 3 h, and on the Hook sheet's hero frontage. Step 9 is an item much bigger than it looked; told to him, planned by day.
