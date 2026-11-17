# n16-11, the games' numbers: method, licence note and empty table (lane, 17 Nov 2026)

For the next order's n16-11 (from n09-12). Machine-free part only: nothing installed, downloaded, extracted or run. Reference: studies/12-tech-budgets.md (its blind spots: measured frame times in a street, cell sizes, shader counts; n09-12's rows: triangles, bones, detail levels, texture sizes).

Evidence (all read 17 Nov 2026, each claim linked there):
- production/research/lane/UE4SS-AND-ENGINES-2026-11-17.md (UE4SS releases, engines, stats in Shipping, DRM, offline readers)
- production/research/lane/FRAMETIME-METHOD-2026-11-17.md (PresentMon, its CSV columns, card memory counters, 1% low definitions, run practice)
- production/research/lane/GAME-TERMS-AND-STUDY-LAW-2026-11-17.md (each game's terms, Steam's agreement, Swiss law articles 19, 21, 39a; not legal advice)

## 1. Corrections to earlier notes

- UE4SS's latest stable release is v3.0.1 (14 Feb 2024, its own changelog), not v4.0.0. v4.0.0 is still "TBD"; its 5.4 to 5.8 support exists only in the rolling experimental build. The lane checked the releases page itself (read 17 Nov 2026, 18:25): v3.0.1 marked Latest, experimental-latest a pre-release. UE4SS-READING-2026-11-12.md and UE4SS-METHOD-LICENCE-2026-11-17.md both say v4.0.0 published 12 Nov; that is not what the page shows today and should be treated as wrong until the PC reads the API itself.
- Shipping builds strip stat commands (Epic: Shipping "strips out console commands, stats, and profiling tools"; Build.h STATS 0 per 2016 engine source quoted on a forum, current source unverified). So "stat unit" or "memreport" through UE4SS will not give frame or memory numbers. Frame time and card memory come from outside the game.
- Engines (minor versions per CUE4Parse's game list and fan sites, not developer-confirmed): Silent Hill 2 Unreal 5.1; Mafia: The Old Country 5.4 (with Denuvo); inZOI likely moved to 5.6 in spring 2026; Kingdom Come II is CryEngine, where UE4SS, FModel and CUE4Parse do not apply.

## 2. Methods, from least to most intrusive

| Method | What it gives | Touches the game | Terms and law that bear on it |
|---|---|---|---|
| A. Config text files | quality tiers, pools, distances, budgets (already done for Mafia and KCD2 in Study 12) | reads files only | none found against plain reading; KCD2's licence bars software that "reads or mines" stored data, which may reach automated reading |
| B. PresentMon from outside | frame time per frame (median, P99, 1% low) in a street, per game, on his PC | nothing by design (Windows' own event tracing; no injection stated, inferred) | none found; needs admin or the Performance Log Users group |
| B2. Windows card-memory counter | the game's card memory over the walk (peak, median) | nothing | none found; counter name to be listed on the PC first |
| C. UE4SS run once (DLL in the game) | a .usmap type map for reading paks offline | loads a DLL into the game | Steam agreement 2.G and 4.B; Take-Two's terms (Mafia, Denuvo on top); inZOI modkit terms on altering internal structure |
| D. Offline pak reading (CUE4Parse, FModel) | triangles per LOD, bone counts, LOD counts, texture sizes | reads encrypted files with the game's AES key | Swiss URG 39a (encryption as a protection measure; whether study is an allowed use is open), Steam 2.G, KCD2 section 5, Take-Two's terms |

Licences of the tools (none ships in the game; ast-grep's line in the allowlist is the precedent for a tool used, not shipped): PresentMon MIT (from the repository; its LICENSE file itself not reached), CapFrameX MIT with bundled MPL 2.0 parts (not needed), UE4SS MIT (production/research/aaa-reference/UE4SS-METHOD-LICENCE-2026-11-17.md), CUE4Parse Apache 2.0, FModel GPL-3.0 (the lane's reading: running it unchanged and shipping nothing of it raises no GPL duty; the allowlist decides). The allowlist is law; ast-grep, a tool used and not shipped, went into it by his pick (item 10), and PROCESS rule 2 asks for a decision record per new tool. So PresentMon goes to him as a one-line licence pick before it is downloaded.

## 3. Recommendation (for the main session; licences are his call, so C and D need his pick)

- A needs nothing new. B needs his licence pick for PresentMon (question 1 below); it answers Study 12's top blind spot (measured frame times in a street) and changes nothing in the games. One repeatable walk of about 60 seconds down a busy street per game, after standing still 30 seconds on arrival, 1 warm-up and 4 measured passes, a re-run if the pass medians differ by more than about 3% (the source's method; `pass_spread_pct` in the script checks it), same settings as Study 12's rows (1440p-class output, the game's High preset, no upscaler change), PresentMon console to CSV plus the card-memory counter once a second; never beside Unreal or a Kiln gate; no alt-tab during a pass (Microsoft's known counter fault). The same walk in LEDGER's packaged build gives the LEDGER column.
- Turn each capture into the table's numbers with tools/lane/frametime_summary.py (written here, its tests pass): frames, median, P95, P99, worst, 1% low both ways, spikes over twice the median.
- C and D (triangles, bones, LOD counts, texture sizes) carry real terms risk: they reach inside the games' encrypted files or load code into them, which the games' terms and Swiss article 39a speak to. The numbers they give are already partly published (inZOI's ModKit docs: hair LOD0 about 40,000 triangles, LODs 0 to 4). Proposed question for his page (licence, his to decide):
  Q1 (licence): Measure the games' frame times from outside with Intel's free PresentMon (MIT, used on his PC, never shipped), written into the allowlist like ast-grep. A) yes (recommended); B) no.
  Q2: Triangle and bone counts from inside Silent Hill 2, inZOI and Mafia need tools that open their locked files, which their terms may forbid. A) published figures and outside measuring only (recommended); B) also open Silent Hill 2 only (no DRM, stable tool); C) open all three.

## 4. The empty table (to fill on the PC; every number from a capture file or marked not)

Run settings per game: output resolution, preset, upscaler and its scale, card, driver, Windows build, route name, date.

| Item | Mafia (UE 5.4) | Silent Hill 2 (UE 5.1) | inZOI (UE 5.6) | Kingdom Come II (CryEngine) | LEDGER (UE 5.8, packaged) | Source file |
|---|---|---|---|---|---|---|
| Median frame time, ms | | | | | | |
| P99 frame time, ms | | | | | | |
| 1% low, fps (count: 1000/mean of slowest 1% / time-weighted as CapFrameX) | | | | | | |
| Spikes over 2x median, per minute | | | | | | |
| Card memory, peak / median, MB | | | | | | |
| Internal resolution, % per axis | | | | | | |
| People on screen in the street (counted by eye) | | | | | | |
| Character triangles, LOD0 (published or method D) | | | inZOI hair alone LOD0 about 40,000, varies by hairstyle, a modder-facing limit (games-numbers/MAPPINGS-SCAN-2026-11-08.md, PUBLISHED-NUMBERS-2026-11-09.md) | | | |
| Character bones (published or method D) | | | | | | |
| LOD count, characters | | | 0 to 4, head (same files) | | | |
| Texture size, character body (published or method D) | | | not found (a 2K figure from a search snippet only, unverified) | | | |

## 5. Steps for the main session on the PC (about 2.5 h of the 3 h budget)

1. Merge this file, the three research files and tools/lane/frametime_summary.py; put Q1 and Q2 on his page (one batch); on Q1's yes, the allowlist line and the DECISIONS line for PresentMon.
2. Download PresentMon's console release from its official GitHub release; read its LICENSE.txt and record it; check the hash GitHub shows.
3. On the PC, list the card-memory counters (Get-Counter -ListSet 'GPU*') and note the exact names.
4. Space check, then per game one warm-up and four 60 s passes on the chosen street; CSVs and counter logs to the games-numbers folder on F: (small text).
5. Summarise each with the script; fill the table; mark anything not measured "not".
6. Same walk in LEDGER's packaged build for its column.
7. If his pick is B or C: research UE4SS experimental's exact build for that engine version first; method D stays offline and nothing is extracted beyond counts.

## Unverified or unreached

PresentMon LICENSE.txt and v2.6.1; UE4SS release asset names and the API; whether UE4SS works on inZOI 5.6 or Mafia 5.4; the card-memory counter's exact names; Silent Hill 2 and inZOI licence pages; Konami's and Take-Two's full terms; whether any game blocks event tracing (none found).
