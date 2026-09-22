# Ruling, 2026-09-14: the leaked override lands alone, queue 273 is an invocation and not a ratchet, and five files are held at the door

STATUS: LOG, 2026-09-14. NOT CURRENT once the pin batch (queue 274) has landed
under its own ruling and the next Unreal run on or after this commit has
printed `expPinRowsLeaked=`; from then the verdict file is the reading copy and
this is the record of what was landed today, what was held, and why.

Director ruling over the batch the resident isolated on 2026-09-14, spawned
under `director_cadence` because the batch exceeds the reviewed-scope threshold
and because it changes a conclusion about why the rig was non-deterministic.
No code was written by this director. Every line number below was read this
session from the file it names.

## 1. The claim, verified before anything else

THE CONCLUSION THAT CHANGED. The rig's non-determinism was carried for weeks as
auto-exposure adaptation. It was a leaked override. Verified in three places,
in this order:

THE PRECONDITION, in the code and on the run line. `PlaceCamera` spawns the
camera actor once and moves it afterwards (`VignetteShot.cpp` 1761-1770:
`if (GCam == nullptr) SpawnActor ... else SetActorLocationAndRotation`). Its
post-process settings therefore survive the shot they were written in. Run 41
prints this in as many words: `shotCamActorStat=one-per-run/the-camera-actor-is-
spawned-once-and-moved-per-shot` (`production/d1-probe/ue-vignette-verdict.txt`
line 187).

THE FAULT, on the artifact and not in prose. Four shot lines at f6508b3 ask for
no pin and carry an override anyway, each at the value of the rung photographed
immediately before it:

    line 216  pinset_night_2         asked=0.0000  read=0.0300/0.0300    overrides=1/1  meanLuma=0.4085
    line 219  pinset_night_3         asked=0.0000  read=0.3000/0.3000    overrides=1/1  meanLuma=0.0943
    line 222  pinset_night_4         asked=0.0000  read=3.0000/3.0000    overrides=1/1  meanLuma=0.0081
    line 225  vign_grid_null_repeat  asked=0.0000  read=10.0000/10.0000  overrides=1/1  meanLuma=0.0610

One condition, `pin_setter_night`, photographed at three exposures. Every one
of those four lines printed the word `AUTO` beside `overrides=1/1`. The first
shot of the run, before any pin had been asked for, read `0.0300/8.0000
overrides=0/0` (line 189), which is what genuine auto exposure looks like on
this engine. The determinism repeat re-photographed that first shot last, after
the null repeat had left pin 10 on the component: `rigMeanLumaFirst=0.6099
rigMeanLumaRepeat=0.0518 rigMeanLumaDelta=-0.5582` (line 323). So the value
was on the verdict line for the whole run and nobody differenced asked against
read. The same shape as queue 224's sun elevation.

THE FIX, read at the write site. The decision now lives in the header g++ runs:
`ExposurePinWriteFor` (`VignetteSpec.h` 2987-3003) returns `bOverride` true
with the asked value when a pin is asked, and false with the CAPTURED values
when none is. The .cpp writes both flags and both values on every placement
with no branch of its own (`VignetteShot.cpp` 1864-1867). The captured pair is
read off the component at the first placement of the run and the capture
precedes the first write (1853-1858); nothing typed from memory stands in for
the engine's default. The repeat pass goes through the same `ApplyCondition`
and `PlaceCamera` as every shot (4144-4145), so the repeat is covered. The
tests cover the accepting case first (a pin writes both overrides on), the
rejecting case (no pin clears both and restores the captured pair), the
nothing-captured case (flags clear, values left alone), and the leaked row
planted from line 225 itself, with the predicate the run tally counts on
asserted to agree with the word (`vignette-spec-test.cpp` 3295-3348).

VERDICT ON THE CLAIM: TRUE. The flags persisted across shots; the new code
writes them on every shot, true or false, with the pre-run values restored.

THE WORD IS A REPAIR, NOT A NEW INSTRUMENT. `LEAKED-PIN` and
`expPinRowsLeaked=N/of=M/shots-asking-for-NO-pin` are a correct word on a key
that already existed and a count on a line that already existed. Jafar's rule
of today, no new instrument this month without a retirement, is about
instruments that can be misread; this one was being misread and now cannot be.
`rigMeanLumaRatio` (`FrameStats.h` 942-957) is a second statistic of the same
two numbers the line already carried as a delta. It is allowed because NOW.md
states the fault as a ratio and a reader should find the number they came for,
and it is one number twice: nobody may count the delta and the ratio as two
pieces of evidence.

## 2. The decayed sentence, and every copy of it

The sentence that this landing falsifies is, verbatim, "THE DETERMINISM TEST
MEASURES A CONDITION THE FIX WAS NEVER APPLIED TO." The fix WAS applied to it,
by leak: the repeat carried `overrides=1/1` at 10.0000. Grepped for the
sentence and for its distinguishing numbers (`-0.5582`, "sentinel predicted
DIFFERS", "change to the test and not to the fix"), case-insensitive, over the
whole repository. Three copies, no others:

    production/findings.txt:3707-3713            the 2026-09-10 entry "THE PIN WORKS"
    production/brief-input/2026-09-11.md:261-266  the Producer's dossier for that day
    production/brief-input/2026-09-12.md:262-267  the Producer's dossier for that day

DISPOSITION. `findings.txt` is newest-first and corrects by appending, never by
rewriting (the "RUN 2 CORRECTION" pattern already in that file): the resident
appends the entry dictated in section 9. The two brief-input files are what
the Producer was handed on those days and are left exactly as they were; a
corrected dossier would falsify what he was told. They are named here so the
next reader of either knows the sentence is retired.

WHAT IN THAT ENTRY STAYS TRUE. "Queue 235's acceptance cannot be met until the
repeat sits on a pinned condition" is still the expectation, for a different
reason than the one written: with the leak gone the repeat of `vign_camA_day`
is back under auto exposure, and run 39 at 83dec33 measured auto exposure with
the rate at 10000 reading DIFFERS (0.6102 against 0.9562). That is why the
next run on this commit alone is expected to print `rigDeterminism=DIFFERS`
still, and why that reading must not be read as the leak fix failing. The
reading that proves the leak fix is section 10.

## 3. The split: RULED RIGHT, with two conditions

The leak fix lands alone now. The pin batch is the next landing.

WHY. It is independent and green on its own (393/393 and 113/113 per the
resident's run of the two g++ binaries `ledger/verify.py` gates). It repairs an
instrument that was printing a false word, and every day it sits unlanded is a
day the verdict format on disk still says AUTO over a leaked pin. Holding it
uncommitted in a working tree while a builder is dispatched is the exact hazard
`findings.txt` recorded on 2026-09-08: a builder stopped mid-edit leaves a tree
verify cannot run on, and the leak fix would be hostage to it.

THE CASE AGAINST, ANSWERED. The resident's own worry is correct as far as it
goes: this commit makes leaked rows honest, it does not make the rig
deterministic, because 23 of 27 conditions at HEAD still ask for nothing and
adaptation is still in force on every one of them. A half-fix that looks whole
is a hazard only if the record lets it look whole. Two conditions:

1. NOW.md and the commit message say in one sentence that this commit does not
   make the rig deterministic, that `rigDeterminism` is expected to read
   DIFFERS on it, and that the reading which proves it is section 10.
2. The pin batch is not deferred behind a generator rewrite. Section 4 says
   why: the generator already does what 273 asks of it.

## 4. Queue 273: the characterisation is WITHDRAWN. It is an invocation, not a ratchet

THE FINDING. `ledger/CoreTests/Program.cs` takes `--ahead-of-run <sha>`
beside `--write-vignette-pieces` (lines 39-58). `WriteVignettePieces(ahead)`
reads `pieces_then` off the named run's own verdict rather than accepting a
typed number (20712-20743) and writes the key only into the file that has a
live gap (20745-20770). The drift check feeds the committed key back into the
regeneration before it compares bytes (20875-20887), which is exactly so that
a file carrying a current key regenerates identically. And the failure that
273 quotes printed its own remedy on the same line, at 21115-21117:

    either land a Unity run, or regenerate with:
    dotnet run -c Release --project ledger/CoreTests -- --write-vignette-pieces --ahead-of-run cb4767e

The item's measured sequence ran the flagless command, which by design spends
the key ("Absent, no key is written and the check is the strict count
comparison it has always been", lines 44-45), and then concluded that no state
satisfies both checks. The state it did not try is the one the failure named.
This is `.claude/rules/ci.md`'s first rule in miniature: the entry point was
cheaper than the argument, and it was printed. Rule 3 applies to the
instrument: the instrument here was the invocation.

The route is also not new. The committed file at HEAD, 610 pieces against a
run that counted 593, was produced on 2026-09-10 by this same flag for the
fascia package, and the comment at 20745-20759 records the guard refusing a
mis-stamped key on that day. A guard pair that has passed a real layout change
is not a pair no legitimate change can satisfy.

SO THE RULE 5b CHARACTERISATION IS WITHDRAWN. Each check passes on its
accepting state, and the pair passes on the flagged regeneration. That last
clause is a prediction from reading the code and is NOT a measurement, so:

THE MEASUREMENT ORDERED, the cheapest decisive one. With the builder's scene
in place (the scratchpad copy `vignette-scene.builder.json`), run

    dotnet run -c Release --project ledger/CoreTests -- --write-vignette-pieces --ahead-of-run cb4767e

and read the `ahead-of-run cb4767e piecesGap=... keyWrittenInto=...` line and
both checks ("regenerating the piece list from the live tree changes nothing"
and "the piece list Unreal reads has as many objects as the Unity run the
stills came from, or declares in the file that it is ahead of it"). If both
are green, 273 closes as this ruling describes. If either is red, the printed
line is the finding and 273 reopens on it, not on the ratchet theory.

WHAT 273 DID FIND, which survives it and becomes the item:

- The key's own `remove_with` text names only the flagless command, which is
  the one command a reader in the ahead state must not run for a scene change.
  One line: add a `regenerate_while_ahead` entry naming the flagged command.
  That is a change to the writer in Core and goes through a builder.
- UNDER D16 THE ANCHOR IS DEAD. Question three judges the file against the
  newest landed UNITY run (`game-design/sim-shots/runs`, 21077-21091). The
  engine is Unreal, so no newer Unity run will ever land, `cb4767e` is newest
  for ever, and the key can never be spent. The code's own words at
  `StreetVignettePieces.cs` 838 apply: an acknowledgement nobody re-reads is a
  waiver. The successor item re-anchors question three to the count the
  Unreal verdict already prints (`piecesEmitted=N/M` on its scene line) or
  retires the Unity comparison with its reason written down. Not this batch.

The resident rewrites 273's status and title to this. The "what must not be
done" paragraph (do not delete the cross-engine check) stands.

## 5. Queue 274: the three are atomic, and they are blocked on one measurement, not on 273

The atomic-set finding is right and was measured properly, one file at a time.
HEAD's `Program.cs` pins the count as a literal, `pinned == 4 && unpinned == 23`
(19631); the builder's copy replaces it with an invariant (scratchpad
`Program.builder.cs` 19625-19703): every sun-on condition carries a pin, every
sun-off condition carries none, and the day conditions that are not rungs
share one value, with three plants each breaking one clause and all three
watched. HEAD's scene has 4 of 27 conditions pinned (the four rungs, read off
`production/specs/vignette-scene.json`); the builder's has 22 day conditions
at 0.300, the four rungs, and two sun-off conditions at 0.000. The invariant
cannot be satisfied by HEAD's scene, and the new scene cannot reach the probe
without regenerating the pieces. Atomic, as 274 says.

274's blocker changes from "273 frees the generator" to "the measurement in
section 4 is green". When it is, the pin batch lands under ITS OWN director
ruling, because it is a Core change and a spec change. That review is not this
one, but two things it will turn on are stated now so nobody argues them in
the moment:

- 0.300 is a MEASURED rung, not an interpolation. The ladder printed it:
  `ladder.pin0.3000.afterDayMeanLuma=0.6590 afterNightMeanLuma=0.6591
  ClipHi=0/921600 ClipLo=0/921600 pinHeld=2/of=2` (verdict line 321). It is
  chosen for determinism, which is D28 step 1, and not for matching the
  reference's mean, which `findings.txt` already says was never the goal. The
  finer ladder toward the reference's 0.4102 inside the 0.300..3.000 bracket
  is the next rung and is not a blocker.
- Night stays at auto by section 3 of the 2026-09-10 ruling. With the repeat
  taken of shot 0 (`vign_camA_day`, sun-on, pinned), queue 235's acceptance is
  met literally by an IDENTICAL repeat on a run that contains night
  conditions, while night frames remain non-comparable across shots. The pin
  batch's ruling says that plainly rather than letting IDENTICAL on one line
  read as a deterministic run.

## 6. The verbatim research waiver: CORRECTLY NARROW. The five files: HELD AT THE DOOR

THE WAIVER IS APPROVED. `RESEARCH_VERBATIM` is a frozen tuple of five
repo-relative names (`tools/producer-check.py` 330-338) that widens only in a
reviewed diff; `RESEARCH_WAIVED_RULES == ("banned",)` and the selftest asserts
exactly that (1939-1941); `linkcap` and `linkdest` still refuse a listed file
(1942-1953); membership is by name through `rel_under` at the sender's own
call site (3720-3726) so the sender and the gate name one file one way; and
the walk grades every listed file twice in one run with the one contributor
toggled, so the ladder prints what the waiver changed and for how many
(3379-3388, 3487-3495). Listing kcd2 by category rather than by failure, and
printing that the waiver did nothing for it, is the right shape: an
arrangement by omission would have been a list of four. The reading
`researchVerbatimWaiverBit=4/5` is the resident's, from its own run of the
gate; this director did not run it and does not restate it as its own.

THE FIVE FILES DO NOT LAND IN `production/outbox/` IN THIS COMMIT. Rule 4: I
opened one. `2026-09-14-research-coverage-audit-kcd2.answer.md` is 109 lines,
91 of them non-empty, at the width of ordinary prose; the other four are 79 to
88 non-empty lines each. `tools/runner/executor.py` 178-182 states the
consequence in its own words: Telegram rejects a sendMessage over 4096
characters, nothing in the outbox sweep splits a long message, and a refusal on
the wire retries every two minutes for ever. Queue 260, the permanent-red
sweep, is still open in `production/queue/`. The bot on his PC started at
2026-09-13T01:14Z and its checkout is reset to `main` about once a minute;
whether it is still up cannot be told from here, NOW.md says so, and if it is,
five files over the cap on `main` are five permanent refusals within minutes,
each writing a record per pass: the 304-refusals incident of 2026-09-07,
times five, on the first day the meter is back. If it is not up, the same
five refusals begin the moment it is restarted.

THE NUMBER THIS RESTS ON IS NOT YET PRINTED. Line counts are not character
counts. Before anything moves: `wc -c` on all five, printed in NOW.md beside
4096. Any file the count puts under 4096 goes to `production/outbox/` as
staged. Any file over it goes to `production/outbox-blocked/` in this commit
with one line in that directory's README naming the count, the cap, and queue
260. The `RESEARCH_VERBATIM` tuple stays as written: the gate already prints
an entry that is not on disk as absent (3478-3482), which is the honest
reading while they are held.

THE DELIVERY ROUTE IS ONE QUEUE ITEM, filed by the resident, not decided here:
Jafar's word was "in full, as its own message", and Telegram's cap makes one
message impossible for a text of this length. The two routes that honour "in
full" are consecutive numbered parts cut at paragraph boundaries, each part
named on the frozen list, or a document send. Which is his call or the next
director's with the counts in hand; neither is a change to the words.

## 7. Group 2, the daemon half of queue 261: LANDS

`executor.py` gains `cli_start_keys` (328-360), pure: `cliLastStart`
last-wins, `cliWhy` in `run_session`'s own words so not-on-PATH and
would-not-start stay distinct, `sessionsStarted` cumulative and never `0/0`,
the words until the first attempt. The keys are written to the status file
(1293) and read by `supervise.py: executor_keys` (328-366), which prints
`nothing-measured/key-absent` for a status file from an older process and
`nothing-measured/no-status-file` when there is none (324-325), which is the
state the first run after this lands will be in. Both selftests drive both
outcomes (executor 2273-2343, supervise 1070-1112). This is deliverable 2 of
the 2026-09-11 ruling, section 5, as ordered. No bound is set on any of it.

DELIVERABLE 1 IS NOT IN THIS TREE AND IS STILL OWED: the install workflow
carries no `executor-status` or `executor-journal-tail` step (grepped
`.github/workflows/ledger-install-supervisor-task.yml`, no hits). 261 stays
open on that and on its accepting run, a session that starts and publishes
the keys, which cannot happen until the CLI starts on his machine.

## 8. Group 3: lands, with four corrections the resident applies before committing

1. `game-design/decision-2026-09-14-ruling-twelve-rulings-the-visual-week-and-
   the-producer-may-step-down.md` says the index "lists 30 D-files against 30
   on disk". `D31-the-visual-path.md` is on disk and on the index (rulings-log
   line 76). The sentence becomes "lists 31 D-files against 31 on disk, D31
   having been added by the plan ruling of the same day". A count is a reading
   at an instant, as rulings-log's own header says; quote it with its instant.
2. THE TREE CARRIES MORE THAN THE BRIEF LISTED. HEAD is 074f85b5 at
   2026-09-14T04:15:19Z (`.git/logs/HEAD` lines 35-36, nothing after), so
   D31, `production/stages.md`, `production/ladder.md` and `game-design/
   decision-2026-09-14-ruling-the-plan-is-two-documents-and-the-phases-fold.md`
   are uncommitted too. They are documents and a director's record of a plan
   ruling, and they commit on the resident's read. NOW.md names them as part
   of this landing so the commit does not carry files nobody listed.
3. Queue 273 and 274 are rewritten per sections 4 and 5. 273's title becomes
   "the key's remove_with names the spending command, and question three is
   anchored to a retired engine"; 274's status becomes "BLOCKED on the flagged
   regeneration reading green, then its own director ruling".
4. NOW.md gets an entry for this landing carrying: the leak, in one sentence
   with the four line numbers; that this commit does not make the rig
   deterministic and what the next run must print (section 10); the five
   character counts beside 4096 and where each file went; 261's deliverable 1
   still owed; and which director wrote which of today's two records.

Also seen and allowed: D5 and D15 carry their SUPERSEDED lines in-file (each
at line 3) and in the index (lines 50 and 60); the budget row is at
`production/budget.md` line 43; queue 273 and 274 exist as filed.

## 9. Dictated text the resident hand-applies, and nothing beyond it

A. `ue-probe/Source/LedgerProbe/Private/VignetteShot.cpp` lines 1486-1490, the
comment in `ApplyCondition`, still ends "and PlaceCamera then writes no
override at all." That sentence is now false and it is the one the leak hid
behind. Replace the final clause with: "and PlaceCamera then writes the
override flags FALSE and restores the captured clamp values, 2026-09-14; see
the LEAK block at the write site." One sentence, no other edit to that file.

B. `production/findings.txt`, appended above the newest entry, verbatim:

    --------------------------------------------------------------------------
    2026-09-14  CORRECTION TO "THE PIN WORKS" (2026-09-10): THE DETERMINISM
                REPEAT WAS PHOTOGRAPHED UNDER A LEAKED PIN, NOT UNDER AUTO.
    --------------------------------------------------------------------------
    The entry below says the determinism test "measures a condition the fix
    was never applied to". It was applied to it, by leak. The camera actor is
    spawned once and moved (verdict line 187, shotCamActorStat=one-per-run),
    and the two AutoExposure override flags were written only when a condition
    asked for a pin, so they stayed in force for every shot after. Run 41's
    own shot lines carry it: pinset_night_2/3/4 and vign_grid_null_repeat ask
    0.0000 and read 0.0300, 0.3000, 3.0000 and 10.0000 with overrides=1/1,
    printed as AUTO (lines 216, 219, 222, 225). One condition, three mean
    lumas: 0.4085, 0.0943, 0.0081. The repeat of vign_camA_day (0.0518 against
    0.6099) inherited pin 10 from the last shot. THE VALUE WAS ON THE LINE FOR
    THE WHOLE RUN AND THE WORD BESIDE IT SAID THE OPPOSITE, the same shape as
    queue 224's sun elevation. Fixed at the write site with the decision moved
    into VignetteSpec.h where g++ runs it; the word is now LEAKED-PIN and the
    run line counts expPinRowsLeaked with its denominator. What the old entry
    still gets right: the repeat sits on an unpinned condition and, with the
    leak gone, is back under auto exposure, which run 39 measured as DIFFERS
    on its own; so rigDeterminism on the leak fix alone is expected to read
    DIFFERS, and the reading that proves the fix is expPinRowsLeaked=0 over
    the rows that could have leaked. Ruling of 2026-09-14, the leak lands
    alone. The copies of the retired sentence in brief-input/2026-09-11.md and
    2026-09-12.md are what the Producer was handed and are left as they were.

## 10. What the next Unreal run on or after this commit must print, and what it must not be read as

No threshold is set here; these are the keys and the readings that decide,
with their denominators.

- `expPinRowsLeaked=0/of=<rows asking for no pin>` on the run line. The
  denominator is the rows that COULD have leaked, not the shot total, as the
  test at `vignette-spec-test.cpp` 3482-3491 fixes it.
- No shot line asking `0.0000` carries `shotExposurePinOverrides=1/1`; every
  such line reads `AUTO` with `shotExposurePinRead=` at the captured pair.
- The three `pin_setter_night` rows read the same exposure family as each
  other, which is what one condition looks like when nothing leaks.
- `rigDeterminism` is EXPECTED to read DIFFERS on this commit alone, because
  `vign_camA_day` is unpinned until the pin batch lands. That line is not the
  proof of the leak fix and must not be reported as its failure. The proof is
  the first bullet.

The Unreal runner has been offline since 2026-09-11T08:18 (`pc-results`
unmoved), so nothing here can be dispatched tonight; the run is armed by the
first commit that can reach it, with the four readings above named in the
dispatch record.

## 11. What this director refuses

- The five verbatim research files in `production/outbox/` before their
  character counts are printed and read against 4096 (section 6).
- Any edit to `production/brief-input/2026-09-11.md` or `2026-09-12.md`.
- Any change to either CoreTests check, or to the cross-engine anchor, in
  this commit; both are the successor item in section 4.
- Any sentence in NOW.md or the commit message that calls the rig
  deterministic on this commit.

Spawn row named below is the newest `studio-director` row in
`.claude/agent-log.tsv` (line 580, agentId ab8dc97171d9eb224), the spawn that
wrote this record. The 13:18:58Z row on line 575 is a different spawn and is
not claimed by this record.

<!--RULING spawn=2026-09-14T13:39:10Z-->
