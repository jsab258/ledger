# Measurement sitting: three terrace facades, end to end in Unreal

PREPARED 23-24 September, overnight; NOT STARTED. Jafar starts it himself with
a meter reading at each end. His order: "three terrace facades ready to build
end to end in Unreal, from dimensioned drawing to accepted pair, and nothing
else."

## What it measures

What ONE facade costs, taken from a dimensioned drawing to an accepted pair in
Unreal, done three times so the number can be multiplied across the town. The
meter gives the whole sitting; the log at the bottom gives each facade's start
and finish, so the three can be told apart.

## Scope: these three and nothing else

| order | block | what it is | why this order |
| --- | --- | --- | --- |
| 1 | `east_parade` | six shops, Mickey's is the first, pitched slate roof, red brick | Jafar's standing order reworks the shopfronts "starting with the parade", and it is the one on the Hook frame |
| 2 | `west_north` | three shops, parapet, grey brick | the parade's shopfront work carries over, so it measures the second-facade cost |
| 3 | `west_south` | three plain fronts, parapet, grey brick | the cheapest; if time runs out, it is the one to lose |

NOT IN SCOPE, and a finding about any of them goes in FINDINGS.md and waits:
the corner, the slice, the simulation, voices, the MetaHuman, the checklist,
any other building. The Hook viewpoint frame is not re-judged either; this
sitting judges each facade against its own drawing.

## THE DRAWINGS DO NOT EXIST YET, and that is step one

There are no dimensioned drawings of these facades anywhere. The pictures
named `terrace-front-*-elevation.png` are old Blender renders, not drawings.
The geometry lives as NUMBERS in `production/specs/vignette-scene.json`
(`blocks`, `shopfront`, `facade`, `roofline`), each tagged with where it came
from. Where those numbers and the photographs disagree, the photographs win
(Jafar 2026-09-22), and the audit has already found where they do: the timber-only
shopfronts are NOT citable; metal shopfronts, fluorescent strips and patterned
tile stallrisers ARE (photographs R05 and R09 in
`production/reference/photographs.md`).

## Each facade, seven steps, each ending in a file

1. **Draw.** A dimensioned front elevation, orthographic, in metres, from the
   spec's numbers corrected by the photographs. Every dimension says where it
   came from (a spec key or a photograph). Output: the drawing, as SVG and PNG.
2. **Write back.** Any number the drawing changes goes back into
   `vignette-scene.json`, so the recipe builds what the drawing says and not
   the other way round.
3. **Build.** `tools/art-recipes/terrace-front.py --export-glb` writes the
   street's geometry, the only place Blender crosses into Unreal.
4. **Into Unreal.** One push; the runner's probe imports the geometry
   (`tools/ue/import_street.py`), builds and renders. Two Unreal builds never
   overlap; a Blender render needs no wait.
5. **Frame.** The block's elevation in Unreal: orthographic, overcast day,
   square to the frontage, the other side of the street hidden.
6. **Pair.** The Unreal frame beside the drawing at the same scale, the
   drawing's dimension lines laid over the frame.
7. **Accept.** Every drawn dimension within 5 cm on the pair, measured, not
   eyeballed; the look against the sheet's palette and the photographs. The
   standing rule applies: two attempts against the reference, then finished
   from dimensions or set aside with a note. An accepted pair is committed
   with its frame.

## Ready, and not ready

Ready tonight: the spec's numbers, the photographs page and its audit, the
recipe's export, the Unreal import, the probe's run on push, and the pair tool
for the Hook sheet.

NOT ready, and all three are fixed costs rather than per-facade ones, so the
recommendation in FOR-JAFAR.md is to build them before the meter starts:

- [x] a tool that turns the spec's numbers into a dimensioned elevation drawing:
      `python tools/facade-drawing.py --block <block> --out <dir>` draws the
      recipe's own plan of the spec, as seen from the street, in millimetres
      (built 24 Sep; the three drawings came out of it on the first night).
- [x] an orthographic elevation shot per bay in the Unreal probe:
      `production/specs/facade-shots.json`, twelve shots, one per bay, 100 px
      a metre (91 since 24 Sep 04:00, width 14 m, centre 3.8 m, so the parapet's
      top is in frame), people and cars hidden. PROVEN 24 Sep: the probe run for
      4b72442c made all twelve (`production/d1-probe/ue-facade_*.png`).
      The lamp posts on the pavement still stand in front of some bays.
- [x] the pair: `python tools/facade-pair.py --block <block> --bay <i> --frame
      <frame> --width-m 14.0 --centre-z-m 3.80 --out <pair>` puts the drawing
      over the frame and measures every drawn edge on it in millimetres,
      50 mm or under to pass (built 24 Sep; its self-test pairs a drawing with
      itself and catches a 120 mm shift).

## The tools, tried once before the meter (24 Sep, just after midnight)

The pair was run on Mickey's bay as it stands tonight, only to prove the
tools. Nothing was changed on the facade. 17 of the 19 edges it could find
were within 5 cm, most within 1 cm. The two that were not are the transom bar
and its toplight rail: the strip lights behind the glass are the nearest strong
edge, and by eye the bar lines up. So an edge the pair marks red is LOOKED AT
on the pair before it is called wrong. Two things were fixed on the way: the
footway's 0.1 m above the road, which put every level about 100 mm out; and
taking the nearest strong edge rather than the strongest, since a sill has two
edges 75 mm apart.

TRIED ON THE OTHER TWO THE SAME NIGHT, bay 0 each, as they stand: west_north
17 of 18 edges found within 5 cm (worst 83 mm), west_south 16 of 16. The
parapet's top (7.10 and 7.175 m) falls at the frame's upper edge with the
shot centred at 3.55 m and is not found; for the parapet rows, raise the
shots' eye_height_m to about 3.9 in production/specs/facade-shots.json
(a spec change, one probe run) if the parapet is to be measured.
DONE THE SAME NIGHT, 04:00: every shot is now 14 m wide centred at 3.8 m
(0bf8a128), and on bay 0 of each, as it stands, the pair finds every
edge but one: east_parade 17 of 20 found within 5 cm, west_north 19 of 21,
west_south 19 of 19, the parapet's coping and the pavement line included.

## Log (filled in during the sitting)

| facade | started | drawing | in Unreal | accepted pair | finished | attempts |
| --- | --- | --- | --- | --- | --- | --- |
| east_parade | 09:41 | 09:42, from the spec, nothing written back | no rebuild: geometry unchanged since 01:38, frames from this morning's probe run (703b0688) | 09:46, attempt 1, six bays | 09:47 | 1 attempt, 0 rejected |
| west_north | 09:47 | 09:47, from the spec; redrawn 09:49 the right way round | no rebuild: frames from this morning's probe run | 09:50, attempt 2, three bays | 09:50 | 2 attempts, 1 rejected |
| west_south | 09:50 | 09:50, from the spec, nothing written back | no rebuild: frames from this morning's probe run | 09:51, attempt 1, three bays | 09:51 | 1 attempt, 0 rejected |

### east_parade, accepted 09:46

Six bays paired (production/art/facades/2026-09-24-measured/east_parade-bay*-pair.png).
Every edge the frames show is within 5 cm except these, each looked at on the
pair: the fascia's top on four bays (maroon on red brick is faint; the search
took the brick course or the sign's tile grout, and by eye the line sits on the
join); Mickey's transom (dark slate on dark glass; the search took the strip
lights behind, as on the first night); and one upright on bay 4 (white jamb on a
cream pier; the search took the post box in front). NOT MEASURED: the ridge at
9.0 m, above the top of every bay frame. Two faults in the pair tool were fixed
on the way, both measurement, not facade: levels only Mickey's has (the 0.12 m
tile course) were being measured on every bay, and an edge found at another
drawn edge (the sill rail's top, 80 mm above an invisible stallriser top) was
reported as the first edge being out.

### west_north, accepted 09:50 on the second attempt

ATTEMPT 1 REJECTED, 09:47: the middle bay's side door was at the other end of
the bay in Unreal. The building was right and the DRAWING was mirrored: the
west blocks are turned a half turn as they land, so seen from the street they
run right to left like the parade, and the drawing mirrored the east side only.
The two end bays had passed only because each is the other's mirror image, and
the camera numbered bay 0 along the street looks at the block's bay 2. Fixed in
the tools: the drawing runs right to left on both sides, and the pair names the
shot that stands in front of each west bay (bay i before shot bays-1-i).
ATTEMPT 2 ACCEPTED: the middle bay 22 of 22 edges within 5 cm (worst 31 mm);
the end bays every edge found within 5 cm but the end pier (74 mm, the brick
return behind it) and two pairs of edges 36 mm apart (the pier's inside and the
door frame) the tool cannot tell apart, each within 5 cm by eye. Pairs:
production/art/facades/2026-09-24-measured/west_north-bay*-pair.png.

### west_south, accepted 09:51 on the first attempt

Every edge found on all three bays, all within 5 cm (worst 46 mm), and by eye
every door and window where the drawing puts it, the right way round. Pairs:
production/art/facades/2026-09-24-measured/west_south-bay*-pair.png.

### What this sitting measured, and what it did not

All three facades were already built to the spec in earlier sittings, and
nothing on any of them needed to change, so no geometry was rebuilt and no
Unreal build was run: each was drawn, paired on this morning's probe frames,
measured and accepted. The sitting measured the drawing-to-accepted-pair half
of a facade, including two fixes to the pair tool and one to the drawing
(the west side ran the wrong way round), and NOT the building of a facade from
nothing.
