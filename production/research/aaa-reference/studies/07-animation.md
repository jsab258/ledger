# Study 7: Animation (25 October 2026)

How Mafia: The Old Country and Kingdom Come: Deliverance II make people move, read from their own files and from what their makers have said in public. Our own words and numbers only; the games' files and the helpers' raw counts stay on F:. Every number was read on 25 October 2026 from the sources named at the end. Revised the same evening after its fresh review (appended).

## Answers

**Walking: neither game uses motion matching.**
- **Mafia** walks on a layered state machine.
  - A base animation blueprint picks a movement source: ordinary, cover, strafing or duels.
  - The ordinary layer holds 16 small state machines (start, cycle, stop, turn, pivot, fall, dodge) playing single clips from data assets.
  - 54 animation classes were read: 59 state machines, 239 states, 563 transitions (183 inertialized).
  - None of them holds a motion-matching node. The game's whole name index of 139,791 packages holds no pose-search asset either.
  - 144 animation classes were not read, among them the female walk and strafe layers and a carry overlay.
- **Kingdom Come II** uses CryEngine's Mannequin with blend spaces: 842 blend-space files and 94 animation databases holding 22,342 options. Starts and stops are their own blend spaces.
- **Hangar 13** captured "systemic" movement (player and NPC) on its Brno stage, per 2K's dev diary of June 2025.

**Starts, stops and turns are chosen, not searched.**
- **Kingdom Come II:**
  - Every start and stop exists in a left-leg and a right-leg version, plus long stops.
  - A table picks the stop by remaining distance (walk 0.6 to 2.1 m), travel angle (5 degrees tolerance) and the quarter of the animation the walk is in. That this keeps the planted foot matched is our reading, not stated in the data.
  - Turns on the spot are blend spaces over the turn angle, with clips at 45, 90, 135 and 180 degrees each way.
- **Mafia:**
  - Each standing movement set holds:
    - 12 starts (0, 90 and 180 degrees each way, walk and run);
    - 6 stops (walk, run, sprint, each foot);
    - 4 idle turns, plus one field named for a feet lock (its use not read);
    - 2 pivots.
  - All 38 of the hero's stops carry a distance curve. Distance matching to a predicted stop point is proven in the cover layer only; the ordinary walk layer has no node that could play a clip by distance, and how its stops are timed is not read.
  - Stride warping, its scale clamped 0.5 to 1.5, fits clips to speed. Orientation warping sits in the civilian, strafe, cover and duel layers, not the hero's ordinary walk.
  - About 155 of the hero's 577 no-weapon clips are movement clips; its movement data assets reference 552 clips in all.

**Feet.**
- **Mafia, in the 54 classes read, has no foot lock on its walk.**
  - Its feet are a control rig run at close range only: a 5 cm sphere trace per foot, pelvis offset up to 40 cm, feet up to 50 cm, a full-body solver at 20 iterations.
  - Its one foot-placement node, with a ball-pivot lock (planting below speed 80, letting go at 50 cm), is in the duel layer.
  - 51 clips carry planted-foot curves (turns, some stops, landings), none on starts or cycles. The skeleton carries curves to switch a foot lock off.
  - Civilians get only a two-bone leg IK, no trace.
- **Kingdom Come II's skeleton** declares 3-bone leg IK, a 5-joint foot-align chain and a feet lock for both legs.
  - Ground alignment is switched off in 932 of its 1,055 uses in the male set (sitting, standing up, lying, ledges, deaths, quest scenes; counted per fragment).
  - No foot-IK tuning numbers are in its data; that they live in code is our inference.
- **The field:**
  - Epic's Foot Placement reference documents the lock's settings, but gives no defaults or tuning advice.
  - Ubisoft's For Honor talk (Clavet, GDC 2016) locks the toe to the ground and keeps play-rate changes within about 10% faster or 20% slower.
  - A 2011 perception study (Pražák, Hoyet and O'Sullivan) is known to us only from a search snippet. It reports that viewers noticed foot sliding below 21 mm. So it gives a floor, not a ceiling: some viewers see slides under our 3 cm bar.

**Interactions and the street's life.**
- **Mafia's scripted world folder** holds 2,144 animations: montages 990, special 396, standing 230, sitting 191, leaning 119, mining 104, patrol 84, sleeping 20.
  - It has 389 smart objects for world interactions (with 87 prop attachments and 12 props beside them).
  - Across all its animations, by name: sitting 451, leaning 196, smoking 198, doors about 190, carrying 108, talking 526. Within the world folder alone: doors 18, carrying 17.
- **Kingdom Come II:**
  - 279 smart-object classes with 510 anchor points.
  - 622 activity poses, each with an In, a Loop and an Out.
  - Doors as 2 sets of 6 stages from both sides.
  - In the male set: 336 sitting and 260 carrying options, and about 400 trade-work fragments.
- **Per street:** neither game's ambient animations per street were counted. This is an open blind spot, taken up by Study 4.

**Talking.**
- **Kingdom Come II:**
  - A gesture table of 4,183 entries in 344 families (agree, disagree, listen, speak, point, think, laugh) across 70 moods, median 2.9 s, about two in five while sitting.
  - Speakers face and look by a 3 by 3 grid of look offsets and 25 male and 13 female look poses.
- **Mafia's conversation set** is 123 animations (59 sequences, 64 montages), mostly standing; 93 animations in the game are named as gestures.
- **Both games pre-bake every face:**
  - Mafia has one face clip per spoken line (12,802), on a MetaHuman-style face rig.
  - Kingdom Come II has one facial file per scene and speaker (18,449 files, 8.2 GB), played on its own layer, with no phoneme data.

**Crowds.**
- **Mafia** uses animation sharing (14 setups, 745 randomised instances for parades, spectators and miners) and a small vertex-animated crowd (13 assets). Its control-rig feet stop beyond the near level of detail.
- **Kingdom Come II** has no crowd animation system. It reduces AI detail beyond 150 m and keeps at most 70 to 80 people in full detail.

**Unreal 5.4 against 5.8.** Every method named here exists in LEDGER's 5.8.2 engine, checked by name in its plugins: distance matching and stop prediction, stride and orientation warping, dead blending, foot placement, animation sharing, vertex-animated crowds.

## For LEDGER

- **For the walk (item 2):**
  - **The best-evidenced professional stop is Kingdom Come II's:** a clip chosen by the remaining distance and the quarter of the stride, in a left-leg, a right-leg and a long version.
  - **Our motion matching instead searches all 223 of Epic's walking clips,** and 134 of them carry a flat foot that travels more than 3 cm in Epic's own data (measured 25 October).
  - **Today's two tries** (holding a low, still foot, and a lock that holds a half-marked foot) are tested on the street first because they keep the sample as it is. They are judged by eye.
  - **If they do not pass:** stops and turns-on-the-spot chosen like Kingdom Come II's, by distance window and stride quarter with per-foot clips, inside the same graph.
- **Play rate:** keep a clip's play rate within about 10% faster and 20% slower of its authored speed (Clavet), so feet do not skate when speed and clip disagree. Mafia's stride-warping clamp of 0.5 to 1.5 is a different setting and no bound on skating.
- **The bar itself:** the only perception figure found says viewers notice slides below 21 mm. It is from a snippet, unverified, but it makes 3 cm a lenient bar.
- **For sitting (item 2's second half):**
  - every activity as In, Loop and Out, tied to an anchor point on the seat;
  - ground alignment off while fitted to furniture.
  - Epic's sample in our project already holds a bench interaction built this way, on smart objects: approach clips from five sides, each on either foot, an idle loop and a stand-up.
- **Quay Street's ambient animations:** a first floor from what both games use most often, not a target. Every route is to be checked: that Mixamo has each one, with matched In, Loop and Out, is not yet checked. No child, alcohol or gambling animation is wanted.

| Action | Count | Route |
|---|---|---|
| Stand idles and fidgets, men and women | 4 | Epic's MetaHuman clips, then Mixamo |
| Lean on a wall or shop front | 2 | Mixamo |
| Sit on a bench, a chair, the office stool | 3 | Epic's bench interaction, then Mixamo |
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
- **Talk's body language:** Kingdom Come II's gesture families and its 3 by 3 look grid are the model.
- **Faces:** both games pre-bake every line, which LEDGER's live talk cannot do. The ruling of 1 October stands: prepared lines use Epic's audio-driven mouths, live lines the voice's loudness.
- **Ignore for now: animation sharing and vertex-animated crowds.** Quay Street's own count of people is set in Study 1 and Study 4; these come back with phase 5's town and Study 12.

## Coverage map

Ticked by this study:
- locomotion and animation, both games;
- doors and world interaction, the animation side only (pick-ups not studied);
- characters, faces' animation only.

Barks and dialogue staging remain with Study 3.

## Open blind spots

- How Mafia's ordinary walk times its stops: the distance curves were not decoded, and the transition rules were not read.
- 144 of Mafia's animation classes, including the female walk and strafe layers.
- Kingdom Come II's foot-IK tuning (in code).
- Ambient animations per street, in both games.
- Anything only seen in play: no public talk by either studio on locomotion or feet was reachable.

## Sources (read 25 October 2026)

- **Mafia's own files**, read with FModel: 1,508 property exports, the package name index, its compiled class list. Raw counts in F:/LedgerTools/aaa-study/mafia/study-7/ (FINDINGS.md and its CSV files).
- **Kingdom Come II's own files**: unpacked tables, scripts and animation databases, the archive indexes, the character parameter files. Raw counts in F:/LedgerTools/aaa-study/kcd2/study-7/.
- **Public sources**, F:/LedgerTools/aaa-study/public/study-7-sources.md: 2K's dev diary of 17 June 2025; the CzechCrunch interview with Warhorse's mocap lead (19 January 2022); Epic's 5.8 animation pages; Clavet's For Honor talk notes; the 2011 study (a search snippet only).
- **Not reached:** Hangar 13's Unreal Fest 2025 talk (video only), Epic's interview with Alex Cox (403), the GDC Vault (down).
- **Epic's walking clips measured** from their assets: production/research/sit-and-turn/metahuman-route-2026-10-24/runs/clip_feet_all.py.

Cost, from the clock: 19:42 to 20:20 for the exports, three helpers in parallel and the synthesis; the fresh review and these fixes 20:20 to 20:40.

## The fresh review (25 October, Opus; verdict: pass with fixes, all applied above)

**Confirmed, about 40 items, many re-counted from the raw files:**
- the class, state and transition counts;
- the start, stop, turn and pivot counts;
- the distance curve on all 38 hero stops;
- the foot rig's limits;
- the duel foot placement;
- the world-folder and by-name counts;
- Kingdom Come II's blend spaces, databases, stop table, smart objects, doors, gesture table and facial files;
- Epic's 134 of 223 clips;
- the 5.8 methods.

**Wrong, and fixed:**
- montages and special actions run together;
- 490 smart objects (389);
- "Epic says nothing about foot locking";
- about 300 sitting options (336);
- the 932 uses misdescribed;
- 577 clips misdescribed;
- an estimated cost.

**Hedges restored:**
- Mafia's distance matching proven for cover only;
- the foot lock only for the classes read;
- Kingdom Come II's stride-quarter reading and foot-IK numbers inferred;
- the 2011 figure from a snippet, and a floor.

**Added:**
- speakers facing;
- Mafia's conversation set;
- per-street ambient counts as a blind spot;
- the Mixamo routes marked to be checked;
- the unsourced street count dropped;
- the next direction rebased on Kingdom Come II's table.
