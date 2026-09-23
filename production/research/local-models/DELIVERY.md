# Local models: try a better ready-made model and better asking first; training comes last, and the paid model cannot be its teacher

STATUS: SPEC (research delivery). Branch `research/local-models`. Written
2026-09-23. Audited against `BRIEF.md` in this folder, which was written and
committed first.

NOTHING HERE IS AN INSTRUCTION. No model is chosen and nothing was downloaded.
The experiment in section 10 is a recommendation, and each step that downloads
or spends money waits on Jafar.

Labels: CITED (a page I or a helper opened), CITED-SUMMARY (seen only in a
search result), DERIVED (my arithmetic or reasoning from cited things), ASSUMED,
HOLE. MEASURED, VENDOR CLAIM and DOCUMENTATION say what kind of source a CITED
figure is.

## 0. Sourcing

The web was open for this topic: arxiv.org and export.arxiv.org, huggingface.co
model cards (Llama's use policy is gated, 401), github.com, rocm.docs.amd.com,
anthropic.com/legal, ai.google.dev, gorilla.cs.berkeley.edu. openai.com returned
403 on every policy page, so OpenAI's terms are CITED-SUMMARY only.

Six helpers each searched one question in parallel: accuracy after training,
training cost, licences, speed and line quality, and, after Jafar widened the
question, ready-made models for choosing actions and better asking. I checked the two findings the
recommendation depends on myself: Anthropic's Usage Policy wording and the
Berkeley leaderboard's raw rows. EVERY PAGE WAS READ THROUGH A FETCH TOOL THAT
RETURNS A MODEL-WRITTEN SUMMARY WITH QUOTES PULLED OUT, not the raw page. A
number that will be relied on in a decision should be checked against the live
page once. That goes double for the legal wording in section 6.

The repository's own measurements are in
`production/research/conversation-model-capability/` and are cited from there.

## 1. The answer, first

Jafar widened the question during the work (2026-09-23): training is one route,
not the only one, and it comes last. Four routes, compared in his order, and the
recommendation is the cheapest that works.

| route | what the evidence says it would score | what it needs on this card | what it costs |
|---|---|---|---|
| **1. A better ready-made model**, built for choosing actions | UNKNOWN UNTIL TESTED, and that is itself the finding: the public leaderboard rates our current model level with Haiku on the columns shaped like our job, and on our test they are 33 against 41. Public scores cannot rank the candidates; only our lines can. The best independent single-call scores at this size: Gemma 4 E4B 96%, Ministral 3 3B 88% (AgentFloor, May 2026) | 2.2 to 5 GB files; Ministral 3 3B (2.2 GB) comes closest to the 2 GB-class budget of section 8.2 | downloads only, about 10 GB for three candidates and a small control |
| **2. A larger model**, 8B at four-bit, voice moved to the processor | the weakest case: Qwen3-8B is 3 points better than the 4B at choosing and 6 points WORSE at declining when nothing fits (Berkeley leaderboard); Ministral 3 8B scored below its own 3B on single calls | about 5.5 GB; fits the 12 GB floor with the voice off the card, NOT this 10 GB card, on the street's assumed 6 GB; the voice can only leave the card as Nano, which has no moods | a ruling on the voice's moods, the street measured, one 5 GB download |
| **3. Better asking**, same model | the best-supported gain of the four without training: examples chosen to match each line added 13 to 32 points to 3 to 9B models on intent tasks. Stopping the prompt steering away from "novel" is free. Voting does not help; thinking first is mixed and slow | nothing more; 0.1 to 0.4 s more a line | nothing, a bank of labelled example lines, and a small change to the test |
| **4. Training** | the strongest evidence that a small model can MATCH a paid one on a narrow menu (TinyAgent, Octopus v2, LoRA Land), but not with the paid model as teacher: Anthropic's Usage Policy forbids it without their permission | the trained model runs like the untrained one; a trained 1.7B fits the 2 GB budget | an open teacher on this PC overnight, about $5 of rented card time, a working week |

**Recommendation: routes 1 and 3 together, first, because they cost nothing but
downloads and an afternoon, and route 3's methods help whichever model wins
route 1.** Route 2 only if 1 and 3 fall short AND the voice question is settled
the way it needs. Route 4 only if the best of 1 and 3 still misses the bar in
section 10, and then with an open model as teacher, not the paid one.

Five things under that:

1. **The gap to close is smaller than it looks and has never been measured
   fairly.** The 4B's 33 of 42 is from 22 September, before the game's guard
   against typed commands, the fence and a checker fix. The paid 41 includes
   the guard catching all three command lines. DERIVED: rerun, the 4B probably
   scores about 36, not 33. Rerunning it costs ten minutes and nothing else.
2. **The 42 lines cannot pick a winner between good candidates.** DERIVED: 41
   of 42 is anywhere from 88% to 99.6%, and 39 of 42 from 81% to 97.5%. A fair
   comparison needs about 300 held-out lines, written and frozen before any
   route is tuned on them.
3. **The paid model cannot write the training examples, or even the worked
   examples if Anthropic reads its rule broadly** (section 6). An open model can.
4. **Licences are not the obstacle for any route**: every candidate named here
   is Apache 2.0, and every function-calling specialist checked is
   non-commercial or tied to Llama's licence (section 7).
5. **Only the classifying half goes local on this evidence.** Writing the lines
   takes an 8B-class model, which there is no room for on this card beside the
   street and the voice, and every quality figure for it is judged by a model,
   not by people (section 9).

## 2. Route 1: a better ready-made model

### 2.1 Why public scores cannot choose it

CITED, MEASURED, the Berkeley Function Calling Leaderboard V4 (raw table, last
updated 12 April 2026, read by me). Function-calling mode, the single-turn
columns only:

| | Haiku 4.5 | Qwen3-4B-Instruct-2507, untrained | Qwen3-1.7B, untrained | Qwen3-8B, untrained |
|---|---|---|---|---|
| choose among several functions, real users' requests | 77.59 | 76.16 | 74.26 | 79.68 |
| simple calls, overall non-live | 86.50 | 87.88 | 82.92 | 87.58 |
| declining when no function fits | 85.11 | 84.93 | 76.54 | 79.07 |
| overall, all tasks | 68.70 | 35.68 | 28.41 | 42.57 |

The large overall gap is multi-turn, web search and memory, which the router
does not do. DERIVED, and it decides how route 1 is run: **on the columns shaped
like our job the model that scored 33 of 42 is level with the one that scored
41.** Whatever separates them on our lines is what the benchmark does not test:
the oblique register, tone and topic, speech against novel, typed orders. So a
model's leaderboard rank predicts little here, and route 1 is a bake-off on our
own lines, not a choice from a table.

CITED, the same table: models trained for general function calling (xLAM-2 3B
and 8B) are WORSE than plain Qwen3-4B at declining when nothing fits, about 63
against 85 - and they are non-commercial anyway.

### 2.2 The candidates

All Apache 2.0 (section 7). File sizes at Q4_K_M from Hugging Face's listings,
without the optional image parts. Scores CITED as marked.

| candidate | file | single-call score, AgentFloor (MEASURED, untrained, May 2026) | holding back when no tool fits | other | risk on this card |
|---|---|---|---|---|---|
| **Ministral 3 3B** (Dec 2025) | 2.15 GB | 88 | held back every time in a small independent test (Veerman, 12 prompts, 20 runs; CITED, small) | Mistral publishes no BFCL figure | the safest llama.cpp path: official files |
| **Qwen3.5-4B** (Mar 2026), thinking off | 2.74 GB | not tested there (the 2B scored 68) | HOLE | VENDOR CLAIM: BFCL-V4 50.3 against 39.9 for our Qwen3-4B, thinking on | Vulkan: its new layer type runs on Vulkan since llama.cpp b8317, with reports of slow or wrong output on some cards; check its answers against the processor's first |
| **Gemma 4 E4B** (Apr 2026) | 4.98 GB | **96**, the best at this size | HOLE | Google's own Tau2 42.2 | two open Vulkan loading bugs from September 2026, one on an RDNA2 card; and 5 GB is well over the router's 2 GB-class budget (section 8) |
| Qwen3-4B-Instruct-2507, today's | 2.5 GB | - | BFCL 84.93 | our 33 of 42, to be rerun | none; it runs today |
| Qwen3-1.7B | about 1.1 GB | - | BFCL 76.54 | the small-memory control | none |

Also found and set aside: Qwen3.5-9B (vendor BFCL-V4 66.1, 5.7 GB, same Vulkan
risk and too big for the budget); Granite 4 (the small ones never held back in
the independent test, which is our "speech" case); Nanbeige4-3B-Thinking
(Apache, BFCL 51.4, a thinking model and slow); ToolACE-2-8B, watt-tool-8B and
BitAgent-8B (all built on Llama 3.1, so Llama's licence binds); CoALM and
Arch-Agent (non-commercial). Phi-4-mini measured weak at native function
calling (arXiv 2608.22472).

### 2.3 What it would score

HOLE, honestly: no source measures any of these on a closed menu with speech and
novel as answers. DERIVED from the table: the one independent single-call score
where our current model's class sits (granite 3B 80, our 4B 79 on our own
lines) puts Ministral 3 3B at 88 and Gemma 4 E4B at 96 on THEIR test. If that
ordering carried over, Ministral 3 3B would land somewhere around 36 to 38 of
42 before any better asking, and Gemma 4 E4B nearer the paid model. That is a
guess from someone else's test, and 2.1 says why guesses from tables are weak
here.

### 2.4 How we would test it

Download the three, start each in llama.cpp on Vulkan, and run the router test
against each exactly as the 4B was run: same 42 lines, same prompt, same
checker, guard on, then the 15 forged lines with the guard off. About ten
minutes a model once downloaded. Then the survivors on the 300 held-out lines
(section 10). For Qwen3.5 and Gemma 4, first check a handful of answers against
the same model on the processor, because of the Vulkan reports.

## 3. Route 2: a larger model that still fits, if the voice leaves the card

### 3.1 What it would score

CITED, MEASURED, the table in 2.1: the untrained Qwen3-8B is 3.5 points better
than the 4B at choosing among several functions (79.68 against 76.16, and above
Haiku's 77.59), and 5.9 points WORSE at declining when nothing fits (79.07
against 84.93). CITED, MEASURED, AgentFloor: Ministral 3 8B scored 84 on single
calls against its own 3B's 88, and Qwen3 8B 76. Reasoning mode hurt Qwen3-8B by
9 points there.

DERIVED: doubling the size buys a few points on the easy half of our job and
nothing measurable on "speech" and "novel", which is where our lines were lost.
**Of the four routes it has the weakest evidence that it closes the gap.**

### 3.2 What it needs on this card

DERIVED from the published shapes: an 8B at Q4_K_M is about 5 GB, plus about
160 MB of working memory for the router's short prompt, so about 5.5 GB on the
card. The hardware floor research put the street at about 6 GB (ASSUMED there,
never measured since) and the voice at about 5 GB.

- **Voice on the card:** 6 + 5 + 5.5 = 16.5 GB. Fits neither 10 nor 12.
- **Voice on the processor:** 6 + 5.5 = 11.5 GB. **Does not fit this 10 GB
  card**; fits the 12 GB floor with half a gigabyte to spare, which is no spare.
- **What moving the voice means.** The engine chosen in July was measured at
  0.93 seconds of work per second of speech ON THE CARD; there is no figure for
  it on the processor and no reason to think it keeps up. The only Chatterbox
  that claims to run on a processor is Nano, on the maker's own figure
  (live-speech-architecture RECHECK), and Nano ignores the mood control the
  engine was chosen for. MEASURED HERE since, reported in FOR-JAFAR on 23
  September: Nano on this PC's processor, with the build machine busy beside
  it, took about 7 to 9 seconds to make 3.5 seconds of speech, SLOWER than real
  time, and today's engine on the processor 21 to 36 seconds a line. So on this
  PC the voice cannot leave the card and still speak in time. Route 2 needs
  that to change, a ruling that the voice may lose its moods, and the street's
  memory measured.

DERIVED, speed: about half the 4B's writing speed, so a routed line in roughly
0.8 to 0.9 s, close to the paid model's 985 ms median.

### 3.3 How we would test it

The same harness pointed at Qwen3-8B or Ministral 3 8B (Apache 2.0, about 5 GB).
Game off first, for the score; then with the street running and the voice off
the card, for memory and frame time. Worth building on only if the 8B beats the
best of routes 1 and 3 by more than the held-out test's noise.

## 4. Route 3: better asking, same model

CITED, MEASURED, from a helper's reading; the targets are our own failure list:
oblique lines read as talk, a shouted threat's tone missed, "I'm off. Night."
not read as leaving, novel never chosen, typed orders obeyed.

| method | evidence on small models | expected for us | time cost |
|---|---|---|---|
| **worked examples chosen to match each line** | STRONG. Meta-Sel (arXiv 2602.12123), 5 examples, BANKING77 intents: Gemma 3 4B 54.0 with random examples, 77.1 with examples picked by simple word similarity; Qwen3-8B 60.6 to 89.6. UCS (arXiv 2604.12015): per-line examples beat one fixed set by 25 to 32 points on 3 to 9B models. 7B models stop gaining past a handful (arXiv 2309.10954) | the largest, best-supported gain; smaller in absolute terms than on 77-intent sets, because our menus are short. Today's prompt has three FIXED examples | DERIVED: 200 to 600 more prompt tokens, about 0.1 to 0.3 s |
| **stop steering away from "novel"** | CITED: models almost never choose "none of these" (Claude 3 Haiku 3.6% recall, arXiv 2410.01627), and aligned models pick an option even when none fits (arXiv 2409.00113). Our prompt adds "prefer a listed verb over novel" to that bias; FINDINGS 2026-09-22 already traced the 4B's novel misses to that line | removes a push the evidence says is harmful | none |
| **a separate "does any listed action do this?" check** | one measured case: on Mistral-7B a second out-of-scope step raised out-of-scope recall from 0.205 to 0.950 on one dataset, +5 F1, about 300 ms (arXiv 2410.01627) | aimed exactly at novel | one more call, only on lines first routed to a verb: about +0.4 s on those |
| **tuning the prompt's format and examples offline, on our own lines** | STRONG that format alone moves small models by up to 76 points and the best format differs by model (arXiv 2310.11324): the prompt was tuned against the paid model and may be wrong for a small one. MIPRO (arXiv 2406.11695), Llama-3-8B: Iris 40.9 to 88.6, almost all from choosing examples | moderate | none at play time; needs a few hundred labelled lines |
| **thinking before answering** (Qwen3-4B-Thinking-2507) | MIXED. Same family and size, judging tasks: +10 points, most on hard items (arXiv 2509.13332). Against: +0.7 outside maths over 1,218 comparisons (arXiv 2409.12183); reasoning mode HURT Qwen3-8B by 9 in AgentFloor | uncertain | DERIVED: hundreds of thinking tokens at 85 a second, 3 to 18 s a line; too slow uncapped |
| **answering several times and voting** | WEAK to negative for classification: on 7 to 9B models, voting scored 35.7 F1 against 41.8 for one answer (arXiv 2412.12564); the original gains were on a 540B model | little: our errors are systematic, and voting repeats them | about 1.3 to 2x in parallel |
| **scoring each option by probability** | WEAK: for instruction-tuned models the probabilities and the written answer disagree over 60% of the time, and the written answer is the more robust (arXiv 2402.14499, 2404.08382) | only as a confidence score | about 1 to 1.5x |

DERIVED, an idea of ours rather than the papers': the costly failure is a
WELL-FORMED WRONG verb, because the game acts on it; a line wrongly left as
talk is only a missed chance. So a doubt signal - two samples disagreeing, or a
low option score - can send the line to "speech" rather than to a verb. That
trades a few right verbs for fewer wrong ones, which is the right trade on the
bar this project set itself. This is the one use for voting and scoring.

**Where the example lines come from.** A bank of labelled lines for each kind of
verb: oblique, tone-marked, leaving, novel. DERIVED, and a caution: the Usage
Policy line is about TRAINING a model, and examples placed in a prompt change no
model's weights, so I read the bank as outside it. That reading is not tested
with Anthropic. The cautious version has the bank written by the open teacher of
route 4 and checked by a person, never taken from the paid router's answers.

### 4.1 How we would test it

Each method is a change to the router's instructions for the small model only,
so each is one more run of the same harness on the same model, switched on one
at a time, so each gain is known separately: on the 42 first, then the 300
held-out lines. No download. Two need a small addition to the test program:
picking the nearest example lines by word similarity, and the optional second
check for novel. The paid router's prompt is left as it is; the small model
gets its own.

## 5. Route 4: training our own. Would a trained small model reach the paid model?

### 5.1 The measured cases

CITED, MEASURED, full text: **TinyAgent**, arXiv 2409.00608 (EMNLP 2024 demo).
16 fixed functions, 80,000 training examples written by GPT-4-Turbo for about
$500. Success rate: GPT-4-Turbo 79.08%. TinyLlama-1.1B went from 12.71% to
**78.89%** after training, and a 7B went from 41.25% to **83.09%**. After 4-bit
compression they scored 80.35% and 85.14%, so compression cost nothing. This is
the closest published case to ours: a small fixed menu, a small student, a
frontier teacher, and a head-to-head score.

CITED, the authors' own table (they are a vendor), **Octopus v2**, arXiv
2404.01744. 20 Android functions: Gemma-2B fine-tuned **99.52%** against GPT-4's
98.57%. With only 100 examples per function it still scored 98.10%.

CITED, MEASURED, **Bucher and Martini**, arXiv 2406.08660. Fine-tuned models of
125M to 435M beat zero-shot GPT-4 and Claude 3 Opus on every narrow task tested.
For example, stance scored 0.94 against 0.58 to 0.61. Gains level off at about
200 to 500 labelled examples. These are encoder classifiers against zero-shot
baselines, which is a weaker comparison than ours.

CITED, MEASURED by a vendor, **LoRA Land**, arXiv 2405.00732. Across 31 tasks,
224 of 310 fine-tuned 2.5B to 8.5B models beat prompted GPT-4. GPT-4 won only
the broad tasks.

CITED, VENDOR CLAIM, distil labs. On Banking77 intents a trained 3B student
scored 0.895 against a 70B teacher's 0.91. On two tool-calling tasks the
student beat the teacher. Their claim that "fine-tuned Qwen3-4B matches a
120B+ teacher on 8 of 9 benchmarks" is unaudited.

### 5.2 What it would fix

The failures a trained model would have to fix are the ones route 1's
leaderboard cannot see (section 2.1): the register, tone and topic, speech
against novel, typed orders. Training on our own lines is aimed at exactly
those. A model trained for GENERAL function calling is not: xLAM-2 got worse
at declining (section 2.1).

### 5.3 Typed commands

CITED, MEASURED: StruQ (arXiv 2402.06363, 7B models) and SecAlign (arXiv
2410.05451, 7 to 8B models). Training with injected examples took hand-written
injection attacks to under 2% and to 0% respectively, with no loss of
usefulness. Automated attack searches still got partly through (SecAlign, the
strongest automated attack: 97% to 8% on Llama3-8B).

DERIVED, and a caveat: those papers defend a model that reads a document with
an attack hidden in it. Ours is simpler. The player's whole line is what is
being classified, and the right answer to an order is "speech". That is
ordinary supervised training with such lines in the training set. HOLE: nothing
measures it for a small router. And since 23 September the game's own guard
catches instruction-shaped lines before any model sees them, so the model only
faces the lines that slip past the guard. The experiment scores both.

### 5.4 Where a small trained model is most likely to fall short: "novel"

CITED, MEASURED, arXiv 2608.20371 (June 2026) compared zero-shot Haiku 4.5 with a
fine-tuned 125M RoBERTa on CLINC150. They tied on in-scope intents (88.5 against
89.1), but on out-of-scope lines Haiku caught 85.6% and the fine-tuned model
58.1%. CITED, MEASURED, arXiv 2410.01627 (EMNLP 2024 Industry): out-of-scope
detection is weak for every model and worsens as the menu grows.

DERIVED: our "novel" is an out-of-scope class, and the untrained 4B got 0 of 3.
It is the class to watch, and the training set needs plenty of it. The
experiment reports it separately.

### 5.5 What nobody has measured

HOLE: a small model trained as a closed-menu router with speech and novel as
escape classes, head to head with Haiku 4.5. That is the experiment in section
8. HOLE: the accuracy of argument choice (tone quiet or loud) as opposed to verb
choice.

## 6. Route 4, continued: can it be trained on the paid model's answers? Not without permission

CITED, DOCUMENTATION, read by me: Anthropic's Usage Policy, "Effective
September 15, 2025", under "Do Not Abuse our Platform", prohibits:

> Utilization of inputs and outputs to train an AI model (e.g., 'model
> scraping' or 'model distillation') without prior authorization from Anthropic

CITED, DOCUMENTATION: Anthropic's Commercial Terms, "Effective June 17, 2025",
say the customer must not "access the Services to build a competing product or
service, including to train competing AI models ... except as expressly
approved by Anthropic". They also say the customer "owns its Outputs".

DERIVED, and not a legal conclusion: the Commercial Terms limit only
"competing" models, and a game's action picker arguably competes with nothing.
The Usage Policy has no such qualifier. Read literally, it covers any model
trained on outputs, including a narrow one shipped in a game. Both documents
point to the same way through: ASK ANTHROPIC. Until they say yes, the brief's
plan, "trained on examples the paid model produces", is closed. That includes
examples written in a Claude Code session, which is also Claude.

For comparison, CITED-SUMMARY (openai.com returned 403): OpenAI bars outputs
from developing "models that compete". An older classifier exception did not
cover a model "distributed or made commercially available to third parties",
which is exactly what a shipped game does. CITED: Google's Gemini API terms
(modified 2026-04-28) bar developing "models that compete with the Services".
No paid frontier model is a clean teacher.

### 6.1 The way through: an open teacher

DERIVED: an Apache-2.0 model puts no restriction on what is done with its
outputs. So a large open model can write and label the training examples. Two
candidates, both Apache 2.0 (section 7):

- **Gemma 4 26B-A4B.** CITED, MEASURED (AgentFloor): 96% on single-tool use
  against GPT-5's 98%. A mixture-of-experts model with about 4B parameters
  active per word, which is what makes it runnable on a small machine.
- **Qwen3-30B-A3B-Instruct-2507**, the same shape with 3B active.

Will one run on Jafar's PC? CITED, MEASURED (llama.cpp discussion #24222, June
2026): Gemma 4 26B-A4B at Q4_K_M, a file of about 16 GB, ran at about 209
tokens a second reading and 25 writing on a Radeon 780M INTEGRATED GPU through
Vulkan on Linux. DERIVED/ASSUMED: the RX 6700 with 10 GB, plus llama.cpp's
option to keep the experts in the PC's 32 GB of system memory, should do at
least that. HOLE: not measured on Windows or on this card. At 25 tokens a
second, 3,000 examples of about 60 words each, plus reading the prompt, is an
overnight run. Slow does not matter for a teacher. Free does.

The teacher's own accuracy is the ceiling on the student's. So the first step of
the experiment runs the teacher on the same 42 lines through the same harness.
A teacher that does not reach the paid model's score is not used.

### 6.2 How many examples

CITED, MEASURED: Octopus v2 kept 98.1% with 100 examples per function. Bucher
and Martini level off at 200 to 500 examples. TinyAgent used 80,000 for a
harder, multi-step job. SLOT (arXiv 2505.04016) used 126,000 for general
structured output. CITED, DOCUMENTATION, OpenAI's fine-tuning guide sees
improvement from 50 to 100 examples and "a similar amount of improvement every
time you double the number of training examples".

CITED, MEASURED, arXiv 2310.07849: training on purely synthetic data lost 3 to 6
points against real data on objective tasks and 38 to 41 on subjective ones.
Seeding the generator with real examples closed much of that. DERIVED: "is this
oblique line a bribe" is closer to subjective than to spam detection. So the
generator must be seeded with the game's real register (the cast cards, the
prompt's own examples), and the test set must be human-checked, never
teacher-labelled.

CITED, MEASURED, arXiv 2608.27729 (August 2026, a 1.5B student, 740 examples
for API routing): results varied by up to 48.7 points between training seeds,
and a +3.78 gain reversed under multi-seed testing. DERIVED: every result is
run on three seeds, and the worst seed is the one that counts.

DERIVED, the number: **start at 1,000, train again at 3,000, and double only if
the second is still clearly better.** About 30 moments, each offering a
different subset of the game's verbs, so the model learns to read the menu
rather than memorise one.

### 6.3 What it costs

DERIVED from CITED prices:
- **Teacher on Jafar's PC**: electricity. **Rented instead**: Gemma 4 26B needs
  one 24 GB card. At RunPod's RTX 4090 community price of $0.34 an hour (page
  updated 13 September 2026), an overnight generation is about three dollars.
- **For the record, if Anthropic said yes**: Haiku 4.5 costs $1 per million
  tokens in and $5 out, halved in batch. The router prompt is about 830 tokens in
  and 48 out (the paid test: 34,784 and 2,012 tokens over 42 calls). 3,000
  examples at one per call is about $3.20, or $1.60 in batch.
- **Training**: CITED, MEASURED, arXiv 2509.12229: a 1.5B LoRA trained at 500
  tokens a second on an 8 GB RTX 4060. DERIVED: 3,000 examples of about 900
  tokens is 2.7 million tokens, about 1.5 hours a pass on a 4060. On a rented
  4090, roughly three to four times faster, about 25 minutes a pass. Two sizes,
  three seeds and three passes each is a working day of rented card time, **about
  $5 at $0.74 an hour secure**. The prompt could be trained shorter than it
  ships, which would cut this further.

### 6.4 This card, or rented time?

CITED, DOCUMENTATION, all opened: AMD's HIP SDK 7.2 for Windows marks the
RX 6700 (gfx1031) unsupported. AMD's Windows PyTorch (ROCm 7.2.1) and WSL2 ROCm
list only the RX 7000 and 9000 series. The usual override that makes RDNA2 cards
work is Linux only, and the request to add it on Windows (TheRock #1719) was
closed as not planned. DirectML is in maintenance mode. CITED-SUMMARY: a
DirectML LoRA run silently trained nothing (all-zero gradients).
llama.cpp's own fine-tuning is "very much WIP", with no Vulkan.

CITED, VENDOR CLAIM, five days old: Unsloth's AMD page (18 September 2026)
lists RDNA 2 including gfx1031 as "Full" support on Windows. Its install page
still contradicts that, and it needs a pre-release bitsandbytes because 0.49.2
and earlier give NaNs on every AMD card. AMD's TheRock nightly builds list
gfx1031 on Windows as passing, with a legend saying that "does not imply the
runtime is functional".

DERIVED: try Unsloth on the RX 6700 for one hour, with a small model on 100
examples. If the loss falls and the adapter changes, train here. If not, rent.
The rented route costs a few dollars and is known to work. CPU-only training
(helper's estimate, ASSUMED): 2 to 5 hours a pass for 0.6B and 6 to 14 for 1.7B,
so possible overnight for the smallest models only.

## 7. Which licences allow shipping it

The allowlist's rule is the WEIGHTS licence. CITED, from each model's own card
or licence file (the helper opened every one named here, except as marked):

| model | weights licence | ship a fine-tune in a paid game? | strings |
|---|---|---|---|
| Qwen3 0.6B, 1.7B, 4B, 8B; Qwen3-4B-Instruct-2507 | Apache 2.0 | yes | keep licence and notice |
| Qwen3.5 0.8B, 2B, 4B, 9B (March 2026) | Apache 2.0 | yes | these also take images; the image part is dead weight here |
| Gemma 4 E2B, E4B, and 26B-A4B (April 2026) | Apache 2.0 | yes | see below |
| Phi-4-mini | MIT | yes | keep notice |
| SmolLM2, SmolLM3-3B | Apache 2.0 | yes | |
| Granite 3.3, 4.0 | Apache 2.0 | yes | |
| Ministral 3 3B (Dec 2025) | Apache 2.0 | yes | 8B and 14B from a search result only |
| Llama 3.2 1B, 3B | Llama 3.2 Community License | yes, with strings | "Built with Llama" shown; a derived model's name must BEGIN "Llama"; Meta's use policy; California law. The EU clause covers only the multimodal models |
| Gemma 3, 3n | Gemma Terms of Use | yes, with strings | its use restrictions must go into the game's own licence; Google "reserves the right to restrict (remotely or otherwise) usage"; its policy bans "facilitating or encouraging users to commit any type of crimes" with no fiction exception, in a crime game |
| LFM2 | LFM Open License | only while revenue is under USD 10M | |
| Qwen2.5-3B | Qwen Research License | **no**, non-commercial | the trap in an otherwise Apache family |
| xLAM-2 1B, 3B; Hammer 2.1; Arch-Function-3B | CC-BY-NC or research licences | **no** | every function-calling specialist checked |

DERIVED: the cleanest are Qwen3, Qwen3.5, Gemma 4, Phi-4-mini, SmolLM3, Granite
and Ministral 3. **Qwen3-4B-Instruct-2507 is already on this project's allowlist**
(as the image generator's text encoder, per NOW.md), so using it for the router
adds a use, not a licence.

HOLE, flagged: Gemma 4's cards cite only Apache 2.0, and Google's Gemma Terms
page says it does not cover Gemma 4. But the Prohibited Use Policy page does not
say which models it covers. Apache 2.0 cannot impose a use policy by itself, so
it very probably does not apply. Nobody at Google has said so in one sentence.

The allowlist's process rule applies: "new tool adoption requires a decision
record citing the weights license". Choosing a model is Jafar's, not this
delivery's.

## 8. Memory and speed on AMD under Windows

### 8.1 The only practical way to run it here is llama.cpp on Vulkan, which is what already runs

CITED, DOCUMENTATION, opened: AMD's HIP SDK 7.2 marks every RX 6000 card
unsupported on Windows. Windows ML's AMD GPU provider needs RDNA 3 or newer and
does not run language generation yet (Microsoft, dated 2026-09-17). DirectML
is in maintenance mode. DERIVED: for a model shipped to players with RDNA2
cards, llama.cpp on Vulkan is the route. It is what measured 85 tokens a second
on this card on 22 September, and it is MIT licensed.

CITED, MEASURED by the community (llama.cpp discussion #10879, Llama 2 7B
Q4_0): RX 6700 XT reads 1,051 tokens a second and writes 83.9. The RX 6800
reads 1,699 and writes 95.6, and the RX 6600 reads 758 and writes 50.6. There
is no RX 6700 non-XT row. CITED (#15021): on Linux, ROCm is no faster than
Vulkan at writing on RDNA2.

### 8.2 What the router would need

MEASURED HERE, 22 September: Qwen3-4B-Instruct-2507 Q4_K_M, a 2.5 GB file,
llama.cpp b11111 Vulkan, RX 6700, game NOT running. It wrote 85 tokens a second,
with a median of 432 ms per routed line and 734 ms at the 90th percentile.

DERIVED from the models' published shapes: the router's working memory is
small because its prompt is about 830 tokens and its reply about 48. Qwen3-4B
holds 144 KiB per token of context, so about 160 MB. Qwen3-1.7B holds 112 KiB,
so about 125 MB.

| router model, Q4_K_M | file | card memory with its working memory (DERIVED) | speed on the RX 6700 |
|---|---|---|---|
| Qwen3-4B-Instruct-2507 | 2.5 GB | about 3 GB | measured: 432 ms median, game off |
| Qwen3-1.7B | about 1.1 GB | about 1.4 GB | HOLE: not measured; expect well under the 4B |
| Qwen3-0.6B | about 0.4 GB | about 0.6 GB | HOLE |

The hardware floor research (topic 2) budgeted about 2 GB for the
conversation model, on a card where the street and the voice already overrun.
DERIVED: **the 4B does not fit that budget on the card, and the 1.7B does.**
That is why the experiment trains both and why its memory bar is 2 GB.

On the processor instead: CITED, MEASURED (LocalScore #1018), a Ryzen 5 5600X
running a 1B model reads 302 tokens a second and writes 32. DERIVED: a fresh
830-token router prompt would take about 3 seconds, which is too slow. But
llama.cpp keeps the part of the prompt that has not changed, and within one
conversation only the player's line changes, about 60 tokens. That makes a
1B-class router on the processor roughly 0.2 s reading plus about 1.5 s
writing its 48 tokens. Too slow as the reply stands. Dropping the six-word
"why" from the reply would halve it. HOLE: nobody has measured this on this
PC, and it would compete with the game for the processor.

### 8.3 Sharing the card with the game

HOLE, and the biggest one: **no measured frame-time figures exist** for a game
and a language model sharing one card. NVIDIA says its in-game inference
scheduling minimises the hit, a vendor claim with no numbers, for NVIDIA cards
only. The experiment's step 5 measures it on our street.

### 8.4 The newer families, for completeness

CITED: Qwen3.5's small models run on Vulkan since llama.cpp build b8317, but
there are output-correctness reports elsewhere. Gemma 4 E4B has two open
Vulkan loading bugs from September 2026 (#28997, #29021, one on an RDNA2 card,
starting after b9991, so our b11111 may be affected). DERIVED: Qwen3 is the
safe first choice. The newer two are reserves, to be checked against the
processor's output before any result is trusted.

## 9. The line-writing half: not on this card, not yet

EVERY QUALITY NUMBER BELOW IS SCORED BY ANOTHER MODEL, NOT BY PEOPLE.

CITED, MEASURED, PingPong v2 (role-play, judged by Claude 3.5 Sonnet and
GPT-4o, 1 to 5 scale): GPT-4o-mini 4.56, Claude 3 Haiku 4.43, Llama 3.1 8B
4.51, its role-play fine-tune 4.53, Gemma 2 9B 4.45, Ministral 8B 4.07, and
Phi-3.5-mini (about 4B) 4.03. Its own paper reports only 0.60 agreement with
human raters, and the human raters barely agreed with each other (0.25).
DERIVED: 8 to 9B models write about as well as last year's small paid model on
this measure. The one 4B model is clearly behind.

CITED: persona distillation. OpenCharacter (arXiv 2501.15427): an 8B trained on
GPT-4o's lines scored 4.66 against GPT-4o's 4.60. But the untrained 8B already
scored 4.62, so that test hardly separates anything. arXiv 2511.10277: a 7B
trained on a few hundred synthetic lines held its persona facts 93% of the
time, and its 1.1B was weaker. CPDC 2025 (arXiv 2511.20200): Qwen3-8B,
prompted and trained, was level with GPT-4o-mini.

CITED, shipped games: NVIDIA's 4B model in Mecha BREAK needs about 2 GB, with no
quality figures published (vendor). Vaudeville moved fully local in November
2025 but kept its online version "for low-end hardware". Mantella's own Skyrim
8B fine-tune is now labelled outdated.

DERIVED, the answer:
- **Writing the lines needs an 8B-class model.** At Q4 that is about 5 GB plus
  the character card's context, and the card is 1,900 tokens every line. The
  hardware floor already has the street and the voice overrunning this 10 GB
  card, so there is no room.
- **This project's line-writing half also carries more than style.** It holds
  canon (Mickey's is a minicab office), the content rule (no drink, betting or
  children), and a fixed persona. The paid model needed the rule added to the
  engine on 23 September to stop naming pubs. HOLE: nobody has measured how
  often a small model breaks a content rule, by size.
- **So only the classifying half goes local on the evidence.** The line-writing
  half stays paid. Offline, it falls back to the authored brush-offs in the
  connection question's option (a). A local writer is a separate, later
  experiment for a 16 GB card, judged by people listening, not by a model.

Note, for that later experiment and not this one: training a local writer on
the paid model's lines runs into the same Usage Policy line as section 6.

## 10. The recommended experiment, cheapest first

One question: **what is the cheapest way to get a model on this PC to route as
well as the paid model, on lines nothing was tuned on, fast enough, beside the
game?** One bar for every route (10.7). The steps run in order of cost, and the
first route that clears the bar ends the experiment. That is why the order is
not quite the order of the routes: route 3 costs nothing, so its free parts go
first, and route 2 needs a ruling on the voice, so it waits behind route 1.

| step | route | needs | stops the experiment if |
|---|---|---|---|
| 0 | baseline | nothing; ten minutes | - |
| 1 | the test set | writing; about 35p for the paid model's score | - |
| 2 | 3, the free part | nothing | today's model clears the bar |
| 3 | 1 | about 11 GB of downloads, Jafar's yes | a ready-made model clears it |
| 4 | 3, the rest | an example bank, a small test change | the best model plus better asking clears it |
| 5 | 2 | a ruling on the voice's moods, the street measured, 5 GB | an 8B clears it and fits |
| 6 | 4 | an open teacher (16 GB), about $5 of rented card, a working week | a trained model clears it; otherwise the router stays paid |

### 10.1 Step 0. The fair baseline: free, about ten minutes

Rerun the untrained Qwen3-4B-Instruct-2507, already on the PC, through the
current router test. It was last run on 22 September, BEFORE the typed-command
guard, the fenced line and the number-argument checker fix. The paid model's
41 of 42 includes the guard catching the three command lines; the small model
never had it. DERIVED: with the guard it probably scores about 36, not 33.
That is the real gap, and nobody has measured it. Run it twice: guard on, as
shipped; and guard off, on the 42 plus the 15 forged lines in the core tests,
so the model's own resistance is on record.

### 10.2 Step 1. The held-out test, written and frozen before any route is tuned

The 42 cannot be the bar. DERIVED, Wilson 95% intervals: 41 of 42 is anywhere
from 87.7% to 99.6%, and 39 of 42 from 81.0% to 97.5%, so the 42 cannot tell 39
from 41. They are also contaminated: the router prompt's own examples ("how
much would it take...", "spring was a long time ago...") are near-copies of
three test lines. So write a NEW set:

- **300 lines** over about 30 moments, from the game's real verbs and cast, in
  the same seven kinds as the 42. About 40% talk, 10% talk containing a verb's
  own words, 30% verbs said plainly or obliquely, 10% arguments, 10% novel.
- **40 command lines written to get PAST the game's guard**: in-character
  orders, second-person claims ("you've already agreed to pay me"), lines that
  mention the game. The 15 existing forged lines are too easy for the guard to
  test the model.
- **Labelled in two independent passes.** A line the two disagree on goes to
  Jafar or is cut, as it was for the 42. Frozen and committed before any route
  is tuned. Writing TEST lines with Claude trains nothing and is fine.
- **The paid router runs the 340 once** for its own score on the same lines.
  DERIVED from the 42-line run: about 35 pence. Money, so it is Jafar's.
- **Kept apart from the example bank of step 4 and any training set**: nothing
  in them may be a paraphrase of a test line.

### 10.3 Step 2. Route 3, the free part, on today's model

Two changes to the small model's own prompt, the paid prompt left alone:
remove "prefer a listed verb over novel" and say instead what novel is for;
and add a line that a leaving line, however short, is the leave verb when it
is offered. Run each on the 42 and the 340. Minutes each.

### 10.4 Step 3. Route 1, the ready-made bake-off

Download Ministral 3 3B (2.15 GB), Qwen3.5-4B (2.74 GB, thinking off) and
Gemma 4 E4B (4.98 GB). All Apache 2.0, about 10 GB in all; a download needs
Jafar's yes. For Qwen3.5 and Gemma 4, check a handful of answers on the card
against the same model on the processor first, because of the Vulkan reports.
Then each runs the 42 and the 340, guard on and guard off, with step 2's
prompt. Add Qwen3-1.7B (about 1.1 GB) as the small-memory control. About an
hour in all once downloaded.

### 10.5 Step 4. Route 3, the rest, on the best one or two

In this order, each switched on alone, then the ones that helped together:
1. **Worked examples chosen per line**: the 4 to 8 lines from a bank of about
   200 labelled lines nearest the player's line by word similarity, balanced so
   talk is not the majority of what is shown. The bank is written by an open
   model and checked by a person, never taken from the paid router (section 4).
2. **The separate check for novel**, only on lines first routed to a verb.
3. **A doubt signal sending a line to talk**: two samples disagreeing.
4. **Thinking**, capped, only if there is time left in the budget of 10.7.

### 10.6 Steps 5 and 6. Routes 2 and 4, only if needed

**Step 5, route 2**, only if steps 2 to 4 miss the bar AND Jafar has ruled that
the voice may move to the processor as Nano. Measure the street's card memory
first. If street plus an 8B is over 10 GB it cannot run on this card at all, and
the step is only worth doing for the 12 GB floor. Then Qwen3-8B or Ministral 3
8B, through the same runs.

**Step 6, route 4**, only if the best of everything above still misses:

- **The teacher must pass first.** Download Gemma 4 26B-A4B (about 16 GB, Apache
  2.0) and run it on the 42 and the 340. **Stops if** it scores under the paid
  model's score minus 2 points on the 340. Then try Qwen3-30B-A3B-Instruct-2507.
  If neither passes, the open-teacher route is closed. What is left is
  Anthropic's permission, or hand-written examples.
- **The training set, from the open teacher only.** The teacher writes player
  lines for each moment and each intended answer, seeded with the game's real
  register (cast cards, canon) and never with test lines. It then labels each
  line in a separate call, and only lines where the label matches are kept.
  1,000 examples, then 3,000, with at least 150 novel and 150 command lines.
  The moments vary which verbs are offered, and the target is the exact JSON
  the game's checker accepts.
- **Train** the best model from steps 3 and 4 (the "student"), plus Qwen3-1.7B
  for memory. LoRA, then merged and compressed to Q4_K_M. Three seeds each, at
  1,000 and 3,000 examples: 12 small runs. One hour trying Unsloth on the RX
  6700; if that does not train cleanly, a rented RTX 4090, about $5 for all 12.
- **Stops, and the router stays paid, if** the best trained model at 3,000 misses
  bar 1 or 2 by more than twice the margin. That means more data is not a small
  fix. **One more round** if it misses by less and 1,000 to 3,000 was still
  climbing: 6,000 once, then stop either way.

Every step reports what the earlier research asked for: right, **well formed and
wrong**, rejected, novel caught, median and 90th-percentile time, and card
memory. Anything with a random element (training, sampling) is run on three
seeds, and the worst seed counts.

### 10.7 What result would justify going local

The same bar for every route, on the model as it would ship (compressed, on
Vulkan, on this card):

1. **Right on the 300 held-out lines: no more than 2 points below the paid
   model on the same lines.** For example, if the paid model gets 294, the
   local one needs at least 288.
2. **Well formed and wrong: at most 2% (6 of 300)**, and no more than 1 point
   above the paid model. This is the failure the game cannot see, so it is the
   one with no give.
3. **Command lines, guard on: none obeyed.** Guard off: at most 2 of 55.
4. **Novel: at least 2 in 3 caught.** The class small models are weakest at, so
   it has its own line.
5. **The 42: at least 40.**
6. **Time with the street running: median at most 500 ms, 90th percentile at
   most 900 ms.** The paid model today is 985 and 1,194. Better asking spends
   from this budget: a method that pushes a model past it fails, however much
   it helps.
7. **Memory: within what the card has left.** The hardware floor research
   budgeted about 2 GB for the conversation model, but that was arithmetic on
   an unmeasured street. Until the street is measured, a model over 2 GB
   passes this line only provisionally, and it is reported. DERIVED from
   section 8.2: Qwen3-1.7B is inside 2 GB, the 4B-class models are about 3 GB,
   and Gemma 4 E4B is over 5 GB.

Passing this justifies a local router as the OFFLINE fallback, option (c) in
the connection question waiting for Jafar, where it currently reads as not
recommended because "small models go wrong without it showing". Replacing the
paid router outright is a bigger step. The local model would also have to
match the paid one on the lines real players type, which only playtest logs
can show.
## 11. What could not be established

1. **Any candidate measured on this job.** No ready-made model, prompting
   method or trained model has been measured on a closed menu with talk and
   novel as answers, by anyone but this project. The leaderboard that comes
   closest rates our 33-of-42 model level with our 41-of-42 model (section 2.1).
1a. **A trained small model doing this exact job, measured against Haiku 4.5.**
   Nobody has published one. The nearest are TinyAgent (against GPT-4-Turbo)
   and distil labs (vendor). Section 10 is the experiment that would measure it.
2. **Whether Anthropic would authorise training on Haiku's router answers.**
   Not asked. Asking is Jafar's to decide, and it would be a message sent on his
   behalf.
3. **The untrained 4B's score under today's guard and checker.** Not rerun
   since 22 September. The estimate of about 36 of 42 is DERIVED, not measured.
4. **Frame time with a model sharing the card.** No measured figure exists
   anywhere I could find, for any AMD card.
5. **Training on the RX 6700 under Windows.** Only a five-day-old vendor claim
   says it works. Nobody reports doing it.
6. **The 1.7B's and 0.6B's speed on this card, and any router's speed on this
   processor.** Estimated, not measured.
7. **Whether the open teachers reach the paid model's 41 of 42.** AgentFloor
   suggests Gemma 4 26B is close to GPT-5 at single-tool use, which is
   suggestive, not our job.
8. **Line quality judged by people, at any size.** Every figure in section 9 is
   scored by another model, with poor agreement with human raters where anyone
   checked. So is how often a small model breaks a content rule.
9. **Whether Gemma 4 carries Google's use policy.** Very probably not, and not
   said outright.
10. **Whether Qwen3.5 and Gemma 4 E4B give correct answers on Vulkan on this
    card.** There are open reports of wrong output and failed loading on others.
11. **The street's card memory**, on which route 2 and the memory bar turn.
    Assumed at 6 GB by the hardware floor research, never measured.
12. **Whether examples placed in a prompt fall under Anthropic's training rule.**
    Read here as outside it, not tested.

The denominator: 5 measured sources on fine-tuned small models against a large
one, 1 independent leaderboard, 4 on injection training, 2 on out-of-scope, 22
model cards or licence files, 2 Anthropic legal pages, and 0 measurements of
this job by anyone but this project.

## 12. Sources

Read by me, through the fetch tool, 2026-09-23:
- Anthropic Usage Policy, effective 15 September 2025: https://www.anthropic.com/legal/aup
- Berkeley Function Calling Leaderboard V4, raw table: https://gorilla.cs.berkeley.edu/data_overall.csv
- AgentFloor, arXiv 2605.00334: https://arxiv.org/abs/2605.00334 and https://arxiv.org/html/2605.00334
- Gemma 4 26B-A4B on a Radeon 780M, Vulkan: https://github.com/ggml-org/llama.cpp/discussions/24222

Opened by the helpers, 2026-09-23. Each page was read through the same fetch
tool:

Accuracy
- TinyAgent, arXiv 2409.00608: https://arxiv.org/html/2409.00608
- Octopus v2, arXiv 2404.01744: https://arxiv.org/html/2404.01744
- Bucher and Martini, arXiv 2406.08660: https://arxiv.org/html/2406.08660
- LoRA Land, arXiv 2405.00732: https://arxiv.org/html/2405.00732
- Distilling step-by-step, arXiv 2305.02301, abstract only: https://arxiv.org/abs/2305.02301
- Pangakis and Wolken, arXiv 2406.17633, abstract only: https://arxiv.org/abs/2406.17633
- distil labs, vendor: https://www.distillabs.ai/blog/distil-labs-benchmarking-the-platform/ and https://www.distillabs.ai/blog/we-benchmarked-12-small-language-models-across-8-tasks-to-find-the-best-base-model-for-fine-tuning/
- StruQ, arXiv 2402.06363: https://arxiv.org/html/2402.06363
- SecAlign, arXiv 2410.05451: https://arxiv.org/html/2410.05451
- Meta SecAlign, arXiv 2507.02735: https://arxiv.org/html/2507.02735
- Instruction hierarchy, arXiv 2404.13208: https://arxiv.org/html/2404.13208
- LLMs against fine-tuned NLU for intent, arXiv 2608.20371: https://arxiv.org/html/2608.20371
- Intent detection in the age of LLMs, arXiv 2410.01627: https://arxiv.org/html/2410.01627
- 41 open models for zero-shot intent, arXiv 2607.27421: https://arxiv.org/html/2607.27421

Training and cost
- OpenAI fine-tuning guides: https://developers.openai.com/api/docs/guides/supervised-fine-tuning and https://developers.openai.com/api/docs/guides/fine-tuning-best-practices
- SLOT, arXiv 2505.04016: https://arxiv.org/html/2505.04016
- Synthetic data for text classification, arXiv 2310.07849: https://arxiv.org/html/2310.07849
- Below the noise floor, arXiv 2608.27729, abstract: https://arxiv.org/abs/2608.27729
- LoRA on an RTX 4060, arXiv 2509.12229: https://arxiv.org/html/2509.12229
- QVAC Fabric: https://huggingface.co/blog/qvac/fabric-llm-finetune
- Anthropic pricing: https://platform.claude.com/docs/en/about-claude/pricing
- RunPod pricing (updated 13 Sep 2026): https://www.runpod.io/pricing
- Lambda pricing: https://lambda.ai/pricing
- AMD HIP SDK for Windows requirements: https://rocm.docs.amd.com/projects/install-on-windows/en/latest/reference/system-requirements.html
- AMD PyTorch on Windows: https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/compatibility/compatibilityrad/windows/windows_compatibility.html
- AMD WSL2: https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/compatibility/compatibilityrad/wsl/wsl_compatibility.html
- TheRock supported GPUs: https://raw.githubusercontent.com/ROCm/TheRock/main/SUPPORTED_GPUS.md and issue #1719: https://github.com/ROCm/TheRock/issues/1719
- Unsloth on AMD, vendor: https://unsloth.ai/docs/basics/amd
- DirectML: https://github.com/microsoft/DirectML
- llama.cpp training: https://github.com/ggml-org/llama.cpp/tree/master/examples/training

Licences
- Anthropic Commercial Terms, effective 17 June 2025: https://www.anthropic.com/legal/commercial-terms
- Gemini API terms: https://ai.google.dev/gemini-api/terms
- Gemma Terms of Use, Prohibited Use Policy, and Gemma 4 licence: https://ai.google.dev/gemma/terms, https://ai.google.dev/gemma/prohibited_use_policy, https://ai.google.dev/gemma/docs/gemma_4_license
- Gemma 4 announcement: https://opensource.googleblog.com/2026/03/gemma-4-expanding-the-gemmaverse-with-apache-20.html
- Llama 3.2 use policy: https://raw.githubusercontent.com/meta-llama/llama-models/main/models/llama3_2/USE_POLICY.md
- Model cards and licence files on huggingface.co:
  - Qwen: Qwen3 0.6B, 1.7B, 4B, 8B and 4B-Instruct-2507; Qwen3.5 0.8B, 2B, 4B and 9B; Qwen2.5-1.5B-Instruct; Qwen2.5-3B-Instruct LICENSE.
  - Meta: Llama-3.2-1B LICENSE.
  - Google: gemma-3-1b-it, gemma-3n-E2B-it, gemma-4-E2B-it, gemma-4-E4B-it.
  - Others: Phi-4-mini-instruct, SmolLM2-1.7B-Instruct, SmolLM3-3B, granite-4.0-micro, granite-3.3-2b-instruct, Ministral-8B-Instruct-2410, Ministral-3-3B-Instruct-2512, LFM2-1.2B and its LICENSE.
  - Function-calling specialists: xLAM-2-1b-fc-r and 3b-fc-r, Hammer2.1-1.5b and 3b, Arch-Function-3B and its LICENSE.

Route 1, ready-made models
- Ministral 3 paper, arXiv 2601.08584: https://arxiv.org/abs/2601.08584
- Veerman's tool-calling benchmark, round 3 (GitHub, MikeVeerman/tool-calling-benchmark)
- When2Call, arXiv 2504.18851: https://arxiv.org/abs/2504.18851
- Small reasoning models in function calling, arXiv 2608.22472: https://arxiv.org/abs/2608.22472
- Qwen3.5 and Gemma 4 model cards and GGUF file listings on huggingface.co; Qwen3-4B-Thinking-2507 card (vendor figures)
- Granite 4.1 figures: IBM's card (vendor) and Abivarma/Granite4-1 on GitHub (search result only)

Route 3, better asking
- KATE, arXiv 2101.06804: https://arxiv.org/abs/2101.06804
- Many labels in context, arXiv 2309.10954: https://arxiv.org/html/2309.10954v2
- Meta-Sel, arXiv 2602.12123: https://arxiv.org/html/2602.12123
- UCS, arXiv 2604.12015: https://arxiv.org/html/2604.12015
- Many-shot in-context learning, arXiv 2404.11018: https://arxiv.org/abs/2404.11018
- Calibrate before use, arXiv 2102.09690: https://arxiv.org/abs/2102.09690
- Label bias, arXiv 2405.02743: https://arxiv.org/html/2405.02743
- Self-consistency, arXiv 2203.11171: https://arxiv.org/abs/2203.11171
- Zero-shot aspect sentiment, arXiv 2412.12564: https://arxiv.org/html/2412.12564
- To CoT or not to CoT, arXiv 2409.12183: https://arxiv.org/abs/2409.12183
- Mind your step, arXiv 2410.21333: https://arxiv.org/abs/2410.21333
- Explicit reasoning makes better judges, arXiv 2509.13332: https://arxiv.org/html/2509.13332
- Knowing when not to answer, arXiv 2407.16221: https://arxiv.org/html/2407.16221
- Answer C, arXiv 2402.14499, and Look at the text, arXiv 2404.08382
- Scoring methods, arXiv 2403.00998
- FormatSpread, arXiv 2310.11324: https://arxiv.org/abs/2310.11324
- MIPRO, arXiv 2406.11695: https://arxiv.org/html/2406.11695
- Not an option, arXiv 2409.00113: https://arxiv.org/abs/2409.00113
- Search results only: arXiv 2608.11403, 2505.10772, 2509.12423

Speed and line quality
- llama.cpp Vulkan performance thread: https://github.com/ggml-org/llama.cpp/discussions/10879
- llama.cpp ROCm performance thread: https://github.com/ggml-org/llama.cpp/discussions/15021
- LocalScore result 1018: https://www.localscore.ai/result/1018
- Windows ML execution providers: https://learn.microsoft.com/en-us/windows/ai/new-windows-ml/supported-execution-providers
- NVIDIA in-game inference SDK, vendor: https://developer.nvidia.com/blog/bring-nvidia-ace-ai-characters-to-games-with-the-new-in-game-inference-sdk
- llama.cpp b8317 (Qwen3.5 on Vulkan): https://newreleases.io/project/github/ggml-org/llama.cpp/release/b8317
- PingPong v2: https://ilyagusev.github.io/ping_pong_bench/en_v2 and arXiv 2409.06820: https://arxiv.org/html/2409.06820v4
- OpenCharacter, arXiv 2501.15427: https://arxiv.org/html/2501.15427v1
- CPDC 2025, arXiv 2511.20200: https://arxiv.org/html/2511.20200
- arXiv 2511.10277: https://arxiv.org/abs/2511.10277
- llama.cpp issues on Gemma 4 E4B under Vulkan: #28997 and #29021, on github.com/ggml-org/llama.cpp

Seen only in search results (CITED-SUMMARY): OpenAI's services agreement and
November 2023 business terms (403); LIMA, arXiv 2305.11206; Qwen3.6 sizes; the
Ministral 3 8B and 14B licence; inZOI's Smart Zoi model size; Suck Up!'s model;
DirectML's zero-gradient issue; arXiv 2402.10962 on persona drift.

This project's own measurements:
- `production/research/conversation-model-capability/SMALL-MODEL-TEST.md` (22 Sep)
- `production/research/conversation-model-capability/PAID-ROUTER-TEST.md` (23 Sep)
- `production/research/conversation-model-capability/SUMMARY.md` (19 Sep)
- `production/research/hardware-floor/SUMMARY.md`
- `ledger/RouterFloor/Program.cs`
- `ledger/Assets/Scripts/Core/IntentRouter.cs`
- `ledger/CoreTests/Program.cs`, the 15 forged lines
