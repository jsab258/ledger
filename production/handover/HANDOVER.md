# Handover: where the production session stands

The one file a fresh session starts from. Rewritten, not appended, at each stop; capped at 1,800 words (tools/doc-caps.py, 8 Nov). Rules are CLAUDE.md's and RULINGS.md's; the items are NOW.md's and the order's; this file holds what is in flight, what failed and why, the next steps in order and the tries used. Older lessons: TRIED-ARCHIVE.md.

**Started:** 2026-11-11 12:22 (hourly run)
**Stopped:** 2026-11-11 12:06 (history 342k past its point after advisor 97's first cuts; Sheila's cardigan helper still running, its report lands in SHEILA-CARDIGAN-S4-2026-11-11.md)
(The hourly task runs `python tools/fresh_gate.py` first; at each item's end `python tools/history_check.py`: OVER means rewrite this file, set Stopped, stop.)

**The goal:** his order of 9 November (production/orders/2026-11-09.md, adopted by his tap 8 Nov 17:17; runs to 13:00 Monday 16 November).

## Standing ways of working (carry across every rewrite)
- **The night (advisor 42 and 44, his anger 07:32, 9 Nov):** round the clock; during the night's build and walk only work touching Unreal and heavy local jobs pause; every session and all allowed helpers keep working on everything else; no session stops for the night. Space checked before the night build by 23:30. Six helpers while behind the line (his tap 07:17).
- Standing since his 8 Nov tap (RULINGS 6 Nov): the waiting list when the order's items wait; four helpers, none that may finish during a tester walk; the hourly start round the clock, nothing touching Unreal 01:15 to 04:30, stopping before 01:40.
- A short row to 'reports' at least once an hour while working, even with nothing finished (message 15), ending 'Allowance: N% at HH:MM, pace X; my spend US$Y since HH:MM' (get_usage, Weekly all models; `python tools/pace_line.py <percent>`; `python tools/token_measures.py --spend HH:MM`; messages 17, 18). **Write the row with ArtifactData and see its version in the result; never record a row that was not written.** The "at" field is +01:00 (Swiss winter time).
- **Every time stamp from PowerShell's Get-Date at the moment of writing, never estimated**.
- **Advisor 33 (19:55):** any hourly reading over 2 points behind the line: at once the session on Unreal work and four helpers on the order's no-Unreal parts, pulled forward in order, round the clock; the hour's row names what was pulled forward; within 2 points carry on; over 3 ahead, two helpers.
- Never stop for lack of work: the order's next item, then the waiting list, then the fallback list (message 12). Phase 3's port: its open rows (G5, W3 to W6) are all low and would change the game, so they wait for an order.
- An advisor's standing way goes here the same hour, named in its ack (message 13); the six measures' table in each morning's overview (message 11).
- **Advisors 64 and 68 (9 Nov):** never end a turn while work remains: while a long job runs, work other items, read his page and the advisor every 15 minutes, check the job. A session ending a turn with no goal running writes Stopped first. The gate starts the next session after 30 quiet minutes even while a job runs, naming the job; that session leaves the card alone until it ends.
- **Advisor 91 (10 Nov):** the Monday numbers carry the builder's share of the account's weekly meter: its week's logged dollars divided by the dollars one meter point costs, measured in stretches when the builder ran alone (night hours; 9 to 10 Nov gave about 8 points for its logged spend), method and uncertainty stated; the rest of the points are everything else on his account.
- **The lean start's page reads, filtered (advisor 97, 11 Nov; measured: the three full listings cost about 10,000 tokens a start):** never list advisor, advisor-acks or verdicts whole, nor with out_dir. Two queries for the advisor: advisor-acks ordered by "at" descending, limit 1; then advisor where "at" is after that ack's. Verdicts: a query where "at" is after the last page read. Open page items by a filter on items.json (answered items now live in archive.json, never read at the start). The task file still says the old reads: editing it was refused by the permission check, so it is his to change.
- Helper briefs that work on one person carry "person <name>" (the token audit's By person table, from 8 Nov).

## Run on 11 Nov, 11:22 to 12:15
- Advisor 94 (his ask 10:23) done: Drape Studio retested on its update (DRAPESTUDIO-TEST-2026-11-11.md, preview drapestudio-jumper-2026-11-11.jpg): run 1 holds the jumper on the shoulders (front 1,082 to 1,626 mm against Marvelous 1,068 to 1,625), 0 cloth points inside against 74, 246 s against 124 s, cuffs bunch; auto seams fold the waistband; repeatable; FBX export works. Yesterday's body counts were partly our check misreading relative OBJ face numbers. Pushed fdec78a35.
- n09-6 resizing verdict (RESIZING-VERDICT-2026-11-11.md, review PASS WITH FIXES, made): Epic's resizing already dresses every built cast member as the white layer (nearest of six source shapes, baked per character, about 5 MB, 4 levels, no cloth kept); Tom's jumper not put through it (no end-to-end script route; CreateCombinedFaceAndBodyMesh C++ only; a C++ helper about 4 h). On his page: resizing-backbone-2026-11-11 (keep carried garments recommended / 4 h real test). tools/ue/resize_probe.py reads built outfits (commandlet); its vertex counts failed twice, left.
- n09-9: p1-packaged.ps1 writes <label>-launch.txt per capture (checked on a real line: TEST).
- Sheila's skirt route decided (DECISIONS 11:28): Chaos cloth on the skirt alone (Mafia's and KCD2's method), after the cardigan and shoes.
- Advisors 95, 96, 97 acked. 96 done: FRESH-SESSIONS-2026-11-11.md (history share 53/40/24% by week; no session for 1,439 of 2,820 minutes; start US$0.35; records 7.2%), row 12:10. 97 part 1 done: START-COST-2026-11-11.md (fixed 61,451 tokens; listings about 9,900, now filtered queries, see standing ways); items.json archived (172 KB to 18 KB). The edit of the scheduled task's own SKILL.md (and HOURLY-TASK.md) to filtered reads was refused by the permission check: never work round it; his to change.
- His page: 3 open items (resizing-backbone, fifteen-minute-start, efficiency-ruling), the phone screen's limit. Last page read 12:00 (verdicts none new).

## Next, in order
1. FIRST: pace (12:05: 31%, +4.9, two helpers at most); his page's verdicts after 12:00 and advisor messages after 11:58 (filtered queries). On his taps: fifteen-minute-start yes: the steps in advisor 95 (schedule, hand-over wording, fresh_gate test, RULINGS replacing 4 Nov's hourly line, DECISIONS); efficiency-ruling yes: RULINGS line replacing 5 and 7 Nov's efficiency line, his words; resizing-backbone: keep = record and close; test = the C++ helper route in the verdict.
2. Sheila's cardigan: an importer helper started 12:00 (brief: carry Tom's jumper chain-j3d to MH_LenaS4, cut the front, 29 mm band, seven buttons, clear over the blouse, skin; report SHEILA-CARDIGAN-S4-2026-11-11.md, files F:/LedgerTools/garments/sheila/cardigan-s4-2026-11-11). Its report may land after this session stopped: read the file. Then step 4 shoes (carry Ron's v2 boots, low brown derby), then the skirt by Chaos cloth (make_cloth_garment.py route).
3. Advisor 97 rest: part 2a, the Stop hook (tools/stop_hook.py, selftest 5/5, blocks this real session correctly; not installed): its one-tap item when a page slot frees (install = .claude/settings.json Stop hook running python tools/stop_hook.py; it lets go after one nudge via stop_hook_active). Part 2b: check whether skills can be hidden for this project only (claude-code-guide helper), then the item or a recommendation against. Part 3, standing: by 19:00 daily DAILY-YYYY-MM-DD.md in production/research/token-audit/ with the fixed measures (advisor 97 lists them), the extractor's scripts in C:/Users/Jafar/AppData/Local/Temp/ledger-audit-96/ reusable.
4. Before 23:30: space for the night build (F: 26.2 GB at 11:50); nothing touching Unreal 01:15 to 04:30. The walk carries n09-3's re-import, n09-5's stand-up, Tom's rows back at the morning look.
5. n09-12 (UE4SS run per game, never beside Unreal); n09-3's cooking plan.
6. Morning: the walk report (cast idles), the stand-up lines, the memreport for n09-3.

## Tried and failed, and why (newest; older in TRIED-ARCHIVE.md)
- Tom's surfaces by painted maps (11 Nov, try 3): denim streaks evenly spaced and continuous with no diagonal read as pinstripe close up; a dark jacket hides lightness speckle; a grain tile reaches the boot's welt. Three tuning passes on the welt changed nothing (cause misread). Listed for the next order.
- Motion 1, rise from a chair (set aside 11 Nov 00:42 after 2 of 2).
- Clips over 81 frames lose the card (Vulkan device lost).

## In flight (carried)
- TomJeansTC stays held, never released; it now draws the details-stage colour map.
- F:/LedgerTools/gate/new/tom-films-2026-11-11 and -b; brick-flemish-2026-11-11 (the swapped brick files' originals in originals/; the packaged copy restored 06:37).
- C:/LedgerTools/ai-video/out (motion films and FBX); C:/LedgerTools/mocap-solve scratch project; mh-assemble test assets in /Game/MocapSolve and /Game/CaptureManager/Imports/m2s1101*_1 (the session's, unused).
- F:/LedgerTools/texture-tools (about 600 MB); F:/LedgerTools/drapestudio-test-2026-11-11 (the retest).

## Kept as they are
- Uncommitted on purpose: the office prints (copies on F:/LedgerTools/game-inputs); untracked shop-room files are not this session's; stash@{0} kept.
- Waiting list for the next order, beyond the order file's own: as written at 10:25 (git show c8d0834c7:production/handover/HANDOVER.md, 'Kept as they are'), plus Drape Studio's cuffs and a per-piece worst-stretch check, and the true resize of Tom's jumper if he picks keep.
- Tries used (older: TRIED-ARCHIVE.md, "Tries carried 10 Nov"): Tom's surfaces 3 (two tiles, one painted), set aside, listed; Sheila's skirt band clear 2 of 2, set aside; the cast's bind pose 1 of 2 (fallback idle, confirmed in packaged logs, the walk to confirm); the office exit 2 of 2 (stand-up, tonight's walk decides); Tom's chest skin 1 of 2, passed; the boots 5 (his yes), passed; the crown 4, listed; the solve: commandlet 2, full editor 2; Drape Studio's jumper 2 of 2, spent; motion 3's clip 2 of 2; motion 1's clip 2 of 2, set aside; texturing: jeans masks 2 then the fair film (set aside as a garment method), brick 2 offline plus one packaged film (his look), timber edge wear 2 of 2, set aside (today's stays), the cornice 2 of 2 set aside.
- API spend: US$1.15 (8 Nov); none since.
**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run more helpers than RULINGS allows; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help, or guess a tool's name; let a helper stop a process; work while another LEDGER session works; write a time without Get-Date; put an unmeasured number in a row (done once at 06:50, corrected).
