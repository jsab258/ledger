# Ron cannot leave Mickey's office: diagnosis, 9 Nov 2026

Packaged 5ed8f38's log. Read-only.

## The measure

"Here by office_east wall" names only the first thing at Ron's own spot (the bench too); the walk's test starts 0.6 m out (CrimeProbe.cpp:7928). The fault predates the box: on 7 Nov the same three walks failed ("0.6 m on by office_notices" eastward, the shop front's frame toward the rank), and Ron appeared at the rank at D1 09:19 (F:/LedgerTools/gate/new/office-sit-default-2026-11-07/walk-day/logs/LedgerProbe.log).

## How a walk finds its way

A straight line, tested every half metre with a 30 cm capsule (7780-7806, 7924-7936); if blocked, one side step of 0.6 or 1 m, up to four legs (7940-7979). No navigation mesh, no doors. Every one of Ron's targets (30 m east, the cafe, the rank) lies through a wall; the door is at the west end (x 4.65, z 5.0). From inside, no line ever reaches it.

## Why he waits, then appears

A failed walk falls back to the old way: held while in Tom's view, with no end within 6 m (8392-8393, 8536-8542). Tom sat 1.31 m away from D0 21:13 to D2 10:12. Then Ron was placed at the rank (8551-8557), two seconds before Tom's talk with Sheila opened: most likely the camera turned to her and Ron left its 50-degree cone (7860-7870). Medium confidence; the camera's direction is not logged.

The seated check is stale: it wants clips named "A_sit" (8027); Ron sits in A_bench_idle_MH since 2 Nov (01e14f296), so walks are tried from the bench, with no stand-up.

## Should the box block people?

Yes. The boxes are engine cubes, query-only, default BlockAll: world-static, blocking Pawn and Camera (VignetteShot.cpp:1900-1926; UE 5.8.2 StaticMeshActor.cpp:33, BaseEngine.ini:3104). Letting people through would let Tom past the wall again. Keep it.

## Smallest fix (not applied)

1. CrimeProbe.cpp:8027: treat any seated loop as seated (a flag set in SeatPerson, 7819-7846, when its clip is not empty). Seated people keep the old way, as the comment at 7879 intends, and the failed tries stop. Ron still appears at the rank once Tom looks away.
2. To walk him out, at 8030 before WalkPath: a walker inside the room (GOffice.bOn, X0..X1, Z0..Z1) going outside is routed through the door: an inside point (GOffice.DoorX, about 6.0), an outside point (DoorX, about 4.35; the "Ron at the door" mark is 4.64, 4.3), then the target, each leg through WalkPath. From the bench the first point must lie almost due west (about 7.4, 5.95); the capsule clears bench and window board there by 2 cm. A seated starter also needs A_stand_up_MH first, as the sit proof plays it (about 10075-10090).

## Same cause elsewhere

- Sheila (line 1987) is shut in: 40 cm between counter and radio desk, 45 cm behind the desk with Mickey's chair in it; the capsule needs 60 cm. A door route fails from her mark unless indoor legs use a narrower test.
- The public side has a lane at least 1.88 m wide to the door.
- Ron's standing breaks play while he sits (log 00:40:49, 00:41:04); BreakTick (PersonAnim.cpp:315-337) has no seat test.
- The sit proof has the same stale "A_sit" test (9966, 10084).

## Checks and gaps

High confidence for route and fallback. To confirm: an editor run with fix 1 logs no "cannot walk" for Ron on the bench; with fix 2, "in 3 leg(s)". Not checked: the door frame against the capsule (Tom's 34 cm one passes), how the breaks look, and Kingdom Come II's or Mafia's method; the study has one line, extras "come out through a door" (01-npc-life.md:37).
