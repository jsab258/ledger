# Ron's donkey jacket, worn in the game (night of 28 to 29 September)

The jacket of 28 September (../donkey-jacket-2026-09-28/), taken on until it stopped failing in plain sight, then checked against production/reference/donkey-jacket-1990.md and by three blind reviewers, all of whom failed it. Set aside (review-3.md): not on Jafar's page.

What changed, each against a fault seen in the game's own frames:

- **Length**: the hem let down to mid-thigh, a back length of 80 cm (the references: 81 to 90 cm; it was 72).
- **The jumper through the cloth**: the front had settled back onto his belly, to 1 cm of his skin, and his jumper, which lies on the skin, showed through. After the drape settles, every point of the body of the jacket nearer his skin than 3.5 cm is carried back out to 3.5 cm (drape_jacket.py, JUMPER_CLEAR); and in Unreal each point of the cloth may move at most 1.5 cm from where his movement carries it (make_cloth_jacket.py, the template's SimulationMaxDistanceConfig), where before it sank freely onto his collision shapes. Melton is heavy and stiff and moves with the body.
- **The chest**: his pectorals showed through, and after the jumper fix the chest read as a bust (the first blind review). After the drape settles, the front is hung straight again from the fullest point and the chest filled across its hollows, slice by slice, as stiff melton spans them.
- **The sleeves**: stood off his arm point by point they kept his biceps and read as a quilted puffer's (the first blind review); each is now a straight tube tapering from the upper arm to the cuff round the arm's bones.
- **The collar**: a 3.5 cm stand and a fall close round the neck, its points on the upper chest (the first read as two small tabs, a later one as a sailor's collar), made as a solid piece the game fixes to his upper back (LedgerJacket.h, spine_05). As part of the cloth's render mesh it flew out in spikes; as a second simulated layer 12 mm over the yoke, the collar's points and the yoke's were drawn to the wrong layer and both came out torn and blotchy. Taken out of the cloth, the yoke is one clean panel.
- **The front**: a groove down the front, a few centimetres to one side of the buttons, reads as the overlapping front's edge (buttons had sat on a front with no opening; a cut right through showed the jumper).
- **Pockets**: two flapless patch pockets, their foot about 8 cm above the hem, straight-edged, each a solid 4 mm patch whose rim catches the light (a flat layer did not show at all; a turned-back lip rendered as black slots).
- **The yoke**: black (0.004) and glossy (roughness 0.3) against the navy, cut straight across the top of each shoulder, and at the back down to the armpits, 30 cm below the collar seam (it read as a grey smear with torn ends, and the back was a shallow band).
- **Buttons**: five, from the neck down, evenly 16 to 17 cm apart (four started below the yoke).
- **Sitting**: a sit made in Blender on his own skeleton (tools/meshgen/blender/sit_anim.py: thighs up, knees bent, the back a little forward, arms down with the forearms on the lap, the pelvis lowered so the feet stay on the floor), imported onto the MetaHuman skeleton (tools/ue/import_anim.py). The first came in a hundred times too big: the skeleton's parent, which scales it to metres, had been dropped.
- **The films**: the portrait tool's motion shot now frames the whole person, so the hem and the lap are seen.

Films (the fourteenth round, cloth asset CA_ron_donkey_09290118, cloth-asset.txt): films-sheet.jpg (walk, Epic's walk loop; arms, Epic's body range of motion; sit, no chair in the scene yet; four frames a second, the cloth simulating in real time) and still.jpg. front-back-check.jpg: the Blender check renders, front and back. ron_donkey.json: the drape's measures.

Reviews: review-1.md (the seventh round: FAIL, four obvious faults, acted on), review-2.md (the eleventh round: FAIL, four obvious faults, three acted on, the skirt's weights researched), review-3.md (the fourteenth round).

Next, researched but not run (production/research/character-pipeline/cloth-weight-maps-2026-09-29.md): a maximum distance that grows from the hips to the hem, written by two Dataflow nodes (a linear gradient sampler into a MaxDistance weight map), so the skirt hangs from the body instead of following the thighs.
