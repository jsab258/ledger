# Melee feel targets: what a fist fight must do, measured from the outside (18 November 2026)

Fighting is the next feel study after driving. Every one of his combat options includes fists and improvised weapons, so these targets are needed whichever option he picks. The browser feel study is tuned toward this sheet first; the Unreal game later runs the same drills and must match the browser's numbers. Written by a cloud helper on 18 Nov 2026; not yet reviewed (a fresh review should follow, as for driving). Marks: [READ] read at the source today; [SS] search result only; [I] judgement with its reason; est. an estimate. All sources searched or read 18 Nov 2026.

His rule (RULINGS, 17 Nov): other games are studied from the outside only (gameplay footage played in the browser, developer talks, published analysis). Never decompiled, their files never opened or extracted, copy protection never got round, their videos never downloaded.

Rules this sheet obeys: his design "LEDGER Combat: Final State" (game-design/combat-design.md) with his 30 Oct ruling, quoted from RULINGS.md: "fists knock a man out and never kill on their own; a fall against a kerb, wall or step after a blow can kill, rarely, and the town treats it as a killing". Tom cannot die. No lock-on, no combat music, no health bar. Nothing to do with drink: no bottles or glasses as weapons, so the improvised weapons here are a chair, a brick and a length of pipe (the design's list).

Note on Study 14: some numbers below come from Study 14 (28 Oct), which read KCD2's and Mafia's own files before his 17 Nov ruling replaced that method. They are quoted from our own notes as they stand; nothing was opened for this sheet, and none of them was re-checked today. Every Study 14 number is pre-ruling: it may guide a first tuning, but it is not evidence under the 17 Nov rule and must be re-measured from the footage in (e) before any band rests on it.

## In short

- A blow must start moving within 0.1 s of the button. A jab lands about 0.25 to 0.40 s after it starts, a hook 0.45 to 0.75 s, the committed heavy blow 0.63 to 0.85 s, a pipe or chair swing 0.80 to 1.05 s.
- Contact is sold by a short freeze (hit-stop) of about 0.03 s for a jab up to about 0.1 s for a heavy blow or a swung weapon, a camera close-in held about 0.8 s, a small shake and a layered sound landing within one frame of the blow.
- A man struck reels 0.5 to 0.7 s from a light blow and 0.9 to 1.3 s from a heavy one. An enemy's wind-up is readable 0.45 to 0.80 s before it lands, so a player can block or dodge on sight.
- At most two men swing at Tom at the same moment, their swings at least 0.4 s apart. A fist knock-out lasts 10 to 30 s; a fist fight kills only through a fall against a kerb, wall or step after a blow, and never kills Tom.
- Mashing empties stamina in 6 to 10 jabs or 3 to 4 heavy blows; it refills in 4 to 8 s.
- Most bands rest on judgement: no public source gives the hit-stop, block or dodge timings of the reference games. Frames from the videos in (e) should replace the estimates.

## (a) The reference set

| Game | Why it is in the set | What to take, what to leave |
|---|---|---|
| Kingdom Come: Deliverance II | His named reference (Study 14). Grounded, readable blows, morale that ends fights, fists that cannot kill, a town that reacts | Take timing and consequence. Leave first person, lock-on and skill-widened windows (Tom does not improve) |
| Grand Theft Auto (V, and IV's physics-blended street fights) | His second named reference (18 Nov, advisor 229): why people play for hours. A fight can start anywhere in an open town, and the street reacts (onlookers, police) | Take the open-street start and the town's reaction. Leave arcade damage and lock-on. No frames measured yet: GTA footage to be added to the plan in (e) |
| Mafia: The Old Country | One data point among others, never the bar: studied only as a period game made in Unreal (his words of 18 Nov, advisor 229). Closes in by motion warping instead of lock-on; hit-stop per kind of blow; melee camera held 0.8 s; layered sounds | Take the contact kit and the warp. Leave the knife duel mode |
| Sleeping Dogs | The closest street brawler: strikes, grapples, counters and the street as a weapon (phone booths, stalls, cars). Its designers named a continuous-take fight from The Protector as their first reference [READ, Siliconera] | Take environment moves and counters. Leave the martial-arts speed and the visible counter flash |
| The Last of Us Part II | Melee with weight in a grounded world. Naughty Dog lengthened enemy tells and added a dodge so that melee became a skill, not a trade of hits [READ, Game Developer 21 Jul 2021]. Enemies spread round the player on 16 radial lines; separate high and low attacks over fences [READ, 4Gamer 22 Jul 2021] | Take long readable tells, the dodge, spacing round the player, attacks shaped by walls. Leave the gore level (canon allows blood and light gore, no cruelty as spectacle) |
| Yakuza 0 and the Yakuza series | The street brawl with things at hand, and the most-studied attack spacing in crowd fights | Take things at hand and surfaces (Study 17). Leave frequent random fights and finishers into walls (no cruelty as spectacle). Note: Yakuza: Like a Dragon itself fights turn by turn, so its frames are of no use for timing; use Yakuza 0 |
| Red Dead Redemption 2 fist fights | Physics-blended hit reactions (Euphoria) on authored blows; heavy, slow, readable punches; the town watches | Take the weight of reactions and the slow tempo. Leave its lock-on |
| Batman Arkham freeflow (counterpoint) | The best-known crowd system: one hit, counter on a warning, enemies mostly take turns, the last man falls in one hit at a combo of 2 or more [READ, Costiuc, 28 Sep 2018] | What LEDGER is not: no counter icons over heads, no combo meter, no man flying across the room. Useful as the outer edge: if a measured number reaches Arkham's, the fight has stopped being grounded |

Order corrected 18 Nov evening (his words, advisor 229): KCD2 is the measuring stick, with GTA for why people play for hours; Mafia's numbers stay only as one data point among others.

## (b) Ground truth from real fighting

| Fact | Number | Source |
|---|---|---|
| Whole punch, start of movement to end, trained boxers | jab or cross 357 ms (plus or minus 178); hook 477 ms (plus or minus 203) | Boxing News, "The science behind the hook", 26 Nov 2015, citing a 2011 Liverpool John Moores University study [READ]. The study itself appears as "Piorkowski et al 2011, punch kinematics" in search results; its repository page could not be opened (permission timed out) [SS] |
| Hand speed | hooks reach a higher peak hand speed than jabs or crosses | same article [READ]; no figure given |
| Human reaction to a seen signal | simple reaction about 0.2 to 0.25 s; choosing between responses about 0.3 to 0.45 s | est. Common textbook ranges; the athlete reaction-time paper found (PMC, 2018, three measures of reaction time in individual sports) could not be opened, so this is not evidence [SS] |
| Delay players notice | median smallest noticed delay 40 ms; self-reported average 85 ms; tolerated median 120 ms, about 100 ms for shooters | Jiang, Kundu, Liu, Salay, Xu and Claypool, "A Survey of Player Opinions of Network Latency in Online Games", WPI, 2020 [READ]. Network delay and self-report, not measured input delay |
| How long a knocked-out man stays down | not found | No study of knock-out duration was reached. KCD2's quest knock-out is 10 s (Study 14). Boxing's count of ten is a rule, not a measure |
| A real fist fight's pace | not found | No source measured blows per minute in a street fight. Judgement: far slower than a game's, with long spells of grabbing and pushing [I] |

Ground truth sets the floor for speed: a game jab much faster than a real one (under about 0.25 s to contact) cannot be read by the man receiving it, and a hook much slower than 0.75 s looks like slow motion [I].

## (c) Behaviour targets, C1 to C15

Each band: the real or reference figure, widened where games bend reality on purpose. The key names are the scorer's (tools/lane/melee_drills.py).

| ID | Number | Band | Source |
|---|---|---|---|
| C1 | Button to the blow starting to move (all blows, block, dodge) | 0 to 0.10 s | Latency survey above, est. (a game frame budget on top of 40 to 85 ms noticed) |
| C2 | Jab: start to contact; contact window; recovery after contact | 0.25 to 0.40 s; 0.03 to 0.10 s; 0.20 to 0.40 s | Real jab 0.36 s whole [READ]; Mafia's left hit window opens from 0.27 s (Study 14); window and recovery est. |
| C2 | Hook: same three | 0.45 to 0.75 s; 0.05 to 0.15 s; 0.35 to 0.50 s | Real hook 0.48 s whole [READ]; KCD2 hooks land at 0.70 s, about 0.4 s from contact to end (Study 14) |
| C2 | Heavy (committed blow, LEDGER's B01): same three, plus recovery after a miss | 0.63 to 0.85 s; 0.05 to 0.17 s; 0.35 to 0.50 s; miss 0.70 to 0.90 s | KCD2 unarmed median 0.75 s, range 0.63 to 0.80; B01 0.73 s; swing live 0.17 s before contact; miss recovery 0.8 s by judgement (Study 14, item 2) |
| C2 | Improvised swing (pipe, chair, brick): same three | 0.80 to 1.05 s; 0.08 to 0.20 s; 0.50 to 0.80 s | KCD2 blunt weapon to contact 0.93 s (Study 14); the rest est. |
| C3 | Hit-stop (the freeze on contact): jab, hook, heavy, swing | 0.025 to 0.05; 0.04 to 0.08; 0.06 to 0.12; 0.07 to 0.13 s | est. LEDGER now uses 2 frames (0.033 s). Fighting games run far longer (Capcom's seminar gives 8, 12, 16 frames, 0.13 to 0.27 s, as an example [READ]; Street Fighter II about 10 frames [READ, Wagar]); KCD2 has none; Mafia's values were not reached. Grounded games sit well below fighting games [I] |
| C4 | Hit reaction on the man struck: light; heavy | 0.50 to 0.70 s; 0.90 to 1.30 s | KCD2 weak class 0.6 s, unarmed 1.18 s; Mafia 1.06 s (Study 14); LEDGER D03, D04 |
| C5 | Enemy wind-up readable before contact; guard fully up after the button; the drill's block succeeds | 0.45 to 0.80 s; 0 to 0.15 s; yes | Wind-up: choice reaction (about 0.3 to 0.45 s, est.) plus input and frame delay; TLOU2 lengthened tells for this reason [READ]. Accessible mode: wind-up 1.25 to 1.5 times longer (the design's longer window), est. |
| C6 | Dodge: button to moving; blows cannot land for; whole dodge; the drill's dodge succeeds | 0 to 0.10 s; 0.20 to 0.35 s; 0.50 to 0.80 s; yes | est. TLOU2 added a dodge to make melee a skill [READ]; no window was published |
| C7 | Knocked down (conscious) to starting to get up; getting up; fist knock-out to starting to get up | 1.5 to 3.0 s; 1.0 to 2.0 s; 10 to 30 s | est.; knock-out lower edge KCD2's 10 s (Study 14) |
| C7 | Deaths breaking his ruling in a fists-only fight | 0 | His 30 Oct ruling. Counted as a break: any death of Tom; any fists-only death not preceded by a fall against a kerb, wall or step within 3 s of a blow landing |
| C8 | Men swinging at Tom at the same moment; gap between two men's swing starts; longest wait between one man's swings | 1 to 2; at least 0.40 s; at most 2.5 s | Design: two against one is deadly, three is a beating, so two can swing, but staggered; KCD2 caps nothing and keeps at most 2 s between a man's blows (Study 14); attack tickets common in crowd fights [READ, Signals and Light 11 May 2024]; numbers est. |
| C9 | Closing in without lock-on: time; stopping distance; furthest start | 0.40 to 0.55 s; 0.9 to 1.1 m; at most 2.0 m | Mafia warps up to 2 m, to 1 m off, in 0.42 to 0.52 s (Study 14) |
| C9 | Target choice: the man nearer the stick direction is picked | 100% of scripted cases | Design: no lock-on |
| C10 | Fight camera: distance behind; both men in frame; the other man's feet in frame; camera inside a wall; close-in on contact held; shake peak; shake settles | 3.5 to 5.0 m; at least 95% of frames; at least 90%; 0 frames; 0.6 to 1.0 s; 0.3 to 1.5 degrees; within 0.3 s | His 28 Oct camera pick (wider, feet and watchers seen); Mafia's melee camera held 0.8 s (Study 14); distance, shake and settle est.; shake obeys Reduce motion |
| C11 | Stamina: jabs from full to empty; heavy blows from full to empty; empty to full | 6 to 10; 3 to 4; 4 to 8 s | LEDGER now 0.34 a swing (3 heavies) and 0.09 a second (11 s); KCD2 26 a swing of 100 and 22 a second (about 4 and 4.5 s) (Study 14); jab count est. |
| C12 | Hits before breaking: chair; brick; pipe | 1 to 3; 2 to 5; at least 20 (does not break) | est. |
| C13 | Sound: whoosh from blow start; impact from contact; pain cry after contact; enemy shout before his blow lands | -0.05 to +0.10 s; within 0.034 s; 0.05 to 0.30 s; at least 0.40 s | est.; four sound layers (Mafia) and combat shouts as warnings (KCD2) from Study 14 |
| C14 | Three-blow combination (jab, jab, hook) with early inputs: blows landed; total time | 3; 1.5 to 2.4 s | est. Recovery is cut short into the next blow |
| C15 | Heavy blows to put a fresh, unguarded man down | 3 to 6 | LEDGER Combat.cs gives 4; neither reference game gives it (Study 14); band est. |

## (d) Published professional methods

| Method | What it says | Source, date |
|---|---|---|
| Attack data and behaviours, two layers (TLOU2) | Each attack has animations for both men, start conditions (range, facing, a clear line), and timeline marks for hit frames, target tracking and invulnerable spells. Above it, each enemy is in one behaviour with an attack list, a destination (close in, keep distance) and enter and exit rules. Tells lengthened from Uncharted 4, where blows almost always landed | Ming-Lun "Allen" Chou, GDC 2021, "Melee AI in The Last of Us Part II"; summary by Game Developer, 21 Jul 2021 [READ]; GDC Vault session page [SS] |
| Spacing slots round the player (TLOU2) | 16 radial lines out from the player; enemies wait between them; obstacles bend the lines. High and low attack sets near waist-high fences | 4Gamer report of the same talk, 22 Jul 2021 [READ] |
| Melee system and paired animation (TLOU) | Design and build of the melee system, animation syncing between two bodies | Anthony Newman, GDC 2014; Game Developer video post 30 Oct 2017 [READ, no numbers in the post] |
| Attack tickets and priority | Who may attack: one at a time; free attackers controlled by level design; tickets capping concurrent attacks, costing more for strong blows; a priority layer (distance, camera angle, hit reactions) choosing who gets a ticket; a director reading player stress | Signals and Light, "How do simultaneous enemy attacks work?", 11 May 2024 [READ]; "Enemy combat fundamentals", 23 Mar 2024 [READ] |
| Hit-stop | Freezing both bodies at contact makes the hit read and feel stronger; Street Fighter II about 10 frames; games without it (Dark Souls 2) read weaker, helped by sparks | Celia Wagar, CritPoints, 17 May 2017 [READ] |
| Hit-stop scaled by strength | An example game: 8, 12, 16 frames for light, medium, heavy | Capcom, Street Fighter V seminar column, undated [READ] |
| Hit-stop tuned by eye per animation | Avowed's combat designer sets hit-stop per animation and per weapon, and times particles to the instant | Wes Fenlon, PC Gamer, 22 Nov 2024 [READ] |
| Environment as the hook (Sleeping Dogs) | Environment interaction called the key hook; props in the open world, not only in missions; physics throws when no finisher is scripted | Siliconera interview with Mike Skupa and Jeff O'Connell, undated (about 2012) [READ] |
| Freeflow (Arkham) | Hit and counter; special enemy types kept to one or two a fight; others do not attack during some takedowns | Stanislav Costiuc, Game Developer, 28 Sep 2018 [READ] |
| Motion warping instead of lock-on; hit-stop per kind; camera close-in; sound layers | From Mafia's and KCD2's behaviour as recorded in Study 14 | Study 14, 28 Oct 2026 (repository) |

Method chosen for LEDGER from these: blows are data with timeline marks (TLOU2); enemies take attack tickets, at most two out at once, with a priority by distance and camera view (Signals and Light, Dark Souls example); spacing slots round Tom shaped by walls; motion warping to close in (Mafia); hit-stop per kind of blow, short, set by eye inside the C3 bands and then frozen as data (Avowed's method, our bands).

## (e) Frame-taking plan

Videos are played in the browser on YouTube, never downloaded. Titles and links below are exactly as they appeared in today's search results; no channel name appeared in any result, so each channel must be confirmed on the page before use [SS]. Prefer clips without commentary overlays or mods; step frames with the period and comma keys at the highest frame rate offered.

| # | Game | Title in search result | Moments to capture | Measures |
|---|---|---|---|---|
| 1 | Sleeping Dogs | "Sleeping Dogs - Combat Walkthrough" (youtube.com/watch?v=TgiBiJoaQXo) | A single light strike from rest; a counter on the red warning | C2 jab, C5 warning lead |
| 2 | Sleeping Dogs | "Sleeping Dogs Melee Combat" (youtube.com/watch?v=bPF0IZgr5nI) | Environment move against a wall or stall; reaction length | C4, surface moves |
| 3 | Sleeping Dogs | "Sleeping Dogs: Definitive Edition Combat Gameplay" (youtube.com/watch?v=w1FZfWG0KE0) | Several thugs at once: how many swing together | C8 |
| 4 | Kingdom Come: Deliverance II | "Kingdom Come Deliverance 2 Fist Fight Only Unarmed Combat Challenge Part 1" (youtube.com/watch?v=l7B5xog9SwU) | Swing start to contact; stagger; knock-out to getting up | C2 heavy, C4, C7 |
| 5 | Kingdom Come: Deliverance II | "Kuttenberg Fight Club (No Weapons)" (youtube.com/watch?v=0Lr24tu5jb8) | One-on-one bouts: blocks, stamina running out | C5, C11 |
| 6 | Mafia: The Old Country | "Melee Combat in Mafia The Old Country" (youtube.com/watch?v=ZjizYMAVZxk) | Closing in on a blow; hit-stop frames; camera close-in and its return | C9 warp, C3, C10 |
| 7 | Mafia: The Old Country | "Gameplay Combat Overview - Mafia: The Old Country" (youtube.com/watch?v=JbX7koh5omk) | Fist combination timing | C2, C14 |
| 8 | The Last of Us Part II | "The Last of Us Part 2 Remastered - Brutal Combat Gameplay Vol. 1 ( GROUNDED / NO DAMAGE )" (youtube.com/watch?v=ZjqnGwIHch8) | Enemy wind-up to contact; player dodge start to clear; a pipe swing | C5, C6, C2 swing |
| 9 | Red Dead Redemption 2 | "Melee Fighting Mechanics" (youtube.com/watch?v=1X2k6UdJah4) | Punch start to contact; physics-blended reaction length; knock-down | C2, C4, C7 |
| 10 | Red Dead Redemption 2 | "Red Dead Redemption 2 - Street Fight Brutal Combat" (youtube.com/watch?v=pRFbRDhsOpc) | Camera distance and framing in a street fight; watchers in frame | C10 |
| 11 | Yakuza 0 | "YAKUZA 0 Normal fight, men in black" (youtube.com/watch?v=BynJLUyOV6A) | Crowd: how many swing at once, gaps between their swings; a bicycle or sign picked up | C8, C12 |
| 12 | Yakuza 0 | "Yakuza 0 - Brawler Style: Training" (youtube.com/watch?v=Nd6DCscZvtg) | Clean single blows on a still target | C2, C3 |

Avoid for timing: compilations, "AI remastered" or "cinematic" uploads (frames may be invented or cut), shorts, and clips titled with mods. Several RDR2 results are set in saloons, which shows drink: do not use frames from them on any page (content rule), even for measurement notes.

How each number is read from frames:
- Times (C2, C4, C5, C6, C7): count frames between the first frame of visible movement and the frame of contact (or end), divided by the video's frame rate. Each value from at least five instances; record the median and the range.
- Hit-stop (C3): frames in which both bodies hold still at contact while the background (people, cloth, smoke) moves.
- Attackers (C8): mark each enemy's wind-up start frame; count overlaps.
- Camera (C10): camera distance from a man's known height (about 1.75 m) on screen against the screen height, with the field of view judged from the scene; close-in from the frame the view tightens to the frame it returns.
- Warp (C9): distance closed from the floor against the man's shoulder width (about 0.45 m), est.

## (f) Scripted drills

The tool is tools/lane/melee_drills.py, tests in tools/lane/test_melee_drills.py (31 tests, all passing on 18 Nov 2026).

### Why behaviour carries over, not settings

The browser study and the Unreal game run on different engines, animation and physics. Copying a speed or a curve from one to the other does not make them feel the same. So nothing crosses as a setting: each runs the same scripted drills, driven by a script and never a person, writes the same telemetry, and is tuned until its numbers match. The browser is tuned toward this sheet; Unreal is then tuned toward the browser's numbers.

### The drills

| Drill | Setup | Script | Gives |
|---|---|---|---|
| M1 jab, hook, heavy | Tom and a standing dummy 1.0 m apart; heavy also run 3 m apart so it misses | One press at 1.0 s, wait 3 s | C1, C2, C3, C4, C13 |
| M2 combo | As M1 | jab 1.00 s, jab 1.30 s, hook 1.60 s (early on purpose) | C14 |
| M3 block | One attacker 1.5 m away throws one heavy | Block 0.30 s after his wind-up becomes readable | C5, shout lead |
| M4 dodge | As M3 | Dodge away 0.30 s after the wind-up | C6 |
| M5 knockdown | Fresh opponent, no guard, no kerb within 3 m | Heavy each time Tom can act until he goes down; wait 40 s | C7, C15, the ruling check |
| M5k kerb | As M5 with a kerb 0.5 m behind the opponent; fists only; seeds 1 to 200 | As M5 | The ruling check: a death only through a fall after a blow; never Tom |
| M6 two attackers | Two men start 3 m away either side; Tom does nothing | 20 s idle | C8 |
| M7 breakage | Tom holds a chair, a brick or a pipe by a dummy that never falls | Swing each time he can act, until it breaks or 25 hits | C2 swing, C12 |
| M8 camera, narrow street | A street 2.5 m wide between walls; Tom and one man trade blows along it 10 s, then across it | Alternate jab and hook | C10 |
| M9 stamina | Full stamina, dummy at 1 m | Jab until empty, idle until full; then heavy | C11 |
| M10 targets | Two dummies 1.8 m away, 30 degrees left and right | Stick at -40, -20, -5, 5, 20, 40 degrees, then heavy | C9 |

### What each drill writes

One telemetry file per run, one JSON object per line: the time in real seconds since the drill began, the event name and who did it, with a few fields. Events: input, hit_start, active_start, active_end, hit_contact, miss, hitstop_start, hitstop_end, recovery_end, stagger_start (light or heavy), stagger_end, telegraph_start, attack_start, attack_end, guard_up, block, dodge_start, invuln_start, invuln_end, dodge_end, knockdown, ko, getup_start, getup, fall_hazard (kerb, wall or step), death, stamina, stamina_empty, weapon_break, warp_start, warp_end, target_pick, camera (distance, height, shake, both men visible, feet visible, inside a wall), close_in_start, close_in_end, sound (whoosh, impact, pain, shout). The browser study and Unreal both export this format. Recovery is counted without the hit-stop freeze.

### Pass rules

- Against this sheet: each number inside its band, edges included. A band the run did not produce is shown as missing. A number with no band is shown, not failed.
- Unreal against the browser: within 5% or a fixed allowance, whichever is larger (one frame at 30 fps, 0.034 s, for times; 0.1 m; 0.2 degrees; 2 percentage points); counts must match exactly; a number one side gives and the other does not is a fail.
- The ruling check (fists never kill on their own; Tom never dies) is a band of exactly zero, so it fails like any other number.

### Choices to know about

- The tool's small reference fighter exists only to test the tool. It meets every band, which proves the measuring, not how LEDGER's fighting should be built.
- The rare killing fall: the drills check only that a fists-only death always comes through a fall after a blow. How rare it should be is open in his design (no reference found), so the 200-seed kerb run reports a count but sets no band for rarity.
- Lock-on is absent by his design; M10 checks target choice by stick direction and motion warping instead.
- Bottles are left out of M7 by the content rule, though the brief suggested one.

## (g) What the browser cannot prove

The browser proves numbers: times, counts, distances, angles. It cannot prove how a fight looks, sounds and lands in the real game. These are judged in the Unreal packaged build, through the usual gate.

| Area | What the real game checks | How |
|---|---|---|
| Animation quality | Weight shift, a body committed to the blow, a guard that drops with tiredness; no sliding feet, no snapping between clips | The animation source test of the design (B01, C01, G01, D03 by side), frames beside the reference videos of (e) |
| Contact | Fists meeting a face or body, not air or the inside of a head; two bodies against a wall lined up; cloth and hair moving at impact | Close frames at contact in M1 and M8; motion warping and physics blending checked frame by frame |
| Injuries shown | Bruises and cuts on the MetaHuman faces, blood on clothes within the content rule, a limp | Frames after M5 and M7 against the design's aftermath list |
| Sound quality | Whoosh, impact, pain and effort layers that sound like a street fight in 1990, our own or CC0 recordings | Listened to by ear; C13 sync measured in the build |
| Pad feel | That 0.1 s button-to-motion holds on a real pad in the packaged build | High-speed phone video of the pad and screen together, frames counted |
| Crowd and street | Watchers keeping about 3 m, scattering when a weapon is out, the fight camera finding room in a narrow street with people | M8 with the street's people present; frames compared with the KCD2 numbers in Study 14 |
| Performance | Frame time in budget with two fighters, physics reactions and a crowd | M6 and M8 with frame times logged in the packaged build |

## Sources

### Read today (18 Nov 2026)
- Boxing News, "The science behind the hook", 26 Nov 2015: https://boxingnewsonline.net/the-science-behind-the-hook/ [READ]
- Jiang, Kundu, Liu, Salay, Xu, Claypool, "A Survey of Player Opinions of Network Latency in Online Games", WPI tech report 20-02, 2020: https://ftp.cs.wpi.edu/pub/techreports/pdf/20-02.pdf [READ]
- Game Developer, "How Naughty Dog defined melee attacks and behaviors in The Last of Us Part II", 21 Jul 2021: https://gamedeveloper.com/design/how-naughty-dog-defined-melee-attacks-and-behaviors-in-i-the-last-of-us-part-ii-i- [READ]
- 4Gamer, GDC 2021 report on Naughty Dog's talks, 22 Jul 2021: https://www.4gamer.net/games/364/G036471/20210722007/ [READ]
- Game Developer, video post of Anthony Newman's GDC 2014 melee talk, 30 Oct 2017: https://gamedeveloper.com/design/video-how-naughty-dog-designed-i-the-last-of-us-i-brutal-melee-system [READ, no numbers]
- Signals and Light, "How do SIMULTANEOUS enemy attacks work?", 11 May 2024: https://signalsandlight.substack.com/p/how-do-simultaneous-enemy-attacks [READ]
- Signals and Light, "Enemy combat fundamentals", 23 Mar 2024: https://signalsandlight.substack.com/p/enemy-combat-fundamentals [READ]
- Celia Wagar, CritPoints, on hit-stop, 17 May 2017: https://critpoints.net/2017/05/17/hitstophitfreezehitlaghitpausehitshit/ [READ]
- Capcom, Street Fighter V seminar column, undated: https://game.capcom.com/cfn/sfv/column/131545?lang=en [READ]
- Wes Fenlon, PC Gamer, on Avowed's hit-stop, 22 Nov 2024: https://www.pcgamer.com/games/rpg/if-youve-been-worried-about-avowed-not-looking-punchy-enough-obsidians-combat-designer-has-a-hitstop-animation-superpower-that-might-reassure-you [READ]
- Siliconera, Sleeping Dogs fighting system interview, undated: https://www.siliconera.com/sleeping-dogs-fighting-system-inspired-by-tony-jaa-action-flick-the-protector/ [READ]
- Stanislav Costiuc, "Batman: Arkham Design Analysis (Part 1)", Game Developer, 28 Sep 2018: https://gamedeveloper.com/design/batman-arkham-design-analysis-part-1- [READ]
- YouTube links in (e): search results only [SS].

### In the repository
game-design/combat-design.md; RULINGS.md (12 and 30 Oct, 17 Nov); production/research/aaa-reference/studies/14-combat.md; production/lane/COMBAT-END-STATE-OPTIONS.md; production/research/lane/FEEL-TARGETS-DRIVING-2026-11-17.md (template).

### Not reached
- Piorkowski et al 2011 punch kinematics paper (repository PDF and record page: permission timed out) [SS].
- PMC article on reaction time in individual sports (2018) and PMC9798280 on punching (browser check page) [SS].
- GDC Vault pages for the TLOU2 and TLOU melee talks (talk videos not watched).
- Any measured knock-out duration, any measured street-fight pace, any published hit-stop, block or dodge window for the reference games.
