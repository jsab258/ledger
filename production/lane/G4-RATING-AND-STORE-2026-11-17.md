# G4: age rating, Steam store page, platform (17 Nov 2026)

Reviewed 17 Nov 2026: sound, two facts confirmed at source (capsule sizes, Swiss law dates), fixes applied.

Platform is settled: PC, Windows, Steam. Sources read 17 Nov 2026 unless marked. [READ] read at source today, [SS] search snippet only, [I] inference, est. estimate.

## 1. Age rating

Steam does not run the IARC questionnaire. It uses its own content survey and gives its own rating from it; in Germany, unrated games have been hidden since 15 Nov 2024 [READ, Steamworks content survey page, Germany]. PEGI through IARC: one free questionnaire gives PEGI, ESRB, USK and others, but only on stores that take part (Microsoft Store, Epic, consoles) [SS, PC Games Insider; I for the store list]. A Steam-only game gets no automatic PEGI. Options: rely on Valve's survey rating (no fee found), or get a real PEGI or ESRB by listing a copy or demo on an IARC store, or by a paid Games Rating Authority review (fee not found).

What moves PEGI 16 to 18 [READ, askaboutgames.com PEGI page]:
- PEGI 16: realistic, sustained violence against humans with blood and injuries; crime without punishment; the crudest swearing; illegal drug use shown; prominent tobacco.
- PEGI 18: torture, severe pain or injury to humans; violence against defenceless or vulnerable people; glamorised drug use; detailed criminal methods; very strong language throughout; gambling.

UK: the Video Recordings Act 1984 (revived 2010) still covers games. The Games Rating Authority rates them under PEGI, and selling a PEGI 12, 16 or 18 game to someone under age is an offence [READ, Anglesey Trading Standards, updated Dec 2025]. The page does not say clearly whether pure downloads are covered. The duty falls on the seller, here Valve [I].

Switzerland: the federal law on youth protection in film and video games (JSFVG) came partly into force on 1 January 2025. Industry bodies have two years from 1 January 2025, so to the end of 2026, to write rules the government then makes binding. Providers must show content symbols, offer parental controls and let users report content [READ, Federal Social Insurance Office page]. PEGI is not named there [READ]; Swiss industry has backed PEGI since 2016 [READ, SGDA].

US: ESRB ratings for digital games stay free through IARC [SS, PC Games Insider].

Likely rating for LEDGER [I]: PEGI 16 (ESRB M). Fists, improvised weapons and rare guns with blood sit in 16 (his rulings: "fists, improvised and carried weapons, rare guns", and guns only after melee works); tobacco is fine; no alcohol or gambling helps. Pushes to 18:
- beating a downed, pleading or tied person, or any torture;
- close-up wounds, gore, or rewards for cruelty;
- real crime methods taught step by step;
- drug use shown as glamorous;
- live AI talk producing very strong language, sexual talk or threats beyond what was rated.
Keeps 16: fights end in knockdowns or flight; modest blood; menace spoken, not shown at length; crime has consequences.

## 2. Generative AI on Steam

Since January 2024 the content survey has an AI section with two kinds [READ, PC Gamer, Jan 2026; SS, GamingOnLinux, Jan 2024]:
- Pre-generated: AI-made art, sound or text made during development. Same rules as other content.
- Live-generated: made by AI while the game runs. The developer must describe the guardrails that stop it producing illegal content. Players get a Steam overlay button to report illegal live AI content.

January 2026 change: only AI content that ships in the game or appears in marketing and is "consumed by players" must be disclosed; coding helpers and office tools need not be [READ, PC Gamer, 16 Jan 2026].

LEDGER must declare [I]: live-generated, yes (townspeople's talk, and voices if made live); pre-generated, yes for any AI-made faces, textures, voices or text shipped or on the store page; no for AI-helped code.

Guardrails to describe (draft) [I]:
1. Every reply passes a content check before it is shown or spoken; a failing line is replaced by a written fall-back.
2. The model gets each character's sheet, the town's facts and canon's content rule, and is told never to mention alcohol, gambling or children, never to give real crime or weapon instructions, never to produce sexual content.
3. A claim check stops invented plot facts.
4. The player talks only to story characters, never gives free orders to the model.
5. Lines are length-capped; swearing held to the rated level.
6. Players can report a line in the game; reports are logged.
7. An automated run of hostile player lines before each release, results kept.
All must be true in the build first; 6 and 7 may not exist yet [I].

## 3. Store page

- Fee: 100 US dollars per game, paid back once the game earns 1,000 dollars [READ, Steamworks app fee page].
- 30 days between paying and release for a first title [READ, Steamworks onboarding].
- Coming Soon page public at least two weeks before release; store page and build reviews take 1 to 5 days each [READ, onboarding].
- Required images, sizes since Aug 2024, old sizes refused [READ, Steamworks graphical assets]:
  - Header capsule 920 x 430; small 462 x 174; main 1232 x 706; vertical 748 x 896.
  - Screenshots at least 1920 x 1080, 16:9 (at least five [SS]).
  - Library: capsule 600 x 900; hero 3840 x 1240; logo 1280 wide or 720 tall; header 920 x 430.
  - Icons 256 x 256 and 184 x 184; event cover 800 x 450. Optional: background 1438 x 810, event header 1920 x 622. A trailer is advised [I].
- Wishlists: writers often quote 7,000 to 10,000 wishlists at launch as a healthy start [SS, unverified, est.]; no Valve figure read.

## 4. Order of work, rough hours

1. Now: draft the content survey and AI guardrail text against canon (est. 3 h).
2. PEGI 16 as the target, the push-to-18 list as a design rule for fights, menace and talk (est. 2 h; a ruling for Jafar).
3. Build guardrails 6 and 7 into the talk system (est. 8 to 16 h, Town task).
4. When 2026-grade frames exist: pay the 100 dollars (Jafar, money), make capsules and five screenshots from the packaged build (est. 12 h), write the page text (est. 3 h).
5. Coming Soon live as early as frames allow, ideally six months before release [I].
6. Three months before release: decide on a real PEGI for the UK and Swiss markets (est. 2 h plus fee).
7. Trailer from the packaged build (est. 16 h). Release no sooner than 30 days after the fee.

Raises G4 to medium: survey and guardrail drafts written and checked; PEGI 16 rule ruled by Jafar; the PEGI review fee and Swiss industry rules (due end of 2026) read at source; one capsule made at size from a real game frame.

## Unreached today

PEGI or Games Rating Authority review fee; whether Swiss rules name PEGI; Valve's wishlist guidance; the trailer page; whether the UK Act covers pure downloads.
