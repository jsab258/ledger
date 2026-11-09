# Tom's boots: the "lace stub" at each instep, diagnosis, 9 November 2026

The fault: two final reviewers of packaged build 41bb9d7 saw "a dark lace stub with a pale tip" at each instep, just below the jeans' hem, and called it a stray piece on a laceless boot (F:/LedgerTools/gate/new/tom-whole-2026-11-09/review-whole.json). Working files: F:/LedgerTools/garments/tom/boots/lace-stub-diagnosis-2026-11-09/ (probe1-3.json and their scripts, crops, history-sheet.jpg).

## Is the measure wrong?

Partly. The fault is real, but the reviewers' reading of it is wrong. The boots do have laces: six eyelet pairs and six lace bars a boot (probe1.json). The listed shortfall "no laces or eyelets modelled" is false. The stub is the boot's own lowest lace bar and its front eyelet. Because that bar runs along the foot, not across it, it reads as a stray piece.

## 1. Where it is (high confidence)

- **In the boot's own mesh.** Not the jeans, the body or a map. tom_boots_skinned_v4.fbx (the garments.json row) has, per boot, 12 eyelet rings and 6 lace bars, at about 55, 74, 91, 110, 129 and 146 mm above the sole. The boot's top line is at 158 / 157 mm (probe1.json, probe2.json).
- **The lowest bar.** On the left boot it runs from an eyelet at (x 165, y -113, z 54.5 mm) to one at (185, -65, 56): 48 mm along the foot and 20 mm across, so from the front it looks upright. It lies 0.1 to 3.8 mm off the leather, about 100 mm below the top line, so it does not poke up (probe2.json). The right boot mirrors it.
- **Against the jeans.** Jeans n7's hem sits at 77-78 mm at the front of each foot (probe2.json). The lowest bar and its eyelets lie 9 to 24 mm below it. A ray toward the front camera finds them all uncovered, and every higher row covered. The jeans were draped to rest on the instep with the laces bridged (DECISIONS.md, 30 Oct 14:00).
- **Why it runs along the foot.** The bar is inherited from Ron's passed pair: Ron's v2 has the same lowest pair, at y -123 and -76 (probe3.json). The first version of tools/meshgen/blender/model_footwear.py placed each boot eyelet with a level ray from the front at the row's height, 15 mm either side of the lace line (lines 590-597). On the shallow vamp at 55 mm, one ray lands 48 mm ahead of the other. Ron's bare-legged picture shows it (gate/new/tom-outfit/2026-11-02-sole4/ron-boots-dress.png).
- **The colour and the pale tip are as built.** v4's UVs equal Ron v2's exactly (probe3.json), and the maps are Ron v2's. The lace samples part ID 0, so it gets the boot's near-black tint. The eyelets sample ID 0.75 (TeethColour 0.16), metal 1, roughness 0.38 (ron_boots_v2_packed_polished.png). That metal ring is the pale tip: about 135 brightness in the picture, against 97-99 for the leather's brightest pixels. There is no alpha or UV-island fault.

## 2. Bind pose or posed (high confidence)

It is there at bind pose: the geometry above is unposed. The bar and its eyelets are weighted 100% to foot_l / foot_r, as are the nearest upper points (probe2.json, probe3.json), so they move with the leather in every pose. Not measured: the hem's position in the game's idle pose. The second row's front eyelet sits level with the hem (-2.4 to +3.8 mm) and could peep.

## 3. Earlier pictures (high confidence)

The stub has been there since Tom first wore the boots. The 30 Oct dress5 reviewer wrote "one short flat dark lace stub rising from one pale eyelet... not new: present in dress3 and dress4-cut" (F:/LedgerTools/gate/new/tom-outfit/2026-10-30-dress5/review-tom-boots.json). The 2 Nov toe3 and sole4 reviewers wrote "the lace ends come out from under the hems as before". DECISIONS.md (30 Oct 17:52, 2 Nov 15:33, 4 Nov 15:44) lists "laces barely seen". Not a regression; history-sheet.jpg shows four dates.

## 4. Smallest fix and its proof

- **Smallest fix for the stub:** a v5 boot without the lowest lace bar and its two eyelets (48 points a boot, nothing else moved). The stub goes, but no lacing then shows, so the slip-on read stays.
- **For the lace-up ruling instead:** lacing must show below the 77 mm hem, laid across the vamp. That is a redesign (the script's later open-throat branch with crossed laces). DECISIONS.md (2 Nov 15:33) records no further boot try without his yes, and any change would be a fifth version.
- **Offline screen:** probe2.py's ray test on v5 with jeans n7 must find 0 uncovered lace or eyelet points.
- **Packaged proof:** the same capture as 41bb9d7, with boxes placed relative to the hem (frames have shifted about 10 px before). In tom-boots-dress: left x 615-655, y 785-860; right x 2015-2060, y 895-975. In tom-whole-dress: x 1410-1430, y 1245-1265. Test:
  - no pixel above the leather's maximum plus 10 (about 110);
  - no dark strip: no column dipping more than 15 below the leather median over more than 20 px;
  - then a fresh reviewer at full size.

## 5. Not checked

- The packaged build's import log, to confirm that 41bb9d7 carried v4. The geometry matches the picture, so this is likely.
- LODs 1-3.
- The idle animation's hem and the ankle's corrective joints.
- Why the lace reads mid-grey, not near-black (presumably roughness 0.54 sheen).
- Whether Ron's own boots show the bar as a fault under his trousers.
