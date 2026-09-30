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

## The list (Jafar, 30 September afternoon), in the order of the research note

The research: production/research/grounded-dialogue-selection. "That's all I
know" is what is left when the check refuses a true answer twice, and the check
was never tuned against labelled examples. Where things stand: on the sixty
fixed newcomer questions, labelled independently, it fell from 36 to about 22
on 30 September; two ways of prompting the writer failed and are off.

1. **The empty answers by cause:** for each, the wrong facts chosen, a real
   invention, or a true paraphrase refused.
   - State, 30 September: done (grounded-replies/CAUSES-2026-09-30.md). Of 21
     empty answers, all answerable from what they knew: the facts chosen missed
     the answer in 12 (nothing chosen in 7); the check refused a true detail in
     16, and 29% of all it refused was true; the other 89 refused details were
     invented. So item 2 needs the choice fixed first, or it says the wrong fact.
2. **When the check refuses twice,** the character states the chosen facts
   plainly, in their own manner, built by code. "That's all I know" stays only
   for when no fact was chosen. One sample on his page, one screen.
   - State, 30 September: built, reviewed twice, measured, and off
     (grounded-replies/PLAIN-AND-CHECK-2026-09-30.md). Empty answers fell from
     about 26 to 16 where they could answer, no plain line invented anything,
     but 84 of 123 plain lines were beside the point and every honest "don't
     know" went. It waits for item 4's choice of facts. Ron's sample is on his
     page.
3. **Tune the checker** on about 250 labelled details, confirmed on questions it
   was never tuned on.
   - State, 30 September: done, today's check kept. 255 details labelled
     blind: of what it refused, 62 of 130 were true; of what it passed, 7 of
     90 invented. Three versions (code first, examples from the tuning half,
     two looks) each trade fewer true refusals for more inventions on the
     held-out half; none passes the rule, so tuning is set aside after three
     tries.
4. **A small rule table for the first week:** the kind of question, who is asked
   and what they hold decide between an answer, a partial answer, "don't know,
   ask someone who does", or a written line.
5. **Measure every change** on the sixty, on a new sixty nobody tuned on, and on
   thirty questions nobody in the town can answer.
   - The sets: a helper who saw neither the facts nor the failures wrote twenty
     new first lines and ten nobody can answer (half of them leading), each
     asked of Sheila, Ron and Darren and labelled answerable or not by two
     labellers and a third (bench/firsts-held.txt, firsts-none.txt).
6. **The builder's continuous route**, done before this list: the time-and-state
   faults fixed (all fourteen, the sweep's ten, the independent checks'
   catches), and ROUTE.md handed over; keep its rows current when the Core moves.

**Stop:** new systems, checklist sweeps, and review rounds on depth nobody can
reach yet.

## Rules of 30 September

- **The key's cap is enforced in code.** Every run that can spend on LEDGER's
  key estimates its cost first, and stops at the day's dollar. (A newcomer
  bench labelled about a dollar once cost about $14.50.)
- **This file stays short.**

## Waiting on Jafar

- How Ron says the facts plainly (the town's page of 30 September; off for
  now, it waits for item 4).

After the list: the named cast's own street lines, in Ron's pattern (his tone
approved, 30 September).
