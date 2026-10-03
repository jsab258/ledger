# Thirty minutes, played and counted (3 October 2026, P4, part a)

Jafar's order of 3 October: "P4: the AI tester plays one full thirty-minute session as a player would, and counts its empty minutes; those become the content list." Part a, as the review planned it (3-PROOFS.md): the whole thirty minutes on the free stand-in talk, to count content and empty minutes. Part b, the talk counted on the real checked path, runs on 4 October within that day's dollar (today's is spent to $0.71).

**How.** The packaged game of 99797f2 (the played copy), from New game, played by the AI tester with real key presses and its pictures, about every 15 seconds.
- **Run 1** (17:51 to 18:22) read the pictures only now and then. It missed the one line telling it about Ron's envelope, and so spent its nights on an empty street: what an inattentive player meets.
- **Run 2** (18:25 to 18:55) read every line the game put on screen (its own log of them) and did what they asked.
- Both records are kept: Saved/Sessions/2026-10-03-175201.jsonl and -182514.jsonl, and the pictures in production/playtest/ai-tester/2026-10-03-1751 and -1824 (local).

## What the thirty minutes contain (run 2)

The clock runs a game day in about twelve real minutes, so thirty minutes is five days.

| real minute | what the player meets |
|---|---|
| 1 | Sheila's walk round: the cab office, the fare book, the locked office, the flat upstairs; the one instruction, Rita's window |
| 2 | Sheila, a hello (the stand-in's "Morning. Quiet one today.") |
| 3 | The window goes in with a crash. Six people see it: Sheila, Ron, Darren and three passers-by |
| 4 | walking back to Mickey's (nothing new) |
| 5 | Sheila (the stand-in's "Funny business round here...") |
| 6 | Ron's envelope, for the ferry landing after ten |
| 7 | Ron; the walk down; "The man at the landing: Mickey's?", the envelope handed over, "Right. Wednesday, same again." |
| 8 | Z to morning (day 2) |
| 9 | Ron (stand-in) |
| 10 | walking (nothing new) |
| 11 | Ron, unprompted: "Heard you did Mickey's run. Watch yourself down there." |
| 12 | Ron; E at Mickey's door does nothing |
| 13 | Z through day 2 (nothing to do); Ada, from her step: "There'll be a pot on at nine tonight, if you want it. I don't ask twice, mind." |
| 14 | Z to evening; Ron's second envelope |
| 15 | **the tea with Ada happens unseen**: no Ada, no room, no words, a dark street in front of her terrace |
| 16 | the walk to the landing in the dark (nothing new) |
| 17 | the second envelope handed over ("Right. Friday, same again.") |
| 18 | Sheila, unprompted: "There he is. The busy one." |
| 19 | walking after Darren, who has walked on (nothing new) |
| 20 | typing with nobody near: three reports filed by accident (a fault, below) |
| 21 | Z: "DS Ellis is on Quay Street this morning, asking after you." The wait stops for him, but **Ellis is never seen** |
| 22 | Z through day 5's afternoon (nothing to do) |
| 23 | Ron's third envelope |
| 24 | Ron: "Ellis was at me about you, boss. Wanted you to hear it from me."; the third envelope handed over ("Sunday, same again.") |
| 25–26 | Z to day 6; walking (nothing new) |
| 27 | Sheila: "That detective stopped me about you." |
| 28–30 | standing about (nothing new) |

**Empty minutes: 11 of 30** in run 2: 4, 10, 15, 16, 19, 22, 25, 26, 28, 29 and 30. Of these, 19 and 28 to 30 are partly the tester's own slowness. Run 1, which missed the envelope line, had about 15.

**"That's all I know": 0** of 15 replies across both runs (the stand-in; the real path's count is part b). Reply delays on the real path are P3's (8.4 s to first sound).

## The content list (the empty minutes, and what would fill them)

1. **The days have nothing to do.** Between the night errands, days 2 and 4 are Z or walking. Something to do by day: Mickey's office, which is hinted at and locked; the flat upstairs; the fare book; a driver's shift; Rita.
2. **The tea with Ada is invisible.** It needs a scene: her room, her lines, what she knows.
3. **DS Ellis is only a line on the screen.** He should be met on the street on day 5, and what he asks should depend on who told him what.
4. **The ferry landing and the quay are unbuilt and pitch black:** a flat slab, box houses floating beyond, a photograph of trees, no lamp. The man at the landing is never seen.
5. **The window has no aftermath.** Rita, a boarded window and the street's own remarks come only when asked. The two passers-by go to the police unseen.
6. **Only three people can be talked to** (and Ada from her step). The street's passers-by cannot ("Nobody near enough to talk to").
7. **The single instruction ends at the window.** After it, the next errand is said once, as a subtitle, and is easy to miss (run 1 missed it). A reminder of what is owed tonight would hold the evening together.

## Faults seen (FINDINGS.md)

- **The played copy is a development build.** The apostrophe key opens Unreal's gameplay debugger over the game. On his Swiss keyboard "?" sits on the same key, so a question typed with no talk box open shows the debugger. The friends' build should be a shipping build.
- **Typing with no talk box open sends the letters to the game as keys.** They walk Tom, and one of them files a report: three reports in run 2.
- **The first letter typed into a just-opened talk box lands at its end,** in the game's own log too ("hanks for the welcome... MickeyT").
- **People stand inside each other:** Ron and Darren in one spot, one body with two heads.
- **Clothes:** everyone in the white base layer, Sheila and Darren barefoot (Needs you, Q3).
- **The camera puts Tom between the player and the person speaking.**
- **The fish market's window at night is a flat cream panel.**
- **The stand-in talk says "the player" and quotes lines back.** The nightly walk uses it; the friends' build uses the real talk.
- **Z stops for a beat the player cannot see** ("tea", "landing", "ellis") and then does nothing until it is past. Run 1 stood through such an evening.
