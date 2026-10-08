# Wet road reflecting the sky: sources (8 Oct 2026)

D read at source today; S search summary only; I my calculation.

| Angle above road | Reflectance or coefficient | Condition | Source | |
|---|---|---|---|---|
| 3° | 0.722 | smooth water (puddle, film over the stone tops) | Fresnel, n 1.333, unpolarised | I |
| 5° | 0.584 | same | Fresnel | I |
| 10° | 0.348 | same | Fresnel | I |
| 15° | 0.212 | same | Fresnel | I |
| 20° | 0.134 | same | Fresnel | I |
| 1° (CIE observer) | Q0 W1 0.11, W2 0.15, W3 0.20 or 0.21, W4 0.25 | standard wet classes, lamp light | AGi32 [2], after CIE 47 [1] | D |
| 1° | W-class S1 limits conflicting (W3 26.5–73, W4 73–200 on an S1′ scale; elsewhere W1 < 4.5) | wet classes | search summaries | S |
| 1° | dry R1–R4: Q0 0.10/0.07/0.07/0.08, S1 0.25/0.58/1.11/1.55; Finnish asphalt Q0 0.093, S1 0.80 | dry, for comparison | Ekrias [3] | D |
| 1° | flooded: S1 ≈ 0; drying: r(0,2) over 12× dry (rough asphalt), 7× (concrete), 3× (fine asphalt) | lab cores, flooded then drying | Pattanapakdee [4] | D |
| 1°–10° | S1, Q0, Qd fall as observation angle rises | dry, 18 pavements | Muzet [5], abstract | D |
| 3°–13° | camera BRDF fits, damp vs dry classified; no reflectance figures | damp, daylight | Roser [6] | D |
| diffuse part | albedo about halves when wet: sand 0.182 to 0.091, black mould 0.141 to 0.084 | wet rough ground | Lekner [7], citing Ångström | D |

## What it means

- No measured wet-asphalt reflectance in the sky-mirror geometry at 3–20° was reached. CIE tables fix the observer at 1° and light the road from overhead lamps; their mirror direction never meets the viewer, so a flooded sample reads S1 ≈ 0 [4]. They cannot give sky reflectance per angle.
- Fresnel is the ceiling: a puddle, or a film drowning the stone tops. A real wet road mixes: film fraction f mirrors at Fresnel, stone tops scatter diffusely, darker than dry (about half, [7]). Target ≈ f × Fresnel(angle) + (1 − f) × wet diffuse reflectance (I). No source reached measures f.
- Overcast skylight is near unpolarised, so the unpolarised figures apply.

## Sources

1. CIE 47:1979, Road lighting for wet conditions. https://cie.co.at/publications/road-lighting-wet-conditions (catalogue page only).
2. AGi32 documentation, Pavement surfaces and R-tables pages. https://docs.agi32.com/AGi32/Content/tools/Pavement_surfaces.htm
3. Ekrias A. Road Surface Reflection Properties. Finnish Transport Infrastructure Agency, 2019. https://nmfv.dk/wp-content/uploads/2020/11/Road-Surface-Reflection-Properties-Research-Reports-of-the-Finnish-Transport-Infrastructure-Agency-May-2019.pdf
4. Pattanapakdee K, Chotigo S. Experimental investigation of pavement light reflection characteristics in wet conditions. CIE x046:2019, 1790–1795. https://files.cie.co.at/x046_2019/x046-PO187.pdf
5. Muzet V, Balcer O, Bourges R, Stresser A. Field characterisation of road surfaces reflection properties for several observation angles with a portable measuring device. Lighting Res. Technol., doi:10.1177/14771535261452156.
6. Roser M, Lenz P. Camera-based bidirectional reflectance measurement for road surface reflectivity classification. IEEE Intelligent Vehicles Symposium 2010. https://www.mrt.kit.edu/z/publ/download/Roser_al2010iv.pdf
7. Lekner J, Dorf MC. Why some things are darker when wet. Applied Optics 27(7), 1278–1280, 1988. https://www.wgtn.ac.nz/scps/staff/pdf/darkerwhenwet.pdf

## Unreached (not evidence)

CIE 47, CIE 144, CIE 66 and EN 13201-3 full texts (W-class S1 limits, wet r-tables); Frederiksen and Sørensen 1976, Lighting Res. Technol. 8(4) (abstract only); Muzet's wet on-site work (blocked); Ekrias's Aalto thesis, Sustainability 15:2826 and the INRIM photometry review (all 403); SWOV R-83-52 (bot wall). No study of wet-road luminance relative to overcast sky luminance was found.
