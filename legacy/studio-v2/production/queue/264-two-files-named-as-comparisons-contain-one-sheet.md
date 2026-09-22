# 264: a deliberate content removal left the filenames advertising what was removed

STATUS: READY
OPENED: 2026-09-12

## What actually happened, after two wrong readings of my own

On 2026-09-10, queue 242 CROPPED the outside half out of both Fairview
comparison sheets, deliberately and carefully, to comply with D18's no-children
rule. The outside sheet carries figures reading as children in school uniform in
both of its views, a legible FAIRVIEW SCHOOL nameplate on the gate post, and a
material swatch captioned SCHOOL SATCHEL. The crop measured the gutter rather
than guessing the midline, and both results were opened afterwards:

    fairview_theirs_vs_ours.jpg           gutter=614..623   midline=621  offBy=-7
    fairview_theirs_vs_ours_finished.jpg  gutter=1016..1029 midline=993  offBy=+23
    cropped .../fairview_theirs_vs_ours.jpg           before=1242x962  after=628x962
    cropped .../fairview_theirs_vs_ours_finished.jpg  before=1987x1568 after=971x1568

That work was right and is not what this item is about. The originals are kept
in history, and the pre-crop blob is named in queue 242.

WHAT WAS LEFT UNDONE IS THE NAME. Both files still say `theirs_vs_ours`, and
both now contain only ours. Nothing on the file, and nothing in the D18 ruling
record that describes them, says the outside half was removed or why.

## Why that is not cosmetic, measured on a real incident today

Writing the 2026-09-12 brief, the order said to carry our Fairview sheet beside
theirs. The composite was built from the cropped file, so the picture showed one
sheet under a caption promising a comparison. Opening it caught that, per rule 4.

THEN THE FIX MADE IT WORSE. Reading the filename as simply wrong, I fetched the
outside sheet back off `origin/art/atlas-01`, rebuilt the pair, opened it,
confirmed two labelled halves, and stacked it into a message bound for Jafar's
phone. That picture contained the children and the school nameplate that queue
242 had removed two days earlier. It was caught only by going back to read WHY
the half was missing, which was one grep away the whole time and which I did
after building, not before.

So the naming did not merely mislead a reader. It made a deliberate content
removal look like an error worth reverting, and a later session reverted it.
The brief now carries our sheet alone; the rebuilt pair is off disk.

## Done looks like

1. Neither file keeps a name asserting a comparison that was deliberately taken
   out of it. 8 references name the string across the tree, `tools/content-gate.py`
   among them, whose enforceable text names the finished copy; they move with it.
2. The reason travels with the artifact. Whatever carries the name carries, in
   one line a stranger will read before acting, that the outside half was
   removed under D18 and must not be restored. A removal that does not say it
   was a removal is an invitation.
3. `game-design/decision-2026-09-10-ruling-the-d18-cleanup-close-out.md`
   describes these files in their PRE-CROP state, as pairs with a left half and
   a right half, and that description was accurate when written. It is corrected
   in place, saying what changed and when, rather than being edited out.

## What this item does not claim

That the ruling was wrong to describe halves. It was not; the halves existed
when it looked. I asserted otherwise in the first version of this item, on
aspect-ratio arithmetic and one image read, before finding the crop record. The
arithmetic was right about the files and wrong about the cause.
