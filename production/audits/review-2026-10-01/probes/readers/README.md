# The four readers' programs, 1 October

Each reader worked in its own scratch folder, on copies, and never built inside the repository. Their programs are kept here as they ran, with their output; paths inside them point at those scratch folders. To run one again, copy it beside a checkout and build it as its first lines say (g++ 13 with `-I ue-probe/Source/LedgerProbe/Public -I ue-probe/tests/unreal-shim` and `ue-probe/Source/LedgerProbe/Private/Perception.cpp`; .NET 8 for the C#).

## route/ (the route's logic)
- `p1.cpp`, `p1.txt`: who counts as an onlooker by the cast's day, and who the damage's tick says "was there" (B-c).
- `p2.cpp`, `p2-cs/`, `p2.txt`: the same cases in C++ and C#; they agree on all 3,884 lines (the walls, OnQuayStreet, WouldReport, the keeper's line).
- `p3.cpp`, `p3.txt`: meetings and familiarity, the evidence the talk is sent (N1), the reports and the constable, keeping quiet, a threat (N3), the rung-4 clauses (N2).
- `p4.cpp`, `p4.txt`: Darren's street regard at the fixed 0.20 against 0.40 (M1).

## time/ (time and state)
- `gamesim.cpp`: a line-by-line mirror of the game's free-play clock in CrimeProbe.cpp (its hour, its minute rounds, the constable's hour, and the wait with its hour-by-hour stops, including a verbatim copy of `WaitHourByHour`) over the game's own TownWeek, Waiting and LiveClock headers and the real cast file. What Unreal does (bodies, text on screen) is printed instead.
- `gamesim.txt`: its cases, re-run by this session: `tea-cells` (M3), `ellis-false` and `ellis-false-night` (M2), `no-late` (L4), `tea` (L6), `misc` (the spell in the cells, `Answer(Refused)`, `AsksNow`), `b5` (B5), `ellis-true` (B2's missed visit, fixed).

## save/ (save and reload)
- `talk-probe.sh`, `talk-probe.txt`: the talk program with stand-in replies, sent the lines the game now sends: C1's case (fixed), Ron's and Sheila's pending questions across a Continue (C5 b), a failed talk save (S2). Re-run by this session.
- `reload-week.cpp`, `reload-week2.cpp`: copies of the route's week (route-week-test.cpp) that save and reload the town part way through, the way the game does; `reload-week.txt` (all 171 hour ends) and `reload-mid.txt` (140 points inside an hour): every run gives the straight week's sixteen rows and end state (C4).

## port/ (the port and its tests)
- `harness.cpp`, `Program.cs`, `harness.csproj`: the same cases on both sides for the new branches the golden table does not cover; `h_cpp.txt`, `h_cs.txt` their output. They differ only in the C++ cast reader's hours (accepted, refused in C#) and the capital of a non-ASCII first letter.
- `mutate.sh`: breaks one line of the C++ at a time and re-runs the golden comparison (D1).
