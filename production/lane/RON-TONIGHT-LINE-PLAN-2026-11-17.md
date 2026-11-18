# Ron's "where will you be tonight" line: plan and golden rows, 17 Nov 2026

Review applied (17 Nov, production/lane/reviews/REVIEW-SIGNS-NOSETAIL-RONTONIGHT-2026-11-17.md, section 3, all six fixes): the claim-check change, its tests and its hours are dropped (about 4.5 h now); after midnight follows the claim check's own reading of "tonight" (R7); "this evening" ends at midnight; the trigger gets its own small word list; R12's routine is fixed; R2's stay is 18 to 19.

A helper's plan for the main session. Nothing in the game, the Core, the talk helper or the specs was changed. It is a narrow first step on gap 1 of production/research/phase2-plan/RON-ROUTINE-TALK-2026-11-17.md (his regular day is not in his talk). It covers only tonight, not his whole usual day.

Sources read on 17 Nov: that note; canon.md; production/specs/hook-cast.json (person "rocco"); ledger/Assets/Scripts/Core/CastDay.cs (PlaceOf, WhereWords, SaidOf); ledger/Assets/Scripts/Core/Claims.cs (TimeWordFits, NightDay, WhereHeSays); ledger/Assets/Scripts/Core/Silence.cs (KeepsQuietFor); ledger/TalkHelper/Program.cs (the "Where you are:" line and its selftest); game-design/first-ask-2026-09-29.md; production/cast/cards/rocco.md.

Reference: Kingdom Come II's timed links with places (studies/01-npc-life.md, as the source note cites it). A KCD2 person's next link is a fact the game holds; this plan simply lets Ron say his next one.

## What is there today

- The talk helper calls CastDay.WhereWords(id, day, hour) and adds "Where you are: <said words>." to the scene. That is the only routine fact Ron gets. Asked about tonight, he has nothing to say. The claim check (Claims.WhereHeSays and the helper's check, Program.cs about lines 825 to 850) does not read this line: it judges Tom's own answer to "where were you" against where the asker saw Tom, and never checks what Ron says about Ron.
- Ron's routine (hook-cast.json, "rocco"). Every day except Sunday: 00 off, 07 cafe, 08 mickeys_rank, 12 fish_front, 13 mickeys_rank, 17 quay, 19 mickeys_office, 23 off. Sunday ("sun"): 00 off, 10 allotments, 13 off, 19 mickeys_office, 23 off. Saturday has no key of its own, so it uses the daily routine.
- Spoken place words come from each place's "said" field in the file: quay "the quay at the bottom of Quay Street"; mickeys_office "the front room of Mickey's, the cab office"; cafe "inside the cafe across the street from Mickey's"; allotments "the allotments by the railway". "off" has no words: it means off the street.

## 1. What questions trigger it

The line fires when Tom asks where Ron will be, about a time later tonight. The trigger reader has its own small word list: "tonight", "this evening", "after work", "later", "later on", "you about", "you around", "at night", and a clock time (the same shapes as Claims.ClockWordRx, copied, not shared). "later", "later on", "you about" and "you around" are not in Claims.TimeWordRx, and they must not be added there: that would change NamesAnotherTime and LooseTime and move the claim-check goldens.

Triggers (a where-question plus a tonight time):
- "Where will you be tonight?", "Where are you tonight?", "Where'll you be tonight?"
- "Where will you be later?", "Where are you going to be later on?"
- "Where can I find you after work?", "Where will I find you this evening?"
- "Where are you at ten?", "Where will you be at eight tonight?", "Where'll you be around nine?"
- "You about tonight?", "You around later?"

Does not trigger:
- "Where are you?" or "Where are you now?" (today's "Where you are" line already answers).
- "Where were you last night?" (the past; the claim check's alibi path).
- "Where will you be tomorrow?" or "on Sunday?" (later work; the same function with another day could serve it).
- "at ten in the morning" (not tonight).

## 2. What "tonight" means in hours

Tonight is the calendar day's evening: 17:00 to 05:59 the next morning (an hour before 06:00 belongs to the night before, Claims' NightDay, which is why Thursday's 23:30 and Friday's 01:00 are both inside Thursday's night). Neither canon nor a ruling sets this. It copies how Claims.TimeWordFits reads "tonight", so the word means one thing across the game; no check depends on it. I am not using the 18:00 to 02:00 suggested in the brief.

Asked after midnight, "tonight" follows TimeWordFits too: "tonight" is the night of today's calendar day. At 01:00 on Friday, tonight is Friday evening from 17:00, not what is left of Thursday night.

- "tonight", "after work", "later" (said after 12:00): the stays from now, or from 17:00 if that is later, until 06:00.
- "this evening": in TimeWordFits it ends at midnight (today, from 17:00). The line deliberately reads it as tonight, the same window to 06:00, because Ron's evening stays all end by 23:00 and the answer is the same.
- "later" said before 12:00: read as tonight, the same window. Before noon, "later" in a question about where to find him means this evening. That is my reading, not a fixed rule.
- "at <hour>" with no half of the day given: the next time that hour falls inside tonight. "At ten" is 22:00 and "at six" is 18:00. "At two" is 02:00, the small hours of tonight.
- "at <hour>" when that hour of tonight has already passed (asked 23:30 about ten): Ron says it has been and gone and gives where he is from now on.

## 3. How the line is chosen from the routine

A new Core reader, CastDay.TonightStays(id, day, hour), returns tonight's stays in order: (place, from, to), the current stay included, clipped to the window, with neighbouring hours at the same place joined. It is built only from PlaceOf, so it never disagrees with what the street plays.

Which stay the line names:
1. A clock time was asked ("at ten"): the stay that covers that hour.
2. Otherwise: the longest on-street stay in what is left of tonight. If two are equally long, the first.
3. If nothing on the street is left tonight: "off", and Ron says he is done for the night.

The line can also name one other stay with its hour, the first one if it comes earlier ("down the quay first, about five"). It may also name the hour he goes off ("till eleven"). It never names a place that is not in TonightStays.

Weekday from 15:00: quay 17 to 19 (two hours), office 19 to 23 (four hours). The office wins, with the quay as the earlier stop. That fits the first-ask design: Ron brings the envelope to the office after dark, so the player should learn the office.

## 4. What Ron keeps back by trust

None. No design gates where Ron will be by trust. Sheila's on-trust rule ("namesHim": "on-trust") covers only what she calls Tom. Ron's "keepsQuiet": "owner" means he keeps Tom's secrets for Tom. It does not hide Ron's own whereabouts from Tom. Tom is Mickey's heir and Ron works for him, so he answers plainly at every standing.

One thing he leaves out: the ferry landing. On an ask night the first-ask design sends Ron down to the landing at eleven, but his routine says "off" from 23:00 and the open question in the source note recommends keeping him off the street. So the line says "off home" or "done for the night" and never names the landing. When the ask is live, the existing ask talk speaks about the landing, not this line.

Content rule: Ron never mentions a pub, a pint or a drink, or a bet or the bookies. "Off" is said as "off home", "done for the night" or "in my bed". The templates go through tools/content-gate.py like any spoken line.

## 5. What data the helper must read

- From hook-cast.json, through the CastDay that is already loaded: "rocco"'s "routine" and "days" (only through PlaceOf), and each place's "said". There is no new file, no new field and nothing to stage. hook-cast.json stays the one home for the facts.
- From the request the game already sends: "day" and "hour" (game time), plus Tom's words.
- What goes to the model, beside "Where you are: ...": one line, "Tonight: <said words> from <h> till <h>[, then <said words> from <h> till <h>][, then off the street].", built from TonightStays with hours as Ron would say them ("seven", "eleven"). The model words it in his voice; the facts are the Core's.
- No claim-check change. The check judges only Tom's answers about himself. The guard that Ron's line matches his routine is the CoreTests sweep in section 8.

## 6. Edge cases

- Asked after midnight (00:00 to 05:59): tonight is the coming evening of today's calendar day (section 2). On a weekday that is the office from 19:00. He may add the morning's first place (cafe at seven), named as the morning, not tonight.
- Asked 23:00 to 23:59: also off. "At ten" has passed: "Ten's been and gone."
- Asked 17:00 to 22:59: the current stay counts, so asked at 20:00 he names the office he is already in.
- Routine missing (Ron not in the cast file, or no file loaded): no "Tonight" line at all. Ron uses his own-word "known-only" or "deflect" kind and names no place. Nothing checks a place he might still invent; the selftest's R11 case (no "Tonight:" line) and the paid run's listening are the guard.
- Ron at Mickey's all night (a routine where the office runs from 17:00 past 06:00): one stay, token mickeys_office, "All night in the office."
- Sunday: the "sun" routine. The allotments end at 13:00, so tonight is the office from 19:00.
- Saturday: no "sat" key, so the daily routine (the quay, then the office).
- Midnight crossing into a weekday with its own routine: TonightStays reads each hour through PlaceOf with that hour's real day. A Sunday night after midnight reads Monday's 00 off. That is correct, and the same as the street.
- The question is about tonight, but it is daytime and he is at the rank: the line still names tonight's stays, not the rank.
- "Tomorrow night": does not trigger (section 1).

## 7. Golden rows

Day numbers as Population: day 0 Monday to day 6 Sunday. "Daily" is the weekday routine above; "Sun" is the Sunday one. Line shapes are what the model's line must carry. The words are a guide in Ron's voice (dry, short, "boss"), not fixed text. Rows R11 and R12 use a small test cast file, not hook-cast.json.

| # | Game time | Question | Routine excerpt (tonight) | Expected place token | Expected line shape |
|---|---|---|---|---|---|
| R1 | day 0 (Mon) 15:00 | Where will you be tonight? | Daily: 17 quay, 19 office, 23 off | mickeys_office | Office from seven till eleven, quay first may be named: "Down the quay about five, boss, then the office from seven. Kettle's on till eleven." |
| R2 | day 0 (Mon) 18:00 | Where'll you be later? | Daily: quay 18 to 19 (from now, one hour), office 19 to 23 | mickeys_office | "Office from seven, boss. Till eleven, then I'm off home." |
| R3 | day 1 (Tue) 20:00 | Where are you at ten? | Daily: office 19 to 23 | mickeys_office | Same place as now: "Same as now, boss. Front room of Mickey's till eleven." |
| R4 | day 0 (Mon) 16:00 | Where will you be at ten? | Daily: 22:00 falls in office 19 to 23 | mickeys_office | Covers the hour asked: "Ten? In the office, boss. I'm there seven till eleven." |
| R5 | day 0 (Mon) 15:00 | Where will you be at six? | Daily: 18:00 falls in quay 17 to 19 | quay | The clock time wins over the longest stay: "Down the quay at six, boss. Office after seven." |
| R6 | day 3 (Thu) 23:30 | Where will you be later? | Daily: off from 23 | off | Done for the night, no place tonight: "I'm done, boss. Off home. Cafe at seven if you want me." |
| R7 | day 4 (Fri) 01:00 | Where are you tonight? | Daily, Friday evening (calendar day's night, as TimeWordFits): quay 17 to 19, office 19 to 23 | mickeys_office | Friday's evening, the cafe allowed as the morning extra: "Office from seven tonight, boss. Cafe at seven this morning if you want me sooner." |
| R8 | day 6 (Sun) 11:00 | Where will you be tonight? | Sun: allotments till 13, off, office 19 to 23 | mickeys_office | Not the allotments: "Office from seven, boss. Sunday or not." |
| R9 | day 5 (Sat) 14:00 | Where can I find you after work? | Daily (no "sat" key): quay 17 to 19, office 19 to 23 | mickeys_office | "Office, boss, from seven. Quay before that if you're passing." |
| R10 | day 1 (Tue) 23:30 | Where are you at ten? | Daily: 22:00 passed, off from 23 | off | Says the hour has gone: "Ten's been and gone, boss. I'm off home now." |
| R11 | day 0 (Mon) 15:00 | Where will you be tonight? | Test cast: no "rocco" | none (no Tonight line) | Names no place, own-word known-only or deflect: "Couldn't tell you yet, boss. Wherever I'm wanted." |
| R12 | day 2 (Wed) 15:00 | Where will you be tonight? | Test cast: [[0, "mickeys_office"], [6, "off"], [7, "cafe"], [17, "mickeys_office"]] | mickeys_office | All night: "In the office all night, boss. Where else?" |

Negative row for the trigger test (not a golden line): day 0 15:00, "Where were you last night?", must not fire the tonight line.

Every line passes the content gate: no pub, pint, drink, bet or bookies, and no slurs. Each place in a line is one of the token's "said" words or an area name that AreaFor maps back to the token.

## 8. Regression test it needs

- CoreTests: CastDay.TonightStays and the choice rule against R1 to R12 (token and stays), from hook-cast.json and the two test casts. Also a sweep over every cast person, every day and every hour: each chosen place equals PlaceOf at some hour inside tonight. This is the one-home check.
- TalkHelper --selftest (the "placed" case's pattern at Program.cs about line 2512): for R1 the scene carries "Tonight: the quay at the bottom of Quay Street from five till seven, then the front room of Mickey's, the cab office from seven till eleven, then off the street." with the exact said words; for R11 no "Tonight:" line.
- Trigger: the triggers and non-triggers in section 1 as a word test, the negative row included.
- The usual set before committing: CoreTests, Soak, SaveChaos, PerceptionGolden, StrangerTest. No C++ port is needed: the reader is used only by the C# helper. The port-golden check should still be run to show nothing moved.

## 9. Hours to build (est., for the main session)

- CastDay.TonightStays and the choice rule, with the CoreTests rows: 1.5 h
- Question reading (tonight, later, after work, at <hour>) and the "Tonight:" line in the helper: 1.5 h
- Selftest, the trigger word test and the full test run: 1 h
- One paid run of Ron's talk on R1, R6 and R8, listened to against his card (machine work, API spend logged): 0.5 h

Total about 4.5 hours (est.). No claim-check work. Who builds it: the town side (talk). It touches ledger/Assets/Scripts/Core and ledger/TalkHelper, which this helper did not edit.

## Open points

- Whether "later" before noon means tonight (section 2) is my reading. It fits how the question is asked, but no design says so.
- For the main session: the source note RON-ROUTINE-TALK-2026-11-17.md has the same misreading in its table ("the claim check reads that as the scene"). The claim check does not read the "Where you are:" line; it judges only Tom's own "where were you" answers.
- quay-cast.json's copy of Ron's day (golden run only) has no 07:00 cafe and no Sunday (source note, gap 3). These rows read hook-cast.json, never that copy.
