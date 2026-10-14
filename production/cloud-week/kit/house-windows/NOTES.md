# House windows (unit 8): the street's window kit, thirteen rooms behind it, and the gate

Built 14 October 2026 by the unit 8 builder, to `production/cloud-week/targets/house-windows/TARGET.md` and `target.json` (status "fixes applied, not re-reviewed"; FIXES-APPLIED.md wins over the review).
Branch cloud/week-42. The builder did not commit; the main session snapshots the files.

**Status line (filled at the end of the run, see "Check" below):** @@STATUS@@

## What was made

| What | Where | Size |
|---|---|---|
| Four window kit pieces and the cottages' room card | `production/assets/cloud-week/house-windows/hw_S22.glb`, `hw_S11.glb`, `hw_RC.glb`, `hw_RC2.glb`, `hw_room_card_gf.glb`, and `hw_manifest.json` (which nodes each of the twenty sites switches on, its paint, net, drape, room and card) | S22 3,948 triangles / 367 KB, S11 3,618 / 338 KB, RC 1,458 / 246 KB, RC2 1,706 / 268 KB, the card 72 / 4 KB (limits 6,000 and 400 KB) |
| The scripts | this folder (`build_windows.py` is the one command) | |
| The thirteen rooms, each three pictures and a JSON | outside git, `ledger-scratch/house-windows/rooms/` (`<room>_day.png`, `_night_lit.png`, `_night_dark.png`, `<room>.json`, `<room>.placed.json` with what stands where) | 1536 x 1399 (upper rooms), 3072 x 2349 (cottages) |
| The gate's frames, masks and the card bakes | outside git, `ledger-scratch/house-windows/gate/` | 2560 x 1440 |
| The review pictures | `production/previews/cloud-week/house-windows/hw-<view>-<state>-2026-10-13.jpg` (the date the target names), about 1600 px, under 500 KB | @@PREVIEWS@@ |
| The check | `check_windows.py`, writing `checks/check_windows_v1.json` | @@CHECKLINE@@ |

The kit pieces carry every variant as named nodes (nets N1, N2, N3 and the torn N1 on S22, curtains C1 and C2, blinds B1 to B3, the rods, poles, brackets, headrails, the pendant and the upper rooms' `room__card`); the PC switches on the ones `hw_manifest.json` lists for a site
and sets the house's paint on the `paint_*` slots by name. Pivot, frame and placement are the target's (section 8): pivot the opening's bottom-edge centre on the brick face, x across (the viewer's right), y into the wall, z up; an east
window is translated to (x_centre, +5.125, sill), a west one turned 180 degrees about z and translated to (x_centre, -5.125, sill). Every pane is a node (`glass__*`), every sill, frame and lining a part. COLOR_0 is the box shade of target 8
(street faces 1.0; faces running into the wall 1.0 down to 0.6 at the glass plane; the track 0.5; inside corners 0.3 within 8 mm; putty 0.35; the meeting rail's underside 0.4; parting-bead sides 0.10; the RC gaskets 0.30 and welds 0.35) and, on a pane, the dirt mask
(1.0 clean, 0.8 on the 6 mm band and the lowest 25 mm). The glass is `glass_house` (base 0.03, roughness 0.03, metallic 0, KHR_materials_specular 2.0, opaque: a see-through material that is not alpha-blended); the nets are cards with an RGBA weave texture and a JPEG
normal map, their pleats drawn at random pitch (nets 30 to 70 mm, curtains 55 to 95 mm), depth and a soft S profile, never a regular corrugation; every rod, pole, head-rail and roller is geometry with brackets.

## Rebuild

`python3 build_windows.py` (system Python; each stage calls Blender's Python at `/home/user/.bpyenv/bin/python` under `nice -n 15`) runs `assets kit rooms gate check` in order; `python3 build_windows.py kit` alone rebuilds the glbs, the manifest.
`python3 build_windows.py rooms` renders any room whose JSON is missing (delete a room's JSON to redo it), `python3 build_windows.py gate [frame ...]` renders what is missing of the gate (delete a frame to redo it), `python3 build_windows.py check` runs the check.
Heavy outputs go to `LEDGER_HW_SCRATCH` (default `/home/user/ledger-scratch/house-windows`), never into git. One render at a time: the machine is shared.
The glbs are not bit-identical on a rebuild (float noise in the bevel geometry; the JSON, the node names, the sizes and every check number are identical).

## Where each copied script came from (the shop kit, 14 October 2026)

Another builder was working in `production/cloud-week/kit/shop-windows/` that morning, so nothing there was edited or imported live. The files below were COPIED at 03:13 UTC on 14 October and renamed; each header says what was kept.
`hw_assets.py` from `sw_assets.py` (md5 3d64a1c39efff85d63e37ba641cb2bef), trimmed to the helpers the house rooms use; `hw_room.py` from `sw_room.py` (md5 23f5d4c582194c0eef6974ff7dce858a, the batch B version with `keep_glass`), trimmed
to the Room class's materials, templates, placement and render; `hw_gate.py` rewritten from `sw_gate.py` (md5 08e00d19...) and `hw_gate_run.py` from `sw_gate_run.py` (md5 75b34a4d...): what is kept is the method (the room baked on the card by the game's `trace`,
the card as an emission quad, the night glass as reflection only, the stand-in lamps hidden from the camera and from glossy rays), the scene is the street's; `hw_ctx.py` from `sw_ctx.py` (the shop context's Ctx class left behind). The game's own
`tools/ue/make_interior_material.py` is imported from there (function `trace`, never rewritten). Written new for the house windows: `hw_t.py`, `hw_models.py`, `hw_roomgen.py`, `hw_cloth.py`, `hw_kit.py`, `hw_glb.py`, `hw_measure.py`, `check_windows.py`, `build_windows.py`.

## What was kept from the lab's sash

S22 and S11 are the lab's checked box sash (`production/assets/sash-window/sash_window.glb` and `sash_window_1over1.glb`, 41 and 35 nodes), imported and not redrawn: their joinery nodes keep their shapes and names. What was added to them: each glass sheet
split into one node a pane (the 2/2's split at the glazing bar), each pane tilted by a seeded angle (target 5.2), the box shade in COLOR_0, the putty and parting-bead parts' shade rules, UVs for the net textures, and all the dressing (nets, drapes, blinds, pendant, room card).
RC and RC2 (the upvc replacements) are new, built from the target's parts tables (4.3), bevelled 1.5 mm, with the gasket line and the welded-corner grooves as strips.

## The models (Poly Haven, CC0, 1k)

All sixteen are CC0 on their Poly Haven pages (https://polyhaven.com/a/<id>), each fetched with a `source.json`, and listed with authors in THIRD-PARTY.md ("House rooms behind the street's windows"):
Sofa_01, side_table_01, television_02, hanging_picture_frame_01, hanging_picture_frame_02, hanging_picture_frame_03, ornate_mirror_01, mantel_clock_01, wall_clock, potted_plant_01, Shelf_01, wooden_bookshelf_worn, vintage_oil_lamp, vintage_cabinet_01, painted_wooden_cabinet, painted_wooden_bench;
and the nine textures ceiling_interior, decrepit_wallpaper, dirty_carpet, floral_jacquard, linoleum_brown, old_wooden_floor_02, painted_plaster_wall, peeling_painted_wall, plastered_wall_04.
Every model is placed at scale 1.0 (never shrunk or stretched evenly: the check measures each placed piece's height against the model's own) with all its meshes (the glass kept as a see-through material; the check lists any dropped part).

Marks, looked at at 100 per cent on every placed model's 1k base colour (and at 3 to 5 times where something looked like lettering): television_02 carries "PARAGON" and "Viewing System" lettered upright on the bezel; wall_clock carries "URBAN" and "quartz" on the dial.
Both are painted out by script (`hw_models.py`, `MARKS`, the fill taken from a ring just outside plus the map's own grain; the model's normal and roughness maps get the same boxes because engraved lettering lives in the relief) and the check reads the painted regions again (PIC-07).
The three picture frames' artwork (a printed "Ray Homes", a signed painting, a castle) is replaced by prints cropped from four CC0 Poly Haven HDRI photographs (lake_pier, dalkey_view, blouberg_sunrise_1, belfast_open_field; crops of sea, coast, field and trees, no person, sign or modern building), tone-mapped and warmed.
No other model carries lettering that reads at 1k.

## What the builder decided where the target left it open (all inside the target's numbers)

@@DECISIONS@@

## Check

@@CHECK@@

## Render times

@@TIMES@@

## Known shortfalls

@@SHORTFALLS@@

## Not done

@@NOTDONE@@

## Owed to the PC

@@OWED@@

## For the two fresh reviewers

@@REVIEWERS@@
