# Live talk: how others keep it fast and keep characters from inventing (28 October 2026)

The owner's order of 28 October (D12) asks what inZOI, Where Winds Meet, Ubisoft's AI teammates and NVIDIA ACE have
published about fast live talk (he quotes ACE's "under 0.8 s") and about keeping characters from inventing. It also asks
for one idea to be tested on the bench: a small fast model writes the first sentence while the larger model writes the
rest.

**How this was read.** The written questions came first (FAST-GROUNDED-TALK-QUESTIONS-2026-10-28.md beside this file). Sources were read on
28 October 2026 through a fetch tool that returns a model-written digest of each page, not its raw text. Question 5 was
researched in parallel by one helper under the same rules; the session re-read two of its papers' abstracts, which
matched. A fresh reviewer then checked the figures, code claims, Anthropic pages and the bench design; its fixes are
applied below. No paid model calls, no keys, nothing measured. **Unverified** marks what no primary source confirms.

## The finding that changes the order

**The idea was built and measured on 7 October, then switched off at the owner's word.**
- ConversationEngine.FirstModel has Haiku 4.5 write the first sentence (80 tokens at most). Sonnet 5 then writes the rest,
  told the words already said in a note on its system prompt (GoOnNote), since Sonnet 5 refuses an assistant prefill.
- Five replies each way on the real path, to Sheila (production/research/voice-off-card/CLOUD-VOICE-2026-10-07.md;
  DECISIONS, 7 October):

| | Sonnet alone | Haiku first |
|---|---|---|
| First sentence written (median) | 1.35 s | 0.75 s |
| Its check passed (median) | 2.96 s | 2.41 s |
| First sound (median) | 4.63 s | 3.99 s |
| Cost per reply | $0.026 | $0.032 |

- A fresh blind reader judged the openings about even. The whole replies were **worse in 4 of 5**: "padded with facts
  nobody asked for and running on, as Sonnet carried on from Haiku's sentence".
- His answer: "the faster first sentence stays off". The switch is still in the code, off; ClaimBench has no flag for it.

So the bench test below is **the idea's second try** under the two-tries rule. It differs from the first in three ways:
1. A different writer model.
2. A rewritten note to answer the padding fault.
3. The rest of the path is now fast enough that writing time is most of the wait.

## Our own figures (repository, read today)

| What | Figure | Source |
|---|---|---|
| First sentence written, small talk (Haiku 4.5) | 0.46–0.71 s median | SENTENCE-REPAIR-2026-10-26.md |
| First sentence written, a newcomer's real questions (Sonnet 5) | 1.01–1.35 s median | same |
| The whole check of a first sentence | 2.2–2.5 s median; one check call about 1.1 s | CHECK-TIME-2026-10-27.md |
| Two copies of each check call | saves a median 0.29 s | same |
| Fast local checker (17M) | 0.095 s; clears about half the first sentences | LOCAL-CHECKERS-2026-10-26.md |
| Shipped settings, 28 Oct | first sentence ready at a median **2.10 s** | same, last section |
| Cleared turns, 27 Oct (18 of 30) | written 1.36 s, ready 1.41 s (medians) | F:/LedgerTools/town-scratch/cited-fast/firsts.jsonl |
| Pocket voice after the sentence | about 0.2 s | POCKET-SWITCH-2026-10-26.md |
| Heard, newcomer's questions, game settings (26–27 Oct) | run medians 2.87–7.03 s | SENTENCE-REPAIR, CHECK-TIME |
| A newcomer's turn | about 8,000 tokens in, 120 out; logged $0.020 | production/playtest/talk-runs.jsonl |

**When the fast checker clears a sentence, the writing is nearly all of the wait.** On 7 October the slow check hid it.

**The game's Sonnet 5 replies send no thinking field, so Sonnet 5 thinks adaptively.**
- Anthropic's table: Sonnet 5, "Thinking without a `thinking` field: On".
- CAST-VOICE-2026-10-25.md: "no thinking field".
- FIRST-WORDS-2026-09-30.md recommended turning it off; that was never measured.

How much of Sonnet's 1.0–1.35 s is thinking is unknown. That is the cheapest lever, so the bench below measures it
beside the split.

## 1. inZOI (Krafton, NVIDIA ACE)

- **The model:** "a .5B billion parameter Mistral NeMo Minitron small language model", "on-device", "GPU-accelerated
  exclusively on GeForce RTX GPUs" (NVIDIA, 13 March 2025,
  https://www.nvidia.com/en-gb/geforce/news/nvidia-ace-naraka-bladepoint-inzoi-launch-this-month/).
  - No quantisation, speed or latency is published.
  - "About 1 GB of VRAM" is a fan wiki's figure: **unverified**.
- **What it decides:** actions ("assist a lost character with directions"), inner thoughts shown live, and at day's end
  "adjust their personal schedule". The player steers it with free text.
  - A second-hand account of Krafton's GDC 2025 talk adds daily diaries that plan the next day (GCORES, 23 March 2025,
    https://www.gcores.com/talks/1056614).
  - What it may not decide, or what the game checks, is **not published**.
  - No speech or voice parts are named. It is behaviour, not voiced conversation.
- **Krafton's one speed figure**, for its co-playable characters: "you will hear the responses within 1.5 seconds"
  (GamesBeat, 13 January 2025,
  https://gamesbeat.com/krafton-and-nvidia-team-up-to-create-smarter-ai-characters-for-pubg-and-inzoi/).
- **The same team's PUBG Ally** (NVIDIA Q&A, 25 June 2026,
  https://developer.nvidia.com/blog/how-krafton-built-pubg-ally-a-co-playable-character-powered-by-nvidia-ace/):
  - Minitron 2B, "further quantized", fits 8 GB cards beside the game.
  - A behaviour tree handles reflexes: "Reflex-level actions never have to wait for the model."
  - "tool results are the only ground truth", with "a fixed item taxonomy".
  - No timings are given.

## 2. Where Winds Meet (NetEase, Everstone)

- **NetEase has published no technical account** that English or Chinese searches found.
- **Its one official text** is the Steam disclosure, added on 12 December 2025: "AI-driven NPC text and voice chat that
  responds to player input in real time" (https://store.steampowered.com/app/3564740/; the date from
  https://arcanumrpgs.com/blog/where-winds-meet-ai/).
- **"Cannot create places, items or quests" is a guide writer's description, not NetEase's.**
  - The guide's words: "They can't create new items, spawn new locations, or rewrite quest lines that don't already
    exist". It says output is limited to text and to flags ("become Old Friend", "turn hostile", "give weekly gift").
  - No source is cited (Pallav Pathak, 22 November 2025,
    https://allthings.how/where-winds-meet-and-ai-how-the-mmos-chatbot-npcs-work/). **Unverified.**
- **What went wrong (press):** players finished chat quests by writing invented actions in brackets. The character judged
  from the player's own words whether the task was done (via Arcanum, 26 September 2026).
- **For LEDGER, already held:** the player's words are never evidence; the check never receives them.

## 3. Ubisoft: Teammates (Gemini) and NEO NPC

- **Teammates** (closed playtest, "a few hundred players"; Ubisoft News, 21 November 2025,
  https://news.ubisoft.com/en-us/article/3mWlITIuWuu0MoVuR6o8ps/ubisoft-reveals-teammates-an-ai-experiment-to-change-the-game):
  - The press, not Ubisoft News, names Google Gemini with in-house middleware.
  - Xavier Manzanares: "We use behavior trees ... and then we add a layer with our LLM". Also: "we control design-wise what
    they can say and do, but then it's up to the LLM to decide based on the context how it should be done" (Game
    Developer, 21 November 2025,
    https://www.gamedeveloper.com/business/ubisoft-s-first-playable-generative-ai-experience-is-an-r-d-experiment-called-teammates-).
  - Virginie Mosser: "fences that let NPCs improvise within the world but stay within the boundaries of the lore"
    (Ubisoft News).
  - **Latency:** Ubisoft published no figure. A hands-on report: "the latency was an issue throughout the demo". It says
    Gemini 3's launch added "often by an extra second or two", and describes a speech-to-text, model, voice stack running
    Gemini 2 on Google's servers. Ubisoft's leads named running on the player's PC as an aim (Tommy Thompson, AI and
    Games, 26 November 2025, https://www.aiandgames.com/p/ubisofts-teammates-demo-and-their).
- **NEO NPC** (GDC 2024; Inworld's model with Audio2Face; Ubisoft News, 19 March 2024,
  https://news.ubisoft.com/en-gb/article/5qXdxhshJBXoanFZApdG3L/how-ubisofts-new-generative-ai-prototype-changes-the-narrative-for-npcs):
  - A writer sets each character, held "through guardrail systems", with toxicity filters.
  - No latency figure and no mechanism for world facts.

## 4. NVIDIA ACE: the 0.8 s, and how it is reached

- **The 0.8 s is NVIDIA's Nemotron Voice Agent blueprint:** 0.79 s end to end on one stream, "with speculative speech
  processing enabled". It ran on three H100 data-centre cards, one each for recognition, model and voice, and reached
  1.0 s at 64 streams (NVIDIA FAQ, updated 9 June 2026, marked as partly AI-written,
  https://perspectives.nvidia.com/nemotron-speech/task/faq/which-speech-models-run-voice-assistants-500-milliseconds/).
- **The blueprint page's newer table:** 0.86–0.93 s on four B200 cards (updated 3 March 2026,
  https://build.nvidia.com/nvidia/nemotron-voice-agent.md).
  - Recognition and turn-taking: 0.47–0.49 s.
  - **The model's first token: 0.13–0.23 s.**
  - The voice's first byte: 0.07–0.10 s.
- **Advice page** (AI-written, no source for its savings):
  - "Target under 1 second from the end of user speech to the first synthesized audio".
  - Starting the voice on the first tokens saves 100–200 ms.
  - Updated 10 July 2026,
    https://perspectives.nvidia.com/nemotron-speech/task/faq/what-end-to-end-latency-should-i-target-for-a-conversational-voice-agent-to-feel/.
- **Speculative speech processing** works on stable interim transcripts. Voice made meanwhile is held until the user
  stops. NVIDIA: "approximately 300 ms reduction"
  (https://archive.docs.nvidia.com/ace/ace-controller-microservice/1.0/user-guide.html).
- **ACE for games** (https://developer.nvidia.com/ace-for-games; NVIDIA, 16 June 2026,
  https://developer.nvidia.com/blog/build-on-device-ai-companions-with-the-nvidia-ace-game-agent-sdk-and-unreal-engine-5-plugins/):
  - On-device 4B–9B models in Q4 files, and 350M voices.
  - Retrieval and function calls tie characters to game data. Total War: PHARAOH's advisor reads "1,200+ interlinked game
    data tables".
  - **No game latency figure** was found, and no page names guardrails as the defence against invention.
- **For LEDGER:**
  - The 0.8 s is a data-centre voice agent with spoken input, whose model begins in 0.13–0.23 s. Our cloud writer alone
    takes about 0.6–1.1 s to begin (FIRST-WORDS).
  - Speculative processing needs speech, and our player types. inZOI's route is RTX-only, and the PC has an AMD card.
  - **0.8 s is not reachable with a cloud writer and a check.** The 2 s bar stands.

## 5. Speed with grounding: what is published (helper's findings, links read today)

- **A fast opening, a strong continuation.**
  - RelayS2S (https://arxiv.org/html/2603.23346v2): a 5-word opening, voiced at once; the cascade continues it, told to
    "output only the continuation" and to repair slips. First chunk 748 to 269 ms with GPT-4.1 over the API. Stalls
    27.5% at 3 words, 1.9% at 5. Without its learned gate, poor replies rose from 10.9% to 14.3%.
  - DDTSR (https://arxiv.org/abs/2602.23266): the small model says only "minimal-committal discourse connectives"; waits
    19–51% shorter.
  - Micro language models (https://arxiv.org/abs/2604.19642): a 28M model writes the first 4–8 words; the cloud model is
    "a continuator rather than a respondent". Corrections were needed in 3.7% of replies at 4 words and 16.4% at 16.
    Listeners preferred a short natural bridge to an explicit correction.
  - **The published wins keep the fast part short and nearly free of facts.**
- **Speculative decoding** (https://arxiv.org/abs/2211.17192) gives identical output 2–3 times faster. It needs the
  model's probabilities inside the server, so an API user cannot run it, and it does not speed the first token.
- **Constrained decoding:** Anthropic's structured outputs compile a grammar
  (https://platform.claude.com/docs/en/build-with-claude/structured-outputs). They cannot restrict names inside a free
  sentence; LEDGER's hard name rule does that, at no cost.
- **Retrieval of what the character knows by then** gained 5–7.6 points of consistency
  (https://arxiv.org/html/2405.18027). LEDGER's time-tagged, cited facts already do this.
- **Anthropic, read today.**
  - **Prefill returns a 400 error** on claude-haiku-5-5 ("even with thinking turned off"), claude-sonnet-5 and
    claude-sonnet-5-5.
  - The documented substitute is a note: "Your previous response was interrupted and ended with [previous_response].
    Continue from where you left off"
    (https://platform.claude.com/docs/en/models/haiku-5-5/migration-guide;
    https://platform.claude.com/docs/en/models/sonnet-5-5/migration-guide).
  - claude-sonnet-5 accepts thinking "disabled". Haiku 5.5 is named the fastest
    (https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-latency).
  - Prices and retirement dates:
    - claude-haiku-5-5: $0.10/$0.50 a million tokens; not retired before 7 October 2027.
    - claude-sonnet-5: $2/$10.
    - claude-haiku-4-5: $1/$5, about 7.7 times Haiku 5.5's cost for the same text. **Its earliest retirement date,
      15 October 2026, has passed**, so it can be retired on 60 days' notice.
    - Sources: https://platform.claude.com/docs/en/about-claude/pricing;
      https://platform.claude.com/docs/en/about-claude/model-deprecations.

## Worth copying, and what LEDGER already holds

1. **The game decides; the model only words it.** PUBG Ally's "only ground truth", Teammates' "what they can say and do",
   and Where Winds Meet's failure. **Already held:** the Core decides, the check ignores the player's words, and replies
   cite their facts.
2. **Small models where big ones are not needed.** **Already held:** the 17M fast checker.
3. **Overlap every stage.** **Already held:** the voice is made beside the check.
4. **A short, nearly fact-free opening** has the largest published gains. It meets the 7 October ruling ("no prepared
   openings") and the reaction opener left off on 30 September. **Not copied without his word.**
5. **A faster first sentence:** the order's idea, worth its second try now that the check is fast for half the
   sentences. Beside it, the cheaper lever just found: **Sonnet 5 with thinking off.**

## Method

The session follows this for any change meant to make live talk faster without letting more invention through.

1. **Our stage table first.** Take medians and slowest tenths of writing, check, voice and heard on a newcomer's real
   questions (small talk beside). Read what each request actually sends: model, thinking, effort. Name the stage the
   change acts on and the most it could save.
2. **Search for an earlier try** in DECISIONS, the research library, the code's switches and his pages. Count the tries;
   no third.
3. **Primary sources on how others do it.** Mark data-centre against a player's PC, spoken against typed input,
   on-device against cloud.
4. **The bench design, written before any money.**
   - Arms, including a control that isolates the change.
   - Locked, rotating order.
   - The game's own switches.
   - Pass lines relative to the control.
   - The rule for incomplete sets.
   - Cost from logged tokens.
   - A fresh reviewer checks the design first.
5. **Run under ClaimBench's key-run cap.** One task line a day (measure-YYYY-MM-DD), at most $1 in all that day, every
   turn's steps kept.
6. **Score with fixed scripts.**
   - Quality judged blind by a fresh reader.
   - Invented details read blind to the arm, under the rule written below.
   - A fresh reviewer re-runs the scorer before any claim.
7. **Decide.**
   - Pass: a change to how characters talk goes on his page before it is switched on.
   - Fail: set aside as the try it was, and named in the summary.
   - Either way: RECIPE.md lines and a DECISIONS entry.

## First use: the bench test

**Question.** On a newcomer's real questions, does a small fast model writing the first sentence bring the first word
sooner? The larger model writes the rest. It must do so with no more inventions, no more wrong refusals, no clash between
the halves, and no worse replies.

**Arms.** ClaimBench `firsts --early` at the switches shipped on 28 October: cited facts, name rule, fast checker at the
open cut-off, two copies, ladder.
- **A, today:** `claude-sonnet-5` writes the whole reply on conversation moments, with no thinking field, as shipped.
- **A0, the control:** A with thinking `disabled`. It isolates thinking's share; if A0 alone is fast enough, it is the
  cheaper route.
- **B, the split:**
  - `claude-haiku-5-5`, thinking `disabled`, writes the first sentence: 80 tokens, the same system prompt, so it cites.
  - The moment that sentence is written, `claude-sonnet-5`, thinking `disabled`, writes the rest (at most 120 tokens)
    while the check and voice run.
  - A refused fast sentence stops the rest, and the redraft goes through the same split, as the code does. Refused twice,
    the ladder takes over.
- **Why Haiku 5.5, not 4.5.** Haiku 4.5's earliest retirement date has passed, and it costs about 7.7 times more.
  Anthropic names Haiku 5.5 the fastest. Its speed as a writer is what the bench measures.
- **The join (the second try's change)**, from RelayS2S, the micro language models paper and 7 October's fault:
  > YOUR REPLY HAS ALREADY BEGUN. You have just said, aloud: "…". Most replies end there. Add at most one short
  > sentence, and only if his question still needs a fact that sentence did not give; never add facts nobody asked for.
  > If what you said does not fit what you know, put it right in a few natural words. Never say those words again. If
  > nothing more is needed, write nothing.

**Bench code needed** (behind switches, with CoreTests):
- **New flags:**
  - `--first-model` and `--thinking-off` for `firsts`.
  - `--ab first`, rotating A, A0, B by question.
  - `--parallel 1`.
- **Guard:** the split for conversation moments only. Today it would also split small talk, which runs on Haiku 4.5.
- **Thinking off** on the fast request and on the rest.
- **Two faults found by the review:**
  - A fast sentence held back (a deflection, promise, real-world name or ending) reaches Sonnet as "said, aloud". Then
    Sonnet should write the whole reply instead.
  - A fast reply of one whole sentence never counts as written. Its stream's end should count.
- **Steps recorded per turn:**
  - the model begun and its first text, so thinking shows;
  - `first-fast`, and when the sentence is ready;
  - the check's outcome;
  - the rest's first words, and when the rest passes;
  - the words each model wrote.
- **A KeyTaskCaps line** for each day's task.

**Measured per turn:**
- heard: the hand-over plus 0.2 s of Pocket;
- turns at 5 s or more;
- first sentences refused, and refused twice;
- the gap from the end of the first sentence's audio (made afterwards by Pocket, free) to the rest passing;
- the rest empty, repeating, contradicting or correcting the first sentence;
- invented details heard;
- wrong refusals (refused first sentences read as true);
- the blind reader's choice of the better whole reply, and any padding.

**The hand-reading rule (fixed now).**
- A detail is invented when a sentence states as fact a person, place, time, day, number, object, vehicle or event that
  no numbered fact of the speaker states or directly implies.
- Idioms, opinions, questions and doubts are not details.
- The player's words never support anything.
- Sentences are shuffled with the arm hidden. A fresh reader reads the same set, and disagreements are settled by this
  text.

**Sample and order.** 14 of the newcomer's 20 questions (the file's first 14) to each of Sheila, Ron and Darren make
42 triples, 126 turns.
- Each triple runs back to back, with the order rotating (A, A0, B; then A0, B, A; then B, A, A0).
- At 42, a sign test needs one arm faster in 28 (two-sided p 0.044).
- An incomplete triple is dropped. The line is then the smallest count with two-sided p under 0.05 for those completed.

**Cost and cap.**
- From the logged tokens: about $0.020 a turn, so about $0.06 a triple and **about $2.50 in all**.
- **Within the $1 a day:** 14 triples a day for three days, each run `--cap 0.90`.
- **Or, with his yes:** all 60 triples in one evening, about $3.60.
- The readers use no key.
- Today's dollar is spent ($0.98 logged).

**Pass line.** B is judged against A0, the same thinking setting. All must hold:
1. **Speed:**
   - B heard sooner in at least 28 of 42 triples.
   - Median paired saving at least 0.3 s.
   - Turns at 5 s or more: B no more than A0.
2. **Inventions:**
   - First sentences refused: B no more than A0 + 2.
   - Invented details heard: B no more than A0.
3. **Wrong refusals:** B no more than A0 + 2.
4. **Join:**
   - Contradictions: at most 1.
   - Repeats: at most 2.
   - Median gap from the first sentence's audio end to the rest passing: B no more than A0 + 0.3 s.
5. **Quality:**
   - The reader prefers A0 over B in no more triples than B over A0, plus 4.
   - B padded in no more triples than A0, plus 2.

**A0 against A is scored by the same lines.** If A0 passes, Sonnet 5 with thinking off goes on his page as its own,
cheaper change, whatever B does.

**Pass for B:** his page, with numbers and three pairs to read. It changes D48 ("real conversation better") for the first
sentence, so the page names D48. **Fail on any line:** the faster first sentence is set aside after two tries, named
with the line that failed.

## Unverified and not reached

- **inZOI:** quantisation, speed, VRAM, what the game checks; Krafton's GDC slides (only a second-hand account).
- **Where Winds Meet:** every technical claim, "cannot create places, items or quests" included. GameApps.hk and This Week
  in Video Games answered 403.
- **Ubisoft:** no latency figure from Ubisoft; Gemini 2 against Gemini 3 unresolved; the NEO NPC release PDF was
  unreadable.
- **NVIDIA:** the blueprint's hardware differs between pages; how speculative processing discards work is not described.
- **The helper's paper numbers:** the session confirmed only the abstracts.
- **Anthropic:** Haiku 5.5's speed as a sentence writer is unpublished; the prefill page redirected.
