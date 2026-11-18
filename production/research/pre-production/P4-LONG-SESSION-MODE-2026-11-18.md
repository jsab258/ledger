# P4 (a): the thirty-minute mode for the night walk (18 November 2026, 09:55)

Proof P4 in 3-PROOFS.md, part (a) only: thirty real minutes from New Game in the packaged build, on the stand-in talk, logged minute by minute. Part (b) (the real key) is not in scope.

Method researched: tools/nightly_walk.py, tools/route_walk.py, tools/ai-tester/play.py (usage text), production/specs/session-record.md, .claude/skills/packaged-walk/SKILL.md, production/specs/hook-cast.json (places), ue-probe/Source/LedgerProbe/Public/LiveClock.h (MinutesPerRealSecond), ledger/TalkHelper/Program.cs (the reply's `went` and `fellBack`), two real session files from the night of 18 November (Saved/Sessions 2026-11-18-015921 and -020646), F:/LedgerTools/nightly/task.log (14 to 18 November) and Task Scheduler (read 18 Nov 09:49).

Reference games: none found. No studied game (Mafia, Kingdom Come II) publishes how its testers log a long session minute by minute, so the walk's own method is reused.

## Questions answered

1. Can the night walk run a thirty-minute session without changing the normal walk? Yes. It is a separate tool (tools/long_session.py), called once at the very end of nightly_walk.py's main, after the night's report is written. The call returns at once when no request file exists, with nothing read, logged or run.
2. What does it reuse? From route_walk.py: Route (where Tom and the three are, the game's check lines, short legs by road, the stop test), start (close, launch with -RouteWalk, the tester's retries), walk_to_person, follow_aim, the first line LINE and the deed at Rita's window. Real keys come through play.py. The talk is the stand-in (no `--real-talk`, which the selftest checks). The record is the game's own (Saved/Sessions).
3. What does a player-like half hour look like? New Game, then Sheila's walk round, the first talk and the deed. After that a loop runs until thirty minutes after New Game: Sheila, a wander to a street place from the cast file with a look round, Ron, back to look at the window, Darren, another wander, and round again. The eight lines rotate (some name another of the three, some ask about the window or about him). At night (22:00 to 07:00 on the game clock) it presses Z, as a player would. It never stands idle as filler. A minute in which nothing happened is counted as such.
4. Where does each column come from?
   - What happened: the record's lines plus the walk's action log.
   - Who saw the deed: `witness` with saw true. Rung 0 is marked "the glass only", as the night report does.
   - Who mentioned it later and how: `known` (who, how, story), marked when its story is not a deed of this session.
   - "That's all I know": replies whose `how` is `fallback` or `ladder-refuse` (Program.cs counts the ladder's refusal with it).
   - Reply delays: the reply's `s`.
   - Nothing to do: a minute that has lines, but none from the content set (deed, witness, known, talk, reply, hint, ask, police, ellis, taken, tea, found, trust, week, calls, onlookers, reacted, gathered, named).
   - Broke the illusion: broken replies (fallback, refused, brush, paused, ladder-refuse, cut, walkedOff), replies over 2 s (P2's target), the tester's failed steps, keys that never reached the game, and a crash.
   - A minute with no line in either source reads "no record". Nothing is invented.
5. The clock: two game minutes a real second (LiveClock.h), whatever the player does. Thirty real minutes therefore cover about sixty game hours, less the Z waits. Each row carries the game clock the tester read. The tester is a script, so its own thinking time is well under a second a command.

## The night budget (from the code and the real nights)

- Task Scheduler: walk 01:30, retention 03:30, morning pictures 04:15.
- nightly_walk.py's own limits: the package request (timeout 300 s), up to 20 x 30 s waiting for the build machine to start, then up to 90 x 60 s for it to finish. So by code alone the walk could start as late as about 03:15 in the worst case.
- Real nights (task.log, 14 to 18 Nov):
  - the walk started 01:31 to 01:57 and took 13 to 19 minutes;
  - the bench and the eyes took about 3.5 minutes;
  - "done" came at 01:50 to 02:18.
- The long session needs 35 minutes: 3 to start (1.7 measured on 18 Nov), 30 to play and 2 to quit and close. It starts only if it can end by 03:15, 15 minutes before retention, so it starts no later than 02:40. On the real nights it would run about 02:18 to 02:53, leaving 37 minutes before 03:30.
- Its loop also stops at 03:15 whatever happens. An activity begun just before the stop can run on (the legs of walk_to_person). A watchdog closes every game 10 minutes after the end at the latest, after which each step returns at once, so a night run is over by about 03:25. The first talk and the deed are not begun with under 5 minutes left. Any error still closes the game, first through play.py and then by tree (close_games, taskkill /F /T). "passed_length" is true only for 30 or more rows that stopped as "thirty minutes played"; a run cut short says so.
- A run by day (`--play`) is refused if it would come within 15 minutes of the night window (01:15 to 04:30).

## Output

- production/playtest/p4/<date>-session.json and .md, holding:
  - the table: minute and game clock, then the seven columns;
  - the totals: minutes, minutes with nothing to do, no-record minutes, the deed, who saw it, the glass only, who mentioned it, talks, replies, "that's all I know", the median, the maximum and slow replies, breaks, still seconds, how it ended and the talk's cost;
  - the empty minutes list, each with its minute, clock, place and what the tester was doing: the content list for the friends' build.
- The run's folder is F:/LedgerTools/nightly/<date>/long-session (actions.json, verdict.json). The tester's pictures go where play.py always saves them.
- The table can be written again with `python tools/long_session.py --report <that folder> <date>`.

## How the session asks for a run

`python tools/long_session.py --request 2026-11-19` (the date is the night's own date, after midnight; the day before is also accepted as "tonight"). This writes production/playtest/nightly/long-session-request.json and plays nothing. The night walk then runs the long session after its report:
- the file is renamed `long-session-request.<night>.ran.json` before play, so it runs once;
- if the run could not end by 03:15, the file's date moves to the next night, which runs it;
- a request for a later night waits;
- one older than the night before is renamed `.stale` and not played.

The file needs no commit, because the night task runs in this working copy.

## Unverified until a real night run

- That thirty minutes of the loop stays on the street. walk_to_person's known faults are the office wall and the legs that never arrived. Repeated thirty times, they may give many "never in reach" minutes. Those will be counted, not hidden.
- That Z at night lands as the walk's morning code expects. The loop only presses Z while the clock reads 22:00 to 07:00.
- That one game launch writes one session file for the whole half hour. Two files after a crash are read by their own start times, which the selftest covers.
- That the stand-in ever answers `fallback`. Its words are not the real engine's, so the "that's all I know" count measures the stand-in only.
- The overrun near the hard stop, never measured. It is bounded by the 10-minute watchdog, but the watchdog has been tested only with a stand-in closer.
- Whether the eyes should look at the long session's pictures. They are not run on it: nothing extra is spent on the subscription.
