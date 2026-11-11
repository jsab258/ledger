# Sheila's shoes, modelled new with model_footwear.py on MH_LenaS4 (11 November 2026)

Second route for step 4 (first: Ron's boots carried and cut, SHEILA-SHOES-S4-2026-11-11.md). Files in F:/LedgerTools/garments/sheila/shoes-s4-model-2026-11-11/ ("F:"). Blender 5.2.2 headless, body F:/LedgerTools/bodies/MH_LenaS4/MH_LenaS4_FullBody.fbx. Nothing in Unreal or git. About 1 h.

## Made
- model_footwear.py --kind shoe --ease 0.0075 (the script's own knob, 3 mm over its default) gave one clean build (F:m2): foot 246 mm, 4 eyelet pairs, 20 mm sole stack with 3 mm welt, mid-brown colours from the first route's colours.json (the script's own upper is near black).
- Skinned with skin_shoes.py (left shoe, mirrored; foot and ball bones, at most 2 influences). Final: F:skin3/sheila_shoes_skinned.fbx and .blend. One bespoke script (F:scripts/split_left.py) splits the left shoe, sets colours and pushes the front collar forward 6 mm.
- Triangles: 20,152 for the pair (10,076 a shoe), 10,120 points.
- Raise: 16.0 mm (sole's lowest point 17.15 mm under the bare floor of 1.11 mm). The script's 20 mm stack is 16 mm below the floor; the first route raised 20.6.
- Topline: 62.8 mm above her bare floor at the heel (78.8 above the sole); highest upper point 85.5 mm. Footprints: F:footprints.json (rise 25 mm).

## Foot through the visible outside, over 1 mm (F:posecheck3.json)
Points, worst mm. Left, right:
- Rest: 0, 0. Toe bend: 0, 0.
- Walking: 0, 10 (2.1 mm, right back foot, heel up 20 degrees, 72 to 97 mm above the sole).
- Sitting: 2 (1.2), 2 (1.2), at 72 mm.
- Stair, left: 13 points, 2.6 mm, at the front collar edge (97 to 101 mm).
Not met: walking right, sitting and stair are over 1 mm. Both tries on this fault used: try 1 (ease 7.5 mm) took rest and toe bend to 0 and stair worst from 7.0 to 4.6 mm; try 2 (collar front forward 6 mm) took the worst to 2.6 mm. First route's stair: 13 points, 6.9 mm, all else 0. Stretch worst 1.1 (1.7 at the ball blend in toe bend).

## Pictures (F:pic, 1000 px workbench, her body grey-pink; far 4.4 m, near 1.2 m)
far-side, far-front, far-back, far-threeq; near-side, near-front, near-back, near-threeq. Also the script's own feet-*.png in F:m1.

## Read from the close pictures
- Collar edge: clean, continuous, no flaps or ragged teeth; no floating eyelet slivers. In near-threeq a thin pale gap shows at the front collar of the right shoe, where the forward push opened the tongue's edge (not fixed, tries spent).
- Sole: slim, 16 mm with a 3 mm welt, a plain women's flat sole; not a work boot's.
- Faults seen: the upper's side wall is lumpy above the welt behind the ball (near-side); the toe cap is a blunt shape; eyelets and laces are small. Heel flat, no heel block (as the first route). No texture maps made. Nothing measured in Unreal.
- UV: the pair has the script's single layer; maps not made.

Choice: this route looks like a flat women's derby; the first looked like a work boot. Posed through-faults are small and at the collar front.
