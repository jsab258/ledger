# The Ledger screen: a design study and a draft spec (18 November 2026)

Summary: the Ledger should be Tom's own pocket account book, opened anywhere with one key, with four parts (People, Day book, Open, Money). It writes only what Tom saw, heard or was told, says how he knows each thing, and strikes out what proves wrong instead of removing it. The reference games agree on three points. Their books fill themselves. The best ones are organised around identities and time, not around quests. And they fail when a player cannot find again the one thing they half remember. The prototype already counts Ledger opens, slip opens and Tab use; this note adds a timed "find the fact" test and proposes pass bands, all marked as estimates.

Written by a research helper for Jafar's open question (lane queue item 34), about 30 minutes, 18 November 2026. Other games studied from the outside only: reviews, developer interviews, manuals and published analysis, never their files. Tags: (S) source page read on 18 Nov 2026; (SN) search result only, unverified; (P) the project's own documents; (M) from memory, unverified; (J) judgement, not a source; (E) estimate. Pages that could not be reached are listed at the end and are not used as evidence. Not ruled: canon.md and his rulings outrank everything here.

## Questions asked before the research

1. What do canon, RULINGS.md and game-design/ already fix about the Ledger?
2. How do reference games organise a record of what the player has learned: by person, by place, by time, by task?
3. How do entries get in: automatically, or written by the player?
4. How do they show certainty, wrong beliefs and corrections?
5. What did developers say was hard, and what did reviewers and players say failed?
6. Is the book an in-world object or a menu, and does the game pause?
7. Is there published research on how players find things again in journals?
8. What should the prototype measure to tell whether the Ledger is used, findable, and not a crutch?

## (a) What canon and the design already fix

- The Ledger is a notebook of people and events; no minimap; a paper map and street signs (RULINGS, D12, D20, D37) (P).
- He sees his own position, never other minds; no reputation numbers; no stats (RULINGS, D33, D34, D11) (P).
- Tom's reading of things comes from what he saw and heard, never the true state; a witness's story is only as sure as the witness was: "a noise or a shape is suspicion, never 'he did it'" (RULINGS, 28 and 30 Sep) (P).
- Names: a person's name is shown once learned, otherwise a description; the name on a prompt follows the same rule (production/design/ui/STYLE-GUIDE.md) (P). What the town calls Tom (the new owner, Nowak, Tom, Tommy) reads out his standing; Sheila withholds his name until she trusts him (canon) (P). That is something Tom hears, so the Ledger may record it.
- Permanent memory: nothing is ever wiped (canon, the moat) (P). The period-feel note proposes pocket-notebook rules to match: struck through once, never torn out, ends ruled off (production/research/lane/PERIOD-FEEL-LANGUAGE-INTERFACE-2026-11-18.md) (P).
- Mickey left Tom "a book of uncollectable debts"; the office keeps "a book of every fare" (canon) (P). The prototype lists debts "by the names in Mickey's book" and hides a debt until the book is read (tools/lane/prototype/README.md) (P).
- No timers: routes are "standing obligations, not countdowns" (game-design/open-city-spec.md) (P).
- Suggested lines (RULINGS, 1 Oct): Mixed writing; Tab on a keyboard, shown at once on a controller. They are written only from what Tom knows, "his Ledger and the talk so far", never ranked; Tab moves between his own words and the suggestions; no numbers (STYLE-GUIDE.md) (P).
- Key: L opens the Ledger (game-design/how-to-play.md) (P).
- The interface look is C, the evening paper (his pick, 1 Oct, production/design/ui/README.md); recommended then was A, the fare book (red account book, azure ledger paper, typed entries, ballpoint) (P).
- An older, unruled note (game-design/m15-the-world-speaks.md, M15.3) wanted the Ledger to become "Mickey's actual book, a prop on the bar counter you walk to and open. Not an L-key panel", and every toast to become a spoken line or a line in the book. It predates Mickey's becoming a cab office (D19). Its warning still stands: a panel can become "the crutch that let the world stay mute" (P).
- The prototype (tools/lane/prototype): three parts (By person, By event, What's open); entries carry how Tom knows and how sure; a "Noted in the Ledger: ..." line; a yellow slip beside the talk box (F2 folds it); "L or Tab opens the Ledger"; it already counts Ledger opens, slips shown and opened, Tab opens and lines said (P). Known fault: the slip sits over the subtitle line (lane queue item 36) (P). Its entries are written with "me" and "I" ("Calls me", "What I did").
- Prototype scope's Ledger question: "is a book of beliefs, sometimes wrong, readable and worth opening?"; about 22 words a line; every entry traces to a noticed event or a telling (production/lane/PROTOTYPE-SCOPE-DRAFT.md) (P).

## (b) Reference findings

L.A. Noire (2011). Cole's notebook fills itself: "Important information is automatically entered into your notebook", in sections for clues, locations and persons of interest; it opens on its own at the start of an interview, where the player picks a question and later picks a piece of evidence from it to back an accusation; one button opens and closes it at any time; locations can set a waypoint (Rockstar's PS4 manual, read 18 Nov 2026, https://www.rockstargames.com/img/manuals/en_us/LAN_PS4_DIGITAL_MANUAL_ENG.pdf) (S). A player's blog calls it "very incomplete": "I don't want to read through pages and pages of the log to get a refresher", and says they drove to places "just because they were in my notebook", forgetting why (Giant Bomb user blog, undated, https://www.giantbomb.com/profile/fireburger/blog/frustrations-with-la-noire-spoilers-through-homici/81697/) (S, one player). Lesson (J): an automatic book is right, but each entry must say why it matters, and the book must be searchable by person, not only page by page. The waypoint is not for LEDGER.

Return of the Obra Dinn (2018). The logbook is the whole interface: a crew roster with drawings, a plan of the ship, and ten chapters that act as the timeline; each death fills in basic facts automatically, the player writes in names and fates and can revise them; correct fates are confirmed only in threes, "which deters guesswork" (Wikipedia, read 18 Nov 2026, https://en.wikipedia.org/wiki/Return_of_the_Obra_Dinn, citing GameSpot, who called it a "masterpiece of interconnected design") (S). Pope said the book's structure was "extremely difficult to figure out", and that the fun was "figuring out who they are", "filling out a matrix of features for your list of identities" (Game Developer, Bryant Francis, 26 Nov 2018, https://gamedeveloper.com/design/for-lucas-pope-i-return-of-the-obra-dinn-i-was-a-bunch-of-appealing-design-problems) (S). Lesson (J): a book organised around identities and a timeline is the strongest model for LEDGER's People and Day book; the game never confirms whether Tom's belief is true, which fits canon better than Obra Dinn's confirmations.

Disco Elysium (2019). The journal lists current tasks with their progress and the finished ones, and holds the map once found; the Thought Cabinet is a separate screen (Gamepressure guide, undated, https://gamepressure.com/disco-elysium/user-interface/z5e3e8) (S). Kurvitz called the Thought Cabinet a "quagmire" feature that "almost sunk the entire project" (GameSpot on the Audio Logs episode, undated, https://gamespot.com/articles/how-the-feature-that-almost-sunk-disco-elysium-was/1100-6472676/) (S). An accessibility review found the Thought Cabinet confusing, some menu text "too small" at every size, and controller selection "not sticky" (Can I Play That, Coty Craven, 31 Mar 2021, https://caniplaythat.com/2021/03/31/disco-elysium-the-final-cut-can-i-play-that-accessibility-review/) (S). Lesson (J): keep the Ledger to plain records, not a second system of thoughts; text size and pad navigation must be tested early.

Sherlock Holmes Chapter One (2021). The casebook gives hints as icons (for example a group of people: ask passers-by); pinning a clue reveals where to look; the Mind Palace combines clues into a "logic chart"; the reviewer found the icons "a bit hard to keep track of" (Adventure Gamers Hotspot, Andy Hahn Jones, undated, https://adventuregamehotspot.com/review/266/sherlock-holmes-chapter-one) (S). Lesson (J): icon hints are a marker by another name and need a legend; LEDGER should use words, not icons.

Kingdom Come: Deliverance II (2025). The menus hold "a codex of people, places, and events, for those who wish to read further", used beside the opening recap (RPG Site, Adam Vitale, 8 Feb 2025, https://www.rpgsite.net/review/16825-kingdom-come-deliverance-ii-review) (S); a guide says the quest log "tracks active, completed, and failed quests with detailed objectives" (Deltia's Gaming, undated, https://deltiasgaming.com/?p=133669) (S). From memory and not verified: KCD2's quest entries read as a written chronicle in the past tense, and its menus look like illuminated manuscript pages (M). Lesson (J): the period look can carry the record; the house reference (his rule of 28 Oct) is thin here and needs footage watched from the PC before the look is finished.

Red Dead Redemption 2 (2018). Arthur keeps a leather journal in his satchel; side jobs, odd strangers and story events each get "a few words and maybe a sketch", and the tone shifts with how the player plays; read at the end, it felt like an "entertaining little Western novella" (LitReactor, BH Shepherd, 6 Dec 2018, https://litreactor.com/columns/story-tech-arthur-morgans-journal-in-red-dead-redemption-2/) (S). Lesson (J): a record in the hero's own hand is loved when it adds voice, not only data; for LEDGER, Tom's voice should stay clipped and factual so it never claims what he cannot know.

Heaven's Vault (2019). Aliya's past is "a series of dates on her timeline, there for you to explore if you want", which Emily Short found "extremely clever" (Emily Short's blog, 23 Jul 2019, https://emshort.blog/2019/07/23/heavens-vault-inkle/) (S). On resuming, the game gives "the story so far" in no more than five lines, joined by "and" and "but"; labels change with what the player has found and deduced (Zarf, 23 May 2019, https://blog.zarfhome.com/2019/05/heavens-vault-design-ruminations) (S). Lesson (J): a five-line "so far" at the top of the Day book is cheap and helps a player coming back after days.

Shadows of Doubt (2023, early access; full release 2024). Evidence windows pin to a cork board joined by strings that turn from white to red as a link grows more incriminating and vary in width with reliability (Cole Jefferies devblog 4, 2 Jul 2018, https://colepowered.com/?p=33958) (S). PC Gamer liked drawing "literal red strings between names, faces, and locations", but found some cases tedious and the investigation "forensics and other hard evidence rather than anything social" (Joshua Wolens, 23 Sep 2024, https://pcgamer.com/games/sim/shadows-of-doubt-review) (S). Lesson (J): string colour and width are a hidden-number readout; LEDGER says certainty in words instead.

Alan Wake 2 (2023), added because the period-feel note names it. Early case board versions were "too complicated and confusing" for playtesters; the redesign made it "more precise, more chronological", with smaller questions rewarded more often; new evidence sits in a visible "hand", renamed "clues"; the team built a web prototype first for user research; because the game does not pause there, "everything needed to be interruptible" (Game Developer, Chris Kerr, 6 Dec 2023, https://www.gamedeveloper.com/design/true-detective-meets-hearthstone-the-unlikely-inspirations-behind-alan-wake-ii-s-metaphyiscal-mind-place) (S). Lesson (J): chronology beats a free board; a browser prototype for testing the screen is the method a big studio used, which is LEDGER's plan too.

Research on finding things again. Little was found. One study of World of Warcraft players notes that "people may prefer that their access to information be limited" when it makes play more interesting (Harviainen and Rapp, Journal of Documentation, 2018, abstract only, https://www.emeraldinsight.com/doi/full/10.1108/JD-07-2017-0100) (S, abstract). No published measure of time to find a fact in a game journal was found, so the pass bands below are estimates.

What the references share (J):
- Every book fills itself; none asks the player to type notes (Obra Dinn lets the player write conclusions only).
- The good ones are organised by who and when; quest lists are where complaints gather.
- Failures are about finding again: pages to leaf through, icons to decode, a board that grows past reading.
- Certainty shown as colour or confirmation is a readout of the game's hidden state; LEDGER cannot do that.

## (c) Draft screen spec

### Where it lives and how it opens

- Tom's own pocket account book, opened anywhere with L (keyboard) or the View button (pad), closed the same way or with Esc or B. Mickey's fare book and debt book stay real props at the office; reading the debt book is what copies its names into Tom's Money part (as the prototype does).
- The game pauses while the Ledger is open outside talk. In talk, the slip is the view; opening the full Ledger in talk pauses the talk, and the person is still there when it closes (J; Alan Wake 2 shows the cost of not pausing).
- Tab never opens the Ledger. Tab means one thing everywhere: between Tom's own words and the suggested lines (STYLE-GUIDE.md). The prototype's "L or Tab" should change to L only.

### The four parts

Tabs along the top edge like an account book's cut index: People, Day book, Open, Money. Q and E (pad: LB and RB) change part; it opens on the part last used.

1. People. One page per person Tom has met or noticed looking at him. The heading is the name once learned, else a description ("the woman at the paper shop"); when a name is learned the description is struck through and the name written above it. Under it: what they call Tom, if heard ("Calls Tom 'Nowak'"); the dated entries about them, newest first; what is open with them; money between them. Order: most recent first, with an A to Z index down the side. Typing a letter jumps to that letter (pad: the right stick flicks through the index).
2. Day book. One page per day, headed "Tue 14 Aug 1990". At the top, the week so far in at most five lines (the Heaven's Vault recap). Then each thing Tom did that people could talk about, each thing he saw, and talk he walked in on, with the time ("9.40pm"), the place, and who was there that he knows of.
3. Open. Things waiting: what Tom promised, what he was asked, what he asked someone, what is owed by a day someone named. No countdowns: a day is written only if a person said it ("Rent, £18.00, Friday"). When closed, the line is ruled off with the day and how ("Paid Fri 17 Aug"), never removed.
4. Money. An account book proper, £ and p columns: cash Tom counted, what he owes, what is owed to him, names from Mickey's debt book as written there until met. Only sums Tom knows; no running total he has not counted.

### What every entry holds

- When (day and time as Tom would know them).
- What, in at most about 22 words (the scope draft's figure).
- How he knows, in words: "Saw it", "Heard it", "Darren says", "Overheard by the rank". Never a percentage.
- How sure, in words only where the source was unsure: "A shape, could not see who", "Thinks it was a man".
- The source: every entry links to the event or the telling that made it (the prototype's existing check).
- A belief proven wrong is struck through once with the day and the reason written beside it ("Wrong. Ron says it was Cammack's lad, Thu 16 Aug"). Nothing is ever deleted.

### How an entry appears

- The Noted line: "Noted in the Ledger: Darren says the fire started in the back." One line, in the corner above the subtitles' area, never over them; held about 4 s; a soft pencil sound. At most one every 10 s; others wait in a queue and the line says "Noted in the Ledger: 3 things" (J, E).
- It never appears while a subtitle is on screen; it waits for the line to end.
- Option, if the Noted line proves noisy (see the measures): it is replaced by the pencil sound alone and a small corner of the book showing for 1 s, which is closer to M15.3's "toasts die".

### The slip in talk

- A small yellow slip beside the typing coupon, never over the subtitles. It holds the person's heading (name or description), what they call Tom, the last three entries about them, and what is open with them.
- It starts folded to its heading line; F2 (pad: the left shoulder button held) unfolds it; it remembers the player's last choice.
- The suggested lines may draw on what the slip shows and nothing beyond it (STYLE-GUIDE.md: "his Ledger and the talk so far").

### Wording

- 1990 British plain English; clipped pocket-book notes, mostly without "I": "Put the window in at No. 6. Man across the road looked over. Did not see his face." This avoids the prototype's "Calls me" and "What I did" and reads like a policeman's or a clerk's notebook (J).
- Dates "Tue 14 Aug 1990" (typed, so no ordinal, as the 1990 style sheet's 4.1 and 6.4); times 12-hour, "9.40pm" (style sheet 4.3); money "£18.00", "80p", "a fiver" only in quoted speech.
- Names spelt as Tom heard them until he sees them written.
- Canon's content rule applies to every template and every generated line; the content gate reads the Ledger's templates like dialogue.

### Look

- An account book: red cloth cover with a typed label; azure ledger paper, feint blue rules, red double margin; entries typed in Courier Prime with a few words in ballpoint (Kalam), as already licensed in FONTS.md (P). This is look A from 1 October, used for this one object. His pick for the menus was C, the evening paper, so this needs his yes (decision 2).
- Ruled-off ends, struck-through lines, an index cut down the edge. Pages turn with a short paper sound; no page-curl animation longer than 150 ms (J, in line with the style guide's 150 ms fades).
- Sizes in the style guide's units: it sets nothing the player reads below 24 and key hints at 30; proposed here, the book's body text at least 30 units at 1080 and contrast at least 7:1 on the paper (J, not in the style guide; its ink on newsprint is 13:1).

### Controls

| Action | Keyboard and mouse | Pad |
|---|---|---|
| Open or close | L, Esc | View, B |
| Change part | Q, E, or click a tab | LB, RB |
| Move | arrows, mouse wheel | left stick, cross |
| Open an entry's source | Enter, click | A |
| Jump in the index | type a letter | right stick |
| Slip in talk | F2 | hold left shoulder |
| Suggested lines (keyboard only) | Tab | shown at once |

The pad's letters come from Steam Input and follow rebinding (STYLE-GUIDE.md).

### Never shown

- Anything Tom did not see, hear, read or get told; any name before he learns it.
- What anyone else knows or thinks, how far a rumour has gone, who saw him unless he saw them looking or was told.
- Suspicion, heat, standing, trust or certainty as numbers, bars, colours or icons.
- Waypoints, markers, arrows or map pins from an entry; the paper map stays the only map.
- Countdowns.
- The truth of an event. The prototype's end screen, which shows truth beside the Ledger, is a playtest view only and must not reach the real game (J).

## (d) Measures for the prototype to log, with proposed pass bands

The prototype already counts Ledger opens, slips shown and opened, Tab opens and lines said. Add the rest below. All bands are estimates (E) for a first test with the owner and a few friends; none comes from a published source.

| Measure | How | Proposed pass band (E) | What a miss means |
|---|---|---|---|
| Ledger opens per hour of play | count opens, divide by play time | 3 to 12 | Under 2: not needed or not trusted. Over 20: the world is not telling enough by itself (M15's crutch) |
| Time open per visit | median seconds | 10 to 45 s | Longer: hard to find things |
| Time to find a named fact | scripted ask at a set moment ("What did Darren say about the fire?"); time from open to the right entry highlighted | median under 15 s, nine in ten under 30 s, keyboard and pad each | Index or wording fails |
| Find success | share of scripted asks found at all | 90% or more | |
| Slip use | share of talks where the slip is unfolded | 20 to 60% | Under 10%: useless or hidden; over 80%: should start open |
| Noted line followed by an open within 60 s | share of Noted lines | 10 to 40% | Over 50%: lines too vague to stand alone |
| Tab found (keyboard players) | share who press Tab at least once in their first hour | 80% or more | Under: the Tab lines are too hidden |
| Tab lines used | lines said divided by Tab opens; share of turns from suggestions | 30% or more said per open; 10 to 40% of turns | Under: poor lines; over 60% of turns: typing is being abandoned |
| Pad players' suggested-line share | share of turns from suggestions | 50 to 90% | |
| Wrong beliefs | entries struck through per week | at least one per playthrough | None: the book never shows a belief can be wrong |
| Leaks | entries with no source event | zero (existing check) | Hard fail |

On the Tab question: the prototype already shows the words "Tab: suggested lines" beside the coupon at all times. Add a first-steps slip at the first talk ("Tab shows lines Tom might say"), then judge by the Tab-found band. If fewer than 80% find it, show the lines at once on the keyboard too for the first three talks, then return to Tab (J).

## (e) Decisions

1. Where the Ledger lives: A) Tom's pocket book, opened anywhere with L, with Mickey's fare and debt books as props at the office (recommended); B) only Mickey's book, walked to at the office (the older M15.3 idea).
2. The Ledger's look: A) the red account book (look A of 1 October) as the one exception to the evening paper, since it is an object Tom holds (recommended); B) the evening paper like every other screen.
3. Suggested lines on a keyboard: A) keep them behind Tab with the standing key hint and a first-time slip, and change only if the prototype's Tab-found measure misses (recommended); B) show them at once for everyone.

## Sources not reached, or not used as evidence

- Steam discussion on the KCD2 journal: the page showed only an age gate, no posts.
- GameSpot's Thought Cabinet article and Can I Play That's review do not describe Disco Elysium's journal layout; the journal description rests on one guide page.
- Heaven's Vault: the Wikipedia page, Game Developer's GDC write-up and TechRaptor's interview said nothing about the timeline's workings; only Emily Short's one paragraph and Zarf's recap note were used.
- KCD2's journal look and wording: not confirmed from any page read; marked (M). Needs footage watched from the PC.
- Search results only, not opened: Gamepressure's Sherlock Mind Palace guide; the Harviainen and Rapp full text; Mechanics of Magic's Obra Dinn critique; the RDR2 journal pieces on PC Gamer and USgamer; Rockstar's L.A. Noire reception on Wikipedia.
- No published study of time to find a fact in a game journal was found.
