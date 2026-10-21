# Target for test 6: Ron's plain 1990 clothes as a pattern a cloth simulator can sew

8 October 2026, branch lab. Amends test 4's target (../../4-plain-clothes/target/, rules O1-O14, corrections C1-C7) with what the fresh reviewer found missing (../../4-plain-clothes/REVIEW.md). The garments will be sewn and draped in Marvelous Designer from flat pieces, so the target is now the **pattern** (pattern_md.json); the outline (target_md.json) is the check afterwards.

## Files

| File | What |
|---|---|
| draft_md.py | Derives the pieces from test 4's pattern.json plus A1-A12. Reruns test 4's Thornton draft through its own functions with the amended hem. Writes pattern_md.json. |
| pattern_md.json | 17 flat pieces in cm (x right, y up, outlines counter-clockwise), grain lines, fabrics, cut counts, internal lines, and 51 seams as pairs of point-index lists in sewing order. |
| self_check_md.py | The self-check; writes its result into pattern_md.json under "self_check". |
| target_outline_md.py, target_md.json | The outline and covered points, by test 4's own target_outline.py with the amended globals. Masks are in F:/LedgerTools/lab/clothes/target_md. |

Photographs (PHOTOS.md in test 4): **P1** = photo 01, Tampere 1988, the heavy man at right, full length. This is the only real match on cut, but its jumper is patterned. **P2** = photo 02, a grey V-neck, about 1989, hips up. **P3** = photo 03, 2024, a plain crew neck, used for cut only. Each was looked at full size today. P1 was also cropped at full resolution at the shoulders, the waist and the hem.

Kinds: **Read** = taken from a source. **Scaled** = measured on a photograph and scaled. **Derived** = computed from Ron's mesh or other numbers. **Photo** = what a photograph shows, with the amount judged. **Judgement** = no source.

## Ron's arm, measured today

ron_parts.npz, left arm. Each girth is a tape round the plane section square to the arm's axis, measured from the shoulder point (test 4's axis: shoulder point, shoulder joint, elbow, wrist).

| Biceps (fullest, s 0.12 m) | Elbow (s 0.388) | Forearm (fullest 4-12 cm below the elbow, s 0.428) | Wrist (s 0.62) |
|---|---|---|---|
| 40.0 cm | 36.6 | 34.5 | 20.9 |

Test 4 used the json's 44.2 cm for the biceps, a different measure. These mesh girths are what the self-check uses.

## Amendments

| # | Amendment | Numbers | Kind and source |
|---|---|---|---|
| **A1** | **Sleeve ease.** The sleeve stands off the arm along its whole length. Test 4 tapered it straight from 51.8 to 26 cm, which left about 1 cm of ease at the elbow and 3 mm on the forearm. | Ease (finished minus Ron): **biceps 12.0 cm, elbow 10.0, forearm 9.0**. Sleeve widths 52.0 / 46.6 / 43.5 cm. Stand-off about 19 / 16 / 14 mm. | **Photo** (P1, P2, P3: soft folds, no muscle shows, the sleeve clearly off the arm; P1 more than P2) and **Judgement** on the amounts. **Read:** CYC man size chart, upper arm XL 15½ in (39.5 cm), so Ron's 40.0 is CYC XL; it gives body sizes only, no ease. No period leaflet was reached. |
| **A2** | **Trouser taper and break.** | Hem **54.0 cm round one leg** (21¼ in; half foot 10⅜ in in Thornton's draft). Thigh 86.0, knee 62.2 (unchanged). Back of the hem **2.5 cm off the floor**, on the boot heel. Front 1 in higher, as Thornton's T27 hollow. The boot's instep lifts the front, so the cloth breaks once above it. Leg 31⅛ in (test 4: 30½). Inseam 79.5 cm, outside leg with band 117.1 cm. Plain hem, no turn-up. | **Photo** (P1: full thigh narrowing to the hem, one break on the shoe, plain hem). **Derived:** the 1 October research note gives "about 54 cm round the hem, a half break on the boot" (its own inference) and Fryer's 1990 dock photographs show hems breaking on black boots. **Read:** T27 (Thornton). **Judgement:** 2.5 cm. |
| **A3** | **Two forward pleats and a crease** on each front. | Pleat 1 is 3.5 cm, on the crease; it opens the front from the waist and tapers to nothing at the knee. Pleat 2 is 2.5 cm, halfway to the side seam, tapering to nothing at the seat line. Each is tacked 1.5 cm below the waist seam (a V sewn edge to edge) and continues as a fold line. The crease runs through the middle of the knee line and the hem line; it is also the grain line. A back crease is pressed up to below the seat. | **Photo** (P1: two pleats and a crease). **Judgement:** sizes, direction (toward the fly) and tack depth. The simulator needs the tack to fold the cloth. |
| **A4** | **Waistband flush, with a fly.** | The band's lower edge is cut in six segments, each equal to the waist segment it is sewn to between the pleats and darts, so the band is exactly the waist seam: 110.5 cm, no step. Two halves with a centre-back seam; depth 4.45 cm (Thornton's 1¾ in). The right half has a 3.8 cm underlap extension. **Fly 20 cm** down the front rise: a facing (4.5 cm wide) behind the left front, a shield (5.0 cm) behind the right, and a topstitch line 3.5 cm in on the left front. The fly is sewn shut (the simulator cannot do a zip). | **Photo** (P1, P2: a plain band flush with the trousers, a front fly). **Derived:** band lengths. **Judgement:** fly length and widths, British left-over-right. |
| **A5** | **Ribs that draw in.** | **Hem rib** 7 cm deep, relaxed **106.6 cm** (0.80 of the 133.3 cm body), stretched about 10 to 15 % over the trousers at the hip. The body is gathered onto it and lengthened 1.5 cm so it blouses and still ends where test 4's did. **Cuffs** 6 cm deep, relaxed **19 cm** (0.9 of Ron's 20.9 cm wrist), so they grip; a 30 cm sleeve is gathered onto them. **Neck rib** 2.5 cm deep, single layer, relaxed **39.8 cm** (0.88 of the 45.2 cm neckline): stretched 14 % at the seam, so it lies flat against a neck of 44.2. In the simulator, give rib knit very low crosswise stretch stiffness. | **Read** (web search summaries, pages not opened): ribbing is cast on with about 10 % fewer stitches on needles a few sizes smaller, and 1×1 rib is more elastic than 2×2 (sheepandstitch.com, sarahmaker.com, Wikipedia "Ribbing (knitting)"). Together these give about 20 %, hence 0.80. **Scaled:** P1, rib about 7 cm against a 72 cm body. **Derived:** cuff from the wrist. **Judgement:** neck 0.88, blouse 1.5 cm. |
| **A6** | **Sleeve length and cuff bunching.** | The cuff edge stays at the wrist bone (test 4's J17, 64.6 cm from the shoulder point; the reviewer judged it right). The sleeve is 2 cm longer above the cuff, and the extra bunches over the rib. Width above the cuff 30 cm. | **Photo** (P1, P3: bunching at the cuff; P2: the cuff at the wrist). **Judgement:** amounts. |
| **A7** | **Shoulder line dropped.** | The shoulder seam runs **6 cm past the shoulder point**, down onto the upper arm. Shoulder seam 21.4 cm. The armhole is 2 cm deeper (28.7 cm) and steps in by 5.1 cm over a 6 cm curve at the underarm. Sleeve cap 11.4 cm high, its seam equal to the armhole (J21 kept). | **Photo** (P1: the armhole seam well down the upper arm, about 8 to 10 cm). It disagrees with P2 (near the shoulder bone) and with test 4's J08 (set in). **Judgement:** 6 cm, between them. See the disagreements. |
| **A8** | **Body length and hang kept.** | Chest 133.3 cm, straight body. Back length to the hem edge 72.1 cm when bloused (73.6 cut). | **Read** (CYC via test 4). The reviewer judged both right. |
| **A9** | **Seat shape from the pattern.** | Thornton's back (seat seam, seat angle, the 1 in seat rise, two darts) is sewn as drafted; the simulation gives the seat. In the outline, the cloth now follows the body's own section from the band to the seat line, with an ease growing from the band's to the seat's. Test 4's O9 ran a straight girth, which made the flat seat. | **Read** (Thornton). **Derived** (outline). |
| **A10** | **Slant side pocket** shown as a line on the front (opening from 3.5 cm in at the waist to 17 cm down the side seam). Not cut. | | **Photo** (P1). **Judgement:** not cut, since pocket bags do not show. |
| **A11** | **No belt, no belt loops.** | | **Judgement:** P1 and P2 both hide the waist (rib, hands). |
| **A12** | **Shirt collar under the crew neck** (P1). **Not in this pattern:** a shirt is a separate garment. Listed so it is not forgotten. | | **Photo** (P1), and the research note (older men wore a crew or V-neck jumper over a collared shirt). |

Unchanged from test 4: Thornton's Stout Man's draft and its checks, the 133.3 cm chest, the neck width and depths, the back darts, the waistband depth, the knee girth.

## What the photographs show, element by element

| Element | Photograph shows | Test 4's target said | Now | Source |
|---|---|---|---|---|
| Neck rib | narrow rib lying flat round the base of the neck (P1, P3) | 2.5 cm, 0.85; the outline rib standing on the yoke | 2.5 cm single-layer rib, 0.88, sewn stretched: piece neck_rib | A5 |
| Hem rib | deep rib drawn in at the hip, knit bloused over it (P1, P2, P3) | 6 cm, 0.90, worn over wider trousers | 7 cm, 0.80, body gathered onto it, +1.5 cm blouse: pieces hem_rib_front, hem_rib_back | A5 |
| Cuffs | rib bands gripping the wrist, sleeve bunched over them (P1, P3; P2's cuff at the wrist) | 22 cm rib, 26 cm above it (and not modelled) | 19 cm, 30 cm sleeve gathered onto it, 2 cm bunched: pieces cuff_L, cuff_R | A5, A6 |
| Sleeve | stands off the arm, soft folds, no muscle (P1, P2, P3) | 51.8 cm at the top, 37.6 at the elbow, about 3 mm over the forearm | 52.0 / 46.6 / 43.5 cm | A1 |
| Shoulder line | seam dropped onto the upper arm (P1); near the shoulder bone (P2, P3) | set in, cross back = shoulder + 1 cm | dropped 6 cm | A7 |
| Jumper length | hem at the top of the hip, over the trouser waistband (P1, P3) | 72.1 cm | kept, bloused | A8 |
| Sleeve length | cuff at the wrist bone (P2, P1) | 64.6 cm | kept, +2 cm bunched | A6 |
| Body hang | loose, straight, smooth (P1, P2) | 133.3 cm | kept | A8 |
| Shirt collar | white collar above the crew neck (P1) | not mentioned | listed, not in this pattern | A12 |
| Waistband | plain band flush with the trousers (P2; P1 under the rib) | separate band, with a step at the seat line | band = waist seam exactly | A4, A9 |
| Fly | front fly between the pleats (P1, P2) | a 1½ in band extension only | facing, shield, topstitch line, fly sewn shut | A4 |
| Pleats | two front pleats each side (P1) | flat front (A-T7) | 3.5 and 2.5 cm, tacked | A3 |
| Crease | pressed front crease from the pleat to the hem (P1) | none | fold line on the grain; back crease too | A3 |
| Side pocket | slant opening at the hip (P1) | none | line on the front | A10 |
| Seat | full (heavy man; the reviewer's fault 9) | straight girth from band to seat (O9) | Thornton's seat sewn; outline follows the body | A9 |
| Leg shape | full thigh narrowing to the hem (P1) | straight leg, 57.8 cm hem (A-T3) | 86.0 thigh, 62.2 knee, 54.0 hem | A2 |
| Hem and break | hem resting on the shoe front, one break, plain hem (P1) | level, 4 cm off the floor, no break (A-T5) | 2.5 cm at the back, T27's front hollow, break from the boot | A2 |
| Belt | none visible (P1, P2 hide the waist) | none | none | A11 |

## Where the books and the photographs disagree (the photographs win)

1. **Shoulder.** Test 4's J08 (CYC cross back, set in at the shoulder bone) against P1's dropped shoulder. Dropped, by 6 cm. P2 is nearer set in, so the amount is a compromise; P1's 8 to 10 cm may be 1988 fashion knitwear rather than a plain 1990 jumper on a man in his fifties. **Flag for the coordinator.**
2. **Leg shape.** Thornton's normal knee and foot ratio (A-T3: straight, 57.8 cm hem) against P1's taper. Changed to 54.0.
3. **Length.** Test 4's A-T5 (level, 4 cm off the floor, no break) against P1's break on the shoe. Changed to 2.5 cm at the back, with a break.
4. **Front.** Test 4's flat front (A-T7) against P1's pleats. Changed to two pleats each side.
5. **Hem rib.** J05 and J06 (6 cm, 0.90) against P1's deeper rib, drawn in. Changed to 7 cm, 0.80; the knitting rule (about 10 % fewer stitches and smaller needles) agrees with the photograph.
6. **Cuff.** J19 and J20 (22 cm rib, 26 cm above it, no bunching) against P1 and P3's bunching. Changed to 19 cm and 30 cm, with 2 cm of extra length.
7. **Sleeve widths.** J16 to J20 (judgement) against the stand-off in all three photographs. Widened (A1).
8. **Armhole depth.** CYC's 26.7 cm suits a set-in sleeve; the dropped shoulder takes 2 cm more.

## Self-check (self_check_md.py, run 8 October): PASSED

- **Seams: 51 of 51 pass.**
  - 31 equal-length seams within 3 mm.
  - 6 rib seams at their stated ratio, exact: cuffs 0.633, hem rib 0.80, neck rib 0.88.
  - 4 eased trouser seams with the difference stated: outseam 0.96 cm, longer at the back (Thornton's side seam plus a little from the pleat spread); inseam 0.21 cm, the under side stretched as tailors do.
  - Pleat tacks, darts, fly, band and crotch seams all equal.
- **Finished girths and lengths: 18 of 18 within 5 mm.** Each is measured from the piece outlines against the target table set from the amendments: chest 133.3, back length 73.6 cut, hem rib 106.6 and 7.0 deep, sleeve top 52.0, sleeve length 60.6, sleeve above the cuff 30.0, cuff 19.0, neck rib 39.8, shoulder seam 21.4, waistband 110.5, waist seam after pleats and darts 110.5, seat 128.5 (Thornton's measure, with the pleat fullness), thigh 86.0, knee 62.2, hem 54.0, inseam 79.5. The outside leg (117.1) is reported only: the break sets it.
- **Sleeve ease against Ron (girths re-measured from ron_parts.npz): 3 of 3.** Biceps 52.0 − 40.0 = 12.0. Elbow 46.6 − 36.6 = 10.0. Forearm 43.5 − 34.5 = 9.0.
- **Photograph elements: 18 of 18 covered** by an existing piece, edge, seam, internal line or rule.
- **Outlines:** all counter-clockwise; every edge's index list walks adjacent points.

## Outline: what changed (target_md.json)

target_md.json is made by test 4's target_outline.py, run unchanged except for these globals:
- the sleeve's width along the arm, from the dropped shoulder, the new widths and the cuff;
- hem rib 7 cm deep and 106.6 cm relaxed;
- trouser hem 2.5 cm off the floor at the back and 54.0 cm round;
- seat and thigh girths with the pleat fullness;
- the seat following the body (replacing O9's straight girth).

Its own self-check (covered points within 3 mm of their outline) is in the file and below. **What the outline cannot show:**
- the break: the body mesh has no boot;
- the pleats, crease, fly, rib texture and folds;
- the dropped shoulder: the silhouette is the same.

The pictures and the simulation must show these.

**Its self-check: passed.**
- Covered points outside their own outline by more than 3 mm: jumper 0 of 10,318 front and side; trousers 0 of 7,219 front and side (worst 2.0 mm, side).
- There are 7,219 trouser points, against 7,069 in test 4, because the lower hem covers more of the ankle.
- Levels: rib top at z 1.065, trouser hem at z 0.025 at the back and 0.050 at the front.

**Still a limit:** the outline keeps O7, so the hem rib is drawn as no narrower than the trousers under it. The pleated trousers are wider there (128.5 cm) than the rib's relaxed 106.6 cm. On the body, the rib compresses the trousers' fullness, and only the simulation can show that. The reviewer's fault 7 has to be judged on the simulated picture, not on this outline.

## Notes for sewing in Marvelous Designer

- **Ribs:** sew the rib seams with unequal lengths at the ratios given. Use a rib-knit fabric with low weft stiffness, or MD's elastic on the rib's seam lines at the same ratio, so the rib draws in rather than the body stretching.
- **Fly:** front_L's fall_upper carries three layers: the right front, and the fly facing behind it. MD allows more than two pieces on one line.
- **Pleats:** each pleat is a 1.5 cm V tack sewn edge to edge, plus a fold line. Set the crease fold lines to about 180° with some fold strength so the press holds.
- **Mirrored pieces** (the second leg, sleeve and cuff) are written out in full, with their own indices.

## Not reached

- **1980s British knitting pattern leaflets** (Patons, Sirdar, Wendy, Emu): none reached in the time. Sleeve ease is judged from the photographs.
- **CYC's fit and ease page:** the address tried returned 404. The man size chart was read.
- **The rib sources:** reached only as search summaries; the pages were not opened.
- **Period British trouser bottom widths** for a 42 in waist: none found. The search found two 1980s designer listings at 18 to 18½ in (US sellers, slim men); they are not used.
- **Ron's boot mesh** (ron_boots_skinned.fbx): not measured, so the instep height under the hem and the size of the break are judged (the front about 3 cm higher than the cloth would hang).
- **Ron's hand girth,** for the cuff's stretch over the hand.
- **A tailoring source for pleat sizes and fly length** (Aldrich and others are in copyright and were not reached): judgement.
- **No plain crew-neck period photograph** (test 4's photo search). Plainness comes from P3, which is modern.
