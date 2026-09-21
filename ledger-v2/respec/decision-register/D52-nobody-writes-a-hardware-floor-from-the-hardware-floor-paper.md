# D52. Nobody writes a hardware floor from the hardware-floor paper; what transfers is its modular memory measurement

CANON: none

Ruled by Jafar, 2026-09-21, first message, under "On speech and hardware",
kept verbatim in
`game-design/decision-2026-09-21-the-week-after-the-reset-five-measurements-and-eleven-rulings.md`.
Written by the director the same day; the resident reviews and commits.

## The rule, as given

**"The hardware floor paper says close to the opposite of what was taken from
it. The sub-gigabyte figure is a stock small model scoring sixteen percent on
factuality, which its own authors do not recommend for dialogue; their
recommendation is the seven-billion model. Nobody writes a hardware floor from
that paper. What transfers is its modular memory measurement, swaps and
retrieval in tens of milliseconds at a thousand entries, which supports our
memory design rather than our model choice."**

## Where the sub-gigabyte figure was cited, looked for on main 2026-09-21

Nowhere on main. A grep over every `*.md` for "sub-gigabyte", "under a
gigabyte", "sub-GB", "below a gigabyte", "less than a gigabyte", "under 1 GB",
"factuality", "modular memory", "tens of milliseconds", "thousand entries",
"sixteen percent" and "seven-billion" returned only his message. The figure
and the paper are cited in the research delivery on its branch, which is not
in this checkout; the correction under D43 lands with the research
consolidation (queue 394 in the resident's log), and the consolidation page's
four columns sort it as "a correction the studio applies under D43" with this
record named.

"Hardware floor" on main, all three hits:

- `ledger-v2/open-questions.md` item 3: "Deferred to ship-prep by explicit
  decision (first game, personal target, min-spec is Jafar's PC for now)".
  CORRECTED in this batch under D43: the floor is not deferred to ship-prep
  and not written from a paper; it waits on the small-model test and the cost
  per hour (D47). "Min-spec is Jafar's PC for now" stands.
- `game-design/research/imagegen-licence-check.md:153`, "Claim 4, the hardware
  floor": about image-generation hardware, not the conversation model. Left.
- `legacy/design-doc.md:792`: legacy. Left.

## What transfers, recorded so the paper is not re-read for the wrong number

The modular memory measurement: swaps and retrieval in tens of milliseconds at
a thousand entries. It bears on pillar 1 (permanent per-character memory,
`vision-pillars-v2.md` line 15) and on the scale soak he reopened in the same
message (queue 116 with 351, "whether the simulation runs at three hundred
residents rather than seven"), not on which model speaks. The figures are his
reading of the paper; the paper is not on main and is not verified here.

## What this does not decide

The floor (D47's measurement). The model. The min-spec beyond "Jafar's PC for
now".
