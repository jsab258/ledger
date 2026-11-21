# Privacy check: crash reports and typed talk (rows 8.2.1 and 10.11), 21 November 2026

Design proof run 3, step (c). The ICO's guidance and the EU's own pages, read 21 Nov 2026 by a reading helper (one ICO page cut short at about half; its strictly-necessary part was read in full). This is a design check, not legal advice.

## What the sources say

| Point | What it says | Source and date |
|---|---|---|
| Scope | PECR's storage-and-access rule covers any software reading or storing information on a device, not only websites, and any information, not only personal data | ICO, What are the PECR rules (13 May 2026); ICO blog, Fact vs fiction (11 Sep 2025) |
| Exceptions | Five: communication, strictly necessary, statistical purposes, appearance, emergency assistance (the last three from Feb 2026); preventing technical faults is only an example inside "strictly necessary", which covers what is "essential to provide the service the user requests", judged from the user's side, and not what is merely "useful" | ICO, What are the exceptions (29 Apr 2026); Osborne Clarke (28 May 2026); ICO blog |
| Consent when needed | UK GDPR standard: a clear act, no pre-ticked box, as easy to refuse and withdraw as to give; say what is taken, why, who receives it and how long it is kept; nothing collected before the yes | ICO pages above |
| Basis | PECR first; where PECR needs consent, consent is also the GDPR basis, and a service may not switch to legitimate interests afterwards | ICO, How do the PECR rules relate to the UK GDPR (29 Apr 2026) |
| Reach | PECR and UK GDPR reach a developer outside the UK who offers the game to people in the UK | ICO, What are the PECR rules |
| AI notice | EU AI Act Article 50(1): people must be told they are interacting with an AI system unless it is obvious; in force since 2 Aug 2026; "obvious" read narrowly; the notice clear and distinguishable at or before the first interaction, not in terms and conditions; fines up to EUR 15 million or 3% of turnover; reaches providers outside the EU whose output is used there | European Commission FAQ (24 Jul 2026); DLA Piper (10 Aug 2026); Chambers (10 Aug 2026, which says the final guidelines give single-player game characters as a case that "may" be obvious; not read in the guidelines' own text) |

## What this does to the two rows

8.2.1 Crash reports. A crash report helps mend the game; it is not essential to the service the player asked for, and a per-crash log with a hardware summary is not aggregate statistics. So the consent route is the safe one, which the definition already takes (asks once, default No). Added to its standard:
1. The question says what is sent (build, time, last log lines, a hardware summary; a save only if ticked), why (to mend crashes), who receives it (the named crash service, if any) and how long it is kept.
2. No and Never are as easy as Yes and Always (same size, same place); the choice can be withdrawn in Settings at any time.
3. The hardware summary holds no serial number, machine id, user name or file paths with the player's name in them; nothing is read or sent before the yes.
4. The report written locally on the player's own PC stays local until the yes and is deleted after 30 days if never sent.
Status: MEASURED (pass or fail on the ICO's published guidance).

10.11 Player data and typed talk. Typed talk sent to a cloud AI service is likely personal data (a player can type anything about himself). Added to its standard:
1. The AI notice before the first talk says plainly that the characters' replies are made by an AI service over the internet, that what he types is sent to that service (named), why, and how long it is kept; it offers offline play (written lines only) as an equal choice, and it can be read again from the pause menu at any time.
2. The notice is its own screen, not a line in the terms; nothing typed is sent before it has been shown and answered.
3. The game keeps no copy of typed lines beyond the save's memory of what was said in the story (the deed, not the text), unless the player reports a line.
4. Article 50 is met by that notice; nothing relies on the "obvious" exception, because a player cannot tell a written line from a live one.
Status: MEASURED (pass or fail on the ICO's guidance and Article 50).

Not settled here and not his question: which crash and AI services are used and their own terms; those are checked when the services are chosen for the Unreal build (outside this proof).
