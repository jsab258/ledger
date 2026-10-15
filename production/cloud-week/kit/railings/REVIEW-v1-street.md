PASS

# Guard rail panel A1 (kit piece 3.3), v1: fresh review of the STREET view

Cloud week 42, 11 October 2026. One view judged: `street.png` (1600 x 1200, camera 6.5 m out on the footway side, eye 1.6 m; the panel is about 380 px wide in the frame). Judged against the target (TARGET.md, target.json, kind A1), the builder's notes, and three dated photographs found on Geograph today (two from 1985 and 1988, one from 2016 for close detail; no third period photograph was both legible and clear of the content rule in the time). Form, proportion and construction only; the dark tone of the steel is the render's sky and ground, not judged.

## Faults

None at this view's distance.

## Narrow points (for the builder or the render step; none would be seen as wrong from the street)

1. **The two tarmac patches are not in this render, so this view could not judge them.** `render_railings.py` loads only `guard_rail_A1.glb`; the separate patch mesh is left out, so the posts stand on bare grey ground. At 6.5 m the two dark patches would be the darkest marks in the picture. Not a fault of the panel. Fix: re-render the street view with `guard_rail_A1_ground_patch.glb` loaded beside the panel, and check the two patches by eye (about 250 x 250 at each post foot, one straight flag edge on the footway side, flush with the ground).
2. **Post stubs above the top rail.** The target's 30 mm is at the low end of what the photographs show. Stockton (1988) shows short stubs. Pinner (2016) shows about 60 to 80 mm on a modern panel. At this distance the 30 mm reads correctly as "the post stands a little proud". No change needed; if the close view finds the stub too timid, 50 mm (z 1050) is inside both photographs.

## What is right

- **The kind of object is right for Britain in 1985 to 1990.** Every period photograph found shows a galvanised-grey pedestrian guard rail with a flat top rail at about hip height (about 1.0 m), close-set vertical bars, a bottom rail low over the footway, and square or rectangular posts at the panel joints, standing to or a little above the top rail. The render shows the same: two rectangular posts with capped tops just proud of the rail, a flat top rail, a bottom rail at about 200, and 17 evenly spaced bars between them.
- **The target's judgement on form is supported, not contradicted.** No photograph shows round tube posts or saddle-welded round rails, so the recorded round-tube alternative stays set aside. No photograph shows a different infill: no mesh, no "visibility" stagger, no hoops. Stockton 1988, the nearest period view, shows a top rail whose flat face is at least as wide as the posts. That matches A1's 50 mm top rail laid flat across 30 mm posts.
- **Proportions read correctly.** The panel is about twice as long as it is high (2000 between post axes, 1030 to the post tops). The bars stop on the bottom rail's top and under the top rail's underside, with no gaps or overlaps visible. Bar spacing is about one bar to a hand's width (109 pitch, 97 clear), as close-set as the period photographs, where the bars cannot be counted.
- **The fixings show where they should.** On the right post's outer face, the two nuts read as small bright knobs at the top-rail and bottom-rail heights. On the left post they show as tiny ticks on the outer silhouette. Pinner (2016) shows bolt heads on the posts at the same two heights. In the 1985 to 1988 photographs the fixings are a pixel or less, so they cannot confirm or deny them.
- **No build faults are visible.** Nothing floats or leaks light, no faces overlap at the rail-to-post joints, the post feet meet the ground with a contact shadow, and the 12-sided bars read round at this distance. The builder's 28 of 28 automatic checks agree (bounding box 2072 x 50 x 1030; posts and caps to 1030).
- **Nothing modern shows.** No reflective bands, no sleeves, no plates or lettering.

## Photographs used (Geograph Britain and Ireland, all CC BY-SA 2.0, read 11 October 2026)

| # | page | taken | author | what it shows for this review |
| --- | --- | --- | --- | --- |
| 1 | https://www.geograph.org.uk/photo/2919102 ("Bus wars in Stockton High Street (1988)") | 15 February 1988 | Graham Hogg | The closest period view (1024 px). A long galvanised guard rail along the edge of a raised verge beside the bus lane, in the left foreground. It has a broad flat top rail, close vertical bars, and short square post stubs just above the top rail at each joint. About 1 m high, dull zinc grey. |
| 2 | https://www.geograph.org.uk/photo/1710281 ("Somerset Road, Ashford in 1985") | 25 May 1985 | John Baker | Seen from a multi-storey car park: kerbside guard rails at a signal-controlled pedestrian crossing (800 px). The panels are galvanised, with a top rail, a low bottom rail and vertical bars between posts at the joints. Short runs end at a post, like the street's single panel. |
| 3 | https://www.geograph.org.uk/photo/4856523 ("Junction of High Street and Bridge Street, Pinner") | 8 March 2016 (**not period**) | Christine Johnstone | A close modern panel, painted black, of the same construction as A1. Rectangular posts stand about 60 to 80 mm above a flat top rail, with round bars about a hand's width apart and a bottom rail clear of the paving. Bolts show through the posts at the two rail heights. It is used only for the detail that the period photographs cannot resolve. |

Looked at and not used: other Geograph street views of 1985 to 1990 in London, Coventry and Manchester. Their guard rails were too small to read, or the photograph was set aside under the project's content rule. Wikimedia Commons answered only after a rate-limit wait. Its category "Guardrails in the United Kingdom" holds road vehicle barriers, not pedestrian guard rails, so nothing was taken from it. Downloads are in the session scratchpad (`rail-review-street/`), for review only, not for the game.
