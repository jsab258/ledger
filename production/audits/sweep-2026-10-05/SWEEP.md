# The sweep: everything that exists, and where it stands

Phase 0, item 0.3, 5 October 2026 (PLAN.md; his edit 9). Every branch on GitHub, the project folders on his drives, the approval pages' stored answers and the two old repositories, each marked: already in main, holding work that exists nowhere else (kept, or brought in), or archivable. Measured by tools/branch_sweep.py (branches.json beside this file, with every file named) and by hashing files against every branch; page answers by tools/page_answers.py.

## 1. Branches on GitHub (70)

| Group | Branches | What they hold | Done or proposed |
|---|---|---|---|
| Already in main | 22 | Every commit in main, or every file in main byte for byte (11 merged, 11 squashed or copied) | Archivable: nothing to bring in |
| Research reports found only on their branches | 41 `research/*` | 46 files: the full research deliveries of 14 to 23 September (DELIVERY.md, the coverage audit's CROSS-CUTTING.md, the egress allowlist's probe and census). Main kept only each topic's SUMMARY.md; the full reports, with their sources and claim labels, existed nowhere else. Each file had one version across all branches | **Copied in** beside their summaries, 886 KB of text, reaching main with phase 0's review (decided: research, not taste). Then archivable |
| Older than main | 5: claude/ui-design, town, pc-results, pc-inbox, research/local-models | Main has later versions of everything but old probe outputs (an encounter sound, 19 superseded surface pictures and job results of 11 September, one refused outbound note) | Archivable |
| Taste and identity | 1: art/atlas-01 | The September atlas of Meridian (22 September): the town's map with its seven districts, routes, a Hook street plan, seven AI concept sheets, a town form bible, district plans, 100 previews, research references with their rights noted. Its Mickey's is designed as a pub (hand pumps, beer, a darts poster): against the content rule and his ruling that Mickey's is the cab office | **To him on one page** before anything merges (the page of 5 October) |
| Active | 1: wip | Today's unfinished work | Kept |

"Archivable" means: kept as a tag (archive/<name>), the branch itself removed, nothing lost and any branch restorable from its tag; asked on his page because it changes his GitHub.

## 2. The two old repositories

- **jsab258/game-studio** (frozen 1 September, "harvest-only"): 34 files of the retired agent studio (agents, hooks, skills, templates). None is game content; main's legacy/studio-v2 holds their descendants. Archivable; nothing to bring in.
- **jsab258/wc26-picks** (the project's home before this repository): six branches. Of their 14,428 files all but 80 are in this repository byte for byte; the 80 are superseded: old workflows of July, old job results of 6 September and an older copy of the atlas (9 September, superseded by art/atlas-01). Its branch claude/btc-sentiment-price-tracker is his own unrelated project and was not opened. Archivable; nothing still needed.

## 3. Project folders on his drives

| Folder | Size | Holds | Stands |
|---|---|---|---|
| C:\Users\Jafar\ledger-local | | this repository, main | in use |
| C:\Users\Jafar\ledger-town, ledger-clothes | | worktrees of the branches town and clothes, clean, all committed | retired with the one-session rule; their branches are on GitHub; untracked files not yet checked |
| C:\Users\Jafar\ledger-exec | 1.9 GB | a checkout of the deleted ledger-migrate repository (16 September); 2,831 of 5,914 files are in this project's folder; 341 MB are not: early character models (192 MB), old renders (93 MB), voice conditioning clips, picked clips and live-voice clips (15 MB) | **keep** until its voice clips are checked against the voices in use (a 0.4 disagreement row) |
| C:\Users\Jafar\ledger-exec-state, ledger-meshgen, ledger-rescued | under 4 MB | the old executor's journal, machine reports, rescued voice probes of 6 September | archivable (reports of retired machinery) |
| C:\Users\Jafar\ledger-imagegen | 6.5 GB | the local image model and its runtimes | kept: a tool, not output |
| C:\Users\Jafar\ledger-mixamo | 1.6 GB | the Mixamo harvester | kept: poses come from Mixamo (RULINGS) |
| C:\LedgerTools | | Blender, the voice engines, MetaHuman assembly, Python | kept: tools |
| C:\actions-runner-ledger | | the build machine | in use |
| F:\LedgerTools (51 folders) | | lasting inputs, bodies, garments, models, renders, approvals' full-size pictures, the NoAI quarantine | under production/retention.json's limits; the quarantine is his to delete |
| F:\town-bench, town-bisect, town-scratch | 77 MB | the town session's bench runs, bisect checkouts and a talk build of 28 and 29 September | archivable scratch |
| Documents\Codex, Documents\ChatGPT\Ledger | 1.8 GB | his own conversations and Codex workspace | his; listed, not opened beyond their names |
| Downloads | | his: the 30 September audit (saved in production/audits), two September briefings, an August build zip | his |
| E: | | nothing of the project's | none |

## 4. His page answers

37 pages; 144 stored answers, read from each page's own database into production/approvals/answers/ (INDEX.md lists them). Five July and September pages declare no database; two status pages held no answers. Whether each answer reached the records is checked in page-answers-check.md beside this file.

## 5. What the sweep found that matters most

1. The September atlas was the town's only map, unknown to every list; a second map was drawn from nothing on 4 October. It goes to him today.
2. 46 research reports, the full sources behind the summaries main keeps, lived only on unmerged branches; they are now copied in beside their summaries.
3. Nothing else of value was found only outside main, except the old checkout's voice clips, kept until checked.
