# Lab test 5: the street's four-panel front door, from Ellis and the photographs

8 October 2026, from 11:29, branch lab. **For phase 2: not for the builder today.**

The brief:
- Ellis, *Modern Practical Joinery* (1902): the street's four-panel front door with its frame, built by script like the sash window.
- A fresh helper writes the target from the book and the photographs. When they disagree, the photographs win (Jafar's ruling).
- The target is tested against its own sources before building.
- Then an automatic check, and a fresh reviewer against the photographs.
- A small .glb and the scripts go in git, nothing large.

## The pieces

| Piece | File | Who |
|---|---|---|
| Target: sources, numbers, choices | [target/SOURCES.md](target/SOURCES.md), [target/target.json](target/target.json) | target helper |
| Target drawings: elevation, two sections | [target/target_drawing.py](target/target_drawing.py) → F:\LedgerTools\lab\door\target\target_drawings.json | target helper |
| The target's self-check | [target/self_check.py](target/self_check.py), its result in target.json "self_check" | target helper |
| Build | [door_design.py](door_design.py) (target.json's numbers only), ../tools/joinery.py (mitred mouldings), ../tools/blender_parts.py | me |
| Check | [check_door.py](check_door.py), [checks/](checks/) | me |
| Pictures and model | render_door.py, which also writes the model: F:\LedgerTools\lab\dooruild\door_v2.glb (82 KB, the door and frame without the wall). The repository's size guard (tools/git-size-guard.py) admits models only in the places the game's build imports from, so the .glb stays on F:; the scripts in git rebuild it exactly. Previews in production/previews/lab/door/ | me |
| Review | [REVIEW.md](REVIEW.md) | fresh reviewer |

## The target, and how it was tested before building

**The door** (SOURCES.md has every number's source and kind):
- **Leaf:** 812.8 × 1948 × 50.8 mm (2 ft 8 in by about 6 ft 4¾ in by 2 in).
- **Members:** stiles 114.3; top rail 127, lock rail 228.6 (centre 787 above the leaf bottom), bottom rail 192.8; muntin 132.2.
- **Panels:** four flat panels, 16.9 thick in 12.7 grooves.
- **Mouldings:** outside, a bolection moulding (36 wide, 7 proud, lapping the framing 4.8), a band across the lock rail and a weatherboard; inside, a single planted moulding.
- **Frame:** solid, 4 × 5 in, rebated 22 × 53, with an ovolo on its outer arris.
- **Above:** a 65 mm transom and a fixed fanlight 267 high.
- **Setting:** a 4½ in brick reveal and a stone sill.

**The photographs won nine disagreements with the books (D1-D9):**
- the leaf's height (Hasluck's 6 ft 8 in would not match the photograph);
- the muntin and the bottom rail;
- the lock rail's height;
- the jamb showing past the brick;
- the transom and the fanlight (Hasluck draws a hung sash);
- the top rail (Riley's printed value kept, inside the photograph's error);
- a bolection moulding outside rather than Hasluck's bead butt.

**Against the game's present door** (838 × 1981 mm, no frame, no fanlight): no source read prints that size for a front door.

**Tested against its own sources before building:**
1. **The target's self-check: 68 of 69 pass.**
   - Every printed dimension used comes back from target.json.
   - Every photograph value overrides as stated.
   - The 16 projected edges fall within 2.5 px of the main photograph.
   - The 21 internal-consistency checks pass: members add up, panels fit their grooves, the leaf fits its rebate.
   - The one failure is the six-panel photograph's overall proportion (2.38 against 2.50), reported, not hidden. The first run also caught the helper's own sign error on the moulding laps.
2. **Mine:**
   - **Ellis p.93, read on its page:** stiles 4½ in, middle and bottom rails 9 in, the lock rail at 2 ft 8 in to its centre and "about 6 in lower" from a step. The paragraph is headed "Details of interior doors", which the target applies to an entrance door; the photograph agrees.
   - **The target's elevation laid on the main photograph,** at a scale fitted on the width only (production/previews/lab/door/door-target-on-photo-2026-10-08.jpg): panels, mouldings, band, weatherboard, transom, fanlight and frame all land on the door. The leaf comes out 367 px high against the target's 372, inside the stated error.

**What the target could not settle:**
- **No dated 1880-1905 door with confirmed original joinery was found.** The main photograph (Teignmouth, Geograph 3157125, CC BY-SA 2.0) is 480 × 640 px, undated, and freshly painted.
- The second photograph is six-panel.
- The rebate, stop and moulding sizes are scaled from drawings, not printed.

## The build and its check

- **Built by script from target.json's numbers alone,** member by member:
  - stiles, rails and muntin grooved for the panels;
  - flat panels with side play;
  - bolection and inside mouldings swept round each panel with mitred corners;
  - the band and the weatherboard;
  - the frame rebated out of the solid with its ovolo;
  - the transom rebated for the leaf;
  - the fanlight's pane in grooves;
  - the stone sill.
- **The check cuts the model where the target draws it.** The front view is compared layer by layer for what shows in front (frame, glass, leaf, panels, mouldings). The horizontal and vertical sections are compared whole, at 0.5 mm a pixel, with eleven dimensions besides. The pass rule is the window's: IoU 0.97, outline p95 2 mm, worst 6 mm, dimensions within 1 mm.
- **v1** failed one test: the leaf's front view had a worst point 40 mm out. I had stopped the lock-rail band and the weatherboard 1.6 mm short of the frame's stops, for clearance, and the target runs them stop to stop.
- **v2** runs them as drawn and **passes everything**:
  - the front-view layers at IoU 0.991 to 0.998, every outline within 0.7 mm;
  - the horizontal section IoU 0.987, p95 0.7 mm, worst 4.2 mm;
  - the vertical section IoU 0.991, p95 0.5 mm, worst 3.9 mm;
  - all eleven dimensions exact (checks/check_v2.json).
  - A real band wants a hair of clearance at the stops, a point for the target in phase 2.
- **Simplifications the target makes and the build follows,** for phase 2:
  - the frame's ovolo runs down the jambs only (the drawn head and transom are plain);
  - the panel grooves run the stiles' full length;
  - no tenons, wedges, hinges, lock or furniture;
  - no inside lining or architrave.

## Fresh review

(REVIEW.md; summarised in the lab report)

## Cost

Lab time from 11:29, in the time log. Target helper 26 minutes; fresh reviewer, see the time log. One build and check run takes under a minute.
