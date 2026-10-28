# Study 3: Dialogue and barks (28 October 2026)

How Kingdom Come: Deliverance II and Mafia: The Old Country store, trigger, vary and stage what people say, from conversations to lines said in passing (barks). Read from their files and Warhorse's public wiki, not their code; no game text quoted; raw counts in the session's temporary folder on C: (F: is full). Read 28 October 2026. Tags: **M** measured, **R** read in a file or the wiki, **I** inferred, **N** a name only.

**The short answer.** Kingdom Come II writes a town that answers the player: 138,000 lines, a third said in the street, each crowd line recorded by four or five voices, picked by what the speaker thinks of him (reputation, anger, renown, his looks) and held back by cooldowns street-wide and per person. Mafia writes a story with a thin street: about 12,600 voiced lines, half of them barks; each of its 14 crowd voices has 2 lines per situation (3 or 4 for greetings and bumps), about 73 in all. LEDGER's written street already varies more per situation than either (I); what it lacks is situations: greeting him by regard and appearance, bumping, neighbours greeting each other, talking to oneself at work, rain.

## The numbers

| | Kingdom Come II | Mafia | LEDGER |
|---|---|---|---|
| Spoken lines written | 137,969 (M) | 5,690 exported of 12,558 voiced (M) | 491 shared, 217 own; live talk |
| Voice files | 280,343 English (M) | 5,901 scripted, 6,657 systemic events (M) | a clip per voice and text |
| The player's share | 30% (M) | 24% of exported (M) | suggested lines only |
| Lines per one-voice role | median 9, p75 31, p90 89; 15 over 500 (M; rule below) | median 25; 12 with 100 or more (M) | Ron 159, Darren 33, Father Walsh 17, June 8 |
| Voices | 84 with 100 or more files, 71 with over 1,000 (M) | 49 in barks: 14 civilian, 12 enemy (M) | 6 crowd, plus the cast |
| Lines per crowd voice | median 1,663 street, 1,191 quest (M) | median 73 over about 33 situations (M) | the shared banks |
| Variants per situation | pool median 5, each voice records 2 (M) | per voice: civilians 2 (greeting, bumping 3 to 4), enemies 3 (M) | 14 everyday, 6 per event |
| Wait before a street line returns | median 32 s; crime 20 to 40 s; gossip 10 min; self-talk 15 min (M) | mission barks 7 to 10 s (R); the rest not exported | 45 s floor |
| Words per line (median) | street 7, conversation 12, player 8 (M) | 7 (M) | shared 7 (M) |
| Seconds per line (median) | street 3.6, conversation 4.3 (R field, I meaning) | 2.5 (M) | |
| Words per second | 2.8 (M) | 2.6 (M) | |

## How dialogue is stored

- **Kingdom Come II** keeps all dialogue in its own tool's XML (Skald, KM-A-18), 18,691 quest files (R, M). Its dialogue nodes are player-started conversations (2,241), conversations the game starts (670), lines in the world without a camera (5,421), condition graphs wrapping them (1,216) and cutscenes (169) (M).
  - A decision offers sequences; each has an entry condition, an end, an optional cooldown, and responses: a role, its line, a direction note, and camera, gesture, face and gaze commands (M). 33,325 decisions, 75,614 sequences (M).
  - The text sits in one table per language keyed by the line's name (R, KM-A-91); English holds 155,813 entries (M). A voice file is named by voice and key, so the archives show who recorded what (M).
  - **Choices (M):** a median 2 options (p90 4); the player picks a 4-word prompt, then speaks a median 8 words. About 400 are timed, mostly 5 to 10 s; 1,280 are skill checks (persuade, dread, impress lead) at eleven difficulties; 250 greetings move reputation; 5,306 sequences play once only.
- **Mafia** keeps text in "Lexicon" conversations: per scene a string table and a table of rows (character, voice event, audio length, face clip) (M, N); 1,880 scenes, median 2 lines (M). No choices were found; the game is linear (M, I). Ambient talk is 115 conversation assets alternating speakers over a median 3 parts (89 for two), 15 of them generic by class pairing (M).

## How much is written

- **Kingdom Come II, by where it plays (M):** conversations 60,164 lines; game-started 30,986; in the world 43,833 (one-sided barks 20,024, short exchanges 15,117, chats 7,034, greetings 1,658); cutscenes 2,986. 6% have no English voice.
  - **Per character (M):** the player 40,962; 74,275 for 1,897 one-voice roles (named people and bit parts); 22,732 for 1,696 crowd roles, whose lines a median two or more voices record (another split by voice gives 67,451 and 29,618). The companion has 3,385.
  - **Per passer-by:** a crowd line is recorded by a median 4 voices (p90 16). In street pools each voice records about a third, a median 2 of 5, so a person stays consistent while the street varies (M).
- **Mafia (M):** 5,690 exported lines for 73 characters; the player 1,363, the next 810. 6,657 systemic voice events cover 659 situations (N; grouped by name, I): mission nags 142, combat 138, narration at world interactions 90, perception and alert 63, street reactions 60, ambient conversations 57, the rest mission-only.

## Bark situations

| Situation | Kingdom Come II (M unless tagged) | Mafia (M, from voice names) | LEDGER now |
|---|---|---|---|
| Greeting the player | 419 lines, man or woman; a priority chain picks the pool (below); 40 s street-wide (R) | friendly, hostile: 12 voices × 3 to 4 | stance by story (Recognition) |
| His look and state | weapon drawn, crouching (118 lines, 20 s); dirt, smell, nakedness, injury, a criminal's brand, no torch at night (R) | none by name | none |
| Bumping | 13 lines, 20 s, among 334 for small provocations (pebble, horse, noise, dog), median 40 s | polite, rude, startled, calm: 12 to 14 voices × 3 | none |
| Seeing a crime | 4,747 lines in 763 files by speaker type (man, woman, guard, foes), 6 voices a line, 30 s | heard or seen near or far, a body, panic; trespass in 3 levels | just-now glass, shout, crash, noise; settling |
| Being threatened | a threat reaction, priority 85 (R) | none by name | threat told, threat heard |
| Reputation | refusing to talk at low reputation (111 lines) | none | refuses, avoids, confronts |
| Each other | greetings by pairing (659 lines, 32 s; a pair once in 6 game hours, R); gossip by class pairing and place (2,607 lines, 10 min) | 115 ambient conversations | ambient pairs by state; gossip true to the simulation |
| Alone | talking to oneself at work, by trade, rain, night (357 lines, about 15 min) | idle (22 voices) | none |
| Weather | rain in 33 conditions | none | none, by rule |

**Kingdom Come II's greeting chain (R):** low reputation or his brand; else violent anger; else property anger; else high reputation with renown; else high charisma (his appearance, I); else neutral. Each state is a pool of 4 to 12 one-liners, the neutral one 29 with community variants.

## Keeping it fresh

- **Kingdom Come II, two levels (R):** a street-wide wait by kind, kept on the player, where a more urgent kind breaks a lesser one's wait: companion comment 4.5 s, a body 5.5 s, a drawn weapon 10 s, crouching 12 s, greeting 40 s, mourning 80 s (priorities: greeting 10, weapon 40, threat 85, body 95). Per person: 10 s for anything, 20 s for an NPC's greeting, 45 s after a crime interruption, a greeted-today flag (N). Play time, not the 15-times world clock (I), except the pair greeting's 6 game hours (R), about 24 real minutes. 3,997 street dialogues carry a clash class (flavour, open world, crime, combat, bump) that decides which wins when two meet (R name, I use).
- **Per line (M):** 46% of street sequences carry a cooldown: median 32 s, p25 15 s, p75 5 min, p90 30 min; a conversation's opening greeting 30 min, a friend's greeting 32 min. Street decisions offer a median 2 variants (p90 6), half only one; 2,169 carry a cap on how many each voice records (VoiceoverReductionMaxSequences, 1 to 6) (M). The pick is in code (I).
- **Mafia (R):** a mission speaker repeats every 7 to 10 s, greets and parts at 10 to 15 s, waits 2 to 5 s after any bark; a priority threshold of 100 lets a bark override another. Its bark table was not exported.
- **LEDGER** goes further: never-heard first, then the oldest (Fresh); one remark per person per story; a 45 s floor that keeps a 14-line band from returning inside 10.5 to 22 minutes (measured 28 September).

## Staging

- **Kingdom Come II's conversations (M):** 78% of lines carry a camera command; named shots across all dialogue are close shot 46%, close-up 41%, medium 13%. 77% carry a gesture (1.06 a line; 179 kinds in all, led by a general gesture, confusion and nods), 39% a facial mood (25 moods), 55% a direction note. Gaze aims on a 3×3 grid round a face (R), easing most often over 0.5 s. Where a line sets a start delay (13% of conversation lines) it is a median 0.27 s (M; meaning I). Street lines carry almost no camera (0.7%) and gestures on 25%.
- **Distances (M; meaning I):** street barks carry 35 m in 76% of dialogues that set it (10 m quiet, 50 to 200 m loud); a conversation's limit is 10 m in 1,060 of 1,209; a person calling the player over stands 2 to 4 m off, calls up to four times, then gives up.
- **Mafia:** cutscenes cut a median 3.3 s a shot (p25 2.1, p75 5.3; 2,583 shots in 171 sequences) (M); 96% of line rows name a face clip (M). A mission speaker looks at the player and turns only when speaking, triggered at 10 and 15 m (R). Talkers stand at duo and trio smart objects (N).

## Line length and subtitles

- **Lengths:** 90th percentile 19 words, 7.2 s (Kingdom Come II); 16 words, 6.3 s (Mafia) (M).
- **Subtitles:** Kingdom Come II has separate switches for conversation and bark subtitles, plus name, background and size (R). Mafia splits a subtitle over 120 characters, never under 40 (R); sizes, backgrounds and colours are options (N); Sicilian is a voice language only (R).

## For LEDGER

Targets, not work now: the voices and the town's talk work are not reopened (3 October); new systems wait for PLAN.md (29 September). Items 1 to 3, 5 and 6 are phase 5 proposals for his page.

**How much each kind of character needs (phase 5's batches; the 24 September ruling: everything unprompted written ahead):**
1. **Adopt for the 30 regulars:** about 30 own street lines each, for the situations their day lets them hold (Kingdom Come II's upper quartile for a one-voice role; Darren has 33). Today's cast stays as ruled: own lines for Ron, Darren, Father Walsh and June, shared for Sheila, Alison and Ada.
2. **Adopt for the crowd:** per situation at least 6 lines per kind of speaker, each crowd voice owning a fixed 2 or 3, so a person repeats himself as people do while the street varies. Serves VoiceBank's named risk (six voices is thin); for the town, Mafia's 14 (man or woman, by age), cast only on his yes.
3. **Adopt the missing situations,** written ahead: greeting him by regard in Kingdom Come II's order on LEDGER's values (afraid or suspicious, angry, knows and likes him, his appearance, neutral), no numbers shown (D33, D34); bumping; neighbours greeting each other; talking to oneself at work; a small rain bank (phase 3's weather proof). Serves the Meridian Test: the town visibly knows them.
4. **Ignore** the conversation-opening greeting bank (his 7 October ruling: no prepared openings), skill checks, the community voice categories (accents come from the casting sheets) and Mafia's mission nags.

**Ambient lines with no model call, played at once (StreetVoice, extended):**
5. **Adopt the two-level gate:** the situation from the simulation; a street-wide wait by kind with priority (a deed breaks a greeting's wait; the 45 s floor stays for everyday talk); a personal wait (10 to 20 s; one greeting a person a game day; a pair's greeting once in a few real minutes); Fresh's never-heard-first within that voice's share; the prepared clip and subtitle at once.
6. **Adopt as starting values:** crime reactions 20 to 40 s; gossip 10 min a pair; self-talk 15 min a person.

**Staging and length (phase 1's speaker; phase 3):**
7. **Adopt:** speakers face each other and turn only when speaking; gaze eases over about 0.5 s; a gesture on three lines in four, a face mood on two in five; a prepared reply starts a beat after its opener (about 0.3 s, I). Any conversation camera (the interface is not reopened, 3 October) alternates close shot and close-up, about 3.3 s a shot; street lines never move it.
8. **Adopt length targets:** street lines about 7 words (ours are); replies about 12 words, 4 s at 2.6 to 2.8 words a second, keeping a live reply's first sentence short (the 2 s bar); Tom's suggested lines about 4 words, like Kingdom Come II's prompts. Subtitles split above 120 characters, bark subtitles a separate switch, when the interface is next touched.
9. **Adapt hearing:** Kingdom Come II's barks carry 35 m; LEDGER says a remark within 7 m, its words clear within about 6 m in quiet (Acoustics), the murmur beyond (ChatterLevel).

## Coverage map

To tick in REFERENCE.md: dialogue and choices (both games, data side); barks (KCD2 data side; Mafia by names, settings not exported); cutscenes and staging (camera, gesture, gaze, shot length; the rest Study 16).

## Open blind spots

- **Mafia, not exported (F: full):** systemic text, bark table and settings, voice data, 29 reaction bark assets: its bark cooldowns, chances, ranges, and whether crowd voices say different words.
- **Code:** how either picks within a pool; Kingdom Come II's 51,000 camera commands with no named shot.
- **Units:** whether Kingdom Come II's per-line cooldowns count play time (I; 131 sequences name the world clock explicitly); what its line-length field and start delay mean (I). Its cap on lines per voice holds in only 938 of 2,142 pools (M).
- **Shown only in play:** density, subtitle look, how barks land. No recordings (25 October).

## Sources (read 28 October 2026)

- **Kingdom Come II:** Scripts.pak (Quests/Final; AI crime cooldown trees); Tables.pak (skald, text, ai, ui); English_xml.pak; the English voice archives' directories (nothing extracted). Warhorse's wiki (warhorse.youtrack.cloud), public interface, in full: KM-A-18, KM-A-91.
- **Mafia:** exported Texts, world conversation data, cutscene sequences, the conversation bark Blueprint and bark tasks; DefaultGame.ini; the name index (Systemics, Voice, Wwise events, Barks); script-objects.json (H13Bark, H13Lexicon).
- **LEDGER:** RULINGS.md (talk); StreetVoice, OwnLines, VoiceBank, Confab; talk-protocol.md; the casting cards; production/research/ambient-lines/METHOD-2026-09-30.md.

## Review

A fresh reviewer (28 October) re-measured about 130 numbers and read about 25 values in their files: pass with fixes, all applied (Mafia's words and variants, bumping's count, the start delay's coverage, the role split's rule, five small counts, the pair greeting's units, the 7 m range, the street-lines ruling; items 1 to 3, 5 and 6 made proposals under the 3 October and 29 September rulings). Cost, from the clock: about 11:25 to 12:25 (reading, measuring, synthesis, review, fixes).
