# one-sim: progress (task 4s, "one simulation in the browser")

Run 1, 19 November 2026, 13:19 to 14:12 UTC, in the cloud. Written by the building helper. Nothing here has had a fresh reviewer yet.

## Where it stands, in five lines

1. Way picked: the game's own C++ town code (the Unreal port) compiled to WebAssembly. Reasons and the comparison with the other two ways: production/research/lane/ONE-SIM-METHOD-2026-11-19.md.
2. It is built and it runs in a real browser (headless Chromium 157). The download is 80 KB compressed.
3. It gives the C# Core's answers: all 102,949 comparable golden rows, 8,568 routine hours and 225 hours of six scripted weeks, the last two through the new front door.
4. The C# Core, the reference, was rebuilt and re-run here today: its table is the committed one, CoreTests passes (5,255 checks), Soak passes (9 checks).
5. Not done: the bridge into the prototype, and the list of where the prototype's frozen JavaScript differs from the real rules. First notes for both, with a few measured facts, are under Next.

## Done, with evidence

Everything below comes from one command, last run from scratch at 14:05 UTC with the files as they are now: `tools/lane/one-sim/one-sim.sh all`, 148 s, exit 0, last line "one-sim: everything passed". Logs are in /home/claude/one-sim-work/logs/ (outside the repository, so they do not last: the numbers are copied here).

Step 1, the study: production/research/lane/ONE-SIM-METHOD-2026-11-19.md. Written, sources dated, unreached and unverified things listed. Not yet reviewed.

Step 2, the build and its tests:

| Name in the output | What it checks | Result |
|---|---|---|
| reference: built | PerceptionGolden, Soak and CoreTests built from the real Core (140 files) by path, .NET SDK 8.0.428 | built, no errors |
| C# goldens | The table the Core writes today against the committed one (ue-probe/perception-golden) | 102,960 rows, 267 rules, identical byte for byte |
| Soak | The Core's own soak check | ok, all 9 checks passed |
| CoreTests | The Core's own tests | "All 5255 checks passed.", exit 0, 11 s |
| port-test-as-wasm-game-flags | The port's own golden test (ue-probe/tests/core-port-test.cpp, unchanged) as a WebAssembly program, built with the game's flags | 102,993 checks, 0 failures over 102,949 rows, 0 unanswered, 11 skipped by name (7 claims, 4 FactNull) |
| port-test-as-wasm-with-exceptions | The same with C++ exceptions on | 102,997 checks, 0 failures over 102,953 rows, 7 skipped (claims) |
| T1 golden rows through JavaScript | Every row asked through the loader, no files (data handed in as text) | 102,949 agree, 0 differ, 0 unanswered, 11 skipped by name |
| T1b, T1c | Only the two named holes are skipped; the 3,500 seeded GossipFuzz rows are among those checked | ok |
| T2 routines through the bridge | Where each person is each hour, both cast files, against the Core's CastPlaceOf rows | 8,568 of 8,568 |
| T3 the week hour by hour through the bridge | Six scripted weeks played by calls from JavaScript, each hour's 13 fields against the Core's TownWeekHour rows | 225 of 225 |
| T4 the same calls twice give the same town | Determinism: a digest of every hour, the final state and every held story | 37e81244f129619f both times, in Node and in Chromium |
| T5 | Speed and size | about 15 ms a game day (41 people; 13 to 18 ms over ten runs); one-sim.wasm 301,665 bytes, 102,362 gzip, 79,767 Brotli; loader 6,870 bytes |
| T7 the Ledger's facts through the front door | Who knows what and how (os_knows), read back after every scripted hour | at all 225 hours the number of facts is the hour's own count (held to the C# Core by T3); nobody but the witness is said to have seen the window go; the witness holds it first-hand, recognised, at 130 of 130 hours after the deed |
| T6 the front door takes rough handling | Calls before a town exists, broken cast files, times that are no time (refused at the door), answers outside the list, odd and long text, a thirty-day jump, a second town | nothing fell over; the thirty-day jump about 0.16 s |
| selftest | Four rows spoiled on purpose must be caught, each by its own check | passed 7 of 7 |
| browser | The same checks inside a real page, headless Chromium 157.0.8103.78 | all passed |
| breaks (run apart: `one-sim.sh breaks`) | Seven one-line breaks planted in a copy of the port. Do T2 and T3 see them? | 5 of 7 seen. See findings 2 and 3. |

About "CoreTests' cases where they can run": CoreTests is C# code that calls the C# Core, so it runs on the reference side only (all 5,255 checks, above). What it shares with the port is the golden rows, and every row was asked of the browser copy.

The front door (wasm/one_sim.cpp) has 25 calls: a town from a cast file, one game hour in the game's order, the player's acts between hours (the deed, the answer to the ask, the tea, the week's end, a police report, being taken in), and reading back (where someone is, the week's state as the save writes it, and who knows what and how: saw it or was told, how many tellings away, from whom, how well the first witness saw him, how sure).

## Findings for whoever owns the port and the table (not fixed here, nothing under ue-probe/ or ledger/ was touched)

1. FirstWeek.h declares AdasTea::Ada in a way the C++14 standard needs a second line for. g++ accepts it. clang does not link it under C++14 ("undefined reference to LedgerCore::AdasTea::Ada"). Tried today with this machine's clang++ 18 and the exact command tools/port-golden-check.sh uses when g++ is missing (-std=c++14 -O1): the port test does not link. So that script's clang path is broken today; its g++ and MSVC paths are not affected as far as seen here (MSVC not tried). The browser build uses C++17, where it is fine.
2. Planted break, seen by nothing: removing `Week.Close(Now, Mill, Cast);` from TownWeek.h HourEnd fails no golden row (all 102,949 still agree) and changes nothing in the six scripted weeks. The week's end closing each hour is not pinned by any row.
3. Planted break, seen by nothing: swapping the two nine o'clock calls in TownWeek.h RunHour (DS Ellis before the witnesses' reports) fails no golden row. The TownWeekSteps rows record the step names, which are typed beside the calls, not the calls. Today the swap probably cannot change any outcome, because only damage is ever reported and she comes for a crime only from wounding up (K2's reading). It will matter with the first serious crime.
4. The golden reader asks for town-news.json through the same hook as the cast files. A host that hands in only the two cast files gets four rows unanswered (TownNewsWitnesses and three KeepsHisDeeds). Not a fault, but easy to trip on.

## Next (run 2 onwards), in order

1. One fresh reviewer for the study and for this build (project rule). A fresh helper should also try to break the front door: calls in odd orders, a bad cast file, a town never made.
2. Step 3a, the plain bridge for the prototype. A first map from one reading of the prototype's source today (names only, not checked line by line):
   - clock.js simStep is the prototype's tick (read today): it moves the clock, then stepPeople (routines.js), then perceiveTick (seeing.js: who sees Tom, by the prototype's own geometry), and on their own timers gossipTick and decay (gossip.js). The police run and the story step are called from elsewhere; not traced today.
   - routines.js slot() answers "where is this person now". The real rule is CastDay PlaceOf (os_place_of). The place names differ: the prototype's map.js against the cast file's places and areas. A table between the two is needed.
   - seeing.js witness() and events.js remember() make a memory in the prototype's own shape. The real rules are Perception, Observation and Sighting (how well he was seen, the "rung"), then GossipMill Witness. The door needs a call "this person saw this act at this rung", fed from the prototype's geometry.
   - gossip.js gossipTick and tell are the town's talk. The real rule is the hourly rounds (os_hour and os_rounds_to already run them).
   - ledger.js truthTable and ledgerSeen feed the Ledger screen. The real source is who knows what and how (os_knows, checked by T7) plus the police file (inside os_state).
   - state.js G.minds, G.events and G.ledger are what the save holds today. The real save is TownSave (in the port, not yet behind the door).
   The rest of this item, as planned: Read tools/lane/prototype/project/src (main.js, state.js, events.js, seeing.js, gossip.js, routines.js, ledger.js, police.js) and write down what the prototype would call each tick and what it would read back. Likely new calls: a sighting from the prototype's own geometry into the town (GossipMill Witness with its rung), the town's talk run to the minute (RoundsTo is there), save and load. The real save is three texts (read today in the port's own notes): each person's memory as markdown (MemoryStore), the rumours as JSON (SaveCodec.h), and the week's pieces (TownSave). None is behind the door yet. A good first test: save at some hour, load into a fresh module, play on, and get the same digest as a week played straight through.
3. Step 3b, the list of every place the prototype's frozen copy differs from the real rules, with what changes for the player. Start from production/lane/PROTOTYPE-RULES-READ-2026-11-18.md (its rule ids) and production/lane/PROTOTYPE-VS-DESIGN-2026-11-18.md. First facts, measured today by a throwaway script that read both cast lists (prototype src/cast.js, real production/specs/hook-cast.json):
   - The two casts are different lists of the same street. The prototype has 28 people, all named. The real cast has 41 people, 9 of them named.
   - The 9 named in the real cast are all in the prototype too: Ron Kirby, Sheila Dunn, June, Darren Milner, Ada, Alison Sedman, Rita, Hal, Father Walsh. Five of them carry a different id on each side (the real file's ids are rocco, lena, sam, noor and emil for Ron, Sheila, Darren, Alison and Father Walsh). The bridge needs an id table.
   - 19 prototype people have no named match. Twelve of them fit an unnamed job in the real cast, matched by eye on the job's words (the dispatcher, the day and night drivers, the pawn's back-room hand, the woman from the fish shop, a hand on the quay, a customs officer, Father Walsh's housekeeper, the boarding house keeper, the scrap dealer, the night watchman, the sign painter). The prototype gave them names (Pauline Kitching, Kevin Needham and so on). Which names stand is a canon question for him, not for the bridge.
   - Five prototype people have no place in the real cast at all (the caff's keeper, the takeaway's two keepers, the retired trawlerman, the woman laid off from the laundry), and 20 real people are not in the prototype (most of the laundry, the docks, the pawn's staff, the ferry, the chapel's cleaner, the outfit's man).
   - The last two of the 19, DS Ellis and PC Ibbotson, are people who walk about in the prototype. In the real rules they are steps of the hour (her visit at nine, the constable at ten), not members of the cast.
   - One routine side by side, Ron on a weekday. Real: off until 7, cafe, the rank from 8, the fish shop's front at 12, the rank from 13, the quay from 17, the office from 19, off at 23; Sundays differ. Prototype: home, the caff from 6:36, the rank from 8:06, the fish queue at 12:18, the rank from 12:48, the takeaway's queue at 17:24, the rank from 18:30, home at 23:36. For the player: with the real rules Ron is on the quay and then in the office in the evening, not at the takeaway and the rank, and people move on the hour, not at odd minutes.
   - Not yet looked at: the prototype's heat fading by its own formula (e^(-minutes/1700)), its seeing and naming rules against Perception and Sighting, its gossip against the hourly rounds. Money, fares, jobs, fights and talk have no port at all, so they stay in JavaScript or wait for a port.
4. More of the Core's own checks against the browser copy where rows exist: SaveChaos, StrangerTest and PerceptionGolden's GossipFuzz are C# programs; only the last has rows the port answers. A same-seed week trace written by a small C# program beside the bridge would widen "same results on the same days" beyond the six scripted weeks.
5. A Web Worker wrapper, so a long catch-up (many hours at once) never freezes the page. One game day costs about 15 ms and a thirty-day jump about 0.15 s, so this is not urgent.
6. If he picks B in the study's section 6: a GitHub build machine job that builds the C# Core for the browser, behind the same front door, held to the same checks.

## Blocked, and why

- The C# Core compiled for the browser (way a): the cloud's network refuses NuGet and Microsoft's download sites (403 at the gate for api.nuget.org, www.nuget.org, globalcdn.nuget.org, dot.net, builds.dotnet.microsoft.com, dotnetcli.azureedge.net). Not a fault of the method. Needs a GitHub build machine or those hosts allowed. Nothing was tried to get round it.
- Publishing anything with one-sim.wasm inside: needs his licence lines first (study, section 4 and 6). wasi-libc's full licence text and the notice of the compiler's helper routines are still to be read.
- Emscripten was not tried: its download site (storage.googleapis.com) is refused too. Not needed for this way.

## Exact commands

From the repository root, Linux, two processors are enough. Heavy steps run at low priority (nice 15) and one compile at a time.

    tools/lane/one-sim/one-sim.sh setup       # once (12 s here, tried from nothing in a second folder). Fetches, with checksums:
                                              #   dotnet-runtime-8.0.34 and dotnet-sdk-8.0.428 from conda-forge (157 MB)
                                              #   wasi-sdk-34.0-x86_64-linux.tar.gz from GitHub releases (192 MB)
    tools/lane/one-sim/one-sim.sh all         # reference, wasm, test, selftest, browser: about 3 minutes
    tools/lane/one-sim/one-sim.sh reference   # the C# Core: build, golden table, Soak, CoreTests (about 45 s)
    tools/lane/one-sim/one-sim.sh wasm        # the four WebAssembly builds (about 2 minutes)
    tools/lane/one-sim/one-sim.sh test        # under Node
    tools/lane/one-sim/one-sim.sh selftest
    tools/lane/one-sim/one-sim.sh browser     # needs Python's playwright with Chromium, as the prototype's tests do
    tools/lane/one-sim/one-sim.sh breaks      # the seven planted breaks (about 2 minutes)

Things to know:

- Everything large is in /home/claude/one-sim-work (set ONE_SIM_WORK to move it): the three downloads 334 MB, the .NET SDK unpacked 555 MB, wasi-sdk unpacked 635 MB, build output. (This run also left 90 MB of conda-forge's package index there, used once for the study.) None of it is in git. tools/lane/one-sim holds text only, the largest file under 20 KB.
- `reference` needs the right to mount: the C# check programs look upward from their own folder for the repository's data files, so they run under a folder of links into a read-only view of the repository (a read-only bind mount at $ONE_SIM_WORK/ro-repo). The script takes the view down again after use. Without mount rights it says NOTHING MEASURED and runs nothing against a writable repository.
- The built one-sim.wasm is at $ONE_SIM_WORK/wasm/one-sim.wasm (one-sim.full.wasm keeps the names for debugging).
- Only Chromium was on this machine. Firefox and Safari's engine were not tried (Playwright had neither installed). The module asks for nothing beyond plain WebAssembly: no exceptions, no threads. That is a reason to expect it to work there, not a test.
- Exit codes: 0 good, 1 a check failed, 2 usage, 3 nothing measured.
- Versions today: Node 22.23.5, Python 3.13, g++ 13.3.0, Chromium 157.0.8103.78 (Playwright 1.63.0), wasi-sdk 34.0 (LLVM 23.1.0), .NET SDK 8.0.428.
