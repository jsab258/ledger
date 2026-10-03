# 2. Feasibility: every area against the constraints

## The constraints

- **Agents:** the work is done by AI agents.
- **Money:** almost none. No purchases without his yes, none for the street or cars, no paid voice service.
- **Card:** one AMD RX 6700, 10 GB, shared with the voice.
- **Licences:** AI use allowed, anything marked NoAI excluded. A clause only against training is allowed while nothing we send trains a model (3 October).
- **No hiring.**
- **Bar:** the Hook sheet and the KCD2 frames for visuals, except clothes, which have their own floor. For the systems, the bar is the Meridian Test's conditions: the town visibly knows them, talking feels live, he would rather play it.

## Marks

- Per constraint: **✓** fits, **!** conflicts or is at risk, **?** unknown, **–** does not apply.
- **Verdicts:**
  - **FEASIBLE:** the method works here already, or is known and cheap. Any **!** in its row has a named, cheap fix.
  - **RISKY:** a constraint is in conflict with no known cheap fix, or the method has failed here.
  - **UNKNOWN:** nothing measured or tried decides it.
- **Evidence:** from the repository at 79cf8db (3 October). H4a and H4b are this review's evidence notes, summarised in SOURCES.md. Facts checked here are marked "read here".
- **Proof:** the cheapest one that settles the area (3-PROOFS.md).

Clothing and live voices were known to be risky. **The table finds twenty-three more risky areas and four unknown ones.**

## The table

| # | Area | Agents | Money | Card | Licences | No hiring | Bar | Verdict | Reason | Proof |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Buildings and facades | ✓ | ✓ | ? | ✓ | ✓ | ! | **RISKY** | No free 1990 British kit exists, so everything is made (asset plan, family 1). Every whole street frame since 1 Oct failed a fresh reviewer or Jafar (DECISIONS lines 196 and 235). The parade's bays are identical. The brick is laid in stretcher bond, wrong for a Victorian wall (terrace-front.py line 5672). Composition, item 2.1, failed two reviews. The kit method is planned, not proven. | P10 |
| 2 | Shopfronts, rooms behind glass | ✓ | ✓ | ? | ✓ | ✓ | ! | **RISKY** | Rita's window passed (2 Oct). Seven more made the same way failed three reviews on 3 Oct: goods made in code "read as toys", and projected rooms smear at 1–3 m. The real-room pipeline exists but has never been shown or measured. | P11 |
| 3 | Interiors (Mickey's office) | ✓ | ✓ | ? | ✓ | ✓ | ? | **UNKNOWN** | A grey blockout behind a flag nothing passes. The first camera trial failed: the arm collapses at the door, and Tom's back fills half the frame (production/research/third-person-camera-interiors/NOTE.md). Scope conflicts: "kept for later" (DECISIONS 1 Oct) against basic 14, "Mickey's office enterable". | P15 |
| 4 | Ground and materials | ✓ | ✓ | ✓ | ✓ | ✓ | ! | **FEASIBLE** | Its faults are named and their method is researched: projected decals, the wet road (aaa-street PUDDLES), Poly Haven and ambientCG surfaces in place of Megascans. Open: the bond, repeating cracks, flags that read as tiles. These are fixes, not unknowns. | with P10 |
| 5 | Props and street clutter | ✓ | ✓ | ✓ | ✓ | ✓ | ! | **RISKY** | Nine pieces made by script passed the gate on 29 Sep, but Jafar called the phone box among them a placeholder on 1 Oct (DECISIONS line 196). About 25 kinds of furniture are still to make (asset plan, family 4). Poly Haven CC0 covers crates, drums and buoys. The cost is unmeasured but small (950–7,548 triangles each, counted by H3). | P22 |
| 6 | Food and shop goods | ✓ | ✓ | ✓ | ! | ✓ | ! | **RISKY** | The main source, Megascans food, is NoAI and out (3 Oct). The CC0 fish and fruit scans on Sketchfab (ffishAsia) have not been fetched or tag-checked. No allowed source exists for ice, fillets, dressed crab, sweets in jars or scones (shop-window-interiors/GOODS-2026-10-03.md). Code-made goods failed. | P16 |
| 7 | Signage, posters, text | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | **FEASIBLE** | Our own text in OFL fonts works: name plates, boards, labels. Names are minted by the town on Monday. Open faults to retire: the image-model sign batch ("BRITHH WORIKER", a back bar, bingo), the brand bible's "pub". | – |
| 8 | The hill, vegetation, distance | ✓ | ✓ | ? | ✓ | ✓ | ! | **RISKY** | The hill is boxes, judged so by Jafar (1 Oct) and a reviewer (3 Oct). His ruling is "built properly, never hidden". It depends on the building kit existing first. Vegetation has CC0 sources (Poly Haven, ambientCG) but none is in the street. | P19 after P10 |
| 9 | Sky and atmosphere | ✓ | ✓ | ✓ | ✓ | ✓ | ! | **RISKY** | The overcast light and the haze work (2 Oct). Cloud structure failed two tries; item 2.2 asks for "the sky not white". There is no rain, dusk or chimney smoke in the code, though canon says "weather and grime are the strategy". Rain matters only if he rules it into the thirty minutes. | P20 |
| 10 | Light by day and night, the grade | ✓ | ✓ | ? | ✓ | ✓ | ! | **RISKY** | The night was "one flat orange" (1 Oct), then corrected by values. No grade is built: engine defaults only, D28 owed. A face seen in passing is underlit and "reads East Asian" (FINDINGS). The quay is black at night. | P20 |
| 11 | Cars | ! | ! | ? | ! | ✓ | ! | **RISKY**, with a fallback | No free, allowed, period, fictional car exists. Paid packs are refused, and AI 3D generators give melted shells (TRELLIS needs NVIDIA). The scripted box car failed. Epic's automotive materials are reported NoAI [SS]. The fallback is none: "no cars is better than box cars" (2 Oct). The Hook sheet has cars. | P9 |
| 12 | Faces: Tom, the other eleven principals, the regulars | ! | ✓ | ✓ | ✓ | ✓ | ! | **RISKY** | Sheila's and Darren's faces failed the blind reviewer against their concept portraits and were finished from measurements (DECISIONS line 81). FINDINGS still says they "fail their sheets". Only three female presets read white European. **Tom, the player, on screen in every frame of a third-person game, is still Mixamo's "Adam" in a grey tracksuit** (SliceCharacter.cpp; production/archive/DECISIONS-to-2026-09-24.md line 191). Eleven sheets are text only. The face route depends on Epic's cloud rigging service. | P8 |
| 13 | Hair | ! | ✓ | ? | ! | ✓ | ! | **RISKY** | Only the MetaHuman plugin's library grooms are clean; Fab grooms are NoAI. The library has no 1990 set or perm (faces-and-hair note). Blender curls failed three tries. Strands cost against cards is unmeasured. | with P8 |
| 14 | Bodies and builds | ! | ✓ | ✓ | ✓ | ✓ | ? | **RISKY** | Three spare builds came out identical, three times. The cause is known: the export reads the saved rig unless re-rigged in the same session, and each build needs Epic's cloud rig. No body exists for Tom, Ellis, Agar or Jensen. | with P8 |
| 15 | Clothes | ! | ! | ✓ | ! | ! | ! | **RISKY** (known) | Every tailored route failed (six routes, 24 Sep to 2 Oct). Epic's garments are out by licence, every ready-rigged suit read is NoAI, and no purchases or commissions. The 3 Oct floor and the 8 m crowd rule lower the bar, but nothing meets the floor today. Whether the cast wear a T-shirt and shorts or the withdrawn blouse could not be settled from the records. | P6 |
| 16 | Animation: idles, walks, poses | ✓ | ✓ | ✓ | ! | ✓ | ! | **RISKY** | The planned source, Epic's Game Animation Sample, is NoAI and out. What is left: MetaHuman's own 31 locomotion clips (its stand idle was rejected as "a game hero's ready pose", 3 Oct) and Mixamo, whose "starts, stops and turns rarely match its walks". All three cast share one female technical idle with the head held 70% rigid. Walkers' feet slide. | P7 |
| 17 | Townspeople and crowds | ! | ✓ | ! | ! | ✓ | ! | **RISKY** | Only three people have bodies; three Mixamo stand-ins "jump out at night". The street's people do not perceive (against D25). Twenty people are estimated at 2–5 ms of GPU and 2–3 GB, none measured. Epic's crowd samples are reported NoAI [SS]. Clothes and animation (15, 16) carry over. | P6 |
| 18 | Mouths and faces in speech | ! | ✓ | ? | ✓ | ✓ | ! | **RISKY** | The loudness mouth was judged "only open and close" (1 Oct). Epic's streaming speech-to-face solver in the 5.8 install was never tried; its cost and its AMD route are unknown. Prepared lines use Epic's offline faces. | P12 |
| 19 | Performance and graphics memory | ✓ | ✓ | ! | ✓ | ✓ | – | **RISKY** | The sparse slice's slowest 1% already sits on 16.7 ms (3 Oct). That leaves 1.5–2.8 ms of GPU for everything the proof view adds, less at the 55% the game draws (4-BUDGETS.md). The game already uses the whole 6.0 GB memory envelope beside the voice. The voice needs 2.8 GB and crashed when squeezed (1 Oct). The asset plan assumes Nanite and virtual shadows; the game runs neither. Walking: 23 of 847 frames over 33 ms. | P1 |
| 20 | Live talk (the language model) | ✓ | ! | – | ✓ | ✓ | ! | **RISKY** | On a fresh set of 60 questions, 48 of them answerable, "that's all I know" came 23–25 times (30 Sep, on the bench, not the real path; grounded-replies/RULES-2026-09-30.md). 7% of turns carry an invented detail. **A spending budget switches the claim check off**: `engine.Checker` is set only when the client is an `AnthropicClient`, and the budgeted client is not one (ledger/TalkHelper/Program.cs line 273; BudgetedClient.cs line 23; read here). So the AI tester's in-game run of 30 Sep ran unchecked. The off-game cost sample that day was checked, but the sample tool now sets a budget too (talk_cost_sample.py line 202). Cost is $1.07–3.22 an hour (30 Sep). The action router was never wired into the game. | P3, P4 |
| 21 | Voices (text to speech) | ✓ | ✓ | ! | ✓ | ✓ | ! | **RISKY** (known) | First sound 5.41 s median, none of 30 within 2 s (30 Sep, real path). Every free speed route failed beside the game. Jafar finds the voices flat. Accents drift American. Per-line emotion was never built. VCTK consent is a stated risk. | P2 |
| 22 | The simulation and its C++ port | ✓ | ✓ | ✓ | ✓ | ✓ | ? | **RISKY** in reaching play | A deterministic Core, 57,872 golden rows agreeing. But 12 one-line mutations of new C++ code passed the comparison (review of 1 Oct, D1). Town news, overheard gossip, temperaments and the arrival are built or ported and never reach play. "The town visibly knows them" is measured on paper, not in the game. | P4 |
| 23 | Crime, police, arrest | ✓ | ✓ | ✓ | ✓ | ✓ | ? | **RISKY** in presentation | One crime (Rita's window) leads to an arrest, all shown as text captions. No constable or detective has a body. The threat rule changed three times in four days. | P4 |
| 24 | Combat (fists, improvised weapons) | ? | ✓ | ? | ! | ✓ | ? | **UNKNOWN** (scope) | Ruled in (G3, 23 Sep); "must not look broken" (D24). Nothing in the game; C# only. The pose sources are limited to MetaHuman clips and Mixamo. Whether it belongs in the thirty minutes is not ruled. | his scope ruling first |
| 25 | Thirty minutes of content | ✓ | ✓ | – | ✓ | ✓ | ? | **RISKY** | **No thirty-minute session has ever been played or recorded**, by a person or the tester. The scripted route walks one day in 11 stages with stand-in talk. Only three people can be talked to. Ada and June, two of the first hour's "day-one five", have no body or talk. No office, notebook or coat. | P4 |
| 26 | Save and load | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | **FEASIBLE** | Quit, relaunch and continue are walked by script (0.00 m off). Only Low faults are open. | – |
| 27 | Interface, controls, controller | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | **FEASIBLE** | Built as approved, at both screen sizes, with a controller. | – |
| 28 | Sound, ambience, foley | ✓ | ✓ | ✓ | ? | ✓ | ? | **RISKY** | CC0 only (D26). The street is near-silent: one generated traffic bed, footsteps, a few crowd lines. No rain, wind or office sound, and no record of a glass-break on the smash. No CC0 library brought in beyond the footsteps. | P13 |
| 29 | Music and the radio | ? | ✓ | ? | ? | ✓ | ? | **UNKNOWN** | No direction. The allowlist names MusicGen, whose weights' licence for this use was not checked here. THIRD-PARTY.md's music line is Unity-era. | his scope ruling first |
| 30 | The AI tester and testing | ✓ | ✓ | ! | ✓ | ✓ | – | **FEASIBLE**, with gaps | Scripted walks and screenshot free play work. But everything runs on Development builds; no Shipping build exists. The tester's one real-talk run was unchecked. The nightly "does the town know Tom" walk is not scheduled. The tester shares the card and the PC with the build machine. | P4, P5 |
| 31 | The friends' build itself | ✓ | ✓ | ? | ✓ | ✓ | ? | **UNKNOWN** | **The game reads the key from the current Windows user's folder** (`%LOCALAPPDATA%\LEDGER\live-talk-key.txt`, CrimeProbe.cpp line 3248; read here). A fresh account has none, so talk goes "offline" unless the key file is put there. The portable voice folder has never been started in a fresh account. Six of the twenty basics are not met by the records. | P5 |
| 32 | Live-talk cost and the key | ✓ | ! | – | ✓ | ✓ | – | **RISKY** | Steady talk costs $1.07–3.22 an hour. **Two of his rulings conflict.** The key serves "his live play, and measurement runs by any session, at most one dollar a day", and "nothing else uses it" (DECISIONS line 257, 3 Oct). The friends' build runs on his PC with no relay (line 200, 1 Oct), so friends' talk can only use the key, which the letter of 3 October excludes. The key's monthly cap is not in the repository; at the cap every call fails. | his ruling; P3 |
| 33 | Disk, retention, git | ✓ | ✓ | – | ✓ | ✓ | – | **FEASIBLE**, watched | Retention runs nightly and checks space before each job (2 Oct). But F: is about 111 GB in all, and read 27 GB or 40 GB free on 3 Oct (two records disagree). The public history is 32.5 GB (GitHub API, read here); cleaning it is his decision. | – |
| 34 | Build machine, CI | ✓ | ✓ | ! | ✓ | ✓ | – | **FEASIBLE** | All checks green on 5db99d5. Each run holds his PC's card for 30–40 minutes. Two overlapping builds failed before (28 Sep). | – |
| 35 | The way of working (agents) | ! | ✓ | – | – | ✓ | – | **RISKY** | The builder's order was replaced six times in four days, and licence rulings reversed four times. More than twelve items went past the two-tries rule. The builder holds 17 of the twenty basics and every port. Of 440 rulings, 19 were built nowhere (1 Oct). Agents cannot judge looks: every visual waits on the eye. | P21 |
| 36 | Legal: terms, disclosure, the public repository | ✓ | ✓ | – | ! | ✓ | – | **RISKY** | The Unreal EULA, MetaHuman and Mixamo AI clauses are known only from search summaries. The allowlist still admits the Game Animation Sample. The approved Steam disclosure says every line is checked, which is untrue for capped runs (his own play is checked), and that talk goes through our server, which is untrue while the relay is not hosted. **The repository is public** (GitHub API: `private=false`, read here) and holds KCD2 and GTA V screenshots described as "not redistributed". Whether "Help improve Claude" is off is not confirmed. | P14 |
| 37 | Accessibility | ✓ | ✓ | ✓ | ✓ | ✓ | – | **FEASIBLE** | Subtitles, sizes, presets and remapping research exist. The fuller set is marked "later". | – |

## What the table says

- **Twenty-five areas are risky, two of them the known ones, and four unknown**, against eight feasible, two of them with gaps.
- **The risk sits mostly in people, look and talk**, not in the systems a studio usually fears. Save, the interface, props, signage and the build machine are sound.
- **Three risky areas outweigh the rest for a thirty-minute build:**
  - **talk** (20, 21, 32);
  - **people on screen** (12 to 18, with Tom in a stand-in tracksuit for the whole session);
  - **thirty minutes of content never once played end to end** (25).
- **Three findings are cheap to fix:**
  - the claim check off under a budget (20): first reported by the rulings sweep on 1 Oct, still in the code at 79cf8db;
  - the key missing in a fresh account (31), new here;
  - the disclosure's false claims and the public repository (36), new here.

## What could not be verified

- **How anything made on 3 October looks.** The frames are on his PC.
- **What the cast wear in today's build.** The overview and garments.json disagree.
- **Every cost marked unmeasured,** in particular rooms, crowds, cars, cloth and the face solver.
- **Whether "Help improve Claude" is off.**
- **The key's monthly cap.**
- **The portable voice folder's size.**
- **The free space on F:.**
- **Everything that rests on unreached terms:** the EULA, Mixamo, Steam's survey and the Fab EULA.
