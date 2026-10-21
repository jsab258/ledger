# Bringing the cloud's shopfronts into the game: the map (21 October 2026)

His order of 21 October, item 5: "Rita's front and the three passed shops with their rooms behind the glass" first. A read-only helper mapped the repository the same day; file and line references are its, checked where marked. CW = production/cloud-week/kit/shop-windows; TF = tools/art-recipes/terrace-front.py; VS = ue-probe/Source/LedgerProbe/Private/VignetteShot.cpp.

## The cloud's build

- One command per shop: build_shop.py --shop <id> (build_ritas.py calls it). Stages: assets (Poly Haven 1k models and textures, makers' marks painted out), paper (the 4.1 fascia set), front (<id>_front.glb; Rita also a night grille), display (<id>_display.glb), room (three 4096 x 1855 pictures and a JSON), gate, checks. Each stage runs in its own Python with Blender 5.2.2 as a module (LEDGER_BPY; the cloud's was a Linux venv).
- Needs numpy, scipy, Pillow, shapely. Pillow without Raqm changes text hashes, not the pictures' checks (fascias NOTES).
- Linux paths to replace: the scratch default (build_shop.py:35, sw_ctx.py:17, sw_assets.py:25, sw_display.py:665, sw_prints.py:30: set LEDGER_SW_SCRATCH), the gate's sky HDRI (sw_gate_run.py:57, no fetch code), the OCR second reader (check_try3.py:384-394; without it only row INV-08 fails).
- Downloads, all CC0 but one public-domain text: F:/LedgerTools/polyhaven already holds Rita's models; 14 of the 91 ids the four shops need are missing (ironmonger 11, newsagent 1, tea rooms 2), and no HDRIs or ambientCG files.
- Times on the cloud's 4 CPU cores: Rita about 1.6 h (room 63 min, gate 28 to 37 min); the others 3 to 4 h each. Cycles is set to the CPU in the code.

## The frame

- Front glb: metres, pivot at the bay's middle, at the wall face, on the footway; x along the bay (u from the viewer's left), y = -depth (the street toward -y), written y-up. East (Rita): street x = 21 - u/1000 (middle 18); west: low end + u/1000 (tea rooms 27, ironmonger 33, newsagent 39). Joinery, glass and a plaster hall only: no brick (PC-04: the street must close the gap behind each pilaster).
- **Datum conflict to settle first**: the cloud's wall face is 5.295 m from the crown line, the game's frontage 5.125 (TF:573, brick 0.215 behind it); Rita's current glass 5.075 to 5.098, the other bays' 5.245 to 5.265; the cards 5.875. The cloud's glass back face (5.265) and card (5.875) match the game's box glass and card planes.
- Display glb: placed at the window zone's middle (window_cx +0.975 for Rita and the tea rooms, -0.975 for the others), y -0.025, z 0.600 from the wall; for Rita street x 17.025 where shop-interiors.json has 17.125.

## The game today

- TF plan_parts (5291) builds a bay: pilasters, stallriser, glass, frames, shop door, side door (1278), fascia, cornice, consoles, blind box, sign. No per-bay switch; precedents for taking a bay out: MICKEYS_OWN (7996), per-bay glass keys (8020), STREET_GLB_SKIP (7970), the runtime hide_meshes (VS 7748). KIT_BAYS (3171) already replaces Rita's front with the old kit.
- Rita's smash-window shards are built from that old glass (TF 3534-3538, 3643; CrimeProbe.cpp 1706): the crime must keep working.
- shop-interiors.json has only mickeys and pawnbroker; ApplyShopInteriors (VS 7644) finds the bay by its decal, reads <pictures>_{day,night_lit,night_dark}.png at run time, places a display from /Game/Ledger/ShopDisplays (import_shop_displays.py reads only the checkout).
- The ironmonger, newsagent and tea rooms have flat cards only (TF 2795-2797); west_north is drawn one storey, so the cloud's hanging-sign plates have no brick above them.

## Owed to the PC (the cloud's list, one line each)

PC-01 a marker at the picture's centre moves as predicted; PC-02 the night window bed's mean luma at least 45 with the game's spill, the pool the game's; PC-03 the glass, motion vectors, exposure and frame time; PC-04 no sky inside the bay's outline at STREET_30; PC-05 wear on the joinery, 128-sample pictures, the return walls and hall meeting the card; PC-06 the night fascia name's luma ratio at least 1.3, else a light for his page; PC-07 the display's two strip lights, their lumens measured.
