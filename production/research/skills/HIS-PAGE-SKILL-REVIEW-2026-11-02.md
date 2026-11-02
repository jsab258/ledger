# Review of the his-page skill, 2 November 2026

One fresh reviewer checked .claude/skills/his-page/SKILL.md against its sources. The reviewer was a general-purpose helper: read only, no clicks, no Artifact or ArtifactData calls. The sources were:
- CLAUDE.md and RULINGS.md (30 Sep, 25 Oct, 28 Oct, 29 Oct, 30 Oct, 1 Nov, 2 Nov)
- the tools' usage text and code: needs_you_page.py, day_page.py, progress_page.py, morning_pictures.py, approvals.py, page_answers.py, retention.py, ci-checks.sh, doc-caps.py and timelog.py
- items.json, files.json, pages.json, the page's stored answers, progress.json and FOR-JAFAR.md's overview and summary of 2 November
- the matching DECISIONS.md entries
- the ten memory notes it names
- the gate skill's step 9

**Verdict: SOUND WITH FIXES.** Every command, switch and link exists in its source. One step would have left his progress page on old numbers. One step stated a stall's cause as settled when the record calls it only likely. The rest were omissions and one misquote.

## Fixes (all applied; each re-checked against its source first)

1. **Step 10, his progress page.** It said to publish index.html with the street/ pictures. The page fetches progress.json when it opens (production/progress-page/index.html, line 513), and a publish keeps any file it leaves out. Now progress.json is published with the page and its pictures.
2. **Step 7, the nightly read-back's stall.** It said "halts at its first permission question until he answers it once". DECISIONS 2 Nov 07:45 calls that only "the likely stall". After his first answer, the 08:15 run halted again at its one shell command (DECISIONS 2 Nov 11:50). Now it gives both halts as the records give them. Whether a night runs unattended is "check first", read from INDEX.md's "Read back" date or `--fresh 2`.
3. **Always: where results go.** "Results reach his page as they land" (CLAUDE.md; RULINGS 28 Oct) was missing. Needs you holds only what is open (RULINGS 2 Nov). Now added, with which page carries results marked "check first".
4. **Step 6, acting on an answer.** RULINGS 1 Nov rule 1 was left out: anything new in his answer goes on the next order's waiting list unless something is broken. Now added.
5. **Step 4, the page's "items" data.** The stored documents carry seven fields: id, added, text, links, recommendation, state and closed. They have no options, and some "closed" lines lack their date. Now these seven fields are named and compared, and "closed" is copied whole.
6. **Step 2, his times.** A verdict's "at" is in UTC: 10:47Z is "11:47" in items.json and DECISIONS 2 Nov 11:50. Now the step says to add Switzerland's offset before writing his time.
7. **Step 7, the read-back's commit.** INDEX.md changes on every read and is committed. The commit is made only when the working copy is on wip; anywhere else the answers are staged. Now worded as page_answers.py does it.
8. **Step 6, the DECISIONS title.** The quoted title was wrong; the 15:04 entry reads "HIS THREE ANSWERS OF 14:56 ...". Now it is given as a pattern.
9. **Step 1, the source for his hands.** It cited RULINGS 25 Oct ("goes into Needs you") for this page. Now RULINGS 2 Nov is cited too, which made the page Needs you.
10. **Step 1, what the page holds.** CLAUDE.md's page line also names menace. Now added.
11. **Smaller omissions, now added:**
    - `--check` also fails a done item that has no "closed".
    - ci-checks runs needs-you-check, progress-page `--check` and morning `--fresh 2`, so each failing check fails the build.
    - His answers are read at every pause, not only hourly (approval-page-rules).
    - Some things are told to him, not asked (CLAUDE.md): a fault set aside without his yes, an item much bigger than it looked, and a sample that cannot pass.
12. **Step 3, pictures for a frame.** "Check first" was right, but the sources disagree:
    - the gate skill's step 9 says a link to each picture;
    - needs-you-one-page says "linked or shown on the page";
    - approval-page-rules says no separate links.

    Now all three are named.

## Checked and backed

- **Both links.** The Needs you link matches needs_you_page.py's URL. The progress page's link matches RULINGS 25 Oct and progress_page.py.
- **Every command and switch:**
  - needs_you_page.py: none, `--check`, `--close ID "how"`
  - page_answers.py: none, `--nightly`, `--index`, `--fresh 2`
  - morning_pictures.py: `--no-film`, `--block-only`
  - `retention.py line`
  - approvals.py: `--record ... --against ...`
  - progress_page.py: none, `--check`
- **The page's behaviour (day_page.py).** Answers are stored as verdicts/<id> with pick, note and at. The "need" kind shows links, the recommendation, the time added and the options, oldest first.
- **Rulings.** Every ruling cited matches its line.
- **DECISIONS.** The 07:05, 07:45, 08:00, 11:50 and 15:04 entries back the skill, apart from points 2 and 8.
- **Records.** The items.json examples and the FOR-JAFAR forms are right. No tool caps FOR-JAFAR.md (doc-caps.py).
- **Memory notes.** All ten exist, and their facts are cited correctly.
- **Shape.** Front matter, ten numbered steps each with a **Check:** line, records at the end, and the reasons explained; nothing about 1990 or the story.
- **Read-only checks run by the reviewer.** `needs_you_page.py --check`: 0 faults. `page_answers.py`: PASS (50 pages, 194 answers). `progress_page.py --check`: PASS.

## Not reached

- The live page's database and its published files: no Artifact or ArtifactData calls were allowed. So whether items.json is really published beside the page, and what the live "items" collection holds, is unverified.
- The scheduled task's settings in the Claude app, and Task Scheduler's entries.
- HANDOVER.md has no "last read" line yet, though the memory note asks for one. This is a gap in practice, not in the skill.

## Size and shape

98 lines after the fixes (95 before), under the asked 150.
