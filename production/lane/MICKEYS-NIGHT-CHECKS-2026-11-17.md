# Mickey's front at night: checks on the target's unverified points (17 Nov 2026)

## Review fixes (fresh review PASS WITH FIXES, 17 Nov; reviews/REVIEW-MICKEYS-NIGHT-CHECKS-2026-11-17.md). Read this first; it overrides the text below.

- The window-to-pavement ratio is redone on BS 5489's 3.5 to 10 lux (not EN 13201's): about 3.6 to 5.2 stops for a 6 cd/m2 window (reviewer's figure; it depends on the pavement's reflectance). The "at least 2 stops" aim still holds.
- BS 5489-3:1992 is the nearest standard found, not a 1990 one; its figures are second-hand through Fotios 2020.
- Novak's 50 cd/m2 is an upper bound for advertisements, not a shop-window figure; Novak was read through the fetch tool's summary.
- The fascia's 0.085 is brighter than the cited paints, not "in range".
- The small sign lamp matches modern minicab fronts; 1990 is not checked.
- Float glass 91% through and 8% reflected at 4 mm: usual values, not confirmed from the datasheet's text.

1. Of the target's 13 unverified points, research settled 1 (the lit window and shop window brightness), corrected 2, and partly checked 2; the other 8 need the PC or are judgement calls.
2. The target does not repeat the light-weather mistake about how a spot light spreads its light; one ratio in its table is too narrow (corrected below).
3. Plain shop glass lets through about 91% of the light, so the glass is not why the window is dark; a lit room behind it is.
4. A minicab office front is a harshly lit room behind plain glass, with a backlit sign or flashing orange lamp; a small sign lamp (try 2) fits, but no dated 1990 photograph was found.

## Table

| Point | Verdict | Value | Source |
|---|---|---|---|
| Novak 2025, lit windows 6, shop windows 50 cd/m2 | confirmed, with a note | 6 cd/m2 a lit flat window; 50 cd/m2 is advertisements including shop windows, not shop windows alone | [1] |
| EN 13201's 2 to 15 lux | corrected | EN 13201 is a 2003 standard, not 1990. For 1990 use BS 5489-3:1992: average 3.5 to 10 lux, minimum 1 to 5 | [2], second hand; standard text unreached |
| BS 5489 values for 1990 | stays unverified (value carried) | as above; the 1989 edition not reached | [2] |
| Pool to gap 3.0 to 5.2 stops | stays unverified | PC: pool to gap in the hook night view | none |
| Aim A's 40% and 60 of 255 | stays unverified | judgement; PC: the 8 Oct frame's front box as floor | none |
| Aim C's footway 10 to 30 | stays unverified | PC: footway median in the hook night frame | none |
| Aim C's spill bound | stays unverified | PC: Rita's and the fish shop's spill boxes in the same hook frame | none |
| Period paint albedo | partly checked | modern navy LRV 3.85, near-black 5; the fascia's 0.085 is in range, if anything bright; no 1990 paint read | [3], [4] |
| 1990 cab office door lamp or sign | partly checked | modern fronts: flashing orange beacon, backlit sign, harshly lit room, glass screen, fares on the glass; undated | [5] |
| Room's 8 Oct box mean | stays unverified | PC: measure the 8 Oct cam_mickeys night picture | none |
| The channel split | stays unverified | PC: read VignetteShot.cpp | none |
| The inner office's own dark key | corrected | none exists: the only dark key is on the street door; the inner office needs a new key | repo, read 17 Nov |
| Mickey's window middle for shop_views.py | stays unverified | PC: read shop_views.py | none |

Extra values the brief asked for:

| Point | Verdict | Value | Source |
|---|---|---|---|
| Clear float glass | confirmed | 4 mm: 91% through, 8% reflected; 6 mm: 90%, 8% | [6] (2018; 1990 judged same) |
| 58 W 5 ft tube | partly checked | modern triphosphor 3500 K: 5,200 to 5,240 lm. 1990 halophosphate White 3500 K: not reached, likely lower | [7]; UK White 3500 K preference from the light-weather file |

## Notes

- Spot light check. The target's sums never spread a spot light's lumens over a sphere. The 500 to 167 lm cut is 1.58 stops whatever the cone, since the cone did not change, so "about 1.6 stops" holds. Mafia's 0.25 to 0.5 cd is used only as a ratio. Before try 1, read how Unreal spreads a rect light's 60 lm (the spill light); not read here.
- The ratio in section 3 is too narrow. Lit window 6 over a lit pavement of 0.1 to 0.7 cd/m2 is 9 to 60 times; 50 cd/m2 over the same is 70 to 500 times. So the real range is about 3.1 to 9 stops, not 3.3 to 6.6. Aim B's "at least 2 stops" still holds; the top end can be higher.
- Minicab front: [5] backs a harshly lit front room and backlit or flashing signs. It is modern and London.

## Sources (read 17 Nov 2026)

1. Novak et al., CIE 2025 Midterm, files.cie.co.at/x051_2025/P0796_ID298TomasNovak_OA_with_cover.pdf.
2. LIGHT-WEATHER-VALUES-2026-11-17.md source [11].
3. benjaminmoore.com.es/en/colors/2065-10 (Admiral Blue, LRV 3.85).
4. secure.resene.com light reflectance values page (black 0, Nero 5).
5. ribaj.com/intelligence/mini-cab-offices, Holland and Ward, undated.
6. Scheuten Float datasheet, January 2018, scheuten.com.
7. Whitecroft Lighting lamp data PDF, whitecroftlighting.com.

Unreached: BS 5489 and EN 13201 texts; any dated 1990 photograph of a British minicab front at night; a 1990 halophosphate tube catalogue.
