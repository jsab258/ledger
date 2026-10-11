PASS

# Unit 3.3, guard rail panel A1, v1: fresh review of the CLOSE view (cloud week 42, 11 October 2026)

Render judged: `scratchpad/kit-railings/render/close.png` (preview `production/previews/cloud-week/railings/railings-close-v1-2026-10-11.jpg`). Camera at (-2.5, -1.3, 1.05) on a 32 mm lens, about 2.0 m from the left post, outside its outer end on the footway side. The whole panel is in frame. The left post is about 40 px wide and each nut about 12 px across, so the close detail was judged from 4x to 6x enlargements of the post head, the post foot and the right post head, and from the built mesh (`build/guard_rail_A1.npz`), measured in millimetres. Tone is ignored, as the brief says.

## Faults

None. At this distance nothing would read as wrong to a player. There is no wrong proportion or profile, no missing part, no modern form, and no hole, gap, overlap, floating part or faceting.

## Narrow points (for the builder; none fails the piece)

1. **The top rail is wider than the post it is bolted to (the target's; not settled).** The post is RHS 50 x 30 with its 30 across the run. The top rail is laid flat at 50 across, and the bottom rail at 40. So at every joint the rail and its 6 mm end plate stand 10 mm proud of the post's footway and road faces (5 mm for the bottom rail).
   - Where in the view: beside the left post at top-rail height a thin strip of end plate shows past the post's edge, and at the right post the rail end overhangs the post's near edge.
   - The photographs: Pinner (2016) and Snaith (2014) look as if the post is at least as deep as the rail, but at their size this cannot be measured.
   - The fix, only if the PC photographs (target section 13) show it: make the post and cap RHS 50 x 50 x 3 (R4.5, y ±25). The box (2072 x 50 x 1030), the bar gaps (96.24 and 97.09), the studs and the nuts all stay unchanged.
2. **A groove at the post/cap joint (the build's).** The post's top edge is chamfered 1 mm (z 1026 to 1027) and so is the cap's lower edge (z 1027 to 1028). That leaves a 1 mm V-groove round the post under the cap. The target says the bead is "ground flush", with only the cap's edges broken R1. The groove is under a pixel here, so this is a note only.
   - The fix (`build_railings.py`, post and cap): no bevel on the post's top edge or the cap's bottom edge, keeping R1 only on the cap's upper edge, so the side faces run flush from post into cap.
3. **No washer under the nut (the target's; optional).** Both photographs show a small bright round fixing on the post face. At their size a domed head cannot be told from a nut on a washer.
   - The fix, if the PC photographs show washers: an M10 washer 21 OD x 2 at x ±1025 to ±1027, with the nut moving out 2 mm. Then either lengthen the stud to ±1038 (box 2076, and update A1_bbox) or keep the stud at ±1036 with 1 mm of thread beyond the nut.
4. **The view itself (the render, not the piece).** The camera is at about 2.0 m, not 1.5 m, and the nuts and rail ends are only 12 to 20 px. For v2 the close camera could go to about (-2.0, -0.9, 1.15) looking at (-1.0, 0, 0.65) on the same 32 mm lens: about 1.35 m away, the post filling the frame height and each nut about 18 px.

## What is right (checked against the photographs and the target)

- **The cap stands proud of the top rail.** The post's top is at 1030 under a flat cap plate flush with the post's sides, 30 above the rail top at 1000. All three photographs show the same: a post top standing a little proud of a flat top rail, with a flat top and no knob or finial.
- **The fixings.** Each post has one fixing at each rail height, on the face across the run (the outer face here), small and brighter than the post. Pinner shows two bright round fixings on a post face, at about the top-rail and bottom-rail heights. Snaith shows round heads at both heights on the post face toward a camera looking along the run. The build's bare-zinc hex nuts (17 AF x 8, 3 mm of thread, faces at x ±1025 to ±1033, on the rail axes z 985 and 200) read the same way at this distance.
- **The sections and edges.**
  - Posts: rounded rectangle with R4.5 corners.
  - Top rail: RHS laid flat, its top face broad and level.
  - Bottom rail: low and laid flat.
  - All three read in the render as softened steel edges, not sharp boxes and not tubes. Snaith's galvanised panel is this family: rectangular posts, a broad flat top rail, and a low flat bottom rail the bars stand on.
- **How the bars meet the rails.** The 12 mm round plain bars stand square on the bottom rail's top face (z 210) and stop under the top rail (970), each with a 2 mm weld ring that flares from r 6 to r 8. The ring shows at the bar feet in the enlargement. Snaith's bottom-rail close shows bars standing on the flat bottom rail with small welds in the same way. The bars read round, with no faceting visible.
- **Rail ends.** Closed by 6 mm end plates of the rail's own outline, so no open tube ends show. The rails reach the plates (about 0.3 mm overlap) and the bars sink 0.5 mm into the rails. Nothing floats and nothing gaps.
- **The post foot.** The post goes straight to the ground with no base plate or collar, as the posts in Pinner and Snaith go straight into the footway. The tarmac patches are a separate mesh and are not loaded in this render.
- **The numbers, measured in the built mesh, match the target's 6.1.**
  - Post x -1025 to -975, y ±15, z 0 to 1027, cap 1027 to 1030.
  - Top rail top 1000, underside 970, y ±25.
  - Bottom rail 190 to 210, y ±20.
  - Stud r 5 from x -1036 to -974.
  - Bars 209.5 to 970.5.

## Photographs used (Geograph, all CC BY-SA 2.0; full-size pages opened, downloads in the session scratchpad `rail-review-close/`)

1. **Snaith, A645, galvanised pedestrian guard rail.** https://www.geograph.org.uk/photo/4231072. "Pedestrian barrier alongside the A645 Snaith", © Steve Fareham, taken 1 November 2014, CC BY-SA 2.0. Original 768 x 1024. The nearest posts, their tops, their bolt heads at both rail heights and the bars on the bottom rail were enlarged.
2. **Pinner, black pedestrian guard rail.** https://www.geograph.org.uk/photo/4856523. "Junction of High Street and Bridge Street, Pinner", © Christine Johnstone, taken 8 March 2016, CC BY-SA 2.0. Original 1024 x 768. The two nearest posts were enlarged: cap proud of the top rail, two bright round fixings per post face, post straight into the paving.
3. **Ulverston, galvanised guard rail at a junction.** https://www.geograph.org.uk/photo/6757620. "Prince's Street, Ulverston", © Adrian Taylor, taken 10 June 2018, CC BY-SA 2.0. Used at street distance for the posts standing proud of the top rail and the low bottom rail.

**Dates.** No photograph dated 1975 to 1995 that shows a guard rail close was found in the time.
- Two period street photographs (1982 and 1983) did show guard rail at a distance, but both are excluded under the content rule.
- Wikimedia Commons answered 429 to most requests. The one search that got through returned no guard rail.
- The three photographs used are from 2014 to 2018, of the same long-lived RHS galvanised (or painted) pattern. The PC photographs the target asks for in section 13 should still settle the post's depth and the fixing type (narrow points 1 and 3).
