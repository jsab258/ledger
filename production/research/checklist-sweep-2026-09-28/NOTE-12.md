# A sweep for the town lane, twelfth pass, 29 September 2026

What this is: since the eleventh pass the town built what winding it down does
(cc), threats as far as words go (cd), the whole week on paper (ce) and the
record's four new lines (cf). Everything open on the list is waiting on Jafar
(i, q, aq, as, bj, bp, bu, bv, bz, ca, cc, cd). This pass reads a friend's
first minutes against what is built, the parts of the approved first hour that
nobody has written, the name ladder canon sets out, and how a way to wait
(recommended on his 30 September page) would meet today's pieces. Run again at
this commit, the week on paper gives the same sixteen rows. None of the four
needs a model call or the graphics card. Two carry a question for Jafar.

## Candidates, most important first

1. **Day one has no words: Sheila's walk-round, and the street's first talk
   of him** (the first hour's minutes 0 to 7; the outline's Arrival; A04.05, "a
   clear initial purpose"; A04.16, "an opening that permits ordinary
   experimentation without trapping the player"; A32.12, "correct state
   changes even when a scene is skipped"). About 5 h.
   Why: this is the first minute of every friend's session. In the approved
   first hour Sheila meets him, shows him round, stops at the one door she
   does not open, and then sends him out ("That's Ron on the rank. Go and say
   hello."). The hint to talk fires when her walk-round ends. None of the
   walk-round is written, so the builder has nothing to stage and the talk
   hint has no moment to fire on. The street also has nothing to say about
   him until night one's story reaches Darren at breakfast, minute 13 of play
   (first-ask-2026-09-29.md:75). Until then nobody who saw him arrive shows
   it, though the outline says "the first thing the town does is talk". By
   the routines, seven of the forty are at Mickey's rank, its office or Ada's
   step at nine on the Monday (hook-cast.json).
   Not done: "walk-round" appears only in the first hour, the hints page and
   FirstMoments.cs:15, 28, where CanTalk fires "when Sheila's walk-round ends
   at the office door". Her one line is its last (FirstMoments.cs:76). No Core
   piece or design page holds the walk-round's lines, or what it leaves
   behind. The game counts someone as "met" only once he has talked with
   them: "the first hour's walk-round, which would make Sheila's the first, is
   not built yet" (CrimeProbe.cpp:3057-3059). Nothing about him is filed
   before a deed. StreetVoice.StoryThatShows shows only these stories: his
   night, the outfit's nights, the police asking, his being taken, the week's
   answer and a threat (StreetVoice.cs:354-372). No story of his arrival
   exists. Sheila's card has one line he might hear first ("New management.
   Sit down, you're making the place look untidy.", lena.md:16).
   The work: a small Core piece for day one, in two parts.
   - The walk-round: a few fixed lines in Sheila's words, in order: the
     office, the fare book and the radio, the rank and Ron, the door she does
     not open, where he sleeps. They are written from canon and from the
     street's plain facts as recommended on his 30 September page (the door
     is Mickey's own office, locked; the flat over the office), built that
     way meanwhile. It leaves the same state whether it is played or
     skipped: Sheila has met him, and the talk hint's moment has come.
   - His arrival as the street's first story about him: first-hand for
     whoever of the forty is about Mickey's when he comes, naming no deed,
     and passed on by the town's rounds. It is said to his face once, in a
     bank of its own, by someone who holds it and can tell it is him ("You'll
     be Mickey's nephew, then."). It weighs nothing on how they stand to him,
     as the police asking does not (StreetVoice.cs:523).

   Measured on the forty (TownReach): how many hold it by nightfall and by
   noon on day 2, and when it is first said to his face. The lines go through
   the content gate onto his page. They show as plain text until Sheila's
   voice passes the accent gate, as the hints do. A line under Handovers.

2. **What the town calls him: canon's ladder, by knowing** (canon.md:88-89;
   the outline's "what it calls him says how far he has got"; A38.02, "a
   readable current level or equivalent advancement state"; A38.07, "visible
   acknowledgement of meaningful milestones"). About 5 h, with a question for
   Jafar inside.
   Why: canon names one readout of his standing: the new owner, Nowak, Tom,
   Tommy, and "the gate is knowing, not liking". Jafar ruled that everyone but
   Sheila follows it (DECISIONS.md:92). Today nobody does:
   - The game sends no name, so in talk Darren calls him "the new owner" all
     week, even after "I'm Tom".
   - The Core rule the handover tells the builder to port runs on liking, and
     backwards. It starts everyone at Tom and drops them to Nowak when they
     cool on him. After one evening of tea, Ada would call him Tommy, which
     canon keeps for "two or three people, ever".
   - The same name decides who keeps a deed quiet for him ("only for someone
     on first-name terms", DECISIONS.md:75).
   - It is one of the signs Tom's reading needs
     (production/research/ending-reading/NOTE-2026-09-28.md:64).

   Not done:
   - PlayerIdentity.AddressBy(Gossiper) passes g.Loyalty as closeness
     (PlayerIdentity.cs:137-138): Tom from 0.45, Tommy from 0.75 (59-65).
     Loyalty is "goodwill toward the player", 0.5 for all forty (Gossip.cs:84,
     87). Ada's tea adds 0.25 (FirstWeek.cs:49, 115).
   - KnowsName is any memory at all (PlayerIdentity.cs:103-104), so a rumour
     that calls him "the new owner" teaches his name. CoreTests pins both ("one
     memory of you is enough to learn it", "and a friend uses the short one",
     Program.cs:10359-10360).
   - Nothing reads him giving his name: grep finds no reader for "I'm Tom" or
     "call me Tom" in the Core or the talk program.
   - The game sends acquaintance without "calls" (CrimeProbe.cpp:3060-3067),
     so the talk program uses the new owner (Program.cs:515, 606).
     Silence.Agrees takes first-name terms from that same "calls"
     (Program.cs:806; Silence.cs:283).
   - Not ported, so no golden rows move.

   The work: a question for Jafar:
   - **(a) by knowing him (recommended; canon's rule). Nowak once they know
     his name: he told them, somebody who knows it passed it on, or they are
     Mickey's own people (as his other answer on the 30 September page
     settles). Tom once they have talked with him on two different days, or
     sooner if he asks them to. Tommy for nobody in the first week. A rung
     never falls. Sheila stays the exception, and Ron's "boss" stays his.**
   - **(b) as the code has it, by goodwill: Tom at once, Nowak for those who
     cool on him, Tommy after Ada's tea.**
   - **(c) only Mickey's own people use his name in week one.**

   Build (a) meanwhile:
   - The rung, worked out from knowing, in the Core, in place of AddressBy's
     goodwill.
   - A narrow reader in the talk program for him giving his name: the whole
     clause, as Silence reads an admission, since missing one costs less than
     inventing one. The program then works out "calls" from its own talk days
     when the game sends none.
   - His name passed on by the town's talk as a plain fact, never a secret.
   - The tests pinned again.
   - The week on paper (--week) says who calls him what by days 2, 3 and 7.
   - A `calls` line in the session record, the first time somebody uses his
     name.
   - The independent check, the protocol page, and a line under Handovers in
     place of "calls from AddressBy".

3. **A wait that stops for what the town has for him** (A25.11, "a wait or
   sleep mechanism where schedules make waiting necessary"; A25.12, "safe
   handling of time skips with active missions"; A15.19, "no punishment for
   an action the controls misleadingly presented as harmless"). About 3 h.
   Why: his 30 September page recommends two game minutes a second "and a way
   to wait until evening", a basic the game needs anyway. To the Core a wait
   is skipped hours. If he waits through the week's beats, each passes
   silently or turns against him:
   - The night-one ask passes unasked if Ron never found him. No story then
     exists, so nothing comes back on day 2, the first hour's step four.
   - A tea Ada asked him to becomes a stand-up. In the week on paper that is
     the one road to his arrest: Ada saw the window, reports him once he has
     stood her up, and he is taken on day 5.
   - DS Ellis's visit, the constable at ten and Sheila's question on day 7
     all happen while he is away.

   One key would do what the game never warned him of.
   Not done: TownHours.RunTo runs skipped hours ("asleep, in the cells, a
   load's jump") with nobody on the street (TownRounds.cs:80-99). Nothing says
   when a wait must end. Each piece knows its own times, and nothing gathers
   them:
   - Arrangement.NextNight and AskStands (Arrangement.cs:166, 178). An ask
     Ron never delivered passes silently (17-18).
   - AdasTea.From and ArriveByMinute (FirstWeek.cs:44, 48). No minutes with
     her is StoodUp (93), which costs her goodwill (128).
   - PoliceFile.ConstableComes and EllisComes (PoliceFile.cs:101, 262).
   - WeeksEnd.Waits (WeeksEnd.cs:145).
   - Custody.OutAt (Custody.cs:41).

   The work: one Core call. Given the time now, the time he asks to wait
   until and where he waits, it returns when the wait must stop and why, in
   plain words ("Ron's at the door with something for you.", "Ada's pot is
   on.", "There's a constable asking for you.", "Sheila's waiting in the
   office."), read from each piece's own state. It needs an hour for Ron's
   "after dark", and in custody a wait runs to OutAt. Tests at each beat.
   TownReach --week with a wait every evening, showing nothing changes beyond
   what those hours would have done anyway. The handover.

4. **Nobody at the landing says anything** (A33.05, "completion acknowledged
   rather than silently recorded"; A33.06, "rewards actually delivered and
   explained"). About 2 h.
   Why: most friends will carry the first envelope, on night one, around
   minute 10. The job ends with a man who says nothing. The game records the
   night, but nothing tells the player the job was done, what he did, or
   when the next ask comes. A friend meets the same silence arriving early,
   empty-handed, on a night with no ask, or after telling Ron no. Talking to
   the man gives nothing either: he has no talk card.
   Not done: the design gives the job and "the man who asks for Mickey's", but
   no words for him (first-ask-2026-09-29.md:51-55). Arrangement's lines are
   Ron's and the street's (Arrangement.cs:89-113). The handover asks only for
   "a body at the ferry landing at night" (NOW.md, Handovers, 6z). His routine
   has him there from ten till one (hook-cast.json, outfit_man). Nothing in
   Arrangement answers a visit that is not a handover.
   The work: a handful of fixed lines for him in the Core, chosen by the
   arrangement's state:
   - the handover ("Mickey's? ... Right. Two nights, same again.");
   - empty-handed on an ask night;
   - no ask tonight;
   - finished with ("We're done, you and us.");
   - a brush-off when spoken to.

   Each is said once, and none names what is in the envelope. They show as
   plain text, since no voice is cast for him without Jafar's yes. Through the
   content gate, onto the first-ask page beside Ron's lines, with a line under
   Handovers.

## Considered and set aside

- DS Ellis's words when she comes: her talk card waits on the multiply rule
  (NOW.md, Handovers, 6ar). The same goes for June at Mickey's office every
  morning, and Ada, who has no answer to give when she asks him in.
- What he says travelling further than owning up, his claims, a threat and
  the week's answer: this is a design across all of talk. The nearest step is
  the threat question's "the checking model judges", so it waits on his
  answers.
- Every new game is the same town: the routines, the asks and the week are
  fixed, and the street's words vary only in wording. Variety between
  sessions is scope, and touches the deterministic Core in the moat, so it is
  stage 6's to raise with him.
- The talk's save and the town's save are written apart. Both are written at
  the game's save (the 6r and 6bl handovers), so they fall out of step only
  if the game crashes between the two writes.
- Sheila trusting him though he carries the envelope every night (the week
  on paper): already part of the trust question on his page.
- Tom's reading (i) and the Ledger (as): his.

Evidence from 83688abb
