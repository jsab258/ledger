# 262: the executor adds the archive link while the register allows zero

STATUS: READY
OPENED: 2026-09-11. Ruled by
game-design/decision-2026-09-11-ruling-the-link-floor-marker-batch-and-the-answer-already-sent.md,
section 2 (e).

## What is wrong

tools/runner/executor.py hardcodes SITE_LINK (line 198) to the archive and adds
it in five places: compose_answer (371 to 394) appends "The board: <archive>"
to every session answer carrying no site link, and the four fallback wordings
(400 to 436) carry it unconditionally. Queue 259 taught the register that zero
links is legal while no page is served; it did not teach the executor to stop
adding one, and linkdest still admits the archive, so every executor reply to
Jafar carries the link the 2026-09-10 ruling exists to keep off his phone.
Measured: his "Is this working?" of 2026-09-11 was answered at 13:18:43Z by
fallback_no_cli() with that link.

## Done looks like

1. The executor reads the same marker through producer-check's own
   link_floor_state (loaded by path the way outbox.py's selftest already
   does), never a copy of the logic. While the floor is suspended,
   compose_answer adds nothing and the fallbacks carry no link; while it
   is live, today's behaviour, unchanged.
2. The selftest is a ladder: the same wordings run through the REAL
   register on both rungs with the marker planted each way, and the
   assertion at line 1844 becomes conditional on the rung.
3. The link line is one function with one call site per wording, so a
   sixth wording cannot exist to forget it.

## Ordering

After 261, before 256. 256 changes the destination; this stops the
addition during the window.
