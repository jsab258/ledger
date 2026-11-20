# One-shot builder "foot": Tom on foot, the fight, the camera and the screen

Systems feel, foot and fightx. Branch os/foot (pushed as oneshot-foot). Last update 09:50 Swiss, 20 Nov 2026.

Stopped early at 09:50: the main row of 09:31 read the weekly allowance at 72% against the one-shot's ceiling of about 72.0% (line plus 35), so by the builders' rule this builder finished the piece in hand, committed, pushed and stopped. Everything below is as it stood then.

What was tested and how. The five rule pieces pass under Node: 74 cases (node test/pieces.mjs: hide_rules 31, foot_chase 7, foot_ground 13, fight_types 8, fight_defend 15). The feel numbers tool was run once on this build after the camera work: every band inside, 0 faults (cab camera 5.8 m behind and 1.8 m up, lens 62.5 degrees at rest and 67.0 at 30 mph, lag 0.10 s; fight camera 4.3 m with the other man and his feet in frame; fists unchanged). The in-game tests test/game/foot.mjs and test/game/fightx.mjs are written but have NOT run to the end: the shared machine killed the browser tab in every run (nine builders' browsers at once, the memory limit). The first nine checks of foot.mjs passed before a kill (the five manners, the call, the manners key, sitting and smoking, the second look). Nothing after that is proved in the browser. The existing tests gate6, melee3, melee4, layout, fixes1, watch2 and eyes were not re-run to the end either (gate6 ran twice: one tab kill, one run with a single failure in the three-people check, where a radio line pushed a name off the three subtitle places; not looked into). So every "built" below means built and compiling, with its rule proved in a piece where one is named; none is "passes its test" in the game yet.

## Faults already found

- Cab camera 8.5 m behind and 3.4 m up: fixed, measured 5.8 m and 1.8 m (feel numbers, inside).
- View 87 degrees, never widening: fixed at the wheel, 62.5 at rest to 67.0 at 30 mph (inside). On foot the lens is unchanged (his 86 degrees).
- Fight camera 5.2 m: fixed, measured 4.3 m (inside).
- Street camera: now 3.1 m back by his ruling (was 5.4); the wheel still scales it. Not judged by eye.
- Camera blocked at the bus stop, the ferry landing, a fare's drop and Laverack's awning: built, not tested. The line from Tom to the camera is now tested against the street's own solid shapes a few times a second (the same test the gate makes) and the camera comes in front of what it meets. Cost per test not measured in a rendered run.
- Tom reversing in one frame while his body takes 0.28 s: built, not measured again. On a reversal he swings round at 12.5 radians a second and steps off his new way only once his body is nearly on it.
- Pause menu not usable by keyboard or pad: built, not tested. Arrows move along the buttons of any panel and the title, Enter or E takes one, a pad's D-pad moves and A takes; a panel opens with its first button in hand.
- Door at Mickey's with no prompt off one exact spot: built, not tested. Every door gives its prompt within 2.6 m, the nearest door wins, and beside a person the door has E if he faces it (the talk moves to T), else T.
- A subtitle that never clears: built. Every subtitle also ends by the wall clock (12 s at most).
- Prompts over subtitles: built. The prompts ride above the subtitles' top edge.

## Parts

- 1.1.1 Walk, run and turn: built (turn fix; walking slowly on held Z at half pace). Thin: the footstep's reach is not yet halved (see Needs).
- 1.1.2 On-foot camera follow: built (rows by state, clear line). Not tested for clipping.
- 1.1.3 Doors, stairs and thresholds: built shallow (door prompts only).
- 1.1.4 Carrying: as round 6, untouched.
- 1.1.5 Hiding: built shallow. Piece hide_rules passes (ER-HIDE-01 rows at 4, 8, 18 and 35 m, still against moving). In the game only the light Tom counts at is joined up (still in a doorway 0.12 at night, moving through at the street's light); back turned, among people and behind things are in the piece and set as flags on G.tom, not yet read by the watchers.
- 1.1.7 Stopping and blending in: built shallow (B sits by a bench or shelter, leans by a wall, else lights a cigarette; a step ends it). The second look at a man standing about at night is built; "caught less" is the piece's (ER-STOP-01 rows).
- 1.1.8 Vaulting: built, not tested. Set places only: eight low wall pieces (Mickey's yard, the west alley, the alley's end, the back of Iveson's yard) and the bins and dustbins; a run at one carries him over in 0.8 s. Pursuers do not vault yet.
- 1.3.1 Blows and contact: as round 6 (feel numbers inside).
- 1.3.2 Reading and answering blows: built, not tested in the game. Guard as before; a blocked heavy blow now staggers a little, a swung weapon mostly breaks through; the slip (Space with A or D); the counter (a jab within 0.55 s of a slip or a block lands heavy); breath slows his blows and is heard. Piece fight_defend passes (ER-DEFEND-01, ER-FIGHT-07 by a duel model: reads 200 of 200, mashes 48 of 200).
- 1.3.3 Targeting without lock-on: as round 6.
- 1.3.4 The lower rungs: as round 6. The hard look and the shove are also street manners.
- 1.3.5 The street as a weapon: built shallow. Walls as before; the quay edge added (a man knocked or pushed in). Seven places not counted.
- 1.3.6 Things to hand and carried weapons: built. A weapon now comes out only on held semicolon (0.4 s), in a fight or out of one; a tap of R says so. The quiet blow from behind (J, no prompt, fist 20 s, cosh 30 s, the man keeps a shape at most; never a woman, anyone of sixty or the priest). melee4's one line that drew by a tap is brought up to date.
- 1.3.7 Condition without bars: as round 6, plus breath heard.
- 1.3.8 Odds, crowds and nerve: as round 6.
- 1.3.9 How a fight ends: built. 'fight:end' is told with how (backed off, ran, down, beaten, stepped in, police), the weapon tier and the men. People step in to a fist fight over 28 s with three men near; G.hooks.fightBrokenUp('police') ends one for the law.
- 1.3.11 Marks that last: built, not tested. Bruises and a cut lip three game days, a limp one (no running, slower walk); G.tom.marked is set for the watchers; one remark a day from somebody who sees him; the old doctor's door at 10 Quay Street halves the time left for six pounds. The doctor is a door, not a person yet.
- 1.3.12 Fighter types: built. Piece fight_types passes (ER-TYPES-01). Boxer, brawler, big man, and a knife man only where authored.
- 1.4.1 Reading watchers, 1.4.2 Light and dark as cover: as round 6, untouched.
- 1.4.3 Hearing his own noise: as round 6, untouched.
- 1.4.6 Seeing assist: built shallow (a plain ring over people in G.watch who have noticed him; off by default).
- 1.4.7 Street manners: built; the first checks passed in the browser (ER-MANNER-01 for all five, the call stopping a walker 2 s, the M key with digits). No pad stick pick.
- 1.4.8 Drawing a watcher away: built, not tested. O throws a stone 12 m the way the camera looks, or rattles a bin in reach; heads inside the reach turn and keep "a noise"; 'noise' is told to other systems.
- 1.5.1 Fleeing on foot: as round 6 (police.js is the law builder's).
- 1.5.2 Pursuing on foot: built, not tested in the game. G.hooks.runner(P, why) sets anybody running at 95% of Tom's run; lost after 7 s unseen or 70 m, caught within 1 m from behind, then the choice (let go, a word, front him up). Piece foot_chase passes (ER-PURSUE-01, 02: 50 direct chases all caught, 50 lagging all lost, longest 46 s).
- 1.5.4 Pursuers: not built beyond round 6 (they do not vault; the constable's look round the last place is the law builder's).
- 1.6.8 Using the world: built shallow (new prompts for sitting, throwing in, the doctor, a man down).
- 1.6.12 The torch as a held thing: built. I toggles it when G.tom.items.torch or G.tom.torch is set; G.tom.torchOn is read by the light he counts at (0.7). No beam is drawn.
- 2.2.6 Ground rules and trespass: built, not tested in the game. Piece foot_ground passes (ER-GROUND-01). Iveson's yard is open by hours; other systems' places with a label and a groundMetres count; warned, warned again, then a 'trespass' act and the event 'trespass'.
- 4.2.4 The water's edge: built. Tom cannot walk in (as round 6); a carried weapon or load can be thrown in and is gone (act threw_in, event 'thrown'); a man put in climbs out after 14 s, soaked, alive (ER-WATER-02 by construction, not tested). Tom being put in by others is not built.
- 6.1.1 The prompt, 6.1.2 Subtitles: built (see the faults above).
- 6.1.4 Light and sound cues: as round 6, untouched.
- 6.1.5 Knowing the time: built; not tested. No screen clock: the docket's time shows only for 2 s after N (the watch, with a line of words), beside the market clock, the Harbour Board or in Mickey's, and while passing the time. The chapel bell strikes the hours from seven to nine at night within 260 m.
- 6.4 Menus: built (keys and pad), not tested.
- 6.6 Controls: built shallow. New keys: Z walk slowly, M manners, B stop, N watch, O noise, I torch, semicolon held weapon, Space with a direction slip, G in a fight with nothing to hand grabs the man, then J push, G disarm, X let go. None of the new verbs is on the pad.
- 6.7 Talk screen: untouched.
- 7.10 Difficulty as assists, 8.4.1 Sound shown: built shallow. Five settings, all off by default: seeing, slower fights (tell a quarter longer, one man swinging), driving help and longer walks (set only: the cars and law builders read G.settings.assistDrive and G.settings.assistLongWalk), sound shown (a short word at the right edge for loud noises, his own and the game's sounds). "Show the first hints again" tells other systems by the event 'hints:again'.

## Known faults

- No in-game test of this builder has run to the end (see the top). First thing for the next run: `tools/lane/prototype/oneshot_dev.py test game/foot game/fightx gate6 melee3 melee4 layout fixes1 watch2 eyes` on a quiet machine, then the feel numbers tool.
- test/harness.mjs was broken by the port shift's comment (it swallowed the window size); mended on this branch. Every builder's browser tests fail to start without that one-line fix.
- The street camera at 3.1 m is a large change of view; feet in frame is by arithmetic only.
- The camera's clear-line test may cost frame time on a slow machine; LEDGER.game.feel.camLine().lastMs reads it.
- R no longer draws a weapon; the "How the town watches, and the keys" page still says nothing of the new keys.
- The doctor's door and the vault places were placed from the map's numbers, not by eye.

## Needs from others

- Manager: keep the harness fix (test/harness.mjs line 12) when merging.
- Bridge (seeing.js): read G.tom.slow (halve the walking footstep's reach, A1), G.tom.glanceSecs (the glance among people), G.tom.marked (a give-away, A21), G.tom.belongs (no second look), and a back turned to the watcher (no face). The piece hide_rules has the rule and the rows.
- Spine (main.js, design_notes.js, scenes.js): the pad's buttons for the new verbs and the D-pad in panels (ui.menuKey takes 'ArrowUp', 'ArrowDown' and 'PadA'); the keys page; the to-do that stays "Find Mickey's" under the blue sign; Darren's "I owe the book".
- Law (police.js): G.tom.lastVault ({x, z, t}) for a pursuer to lose time at a vault place; G.hooks.fightBrokenUp('police') when an officer reaches a fight; the events 'trespass', 'noise', 'chase:end', 'thrown'.
- Cars: sounds 'horn', 'glass' and 'force' now exist in audio.js for G.hooks.sfx.
- Jobs: G.tom.torchOn; the event 'searched' ({P, E, found}) when a man down is searched; G.hooks.runner(P, why) for a runner.
