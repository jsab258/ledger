# Fixes after the canon review of units 11, 12 and B5

13 October 2026, branch cloud/week-42, written by the fixer. Nothing is committed or pushed here. Every fix of the review is applied, in the source the pieces are built from, then rebuilt. No second review was run.

## Counts after the fixes

- Town: `check_town.py` 619 of 619 rows pass, 34 of 34 planted faults caught (578 of 578 and 30 of 30 before). 44 people, 1,162 facts of which 51 are new and marked (29 before, 22 reworded), 220 rumours (190 pooled, 30 specific), 430 answers (28 deflections).
- Lines: `check_lines.py` 2,491 of 2,491 rows pass, 54 of 54 planted faults caught (2,489 and 47 before). 1,626 lines (1,643 before), 34 places for directions (35 before), 171 directions (176 before). Voice plan about 4,419 clips, or 8,005 in all six crowd voices.
- Draft: `check_draft.py` 64 of 64 rows pass, `--negative-controls` 25 of 25 caught. Sections 3.3 and 4 are recomputed by the check and equal the tables.
- Gates: `tools/canon-gate.py` over people.json, HOMES.md and NOTES.md (town), lines.json, rules.json and NOTES.md (lines), DRAFT.md and this file: 0 findings. `tools/content-gate.py` with no arguments: 0 new hits over its corpus (9,374 strings); its own `scan()` over every string of people.json, lines.json, rules.json and over DRAFT.md: 0 hits in 82,179 strings. The 6 hits in the two town notes files are the prose that names the content rule, as before.

## The eight faults

1. Four regulars held the design paragraph. Changed `town/authored/e_regulars_2.py` (Wayne, Hal, Susan) and `h_regulars_5.py` (Dennis): the copied quote is gone and each holds the review's one sentence about themselves (`victor.k19`, `hal.k21`, `tibor.k20`, `drago.k21`, all secret). They are now marked new facts in a new group N-REWORDED, because a reworded sentence is no longer word for word from a home.
2. Six greetings claiming what the street thinks of him. Replaced in `lines/authored/darren.py` (`greet-nowak.06`, `greet-tom.09`), `dock_worker.py` (`greet-nowak.07`), `casual_worker.py` (`greet-owner.07`) and `laundry_worker.py` (`greet-nowak.06`, `greet-tom.04`) with the review's neutral lines; conditions and weights kept. `check_lines.py` now fails a line that says what the street thinks of him (a word list, with a planted fault). The search for other lines of that sort is under "Found and reported" below.
3. A16 gave away the fire's truth. `first-30-minutes/DRAFT.md`, A16, Learns: now "The fire is the story the street will not drop."
4. Hal's coin shop and the newsagent on the wrong row. Lines: in `lines/authored/anyone.py` the five Hal directions are deleted, `newsagent.04` and `.05` and `bus-stop.05` are the review's words; in `lines_lib.py` Hal's place is out of DESTS (34 places) and recorded in a new HELD_DESTS; `check_lines.py` no longer lists it and has a row that a held place has no directions and no line names it; `lines/make_notes.py` adds item 7 to "Where the homes disagree" in the review's words. Draft: section 2.4, the B12 status and the A16 beat are the review's words. Town: `town/make_notes.py` item 6 and `HOMES.md` item 5 say the built row and that Hal's shop has no unit. Hal and his trade stay as his sheet has them (facts, answers, schedule); only directions to his shop wait for Jafar.
5. Ada's tea. `lines/authored/pensioner.py`: `greet-owner.08`, `greet-nowak.09`, `greet-tommy.08` are the review's lines. `check_lines.py` now fails a tea or kettle invitation in the pensioner kind (a planted fault catches it).
6. Julie's and Albert's day facts. `town/town_lib.py` (`render_day_from_schedule`) and `town/build_people.py` (the final schedule is chosen first, and the day fact is derived from it); `check_town.py` has a row for each of the 34 people who hold a day fact comparing it with their stored schedule, and a planted fault (Julie at the laundry all day). `tanja.k20` and `fabjan.k20` now read exactly as the review words them. No other person's fact changed.
7. Old names in fact texts. `town/authored/d_regulars_1.py` (Lee, Rita), `e_regulars_2.py` (Susan's stamp), `c_heads.py` (Maureen Jensen, Danny): `joey.k19`, `ferko.k23`, `sera.k14`, `tibor.k19`, `rita.k22`, `danny.k11` are the review's sentences. `check_town.py` now runs the old-name list over carried text too (a planted fault), and a design-note row over every fact text; neither found anything else.
8. Hal and Rita passing on the row. `d_regulars_1.py` (`rita.r1`: June's return, heard from Lee, passed to Wayne and Susan, based on `rita.k06`) and `e_regulars_2.py` (`hal.r1`: the thin trade, from his shop, passed to Rita and Darren, based on `hal.k11`). Both are pooled stories they already hold, with the review's field values. `check_town.py` now fails a rumour whose "sure" says it is kept to themselves while it lists who it goes to.

## Narrow points: town

- T1. Eleven fact texts replaced as worded (`danny.k07`, `fixer.k08`, `tom.k05`, `tom.k06`, `rita.k23`, `emil.k23`, `sam.k26`, `filip.k21`, `lena.k29`, `sam.k28`) and `fixer.r2` "sure" now "street talk". Files: `c_heads.py`, `a_core.py`, `b_ring.py`, `d_regulars_1.py`, `h_regulars_5.py`. Tom's and Ron's `job` facts come from the person's role, so `build_people.py` now lets a role carry a reworded text with its reason.
- T2. `tom.b01` is "Some on the street suppose the new owner has come into money." and stays false (`a_core.py`).
- T3. `rocco.k19` and Ron's role text are "A docker until 1989. Mickey kept him on the door and the rank." (`a_core.py`). The check's Mickey screen flagged the sentence, so a reworded fact may keep a sentence its home line holds word for word.
- T4. `ada.r3` is the paper's word only, true, sure "the paper's word; she does not repeat the rest" (`b_ring.py`, with a new truth basis in `common.py`).
- T5. `ellis.r1` and `aldous.r2` are true, on the same basis (`c_heads.py`).
- T6. `noor.k17` is "a reporter on the local paper" (`b_ring.py`: a shorter quote of the same casting line, so it stays sourced).
- T7. Seven answers replaced as worded: Danny (now a deflection on `danny.k08`), Lily, Kevin, DS Ellis, Father Walsh, Lee, Gordon (`c_heads.py`, `h_regulars_5.py`, `d_regulars_1.py`, `b_ring.py`, `g_regulars_4.py`).
- T8. Father Walsh's "Did Mickey have any enemies?" is the review's answer on `emil.b01` (`b_ring.py`).
- T9. `petra.r4` and `dario.r4` are "street talk", heard from Alison and Darren (`g_regulars_4.py`).
- T10. `takeaway_f.k21` reads "keeps the takeaway on the parade with her husband" (`h_regulars_5.py`).
- T11. Alison's "What do people say about me?" is the review's answer (`b_ring.py`).
- T12. Chose the first of the two ways: the rule gains "or work at Father Walsh's chapel" (`town/make_notes.py`, so NOTES.md) and a new DECISIONS entry; Winifred keeps her answers; the sixteen stay sixteen.
- T13. Town NOTES item 6 and HOMES item 5 carry the built west row (tea room 24 to 30, ironmonger 30 to 36, newsagent 36 to 42; Hal's has no unit) for Jafar's page.

## Narrow points: lines

- L1. Seven street-name lines replaced as worded (`anyone.py`), except one: see "The review got wrong" below. `check_lines.py` now has a row that no line speaks a street name the adopted atlas marks "(proposal)" (nine such names, with a planted fault).
- L2. `driver.bumped.05`, `darren.crime-face.05` replaced (`driver.py`, `darren.py`).
- L3. Five lines replaced: `tradesman.greet-tom.02`, `father_walsh.greet-tommy.08`, `office_worker.greet-owner.07`, `pensioner.greet-stranger.05`, `pensioner.crime-face.08`.
- L4. Petra moved from dock worker to office worker and Dawn from casual worker to office worker (`lines_lib.py`, with the kinds' descriptions). `rules_source.py` has a new `speaker_overrides.excluded_lines` keeping Sheila and the dispatcher from `office_worker.greet-owner.04` and `greet-nowak.05`; `walk_sim.py` applies it and has a rule test (240 picks); `check_lines.py` counts it in every pool and has a rules row and two planted faults.
- L5. `ron.greet-tom.07` is "Afternoon, Tom. Tea's on, if you want it." (`ron.py`).
- L6. `june.bumped.02`, `june.crime-noise.04`, `june.after-deed.07` replaced (`june.py`). The crime-face repetition is a known shortfall, listed in lines NOTES.md ("What to look at first", item 5), because no sample page exists yet to list it on.
- L7. `darren.rain-starts.03` is "Rain. Great. My hair will never recover."
- L8. `father_walsh.in-rain.05`, `darren.in-rain.08` replaced.
- L9. Lines NOTES.md ("What to look at first", item 1) now credits the what-they-call-him design, not canon. DECISIONS.md is append-only, so its old line 472 is not edited; a new entry gives the corrected wording.
- L10. Chose to drop them: the thirteen driver stranger greetings are deleted (`driver.py`) and the kind's rungs are owner, Nowak and Tom (`lines_lib.py`). `check_lines.py` has a new row for every kind: each rung it has lines for must be one a member can stand at, from rules.json's floors (13 rows, with a planted fault). Clip count is now about 4,419.

## Narrow points: draft

- D1. Q2 (a) and D2 are the review's words (`DRAFT.md`).
- D2. A9 and B8 marks moved to Darren's day: `consequence@9:30 ... ` and `consequence@8:30 ...` as worded.
- D3. B1 `ui:move-hint@0:07`, B6 `ui:coat-hint@5:32`, B25 "the five hints", section 4 hints "6, the last at 9:40" and "5, the last at 8:40", and the interface row as the check computes it (A ledger-hint 9:40; B move-hint 0:07, coat-hint 5:32, ledger-hint 8:40).
- D4. `ui:wait-stop@6:05` in A7 and `ui:wait-stop@21:05` in B19; "the game saves in the morning" in A8 and B7; `ui:save` moved to A9 `@9:00` and B8 `@8:00`; first save 9:00 and 8:00. The wait-stop and save cells of the interface row follow.
- D5. A11: "At the fish counter Brenda".
- D6. A2: June's second line is her sheet's "I'm not stopping long. I've a life to get back to."
- D7. A17: "She heard the glass go and has heard who was about". I also changed that row's Learns cell from "Sheila saw the deed" to "Sheila heard of the deed", the same fault seen twice.
- D8. A21 status is the review's words.

## The review got wrong, or its fix does not hold alone

- L1, `anyone.way-tivoli.05`: the review's replacement "The Tivoli, in the Parade. Up the hill, a long way east." has 12 words and the unit's cap is 11 ("each under 12 words"); the row `line.anyone.way-tivoli.05` failed at 12. The line reads "Tivoli, in the Parade. Up the hill, a long way east." (11 words, same facts).
- L4: excluding Sheila and the dispatcher from `office_worker.greet-owner.04` leaves them 5 lines in a dry evening, under the unit's floor of 6 (row `pool.greeting/owner@office_worker`, worst 5). Added one new-owner greeting, `office_worker.greet-owner.10`, "The new owner. Mind the paperwork, it breeds." It is new text the review did not write.
- L10: two driver bump lines, `driver.bumped.06` and `.07`, were marked for strangers only, so with the stranger rung gone they could never be said either (rows `line.driver.bumped.06` and `.07`). Removed the stranger mark from both so they work at any standing.
- T12 and L9 say to edit DECISIONS.md lines 469 and 472. That file is append-only (CLAUDE.md, and the row `decisions.append_only`), so both are corrected by new entries and the old lines stand.
- Fault 4 and B12: the review words only B12's Status. The beat still sends Tom into Hal's shop, and A16's Who and Where still list `hal` and `hals_shop` though no A16 text now uses them. I left them, as worded, because removing them moves section 3.3's people list; the beat is honestly marked NOT YET. A reviewer may want them removed.
- Not wrong, checked: Petra's and Gordon's days end at 19:00 and 17:00, the outfit's man is at the landing from 22:00, Darren starts at the cafe at 09:00, Brenda is at the counter until 14:00, and `StreetFacts.cs` lines 63 and 49 are the thin trade and June's return.

## Found and reported, not changed (the search the order asked for)

Greetings and lines that state something about him or the speaker that the simulation might not hold, weaker than the six:

- `office_worker.greet-owner.02` "Everyone's been talking."
- `pensioner.greet-owner.01` "I've heard so much." and `pensioner.greet-owner.02` "We'd heard you were coming."
- `driver.greet-owner.07` "They say you've the keys to the lot."
- `dock_worker.greet-owner.05` "Heard you came with one suitcase."
- `casual_worker.greet-owner.02` "Heard you've a rank to run." and `casual_worker.greet-tom.04` "Is it true you've a rank to fill?" (the second asserts a vacancy nobody set)
- `darren.greet-nowak.04` "Heard you're doing the rounds."
- `pensioner.greet-tom.02` "I've got your name right this time." and `pensioner.greet-tom.06` "I was just saying your name."
- `pensioner.crime-shape.03` "Somebody ran, past my window." (the kind of fault L3 named: Nora, Edith, Albert and Winifred may have no window on the street)

These are about what is known at the owner rung or are a speaker's own small claims, so the review passed them; the new check is written to the six patterns only and does not fail them. Town side: six people carry the fact "six see him come (Ron, Sheila, the dispatcher, a day driver, Ada, and the sign painter doing the street's boards)", in the design's voice; each of the six could see the others, so it is left.

## Not done

- Nothing in the review is left undone. The sample page for the crime-face shortfall does not exist yet, so the shortfall is in lines NOTES.md for it to take.
- Not run, as before: the PC game, TownReach, any voice.

## Records

- DECISIONS.md: eight entries dated 13 October (one for the reworded facts in the town's own form, seven for the rest). RECIPE.md: the lesson added to the town and lines entries. HANDOVER.md, QUEUE.md and REUSE.md numbers moved to the new counts.
