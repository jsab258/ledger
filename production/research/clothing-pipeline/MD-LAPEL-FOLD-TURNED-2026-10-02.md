# Lapel, facing and collar in Marvelous Designer (2 October 2026)

The problem as given: a scripted jacket (pattern JSON, MD 2026.1) with a same-orientation facing on a Turned seam and roll lines at 330°, strength 8. The facing ends outside the front, the lapel does not roll, the collar sits behind the neck.

D = documented [source]. I = my inference.

## What the sources point to first

1. **Check the facing's offset happened.** On MD 2026.0.315, `SetArrangementPosition` moved nothing, though readback echoed it [17] (D). Check 2026.1 by exported vertices (I).
2. **Professionals place the facing themselves**, with Superimpose (Under) or Layer Clone (Under), after sewing [6, 7, 10, 12] (D). No source says which side a Turned seam puts it.
3. **A real facing lies wrong side to wrong side**, pointing the other way (I). Flip Normal turns a piece inside out and reverses its fold angles [11] (D).
4. **CLO's staff, for a blazer lapel:** fold angles back to 180, lapel-to-facing seams Turned, Strengthen, simulate, then fold [14] (D).

## 1. Turned seams

- Turned gives "a folded, two ply look", sewn "crisp and flat" [2] (D).
- Turned locks fold angle and strength [1, 4] (D); our FoldData there is probably ignored (I).
- It is for stacked layers, like shell and lining [15, summary; 9, p. 65] (D).
- It is a 180° fold at the seam, "as if ironed flat" [18] (D), so it expects pieces stacked, not side by side (I).
- JSON: `SeamLinePairGroupList[].bIsTurned`; each pair side has `Direction` [17, 20] (D).

## 2. Fold angle and strength

- 180 is flat. Towards 0 folds "towards the front of the pattern"; towards 360 "into the back". Strength 0 to 20: higher gets closer to the angle [1, 3, 4] (D).
- The 2024 guide says "0: fold forward, away from viewer" [9, p. 49] (D). Our panel test (30 against 330) settles the direction (I).
- Fold Arrangement pre-folds collars and cuffs "for better stability" [5]; no API call [16, 20] (D).
- Against gravity, Strengthen before simulating [9, p. 49] (D). `SetPatternStrengthen(index, bool)` exists [16, 20] (D), correcting the 1 October note.
- Whether a fold angle alone turns a lapel right back: not found.
- The collar's roll line should meet the lapel's at the collar edge [15] (D, summary).

## 3. How professionals build the front

- **One layer** (most advised, 2019): fold the front on its roll line; fake the facing with render thickness. "4 layers of fabric is difficult to simulate" [12] (D).
- **Sewn facing** [12] (D): fold and freeze the lapel; mirror the facing; sew it Turned to its outline drawn on the front; lower collision thickness; Superimpose (Under); Bond the facing.
- **Layer Clone** [12] (D): cut the folded front along a line; Layer Clone (Under) the lapel part, which lands folded in place; merge the front back; front on layer 1; collision 1 mm; Strengthen; simulate. Clones are sewn along every line [7] (D).
- Layer 1 lies over layer 0 with layer-based collision on [8]; return pieces to 0 at the end [17] (D).
- Non-zero Pressure blew a lapel up; facing collision 0.1 to 0.2 mm [13] (D).
- **Scriptable** [16, 20] (D): `LayerClonePatternPieceMove(index, x, y, bUnder)`, `CutPatternAlongInternalShapes`, `MergeSewnPatterns`, `SetPatternLayer`, `SetPatternFreeze`, `SetAddlThicknessCollision`, `SetSimulationLayerBasedCollisionDetection`, `SetArrangementOrientation` (degrees, default 180 [17]). **Not scriptable:** Superimpose, Flip Normal, Fold Arrangement, Bond (D, by absence). So the Layer Clone route needs no mouse (I).

## 4. The JSON file

- No published schema found. MD validates nothing: invented fields pass, missing ones read garbage; edit an exported file [17] (D).
- Our exports hold `strSuperImposeSide` ("None" on all 82 pieces), `ArrangementPointDataMap`, `FoldData`, `ButtonHeadList`, `ButtonHoleList`; no layer, Strengthen, Freeze or Bond field [20] (D).
- Other `strSuperImposeSide` values, and whether import honours them: not found.

## 5. Buttons and closing

- `AddButtonToPattern` and `AddButtonHoleToPattern(index, x, y, angle)` place them in mm, y downward, not on curved pieces [16, 20] (D).
- Fastening and Tack are by hand only [19]; no API call [16] (D).
- By script: a short seam between internal lines at button and hole, strength 0 (I, untested).

Not found either: a written 2023 to 2026 tailored-jacket breakdown.

## Sources (reached 2 October 2026)

MDM = support.marvelousdesigner.com/hc/en-us/articles/; CLO = support.clo3d.com/hc/en-us/

1. Seamline Property, 6 Jan 2026, MDM 47358171818521
2. Sewing Line Type, 2 Apr 2026, MDM 47358411103001
3. Fold Pattern, 29 May 2025, MDM 47358354961049
4. Fold Seam Line, 29 May 2025, MDM 47358411649305
5. Fold Arrangement, 29 May 2025, MDM 47358260153881
6. Superimpose, 29 May 2025, MDM 47358389619481
7. Layer Clone, 29 May 2025, MDM 47358338558745
8. Simulation Properties, 6 Jan 2026, MDM 47358125463321
9. Creator's Field Guide 2024, June 2024, s3.marvelousdesigner.com/newmdweb/case/20240626/MD+User+Guide+2024.pdf
10. Superimpose (Under), 29 May 2024, CLO articles/115012225947
11. Flip Normal, 29 May 2024, CLO articles/115012225847
12. Facing for lapel (forum), Aug 2019, CLO community/posts/360033634853
13. Pressing facing flat (forum), Oct 2019, CLO community/posts/360036347733
14. Blazer Lapel (forum, CLO staff), May 2024, CLO community/posts/32736330603929
15. Constructing a Collar/Lapel, undated, summary only, CLO articles/115013191087
16. CLO API list and changelog to V11.0.0 (Aug 2026), developer.clo3d.com
17. matty, md-conventions.md, MD 2026.0.315, 19 Sep 2026, github.com/matty/marvelous-designer-plugins
18. J. Versluis, Turned Sewing, 7 Jan 2021, versluis.com/2021/01/md-turned-sewing/
19. Fasten/Unfasten Button, 29 May 2025, MDM 47358265086361; Tack, 22 Oct 2025, MDM 47358185301017
20. Our 2026.1 API dump (md-api-2026.txt) and JSON exports, 2 Oct 2026
