# 4. Five ideas worth a small, cheap proof

Chosen for what each would settle against LEDGER's problems under his rulings as they stand (RULINGS.md, 7 October), at the lowest cost, on this PC, within the licence rules. Each is under two working days and spends nothing; none uses LEDGER's key.

**Revised after the independent check** (SOURCES.md). The first version proposed:
- a local check of the first sentence;
- motion from phone video or Kimodo;
- the tester reading the town's memory through Unreal's MCP server.

His rulings and LEDGER's own earlier work already settle those three, so they moved to "Only if a ruling changes" below.

None of the five is on the plan. Each would join it only by his order on a Monday, at a stated place. This note changes nothing.

| # | Idea | Problem | Days | What it would settle |
|---|---|---|---|---|
| 1 | The gate's AI reviewer tested on planted faults, in frames with no people in them | 2 and 5 | 0.5–1 | How many visible faults the gate lets through to his page, and which prompt and model to trust |
| 2 | Pictures for the nightly walk, taken by the game itself and proved live | 5, and the Meridian test | 0.5 | Whether the tester's "what broke the illusion" line can be filled at all, and how often it is right |
| 3 | The port's seeded generator extended to the town's newer code | the simulation, 5 | about 1 | Whether what the town says and remembers in the game is what the design says |
| 4 | Song lyrics and quoted text in live talk | 1, and the law | 0.5 | Whether canon's "no lyrics" holds in live talk before friends play |
| 5 | Epic's MCP server in the editor, for one bounded look task | 2 and 5 | about 1 | Whether working in the live editor by sight saves the weekly allowance, and what guards it needs |

---

## 1. The gate's AI reviewer, tested on planted faults

**Why.**
- His 2 October rule: nothing reaches his page with a visible fault. The gate's second check is a fresh AI reviewer.
- Nobody has measured how many faults that reviewer finds.
- This period's research says model judges lean towards passing work:
  - judges "confirm satisfied requirements far more reliably than they detect violated ones" (D3-Omni, 25 Aug [ABS]);
  - the best of 20 judges picked the right image on a named criterion 63.1% of the time, against 32.2% by chance (VisionQ, 30 Sep [ABS]);
  - clipping detectors raise many false alarms and suit only "high-recall candidate filters" (28 Jul [ABS]);
  - comparing with the last clean frame works best (RefGlitch, April [ABS]).
- Anthropic's own engineers: "Out of the box, Claude is a poor QA agent" [SHOWN].

**The licence limit.** LEDGER's own terms note (production/research/terms-2026-10-03, read from his PC on 3 October) records two clauses that bind here:
- the Unreal licence, 6(e): MetaHuman characters may not be used "to train or test an AI";
- Adobe's terms, 17(C): nothing from Mixamo may be used to "test" an AI.

So the test frames hold no person: the street and the office with everyone hidden [I, the cautious reading].

**Do.**
1. Take ten frames at 2560×1440 from the morning views and the office, with the people hidden.
2. Plant twenty faults in the scene itself, not painted onto the picture:
   - a debug sphere;
   - a floating prop;
   - a black square;
   - a stretched texture;
   - a missing pane;
   - a duplicated bin;
   - a hole in a wall;
   - a light with no source.

   Keep five frames clean.
3. Run two prompts on Opus 5.5 and Sonnet 5.5, which see the frame whole (Haiku 4.5 shrinks it [SHOWN, Anthropic's vision documentation]):
   - (a) today's fresh-reviewer prompt;
   - (b) one question per kind of fault, with the last approved frame of the same camera beside each.
4. Count the faults found, and the false alarms on clean frames.

**Pass.** The better prompt finds at least 90% of the planted faults, with at most one false alarm per clean frame. If none does, the gate needs mechanical checks behind it (a census of debug objects, a test for things passing through each other) before anything goes on his page.

**Settles.** How far the gate can be trusted, which prompt and model to use, and whether a model alone is enough.
- **It does not judge the look.** No study found measures that; it stays his eye's.
- **It says nothing about faces or people**, which the licence keeps out of the test.

**Cost.** Half a day to a day, on the subscription. Prompt (b) doubles the pictures: 75 per model, 150 in all, at about 4,800 tokens each, so about 0.7 million tokens.

## 2. Pictures for the nightly walk, taken by the game and proved live

**Why.**
- His 3 October ruling asks the nightly walk to report "anything that broke the illusion of a living town".
- The walk's last step already sends its pictures to Claude Code for that (tools/nightly_walk.py, "the eyes"). But the walk saves no pictures. Every report from 4 to 7 October says "no pictures from the walk to look at" (production/playtest/nightly, read here).
- Two findings from this period bear on how to take them:
  - **A frozen capture.** One modder's Windows screen capture returned byte-identical frames while the game ran (Universal Modder's "Oracles" note, 1 October [SHOWN]).
  - **Agents that walk a world miss most faults.** Walking agents found 6.6–42.3% of planted faults in UE5 worlds, against 83.4% for people (WorldAuditBench, 30 Sep [ABS, checked here]). So what the eyes report is a screen, not a verdict.

**Do.**
1. The walk asks the game itself for a frame at each stage of the route. The game already takes its own pictures for the morning views (VignetteShot.cpp), so not the desktop.
2. **Prove the capture is live:** two frames a second apart must differ. If they do not, the report says "capture frozen" instead of judging.
3. The eyes step then runs as written, with proof 1's better prompt if that proof has run.

**Pass.**
- Three nights running with pictures and a live-capture check.
- Once, the eyes' lines checked by hand against the pictures.

**Settles.** Whether the morning paragraph's "what broke the illusion" can be filled at all, and how far to trust it.

**Cost.** Half a day for the builder. The eyes already cap themselves at twelve pictures a night, on the subscription.

## 3. The port's seeded generator, extended to the town's newer code

**Why.**
- **The gap.** The independent review of 1 October changed the newer C++ town code one line at a time, eleven times, at twelve lines. The comparison with the C# design still passed every time (production/audits/review-2026-10-01/FAULTS.md, D1, read here). These were:
  - the news ("there", "mended within the hour", "at my place");
  - slipping out of Ada's tea;
  - the cast file's "inside" check and its fallback;
  - four checks on whether a line names Tom;
  - the town week's telling.

  This session found no record that D1 was closed: it is not in FINDINGS, NOW, DECISIONS or PLAN.
- **LEDGER already has the cure for the gossip code.** A seeded random-world generator, written in both C# and C++ and compared hash by hash, agreed on 12,000 worlds and 3,000 saves. It caught all 37 faults planted in the port that the hand-written rows missed (ledger/PerceptionGolden/GossipFuzz.cs, its own comment, read here).
- **The same lesson in this period's research.** Decompiled code that compiled and passed every test still behaved differently on random inputs 4.9% of the time, and up to 13% ("When LLM Decompilers Recompile More and Preserve Less", 4 Sep [ABS, checked here]).

**Do.**
1. The same pattern for the newer town code (the news, the first week, the cast's day, the street's lines, the town week): seeded days written in both languages, each hashed, added to the golden table.
2. Re-apply the review's eleven changes, and thirty more one-line changes.

**Pass.** Every one of the review's changes is caught, and no unexplained difference remains over 1,000 seeded days.

**Settles.** Whether what the town says and remembers in the game is what the C# design says. The Meridian test's "the town visibly knows them" rests on it.

**Cost.** About a day, on the processor. Split as the gossip generator was: the C# a bounded town task, the C++ the builder's.

## 4. Song lyrics and quoted text in live talk

**Why.**
- **Canon:** "No real people, voices, logos, lyrics, car models."
- **His ruling of 29 September** bars real makes, brands, programmes and public figures from live talk, but does not name lyrics.
- **Nothing in the talk program says so:** no line about lyrics in its instructions or claim check, the content rules or the casting folder (searched here).
- **The law, as reported:** a Munich court found song lyrics reproduced by a chatbot infringing (GEMA v. OpenAI, November 2025 [SS]). Whoever publishes the output carries the risk, and in live talk that is the game [SS].
- **The setting invites it:** a 1990 British street invites "what's that song on the radio?"

**Do.**
1. Write thirty baiting questions to Sheila, Ron and Darren: sing the chorus, finish this line, what's top of the charts, what did you see at the pictures.
2. Run them through the town's bench: the real engine's words, through Claude Code on the subscription, with no key, as the nightly bench already does.
3. Count:
   - lines of real lyrics, of any length;
   - real bands, songs and films;
   - anything after 1992;
   - whether the claim check stops each.

**Pass.** None heard. If any is, one line in the talk instructions and the check, then the same thirty again.

**Settles.** Whether canon's "no lyrics" holds in live talk before friends play, at no cost.

**Cost.** Half a day; no key.

## 5. Epic's MCP server in the editor, for one bounded look task

**Why.**
- **What Unreal 5.8 now has.** An MCP server inside the editor: actors, lights, materials, PCG, automation tests, screenshots, and any editor Python [SHOWN, checked here].
- **Epic's Claude Code plugin** (MIT [SHOWN]) shows the model three meta-tools, "so the prompt cache stays warm".
- **How the builder works today:** by writing editor scripts, running them and looking at renders [I].
- **The research on agents in engines:**
  - agents writing code or scripts beat agents wiring Blueprints by 30–43 points (CraftBench-UE [ABS, checked here]);
  - inspecting before editing adds 10–13 points (OpenGameEval [ABS]);
  - 35.8% of scene edits that reach their target also change something else (Code4Scene [ABS, checked here]).
- **What is not known:** no study measured whether this saves time on a real project. LEDGER has not tried it; its earlier MCP research was Blender's (production/research/blender-mcp).

**Do.**
1. Take one bounded look task from the current phase, such as one shop room's lights, and do it twice:
   - the current way;
   - through the editor's MCP server, with permission prompts on.
2. Read-only first: list the actors, take a screenshot through the game camera.
3. Then the edits. After each edit, compare every actor and its position with the moment before.
4. Commit first. Never while a build or cook runs: two Unreal jobs never overlap.

**Pass.** A fresh reviewer judges both results the same, the MCP way used less of the weekly allowance, and the comparison shows no change nobody asked for.

**Settles.** Whether working in the live editor by sight saves the weekly budget, and which guards it needs.

**Cost.** About a day, on the subscription.

**Risks.**
- The server has "no authentication layer" and runs arbitrary Python [SHOWN]. Keep it on this PC only, with prompts on.
- It is Experimental.
- Under the Unreal licence, 6(e), what the editor sends to Claude is allowed only while Claude does not train on it. "Help improve Claude" stays off, as he ruled on 3 October.

---

## Only if a ruling changes

| Idea | Why not now | What would bring it back |
|---|---|---|
| **A small local check on the first sentence**, with the facts named before writing | **His 7 October ruling:** no cloud voice, no third attempt at the voice, the faster first sentence off; the check study recommended parked (DECISIONS.md). **The voice sets the first sound today, not the check.** On 7 October the voice took 2.2–4.4 s to make its first piece, and the first sounds came at 3.6–5.7 s: about the moment the sentence was written plus the voice's time. So the voice works while the check runs and sets the first sound [I, from the 7 October table in production/research/voice-off-card/CLOUD-VOICE-2026-10-07.md]. **Naming the facts before writing was built on 30 September and measured.** "That's all I know" was no different (18.3 against 21.7 in sixty, p = 1.0), and it was about 0.25 s slower to the first word. **The small checkers are less exact than the slow ones.** Enoki's fast version scored 69.1% against its slow version's 76.4%, on hardware it does not state [SHOWN, paper]. **Training one is arguable.** Under Anthropic's consumer terms, building it with Claude's help counts; his 24 September ruling says no training on the router's answers. | A faster voice. Then the check becomes the floor, as the 7 October proposal says. |
| **New motion**: his own phone video through Epic's markerless capture, or NVIDIA's Kimodo (RP weights) | **His rulings:** poses come from MetaHuman's clips and Mixamo (3 October); the sitting clips come from the Mixamo harvest (7 October). **The method exists:** production/research/sit-and-turn (6 October). **What is unread or unproven:** the markerless plugin comes from Fab and its NoAI flag is unread; the RX 6700 is below Epic's recommended card. Kimodo was "most extensively tested" on NVIDIA cards (RTX 3090, RTX 4090, A100) [SHOWN, README]; nothing shows it on an AMD card, and its weights' licence text was unreached. A new tool enters only by a record naming its weights licence (24 September). | The MetaHuman and Mixamo clips failing the clothes-and-people floor ("nobody frozen stiff") in the game camera |
| **The tester reading the town's memory** through an MCP server in a Development build | **Not needed.** The game already writes its own record of each walk: who saw the deed, who showed they knew it, each reply's outcome and time. The nightly report reads it (tools/nightly_walk.py, production/specs/session-record.md, read here). | Nothing; the record does it |
| **Authored lines picked live** (RePlay, Disney Research, 25 Sep) | **His 7 October ruling:** no prepared openings. RePlay plays only pre-recorded lines. It is built on NVIDIA's PersonaPlex, whose training data raises a dataset-licence question (notes/HE). | His ruling |

## Not worth a proof now

| Idea | Why not |
|---|---|
| World models and generated scenes (Genie, Marble, HY-World, Lyra) | Video or splats, not the street's geometry. Their licences exclude the EU and UK or are research-only. They need NVIDIA-class hardware. |
| Image-to-3D for props (TRELLIS.2, Hunyuan3D, Meshy, Tripo) | **His 22 September ruling:** it waits until hand-made props are the bottleneck. The open models need NVIDIA cards with 24 GB or more. **The licence allowlist lists TRELLIS 2 as MIT.** The research found that its renderer, nvdiffrast, is licensed for non-commercial use only, and that its training data includes Sketchfab items now tagged NoAI [SHOWN, helper note HC]. That entry should be re-read before image-to-3D returns; it is his decision. |
| Neural "photoreal" filters (DLSS 5, GAN filters) | Not on an RX 6700. The open ones were trained on another game's frames. Training one on Unreal output is barred by the Unreal licence, 6(e) (read from his PC on 3 October). |
| Full-duplex speech-to-speech | Speaks before any check. The open ones are research-only or need data-centre cards [SS]. |
| AI tailoring | Not shown anywhere in this period. The field's data cannot express a lapel. |
| Decompiling, modding or mashing up other games | Not lawful for this purpose (3-LEGAL.md), and excluded by the brief |
