# The talk program's protocol

What the game sends the talk program (ledger/TalkHelper, shipped as
LedgerTalk.exe) and what it sends back: one JSON object a line each way, in
UTF-8, on the program's standard input and output. Every field the program
reads or writes is here, with the town list item that brought it; the
handover lines in NOW.md say when to send each, this page says what each is.
`python tools/talk-protocol-check.py` fails when the program reads or writes a
field this page does not name.

## Starting it

`LedgerTalk.exe [--early] [--fake] [--relay <address> --copy <code>]`, from the
folder with its cards and `hook-cast.json` beside it (town list 6aa).
`--early` sends each reply's first checked sentence as soon as it is ready;
`--fake` answers without a model; `--relay` and `--copy` talk through our
server (town list 6b), otherwise `ANTHROPIC_API_KEY` is read.

It first writes one line:

| field | meaning |
|---|---|
| `ready` | true |
| `cards` | the characters it can speak as |
| `online` | whether a model is reachable |
| `fake` | whether it is answering without one |
| `notice` | `title`, `text` and `report`: the AI notice to show before the first conversation and from the menu, and the label for the report button (town list 6c, 6w) |

## A line to a character

| field | | meaning |
|---|---|---|
| `id` | required | the turn's number, returned on every line about it |
| `to` | required | the card: `lena`, `rocco`, `sam` |
| `who` | optional | the cast id when it differs from the card (production/specs/hook-cast.json) |
| `say` | required | what the player typed |
| `day`, `hour`, `minute` | | the game's time now |
| `scene` | | the weather and the light only; where they are comes from the cast file (town list 6u) |
| `fresh` | | true when he walks up to somebody again: a new conversation (town list 6ae); once sent for a person, only the game starts their talk afresh, and until then the program does after six game hours apart (town list 6az) |
| `memories` | | what the character remembers from the simulation: `day`, `hour`, `minute`, `kind`, `importance`, `text`, and `story`, the deed's topic when it is about something Tom did (town list 6ah) |
| `knows` | | facts they hold: `subject`, `predicate`, `value` |
| `suspicion`, `suspicionWhy` | | the level the game holds and why; or instead |
| `evidence` | | `account` (`held`, `seen`, `names`, `rung`, `confidence`, `namingConfidence`, `summary`), `near` (`sawHim`, `heard`, `others`, `summary`) and `familiarity`, from which the Core derives the level (town list 6n) |
| `knowing` | | `level` (`nothing`, `little`, `enough`) and `story`: how much of a story about Tom has reached them (town list 1) |
| `acquaintance` | | `met`, `heardOf`, `calls`: whether they have met him, heard of him, and what they call him (town list 6s) |
| `present` | | the cast ids of whoever is really within talking range of them (town list 6ad) |
| `deed` | | the deed they suspect him of: `topic`, `day`, `hour`; `sawHimAt` (a place or area id where they saw him within about an hour of it); `heardHimAt` (where they have heard he was then); `heardHeSaid` (the area ids of what he has been telling people, when that has reached them); `grave` (true for a killing) (town list 6ac, 6al, 6am) |
| `noReply` | | true to have the Core decide the level from `evidence` without a reply |

The reply:

| field | meaning |
|---|---|
| `id`, `to`, `day` | as sent |
| `reply` | what the character says, checked and cleaned |
| `rest` | with `--early`: what follows the first sentence already sent |
| `ms` | how long it took |
| `offline`, `timedOut` | no model, or too slow: `reply` is the character's own brush-off (town list 6ap) |
| `walkedOff` | he walked off while it was being written: there is no reply, and they keep only what he heard (town list 6ay) |
| `paused` | a plain note for the player, not in a character's voice: live talk has stopped and when it comes back (town list 6t), or cannot be reached just now, or is off in this copy (town list 6ax) |
| `ends` | the character has closed the conversation (town list 6ae) |
| `heard` | the memories the reply could draw on |
| `suspicion`, `level`, `why`, `manner` | where their suspicion stands, why, and how a story about him made them behave |
| `invented`, `promised` | details the check refused, and promises the world will not keep, in the first draft (asked again without) |
| `spokeOf` | the stories a reply drew on, for the session record's `known` event (town list 6ah) |
| `putToHim` | the deed they raised with him to his face this turn, in their own words: asked him straight out, put a caught or doubted answer to him, or took up his owning up; for the session record's `known` event, how "question" (town list 6bc) |
| `claim` | his answer about where he was: `topic`, `areas`, `result` (`consistent`, `contradiction`, `unknown`), `definite`, and `later` when judged on a later turn (town list 6ac, 6am) |
| `ownedUp` | the deed's topic when he owned up to it (town list 6al) |
| `keepsQuiet` | `topic`, `agreed`, `fragile`: when he asked them to keep it quiet, and the Core's answer (town list 6al) |
| `unchecked` | the check could not run; the reply stands unchecked |
| `fellBack` | the reply is the character's own "that's all I know" line |
| `generated`, `model` | whether the words are the model's, and which, for the subtitle log (town list 6c) |

With `--early`, before the reply: `{"id", "to", "first", "ms", "generated"}`,
the first sentence to speak now.

With `noReply`: `{"id", "to", "who", "suspicion", "level", "why"}`.

## Other lines

| sent | answer | meaning |
|---|---|---|
| `{"walkedAway": {"to", "heard"}, "day", "hour"}` | `{"walkedAway", "noted"}` | he left mid-reply; they keep only what he heard (town list 6v); sent while that reply is still being written, it stops it at once, and that line's answer is `{"id", "to", "walkedOff"}` (town list 6ay) |
| `{"report": <id>, "why": <note>}` | `{"reported", "found", "saved", "thanks"}` | the report button on a reply (town list 6c) |
| `{"talk": "save", "path", "stamp"}` | `{"talk": "saved", "people"}` | keep every conversation beside the game's save (town list 6r) |
| `{"talk": "load", "path", "stamp"}` | `{"talk": "loaded", "people", "skipped"}`, or `missing`, `stale`, `error` | put them back |
| `{"talk": "reset"}` | `{"talk": "reset"}` | a new game forgets them |

A report is kept as a line with `reportedAt`, `why` and `turn`.

When the game closes the program's input, it writes one last line and stops:
`{"cost", "usd", "calls"}`, what the session's model calls cost, by model, in
dollars at the game's own price table, and how many there were.

Errors: `{"error": "bad-line"}`; `{"id", "to", "error": "no-card"}` or
`"no-evidence"`; `{"talk", "error": "unknown"}`, `"unwritable"`,
`"unreadable"` or `"path-must-end-.talk.json"`.
