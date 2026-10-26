# Repairing one sentence instead of the whole reply (26 October 2026)

Order ledger item `o26-speech-slow-replies` (his answer of 26 October, 2): give the reply tighter facts so fewer first sentences fail the check; when one fails, rewrite only that sentence; count the replies that wait 5 s or more, before and after.

**How this was read.** Every source below was read on 2026-10-26 through a fetch tool that returns a model-written digest of the page, not the raw text. Long papers were often read only up to about 100,000 characters (noted in the last section). Question 3 was researched by a parallel helper under the same rules; I re-read one of its sources (TimeChara) and its numbers matched. No paid model calls were made and nothing was measured here: every latency for our game below is an estimate and is marked so.

## Where our time goes now (our own records)

- From production/research/voice-latency/CAST-VOICE-2026-10-25.md (20 live turns, 25 October): the first sentence is drafted at 0.75 s (median) and checked by 2.01 s. The check alone takes about 1.1 s, and the slowest check took until 6.43 s. **6 of 20 turns failed the first check, and those were heard at 5 to 9 s.** The 14 turns that passed were heard at 2.9 to 4.9 s, with the slow cast voice on the card (about 2.8 s).
- From production/research/voice-latency/POCKET-SWITCH-2026-10-26.md: since 26 October, Sheila and Ron speak through Pocket, whose first sound comes about 0.2 s after the line. Darren still uses the card voice, at about 2.5 s.
- What a failed first sentence costs today: draft (0.75 s), then check (1.1 s), then a second draft from the reply model (a new request, about 0.75 s more to its first sentence), then a second check (1.1 s), then the voice. That is about 3.9 s plus the voice, with two model round trips and two checks in a row. For Darren every failure is therefore over 5 s. For Sheila and Ron a failure lands at around 4 s, and any slow step pushes it past 5 s.
- From FINDINGS.md (September bench): about 30% of honest replies were flagged by the check and redrafted. Many failures are therefore false alarms by the check, not inventions by the reply. Tightening the reply's facts cannot remove those.
- The reply's facts today (ConversationEngine.BuildSystemPrompt): the card, every belief, and the top 8 memories retrieved for the line (MemoryRetrieval, topK = 8), each tagged with its time. Facts carry no IDs.

## 1. How others repair an unsupported sentence

| Method | What is regenerated | What the repair call gets | Added time | The rest of the draft |
|---|---|---|---|---|
| **RARR** (Gao et al.; PaLM 540B, few-shot) | One span. The editor rewrites the passage, but only one span is meant to change. Edits of more than 50 characters, or more than half the text, are rejected | The current passage, one question, one piece of evidence. One agreement call per (question, evidence) pair, one edit call per disagreement | About 40 s for each statement (reported in the PURR paper) | Kept. Edits are applied one after another, each seeing the earlier ones. Original intent was kept in over 90% of cases |
| **PURR** (Chen et al.; T5-large) | The whole statement, in one editing pass | Statement, questions and all evidence together | About 2 s for each statement, against RARR's 40 s (on different hardware) | Kept. Attribution and preservation were both better than RARR's on all three datasets, e.g. NQ: attribution 44.8 → 59.8 and preservation 91.0 (RARR: 53.8 and 89.6) |
| **FAVA** (Mishra et al.; Llama-2 7B, fine-tuned) | Marked spans only, which are deleted or replaced inside the passage | The prompt, the output and 5 retrieved documents, in one call | Not reported | Kept. Note: ChatGPT used as the editor *lowered* the factual score of ChatGPT's own outputs by 8.1 points, while FAVA raised it by 3.3 |
| **Verify-and-Edit** (Zhao et al.; text-davinci-003) | Each uncertain reasoning sentence, which is replaced by its verified answer | Only a verifying question and the retrieved facts: not the other sentences, not the original question | Cost $0.014 per Fever item, against $0.017 for ReAct | The final answer is **regenerated** from the edited reasoning. Editing ran on about 40% of items |
| **EVER** (Kang et al.; GPT-3.5, Llama 2) | One sentence at a time, before the next is written. A wrong fact: the faulty concepts are revised. An unsupported detail: the whole sentence is rewritten with feedback and evidence, then checked once more | The sentence, feedback naming the problem, and the evidence. The rectification prompt itself is not published | Average runtimes of 115 to 196 s per biography (GPT-3.5), close to RARR's 210 s | Later sentences are written after the repaired one. The paper argues that editing after the fact cannot stop errors "snowballing" into later sentences, but it never measures this. One round fixed nearly all wrong facts (94.5 FactScore) |
| **CoVe** (Dhuliawala et al.; Llama 65B) | The **whole** final response, rewritten from the draft plus verification answers | The verification questions are answered *without* seeing the draft, so the model cannot copy its own mistake; that variant scored best | Not measured; "more LLM prompts", which can run in parallel | Replaced. FactScore 55.9 → 71.4 |

**Streaming guardrails and voice agents (named companies' documentation).** None of them repairs one sentence and carries on:
- **NVIDIA NeMo Guardrails, output-rail streaming.** It checks chunks of 200 tokens by default, carrying 50 tokens of overlap from the previous chunk. When a chunk is blocked, the stream "yields a JSON error object… and terminates". There is no repair. The low-latency profile uses 50-token chunks and sends text before it is checked.
- **Guardrails AI.** It validates each chunk as it streams. A "fix" is a programmatic correction by the validator itself (for example masking personal data), and fixes from several validators are merged with diff-match-patch. In streaming, re-asking the model is "No `reask` support" (company blog, 17 January 2024; its current status is UNVERIFIED).
- **Amazon Bedrock Guardrails.** In synchronous mode, chunks are buffered and scanned, which adds delay. In asynchronous mode they are sent at once and, after a violation, "subsequent chunks will be blocked". There is no repair.
- **LiveKit recipe.** Text is buffered to each full stop, and a second model judges every sentence before speech. On a failure it yields "Content filtered." and ends the reply. Every sentence waits a full judging round trip.
- **ElevenLabs Agents.** In streaming mode, the only exit is ending the call, and up to about 500 ms of audio may already have played. Blocking mode "typically adds 200–500 ms" and allows "Retry". Retry removes the whole turn, injects feedback and generates again, up to three times.
- **OpenAI Agents SDK, realtime voice.** When a guardrail trips, the SDK interrupts the response, cancels it and sends a follow-up message naming the guardrail, "so the model can produce a replacement response". The whole turn is regenerated.
- **Uniphore (company blog, 7 April 2026).** Buffering the whole reply "adds 1-3 seconds of latency before the user hears anything". On a factual failure, the model is asked to regenerate with an error message.
- **Games.** I found no primary source from a game company describing how a failed line is repaired (see the unreached list).

**What this means.** In shipped products the norm is to cut the reply or regenerate the whole turn. Sentence-level repair exists only in research systems, which run offline and slowly, at seconds to minutes per passage. Where they report results, the lessons are:
- Edit only the refused span, and keep the rest of the sentence word for word (RARR, PURR, FAVA). This keeps intent and makes the result predictable.
- Give the editor the evidence and the exact problem. An editor without them made things worse (FAVA's ChatGPT row).
- Check the edited sentence again before it is used (EVER).
- Most of the measured gain came from narrowing the input. In EVER, the variants given retrieved evidence scored 76.9 to 87.3, against 46.7 to 47.5 for self-questioning on Llama 2. Repairing alone counted for less.

## 2. Keeping the following sentences coherent

There are three options:
- **A. Keep the original draft's later sentences and check each one.** This is what RARR, PURR and FAVA do, but they edit with the whole passage in view. In our stream, sentences 2 onward were written *after* the refused detail, so they may lean on it (EVER's and CoVe's "snowballing"). An example: "Dennis did it. **He** was drunk again." The claim check judges whether a detail is supported, not whether the reply still makes sense.
- **B. Generate the rest from the repaired sentence.** This is what EVER, Self-RAG and Lookback Lens do. Self-RAG writes one sentence at a time, keeps the best 2 candidates and conditions each new sentence on the chosen ones. Lookback Lens samples 8 candidate chunks of 8 tokens and keeps the best, but takes 20 to 60 s per example. Verify-and-Edit also regenerates its answer from the edited reasoning.
- **C. End the reply after the repaired sentence.** It costs nothing, and a one-sentence answer is natural speech.

**Fastest for a voice reply: B, started the moment the repaired first sentence passes its check, with C as the fallback.** The rest is then written and checked *while* the first sentence is playing, which takes about 1.5 s for a typical first sentence (CAST-VOICE note). If the next sentence is not checked by the time the first one ends, the character stops there. This is my design inference from the sources above, not a measured result.

**How to continue without prefill.** On the models we use for replies, a reply cannot be continued by prefilling (see section 4). Anthropic documents the replacement: put the text already said into the user turn, for example "Your previous response was interrupted and ended with `[previous_response]`. Continue from where you left off."

## 3. Grounding prompts that reduce unsupported claims

These findings come from the research helper. Most results are on older models (GPT-3.5, text-davinci-003, LLaMA-2, 7B models); only Chroma's study and Anthropic's own pages involve Claude. The list is ranked by strength of evidence.

1. **Give fewer, more relevant facts (about 3 to 5), and drop near-misses.** Eight sources agree.
   - One irrelevant sentence cut accuracy from 95.0 to 72.4 (Shi et al. 2023, code-davinci-002).
   - With the answer placed in the middle of 20 documents, GPT-3.5 scored 53.8%, below its 56.1% with no documents at all (Lost in the Middle).
   - Documents related to the question but without the answer cut accuracy by up to 67% (Cuconasu et al. 2024, 7B models).
   - In ALCE, ChatGPT's correctness stopped improving after the top passage, and its citation quality after the top 3.
   - All 18 models in Chroma's "Context Rot" study (July 2025, including Claude Opus 4 and Sonnet 4) scored better on focused prompts of about 300 tokens than on full ones.
   - In RoleFact, more than five retrieved documents "may hurt".
2. **One line stating what the character does not know.**
   - TimeChara (GPT-4o): a one-line hint such as "{character} had not participated in the scene" raised consistency from 64.5% to 82.2% on average, and from 46.0% to 94.5% on questions about the character's future. With retrieval limited to what the character could know, the average reached 87.5%.
   - Plain retrieval *lowered* GPT-4 Turbo's score on those questions, from 46.5% to 33.5%.
   - Our game already knows what each person saw and did not see, so this line can come from the simulation without an extra model call. This is an inference and has not been tested.
3. **Answer only from these facts, and have a ready in-character way of not knowing.**
   - Framing the context as the speaker's own account, plus an instruction, cut answers taken from the model's own memory from 35.2% to 9.1%. Correct "don't know" answers rose from 30.6% to 87.8% (Zhou et al. 2023, text-davinci-003).
   - Anthropic's "Reduce hallucinations" guide recommends the same steps but gives no numbers.
   - Instructions alone help less than changing what the model is shown (System 2 Attention: 62.8% to 71.7% from an instruction, against 80.3% from cleaning the context).
4. **Fact IDs with "cite the fact you use".** They help the checker but do not prove support. About half of the cited answers from ChatGPT and GPT-4 were not fully backed by the passages they cited (ALCE). Up to 57% of Command-R+'s citations were added after the fact to an answer it had taken from memory (Wallat et al. 2024). Anthropic's own Citations figures ("up to 15%" better recall) are vendor claims and UNVERIFIED.
5. **Asking for quotes first** has been measured only on long documents. For a short fact list it would only add tokens before the first word, so it should be left out.
6. **Persona-sheet formats.** No measured comparison was found.

**A guard for our case.** Only the *reply's* facts should be narrowed. The check must keep the character's full knowledge (card, all beliefs, every memory); otherwise true details the reply knows from its card would start failing, and the false-alarm rate would rise.

## 4. Anthropic specifics (current docs, read 26 October)

- **Prefill is not available on the reply models.**
  - "Prefilling is not supported on Claude 4.6 and later models", and such requests "return a 400 error" (Using the Messages API). That covers Sonnet 5, Sonnet 5.5 and Haiku 5.5.
  - The error text reads: "This model does not support assistant message prefill. The conversation must end with a user message." (API errors page).
  - Claude Haiku 4.5, our small-talk model, still "accepts one when thinking is off" (Haiku 5.5 migration guide).
  - The documented replacement for continuations is to move the text into the user message, as in section 2.
  - The stop-reasons page shows the same idea another way: the earlier text as an assistant turn, followed by a user turn "Please continue from where you left off."
- **A later system message.** On Sonnet 5.5 and Haiku 5.5 (not Sonnet 5), a system message can be added later in the conversation without spoiling the cached prompt. It could carry the "already said" text.
- **Stop sequences.**
  - When a model emits one of your `stop_sequences`, `stop_reason` is `"stop_sequence"` and the `stop_sequence` field names which one fired (Messages API reference).
  - Whether the stop text itself appears in the output is not stated on the pages read (UNVERIFIED).
  - For a one-sentence repair, a full-stop stop sequence would also cut "Mr." or "9.30". A small `max_tokens` plus "one sentence" is safer, and our own sentence splitter already does the cutting.
- **Latency.**
  - The docs give no time-to-first-word figures. Models are ranked only: Haiku 5.5 "Fastest", Sonnet 5.5 "Fast".
  - The advice is to choose Haiku 5.5 at low effort, keep prompts and outputs short, and stream.
  - Haiku 5.5 thinks by default (adaptive). Thinking before the first word costs time. `thinking: {"type": "disabled"}` is accepted on Haiku 5.5 at effort `high` or below. On Sonnet 5.5, `between_tools` is the setting with no up-front thinking.
  - Haiku 5.5 counts about 30% more tokens than Haiku 4.5 for the same text.
  - Prompt caching: no percentage is given, only "improved time-to-first-token for long documents". The minimum cacheable prompt is 512 tokens on Haiku 5.5 and Sonnet 5.5, 1,024 on Sonnet 5 and 4,096 on Haiku 4.5. We measured at most about 0.15 s from caching at our prompt size (1 October).
- **An aside.** From API version `2026-10-21`, any `temperature`, `top_p` or `top_k` returns a 400 on every model. This matters if the talk helper ever moves to that version.

## Recommendation: the fastest sound method for our case

1. **Measure "before" first, on enough turns.** A count of 2 to 6 in 20 is too noisy to show a change. The plan:
   - Run the same script of at least 60 turns, 20 each for Sheila, Ron and Darren, with the real model in the packaged game.
   - Record each turn's steps (`draft`, `check`, `redraft`, `recheck` are already in the talk protocol).
   - Count the turns heard at 5 s or later, for each voice.
   - Measure the first-sentence failure rate separately on the 240-turn held-back bench (no voice needed). Split each failure into "invented" and "false alarm".
2. **Tighten the reply's facts (the reply only).**
   - Give it the top 3 to 5 memories for the line instead of 8, and only the beliefs that bear on it.
   - Add one line, built from the simulation, naming what the character did not see.
   - Add the character's own way of saying "can't say" from their casting sheet.
   - Add the instruction "say only what these and your card support".
   - Short fact IDs are optional and serve the checker.
3. **When a first sentence fails, rewrite only that sentence.**
   - Stop the stream, as today.
   - Make one call to the fastest model: Haiku 5.5, thinking off or low effort, `max_tokens` about 60.
   - Give it the voice line, the player's line, the tightened facts, the failed sentence and the refused details.
   - Ask for: "the same sentence with these details removed or replaced by not knowing; add nothing".
   - Check the result with the same check; then voice it. If it fails, the existing fallback line follows.
4. **The rest of the reply.** As soon as the repaired sentence passes, ask the reply model for at most two more sentences, quoting what was said in the user turn (prefill is not allowed). Check them as usual and play them if they are ready when the first sentence ends; otherwise the reply ends there.
5. **Only if waits of 5 s or more remain:** start the sentence rewrite at the same moment as the first check, using the drafted sentence and "add nothing the facts do not support". Use it only if the check fails. It costs one small Haiku call per turn and saves the rewrite's own time.

**Expected effect (UNMEASURED; estimates from the timings above).**
- **Rewriting one sentence instead of the whole reply saves little on its own.** Both paths pay one more model round trip and one more check. The rewrite is faster only because its call is smaller and runs on the fastest model: perhaps 0.2 to 0.4 s per failure. With step 5, a failure for Sheila or Ron would be heard at about 3.2 s instead of about 4 s.
- **The bigger lever is fewer failures (step 2).** The sources suggest a real drop in invented details, but the size on Claude and on our cast is unknown. The check's false alarms (about 30% of honest replies in September) are not touched by it.
- **What to expect, by voice:**
  - Sheila and Ron: most waits of 5 s or more should go, leaving the slow checks (one took until 6.4 s).
  - Darren: each failure still costs over 5 s while he stays on the card voice, so his count falls only with his failure rate.
- **Overall:** from 2 to 6 in 20 now, perhaps to 0 to 2 in 20. That is a guess, to be replaced by the "after" run on the same script.

## Unverified / not reached

- **"The Tail at Scale"** (hedged requests, the general basis for step 5): the ACM page returned 403 and the author's PDF could not be read. It is not relied on.
- **Inworld's KnowledgeFilter docs:** behind a sign-in page, not read. No primary source from a game company on repairing a line was found. NVIDIA ACE pages found describe speech and faces only.
- **Guardrails AI:** "no reask in streaming" comes from a January 2024 post. Its current state is UNVERIFIED.
- **OpenAI Agents SDK:** the unit and default of `debounce_text_length` are not stated.
- **RARR:** the last 43,000 characters were not read. PURR's 2 s and RARR's 40 s were measured on different hardware.
- **EVER:** the rectification prompt is not published, and conditioning later sentences on the repaired one is implied, not stated.
- **Partial reads:** Self-RAG and Lookback Lens were read in part only.
- **Stop sequences:** whether the stop text is included in the output is UNVERIFIED.
- **Model speed:** no time-to-first-word numbers for Haiku 5.5 or Sonnet 5/5.5 exist in the docs. Every repair-call time above is an estimate.
- **Anthropic Citations:** the "up to 15%" and the customer "10% to 0%" figures are vendor claims, UNVERIFIED.
- **Helper's list for question 3:**
  - The arXiv PDFs of ALCE and Zhou et al. were unreadable and were read through ar5iv.
  - The endings were not read for TimeChara (80,000 characters), AbstentionBench, ALCE, Jin et al., Zhang et al. and the role-play refusal paper.
  - Numbers that exist only in figures were not read: Anthropic's long-context post for each technique, Chroma's distractor results, Jin et al. and AbstentionBench.
  - Read as abstracts only: CHARM and "Staying In Character".
  - Not read: RoleLLM, Character-LLM, Chain-of-Note, AuthorityBench and FACTS Grounding.
- **Not checked by a fresh reviewer.** Per the research rule, the recommendation above needs one fresh reviewer against these sources before it becomes the design.

## Sources (all read 2026-10-26)

Repair methods:
- RARR, https://ar5iv.labs.arxiv.org/html/2210.08726
- PURR, https://ar5iv.labs.arxiv.org/html/2305.14908
- FAVA, https://ar5iv.labs.arxiv.org/html/2401.06855
- Verify-and-Edit, https://ar5iv.labs.arxiv.org/html/2305.03268
- EVER, https://ar5iv.labs.arxiv.org/html/2311.09114
- CoVe, https://ar5iv.labs.arxiv.org/html/2309.11495
- Self-RAG, https://ar5iv.labs.arxiv.org/html/2310.11511
- Lookback Lens, https://ar5iv.labs.arxiv.org/html/2407.07071

Guardrails and voice agents:
- NeMo Guardrails, https://docs.nvidia.com/nemo/guardrails/latest/configure-guardrails/yaml-schema/streaming/output-rail-streaming
- Guardrails AI, https://guardrailsai.com/guardrails/docs/concepts/streaming/streaming_fixes and https://www.guardrailsai.com/blog/validate-llm-responses-real-time
- Bedrock, https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-streaming.html
- LiveKit, https://docs.livekit.io/reference/recipes/llm_powered_content_filter/
- ElevenLabs, https://elevenlabs.io/docs/agents-platform/best-practices/guardrails
- OpenAI Agents SDK, https://openai.github.io/openai-agents-python/realtime/guide/
- Uniphore, https://www.uniphore.com/blog/multi-layer-guardrails-for-voice-agents/

Anthropic:
- https://platform.claude.com/docs/en/build-with-claude/working-with-messages
- https://platform.claude.com/docs/en/api/errors
- https://platform.claude.com/docs/en/models/haiku-5-5/migration-guide
- https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons
- https://platform.claude.com/docs/en/api/messages/create
- https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-latency
- https://platform.claude.com/docs/en/build-with-claude/prompt-caching
- https://platform.claude.com/docs/en/about-claude/models/overview

Grounding (read by the helper):
- ALCE, https://ar5iv.labs.arxiv.org/html/2305.14627
- Wallat et al., https://arxiv.org/html/2412.18004
- Anthropic Citations, https://platform.claude.com/docs/en/build-with-claude/citations
- Zhou et al., https://ar5iv.labs.arxiv.org/html/2303.11315
- Reduce hallucinations, https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations
- System 2 Attention, https://ar5iv.labs.arxiv.org/html/2311.11829
- Shi et al., https://ar5iv.labs.arxiv.org/html/2302.00093
- Lost in the Middle, https://ar5iv.labs.arxiv.org/html/2307.03172
- Cuconasu et al., https://ar5iv.labs.arxiv.org/html/2401.14887
- Chroma "Context Rot", https://www.trychroma.com/research/context-rot
- TimeChara, https://arxiv.org/html/2405.18027v1
- RoleFact, https://arxiv.org/html/2406.17260
- RoleBreak, https://arxiv.org/html/2409.16727

## The fresh review (26 October, afternoon): sound with fixes

A fresh reviewer opened every source and the raw run of 25 October. Verdicts: the product survey and the API facts (prefill refused on Sonnet 5, Sonnet 5.5 and Haiku 5.5) supported; FAVA, EVER, CoVe and TimeChara only partly as the note read them (a general-model editor with evidence still scored worse; TimeChara's gain came from extra model calls judging each question, not a fixed line); "3 to 5 facts" is an extrapolation to test (3, 5 and 8), not a finding. Corrections that change the plan:

- **The failure path is about 1 s slower than the note's model:** in the raw run a redrafted first sentence passed at 4.86, 4.99 and 4.89 s, so with Pocket a failure for Sheila or Ron still lands at about 5.1 to 5.2 s. Re-scored with Pocket's 0.2 s voice, 5 of the 20 turns stay at 5 s or more (lines 4, 9, 11, 12, 17): three redrafts, two refused twice. Line 16 was a late voice start, not a check.
- **Thinking off for any rewrite call**, never "low effort" with a 60-token limit (thinking tokens count toward it).
- **Reuse first:** the reply prompt already chooses what bears on his line (ChooseFirst, on), tells the character to say only what it was told, carries the "could you know it?" rule, and the redraft is already told the refused details. Two switches exist, off and unmeasured: **NarrowRedraft** (the second try in one or two short sentences, the nearest thing to "rewrite only that sentence") and **PlanFirst** (the reply names 1 to 3 facts by number before speaking, a tighter set of facts). Measure them before writing new code.
- **False alarms are most failures** (40 to 45 of 132 clean turns flagged on the held-back bench): tighter facts cannot touch them, and a rewrite of a false alarm loses a true detail. The before and after must count, besides 5 s waits, invented details let through, "that's all I know" and fallback lines, and true details lost; and sort every slow turn by cause (redraft, refused twice, slow passing check, late voice).
- **Sizing:** 60 live turns cannot show a drop from 10 to 3; the slow-wait rate is better computed as each path's measured time times its rate, the rates taken from the bench (larger, no voice, cheaper per turn).

**The plan, revised:** (1) the "before": live turns on today's voices with each turn's steps kept (tools/voice-live/latency.py now records them), sorted by cause; the bench's first-sentence failure rate with today's settings; (2) NarrowRedraft and PlanFirst measured on the same bench; (3) only then new code: a repair of the failed sentence alone (thinking off, the refused details named), whose pass rate is benched offline before it is wired to speech; ending after the repaired sentence is the expected case; (4) the "after" the same way. The bench's cost against the $1 a day limit for measurement calls is to be sized before it runs.

## The "before", measured (26 October, 15:30)

30 live turns on today's voices (Sheila and Ron on Pocket, Darren on the card), the packaged game open in the street, the check on Haiku 5.5, each turn's steps kept (tools/voice-live/latency.py --live --early --pending --prewarm --checker claude-haiku-5-5 --lines 30; F:/LedgerTools/latency/before-slow-2026-10-26.json; about $0.4).

| Who | Turns | First sound heard, median | 5 s or more | First sentence refused |
|---|---|---|---|---|
| Sheila (Pocket) | 10 | 1.97 s | 3 | 1 |
| Ron (Pocket) | 10 | 1.92 s | 3 | 3 |
| Darren (card) | 10 | 4.39 s | 4 | 1 |
| All | 30 | 3.43 s | **10** | 5 |

The ten slow turns by cause:
- **The card voice (3, all Darren):** his first sentence passed its check at 1.7 to 2.4 s and was heard at 5.2 to 9.7 s. Pocket for him (his recast, on his page) is the fix; nothing in the check touches these.
- **Refused twice (4: Ron 3, Sheila 1):** the first sentence refused, the second draft's first sentence refused too, so the character fell back ("You've had the lot off me, friend.") at 6.4 to 8.3 s. This is the path the repair and NarrowRedraft act on.
- **A whole-reply check that found something (1, Sheila):** no early first sentence; draft, check, redraft, recheck, fallback at 7.8 s.
- **The 8-second limit (1, Sheila):** a brush-off ("Later. I'm in the middle of something.") after 8.3 s with the first sentence passed; the turn's own steps do not show where the time went (to be traced).
- **A redraft that passed (1, Darren):** 9.45 s, on the card voice.

So, of the 7 slow turns the speech check can change, 5 end in the fallback: the second draft failing again matters more than the first draft's time. The "after" is measured the same way.

## The bench, and why its 3.2 s is not the 2.41 s (26 October, evening)

**The bench.** ClaimBench `firsts --early` now runs a turn as the game does (the first sentence checked alone and handed over when it passes; the game's own switches: rules, plain fallback, the ladder and its judge, the model by the kind of moment, the check on Haiku 5.5), on LEDGER's key under its own $10 cap (`--task slow-replies-2026-10-26`; the counting wrapper now streams, without which every turn ran as a whole-reply check), and keeps each turn's steps. `tools/voice-live/slow_turns.py` scores a run: heard = the first sentence's hand-over plus 0.2 s of Pocket voice (all three speak through Pocket since Darren's recast). Raw: F:/LedgerTools/town-scratch/slow-replies (slow-turns-2026-10-26.json). Spent $4.86 of the $10.

**His question: 3.2 s against 22 October's 2.41 s.** Step by step, medians in seconds after the line is sent:

| Run (lines) | Who | Reply drafted | Check passed | Voice ready | Heard |
|---|---|---|---|---|---|
| Live, 22 Oct, Pocket (street small talk, 20) | Sheila / Ron / Darren | not recorded | 2.05 / 2.09 / 2.75 | 2.29 / 2.33 / 3.01 | 2.32 / 2.37 / 3.05 |
| Live, 26 Oct 15:30 (the same script, 30; Darren on the card) | Sheila / Ron / Darren | 0.68 / 0.67 / 0.71 | 1.82 / 1.88 / 2.10 | 1.93 / 1.88 / 4.36 | 1.97 / 1.92 / 4.39 |
| Bench on that script's own 12 lines (36) | Sheila / Ron / Darren | 0.46 / 0.49 / 0.49 | 0.50 / 1.50 / 1.50 | +0.2 | 1.55 / 1.91 / 1.79 |
| Bench, a newcomer's 20 real questions (60) | Sheila / Ron / Darren | 1.01 / 1.13 / 1.35 | 2.49 / 3.29 / 2.89 | +0.2 | 2.78 / 3.91 / 3.26 |

(Check passed: the turns whose first sentence passed, or needed no check; heard: every turn.)

- **The bench is not slower than the game:** on the live script's own lines it hears Sheila and Ron no later than the live run did (1.55 and 1.91 against 1.97 and 1.92), and Darren on Pocket at 1.79 against his card voice's 4.39.
- **The difference is the questions.** The live script is street small talk ("Evening. Anything going on round here?"), which the game gives the lighter model (Haiku 4.5; TalkMoment), and many of whose first sentences carry nothing to check ("Nothing much."). The bench's set is a newcomer's real questions about the place ("Who are you?", "How did Mickey die?"), which the game gives the better model (Sonnet 5): drafting takes 0.5 to 0.8 s longer, and their first sentences name people and places, so the check takes longer (median 1.4 to 1.7 s against about 1.0) and refuses more of them.
- **So both figures are true, for different talk:** about 2 s for small talk (22 October's 2.41 s with Pocket, about 2.1 s with the pending voice), about 3 s for a newcomer's real questions. Switches are judged only against the same lines on the same bench.

**The switches, two runs each where it mattered (60 turns a run):**

| Run | 5 s or more | First sentence refused | Refused twice | Heard, median |
|---|---|---|---|---|
| Today's settings | 17, 9 | 14, 7 | 7, 2 | 3.17, 3.03 |
| NarrowRedraft | 19, 13 | 8, 11 | 3, 5 | 3.30, 3.06 |
| PlanFirst | 23 | 6 | 3 | 4.21 |

- Two identical runs of today's settings gave 17 and 9 slow turns: the API's own pace and the model's choices vary that much, so one run proves nothing.
- **Every turn whose first sentence was refused was heard at 5 s or later** (36 of 36 across the four runs of today and NarrowRedraft). The refusal itself arrives at 2.9 to 4.5 s, because a refusing check writes out its whole list (1.9 to 3.1 s against about 1.5 for a pass); any second sentence and its check then land past 5 s.
- **NarrowRedraft:** no better (32 of 120 slow against 26 of 120). **PlanFirst:** fewer refusals, but planning first adds about 1.3 s to every turn; worse. Neither is switched on.
- **What follows for the repair:** rewriting only the refused sentence after the refusal saves only its writing time (0.5 to 3 s here) and still lands near 5 s. The repair pays only if it starts alongside the first check (a safe rewrite of the drafted sentence, used only if the check refuses), so that a refusal needs one more check, not a draft and a check. That is the next code, benched the same way before it reaches speech.

## Why Ron's check looked slowest (his question, 26 October evening)

His ruling the same evening: the 2-second bar is judged on a newcomer's real questions; small talk is reported beside it, never instead (RULINGS.md, speech). His question: Ron's check is the slowest on real questions (about 3.3 s to pass); why, for example the length of his known-facts list?

- **The 3.3 s was one run's time from the line to the check passing** (drafted 1.13 s, check alone 2.28 s, in the "today" run). Over all four runs of today's settings and NarrowRedraft, a passing first-sentence check took (median): Sheila 1.26 s, Ron 1.63 s, Darren 1.79 s. Ron is in the middle, not the slowest.
- **The facts list is the same size for all three:** 56 to 58 items, about 7,200 characters (about 4,250 tokens with the check's instructions). Across 187 passing checks, the check's time does not follow the list's length (correlation 0.08); it follows the sentence's length a little (0.27): Sheila's first sentences run to a median 3.5 words, Ron's 7, Darren's 8.
- **Measured one call at a time** (ClaimBench `checktime`: 10 passed first sentences per character from those runs, each checked twice on Haiku 5.5 with its own list and with the list cut to its first 15 items, order alternating; F:/LedgerTools/town-scratch/slow-replies/checktime; $0.02):

| Who | Whole list (about 57 items, 4,250 tokens in) | Cut to 15 items (2,150 tokens in) | Tokens written |
|---|---|---|---|
| Sheila | 1.05 s | 1.13 s | 43 / 40 |
| Ron | 1.11 s | 1.05 s | 44 / 55 |
| Darren | 1.07 s | 0.99 s | 43 / 44 |

- **So neither the list nor his sentences is why.** Alone, every check takes about 1.1 s (1.13 s plus 0.7 ms a token written; halving the list moves it under 0.1 s either way). The checks of 2 to 4 s in the runs are the service's own varying wait: they fell on all three, and on Ron's turns most in that one run. Tighter facts would therefore not speed the check; they matter only for how often it refuses. A check on this PC (the fast checker, whose numbers come tonight) is the one change that removes that wait for the sentences it is sure of.

## The refused sentence rewritten alone: two tries, set aside (26 October, evening)

Benched offline first, as planned (ClaimBench `repair`; F:/LedgerTools/town-scratch/slow-replies/repair; $0.15): 40 of Gemini's unsupported first sentences from the tuning contexts (the held contexts stay the fast checker's test), each through the game's own check on Haiku 5.5 (it refused all 40), then rewritten by Haiku 5.5 with thinking off, two ways (the refused details named, as after a refusal; nothing named, as a rewrite started alongside the check), and each rewrite checked again the same way.

| Try | Named: passed | Alongside: passed | Of those passing, an answer kept |
|---|---|---|---|
| 1. Keep the speaker's words and length, take the unsupported out | 6 of 40 | 6 of 40 | |
| 2. Only what one item says, nothing inferred, shorter is better | 12 of 40 | 17 of 40 | 4 of 12; 2 of 17 (the rest "I don't know") |

Each call took about 1.1 s to rewrite and 1.3 s to check again.

- **Try 1 fails:** the rewriter re-invents from who the speaker is ("since he's living in Mickey's flat over the office"; "trade's been thin since the docks went"), and the check rightly refuses it.
- **Try 2 fails differently:** what passes is nearly always a plain "don't know", the answer lost; today's second draft passed about 60% of refused turns in the runs above.
- **Set aside after two tries** (his rule). Wired alongside the check, it would turn a slow answer into a fast "don't know" about one time in three, which is not what he asked for.
- **The other direction, from the same data:** some refused rewrites look true to the speaker's card (Ron: "Two drivers on the rank, one by day and one by night"). This matches the September finding that false alarms are most of the check's refusals (40 to 45 of 132 clean turns flagged on the held-back bench). The lever for slow replies is therefore the check's false alarms: fewer of them, or the fast checker clearing the sentences it is sure of. Tonight's numbers bear on the second; the first gets its own research, from the refusals these runs kept.
