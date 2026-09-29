# A sweep for the town lane, eleventh pass, 29 September 2026

What this is: since the tenth pass the town built the arrest, the police
asking, the damage found in the morning, the town's hourly rounds, Sheila's
trust and the week's end (bp to ca). Everything open on the list is waiting on
Jafar (i, q, aq, as, bj, bp, bu, bv, bz, ca). This pass reads the first hour
and the outline through to day 7 against what is now built, the archived
checklist's open rows cited nowhere, and FINDINGS. It looks hardest at how
today's pieces meet each other, since each was built and measured on its own.
None of the four needs a model call or the graphics card.

## Candidates, most important first

1. **Her words promise what his answer does not do** (the first hour's day 7;
   the outline's Act I; A33.19, "completed objectives not continuing to issue
   obsolete instructions"). About 2.5 h.
   Why: told "Wind it down", Sheila answers "Right. I'll close the book on
   it", having just said it means "Mickey's arrangements finished". That
   evening Ron still brings Mickey's envelope for the landing. Her day is an
   ask night: the asks fall every other day from day 0, so 0, 2, 4 and 6, and
   her question falls on day 6. Told "Take it over" after he has already told
   Ron no, she offers him "Mickey's arrangements and everything that comes
   with them", but the outfit is gone for good.
   Not done: Arrangement ends only by a no or three nights away (Arrangement.cs:
   116, 119, 193, 198), and nothing in it reads WeeksEnd. WeeksEnd is used only
   by StreetVoice, TownSave, the talk program and TownReach. WeeksEnd.cs:38
   says "What each answer does beyond that is Act II's". Her words are fixed
   whatever the arrangement's state (WeeksEnd.cs:71-72, 83-84). Neither piece
   is ported yet, so the fix costs the builder nothing.
   The work: a question for Jafar: **(a) winding it down ends Mickey's
   arrangement that night: Ron carries word down to the landing, and it
   becomes the outfit's talk as a no does. Taking it over never undoes a no
   (recommended, since her words already say so); (b) her words change
   instead, and only his no to Ron ends it.** Build (a) meanwhile. Her plain
   question and her answer to his yes follow the arrangement's state ("that's
   done with already"). Ron remembers it, as HeardNo has him remember a no.
   Then TownSave's replay, SaveChaos, TownReach --week-end with the
   arrangement standing, the independent check, the changed words on his page
   and a line under Handovers.

2. **A threat said to a witness goes nowhere** (no row names it; nearest
   A15.07, "suspicious behaviour and an openly hostile act"; set aside in the
   fourth pass as a design ruling, now due before friends play). About 6 h;
   may prove bigger.
   Why: in the slice, Sheila or Ada sees him at the window and asks him about
   it. The most natural answer a player types in a crime game is a threat
   ("Say a word and you'll regret it"). Today the town never learns he
   threatened anybody. The threat never makes them warier and never becomes a
   story. The character can only react in words the Core does not hold, so
   the next day the town treats him as if he had said nothing.
   Not done: Silence.AsksQuiet refuses any line carrying a threat or money
   ("or else", "you'll regret", Silence.cs:107-113), leaving it to "Gossip's
   Bribe and Intimidate" (Silence.cs:22). In play, only the retired Unity
   layer calls Intimidate (DialogueUI.cs; otherwise only tests, BalanceLab and
   SimHarness do), and the talk program reads only owning up and asks for
   silence (TalkHelper Program.cs:792-793). Intimidate cannot simply
   be wired in: it silences anybody with nerve at 0.6 or under
   (Gossip.cs:922, 989), and every one of the forty has the default 0.5
   (Gossip.cs:86; their own traits are bj, with Jafar), so every threat would
   work on everybody.
   The work: a question for Jafar: **(a) this week a threat never buys
   silence. It is itself the street's story ("the new owner threatened me
   over the window"), and it makes them warier (recommended until bj gives
   the forty their nerve); (b) it silences those of low nerve, once bj is
   settled; (c) threats stay unread.** Research first what threatening a
   witness was in law and on such a street in 1990. Then read a threat about
   a deed they hold in narrow shapes, the way Silence reads an admission
   (missing one costs less than inventing one). The Core decides, the
   character is told the outcome, and the story is filed. Also the session
   record's `deed`, the talk protocol page, and the independent check, which
   took five passes on the no to Ron.

3. **The week on paper, all seven days, every piece together** (ROADMAP stage
   4, the first hour; A33.18, "sensible handling of multiple simultaneous
   missions"). About 3 h.
   Why: the asks, Ada's tea, the police file and DS Ellis's asking, the
   constable and custody, the damage found, Sheila's trust and her question
   were each measured alone. Candidate 1 is a collision between two of them
   that no measurement could show. What a friend's week actually does has
   never been run from day 1 to day 7.
   Not done: TownReach --first-hour stops at minute 60 (Program.cs:369). It
   runs its own copy of the rounds (417), not TownRounds.Hour, which is the
   game's call since bs. It has no window, Aftermath, Custody, Trust or
   WeeksEnd, which run only in their own modes (--found, --arrest, --week-end;
   the last starts from an empty town on day 6, Program.cs:230-243). One
   meeting to check: trust is barred by any deed he was seen at (Trust.cs:37),
   and the slice's one deed is seen by Sheila at Mickey's rank (NOW,
   Handovers, 6ac). So a friend who plays the slice's crime may never see the
   real book.
   The work: a --week mode for the eight choices of the first hour on paper,
   with the window seen by Sheila, by Ada or by nobody. It runs TownHours.RunTo,
   the window and its Aftermath, PoliceFile with Asked and ConstableComes,
   Custody, the asks, the tea, her trust from talk days and her question. It
   gives a table for his page: when DS Ellis comes, whether he is taken,
   whether she trusts him by day 7, which book, and who holds his answer by
   Monday noon. Faults it finds are fixed or put on the list.

4. **What the session record keeps of the tea, the damage found, her trust and
   his answer** (ROADMAP stage 5, Meridian condition 2). About 1.5 h.
   Why: Ada's tea (day 3) and the window's damage found the next morning
   (day 2) both fall inside a friend's half hour. Neither is recorded, so a
   playtest cannot say whether friends sat with Ada. Nor can it count the
   street finding his damage as the town reacting to what he did. Sheila's
   trust and the week's answer are missing too, for longer sessions.
   Not done: the record's lines are start, place, still, deed, known, talk,
   named, load, reply, hint, ask, police, ellis, taken and end
   (production/specs/session-record.md:27-41). tools/session_read.py knows no
   tea, found, trust or week. TeaState (FirstWeek.cs:7) and Aftermath.Tick's
   finders (TownNews.cs:186) are there to write.
   The work: `tea` (the state), `found` (who, the deed; counted as the town
   reacting to it though it names nobody), `trust` and `week` (the answer, its
   story counted as a deed). Add them to the spec and the reader, with
   warnings for unknown words, the self-test, and a line under Handovers.

## Considered and set aside

- The dead stay in the town's rounds: TownRounds.Hour and CastDay have no
  alive filter, and nothing new passes Homicide's. Set aside a third time
  (NOTE-2, NOTE-3), since there is no killing in the playable build.
- Act II in the Core is July's pub, with "one slow beer" and "Kids' stuff"
  (ActTwo.cs:50, 53), which the content gate does not read (its corpus,
  tools/content-gate.py:789-816, has no Core source). Retired with the Unity
  layer (FINDINGS). Act II's new text comes with Act II, after the week's
  answer.
- Philip Danby, "still to write" in the outline, is not among the forty
  (hook-cast.json). Adding him moves the port's golden table, and a card for
  him waits on the multiply rule.
- The cab office's own fares and takings: Act III reads them
  (ActThree.cs:76-77), but nothing in the new game makes them, and the first
  hour needs none. They belong with Act III.
- Money offered in talk: the first hour has no money beyond the envelope.
- The talk's suspicion against the port's (FINDINGS): the builder's wiring;
  the protocol already takes the game's level (talk-protocol.md:42).

Evidence from b4ddf1d7
