# One-shot builder "bridge": the real town code in the prototype, and the engine parts

Friday 20 November 2026. Branch os/bridge (pushed as oneshot-bridge). What changed for the player: production/lane/ONE-SHOT-SIM-DIFFERENCES.md.

## Parts

- 9.3 One simulation: built. The prototype runs the game's own town code through the bridge. Tests: test/game/town.mjs (21 checks), tools/lane/one-sim checks T13 and T14 (new) beside T1 to T12. Thin: the talk of the 19 people the real cast lacks is still the prototype's own; the nine stand by the prototype's week, not the real routine (a switch, off).
- 2.2.1 Seven slots per act: built shallow (unchanged from round 6: one event an act, each witness holding what they caught). No new test.
- 2.2.2 Identification ladder: passes its test. The rung is the real rule's (Perception::IdRung) for everybody. Tests: one-sim T13 (528 golden rows through the new door), game/town.mjs, pieces witness_mind (31 cases).
- 2.2.3 Sight by distance and light: passes its test for the rung (figures at 5, 15, 30 m, light 1, 0.7, 0.12 in game/town.mjs; 324 InSight golden rows through the door in T13). Who has him in view at all is still the prototype's geometry.
- 2.2.4 Sound reach: built (the prototype's numbers, unchanged). Checked against the real rule at two points (3.6 m at three in the morning, nothing at noon). The real rule's 100 AudibleRadius rows pass through the door (T13).
- 2.2.5 Give-away rules, and 1.4.4 Give-aways and the coat: built shallow, passes its piece test (pieces giveaways, 20 cases, one per give-away: ER-EYES-10). Thin: blood, dirt, wrong clothes and bruises are read only if another builder sets them on Tom.
- 2.3.1 Per-person memory store: built. Memories keep the rung; the town's memories travel in the save. Test: game/town.mjs (every memory survives save and load).
- 2.3.2 Witness certainty: passes its test (sure follows the rung: pieces witness_mind; game/town.mjs).
- 2.4.1 Transmission: built. Between people the real town has it is the town's own, read back into their minds. Tests: one-sim T8, T9 (the C# rows), game/town.mjs.
- 2.4.2 Cooling by kind: passes its piece test (pieces cooling, 13 cases). A prototype-side rule; the moat is untouched.
- 2.4.3 Showing what people know: built (unchanged: looks, remarks to his face), fed by the town for the nine.
- 2.4.4 It comes back: built (unchanged rule, fed by the town). Not measured again over 16 seeded weeks in this run.
- 2.1.3 Off-screen life: built. The real town runs through skipped time (sleep, the cells) hour by hour.
- 2.14 Each person's temper: passes its test (the same wounding: a timid witness stays away, a steady one goes, a friend does not; a victim settles or does not; game/town.mjs, one-sim T14).
- 2.10.2 Rival eyes and ER-EYES-05: built shallow. LEDGER.game.town.chain(person, event) and reactions() print the chain for every remark to his face, statement, visit by DS Ellis and arrest; the test asserts every chain ends at somebody who saw it. Rivals' own moves are the rise builder's to print through the same call.
- 7.8 Saving: built. The town in the save, same to the last character after a load; an older save loads with a fresh town. Tests: game/town.mjs, test/oldsave.mjs (with an older build), one-sim T10. Thin: "the same next hour after a reload" is held for the town only; the prototype's own chance is not seeded across a reload.

## Decisions taken (recorded here as the brief asks)

- DIFFERENCES.md's seven decisions: by the recommended answers and the brief; the table is in ONE-SHOT-SIM-DIFFERENCES.md.
- tools/lane/one-sim/ was changed (the checklist says never; the brief orders the review fixes): doors only, no rule. one_sim.cpp gained six calls (an open act, the rung, in sight, how far a noise carries, would this person report, the same for a person the cast lacks, a temper). The loader and the bridge gained the same, calls that do not wait for a promise, and the crimes that are no damage.
- Licences: the library pieces inside one-sim.wasm ship under allowlist item 18 (permissive, notices kept). Credits: tools/lane/prototype/ONE-SIM-CREDITS.md, copied beside the page by the build. Four third-party notice files it names were not read (this run had no page reader): owed before publishing.
- one-sim.wasm is not in git (it is built from the town code). build.py takes it from ONE_SIM_WASM, or ONE_SIM_WORK/wasm, or /home/claude/one-sim-work/wasm.

## The seeded week

- With the real town in, the seeded week still plays to its end and gives the same result twice (digest 8d5ba989f0992b10e1c7 on this branch). Against round 6's record: 115 events (97), 208 tellings (177), 188 Ledger entries (157), pocket 68.40 (68.00), 22 noted lines (24), 13 talks (13). More events because the real rung turns some sightings into new kinds of sighting; more tellings because the town's own talk reaches the nine.
- The record test/golden/week.json is NOT rewritten here: every builder changes the week. The manager writes it once the build settles (node test/same_week.mjs --write).

## Known faults

- The old trigger for DS Ellis (the street's loudness, Thursday or Friday) still runs beside the real one: it is in police.js.
- The arrest scene charges the prototype's hours and bill, not the town's custody.
- A covered pair's "heads together" is never caught (the town hands out no tellings).
- The switch that moves the nine by the real routine is built and not walked.

## Needs from others

- Manager: after merging, rebuild the simulation file from this branch's front door (tools/lane/one-sim/one-sim.sh wasm, into /home/claude/one-sim-work), or builds get the older file and the game says the real town is "an older build" and runs the old rules. A built copy is at /home/claude/one-sim-work-bridge/wasm/one-sim.wasm.
- Manager: project/test/harness.mjs line 12 was a syntax error (the comment swallowed the rest of the line); fixed here by moving the comment to the line's end.
- Manager: publish one-sim.wasm and ONE-SIM-CREDITS.md with the page (build.py lists them in publish-files.json); read the four notice files and add them to the credits before publishing. Write the new same_week record at the end.
- Police builder (police.js): when G.x.town.live, come for him only on st.arrest set by the town (it carries town: { end, until, hours }: use those hours); let DS Ellis come only on flags.forceEllis (the town's reason is in G.x.town.ellis), not on loudness; custody should not bill when the town charges.
- Story builder (scenes.js): 'town:hour' carries invite (Ada asks today) and ron (the envelope tonight) by the real week; Sheila's question fits the real week on Sunday.
- Every builder: a kind that damages a thing carries town: 'deed' and may carry thing: 'the chip shop window'; a robbery kind carries offence: 4 (the police file's own number), a killing 5.
