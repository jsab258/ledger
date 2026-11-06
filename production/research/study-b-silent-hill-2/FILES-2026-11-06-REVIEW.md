# Review of FILES-2026-11-06.md, 6 November 2026

| Claim | Verdict | Why |
|---|---|---|
| Unencrypted; engine 5.1; PSOVersion | holds | Headers re-read (flags 9, pak flag 0); "++UE5+Release-5.1" in the exe, UTF-16. |
| Pipeline cache "not reached" | fails | Loose file ships: Content/PipelineCaches/Windows/SHProto_PCD3D_SM6.recorded.upipelinecache, 5,409,774 bytes. |
| One mesh per character, clothes inside | fails | Headers give classes, not geometry. Inference marked "measured". |
| "Each hero" mesh; "no cloth" list | fails | 130 packages is a selection, rule unstated (James alone: 169 texture packages). |
| Simulated cloth on hems, skirts | unsure | Assets exist; garment covered and in-game use unread. |
| Nurse skirt link | holds | Marked inference; weak. |
| Texture byte sums | holds | Marked estimate; 22,364,160, 5,586,944, 2,793,472, 1,392,640 reproduce. |
| "Full mip chain" | fails | Sums stop at 128; a full chain is 22,369,621. |
| "2048 doubled" | fails | Same rule gives 11,173,888. 4096x2048 fits exactly, unlisted. |
| Bulk totals are textures | unsure | Other assets may hold bulk. |
| Question 5 "Answered" | fails | Hair, skeleton, facial rig unanswered, absent from "Not reached"; likewise Nanite use, draw distances. |
| HZB sentence | fails | Names Epic, then excludes it. |
| Virtual shadows off; all lighting dynamic | unsure | Preset overrides unchecked; gloss unmarked. |
| Unread list claims nothing | holds | Except rows above. |
| No mappings on this PC | unsure | None in the game or F:\LedgerTools; elsewhere unsearched. |

## Could not be checked

list-sh2.tsv, the config copies and class lists are deleted; the .ini files sit inside the pak, closed by the brief. So file counts, sizes, config values, cloth, morph and body counts have no surviving source. The tool logs an unreadable export as "ERR", so "none failed" may not cover exports. The Mafia mappings trial left no record.
