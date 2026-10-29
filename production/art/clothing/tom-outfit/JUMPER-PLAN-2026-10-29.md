# Tom's plain jumper: the plan (29 October 2026)

His order C9: after the cuffs, the jumper, jeans and shoes by the game-garment skill. Reference first: Mafia's knitted top (production/research/game-clothing-pipeline/MAFIA-SWEATER-2026-10-29.md, "For Tom's jumper") and the September jumper research (production/research/clothing-pipeline/JUMPER-2026-09-30.md, read in full again today).

## The pattern

- **Block:** FreeSewing's Brian (MIT) at Tom's measures, chest ease 10% (the jacket's 15%): F:/LedgerTools/garments/tom/jumper/pattern/brian-jumper.json, drafted 29 October by tools/meshgen/freesewing_draft.mjs. Chest 1,176 mm on his 1,069; the jacket's 1,229. Ease: none found in either game; FreeSewing's own jumper design (Sven) is not installed here, so its default is unverified and nothing was downloaded.
- **Pieces:** a whole front and a whole back, each mirrored about its centre; two one-piece sleeves; a rib welt in two parts (front, back); two rib cuffs; a crew neckband.
- **Neck:** the front neckline lowered from Brian's 61 mm to 80 mm (a crew neck 3 to 4 in deep, 7 to 8.5 in wide [K1]; Brian's opening is 184 mm, 7.2 in); the band 28 mm, folded double [K3].
- **Length:** the welt's lower edge at 0.95 m, just below the belt [K5]: body 535 mm from the shoulder's high point, welt 75 mm (3 in; vintage patterns 3 to 4 in [K4]).
- **Rib:** the welt drawn in 8 to 10% (JUMPER-2026-09-30, the welt); the cuffs 75 mm.

## The route

- **Body and sleeves:** Marvelous's drape on the straight-elbow avatar, as the jacket (skill step 2 and 3): 20 mm particles while building, 10 mm on the body, Fitting last.
- **Rib edges by the built route from the start:** Marvelous's elastic rib was set aside after two tries on the jacket's cuffs (29 October); the cuffs built to the wrist's shape passed every mark (tools/md/build_cuffs.py, which moves only a draped band's points). So the welt (0.90 of the hem), cuffs (the wrist's girth) and neckband (0.92 of the neckline) are draped loosely with the shell, sewn plainly, and then built to the body's shape (DECISIONS, 29 October). The job: tools/md-bridge/jumper.py, nine pieces, 21 seams; the first, F:/LedgerTools/garments/tom/jumper/job_j1.py.
- **Game mesh:** about 19,400 triangles at LOD0, then 42, 23 and 8% (Mafia's sweater 19,406); 2048 textures, about 16 px/cm; the knit as a tiling detail normal, about 7.1 cm a repeat, not baked; folds and seams baked (MAFIA-SWEATER, 1 to 4).
- **Weights:** the body's, as the jacket (skin_garment.py), checked against the September zones (side panel on the spine, the cuff on the lower arm's twist, no hand or wrist joints); 8 influences at LOD0 and LOD1, 4 below.
- **Under the jacket:** the covered parts hidden, as Mafia hides parts by a slot's invisible material; only the neckband and, where the sleeves ride up, the cuffs show (LEDGER's choice, MAFIA-SWEATER 2).

## The checks

Each step's check is the skill's; beside them: the neckband's opening passes his head at the knit's stretch (head 22 in, opening at least 14.5 in at 50% [K2]); the welt holds when he sits (the September fault: a shelf).

## Waiting on

Marvelous reopened (his ruling of 29 October: computer use only in Marvelous, after 10 minutes with no input).
