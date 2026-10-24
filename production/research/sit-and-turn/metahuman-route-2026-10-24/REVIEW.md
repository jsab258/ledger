# Review of METAHUMAN-ROUTE-2026-10-24.md (fresh reviewer, 24 October 2026)

**Verdict: SOUND WITH CORRECTIONS.** The result stands: the walk does not pass, and setting it aside follows his rule. Even with the measure's own faults taken out, stops still slide about 15 cm and turns about 11 cm. The numbers and the cause given are not right as written:
1. The table's medians are the lower of the two middle values, not the median. Nine cells are low (check 1).
2. The worst figures for starts (12 cm), turns (21 cm) and the steady walk (25 cm) are not slides. They are Tom's right foot in mid-swing, which the measure reads as planted (check 4). Without them the worst values are 6, 11 and 12 cm.
3. "The worst slides (15 to 21 cm) match that 20 cm radius" is wrong. The 20 to 21 cm figures are those swing misreads. The 15 cm "stop" is a foot that slid as the run began. The radius in force at run time is not known: the 20 cm is the node's stored value, but a function call overrides it (check 2).
4. "Most steps now stay within the bar" is true only because the steady walk and the run are counted in. At starts, stops and turns, 29 of 46 contacts are over 3 cm.
5. His clips' "69 cm" stop is the run's 21 cm body drop. That is the same fault the footnote already sets aside for the run.
6. "Two runs each" is wrong for his clips: there is one run (default1).
7. Two of the four switch settings in the tries show no sign of having taken effect, so "Epic's defaults are the best of its own options" is not established (check 5).
8. The mover walks at the sample's 200 cm/s and runs at 500. The game's speeds are 160 and 420. The write-up does not say so.

---

## 1. The results table against the run files

All contact lines in gasp11a, gasp11b and default1 were recomputed per kind and per body (a script read the lines `..., his/the mannequin's left/right foot, slid X cm`).

**Worst values: all correct.** Tom: 12.01, 15.04, 20.91, 24.92, 6.14. Mannequin: 5.87, 17.18, 13.11, 22.87, 3.83. Clips: 37.68, 68.93, 49.72, 36.79. Each also matches the runs' header lines.

**Counts over 3 cm: all correct**, counting strictly over 3. Exactly 3.00 passes the bar: one such contact each in Tom's turns, the mannequin's stops and the clips' walk.

**Medians: wrong in nine cells.** Every median in the table equals the lower of the two middle values (the value at place (n-1)/2 when the steps are sorted). For an even count, the median is the mean of the two middle values. The method is not stated, and it always reads low:

| Cell | Table | Median |
|---|---|---|
| Tom, starts (n 10) | 2.0 | **2.8** |
| Tom, stops (n 16) | 4.6 | **5.1** |
| Tom, turns / walk / run | 3.4 / 1.4 / 1.0 | 3.4 / 1.4 / 1.0 (correct) |
| Mannequin, starts (n 8) | 4.2 | **4.6** |
| Mannequin, stops (n 14) | 3.4 | **3.6** |
| Mannequin, turns (n 18) | 4.8 | **4.9** |
| Mannequin, steady walk (n 40) | 2.6 | **2.7** |
| Mannequin, run | 1.9 | 1.9 (correct) |
| Clips, starts (n 5) | 25.9 | 25.9 (correct) |
| Clips, stops (n 4) | 18.4 | **19.9** |
| Clips, turns (n 18) | 6.2 | **12.9** |
| Clips, steady walk (n 40) | 2.0 | **2.5** |

So the summary's "median slide is 1.0 to 4.6 cm by kind" should read 1.0 to 5.1. The Why section's "medians 1.0 to 4.6 against 1.9 to 4.8" should read 1.0 to 5.1 against 1.9 to 4.9.

**Other faults in the table:**
- **"Of N" counts only the contacts that were itemised.** The header lines also count feet still planted when the route ends. That is 18 stops for Tom (table: 16), 18 for the mannequin (14) and 6 for the clips (4). The 22 October review asked for the header's figures; the table should say which it uses.
- **"Two runs each, the same start and heading."** The start and heading are the same in every run (100,400, heading 90). His clips have only one run.
- **His clips' 68.93 cm stop** (default1, 27.15 s) begins at about 27.0 s, just after the run ends. It slides 69 cm in at most 0.15 s, which is run speed. This is the RunDropCm fault the footnote excludes for the run. His clips' stop worst without it is 21.5 cm, and that one is the run's start (next point).
- **Kinds are assigned when a foot lands**, not when it slides (`MeasureBody`: `F.Kind[I] = Kind` at plant). So the 15.04 / 13.42 cm "stops" (24.96 / 24.94 s) are feet planted at the stop that slid 0.46 s into the run. Walking stops reach 12.6 / 12.9 cm (22.70 s). The first stop's 9.6 / 8.9 cm slides are counted as "loop". All of these are still joins, so the verdict is unchanged, but the labels in the summary are inexact.

## 2. Claims about the sample's files, checked in the exports

| Claim | Found | Where |
|---|---|---|
| Child-actor slot tagged `VisualOverride` | **True** | inspect.txt: `VisualOverride_GEN_VARIABLE (ChildActorComponent) component_tags=["VisualOverride"]` |
| The manager puts a class there and hides the mannequin | **True** | AC_VisualOverrideManager.t3d 651-713: GetComponentsByTag("VisualOverride"), then SetChildActorClass, then on the slot's attach parent SetVisibility(NOT IsValidClass(VisualOverride), not passed to its children) |
| "its mesh ticking always" | **True, but not set by the manager** | It is the character's own CharacterMesh0 setting, ALWAYS_TICK_POSE_AND_REFRESH_BONES (inspect.txt) |
| Kellan's Body tagged `RTG_UEFN_to_Metahuman_nrw` | **True** | inspect.txt, Body_GEN_VARIABLE |
| Kellan's Body runs ABP_GenericRetarget | **Not shown in the exports** | inspect.txt gives only the animation mode; BP_Kellan.t3d never names the graph. Epic's page (EPIC-SOURCES S2) says to set it. Note too that Kellan's body parts are ONLY_TICK_POSE_WHEN_RENDERED (inspect.txt). Tom's are set to tick always, so "as the sample dresses Kellan" differs there. |
| The graph looks the tag up in IKRetargeter_Map and copies from the parent mesh | **True** | ABP_GenericRetarget.t3d around line 601: owning component's ComponentTags[0], then Map_Find, then LoadAsset, then IKRetargeter. The map holds `RTG_UEFN_to_Metahuman_nrw` (inspect.txt). Retarget Pose From Mesh feeds the output; the Copy Pose node is unconnected. |
| (detail) | | The lookup uses the **first** tag. The code appends with AddUnique (SliceCharacter.cpp 460), so it works only while Tom's Body has no other tag. The runs show it works now. The graph's curve-driven Blend to Source covers the arms only (ChainCurveMap line 843: RightArm, LeftArm), so the legs keep the asset's settings. |
| CharacterInputState: WantsToWalk, WantsToSprint, WantsToStrafe, WantsToAim, WantsToCrouch | **True** | gasp_cbp.t3d: CharacterInputState is S_PlayerInputState with exactly these five. GetDesiredGait reads WantsToWalk, WantsToCrouch and CanSprint. UpdateRotation_PreCMC turns to the controller when WantsToStrafe or WantsToAim is set. Strafe being **on by default** is not in the exports (the struct's defaults were not exported). The walking backwards the write-up reports fits it. |
| `DDCvar.FootPlacementMode` (1 = the foot placement node) | **Meaning true; "its graphs read" not shown** | DefaultEngine.ini line 169: "0 == off, 1 == foot placement node, 2 == biped control rig", default 1. That name appears in neither gasp_abp.t3d nor gasp_cbp.t3d. The graph declares a FootPlacementMode variable (around line 63808) and never refers to it. The only data-driven settings the graph names are DrawCharacterDebug*, MMDatabaseLOD and OffsetRootBone.TranslationRadius. |
| Plant settings 20 cm, 0.2, 60°, 0.2 | **True as stored on both foot placement nodes** | gasp_abp.t3d around lines 14058 and 30476 |
| "bound at run time to its Get_FootPlacementPlantSettings" | **True, and it undoes the 20 cm** | PropertyBindings: PlantSettings bound to Get_FootPlacementPlantSettings (bIsBound=True). That function returns PlantSettings_Stops when the current database tags include "Stops", else PlantSettings_Default. Neither variable's value is in the export. So the radius and angle in force at run time are **unknown**, and the 20 cm / 60° the summary and the Why section reason from is the stored value that the binding replaces. |
| (not in the write-up) | | The node's plant-speed mode is not stored, so it keeps the engine default, Manual (AnimNode_FootPlacement.h:533). In Manual mode, planting follows the curves contact_l and contact_r, which a Remap Curves node turns into a speed (around line 14107: `contact_l=(1-contact_l)*100`). A missing curve means "unplanted" (AnimNode_FootPlacement.cpp around 1549-1553). ENGINE-SOURCE §3 found contact_l and contact_r only as "..._CURVE_CONTROL" names, unresolved. Whether the sample's foot placement plants at all is therefore open. |

## 3. Claims attributed to EPIC-SOURCES.md and ENGINE-SOURCE.md

- **"24 sources read 24 October": true** (S1 to S24). Not all were read in full: S10 to S12 are keyword sections, S21 and S22 were partly scanned, and S24 is a WebFetch summary only.
- **"They describe the 5.4/5.5 sample only": mostly.** The how-to pages describe the 5.4/5.5 layout, but S13 and S14 describe the 5.7 and 5.8 samples' new features.
- **"Nothing documents SandboxCharacter_CMC, AC_VisualOverrideManager or the ovw retargeter": true** (EPIC-SOURCES, main finding and "Could not be reached").
- **"Epic's one rule for a hidden mover ... always tick pose and refresh bones and tick before the worn body": true** (S4, S5).
- **"Speed Planting is documented for stored animations, not live play": overstated.** Epic's page shows only the export workflow. EPIC-SOURCES marks live use unverified and says the API page (S9) "suggests a live use". It should read "documented only for exported animations; live use unverified".
- **"Blend to Source = 1 on both legs": true** (ENGINE-SOURCE §1.4). ENGINE-SOURCE says this came from reading the asset bytes and was never seen in the editor; the write-up drops that caveat. "Whatever the mannequin's feet do, his copy" is stronger than the source, which lists six ways a still mannequin foot can still give a moving MetaHuman foot (§2.2). The trace does support it closely: in trace1 the two balls stay within about 1 cm of each other through a stride.
- **"Speed Planting is inert ... no per-foot speed curves": true** (§3: the curve names are None, and the animations carry no such curves).
- **"The retarget node walks up the attachment chain": true** (§4).
- **Direction A, "an IK Rig node fed world-space goals after Retarget Pose From Mesh (point 5)": true** (§5 and short answer 5).
- **Minor points in the sources themselves:**
  - ENGINE-SOURCE §5 lists the node contents of SandboxCharacter_**Mover**_ABP, while the route runs SandboxCharacter_CMC_ABP.
  - EPIC-SOURCES says reading ran "07:30 to 08:45". The go began at 08:06 (commit 11b2116f) and the file was last written at 08:24.

## 4. The four harness faults, and whether the measure is fair

**The four fixes are genuine, and none of them flatters the walk.**
- **Fault 1:** the mover now follows any move the game makes of Tom (GaspTick 494-502).
- **Fault 2:** strafe is off (GaspTick 519). This is the right set-up for a player who turns to where he goes.
- **Fault 3:** the worn parts always work out their pose (StartGaspMover 451). A frozen body would read worse, not better.
- **Fault 4:** the ground under each ball is now traced (MeasureBody 751-759). This fits "within 2.5 cm of its standing height" better than the capsule's foot did on kerbs and the pavement's fall. It removes false contacts that read as metres of slide.

**The measure has a fault the write-up missed, and it makes the numbers worse:**
- **What it does.** A foot counts as planted when `H - Rest < 2.5` **and** `H <= H_other + 1.0` (MeasureBody 781). The second test compares heights over the ground, not heights above each foot's own standing height.
- **Why it catches Tom's right foot.** In trace1, Tom's right ball stands about 0.2 to 0.6 cm lower over its ground than his left. This comes from the trace's down and up flags. Those flags are printed before they are updated, so each line shows the previous frame's state.
- **What the trace shows.** At 6.00 s (stretch 1, T 0.94 to 1.00), his right ball passes 1.3 cm above its standing height in mid-swing, moving about 12 cm a frame (about 620 cm/s), while his left foot is flat. It passes both tests and is read as planted. The mannequin's ball passes just as low (1.4 cm) but its heights differ the other way, so it is not read as planted.
- **The same pattern in every run.** One frame read as planted gives a 0.00 cm "slide"; two or three frames give 10 to 31 cm. In gasp11a/b these "contacts" begin 0.21 to 0.29 s after the same foot lifted, on most right strides. They are absent from the mannequin, except once at 16.17 s.

These are Tom's worst start (12.01), both worst turns (20.91, 20.51), the five steady-walk values of 20 to 25 cm, and t2rminia's 30.95 turn. Without them (by that timing pattern; trace1 proves one instance directly), Epic's route reads:

| Kind | Tom: median / worst, over 3 cm | Mannequin |
|---|---|---|
| starts | 2.8 / 6.0, 4 of 8 | 4.6 / 5.9, 7 of 8 |
| stops | 5.1 / 15.0, 12 of 16 | 3.6 / 17.2, 10 of 14 |
| turns | 3.3 / 11.0, 10 of 18 | 4.9 / 13.1, 18 of 18 |
| steady walk | 1.4 / 11.7, 8 of 38 | 2.6 / 9.6, 15 of 38 |
| run | 1.0 / 6.1, 2 of 16 | 1.9 / 3.8, 1 of 16 |

Still a fail, and now Tom and the mannequin agree at the worst steps as well as at the medians. Ways to remove the misread: compare each foot's height above its own standing height; add a speed gate, as the write-up's direction C proposes. The 2.5 cm band alone cannot tell a swing from a stance, because both bodies' swing balls pass within 1.5 cm of standing height.

The write-up's own wording, "no higher than the other foot", leaves out the 1 cm margin that causes this.

## 5. The two tries, and "set aside after two tries"

- **Try 1, part one: MMDatabaseLOD 1.** It plainly took effect (stops 71.6 / 71.6 cm).
- **Try 1, part two: FootPlacementMode 2.** It shows no sign of taking effect:
  - The CVar's name appears nowhere in the exported graph or character.
  - t1fp2a/b reproduce gasp11a/b within the spread between gasp11a and gasp11b. For example, mannequin loop 22.86 / 11.82 against 22.87 / 11.51, and stop 16.20 / 16.89 against 16.38 / 17.18.
  - The value logged at start-up (StartGaspMover 483) is not in the run files.
- **Try 2: attribute-based root motion.** Same doubt:
  - The character's UsingAttributeBasedRootMotion is declared and nowhere used in gasp_cbp.t3d.
  - The `DDCVar.AttributeBasedRootMotion.Enable` name appears in neither export.
  - The results match the default once the swing misreads are removed: start 6.0, stop 15.2, turn 11.3.
- **What the tries tested.** Both are switches among Epic's own options, which is a fair first step. Neither tests the cause the write-up gives (the plant settings, or a lock).

**Does setting it aside follow?** Yes, by his rule: two tries failed, then research. But "Epic's defaults are the best of its own options" is not shown, because two of the four settings may have done nothing. Mending the measure (check 4) is a fix to the measure, not a third try at the walk.

## 6. The Why and the next directions

- **"The mannequin under him slides about as much as he does": supported**, and more firmly once the misreads are out (check 4 table).
- **"The bound is the sample's own foot placement ... 20 cm or 60°": unverified, stated as fact.**
  - The plant settings in force come from PlantSettings_Default and PlantSettings_Stops, whose values are unknown (check 2).
  - Whether the node plants at all depends on contact curves that ENGINE-SOURCE could not find.
  - No run isolates the node.
- **"The worst slides (15 to 21 cm) match that 20 cm radius": not supported.**
  - The 20 to 21 cm values are swing misreads.
  - The 15 cm one is a foot sliding as the run begins.
  - The match is a coincidence.
- **The frame trace of the stop (trace1, stretch 2): roughly right.**
  - **The planted foot.** The left foot moves 8.8 cm back and 7.7 forward while flat (recorded as 8.95 cm, labelled "loop"); the write-up says "about 7".
  - **The scuff.** The trailing foot travels 45.5 cm forward at 1.2 to 2.4 cm above standing height, not "2 to 3 cm". The measure does **not** read it as planted. That contradicts direction C's "counts the stop's scuff ... as slide". The heel-pivot part of C is untested.
  - **Not mentioned.** Afterwards the right foot steps back 51 cm, at most 3.9 cm up. The feet first land 30 to 40 cm ahead of where the capsule stops.
- **Speed (not in the write-up).** The mover's walk is 200 cm/s and its run 500 (the runs' "max 200/500" and "200 cm/s" lines). His clips run at 160 and 420. So the comparison is not at one pace, and on this route Tom would walk a quarter faster than the game's pace.
- **Next directions.**
  - **C should come first.** The evidence for it is now specific: the swing misread, kinds labelled by landing, and itemised counts left short of the header's.
  - **B needs two facts before it is worth doing:** the values of PlantSettings_Default and PlantSettings_Stops, and whether the contact curves exist.
  - **A follows from ENGINE-SOURCE §5** and remains a reasonable research direction.
- **Cost.** By the commits the go ran 08:06 to 09:34, about 1.5 hours, not "about 2".
