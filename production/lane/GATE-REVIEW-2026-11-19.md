# Review of the two publish gates (fresh reviewer, 19 Nov 2026)

Scope: tools/lane/gate (loop prototype, Python) and tools/lane/driving-gate (driving study, Node). I changed no repository files.
What I ran: both unit test sets, one gate scenario again (`--only indoors`), and three small probe scripts of my own against /root/gate-dist, kept in the scratchpad. The driving study's page is not in the repository, so the driving gate is judged from its own code only.

## Verdict in three lines

- Every failure in the final loop report is a real fault in the game. But two of the "told on screen" checks are measured so badly that they would still fail after the game is fixed, or pass by luck.
- At least one pass in the final report is false. Camera clear shows 0 of 10 failed only because the run reached 2 rooms instead of 9. Run alone, the same scenario finds a camera fault at Regent House.
- Of the owner's two complaints, the driving gate catches the stranded car but passed the keyboard steering. The loop gate catches the keyboard snap when a key is pressed, but not when it is let go. Neither gate can test a pole hit in the loop prototype, because its lamp posts are not solid.

## 1. Final loop report (/root/gate-final/report.json): fault in the game, or in the gate?

| Failure | Verdict | Evidence |
|---|---|---|
| damage told, 4 of 4 | **Real fault, badly measured.** The game never says the car is damaged. A crash only plays a sound and shakes the screen (drive.js 111-117). The only words come from the Ledger's "Noted" line, and only when someone saw the crash ("…may have seen that you put the cab into something", kinds.js 294-298). That line is often merged into "Noted in the Ledger: 11 things" (ui.js 150-152). My probe got exactly that. | The gate reads the words only after the whole 12 s hold of W, not within 1.5 s of the hit (clumsy.py 275, 290-293). Its comment saying the frames after the hit are re-run is wrong. Its word list has no match for the game's own phrasing (invariants.py 43). |
| keyboard steering eased | **Real.** The key value goes straight into the turn rate, with no ramp (drive.js 85-97; player.js 391-395). In my probe the turn rate went from 0 to 1.56 rad/s in one frame when D went down, and from 1.68 back to 0 in one frame when it came up. | The check sees only the press. Its "first frame" is really the second frame (clumsy.py 319-322). |
| a person hit: told on screen | **Real.** There is no direct message. The "knows that you knocked … down" line waits behind any subtitle (ui.js 150, 166) and is merged with other waiting notes. In my probe it had not appeared 3 s after the hit. | Measured on the page's text, which only updates when a frame is drawn (see Must fix 2). |
| a person hit: choice offered | **Real.** After a run-down nothing offers help or driving off. The only prompt is "Get out" (drive.js 127-146 sets the person down and nothing more; there is no help prompt anywhere in player.js). | The check is fair, but it looks only from inside the cab. |
| a pad moves Tom / drives the cab | **Real, and by design.** The game only lets a pad work the Ledger (main.js 400-438, "A pad drives the Ledger only"). Nothing reads the sticks or triggers for movement. | The check is fair. |

Passes that could be false:

- **camera clear 0/10: false pass.** Earlier run out6 and my rerun of `--only indoors` both fail at Regent House: the ray to the camera is blocked 0.72 m from Tom (picture: Tom half hidden by the near wall). The final run took the indoors scenario after midnight on the game clock, so 14 doors were "closed" and only Mickey's and Regent House were entered. Compare the rooms in the final report (2) with out6 and my rerun (8 and 9). The final run only wrote notes about this and still passed.
- **never stuck (cab after a hit) 12/12: true, but empty.** The cab cannot be stranded at all: each damage point takes off 5% of top speed, up to 4 points (rules.js 970-981). Crashes ran at only 17 to 28 mph, into walls and props only, never into poles, traffic or parked cars.
- **a person hit is hurt, never killed: true for one speed.** One person was hit at about 9 m/s. In my probe the same set-up also knocked down three other people at the rank on the way in ("the lad with the pager", "the day driver", "the big man"). The gate neither saw nor reported them. They stay down for the rest of the run.
- **out of the cab onto open ground: weak.** It was tested only where the cab stood in open road. The fallback exit point (drive.js 179) is never checked, so a cab wedged against walls is never tried. The F presses really do switch in and out; my probe confirmed it.
- **pause and resume, save then load: weak.** Pause checks only the pause flag, not that the world stops. Save and load compare three numbers, and use the loading function directly instead of Continue from the title (clumsy.py 399-408).
- **no pause nothing holds: almost cannot fail in this set-up.** The detector only runs in the drawing loop, after 3 s of real time, and unpauses the game itself (main.js 776-786). The gate steps the game far faster than real time.

## 2. The owner's two complaints

- **Stranded by one pole hit.**
  - Driving gate: caught (DRIVING-ROUND4-FINDINGS check 1).
  - Loop gate: cannot test it. The lamp posts are drawn (render/town.js 809-811) but are not in the collision map (map.js 800-816). `isBlocked` is false at all four lamp posts I tried. The gate picks its crash targets with that same collision function (clumsy.py 261-269), so it never aims at a pole, and it cannot notice that a pole is a ghost. If a later build makes poles solid and they strand the cab, the gate still will not aim at them.
- **Jerky keyboard steering.**
  - Driving gate: missed (PASS). Its smoothness test only measures the first move away from straight (lib.js 76-89). Letting go and switching from A to D are never judged, yet the findings themselves describe a swing on letting go.
  - Loop gate: caught on the press only. A ramp of two frames would pass its "under half the full rate" rule.

Kinds of fault both gates miss:

- Anything that only shows in real time. Both gates step the game at a fixed rate, so uneven frame pacing and hitches are never seen. The loop game's camera only moves in the drawing loop (main.js 760), so camera jerk while driving is never measured. That is a likely cause of steering that "feels jerky".
- Mismatch between what is drawn and what is solid (ghost poles, invisible walls). Both gates use the game's own collision to judge the game.
- Words: only text is read, never sound. Overlapping or unreadable text is never checked.
- Driving at traffic and parked cars. A crash at the car's top speed (loop prototype: about 32 mph).
- The aftermath of a run-down (police, gossip, the person getting up). Hits on more than one person.
- How the player gets places: teleports skip the walk and the drive, and the cab keys are given by set-up.

## 3. Ranked findings

### Must fix

1. **Results depend on what ran before (loop gate).** All scenarios share one game session (clumsy.py 549-564). The game clock moves on, so the indoors coverage fell from 9 rooms to 2 and a real camera fault went unreported. Other state also carries over:
   - car damage is never reset;
   - people knocked down stay down;
   - `clear()` answers story scenes with the first choice (clumsy.py 147-149).

   Fix: start each scenario from a fixed save at a fixed hour, or a fresh page.
2. **The "told on screen" checks measure the wrong thing (loop gate).**
   - The page's words only refresh when a frame is drawn (main.js 755-758, `hud`). The gate runs the game inside a single script call with no drawing in between (clumsy.py 111-116). My probe saw about 47 ms of real time across a whole 1.5 s check window, so the text read is mostly stale.
   - The damage check also starts too late (item 1 in the table above).
   - The word lists do not match the game's own wording.

   Fix: read the game's message lists (ui.subs, ui.notes, news) at each step, or draw the HUD each step. Start the clock at the hit frame. Match on the game's event kinds, not English words.
3. **A scenario that tests nothing still passes.**
   - Loop gate: no hit found, no room entered, or nobody knocked down all become notes only (clumsy.py 285, 465, 526).
   - Driving gate: the pedestrian rule never calls `fail` (gate.js 220-232). The whole-run stranded count is reported but never fails (gate.js 287-288). That is why the findings show "NOT REACHED".

   Fix: each rule needs a minimum number of real checks, otherwise it fails as "not reached".
4. **Steering smoothness is judged on the press only (both gates).** Measure the press, the release and the change from A to D. Pass only when the move takes at least about 0.1 s from 10% to 90% and no single frame changes it by more than a set step. Hold speed steady while measuring.
5. **The gates judge the game with the game's own collision.** Crash targets come from `isBlocked` (loop gate) and from the camera's collision world (driving gate, gate.js 101-122, driver.js 246 and 259). So ghost poles pass, and in the driving gate "camera clear" is close to always true. Fix: aim at named prop types (lamp, bollard, parked car, traffic). Test the drawn solid meshes, not only the collision map.

### Should fix

6. **Damage carries over between crashes (clumsy.py 271).** The car reaches the cap of 4 after four crashes, so the other 8 crashes could never be checked for "damage told", and top speed drops 20%.
7. **The camera test hangs on one distance (clumsy.py 182; invariants.py 65-71).** It ignores anything within 0.7 m on foot or 2.7 m in the cab. The Regent House hits were at 0.72 to 0.73 m, so the verdict flips on 3 cm. A wall within 2.7 m behind the cab is never seen. Ignore Tom's and the cab's own meshes by name, test several points on the body, and also test while driving.
8. **gate.py can be fooled.**
   - GATE.json says `"pass": true` even with no hands-on write-up (gate.py 85-94, 104).
   - `"known" not in line` skips a line that says "unknown" (gate.py 55).
   - A line "No blockers" is counted as a blocker.
   - MAJOR faults never block.
   - KNOWN.json is keyed by rule name, so one accepted camera fault would hide every future camera fault.
9. **Driving gate, `recover()` sets up the reset test itself (gate.js 84-85; driver.js 255-257).** `__place` repairs the car and moves it, then the gate puts back a few damage fields by hand and forces power to 0. The result "Backspace leaves it dead" is partly made by the gate. Test Backspace on the car as the crash left it.
10. **Driving gate rebuilds the page's frame loop itself (driver.js 231-241).** It sets `spin`, `foot`, `up` and `down` on its own. Steering is measured on that copy, not on the page's real loop.
11. **Driving gate counts any message as "damage told" (gate.js 160).** It looks back 6 s, so an older message can count too. It should look for damage words, after the hit only.

### Minor

12. The note reads `LEDGER.rules.DRIVING`, which does not exist (the game has `rules.driving`), so the report says "top speed None" (clumsy.py 303).
13. Button spam taps W, A, S and D as a press and release with no game step in between, so they never move Tom (clumsy.py 357).
14. The corner spots are found by a grid search over the whole map, so some may be places no player can reach.
15. The hands-on prompt has a helper send key presses. CLAUDE.md says "Helpers never send clicks or keys". The ruling it points to (29 and 30 Oct) is about computer use on the owner's PC, so a headless browser is probably fine, but someone should confirm it.
16. Game wording found on the way: "the day driver knows that you knocked the day driver down with the cab".

## 4. Unit tests

Both sets pass: Python 11 tests, Node 8 tests. They only test the small pure helpers on made-up numbers, and none would have caught the problems above:

- timing windows and stale text;
- coverage minimums;
- state carrying between scenarios;
- word lists against the game's real strings;
- release and reversal in steering;
- `recover()` and `steerCheck()`.

test_invariants.py 251 treats "Crunch." as a message, yet the real damage check would reject that word. Worth adding:

- a test that builds each rule's words from kinds.js and talk_lines.js and checks they match;
- a series that presses, releases and reverses, for the steering helpers;
- a judge test with "unknown" and "No blockers" lines;
- a test that fails a scenario which tested nothing.

## 5. New faults in the game found during the review (not in any report)

- Lamp posts are drawn but not solid; the cab and Tom pass through them (render/town.js 809-811 against map.js 800-816).
- The camera hides Tom behind a wall in Regent House (found by out6 and by my rerun; missing from the final run).
- Steering also snaps when the key is let go (turn rate to 0 in one frame).
- Driving into a person at the rank also knocked down three people near them; nothing on screen said so within 3 s.
