# D47. The conversation pillar's reasoning is withdrawn, not the pillar: the model never adjudicates, and nothing follows about its size

CANON: none

Ruled by Jafar, 2026-09-21, in his first message of that day, kept verbatim in
`game-design/decision-2026-09-21-the-week-after-the-reset-five-measurements-and-eleven-rulings.md`
under "On the conversation pillar". Written by the director the same day; the
resident reviews and commits. His instruction for this batch: "RULINGS,
recorded as you go. Number them from the register's next free number after
checking it. They are corrections to decisions, not new work."

The directive above is `none` because pillar 2 in
`ledger-v2/respec/vision-pillars-v2.md` is unchanged by this record. What is
withdrawn is an inference drawn from it, not the pillar and not a world fact.

## The rule, as given

**"The pillar's reasoning about the conversation model is withdrawn, not the
pillar. It said the model only classifies and picks from closed sets, so it can
be small. The constraint-tax paper, read in full, measures the opposite for
small models: constraining output to a closed set takes schema validity to one
hundred percent and answer accuracy from 19.7 down to 11, with wrong-but-valid
answers at 88.9 percent. A small model would confidently return well-formed
wrong choices, which is the one failure the deterministic core cannot catch,
since it checks that an output is in the set and not that it is the right
member. The pillar stands: the model never adjudicates. What falls is the
inference that it can therefore be small. Its size is the measurement ordered
above, and no hardware floor is written before that number exists."**

## What stands, quoted from the source so nobody re-derives it

Pillar 2, `ledger-v2/respec/vision-pillars-v2.md` line 16, read 2026-09-21:
"Real conversation. Live LLM dialogue with per-character memory, spoken via
the local voice pipeline, within measured latency budgets. Conversation always
matters: outputs are classifications and closed-set choices that deterministic
Core executes." Pillar 3, line 17: "LLMs classify, never adjudicate."
Constitution law 2, `ledger-v2/studio-v2/constitution.md` line 4:
"Classification, not adjudication. LLMs choose from closed sets assembled from
live state; deterministic Core computes every outcome the player feels."

None of those three sentences says the model can be small. The sentence that
drew that inference was not found on main: a grep over every `*.md` in the
tree on 2026-09-21 for "can be small", "small model", "smaller model", "cheap
model", "local model" and "closed set" returned the three sentences above,
D-record cross-references, v1 documents about cost tiers (named under D48),
and nothing drawing the size inference. His message attributes it to "the
research", which sits on a research branch not in this checkout. Its mark
under D43 lands with the research consolidation (the number the resident's
log assigns is queue 394).

## What falls, and what replaces it

The inference "closed sets, therefore small". What replaces it is a
measurement, not an argument: the small-model test he ordered in the same
message (the number the resident's log assigns is queue 390; no file numbered
388 to 398 existed under `production/queue/` when this record was written,
listed 2026-09-21, while 380 to 387 did). His bar for it, verbatim: "scored on
a bar that counts a well-formed wrong answer as a failure rather than a pass",
with caching on and the cost per hour printed first. "It gates the hardware
floor, and the hardware floor gates who can run this game, which is a scope
decision I cannot make without the number."

Until that number exists: no document writes a model size, a hardware floor or
a min-spec from an argument (D52 for the paper that was read as one), and
nothing tiers residents by model (D48).

## What the deterministic core checks today, read rather than remembered

`ledger/Assets/Scripts/Core/ResponseValidator.cs`, read whole on 2026-09-21:
length (`MaxChars = 900`, cut at a sentence end), eight fourth-wall break
markers replaced by an in-character deflection, self-narration, and
well-formedness through `TextShape`. `Core/ConversationEngine.cs:276`
`ValidateReply`: strips reasoning blocks and stray tags, unwraps quotes,
truncates. `Core/IntentRouter.cs:438` `public static Intent Validate(string
raw, IntentContext ctx)` is the closed-set site by its signature; its body was
not read for this record. That is membership and shape. Nothing there can tell
the right member of a set from a wrong one, which is his point.

## What changed in the same batch

- `ledger-v2/open-questions.md` item 3, corrected under D43: it read "Deferred
  to ship-prep by explicit decision"; it now says the floor waits on the
  small-model test and the cost per hour, citing D47 and D52. Item 1 of the
  same file, "Engine. Open until the D1 probe lands", was stale against D16 and
  is corrected in the same pass; named in the report.
- Nothing in `vision-pillars-v2.md`, the goal block or the constitution moved.

## What this does not decide

The model. Whether tiering by interaction is needed (D48). The floor (D52).
Where the conversation pillar's rungs sit on the ladder, which is the first of
the two cards he asked for and is the Producer's to write.
