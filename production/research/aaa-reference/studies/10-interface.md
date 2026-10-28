# Study 10: Interface (28 October 2026)

What Mafia: The Old Country and Kingdom Come: Deliverance II show, when they hide it and how they size it, from their own files and public pages for play, beside LEDGER's evening paper (style guide and code). Our own words and numbers; raw notes on F:/LedgerTools/aaa-study (mafia/study-9-10-13, kcd2/study-9-10-13, public/study-9-10-13-sources.md, Study 2's HUD tables); read 28 October 2026. Tags: **M** measured, **R** read, **I** inferred, **N** a name only. A "unit" is a pixel on a 1080-tall screen: Mafia and LEDGER both lay out at 1080 tall and scale by height.

**The short answer.** Mafia hides weapons, items and health while calm, and keeps objectives on by default. 17 HUD parts each have a switch. Its subtitles are small: about 21 units by default, in three sizes, five colours and three backings. A setting pins the HUD to the screen's corners or holds it near the centre.

Kingdom Come II keeps a compass and bars on (adaptive since patch 1.4) and gives street chatter subtitles their own switch.

LEDGER already shows less than either, with subtitles nearly twice Mafia's size. The changes are small:
- a width and scale choice;
- switches for prompts, hints and chatter;
- prompts chosen by facing;
- shake under Reduce motion.

## The numbers

| | Mafia | Kingdom Come II | LEDGER |
|---|---|---|---|
| Subtitle size | 26 × 0.8 / 1.0 / 1.2; default ≈ 21 (R; the scale's use, I) | Small, Classic, Large, Extra large (R) | 34 / 39 / 46 / 54; default 39 (R) |
| On his 3440×1440 | about 28 px (I) | | about 52 px (I) |
| Subtitle place | centre 51% of the width, 60 up; split past 120 characters (R) | | last line 104 up; two lines at most (R) |
| Backing | off (default), 50%, 100% (R) | on or off (R) | 80%, 0 to 100% (R) |
| Colour | yellow default, 4 more (R) | none found (N) | one (R) |
| Chatter subtitles | own channel (N) | own switch (R) | with the talk (R) |
| Subtitle timing | in 0.2 s after 0.2 s; out 0.2 s after 1.0 s (R) | | in at once; out 150 ms, held ≥ 1 s (R) |
| Reading text | body and prompts 20; titles 48 (R) | not in data | key hints 30; choices 48 to 50; nothing read under 24 (R) |
| Typefaces | Clarika Pro Grotesque; two display faces for titles (R) | 7 families, "Kingdom Come" and "Warhorse Manuscript" among them (R) | Libre Franklin, League Gothic, Old Standard TT, UnifrakturMaguntia (R) |
| HUD parts | 17 presenters; 17 switches (R, M) | 27 UI elements; HUD 70 clips (M) | prompt, wait hint, first-time hint, subtitles, typing box (R) |
| Wide screens | corners or fixed; safe zone 80 to 100%; HUD scale 0.8 / 1 / 1.2 (R) | none in data (M) | centred 16:9; width option "later" (R) |
| Settings | 122 in 14 groups (10 ungrouped), 12 under accessibility (M) | 88 buttons on 18 pages (M) | 22 lines on 4 tabs (M) |

## What shows, and when it hides

- **Mafia** (R, decoded from each presenter's excluded states and visibility flags):
  - weapons, items and health may hide only in calm, and stay for an alert, a fight or trespass;
  - objectives are Always On by default; on Automatic they show 30 s (text) and 5 s (marker) when they change; on Manual, only on a "ping" key;
  - prompts hide in cutscenes, dialogue, duels, menus and loading;
  - subtitles hide only while loading;
  - the story grants the HUD piece by piece, from all hidden in the prologue to the map by chapter 2 (Study 2).
- **Kingdom Come II, before patch 1.4:** compass and bottom bars always on, key prompts bottom right, hints top left (R, public: a UI designer's teardown, 8 July 2025). Patch 1.4 (9 September 2025) added an adaptive option. Hardcore strips the compass's letters and the player's map marker (R, menu text).

## Prompts and map

- **Mafia** has two kinds of prompt (R, layout file): an icon drawn on the object at its screen position, and a short list low at the left for actions with no object. Its target is scored ahead of the player and inside the view (Study 9). A review places button prompts lower right and finds them hard to read on light ground (Can I Play That?, 29 August 2025).
- **Kingdom Come II** prompts for what sits at the screen's centre (I), with 146 verb strings (M). A held key guards irreversible acts (R, public).
- **LEDGER** draws one prompt beside the person's head, joined by a short line, only with a clear line of sight. The style guide's "facing it" is not in the code.
- **Maps:**
  - Mafia: a full map, no minimap, road signs that point the way (switchable);
  - Kingdom Come II: a map with fog of war (2,601 cloud pieces) and a compass (R, M);
  - LEDGER: none ("nothing he could not know").

## Menus, settings and sizes

- **Mafia** keeps 122 settings in four typed tables, each row a default, range, step, help text and group (M); a photosensitivity page shows at first start (N). **Kingdom Come II:** only crosshair, tutorials, subtitles and Tobii's clean screen touch the HUD (R). **LEDGER:** 22 lines (picture 10, sound 4, controls 2, subtitles and reading 6), each explained in a sentence, as Mafia's are.
- **1920×1080 against 3440×1440:**
  - Mafia scales by height from 1080 (R), so on his screen every unit is drawn 1.33 times. The extra 21:9 width is spread to the edges ("corners") or the HUD is held near the centre ("fixed").
  - LEDGER scales the same way and keeps all reading in the centre 1920 units.
  - At 1080, subtitles: Mafia 21 by default and 31 at the largest; LEDGER 39 and 54. Prompts: Mafia 20, LEDGER 30.
  - A review found Mafia's subtitles may still be small for low vision (Thumb Culture, 19 August 2025).

## Accessibility

- **Mafia** (R): subtitle size, backing, colour and speaker; HUD scale; three colour-blind modes for the interface only; simplified struggle; swap sticks; sprint hold or toggle; camera shake; damage effects; hints.
- **Kingdom Come II** (R): subtitle size, backing, speaker name, chatter; motion blur; near depth of field; dead zone; hardcore.
- **LEDGER:** subtitles, size, backing, speaker, Reduce motion, suggested lines, look speed, invert; no meaning rests on colour.

## Side by side: what to change

| Part | Mafia | Kingdom Come II | LEDGER | Change |
|---|---|---|---|---|
| Screen width | corners or fixed, safe zone 80 to 100% | none | centred 16:9 | Adopt, on his page: the planned "Interface width" as these two choices, with a 0.8 / 1 / 1.2 scale |
| Prompts | scored, icon on the object | screen centre | nearest, by the head | Adapt: by facing (Study 9); a prompts switch |
| Hints | switch | switch | until done | Adopt: a first-time hints switch |
| Chatter | own channel | own switch | with the talk | Adopt: a street-chatter subtitle switch |
| Subtitles | 21, 3 sizes, 3 backings | 4 sizes, on/off | 39, 4 sizes, 0 to 100% | Keep |
| Subtitle colour | 5 | none found | one | Ignore: one paper, one red |
| Subtitle fade-in | 0.2 s after 0.2 s | | at once | Keep: in step with the voice |
| Calm HUD | weapons and health hidden; objectives on | compass on | nothing | Keep |
| Map | map, signs | map, fog, compass | none | Keep |
| Camera shake | switch | none found | none yet | Adopt: under Reduce motion once Tom's camera shakes |
| Photosensitivity | page at first start | | none | Adapt: one line on the first page, only if something flashes |

## For LEDGER

1. **Adopt, through his page:** the width and scale choice, which changes every screen on his monitor; it serves the friends' build, and the guide plans it "later".
2. **Adopt:** the three switches for the friends' build: small additions to existing screens, not new systems (29 September ruling).
3. **Adapt** prompts by facing (the FINDINGS fault "T opens the talk with whoever is nearest"); **adopt** shake under Reduce motion; **adapt** a photosensitivity line only if something flashes.
4. **Ignore:** markers, timers and a map (nothing he could not know), subtitle colours and colour-blind modes (no meaning rests on colour), aim assist (not a shooter).
5. **Keep the sizes:** larger than Mafia's, whose small default its critics named; Kingdom Come II's are not in its data.

## Coverage map

Tick "Interface and menus": both games, 28 October (Study 10; first appearances already by Study 2). Tick "Difficulty", its settings side only.

## Open blind spots

- Font sizes as played, and all of Kingdom Come II's sizes: its Scaleform files are not unpacked.
- What Kingdom Come II's adaptive option hides, and hardcore's full list: the public sources disagree.
- Mafia's prompt position in play: left in the layout, lower right in a review.
- Either game at 21:9 in play: no recordings.

## Sources (read 28 October 2026)

- Mafia's settings and string tables, 90 layout files (read as text on F:), presenters, Study 2's HUD tables, DefaultGame.ini, the mappings' enums; Kingdom Come II's Libs/UI and menu text.
- Public: PCGamingWiki; 2K's notes; Can I Play That? (29 August 2025); Thumb Culture (19 August 2025); DTF.ru (8 July 2025); patch 1.4 (9 September 2025); Plaion (15 April 2025).
- LEDGER: STYLE-GUIDE.md, LedgerPaper.h, LedgerSettings.cpp, CrimeProbe.cpp, FINDINGS.md.

## Review

The same fresh reviewer (28 October): pass with fixes, all applied: 17 presenters, colour-blind modes for the interface only, the calm HUD, Kingdom Come II's prompt and colour hedged, sizes compared with Mafia's only, the width choice routed to his page, one font name replaced by a description. Cost: within Study 9's.
