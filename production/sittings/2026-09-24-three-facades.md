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
- [ ] an orthographic elevation shot per bay in the Unreal probe:
      `production/specs/facade-shots.json`, twelve shots, one per bay, 100 px
      a metre, people and cars hidden. Written 24 Sep; proven only when a
      probe run has made the twelve frames.
- [x] the pair: `python tools/facade-pair.py --block <block> --bay <i> --frame
      <frame> --width-m 12.8 --centre-z-m 3.55 --out <pair>` puts the drawing
      over the frame and measures every drawn edge on it in millimetres,
      50 mm or under to pass (built 24 Sep; its self-test pairs a drawing with
      itself and catches a 120 mm shift).

## Log (filled in during the sitting)

| facade | started | drawing | in Unreal | accepted pair | finished | attempts |
| --- | --- | --- | --- | --- | --- | --- |
| east_parade | | | | | | |
| west_north | | | | | | |
| west_south | | | | | | |
