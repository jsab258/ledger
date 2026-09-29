# The session record: what the game writes while somebody plays

Town list 6p, 28 September. ROADMAP stage 5 asks for "the four Meridian Test
conditions read off one session". Jafar's runbook (production/playtest/RUNBOOK.md,
his words, never rewritten) says how a session with a friend is run and what
he writes down afterwards. This record does not change that. It keeps what the
game itself can see, so that his four notes have the facts beside them and so
that "three friends getting stuck in the same place" can be read off several
sessions rather than remembered.

## Where it goes

One file per session, JSON lines, UTF-8 with no byte-order mark, in the
game's own Saved folder: `Saved/Sessions/<yyyy-mm-dd-hhmmss>.jsonl`, the local
time the session started (seconds, so a crash and a relaunch in the same minute
are two files). It never leaves the PC. The words a player types are never
kept: only who they named, and no line carries any field this page does not
list.

## The lines

Every line is one object with `t`, real seconds since the session started (one
decimal), and `e`, the event. In the order they happen:

| e | fields | written when |
|---|---|---|
| `start` | `player` (`"friend"` or `"jafar"`), `build` (commit), `fresh` (true for a new game) | the session starts |
| `place` | `at`, a place id from the cast file (production/specs/hook-cast.json) | the player comes within 6 m of a place other than the last one written |
| `still` | `s`, seconds; `at`, the last place | the player has neither moved nor typed for 20 s or more, written once when the spell ends (so it began `s` seconds before `t`), and before `end` if it is still going then |
| `deed` | `what`, the story's topic (`"player.window_d1"`); `seen`, the ids who saw it | the player does something the town can hold |
| `known` | `who`; `how`: `"look"`, `"remark"`, `"recognition"`, `"question"` or `"talk"`; `story`, the topic | somebody visibly shows they know something he did: the second, longer look; a remark to a companion; a line to his face; a question about it in conversation, or anything else the talk helper reports they put to his face (its `putToHim`); or a reply of theirs drew on it (its `spokeOf`) |
| `talk` | `who` | the player opens a conversation |
| `named` | `who`, whom he is talking to; `names`, the ids of the people his line named, by any name the town uses for them; never the line itself | a line the player typed names somebody |
| `load` | `from`, the save; `deeds`, the topics of the deeds the loaded save holds | a save is loaded |
| `reply` | `who`; `how`: the talk helper's `went` (`"own"`, `"fallback"`, `"refused"`, `"brush"`, `"cut"`, `"paused"`, `"ended"`), or `"walkedOff"`; `s`, seconds from his line to the first word he heard | a person answers him (town list 6bd: where a friend's talk broke) |
| `hint` | `moment`, FirstMoments's moment (`"StandingStill"`, `"CanTalk"`, `"FirstAsk"`, `"SeenAtDeed"`, `"OverheardAboutHim"`, `"LedgerOpened"`) | a hint shows, what FirstMoments.Happened or Due returned (town list 6bh) |
| `ask` | `night`, the ask's day; `answer`: `"did"`, `"refused"` or `"noshow"`; `story`, its topic (`"player.outfit_d0"`) | the outfit's ask is answered (Arrangement.Answer, or PassedTo for a night Ron brought him the ask and nobody answered; a night the ask never reached him is not written, town list 6bn); its story counts as a deed of this session for the town's reaction (town list 6bh) |
| `police` | `who`, who told them; `story`, the deed's topic; `how`: `"statement"`, `"description"` or `"talk"` (PoliceFile.Known) | somebody tells the police, or the street's talk reaches DS Ellis (town list 6bm) |
| `ellis` | `why`: `"talk"`, `"body"`, or the reported crime (`"Wounding player.cut_d2"`); `day`, the game day | DS Ellis comes to Quay Street (PoliceFile.EllisComes; town list 6bm); with `day`, her asking after him (`player.police_d<day>`) counts as the town reacting to the crime she came for, or to what he had done by then (town list 6bt) |
| `taken` | `story`, the deed he was taken in for; `day`, the game day; `end`: `"Cautioned"`, `"Charged"` or `"BailedToReturn"` (Custody.End) | he is taken in (PoliceFile.TakeIn); the street's word of it (`player.taken_d<day>`) counts as the town reacting to that deed, as what he claimed about a deed (`player.claim_<deed>`) does to the deed (town list 6bt) |
| `end` | `why`: `"quit"` or `"crash"`; `usd`, what the talk cost this session (the talk helper's closing line) | the session ends |

Required: `player` (start), `at` (place), `s` (still), `what` (deed), `who` and
`story` (known), `who` (talk), `names` (named), `moment` (hint), `night`, `answer`
and `story` (ask), `who`, `story` and `how` (police), `why` (ellis, end), `story` and
`day` (taken); `load`
needs none.
The others may be left out. `player` is `"friend"` or `"jafar"` and `how` one
of the five above; any other value is warned about. Nothing else is written. A line the reader cannot use
(unknown `e`, a field missing or of the wrong kind) is shown as unread, and a
field this page does not list is warned about, most loudly on `named`.

## What the reader gives him

`python tools/session_read.py <file or folder>`

For one session:
- how long it ran and how it ended, and whether it began as a new game or loaded a save;
- where they went on their own, in order, with minutes;
- when they went still, where, and for how long;
- whom they named, and when first;
- each time the town showed it knew something they had done: a `known`
  whose `story` is the `what` of a `deed` done at or before it, in this
  session (Meridian condition 2: the first, by minute thirty or not); knowns
  about anything else are listed apart, as about something from before the
  session or a load;
- for a friend's session, his four things as the runbook has them, with what
  the record saw beside the one it can speak to; every answer is his.

For a folder of sessions:
- where friends went still, by how many of them went still there, then for how
  long (where they got stuck: "three friends getting stuck in the same place");
- in how many friends' sessions (`player` `"friend"` only) the town reacted by
  minute thirty, and of those the median minute;
- for his own sessions (`player` `"jafar"`), which evenings he played and for
  how long: the one fact condition 4 has that is not a memory.
