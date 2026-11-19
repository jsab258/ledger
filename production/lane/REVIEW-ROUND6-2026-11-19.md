# Review: lane round 6, the gate (19 November 2026)

A fresh, independent reviewer read commit 531c32a against its parent (tools/lane), DESIGN sections 19, 17 and 5 and
the experience rules named in the brief, and ran tests on a copy of the build in its own work folder (assets from
/home/claude/proto-assets). Nothing in the tree was changed except this report.

## Verdict: PASS WITH FIXES

The game code does what the changelog says. No regressions were found in saves, people's numbers or the frozen
town. The gate tool changes are sound and do not make the gate pass wrongly in any way found that matters. Two
things should be put right before the round is published, and one test run has to be finished on a quiet machine.
Nothing found is a must-fix fault in the game itself.

## What was run

- numbers PASS, same_week PASS (the seeded week matches round 5 part for part), fixes1 PASS, talk5 PASS.
- gate6: run three times. Every check that ran passed (37 at most: steering, lamp posts at 10, 20 and 32 mph, the
  parked car, six crashes in a row, the wedged cab both ways, boxed in, every door blocked, the clumsy minute).
  Each run then stopped with "Target crashed" at a different place (after 37, 17 and 8 checks), while another
  helper had several headless browsers open on the same machine (each graphics process near 500 MB). That fits the
  crash the round's own RESULTS.md reports with three browsers at once, and is most likely the machine, not the
  game. But it means the second half of gate6 (on foot, run-downs, the prompt, walking, the pad, the camera, save
  at the wheel, typing in a talk) was not seen to pass in this review.
- oldsave was not run (it needs an older build); RESULTS.md says a round 5 save loads.

## Claims checked against the code

- Eased key steering: yes. drive.js stepCar eases keys only (inp.kx) to full lock in 0.28 s and centres in 0.5 s,
  inside ER-DRIVE-02's 0.2 to 0.35 s and 0.4 to 0.9 s; a stick (inp.x) is used as it is. gate6 measured 0.283 s
  and 0.500 s.
- Solid lamp posts: yes, for the cab (postAt in solidAt and poseHit, the gaps between the three circles checked)
  and on foot (footSolid). The town's walks still use blocked() alone, so routines are untouched.
- Parked cars solid on foot: yes, footSolid and footClear use each car's box; a step is refused only when it goes
  deeper, so Tom can always walk out.
- Crash and run-down told the same frame: yes. sub() is called in the same stepCar call as act('crash') and
  act('run_down'), naming the thing (hitWhat) or the person as Tom knows them (tomName). The lines say a person is
  "hurt badly, and alive" or "bruised and shouting, no worse": a car hurts and never kills.
- Never stranded: yes. The cab never swings itself into something solid; a wedged cab may crawl the way out that
  is nearest; a boxed-in cab is worked clear after 0.8 s of trying; F with every door blocked puts Tom on clear
  ground; on foot, a second of pushing while inside something puts him on clear ground.
- Indoor and prop camera kept clear: yes. Indoors the camera swings back toward straight behind until its low arm
  misses the side walls and the new full-height partitions (TALL, filled for the office and boarding rooms); pitch
  indoors is held at 0.42 or more, so the arm length sum cannot go negative. On the street big props (1.3 m and
  over) now pull the camera in front.
- Pad plays the game: yes. Every button goes through onKey, the keyboard's road; sticks and triggers have dead
  zones from rules.js (new "pad" section); prompts show pad names while a pad is in use.
- Prompt names the person ahead: yes. fight.js target() scores by angle off his facing first, distance second,
  named people by 0.03 rad, back-turned people a little further, and holds a choice 0.2 s.
- Continue at the wheel: yes. saving.js already clears inCar on restore; loadWeek now moves Tom to exitPoint when
  he would stand inside the cab's body.
- Destructive buttons ask twice: yes. The pause panel and the title are rebuilt each time they open, so the
  "Sure?" state does not linger.

## Regressions looked for

- Save compatibility: nothing new is saved (the cab's eased steering, jam timer and the pad live outside the
  save), no saved field changed meaning. An old save with the cab on a post is handled by the wedged rule.
- People's numbers: rules.js has additions only (ladder target weights, tom, pad, driving); no existing value
  changed. same_week passes.
- Frozen town simulation: seeing, gossip, routines, police, custody, events and kinds untouched. map.js only adds
  exports; blocked() is unchanged.
- Content rule: the new text (crash, run-down, jam lines, the keys help) has no alcohol, gambling or children,
  and no death.

## Findings

### Must fix before publishing

None in the game or the gate tool.

### Should fix

1. tools/lane/prototype/PUBLISHED.json lines 3 and 196 (with "built", lines 8 to 9): the record now says round 6
   with round 6's hashes under the top version 1795032844-05a0, which is round 5's live page, and the same version
   is also listed under "previous" as round 5 (lines 92 to 93). The commit says round 6 is not yet published. Any
   check of the live page against this record would be misled. Leave the record at round 5 until the publish, or
   mark the top entry as built and not published.
2. test/gate6.mjs must be run alone to the end on a quiet machine before publishing; in this review its second
   half never ran (see above). Not a code fault, but the round's own claim rests on it.
3. tools/lane/gate/clumsy.py line 457: the new "A to D" guard compares size only, abs(to) against abs(press).
   It is meant to prove the cab ends turning the other way, so it should also check that the end has the same sign
   as press[-1]. Today a swing that ended part way, still turning the A way at over half lock, would pass this
   line (steer_change alone would not catch it if the swing reached 90 percent of a smaller change).

### Minor

4. tools/lane/gate/clumsy.py line 687: "everyone knocked down is told" matches the shown name as a substring. Two
   strangers with the same description ("A docker") are both satisfied by one line. Count lines per name, or
   require one line per person.
5. tools/lane/prototype/project/src/rules.js line 475: ladder.namedPreferredByMetres is no longer read (target()
   now uses targetNamedPreferredByRadians). A dead number in the one table; remove it or mark it retired.
6. tools/lane/prototype/project/src/player.js line 496: walking is eased for the stick and touch too, though the
   changelog (item 11) and ER-INPUT-01 say keys. Harmless at 0.12 s; say so or limit it to keys.
7. tools/lane/prototype/project/src/drive.js line 128 (workClear): the nearest clear ground is found by rings with
   no check that it is reachable, so a boxed-in cab could be put down on the far side of a wall or inside a yard.
   It says so on screen; worth a reachability check later.
8. rules.js line 1012: a crash counts above 5 m/s, about 11.2 mph, while ER-DRIVE-08 and gate6's message say
   "under 10 mph". The game is on the lenient side of the rule, which is allowed; the test text should say 11.
9. main.js line 793: Continue after a save at the wheel puts Tom at the door, not back at the wheel. ER-SAVE-02
   says Continue returns him where he left; standing at the door is a fair reading since a save holds no fare or
   traffic, but it should be named as a known shortfall.

## Gate tool changes in short

- Steering: holding the cab on a 5 m clear spot each frame measures the steering and nothing else. Sound.
- Pad: scenes finished first, each window tried again if a box opened, a window that never ran clear fails as
  "not reached". Sound; it cannot pass by default.
- Person-told rule: others knocked down must each be named on screen within 1.5 s of their own fall and none
  killed. The choice after a run-down is keyed by the rule alone, which matches the one KNOWN.json line; that line
  would also hide any other failure of the same rule until round 16, which is acceptable because the rule is the
  missing choice itself. In the round's final run nobody else went down, so the new rule had no case there;
  gate6 covers it with three people driven through.
