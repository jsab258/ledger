# Fable loop prototype: next round prompt (18 November 2026)

For Jafar: this is the next message for Fable in the loop-prototype chat (the walking-and-talking game, not the driving study).
Paste everything inside the box below into that chat once Fable's current round there is finished; it works whatever that round built.
It is a medium round: mostly fixes, test handles and one new Ledger screen, no new systems.

```
Fable, this is the next round of the LEDGER loop prototype. Start from your latest version and keep what works; if something below is already done, say so and move on. No new systems: make the game readable, fix known faults, add one Ledger screen test.

1. The readable source, first

Send the game's source as you wrote it, before bundling or shortening names: one file per part (seeing, gossip, the Ledger, money and debts, police, routines, talk, saving, scenes, rendering), as files or a zip, with three.js as a dependency pinned at 0.187.0, the build command, and the design notes. The project keeps it in its repository with tests; the published page must be what this source builds.

2. Fix these faults

a) Restoring a save through the test hook (window.LEDGER.restore) leaves every person holding their old memory object, and the restored memories have no index. The game's own Continue rebuilds the people; the hook does not. Make restore do the same.
b) Ron sets off home at 23:36, walks about 3 metres from the rank and stops, still marked as walking, and is still on the street at 03:00. Fix it, and check that every named person who sets off for a place gets there.
c) On Tuesday night the game paused once and did not resume within a minute. Cause unknown. Add a check that finds it: every pause and resume logged with the game time and its reason, plus a test-hook check that steps through Tuesday and Wednesday nights and reports any pause with no resume. Fix what it finds.
d) The yellow slip in talk covers the subtitle line. It must sit beside the typing box and never over the subtitles.
e) Rent: Sylvia's line says "Friday, by six", but the code marks it late only from Saturday 00:00. Make the code follow the line: late from Friday 6pm game time.

3. Test-hook additions

Add hook calls for the checks skipped today because they need key presses:
- choose a suggested line, and answer a yes/no decision in talk (this covers collecting or striking out a debt);
- read and advance a written scene, and pick its choices (Sheila's first scene that reads Tom the book; offering and taking jobs);
- the night job's drop door (the E prompt), so dirty money reaches the tin; and washing through Sheila;
- the fare: accept the radio offer, pick up, drop off, with the fare places readable by name instead of found by the shape of their data.

Every number in the hook readable: plain names with units (pence, game minutes, metres, real seconds), and every rule's number in one named table the hook exposes (say LEDGER.rules).

4. The Ledger screen test

A test only: the real game will judge it. Build it to measure, not to finish.
- Opens anywhere with L only, closes with L or Esc. Tab never opens it: Tab means only the suggested lines in talk. It pauses the game, or the talk.
- Four parts as tabs along the top: People, Day book, Open, Money; Q and E change part; it opens on the last part used.
- People: a page per person met or noticed, headed by a description until the name is learned, then the description struck through with the name above; newest first, an A to Z index, a typed letter jumps there.
- Day book: a page per day ("Tue 16 Oct"), the week so far in five lines at most, then entries with time and place.
- Open: things waiting, a day only if someone said it, closed lines ruled off, never removed. Money: pounds and pence, only sums Tom knows.
- Each entry: when, what (22 words at most), how Tom knows ("Saw it", "Darren says"), sureness in words only when unsure, and its source event. Never percentages, bars, colours or icons. A wrong belief is struck through with the day and reason, never deleted.
- Wording: clipped notebook entries without "I" or "me" ("Calls Tom 'the new owner'", not "Calls me"). Money "£18.00", "80p". Times "6.30pm". Dates "Fri 19 Oct".
- The Noted line: never over the subtitles and never while one shows, about 4 seconds, one per 10 seconds at most, extras queued as "Noted in the Ledger: 3 things".
- The slip in talk starts folded to its heading; F2 unfolds it; it remembers the last choice.
- The end screen's truth view stays, labelled as a playtest view, with a setting to switch it off.

Log these measures, show them on a screen, export them as one JSON file and through the hook: Ledger opens per hour of play; median seconds open per visit; scripted "find the fact" asks at set moments (time from open to the right entry, and whether found, keyboard and pad apart); share of talks with the slip unfolded; share of Noted lines followed by an open within 60 seconds; whether Tab was pressed in the first hour; lines said per Tab open and share of turns from suggestions; entries struck through per week; entries with no source event (must be zero).

5. Keep everything else as it is

Change nothing else. Nothing on screen the player could not know; names only once learned. No alcohol or gambling, shown or spoken of; tobacco is fine; no children anywhere. Tom is seen in third person. Britain, October 1990.

When done, send back:
- the source files and build command;
- a short dated changelog: what changed, item by item;
- the measures JSON from one full week played;
- anything you could not do, and why.
```
