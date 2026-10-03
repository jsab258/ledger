# Notes on the drafts (3 October 2026)

**What this folder is.** Drafts for the builder to apply after Jafar has answered QUESTIONS.md. Nothing live is replaced.

| File | Becomes | Words |
|---|---|---|
| RULINGS.md | RULINGS.md at the root | 2,466 |
| CLAUDE.draft.md | CLAUDE.md | 989 |
| QUESTIONS.md | his one page | – |
| CHECK.md | tools/doc-caps.py and its wiring | – |

CLAUDE.md is a draft name here on purpose: a file named CLAUDE.md in this folder would be loaded by any session working in it.

**Applying them.**
1. Answer the questions; edit each line marked [Qn] in RULINGS.md to match.
2. Copy RULINGS.md and CLAUDE.draft.md to the root.
3. Trim NOW.md, TOWN.md and CLOTHES.md under their caps.
4. Land the check in the same commit (CHECK.md).

DECISIONS.md stays as the history, appended to and not read at the start of work.

## What was read

- CLAUDE.md, NOW.md, DECISIONS.md: all 242 entries, 24 September to 3 October.
- production/archive/DECISIONS-to-2026-09-24.md: 138 lines, its D-records summarised from the rulings sweep's reading of each.
- canon.md and the rulings sweep (production/audits/rulings-sweep/, its rulings.json).
- Checked in the code and specs where a ruling's state mattered:
  - production/specs/in-game.json: Ron's approved face is P2 (26 September), Darren's voice p241;
  - the casting sheets for Danny and June;
  - the commit of 2 October (4d55809) that closed the sweep's last open items, which is why it is not a question.

## How "binds today" was decided

- **His rulings only.** Lines marked "Jafar" in DECISIONS.md, his D-records and dated rulings in the archive, and his rulings carried in CLAUDE.md.
- **Session decisions are left out**, except a few that carry out a ruling of his and that other sessions must follow: the shop trades, the shop rooms, free play's crime at Rita's window. Left out are those marked "Claude", "Claude (town)", "builder" or "my decision", most of them how something was built. They stay in DECISIONS.md, the archive, the code and game-design/. One line keeps the town's design decisions standing: "the town's decisions within canon stand unless he overturns them".
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

## Not settled from the dates

The eight questions in QUESTIONS.md. Two more were dropped:
- **The rulings sweep's items** against the one list: already built on 2 October.
- **Ron's voice "until a clean one is found"** (in-game.json) against "voices not reopened" (3 October): the later ruling decides it.
