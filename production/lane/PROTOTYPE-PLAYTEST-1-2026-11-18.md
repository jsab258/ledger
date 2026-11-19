# Prototype playtest 1: the AI playtester's first run (18 Nov 2026)

Written by the cloud lane (advisor item 4k, from his playtest of 13:02). The loop prototype as published on its page (version 1794997640-def7, Fable's second round, built here byte for byte from the readable source) was played by tools/lane/prototype/playtester/ in headless Chromium through the game's own test hook, seed 19901120. Two runs: the sweep (every person at 9.30, 13.00, 18.00 and 22.00 on Tuesday, three approaches each, then a talk with everyone) and a scripted newcomer's first hour. A fresh helper then read the transcripts and looked at every screenshot as a player would. Live AI talk runs only inside claude.ai, so only the written lines were tested: live talk is untested. Rerun: python tools/lane/prototype/playtester/playtest.py --assets DIR (or the prototype's test command, where it now runs last).

## In short

His three findings are confirmed and measured. The talk prompt picks a named person off to the side over the person right in front (10 cases in one sweep). Most named people answer the suggested questions with the same four stock lines, and several say one line again and again (Sheila the same sentence to five questions in a row, Ada one sentence ten times over three short talks). In the newcomer's first hour, 39% of play time was waiting with nothing to do, 37% talking, 21% walking and 3% driving; after the first half hour nothing new of its own kind arrived, and one stretch ran 11.5 minutes with nothing new, against Study 2's limit of about 5.

## Faults, ranked by how much they spoil play

Obvious bugs (for the Fable fix round):

1. Talk gives nothing back. Named people fall back on stock lines anyone says ("Same as ever. Less of it.", "Aye, well. There it is.", "You get used to the quiet. You never get to like it.") for most suggested questions; the sweep counts 5 or 6 stock replies in 6 turns for June, Alison, Walsh, Pauline, Kevin, Terry, Rita, Brenda, Grace, Lily, Hal, Susan, Nora, Shaun, Peter, Norman and Sylvia. Several repeat one line word for word: Sheila "The weather isn't in the book. I only discuss what's in the book." to five questions in a row; Ron "Thirty years on the dock, I never minded rain. It's the standing still." four times; Ada "Sit a day at this window and you'll not need the wireless." ten times across her three talks on Wednesday morning (four in one talk). The shared answer about Mickey ("He'd have liked the turnout. He'd have counted it.") comes word for word from five people: Susan, Alison and June in the newcomer run, June, Father Walsh and Sylvia in the sweep. Reproduce: Tuesday 9.30am, talk to Sheila (or Ron, or Ada on Wednesday) and pick any three suggested questions. Evidence: sweep table (stock and repeats columns); newcomer transcripts.
2. The talk prompt names someone other than the person in front. With Tom facing a person 1.2 to 2 m away, the prompt (and E) goes to someone else, mostly a named person, up to 2.7 m away and up to 37 degrees off to the side: "Talk to a young woman with a carrier bag" in front of a 65-year-old woman; "Talk to the night watchman on the row" in front of Terry; "Talk to Darren Milner" in front of a lad in a shell suit; "Speak to a man" in front of Albert (a nearer stranger 37 degrees off: the wide cone, not the named bonus). The three Terry cases have the night watchman on the very same spot as Terry, so they show two people standing in one place as much as the picker's bias. In his own play the same rule gave "talk to woman" over a man. Cause in the source: the target picker accepts anyone within 3.6 m and 69 degrees of Tom's facing and counts named people 1.2 m nearer than they are, and marked people a further 1 m (fight.js target(), LEDGER.rules ladder.targetWithinMetres 3.6, ladder.targetWithinFacingRadians 1.2, ladder.namedPreferredByMetres 1.2). Reproduce: Tuesday 9.30am, stand 1.2 m in front of the old woman passer-by near Julie and read the prompt.
3. Speech with nobody there, and the same line twice at once. Bubbles such as "Aye." and an empty "..." float on walls or in black; Peter and Lily say "They say you keep funny hours" (Lily adds "Mr Nowak") at the same moment, as two stacked subtitles, with neither on screen. Reproduce: Tuesday 1pm and 6pm by the Golden River hatch. Evidence: sweep shots 02 ("Aye." on the scrap pile) and 03 (the same "Aye.", and Peter and Lily at 6pm), newcomer shot 08 (the empty bubble on a house front).
4. Lines out of time. Terry greets with "Evening." at 9.30am. Reproduce: Tuesday 9.30am, talk to Terry.
5. A name shown before it is learned: "Speak up to Ada at her window" on Tuesday before Tom has met her, with Ada not in view. Evidence: newcomer shot 07.
6. The to-do note goes stale: on Thursday just after midnight it still says Ada wants him for tea "at seven tonight", after the hour has passed with nothing said. Evidence: newcomer shot 12.
7. Some talks stop dead after a debt line, with nothing further offered (Wayne, Lee, Julie, Dennis in the sweep). Needs a check by hand: the tester answered the debt with no, which may close the talk on purpose.
8. Paying for help buys nothing: Ron takes a fiver and says "Nobody saw a thing"; Darren takes 3 pounds and says "Nothing going round that I've heard." A player reads it as money thrown away. (Darren's second payment, a fiver for a good word put about, he says he will do, so that one is not counted.) Reproduce: Monday, pay Ron, then Darren.

Probably the tester's own doing, to check by hand before any fix: a black screen at Wednesday 12.05pm on Quay Street (shot 10, taken just after a script move); the camera inside a lamp post, the cab's bonnet, or outside the takeaway (shots 03, 09, 11, 12), all right after the script moved Tom in a straight line through solid things.

Not faults: the PLAYTEST ASK panel is the prototype's own test design; the Tuesday to-do names no person or place on purpose ("Walk the street").

Design feel (for the main session and the real game, not a Fable fix under his prototype rule):

9. Too much waiting and talk, not enough doing. First hour, booked by activity: waiting 23.5 min (39%), talking 22.6 (37%), walking 12.7 (21%), driving 1.8 (3%); fighting and night-job actions 0 (the scripted newcomer never reached the night job: untested, not proof that it is missing). Most of the waiting is the script's own choice: 15 of the 23.5 minutes are "nothing to do" steps, booked when the scripted newcomer had no named person left nearby, and it never opens the Ledger, tries a door or seeks the night job. The figure shows the street gives a newcomer no next step after the first half hour; it does not measure how long a human would stand idle.
10. Thin cab work: three fares in an hour (1.40, 1.40 and 3.10 pounds); three times two minutes in the cab with no fare offered.
11. Strangers give one remark and no talk (17 people bark only in the sweep). Fine for passers-by in AAA games; listed because he noticed it.

## The activity mix against Study 2

| | Study 2 (Mafia DE, KCD2, first 30 min) | LEDGER prototype, newcomer, minutes 0 to 30 | minutes 30 to 60 |
|---|---|---|---|
| Distinct activities | about 10 in both | 5 kinds (walk, talk, sit in the cab, drive, take a fare) | no new kind |
| New things (places, people, scenes) | something new about every 3 min | 48 (mostly first meetings and their scenes; 52 counting the first four actions, the like-for-like figure, since Study 2 counts controls) | 11 |
| Longest stretch with nothing new | about 5 min | 4.4 min | 11.5 min (from minute 30.2) |
| Watching or waiting (not like for like) | 18 to 44% watching | waiting 39% of the hour, watching not booked | |

Reading: the first half hour is full of people and scenes but has only five kinds of thing to do; the second half hour runs dry. Study 2's figures are estimates from the games' files and reviews (Study 2's own marks); the prototype's are from the tester's booking with stated estimates (walking 2.2 m/s, driving 8 m/s over 1.35 times the straight line, reading 3.3 words a second, 3 s a choice), not from a human player. Game time runs much faster than real time here: one booked hour covered Monday 3.30pm to Thursday 10am, mostly through the waits and the forced nights.

## What the tester cannot see

Live AI talk; walls along a walk (Tom is moved in straight lines); fights and the night job (not reached); key-press feel; sound. A human playtest stays the judge of feel.

## Next

- Fable round: production/lane/FABLE-PROTOTYPE-FIXES-1.md (faults 1 to 8 only, under his prototype rule).
- After that round: rerun the playtester; faults 1 and 2 should show as near zero in the sweep table and the prompt list.
- For the main session: faults 9 to 11 feed the real game's first-hour plan (Study 2's adopt list) and the talk design, not the frozen prototype.
