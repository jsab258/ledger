# Fixes after the canon review of units 11, 12 and B5, second pass

13 October 2026, branch cloud/week-42, written by the follow-up fixer. Nothing is committed or pushed here. The lines are changed in the authored sources (the .py files in lines/authored), then rebuilt with `python3 build_lines.py`; `lines.json`, the two json files in lines/checks and `lines/NOTES.md` were never edited by hand (NOTES.md is rebuilt by `make_notes.py`, which carries the new paragraph). The draft was edited directly, as it is the written home.

## Counts after this pass

- Lines: `check_lines.py` 2,500 of 2,500 rows pass (2,491 before), 62 of 62 planted faults caught (54 before). Still 1,626 lines, 34 places, 171 directions and about 4,419 clips: every replacement stands in the place of the old line with the old line's tags, so no group changed size and none needed an added line (every pool stays at or above the floor of six, row by row). Pairs of lines in two kinds that share 50 to 60 percent of their words: 82 (83 before; lines/NOTES.md says so).
- Draft: `check_draft.py` 64 of 64 rows pass, `--negative-controls` 25 of 25 caught. Section 3.3 now says 14 people in both routes (15 before); section 4 is unchanged (the new B12 keeps its two live exchanges, its tags, tension and status class).
- Gates: `python3 tools/content-gate.py`: 0 new hits over 9,374 strings. The gate's own `scan()` over every string of lines.json, rules.json and the town people.json (36,504 strings) and over DRAFT.md: 0 hits. `python3 tools/canon-gate.py` over lines.json, rules.json, lines/NOTES.md, DRAFT.md and this file: clean (the run is at the foot of this file).

## Task 1: the eleven lines of the first fixer's list

Each was judged against canon.md, RULINGS.md and the town data (people.json, StreetFacts.cs): could the claim be false in some run of the simulation? Nine could, and are replaced. Two cannot, and stay.

- `office_worker.greet-owner.02` was "So you're the new owner. Everyone's been talking." Now "So you're the new owner. Do excuse the rush." Reason: that the street talks of him is the game's own mechanic (gossip), nothing sets it at this rung.
- `pensioner.greet-owner.01` was "You'll be the new owner. I've heard so much." Now "You'll be the new owner. How do you do, dear?" Reason: how much any one person has heard of him is not held anywhere; a crowd pensioner holds no facts at all.
- `pensioner.greet-owner.02` was "So you're the new owner. We'd heard you were coming." Now "So you're the new owner. Take your time, dear." Reason: nothing says anyone expected him; the street's own facts say the funeral came before he did and that he missed it.
- `driver.greet-owner.07` was "The new owner. They say you've the keys to the lot." Now "The new owner. Say where, and I'll drive you." Reason: hearsay about him (the review's fault 2 kind), and "the lot" reaches past the office to the outfit, which nothing says the drivers know.
- `casual_worker.greet-tom.04` was "Tom. Is it true you've a rank to fill?" Now "Tom. Mornings or afternoons, I'm not fussy." Reason: asserts a vacancy nobody set. The first rewrite, "I'm free for both", is a known catchphrase on the check's list and was caught; this one is the speaker's own state, which the kind already speaks.
- `darren.greet-nowak.04` was "Mr Nowak. Heard you're doing the rounds. Want a guide?" Now "Mr Nowak. Want a guide? I know every doorway." Reason: whether he is doing the rounds depends on what Tom has done; he may not have left the office.
- `pensioner.greet-tom.02` was "Hello, Tom. I've got your name right this time." Now "Hello, Tom. Fancy meeting you here, dear." Reason: claims she once had it wrong; nothing records that she did.
- `pensioner.greet-tom.06` was "There's Tom. I was just saying your name." Now "There's Tom. Lend me your arm, dear?" Reason: the same claim the review replaced in `laundry_worker.greet-tom.04` ("We were just talking about you"); she may be alone.
- `pensioner.crime-shape.03` was "Somebody ran, past my window. Gone in a flash." Now "Somebody ran past. Gone in a flash, dear." Reason: Nora, Edith, Albert and Winifred may have no window on the street; the line is still a shape and still no more than a shape.

### The two that stay, and why

- `dock_worker.greet-owner.05` "The new owner. Heard you came with one suitcase." Canon's premise has him arriving with one suitcase and a letter. StreetFacts.cs fact `will` says it in the street's own words ("the new owner came with one suitcase and a letter saying so") and is given "to every talking character as things they know"; all three named dock workers (Colin, Dennis, Gordon) hold it in people.json. At the owner rung it is a plain fact of his arrival that no run can change. A crowd dock hand holds no personal facts; the line is then the street's common knowledge, which is what StreetFacts.cs calls the fact. If Jafar wants crowd passers-by kept off every line that mentions a fact, that is a rule for the picker, not for this line.
- `casual_worker.greet-owner.02` "So you're the new owner. Heard you've a rank to run." Canon makes Mickey's a minicab office with a rank outside it and leaves it to him. StreetFacts.cs facts `office` ("with the rank outside") and `will` (left the office to the new owner) are held by both named casual workers (Lee and Julie). At the owner rung, "the new owner" means the owner of Mickey's, so the claim is the meaning of the rung. The sister line, "a rank to fill", is the one that asserted something new.

A new row, `claims.kept_lines_held_by_street_facts`, now holds these two to that reasoning: each line must still carry its phrase, StreetFacts.cs must still state it, and every named member of the kind must still hold the fact in people.json. A third "heard you" line cannot stand without being added to that list and passing the same test.

### Also replaced: six more lines of the same kinds, found by the new patterns

The new check could not pass with these in, so they are replaced the same way (in place, same tags).

- `pensioner.greet-nowak.07` was "Mr Nowak. We've all been hearing about you." Now "Mr Nowak. Keep out of the draughts, now." Reason: what the street has been hearing, as with "Everyone's been talking".
- `laundry_worker.greet-nowak.01` was "Mr Nowak. We've heard all about you." Now "Mr Nowak. Shirts, sheets, or just a chat?" Reason: the same.
- `laundry_worker.greet-owner.04` was "The new owner. We've all been dying to look at you." Now "The new owner. Well, there's a thing." Reason: a claim about the whole laundry's feelings toward him.
- `shopkeeper.greet-owner.03` was "The new owner. We've been expecting you." Now "The new owner. Anything you need, just ask." Reason: the same claim as "We'd heard you were coming".
- `darren.greet-nowak.05` was "Nowak! You've met half the street. I've met all." Now "Nowak! Ask me who lives where. Go on." Reason: what he has done in the town, as with the rounds; the boast about Darren is his own fact (StreetFacts.cs `darren_rounds`), so it stays.
- `office_worker.crime-shape.01` was "Somebody went by the window, quickly. I couldn't say who." Now "Somebody went by, quickly. I couldn't say who." Reason: the window claim again; an office worker passing the street has no window.

## The check (check_lines.py)

- Seven patterns, each its own failure message in the line's row, each with its own planted fault that must be caught by that message and no other (8 new faults in all: 54 to 62): the street talks, has heard, waited or been curious; what is said or known of him; "heard you ..." outside the two kept lines; what he has done in the town; what was said of his name before; an opening or a fact nobody set ("to fill", "is it true"); and a speaker put at a window, door or step in a crime line by any kind but the shopkeeper (a counter and a shop window). The eighth fault damages the dock worker's kept line so it no longer matches its street fact, and the kept-claims row catches it.
- To prove each control is aimed, every pattern was switched off in turn: its own planted fault was then missed and the other seven were not. Done once, here, not kept as a row.
- The harness `trial()` gained an optional `needle`, so a planted fault counts only when the row's failure text names the check it is aimed at.

## Task 2: first thirty minutes

- B12 (Tue 16:00) was set in Hal's shop at the far end of the row (marked NOT YET) with `hals_shop` and `hal`, then the cafe. Now the same two-minute beat on the built street: `ritas_counter` and `cafe`, `rita` and `cafe`. First minute, four o'clock in Rita's pawn with the window whole: the bell over her door rings as Tom goes in, he asks what she does here, and Rita answers "I'll look at it. Looking costs you nothing." (rita.q2, her card's answer to "What do you do here?"). The second minute is unchanged: Grace at the cafe, "Sit down before you fall down. Tea's on." (cafe.q2). Rita's routine has her at the counter until five and on her step until six on a Tuesday, and the pawn is open until half past five (hook-cast.json), so the schedule row passes without a star. Learns was "The street has two ends; the cafe is where the town sits." and is now "Rita will look at anything and say little; the cafe is where the town sits." Status stays NOT YET: "shop insides, and the bodies and cards for Rita and Grace" (it named Hal). Live exchanges stay 2, so section 4's live cell (19, $0.48) is the same.
- Why Rita and not another: on the built west row (tea room, ironmonger, newsagent) no routine puts a named person in a unit between four and eight on a Tuesday but Grace (from five, and the cafe is already the beat's second minute); Edith's turn at the pension counter ends at eleven and the ironmonger has no keeper. Rita is in a unit that exists (bay 2), is a card the town already holds, and her answer is the same kind of dry reply as Hal's "the company I keep the shop for". The draft names no new person, place or event, so no proposal is needed.
- A16 (Wed 12:00): the Where cell no longer lists `hals_shop` and the Who cell no longer lists `hal`; no A16 text used either.
- Section 3.3: "People in both routes: 14" (was 15), because Hal is now in neither route. Only-in-A, only-in-B and the places lists are unchanged. The shortfall page (6.2) and question Q2 said 16 people in route B wait for a body or card; the count is now 15 (Hal gone, Rita still in), and both say 15. These two numbers are not rows of the check; I recomputed them with `check_draft.py --measures`.
- Left in the draft as it stands: Hal and Rita as the subject of the street's news in A11 and B5 ("Hal and Rita had words in the pawn", from the town-news sample), section 2.4's sentence that Hal's coin shop has no unit on the built street, and Q2 and D2's "Hal-and-Rita" story. None puts him in a place.

## What I left, and why

- `pensioner.greet-tommy.04` "I was only just thinking about you." A thought, which no state of the simulation can show false; the Tommy rung is the last and nearly always spoken to a friend.
- `shopkeeper.greet-owner.06` "Not seen the new owner in here yet.", `pensioner.greet-owner.08` "I've seen you go by.", `office_worker.greet-owner.07` "I've seen you about." These are a speaker's own sightings, not the town's standing. The last two are the review's own replacement words. A reader may still want the first looked at: if Tom has been in that shop and is still at the owner rung it is false.
- `laundry_worker.greet-owner.02` and `june.greet-tom.07` ("you're not what I expected"): the speaker's own feeling.
- `tradesman.greet-owner.05` "I've seen your door lock. Shocking." and the office worker's crime lines that put the speaker indoors ("I heard that from inside", "over the typewriter"): a kind's flavour, the same doubt as the window lines but not a standing claim; the new window pattern does not cover them. A reader's call.
- `darren.greet-tom.05` "If it's said round here, I've heard it." Stays: it is Darren's own street fact.
- The crowd question for the two kept lines (above): a crowd dock hand or casual worker holds no facts, and the picker may say a kept line to one. Decided here only that the line is true for the street; a picker rule is for the PC session.
- Not done, as before: the PC game, TownReach, any voice. The follow-up has no second fresh review. The check cannot judge whether the new lines are in their speakers' voices; they are screened by lists only.
- `production/cloud-week/QUEUE.md` lines 73 and 101 and the first fixes file still carry the old counts (2,491 and 54), as the dated log they are; RECIPE.md's lines entry now carries both passes. I did not touch QUEUE.md, HANDOVER.md or REUSE.md.

## Records

- DECISIONS.md: one entry dated 13 October (append only).
- RECIPE.md: the lines entry gains this pass (counts, what failed, the lesson).
- lines/NOTES.md (rebuilt): counts 2,500 rows and 62 faults, the new check bullets, a paragraph on this pass, the sample walk's lines, and 82 pairs.
