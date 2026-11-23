# BLUEPRINT 10: Shipping

Part of the LEDGER blueprint; the index, the rules of reading and the conflicts are in BLUEPRINT.md. Getting the game out: one full release late in 2027.

Each entry: how it works; its standard and test; the source of the standard; its status; its coverage row. Conflicts are numbered C-nnn and listed in BLUEPRINT-11-conflicts-and-gaps.md.


## 10.1 Release build

The packaged release build and installer.


### 10.1 Release build

- How it works: Done means in the packaged release build, walked by the AI tester. The package is cooked from main or from wip's nightly build; packaged builds are made only for a step's evidence, nightly if wip moved, or main, with no second cook and a rest on Monday, and two Unreal builds never overlap. The release is one full release late in 2027, not early access. On 5 Oct the Shipping package launched through a copy of the desktop shortcut with its own talk program and voice inside.
- Standard: Done means in the packaged release build, walked by the AI tester (CLAUDE.md) Test: nightly packaged walk
- Source: CLAUDE.md (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: CLAUDE.md (Done means); RULINGS 28 Oct, 6 Oct; friends-build MAP; tools/nightly_package.py, tools/p1-packaged.ps1
- Status: outside. Coverage row: 10.1.

## 10.2 Store, rating and disclosure

Store page, age rating, Steam's AI disclosure, price and length statement.


### 10.2 Store, rating and disclosure

- How it works: Steam runs its own content survey and rating (unrated games are hidden in Germany since 15 Nov 2024); a PEGI 16 (ESRB M) target is likely, and what would push it to 18 is the design rule for fights, menace and talk (beating a downed or pleading person, torture, close-up gore or reward for cruelty, taught crime methods, live talk beyond the rated level). The AI disclosure is drafted: live-generated yes (townspeople's replies by Claude, voices made on the player's own computer), pre-generated yes for shipped AI art, voices and text, no for coding help, with seven guardrails described. The store fee is 100 US dollars per game, 30 days between paying and release, the Coming Soon page public at least two weeks before. The length statement is 15 to 20 hours.
- Standard: Steam's AI disclosure as drafted (24 Sep); length 15 to 20 hours (28 Oct) Test: rating questionnaire; disclosure matches the build
- Source: RULINGS 24 Sep, 28 Oct; G4-RATING-AND-STORE (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: G4-RATING-AND-STORE-2026-11-17 s1 to s4; production/store/steam-ai-disclosure.md; RULINGS 24 Sep, 28 Oct
- Status: outside. Coverage row: 10.2. Conflicts settled: C-179.

## 10.3 Friends' builds

A friends' build at the end of every phase from phase 4, on his PC.


### 10.3 Friends' builds

- How it works: A friends' build is made at the end of every phase from phase 4 on, on his PC and his own account, through the shortcut, with his key capped at 5 dollars an evening and no relay. It passes the Meridian Test: friends do not bounce off, the town visibly knows them, talk feels live and he would rather play it, and nothing unfinished is in sight, checked against the twenty basics. The friends' evening comes after the whole street, and before Unreal, real players meet the browser evening once it meets the measured bar, with verdicts beside his and the AI panel's.
- Standard: Meridian Test (3 Oct): they do not bounce off, the town knows them, talk feels live, he would rather play it Test: the Meridian Test
- Source: RULINGS 3 Oct, 28 Oct, 1 Nov (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: RULINGS 3 Oct, 4 Oct, 28 Oct, 1 Nov, 21 Nov; production/friends-build/MAP.md
- Status: outside. Coverage row: 10.3. Conflicts settled: C-180.

## 10.4 Credits and notices

Third-party notices, credits for CC-BY makers, allowlist notices kept.


### 10.4 Credits and notices

- How it works: Third-party notices and credits are an obligation: tools/attribution-check.py fails the build when any third-party asset directory lacks a row in THIRD-PARTY.md. The shipped credits must carry the VCTK corpus credit (the creators, the licence link, the source link and a note that recordings were modified; speakers by number only) and credit CC BY makers of clothes and accessories with brand marks painted out. The credits play after the ending, before play returns in the town; whether they can be opened again from the title is not stated.
- Standard: Every CC-BY maker credited; notices kept (allowlist) Test: script: every shipped licensed file has its notice
- Source: RULINGS 3 Oct, 30 Oct; allowlist (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: THIRD-PARTY.md; RULINGS 3 Oct, 30 Oct; ledger-v2/research/license-allowlist.md; friends-build MAP; GAME-DESCRIPTION-COPY-2 §33
- Status: outside. Coverage row: 10.4.

## 10.5 Release testing

Final passes over the whole game: every ending, every job outcome, long sessions.


### 10.5 Release testing

- How it works: Final passes over the whole game: every ending reached by a scripted route including from a hunted state, every outcome of every job (failures included) reached by a script and leaving a Ledger line, and long sessions. The panel passes at 6 of 8 on a whole playthrough, from the first hour to the ending (BUILD-ORDER M1).
- Standard: ER-END-01, ER-JOB-05 across the whole game; the panel at 6 of 8 Test: all scripted routes in the release build
- Source: DESIGN §16, §4; BUILD-ORDER (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: DESIGN §16 (ER-END-01), §4 (ER-JOB-05); BUILD-ORDER M1; DESIGN §19
- Status: outside. Coverage row: 10.5. Conflicts settled: C-181.

## 10.6 After release

Patches, new districts in updates, a stated position on mods.


### 10.6 After release

- How it works: More districts (Copper Row, the Exchange, the Parade, Fairview, Ironside, Gullwing) come in updates after release, free or paid; there are no paid outfit or car packs and one edition only. There are no mods at release. Patches and a position on mods after release are not designed.
- Standard: More districts in updates after release (28 Oct) Test: none until release
- Source: RULINGS 28 Oct (his ruling or canon). Designed in: RULINGS 28 Oct, 23 Sep; canon.md (seven districts); MECHANICS-MAP M10.4, M10.5; DECISIONS-PENDING 20 Nov
- Status: measured. Coverage row: 10.6.

### GD-06 Mods and community content

- How it works: There are no mods and no community content at release; the part is left out. KCD2 reviews mention mods in 3.8% of reviews, praise and complaint together.
- Standard: left out Test: tester count or rule check
- Source: ST mods theme (KCD2, 3.8 percent of reviews) (left out by his ruling or canon). Designed in: DEFINITIONS GD-06; RULINGS 23 Sep (no mods at release); themes-steam.json ST-184
- Status: out. Coverage row: GD-06. Conflicts settled: C-182.

## 10.7 Platform account, cloud saves and achievements

Steam integration: cloud saves, achievements if any, overlay, account handling.


### 10.7 Platform account, cloud saves and achievements

- How it works: Steam first and no other account. Every save slot and the settings file sync through Steam Cloud; a clash shows both saves with day, hour and place and lets the player pick. No achievements at release, because a pop-up in play is a marker and the vision has none. Pass: a save made on one PC loads on another on the same account (10 trials), 5 forced clashes lose nothing, and no achievement or pop-up appears in play.
- Standard: (1) Two PCs, same account: a save made on one loads on the other; (2) a forced clash shows both and loses neither; (3) no achievement or pop-up appears in play. Test: Two-machine sync test x 10; clash test x 5.
- Source: The description, section 3 (no meters); VISION (no stats or counts); Steamworks Cloud as commonly used [I]. (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS 10.7; GAME-DESCRIPTION-COPY-2 §36; G4-RATING-AND-STORE
- Status: decided. Coverage row: 10.7.

## 10.8 Trailer, key art and store capsule

The pictures and film that sell it.


### 10.8 Trailer, key art and store capsule

- How it works: Named only; not designed beyond: every picture is judged against the Hook sheet and KCD2 frames, dated photographs win, and a yes only for 2026-grade work. The store needs a header capsule 920 by 430, small 462 by 174, main 1232 by 706, vertical 748 by 896, screenshots at least 1920 by 1080 (at least five), library capsule 600 by 900, hero 3840 by 1240, a logo and icons, and a trailer is advised. G4 estimates 12 hours for capsules and five screenshots from the packaged build and 16 for a trailer.
- Standard: Every visual judged against the Hook sheet and KCD2 frames, dated photographs win; yes only for 2026-grade work Test: his eye
- Source: RULINGS 21 Sep, 1 Oct (the look); CLAUDE.md gate (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: RULINGS 21 Sep, 1 Oct; CLAUDE.md (gate); G4-RATING-AND-STORE s3, s4
- Status: outside. Coverage row: 10.8.

## 10.9 Player support and community

Where players report problems and get answers after release.


### 10.9 Player support and community

- How it works: Routes: 'Report a problem' in the pause menu (with 8.2.1's consent), one support address in the menus and on the store page, and the Steam forum as the community place; any live line can be reported from the pause menu or by a key, and Steam gives players an overlay button for illegal live AI content. Pass: every route present, and a test report reaches the support inbox with its build and the player's words within 5 minutes (ten test reports from the pause menu).
- Standard: Every route present; a test report reaches the support inbox with its build and the player's words within 5 minutes. Test: Ten test reports from the pause menu.
- Source: The description, section 34 (line report); sources/a11y-pc.json (PC expectations). (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS 10.9; GAME-DESCRIPTION-COPY-2 §28, §36; G4-RATING-AND-STORE s2
- Status: decided. Coverage row: 10.9.

## 10.10 Legal and company admin

Name search, the company's admin, tax and contracts for selling the game.


### 10.10 Legal and company admin

- How it works: Named only; not designed beyond: name search, company admin, tax and contracts for selling the game are money and accounts matters that are his alone; sessions only record the gap. Licences are not his question (sessions decide by the allowlist), money stays his.
- Standard: none; money matters are his Test: his yes
- Source: map-departments; RULINGS 16 Sep (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: RULINGS 16 Sep, 19 Nov; map-departments gap 7
- Status: outside. Coverage row: 10.10.

## 10.11 Player data and privacy

Consent and data protection for what players type that is sent to the talk service.


### 10.11 Player data and privacy

- How it works: The AI notice is its own screen shown before the first typed line and answered before anything typed is sent: it says replies are made by a named AI service over the internet, what he types is sent to it, why, and for how long, and it offers offline play (written lines only) as an equal choice; it can be read again from the pause menu. A privacy page in Settings repeats it and offers deletion of anything held off the PC. Offline mode plays the whole first hour; no copy of typed text is kept beyond the story's memory of what was said unless the player reports a line; EU AI Act Article 50(1) has applied since 2 Aug 2026.
- Standard: (1) The AI notice, its own screen before the first typed line, says replies are made by a named AI service over the internet, what is sent, why and for how long, and offers offline play as an equal choice; readable again from pause; (2) nothing typed is sent before it is answered; (3) offline mode plays the whole first hour; (4) no copy of typed text kept beyond the story's memory unless reported; (5) the service's retention and the deletion route are as stated. Test: B: first-hour run offline; S: note present before first talk.
- Source: PRIVACY-CHECK-2026-11-21.md: ICO guidance; EU AI Act Article 50(1), in force 2 Aug 2026 (Commission FAQ 24 Jul 2026) (real-world figure or published standard). Designed in: DEFINITIONS 10.11; PRIVACY-CHECK-2026-11-21; GAME-DESCRIPTION-COPY-2 §28, §36
- Status: measured. Coverage row: 10.11. Conflicts settled: C-183, C-184.

## 10.12 Demo, price and wishlists

A demo of the first hour, the price, the wishlist plan.


### 10.12 Demo, price and wishlists

- How it works: Not part of play. A store page with wishlists opens when the Unreal build has the first street frame he approves; a demo, if any, is the first evening only; the price is his money decision.
- Standard: None at this gate. Test: his yes on price
- Source: CLAUDE.md (money is his); the shipping rows 10.1 to 10.5 already OUTSIDE. (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: DEFINITIONS 10.12; CLAUDE.md (money is his)
- Status: outside. Coverage row: 10.12.
