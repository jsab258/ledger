# Checklist sweep for the town lane, 28 September 2026

What this is: the 979-item checklist (production/archive/ROADMAP-checklist-to-2026-09-24.md), read against the thirty-minute build for friends and ROADMAP stages 4 and 5. Kept: town-lane items (simulation, save logic, talk, text, measurement) that the build would plainly be missing, that are not done, and that need no Unreal. TOWN.md's list and NOW.md's Handovers were read so nothing already done or handed over comes back. Evidence is from grep and reading the code on branch town at 2951fb2d.

## Candidates, most important first

1. **A39.14 "Relevant NPC states restored consistently"** (line 747; also N7 "Live spoken conversation with memory", line 591). About 5 h.
   Why: friends will quit and come back. The milestone promises the town remembers, and what Tom says to someone is the most personal thing it could remember.
   Not done: TalkHelper `Helper.Answer` builds each engine with `new MemoryStore(card.Id)`, and with no file path that store lives only in memory (MemoryStore.cs: "null => in-memory only"). `ConversationEngine.RememberSaid` writes the conversation there. The reply JSON returns none of it, and there is no message to save, load or reset it. The game writes no "conversation" memory either (ue-probe/Source: nothing found). So after a reload every character forgets the talk. And while the helper keeps running, a new game or an older save carries memories over from the abandoned timeline.
2. **A31.12 "Conversation state that does not repeat completed introductions endlessly"** (line 729). About 3 to 4 h.
   Why: on day 1 of the first hour Sheila shows him round, and Ron and Darren meet him.
   Not done: lena.md:30, rocco.md:32 and sam.md:31 in production/cast/cards all fix "I have never met Mickey's nephew, the new owner." That holds for the rest of the game. The name ladder is built (`PlayerIdentity.AddressBy`, `KnowsName`), but ConversationEngine, CharacterCard and TalkHelper never call it, so the model is never told what this person calls him. The cards change, so check their approvals.
3. **A04.07 "Instructions shown when their actions become relevant"** (line 827; with A04.11, line 831, and A04.13, line 833). About 5 h.
   Why: friends have thirty minutes to learn the game. Stage 4's first hour rests on hints that fire on first occurrence, never on the clock (game-design/first-hour-2026-09-29.md; teaching research).
   Not done: grep finds no hint or tutorial logic in Core. Its only `Hint` is Access's near-miss text. The old hints live in the retired Unity layer (Game/GameController.cs `_hintedDirty`, `_hintedClose`). The first-hour doc lists "the hints on first occurrence" as not built. The Core side is a hint book: each hint's trigger state, fired once, never overlapping, saved, in the world's words where it can be. The screen is the builder's.
4. **A33.01 "A clear current objective or understandable self-directed goal"** (line 855; A04.05 "A clear initial purpose", line 825). About 8 h, after his verdict on the first hour.
   Why: night one's ask is the spine of the first hour. Without it the session has no purpose and nothing for the town to talk about.
   Not done: Core `Campaign` is still the old week rule: "a nightly outfit job (miss too many and you're cast out)", `PatienceLossPerMiss` 0.34 and `Verdict.LostCastOut`, plus bar takings from the pub era. The first hour says refusing "does not fail the game". The doc lists the outfit's asks, and its people talking about them either way, as not built.
5. **A25.11 "A wait or sleep mechanism where schedules make waiting necessary"** (line 722; A25.10, line 497). About 3 h, measured in TownReach.
   Why: the first hour's Meridian result (13 of 13 by minute 30, 7 of them only at minute 30) assumes the old clock of 2 game minutes a real second. At a slower rate day 2 falls after minute 30, or the player has to wait for the evening.
   Not done: the first-hour doc says "the new game has not set its clock yet". grep finds no game-minutes-per-second rate in Core or ue-probe/Source. The probe sets the time in scripted jumps (CrimeProbe.cpp `GNow = GameTime(...)`). Measure the bar at a few rates, recommend one, and say whether a wait is needed.
6. **A01.13 "A usable response to unavailable online services"** (line 775; A48.18 "Error messages that explain the problem in player language", line 587). About 3 h.
   Why: the friends' copies run on the relay with an allowance. When it runs out, every character just says "Catch me later" for the rest of the day.
   Not done: the relay refuses with 403 `allowance_spent` or `relay_stopped`, or 429 `too_busy` (Relay.cs). TalkHelper's `catch (Exception)` turns every failure into one of three `BrushOffs`, marked `timedOut`. "offline" only means no key. No plain-words text for it exists (AiNotice holds only the notice and the thanks for a report).
7. **A13.22 "Consistency between a person's current behaviour and dialogue"** (line 466; A13.23, line 467). About 3 h.
   Why: the claim check allows specifics only from memory or "the scene above". With a thin scene a character is wrong, or flagged, about where they are and what they are doing.
   Not done: the helper takes free `scene` text. The probe sends the fixed "Quay Street, by the parade." to everyone (CrimeProbe.cpp:2660). `CastDay.PlaceOf(id, day, hour)` knows where each person is, but nothing turns that into the scene.
8. **V7 "Writing at volume, and editing it"** (line 1179, staged at 6; the nearest row). About 2 h a card; one first, then the rest only after he approves one in the game (the multiply rule).
   Why: the first hour has Tom meet Ada and June on day 1, with Alison and DS Ellis later. The Hook asks for more residents.
   Not done: production/cast/cards holds only lena, rocco and sam. TalkHelper answers `"error":"no-card"` for anyone else. Their casting sheets (production/casting/*/SHEET.md) give looks and voice, not talk cards.
9. **A31.09 "A predictable response to walking away"** (line 567). About 2 h.
   Why: typed talk is slow to answer, and friends will walk off mid-reply.
   Not done: TalkHelper has no message that cancels a turn. The only cancellation is its patience timeout (`cts.Cancel()`), so a reply that finishes after he has gone is remembered as said (`RememberSaid`), and nothing records that he left.
10. **A49.11 "Optional data collection distinguishable from required operation"** (line 1042; A01.11, line 773). About 1.5 h, text and the gate.
    Why: every typed line goes through our relay to the AI company. Privacy was the top complaint about Whispers from the Star (runtime-ai-business/DELIVERY.md:76).
    Not done: `AiNotice.Text` explains only what a report sends ("and nothing else does"). Nothing tells the player where typed words go, that the relay keeps sizes and costs but never words (Relay.cs), or what the session record keeps.

## Considered and rejected: already done

- A13.13 ambient speech not repeated (line 465): `RemarkLedger` and `StreetVoice.ClearWordsEverySeconds` (6k, 6o).
- A14.03 unaware to suspicious to engaged (line 666), and A31.13 dialogue that acknowledges completed actions (line 730): `StreetVoice.RegardFor`, `Suspecting.Derive`, TalkHelper's "knowing" and "evidence" (items 1, 6n).
- A31.16 subtitles matching the spoken line (line 570), and A31.18 no silence while waiting for a line (line 572): TalkHelper's "first" and "rest", `CorrectLastSaid`, and the patience brush-off (6a).
- A44.05 captions for non-speech sounds (line 575): Core `Captions`. A48.15 no speed change with frame rate (line 586): ue-probe FixedClock.h.
- A39.21 save compatibility after updates (line 937): `SaveCodec.Version`, `MinReadableVersion`, `Migrate`, `SaveFault.FromTheFuture`. A39.20 and A48.16, damaged or repeated saves (lines 749 and 750), on the Core side: the SaveChaos contract.
- AI01 to AI04, the relay and the allowance (lines 605 to 607, 1085): ledger/Relay (`CopyDayUsd`, `StopAt`; 6b, waiting on hosting). AI05, AI06 and U3, the notice and the report (lines 1086, 1087, 1243): `AiNotice`, `ReportAsync`. AI07 (line 1088): production/store/steam-live-ai-disclosure.md. AI08 (line 1089): 6e.
- R01 to R03, the router (lines 602 to 604): `RouterExamples` (done by 28 September, per TOWN.md).
- A35.16 and A35.17, the journal and clues (lines 899 and 900): `PlayerKnowledge` and `KnownLead`, saved under "knowledge". How it reads is 6i, waiting on his ruling.
- U5 playtesting outside the team (line 1090), and O6 a session summary (line 1053): production/playtest/RUNBOOK.md, specs/session-record.md, tools/session_read.py (6p).
