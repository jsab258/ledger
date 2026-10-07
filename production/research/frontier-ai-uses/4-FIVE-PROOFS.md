# 4. Five ideas worth a small, cheap proof

Chosen for what each would settle against LEDGER's problems under his rulings as they stand (RULINGS.md, 7 October), at the lowest cost, on this PC, within the licence rules. Each takes a day or less. Two use LEDGER's key, inside the dollar a day for measurement runs; the rest use the subscription only.

**Revised twice after independent checks** (SOURCES.md). Earlier versions proposed six ideas that turned out to be settled already:

| Idea dropped | Settled by |
|---|---|
| A local check of the first sentence | His rulings |
| Motion from phone video or Kimodo | His rulings |
| The tester reading the town's memory through Unreal's MCP server | The game's own session record |
| Pictures for the nightly walk | Existing work; a one-line fault, below |
| Random testing of the C++ port | The port audit of 5 October |
| A trade-mark search | The branding research of 1 October |

None of the five is on the plan. Each would join it only by his order on a Monday, at a stated place. This note changes nothing.

| # | Idea | Problem | Days | Money | What it would settle |
|---|---|---|---|---|---|
| 1 | The gate's AI reviewer tested on planted faults | 2 and 5 | 0.5–1 | none | How many street and room faults the gate lets through, and which prompt and model to trust |
| 2 | Sonnet 5.5 as the writer, on the real path | 1 | 0.5 | ≤ $1 of the key | Whether the newest model shortens the one part of the delay his rulings leave open |
| 3 | The claim check on the next model, before Haiku 4.5 retires | 1 | 0.5–1 | ≤ $1 of the key | Which model the check moves to, measured before the change is forced |
| 4 | Quoted song lyrics in live talk | 1, and the law | 0.5 | none | Whether canon's "no lyrics" holds for quotations, which the real-names guard cannot catch |
| 5 | Epic's MCP server in the editor, for two bounded look tasks | 2 and 5 | about 1 | none | Whether working in the live editor by sight saves the weekly allowance, and what guards it needs |

---

## 1. The gate's AI reviewer, tested on planted faults

**Why.**
- His 2 October rule: nothing reaches his page with a visible fault. The gate's second check is a fresh AI reviewer.
- Nobody has measured how many faults that reviewer finds. tools/frame-drift.py compares each frame with the last build pixel by pixel; it says what moved, not whether it is a fault.
- This period's research says model judges lean towards passing work:
  - judges "confirm satisfied requirements far more reliably than they detect violated ones" (D3-Omni, 25 Aug [ABS]);
  - the best of 20 judges picked the right image on a named criterion 63.1% of the time, against 32.2% by chance (VisionQ, 30 Sep [ABS]);
  - clipping detectors raise many false alarms and suit only "high-recall candidate filters" (28 Jul [ABS]);
  - comparing with the last clean frame works best (RefGlitch, April [ABS]).
- Anthropic's own engineers: "Out of the box, Claude is a poor QA agent" [SHOWN].

**The licence question, his to settle.** LEDGER's records disagree on whether people may be in the test frames.
- **The allowlist (entry 3)** says MetaHumans are never "used to train or test, an AI" (Unreal licence 6(e)). It says nothing from Mixamo is used "to make, train, test or improve an AI" (Adobe 17(C)).
- **His 3 October ruling and the terms note** treat both clauses as training clauses, fine while nothing we send trains a model.

Until he rules, this proof uses the allowlist's wording: frames with everyone hidden [I].

**Do.**
1. Twenty frames at 2560×1440, from the morning views and the office, with the people hidden.
2. Plant one fault in each, in the scene itself and not painted onto the picture:
   - a debug sphere;
   - a floating prop;
   - a black square;
   - a stretched texture;
   - a missing pane;
   - a duplicated bin;
   - a hole in a wall;
   - a light with no source.
3. Add five clean frames: 25 in all.
4. Run two prompts on Opus 5.5 and Sonnet 5.5, which see the frame whole (Haiku 4.5 shrinks it [SHOWN, Anthropic's vision documentation]):
   - (a) today's fresh-reviewer prompt;
   - (b) one question per kind of fault, with the last approved frame of the same camera beside each.
5. Count the faults found, and the false alarms on clean frames.

**Pass.** The better prompt finds at least 18 of the 20 faults, with at most one false alarm per clean frame. If none does, the gate needs mechanical checks behind it (a census of debug objects, a test for things passing through each other) before anything goes on his page.

**Settles.** How far the gate can be trusted on street and room faults, which prompt and model to use, and whether a model alone is enough.

**It does not settle:**
- **faults in people**: faces, clothes, hands through the body. These are the people he judges himself, and they stay outside the test until he rules on the licence question.
- **the look**, which no study has measured; that stays his eye's.

**Cost.** Half a day to a day, on the subscription. Prompt (b) doubles the pictures: 75 per model, 150 in all, at about 4,800 tokens each, so about 0.7 million tokens.

## 2. Sonnet 5.5 as the writer, on the real path

**Why.**
- **Under his rulings,** the free voice stays, so the first sound is about the moment the first sentence is written plus the voice's time [I, from the 7 October table in production/research/voice-off-card/CLOUD-VOICE-2026-10-07.md]. The writing (1.35 s median on 7 October) is the one part of the delay his rulings leave open.
- **The live talk still writes with Sonnet 5** (ConversationEngine.cs, read here).
- **What is known of Sonnet 5.5:**
  - released 28 September at Sonnet 5's price;
  - "30%+ faster" output [CLAIMED];
  - thinking is switched off with `between_tools`, since "disabled" now errors, and forced tool choice errors [SHOWN, Anthropic's documentation];
  - it caches from 512 tokens, against 1,024 for Sonnet 5 (production/research/prompt-caching, 29 September).
- **A reply is short** (about 53 output tokens on 7 October), so the time to the first word may matter more than output speed. That is untested [I].

**Do.**
1. Make the two settings changes behind a switch, as the faster first sentence was.
2. Run the same ten bench lines to Sheila with Sonnet 5 and then Sonnet 5.5, on the played copy with today's voice, each run logged with its tokens and cost (talk-runs.jsonl).
3. Record the moment the first sentence is written and the first sound.
4. A fresh reader judges the pairs blind, as on 7 October.

**Pass.** The first sound comes earlier by at least 0.3 s at the median, with replies judged no worse.

**Settles.** Whether the newest model shortens the delay within his rulings, and at what quality. It will not bring two seconds; that stays reported failed.

**Cost.** Half a day; about $0.55 of the key for twenty replies (7 October: $0.13 for five checked replies).

**Note.** Changing the writer's version is arguably a routine choice under his ruling that the model follows the kind of moment (D48). His 3 October list keeps "the town's talk work" closed, so the result goes to him before any switch is turned on.

## 3. The claim check on the next model, before Haiku 4.5 retires

**Why.**
- **Every check runs on Haiku 4.5:** the claim check, the threat reading and small talk.
- **Its retirement** is promised "not sooner than 15 October 2026", with at least 60 days' notice [SHOWN]. Haiku 5.5 is promised "in the coming weeks" [CLAIMED].
- **The pre-production risk register** lists this (W3) with no proof attached.
- **The check was tuned once.** Three tuned versions on 255 labelled details found none better; the check stays as it is (DECISIONS.md, 30 September). A model change could undo that silently.

**Do.**
1. On the bench of 255 labelled details, through Claude Code on the subscription where the bench allows it, compare:
   - today's check on Haiku 4.5;
   - the same on Sonnet 5.5;
   - the same on Haiku 5.5, the day it ships.
2. Count the inventions passed and the true details refused.
3. Then one timing run on the real path for the best of them, inside the dollar.

**Pass.** A successor passes no more inventions and refuses no more true details than Haiku 4.5, at a check time no longer than today's.

**Settles.** Which model the check moves to, measured before the change is forced, and whether the check's time can come down for a faster voice later.

**Cost.** Half a day to a day; up to $1 of the key for the timing run.

## 4. Quoted song lyrics in live talk

**Why.**
- **Canon:** "No real people, voices, logos, lyrics, car models."
- **The real-names guard covers names, not quotations.** Live talk already has a rule against naming "a band or singer", programmes and public figures (RealWorld.cs, on by default), and a bench of small-talk questions that includes "What music are you into?" (ClaimBench, read here). But the guard looks for names. A character asked to "sing us the chorus" can quote a real song without naming anyone, and the claim check does not look for quotations [I, from reading both].
- **The law, as reported:** a Munich court found song lyrics reproduced by a chatbot infringing (GEMA v. OpenAI, November 2025 [SS]). Whoever publishes the output carries the risk, and in live talk that is the game [SS].
- **The setting invites it:** a 1990 British street invites it.

**Do.**
1. Write twenty quote-baiting questions to Sheila, Ron and Darren:
   - sing us the chorus;
   - finish this line;
   - what's that one that goes;
   - give us a verse;
   - what was the line from the film.
2. Run them through the town's bench, with the real engine's words through Claude Code on the subscription and no key, as the small-talk bench runs.
3. Count every line of real lyrics, poems under copyright or film dialogue, of any length.

**Pass.** None. If any appears, one line in the prompt's rule beside the real-names rule, then the same twenty again.

**Settles.** Whether canon's "no lyrics" holds for quotations before friends play.

**Cost.** Half a day; no key.

## 5. Epic's MCP server in the editor, for two bounded look tasks

**Why.**
- **What Unreal 5.8 now has.** An MCP server inside the editor: actors, lights, materials, PCG, automation tests, screenshots, and any editor Python [SHOWN, checked here].
- **Epic's Claude Code plugin** (MIT [SHOWN]) shows the model three meta-tools, "so the prompt cache stays warm".
- **The research on agents in engines:**
  - agents writing code or scripts beat agents wiring Blueprints by 30–43 points (CraftBench-UE [ABS, checked here]);
  - inspecting before editing adds 10–13 points (OpenGameEval [ABS]);
  - 35.8% of scene edits that reach their target also change something else (Code4Scene [ABS, checked here]).
- **What is not known:** no study measured whether this saves time on a real project.
- **LEDGER has not tried it.** Its MCP work was Blender's (production/research/blender-mcp), and the AAA-street research could not confirm whether Epic's own server shipped in 5.8 (aaa-street/1-PIPELINE.md).

**Do.**
1. A decision record for the plugin first, as the allowlist's process requires for a new tool.
2. Two comparable look tasks from the current phase, such as two shop rooms' lights: one done the current way, one through the editor's MCP server with permission prompts on. Swap which way goes first on the second pair, so neither way benefits from having learnt the room.
3. Read-only first: list the actors, take a screenshot through the game camera.
4. Then the edits. After each edit, compare every actor and its position with the moment before.
5. Commit first. Never while a build or cook runs: two Unreal jobs never overlap.

**Pass.** A fresh reviewer judges the results equal, the MCP way used less of the weekly allowance in both pairs, and the comparison shows no change nobody asked for.

**Settles.** Whether working in the live editor by sight saves the weekly budget, and which guards it needs.

**Cost.** About a day, on the subscription.

**Risks.**
- The server has "no authentication layer" and runs arbitrary Python [SHOWN]. Keep it on this PC only, with prompts on.
- It is Experimental.
- Under the Unreal licence, 6(e), what the editor sends to Claude is allowed only while Claude does not train on it. He said on 3 October that he was switching "Help improve Claude" off; the setting itself has not been read (terms note).

---

## Found on the way: faults, not proofs

These need no order; they belong in FINDINGS or the list, which this branch may not edit.

1. **The nightly walk's eyes never see its pictures.**
   - The tester saves a picture after every command as step-NNN.jpg (tools/ai-tester/play.py).
   - The nightly report's eyes look only for .png files (tools/nightly_walk.py).
   - So every report from 4 to 7 October says "no pictures from the walk to look at" (production/playtest/nightly, read here).

   One line fixes it. Once fixed, WorldAuditBench is the caution for reading the results: agents walking UE5 worlds found 6.6–42.3% of planted faults, against 83.4% for people [ABS, checked here]. So the eyes' lines are a screen, not a verdict.
2. **The town's newer C++ code still has untested lines.**
   - The port audit of 5 October ran 651,000 random scripts through the C# and the C++ and planted 30 one-line breaks; 11 passed every test (production/audits/sweep-2026-10-05/port-vs-core.md, read here).
   - Of the twelve lines the 1 October review named (its D1), eight still passed.
   - The second independent check here re-ran breaks at those twelve lines on 7 October: nine passed [its run, not repeated here].

   This period's decompilation research shows the same thing: code that passed every test still behaved differently on random inputs 4.9% of the time [ABS, checked here]. LEDGER's own gossip generator is the cure where it is used. It caught all 37 faults planted in the port that the hand-written rows missed (GossipFuzz.cs).

## Only if a ruling changes

| Idea | Why not now | What would bring it back |
|---|---|---|
| **A small local check on the first sentence** | **His 7 October ruling:** no cloud voice, no third attempt at the voice, the faster first sentence off; the check study recommended parked (DECISIONS.md). **With the free voice, the voice sets the first sound.** On 7 October the voice took 2.2–4.4 s to make its first piece, and the first sounds came at 3.6–5.7 s: about the written sentence plus the voice [I, from the 7 October table]. His words that day ("the check on the first sentence, not the voice, sets the floor") hold for a fast cloud voice, not for the voice he kept. **The small checkers are less exact than the slow ones.** Enoki's fast version scored 69.1% against its slow version's 76.4%, on hardware it does not state [SHOWN, paper]. **Training one is arguable.** Under Anthropic's consumer terms, building it with Claude's help counts, and he ruled no training on the router's answers (24 September). | A faster voice. Then the check becomes the floor, as the 7 October proposal says. Proof 3 measures its successor in the meantime. |
| **New motion**: his own phone video through Epic's markerless capture, or NVIDIA's Kimodo (RP weights) | **His rulings:** poses come from MetaHuman's clips and Mixamo (3 October); the sitting clips come from the Mixamo harvest (7 October). **The method exists:** production/research/sit-and-turn (6 October). **What is unread or unproven:** the markerless plugin comes from Fab and its NoAI flag is unread; the RX 6700 is below Epic's recommended card. Kimodo was "most extensively tested" on NVIDIA cards [SHOWN, README], and its weights' licence text was unreached. A new tool enters only by a record naming its weights licence (24 September). | The MetaHuman and Mixamo clips failing the floor ("nobody frozen stiff") in the game camera |
| **Authored lines picked live** (RePlay, Disney Research, 25 Sep) | **His 7 October ruling:** no prepared openings. RePlay plays only pre-recorded lines. It is built on NVIDIA's PersonaPlex, whose training data raises a dataset-licence question (notes/HE). | His ruling |

## Not worth a proof now

| Idea | Why not |
|---|---|
| The tester reading the town's memory through an MCP server | The game already writes its own record of each walk (who saw, who showed they knew, each reply's outcome and time), and the nightly report reads it (tools/nightly_walk.py; production/specs/session-record.md) |
| World models and generated scenes (Genie, Marble, HY-World, Lyra) | Video or splats, not the street's geometry. Licences exclude the EU and UK or are research-only. They need NVIDIA-class hardware. |
| Image-to-3D for props (TRELLIS.2, Hunyuan3D, Meshy, Tripo) | **His 22 September ruling:** it waits until hand-made props are the bottleneck. The open models need NVIDIA cards with 24 GB or more. The allowlist lists TRELLIS 2 as MIT; the research found its renderer, nvdiffrast, licensed for non-commercial use only, and its training data drawn partly from Sketchfab items now tagged NoAI [SHOWN, notes/HC]. That entry is for re-reading when image-to-3D returns. |
| Neural "photoreal" filters (DLSS 5, GAN filters) | Not on an RX 6700. The open ones were trained on another game's frames. Training one on Unreal output is barred by the Unreal licence, 6(e) (read from his PC on 3 October). |
| Full-duplex speech-to-speech | Speaks before any check. The open ones are research-only or need data-centre cards [SS]. |
| AI tailoring | Not shown anywhere in this period. The field's data cannot express a lapel. |
| A trade-mark search for "LEDGER" | Done as far as the cloud can on 1 October (production/research/ui-design/BRANDING.md). Ledger SAS holds LEDGER in class 9 in the EU, UK and US and enforces it, so it "must be settled before any Steam page". What is left is a lawyer's. |
| Decompiling, modding or mashing up other games | Not lawful for this purpose (3-LEGAL.md), and excluded by the brief |
