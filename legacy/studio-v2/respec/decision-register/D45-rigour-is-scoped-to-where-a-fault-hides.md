# D45. Rigour is scoped to where a fault hides

Ruled by Jafar, 2026-09-15, alongside D41 to D44, and it is the one that
changes the most about how the studio spends its hours.

## The rule, as given

**"Rigour is scoped to where a fault hides. The Core keeps everything it has:
full review, golden files, planted rejecting cases, a director on simulation
changes. That is the moat and a silent fault there costs weeks. The tools that
measure the game are not the game: a fault in a checker, a watcher, a lint or
a dashboard shows up the next time somebody reads it, so they get a test and
no review, and no ruling record."**

**"The pattern this week has been that most hours went into the studio finding
faults in itself, each one real and each one costing a day. Keep finding them;
stop spending a review on each."**

## The principle underneath, which is why this is not a loosening

A fault's cost is how long it stays HIDDEN, not how wrong it is. A silent
fault in the simulation can run for weeks before anything contradicts it,
because nothing else computes the same answer. A fault in a checker announces
itself the next time somebody reads what it printed. So the two deserve
different amounts of ceremony, and spending the same on both is not rigour, it
is ritual.

THE DAY THIS RULING WAS MADE SUPPLIES ITS OWN EVIDENCE. The studio found, in
one day: a watcher that said "not yet" beside a landed frame, a formatter that
would have shipped a silently truncated verdict line, a budget reader eight
points wrong in the direction of more headroom, a tool retired six days ago
still being cited as live, and a selftest red for six days outside the gate.
Every one is real, every one was found by reading rather than by review, and
none of them needed a director to be true.

## What keeps its full review

The Core. Simulation changes. Golden files. Planted rejecting cases. A
director on all of it. Canon, the pillars, scope and the moat, which are his
and which D41 to D45 do not touch.

## What loses its review, keeping its test

Checkers, watchers, lints, dashboards: the tools that MEASURE the game. They
get a test and no review and no ruling record. The test is not optional and is
the thing that replaces the review.

## The line this record draws so a session does not have to ask

A tool that measures the game is ungated. A tool the GAME RUNS ON is not: the
line is whether the artefact ships inside the thing being played or only
reports on it. Where an artefact does both, the structural half of D41's test
decides, because that test is about what undoing a wrong answer costs.

## The consequence the studio must act on, not merely record

`director_cadence` counts changed lines across eight scope prefixes and fires
a review at a hundred, and it does not know the difference D45 just made. The
gate as it stands would keep demanding a director for a checker fix. Making
the gate agree with this ruling is itself tool work under this same ruling: it
gets a test, not a review.
