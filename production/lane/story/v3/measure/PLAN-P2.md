# Phase 2 measure: plan, written and pushed before any summariser or reader runs

23 November 2026. Three bibles: v3/bibles/BIBLE-Z4.md (The Knowledge), BIBLE-X4.md (The Burial Club), BIBLE-Y5.md (The Arrested Ship), each by one fresh claude-fable-5-2 writer from v3/bibles/BIBLE-BRIEF.md.

## The blindness fix, this time

Until now every helper carried the project's standing instructions and so could tell which page was ours. Today's fix: summarisers and readers are started with the command-line Claude from an empty folder outside the repository, with no tools, the whole task given as text. A test run answered that it had no project instructions (model claude-opus-5-5). It is measured, not assumed: each reader is asked at the end whether any page is an unshipped plan and whether he can tie any page to a project he knows of. Blindness passes if no reader ties our page to this project.

## The pages

One neutral summariser per bible (blind claude-opus-5-5), given measure/FORMAT.md, reader-check/summaries/DISGUISE.md, the setting mapping of v3/premises/pack/PACKER-BRIEF.md (an invented northern republic, 1991, a harbour labour register, a radio-taxi office, roles for names, new nicknames) and the bible without its sections 0, 11 and 12 (they say what changed, what is invented and what canon is strained). At most five short quoted lines, since the shipped pages quote few. Pages: v3/measure/pages/S-Z4.md, S-X4.md, S-Y5.md. A page outside 1,900 to 2,300 words is sent back once.

## The readers

Each bible is read by three fresh blind readers (claude-opus-5-5), nine readers in all. Each reader's pack: measure/MEASURE.md as context, then ten pages under letters in a shuffled order (seed 20261123): the eight shipped pages of the reader check, the GTA VI page, and one of ours (letter H). One of ours per pack, so that no reader sees a family of three. Brief: reader-check/BRIEF-FIXED.md changed only from eight pages to ten, with one question added after section D (unshipped plan? any project you know?).

## Scoring, fixed now

- Per bible: its three places among ten, its mean mark, RDR2's mean mark in the same packs, and the three verdicts.
- Reader fitness on the eight anchors, per reader and pooled over all nine (reader-check/agree.py): Spearman at least 0.60, at least 18 of 23 pairs, RDR2 first or second for at least six of nine. If it fails, the result is reported as provisional.
- The floor ruler and the punished patterns: one further fresh blind reader per bible fills in measure/MEASURE.md for our page and the RDR2 page (praise items, fault items, watch items), counted by measure/tools/score_marks.py.
- The pick: the bible with the best mean place among ten; ties broken by the mean mark, then by the ruler's net score, then by fewer failed fault items. If the first two are within half a place and 0.2 of a mark, that is said plainly and the pick stands by the tie-break.
- Revision: at most two rounds on the picked bible, each from the readers' own three heaviest complaints, each re-read by three fresh blind readers in the same way. A round that does not raise the mean mark is reverted.
- The bar: RDR2's mean mark in the same packs. Whatever the result, it is reported beside it.
