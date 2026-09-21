# D49. Live content screening is a pillar dependency, and the conversation pillar's first rung

CANON: none

D18's content rule is UNCHANGED; this record adds the gate that applies it to
what a character says while the game runs.

Ruled by Jafar, 2026-09-21, first message, under "On the conversation pillar",
kept verbatim in
`game-design/decision-2026-09-21-the-week-after-the-reset-five-measurements-and-eleven-rulings.md`.
Written by the director the same day; the resident reviews and commits.

## The rule, as given

**"Live content screening is built, and it is a pillar dependency rather than
a ship task. Steam's January 2026 rules put us in the live-generation category
twice over, because our characters both write and speak their lines as the
game runs, and that category requires guardrails that stop illegal or
offensive material reaching the player as a condition of being on the store.
Today the validator checks length and staying in character, and the content
rule is called only from crowd body generation, so nothing screens what a
character says or what the voice speaks. It does not need to be sophisticated
to start, because the deterministic core already licenses what a character may
say and this is a last gate rather than the whole defence. It goes on the
ladder as the conversation pillar's first rung."**

## His sentence about today's code, checked by grep and by reading, 2026-09-21

"Today the validator checks length and staying in character":
`ledger/Assets/Scripts/Core/ResponseValidator.cs`, read whole. Its docstring
says "Two jobs only". It truncates at `MaxChars = 900` on a sentence boundary;
it replaces a reply containing any of eight break markers ("as an ai",
"language model", "system prompt", ...) with an in-character deflection; it
deflects self-narration (`ReadsAsNarration`); it repairs shape through
`TextShape.Tidy` and deflects what `IsWellFormed` refuses; `Humanize` strips
AI tells; `TellCount` is telemetry. There is no word list for illegal or
offensive content and no call to `ContentRule`. `Core/ConversationEngine.cs:276`
`ValidateReply` strips reasoning blocks and stray tags, unwraps quotes and
truncates. Length and staying in character: HOLDS.

"The content rule is called only from crowd body generation": every call site
of `ContentRule.` in `*.cs`, `*.cpp` and `*.h` on 2026-09-21 is
`Core/Population.cs:177` (`ContentRule.Screen(Trades)`) and `:186`
(`IsShowableTrade`), `Game/RealBody.cs:501` (`IsUnderageModel` on a prefab
stem), and `CoreTests/Program.cs`. `Core/ContentRule.cs` says of itself: "It
does not read dialogue: that is tools/content-gate.py". Crowd generation and
the crowd body pick, nothing on the reply path: HOLDS.

"All five content gates read text": `tools/content-gate.py` exists;
`ledger/verify.py:1771` walks the banks; `tools/brand-verify.py` reads
`contentRule`; `tools/canon-gate.py` and `tools/imagegen/imagegen.py` scan
prompts and forbidden tokens. All five read static text or prompts, none a live
reply. Not read for this record: `tools/voice-live/speak.py`, so whether the
voice path carries any screen of its own is unchecked; no call to a screen was
found by the grep above.

Steam's rules and the category are his statements from the research and are
not verified here.

## What is decided

1. Screening is a DEPENDENCY of pillar 2, not a ship-prep task.
   `ledger-v2/open-questions.md` item 7 still lists moderation under
   "deferred to ship-prep"; that word now covers moderation of players, not
   screening of generated lines, and the item is corrected in this batch to say
   so.
2. It is the conversation pillar's FIRST RUNG. WHERE that pillar's rungs sit
   relative to the visual stages is the first of the two cards he asked for
   (Producer, `production/decision-queue.md`). The rung table in
   `production/ladder.md` is his to edit (stages.md: "nobody but him edits the
   rung table"), so this record adds no row there. Until the card is answered
   the rung is recorded under stage 2 in `production/stages.md`, where the
   conversation clauses already fold.
3. Its shape: a last gate on the reply path, where `ResponseValidator.Validate`
   already stands ("every LLM reply passes through here before the player sees
   it"), and before the line reaches the voice. It fails closed to the same
   in-character deflection. It ships inside the game, so it is Core work with
   full review (D45), with a planted rejecting case and an accepting case both
   watched (rule 5b), and it prints its denominator: replies screened, replies
   refused.
4. "It does not need to be sophisticated to start." A word list under D18's
   canon section is a valid first rung; the next rung is the research task.

## What this does not decide

What the screen is beyond a first rung. When it is built: no queue item is
filed by this record; the stage placement waits on the card, and D44 gives the
studio the order within the ladder once it is placed.
