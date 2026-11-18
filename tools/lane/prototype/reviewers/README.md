# The simulated Steam panel (lane task 4m, 18 Nov 2026)

After every published round of the loop prototype, eight fresh helpers each play one kind of player (CARDS.md) and review the build from the playtester's record alone. A signal for choosing the next round, never a gate on its own.

## Steps

1. Play the build: `python ../playtester/playtest.py --assets DIR --allow-changed --out OUT`.
2. Make the packet, the only thing a reviewer sees: `python packet.py OUT packet.md --label "build of ..."`. It holds the activity mix, new things over time, tense moments, the sweep's faults and the transcripts; lines naming our intentions (objectives, design, canon, rulings) are left out.
3. Give each of the eight cards to a fresh helper with PROMPT.md, the card and the packet (the helper reads only those two files). Each answers in JSON.
4. Collect the eight answers in `reviews-<round>.json` and score them: `python themes.py reviews-<round>.json` (PLAYERS.md's forty themes, word lists rebuilt here, beside KCD2's and Mafia's shares).
5. Write production/lane/REVIEWS-<round>.md: thumbs-up share, quit points, most exciting moments, recurring complaints backed by the playtester's evidence (ranked, the next round's candidates), and complaints that go against deliberate design (no waypoints, no minimap, talk as the consequence) logged as expected friction.

## Calibration

The panel must tell the 12:00 build of 18 Nov (before the eight fixes) from round 1's build on the faults fixed. Both builds are played by the same playtester (the 12:00 source copied beside it) so the packets differ only by the build. If the panel cannot tell them apart, the method changes (two tries) and the change is said plainly.
