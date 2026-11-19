# REVIEW-FIX-CHECK: the five must-fix points, after the fix

19 November 2026. A fresh reviewer, reading CLAUDE.md, canon.md, RULINGS.md, REVIEW-SYNTHESIS.md and the five revised files (VISION, DESIGN, TRACE, BUILD-ORDER, QUESTIONS), with the diff against the commit before. Each fault was searched for across all five files, not sampled. FIX-LOG.md was read only after the verdicts below were formed. Line numbers are the files as they stand today.

## Verdict

All five must-fix points are closed. Three new points in the changed lines each need a one-line fix: one misreads canon, one brings back a word that reads as a child, and one quietly settles an open question. Two small residuals follow.

## The must-fix points

### M1. Guns common, killing routine: closed

- DESIGN 236: state 2 now reads "Guns stay rare: only named men carry." DESIGN 237: state 3 reads "A few named men on each side now carry ... each death is a named, permanent event; guns stay rare."
- DESIGN 250: ER-FIGHT-09 caps carriers and deaths at every dial state, with a seeded check.
- Searched all five files for gun, shot, armed, firearm, common, kill, death and deadly. Every other mention keeps guns rare and last: DESIGN 229 ("firearms, rare and last"), 233 to 235, 239, 521; TRACE 23, 197, 295, 374; BUILD-ORDER 95, 125. No line makes guns common or killing routine. "Silence is the commonest music" (DESIGN 494) is not about guns.

### M2. A car able to kill, directly or through a fall: closed

- DESIGN 182: "A car strike is never a blow under the fall rule: whatever the person lands on, a car never kills, and rung 8 is never reached with a car."
- DESIGN 225 (death): "A car strike is never such a blow (section 5)." DESIGN 246, ER-FIGHT-05: "A car strike never counts as a blow."
- DESIGN 193, ER-DRIVE-03: the check now throws people against a kerb, wall or step, aimed and unaimed, and nobody dies.
- DESIGN 338: a crewman driving is an AI driver and always brakes, so only the player's car strikes (canon 117).
- VISION 23, TRACE 25, 196, 265, 298 and 339, and BUILD-ORDER 72 all say a car never kills. No line lets a car kill.

### M3. On screen what Tom cannot perceive: closed

- DESIGN 63, ER-CORE-02: limited to "every change Tom could perceive", and its check asserts no screen text or Ledger line for what he could not.
- DESIGN 77: the assist outlines only people Tom can see who face him, "never a figure he could not see, never what they know"; DESIGN 507, ER-SCREEN-01, names that one exception.
- TRACE 119 and 241 point at both.
- DESIGN 291 to 295 (the Ledger), 496 (the screen) and 394 (ER-RISE-01) agree. One adjacent rule can still be read the old way: see residual R1.

### M4. June Suddaby, Philip Danby and Father Walsh: closed

- June: DESIGN 406, minute 1:30, "June Suddaby, Mickey's daughter, still in town and wanting nothing from the office". This matches the approved first hour (game-design/first-hour-2026-09-29.md, "June, Mickey's daughter, back for the funeral, wants nothing from the office") and the approved outline. Her own street lines: DESIGN 315.
- Danby: DESIGN 468, Act I's "someone worth being honest for, who can be Alison Sedman or Philip Danby", as the approved outline has it ("still to write").
- Father Walsh: DESIGN 319, a person with his own street lines and memory, never a mechanic.
- The cast list at DESIGN 459 to 466 points each one at those lines.
- TRACE 260 (June at section 15 minute 1:30 and section 11; Walsh at section 11; Alison and Danby at section 16 Act I) and TRACE 292 (the five met on day one, section 15 minutes 1:30 and 1:45) agree with DESIGN. The only stray pointer is R2.

### M5. A word that reads as a child: closed for "lad"

- DESIGN 140: "a yard hand, a man in his twenties". DESIGN 425: "front up his yard hand". TRACE 317: "Cammack's men".
- Searched all five files for lad, boy, girl, kid, child, son, daughter, school, pupil, young, youth, teen, baby, junior, lass, nipper and similar. Left: the bans themselves (VISION 38, DESIGN 534, TRACE 267), "the nephew" (Tom, DESIGN 376) and June as Mickey's daughter, who is an adult in canon. There is one new word, "pupils", in a changed line: see N2.

## New points in the changed lines

### N1. DESIGN 15 misreads canon's spend rule

- canon.md 177 to 182: "fighting must look and feel AAA (Jafar, 12 October 2026). Driving, when it comes, must end at AAA quality".
- DESIGN 15 says that, read literally, the spend rule "starves the fights, driving and jobs the pillar puts first". Canon already exempts fights and driving. QUESTIONS 13 repeats the misreading: "gives everything else the smallest budget".
- Fix, DESIGN 15: replace "Read literally, that starves the fights, driving and jobs the pillar puts first." with "It already exempts fighting (AAA, 12 Oct) and driving (AAA as the end state, 17 Nov), so the pull is on jobs, fares and how play time is shared."
- Fix, QUESTIONS 13: replace "gives everything else the smallest budget" with "gives everything else, fighting and driving excepted, the smallest budget".

### N2. DESIGN 465 brings back a child word

- canon.md 125 to 127: "NO CHILDREN ANYWHERE: none rendered, none in the crowd, none in dialogue or image prompts. THE SCHOOL STANDS CLOSED".
- DESIGN 465: "so his work is never shown with pupils". This names pupils, and it suggests his work can be shown, when the school is closed.
- Fix: replace "Danby is a teacher, but no children appear anywhere and the school stands closed for the game's window (canon), so his work is never shown with pupils." with "Danby is a teacher by trade; the school stands closed for the game's window (canon), so he is never seen at work."

### N3. BUILD-ORDER 37 quietly settles the cab question

- QUESTIONS 15 puts the cab as the day's main verb to him, and BUILD-ORDER 121 says it is "decided by his answer to QUESTIONS 6, not adopted before". BUILD-ORDER 37 instead says "the week run in stage B decides".
- Fix, BUILD-ORDER 37: replace "and the week run in stage B decides." with "and his answer to QUESTIONS 6 decides, with the week run's numbers beside it."

### Checked and clean

- No em-dashes and no italics in the five files. Bold is used, which is not italics.
- No first person. The "we" in DESIGN 15 is a quote of his own words.
- No alcohol or gambling in any changed line. "Main bet" is gone. "The odds" (DESIGN 37, 42, 114, 223; BUILD-ORDER 71, 87) means a fight's numbers.
- These new lines match their rulings: street lines (RULINGS 104), reporting a line (RULINGS 101), offline sign (RULINGS 100), the crowd after a deed (RULINGS 92), Mickey's death and the fire (RULINGS 109), clothes approval (RULINGS 82), and ER-PERF-01 (RULINGS 64). The CCTV line (DESIGN 86) matches canon 56 to 59.
- The open questions are put as questions. Endings: QUESTIONS 5, DESIGN 476 and 532, TRACE C1. Canon's two games: QUESTIONS 13, DESIGN 15, TRACE C18. The cab as the main verb: QUESTIONS 15, DESIGN 17, 49 and 165, VISION 11, TRACE C17 and BUILD-ORDER 121. N3 is the one exception. DESIGN builds to the recommended answers meanwhile and says so, as QUESTIONS 3 allows.

## Residuals (small; they do not reopen a must-fix)

- R1, next to M3. DESIGN 93, ER-EYES-01, scores "who noticed" as "right 8 times in 10 against the simulation's truth". That truth includes watchers Tom could not see or hear, so meeting the rule literally would push cues for them onto the screen (RULINGS 116, "never other minds"). Fix: replace "against the simulation's truth" with "against the watchers Tom could see or hear, never those he could not".
- R2, a TRACE pointer. TRACE 266 says the chapel line is in section 6 ("The chapel is a place, never a mechanic (§6)"), but it is in section 11 (DESIGN 319). Fix: change "(§6)" to "(§11)".

## Applied (19 Nov, lane run of 09:16)
N1, N2, N3, the ER-EYES-01 scoring line and the TRACE section pointer were applied word for word as above.
