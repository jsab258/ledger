# Study 7: Animation (25 October 2026)

How Mafia: The Old Country and Kingdom Come: Deliverance II make people move, read from their own files and from what their makers have said in public. Our own words and numbers only; the games' files and the helpers' raw counts stay on F:. Every number below was read on 25 October 2026 from the sources named at the end.

## Answers

**Walking: neither game uses motion matching.**
- **Mafia** walks on a layered state machine.
  - A base animation blueprint picks a movement source (ordinary, cover, strafing, duels).
  - The ordinary layer holds 16 small state machines: start, cycle, stop, turn, pivot, fall, dodge.
  - Each state plays single clips, chosen from data assets.
  - 54 animation classes were read: 59 state machines, 239 states, 563 transitions. Not one motion-matching node.
- **Kingdom Come II** uses CryEngine's Mannequin with blend spaces.
  - 842 blend-space files and 94 animation databases with 22,342 options.
  - Starts and stops are their own blend spaces.
- **Hangar 13** captured "systemic" movement (player and NPC) on its Brno stage, per 2K's dev diary of June 2025. Its current job postings mention motion-matching research, which describes the studio now, not the shipped game.

**Starts, stops and turns are chosen, not searched.**
- **Kingdom Come II:**
  - Every start and stop exists in a left-foot and a right-foot version, plus long stops.
  - A table picks the stop by remaining distance (walk 0.6 to 2.1 m), travel angle (5 degrees tolerance) and the quarter of the stride the walk is in, so the planted foot matches the clip.
  - Turns on the spot are blend spaces over the turn angle, with clips at 45, 90, 135 and 180 degrees each way.
- **Mafia:**
  - Each movement set holds 12 starts (0, 90 and 180 degrees each way, walk and run), 6 stops (walk, run, sprint, each foot), 4 idle turns plus a feet-locked turn, and 2 pivots.
  - Its stops carry a distance curve (all 38 of the hero's stops). They are distance-matched to a predicted stop point: the library calls PredictGroundMovementStopLocation, DistanceMatchToTarget and AdvanceTimeByDistanceMatching appear in its graphs.
  - Starts get a start offset by angle.
  - Stride warping (scale clamped 0.5 to 1.5) and orientation warping fit clips to the real speed and direction.
  - 183 of its 563 transitions are inertialized.
- The hero's ordinary movement draws on 577 clips; civilians on 113.

**Feet.**
- **Mafia's walk has no foot lock.**
  - Its feet are a control rig run at close range only: a 5 cm sphere trace per foot, pelvis offset up to 40 cm, feet up to 50 cm, a full-body solver at 20 iterations.
  - Stride warping moves the feet through virtual IK bones.
  - Its one foot-placement node, with a ball-pivot lock, is in the duel layer only. It plants below speed 80 and lets go at 50 cm.
  - Turns, some stops and landings carry planted-foot curves (51 clips); starts and cycles carry none.
  - Civilians get only a two-bone leg IK, no trace.
- **Kingdom Come II's skeleton** declares 3-bone leg IK, a 5-joint foot-align chain and a feet lock for both legs.
  - Ground alignment is switched off clip by clip wherever a body is fitted to furniture (932 of 1,055 uses in the male set).
  - Its foot-IK tuning numbers are not in any data file; they live in its code.
- **The field:**
  - Epic's own pages for 5.8 say nothing about foot locking.
  - Ubisoft's For Honor talk (Clavet, GDC 2016) locks the toe to the ground and keeps play-rate changes within about 10% faster or 20% slower.
  - A 2011 perception study puts what viewers notice at about 2.1 cm. This is from its abstract only and unverified.

**Interactions and the street's life.**
- **Mafia's scripted world animation** holds 2,144 clips:
  - standing 230, sitting 191, leaning 119, patrol 84, sleeping 20;
  - 990 montages of special actions;
  - 490 smart objects tie them to places.
  - By name: sitting 451, leaning 196, smoking 198, doors about 190, carrying 108, talking 526.
- **Kingdom Come II:**
  - 279 smart-object classes with 510 anchor points;
  - 622 activity poses, each with an In, a Loop and an Out;
  - doors as 2 sets of 6 stages (opening and closing, inward and outward) from both sides;
  - for the male set, about 300 sitting and 260 carrying options, and about 400 trade-work fragments.

**Talking.**
- **Kingdom Come II** has a gesture table of 4,183 entries in 344 families (agree, disagree, listen, speak, point, think, laugh...) across 70 moods, median 2.9 s, about two in five while sitting.
- **Both games pre-bake every face:**
  - Mafia has one face clip per spoken line (12,802), on a MetaHuman-style face rig.
  - Kingdom Come II has one facial file per scene and speaker (18,449 files, 8.2 GB), played on its own layer. It has no phoneme data.

**Crowds.**
- **Mafia:**
  - Animation sharing: 14 setups, 745 randomised instances, for parades, spectators and miners.
  - A small vertex-animated crowd: 13 assets.
  - Its control-rig feet stop beyond the near level of detail.
- **Kingdom Come II** has no crowd animation system. It reduces AI detail beyond 150 m and keeps at most 70 to 80 people in full detail.

**Unreal 5.4 against 5.8.** Every method named here exists in LEDGER's 5.8.2 engine, checked by name in its plugins: distance matching and stop prediction, stride and orientation warping, dead blending, foot placement, animation sharing, vertex-animated crowds.

## For LEDGER

- **Adopt, for the walk (item 2): the professional stop is a chosen clip whose planted foot already matches, not a searched one.**
  - Both games pick stops by distance and by which foot is down; Kingdom Come II also by the quarter of the stride.
  - Our motion matching searches all 223 of Epic's walking clips, and 134 of them carry a flat foot that travels more than 3 cm in Epic's own data (measured 25 October).
  - So the first fix stays as planned: hold a low, still foot (the clip's contact marks) and lock it more readily. The day's runs follow in the walk's record.
  - If that does not pass by eye, the next direction is Mafia's: distance-matched stops and turns picked by foot, inside the same graph.
- **Adapt: turns on the spot as their own clips by angle (45, 90, 135, 180).** Mafia gives the feet-locked turn its own clip.
- **Adopt: warping bounds.** Stride warping clamped to 0.5 to 1.5 and play-rate changes kept within about 10% faster and 20% slower, so feet do not skate when speed and clip disagree.
- **Adopt, for sitting (item 2's second half):**
  - every activity as In, Loop and Out, tied to an anchor point on the seat;
  - ground alignment off while fitted to furniture.
- **Quay Street's ambient animations.** Each needs In, Loop and Out where it is a pose; Mixamo is allowed on his account, Epic's MetaHuman movement clips are allowed, and none of these is ours to make:

| Action | Count | Route |
|---|---|---|
| Stand idles and fidgets, men and women | 4 | Epic's MetaHuman movement clips, then Mixamo |
| Lean on a wall or shop front | 2 | Mixamo |
| Sit on a bench, a chair, the office stool | 3 | Mixamo, fitted to the anchor |
| Smoke a cigarette | 1 | Mixamo |
| Read a newspaper standing and sitting | 2 | Mixamo |
| Talk in pairs | 8 | Mixamo |
| Behind a shop counter | 2 | Mixamo |
| Sweep the pavement | 1 | Mixamo |
| Carry a bag or a box | 2 | Mixamo |
| Open and close a door, inward and outward | 4 | Mixamo, both sides |
| Wait at the bus stop or the phone box | 2 | Mixamo |
| Turn and look | 1 | Mixamo |
| Startle | 1 | Mixamo |
| Point | 1 | Mixamo |

  - The pair talk covers agree, disagree, listen, speak, point, shrug, think and laugh.
  - The counter actions are idle and wiping.
  - Turn and look is for noticing Tom; the startle is for a deed seen.
  - Counts are a first floor from what both games use most, not a target; no child, alcohol or gambling animation is wanted.
- **Ignore for now: animation sharing and vertex-animated crowds.** Quay Street holds about 20 to 30 people within 48 m. They return with phase 5's town and Study 12.
- **Faces:** both games pre-bake every line, which LEDGER's live talk cannot do. The ruling of 1 October stands: prepared lines use Epic's audio-driven mouths, live lines the voice's loudness. Kingdom Come II's gesture families are the model for talk's body language.

## Coverage map

Ticked by this study: locomotion and animation (both games); doors, pick-ups and world interaction (the animation side); characters (faces' animation only). Barks and dialogue staging remain with Study 3.

## Open blind spots

- How Mafia's stops avoid sliding inside the clip (its distance curves' shapes were not decoded).
- 144 of its animation classes were not read (garments, weapons, vehicles, horses).
- Kingdom Come II's foot-IK tuning lives in code.
- Anything only seen in play: no public talk by either studio on locomotion or feet was reachable.

## Sources (read 25 October 2026)

- **Mafia's own files**, read with FModel: 1,508 property exports, the package name index, its compiled class list. Raw counts in F:/LedgerTools/aaa-study/mafia/study-7/ (FINDINGS.md and its CSV files).
- **Kingdom Come II's own files**: unpacked tables, scripts and animation databases, the archive indexes, the character parameter files. Raw counts in F:/LedgerTools/aaa-study/kcd2/study-7/.
- **Public sources**, F:/LedgerTools/aaa-study/public/study-7-sources.md:
  - 2K's dev diary of 17 June 2025;
  - the CzechCrunch interview with Warhorse's mocap lead (19 January 2022);
  - Epic's 5.8 animation pages;
  - Clavet's For Honor talk notes;
  - the 2011 perception abstract (unverified).
  - Not reached: Hangar 13's Unreal Fest 2025 talk (video only), Epic's interview with its art director (403), the GDC Vault (down).
- **Epic's walking clips measured** from their assets: production/research/sit-and-turn/metahuman-route-2026-10-24/runs/clip_feet_all.py.

Cost: about 1.5 hours of helpers in parallel (three Sonnet extractions, about 25 minutes each of wall time), the synthesis by the session, its fresh review below.
