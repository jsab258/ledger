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
| Pictures and model | render_door.py, which also writes the model: F:/LedgerTools/lab/door/build/door_v2.glb (82 KB, the door and frame without the wall). The repository's size guard (tools/git-size-guard.py) admits models only in the places the game's build imports from, so the .glb stays on F:; the scripts in git rebuild it exactly. Previews in production/previews/lab/door/ | me |
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

## Fresh reviews

**The first (REVIEW.md, v2): FAIL, on the moulding profiles, not the proportions.**
- **What it measured right:** against the main photograph, every stile and rail, the muntin, both panel heights, the band and the weatherboard within about 1% of the door's size; the frame width, the transom light, the leaf's setback and the reveal also match; no gaps, holes or stray pieces.
- **What failed:**
  - the bolection mouldings read as flat facets (a square strip, then a straight bevel), where the photographs show bold curved mouldings with deep shadow;
  - the lock-rail band was a plain plank, and the weatherboard a flat wedge;
  - lesser: the transom is flush (the photographs' projects with a moulded top), no ironmongery, the frame's ovolo makes the jamb read round, dark hairlines along the mouldings, the sill and lintel stopping flush with the opening.

**The second try (v3), inside the target's numbers.**
- **Profiles:**
  - the bolection given a rounded nose, a fillet and an ogee (a bead over a deep cove), at the target's 36 wide and 7 proud;
  - the band a rounded top and a cove under;
  - the weatherboard a rounded nose, a throat and a hollow weathering.
- **Shading:** smooth, with the arrises kept sharp (by angle); the facets were partly flat shading.
- **The hairlines:** every moulding lifted 0.3 mm off the faces it sits on, which were coplanar.
- **Ironmongery:** a brass letter plate and a knob, placed from the photograph, as a layer the check leaves out because the target has none.
- **Context:** the sill and the arch run into the brickwork.
- **Left as the target has them, for phase 2:** the flush transom (a projecting moulded transom is a target change, and would fail the section check by more than 6 mm); the frame's ovolo of 19 mm.
- **v3 still passes every check:** the front-view layers within 0.7 mm; the sections IoU 0.985 and 0.987, worst 3.9 and 4.9 mm; all dimensions exact.

**The second fresh review (REVIEW-2.md, v3): FAIL.**
- **What is right:** "the leaf is a close copy of the main photograph": the layout, the panel mouldings now the right size, the letter plate's size and place and the knob's height, the fanlight and the frame's width; "from the street it reads as a late-Victorian four-panel door".
- **What fails**, sorted by where each comes from:
  - **The target, against its own photographs** (the photographs-win rule missed these three):
    - the frame's ovolo makes the jambs read as round tubes beside a square head and transom; both photographs show a flat, square-edged frame;
    - the transom is flush, where the photographs show a deeper moulded transom projecting over the door;
    - the sill is a thin slab, where photograph 1 has a deep stone step.
  - **The build:**
    - overlapping surfaces in the context stonework (diagonal stripes on the lintel's ends and the sill's left end) and an odd step at the left jamb's foot;
    - the ironmongery reads as stand-ins (a flat disc knob too near the edge, a bare letter plate, no lock);
    - the band and weatherboard still read as plain boxes, and the weatherboard runs into the frame.

## Result

- **Two tries, two fresh reviews failed: set aside by the two-tries rule, for phase 2.**
- **The proportions are right by every measure:** the check (every drawing within its tolerance, all dimensions exact) and both reviewers (within about 1% of the photograph).
- **What failed is detail the target did not write down:** profiles, ironmongery, the frame's edge as the photographs show it.
- **Phase 2's first step is the target, not the model.**
  - Square the frame's edges and give the transom its projecting moulded top, as the photographs show (the photographs-win rule).
  - Write the band's and weatherboard's profiles from the photograph.
  - Add a lock, a framed letter plate and a turned knob, and the step.
  - Then rebuild, and remove the overlapping context faces.

## Verdict on the method

**It worked for the proportions and not yet for the door,** as with the window.

**The exact target and the automatic check did their part:**
- the target was tested against its sources before building: its own self-check (68 of 69), my reading of Ellis's page, and its elevation laid on the photograph;
- the build matched it at the second run.

**The fresh reviewer then found what neither carried:**
- the profiles' character;
- the ironmongery;
- three places where the target followed the books against its own photographs.

**The lab's lesson again:** the photographs-win rule has to be applied element by element, edges and profiles included, by the target writer and checked by someone else before building. Half of the second review's faults would have been caught there.

## Cost

Lab time from 11:29, in the time log. Target helper 26 minutes; two fresh reviewers, 8 and 6 minutes. One build and check run takes under a minute.
