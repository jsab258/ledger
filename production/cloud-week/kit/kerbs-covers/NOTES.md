# Kerbs, channel, crossover, gully grates and covers (kit piece 3.7): build notes

12 October 2026, cloud week 42, built by the coordinating session from `production/cloud-week/targets/kerbs-and-covers/target.json` with no departure: `build_kerbs.py` (about 8 s), `check_kerbs.py` (67 of 67 in `checks/check_v1.json`) and `render_kerbs.py` (the two review views).

**Built** (one .glb each in `production/assets/cloud-week/kerbs-covers/`, metres, z up, scale 1, in the target's frame: x along the kerb, y across with the face line at y 0 and + toward the carriageway, z up from the top of the channel setts; pivots as the target gives them):

| File | Triangles | What it is |
|---|---|---|
| `kerb_granite.glb` | 100 | one dressed granite block 900 long: the half-battered face (vertical to 45, back 20 by 90), the R25 top arris, a flat top to the back at -170, buried to -140 (255 deep); the end arrises eased 10 |
| `kerb_concrete.glb` | 108 | one precast block 915 long, 95 up, 125 across, the R50 bull-nose over the top 50, 255 deep; end arrises eased 3 |
| `channel_setts.glb` | 740 | a 1.2 m run of the two granite courses (104 and 100 across, 204 in all), setts 120 to 210 long (mean about 160) in running bond, joints 11, tops domed 4 with a 3 mm scatter and the far course up to 5 lower where worn, the mortar recessed 8; three sett materials by name |
| `channel_concrete.glb` | 44 | the concrete channel block 915 long, 255 wide, 125 deep, beside the concrete kerb |
| `crossover_A.glb` | 1,464 | the dropped crossing at 3.0 m: two granite end blocks, two flank strips (140 x 663, top 110), the concrete ramp (rise 98 over 721, x +-1488, back edge at y -845), the lip row of 19 setts (top 12), 12 mm joints |
| `gully_grate_A.glb` | 428 | the street's grate, 440 x 290, 45 deep, eight slots 26 x 255 at pitch 51 (22 at the foot), open fraction 0.416; with the gully pot (300 deep, black) under it |
| `gully_grate_B.glb` | 516 | the optional oval grate, 355 x 325, seven slots 20 wide trimmed to 91, 182, 255, 288, 255, 182, 91, two lifting holes 18 across at x +-166; the pot |
| `cover_stud_square.glb` | 1,500 | 600 square, frame 12, two triangular leaves on a diagonal joint 3 wide, a 10 x 10 lattice of square studs 28 on a 59 pitch, 3 high, the studs the joint crosses cut to half-studs, a 12 keyhole in each leaf, the blank raised boss 50 x 25 x 2 |
| `cover_round_600.glb` | 2,772 | frame 690 across and 68 deep, lid 590, the basket-lug tread (lugs 36 x 10.5 x 2.5, cell 71.4 x 83.5, the plain rim 25) |
| `cover_recessed_footway.glb` | 1,500 | 1060 x 600: the flange 40 level with the flags, the ledge 60 stepped 11 down, the infill 860 x 400 (top 8 under the flags, its edge stepped for the 22 chamfer), lugs on the frame (two staggered rows on the long sides, three columns at the left end, two at the right) |
| `cover_recessed_road.glb` | 108 | 645 x 670, frame 25, the tarmac infill with its 10 hairline |
| `cover_road_double_leaf.glb` | 8,688 | 1710 x 570, two leaves with a 15 gap, studs 17 across turned 45 degrees on a pitch of 31, the edge margin 28 (the largest file: 610 KB) |
| `service_stopcock.glb`, `service_gas.glb`, `service_telecom.glb` | 784, 148, 140 | the three small footway covers (Judgement: no photograph reached), all blank |
| `review_scene.glb` | 14,248 | NOT a kit piece: the pieces placed on a flat footway and road for the two review pictures (seven granite blocks, four concrete, the channel, the grate, the round cover, the stud cover, the crossover at x 8 to 12.8 m) |

Material slots are named for what they are (the target's names): `granite_grey`, `granite_blue_grey`, `granite_pink_grey`, `sett_pale_worn`, `sett_dull`, `concrete_kerb`, `concrete_ramp`, `flag_pale`, `cast_iron_grate`, `cast_iron_cover`, `mortar_pale`, `bitumen_joint`, `tarmac_infill`, `pot_black`. The colours are clean-surface albedos on the wear target's road scale; grime, shade and wet are the wear family's, so the dark kerb face of the photographs is not baked in.

**Not built:** the two kerb corners (mitre 133 degrees, radius 6.2 m) and the precast taper (dropper) crossing: not in today's street, the target keeps them for a later build-out; tactile paving (none on a 1990 street); the colour variants (grey 75 %, blue-grey 20 %, pink-grey 5 % of the blocks), the wear states (chipped arris, tyre-polished front, weed at the foot, rust and silt on the grates, one slot half-blocked with a leaf) and the dish in the asphalt beside the grate: the engine's materials and masks (unit 4.5). The asphalt edge and the road are the street's ground, not kit pieces (the review scene lays a flat road at z 6 and flags at z 110 for the pictures only).

**For the builder:** the kerb blocks are laid with 8 mm joints, lengths 750 to 1050 (the engine scales or picks; the model is the 900 block), never two equal in a row, the laying scatter and tilt are the engine's. The grate's pot is a hollow box 300 deep under the slots, so that they read black. The review tool laid its pavement at the lowest vertex until 12 October (a buried kerb depth or skirt showed above the ground): fixed in `kit/tools/review_render.py` (the pavement is at z 0). The kerb blocks' end arrises are the only bevels (the long back and foot edges are not eased).
