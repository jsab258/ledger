# People alive, standing and walking: first-pass reading (7 November 2026)

First-pass notes for the faults: Tom treading on the spot at a shop front, foot sliding, stiff standing poses, a walker's turn at a pause. No synthesis, no recommendation. All outside pages read 7 Nov 2026 unless marked HOME (read earlier by the project; not re-read). Anything not read in full is marked unverified.

## What home already answers (do not re-read)

- Study 7, production/research/aaa-reference/studies/07-animation.md (25 Oct): neither Mafia nor Kingdom Come II uses motion matching. Both choose starts, stops and turns from tables: KCD2 picks a stop by remaining distance (0.6 to 2.1 m), travel angle and stride quarter, left and right foot versions, and turn blend spaces at 45/90/135/180 degrees. Mafia has per-set 12 starts, 6 stops, 4 idle turns, 2 pivots, civilians get only two-bone leg IK, the ground trace rig stops beyond the near LOD. KCD2 has no crowd animation system. Gives Epic's 223 walking clips, 134 with a flat foot travelling over 3 cm. Pose-search foot-slide perception figure (21 mm) is unverified (snippet).
- Study 1, studies/01-npc-life.md: Mafia civilians pause look-at beyond 32 m, simplify from 10 m, freeze unseen beyond 70 m; KCD2 full detail for 70 people within 150 m.
- natural-idles/NOTE.md (1 Oct): Witcher 3 pool of 35 idles per skeleton type (read at gameanim.com); vendor rules of thumb (MoCap Online guides, 11 Apr and 17 Mar 2026): base idle loop 8 to 12 s with a weight shift, breaks every 30 to 60 s, breathing additive 1 to 2 cm at 15 to 20 breaths a minute, 4+ base idles per sex (5 to 8 per archetype, little gain above 12), play rate 0.9 to 1.1, random start, mirrored copy counts as variation. Suspect list for the stiff stance (shared Technical_Loops idle, head and neck held 70% toward bind rotation). GASP's idle breaks come from a state machine plus Chooser table (Epic forum, Apr 2025). RandomPlayer node fields.
- sit-and-turn/TOM-MOTION-MATCHING-2026-10-22.md and WALK-2026-10-25.md: the sample's own graph (blend 0.5 s, play rate 0.85 to 1.15, Offset Root Bone max 30 cm, half-life 0.3 s moving and 0.1 s idle, chooser rules, turn in place only when the body is 50 degrees off and the speed is low, Foot Placement plant threshold 1 on the contact curve), Tom's measured slides, two tries and a third (stop chosen the KCD2 way).
- Not found at home: anything on treading on the spot against an obstacle, a turn at a pause, or look-at limits.

## (4) Treading on the spot against an obstacle (new)

- Epic forum, "Motion Matching Mesh ignores Walls", UE 5.4.1, thread Jan to Jun 2025, https://forums.unrealengine.com/t/motion-matching-mesh-ignores-walls/2264940 (read in full 7 Nov 2026): the capsule collides, the animated bones pass through the wall; one poster calls it a known issue in 5.5 (community claim, no Epic staff reply, unverified). Workarounds named: a larger capsule, mesh collision (called glitchy; neither worked for the poster), turning root motion off (loses turning), a line-trace "braking" system the last poster built. Unresolved at last post.
- Orange Duck (Daniel Holden), "Code vs Data Driven Displacement", https://theorangeduck.com/page/code-vs-data-driven-displacement (read 7 Nov 2026; undated on the page): when a simulated body and the animated character drift apart, options are doing nothing, synchronising, damped adjustment, velocity-limited adjustment (example cap 0.5 of character velocity), clamping. Unlimited adjustment still slides feet when standing or planting and turning. It states walk animations look worse pushed against walls and foot locking cannot fix it. Pushing against a clamp feels "dragged along".
- Research paper, arXiv 2510.22632v1, posted 26 Oct 2025, https://arxiv.org/html/2510.22632v1 (read 100,000 of 117,418 characters; last 17,000 unread): motion matching with obstacle features added to the pose query. A 36-dimension feature vector (27 query, 9 environment), search every 10 frames at 60 Hz, 184,553 poses, about 50 MB. In a dense cone field: standard motion matching 0.22 ms search, 0.88 s collision time; the method 0.80 ms and 0.08 s. Characters slow, turn the torso, sidestep (0.35 m corridor) or step back. Research result, not a shipped game's practice.
- A search for a fix for "walk in place at an obstacle" found only the above and unrelated product forums (Reallusion, Godot). No studio write-up of the exact symptom was found. The question is open from outside sources.

## (4) Foot contact, locking, stride warping, slide correction

- Epic Python API, FootPlacementPlantSettings (5.7), https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/FootPlacementPlantSettings?application_version=5.7 (read 7 Nov 2026): a bone is planted below speed_threshold read from a speed curve; unalignment_speed_threshold is where it is fully released, and the gap should roughly match the foot's roll phase; unplant_radius is the linear drift that releases the lock, replant_radius_ratio is the fraction of that at which it replants; unplant_angle and replant_angle_ratio likewise; separating_distance keeps feet apart. No defaults and no tuning advice on the page.
- AnimNode_FootPlacement (5.7), https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/AnimNode_FootPlacement?application_version=5.7 (read 7 Nov 2026): plant speed mode Graph uses the animation's root-motion speed, Manual uses a per-foot curve. lod_threshold: the node stops above that LOD (default 0), with transitions noted as needing revisiting.
- AnimNode_StrideWarping (5.7), https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/AnimNode_StrideWarping?application_version=5.7 (read 7 Nov 2026): stride scale = locomotion speed divided by the clip's root-motion speed; min_root_motion_speed_threshold stops warping at starts and stops; pelvis pulled down toward IK feet; IK clamped by FK limits. No default ranges.
- Epic's Motion Matching page, https://dev.epicgames.com/documentation/en-us/unreal-engine/motion-matching-in-unreal-engine (read 7 Nov 2026): cost = sum of channel costs; fewest trajectory samples possible; Search Throttle Time; Continuing Pose and Looping cost biases; "Block Transition" tags; Normalization Sets; notify filter 0.2 s default; montages not supported in animation blueprints; no budget numbers and no mention of obstacle stalls.
- Epic's Motion Warping page, https://dev.epicgames.com/documentation/en-us/unreal-engine/motion-warping-in-unreal-engine (read 7 Nov 2026): warps a montage's root motion to a named target over a notify window (scale or skew, rotation optional). No guidance on obstacles, minimum or maximum warp distance.
- Foot placement and stride warping user-guide pages returned empty text; Foot Placement guidance beyond the API lists is unreached.

## (5) Starts, stops, turns on the spot

- Epic's GASP page, https://dev.epicgames.com/documentation/en-us/unreal-engine/game-animation-sample-project-in-unreal-engine (read 7 Nov 2026): turn in place triggers when the root differs from the capsule by over 50 degrees (while aiming), and plays after a stop ("stick flick"); the page calls aiming turn-in-place work in progress. Start detected when future velocity exceeds current; disabled during pivot databases. Root translation offset released when stopped. Leg IK pins feet to IK bones that warping moves.
- KCD2 and Mafia tables: see HOME above. Nothing new found from outside on turns at a pause; the Clavet GDC 2016 talk (https://www.gdcvault.com/play/1022985/Motion-Matching-and-The-Road) is behind the Vault sign-in; unreached (only secondary summaries: per-frame brute-force search of all mocap).

## (3) Looking around

- Epic 5.8 GASP blog (3 Aug to 12 Aug 2026 per HOME note), https://www.unrealengine.com/tech-blog/download-the-latest-game-animation-sample-project-now-updated-for-ue-5-8: refused with 403 today. Through search results only (unverified, secondary summary): an Experimental additive Look-At point-of-interest solver in Control Rig, nondestructive, per-body-part reaction, test samples for locomotion, acting gestures and an NPC patrol. Its parameters were not reached.
- GASP docs page (above): only an aim offset (camera direction, dead blending on reset); no NPC look-at.
- Witcher 3, https://www.gameanim.com/2016/03/23/cinematic-dialogue-witcher-3/ (read 7 Nov 2026; article 23 Mar 2016): pose-based look-ats hand-authored for special idles (sitting, leaning), each blending between 3 poses; look-ats cover whole body, head only or eyes only.
- Limits and timing: only tutorials and vendor documents found (search summary only, unverified): eyes about 30 degrees horizontal and 20 vertical; a sample with head limits of 60 yaw and 30 pitch; eyes take the remainder after the head turns; look-at weight faded to zero for targets nearly sideways; temporal smoothing against snapping. No studio source on eye-leads-head timing. Mafia civilians pause look-at beyond 32 m (HOME).

## (1) and (2) Idle variety, weight shifts

- Numbers are HOME only: Witcher 3's 35 per type; vendor figures above (all vendor rules of thumb, not studio data). GASP clip counts: a third party counts 45 idles, 33 poses, 11 look-at clips of about 1,800 (HOME, third party's counts). Epic's docs page gives no idle counts.
- KCD2 gesture table 4,183 entries in 344 families, median 2.9 s (HOME, Study 7).
- No new studio source on idle length, choice or weight shifts found today. The Naughty Dog GDC 2021 NPC talk (Last of Us Part II) was reached only as titles and a short preview (https://www.gamedeveloper.com/design/learn-about-the-character-technology-of-i-the-last-of-us-part-ii-s-i-npcs-at-gdc-2021, read 7 Nov 2026); the slides (about 3.8 GB) were not fetched.

## (6) Crowd cost, cut with distance

- Animation Budget Allocator, https://dev.epicgames.com/documentation/en-us/unreal-engine/animation-budget-allocator-in-unreal-engine (read 7 Nov 2026): default 1.0 ms game-thread budget (1.0, 1.5, 2.0, 2.5 ms across four scalability levels); ranked by significance; default max tick rate 10; interpolation (16 components, rate 6); skips optional work ("Lo"); off-screen ticks capped at 4. No distance values.
- Animation optimisation page, https://dev.epicgames.com/documentation/en-us/unreal-engine/animation-optimization-in-unreal-engine (read 7 Nov 2026): update rate at 15 Hz and under at distance, no thresholds.
- MetaHuman crowds, https://dev.epicgames.com/documentation/metahuman/create-metahuman-crowds-in-unreal-engine (read 7 Nov 2026): close full actors with animation blueprints, distant instanced meshes with baked GPU animation, then not rendered; example 10 full actors and hundreds of instanced; thresholds unstated; timing variety to avoid lockstep.
- Foot Placement node stops above a chosen LOD (above). KCD2, Mafia: HOME.

## (7) Published clip counts and budgets

Only: Witcher 3 35 idles per type and about 2,400 dialogue animations; KCD2 gesture table; Mafia and KCD2 counts in Study 7; MoCap Online ranges (vendor); GASP counts by a third party; Epic's 1.0 ms animation budget default. No studio published a budget for idle clips per street.

## Unreached or unverified

- GDC Vault talks (Clavet 2016, Naughty Dog 2021): sign-in wall or slides not fetched.
- Epic tech blogs (5.7, 5.8): 403 today.
- Epic Foot Placement and Stride Warping user guides, Mass crowd docs: empty text.
- Look-at limits: no primary source.
- The "known issue fixed in 5.6" claim for the wall problem: unconfirmed.
- Remaining 17,000 characters of the arXiv paper.
