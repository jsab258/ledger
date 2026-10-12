# Rita's shop (unit 7, stage 1): the build

13 October 2026, cloud week 42, part 2. Built by script from `production/cloud-week/targets/shop-windows/target.json` as it stood after the review's fixes (status "fixes applied, not re-reviewed"; the review's TARGET-REVIEW.md read for context, its amendments are in the JSON). Rita's pawnbroker, east_parade bay 2: the whole front, the room behind the glass in three pictures, the near metre as real meshes, and the gate that shows what the game will show without Unreal. Nothing committed or pushed; the target is untouched.

**The check: {{CHECK_LINE}}** (`checks/check_ritas_v1.json`, one row per check of the target that applies, printed as "N of M rows pass").

## What was made

| file | what |
|---|---|
| `build_ritas.py` | the one command: `python3 build_ritas.py` (every stage) or `python3 build_ritas.py front display` (some). Stages: assets, paper, front, display, room, gate, checks. It runs each stage in its own Python with Blender 5.2.2 as a module (`/home/user/.bpyenv/bin/python`) |
| `sw_assets.py` | the 45 Poly Haven models and 2 textures (1k, CC0) fetched into SCRATCH/polyhaven, contact sheets, every maker's mark painted out of the maps, INV-06's script test |
| `sw_front.py` | Rita's front, assembled in Blender |
| `sw_room.py`, `sw_display.py` | the room and its three pictures; the display |
| `sw_gate.py`, `sw_gate_run.py` | the gate: the card baked through the game's `trace` and the renders |
| `check_ritas.py`, `checks/check_ritas_v1.json` | the check and its rows |
| `production/assets/cloud-week/shop-windows/ritas_front.glb` | the whole front (day state: the grille's rail and channel stand), {{FRONT_TRIS}} triangles, {{FRONT_MB}} MB with its textures: over the push guard's 1 MB, so out of git (listed in `.git/info/exclude` as the 3.2 kit did) and rebuilt by `build_ritas.py front` |
| `.../ritas_grille_night.glb` | the night lattice alone ({{GRILLE_TRIS}} triangles, 1.5 MB, out of git) |
| `.../ritas_display.glb` | the display ({{DISP_TRIS}} triangles, {{DISP_MB}} MB, out of git) |
| `.../rooms/pawnbroker_{day,night_lit,night_dark}.png` and `pawnbroker.json` | the three 4096 x 1855 pictures and the JSON beside them (out of git: copies of the masters in SCRATCH/shop-windows/rooms; on the PC the masters go to F:/LedgerTools/shop-rooms) |
| `production/previews/cloud-week/shop-windows/` | the review set (below) |

The review set (JPEG, 1600 px, under 500 KB): `ritas-street-square-{day,night-lit}-2026-10-13.jpg`, `ritas-close-35-{day,night-lit}-2026-10-13.jpg`, the three pictures reduced `ritas-room-{day,night-lit,night-dark}-2026-10-13.jpg`, and for Jafar the before-and-after `ritas-room-before-after-2026-10-13.jpg` (the approved pawnbroker_day.png above the new day picture).

## How to rebuild

`python3 build_ritas.py` from this folder. Heavy outputs go to SCRATCH (`/home/user/ledger-scratch`, override with `LEDGER_SW_SCRATCH`; F:/LedgerTools on the PC). Times on four CPU cores, no GPU: assets about 1 minute (plus the fetch), paper 30 s, front 5 s, display 15 s, room {{ROOM_MIN}} minutes (a 4-minute light calibration, then the three pictures at 64 samples: {{ROOM_TIMES}}), gate {{GATE_MIN}} minutes (the bake through `trace` is seconds a camera; the renders are 2560 x 1440 at 32 samples, denoised), checks 2 minutes. `LEDGER_REUSE_CAL=1` reuses the light strengths of the last calibration; `LEDGER_ROOM_SAMPLES` and `LEDGER_GATE_SAMPLES` set the samples.

## What was kept from earlier work, and what is new

Kept: the 3.2 kit's `Builder` (pilasters, consoles, fascia board, cornice, sill, stallriser, window frame with its nine toplights), imported and called as `build_assembly()` calls it, so every kit number stands (its own 171-row check passed on these parts); the 3.1 door family's F1 for the side door (mirrored, trimmed at the transom, buttermilk leaf, 24.4 mm fillers); the 4.1 fascia set rebuilt by `make_fascias.py` (the board's basecolour, height, orm and wear maps, the three balls' faces, the glass rows) and 4.2's OPEN and CLOSED card from `make_paper.py`; the approved room's box, finishes (the Poly Haven lino and plaster, the 1.0 m brown dado), its three T12 battens, its counter with the scripted jewellery (tori, discs, chains), its notices and its camera rule; the display's velvet bed, a ticket on each piece, the cut of each model to about 4,500 triangles (never by more than 70 per cent) and 512-pixel JPEG pictures. The game's rule is imported, not rewritten: `tools/ue/make_interior_material.py` `trace`.

Changed or new (the target's changes): the counter moved to the back wall and both side units became flat pegboards; the stock wall 0.30 deep with the four televisions on 0.35 boards, clear of the back door; the grandfather clock and the cabinet gone; pictures 4096 wide; the shop door, its band, the fanlight, the bell, the grille; every maker's mark painted out. The existing 23 MB `pawnbroker-display.glb` was not reused as it stood: its pictures carry marks (the Lorex pocket watch and others), so the display is rebuilt from the target's table of 31 pieces of 26 models with the cleaned maps; what is kept of it is listed above.

{{BODY}}
