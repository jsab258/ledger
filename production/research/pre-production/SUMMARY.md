# Pre-production review: what is still undecided, and what to prove first (3 October 2026)

**The question.** LEDGER went from research straight into production, so fundamental decisions keep surfacing mid-production: casting, clothing, licences, how the world's assets are made. Jafar wants the rest found now.

**What was done.** This cloud session read CLAUDE.md, DECISIONS.md (RULINGS.md is not yet at the root), ROADMAP.md, canon.md, the asset plan and the research and audit folders. Five read-only helpers each took one question for about thirty minutes (notes/). The deciding facts were then checked here at the source (SOURCES.md). No code or rule was changed.

## The answers

1. **Pre-production audit** (1-AUDIT.md).
   - LEDGER **has** a narrative bible, an interface style guide, roles and an approval process.
   - It has only **parts** of the gate, the design document, the art bible, the asset list and methods, the technical design, the performance budget, the pipeline, licensing, money, QA and release.
   - It has **no** schedule and **no** risk register.
   - It settled *what it wants* early and well. It did not settle *what each thing costs to make and whether the method works*. That is the half that prevents mid-production surprises, and each of the four surprises maps to it.
2. **Feasibility** (2-FEASIBILITY.md): 37 areas against the six constraints.
   - **23 are risky:** the two known ones, clothes and live voices, and 21 more. **4 are unknown** and **10 are feasible**.
   - The risk sits in people, look and talk, not in the systems: save, the interface, props, signage and the build machine are sound.
3. **Proofs** (3-PROOFS.md): 21 cheap proofs, each one to five days, each ending in a number or a reviewer's verdict.
4. **Budgets** (4-BUDGETS.md), derived from 60 fps at 3440×1440 on the RX 6700 with the voice running:
   - a 14 ms GPU envelope split by family;
   - a 6.0 GB memory envelope for the game beside the voice's 2.8 GB;
   - texture density from the camera (512 px/m for the street, 1,024 for what is read at arm's length);
   - per-asset limits for buildings, rooms, props, food, signs, cars, people, clothes, hair and plants.

   All are provisional until P1 profiles the hook camera.
5. **Definition of done** (5-DONE.md): twelve lines every asset meets, plus a line per kind: in the packaged game, with distance versions, collision, its source and licence recorded with its NoAI status, judged against its bar, its approval recorded.
6. **Risk register** (6-RISKS.md): the top ten risks to the thirty-minute friends' build, scored, each with a trigger you can measure and its cheapest mitigation, and a fifteen-minute review every Monday. The top three today:
   - **R1, talk feels empty or unchecked: 25 of 25;**
   - **R2, replies too slow: 20;**
   - **R3, the street not at the bar in time: 20.**

## Found or confirmed by this review, cheap to fix

1. **A spending budget switches the claim check off.** The checker is attached only when the talk client is the plain Anthropic client. A budget wraps it in another class, so every measured run on the key ran unchecked, including the only in-game measurement of real talk (30 September). His own play is checked. Steam's approved disclosure says "every line is checked before you hear it". The rulings sweep found this on 1 October; it is still in the code today. (P3)
2. **In a fresh Windows account the characters cannot talk.** The game reads the key from the current user's own folder. The friends' build is ruled to run in a fresh account, which has no key there. The portable voice has also never been started outside his account. (P5)
3. **The repository is public** (32.5 GB). It holds the KCD2 and GTA V reference frames that THIRD-PARTY.md calls "not redistributed". The approved Steam disclosure also says talk goes "through LEDGER's own server", which is not hosted. (P14)
4. **The game runs with Nanite and virtual shadows off; the asset plan assumes both on.** Every triangle budget depends on which is true. (P1)
5. **Today's sparse street already uses most of the frame.** Standing, at half resolution, with the voice speaking: 75 fps median, the slowest 1% at 16.7 ms. The workflow's comment that the voice is not running is stale. About 2.6 ms of GPU is left for everything the proof view adds, unless scalability High or the voice leaving the card pays for more. Walking shows 23 of 847 frames over 33 ms. ROADMAP's "last measurement 24 September" is out of date.
6. **No thirty-minute session has ever been played,** by a person or by the tester. The player character, on screen for all thirty minutes, is still a Mixamo stand-in in a grey tracksuit. (P4, P8)

## The proofs to run first

About two days and under a dollar settle findings 1 to 3:
1. **P3:** fix the check under a budget, then measure checked talk on the real path.
2. **P5:** start the friends' build in a fresh account.
3. **P14:** read the Unreal, MetaHuman, Mixamo, Steam and Fab terms from his PC and correct the records.

Then:
- **P1**, the hook camera's profile, which settles every budget;
- **P4**, one thirty-minute session played and counted, whose empty minutes become the content list;
- **P2**, already list item 3.

The rest follow their families.

Each proof joins the builder's list only by his order at a stated position. This review changes no list.

## Decisions this raises for Jafar (scope, money, licences)

1. **Money: friends' talk.** Steady talk costs $1.07 to $3.22 an hour. His key's rule covers his play and measurement runs. **Recommended:** friends' evenings get their own cap, set from P3's measured cost per thirty minutes.
2. **Licence and money: the public repository.** **Recommended:** make it private, after checking what GitHub's private-repository minutes would cost for the Linux core tests; that cost is not checked here. The alternative is to keep it public and take the reference screenshots out.
3. **Scope: what the thirty minutes contain.** **Recommended:** after P4, one paragraph naming the first-hour beats, the characters, and the office (out unless P15 passes), combat (out, kept for stage 3) and music (out). This is a recommendation, not a ruling.
4. **Security: the key in the friends' account.** **Recommended:** a copy placed in that account for the evening and removed after, which needs no code. The alternative is a machine-wide path, which is a code change.

## Marks

- **[M]** measured on his PC and recorded in the repository;
- **[R]** read at the source on 3 October;
- **[W]** read on Wikipedia;
- **[SS]** search summary only, a lead and not evidence;
- **[I]** this review's inference;
- **UNREACHED**.

## What could not be verified

- **Studio practice** beyond Epic's documentation and Wikipedia. Every games-industry site, talk and book was unreached; their points are leads only.
- **Every hardware benchmark** for RX 6700-class cards (the sites were unreached).
- **The Unreal EULA, MetaHuman and Mixamo terms, Steam's survey and the Fab EULA:** read only through search summaries. P14 reads them from his PC.
- **Every budget allocation and day estimate.** They are this review's, pending P1 and P21.
- **Anything on his PC:** how the work of 3 October looks, what the cast wear today, F:'s free space (two records disagree), whether "Help improve Claude" is off, the key's monthly cap, the portable voice folder's size.
- **His pages' stored answers:** not read.

## Files

- 1-AUDIT.md
- 2-FEASIBILITY.md
- 3-PROOFS.md
- 4-BUDGETS.md
- 5-DONE.md
- 6-RISKS.md
- SOURCES.md
- notes/: the five helpers' evidence, as written, with corrections in SOURCES.md
