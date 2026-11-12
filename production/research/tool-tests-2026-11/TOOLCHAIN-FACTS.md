Method researched: production/research/tool-tests-2026-11/ round reports (MOTIONSMITH-ROUND1-2026-11-12.md, SEAMSHIFT-ROUND1-2026-11-12.md, CASCADEUR-METHOD-2026-11-12.md, METATAILOR-METHOD-2026-11-12.md, VELLUM-METHOD-2026-11-12.md), read 2026-11-12

# What an AI builder needs from its tools: facts gathered from the tests

One growing note (advisor 119, 120, 122, 12 Nov 2026). Setting-free: anything about one game's period, town or cast stays in the reports it links. It becomes the recipe's toolchain chapter at the phase's end. No design yet: facts, with their evidence file.

## The shared core (seen across the tools tested so far)

- **Job in, result out, no window.** A job file names inputs, settings and pass bars; the run writes the output, a pass/fail file with every bar's before and after, a log with input and output fingerprints, a picture and a film. Exit code says pass or fail. Seen working in Motionsmith and Seamshift; Cascadeur and MetaTailor needed clicks or crashed on the scripted route (MOTIONSMITH-ROUND1, SEAMSHIFT-ROUND1, CASCADEUR-TEST4, METATAILOR-TEST).
- **Same input, same bytes.** Two runs give identical files (Motionsmith 28 of 28; Seamshift twice). Without it, a builder cannot tell a fix from noise.
- **One body and skeleton loader** that matches the engine's character skeleton exactly (joint names, axes, units, rest pose), read from the engine's own character files, for every body variant. Both of his tools rebuilt this separately.
- **One check suite**, used by every module and by the tool's own tests, with one definition of each measure (planted foot, standing leg, cloth inside the body, band height). Motionsmith's make and fix judge "planted" and "standing" differently, so its own moves fail its own fix bars.
- **The identity case first.** Running a correction on something already correct must change it by under the measure's tolerance. Both of his tools fail it in round 1 (Seamshift's identity fit moved the garment; Motionsmith's fix bent clean knees by up to 43 degrees). A cheap test that exposes a whole class of rule faults.
- **Stand-in inputs as hard as the real faults.** Test inputs must carry the real input's fault sizes (measured from a real case), not mild ones; Motionsmith's stand-ins carried about an eighth of a real solve's knee error and passed.
- **Engine round trip as a check.** Import the output with the engine's own importer, export it back and compare: proves the file is read as written (Motionsmith: identical to 0.001).
- **A film with the real body, not a skeleton**, so the look can be judged from the tool before the game.
- **Every number with its source** (Motionsmith's MECHANICS lists each value, estimates marked): lets a reviewer find the rule behind a fault in minutes (the 18-degree "leave alone" limit was found there).

## Per kind of tool

### Motion clean-up and making moves
- Needs: contact pinning (feet held while planted), standing legs straightened, floor kept, timing kept, hands to targets, moves made from a few key poses, refit to other bodies by limb length, root motion for travel.
- The hard part: telling a fault from intent. Deciding "standing" from the knee angle fails both ways (a sunk solve left bent, a deliberate bend flattened). Contact and pelvis height against leg length are the facts to decide from (MOTIONSMITH-ROUND1).
- Lacked so far: Cascadeur straightens no knee and pushes toes into the floor (CASCADEUR-TEST4); Motionsmith leaves solve-sized bends alone.

### Garment fitting onto other bodies
- Needs: fit a finished, skinned garment onto another body with no cloth inside the body, bands at their heights, UVs and skinning kept, layered garments counted together (an open front over a lower layer).
- Lacked so far: Seamshift fails layered garments and its identity case (SEAMSHIFT-ROUND1); MetaTailor needs clicks (METATAILOR-TEST).

### Hair (strands and cards)
- Needs: strands grown on the character's real scalp (a painted mask), cut by per-zone lengths, curl and clumping, exported as engine-readable curves (Alembic groom), plus a cards version for distance placed outside the scalp, budgets per head, pictures beside the reference photographs from the bar's views (crown from behind, talk close-up, the distances).
- Checks must measure what is seen, not what was made: a card count passed while nine in ten card points sat inside the head (LOOMWRIGHT-HAIR-ROUND1). Coverage of the scalp from the camera, measured lengths per zone, facial strands rooted on skin.
- A named person's job must fail without its real head and reference photograph, rather than fall back to a proxy silently.
- Lacked so far: Houdini's free edition cannot write the Alembic (PLAN-2026-11-11); Loomwright writes it and Unreal imports it, but grows on a proxy head and buries its cards.

### Cloth drape, procedural building
- To be filled from the next rounds (Loomwright's cloth and streets; the Vellum tests VELLUM-TEST2 and VELLUM-TEST3 hold the commercial side).

### File formats
- Write binary FBX (or OBJ beside it): ASCII FBX is read by Unreal but refused by Blender (LOOMWRIGHT-HAIR-ROUND1), and the checks run in Blender.
