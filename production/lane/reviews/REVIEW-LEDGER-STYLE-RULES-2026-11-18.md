# Review: Ledger screen study, 1990 style sheet, prototype rules read (18 November 2026)

Fresh independent reviewer, about 25 minutes, 18 November 2026. Checked against canon.md, RULINGS.md, the licence allowlist (ledger-v2/research/license-allowlist.md), production/design/ui/STYLE-GUIDE.md, FONTS.md, README.md, the prototype bundle (tools/lane/prototype/src/bundle, joined; its SHA-256 matches MANIFEST.json) and web sources re-read today. Small fixes were applied in place; nothing committed.

## A. LEDGER-SCREEN-STUDY-2026-11-18.md: PASS WITH FIXES

Sources re-read and matching: Obra Dinn on Wikipedia (fates checked in threes against guesswork, with a late exception of twos the note leaves out; GameSpot's "masterpiece of interconnected design"); Game Developer on Alan Wake 2 (every quote matches); RPG Site on KCD2 (Vitale, 8 Feb 2025, quote exact); LitReactor on RDR2 (Shepherd, 6 Dec 2018, quotes exact); Can I Play That on Disco Elysium (the "too small at every size" summary is a fair reading of "none of them are large enough"); Zarf on Heaven's Vault (five lines, joined by "and" and "but").
Project citations checked: the M15.3 quotes, the scope draft's "about 22 words" and its book-of-beliefs question, L in how-to-play.md, the 1 October pick of look C with A recommended, and "his Ledger and the talk so far". The prototype's "L or Tab opens the Ledger" help line, "Calls me" and "What I did" are all in the bundle.
Canon and rulings: no conflict found. Other games are studied from outside only (17 Nov ruling). Shows no truth, no numbers, no markers, no minimap (D11, D12, D33, D34). Nothing is ever wiped (the moat). No drink, gambling or children. The "bar counter" text is a quote from the older pub-era note, labelled as older than D19.
Allowlist: Courier Prime and Kalam are both in FONTS.md (OFL 1.1). The red account book look needs his yes, and decision 2 says so.
Estimates: every pass band and the Noted-line timings are marked E or J.
Fixed: the style guide was cited for "body text at least 30 units, contrast 7:1", but it says neither. Reworded as this note's own proposal (J), giving the guide's real values (nothing read below 24, ink 13:1).
Fixed: the 150 ms page-curl limit is now marked J, in line with the guide's fades, because the guide has no page-curl rule.
Fixed: dates and times did not match the style sheet (typed "Tue 14th Aug", "9.40 pm"). Changed to "Tue 14 Aug 1990" and "9.40pm" throughout, including the example entries.
Left as is: the decisions are three, each with a recommendation. "Ten chapters" rests on Wikipedia's ten events, which is close enough.

## B. STYLE-SHEET-1990-DRAFT-2026-11-18.md: PASS WITH FIXES

Sources re-read and matching: Wikipedia on the 5p (small coin 27 June 1990); Hansard, 19 Nov 1990 (the old 5p stops being legal tender after 31 December 1990); Hansard, 18 April 1991 (VAT 17.5% from 1 April 1991); edinphoto (22p and 17p dated 17 Nov 1990, which the sheet rightly flags against the Gazette's 17 September); InPublishing (Winfield, 1 Nov 2004: four or five words, cryptic but honest, felt pen, then A2 pre-printed); smugpie's README (drawings under the Open Government Licence, no separate font licence); Wikipedia on Rail Alphabet (1965; New Rail Alphabet 2009; RA2 2020).
Stamp date: no second source settled 17 September against 17 November today. The sheet's choice (primary over secondary) and its marking are sound.
Allowlist: off-list items are named as off-list with the licence each would need (OGL, commercial, public domain, Apache 2.0). Nothing off the list is recommended.
Fixed: rule 1.1 says only FONTS.md faces may be used, but 1.2 to 1.4 name Cutive Mono, Lekton, Patrick Hand, Caveat and Anton, which have no FONTS.md row (they are OFL in PERIOD-PRINT-AND-FONTS.md). Added a line: each needs its row and the three checks first.
Fixed: rule 5.3 called "third person in system text" a project fact. Canon's "third-person, never first-person" is about the camera. Now marked as a choice that matches it, and key hints may still address the player. Rule 9.6 updated to match.
Fixed: rule 9.7 credited the style guide with banning a spinning save icon. The guide bans only a bar that guesses and allows "a short moving piece". Split into P and C.
Checked, fine: the two repository finds (dollars in how-to-play.md lines 64 and 83; "Meridian Courier" in cast-noor-draft.md) are real. The decisions are three, each with a recommendation. No em-dashes or italics.

## C. PROTOTYPE-RULES-READ-2026-11-18.md: PASS WITH FIXES

Search strings: 66 checked with grep -F against the joined bundle, and all occur. Unflagged repeats: `nostmt:1` (10), `sr(500)` (2), `sr(20,!0)` (2), "Nine pounds, since the summer" (2). `Sn(.35)` is flagged correctly.
Numbers checked against nearby code, all matching: the sight formula (4 + 44 x light^1.2, rain 0.3, mist 0.22), the noise hour factors, the heat fade e^(-t/1700), the debts (8000, 1500, 2200, 900, 3000 pence), the fare price ((80 + 0.9 x metres), rounded to 10p, offer 26 s), the statement conditions (0.55, 0.5, 0.05, -0.15), the cell hours (5 or 4, +2) and the 2500/4000 bill, Ellis (Thursday and Friday, 10:00 to 13:00, 2.2), the 45 s game hour, rent 1800 with late from day 5, fear 0.07/0.18, the "saw" check (34 m, 0.9 rad, 2.5, 7, 9, 0.2), and Sheila's, Darren's and Ron's trait values.
Fixed: Terry was listed among the people who never make statements. In the code Terry has no nostmt field. Removed him and noted the ten matches.
Fixed: noted the strings that occur twice.
Fixed: the radio's 14 to 30 second wait after a paid fare was missing. Added.
Content and wording: third person ("him", "Tom") throughout; no drink, gambling or children. Correctly marked UNVERIFIED until Fable's source confirms it.

## Not reached

The 17 September versus 17 November stamp date stays open, on one secondary source each way.
