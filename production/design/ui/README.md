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

## What is not in this folder, and why

The rendered pictures are not committed yet. The repository's attribution check (tools/attribution-check.py) refuses any picture or font file in a folder it does not know, and the list of folders of the project's own pictures lives in that tool's code, which this job was told not to change. The pictures are on Jafar's choice page, and go into this folder once the check knows it (one line in the tool's list of our own folders).

## Step 2, after his pick

The full set in the chosen look, each at 3440 by 1440 and 1920 by 1080, with a short style guide: the title screen (New game, Continue, Quit, and Settings), the pause menu, settings with quality presets, the prompt on people and things you can use, first-time key hints, subtitles with the speaker's name, the typing box, and the loading screen with its progress.
