# D39: the audit's twenty recommendations, ordered

STATUS: DECIDED 2026-09-14 by Jafar, dictated and recorded by the resident.
Process level: it orders the five research audits' findings against the
roadmap and rules out four of them. It does not itself file queue items; see
the coverage note below.

## The gate on all of it

**Nothing here starts before the visual slice lands** (D28, D31).

## The next batch after the visual slice, five items

1. **Appearance as a perception input**, since the identification ladder's
   bottom rung is clothing and nothing supplies it.
2. **The gap between the act and the discovery**, because
   `HomicideBook.Pressure` has no travel term.
3. **Objects traceable to what you did**, the other end of a model that
   already exists.
4. **The lit window looking back out**, so the information runs both ways.
5. **Sleep as a way to cross a day**, so rumour travel is something the
   player plays against rather than something that happens to them.

## The following batch, six items

1. **Enforcers**, meaning who sees through a disguise is who knows you.
2. **Show the working**, the itemised reasons that are D33's surface.
3. **What you leave at a scene**, prints and a heel mark and a dropped
   object.
4. **Frisking at a threshold**, which finally exercises the concealment
   model.
5. **Finding a person from a description**, the identification ladder run
   backwards.
6. **The town changing its behaviour after a crime.**

## Later, queued with numbers, five items

1. **Persuasion and intimidation rebased on memory rather than stats.**
2. **The camera and the tape as a witness that cannot be talked to.**
3. **Habits that make a person predictable.**
4. **Weather as an event that moves people indoors.**
5. **Failure producing content rather than a refusal.**

## Ruled out, with the reason recorded, four items

1. **Blend-in behaviour**, which is Hitman's disguise game rather than ours.
2. **A universal greet or antagonise verb**, which would make every stranger
   shallow in a game whose point is that interactions are not.
3. **A codex entry on first contact**, which is tutorial furniture.
4. **The phone box as a distraction verb**, which costs a phone system, an
   NPC response and a reason to answer, for a small tactical gain.

5 + 6 + 5 + 4 = 20, which is the count his dictation names.

## Verified at source, per rule 1

`HomicideBook.Pressure` exists at `Core/Homicide.cs:321`: it sums the body
count and, when there are live witnesses, a named weight from the best
believed confidence. No term in it reads a time or a distance for a report
to travel, which is exactly the gap item 2 names. "The identification
ladder" is an established term in the code, not invented for this ruling:
`Core/Observation.cs:68` calls it out by name against `Perception.IdRung`,
and `Core/Traces.cs:80` says a mark feeds the identification ladder rather
than the case file.

## Coverage against the queue, checked and not filed

Per D32, a ruling that orders work to the queue names the item by number and
something checks the item exists. `tools/docs-check.py` reads
`QUEUE: <number> <name>` at column 0, but its root is `game-design/` alone
and it prints every other tree, `production`, `ledger-v2` and `legacy`, as
NOT WALKED, naming that QUEUE markers are not read there either. A marker
written into this record would not be checked by anything, so none is
written here.

Checked instead by hand: a keyword grep across every file under
`production/queue/`, recursive, so it also covers `production/queue/done/`,
using each item's own words and the terms its research-audit source used.
The directory is live and other agents file into it while this was being
checked, so a total file count is a reading at an instant and not quoted
here; what is quoted is the search's result. **0 of these 20 items has a
dedicated queue item today.** Three near misses were read in full and ruled
out by hand: `040-window-practicals-in-core.md` wires lit bays from Core,
not the window looking back at the player; `037-d12-ledger-core-rescope.md`
surveys D12's clauses generally, not D33's itemised Why surface; and
`277-provenance-never-reaches-the-file-the-run-reads.md` is pipeline
provenance for an exposure pin, not object provenance in play.

**By group, with its denominator: 0 of 5 (next batch), 0 of 6 (following
batch), 0 of 5 (later, queued) and, as expected, 0 of 4 (ruled out, which
are never filed).**

**Sixteen of the twenty, everything except the four ruled out, would need a
queue item filed before work on it could start. Filing them is not done by
this record.** D32 permits a ruling to order work that a builder later
files; what it forbids is the order existing with no number and no item,
which this record avoids by naming none. Which of the sixteen to file, and
when, is his to decide.
