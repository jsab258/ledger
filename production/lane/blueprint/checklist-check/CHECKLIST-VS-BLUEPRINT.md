# The 957-item checklist against the blueprint

23 November 2026, checklist check (claude-opus-5-5 leading, four Sonnet helpers matching by section, a fresh Opus checker on 60 rows). Sources: production/research/feature-coverage/MASTER-CHECKLIST.md (23 Sep) on wip; the blueprint (BLUEPRINT.md and chapters 01 to 10, version 1 after keeper run 3) on lane-2026-11; canon.md and RULINGS.md on wip.

## Summary

All 957 items are still there, each now checked: 560 covered (194 only partly, the note says what is short), 80 out by canon, his rulings or an OUT part, 132 Unreal-phase looks, engine or performance items (35 with no part yet), 185 missing (29 need an in-or-out decision first, such as mounts, fast travel, achievements; 14 already among BLUEPRINT-11's gaps).

By blueprint group (covered / out / Unreal / missing): 01 Hands 152/26/15/57; 02 Town 80/6/1/13; 03 Story 40/1/2/9; 04 Place 21/0/13/2; 05 Looks and sound 44/2/70/22; 06 Interface 45/5/0/27; 07 Shape 65/27/1/18; 08 Technical 82/4/27/20; 09 Machinery 24/2/3/5; 10 Shipping 7/7/0/12.

The twenty missing a player would notice most:
1. Sound direction (A28.01, A28.02, A28.15)
2. Walls muffle, open doors carry (A28.06, A28.07)
3. People popping in view (A13.25, A25.16)
4. Fleeing people running away from the danger (A13.18)
5. Walking off mid-talk; a fight breaking in (A31.09, A31.10)
6. Saving shown and explained (A39.01, A39.03)
7. Saves never overwritten unasked (A39.08, A39.09)
8. Saying what was picked up (A36.02)
9. Progress and cancel for searches and holds (A11.10, A11.11, A03.10)
10. Camera close in rooms, on stairs (A05.09, A05.11)
11. Above and below by ear; where the ears sit (A28.12, A28.13)
12. Recoil, rate of fire, empty click (A19.04, A19.09, A19.11)
13. Readable recovery after a blow (A18.05)
14. Loose objects with weight (A12.05 to A12.08)
15. Fallen speakers' lines; talking over each other (A30.13, A13.12)
16. Repeated or trailing sounds (A29.15 to A29.17)
17. Menu-closing clicks acting in play (A03.15, A03.16, A40.04)
18. Accidental scene skip; facing after scenes (A32.08, A32.10, A05.21)
19. Pursuers replanning, not firing into walls (A14.10, A14.14)
20. The camera fighting his own mouse or stick (A05.13)

## Notes for the keeper

Fold the missing items in as parts or gaps. Tom's position on the paper map (A35.02, A35.03) wants an in-or-out decision before it is a gap. OUT-08 reads wider than its ruling (no jump only) for crouch, swimming and climbing; one ruling line would settle the six mount items (A27.01 to A27.06) as out. The fresh checker agreed with 56 of 60 sampled rows; its systematic corrections are applied once and listed in CHECK-SAMPLE.md. The groups are assigned by checklist section, so a covered item may cite parts from another chapter.

## Every item

Verdicts: covered (parts named), out (the line that excludes it), unreal (Unreal phase; parts or none), missing (what the blueprint would need; "Decide in or out" where a ruling is wanted first). Gap: the BLUEPRINT-11 gap number (G-numbering in gaps-index.txt) where already listed.

| id | feature | verdict | parts | gap | note |
|---|---|---|---|---|---|
| A01.01 | A working launch from the installed shortcut or platform library | unreal | 8.5 |  | Unreal build starts from its shortcut; the browser build is a page |
| A01.02 | A visible response while the application starts | unreal | 8.5 8.1.3 |  | progress shown while shaders and the street prepare |
| A01.03 | Startup that does not require unrelated windows or manual commands | unreal | 8.5 |  | starts from one shortcut with talk program and voice inside |
| A01.04 | Clear identification of the game being launched | covered | 6.4 8.5 |  | partly: title screen with New game, Continue and Quit; no window title or splash rule |
| A01.05 | A sensible initial display resolution | unreal | 8.5 8.3.1 |  | opens at a sensible size; first launch finds a smooth picture; Unreal only |
| A01.06 | Startup on the intended monitor | unreal | 8.3.1 8.5 |  | none names which monitor it opens on; Unreal build needs a monitor choice and a test |
| A01.07 | Initial sound at a reasonable volume | covered | AX-04 5.5.7 |  | partly: five volume sliders, but no first-launch level is set |
| A01.08 | Access to language selection before language-dependent instructions | out | OUT-10 8.9 |  | OUT-10 English only, no localisation |
| A01.09 | Access to subtitles before the opening dialogue | covered | AX-02 6.1.2 |  | subtitles on by default and offered on the first menu before any sound |
| A01.10 | Access to essential accessibility settings before gameplay | covered | AX-02 AX-04 AX-09 AX-06 |  | assists offered on the first menu; settings reachable before play |
| A01.11 | A readable explanation of required account or permission requests | covered | 10.11 8.2.1 |  | partly: the AI notice and crash-report consent are plain screens; no account beyond Steam is asked |
| A01.12 | Offline access to offline content where supported | covered | 8.6.1 10.11 |  | offline mode plays the whole first hour on written lines |
| A01.13 | A usable response to unavailable online services | covered | 8.6.1 |  | offline or slow, written street carries on with an in-character brush-off |
| A01.14 | Progress information during lengthy initial preparation | unreal | 8.5 8.1.3 |  | progress while shaders and the street prepare |
| A01.15 | An explanation when required content is still installing | missing |  | G285 | Decide in or out: no rule for a message while the store is still installing or updating content |
| A01.16 | An actionable error when the game cannot start | missing |  | G285 | Decide in or out: no start-failure message saying what failed and what to do; 8.2.1 covers only the crash report after a crash |
| A01.17 | Remembered first-run choices | covered | AX-06 8.5 |  | partly: every setting is remembered and survives an update; first-run choices (presets, brightness, scale) are not named as remembered |
| A01.18 | Skippable repeated introductory logos where permitted | missing |  |  | Decide in or out: no start logos are named, so no skip rule exists; needs one line if the store or engine adds any |
| A02.01 | A clear distinction between starting, continuing and loading | covered | 6.4 7.8 |  | title menu offers New game, Continue and Quit; save and load is its own screen |
| A02.02 | "Continue" that selects the appropriate latest progress | covered | 6.4 AX-07 8.5 |  | partly: Continue returns him as saved; no rule says which of manual and autosave counts as latest |
| A02.03 | Protection against replacing an existing playthrough with "New Game" | covered | 6.4 AX-07 7.8 |  | partly: eight manual slots and three autosaves; no explicit warning when New game would push out autosaves |
| A02.04 | A visible selected menu item | covered | AX-06 |  | focused item always visible |
| A02.05 | Menu navigation in a predictable order | covered | AX-06 6.4 |  | partly: menu walk logs focus on every screen; order itself is not specified |
| A02.06 | Consistent confirm and back controls | covered | AX-06 6.6 |  | partly: Back always goes one level up; confirm is not named as one fixed control |
| A02.07 | A reliable way back from every screen | covered | AX-06 |  | Back goes one level up on every screen and never quits |
| A02.08 | Mouse support for visible buttons on PC | covered | AX-06 6.4 |  | menu walk by pad, keys and mouse on every screen |
| A02.09 | Clickable areas that match their visible buttons | covered | AX-06 |  | partly: large stationary targets; hit area matching the drawn button is not stated |
| A02.10 | Scroll-wheel support for scrolling lists | missing |  |  | needs a line that the save list, settings and Ledger scroll with the wheel, plus a menu-walk check |
| A02.11 | Controller navigation that reaches every setting | covered | AX-06 6.6 | G241 | partly: menu walk by pad is a test; the pad layout is not yet written |
| A02.12 | Selection that remains visible while a list scrolls | covered | AX-06 |  | partly: focus always visible; scrolling lists not named |
| A02.13 | Useful explanations for disabled options | missing |  | G280 | needs a rule that an unavailable option says why (for example Continue with no save) |
| A02.14 | Confirmation before destructive actions | covered | 6.4 AX-06 6.7 |  | partly: nothing destructive one press from Resume, and irreversible talk choices ask twice; no confirm named for deleting a save or quitting |
| A02.15 | Dialogues that capture input without activating buttons behind them | missing |  |  | needs a rule that a pop-up dialogue takes all input and nothing behind it fires, with a menu-walk check |
| A02.16 | Menus that remember position when returning from a detail screen | missing |  |  | needs a rule that a menu returns to the same item after a detail screen; AX-06 remembers settings, not position |
| A02.17 | Text entry that works with the current device | covered | 6.7 3.6.8 8.6.1 |  | partly: talk typing works by keyboard or suggested lines by pad; no menu text entry such as save names |
| A02.18 | An on-screen keyboard when physical typing is unavailable | covered | 3.6.8 8.6.1 3.6.6 |  | on a pad suggested lines show at once with an on-screen keyboard |
| A02.19 | Loading or busy feedback after an accepted selection | covered | 8.5 6.4 8.11.1 |  | partly: progress shown at start-up; budget for new game to control; no busy sign for other accepted choices such as load |
| A02.20 | Protection against repeated clicks starting the same operation twice | missing |  |  | needs a rule and test that a double click or press cannot start load, save or new game twice |
| A03.01 | Movement and actions that respond promptly to input | covered | 1.1.1 6.6 |  | every action answers within 100 ms |
| A03.02 | Camera movement that responds promptly | covered | 1.1.1 1.1.2 5.8.1 | G7 | partly: mouse look never jumps and blends take 1 s or less; follow lag has no number |
| A03.03 | Consistent controls across equivalent situations | covered | 6.6 1.6.8 6.1.1 |  | one use key for every usable thing; fixed keys list |
| A03.04 | Correct button prompts for the connected device | covered | 6.6 | G241 | partly: prompts follow the device last used; pad layout is not written |
| A03.05 | Prompts that update after rebinding | covered | 6.6 AX-05 |  | partly: every action can be rebound; prompts showing the new key is not stated |
| A03.06 | Switching between supported mouse, keyboard and controller input | covered | 6.6 |  | keyboard with mouse and pad each reach every verb; prompts follow the last device used |
| A03.07 | Simultaneous input where useful, such as controller movement with gyro aiming | missing |  |  | Decide in or out: gyro or other simultaneous pad aiming is not mentioned; aiming is by mouse or stick (RT-10) |
| A03.08 | No duplicate action from one physical button press | covered | 6.1.1 |  | partly: use-key misfire test (500 presses, zero); no general one-press-one-action check |
| A03.09 | Correct distinction between pressing, holding and releasing | covered | 6.6 AX-05 |  | every hold has a toggle and a hold-becomes-tap switch; held press used for pocket and gun draw |
| A03.10 | Clear feedback when an action requires holding | missing |  |  | needs a rule that a hold shows progress (pocket lift, gun draw, search) and a check that it does |
| A03.11 | Reasonable tolerance for slightly early action presses | covered | 6.6 1.1.1 |  | a press 100 ms early still counts |
| A03.12 | Predictable handling of conflicting simultaneous inputs | missing |  |  | needs a rule for opposite or clashing inputs (both strafe keys, keys plus stick) and a test |
| A03.13 | Movement that stops when the movement input stops | covered | 1.1.1 |  | partly: starting and stopping have a short ease; stop on release is not tested as such |
| A03.14 | No stuck movement after opening a menu or changing focus | covered | AX-10 |  | no stuck key after losing focus (100 alt-tabs); menu-open case not named |
| A03.15 | No attack caused by the same click that dismisses a menu | missing |  |  | needs a rule and test that the click or press that closes a menu does nothing in play |
| A03.16 | No unexpected action from an input held through a loading screen | missing |  |  | needs a rule that input held through loading or the ferry shot does nothing on arrival |
| A03.17 | Analogue movement speed on supported sticks | covered | 1.1.1 |  | partly: a light stick touch walks slowly; fully analogue speed is not stated for foot |
| A03.18 | Equal intended movement speed in straight and diagonal directions | missing |  |  | needs a line and test that diagonal speed equals straight speed on keys and stick |
| A03.19 | Sensible controller dead zones | missing |  |  | needs pad dead-zone defaults and a setting; AX-05 has sensitivity and invert only |
| A03.20 | Predictable mouse movement without unwanted acceleration | missing |  |  | needs a line that mouse look has no acceleration (raw input) in AX-05 |
| A03.21 | A usable response to controller disconnection | missing |  |  | needs a rule for pad unplugged mid-play (pause, prompt change) and a test |
| A03.22 | Safe reconnection without restarting the game | missing |  |  | needs a rule that a pad reconnects without restart and a test |
| A03.23 | Input handling independent of frame rate | covered | FIT-G4 8.11.2 1.1.1 |  | partly: speeds never depend on frame rate and logic runs on a fixed step; input sampling is not named |
| A03.24 | Clear control ownership when several controllers are connected | missing |  |  | needs a rule for which pad drives when two are connected (single player) |
| A04.01 | An unmistakable transition from watching to controlling | covered | 7.1 5.8.2 |  | ferry shot of 20 s then control at 0:20; skippable |
| A04.02 | A starting camera aimed at something useful | covered | 7.1 1.1.2 |  | control starts on Quay Street with the camera at the Between height looking down the street |
| A04.03 | A safe opportunity to test movement | covered | 7.1 1.1.3 |  | partly: control within 1.5 min and never stuck; no named safe space for trying moves |
| A04.04 | A safe opportunity to test the camera | covered | 7.1 1.1.2 6.5 |  | partly: control at 0:20 and a hint after 4 s standing still; no camera hint named |
| A04.05 | A clear initial purpose | covered | 7.1 6.2.3 |  | Sheila walk-round at 1:45, first verb by 3 min, Open lists what next and where |
| A04.06 | A discoverable first destination or activity | covered | 7.1 6.9 6.2.3 |  | every go-to step names its place by landmark; newcomer reaches a place in 3 min |
| A04.07 | Instructions shown when their actions become relevant | covered | 6.5 6.1.1 |  | hints fire the first time they can mean something; prompt names what is ahead |
| A04.08 | Instructions using the player's actual bindings | covered | 6.5 6.6 |  | partly: prompts follow the last device; rebound keys not stated |
| A04.09 | Time to read an instruction before it disappears | covered | 6.5 | G240 | partly: never two hints within 12 s; on-screen time of one hint is not set |
| A04.10 | Confirmation that a tutorial action succeeded | missing |  | G240 | needs a rule that a taught action is confirmed when done, with a test |
| A04.11 | A way to recover instructions dismissed accidentally | covered | 6.5 |  | "hints again" brings them back from the Ledger |
| A04.12 | Tutorials that cope with an action performed early | covered | 6.5 |  | partly: a hint fires only when it can mean something; an action done early is not named |
| A04.13 | Tutorials that stop repeating after understanding is demonstrated | covered | 6.5 |  | each hint fires once |
| A04.14 | A way to revisit controls and basic rules | covered | 6.5 6.6 |  | partly: hints again from the Ledger; no controls page named |
| A04.15 | A way to skip familiar instruction without breaking progression | covered | 6.5 |  | partly: hints come on need or hesitation only, nothing forced; no skip switch |
| A04.16 | An opening that permits ordinary experimentation without trapping the player | covered | 7.1 1.1.3 7.9 |  | never stuck within 5 s, no game over, hints only on hesitation |
| A05.01 | Free horizontal and vertical looking within the intended camera model | covered | 1.1.2 5.8.1 |  | mouse look free; camera arm by state |
| A05.02 | A useful default viewing distance in third person | covered | 1.1.2 5.8.1 |  | 3.1 m back on foot, 3.5 to 5.0 m in a fight, 5.8 m in a car |
| A05.03 | A useful default field of view | covered | AX-03 8.3.1 5.8.1 |  | 86 degrees default, setting 75 to 100 |
| A05.04 | Camera framing that keeps the controlled character readable | covered | 1.1.2 5.8.1 |  | feet always in frame; both men's feet in 90% of fight frames |
| A05.05 | Camera movement that does not lag so much that control feels detached | covered | 1.1.2 5.8.1 | G7 | partly: blends 1 s or less; follow lag has no number |
| A05.06 | Camera collision that prevents seeing through walls | covered | 1.1.2 5.8.1 |  | never ends inside a wall, body, car or lamp post; clip detector soak |
| A05.07 | Camera recovery after an obstruction clears | covered | 1.1.2 5.8.1 |  | partly: blends in a second or less; recovery after an obstruction is not named |
| A05.08 | Smooth handling of poles, foliage and other small obstructions | covered | 1.1.2 | G16 | comes in front of thin things; lamp posts named |
| A05.09 | Character fading or another solution when the camera gets too close | missing |  |  | 1.1.2 keeps the camera out of walls and bodies, but nothing fades or hides Tom when the camera is close in rooms; needs that rule |
| A05.10 | A usable view in cramped interiors | covered | 1.1.2 5.8.1 | G228 | closer camera in rooms and talk; screenshots in tight rooms |
| A05.11 | A usable view while ascending and descending stairs | missing |  |  | 1.1.3 has stairs walked without snagging; the camera view going up and down stairs is unstated; needs a stairs camera check |
| A05.12 | A usable view while climbing or hanging | out | OUT-08 |  | OUT-08 no climbing (OUT-08 reads wider than the ruling, which says only no jump) |
| A05.13 | Camera behaviour that does not repeatedly fight manual input | missing |  |  | needs a rule that the camera never overrides mouse or stick input, plus a test |
| A05.14 | Predictable recentering, if provided | missing |  |  | Decide in or out: no recentre key or behind-the-back rule is named |
| A05.15 | Smooth transitions between exploration, aiming and conversation | covered | 5.8.1 5.8.3 |  | blends of 1 s or less between street, run, room, talk, fight and car rows |
| A05.16 | Appropriate framing when crouching or going prone | out | OUT-08 |  | OUT-08 no crouch, no prone (OUT-08 reads wider than the ruling, which says only no jump) |
| A05.17 | Aiming that follows the intended sightline | covered | RT-10 |  | partly: gun aim row with no crosshair; sightline and camera offset are not specified |
| A05.18 | Shoulder switching where the aiming design requires it | missing |  |  | Decide in or out: shoulder switching is not mentioned in the gun aim row |
| A05.19 | Lock-on that selects a plausible target, if present | covered | 1.3.3 |  | the design chooses no lock-on: the man pointed at is the man hit, tested in 1.3.3 |
| A05.20 | Lock-on that releases sensibly when a target dies or disappears | covered | 1.3.3 |  | the design chooses no lock-on: the man pointed at is the man hit, tested in 1.3.3 |
| A05.21 | Camera recovery after a cutscene without disorienting rotation | missing |  |  | needs a rule for where the camera and heading land after the ferry shot or any scene |
| A05.22 | Camera shake that does not hide essential information | covered | AX-03 5.8.1 |  | partly: shake obeys Reduce motion and has its own switch; no rule that shake never hides information |
| A05.23 | Stable horizon and manageable camera motion | covered | AX-03 |  | partly: each motion effect has a switch; no horizon or roll rule outside photo mode |
| A05.24 | A sensible relationship between camera direction and movement after a camera cut | missing |  |  | needs a rule that move keys keep a sensible heading after a camera cut or blend |
| A06.01 | Walking, jogging and running appropriate to the control scheme | covered | 1.1.1 FIT-G4 |  | walk 1.6, slow walk 0.9, run 5.5 m/s |
| A06.02 | A usable sprint where the game's travel distances imply one | covered | 1.1.1 FIT-G4 5.2.1 |  | run at 5.5 m/s for chases; no stamina |
| A06.03 | Acceleration that fits the character's apparent weight | covered | 1.1.1 | G6 | partly: weight and short ease named; start and stop numbers wait on measuring |
| A06.04 | Deceleration that fits the intended responsiveness | covered | 1.1.1 | G6 | partly: short ease on stopping; no numbers |
| A06.05 | Turning that looks and feels connected to the feet | unreal | 5.2.1 1.1.1 |  | was covered; motion matching with no foot sliding; quick turning |
| A06.06 | Stationary turning without impossible foot rotation | unreal | 5.2.1 1.1.1 |  | was covered; partly: motion matching; turn on the spot is not specified |
| A06.07 | Backward movement with an appropriate gait | unreal |  |  | was missing; needs a line on backing-up gait (he backs out of rooms and off fights) in 5.2.1 or 1.1.1 |
| A06.08 | Sideways movement with an appropriate gait | unreal |  |  | was missing; needs a line on sideways gait (or that movement always faces travel) in 5.2.1 or 1.1.1 |
| A06.09 | Smooth transitions between movement speeds | covered | 5.2.1 1.1.1 |  | partly: motion matching and eased movement; blends not tested |
| A06.10 | Consistent movement relative to the camera or facing convention | missing |  |  | needs a stated rule for movement relative to camera (camera-relative on keys and stick) and a test |
| A06.11 | Reliable movement over small kerbs and floor seams | covered | 1.1.3 8.10 |  | partly: never stuck within 5 s and no pass-through; kerbs and seams not named |
| A06.12 | Reliable movement up and down ordinary stairs | covered | 1.1.3 8.10 | G8 | stairs walked, not snagged on; no speed or time |
| A06.13 | Sensible behaviour on slopes | missing |  |  | needs a slope rule (Quay Street climbs 48 m from the quay) and a walk test |
| A06.14 | Clear limits on slopes too steep to climb | missing |  |  | needs a slope limit and what stops him; the town is mostly flat but nothing says so |
| A06.15 | No snagging on tiny decorative geometry | covered | 8.10 1.1.3 |  | partly: zero stuck over 5 s in the soak; small decoration not named |
| A06.16 | Predictable sliding along a wall instead of becoming stuck | covered | 8.10 1.1.3 |  | partly: never stuck over 5 s; sliding along walls is not stated |
| A06.17 | A crouched collision shape that actually fits under lower obstacles | out | OUT-08 |  | OUT-08 no crouch (OUT-08 reads wider than the ruling, which says only no jump) |
| A06.18 | Prevention of standing through a ceiling | out | OUT-08 |  | OUT-08 no crouch, so nothing to stand through (OUT-08 reads wider than the ruling, which says only no jump) |
| A06.19 | Movement that follows moving platforms | out | 4.6.2 |  | RULINGS 23 Sep: boats and buses are scenery; Tom rides cars only (1.2.8) |
| A06.20 | Appropriate restrictions while carrying, aiming or injured | covered | 1.1.4 FIT-G4 1.3.11 |  | holdall slows him; a limp for a day after a beating; slow walk |
| A06.21 | Recovery from being wedged between objects | covered | 1.1.3 8.10 |  | within 5 s he moves on or a short in-world reset puts him on clear ground |
| A07.01 | A responsive jump with readable height and distance | out | OUT-08 |  | OUT-08 no jump key (RULINGS 23 Sep genre: no jump) |
| A07.02 | Predictable control while airborne | out | OUT-08 |  | OUT-08 no jump key (RULINGS 23 Sep genre: no jump) |
| A07.03 | Forgiveness around ledge departure and landing inputs | out | OUT-08 |  | OUT-08 no jump key (RULINGS 23 Sep genre: no jump) |
| A07.04 | A landing animation appropriate to the fall | out | OUT-08 |  | OUT-08 no jump or climbing, so no drops; the quay edge stops him (4.2.4) |
| A07.05 | Fall damage that follows understandable rules | out | OUT-08 |  | OUT-08 no jump or climbing, so no drops; the quay edge stops him (4.2.4) |
| A07.06 | A clear distinction between a safe drop and a dangerous fall | out | OUT-08 |  | OUT-08 no jump or climbing, so no drops; the quay edge stops him (4.2.4) |
| A07.07 | Consistent identification of vaultable obstacles | covered | 1.1.8 |  | vault places are marked in the map data and prompted |
| A07.08 | Vaulting that fits the obstacle's height and thickness | covered | 1.1.8 |  | under about 1.2 m, running at it, about 0.8 s; thickness not named |
| A07.09 | Mantling that puts hands and feet on the actual surface | covered | 1.1.8 OUT-08 |  | partly: vault only, no mantle or climb; hand placement not stated |
| A07.10 | Prevention of climbing into blocked space | covered | 1.1.8 OUT-08 |  | vaults only at set marked places, nowhere else |
| A07.11 | A way to cancel or drop from a climb | out | OUT-08 |  | OUT-08 no climbing (OUT-08 reads wider than the ruling, which says only no jump) |
| A07.12 | Ladder entry from plausible positions | out | OUT-08 |  | OUT-08 no climbing, so no ladders for Tom (OUT-08 reads wider than the ruling, which says only no jump) |
| A07.13 | Ladder exit without falling or becoming stuck | out | OUT-08 |  | OUT-08 no climbing, so no ladders for Tom (OUT-08 reads wider than the ruling, which says only no jump) |
| A07.14 | Consistent behaviour at climbable and non-climbable lookalikes | out | OUT-08 1.1.8 |  | OUT-08 no climbing; vault points are the only marked ones (OUT-08 reads wider than the ruling, which says only no jump) |
| A07.15 | Clear entry into swimming rather than walking underwater | out | OUT-08 4.2.4 |  | OUT-08 no swimming; Tom never enters the water (4.2.4) (OUT-08 reads wider than the ruling, which says only no jump) |
| A07.16 | A usable transition between swimming and the shore | out | OUT-08 4.2.4 |  | OUT-08 no swimming; Tom never enters the water (4.2.4) (OUT-08 reads wider than the ruling, which says only no jump) |
| A07.17 | Swim movement and animation that agree | out | OUT-08 4.2.4 |  | OUT-08 no swimming; Tom never enters the water (4.2.4) (OUT-08 reads wider than the ruling, which says only no jump) |
| A07.18 | Readable breath or drowning rules if diving is possible | out | OUT-08 4.2.4 |  | OUT-08 no swimming; Tom never enters the water (4.2.4) (OUT-08 reads wider than the ruling, which says only no jump) |
| A07.19 | Water camera and sound changes when submerged | out | OUT-08 4.2.4 |  | OUT-08 no swimming; Tom never enters the water (4.2.4) (OUT-08 reads wider than the ruling, which says only no jump) |
| A07.20 | Appropriate controls and release behaviour for ropes, ziplines or grapples, if included | out | OUT-08 |  | OUT-08 no climbing and no grapples or ropes (OUT-08 reads wider than the ruling, which says only no jump) |
| A08.01 | A complete character model from ordinary viewing angles | unreal | 5.1.1 5.1.2 5.10 |  | MetaHuman faces and bodies judged in Unreal against the Hook sheet; no all-angle check named |
| A08.02 | Consistent scale between characters and their surroundings | unreal | 5.1.2 5.3.1 4.1.5 |  | bodies fixed in F:\LedgerTools; building kits from dated photographs; needs a scale check in the Unreal gate |
| A08.03 | Clothing that fits the body rather than visibly floating | unreal | 5.1.4 5.1.2 |  | clothes fit the bodies, no clipping or holes (floor) |
| A08.04 | Believable hands and fingers | unreal | 5.1.2 |  | none names hands; needs a hands check in the Unreal gate (close-ups, held items) |
| A08.05 | Believable eyes, eyelids and gaze direction | unreal | 5.1.1 5.2.4 |  | partly: faces judged at talking distance; eyelids and gaze not named |
| A08.06 | A mouth interior that survives ordinary close-ups | unreal | none |  | needs a mouth-interior check in the Unreal gate (teeth, tongue in talk close-ups) |
| A08.07 | Hair that behaves plausibly under the game's lighting | unreal | 5.1.3 |  | hair pass list: by day, night, wet, from behind, at four distances |
| A08.08 | Skin, fabric, leather and metal that look different | unreal | 5.1.4 5.3.2 5.10 |  | clothes floor and calibrated reflectances; no list of cloth, leather and metal to tell apart |
| A08.09 | Equipped clothing and gear reflected on the visible character | covered | 1.6.10 1.6.9 1.1.4 |  | three outfits and a dark coat show on him; holdall seen, coat items unseen |
| A08.10 | Held items attached to the correct hand and orientation | covered | 5.2.3 1.1.4 |  | partly: holdall in hand; no rule for correct hand or orientation beyond no glitches |
| A08.11 | Holstered gear occupying a plausible place on the body | covered | 1.6.9 1.1.4 |  | partly: gear under the coat is unseen by design; no holster |
| A08.12 | No major body or clothing gaps during ordinary poses | unreal | 5.1.4 5.2.3 |  | no clipping or holes; poses in the gate |
| A08.13 | A character shadow that matches the visible body and equipment | unreal | 5.4.2 5.1.4 |  | none names character shadows; needs a shadow check in the Unreal gate |
| A08.14 | Consistent appearance across gameplay, menus and cutscenes | unreal |  |  | was missing; needs a line that the ferry shot, talk and play use the same character assets and outfit state |
| A08.15 | Detail changes with distance that do not transform identity | unreal | 5.1.3 5.1.4 |  | hair judged at about 1, 3.1, 10 and 25 m with no colour change or popping; faces and bodies by LOD not named |
| A08.16 | Visible wetness, dirt or injury where the presentation promises it | covered | 1.3.11 5.9 1.4.4 5.3.2 |  | partly: bruises, cut lip, limp, blood and dirt shown on him; wet clothes in rain not stated |
| A08.17 | Consistent first-person hands, body and third-person appearance where both views exist | out | OUT-02 |  | OUT-02 no first-person view |
| A09.01 | Idle breathing and small posture changes | unreal | 5.2.5 |  | idles must not hold still; breathing not named |
| A09.02 | Idle variation rather than a conspicuous repeating loop | unreal | 5.2.5 | G204 | random start, play rate 0.9 to 1.1; idle counts not set |
| A09.03 | Feet that remain planted instead of sliding during stops | unreal | 5.2.1 | G200 | feet must not slide; 3 cm a contact in research, test not run |
| A09.04 | Foot placement that follows stairs and uneven ground | unreal | none |  | needs foot placement on stairs and uneven ground in 5.2.3 or 5.2.1 and a check in the Unreal gate |
| A09.05 | Knees and hips that accommodate different foot heights | unreal | none |  | needs the same Unreal check (leg bend on steps and kerbs) |
| A09.06 | Stride length that matches travel speed | unreal | 5.2.1 |  | motion matching with feet not sliding; speeds set |
| A09.07 | Body lean during acceleration and turning | unreal | 5.2.1 |  | partly: motion matching only; lean is not named |
| A09.08 | Smooth transitions between idle, walking and running | unreal | 5.2.1 |  | motion matching blends walk and run |
| A09.09 | Upper-body actions that coexist with leg movement | unreal | 5.2.1 5.2.3 |  | none says upper-body actions play over walking (carry, smoke, search); needs a layered-animation line |
| A09.10 | Head movement that is partly independent of the torso | unreal | 5.2.6 5.2.4 | G208 | head turns first at the start of recognition; independence from torso is not specified |
| A09.11 | Hands that meet handles, rails and other contact points | unreal | 5.2.3 | G202 | only standard is that none glitches |
| A09.12 | Finger poses that fit held objects | unreal | none |  | needs finger poses for held things (holdall, cigarette, gun) in the Unreal gate |
| A09.13 | Two-handed objects held by both hands | unreal | none |  | needs two-handed holds named (a box, a gun) or ruled out |
| A09.14 | Seated bodies that actually meet the chair | unreal | 5.2.3 1.1.7 |  | sit is named as an interaction; contact with the seat is not |
| A09.15 | Sit-down and stand-up transitions | unreal | 5.2.3 1.1.7 | G202 | sit and stand named; transitions have no timing |
| A09.16 | Animation appropriate to the character's current weapon or burden | unreal | 5.2.1 5.2.3 5.2.2 | G202 | holdall run speed set; carry and weapon animation sets not listed |
| A09.17 | Reactions to impacts that fit their direction | covered | 5.2.8 1.3.1 |  | a struck man reels by the side he was hit |
| A09.18 | Interruptions that leave the body in a valid pose | unreal | none |  | needs a rule that cut-off animations blend to a valid pose (gate check) |
| A09.19 | Recovery from knockdown that connects to the final fallen position | covered | 5.2.8 RT2-11 | G207 | partly: rolls once and sits up within 5 s; clip count and final-pose match not set |
| A09.20 | Death motion or ragdoll behaviour consistent with the hit | covered | RT2-12 5.2.8 8.10 | G291 | partly: falls follow hit direction and speed bands; ragdoll blend not designed |
| A09.21 | Bodies that rest on the ground rather than hover | covered | 8.10 5.2.8 |  | partly: nothing passes through floors or walls; resting contact not named |
| A09.22 | Hair, clothing and attachments that follow body movement | unreal | 5.1.3 5.1.4 9.1.8 |  | hair strands and loose cloth parts simulated; follow-through not tested apart from the gate |
| A09.23 | No sudden default pose while an animation loads | unreal | none |  | needs a check that nobody shows a default pose on streaming in (Unreal gate) |
| A09.24 | No identical synchronised idle motion across a crowd | unreal | 5.2.5 |  | was covered; random start and play rate 0.9 to 1.1 with neighbours differing |
| A10.01 | NPCs turning their eyes toward someone addressing them | unreal | 5.2.4 5.2.9 | G208 | was covered; partly: both face each other with a glance before a live answer; eyes alone not named |
| A10.02 | NPCs turning their head toward an approaching player when appropriate | covered | 5.2.6 1.4.1 |  | partly: head turns for recognition; a stranger turning to an approaching Tom is not named |
| A10.03 | The torso turning when the player moves beyond a comfortable head angle | unreal |  | G208 | was missing; needs a gaze rule that the torso follows when Tom is beyond a comfortable head angle |
| A10.04 | Limits that prevent impossible head and neck rotation | unreal | none |  | needs neck and head limits in the Unreal gate for the head turns of 5.2.6 |
| A10.05 | Gaze directed at the player's face rather than their feet or empty space | unreal | 5.2.4 | G208 | was covered; partly: both face each other at about 1.5 m; gaze target not specified |
| A10.06 | Eye contact that occasionally breaks | unreal |  | G208 | was missing; needs a gaze rule for occasional breaks of eye contact in talk |
| A10.07 | Blinking rather than a permanent stare | unreal | none |  | needs a blink check in the Unreal gate (MetaHuman faces) |
| A10.08 | Facial expression that broadly fits the line being spoken | unreal | 5.2.4 5.2.9 | G203 | was covered; partly: mouths follow loudness only; no expression list |
| A10.09 | Listener reactions while another person speaks | unreal |  | G208 | was missing; needs a listener-reaction rule during live and written lines |
| A10.10 | Gestures that fit the conversation rather than random arm waving | unreal |  | G208 | was missing; needs a gesture set for talk; 5.2.9 says gestures are not designed |
| A10.11 | People orienting toward a shared point of interest | covered | 2.5.3 3.7 |  | partly: after a seen deed people look and gather; shared attention at other times not named |
| A10.12 | Expression and posture changes when a conversation becomes hostile | covered | 1.3.4 5.2.6 |  | the ladder from stare and square up to threat shows in posture and face |
| A10.13 | Reactions to excessive proximity | missing |  |  | needs a reaction rule when Tom stands too close to a stranger or stares |
| A10.14 | A return to ordinary activity after the player leaves | covered | 2.1.1 2.5.3 5.2.5 |  | people go back to their routine; a crowd drifts back after a deed |
| A11.01 | A clear way to distinguish usable objects from decoration | covered | 6.1.1 1.6.8 AX-11 |  | everything usable has a prompt; key objects distinct by shape and light |
| A11.02 | A stable current interaction target | covered | 6.1.1 |  | prompt held 0.2 s before it changes |
| A11.03 | Prompts attached to the intended object | covered | 6.1.1 |  | prompt names the person or thing ahead and in view |
| A11.04 | Interaction range that matches apparent reach | missing |  |  | needs a use range in metres and a check (reach versus the visible object) |
| A11.05 | No interaction through an intervening solid wall | covered | 6.1.1 |  | partly: prompts only for what is ahead and in view; wall test not named |
| A11.06 | Appropriate priority when talk, loot and open share a button | covered | 6.1.1 |  | one prompt asks which when two things share a key; a person with a word comes before a door |
| A11.07 | A clear description of the action before committing | covered | 6.1.1 1.6.8 |  | the prompt names what the action will do |
| A11.08 | Feedback when an interaction succeeds | covered | 6.2.2 6.1.3 |  | partly: Day book and belief line record results; no general success cue for each interaction |
| A11.09 | Feedback explaining why an interaction is unavailable | covered | 1.1.3 FIT-P34 |  | a locked door says it is locked; other doors say so |
| A11.10 | Progress indication for prolonged interactions | missing |  |  | needs a progress sign for timed searches (2, 4 and 5 s) and the held pocket lift |
| A11.11 | Predictable cancellation of prolonged interactions | missing |  |  | needs a cancel rule for searches and holds (stepping away aborts) |
| A11.12 | Doors whose visible movement agrees with their blocking state | covered | 1.1.3 8.10 |  | partly: doors open with the use key and never catch; door collision state not named |
| A11.13 | Door handling that does not trap the player inside the door | covered | 1.1.3 1.2.3 8.10 |  | never stuck over 5 s; a blocked car door never traps him |
| A11.14 | Sensible behaviour when a door's path is obstructed | missing |  |  | needs a rule for a door blocked by a body or prop (stop, push or refuse) and a test |
| A11.15 | Locked doors that communicate their status | covered | 1.1.3 FIT-P34 1.6.1 |  | a locked door says it is locked; keys and force are the ways in |
| A11.16 | Containers that visibly and mechanically change after opening | covered | 1.6.2 FIT-P52 |  | partly: drawers, desks and wardrobes searched and found items authored; visible opening not stated |
| A11.17 | Pickups that disappear or change state when taken | covered | 1.6.2 1.6.3 |  | partly: taking is one press and goods leave the place; visible removal not stated |
| A11.18 | A dropped object appearing in a sensible reachable place | covered | 1.3.6 1.6.7 |  | partly: dropped weapons and left things stay in the world; landing place not ruled |
| A11.19 | Readable inspection views for documents and small objects | covered | 6.10 |  | letters open on screen as a page and go into the Ledger |
| A11.20 | Return from inspection to the previous position and context | missing |  |  | needs a line that closing a letter or inspect view returns him to the same spot and camera |
| A11.21 | Controls for switches, terminals and similar devices that produce a visible result | covered | 1.6.8 RT2-19 |  | kettle, radio, fare book, tin and phones each used by the use key |
| A11.22 | Occupied objects that cannot be used by two characters simultaneously | covered | 2.1.1 |  | partly: places have a cap and an owner for people; Tom and a person on one object not named |
| A11.23 | Clear distinction between harmless use and theft or aggression | covered | 2.2.6 1.6.2 1.6.3 |  | places labelled public, open by hours, private or forbidden; taking and lifts are deeds seen like any |
| A11.24 | An interaction ending cleanly if its object is destroyed or removed | missing |  |  | needs a rule for an interaction ending cleanly when its object is broken or taken (1.6.14 breaks things) |
| A12.01 | Solid ground everywhere that appears walkable | covered | 8.10 |  | zero pass-throughs and zero stuck over 5 s in a 2-hour soak |
| A12.02 | Solid walls where walls are visibly present | covered | 8.10 |  | nothing passes through walls |
| A12.03 | Collision shapes that broadly match visible objects | covered | 8.10 |  | partly: pass-through detector; collision fit to the visible shape is not checked |
| A12.04 | Doorways that admit a character who visibly fits | covered | 1.1.3 8.10 |  | door use under 2 s, never catches |
| A12.05 | Small loose objects that do not act like immovable roadblocks | missing |  |  | needs a rule for small loose props (bins, crates, stones) so they do not block him |
| A12.06 | Heavy objects that do not behave like weightless toys | missing |  |  | needs a weight line for heavy props (crates, barrels) and a test |
| A12.07 | Dropped objects falling under consistent gravity | missing |  |  | needs one gravity and a drop test for thrown stone, dropped items and bodies |
| A12.08 | Objects settling instead of vibrating indefinitely | missing |  |  | needs a settle-time rule for props and bodies (sleep after a set time) |
| A12.09 | No explosive physics response from mild contact | covered | 8.10 |  | partly: no car launches or spins on a touch; props not named |
| A12.10 | Fast objects that do not pass through obvious barriers | covered | 8.10 |  | zero pass-throughs including cars, checked by detector |
| A12.11 | Characters not pushing through one another without explanation | covered | 8.10 |  | nothing passes through bodies or cars |
| A12.12 | A workable solution to being blocked by a friendly character | missing |  |  | needs a rule for being blocked by a friend or crewman (swap, nudge or wait) |
| A12.13 | Moving machinery carrying or blocking objects consistently | missing |  |  | Decide in or out: no moving machinery (cranes, lorry tail-lifts, barriers) is designed at the docks |
| A12.14 | Appropriate friction on visibly different surfaces where it matters | covered | 1.2.1 5.5.1 |  | partly: rain lowers car grip and footsteps differ by surface; on foot no friction |
| A12.15 | Physical reactions accompanied by matching sound | covered | 5.5.2 5.5.6 5.5.1 | G217 | doors, impacts and blows have their own sound layers |
| A12.16 | Broken objects leaving plausible remnants if destruction exists | covered | 2.19 1.6.14 5.3.2 |  | glass and damage stay until mended; remnants not itemised |
| A12.17 | Destruction that changes collision as well as appearance | missing |  |  | needs a rule that a broken window or door changes collision and what he can pass through |
| A12.18 | Stable interaction between bodies, props and uneven ground | covered | 8.10 |  | partly: soak of walking, driving and fights; props on uneven ground not named |
| A13.01 | People walking somewhere or doing something | covered | 2.1.1 2.1.2 3.7 |  | everyone keeps a routine; crowd keeps clock windows |
| A13.02 | Variation in pace, posture and activity | covered | 2.1.2 5.2.5 5.1.5 | G199 | partly: activity from routines and idle variation; pace and posture variety has no rule |
| A13.03 | People avoiding one another while moving | covered | 2.1.5 | G77 | crowd walks round people and things without jams; no distances yet |
| A13.04 | People avoiding the player when there is room | covered | 2.1.5 | G77 | partly: avoidance and step-aside timing still to be measured |
| A13.05 | A response to bumping into someone | covered | 3.6.4 |  | partly: crowd lines for bumping into someone; no body reaction is named |
| A13.06 | A response to repeatedly blocking someone's route | missing |  |  | needs a rule for people reacting to Tom blocking their way (a remark, then a step round) |
| A13.07 | Navigation through doorways without permanent jams | covered | 2.1.1 2.1.5 |  | caps and owners per place so no doorway jams; 30-minute crowd walk |
| A13.08 | Use of stairs rather than walking through their geometry | covered | 2.1.1 8.10 |  | partly: every walk arrives and nothing passes through walls; stairs not named for crowd |
| A13.09 | Plausible transitions into sitting, working or leaning | covered | 5.2.3 1.1.7 5.2.5 | G204 | partly: sit, lean and smoke are named interactions; NPC work and sit idles are not built |
| A13.10 | Hands and props matching the activity being performed | unreal |  | G204 | was missing; needs an idle list by trade with props (broom, crate, cigarette), since work and smoke idles are not built |
| A13.11 | Conversations with actual listeners | covered | 2.4.1 3.6.4 3.6.3 |  | partly: neighbours greet and talk passes within 6 m; staged two-person chat not named |
| A13.12 | People taking turns rather than all speaking simultaneously | missing |  |  | needs a rule that two people speak in turn and wait, with a transcript check |
| A13.13 | Ambient speech that is not repeated every few seconds | covered | 3.6.3 FIT-L01 3.6.4 |  | no shared street line heard twice in one real hour; speech at most every 45 s |
| A13.14 | Reactions to a nearby loud or unusual event | covered | 1.4.3 1.2.11 2.5.3 |  | noises turn heads at their reach; people look and gather |
| A13.15 | Reactions to a visibly drawn weapon where the setting warrants it | covered | 2.5.3 1.3.8 |  | watchers keep about 3 m and scatter once a weapon is out; bystanders who saw a weapon flee |
| A13.16 | Different reactions to harmless proximity and actual violence | covered | 2.5.3 1.3.8 |  | harmless proximity draws a look; a seen deed or weapon brings gathering or flight |
| A13.17 | Fleeing or taking cover from danger | covered | 2.5.3 1.3.8 |  | partly: bystanders flee a weapon; taking cover is not named |
| A13.18 | Escape routes that lead away from danger | missing |  |  | partly in 2.5.3 (bystanders who saw a weapon flee); needs a rule that they run away from the danger and toward the doors, with a test |
| A13.19 | A response to an injured or dead person | covered | 3.6.4 2.16 2.5.3 3.7 |  | a body or a man down has its own situation lines; people gather; a man fallen on the cobbles is a happening |
| A13.20 | A way for panic to resolve once danger passes | covered | 2.5.3 2.5.4 |  | partly: crowd drifts back and witnesses talk quieter; a panic-end rule is not named |
| A13.21 | People who do not immediately resume cheerful chatter beside an ongoing emergency | covered | 2.5.3 3.6.4 |  | witnesses talk quieter for a game hour; lines for a body or man down |
| A13.22 | Consistency between a person's current behaviour and dialogue | covered | 3.6.2 2.1.1 |  | a character says only what the simulation knows; activity from routine |
| A13.23 | Appropriate response when spoken to during another activity | missing |  |  | needs a rule for how a person answers when spoken to mid-task (stops, answers short, glances) |
| A13.24 | Some continuity when briefly looking away and back | covered | 2.1.1 2.1.3 |  | the town code uses no chance and unseen people keep the same rules, so the same week plays the same |
| A13.25 | No obvious appearance or disappearance directly in view | missing |  | G270 | needs a spawn and despawn rule that nobody pops in or out in view, with a distance and a test |
| A13.26 | A reasonable solution when an NPC's intended route becomes blocked | covered | 2.1.1 2.1.5 |  | partly: places have caps and every walk arrives; re-routing around a blocked path is not named |
| A14.01 | Enemies detecting the player through understandable senses | covered | 1.4.1 2.2.3 2.2.4 |  | Watchers see and hear by set distance, light and noise reach. |
| A14.02 | Solid cover preventing direct sight where expected | covered | 1.1.5 1.5.4 |  | Behind a van, stall or corner nothing is caught; watchers never see through walls. |
| A14.03 | A readable transition from unaware to suspicious to engaged | covered | 1.4.1 2.2.2 2.3.2 |  | Head turn at least 0.8 s before identification, then the five-rung ladder from shape to known. |
| A14.04 | Reactions to relevant sounds | covered | 1.4.3 1.4.8 2.2.4 |  | Noise reach by act, hour and rain; heads turn to noises. |
| A14.05 | Investigation of a sound's location rather than magical knowledge of the player | covered | 1.4.8 |  | A watcher inside a noise reach turns or walks to look and remembers the noise; Tom is not known by magic. |
| A14.06 | Search focused on the last plausible known position | covered | 1.5.4 DP5-C03 2.6.10 |  | After a lost chase the patrol searches the last-seen streets only. |
| A14.07 | A distinction between seeing the player and being told about them | covered | 2.3.1 2.4.1 2.3.2 |  | Memory records what each person saw, heard or was told, with certainty by source. |
| A14.08 | Communication of an alert through visible or audible behaviour | covered | 1.4.1 1.5.4 2.5.3 |  | Alert shown by body and voice: head turns, calling out, walking off to tell, crowd looks. |
| A14.09 | Enemy movement that uses the actual available routes | covered | 1.5.4 1.5.1 |  | partly: pursuers use the real back ways and never cheat through walls; no stated test that NPC pathing uses only walkable routes. |
| A14.10 | Replanning when doors, vehicles or other obstacles move | missing |  |  | Needs a rule and test that NPC and pursuer paths replan when a door shuts or a car blocks a lane. |
| A14.11 | Enemies able to negotiate ordinary stairs and doorways | covered | 8.10 2.1.1 1.1.8 |  | partly: nobody stuck over 5 s and places capped so doorways do not jam; no stairs test for NPCs. |
| A14.12 | Combat positioning that avoids all enemies occupying one point | covered | 1.3.2 1.3.8 |  | partly: at most two men swing at once, 0.4 s apart, watchers keep about 3 m; no spacing rule beyond that. |
| A14.13 | Enemies using appropriate engagement distance | covered | 1.3.12 1.3.3 |  | Fighter types set distance: brawler rushes, knife man keeps away, boxer guards. |
| A14.14 | Enemies not firing continuously into an obvious obstruction | missing |  |  | Needs a rule in RT-10 that armed men do not fire without a clear line, and a test with a wall between. |
| A14.15 | Appropriate retreat, advance or repositioning | covered | 1.3.9 1.3.8 1.3.12 RT-10 |  | Men back off, run or give way by nerve; the wiry type slips and runs; armed men run when outmatched. |
| A14.16 | A response to being flanked | missing |  |  | Needs a rule for how a man reacts when Tom or a mate gets behind him (turn, call out or break). |
| A14.17 | A response to allies being injured or killed | covered | 1.3.8 1.3.9 2.14 |  | partly: nerve and numbers make a man give way sooner when alone; no explicit reaction to a mate going down. |
| A14.18 | Believable limits on accuracy and reaction speed | covered | 1.3.2 RT-10 |  | Every blow readable 0.45 to 0.80 s ahead; gun hits depend on aim, distance and movement. |
| A14.19 | Clear reasons when an enemy cannot be damaged or interrupted | covered | 1.3.1 1.3.2 1.3.12 |  | partly: committed blows and breaking weapons are readable; nobody is invulnerable so no special reason line is needed. |
| A14.20 | A sensible end to searching or combat | covered | 1.3.9 1.5.4 DP5-C01 |  | A fight ends by back-off, run, down or police; a chase ends lost, caught, wrecked or at the edge. |
| A14.21 | No immediate forgetting of a fight merely because the player steps around a corner | covered | 2.3.1 1.5.4 DP5-C03 |  | Memory is permanent and a search continues; seen again inside it the same chase resumes. |
| A14.22 | No pursuit through impossible or inaccessible routes | covered | 1.5.1 1.5.4 8.10 |  | Bollarded lanes stop cars, pursuers never pass walls, and no stuck over 5 s. |
| A14.23 | No permanent lock into combat after every threat is gone | covered | 1.3.9 DP5-C01 |  | No chase timer but fixed endings; fights end on back-off or arrival of police. |
| A15.01 | A clear indication of whether the player is concealed or exposed | covered | 6.1.4 1.4.1 1.4.2 |  | Picture corners darken with the watchers' light value; nothing says hidden by design. |
| A15.02 | Consistent effects of posture on visibility and noise | covered | 1.1.5 2.2.4 OUT-08 |  | partly: still, slow walk and run change sight and noise; no crouch (OUT-08 no crouch). |
| A15.03 | Consistent effects of lighting if darkness is a stealth mechanic | covered | 1.4.2 2.2.3 |  | Light scale daylight 1, lamp 0.7, unlit 0.25, doorway 0.12 drives what is caught. |
| A15.04 | Sound generation that matches movement and actions | covered | 2.2.4 1.4.3 5.5.1 |  | Noise reach by act (walk, run, door, car, horn, shot) and the player hears the same. |
| A15.05 | Readable boundaries for restricted areas | covered | 2.2.6 4.1.3 |  | partly: places carry public, hours, private or forbidden labels; how a private place reads to the eye is not stated. |
| A15.06 | A warning or understandable transition before punishment where appropriate | covered | 2.2.6 1.6.1 1.5.4 |  | A challenge warns, warns again, then acts; a constable announces himself 3 s ahead. |
| A15.07 | Distinction between suspicious behaviour and an openly hostile act | covered | 1.3.4 2.2.1 |  | Eight-rung ladder: stare, square up, threaten up to kill, each an act the town reads. |
| A15.08 | Witness reactions that depend on whether they could observe the event | covered | 2.2.1 2.2.3 2.3.2 |  | Witness knowledge depends on distance, light, facing and what was caught. |
| A15.09 | A visible or audible reporting process if reporting matters | covered | 2.5.1 2.5.2 |  | A witness walks to a friend, phone box or station and is seen going; walk of at least 30 s. |
| A15.10 | A chance to respond before an alert spreads, where promised by the design | covered | 2.5.1 2.5.2 |  | Tom can reach the walker first and talk her round, pay, threaten or let go. |
| A15.11 | Law response proportionate to the apparent offence | covered | 2.6.3 2.6.9 2.13 |  | Police response set by deed, signed statement and the escalation dial; no fines as a system. |
| A15.12 | An understandable wanted or pursuit state | covered | 2.13 2.4.3 1.5.4 |  | Dial is a fact in town memory shown in people and police, not a meter; chase shown by the pursuer. |
| A15.13 | Clear conditions for losing pursuit | covered | DP5-C01 FIT-F03 1.5.4 |  | Lost after 7 s unseen or a set gap while out of sight; no timer. |
| A15.14 | Searches that do not continuously know the hidden player's exact location | covered | 1.5.4 DP5-C03 2.6.10 |  | Searchers go to the last-seen streets and do not know where he hid. |
| A15.15 | Consistent treatment of disguises or changed appearance if supported | covered | 1.4.4 1.6.10 |  | Coat, cap, respray and barber shed what a witness has not told; gossip already carried stays. |
| A15.16 | Distinction between surrender, escape and renewed aggression | covered | 2.6.2 RT2-22 1.3.9 |  | Stand and be searched, run and it is a chase, back off ends a fight; caught runner searched as if he stood. |
| A15.17 | Clear consequences of fines, arrest or confiscation | covered | 2.6.4 2.6.9 2.6.2 7.9 |  | Arrest costs set game hours, charge and bail, search keeps what is found; no fines. |
| A15.18 | A usable return to ordinary play after punishment or escape | covered | 7.9 2.6.4 4.3.8 |  | Control back within 2 real minutes after arrest or beating, with the cost said. |
| A15.19 | No punishment for an action the controls misleadingly presented as harmless | covered | 6.1.1 1.6.1 |  | partly: prompt names the thing and the wrong action never fires; no test that harmless-looking prompts carry no crime. |
| A16.01 | Following at a useful distance | covered | 1.7.4 |  | A man at his side follows at about 2 m. |
| A16.02 | Keeping up without repeatedly falling far behind | covered | 1.7.4 |  | Never lags more than 10 s. |
| A16.03 | Slowing down or waiting appropriately during guided travel | covered | 1.7.4 1.7.1 |  | He waits at doors and on a wait order. |
| A16.04 | Yielding when blocking a doorway or corridor | covered | 1.7.1 1.7.4 |  | Crew never block a door or lane (ER-CREW-02). |
| A16.05 | Navigating the same ordinary obstacles as the player | covered | 1.7.4 8.10 |  | partly: doors, car and fights covered; vault places and stairs for followers not stated. |
| A16.06 | Sensible recovery when separated | covered | 1.7.4 |  | partly: keeps up or waits and never fails a job by being slow; no stated catch-up when truly left behind. |
| A16.07 | Entering and leaving vehicles appropriately | covered | 1.2.3 1.2.7 1.7.4 |  | Crew and fares ride in the cab and a man at his side rides along. |
| A16.08 | Participation in combat consistent with the companion's role | covered | 1.7.4 1.3.8 |  | He stands in a fight and takes the second man, so two against two is fair. |
| A16.09 | A clear response to friendly fire | missing |  |  | Needs a rule for Tom hitting a man at his side or a mate hit by a swing (reaction, memory, loyalty cost). |
| A16.10 | Commands with acknowledgement and visible results | covered | 1.7.1 |  | Two inputs at most, answered in voice or body within 1 s; a man who cannot says why. |
| A16.11 | Dialogue that survives walking, stopping and temporary interruption | covered | 5.8.3 RT2-20 1.2.7 |  | Talk can run while walking or driving; clock rule set for moving talk; no talk scene runs 60 s without control. |
| A16.12 | No repeated dialogue announcing an event that has already happened | missing |  |  | Needs a said-once flag on follower and passenger lines about events, tested in a long ride-along. |
| A16.13 | Clear downed, dead or unavailable states | covered | 2.11.3 2.16 1.7.1 |  | partly: fates, death and refusal-with-reason are covered; in-the-moment downed follower state not described. |
| A16.14 | A companion's presence and equipment surviving save and load | covered | 2.3.1 7.8 8.11.3 |  | partly: the town state and memory survive save and load (SaveChaos); a follower's present-at-his-side state is not named. |
| A17.01 | A clear distinction between exploration and combat readiness | covered | 1.3.4 1.3.6 |  | partly: weapons draw only on a held input and cannot be undrawn unseen; fists have no separate ready stance, guard is a held key. |
| A17.02 | Attacks that occur in response to the intended input | covered | 1.3.1 1.3.3 |  | A blow starts within 0.1 s of the button; the man pointed at is the man hit. |
| A17.03 | Reach and hit detection that broadly match the visible action | covered | 1.3.1 1.3.3 |  | No lock-on, slide to about 1 m, closing 0.40 to 0.55 s from at most 2 m, nobody hit through a wall. |
| A17.04 | A visible or audible distinction between hitting and missing | covered | 1.3.1 5.5.6 |  | Hit-stop, camera close-in and four sound layers with impact within 0.034 s of contact. |
| A17.05 | A distinction between damaging armour, a shield and an exposed target | missing |  |  | Decide in or out: no armour or shield in the design; guard in 1.3.2 is the nearest thing. |
| A17.06 | Reactions showing where damage came from | covered | 5.2.8 1.3.1 |  | A struck man reels to the side he was hit. |
| A17.07 | Clear feedback for blocked, resisted or ineffective attacks | covered | 1.3.2 5.5.6 |  | Blocked fist does little, blocked heavy blow staggers Tom, weapons break through. |
| A17.08 | Enemy attacks that can be read before they connect | covered | 1.3.2 |  | Every incoming blow readable 0.45 to 0.80 s before it lands, never an icon. |
| A17.09 | A comprehensible relationship between commitment and cancellation | covered | 1.3.1 1.3.2 |  | Heavy blow cannot be cancelled; a slip about 0.3 s turns the next blow into a counter. |
| A17.10 | Reliable switching between available combat actions | covered | 1.3.6 1.3.2 |  | Weapon on a held input from two things under the coat; guard and slip on their own keys. |
| A17.11 | A readable resource cost where attacks consume stamina or energy | covered | 1.3.2 5.9 |  | Mashing empties Tom in 6 to 10 jabs and he needs 4 to 8 s for his wind, shown in breath. |
| A17.12 | Consistent interaction between attacks and scenery | covered | 1.3.5 8.10 |  | Seven street places with paired moves; nobody hit through walls. |
| A17.13 | A clear end to the encounter | covered | 1.3.9 |  | A fight ends on back-off, run, down, police or people stepping in. |
| A17.14 | Feedback for victory, escape or failure | covered | 1.3.9 4.3.8 7.9 |  | Win ends the fight; a beaten Tom wakes with the cost said within 60 s; running is an input. |
| A17.15 | Camera and effects that leave the important action visible | covered | 5.8.1 1.3.1 |  | Fight camera 3.5 to 5.0 m back keeps both men's feet in at least 90% of frames; close-in is a switch. |
| A18.01 | Attack animations that fit the equipped weapon | unreal | 5.2.2 1.3.6 |  | Fight animation follows the melee sheet; weapon-specific fit is judged in Unreal. |
| A18.02 | Contact timing that agrees with damage timing | covered | 1.3.1 5.5.6 |  | Jab contact 0.25 to 0.40 s, hit-stop and impact sound locked to contact. |
| A18.03 | Plausible weapon reach | covered | 1.3.3 1.3.6 |  | partly: closing distance and swing times set; no reach figure per weapon. |
| A18.04 | Directional movement that does not slide the attacker implausibly into position | covered | 1.3.3 5.2.2 |  | partly: slide limited to about 1 m in the wind-up; animation quality judged in Unreal. |
| A18.05 | Readable attack recovery | missing |  |  | Needs recovery times after a jab, heavy blow and swing, and a test that they are readable. |
| A18.06 | Blocking that responds within the game's stated rules | covered | 1.3.2 |  | Guard is a held key with set results by blow type. |
| A18.07 | Clear distinction between blockable and unblockable attacks | covered | 1.3.2 |  | partly: swung weapons break through guard; no stated visual cue for the unblockable. |
| A18.08 | Dodge movement with understandable distance and vulnerability | covered | 1.3.2 |  | A tap with a direction slips a blow in about 0.3 s; counter follows. |
| A18.09 | Parry timing with readable success and failure, if present | covered | 1.3.2 |  | partly: no parry, a slip then counter has its own window and result. |
| A18.10 | Combos that accept inputs predictably, if present | missing |  |  | Decide in or out: no combo system is described, only single jab, heavy blow and swing. |
| A18.11 | Knockback or stagger appropriate to the attack | covered | 1.3.2 RT-11 5.2.8 |  | Stagger by blow type, hidden capacity by fighter type, reel to the hit side. |
| A18.12 | Finishing moves that cope with nearby walls and furniture | covered | 1.3.5 RT2-11 |  | partly: no finishers by design; the street moves are fitted by height to railings, bonnets and walls. |
| A18.13 | Multiple attackers behaving in a way the camera and controls can handle | covered | 1.3.2 1.3.8 5.8.1 |  | At most two swing at once, watchers keep 3 m, fight camera widens. |
| A18.14 | Consistent handling of unarmed attacks versus weapons | covered | 1.3.1 1.3.6 RT-11 |  | Fists never kill alone; weapons add capacity and swing time; things to hand break. |
| A19.01 | Aiming aligned with where the shot can actually travel | covered | RT-10 1.3.10 |  | partly: mouse or stick aims, hit depends on aim and movement; timings not yet set. |
| A19.02 | A solution to the camera seeing around cover while the muzzle remains blocked | missing |  |  | Needs a rule and test for the aim camera and muzzle at cover or a wall (aim blocked, no shot through geometry). |
| A19.03 | Projectile or hit behaviour consistent with the weapon | covered | RT-10 RT2-14 |  | partly: revolver and sawn-off are set apart by rounds and price; spread and range bands not set. |
| A19.04 | Recoil that is visible and reflected in subsequent aim | missing |  | G38 | Needs recoil and aim return for each gun, measured with the firearms footage. |
| A19.05 | Muzzle flash or another appropriate firing cue | unreal | 5.9 |  | muzzle flash is a looks item for the Unreal phase |
| A19.06 | Firing sound appropriate to the weapon and distance | covered | 2.2.4 5.5.7 1.3.10 |  | partly: shot heard to 177 m by day and gunshots clip in loud-noise softening; no per-weapon gun sound design. |
| A19.07 | Impacts at the actual hit location | covered | RT-10 |  | partly: arm shot disarms, leg shot stops a runner, so hit place matters; impact marks not specified. |
| A19.08 | Different impact responses for flesh, wood, metal and stone | unreal | none | G232 | 5.9 names blood, rain, breath, smoke and glass only; Unreal needs bullet and blow impacts per flesh, wood, metal and stone. |
| A19.09 | Appropriate rate of fire | missing |  | G38 | Needs a rate of fire for the revolver and sawn-off with the draw, aim and hit timings. |
| A19.10 | Ammunition counts that agree with shots fired | covered | RT-10 RT2-14 |  | partly: six rounds tracked and bought by the box; no on-screen count by design. |
| A19.11 | Distinct empty-weapon feedback | missing |  |  | Needs an empty-gun cue (click and hand action) in RT-10, since there is no ammunition count on screen. |
| A19.12 | Reloading with correct ammunition transfer | covered | RT-10 RT2-14 |  | partly: a revolver holds six and reloads in a shown action; transfer from boxes carried not stated. |
| A19.13 | Reload animation that matches the weapon | unreal | RT-10 5.2.3 |  | Reload is a shown action; the animation fit is judged in Unreal. |
| A19.14 | Predictable handling of interrupted reloads | missing |  |  | Needs a rule for a reload broken off by a hit, a draw change or running. |
| A19.15 | Weapon switching without duplicated or missing weapons | covered | 1.3.6 1.6.9 |  | Two things under the coat, drawn on a held input, one weapon at a time. |
| A19.16 | Equip and holster transitions that match the visible state | covered | 1.3.6 RT-10 |  | partly: draw on a held input and cannot be undrawn unseen; holster look not stated. |
| A19.17 | Clear distinctions between ammunition types or firing modes, if supported | missing |  |  | Decide in or out: only two guns with one round type each are described, no types or fire modes. |
| A19.18 | Controller aiming assistance appropriate to the design | covered | AX-05 |  | partly: Needs a pad aim-assist rule for the aim row (RT-10); 6.6 says only that every verb is reachable by pad. |
| A19.19 | Scope transitions that preserve orientation | missing |  |  | Decide in or out: no scoped weapon in the two-gun list (RT2-14), so likely moot. |
| A19.20 | A visible aiming or trajectory cue for throws where precision is expected | missing |  |  | Needs an aim or arc cue for thrown stones and goods (1.4.8, 1.6.7) or a stated decision that none is shown. |
| A19.21 | Thrown objects leaving from a plausible position | unreal | 5.2.3 1.4.8 |  | Throw animation and hand position judged in Unreal; 5.2.3 is only named, standard is that nothing glitches. |
| A19.22 | Explosion effects with understandable range and cover interaction | missing |  |  | Decide in or out: no explosives appear in the design; Bonfire Night display is the only blast-like event. |
| A19.23 | Damage feedback that distinguishes a hit from a kill | covered | RT-10 2.16 RT2-11 |  | Before War a gun hit wounds and never kills; killing is a named, permanent event. |
| A19.24 | Weapon behaviour near walls that does not visibly put the barrel through everything | unreal |  |  | was missing; Needs a rule that the drawn gun is lowered or blocked at close walls, with the aim row camera test. |
| A20.01 | An understandable representation of remaining health | covered | 1.3.7 RT-11 |  | Posture, breath, guard, blood and limp show state; no health bar; fresh, hurt, beaten. |
| A20.02 | Clear distinction between damage, healing and temporary protection | covered | 1.3.7 1.3.11 |  | partly: harm, marks and stitching by the doctor are shown; no temporary protection exists in the design. |
| A20.03 | Low-health warning without making the game unreadable | covered | 1.3.7 RT-11 |  | Hurt shows as slower guard, shorter breath and a stagger; no warning overlay by design. |
| A20.04 | Healing controls that give immediate acknowledgement | missing |  |  | Decide in or out: only healing is time and the doctor (1.3.11); no use-item healing verb is described. |
| A20.05 | Healing resource consumption that matches the action | missing |  |  | Decide in or out: same as A20.04; no healing item, so nothing is consumed. |
| A20.06 | Clear status effects and their duration or removal conditions | covered | 1.3.11 RT-11 |  | Bruises three game days, limp one day, knife bleeds until stitched. |
| A20.07 | Readable stamina or similar exhaustion feedback | covered | 1.3.2 5.9 |  | Breath shown; wind regained in 4 to 8 s. |
| A20.08 | A clear death or defeat state | covered | 1.3.9 7.9 OUT-12 |  | Tom cannot die; defeat is a beating with a waking place and cost. |
| A20.09 | Some indication of the cause of defeat | covered | 7.9 4.3.8 RT2-13 |  | The cost is said and the street knows he lost; who robbed him is known. |
| A20.10 | A quick, understandable retry route | covered | 7.9 1.3.9 OUT-12 |  | No game over; control back within 60 s after a beating, 2 minutes after any failure. |
| A20.11 | Checkpoints placed to avoid needless repetition | covered | 7.8 7.9 |  | No checkpoints; autosave after every deed, consequence and job step. |
| A20.12 | Consistent reset of enemies, resources and objectives on retry | covered | 7.8 2.3.1 |  | partly: no retry reset by design; reload gives the same next hour (ER-SAVE-01). |
| A20.13 | No respawn inside an active unavoidable hazard | covered | 4.3.8 1.3.9 |  | partly: three set waking places and control within 60 s; no test that no attacker is still on him. |
| A20.14 | Clear penalties for death, if any | covered | 1.3.9 RT2-13 7.9 2.6.4 |  | Robbery, lost hours, marks and talk are the penalties. |
| A20.15 | A way to recover from an unwinnable checkpoint or stuck state | covered | GD-03 GV-05 8.10 7.9 |  | Never stuck over 5 s, sequence breaks allowed, another road within a game day. |
| A20.16 | Ability to adjust relevant difficulty or assistance without discarding the playthrough | covered | 7.10 6.4 |  | Assists are settings, off by default, each changing only its own thing. |
| A21.01 | Human-scale doors, stairs, furniture and streets | covered | 1.1.3 4.1.5 4.3.1 |  | Door widths and room sizes from interior research; street rules from Study 4. |
| A21.02 | Plausible connections between adjacent spaces | covered | 4.3.2 FIT-P34 4.1.5 |  | partly: office to flat by stair and rooms counted; no general adjacency rule. |
| A21.03 | Exteriors and interiors that broadly agree in position and size | missing |  |  | Needs a check that outside footprints and inside room sizes agree (door and window positions match). |
| A21.04 | Clear distinction between reachable scenery and background scenery | covered | FIT-P34 4.2.4 8.10 |  | Every other door says it is locked; the quay edge stops him like a kerb. |
| A21.05 | Readable routes through ordinary environments | covered | 6.9 4.1.3 6.3 |  | Door numbers, street name plates and the paper map; directions by landmark. |
| A21.06 | Landmarks that help orientation | covered | 4.1.3 6.9 3.4.3 |  | Named landmarks, and Pauline gives the way by landmark. |
| A21.07 | Visually distinct areas rather than indistinguishable repeated streets | covered | 4.2.1 4.2.2 4.2.3 4.3.3 |  | Ferry landing, basin, dock gate and Quay Street are separate named places. |
| A21.08 | Consistent visual language for climbable, breakable and inaccessible objects | missing |  |  | Needs a look rule for vault places (1.1.8) and breakable things to hand (1.3.6), so players can tell them. |
| A21.09 | Boundaries communicated by believable obstacles or explicit rules | covered | 4.1.4 4.2.4 OUT-05 |  | Quay edge, bollards, and a soft edge back as time passed. |
| A21.10 | A usable response to leaving the intended play area | covered | 4.1.4 |  | Leaving by the soft edge is a time skip, nothing fails. |
| A21.11 | Space for the character and camera along intended routes | covered | 1.1.2 1.1.3 5.8.1 |  | Camera never ends inside a wall; Tom's 68 cm against real doorway widths. |
| A21.12 | Alternative routes where exploration is presented as open-ended | covered | 4.1.2 1.5.1 FIT-G1 |  | partly: loops, ginnels and yards give routes; no stated test of alternatives per job. |
| A21.13 | Useful destinations rather than scenery alone | covered | 7.12 FIT-P34 4.3.3 |  | Something to do within 30 s by day; 24 enterable rooms each with a usable object. |
| A21.14 | Travel distances appropriate to available movement options | covered | GD-01 FIT-G4 CLK-03 |  | Travel time bands, speeds and places within about 200 m of walking. |
| A21.15 | A way back from ordinary exploratory detours | covered | 6.3 6.9 |  | Paper map and street signs; Ledger keeps directions. |
| A21.16 | Consistency between visible danger and actual traversal rules | covered | 4.2.4 8.10 |  | The quay edge stops him like a kerb; no passing through walls or bodies. |
| A21.17 | Clear access rules for closed buildings or locked regions | covered | 1.1.3 FIT-G10 2.2.6 |  | Locked door says so; opening hours and private labels set who may enter. |
| A21.18 | Indoor layouts that permit both navigation and intended encounters | covered | 4.3.1 4.3.2 FIT-P34 1.1.3 |  | Rooms built to the room kit with enterable counts; nothing inside Mickey's holds him. |
| A22.01 | Complete visible surfaces without holes or missing faces | unreal | 5.10 5.3.1 |  | Gate says no visible fault; no check named for holes or missing faces. |
| A22.02 | Appropriate detail at normal viewing distance | unreal | 5.11.4 5.10 |  | Triangle caps and 512 px/m at walking distance; judged against the Hook sheet. |
| A22.03 | Textures that do not stretch conspicuously | unreal | 5.11.4 |  | Texel density figures set; stretch test not named. |
| A22.04 | Texture scale consistent with real object size | unreal | 5.11.4 5.3.2 |  | Texel density and real-value calibration set. |
| A22.05 | Materials distinguishable as wood, metal, glass, cloth and stone | unreal | 5.3.2 5.11.4 |  | Shared surface material classes and photographs; look judged against the Hook sheet. |
| A22.06 | Object edges that do not all look infinitely sharp | unreal | none |  | Needs an edge-bevel and edge-wear standard for hard edges, judged against the Hook sheet. |
| A22.07 | Buildings and props visibly grounded rather than floating | unreal | 4.1.5 5.3.1 |  | Street build rules and kit pivots at sill or bottom face; no float check named. |
| A22.08 | Believable joins between walls, floors, roofs and terrain | unreal | 5.11.4 5.3.1 |  | Kit grid and fit rule: pieces within 10 per cent, pivots at sill. |
| A22.09 | No conspicuous flickering between overlapping surfaces | unreal | none |  | Needs an overlapping-surface flicker check (z-fighting) in the packaged walk. |
| A22.10 | Variation that disguises obvious repeated components | unreal | 5.11.4 |  | Kit variety: at least 15 distinct meshes per front, at most 10 per cent used once, checked by script. |
| A22.11 | Wear and dirt consistent with use and exposure | unreal | 5.3.2 5.11.4 |  | Grime strategy and wear decals set, calibrated to wet overcast photographs. |
| A22.12 | Furnishing and clutter consistent with a place's function | covered | 4.3.1 FIT-P52 4.4 |  | partly: office and drawers have written contents; no general rule per room type. |
| A22.13 | Signs and labels that are readable when they matter | covered | 4.1.3 6.9 4.4 |  | Every door numbered and every street named; signs made period-correct. |
| A22.14 | Period and setting consistency in conspicuous objects | covered | 4.9 4.4 4.6.1 5.10 |  | Late-analog 1990 detail, 1990 street furniture and fictional cars checked against dated photographs. |
| A22.15 | Objects that remain recognisable across lighting conditions | unreal | none |  | Needs a day, night and wet screenshot check of landmark props for recognisability. |
| A22.16 | Detail changes with distance that do not cause conspicuous shape popping | unreal | 5.11.4 |  | partly: LOD rule (each about half, none above 0.6 of the last); no popping test. |
| A22.17 | Interior dressing that survives viewing from both directions | unreal | 5.11.4 |  | partly: interior standards exist for rooms behind glass; no check from both sides. |
| A23.01 | Lighting that establishes readable shapes and space | unreal | 5.4.1 5.4.2 5.10 |  | Exposure, lamp pools and floor of visibility, judged against the Hook sheet. |
| A23.02 | Shadows connecting people and objects to their surroundings | unreal | 5.4.2 5.11.4 |  | Shadow-casting lights capped at 6 in view; window lamps cast within 15 m. |
| A23.03 | Shadows that broadly follow moving characters and lights | unreal | 5.11.4 5.4.2 |  | Sun cascades and shadow lights set; moving-character shadow check not named. |
| A23.04 | No major light leaking through solid walls | unreal | none |  | Needs a night walk check for light leaking through walls and window frames. |
| A23.05 | Indoor light levels that differ plausibly from outdoors | unreal | 5.4.1 5.4.2 |  | partly: day exposure and night pools set; no interior light levels. |
| A23.06 | Exposure changes that do not blind the player during ordinary transitions | unreal | 5.4.1 |  | Exposure pin is fixed (4.0 day, 0.4 night), so no auto-exposure flash; doorway transition not tested. |
| A23.07 | Dark areas that remain playable under the intended rules | covered | 1.4.2 5.4.2 6.1.4 | G214 | partly: Tom and ground 5 m round him always visible above a floor; floor has no number (G214). |
| A23.08 | Visible lamps whose surroundings respond to their light | unreal | 5.4.2 5.11.4 4.4 |  | Lamp pools about ten times the fill; lit windows; lights capped. |
| A23.09 | Switchable lights whose appearance and illumination change together | unreal | 2.1.1 5.4.2 |  | Lit window means somebody home; no rule that glow and light switch together. |
| A23.10 | Reflections that broadly agree with the environment | unreal | 5.3.3 5.3.4 |  | Wet street mirrors sky and buildings; shop glass shows the street. |
| A23.11 | A sensible solution for player visibility in mirrors where mirrors are usable | unreal | none |  | No usable mirror in the design (car rear window is a camera turn, 1.2.2); Unreal would need Tom in shop-glass reflections. |
| A23.12 | Glass that behaves consistently as transparent, reflective or obscured | unreal | 5.3.4 | G212 | Glass shows sky and street; no crack state or reflection quality set. |
| A23.13 | Stable image edges without distracting shimmer | unreal | 8.3.1 |  | Upscaler listed in settings; no anti-alias choice or shimmer test. |
| A23.14 | Motion rendering without severe ghost trails | unreal | 8.3.1 |  | Upscaler listed; no ghosting test on cars and moving people. |
| A23.15 | Consistent colour and brightness across gameplay and cutscenes | unreal | 5.4.3 5.8.2 | G215 | One colour grade shared by browser and Unreal; grade values still owed. |
| A23.16 | Distant scenery integrated with sky and atmosphere | unreal | 5.4.1 5.11.4 |  | Sky is a photograph; hill built as merged houses at distance. |
| A23.17 | Important targets remaining distinguishable amid visual effects | covered | AX-11 6.1.1 |  | partly: key objects distinct and never by colour alone; no test against rain, smoke or blood effects. |
| A24.01 | Vegetation moving appropriately in wind | unreal | none |  | Needs wind motion for trees and grass on the hill (vegetation ratio is set, motion is not). |
| A24.02 | Hanging fabric and similar objects responding to the environment | unreal | 5.11.4 |  | partly: coat tails and hems simulated; washing, awnings and signs not named. |
| A24.03 | Rain that does not visibly fall through ordinary roofs | unreal | 5.9 | G232 | Rain is named but not built; Unreal needs rain blocked under roofs and arches. |
| A24.04 | A change in rain sound when moving under cover | covered | 5.5.4 |  | partly: one rain value fades layers and rooms change echo; sheltered outdoor spots not named. |
| A24.05 | Wet surfaces looking different from dry ones | unreal | 5.3.3 5.11.4 |  | Wet street dark and glistening, roughness 0.06 against dry; dry-out 3 to 14 hours. |
| A24.06 | Plausible transitions into and out of weather | covered | 5.3.3 4.8 2.1.4 | G191 | partly: one wetness value and a drying time; ramp rules and weights not set. |
| A24.07 | Character or NPC responses to conspicuous weather where the presentation warrants them | covered | 2.1.4 5.5.4 |  | partly: rain empties the street and halves voices; no umbrella or hurry animation. |
| A24.08 | Water surfaces moving rather than appearing solid | unreal | 5.3.3 |  | Harbour water dark and reflection-led in research; no motion standard. |
| A24.09 | Ripples or splashes when entering water | unreal | none | G232 | Needs splash effect and sound for things and men put in the water (4.2.4). |
| A24.10 | Wakes from moving boats or swimmers | unreal | 4.6.2 |  | Boats are scenery (RULINGS 23 Sep); wakes needed only if scenery boats move. |
| A24.11 | Fire giving appropriate light, movement and sound | unreal | none | G232 | Fire is not in 5.9; the warehouse fire and Bonfire Night display need light, motion and sound. |
| A24.12 | Smoke and dust appearing to originate from their causes | unreal | 5.9 | G232 | partly: smoke named; dust and source tie not set. |
| A24.13 | Surface-specific debris from impacts | unreal | none | G232 | 5.9 lists broken glass only; needs debris per surface for blows, shots and car hits. |
| A24.14 | Temporary marks such as bullet holes or blood persisting long enough to connect cause and effect | covered | 5.3.2 2.19 5.9 |  | partly: blood and glass last until washed, rained off or mended; bullet holes not named. |
| A24.15 | Footprints or tracks where a visibly impressionable surface invites them | unreal | none |  | No tracks system; only needed for wet or muddy ground, a choice for Unreal. |
| A24.16 | Effects ending when their source ends | unreal | none |  | Needs a check that smoke, fire, spray and flashes end with their source. |
| A24.17 | Effects staying attached to moving sources | unreal | none |  | Needs a check that effects follow moving cars and people (exhaust, breath, smoke). |
| A24.18 | Weather and time changes that do not visibly reset at ordinary area boundaries | covered | 2.1.4 7.13 4.8 |  | Weather and clock are global values, not area state; streaming reset not tested (8.1.2). |
| A25.01 | Background activity beyond the player's immediate objective | covered | 2.1.1 2.1.2 2.1.3 3.7 |  | Routines, crowd windows, off-screen life and street happenings. |
| A25.02 | Ambient sound appropriate to the location | covered | 5.5.3 2.1.2 |  | Street beds, one-shots capped by place and hour, placed sources. |
| A25.03 | Population density that fits the place and time | covered | 2.1.2 FIT-G9 |  | People counts by hour and place, halved in rain. |
| A25.04 | People occupying different activities rather than all wandering | covered | 2.1.1 3.7 5.2.5 |  | partly: routines and happenings vary activity; work, smoke and talk idles are not built. |
| A25.05 | A plausible distinction between open and closed businesses, if operating hours exist | covered | 4.3.3 FIT-G10 2.2.6 |  | Shop hours, Sunday shut, back-room knock hours. |
| A25.06 | Continuity when leaving a small area and immediately returning | covered | 2.1.3 2.19 |  | Unseen people keep the same rules and things stay where left. |
| A25.07 | Consistent handling of dropped objects and casualties | covered | 2.16 2.19 1.6.7 RT2-11 |  | Bodies, dropped weapons and goods are remembered by who saw; things stay until mended. |
| A25.08 | Clear rules for replenishing loot or respawning enemies | covered | 2.7.5 2.16 |  | partly: shops restock weekly and a killed man stays dead; drawer refill rule not stated. |
| A25.09 | Events that do not visibly restart every time the player crosses a nearby boundary | covered | 2.1.3 3.7 |  | Happenings come from town state and hour, never dice or boundaries. |
| A25.10 | Day and night changes reflected in lighting and relevant activity, if time advances | covered | 4.7 2.1.1 5.4.2 |  | Light states and routines turn with the hour; people sleep, windows go dark. |
| A25.11 | A wait or sleep mechanism where schedules make waiting necessary | covered | 7.11 |  | Wait until a known appointment; sleep is a skip. |
| A25.12 | Safe handling of time skips with active missions or followers | covered | 7.11 2.1.3 GD-03 |  | A wait or sleep always stops for what the town has; job steps sleep and settle by the clock. |
| A25.13 | Ambient events that allow interruption and recovery | covered | 3.7 FIT-G6 |  | partly: happenings are small authored scenes Tom can step into; recovery after he ignores one not described. |
| A25.14 | Animals behaving like animals rather than stationary ornaments, where present | covered | FIT-P45 4.11.1 |  | Gulls rise, dogs bark, cats in yards. |
| A25.15 | Birds or small wildlife reacting to close movement or noise | covered | FIT-P45 |  | Gulls rise when someone runs at them and draw a glance. |
| A25.16 | No immediate repopulation directly in front of the player after a disturbance | missing |  |  | Needs a rule that crowd and happening spawns appear out of view or beyond a set distance from Tom. |
| A26.01 | A clear way to enter the intended vehicle and seat | covered | 1.2.3 6.1.1 |  | Door to seated 1.5 to 2.5 s with a prompt naming the car. |
| A26.02 | Entry animation that fits the door and seat | unreal | 1.2.3 5.2.3 |  | Timing set; animation fit to door and seat judged in Unreal. |
| A26.03 | Sensible entry when one side is obstructed | covered | 1.2.3 |  | From either side; a blocked door never traps him. |
| A26.04 | Driving controls that respond consistently | covered | 1.2.1 6.6 |  | Keys and pad reach the same course time within 10%. |
| A26.05 | Acceleration and braking appropriate to the vehicle | covered | 1.2.1 |  | 0 to 30 mph in 3.0 to 4.5 s; dry braking bands. |
| A26.06 | Steering that remains manageable across speeds | covered | 1.2.1 |  | Steering eases in 0.2 to 0.35 s; lane change settles within 1 s. |
| A26.07 | Reverse controls that are clear and usable | missing |  |  | Needs the reverse control and its prompt, and a test that reversing out of a wedge works on keys and pad. |
| A26.08 | Wheels rotating at a plausible rate | unreal | none |  | Needs a wheel spin rate tied to speed on the car asset. |
| A26.09 | Front wheels turning with steering where appropriate | unreal | none |  | Needs front wheels turning with steering on the car asset. |
| A26.10 | Suspension responding to road irregularities | unreal | 1.2.1 |  | Sway named in 1990 feel; no suspension standard. |
| A26.11 | Tyre contact that broadly matches the ground | unreal | 8.10 1.2.1 |  | partly: no launch or spin on a touch; wheel-to-ground contact check not named. |
| A26.12 | Engine sound responding to speed and load | covered | 5.5.5 |  | partly: engine note tracks speed within 5%, 28 to 210 Hz; load not named. |
| A26.13 | Skid and collision sounds responding to the actual event | covered | 5.5.5 5.5.2 |  | partly: squeal from 80% of grip; crash sound not specified. |
| A26.14 | Brake lights, headlights and reversing lights where the vehicle has them | covered | 1.2.4 5.4.2 |  | partly: headlights implied by the broken-lamp rule; brake and reversing lights not named. |
| A26.15 | A usable driving camera and rearward view | covered | 1.2.2 |  | Chase camera band, never in walls; B turns it to the rear window. |
| A26.16 | A way to leave the vehicle safely | covered | 1.2.3 |  | Out in under 2 s and immediate after a wreck. |
| A26.17 | Exiting that avoids placing the player inside walls or traffic | covered | 1.2.3 1.2.4 8.10 |  | partly: moves or can be left within 5 s; no rule for the exit spot beside walls or traffic. |
| A26.18 | Vehicle damage communicated visually or mechanically | covered | 1.2.4 |  | Stages by closing speed shown as dent, crumple, pull to one side, broken lamp. |
| A26.19 | Recovery from an overturned or irretrievably stuck vehicle | covered | 1.2.4 8.10 |  | partly: wedged car always backs out within 5 s and no launches; overturning not mentioned. |
| A26.20 | Traffic following plausible lanes and junction rules | covered | 4.5.1 | G186 | partly: lanes, IDM, 20 to 28 mph, stops behind people; junction rules not designed. |
| A26.21 | Traffic responding to obstructions and collisions | covered | 4.5.1 1.2.5 | G186 | partly: traffic halts for people and hoots; response to crashes not designed. |
| A26.22 | Pedestrians responding to approaching vehicles | covered | 1.2.5 2.1.5 |  | People look before stepping out and none within 23 m of a car at 30 mph. |
| A26.23 | Passengers remaining correctly seated during movement | covered | 1.2.7 1.2.8 |  | partly: crew and fares ride in the cab; seat and sway animation not stated. |
| A26.24 | A vehicle remaining where it was left under the game's persistence rules | covered | 2.19 1.2.9 7.8 |  | Things stay where left; wrecked cab off the road a day; save keeps the town. |
| A27.01 | Mounting and dismounting from plausible positions | missing |  |  | Decide in or out: no mount, horse or riding animal appears anywhere in the blueprint; none fits 1990 Hook, probably out |
| A27.02 | Mount movement whose gait matches its speed | missing |  |  | Decide in or out: no mount, horse or riding animal appears anywhere in the blueprint; none fits 1990 Hook, probably out |
| A27.03 | Mount turning and stopping that fit its body | missing |  |  | Decide in or out: no mount, horse or riding animal appears anywhere in the blueprint; none fits 1990 Hook, probably out |
| A27.04 | Mount avoidance of ordinary obstacles | missing |  |  | Decide in or out: no mount, horse or riding animal appears anywhere in the blueprint; none fits 1990 Hook, probably out |
| A27.05 | A usable way to call, locate or recover an owned mount | missing |  |  | Decide in or out: no mount, horse or riding animal appears anywhere in the blueprint; none fits 1990 Hook, probably out |
| A27.06 | Clear mount health, stamina or distress where those affect play | missing |  |  | Decide in or out: no mount, horse or riding animal appears anywhere in the blueprint; none fits 1990 Hook, probably out |
| A27.07 | Boats floating at a plausible height | out | 4.6.2 4.2.4 |  | RULINGS 23 Sep genre: boats and buses scenery; boats are scenery, never boarded or floated |
| A27.08 | Boat steering, acceleration and stopping appropriate to water travel | out | 4.6.2 4.2.4 |  | RULINGS 23 Sep genre: boats and buses scenery; no boat is steerable |
| A27.09 | Boarding and leaving without falling through the vessel | out | 4.6.2 4.2.4 |  | RULINGS 23 Sep genre: boats and buses scenery; no boarding of vessels |
| A27.10 | Movement that remains stable on a moving deck | out | 4.6.2 4.2.4 |  | RULINGS 23 Sep genre: boats and buses scenery; no moving deck to stand on |
| A27.11 | Public transport that clearly communicates boarding and destination | out | 4.6.2 |  | RULINGS 23 Sep genre: boats and buses scenery; no public transport to ride |
| A27.12 | Carried equipment and companions surviving transport transitions | covered | 1.2.3 1.2.7 1.2.8 1.6.9 |  | partly: cars only (crew and fares ride in the cab, items survive); boats and buses are out |
| A28.01 | Sounds coming from the direction of their source | missing |  |  | Needs a part saying a sound comes from its source's side (panning) with a test; blueprint sets only reach in metres |
| A28.02 | Sound direction changing correctly as the player turns | missing |  |  | Needs a test that sound direction follows Tom's facing or the camera; none written |
| A28.03 | Moving sources carrying their sounds with them | covered | 5.5.5 5.5.3 |  | partly: car and placed sources carry their sound by reach; no rule or test that a moving source's sound moves with it |
| A28.04 | Distant sources sounding quieter than nearby sources | covered | 5.5.3 2.2.4 1.4.3 |  | partly: every sound has a reach and loudness is reach in metres; no distance fall-off curve or test |
| A28.05 | Distant sources losing appropriate detail | missing |  |  | Needs a rule that far sources lose high detail (a distance filter), with a listening test |
| A28.06 | Walls and closed doors muffling relevant sounds | missing |  |  | Needs a muffling rule for walls and shut doors; rain cuts reach and rooms get reverb, but nothing dulls sound through walls |
| A28.07 | Openings providing a plausible route for sound | missing |  |  | Needs a rule that sound leaks through open doors and windows (a door left open carries a shout); none written |
| A28.08 | Room acoustics differing from open air | covered | 5.5.4 |  | SND-16 and SND-17: shared reverb swapped at the doorway and a room tone per room kind |
| A28.09 | Larger and smaller rooms sounding different where conspicuous | covered | 5.5.4 |  | partly: eight room kinds (office, caff, chapel and so on) each with its own tone; no size-based rule |
| A28.10 | Smooth acoustic transitions at room boundaries | covered | 5.5.4 |  | SND-16 crossfades the reverb over about 1 m of walking and at least 0.5 s |
| A28.11 | Large sources sounding spatially broad rather than like tiny points | missing |  |  | Needs a rule for wide sources (rain, a crowd, the quay) to play as beds, not point sounds |
| A28.12 | Above and below having useful audible distinction where supported | missing |  |  | Needs a rule for sound above and below (the flat over the office, stairs); only one level is described |
| A28.13 | A sensible listening position when the camera moves away from the character | missing |  |  | Needs a rule for where the ears sit (Tom or the camera, 3.1 m back); not stated |
| A28.14 | No distant conversation playing at intimate, full-volume closeness | covered | 5.5.3 5.5.7 GD-02 |  | partly: far voices capped (3 by day) and talk lowers the beds; no rule on how loud a far conversation may be |
| A28.15 | No obvious snapping between left and right as a source passes nearby | missing |  |  | Needs a smooth-pan rule and a drive-past test for passing cars; linked to panning, which is not specified |
| A29.01 | Footsteps synchronised with foot contact | covered | 5.5.1 |  | partly: steps by surface and gait; no test that the sound lands on foot contact |
| A29.02 | Different footstep sounds on different surfaces | covered | 5.5.1 |  | SND-05 to 07: at least seven surfaces, three shoe kinds |
| A29.03 | Footstep cadence changing with movement speed | covered | 5.5.1 1.4.3 |  | walk, run and slow walk differ; a tester with the picture off can tell a walk from a run |
| A29.04 | Appropriate landing sound | out | OUT-08 |  | OUT-08 no jump or climb: only the 0.8 s vault, which lands as a step (OUT-08 reads wider than the ruling, which says only no jump) |
| A29.05 | Clothing and equipment movement where audible | missing |  |  | 5.5.1 is called foley but sets only footsteps; needs coat rustle and holdall sounds |
| A29.06 | Breathing or exertion appropriate to strenuous activity | covered | 1.3.7 5.5.6 5.9 |  | partly: breath shows in fights and as an effect; no rule for Tom's breathing when running |
| A29.07 | Doors sounding when they move and latch | covered | 5.5.2 |  | doors creak, hit and latch; G217 has no set size |
| A29.08 | Pickups and item handling providing subtle confirmation | missing |  |  | Needs a small sound standard for taking, searching and putting things down; none written |
| A29.09 | Collision sounds appropriate to the materials involved | covered | 5.5.2 1.2.4 |  | partly: doors and glass; no material table for car hits on poles, bins, walls |
| A29.10 | Breakage sounds matching the object | covered | 5.5.2 |  | partly: forced door and broken glass only; no other breakage |
| A29.11 | Weapon handling, firing and reloading sounds aligned with actions | covered | 5.5.6 1.3.10 RT-10 | G221 | partly: shot, echo and four fight layers timed; reload and draw sounds not set |
| A29.12 | Damage and pain sounds fitting the affected character | covered | 5.5.6 5.6.1 |  | pain cry after contact, voices chosen per character; no per-type pain set |
| A29.13 | Machines sounding active only while operating | covered | 5.5.5 5.5.3 |  | partly: engine follows speed and placed sources name an owner; no rule for other machines going quiet when off |
| A29.14 | Splash sounds matching water contact | missing |  |  | Needs a splash sound for things thrown in and men put in the water (4.2.4); none written |
| A29.15 | Variation that prevents repeated actions sounding mechanically identical | missing |  | G221 | Needs a no-repeat and variant-count rule per sound; G221 notes no set size for fight sound |
| A29.16 | No double-triggered sound for a single event | missing |  |  | Needs a test that one event fires one sound (mix record check); none written |
| A29.17 | No continued footsteps after the character stops | missing |  |  | Needs a test that steps stop when Tom stops; none written |
| A29.18 | Sound events occurring when the action happens rather than noticeably late | covered | 5.5.6 |  | partly: fight layers have timing limits (impact within 0.034 s of contact); other events have none |
| A30.01 | Important speech intelligible over ambience and action | covered | 5.5.7 AX-04 |  | bed at least 6 dB under a spoken line; 'voices clear' switch adds 6 dB |
| A30.02 | Consistent dialogue loudness across speakers | covered | 5.5.7 | G222 | partly: loudness -23 LUFS over 30 min and the quietest lead voice sets the mix; G222 no lead level |
| A30.03 | Distinct voices that help identify recurring characters | covered | 5.6.1 3.2.1 |  | a voice chosen per character, judged by ear, cast on his yes |
| A30.04 | Speech fitting the speaker's emotional situation | missing |  |  | Needs a standard for delivery to fit the speaker's mood (live and prepared lines); only voice choice is set |
| A30.05 | No clipping or harsh overload during loud events | covered | 5.5.7 AX-04 |  | true peak at most -1 dBTP; loudest sound at most 20 LU above; loud noise softening switch |
| A30.06 | No audible clicks at the start or end of loops | missing |  |  | Needs a seamless-loop test for beds and music; beds are loops but no click check is written |
| A30.07 | Music transitions that do not cut abruptly without intention | covered | 5.7.1 FIT-P09 |  | partly: music is heard only from in-world sources so there is no score to cut; Q11 short score undecided |
| A30.08 | Combat music starting and ending with the encounter | covered | 5.5.6 5.7.1 |  | by design no combat music: 'never combat music', nothing starts or changes for a fight or chase |
| A30.09 | Exploration music that does not overwhelm ordinary interaction | covered | 5.7.1 5.5.7 |  | music only where it plays in the world; silence is the commonest music |
| A30.10 | Appropriate silence and contrast rather than constant maximum intensity | covered | 5.5.7 5.7.1 |  | 'silence is the commonest music' |
| A30.11 | Avoidance of conspicuously short musical loops | missing |  | G226 | Needs a minimum loop length for radio and in-world pieces; none set and no song list |
| A30.12 | Important sounds remaining audible in a crowded mix | covered | 5.5.3 5.5.7 |  | at most 40 sounds at once, spawn caps by hour, voice leads the mix |
| A30.13 | No dialogue continuing from a dead or departed speaker without explanation | missing |  |  | Needs a rule that a line stops when its speaker falls, leaves or is killed mid-line; none written |
| A30.14 | Audio pausing, resuming and loading consistently with the game state | missing |  |  | needs a rule that game sound pauses or ducks with the pause menu and when the window loses focus (6.x or 8.x) |
| A30.15 | Consistent presentation across headphones and supported speaker layouts | missing |  |  | Needs a headphone and speaker-layout check; AX-04 has only a mono switch |
| A30.16 | Radio or other in-world music sounding attached to its source | covered | 5.7.1 FIT-P09 |  | music only where it plays in the world: caff radio, window, chapel organ |
| A31.01 | A clear way to start and leave a conversation | covered | 6.7 3.6.1 2.5.2 |  | speak to a named person; Leave always offered |
| A31.02 | Acknowledgement when the player initiates speech | covered | 5.6.3 5.2.4 3.6.1 |  | a glance and a thinking sound before the answer |
| A31.03 | Conversational distance and facing that look plausible | covered | 5.2.4 1.1.2 |  | Tom stands about 1.5 m from a speaker, both facing |
| A31.04 | Mouth movement synchronised approximately with speech | unreal | 5.2.4 5.2.9 8.12.2 | G203 | was covered; mouths follow loudness (live) or audio-driven (prepared); G203 no accuracy number |
| A31.05 | Correct association between the speaking voice and visible character | covered | 5.6.1 AX-02 |  | voice cast per character, speaker's name in subtitles |
| A31.06 | Dialogue choices that communicate the intended meaning | covered | 6.7 3.6.5 3.6.6 |  | decision lines are the exact text Tom says; suggested lines about four words |
| A31.07 | A distinction between asking for information and making a consequential commitment | covered | 3.6.5 6.7 |  | only a plain yes is taken; anything irreversible asks twice |
| A31.08 | Choice selection that does not accidentally confirm during menu navigation | covered | 6.7 AX-06 |  | only a plain yes is taken and nothing destructive sits one press from Resume |
| A31.09 | A predictable response to walking away | missing |  |  | Needs a rule for Tom walking off mid-talk (talk ends, person remembers); only haggling says walking away is remembered |
| A31.10 | A predictable response to combat interrupting speech | missing |  |  | Needs a rule for a fight or shout breaking in on talk; standing talk stops the clock so it is not covered |
| A31.11 | Important information recoverable after interruption | covered | 6.2.2 6.2.3 6.2.1 |  | what Tom was told is written in the Day book and Open page |
| A31.12 | Conversation state that does not repeat completed introductions endlessly | covered | 2.3.1 2.12.4 3.6.4 |  | memory is permanent per person and greetings follow regard, so no repeated introductions |
| A31.13 | Dialogue that acknowledges relevant completed actions | covered | 2.3.1 3.6.2 2.12.4 |  | people speak from what they saw and were told; claim check on live lines |
| A31.14 | Dialogue that does not refer to absent or dead characters as visibly present | covered | 3.6.2 2.16 |  | claim check holds speech to the town's state; a missing man is the town's question |
| A31.15 | Ambient and important dialogue prevented from talking over one another excessively | covered | 5.5.7 GD-02 |  | talk lowers beds; everyday street talk at most every 45 s |
| A31.16 | Subtitles matching the actual spoken line | covered | 6.1.2 AX-02 8.12.2 |  | subtitle shows only with its audio; every line logged in a 2-hour soak |
| A31.17 | Appropriate pauses and turn-taking | covered | 5.6.3 3.6.1 |  | partly: reply within 2 s or the written line plays; no pause-length rule |
| A31.18 | No conspicuous silence while a character appears to be waiting for a missing line | covered | 5.6.3 8.6.1 |  | a line slower than 8 s is dropped for an in-character brush-off; offline written lines carry on |
| A32.01 | A clear distinction between a cutscene and interactive control | covered | 5.8.2 5.8.3 7.1 |  | few short scenes; control at 0:20 after the ferry shot; staged talk keeps control |
| A32.02 | Camera placement that shows the intended action | covered | 5.8.2 5.8.1 | G229 | partly: only the ferry shot is specified; no shot-composition standard |
| A32.03 | Characters and props arriving in the correct positions | missing |  |  | Needs a check that people and props start a staged scene in place and end at the right marks; none written |
| A32.04 | Player equipment and appearance carried into scenes where appropriate | missing |  |  | Needs a rule that scenes show Tom's current coat and carried items (1.6.10); none written |
| A32.05 | Facial and body performance consistent with the dialogue | covered | 5.2.4 5.2.9 5.2.6 |  | mouths follow the voice and body language of knowing is ruled |
| A32.06 | A way to pause where the presentation permits it | covered | 6.4 AX-10 |  | Esc pauses everywhere |
| A32.07 | A way to skip already-seen scenes | covered | 5.8.2 |  | every scene is skippable |
| A32.08 | Protection against accidentally skipping an entire scene | missing |  |  | Needs a confirm or hold-to-skip so one stray key cannot skip a scene; none written |
| A32.09 | Subtitles that survive cinematic framing and letterboxing | missing |  |  | Needs subtitles tested inside any cinematic framing; 6.1.2 tests four window sizes only |
| A32.10 | Gameplay resuming in a sensible position and facing | missing |  |  | Needs a rule that control returns at a usable place and facing after a scene; none written |
| A32.11 | No damage or enemy activity during a scene that denies player control unless deliberately communicated | missing |  |  | Needs a rule on danger during staged and moving talk (RT2-20 keeps the world running); none written |
| A32.12 | Correct state changes even when a scene is skipped | covered | 1.2.8 5.8.2 3.5.6 |  | partly: a skipped ride passes its exact drive time and job states are saved; no test of a skipped scene's state |
| A32.13 | No prolonged loading hidden behind a frozen character or black screen without feedback | unreal | 8.5 8.1.3 8.1.2 | G270 | progress shown while the street prepares; trips past the soft edge load nothing; G270 no load limit |
| A33.01 | A clear current objective or understandable self-directed goal | covered | 6.2.3 3.5.6 |  | Open lists jobs and appointments by person and landmark |
| A33.02 | A way to review the objective after forgetting it | covered | 6.2.3 6.2.2 6.5 |  | Ledger Open and Day book; hints again |
| A33.03 | Clear distinction between mandatory and optional tasks | missing |  |  | Needs a way for Open to show which jobs the story needs and which are optional; not stated |
| A33.04 | Objective progress updating after relevant actions | covered | 3.5.6 6.2.2 6.1.3 |  | each step change is saved and written in the Day book within a game minute |
| A33.05 | Completion acknowledged rather than silently recorded | covered | 6.2.2 6.1.3 7.9 |  | each step done or failed is a Day book line; the town can talk about it |
| A33.06 | Rewards actually delivered and explained | covered | 6.2.4 2.7.1 2.7.5 |  | money said in words after a job; payment follows the debtor's purse |
| A33.07 | Failure conditions communicated before they matter where possible | covered | 3.5.6 CLK-04 7.11 |  | windows known at least 5 game hours before they open; 'wait until' offered |
| A33.08 | A clear response to leaving an active mission area | covered | 3.5.6 |  | steps sleep while Tom is away and settle by the clock |
| A33.09 | Tasks that survive doing valid steps in an unexpected order | covered | GD-03 |  | a step met early, late or by another route counts as met; tester runs all orders |
| A33.10 | Recognition of an item already owned when it is requested | covered | GD-03 |  | a step already met counts as met |
| A33.11 | A solution when a required character is absent, dead or obstructed | covered | GD-03 RT2-05 2.16 |  | job moves to failed in a state the town can talk about; never stuck |
| A33.12 | Protection against permanently losing an indispensable quest item | covered | RT2-13 1.6.9 GD-03 |  | a taken envelope becomes a debt; stored items survive; no job waits on an impossible step |
| A33.13 | Required interactions remaining usable despite ordinary world changes | covered | GV-04 3.5.6 |  | places stay open; every lock has three keys |
| A33.14 | A way to restart or recover a broken activity | covered | GD-03 GV-05 8.10 |  | no job ends stuck; nobody stuck over 5 s; no blocking fault at release |
| A33.15 | Clear communication of time limits | covered | 3.5.6 CLK-04 6.1.5 |  | job windows on the town clock and a known hour anywhere within 3 s |
| A33.16 | Dialogue and markers agreeing on the destination | covered | 6.9 3.5.6 |  | every job gives an address and landmark, two sources of direction |
| A33.17 | Markers resolving to reachable interaction points | out | OUT-09 6.9 |  | OUT-09 no markers; reachability is tested by newcomers reaching ten named places unaided |
| A33.18 | Sensible handling of multiple simultaneous missions | covered | 6.2.3 3.5.6 3.5.7 |  | Open lists every live job, debt and appointment |
| A33.19 | Completed objectives not continuing to issue obsolete instructions | covered | 6.2.2 6.2.3 3.5.6 |  | Open lists live items; finished ones go to the Day book and wrong beliefs are struck through |
| A33.20 | A reason to explore beyond the main route | covered | 3.3 3.7 7.12 GD-02 |  | side stories, street happenings and something within 30 s by day |
| A33.21 | Activity variety appropriate to the game's promised scope | covered | 7.14 7.16 GD-08 |  | variety, pastimes and the job catalogue per act |
| A34.01 | Health or equivalent survival information readable when needed | covered | 1.3.7 RT-11 |  | no health bar by ruling intent: posture, breath, guard, blood and limp show state |
| A34.02 | Ammunition or resource information readable before an action fails | missing |  |  | Decide in or out: 1.3.10 says no ammunition count, so needs a way to see a revolver is empty (cylinder, dry click) |
| A34.03 | Clear current weapon, tool or ability state | covered | 1.6.9 6.2.3 1.3.10 |  | partly: Open lists what he carries; a drawn gun and held item are seen; no on-screen state |
| A34.04 | Feedback when an action is on cooldown or otherwise unavailable | covered | 1.3.2 1.1.3 FIT-P34 |  | OUT-06 no skills or abilities, so no cooldowns |
| A34.05 | Interaction prompts that do not obscure the object | covered | 6.1.1 AX-01 |  | partly: prompt held 0.2 s and sized for reading; no placement rule against hiding the object |
| A34.06 | Aiming indicators visible against varied backgrounds | covered | 1.3.10 AX-05 |  | partly: no crosshair; an optional dot is off by default; no contrast test |
| A34.07 | Damage direction or an equivalent way to locate unseen danger | covered | 1.3.2 8.4.1 1.5.2 |  | partly: blows read in the body, shouts and cars shown by sound-shown; no on-screen direction cue by design |
| A34.08 | Distinguishable friendly, hostile and neutral indicators where used | out | OUT-09 2.4.3 |  | OUT-09 no markers: no friend or foe icons; people read by posture and the seeing outline 1.4.6 |
| A34.09 | Status-effect indicators that explain their meaning | covered | 1.3.7 RT-11 1.3.11 |  | OUT-06 no meters or status icons; hurt and beaten show in his body only |
| A34.10 | Notifications that remain long enough to read | missing |  |  | Needs a minimum on-screen time for the belief line and toasts; none set |
| A34.11 | Notification handling that does not bury urgent information | covered | 6.5 6.1.3 |  | partly: never two hints within 12 s; no priority rule for urgent text |
| A34.12 | No overlapping subtitles, prompts and objective text | covered | 6.1.2 AX-01 |  | partly: subtitles tested for no overlap at four window sizes; prompts and belief line not in that test |
| A34.13 | Appropriate removal or reduction of HUD during noninteractive scenes | missing |  |  | Needs a rule hiding prompts and the belief line in staged scenes; only photo mode hides the interface |
| A34.14 | A clear indication when the world continues running behind a menu | missing |  |  | RT-18 says Ledger and map stop Tom but not the town; needs a visible sign that the town goes on |
| A34.15 | UI values that match actual gameplay state | covered | 6.2.4 6.2.1 6.1.5 |  | money, people and time are stated from real state; nothing on screen Tom could not know |
| A34.16 | A way to reduce unnecessary HUD elements where supported | covered | AX-02 6.5 6.1.2 |  | partly: screen already minimal; street-chatter subtitles and hints can be turned off |
| A35.01 | A map that opens promptly and returns cleanly to gameplay | covered | 6.3 RT-18 |  | map opens with Comma and stops Tom, not the town; no timing standard |
| A35.02 | A visible player position | missing |  |  | Needs Tom's own position drawn on the paper map or a ruling that it is not; 6.3 marks only places |
| A35.03 | A clear indication of facing or travel direction | missing |  |  | Needs facing shown with Tom's position on the paper map; not stated |
| A35.04 | Useful map scale and zoom | missing |  | G238 | Needs a map scale and zoom rule; the map is drawn but its extent and zoom are not set |
| A35.05 | Panning with the current input device | covered | 6.6 6.3 |  | partly: every verb reachable by keys, mouse and pad; map panning not described |
| A35.06 | Legible labels and distinguishable icons | covered | AX-01 6.3 |  | partly: text size and contrast rules cover labels; no icon-distinction rule |
| A35.07 | A legend or explanation for unfamiliar symbols | missing |  |  | Needs a key to the map's marks; none written |
| A35.08 | Selection of overlapping icons | missing |  |  | Needs a rule for picking among overlapping marks; none written |
| A35.09 | A way to place and remove a personal waypoint | out | OUT-09 |  | OUT-09 no minimap, waypoints or markers |
| A35.10 | A route or directional cue that follows reachable paths where supplied | out | OUT-09 6.9 |  | OUT-09 no route lines; directions come from people and landmarks |
| A35.11 | Recalculation after leaving a suggested route | out | OUT-09 |  | OUT-09 no route to recalculate |
| A35.12 | Height or floor distinction where a flat marker would mislead | missing |  |  | Needs a floor rule for the flat above the office and multi-storey rooms on the map; not stated |
| A35.13 | Clear distinction between discovered and undiscovered places | covered | 6.3 |  | map marks only places he has been or been told of; G238 gives no rule for 'told of' |
| A35.14 | Clear distinction between completed and incomplete activities | covered | 6.2.2 6.2.3 |  | partly: Open and Day book split live from done; the map does not show job state |
| A35.15 | Navigation aids that remain consistent with world signs and names | covered | 6.9 4.1.3 6.3 |  | street plates, door numbers and landmarks match the Ledger's names |
| A35.16 | A journal that preserves useful task and story information | covered | 6.2.2 6.2.3 6.10 |  | Day book and Open keep every job step and letter |
| A35.17 | A way to review recently acquired notes or clues | covered | 6.2.2 6.10 |  | Day book lists events in order; letters go into the Ledger |
| A35.18 | Fast-travel eligibility, cost and restrictions explained where fast travel exists | missing |  |  | Decide in or out: no fast travel is designed or ruled out; OUT-05 makes distant districts time skips and 1.2.8 skips a crew ride |
| A35.19 | Fast travel arriving at a safe, usable position | missing |  |  | Decide in or out: no fast travel is designed or ruled out; OUT-05 makes distant districts time skips and 1.2.8 skips a crew ride |
| A35.20 | Travel preserving relevant equipment, followers and mission state | missing |  |  | Decide in or out: no fast travel is designed or ruled out; OUT-05 makes distant districts time skips and 1.2.8 skips a crew ride |
| A36.01 | A reliable record of what the player owns | covered | 1.6.9 6.2.3 |  | Open lists what he carries; stored items survive save, load and skipped time |
| A36.02 | Pickup feedback identifying what was acquired | missing |  |  | Needs an on-screen or spoken acknowledgement of what was taken; taking is one press with no feedback described |
| A36.03 | Item names, quantities and useful descriptions | covered | 6.2.3 1.6.9 |  | partly: carried things named in words; no item descriptions or quantities rule |
| A36.04 | Clear distinction between usable, equippable, valuable and quest items | missing |  |  | Needs item kinds (usable, valuable, hot, quest) told apart in Open; only the hot mark exists |
| A36.05 | Sorting or filtering sufficient for the expected inventory size | covered | 1.6.9 |  | carrying is limited to two under the coat and one in hand, so no sorting is needed |
| A36.06 | Consistent stacking of identical items | missing |  |  | Needs a stacking rule for like items (cigarettes, notes, keys); none written |
| A36.07 | Quantity selection for moving or discarding stacks | missing |  |  | Needs a rule for how many of a stack to drop or hand over; none written |
| A36.08 | A clear equipped state | covered | 1.6.9 1.6.10 1.3.10 |  | partly: held and under-coat items and worn outfit are seen; no menu state |
| A36.09 | Comparison with currently equipped gear | out | OUT-06 |  | OUT-06 no stats, so gear has nothing to compare |
| A36.10 | Equipment restrictions explained before selection | missing |  |  | Needs a way to tell why an item cannot be carried or worn; only 'wrong clothes for the door' is shown by people |
| A36.11 | Immediate gameplay and visual effects from equipping | covered | 1.6.10 1.4.4 |  | each outfit changes how strangers speak and which doors open |
| A36.12 | Quick access to frequently used items | covered | 6.6 1.3.10 |  | partly: fixed keys for torch, stone, cigarette, watch and a held key draws a gun; no general quick slot |
| A36.13 | Consistent consumption of single-use items | missing |  |  | Needs a single-use rule (torch battery, cigarettes, envelope handed over); none written |
| A36.14 | A clear capacity or weight rule if capacity is limited | covered | 1.6.9 |  | two under the coat and one in the hand |
| A36.15 | Feedback when a pickup fails because the inventory is full | missing |  |  | Needs feedback when Tom's hands and coat are full; none written |
| A36.16 | A way to drop, store or otherwise manage unwanted items | covered | 1.6.9 1.6.7 |  | office drawer, yard shed and tin for storing; drain, dock and quay for disposing |
| A36.17 | Protection against accidental destruction of valuable items | missing |  |  | Needs a confirm before throwing away or handing over something valuable; talk asks twice but items do not |
| A36.18 | Clear ownership or theft status where relevant | covered | 1.6.3 2.7.6 |  | hot mark on stolen goods and the owner never forgets them |
| A36.19 | Containers retaining sensible contents after being opened | covered | 1.6.2 FIT-P52 1.6.9 |  | partly: contents authored per job and an ordinary drawer's contents set; no rule for refilling |
| A36.20 | Inventory state surviving death and reload according to the stated rules | covered | RT2-13 7.8 7.9 |  | Tom cannot die; beating may rob him of paper money and held items; reload gives the same next hour |
| A36.21 | Menus remaining usable while quantities change | missing |  |  | Needs a check that Ledger pages stay usable while the town changes them; none written |
| A37.01 | Clear prices before purchase | covered | 2.7.8 2.7.5 |  | prices spoken by the seller; no table by design |
| A37.02 | A visible current balance | covered | 6.2.4 |  | money said in words: what he has, the tin, what is owed |
| A37.03 | Distinct buying and selling states | covered | 2.7.5 2.7.6 |  | shops buy, haggle or refuse; fences pay a fraction |
| A37.04 | Preview of the actual transaction quantity and total | missing |  |  | Needs a spoken total for more than one item; the shop list is one item at a time with a three-offer haggle |
| A37.05 | Insufficient-funds feedback that explains the shortfall | covered | RT-14 2.7.8 |  | partly: an offer above what Tom carries fails in character; no wording standard for buying |
| A37.06 | Transactions occurring once per confirmed purchase | missing |  |  | Needs a test that one confirmed purchase charges once; none written |
| A37.07 | Clear distinction between sale value and purchase price | covered | 2.7.6 2.7.5 |  | fence pays about a third of retail; shop prices are the seller's list |
| A37.08 | Recovery from accidental sale where a buyback system is provided | missing |  |  | Decide in or out: no buyback designed; needs a ruling or a rule that a sold item can be bought back from the buyer |
| A37.09 | Shop stock and availability behaving consistently | covered | 2.7.5 FIT-G10 |  | shops keep hours, restock weekly and market day empties them |
| A37.10 | Crafting recipes showing ingredients and output | out | OUT-07 |  | RULINGS 23 Sep: no crafting; recipes do not exist |
| A37.11 | Clear indication of which ingredients are missing | out | OUT-07 |  | RULINGS 23 Sep: no crafting; missing ingredients do not exist |
| A37.12 | Preview of upgrade effects before spending resources | out | OUT-07 |  | RULINGS 23 Sep: no crafting; upgrade previews do not exist |
| A37.13 | Crafting consuming the stated ingredients and producing the stated result | out | OUT-07 |  | RULINGS 23 Sep: no crafting; crafting results do not exist |
| A37.14 | Safe handling of crafting while inventory capacity is limited | out | OUT-07 |  | RULINGS 23 Sep: no crafting; crafting with limited capacity do not exist |
| A37.15 | Clear distinction between repair, upgrade and replacement | out | OUT-07 1.2.9 |  | OUT-07 no crafting or upgrades; cars are mended or replaced at the yard (1.2.9) |
| A37.16 | No unexplained loss of money or materials when an operation is cancelled | missing |  |  | Needs a test that a cancelled haggle or sale costs nothing; walking away is remembered but loss is not tested |
| A38.01 | Clear feedback when experience or progression is earned | covered | 7.7 2.12.1 2.12.4 |  | rise shown in what people call him and how they greet him |
| A38.02 | A readable current level or equivalent advancement state | covered | 7.7 6.2.5 OUT-06 |  | position said in words and in Tom's reading, never a number |
| A38.03 | Explanation of what an upgrade actually changes | covered | 2.12.2 2.12.3 |  | partly: the rung table says what opens at each step; no upgrades by design |
| A38.04 | Clear prerequisites and costs | covered | 2.12.2 2.7.8 |  | rung table gives what is needed; costs are spoken prices |
| A38.05 | Immediate application of purchased abilities | out | OUT-06 |  | OUT-06 no skills, perks or abilities to buy |
| A38.06 | Instruction for newly unlocked actions | covered | 6.5 |  | interface and hints appear piece by piece at first need |
| A38.07 | Visible acknowledgement of meaningful milestones | covered | 7.7 3.1.1 3.1.2 |  | greetings, property and act ends mark milestones |
| A38.08 | Customisation previews before commitment | missing |  |  | Decide in or out: no preview of clothes before buying; the blueprint would need a try-on or shop-mirror line in 1.6.10 |
| A38.09 | Character creation that can be inspected under useful lighting | out | OUT-01 |  | OUT-01 player is Tom Nowak throughout; no character creation |
| A38.10 | Appearance choices that remain recognisable in gameplay | covered | 1.6.10 5.1.4 |  | clothes change how the town reads Tom |
| A38.11 | Difficulty descriptions that say what changes | covered | 7.10 AX-08 |  | each assist has a plain line on what it changes |
| A38.12 | Appropriate acknowledgement when difficulty is changed | missing |  |  | Needs a short confirmation when an assist is switched; 7.10 tests each changes only its own thing |
| A38.13 | A clear distinction between cosmetic and mechanical choices | missing |  |  | needs a way for the player to learn what a coat or outfit changes (who notices, what it hides) in 1.6.10 |
| A38.14 | Explanation of irreversible choices or respec limits | covered | 6.7 OUT-12 |  | game says what is permanent before it happens; irreversible acts ask twice |
| A38.15 | Progression and unlocks surviving reload | covered | 7.8 2.12.1 2.3.1 |  | everything is saved including rung and memories |
| A39.01 | A clear explanation of when progress is saved | missing |  |  | Needs a plain line telling the player when the game saves; autosave rules exist but nothing says it to him |
| A39.02 | Autosaving at sensible milestones | covered | 7.8 8.11.3 AX-07 | G352 | after every deed, consequence and job step; G352 no longest gap |
| A39.03 | A visible indication while a save is in progress | missing |  |  | Needs a visible 'saving' sign; none designed |
| A39.04 | Manual saving or an explicitly communicated alternative | covered | 7.8 AX-07 6.4 |  | at least eight manual slots plus three rotating autosaves |
| A39.05 | Clear reasons when saving is temporarily unavailable | covered | 7.8 |  | by design never refused, even in a fight, so no reason message needed |
| A39.06 | A clear distinction between checkpoint, autosave and manual save | covered | 7.8 AX-07 |  | partly: manual slots and rotating autosaves are told apart; no checkpoints exist |
| A39.07 | Save entries identifiable by time, location or progress | covered | AX-07 6.4 7.8 |  | picture, day, hour, place and rung in words |
| A39.08 | Confirmation before overwriting or deleting a save | missing |  |  | Needs a confirm before overwriting or deleting a slot; AX-06 only bars a destructive choice next to Resume |
| A39.09 | Separate playthroughs or profiles not silently overwriting each other | missing |  |  | Needs a rule that New game never overwrites existing slots or autosaves; no profile concept |
| A39.10 | Player location restored to a usable position | covered | 7.8 8.11.3 8.10 |  | reload gives the same next hour; nobody stuck over 5 s |
| A39.11 | Inventory and equipment restored consistently | covered | 7.8 1.6.9 |  | carried and stored items survive save and load |
| A39.12 | Mission progress and completed choices restored consistently | covered | 7.8 3.5.6 |  | every job state change saved |
| A39.13 | Relevant world changes restored consistently | covered | 2.19 7.8 |  | marks keep across save and load |
| A39.14 | Relevant NPC states restored consistently | covered | 2.3.1 7.8 RT2-10 | G92 | person memory saved; G92 no cap on kept extras |
| A39.15 | Timers and temporary effects restored according to clear rules | covered | 7.8 7.13 2.19 |  | partly: reload gives the same next hour and marks fade on the clock; no timer-specific test |
| A39.16 | No duplicated rewards or consumed items after reloading | covered | 7.8 8.11.3 |  | partly: save and reload give the same week and next 10 minutes; no explicit test for duplicated rewards |
| A39.17 | No loading into an unavoidable death loop | covered | 7.9 OUT-12 |  | Tom cannot die and control returns within 2 minutes; saving mid-fight could reload beside enemies, untested |
| A39.18 | Previous valid progress surviving an interrupted save | covered | AX-07 8.11.3 |  | written to a new file and swapped; kill test across 100 saves |
| A39.19 | A useful message when storage is full or unwritable | missing |  |  | Needs a message and safe behaviour when a save cannot be written (disk full, read-only); none written |
| A39.20 | Recovery options for a damaged save where possible | covered | AX-07 8.11.3 7.8 |  | partly: three rotating autosaves and last two good states; no damaged-save message or choice |
| A39.21 | Clear compatibility handling after updates or missing downloadable content | covered | 8.11.3 AX-06 |  | partly: old save versions are converted or refused; settings survive an update; no downloadable content exists |
| A39.22 | Offline saves retained when reconnecting | covered | 10.7 |  | clash shows both saves; offline play is local first |
| A39.23 | Cloud conflicts presented without silently destroying newer progress | covered | 10.7 |  | a clash shows both saves with day, hour and place; 5 forced clashes lose nothing |
| A39.24 | Progress transferring correctly between supported machines | covered | 10.7 |  | same-account PCs tested 10 times |
| A39.25 | Machine-specific graphics settings not making another machine unusable | missing |  |  | 10.7 syncs the settings file too, so graphics settings could follow a save to a weaker PC; needs graphics kept per machine |
| A39.26 | Loading screens that provide progress or signs of life | unreal | 8.5 8.1.3 | G270 | progress while the street prepares; G270 no load limit |
| A39.27 | Control withheld until the loaded world is ready | missing |  |  | Needs a rule that control waits until the loaded world is ready; only a first-launch hold for shaders is set |
| A39.28 | A sensible return to title or another save after load failure | missing |  |  | Needs a path back to title or another save when a load fails; none written |
| A40.01 | A pause command available during ordinary single-player play | covered | 6.4 AX-10 RT-18 |  | Esc pauses everywhere |
| A40.02 | A clear distinction between menus that pause and menus that do not | covered | RT-18 6.3 6.2.1 6.2.2 6.2.3 |  | clock stops only in talk and pause; Ledger, map and letters do not pause the town |
| A40.03 | Simulation, animation and relevant sound pausing consistently | covered | RT-18 AX-10 |  | partly: clock and state frozen (save hash unchanged); animation and sound not named |
| A40.04 | Resuming without a queued accidental attack or movement | missing |  |  | Needs Resume to drop queued input; 6.6 buffers a press 100 ms early but nothing clears it on resume |
| A40.05 | Sensible behaviour when the application loses focus | covered | AX-10 |  | game pauses on losing focus; 100 alt-tabs and 50 resizes tested |
| A40.06 | Safe recovery after system sleep or suspend | missing |  |  | Needs a sleep and wake test; AX-10 covers alt-tab and resizing only |
| A40.07 | A clear route back to the title menu | covered | 6.4 7.15 |  | partly: title and quit exist; pause menu's route to title not spelled out |
| A40.08 | A clear quit-to-desktop option on PC | covered | 6.4 8.5 |  | Quit is on the title menu; pause menu quit not stated |
| A40.09 | A warning when quitting would lose unsaved progress | covered | 7.8 AX-07 |  | by design quitting saves, so no warning is needed |
| A40.10 | Quitting that waits for an active save or clearly explains why it cannot yet finish | covered | 7.8 AX-07 |  | partly: quit saves and saves swap in once complete; no rule to wait for a save in flight |
| A40.11 | No indefinitely hanging process after closing the game | missing |  |  | Needs a test that the process and the local voice helper (8.12.1) close within seconds of quit |
| A40.12 | No continued game audio after exit | missing |  |  | Needs a test that no sound plays after exit (voice helper included); none written |
| A40.13 | Settings and intended progress retained on the next launch | covered | AX-06 7.8 8.5 |  | every setting remembered; Continue returns him as saved |
| A40.14 | A useful reminder of current objectives after a longer break | covered | 6.2.3 6.2.5 6.5 |  | Open answers 'what next, and where'; Tom's reading and hints again |
| A41.01 | Resolution selection appropriate to the display | unreal | 8.3.1 8.5 |  | Resolution list including 21:9 at 3440 by 1440 is set; judged in the Unreal build |
| A41.02 | Windowed, borderless or fullscreen options appropriate to the platform | unreal | 8.3.1 |  | Windowed, borderless and full screen are listed; Unreal build to meet |
| A41.03 | Monitor selection on supported PC setups | unreal | none |  | No part names monitor choice; 8.3.1 would need a monitor selector line and a two-monitor test |
| A41.04 | Refresh-rate handling that uses the chosen display correctly | unreal | 8.3.1 |  | partly: frame cap and V-sync are set; nothing says the display refresh rate is read or honoured; needs a refresh-rate test on a high-refresh screen |
| A41.05 | A frame-rate limit option on PC | unreal | 8.3.1 |  | Frame cap of 30, 60, 120 or none is set |
| A41.06 | Vertical synchronisation or an equivalent tearing control | unreal | 8.3.1 |  | V-sync is a listed setting |
| A41.07 | Quality presets with meaningful performance differences | unreal | 8.3.1 8.1.3 | G271 | partly: Low, Medium, High ladder exists but only High is measured and no step has a target gain |
| A41.08 | Individual control over major expensive visual features | unreal | 8.3.1 AX-03 |  | partly: per-option overrides, motion blur and depth of field switches exist; the list of expensive features (shadows, volumetrics) is not written |
| A41.09 | Texture quality appropriate to available graphics memory | unreal | 8.1.1 | G269 | partly: texture pool fixed at 1,500 MB for the 6 GB line; no pool steps by card size are adopted |
| A41.10 | Field-of-view adjustment where the camera model permits it | covered | 8.3.1 AX-03 | G278 | Field of view 75 to 100, default 86; no pass test and car camera scaling unsaid |
| A41.11 | Brightness or gamma calibration with a useful reference | unreal | 8.5 8.3.1 |  | partly: brightness is offered at first launch; no calibration reference picture is described |
| A41.12 | HDR configuration where HDR is supported | unreal | 8.3.1 |  | HDR is judged with Unreal; no HDR standard or test written yet |
| A41.13 | Motion-blur control | covered | AX-03 8.3.1 5.4.3 |  | Motion blur off by default with its own switch |
| A41.14 | Film grain, chromatic aberration and similar presentation controls where used | unreal | 5.4.3 AX-03 | G215 | partly: grain is part of the grade and depth of field has a switch; no grain or chromatic aberration switch or strength is set |
| A41.15 | Upscaling and image-quality choices where supported | unreal | 8.3.1 8.1.1 | G274 | Upscaler where the engine has one and a resolution scale are listed; the packaged walk draws at 55% and upscales |
| A41.16 | Clear distinction between rendered frame rate and generated-frame options where offered | unreal | 8.3.1 | G274 | Frame generation is named in the row but no source covers it; needs a rule that generated frames are labelled apart from rendered ones, or a decision to leave it out |
| A41.17 | UI scaling that remains usable at the chosen resolution | covered | AX-01 |  | UI scale 100 to 200% checked at three resolutions |
| A41.18 | Correct aspect-ratio handling without stretched people or clipped HUD | covered | 8.3.1 AX-01 6.1.2 |  | partly: 21:9 is listed and text is checked at three sizes; no test for stretched people or clipped prompts at other aspect ratios |
| A41.19 | Preview or explanation of what a graphics setting changes | unreal | 8.3.1 |  | A benchmark or settings preview is listed; wording of each setting not written |
| A41.20 | Confirmation with automatic reversal of an unusable display mode | unreal | none |  | No part has a revert-if-not-confirmed timer for display changes; 8.3.1 would need one with a test |
| A41.21 | Clear indication when a setting requires restarting | missing |  |  | Needs a rule that any setting needing a restart says so before applying, with a menu-walk check |
| A41.22 | Settings that remain applied after restarting | covered | AX-06 6.6 |  | Every setting is remembered, settings file compared across a restart |
| A42.01 | Separate master, dialogue, effects and music volume controls | covered | AX-04 |  | Five sliders: master, voices, effects, street, music; checked at 0 and 100 |
| A42.02 | Volume changes audible while adjusting them | missing |  |  | AX-04 checks buses with meters but does not say a slider plays a sample while moved; add to AX-04 |
| A42.03 | Correct selection or following of the intended output device | missing |  |  | Nothing on choosing or following the output device; needs a rule and a test for default-device change and unplugging |
| A42.04 | Speaker and headphone presentation choices where relevant | missing |  |  | Only a mono switch exists; no speaker or headphone mix choice in AX-04 |
| A42.05 | A reduced dynamic-range option for quiet listening | covered | AX-04 |  | partly: loud noise softening clips gunshots to a door slam and voices-clear lifts speech 6 dB; no general quiet-listening compressor |
| A42.06 | Independent subtitle and spoken-language settings where supported | out | OUT-10 8.9 |  | RULINGS 23 Sep genre: English only, so one spoken and one subtitle language; subtitles on or off is AX-02 |
| A42.07 | Full rebinding of ordinary gameplay actions | covered | 6.6 AX-05 |  | Every action rebindable on keys and pad, per device |
| A42.08 | Rebinding of menu actions where necessary for accessibility | covered | AX-05 AX-06 |  | partly: every action rebindable; menu navigation keys are not named as rebindable |
| A42.09 | Warnings about conflicting bindings | covered | AX-05 |  | partly: No rule for warning when two actions share a key; add to AX-05 with a rebind test |
| A42.10 | A way to restore default bindings | covered | AX-05 6.6 |  | Reset to defaults per device |
| A42.11 | Independent horizontal and vertical sensitivity where useful | covered | AX-05 |  | Mouse and stick sensitivity set separately for X and Y |
| A42.12 | Separate aiming and general camera sensitivity | missing |  |  | AX-05 has one sensitivity per device; no separate aiming sensitivity once guns exist (RT2-14) |
| A42.13 | Camera inversion options | covered | AX-05 |  | Invert per axis per device |
| A42.14 | Adjustable controller dead zones | missing |  |  | No dead-zone setting for sticks; add to AX-05 with a pad drift test |
| A42.15 | Stick and trigger response options where supported | missing |  |  | No stick or trigger response curve options; add to AX-05 if the pad is to be a first-class device |
| A42.16 | Hold-versus-toggle choices for sustained actions | covered | 6.6 AX-05 |  | Every hold has a toggle and a hold-becomes-tap switch |
| A42.17 | Adjustable vibration and haptic intensity | missing |  |  | No vibration or haptic setting anywhere; needs a rule on whether the pad vibrates and an intensity slider |
| A42.18 | Aim-assistance configuration where assistance is provided | covered | AX-05 7.10 |  | Aim-assist strength off, light, strong once guns exist; dot optional and off |
| A42.19 | Controls explained without requiring memorisation of a diagram | covered | 6.5 6.6 6.1.1 |  | Hints on first need, prompts follow the device last used, hints again from the Ledger |
| A42.20 | Separate contextual bindings where driving or other modes require them | covered | 6.6 AX-05 1.2.1 |  | partly: every action rebindable and prompts follow the device; a separate on-foot and car binding set is not stated |
| A43.01 | Readable default text at normal viewing distance | covered | AX-01 |  | All text at least 24 units |
| A43.02 | Adjustable text size | covered | AX-01 |  | Scales 100 to 200% in Settings |
| A43.03 | Text reflow without clipping after enlargement | covered | AX-01 6.1.2 |  | No overlap or leaving the screen at any window size, screenshot-checked |
| A43.04 | Adequate contrast between text and background | covered | AX-01 |  | Body text at least 4.5 to 1, measured on 50 frames |
| A43.05 | Configurable text backgrounds or outlines where needed | covered | AX-02 AX-01 |  | Subtitle background box off, half or full; outlines on other text not stated |
| A43.06 | Important information conveyed through more than colour alone | covered | AX-11 6.1.4 |  | No information by colour alone; tested through three colour-blindness simulations |
| A43.07 | Distinguishable friendly, hostile and neutral markers for different colour-vision needs | out | OUT-09 AX-11 |  | OUT-09 no markers; people and key objects differ by shape and light under AX-11, so no friend or foe markers exist |
| A43.08 | Scalable or configurable aiming reticles | covered | AX-05 |  | partly: the aiming dot is optional and off by default; no size or colour option |
| A43.09 | Optional emphasis for interactable objects where needed | covered | 6.1.1 7.10 AX-11 |  | Every usable thing has a prompt; seeing outline is an assist; key objects differ by shape and light |
| A43.10 | A way to distinguish important objects from visual clutter | covered | AX-11 7.10 |  | partly: key objects distinct by shape and light and an optional outline; no clutter test |
| A43.11 | Menu narration or screen-reader support where offered | covered | AX-09 |  | Read menus aloud switch, off by default and offered on the first menu |
| A43.12 | Narration that announces selection, value and changes | covered | AX-09 |  | Speaks the focused item and its value; menu walk log must show a speech event for each |
| A43.13 | Narrated or otherwise accessible error and confirmation messages | covered | AX-09 | G282 | partly: menus and Ledger lines read; error and confirmation boxes are not named and in-play prompts have no test |
| A43.14 | Accessible reading of essential documents and clues | covered | AX-09 6.10 6.2.2 |  | partly: Ledger lines are read aloud and letters go into the Ledger; letters shown as page images are not said to be read |
| A43.15 | UI focus that remains visible and inside the active dialogue | covered | AX-06 6.7 |  | Focused item always visible; Leave always offered in talk |
| A43.16 | Gameplay information that remains legible after changing display size or resolution | covered | AX-01 6.1.2 |  | Text checked at three resolutions and four window sizes |
| A44.01 | Subtitles available for essential dialogue | covered | 6.1.2 AX-02 |  | Subtitles on by default for every spoken line |
| A44.02 | Subtitles available before the opening scene | covered | AX-02 |  | Offered on the first menu before any sound |
| A44.03 | Speaker identification when the speaker is not obvious | covered | AX-02 6.1.2 |  | Speaker name on by default for named people |
| A44.04 | Directional indication for important off-screen speech or sound where needed | covered | 8.4.1 | G275 | partly: words at the screen edge for shouts and cars; no direction of the sound is given |
| A44.05 | Captions for essential non-speech sounds | covered | 8.4.1 | G275 | Sound shown assist captions loud noises, the street going quiet, shouts and cars |
| A44.06 | Sufficient subtitle display time | covered | 6.1.2 AX-02 |  | partly: line plus 0.3 s; no minimum reading time for short lines and no adjustment |
| A44.07 | Subtitle styling and size options | covered | AX-02 6.1.2 |  | Three sizes, box off, half or full, name on or off |
| A44.08 | Mono output without losing essential information | covered | AX-04 |  | Mono switch; essential information also shown by 8.4.1 |
| A44.09 | Visual equivalents for gameplay-critical audio signals | covered | 8.4.1 6.1.4 |  | Sound shown words and the corner light cue |
| A44.10 | Alternatives to required speech input where voice commands exist | covered | 6.7 8.6.1 |  | partly: no speech input exists; talk is typed or picked from suggested lines, and a whole talk can be done by pad |
| A44.11 | Separate voice-chat and game-audio control in multiplayer | out | OUT-03 |  | RULINGS 23 Sep: no multiplayer |
| A45.01 | Core actions remappable rather than only swapping entire preset layouts | covered | 6.6 AX-05 |  | Every action rebindable individually |
| A45.02 | Alternatives to repeated rapid button presses | covered | AX-05 |  | No action needs repeated pressing |
| A45.03 | Alternatives to prolonged button holds | covered | AX-05 6.6 |  | Toggle for every hold and hold-becomes-tap switch |
| A45.04 | Alternatives to difficult simultaneous button combinations | missing |  |  | No rule that no verb needs two buttons at once; add a check to AX-05 or 6.6 |
| A45.05 | Adjustable timing windows for demanding interactions where offered | covered | 7.10 6.6 |  | partly: slower fight wind-ups, longer witness walks and a 100 ms early-press window exist; no general timing slider |
| A45.06 | Quick-time events that can be simplified or bypassed where appropriate | covered | AX-05 5.8.2 |  | partly: no quick-time events are designed and no action needs repeated pressing; cutscenes are skippable |
| A45.07 | Menu operation without precise pointer placement | covered | AX-06 |  | Large stationary targets; menu walk by pad, keys and mouse |
| A45.08 | Adjustable cursor or menu-navigation speed | missing |  |  | Nothing on menu or cursor speed; add to AX-05 if a pad cursor is ever used |
| A45.09 | Assistance for sustained steering, aiming or camera control where offered | covered | 7.10 AX-05 |  | Driving help eases steering and strengthens brakes; longer fights and walks |
| A45.10 | A way to pause without demanding the same dexterity as combat | covered | 6.4 AX-10 |  | Esc pauses everywhere; pause on losing focus |
| A45.11 | Support for compatible alternative controllers | missing |  |  | Only keyboard, mouse and a pad are named; add a line and a test for adaptive controllers through the platform input layer |
| A45.12 | No mandatory motion gesture without a button alternative where practical | covered | 6.6 AX-05 |  | No motion gestures exist; every verb is a key or pad button |
| A46.01 | Plain explanations of goals and unfamiliar terms | covered | 6.2.3 6.5 6.2.4 |  | Open page, hints and money in words in plain language; terms list not written |
| A46.02 | A way to review tutorials and recent information | covered | 6.5 7.10 |  | Hints again from the Ledger |
| A46.03 | Adjustable or pausable reading time | covered | 6.4 7.13 6.10 |  | partly: Esc pauses, talk stops the clock, letters open as pages; subtitle time is not adjustable |
| A46.04 | Clear indication of what changed after a menu action | missing |  |  | No rule that a menu action shows what changed (setting applied, game saved); add to AX-06 with a menu-walk check |
| A46.05 | Assistance settings separated by challenge where practical | covered | 7.10 |  | Each assist changes only its own thing, all off by default |
| A46.06 | Difficulty changes that do not require restarting the game | covered | 7.10 AX-06 |  | Settings are reachable from pause; assists apply without a restart is implied, not tested |
| A46.07 | Optional navigation assistance where the world is difficult to parse | covered | 6.9 7.10 |  | partly: lost-for-90-s landmark line, a passer-by after 3 minutes, directions kept in the Ledger; no markers by OUT-09 |
| A46.08 | Reduced camera shake and head movement options | covered | AX-03 |  | Switches for shake, head bob, close-in and blur |
| A46.09 | Control over camera recentering where it causes discomfort | missing |  |  | On-foot camera follow (1.1.2) has no recentring control or setting; add to AX-03 or 1.1.2 |
| A46.10 | Control over strong flashing and other avoidable visual triggers | covered | AX-03 |  | Reduce flashing switch and photosensitivity line |
| A46.11 | Reduced motion or animated-background options in menus | missing |  |  | AX-03 title names background movement but no menu animation switch is described; add one or state menus are still |
| A46.12 | Control over repetitive UI pulsing and notifications | missing |  |  | No rule on pulsing UI or notification frequency beyond hint spacing (6.5); add a no-pulse line |
| A46.13 | Clear content information where potentially distressing content is central | covered | 10.2 AX-03 |  | partly: rating target and photosensitivity line shown once guns flash; no in-game content note at start |
| A46.14 | Accessibility settings retained across sessions | covered | AX-06 |  | Every setting remembered and survives an update |
| A47.01 | Interface text available in the selected supported language | out | OUT-10 8.9 |  | RULINGS 23 Sep genre: English only, no localisation |
| A47.02 | Subtitles and audio using the selected supported languages | out | OUT-10 8.9 |  | RULINGS 23 Sep genre: English only |
| A47.03 | Correct characters rather than missing-glyph boxes | missing |  |  | No glyph test; English only still needs pound sign, dashes and curly quotes checked in the chosen faces |
| A47.04 | Longer translated text fitting the interface | out | OUT-10 |  | RULINGS 23 Sep genre: English only, no translation |
| A47.05 | Appropriate line breaks and reading direction | out | OUT-10 |  | RULINGS 23 Sep genre: English only |
| A47.06 | Names and terminology used consistently across dialogue, maps and objectives | missing |  |  | No names-and-terms check across dialogue, map and Ledger; 4.9 brand bible owes six names; add a names list check to 9.7 |
| A47.07 | Localised button and keyboard instructions that match the actual controls | covered | 6.6 6.1.1 |  | partly: prompts follow the device last used; showing the rebound key is not stated |
| A47.08 | User-entered names preserving supported accents and characters | missing |  |  | Decide in or out: no name entry exists (Tom is fixed); typed talk accents are not tested |
| A47.09 | Sensible number, date and measurement formatting | covered | 6.2.4 4.9 |  | Money is pounds and pence in words; 1990 units only |
| A47.10 | Legible translated versions of essential in-world writing | out | OUT-10 |  | RULINGS 23 Sep genre: English only |
| A47.11 | No exposed placeholder keys or internal labels | missing |  | G290 | No check for placeholder keys or internal labels on screen; text out of code has no named test |
| A47.12 | Language changes that apply predictably and explain any restart requirement | out | OUT-10 |  | RULINGS 23 Sep genre: English only, no language switch |
| A48.01 | A stable frame rate appropriate to the selected mode | covered | 8.1.1 8.11.1 | G269 | 60 fps at 3440 by 1440 never under 30; browser frame median 16.7 ms |
| A48.02 | Even frame timing rather than frequent small freezes | covered | 8.1.1 8.11.1 |  | Median, worst and ceiling frame times set; slowest 1% measured |
| A48.03 | No major hitch at the first use of an ordinary effect or weapon | unreal | 8.1.3 | G271 | PSO precaching and a hold on the first loading screen; no hitch limit or test set |
| A48.04 | World loading that keeps up with supported travel speeds | unreal | 8.1.2 | G270 | Named only; no load time or hitch limit; the soft edge is a time skip |
| A48.05 | Terrain and collision loaded before the player reaches them | unreal | 8.1.2 8.10 | G270 | Named only; collision has a soak test, streaming ahead of the player has none |
| A48.06 | Textures resolving before their absence becomes conspicuous | unreal | 8.1.2 | G270 | No texture streaming limit or test; needs a pop-in and texture-resolve standard |
| A48.07 | No large visible objects appearing suddenly at short range | unreal | 8.1.2 | G270 | No pop-in distance set |
| A48.08 | Stable performance in the expected crowd and combat density | covered | 8.1.1 8.11.1 | G269 | Budgets stated for the busiest view in rain and at night; people and shadow caps not yet adopted |
| A48.09 | Menus that remain responsive when the world is busy | covered | 6.6 8.11.2 |  | partly: every action answers in 100 ms and a job queue caps heavy work at 2 ms a frame; no menu test while busy |
| A48.10 | Loading that does not indefinitely freeze without explanation | covered | 8.5 6.4 |  | Progress shown while shaders and the street prepare; new game to control within 20 s |
| A48.11 | Long-session stability without steadily worsening performance | covered | 10.5 GV-05 8.10 |  | 2-hour soak and whole-evening walks with zero crashes; 8.11.1 memory at week 7 |
| A48.12 | Stable behaviour when changing graphics settings | covered | AX-10 8.3.1 |  | partly: 50 resizes tested; changing presets or display mode live is not tested |
| A48.13 | Stable behaviour when changing audio or input devices | missing |  |  | No test for plugging or changing audio or input devices in play |
| A48.14 | Correct recovery after task switching | covered | AX-10 |  | 100 alt-tabs, no crash, stuck key or changed state |
| A48.15 | No simulation speed changes caused by frame-rate changes | covered | 8.11.2 |  | Fixed 1/60 s step; timings independent of frame rate |
| A48.16 | No obvious corruption after repeated save and load | covered | AX-07 7.8 8.11.3 |  | Process killed at random during 100 saves; good save always loads |
| A48.17 | A usable recovery route from a crash | covered | AX-07 8.2.1 7.8 |  | Rotating autosaves, a crash loses at most the last deed, crash report on next launch |
| A48.18 | Error messages that explain the problem in player language | missing |  |  | No rule for plain-words error messages (save failed, disk full); 8.6.1 covers only the talk fallback |
| A48.19 | No routine need to restart the game to restore basic controls or interactions | covered | GV-05 8.10 AX-10 |  | Never stuck is a release bar; stuck over 5 s is zero |
| A48.20 | Updates that preserve existing progress and settings where promised | covered | AX-06 8.11.3 10.6 |  | Settings survive an update; save converter; saves in Steam Cloud; patches not designed (G297) |
| A49.01 | Correct association between the signed-in player and their saves | covered | 10.7 |  | Steam first; saves and settings sync through Steam Cloud on the same account; local multi-user not described |
| A49.02 | A clear response when an account signs out | missing |  |  | No rule for signing out of Steam in play or offline start; add to 10.7 with a test |
| A49.03 | Controller ownership changing safely with the active user | missing |  |  | No rule for pad ownership or unplugging a pad in play; add to AX-10 or 6.6 |
| A49.04 | Platform overlays opening and closing without breaking control | missing |  | G298 | needs a line on platform overlays (Steam overlay) pausing or not breaking input; AX-10 covers only lost focus |
| A49.05 | Screenshots and capture shortcuts working normally | missing |  |  | Photo mode saves its own pictures (6.8) but nothing tests Steam screenshot keys in the packaged build |
| A49.06 | Supported achievements or trophies unlocking at the intended time | missing |  |  | Decide in or out: 10.7 says no achievements at release (Q16 recommends it, not yet ruled) |
| A49.07 | Offline-earned progress synchronising appropriately when supported | covered | 10.7 |  | partly: Steam Cloud sync and clash picker for saves; no achievements to sync |
| A49.08 | Owned downloadable content correctly recognised | missing |  |  | Decide in or out: 10.6 allows paid district updates but no rule recognises owned content |
| A49.09 | Missing content explained without silently damaging saves | missing |  |  | No rule for a save made with content the install lacks; needed once districts are added after release |
| A49.10 | Required permissions requested at a relevant moment | covered | 10.11 8.2.1 |  | AI notice before the first typed line; crash report asked once; nothing sent before a yes |
| A49.11 | Optional data collection distinguishable from required operation | covered | 8.2.1 10.11 |  | Report and typed text only on a yes; offline play is an equal choice |
| A49.12 | System sleep and resume behaving predictably | missing |  |  | No sleep and resume test; talk service connection after resume is also unplanned |
| A49.13 | Handheld or small-display interfaces remaining usable where the platform is supported | out |  |  | canon project facts: PC only, on Windows; handheld platforms not targeted (AX-01 still tests 1280 by 720) |
| A49.14 | Battery or power interruptions not corrupting the last completed save | covered | AX-07 7.8 |  | Save written to a new file and swapped in only when complete; process-kill test |
| A50.01 | A clear way to host, join or find a session | out | OUT-03 |  | RULINGS 23 Sep genre: no multiplayer; OUT-03 single player only |
| A50.02 | Clear distinction between private, friends-only and public sessions | out | OUT-03 |  | RULINGS 23 Sep genre: no multiplayer; OUT-03 single player only |
| A50.03 | Invitations that reach the correct session | out | OUT-03 |  | RULINGS 23 Sep genre: no multiplayer; OUT-03 single player only |
| A50.04 | Useful explanation when joining fails | out | OUT-03 |  | RULINGS 23 Sep genre: no multiplayer; OUT-03 single player only |
| A50.05 | Connection progress with a way to cancel | out | OUT-03 |  | RULINGS 23 Sep genre: no multiplayer; OUT-03 single player only |
| A50.06 | Region or connection-quality information where latency matters | out | OUT-03 |  | RULINGS 23 Sep genre: no multiplayer; OUT-03 single player only |
| A50.07 | Other players' movement represented smoothly enough to interpret | out | OUT-03 |  | RULINGS 23 Sep genre: no multiplayer; OUT-03 single player only |
| A50.08 | Hits and interactions resolving consistently enough to feel fair | out | OUT-03 |  | RULINGS 23 Sep genre: no multiplayer; OUT-03 single player only |
| A50.09 | Clear ownership of mission progress and rewards | out | OUT-03 |  | RULINGS 23 Sep genre: no multiplayer; OUT-03 single player only |
| A50.10 | Clear rules for shared versus individual loot | out | OUT-03 |  | RULINGS 23 Sep genre: no multiplayer; OUT-03 single player only |
| A50.11 | Safe handling of players joining or leaving mid-activity | out | OUT-03 |  | RULINGS 23 Sep genre: no multiplayer; OUT-03 single player only |
| A50.12 | Recovery or clear consequences when the host disconnects | out | OUT-03 |  | RULINGS 23 Sep genre: no multiplayer; OUT-03 single player only |
| A50.13 | Rejoining without unnecessary loss of progress where supported | out | OUT-03 |  | RULINGS 23 Sep genre: no multiplayer; OUT-03 single player only |
| A50.14 | Clear downed, dead and spectating states | out | OUT-03 |  | RULINGS 23 Sep genre: no multiplayer; OUT-03 single player only |
| A50.15 | A usable revive or respawn flow where the mode includes one | out | OUT-03 |  | RULINGS 23 Sep genre: no multiplayer; OUT-03 single player only |
| A50.16 | Communication through voice, text or pings as appropriate | out | OUT-03 |  | RULINGS 23 Sep genre: no multiplayer; OUT-03 single player only |
| A50.17 | Voice input and output selection | out | OUT-03 |  | RULINGS 23 Sep genre: no multiplayer; OUT-03 single player only |
| A50.18 | Visible microphone state and a reliable mute control | out | OUT-03 |  | RULINGS 23 Sep genre: no multiplayer; OUT-03 single player only |
| A50.19 | Individual mute, block and report controls | out | OUT-03 |  | RULINGS 23 Sep genre: no multiplayer; OUT-03 single player only |
| A50.20 | Clear communication of friendly-fire rules | out | OUT-03 |  | RULINGS 23 Sep genre: no multiplayer; OUT-03 single player only |
| A50.21 | Understandable handling of version or content mismatches | out | OUT-03 |  | RULINGS 23 Sep genre: no multiplayer; OUT-03 single player only |
| A50.22 | Clear warning that menus do not pause a live session | out | OUT-03 |  | RULINGS 23 Sep genre: no multiplayer; OUT-03 single player only |
| A50.23 | Protection against common forms of cheating or session disruption appropriate to the mode | out | OUT-03 |  | RULINGS 23 Sep genre: no multiplayer; OUT-03 single player only |
| A50.24 | Supported cross-play and cross-progression behaving as advertised | out | OUT-03 |  | RULINGS 23 Sep genre: no multiplayer; OUT-03 single player only |
| A50.25 | A clear end-of-session flow that preserves earned progress | out | OUT-03 |  | RULINGS 23 Sep genre: no multiplayer; OUT-03 single player only |
| A51.01 | A photo mode that pauses or clearly explains its live behaviour | covered | 6.8 |  | Freezes the town; leaving restores the state exactly (save hash) |
| A51.02 | Photo controls that do not accidentally trigger gameplay actions | covered | 6.8 |  | Reachable from pause only; 200 random sessions tested for state change |
| A51.03 | A way to hide the HUD for clean captures | covered | 6.8 |  | All interface hidden; saved picture tested for interface pixels |
| A51.04 | Captures saved somewhere discoverable | covered | 6.8 |  | partly: pictures are saved at window size; the folder and finding them are not said |
| A51.05 | A streamer-friendly music option where licensed music would obstruct sharing | missing |  |  | Music is invented or made for the game (5.7.1) so licence obstruction is unlikely; no stated streamer-safe position or check |
| A51.06 | Rewatchable tutorials, cinematics or records where the game provides an archive | covered | 6.2.2 6.5 10.11 |  | partly: Day book, hints again and the AI notice can be read again; cutscenes (ferry shot) are not said to be rewatchable |
| A51.07 | Credits accessible without having to finish the game | covered | 6.4 10.4 | G239 | partly: credits are a menu item; whether they open from the title is not stated |
| A51.08 | Credits that can be paused, scrolled or exited | missing |  | G295 | Credits named in 6.4 and 7.15; no scroll, pause or exit controls |
| A51.09 | Clear communication of the ending's effect on continued free play | covered | 7.15 |  | Ledger last page says no new main beats; the clock runs on |
| A51.10 | A usable post-completion state where continued exploration is offered | covered | 7.15 RT2-21 |  | Play returns in the town within 10 s at the ending state |
| A51.11 | Clear rules for replay, chapter selection or New Game Plus where offered | covered | 7.15 GD-04 |  | partly: no New Game Plus by design; named replay differences; no chapter select |
| A51.12 | A way to distinguish completed content from remaining content | covered | 6.2.2 6.2.3 |  | partly: Open lists what remains and the Day book what is done; no completion count by OUT-06 |
| A51.13 | Returning after a long break without having to reconstruct the entire playthrough from memory | covered | 6.2.3 6.2.5 6.2.2 |  | Open answers what next and where from the Ledger alone; Tom reading |
| A1 | Splash and logo screens, legal notices | missing |  |  | No splash, logo or legal notice screen at launch; 10.4 and 8.12.3 give the notices and 8.5 the first screen |
| A2 | First-run hardware detection and default quality preset | unreal | 8.3.1 8.5 8.1.3 |  | First launch finds a picture the PC can keep smooth, then offers presets, brightness and scale |
| A4 | Build version visible to the player | missing |  |  | The crash report holds the build (8.2.1) but no build version is shown to the player; add to the title or settings page |
| D1 | Keyboard and mouse | covered | 6.6 |  | Keyboard with mouse reaches every verb |
| E4 | Look sensitivity and acceleration | covered | AX-05 |  | partly: separate sensitivity and invert; no acceleration option |
| F2 | Objective or quest log | covered | 6.2.3 6.2.2 |  | Open lists jobs, debts, promises and appointments with landmarks; no markers by OUT-09 |
| F7 | Screen reader or menu narration | covered | AX-09 |  | Menus and Ledger read aloud by the system speech voice |
| H9 | Animation budget at crowd scale | unreal | 5.2.5 8.1.1 | G269 | 3 ms animation budget proposed in Study 12, not adopted; Unreal-only |
| J9 | Interiors that can be entered | covered | 4.3.1 4.3.4 FIT-P34 GV-04 |  | At least 24 rooms open; places stay open |
| K7 | Police and authority response | covered | 2.6.1 2.6.10 2.6.3 2.6.4 |  | Beat constable, patrol, arrests as hours, police after a deed |
| N7 | Live spoken conversation with memory | covered | 6.7 3.6.1 8.12.2 |  | Anyone named can be spoken to live, with memory; voices on Pocket; Tom is text |
| O6 | Statistics and a session summary | out | OUT-06 6.2.5 |  | OUT-06 no stats; the Day book and Tom reading are the only record |
| P3 | Post-processing chain | unreal | 5.4.3 5.4.1 | G215 | Grade, grain and depth of field named only; no target values |
| Q5 | Minimum specification and the hardware floor | missing |  | G271 | No minimum specification or hardware floor; 8.1.3 says none set |
| R11 | Accessibility information before purchase | covered | AX-08 | G281 | Accessibility page and the same list on the store page, script-checked; store page text not written |
| S5 | Content variation by locale | out | OUT-10 |  | RULINGS 23 Sep genre: English only |
| T1 | A store page, a build and patching | covered | 10.1 10.2 10.8 10.6 | G292 | partly: store, build and Coming Soon rules exist; installer and patching not designed |
| T4 | Age rating submission | covered | 10.2 |  | Steam survey, PEGI 16 target and what would push it to 18 |
| T5 | EULA and third-party licence attributions | covered | 10.4 9.7.1 8.12.3 |  | partly: third-party notices and credits checked by a script; the game own EULA is not mentioned |
| T6 | Anti-cheat or DRM decision | missing |  |  | No statement on DRM or anti-cheat; single player, so decide whether Steam wrapper or none |
| T7 | Platform terminology and button naming | missing |  |  | No rule on Steam terms or button names in text; 6.6 prompts follow the device but naming is not set |
| U3 | A way for the player to report a problem | covered | 8.2.1 10.9 | G272 | Report a problem in pause, support address, test reports reach the inbox |
| U4 | Patch notes and a post-launch plan | covered | 10.6 | G297 | partly: districts after release named; patch notes and a patch plan are not designed |
| U5 | Playtesting with people outside the team | covered | 10.3 10.5 |  | Friends builds from phase 4, the panel of eight on a whole playthrough |
| V1 | Voice casting and direction | covered | 5.6.1 5.6.2 5.6.3 | G223 | Voices chosen per character on his yes; others not yet cast |
| V10 | A credits screen naming everyone | covered | 10.4 | G295 | partly: credits obligations set; no credits screen or full name list yet |
| V2 | Motion capture and performance | covered | 5.2.7 5.2.1 |  | partly: clips from libraries and CMU capture; no own capture or performance direction |
| V3 | Music composition and licensing | covered | 5.7.1 FIT-P09 9.7.1 | G226 | partly: music from places, made for the game or invented; no list, composer or licence plan |
| V4 | Brand and legal clearance | covered | 4.9 8.8 10.10 |  | partly: no real brand or person in print or speech; brand bible owes six names; name search is his |
| V5 | Marketing capture: trailers and screenshots | covered | 10.8 | G299 | partly: sizes and hour estimates; no trailer brief |
| V6 | Art direction and a style bible | covered | 5.10 5.11.4 |  | Hook sheet, dated photographs, standards and teardowns |
| V7 | Writing at volume, and editing it | covered | 3.6.3 3.6.4 8.8 GD-08 |  | partly: written lines checked once and word-list gated; no editing pass or volume plan |
| V8 | QA: functional, compliance and localisation testing | covered | 9.5 10.5 GV-05 |  | Bot, scripted tests, nightly packaged walk and release passes; no localisation by OUT-10 |
| V9 | Build and release engineering | covered | 10.1 9.5 9.7 |  | Packaged release build walked by the tester, guards on every commit |
