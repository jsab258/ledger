FAILED: Marvelous Designer could not be driven by script this afternoon, so nothing was draped.

# Ron's jumper and trousers in Marvelous Designer (lab test 5, 8 October 2026)

14:43 to 16:20, branch lab. The trial installed here is evaluation-only under its terms.

## What happened

1. **The target was amended first, as ordered.** A fresh helper took 16 minutes, and its self-check passes. The amendments add everything the test 4 reviewer found missing (details below).
2. **Marvelous Designer cannot be driven by script from outside.**
   - Its Python API runs only inside the open program. It has no command line, no headless mode and no way to run a script at start-up: Marvelous's own forum (2022) and changelogs to 2026.1, as read by the builder in production/research/clothing-pipeline/MD-SCRIPTING-2026-09-29.md.
   - The builder's bridge (tools/md/md_bridge.py on wip; a copy at F:\LedgerTools\md-bridge\md_bridge.py) runs every job dropped in a folder, but someone has to press Run on it once in Marvelous's Python window each time the program opens. Its documented path had gone with the old clothing folder, so I placed a copy on F:.
3. **I sent you one notification at 14:46** asking for that click, with 15:20 as the stop. Following your order not to click through the program myself, the test stopped when no heartbeat came by 15:20; there was still none at 16:16.

**Verdict:** the drape was not tried. The question this test was to answer, whether Marvelous drapes Ron's clothes well enough to keep, remains open.

## The amended target (kept, production/lab/6-marvelous-clothes/target/)

- **A1, sleeve ease** over Ron's arm, re-measured square to it: 12 cm at the biceps, 10 at the elbow, 9 on the forearm (19, 16 and 14 mm off the arm). Test 4 left about 3 mm on the forearm.
- **A2, trouser taper and break:** the hem 54 cm round one leg (Thornton's straight leg had 57.8), sitting 2.5 cm off the floor at the back and an inch higher at the front, so it breaks once on the boot.
- **A3:** two forward pleats each side, a front crease and a back crease.
- **A4:** a flush waistband in six segments, and a fly.
- **A5, the ribs drawing in:**
  - hem rib 7 cm deep at 0.80 of the body, with the body bloused over it;
  - cuffs 19 cm round over a bunched sleeve;
  - a flat single-layer neck rib at 0.88 of the neckline.
- **A7:** a shoulder dropped 6 cm. Photograph 1 shows 8 to 10, photograph 2 nearly set in; the compromise is noted for your eye.
- **The table:** 18 photograph elements, each with what test 4 said and what the target now says; eight book-against-photograph disagreements, each settled for the photograph.
- **Self-check passed:**
  - 51 of 51 seams equal or at their stated ease;
  - 18 of 18 girths and lengths within 5 mm;
  - the three sleeve eases exact;
  - every photograph element covered;
  - no covered body point more than 3 mm outside the new outline.
- **Not reached:** 1980s British knitting leaflets, a period trouser hem width for a 42 in waist, and Ron's boot model.

**Time:** 1 hour 37 minutes of the lab. The target helper took 16 minutes; the rest was the wait for the bridge, which overlapped the download question for test 6.

## What would let it run

- **One press of Run in Marvelous each sitting** starts the bridge. Everything after that is scripted: pieces from pattern_md.json, sewing, fabric, simulation, export.
- The amended pattern is ready for that, or for any other cloth route.
- **There is no handover** to the builder, because it did not pass.
