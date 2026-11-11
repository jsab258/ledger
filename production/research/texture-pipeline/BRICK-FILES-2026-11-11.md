# Brick files in the packaged game, 11 November 2026

Read only. VignetteShot.cpp = ue-probe/Source/LedgerProbe/Private/VignetteShot.cpp (VS). Packaged root = F:\LedgerTools\played-game\Windows\LedgerProbe\Content\LedgerData (LD); the game's repo root is the sidecar's ../../.. (VS:2079).

## (a) The street's red brick
- Rows: quay-street.json has 8 rows on brick_red, each with surface_map brick_red, tile_m 0.55 and drawn_map production/assets/street/surfaces/brick_red, drawn tile 7.0875 x 7.2 m (quay-street.json:505-529; bay rows carry a house_tint, e.g. h_east_parade_bay0).
- First bind (VS:7488-7511): the drawn map wins, LD/production/assets/street/surfaces/brick_red.png, brick_red_n.png, brick_red_r.png (suffixes SurfaceBind.h:62-66). Tiled 1/7.0875 by 1/7.2 (VS:7562-7563). The photo path (CityPack/textures brick_red.jpg, _n, _r, tile 0.55) is the fallback only (VS:7512-7533, 7561).
- Scan overlay replaces all three (VS:8788-8805, 8860-8863), since brick_red's scan entry has "always": true (ps5-corner.json:348-362). Files: LD/production/assets/scanned/polyhaven/brick_4/brick_4_diff_2k.jpg (2048 sq, RGB, 1.3 MB), brick_4_nor_dx_2k.jpg (2048, RGB), brick_4_rough_2k.jpg (2048, grey) (ps5-corner.json:350-354; sizes read from the files). The scan covers 1.05 m (ps5-corner.json:355), so tiling 1/1.05 (VS:8805, 8864-8865).
- So the colour on screen is brick_4 at 1.05 m, not the drawn map.
- Colour grade (VS:8806-8809): match_rgb 0.479, 0.298, 0.314 (ps5-corner.json:356-360) x look-file surface gain x house tint. Colours are sRGB for map 0, linear for the others (VS:8798, 6191).
- Layers on top:
  - Per-brick tones: brick_4_ids.png (2048, RGBA, nearest), tones 0.585/1.019/1.348, hue 1.9249/0.7844/0.4123 (ps5-corner.json:364-375; VS:8811-8845). -NoBrickTones (VS:8813).
  - Streaks: BrickStreakFor, brick_red and brick_grey only (VS:7364, 7583). -NoBrickStreaks (VS:7363).
  - Wall macro 0.08 at scale 0.0025 (ps5-corner.json:377-378; VS:8848-8852). -NoWallMacro (VS:8848).
  - Wet and wear tints: AlbedoGrade, wetness and a water level via TakesWater (VS:8700-8716).

## (b) The TomWalkProof course
- The course is a timed route of Tom's own headings, not a fixed place (SliceCharacter.cpp:925-936). He starts where he stands in the live street (tools/walk_run.sh:9) and takes the clearest heading (SliceCharacter.cpp:1010-1019). -TomWalkProofFrom and -TomWalkProofYaw may place him (SliceCharacter.cpp:1001-1019).
- The wall there is unread. The code names no wall, and the trace only logs the actor name it hits (SliceCharacter.cpp:1340-1352). Which row it is stays unread until a run's ledgerTomMove "wall" line names it.
- If the wall is a Quay Street house row, (a) applies unchanged.

## One run with a 1.35 m candidate, no C++
1. Swap, with names kept: brick_4_diff_2k.jpg, brick_4_nor_dx_2k.jpg and brick_4_rough_2k.jpg in LD/production/assets/scanned/polyhaven/brick_4/. The loader detects the format from the bytes, not the suffix (VS:6149), and takes any size (VS:6182), so 2048 px works. The roughness file can be 8-bit grey (VS:6164). The normal must be DirectX, as brick_4_nor_dx is. Mips: CreateTransient makes none, so a far wall will shimmer (VS:6182; same for brick_4 today).
2. Tiling: edit covers_m 1.05 to 1.35 in ps5-corner.json:355, which is data. Without it the candidate prints at 1.05 m and the tile is wrong by 29%.
3. Grade: edit match_rgb (ps5-corner.json:356-360) to 1, 1, 1, or the candidate is multiplied by brick_4's grade and the colour is wrong. Surface gain and house tint still apply, as they do to today's picture (VS:8806-8809).
4. Fair switches: -NoBrickTones and -NoWallMacro. -NoBrickStreaks too if streaks are not wanted. Without -NoBrickTones the brick_4_ids.png map (laid on the scan's own bricks) tints the new bricks at the wrong places (VS:8836-8841). Run today's brick with the same switches.
5. The file swap is in the packaged copy, which the build machine is building now, so it is not done here.

Without code, the real limit is that the candidate's mortar and bond must fit one metre-scale tile; the tones map cannot be re-bound. The smallest code change would be a per-entry "ids" of nothing, or a parameter for covers_m. Neither is needed, since the json edits and -NoBrickTones cover it.
