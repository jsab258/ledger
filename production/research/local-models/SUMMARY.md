# Can the game talk without the paid model? The part that picks actions probably can, and training should come last

The research topic on local models. The full write-up with every source is
DELIVERY.md beside this file. Written 23 September.

## For you

Normally these would go in FOR-JAFAR.md. The brief said this topic writes only
in its own folder, so they are here, and they need copying across when the
branch is merged.

**Decisions waiting on you**

- **May I download four free models to test them on your card?** About 10 GB in
  all, every one free for any use (Apache licence), kept outside the project and
  never committed: Ministral 3 3B (2.2 GB), Qwen3.5 4B (2.7 GB), Gemma 4 E4B
  (5.0 GB) and Qwen3 1.7B (1.1 GB).
  - **(a) Yes (my recommendation).** This is the cheapest real test there is.
  - (b) Only the two smallest.
  - (c) Not now.
  - Meanwhile: the first two steps need no download, and I would do them first.
- **May I spend about 35 pence running the paid model on the new test lines?**
  That gives a fair score to beat, on lines nobody has tuned anything on.
  - **(a) Yes (my recommendation).**
  - (b) No: compare against the 42 lines only, which can't tell a good model
    from a very good one.
- **Anthropic's rules forbid training a model on the paid model's answers**
  without their permission. That also covers anything I write, since I am
  Claude too. It only matters if we get to training, which comes
  last.
  - **(a) Use a large free model as the teacher, run on your own PC overnight
    (my recommendation).** Free, and no permission needed.
  - (b) Ask Anthropic for written permission. That's a message you would send.
  - (c) Write the training examples by hand.
  - Meanwhile: nothing depends on this until the last step.

**Things you should know**

- 2026-09-23 The small model's 33 out of 42 was measured before the game started
  blocking typed commands itself. The paid model's 41 includes that help. Rerun
  fairly, the small model probably gets about 36. Rerunning costs ten minutes.
- 2026-09-23 The 42 test lines are too few to tell a good model from a very good
  one, and three of them are nearly copies of the examples in the model's own
  instructions. A fair test needs about 300 fresh lines, written before anything
  is tuned.
- 2026-09-23 Only the half that picks the action can go local on this evidence.
  The half that writes the spoken line needs a bigger model than your card has
  room for beside the street and the voice.

## The answer

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
claims to run on the processor is Resemble's small "Nano", which can't do moods.

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
