# NOW

Where the game stands, 2026-09-22. The simulation is real and tested: perception,
memory and gossip run in the C# Core against its own test suite, the C++ port
still matches the C# golden table, and a fake-player harness plays it through
on every push. The town exists as plans, specs and canon rather than as
geometry you can walk: Meridian's streets, Mickey's minicab office and the
interiors are decided and drawn but not built. What is actually standing is the
vignette scene, a small authored street corner used to judge the look, and the
visual bar for it is the Hook sheet. Speech, barks and the voice cast are
sourced and staged. The engine is Unreal, and the Unreal probe builds on the
runner. Nothing in the game is blocked on a decision: everything below is work.

## The next visible outcomes

THESE TWO ARE THE STUDIO'S READING AND NOT HIS WORDS. His order said "the two
outcomes named below" and then did not name them, so these are the two that
were in flight when it arrived. One line from him replaces either.

1. THE LIGHTING COLUMN, FINISHED. A British swan-neck column with a sodium
   lantern, standing in the vignette scene with its grime, accepted against the
   Hook sheet by eye.
2. THE FIRST TERRACE FRONT, STANDING. One authored Meridian facade on the
   street, with its wear as a separable layer, judged in a rendered frame.

## Where the lamp was left

FOUR ATTEMPTS, THE FOURTH RENDERED AND NOT ACCEPTED, and the blocker is the
reference rather than the recipe. `tools/art-recipes/lighting-column.py` builds
the whole column from `production/specs/vignette-scene.json`: base, shaft, a
neck of a 0.14 m corner then a 0.36 m level arm then a 0.24 m dropper, lantern,
photocell, and three grime panels. Attempt 4 ran clean and its frames are on
`art/atlas-01` at 6f77ff59. It was authored to hit an aspect of 2.27 traced off
the Hook sheet, and THAT NUMBER WILL NOT HOLD STILL: the sheet's lamp is 25
pixels wide on a 4-pixel pole, and three traces of the same crop give 2.27,
3.0 and 3.3 depending where the threshold falls. What the sheet does settle,
and this survives any threshold, is that its lamp encloses no sky in 39 traced
rows: it is a KINK at the top of the pole with the lantern hanging off it,
never an arch with a bare arm and a dropper under it. Both renders are arches.
Normalised by the one length both images pin, canon's 0.114 m shaft, the sheet
is 6.0 pole-diameters wide and 2.0 tall against attempt 4's 6.80 and 2.98.
FINISH IT FROM THE WRITTEN DIMENSIONS: drop the sheet-derived target and its
tolerance from the recipe, build the neck as a kink with the lantern hanging
directly off it, render it here in Blender, and look. The measurements are in
`legacy/studio-v2/production/throughput.md` under batch b006 and the reference
problem is `legacy/studio-v2/production/queue/421-*`.

## Where the facade was left

NOT STARTED, DELIBERATELY. The spec is written and clean:
`production/specs/terrace-fronts.md`, 644 lines, passing the canon gate. Its
two preconditions landed. Under the ruling of 2026-09-21 the fronts are
AUTHORED in Blender from the atlas plans rather than bought, because no free
British terrace kit exists on Fab; under the grime ruling the wear is a
separable layer and the facade is the first point in that series, so its
coverage is measured and the floor is not invented; and under the sheet ruling
the brief names the concept sheet and the research that govern it, with
`game-design/research/GOVERNS.md` as the index that makes that possible. It was
not begun because beginning it would have answered a card that was Jafar's.
