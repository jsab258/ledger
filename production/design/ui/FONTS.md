# The fonts the interface designs use, and their licences

Every one is under the SIL Open Font Licence 1.1, which is on the project's licence allowlist for fonts (ruled by Jafar on 30 September). The OFL lets a sold game ship the font, whole or cut down, provided its licence text goes with it and the font is never sold on its own; pictures made with it carry no condition.

Checked at source on 1 October 2026 by the design session: the licence field in google/fonts' METADATA.pb, the OFL.txt beside it (copied into fonts/ here, one folder per family), the licence string inside the font file, and that the file has the £ sign. The research behind the choices is production/research/ui-design/PERIOD-PRINT-AND-FONTS.md.

The mockups ask Google Fonts for them, so this folder holds the licences and not the font files: a font file in the repository needs its row in THIRD-PARTY.md and in tools/attribution-check.py first, which is the builder's step when a font goes into the game.

| Font | Used for | Copyright, from its OFL.txt | Reserved Font Name | Source | Files |
|---|---|---|---|---|---|
| Courier Prime | A: the typed entries, the typing box, the keys and the speaker's name tab | Copyright 2015 The Courier Prime Project Authors | none | github.com/google/fonts/tree/main/ofl/courierprime | static |
| Kalam | A: a few ballpoint words only ("Where to?", "to Sheila", the day and time) | Copyright (c) 2014, Indian Type Foundry | none | github.com/google/fonts/tree/main/ofl/kalam | static |
| Old Standard TT | A: the account book's gold title; C: datelines and the italic lines under a choice | Copyright 2011 The Old Standard Project Authors | none | github.com/google/fonts/tree/main/ofl/oldstandardtt | static |
| Marcellus SC | B: the title, as a street name plate (the font the game's own name plates already use) | Copyright 2012 Brian J. Bonislawsky, Astigmatic (AOETI) | Marcellus | github.com/google/fonts/tree/main/ofl/marcellussc; already in production/fonts/marcellus-sc with THIRD-PARTY.md's row | static |
| Work Sans | B: everything read, the nearest free grotesque to the road signs' Transport | Copyright 2019 The Work Sans Project Authors | none | github.com/google/fonts/tree/main/ofl/worksans | variable only |
| PT Sans | A: the subtitles (the standards ask for a plain sans there); the very file the game already ships as LedgerSans.ttf, byte for byte | Copyright (c) 2010, ParaType Ltd. | PT Sans, ParaType | github.com/google/fonts/tree/main/ofl/ptsans; already in THIRD-PARTY.md as the shipped font | static |
| UnifrakturMaguntia | C: the masthead word only | Copyright (c) 2010, j. 'mach' wust, with Reserved Font Name UnifrakturMaguntia; Copyright (c) 2009, Peter Wiegel | UnifrakturMaguntia | github.com/google/fonts/tree/main/ofl/unifrakturmaguntia | static |
| League Gothic | C: the ears, the STOP PRESS band and the coupon's label, never running text | Copyright 2010 The League Gothic Project Authors | none | github.com/google/fonts/tree/main/ofl/leaguegothic | variable only (width) |
| Libre Franklin | C: everything read (the choices set as headlines, the subtitles, the typing box) | Copyright 2020 The Libre Franklin Project Authors | none | github.com/google/fonts/tree/main/ofl/librefranklin | variable only |

- **Variable only** means google/fonts keeps just one variable file for the family. Whether Unreal draws variable fonts properly was not checked; static cuts made from them with fontTools are allowed without renaming, since none of the three has a Reserved Font Name.
- **A Reserved Font Name** (Marcellus, UnifrakturMaguntia, PT Sans) only matters if we change the font: a changed copy must be renamed. Used as it is, nothing changes.
- **Left out on purpose:** Tinos (its folder has no licence file, though its metadata says OFL), and Special Elite and Homemade Apple (Apache 2.0, not on the allowlist).
