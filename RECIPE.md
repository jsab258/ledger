# RECIPE: the notebook

A notebook, not a project (Jafar, 13 October 2026). Its purpose: no lesson we learn is lost, so that one day the process can make a whole AAA game.

**The rule.** Every unit that finishes or is set aside adds a few lines here in the same commit: what was made; the method in setting-free words; the tools; the target and the check; the cost in hours; what failed and why; the evidence file. Anything specific to 1990 or Meridian stays in data, never in the method. No separate recipe work, no recipe tests. (RULINGS.md, 13 Oct; CLAUDE.md, Records.)

**Unit 14** of cloud week 42 writes up what came before 13 October, if time allows, as a separate section below, and writes REUSE.md (what is method and what is 1990 or Meridian content in each tool).

**Entry form** (newest first, under "Notebook"):

    ### <date> <unit or task>: <what it was>
    - Made: ...
    - Method (setting-free): ...
    - Tools: ...
    - Target and check: ...
    - Cost (hours): ...
    - Failed and why: ...
    - Evidence: <file>

## Notebook

### 13 Oct 2026, unit 8: the exact target for a family of repeated pieces (a street's house windows), written, failed its fresh review, fixed
- Made: a target for twenty windows in ten houses in four kinds (parts in millimetres), the glass and the shaded box as numbers, nets and drapes, thirteen small rooms behind the glass by the game's own projection rule, a cloud gate that measures a render against photographs by the piece's state, 47 checks, and a self-check with 27 seeded faults that must each be caught. A fresh reviewer found three faults and twelve narrow points; the fixes are applied and not yet re-reviewed.
- Method (setting-free): measure real photographs the way the check will measure a render (the same region, the same statistic), before a band is written from them; box the object tight so its surroundings (stone, brick) do not leak into the number. Name the object's states (bare, net, draped) before the bands, because one band cannot suit them all. Check a design against all of the owner's standing rulings, not only the latest, before a photograph tally is allowed to decide anything; where they disagree the ruling stands and the question goes to him on one page. Place the cameras where the camera table says before a budget is derived, and use the exact pixel angle. Check every placed model's texture region by region at full size against its list of marks before a room is rendered, and look again after a review finds one. Apply a fix list as written; where a line is shown wrong (a window called a bedroom that is a landing), apply its evident intent and flag it with the evidence.
- Tools: python with numpy and PIL; the game's own projection function imported, never rewritten; the photograph library's and the asset library's public interfaces; a self-check with negative controls.
- Target and check: the checks (kit geometry, glass, white-board bands by state, night, rooms, sites, content); self-check after the fixes 402 pass offline and 424 with the live catalogue and previews, 27 of 27 controls caught. Nothing built.
- Cost (hours): writer about 1.0 (00:36 to 01:37 by file times); fresh reviewer about 0.4; fixer about 0.8.
- Failed and why: (1) the frame colours went against the owner's standing ruling: only the latest rulings were read for a conflict and a photograph tally was let to settle it. (2) The photograph numbers measured stone and brick, not the frame: the boxes were drawn wide by eye, not the way the gate measures, so an honest render would have failed its own bands; three of the four "bare" windows carried a blind or a curtain. (3) A maker's name, 3 pixels high, on a model's front bezel: the look at the maps was not region by region against a marks list. Narrow: cameras at the card's centre, not the window; a piece of the wrong period in a room; a lit order that lit landings before lounges.
- Evidence: production/cloud-week/targets/house-windows/TARGET-REVIEW.md, FIXES-APPLIED.md, TARGET.md, target.json

### 13 Oct 2026, unit 6.1b: checklists for a set of studies from the owner's own study plan
- Made: one page per study for twelve studies (game, where to look first, what to count, when to stop, what the output page must hold), in one file beside the kit that covers the other four.
- Method (setting-free): turn a study plan into an operating checklist without touching the thing studied. Take each study's questions, "where it lives" and output lines straight from the plan; add the kit's maps; mark every line by where it came from (plan, kit, inference) so nothing inferred passes as read. Give each study a stop rule and one thing it must not copy. Tie each output to the existing ruling or finished unit it must be set against, so the study adds to a decision and does not reopen it.
- Tools: none beyond a check script for forbidden dashes and italics.
- Target and check: every study in the plan has a page; the check script; no review (ordered).
- Cost (hours): about 0.6 of my own time.
- Failed and why: nothing failed. The first draft cited the wrong document for the frame-time exit; found by looking the number up before finishing. Lesson: look a number up in its home file before writing its source.
- Evidence: production/research/aaa-reference/CHECKLISTS.md

### 13 Oct 2026, unit 7b follow-up: a finished research file set against a new design
- Made: a section in COMBAT.md comparing its findings with Jafar's new combat rulings and design (39 rows, each adopt, adapt, ignore or not covered), the old comparison rows marked superseded and kept, the draft target list for the first combat test extended by 15 entries.
- Method (setting-free): when a design replaces the document a finished study was written against, add a comparison section instead of rewriting the study: one row per design point, what the references do (cited to the study's own sections), a verdict, and where the design is silent say "not covered". Mark superseded old rows, never delete them. Extend a target list with new ids and never renumber, so every cross reference holds. List every point the design leaves unclear for its author. Read the design from its source, not from a summary.
- Tools: a check script (no forbidden dashes or italics, table cell counts, every cited id defined, frames equal seconds times the frame rate, quotes under the length cap).
- Target and check: the script above, run by the writer; no fresh review (ordered).
- Cost (hours): about 0.4 of one helper's work, plus about 0.5 to find and read the design doc and brief the helper.
- Failed and why: the first brief gave the helper only a summary of the design, because the design doc was thought to be unreadable; it was a Claude doc, found through the artifact list, and the helper was re-briefed mid-task. Lesson: when a source "cannot be found", list every place the owner keeps documents (Drive, the artifact list, the repository) before working from a summary.
- Evidence: production/research/aaa-reference/COMBAT.md
