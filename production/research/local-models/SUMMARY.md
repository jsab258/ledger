# Can the game talk without the paid model? The part that picks actions probably can, and training should come last

The research topic on local models. The full write-up with every source is
DELIVERY.md beside this file. Written 23 September.

## What the measurements found (23 September, evening)

You said yes to all three questions, and the experiment ran on your card the
same evening. The full table is in RESULTS.md beside this file.

- **No free model on your card picks actions as well as the paid one yet.** On
  299 fresh test lines the paid model gets 259 right. The best free model gets
  251 with better wording, and today's model gets 216 as it ships. Leave out the
  lines where the test itself is arguable (explained below), and the paid model
  gets 252 of 264 with 10 tidy-but-wrong answers. The best free model gets 235,
  with 27 tidy-but-wrong. Those are the answers the game would carry out without
  noticing they're wrong.
- **The old 42 lines flattered everyone.** The paid model's 41 of 42 becomes
  87% on fresh lines, and today's model's 32 becomes 72%.
- **Better wording helps, but it trades against safety.** The changes that lift
  the score also make the model obey more of the typed orders that get past the
  game's own block.
- **Every free model obeys most of those orders.** The paid model obeys 16 of
  39. The free ones obey 25 or more.
- **Worked examples picked per line: EXAMPLES.**
- **Gemma 4 is out**: about four seconds a line, and most answers unreadable.
- **Speed and memory are fine.** Today's model answers in a third of a second
  and uses 3 GB of the card.
- **The arguable lines:** the paid model calls handing someone a scarf, or
  carrying their boxes, "just talk", where the test's writers called it a new
  action. The game's rules support either reading.

**So the cheap routes don't reach the paid model.** Training is now the only
route with evidence it could close the gap. By your ruling, its teacher is a
large free model on this PC, and its first step is checking that teacher on the
same 299 lines. The line-writing half is untouched, as you ruled. It waits on
the slice's card measurement and is queued on the checklist.
## What the research predicted, before measuring

You asked for four routes, cheapest that works. Here is how they come out.

**1. A better ready-made model.** Possibly, and only a test on our own lines can
say. The surprise: on the public leaderboard for choosing actions, the model we
tested sits level with the paid model. Yet on our lines it got 33 against 41.
So the public scores can't pick the winner. What trips small models up is
particular to us: the way people in the game hint rather than say, the tone of
a threat, telling talk from a real action nobody offered, and players typing
orders. Three newer free models, all from this year or late last year, did
better than ours at picking one action in an independent test. The best was
Gemma 4 (96%, and the paid frontier model got 98%), then Ministral 3 (88%).

**2. A larger model, with the voice moved to the processor.** The weakest case.
The larger version of our model is a little better at choosing and worse at
recognising "this is just talk", which is where we lose most lines. It needs
about 5.5 GB. Even with the voice off the card, that doesn't fit your 10 GB card
beside the street; it would just fit a 12 GB one. And the only voice that
can run on the processor is Resemble's small "Nano", which can't do moods, and
on your PC it took 7 to 9 seconds to say 3.5 seconds of speech, too slow.

**3. Better asking, same model.** The best-supported gain without any training.
At the moment the model sees the same three worked examples every time. Picking
the four to eight examples most like what the player just typed added 13 to 32
points for models this size in several independent studies. It costs a tenth to
a third of a second. One line in our instructions actually pushes the model
away from recognising a new action, and removing it costs nothing. Two things
that sound good don't help here: asking several times and voting, and letting
the model "think" first, which takes 3 to 18 seconds a line.

**4. Training our own.** The strongest evidence that a small model can MATCH the
paid one: every study that trained a small model on one narrow menu got it level
or ahead. It needs a few thousand examples and about five dollars of rented
graphics card; your card isn't officially supported for training on Windows.
But the paid model can't be the teacher (see above). A large free model can,
and one that does well at this probably runs on your PC overnight.

**My recommendation: try 3 and 1 first, together, because they cost nothing but
downloads and an afternoon.** Try 2 only if they fall short and you're willing
to give up moods in the voice. Try 4 only if everything else falls short.

## What "good enough" would mean

On about 300 fresh lines, the local model would need to:
- get no more than 2 points fewer right than the paid model;
- give no more than 6 answers that look tidy but are wrong, the failure the
  game can't see;
- obey none of the typed orders;
- answer in half a second with the street running, which is faster than the
  paid model is today;
- fit in the memory the card has left.

Passing that would make a local model worth having as the offline fallback in
your open question about the connection dropping. That's option (c), which I
currently recommend against because small models go wrong without it showing.
Replacing the paid model outright would need more: real players' lines, which
only playtests give.

## The experiment, cheapest first

0. Rerun today's model fairly. Free, ten minutes.
1. Write the 300 fresh lines, plus 40 typed orders built to slip past the game's
   own block. The paid model gets its score on them for about 35p.
2. The free fixes to the instructions, on today's model.
3. The four downloaded models, on the same lines.
4. Examples picked per line, and a second check for new actions, on the best one
   or two.
5. The larger model, only if needed, and only with the voice question settled.
6. Training, only if all else fails. Teacher first: if the free teacher can't
   match the paid model itself, stop.

The first route that meets the bar ends it.

## Licences

Not a problem for any route. Every model named here is free for commercial use
and can be shipped in the game (Apache or MIT). Every model built specifically
for choosing actions that I found is either non-commercial or tied to Meta's
Llama licence, which is why none of them is on the list.
