# People alive: proposal for Monday (7 November 2026)

Nothing decided. Costs are rough estimates. Outside pages and local files read 7 Nov 2026 unless dated. Studies 1 and 7: 25 Oct. NOTE: natural-idles/NOTE.md, 1 Oct. WALK: sit-and-turn/WALK-2026-10-25.md. REHEARSAL: audits/phase1-exit/REHEARSAL-2026-11-07-B.md.

## 1. Treading against an obstacle

**Method:** before the push reaches the mover (SliceCharacter.cpp:842-848), sweep the capsule ahead and remove the part of the push going into the obstacle. Head-on he stops; glancing, he walks along it at his true speed. Reference: none found in Studies 1 or 7.

**Options weighed:**

1. Line-trace braking, recommended: one poster's own fix, [forum](https://forums.unrealengine.com/t/motion-matching-mesh-ignores-walls/2264940), June 2025; no Epic reply.
2. Larger capsule, mesh collision: same thread; its reporter says neither worked.
3. Clamping body against animation: [Holden](https://theorangeduck.com/page/code-vs-data-driven-displacement), undated: feels "dragged along"; foot locking cannot fix walking against walls.
4. Obstacle features in the search: [arXiv](https://arxiv.org/html/2510.22632v1), 26 Oct 2025, last 17,000 characters unread: colliding 0.08 s against 0.88 s, searching 0.80 ms against 0.22 ms. Research only; not now.

**"Fixed in 5.6":** stays unverified; nothing found supports it. The thread says only "known issue in 5.5. Wait for 5.6" (8 Jan 2025), a forecast; no post says fixed. Only 5.8 is installed, so no before-and-after; the 5.6 release notes returned empty text. In 5.8's PoseSearch plugin, PoseSearchTrajectoryLibrary.cpp:932 and :965 are that file's only traces, both vertical (:934; its header, :205). Searching the plugin's source for "wall" and "obstacle" shows no sideways handling.

**Likely cause (inferred, unmeasured):** prediction takes acceleration (same file, :79); velocity reflects real travel (CharacterMovementComponent.cpp:5873); the sample's IsMoving needs both nonzero (F:/LedgerTools/game-inputs/gasp/exports/SandboxCharacter_CMC_ABP.t3d:15301-15365). So a dead-on block may stand, a glancing scrape keep striding.

**Cost:** half a day, plus a night's build. **Judged:** packaged side-on full-rate film at Mickey's front, head-on and glancing: no stride without travel. **Risk:** chosen stops need 68 to 118 cm (WALK), so near a wall one could carry him in.

## 2. Foot slide

**Method:** Tom: no more lock tuning; his third try is spent, and Epic's forward stops drag 11.3 and 17.6 cm in their own data (WALK). Speakers: body at the clip's own root speed, play rate within 10% faster, 20% slower (Clavet, through Study 7), then Kingdom Come II's per-foot stops.

**Cost:** a day. **Judged:** packaged, every 1/60 s step round each contact. Against: Tom worst 13.68 cm, Sheila 42.8, Ron 28.2 (REHEARSAL). **Risk:** the height reading over-counts swinging feet; MetaHuman's stops are unmeasured. The 21 mm perception figure stays unverified.

## 3. Stiff standing poses

**Method:** one base idle with a weight shift, retargeted to each body; Epic's M_Relaxed_Stand_Idle_Loop is on F:, unviewed. Today's is the female template's (CrimeProbe.cpp:940), a suspect NOTE never rendered; "arms held away" was seen 7 Nov (REHEARSAL). Source: NOTE, Study 7.

**Cost:** a day on Ron; others after his look. **Judged:** 45 s packaged film at 2.6 m: arms hang, pelvis shifts within 10 s (NOTE). **Risk:** the head parting from the neck (DECISIONS 2 Nov 13:34).

## 4. A walker's turn at a pause (try 1 of 2 used)

**Method:** replace the bare rotation at 120 degrees a second (PersonAnim.cpp:616) with the speakers' turning clips (CrimeProbe.cpp:7983). PersonAnim.cpp:598 itself says in-place turning slides planted feet 41 cm at 60 degrees. Kingdom Come II blends turns at 45/90/135/180; Mafia has 4 idle turns (Study 7).

**Cost:** half a day. **Judged:** packaged side-on film of a pause, every step: no lean or slide. **Risk:** 7 of Epic's 8 turns travel over 3 cm (WALK); two clips, angles unread. The fault is one unjudged still, so film first.

## 5. Idle variety

**Method:** hold; add only on repetition seen. Epic's 18 standing breaks are on F:, five carried over. Vendor rule, not studio data: 4+ base idles ([MoCap Online](https://mocaponline.com/blogs/mocap-news/idle-animation-game-dev-guide), 11 Apr 2026, read 1 Oct).

**Cost:** about a day, if earned. **Judged:** section 3's film: neighbours never in step. **Risk:** misses the seen 2.3 s jump, the placeholders' (FINDINGS).

## 6. Looking around

**Method:** hold; no fault recorded. If the film shows a held neck, lower CalmAlpha (0.7, PersonAnim.h:97; NOTE: 0.2 to 0.3). Epic's additive LookAtPOI comes later: on F:, unopened; the 5.8 blog refused today (403), parameters unreached. Limits remain unverified. Mafia pauses look-at beyond 32 m (Study 1); fit unchecked.

**Cost:** an hour; the solver several days. **Judged:** same film, Tom passing. **Risk:** experimental solver; cost per person.

## First, in order

1. The owed film: packaged, side-on, full rate, Mickey's front and open street, logging the mover's velocity, push and clip. It tests section 1's cause and judges sections 2 and 4.
2. The push cut (section 1), if the film agrees.
3. Ron's base idle (section 3), to his look.

Unreached: GDC talks; Epic's Foot Placement guide.
