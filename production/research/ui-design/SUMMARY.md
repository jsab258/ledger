# The game's screens: what the research says, in short

1 October 2026. Two research helpers, each given the problem and about thirty minutes, with dated sources; the full notes are beside this one. Most game-industry and standards sites were blocked by the session's network that day, so many figures are from search summaries, and each note marks which.

## How game teams make an interface (PIPELINE-AND-STANDARDS.md)

- The same order everywhere: list every screen and what the player needs on it; how the screens connect; grey layouts; a style guide; mockups painted over real game frames at every screen shape; a playable prototype; a kit of parts with every state (normal, chosen, pressed, greyed out); how things appear and disappear; then building it in Unreal (CommonUI) and testing it by measuring text in screenshots.
- Kingdom Come: Deliverance II draws its menus as a manuscript and its maps by hand, and in its hardest mode removes the compass, the markers and the player's own position on the map. Red Dead Redemption 2 keeps period lettering for titles and plain type for anything read, and lets each part of the screen be off, shown only when needed, or always on.
- Faults of both to avoid: KCD2's interface does not grow on big screens and spreads to the edges of a wide screen, so players modded it back into the middle; RDR2's subtitles were small, with no size setting.
- Unreal sizes an interface by the screen's height: built once at 1920 by 1080, it is a third larger on Jafar's 3440 by 1440 screen. Anything to read or act on stays in the middle 16:9 of a wide screen.
- Subtitles: on by default; at most about 40 letters a line and two lines; the speaker's name when the speaker changes; a dark backing whose strength the player sets; a plain sans-serif among the choices; several sizes. A default of 36 at 1080 (48 on his screen) is the helper's own figure from viewing distance, not a published standard; the television figure is 46.
- Text at least 4.5 times brighter or darker than its backing, 7 times for subtitles where possible; measured over the worst frame (a white sky, a lamp, headlights).

## What 1990 British print looked like (PERIOD-PRINT-AND-FONTS.md)

- Road signs in Transport (Kinneir and Calvert), British Rail in Rail Alphabet, street name plates often in Kindersley capitals, Ordnance Survey maps in Univers and Times. None of these is free; the nearest free faces are named.
- Office paper of 1990 was typed on daisy-wheel machines in Courier or Prestige Elite; account books had pale blue lines and red money columns; police notebooks ruled off every entry.
- Local evening papers were black and white with one spot colour; contents bills outside newsagents sold the evening edition.
- Buses after deregulation in 1986: faded National Bus Company red or green beside new local colours.
- Not found: police appeal boards in 1990, the faces of 1990 local mastheads, the A to Z's road colours of the time.

## Fonts

- Every font the designs use is under the SIL Open Font Licence, checked again at source on 1 October (licence field, licence file, the licence inside the font, the £ sign). Their licence texts are in production/design/ui/fonts/, and the record in production/design/ui/FONTS.md.
- Special Elite and Homemade Apple are Apache 2.0, not on the allowlist. Tinos has no licence file in its folder, so it is not used. No free version of Transport, Rail Alphabet, Gill Sans or Univers exists; buying one would be a decision for Jafar.

## Settled by earlier rulings, so not asked

- Names over subtitles: a person's name only once Tom has learned it, and until then the street's description of them ("the man at the bus stop"), since the interface shows only what he knows (D12: the Ledger is his own memory). The helper suggested asking Jafar; under D12 it needs no question, and the designs follow it.
- No markers on the paper map, and no minimap (D20, D36).
