# Review of START-CHOOSER-2026-10-29.md (29 October 2026)

**Verdict: PASS WITH FIXES.** The asset readings and engine citations are almost all right. The direction (the sample's own search before planning his steps) is supported. But the check, as written, cannot pass while step 5, the approach line and the walk-in test stay as they are, and the cost leaves out the measuring the check needs.

**How it was checked.** The cited .uasset files were read again by a fresh reader of the package's name, import and export tables and tagged properties. Every cited header and line under UE_5.8 was opened. clip_sheet.json, seats.json and Saved/Logs/sit-approach-10.log (28 Oct, 23:51) were read. Each web page was fetched.

**Confirmed (no change):**
- Chooser context order, outputs Write; the five angle ranges.
- Pose Match settings (brute force, unmirrored, bias 0, range 0–0, end exclusion 0); its internal database and schema.
- Schema channels, weights, MaxDistance 50.
- CostThreshold 1.0; distance limit 300; the quoted comments.
- Notifies from 2.258–3.667 s; warp windows to 3.10–5.17 s; F_Lfoot's ratios and blend-out.
- Travel left 4.18–5.15 m and 32–68 cm.
- Every header line; the proxy entry; the "PoseHistory" tag.
- The patent; the warping, chooser and sample pages.

**Could not check from the bytes:** the Blueprint wiring, and which sign of TargetAngle means left in the sample. **Not reached:** Epic's 5.8 sample blog (403), and its gamedev.net copy (403).

## Faults

1. **"past a 'Minimum Velocity Check' of 100."** 100 is only the task's class default. The player's tree, ST_Player_SandboxCharacter_SmartObject, sets it to **0.0** in the same task instance that sets CostThreshold 1.0. *Correction:* "the player's tree sets the check to 0 (the task's default is 100)". Drop "the meaning of the velocity check" from Unverified.

2. **"ease-in-out" (the warp) and "0.25 s … linear" (the blend-in).** Both were read from F_Lfoot, which is not a kept entry.
   - F_Lfoot's along-travel warp curve is unset, which means the engine's default, FromRootMotionTranslation (RootMotionModifier_PrecomputedWarp.h:29). Other clips use Linear or EaseIn.
   - The kept BR montages save no blend option, so they blend with HermiteCubic (AlphaBlend.h:33, 223). R_090_Rfoot blends Linear. All are 0.25 s.

   *Correction:* give the kept clips' own curves.

3. **"plants of the same foot fall 150 to 170 cm apart (M)."** Re-counted from clip_sheet.json: 150–173 cm on the straight walk. The kept behind-right clips also show gaps of 118–137 cm before their notify, and F_Lfoot one of 209 cm. *Correction:* "mostly 150–170 cm; 118–137 in the behind clips".

4. **Distance matching "(page, and AnimDistanceMatchingLibrary.h:17–18, 37) … 'common to … use techniques such as Stride Warping to make up the difference.'"** The 5.8 page has neither the sentence nor the 0.75–1.25 clamp. Both are only in the header. *Correction:* cite the header alone.

5. **"Keep step 5, the approach line and the fallback as they are" against "at least 8 of 9 started by the search."** In the last run (sit-approach-10.log) only 5 of the 9 walk-ins reached the start search:
   - two took "no seat taken": the test began where no seat was in reach;
   - two took "fallback: no room to join the path": the door end's behind-right entries, as the order's own line also says.

   Kept as designed, at most 5 of 9 can be started by the search. *Correction:* either change the test's start places and the door end's join (and cost that), or set the target on walk-ins that reach the line (for example 5 of 5, and at most 1 fallback among them), stating which.

6. **"Where only one foot was kept, about half the matches are lost (I)."** This is understated, and not tied to the seats.
   - seats.json keeps only R_090_Rfoot for the middle and counter-end seats. All 5 walk-ins that reached the line used it.
   - With one clip, the ±50 cm band can shift his step phase by only about ±0.3 of a cycle (50 of 150–170 cm). As he walks in, his stride and the clip's advance together, so the offset barely changes (I). A walk-in therefore matches or never does: per walk-in, not per frame.
   - The Pose Match column returns only its single best row (MaxNumberOfResults = 1, PoseSearchChooserColumn.h:165). So an unkept R_090_Lfoot that scores better hides a kept match under 1.0, and the frame is refused.
   - The same arithmetic undercuts "That covers more than a gait cycle" in section 1: one clip's 100 cm band is about 0.6 of a cycle. Only both feet together cover more than one.

   *Correction:* name this as the main risk. Either room-test the other foot of R_090, or lower the target for one-foot seats.

7. **The check's numbers "planted-foot slide no more than 3 cm … attach bone within 2 cm and 3 degrees … hips within 5 cm, ±3 cm … no room contact deeper than 1 cm", and "9 more at a slower walk".** -TomSitApproachTest prints only cases, started, fallbacks, sat and heading (SliceCharacter.cpp:1874), plus step 6's start line. Elsewhere:
   - foot slide at a sit is measured nowhere;
   - the attach offset only in -TomSitEntryTest, with the warp off (2167–2170);
   - the hips only in -TomSitProof, to 10 cm and 40–60 cm (2179);
   - contact only in -TomSitRoomTest.

   The test always pushes at full input (speed 200), so there is no slower walk to choose. *Correction:* the check is measurable only after these measures and a walk-speed switch are added to the approach test. Say so, and cost it. SPOTS item F (0.5 h) was for -TomSitProof and is not done.

8. **"About 6.5 hours, likely 5 to 9."** Plausible for the C++ call alone. It omits:
   - the measures and speed switch in fault 7 (about 1 to 1.5 h);
   - any work on the four walk-ins that never reach the search (fault 5; at least 1 h if done).

   Its "Packaged run, 1.0" also overlaps SPOTS item H. *Correction:* about 8 to 11 h for the check as written, or keep 6.5 h and narrow the check.

9. **"while his distance to the slot lies inside the room-tested band."** The band (100 and 150 cm) is root travel left to the root's end (MomentWithLeft, SliceCharacter.cpp:1440–1450). TargetDistance and the database are root to attach (PoseSearchFeatureChannel_Distance.cpp:182–191), and the attach bone ends 20 cm from the root. The two measures differ by about 3 cm (R_090 starts) up to 20 cm (front clips). *Correction:* convert the band per clip, or gate on travel left.

10. **Unverified, incomplete.** Add:
    - that the widened ±50 cm room test keeps any entry at all: every entry already touched the room from 200 cm, and the new 50 cm edge is untried;
    - the single-best masking (fault 6);
    - the walk-ins that never reach the line (fault 5).

## The recommendation

The evidence supports trying the sample's search before planning his steps:
- Tom's mover is the sample's own SandboxCharacter_CMC, with its own graph and pose history, so the cost scale and the 1.0 threshold carry over.
- The second direction needs stride control. The sample's graph has none (no stride-warping node in SandboxCharacter_CMC_ABP).

The design stands once faults 5 to 10 change its target, its check and its cost.
