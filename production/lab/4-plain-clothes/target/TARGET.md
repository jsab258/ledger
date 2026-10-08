# Target: Ron's plain 1990 jumper and trousers

## Sources

- **Read:** Thornton, *International System of Garment Cutting*, 2nd ed., c. 1911 (archive.org `Thornton_International_System_of_Garment_Cutting`, PD Mark): p. 286 (leaf n288), Plate 110 (n289), p. 288 (n290), Plate 112 (n293).
- **Read:** Craft Yarn Council (CYC) man size chart, craftyarncouncil.com/standards/man-size. **Not read:** CYC fit bands. **Not found:** 1990 trouser widths.

## Ron's measures

- **json (mm):** chest 1231, waist 1079 (z 1.139), hips 1156 (z 1.019), neck 442, biceps 442, wrist 217, shoulders 446, shoulder to wrist 636.
- **mesh:** seat 1187 (z 0.95), crotch z 0.826; neck point (±0.090, 0.010, 1.668); shoulder point (±0.235, 0.015, 1.600); back neck z 1.635; notch z 1.620; elbow (0.272, −0.005, 1.215); wrist (0.318, −0.170, 1.035). The json's HPS (1.611) disagrees; mesh used.

## Trousers (Thornton)

**Rules.** T01–T27 are Dia. 1's printed rules. S01–S05 are the Stout Man's exceptions.

**Check: passed.** All 25 of Dia. 1's worked values (within 1/16 in) and all five of Dia. 8's match; every rule re-measures.

**Readings.**
- T22 prints "X to 8"; read as "5 to 8", as in the small-waist draft.
- Dia. 8 prints seat 21 1/2 but works with 21; the working is followed.
- C and 9 (unprinted) go on G's square line, side seam produced, per the plates (A-T1, A-T2).

**Ron (inches).** Side 45 1/4, leg 30 1/2, half waist 21 1/4, half seat 23 5/8, half knee 11 3/4, half foot 11 1/8. Disproportion 5/8: Stout Man's draft.

**Adaptations.**
- **A-T3 (judgement):** straight leg. Knee and foot keep Thornton's normal ratio to the seat.
- **A-T4:** seat = mesh + 1/2 in (measured over trousers).
- **A-T5 (judgement):** level hem, 4 cm off the floor. The 1 in front hollow (T27) is kept.
- **A-T6 (judgement):** fork 1 cm below the crotch.
- **A-T7:** cut at the waist-hollow line; the 1 3/4 in band becomes a separate waistband (z 1.139–1.184). Flat front.
- **A-T8:** two 1/2 in back darts (p. 288); their 3 1/2 in length is judgement.

**Girths (cm).**

| Waistband | Seat | Thigh (one leg) | Knee | Hem | Rise | Inseam | Outside leg |
|---|---|---|---|---|---|---|---|
| 110.5 | 123.8 | 84.2 | 62.2 | 57.8 | 33.0 | 77.9 | 111.0 |

## Jumper (cm)

- **J01** ease 4 in (judgement). **J02** chest + ease = 133.3. **J03** front = back = half.
- **J04** back length = CYC back hip length, interpolated: 72.1 (hem z 0.995).
- **J05, J06** hem rib 6 deep, 0.90 × width (judgement).
- **J07** armhole depth = CYC, interpolated: 26.7 (underarm z 1.333).
- **J08** cross back = shoulder to shoulder + 1 (judgement).
- **J09–J11** from the mesh: shoulder drop 6.8, neck width 18, back neck depth 3.3.
- **J12** front neck at notch + 2. **J13** armhole steps in over its lower third. **J14, J15** neck rib 2.5 deep, 0.85 × neckline (all judgement).
- **J16** biceps + 3 in = 51.8. **J17** shoulder to wrist + 1 = 64.6. **J18–J20** cuff 6 deep, 22 round, 26 above it (all judgement).
- **J21** cap seam = armhole: cap 19.1 high, elbow 37.6.

## Outline rules

The front and back views share one (x, z) silhouette.

**Both garments**
- **O1** Cloth sits at least 3 mm off the body (judgement).
- **O2** Supported cloth: the body's section grown by (garment − body girth) / 2π.

**Jumper**
- **O3** Above the underarm: the upper body + chest ease (18 mm); a 2.5 cm neck rib on top.
- **O4** Hem where J04 runs out down the centre back, hollows bridged.
- **O5** Below the chest it falls straight: hull of the eased chest section and the body (or trousers) + 3 mm.
- **O6** The rib grips, then blouses over 4 cm (judgement).
- **O7** Worn over the trousers.
- **O8** Sleeve: the arm's section grown to the pattern's width along the arm's axis (see C1, C4).

**Trousers**
- **O9** The waistband grows to 110.5. Below it the girth runs straight to 123.8 at the seat line.
- **O10** Knee line (z 0.479) to seat line (z 0.916): edges run straight to the seat's side, the fork, the seat front and fullest back.
- **O11** Below the knee: a round tube of the pattern's girth. The hem is 1 in higher at the front.

**Seams and coverage**
- **O12** Seams where these rules put the pattern's edges: side and leg seams at section extremes, armholes an ellipse at x ±0.228, crotch seam on x = 0, hems, cuffs and band as rings.
- **O13** Jumper: neckline to z 0.995, arms to the wrist; trousers: z 1.184 to the hem (cover_lod0.npz).
- **O14** No head, hands or feet.

## Corrections (8 October, after the coordinator's check)

- **C1 (sleeve):** at each station along the arm's axis the sleeve edge stands off the arm's own covered points by the ease, joined with those points + 3 mm, so never inside the arm + 3 mm. The cuff end is the wrist plane that ends the covered list (list not trimmed).
- **C2 (feet):** points below the hem line (0.040 back to 0.0654 front) or outside the leg tube below z 0.12 leave the trousers list: 7,385 to 7,069.
- **C3 (band top):** the trousers' top edge is now exactly at z 1.1835.
- **C4 (sleeve cap):** no yoke-to-sleeve step. From the shoulder point to the cap height h (19.1) the ease grows along a quarter-sine, e = 3 mm + (e_h − 3 mm)·sin(π/2·s/h).
- **Self-check:** `target_outline.py` fails if any covered point is over 3 mm outside its outline in any view. Now 0 of 10,318 and 0 of 7,069.

## Left open

Curves not digitised; about 5 mm step at the trouser seat line; sleeve droop ignored; not yet reviewed.
