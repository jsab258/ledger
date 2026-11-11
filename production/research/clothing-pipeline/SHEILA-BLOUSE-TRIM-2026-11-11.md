# Sheila's blouse worn under the cardigan: covered faces cut (11 November 2026)

Files in F:/LedgerTools/garments/sheila/blouse-under-cardigan-2026-11-11/ ("F:"): sheila_blouse_under_cardigan_skinned.fbx, trim.py, trim.json, trim.log, pic/. Blender 5.2.2 headless. Nothing imported into Unreal. Cardigan unchanged.

## Method (trim.py)
- Input: blouse-s4-2026-11-11/skinned/sheila_blouse_s4_skinned.blend, with the cardigan from chain2/skinned loaded onto the same skeleton, rest pose.
- Layers told apart as the report's blouse_outer.py did (faces looking away from the body = outer). Inner-layer faces use the reversed normal as "outward".
- A face is cut when every point and its centre have cardigan cloth within 40 mm along the outward direction, no point is within 15 mm of any cardigan open edge (V, centre front, neck, cuffs, hem), and no point is above z 1.33 (collar kept whole).
- A first try that also cut points poking out of the cloth ragged the collar wings; dropped, collar guard added.
- Faces deleted only: weights (65 groups) and both UV maps untouched; points left without a face removed.

## Counts
- Faces 35,845 to 10,908 (24,937 cut: 12,345 outer, 12,592 inner). Points 19,810 to 7,808.
- Blouse outer-layer points through the cardigan (below z 1.37, not on a cardigan edge face; signed distance to nearest cloth), before to after:
  - rest: over 1 mm 171 to 115; over 3 mm 88 to 59; max 11.8 to 11.8 mm. (Report's own count at rest: 176, 94, 11.8; this method reads 171, 88, 11.8.)
  - arms down: 464 to 181; 312 to 141; max 50.6 to 50.6 mm.
  - walking: 410 to 124; 262 to 82; max 51.4 to 51.4 mm.
  - seated: identical to rest in both (171/88 and 115/59), so that pose does not move the trunk.
- V opening: 1,148 front rays across the opening, same grid before and after: 897 hit cardigan, 251 hit blouse, 0 hit body or nothing. No hole. The V close pictures before and after look identical.

## Pictures
pic/final-*.png (pair), pic/before-V-* and after-V-* (V close).

## Faults
- The hem lump at z 1.0 (front centre and sides) is still there: its faces poke out of the cloth, so they are not "covered" and were kept. 59 points over 3 mm remain at rest, in z 1.009 to 1.274. It needs the cardigan pushed out or the lump faces cut by hand, a different fix.
- Down and walking poses: blouse still through the cardigan up to 51 mm at the arms.
- The pose figures use an own check (nearest-cloth signed distance), not parity_check.py, which measures body through one garment.
