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

The target for the family "bollards on Quay Street and at its quay end", written from Poly Haven's CC0 London photographs (all 2019) and the repository's own numbers. Everything is millimetres unless a line says otherwise; the .glb is metres, z up, scale 1. `target.json` holds the same numbers for a script; `target_drawing.py` draws them (elevations, plans, the street's places, each kind laid on its photograph); `self_check.py` tests them against their own sources (last result: **%(sc)s**). `make_target.py`, `make_previews.py`, `make_doc.py` and `bollard_data.py` re-make the files from the hand-read numbers and the panoramas.

**Photograph kinds, in one breath.** K1 is a black cast-iron post, 1050 high, a plinth foot 196 across, one straight taper, one fat half-round bead at half height (0.506 H), a neck, a rounded cap collar and a flattened dome (Photo, two panoramas). K2 is a plain tapered iron post, 1180 high, a rolled foot ring %(k2_foot_d)s across, a thin collar band at 0.59 H and a flat or low-cone cap (Photo, two panoramas, in grey and in black). K5 is a bolted chain post, 1135 high, on a 286 flange with four nuts, two beads and a dome, with eyes at 420 and 840 for a spiked chain (Photo, one marina). K3 (concrete), K4 (steel tube), K6 (mooring bollards) and K7 (cleat) have NO photograph in reach and are judgement, the kit's or the asset plan's numbers, marked so everywhere.

## 1. Where on Quay Street bollards would have stood in 1990, and how many

The clutter research (street-clutter-1990, "Bollard (weak)") says: old cast-iron "cannon" bollards at terrace corners, alongside plain precast concrete ones; black paint, sometimes a white band (uncertain; no photograph shows one, so none is used); nothing reflective, stainless or gold. The asset plan wants "bollards at corners and the quay edge", 6 to 10 on the street, "two to four models a kind, because a council fits one design to a street". The scene file already puts two bollards at the yard mouth. So, in the street's frame (x along, 0 at the south end; z across, east positive; the kerb face at z = +-3.0; the footway 2.0 m):

| place | kind | count | x (m) | side | axis behind the kerb face | basis |
|---|---|---|---|---|---|---|
| the yard mouth, either side of the 3.0 m crossover (x 21.0 to 24.0) | K1 cast iron, domed | 2 | 20.7 and 24.3 | west | 0.5 m (z -3.5) | Read: the scene file already places them; Photo: the pattern stands at corners in two panoramas |
| the chandler's front (x 40 to 46), guarding the metal-refit window | K4 steel tube | 2 | 40.5 and 44.0 | east | 0.45 m (z +3.45) | Judgement: a 1980s shop-front guard; no photograph |
| the street's top end, where the kerbs climb and bend east | K3 concrete | 2 | 47.2 | both | 0.5 m (z +-3.5) | Judgement: "plain precast ones" at terrace corners (the clutter research) |
| the quay-end junction (atlas (400,320), x = -30): the four kerb-return tangent points | K2 plain iron | 4 | about -30 | both arms | 0.5 m | Judgement: corners; the south-quay kit's junction gives the points |
| **on the street and its junction** | | **10** | | | | the asset plan's 6 to 10 |
| the quay edge (north quay, 70 m south of the street end) | K6 mooring bollard (7 bell, 3 cannon) | 10 | -69.25, every 30 m | the quay | 0.75 m behind the cope nose | Read: the south-quay kit places ten; the cannon pattern is Judgement |
| the quay ladder's head (y -36) | K5 chain post, chain between | 4 | on the cope line, 3.0 m apart | the quay | 0.5 m behind the cope nose | Judgement (a Photo of the post, not of a quay) |
| the jetty's fender | K7 cleat | 3 | 6 m apart | the jetty | 0.1 m behind its edge | Judgement |

Never in front of a door or a lamp column, never in the crossover, never leaving less than 1.2 m of footway (the footway is 2.0 m: the axis at 0.5 m and a base radius of 0.1 leave 1.4). The photographs show set-backs of 0.33 m (K1 in the inside corner of a kerb build-out), 1.05 m (K2 on a 2.5 m footway) and about 1.25 m (K2 on a wide footway); 0.5 m is the scene's Read value, the right one for a 2.0 m footway (a bollard 450 to 600 mm back is the usual rule: Judgement), and is kept. The existing yard-mouth bollard at x 24.3 stands 0.52 m (in x) from the tea room's side door centre (24.822) but 1.5 m from the facade, at the kerb: it does not block the door and is kept (Read).

## 2. Sources

All photographs are Poly Haven's, CC0 (licence read at https://polyhaven.com/license on 9 October 2026: "All assets ... are licensed as CC0"), author Andreas Mischok, used for measuring only: not placed in the game, not traced into a texture, not fed to an image model. The cloud's network refused Wikimedia, Geograph, Flickr, archive.org, Historic England, British Listed Buildings, dimensions.com, pavingexpert, gov.uk, Hertfordshire, the Bristol Industrial Archaeological Society and every other site I tried (only Poly Haven answered): **no photograph from 1975 to 2000 was reached; every photograph is from 2019**, and for each the table says whether it shows the period object or a replacement and why it would look the same in 1990.

| id | URL (files via api.polyhaven.com/files/<id>, the 8k tone-mapped JPG) | date read | author, licence | date taken (lat, lon) | what it shows | used | period or replacement, and why the same in 1990 |
|---|---|---|---|---|---|---|---|
| S1 | https://polyhaven.com/a/urban_street_01 | 2026-10-09 | Andreas Mischok, CC0 1.0 | %(d_us01)s (51.528295, -0.053879) | a Bethnal Green street (east London): five or six black cast-iron bollards (four inspected: the same pattern), each at a corner of a granite kerb build-out and planted bed, a 75 mm-gauge brick wall | YES, K1 main (US01_b) | The pattern (plinth, taper, bead, domed cap) is the long-lived cast form and the paint is worn: the bollards are probably older than ten years but their date is unknown, so they may be 1980s to 2010s castings. They differ from 1990 in fresh gloss paint and a re-set build-out; no band, no reflective strip, no crest is visible. |
| S2 | https://polyhaven.com/a/bethnal_green_entrance | 2026-10-09 | Andreas Mischok, CC0 1.0 | %(d_bge)s (51.526915, -0.054044) | a park entrance: three or more of the same family on block paving, one with its foot paint mostly gone, a gate pier with a 75 mm brick gauge | YES, K1 second (BGE_a) | Block paving is 1990s to 2000s; the bollards' pattern is the same family, a little slimmer. Same caveat as S1. |
| S3 | https://polyhaven.com/a/birbeck_street_underpass | 2026-10-09 | Andreas Mischok, CC0 1.0 | %(d_bb)s (51.525806, -0.056277) | a street under a railway arch: about ten grey plain tapered bollards on a concrete-kerbed footway, double yellow lines | YES, K2 main (BB_b) | Plain tapered iron posts were fitted from the 1970s; this grey paint and the flat top may be a 1990s to 2000s fitting; the arch lights light it orange, so its grey is read as a neutral mid-dark grey. |
| S4 | https://polyhaven.com/a/urban_street_02 | 2026-10-09 | Andreas Mischok, CC0 1.0 | %(d_us02)s (51.526655, -0.056465) | an estate road: the same plain tapered bollard in black with a low cone cap, on flags | YES, K2 second (US02_a) | A 1970s to 80s housing estate; the bollard may be older than the 2000s window frames beside it. Same caveat. |
| S5 | https://polyhaven.com/a/limehouse | 2026-10-09 | Andreas Mischok, CC0 1.0 | %(d_lh)s (51.510606, -0.036324) | a marina basin (Limehouse): bolted cast-iron chain posts, a spiked chain, resin-bound gravel, clay paviors, floating pontoons | YES, K5 (LH_b) | The marina is a 1980s to 90s redevelopment; the bolted flange and the spiked chain may be later than 1990; kept as the only photographed British quay-edge ironwork. |
| S6 | the repository: production/specs/vignette-scene.json, vignette-pieces.json; production/cloud-week/targets/SCENE-SLOTS.md, kerbs-and-covers/TARGET.md, shopfronts/target.json; production/research/asset-plan/3-FURNITURE-PROPS-FOOD.md; street-clutter-1990/SUMMARY-2026-09-29.md; south-quay/METHOD-2026-10-06.md; tools/art-recipes/south-quay/south_quay_geom.py; production/assets/street/clutter/bollard.glb | 2026-10-09 | the project | 2026-09-29 to 2026-10-09 | the street's layout, its levels, its furniture, the present stand-ins (0.765 and 1.008 m), the quay kit's bollard | YES (Read numbers) | n/a |
| S7 | WebSearch result summaries, 9 October 2026: a cannon-bollard history (quay guns, Napoleonic surplus), manufacturer heights (1100, 1140, 1520 mm, "around 1 m" for visual accessibility), a 2011 county standard drawing for a 230 mm precast bollard at 600 or 915 above ground, a 160 x 750 concrete post, Bristol's 1893 quay bollards, Charlestown's upturned cannon barrel | 2026-10-09 | third-party pages (reached only as summaries) | n/a | leads | LEADS ONLY: no number taken | n/a |

**Looked at and left out.** adams_place_bridge, cambridge, canary_wharf, leadenhall_market, urban_street_03 and urban_street_04 show no bollard that is a street bollard (a keep-left sign post in 04 is a sign); docklands_01 and docklands_02 are Dublin (coordinates 53.346, -6.238), not Britain, and were not used. Poly Haven's catalogue (2,384 assets, searched 9 October) has no bollard, cleat, mooring post or chain-post model (its modular wooden pier and lateral sea marker are not what is wanted). ambientcg.com answered its home page; no bollard asset was looked for there.

**Unreached** (a page that refused is not evidence; nothing was taken from any of these): Wikimedia Commons, Geograph, Flickr, archive.org, HathiTrust, Historic England (list entries 1202530 and 1272267), British Listed Buildings, the Bristol Industrial Archaeological Society's PDF, dimensions.com, pavingexpert, gov.uk, a county highways PDF, Sketchfab, Pexels, Unsplash (all refused or not resolvable); WebFetch of two PDFs failed to resolve the host.

## 3. How the photographs were measured, and why the camera height is not 1.6 m

Each panorama (8192 x 4096) is re-projected with numpy to a flat, square-on elevation of one bollard: a vertical plane through its axis, perpendicular to the line of sight, 1 mm a pixel (the native resolution is 2.5 mm a pixel at 3 m, 5 mm at 7 m, so the pictures are up-sampled and soft). The foot of the base gives the bearing and the distance (from the depression angle and the camera height); the base radius puts the axis 0.1 m behind the foot's front edge. **Every length then scales with the camera height**, which the panoramas do not give. The previous target writers took 1.6 m (proved, they said, by a 75 mm line on a different panorama). Here the height is found per panorama from objects of known size in the same plane (anchors in `target.json` `calibration.anchors`, recomputed by `self_check.py`):

| panorama (session) | anchors | camera height used |
|---|---|---|
| urban_street_01 (18 Aug 2019) | a 75 mm brick course reads 75.5 mm at 1.15 m (so 1.14); the single yellow line reads 98 mm at 1.6 m (so 1.22 for 75 mm) | 1.16 +-0.06 |
| bethnal_green_entrance (18 Aug) | brick course 92 mm at 1.15 (0.94); stretcher module 255 for 225 (1.02) | 1.02 +-0.08 |
| birbeck_street_underpass (18 Aug) | each line of the double yellow reads 97 mm at 1.6 (1.24 for 75 mm) | 1.22 +-0.10 |
| urban_street_02 (18 Aug) | none of its own (its brick is not a 75 mm gauge) | 1.15 +-0.12 (pooled) |
| limehouse (19 May) | a clay paver (200 x 100 with 5 joints) reads 146 x 280 at 1.6 (1.15 and 1.17) | 1.17 +-0.06 |

The independent check that this is right: the two K2 bollards (Birbeck at its 1.22 m, the estate road at the pooled 1.15 m) come out 1180 and 1188 high, with the collar at 0.587 and 0.592 of the height; the two K1 bollards come out 1050 (at 1.16) and 1014 (at 1.02), 3.5 % apart. At 1.6 m K1 would be 1.45 m tall and K2 1.55 to 1.65 m, which no street bollard is. **Every number below is +-6 to +-10 % in absolute size** (the proportions are exact to the pixel). **A warning for the kerbs-and-covers target**: it uses 1.6 m for urban_street_01 and urban_street_02 (the Bethnal Green session); these anchors give 1.0 to 1.2 m, so its mitred-corner and tarmac-cover numbers from those two panoramas are probably 30 % too large (the 75 mm-gauge wall in urban_street_01 reads 105 mm at 1.6 m).

Other methods: `edge_residuals` in `bollard_lib.py` finds the strongest edge within +-12 mm of each predicted edge; ground plans (the z = 0 plane, axis at the centre) give set-backs; widths and heights are read on gridded crops at 3 x (error +-1.5 mm in the picture, +-3 mm with the soft edges). A casting seam, a fluting or a mark would show at 5 mm a pixel only if 1 mm deep: none shows (the shaft's vertical streaks are reflections: a contrast-stretched crop of BGE_a shows no regular flutes).

## 4. Frame, pivot, glb

* Profiles are (r, z): r the radius from the axis, z up from the ground at the foot; each runs from (0,0) up the outline to the axis at the top (a lathe). Elevation polygons mirror the profile about the axis.
* **Pivot**: the centre of the base on the ground. On the footway that is the flag top, +120 mm above the channel top (the kerbs target's frame: the kerb face line at y = 0, the kerb top +125); on the quay the apron, level with the kerb top. The axis stands at y = -500 mm toward the footway.
* **glb**: metres, z up, scale 1, one mesh per variant; bolts, chain eyes and chains as separate meshes of the same piece; **no text, no decal with lettering, no crest, no monogram, no band** on any mesh or texture.
* The photographs' z = 0 is the ground at the axis: the front-bottom edge of a base appears 50 to 55 mm BELOW z = 0 in an elevation (it is nearer the camera than the axis), so the drawing's foot sits "above" the photographed foot in the overlays by that much.

## 5. The target, kind by kind

Every number carries its kind: **Read** (printed in the repository), **Photo** (measured on a photograph: method in section 3, +-6 to +-10 % in size), **Derived**, **Judgement** (a trade or period guess, said so).

### 5.1 K1: cast-iron street bollard, domed head, one collar bead (`cast_iron_domed`)

Height **%(H1)g** (Photo: US01_b %(H1)g at 1.16 m; BGE_a 1014 at 1.02 m); plinth diameter 195.7; a stout post: shaft diameter 158 at the shoulder, 115 under the neck, 107 at the neck. Profile (r, z), authoritative in `target.json` `kinds.K1.profile_rz`:

<<K1_ROWS>>

<<K1_PARTS>>
* **Edges**: no sharp edges; every step rounded (R4 to R8) or coved; the foot has a 3 mm chamfer. No flats, no facets, no fluting, no beading on the bead. [Photo]
* **Mouldings**: the **collar bead** (z 497 to 562, r peak 83.2, 14 proud of the taper, half-round, fuller below its middle, its underside the drip; a thin fillet ring about 4 high and 1 proud on its top edge); the **cap collar** (z 948 to 976, r peak 68.1, a fat rounded ring with a flat underside at the neck); a 4 mm **quirk** at z 976 to 980; a **thin ring** 15 high at r 59; the **dome** (r 51.4 at its foot, 53 high, flattened). The plinth's top edge is R6 then a cove 18 high to the shaft. [Photo US01_b]
* **Seams**: none visible at this resolution; a faint parting line down each side may be added at 0.3 mm (Judgement). **Fixings**: none; rooted. **Marks**: none: no maker, council, crest, monogram or lettering was visible on any of the five or six bollards of S1 or the three or four of S2.
* **Root, how it meets the ground**: on flags or block paving the plinth stands directly on it; the paving is cut round it or butts it with a 5 to 15 mm dark grit joint, no mortar fillet, no collar plate (Photo BGE_a). In a planted bed it stands on the soil with bark chips and leaves banked about 20 mm against the plinth (Photo US01_b).
* **Paint**: black, sRGB **(24, 24, 26)** (measured medians 38, 10, 15 and 18 across four tone-mapped panoramas: 24 chosen), gloss, roughness **0.35** (the sky shows in the dome, the bead and the shoulder), metal 0. **No white or yellow band, no reflective strip, no sleeve** (none in any photograph; the research says reflective bands are wrong for 1990).
* **Wear and damage as photographed**: one pale vertical paint chip 15 x 65 mm at z 70 to 135 on one side of US01_b (primer or filler showing); on BGE_a the lower 110 mm of the plinth bare grey-brown metal in a speckled pattern over 60 to 70 % of its area, sRGB (64, 58, 52) against the body's black; fine scratches and dull rub marks below 0.5 m; dust and tyre grime on the plinth and lower shaft, cleaner above 0.7 m; a lean of about 1 degree in the viewing plane (0.7 to 1.6 degrees fitted on the two). No rust streaks, no graffiti, no stickers, no dents.
* **Variants**: K1a (the profile above) and K1b (BGE_a: every z x %(k1b_z)s and every r x %(k1b_r)s of K1a, rms %(k1b_rms)s mm over 15 half widths; its collar is about 4 % higher, 0.53 H, and its plinth about 20 % taller: not modelled, inside the checks' tolerance); conditions: glossy repaint with a few scuffs; worn foot (plinth paint 60 to 70 % gone); dull and chalky with a rust bloom at the foot (Judgement).

### 5.2 K2: plain tapered iron bollard, collar band at 0.59 H (`cast_iron_plain`)

Height **%(H2)g** (Photo: BB_b %(H2)g at 1.22 m; US02_a 1188 at 1.15 m), foot ring %(k2_foot_d)s across. Profile in `target.json` `kinds.K2.profile_rz`:

<<K2_ROWS>>

<<K2_PARTS>>
* **Edges**: rounded or coved throughout; the cap plate's edge R3. **Mouldings**: the **collar band** (z 674 to 713, r peak %(k2_collar_r)s, only 8 proud of the taper, a thin rounded band with no beads either side, at 0.587 H on BB_b and 0.592 H on US02_a); the **rolled foot ring** (z 0 to 49, r peak %(k2_foot_r)s, its top sloping in to the shaft, a lighter rub mark round it). **Cap**: BB_b a flat plate overhanging the shaft by 6 and domed 5 mm (K2a); US02_a a rim ring (r 80, z 1148 to 1166) under a low cone rising 22 to the apex (K2b, `profiles_final.US02_a`).
* **Seams, fixings, marks**: none visible. A thin dark scratch about 40 mm long at z 840 to 880 on BB_b is damage, not a seam. **Root**: the foot ring stands on the paving or tarmac, a darker 20 mm ring of dirt round it, no collar plate.
* **Paint**: grey variant sRGB **(88, 89, 91)** satin, roughness 0.5 (the measured median (97, 77, 70) is under the underpass's orange light, lightness 81: neutralised, Judgement); black variant (24, 24, 26), semi-gloss; metal 0. The orange rim seen on BB_b's cap is the underpass light on the plate, not brass. **No band.**
* **Wear and damage as photographed**: a lighter, scuffed ring round the foot ring; a few chips and thin dark scratches on the upper shaft (BB_b); a tan dust line at the foot; no rust, no dents; lean 0.2 to 1.0 degree.
* **Variants**: K2a (flat cap, grey) and K2b (low cone, black: z x %(k2b_z)s, r x %(k2b_r)s of K2a over the shaft, rms %(k2b_rms)s mm over 18 half widths); conditions: clean satin; scuffed with chips; black gloss.

### 5.3 K3: round precast concrete bollard (`concrete_round`): JUDGEMENT, no photograph reached

Height 850, foot diameter 250, top 200 (leads only: a county drawing's 230 mm precast unit at 600 or 915 above ground, a 160 x 750 post, "millions of concrete bollards" in the 1970s). Profile: `%(K3)s`. A tapered cylinder, a 20 mm chamfer into a shallow dome (rise 18); two vertical mould lines 180 degrees apart (1 mm) and a horizontal pour line at z 400 +-60. Bare concrete, sRGB (152, 150, 144), roughness 0.9, never painted, no band. Cast into a footing; the flags butt it with a 10 mm tarmac or mortar fillet. Wear: a dark grime band to 150 mm, rain streaks below the chamfer, a darker top, a chipped top arris with aggregate showing, a rust-coloured stain 40 mm wide from a cut-off lifting eye. One model, three conditions.

### 5.4 K4: steel tube bollard with a welded cap (`steel_tube`): JUDGEMENT, no photograph reached

A 114.3 mm tube (the asset plan's 60 to 114 mm), 1000 above ground, a welded shallow dome (rise 18) with a 2 mm weld bead, a vertical weld seam up the tube. Profile: `%(K4)s`. Painted black gloss (24, 24, 26, metal 0, roughness 0.4) or dull galvanised (120, 122, 124, metal 1). Set in a footing flush with the paving, a 15 mm tarmac fillet round it. **No band, no sleeve** (reflective bands are later). Wear: scuffs, a rust bloom 100 mm high at the foot, a dent and scrape at 0.4 to 0.6 m, a lean up to 2 degrees. One model: black, galvanised, black with a rusted foot.

### 5.5 K5: bolted cast-iron chain post (`chain_post`)

Height **%(H5)g** (Photo LH_b, +-6 %), flange 286. Profile in `target.json` `kinds.K5.profile_rz`:

<<K5_ROWS>>

<<K5_PARTS>>
* **Fixings**: four hex nuts on studs through the flange, 22 across flats, 14 high, studs 14 above the nuts, on a pitch circle of radius 124, at 45, 135, 225 and 315 degrees to the line of posts (the photograph shows two at the sides and one at the front); nuts and studs bright steel (150, 150, 152, metal 1) with dull rust at the threads. **Chain eyes**: a cast D-lug on each side of the shaft at z **420 and 840** (+-30), in the line of the posts; the chain's end link passes through it.
* **The chain** (Photo, link sizes +-15 %): post spacing 3.0 m (read off the panorama: 3.06 m between two posts); a link of bar 12, inner length 55, inner width 25, outer 79 x 49, pitch 55; every second link carries two cast conical spikes 28 long, 8 at the base, at right angles to the link's plane; mid-span sag of 150 (Judgement); two chains, at the eye heights. The chain is black, rubbed bright at the link contacts.
* **Paint**: black, sRGB (24, 24, 26) with a blue sheen from the sky (measured (17, 19, 27)), matt to satin and chalky, roughness 0.55, metal 0. **Marks**: an embossed mark about 45 mm long runs up the right side of the shaft at z 80 to 110 and is unreadable at this resolution: **LEAVE BLANK**, no maker's mark; the previews blur it. **Root**: the flange stands on resin-bound gravel (Photo) or the apron, the nuts proud.
* **Wear**: dust on the flange, pale dry splash marks to 0.2 m, the chain rubbed bright at its contacts; no rust on the casting, no graffiti. One model, with or without chain.

### 5.6 K6: quay mooring bollards (`mooring_bollard`): Read for the bell pattern, Judgement otherwise; no photograph reached

K6a, the **bell bollard** of the south-quay kit (Read from `south_quay_geom.py`): 720 high, a flange r 250 (40 thick, then a cone), a barrel r 150 tapering to 130 at z 510, a head flaring to r 220 at z 630 that overhangs the barrel by 70, then a dome: `%(K6A)s`. K6b, an **upturned cannon barrel** (a Charlestown lead; Judgement): 965 high, r 190 at the foot tapering to 150, two reinforcing rings and a ball top: `%(K6B)s`. Black, worn, sRGB (26, 26, 28), roughness 0.6. Set in the granite sett apron or the cope with a 10 mm lead or mortar joint, 0.75 m behind the cope nose (Read). Wear: a bright rope groove polished into the barrel at z 480 to 520, paint gone to rust-brown on the head's upper rim and the flange, dents and chips.

### 5.7 K7: horn cleat (`cleat`): Judgement, no photograph reached

400 long, 110 wide, 126 high; a base 400 x 110 x 22 with two 16 mm bolts 300 apart (nut across flats 24), a pedestal 96 wide and 48 high, horns tapering from 32 to 22 thick with their tips curving up to 126 above the base. Half outline (x from the centre, z): `%(K7)s`. Black or bare iron, roughness 0.6; wear: rope polish under the horns, rust at the bolts.

## 6. Materials and colours

| material | sRGB | roughness (words, 0 to 1) | metal | use |
|---|---|---|---|---|
| iron_black_gloss | (24, 24, 26) | gloss, 0.35 | 0 | K1, K2b |
| iron_grey_satin | (88, 89, 91) | satin, 0.5 | 0 | K2a |
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
| height of the street's cast bollard | the street recipe's clutter bollard is 0.765 high r 108 (a cannon-and-ball from a list text); the research says 90 to 120 cm, "older ones often about 90 cm (uncertain)" | K1 %(H1)g, K2 %(H2)g | the photographs; the 0.765 stand-in is replaced by K1 |
| the held `decorative_bollard_02` | 1.008 high, 0.201 across (a CC0 mesh) | K1 1050 high, 196 across | K1 |
| the form of the "cannon" | a cannon barrel with a ball | the photographed post is a plinth, a taper, one bead and a domed cap: a plain cousin; no cannon barrel is photographed | K1 for the street; K6b (Judgement) for the quay |
| the white band | "black paint, sometimes with a white band" (the research, uncertain) | no band on any bollard, in the underpass, the park, the estate or the marina | none |
| camera height | 1.6 m (the kerbs target) | the anchors give 1.0 to 1.22 m | the anchors (section 3) |
| set-back from the kerb | 0.5 m (the scene, the asset plan) | 0.33, 1.05, 1.25 m | 0.5 kept (a 2.0 m footway) |
| the bead and cap collar | an unribbed "tapered cylinder with rings and a half-sphere top" | one half-round bead at 0.506 H, a rounded cap collar, a quirk, a thin ring and a flattened dome (not a half-sphere: 53 high on r 51) | the photograph |
| lean | 1 to 3 degrees (the asset plan) | 0.2 to 1.0 degree in the viewing plane | seeds 0 to 2 |

## 9. Variants the street needs

Two to four models a kind at most (the asset plan); a council fits one design to a street, so repeats are true. **Models**: K1 two (K1a, K1b), K2 two (flat grey cap, low-cone black cap), K3 one, K4 one, K5 one (with or without chain), K6 two (bell, cannon), K7 one: 10 models. **Conditions**: three per model, as listed under each kind. On the street and its junction: K1 x 2 (the same model twice, K1a and K1b on the two sides of the yard mouth is allowed), K2 x 4, K3 x 2, K4 x 2. On the quay: K6 x 10, K5 x 4, K7 x 3.

## 10. The checks unit 3.4's automatic check must pass

`target.json` `checks` lists %(nchecks)s: each a name, what to measure, the expected value and the tolerance. The ones that matter from the street: K1 height 1050 +-40, plinth diameter 196 +-14, collar bead's fullest diameter 166 +-10 at z 531 +-30, neck diameter 107 +-8, cap collar 136 +-8, dome rise 53 +-8; K2 height 1180 +-50, foot ring %(k2_foot_d)s +-16, collar band at 0.59 H +-0.03, 8 +-4 proud; K5 height 1135 +-40, flange 286 +-16, four bolts on a 124 +-8 pitch circle, chain eyes at 420 and 840 +-30; the largest radial distance between a built outline and `profile_rz` at the same z at most 6 mm (K1), 7 mm (K2); lean seed 0 to 2 degrees; paint albedo within 10 of the sRGB values; **no white, yellow or reflective band, no lettering, no crest, no maker's mark** on any mesh or texture; every street bollard 0.5 +-0.1 m behind the kerb face, at least 1.2 m of footway clear, 1.2 m in plan from every door centre, 1.5 m from a lamp column, 0.25 m from the crossover edge; ten on the street and junction; the quay's 10, 4 and 3.

## 11. What the target could not settle

* The camera heights (1.0 to 1.22 m, per panorama) rest on a brick gauge, a line width and a paver size; every length is +-6 to +-10 % until a photograph with a measuring scale in the plane is reached.
* Whether any of these bollards stood in a 1990 British street: every photograph is from 2019. K1's and K2's patterns are the long-lived cast pattern; their boroughs, makers and dates are not known; the grey paint of K2a may be a 1990s fitting.
* K3 (concrete), K4 (steel tube), K6 (mooring bollards), K7 (cleat): no photograph in reach; their numbers are the kit's, the asset plan's or judgement.
* Whether a chain post (K5) belongs on a 1990 quay: its marina dates from the 1980s to 90s and its flange is bolted.
* The chain's sag, the spikes' exact form and the two eyes' shape (a D-lug is assumed under a chain's end link).
* Casting marks: none on K1 or K2; K5's one embossed mark is left blank.
* The K1b profile is a scaled K1 (rms %(k1b_rms)s mm over 15 half widths); BGE_a's collar and plinth heights differ by 4 and 20 %.

## 12. What I would read once the network opens

Wikimedia Commons: the category "Bollards in the United Kingdom" and its cannon, mooring and concrete subcategories (1975 to 2000 photographs, the author and date on the file page); Geograph: 1980s and 1990s squares of dock and harbour towns with cast bollards, cleats and concrete posts (CC BY-SA, the date taken on each page); Historic England list entries 1202530 (Bristol, Floating Harbour quay wall and bollards, 1893) and 1272267 (Docks 1 to 6 quay walls and bollards) and the Kent and Derbyshire HER pages for cannon bollards; the Bristol Industrial Archaeological Society's Journal 3, Grahame Farr's 1970 paper on the quay bollards (types with sizes); BS 7263 and the Traffic Signs Manual's chapter on bollards and their set-backs; a 1980s highways standard detail for a precast and a cast bollard; the Hook sheet's own bollard, if it has one, at full size, and the street recipe's clutter bollard's reference photographs (Historic England's Queen Street, Leeds list text).

## 13. The previews (production/previews/cloud-week/refs/bollards/), credited

All crops are of the object only (the bollard and a 28 mm margin, 16 mm on the chain post so that a boat's lettering stays out, the rest of each elevation flat grey; the foot close-ups and ground plans show paving and kerb only: no cars, people, lettering, litter or bottles; K5's embossed mark is blurred). Photographs: Poly Haven, CC0, Andreas Mischok (S1 to S5); the drawings are this target's.

| file | what |
|---|---|
| `ph-urban_street_01-us01_b-k1-elevation.jpg`, `...-k1-target-on-photo.jpg`, `...-foot-close.jpg`, `...-ground-plan.jpg` | S1: K1 main photograph (1 mm a pixel), the drawing laid on it (red outline, yellow axis, cyan z ticks every 100), the foot and its bark bed, the plan with a 0.5 m grid |
| `ph-bethnal_green_entrance-bge_a-k1-elevation.jpg`, `...-k1-target-on-photo.jpg`, `...-foot-close.jpg` | S2: K1 second, K1b outline, the worn foot on block paving |
| `ph-birbeck_street_underpass-bb_b-k2-elevation.jpg`, `...-k2-target-on-photo.jpg`, `...-foot-close.jpg`, `...-ground-plan.jpg` | S3: K2 main (1.1 mm a pixel), outline, foot ring, plan (set-back 1.05 m) |
| `ph-urban_street_02-us02_a-k2-elevation.jpg`, `...-k2-target-on-photo.jpg`, `...-foot-close.jpg`, `...-ground-plan.jpg` | S4: K2b (black, low cone), outline, foot, plan |
| `ph-limehouse-lh_b-k5-elevation.jpg`, `...-k5-target-on-photo.jpg`, `...-foot-close.jpg`, `...-ground-plan.jpg` | S5: K5 with its chain eyes and four nuts, outline, flange, plan (the quay edge, the chain) |
| `target-drawing-sheet.jpg` | the drawings of K1 to K7 (elevation and plan), two rows |

Fitted on the photographs by `self_check.py` (a scale fitted on one dimension, the height or the collar): %(fit)s.

## 14. Files

`TARGET.md` (this), `target.json`, `target_drawing.py`, `self_check.py`; the makers `bollard_data.py` (the hand-read numbers), `bollard_lib.py`, `make_target.py`, `make_previews.py` (needs the panoramas), `make_doc.py`; `frames.json` (the elevations' frames).
'''
DD = dict(k2_foot_r='%.1f' % max(r for r, z in P2 if z <= 50), k2_foot_d='%.0f' % (2 * max(r for r, z in P2 if z <= 50)), k2_collar_r='%.1f' % max(r for r, z in P2 if 640 <= z <= 720),
          k1b_z=VF['K1b_from_BGE_a']['z_factor'], k1b_r=VF['K1b_from_BGE_a']['r_factor'], k1b_rms=VF['K1b_from_BGE_a']['rms_mm'],
          k2b_z=VF['K2b_from_US02_a']['z_factor'], k2b_r=VF['K2b_from_US02_a']['r_factor'], k2b_rms=VF['K2b_from_US02_a']['rms_mm'],
          summary=T['summary_line'], sc=SC, H1=H1, H2=H2, H5=H5, nchecks=len(T['checks']),
           d_us01=P['urban_street_01']['date_taken'], d_bge=P['bethnal_green_entrance']['date_taken'], d_bb=P['birbeck_street_underpass']['date_taken'],
           d_us02=P['urban_street_02']['date_taken'], d_lh=P['limehouse']['date_taken'],
           K3=pts(K['K3']['profile_rz']), K4=pts(K['K4']['profile_rz']), K6A=pts(K['K6']['profile_rz']),
           K6B=pts(K['K6']['variants'][1]['profile_rz']), K7=pts(K['K7']['elevation_half_xz']),
           fit='; '.join('%s median %.1f mm, p90 %.1f mm, scale %.3f' % (k, v['median_abs_mm'], v['p90_abs_mm'], v['scale_fitted_on_one_dimension']) for k, v in fit.items()) or '(run self_check.py)')
for k_, v_ in DD.items():
    md = md.replace('%(' + k_ + ')s', str(v_)).replace('%(' + k_ + ')g', ('%g' % v_) if isinstance(v_, (int, float)) else str(v_))
md = md.replace('<<K1_ROWS>>', rows(K['K1']['profile_rz'])).replace('<<K1_PARTS>>', parts_table('K1'))
md = md.replace('<<K2_ROWS>>', rows(K['K2']['profile_rz'])).replace('<<K2_PARTS>>', parts_table('K2'))
md = md.replace('<<K5_ROWS>>', rows(K['K5']['profile_rz'])).replace('<<K5_PARTS>>', parts_table('K5'))
open(os.path.join(HERE, 'TARGET.md'), 'w', encoding='utf-8').write(md)
print('TARGET.md written,', len(md), 'characters')
