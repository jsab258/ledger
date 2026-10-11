FAIL

Fresh review, unit 3.4, the bollards (K1, K2, K3, K4, K6, K5 left to right), view "street": camera 6 m out at eye height 1.6 m, looking at the row's centre 0.5 m up, 38 mm lens. That gives about 3.5 mm a pixel at the row; K6's 440 mm head spans about 125 px. Render v1: `scratchpad/kit-bollards/render/street.png`, preview `production/previews/cloud-week/bollards/bollards-street-v1-2026-10-11.jpg`. It is judged against the target's photographs (Poly Haven 2019 previews US01_b, BB_b, US02_a, LH_b and LH_b's foot close-up) and seven Geograph photographs, three of them from 1979 to 1990 (listed at the end). Crops and downloads are in `scratchpad/bollard-review-street/`.

One fault a player would see at this distance: the head of K6, the quay mooring bollard. Everything else passes, with the narrow points listed below.

## Faults

1. **K6's head is built as the kit's raw polyline, with hard creases. The target asks for a rounded rim and a dome.**
   - **Where in the view:** the fifth post from the left. The mushroom head reads as a crisp, machined hat: a sharp crease where the underside meets the rim (r 210, z 590), a vertical band (r 220, z 630), a second crease above it (r 200, z 670), then a straight cone to a second flat at (r 110, z 710). There are further hard steps at the barrel's shoulder (r 150 to 130, z 470 to 510), where the neck meets the head's underside (r 130, z 550), and on the flange (r 250 to 190, z 40 to 60). The crisp band is about 23 px tall at this distance, with highlights on both creases, and is plainly visible.
   - **What the photographs show instead:** every cast mooring bollard photographed has a rolled rim and a domed top, with no flat facets or creases. Belfast 2019 (Geograph 6026508) shows a mushroom head with a fully rounded rim and a gently domed crown. Glasgow 2013 (Geograph 3463316) shows a thick head with a heavily rounded edge and a rounded underside running into the waist. The squat quay post in Hull 1982 (Geograph 7461489, left foreground) has a softly flared top.
   - **Whose fault:** mainly the build's. The target says "soften the kit's polyline corners into R10 or more" (`kinds.K6.parts[head].what`) and "then a dome". The build lathes `profile_rz` as it stands, and NOTES.md says "no departures". The target shares the blame: its `profile_rz` for K6 is still the unsoftened polyline, so any build made by script from the numbers alone reproduces the creases. The builder's own 1 mm Hausdorff profile check for K6 then rewards the creases.
   - **The exact fix, in the build** (and ideally in the target's K6 `profile_rz`), with K6a's points otherwise unchanged:
     - **(a) Rim.** Replace the corners at (210, 590), (220, 630) and (200, 670) with one circular arc through all three points: centre (r 158.3, z 624.2), radius 61.9. That makes a bull-nose rim.
     - **(b) Top.** Replace the run from (200, 670) through (110, 710) to (0, 720) with one spherical dome of radius 425, centred on the axis at z 295. It passes through (200, 670) and (0, 720) and lies within 4.5 mm of (110, 710).
     - **(c) Remaining corners.** Fillet with R 20 at (150, 470), (130, 510), (130, 550) and the rim-to-underside join. Use R 10 at (250, 40), (190, 60) and (170, 80), and R 5 on the flange's foot edge.
     - **(d) Sampling.** Sample each arc at least every 10 degrees.
     - **(e) Check tolerance.** Loosen K6's profile check to the fillets' deviation (at most about 8 mm at a corner) instead of 1 mm.

## Narrow points (exact fixes, not seen as wrong at 6 m)

1. **K5's four nuts are sunk into the flange.** Where: the last post's foot. Only four small pale stud tips show, and no hex nuts.
   - The build seats each nut at the rim top (nut z 35.5 to 50.0, across r 111.8 to 136.2). The flange's top surface over that footprint rises from z 42.5 to z 65.4, because the pitch circle (r 124) lies on the slope from (141, 40) to (125, 50) to (105, 72). Each nut is therefore more than half buried and its inner half is fully inside the casting.
   - LH_b's foot close-up shows four hex nuts standing fully proud on a flat seat near the rim, with the cove up to the shaft starting just inside them.
   - Whose fault: the target's (its profile slopes where the photograph shows a flat seat) and the build's (it placed the nuts without testing that they sit on the surface).
   - Fix: give the flange a flat seat. In K5's `profile_rz`, replace (141, 40), (125, 50) with (141, 40), (139, 42), (108, 42), then cove up to (100, 52) and (95, 70), rejoining at (91, 100). Seat the nuts at z 42 to 56 and the studs at z 42 to 70.
   - Add a check that each nut's underside lies within 1 mm of the flange surface over its whole footprint. This will be a fault in the close view if it is left.
2. **K5's chain lugs are square-ended plates.** Where: the four small tabs on the last post at z 420 and 840. They read as welded flat bars, not cast D-lugs.
   - The target says "D-lug" but gives no outline. The builder's rectangle, 40 by 55 with 2 mm edges, is a judgement.
   - Fix: keep 55 high where the lug meets the shaft and taper the sides to 36 high at the hole centre (22 from the shaft face). Close the outer end with a half-round of radius 18 about the hole centre, so it is still 40 proud with a 6 mm wall around the 24 mm hole. Round the edges R 3.
3. **K2b (950 high, low cone cap) and K6b (982 high, the upturned cannon) are not built, and nothing says so.**
   - The target's section 9 asks for nine models: K2 two, K6 two.
   - NOTES.md says "no departures", and `checks/check_v1.json` `not_built` lists only K7, K5's chain and the conditions.
   - Fix: build both from `profiles_final.US02_a` and `kinds.K6.variants[K6b].profile_rz`, or add them to NOTES.md's "Not built" line and to `not_built` with the reason.
4. **Small features of K3 and K4 are neither modelled nor listed as not built.**
   - K3's two vertical mould lines and its pour line at z 400.
   - K4's vertical weld seam and its 2 mm cap weld bead.
   - None of these is visible at 6 m. Fix: say in NOTES.md that they go into the engine's normal maps, or model them at 1 to 2 mm.
5. **For the target, not the build: period chain posts.** On the 1979 working quay at Ramsey (Isle of Man; Geograph 3452068), the quay-edge chain posts are thin plain steel tubes, painted, with a chain sagging between them. K5's bolted, beaded cast post comes from a 1980s-to-90s marina, as the target itself says in section 11. Keep K5 as built, but the target's next version could note this period alternative for an unrestored 1990 quay.

## What is right

- **Order, heights and proportions read true across the row.** K5 is tallest, then K1, K2, K4, K3, and K6 is the squat one. K5 to K1 measures 1.05 in the render against 1135/1082 = 1.049. Nothing floats and nothing sinks; every foot meets the ground. The silhouettes are smooth: at 64 sides the facet depth is about 0.3 mm even at K6's flange.
- **K1 matches US01_b**, as on the target's overlay:
  - a plinth with a coved shoulder;
  - one straight taper;
  - the fat half-round bead at half height;
  - the upper taper, neck and fat cap collar;
  - the quirk and thin ring;
  - a flattened dome, not a hemisphere.
  
  It is the same family as the cast-iron post in Reading 2013 (Geograph 3842932): a taper with rings and a domed head. It has no band, lettering or crest.
- **K2 matches BB_b and US02_a.** It is a plain straight taper with a thin rounded collar band just above half height, the rolled foot ring wider than the shaft, and the flat cap plate slightly overhanging. It is black by default.
- **K3 is a plausible plain precast post.** It is a tapered round post with a chamfered, slightly domed top, unpainted grey and with no band. The round concrete posts at Kings Langley (Geograph 4680721, 2015) are the same plain kind, with flat-chamfered tops.
- **K4 is a plain black tube with a shallow welded cap**, with no band or sleeve. Ramsey 1979 shows plain steel-tube posts in use on a quay in the period.
- **K5 matches LH_b's elevation**:
  - a round flange;
  - the fat lower bead;
  - the long shaft;
  - the upper bead and neck;
  - the flaring cap collar;
  - the dome.
  
  It has two pairs of lugs at the photographed heights, in the line of the posts.
- **K6's proportions are plausible.** The flange, barrel, waist and overhanging head (about 1.7 times the waist) sit within the range of Glasgow 2013 (waisted barrel, head about 1.5 times the waist, broad base plate) and Belfast 2019 (straight barrel, head about 1.25 times). The squat cast quay post in Hull 1982 has the same stance. Only the head's edges (fault 1) are wrong.
- **Colours are the right kind**: black paint on the irons, bare grey concrete on K3, bright steel only on K5's studs. There are no white, yellow or reflective bands, no lettering and no maker's marks on any kind.

## Photographs used

Geograph photographs are all CC BY-SA 2.0. Each date is the "Date Taken" read on the photograph's page on 11 October 2026.

| page | taken | licence | what it was used for |
|---|---|---|---|
| https://www.geograph.org.uk/photo/7461489 (Old Harbour, River Hull, Kingston upon Hull) | 6 June 1982 | CC BY-SA 2.0 | a squat cast-iron mooring post on a working quay edge, with a softly flared head (K6) |
| https://www.geograph.org.uk/photo/3452068 (Ramsey, East Quay, Isle of Man) | 29 July 1979 | CC BY-SA 2.0 | plain steel-tube posts with a sagging chain along a working quay (K4, K5 note) |
| https://www.geograph.org.uk/photo/1043161 (Killyleagh harbour, Co. Down) | 5 May 1990 | CC BY-SA 2.0 | a plain cylindrical mooring post on a stone quay (K6 context only; small in the frame) |
| https://www.geograph.org.uk/photo/6026508 (Mooring bollard, Belfast) | 14 January 2019 | CC BY-SA 2.0 | a mushroom head with a fully rounded rim and domed crown (K6, fault 1) |
| https://www.geograph.org.uk/photo/3463316 (Mooring bollard, Glasgow) | 26 April 2013 | CC BY-SA 2.0 | a waisted barrel, a thick round-edged head and a broad base plate (K6, fault 1) |
| https://www.geograph.org.uk/photo/3842932 (cast iron bollard, Hosier Street, Reading) | 11 December 2013 | CC BY-SA 2.0 | a cast street post: taper, rings, domed head (K1, K2) |
| https://www.geograph.org.uk/photo/4680721 (Public footpath, Kings Langley) | 26 September 2015 | CC BY-SA 2.0 | plain round concrete posts (K3) |
| the target's previews of Poly Haven urban_street_01 (US01_b), birbeck_street_underpass (BB_b), urban_street_02 (US02_a), limehouse (LH_b, elevation and foot close-up) | 2019 | CC0 | K1, K2 and K5's forms; K5's nut seat (narrow point 1) |

Geograph's feed returned no close photograph of a street bollard taken before 1995. The searches tried were "bollard", "bollards", "cast iron bollard", "cannon bollard", "concrete bollard(s)", "steel bollards", "bollards street", "bollards quay/harbour/dock" and year words, two to three pages each. The period evidence above is therefore harbour views with bollards in them. Wikimedia Commons was not queried, for lack of time.
