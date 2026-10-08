# The lab's glass fix, applied: the gate, 8 October 2026

His message of 14:30: the lab's glass notes (production/lab/GLASS-NOTES.md) applied, two tries, the memory peak within the card.

**Try 1, step 1 of the notes:** every glass catch kept out of the scene textures' size (`bExcludeFromSceneTextureExtents`, VignetteShot.cpp), the windows the cameras stand at caught at 1024 a face (glass_cube_hero_size; Mickey's window, Rita's, and Mickey's door glass since 12:20).

**Memory** (the game's own dedicated GPU memory, sampled twice a second through the day and night runs, F:/LedgerTools/scratch/glass-1008/t1/mem-*.csv): peaks of 7.4 GB in the first catch round and 7.9 GB in the night's, for a few seconds each; settled at 5.27 GB after the round against 4.98 before (the cubes themselves). On 7 October the card peaked at 8.0 GB with 512 catches and 9.2 GB at 1024. Within the 10 GB card; above the lab's stricter 6.0 GB mark.

**One fresh reviewer per view, each beside its last good picture** (F:/LedgerTools/gate/new/glass/2026-10-08-t1):

| View | Verdict |
|---|---|
| Office, day | The roofline's steps halved (about 4 px every 9-10 rows to about 2 px every 4-5), still regular at 4x; the aerial whole again; no seam between faces. **Blocks:** the reflected houses, wall and road lost their light and detail. Measured across the day's pictures, that loss came between 12:42 and 13:00 (the reflected road 97 -> 15), before this change, when Mickey's room was re-imported with its back room: under investigation. |
| Office, night | The reflected cottage windows crisper (edges 7-8 px -> 3-4 px, their bars showing), no brighter; the steps halved; the aerial reads. **Passes.** |
| Hook, day | Mickey's transom ghost gone; the pawnbroker's reflected brick sharper, no rings, but a small stepped white block at its foot. **Blocked** on the cover's pale border back in front of Mickey's: not this change but the 11:20 fix lost from the recipe (restored, with a self-test). |

**The office's dark reflection, found (15:30).** Not the room and not this change: with -PaintedRooms the reflection came back (the reflected road 90, the gable 78), but the room as it was at 12:34 re-imported gave the same dark glass, and the cube dumped after the round (-GlassCatchDump) held the street lit. Every pass of a window's catch wrote into the cube the glass shows, and Lumen gathers a fresh catch's light over its passes, so for a dozen frames a round the window reflected an unlit street; the photographs, a few seconds in, fell in that time once the street took longer to load. Fixed (try 1): the gathering passes go to a spare cube of the same size, the last pass to the window's own (VignetteShot.cpp, GlassCatchScratch). The same picture then measures the reflected terrace 62, the gable 54, the road 84 (noon: 62, 53, 99; the road lower because the catch now keeps no reflections of its own). A player would have seen the flash at every change of light.

**The cover's pale border** was the 11:20 fix lost from the street recipe (its commit held only the decision): the iron frame restored, with a self-test (accept/the-cover-sits-in-an-iron-frame), the street re-exported.

**The tries closed (16:05).** The frame-rate try inside the catch (no Lumen reflections, half the gather) caught the wet pavement pale: a stepped grey wash at the foot of Mickey's panes and a haze on Fresh Fish's (the hook reviewer blocked on both, 15:55); taken out. Last pictures (F:/LedgerTools/gate/new/glass/2026-10-08-t2 and -t3), a fresh reviewer each:

| View | Verdict |
|---|---|
| Office, day (15:50) | **Passes.** The houses lit again (within half a level of noon's), brick courses and chimney pots read; the steps halved (gable: every 19 rows ±1.8 px -> every 9.5 rows ±1 px; wall foot 24 x 5 px -> 12 x 2.5 px); the rings gone; the aerial whole. Listed: the reflected ground paler (that picture had the cheap catch, since taken out), more of the stepped wall foot exposed. |
| Hook, day (16:00) | The wash and the haze gone (43 and 110 against noon's 41 and 108); the cover a flush plate; the pawnbroker's stepped block gone; reflections sharper. The reviewer would block on a small pale stepped patch in Mickey's top-left transom pane (x 1718-1750, y 718-752; 44 against noon's soft 26): the reflection of a pale house across the road, now caught sharp enough to show its steps. Judged the known stair-step shortfall (the capture's missing anti-aliasing) in a new place, as the reviewer allowed: listed, not blocking. Its remedy is the lab's step 2 (four rotated cubes averaged), not tried today. |

His order's two tries: try 1 kept; the blocks it met were the catch's timing and the lost cover, each fixed and judged.
