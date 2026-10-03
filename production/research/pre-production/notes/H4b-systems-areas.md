> **Helper evidence note** for the pre-production review of 3 October 2026, kept as written by a read-only helper. Corrections found on checking are listed in ../SOURCES.md, "Corrections to the helper notes"; where they differ, the numbered sections govern.

# H4b. LEDGER's systems, area by area: where each stands (evidence as of 3 October 2026)

Read-only evidence gathering over /home/user/ledger at main 79cf8db (3 Oct 2026, 10:46 UTC). Nothing in the repository was changed.

**Method and limits**
- The local clone is shallow: it holds only 105 commits, from 1 October on. Commits from 20 to 30 September (1,172 on main) were listed from GitHub with `gh api` (saved at scratchpad/commits-0920-0930.tsv). Of those, 245 are the build machine's automatic "UE machine probe" returns. Another 22 have come since 1 October.
- Read: NOW.md, TOWN.md, CLOTHES.md, FINDINGS.md, DECISIONS.md (all 262 lines), FOR-JAFAR.md, ROADMAP.md, THIRD-PARTY.md, canon.md, ledger-v2/research/license-allowlist.md, every audit in production/audits/, about 30 research notes, production/playtest/, production/d1-probe/ verdicts, the headers of the main tools, and the code where a claim needed checking (TalkHelper, Relay, CrimeProbe.cpp, voice-server.py).
- Two tools were run read-only: `tools/content-gate.py --enforceable` and `tools/approvals.py`. `git status` was clean afterwards.
- Not reachable from here:
  - Jafar's PC: the F: drive, the played copy, the AI tester's pictures, session records, logs;
  - his approval pages' stored answers;
  - billing;
  - the live voices (not heard);
  - the Unreal editor.
- Anything stated about those comes from the repository's own records and is labelled as such.
- Times are as the records give them. Where a record does not say, UTC is assumed.
- **Notation.** "DEC:nnn" means DECISIONS.md line nnn. Bare D-numbers (D18, D19, D24, D46, D48, D56) are the project's own numbered decision records, as canon.md and production/archive/DECISIONS-to-2026-09-24.md use them. "#n" after "rulings sweep" is the row in production/audits/rulings-sweep/SUMMARY.md.

---

## 1. Live talk (the language model)

**In the packaged game today**
- Typed talk works with three characters only: Sheila (id lena), Ron (rocco) and Darren (sam).
- Only three talk cards exist and ship: production/cast/cards/lena.md, rocco.md and sam.md. tools/publish-talk-helper.ps1 copies those three.
- The talk program is ledger/TalkHelper, the C# Core's ConversationEngine. It is published as LedgerTalk.exe beside the game and needs no .NET.
- It calls Anthropic's Messages API directly. The key is read from `%LOCALAPPDATA%\LEDGER\live-talk-key.txt`, and only in a run somebody is playing (CrimeProbe.cpp:3218-3255).
- Models (ledger/Assets/Scripts/Core/LlmClient.cs:53-67):
  - claude-sonnet-5 for "real conversation" and claude-haiku-4-5 for small talk, chosen by the kind of moment (D48 as re-ruled on 1 October; TalkMoment.cs);
  - the claim check runs on Haiku 4.5;
  - prices in code: Sonnet 5 at $2/$10 and Haiku 4.5 at $1/$5 per million tokens (read 28 September).
- Around each reply:
  - a content rule (ContentRule/ContentWords), a SafetyRule and a real-world rule (RealWorld.cs: no real brands and nothing after 1992);
  - a claim check (ClaimCheck.cs): a second model lists every specific a line states, and the Core fails any specific with no source;
  - the first-week rule table and the "plain line" (on since 30 September);
  - grounding by code before writing (Bearing, 30 September);
  - fixed own-lines per card for a refusal.
- The first sentence is streamed (`--early`) and handed to the voice ahead of its check (`--pending`). It plays only if the checked words match.
- A plain first sentence ("Hang on, boss.") is spoken without waiting for its check (DEC:132).
- The AI notice is a card before the first conversation (DEC:213). R reports the last reply (CrimeProbe.cpp:3211).
- Suggested lines: on Tab with a keyboard, at once with a controller. Tom's written lines were approved 1 October; the small model writes the follow-ups.
- The threat read is a checking-model call beside the reply (DEC:150, DEC:140).

**Measured, with dates**

| What | Figure | Date and source |
|---|---|---|
| Enter to the words on screen, in the packaged game on LEDGER's key (30 lines; AI tester, `--real-talk`) | median 1.91 s, 1.12 to 3.79 s, 90th percentile 3.12 s | 30 Sep, production/playtest/real-talk-2026-09-30.md |
| Same run, Enter to first sound | median 5.41 s, 2.20 to 10.21 s; none of 30 within 2 s | same |
| Same run, fallbacks and timeouts | 29 own replies, 1 ended the conversation, 0 fell back, 0 timed out | same |
| Same run, cost | $0.2324 | same |
| Off-game sample with the check (24 turns, 103 calls) | first sentence passed at median 2.0 s; heard with `--early` at median 2.1 s, slowest 5.5 s; median 4.3 s to the whole reply; 2 fallbacks of 24 | 30 Sep, production/playtest/talk-cost-2026-09-30-after.md |
| Sheila's first sentence (first_token_sample) | Sonnet 5 median 1.43 s (cached 1.32 s; no gain); Haiku 4.5 0.81 s | 1 Oct, production/playtest/first-token-2026-10-01.md |
| Cost per turn (30 Sep sample) | $0.0179 | talk-cost-2026-09-30-after.md |
| Cost per hour of steady talk | $2.14 at 120 turns/h; $1.07 at 60; $3.22 at 180 | same |
| Earlier cost estimates | 23 Sep, before the claim check: 24 turns $0.126 (a fair amount of talk $0.31/h); the business research's placeholder was $0.14/h | production/research/talk-helper/cost-of-an-hour-2026-09-23.md; runtime-ai-business/SUMMARY.md |
| Where the bill goes (29 Sep, 24 turns, 123 calls, $0.3705) | input is 87% of it; Haiku input alone 64%; about 4.6 Haiku calls per turn (reply, first-sentence check, whole-reply check, second looks) | production/research/prompt-caching/NOTE-2026-09-29.md |
| Prompt caching | Haiku 4.5 caches nothing under 4,096 tokens, so its calls cannot be cached; expected saving about 11% of a session | same |
| "That's all I know" on a newcomer's 60 fixed questions | 36 of 60 (30 Sep morning), then a mean of 21.7. With the rule table on: 5 to 7 on the tuned sixty, 23 to 25 on a fresh sixty nobody tuned on (level with no table). The overview says "23 of 60 in its latest run" | production/research/grounded-replies/MEASURED-2026-09-30.md, RULES-2026-09-30.md; TOWN.md; FOR-JAFAR overview |
| Invented details the player would hear | 30% → 5% → 7% (16 of 240 held-back turns); the check flags 30% of honest replies | 28 Sep, FINDINGS; production/research/invented-claims/RESULTS-2026-09-28.md |
| Small talk ending in "That's as far as I can take you" | 13 to 15 of 36 | 29 Sep, FINDINGS |
| Logged spend on LEDGER's key (talk-runs.jsonl plus the measuring run) | 30 Sep: $0.3973 + $0.4288 + $0.2324 = about $1.06; 1 Oct: $0.0096 + $0.1689 | production/playtest/talk-runs.jsonl; real-talk-2026-09-30.md |

**What was tried and failed or set aside**
- Prompt-only fixes for the empty answers were set aside under the two-tries rule (DEC:132, DEC:163, DEC:169):
  - planning facts first: 18.3 against 21.7 of 60, no different;
  - a narrower second try: worse, 26.7;
  - the check's retune: three versions on 255 labelled details, none better.
- A reaction opener was left off (DEC:182): it became a verbal tic.
- Repairing flagged replies was dropped after it failed its independent check.
- The local model as router or writer (24 Sep, production/research/local-models/SUMMARY.md):
  - paid model 286 of 299, best free model 271 to 274 with worked examples;
  - free models obey most injected orders;
  - kept only as a "later" offline option (DEC:12);
  - the hardware-floor research estimates that game, voice and a local model do not fit 10 GB together.

**Open faults and audit findings still stuck**
- **A budget switches the claim check off.** Reported by the rulings sweep (1 Oct, "built against a ruling" 1), and confirmed still in the code at 79cf8db:
  - ledger/TalkHelper/Program.cs:273 attaches the checker only when the client is the plain `AnthropicClient` (or `CheckAlways`, true only in the size-logging fake mode);
  - Program.cs:1433-1444 wraps the client in `BudgetedClient` whenever `--budget-usd` or `LEDGER_TALK_BUDGET_USD` is set;
  - ConversationEngine.cs:1733 skips checking when there is no checker;
  - the AI tester's `--real-talk` (tools/ai-tester/play.py:426-428) and `tools/talk_cost_sample.py --live` (line 202) both set a budget.
- So the 30 September in-game measuring run, and any capped measuring run since, ran without the claim check. Its 1.91 s to the words is not the checked path.
- Jafar's own play sets no budget, so it is checked.
- Steam's approved disclosure says "every line is checked before you hear it" (production/store/steam-ai-disclosure.md). That is untrue for capped runs and for plain first sentences (DEC:132).
- **The action router is not in the game.** The router (IntentRouter.cs, "the paid router stays", DEC:12, DEC:22) and its prompt-injection block are C# Core only. A typed order reaches live talk, guarded only by a prompt line (rulings sweep TABLE lines 41-46, 104-110, 1902-1908, 2037-2038). No ruling retires it.
- FINDINGS:
  - the check does not read what a speaker says about Tom ("we've known each other a good while" passes);
  - the hours and alibi tests are word lists that leak;
  - beliefs made by reflection would count as known.
- The stock fallback "That's the whole of it. The rest would be gossip." can be a first reply that presumes earlier talk (FINDINGS; first-token-2026-10-01.md).
- Suspicion: the game's C++ port raises it, but talk reads the C# helper's number, and nothing in the game reads the port's (FINDINGS).
- D48: the rulings sweep found the model chosen by card (Sheila on Sonnet, Ron and Darren on Haiku). Re-ruled and changed by the town on 1 October (DEC:226/DEC:227). Not re-verified here in the packaged game.

**Offline behaviour**
- With no key, or no reply in 8 s, the character gives a brush-off line of its own, marked offline or timedOut (TalkHelper header).
- A played run without the key file logs "offline: no live-talk key file" (CrimeProbe.cpp:3290-3292).
- No local model fallback exists.

**What makes it hard under the constraints**
- Steady talk measured at $1.07 to $3.22 an hour (30 Sep). The key is held to about $1 a day for measurement runs and his live play together (DEC:257), so one hour of steady talk is one to three days of that allowance.
- At the relay's default per-copy allowance ($0.50 a day, $5 a month; DEC:118), $2.14/h buys about 14 minutes of steady talk a day. That is arithmetic from the records, not a measurement.
- The 24 September audit's business arithmetic ($17.49 net per sale) already failed at 16-63¢/h. The measured figure with checks is several times higher.
- The two-second target competes with the claim check, which costs about 1.1 s on the first sentence (TOWN.md item 3).
- Haiku 4.5 is promised no retirement before 15 Oct 2026 (prompt-caching note, read 29 Sep), but it carries all the checks.

**Reading.**
- Works: typed talk with three grounded characters in the packaged game, with notice, report key, content rules and a claim check on uncapped play.
- Unproven: the checked path's delay in the game; talk with anyone but three people; cost at the friends' build's real usage.
- Failed: the 2 s target; empty answers on unseen questions (about 40%); the claim check under a budget; the router never wired.

---

## 2. Voices (text to speech)

**In the game today**
- The engine is Chatterbox Nano (Resemble AI, MIT, weights included), run as a separate Python program, tools/voice-live/voice-server.py, beside the game.
  - Its token model runs on the graphics card through DirectML.
  - The decoder's heavy half has run on the card since 30 Sep (commit 6dff6b9: "0.7 s sooner").
  - Voices are learned once, on the processor, because DirectML aborts on complex numbers (FINDINGS).
  - It speaks whole sentences; streaming within a sentence is off by default (`LEDGER_VOICE_STREAM=1`).
- The cast's voices:
  - Ron: VCTK p227;
  - Darren: VCTK p241;
  - Sheila: VCTK p267 since 2 October (DEC:230; 12 test lines with no American reading; Jafar's note on p267: "sounds very flat, artificial", DEC:136).
- Thinking sounds ("Let me think.", "Well, now.") play at once to cover the wait: two each for Ron and Darren (DEC:84), and Sheila's two since 2 October.
- Mouths follow the voice's loudness (DEC:192). Jafar's no of 1 October: "the mouths only open and close with loudness; Sheila's mouth twists sideways with a seam across her cheek" (DEC:196). No commit since addresses the seam.
- Subtitles appear when their sound starts (commit 4d55809, 2 Oct).
- The man at the landing speaks words only: no voice is cast for him without Jafar's yes.
- For the friends' build, the game starts a "Voice" folder beside itself holding a portable Python, torch and weights (CrimeProbe.cpp:3405-3430; tools/voice-live/make_portable.py). The folder is built on F:. No record of a test in a fresh Windows account was found.

**Measured latency (the voice's share, after the words)**

| Date | What | Figure | Source |
|---|---|---|---|
| 24 Sep | Nano beside the game | 1.28 to 1.38 s of work per second of speech; alone 0.90 to 1.04 | production/research/nano-listening-test/card-timing-2026-09-24.md |
| 26 Sep | First sound in the game, the player's own path | 5.35 s median (slowest 8.7) | DEC:46 |
| 30 Sep | Real path (see area 1) | voice share median 3.66 s, 1.03 to 8.23 s | real-talk-2026-09-30.md |
| 1 Oct | Short line on the card | 3.95 → 2.98 s. Streaming in pieces, compiled step, frame caps, half resolution and priority all failed to help beside the game; every route ran at about half its idle speed | production/research/voice-latency/STREAMING-IN-GAME-2026-10-01.md |
| 2 Oct 14:00 | Whole voice beside the finished game, 8 lines each | card as today 3.66 s median (4.52 slowest); card with the game's texture pool capped at 600 MB 3.44 s (3.93); processor on four cores the game does not use 4.40 s (5.10) | production/research/voice-latency/EVIDENCE-2026-10-01.md |
| 2 Oct 20:20 | Token step quantised to 8 bits, processor, idle | 1.7× faster; scores shift up to 1.9, changing tokens; not yet heard, not yet timed beside the game | same |
| 3 Oct | Overview | "about 5.5 s from Enter to the first sound (not the real path end to end)" | FOR-JAFAR.md |

**Graphics memory (10 GB card)**
- Nano alone: 2.7 to 2.8 GB of the card plus about 1 GB shared.
- Beside the game it was given 1.40 GB of the card and 2.03 GB of shared system memory, and one run crashed in DirectML.
- The game: 4.8 to 6.1 GB; the card 7.7 to 9.3 GB in use (1-2 Oct, EVIDENCE-2026-10-01.md).
- Earlier figures: Nano 2.1 GB beside a 3.5 GB slice (24 Sep).
- Cause found: half of what the voice works on is pushed out of the card's own memory beside the game. Capping textures tripled the token rate but gained only 0.2 s on the median.

**Quality and accents**
- The accent checker is ruled "a screen, never a gate" (30 Sep). It still prints REJECT (tools/voice-live/take_gate.py:9,124), which the rulings sweep flagged as built against the ruling.
- The 30 September audit found the calibration rejects 24 of 50 genuine Scottish clips, and Darren's approved voice scores Scottish in 0 of 12 generated lines.
- FINDINGS:
  - Nano drifts American inside lines: Sheila's old voice D failed 4 of 7, and some of Ron's and Darren's acted takes;
  - the crowd's recorded lines drift American (Northern Irish man 20 of 25); five street lines are out of use;
  - no street voice rides on a cast MetaHuman yet.
- Ron's lines were judged "more lively" on Nano than Sopro ("very flat", DEC:183).
- Older voices are missing: Father Walsh's approved Irish voice is a 25-year-old against his 61 (DEC:90). Danny, June and Walsh get a listening page (DEC:261, 3 Oct; not yet made).
- The per-line emotion and paralinguistic tag steps ordered on 24 September were never built (rulings sweep #9; ROADMAP stage 2).

**Tried and set aside**
- Pocket TTS (2.0 s in the game, but American drift; three attempts, DEC:47, DEC:85).
- Sopro (2.0 s in play; Jafar finds Ron "flat").
- VoxCPM2 (Apache-2.0, needs about 8 GB, not beside the game; kept for some prepared lines, but Jafar picked Nano for Ron's threat, DEC:128).
- Paid streaming voices: researched (Inworld TTS-2 Flash about $0.28/h of play, production/research/live-speech-architecture/paid-voices-2026-09-28.md), then ruled out on money (DEC:105).
- Moving the voice into the game, the "proper conversion" to ONNX on the processor: estimated at about two working weeks (production/research/voice-in-the-game/SUMMARY.md). Jafar's condition, evidence that it shortens the delay (DEC:191), was not met by the processor route on 2 October. The 8-bit decoder test (NOW item 3, about two days) is the "last free test" and is queued after the 13-step proof view.

**Licences and consent** (detail in area 16)
- VCTK is CC BY 4.0. Personality rights are excluded by the licence; Jafar accepted consent as a stated risk on 24 Sep.
- The credit was added to the credits page on 2 Oct.
- Watermark: applied in the streamed path (voice-server.py:377). Not determined for the default whole-sentence path, which relies on the Nano package's own `generate()`. Lines made in advance are unmarked, and a failure to mark is silent (rulings sweep #27).

**Reading.**
- Works: three cast voices speaking live, locally, free, with thinking sounds and subtitles in sync.
- Unproven: the 8-bit decoder; the portable stopgap in a fresh account; accents by ear for the older cast.
- Failed: the 2 s target; every free speed route tried in the game; per-line emotion never built; Jafar finds the voices flat.

---

## 3. The simulation (perception, memory, gossip, schedules) and its C++ port

**What exists**
- The C# Core: 134 files, about 48,100 lines (ledger/Assets/Scripts/Core). It holds perception, memory, gossip, suspicion, PlayerIdentity, CastDay (40 people, 80 friendships, weekday routines; production/specs/hook-cast.json), arrangement, waiting, police, custody, the first week, week's end, town news, trust, silence, threats, claims, and much the game never reaches: Act II and III, endings, rivals, economy, combat, traffic, press and so on.
- The C++ port: about 11,900 lines across 29 headers in ue-probe/Source/LedgerProbe/Public. It covers Perception, Gossip, MemoryStore, Suspecting, Suspicion, CastDay, Schedule, Arrangement, Waiting, PoliceFile (with Custody), FirstWeek, TownWeek, TownRounds, TownSave, TownNews, WeeksEnd, Silence, StreetVoice, OwnLines, PlayerIdentity, DayOne and more.
- Not ported (grep of ue-probe/Source shows no use): Combat, Harm, Traffic, Trust, ActTwo, ActThree, Empire, Economy, Informing, Negotiation, Debts, IntentRouter, Campaign, Phones.
- **Comparison and tests**
  - Perception golden: 57,872 rows, 0 mismatches (production/d1-probe/ue-verdict.txt, 3 Oct).
  - CoreTests: 5,074 pass (commit d15ccd3, 1 Oct).
  - The 30 September audit reran 56,997 checks, 0 failures.
  - The independent review of 1 October: 57,864 compared rows agree. But one-line mutations of 12 new C++ lines all passed the comparison (FAULTS.md D1: TownNews.h, FirstWeek.h, CastDay.h, StreetVoice.h NamesHim, TownWeek.h TellDue). "Much of the new code is never reached by those rows."
  - The 30 September review found four faults written into the golden tables themselves (fixed 1 Oct).
- **In the game**
  - A running clock at two game minutes per real second, so a day is 12 real minutes (DEC:112).
  - The whole cast is in the gossip network by id.
  - Witnesses are measured where they stand, in that hour's light (DEC:178).
  - No talk through walls (DEC:181).
  - The three talkers have bodies. Everyone else counts only from behind their own shop window, with no body (DEC:178).
  - Mixamo walkers pace at a fixed 1.2 m/s, "seen and not simulated" (production/specs/street-people.json; rulings sweep #8, #17).

**Measured (Core, on paper)**
- News reach at 30 minutes of play, the 40-person cast (DEC:52): half-sure stories reach 0.52 to 0.63 people, sure ones 1.58 to 3.93.
- First hour (game-design/first-hour-2026-09-29.md): one of the day-one five says the night's story to Tom's face by minute 30 in 13 of 13 cases, but 7 only at minute 30 itself; in the coat, 6 of 13.
- These are the Core's figures, not measured in the game, and they assume Ada, June and others whom the game cannot yet show.

**Open and stuck**
- Rulings sweep (1 Oct), still not on a list or not built:
  - the street's people do not perceive or remember (#8);
  - nobody has their own nerve, loyalty or greed, and a reversed nerve rule remains in StreetVoice.cs:813 and StreetVoice.h:457 (#15; DEC:123);
  - town news is never loaded by the game (#21);
  - overheard gossip in free play is never voiced (#22);
  - the day-zero arrival is ported but only tests call it (#12; commit 4d55809 of 2 Oct does not list it).
- FINDINGS: three time-and-state faults in the police file wait for a detective's crime.
- Independent check of 1 October's port (d15ccd3): two Medium faults in the rules themselves were sent to the town for Monday ("a threat leaves the sighting of him free to spread; a threat filed before the ruling never gains its silence").

**Hard under the constraints.** The simulation is much deeper than what a player can reach. The adversarial audit (30 Sep): "the playable game is substantially shallower than the implemented simulation". Each new rule has to be built in C# by the town and ported to C++ by the builder. Two lanes feed one integration bottleneck (audit 30 Sep, finding 4).

**Reading.**
- Works: a deterministic, heavily tested Core and a faithful port of the first week's rules, golden-compared on every build.
- Unproven: that the comparison covers the new code (12 mutants survived); that the town visibly knows Tom in the game rather than on paper.
- Failed: per-person temperaments, town news, overheard gossip and the arrival, all built or ported but never reaching play.

---

## 4. The crime layer, police and arrest

**In the game.** One player crime: E at Rita's pawn-shop window breaks it (DEC:155). Around it:
- witnesses filed at the rung of identification Perception gives;
- the damage found;
- reports the next morning by the rules in DEC:95 and DEC:98, with Mickey's people never reporting (DEC:210, DEC:224);
- a constable at ten o'clock, shown as text captions ("A constable: ..."; "At the station: <rights>"; CrimeProbe.cpp:6280-6300), with hours in the cells passing;
- DS Ellis's visits from the street's talk, shown as captions and wait stops.
- Talk-side crimes and responses: asking someone to keep quiet (Silence.cs), threats (the ThreatRead model call), lies about where he was (Claims.cs), owning up.
- The arrangement: Ron brings the outfit's envelope at 20:00, and the man at the landing says his lines (words only).

**Not in the game**
- No constable or detective body ("NO CONSTABLE IN PLAY", rulings sweep #14).
- Owning up never earns the caution (#23).
- The coat (evidence, harder to recognise) is not built.
- The magistrates' court is set aside (DEC:127).
- The crime verbs owed by D56 are on ROADMAP stage 3 with their specifics, but unbuilt in the Core: order a man hurt, point a plan at a person, frame someone, lean on a witness, move a body, sanction crew, hit a rival's property, have someone vouch.
- Killing exists in the Core (Homicide.cs; the PoliceFile port reads its inquiry), but there is no way to kill in the game.

**Changing rulings.** Threats:
- "never buys silence" (DEC:140, 30 Sep);
- then "a threat talks a witness round" (1 Oct, built in d15ccd3);
- then "can stop a report but never the street's talk" (DEC:259, 3 Oct).
- N3 is to be redone by the town, then ported (production/drafts/rulings-2026-10-03/NOTES.md item 3). Not yet done.

**Reviews.**
- The 30 September review found "nobody can ever report him".
- The 1 October review confirmed reporting, recognition and the constable now work in code. It found N1 (High, a witness told she knew nothing) and N2 (High, "Nowak" named before anyone knew it), both fixed 1 October (a0a0891; town commit 7f7ed78).

**Reading.**
- Works: one witnessed crime leading through gossip and reports to an arrest, all as text.
- Unproven: the police beats played in a full week by a person; the threat ruling of 3 October.
- Failed or absent: every crime verb but one; police with bodies; the coat; killing in play.

---

## 5. Combat (fists, improvised weapons)

- **In the game: nothing.** No Combat, Harm or Arsenal code in ue-probe/Source. `Observe.DeedFor` "needs Arsenal and Weapon, neither of which is ported" (CrimeProbe.h:388; Observation.h:16).
- **In the C# Core** (production/research/crime-and-combat-coverage/SUMMARY.md, 19 Sep): fists, improvised weapons, carried weapons that can be spotted, lingering injuries, witnesses. Three gaps: being outnumbered, running away, and police arriving mid-fight.
- **Rulings.**
  - G3, fists and improvised weapons, is ruled "in" (23 Sep).
  - D24 says fighting "may exist and must not look broken", with the smallest budget.
  - The rulings sweep (#19) found it on no list. ROADMAP stage 3 now carries "combat's three gaps" and the genre items.
- No combat animation, hit reaction or contact work exists in the Unreal project.
- The poses ruling of 3 Oct limits sources to MetaHuman's own clips and Mixamo.

**Reading.**
- Works: nothing in the game.
- Unproven: everything (C# only).
- Failed: not attempted in Unreal.

---

## 6. The first week's designed content against what is built and playable

**Designed** (game-design/, approved or "settled as written", DEC:125): the first hour, day one, day three, the first ask, the landing, Ellis, arrest and its words, threats, waiting, the week's end, Sheila's trust, what they call him, the warehouse fire, town news, the ending's signs (deferred, DEC:158), and the story outline (approved 28 Sep).

**Built and walked in the packaged game** (records, not verified here)
- A new game on day 0 at nine (CrimeProbe.cpp, free play).
- Sheila's walk-round as plain text, then hints and the errand (DEC:135).
- The running clock and Z to wait hour by hour, stopping for Ron's envelope, the landing, Ada's tea, the constable, Ellis, Sheila's question and his release (DEC:109; review runs, production/playtest/review-runs-2026-09-30.md).
- Rita's window, witnesses and the arrest as text.
- Ada's tea: standing on her step between 21:00 and 23:00; she has no body (CrimeProbe.cpp:6440-6457).
- Sheila's week's-end question, with Monday as fallback.
- Live talk with three people, with suggested lines.
- The scripted route walk: 11 of 11 stages pass (production/playtest/route-walk/2026-10-01-0654/verdict.json: new game, talk to Sheila, typed talk does not move Tom, reply words, the deed, onlookers, a wait from 13:28 to 20:00, save, quit, relaunch, continue within 0.00 m). It uses stand-in talk.

**Not built or not reachable**
- No talk cards for anyone but three people. Ada, June, Alison, Walsh, Ellis and the landing man cannot be talked to. Walsh's and June's approved street lines can never be heard (rulings sweep #37).
- Mickey's office is not enterable: only a spec (production/specs/mickeys-office.json; "kept for later", DEC:202).
- Not built: the Ledger notebook ("not in this build yet", DEC:209), the coat, the arrival at day 0 (#12), town news (#21), and the warehouse-fire thread through Alison (she has no card or body).
- The thirty regulars are written but not in the game (#35).
- Acts II and III, the rivals and the endings: C# only (#20).
- The player character is a Mixamo-derived stand-in (tom-player.glb, "the man in the grey tracksuit"; SliceCharacter.cpp:36). The street's remaining figures (Martha, Kate, Leonard) are Mixamo placeholders (FINDINGS).

**How much of thirty minutes exists.** Not measured.
- No record exists of a 30-minute session played by a person or by the AI tester on the real talk path.
- The first-hour design packs day 1 to day 3 into 36 minutes at 12 real minutes a game day. Its "it comes back" beat depends on the day-one five, two of whom (Ada, June) have no body or talk in the game.
- The visual side, which gates the friends' build (DEC:222), is at item 2.1 of 13: composition failed two fresh reviews (NOW STATE, 3 Oct). Jafar answered no to all four looks on 1 October (DEC:196). The seven new shopfronts failed their fresh review (FOR-JAFAR, Builder 3 Oct).

**Reading.**
- Works: one continuous route through day 0 (deed, consequence, wait, save and reload), walked by script.
- Unproven: any 30-minute session; "the town visibly knows them" in the game.
- Failed or absent: most of the first hour's people, the office, the Ledger and the coat.

---

## 7. Save and load

**In the game**
- One town save (TownSave, town.json) plus the talk saved beside it as `.talk.json`. The talk program refuses any other suffix: that once silently lost every conversation (production/playtest/review-runs-2026-09-30.md).
- Autosave on the hour after talk. Continue from the title. Quit to title restarts the game from its own command line (DEC:209).
- Saves now carry the build's commit (CrimeProbe.h:1801-1813, fix for review S5).

**Measured**
- Route walk on 1 October: continue at the saved point, 0.00 m off.
- The 1 October review: "a reload at any point of the week gives the same week as playing straight through", run at 311 points. That ran in the Core and port code, not the package.
- The build machine's encounter-reload verdict: PASS on 5db99d5 (3 Oct).

**Open (review of 1 Oct, Low)**
- A failed or unfinished talk save still loses every conversation.
- Where people stand is not saved.
- Two late replies in a row lose the first.
- The town's "Remaining save items" (C5) were listed as remaining on 30 Sep. Not determined which are fixed.

**Reading.**
- Works: quit, relaunch and continue, with town and talk restored, scripted and repeated.
- Unproven: saves across builds in a friend's session; Shipping's save path.
- Failed: none open above Low.

---

## 8. The interface, controls and controller

**In the game** (commits 01b9c8f, 3e693da and 318d9dc, 1 Oct; production/design/ui)
- The approved "evening paper" look, built in Slate as drawn, on every screen:
  - a title with New, Continue and Quit;
  - loading with progress;
  - settings: presets with Detect, sound, controls, subtitles and reading, reduce motion;
  - a pause page;
  - subtitles at most two lines;
  - the talk "coupon";
  - prompts on people and the window;
  - the FIRST STEPS slip;
  - the AI notice card;
  - suggested lines;
  - four synthesised interface sounds ("not yet heard by anyone").
- Credits page (2 Oct).
- Keyboard and mouse.
- Controller: left stick walks, right stick looks, A talks or uses, Start pauses, round-button prompts. Checked by `-PadShot`: the stick walked Tom 152-153 cm and turned the view 72-74°.
- Steam's floating keyboard is not used outside Steam.
- Microphone: later (DEC:208).
- Fixed 2 Oct (0f02a55): Q from the pause page did not quit.

**Open**
- The Ledger notebook and the paper map are absent.
- Text is held in the C++ and C# source, not in tables for translation (#44).
- The interface's "finish" (scanned paper, KCD2 comparison) waits.
- The game has run at 3440×1440 and 1920×1080. Its frames read as first person on the design page because no Tom is visible (README); that is the camera, not the interface.

**Reading.**
- Works: the full menu, talk and settings set, with controller support, filmed at both screen sizes.
- Unproven: friends' first use without help; the sounds by ear.
- Failed: nothing recorded.

---

## 9. Sound, ambience and foley (CC0 only)

**In the game**
- One ambience bed: "traffic-distant", generated from noise, positional (production/specs/street-sounds.json; production/assets/sounds holds one file).
- Tom's footsteps: 16 cuts from two CC0 recordings, sturmankin on Freesound and Joseph Sardin on BigSoundBank (DEC:133; THIRD-PARTY.md). Two earlier CC0 sets failed review.
- Six crowd voices' pre-voiced street lines (VCTK clones, made by the old Unity pipeline); five lines are out of use for American drift.
- One shout cue, from a crowd voice.
- The interface's synthesised sounds.
- Positional sound proved 23 Sep (A28.01/02 done).

**Not in the game** (checklist sweep production/research/checklist-sweep-2026-09-29/BUILDER.md marks them "later")
- Ambient sound for street and office (A25.02).
- Rain and wind.
- Traffic engines (no traffic exists).
- Moving sources carrying sound; the office's muffling.
- Physical reactions with matching sound: the broken window's sound against its remnants (A12.15).
- Music: the radio and the Core's MusicModel are not in Unreal.
- Nothing records that a glass-break sound plays on the smash. Not determined.

**Reading.**
- Works: positional sound, footsteps and a traffic bed.
- Unproven: everything else.
- Failed: no CC0 ambience or foley library has been brought in beyond the footsteps. The street is near-silent, the audit table of 24 Sep notes the same, and it is still true by the records.

---

## 10. The AI tester and the packaged build's testing

**What exists**
- tools/ai-tester/play.py: the Claude Code session itself plays through screenshots and real key presses (DEC:99). It never reads the key; talk runs as the stand-in except the one `--real-talk` run.
  - It refuses while the PC was used in the last two minutes and waits for the build machine's game.
  - It runs at 1280×720, windowed.
- tools/route_walk.py: a fixed script with no model, 11 stages with real key presses. The last committed verdicts are five runs on 1 October (05:51 to 06:54), all 11/11.
- On 2 October two walks failed the quit stage (fixed in 0f02a55). One walk's steering caught Tom at the kerb for five game hours (commit 0f02a55 message).
- Build-machine checks on every Unreal-touching push, all PASS on 5db99d5 (3 Oct): perception golden, crime probe, encounter play / live (stand-in talk, `talkFake=yes`) / reload / unseen, walk and slice walk, shots, and a performance capture.
- AI tester free play (30 Sep and 1 Oct) found:
  - the quay almost black at night;
  - the pavement at Rita's trapping Tom;
  - the fish market's crate walling the pavement;
  - Mixamo's "Michelle" standing by the fish market at night.
  These are in FINDINGS. The pictures are on his PC only.

**Gaps**
- Everything runs on the Development package. No Shipping build exists: `-clientconfig=Development` (.github/workflows/ledger-probe-unreal.yml:555). The 30 September audit asked for a Shipping release walked 30 minutes in a fresh Windows account; not done.
- The tester cannot judge live talk: stand-in only. The one real run ran without the claim check (area 1).
- The nightly "does the town know Tom" report, ruled 3 October (DEC:256), was "to set up on 3 October" (NOW.md). The overview at 12:15 says it is the current item. No schedule for a nightly tester walk exists in the repository. The only scheduled task found is retention at 04:30.
- PC lock stops key presses (production/research/packaged-game-testing/SUMMARY.md).
- At two game minutes per real second, the tester's thinking time lets the clock run on.
- Twelve surviving mutants (area 3).
- tools/approvals.py, run read-only today: "placedInGame=8 placedWithoutCurrentApproval=8". Every placed thing (the three cast, witness lines, look, pieces, sounds, window interiors) lacks a current approval record (rulings sweep "built against" #10, still so).
- Performance: the per-build capture is the old slice standing still, drawn at half size and upscaled: 75.1 fps median, worst frame 19.6 ms, card 3,681 MB (ue-perf-verdict.txt, 3 Oct). Its voice line still reports the 24 September measurement. The packaged game at Highest at 3440×1440 took "about 26 ms of card time a frame" (30 Sep, STREAMING-IN-GAME note). The rulings sweep (#26) found no current measurement of the real street with the voice.

**Reading.**
- Works: scripted packaged walks with real inputs; deterministic build checks; screenshot-driven free play.
- Unproven: Shipping; the fresh account; nightly cadence; real-talk testing with the check on; frame rate of the real street with the voice.
- Failed: none of the scripted checks is red today; the approval flags are all unresolved.

---

## 11. The friends' build

**Ruled**
- Friends play on Jafar's PC, from a shortcut, in a fresh Windows account, with no relay and no sent copies (DEC:200).
- It waits until the proof view has passed his eye and the street-wide pass is done (DEC:222). It is NOW item 5, last.
- It must have the "twenty basics" (production/research/checklist-sweep-2026-09-29/BUILDER.md) and "no placeholder anywhere a friend can look" (DEC:201).

**Status of the twenty, from records only** (not verified in play)

| Status | Basics |
|---|---|
| Done or present | title (5); first purpose, the walk-round (6); hints (7); prompts (8); typing never walks Tom (9); Sheila has a voice (11); footsteps (18); pause (19); autosave (20); quality presets and Detect (4); a resolution held at 60 (3, commit 1d74cf3) |
| Partly | people turn toward the smash (16: walkers within 35 m gather; "two came in the film") |
| Not met | a reply heard soon enough (10: 5.4 s); lips in time (12: Jafar's no); people walking routines (13); Mickey's office enterable (14); camera never through a wall (15: no interior to test); believable smashed window (17: FINDINGS) |
| Unproven | shortcut start with talk and voice inside (1); shader-compile progress (2) |

**Hard parts found in code and records**
- **The key's location.** The game reads `%LOCALAPPDATA%\LEDGER\live-talk-key.txt` (CrimeProbe.cpp:3248). A fresh Windows account has its own LOCALAPPDATA, so without the file placed there the talk runs "offline". This is inferred from the code; no record addresses it.
- **The voice stopgap** is a portable Python, torch and weights folder (size not recorded in the repository). Not recorded as tested in a fresh account.
- **Shipping.** Packaging is Development; no Shipping build has been made.
- **The account.** An earlier NOW line recorded the build "waits on his fresh Windows account and room on F:" (rulings sweep TABLE lines 1222 and 2779).
- **Cost.** The friends' talk runs on LEDGER's key. A 30-minute session at the measured $1.07 to $2.14/h is $0.50 to $1.07, against the key's about-$1-a-day rule (DEC:257 covers "his live play" and measurement runs). Whether friends' play counts under that dollar is not ruled.

**Reading.**
- Works: the pieces (package, talk program beside it, voice-folder code, title, settings).
- Unproven: a fresh-account start; Shipping; a 30-minute session.
- Failed: six of the twenty basics not met by the records; the visual bar it waits on is at step 2.1 of 13.

---

## 12. The relay server (for later)

**Built: ledger/Relay** (ASP.NET Core, MIT; DEC:56, 28 Sep)
- Copy codes kept only as hashes.
- Per-copy allowance $0.50 a day and $5 a month (DEC:118).
- The model is chosen by role.
- Replies capped (core 400 tokens, ambient 1,000).
- A month budget, with a stop at 80% of it. The default `MonthBudgetUsd = 400` in code (Relay.cs); Jafar is to set the real value.
- Logs sizes and costs, never words. Keeps reports.
- Self-test: 21 of 21 against a stand-in provider.

**Not hosted.**
- It goes "first on his existing Hetzner server" once friends test remotely (DEC:65).
- Friends' talk through it gets no key yet (DEC:110).
- The privacy notice is to be drafted before any friend plays through it (DEC:115; rulings sweep #42, on no list).

**Stuck.** The relay admits only three system-prompt openings (Relay.cs, SystemShapes). It would refuse two of today's live calls:
- suggested lines, whose prompt opens "You suggest what Tom Nowak could say next" (Suggest.cs:66);
- the threat read, which opens "You read one line a man says" (ThreatRead.cs:23).

The rulings sweep found this on 1 October; it is still so in the code.

**Missing.** Steam ownership authentication (researched in production/research/runtime-ai-business/notes/plumbing.md, not built). The game holds no relay URL by default.

**Reading.**
- Works: a tested relay against a stand-in.
- Unproven: hosting, real traffic, Steam login.
- Failed: it rejects two of the game's five live call kinds.

---

## 13. Disk space, retention and git size

**Disk**
- 3 Oct 12:10 (overview): C: 85 GB free, F: 40 GB free.
- The build machine's own probe at 10:03 UTC the same day read F: as 27.0 GB free of about 111 GB (production/d1-probe/ue-machine.txt). Its other figures: C: 86.8 GB free of about 930; D: 0.1, E: 9.6 and G: 1.5 GB free. Those are not the project's drives.
- F: is small: about 111 GB in all. It holds bodies, garments, renders, voice graphs, the played copy, models, approvals, Unreal's 6 GB cache, the voice-portable folder and the 14.5 GB NoAI quarantine.
- Incidents:
  - C: reached 0 bytes on the night of 1 October and the build machine's runner crashed (CLAUDE.md; tools/retention.py header);
  - F: fell to 2.4 GB the same night;
  - C: dipped below 60 GB on 1 and 2 October (FOR-JAFAR summaries);
  - 47 GB was deleted on his yes on 2 Oct, F: going from 2.5 to 37 GB (commit 27a3d98).

**Retention** (DEC:231, 2 Oct)
- tools/retention.py runs nightly at 04:30 via Windows Task Scheduler, with limits in production/retention.json.
- A free-space check before every job: C: keeps 40 GB, F: 20 GB.
- Waiting on him: deletion of the 14.5 GB quarantine (Needs you 2).

**Git**
- GitHub reports the repository at 32,460,361 KB, about 32.5 GB (`gh api repos/jsab258/ledger`, today). It is public (`"private": false`).
- 30.6 GB of that is the build machine's test pictures, committed on every run from 22 September to 3 October.
- Stopped 3 Oct: the build machine now commits text verdicts only, and tools/git-size-guard.py runs in a shared pre-commit hook (DEC:247).
- Rewriting history to about 5 GB waits on his answer (Needs you 1).
- Still in git by design: what the build reads (production/assets, Unreal content, fonts, the Hook sheet).

**Rulings sweep, still stuck.** tools/cleanup.py still lists production/playtest, which holds tracked records, among its deletable places (cleanup.py:45).

**Reading.**
- Works: nightly retention and pre-job space checks, as of 2 Oct.
- Unproven: retention over a full week; F: under sustained renders.
- Failed: a 32.5 GB public history (GitHub advises under 10 GB, per the overview); two disk-full nights before the rule.

---

## 14. The build machine and the Unreal build in CI

**Setup**
- A self-hosted GitHub Actions runner, "ledger-pc", on Jafar's own PC.
- It shares the RX 6700 and the disks with the builder session, the AI tester and the voice.
- .github/workflows/ledger-probe-unreal.yml (3,131 lines) runs on every push touching ue-probe/, tools/ue/, TalkHelper, the Core, production/specs, production/assets/{street,people,vehicles,sounds,steps} or tools/runner.
- Concurrency: one running, the newest waiting (since 29 Sep, when "eight or more stood queued" at night).
- Core tests (ledger-core-tests.yml) and the fake-mode AI playtest (ledger-ai-playtest.yml) run on GitHub-hosted Ubuntu. The latter's live mode ran 46 times on 28-29 Sep on a key before it was removed (DEC:99; adversarial audit).

**Measured**
- The 3 Oct run on 5db99d5 took about 30 minutes, 10:03 to 10:34 UTC (probe timestamps). Cold build 3.02 min, editor build 3.23 min.
- Earlier runs were "about forty minutes" (workflow comment, 29 Sep).
- Every verdict file is PASS on 5db99d5.
- `materialCompile=UNPROVEN` remains in ue-build.txt.

**Failures recorded**
- The runner crashed when C: filled (1 Oct).
- ConflictingInstance failures when two Unreal builds overlapped (28 Sep, DEC:60).
- One scripted reload run ended with no verdict (cf76e4d, FINDINGS).
- All packages stamped SHA-UNKNOWN until the 1 October fix.
- The 24 September audit measured about two-thirds of a sitting spent in runner round trips.

**Under the constraints**
- Free in money.
- Costs graphics-card time and disk on the one PC.
- A push that touches specs or assets starts about 30-40 minutes of Unreal work that the AI tester must wait out.
- Packaging is Development only.

**Reading.**
- Works: an Unreal build and packaged checks on every relevant push, all green today.
- Unproven: a Shipping package; the build machine's load beside a night of tester runs.
- Failed: the 30.6 GB of committed pictures; past disk-full crashes.

---

## 15. The agent workflow itself

**Shape.** Three local sessions on one PC (CLAUDE.md):
- the builder (main, Unreal, graphics card);
- the town (worktree ledger-town, the Core and talk);
- clothing (Blender).

Plus cloud sessions for research, independent reviews, audits and the rulings sweep, merged by pull request. Handovers are single lines in NOW.md. One /goal runs to Sunday 20:00 (DEC:49).

**Volume and overhead (counted)**
- Commits: 1,172 on main from 20 to 30 Sep (245 of them probe returns), plus 105 from 1 to 3 Oct (22 probe returns). Peak: 387 commits on 23 Sep.
- 109 research topic folders and 260 research notes in production/research/.
- 26 approval-page folders from 25 Sep to 2 Oct (production/approvals).
- DECISIONS.md, 24 Sep to 3 Oct: 255 entries, 133 of them Jafar's (about 13 a day; 38 on 29 Sep), 40 "Claude, his to overturn" and 82 other.
- Record sizes today: CLAUDE.md 4,372 words (the 24 Sep effort audit targeted ≤600); DECISIONS.md 24,854; NOW.md 3,307; THIRD-PARTY.md 5,027.
- Draft caps of 1,000, 2,500, 200 and 300 words are waiting to be applied (production/drafts/rulings-2026-10-03/NOTES.md).
- The audits found:
  - 35% of commits records-only (24 Sep);
  - NOW and TOWN at about 20,477 words (30 Sep);
  - of 440 rulings, 19 built nowhere and 79 only partly (rulings sweep, 1 Oct).

**Priority churn**
- The builder's order was replaced six times in four days: DEC:154 and DEC:174 (30 Sep); DEC:202, DEC:212 and DEC:222 (1 Oct); DEC:244 (3 Oct, "we have been jumping between a dozen things").
- Reversals:
  - Marvelous Designer: no (30 Sep), in (1 Oct), out (2 Oct);
  - the Game Animation Sample: allowed (30 Sep), out as NoAI (3 Oct);
  - Megascans: requested (1 Oct), out (3 Oct);
  - Epic's garments: the stopgap, then removed with 14.5 GB quarantined (3 Oct);
  - threats: three rulings in four days.

**Past the two-tries rule** (named in records)
- the jacket's 14 overnight rounds (29 Sep);
- the Marvelous jacket ("nine drapes", failed on cut and lapel, 2 Oct);
- Sheila's and Darren's faces S1 to S4;
- hair curls (3 tries);
- spare body builds (3);
- Pocket TTS (3);
- the claim check's retune (3);
- the street lines (fourth try);
- Tom's written lines (third review);
- the voice delay (set aside 1 Oct, reopened as item 3);
- the hill's mist (FINDINGS);
- proof-view composition 2.1 (two failed reviews; research before a third).

**Owner's time and attention**
- He answers from his phone. Pages are capped at three decisions.
- His picks were read late: seven hours on 29 Sep; answered taps listed as waiting on 30 Sep (CLAUDE.md).
- The page recommended yes to four looks he rejected (1 Oct, DEC:196).
- Friday's page carried a test chart and black squares (DEC:235).
- Today's overview carries three "Needs you" items (git history clean; NoAI deletion; "Help improve Claude").
- FOR-JAFAR.md holds no town summary dated 3 October (the latest is "Town, 2 October", written 1 Oct 21:15). A stale "26 September, day" summary is still in the file.

**Research loops**
- Cloud research repeatedly could not reach primary sources: arXiv, Hugging Face, Edinburgh's VCTK page, Fab, Sketchfab, Steam, the Unreal EULA, Adobe's Mixamo FAQ.
- This led to the "unreached source is never evidence" rule (2 Oct). The free-garments research had to be redone from the PC (DEC:241).
- Clothing had 17 research notes by 30 Sep while the method was unresolved (adversarial audit).

**Where the work queues**
- The builder owns 17 of the twenty basics plus every port. Town and clothing feed it (adversarial audit, finding 4).
- The 3 Oct list puts 13 visual steps, each with a fresh review, before the voice test, the street-wide pass and the friends' build.
- The goal ends Sunday 4 Oct 20:00.

**Reading.**
- Works: independent reviews and audits that find real faults; deterministic tests; written rulings.
- Unproven: whether one ordered list holds for a week.
- Failed: records outgrowing their caps; rulings not becoming work (19 nowhere); repeated priority resets; work redone after licence reversals; the two-tries rule exceeded repeatedly.

---

## 16. Legal

### Unreal Engine EULA and MetaHumans
- Unreal 5.8. The credit notice is on the credits page (THIRD-PARTY.md; production/specs/credits.json, 2 Oct).
- MetaHumans are made in the engine's own MetaHuman Creator, not on Fab.
- The EULA text was **unreached** by the asset-plan research. Its AI clause is cited from search summaries [SS, note 27]: no use "to build or enhance any database or training or testing any artificial intelligence...", while AI workflows are allowed (production/research/asset-plan/0-SOURCES-AND-LICENCES.md lines 90, 177).
- Ruled 3 Oct (DEC:262): training-only clauses do not rule an asset out "while nothing we send trains a model". Jafar "is switching off 'Help improve Claude'". The overview still lists it under Needs you (item 3), so this is not confirmed done.
- MetaHuman files are kept out of the repository "because the repository is public" (DEC:14), backed up to Dropbox.
- Epic's MetaHuman garment packs, the Game Animation Sample and Megascans are all NoAI on Fab: 42 of 42 listings read from the PC, "Allows usage with AI: No" (production/specs/fab-noai-check-2026-10-03.md). Removed 3 Oct.
- Every MetaHuman-compatible Fab listing is NoAI automatically [READ, Epic docs], so no Fab garment can ever be used.
- Allowlist SHIP-SAFE 8 still admits the Game Animation Sample, and entry 3 says MetaHuman is "usable outside Unreal". Both are stale against 3 Oct, by reading ledger-v2/research/license-allowlist.md.

### Mixamo
- In use: the player body (tom-player.glb), the street's placeholder figures, and 41 clips plus X/Y Bot in the old Unity tree (THIRD-PARTY.md).
- Allowed by D46. The terms carry a training-only clause [SS]; Adobe's FAQ is **unreached**.
- Now one of only two pose sources (DEC:252).

### VCTK voices and consent
- CC BY 4.0. Edinburgh's licence and README were read 23 Sep (VOICE-PERMISSIONS-2026-09-24.md). Section 2(b)(1) excludes publicity and personality rights.
- What the speakers signed is unpublished. Jafar accepted consent "as a stated risk" (24 Sep, DEC:13); no email to Edinburgh.
- The corpus terms forbid identifying speakers.
- The credit, with creators, DOI, licence and a modification note, is now on the credits page and staged with the game (2 Oct).
- The four August voices' records are weaker.
- OpenSLR SLR83 (CC BY-SA) voices are listening candidates only; the ShareAlike question is a stated risk.
- Paid voice services would need speaker consent the recordings lack (paid-voices note, 28 Sep).

### The text-to-speech model's licence
- Chatterbox (all sizes) and the Perth watermarker: MIT, weights included (voice-in-the-game research, 30 Sep).
- THIRD-PARTY.md has no row naming the shipped voice engine (Nano), its runtimes (PyTorch, ONNX Runtime/DirectML) or the portable Python bundle the stopgap would ship. DirectML's redistribution terms are listed as unverified in the voice-in-the-game research.
- The watermark rule ("keep watermark") is only partly met (area 2).
- The banned TTS models (XTTS-v2, F5-TTS) are listed in NEVER SHIP.

### The language model provider's terms
- Anthropic's Commercial Terms, opened 24 Sep (production/research/runtime-ai-business/notes/plumbing.md:17): "use the Services ... to power products ... to its own customers and end users". The customer is responsible for users following the Usage Policy, and may not resell.
- Retention, from the Privacy Center (read 28 Sep): API inputs and outputs deleted within 30 days; kept up to 2 years if flagged; no training by default.
- The notice text in AiNotice.cs says this (DEC:80).
- Open, not decided:
  - an EU or UK representative (GDPR Art. 27);
  - the Swiss FADP Art. 19 country naming;
  - a full privacy notice (drafted "before any friend plays through our server", on no list, rulings sweep #42).
- Anthropic's minors guidelines were seen as a search snippet only.
- The allowlist has no entry for a language model (llm-inference-economics research). Still true by reading the allowlist.
- The provider's org spend cap tiers start at $500 a month; at the cap every call fails until the 1st (plumbing note:44).

### Steam's AI disclosure
- Researched 29 Sep. The survey form itself was **unreached** (it needs a sign-in).
- The draft was approved as drafted on 30 Sep (DEC:143; production/store/steam-ai-disclosure.md.approval.json).
- Its text claims:
  - "every line is checked before you hear it": not true of capped runs or plain first sentences;
  - talk goes "through LEDGER's own server": not hosted.
- Some survey answers lock at approval.
- No Steam page exists.
- The trademark check on the name LEDGER is deferred until before any Steam page (production/design/ui/README.md).
- The research's suggestion "never ask for a player's own key" conflicts with the business direction's later own-key mode (DEC:10). Not reconciled.

### Real names and brands
- Canon: every brand, vehicle and product is fictional; no real people, voices, logos or car models.
- Live talk's RealWorld rule asks again on a real name (DEC:72).
- Owed by the brand bible:
  - the football club, local paper, pirate radio, TV channel, kiosk operator mark and postal cypher;
  - the names the asset plan needs (car makers, police force and others), to be minted by the town on Monday 5 Oct (DEC:255).
- Still in content/brands/brand-bible-v1.json:11: "MICKEY'S IS A PUB AND STAYS A PUB" (against D19; rulings sweep #24; NOW 2.6, fault 3).
- tools/names-gate.py does not know the retired name "Emil" (sweep, still so).
- The phone box is modelled on the real KX100's drawings, with a made-up mark not yet made (DEC:131, DEC:239).
- The repository is public and holds KCD2 and GTA V screenshots as references (production/reference/, game-design/reference/). THIRD-PARTY.md calls them "not redistributed", which a public repository contradicts. That is an inference from the GitHub API's `private:false`; not researched in the repository.

### The content rule
- Canon D18: no alcohol, gambling or children; tobacco allowed.
- `tools/content-gate.py --enforceable`, run today: 8 of 20 clauses enforced mechanically.
- Live talk checks every line (ContentRule, SafetyRule).
- Still stuck:
  - the word and era gates skip the talk cards that go into every live prompt (rulings sweep #38);
  - the animation check walks the old Unity library, not the game's clips (#38);
  - a back-bar picture (`decal_05_interior_bar_back`) is still in the fallback street spec (production/specs/vignette-pieces.json:653), unread by the content gate;
  - the 3 September sign batch's worded pictures, some breaking the rule, are still to be retired (NOW 2.6, fault 2).
- The newsagent's stock leaves out pools coupons (DEC:243).

**Reading (legal).**
- Works: VCTK credit shipped; NoAI material removed and quarantined; the AI notice and report key in the game; the content rule on live lines.
- Unproven: the Unreal EULA and Mixamo terms, both unreached and resting on search summaries; VCTK speaker consent; Steam's survey wording; the privacy obligations for a Swiss seller.
- Failed or stale: the allowlist entries for MetaHuman and the animation sample; the brand bible's pub line; the disclosure's claims; no LLM or voice-runtime licence rows.

---

## 17. What could not be determined

- How long a friend's 30-minute session actually holds content, and whether the town is seen to know them in the game: no record of a 30-minute session exists.
- The voice's quality by ear, and Jafar's current verdicts on his pages: private, not read.
- Whether the watermark is applied on the default (whole-sentence) voice path.
- The real cost per hour of a friend's play (only scripted 24-turn samples exist), and the key's monthly cap amount: no figure in the repository.
- Whether a glass-break sound plays on the smash.
- The size of the portable voice folder, and whether it starts in a fresh Windows account.
- Frame rate of today's street with the cast and voice at his screen size: the per-build capture measures the old slice.
- Whether the town session wrote a 3 October summary anywhere but main.
- Whether the "Help improve Claude" switch has been turned off.
- Whether the 1 October review's remaining Low save items (C5) are fixed.
- The F: free-space discrepancy on 3 Oct: 27.0 GB (probe at 10:03 UTC) against 40 GB (overview, 12:10).
