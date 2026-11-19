# The loop prototype's AI playtester

Written by the cloud lane, 18 Nov 2026 (advisor item 4k, from his playtest of 13:02). One command after every Fable round:

    python playtest.py --assets DIR            (DIR: the page's pictures, as for build.py)
    python ../run_proto_tests.py --assets DIR  (Fable's tests, then this playtester last)

It builds the prototype from ../project (byte for byte against the published page), plays it in headless Chromium through the game's own test hook (window.LEDGER) and writes, outside the repository (default ~/.cache/ledger-playtest/<time>/):

- sweep.md: every person on the street at 9.30, 13.00, 18.00 and 22.00 on Tuesday, walked up to from three approaches (1.2 m straight on; 2.0 m at 34 degrees either side). Faults: the talk prompt naming someone other than the person in front (and whether the sex differs), wording that does not fit the person's record (man or woman, old, young or lad), a name shown before Tom has learned it, no talk prompt in front of a person. Then a talk with each person: their replies classed as their own written lines, stock lines anyone says, or other (made by the game from what they know, scenes); turns held; replies repeated word for word. Strangers give a one-line bark and no talk. The words on screen are checked for overlaps and text off the edge.
- newcomer.md: a scripted newcomer plays the first 60 minutes (follows what the game asks by the names in its words, talks, sits in the cab for a fare every ten minutes, takes the night job, looks about, waits). Play time is booked by activity with stated estimates (walking 2.2 m/s, driving 8 m/s over 1.35 times the straight line, reading 3.3 words a second, 3 s a choice); something new (a place, a person, a kind of action, a scene) is logged when it arrives, so each half hour's count and the longest stretch with nothing new compare with Study 2.
- transcripts.md, report.json, shots/*.png (a picture every five minutes and one per sweep time).

Limits: Tom is moved in a straight line (walls ignored), so walking times are estimates and sightings along the way are approximate. Live AI talk runs only inside claude.ai, so only the written (scripted) talk is tested; live talk is untested. A seeded Math.random makes a run repeat (--seed). The game's code is not changed.

Files: playtest.py (the runs), wording.py (does a description fit a person), stock_lines.mjs (reads the stock and own lines from the source), tests/test_playtester_units.py (9 unit checks, no browser).
