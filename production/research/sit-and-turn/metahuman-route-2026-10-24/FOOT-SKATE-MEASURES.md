# Foot skate: how research and games measure it, and what they accept (24 October 2026)

This answers direction C of METAHUMAN-ROUTE-2026-10-24.md: how the field measures foot sliding, and whether the route's 3 cm bar matches it. Every source was read on 24 October 2026. Nothing was run. Source numbers [F1]... are listed at the end. "Full" means the whole text was read. "Fetch" means the page was read through the web tool's extract, so quotes were checked against that extract, not the original layout.

## The questions (written before reading)

1. How do published methods define foot contact (height, speed, heel and toe apart, labels from the data), with the numbers they use?
2. How do they define and report foot skate (mean speed in contact, total drift, a ratio, a height-weighted speed), with formulas and typical values for motion matching and learned methods?
3. Do studios or Epic publish a slide tolerance? How are feet released at stops and pivots? Are scuffs, shuffles and pivots treated as intended?
4. Does a 3 cm worst-case bar at every start, stop and turn match how the field judges sliding?

## 1. Foot contact: how it is defined

**Short answer.** Almost everyone calls a foot "in contact" only when it is slow, and usually also low. Heel and toe (or ball) are treated apart. No two sources use the same numbers, and the authors say plain thresholds get about 90% of contacts right, so data is checked by hand.

| Source | Joint(s) | Speed test | Height test | Other |
|---|---|---|---|---|
| Kovar 2002 [F1] | heel and ball, each on its own | automatic detection, then edited by hand | none given | no numbers given |
| PFNN 2017 [F2] | heel and toe, each on its own | speed below an unstated threshold | none | checked and corrected by hand |
| HumanML3D labels, used by MDM [F9, F10] | ankle and foot joints | squared per-frame move < 0.002 m² (about 4.5 cm a frame, about 0.9 m/s at 20 fps) | a height factor is defined, but MDM's copy does not use it | |
| Holden's motion-matching demo, the companion code to Learned Motion Matching [F18] | toes | below 0.15 (m/s, inferred from the code) | none | 6-frame median filter |
| Holden's 2026 foot-locking article [F19] | toe (only the toe is locked; the heel is left free) | 0.1 to 0.5 m/s suggested | under 0.1 m | 5-frame median at 60 Hz; heuristics get about 90% right; hand labels are the only gold standard |
| Unity motion-matching paper 2023 [F21] | toes | near zero, no number given | none | median filter, radius 6 |
| UnderPressure 2022 [F3] | heel and toe | none (pressure insoles) | none | over 5% of body weight on the zone; foot over 10%; contacts under 0.1 s dropped |
| Epic Foot Placement node [F23, F24] | plant bone = ankle; speed read at the ball | ball speed < 60 cm/s (default), or a speed curve | < 10 cm from the plant plane (default) | both tests must pass |
| Epic retargeter Speed Planting [F25] | ball speed curves | example 30, set just above the speed curve's flat part | none | |

Points that matter for the route:
- **Speed is the main test everywhere a contact is labelled.** A foot dragged low but fast is "not in contact" in PFNN, HumanML3D, Holden, Unity and Epic's node.
- **Height-only contact appears only inside skate metrics** (section 2). These treat any low foot as "should be still" and then score its movement.
- **Heel and ball are separate.** Kovar plants the heel, the ball or both [F1]. UnderPressure adds contact points under the foot so the foot can rotate about them [F3]. Epic's default lock pivots around the ball [F23].
- **Kovar names two cases with no clear footplants**: a runner skidding to a halt, and a dancer shuffling. There automatic detection is unreliable and constraints are hand-edited [F1].
- **Fixed thresholds do not fit every motion.** UnderPressure: they must be tuned per motion type, body and contact zone [F3]. OmniControl dropped its skate ratio on KIT-ML because that dataset's real feet sit above zero and skate [F6].

## 2. Foot skate: how it is reported, with typical values

**Short answer.** Four families exist. All are averages or shares of frames, used to compare methods. None counts the worst drift of a single contact. Real motion capture scores above zero on most of them. No paper gives a pass mark.

**a. Mean horizontal foot speed while in contact.** UnderPressure measures skate this way and cites Starke 2019 (NSM), Starke 2020 (LMP), Zhang/Starke 2018 (MANN) and MVAE 2020 as doing the same [F3]. Its cleanup roughly halved that speed, and the gain was judged by eye [F3].

**b. Height-weighted speed (the MANN family).**
- Formula: skate = v × clamp(2 − 2^(h/H), 0, 1), averaged over frames.
  - v is the foot's horizontal speed (or move per frame), h its height, H a height limit.
  - The weight is 1 on the ground and falls to 0 at height H.
- Four later papers credit it to Zhang, Starke, Komura & Saito 2018 (MANN) [F11, F12, F13, F14]. MANN itself was not reached.
- Values:
  - **Tang 2022** [F11]: H = 2.5 cm, chosen because the real data itself skates. Real mocap 0.07 to 0.23; learned methods 0.10 to 1.19; plain interpolation up to 2.74. Units not stated.
  - **RSMT 2023** [F13]: H = 2.5. Real mocap 0.16 to 0.27; methods 0.17 to 1.29.
  - **MVAE 2020** [F14]: H = 3.3 cm. Real mocap 0.10 cm a frame; MVAE 0.07 to 0.44.
  - **TPTN 2023** [F12], 60 fps: H = the mean contact height in its data (10.85 cm foot, 1.55 cm toe).
    - Real mocap 0.18 to 0.27 cm a frame (about 11 to 16 cm/s, weighted and averaged over all frames).
    - PFNN 0.35, Neural Animation Layering 0.35, MVAE 0.48 to 0.53.

**c. Share of frames that skid (the GMD ratio, used by MDM's follow-ups).**
- Definition: the share of frames where either foot is below 5 cm in two adjacent frames and moves more than 2.5 cm in a frame [F4, F6].
- In GMD's code [F5]: 20 fps, a speed over 0.50 m/s both in the frame and over a 5-frame average. That is 2.5 cm a frame. The code's comment gives 20 cm/s, which the value does not match.
- Values on HumanML3D [F6]: real data 0.000; MDM 0.10; PriorMDM 0.09; GMD 0.10; OmniControl 0.05 to 0.09. GMD's own tables, across settings: MDM 0.09 to 0.31, GMD 0.09 to 0.27 [F4].
- What it misses: a foot creeping at 40 cm/s for half a second drifts 20 cm and is never counted.

**d. Mean move per frame while in contact (PhysDiff).**
- Definition: foot joints touching the ground in two adjacent frames; their average horizontal move, in mm [F7]. The contact height is not stated in the text read.
- Values: MDM 1.4 mm; MotionDiffuse 3.9; PhysDiff 0.4 to 0.5 [F7].

**Others.** MDM adds a training penalty on foot speed during contact frames, using the HumanML3D labels. It reports no skate figure [F8]. GAMMA scores contact with a 0.05 m height and a 0.075 m/s speed limit [F15]. The 2023 survey of human motion generation says there is no standard metric: settings and methods differ from paper to paper [F16].

**Motion matching and PFNN.** PFNN fixes feet at run time with two-joint IK using its contact labels, and reports no skate number [F2]. Holden's motion-matching demo locks the toes and reports no number [F18]. The Unity motion-matching paper reports none either. It says only that position correction is kept small so users do not notice the sliding it adds [F21].

## 3. Studios and Epic: tolerances, release, pivots and scuffs

**Short answer.** No studio or Epic source read gives a slide tolerance. They publish lock settings instead: how far the animation may pull away before a locked foot is let go. These are 20 to 40 cm. Practitioners say a little sliding beats a broken pose.

**Epic's Foot Placement node** (installed UE 5.8 header and source [F23]; API page [F24]):
- **When it plants:** ball speed under the Speed Threshold (60 cm/s by default) and within the Distance To Ground (10 cm by default) of the plant plane.
- **When it lets go:**
  - when the held foot and the animated foot are more than the Unplant Radius apart, measured flat (35 cm by default);
  - or when the twist passes the Unplant Angle (45° by default).
  - It plants again inside Replant Radius Ratio × radius (0.35 by default), with springs blending in between.
- **Lock type:** by default the foot pivots around the ball (PivotAroundBall).
- **Built-in fallback:** past a horizontal foot offset of 10 cm (Max Offset Horizontal), the node first rolls the planted foot and then lets it slide.
- **The sample's own settings,** read in the game's editor today [F26]:
  - normal: 20 cm and 60°, pivoting on the ball;
  - for stop clips: Unplant Radius 40 cm and replant ratio 0.75.
  - So Epic does treat stops on their own, but by holding the lock longer, not by allowing more slide.
- **What Epic publishes about slide size:** no tolerance [F24, F25]. The retargeter page says only to set the plant threshold just above the flat part of the speed curve [F25].

**Holden (Ubisoft La Forge's motion-matching work, his own site)** [F18, F19, F20]:
- **How the lock works:**
  - It starts when a contact begins, at the toe's position.
  - It ends when the contact ends, or when the animation is more than the unlock radius away (0.2 m in his demo).
  - Then it blends out over a half-life of 0.1 s [F18]; his 2026 article uses inertialization [F19].
- **Heel and toe:** lock the toe and give the heel freedom. Pivoting on the toe with the heel up is common in real data [F19].
- **On pose versus slide:** rather than drop the hips into a crouch to keep a foot locked, he writes it is "almost always better to just let the feet slide" [F19]. He also says foot locking is hard to make look good [F20].
- **Judgement:** by side-by-side viewing, with no number [F19].
- **Correction:** limited to a share of the character's own speed (0.5 in his demo), so feet do not visibly slide while it stands [F20].

**Clavet, For Honor (GDC 2016), second-hand only** [F22]: a GameAnim write-up of the talk reports four points.
- Fast switching between clips always causes some foot sliding.
- The toe is locked at run time to a ground point taken from the animation.
- Clips should not be sped up more than about 10% or slowed more than about 20%.
- It is better to slide the character and use foot IK.

The slides were not reached.

**Scuffs, shuffles and pivots.**
- Pivots are handled as a ball (toe) plant with the heel free:
  - Kovar plants one point only, and the foot turns about it [F1];
  - Epic pivots around the ball by default [F23];
  - Holden frees the heel [F19].
- For scuffs and shuffles, no source read names a "scuff" step or calls it intended. The nearest is Kovar, who treats skids and shuffles as motions without clear plants [F1]. Unverified beyond that.

## 4. Does a 3 cm worst-case bar at every contact fit the field?

**Short answer: not as the field measures, though the size is defensible.** The research field compares methods by averages and frame shares, and has no pass/fail tolerance. Studios judge by eye, in the game, and accept small slides to keep the pose. Nobody measures the worst total drift of every contact.

The 3 cm size itself is in the right range for what people notice:
- **Watching:** viewers noticed foot sliding below 21 mm in most conditions of a 2011 study [F17]. Only the abstract was reached; the conditions are not known.
- **Walking:** gait-slip research counts a heel slip over 3 cm as a slip. Below that it is a "microslip" [F27, F28]. A 1991 study found walkers' detection of a slip changes at about 3 cm [F28].

Where the route's measure is stricter than everyone else's:
1. **It decides "planted" by height alone (within 2.5 cm).** Every contact-labelling method also requires the foot to be slow [F2, F9, F18, F19, F23].
   - So the stop's low scuff (a foot sliding about 45 cm, 1 to 3 cm off the ground [F26]) is a moving foot to the labellers and to Epic's lock.
   - The skate metrics (GMD, MANN family) would count it as skating, but only as a share or an average.
2. **It counts the worst contact, not the average.** Real motion capture itself scores above zero on the MANN-family measures [F11, F12, F13, F14]. A worst-case bar will fail some real human contacts. How many is unknown until the same measure is run on the raw source clips.
3. **It measures the ball only.** That matches the field's choice of plant point [F1, F19, F23]. But a pivot on the ball can still move the ball joint a little, since the foot turns about its contact patch below the joint. Inference, not measured.

What the field would add, as options (inference from the sources, not a decision; the bar is Jafar's):
- a contact test needing low and slow;
- the same measure run on the source animation, to tell authored scuffs from added slide;
- side-on review at the gameplay camera, beside the numbers.

## Sources (all read 24 October 2026)

| # | Link | How read | What it gives |
|---|---|---|---|
| F1 | https://research.cs.wisc.edu/graphics/Gallery/kovar.vol/Cleanup/cleanup.pdf | Full | Heel and ball plants, single or both; automatic detection then hand edits; skids and shuffles lack clear plants; blend windows 5 to 10 frames; no slide numbers. |
| F2 | https://theorangeduck.com/media/uploads/other_stuff/phasefunction.pdf | Full text searched; sections 4 and 6 read | Heel and toe contact by speed under an unstated threshold, hand-corrected; run-time two-joint IK; no skate metric. |
| F3 | https://arxiv.org/pdf/2208.04598 | Intro, related work, labels, evaluation, cleanup read | Heel and toe contacts from insoles (5% / 10% body weight, under 0.1 s dropped); thresholds about 90% right and need per-motion tuning; skate = mean horizontal foot speed in contact, citing NSM, LMP, MANN and MVAE; cleanup roughly halves it. |
| F4 | https://arxiv.org/pdf/2305.12577 | Metric section and Tables 1 to 3 | Skate ratio: foot below 5 cm, skid over 2.5 cm; MDM 0.09 to 0.31, GMD 0.09 to 0.27 across settings. |
| F5 | https://raw.githubusercontent.com/korrawe/guided-motion-diffusion/main/data_loaders/humanml/utils/metrics.py | Fetch | 20 fps; height under 0.05; speed over 0.50 instantaneous and over 5 frames; joints 10 and 11. |
| F6 | https://arxiv.org/pdf/2310.08580 | Table 1, sections 4 and A.8 to A.10 | Same ratio; real 0.000, MDM 0.1019, PriorMDM 0.0897, GMD 0.1009, OmniControl 0.0547 to 0.0874; KIT-ML not scored, its real feet skate. |
| F7 | https://ar5iv.labs.arxiv.org/html/2212.02500 | Fetch | Skate = mean horizontal move of foot joints in contact on adjacent frames, mm; MDM 1.406, MotionDiffuse 3.925, PhysDiff 0.42 to 0.51. |
| F8 | https://ar5iv.labs.arxiv.org/html/2209.14916 | Fetch | MDM's foot-contact training penalty from data labels; no skate metric reported. |
| F9 | https://raw.githubusercontent.com/EricGuo5513/HumanML3D/main/motion_representation.ipynb | Fetch | HumanML3D labels: threshold 0.002 on squared per-frame move; joints 7, 10 and 8, 11; 20 fps. |
| F10 | https://raw.githubusercontent.com/GuyTevet/motion-diffusion-model/main/data_loaders/humanml/scripts/motion_process.py | Fetch | Same detector; the height factor is defined but its test is commented out. |
| F11 | https://arxiv.org/pdf/2205.02540 | Metric section and Tables 1 to 7 | MANN-family formula, H = 2.5 cm, credited to Zhang et al. 2018; real mocap 0.07 to 0.23. |
| F12 | https://ar5iv.labs.arxiv.org/html/2304.12571 | Fetch | Eq. 13 with H 10.85 / 1.55 cm, credited to MANN [58]; cm a frame at 60 fps; real 0.18 to 0.27, PFNN 0.354, Neural Layering 0.351. |
| F13 | https://ar5iv.labs.arxiv.org/html/2306.11970 | Fetch | Same formula, H = 2.5, credited to Zhang 2018; real 0.16 to 0.27. |
| F14 | https://ar5iv.labs.arxiv.org/html/2103.14274 | Fetch | Same formula, H = 3.3 cm, credited to Zhang 2018; real mocap 0.10 cm a frame. |
| F15 | https://ar5iv.labs.arxiv.org/html/2112.09251 | Fetch | Contact score with 0.05 m and 0.075 m/s limits. |
| F16 | https://arxiv.org/pdf/2307.10894 | Section 8.1.3 | No standard physical-plausibility metric; thresholds differ by paper. |
| F17 | https://api.openalex.org/works/W2048301879 | Abstract only | Prazak, Hoyet & O'Sullivan, SCA 2011: footsliding below 21 mm noticed in most conditions; any cleanup preferred to none. |
| F18 | https://raw.githubusercontent.com/orangeduck/Motion-Matching/main/resources/generate_database.py and .../main/controller.cpp | Fetch | Toe contact under 0.15; median 6; unlock radius 0.2; blend half-life 0.1; foot height 0.02. |
| F19 | https://theorangeduck.com/page/inverse-kinematics-foot-locking (30 Jul 2026; author not named on the page) | Fetch | Toe lock, free heel; 0.1 to 0.5 m/s and 0.1 m thresholds; about 90%; lock and unlock by distance with inertialization; let feet slide rather than break the pose; judged by eye. |
| F20 | https://theorangeduck.com/page/code-vs-data-driven-displacement (23 Sep 2021) | Fetch | Correction capped at 0.5 of character speed; foot locking hard to make look good; some sliding beats bad posing. |
| F21 | https://ar5iv.labs.arxiv.org/html/2310.05215 | Fetch | Toe contact near zero speed; lock and unlock without numbers; no slide measure. |
| F22 | https://www.gameanim.com/?p=13538 (3 May 2016) | Fetch | Second-hand summary of Clavet's For Honor talk: toe locked to a ground point; 10% / 20% timescale limits; slide plus foot IK. |
| F23 | Installed UE 5.8: Plugins/Animation/AnimationWarping/.../AnimNode_FootPlacement.h lines 217 to 516 and .cpp lines 601 to 736, 1214 to 1226, 1535 to 1553 | Full for those parts | Defaults: 60 cm/s, 10 cm, 35 cm, 0.35, 45°, 0.5, PivotAroundBall, roll-then-slide past 10 cm. Plant and let-go tests are flat distance and twist. |
| F24 | https://dev.epicgames.com/documentation/unreal-engine/API/Plugins/AnimationWarpingRuntime/FFootPlacementPlantSettings | Fetch | The same settings as published; no defaults, no tolerance. |
| F25 | https://dev.epicgames.com/documentation/en-us/unreal-engine/fix-foot-sliding-with-ik-retargeter-in-unreal-engine | Fetch | Speed-plant threshold example 30, just above the curve's flat part; no tolerance. |
| F26 | ../METAHUMAN-ROUTE-2026-10-24.md and REVIEW.md (this folder) | Full | The sample's plant settings (20 cm / 60°; stops 40 cm / 0.75); the stop scuff (about 45 cm at 1 to 3 cm height). |
| F27 | https://pmc.ncbi.nlm.nih.gov/articles/PMC5987760 | Fetch | Iraqi et al. 2018, J Biomech: a slip is a slip distance over 3 cm, citing Leamon & Li 1990. |
| F28 | https://koreascience.kr/article/JAKO199111919571979.pub | Abstract | Son & Li 1991: walkers' slip detection changes at about 3 cm; the microslip/slip line is there. |

## Could not be reached

- **Clavet's GDC 2016 slides** (media.gdcvault.com PDF):
  - over the web tool's 10 MB limit;
  - the S3 copy refused (403); GDC Vault was in maintenance;
  - one try in the browser pane offered a file download instead. It was not retried.
- **Zadziuk's GDC 2016 slides:** refused (403).
- **Learned Motion Matching 2020 PDF** (Ubisoft): over 10 MB. Its companion code [F18] was read instead.
- **Starke's own papers:**
  - MANN 2018, NSM 2019, LMP 2020, Neural Animation Layering 2021 and DeepPhase 2022: the GitHub copies are over 10 MB, ACM refused (403), and the Edinburgh links have moved;
  - Starke 2023 in-betweening: the arXiv PDF is over 10 MB, and the HTML copy failed.
- **Prazak 2011, full text:** Eurographics library refused (403); closed access. Abstract only.
- **Leamon & Li 1990:** a conference paper, not found. Only papers citing it were read.
- **Lee et al. 2002, contact thresholds:** the CMU site's certificate failed.
- **Epic's Foot Placement guide page:** it renders no body text to the tool. The engine source and API page were used instead.
- **Not sought:** GDC Vault videos (EA's "Motion Matching at EA", For Honor) and Epic's Unreal Fest talks.

## Unverified

- MANN's formula is as four later papers quote it; MANN itself was not read.
- Starke's own skate numbers are unknown.
- The Clavet points are second-hand.
- Units: Tang 2022 and RSMT give no units, and MVAE's frame rate was not checked. Holden's 0.15 is m/s by code context.
- The 2011 study's viewing conditions are unknown.
- Whether the stop scuff is in Epic's source clips was not checked here.
- The ball joint moving during a ball pivot is inference.
