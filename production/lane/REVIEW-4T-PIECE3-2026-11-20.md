# Review of 4t: the gate calling the machine checks, and piece 3 (breakers)

Fresh reviewer: Opus at high effort, 20 Nov 2026 about 02:25 Swiss time, read only, against the code and its own docs.
Verdict: PASS WITH FIXES (6 must, 7 should). Fixed once by the lane the same run; 22 unit checks pass; an end-to-end replay of a short real session reached the same game at every action.

## Must, all fixed
1. The gate passed with the machine checks skipped. Now a gate run without them never passes.
2. An old machine report could stand in for this build's. The option is removed: the gate always runs the checks on the build it judges and deletes any earlier report first.
3. A money, people or cab claim was marked reproduced by any unrelated rule fault, and people by a one-frame graze. Now money reads only the money rules, people only the 1.5 s held scan; cab has no machine test.
4. A crash claim was reproduced by any error at any time. Now only errors raised while the claimed action itself ran count.
5. Money and cab tests cannot see most claims ("paid twice", "money from nothing"), yet a holding test gave a final no. Now only crash, stuck, camera and content can give NOT REPRODUCED; money and people give NEEDS A LOOK when the test holds; cab, soft lock, talk, period, other are NEEDS A LOOK.
6. BREAKERS.md said words were compared and cab was checked by machine. Rewritten to match the code.

## Should
- Fixed: the action log is now one session per folder (play.py refuses a used folder; replay refuses a log whose numbers do not climb); the seed is written as the log's first row and read back; unquoted typed words are all typed, as logged; one broken replay no longer loses the others; replay's work folder lives inside --out and is removed after; testers get a copy of play.py outside the repository (PLAYDIR) instead of repository paths; setting details taken out of the breaker cards; the stop answer no longer shows page errors the tester never saw.
- Left open: a known-list key for rules with no place in them ("rules hold every game hour", "no page errors") would hide every new fault of the same rule; KNOWN.json holds none today, and whoever adds one must key it by the fault's own words. Named in TESTING-SETUP-4T-2026-11-20.md.
