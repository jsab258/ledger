# Choosing what a character can say, then wording it: the professional pipeline, LLM-era practice, measurement, and steps for LEDGER (detail)

Research, 30 September 2026, by a separate research helper (about thirty minutes).

(The helper returned its text; the session that asked for it saved it here. That session checked three project facts against the files: the answerability labels give 44 of 60 agreement, Cohen's kappa 0.51, with one labeller saying "no" on 13 pairs; the checker's comment gives 100 of 108 invented replies caught and 42 of 132 honest ones refused on the bench's held-out half; and facts are chosen today by shared words (ClaimCheck.Bearing). It also marked the example line in step 1 as a made-up illustration. Nothing else was changed.)

**How the research was done.** Web access was narrow: GDC Vault, Valve's developer wiki, gamedeveloper.com, arxiv.org, ACL Anthology and most game and vendor sites were blocked. What worked:
- search summaries (marked SNIPPET);
- the arXiv export mirror, for full papers;
- raw GitHub, which is where Valve's released source code came from.

Valve's method below is taken from its code, not its slides.

**What this builds on, and does not repeat.** grounded-replies/NOTE-2026-09-29, PLAN-FIRST-2026-09-30 and MEASURED-2026-09-30; invented-claims/SUMMARY-2026-09-28; talk-helper/METHOD-2026-09-30; and the audit's "Dialogue writing" row. Already covered there:
- AIS, AttributionBench, FACTS Grounding, FaithJudge, BEGIN;
- plan-then-realise, RoleFact, TimeChara;
- Yarn Spinner saliency, Talk of the Town preconditions, Hidden Door;
- Inworld's graph, and the detective-game knowledge tree.

**Labels.** "Established" means practice that shipped or is published. "Recommendation" means my own reasoning for LEDGER.

---

## (a) The professional pipeline

The pipeline runs: knowledge representation → query → rule selection → authored or generated wording → memory written back.

### a1. Valve's Response System, reproducibly (established; read in Valve's released code)

**Sources.** Source SDK 2013: AI_ResponseSystem.cpp, ai_speech.cpp and baseentity.cpp. A 2010 version of the same library ("responserules/runtime"), as carried in the Mapbase mod base. Ruskin's GDC 2012 talk describes the Left 4 Dead use (SNIPPET, plus the earlier note's reading of the slide text).

**1. Knowledge representation.** Every entity holds a flat list of "contexts":
- each context is a key, a value, and an optional expiry time;
- adding a context splits "key:value:duration" and, when a duration is given, stores `now + duration` as its expiry;
- an existing key is overwritten;
- the world entity has its own contexts, which reach queries with a "world" prefix;
- global game states are also appended.

There is no belief model. "Who knows what" is simply which entity carries which key.

**2. The query ("criteria set").** When a character is to speak, the code builds a list of key → value pairs, each with a weight:
- "concept": the event or request, such as an idle remark or reacting to reloading. It always comes first, with a heavier weight.
- Optional modifiers from the caller, such as "subject:X".
- The speaker's own state. In the 2013 code this is: classname, name, health, health fraction, map, a random number from 0 to 100, NPC state, enemy, time since combat, speed, weapon, distance to the player, whether it sees the player, and whether the player sees it.
- Every context the speaker holds.
- The world's contexts and the player's criteria.

**3. Rules.** A rule is a named list of criteria plus response-group names and flags:
- "matchonce": disable the rule after it fires;
- "applyContext": facts to write back when it fires;
- "applyContextToWorld": write them to the world instead of the speaker.

A criterion names:
- a key;
- a matcher: an exact value, "!=" a value, or a numeric bound ">x", ">=x", "<x", "<=x", or both, as a range;
- a weight (default 1);
- an optional "required" flag.

Criteria can be nested groups.

**4. Scoring.** For each enabled rule:
- the score is the sum, over its criteria, of (criterion weight × weight of that key in the query) for each criterion that matches;
- a failed "required" criterion sets the rule's score to 0 and stops scoring it;
- a failed optional criterion adds nothing.

The best score wins, and it must be at least 0.001. Rules tied at the best score are chosen between at random.

- **In practice** writers mark the concept and most criteria "required". The effect is Ruskin's "most specific rule wins": a rule that also demands "has already said X" or "is near the fuel can" beats the general rule for the same concept.
- **Performance.** The 2010 library partitions rules by speaker and concept ("basically a separate-chained hash") so that only the relevant bucket is scored. The earlier note's reading of the slides gives about 10,000 lines in Left 4 Dead 2, each looked up in microseconds (not re-read today).

**5. Responses.** A rule points to response groups. Each response has:
- a type (speak, sentence, scene, response, print);
- a weight;
- optional flags: first, last, speakonce, odds (a 0–100 chance of speaking at all), respeakdelay, predelay.

Group flags are permitrepeats, sequential and norepeat (the group switches off once exhausted). Within a group the code picks by weighted chance among responses not yet used this cycle, with "first" and "last" slots handled specially.

**6. Writing back.** When the rule fires, its context string is added to the speaker (or the world). The next query therefore carries "said X", "knows Y" or "joke used", with an expiry if one was given. Running gags, "already told you" lines and cross-character memory all rest on this.

The 2010 library adds a "then" follow-up on a response: target, concept, contexts, delay. The code's own example is "subject TALK_ANSWER saidunplant:1 3", so one character's line queues another character's reply concept, carrying facts.

**7. Authoring "I don't know", partial answers and coverage.**
- Writers author the general case first: concept plus speaker only. Then they add specialised rules on top, each with more criteria.
- A "don't know" or deflection is simply the general rule for that concept. A partial answer is a rule that matches some of the facts.
- Nothing ever falls through to silence, unless the writers want silence (odds, norepeat).
- Debugging is by console: rr_debugresponses and rr_debugrule print why each rule scored as it did.

**Illustration for LEDGER (recommendation, not Valve's; the fact names are placeholders).**

| rule | criteria | response |
|---|---|---|
| `where_sleep_general` | concept=where_sleep | "don't know, ask Sheila", only if the speaker holds a fact that Sheila keeps the keys; otherwise a generic "ask at the office" |
| `where_sleep_knows` | concept=where_sleep, speaker holds F:tom_sleeps_flat | answer from that fact |
| `where_sleep_told` | the above, plus said:where_sleep=1 | "As I said, …" |

The most specific rule that matches wins.

### a2. Descendants and other ways of representing who knows what

**Games that choose written lines by conditions:**
- **Naughty Dog, The Last of Us** (Jason Gregory, GDC 2014). A context-aware dialogue system using individual knowledge, collective knowledge, global game state and the surroundings, run by the sound designers (SNIPPET; internals not read).
- **Firewatch** (Ewing and Armstrong, GDC 2017). It grew from "an interrupt heavy bark system" into long conversations that restart when interrupted, driven by a data-driven event system (SNIPPET; internals not confirmed).
- **Hades.** "Almost every line an NPC speaks sits behind a set of prerequisites". The game files' requirement keys include RequiredPlayed, RequiredFalsePlayed, RequiredAnyPlayed and the "this run / this room" variants, alongside game-state flags. Hades II adds per-line priority annotations (read in a fan tool's code; the exact priority algorithm is not confirmed).
- **Bethesda (Creation Kit).** A topic holds a stack of infos. "The first Info whose conditions return true is the Info the NPC will say". "Say Once" is kept per actor (SNIPPET).
- **BioWare (Dragon Age toolset).** NPC lines are tried in order against plot flags, and the first valid one plays. The toolset's advice is to make the last child line unconditioned "so that there will always be a default line" (SNIPPET).
- **Watch Dogs: Legion.** Each playable line was written in about 20 versions tied to procedural personas (GDC 2023; SNIPPET).

**Knowledge held as data, not prose:**
- **Shadows of Doubt.** Citizens record whom they saw, and those memories get fuzzier over time. Questioning gives timeline entries, not dialogue (DevBlog 10; SNIPPET).
- **Talk of the Town** (James Ryan). Each character holds mental models of others: belief facets such as hair colour or workplace. Each belief carries evidence of several kinds (observation, statement, lie, transference, confabulation, forgetting), each with a strength. Dialogue comes from an authored grammar whose symbols carry preconditions on game and conversation state and are tagged with dialogue moves (AIIDE 2015 and 2016, Game AI Pro 3; SNIPPET).

**Façade** (Mateas and Stern, 2004). Rules map typed text to about two dozen discourse acts, and authored reactions are chosen from those acts. The authors estimate understanding failed "about 30% of the time". The design deflects and recovers in character rather than failing visibly (SNIPPET).

**Not reached:** CK3's secrets (the knower lists are not confirmed), Versu, Disco Elysium.

### a3. What these have in common (established)

1. **Knowledge is held as structured facts,** per character and per world, often with expiry. It is not held as prose.
2. **Selection is done by code,** against conditions. The most specific match wins, and ordered lists end in an unconditioned default.
3. **Truth is guaranteed by selection.** A line can only play when its facts hold; nothing checks it afterwards.
4. **"Not known" and deflections are authored defaults, chosen.**
5. **Saying something writes a fact back.**

---

## (b) LLM-era games: what stays in code, what the model may do, how "not known" is handled

**Inworld: knowledge filters** (undated blog and docs; SNIPPET).
- Information falls into four categories: creator-specified, mutations of it, improbable character knowledge, and others.
- The filters are None, Mild and Strict. Strict allows only what was entered in the Core Description, Personal Knowledge or Common Knowledge, "suitable for suspects in a murder mystery".
- A separate "Fourth Wall" feature stops out-of-world mentions.
- No published rates. The earlier note covers its runtime graph.

**Ubisoft NEO NPC** (19 March 2024; SNIPPET). Writers author the backstory, knowledge and "guardrails". When a player veers off, the character quips and steers back.

**Meaning Machine, Dead Meat.** Authored story content steers an interrogation. It was shown on an on-device small model at CES and GDC 2025. The studio's player study reports that 95% enjoyed it (a marketing figure). Internals are not public (SNIPPET).

**Where Winds Meet** (NetEase, launched 14 November 2025; SNIPPET).
- The chat NPCs ("Jianghu Friends") could be talked into treating quests as done, for example by typing "(tells him the correct answer)".
- Lesson (established by counter-example): the model must never decide game state.

**Krafton CPC / PUBG Ally / inZOI** (CES, January 2025; SNIPPET). An on-device small language model built with NVIDIA ACE is fed game state. How it is grounded is not published.

**Mantella (Skyrim mod)** (docs undated; SNIPPET).
- It ships 3,000+ authored NPC biographies.
- NPCs get summaries only of conversations they were present for: a per-character perspective filter, in code.
- CHIM "defaults to ignorance" (earlier note).

**Trading NPCs** (arXiv, 9 July 2025; OPENED).
- A six-state machine, with the model writing a placeholder (`__PRICE__`) that code replaces with the computed value.
- Over 100 dialogues: >97% state compliance, >95% item-referencing accuracy, and 99.7% calculation precision.
- This is the delexicalised pattern: the model never writes the specific.

**Detective game with a knowledge tree** (19 September 2026; abstract OPENED). Critical hallucinations were cut by 64.78%, and premature disclosure was prevented. The strict rules forced some awkward reveals.

**Drama Llama** (15 January 2025; abstract OPENED). Storylets whose triggers are written in natural language and judged by the model. Authoring control is kept by the storylet structure.

**Ubisoft Ghostwriter** (22 March 2023; SNIPPET). The model drafts bark variants offline; writers choose and edit, and the game ships the approved lines. This is the "generate at authoring time, ship as authored" route.

**Production NLG outside games** (established; OPENED).
- Meta's conversational NLG generates from a tree-structured meaning representation and checks the output's structure ("tree accuracy").
- "Tree accuracy is also used in production to guard against hallucination: if tree accuracy fails, we fall back on templates to ensure correct response generation, even if it is less natural" (Arun et al., 8 November 2020).
- Constrained decoding reached >90% tree accuracy with 2,000 training examples; reranking by tree accuracy reached 97.6% and 95.4% (Balakrishnan et al., 17 June 2019).

**Cloud grounding checks** (SNIPPET / OPENED).
- AWS Bedrock's contextual grounding check gives a 0–1 score against a threshold you set. A higher threshold blocks more; the threshold is set to the use case's tolerance.
- Microsoft's groundedness detection offers "correction", which rewrites ungrounded sentences to match the sources (preview September 2024; doc dated 21 November 2025).
- Note: LEDGER's own "repair" of flagged replies failed its independent check (29 September), because kept fragments could affirm dropped claims.

**Summary of practice.**
- Kept in code: selection of facts, perspective (who was present), game state, and specifics such as prices and names.
- The model is allowed: wording, register, small talk, steering back.
- "Not known" is handled by an authored or configured ignorance, or a steer back; never by a checker silencing a reply.
- No product publishes its fallback or refusal rates.

---

## (c) Measurement

### c1. Labelled sets (established)

- **Include unanswerable questions written to look answerable.** SQuAD 2.0 did this with 50,000 such questions, and a strong system fell from 86% F1 to 66% F1 (June 2018).
- **Selective answering** is scored as coverage (how many are answered) against accuracy on those answered (Kamath, Jia and Liang, June 2020).
- **AbstentionBench** found reasoning fine-tuning degrades abstention by 24% on average, and that scaling is "of little use" (June 2025).
- **For LEDGER:** all 60 are answerable. The set therefore measures false refusal only, never invention under pressure.

### c2. Metrics

- **Trust-Score** (September 2024) computes precision and recall for refusals and for answers separately, and averages the two F1 scores (F1-GR). It names the errors: over-responsiveness, excessive refusal, over-citation, improper citation. RAGChecker (August 2024) works at claim level.
- **For LEDGER** (recommendation), per arm:
  1. fallback on answerable questions (false refusal);
  2. invented detail (two labellers);
  3. correct "don't know" on unanswerable questions;
  4. a blind naturalness preference on a sample, since grounding costs engagingness in every study in PLAN-FIRST.

### c3. How many questions (established method; figures are my simulation)

- **Miller / Anthropic** (1 and 19 November 2024) recommend:
  - clustered standard errors when questions come in groups (they can be "over 3X larger than naive");
  - resampling each question K times;
  - paired differences;
  - power analysis before running.
- **LEDGER's sixty are twenty questions × three characters,** so cluster by question.
- **My simulation** assumed the fallback rate starts at 36% and questions vary in how hard they are. With 60 questions × 3 runs per arm, compared question by question and grouped by question:

  | fall from 36% to | power |
  |---|---|
  | 30% (about 22 → 18 in 60) | about 30% |
  | 25% (about 22 → 15) | about 72–77% |
  | 20% (about 22 → 12) | about 96% |

  - Detecting 36% → 30% at 80% needs roughly 250 questions.
  - So the plan-first result (21.7 against 18.3) was never testable on this set.
- **Inventions.** At about 2 in 60, detecting even a rise to about 5 in 60 needs about 180 replies per arm. To certify "under 2%" with zero inventions takes about 150 clean replies (rule of three: upper 95% bound ≈ 3/N).

### c4. Agreement between labellers (established; LEDGER's figure computed from its own label file)

- AIS reported alpha 0.69–0.79; BEGIN, 0.7; RAGTruth, 91.8% per reply (earlier notes).
- **LEDGER's two answerability labellers** agreed on 44 of 60: Cohen's kappa ≈ 0.51, moderate.
  - One labeller said "no" on 13 pairs where the other said yes or partly.
  - The third labeller made all 60 at least partly answerable. Those 13 are exactly where a "don't know" might be defensible.
  - Recommendation: a one-page labelling guide with examples, a 20-item pilot, and kappa of 0.6 or more before trusting the labels. Report the 13 separately.

### c5. Calibrating a checker so it stops refusing true paraphrases (established methods)

1. **Measure it as a classifier on labelled details, not replies.**
   - TRUE (April 2022) reports ROC AUC, which needs no threshold. Where a threshold is needed, it is tuned on the development split by maximising the geometric mean of TPR and 1−FPR, and reported on test.
   - SummaC (November 2021) sets a threshold per dataset on validation data and reports balanced accuracy.
   - MiniCheck (April 2024) fixes the threshold at the score's midpoint for zero-shot use; a weaker variant fell from 69.1 to 59.9 balanced accuracy without tuning.
   - Hamel Husain (October 2024): one domain expert labels pass/fail with a written critique; the judge is scored against the expert by precision and recall; the few-shot examples come from a training split, never the test split.
2. **Choose the operating point deliberately.**
   - Conformal factuality (February 2024) removes the least-certain sub-claims until a target error rate α is met, calibrated on a labelled set. It achieved 80–90% correctness while keeping most of the output. Over calibration draws the result varied by about 0.09 (standard deviation), so small sets are noisy.
   - "The Semantic Illusion" (December 2025) used a calibration set of 600. Embedding and NLI detectors reached 100% false positives at the target coverage on real hallucinations (NLI AUC 0.81), while a GPT-4 judge had 7% false positives (95% CI 3.4–13.7%).
   - Lessons: surface-similarity checkers cannot separate hard cases; an LLM judge can; calibration needs hundreds of labelled items.
3. **Split claims sensibly.** WiCE (March 2023) found that automatic claim splitting helps entailment checkers. "Molecular facts" (June 2024) found fully atomic facts lose context; keep each claim just large enough to stand alone.
4. **LEDGER's current setting,** from the checker's own comment (the claim-check bench's held-out half, 30 September):
   - invented replies caught: 100 of 108 (about 93%);
   - honest replies refused: 42 of 132 (about 32%).

   That is one point on the precision–recall plane, not a chosen one.

---

## (d) Steps for LEDGER, in order (recommendation; effort is my estimate)

The measured bottleneck: planning did not beat selection in code, and the remaining fallbacks are replies the checker refuses twice (MEASURED). So the order targets the fallback's content and the checker first, and the rule table second.

**Step 0. Find where the fallbacks come from (half a day).**
- For each question: does the code-chosen top three contain an answering fact? This is selection recall.
- Label each of the day's 22 fallbacks (about 65 over three runs) as:
  - (a) selection missed;
  - (b) a real embellishment refused;
  - (c) a true paraphrase refused;
  - (d) the question is arguably not answerable (the 13 disputed pairs).

The mix decides how much steps 1 and 2 can gain.

**Step 1. A grounded fallback instead of a content-free one (about a day).** This is Meta's production pattern.
- When the redraft still fails, code builds the line from the chosen facts: a plain spoken form per fact, or per fact kind, in the character's register, with a short character opener.
  - Example (a made-up illustration of the shape, not canon or the game's facts): if the chosen facts were "the service was at Father Walsh's chapel" and "June came back for it", and the model's reply embellished them with "Father Walsh took the service" and was refused, code would say the chosen facts plainly instead: "It was at Father Walsh's chapel. June came back for it."
- Only facts the selection marked shareable are used. A deflecting intent keeps its deflection.
- "That's all I know" stays only when nothing was chosen.
- This never edits the model's words, so it avoids the failure mode of the 29 September repair.
- The spoken forms are dialogue, so one character's sample goes to Jafar's page.
- **Measure:** fallback rate, inventions (they should not rise, since every specific comes from a fact), and blind naturalness against the model's replies.

**Step 2. Calibrate the checker on a detail bench (one to two days).**
- **Build the bench.** About 250 details from existing runs: every flagged detail plus a sample of passed ones, including planted inventions.
  - Two labellers blind to the checker's verdict, with a third to settle.
  - Five labels: stated, implied (a plain listener would take it as the same thing or a direct consequence), added, contradicted, no claim. Plus the kind.
  - Split into a tuning half and a held-out half by question.
- **Move closed-class specifics to code:** names, numbers, times, days, vehicles, and places from the street list. Each must match a value or alias in the chosen facts. Code clears it on a match, and flags it when there is no match.
- **The model check keeps open-class additions** (size, manner, deeds, habits), where the strict "in the item itself" standard belongs, and event paraphrase, judged by the "implied" standard.
- **Worked examples only from the tuning half.**
- **Choose the variant** (standard per kind, number of looks, looks at the chosen facts only) with the lowest honest-refusal rate whose invented-pass rate on the held-out half is no worse than today's (about 7%). Compare variants on the same details with a paired McNemar test.
- Then rerun the 60 (step 4).

**Step 3. A small rule table for the first week (two to three days).**
- About 25–40 concepts for a newcomer's questions: who are you, what is this place, where do I sleep, the door, the boss, money, the will, Mickey, trust, food, family, what now. The model or keywords classify the player's line into one; "other" falls through to today's path.
- Per concept, rules with criteria on:
  - the speaker;
  - facts held;
  - wariness;
  - time;
  - "already told".
- Each rule yields:
  - an answer type (answer, partial, "don't know, ask X", deflect, refuse);
  - the fact ids;
  - optionally an authored line for indispensable beats.
- The most specific rule wins, and a default exists for every concept.
- "Ask X" only when the speaker holds a fact that X knows.
- After speaking, write back "told Tom F-id": a fact about the conversation, never prose as evidence.
- The authored beats and deflections are dialogue, so they go to Jafar's page.

**Step 4. Measure each change so a difference is real (ongoing; about half a day to set up).**
- Question sets:
  - the 60 as the tuning set;
  - a held-out 60 of new newcomer questions, written by a helper who has seen neither the facts nor the failures;
  - 30 unanswerable or leading questions ("You saw the van, didn't you?").
- 3 runs per arm; paired comparison per question, grouped by question.
- Report the four measures in c2.
- A change counts only if it holds on the held-out set. Expect to see only large effects (see c3).

**Money or scope for Jafar** (none needed for steps 0–4): a stronger checker model (about twice the cost per check), or a small local checker (graphics card and licence).

---

## (e) What could not be verified or reached

- **Valve.** Ruskin's slides and talk, and Valve's developer wiki, were blocked. The method is from the 2013 SDK code and a 2010 library copy carried in Mapbase; which Valve game that copy shipped with is not confirmed. Left 4 Dead line counts come from the earlier note, not re-read.
- **Other games' internals.** The Last of Us, Firewatch, Hades' priority algorithm, Watch Dogs: Legion's Census, CK3's secrets, Shadows of Doubt's memory model: all SNIPPET level or not reached.
- **LLM-era products.** Inworld, NEO NPC, Dead Meat, Where Winds Meet, Krafton's CPC and NVIDIA ACE titles: no published internals or rates. Vaudeville, Suck Up! and 1001 Nights: nothing technical found.
- **Fallback rates.** No studio publishes how often its characters say "don't know".
- **My own figures.** The sample-size numbers are my simulation, with an assumed spread of difficulty across questions.

---

## Sources

**Valve and game code**
- AI_ResponseSystem.cpp (Source SDK 2013) — Valve — undated repository file — https://raw.githubusercontent.com/ValveSoftware/source-sdk-2013/master/src/game/server/AI_ResponseSystem.cpp — read 30 Sep 2026 — OPENED
- ai_speech.cpp (Source SDK 2013) — Valve — undated — https://raw.githubusercontent.com/ValveSoftware/source-sdk-2013/master/src/game/server/ai_speech.cpp — read 30 Sep 2026 — OPENED
- baseentity.cpp (Source SDK 2013) — Valve — undated — https://raw.githubusercontent.com/ValveSoftware/source-sdk-2013/master/src/game/server/baseentity.cpp — read 30 Sep 2026 — OPENED
- response_system.cpp / response_system.h (responserules runtime, header "1996-2010") — Valve, as carried in Mapbase — undated — https://raw.githubusercontent.com/mapbase-source/source-sdk-2013/master/sp/src/responserules/runtime/response_system.cpp — read 30 Sep 2026 — OPENED
- AI-driven Dynamic Dialog through Fuzzy Pattern Matching — Elan Ruskin, Valve — GDC 2012 — https://www.gdcvault.com/play/1015528/AI-driven-Dynamic-Dialog-through — read 30 Sep 2026 — SNIPPET
- GDC 2012 Talk on Dynamic Dialogue — Emily Short — 16 Mar 2012 — https://emshort.blog/2012/03/16/gdc-2012-talk-on-dynamic-dialogue/ — read 30 Sep 2026 — SNIPPET
- A Context-Aware Character Dialog System — Jason Gregory, Naughty Dog — GDC 2014 — https://www.gdcvault.com/play/1020386/A-Context-Aware-Character-Dialog — read 30 Sep 2026 — SNIPPET
- Do You Copy? Dialog System and Tools in Firewatch — Patrick Ewing and William Armstrong — GDC 2017 — https://www.gdcvault.com/play/1024000/Do-You-Copy-Dialog-System — read 30 Sep 2026 — SNIPPET
- Hades Dialogue Explorer (README and generate_data.py) — NikkelM — undated — https://github.com/NikkelM/HadesDialogueExplorer — read 30 Sep 2026 — OPENED
- Dive into the dialogue of Hades at GDC 2021 — Game Developer — 2021 — https://www.gamedeveloper.com/audio/dive-into-the-dialogue-of-i-hades-i-at-gdc-2021 — read 30 Sep 2026 — SNIPPET
- Topic Info — CreationKit Wiki — undated — https://ck.uesp.net/wiki/Topic_Info — read 30 Sep 2026 — SNIPPET
- Conversation tutorial / Conversation — Dragon Age Toolset Wiki — undated — http://www.datoolset.net/wiki/Conversation_tutorial — read 30 Sep 2026 — SNIPPET
- How Watch Dogs: Legion changed Ubisoft's narrative design — Game Developer (Brandon Hennessy, GDC 2023) — 2023 — https://www.gamedeveloper.com/marketing/how-i-watch-dogs-legion-i-made-ubisoft-rethink-its-storytelling — read 30 Sep 2026 — SNIPPET
- Shadows of Doubt DevBlog 10: Gameplay Loop — ColePowered Games — undated — https://colepowered.com/shadows-of-doubt-devblog-10-gameplay-loop/ — read 30 Sep 2026 — SNIPPET
- Simulating Character Knowledge Phenomena in Talk of the Town — James Ryan and Michael Mateas, Game AI Pro 3 — 2017 — https://www.gameaipro.com/GameAIPro3/GameAIPro3_Chapter37_Simulating_Character_Knowledge_Phenomena_in_Talk_of_the_Town.pdf — read 30 Sep 2026 — SNIPPET
- Characters Who Speak Their Minds: Dialogue Generation in Talk of the Town — Ryan et al., AIIDE — 2016 — https://cdn.aaai.org/ojs/12877/12877-52-16394-1-2-20201228.pdf — read 30 Sep 2026 — SNIPPET
- Natural Language Understanding in Façade: Surface-Text Processing — Michael Mateas and Andrew Stern, TIDSE — 2004 — https://link.springer.com/chapter/10.1007/978-3-540-27797-2_2 — read 30 Sep 2026 — SNIPPET

**LLM-era games and products**
- Knowledge Filters: Introducing new ways to constrain what your NPC knows — Inworld AI — undated — https://inworld.ai/blog/knowledge_filters — read 30 Sep 2026 — SNIPPET
- How Ubisoft's New Generative AI Prototype Changes the Narrative for NPCs — Ubisoft — 19 Mar 2024 — https://news.ubisoft.com/en-us/article/5qXdxhshJBXoanFZApdG3L — read 30 Sep 2026 — SNIPPET
- GAME CONSCIOUS AI — Meaning Machine — undated — https://www.meaningmachine.games/game-conscious-ai — read 30 Sep 2026 — SNIPPET
- Recap: Dead Meat Player Study — Bristol Digital Game Lab — 5 May 2025 — https://bristoldigitalgamelab.blogs.bristol.ac.uk/2025/05/05/recap-dead-meat-player-study/ — read 30 Sep 2026 — SNIPPET
- Where Winds Meet Player Has NSFW Chat Session With AI NPC — Kotaku — undated in snippet (game launched 14 Nov 2025) — https://kotaku.com/where-winds-meet-ai-npc-llm-chatgpt-steam-2000650074 — read 30 Sep 2026 — SNIPPET
- Where Winds Meet Players Exploit AI to Skip Quests — Outlook Respawn — undated — https://respawn.outlookindia.com/gaming/gaming-news/where-winds-meet-ai-exploit-lets-players-skip-quests — read 30 Sep 2026 — SNIPPET
- [CES 2025] KRAFTON showcased AI model CPC built with NVIDIA ACE — Krafton — Jan 2025 — https://www.krafton.com/en/news/press/ces-2025-krafton-showcased-ai-model-cpc-built-with-nvidia-ace/ — read 30 Sep 2026 — SNIPPET
- Mantella README and docs — art-from-the-machine — undated — https://github.com/art-from-the-machine/Mantella/blob/main/README.md — read 30 Sep 2026 — SNIPPET
- State-Inference-Based Prompting for Natural Language Trading with Game NPCs — Kim et al. — 9 Jul 2025 — https://arxiv.org/abs/2507.07203 — read 30 Sep 2026 — OPENED
- Enforcing Narrative Reliability and Epistemic Pacing in LLM-Driven Detective Games via Structured Knowledge Trees — Rahmati and Zhao — 19 Sep 2026 — https://arxiv.org/abs/2609.23043 — read 30 Sep 2026 — OPENED (abstract)
- Drama Llama: An LLM-Powered Storylets Framework — Sun et al. — 15 Jan 2025 — https://arxiv.org/abs/2501.09099 — read 30 Sep 2026 — OPENED (abstract)
- Staying In Character: Perspective-Bounded Memory for Book-Based Role-Playing Agents — Tang et al. — 24 Jun 2026 — https://arxiv.org/abs/2606.25632 — read 30 Sep 2026 — OPENED (abstract)
- Here are more details on Ubisoft's Ghostwriter AI tool from GDC 2023 — Game Developer — Mar 2023 — https://www.gamedeveloper.com/marketing/here-are-more-details-on-ubisoft-s-narrative-ai-tools-from-gdc-2023 — read 30 Sep 2026 — SNIPPET

**Production NLG and grounding checks**
- Best Practices for Data-Efficient Modeling in NLG — Arun et al., Meta — 8 Nov 2020 — https://arxiv.org/abs/2011.03877 — read 30 Sep 2026 — OPENED
- Constrained Decoding for Neural NLG from Compositional Representations in Task-Oriented Dialogue — Balakrishnan et al. — 17 Jun 2019 — https://arxiv.org/abs/1906.07220 — read 30 Sep 2026 — OPENED
- Use contextual grounding check to filter hallucinations in responses — AWS — undated — https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-contextual-grounding-check.html — read 30 Sep 2026 — SNIPPET
- Groundedness detection in Azure AI Content Safety — Microsoft — 21 Nov 2025 — https://github.com/MicrosoftDocs/azure-ai-docs/blob/main/articles/ai-services/content-safety/concepts/groundedness.md — read 30 Sep 2026 — OPENED
- Correction capability helps revise ungrounded content and hallucinations — Microsoft — Sep 2024 — https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/correction-capability-helps-revise-ungrounded-content-and-hallucinations/4253281 — read 30 Sep 2026 — SNIPPET

**Measurement and checker calibration**
- Know What You Don't Know: Unanswerable Questions for SQuAD — Rajpurkar, Jia and Liang — 11 Jun 2018 — https://arxiv.org/abs/1806.03822 — read 30 Sep 2026 — OPENED (abstract)
- Selective Question Answering under Domain Shift — Kamath, Jia and Liang — 16 Jun 2020 — https://arxiv.org/abs/2006.09462 — read 30 Sep 2026 — OPENED (abstract)
- AbstentionBench — Kirichenko et al. — 10 Jun 2025 — https://arxiv.org/abs/2506.09038 — read 30 Sep 2026 — OPENED (abstract)
- Measuring and Enhancing Trustworthiness of LLMs in RAG (Trust-Score) — Song et al. — 17 Sep 2024 — https://arxiv.org/abs/2409.11242 — read 30 Sep 2026 — OPENED
- RAGChecker — Ru et al. — 15 Aug 2024 — https://arxiv.org/abs/2408.08067 — read 30 Sep 2026 — OPENED (abstract)
- Adding Error Bars to Evals — Evan Miller, Anthropic — 1 Nov 2024 — https://arxiv.org/abs/2411.00640 — read 30 Sep 2026 — OPENED
- A statistical approach to model evaluations — Anthropic — 19 Nov 2024 — https://www.anthropic.com/research/statistical-approach-to-model-evals — read 30 Sep 2026 — OPENED
- TRUE: Re-evaluating Factual Consistency Evaluation — Honovich et al. — 11 Apr 2022 — https://arxiv.org/abs/2204.04991 — read 30 Sep 2026 — OPENED
- SummaC — Laban et al. — 18 Nov 2021 — https://arxiv.org/abs/2111.09525 — read 30 Sep 2026 — OPENED
- MiniCheck — Tang, Laban and Durrett — 16 Apr 2024 — https://arxiv.org/abs/2404.10774 — read 30 Sep 2026 — OPENED
- Language Models with Conformal Factuality Guarantees — Mohri and Hashimoto — 15 Feb 2024 — https://arxiv.org/abs/2402.10978 — read 30 Sep 2026 — OPENED
- The Semantic Illusion: Certified Limits of Embedding-Based Hallucination Detection in RAG Systems — Debu Sinha — 17 Dec 2025 — https://arxiv.org/abs/2512.15068 — read 30 Sep 2026 — OPENED (abstract)
- WiCE: Real-World Entailment for Claims in Wikipedia — Kamoi et al. — 2 Mar 2023 — https://arxiv.org/abs/2303.01432 — read 30 Sep 2026 — OPENED (abstract)
- Molecular Facts — Gunjal and Durrett — 28 Jun 2024 — https://arxiv.org/abs/2406.20079 — read 30 Sep 2026 — OPENED (abstract)
- Using LLM-as-a-Judge For Evaluation: A Complete Guide — Hamel Husain — Oct 2024 — https://hamel.dev/blog/posts/llm-judge/ — read 30 Sep 2026 — SNIPPET

**LEDGER's own material (not web)**
- production/research/invented-claims/bench/firsts-answerable.jsonl: the answerability labels, from which the agreement and kappa are computed.
- ledger/Assets/Scripts/Core/ClaimCheck.cs: the comment on the checker's "Looks" setting (catch and refusal rates), and Bearing (how facts are chosen today).
- production/research/grounded-replies/MEASURED-2026-09-30.md: the measurement of 30 September.
