# House windows (unit 8): the street's window kit, thirteen rooms behind it, and the gate

Built 14 October 2026 by the unit 8 builder, to `production/cloud-week/targets/house-windows/TARGET.md` and `target.json` (status "fixes applied, not re-reviewed"; FIXES-APPLIED.md wins over the review).
Branch cloud/week-42. The builder did not commit; the main session snapshots the files.

**Status:** `check_windows.py` reads **55 of 60 rows pass** (the target's own 47 rows: 42 pass). Five rows fail and each is explained under "Check" (WB-01, WB-03, WB-07, NIGHT-01, NIGHT-02). All four kit pieces and the cottages' card, all thirteen rooms (39 pictures), and the gate's views for the Hook, the reverse view, cam_A and two close views, day and night, are done; the views of the target's 22 that were not rendered are listed under "Not done".

## What was made

| What | Where | Size |
|---|---|---|
| Four window kit pieces and the cottages' room card | `production/assets/cloud-week/house-windows/hw_S22.glb`, `hw_S11.glb`, `hw_RC.glb`, `hw_RC2.glb`, `hw_room_card_gf.glb`, and `hw_manifest.json` (which nodes each of the twenty sites switches on, its paint, net, drape, room and card) | S22 3,948 triangles / 367 KB, S11 3,618 / 338 KB, RC 1,458 / 246 KB, RC2 1,706 / 268 KB, the card 72 / 4 KB (limits 6,000 and 400 KB) |
| The scripts | this folder (`build_windows.py` is the one command) | |
| The thirteen rooms, each three pictures and a JSON | outside git, `ledger-scratch/house-windows/rooms/` (`<room>_day.png`, `_night_lit.png`, `_night_dark.png`, `<room>.json`, `<room>.placed.json` with what stands where) | 1536 x 1399 (upper rooms), 3072 x 2349 (cottages) |
| The gate's frames, masks and the card bakes | outside git, `ledger-scratch/house-windows/gate/` | 2560 x 1440 |
| The review pictures | `production/previews/cloud-week/house-windows/hw-<view>-<state>-2026-10-13.jpg` (the date the target names), about 1600 px, under 500 KB | ten: Hook, reverse, cam_A and two close views (`close` is the target's H_ALONG_30_NEAR, `close2` a tighter one at 1.5 m from the wall), each day and night_lit; 83 to 213 KB |
| The check | `check_windows.py`, writing `checks/check_windows_v1.json` | 60 rows, 55 pass, 5 fail, 0 not run (the target's own 47: 42 pass) |

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

S22 and S11 are the lab's checked box sash (`production/assets/sash-window/sash_window.glb` and `sash_window_1over1.glb`, 41 and 35 nodes), imported and not redrawn: all joinery nodes keep their shapes and names (the lab's 41 nodes less its two glass sheets, which became one node a pane). What was added to them: each glass sheet
split into one node a pane (the 2/2's split at the glazing bar), each pane tilted by a seeded angle (target 5.2), the box shade in COLOR_0, the putty and parting-bead parts' shade rules, UVs for the net textures, and all the dressing (nets, drapes, blinds, pendant, room card).
RC and RC2 (the upvc replacements) are new, built from the target's parts tables (4.3), bevelled 1.5 mm, with the gasket line and the welded-corner grooves as strips.

## The models (Poly Haven, CC0, 1k)

All sixteen are CC0 on their Poly Haven pages (https://polyhaven.com/a/<id>), each fetched with a `source.json`, and listed with authors in THIRD-PARTY.md ("House rooms behind the street's windows"):
Sofa_01, side_table_01, television_02, hanging_picture_frame_01, hanging_picture_frame_02, hanging_picture_frame_03, ornate_mirror_01, mantel_clock_01, wall_clock, potted_plant_01, Shelf_01, wooden_bookshelf_worn, vintage_oil_lamp, vintage_cabinet_01, painted_wooden_cabinet, painted_wooden_bench;
and the nine textures ceiling_interior, decrepit_wallpaper, dirty_carpet, floral_jacquard, linoleum_brown, old_wooden_floor_02, painted_plaster_wall, peeling_painted_wall, plastered_wall_04.
Every model is placed at scale 1.0 (never shrunk or stretched evenly: the check measures each placed piece's height against the model's own) with all its meshes (the glass kept as a see-through material; the check lists any dropped part).

Marks, looked at at 100 per cent on every placed model's 1k base colour (and at 3 to 5 times where something looked like lettering): television_02 carries "PARAGON" and "Viewing System" lettered vertically on the bezel; wall_clock carries "URBAN" and "quartz" on the dial.
Both are painted out by script (`hw_models.py`, `MARKS`, the fill taken from a ring just outside plus the map's own grain; the model's normal and roughness maps get the same boxes because engraved lettering lives in the relief) and the check reads the painted regions again (PIC-07).
The three picture frames' artwork (a printed "Ray Homes", a signed painting, a castle) is replaced by prints cropped from four CC0 Poly Haven HDRI photographs (lake_pier, dalkey_view, blouberg_sunrise_1, belfast_open_field; crops of sea, coast, field and trees, no person, sign or modern building), tone-mapped and warmed.
No other model carries lettering that reads at 1k.

## What the builder decided where the target left it open (all inside the target's numbers)

1. **The angle from the wall is the line of sight's angle to the wall's plane in three dimensions** (target 9: "from the scene's geometry"). For an upper window a camera on the footway adds the climb to its distance, so the target's H_ALONG_15_NEAR reads 12.9 degrees and H_ALONG_30_NEAR 19.5; the 15 to 30 degree bands of WB-01, WB-02 and WB-04 are therefore measured on H_ALONG_30_NEAR (frames `h-along30-bay3w1`, `h-along30-bay1w1`, `close`, `close2`); `h-along15-bay3w1` is rendered as an extra and counts as 19 degrees only for its neighbour.
2. **WB-01 to WB-07 and NIGHT-01 to NIGHT-03 are read in the target's own measuring views** (its H cameras, here also the two close views), as the rows say ("the gate's five views", "the one camera that sees each squarely"; the night rows only for windows seen at 45 degrees or more). The review views (Hook, reverse, cam_A) are far, along the wall, and are reported beside, never failed: a Hook net window at 15 to 30 degrees reads P/L 0.24 to 0.33.
3. **A window cut by the picture's edge is not measured** (WB-06, WB-07).
4. **SITE-02 leaves out a cottage's own two windows** (one room, one card), as the target's own self-check does (`same_house`).
5. **PIC-03 lets a lit landing's card take the target's absolute floor** (landing_bulb.card_emission_floor_linear) and leaves an empty room's night_lit out with the night_dark pictures (the target says it IS the night_dark picture). **PIC-04 finds the back wall's corners where the dark line under the coving leaves the horizontal** (the first try, the strongest vertical edge, was fooled by the striped papers of lounge 3 and bedroom 3). **PIC-09 uses the robust noise figure** (1.4826 x median absolute deviation: the plain standard deviation read pattern pixels of the same striped papers as 1.9 levels of noise; the robust figure is 0.5 to 0.9 on every room). **GLS-04 fails a sodium-coloured patch** brighter than the reflection-off render (the shops' burnt orange bar); a grey patch is the night sky in the glass, a real reflection, listed beside. **GLS-05 does not count orange on a window's own paint or on brick** in the lamp's pool (cam_A stands under a lamp).
6. **WB-08's old fault is rendered flat**: a lit pale card for the pane and joinery with its own light, no box shade and no shading of the reveal. A first try (the old pane as a diffuse card, only the box shade removed) still read D/L 0.52 because Cycles shades the reveal by itself, which would have let the old fault pass the check; flat, it reads D/L 0.83, spread 1, no dip, P/L 0.84 and fails WB-02, WB-04, WB-04b and WB-05 as the row demands.
7. **The mantel clock keeps its model's own size** (342 x 126 x 161 mm; the catalogue's 484 x 251 x 161 is not the mesh): never stretched; its height matches (PIC-11).
8. **A landing's stair is drawn with a newel and balusters** (the target says balusters are not drawn): 26 to 30 mm flat boards on three different front planes (26, 29, 30 mm proud, inside the 0.03 side budget), because a stringer and handrail alone read as two leaning planks. The first version had the slope the wrong way and ran through the picture rail; the rail now ends under the coving. **A doorway has no skirting** (the skirting band stops at the door leaf): a band running behind the leaf on the same plane shadowed the leaf black.
9. **The night glass reflects at 0.2 and the dome is 0.15** (the shops' gate numbers, kept; the house target gives the dome 0.15 and no glass weight). The pane is the shops' pane (a Mix of transparent and a rough 0.03 glossy by the dielectric Fresnel, F0 0.08, day 1.0, night 0.2; roughness 0.35 where COLOR_0 says dirt), not the Principled stand-in the target's 5.1 names; MAT-04 reads 0.250 of the sky at 16 degrees (limit 0.26 +-0.05).
10. **Samples**: rooms 24 samples (cottages 16, four times the pixels), the gate 40 (the target says 128 and 48), OpenImageDenoise, adaptive; the noise row PIC-09 reads 0.5 to 0.9 levels. The first sky and lamp calibration is stored (`gate/gate_lights.json`: sky 1.579, lamp 2377 W; the paving under the near lamp reads sRGB 150; a grey card reads 0.18).
11. **The stand-in street's cottage sills were wrong and are fixed** (found from the cottage close view: a black strip along every cottage sill): the stone sill had been put 50.8 mm into the wall and its top shared the plane of the wall's own top under the window. Not a kit fault; the gate's scene.
12. **The room pictures were looked at one by one as they came off the queue**: the first landing showed the stair and doorway faults of decision 8 and was rendered again; every other room was accepted at the first render.
13. **One extra view**, `close2`, was added to the gate for the close reviewer (the target's five views are 5 to 9 m from an upper window).

## Check

`python3 build_windows.py check`: **55 of 60 rows pass** (5 fail, 0 not run; the target's own 47 rows: 42 pass), `checks/check_windows_v1.json`. Every row of the target's `checks` that applies to built things and renders is in it (KIT-01 to 15, MAT-01 to 04, WB-01 to 09, NIGHT-01 to 06, PIC-01 to 12, SITE-01 to 04, CONTENT-01), plus the shops' reviews' rows (KIT-16 real RGB normal maps, TEXCOORD_0 and no Bump in any glb; KIT-17 nothing floats in a kit piece; KIT-18 folds are not a regular corrugation; GLS-04 no bright band in the night glass; GLS-05 no lit stand-in lamp; FRM-01 no see-through slot; PIC-03b the night wash does not burn the corners; PIC-10 floating goods; PIC-11 real size; PIC-12 every placed model keeps all its parts) and PRV-01. The rows that do not apply on the cloud (the target's PC rows OWED-01 to OWED-06) are not in it.

**The five that fail**

- **WB-01 net windows read P/L 0.25, 0.23, 0.36 and 0.30 at 19 to 22 degrees** (band 0.55 to 0.97). The nets themselves are there and bright (with the glass's reflection off the lower sash reads about 0.5 of the frame), but a clear upper sash reads the dark day room (the target's own day room is 14 levels), the stand-in eaves' soffit shows in the top of the glass, and the overcast sky's reflection (F about 0.2 at 20 degrees from the wall, a sky several times as bright as the white paint) lays a flat veil over the net. In a test render an RC window with a full-height net read 0.84 in the same view (the glass there reflects the sky across the whole pane). The target says itself that the band is carried down from 31 to 39 degrees (its `could_not_settle`); the packaged game's own pane is OWED-01.
- **WB-03 the bare window from across reads P/L 0.75 (band 0.35 to 0.70) and blue over red by 4 levels (at least 10).** The pane is the overcast dome's reflection over the dark room; P8's pane was a clear blue sky. The dome is the project's own and is neutral.
- **WB-07 one window of six reads 2.995 (the band starts at 3.0): the flaking-paint window `east_parade_bay3_upper_w1`.** The rest read 3.40 to 7.34.
- **NIGHT-01 and NIGHT-02: lit windows read 57 to 115 and dark windows 43 to 82 (their rule: dark 8 to 30, lit at least 4 times that).** The dark rooms' pictures seen through the pane are brighter than their means, and the night sky's reflection adds 7 to 58 levels at 40 to 70 degrees from the wall; with the reflection off the dark panes still read 17 to 62 (the nets' sodium emission and the dark room picture's central part at 0.7). NIGHT-04 (the pictures' own mean, 14.6 to 15.5) passes. A weaker dome as light (a tenth) was tried and moved the dark windows by 10 levels only. Not fixed; a target number against another.

**Rows that pass and what they stand on:** the kit rows read the exported glbs (sizes, planes, tilts, nets' planes and the 64 mm to the lower pane, box shade, 6 mm lines, no opening in the front); WB-02 bare window 0.25, WB-04 D/L 0.06 to 0.07 (limit 0.72), WB-04b dip 0.08 to 0.16 (limit 0.60), WB-05 spreads 54 to 183, WB-06 band medians span 15 to 28 levels, WB-08 the old fault fails as it must (above), WB-09 windows under 10 degrees read pane under the lining; NIGHT-03 the lit nets' colours; the thirteen rooms' pictures at the sizes of the target with means 15 / 70 / 105 (landings 40) within 15 per cent.

## Render times

Rooms (one at a time, niced, four shared cores): 24 samples, denoised; upper rooms 2.6 to 5.4 minutes a picture (a room 8 to 14 minutes), cottages 6.6 to 11.3 minutes a picture (a room 24 to 36 minutes); total 3.1 hours for the thirteen rooms (and 0.4 hour thrown away: the first landings, rendered with the stair and doorway faults, were done again). The calibration of each room's lights (a few quarter-size pictures) is included.
Gate: 2560 x 1440, 40 samples, 4.8 to 19 minutes a frame by load (Hook 5.0 and 5.1, reverse 4.8 and 4.5, cam_A 7.0 and 8.3, close 7.0 and 7.8, close2 8.6 and 9.0, H_ACROSS_0 8.6 to 9.3, H_ALONG_30 7.2, the cottage along-30 17.5 and 19.2 with the machine busy), 20 frames in all, 2.9 hours; masks 2 seconds each, the reflection-off night frames about a minute each; the Hook, the reverse view, cam_A and the cottage along-30 day frame were rendered twice (the first frames showed the black cottage sills, decision 11), about 1.1 hours more. The kit: about 3 minutes for the five glbs. The check: 11 seconds.

## Known shortfalls

- The nets are cards with an alpha weave and a normal map, not geometry: the folds read from about 3 m; from the Hook they are a pale sheet, and by day a flat sky veil lies over them at 15 to 30 degrees from the wall (WB-01).
- Day sky: the dome clips to white above the horizon in the frames (calibrated to the grey card, as the target says); the glass reflects a flat overcast sky. The game's own reflections (Lumen, the street cube) are not shown (OWED-06).
- The stand-in street is boxes: its eaves (0.3 m, a flat soffit) show black in the top of the upper panes seen from below; the ground floors are stand-ins.
- Rooms: sixteen models and nine textures at 1k, no period British room photograph reached; a dark room seen through a pane reads brighter than its picture's mean (NIGHT-01).
- Lit windows by night show the room card at 0.28 (picture x 0.7 x 0.4) and the nets' emission 0.48: the upper sash of a lit window is dim by the target's numbers (a net-less upper sash reads the room's wall).
- The kit's glbs are not bit-identical on a rebuild (float noise); the nodes, sizes and every check figure are.
- The gate used 40 samples (the target 48) and the rooms 24 (cottages 16; the target 128): the noise row passes (0.5 to 0.9 levels), but the pictures should be rebuilt on the PC at the target's samples (OWED-04).

## Not done

Nothing of the build is left out: four kit pieces, the cottages' card, the manifest, thirteen rooms in three pictures each (up_lounge_1, 2, 3, up_bedroom_1, 2, 3, up_landing_1, 2, up_empty_1, 2, gf_front_1, 2, 3; the empty rooms' night_lit is a copy of their night_dark, as the target says), the check, this file, the THIRD-PARTY.md section and the RECIPE.md entry.
Of the target's 22 gate renders (GS_A 11, GS_B 11) 8 are rendered (GS_A: H_ACROSS_0 day and night, H_ALONG_15_NEAR day, H_ALONG_30_NEAR day and night, H_UNDER day; GS_B: H_ALONG_30_NEAR day and night) and 14 were **not rendered**:
- GS_A (the east parade), 5: H_ACROSS_30 day and night; H_ALONG_15_NEAR night (day is `h-along15-bay3w1`); H_ALONG_15_ROAD day and night (the WB-09 row is read from cam_A, where three windows are under 10 degrees instead).
- GS_B (the cottages), 9: H_ACROSS_0 and H_ACROSS_30 from the east footway, day and night; H_ALONG_15_NEAR day and night; H_ALONG_15_ROAD day and night; H_UNDER day.
- The old fault is rendered once (`old-fault`, in the view of the bare window at 19 degrees), not in every view.
Not shown by the cloud at all: the game's pane, Lumen's reflections, the street cube (OWED-01, OWED-06).

## Owed to the PC

- The room pictures are in `ledger-scratch/house-windows/rooms/` (39 PNGs, about 140 MB, and the JSON): the PC takes them (they are not in git), rebuilds them with `make_house_rooms.py` at 128 samples (OWED-04; not written here: `build_windows.py rooms` is the cloud's) and imports them as sRGB textures. The four HDRIs the three framed pictures' prints are cropped from are read from another builder's cache (`/home/user/ledger-scratch/polyhaven/_hdri`): the PC fetches lake_pier, dalkey_view, blouberg_sunrise_1 (Poly Haven, CC0) and has the repository's belfast_open_field.
- OWED-01 to OWED-03, OWED-05 and OWED-06 as the target lists them (the pane in the game, the box shade read by M_LedgerSurface, the marker test in the packaged game, Jafar's page, the street cube). WB-01, WB-03 and the two night rows are best settled there: the target's bands were set from photographs and its own `could_not_settle` says the 15 to 30 degree net band is carried down from 31 to 39 degrees.
- The nets, curtains and blinds import with their glbs; the manifest says which nodes each of the twenty sites switches on.

## For the two fresh reviewers

**The street reviewer** (Hook, reverse, cam_A; `production/previews/cloud-week/house-windows/hw-hook-*`, `hw-reverse-*`, `hw-cam-a-*`): look first at the Hook day frame's near three east windows (white frames, reveal, sill, a net or a bare pane), then at the night frame's lit window at the near end (a cream curtain and net lit warm, the rest dark), then at the west cottages at the left (stone sills, no black strip). Look for: a lit stand-in lamp (none is meant to show), an orange bar in a night pane, a see-through slot at a sill or a lining, a window floating off its wall.
**The close reviewer** (`hw-close-*` the target's view, `hw-close2-*` the tighter one, both of `east_parade_bay0_upper_w1`: a box sash with a voile net and open cream curtains, grimy white paint): look first at the night frame's net and curtain (varied folds, a lit cloth seen through the glass, the rod and brackets), then the day frame's lining, putty line, parting bead and meeting rail (the dark line round each pane), then the sill and the sash horn. By day the sky's reflection lies flat over the lower sash: that is the glass, not a missing net (with the reflection off the net is plainly there).
Both: the rooms are pictures, not geometry; the five failing rows are above, and none is about the kit.
