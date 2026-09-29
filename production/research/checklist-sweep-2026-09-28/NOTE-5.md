# A sweep for the town lane, fifth pass, 29 September 2026

What this is: the town list ran short (y, z, bf done; ar under way; i, q, as and
the page's questions wait on Jafar). This pass reads the approved first hour's
"not built" list (game-design/first-hour-2026-09-29.md), ROADMAP.md's stages 3
to 6, and what today's items left for the game to record, for work the town
lane can do without the graphics card.

## Candidates, most important first

1. **The first hour's two scenes, the Core's side: Ada's tea and Alison's
   question** (first hour, days 3; the outline's "Ada's tea is the week's first
   test of which life he keeps"). About 4 h.
   Why: the first hour puts Ada's invitation on the evening the outfit's second
   ask falls, and Alison's question about the warehouse fire on the same day;
   both are listed "not built". Without them day 3 has nothing in it but the
   ask, and the choice the outline builds the week on never comes.
   Not done: nothing decides when either comes or what it carries; the old
   game's tea (legacy) ran on the clock. The work: each as a moment that fires
   on the world's state (Ada has met him and the second ask falls tonight;
   Alison has heard the fire's founding rumour and has met him), what Tom's
   choice leaves (tea with Ada means the landing is a night away; the answer to
   Alison is a claim she remembers), measured on the forty; their words to his
   page. Their talk cards wait on the multiply rule.

2. **What the game records of the new pieces** (the session record, town list
   6p; today's y and z). About 2 h.
   Why: the reader is how Jafar learns where a friend got stuck and whether the
   town reacted. It cannot see a hint shown, an ask answered or the night's
   story coming back, so a playtest cannot say whether the first hour worked.
   Not done: production/specs/session-record.md has no `hint` or `ask` event;
   tools/session_read.py reads none. The work: the two events in the spec and
   the reader (the ask's story is already a deed topic, player.outfit_d<day>),
   with the reader's self-test; the writing is the builder's.

3. **Damaged saves against today's new state** (SaveChaos; FirstMoments,
   Arrangement, TownNews's filed list, RemarkLedger). About 2 h.
   Why: SaveChaos throws malformed values at every field of the old save; each
   new FromJson was tested by hand for a few shapes, not by the suite that
   found the old save's faults.
   Not done: ledger/SaveChaos covers none of them. The work: add them to its
   corpus, fix what it finds.

## Considered and set aside

- The Meridian conditions sampled (stage 6): they need people, and the
  runbook is his.
- The Ledger's screen and belief: waits on his ruling (town list as).
- The game's clock and the street's plain facts: on his 29 September page.
