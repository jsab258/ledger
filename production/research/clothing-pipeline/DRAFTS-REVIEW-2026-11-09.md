# Review of the two n09-6 drafts (9 November 2026)

Fresh reviewer. Each source opened; F: paths checked with ls only. No file other than this one written.

## 1. PATTERN-LIBRARY-2026-11-09.md: PASS WITH FIXES

Checked and correct: unit-costs JSON hours (zip jacket 6.78, jumper 2.81, jeans 1.61, boots 2.95 with 1.45 set aside, outfit 14.15, at least 9.8 first-of-kind); SCOREBOARD 5.81 (six windows) and 1.96 (Darren alone); RON-MEASURES knit sum 0.35; Tom's measures (chest 1069, waist 885, hips 1042, neck 420) and 109 arrangement points in SPEC.md; garments.json TomJumper text (26 degrees, ease 4%, 8.5 by 4 in, 19,480 triangles); Sheila's handbag, Titan, boots, carry.json and zprj paths exist on F:.

Fixes:
1. Entry 2 names the shipped jumper as "skin-try1/slots-neck/jumper_skinned.fbx". The file exists only under chain-j3d/ (garments/tom/jumper/chain-j3d/skin-try1/slots-neck/). Add the prefix.
2. Entry 1 says the jacket is 13 pieces and 29 seams. SPEC.md's first-drape line says eleven pieces and 25 seams; 13 and 29 come from the later drape 4 line. Cite that line.
3. Entry 2 gives ease 4%, but JUMPER-PLAN says 10% for the first block. The draft should say the 4% is the j3 re-cut, not the plan.
4. Entry 3's hem (419 mm), rises, outseam and inseam could not be traced to JEANS-PLAN lines 9-10 and 26. That plan's text names Charlie's 478 mm hem. The figures probably come from titan-jeans.json, which was not read (a Windows Python call could not open the F: path). Mark them "unverified" or cite the JSON.
5. Hours "about 7.7 R" and RECIPE line numbers (720-734, 1654, 1670, 1931) were not re-opened here. The draft mixes M, I and R in one cell. Keep, but say which is the headline figure.
6. Opening line says commit history is unread, so the "first of its kind" claims rest on records only. Acceptable, and stated.

No period or canon problem found: no brand, no modern item, no alcohol, gambling or children. "Charlie", "Brian" and "Titan" are FreeSewing pattern names (MIT), not clothing brands.

## 2. SHEILA-REFIT-PLAN-2026-11-09.md: PASS WITH FIXES

Checked and correct: casting sheet (beige hand-knitted cardigan, cream blouse, brown pleated skirt, flesh tights, brown lace-ups); skirt sitting set aside after seven tries (skirt-review-standing.md); cardigan details (29 mm band, seven buttons, 5 cm welt, 6 cm cuffs) in sheila/README.md; waist 824 in MH_LenaS4 measurements.json; Hook list "11 out, 38 in"; 2.95 h boots refit as the one measured refit (Hook review item 2); Mafia hem flap bones; the Lena bodies and Sheila garment folders exist on F:; SKILL.md refit lines 99-107 are cited accurately.

Fixes:
1. "Seat 964" is unsupported. The body files and SHEILA-CLOTHES give hips 931 (930.6). Correct it or cite where 964 comes from.
2. "Mafia: about 20 flap joints, 12 at the hem": the source says about 20 flap bones carry weight and 12 carry more than 1% at the lowest 3 cm, and its physics asset has 18 flap bones. The plan's "12 at the hem" is loose. Reword to "12 above 1% in the lowest 3 cm".
3. Age 53 and height about 1.50 m could not be matched to a line in SHEILA-CLOTHES in this pass. Give the line.
4. Step 1 and step 3 use "Shown/Hidden" slots as for Tom's jumper. That fits the skill's step 9 and the refit section.

Contradictions with SKILL.md: none outright. The plan follows the refit order (body the game builds, game file, carry, clear_layers --over, head, neckband, skinning step 9), the held row, import into mh-assemble only, garments_shipped_check, -WearHeld, and the hold/released rule. Two cautions. (a) Step 3's alternative, "re-drape in Marvelous", must follow SKILL.md step 2 (full body with neck, drape in the order worn: blouse and skirt under the cardigan, proxy not detailed mesh); the plan says "per the skill's steps 2 to 4" and that is enough. (b) The plan says new routes for skirt or cardigan may need his yes; this agrees with the two-tries rule, and the plan correctly lists it as an open question.

Total check: steps 0 to 7 add to 15.3 h, the stated "about 15 h"; without steps 4 to 6 (3.8 h) it is 11.5 h, not the stated 12.5. Fix the figure.

Period and canon: no brand, no modern cut, tights and cardigan right for 1990. Clean.
