# Study 9: Camera, controls and feel (28 October 2026)

Mafia: The Old Country (third person, Unreal 5.4) and Kingdom Come: Deliverance II (first person) from their own files, and public pages for play. Our own words and numbers; raw notes on F:/LedgerTools/aaa-study (mafia/study-9-10-13/notes, kcd2/study-9-10-13, public/study-9-10-13-sources.md); read 28 October 2026. Tags: **M** measured, **R** read, **I** inferred, **N** a name only. Distances in metres.

**The short answer.** Mafia's camera is data: 83 of its 116 camera modes are picked from one table by the player's state, 15 more from a table of paired moves. On foot it is close and calm: 82°, 1.65 m behind a pivot 1.25 m up. It narrows and closes in for town walking, low rooms and talk, and widens for running. Interaction is scored ahead of the body and inside the camera's view. Tom's street camera, as coded, hangs twice as far back (3.2 m) with a wider lens (90°). LEDGER should take Mafia's on-foot, room and talk numbers and its scored target, in a spec, through his page.

## The numbers, and what we propose for Tom

| | Mafia | Kingdom Come II | LEDGER as coded | Proposed for Tom |
|---|---|---|---|---|
| Lens on foot | 82°, slider 50 to 120 (R) | slider 75 to 110 (R, public) | 90° (M, packaged walks 21 to 28 Oct) | 82°; slider 70 to 110 |
| On his 3440×1440 | about 99° × 52° (I, Unreal's rule; "Hor+" on PCGamingWiki agrees) | | about 107° × 59° (I) | about 99° × 52° |
| Pivot | 1.25 m above the feet; crouched 0.90 (R) | the eye | the hip, 0.88; office +0.6 (R) | 1.25 m |
| Camera from pivot: back, side, up | 1.65, 0.45, 0.35 (R) | | 3.20, 0.45, 0.55 (R) | 1.55, 0.40, 0.35 (79°) in the street |
| Town or walking, calm only | −3°, 0.10 closer, 0.05 less to the side; blend 1.3 s in, 2.0 s out (R) | | none | as Mafia |
| Running | 85°, 1.40 back, 0.2 s blend (R) | look −35 to 45° (R; perhaps an engine leftover, I) | none | 85°, 1.40 back, 0.2 s |
| Rooms | standard ceiling 1.40 back; low ceiling, calm only: 1.20, 0.35 side, 78° (R) | | office arm 2.0 (R) | tagged rooms; Mickey's office 1.20, 0.35, 78° |
| Pitch | −70 to 70°; fully up the camera comes 0.9 in (R) | −70 to 80° (R; leftover, I) | Unreal's default (I) | −70 to 70° |
| Lag | pivot spring up to 0.30; no auto-follow on foot by default (R) | | none (R) | as Mafia |
| Blends | 1.0 s in the walking mode, 0.75 s in the transitions table; which wins is code (R, I) | | arm eases at rate 4 (R) | 0.75 to 1.0 s |
| Talk | player placed 1.5 away; 63°, pivot 1.50; 2 s blends (R) | a camera command on 80,812 of 147,859 lines (M) | the street camera | Tom 1.5 m away; 63°; 1.20 back, 0.25 side |
| Whom to act on | body shapes to 2.75 ahead; a 60° camera cone to 5 m; choice held 0.2 s (R) | the centre of the screen (I) | nearest (R) | scored by facing and view; held 0.2 s |
| Reach | 2.5 by default, 2.0 for talks (R) | doors 2.0, stashes 2.5, locks 1.5 (R) | talk 3.5, use 2.2 (R) | 3.5 until the facing rule works, then try 2.5 |
| Holds | 0.2 to 4 s; taps within 0.15 to 0.3 s (R) | 0.25 s on 48 actions, 0.5 s on 16 (M) | none | 0.25 s |

## The on-foot camera (Mafia)

- **Tables pick the camera.** Each of the 83 rows is a mode plus a tag rule (death, aiming, cover, sprint, crouch, rooms, horse, car). Plain walking is row 82, and its rule is empty. An empty rule matches nothing in Unreal, so the default is picked in code (I). The rest of the 116 modes serve talks and films (I).
- **Walking:** the pivot rides a spring (at most 0.30 m); at 5 m/s the lens widens 2% and the camera eases up to 12 cm back (a curve scaled 0.3: I); a rotation-only shake scales with speed, near nothing standing still (I).
- **Layers on the walking mode:**
  - town or walking, calm only: −3°, 10 cm closer, 5 cm in;
  - alert: 4 cm lower, 0.6 s;
  - fight: 15 cm lower, 0.4 s;
  - focus: 25 cm closer.
- **Lenses by state:** sprint 85°; talk 63°; walk-and-talk 70°, 10° narrower while lines play; aim 65°.
- **Options:** lens; camera shake (on); camera follow on foot (off: the camera stays where the player left it).

## Near walls and in rooms

- **Mafia tags spaces, then swaps the camera:** standard ceiling, low ceiling, mines, town exterior (N; set by volumes, I). Its collision safe point sits 1.95 m above the feet, traced from 0.90 m (R; their use, I). Whatever blocks the view is hidden on a collision channel of its own (R). Probe size, hide radius and dither are code defaults, not read.
- **LEDGER:** one spring arm, a 12 cm probe from the hip, the office alone with its own numbers, Tom hidden within 55 cm; packaged, Epic's sample camera hangs further back than the editor's (27 October, cause not found). Mafia confirms the camera-interiors note's per-room method, with tagged spaces for our rectangle test.

## Talking

- **Mafia's story talks** (R):
  - movement and camera locked; the player walked to 1.5 m;
  - five shots: wide, close-up on either, over either shoulder;
  - layouts for one-to-one, a chair, a table, and groups of two or three.
  - From a 1.50 m pivot at 63°: close 0.80 back and 0.30 to the side; far 1.20 and 0.25; distant 1.70 and 0.45.
  - A talk starts only with the camera within about 18° of the speaker (I, from a 0.95 dot product).
- **Kingdom Come II** authors a shot for most lines (M): custom 28,819, close shot 14,135, close-up 12,496, medium 3,975. Its placed scene cameras have a median vertical angle of 22° (M; vertical, I), not comparable with the lenses above.
- **LEDGER:** "the camera puts Tom between the player and whoever speaks" (FINDINGS, P4, 3 October).

## Interaction and input

- **Mafia scores targets** (R): body shapes reach 2.75 m ahead and 2 m to each side; a 60° camera cone out to 5 m scores as much as the main body shape; the current choice keeps a bonus for 0.2 s, so it does not flicker; reach is 2.5 m, 2.0 m for talks. Interact starts on the press; interactables default to a "standard hold", its length in code (N).
- **Kingdom Come II** acts at the screen's centre (I). It has no angle limit on 91% of 1,375 placed objects (M).
- **LEDGER:** "T opens the talk with whoever is nearest, not the one Tom faces" (FINDINGS, 4 October). The style guide's "facing it" is not in the code.
- **Input:** Mafia's sprint toggles by default; neither game shows an input buffer in data (code, N).

## For LEDGER

1. **Adopt, through his page:** Mafia's street, room and talk framing for Tom. It changes the look of every frame, so it goes on one page as one decision (CLAUDE.md). It serves phase 1's packaged walk and the friends' build.
2. **Adapt, small:** the four proposed modes (street, run, room, talk) as rows in one spec, read by the existing camera arm. This is not a new camera system (29 September ruling). It also serves Study 13's tuning home.
3. **Adopt: tagged rooms** after NOW item 5. The office now passes its back wall through Epic's camera, so the room's numbers are tried there as a gate, not slipped into it.
4. **Adopt: Tom placed at 1.5 m for a talk.** It closes the 3 October camera fault, and goes on the same page as item 1.
5. **Adapt: choose the person ahead and in view,** held 0.2 s. It closes the 4 October fault and meets the style guide.
6. **Ignore:** aiming, cover, car and horse cameras (not a shooter, 12 October); the first-person camera; shots authored per line (LEDGER's talk is live). Camera shake goes under Reduce motion (Study 10), not a switch of its own.

## Coverage map

Add a row "Camera and input" (Mafia: data, 83- and 16-row mode tables; Kingdom Come II: first person, authored dialogue shots), ticked 28 October (Study 9). Also tick "Doors, pick-ups, world interaction", its targeting side.

## Open blind spots

- Code: Mafia's default mode, hold length, probe and hide defaults; input buffering in both games.
- Epic's sample camera rigs in our packaged game (editor files, no editor today); Kingdom Come II's default lens; Mafia's input config (its raw export saved nothing).
- Feel in play: no recordings. One review found aim and camera share one sensitivity, making the camera "too sluggish" (Jimquisition, 19 August 2025).

## Sources (read 28 October 2026)

- Mafia's Camera, Input, settings, targeting and conversation exports and configs; Kingdom Come II's profiles, rpg_param.xml, quest files and level cameras; Unreal 5.8's projection source; PCGamingWiki, 2K's notes, Jimquisition.
- LEDGER: SliceCharacter, CrimeProbe, LedgerSettings, mickeys-office.json, the camera-interiors note, FINDINGS, DECISIONS, the nightly walk logs.

Extract: 46.4 MB on F: for Studies 9, 10 and 13; no textures, meshes or sound.

## Review

A fresh reviewer (28 October) checked about 115 numbers across Studies 9, 10 and 13, re-measuring 34: pass with fixes, all applied. Corrected: the default row, the room and town conditions and blends, the camera cone and reach, the mode count, the default blend, 107°, Kingdom Come II's holds. Hedged: the order rule, the shake, the 21:9 angles. Rescoped item 2; items 1, 3 and 4 routed to his page. Cost, from the clock: 12:50 to 14:08 for Studies 9, 10 and 13 together (reading, two helpers, extract, synthesis, review, fixes).
