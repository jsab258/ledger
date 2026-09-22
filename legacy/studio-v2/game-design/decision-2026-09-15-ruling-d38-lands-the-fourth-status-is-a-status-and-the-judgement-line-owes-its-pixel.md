# Ruling, 2026-09-15 (19:43Z spawn): D38 lands as four files, the fourth status is a status and every tally keeps it apart from absent, the five citations were re-read against the code and all five turn out measured, the board's judgement line is derived and read back and its pixel is owed as a printed line, the sleep pair goes to Jafar, and the tally readback guard is queued

STATUS: LOG, 2026-09-15. NOT CURRENT once the commit this record stamps has
landed with the two printed lines pasted into section 6 and the dictated
edits of section 7 applied; from then `production/systems-inventory.json`,
`tools/systems-inventory-check.py`, `tools/map.py` and `map.html` are the
reading copies and this is the record of what was ruled and why.

Director ruling on the batch that lands D38 (recorded 2026-09-14, applied to
nothing until tonight). Escalated because `director_cadence` reads
`DIRECTOR NOT SPAWNED`, 646 changed lines against the inherited 100,
`workByScope=tools:630/claude:16`. The builder that wrote the batch hit its
turn limit three times and delivered no report, so every claim below is read
off the tree and not off anybody's account of it. This director has no shell:
every number here was read from the file and line it names in this session,
or is arithmetic shown in full. Where a number could only come from running a
tool, the record says NOT PRINTED THIS SESSION and orders the print rather
than quoting a docstring.

Author: tier-1 director, stamp at the foot naming row 638 of
`.claude/agent-log.tsv` (`2026-09-15T19:43:24Z` TAB `studio-director`,
agentId `a8aa7c79263ef588c`). Rows 636 and 637 (`instrument-builder`,
`a9e72a497501cc44e`, 18:46Z and 18:58Z) are the D38 builder's rows and are not
claimed. Row 639 (`instrument-builder`, `ad2014bdb3f3b9999`, 19:44:56Z) was
spawned ninety seconds after this director and is not claimed either; see
section 10. The reference commit is `e4d8cfe1` ("Ten hours, and the brief
asks for the reading"), which `.git/logs/HEAD` line 101 dates to epoch
1789500301, 19:25:01Z, so row 638 is newer than the reference and no earlier
director row (634, 07:55Z) could carry this batch. The resident never writes
the stamp.

## 0. What was opened

`ledger-v2/respec/decision-register/D38-*.md` whole, `D39-*.md` whole,
`rulings-log.md` whole; `tools/systems-inventory-check.py` whole (1076
lines); `production/systems-inventory.json` whole (1766 lines) plus a grep of
every `"status":`, `"typedBy": "jafar/` and `"short":` line; `tools/map.py`
1 to 400, 2130 to 2310, 2370 to 2590, 2594 to 2800, 2800 to 3000, 3340 to
3370, 4022 to 4072, 4200 to 4350, 4380 to 4490, 5207 to 5470, 5540 to 5620,
5990 to 6060, 7600 to 7700, and a grep of every `ruled`, `judgement`,
`jafar`, `D38`, `D39`, `ruledout` and `⊘` site (7700 lines); `map.html` 1 to
45 and 236 to 255 whole, and lines 256, 274, 275, 278 to 294 by extracted
match (the page is 298 lines and 138k tokens, the picture is on line 281);
`ledger/verify.py` 1455 to 1535, 6585 to 6725, 7308 to 7328 and the `RULING`
regex at 3552; `tools/docs-check.py` 108 to 122 and 517 to 522;
`tools/publish-glance.py` 244 to 268; `.github/workflows/publish-glance.yml`
by grep; `.claude/agent-log.tsv` 618 to 639; `.git/HEAD`,
`.git/refs/heads/main`, `.git/logs/HEAD` 100 to 101; `production/NOW.md` 1 to
80; `production/queue/` by glob for the top numbers (314 is the highest on
disk, live directory); and the code the five tiles cite:
`ledger/Assets/Scripts/Core/Traces.cs`, `Core/Gossip.cs` 240 to 279,
`Core/Arsenal.cs` 320 to 355, `Core/Coat.cs`, `Core/Occupancy.cs`,
`Game/EvidenceHost.cs`, `Game/ViolenceHost.cs`, `Game/GameController.cs`,
`Game/WorldBuilder.cs`, each by grep for the symbol named, and
`game-design/sim-shots/verdict.txt` lines 90, 92 and 98 by extracted match.

## 1. The ruling

THE BATCH LANDS. No builder round. Before the commit the resident applies the
four dictated edits of section 7 (three strings in the inventory's own
`howToRead`, one three-line comment in the checker), regenerates the page
once and pastes the two printed lines into section 6, and files the three
queue items of section 8 by name. One question goes to Jafar through the
Producer (section 9), a second only if the printed pixel makes it one.

Why it lands rather than goes back: every claim the brief made about parts 1
and 2 survived being re-read against the code (sections 2 and 3), the page
was opened and reads as the ruling asked (section 4), and the one place the
fourth status could have been lumped back into absent was checked at every
site that counts, colours or tallies it and none does (section 5). What the
batch lacks is a guard, a pixel and three lines of reading notes, none of
which is a reason to hold D38 a second day.

## 2. Part 1, the schema, verified

`tools/systems-inventory-check.py` 131: `STATUSES = ("exists", "partial",
"absent", "ruled-out")`. 136: `NOWHERE_STATUSES = ("absent", "ruled-out")`,
used at 503 (no `where` on either) and 617 (no `evidence` on either), which
groups the two for the one property they share and nowhere else. 143:
`RECORD_IN_NOTE_RX = r"\bD\d+\b"`. 511 to 530: a `ruled-out` tile whose note
names no D-number is REFUSED (516 to 521), and one whose D-number resolves to
no file under `ledger-v2/respec/decision-register/` is REFUSED (522 to 528);
a resolved pair goes into `ruledOutRecords` and prints on the `ruledOut:`
line with its denominator (790 to 793). The brief cited "511 to 517"; the
rung is 511 to 530 and it is two refusals, not one.

659: `notAbsent` is now `status in ("exists", "partial")` counted directly,
with the comment saying why: the old "everything not absent" form would have
counted a ruled-out tile as one that owed a codebase, which is a denominator
one larger than the set examined. `tools/map.py` 2390 to 2396 makes the same
correction under the name `owesWhere`, and the page's own detail line reads
`heatWhereMissing=0/71-exists-or-partial` (map.html 275), 71 being 30 plus 41.

Selftest shape, counted off the code rather than the report: accepting rungs
are the live inventory (1), the eight parser cases, rung 2 (typed exists with
no evidence), rung 3 (`where` and `short`), rung 4 (a ruled-out tile naming
D39, a real record): 12. Planted refusals in the list at 934 to 1017: 30,
plus the empty-file exit 2 and the no-names-file exit 3: 32. Total 44, which
is the 44 the brief quoted, and the four ruled-out refusals are among them
(970 to 985: carrying `where`, carrying evidence, naming no record, naming
D9999). Rule 5b is met on the checker: both outcomes, accepting first, the
condition planted.

Two comments in the same file did not move with the code and are dictated in
section 7: 749 to 751 still say `none` is "the absent tiles".

## 3. Part 2, the tiles, and the citations were read, not copied

Counted by this director from the grep of every `"status":` line in
`production/systems-inventory.json`: exists 30, partial 41, absent 36,
ruled-out 4, total 111. `"typedBy": "jafar/` occurs 20 times, all on lines
1505 to 1759, the twenty entries the batch added. `"short":` occurs 38 times.
The page prints the same four counts (section 4). Against the brief's "91 this
morning": 30 minus 4, 41 minus 1, 36 minus 11 sum to 91, so the arithmetic
is consistent, though the pre-batch file was not readable by this director
without git and the "91" is the resident's.

The five built systems, each re-verified by this director against the code
tonight, with what D38's table did NOT carry and the builder therefore cannot
have copied:

1. Blood. `Core/Traces.cs` 17 `class Stain`, 44 `Noticeable`, 58 `Age`, 69
   `WashMinutes = 25`, 71 `Wash`. Beyond D38: `Game/ViolenceHost.cs` 297
   `PlayerStain = new Stain`, 356 `Traces.Age`, 362 `Traces.Wash`, 388
   `Traces.Noticeable`, 209 and 412 `StainsNoticed`; `verdict.txt` line 90
   carries `blood[taken=1 noticed=428 washed=1 publicFailed=True atHome=True
   worstCost=0.30]`. Typed exists. Correct.
2. Provenance. `Traces.cs` 98 `enum Origin` with exactly `Bought`, `Stolen`,
   `Taken`, `Inherited`, `Ordinary` at 102 to 112; `Game/EvidenceHost.cs` 70
   `Traces.Acquire`, 87 `Traces.Used`, 112 `Traces.Dispose`, 90, 115 and 184
   `Traces.ResidualRisk`. Beyond D38: `verdict.txt` 90 `provenance[bought=0.85
   stolen=0.60 taken=0.45 inherited=0.55 ordinary=0.05 ...]`. Typed exists.
   Correct.
3. Disguise. `Core/Gossip.cs` 258 to 261 is the doc comment of `Witness`
   (262): "a disguise (or distance, or darkness) passes less than 1.0". D38
   said line 259 and line 259 it still is. Beyond D38: `Game/GameController.cs`
   193 `CoatWitnessConfidence = 0.6`, 2732 `WearingCoat ? CoatWitnessConfidence
   : 1.0`; `verdict.txt` 90 carries the gate `ok disguise` and line 92
   `coatConf=0.60`. Typed exists. Correct.
4. Concealment. `Core/Arsenal.cs` 47 `enum Concealment` with exactly
   `Innocent`, `Concealable`, `Damning`, `Impossible` at 50 to 56; `Fits` (325)
   reads `Impossible` and `Damning`, `FriskCost` (342) prices three by name and
   the fourth by `default: return 1.0` at 350; `Core/Coat.cs` 26, 50 and 68
   `Arsenal.Get`, 52 and 73 `Arsenal.Fits`, 122 `Arsenal.FriskCost`. Beyond
   D38: `verdict.txt` 90 `carry[took=2/3 ... found=0.35 cost=0.46 ... frisks=1
   refused=1]`. Typed exists. Correct.
5. The lit window. `Core/Occupancy.cs` 15 to 16: "A lit window means SOMEBODY
   IS IN. That is the information pillar rather than decoration"; 128
   `ShopLit`, 152 `WindowLit`. Beyond D38: `Game/WorldBuilder.cs` 4122
   `SetWindowsLit` calls `Occupancy.ShopLit` at 4154 and `Occupancy.WindowLit`
   at 4155; `verdict.txt` 98 `windowsLit=3/6`. Typed PARTIAL under the
   type-the-lower rule because nothing reads a window back on the player's
   behalf, which is exactly D39's item 4. Correct, and it is the one of the
   five where reading the code changed the colour.

So D38's own expectation, "marked built-not-measured where no verdict key
emits it", did not survive the reading: all five have a verdict key, and the
notes say so. That is a builder that read the code. The one overclaim is a
word: the blood note says the gate is emitted "every run", and one committed
verdict proves one run. Not worth a round; noted.

`typedAgainst: this checkout at commit ec66f99a` against a HEAD of
`e4d8cfe1`: checked in `.git/logs/HEAD` lines 100 to 101, `ec66f99a` was HEAD
from 18:33:03Z to 19:25:01Z, which is the builder's whole working window
(rows 636 and 637 at 18:46Z and 18:58Z, limit hit at 19:14Z per NOW.md), and
the commit that moved HEAD is a documents commit. The field was true when
typed and stays.

Attribution: the twenty carry `typedBy` as `jafar/D38` or `jafar/D39`, role
`jafar` and the record as the name. The checker's ROLES accepts it, and it is
the right reading: a tile whose existence and colour rule come from his
dictated record carries his judgement, including the lit window, whose
partial is his own type-the-lower rule applied. The board's first sentence
therefore reads 20 of 111 and that number is his.

## 4. Part 3, the page, opened

`map.html` line 250 `<body id="map">`. Line 251, the visual ladder, RUNG 1 OF
7, unchanged and out of scope. Line 252, the board, in this order:

    THE BOARD
    20 of 111 tiles here carry your judgement. The other 91 are the
      studio's reading.
    111 systems, 30 exists, 41 partial, 36 absent, 4 ruled-out.
    Typed by the studio 2026-09-09..2026-09-15. 29 of 111 typed by a
      director, 62 by a builder, 20 of 111 ruled by you. Your ruling
      replaces any tile.
    30 tiles here are green. 23 are read in the older build only, 4 in
      both builds, none of the 30 in the newer build on its own, and 3 are
      about files rather than play.
    ● exists  ◐ partial  ○ absent  ⊘ ruled-out
    Every colour here is a typed judgement of state, not measured by this
      page ... [tap] where these come from, and who typed each one

then the five areas, the moat 26, the world 25, what the player touches 42,
content 11, the studio 7 (sum 111), every tile one text node with its mark,
the four ruled-out tiles drawn `h-ruledout` with `⊘` and a line-through in
the player-facing row. Lines 253 to 254, the next three. Line 255, the one
tap: `the audit view, which is measured`. Nothing else is on the scroll: no
path, no key, no sha, no fraction between lines 250 and 255. Line 256 is the
sheets. Line 278 is the audit sheet, and inside it, by extracted match: the
heading "the audit view: what this page measured, not what anybody typed"
(278), "what you can run, and what to press" (282), "the game, and the path
through it" (284), the flow SVG (287), "the studio ladder, which is a
different measurement" (288) with its LADDER START and END markers (290 and
292), and the street frame as a data URI (281). The about sheet's detail
lines (274 to 275) carry `typedInventory=... words=absent.36/exists.30/
partial.41/ruled-out.4`, `heatStates=absent.36/exists.30/partial.41/
ruled-out.4`, `heatTypedBy=builder.62/director.29/jafar.20/untyped.0/of.111`,
`heatTilesByWhere=core-csharp.54/both.6/ue-probe.1/repo.10`.

So the page is the board and the next three, with the ladder above them as
RULING 3 requires, and the audit view is one tap down and whole.

THE JUDGEMENT COUNT IS DERIVED, NOT A LITERAL. `tools/map.py` 2594 to 2621
`heat_judgement_words` reads `roleCounts["jafar"]` and `tiles`, both built
once by `heatmap()` at 2453 to 2456 and 2497 while it walks the file, and is
called at 2830 as the first sentence after the head. `check_typed_attribution`
(5367 to 5470) parses the sentence back off the rendered bytes with
`JUDGE_LINE_RX` (5316), compares number AND denominator with the run's count
(5415 to 5417), and requires it above the attribution sentence (5418 to
5420). The selftest at 7182 to 7210 asserts the live sentence is the derived
one and that the guard bites when the line claims every tile, drops its
denominator, or is deleted.

NOTHING DELETED, AS FAR AS THE PAGE CAN SHOW. This director had no diff (no
shell, and the previous `map.py` is not readable without git), so the claim
in the docstring at 82 to 88 that the audit block moved unreworded is checked
by presence, not by bytes: every block the 2026-09-07 rebuild put on the
first screen is inside the audit sheet (above), `CHECKS` at 5993 to 6012
still carries all 38 guards, and `HALF_OF` at 6041 still assigns the four
guards the 2026-09-09 ruling moved (`noComfortingBar`, `availabilityWords`,
`noAbsenceClaim`, `playerControlMatchesScan`) to the derived half. The bounds
did not move: `FOLD_PX = 844` (4509), `FOLD_PROSE_WORD_BOUND = 179` (4526),
`EXPECTED_NAMES = 27`, `CAP = 10`.

THE PIXEL IS OWED. His sentence was "the first screen says how many tiles
carry my judgement". The builder's docstring (90 to 98) says the sentence was
moved to the top of the board because the attribution line sat at 846 px
against a fold of 844, that the ladder alone is 735 px, and that the line's
top against the fold "is printed every run with NO BOUND SET" because the
collision with RULING 3 "is a director's to rule on and the pixel is what a
ruling should read". That number, `judgementLineTopPx`, was NOT PRINTED THIS
SESSION: it is not in the page (the model is computed after the page is
built, 4445 to 4475, and only reaches stdout at 7654), not in NOW.md, and not
in any report, because there was none. A docstring's 735 and 846 are numbers
somebody printed on some run and this record does not conclude from them.
Section 6 orders the print.

Ruled on the collision in advance, so the print decides and not a second
spawn: RULING 3 stands (the ladder is his and stays above everything), the
judgement sentence stays the first line of the board directly under it, and
"on the first screen" is met when `judgementTopIsAboveTheFold=yes`. If the
printed line reads `no`, two of his rulings cannot share 844 px at seven
rungs, and which one yields is his call (section 9, question 2), not a
builder's.

## 5. Ruled-out is distinguishable from absent at every site

Every place that counts, colours or tallies the four states, read tonight:

- Checker `byStatus:` line (744): four terms, each with the denominator.
- Checker `evidence:` line (782 to 786): `absentCarryNone=` and
  `ruledOutCarryNone=` as two keys.
- Checker `ruledOut:` line (790 to 793): tiles, naming a record, and the
  pairs.
- Checker `byWhere:` line (755 to 760): `none=N/111-absent-or-ruled-out` is a
  census of the `where` field and its label says which two statuses lack one;
  `missingWhere=` divides by exists-or-partial (`notAbsent`, 659).
- Map `HEAT_MARK` and `HEAT_CLASS` (2195 to 2197): fourth mark `⊘`, fourth
  class `h-ruledout`, chosen without a hyphen because the readback regex at
  5229 is `h-[a-z]+` and a hyphenated class would have fallen out of its own
  count silently; CSS at 3358 to 3359 (double border, line-through) and 3484
  (light theme).
- Map legend (2759 to 2761) walks `HEAT_DRAWN_STATES`; `check_heatmap` (5237)
  requires the word for every drawn state in the legend and (5236) the mark
  of every tile to match its class.
- Map tally sentence `heat_counts_words` (2544 to 2557) walks `HEAT_STATES`
  and prints a zero for a state nobody typed, from `counts` keyed per state
  word (2490 to 2491).
- Map provenance sheet (2930 to 2932): "36 absent and 4 ruled out, all of
  which carry none".
- Map done line `heatStates=` (4324) and `typedInventory ... words=` (4033 to
  4036), both per word.
- `ledger/verify.py` 1462: `SYSTEMS_INVENTORY_RE` parses `entries=`,
  `namesFromOrder=` and `covered=` only, so a fourth status token cannot be
  dropped by it. No other reader of the inventory exists in the tree: the
  grep for `systems-inventory` across `*.py`, `*.yml` and `*.sh` finds the two
  tools, `map.py`, `verify.py`, the publish workflow (path triggers) and a
  comment in `publish-glance.py` about the generated-at sentence.

THE GAP, and it is a guard and not a fault in the artifact: the tally
sentence on the board's face (`hNow`) is derived but nothing reads it back.
`check_typed_attribution` reads the judgement line, the attribution line and
the split; `check_heatmap` reads tiles, marks, legend and areas; no check
parses "111 systems, 30 exists, 41 partial, 36 absent, 4 ruled-out" against
`counts`. And `map.py`'s selftest plants no ruled-out tile: the grep for
`ruledout`, `ruled-out` and `⊘` finds nothing after line 3484, so the only
exercise of the fourth mark is the live page, which is the accepting case
and not a run in which the lump CAN happen. Queued as item (a) in section 8.

## 6. The lines the resident prints and pastes here before the commit

After the edits of section 7, from the repository root, run
`python3 tools/map.py` once (it regenerates `map.html` and prints its done
lines) and paste, verbatim, the three lines that begin

    map: judgementLineTopPx=
    map: pageScrollPx..IfAuditWereInline=
    map: DONE pageBytesGenerated=

into this section under the heading PRINTED, then run `python3
ledger/verify.py` and paste the footer from `ledger/.verify-footer` into the
commit message as CLAUDE.md requires. Commit the regenerated `map.html`, not
the builder's, so the page and the numbers are one photograph. If the first
line reads `judgementTopIsAboveTheFold=no`, section 9 question 2 goes to
Jafar in the same brief as question 1.

PRINTED, from `python3 tools/map.py` run at 2026-09-15T20:0xZ on this tree
after the section 7 edits, verbatim:

    map: judgementLineTopPx=798/844-fold judgementLineHeightPx=43 judgementTopIsAboveTheFold=yes judgementWholeLineAboveTheFold=yes ladderBottomPx=749 (series, NO BOUND SET: RULING 3 puts the visual ladder above everything and this pass does not move it)
    map: pageScrollPx..IfAuditWereInline=4255..8556 auditBehindATapPx=4301 auditOnTheScroll=no-it-is-one-tap-down auditReachableAt=#audit nothingDeletedToShorten=true foldModel=block-flow/css-derived/avg-advance-0.5em/margins-do-not-collapse
    map: DONE pageBytesGenerated=230474/250000-cap ofWhichPictureB64=79860 checksFailed=0/38 checkedBytes=generated servedPageResult=nothing-measured

THE PIXEL IS ANSWERED AND QUESTION 2 DOES NOT GO TO HIM. It reads
`judgementTopIsAboveTheFold=yes`, and the stronger
`judgementWholeLineAboveTheFold=yes` beside it: the line starts at 798 px and
is 43 px tall against an 844 px fold, with the ladder's bottom at 749 px. So
RULING 3's ladder and his judgement line CO-EXIST with 46 px of the first
screen to spare, and the conditional question this record prepared is spent
rather than asked. Section 9 question 1, the sleep pair, still goes.

AND THE PAGE HALVED WITHOUT LOSING ANYTHING: 4255 px scrolled against 8556 px
had the audit stayed inline, `auditOnTheScroll=no-it-is-one-tap-down`, and
`nothingDeletedToShorten=true`. That last token is the 2026-09-07 rebuild's
rule holding, which was that the evidence moves and does not go away.

## 7. Dictated edits, hand-applied by the resident, then the two selftests

`production/systems-inventory.json`, three strings inside `howToRead`, each a
whole-string replacement inside its existing quotes, no double quote in any
of them:

Line 42, now beginning `status is a TYPED JUDGEMENT`, becomes:

    status is a TYPED JUDGEMENT of where a system stands: exists, partial, absent or ruled-out. It is the studio's reading, ruled by Jafar, and it changes by a ruling rather than by a grep. RULED-OUT IS NOT ABSENT, ruled by Jafar on 2026-09-15 and landed with D38: absent is not built yet and waits its turn; ruled-out is decided against, its note names the record that struck it and the validator refuses one that does not, and no work follows it. No tally sums the two.

Line 45, the sentence `An entry typed absent carries none, so a tile cannot
read absent while citing paths that say otherwise.` becomes:

    An entry typed absent or ruled-out carries none, so a tile cannot read as nowhere while citing paths that say otherwise.

Line 52, the words `REQUIRED when status is exists or partial and FORBIDDEN
when it is absent, for the same reason evidence is` become:

    REQUIRED when status is exists or partial and FORBIDDEN when it is absent or ruled-out, for the same reason evidence is

`tools/systems-inventory-check.py` 749 to 751, the three comment lines
beginning `# \`none\` is the absent tiles`, become these three:

    # `none` is the absent and ruled-out tiles, neither of which may carry
    # one; `missing` is the fault, and it prints its denominator either way
    # so a clean run cannot be confused with a run that examined nothing.

Then `python3 tools/systems-inventory-check.py --selftest` and `python3
tools/map.py --selftest`, both read to their last line, before verify.

## 8. Adjacent work, to the queue by name, numbers assigned at filing

The top number on disk while this was written was 314 (`production/queue/`,
live directory, re-count at filing). The resident files these three and
writes each back into this section as a `QUEUE: NNN name` line at column 0 in
the same commit, so `tools/docs-check.py` checks that the item exists (D32).

QUEUE: 315 the-boards-tally-is-derived-and-nothing-reads-it-back

(a) The board's tally sentence is derived and nothing reads it back, and the
map selftest plants no ruled-out tile. Acceptance: a check parses the `hNow`
sentence with a regex anchored on `heat_counts_words`' own shape, compares
all four numbers and the total with `counts`, and prints them as
`tallyOnPage=.../counted=...`; two rejecting fixtures, accepting first on the
live page: the ruled-out clause deleted with its 4 folded into absent (40
absent, no ruled-out clause, tiles unchanged), and `4 ruled-out` reading `0
ruled-out` with the four tiles still drawn; plus one planted inventory
fixture carrying a single ruled-out tile for `check_heatmap`, asserting mark
`⊘`, class `h-ruledout` and the legend word.

QUEUE: 316 the-inventorys-reading-notes-name-a-retired-plan-and-a-stale-count

(b) The inventory's `howToRead` names a retired plan and a stale count. Line
50 says `phase names a row in ledger-v2/respec/roadmap-v2.md`, retired as a
plan document on 2026-09-14 by the fold into `production/stages.md`; line 53
says ten entries carry a `short` (38 do tonight) and quotes a name-length
distribution from 2026-09-09. Acceptance: both sentences true against the
file on the day, the phase vocabulary `PHASES` in the checker re-pointed at
whatever `stages.md` calls its rows, and the short count either read from
the checker's own `labels:` line or dropped from the prose.

QUEUE: 317 d38s-third-rule-the-five-later-items-get-cards-and-no-tile

(c) D38's third typing rule, still unapplied: "Everything ruled later (D39)
goes in the queue with a number and no tile until its stage arrives." Five
cards, each BLOCKED on the visual slice (D28, D31, D39's gate), no tile:
persuasion and intimidation rebased on memory rather than stats; the camera
and the tape as a witness that cannot be talked to; habits that make a person
predictable; weather as an event that moves people indoors; failure producing
content rather than a refusal. D39's closing clause ("which of the sixteen to
file, and when, is his to decide") and D38's rule read against each other:
D38 is the specific instruction for this group and a queue card is not a
start, so D38 governs and the five are filed; the eleven now-or-next items
stay unfiled under D39's clause until he names them.

## 9. To Jafar, through the Producer, in the next brief

1. THE SLEEP PAIR. The board now carries two absent tiles for one verb:
   `sleep and the day boundary` (player-facing, typed 2026-09-10, "nothing
   advances the clock by resting and nothing ends a day") and `sleep as a
   way to cross a day` (the moat, D39 item 5, "so rumour travel is something
   the player plays against"). The builder's note says the two are halves and
   not one system twice. This director reads them as one mechanic with one
   consequence: the day the player can sleep, both tiles change or one lags,
   and a board whose value is that its colours can be trusted at a glance
   should not have a tile that lags by construction. Recommendation: one
   tile, in the moat row under D39's name, with the 2026-09-10 tile retyped
   into it under D21 (a retype needs a ruling; this is the ruling if he says
   yes), and the board reads 110 with 20 his. His count in D38 was twenty
   writes; a retype is a write, so the arithmetic holds. Landed as two tonight
   because his record said twenty tiles and the builder followed it; his
   call which.
2. ONLY IF SECTION 6 PRINTS `judgementTopIsAboveTheFold=no`: RULING 3's
   ladder (seven rungs, each with its tap) and the sentence "N of M tiles
   here carry your judgement" cannot both be on one 844 px screen. Which
   yields: the ladder loses its per-rung taps into a single tap, or the
   sentence rides the ladder's head line, or the straddle is accepted. Not
   asked if the line prints `yes`.

## 10. Commit hygiene, and two things the record will not hide

Stage by name: the four files, this record, and the one line dictated to
`rulings-log.md` below. `workByScope=claude:16` names sixteen pending lines
under `.claude/` that the brief's file list does not account for: rows 638
and 639 of the agent log are two of them at most. The resident names what the
rest are before staging, and anything that is not this batch stays out of
this commit.

Row 639, an `instrument-builder` spawned at 19:44:56Z, ninety seconds after
this director, is not part of the batch reviewed. If it touched any of the
four files after this reading, the two selftests of section 7 and the print
of section 6 are re-run on the tree as it stands at commit time; this ruling
is of the tree as read between 19:43Z and the time of the stamp.

The hold. NOW.md at 19:20Z records his ten-hour rule biting: "unmeasured
means INBOX HALF ONLY, NO BUILDERS, NO DISPATCHES, NO RENDERS", and "do not
spawn a director for it". Rows 638 and 639 were spawned at 19:43Z and 19:44Z.
Either his reading arrived between 19:20Z and 19:43Z, in which case NOW.md
carries the number and the time before this commit, or the two spawns breach
the hold and NOW.md says so in as many words. The record does not decide
which; it refuses to leave the question unwritten.

## 11. What the brief got wrong

1. "511 to 517" for the ruled-out rung: it is 511 to 530 and it is two
   refusals (no record named; record named does not exist), which is
   stronger than the brief credits.
2. The file list (four files, 630 lines under `tools/`) does not account for
   the sixteen lines under `.claude/` that the gate counted. Section 10.
3. "The counts are exactly D38's" is true of the arithmetic and silent on
   overlap: D38's twenty was written without checking the eleven now-or-next
   items against the sixteen absent tiles the 2026-09-10 census added, and
   one pair (sleep) is a likely double. Section 9.
4. "Zero of D33 to D39 had reached any artifact ... their only citation
   outside their own files was rulings-log.md" could not be checked for the
   pre-batch tree without git. Read against tonight's tree the only other
   citations are tonight's own (NOW.md, budget.md's spend row, the ten-hours
   record) and a false positive inside a data URI in `glance.html` line 81,
   so nothing contradicts it; it is the resident's claim, not this record's.
5. Nothing else in the five readings was wrong. The 38 checks and 44 rungs
   were both re-counted off the code and match.

## 12. The quality ladder at close

This is the first working result for the instrument and the best available
for the data. The next rung is the tally readback guard with its planted
ruled-out fixture (8a), then the pixel (section 6), then the reading notes
(8b). An aspect whose next rung is blank: none here.

## 13. One line for the register's index, dictated

Insert after the 2026-09-15 line for "the forty are waived by name" in
`ledger-v2/respec/decision-register/rulings-log.md`:

    - **2026-09-15** D38 lands as four files: the fourth status is a status and every tally keeps it apart from absent, the five built systems' citations were re-read against the code and all five turn out measured, the board's judgement line is derived and read back and its pixel against the fold is owed as a printed line, the sleep pair goes to Jafar, D38's third rule (five later items to the queue) is filed by the resident, and the tally readback guard is queued
      `game-design/decision-2026-09-15-ruling-d38-lands-the-fourth-status-is-a-status-and-the-judgement-line-owes-its-pixel.md`

<!--RULING spawn=2026-09-15T19:43:24Z paths=tools/systems-inventory-check.py,tools/map.py,production/systems-inventory.json,map.html,game-design/decision-2026-09-15-ruling-d38-lands-the-fourth-status-is-a-status-and-the-judgement-line-owes-its-pixel.md-->
