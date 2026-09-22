# D48. No resident speaks through a worse model than another because of who they are

CANON: none

Ruled by Jafar, 2026-09-21, first message, under "On the conversation pillar",
kept verbatim in
`game-design/decision-2026-09-21-the-week-after-the-reset-five-measurements-and-eleven-rulings.md`.
Written by the director the same day; the resident reviews and commits.

## The rule, as given

**"No resident speaks through a worse model than another because of who they
are. The research recommends running the crowd on a small local model and the
named cast on a better one. That is ruled out, because a consistent quality
difference would tell the player who matters before the game does, which is
the opposite of what this game is about. If tiering is needed, it follows the
interaction rather than the person, so a passing remark runs cheap for anyone
and a real conversation runs well for anyone; or everyone runs the better
model. Choose between those only when the small-model test and the cost per
hour exist."**

## The test, in one line

Tiering by PERSON is out. Tiering by INTERACTION is allowed. Choosing between
"tier by interaction" and "everyone on the better model" waits for D47's
measurement and the printed cost per hour.

This is D25's principle on a third axis. D25: residents are tiered by
authoring, never by memory. D48: never by model either. A player who can hear
which residents the studio spent more on has been told who matters, and the
moat is that the town decides that, through what people remember and say.

## What it covers

"Speaks through a worse model" covers the language model that writes a line
and the voice model that says it. It does not forbid fewer voice IDENTITIES
for the crowd than for the cast (the 2026-08-01 count in
`game-design/production-plan-audio-art.md`, "x 6 crowd pool voices", is a count
of identities on one engine, not a quality tier); it forbids a worse engine or
a worse model behind anyone because of who they are.

## Sites on main that said otherwise, and what was done under D43

- `game-design/production-plan-audio-art.md` section 1a, lines 46 to 49 on
  2026-09-21: "premium voices for the ten named cast members (low volume,
  highest quality bar, much of it pre-generatable), and either commodity-cheap
  or local for everything else", and section 1g line 303 "the tiered shape in
  §1a". A 2026-07-28 SPEC. MARKED in the file in this batch, at section 1a,
  with a D48 note; the old text stands under it as the record of what was
  proposed.
- `game-design/research-mechanics.md` lines 46 to 47: "Mitigate: cheap model
  tier for ambient NPCs, better model for core cast". A v1 research document.
  Dictated one-line mark for the resident to hand-apply immediately after line
  47: `RULED OUT by D48, 2026-09-21: no resident runs on a worse model because
  of who they are; tiering, if any, follows the interaction.`
- `game-design/m15-the-world-speaks.md` line 146: "Mitigation: cheap model
  tier, per-pair-per-day caching" for ambient chatter. Read with two lines of
  context only. It tiers by CHANNEL (ambient chatter), which is by interaction,
  so it is not contradicted; named here so nobody re-reads it as a tier by
  person.
- The research recommendation itself ("the crowd on a small local model and
  the named cast on a better one") was not found on main by grep for "crowd on
  a", "named cast on", "small local model", "cheaper model", "worse model" over
  `*.md` on 2026-09-21. It is in the research delivery on its branch; its mark
  lands with the consolidation (queue 394 in the resident's log).

## What this does not decide

Which model. Whether tiering by interaction is needed at all. What "a passing
remark" and "a real conversation" are as classes: that is a design line for
the conversation pillar's rungs, drawn when the numbers exist.
