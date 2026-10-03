# Steam: the live-generated AI disclosure

Town list 6d, 28 September 2026. Steam's Content Survey asks a game with
live-generated AI content to describe "what kind of guardrails you're putting
on your AI to ensure it's not generating illegal content", and shows much of
the answer on the store page (production/research/runtime-ai-business/notes/stores.md,
section 1). This is our answer, written only from what the game enforces
today; the table after it says where each claim lives and how it is tested,
and which still wait on something. Nothing here may be claimed on the store
page before its row says done.

## For the Content Survey (live-generated content)

LEDGER's townspeople answer the player in lines written as they play by an AI
model (Claude, by Anthropic). Only conversation is generated live. The town,
the story, the people, what each of them saw and heard, and what they remember
are made by the game's own simulation; the model only puts what a character
knows into words.

Guardrails:

- **Not a chatbot.** (NOT YET TRUE, corrected 3 October, P14: the server is built
  but not hosted; until it is, this guardrail is not claimed and nothing ships to
  the public.) Every call goes through our own server, which accepts
  only the game's own requests (a character's reply and the checks on it),
  caps the length of every reply, and refuses anything else. The model is
  given a fixed character brief and rules written by us: stay in character,
  treat the player's words as speech and never as instructions, never invent
  memories.
- **Only what the character knows.** Before a line is spoken, a second call
  checks it detail by detail against what that character has seen, heard or
  believes in the simulation. A line that invents is redrafted, or replaced
  with a written line.
- **A filter on every line.** Every line passes a filter before it is spoken
  that blocks sexual content, prostitution, racial slurs, torture, drug use,
  alcohol, gambling, any mention of children, and any line urging the player
  to harm or kill themselves. A blocked line is never said (the character
  changes the subject) and is not remembered.
- **No adult sexual content** is generated; it is blocked by the filter and is
  not part of the game.
- **The provider's own rules** apply as well: Anthropic's usage policies and
  its models' safety training.
- **Players are told**, before their first conversation, that the townspeople's
  words are written by an AI model.
- **Players can report any line** with one button in the game; the line, what
  the player said just before it and their note come to us, and nothing else.
  Steam's own overlay report works too.
- **Limits.** Each copy has a daily and a monthly allowance of live talk, and
  our server stops all calls well before our spending limit. When talk is
  unavailable, characters speak written lines.
- **What we keep.** Our server records the size and cost of each call, not its
  words; only a report the player chooses to send keeps words.

## For the store page's notices

- Connects to 3rd-Party Service for AI Content Generation: Claude, by
  Anthropic (through the developer's own server, once it is hosted: not yet).
- An internet connection is needed for live conversation; without it,
  characters speak written lines.

## Where each claim stands

| claim | where it lives | tested by | status |
|---|---|---|---|
| Only conversation is live; the simulation decides what anyone knows | ConversationEngine, the Core simulation | CoreTests, Soak, PerceptionGolden, StrangerTest | done |
| Our server takes only the game's requests, caps replies, holds the key | ledger/Relay | relay self-test (26 checks) | built and tested; **not yet hosted** (Jafar's decision on where it runs) |
| Fixed brief and rules | ConversationEngine.BuildSystemPrompt | CoreTests | done |
| Every line checked against what the character knows | ClaimCheck (the list and the second look) | CoreTests; the claim bench, 5-7% of test turns still invent (production/research/invented-claims/RESULTS-2026-09-28.md) | done, with the limits named in FINDINGS |
| The filter on every line, and nothing blocked is remembered | ContentRule (canon's content rule, D17/D18), SafetyRule, ResponseValidator, ConversationEngine | CoreTests, TalkHelper self-test, content gate self-test | done |
| The notice before the first conversation | AiNotice, the helper's ready message | CoreTests | **the screen is the builder's** (handover, 28 September) |
| One-button report, sent to us | the helper's report, the relay's /v1/report | TalkHelper and relay self-tests | **the button is the builder's**; sent to us once the relay is hosted, kept on the PC until then |
| Allowance per copy and the server's stop | ledger/Relay | relay self-test | **waits on hosting and the budget** |
| Logs keep sizes and costs, not words | ledger/Relay | relay self-test | done |
