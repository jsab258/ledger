# The parts tree

LEDGER as one multilevel parts list, like a bill of materials: level 0 the game, level 1 ten groups, then sub-assemblies, then buildable parts. His decision of 19 Nov 2026, 20:52 (advisor 257). The tree never creates work by itself: Monday's order and the loops pick what is built; the tree makes sure nothing is invisible.

## Files

- PARTS-TREE.json: the source of truth. Edit it, then run the three tools below.
- PARTS-TREE.md: the indented tree with status, for a phone (generated).
- ONESHOT-CHECKLIST.md: every gameplay part the one-shot builds into the prototype, with its test and design (generated).
- PLAN-VIEW.md: the order for the prototype and the Unreal phases, the critical path, what blocks the most (generated).
- RESEARCH-NEEDED.md: felt parts whose standard is still to be measured (generated).
- GAPS-2026-11-20.md: every gap found, by method, and the part it became.
- QUESTIONS-FOR-JAFAR-2026-11-20.md: three scope questions, recommendations marked.
- DECISIONS-PENDING.md: one line per choice, for the builder to append to DECISIONS.md.
- PARTS-LOG.md: done, next, broken, so the lane can continue.
- SUMMARY.md: one paragraph for the advisor.
- work/: the helpers' raw mappings the tree was built from (checklist, players, departments, studies and risks, mechanics, prototype and Unreal status, measured hours).
- SKELETON.txt: the first list of ids the helpers mapped against (kept for traceability; the JSON supersedes it).

Tools (tools/lane/parts-tree/): rollup.py recomputes headings' statuses from their leaves after any status edit; check.py validates and prints totals (exit 1 on any fault; --json for the progress page); render_md.py writes PARTS-TREE.md; render_views.py writes the checklist, plan view and research list. first-build/ holds the scripts that first assembled the JSON from the helpers' files; later edits go into the JSON directly.

## Fields of each part (PARTS-TREE.json, "parts")

- id: like 1.3.2; the first number is the group. level: 0 to 4. parent; children; leaf (true for a buildable part).
- name; what: one plain line.
- felt: true if the player feels it (all of group 1 and the felt parts of 2, 5, 6, 7 and others).
- standard: a reference game and what to measure, a measured number, or a rule from canon, his rulings or DESIGN; "none yet" when there is none; for a felt part research_items must then name the research; parts nobody feels (such as 10.9 support or 10.10 company admin) may stand on "none" without an item.
- standard_source: where the standard comes from.
- research_items: ids in the top-level "research_items" (RN-01 and on): what to measure, in which games, how.
- designed_in: DESIGN section, the addendum's section, a ruling, a spec, or "not designed".
- track: prototype, unreal or both. status: per track, {status, evidence}; status is one of missing, designed, built shallow, built, passes, unknown. Unknown means the repository gave no evidence; nothing is guessed. Evidence names the file. "designed" for a part with no sweep row means its design exists and nobody checked the build.
- needs and blocks: part ids, mirrored (a needs b exactly when b blocks a), no loops. A need means "must exist first", not "is related".
- hours: {prototype, unreal, basis}: first estimates; basis says measured, from a comparable (work/measured-hours.md), or a marked guess.
- risk: {level: low, medium or high, why}.
- test: how we know it is done (a machine check S, the clumsy bot B, a hands-on check H, feel numbers, his eye), and the experience rules that apply.
- owner: builder, town, clothing or lane.
- checklist_items: the old 957-item checklist's ids hung on this part as acceptance checks (production/research/feature-coverage/MASTER-CHECKLIST.md).
- review_themes: review and player themes it answers (rounds' reviews, PLAYERS.md theme ids).
- notes: anything the session changed by hand, with its reason.

Top level: "ruled_out_checks" (the 116 checklist items ruled out, each with the decision) and "research_items".

## The rule it enforces

Every part a player feels has a standard, a reference game measured or a rule, and a part without one is a research item (proposed RULINGS line, advisor 257). check.py fails on a felt part with neither, on a missing field, a duplicate id, a need or block that names no part or is not mirrored, a loop, and on any experience rule in DESIGN.md or its addendum that lands in no part.

## Group names

Kept as his brief gave them; the gap checks added parts inside the groups, never a new group.
