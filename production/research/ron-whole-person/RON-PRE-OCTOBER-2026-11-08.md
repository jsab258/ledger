# Ron before the time log, n09-5 (8 November 2026)

Read-only git log, commits before 5 Oct 2026, local clock +0200 (CI commits shown as +0000, same instants). Sitting: commits within 90 minutes of the previous one. Hours I: a sitting's first-to-last span, with 0.5 h as the floor for a one-commit sitting (an assumption, not a measure). Most commits are shared with other people or the town's code, so every figure is an upper bound on Ron's own work. Sittings may overlap between rows; rows do not sum to wall-clock time.

| Part | Paths | First | Last | Commits | Sittings | Hours I | Notes |
|---|---|---|---|---|---|---|---|
| Body (MH_RoccoP2) | none own | not recorded | not recorded | 0 | n/a | not recorded | First "RoccoP2" in git is da55b8b9b (26 Sep 10:20); no commit holds the body's making. |
| Face (preset pick, P2 rebuild, approval) | production/casting/ron-kirby/ (SHEET, P2 images) | d5a4312eb 24 Sep 16:08 (MetaHumans in the street) | d4f64668d 29 Sep 21:22 (his page) | 8: d5a4312eb 271701f20 648ba22e9 34a785957 db1297a93 e51b35cb1 6f4ee6175 d4f64668d | 7 | 3.5 | Face frozen as P2 (6f4ee6175, 28 Sep 15:26). Shared with Lena and Sam commits. |
| Voice pick | voice-candidates/rocco, game-design/picked-clips/rocco.p227.mp3, voice-conds/rocco.*, audition-rocco.wav, content/voice/acks/rocco | 527178b16 31 Jul 11:39 | d42d67308 28 Sep 21:36 | 10: 527178b16 4eefad700 986c2b8c1 b216faea0 683cfd58d 6394edbbe f4d5cf69e d119d33f8 1b035a467 d42d67308 | 6 | 3.2 | Picked clip kept 986c2b8c1 (31 Jul 14:34); CI commits are machine time, not his. |
| Voice acting tests | production/casting/acting-2026-09-29, ron-kirby/voices | e214246db 29 Sep 03:41 | d4f64668d 29 Sep 21:22 | 3: e214246db 9d01a83ea d4f64668d | 3 | 1.5 | His pick (Chatterbox Nano over Sopro) made 30 Sep 05:54, recorded 1 Oct 00:55 (DECISIONS 30 Sep). |
| Street lines | production/casting/ron-kirby/STREET-LINES.md (+ approval.json) | 69fac1615 30 Sep 09:19 | 5d80bbe8a 30 Sep 15:00 (approval file) | .md 1; with approval 3 (69fac1615 cbe276499 5d80bbe8a) | 1 (.md) | 0.5 | 159 lines in one commit (DECISIONS 30 Sep). Tone tap 30 Sep (his). Elapsed time before the commit not recorded. |
| Talk card | production/cast/cards/rocco.md | c03d8fb72 23 Sep 16:46 | 5d80bbe8a 30 Sep 15:00 | 8: c03d8fb72 5518e8b06 989d51dcf 21e125ac4 607bfc27a 5a8dc29a8 cbe276499 5d80bbe8a | 7 | 3.5 | Commits mostly change all cards; Ron's share not recorded. |
| Facts | ledger/Assets/Scripts/Core/StreetFacts.cs | 12142c8b3 29 Sep 18:10 | 2fa0163b0 1 Oct 08:31 | 7: 12142c8b3 89168d218 cbe276499 5d80bbe8a 2615b4f5f b0fecacf9 2fa0163b0 | 5 | 2.7 | Shared street code, not Ron only; Ron's plain wording taps 30 Sep. |
| Routine | production/specs/hook-cast.json ("routine" rows, id "rocco") | 3d31ddc53 28 Sep 16:20 | bb605acba 30 Sep 23:13 | 15 (list: 3d31ddc53 e2f690a64 4ebdccbec 0494a9452 ce9a4600b 186f7ba2e caf5b09e9 28d41a527 508cea5b1 a1df1ccb2 eae4e1048 71f5aa28b 7bd1b8290 1237a7de0 bb605acba) | 8 | 6.4 | File holds all 41 people's rows; Ron's own edits not separable. File's earlier history, if renamed, not followed: not recorded. |
| Donkey jacket, 25-30 Sep | production/art/clothing/donkey-jacket-* | 99d6ba413 25 Sep 01:11 | 2d03cdf10 30 Sep 13:38 (set aside) | 13: 99d6ba413 1899a172e c46166868 daf73e055 b432f685e 67c82f362 c2cf9dacb 18ffed6ce bb809f8cf fcd8f8eea 309f64375 7462dcf24 2d03cdf10 | 8 (5 to 29 Sep, 3 on 30 Sep) | 3.9 + 1.5 = 5.4 | Set aside after three blind reviews twice (fcd8f8eea 29 Sep 21:15; 2d03cdf10 30 Sep). 7 Oct attempt is after this window. The 2 Oct tests: not Ron-specific, not counted. |

## Total

Inferred, upper bound: 26.7 h across face 3.5, voice 4.7, street lines 0.5, card 3.5, facts 2.7, routine 6.4, jacket 5.4. Not recorded: body (no commits), his own minutes in any sitting, Ron's share of shared commits, and CI waiting.

DECISIONS lines naming Ron or Rocco, 28 to 30 Sep, were counted by grep (about 30; e.g. 28 Sep thinking sounds, 29 Sep outfit's ask, 30 Sep street lines, tone, voice). They carry no hours.
