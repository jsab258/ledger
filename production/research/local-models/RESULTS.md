# The action-picking comparison, measured: no local model reaches the paid router yet

STATUS: MEASURED, 2026-09-23, on this PC (RX 6700, 10 GB, llama.cpp b11111 on
Vulkan, Windows 11). Branch `research/local-models`. It follows the
experiment in DELIVERY.md section 10, in Jafar's order: the fair rerun, the
fresh lines, the models. Every run is in `runs/`, as a report (`.md`) and one
row per line (`.tsv`). The test lines are in `heldout/` (frozen, see its
README), and the worked-example bank is in `bank/`.

## The one table

299 fresh lines, one right answer each. "Tidy but wrong" means well formed and
wrong, the failure the game cannot see. The 35 "novel" lines are counted
separately as well, for a reason given below. The typed orders are the 39 lines
that get past the game's own guard. Median time is for one routed line, with
nothing else on the card except where noted.

TABLE

The paid router is claude-haiku-4-5 with the shipped prompt and guard, run on
this PC through the game's own client and key. The spend was $0.39 (about 30p),
plus about 30p on the GitHub attempt, whose results were lost.

## What it says

1. **No local model reaches the paid router, and the gap is on ordinary
   lines, not novel ones.** Without the novel lines, the paid router gets 252 of
   264 with 10 tidy-but-wrong answers. The best local result there is 235, with
   27. That is 17 more lines wrong, and nearly three times the failures the game
   cannot see. The bar in DELIVERY section 10.7 was: no more than 2 points
   below the paid model, and no more than 1 point above its tidy-but-wrong
   rate. Every local configuration misses it.
2. **The 42 old lines flattered everyone.** The paid model scored 41 of 42 and
   today's local model 32. On the fresh lines they score 87% and 72%. The fresh
   set is harder, and it separates the models where the 42 could not.
3. **Better asking helps, and it is not free.** The three wording changes lift
   today's model from 216 to 242, and Ministral from 237 to 251. But most of
   the lift comes from dropping the fence around the player's line, and the
   fence is what makes typed orders fail. Without it, today's model obeys 31 of
   39 orders instead of 25. Keeping the fence and making the other two
   changes: 229.
4. **Every local model obeys most of the typed orders that get past the guard.**
   The paid router obeys 16 of 39. The best local model that is also accurate
   obeys 25 or more. Gemma 4 E4B obeys few, but only because most of its
   answers are unreadable.
5. **On novel lines the paid router is the weak one, and that is partly the
   test.** It catches 7 of 35 novel lines. It reads handing someone a scarf, or
   carrying their boxes, as talk. The game's own rules say a novel action is
   small and "moves the world", so talk is a defensible reading of a courtesy.
   The test's writers took a broader view. That is why the table counts those
   lines separately. It is a design question the router's prompt answers today
   by default: whether a courtesy is an action.
6. **Speed and memory are not the obstacle.** Today's 4B routes in about a third
   of a second, using 3.0 GB of the card. The 1.7B uses 1.6 GB and is as fast,
   but it is far less accurate (184).
7. **Gemma 4 E4B is out**: about 3 to 4 seconds a line, and most answers are not
   in the form the game reads. The best independent single-call score of any
   small model did not carry over to this job. That is the finding the
   delivery predicted: public scores cannot rank candidates for this job.
8. **Qwen3.5 4B gives the same answers on the card as on the processor** (37 of
   42 both ways), so the Vulkan reports of wrong output did not bite here. Nor
   did they for Gemma (22 against 21).

## What this means for the routes

- **Route 1, a better ready-made model:** the best is Ministral 3 3B or Qwen3.5
  4B, each about 20 lines short of the paid router on the 264 non-novel lines.
  Not enough.
- **Route 3, better asking:** worth 13 to 26 lines on today's model, most of it
  from a change that weakens the defence against typed orders. Worked examples
  picked per line: RESULT.
- **Route 2, a larger model:** not tried. It needs the voice off the card,
  which the Nano measurement says cannot happen in real time on this PC.
- **Route 4, training:** now the only route left with evidence it could close
  the gap. By Jafar's ruling, the teacher is a large free model on this PC.
  The first step is to check that teacher on these same 299 lines.

## Caveats

- The test lines were written and labelled by Claude models, and three of them
  agreed on 338 of 339. The labels are Claude's consensus, not a person's.
- Answer times were measured with a stray Unreal check running on the PC
  runner for part of the bake-off (see FOR-JAFAR). The times for today's
  model and Qwen3.5 in that window are high. The scores are unaffected
  (temperature 0).
- One run per configuration: temperature 0 makes a run repeatable, so there
  were no seeds to vary.
