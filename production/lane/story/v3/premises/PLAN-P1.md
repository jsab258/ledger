# Phase 1 ranking: plan, written and pushed before any reader runs

21 November 2026. Twenty premises (SET-X.md X1 to X6 and SET-Y.md Y1 to Y6 by two fresh claude-fable-5-2 helpers from PREMISE-BRIEF.md alone; SET-Z.md Z1 to Z8 by the story session, Z1 being The Passenger at its best version).

## What the readers get

One pack of 32 one-paragraph pitches, all in one format (PITCH-FORMAT below), all written by one neutral hand (a fresh claude-opus helper, the packer) so that no voice marks a group:

- our twenty, moved to one invented setting;
- eight anchors: the eight shipped games of the reader check (RDR2, GTA V, GTA IV, KCD2, Sleeping Dogs, Hitman, Watch Dogs: Legion, L.A. Noire), cut down from their disguised summaries in reader-check/summaries/;
- four decoys: four other shipped story games, disguised from the packer's knowledge (Yakuza 0, Disco Elysium, Watch Dogs of 2014, Saints Row of 2022), so that "a page I do not recognise" does not mean "the one under test".

Each of three fresh claude-opus readers gets the 32 in a different shuffled order under neutral numbers, with the checked brief (reader-check/BRIEF-FIXED.md) changed only where it must be: pitches not summaries, 32 not eight, and it no longer says how many are shipped.

## The blindness fix (the last check's fault: readers could tell which page was ours)

Last time the helpers could see the project's standing instructions, and our page kept Britain, 1990 and a cab office, so they matched it to the project. This time:

1. Our twenty are moved off every word those instructions hold: an invented northern country, 1991, a harbour labour register for the Scheme, a radio-taxi office, roles for names, new nicknames in place of the real British ones. One mapping for all twenty, so the move adds no noise between them.
2. Readers run with their working folder outside the repository and are given one file by path in a temporary folder.
3. Decoys, and a brief that does not say which or how many pitches are shipped.
4. It is measured, not assumed. After ranking, each reader says for every pitch: shipped game or unshipped plan, how sure, and whether it comes from any project he knows of. Blindness passes if no reader ties any pitch to this project. It is reported also how well readers separate our twenty from the twelve shipped.

A limit that cannot be removed: twenty pitches sharing one set-up (a stranger inherits a dead relative's taxi office, a doorman, a bookkeeper) will be seen as a family. That does not bias the ranking inside the family, which is what Phase 1 decides; it may lean the family's marks against the shipped games, so those are reported with that warning.

## PITCH-FORMAT

One paragraph, 200 to 240 words, present tense, British spelling, no names of people, places or brands (roles and plain descriptions), no lists, no bold or italics, no em-dashes, no judging words. In this order: the world and what is ending in it; the lead and what he wants or owes; the two to four people who matter; what the player's hands do; the turn; what is lost for good; what decides the ending and what the endings are. Nothing improved and nothing weakened: every beat the source states, none it does not.

## Scoring, fixed now

- Each reader gives each pitch a mark out of 10 (the mark he expects its players to give its story) and ranks all 32 with no ties.
- Pooled rank of a pitch: the mean of its three ranks; ties broken by the mean mark, then by the best single rank.
- The top three: the three of our twenty with the best pooled rank. No rule about variety; if two of the three are near twins, that is said and both still go forward.
- Reader fitness on short pitches, on the eight anchors only (reader-check/agree.py, the players' tiers of reader-check/PLAN.md): pooled Spearman at least 0.60, at least 18 of 23 ordered pairs, and the RDR2 pitch first or second among the eight anchors for two of three readers. If this fails, the ranking of our twenty is reported as provisional and the pack is mended once (longer pitches) and rerun with three new readers.
- Agreement between readers on our twenty: Kendall's W over the three rankings, reported. Under 0.4 means the three do not agree enough to separate neighbours; then only clear gaps (a mean rank apart by five places or more) count.
- Canon: a premise is not marked down by the readers for straining canon (they do not know canon). The canon notes of the top three are carried forward as multiple-choice questions for him.
