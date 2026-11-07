# Fresh review of three proposals for Monday's order (8 Nov 2026)

A fresh reviewer read each proposal against its reading notes and the local files they cite (WALK, REHEARSAL-B and -D, NOTE, Studies 4, 7 and 12, LAUNCH-PEAK, both diagnoses, UNIT-COSTS, FINDINGS, slice-perf.py, PersonAnim.cpp, SliceCharacter.cpp). No web page was fetched: no fetch tool was available in this run, so the web links were not checked again and rest on the readings' 7 Nov notes. No file other than this one was written.

## 1. QA lean proposal: PASS WITH FIXES

**Tracing.** Every outside claim matches the reading: Warhorse's per-objective marks, TITAN's 30% false alarms, GBQA's 48.39% (abstract only, marked), XR-003 menus, the five PC resolutions, Lachance's 10% and idle testers, the bug-report fields. The project facts that are not in the reading trace to project files: 6,161 to 8,481 MB in 32 captures (REHEARSAL-2026-11-07-D line 15), the reviewer cost of US$0.59 to 1.66 and the US$22 to 38 stand-in rate (UNIT-COSTS lines 13, 27, 30; the rate marked inferred there), the quay diagnosis at "about 95%" (its line 5), and FINDINGS 25 and 28. These have no file named: "14 legs towards (7.9, 4.6)" (no verdict.json path or date), "at least 12 night reports from 23 Oct", "his 8 Oct ruling".

**Unverified and unreached.** These are handled well: the digest limits, Warhorse's undated interview, the abstract-only papers, Mafia's QA unreached, no money cost per game hour.

**Follows from the reading.** Yes. The month-long drop rule and the 15% share are the proposal's own (the 15% is marked as the brief's figure).

**Lean.** Mostly. There is no new department, the first step is four read-only report lines, and every check has a cost. Two weaknesses:
- The memory line compares `gpuMemMB` with 6,000. In slice-perf.py:76 that figure is a median after dropping 300 frames, which is the exact fault the memory plan names ("medians read as peaks"). The two proposals also disagree on the line: this one uses 6,000, the memory plan a ceiling of 5,650 under a budget of 5,771.
- The undressed-count line is kept even though the proposal says this fault was "never missed" and the line saves "little".

The fault list also leaves out two of this week's faults that reviewers found on films: Tom's knee and boot going through the window board, and the camera cutting off seated Ron. The list should say that the existing eyes caught them, so no check is needed.

Fixes:
- Memory line: read the per-frame peak of GPUMem/LocalUsedMB at High, not the median, and take its line from the memory plan.
- Drop the undressed-count line from the first step, or give a fault it would have caught.
- Name the source file for the 14 legs, the 12 night reports and the 8 Oct ruling.
- Name the window-board and seated-Ron faults as already caught by the reviewers' eyes.

## 2. People alive proposal: PASS WITH FIXES

**Tracing.** The outside figures match the reading: the forum thread, Holden's "dragged along", the arXiv figures (0.08 s against 0.88 s, 0.80 ms against 0.22 ms, tail unread), Mafia's 4 idle turns and KCD2's 45/90/135/180. The local figures all check out:
- WALK: stops dragging 11.3 and 17.6 cm, stops chosen with 68 to 118 cm left, 7 of 8 turns over 3 cm.
- REHEARSAL-B: 13.68, 42.8 and 28.2 cm.
- NOTE: CalmAlpha 0.7, to be lowered to 0.2 to 0.3.
- PersonAnim.cpp:598 (41 cm at 60 degrees) and :616 (120 degrees a second).
- SliceCharacter.cpp:842-848 (the push reaching the mover).

Unsupported or overstated:
- "play rate within 10% faster, 20% slower (Clavet, through Study 7)": the reading lists Clavet's talk as unreached behind the sign-in wall. Study 7 took the figure from talk notes, so it is second-hand and should be marked unverified.
- "Line-trace braking, recommended": the only support is one poster's own workaround in a thread left unresolved. The sweep that cuts the push is the project's own design. Its promised result ("glancing, he walks along it at his true speed") is a prediction and is not marked as one.
- "Epic's 18 standing breaks are on F:, five carried over" and "M_Relaxed_Stand_Idle_Loop is on F:": neither names a source, and neither was found in NOTE or WALK.
- The 5.8 PoseSearch source lines and "the 5.6 release notes returned empty text" are new evidence that the reading does not contain.

**Unverified and unreached.** "Fixed in 5.6" is properly marked unverified, and so are the likely cause and the 21 mm figure. The closing "Unreached" line, though, names only the GDC talks and the Foot Placement guide. The 5.8 blog (403), the 5.6 notes, the Stride Warping guide and the arXiv tail appear only in the text.

**Lean.** Yes. Costs are given, two sections are held until a fault is seen, and the first step is the film already owed.

Fixes:
- Mark Clavet's play-rate bounds as second-hand and unverified.
- Call the push cut untested and the project's own, not the forum's.
- Give the F: path for the 18 breaks and the relaxed idle loop.
- Add the PoseSearch source reading and the empty 5.6 notes to the reading.
- Complete the closing unreached list.

## 3. Memory plan: PASS WITH FIXES

**Tracing.** These check out:
- The figures are medians after 300 dropped frames (slice-perf.py:26, 76).
- The step ran at Highest with a pool of 1000 (diagnosis line 21).
- LAUNCH-PEAK gives 6,086 to 6,224 MB, a heap of 768 to 896 MB, a render-target pool of 1,276 MB and a budget falling from 9,427 to 5,771 MB.
- Mafia's 128 m and 32 m grids and 78.5 uses per mesh, and the 14.7 against 10.25 m street widths (Study 4).
- From Study 12: freezing after 3 s unseen beyond 70 m, props casting shadows to a quarter distance, vertex-animated set-piece crowds, and the scale test as KCD2's idea (Study 12 line 77).
- The table's sums (5,534 and 5,650).

Unsupported or overstated:
- "Render targets (includes 256 MB shadow pages, by arithmetic [S])": the reading says the page's texel format was not read, so no MB per page is stated. The arithmetic rests on source lines the reading never records.
- "Streamed textures ... ceiling 1,000, mark: textures' 2,000 from Mafia": the mark does not explain the 1,000. Mafia's level for a 6 GB card is 1,500 (Study 12).
- "Strand-haired people at once: 8 ... Kingdom Come II's 70": KCD2's 70 means full detail, not strand hair.
- Section 4 takes LAUNCH-PEAK's "Windows' counter ... never showed in the game's figure" as settled. REHEARSAL-2026-11-07-D line 15 records that this conflicts with the diagnosis (private memory moves too). The conflict is not stated.

**Unverified and unreached.** These are handled well: the 5.4 version mark, the 2.3 GB per person (snippet), UE-305620, TechSpot (403), the empty Epic pages, the possibly overlapping columns.

**Lean.** Yes. There is no new tool, it reports and never fails, and it takes three runs only when a reading crosses the line. Step 3 notes "nothing is multiplied" but leaves the session to rule on it. A test-only switch does not obviously break his rule, but the reading belongs in DECISIONS.md with its reason.

Fixes:
- Record the VSM page format and the source lines behind the 256 MB, or mark the figure unverified.
- Explain the streamed-texture ceiling of 1,000 against Mafia's 1,500 for a 6 GB card.
- Say "full detail", not "strand-haired", for KCD2's 70.
- State REHEARSAL-D's conflict with LAUNCH-PEAK in section 4.
- Record the scale test's reading of "nothing is multiplied" in DECISIONS.md.

## Across the three

The QA memory line and the memory plan should share one measure (the per-frame peak at High) and one line. No fetched text contained instructions, since nothing was fetched.
