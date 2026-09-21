# The clip sheet beside this file is STALE as of 2026-09-21

STATUS: LIVE, verified 2026-09-21, the day the library changed under it. This
file is DELETED, not updated, by the sim run that regenerates the pair; if it
is still here, the pair beside it still misdescribes the library.

`clips.tsv` and `clips.jpg` in this directory were written by a sim run on
2026-09-03 (commit 28a2d6e1) and they DESCRIBE A LIBRARY THAT NO LONGER
EXISTS. Commit cbadeeb3 removed two clips under D17 and renamed a third:

  row 2 col 0   `drink`         the clip is DELETED, the slot is DELETED
  row 10 col 2  `work_counter`  the clip is DELETED, the slot survives empty
  `sit_drink`                   renamed to `sit_wait`

So the JPG renders two tiles for animations that are not in the tree, and the
TSV names three slots that no longer read the way it says.

WHY NEITHER FILE WAS EDITED AND NEITHER WAS DELETED. They are a MATCHED PAIR
written together by the instrument, not inputs: `ClipSheet.cs:465` writes the
TSV from the file names at runtime and `tools/sim-shots-commit.sh:71-72` copies
the pair into the tree together. Hand-editing the TSV would relabel tiles in
the JPG beside it, which is the silent-instrument failure this project's own
rules exist to stop. Deleting the pair would throw away evidence of a real run.

HOW IT IS FIXED: a sim run that regenerates both, staged with `clips=1`, which
is the fifth positional argument to `tools/sim-shots-stage.sh` (line 177, read
2026-09-21). That is the UNITY pipeline and NOT the ue-probe dispatch; the
resident first assumed the two could ride one dispatch and that was wrong.

Until then this marker is the correction: the pair is evidence of what the
library held on 2026-09-03 and is not a reading of what it holds now.
