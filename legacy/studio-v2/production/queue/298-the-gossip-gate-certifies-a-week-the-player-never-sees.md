line: instruments and premise, jointly
spec: the phase 1 gate requires a witnessed crime to reach a second and third
  NPC "within one in-game week". MEASURED: the play clock is 2 game-minutes
  per real second (ledger/Assets/Scripts/Game/GameController.cs:12, "1 game
  day = 12 real minutes"), so one in-game week is 84 REAL MINUTES of play.
  The Meridian Test's whole first session is 30 minutes. So the gate
  certifies a window 2.8 times longer than the entire session it exists to
  serve, and A BUILD CAN PASS IT AND STILL FAIL THE TEST.
  TWO CLOCKS, and the distinction is why this hid: sim mode overrides the
  rate to 20 game-minutes per real second
  (Game/SimDirector.cs:65, "1 game day = 72 real seconds"), so the gate is
  CHEAP TO RUN, about 8.4 real minutes of sim for the week. Nothing about
  running it is painful, which is exactly why nobody noticed that the thing
  it certifies is unreachable in a session.
acceptance: the gate restated against the TEST rather than the calendar, per
  Jafar 2026-09-14: what must be true inside 30 minutes of play for condition
  2 of the Meridian Test ("within those 30 minutes the world visibly knows
  them at least once: recognized, gossiped about, or confronted with
  something they did earlier"). Then a sim run measuring that window, at the
  PLAY clock rate rather than the sim rate, since a rate that compresses the
  day also compresses every travel term the result depends on. Whether the
  answer is a shorter window, a faster rumour, or a scripted first encounter
  is NOT decided here.
max_sessions: 1
status: READY 2026-09-14, ordered by Jafar, who ruled the direction: "Rule
  the gate against the test rather than the calendar." The re-specification
  itself is a roadmap change and therefore a director's, not a builder's.
  Note for whoever takes it: the 84 minutes is the PLAY figure and the 8.4 is
  the SIM figure, and quoting either without naming which clock is how this
  gets miscommunicated next time.
