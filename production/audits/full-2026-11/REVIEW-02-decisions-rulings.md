# Review 02: his decisions and the rulings

Reviewer 2 of stage 2, 19 Nov 2026. Read only. Sources: RULINGS.md, canon.md, CLAUDE.md (the repository copy, last changed 4 Nov, commit 8db3212b4), DECISIONS.md, the four orders, production/rulings-enforcers.json with tools/rulings_check.py, the 273 advisor rows and 261 acknowledgements, the 87 page picks with production/approvals/needs-you/archive.json and items.json, and the stage 1 extraction files.

## Summary

His decisions mostly reach RULINGS.md the same day, and the newest (cars, combat, outside-only studies, GTA VI) are recorded faithfully. The weakness is around RULINGS. Three texts still describe an older game or older rules: canon.md (which outranks RULINGS and still says what people know about you is the mechanic, against his 18 Nov "we don't want a gossip simulator"), CLAUDE.md (at least ten replaced lines, loaded into every session and helper) and CHARTER.md (unchanged since 5 Oct). The enforcement he asked for on 17 Nov ("The check is code, not memory") is mostly a label: 33 of 85 standing lines are "enforced" only by a Monday audit whose contents never look at them, and rulings_check.py passes any enforcer whose file merely contains a phrase. The trace is a useful first map but overstates "lost" (7 of 11 are superseded) and "contradicted" (21 rows are 16 decisions, 12 of them one cause), and missed several live conflicts. Costs: records 4 to 5% of spend on 18 Nov (DAILY-2026-11-18.md line 15); 21 commits to RULINGS from 16 to 18 Nov; the enforcer backfill one 1,350-line commit (472fb7233); his attention 273 advisor rows in 15 days and 87 page picks; time lost to stale texts not recorded.

## Re-check of the trace

- Lost (11): 2 confirmed (the negative-finding rule, finding 6; the D7 tone judge, which canon still cites, finding 3). 7 are superseded by his later rulings: concept sheets and map tiles by the 5 Oct reset (RULINGS line 17; the trace's own D-G-084 says tiles moved to CATALOGUE.md), the ten-hour meter and "opening a page" by the pace line (line 37), queue numbers by the order ledger (line 33), the visual-versus-structural boundary by the 3 Nov sized reviews (line 42). 1 is unclear: Panel Cloth and Chaos resizing, which ack 2026-11-13-1625-149 says went into Kiln's suite on F:. 1 is a stale line, not lost: sound by his ear (RULINGS line 118, waiting item 12).
- Contradicted (21 rows, 16 decisions): 18 rows confirmed, 12 of them one cause, CLAUDE.md (finding 2). Two are simply superseded: the 9 Sep phone cards (by the 3 Oct trades line) and "visual work ungated" (by the 7 Oct and 3 Nov gate rulings). D-D-085 is overstated: the "three times 1,200 words" counts the item ledger and studies; the order text itself was about 1,340 words on 9 Nov and 1,880 on 16 Nov.
- Sample of 44 rows drawn at random (16 enforced, 16 in force, 12 superseded): 37 hold; 4 hold only in part (the enforcer covers one clause: D-C-095, D-B-017, D-C-145, plus D-C-094); 3 are wrong: D-G-150 (claims watermark code; the live Pocket voice has none, as the trace's own D-C-125 says), D-C-196 (names, finding 1), D-C-094 (the Hook sheet "enforced" by a check that only keeps pictures out of git). All 12 superseded rows hold.
- Missed by the trace: findings 3, 4, 7 and the phase 2 re-estimate in finding 6.

## Findings, ranked

### 1. "Enforced" mostly means a phrase exists in a file (high)

Impact: he asked for every standing rule to be checked by code; for about half of them nothing checks anything, so drift is found only when he notices it, which is the pattern he complained of on 17 Nov.

Evidence:
- His words, advisor 205 (17 Nov 16:38): "The check is code, not memory." He had to ask (16:36, advisor 204): "Is this something you're going to remember for a bit and then forget". CLAUDE.md line 43 had required "Each rule gets a check failing the build where possible" since 5 Oct.
- tools/rulings_check.py lines 48 to 59: "monday-audit" returns no fault without condition; any other enforcer passes if the file exists and contains the quoted words. Nothing checks that the enforcer runs or tests the ruling.
- production/rulings-enforcers.json: 33 of 85 entries name only "monday-audit", among them combat (fists never kill alone), Mickey's death, "no jump", purchases his alone, the 18 Nov publish gate and the camera.
- The Monday audit as defined never reviews them: advisor 183 (16 Nov) lists twelve numbers (finish date, pieces, spend, faults, his page); the scheduled weekly task (work/scheduled-tasks-2026-11-19.md item 3) runs five pass or fail tests on efficiency; advisor 205 point 4 only lists the rules added that week. First run 23 Nov, so these 33 lines have had no check of any kind.
- Code enforcers that test something else: the Hook sheet line by push_guard.py's "a picture or film added or changed outside production/previews/"; "No voice is cast without his yes" by tools/voice-cast-check.py, which reads the old Unity build's CastTier1.cs and VoiceBank.cs (no p267, p227 or p286 in either) and is run by no hook, gate or ci line; "The story's spine" by the words "real brand besides" in canon-gate.py (a message about "google"); Mickey's office by tools/office_look.py, a picture runner; "DECISIONS.md ... about 40 words" by doc-caps.py, whose line 45 says DECISIONS.md "had no cap and have none".
- tools/names-gate.py lines 39 to 42 list the 24 Sep renames only; canon.md line 97 adds "Father Emil became Father Brendan Walsh" (28 Sep). The self-test checks list against canon one way only (lines 24 to 25). content/dialogue/pub-regular-v1.json line 41 still says "Father Emil knew your uncle". Whether the Unreal build ships that bank is not established here.

End: rule. rulings_check fails an entry whose only enforcer is "monday-audit" unless the Monday audit file carries a dated verdict line for it (a quarter of the 33 each Monday, so each is judged monthly); fails a code enforcer not called from ci-checks.sh, the hooks, fresh_gate.py or the DAILY file; names-gate's self-test checks canon's NAMES block against its list both ways. List item: replace the five wrong enforcers above with real checks or honest "judgement" entries.

### 2. CLAUDE.md, read by every session and helper, carries ten replaced rules (high)

Impact: helpers see CLAUDE.md, not RULINGS, so they work to rules he withdrew; it already misdirected one helper, and it is the root of 12 of the trace's 21 contradictions.

Evidence (CLAUDE.md line, against what replaced it):
- 16: "20% kept for him", against RULINGS line 37 (the last 10%, his tap keep-monday-share-2026-11-06).
- 11 and 36: RECIPE.md as the notebook, against RULINGS line 36 (NOTEBOOK.md takes the lines; RECIPE.md is read before any first try).
- 32 and 33: FOR-JAFAR.md summary and overview, against RULINGS line 36 ("No FOR-JAFAR.md"; the file's first line says stopped 9 Nov).
- 37: "No separate recipe work, no recipe tests", against RULINGS line 36 (monthly cold re-run, "over CLAUDE.md").
- 51 and 52: reference first "Mafia or Kingdom Come II ... their files on demand" and "Mafia's missing numbers fetched", against RULINGS line 53 (outside only; Mafia "never the yardstick").
- 53: "a third try needs his yes first", against RULINGS line 27 ("None asks him"). DECISIONS.md line 420 (18 Nov 13:13): "the helper's 'needs his yes' is CLAUDE.md's older rule".
- 67: "a full disk: stop and wait", against advisor 189 (17 Nov 08:02, his words "can't afford idle time because of an easily avoidable problem").
- 17 and 24 cite "RULINGS 1 Nov, the week's rules" and a "NEEDS YOU:" message rule; neither line exists in RULINGS now. Line 31 says its own cap is 1,000 words; doc-caps.py line 31 sets 1,625 (it holds 1,622).
- Why it stays: his pick of 9 Nov 09:42 ("No paste into CLAUDE.md: the five changes go into the rulings instead", archive.json item confirm-chat-0813-2026-11-09), and DECISIONS.md line 341 (17 Nov): "CLAUDE.md is his and at its cap". RULINGS now says "over CLAUDE.md" twice (line 36).

End: list item. The builder drafts one shorter CLAUDE.md that points to RULINGS for everything RULINGS governs and drops the ten lines (net fewer words), put to him as one ACTION item (his-setting) with the before and after. Rule: rulings_check fails while any RULINGS line says "over CLAUDE.md" for more than seven days.

### 3. Canon and the charter still describe the old game (high)

Impact: canon outranks everything, so a session that follows the stated order of authority applies a spend rule that starves the fights, driving and jobs he now wants first; the "what is the game" question has four homes.

Evidence:
- canon.md lines 172 to 179 (D24, 14 Sep): "It is a small dense town where what people know about you is the mechanic. Anything that does not feed perception, memory, gossip or consequence gets the smallest budget". Line 14: "open-town crime sim and social RPG". Line 66: "The bar is the Meridian Test".
- Against: canon.md lines 155 to 170 (18 Nov pillar: "Talk stays the moat, never the main thing the player does"; his words "we don't want a gossip simulator"); RULINGS line 53 ("KCD2 is the bar", recorded only in RULINGS, which canon outranks); RULINGS lines 11 and 12 (AAA driving end state, AAA guns with an escalation dial).
- canon.md line 7: "Tone is the judge's under D7, not a gate". The D7 judge (a calibration sample of 30 to 50 items, 80% agreement) was never built (trace D-G-040).
- canon.md lines 9 to 10: "A ruling that changes canon edits canon in the same batch (Jafar, 2026-09-16)". That rule should have caught D24 on 12 Oct (fighting AAA), 28 Oct (15 to 20 hours, the release) and 18 Nov.
- CHARTER.md (unchanged since commit 6679e4a1b, 5 Oct): goal "Thirty minutes of Quay Street", "No new acts, combat programme ... before this works", "20% kept for Jafar", "$1-a-day measurement". RULINGS line 17 still says "CHARTER.md and PLAN.md replace every list", while his 17 Nov 21:57 decision made the loop prototype "the spec of record" (DECISIONS.md line 339), a status no ruling carries.
- He raised the drift himself: 18 Nov 15:19 (advisor 224), "we had all those discussions months ago. Seems like we drifted"; 18 Nov 16:02 (advisor 226). The trace marks both D24 rows "in-force", and D-G-071 calls the pillar the "same text".

End: ruling for him: "Canon's 'What LEDGER is not' still says what people know about you is the mechanic and everything else gets the smallest budget: A) rewrite it to his 18 Nov pillar, name KCD2 as the bar in canon and drop the D7 judge line (recommended), B) keep it as written?" List item: retire CHARTER.md or rewrite it to the 28 Oct release, and give the prototype's "spec of record" status one line in RULINGS.

### 4. The outside-only ruling has not reached the order machinery (medium)

Impact: a forbidden method (reading other games' files) is still an open item, and the order check will force it into the next order unless he spends a tap dropping it.

Evidence:
- RULINGS line 53 (17 Nov 22:33, advisor 214): other games' files "never opened".
- production/orders/2026-11-16.md line 91: "`n16-11` **carried over** Numbers from the games' files: UE4SS once per game"; NOW.md line 12: "n16-11 the games' numbers".
- tools/order_ledger.py lines 18 to 19: an id not done or dropped must reappear in the next order; "dropped (needs "Jafar")". Lines 22 to 25 still require "a number or method from Mafia or Kingdom Come II" (selftest "Reference: Mafia's 1.65 m").
- DECISIONS.md line 319 (17 Nov 18:55, four hours before his ruling): n16-11 "decided under his 11 Oct study ruling, not asked: the study reads the games' files as it already does (FModel, published keys)".
- The trace marks D-D-146 (the carry-over) "done".

End: rule. When a ruling forbids a method, the same commit marks every open order item that uses it "dropped (Jafar, ruling <date>)", and order_ledger.py accepts a ruling's date as his drop. List item: order_ledger.py's reference words become "KCD2, GTA or a study, measured from outside".

### 5. Two voice rulings lapsed silently when Pocket replaced the old voice (medium)

Impact: his ruling on marking generated speech and his own acting picks for Ron and Darren no longer hold, and nobody asked him.

Evidence:
- RULINGS line 77: "D50: the voice watermark is kept on generated speech"; "25 Sep: Ron's and Darren's lines made in advance use an acted reference".
- tools/voice-live/pocket-server.py has no watermark code (the call exists only in voice-server.py line 452, the old Chatterbox route); THIRD-PARTY.md lines 158 to 164 list Pocket's obligations without one; the allowlist (line 4) ties "keep watermark" to Chatterbox.
- He chose the acted reference in all seven of Ron's and Darren's lines he picked (production/archive/DECISIONS-to-2026-11-09.md line 40). Pocket copies read VCTK clips (production/research/voice-latency/POCKET-DELIVERY-2026-10-26.md).
- His 26 Oct picks (archive lines 691 to 698) were on Pocket passing a listening test; no record says he was told either ruling would lapse. CLAUDE.md line 57 lets approvals lapse with their basis; rulings have no such rule.

End: ruling for him: "The live voices carry no watermark since the switch to Pocket: A) add an open-licence watermark to Pocket's output, researched first (recommended), B) narrow D50 to the old voice only?" List item: one Pocket sample of Ron and Darren from an acted reference on his listening page, so his 25 Sep choice is either kept or retired by him.

### 6. Promises to him that ended in nothing (medium)

Impact: he raised these as top priorities; each was acknowledged and then not carried out, which costs his trust and repeats the "I had to tell you" pattern.

Evidence:
- Negative findings: his words 9 Nov 13:50 (advisor 2026-11-09-1415-59), "should not have required my pushback; research was sloppy". The ack (15:31): "goes into the next batch on his page as one tap, yes recommended". No such item exists among the 87 picks or the 104 page items in items.json and archive.json; no rule in RULINGS, CLAUDE.md or .claude/agents.
- Phase 2 re-estimate: his words 9 Nov, "an absolute must; top priority". production/progress-page/progress.json: the 16 Nov point is "last point less the 21 h of phase 2 work in the time log; not re-estimated", the method advisor 183 forbade ("never last point minus hours logged"). His 1 Feb scope test (RULINGS line 15) rests on this number.
- RULINGS items marked owed with no list item: "the flat voices' experiment is owed" (since 24 Sep, line 77); a listening page for Danny, June and Father Walsh (27 Oct, line 76; none found); phase 5 "designed during phase 2" (line 19; no design file found); grain, grade and depth of field "owed" (15 Sep, line 61).

End: rule. Every RULINGS clause containing "owed", "to be finished" or "gets a ... page" names its order or waiting-list item, and rulings_check fails one that names none. List item: the negative-finding rule goes to his page as promised (or into the research helpers' brief, saying so in one line); the 23 Nov Monday file redoes the phase 2 figure from measured costs.

### 7. Rules about his own process that practice dropped, still counted in force (medium)

Impact: the records tell him the week is protected and the files are short when neither is true, so he cannot judge what his rules are buying.

Evidence:
- "Nothing new between Mondays" (CLAUDE.md line 17; order of 2 Nov line 130; NOW.md GOAL "anything new goes on its waiting list"). This week alone, work started mid-week by his picks: the cloud lane (17 Nov 17:15, advisor 206), the synthesis (18 Nov 20:47, advisor 230), GTA VI text study from 19 Nov (advisor 235), this audit ("Do it now", about 8 to 15% of a week by advisor 237). The trace marks D-D-078 "in-force".
- DECISIONS.md "about 40 words" (RULINGS line 36; its own head, line 3): 444 entries, median 66 words, the newest 60 a median of 85.5 and up to 171; 61 entries at 45 words or under.
- "Startup files edited at most once a day" (RULINGS line 23): RULINGS.md committed 8 times on 17 Nov and 8 on 18 Nov; the handover 33 and 21 times. The token audit measured mid-session startup-file changes at 0% of cost (N09-11-CACHE-AND-TOOLS-2026-11-08.md line 46), so the rule has no measured basis. The trace counts D-C-030 "enforced".

End: ruling for him: "New work between Mondays: A) keep the 1 Nov rule, the advisor parking new asks on the waiting list unless he writes 'now' (recommended), B) drop the rule so his picks start at once?" Rule: doc-caps.py warns on any new DECISIONS entry over 60 words. The startup-files clause goes to him as a one-line question when the next ruling batch is shown (a code change to a ruling needs his yes first).

### 8. Stale lines inside RULINGS while the cap squeezes his new words (medium)

Impact: RULINGS breaks its own head rule ("Done, repeated or replaced rulings leave the same day"), and with the file at 4,899 of 4,900 words the session compresses his newest wording to make room instead.

Evidence:
- Line 84: "2 and 8 Oct, stopped: procedural tailoring ... draping tailored jackets"; line 82: "tailoring waits for the tools". Against line 83 (6 to 8 Nov tailor boss) and line 39 (13 and 18 Nov Kiln, the week's main item, n16-1).
- Line 118: "D26: sound is a lane", against CLAUDE.md line 15 (one session, no lanes) and line 39 ("crowd, card memory, sound later").
- Line 98: "the paid router stays ... three router changes owed", against line 40 (12 Nov: talk models from any provider, re-checked monthly).
- Room-making: DECISIONS.md line 435 ("its wording compressed", the KCD2 ruling), line 450 ("room made by cutting repeats"); 21 commits to RULINGS.md from 16 to 18 Nov.

End: list item: one sweep removes these three lines (and finding 5's two once he answers), freeing room before any more of his words are compressed. Rule: a ruling's commit first removes the lines it replaces and names them in its DECISIONS entry.

### 9. Old-version decisions dropped in the rebuild, found only when he asked (medium)

Impact: July decisions the 5 Oct rebuild did not carry come back one at a time, each costing him a question.

Evidence: advisor 234 (18 Nov 22:07): his July answer that a car hurts and never kills "never reached the rebuild's canon or rulings"; it surfaced only because he asked "how do we balance consequences w driving?" (legacy/studio-v2/game-design/decisions-answered.md line 419). Advisor 224: "verbs first" was a July discussion too (same file, line 17). The 3 Nov RULINGS rewrite checked dropped lines against DECISIONS and CLAUDE.md only (commit baba7ad56), never legacy/.

End: list item: stage 3 lists the legacy decisions the trace marks in force that no current text carries, as one batch on his page, with the two truly lost rows.

### 10. The trace's page-pick rows were classified blind (low)

Impact: 45 of his 87 page decisions were judged without the question he answered, so the trace's counts should not be quoted as findings.

Evidence: 45 rows say "question text not stored"; all 45 ids are in production/approvals/needs-you/archive.json or items.json with text, options and close line (for example tries-rule-2026-11-09, closed "RULINGS 7 Nov tries line amended").

End: list item: before stage 3 quotes numbers, re-run the page-pick rows with archive.json joined and correct the lost and contradicted counts as in the re-check above.

## What Jafar raised himself in this area

- 9 Nov 13:50, sloppy negative research (finding 6); should have been caught by CLAUDE.md line 49 ("before ... calling anything impossible").
- 17 Nov 16:36 and 16:38, rules not enforced (finding 1); CLAUDE.md line 43, standing since 5 Oct.
- 18 Nov 15:19 and 16:02, drift from "verbs first" (finding 3); canon.md lines 9 to 10.
- 18 Nov 16:43, Mafia not the bar (findings 2, 4); RULINGS line 56 already named KCD2 frames when the 28 Oct reference rule was written.
- 18 Nov 21:54, car deaths lost since July (finding 9); the 3 Nov rewrite's check of dropped lines.
- 18 Nov 21:10, "why didn't this come to my needs you page" (advisor 231); needs_you_page.py --waiting, built that evening (DECISIONS.md line 446).

## Counts

High 3, medium 6, low 1.
