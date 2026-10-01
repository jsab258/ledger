# The game's screens: interface design

The interface for LEDGER's menus and talk, designed from the research in production/research/ui-design/ (read SUMMARY.md there first). Third-person, PC, Britain in 1990; the interface belongs to the same world as the Ledger notebook (D37) and the paper map (D20, D36): no minimap, no markers, nothing the player could not know.

## Step 1: three looks, for Jafar to pick one (1 October 2026)

Each look is shown on the same three screens: the title screen, a conversation (Sheila's reply in the subtitles, his next line being typed above it) and the pause menu.

- **A, the fare book** (step1/a-fare-book.html): the cab office's own paperwork. A red account book with a typed label on its cover; azure ledger paper, feint blue rules, a red double margin; entries typed in Courier and sitting on the rules; a few words in ballpoint; the line in hand highlighted. Subtitles in PT Sans, the game's own sans.
- **B, the street's signs** (step1/b-street-signs.html): the street's own signs. The title as a street name plate in the Kindersley capitals of the game's own plates; green direction-sign panels; the chosen line turning primary-route yellow with the sign's arrow; his line on a white plate under a green "Sheila" sign.
- **C, the evening paper** (step1/c-evening-paper.html): a 1990 local evening paper, black and one red. The title as the late final's front page with a halftone of the street; choices as headlines; the pause as a STOP PRESS box; speech as a caption, his line on a reader's coupon.

What they share, from the standards: built at 1080 tall and scaled by height, as Unreal does, so on his 3440 by 1440 screen everything is a third larger; everything to read or act on inside the middle 16:9 of a wide screen; subtitles 39 units (about 48 pixels from the top of an h to the foot of a y on his screen), mixed case, at most two lines under 40 letters, on a dark backing at 80% (to be adjustable), 10% up from the bottom, with the typing box above them and its keys beside it; key hints 30 units in a plain face; the smallest labels 28 units; text contrast 7:1 or better where it matters (measured over a white sky).

The street behind each mockup is the game's own frame of 1 October (production/approvals/2026-10-01), not the concept sheet. The pictures to judge are 2560 by 1440: the interface at its true size on his screen, over the frame at its own full size. The 3440 by 1440 pictures show how it sits on his wide screen; there the frame is enlarged by a third, since no wider game frame exists yet.

The times on the screens follow the light behind them: the title at night says 9.40 pm; the conversation and the pause are by day.

Each look went through my own check against the references and then reviewers who had not seen it made, each round fixing what they found obvious; what they still note goes on Jafar's page beside each look.

## How to draw them

The pages ask Google Fonts for their fonts (FONTS.md lists each, with its licence; the licence texts are in fonts/). Open a page in a browser with `?screen=title`, `?screen=talk` or `?screen=pause`. A window 1920 by 1080 is a 16:9 screen; 2580 by 1080 is his 21:9 screen; draw at 4/3 scale for 1440 tall.

## His answers (1 October 2026, read from the page's store at 13:48)

- **The look: C, the evening paper** (verdicts/ui-direction). Recommended was A; his pick governs. Its reviewers' notes carry into step 2: the masthead word is the game's title, never a newspaper's name used in play; the menus stay mixed case in a plain heavy face; speech stays light on dark.
- **The pictures go into the pull request: yes** (verdicts/ui-pictures-in-repo). One line in tools/attribution-check.py now names this folder as the project's own work; the step-1 pictures are in step1/pictures/, full size (2560 by 1440 and 3440 by 1440), as WebP.
- **The finish: (a)**, in chat: we do it ourselves, with real scanned materials and the game's own renders, and one finished screen is judged against Kingdom Come: Deliverance II before more. It waits for the playable route (his rule of 30 September).
- **Branding**: researched before any start (production/research/ui-design/BRANDING.md).

## Step 2: every screen in the evening paper (1 October 2026)

- **The screens** (step2/evening-paper.html, open with ?screen=...): title, pause, settings with quality presets, the prompt on a person, a first-time key hint, subtitles from someone Tom has no name for, the typing box grown to two lines, loading with its progress. The pictures are in step2/pictures/, at 3440 by 1440 and 1920 by 1080 (WebP, full size).
- **The kit** (step2/kit.html, step2/pictures/kit.webp): every part in every state at true size.
- **The rules**: STYLE-GUIDE.md (type, colour with measured contrast, layout, materials, parts and states, how things appear and disappear, notes for Unreal).
- **Review**: my own check against the standards and the period research, then fresh reviewers who had not seen it made: one full review whose obvious faults were all fixed, and a recheck that found them gone, with two small mismatches fixed after. What they still note is on his page under each screen.
- **Not fixable here**: the game's frames show no Tom, so the in-play screens read as first person. That is the builder's camera, not the interface.
- **His page**: https://claude.ai/artifact/KRReoxSgX8qEfPAebV4JhM (source step2/page/). It asks whether to build the set as drawn (verdicts/ui-set-evening-paper), and whether a trade mark lawyer should check the name LEDGER before anything goes public (verdicts/ui-name-check; recommended: yes, now, with two fallback names; production/research/ui-design/BRANDING.md).

## His answers on step 2 (1 October 2026, in chat; nothing tapped on the page)

- **The set: liked as drawn**, with one thing missing: players who use a controller, or do not want to type, choose from **suggested lines** instead of typing; typing stays. This overrides the research's "no suggested questions"; the suggestions are designed next (research first), and the style guide changes with them.
- **The name: LEDGER stays for now.** No trade mark check yet; it is to be raised again before any Steam page, trailer or announcement (BRANDING.md).

## Next

- **The finish**, under his answer (a): scanned paper, a real halftone screen, sound; one screen finished and judged against Kingdom Come: Deliverance II before the rest. It starts once the playable route works (his rule of 30 September).
- **The branding**, after the name check: positioning, the wordmark, the brand guide, key art and Steam's set, as BRANDING.md lays out.
