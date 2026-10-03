# 3. The cheapest proof that settles each risky or unknown area

Each proof is small, runs on his PC, and ends in a number or a reviewer's verdict that decides the area. Several are already partly on the builder's list. The rest would join it only by his order at a stated position (CLAUDE.md, "The one list"). This review changes no list.

**Order.** Highest risk first, cheapest first within that. P3, P5 and P14 together take about two days and cost under a dollar. They settle three of the review's new findings.

| Proof | Settles areas (2-FEASIBILITY.md) | Days | Dollars | Owner |
|---|---|---|---|---|
| P3 Checked talk, measured on the real path | 20, 32 | 1 | ≤ 0.55 | town (fix), builder (run) |
| P5 The friends' build in a fresh Windows account | 31, 30 | 0.5–1 | 0 | builder; Jafar for the account |
| P14 The terms, read from his PC | 36, 6, 29 | 0.5 | 0 | builder; Jafar for one ruling |
| P1 Profile the hook camera | 19, and every budget in 4-BUDGETS.md | 1–2 | 0 | builder |
| P4 One thirty-minute session, played and counted | 25, 22, 23, 20 | 1 | ≤ 1 | builder (tester) |
| P2 The voice off the card, timed beside the game | 21, 19 | 2 (list item 3) | 0 | builder |
| P8 Tom and one more principal, judged blind | 12, 13, 14 | 2–3 | 0 | builder; Jafar for faces |
| P7 Idles and walks without the Game Animation Sample | 16 | 1–2 | 0 | builder |
| P6 One coat at 8 m on three bodies, and twelve people's cost | 15, 17 | 3–5 | 0 | clothing, builder |
| P10 One house of the building kit at the bar | 1, 4 | 2 | 0 | builder |
| P11 One real room behind glass, measured | 2 | 1–2 | 0 | builder |
| P16 Food from allowed scans | 6 | 1 | 0 | builder, from his PC |
| P9 A fictional car's silhouette, blind | 11 | 1 | 0 | builder |
| P19 The hill from the kit | 8 | 1–2 (after P10) | 0 | builder |
| P20 A grey card: night exposure, faces in passing, the sky | 10, 9 | 1 | 0 | builder |
| P15 Mickey's office camera, walked | 3 | 1 | 0 | builder |
| P12 Epic's streaming face solver on one live line | 18 | 1–2 | 0 | builder |
| P13 A CC0 ambience bed | 28 | 1 | 0 | builder; Jafar's ear |
| P17 Combat, if ruled in | 24 | 2 | 0 | town, builder |
| P18 Music, if ruled in | 29 | 0.5 | 0 | builder |
| P21 One week against a dated plan | 35 | 30 minutes a week | 0 | builder |
| P22 The phone kiosk remade, and the kerbside run | 5 | 0.5 for the kiosk | 0 | builder |

Days are this review's estimates [I], in builder-days.

---

## P3. Checked talk, measured on the real path

**Why.** The claim check is off whenever a spending budget is set. `engine.Checker` is attached only when the client "is AnthropicClient" (ledger/TalkHelper/Program.cs line 273). The budget wraps the client in `BudgetedClient`, a separate class that is not one (Program.cs lines 1433–1444; BudgetedClient.cs line 23; read here). The AI tester's `--real-talk` sets a budget. So the only in-game measurement of real talk (30 September: words 1.91 s, first sound 5.41 s, $0.23 for 30 lines) ran unchecked, and Steam's approved disclosure ("every line is checked before you hear it") is untrue for such runs.

The off-game cost sample of the same day was checked: it logs "check 4.2 s (21 turns)". But `talk_cost_sample.py --live` now sets a budget too (line 202, read here), so its next live run would be unchecked. Jafar's own play sets no budget and is checked. The rulings sweep first reported this on 1 October (production/audits/rulings-sweep/SUMMARY.md line 166); it is still in the code at 79cf8db.

**Do.**
1. Write a test from the design that fails today: a budgeted real client gets a checker.
2. Fix the condition so it looks through the budget to the real client. This is town code: the Core and TalkHelper.
3. Re-run the AI tester's `--real-talk` in the packaged game. **Its cap is $0.50 in code** (tools/ai-tester/play.py line 82, read here), set for the one run of 30 September (DECISIONS line 173). Thirty checked lines cost about $0.54 at the measured $0.0179 a turn, so the run would be cut short. Either run 25 lines, or raise the constant inside his ruling of 3 October (measurement runs, at most $1 a day in all). The constant is a code change for the builder.
4. Record words on screen, first sound, cost, fallbacks, "that's all I know", and invented details labelled by a fresh reviewer.

**Pass.**
- The numbers are recorded on the checked path.
- The disclosure is either true or sent to Jafar to amend.
- Cost per 30 minutes of talk is known (feeds area 32).

**Cost.** One day; about $0.45–0.55, inside the key's day.

## P5. The friends' build in a fresh Windows account

**Why.** The game reads the key from `%LOCALAPPDATA%\LEDGER\live-talk-key.txt` (CrimeProbe.cpp line 3248, read here). A fresh account has its own LOCALAPPDATA, so talk would start "offline". The portable voice folder has never been started outside his account. Everything is packaged as Development (`-clientconfig=Development`, ledger-probe-unreal.yml line 555, read here).

**Do.**
1. In a fresh local account, start the game from a shortcut, with nothing else installed for that account.
2. Decide how the key reaches it: a copy in that account's folder, or a machine-wide path. This is a money and security choice for Jafar, since friends play beside the key.
3. Play ten minutes.
4. Time to title, first reply and first voice; record disk use and anything that needed his account (Python, .NET, runtimes).
5. Repeat with one Shipping package.

**Pass.** Talk and voice work from the shortcut, and the list of what had to be added is empty or written down.

**Cost.** Half a day to a day. Creating a Windows account needs his yes and an administrator.

## P14. The terms, read from his PC

**Why.** The Unreal EULA's AI clause, the MetaHuman terms, Mixamo's terms, Steam's AI survey and the Fab EULA are all known only from search summaries. Every cloud session was refused those hosts (production/research/asset-plan/0-SOURCES-AND-LICENCES.md; H2 here). The NoAI ruling of 3 October removed 42 items in a day. The same pattern can repeat on what is left.

**Do.**
1. From his PC, save the dated text of each clause.
2. Record whether "Help improve Claude" is off: his settings, or his word.
3. Then correct the records:
   - the allowlist's entry 8 (it still admits the Game Animation Sample, read here) and entry 3;
   - THIRD-PARTY.md rows for the shipped voice engine (Chatterbox Nano, MIT), its runtimes (PyTorch, DirectML) and the language model's terms;
   - the disclosure's two claims, after P3.
4. One ruling for Jafar: **the repository is public** (GitHub API `private=false`, read here). It holds KCD2 and GTA V screenshots that THIRD-PARTY.md calls "not redistributed". Making it private has a money side: GitHub's free minutes for private repositories would then pay for the Linux core tests [I; GitHub's current terms not read here].

**Pass.** Every licence the pipeline rests on is read and dated, and the records match.

**Cost.** Half a day.

## P1. Profile the hook camera

**Why.** Nothing per pass has been measured. The asset plan assumes Nanite and virtual shadows, and the game runs neither (4-BUDGETS.md, 4.3). The sparse slice's slowest 1% already touches 16.7 ms.

**Do.** In the packaged game, at the hook camera:
1. Capture `ProfileGPU`, `stat rhi` (draws, primitives), `memreport -full`, Windows' dedicated memory and system memory.
2. Cover day and night, standing and a 30-second walk, at 55% and 70% (the game's own rungs) and 50% (the build's timing), at scalability Epic and High.
3. Repeat with Nanite on for the street's meshes, and with virtual shadows on.
4. Keep the cast voice server speaking throughout.
5. Add a triangle stress: the street's geometry four times over, to give milliseconds per million triangles on this card.

**Pass.** A per-pass table that confirms or cuts every allocation in 4-BUDGETS.md, and settles High against Epic and Nanite on or off.

**Cost.** One to two days. Much of it can run on the build machine as a new shot flag.

## P4. One thirty-minute session, played and counted

**Why.** No thirty-minute session has ever been played or recorded. The "town visibly knows them" figures are the Core's, on paper (H4b, area 6).

**Do.**
1. After P3, the AI tester plays 30 real minutes from New Game in the packaged build, as a player would. Thirty minutes of checked talk cost $0.54–1.61 at the measured rates, so at the top rate it passes the day's dollar. Split it:
   - (a) the whole thirty minutes on the stand-in talk, which is free, to count content and empty minutes;
   - (b) the talk counts on the real checked path inside the day's dollar, about fifteen minutes of talk.

   A single full run on the key needs his money ruling.
2. Log each minute:
   - what happened;
   - who saw the deed;
   - who mentioned it later, and how;
   - "that's all I know" counts;
   - reply delays;
   - minutes with nothing to do;
   - anything that broke the illusion.

This is the nightly report ruled on 3 October, run once at full length.

**Pass.** A minute-by-minute table. Its empty minutes become the content list for the friends' build.

**Cost.** One day; at most $1 of talk. Known issue: the clock runs at two game minutes a real second while the tester thinks.

## P2. The voice off the card, timed beside the game

**Why.** First sound is 5.41 s median. The voice's own share is 3.66 s beside the game. It needs 2.8 GB of the card (H3, H4b). This proof is already list item 3, the 8-bit decoder on the processor. What this review adds is two measurements: frame time while it speaks, since the voice took four of the twelve logical processors on 2 October, and first sound on the real path.

**A fact to state before the test.** Even an instant voice cannot sound before the words exist:
- the unchecked words reached the screen at 1.91 s median in the game (30 Sep);
- the checked first sentence is released to the voice at 2.1 s median from the turn's start (off-game, 22 of 24 turns; production/playtest/talk-cost-2026-09-30-after.md line 9).

So the 2 s target cannot be met by the voice alone. The thinking sounds carry the gap.

**Pass.**
- The voice's own share is at most 1.0 s median beside the game.
- The frame median is no more than 1 ms worse while it speaks.
- The slowest 1% stays under 25 ms.

If it fails, a money ruling goes to Jafar: the researched paid streaming voice (about $0.28 an hour of play, production/research/live-speech-architecture/paid-voices-2026-09-28.md), or keep today's delay. A paid voice would also reopen "voices as chosen" (3 Oct), would need speaker consent the VCTK recordings lack, and needs an allowlist entry: the service named is not on it.

**Cost.** Two days, as listed.

## P8. Tom and one more principal, judged blind

**Why.** Tom is on screen in every frame of a third-person game and is still a Mixamo stand-in in a grey tracksuit (SliceCharacter.cpp). Two of three faces failed blind review. Spare bodies came out identical three times, a cause now known.

**Do.**
1. Build Tom from his casting sheet by the scripted MetaHuman route, with his body re-rigged in the same session (the known fix) and a library groom.
2. Build one more principal by the untried MPFB2 to Mesh-to-MetaHuman route.
3. A fresh reviewer matches each blind to its sheet: age, origin, period hair.
4. Record the hours per face.

**Pass.** Both match their sheets blind, and the cost per face is known. Faces are his to approve.

**Cost.** Two to three days.

## P7. Idles and walks without the Game Animation Sample

**Do.**
1. Retarget MetaHuman's own locomotion clips and a chosen Mixamo idle set (four base idles and six breaks) onto the three cast.
2. Test with the 70% head hold removed.
3. Match walk speed to each clip, so feet stop sliding.
4. Film three people standing and walking out of step.
5. A fresh reviewer checks against dated street photographs and the floor's "nobody frozen stiff".

**Pass.** No stiffness and no sliding flagged.

**Cost.** One to two days.

## P6. One coat at 8 m on three bodies, and twelve people's cost

**Do.**
1. One plain coat, from a MakeHuman CC0 base or Blender, skinned to three bodies.
2. Walking on P7's clips, filmed in the game camera at 8 m by day.
3. A fresh reviewer checks against the Hook sheet's two foreground men and the floor of 3 October.
4. Twelve such people at LOD 2 or more with hair cards: measure milliseconds and megabytes.

This is the cheapest third of the asset plan's 8–14-day people proof.

**Pass.**
- Nothing flagged at 8 m.
- Twelve people at most 0.7 ms of GPU and 200 MB, with garment and body textures shared (4-BUDGETS.md).

**Cost.** Three to five days.

## P10. One house of the building kit at the bar

**Do.** One terrace house, not the asset plan's six frontages:
1. Flemish or English garden-wall bond, in place of today's stretcher bond.
2. One shared trim sheet.
3. Reveals that read, sills with a drip, sash detail, wear by rule.
4. A fresh reviewer judges it at 3 m and 15 m, day and wet, beside the Hook sheet and dated photographs.
5. Count triangles and materials against 4-BUDGETS.md.

**Pass.**
- No repeat, the reveals read, the bond is right.
- At most 150,000 triangles and 12 materials.

**Cost.** Two days.

## P11. One real room behind glass, measured

**Do.**
1. `shop-room.py --export-room` for the next shop in view, with its night light and front-layer glass.
2. Judge it at 1–3 m beside Rita's.
3. Measure milliseconds and megabytes with the room in view.

**Pass.** Accepted with Tom at 1–3 m; at most 0.15 ms and 40 MB per room.

**Cost.** One to two days.

## P16. Food from allowed scans

**Do.** From his PC (Sketchfab is unreachable from the cloud):
1. Fetch three of ffishAsia's CC0 scans (cod, mackerel, crab) with his token, reading each listing's tags for NoAI at download.
2. Cut each to 2,000 triangles or fewer.
3. Make crushed ice in Blender.
4. Lay one fishmonger's slab and judge it at 1–3 m beside Rita's.

**Pass.** Not called "toys", and every tag is clean.

**Cost.** One day.

## P9. A fictional car's silhouette, blind

**Do.**
1. One platform from the loft generator, untextured, in the asset plan's proportions.
2. Render it side, front, rear and three-quarter.
3. Run the asset plan's blind test.

**Pass.** No model named with confidence, and the car placed in Britain or Europe, 1985–91. Only then the 4–6-day material pass. The fallback, no cars, stands.

**Cost.** One day.

## P19. The hill from the kit (after P10)

**Do.**
1. Rows of P10's kit at their distance versions on the hill's footprint, 110–206 m from the hook camera, in the day haze.
2. Judge them and measure them.

**Pass.** The rows read as houses, not boxes, at no more than 0.4 ms.

**Cost.** One to two days.

## P20. A grey card: night exposure, faces in passing, the sky

**Do.**
1. A grey card in the game's own camera, by day and at night. The research says this settles the disputed night exposure (aaa-street, 3-LIGHT-AND-GRADE.md).
2. Sheila at 5 m and 10 m by day without the conversation light: measure her face against the card, try fill from the sky light, and put both to a fresh reviewer.
3. One structured overcast from Poly Haven's CC0 skies on the dome, judged against the sheet. Cloud structure failed twice by other means (area 9).

If he rules rain in, add half a day here.

**Pass.** Her face reads in passing, the night exposure is a number, and the sky is not flat white.

**Cost.** One day.

## P15. Mickey's office camera, walked

**Do.**
1. Build with `-MickeysInside`.
2. Follow the camera note's eight steps.
3. Film the door, the counter and the back room.

Then a scope ruling for Jafar: is the office in the thirty minutes (basic 14) or not.

**Pass.** No wall fills a third of the frame, and Tom never vanishes.

**Cost.** One day.

## P12. Epic's streaming face solver on one live line

**Do.**
1. Find whether the 5.8 install's streaming audio-driven solver runs on this AMD card, on the processor or through DirectML.
2. Drive Sheila from one live reply.
3. Measure the latency and cost it adds.
4. Compare it blind with the loudness mouth.

**Pass.** It runs here, adds at most 100 ms and 1 ms of GPU, and a reviewer prefers it. If it fails, the mouth stays a stated shortfall.

**Cost.** One to two days.

## P13. A CC0 ambience bed

**Do.**
1. A two-minute street bed from CC0 sources only (D26): harbour, gulls, distant traffic, others' footsteps, a shop bell, wind.
2. Record each file's source and licence, and read each site's AI terms at download.
3. Put it on his page for his ear (D42).

**Pass.** His yes.

**Cost.** One day.

## P17 and P18. Combat and music: rulings first

- **Combat:** G3 rules fists in, and D24 says it "must not look broken". But nothing says whether it belongs in the thirty minutes. Ask first. If yes: one punch and one hit reaction from Mixamo on a MetaHuman, seen by a witness through the real perception code, judged "not broken". Two days.
- **Music:** there is no direction. If he rules it in: read the licence of the weights named in the allowlist (MusicGen), and play one track in the street by his ear. Half a day.

## P21. One week against a dated plan

**Why.** The order was replaced six times in four days. More than twelve items went past the two-tries rule. Nothing is dated (1-AUDIT.md, item 10).

**Do.**
1. Put dates on list items 2.1 to 5, with a 30–40% buffer for new technology [SS, producers' rule of thumb].
2. Each Monday, record items planned against items finished, and every two-tries breach.
3. Review 6-RISKS.md.

**Pass.** After one week, a measured rate that dates the friends' build.

**Cost.** Thirty minutes a week.

## P22. The phone kiosk remade, and the kerbside run

**Why.** Jafar called the phone box a placeholder on 1 October (DECISIONS line 196). It is one of the nine scripted pieces that had passed the gate on 29 September. So the gate's pass did not meet his bar, and about 25 kinds of street furniture are still to make (asset plan, family 4).

**Do.**
1. Remake the KX100 with the asset plan's materials: brushed stainless, grimy glass, the payphone.
2. Check its size against the KX100's drawings; the scene file may hold the older K6's (asset-plan fault 6).
3. Judge it at the hook camera beside a dated photograph.

If it passes, the asset plan's kerbside run (4–6 days) follows.

**Pass.** A fresh reviewer does not call it a placeholder at walking distance.

**Cost.** Half a day for the kiosk.

## What could not be verified

- **Every day estimate** is this review's [I].
- **Whether the streaming face solver runs on AMD.**
- **Whether the town's fix for P3** touches anything beyond Program.cs. Only the condition was read.
- **GitHub's current private-repository minutes.**
- **Every "Pass" threshold** that names milliseconds or megabytes rests on 4-BUDGETS.md's provisional allocations.
