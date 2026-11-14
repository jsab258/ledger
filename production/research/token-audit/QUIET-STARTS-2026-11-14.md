# Quiet starts: what the launcher costs between rounds (14 November 2026)

Asked by advisor 160 (14 Nov 20:12). Method researched: HANDOVER-START-2026-11-12.md (the launcher's behaviour, read from the session logs) and tools/token_audit.py's prices; measured, not guessed: every run of 14 November from 06:06 to 20:21, priced step by step from its own log.

## Before (14 Nov, 69 runs, US$79 of the day's US$89)
- A run whose gate says WAIT: 2 steps, US$0.46 (US$0.74 when the shared start had left the cache). About 45 of them: about US$22.
- A run that goes, finds nothing due, reads the page, writes a row and stops: 7 to 13 steps, one minute, US$1.27 to 1.89, average about US$1.45. 14 of them: about US$21.
- Working runs (rounds 6, 7, 8 and this evening's): 4 runs, about US$28 with the session's part of each round (the fixers' helpers are counted apart).
- So about US$43 to 48 of the day went to starts that did no work; a Kiln round costs about US$9.24.
- Why a start costs what it does: its first step writes about 80,000 tokens of tools, skills and project files to the cache. On Fable that is US$0.43; on Opus 5.5, by the same list prices, about US$0.17.

## What changed today (in the session's reach)
- tools/fresh_gate.py honours a handover line "**Next due:** YYYY-MM-DD HH:MM": after a clean stop no session starts before it, except one page check each 55 minutes (his taps and the advisor's rows still read within about an hour). Before: a start about every 45 minutes (the 30-minute cap of 13 Nov plus the quarter). Checked by its self-test (58 cases) and on the real handover at six times.
- A quiet check writes no row when the handover states the next time and the last row says so (advisor 160: a stated next time is planned silence).
- Expected: quiet starts from about 14 to about 10 a day, about US$6 a day. Small: the WAIT runs are untouched.

## What is not in a session's reach (on his page, 14 Nov 20:31)
- The model of the scheduled task. RULINGS 8 and 10 Nov set Opus for the session; the task runs on Fable. On Opus every start and every step costs about 40% as much by list prices: about US$25 a day saved on quiet days.
- Not asked now, for a later look: the schedule's quarter-hour (each WAIT costs a full start; a half-hour schedule would halve them, at the price of slower handovers when a session ends early).

## Tomorrow's DAILY file
Runs by kind (WAIT, quiet start, working) with their dollars, beside the rounds' dollars, for 14 and 15 November.
