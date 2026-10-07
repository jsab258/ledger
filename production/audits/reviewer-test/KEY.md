# The test's pictures: which frame is which

Hidden from every reviewer until all reviews were in. Frame 26 is a clean copy of base B09 made only for the realism check. "Pixels changed" counts pixels that differ from the clean copy by more than 24 levels, so soft faults (the low-resolution brick, the prompt's box) count low; the box gives their extent.

## The ten bases

| B01 | mickeys-room-furniture-day-2026-10-06.jpg | whole picture |
| B02 | mickeys-room-furniture-night-2026-10-06.jpg | whole picture |
| B03 | morning-hook-day-2026-10-07.jpg | 0, 0, 1600, 512 |
| B04 | morning-reverse-day-2026-10-07.jpg | 1025, 0, 1600, 900 |
| B05 | morning-night-2026-10-07.jpg | 0, 0, 1600, 512 |
| B06 | proof-2.6-shop-signs-and-bills-2026-10-04.jpg | 0, 0, 885, 900 |
| B07 | rita-day-kit-2026-10-06.jpg | 490, 0, 1600, 900 |
| B08 | rita-night-kit-2026-10-06.jpg | 490, 0, 1600, 900 |
| B09 | proof-2.6-mickeys-try3-2026-10-04.jpg | 1092, 0, 1600, 900 |
| B10 | proof-2.6-shop-signs-and-bills-2026-10-04.jpg | 975, 0, 1600, 900 |
| Base | Preview it is cut from | Cut (x0, y0, x1, y1), none = whole |
|---|---|---|

## The twenty-five frames

| Frame | Base | View | Fault | Where (x0, y0, x1, y1 px) | Pixels changed |
|---|---|---|---|---|---|
| frame-01 | B08 | Rita's front at night | fireflies: about fifty bright white specks over the dark fascia and the kiosk's side | 20, 10, 1100, 880 | 0.05% |
| frame-02 | B07 | Rita's front by day | mirrored text: the kiosk's 'Telephone' sign reads backwards | 652, 226, 764, 302 | 0.37% |
| frame-03 | B03 | hook view by day, upper part | stretched texture: the brick on the corner house's side smeared into horizontal streaks | 1330, 120, 1530, 290 | 1.11% |
| frame-04 | B07 | Rita's front by day | clean (no fault) |  |  |
| frame-05 | B03 | hook view by day, upper part | black square: a flat black block over the houses at the street's far end | 448, 392, 506, 446 | 0.39% |
| frame-06 | B06 | shop row, left part | missing window pane: the lower right pane of the middle first-floor window is a black hole | 428, 204, 455, 254 | 0.18% |
| frame-07 | B05 | street at night, upper part | debug text: the engine's red LIGHTING NEEDS TO BE REBUILT message top left | 8, 6, 470, 46 | 0.40% |
| frame-08 | B05 | street at night, upper part | clean (no fault) |  |  |
| frame-09 | B09 | Mickey's door and corner | hole in a wall: a ragged hole through the corner wall with sky behind it | 382, 556, 454, 623 | 0.64% |
| frame-10 | B04 | reverse view by day, the Ironmonger | floating object: the litter bin and its post sit 55 px too high, the post's foot hanging above the pavement | 250, 545, 340, 790 | 0.83% |
| frame-11 | B03 | hook view by day, upper part | clean (no fault) |  |  |
| frame-12 | B06 | shop row, left part | duplicated object: a second pillar box stands into the first, half overlapping it | 152, 500, 278, 664 | 0.93% |
| frame-13 | B10 | shop row, right part | untextured placeholder: the fish shop's upper window is a flat grey panel | 420, 143, 482, 258 | 0.50% |
| frame-14 | B02 | office at night | a ragged white strip across the top pane over the blind (the night picture had none) | 588, 92, 918, 138 | 0.63% |
| frame-15 | B04 | reverse view by day, the Ironmonger | a dark seam stripe down the roof's slates from ridge to eaves | 314, 124, 356, 296 | 0.08% |
| frame-16 | B08 | Rita's front at night | a floating 'Talk to Rita' prompt over the pavement with nobody there | 288, 692, 463, 730 | 0.08% |
| frame-17 | B10 | shop row, right part | low-resolution texture: the fish shop's upper brick is blocky and blurred either side of its window | 338, 108, 625, 326 | 0.12% |
| frame-18 | B07 | Rita's front by day | wrong scale: one vase in the window three times the size of the goods around it | 200, 450, 284, 576 | 0.54% |
| frame-19 | B09 | Mickey's door and corner | texture tiling: the corner wall's lower part is one small stained tile repeated in a grid, seams showing | 306, 330, 500, 750 | 3.95% |
| frame-20 | B10 | shop row, right part | clean (no fault) |  |  |
| frame-21 | B01 | office by day | test-colour block: the notice board on the right wall is flat magenta (a missing material) | 1157, 505, 1249, 581 | 0.50% |
| frame-22 | B02 | office at night | z-fighting: jagged pale stripes flicker through one panel of the counter's front | 812, 660, 962, 795 | 0.47% |
| frame-23 | B01 | office by day | clean (no fault) |  |  |
| frame-24 | B05 | street at night, upper part | light where none belongs: a warm glow on the blank upper wall of the corner house, no lamp | 1360, 95, 1520, 255 | 0.78% |
| frame-25 | B01 | office by day | floating object: a copy of the yellow box files hangs in mid-air in front of the blind, nothing under it | 690, 400, 852, 488 | 0.55% |

The pictures themselves are not in git (the size guard keeps pictures to production/previews/); `plant_faults.py` remakes the bases and all twenty-five frames from the committed previews (`python plant_faults.py <repo> <out>`), and `key.json` is the key it wrote.

## The realism check's last good pictures

The same views two days earlier, cut the same way: B01 beside `proof-2.6-mickeys-2m-day-try3-2026-10-04.jpg`, B02 beside `proof-2.6-mickeys-2m-night-try3-2026-10-04.jpg`, B09 beside `proof-2.6-mickeys-try2-2026-10-04.jpg` (cut 1092, 0, 1600, 900). Frame-26 is base B09 itself, saved the same way. The reverse view's earlier version was left out because shapes reflected in its windows might be people.
