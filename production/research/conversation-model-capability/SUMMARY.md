# The closed set does not make the job easier, and there is a measured tax

STATUS: SPEC (research delivery). Branch `research/conversation-model-capability`.
Written 2026-09-19. Audited against `BRIEF.md` in this folder, written first.

NOTHING HERE IS AN INSTRUCTION. No decision record, no model chosen.

## 0. Sourcing

`export.arxiv.org` is open (200) and is the channel for this topic. **Three
papers were read in full** through it. Three web searches. Everything not
attributed to one of the three papers is a search summary and is labelled
CITED-SUMMARY.

## 1. The answer, first, and it inverts the pillar's reasoning

The pillar's logic is: the model only classifies and picks from closed sets, so
it can be small. The measured evidence says the second half does not follow from
the first.

**Constraining a small model's output to a closed set makes the FORMAT perfect
and can make the CHOICE worse.**

CITED, read in full, arXiv 2605.26128, "The Constraint Tax: Measuring
Validity-Correctness Tradeoffs in Structured Outputs for Small Language Models",
whose subject is literally "on-device and low-cost small language model
deployments, where sub-3B checkpoints are attractive". Its abstract, verbatim:

> The usual assumption is that hard output constraints only improve the wrapper
> around an answer. Our measurements show that, for small models, the wrapper
> can change the answer.

In its 15,000-generation main suite:

| | prompt only | hard answer-only schema |
|---|---|---|
| schema validity | 61.5% | **100.0%** |
| answer accuracy | 19.7% | **11.0%** |
| wrong-valid-schema rate | 49.5% | **88.9%** |

And the setting closest to LEDGER's job, a calendar tool-call analogue, which is
exactly "pick the right member of a closed set and emit it as structured data":

> prompt-only JSON achieves 91.5% executable accuracy; the same hard tool-call
> schema reaches only 48.0%, even though both directly generated modes are
> 100.0% schema-valid. **The error is semantic, not structural.**

DERIVED, and it is the finding: a closed set is not a smaller job. It is the
same job with the failure mode hidden, because every wrong answer now looks
well-formed. "Wrong-valid-schema rate" is the paper's name for that, and at
88.9% it is the dominant outcome rather than an edge case.

## 2. What reliability means as a number a build could be held to

The brief asked for this specifically, and the same paper answers it better than
I would have:

> Production reports should separate schema validity, answer accuracy,
> executable accuracy, and wrong-valid-schema rate.

And the warning that goes with it: **"A production system that reports only
schema validity would miss the regression."**

DERIVED: a gate that asserts "the model returned a member of the closed set" is
the exact gate this paper says is blind. The number this project would have to
hold a build to is **wrong-valid-schema rate**, which is the fraction of
responses that are well-formed and wrong. Nothing in this repository measures
anything of that shape today, and the conversation model is not built yet, so
this is cheap to get right before it exists rather than after.

## 3. The lever that does work at 1B, and it is not constraining

CITED, read in full, arXiv 2505.04016, "SLOT: Structuring the Output of Large
Language Models": with supervised fine-tuning, Llama-3.2 at 1B and 3B and
Mistral-7B "outperform existing solutions across evaluation dimensions", and
"even the 1B parameter model reaches impressive performance", with constrained
decoding providing "a complementary guarantee of structural validity, which is
particularly pronounced in smaller models".

DERIVED, reading 2505.04016 against 2605.26128: the two are not in conflict.
Constraining alone taxes a small model. Fine-tuning the small model for the
output shape, and then constraining, is the combination that works. That is the
same shape as arXiv 2511.10277's method, which fine-tuned a persona with LoRA
rather than prompting one.

**So the honest answer to "what is the smallest model that reliably does this"
is: smaller than you would think IF it is fine-tuned for the job, and worse than
you would think if it is prompted and constrained.** The size question is
downstream of a training decision nobody here has made.

## 4. The latency cost, which nobody had priced

CITED, read in full, arXiv 2605.02363, "When Correct Isn't Usable": across three
7 to 9B models, "constrained decoding enforces syntactic validity but incurs
3.6 to 8.2 times latency overhead and in several settings degrades task
performance substantially". On GSM8K the range is "3.6 (Llama CONSTRAINED) to
8.2".

DERIVED, and it lands on live speech: topic 1's whole budget is time to first
sound, and the LLM leg is the one it called "the leg nobody has measured". If
that leg uses constrained decoding, this is a 3.6x to 8.2x multiplier on an
unmeasured number. HOLE: the figure is for 7 to 9B models on a maths benchmark,
not a 1B classifier on a dialogue turn, and I did not find a figure for the
latter.

## 5. Has anyone shipped it? Yes, once, and it is a named case

CITED-SUMMARY: inZOI, Krafton's life sim, early access 28 March 2025. Its
"Smart Zoi" characters "run on an on-device small language model built with
NVIDIA ACE, so the AI drives moment-to-moment behavior locally rather than
phoning a cloud for every line". That is the nearest shipped analogue to pillar
2 that exists.

CITED-SUMMARY, and it is the caution worth carrying: runtime dialogue systems
calling a local model "are powerful for jams and experiments but harder for
certification, offline play, and consistent canon". DERIVED: consistent canon is
precisely what this project's deterministic Core is supposed to guarantee, so
the architecture already answers the third objection. The first two are ours to
face later.

HOLE: I could not open inZOI's own material. What Smart Zoi actually decides,
at what size, with what reliability, is unestablished.

## 6. On the persona half

Benchmarks for persona consistency exist and are named: CITED-SUMMARY, RPEval
(emotional understanding, decision-making, moral alignment, in-character
consistency), PersoBench, PersonaArena, plus a survey of role-play evaluation.

DERIVED, and it is a caveat rather than a finding: these evaluate open-ended
in-character generation and score it with an LLM judge, which is the same
instrument arXiv 2511.10277 used to produce the 55 percent figure that prompted
this topic. **None of them measures the thing pillar 2 actually asks for**,
which is closed-set selection under a fixed persona. The benchmark that bears on
this project's job is the constraint-tax protocol in section 1, not a role-play
leaderboard.

## 7. What changes for the decision

1. **The hardware floor still cannot be written, and now for a better reason.**
   Not "nobody chose a size" but "size is downstream of whether the model is
   fine-tuned for the job". A fine-tuned 1B and a prompted 7B are different
   entries in the memory budget and the evidence points at the former.
2. **The pillar's sentence should be read more carefully than it has been.**
   "Classifies and picks from closed sets" describes the interface, not the
   difficulty. Nothing measured supports the inference from closed set to small
   model, and 2605.26128 measures the opposite.
3. **The number to hold a build to is wrong-valid-schema rate** (section 2), and
   it is cheapest to design in before the model exists.
4. **Constrained decoding is not free on latency** (section 4), and the live
   speech budget has no room for a 3.6x multiplier on an unmeasured leg.

## 8. What could not be established

1. **A single smallest-model number.** The question as posed has no published
   answer, because published results are per task, per fine-tune and per
   constraint mode. The three papers bound it rather than answer it.
2. **Any figure for a 1B model doing closed-set selection under a persona**,
   which is the exact job. The nearest is 2511.10277's 55 percent on open
   factuality, which is a different task.
3. **What inZOI's on-device model actually does or how big it is.** Section 5.
4. **Latency for a small classifier**, as opposed to 7 to 9B models on maths.
5. **Whether an LLM judge is a sound instrument** for any of this. Three of the
   sources rest on one and none validates it against humans.

## 9. Sources

Read in full through `export.arxiv.org`, 2026-09-19:
- arXiv 2605.26128, "The Constraint Tax: Measuring Validity-Correctness
  Tradeoffs in Structured Outputs for Small Language Models"
- arXiv 2605.02363, "When Correct Isn't Usable: Improving Structured Output
  Reliability in Small Language Models"
- arXiv 2505.04016, "SLOT: Structuring the Output of Large Language Models"

Search channel summaries, none opened: cinevva.com, localaimaster.com,
markaicode.com, distillabs.ai, martinuke0.github.io, and the persona benchmark
listings (RPEval, PersoBench, PersonaArena).

Prior lane work relied on: `production/research/hardware-floor/RECHECK.md` for
arXiv 2511.10277.
