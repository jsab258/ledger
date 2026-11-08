# Hair: cards against strands, the result (n09-7), 8 November 2026

Run 22:28 to 22:50 Swiss, packaged copy 5ed8f38 (nightly of wip 91f82ea5), High, by HAIR-TEST-PLAN-2026-11-08.md. Pictures, films, profiles, logs and both reviews: F:/LedgerTools/gate/new/hair-test-2026-11-08/ (about 520 MB). Comparison runs, not passes (test switches).

## What ran

- Tom's camera, six runs: A strands as shipped and B cards (`-dpcvars=r.SkeletalMeshLODBias=1`, confirmed in each B log: "Value remains '1'"), street by day, office by day, office at night (tools/office_look.py, `--here`, plain, `--night`).
- Talk close-ups, three runs: A, B and M (bias 2, the meshes level), `-FaceAB -MouthFilm -PreparedAck -csvGpuStats -ExecCmds="scalability 2,csvprofile start"`; each closed itself in 148 s, 68 to 69 film frames, one CSV each. Ron, Sam and Lena (the -FaceAB cast); Tom has no close-up switch.

## Measures

| | A strands | B cards | M meshes |
|---|---|---|---|
| Tom's crown median grey, street day | 28 | 21 | - |
| office day (band 79-99) | 115 | 79 | - |
| office night | 124 | 90 | - |
| Hair passes, one person close (ms) | 0.16 | 0.25 | 0.24 |
| GPU median close (ms) | 14.17 | 12.89 | 12.71 |
| Card memory median close (MB) | 5,639 | 5,194 | 5,186 |

The crown box was checked on the 3 Nov picture: 110 against the 111 recorded then. The CSV runs differ in length (52, 257, 530 frames: the profile is cut when -FaceAB closes the game at differing points), so A's frame and memory figures are thin; hair is under 0.3 ms in every variant, as in the crowd on 6 Nov. B's 0.45 GB lower memory includes faces, bodies and clothes one level down, not hair alone (n09-3's hair voxel texture stays a separate question).

## Reviews (two fresh reviewers)

- Tom's camera (review-camera.json): **B new faults.** A flat orange-brown patch on the crown with no strand detail (helmet look, 4), hard-edged white blotches across the crown (pixels over 200: day 2.0 to 4.9%, night 5.7 to 7.1%; 4), a hard scalloped nape edge in the street (2). B reaches the band only through the dark patch. Crown numbers confirmed.
- Talk close-ups (review-close.json): **B and M not usable close.** Cheek-normalised A to B: Ron crown +39, side +71 (grey); Sam crown +24, side +88 (light brown); Lena side +27, grey to the eye; Lena's hair flat grey ribbons (4), a pale card edge at her right temple (3), stiff spikes above Ron's crown (2). M: painted helmets (5), Ron's moustache ginger, Sam's stubble gone with the face level (4). Caveat: the runs are not in step frame for frame.

## Decision (the plan's table, row 3)

B fails at Tom's camera too, so: **strands as shipped (A)**. Tom's crown and the strands-to-cards colour hand-over stay listed known faults. The hybrid (C) is not recommended: B's faults show at Tom's 3.1 m camera, which C would draw with cards. The hair gate (RULINGS 3 Nov) stays open; this decides the method, not a pass.

## Unread or left

10 and 25 m, overcast, window, street at night and wet, side-on walking, sitting, shimmer, shadows, period photographs, his look (left for the full gate, as the plan says). Tom close: no switch. Whether ForcedLOD 0 overrides the bias in a real talk.
