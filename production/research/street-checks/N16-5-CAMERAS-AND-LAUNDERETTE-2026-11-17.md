Method researched: read-only extraction from the repository files named below, read 17 Nov 2026; geometry worked by hand (no tool run).

# n16-5: gate cameras, which plan fronts and roof runs they see, and the launderette's files (17 Nov 2026)

Extraction only; nothing judged. Tags: **R** read in the file named; **C** computed here by hand (method in section 3); **U** not read or not confirmed.

## 1. The cameras the gate and morning pictures use

Home: production/specs/vignette-scene.json, "cameras" (lines 760 to 828). tools/ue's game (CrimeProbe.cpp PageShotsTick, lines 5099 to 5120) reads that array for every -PageShots mode that is not shop/shopnight, with x_m, z_m, eye_height_m, yaw_deg, pitch_deg, fov_vertical_deg. tools/street_views.py (SHOTS vign_hook_day, vign_reverse_day, vign_hook_night) and tools/morning_pictures.py (VIEWS, the same three names) use cam_hook and cam_reverse. Frame (scene file lines 15 to 20): x along the street, 0 south, +x north; z across, +z east (the parade's side); yaw 0 faces +x, 90 faces +z; positive pitch is DOWN, negative is UP. Image 2560 x 1440 (street_views.py command line), so aspect 16:9.

| Camera | x | z | eye | yaw | pitch | vertical lens | Horizontal lens (C, at 16:9) | Used by |
|---|---|---|---|---|---|---|---|---|
| cam_hook | -3.0 | -1.6 | 2.20 | 20.4 | -3.4 (up) | 46.0 | 74.1 | morning hook day and night, street_views, gate "hook" |
| cam_reverse | 38.0 | 1.6 | 1.70 | 200.4 | -3.4 (up) | 46.0 | 74.1 | morning reverse day, street_views, gate "reverse" |
| cam_A | 4.0 | 4.0 | 1.60 | 0.0 | +4.0 (down) | 60.0 | 91.4 | scene file; gate "cam_A" (plan section 3) |
| cam_B | 21.0 | -4.0 | 1.60 | 90.0 | -3.0 (up) | 60.0 | 91.4 | scene file; gate "cam_B" |
| cam_mickeys | 6.9 | 3.25 | 1.60 | 90.0 | -6.0 (up) | 60.0 | 91.4 | scene file; gate "cam_mickeys" |

Horizontal lens: 2 x atan(tan(v/2) x 16/9). 60 degrees gives 91.4 (the scene file says "92-degree frame", line 813); 46 gives 74.1.

Notes as written in the scene file (R):
- cam_A: "on the east footway 0.875 m back from the kerb"; "sees" list A, B, E, G, H (piece classes, not fronts). tools/street_checks.py line 129 holds a cam_A copy (x 4.0, z 4.0, yaw 0.0, eye 1.6) for the street's ends check.
- cam_B: "stands on the WEST footway looking due east across the street at the east parade, at x=21.0 which is the middle of that block"; "sees roofline"; "This camera and only this camera sees the roofline" (line 785).
- cam_hook: "FITTED TO THE SHEET, 3 October"; "declared_ground y 0.0 quay_apron_at_crown_level"; its note (line 800) also holds the retired first numbers (x -3.2, z -2.2, eye 2.0, yaw 20.4, fov 46 and an older 39 degree variant); the current numbers are the table's.
- cam_reverse: "from the far end of the level street (x 38, before the climb at 44) on the east carriageway"; hook's lens turned round, parade on its left.
- Other camera definitions found, not tabled: terrace-front.py lines 6242 to 6510 (Blender's own hook-sheet, cam_A-like and cam_B-like preview cameras, "3-degrees-UP" cam_B variant) and lines 7962 to 8318 (the camera builder); tools/art-recipes/hook-preview.py, tools/perf-hook.py, tools/scale_test_layout.py, tools/frame-shadow-probe.py, production/specs/scale-test.json, street-people.json, unreal-look.json (lines 164, 196, long lines omitted by the search) name cam_ ids; **U**: their numbers were not read.

### Shop cameras (per front)

Source: CrimeProbe.cpp lines 5040 to 5097 (R). Per shop, from -PageShopList=id@x[@side], x = the window's middle, side 1 east, -1 west:
- three shots at street x = middle - 2.4, middle, middle + 2.4; z = 3.9 x side; eye 1.6; vertical lens 55; pitch 4 down for the left and right shots, 12 down for the square shot; yaw = atan2(5.9 x side - z, middle - x), i.e. each looks at the window's middle on z = 5.9 x side;
- one whole-front shot at x = middle, z = -3.6 x side (far pavement), eye 1.6, pitch 2 down, vertical lens 50, looking straight across at z = 5.9 x side.
tools/shop_views.py default: chandler@42.025; its command adds -PageNoPeople.

Window middles per front (which x the shop cameras take):

| Front | Window middle for the shop cameras | Side | Source | State |
|---|---|---|---|---|
| Launderette (east_parade bay 4, x 27 to 33) | 29.025 | +1 | display x 27.350 to 30.700 (production/cloud-week/targets/shop-windows/TARGET.md line 397; shop-interiors.json launderette display x0 27.35, x1 30.7); launderette-front-glass.json panes win_glass x -0.66 to 2.61 in the front frame (origin bay middle x 30.0, shop-interiors.json "front" x 30.0), x street = 30 - u: 27.39 to 30.66 | no run command naming it found (U); worked from the display |
| Grocer (bay 5, x 33 to 39) | 35.497 for the display zone 33.350 to 37.644 (door at the high-x end, 37.644 to 38.65) | +1 | TARGET.md line 419; gate-grocer GATE.md line 25 "display over the window zone, street x 33.35 to 37.644"; milk-crates TARGET.md line 231 puts the window's stallriser centre at x 37.30 for the crates (a different object) | no run command found (U); the middle depends on whether the door end counts: window only is not stated |
| Ironmonger (west_north bay 1, x 30 to 36) | 32.0 recorded; display 30.350 to 33.700 (centre 32.025) | -1 | gate-ironmonger GATE.md line 21: "-PageShop=ironmonger -PageShopX=32.0 -PageShopSide=-1; without the last two they framed Rita's shop" | recorded in a gate |
| Newsagent and tobacconist (west_north bay 0, x 36 to 42) | 38.025 (display 36.350 to 39.700) | -1 | gate-newsagent GATE.md line 19 "the front at street x 39.0; the display over x 36.35 to 39.70"; TARGET.md line 507 | no run command found (U); worked from the display |
| Ship's chandler (east_chandler, x 40 to 46) | 42.025 | +1 | tools/shop_views.py line 30 default; gate-chandler GATE.md line 18 "display x 40.35 to 43.70" | in code |
| Tea rooms (west_north bay 2, x 24 to 30) | 27.98 recorded (display 26.30 to 29.65, centre 27.975) | -1 | gate-tea-rooms GATE.md lines 26 to 28: "-PageShopX=26.0 aimed at the wrong window middle ... cameras at the window's middle, 27.98" | recorded in a gate |
| Empty unit (east_parade bay 3, x 21 to 27) | none found | +1 | no display, no shop entry with a display in TARGET.md (its section lists "whitewash over every pane", line 373 to 375); no gate folder (production/audits has no gate-empty-unit) | none (U) |

Rita's (not in the plan's list) for scale: PageShopX=17.0 and 17.6 in gate-ritas-front GATE.md lines 3 and 30.

## 2. Front positions in the street spec

Source: vignette-scene.json "blocks" (R): east_parade start_x 3.0, 6 bays of 6.0 m, depth 8; west_south start 3.0, 3 bays, drawn one storey (3.0 m) under a 40 degree pitch; west_north start 24.0, 3 bays, drawn one storey (3.40 m) under a 35 degree pitch; east_chandler start 40.0, 1 bay (a 1.0 m passage at 39.0). Bay plan: terrace-front.py lines 893 (EMPTY_UNIT = east_parade 3), 3303 to 3306 (CLOUD_FRONTS). Bay x ranges: east_parade bay n = 3 + 6n to 9 + 6n (bay 3 = 21 to 27, bay 4 = 27 to 33, bay 5 = 33 to 39). West row as the plan has it: tea rooms 24 to 30, ironmonger 30 to 36, newsagent 36 to 42.
Frontage planes used here: east z = +5.25 (cam_mickeys' note: "2.0 m out from the glass (5.25)"; the launderette front stands at z 5.295, shop-interiors.json); west z = -5.25 (**I**: mirrored, not read). Eaves: east 6.30 m above the crown, ridge 2.80 m higher, eaves edge at z 4.825 (cam_B's note, line 785); west_north eaves about 3.5 m (street-dressing telegraph-pole TARGET.md line 147: "eaves 3.5 m above the crown"), ridge 6.2 (west_north "why"); west_south eaves about 3.0 plus a little (storey 3.0, **I** eaves z mirrored to -4.825).

## 3. Which fronts fall in each camera's view (C)

Method. For each camera: horizontal half-angle = half the horizontal lens above. For a target point (x, z) the bearing = atan2(z - cam z, x - cam x) in the scene's yaw convention; the target is in frame if |bearing - yaw| is within the half-angle. The point taken per front is the window middle on its frontage plane (z = +5.25 or -5.25); the bay's two edges are tested too. Vertical: elevation to the target from the eye, compared with the vertical half-angle about the camera's pitch (negative pitch = looking up). Distances in plan. Nothing here tests occlusion by buildings, props, lamp columns or the climb past x 44, or the image's own pixels; "in" means inside the lens cone only.

Bearing windows (yaw +/- half-angle): cam_hook -16.65 to 57.45; cam_reverse 163.35 to 237.45; cam_A -45.7 to 45.7; cam_B 44.3 to 135.7; cam_mickeys 44.3 to 135.7.

### Fronts

| Front (window middle) | cam_hook | cam_reverse | cam_A | cam_B | cam_mickeys |
|---|---|---|---|---|---|
| Launderette (29.025) | in: bearing 12.1, 36 m; bay edges 10.8 to 12.9. Gate record: hook shows it "about 65 x 220 px" (gate-launderette GATE.md line 45) | out by 1.7 at the bay's near edge, further for the window: bay at bearings 143.9 to 161.65 against the window's 163.35. Gate record: only the box sign is in frame, "cut by the left edge" (line 46) | in: bearing 2.9, 25 m; very oblique (the camera is 1.25 m from the frontage plane) | in, window's right end 0.2 m out: window 27.35 to 30.70 against the limit x 30.48 (cone half-width 9.48 m at 9.25 m across); bay edge x 33 out | out (only x 4.85 to 8.95 in view) |
| Grocer (35.497; zone 33.35 to 37.644) | in: bearing 10.1, 39 m | out: bearing about 124 (the camera is 2.5 m from the window's middle, 3.65 m across) | in: bearing 2.3, 31.5 m, very oblique | out (needs x <= 30.48) | out |
| Ironmonger (32.025) | in: bearing -5.9, 35 m | in at its window's middle: bearing 228.9; window 30.35 to 33.70 spans 221.8 to 237.9, its right end 0.5 past the limit 237.45 | in: bearing -18.3, 28 m | out: behind (camera z -4.0 looks +z, the west frontage is at -5.25) | out |
| Newsagent (38.025) | in: bearing -5.1, 41 m | out: the camera stands at x 38.0, bearing about 270, 6.85 m across, beyond 237.45 | in: bearing -15.2, 34 m | out: behind | out |
| Ship's chandler (42.025) | in: bearing 9.0 to 8.0, 44 to 49 m. The road beyond x 44 climbs (cam_reverse note): occlusion not checked | out: behind the camera (x 40 to 46 against the camera's x 38.0) | in: bearing 1.9, 38 m, very oblique | out | out |
| Tea rooms (27.975) | in: bearing -6.7, 31 m | in: bearing 214.35; bay edges 206.1 to 220.6 | in: bearing -21.1, 24 m | out: behind | out |
| Empty unit (bay 3, middle 24.0) | in: bearing 14.5 to 15.9 (bay edges 12.9 to 15.9) | in at the middle (165.4), near edge x 27 about 1.7 outside (161.65) | in: bearing 3.6, 20 m, very oblique | in: bay 3 is x 21 to 27, centre dx 3, well inside | out |

Hook's vertical: eaves of the east parade at the near end of the run, elevation about 9.4 degrees, ridge about 14.7, against about +26.4 degrees up; fronts' ground floors near zero to slightly down. Reverse's east side bay 3 eaves: about 22 degrees against +26.4. cam_A, cam_B vertical ranges were not worked past the roof rows below.

### Roof runs

R1 east_parade north half (bays 3 to 5, x 21 to 39, eaves z 4.825), R2 the chandler's roof (x 40 to 46), R3 west_north (x 24 to 42, eaves 3.5 m at z -4.825), R4 west_south cottages (x 3 to 21, eaves about 3.0 to 3.1 at z -4.825 **I**).

| Run | cam_hook | cam_reverse | cam_A | cam_B | cam_mickeys |
|---|---|---|---|---|---|
| R1 | in: eaves line bearings 15 (x 21) to 8.7 (x 39); eaves 9.4 up, ridge 14.7 up | bay 3 only, x 21 to 27.2 (the eaves line leaves the frame at x 27.2); eaves about 22 up, ridge out at the top | in: eaves at 0.8 m across, elevation 15.5 (x 21) to 7.6 (x 39) | bay 3 (x 21 to 27) and bay 4 to x 30.0; cam_B's own note: eaves at 27.7 degrees elevation, pitched up 3 | out |
| R2 | in: bearings 8.5 to 7.5, eaves about 5.4 up | out (behind) | in: bearings about 1.6 to 1.8 (x 40 to 46), eaves about 7.4 up | out | out |
| R3 | in: bearing -6.8 (x 24) to -4.1 (x 42) | in for x 24 to 33.9 (the eaves line leaves at x 33.9); the ridge (6.2) leaves the frame's top sooner | in: bearing -23.8 (x 24) to -13.1 (x 42) | out (behind) | out |
| R4 | in for x 7.8 to 21 (the bearing -16.65 limit falls at x 7.8; x 3 to 7.8 is left of frame). Gate plan: "a thin orange fringe at the near left gutter, hook day" | in: bearing about 190 to 201 | in for x 12.6 to 21 (x under 12.6 is outside 45.7); the near end is beside the camera | out (behind) | out |

## 4. The launderette's files, as the plan names them

Plan source: N16-5-PLAN-2026-11-17.md lines 26 to 37 (the corner's layers), 61 (F1 row), 59 and 60 (P0, S1), 81 (time log). Paths checked with Glob on 17 Nov 2026.

| What the plan names | Path | Exists |
|---|---|---|
| Wear spec | production/specs/shop-fronts/launderette-front-wear.json | yes |
| Glass spec | production/specs/shop-fronts/launderette-front-glass.json | yes |
| Interiors spec, its "front" | production/specs/shop-interiors.json (launderette entry lines 135 to 196) | yes |
| Gate record | production/audits/gate-launderette/GATE.md | yes |
| Recipe | tools/art-recipes/front_wear.py | yes |
| Recipe (front made ready) | tools/art-recipes/front_for_game.py | yes |
| Street recipe | tools/art-recipes/terrace-front.py | yes |
| Import | tools/ue/import_street.py | yes |
| Staged data list | tools/ue/stage_game_data.py | yes |
| Shop views | tools/shop_views.py | yes |
| Street wear | tools/street_wear.py | yes |
| Street wear spec | production/specs/street-wear.json | yes |
| Corner spec | production/specs/ps5-corner.json | yes |
| Street spec | production/specs/vignette-scene.json | yes |
| Look spec | production/specs/unreal-look.json | yes |
| Street asset table (plan P0) | production/assets/street/quay-street.json | yes |
| Stain check | tools/stain_check.py | yes |
| Time log | tools/timelog.py | yes |
| Chandler's wall-box check (chandler's alone) | tools/chandler_wear_check.py | yes |
| Kit piece (named in the glass spec's "source") | production/assets/cloud-week/shop-windows/steam_laundry_front.glb | yes |
| The gate's brief | F:/LedgerTools/gate/new/launderette-2026-10-24/BRIEF.md (GATE.md line 11) | **not found** by Glob of that folder (no files returned) |
| Gate last-good pictures | F:/LedgerTools/gate/last-good/launderette/ (GATE.md line 49) | **unread** (not listed) |
| Shop sign pictures for night glow | F:/LedgerTools/game-inputs/production/art/shop-signs/launderette/steam_laundry_emissive.png, steam_laundry_box_face_a_emissive.png, steam_laundry_box_face_b_emissive.png (wear spec) | **unread** (F: path not listed) |

Not read: production/specs/shop-fronts/grocer, other fronts' wear files beside Rita's.

### Current values written for the launderette (R)

**production/specs/shop-fronts/launderette-front-wear.json** (the whole file read):
- front "launderette-front", out "launderette-front-worn".
- paints: paint_cream (texture 4096 px), paint_side_door_dark_brown (2048 px); roughness map 1024 px; detail_below_m 1.2; detail_ratio 3.0.
- dirt_hue [0.2, 0.155, 0.11]; dirt_luminance 0.55; dirt_luminance_floor 0.035; foot_m 0.17; foot_ragged_m 0.05; foot_full 0.4; tide 0.15; tide_m 0.03; splash_m 0.4; splash 0.5; splash_above 0.55; ao_m 0.08; ao_reach_m 1.0; ao 0.9; ao_everywhere 0.3; ledge 0.3.
- lever [-2.178, -0.03, 0.842]; lever_m 0.15; lever_weight 0.25 (the side door's brass knob).
- chip_colour [0.22, 0.18, 0.13]; chip_edge_m 0.03; chip_scale 25.0; chip_above 0.58; chip regions: the left pilaster's plinth x -3.0 to -2.655, z 0.0 to 0.6, amount 1.0, paint_cream; the right pilaster's plinth x 2.65 to 3.0, z 0.0 to 0.6, amount 0.6, paint_cream.
- roughness_dirt 0.55; roughness_chip 0.6.
- night_glow: material fascia_steam_laundry (png steam_laundry_emissive.png), sign_face_a, sign_face_b (the two box-face emissive pngs), all under F:/LedgerTools/game-inputs/production/art/shop-signs/launderette/.
- Its note: window and shop door anodised aluminium in bronze (paint_alu_bronze, metallic 0.85, left clean); stallriser tiled (a picture, not baked); shop door at the back of a recessed lobby (x -1.706 to -0.700) with brass furniture left clean; cream render pilasters (x -3.0 to -2.65 and 2.65 to 3.0, plinths 0 to 0.6 up, 0.18 proud) and cornice; dark brown side door at the viewer's left (x -2.597 to -1.759, flush at y about -0.03), knob at x -2.178, 0.842 up; "Only the cream plinths chip; no rail chips".

**production/specs/shop-fronts/launderette-front-glass.json**: source steam_laundry_front.glb; 11 panes in the front's frame (x about bay middle from the viewer's left, y = -out from the wall face, z up): band_toplight_glass_0, _1, _2 (x -1.66 to -0.746, z 2.48 to 2.79); door_glass_0 (x -1.609 to -0.797, z 0.594 to 1.974); fanlight_glass (x -1.658 to -0.748, z 2.127 to 2.404); glass_fanlight (x -2.5826 to -1.7734, z 2.1115 to 2.3907); lobby_glass_w (x -0.717 to -0.711, z 0.625 to 2.375); win_glass_lower_0 (x -0.66 to 0.958, z 0.625 to 2.4); win_glass_lower_1 (x 0.992 to 2.61, z 0.625 to 2.4); win_glass_top_0 (x -0.66 to 0.958, z 2.48 to 2.79); win_glass_top_1 (x 0.992 to 2.61, z 2.48 to 2.79). Window has two lights (terrace-front.py line 3308, CLOUD_LIGHTS = {"launderette-front": 2}).

**shop-interiors.json launderette entry**: block east_parade, bay 4, side 1; trade "launderette (Steam Laundry, no. 9)"; room w 5.3, h 2.4, d 4.5; card x0 27.35, x1 32.65, bottom 0.65, top 3.05, z 5.875; display glb launderette-display, x0 27.35, x1 30.7, front 5.27, bed 0.7; lit_at_night false; brightness_day 0.15, brightness_night 0.7; front glb "launderette-front-worn" ("launderette-front" is the clean copy), x 30.0, z 5.295, up 0.1; night_glow slots fascia_steam_laundry (strength 0.7), sign_face_a (0.7), sign_face_b (0.7); street_decals false (note: "its wear to be baked into its own paints after its gate"); door_sign_closed production/art/shop-signs/door-card-closed; camera_d 5.3; pixels_wide 4096.

**Sign text and colours as written**:
- Cloud front (the one drawn): fascia name blocks "STEAM LAUNDRY", trade "LAUNDERETTE", "SERVICE WASHES", "DRY CLEANING"; hanging sign steam_laundry_box; window lettering "SERVICE WASHES" and "9" (TARGET.md lines 389 and 390). Paint sRGB: pilaster, console, cornice, fascia board [222, 209, 175]; stallriser [228, 228, 220]; window frame and shop door [84, 68, 53]; side door [74, 48, 34]; metal [170, 172, 174] (TARGET.md line 388). Door paint alu_bronze. Gate record: "fascia, box sign and glass lettering read right"; "LAUNDR" warm patch at night; CLAYBROOK on the packets (renamed from BRIGHTWELL).
- Spec fascia in the street recipe (terrace-front.py line 920): SIGN_OVERRIDE east_parade bay 4 = production/assets/vignette/decals2d/fascia_trade_launderette; its lettering in tools/props/make_vignette_2d.py lines 260 to 262: "LAUNDERETTE" (cap height 210 mm, LibreFranklin-800, colour (28, 64, 140)) and "SERVICE WASHES  ·  DRY CLEANING" (70 mm, LibreFranklin-700, (176, 30, 34)) on a board (236, 232, 222), shade False. **U**: whether this board still draws where the cloud front stands; terrace-front.py line 6171 lays the cloud front when `here in CLOUD_FRONTS and not refit`.
- Interior picture crop: terrace-front.py line 2861, ("east_parade", 4): int23_laundry (0.03, 0.10, 0.73, 0.98).
- Hours: Mon to Sat 8:00 to 17:30 (TARGET.md line 392); the room is dark at night, its box sign and fascia glow.

**Street-wear (production/specs/street-wear.json)**: bay east_parade_bay4: seed 1848225893, brick_set 0, tint [1.066, 0.955, 0.978], wear 0.983 (lines 66 to 76); wearCoverage 1.0 on wall east_parade_bay4 (line 4266); 7 marks "on": "east_parade_bay4": splash (x 30, y 0.4, z 5.115, 6 x 0.6, strength 0.997), wash (x 30, y 3.2, 6.12 x 6.2, 0.526), damp (x 30, y 0.6, 6.12 x 1.0, 0.695), streak wear_streak_b at x 28.4753 y 4.0273 (0.9557 x 1.1908, 0.502), streak wear_streak_b at x 31.5347 y 4.032 (0.9294 x 1.1719, 0.711), algae at x 33 y 0.35 (0.8 x 1.0, 0.997), algae at x 33.12 y 1.3 (0.35 x 1.5, 0.845). tools/street_wear.py: STREET_LEVEL_X_M = 33.0 (line 652); KIT_FRONTS holds east_parade_bay2 only in what was grepped (line 594; the launderette is not named in street_wear.py); BRICK_STREAK_BAYS = {CHANDLER: ("east_chandler_bay_north",)} (line 534).

**Brick, ps5-corner.json "scanned" (the launderette's wall draws brick_red)**: base brick_red, asset photo_flemish_n16_4, covers_m 2.72, match_rgb [0.556, 0.376, 0.316], always true, macro 0.08, macro_scale 0.0025 (lines 346 to 366); brick_grey base asset brick_wall_001, covers_m 1.05 (line 369 on). vignette-scene.json east_parade wall_surface "brick_red".

## 5. Gaps (U)

- No recorded camera command (-PageShopX) for the launderette, grocer or newsagent; windows middles above are worked from the displays' spans in shop-windows TARGET.md. The grocer's window-only middle is not stated (its display zone includes the lobby's door end).
- No shop camera or display for the empty unit (bay 3).
- F: paths (the launderette gate's BRIEF.md, last-good pictures, the emissive pngs) were not listed; BRIEF.md's folder returned nothing.
- cam_A, cam_B and cam_mickeys are named in the plan's views; whether the gate's pictures use exactly these scene-file numbers or terrace-front.py's Blender variants (lines 6242 to 6510) was not settled.
- West frontage z = -5.25 and west eaves z are mirrored from the east, not read.
- No occlusion (buildings, lamp columns, props, the climb past x 44) and no pixel test was made.
