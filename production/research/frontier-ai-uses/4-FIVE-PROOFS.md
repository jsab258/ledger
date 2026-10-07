# 4. Five ideas worth a small, cheap proof

Chosen for what each would settle against LEDGER's hardest problems, at the lowest cost, on this PC, within the licence rules. Each proof is small: under three working days and at most a dollar of the key.

None of them is on the plan. Each would join it only by his order on a Monday, at a stated place (CLAUDE.md). This note changes nothing.

| # | Idea | Problem | Days | Money | What it would settle |
|---|---|---|---|---|---|
| 1 | Check the first sentence locally, against facts the writer names | 1, talk | 2–3 | ≤ $1 | Whether the check can stop setting the floor without letting more invented details through |
| 2 | Natural sitting, standing, turning and idling from phone video, or from Kimodo | 4, animation | 1–2 | none | Whether those motions can come free and cleanly licensed, and whether the RX 6700 can solve them |
| 3 | The nightly tester reads the town's memory through Unreal's own MCP server | 5, and the Meridian test | 1–2 | none | Whether "the town visibly knows them" can be measured every night from the game's state |
| 4 | The gate's AI reviewer tested on planted faults, with the last approved frame beside each | 2 and 5 | 0.5–1 | none | How many visible faults the gate lets through to his page, and which prompt and model to trust |
| 5 | Differential fuzzing and mutant checks of the C++ port | the simulation, 5 | 1 | none | Whether what the town remembers in the game is what the design says, beyond the golden rows |

---

## 1. Check the first sentence locally, against facts the writer names

**Why.** His words of 7 October: "the check on the first sentence, not the voice, sets the floor"; propose "a lighter check, or choosing the facts before writing so less needs checking" (production/research/invented-claims/CHECK-FLOOR-PROPOSAL-2026-10-07.md). The research gives that proposal a concrete, new method:
- **Claude's structured outputs** can make Sonnet name its fact IDs before the line, with a fixed schema compiled once [SHOWN].
- **A small encoder** checks a sentence against the named facts in about a tenth of a second (Enoki 0.11–0.13 s on its authors' hardware [SHOWN, paper]).
- **MIT-licensed detectors** exist to start from (LettuceDetect v2, TinyLettuce 17M to 68M [SHOWN, checked here]).
- **No new speech model offers a check before speaking** (1-WHAT-IS-NEW.md, 1.7).

**Do.**
1. **Bench, no game.**
   - Training sentences are made from the simulation's facts by code, so none comes from Claude, which Anthropic's consumer terms forbid for training models [SHOWN, checked here]:
     - true sentences from real facts;
     - false ones by swapping the person, place, time or object;
     - ones asserting what the character could not know;
     - ones that repeat as fact something only the player said (the Where Winds Meet failure).
   - Fine-tune the smallest TinyLettuce or an mmBERT-base, run through ONNX on the 5600X's processor, not the shared card.
   - Add the rule pass: every fact ID belongs to the character; every name, place, time and number in the sentence appears in those facts.
   - Test it on the existing bench sentences (production/research/invented-claims/bench), which are test inputs only, against Haiku's verdicts and the labels.
2. **Real path, once, inside the dollar.**
   - Sonnet 5.5, with thinking off (`between_tools`) and low effort, writes `{facts, line}`. The local check clears sentence 1; Haiku checks the rest while it plays; anything unsure goes to Haiku.
   - Record the time from Enter to "cleared to speak", and the first sound with today's voice.

**Pass.**
- The local check misses no more invented details than Haiku on the bench and the adversarial set.
- It takes at most 0.2 s a sentence on the processor.
- On the real path, "cleared to speak" comes about a second earlier than today's 2.96 s median (7 October).

**What it settles, and what it does not.**
- **On a pass,** the check stops setting the floor, and the 2 s exit then hangs only on the voice's first audio. That needs a paid streaming cloud voice, a money decision already on his page.
- **With today's free voice** first sound stays above 2 s whatever the check does, as the 7 October proposal says.
- **On a failure,** the check stays on Haiku, and the research has shown no faster safe check exists today.

**Cost.** Two to three days, up to $1 of the key.

## 2. Natural sitting, standing, turning and idling, from phone video or Kimodo

**Why.** Epic's Game Animation Sample is excluded as NoAI. What remains is MetaHuman's own clips and Mixamo. On 3 October the builder kept the plugin's stand idle off because it set Ron and Sheila "wide-legged and braced, a game hero's ready pose" (CrimeProbe.cpp, read here). Two new routes have no dataset problem:
- **Epic's MetaHuman Animator Markerless Motion Capture** (UE 5.8): body animation "from a single camera", processed "locally on your machine" [SHOWN, checked here].
- **NVIDIA's Kimodo, SOMA RP weights**, trained on 700 hours of licensed studio mocap, not AMASS [SHOWN, checked here].

**Do.**
1. On his PC, read the markerless plugin's Fab "Allows usage with AI" flag. Fab is unreached from the cloud.
2. **If it is clear:**
   - Film four phone takes against a plain wall, each 10 to 20 seconds: sit down on a chair, stand up, turn 180 degrees, stand listening. Jafar or anyone willing.
   - Solve them offline.
   - Record time, video memory and any failure on the RX 6700, which is below Epic's recommended RX 6800 XT.
3. **If it is not clear, or the card cannot solve it, or nobody films:** generate the same four with Kimodo SOMA-RP.
   - Run its text encoder on the processor (under 3 GB of video memory); keyframes set the seat height.
   - BVH to Blender to FBX, then UE 5.8's IK retargeter with foot planes.
   - Motion Warping lands the sit-down on the office's bench.
4. Put both on Ron in the game camera. A fresh reviewer judges them against dated photographs of people in 1990 streets and the floor "nobody frozen stiff".

**Pass.** The reviewer finds no stiffness, sliding or pass-through on at least three of the four motions.

**Settles.** Whether problem 4 has a free, clean source today, and which one.
- **Never** Kimodo's SMPL-X version (non-commercial).
- **Never** a "drunk" or "childlike" prompt (the content rule).

**Cost.** One to two days; nothing bought.

## 3. The nightly tester reads the town's memory through Unreal's own MCP server

**Why.** His 3 October ruling asks the tester for "who noticed what he did, who mentioned it to him later and how, how many questions got 'that's all I know', how long each reply took". Every number must come from the real path. Unreal 5.8 lets "cooked and shipping game builds ... host an MCP server" with tools registered in C++ [SHOWN, checked here]. In agent-built games, checks on the game's state agreed with human judges 92.6% of the time, against 78.4% for a judge watching video (SWE-Game, September [ABS]).

**Do.**
1. In a Development build only, behind a compile flag, never in Shipping or the friends' build, register three read-only tools:
   - (a) a deed's witnesses and the gossip chain that followed (who told whom, when);
   - (b) each reply's timestamps: player's Enter, sentence 1 cleared, first audio sample;
   - (c) a frame read from the render target, with its hash.
2. The tester plays its thirty minutes through input as now. At the end it calls the tools and writes the morning paragraph from them.
3. It compares what the memory says against what was said aloud.
4. **Prove the capture live:** two hashes a second apart must differ. One modder's Windows capture returned identical frames while the game ran (Universal Modder's "Oracles" note, 1 October [SHOWN]).
5. As a separate step, try Epic's Claude Code plugin in the editor, read-only first (list actors, a screenshot from the game camera), with permission prompts on.

**Pass.** One night's paragraph built wholly from the tools, matching a hand check of the same run.

**Settles.** Whether the Meridian condition "the town visibly knows them" can be measured on every build without anyone judging video, and what that costs in code and usage.

**Cost.** One to two days. Talk on the stand-in; at most $1 if one real-talk run is included.

## 4. The gate's AI reviewer, tested on planted faults

**Why.**
- His 2 October rule: nothing reaches his page with a visible fault.
- The research says model judges miss most faults and lean towards passing work:
  - agents found 6.6–42.3% of planted faults in UE5 worlds, against 83.4% for humans (WorldAuditBench);
  - judges "confirm satisfied requirements far more reliably than they detect violated ones" (D3-Omni);
  - comparing with the last clean frame helps (RefGlitch) [ABS].
- Anthropic's own engineers: "Out of the box, Claude is a poor QA agent" [SHOWN].
- Nobody has measured how well LEDGER's own reviewer does.

**Do.**
1. Take ten of the morning pictures at 2560×1440.
2. Plant twenty faults across them: a debug sphere, a floating prop, a black square, a stretched texture, a person through a wall, a missing pane, a duplicated bin. Keep five frames clean.
3. Run two prompts on Opus 5.5 and Sonnet 5.5, which see the frame whole; Haiku 4.5 shrinks it:
   - (a) today's fresh-reviewer prompt;
   - (b) a criterion-by-criterion prompt with the last approved frame of the same camera beside each.
4. Count faults found, and false alarms on the clean frames.

**Pass.** The better prompt finds at least 90% of the planted faults with at most one false alarm per clean frame. If none does, the gate needs deterministic checks behind it (a debug-object census, penetration tests) before anything goes on his page.

**Settles.** How far the gate can be trusted, which prompt and model to use, and whether a model alone is enough. **It does not judge the look,** which no study has measured; that stays his eye's.

**Cost.** Half a day to a day, on the subscription: about 0.3 million tokens.

## 5. Differential fuzzing and mutant checks of the C++ port

**Why.** The independent review of 1 October found 12 one-line mutations of new C++ code that the golden comparison still passed (production/audits/review-2026-10-01/FAULTS.md, D1). The same failure turned up across this period's AI decompilation research:
- code that compiles and passes every test still behaved differently on fuzzed inputs, 4.9% of the time and up to 13% ("Recompile More and Preserve Less", 4 Sep [ABS, checked here]);
- a test suite never run against deliberately broken versions passed wrong code (GameLogicBench [ABS]).

LEDGER's port is a matching problem of the same shape. Its golden rows are the only check.

**Do.**
1. A harness that builds seeded random days for the Hook's cast and runs the same inputs through the C# Core and the C++ port, comparing memory, gossip, suspicion and the police file tick by tick, and stopping at the first difference.
2. A mutation run: thirty one-line changes to the newest port headers; count how many the golden table catches and how many the fuzz harness catches.

**Pass.** The harness catches every mutant the review found, and no unexplained divergence remains over a thousand seeded days.

**Settles.** Whether what the town remembers in the game is what the design says, which is the core of the Meridian test.

**Cost.** About a day, on the processor; nothing bought. The Core side is a bounded town task, the port the builder's.

---

## Not worth a proof now

| Idea | Why not |
|---|---|
| World models and generated scenes (Genie, Marble, HY-World, Lyra) | Video or splats, not the street's geometry; licences exclude the EU and UK or are research-only; NVIDIA-class hardware |
| Image-to-3D for props (TRELLIS.2, Hunyuan3D, Meshy, Tripo) | NVIDIA with 24 GB or more; non-commercial or territory-limited; training data includes Sketchfab items now tagged NoAI |
| Neural "photoreal" filters (DLSS 5, GAN filters) | Not on an RX 6700; tainted training data; training one on Unreal output conflicts with the engine licence |
| Full-duplex speech-to-speech | Speaks before any check; the open ones are research-only or need 80 GB |
| AI tailoring | Not shown anywhere in this period; the field's data cannot express a lapel |
| Decompiling, modding or mashing up other games | Unlawful for this purpose (3-LEGAL.md); excluded by the brief |
