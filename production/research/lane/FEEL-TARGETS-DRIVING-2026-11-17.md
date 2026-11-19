# Driving feel targets: what the car must do, measured from the outside (17 November 2026)

For his driving plan of 17 Nov (advisor 214): simple driving in his browser test now; this study from the outside; browser driving tests in rounds of measure, tune and his short playtest; AAA driving in the real game once the map is bigger. Written by the cloud lane from three research helpers and one code helper; a fresh review follows. Reviewed 17 Nov 2026: PASS WITH FIXES (production/lane/reviews/REVIEW-FEEL-TARGETS-DRIVING-2026-11-17.md), applied. Marks: [READ] read at the source today; [SS] search result only; [I] judgement with its reason; est. an estimate from arithmetic. All sources read or searched 17 Nov 2026.

Revised 18 Nov 2026 by the cloud lane for his rulings of that day (RULINGS, Cars line): LEDGER is not a driving sim; its cars feel fun and easy first, like open-world games that are not sims; the 1990 character is carried by sound, body sway, the look and relative speed (12:36); cars are automatic by default (12:32). A provisional game set is now the default target (section c2); the real 1990 figures stay as flavour and a plausibility floor. The 17 Nov review covers the sheet as it was; the 18 Nov changes (In short, c2, f) are owed a fresh review.

His rule, which binds every helper and the main session: other games are studied from the outside only (gameplay footage, developer talks, published analysis). Never decompile, never open or extract their files, never get around copy protection, never download their videos.

Canon: no real car models or brands appear in the game; real cars below are ground truth for numbers only.

## In short

- The target is now the game set (section c2), the default since his rulings of 18 Nov: fun and easy first, like open-world games that are not sims. The ordinary car does 0 to 30 in 3 to 4.5 s and 0 to 60 in 10 to 14 s, tops out at 95 to 110 mph, brakes from 30 mph in 8 to 11 m, turns in 8.5 to 9.8 m, holds 0.82 to 0.92 g, and swings round 120 to 180 degrees on the handbrake. The gearbox is automatic by default. Every game number is provisional until next week's footage measurements replace it (method: production/lane/FOOTAGE-TO-GAME-SET-2026-11-18.md).
- 1990 shows in sound, body sway (roll and pitch at or above the real car's), the look and relative speed (police and bosses' saloons and the fast hatch stay quicker than the ordinary car; the view widens with speed).
- The real 1990 car (section b) is flavour and a floor, never the target: a 1990 small hatch of about 800 kg and 55 bhp did 0 to 60 in 13 to 17 s, 90 to 100 mph, turned in about 9.4 to 10.5 m, with gentle understeer and no ABS. The game may be quicker, grippier and sharper than that car, but not slower, wider-turning, longer-braking or stiffer, where that would feel wrong (per metric in c2).
- The 17 Nov "ordinary" and "fast" sets (the real band widened by allowed game departures, sections c and f) stay as named alternatives in the tool.
- Eight scripted drives (D1 to D8, D9 read from two of them) turn any car into those numbers. The same drives run unchanged on the browser car now and the Unreal car later; the Unreal car must land within 5% of the browser's results. Behaviour carries over, never physics settings. The tool is tools/lane/driving_drives.py (33 tests pass, game set the default); the Fable prompt for his next round is production/lane/FABLE-DRIVING-NEXT-ROUND.md.
- Best frames to measure: Forza Horizon 4 in Britain (it shows speed on screen); The Getaway for London street scale and camera; GTA IV for body roll as the upper limit. No YouTube page opened from the cloud, so the video list is from search titles only.

## (a) The reference set

No single game is the target. Each one is good for one or two things. The ground truth for numbers is the real 1990 car (section b); the games show how far a game may sensibly bend reality for fun.

| Game | Good for | Do not copy | Verdict |
|---|---|---|---|
| GTA IV (2008) | Weight. Cars roll, pitch and heave; they feel "lumbering and slippery" with soft suspension. The Drive (Aug 2026) says the game looks harder to drive than it is, because the camera and body movement sell the weight [READ]. The closest big-studio feel to an ordinary soft 1980s car. | Too much float and wallow for a small British hatch; its cars are big American barges. Handbrake turns are harder than in V [READ]. | Best reference for body roll and pitch, scaled down for a light hatch. |
| GTA V (2013) | Town driving that is easy and quick to pick up. More grip, quicker turn-in, muted suspension [READ, The Drive]. | Grip far above a 1990 hatch on thin tyres; a light tap can still spin a car [READ]. Too sharp and too sticky for our period. | Reference for ease of control and steering response, not for grip or weight. |
| Mafia III (2016) | Period car feel in town. The design director called it "Hollywood action driving", with each car given "a certain heaviness" that lets it drift round corners, and surfaces such as gravel changing the handling [READ, Game Informer, May 2016]. It has a separate simulation driving setting [SS, Twinfinite]. | American 1960s cars; drifting as the normal way to corner. | Good model of a two-level setup: a kind default and a truer setting. |
| Sleeping Dogs (2012) | Fun, forgiving chases in tight city streets; any car is easy to drift [READ, GameSpot]. | The "physics-defying sideways shunt" used to ram cars off the road [READ, GameSpot]. That is a power, not a car. | Reference for how much forgiveness a chase needs; copy none of its physics. |
| The Getaway (2002) | The only big game set on British streets with ordinary small cars. No HUD: the car's own indicators point the way; cars are fragile and smoke when badly hurt [READ, Traxion]. | Real licensed cars (canon forbids it). Handling was judged poor: sharp turn-in leads to fights with counter-steer, and police cars are unrealistically fast [READ, Traxion]. | Reference for British street scale, fragility and no-HUD guidance; a warning on handling and police speed. |
| Forza Horizon 4 (2018) | British roads: Cotswolds, Highlands, Edinburgh, a "greatest-hits version of Britain" [READ, Top Gear, Oct 2018]. "Perfectly balanced arcade handling" [READ]. Car-to-car differences that you can feel. | Racing speeds, racing grip, open roads rather than a port town. | Reference for car feel, road surface and how British roads look at speed. |
| Mafia: The Old Country (2025) | General feel only: how a modern big-studio game makes a slow, old car still fun. No review was read today. | Its cars are from the 1900s. | General mood only; no numbers. |

## (b) Ground truth: real cars of about 1985 to 1990

Spec-site figures are the maker's or a magazine's; most sites do not say which. Only the 205 GTi row names the magazines. Treat every row as about plus or minus 5% until a dated Autocar or What Car test is read from the PC (none was reachable today).

| Car (period) | Kerb weight | Power | 0 to 60 mph | Top speed | Turning circle | Source |
|---|---|---|---|---|---|---|
| Ford Fiesta Mk3 1.1 (1989) | 785 kg | 54 bhp | 15.8 s | 93 mph | not found | Encycarpedia [READ] |
| Vauxhall Nova 1.2 S (1983 to 87) | 739 to 750 kg | 55 hp | 16 s (0 to 62) | 94 mph | 9.4 m | auto-data.net [READ] |
| Austin Metro 1.0 (1987) | 771 kg | about 44 bhp [SS] | 18.2 s | 86 mph (138 km/h) | not found | Carbaze [READ] |
| Ford Escort Mk4 1.3 (1986) | 860 kg | not listed | 13.1 s | 98 mph (158 km/h) | not found | Carbaze [READ] |
| VW Golf Mk2 1.6 (1983 on) | 870 kg | 74 bhp | 12.6 s | 104 mph | not found | Encycarpedia [READ] |
| Austin Montego 1.6 L (1984) | 1,020 kg | 85 bhp | 11.5 s (Autocar test: 11.9 s) | 103 mph (Autocar: 99 mph) | not found | Unique Cars and Parts; Autocar 19 May 1984 [READ] |
| Ford Sierra 1.6 GL (1985) | 1,076 kg | not listed | not listed | 112 mph (180 km/h) | not found | Carbaze [READ] |
| Peugeot 205 GTi 1.6 (1986 to 92), fast end | 886 kg | 115 hp | 8.7 s Autocar, 8.2 s Motor | 122 mph Autocar | not found | Autozine, citing Autocar and Motor [READ] |
| Peugeot 205 GTi 1.9 (1986 to 94) | 910 kg | 130 hp | 7.8 s Autocar | 120 mph | not found | Autozine [READ] |
| Rover 820 Si (1986), police and bosses | 1,290 kg | 138 bhp | 10.5 s | 126 mph | not found | Unique Cars and Parts [READ] |
| Ford Granada 2.8i (1986), police and bosses | 1,305 kg | 150 bhp | 9.1 s | 127 mph | not found | Unique Cars and Parts [READ] |

What the table says, in plain words:
- An ordinary 1990 small hatch weighs 740 to 870 kg, has 45 to 75 bhp and takes 12 to 18 seconds to reach 60 mph. Top speed is 86 to 104 mph. That is much slower than any modern car or any GTA car.
- A family saloon (Montego, Sierra) is 1,000 to 1,100 kg and takes about 11 to 13 s.
- The fast hatch (205 GTi) is about 8 to 9 s to 60 and around 120 mph. Autozine notes the 1.6 gives "quite dramatic oversteer" when the driver lifts off mid-corner [READ]. That is a useful character for a fast car.
- The big saloon (Rover 800, Granada) is 1,290 to 1,305 kg, 9 to 10.5 s to 60, about 126 mph. Police and bosses can catch an ordinary hatch easily, which is true to life.

Highway Code stopping distances (checked, [READ] on two current sites; the same figures stood in 1990 [I]: the table has been unchanged for decades, which is the complaint in the Classics World piece):

| Speed | Thinking | Braking | Total |
|---|---|---|---|
| 30 mph | 9 m | 14 m | 23 m |
| 50 mph | 15 m | 38 m | 53 m |
| 70 mph | 21 m | 75 m | 96 m |

The brief's figures (23, 53 and 96 m) are correct. The braking parts work out at about 0.65 g, which is a gentle stop by modern standards (est., from v squared over twice the distance). The Code assumes 0.67 s of thinking time; TRL research found about 1.5 s on average [READ, Classics World]. In the wet the Code says stopping distances are at least double [I: widely quoted, not read at source today; check rule 126 and 227 wording from the PC].


Note (17 Nov, now the "ordinary" alternative, not the default): the ranges in (c) are the real band; the ordinary set the tool keeps by name is the real band widened by the 'Where games depart' column (for example 30 mph braking 9.5 to 14 m, grip 0.70 to 0.85 g, roll 3 to 6 deg, front load 75 to 82%). Three game bands are rounded inward on purpose, so the tightest stated loosening is not used in full: 30 mph braking starts at 9.5 m (not 9.35), roll tops out at 6 deg (not 6.75), braking pitch at 5 deg (not 5.25). The fast hatch's grip limit is 0.90 g and the ordinary handbrake turn tops out at 150 deg, the real ends of their (c) ranges.

## (c) Behaviour targets, M1 to M12

"Ordinary" means a 1990 small hatch of about 800 kg and 55 bhp; "fast" means a 205 GTi-class car. Game note: where games depart from reality on purpose. No source read today put a number on how much shorter games brake or how much tighter they turn; those departures are marked [I].

| Metric | Ordinary hatch target | Fast hatch | Source | Where games depart |
|---|---|---|---|---|
| M1 acceleration | 0 to 30: 4.5 to 6 s. 0 to 60: 13 to 17 s | 0 to 30: 3 to 3.5 s. 0 to 60: 8 to 9 s | 0 to 60 from table (b) [READ]. 0 to 30 est.: period tests usually put 0 to 30 at about a third of 0 to 60 for slow cars, and a bit more for fast ones [I] | Games usually shorten slow cars' times so town driving is not dull [I]. Allowed: up to 20% quicker to 30 mph; keep 0 to 60 honest so cars feel 1990. |
| M2 top speed; speed at 100 m | 90 to 100 mph; 40 to 46 mph at 100 m | 118 to 122 mph; 50 to 56 mph at 100 m | Top speeds (b) [READ]. 100 m figures est., integrating the acceleration above | Top speed rarely matters in a port town; the 100 m figure is the town feel. Keep it. |
| M3 braking to stop, dry | 30 mph: 11 to 14 m. 50 mph: 30 to 38 m. 70 mph: 60 to 75 m | 10 to 12 m; 28 to 33 m; 55 to 65 m | The longer end is the Highway Code's braking part (14, 38, 75 m) [READ]. The shorter end is est. from about 0.8 to 0.9 g, which a good non-ABS car on period tyres could reach [I] | Games commonly brake harder than real cars, so the driver feels in control [I]. Allow up to about 15% shorter than the short end; no shorter. |
| M3 wet | About 1.5 to 2 times the dry figures | same ratio | Highway Code "at least double" for total distance [I, not read at source]; wheels lock easily on 1990 cars without ABS [I] | Games soften wet braking a lot [I]. Keep a clear, felt difference. |
| M4 turning circle | 9.4 to 10.5 m | 10 to 10.5 m | Nova 9.4 m [READ]; the rest of the range is [I] from period small-car norms, check others from the PC | Games turn tighter at low speed for parking and alleys [I]. Allow down to about 9 m; never U-turn on a two-lane street in one go. |
| M5 steering response | Yaw rate at 63% in 0.20 to 0.35 s; self-centre to under 5% in 0.6 to 1.2 s | 0.15 to 0.25 s; 0.5 to 1.0 s | [I]: soft 1980s hatches without power steering were slower to respond than modern cars; the Montego test calls the steering "dead near the straight-ahead" [READ] | GTA V is quicker than real; GTA IV slower [READ, The Drive]. Aim between them. |
| M6 roll and pitch | Roll at 0.5 g: 3 to 4.5 deg. Pitch at 0.8 g braking: 2 to 3.5 deg nose down; full throttle: 0.5 to 1.5 deg nose up | Roll 2 to 3 deg; pitch slightly less | [I]: textbook roll gradients for ordinary cars are about 4 to 8 deg per g, softer cars at the top; the measured-data paper (Systems Technology) was not reachable. The Montego test says body roll was "well resisted" [READ] | Games exaggerate roll and pitch so the player feels weight (GTA IV) [READ]. Allow up to 1.5 times real on screen, since it is cheap and sells weight. |
| M7 front load at 0.8 g braking | 75 to 82% on the front axle | 72 to 80% | est.: static front share about 60 to 63% for a front-engine front-drive hatch [I], plus transfer of 0.8 times centre-of-mass height (about 0.5 m) over wheelbase (about 2.3 to 2.45 m), so about 16 to 18 points | Not felt directly; it drives nose dive and rear twitch under braking. |
| M8 grip and slide | Highest steady lateral grip on a 40 m circle: 0.70 to 0.78 g. Slide begins gently, front first (understeer). Recovery after counter-steer: 0.5 to 1.0 s | 0.82 to 0.90 g; lifting off mid-corner swings the tail out | [I]: 1980s hatches ran narrow 13-inch tyres. Montego: "predictable understeer" [READ]. 205 GTi lift-off oversteer [READ, Autozine] | Games give more grip than real (GTA V more than IV) [READ]. Allow up to about 0.85 g for the ordinary car; keep understeer as its habit. |
| M9 handbrake turn from 30 mph | 90 to 150 deg of turn in 1.2 to 2.0 s | 120 to 180 deg in 1.0 to 1.6 s | [I]: a cable handbrake on rear drums locks the light rear of a front-drive car easily, but it is a crude tool | Games make handbrake turns far easier and wider than real [I]; harder in GTA IV than V [READ]. Allow it, but it should cost speed. |
| M10 camera | Behind: 5 to 7 m from car centre. Height: 1.6 to 2.2 m. Position lag: 0.1 to 0.3 s. Field of view: 60 to 65 deg at 0, 62 to 68 at 30, 66 to 74 at 60, 70 to 80 at 90 mph | same, slightly more widening at speed | All [I]: no published values found today. The Game Developer camera article (Pignole, 2015) lists the parameters but no numbers [READ] | Camera behaviour changes how weighty a car feels (The Drive on GTA IV) [READ]. Widening the view with speed is the cheapest way to make a slow car feel quick. |
| M11 collisions and damage | Under 5 mph: no damage, little speed lost. 5 to 15 mph: dents, lights may break, lose 30 to 60% of speed. 15 to 30 mph: panels crumple, steering pulls, smoke possible. Over 30 mph: car may not drive on | same; a little tougher at big saloons | [I], from the stages of how 1980s cars crumple; The Getaway's fragile, smoking cars [READ] | Games make cars much tougher than real so chases last [I]. Choose fragile like The Getaway, since LEDGER is not a driving game. |
| M12 sound cues | Idle about 800 to 900 rpm, limit about 6,000 to 6,500 rpm for a four-cylinder; engine note (two firings per turn) about 28 Hz at idle to about 210 Hz at the limit. Gear change: a dip of 0.4 to 0.8 s on a manual (the gearbox is automatic by default since 18 Nov: an automatic's change is a shorter, softer dip, length not yet set [I]). Tyre squeal from about 80% of the M8 grip limit. Impact sounds keyed to the M11 bands | Limit near 6,500 to 7,000 rpm | Firing frequency is plain arithmetic; rpm ranges [I] from period engines; squeal onset [I] | Games start squeal early to warn the player [I]. Keep that: it is a useful cue. |

## (c2) The game set: the default target (18 Nov 2026, provisional)

His rulings of 18 Nov: LEDGER is not a driving sim; cars feel fun and easy first, like open-world games that are not sims; 1990 is carried by sound, body sway, the look and relative speed (12:36); automatic gearbox by default (12:32). So the default target is no longer the real car widened a little: it is a game band, set where non-sim open-world games sit [I, from the reference set in (a) and the lane's judgement; no footage measured yet].

PROVISIONAL: every number in this table is a first judgement, to be replaced next week by measurements from the reference games' footage (the frame plan in (e), turned into numbers by production/lane/FOOTAGE-TO-GAME-SET-2026-11-18.md). Until then the tool checks them as written.

Automatic gearbox: the default car changes gear by itself; the drives assume it (no clutch or gear input in any script). A manual, if ever offered, is an option, not the default.

What "floor" means: the real 1990 figure is a plausibility limit on the side where a game car would feel wrong, usually slow, sluggish or clumsy. The game may go past the real car on the fun side (quicker, grippier, sharper, easier); it should not fall short of the real car on the other. For body sway the floor runs the other way, because sway is one of the things that carries 1990: the game car should move at least as much as the real one.

| Metric | Game band (provisional, default) | Real 1990 ordinary hatch (flavour) | The floor for this metric |
|---|---|---|---|
| M1 acceleration | 0 to 30 mph 3.0 to 4.5 s; 0 to 60 mph 10 to 14 s | 4.5 to 6 s; 13 to 17 s | May be quicker than real; never slower than the real car (0 to 60 over 17 s, 0 to 30 over 6 s). Relative speed must hold: the fast hatch and the big saloons stay clearly quicker than the ordinary car. |
| M2 top speed; speed after 100 m | 95 to 110 mph; 44 to 52 mph | 90 to 100 mph; 40 to 46 mph | May be faster; not below the real 90 mph top speed or 40 mph after 100 m. Stays well under the fast hatch's 118 to 122 mph so relative speed shows. |
| M3 dry braking from 30, 50, 70 mph | 8 to 11 m; 22 to 30 m; 44 to 58 m | 11 to 14; 30 to 38; 60 to 75 m (long end: the Highway Code's braking part) | May stop shorter than real (the player feels in control); never longer than the Highway Code's braking distances (14, 38, 75 m). The short end (about 1.1 g at 30 mph, est.) is beyond any 1990 car on period tyres: game licence, kept because control comes first. |
| M3 wet, as a multiple of dry | 1.3 to 1.6 | about 1.5 to 2 | Games soften the wet; the floor is that the difference stays clearly felt: never under 1.3 times dry. |
| M4 turning circle | 8.5 to 9.8 m | 9.4 to 10.5 m | May turn tighter (parking, alleys); never wider than the real 10.5 m. Still no one-go U-turn kerb to kerb on a 7.3 m street. |
| M5 steering response; self-centring | yaw to 63% after a 30 mph step 0.15 to 0.25 s; self-centring 0.4 to 0.9 s | 0.20 to 0.35 s; 0.6 to 1.2 s | May answer quicker than real; never slower than the real 0.35 s or 1.2 s. Input to response under 100 ms stays a hard rule (d, item 11). |
| M6 roll and pitch (sizes) | roll at 0.5 g 3.5 to 6 deg; pitch at 0.8 g braking 2.5 to 5 deg; pitch under full throttle 1.0 to 2.5 deg | 3 to 4.5; 2 to 3.5; 0.5 to 1.5 deg | Reversed floor: sway carries 1990, so at least the real car's movement (never stiffer than 3 deg roll, 2 deg brake pitch, 0.5 deg throttle pitch); the top stays under GTA IV's float (a). |
| M7 front load at 0.8 g braking | 72 to 82% | 75 to 82% | Not felt directly; never above the real 82%, which would mean more nose dive and rear twitch than the real car; the lower end lets the rear stay planted, which is easier. |
| M8 grip; recovery | highest steady lateral grip 0.82 to 0.92 g; recovery after counter-steer 0.3 to 0.8 s | 0.70 to 0.78 g; 0.5 to 1.0 s | May grip and recover better than real; never under the real 0.70 g or slower than 1.0 s. Understeer stays the ordinary car's habit. |
| M9 handbrake turn from 30 mph | 120 to 180 deg, settling in 1.0 to 1.6 s | 90 to 150 deg in 1.2 to 2.0 s | May swing further and settle sooner than real; never less turn than the real 90 deg or slower than 2.0 s. It should still cost speed. |
| M10 camera | distance 5 to 6.5 m; height 1.6 to 2.0 m; lag 0.1 to 0.25 s; field of view 60 to 65 deg at 0, 64 to 70 at 30, 70 to 78 at 60, 76 to 86 at 90 mph | no real figure (a camera is not a car part); the 17 Nov judgement was 5 to 7 m, 1.6 to 2.2 m, 0.1 to 0.3 s, 60 to 65, 62 to 68, 66 to 74, 70 to 80 deg | No floor from the real car. The stronger widening with speed is how relative speed reads on screen. |
| M11 collisions | unchanged from (c): fragile, like The Getaway | (c) | (c) |
| M12 sound | unchanged from (c), but automatic changes by default | (c) | Sound is one of the four carriers of 1990: period engine notes stay the target, not a game band. |

The fast set and the big saloon have no game set yet. The 17 Nov fast set overlaps the game set on braking and grip (fast grip 0.82 to 0.90 g against the game set's 0.82 to 0.92 g), so relative feel between the ordinary and fast car is not yet guaranteed; a game fast set should follow the footage numbers.

## (d) Published professional methods for car feel and car cameras

Read 17 Nov 2026. Marks: [READ] read at source today, [SS] search snippet only, [I] inference, est. estimate. Where the page read was only a summary of a talk, it says so: the talk video itself was not watched.

1. Marco Monster, "Car Physics for Games", version 1.9, Nov 2003 [READ].
Says: a car is three simple sums: engine force minus drag (grows with speed squared) minus rolling resistance (grows with speed); weight moves to the front under braking by height of centre of mass over wheelbase times deceleration; at low speed the car simply follows its wheels (turn radius = wheelbase / sin of steer angle).
LEDGER takes: the weight-transfer sum as the check for M7 (front load under 0.8 g braking) and the low-speed geometry as the check for M4 (turning circle from wheelbase and lock). Source: asawicki.info mirror.

2. Pacejka and Bakker, "The Magic Formula Tyre Model", Vehicle System Dynamics, 1992 [READ, abstract only].
Says: one fitted curve gives side force, braking force and self-aligning pull from tyre slip; its coefficients each describe one visible feature of the tyre curve (stiffness, peak, shape).
LEDGER takes: the shape to aim for in M8: grip rises with slip, peaks, then falls gently, so slide onset is felt, not sudden. Monster adds that real tyre data is rarely published [READ], so LEDGER fits to feel, not to data. Source: bengravell.github.io summary page.

3. Hamish Young (Avalanche Studios), "Vehicle Physics and Tire Dynamics in Just Cause 4", GDC 2019 [READ, session page and preview article].
Says: the Magic Formula may not suit arcade or "simcade" handling; he proposes a simpler tyre model with fewer settings that players find more forgiving.
LEDGER takes: permission to use a simple, designer-friendly tyre curve in Chaos rather than chasing simulation; tune to the M8 and M3 targets directly. Source: GDC Vault 1026035; Game Developer, 20 Dec 2018.

4. Matthew Harris (Criterion Games), "Vehicle Feel Masterclass: Balancing Arcade Accessibility with Simulation Depth", GDC 2018 [READ, session page and article].
Says: sixteen years of Criterion handling (Burnout to Need for Speed); the physics is only part of feel; camera movement, input choices and handling assists matter as much.
LEDGER takes: treat camera (M10) and assists as part of the handling sheet, not as polish added later. Source: GDC Vault 1025383; Game Developer, 2 Jul 2020 (video on GDC YouTube).

5. Three Fields Entertainment (ex-Burnout), Dangerous Driving interview, Epic Games, 22 Apr 2019 [READ].
Says: full Unreal vehicle simulation (tyres, suspension, gears, drag), tuned by a handling specialist reading telemetry across hundreds of settings; drifting swaps engine, tyre and gearbox settings for the duration; motion blur sells speed.
LEDGER takes: tune from logged numbers (the scripted drives), not by eye alone; allow a handbrake "mode" that changes tyre settings while held, which is how M9 can be hit without ruining M8. Source: unrealengine.com developer interview.

6. Turn 10, "The secrets behind the exquisite handling of Forza Motorsport", PC Gamer, Andy Kelly, 6 May 2019 [READ].
Says: the base physics is left alone; a buffer sits between stick and physics so quick taps do not spin the car, with return-to-centre tuned separately; yaw torque is clamped and scaled instead of changing the car's inertia; estimated values are flagged for later replacement.
LEDGER takes: the stick buffer and separate return rate are exactly M5 (steering response and self-centring); flag every estimated car figure in the targets sheet the same way. Source: pcgamer.com.

7. Ross McGregor, "How Grand Theft Auto IV broke the open world mould for vehicle physics", Traxion.gg, undated [READ].
Says: GTA IV exaggerates suspension softness (boat-like roll on big saloons), most cars understeer, inertia is realistic so the player must plan, braking in a straight line before a corner works best.
LEDGER takes: GTA IV is the upper bound for M6 body roll, not the target; LEDGER's 1990 saloons should roll visibly but less. Source: traxion.gg.

8. Jared Cone (Psyonix), "It IS Rocket Science! The Physics of Rocket League Detailed", GDC 2018 [READ, article only].
Says: the physics was shaped by the design (cars playing football) and by networking, not by realism.
LEDGER takes: the principle that feel targets come from what the game needs (town chases at 30 to 50 mph) before physical accuracy. Source: Game Developer, 24 Apr 2018; GDC Vault 1024972.

9. John Nesky (thatgamecompany), "50 Game Camera Mistakes", GDC 2014 [READ, article only].
Says: "cameras are most noticeable when they fail"; a tour of common camera faults and fixes from his work on Journey.
LEDGER takes: the camera passes when nobody mentions it; the reviewer checks M10 against faults (snapping, clipping, losing the car). The detailed list was not read: watch the talk before camera tuning. Source: Game Developer, 17 Nov 2015; GDC Vault 1020460.

10. Samantha Stahlke, "Prototyping a dynamic camera system", Game Developer, 19 Sep 2017 [READ].
Says: damp the camera's offset rather than chasing the target point, so it stays responsive; turn yaw in steps, not snaps, to avoid dizziness; clamp camera travel per frame to stop it passing through walls.
LEDGER takes: M10 position lag should come from damping the offset (Unreal spring arm lag) and be measured in seconds. Not a car camera, so lower weight.

11. Steve Swink, "Game Feel", 2008 (Morgan Kaufmann; review by Liz England, 26 Aug 2015) [READ, review].
Says: feel is real-time response (under 100 ms), simulated space and polish; vague words like "floaty" can be turned into measured parts.
LEDGER takes: the whole method of this sheet: every feel word gets an M number. Input to response under 100 ms is a hard rule for steering and throttle.

12. Epic Games, "How to set up vehicles in Unreal Engine" (UE 5.9 page) [READ]. LEDGER is on 5.8: the main session checks on the PC that the same settings exist in 5.8 before relying on them.
Says: torque curve as rpm against Nm (inverted U), wheel radius in cm matching the model, per-wheel engine, handbrake and steering flags, max steer angle in degrees.
LEDGER takes: max steer angle plus wheelbase sets M4; the torque curve sets M1 and M2; handbrake flags on rear wheels only for M9. The page gives no values for centre of mass or friction: those come from the scripted drives. Unread: Chaos movement component reference (page empty when fetched).

## (e) Frame-taking plan for the main session

How to take the frames (outside-only rule: watch, never download)
- Open the video in the browser at the highest quality offered. Pause with the space bar or K; the full stop key steps one frame forward, the comma key one frame back [READ, vidIQ]. Speed can be set to 0.25x in the settings cog [READ].
- Take each frame with the Windows screenshot tool (Win+Shift+S) or the builder's existing screenshot helper, saved straight into the research folder named in production/retention.json, file name: game, video ID, timestamp.
- Timing: note the player's timestamp on each frame. Frame rate of the upload decides precision (30 or 60 frames a second, check in the player's "Stats for nerds" [I]). Time between two frames = frame count divided by frame rate.
- Only use unmodded footage. Many GTA V "speedometer" videos use mods that change cars; reject them for M1 to M3.

Known lengths for measuring
- UK: hatched-area and warning-line dashes are a 4 m mark and 2 m gap at 40 mph or less, 6 m mark and 3 m gap above 40 mph [READ, Traffic Signs Manual ch. 5]. Centre-line (diagram 1008) studs sit every 12 m at 40 mph or less, 18 m above [READ]; the 1008 mark and gap themselves were not read, so the brief's "4 m line, 5 m or 9 m gap" is unconfirmed. Use the warning line (6 m repeat) near junctions as the ruler. These are today's rules; 1990 British markings may differ [I].
- US (GTA IV, GTA V, Mafia III): broken lane lines are 10 ft (3.0 m) line and 30 ft (9.1 m) gap, a 12.2 m repeat [READ, MUTCD 2009, 3A.06]. Whether Rockstar and Hangar 13 copied this exactly is not known: check against a car length first (a saloon is about 4.5 to 5 m, est.).
- Hong Kong (Sleeping Dogs): no marking standard read. Use car lengths only.

Video list (links from today's searches; pages themselves could not be opened, so descriptions are from titles only [SS])

| # | Game | Link | Moments to capture | Metrics | Confidence |
|---|---|---|---|---|---|
| 1 | Mafia III | https://www.youtube.com/watch?v=mloBuWouFCM ("Official Inside Look: Driving in New Bordeaux") | Developer's own framing of handling; any straight from standstill; cornering at a junction | M1 if HUD speed shows, M6 roll, M10 camera distance and height | Medium: official, but edited trailer cuts break timing |
| 2 | Mafia III | https://www.youtube.com/watch?v=5kmjMxykw7c ("Relaxing Drive in Muscle Car") | First pull away from standstill; hard stop at a junction; full lock turn in a side street | M1 (HUD speed [I]), M3 by lane dashes, M4 against road width, M10 lag during acceleration | Medium-high: long unedited drive [SS] |
| 3 | Mafia III | https://www.youtube.com/watch?v=i34BoahLd5Y ("New Bordeaux Drifter", 5 s drift) | Start of the slide, counter-steer, recovery | M8 slide onset and recovery time, M9 | Medium |
| 4 | GTA IV | https://www.youtube.com/watch?v=Qdeq-hMoBA8 ("Gameplay Driving Around") | Stop from cruising speed counted on lane dashes; body lean in a 90 degree turn | M3, M6 roll (measure roof tilt angle on screen), M10 | Medium: no speedometer in vanilla GTA IV, speed only from dashes per second |
| 5 | GTA IV | https://www.youtube.com/watch?v=ACt2evMb1rw ("Driving is Stressful in GTA 4, Free Roam PC") | Braking pitch (nose dive), slide in traffic, collision with a car | M6 pitch, M8, M11 speed lost in impact | Medium |
| 6 | GTA IV vs V | https://www.youtube.com/watch?v=XCsgP4oOYoE ("GTA 4 vs GTA 5 Physics Comparison") | Same manoeuvre side by side: handbrake turn, roll in a bend | M6 and M9 compared directly | Medium: check for mods first |
| 7 | GTA V | https://www.youtube.com/watch?v=VUt4VRkpAog ("Braking Distance Test, 4 vehicle comparison") | Brake point to rest for each car | M3 (dash count) | Medium-low: game not confirmed from title |
| 8 | GTA V | https://www.youtube.com/watch?v=gvusDEF3eh4 ("GTA 5 Relaxing Driving Tour") | Steady city driving: camera position when cruising, then on a hard pull away | M10 distance, height, lag, field of view from car width | Medium: check for graphics mods |
| 9 | Sleeping Dogs | https://www.youtube.com/watch?v=uuhe6bkZER4 ("Sleeping Dogs Driving, Gameplay Video") | Handbrake turns, ramming, camera pull-back at speed | M9, M11, M10 field of view widening with speed | Medium: likely publisher footage, edited |
| 10 | Sleeping Dogs | https://www.youtube.com/watch?v=kybmFm0Zdbo ("Free Roam Driving") | Pull away, junction stops, full lock U-turn | M1 by car lengths, M3, M4 | Medium |
| 11 | The Getaway (PS2) | https://www.youtube.com/watch?v=yeKnslu4pas ("First 10 Minutes", 4K 60fps) | First chase through London: braking for a junction, kerb strikes, camera behind the car | M10 (the best London camera reference), M3 using UK warning lines, M11 | Medium: no HUD at all in The Getaway, so all speeds from road markings |
| 12 | The Getaway | https://www.youtube.com/watch?v=I1dVtKTyBBY ("Timelapse, Driving Around the Map Edge") | Avoid timelapse sections for timing; use for camera framing only | M10 framing only | Low for timing |
| 13 | Forza Horizon 4 | https://www.youtube.com/watch?v=VGEmAS05ch0 ("Exploring the Edinburgh City, Spring") | British streets with HUD speed: pull away to 30 and 60 mph; brake to stop | M1 (best HUD), M2 speed at 100 m, M3 with UK markings, M10 | High for measurement, if the HUD speedometer is visible [I] |
| 14 | Forza Horizon 4 | https://www.youtube.com/watch?v=sC1-UKYL9Vw ("1984 Rover SD1 Vitesse, Car Show Speed Jump Crash Test") | A period British saloon: launch, top speed run, crash | M1, M2, M11 against a period car | High for period car, medium for town feel |
| 15 | Forza Horizon 4 | https://www.youtube.com/watch?v=WG5W9dyq0A0 ("1986 Ford Escort RS Turbo, Car Show Speed Jump Crash Test") | Same as 14 for a hot hatch of the era | M1, M2, M11 | High |
| 16 | Mafia: The Old Country | https://www.youtube.com/watch?v=gxaCX-pqnGg ("Driving Across the Entire Map") | General feel only: camera position and lag on country roads | M10 only, as a feel reference | Low (general feel only, per the brief) |

Also found: The Getaway full longplay (https://www.youtube.com/watch?v=30kPU5R6chM), useful if 11 lacks a clean braking moment.

How each metric is read from a frame
- M1, M2: with a HUD speed, step frames from the first frame the car moves to the first frame showing 30 mph, then 60 mph. Without a HUD, count dash repeats passed per second.
- M3: frame where brake lights come on (or nose dips) to frame the car stops; count dash repeats under the car. Reaction time is not included.
- M4: full-lock turn across a road; compare the arc with the road width (UK town single carriageway about 7.3 m, est.).
- M6: tilt of the roofline against the horizon in a steady bend; pitch from the bonnet line under braking.
- M10: camera field of view: car width on screen (pixels) against screen width, with the camera distance estimated from the car's known length; lag: how far the car moves up the screen in the first second of hard acceleration, and how long it takes to settle back.

Unreached or not found
- No YouTube page could be opened (failed at the site), so no timestamps, upload dates or channel names are confirmed: all video details are from search titles [SS].
- No clean unmodded GTA V acceleration video with a speedometer was found; vanilla GTA V has no speedometer.
- Talk videos (Harris, Young, Cone, Nesky) were not watched; only session pages and articles were read.
- UK diagram 1008 centre-line mark and gap lengths were not read.
- Unreal Chaos movement component reference page returned no content.


## (f) Scripted test drives

The tool is tools/lane/driving_drives.py, with plain notes in tools/lane/DRIVING-DRIVES-README.md and tests in tools/lane/test_driving_drives.py (written 17 Nov 2026).

### Why behaviour carries over, not settings

The browser prototype and the Unreal car run on different physics. If you copy the same grip, mass or spring numbers from one to the other, they still feel different. So nothing is copied across as a setting. Instead each car runs the same fixed test drives, driven by a script and never by a person, and is tuned until its measured numbers match. The browser car is tuned toward this sheet first; the Unreal car is then tuned until it matches the browser car's numbers. Because the inputs are scripted and the physics runs at a fixed step, the same drive gives the same numbers on every run, so a change in the numbers always means the car changed.

### The drives

Every drive starts from standstill at the same spot, facing forward. "Hold a speed" means the shared speed controller in the tool, which presses throttle or brake to keep that speed; "steady" means within about 0.5 mph for 2 seconds.

| Drive | Inputs | Gives |
|---|---|---|
| D1 Straight run | Full throttle, no steering, until top speed settles (under 0.1 mph gained in 5 s), at most 150 s | M1 0 to 30 and 0 to 60 mph; M2 top speed and speed after 100 m; M6 pitch under full throttle |
| D2 Braking | Hold 30, 50 or 70 mph until steady, then full brake at once, no steering, to a stop; dry, then wet | M3 braking distance from each speed, dry and wet (braking only, no thinking distance), and wet as a multiple of dry |
| D3 Turning circle | Hold 5 mph, then full right lock for a loop and a quarter | M4 kerb to kerb turning circle |
| D4 Slalom | Cones in a line every 18 m; a steering script weaves between them while holding 30 mph, then 32, 34 and so on until a run touches a cone (passes closer than 0.9 m) | Highest clean speed and the delay between steering and turning (support for M5) |
| D5 Step steer | Hold 30 mph, then step the steering to a 2 degree road-wheel angle, hold 2 s, let go | M5 time to 63% of the settled turn rate; self-centring time to under 5% after letting go |
| D6 Steady circle | Follow a 40 m radius circle while the speed rises slowly (0.15 m/s each second from 15 mph) until the car runs 2 m wide; then lift off and steer the wheels where the car is going | M8 highest steady sideways grip (g), the speed it slid at, recovery time; M6 roll at 0.5 g |
| D7 Handbrake turn | Hold 30 mph, then full lock and handbrake at once for 0.6 s; then handbrake off, steering straight, full brake until stopped | M9 how far the car turned (degrees) and how long the turn took to settle (s) |
| D8 Camera run | One second at rest, then full throttle to 90 mph | M10 camera distance and height at rest, lag, field of view at 0, 30, 60 and 90 mph |
| D9 Pitch and roll | No run of its own: read from D2 (pitch and front load share at 0.8 g braking) and D6 (roll at 0.5 g) | M6, M7 |

M11 (collisions) and M12 (sound) are not measured by scripted drives yet.

### What each drive writes

Each run writes one telemetry file, one row per physics step, in the format the README sets out: time, position, heading, speed, turn rate, sideways and forward g, roll, pitch, front load share, the applied steering, throttle, brake and handbrake, the drive's stage, and the camera's distance, height, field of view and lag. The browser game and the Unreal car both export this same format, so one tool measures both.

### The game bands the drives check (game set, the default)

Provisional until next week's footage measurements (section c2). Automatic gearbox by default.

| ID | Number | Band |
|---|---|---|
| M1 | 0 to 30 mph; 0 to 60 mph | 3.0 to 4.5 s; 10 to 14 s |
| M2 | top speed; speed after 100 m | 95 to 110 mph; 44 to 52 mph |
| M3 | dry braking from 30, 50, 70 mph; wet | 8 to 11, 22 to 30, 44 to 58 m; wet 1.3 to 1.6 times dry |
| M4 | turning circle | 8.5 to 9.8 m |
| M5 | response (63%); self-centring | 0.15 to 0.25 s; 0.4 to 0.9 s |
| M6 | roll at 0.5 g; pitch at 0.8 g braking; pitch at full throttle | 3.5 to 6; 2.5 to 5; 1.0 to 2.5 deg |
| M7 | front load at 0.8 g braking | 72 to 82 % |
| M8 | highest steady lateral grip; recovery | 0.82 to 0.92 g; 0.3 to 0.8 s |
| M9 | handbrake from 30 mph | 120 to 180 deg turned, settled in 1.0 to 1.6 s |
| M10 | camera behind, up, lag; field of view at 0, 30, 60, 90 mph | 5 to 6.5 m, 1.6 to 2.0 m, 0.1 to 0.25 s; 60 to 65, 64 to 70, 70 to 78, 76 to 86 deg |

The numbers the drives give with no band in any set (wet distances in metres, slalom speed and lag, slide onset speed, field of view widening) are shown but never fail. M11 and M12 are not measured by the drives.

Named alternatives, kept from 17 Nov and chosen by name in the tool:

Ordinary set (the real 1990 small hatch widened by the allowed game departures):

| ID | Number | Band |
|---|---|---|
| M1 | 0 to 30 mph; 0 to 60 mph | 3.6 to 6.0 s; 13 to 17 s |
| M2 | top speed; speed after 100 m | 90 to 100 mph; 40 to 46 mph |
| M3 | dry braking from 30, 50, 70 mph; wet | 9.5 to 14, 25.5 to 38, 51 to 75 m; wet 1.5 to 2 times dry |
| M4 | turning circle | 9.0 to 10.5 m |
| M5 | response (63%); self-centring | 0.20 to 0.35 s; 0.6 to 1.2 s |
| M6 | roll at 0.5 g; pitch at 0.8 g braking; pitch at full throttle | 3 to 6; 2 to 5; 0.5 to 2.25 deg |
| M7 | front load at 0.8 g braking | 75 to 82 % |
| M8 | highest steady lateral grip; recovery | 0.70 to 0.85 g; 0.5 to 1.0 s |
| M9 | handbrake from 30 mph | 90 to 150 deg turned, settled in 1.2 to 2.0 s |
| M10 | camera behind, up, lag; field of view at 0, 30, 60, 90 mph | 5 to 7 m, 1.6 to 2.2 m, 0.1 to 0.3 s; 60 to 65, 62 to 68, 66 to 74, 70 to 80 deg |

Fast set (a 1990 fast hatch): 0 to 60 in 8 to 9 s; top speed 118 to 122 mph; braking from 30, 50, 70 mph 8.5 to 12, 24 to 33, 47 to 65 m; roll at 0.5 g 2 to 4.5 deg; lateral grip 0.82 to 0.90 g; the rest as the ordinary set, 0 to 30 and speed after 100 m left open.

### Pass rules

- Against this sheet: each number must sit inside its band, edges included. Three sets can be chosen by name: "game" (the default, provisional), "ordinary" and "fast" (the 17 Nov real-car-based alternatives). Numbers with no band yet are shown but do not fail.
- Unreal against the browser: each number must be within 5% of the browser's number, or within a fixed allowance by unit if that is larger: 0.05 s, 0.3 m, 1 mph, 0.3 degrees, 1 percentage point of load share, 0.02 g. A number one car gives and the other does not is a fail.
- Both rules are checked by the tool's compare step, which writes a pass or fail for every number.

### Choices to know about

- D1 runs until the top speed settles rather than for 30 s, because a 1990 hatch takes over a minute to get near its top speed.
- Readings at 0.5 g and 0.8 g come from a straight line through the run's samples, because a hatch brakes at about 0.65 to 0.7 g and may never reach 0.8 g on its own.
- The tool's small Python reference car exists only to test the tool. It meets every band in the ordinary set, which proves the measuring works, not how LEDGER's car should be built. It is not retuned for the game set (against it, the reference car is about 0.7 s slow to 30 mph, short of top speed, grip and handbrake swing, brakes long and turns too wide), so the tool checks it against the ordinary set.

## (g) What the browser cannot prove

The browser test can prove numbers: times, distances, angles, how quickly the car answers. It cannot prove how the car looks, sounds and holds up in the real game. These are judged in the Unreal game, against the same targets, in the packaged release build.

| Area | What the real game checks | How |
|---|---|---|
| Damage and deformation | That the M11 bands look right: dents at low speed, crumpled panels and broken lamps in the middle band, a car that will not drive at the top; panels on real hinge lines; no damage passing through glass or wheels | Scripted crashes at 5, 10, 20, 30 and 40 mph into a wall, a post and another car; still frames from four sides; compared with period crash photographs and with The Getaway and GTA IV footage played in the browser |
| Interiors | Dashboard, seats, wheel and mirrors read as a plain 1990 car, no brand, seen through glass and from the driver's seat if used | Close frames against period interior photographs; gate review |
| Engine sound quality | That it sounds like a small four-cylinder and follows the M12 pitch range, gear dips and squeal onset | Recorded passes at 20, 30 and 50 mph and a full-throttle run; pitch measured against rpm; listened to by ear against period recordings |
| How speed looks | That 30 mph in a street feels like 30 mph: motion blur, road texture, kerbs and lamp posts flowing past at the edges, the M10 view widening | Side by side clips at 30 and 60 mph with GTA IV and Forza Horizon 4 footage played in the browser; his short playtest; frame checks that blur does not smear signs |
| Performance with traffic | Frame time stays in budget with the player's car, traffic cars and pedestrians at once, including during a crash | Scripted drive through the busiest street with the planned traffic count, frame times logged (see the frame-time method note), worst one percent of frames compared with the budget |
| Feel on a real pad and wheel | That the tuning carried over from the browser still meets M1 to M10 under the Unreal vehicle system | Rerun the same scripted drives in Unreal and compare each metric with the browser result; any gap beyond the 5% rule of (f) (or its fixed allowance by unit) is a finding |


## Sources

### For (a), (b), (c) and (g)

- Adam Ismail, "GTA 6 driving physics hint at return to the realism of GTA 4", The Drive, 21 Aug 2026 [READ]: thedrive.com
- Elise Favis, "Mafia III's driving mechanics are inspired by 1960s Hollywood films", Game Informer, 7 May 2016 [READ]
- Twinfinite, Mafia III simulation driving guide, 2016 [SS]
- GameSpot, Sleeping Dogs review, 2012 [READ, no date or author on the fetched page]
- Traxion.gg, "The Getaway: Grand Theft Auto with licenced cars" [READ, undated]
- Mike Channell, "Forza Horizon 4 review", Top Gear, 1 Oct 2018 [READ]
- Yoann Pignole, "Third-person camera design with free move zone", Game Developer, 28 Sep 2015 [READ]
- Autocar, "Austin Montego 1.6L road test", 19 May 1984, Throwback Thursday reprint [READ]
- Autozine, Peugeot 205 GTI archive page, citing Autocar and Motor tests [READ]
- Encycarpedia: Ford Fiesta 1.1 (1989) and VW Golf 1.6 (1983) [READ]
- auto-data.net: Vauxhall Nova 1.2 S [READ]
- Carbaze: Austin Metro 1.0 (1987), Ford Escort 1.3 L Mk4 (1986), Ford Sierra 1.6 GL (1985) [READ]
- Unique Cars and Parts: Austin Montego 1.6 L (1984), Rover 820 Si (1986), Ford Granada 2.8i (1986) [READ]
- Driving Theory 4 All, stopping distances table [READ]; Tom Wiltshire, Auto Express, 24 Feb 2016 [READ]
- Classics World, "Is it time for a stopping distance rethink?" [READ, undated]
- Zeperfs, 205 GTI 1.6 page [READ, figures partly garbled]

Unreached today: Systems Technology paper on measured roll gradients (permission timed out); Parkers spec pages for Nova and Cavalier (site error); cars-data.com Metro and Golf pages (site error); SAE paper 880324 on 1988 braking with and without ABS (page did not load); the Highway Code itself (wet-road wording). No period Autocar or What Car braking or turning-circle figures were reached; these should be read from the PC before the M3 and M4 targets are locked.

### For (d) and (e)
- Monster, M., Car Physics for Games v1.9, Nov 2003: https://asawicki.info/Mirror/Car%20Physics%20for%20Games/Car%20Physics%20for%20Games.html [READ]
- Pacejka and Bakker 1992, summary: https://bengravell.github.io/knowledge-base/papers/1992_pacejka_the_magic_formula_tyre_model/ [READ]
- Young, GDC 2019: https://gdcvault.com/play/1026035/Vehicle-Physics-and-Tire-Dynamics [READ]; https://gamedeveloper.com/design/get-under-the-hood-of-i-just-cause-4-i-s-vehicle-physics-at-gdc-2019- (20 Dec 2018) [READ]
- Harris, GDC 2018: https://gdcvault.com/play/1025383/Vehicle-Feel-Masterclass-Balancing-Arcade [READ]; https://gamedeveloper.com/design/video-balancing-accessibility-with-depth-to-make-vehicles-feel-great (2 Jul 2020) [READ]
- Three Fields Entertainment interview, 22 Apr 2019: https://www.unrealengine.com/developer-interviews/three-fields-entertainment-explains-how-they-evolved-burnout-arcade-racing-formula-dangerous-driving [READ]
- Kelly, PC Gamer, 6 May 2019: https://www.pcgamer.com/uk/the-secrets-behind-the-exquisite-handling-of-forza-motorsport/ [READ]
- McGregor, Traxion.gg, undated: https://traxion.gg/how-grand-theft-auto-iv-broke-the-open-world-mould-for-vehicle-physics/ [READ]
- Cone, GDC 2018: https://gamedeveloper.com/design/video-the-rocket-science-behind-i-rocket-league-s-i-physics (24 Apr 2018) [READ]
- Nesky, GDC 2014: https://gamedeveloper.com/design/video-50-common-game-camera-mistakes----and-how-to-fix-them (17 Nov 2015) [READ]; https://gdcvault.com/play/1020460/50-Camera [SS]
- Stahlke, 19 Sep 2017: https://gamedeveloper.com/design/prototyping-a-dynamic-camera-system [READ]
- England, review of Swink's Game Feel, 26 Aug 2015: https://lizengland.com/blog/review-game-feel-by-steve-swink/ [READ]
- Epic, How to set up vehicles (UE 5.9): https://dev.epicgames.com/documentation/unreal-engine/how-to-set-up-vehicles-in-unreal-engine [READ]
- Traffic Signs Manual chapter 5 (2018/19): https://assets.publishing.service.gov.uk/media/5c4ace6ded915d38a0611abc/traffic-signs-manual-chapter-05.pdf [READ, first part]
- MUTCD 2009, section 3A.06: https://mutcd.fhwa.dot.gov/htm/2009/mutcd2009cl_3.htm [READ]
- vidIQ, YouTube frame by frame: https://vidiq.com/blog/post/youtube-frame-by-frame/ [READ]
- YouTube links in the table: search results only [SS].
