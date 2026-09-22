# The Hook camera, derived from the new sheet's own geometry

Jafar, 22 September: "derive the camera's lens from the new sheet's own
geometry and write down how." This is the how.

The sheet is `hook-sheet.png`, 2048 x 1088, one street photograph made by an
image model. **It is consistent about where lines meet and inconsistent about
how far apart it drew things** — the old sheet's derivation found the same in
its own way (a kerb that bent 21.7 px off straight). So every number below says
which feature fixed it, and the features that disagreed are listed with why
they were not used.

## What the sheet fixes firmly

**1. The vanishing point of the street: x 1502, y 620** (of 2048 x 1088).
Found by edge detection, not by eye: every strong straight edge along the left
terrace — roofline, gutter, window sills and heads, fascias, stallriser, the
far kerb — gathered by a Hough transform, the outliers dropped, and the
least-squares meeting point of the 17 that remained. Median distance of a
line from that point: 6 px. The script is `hook-sheet-lens-vp.py` beside this file, so the point can be found again rather than taken on trust; its overlay was looked at, not trusted.

**2. The horizon is at row 620, 0.570 of the way down** — 76 px below centre.
Two independent reads agree: the vanishing point above, and the standing
people. For a person of ordinary height the horizon passes at the camera's
eye height, and solving two people's head and feet rows together puts it at
622.

**3. The camera is about 1.9 m up, not 1.6.** Three people, assumed 1.75 m
tall: (feet row - horizon) / (height in pixels) x 1.75 gives 1.90, 1.92 and
1.75 m. The prompt asked for 1.6 m; the model drew from a little higher, the
height of a tall man's eyes.

**4. The verticals do not lean.** Three long downpipes lean -0.6, +1.7 and
-1.2 degrees — both ways, which is the model's hand rather than a tilted
camera. So the camera is LEVEL, and the horizon sits below centre because the
picture is SHIFTED, the way an architectural photograph is taken. In Blender
that is pitch 0 with a vertical lens shift, not a camera tipped up.

**5. The camera is turned 20.4 degrees towards the parade.** The street runs
off to the right of centre (the vanishing point is 478 px right of it), so the
camera looks that far left of straight up the street. The angle follows from
the lens in step 6.

## The lens: a range, and where in it

**6. Vertical field about 46 degrees on the sheet's 1.882 frame — 77 degrees
horizontal — with an honest range of 42.5 to 50 vertical.** Nothing in a single
picture fixes a lens except a known distance along the street, and the sheet
offers several that disagree:

| distance along the street, assumed | lens it implies | used? |
| --- | --- | --- |
| Mickey's front, pilaster to pilaster, 6.0 m (our bay) | about 1260 px, 47 deg vertical | **yes** |
| the nearest parked car, 4.4 m (a 1990 saloon) | about 1170-1370 px, 43-50 deg | **yes, as the range** |
| the first-floor windows, evenly spaced, 3.0 m apart (ours are) | about 2300 px, 26 deg | no - the model drew three windows over Mickey's bay where our street has two, so its window rhythm is decoration, not a module |
| the chimney stacks, evenly spaced, one per 6 m bay | needs the roof's depth, which the sheet does not show | no |

The real objects agree with each other and the decoration does not, so the
real objects set it. 46 degrees vertical is the middle of their range; the
last choice within the range is made by rendering and overlaying, and that
choice is written into the recipe's own note.

## Where the camera stands

**7. Across the street: 7.3 m from the east frontage** — y = -2.2, in the west
half of the carriageway, 0.8 m from the west kerb. From the frontage's own
ground line: its slope through the vanishing point is the frontage's distance
over the camera's height, read at two points on Mickey's front (4.15 and 3.51,
because the shopfront's bay window bends the line) and averaged. It is, as it
happens, exactly where the old hook camera stood across the street.

**8. Along the street: at x = -3.2, just south of the terrace's end**, on the
quay apron. Fixed by making Mickey's front land where the sheet has it: its
south pilaster at 0.146 of the frame's width. With the pose above, its north
pilaster then lands at 0.383 against the sheet's 0.396 - 19 px on the sheet's
2048, which is the size of the disagreement between the sheet and itself.

## What this does NOT settle

- **The road bends.** Near the camera the painted lines run towards a point
  far to the right of the terrace's vanishing point: the model drew the road
  curving where our Quay Street is straight. The near road will not line up,
  and that is the sheet, not the camera.
- **The sheet's terrace is lower than ours.** Read against the camera height,
  its eaves sit at about 5 to 5.5 m; ours are at 6.2. That is a composition
  question - the third step of the visual lane - and not a lens one.
- **The sheet's facade runs on past Mickey's to the left edge of the frame**;
  our terrace ends 3 m south of Mickey's front. Also composition.
