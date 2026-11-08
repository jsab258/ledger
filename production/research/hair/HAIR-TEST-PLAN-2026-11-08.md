# Hair: cards against strands, the test plan for 9 November 2026 (n09-7)

Written 8 Nov; nothing run. All sources below read 8 Nov 2026. Reference first: Mafia ships strands with card meshes (a hybrid), Kingdom Come II cards (figures unverified) (studies/06-characters-wardrobe.md, lines 87-90); the scan reads cards at play distance, strands only in talk close-ups, measured on the RX 6700 (field-scans/HAIR-2026-11-08.md, section 5). Every run is on the packaged copy, at High, and is a comparison, not a pass (launch_line_check will read TEST; packaged-walk skill, step 9).

## Variants

| | What | Set by |
|---|---|---|
| A | Strands as shipped: face LOD0 strands, LOD1 cards, LOD2 meshes (hair map 1,3,5,7); facial hair kept on strands to LOD1 | Blueprint LODSync (MOUSTACHE-LOD-2026-11-02.md, section 1); CrimeProbe.cpp 1067-1087; DefaultEngine.ini 104 (`r.HairStrands.Voxelization.DensityScale.Shadow=0`) |
| B | Cards at every distance | `-dpcvars=r.SkeletalMeshLODBias=1` (HAIR-CARDS-VS-STRANDS-2026-11-06.md, item 2). Not `r.HairStrands.UseCardsInsteadOfStrands 1`: everyone bald (same note, item 1). The bias also drops faces, bodies and clothes one level, so B's frame cost reads low; read the hair passes, not the frame total |
| C | Hybrid: B everywhere except the person spoken to, held at LOD0 (strands) | The talk's `ForcedLOD 0` (LedgerTalkLight.h 21-23, 87-92). C's close-up is A's; C's play distance is B's. No own run; shipping it would need a hair-only map change like CrimeProbe.cpp 1071-1087 (not made tomorrow) |

## Views kept from the 3 Nov ruling, and what is left

Kept: Tom's camera from behind (the crown), by day and indoors at night under lamps; the talk close-up by day (about 1 m); the 3.1 m camera distance. Left for the full gate (RULINGS.md, "3 Nov, hair"): 10 and 25 m (all three variants draw cards or meshes there, so they do not decide), overcast, by a window, the street at night and wet, side-on walking, sitting, shimmer while walking and turning, shadows on wall, collar and neck, period photographs, the packaged walk, his look. Night talk: no switch reaches it (06 Nov note, Views table); left.

## Measures

- **Frame cost, the corner's crowd: already answered, not rerun.** 6 Nov, hook camera, 1,200 frames, no voice, High: frame median 15.17/15.12 ms strands, 15.13/15.13 forced cards, 15.12/15.17 level 1; the "people (hair and skin)" passes 0.29 day, 0.21 night in all three (runs.jsonl lines 352-363). Hair is under 0.3 ms there.
- **Frame cost, one person close: new.** -FaceAB runs (below) with `-csvGpuStats` and the CSV started from the launch line (`-ExecCmds="scalability 2,csvprofile start"`; whether the CSV is written when -FaceAB closes the game is unverified, check the file first); read with `python tools/perf-hook.py CSV --label NAME`, columns HairStrands, HairGuideInterpolation, HairCardsInterpolation (perf-hook.py lines 25-35). No CSV: one person's cost stays unread and is named, as on 6 Nov.
- **Colour hand-over.** Median sRGB patches (crown, side, moustache) with the cheek ratio for equal exposure, as HAIR-NEAR-DARK-2026-11-07.md's table. The known fault stands: strands to cards turns Ron, Sam and Lena grey or light (06 Nov, item 2); two tries are spent (DefaultEngine.ini 105-106; HAIR-NEAR-DARK, 19:15), so tomorrow only measures. New: cards to meshes (bias 2 run), which B would show at its first switch. Screen, the plan's own (unsourced): more than about 10 sRGB levels on a patch is a change; a fresh reviewer judges.
- **The crown.** Tom's crown median grey at his camera, method of F:/LedgerTools/gate/work/hair-crown; target band 79-99; now day 111, night about 120 with the scalp paint (DECISIONS 3 Nov 11:59). Strands are what he draws there: the shadow scale moved the crown 140 to 79 (DECISIONS 3 Nov 10:39), and that scale reaches strands only (HAIR-SHADOW-2026-11-02.md, section 1). Cards cast as geometry, with no voxel pass (same, lines 9, 21). By day his hair read the same at level 1 (06 Nov, item 4); office and night untested.

## Runs, in order (about 95 minutes)

0. Checks (10 min): `python tools/retention.py space --job "hair test" --drives CF`; no Runner.Worker; outside 15 minutes before 01:30, 03:30, 04:15; `python tools/close_games.py --dry-run`; the played copy's build commit (packaged-walk skill, steps 2 and 5).
1. A, Tom's camera (12 min, three runs): `-OfficeLook -OfficeLookHere` (street, day), `-OfficeLook` (office day), `-OfficeLook -OfficeLookNight` (CrimeProbe.cpp 9774-9778), each with the street's switches `-LedgerSlice -LedgerCrime -Encounter=live -LiveFresh -TalkFake -NoTitle` and `-ExecCmds="scalability 2"` (gate skill, step 2).
2. B, the same three with `-dpcvars=r.SkeletalMeshLODBias=1` (12 min).
3. A, close-up with cost (10 min): `-FaceAB -MouthFilm -PreparedAck` (06 Nov note; MEMORY faceab-needs-preparedack) plus the CSV switches.
4. B, the same with bias 1 (10 min). The 6 Nov close-up cards pictures are the look's fallback.
5. Bias 2, the same (10 min): the meshes level close, for cards to meshes.
6. Measures and two fresh reviewers, Tom's camera pair and the close-up pair, each beside the 6 Nov pictures (30 min).

## Decision

| Result | Recommendation on his page |
|---|---|
| B's close-up has no new fault (card edges, clumps, bald or helmet look) and B's crown is in 79-99 or below A's | Cards everywhere (B): no strand-to-card switch, the crown's voxel cause gone, cheapest |
| B fails close, passes at Tom's camera (crown at or below A, no new fault) | Hybrid (C), saying it carries the colour switch at each talk's start until the card colour is mended: a third try (lever 1, card values at spawn, about 2 hours, HAIR-NEAR-DARK section 3) needs his yes |
| B fails at Tom's camera too | Strands as shipped (A); crown and hand-over stay listed known faults |
| Any variant's hair passes over about 1 ms for one person, or the GPU median over 14.0 ms | The cheaper variant among those passing the look (14.0 ms line: perf-hook.py line 24; no hair budget exists in the notes) |
| The CSV is not written | Decide on look and the crowd's figures; one person's cost listed as unread |

Unverified: whether ForcedLOD 0 overrides the bias in a real talk (C's talk is taken as A's); KCD2 figures; the patch threshold.
