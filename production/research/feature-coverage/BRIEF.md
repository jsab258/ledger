# BRIEF: whether the PLAN has every feature a modern game is expected to have

STATUS: BRIEF. Written 2026-09-23, before any research began, per Jafar's
instruction of 2026-09-19 that a topic's brief is a file in the topic's folder
and the delivery is audited against the commission rather than against its own
account of it.

This topic is the successor to
[baseline-features](../baseline-features/SUMMARY.md), which audited the build.
This one audits the plan.

## The commission, in his words

> You are a research session for LEDGER. You produce research and nothing else:
> work on a branch named research/feature-coverage, write only under
> production/research/feature-coverage/, arm no triggers, dispatch nothing, open
> no pull requests.
>
> Write BRIEF.md first, with this brief in it.

### The problem

> This project has catalogued around two hundred systems from studying games,
> and still missed basics every game has had since 2009, found by accident while
> playing: people turning their head to look at you, and sound that comes from
> where its source is. Two earlier audits missed them because both worked from
> lists of features that someone remembered, and the second was even given its
> categories in advance, so it could only find what fitted them. The question
> here is not whether the game has a feature yet. It is whether the PLAN has it:
> whether every feature a player of a modern game would expect is written down
> somewhere in this project's roadmap, inventory or research, so it cannot be
> forgotten.

### The method

> The method is four lenses, each complete by its own construction, not by
> anyone's memory.
>
> 1. Who builds it. Take the full credits of two or three large modern games,
>    GTA V, Red Dead Redemption 2 and Kingdom Come Deliverance 2 are good, and
>    list every department. For each department, what does that team deliver in
>    a typical game of this kind, as player-facing features.
> 2. What runs every frame. Take the standard list of a game engine's runtime
>    subsystems, from Unreal's own module list and the standard texts on engine
>    architecture: rendering, animation, physics, audio, AI and navigation,
>    input, camera, interface, save, streaming, localisation, platform services,
>    effects, and whatever else the list holds. For each, the player-facing
>    features it produces.
> 3. Moment by moment. Walk the first thirty minutes of a modern open-world game
>    from launching it to quitting it, second by second: every screen, every
>    thing seen, heard and done, and every system behind it.
> 4. What the industry already checks. The published platform certification
>    requirements and accessibility guidelines, such as the Xbox Accessibility
>    Guidelines and the Game Accessibility Guidelines, which are checklists of
>    expected basics.

### The merge

> Merge the four into one checklist and remove duplicates. For every item,
> record which lenses found it, because an item found by only one lens shows
> where the others are blind.

### The comparison

> Then compare the whole checklist against the plan, not the build: ROADMAP.md,
> the systems inventory archived in
> legacy/studio-v2/production/systems-inventory.json, the research under
> production/research/, including the baseline-features delivery, and canon.md.
> Mark each item as in the plan, partly, or absent from the plan. For the absent
> ones, say which stage of ROADMAP.md it belongs to, or that D24 rules it out,
> since not everything a modern game has belongs in this one.

### The deliverables

> Deliver SUMMARY.md for me, one page in plain words: how many expected features
> the plan was missing, the ones a player would notice soonest, and which lens
> found the things the others missed. And DELIVERY.md: the full merged checklist
> with its lenses and its place in the plan, in a form that becomes the
> per-stage checklist in ROADMAP.md.

## The standing boundaries of this lane, restated

From the lane's founding brief, never rescinded: work on a branch named
`research/<topic>` from the commit this session starts at, never commit to main,
write only under `production/research/<topic>/`, touch nothing else, arm no
triggers, install nothing, dispatch no workflows, send no messages, open no pull
requests, propose nothing into the queue. The studio reads the delivery.

## What this delivery should be judged against

1. Were the four lenses built by construction rather than by recall? A lens that
   was written from memory and then decorated with a source is the exact failure
   this topic exists to correct, and it has to be visible in the delivery which
   lens rows are cited and which are not.
2. Does every item carry the lenses that found it, including the items only one
   lens found, which are the point of the exercise?
3. Is every plan verdict backed by a file and a line in this repository rather
   than by a recollection of what the plan says?
4. Are the sources that could not be reached named, with what that costs the
   lens they belonged to, rather than quietly replaced by general knowledge?

## Added 2026-09-23, after the delivery: the second commission

Jafar then put an independent list of 923 player expectations on main, written
by a different model without sight of mine, at
[astra-list.md](./astra-list.md), and commissioned the comparison that
replaced the original DELIVERY.md:

> Compare it against your checklist and against the plan. For every item in it,
> mark whether your list has it, whether the plan has it, or neither. The items
> in neither are the blind spots this whole exercise exists to find: list them
> first, grouped by area, and say which of your four lenses should have caught
> each one and why it did not.
>
> Then merge both lists into one master checklist at the level of specific
> features, never headings, since headings are what swallowed head-turning and
> positional sound. Each item gets its place in ROADMAP.md's stages, or a note
> that it does not belong in this game and why.
