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
| `acquaintance` | | `met`, `heardOf`, `calls`: whether they have met him, heard of him, and what they call him (town list 6s); `trusts`, whether they trust him, which matters only to somebody the cast file marks `"namesHim": "on-trust"` (Sheila, Jafar's ruling of 29 September): until the game sends `true`, or their own talk earns it (the reply's `trustEarned`, town list 6bz, which only a reset forgets), they call him the new owner whatever `calls` says; what the game last sent holds until it sends `true` or `false` again, a `false` never undoes trust their talk earned, and a load or a reset forgets what the game sent |
| `present` | | the cast ids of whoever is really within talking range of them (town list 6ad) |
| `ask` | | `tonight`: true while the outfit's ask this person brought tonight stands (Ron, while Arrangement.AskStands: from Delivered until one in the morning, unanswered; town list 6bn); the reply then knows it is his to answer, or that he has just said no |
| `week` | | Sheila's question at the week's end (town list 6ca; WeeksEnd): `ask` true on the turn she puts it (the game's WeeksEnd.Ask just returned true: only at Mickey's office, where the book is), with `realBook` (she trusts him, so it is over Mickey's real book), `dayOff` (a Sunday, her day off) and `ended` (Mickey's arrangement has already ended, so her plain question never offers it, town list 6cc); `stands` true on every later turn to her while it stands (WeeksEnd.Stands). Only Sheila is read for it |
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
| `went` | how the reply went, for the session record's `reply` line: `own` (their own words), `fallback` (their "that's all I know"), `refused` (a line the rules refused, their stand-in said), `brush` (too slow or no model), `cut` (with `--early`, the first sentence heard and the rest too slow even with its own six seconds, town list 6bx), `paused` (talk stopped or unreachable), `ended` (their own words, and they closed the talk); a walk-off answers `walkedOff` instead (town list 6bd) |
| `steps` | the turn's steps, each `[name, ms]` from the turn's start: `draft`, `check`, `redraft`, `recheck`, in the order they ran (town list 6bx) |
| `named` | the cast ids of the people his line named, by name, first name, surname or the street's word for them ("the bookkeeper"), never the words; for the session record's `named` line (town list 6bd) |
| `putToHim` | the deed they raised with him to his face this turn, in their own words: asked him straight out, put a caught or doubted answer to him, or took up his owning up; for the session record's `known` event, how "question" (town list 6bc) |
| `claim` | his answer about where he was: `topic`, `areas`, `result` (`consistent`, `contradiction`, `unknown`), `definite`, and `later` when judged on a later turn (town list 6ac, 6am) |
| `ownedUp` | the deed's topic when he owned up to it (town list 6al) |
| `threatened` | the deed's topic when his line threatened them to keep quiet about it (Silence.Threatens: a menace beside what they must not do, "Say a word and you'll regret it", every other sentence only the words round one; never a question, a joke, somebody else's words, or "I know where you live", often friendly); once a deed; an ask for silence after it, over the same deed, is refused. A threat never buys silence: they remember it and are warier; the game files the story with Silence.FileThreat, the one threatened holding it first-hand (town list 6cd, carried until Jafar rules on his 30 September page) |
| `refusedAsk` | true when, with `ask.tonight` sent, his line was a plain yes (Arrangement.ConfirmsNo: "Yes.", "Yes please", "Yes, I'm sure", "Tell them no.") to Ron's own question, "You want me to tell them no to the envelope?", as his very next line, to Ron, in that conversation within three game hours (a line to anybody else, "walkedAway" and "fresh" clear the question; only Ron, the doorman, is read for it); the game then answers the night Refused, which ends Mickey's arrangement and gives Ron his memory of it. A line that only sounds like a no (Arrangement.SoundsLikeNo) gets that question as its `reply`, written by no model (`generated` false), and `refusedAsk` false; with live talk off, paused, unreachable or too slow, a yes gets Ron's fixed "I'll take your no down the landing" in place of a brush-off (town list 6bn) |
| `weekAnswer` | with `week` sent: `WindDown`, `TakeOver` or `WontSay` when his line was his plain yes (WeeksEnd.Confirms) to her own plain question, as his very next line to her; the game then calls WeeksEnd.Give with that turn's time and Mickey's arrangement, which files the street's story and her memory, and for `WindDown` ends the arrangement that night (Arrangement.WoundDown, town list 6cc). Her lines at the week's end are fixed, written by no model (`generated` false), so they come with live talk off too: `week.ask` gets her question (WeeksEnd.Opening), a line that sounds like one answer while it stands gets her plain question (WeeksEnd.AskPlainly), his yes gets her closing line (WeeksEnd.Took), and with live talk off any other line gets the question again (WeeksEnd.StillAsks); otherwise `null`, and she answers in her own words, told the question stands. A put-off ("I'll let you know") is no answer (town list 6ca) |
| `keepsQuiet` | `topic`, `agreed`, `fragile`: when he asked them to keep it quiet, and the Core's answer (town list 6al) |
| `unchecked` | the check could not run; the reply stands unchecked |
| `fellBack` | the reply is the character's own "that's all I know" line |
| `generated`, `model` | whether the words are the model's, and which, for the subtitle log (town list 6c) |
| `trusts`, `trustEarned` | for somebody the cast file marks `"namesHim": "on-trust"` (Sheila), whether they trust him after this turn, and `trustEarned` true on the one turn of the timeline their own talk earned it (Trust.Earned: once he has talked with them on three different game days, counting only his own non-empty lines, live talk or none; while the game has never sent them a deed with a sighting or hearsay it can place (DeedEvidence), he has never been caught out with them (a lie caught, a sighting his answer did not name, what he told others; Doubted), whatever he said since, both kept in the talk's save; and their suspicion still Trusting); earned only on a turn they answered in their own words (`went` own, ended or fallback), or with live talk off, and never on the day Sheila puts her week's question once she has put it (`week` sent, town list 6ca); a sighting or hearsay near a deed with no place named (`evidence.near`) keeps it back too. Once earned it holds, and it is kept in the talk's save, so a load never says it again. The game's `acquaintance.trusts: true` makes it so whatever the talk, and `trustEarned` then never comes; its `false` never undoes trust earned. When `trustEarned` comes, the game may show her real book. `null` for everybody else; the offline reply carries both too, and a reply without them (a walk-off, Ron's fixed question) leaves it as it was (town list 6bz, carried until Jafar rules on his 30 September page) |

With `--early`, before the reply: `{"id", "to", "first", "ms", "generated"}`,
the first sentence to speak now.

With `noReply`: `{"id", "to", "who", "suspicion", "level", "why"}`.

## Other lines

| sent | answer | meaning |
|---|---|---|
| `{"walkedAway": {"to", "heard"}, "day", "hour"}` | `{"walkedAway", "noted"}` | he left mid-reply; they keep only what he heard (town list 6v); sent while that reply is still being written, it stops it at once, and that line's answer is `{"id", "to", "walkedOff", "ownedUp", "keepsQuiet", "refusedAsk"}`, the last three as for any reply, since what his line did stands (town list 6ay, 6bn) |
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
