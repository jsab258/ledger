FAIL

# Shopfront unit 3.2, Rita's front: fresh review of the CLOSE view (v1)

11 October 2026, cloud week 42. A fresh reviewer: this reviewer did not write the target or build the piece, and has not seen any other verdict. The brief followed is `production/cloud-week/kit/REVIEW-BRIEF.md`.

The piece was judged on its render (`kit-shopfront/render/close.png`, 1600 x 1200; preview `production/previews/cloud-week/shopfront/shopfront-close-v1-2026-10-11.jpg`). The camera is 1.75 m out and 1.27 m to the right of the left pier, at 2.65 m, looking at the capital, the console, the end of the fascia and the cornice. Light, the pale ground and the absence of wear are not judged. Three things are out of this unit's scope and also not judged: the blank fascia, the dark opening where the side door goes, and the pale strip under the board where the door head is missing.

**Verdict:** FAIL, on two faults that a player would see at this distance. The worst is the console's side profile, which comes from the target and is not a narrow point. The leaf is the build's fault.

## Faults, worst first

### 1. The console's scroll is shallow and has nearly equal rolls at top and bottom, so it reads as a block with two rolls. The photographs show a tapering bracket with one large scroll. (TARGET's fault: the build followed it within 0.1 mm.)

- **Where in the view:** the console in the middle-left of the frame. Its left edge is its side profile seen at about 39 degrees, from y 330 to 690.
  - The top roll stands out about as far as the bottom roll, at x 690 and x 695.
  - The body between them is almost flat. At the waist the console is only 20 mm in front of the fascia: waist d 140, board face d 120.
  - The side volutes show as two small coils at the ends of the rolls, at x 815, y 380 and y 655. Their 5 x 4 mm grooves read as scratched lines.
- **The target's numbers:**
  - Upper volute r 45: its diameter is 0.44 of the 205 depth.
  - Lower volute r 26: 0.25 of the depth.
  - Waist 140: 0.68 of the depth.
  - The lower volute's front is d 184, so the foot is almost as deep as the top (205).
- **What the photographs show instead:**
  - **Kennington Lane, 2013** (console close up, side seen almost square on):
    - The upper volute fills about 0.85 of the console's depth and is its main feature: a raised spiral band of 2 to 3 turns around a proud eye.
    - The body narrows to about 0.5 of the top depth.
    - The lower volute is about 0.6 of the top depth, with a pendant drop below it.
    - The console stands well out from the fascia. These ratios come from the 640 px image and are good to about 15 per cent.
  - **64 Marygate, York, 2013:**
    - Each console has a large scroll at the top. Its body tapers to about 0.4 of the top's depth at the foot, with a pendant leaf below.
    - The cornice breaks forward over each console under a lead cap.
  - **Percy Park Road, Tynemouth, 2021** (a northern port):
    - A large roll at the top and a long body tapering to a small lower roll.
    - A round drop at the foot.
  - In all three photographs, the top is clearly the larger end and the console projects well past the fascia. None is a near-equal pair of rolls on a flat face.
- **Why the target got here:** it had no photograph of a console (its section 6 says so). It set the waist at 140 or more so that the board's bed mould (d 132) would not show beside it. Inside a 205 envelope that left no room for a real scroll.
- **The exact fix**, to the target's `parts.console` (`side_silhouette`, the spirals, the bosses, CON-01 to 09) and then a rebuild:
  - **Keep:** 240 wide, 550 high, z 2850 to 3400, centred on u 175 / 5825, the 12 mm front chamfer, and the waist at d 140 or more (the board rule stays).
  - **Top:** the cap block goes to d 290 at z 520 to 550.
  - **Upper volute:**
    - Eye at d 200, z 440 (local); outer radius 80, so the front reaches d 280 at z 440 and the top reaches z 520.
    - 1.5 turns.
    - On the side, a raised spiral fillet 10 wide, standing 6 proud, in place of the 5 x 4 groove.
    - An eye boss 30 across, standing 8 proud.
  - **Body:** concave, from the volute's underside (about d 200 at z 360) down to the waist at d 140, z 170.
  - **Lower volute:**
    - Eye at d 125, z 60; outer radius 40, so its front is d 165. It rolls the other way.
    - The same raised fillet and a boss 20 across.
  - **Foot:** 130 deep, on the capital's flat. The capital's 175 front stays 10 in front of the lower volute.
  - **Optional:** a turned drop 60 long under the lower volute (Kennington and Tynemouth have one).
  - **The cornice** (`parts.cornice`, COR-*): it must break forward over each console, as at York. Over u 45 to 305 (and 5695 to 5955), the 19-point section moves out 85, so the nose is at d 300. It is returned back to the main run's nose (d 215) by mitred returns on both sides. The outer end's existing return to the wall stays.
  - This changes the cornice's plan and the console's envelope, so it is a target change. Whoever owns the fascia target should be told, because its cornice is described as fixed.

### 2. The leaf reads as a stack of horizontal ribs (a stepped wedge), not as an acanthus leaf. (BUILD's fault, with one point the target left open.)

- **Where in the view:** the front face of the console, the centre of the shot, x 740 to 800, y 440 to 595.
  - About seven horizontal grooves cross the whole width of the leaf, so the edges step like a stack of plates.
  - The midrib barely shows. There are no separate lobes, and nothing turns forward.
  - The leaf stops flat under the top roll.
- **What the photographs show instead:**
  - **Kennington Lane, 2013:** a carved acanthus with a raised midrib. Veins run from the rib out to each lobe's fingers. The lobes curl forward, and the leaf's head lies over the front of the upper scroll.
  - **64 Marygate, York, 2013:** the leaf is a pendant at the foot of the console, with two rosettes.
  - **Tynemouth, 2021:** low-relief carved leaf and flower motifs run down the front.
  - None of them has grooves running straight across the leaf.
- **Who is at fault:**
  - The target asks for 3 lobes a side, a rib 8 wide standing 4 proud, and grooves 4 x 3 between the lobes, but it does not say which way the grooves run.
  - The build's notes say the grooves cross the leaf at each notch ("not diagonal veins"). That choice, together with the row-by-row dome, makes the stepped wedge.
- **The exact fix** (build; the target should add the vein direction to `leaf`):
  - Model the midrib as a raised strip the full length of the leaf, 8 wide and 4 proud of the dome.
  - Replace each across-leaf groove with a vein, 3 wide and 2 deep, running from its notch up and inward to the rib, so the veins make a chevron that points down the leaf.
  - Dome each lobe on its own: 12 at the lobe's middle, 0 at its notches. Turn each lobe tip 6 forward.
  - Carry the leaf's head 50 up over the front of the upper roll, following its curve, rather than stopping under it.

## Narrow points (each a small detail with an exact fix; not a fault on its own)

1. **No bed mould under the cornice's corona** (TARGET's). The top of the fascia meets the 95 mm flat soffit at a bare right angle, along the top of the board in the view.
   - York (2013) shows a dentil course and a moulding in that angle; Kennington (2013) a dentil course; Norwich Bank Street (2013) an enriched band.
   - Fix: a cyma reversa bed mould, 40 high, from d 120 to d 150, at z 3360 to 3400. It stops against the consoles' inner sides and stays clear of the drip groove at d 155.
2. **The capital's tablet** has square, sheet-like edges. A 3 mm ovolo or chamfer round it would read as joinery. Seen at this distance; not seen from the street.
3. **The render, not the piece:** the pale strip of sky between the board's underside and the interior box (x 925 to 1600, y 645 to 690) is the missing door head. In the next close render, the scene's interior should reach up to the board or a plain head should be added, so the reviewer reads the board's foot against something dark.

## What is right

- **The order of members** is the one the photographs show, with no gaps, overlaps, floating parts or faceting:
  - the panelled shaft;
  - a round astragal;
  - the die with its tablet;
  - the hollow flare and the abacus;
  - the console standing on the capital's top;
  - the board between the consoles, standing 55 on the capital;
  - the cornice oversailing the console, with the drip groove and the mitred end.
- **The capital's kind** (a necking, a plain die, a flare to a top slab) matches P1 Leadenhall's flared pier cap (`P1-leadenhall-pilaster-capital.jpg`: ledge, die, flare, slab). Pilasters carrying the entablature on a capital are what Norwich (2013) and York (2013) show.
- **The rolls and spiral eyes** are smooth and clean at this distance. The 12 mm chamfer on the console's front edges and the 1 mm eased arrises read as painted joinery.
- **The oxblood paint is the right kind:** the Kennington console and fascia are painted this colour.
- The blank fascia, the empty side-door opening and the missing wall are out of scope, as the brief says.

## Photographs used

All from Geograph, licence CC BY-SA 2.0. Each page was read on 11 October 2026 and its "taken" date checked on the page. They are used for judging only: none is in the repository or the game.

| page | taken | author | licence | what it shows | used for |
|---|---|---|---|---|---|
| https://www.geograph.org.uk/photo/4782551 "Detail of 332 Kennington Lane" | 2013-04-20 | Stephen Richards | CC BY-SA 2.0 | a C19 shopfront console close up, side almost square on: large upper volute with a raised spiral, acanthus over the front, lower volute, pendant drop; maroon paint | faults 1 and 2, the dentil course (narrow point 1), the paint |
| https://www.geograph.org.uk/photo/4919236 "Detail of 64 Marygate, York" | 2013-05-14 | Stephen Richards | CC BY-SA 2.0 | a Victorian corner shopfront (northern town): tapering consoles with large top scrolls and pendant leaves, the cornice broken forward over each console under lead, a dentil course under the cornice, fluted pilasters | faults 1 and 2, narrow point 1 |
| https://www.geograph.org.uk/photo/6767122 "Ruby & Frank, 4 Percy Park Road, Tynemouth" | 2021-03-02 | Geoff Holland | CC BY-SA 2.0 | an 1880s shopfront in a northern port: a tall console with a large top roll, a tapering carved front, a small lower roll and a round drop | faults 1 and 2 |
| https://www.geograph.org.uk/photo/5215258 "Detail of 8-10 Bank Street, Norwich" | 2013-06-16 | Stephen Richards | CC BY-SA 2.0 | a late Victorian front: panelled pilasters with capitals carrying the entablature, an enriched band under the cornice | the capital's place, narrow point 1 |
| https://www.geograph.org.uk/photo/2812069 "Row of shops, Portland Road, Hove - 1984" | 1984-10-12 | nick macneill | CC BY-SA 2.0 | a 1984 parade of fronts with pilasters and fascias, much altered | period context only: at 640 px the consoles are too small to read, so it is not evidence for any form above |

The target's own photographs (P1 Leadenhall Market, 2019, CC0 Poly Haven: the previews in `production/previews/cloud-week/refs/shopfronts/`) were also compared. They show no console at all, as the target says.

None of the photographs above was taken between 1975 and 1995 at a scale that shows a console. The objects in them are Victorian (1840s to 1880s fronts) and stood the same way in 1990. Most Geograph close-ups were taken after 2005, so the dates are given as they are.
