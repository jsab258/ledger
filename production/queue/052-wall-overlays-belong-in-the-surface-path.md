line: infrastructure (asset routing)
spec: this file, ordered by the 3 September ruling decision A
acceptance: wall_soot_brick and wall_salt_render are resolved through AssetLibrary as SURFACES rather than stamped as decals; the decal path no longer names them; a frame shows them tiling across a wall rather than as a patch of different masonry
max_sessions: 1
status: CLOSED 2026-09-10, not on the ladder, BY COMMIT cd55a79c (subject: D18 lands at five sites, 510 files are archived and nothing is deleted). No ruling named this closure; see production/queue/275. Reviewed 2026-09-14 against production/stages.md and not reopened. and untouched for 7 days 2026-09-03. engine-specialist, small.

## The finding

Opened by the queue 046 builder rather than inferred: both files are
full-frame 1024x1024 TILING SURFACES, not stamps. Applying one as a decal
puts a rectangle of different-looking brick onto a brick wall, which reads as
damage rather than as material. They belong where every other tiling texture
goes.

`wall_soot_brick` also carries a garbled painted mark on one brick, noted
here so the next reader does not rediscover it: that is a generation fault
and is not fixed by moving the file to a different code path.
