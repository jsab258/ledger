# Sheila's shoes, from Ron's boots carried to MH_LenaS4 and cut to a low derby (11 November 2026)

Step 4 of SHEILA-REFIT-PLAN-2026-11-09.md. Files in F:/LedgerTools/garments/sheila/shoes-s4-2026-11-11/ ("F:"). Blender 5.2.2 headless, own process. Nothing in Unreal or git. About 1.5 h.

## Made
- **F:sheila_shoes_s4_skinned.fbx**: 4,637 points, 9,186 triangles, six leg and foot bones (Ron's weights kept point for point), UVs from Ron's v2 (rim faces have none). Blend: F:sheila_shoes_s4.blend.
- Layout check (plan's open question): her full body shares the 51,619 points and 95,330 faces of Ron's. The carry ran in one try (F:carry.log, carry.json; mean move 27.3 mm, leather 5.0 mm median off her foot, toe 25 mm beyond her 245 mm foot).
- Cut (F:scripts/cut_derby.py): collar line level at 55 mm above her bare floor round the ankle, rising to 92 mm over 12 mm in front of the medial ankle bone to the throat; faces above deleted, rim bridged between outer and inner shell; 3 of 6 eyelet pairs and lace crossings kept. Colours (F:colours.json): mid brown upper, dark brown sole, brown laces, dull metal eyelets.
- Footprints: F:footprints.json. raise_mm: 20.6 (lowest sole point 20.45 left, 20.60 right under her bare floor; flat sole floor 20.0).

## Checks (measured; F:cut3/measure.json, posecheck.json)
- Standing: sole lowest point 20.45 / 20.60 mm under the bare floor, so raise_mm 20.6 puts it on the floor.
- Foot through the shoe's visible outside, over 1 mm: rest, walking, sitting, toe bend 0 each foot (toe and heel 0). Stair, left foot: 13 points, deepest 6.9 mm, at the top eyelets about 110 mm above the sole.
- Upper at the ankle: 56.1 mm above her bare floor (76.6 above the sole). Her lateral ankle bone tip is at about 64 mm, so the collar sits 8 mm below it.
- Pictures (1000 px workbench, her body in grey-brown): F:pic/far-side, far-front, far-back, far-threeq (4.4 m, camera 1.6 m, 180 mm lens on her feet); near-* the same at 1.2 m.

## Tries
- Collar try 1 (ramp from the ankle centre): upper at the ankle read 91 mm (ramp over the ankle bone); redone with the ramp starting 18 mm further forward (try 2).
- Collar edge: ragged teeth (clamped only the high points); fixed in the second try by setting every cut-edge point on the line. Both faults used their two tries.

## Left, plainly
- Heel: 20 mm flat, not 25 mm. The game's floor is flat under a flat-posed foot; a raised heel needs a pitched foot. No heel block made.
- The shape is still Ron's work boot: a wide, chunky sole and welt flange (about 29 mm thick), not a slim women's sole; the toe is Ron's plain toe. Looks heavy beside a 1990 court-type derby.
- Eyelets and laces read as thin slits at this workbench shading; three pairs only (a fourth would meet the ankle bone).
- The steep step at the quarter's front edge is the cut line's rise (about 70 degrees).
- Stair pose: edge stretch worst 3.0 (rest 1.0), where the cut-edge points moved.
- No texture maps made (brief asked for colour only); footwear_maps.py not run.
- Unmeasured: anything in Unreal.
