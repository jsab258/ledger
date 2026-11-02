---
name: his-page
description: The one way anything reaches Jafar in LEDGER for a decision, a look or his hands. The one permanent page "LEDGER: Needs you" (writing an item, publishing it to the same link and its data, acting on his tap and closing it), the NEEDS YOU message sent before any report, reading his answers (before any ask or summary, hourly while working, and the nightly read-back), the morning overview with its three pictures, the day's summary, and his progress page. Use it whenever something might need his yes, his sign-in, his hands, money or a licence; whenever a third try is wanted; whenever a whole frame or a whole person reaches its gate; whenever an answer may have landed on his page; before writing the overview, the day's summary or any chat update to him; when the progress page or the morning pictures are due; and whenever someone asks "should we ask him?", "did he answer?", "what's open for him?" or "where is today's report?", even if nobody says "page".
---

# His page

Why: Jafar is not a programmer; he reads LEDGER in the chat and on his pages only (CLAUDE.md, "Talking to Jafar"). Asks spread over daily pages and reports got lost, or were put to him twice after he had answered, so since 2 November every ask is one item on one permanent page, sent first as its own NEEDS YOU message, and his answers are read before anything else is said (RULINGS 30 Oct, 1 Nov, 2 Nov). Shaped like the garment skill (.claude/skills/game-garment/SKILL.md); the gate skill (.claude/skills/gate/SKILL.md, step 9) ends here for whole frames and people. Each step names its source: a tool's usage text, RULINGS.md or DECISIONS.md by date, or a memory note by file name (C:\Users\Jafar\.claude\projects\C--Users-Jafar-ledger-local\memory\). "Check first" marks what the sources do not settle.

**The links**, copied from their homes, never typed from memory:
- Needs you: https://claude.ai/artifact/1VZHkCBAHdw8HBdNHrByL8 (tools/needs_you_page.py, its URL; RULINGS 2 Nov). Its source is production/approvals/needs-you/index.html; the items' home is production/approvals/needs-you/items.json.
- His progress page: https://claude.ai/artifact/EEcWMTp5E9VqKrQsC8KBdk (RULINGS 25 Oct; tools/progress_page.py). Its source is production/progress-page/.
- Every page he has and where it keeps his answers: production/approvals/answers/pages.json.

**Always** (his rulings; none of these bends):
- Plain words, short; no paths, hashes, flags or tool output unless he asks; chat updates at most ten lines, no files, no promised times; a mistake in one sentence, then move on (CLAUDE.md). Never send him FOR-JAFAR.md or any .md file: when he asks for the report, write it in the chat (no-md-files-to-jafar; 28 Oct he asked "Since when do you give me md files").
- One page at one link, updated in place; no daily pages (RULINGS 2 Nov).
- Reports carry no asks; every ask is a NEEDS YOU message and an item on the page (RULINGS 1 Nov).
- His answers are read before he is asked anything about a page, at least hourly while working, and before any summary (RULINGS 30 Oct; 2 Nov 08:00; CLAUDE.md, Records).
- Nothing his rulings settle goes on the page; nothing with a visible fault, debug object or placeholder (RULINGS 30 Oct; approval-page-rules).
- Never idle waiting on him: carry on meanwhile (CLAUDE.md; RULINGS 1 Nov, rule 8).
- Results reach his page as they land (CLAUDE.md; RULINGS 28 Oct); Needs you lists only what is open (RULINGS 2 Nov), so which page carries a result: check first.

**Requests this covers**, for example: "does this need him?"; "ask him for a third try"; "he has to download something only he can"; "did he answer?"; "he tapped done, act on it"; "a street frame passed its gate, show him"; "write the morning overview"; "where is today's report?"; "the progress page is due"; "the read-back hasn't run".

## 1. Ask, or decide?

- Test every would-be ask against his 30 October ruling: decide it yourself, record it in DECISIONS.md and carry on whenever the answer follows from canon, his rulings, the research or the period references, or whenever you would recommend one option and the other differs only in detail (cuts, colours, fits, which reference or method to follow, retries within the two-tries rule). Ask him only for money or purchases; anything needing his sign-in or his hands; licences outside the list; canon, story or scope changes; how a whole street frame or a person looks at its gate (RULINGS 30 Oct; 1 Nov, rule 3). Also asked: a third try, once, with its reason (RULINGS 1 Nov, rule 4); anything touching taste or identity, before merging (CLAUDE.md). CLAUDE.md's page line also names menace among what the page holds (people, street frames, story, menace, canon, money, licences, scope, taste, identity). Deletes follow their own rule (RULINGS, Disk, 29 Oct).
- Anything needing his hands (a purchase, a sign-up, a download, a key) goes into Needs you as soon as it is foreseen (RULINGS 25 Oct), which since 2 November is this page (RULINGS 2 Nov).
- Told him, not asked: a fault set aside without his yes for a third try, named in the summary; an item much bigger than it looked; a sample that cannot pass within its budget, reported plainly as a failed capability (CLAUDE.md, "How the work is done").
- What you decide that he will see in the game gets one line in the day's summary, so he can overturn it (RULINGS 30 Oct).
- **Check:** each ask names which of those kinds it is; everything else is decided, with its DECISIONS line. On 30 October he was asked a licence his 3 October ruling already allowed and a cut that was detail (decide-within-canon-three-a-day).

## 2. Read his answers first

- His taps land in the page's database as verdicts/<item id> (pick, note, at; tools/day_page.py, which stores them; needs_you_page.py docstring). Read them with the ArtifactData tool (list, collection "verdicts", the page's url) before asking anything, before the overview or any summary, at least hourly while working, and at every pause (each background notification, before each commit); act on each at once (step 6); note the last read time in production/handover/HANDOVER.md (RULINGS 2 Nov 08:00; needs-you-one-page; approval-page-rules).
- A verdict's "at" is UTC: add Switzerland's offset before writing his time (his collar answer, stored at 10:47Z, is "11:47" in items.json and DECISIONS 2 Nov 11:50).
- Read the store itself, never a session's summary of it: on 30 September an overview listed two taps as waiting that he had answered at 16:24 (needs-you-reads-every-page-store). An item that still points to another page: read that page's store too; pages.json names its collections.
- **Check:** every open item's verdict looked up within the hour; no answer sits unacted.

## 3. Write the item

- One item for each thing he is asked, in items.json (fields from tools/needs_you_page.py and the items in use): id (a short name and the date, as collar-fourth-try-2026-11-02); added, "YYYY-MM-DD HH:MM" in Swiss time from PowerShell's Get-Date, since Git Bash's clock is an hour behind (MEMORY.md, read-swiss-time-with-powershell); text, what to do in one line with the exact steps (which button, which folder); links, a label and a full https url for every link it needs; recommendation; options, pairs of value and label, the recommended one marked "(recommended)" in its label ("done" alone when left out); state "open".
- Write items.json with the Edit or Write tool, never a Bash heredoc: a Windows path in an item's text (F:\LedgerTools\...) is a doubled backslash in JSON, and a heredoc on this PC halves it (bash-heredoc-backslashes).
- A look at its gate (a whole frame or a whole person): pictures at 2560x1440, never enlarged, opening full size, films with their sound (RULINGS 30 Sep); every frame looked at full size, corners included, and checked by a fresh reviewer for any visible fault, debug object or placeholder first (approval-page-rules; the gate skill, step 9); shortfalls against the bar first, "yes" recommended only for what would pass in a 2026 game (CLAUDE.md; gate-judges-against-the-bar); nothing back for a look unless it has visibly changed since he judged it (approval-page-rules). How a frame's pictures reach this page: check first. The sources differ: the gate skill (step 9) says a link to each full-size picture; needs-you-one-page says "linked or shown on the page"; approval-page-rules says every picture is judged on the page itself, no separate links. The page's "need" kind draws links only (day_page.py), --check takes only https links, and no frame item has been on it yet.
- One phone screen: at most three one-line decisions, any detail folded shut, unless he asks for more (CLAUDE.md; approval-page-rules). An item he has answered is never put back.
- `python tools/needs_you_page.py --check` (a missing field, an id twice, a state not open or done, a bad time, a link not https, a done item without "closed"; ci-checks runs it, so a fault fails the build), then `python tools/needs_you_page.py` (writes page.json and index.html through day_page.py; prints the open and done counts).
- **Check:** --check reports 0 faults; the open count is the one expected; the text can be done without any other message.

## 4. Publish to the one link, and write its data

- The Artifact tool publishes production/approvals/needs-you/index.html again to the same link (from another session: by its url, after reading it); items.json is published beside it, with any file day_page.py lists in files.json under its published name (needs_you_page.py docstring; day_page.py; needs-you-one-page).
- Then the ArtifactData tool writes each item into the page's collection "items", the item's id as the document's, with RULINGS 2 Nov's fields (id, added, text, links, recommendation, state) and "closed", state "done" for closed ones: the advisor's hourly checker reads it (RULINGS 2 Nov; needs-you-one-page). The documents stored so far carry no options, and some "closed" lack their date (production/approvals/answers/1VZHkCBAHdw8HBdNHrByL8/items): copy "closed" whole from items.json.
- **Check:** the page shows the open items oldest first, each with its links, recommendation and time added; the "items" collection agrees with items.json on those seven fields, item for item.

## 5. The NEEDS YOU message

- Its own chat message, sent before any report: it starts "NEEDS YOU:", says exactly what to do, gives every link (the page's full link; exact download links), and nothing else (RULINGS 1 Nov; CLAUDE.md). Write it first in the turn, then the report (asks-end-with-page-link). Any message asking him to tap, click or answer ends with its page's full link, or says plainly there is none (RULINGS 28 Oct).
- One multiple-choice question, the recommendation marked; carry on meanwhile (CLAUDE.md).
- **Check:** the report after it holds no question and no ask.

## 6. Act on his answer, and close it

- Act at once on what was asked (RULINGS 2 Nov 08:00). Anything new in his answer (a note asking for more) goes on the order's waiting list for the next Monday, unless something is broken (RULINGS 1 Nov, rule 1; CLAUDE.md). Then `python tools/needs_you_page.py --close ID "how"`: the item is done with the time and how, and the page is rebuilt. The "how" as in use: "answered yes (11:47): one try, about 2 hours" (items.json). Publish again and set the item's state "done" in "items" (step 4).
- One DECISIONS.md entry, in the pattern "HIS ANSWERS OF <time> ..., ACTED ON", naming what each answer starts (DECISIONS 2 Nov 08:00, 15:04). A ruling goes into RULINGS.md the same day, replacing its line (CLAUDE.md, Records; RULINGS 2 Nov 11:47). A yes that approves something the game uses (a face, a voice, the look) is recorded beside it, to lapse with its basis: `python tools/approvals.py --record THING --against SRC [SRC ...] [--by Jafar] [--note "..."]` (CLAUDE.md; approvals.py).
- "Done" that is not done: check what he did before acting on it. On 2 November two sessions he marked done were still waiting; the item was closed as answered, and the same ask went back as a new item saying what still waited (DECISIONS 2 Nov 11:50; items.json, sessions-still-waiting-2026-11-02).
- **Check:** --close did not print "no open item"; the page and "items" agree; the entry is written.

## 7. The nightly read-back

- Each page's answers are copied with ArtifactData into production/approvals/answers/<page id>/<collection>/<answer>.json; then `python tools/page_answers.py --nightly` writes INDEX.md with the day read (so every read changes it), checks, commits that folder alone when anything in it changed, only when the copy is on wip (elsewhere it stages the answers for the builder), and pushes to wip only as a fast-forward. `python tools/page_answers.py` checks; `--index` rewrites the index; `--fresh 2` (in tools/ci-checks.sh) fails once the read-back is over two days old (page_answers.py).
- The scheduled task ("LEDGER: read back page answers (nightly)" in the Claude app) halted with no new run from 26 October, most likely at a permission question (DECISIONS 2 Nov 07:45, "the likely stall"); after his first answer, the 08:15 run halted again after its page reads, most likely at its one shell command (DECISIONS 2 Nov 11:50); he answered both by about 12:00 and it wrote 11 answers (items.json, sessions-still-waiting-2026-11-02). Whether the next night runs unattended: check first, by INDEX.md's "Read back" date or `--fresh 2`. While it is stopped, read every page by hand (DECISIONS 2 Nov 07:45); stopping another session was refused to the session, so it went on his page.
- A new page is registered in pages.json (id, title, updated, storage, collections) the day it is made (pages.json; DECISIONS 2 Nov 07:05).
- **Check:** `python tools/page_answers.py` prints outcome=PASS; `--fresh 2` passes.

## 8. The morning overview and its pictures, by 07:30

- tools/morning_pictures.py, run by Task Scheduler ("LEDGER morning pictures"), films the same three views (the hook camera by day, the reverse view, the street at night), writes their previews to production/previews/, and rewrites the overview's morning block in FOR-JAFAR.md (the phase, the current and next item from NOW.md, today's beside yesterday's, the Hook sheet), then commits and pushes to wip as a fast-forward; a failure is written into the block, never skipped. `--no-film` redoes its steps 4 to 6 from today's renders; `--block-only` writes the block only. No decision is asked of him with them (CLAUDE.md; morning_pictures.py).
- The rest of the overview, by 07:30 and on change (CLAUDE.md, Records): retention's line (`python tools/retention.py line`); the current and next item; the tester's paragraph; on Mondays the week's visible change, before and after (RULINGS 1 Nov, rule 10), and the risks in five lines; Needs you, at most five, each recommended, gone once answered, the page's link first (FOR-JAFAR.md, 2 Nov); Road to worth playing. Every number real or marked not.
- Write Needs you only after step 2's reading (needs-you-reads-every-page-store).
- **Check:** the morning block carries today's date, or says plainly why there are no pictures (ci-checks also runs `morning_pictures.py --fresh 2`); Needs you matches the page's open items.

## 9. The day's summary, by 07:00

- In FOR-JAFAR.md below the overview: under 200 words, what failed named, ending in something to act on (CLAUDE.md, Records). The form in use: Failed; Done; Decided, yours to overturn (one line for each decision he will see: RULINGS 30 Oct); Act on, the page's link (FOR-JAFAR.md, 2 Nov). Also one line each for any computer use, bridge start or delete (RULINGS 29 Oct; 30 Oct; Disk, 29 Oct).
- His page answers read first (CLAUDE.md). The session can close in the night: write the overview and the summary as they stand before going quiet, and update them in the morning (write-morning-update-before-night, 7 Oct).
- Its commit is the one notes-only commit allowed, and it runs the backup (CLAUDE.md).
- **Check:** under 200 words, counted (no tool caps this file: check first); no ask in it beyond the page's link.

## 10. His progress page, every night

- Read the live page first (the Artifact tool's read), then `python tools/progress_page.py` refreshes production/progress-page/progress.json (the studies and carried items from the order ledger, the 2027 line, the morning pictures' days) and prints each street/ picture a publish must carry; stations and bosses are written by hand from the measures and his rulings, each number re-measured or carrying its date (RULINGS 25 Oct; 1 Nov, rule 9). Publish production/progress-page/index.html again to the same link with progress.json and those street/ files (RULINGS 25 Oct): the page fetches progress.json when it opens (its index.html), and a publish keeps any file it leaves out, so without it the page shows yesterday's numbers.
- A carried item shows in his words: one plain line in progress_page.py's PLAIN, no codes or file names (his note of 26 Oct, there).
- **Check:** `python tools/progress_page.py --check` prints PASS (ci-checks runs it too).

## Records

- items.json is the asks' home and production/approvals/answers/ his answers'; DECISIONS.md one entry per answer acted on and per decision taken instead of asked; RULINGS.md his rulings, the same day; approvals beside what they approve (tools/approvals.py); HANDOVER.md the last hourly read; FOR-JAFAR.md the overview and the summary; the time against the item (tools/timelog.py), helpers' too (CLAUDE.md).
