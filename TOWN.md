# TOWN: the town session

The second session, in the worktree ledger-town on the branch town. Its lane:
- the Core simulation and its tests;
- the conversation helper;
- documents.

It never runs Unreal, renders, image or voice generation or local models, and
never touches the Unreal project, art or voices. Work for the game goes to the
builder as one line under Handovers in NOW.md. The day's summary goes under
Town in FOR-JAFAR.md by 07:00. Before every push: fetch, rebase onto main, run
the Core suites, and know what the push sets off. This file is current state and
the list only; its history is in git.

## The list (Jafar, 30 September, after the adversarial audit), in order

1. **Grounded replies.**
   - Research the method first: how studios build contextual dialogue, Valve's
     GDC talk on AI-driven dynamic dialog included.
   - Then test the audit's method: pick the facts the character actually knows
     and what they want to say first, then word it.
   - Measure against a fixed set of newcomer questions, labelled independently:
     the fallback rate before and after.
   - State, 30 September: done as asked.
     - The research: production/research/grounded-replies/PLAN-FIRST-2026-09-30.md.
     - The fixed set: sixty newcomer questions, all at least partly
       answerable, by two labellers and a third on their differences.
     - The measurement, three runs of each version labelled independently
       (MEASURED-2026-09-30.md): "that's all I know" from 36 of 60 this
       morning to a mean of 21.7 with today's version, and 18.3 with the facts
       and intent planned first. Question by question the two do not differ
       (16 better, 15 worse, p = 1.0). Inventions stay at about one or two in
       60.
     - Planning stays off behind its switch: no better, and dearer.
   - What still falls back is a reply the check refuses twice: an
     embellishment it rightly stops, or a paraphrase it still misses.
2. **Time and state defects.**
   - Arrangement.Answer accepted Wednesday's completed delivery while the clock
     said Monday. Fixed in the C#: the envelope and the no only on their own
     night. The C++ is the builder's, handed over with rows.
   - Then the same class of fault everywhere time and state meet.
   - State, 30 September: done. All fourteen faults the builder's port reviews
     found are fixed in the C#, each with a regression and rows awaiting the
     port. The sweep of the same class across the whole Core found twelve,
     each proved by a probe:
     - nine fixed, each with a regression and rows awaiting the port, and the
       route's sixteen rows unchanged;
     - three set aside, since they need a crime a detective takes, which the
       game does not have yet (FINDINGS).
3. **Support the builder's continuous route:** for each piece of the town's
   that it needs, precise inputs, outputs and acceptance cases.
   - State: handed over, production/handovers/ROUTE.md. It gives the Core's own
     week, hour by hour, as the reference; the ids fix; the talk fields; one
     TownSave; and sixteen acceptance rows with the wait's stops.
   - Next: keep the rows current when the Core moves.

**Stop:** new systems, checklist sweeps, and review rounds on depth nobody can
reach yet.

## Rules of 30 September

- **The key's cap is enforced in code.** Every run that can spend on LEDGER's
  key estimates its cost first, and stops at the day's dollar. (A newcomer
  bench labelled about a dollar once cost about $14.50.)
- **This file stays short.**

## Waiting on Jafar (the town's second page of 30 September)

- Ron's own street lines: the sample for the named cast.
- The thirty regulars.
- Whether the ending's signs wait until the week's end is in the game
  (recommended).
