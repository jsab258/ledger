# Test plan, phases 2 and 3 (draft, 8 Nov 2026)

For n09-9 (orders/2026-11-09.md line 30); nothing decided. Base: QA-LEAN-PROPOSAL-2026-11-07.md (QA), QA-FIRST-STEPS-2026-11-08.md (STEPS), their reviews; all read 8 Nov 2026. Method: Warhorse's per-objective marks (QA line 11, undated digest); Mafia's QA unreached. Rule: a check only after a fault slipped past, dropped after a month catching nothing (RULINGS line 23).

## 1. The bar before a build reaches him

Each check is marked **fails** (stops the build or the pass) or **reports** (a line read by the session, failing nothing alone).

1. **ci-checks pass** (fails): CoreTests, TalkTests, Soak, SaveChaos, PerceptionGolden, StrangerTest (ci-checks.sh lines 235 to 241), canon and content gates, reach-check (line 148), homes_check.py and the spec tests (lines 205, 220; study 13 line 59). Catches broken simulation, the port drifting from the C# goldens, brand words.
2. **Asset checks before any reviewer** (fails for garments and the shipping project; the street's known list fails nothing alone) (tools/ue/asset_checks.py, D13 28 Oct): stale imports, placeholders, JPEG normals, triangle overruns (8 Nov sweep: shop displays 74,000 to 702,000 against 60,000, FINDINGS line 12). Editor side untested when written (asset_checks.py line 35).
3. **Reviews sized to the piece** (fails on a new fault) (RULINGS line 36).
4. **Passed on the player's launch** (reports today; the packaged-walk skill's pass needs PLAYER or PLAYER+WATCH, STEPS line 90): launch_line_check.py reads PLAYER, PLAYER+WATCH or TEST. Catches the office "passed" behind -MickeysInside (STEPS step 2). A stale log passing as tonight's (LAUNCH-LINE-REVIEW fault 1) was fixed on 8 Nov (commit cdaf03073).
5. **The nightly packaged walk** (fails on route stages, the eyes on its pictures, save and Continue; the legs-never-arrived line reports only, firing 16 of 20 nights, section 5) (nightly_walk.py). A piece passes only there (CLAUDE.md).
6. **Memory and frame** (reports; built 8 Nov in slice-perf.py and perf-hook.py, MEMORY-PEAK-REVIEW-2026-11-08.md): peak frame at High against 5,650 MB, worst frame against 33.3 ms (PIECES-DRAFT line 84). Catches medians read as peaks (STEPS lines 116 to 121; QA lines 38 to 42). Reads Highest until the perf step moves to High (STEPS, "Held").
7. **His page only after the gate** (fails on a new fault): Hook sheet, last good picture beside (CLAUDE.md, "The gate").

**The pass:** a build reaches him when every "fails" check above passes on it and the session has read every "reports" line, each new fault named in it blocking and each known shortfall listed.

"99% done" (RULINGS line 23) has no measure in any source read. Working reading: checks 1 to 7 name no new fault on the build he gets (unverified; the session's to rule).

## 2. Phase 2, by piece kind

Weekly measures stay on the progress page (PIECES-DRAFT section 4), not bars. No check is added in sections 2 and 3; everything listed beyond section 1 is a measure, and phase 3's "empty minutes" (PLAN line 34) is the only new measure.

- **Fronts**: kit target from the source by a fresh helper, automatic check, reviewer against photographs (RULINGS line 57); asset checks; medium gate; night pictures in the walk. Mickey's dark front was caught by eyes (FINDINGS line 8, 4 Nov). Nothing added.
- **Shells and roofs**: asset checks; kit placements per mesh as a measure. The draft's width and street-end checks (PIECES-DRAFT line 21) name no slipped fault: measures only.
- **Ground and furniture**: wet_ground_check.py, stain_check.py. Missing ground behind the frontage was caught by a gate (FINDINGS line 8). Blocked ways: the legs line and the walk (crates and cars walled off pavements, FINDINGS line 19). Collision left on: its ten places counted in play with the camera and walk checks (FINDINGS line 24). Nothing added.
- **Props**: one Sonnet reviewer, one round, then the walk (RULINGS line 36); triangles via asset checks; props per 10 m measured.
- **People and clothes**: asset checks; garments_shipped_check.py; full gate and his look; walk, sit and turn on film (order rule 10). The base layer was named in 12 night reports (QA line 36): no check. Treading on the spot: the legs line plus one small review on a fire (QA line 44). Candidate only: an import into the wrong project "succeeds and changes nothing" (MEMORY); whether it reached a build is unverified, so not added.
- **Light and weather**: charts C2 and C3, night clip at most 2% (PIECES-DRAFT line 81); the three morning views; gate pictures at High (MEMORY).
- **Sound**: layers present against the study's table (measure); allowlist and attribution-check.py; his ear decides, the accent checker only screens (RULINGS line 69).
- **Cars**: P9's blind silhouette and his tap first (PLAN line 29; PIECES-DRAFT lines 71 and 93); canon gate for brand words; asset checks; legs line for blocked ways.
- **Exit** (PLAN line 30): whole-street day and night walk, reverse views and P15, a fresh reviewer.

## 3. Phase 3, the town remembers (PLAN line 33)

- **The port (N3)**: port-golden-check.sh and route_week_check.py (16 rows against the Core's): drift from the goldens.
- **Arrivals and deliveries**: route stages and the eyes. A person vanishing in view after 12 s (FINDINGS line 19) was caught by the tester: nothing added.
- **Consequence kept after restart**: the walk's save, quit and Continue; SaveChaos. The police file's three faults (FINDINGS line 18) are fixed before a detective's crime is wired; whether crime-verdict-check.py covers them was not read (unverified).
- **The office and the ledger**: the launch line (the office's own fault); the camera reviews that caught seated Ron cut off (QA line 56).
- **Talk**: the nightly sixty-question bench through ClaimCheck.CheckAsync (MEMORY) for "that's all I know"; first word at 2.0 s (FINDINGS line 11). Suspicion unread from the port (FINDINGS line 9) is a build item, not a check.
- **Exit**: two thirty-minute routes, one live route, at most five empty minutes, no critical fault (PLAN line 34). "Empty minutes" has no tool: built as the exit review's measure, not a nightly check. Feel checks are his, judged on fun (order rule 7).

## 4. Dropped or not added

- Menu sweep, five resolutions: no fault yet (QA line 14).
- Firewall line: no better than the tester (QA line 32).
- Undressed count: never missed (PROPOSALS-REVIEW line 15; QA line 36).
- Quay StandBlockedAt line: needs C++; only if the quay stop returns (STEPS line 16).
- An agent driving free play: needs his ruling (QA line 63).
- Testing tag: a record, not a check (STEPS step 4).
- Study 13's naming check (lines 42, 69 to 73), a spec number duplicated as a C++ constant (lines 64 to 67) and Mafia's asset-registry tags (line 84): no fault of ours slipped past them; not added (TEST-PLAN-VS-STUDY13-2026-11-08.md).

## 5. Open, unverified, unreached

- The legs line fires on 16 of 20 nights (STUCK-LEGS-REVIEW line 15): as a bar it would always fail. Sheila's spot, 1.31 m short on five nights, needs its cause read.
- Perf step at High held for the order; two commands in one -ExecCmds on 5.8 unverified.
- Unverified: clock-to-picture mapping; the asset checks' editor run.
- Study 13 read 8 Nov (TEST-PLAN-VS-STUDY13-2026-11-08.md): no budgets or build gate in it. Not reached: crime-verdict-check.py, encounter-verdict-check.py, Mafia's QA.

## Review (8 Nov)

One fresh small review, pass with fixes, seven findings (TEST-PLAN-REVIEW-2026-11-08.md); all seven applied by the session the same evening: the suites' lines 235 to 241 with TalkTests; reach-check for gamecheck; the medians' and the dark front's citations; a fails or reports mark on every check and one pass sentence; check 6 marked not built; the lean note; the P9 and never-missed citations.
