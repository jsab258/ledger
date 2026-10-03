# Notes on the drafts (3 October 2026)

**What this folder is.** Drafts for the builder to apply after Jafar has answered QUESTIONS.md. Nothing live is replaced.

| File | Becomes | Words |
|---|---|---|
| RULINGS.md | RULINGS.md at the root | 2,490 |
| CLAUDE.draft.md | CLAUDE.md | 993 |
| QUESTIONS.md | his one page | 378 |
| CHECK.md | tools/doc-caps.py and its wiring | – |

CLAUDE.md is a draft name here on purpose: a file named CLAUDE.md in this folder would be loaded by any session working in it.

**Applying them.**
1. Answer the questions; edit each line marked [Qn] in RULINGS.md to match.
2. Copy RULINGS.md and CLAUDE.draft.md to the root.
3. Trim NOW.md, TOWN.md and CLOTHES.md under their caps.
4. Land the check in the same commit (CHECK.md).

DECISIONS.md stays as the history, appended to and not read at the start of work.

## What was read

- CLAUDE.md, NOW.md, DECISIONS.md: all 250 entries, 24 September to 3 October, up to main at 5db99d5 (his NoAI, clothes and asset-plan rulings of 3 October, which landed while the drafts were being checked).
- production/archive/DECISIONS-to-2026-09-24.md: 138 lines, its D-records summarised from the rulings sweep's reading of each.
- canon.md and the rulings sweep (production/audits/rulings-sweep/, its rulings.json).
- Checked in the code and specs where a ruling's state mattered:
  - production/specs/in-game.json: Ron's approved face is P2 (26 September), Darren's voice p241;
  - the casting sheets for Danny and June;
  - the commit of 2 October (4d55809) that closed the sweep's last open items, which is why it is not a question.

## How "binds today" was decided

- **His rulings only.** Lines marked "Jafar" in DECISIONS.md, his D-records and dated rulings in the archive, and his rulings carried in CLAUDE.md.
- **Session decisions are left out**, except a few that carry out a ruling of his and that other sessions must follow: the shop trades and the shop rooms. Left out are those marked "Claude", "Claude (town)", "builder" or "my decision", most of them how something was built. They stay in DECISIONS.md, the archive, the code and game-design/. One line keeps the town's design decisions standing: "the town's decisions within canon stand unless he overturns them".
- **The later of two rulings stands.** For example:
  - one list on 3 October, replacing the lists of 30 September and 1 October;
  - clothes on 3 October, replacing 25 and 30 September, and 1 and 2 October's Marvelous Designer route;
  - D48 re-ruled on 1 October, replacing "Sheila stays on her model";
  - the hill "built properly, never hidden" on 3 October, replacing "convincing or hidden" on 1 October;
  - retention on 2 October, replacing the 25 September deletion list;
  - the accent checker a screen on 30 September, replacing the voice gate of 29 September;
  - his picks of 30 September replacing the town's "carried until he rules" on the arrangement and threats.
- **Left out as done or expired:**
  - the cleanups of 26 and 28 September;
  - the merges of the cloud research;
  - the measuring run;
  - one-night rules (overnight, "For you:", the stop hook);
  - MH_Test;
  - the 1 October list ahead of stage 1, now built.
- **Process rules** went into the CLAUDE.md draft, not into RULINGS.md: the gate, his page, records, research, the two tries, lanes, git and disk procedure.
- **Canon facts** are not repeated: names, the street's sides, the content rule, brands and Mickey's as a cab office.
- **One clause comes from his brief of 3 October, not from DECISIONS.md:** human-made inputs (buying, commissioning, hiring) only by his explicit ruling, today none. It is marked so in RULINGS.md; the builder writes it into DECISIONS.md when applying the drafts.
- **The caps are his** (3 October): 1,000, 2,500, 200 and 300 words.

## Not settled from the dates

The five questions in QUESTIONS.md. Five more were dropped; two of them he settled himself on 3 October, while the drafts were being checked:
- **NoAI against Epic's own content** (the Megascans, the Game Animation Sample, Epic's MetaHuman garments): he ruled the rule as written on 3 October; they are out.
- **Buying clothes** (a suit under $40 on 2 October against no human-made inputs on 3 October): he ruled no purchases and no commissions for clothes on 3 October.
- **The rulings sweep's items** against the one list: already built on 2 October.
- **The mouths:** D201's reason settles it, so every prepared line uses Epic's audio-driven mouths.
- **A casting sheet against a reply that passes:** not a conflict.

Clothing's stop on new garment families (2 October) is overtaken by 3 October, which has the clothing session make plain garments from unrestricted sources, and is left out of RULINGS.md.

Ron's voice "until a clean one is found" (in-game.json) against "voices not reopened" (3 October) is settled by the later ruling; question 5 asks only about the three voices not yet in the game.

## The independent check

A reviewer that had not seen the drafting compared them with DECISIONS.md, the archive, canon and the sweep, and raised 25 points. The ones checked and fixed:
- **Wrong or missing dates:** the key, D28 and D40.
- **The allowance:** credited wrongly; replaced by his 24 September ruling (every live call through our server, the key never shipped, a spending stop).
- **The constable line:** against canon, so removed.
- **Cars:** now fictional, as canon says.
- **Sheila's calm reference:** lapsed when her voice was replaced.
- **The threat conflict:** fault N3, now question 3.
- **Lines restored:**
  - image-to-3D waits;
  - the eleven sheets' faces are cast in MetaHuman;
  - the talk runs as the C# helper;
  - no training on the paid model's answers;
  - the friends' build;
  - the items ruled for after the route works.
- **The CLAUDE.md draft:** the gate's full references, the disk safeguards, the research triggers and the graphics card's priority, all put back.

A question on CLO's free licence was dropped as moot; the smaller points (the overview, the page and the working rules) were applied.