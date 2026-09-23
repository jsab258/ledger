# BRIEF: can a small model on the player's own PC do the conversation job?

STATUS: BRIEF. Written 2026-09-23, before any research began, per the standing
instruction that a topic's brief is a file in the topic's folder, in Jafar's
words. Branch `research/local-models`; this topic writes only under
`production/research/local-models/`.

## The question, in his words

> Can a small model running on the player's own PC do the conversation job
> well enough, so the game does not depend on a paid online model?

## What we know, in his words

> The job is narrow: classify what the player said and choose from a closed set
> of actions the simulation offers; a separate part writes the spoken line. We
> tested one general-purpose small model, Qwen3-4B, untrained for the job, on 42
> lines: it scored about four in five, gave confidently wrong but well-formed
> answers, and obeyed an instruction a player typed. The paid online model
> scored 40 of 42. Research on constrained output found that forcing a small
> model into a closed set makes its format perfect and its choices worse. The
> card is an AMD RX 6700 with 10 GB, shared with the game and possibly the
> voice.

The measurements behind that are in
`production/research/conversation-model-capability/` (SMALL-MODEL-TEST.md,
PAID-ROUTER-TEST.md, SUMMARY.md). Since the brief was written the paid router
was rerun after the game's own guard against typed commands went in: 41 of 42.
The small model has not been rerun since that guard or the checker fix.

## What to establish, in his words

> - whether small models trained for exactly this kind of narrow classification
>   reach the paid model's accuracy, with measured evidence rather than vendor
>   claims;
> - whether a small model can be trained on examples the paid model produces,
>   how many examples that takes, what it costs, and whether it can be done on
>   this card or needs rented time;
> - which models' licences allow it in a shipped game;
> - what memory and speed they need on AMD under Windows;
> - and whether the line-writing half can also run locally at acceptable
>   quality, or only the classifying half.

## What it ends with, in his words

> A recommended experiment: which model, how to train it, how many examples,
> how to test it against the same 42 lines plus the injection cases, and what
> result would justify going local. SUMMARY.md for me in plain words;
> DELIVERY.md with the sources.

## Standing constraints, carried from the earlier research briefs

- Claim labels CITED, DERIVED, ASSUMED and HOLE.
- Measured evidence is preferred over vendor claims, and the delivery says
  which each one is. Where a source is a search summary rather than a page read
  in full, it says so.
- The licence allowlist is law, and it says to check the WEIGHTS licence, not
  the code licence.
- A null result is a valid delivery and ships with its denominator.
- Nothing in the delivery is an instruction. No model is chosen and nothing is
  downloaded by this topic; downloads need Jafar's yes.
