#!/usr/bin/env python
"""Writes TARGET.md of the bollards family from target.json (the numbers) and the prose below.
/home/user/.bpyenv/bin/python make_doc.py"""
import os, json, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
T = json.load(open(os.path.join(HERE, 'target.json')))
K = T['kinds']


def pts(prof):
    return ', '.join('(%g, %g)' % (r, z) for r, z in prof)


def rows(prof, n=6):
    out = []
    for i in range(0, len(prof), n):
        out.append('`' + ', '.join('(%g, %g)' % (r, z) for r, z in prof[i:i + n]) + '`')
    return '<br>'.join(out)


def parts_table(kid):
    s = '| part | z from | z to | r min | r max | what |\n|---|---|---|---|---|---|\n'
    for p in K[kid]['parts']:
        s += '| %s | %g | %g | %g | %g | %s |\n' % (p['name'], p['z0'], p['z1'], p['r_min'], p['r_max'], p['what'])
    return s


fr = T['photo_frames']
fit = T['self_check']['photograph_fit'] if 'self_check' in T and 'photograph_fit' in T['self_check'] else {}
P = T['calibration']['panoramas']
H1, H2, H5 = K['K1']['height'], K['K2']['height'], K['K5']['height']
P2 = K['K2']['profile_rz']
VF = T['variant_fits']
SC = T['self_check']['result'] if 'self_check' in T else '(run self_check.py)'

md = '''# Quay Street's bollards and the quay's mooring ironwork: the target (cloud week 42, 9 October 2026)

**%(summary)s**

The target for the family "bollards on Quay Street and at its quay end", written from Poly Haven's CC0 London photographs (all 2019) and the repository's own numbers. Everything is millimetres unless a line says otherwise; the .glb is metres, z up, scale 1. `target.json` holds the same numbers for a script; `target_drawing.py` draws them (elevations, plans, the street's places, each kind laid on its photograph); `self_check.py` tests them against their own sources (last result: **%(sc)s**). `make_target.py`, `make_previews.py`, `calibrate.py`, `make_doc.py` and `bollard_data.py` re-make the files from the hand-read numbers and the panoramas.

**Photographed kinds, in one breath.** K1 is a black cast-iron post, %(K1_H)s high, a plinth foot %(K1_baseD)s across, one straight taper, one fat half-round bead at half height (0.506 H), a neck, a rounded cap collar and a flattened dome (Photo, one model, measured at its bed level). K2 is a plain tapered iron post, %(K2_H)s high (K2a, flat cap) or %(K2b_H)s high (K2b, low cone cap, a smaller casting), a rolled foot ring %(K2_ringD)s across, a thin collar band at 0.59 H, black by default (Photo, two panoramas, each at its own camera height). K5 is a bolted chain post, %(K5_H)s high, on a 286 flange with four nuts, two beads and a dome, with D-lug eyes at 420 and 840 for a plain chain (Photo, one marina). K3 (concrete), K4 (steel tube), K6 (mooring bollards: the kit's bell and an upturned cannon, 982 high) and K7 (cleat) have NO photograph in reach and are judgement, the kit's or the asset plan's numbers, marked so everywhere. **This is the target's second version, amended after a fresh review (section 15).**

## 1. Where on Quay Street bollards would have stood in 1990, and how many

The clutter research (street-clutter-1990, "Bollard (weak)") says: old cast-iron "cannon" bollards at terrace corners, alongside plain precast concrete ones; black paint, sometimes a white band (uncertain; no photograph shows one, so none is used); nothing reflective, stainless or gold. The asset plan wants "bollards at corners and the quay edge", 6 to 10 on the street, "two to four models a kind, because a council fits one design to a street". The scene file already puts two bollards at the yard mouth. So, in the street recipe's frame (x along the street, 0 at its south end, + north; y or z across, east positive; metres; the kerb face at +-3.0; the footway 2.0 m):

| place | kind | count | where (x, y or z, m) | axis behind the kerb face | basis |
|---|---|---|---|---|---|
| the yard mouth, either side of the 3.0 m crossover (x 21.0 to 24.0), west | K1 cast iron, domed | 2 | (20.7, -3.5) and (24.3, -3.5) | 0.5 m | Read: the scene file already places them; Photo: the pattern stands at corners |
| either side of the mouth of the 1.0 m passage between the parade and the chandler (x 39 to 40), east: the path to the yard and steps behind, so a car cannot nose onto the footway there | K3 concrete | 2 | (38.8, 3.5) and (40.2, 3.5) | 0.5 m | Judgement: the plain precast posts the clutter research names at terrace corners; older council stock |
| anti-parking posts at the chandler's front (x 40 to 46), east: the chandler's own private posts | K4 steel tube | 2 | (41.5, 3.45) and (44.0, 3.45) | 0.45 m | Judgement: a shop front's own posts; no photograph |
| the quay-end junction (atlas (400,320), x = -30): the two tangent points of the 8 m return (inside Quay Street's turn west) and the two of the 6 m return (the Harbour Board approach), each moved 0.5 m from the kerb face along the footway normal; NONE on the 12 m outside return | K2 plain iron, black | 4 | (%(jn1x)s, %(jn1y)s), (%(jn2x)s, %(jn2y)s), (%(jn3x)s, %(jn3y)s), (%(jn4x)s, %(jn4y)s) | 0.5 m | Judgement for the places; Derived for the coordinates: what the south-quay kit's Junction builder computes (`self_check.py` recomputes them from the kit) |
| **on the street and its junction** | | **10** | | | the asset plan's 6 to 10 |
| the north quay (five, x -69.25, 0.75 m behind the cope nose, y -88, -58, -28, 2, 30), the jetty (two, x -110.75, y -80 and -45) and the east quay (three, y 40.75, x -95, -115, -140) | K6 mooring bollard: K6b (the cannon) at the three quay ends (-69.25,-88), (-69.25,30), (-140,40.75), K6a (the bell) at the other seven | 10 | the south-quay kit's BOLLARDS, exactly | 0.75 m behind the cope | Read (the kit); the cannon is Judgement |
| the north quay's ladder (y -36): four posts at x -69.5 (0.5 m behind the nose), y -40.5, -37.5, -34.5, -31.5, a plain chain between the OUTER pairs only (-40.5 to -37.5 and -34.5 to -31.5); the 3.0 m over the ladder stays open so a person can climb out | K5 chain post | 4 | as stated | 0.5 m behind the cope | Judgement on the kit's ladder |
| the jetty (stone, a granite cope; the kit has no timber fender): three cleats on the cope at x -110.25 (0.25 m behind its nose at x -110), y -64, -58, -52, long axis along y, beside the jetty boat's berth (y -63 to -53) | K7 cleat | 3 | as stated | 0.25 m behind the nose | Judgement on the kit's jetty and boat |

**Why four kinds share one street** (against the asset plan's "one design to a street"): the design is one per OWNER, and a harbour street has several: K1 is the council's cast stock (the yard mouth), K3 older council precast stock (the side passage), K4 the chandler's own private posts, K2 the Harbour Board's, where its approach meets the street (the junction).

Never in front of a door or a lamp column, never in the crossover, never leaving less than 1.2 m of footway (the footway is 2.0 m: the axis at 0.5 m and a base radius of 0.1 leave 1.4). The photographs show set-backs of 0.33 m (K1 in the inside corner of a kerb build-out), 0.93 m (K2a on a 2.5 m footway) and about 0.91 m (K2b on a wide footway), recomputed at the corrected camera heights; 0.5 m is the scene's Read value, the right one for a 2.0 m footway (a bollard 450 to 600 mm back is the usual rule: Judgement), and is kept. The existing yard-mouth bollard at x 24.3 stands 0.52 m (in x) from the tea room's side door centre (24.822) but 1.5 m from the facade, at the kerb: it does not block the door and is kept (Read).

## 2. Sources

All photographs are Poly Haven's, CC0 (licence read at https://polyhaven.com/license on 9 October 2026: "All assets ... are licensed as CC0"), author Andreas Mischok, used for measuring only: not placed in the game, not traced into a texture, not fed to an image model. The cloud's network refused Wikimedia, Geograph, Flickr, archive.org, Historic England, British Listed Buildings, dimensions.com, pavingexpert, gov.uk, Hertfordshire, the Bristol Industrial Archaeological Society and every other site I tried (only Poly Haven answered): **no photograph from 1975 to 2000 was reached; every photograph is from 2019**, and for each the table says whether it shows the period object or a replacement and why it would look the same in 1990.

| id | URL (files via api.polyhaven.com/files/<id>, the 8k tone-mapped JPG) | date read | author, licence | date taken (lat, lon) | what it shows | used | period or replacement, and why the same in 1990 |
|---|---|---|---|---|---|---|---|
| S1 | https://polyhaven.com/a/urban_street_01 | 2026-10-09 | Andreas Mischok, CC0 1.0 | %(d_us01)s (51.528295, -0.053879) | a Bethnal Green street (east London): five or six black cast-iron bollards (four inspected: the same pattern), each at a corner of a granite kerb build-out and planted bed whose soil is 0.07 m below the footway, a 75 mm-gauge brick wall | YES, K1 main (US01_b) | The pattern (plinth, taper, bead, domed cap) is the long-lived cast form and the paint is worn: the bollards are probably older than ten years but their date is unknown, so they may be 1980s to 2010s castings. They differ from 1990 in fresh gloss paint and a re-set build-out; no band, no reflective strip, no crest is visible. |
| S2 | https://polyhaven.com/a/bethnal_green_entrance | 2026-10-09 | Andreas Mischok, CC0 1.0 | %(d_bge)s (51.526915, -0.054044) | a park entrance: three or more of the same family on block paving, one with its foot paint mostly gone, a gate pier with a 75 mm brick gauge | EVIDENCE ONLY (BGE_a, a second casting: not a model) | Block paving is 1990s to 2000s; the bollards' pattern is the same family, shorter and slimmer, with a taller rolled plinth. Same caveat as S1. |
| S3 | https://polyhaven.com/a/birbeck_street_underpass | 2026-10-09 | Andreas Mischok, CC0 1.0 | %(d_bb)s (51.525806, -0.056277) | a street under a railway arch: about ten grey plain tapered bollards on a concrete-kerbed footway, double yellow lines | YES, K2 main (BB_b) | Plain tapered iron posts were fitted from the 1970s; this grey paint and the flat top may be a 1990s to 2010s fitting (black was the 1990 norm: black is the default); the arch lights light it orange, so its grey is read as a neutral mid-dark grey. |
| S4 | https://polyhaven.com/a/urban_street_02 | 2026-10-09 | Andreas Mischok, CC0 1.0 | %(d_us02)s (51.526655, -0.056465) | an estate road: the same plain tapered bollard in black with a low cone cap, on flags | YES, K2b (US02_a) | A 1970s to 80s housing estate; the bollard may be older than the 2000s window frames beside it. Same caveat. |
| S5 | https://polyhaven.com/a/limehouse | 2026-10-09 | Andreas Mischok, CC0 1.0 | %(d_lh)s (51.510606, -0.036324) | a marina basin (Limehouse): bolted cast-iron chain posts, a spiked chain, resin-bound gravel, clay paviors, floating pontoons | YES, K5 (LH_b) | The marina is a 1980s to 90s redevelopment; the bolted flange and the spiked chain may be later than 1990; kept as the only photographed British quay-edge ironwork. |
| S6 | the repository: production/specs/vignette-scene.json, vignette-pieces.json; production/cloud-week/targets/SCENE-SLOTS.md, kerbs-and-covers/TARGET.md, shopfronts/target.json; production/research/asset-plan/3-FURNITURE-PROPS-FOOD.md; street-clutter-1990/SUMMARY-2026-09-29.md; south-quay/METHOD-2026-10-06.md; tools/art-recipes/south-quay/south_quay_geom.py; production/assets/street/clutter/bollard.glb | 2026-10-09 | the project | 2026-09-29 to 2026-10-09 | the street's layout, its levels, its furniture, the present stand-ins (0.765 and 1.008 m), the quay kit's bollard | YES (Read numbers) | n/a |
| S7 | WebSearch result summaries, 9 October 2026: a cannon-bollard history (quay guns, Napoleonic surplus), manufacturer heights (1100, 1140, 1520 mm, "around 1 m" for visual accessibility), a 2011 county standard drawing for a 230 mm precast bollard at 600 or 915 above ground, a 160 x 750 concrete post, Bristol's 1893 quay bollards, Charlestown's upturned cannon barrel | 2026-10-09 | third-party pages (reached only as summaries) | n/a | leads | LEADS ONLY: no number taken | n/a |

**Looked at and left out.** adams_place_bridge, cambridge, canary_wharf, leadenhall_market, urban_street_03 and urban_street_04 show no bollard that is a street bollard (a keep-left sign post in 04 is a sign); docklands_01 and docklands_02 are Dublin (coordinates 53.346, -6.238), not Britain, and were not used. Poly Haven's catalogue (2,384 assets, searched 9 October) has no bollard, cleat, mooring post or chain-post model (its modular wooden pier and lateral sea marker are not what is wanted). ambientcg.com answered its home page; no bollard asset was looked for there.

**Unreached** (a page that refused is not evidence; nothing was taken from any of these): Wikimedia Commons, Geograph, Flickr, archive.org, HathiTrust, Historic England (list entries 1202530 and 1272267), British Listed Buildings, the Bristol Industrial Archaeological Society's PDF, dimensions.com, pavingexpert, gov.uk, a county highways PDF, Sketchfab, Pexels, Unsplash (all refused or not resolvable); WebFetch of two PDFs failed to resolve the host.

## 3. How the photographs were measured, and why the camera height is not 1.6 m

Each panorama (8192 x 4096) is re-projected with numpy to a flat, square-on elevation of one bollard: a vertical plane through its axis, perpendicular to the line of sight, 1 mm a pixel (the native resolution is 2.5 mm a pixel at 3 m, 5 mm at 7 m, so the pictures are up-sampled and soft). The foot of the base gives the bearing and the distance (from the depression angle and the camera height); the base radius puts the axis 0.1 m behind the foot's front edge. **Every length then scales with the camera height**, which the panoramas do not give.

**Each camera height is measured at the bollard's own ground level; where an anchor stands on another level, the step between them is measured and added.** (The first version of this target put two heights at the wrong level: Birbeck's line is on the road, 0.105 m below the footway the bollard stands on; US01_b stands in a planted bed 0.07 m below the footway the walls stand on; and US02_a was given a pooled 1.15 m with no anchor, which would need 95 mm brick courses.) Two kinds of anchor, both independent of the heights used to re-project the pictures:

1. **Walls by the horizon method** (`calibrate.py`, raw rows kept in `target.json` `calibration.horizon_anchors`): in a levelled equirectangular panorama the horizon is the middle row; on a vertical wall the courses of a 75 mm brick wall are evenly spaced in tan(angle) below the horizon; camera height above the wall's foot = 75 mm x tan(angle of the foot) / (course pitch in tan units). The joints were counted by eye on a crop, the pitch refined by a fold in tan units, the foot row read by eye.
2. **A yellow line or a paver on a plane at an assumed 1.6 m** (`calibration.anchors`): the true height is 1.6 x true size / measured size.

| panorama (session) | anchors, each brought to the bollard's ground | camera height used |
|---|---|---|
| urban_street_01 (18 Aug 2019), US01_b | garden wall 1.23 and gate pier 1.05 by `calibrate.py` (the reviewer: 1.23 and 1.19; both include the 0.07 m step down to the bed); the single yellow line 1.22 above the road, 1.17 above the bed | **1.195 +-0.07** (K1 x 1.030 against the first version) |
| bethnal_green_entrance (18 Aug), BGE_a | planter wall on the same block paving 0.96 (the reviewer 1.03 to 1.04); the gate pier's course 0.94 and stretcher 1.02 by re-projection | 1.02 +-0.07 (the reviewer: holds) |
| birbeck_street_underpass (18 Aug), BB_b | viaduct wall on BB_b's footway 1.05 (to 1.10 for a 79 mm Victorian course); the double yellow line 1.24 above the road, 1.13 above the footway; the reviewer's mean 1.085 | **1.085 +-0.06** (K2a x 0.8897 against the first version's 1.22) |
| urban_street_02 (18 Aug), US02_a | the building wall behind it 0.88 (the reviewer 0.93) and the gate pier at the panorama seam 0.92 (the reviewer 0.91), both on its own footway | **0.92 +-0.04** (K2b x 0.80 against the first version's 1.15) |
| limehouse (19 May), LH_b | a clay paver (200 x 100 with 5 joints) reads 146 x 280 at 1.6 m (1.15 and 1.17); the reviewer's blue-brick building on the same paving 1.15 to 1.18 | 1.17 +-0.06 (holds) |

Where my own horizon measurements and the fresh reviewer's differ by 5 % (BGE, the US01 pier, the US02 wall) the reviewer's figures are adopted as the stated heights and the spread is the stated error: `self_check.py` recomputes every anchor from its raw rows and fails if the mean at the bollard's ground is farther from the stated height than the stated error. Nothing in group C of the self-check tests the scale (the pictures are re-projected at the stated heights, so their fits are tautological for it); the calibration test in group B is the one that can catch a wrong height.

Results: no panorama was taken at 1.6 m; heights are 0.9 to 1.2 m above their own ground. **Every number below is +-4 to +-7 % in absolute size** (the proportions are exact to the pixel). **Tell the kerbs-and-covers writer**: it uses 1.6 m for urban_street_01 and urban_street_02. At the road (where its kerbs and covers lie) the heights are about 1.25 to 1.27 m in urban_street_01 (the bed 1.195 plus the 0.055 to 0.07 it stands above or below the road) and about 1.03 m in urban_street_02 (0.92 on the footway plus the 0.125 kerb), so 1.6 m is about 25 % high in urban_street_01 and about 55 % high in urban_street_02; its mitred-corner and tarmac-cover numbers from those two panoramas should be re-checked.

Other methods: `edge_residuals` in `bollard_lib.py` finds the strongest edge within +-10 mm of each predicted edge (group C: it tests the shape, not the scale); ground plans (the z = 0 plane, axis at the centre) give set-backs; widths and heights are read on gridded crops at 3 x (error +-1.5 mm in the picture, +-3 mm with the soft edges). A casting seam, a fluting or a mark would show at 5 mm a pixel only if 1 mm deep: none shows (the shaft's vertical streaks are reflections: a contrast-stretched crop of BGE_a shows no regular flutes).

## 4. Frame, pivot, glb

* Profiles are (r, z): r the radius from the axis, z up from the ground at the foot; each runs from (0,0) up the outline to the axis at the top (a lathe). Elevation polygons mirror the profile about the axis.
* **Pivot**: the centre of the base on the ground. On the footway that is the flag top, +120 mm above the channel top (the kerbs target's frame: the kerb face line at y = 0, the kerb top +125); on the quay the apron, level with the kerb top. The axis stands at y = -500 mm toward the footway.
* **glb**: metres, z up, scale 1, one mesh per variant; bolts, chain eyes and chains as separate meshes of the same piece; **no text, no decal with lettering, no crest, no monogram, no band** on any mesh or texture.
* The photographs' z = 0 is the ground at the axis: the front-bottom edge of a base appears 50 to 55 mm BELOW z = 0 in an elevation (it is nearer the camera than the axis), so the drawing's foot sits "above" the photographed foot in the overlays by that much.

## 5. The target, kind by kind

Every number carries its kind: **Read** (printed in the repository), **Photo** (measured on a photograph: method in section 3, +-4 to +-7 % in size), **Derived**, **Judgement** (a trade or period guess, said so).

### 5.1 K1: cast-iron street bollard, domed head, one collar bead (`cast_iron_domed`)

Height **%(K1_H)s** (Photo US01_b, measured at its own ground, the planted bed, at a camera height of 1.195 +-0.07 m; the first version's 1050 was 3 % small because it took the footway's level); plinth diameter %(K1_baseD)s; a stout post: shaft diameter %(K1_shaftD)s at the shoulder, %(K1_underneckD)s under the neck, %(K1_neckD)s at the neck. **One model.** (BGE_a is a second casting of the pattern, 6 % shorter and 13 % slimmer, with a taller rolled plinth: not modelled, a council fits one design to a street; the yard mouth uses K1 twice with two condition seeds.) Profile (r, z), authoritative in `target.json` `kinds.K1.profile_rz`:

<<K1_ROWS>>

<<K1_PARTS>>
* **Edges**: no sharp edges; every step rounded (R4 to R8) or coved; the foot has a 3 mm chamfer. No flats, no facets, no fluting, no beading on the bead. [Photo]
* **Mouldings**: the **collar bead** (z %(K1_b0)s to %(K1_b1)s, r peak %(K1_br)s, %(K1_bp)s proud of the taper, half-round, fuller below its middle, its underside the drip; a thin fillet ring about 4 high and 1 proud on its top edge); the **cap collar** (z %(K1_c0)s to %(K1_c1)s, r peak %(K1_cr)s, a fat rounded ring with a flat underside at the neck); a 4 mm **quirk**; a **thin ring** 15 high at r %(K1_tr)s; the **dome** (r %(K1_dr)s at its foot, %(K1_dh)s high, flattened). The plinth's top edge is R6 then a cove about 19 high to the shaft. [Photo US01_b]
* **Seams**: none visible at this resolution; a faint parting line down each side may be added at 0.3 mm (Judgement). **Fixings**: none; rooted. **Marks**: none: no maker, council, crest, monogram or lettering was visible on any of the five or six bollards of S1 or the three or four of S2.
* **Root, how it meets the ground**: on flags or block paving the plinth stands directly on it; the paving is cut round it or butts it with a 5 to 15 mm dark grit joint, no mortar fillet, no collar plate (Photo BGE_a). In a planted bed it stands on the soil with bark chips and leaves banked about 20 mm against the plinth (Photo US01_b). **The bed level**: US01_b's ground is the soil, 0.07 m below the footway kerb top (a 0.05 visible face, an edging stone, then 0.02 to the soil); its camera height is measured there. On a footway the pivot is the flag top.
* **Paint**: black, sRGB **(24, 24, 26)** (measured medians 38, 10, 15 and 18 across four tone-mapped panoramas: 24 chosen), gloss, roughness **0.35** (the sky shows in the dome, the bead and the shoulder), metal 0. **No white or yellow band, no reflective strip, no sleeve** (none in any photograph; the research says reflective bands are wrong for 1990).
* **Wear and damage as photographed**: one pale vertical paint chip 15 x 65 mm at z 70 to 135 on one side of US01_b (primer or filler showing); fine scratches and dull rub marks below 0.5 m; dust and tyre grime on the plinth and lower shaft, cleaner above 0.7 m; a lean of about 1 degree in the viewing plane (0.7 to 1.6 degrees fitted on two). **The worn-foot condition ONLY** (Photo BGE_a): the lower 110 mm of the plinth bare grey-brown metal in a speckled pattern over 60 to 70 % of its area, sRGB (64, 58, 52) against the body's black; not every instance has it. No rust streaks, no graffiti, no stickers, no dents.
* **Variants**: one model; three conditions: glossy repaint with a few scuffs (US01_b); worn foot (BGE_a: plinth paint 60 to 70 % gone to z 110); dull and chalky with a rust bloom at the foot (Judgement). The second casting (BGE_a: every z x %(k1b_z)s and every r x %(k1b_r)s of K1, rms %(k1b_rms)s mm over 15 half widths; a plinth about 140 high with a convex roll on its top edge; the bead centre at 0.53 H) is evidence only, with no check.

### 5.2 K2: plain tapered iron bollard, collar band at 0.59 H (`cast_iron_plain`)

K2a: height **%(K2_H)s**, foot ring %(K2_ringD)s across (Photo BB_b, measured at its own footway, camera height 1.085 +-0.06 m: every z and r of the first version x 0.8897; shaft diameter %(K2_d300)s at z 300 and %(K2_d900)s at z 900). K2b: height **%(K2b_H)s**, foot ring %(K2b_ringD)s across (Photo US02_a at its own footway, 0.92 +-0.04 m: x 0.80 of the first version): a SMALLER casting of the same pattern, %(K2b_vs)s the height of K2a. Profile of K2a in `target.json` `kinds.K2.profile_rz`; **K2b IS `profiles_final.US02_a`, whole** (z x %(k2b_z)s, r x %(k2b_r)s of K2a over the shaft, then its own cone):

<<K2_ROWS>>

<<K2_PARTS>>
* **Edges**: rounded or coved throughout; the cap plate's edge R3. **Mouldings**: the **collar band** (z %(K2_c0)s to %(K2_c1)s, r peak %(k2_collar_r)s, %(K2_cp)s proud of the taper, a thin rounded band with no beads either side, at 0.587 H on BB_b and 0.592 H on US02_a); the **rolled foot ring** (z 0 to 46, r peak %(k2_foot_r)s, its top sloping in to the shaft, a lighter rub mark round it). **Cap**: K2a a flat plate overhanging the shaft by about %(K2_ov)s and domed 5 mm; K2b a rim ring (r %(K2b_rim)s, z %(K2b_z0)s to %(K2b_z1)s) under a low cone rising %(K2b_rise)s to the apex.
* **Seams, fixings, marks**: none visible. A thin dark scratch about 40 mm long at z 840 to 880 on BB_b is damage, not a seam. **Root**: the foot ring stands on the paving or tarmac, a darker 20 mm ring of dirt round it, no collar plate.
* **Paint: BLACK is the default** (the 1990 norm, and US02_a's paint): sRGB **(24, 24, 26)**, semi-gloss, roughness 0.45, metal 0. The grey of BB_b (sRGB (88, 89, 91), satin, roughness 0.5; the measured median (97, 77, 70) is under the underpass's orange light, lightness 81: neutralised, Judgement) is a 2019 London underpass paint and is ONE condition only. The orange rim seen on BB_b's cap is the underpass light on the plate, not brass. **No band.**
* **Wear and damage as photographed**: a lighter, scuffed ring round the foot ring; a few chips and thin dark scratches on the upper shaft (BB_b); a tan dust line at the foot; no rust, no dents; lean 0.2 to 1.0 degree.
* **Variants**: K2a (flat cap) and K2b (low cone); conditions: clean black semi-gloss (US02_a); scuffed with chips (BB_b); mid-dark grey satin (BB_b's paint).

### 5.3 K3: round precast concrete bollard (`concrete_round`): JUDGEMENT, no photograph reached

Height 850, foot diameter 250, top 200 (leads only: a county drawing's 230 mm precast unit at 600 or 915 above ground, a 160 x 750 post, "millions of concrete bollards" in the 1970s). Profile: `%(K3)s`. A tapered cylinder, a 20 mm chamfer into a shallow dome (rise 18); two vertical mould lines 180 degrees apart (1 mm) and a horizontal pour line at z 400 +-60. Bare concrete, sRGB (152, 150, 144), roughness 0.9, never painted, no band. Cast into a footing; the flags butt it with a 10 mm tarmac or mortar fillet. Wear: a dark grime band to 150 mm, rain streaks below the chamfer, a darker top, a chipped top arris with aggregate showing, a rust-coloured stain 40 mm wide from a cut-off lifting eye. One model, three conditions.

### 5.4 K4: steel tube bollard with a welded cap (`steel_tube`): JUDGEMENT, no photograph reached

A 114.3 mm tube (the asset plan's 60 to 114 mm), 1000 above ground, a welded shallow dome (rise 18) with a 2 mm weld bead, a vertical weld seam up the tube. Profile: `%(K4)s`. Painted black gloss (24, 24, 26, metal 0, roughness 0.4) or dull galvanised (120, 122, 124, metal 1). Set in a footing flush with the paving, a 15 mm tarmac fillet round it. **No band, no sleeve** (reflective bands are later). Wear: scuffs, a rust bloom 100 mm high at the foot, a dent and scrape at 0.4 to 0.6 m, a lean up to 2 degrees. One model: black, galvanised, black with a rusted foot.

### 5.5 K5: bolted cast-iron chain post (`chain_post`)

Height **%(K5_H)s** (Photo LH_b, +-6 %), flange 286. The POST is photographed; the photographed spiked chain is the marina's dress and is not used. Profile in `target.json` `kinds.K5.profile_rz`:

<<K5_ROWS>>

<<K5_PARTS>>
* **Fixings**: four hex nuts on studs through the flange, 22 across flats, 14 high, studs 14 above the nuts, on a pitch circle of radius 124, at 45, 135, 225 and 315 degrees to the line of posts (the photograph shows two at the sides and one at the front); nuts and studs bright steel (150, 150, 152, metal 1) with dull rust at the threads.
* **Chain eyes**: a cast **D-lug** on each side of the shaft at z **420 and 840** (+-30), in the line of the posts: **55 high, 40 proud of the shaft, 18 thick, with a 24 mm hole whose centre is 22 from the shaft face** (Photo LH_b, +-30 %); the chain's end link passes through the hole.
* **The chain on Quay Street's quay: plain short link, a 13 mm bar** (an unrestored 1990 working quay; Judgement, the photographed bar reads 12 +-15 %): inner length 39 (3 x the bar), inner width 18, outer 65 x 44, pitch 39, **no spikes**; post spacing 3.0 m (3.06 m read between two posts); mid-span sag 150 (Judgement); two chains, at the eye heights, black, rubbed bright where the links touch. The photographed marina chain (bar 12, inner length 55, inner width 25, outer 79 x 49, every second link with two conical spikes 28 long and 8 at the base at right angles to the link's plane, +-15 %) is kept in `target.json` only as an option the street does not use.
* **Paint**: black, sRGB (24, 24, 26) with a blue sheen from the sky (measured (17, 19, 27)), matt to satin and chalky, roughness 0.55, metal 0. **Marks**: an embossed mark about 45 mm long runs up the right side of the shaft at z 80 to 110 and is unreadable at this resolution: **LEAVE BLANK**, no maker's mark; the previews blur it. **Root**: the flange stands on resin-bound gravel (Photo) or the apron, the nuts proud.
* **Wear**: dust on the flange, pale dry splash marks to 0.2 m, the chain rubbed bright at its contacts; no rust on the casting, no graffiti. One model, with the plain chain or without.

### 5.6 K6: quay mooring bollards (`mooring_bollard`): Read for the bell pattern, Judgement otherwise; no photograph reached

**K6a, the bell bollard** of the south-quay kit (Read from `south_quay_geom.py`): 720 high, a flange r 250 (40 thick, then a cone), a barrel r 150 tapering to 130 at z 510, a head flaring to r 220 at z 630 that overhangs the barrel by 70, then a dome (soften the kit's polyline corners to R10 or more): `%(K6A)s`. **K6b, the upturned cannon** (a Charlestown lead; Judgement), **982 high**: a barrel r 190 at the foot tapering to r 150 with two reinforcing rings, then the **muzzle swell** to r 172 (z 840 to 905), a **flat muzzle face at z 914**, and in it a **ball of radius 105 (centre z 877) standing 68 above the face** (the face meets the ball at r 98.3): `%(K6B)s`. (The first version's top was a stepped spire and read as a lighthouse.) Black, worn, sRGB (26, 26, 28), roughness 0.6. Set in the granite sett apron or the cope with a 10 mm lead or mortar joint, 0.75 m behind the cope nose (Read). Wear: a bright rope groove polished into the barrel at z 480 to 520, paint gone to rust-brown on the head's upper rim and the flange, dents and chips.

### 5.7 K7: horn cleat (`cleat`): Judgement, no photograph reached

400 long, 110 wide, 126 high. **Plan**: a base plate 400 x 110 with its ends rounded R55 (a stadium), 22 thick, two 16 mm bolts 300 apart (nut across flats 24); a pedestal 96 along x and 124 across at its foot with rounded ends, 48 high, its section narrowing upward; **horns of round section, 32 diameter at the pedestal tapering to 22 at the tips**, the tips curving up to 126 above the base. Half outline of the elevation (x from the centre, z): `%(K7)s`. Black or bare iron, roughness 0.6; wear: rope polish under the horns, rust at the bolts. Fixed on a stone cope (the jetty's), not a timber fender.

## 6. Materials and colours

| material | sRGB | roughness (words, 0 to 1) | metal | use |
|---|---|---|---|---|
| iron_black_gloss | (24, 24, 26) | gloss, 0.35 | 0 | K1, K2 (the default paint, both caps) |
| iron_grey_satin | (88, 89, 91) | satin, 0.5 | 0 | K2: the one grey condition (BB_b's paint) |
| iron_black_matt | (24, 24, 26) | matt to satin, 0.55 | 0 | K5, K6 |
| bare_iron_foot | (64, 58, 52) | dull, 0.7 | 0 | paint loss at the foot of K1 (BGE_a: 4.5 times the body's lightness) |
| concrete_grey | (152, 150, 144) | dry, 0.9 | 0 | K3 |
| galvanised | (120, 122, 124) | dull sheen, 0.5 | 1 | K4 variant |
| rust | (110, 60, 32) | 0.85 | 0 | rust blooms (Judgement) |
| bright_steel | (150, 150, 152) | 0.4 | 1 | K5 nuts and studs |

The street recipe's present clutter bollard is baseColor linear 0.0046 (sRGB about 15) and roughness 0.55: darker and duller than the photographs' black gloss.

## 7. Wear and damage, summarised (the lines are under each kind)

Painted cast iron wears at the foot first (paint lost in flakes and speckles, grime banked up to 0.5 m), by scuffs at bag height, and by chips on the upper shaft; it does not rust visibly in these photographs and does not dent. Concrete stains and chips; steel tube dents, scrapes and rusts at the foot (Judgement). Seeds per instance: lean 0 to 2 degrees; paint fade 0 to 1; dirt height 80 to 600 mm; rust 0 to 1; chips 0 to 12; foot paint-loss height 0 to 120 mm; dents 0 to 2 (steel only).

## 8. The photographs-win disagreements, element by element

| element | book, standard or the repository | photograph | chosen |
|---|---|---|---|
| height of the street's cast bollard | the street recipe's clutter bollard is 0.765 high r 108 (a cannon-and-ball from a list text); the research says 90 to 120 cm, "older ones often about 90 cm (uncertain)" | K1 %(K1_H)s, K2 %(K2_H)s (K2b %(K2b_H)s) | the photographs; the 0.765 stand-in is replaced by K1 |
| the held `decorative_bollard_02` | 1.008 high, 0.201 across (a CC0 mesh) | K1 %(K1_H)s high, %(K1_baseD)s across | K1 |
| the form of the "cannon" | a cannon barrel with a ball | the photographed post is a plinth, a taper, one bead and a domed cap: a plain cousin; no cannon barrel is photographed | K1 for the street; K6b (Judgement) for the quay |
| the white band | "black paint, sometimes with a white band" (the research, uncertain) | no band on any bollard, in the underpass, the park, the estate or the marina | none |
| camera height | 1.6 m (the kerbs target); the first version of this target: 1.16, 1.22 and a pooled 1.15 at the wrong levels | 0.9 to 1.2 m at each bollard's own ground (section 3) | the anchors at the bollard's ground |
| set-back from the kerb | 0.5 m (the scene, the asset plan) | 0.33, 0.93, 0.91 m | 0.5 kept (a 2.0 m footway) |
| the bead and cap collar | an unribbed "tapered cylinder with rings and a half-sphere top" | one half-round bead at 0.506 H, a rounded cap collar, a quirk, a thin ring and a flattened dome (not a half-sphere: %(K1_dh)s high on r %(K1_dr)s) | the photograph |
| lean | 1 to 3 degrees (the asset plan) | 0.2 to 1.0 degree in the viewing plane | seeds 0 to 2 |
| the chain | the marina's spiked chain (Photo) | an ornamental docklands dress | a plain short-link chain on an unrestored quay |
| K2's paint | grey (BB_b, a 2019 London underpass) | black (US02_a); black was the 1990 norm | black default, grey one condition |

## 9. Variants the street needs

Two to four models a kind at most (the asset plan); a council fits one design to a street, so repeats are true. **Models**: K1 one, K2 two (K2a flat cap, K2b low cone and smaller), K3 one, K4 one, K5 one (with the plain chain or without), K6 two (bell, cannon), K7 one: 9 models. **Conditions**: three per model, as listed under each kind. On the street and its junction: K1 x 2 (one model, two condition seeds), K2 x 4 (K2a and K2b mixed), K3 x 2, K4 x 2. On the quay: K6 x 10, K5 x 4, K7 x 3.

## 10. The checks unit 3.4's automatic check must pass

`target.json` `checks` lists %(nchecks)s: each a name, what to measure, the expected value and the tolerance. The ones that matter from the street: K1 height %(K1_H)s +-50, plinth diameter %(K1_baseD)s +-14, collar bead's fullest diameter %(K1_beadD)s +-10 at z %(K1_bc)s +-30, neck diameter %(K1_neckD)s +-8, cap collar %(K1_capD)s +-8, dome rise %(K1_dh)s +-8; K2a height %(K2_H)s +-60, foot ring %(K2_ringD)s +-18, shaft diameter %(K2_d300)s at z 300 and %(K2_d900)s at z 900, collar band at 0.59 H +-0.03, %(K2_cp)s +-4 proud, cap overhang %(K2_ov)s +-4; K2b height %(K2b_H)s +-50, its cone cap; K5 height %(K5_H)s +-40, flange 286 +-16, four bolts on a 124 +-8 pitch circle, chain eyes at 420 and 840 +-30, the D-lug 55 x 40 x 18 with a 24 hole, a plain chain 13 mm bar with no spikes; K6a head overhang 70 +-15; K6b height 982 +-40, ball radius 105 +-15 standing 68 +-15 above the muzzle face, muzzle swell r 172 at z 914; the largest radial distance between a built outline and `profile_rz` at the same z at most 6 mm (K1), 7 mm (K2); lean seed 0 to 2 degrees; paint albedo within 10 of the sRGB values (K2 black by default); the worn-foot loss on that condition only; **no white, yellow or reflective band, no lettering, no crest, no maker's mark** on any mesh or texture; every street bollard 0.5 +-0.1 m behind the kerb face, at least 1.2 m of footway clear, 1.2 m in plan from every door centre, 1.5 m from a lamp column, 0.25 m from the crossover edge; ten on the street and junction at the four junction (x, y) of section 1; the quay's K6 at the kit's ten coordinates, K5 at x -69.5 y -40.5, -37.5, -34.5, -31.5 with chains only between the outer pairs, K7 at x -110.25 y -64, -58, -52.

## 11. What the target could not settle

* The camera heights (0.92 to 1.195 m, per panorama, each at its bollard's own ground) rest on brick gauges (75 mm modern, 73 to 79 mm Victorian), a line width and a paver size; every length is +-4 to +-7 % until a photograph with a measuring scale in the plane is reached. My own horizon measurements run up to 5 % under the fresh reviewer's on four walls; the reviewer's are adopted.
* Whether any of these bollards stood in a 1990 British street: every photograph is from 2019. K1's and K2's patterns are the long-lived cast pattern; their boroughs, makers and dates are not known; the grey paint of K2a is probably a 1990s to 2010s fitting (black is the default).
* K3 (concrete), K4 (steel tube), K6 (mooring bollards), K7 (cleat): no photograph in reach; their numbers are the kit's, the asset plan's or judgement.
* Whether a chain post (K5) belongs on a 1990 quay: its marina dates from the 1980s to 90s and its flange is bolted; the street uses a plain chain, not the photographed spiked one.
* The chain's sag and the D-lug's exact form (one cast lug through which an end link passes is assumed).
* Casting marks: none on K1 or K2; K5's one embossed mark is left blank.
* BGE_a (the second K1 casting) is not modelled: its plinth is about 140 high with a convex roll and its bead at 0.53 H.

## 12. What I would read once the network opens

Wikimedia Commons: the category "Bollards in the United Kingdom" and its cannon, mooring and concrete subcategories (1975 to 2000 photographs, the author and date on the file page); Geograph: 1980s and 1990s squares of dock and harbour towns with cast bollards, cleats and concrete posts (CC BY-SA, the date taken on each page); Historic England list entries 1202530 (Bristol, Floating Harbour quay wall and bollards, 1893) and 1272267 (Docks 1 to 6 quay walls and bollards) and the Kent and Derbyshire HER pages for cannon bollards; the Bristol Industrial Archaeological Society's Journal 3, Grahame Farr's 1970 paper on the quay bollards (types with sizes); BS 7263 and the Traffic Signs Manual's chapter on bollards and their set-backs; a 1980s highways standard detail for a precast and a cast bollard; the Hook sheet's own bollard, if it has one, at full size, and the street recipe's clutter bollard's reference photographs (Historic England's Queen Street, Leeds list text).

## 13. The previews (production/previews/cloud-week/refs/bollards/), credited

All crops are of the object only (the bollard and a 28 mm margin, 16 mm on the chain post so that a boat's lettering stays out, the rest of each elevation flat grey; the foot close-ups and ground plans show paving and kerb only: no cars, people, lettering, litter or bottles; K5's embossed mark is blurred). Photographs: Poly Haven, CC0, Andreas Mischok (S1 to S5); the drawings are this target's. The elevations are re-projected at the corrected camera heights.

| file | what |
|---|---|
| `ph-urban_street_01-us01_b-k1-elevation.jpg`, `...-k1-target-on-photo.jpg`, `...-foot-close.jpg`, `...-ground-plan.jpg` | S1: K1 main photograph (1.05 mm a pixel), the drawing laid on it (red outline, yellow axis, cyan z ticks every 100), the foot and its bark bed, the plan with a 0.5 m grid |
| `ph-bethnal_green_entrance-bge_a-k1-elevation.jpg`, `...-foot-close.jpg` | S2: the second K1 casting (evidence only, no overlay: it is not a model), the worn foot on block paving |
| `ph-birbeck_street_underpass-bb_b-k2-elevation.jpg`, `...-k2-target-on-photo.jpg`, `...-foot-close.jpg`, `...-ground-plan.jpg` | S3: K2a, outline, foot ring, plan (set-back 0.93 m) |
| `ph-urban_street_02-us02_a-k2-elevation.jpg`, `...-k2-target-on-photo.jpg`, `...-foot-close.jpg`, `...-ground-plan.jpg` | S4: K2b (black, low cone), outline, foot, plan |
| `ph-limehouse-lh_b-k5-elevation.jpg`, `...-k5-target-on-photo.jpg`, `...-foot-close.jpg`, `...-ground-plan.jpg` | S5: K5 with its chain eyes and four nuts, outline, flange, plan (the quay edge, the chain) |
| `target-drawing-sheet.jpg` | the drawings of K1 to K7 (elevation and plan), two rows |

Fitted on the photographs by `self_check.py` (a scale fitted on one dimension, the height or the collar; this tests the SHAPE: the scale is tested by the calibration anchors of section 3): %(fit)s.

## 14. Files

`TARGET.md` (this), `target.json`, `target_drawing.py`, `self_check.py`; the makers `bollard_data.py` (the hand-read numbers), `bollard_lib.py`, `make_target.py`, `make_previews.py` and `calibrate.py` (both need the panoramas), `make_doc.py`; `frames.json` (the elevations' frames) and `anchors.json` (the horizon anchors' raw rows).

## 15. What changed after the fresh review (the second and last try)

The first version failed review on 3 faults and 12 narrow points. Each is answered here; where the target now says something the reviewer did not ask for, it is because a number moved with the fix.

**Fault 1, camera heights taken at the wrong level (K2 11 to 20 % oversize, K1 3 % small).** Section 3 now measures every height at the bollard's own ground, with the step added, from anchors independent of the re-projection (the horizon method on brick walls, `calibrate.py`). K2a (BB_b) at 1.085 +-0.06 m at its footway: every z and r x 0.8897, height **%(K2_H)s**, foot ring %(K2_ringD)s across, collar band z %(K2_c0)s to %(K2_c1)s, cap overhang %(K2_ov)s; checks `K2_height` %(K2_H)s +-60, `K2_foot_ring_diameter` %(K2_ringD)s +-18, `K2_shaft_diameter_z300` %(K2_d300)s +-12, `K2_shaft_diameter_z900` %(K2_d900)s +-10, `K2_collar_proud` %(K2_cp)s +-4, `K2_cap_overhang` %(K2_ov)s +-4. K2b (US02_a) at 0.92 +-0.04 m from the two brick surfaces on its own footway (not the pooled 1.15): x 0.80, height **%(K2b_H)s**, foot ring %(K2b_ringD)s, z factor %(k2b_z)s and r factor %(k2b_r)s against K2a; new check `K2b_height` %(K2b_H)s +-50. K1 at 1.195 +-0.07 m at its bed level (the walls' 1.16 and 1.12 plus the 0.07 step, and the road line): scaled x 1.030, height **%(K1_H)s**, plinth %(K1_baseD)s; `K1_height` %(K1_H)s +-50, `K1_base_diameter` %(K1_baseD)s +-14. The "independent check" sentence and the self-check test "the two K2 photographs agree on the height" are deleted (they were circular: US02_a had the pooled height); a calibration test per panorama that recomputes each height from its raw anchors (and fails if the mean at the bollard's ground is outside the stated error) replaces them, and a test that K2a is not taller than K1. The warning for the kerbs-and-covers writer now says about 25 % high in urban_street_01 and about 55 % high in urban_street_02 at the road, not "30 %" for both. I could not show the reviewer wrong: my own horizon measurements on the same walls agree with theirs to 0 to 5 % in most places (BGE 0.96 against 1.03 to 1.04, the US01 gate pier 1.05 against 1.19 at the bed, the US02 wall 0.88 against 0.93), my US01 garden wall (1.23) and BB wall (1.05) and US02 pier (0.92) match, and the stated errors cover the spread.

**Fault 2, the quay placements.** K6 now at the south-quay kit's ten coordinates exactly (five north quay, two jetty, three east quay), K6b at the three quay ends; K7 at x -110.25, y -64, -58, -52 on the jetty's granite cope, long axis along y, beside the boat's berth (no timber fender); K5 at x -69.5, y -40.5, -37.5, -34.5, -31.5 with chains only between the outer pairs and the 3.0 m over the ladder open; the junction posts are the tangent points of the 8 m and 6 m returns moved 0.5 m along the footway normal, none on the 12 m outside return: (%(jn1x)s, %(jn1y)s), (%(jn2x)s, %(jn2y)s), (%(jn3x)s, %(jn3y)s), (%(jn4x)s, %(jn4y)s), recomputed live from the kit by `self_check.py` (checks `quay_K6_xy`, `quay_K5_xy`, `quay_K7_xy`, `junction_posts_xy`).

**Fault 3, K6b.** Replaced from (150, 760) with the muzzle swell to r 172, a flat muzzle face at z 914 and a ball of radius 105 (centre z 877) standing 68 above it; height **982**; new checks `K6b_height`, `K6b_ball` (105 +-15, standing 68 +-15) and `K6b_muzzle_swell`; `self_check.py` tests that every point above the face lies on the sphere.

**Narrow points.** (1) K1b dropped: one K1 model, the yard mouth uses it twice with two condition seeds; BGE_a stays as evidence with its fitted factors and no overlay. (2) `kinds.K2.base_diameter` is twice the foot ring's radius (%(K2_ringD)s). (3) K2b is `profiles_final.US02_a`, whole, with no mixed scales. (4) The D-lug: 55 high, 40 proud, 18 thick, a 24 mm hole centred 22 from the shaft face (Photo, +-30 %). (5) The chain is plain short link, 13 mm bar, no spikes; the spiked marina chain is an unused option. (6) K3 moved to flank the 1.0 m side passage (x 38.8 and 40.2, east), K4 to 41.5 and 44.0, and section 1 says why one street carries four kinds (four owners). (7) K2 is black by default, grey one condition. (8) K7's plan: a 400 x 110 base with R55 ends, a 96 x 124 pedestal, round horns 32 tapering to 22. (9) The foot paint loss is the worn-foot condition only. (10) New checks: K2b's cone cap, K6a's head overhang (70 +-15), K6b (fault 3), the quay and junction coordinates, the D-lug, the plain chain. (11) The self-check now calibrates each panorama independently (group B), and says that group C tests the shape, not the scale. (12) K4 is "anti-parking posts at the chandler's front".
'''
import math
sys.path.insert(0, HERE)
import bollard_lib as LB
CK = {c['name']: c for c in T['checks']}
P1_ = K['K1']['profile_rz']
PT1 = {p['name']: p for p in K['K1']['parts']}
M1 = {m['name']: m for m in K['K1']['mouldings']}
rz = lambda P, z: float(LB.r_of_z(P, [z])[0])
V2B = [v for v in K['K2']['variants'] if v['id'] == 'K2b'][0]
H2B = V2B['height']
jp = T['placements']['junction']['points']
DD = dict(K1_H='%.0f' % H1, K1_baseD='%.0f' % K['K1']['base_diameter'], K1_shaftD='%.0f' % (2 * PT1['shaft_lower']['r_max']), K1_underneckD='%.0f' % (2 * PT1['shaft_upper']['r_min']),
          K1_neckD='%.0f' % (2 * PT1['neck']['r_min']), K1_b0='%.0f' % M1['collar_bead']['z'][0], K1_b1='%.0f' % M1['collar_bead']['z'][1], K1_br='%.1f' % M1['collar_bead']['r_peak'],
          K1_bp='%.0f' % (M1['collar_bead']['r_peak'] - rz(P1_, M1['collar_bead']['z'][0])), K1_c0='%.0f' % M1['cap_collar']['z'][0], K1_c1='%.0f' % M1['cap_collar']['z'][1],
          K1_cr='%.1f' % M1['cap_collar']['r_peak'], K1_tr='%.0f' % M1['thin_ring']['r'], K1_dr='%.1f' % PT1['dome']['r_max'] if False else '%.1f' % rz(P1_, PT1['dome']['z0'] + 1.5),
          K1_dh='%.0f' % (H1 - PT1['dome']['z0']), K1_beadD='%.0f' % CK['K1_collar_max_diameter']['expected'], K1_capD='%.0f' % CK['K1_cap_collar_max_diameter']['expected'],
          K1_bc='%.0f' % CK['K1_collar_centre_z']['expected'],
          K2_H='%.0f' % H2, K2_ringD='%.0f' % K['K2']['base_diameter'], K2_d300='%.0f' % CK['K2_shaft_diameter_z300']['expected'], K2_d900='%.0f' % CK['K2_shaft_diameter_z900']['expected'],
          K2_c0='%.0f' % K['K2']['mouldings'][0]['z'][0], K2_c1='%.0f' % K['K2']['mouldings'][0]['z'][1], K2_cp='%.0f' % CK['K2_collar_proud']['expected'], K2_ov='%.0f' % CK['K2_cap_overhang']['expected'],
          K2b_H='%.0f' % H2B, K2b_ringD='%.0f' % CK['K2b_foot_ring_diameter']['expected'], K2b_vs='%.0f %% of' % (H2B / H2 * 100), K2b_rim='%.0f' % V2B['cone']['rim_r'],
          K2b_z0='%.0f' % V2B['cone']['rim_z'][0], K2b_z1='%.0f' % V2B['cone']['rim_z'][1], K2b_rise='%.0f' % V2B['cone']['rise'], K5_H='%.0f' % H5,
          jn1x='%.2f' % jp[0]['x_m'], jn1y='%.2f' % jp[0]['y_m'], jn2x='%.2f' % jp[1]['x_m'], jn2y='%.2f' % jp[1]['y_m'], jn3x='%.2f' % jp[2]['x_m'], jn3y='%.2f' % jp[2]['y_m'],
          jn4x='%.2f' % jp[3]['x_m'], jn4y='%.2f' % jp[3]['y_m'],
          k2_foot_r='%.1f' % max(r for r, z in P2 if z <= 50), k2_foot_d='%.0f' % (2 * max(r for r, z in P2 if z <= 50)), k2_collar_r='%.1f' % K['K2']['mouldings'][0]['r_peak'],
          k1b_z=VF['K1_second_casting_from_BGE_a']['z_factor'], k1b_r=VF['K1_second_casting_from_BGE_a']['r_factor'], k1b_rms=VF['K1_second_casting_from_BGE_a']['rms_mm'],
          k2b_z=VF['K2b_from_US02_a']['z_factor'], k2b_r=VF['K2b_from_US02_a']['r_factor'], k2b_rms=VF['K2b_from_US02_a']['rms_mm'],
          summary=T['summary_line'], sc=SC, H1=H1, H2=H2, H5=H5, nchecks=len(T['checks']),
           d_us01=P['urban_street_01']['date_taken'], d_bge=P['bethnal_green_entrance']['date_taken'], d_bb=P['birbeck_street_underpass']['date_taken'],
           d_us02=P['urban_street_02']['date_taken'], d_lh=P['limehouse']['date_taken'],
           K3=pts(K['K3']['profile_rz']), K4=pts(K['K4']['profile_rz']), K6A=pts(K['K6']['profile_rz']),
           K6B=pts([v for v in K['K6']['variants'] if v['id'] == 'K6b'][0]['profile_rz']), K7=pts(K['K7']['elevation_half_xz']),
           fit='; '.join('%s median %.1f mm, p90 %.1f mm, scale %.3f' % (k, v['median_abs_mm'], v['p90_abs_mm'], v['scale_fitted_on_one_dimension']) for k, v in fit.items()) or '(run self_check.py)')
for k_, v_ in DD.items():
    md = md.replace('%(' + k_ + ')s', str(v_)).replace('%(' + k_ + ')g', ('%g' % v_) if isinstance(v_, (int, float)) else str(v_))
md = md.replace('<<K1_ROWS>>', rows(K['K1']['profile_rz'])).replace('<<K1_PARTS>>', parts_table('K1'))
md = md.replace('<<K2_ROWS>>', rows(K['K2']['profile_rz'])).replace('<<K2_PARTS>>', parts_table('K2'))
md = md.replace('<<K5_ROWS>>', rows(K['K5']['profile_rz'])).replace('<<K5_PARTS>>', parts_table('K5'))
open(os.path.join(HERE, 'TARGET.md'), 'w', encoding='utf-8').write(md)
print('TARGET.md written,', len(md), 'characters')
