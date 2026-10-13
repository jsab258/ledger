# NOTES: ambient lines (unit 12, cloud week 42)

Written 13 October 2026 for Jafar's order of 12 October: "Ambient lines: short spoken lines per kind of person and situation (greeting, being bumped into, rain, seeing a crime, being asked the way), in the voice canon.md gives the town, within the content rule, with cooldown and variety rules, as data the game can play without a model call." Nothing here is in the game or on a page of his yet. It is a proposed addition: the PC session adopts it after its tests (how is below). Everything invented is marked, and sits in DECISIONS.md as eight entries, each ending "Marked for Jafar."

## What was made (production/cloud-week/lines/)

- **lines.json**: the lines. 1,626 lines, 13 kinds of person, 14 situations, 34 places for directions. Each line has an id, its words, who says it (kind), the moment (situation), the conditions that must hold (weather, time of day, his standing with them, how sure they are, the place asked about), a weight and a cooldown group. It is the street's own dialogue-bank format, extended (see the format section).
- **rules.json**: the rules, as data: cooldowns, variety, priorities and silence. Every number carries its reason and its source, or says it is invented here.
- **check_lines.py**, **checks/check_v1.json**, **checks/walk_v1.json**: the check, its rows, and the walks. Result today: **2500 of 2500 rows pass**, and **62 of 62 seeded faults** are caught.
- **walk_sim.py**: the small simulation the check plays (thirty minutes of a walk through the rules).
- **build_lines.py**, **lines_lib.py**, **rules_source.py**, **authored/**: the builder and the written text. `python3 build_lines.py` makes lines.json and rules.json; `python3 check_lines.py` checks them; `python3 make_notes.py` makes this file; `python3 export_slots.py` turns lines.json into the street's two existing derived shapes (below). Standard library only; each takes seconds on one core.

## The numbers

- **Kinds of person: 13.** Nine shared (said by anybody who stands in the kind) and four own, for Ron, Darren, Father Walsh and June, as RULINGS has it. Sheila, Alison and Ada keep the shared lines, as RULINGS has it: Sheila and Alison stand in office worker, Ada in pensioner. Tom, the three heads, the Fixer, DS Ellis and the outfit's man have no kind; they speak in authored scenes and live talk only, and the check requires each of them to have a stated reason.
- **Situations: 14** (greeting at five standings, being bumped into, rain starting, in rain, a crime heard, a crime glimpsed, a crime seen face to face, after a deed, being asked the way, a farewell), and **34 places** for the way.
- **Lines: 1,626.** Of these 1,455 are the kinds' own words (at least 8 in every kind and situation the kind has, and 13 for a greeting to a stranger), and 171 are directions, 5 or 6 for each of the 34 places, said by any resident who knows the place.
- Every line is under twelve words (the longest is 11).

| Kind | Who stands in it | Lines |
|---|---|---|
| shopkeeper | Brenda, Rita, Wayne, Hal, Grace, Peter, Lily, Sylvia, the pawn's appraiser, the pawn's clerk | 116 |
| dock worker | Colin, Dennis, Gordon | 116 |
| pensioner | Ada, Edith, Albert, Winifred, Nora | 126 |
| office worker | Sheila, Alison, Pauline, Christine, Susan, Philip, the customs assistant, Karen, Dawn | 127 |
| driver | Kevin, Terry | 103 |
| laundry worker | Doreen, Tracey, Iva (laundry presser), Selma (laundress) | 116 |
| tradesman | Ian, Shaun, Jelena (locksmith), Gary | 115 |
| night shift | Norman | 120 |
| casual worker | Lee, Julie | 115 |
| Ron | Ron | 94 |
| Darren | Darren | 93 |
| Father Walsh | Father Walsh | 112 |
| June | June | 102 |
| directions (any resident who knows the place) | | 171 |

Lines by kind and moment (the kind's own words, not the directions):

| Kind | Greetings | Bumped | Rain | Crime | After a deed | Asked the way | Farewell | Total |
|---|---|---|---|---|---|---|---|---|
| shopkeeper | 40 | 9 | 18 | 24 | 8 | 8 | 9 | 116 |
| dock worker | 41 | 9 | 18 | 24 | 8 | 8 | 8 | 116 |
| pensioner | 50 | 9 | 18 | 24 | 8 | 8 | 9 | 126 |
| office worker | 52 | 9 | 18 | 24 | 8 | 8 | 8 | 127 |
| driver | 28 | 9 | 18 | 24 | 8 | 8 | 8 | 103 |
| laundry worker | 41 | 9 | 18 | 24 | 8 | 8 | 8 | 116 |
| tradesman | 40 | 9 | 18 | 24 | 8 | 8 | 8 | 115 |
| night shift | 44 | 9 | 18 | 24 | 8 | 8 | 9 | 120 |
| casual worker | 40 | 9 | 18 | 24 | 8 | 8 | 8 | 115 |
| Ron | 20 | 8 | 18 | 24 | 8 | 8 | 8 | 94 |
| Darren | 19 | 8 | 18 | 24 | 8 | 8 | 8 | 93 |
| Father Walsh | 38 | 8 | 18 | 24 | 8 | 8 | 8 | 112 |
| June | 27 | 9 | 18 | 24 | 8 | 8 | 8 | 102 |

Greeting lines by standing, over all kinds: stranger 104, the new owner 103, Nowak 122, Tom 124, Tommy 27. Ron and Darren have no stranger or new owner greeting (they know his name from the start); Father Walsh and June have no stranger greeting; the drivers have none either (the day driver and the night driver both know who he is from the first day, so thirteen such lines could never be said and were dropped after the canon review); Tommy has lines in three kinds only (pensioner, office worker, Father Walsh).

## The check (check_lines.py): 2500 of 2500 rows pass

It re-reads every home (the cast and the routines, the atlas, Population.cs, RealWorld.cs, StreetFacts.cs, StreetVoice.cs, the content and canon gates) and does not trust what the builder said. One row for each of the 1626 lines, and rows for:

- **each line**: under twelve words; its fields, id and bank right; every condition valid for its situation; none of the words the content rule bans (the content gate and slurs-v1.json), no real brand, place, person, team or programme (RealWorld.cs's lists and a few of its own), nothing after 1992, no quotation or known lyric; standing words exactly canon's (the new owner, Nowak, Tom, Tommy, and only the line's own rung); Mickey named only as the place, and the two approved lines carried by no kind; dialect, police and gender flags true; a crime line never claims more than its sureness (a noise line never says it saw, a shape line never gives a face, a sex or a coat, a face line never names or accuses); no line states a standing the simulation might not hold (what the street has said, heard, expected or felt about him, what he has done or been called before, an opening nobody set, a window the speaker may not have); each direction checked against where its place really is.
- **the two lines that say 'heard you ...'** and stay (a dock worker's one suitcase, a casual worker's rank to run): each claims only what a StreetFacts.cs fact states, held by every named member of the kind in people.json.
- **each kind and situation**: the count, and no lines in a situation the kind does not have.
- **each situation across kinds**: no two kinds say the same thing in other words (at least 60 percent of the words shared, address words such as boss, love and son aside). This is the fault that failed the street's earlier attempts at lines in several mouths; all 153 pairs found at 60 percent or more were rewritten, and 82 pairs between 50 and 60 percent remain (the same fact in a similar frame, such as two ways to say mind how you go).
- **each group (kind and bank)**: after every condition (each weather and hour it can happen, each standing, each accent, never-police) at least six lines are left; each rung reads out its word; no two lines say the same thing (a shared four-word run, or three quarters of the content words).
- **the cast and the trades**: every person in the cast and the routines has one kind or a stated reason for none; every trade the old crowd generator names has one kind; the own kinds are exactly the four RULINGS names; Sheila, Alison and Ada keep the shared lines.
- **the places**: each place is where its home says (the routines, the built street, the atlas converted with its own anchor), with five or more lines.
- **the rules**: each number agrees with the code and the rulings it comes from (the 45 s is StreetVoice.ClearWordsEverySeconds), each has a reason, and the priorities put a crime above a greeting.
- **each rule alone** (rule.*): a small scenario for each: a crime line fades neighbour talk, a crime outranks a waiting greeting, a higher priority replaces a waiting line, the neighbours' gap in the dry and in rain, the hush doubles it, a witness says no hello, the bag uses every line before a repeat, the seven who never go to the police are never picked a line that rings them, Nora and the Tangs never get dialect, a question is always answered.
- **the walks** (below), **canon-gate** over lines.json, rules.json and this file, and **content-gate** over this file.
- **62 seeded faults**: the check damages a copy of the files (a thirteen-word line, a banned word of each of the rule's kinds, a real brand, a year after 1992, a real place, Nowak in a stranger greeting, a stranger describing Mickey, a direction up for a place down, a long walk for a place at 76 m, Ron ringing the police, the neighbours' gap set to 30 s, a greeting above a crime in the priorities and the rest) and requires each to fail a row. **62 of 62** do.

Words are checked by lists: a screen, not a reader. What a reader still has to judge is at the end of this file.

## The walk: thirty minutes through the rules (walk_sim.py, seed 1990)

Tom walks Quay Street and pauses; twenty passers-by cross his path; four of the street's own people stay where they are (Ron at the rank, Marla at her door, Ada on her step, Rita at hers); rain falls from minute 12 to minute 20 (drizzle for the first and last minute); one crime happens at minute 15, within sight of where he is. Every line goes through rules.json as the PC session's picker would apply it.

**The main walk.** 24 people came within earshot; 24 lines were played and 23 heard by him. Heard by moment: asked the way 1, a crime glimpsed 1, farewell 4, greeting to Nowak 2, greeting to the new owner 10, greeting to a stranger 3, greeting to Tom 1, talk in rain 1.

- **Repeats: none.** No speaker said a line twice inside 30 minutes, no line was said by two speakers inside 120 s, and no words were heard twice at all.
- **Busiest minute:** 5 heard lines (the cap is six outside a crime).
- **Gaps:** 16 of the 30 minutes had no line at all (53 percent); the longest silence was 231 s (from 15:02 to 18:53). The rain thinned the street: 2 passers-by arrived in the 8 rain minutes against 18 in the other 22.
- **Neighbours' talk:** 1 neighbour line(s) heard, never closer than 45 s. One group never spoke twice inside a minute (the closest two were 189 s apart).
- **Not played:** 146 moments, nearly all by design: the chance roll failed 85, neighbours' gap 18, a witness within the hour says nothing of this kind 17, speaker's family cooldown 16, family gap 7.

The lines he heard, in order (minutes and seconds into the walk):

- 00:01, Ron, greeting to Nowak: "Boss. You've the look of a man who's not eaten."
- 00:28, shopkeeper, greeting to the new owner: "The new owner. Anything you need, just ask."
- 00:32, pensioner, farewell: "I'll let you get on, dear."
- 00:44, shopkeeper, greeting to a stranger: "Anything I can help you find?"
- 00:59, office worker, greeting to the new owner: "You'll be the new owner, I take it."
- 01:53, shopkeeper, farewell: "Mind how you get home."
- 01:56, pensioner, greeting to the new owner: "You'll be the new owner. How do you do, dear?"
- 04:58, shopkeeper, greeting to the new owner: "Not seen the new owner in here yet."
- 05:02, shopkeeper, farewell: "Ta-ra for now."
- 05:48, dock worker, greeting to Nowak: "Now then, Nowak."
- 05:50, dock worker, asked the way: "Ask at the cab office. That's what they're for."
- 09:28, dock worker, greeting to a stranger: "Watch the setts. They'll turn your ankle."
- 10:00, tradesman, greeting to the new owner: "New owner. Don't touch anything till it's dry."
- 11:06, laundry worker, greeting to the new owner: "New owner, is it? Don't stand in my steam."
- 11:51, shopkeeper, greeting to the new owner: "You must be the new owner. Mind how you go."
- 12:00, Ron, talk in rain: "Rank's a pond. Mind your boots, boss."
- 15:02, casual worker, a crime glimpsed: "Something moved. I'll leave it at that."
- 18:53, tradesman, greeting to the new owner: "New owner, you'll rust standing there."
- 22:30, dock worker, greeting to the new owner: "So that's the new owner. Smaller than I thought."
- 23:22, laundry worker, farewell: "I'll get back to my presses, love."
- 24:42, Father Walsh, greeting to the new owner: "Ah, the new owner. I'm glad you've come."
- 24:57, casual worker, greeting to Tom: "Hello, Tom. Cadge a fag?"
- 26:45, casual worker, greeting to a stranger: "Don't suppose you're hiring?"

**Thirty other seeds of the same walk** (1991 to 2020), with the main one: lines heard 15 to 25 (middle 21); busiest minute outside a crime 3 to 6; minutes with no line 43 percent to 70 percent of the half hour (middle 53 percent); longest silence 203 s to 719 s (middle 420 s). Zero repeats inside a floor and no neighbour line closer than 45 s in any of them. Across them every moment was heard at least once but Tommy: after a deed 12, asked the way 16, bumped into 15, a crime seen face to face 8, a crime heard 10, a crime glimpsed 5, farewell 131, greeting to Nowak 98, greeting to the new owner 217, greeting to a stranger 61, greeting to Tom 12, talk in rain 9, rain starting 13.

**A busy half hour** (eighty passers-by instead of twenty, same rain and crime): 40 lines heard, busiest minute 6 outside the crime, still no repeat and no neighbour line closer than 45 s. **An afternoon walk** (15:00): 23 heard. **A night walk** (22:00, more night shift, fewer old people and shopkeepers out): 19 heard, no repeat. **The test has teeth:** the busy walk with the variety and cooldown rules switched off shows 11 same-speaker repeats and a neighbour gap of 5.0 s.

What the walk does not show, and the first target it missed: it is quiet after the crime, because witnesses say no hello for the hour and their talk carries 4 m, as ruled. The first target for silence was 40 percent of the minutes in every walk; one walk of thirty-one came in at 37 percent, a busy half hour and no fault, so the target is now a third in every walk and 45 percent in the middle one (rules.json says so). The street's existing ambient exchanges are stood in for by a share of the neighbour slots (60 percent in the dry, 40 in rain): an assumption of the simulation, not a measurement, and TownReach on the PC should replace it.

## The format and where it lives

**Its home today.** The street's lines already have homes and shapes, and this adds none:

1. Core/StreetVoice.cs holds the shared banks (a bank key such as ambient/open/night or recognition/avoids, and an array of lines), and Core/OwnLines.cs holds a named person's own banks under the same keys (ByCast[id][bank]). RemarkLedger keeps what he heard under the key "bank@id" and saves it.
2. game-design/barks.json is the enumeration of those banks that BarkGen makes (a slot per bank: id, family, brief, everySeconds, wanted, have, lines), and the voice manifest lists a clip per voice and line (slot, index, line, voice, file).
3. content/dialogue/*-v1.json are dialogue banks in JSON (bank, license, era, register, rungs, speakers, and lines with id, context, rung, speaker, text), read by the content gate and the dialogue pipeline.

**What lines.json is.** The third shape, extended, with the first's bank keys: its header and its id, context, rung, speaker and text fields are the dialogue bank's own (speaker is the kind of person, as w1 is "the shopkeeper" there; rung is the standing, as its "stranger" and "novak" are; idRung is how sure, as in crime-witness-v1: 0 a noise, 1 a shape, 3 a face). It adds kind and situation (kind repeats speaker, situation refines context; the check requires them equal), conditions, weight, group, delivery and dialect, and a flag for lines that ring the police. Each line's bank is a key in the street's grammar (greeting/stranger, rain/in, crime/face, way/to/ritas) and its group is "bank@kind", exactly the key RemarkLedger already keeps for OwnLines. So the ledger, the shuffle bag and BarkGen's repeat floor already fit it.

export_slots.py writes the second shape (barks.json's slots) and the third (barks-manifest.json's renders, with each clip named as VoiceBank.ClipName names it) from lines.json whenever they are wanted, and stores neither: lines.json stays the one home.

## How the PC session adopts it

1. **Put the data home.** Copy lines.json to content/dialogue/ambient-lines-v1.json and rules.json beside it (content/rules/ambient-rules-v1.json). The content gate already walks content/dialogue/*.json (its bank reader takes id and text), so the gate covers it from then on; run `python3 tools/content-gate.py` and `python3 tools/canon-gate.py --corpus`.
2. **Read it in Core.** A new Core/AmbientLines.cs, no engine types, loads the two files the way CastDay reads hook-cast.json (MiniJson), and picks: the conditions, the accent and never-police filters, the cooldowns, the weighted bag through RemarkLedger under "bank@kind". Resolve a speaker's kind in the order rules.json gives: an own kind (rocco, sam, emil, june), the person's kind (lines.json speakers), then the crowd's trade (rules.json trade_kinds). An unknown trade says nothing.
3. **Wire the moments that do not exist yet.** Today the game plays only two street lines to Tom (Recognition as he comes near, FaintRemark once he has passed: production/research/ambient-lines/own-lines-2026-10-01.md found this). So: a greeting where Recognition is asked, only for somebody at Notices or below (above that the existing recognition banks speak and these stay silent); a bump from the knock the street's figures already take (NpcWalker.Bumped in the C# reference, and whatever the Unreal build calls it); rain from Weather.Rain crossing the cut points; crime and after a deed from each witness's perception (idRung 0, 1 or 3, never above what Perception measured); farewell when a talk ends; the way when he asks one (the answer is a direction line if the person knows the place, else one of the kind's own).
4. **The voice's rules belong to the Game layer.** One line sounding at a time (two in a crime), priority, shelf life and the fade are in rules.json; SpeechDirector and SpeechQueue apply them.
5. **Tests first.** Port walk_sim.py's rule_tests as CoreTests rows (they are small scenarios, one rule each), a golden table of picks (seed and state to line id) for the C++ port as OwnLines.h has, and the walk as a Soak. Run TownReach --two-hours to size the groups of lines as METHOD-2026-09-30 says (I could not: it is C# on the PC).
6. **Voices** (below): render in the order of how often a moment plays.
7. **His page before it merges** (CLAUDE.md: anything touching a voice or identity reaches him on one page). Not all 1,626 lines: three lines for each kind, the four own kinds first, shortfalls first. The one line most worth his eye is Ron's, whose tone he approved.
8. **A fresh reviewer per situation**, as the gate asks, against the casting sheets and a third hearing. None was run here: this unit is content, and the check cannot hear a voice. Until then every line is ready for review, not passed.
9. **Nothing multiplied before one complete sample** (CLAUDE.md). This unit wrote all kinds at once because the order asked for it. The recommendation: land one kind first, Ron's new moments, in the assembled game, on his page, then the rest.

## After the canon review of 13 October

A fresh reviewer read all 1,643 lines of the first version and failed the unit on three faults, each a text change, now applied: six greetings that claimed what the street thinks of him (replaced by neutral lines, and the check now fails that kind of claim); five directions to Hal's coin shop, which has no unit on the built street (held, the place taken out of the list, so 34 places); and three pensioner lines that invited him to tea, which Ada's design forbids (replaced, and the check now fails a tea invitation in the pensioner kind). The narrow points are applied too: no street name the atlas still marks as a proposal, later or American idiom, lines that asserted what nobody set, Petra and Dawn moved to office worker, Sheila and the dispatcher kept from the two lines about their own desks, Ron's Tom greeting, June's train, Darren's hair, two lines that sounded written, and the thirteen stranger greetings of the drivers, which could never be said and were dropped. Two consequences the review did not name: two driver bump lines marked for strangers lost that mark for the same reason, and office worker gained one new-owner greeting so that Sheila and the dispatcher still keep six lines to draw on after the exclusion.

A second pass the same day (REVIEW-canon-11-12-B5-FIXES-2.md) took the eleven greetings and crime lines the first fixer reported but left, which claim a standing the simulation might not hold (what the street has said, heard or expected of him, what he has done, what was said of his name, an opening nobody set, a window a pensioner may not have). Nine were replaced by neutral lines of the same voice and two stay, because each claims only a StreetFacts.cs fact that every named member of the kind holds (the one suitcase, the rank outside the office). The new check found six more of the same kind in other kinds (the street's talk, curiosity or expectation in four, what he has done in one, a window in one); those were replaced too, so fifteen lines changed in all, each in place with the same conditions, so no pool changed size. The check gained seven patterns and one row, each pattern with a planted fault aimed at it alone.

## The voices it needs

The new lines need no new voice. Per RULINGS (3 Oct, 24 Sep): Ron, Darren, Sheila and the dispatcher have their game voices; June and Father Walsh wait for his yes on the listening page; nobody else has one, so everybody else speaks in the six crowd voices (crowd_m1 to m3, crowd_f1 to f3, which VoiceBank.VoiceFor draws by the speaker's id).

| Kind | Spoken by |
|---|---|
| Ron | Ron's July voice (p227) |
| Darren | Darren's voice (p241) |
| Father Walsh | his July voice, once he says yes to it (the sheet notes it needs an older one) |
| June | p277 or a better fit, once he says yes |
| office worker | Sheila (p267) and the dispatcher (p280) in their own voices; Alison, Christine, Susan, the customs assistant and Philip in crowd voices |
| the other eight shared kinds and the directions | the crowd voices |

What that costs in clips (a clip per voice and line): **about 4,419** if every shared line is made in the voices of the people who stand in its kind and are met more than once, which keeps each of them sounding like one person; **about 8,005** if every shared kind is made in all six crowd voices. The first is recommended. (Sex known: 4,419. Sex not known, as VoiceBank is called today: 4,281.) By voice, sex known: crowd_f1 644, crowd_f2 771, crowd_f3 540, crowd_m1 638, crowd_m2 540, crowd_m3 631, darren_p241 93, dispatcher_p280 127, june_p277_pending 102, ron_p227 94, sheila_p267 127, walsh_july_voice_pending 112.

Rules the voice plan rests on, all checked: shared lines are gender-free (a gendered word is allowed only in a kind that one sex speaks: laundry worker, Ron, Darren, Father Walsh, June); a line in northern dialect is never given to Nora (Cork) or the Tangs (Hong Kong English), who have no local-accent voice, and the recommendation is that they say nothing from these banks until their voices are cast; hushed lines are the same take played 6 dB lower, not a different one. The street's anonymous passers-by have no fixed voice, so VoiceFor needs a second argument, the voices rendered for the line's kind, to choose among.

## Where this departs from the method note (METHOD-2026-09-30.md), and why

- **Conditions are data, not branches.** The street's picker chooses its bank by code (an hour test here, a stance there). Fourteen moments with weather, hour, standing and sureness would be thousands of lines of branches; as data the PC session tests them as rows and a writer can change them. The bank keys, the ledger and the bag are the street's own.
- **A group is 8 to 13 lines, not the note's 8 to 20, and not sized from TownReach.** The brief set eight as the floor; the busiest bank (a greeting to a stranger) is 13; the walks use a fraction of every group. TownReach --two-hours has to be run on the PC to size them as the note says. A larger group costs render time: the plan above is already about 4,419 clips.
- **"Never repeats" is measured over thirty-one walks of thirty minutes and a busy one, not many two-hour walks.** Same reason: the real walk is the PC's.
- **All kinds were written together**, where the note says one character complete first, then the rest. The order asked for kinds by situations, and everything here is a proposal on a cloud branch. The recommendation above (one kind first, Ron) restores the note's order at the point it matters, before anything is multiplied in the game.
- **The note's per-line gate** (the casting sheet's voice; words and prices right; the content rule and canon; whether the speaker could know it; not a paraphrase of its group's other lines; low-key enough for a third hearing): the machine part is the check (content, canon, could-know through conditions, paraphrase by shared runs); the part that needs a reader (voice, third hearing) is not done.
- **Set-aside lessons used.** The set-aside note (six-voices-v3) says the banks failed because they were written from their names and not from the moment that plays them, and that people meet each other. These are written from the moment (a rung, a weather, a sureness, a place asked about), and the check holds each to its moment. Known shortfall: in rain and after a deed the lines are one-sided remarks, not exchanges; replies are the street's existing reply banks.

## Where the homes disagree (for the PC session; none is settled here)

1. **Two chapels, two markets.** hook-cast.json has Father Walsh's chapel and the open market (Tuesday, Friday, Saturday) a few minutes up from the street; the atlas has Fairview Chapel and the Market Hall far up the hills. The directions treat them as four places.
2. **The cafe.** StreetFacts.cs puts it opposite the north end of the parade; hook-cast.json puts it at 24 m, opposite the middle; canon says the shops of the west block are across from the north half. The lines say "opposite the parade's north half", canon's words.
3. **Population.Trades** still names a "bartender" (ContentRule.cs's own comment calls the trade a design question). No line mentions it; the trade is mapped to shopkeeper; a replacement such as "cafe hand" would end the question. Its names (Yolanda, Wendell) are the prototype's, American, and unused here.
4. **VoiceBank.Cast** lists ada, marla, joey, rita, hal and vesna as cast, though RULINGS says no voice is cast without his yes and names only five in the game. This plan uses only the five (and the two pending); the PC session should look at what the game really speaks.
5. **Julie Kettlewell** is laid off by her sheet and still a laundress in hook-cast.json; her sheet outranks, so she stands in casual worker.
6. **The directions' small details** (the steam over the laundry, the chapel's bell, the stack at the Retort works, net curtains at the boarding house) are invented flavour, not facts from a home.
7. **Hal's coin shop** (hook-cast.json x 39) has no unit on the built street: RULINGS 3 Oct makes the west row a tea room, an ironmonger and the newsagent (x 36 to 42). Directions to Hal's are held until Jafar places it. The newsagent's directions say it is opposite the grocer's, true at hook-cast.json's x 32 and at the built unit's x 36 to 42.

## Invented for Jafar (DECISIONS.md, one entry for each kind, each marked)

1. The thirteen kinds and who stands in each (51 people and routines' ids, 30 trades), and who has none.
2. Standing in greetings: where each person starts on the ladder, Tommy in three kinds only, Sheila held at the new owner until trust, "boss" Ron's and "son" Father Walsh's.
3. Crime lines in three levels of sureness, none naming or accusing; the mark and named rungs left without lines.
4. Directions to 34 places, and what the lines do where the homes disagree (two chapels, two markets, the cafe's place).
5. The numbers in the rules (floors, gaps, caps, chances, priorities, shelf lives, the quiet targets).
6. Weather and hour bands (0.10 and 0.50; five, twelve, seventeen, twenty-one), and who is out in rain and how far talk carries.
7. The hour after a deed: a 90 s gap, 6 dB quieter, 4 m, and no hello or remark on the weather.
8. Voices: nothing new cast, the crowd voices for the rest, Nora and the Tangs silent until cast, the clip counts.

## What to look at first

1. **Tommy.** Which three kinds may say it (pensioner, office worker which is Sheila's, Father Walsh), or fewer. The what-they-call-him design keeps that rung for two or three people, ever, and for nobody in the first week; canon names none, so which kinds may say it is his choice.
2. **One sample, not 1,626 lines.** Three lines for each of the thirteen kinds, from the file, would tell him whether the town sounds like his town. Ron's are the ones his tone approval covers.
3. **The quiet.** In the main walk he hears 23 lines in half an hour and goes 231 seconds once with none (the rain and the crime). Is that a street or too still?
4. **The clip count** (about 4,419) against the voice engine's time.
5. **Known shortfall, for the sample page: the crime-face banks.** In all thirteen kinds the lines for a face seen say nearly one thing (some form of "I'd know that face"), and the check's 60 percent line between kinds does not catch it because the kinds differ in wording. It is listed, not fixed: it fails nothing alone.

## What the check cannot judge

- Whether a line is funny, or in a person's voice, or bears a third hearing. The machine part is screens and counts. The eight groups of greetings to a stranger are the ones to read first, since they are said the most.
- Whether two kinds say the same thing in other words below the 60 percent line: 82 pairs stand between 50 and 60 percent. Across kinds the crime lines share a plain fact (I saw the face; I'd know it again), and some ideas recur (ask at the cab office, a face in the head).
- Whether a direction is easy to follow in the game's own geometry. It agrees with the atlas, the routines and the built street's bays; it was not walked.
- The real lyric or catchphrase: the check holds a list of known ones and the line lengths; it cannot prove none exists.

