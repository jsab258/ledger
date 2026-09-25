# The flat cap, 25 September: the first garment on the free route

FreeSewing's Florent flat cap (MIT), drafted for a 57 cm head, sewn and
draped in Blender, and worn in the street by Ron (candidate C5, only to show
it). The sitting's third item, with the hours recorded because the research's
estimate (8 to 20 hours for a first simple garment) was a guess.

| Step | Minutes | How |
|---|---|---|
| Pattern drafted; its pieces cut flat as cloth | 35 | tools/meshgen/freesewing_draft.mjs, tools/meshgen/blender/pattern_panels.py |
| Sewn and draped on a head of the same girth | 20 | tools/meshgen/blender/sew_cap.py, six runs |
| Into Unreal with its own wool; on Ron's head in the street | 15 | tools/ue/import_cap.py; the portrait tool's -PortraitHat |
| **Total** | **about 70** | my working time, not a person's by hand |

What went wrong on the way, each fixed: with gravity from the start the cap
slid off the head; strong seams balled the cloth; the band rode up until the
head opening was held on the hat line, as a cap's band sits once it is on;
the brim's outline was traced backwards and crossed itself; neighbouring
pieces faced opposite ways, which showed as ragged seams; Unreal kept an old
material, so the cap came in pale.

Not finished:
- It is rounder than a true flat cap: the crown stands up rather than lying
  forward over the brim.
- Plain dark wool, with no tweed weave and no stitching.
- It was draped on an egg-shaped head, not the wearer's, and is set on each
  head by hand (Ron C5: -HatAt=1.5,9 -HatTilt=7).

The cap's Blender file and FBX are on drive F (F:\LedgerTools\freesewing\cap\sew)
and are made again by the scripts. sewing-report.json has the seam gaps by
frame and the cap's size.
