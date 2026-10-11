# Cloud week 42: the handover for the builder

Kept usable at any moment: updated after every finished piece. Last updated 11 October 2026, 23:20 (Swiss). The queue (QUEUE.md) says what state each unit is in; this file says what the builder does with what is done. Branch cloud/week-42, made from wip on 8 October; nothing here is on wip or main until the builder takes it.

## How a piece gets into the game (the same for every kit piece)

1. **Take the model.** Each kit piece is a .glb in production/assets/cloud-week/<piece>/ (metres, z up, scale 1, pivot at the base's centre on the ground; wall-mounted pieces at the back face's bottom centre, the wall at y = 0, the street toward -y). Its script rebuilds it exactly: `python build_<piece>.py` in production/cloud-week/kit/<piece>/ with Blender 5.2 as a Python module (or `blender -b --factory-startup -P build_<piece>.py`).
2. **Bring it in by the held-props route the street already has**, never by hand in the editor: copy the .glb under ledger/Assets/Props/base-mesh/, name it on a line of production/specs/vignette-bill-of-materials.json, place it in production/specs/vignette-scene.json (held_props: a placement is the mesh's BOUNDING-BOX CENTRE, never scaled; read its pivot_note), and import it with tools/ue/import_prop_meshes.py (to /Game/Ledger/Props/SM_<asset>, with collision). The stand-in it replaces and its place are in targets/SCENE-SLOTS.md. Check this route on the PC before the first piece: it was read, not run, from the cloud.
3. **Materials:** each material slot is named by what it is (paint_black, cast_iron, concrete, granite, glass...) with the target's base colour, roughness and metallic as starting values only; the look is made in Unreal against the Hook sheet. UVs are at real scale (1 UV unit = 1 m) for the tiling materials. Wear comes from the masks (unit 4.5, target 2.11), not the model.
4. **The gate:** the automatic check passed and two fresh reviews (street distance and close) passed in the cloud against photographs; the game's gate (CLAUDE.md: your check, a fresh reviewer per view in the game's camera, the Hook sheet, KCD2 frames) is still owed on the PC. Nothing is multiplied before Jafar approves one complete sample in the assembled game.

## Pieces built (kit)

| Unit | Piece | Model | Check | Reviews | For the builder |
|---|---|---|---|---|---|
| 3.1 | Front door: T1 terrace four-panel door, F1 flat's side door | production/assets/cloud-week/door/door_T1.glb (9,898 triangles, 397 KB), door_F1.glb (13,824, 540 KB) | kit/door/checks/check_v2.json: T1 162 of 162, F1 108 of 108 | try 2: all views pass; one narrow point | **Fix first:** delete the parts iron_bellpush_bezel and iron_bellpush_button from door_T1 (rebuild without them) so a plain dark oblong remains; the two-part push reads as a modern video doorbell. The brick plinth's returns (70 mm in front of each end of the threshold) belong to the wall kit, not the door. Paint colour is a build parameter (--door-colour). Notes: kit/door/NOTES.md. |
| 3.2 | Shopfront parts and Rita's front (bay 2): pilaster, console (carved leaf), fascia board with bed mould, cornice broken forward over the consoles, sill, stallriser, window frame with nine toplights | production/assets/cloud-week/shopfront/{pilaster,console,fascia_board,cornice,sill,stallriser,window_frame}.glb (1,762 / 8,592 / 148 / 1,278 / 116 / 2,620 / 3,028 triangles; each under 320 KB); the assembly shopfront_ritas.glb (27,898 triangles, 1.17 MB) is over the push guard and is NOT in git: `python build_shopfront.py` in kit/shopfront/ rebuilds it (3 min) | kit/shopfront/checks/check_v2.json: 171 of 171 | try 1: street PASS, close FAIL; try 2: see QUEUE.md | Built to the target PLUS seven departures from the fresh reviews, each in kit/shopfront/departures.py and NOTES.md (console profile and leaf, cornice break, cyma bed mould, nine toplights, tablet chamfer): the target's numbers for these are superseded; the cornice is 150 high (a heavier one, 0.4 to 0.6 of the board, is Jafar's call). Parts sit on the street datum (x 0 at the part's middle); the placement table is in NOTES.md. Doors, side door and lobby are not built: their slots are plain. |

## 2D (finished pictures, rebuilt by script; the PNGs are not in git)

None finished yet. 4.1, the fascia signs, is in its check (try 2); see the queue.

## Targets ready to build (each: TARGET.md, target.json, target_drawing.py, self_check.py, TARGET-REVIEW.md in production/cloud-week/targets/<family>/)

| Unit | Family | State | What the builder must know |
|---|---|---|---|
| 2.1 | front-door | done; built as 3.1 | the plinth returns are the wall's |
| 2.2 | shopfronts | done, fixes applied, not re-reviewed | ten fronts by table; Rita's is the model (bay 2); one CC0 photograph measured (a restored arcade), no 1990 provincial front reached when it was written |
| 2.3 | railings | done | one kerbside guard rail panel (welded, galvanised); its form is judgement: check two dated photographs before its build is gated |
| 2.4 | bollards | done | cast-iron domed posts at the yard mouth, plain posts at the quay end, ten mooring bollards, chain posts, cleats; unmarked |
| 2.6 | pillar-box | done; checked against two dated photographs on 11 October (PHOTO-CHECK.md): FAIL on proportion | build to PHOTO-CHECK.md's amendments: body 390 (not 489), 1500 high, cap 535, a straight black base 300 high, slot 250 wide; flush blank areas where cypher and lettering would be (canon owes the cypher) |
| 2.7 | kerbs-and-covers | done | half-battered granite kerb, two-course sett channel, the dropped crossover, a 485 x 325 gully grate, four blank covers; sizes re-measured at each panorama's own camera height |
| 2.9 | fascia-signs | done; made in 4.1 | ten boards, four hanging signs |
| 2.10 | posters-boards-plates | done, fixes applied, not re-reviewed | 84 items: posters, notices, To Let boards, street name plates |
| 2.11 | wear | done, fixes applied, not re-reviewed | 33 kinds of seeded mask |

## Research notes (production/cloud-week/research/)

1a sash windows at low angles; 1b a walk without foot slide; 1c night pools in Lumen; 1d shop glass without the frame cost; 1e Epic's Unreal MCP server in the 5.8 editor (a ten-minute test on the street).

## Found this week, for the builder (each is outside the cloud's reach)

- The street's lamp columns stand at x 8 east, 18 west, 28 east, 38 west (StreetVignette.cs steps by half the spacing), not "x 8, 28, 48"; their shaft is about 61 to 68 mm, not 114.
- The scene file's lantern colour (1, 0.7055, 0) is stale against the 589 nm derivation (1, 0.22, 0) the night note and the game's own look file use.
- The approved Hook sheet shows no lamp column; the "slender dark column" was the retired sheet's.
- Mickey's glass carries 0632 960418 and MINICABS · 24 HOURS from another family, not approved: the second contradicts the cast's hours (7.00 to 3.00); 0632 was a real exchange code (unchecked); for the town and the shop-room builder.
- Fascia textures are 5410 x 550: check in the installed 5.8.2 source whether a non-power-of-two texture gets mips before choosing make_fascias.py --pack pad or stretch (2d/fascias/NOTES.md).
- Pillow's Raqm layout on Windows: if `python -c "from PIL import features; print(features.check('raqm'))"` prints False, the kerning differs slightly and the SHA-256 hashes will not match; the pictures and checks still hold.
- Poly Haven's London panoramas were taken at 0.9 to 1.5 m, not 1.6 m: any size measured from them assumes the camera height measured per panorama (targets' calibrate.py).

## Not done yet

See QUEUE.md: the order from 11 October is 4.1, 3.2, 4.2, 3.3, 3.4, 3.8, 3.5, 3.6, 3.7, 4.3, 4.4, 4.5, 5.1, with 2.8 (lamp posts) and 2.5 (litter bins) finished beside them.
