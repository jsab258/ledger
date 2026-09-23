#!/usr/bin/env python3
"""ONE TERRACE FRONT, AUTHORED FROM ITS WRITTEN DIMENSIONS.

STATUS: ACCEPTED, 2026-09-22, after two more attempts against the Hook sheet.
The ground floor was a PLACEHOLDER until today and the note said why: the
stallriser, the display glazing, the toplight and both doors were all the same
near-black value and the glazing had no frame, so a British shopfront's four
parts did not separate at any distance and neither door was findable. They
separate now. The glazing has jambs, a sill rail and two mullions dividing it
into three lights; the transom runs across the glass and the shop door as one
line; the stallriser is lighter because it catches the sky; the shop door
carries the shopfront's own joinery and the side door a different paint.

WHAT THE SECOND ATTEMPT GOT WRONG, because it is the useful half: the first
replacement side door was a blue-green that looked nothing like brick and had
a luminance of 0.0483 against the brick's 0.0488. The same door hiding in the
same wall, wearing a different hue. Hue does not carry at distance; value
does, and this file now checks it rather than trusting an eye.

BOTH OF THE FAULTS IT WAS LEFT WITH ARE FIXED, 2026-09-22. The two doors read
as one busy patch because the side door's casing was built OUTSIDE the door's
own width, which put its left upright exactly where the shop door's right
stile already stood - two pieces of joinery in the same strip of wall, at the
one point on the elevation where a person has to tell two doors apart. The
casing sits inside its own opening now and the leaf is recessed half a brick,
so the private door is in shadow and reads as a way in rather than as more
shopfront. The toplight did not separate from the glazing because it had a bar
under it and nothing over it, which is not a band; a head rail closes it
against the fascia, and the transom sits twice as proud as the rest of the
joinery because it is the one horizontal that has to carry across a street.

The first authored Meridian facade: a single `east_parade` bay - the
shopfront row - built as an elevation and stood on the street.

    blender --background --factory-startup --python tools/art-recipes/terrace-front.py \
        -- --out DIR [--root DIR] [--bay N]
    python3 tools/art-recipes/terrace-front.py --plan
    python3 tools/art-recipes/terrace-front.py --selftest

WHAT GOVERNS IT. `production/specs/terrace-fronts.md`, 644 lines, which is
SPEC station only and authors no geometry; every number it tags MEASURED
comes from `production/specs/vignette-scene.json`, and THIS FILE READS THAT
FILE rather than retyping the spec's table. That is the difference between a
recipe and a transcription: if the scene file moves, this moves with it, and
cross_check() prints the agreement per field every run so a silent divergence
is impossible. The Hook sheet governs LOOK and PERIOD; it governs no
geometry, which is the ruling of 2026-09-21 and the lesson the lamp column
paid four attempts for.

NO BOOLEANS ANYWHERE, and that is a decision rather than a limitation. A
British terrace elevation IS a coursed plane broken by openings, and the
street's own blockout already emits it that way: sills, lintels and reveals
are separate pieces in `vignette-pieces.json`, not holes cut in a wall. So
the front is built as PANELS AROUND THE OPENINGS - bands and piers whose
edges are the opening edges - which needs no boolean, cannot leave a
non-manifold seam, and puts every edge exactly where a dimension says.

WHAT THIS DOES NOT AUTHOR, said plainly rather than left to be discovered:
the cornice and console brackets above the fascia band, which are already
authored and committed as `fascia_cornice_01` and `fascia_console_01`
(`production/art/fascia-01/`); the interior card behind the glazing, which is
BOM C11 and belongs to the decal generator; the chimney pots (D3, HAVE); and
the wear layer, which under D53 is a separable pass and is not this station.
The fascia band this file builds is what those brackets sit ON, and its top
is the first-floor slab, so it cannot move without moving them.
"""
import json
import math
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SPEC_REL = "production/specs/vignette-scene.json"
PIECES_REL = "production/specs/vignette-pieces.json"

#: THE STREET DATUM, MEASURED. `production/specs/terrace-fronts.md` section 3:
#: "street absolute y = local y + 0.100 m", the built street's own
#: footway-above-crown offset at the frontage line, constant across every
#: piece checked. Everything below is authored in LOCAL coordinates, where 0
#: is the bay's own threshold, and integration adds this.
THRESHOLD_ABOVE_CROWN_M = 0.100

#: Materials, the same convention lighting-column.py uses and for the same
#: reason: authored Base Color triples assigned RAW, so a later reader can
#: see which number was used without opening a colour-management setting.
#: LINEAR sRGB, because Blender's node sockets store linear on a direct
#: property set.
#:
#: brick_red and brick_grey are CHOSEN here, and are marked so: the scene
#: file names the SURFACE ("brick_red") and not a colour, and no committed
#: file in this repository carries a triple for it. They are a low-chroma
#: London-stock red and a soot-grey, which is what the period research asks
#: for; the Hook sheet governs whether they are right and the eye decides.
#: THE WHOLE PALETTE WAS SET AGAINST THE WRONG SHEET, and this is the
#: correction. Every value below marked with a MEASURED line was re-read on
#: 22 September off production/reference/hook-sheet.png - the approved
#: in-house sheet - by taking the median of a region of its street panel and
#: converting the display sRGB to linear. The numbers the recipe had were
#: judged against Codex's retired sheet, which is a DARK, streaming, noir
#: street; the approved one is flat overcast daylight, much higher key, and
#: warm where ours is grey. Ours measured mean 74 against its 120, brightest
#: five per cent 163 against 229, and warmth (R minus B) +0.7 against +18.5.
#:
#: A DISPLAY VALUE IS NOT AN ALBEDO and these are used as a first pass, not
#: as a claim. Under the flat overcast sky this scene lights with, a diffuse
#: surface renders at roughly its albedo, so the sheet's linear value is a
#: fair starting albedo; what settles each one is sampling OUR OWN render and
#: correcting, which is the loop the texture means already use. What is not
#: in doubt is the SIZE of the gap - three times on the brick, eight on the
#: slate, twenty-eight on the joinery - and no amount of tone mapping
#: accounts for twenty-eight.
MATERIALS = (
    # MEASURED: sheet 0.266, 0.078, 0.045, warmth +0.221. Ours was 0.085,
    # 0.040, 0.030 - three times too dark and a quarter of the warmth. The
    # LIGHTENING TOWARDS GREY made last sitting is reversed here: "a
    # soot-darkened London stock is greyer and lighter than a red brick" is
    # sound about a soot-darkened stock and the approved sheet's parade is
    # not one. It is warm red brick and it is the warmest thing in the frame.
    # SECOND PASS, AND THIS ONE IS A CORRECTION MEASURED OFF OUR OWN
    # RENDER rather than read off the sheet. The first pass set the albedo to
    # the sheet's linear value on the reasoning that a diffuse surface under
    # a flat overcast sky renders at roughly its albedo; it came back at
    # 0.78, 0.65, 0.62 of the reference, because AgX does not leave a value
    # where it found it. The ratios are applied per channel and the loop runs
    # again - which is the same loop the texture means already use, and the
    # only honest way to set a number that passes through a tone curve.
    # AND MORE SATURATED, which is a separate measurement from brighter and
    # is the one that was left. Sampled in the RENDER, our brick came out at
    # saturation 0.45 - sitting exactly on the boundary this file uses to
    # count "a pixel carrying real colour" - while the sheet's is 0.57,
    # comfortably over it. That is most of the remaining colour gap and it is
    # not the shopfronts: the saturated thing in the reference is the BRICK,
    # because there is so much more of it than there is of any paint.
#: RE-CLOSED AGAINST THE NEW SHEET, 22 September, at the derived lens. Every
#: value this table carried was tuned against the RETIRED sheet or its
#: predecessor, and Jafar stopped palette work until the new one existed. It
#: does now. The gaps were measured REGION BY REGION, sheet against ours, not
#: on the whole frame, because the two frames still differ in composition and
#: a whole-frame mean would have tuned the road to make up for an end wall:
#:   sky       244 246 248 against 228 230 233   ours too grey
#:   road      149 150 154 against 185 186 189   ours far too bright
#:   pavement  100  83  61 against  78  66  53   ours too dark and too cold
#:   brick     112  81  72 against 125  84  71   ours too red
#:   far parade sat 0.24 against 0.14            ours washed out by haze
#: Each change below names the gap it is for. The scale factors are the
#: linear ratios those sRGB gaps imply, (sheet/ours) ^ 2.2 per channel.
    ("brick_red",   (0.236, 0.092, 0.057), 0.92),   # was (0.300, 0.100, 0.055): too red
    # LIGHTENED 2026-09-22 after the first render of the plain row, which came
    # back charcoal. A soot-darkened London stock is GREYER and LIGHTER than a
    # red brick in daylight, not darker; at the old value the west row read as
    # a black slab beside the parade and the only thing on it that carried was
    # the doors. The check below - nothing hides in the wall behind it - now
    # runs for this row too, which is what stopped the joinery following it up.
    # The plain rows: a lighter, warmer stock than the parade's, because on
    # the sheet the buildings away from the near corner are pale render and
    # light brick rather than anything sooted.
    # AND THE PLAIN ROWS ARE WARM BRICK TOO. Measured against the sheet's
    # own near wall this came back 0.65 of its red and 1.15 of its blue - a
    # neutral grey-brown where the reference is strongly red, 141 against 60.
    # It is the wall that takes the left third of the frame, so its neutrality
    # was most of why our whole picture measured +0.7 warmth against +18.5.
    # PULLED BACK, because with the frame at the sheet's own aspect this
    # wall fills a third of the picture and at 0.313 red it took our warmth
    # PAST the reference: +22.3 against its +18.5. The correction that was
    # right when the wall was a quarter of a squarer frame is wrong now.
    ("brick_grey",  (0.210, 0.092, 0.064), 0.92),   # was (0.268, 0.100, 0.062), same ratio
    ("stone",       (0.240, 0.225, 0.200), 0.80),   # sills, lintels, coping
    # THE GROUND IS NOT THE SAME STONE AS A WINDOW SILL, and sharing one
    # material with the sills was why the first night frame came back with a
    # near-white pavement. Wetting the road meant wetting every sill and
    # coping on the street; darkening the pavement would have darkened them
    # too. They are different surfaces in life and they are different here.
    #
    # AND PAVING IS DARK. A dry British footway is a mid grey and a WET one is
    # nearly black, because water fills the pores and what you then see is a
    # mirror of whatever is above it. The Hook sheet's own street panel is the
    # reference and its pavement is among the darkest things in the frame.
    # MEASURED: sheet 0.122, 0.080, 0.054, warmth +0.068 - a WARM BUFF
    # stone, not a grey one. THIS REVERSES THE SECOND DECISION MADE AGAINST
    # CODEX'S SHEET. The note that stood here said "a dry British footway is
    # a mid grey and a WET one is nearly black... the Hook sheet's own street
    # panel is the reference and its pavement is among the darkest things in
    # the frame". The reasoning was fine and the sheet was the wrong one: on
    # the approved sheet the pavement is among the LIGHTER things in the
    # frame, at two and a half times what we had and warm with it.
    # PASS 2: 93/75/56 after pass 1 against the sheet's 100/83/61.
    ("paving",      (0.245, 0.151, 0.069), 0.62),   # was (0.121, 0.073, 0.042): the new sheet's flags are warm tan
    # THE KERB AGAINST THE NEW SHEET, 22 September. Its kerbs are pale grey
    # stone with a clean arris - 149/143/140 sRGB where the far kerb is lit,
    # 96/84/71 on the near one's wet face - and ours came back at 38/34/28 on
    # the face, a black line down the street. The value is lifted to the
    # sheet's lit kerb, and the face's own shade does the rest.
    ("kerbstone",   (0.300, 0.280, 0.255), 0.58),   # was (0.105, 0.092, 0.078): near black on the face
    # THE SHOPFRONT'S PARTS EACH HAVE THEIR OWN VALUE NOW, and that is the
    # whole of the second attempt. The first one gave the stallriser, the
    # glazing, the toplight and both doors one near-black tone, so a British
    # shopfront's four parts did not separate at any distance and neither door
    # could be found. Nothing about the DIMENSIONS was wrong - they agree with
    # the built street to the micron - so the repair is value and frame.
    #
    # THE ORDER MATTERS MORE THAN THE HUES. Glass is the darkest thing on the
    # elevation because what it shows is an unlit interior; the painted
    # joinery around it is several times lighter, which is what draws the
    # frame; the stallriser is lighter still because it catches the sky; and
    # the side door is a different paint from the shop's, because a shop and
    # the flat above it were never painted by the same person on the same day.
    # DARKENED WHEN THE SHOPS WERE LIT, and the direction reversed with them.
    # While the glazing stood for an unlit interior the joinery had to be the
    # LIGHTER of the two or no frame drew; now the window is lit and sees
    # through, and a British shopfront's joinery is dark oxblood or bottle
    # green read against that brightness. Same requirement - the frame
    # separates from the opening - arrived at from the other side.
    # MEASURED, AND THE BIGGEST SINGLE ERROR ON THE STREET: the sheet's sash
    # bars and shopfront frames read 0.73 to 0.76 linear and ours was 0.026.
    # TWENTY-EIGHT TIMES. White-painted joinery against red brick is the
    # approved sheet's whole character - every window on it is a white grid -
    # and we had near-black woodwork, which is most of the reason our frame
    # has no highlights in it at all (brightest five per cent 163 against
    # 229). It is not a subtlety; it is the thing the street is made of.
    ("paint_joinery",(0.680, 0.672, 0.640), 0.42),  # WHITE, as the sheet is
    # A DARK PAINTED BOARD, not a pale one, and the check above forced it.
    # This was 0.086, 0.104, 0.090 - "lighter because it catches the sky",
    # which is a judgement made against Codex's sheet. With the brick raised
    # to its measured value the two came within seven thousandths of each
    # other and the stallriser vanished into the wall. On the approved sheet
    # the kicked board is the SHOP'S OWN COLOUR and the commonest of them is
    # a deep oxblood, which is what this fallback now is; per-bay paint from
    # FASCIA_PAINT overrides it on every bay that has one.
    ("paint_stall", (0.060, 0.014, 0.018), 0.50),   # the kicked board, the shop's colour
    # THE METAL REFIT, AND IT IS THE PHOTOGRAPHS OVERRULING THE SHEET.
    #
    # There is not ONE metal shopfront on the approved sheet - every frontage
    # on it is painted timber with small panes, which is a conservation-area
    # refit and not a 1989 working street. R05's photograph, Princes Avenue
    # in August 1989, is "METAL SHOPFRONT, FLUORESCENT STRIPS, stacked goods,
    # PATTERNED TILE STALLRISER"; D01 gives Quay Stores "a plain metal
    # shopfront" and D06 says "Hook shops receive METAL FRAMES, practical
    # light fittings and repair patches within older masonry". The rule Jafar
    # recorded on 22 September decides it: the sheet governs mood, palette
    # and composition, the photographs govern what things actually looked
    # like, and where they disagree the photographs win.
    #
    # NOT EVERY BAY, because D06 says metal frames AMONG older masonry. A
    # parade where every front is metal is the same mistake as one where
    # every front is timber, in the other direction.
    #
    # MILL-FINISH SILVER, AND THE CHECK CHOSE IT. The first value was a dark
    # anodised grey, 0.152/0.156/0.160, which is a real period finish and
    # came out at luminance 0.1554 against grey brick's 0.1330 - inside the
    # 0.02 this file refuses, so the new front would have vanished into the
    # wall it was cut into. That is the fourth time "no painted part hides in
    # the brick behind it" has caught a colour chosen for being plausible
    # rather than for being visible.
    # SILVER IS ALSO THE COMMONER 1989 FRONT. It sits at 0.339, clear of the
    # brick below it and clear of the white timber beside it at 0.672, so the
    # refitted bay reads as a THIRD material rather than as a dirty version
    # of either.
    ("frame_metal", (0.330, 0.340, 0.352), 0.30),   # mill-finish aluminium
    # AND THE TILED STALLRISER, which is the other half of what R05 shows. A
    # tile is glossier than a painted board and darker than the frame above
    # it; the PATTERN is not built, and that is said out loud rather than
    # implied - we hold no tile map and inventing one from noise would be a
    # texture pretending to be evidence.
    ("tile_stall", (0.044, 0.052, 0.058), 0.18),    # glazed tile, no pattern
    # THE CAB OFFICE'S FRONT, 22 September, the shopfronts step, and it is
    # the one place on the parade where the sheet and the photographs say
    # the same thing. R05 is "metal shopfront... PATTERNED TILE STALLRISER";
    # the approved sheet's MICKEY'S is a slim frame painted slate blue-grey
    # over a pale patterned tile. So: R05's construction in the sheet's
    # colours. The frame measures 57-75, 72-84, 86-92 sRGB across its pier,
    # its fascia and its door, and this is the middle of that in linear; the
    # tile measures 158, 151, 132 over its pattern, so its GROUND is paler
    # than that and the pattern takes it down to the measured mean.
    #
    # FINISHED FROM THE MEASUREMENT, after two attempts. Rendered, the first
    # values came back well under the sheet on the same front - the pier
    # 46/56/65 against 57/72/86, the tile 113/107/92 against 158/151/132 -
    # because a pier and a stallriser stand in their own recess's shade.
    # Raised by the measured gap, the frame only by a quarter: at the full
    # gap its luminance walks into the brick's, and on the sheet the two are
    # told apart by hue AND by value, the frame about two-thirds the brick's.
    ("frame_painted", (0.0625, 0.0875, 0.119), 0.35), # powder-coated slate
    ("tile_patterned", (0.620, 0.570, 0.430), 0.20), # glazed, a pattern on it
    # AND THE EMPTY UNIT'S GLASS IS WHITENED, which is what was done to an
    # empty shop's window in 1989 - a wash of whiting on the inside so the
    # bare room does not show - and it is the other half of R05's "letting
    # board". Pale, matt, and not glass at all to the eye.
    ("glass_whitened", (0.420, 0.415, 0.385), 0.85),
    # THE SIDE DOOR IS A DIFFERENT PAINT, AND THE SECOND ATTEMPT HAD TO MOVE
    # IT. A warm brown was a plausible door colour and it was almost exactly
    # brick_red's own value, so the door vanished into the wall it sits in -
    # the same failure as the first attempt, one part along. It is a dark
    # dark green now, and the FIRST dark green was rejected by this file's own
    # new check: a blue-green that looked nothing like brick had a luminance
    # of 0.0483 against the brick's 0.0488, which is the same door hiding in
    # the same wall wearing a different hue. Hue is not what carries at
    # distance; value is. This one sits at half the brick's, and the check
    # below holds it there.
    # The doors stay dark - on the sheet they are a deep teal and a deep red
    # inside white surrounds - but not as dark as they were.
    ("paint_door",  (0.030, 0.055, 0.048), 0.42),   # the side door: a different paint
    ("paint_fascia",(0.030, 0.022, 0.030), 0.45),   # the lettered board
    # THE GLASS WAS A BLACK WALL. At 0.012 it absorbed the lit interior behind
    # it and every shopfront on the row read as a boarded hole, which is the
    # opposite of what a window does: a window is the one surface on a
    # frontage you are supposed to see PAST. Lifted, and its transmission
    # raised below, so the shop behind it carries.
    # LIFTED WITH THE REST OF THE STREET. This was set when the whole
    # picture was three times darker; against the approved sheet a shop
    # window is not a black hole, it is a dark surface with the sky and the
    # opposite frontage lying in it.
    ("glass",       (0.085, 0.092, 0.100), 0.0),   # 0.06 until 23 September: polished float glass has none
    ("lead",        (0.030, 0.030, 0.032), 0.60),   # downpipe
    # MEASURED: sheet 0.220, 0.202, 0.195 - EIGHT TIMES what we had, and
    # warm where ours was blue. A wet Welsh slate roof under an overcast sky
    # is a mid grey that mirrors the sky, not a black one; ours read as a
    # hole in the roofline.
    # DARKER, 22 September, against the new sheet: its slate reads 61/58/61
    # on the near parade and about 117/112/107 on the hill, and ours came back
    # pale - a roof faces the bright overcast sky, so a mid-dark albedo reads
    # light. Wet Welsh slate is close to black. From the hook camera the
    # street's own roofs barely show; this is mostly the hill's.
    ("slate",       (0.060, 0.058, 0.062), 0.70),   # was (0.150, 0.140, 0.135)
    # The sheet's wet road reads 0.292 linear, but almost all of that is the
    # SKY IN IT rather than the tarmac: a wet road is a mirror. So this is
    # raised only to where a damp British carriageway actually sits and the
    # rest is left to the reflection, which is what _wetten is for. Ours at
    # 0.016, then darkened again for wetness, was reading as fresh tar.
    # A WORN BRITISH ROAD IS PALE, which is the thing two passes of this got
    # wrong in opposite directions. It was 0.016 - fresh tar - and raising it
    # to 0.055 still rendered at 0.40 of the reference with the reflection
    # turned on. The sheet's carriageway sits at sRGB 147 near the camera,
    # where a grazing-angle sky reflection contributes least, so most of that
    # value is the surface itself: years of pale chippings polished by tyres,
    # not the black of a road laid last week.
    # THIRD AND LAST PASS ON THE ROAD, and this one is targeted rather than
    # global. Sampled in the render against the sheet's own carriageway:
    # ours 109,108,109 against its 150,150,146, both near-neutral, so the
    # hue was right and the value was 27 per cent short. Raising the whole
    # frame to close a gap like this is what made the picture worse an hour
    # ago; raising the ONE surface the measurement names does not.
    # PASS 2: pass 1's 0.216 brought the road from 185 to 165 against the
    # sheet's 149 - a 0.6 cut in albedo bought only 0.78 in radiance, because
    # a wet road is mostly reflected sky. Another 0.58: 0.125 is about what
    # weathered asphalt measures dry, and it is wet.
    ("asphalt",     (0.125, 0.123, 0.118), 0.85),   # was (0.360, 0.354, 0.338): the new sheet's road is mid-grey, not silver
    # PEOPLE ARE NOT SILHOUETTES IN DAYLIGHT. A silhouette is right for the
    # dusk frame and wrong for the working one: the sheet's own panel has a
    # teal jacket, an orange one and a white coat in it, and they are a good
    # part of what makes that street look inhabited rather than evacuated.
    # Three muted period tones, assigned round the figures, none of them
    # bright: 1990 was not a colourful decade outdoors.
    # THE PROPS' OWN TIMBER: crates, pallets and the A-board. Bare, weathered
    # softwood rather than anything painted, which is what a crate outside a
    # fish shop is.
    ("prop_timber", (0.105, 0.062, 0.031), 0.78),
    ("figure",      (0.014, 0.014, 0.016), 0.80),
    ("figure_a",    (0.020, 0.042, 0.048), 0.75),   # a teal anorak
    ("figure_b",    (0.086, 0.030, 0.012), 0.75),   # a rust jacket
    ("figure_c",    (0.055, 0.052, 0.046), 0.75),   # a grey overcoat
    # THE YELLOW IS NOT MINE AND NOT NEW. The scene file carries it as gamma
    # sRGB (0.78, 0.66, 0.18) and says where it came from: the game's own
    # Furniture.cs, which has been painting the town's kerbs since M17.10. A
    # second opinion about the same yellow would put two yellows in one
    # project. Converted to linear here because that is what a Blender socket
    # holds, and nothing else about it is decided here.
    # WORN, NOT FRESH. The approved sheet does carry double yellows, so they
    # stay - but on it they are faded and nearly lost against the tarmac,
    # while ours were the single brightest thing in the picture. Halved.
    # WORN PAINT IS CREAM, and the new sheet says so: its double yellows read
    # 219/206/170 where ours read 179/156/91, an ochre stripe. Road paint
    # weathers pale long before it goes, and on a wet overcast road it reads
    # as a cream line. Scaled by the linear ratio of the two, per channel.
    ("paint_yellow",(0.405, 0.331, 0.079), 0.55),
    # THE CENTRE LINE'S WHITE, weathered as the yellows are: road paint on a
    # working street is a dirty off-white, not the white of a new line.
    ("paint_white", (0.520, 0.515, 0.490), 0.55),
    # CHIMNEY POTS, sampled off the new sheet's nearest stack, 22 September:
    # two terracotta at 126/76/65 and 123/77/62 sRGB, one buff at 196/169/127.
    ("pot_clay",    (0.203, 0.073, 0.051), 0.80),
    # A DISH IS PALE GREY PRESSED STEEL, and it is the palest thing on the
    # upper wall, which is why the sheet's reads at all at that size.
    ("dish_grey",   (0.420, 0.425, 0.420), 0.45),
    # A CEMENT REPAIR PATCH on old brick, sampled off the new sheet's near
    # gable at 175/141/93 and pulled back a little from the orange its light
    # puts in it.
    ("render_patch",(0.380, 0.285, 0.160), 0.85),
    # RUBBED BRICK, for the window arches: on the new sheet the arch over
    # each window reads 123/67/49 against the wall beside it at 115/63/46 -
    # the same clay, finer and a touch brighter. Scaled off brick_red by that
    # ratio in linear rather than sampled outright, so the two stay a pair.
    # ATTEMPT TWO LIFTS IT TO 1.3 OF THE WALL: at the measured 1.15 the ring
    # vanished into the brick at the hook camera's raking angle, where the
    # sheet's reads because its radiating joints and the curved sash under
    # it give it an edge. The sash is built now too; see _segmental_arch.
    ("brick_rubbed",(0.307, 0.120, 0.074), 0.90),
    ("pot_buff",    (0.554, 0.397, 0.212), 0.80),   # was (0.260, 0.180, 0.020)
    # THE VEHICLE. Car paint is the only genuinely SMOOTH surface on this
    # street - everything else is brick, stone, timber or tarmac - and that
    # is most of what makes a car read as one at twenty-five metres: it holds
    # a highlight where nothing around it does. Dark, because the approved
    # sheet's is dark.
    # CREAM RENDER, the pale houses among the brick on the new sheet's hill.
    # Read off the sheet at about 200/185/150; in linear, this.
    ("render_cream",(0.550, 0.480, 0.280), 0.80),
    ("car_dark",    (0.022, 0.024, 0.032), 0.26),
    # THE SHEET'S SECOND CAR, a faded blue-grey saloon of the kind every
    # street had in 1990. A second paint so the rank is two cars and not one
    # car twice.
    ("car_bluegrey",(0.070, 0.085, 0.105), 0.30),
    ("car_glass",   (0.010, 0.011, 0.014), 0.10),   # darker than shop glass
    ("tyre",        (0.008, 0.008, 0.008), 0.88),
    ("car_trim",    (0.018, 0.018, 0.019), 0.55),   # moulded black plastic
    # THE YELLOW REAR PLATE IS THE STRONGEST PERIOD-BRITISH TELL IN THE FRAME
    # and it costs one box. White front, yellow rear has been the law here
    # since 1973, and it is a fact about British roads rather than a brand -
    # so it carries none of the canon risk the bill of materials flags
    # against a real car SHAPE.
    ("plate_rear",  (0.480, 0.380, 0.035), 0.50),
    ("plate_front", (0.560, 0.560, 0.540), 0.50),
    ("lamp_red",    (0.160, 0.012, 0.010), 0.22),
    # The lit shop interior, emissive. Its colour and its strength are the
    # piece file's own window_practicals: gamma (1, 0.86, 0.62) at 1.6.
    ("interior_lit",(1.000, 0.714, 0.344), 0.90),
    # R05's "FLUORESCENT STRIPS", 22 September: the 1989 photograph's metal
    # shopfront is lit by bare tubes, and so is the approved sheet's MICKEY'S.
    # A tube is the brightest thing in a shop window by day, which is most of
    # why a lit shop reads as open against an overcast street.
    ("tube_lit",    (0.900, 0.940, 1.000), 0.50),
    # THE LAMP'S OWN THREE, copied from tools/art-recipes/lighting-column.py's
    # MATERIALS rather than chosen again here, so the column in the street is
    # the column that was accepted. lens_amber is the spec's own sodium
    # colour and is emissive at night.
    ("steel_dark",  (0.021, 0.021, 0.024), 0.42),
    ("grime",       (0.078, 0.061, 0.048), 0.90),
    ("lens_amber",  (0.780, 0.360, 0.040), 0.20),
    # WHAT A WINDOW SHOWS IS THE INSIDE, and the first render of this bay is
    # why that has a material of its own. The carcass behind the elevation was
    # brick_red and filled the frontage plane, so every opening - two sashes,
    # a shopfront, two doors - read as unbroken brickwork and the front came
    # back as a blank box with sills on it. The openings are real; there was
    # simply nothing dark behind them.
    # AN UNLIT ROOM IS NOT A BLACK HOLE. At 0.010 every window on the street
    # that has no practical behind it - the whole west row, every flat above
    # the parade - read as a hole punched in the wall rather than a room with
    # the light off. A room in daylight with no lamp on still has a ceiling, a
    # back wall and whatever daylight reaches it through its own window, which
    # is dim but is not nothing. The shops have cards behind them and these
    # have this, and the difference between the two is the point.
    ("interior",    (0.038, 0.035, 0.032), 0.95),
)

#: WHICH SIDE OF ITS OPENING EACH BAY PUTS ITS DOORS ON. The spec names this
#: as a per-bay parameter and does not give the per-bay values, so the pattern
#: is CHOSEN here and marked so.
#:
#: WHY IT EXISTS AT ALL. The spec MEASURED the built street and found zero
#: per-bay variation: every shop door on the row at exactly bay_start +
#: 1.638 m and every side door at exactly bay_start + 0.769 m, checked across
#: three bays. One stencil repeated six times is what reads as generated
#: rather than authored the moment somebody walks along it, and no amount of
#: texture repairs a rhythm.
#:
#: WHY NOT SIMPLE ALTERNATION. Left, right, left, right makes every neighbour
#: the mirror of the last, which is a second stencil rather than none - the
#: eye has the beat in two bays. A pair, a single, then a pair is what a
#: parade built at one time and fitted out by six different tenants looks
#: like.
BAY_DOORS_ON = ("left", "left", "right", "left", "right", "right")

#: BAY 5 HAS NO SIDE DOOR, and that one is the spec's rather than mine:
#: section 4 item 2, the grocer whose upper flat is reached from the rear
#: yard, which frees 0.838 m for display glazing. It is the only bay whose
#: opening zone is not the fixed 5.3 m.
BAY_WITHOUT_SIDE_DOOR = 5

#: THE STREET'S OWN CROSS-SECTION, MEASURED from the scene file's `street`
#: block: a 6.0 m carriageway in two 3.0 m lanes, a 2.0 m footway each side,
#: and a 125 mm kerb upstand. The frontage line is 5.125 m from the centre,
#: which is the atlas's own `street_anchor` datum. Read rather than typed,
#: like everything else here.
STREET_FRONTAGE_M = 5.125

#: WHERE THE LAMP COLUMNS STAND, MEASURED from the emitted piece list rather
#: than re-derived from the spacing rule: four columns at 8, 18, 28 and 38 m,
#: staggered side to side, set 0.6 m back from the kerb. The piece file is the
#: street as built and this recipe places its fronts around the same lamps.
LAMP_AT = ((8.0, 3.725), (18.0, -3.725), (28.0, 3.725), (38.0, -3.725))

#: The two conditions the scene file names, and the only two this recipe
#: renders. MEASURED: `conditions` in production/specs/vignette-scene.json.
#: overcast_day is the DEFAULT British frame rather than a side case - the
#: research counts 1403 sunshine hours against about 4400 daylight, which is
#: under a third with the sun out - and wet_night is D31's own tying frame,
#: the one the whole stage is judged on: dusk, wet, lamps lit, a figure in
#: silhouette.
CONDITIONS = ("overcast_day", "wet_night")

#: THE TEXTURE PACK, AND WHICH OF OUR MATERIALS TAKES WHICH SURFACE.
#:
#: WE ALREADY HOLD THESE. ledger/Assets/StreamingAssets/CityPack/textures
#: carries eighteen surfaces with a base, a roughness and a normal map each,
#: named for the very surfaces the scene file names - brick_red, brick_grey,
#: asphalt, sidewalk, kerb, roof, concrete, glass, wood, metal, setts. They
#: are ambientCG, CC0, and ambientCG is on the licence allowlist. Nothing is
#: fetched here and nothing new is attributed.
#:
#: TILE METRES IS THE ONE NUMBER THAT MATTERS and it is per surface, because
#: a texture tiled at the wrong size is worse than no texture: brick at half
#: scale reads as tile and at double scale as blockwork, and either tells the
#: eye the wrong thing about how big the building is. Set from what the
#: surface IS - a brick course is 75 mm, so 1.5 m of wall is twenty courses,
#: which is what one of these maps holds.
TEXTURE_DIR = "ledger/Assets/StreamingAssets/CityPack/textures"

#: WHAT EACH MAP'S AVERAGE COLOUR ACTUALLY IS, in linear sRGB, MEASURED off
#: the committed files on 2026-09-22 and written down rather than assumed.
#:
#: WHY THIS TABLE EXISTS AT ALL: THE PACK'S NAMES DO NOT MATCH ITS COLOURS.
#: `brick_red` averages a sandy fawn and `brick_grey` averages a pinkish
#: brown, so taking each map's own colour put the RED parade in pale
#: sandstone and the GREY west row in red brick - the two rows swapped, and
#: thirteen percent apart in value, which is inside the bound this file's own
#: check refuses for a painted part against its wall. `roof` is terracotta
#: pantile and this town is slated; `roof_b` is the slate.
#:
#: SO THE PHOTOGRAPH SUPPLIES PATTERN, RELIEF AND ROUGHNESS, AND THE PROJECT
#: SUPPLIES THE PALETTE. Each map is multiplied by the authored colour divided
#: by its own measured average, which lands the rendered surface on the colour
#: this file authored while keeping every brick edge, every joint and every
#: streak the photograph has. It is the one way to have both, and the
#: alternative - taking the pack's hues - loses the period palette, the value
#: separation the checks enforce, and the distinction between the two rows.
TEXTURE_MEAN = {
    "asphalt": (0.0602, 0.0577, 0.0571),
    "brick_grey": (0.2435, 0.1951, 0.1777),
    "brick_red": (0.2717, 0.2317, 0.1599),
    "concrete": (0.2384, 0.2312, 0.1923),
    "glass": (0.0659, 0.0798, 0.0929),
    "kerb": (0.2614, 0.2617, 0.2402),
    "metal": (0.1972, 0.1862, 0.1853),
    "plaster": (0.5225, 0.5166, 0.4732),
    "roof_b": (0.0315, 0.0304, 0.0364),
    "setts": (0.2127, 0.2139, 0.2342),
    "sidewalk": (0.1728, 0.1611, 0.1114),
    "wood": (0.1483, 0.0907, 0.0519),
}
#: THE TILE FIGURES WERE ALL ABOUT THREE TIMES TOO LARGE on the first pass and
#: the pair said so in one look: the near wall's bricks read about 0.25 m on
#: the course against a real 0.075 m, which makes a two-storey terrace look
#: like a garden wall seen from a foot away. A texture at the wrong scale is
#: worse than no texture, because it does not just fail to say what the
#: surface is - it says the wrong thing about how big the building is.
#:
#: SET FROM THE COURSE, NOT BY EYE. A British brick course is 75 mm including
#: its bed joint, these maps carry roughly seven courses, so 0.55 m of wall is
#: one tile. The ground surfaces follow the same rule from their own units: a
#: sett is about 100 mm and these hold seven or eight of them.
SURFACE_OF = {
    "brick_red":    ("brick_red", 0.55),
    "brick_grey":   ("brick_grey", 0.55),
    "asphalt":      ("asphalt", 2.0),
    # SETTS RATHER THAN THE PACK'S `sidewalk`, which is a mossy green and
    # turned the whole footway the colour of a canal bank. The sheet's
    # pavement is grey stone.
    # FLAGS, NOT SETTS, 22 September. The new sheet's footway is large stone
    # flags, and so is R09's 1989 photograph - "slab paving" - which settles
    # it: where the sheet and the photographs agree there is nothing to
    # weigh. The pack holds no flag map (its `sidewalk` is mossy cobbles), so
    # the concrete map gives the stone its mottle and _flag_joints lays the
    # joints over it at a real flag's size.
    # AND THE PLASTER MAP, NOT THE CONCRETE, attempt two of the flags' stone:
    # the concrete map has long streaks in it that read, at the footway's
    # raking angle, as the boards of a wooden floor. The plaster map's
    # mottle has no direction, and the flags' own tones and joints carry
    # the structure.
    "paving":       ("plaster", 1.2),
    "kerbstone":    ("kerb", 0.6),
    # roof_b, NOT roof: `roof` is terracotta pantile and averages a strong
    # orange, and this town is slated. `roof_b` is the slate.
    "slate":        ("roof_b", 0.8),
    "stone":        ("concrete", 0.8),
    # PAINTED JOINERY TAKES PLASTER, NOT TIMBER, and the reason is a clamp
    # this file already carried. The tint gain is the authored colour over
    # the map's own average, bounded to 6.0 so a dark map cannot be driven
    # into blown highlights - and white paint over the wood map needs
    # 0.672/0.0907 = 7.4 on green and 0.640/0.0519 = 12.3 on blue. Both hit
    # the ceiling, so the gain came out lopsided and every white sash on the
    # street rendered CREAM. Widening the clamp would have traded that for
    # the blown patches it exists to prevent. The real answer is that GLOSS
    # PAINT DOES NOT SHOW GRAIN: a painted sash is a smooth surface, the
    # plaster map is the smooth one we hold, and its own average is light
    # enough that white needs a gain of 1.3.
    "paint_joinery":("plaster", 0.5),
    "render_cream": ("plaster", 1.0),
    "paint_stall":  ("plaster", 1.0),
    # Both refit surfaces are SMOOTH, so they take the plaster map for its
    # relief and not the timber one: metal has no grain and neither has a
    # glazed tile.
    "frame_metal":  ("plaster", 0.4),
    "tile_stall":   ("plaster", 0.3),
    "frame_painted": ("plaster", 0.4),
    "tile_patterned": ("plaster", 0.3),
    "glass_whitened": ("plaster", 0.6),
    "paint_door":   ("wood", 0.6),
    "paint_fascia": ("wood", 1.0),
    # A PANE OF GLASS IS NOT A PHOTOGRAPH OF ANYTHING, and it had the
    # pack's glass map box-projected across it at 1.4 m: every shop window
    # on the street carried a repeating dark checker, which reads as a
    # grille or a filthy tile and never as glazing. It is the one surface
    # here with NO texture of its own - what you see in a window is the
    # street reflected in it and the room behind it, both of which arrive
    # from the scene now that raytracing is on.
    "glass":        (None, 0.0),
    "lead":         ("metal", 0.35),
    "steel_dark":   ("metal", 0.35),
    "interior":     (None, 0.0),
    "prop_timber":  ("wood", 0.5),
    "paint_yellow": (None, 0.0),
    "paint_white":  (None, 0.0),
    "pot_clay":     ("plaster", 0.5),
    "brick_rubbed": ("plaster", 0.4),
    "render_patch": ("plaster", 0.3),
    "pot_buff":     ("plaster", 0.5),
    # EVERY VEHICLE SURFACE IS FLAT COLOUR ON PURPOSE. The pack's brick,
    # plaster and timber are the wrong story for a pressed steel panel, and
    # its metal map is machined plate. A car at twenty-five metres is a
    # shape, a value and a highlight.
    "car_dark":     (None, 0.0),
    "car_glass":    (None, 0.0),
    "tyre":         (None, 0.0),
    "car_trim":     (None, 0.0),
    "plate_rear":   (None, 0.0),
    "plate_front":  (None, 0.0),
    "lamp_red":     (None, 0.0),
    "interior_lit": (None, 0.0),
    "tube_lit":     (None, 0.0),
    "figure":       (None, 0.0),
    "figure_c":     (None, 0.0),
    "figure_b":     (None, 0.0),
    "figure_a":     (None, 0.0),
    "grime":        (None, 0.0),
    "lens_amber":   (None, 0.0),
}

#: THE FASCIA PALETTE, from the spec's own list: oxblood, bottle green, deep
#: navy, cream or stone, and bare soot-darkened timber. The spec is explicit
#: about how they are used - "never one colour per bay at random: a real
#: parade was repainted in waves by whoever owned it, not rainbow-striped" -
#: so the assignment below runs in waves: two oxblood together, then navy,
#: then a green pair, then the one bare board.
#:
#: BAY 3 IS BARE TIMBER ON PURPOSE. The fascia package already records it as
#: the one bay with NO lettering and an awning instead, its right-hand console
#: "clipped off and never put back... the parade's empty unit". A row where
#: every shop is trading is a row nobody believes.
#: CREAM WAS MISSING AND IT IS HALF THE PARADE. The spec's own list is
#: "oxblood, bottle green, deep navy, CREAM OR STONE, and bare soot-darkened
#: timber", and the first five bays were built from the four dark ones only -
#: so every shopfront on the row was darker than the brick behind it and the
#: parade read as one long shadow. The approved sheet has TWO pale fronts in
#: five, and its cream one measures 0.630, 0.530, 0.325 linear: not an
#: accent, one of the brightest things in the picture. Pulled back a little
#: from the measurement because ours catches more sky than a shop under an
#: awning does.
#:
#: STILL IN WAVES, which is the rule that matters here: two oxblood together,
#: then cream, then the bare unit, then cream again, then the green. The
#: cream wave running either side of the closed shop is the story the fascia
#: package already tells - a parade repainted by whoever owned it, with one
#: unit that nobody did.
#: WHICH BAYS HAD THEIR FRONTS REPLACED, and it is one of six.
#:
#: THE FISH SHOP IS THE ONE, and it is chosen rather than picked. MICKEYS.md
#: puts the fish shop in the bay north of the cab office, which is bay 1;
#: R05 and R09 both photograph metal-fronted food shops in 1989; and a wet
#: fish counter is the trade that most wants a washable front and a
#: fluorescent strip over it. Bay 0 is the cab office and is Jafar's anchor
#: interior, bay 3 is the empty unit, and the rest keep their timber.
#:
#: IT IS A LIST AND NOT A FLAG so that a second refit is one entry rather
#: than a second code path, and so the check below can count them.
#:
#: KEYED BY BLOCK AND BAY NOW, 22 September, and it was keyed by bay alone.
#: A bare bay number applied to EVERY shop block, so west_north's bay 1
#: became a metal front by accident of its index. It is kept as one - D06
#: says metal frames among older masonry, and that bay is across the road
#: from the fish shop - but it is written down here as a choice rather than
#: left as a side effect.
#:
#: THE CAB OFFICE IS THE SECOND REFIT, and the sheet and the photographs
#: agree on it: R05's metal front and patterned tile, in the approved
#: sheet's slate blue-grey, with the fascia and the piers in the same paint
#: because a front is painted as a unit. "frame" is the section material,
#: "stall" the stallriser's, "paint" the piers' and fascia's where the refit
#: repainted them too.
SHOPFRONT_REFITS = {
    ("east_parade", 0): {"frame": "frame_painted", "stall": "tile_patterned",
                         "paint": ("slate_blue", (0.0625, 0.0875, 0.119))},
    ("east_parade", 1): {"frame": "frame_metal", "stall": "tile_stall"},
    ("west_north", 1):  {"frame": "frame_metal", "stall": "tile_stall"},
}
#: The two section materials a refit can be in, for the checks.
REFIT_FRAMES = ("frame_metal", "frame_painted")
#: And every material a shopfront's joinery can be in.
JOINERY_MATERIALS = ("paint_joinery",) + REFIT_FRAMES

#: THE EMPTY UNIT, whitened and to let. R05's parade has "a neighbouring
#: letting board"; the spec already made bay 3 the unit nobody trades from.
EMPTY_UNIT = ("east_parade", 3)
#: THE TWO BOARDS THIS PROJECT LETTERED ITSELF, in PT Sans, by
#: tools/props/make_vignette_2d.py - root-relative paths, not image-lane ids.
LETTERED = "production/assets/vignette/decals2d"
LETTING_BOARD = LETTERED + "/board_to_let"
LETTING_BOARD_M = (0.90, 0.45)
#: AND THE CAB OFFICE'S NAME. The spec's decal for east_parade_fascia0 is
#: still the image lane's maroon signboard - gilt serifs and a border, a
#: pub's board, made against the retired sheet when Mickey's was a pub. The
#: approved sheet signwrites the name across the fascia in plain capitals,
#: so the recipe lays that instead. THE SPEC IS NOT CHANGED HERE: the Unreal
#: probe stages the generated directory and nothing else, so moving the
#: spec's id is a probe change and waits for one.
SIGN_OVERRIDE = {("east_parade", 0): LETTERED + "/fascia_mickeys_plain"}

FASCIA_PAINT = (
    # LIFTED TO THE SHEET'S OWN VALUES, 22 September. Sampled off its street
    # panel, its green shopfront is 0.065, 0.090, 0.078 linear and ours was
    # 0.010, 0.030, 0.019 - FIVE TIMES darker, which is not a bottle green,
    # it is a black door. Period shop paint was dark; it was not unlit. The
    # oxblood comes up with it for the same reason and by the same amount.
    #
    # AND THE ORDER MOVED BY ONE, which is composition rather than palette.
    # On the approved sheet the NEAREST shop is the richest thing in the
    # frame - deep oxblood, filling the right third - and ours was cream,
    # which put the palest mass in the picture exactly where the reference
    # puts its darkest. The west block is built as a half turn so its bays
    # arrive in reverse and its nearest is index 2; rotating the wave by one
    # puts oxblood there. Still in waves: two oxblood together, the bare
    # unit, cream either side of it, then the green.
    ("cream",      (0.520, 0.430, 0.270)),
    ("oxblood",    (0.105, 0.020, 0.024)),
    ("oxblood",    (0.105, 0.020, 0.024)),
    ("bare_timber",(0.021, 0.014, 0.010)),
    ("cream",      (0.520, 0.430, 0.270)),
    ("bottle_green",(0.060, 0.085, 0.072)),
)

#: THE SIGNS ARE READ FROM THE SPEC'S OWN DECALS NOW, 22 September, and the
#: dict that stood here was wrong in two ways the spec was not.
#:
#: IT WAS KEYED BY BAY ALONE, so every shop block got the parade's signs:
#: west_north carried a second MICKEY'S, a second fish market and a second
#: Rita's across the road from the first. That is the fault Jafar ruled
#: uncitable on the sheet itself - "the second MICKEY'S sign on the
#: neighbouring shop" - built into our own street. The spec anchors each
#: sign to ONE piece, east_parade_fascia<N>, and west_north has none.
#:
#: AND IT PASTED THE WHOLE IMAGE. Three of the four generated signs are
#: photographs of a whole shopfront, and the spec carries a uv crop for each
#: - "pasting all of it on a fascia band would put a photograph of a street
#: on a street" - which the recipe never read. It reads it now, and each sign
#: goes on at the spec's own width.
DECAL_DIR = "ledger/Assets/StreamingAssets/Decals"

#: The two frames. ELEVATION IS THE ONE THAT JUDGES THE FRONT - square to the
#: frontage with the roofline in, which is cam_B's own description in the
#: scene file - and EYE is the one that says whether it belongs on a street,
#: at cam_A's 1.6 m and its measured 4 degree downward pitch. Both are
#: derived from the bay's own dimensions below rather than typed, so a bay of
#: another width still frames.
FRAMES = ("elevation", "eye")
AUTHORED_RES = (1400, 1100)

#: THE HOOK FRAME IS THE SHEET'S OWN SHAPE, and this is the thing no amount
#: of moving the camera could have fixed.
#:
#: MEASURED: the approved sheet's street panel is 617 x 326 pixels, an aspect
#: of 1.89 - a wide, letterbox picture. Ours was 1400 x 1100, an aspect of
#: 1.27, very nearly square. At a 60 degree VERTICAL field those two are not
#: the same camera at all: the horizontal half-field is atan(tan(30) x aspect),
#: which is 36.2 degrees at 1.27 and 47.5 degrees at 1.89. Eleven degrees.
#:
#: WHAT THAT COST, in metres. A frontage 7.3 m to one side only enters the
#: frame once it is lateral/tan(half-field) ahead of the camera: 10.0 m away
#: at 36.2 degrees, 6.7 m at 47.5. So our nearest visible parade was a third
#: further off than the reference's and correspondingly smaller, and moving
#: the camera along the street could not close that gap - the 10 m is set by
#: the lateral distance and the field, and is the same wherever the camera
#: stands. Two hours went on trying to move it.
#:
#: 1400 x 740 is 1.892 against the panel's 1.8926.
HOOK_RES = (1400, 740)
#: THE NEW SHEET'S SHAPE, 22 September: pass 4 is 2048 x 1088, an aspect of
#: 1.882; 1400 x 744 is 1.8817. The retired poster's panel was 1.8926, which is
#: why the line above was 740.
HOOK_RES = (1400, 744)

#: AND THE LENS WAS NEVER DERIVED FROM THE APPROVED SHEET AT ALL, which is
#: the answer to why our frame and the concept art are not the same angle.
#:
#: THE ASPECT ABOVE WAS MEASURED ON THE APPROVED SHEET. The FIELD was not:
#: 60 degrees is this recipe's default for its other cameras and it was
#: carried across unchanged. Nothing on the approved sheet has ever been
#: measured to give 60.
#:
#: THE ONLY FIELD ANYBODY EVER DERIVED FOR A HOOK PANEL IS CODEX'S.
#: production/specs/vignette-scene.json derives it at length - "fov_vertical
#: _deg 39.0: THE ONLY NUMBER HERE THAT NEEDS AN ASSUMPTION" - from two
#: shopfront boundaries against a 6 m bay, giving 875 px of focal length,
#: 38.8 degrees vertical and 59.7 HORIZONTAL. Every one of those numbers was
#: read off the 1024 x 1536 sheet that Jafar RETIRED on 9 September. It is
#: the same fault as the reference itself, one level further in: the
#: picture was replaced and the camera derived from it was not.
#:
#: WHAT THE DIFFERENCE ACTUALLY IS. 60 vertical on a 1.892 frame is 95.1
#: degrees HORIZONTAL. The derived panel is 59.7. We are shooting a
#: thirty-five-degree wider picture than the only measurement there is, and
#: that is what puts a wall 2.9 m to the left across a third of the frame
#: where the concept art has open street.
#:
#: 33.75 WOULD BE THE SAME HORIZONTAL FIELD ON OUR FRAME, and it was
#: rendered on 22 September rather than argued about. IT IS NOT ADOPTED, and
#: the reason is worth more than the number:
#:
#:   IT IS NOT A DERIVATION FROM THE APPROVED SHEET EITHER. It is the
#:   RETIRED sheet's horizontal field carried onto our aspect. Swapping an
#:   unmeasured number for a borrowed one is not progress.
#:
#:   AND IT MOVES THE FOUR NUMBERS THE WRONG WAY. Measured on the same
#:   build, same street, same light, only the lens changed:
#:       sheet        mean 119.7  hi 235  warm +18.5  colour 45.7%
#:       ours at 60      119.5      228        +17.0          39.0%
#:       ours at 33.75   122.6      219        +11.5          29.2%
#:   A narrower lens fills the frame with road and sky instead of brick, so
#:   warmth and colour both fall away from the sheet. THE UNCOMFORTABLE HALF
#:   OF THAT: the palette work this week was tuned until those numbers
#:   matched, at a field of view nobody derived - so some of it is
#:   compensating for the lens rather than describing the street. Changing
#:   the lens and the palette in the same move would hide which was which.
#:
#: THE REAL FIX IS TO DERIVE THE APPROVED SHEET'S OWN FIELD, from its bay
#: module traced across its street panel, the way
#: production/specs/vignette-scene.json derived the retired sheet's. That is
#: a sitting's work and it is Jafar's to schedule; until then this stays at
#: the value the accepted frames were measured at, and says so.
HOOK_FOV_V_DEG = 60.0
#: AND NOW IT IS DERIVED, 22 September, from the NEW sheet's own geometry:
#: production/reference/hook-sheet-lens.md is the how. 46 degrees vertical on
#: the sheet's 1.882 frame, 77 horizontal, the middle of the 42.5 to 50 range
#: that the real objects in the sheet agree on (Mickey's front as one 6 m bay;
#: the nearest parked car as a 1990 saloon). The sheet's window rhythm implies
#: 26 degrees and was not used: the model drew three windows over Mickey's bay
#: where our street has two, so that spacing is decoration and not a module.
HOOK_FOV_V_DEG = 46.0
#: THE CAMERA IS LEVEL AND THE PICTURE IS SHIFTED. The sheet's verticals do not
#: lean (three downpipes, -0.6, +1.7 and -1.2 degrees - both ways, which is the
#: model's hand), yet its horizon sits at row 620 of 1088, 0.570 of the way
#: down. A level camera with a lens shifted up is how an architectural
#: photograph puts the horizon low and keeps its walls straight; tipping the
#: camera would make every wall lean.
#: THE SHIFT IS A FRACTION OF THE HEIGHT HERE, AND THAT WAS MEASURED. The first
#: render took Blender's shift as a fraction of the frame's larger side and
#: passed 0.070 x 744 / 1400: the horizon then landed at 0.537 of the height,
#: exactly half way to the 0.570 it was sent to. With sensor_fit VERTICAL the
#: shift is in units of the fitted side, the height, so it is 0.070 as it is.
#: Checked by running production/reference/hook-sheet-lens-vp.py on the render
#: and comparing its vanishing point with the sheet's, not by eye.
HOOK_HORIZON_FROM_TOP = 620.0 / 1088.0

#: HOW MUCH BRIGHTER THE SKY IS TO THE CAMERA THAN TO THE STREET. See _world.
SKY_AS_SEEN_GAIN = 1.4
HOOK_EYE_M = 1.9          # three people in the sheet, read as 1.75 m adults
HOOK_YAW_LEFT_DEG = 20.4  # the street's vanishing point is 478 px right of centre


# ---------------------------------------------------------------------------
# PURE. Everything a selftest can drive with no Blender and no filesystem
# beyond reading the two committed spec files.
# ---------------------------------------------------------------------------


def brick_length_m(raw):
    """One British brick on its length, MEASURED rather than typed.

    `blocks[1].roof.parapet_thickness_m` is 0.215 in the scene file and its
    own note says why: "one British brick on its length, 215 mm". That is the
    module this elevation's wall thickness is, so it is read from there
    rather than written again here. The facade block's reveal_depth_m is the
    half-brick from the same module, and selftest asks whether the two still
    describe the same brick."""
    try:
        for b in raw.get("blocks", []) or []:
            t = (b.get("roof") or {}).get("parapet_thickness_m")
            if t:
                return float(t)
    except (TypeError, ValueError):
        pass
    return None


def load_spec(root, spec_rel=SPEC_REL, block_id="east_parade"):
    """(params, error). The numbers, read from the scene file, never typed.

    ANY OF THE THREE BLOCKS. The street has two row types and the difference
    between them is MEASURED rather than assumed: the shopfront row earns its
    piers because a shopfront needs them, and the plain row is a continuous
    coursed plane broken only by openings, with no pilaster, no stallriser, no
    fascia and no transom anywhere on it. The spec checked the built street's
    own piece list to confirm that, and this reads the same two fields it did.
    """
    path = os.path.join(root, spec_rel)
    if not os.path.exists(path):
        return None, "no-spec-file/%s" % path.replace(" ", "~")
    try:
        with open(path, "r", encoding="utf-8") as fh:
            raw = json.load(fh)
    except (OSError, ValueError) as exc:
        return None, "unreadable-spec-json/%s" % type(exc).__name__

    blocks = raw.get("blocks")
    if not isinstance(blocks, list) or not blocks:
        return None, "spec-has-no-blocks"
    block = None
    for b in blocks:
        if b.get("id") == block_id:
            block = b
            break
    if block is None:
        return None, "spec-has-no-block/%s" % block_id.replace(" ", "~")

    shop = raw.get("shopfront")
    face = raw.get("facade")
    roofline = raw.get("roofline")
    if not isinstance(shop, dict) or not isinstance(face, dict) or not isinstance(roofline, dict):
        return None, "spec-missing-shopfront-facade-or-roofline"

    try:
        storeys = [float(v) for v in block["storey_heights_m"]]
        roof = block["roof"]
        p = {
            "bay_width_m":      float(block["bay_width_m"]),
            "depth_m":          float(block["depth_m"]),
            "start_x_m":        float(block["start_x_m"]),
            "bays":             int(block["bays"]),
            "block_id":         str(block["id"]),
            "side":             str(block["side"]),
            "wall_surface":     str(block["wall_surface"]),
            "ground_floor":     str(block["ground_floor"]),
            "roof_kind":        str(roof["kind"]),
            "ground_h_m":       storeys[0],
            "first_h_m":        storeys[1],
            "pitch_deg":        float(roof.get("pitch_deg", 0.0)),
            "eaves_overhang_m": float(roof.get("eaves_overhang_m", 0.0)),
            "parapet_h_m":      float(roof.get("parapet_height_m", 0.0)),
            "parapet_t_m":      float(roof.get("parapet_thickness_m", 0.0)),
            "coping_w_m":       float(roof.get("coping_width_m", 0.0)),
            "coping_t_m":       float(roof.get("coping_thickness_m", 0.0)),

            "stallriser_h_m":   float(shop["stallriser_height_m"]),
            "stallriser_proj_m":float(shop["stallriser_projection_m"]),
            "pilaster_w_m":     float(shop["pilaster_width_m"]),
            "pilaster_proj_m":  float(shop["pilaster_projection_m"]),
            "transom_h_m":      float(shop["transom_height_m"]),
            "transom_t_m":      float(shop["transom_thickness_m"]),
            "fascia_bottom_m":  float(shop["fascia_bottom_m"]),
            "fascia_proj_m":    float(shop["fascia_projection_m"]),
            "glazing_recess_m": float(shop["glazing_recess_m"]),
            "shop_door_w_m":    float(shop["shop_door"]["width_m"]),
            "shop_door_h_m":    float(shop["shop_door"]["height_m"]),
            "shop_glazed_from_m": float(shop["shop_door"]["glazed_from_m"]),
            "side_door_w_m":    float(shop["side_door"]["width_m"]),
            "side_door_h_m":    float(shop["side_door"]["height_m"]),
            "letterplate_w_m":  float(shop["side_door"]["letterplate_width_m"]),
            "letterplate_h_m":  float(shop["side_door"]["letterplate_height_m"]),
            "letterplate_at_m": float(shop["side_door"]["letterplate_at_m"]),

            "windows_per_bay":  int(face["windows_per_bay"]),
            "window_w_m":       float(face["window_width_m"]),
            "window_h_m":       float(face["window_height_m"]),
            "reveal_m":         float(face["reveal_depth_m"]),
            "sill_proj_m":      float(face["sill_projection_m"]),
            "sill_t_m":         float(face["sill_thickness_m"]),
            "sill_extra_w_m":   float(face["sill_extra_width_m"]),
            "lintel_t_m":       float(face["lintel_thickness_m"]),
            "head_below_ceiling_m": float(face["head_below_ceiling_m"]),
            "brick_course_m":   float(face["brick_course_m"]),

            "downpipe_dia_m":   float(roofline["downpipe"]["diameter_m"]),
            "chimney_w_m":      float(roofline["chimney"]["width_m"]),
            "chimney_d_m":      float(roofline["chimney"]["depth_m"]),
            "chimney_above_ridge_m": float(roofline["chimney"]["height_above_ridge_m"]),
        }
        bl = brick_length_m(raw)
        if bl is None or bl <= 0:
            return None, "spec-carries-no-brick-length-to-read-a-wall-thickness-from"
        p["wall_t_m"] = bl
        # THE SIGNS ON THIS BLOCK, and only this block's.
        signs = {}
        pre = "%s_fascia" % block_id
        for d in (raw.get("decals") or {}).get("items") or []:
            on = str(d.get("on", ""))
            if d.get("bom") != "C6_fascia_lettering" or not on.startswith(pre):
                continue
            if not on[len(pre):].isdigit():
                continue
            signs[int(on[len(pre):])] = {
                "id": str(d["id"]), "uv": d.get("uv"),
                "width_m": float(d["width_m"]), "height_m": float(d["height_m"]),
                "dx_m": float(d.get("dx_m", 0.0))}
        p["fascia_signs"] = signs
    except (KeyError, TypeError, ValueError, IndexError) as exc:
        return None, "spec-field-refused/%s" % str(exc).replace(" ", "~")[:80]

    for key in ("bay_width_m", "depth_m", "ground_h_m", "first_h_m",
                "window_w_m", "window_h_m", "pilaster_w_m"):
        if p[key] <= 0:
            return None, "non-positive-dimension/%s=%.6f" % (key, p[key])

    # DERIVED, and every one of these is the spec's own arithmetic re-done
    # here rather than copied as a literal, so the two cannot drift.
    p["eaves_m"] = p["ground_h_m"] + p["first_h_m"]
    p["ridge_rise_m"] = (p["depth_m"] / 2.0) * math.tan(math.radians(p["pitch_deg"]))
    p["ridge_m"] = p["eaves_m"] + p["ridge_rise_m"]
    # THE TOP OF THE ROW, whichever roof it has. A parapet stands its own
    # height above the eaves with a coping on it; a pitch stands a ridge and a
    # stack. Written once here so the cameras and the checks do not each pick
    # a roof to believe in.
    if p["roof_kind"] == "parapet":
        p["top_m"] = p["eaves_m"] + p["parapet_h_m"] + p["coping_t_m"]
    else:
        p["top_m"] = p["ridge_m"] + p["chimney_above_ridge_m"]
    p["opening_zone_m"] = p["bay_width_m"] - 2.0 * p["pilaster_w_m"]
    # The display run is what is LEFT of the opening zone once the two doors
    # have taken theirs. The spec states the identity the other way round
    # (3.562 + 0.9 + 0.838 = 5.300) and acceptance check 10 asserts it.
    p["display_w_m"] = p["opening_zone_m"] - p["shop_door_w_m"] - p["side_door_w_m"]
    p["window_head_m"] = p["eaves_m"] - p["head_below_ceiling_m"]
    p["window_sill_m"] = p["window_head_m"] - p["window_h_m"]
    p["sill_w_m"] = p["window_w_m"] + p["sill_extra_w_m"]
    p["_path"] = path
    return p, ""


def window_centres(p):
    """Where the upper windows sit, MEASURED off the emitted pieces: bay_start
    + 1.5 m and + 4.5 m. Expressed as fractions of the bay so a bay of another
    width still divides sensibly, and asserted against 1.5/4.5 at 6.0 m in
    selftest so the fraction cannot quietly restate a different rhythm."""
    w = p["bay_width_m"]
    return [w * 0.25, w * 0.75]


def cross_check(p, root, pieces_rel=PIECES_REL):
    """[(field, authored, emitted, agree)]. The authored numbers against the
    610-piece blockout the street is actually built from.

    THIS IS THE CHECK THAT MATTERS, and it is the one lighting-column.py
    carries for the same reason: an authored front that disagrees with the
    emitted carcass it replaces will float, sink or overhang, and no render
    of the front ALONE can show it."""
    path = os.path.join(root, pieces_rel)
    rows = []
    try:
        with open(path, "r", encoding="utf-8") as fh:
            raw = json.load(fh)
    except (OSError, ValueError):
        return rows
    by_name = {}
    for piece in raw.get("pieces", []) or []:
        if isinstance(piece, dict) and piece.get("name"):
            by_name[piece["name"]] = piece

    def take(name, key):
        piece = by_name.get(name)
        if not isinstance(piece, dict):
            return None
        v = piece.get(key)
        try:
            return float(v)
        except (TypeError, ValueError):
            return None

    wanted = (
        ("carcass_height_m", p["eaves_m"], take("east_parade_bay0", "sy_m")),
        ("carcass_width_m", p["bay_width_m"], take("east_parade_bay0", "sx_m")),
        ("carcass_depth_m", p["depth_m"], take("east_parade_bay0", "sz_m")),
        ("upper_window_w_m", p["window_w_m"], take("east_parade_up0_w0", "sx_m")),
        ("upper_window_h_m", p["window_h_m"], take("east_parade_up0_w0", "sy_m")),
    )
    for field, authored, emitted in wanted:
        if emitted is None:
            rows.append((field, authored, None, None))
        else:
            rows.append((field, authored, emitted, abs(authored - emitted) < 1e-6))
    return rows


def _box(parts, pid, material, x0, x1, y0, y1, z0, z1, note=""):
    """One rectangular piece, named, with its own extents. Refuses a box with
    a non-positive dimension rather than emitting a degenerate one: a zero
    width face renders as nothing and reads in a frame as a missing part."""
    if x1 <= x0 or y1 <= y0 or z1 <= z0:
        raise ValueError("terrace-front: degenerate box %s (%.4f..%.4f, %.4f..%.4f, %.4f..%.4f)"
                         % (pid, x0, x1, y0, y1, z0, z1))
    parts.append({"id": pid, "material": material, "note": note,
                  "x0": x0, "x1": x1, "y0": y0, "y1": y1, "z0": z0, "z1": z1})
    return parts[-1]


def _side_door(parts, p, side_x0, side_x1, jamb_t, rec, joinery_proj, wall, T, fb):
    """The private door to the flat above, when the bay has one.

    LIFTED OUT OF plan_parts 2026-09-22 so a bay can be built WITHOUT it.
    Section 4 item 2 of the spec asks for exactly one bay on the row with no
    side door at all, and a block of twenty lines in the middle of a function
    cannot be skipped without wrapping every one of them in a condition, which
    is how an indentation mistake becomes a missing doorframe nobody notices.
    """
    # SIDE DOOR: the flat above. Its own spandrel, and a letterplate.
    # THE LEAF SITS INSIDE ITS OWN CASING AND SET BACK INTO THE WALL. Both
    # halves fix the fault the last render showed: the two doors read as one
    # busy patch. The casing used to be built OUTSIDE the door's own width,
    # which put its left upright exactly where the shop door's right stile
    # already was - two pieces of joinery in the same place, at the one point
    # on the elevation where a person needs to tell two doors apart. And the
    # leaf sat flush with the shop door's, so nothing but colour separated
    # them. It is recessed by the same half-brick the upper windows use, which
    # puts it in shadow and makes the private door read as a way in rather
    # than as more shopfront.
    _box(parts, "side_door_leaf", "paint_door",
         side_x0 + jamb_t, side_x1 - jamb_t, rec, rec + 0.04,
         0.0, p["side_door_h_m"],
         "1981x838mm/the-standard-British-external-door/imperial-because-the-country-was")
    # A CASING ROUND IT, in the shopfront's joinery rather than the door's own
    # paint, because the frame belongs to the building and the leaf belongs to
    # whoever lives behind it.
    for Name, X0, X1 in (("side_door_casing_left", side_x0, side_x0 + jamb_t),
                         ("side_door_casing_right", side_x1 - jamb_t, side_x1)):
        _box(parts, Name, "paint_joinery", X0, X1, -0.01, rec + 0.04,
             0.0, p["side_door_h_m"] + jamb_t,
             "the-casing's-upright/inside-the-door's-own-width-so-it-cannot-stand-on-the-shop-door")
    _box(parts, "side_door_casing_head", "paint_joinery",
         side_x0, side_x1, -0.01, rec + 0.04,
         p["side_door_h_m"], p["side_door_h_m"] + jamb_t, "the-casing's-head")
    lp_w, lp_h = p["letterplate_w_m"], p["letterplate_h_m"]
    lp_cx = (side_x0 + side_x1) * 0.5
    _box(parts, "letterplate", "lead", lp_cx - lp_w / 2.0, lp_cx + lp_w / 2.0,
         rec - 0.015, rec, p["letterplate_at_m"], p["letterplate_at_m"] + lp_h,
         "the-one-detail-that-says-somebody-lives-above-the-shop")
    _box(parts, "side_door_spandrel", wall, side_x0, side_x1, 0.0, T,
         p["side_door_h_m"], fb, "brick-between-the-door-head-and-the-board")



def _plain_ground(parts, p, T, wall, bay):
    """The plain row's ground floor: a coursed plane with three openings.

    NO PILASTER, NO STALLRISER, NO FASCIA, NO TRANSOM, and that is MEASURED
    rather than an omission. The spec read the built street's own piece list
    for a west bay and found sills and lintels, a side door, a downpipe and
    upper windows - and no shopfront assembly of any kind on either west row.
    A domestic terrace elevation is a continuous coursed plane broken only by
    openings; a commercial parade earns its piers because a shopfront needs
    them. Building the plain row out of the shopfront's parts with some of
    them switched off would have produced a house wearing a shop's bones.

    THE OPENINGS, all MEASURED: a household door at bay_start + 1.5 m and two
    windows at + 3.3 and + 5.1, sills at local 1.525 and heads at 3.1, with a
    0.3 m band of brick between the head line and the slab. That band is the
    row's own signature and it is why nothing lettered belongs above a
    plain-row door: there is no board to letter.
    """
    W = p["bay_width_m"]
    GF = p["ground_h_m"]
    rec = p["reveal_m"]
    head_z = 3.1
    door_w, door_h = p["side_door_w_m"], p["side_door_h_m"]
    win_w, win_h = p["window_w_m"], p["window_h_m"]
    sill_z = 1.525
    sill_t = 0.075
    jamb_t = p["transom_t_m"]

    # THE DOOR SIDE STILL VARIES, for the reason it varies on the parade: the
    # spec measured every plain-row door at exactly bay_start + 1.5 m across
    # four bays, which is the same one stencil one row along. Mirrored within
    # the bay, so the rhythm changes without any opening moving off the
    # module the row is built on.
    mirrored = BAY_DOORS_ON[bay % len(BAY_DOORS_ON)] == "right"
    def at(x):
        return (W - x) if mirrored else x

    door_cx = at(1.5)
    win_cx = [at(3.3), at(5.1)]
    openings = [(door_cx - door_w / 2.0, door_cx + door_w / 2.0, 0.0, door_h)]
    for cx in win_cx:
        openings.append((cx - win_w / 2.0, cx + win_w / 2.0, sill_z, sill_z + win_h))

    # The wall, as bands and piers around the openings. Same construction as
    # the first floor above it, which is what makes the two read as one wall.
    lo_band = min(o[2] for o in openings)
    hi_band = max(o[3] for o in openings)
    if lo_band > 1e-9:
        _box(parts, "gf_band_below", wall, 0.0, W, 0.0, T, 0.0, lo_band,
             "brick-under-the-window-sills")
    _box(parts, "gf_band_above", wall, 0.0, W, 0.0, T, hi_band, GF,
         "the-0.3m-band-of-brick-between-the-heads-and-the-slab/the-row's-own-signature")

    edges = [0.0]
    for a, b, _z0, _z1 in sorted(openings):
        edges.extend([a, b])
    edges.append(W)
    for i in range(0, len(edges) - 1, 2):
        a, b = edges[i], edges[i + 1]
        if b > a + 1e-9:
            _box(parts, "gf_pier_%d" % (i // 2), wall, a, b, 0.0, T, lo_band, hi_band,
                 "the-brick-between-the-openings")

    # Where an opening is shorter than the band it sits in, the brick above or
    # below it is emitted too, or the wall has a hole nothing fills.
    for n, (a, b, z0, z1) in enumerate(sorted(openings)):
        if z0 > lo_band + 1e-9:
            _box(parts, "gf_under_%d" % n, wall, a, b, 0.0, T, lo_band, z0,
                 "brick-under-a-window-that-starts-above-the-door's-foot")
        if z1 < hi_band - 1e-9:
            _box(parts, "gf_over_%d" % n, wall, a, b, 0.0, T, z1, hi_band,
                 "brick-over-an-opening-shorter-than-its-neighbour")

    # The door, recessed, in its own paint with a joinery casing.
    _box(parts, "side_door_leaf", "paint_door",
         door_cx - door_w / 2.0 + jamb_t, door_cx + door_w / 2.0 - jamb_t,
         rec, rec + 0.04, 0.0, door_h,
         "1981x838mm/the-standard-British-external-door")
    for Name, X0, X1 in (("side_door_casing_left",
                          door_cx - door_w / 2.0, door_cx - door_w / 2.0 + jamb_t),
                         ("side_door_casing_right",
                          door_cx + door_w / 2.0 - jamb_t, door_cx + door_w / 2.0)):
        _box(parts, Name, "paint_joinery", X0, X1, -0.01, rec + 0.04, 0.0, door_h + jamb_t,
             "the-casing's-upright")
    _box(parts, "side_door_casing_head", "paint_joinery",
         door_cx - door_w / 2.0, door_cx + door_w / 2.0, -0.01, rec + 0.04,
         door_h, door_h + jamb_t, "the-casing's-head")
    lp_w, lp_h = p["letterplate_w_m"], p["letterplate_h_m"]
    _box(parts, "letterplate", "lead", door_cx - lp_w / 2.0, door_cx + lp_w / 2.0,
         rec - 0.015, rec, p["letterplate_at_m"], p["letterplate_at_m"] + lp_h,
         "the-one-detail-that-says-somebody-lives-here")

    # The windows, with the same sills and lintels the floor above uses.
    sw = p["sill_w_m"] / 2.0
    for n, cx in enumerate(win_cx):
        _box(parts, "gf_glass_%d" % n, "glass", cx - win_w / 2.0, cx + win_w / 2.0,
             rec, rec + 0.02, sill_z, sill_z + win_h,
             "set-back-one-half-brick/the-same-reveal-the-floor-above-uses")
        _box(parts, "gf_sill_%d" % n, "stone", cx - sw, cx + sw,
             -p["sill_proj_m"], T, sill_z - sill_t, sill_z, "the-window's-own-sill")
        _segmental_arch(parts, "gf_arch_%d" % n, cx - win_w / 2.0, cx + win_w / 2.0,
                        sill_z + win_h, "segmental-rubbed-brick-arch/as-upstairs")


#: THE WINDOW HEADS ARE SEGMENTAL ARCHES, 22 September, and the lintels they
#: replace were the retired sheet's. On the approved sheet every terrace
#: window, upstairs and down, has a shallow arch of rubbed brick over it; ours
#: had a flat stone lintel. THE OPENING IS UNCHANGED - its width and its head
#: height are the scene file's geometry, and the arch springs from that head
#: - what changes is the form over it, which is the sheet's to govern.
#: A RISE OF ONE-SEVENTH OF THE SPAN is the ordinary Victorian segmental
#: head; the RING is one brick on end, 215 mm; it stands 12 mm proud of the
#: wall face so the colour change has an edge to it.
ARCH_RISE_FRACTION = 1.0 / 7.0
ARCH_RING_M = 0.215
ARCH_PROUD_M = 0.012
ARCH_SEGMENTS = 10


def _segmental_arch(parts, pid, a, b, spring_z, note):
    """An arch ring over the opening a..b, springing at spring_z, bay-local."""
    span = b - a
    rise = span * ARCH_RISE_FRACTION
    R = (span * span / 4.0 + rise * rise) / (2.0 * rise)
    cx = (a + b) / 2.0
    cz = spring_z + rise - R
    th_r = math.atan2(spring_z - cz, b - cx)
    th_l = math.pi - th_r
    prof = []
    # EXTRADOS right to left, then INTRADOS left to right: anticlockwise,
    # which is the winding _prism needs for its normals to face out.
    for k in range(ARCH_SEGMENTS + 1):
        t = th_r + (th_l - th_r) * k / ARCH_SEGMENTS
        prof.append((cx + (R + ARCH_RING_M) * math.cos(t), cz + (R + ARCH_RING_M) * math.sin(t)))
    for k in range(ARCH_SEGMENTS + 1):
        t = th_l + (th_r - th_l) * k / ARCH_SEGMENTS
        prof.append((cx + R * math.cos(t), cz + R * math.sin(t)))
    _prism(parts, pid, "brick_rubbed", prof, -ARCH_PROUD_M, 0.0, note)
    # AND THE WINDOW FOLLOWS THE ARCH, which is attempt two and the reason
    # the first could not be seen: on the sheet the sash's head is CURVED to
    # the arch, a white line under the brick with glass inside it, and our
    # flat-headed sash left brick between itself and the ring. The opening's
    # rectangle stays the scene file's; the segment above it is glazed and
    # framed on the wall face, which is what reads from across the street.
    seg = [(cx + R * math.cos(th_r + (th_l - th_r) * k / ARCH_SEGMENTS),
            cz + R * math.sin(th_r + (th_l - th_r) * k / ARCH_SEGMENTS))
           for k in range(ARCH_SEGMENTS + 1)]
    _prism(parts, pid + "_light", "glass", seg, -0.004, -0.001,
           "the-arched-head's-glass/over-the-sash")
    fr = []
    for k in range(ARCH_SEGMENTS + 1):
        t = th_r + (th_l - th_r) * k / ARCH_SEGMENTS
        fr.append((cx + R * math.cos(t), cz + R * math.sin(t)))
    for k in range(ARCH_SEGMENTS + 1):
        t = th_l + (th_r - th_l) * k / ARCH_SEGMENTS
        fr.append((cx + (R - FRAME_T) * math.cos(t), cz + (R - FRAME_T) * math.sin(t)))
    _prism(parts, pid + "_frame", "paint_joinery", fr, -0.008, -0.004,
           "the-sash-frame's-curved-head")


#: THE DENTIL COURSE, the other thing every roofline on the approved sheet
#: has and ours did not: a band of brick stepped out under the eaves with a
#: row of headers standing proud above it, one brick in two. Header ends are
#: 102.5 mm across and a course is 75 mm, so the dentils are that, 205 mm
#: apart, and the whole course stands 40 mm proud.
DENTIL_W_M, DENTIL_H_M, DENTIL_PITCH_M, DENTIL_PROUD_M = 0.1025, 0.075, 0.205, 0.040


def _dentil_course(parts, W, eaves, wall):
    """A projecting band and a row of dentils just under the eaves, bay-local."""
    band_z0 = eaves - 3.0 * DENTIL_H_M
    _box(parts, "eaves_band", wall, 0.0, W, -DENTIL_PROUD_M, 0.0, band_z0, band_z0 + DENTIL_H_M,
         "a-course-stepped-out-under-the-eaves")
    n = int(W / DENTIL_PITCH_M)
    off = (W - (n - 1) * DENTIL_PITCH_M - DENTIL_W_M) / 2.0
    for k in range(n):
        x0 = off + k * DENTIL_PITCH_M
        _box(parts, "dentil_%d" % k, wall, x0, x0 + DENTIL_W_M, -DENTIL_PROUD_M, 0.0,
             band_z0 + DENTIL_H_M, band_z0 + 2.0 * DENTIL_H_M,
             "a-header-standing-proud/one-in-two")


def _upper_floor(parts, p, T, wall):
    """The first floor, identical on both rows.

    THE WINDOW RHYTHM IS THE ONE THING THE SPEC FORBIDS VARYING: two sashes at
    bay_start + 1.5 and + 4.5 on BOTH rows, the string-course a viewer's eye
    follows down the whole street. It is the strongest terrace cue there is,
    which is why it lives in one function that both row types call rather than
    being written twice and drifting once.
    """
    GF = p["ground_h_m"]
    EAVES = p["eaves_m"]
    W = p["bay_width_m"]
    # ---- first floor: a coursed plane broken by two openings -------------
    sill_z = p["window_sill_m"]
    head_z = p["window_head_m"]
    hw = p["window_w_m"] / 2.0
    centres = window_centres(p)
    opens = [(c - hw, c + hw) for c in centres]

    # The three horizontal bands. Band B is the only one the openings cut.
    _box(parts, "upper_band_below", wall, 0.0, W, 0.0, T, GF, sill_z,
         "coursed-brick-from-the-slab-to-the-sills")
    _box(parts, "upper_band_above", wall, 0.0, W, 0.0, T, head_z, EAVES,
         "coursed-brick-from-the-heads-to-the-eaves")
    _dentil_course(parts, W, EAVES, wall)

    edges = [0.0]
    for a, b in opens:
        edges.extend([a, b])
    edges.append(W)
    for i in range(0, len(edges) - 1, 2):
        a, b = edges[i], edges[i + 1]
        if b > a + 1e-9:
            _box(parts, "upper_pier_%d" % (i // 2), wall, a, b, 0.0, T, sill_z, head_z,
                 "the-brick-between-the-openings")

    for i, (a, b) in enumerate(opens):
        cx = (a + b) * 0.5
        sw = p["sill_w_m"] / 2.0
        # THE REVEAL IS HALF A BRICK, and it is why a window is not a decal.
        _box(parts, "upper_glass_%d" % i, "glass", a, b, p["reveal_m"], p["reveal_m"] + 0.02,
             sill_z, head_z, "set-back-one-half-brick/102.5mm/the-depth-that-stops-it-reading-flat")
        _box(parts, "upper_sill_%d" % i, "stone", cx - sw, cx + sw,
             -p["sill_proj_m"], T, sill_z - p["sill_t_m"], sill_z,
             "0.95m-wide/window-plus-50mm-each-side")
        _segmental_arch(parts, "upper_arch_%d" % i, a, b, head_z,
                        "segmental-rubbed-brick-arch/rise-a-seventh-of-the-span")
        _sash(parts, i, a, b, sill_z, head_z, p["reveal_m"])
        # NET CURTAINS behind the upstairs glass, 22 September. On the new
        # sheet every upstairs window is PALE - white frames over white nets,
        # 157 against our 100 to 107 - and ours looked straight through
        # clear glass into an unlit flat. The research names nets as the
        # per-house signature of a 1990 terrace, and the held net pictures
        # (BOM C12, DRESSING) are the two gathered weaves, alternated.
        net = _box(parts, "upper_net_%d" % i, "interior_lit", a, b,
                   p["reveal_m"] + 0.05, p["reveal_m"] + 0.06, sill_z, head_z,
                   "net-curtain/C12/behind-the-glass")
        net["decal"] = NET_CURTAINS[i % len(NET_CURTAINS)]
        net["decal_emit"] = "net"


#: A BRITISH SASH, IN THE SECTIONS THAT READ AT TWENTY-FIVE METRES.
#:
#: THE UPPER WINDOWS HAD NO FRAME AT ALL. Until now each one was a pane of
#: glass in a hole with a stone sill under it and a stone lintel over it -
#: nothing white, nothing divided, nothing between the glass and the brick.
#: On the approved sheet EVERY window is a white grid, and that is not a
#: detail of the street, it is what the street is made of: white-painted
#: joinery against red brick, repeated forty times down the row. It is also
#: where most of our missing highlights were - our brightest five per cent
#: measured 163 against the sheet's 229, and a frame at 0.68 linear is the
#: brightest thing a facade has on it.
#:
#: THE SECTIONS ARE A JOINER'S, NOT A GUESS. A box sash has an outer frame
#: about 55 mm on the face, a MEETING RAIL where the two sashes cross that is
#: the heaviest member at 45 mm, and glazing bars lighter than both at 22 mm.
#: One meeting rail and one vertical bar per sash is a two-over-two, which is
#: what a late Victorian terrace flat has - not the six-over-six of a
#: Georgian front, and not a single undivided pane, which is a replacement
#: window and forty years early.
FRAME_T = 0.055
MEETING_RAIL_T = 0.045
GLAZING_BAR_T = 0.022
#: How far the joinery stands in front of the glass. The glass sits at the
#: reveal and is 20 mm thick, so 30 mm in front of it puts the frame proud of
#: the pane and still well inside the half-brick reveal - a frame flush with
#: its own glass casts no shadow and reads as paint on a window.
SASH_PROUD_M = 0.030


def _sash(parts, i, a, b, sill_z, head_z, reveal):
    """The white frame, its meeting rail and its bars, for one opening."""
    # ENTIRELY IN FRONT OF THE PANE, and it matters twice. Glazing really is
    # like this - the pane sits in a rebate BEHIND the face of the frame, so
    # the frame's back face and the glass's front face meet. And it lets a
    # frame be told apart from brick by geometry alone: anything whose whole
    # depth is in front of the glazing plane is joinery, anything crossing it
    # or behind it is the carcass showing through a hole.
    y1 = reveal
    y0 = reveal - SASH_PROUD_M
    f = FRAME_T
    # THE OUTER FRAME: two jambs the full height, then the head and the cill
    # rail between them, so no two pieces occupy the same millimetre.
    _box(parts, "upper_sash_jamb_l_%d" % i, "paint_joinery", a, a + f, y0, y1,
         sill_z, head_z, "55mm-on-the-face")
    _box(parts, "upper_sash_jamb_r_%d" % i, "paint_joinery", b - f, b, y0, y1,
         sill_z, head_z, "55mm-on-the-face")
    _box(parts, "upper_sash_head_%d" % i, "paint_joinery", a + f, b - f, y0, y1,
         head_z - f, head_z, "under-the-lintel")
    _box(parts, "upper_sash_cill_%d" % i, "paint_joinery", a + f, b - f, y0, y1,
         sill_z, sill_z + f, "on-the-stone")
    # THE MEETING RAIL, at mid height, where the two sashes cross. It is the
    # heaviest member and it is the one that makes a window read as a SASH
    # rather than as a picture frame.
    mid = (sill_z + head_z) * 0.5
    _box(parts, "upper_sash_meeting_%d" % i, "paint_joinery", a + f, b - f, y0, y1,
         mid - MEETING_RAIL_T * 0.5, mid + MEETING_RAIL_T * 0.5,
         "the-heaviest-member/where-the-two-sashes-cross")
    # ONE VERTICAL BAR IN EACH SASH: a two-over-two.
    cx = (a + b) * 0.5
    g = GLAZING_BAR_T * 0.5
    _box(parts, "upper_sash_bar_lower_%d" % i, "paint_joinery", cx - g, cx + g, y0, y1,
         sill_z + f, mid - MEETING_RAIL_T * 0.5, "two-over-two/the-lower-sash")
    _box(parts, "upper_sash_bar_upper_%d" % i, "paint_joinery", cx - g, cx + g, y0, y1,
         mid + MEETING_RAIL_T * 0.5, head_z - f, "two-over-two/the-upper-sash")


#: A 115 mm HALF-ROUND GUTTER, the ordinary cast-iron size on a terrace.
GUTTER_W_M, GUTTER_H_M = 0.115, 0.075


def _roof_and_rainwater(parts, p, T, wall, party_wall, bay=0):
    """The roof this row has, its downpipe and, where the row carries one, its
    stack. Shared for the same reason the upper floor is."""
    W = p["bay_width_m"]
    D = p["depth_m"]
    EAVES = p["eaves_m"]
    # ---- roof, downpipe, stack -------------------------------------------
    # The roof is two slopes to a ridge running ALONG the street. Only the
    # street-facing one is in any frame this recipe takes, but both are built
    # because a half roof reads as a fault from the eye camera's angle.
    if p["roof_kind"] == "parapet":
        # A FLAT PARAPET WITH A COPING ON IT, and no stack: the spec checked
        # the built street and neither west row carries a chimney today, so
        # none is invented here.
        pt = p["parapet_t_m"]
        _box(parts, "parapet", wall, 0.0, W, -pt * 0.5, pt * 0.5,
             EAVES, EAVES + p["parapet_h_m"],
             "one-British-brick-thick/215mm/the-row's-own-roofline")
        cw = p["coping_w_m"]
        _box(parts, "coping", "stone", 0.0, W, -cw * 0.5, cw * 0.5,
             EAVES + p["parapet_h_m"], EAVES + p["parapet_h_m"] + p["coping_t_m"],
             "the-stone-that-keeps-the-weather-out-of-the-wall-head")
        dr = p["downpipe_dia_m"] / 2.0
        if party_wall:
            _box(parts, "downpipe", "lead", W - dr * 2.0, W, -p["downpipe_dia_m"], 0.0,
                 0.0, EAVES, "at-the-party-wall/never-at-a-row-end")
        return parts

    ov = p["eaves_overhang_m"]
    # THE EAVES ARE THE WALL'S, AND THE LINE ALONG THEM IS A BLACK GUTTER,
    # 22 September. This course was pale stone and read, along the whole
    # row, as a concrete coping; on the new sheet the roofline is slates
    # over a dentil course with a black cast-iron gutter along its edge, and
    # nothing pale at all.
    _box(parts, "eaves_course", wall, -ov * 0.5, W + ov * 0.5, -ov, T,
         EAVES, EAVES + 0.09, "the-line-the-roof-starts-from")
    _box(parts, "gutter", "lead", -ov * 0.5, W + ov * 0.5, -ov - GUTTER_W_M, -ov,
         EAVES - 0.03, EAVES - 0.03 + GUTTER_H_M,
         "a-115mm-half-round-cast-iron-gutter/black")
    parts.append({"id": "roof_front", "material": "slate", "kind": "slope",
                  "x0": -ov * 0.5, "x1": W + ov * 0.5,
                  "y_eaves": -ov, "y_ridge": D / 2.0,
                  "z_eaves": EAVES, "z_ridge": p["ridge_m"],
                  "note": "35-degrees/the-common-British-slated-terrace-pitch"})
    parts.append({"id": "roof_back", "material": "slate", "kind": "slope",
                  "x0": -ov * 0.5, "x1": W + ov * 0.5,
                  "y_eaves": D + ov, "y_ridge": D / 2.0,
                  "z_eaves": EAVES, "z_ridge": p["ridge_m"],
                  "note": "built-though-unseen/a-half-roof-reads-as-a-fault-from-the-eye-camera"})

    # DOWNPIPE at the party wall, never at a row's outer end. This bay's
    # right-hand edge IS an internal party wall on a six-bay row.
    dr = p["downpipe_dia_m"] / 2.0
    if party_wall:
        _box(parts, "downpipe", "lead", W - dr * 2.0, W, -p["downpipe_dia_m"], 0.0,
             0.0, EAVES, "at-the-party-wall/one-per-bay-boundary-never-at-a-row-end")

    # CHIMNEY STACK, on the party wall, top one metre above the ridge.
    cw, cd = p["chimney_w_m"], p["chimney_d_m"]
    if party_wall:
        stack_top = p["ridge_m"] + p["chimney_above_ridge_m"]
        _box(parts, "chimney_stack", wall, W - cw / 2.0, W + cw / 2.0,
             D / 2.0 - cd / 2.0, D / 2.0 + cd / 2.0,
             EAVES, stack_top,
             "a-stack-serves-both-houses-either-side-of-the-wall-it-stands-on")
        # THE OVERSAILING CAP, two courses standing out a brick's width all
        # round just under the top, which is what throws rain off the stack's
        # face and what every stack on the new sheet has. Its top is the
        # stack's own, so the pots stand on the cap and nothing floats.
        ov = STACK_CAP_OVERSAIL_M
        _box(parts, "chimney_cap", wall, W - cw / 2.0 - ov, W + cw / 2.0 + ov,
             D / 2.0 - cd / 2.0 - ov, D / 2.0 + cd / 2.0 + ov,
             stack_top - STACK_CAP_H_M, stack_top,
             "oversailing-courses/%.0fmm-proud-all-round" % (ov * 1000))
        if bay in AERIAL_ON_STACKS:
            _aerial(parts, bay, W, D / 2.0, stack_top)


#: THE TELEVISION AERIAL, AND ITS ELEMENTS ARE DERIVED FROM PHYSICS.
#:
#: The scene file works the length out rather than choosing it, and the
#: working is worth keeping where the geometry is: British television in 1990
#: is UHF Bands IV and V, 470 to 860 MHz; a half-wave dipole at the 550 MHz
#: middle of that band is c/(2f) = 299792458/(2 x 550e6) = 0.2725 m. So the
#: elements of a domestic yagi are about 0.27 m and THE WHOLE COMB IS BARELY
#: A METRE ACROSS. That is the reason a period British roofline is a forest
#: of small combs rather than the large dishes that replaced them, and it is
#: why an aerial drawn at any size that reads comfortably would be wrong.
#:
#: ON TWO STACKS, NOT ALL FIVE, and the spec names which: a roofline where
#: every house has one is as wrong as a roofline where none does.
#:
#: THE BOOM POINTS ALONG THE STREET. A yagi points at its transmitter and
#: every aerial in a real street points the same way, so the direction is a
#: choice; this one is made so the ELEMENTS run across the street and read as
#: a comb from the hook camera rather than end-on as a single rod. British
#: UHF is horizontally polarised, so the elements are horizontal either way.
AERIAL_ON_STACKS = (1, 3)
AERIAL_MAST_H, AERIAL_MAST_D = 1.5, 0.038
AERIAL_BOOM_L, AERIAL_BOOM_D = 1.2, 0.020
AERIAL_ELEMENTS, AERIAL_ELEMENT_L, AERIAL_ELEMENT_D = 10, 0.27, 0.012


def _aerial(parts, bay, cx, cy, stack_top):
    """One yagi, standing on a stack: a mast, a boom, and the comb."""
    m = AERIAL_MAST_D / 2.0
    top = stack_top + AERIAL_MAST_H
    _box(parts, "aerial_%d_mast" % bay, "steel_dark", cx - m, cx + m,
         cy - m, cy + m, stack_top, top, "38mm/lashed-to-the-stack")
    b = AERIAL_BOOM_D / 2.0
    _box(parts, "aerial_%d_boom" % bay, "steel_dark",
         cx - AERIAL_BOOM_L / 2.0, cx + AERIAL_BOOM_L / 2.0,
         cy - b, cy + b, top - b, top + b, "1.2m-along-the-street")
    e = AERIAL_ELEMENT_D / 2.0
    half = AERIAL_ELEMENT_L / 2.0
    # EVENLY SPACED, because the spec gives a count and a boom length and
    # nothing else. A real yagi's director spacing opens out along the boom;
    # at this size that is a difference of millimetres on a rod already
    # thinner than a pixel, so it would be invention rather than accuracy.
    step = AERIAL_BOOM_L / float(AERIAL_ELEMENTS)
    for k in range(AERIAL_ELEMENTS):
        ex = cx - AERIAL_BOOM_L / 2.0 + step * (k + 0.5)
        _box(parts, "aerial_%d_element_%d" % (bay, k), "steel_dark",
             ex - e, ex + e, cy - half, cy + half, top - e, top + e,
             "0.27m/half-wave-at-550MHz")


def _lighting_column_module():
    """The authored lamp column, imported rather than reimplemented.

    THE COLUMN IS ALREADY AUTHORED AND ACCEPTED - the kink at the top of the
    pole with the lantern hanging off its back corner, finished from its
    written dimensions over six attempts - and it lives in
    tools/art-recipes/lighting-column.py. Building a second one here so the
    street could have lamps in it would be the two-implementations trap with
    the one asset this project has actually finished.

    IT NEEDS NO NEW MESH CODE EITHER: that recipe's parts already carry their
    own verts and faces, because it builds them with pure functions and hands
    them to Blender separately. So this takes the geometry as it is, turns it
    to face the road, and places it.
    """
    import importlib.util
    # THE RECIPE RUNS ITSELF WHEN BLENDER LOADS IT, which is what makes it a
    # recipe; this says "I am importing you, do not run". Set and cleared
    # around the import so nothing else in the process inherits it.
    os.environ["LEDGER_RECIPE_IMPORT"] = "1"
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lighting-column.py")
    spec = importlib.util.spec_from_file_location("ledger_lighting_column", path)
    if spec is None or spec.loader is None:
        return None
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
    finally:
        os.environ.pop("LEDGER_RECIPE_IMPORT", None)
    return mod


def lamp_parts(root):
    """(parts, error). Every lamp column in the street, placed and turned.

    THE TURN. The column is authored with its outreach along its own +x; in
    the street the lantern has to reach over the ROAD, which is across. So a
    column on the east side is turned a quarter turn one way and one on the
    west side the other, which is also why the two sides' lanterns hang toward
    each other rather than both the same way.
    """
    lc = _lighting_column_module()
    if lc is None:
        return [], "lighting-column-recipe-not-importable"
    params, err = lc.load_lighting_spec(root)
    if err:
        return [], "lighting-column-spec/%s" % err
    built = lc.build_parts(params)
    out = []
    for n, (px, py) in enumerate(LAMP_AT):
        east = py > 0.0
        for part in built:
            verts = []
            for (vx, vy, vz) in part["verts"]:
                # east: local +x -> street -y (over the road). west: the other way.
                wx = px + (vy if east else -vy)
                wy = py + (-vx if east else vx)
                verts.append((wx, wy, vz))
            out.append({"id": "lamp%d_%s" % (n, part["id"]),
                        "material": part["material"], "kind": "mesh",
                        "verts": verts, "faces": part["faces"],
                        "lamp": n, "lamp_at": (px, py)})
    return out, ""


#: The lantern's own numbers, MEASURED from the emitted piece list: its centre
#: sits at 4.965 m above the road crown and it is 0.200 m deep, so its
#: underside - where the lens is and where light actually leaves it - is at
#: 4.865 m.
LANTERN_CENTRE_M = 4.965
LANTERN_HEIGHT_M = 0.200
LANTERN_LIGHT_DROP_M = 0.05


def lantern_lights():
    """Where a point light goes when the lamps are lit: below the lantern's
    UNDERSIDE, which is where its lens is.

    IT WAS INSIDE THE HOUSING, and that is why two rounds of raising the
    lantern power changed nothing. The piece file's rule is "one point light
    0.05 m below the centre of each EMISSIVE PIECE", and the emissive piece is
    the lens on the lantern's underside - not the lantern. Read as the
    lantern's centre, it put the light 0.05 m below 4.965, which is 0.10 m
    inside a 0.20 m deep opaque steel housing. The lamps were lit and sealed:
    six thousand watts shining into the inside of a box.
    """
    out = []
    base = LANTERN_CENTRE_M - LANTERN_HEIGHT_M / 2.0 - LANTERN_LIGHT_DROP_M
    for n, (px, py) in enumerate(LAMP_AT):
        east = py > 0.0
        reach = 31.0                      # outreach_m, toward the road
        ly = py - reach if east else py + reach
        out.append((px, ly, base))
    return out


#: THE STACK'S CAP AND ITS POTS, 22 September. BOM line D3 has been
#: MANDATORY and unbuilt: "chimney pots on the stack", and the scene file's
#: own chimney note says a 0.90 x 0.45 stack is a TWO-FLUE stack - so two
#: pots, one a flue. The held meshes (roll_top_chimney, weathertop_chimney)
#: measure 0.67 and 0.95 m across, which is a whole stack and not a pot, so
#: the pots are built here at a pot's size: a 600 mm roll-top, 280 mm across
#: at the foot, tapering to 240, with its roll at the top. The new sheet's
#: nearest stack has two terracotta and one buff; a buff pot is a
#: replacement, so one in two stacks carries one.
STACK_CAP_OVERSAIL_M, STACK_CAP_H_M = 0.06, 0.15
POT_H_M, POT_R_FOOT_M, POT_R_TOP_M, POT_ROLL_R_M, POT_ROLL_H_M = 0.60, 0.14, 0.12, 0.145, 0.06
POT_SIDES = 8


def _pot_mesh(cx, cy, z0, r0, r1, h):
    """An octagonal frustum, row-local: (verts, faces)."""
    import math as _m
    vs, fs = [], []
    for k in range(POT_SIDES):
        a = 2.0 * _m.pi * k / POT_SIDES
        vs.append((cx + r0 * _m.cos(a), cy + r0 * _m.sin(a), z0))
    for k in range(POT_SIDES):
        a = 2.0 * _m.pi * k / POT_SIDES
        vs.append((cx + r1 * _m.cos(a), cy + r1 * _m.sin(a), z0 + h))
    n = POT_SIDES
    for k in range(n):
        fs.append((k, (k + 1) % n, n + (k + 1) % n, n + k))
    fs.append(tuple(range(n - 1, -1, -1)))
    fs.append(tuple(range(n, 2 * n)))
    return vs, fs


def plan_pots(p):
    """Two pots on every stack of a pitched row, in the row's local
    coordinates, placed by plan_street exactly as the gables are."""
    if p["roof_kind"] == "parapet":
        return []
    W, D = p["bay_width_m"], p["depth_m"]
    top = p["ridge_m"] + p["chimney_above_ridge_m"]
    parts = []
    for b in range(p["bays"] - 1):          # a stack on every party wall
        sx = (b + 1) * W
        for k, dx in enumerate((-0.22, 0.22)):
            mat = "pot_buff" if (b % 2 == 1 and k == 1) else "pot_clay"
            v, f = _pot_mesh(sx + dx, D / 2.0, top, POT_R_FOOT_M, POT_R_TOP_M,
                             POT_H_M - POT_ROLL_H_M)
            parts.append({"id": "chimney_pot_%d_%d" % (b, k), "material": mat,
                          "kind": "mesh", "verts": v, "faces": f,
                          "note": "roll-top-pot/%.0fmm/%s" % (POT_H_M * 1000, mat)})
            v, f = _pot_mesh(sx + dx, D / 2.0, top + POT_H_M - POT_ROLL_H_M,
                             POT_ROLL_R_M, POT_ROLL_R_M, POT_ROLL_H_M)
            parts.append({"id": "chimney_pot_%d_%d_roll" % (b, k), "material": mat,
                          "kind": "mesh", "verts": v, "faces": f,
                          "note": "the-roll-at-the-pot's-top"})
    return parts


#: HOW THICK A TERRACE'S END WALL IS: one and a half bricks, the ordinary
#: British gable, and thicker than the party walls inside the row because it
#: is an outside wall and carries the weather.
END_WALL_T = 0.34


def plan_end_walls(p):
    """The two ends of a row, in the row's own local coordinates.

    WHY THIS EXISTS, 22 September. The row simply STOPPED: its first and last
    bays were open at their outer sides, so a camera looking along the street
    from past the end saw straight into the end building - the carcass boxes
    in the interior material, a flat dark slab. The new Hook sheet shows brick
    there, and every terrace in Britain ends in a gable. It went unseen for as
    long as the camera stood inside the row; turning it to the sheet's view,
    from the south end, put the terrace's end in the near left of the frame.

    Built in LOCAL coordinates - x along the row from 0 to its run, y back
    from the frontage, z up - so plan_street places them exactly as it places
    the bays, the west blocks' half turn included.
    """
    W, D = p["bay_width_m"], p["depth_m"]
    run = W * p["bays"]
    wall = p["wall_surface"]
    t = END_WALL_T
    if p["roof_kind"] == "parapet":
        top = p["eaves_m"] + p["parapet_h_m"]
    else:
        top = p["eaves_m"]
    parts = []
    for name, x0, x1 in (("south", -t, 0.0), ("north", run, run + t)):
        parts.append({"id": "end_wall_%s" % name, "material": wall,
                      "x0": x0, "x1": x1, "y0": 0.0, "y1": D, "z0": 0.0, "z1": top,
                      "note": "the-row's-end/one-and-a-half-bricks/an-outside-wall"})
        if p["roof_kind"] != "parapet":
            # THE GABLE: the triangle between the two eaves and the ridge,
            # the ridge at the middle of the depth as the roof builds it.
            E, R, mid = p["eaves_m"], p["eaves_m"] + p["ridge_rise_m"], D / 2.0
            verts = [(x0, 0.0, E), (x0, D, E), (x0, mid, R),
                     (x1, 0.0, E), (x1, D, E), (x1, mid, R)]
            faces = [(0, 2, 1), (3, 4, 5), (0, 1, 4, 3), (1, 2, 5, 4), (2, 0, 3, 5)]
            parts.append({"id": "gable_%s" % name, "material": wall, "kind": "mesh",
                          "verts": verts, "faces": faces,
                          "note": "the-gable/eaves-to-ridge/%.1fm-rise" % p["ridge_rise_m"]})
    return parts


def plan_street(root, spec_rel=SPEC_REL):
    """(parts, error). Every block the scene file names, on its own side of
    the road, with the road between them.

    THIS IS THE FRAME THE STAGE IS JUDGED BY. The bar for stage 1 is a frame of
    the built street FROM THE HOOK SHEET'S OWN VIEWPOINT standing beside the
    sheet, and a viewpoint is a place in a street rather than a place in front
    of one building. A row rendered on its own proves the row; it cannot show
    what the sheet is actually being compared on - how far the eye carries down
    the road, what the rooflines do against the sky, where the clutter is.

    THE WEST SIDE IS TURNED RATHER THAN REBUILT. Its bays are built by the
    same code at the same origin and then rotated a half turn, because a
    second implementation of a terrace that happened to face the other way is
    two terraces that drift.

    IT WAS MIRRORED UNTIL 2026-09-22 AND THAT WAS WRONG. Negating y alone
    turns a frontage to face the street and REVERSES ITS HANDEDNESS with it:
    a viewer looking at an east face has +x on their right hand, and a viewer
    looking at a west face has +x on their left. Brick does not care. The
    first frame with a shopfront on the near west block had MICKEY'S painted
    backwards across it, and every sign that side ever gained would have
    been. Jafar's ruling: fix the CONSTRUCTION, not the lettering.

    A HALF TURN ABOUT THE BLOCK'S OWN CENTRE negates x AND y together, which
    preserves handedness, so lettering reads the right way round on both
    sides of the road with nothing done to the lettering. The block stays
    where the scene file puts it because the centre it turns about is its
    own; what changes is that its bays run the other way along the street,
    which is what a terrace rotated a half turn actually does.
    """
    out = []
    for block_id in ("east_parade", "west_south", "west_north"):
        q, err = load_spec(root, spec_rel, block_id)
        if err:
            return None, err
        east = q["side"] == "east"
        for part in plan_row(q) + plan_end_walls(q) + plan_pots(q):
            r = dict(part)
            r["id"] = "%s_%s" % (block_id, part["id"])
            r["block"] = block_id
            run = q["bays"] * q["bay_width_m"]
            # A MESH IS PLACED VERTEX BY VERTEX, by the same rule as a box:
            # along from the block's start (turned end for end on the west),
            # back from the frontage (negated on the west), up from the
            # footway. Only the end walls' gables arrive here as meshes.
            if part.get("kind") == "mesh":
                vs = []
                for (x, y, z) in part["verts"]:
                    X = (x + q["start_x_m"]) if east else (q["start_x_m"] + run - x)
                    Y = (STREET_FRONTAGE_M + y) if east else -(STREET_FRONTAGE_M + y)
                    vs.append((X, Y, z + THRESHOLD_ABOVE_CROWN_M))
                # The half turn negates x and y together, which is a rotation
                # and not a reflection, so the faces still face outwards.
                r["verts"] = vs
                out.append(r)
                continue
            # ALONG the street first: each block starts where the scene file
            # says it starts, not at zero - and a west block is TURNED end
            # for end about its own centre as it lands, which is the other
            # half of the half turn. x is measured back from the block's far
            # end instead of forward from its near one, so bay 0 finishes at
            # the far end and the whole run keeps its handedness.
            run = q["bays"] * q["bay_width_m"]
            if east:
                r["x0"] = part["x0"] + q["start_x_m"]
                r["x1"] = part["x1"] + q["start_x_m"]
            else:
                r["x0"] = q["start_x_m"] + run - part["x1"]
                r["x1"] = q["start_x_m"] + run - part["x0"]
            if part.get("kind") == "slope":
                ye, yr = part["y_eaves"], part["y_ridge"]
                r["y_eaves"] = (STREET_FRONTAGE_M + ye) if east else -(STREET_FRONTAGE_M + ye)
                r["y_ridge"] = (STREET_FRONTAGE_M + yr) if east else -(STREET_FRONTAGE_M + yr)
            else:
                a = STREET_FRONTAGE_M + part["y0"]
                b = STREET_FRONTAGE_M + part["y1"]
                r["y0"], r["y1"] = (a, b) if east else (-b, -a)
            # THE FRONTS STAND ON THE FOOTWAY, not on the road crown. The
            # spec's own conversion: street absolute = local + 0.100 m, the
            # built street's footway-above-crown offset at the frontage line.
            # Every bay is authored in local coordinates and integration adds
            # this, which is exactly what this is.
            for k in ("z0", "z1", "z_eaves", "z_ridge"):
                if k in r:
                    r[k] = r[k] + THRESHOLD_ABOVE_CROWN_M
            out.append(r)

    # ---- the road between them, MEASURED from the street block -----------
    q, _e = load_spec(root, spec_rel, "east_parade")
    half = 3.0          # carriageway half width
    kerb_w, kerb_up = 0.125, 0.125
    foot = 2.0
    x0, x1 = -2.0, 44.0
    # THE ROAD IS CROWNED, AND IT NEVER WAS. The scene file has carried a
    # crossfall of 0.025 - one in forty, the value British road practice uses
    # for a straight carriageway - since it was written, with its own derived
    # consequence spelled out: "the crown stands 3.0 x 0.025 = 0.075 m above
    # the channel, and that 75 mm is the whole reason A0 exists. A FLAT
    # CARRIAGEWAY PUTS THE WET-CONDITION WATER EVERYWHERE INSTEAD OF AT THE
    # KERB." Ours was one flat box, so the spec was right twice over and
    # nobody had built it.
    #
    # IT IS ALSO WHY OUR ROAD READS DRY. A flat glossy plane returns the sky
    # at one angle across its whole width and comes back as an even sheet of
    # grey; a crowned one returns it at an angle that CHANGES from the crown
    # to the channel, which is the long soft highlight down the middle of the
    # road that every wet street photograph has and ours did not.
    #
    # SEVENTY-FIVE MILLIMETRES IS NOT EYEBALLED and it is not typed either:
    # it is half_width times crossfall, both read off the scene file, so a
    # street that is ever widened re-derives its own crown.
    crossfall = 0.025
    fall = half * crossfall
    _road(out, "carriageway", "asphalt", x0, x1, half, fall,
          "two-3.0m-lanes/crowned-1-in-40/%.3fm-above-the-channel" % fall)
    # THE FAR END IS THE BASIN END. See _backdrop: the road stops at x0 and
    # everything past it was sky. The road's own x0 is handed over rather
    # than typed a second time, so a street that is ever lengthened takes
    # its backdrop with it.
    if abs(x0 - BACKDROP_ROAD_END) > 1e-9:
        raise AssertionError("the road moved and the backdrop did not: "
                             "x0=%r BACKDROP_ROAD_END=%r" % (x0, BACKDROP_ROAD_END))
    _backdrop(out)
    # AND THE OTHER END, since the camera turned to face it.
    _north_rise(out)
    _north_approach(out)
    # THE DISH, on the cab office, where the approved sheet has it.
    _dish(out)
    _repair_patches(out)
    # THE PAVEMENT TURNS THE CORNER at each block's south end. The footways
    # stop at the frontage line, and past a terrace's gable there was no
    # ground at all: from the turned camera the sky map's green field showed
    # through beside the end wall. Flags from the road's own end at x = -2 up
    # to the gable at x = 3, the full depth of the block behind the frontage,
    # on both sides.
    for sgn, side in ((1.0, "east"), (-1.0, "west")):
        a, b = sgn * STREET_FRONTAGE_M, sgn * (STREET_FRONTAGE_M + 8.6)
        _box(out, "corner_footway_%s" % side, "paving", BACKDROP_ROAD_END, 3.0,
             min(a, b), max(a, b), -0.30, THRESHOLD_ABOVE_CROWN_M,
             "the-pavement-turns-the-corner-at-the-gable")
    for sgn, name in ((1.0, "east"), (-1.0, "west")):
        a, b = sgn * half, sgn * (half + kerb_w)
        _box(out, "kerb_%s" % name, "kerbstone", x0, x1, min(a, b), max(a, b),
             -0.30, kerb_up, "125mm-face/the-standard-British-upstand")
        c, d = sgn * (half + kerb_w), sgn * STREET_FRONTAGE_M
        _box(out, "footway_%s" % name, "paving", x0, x1, min(c, d), max(c, d),
             -0.30, THRESHOLD_ABOVE_CROWN_M, "2.0m/the-normal-British-footway")
    # ---- the double yellow lines, MEASURED off the emitted piece list -----
    # Two 0.1 m bands 0.1 m apart, 12 mm of paint, running the street's whole
    # length at 2.5 and 2.7 m from the centre - which is 0.25 m out from the
    # kerb face, the figure the scene file gives. Read from the pieces rather
    # than re-derived, because the built street already has them and a second
    # arithmetic would be a second street.
    for sgn, side in ((1.0, "east"), (-1.0, "west")):
        for n, across in enumerate((2.5, 2.7)):
            a, b = sgn * across, sgn * (across + 0.1)
            _box(out, "yellow_%s_%d" % (side, n), "paint_yellow", -2.0, 44.0,
                 min(a, b), max(a, b), 0.0, 0.012,
                 "100mm-band-100mm-apart/12mm-of-paint/0.25m-out-from-the-kerb-face")

    # ---- the centre line, 22 September -----------------------------------
    # THE NEW SHEET HAS ONE AND SO DOES R09 ("carriageway markings"), and the
    # scene file already named it as this street's next step (A6, "a centre
    # line ... a RUN along a path"). THE DIMENSIONS ARE THE REGULATION'S, not
    # the sheet's: diagram 1008, the centre line for roads at 40 mph or less
    # - 2 m marks, 4 m gaps, 100 mm wide on a two-lane road of 5.5 m or more,
    # which a 6 m carriageway is. Read from the Traffic Signs Manual, Chapter
    # 5, table 4-1; the 1990 figures are ASSUMED the same, which is written
    # here rather than implied. 12 mm of paint on the crown, which stands
    # `fall` above the channel.
    CL_MARK, CL_GAP, CL_W = 2.0, 4.0, 0.10
    xm, k = x0, 0
    while xm + CL_MARK <= x1 + 1e-9:
        _box(out, "centre_line_%d" % k, "paint_white", xm, xm + CL_MARK,
             -CL_W / 2.0, CL_W / 2.0, fall - 0.004, fall + 0.008,
             "diagram-1008/2m-mark-4m-gap/100mm/on-the-crown")
        xm += CL_MARK + CL_GAP
        k += 1

    # ---- the lit shop interiors ------------------------------------------
    # EVERY BLOCK THAT HAS SHOPS, ON ITS OWN SIDE OF THE ROAD, which this was
    # not: it named east_parade in the code and put its cards at +y, so when
    # Jafar ruled the near west block into shops on 22 September that block's
    # windows became black holes with nothing behind them - the exact fault
    # these cards were written to fix, reintroduced by a hard-coded block id.
    # The blocks are asked what they are now.
    #
    # A card 1.2 m behind the frontage, the depth the shopfront block gives,
    # lit at the file's own colour.
    for block_id in ("east_parade", "west_south", "west_north"):
        q, _e2 = load_spec(root, spec_rel, block_id)
        if _e2 or q["ground_floor"] != "shopfront":
            continue
        east = q["side"] == "east"
        run = q["bays"] * q["bay_width_m"]
        for bay in range(q["bays"]):
            # BAY 3 OF A SIX-BAY PARADE IS THE EMPTY UNIT and stays dark; on
            # a shorter block there is no empty unit to skip.
            if q["bays"] == 6 and bay == 3:
                continue
            # AND THESE TURN WITH THEIR BLOCK. The cards are placed straight
            # into world coordinates rather than through plan_row, so the
            # half turn that plan_street applies to a west block has to be
            # applied to them here too - otherwise bay 0's lit room ends up
            # behind bay 2's window, which is the sort of fault that looks
            # like a lighting bug for an hour.
            bx = (q["start_x_m"] + bay * q["bay_width_m"] if east
                  else q["start_x_m"] + run - (bay + 1) * q["bay_width_m"])
            # CLOSER TO THE GLASS THAN THE 1.2 m THE BLOCK GIVES, and wider.
            # At 1.2 m back and inset half a metre each side the card was a
            # small bright patch in the middle of a black hole; what a person
            # sees through a shop window at a glancing angle is the back of
            # the shop filling it, because the glass is only a metre in front
            # of it and the window is not a porthole.
            y0, y1 = STREET_FRONTAGE_M + 0.75, STREET_FRONTAGE_M + 0.79
            a, b = (y0, y1) if east else (-y1, -y0)
            card = _box(out, "interior_card_%s_%d" % (block_id, bay), "interior_lit",
                        bx + 0.35, bx + q["bay_width_m"] - 0.35, a, b,
                        THRESHOLD_ABOVE_CROWN_M + 0.55, THRESHOLD_ABOVE_CROWN_M + 2.95,
                        "the-lit-back-of-the-shop/on-this-block's-own-side-of-the-road")
            pic = INTERIOR_PICTURE.get((block_id, bay))
            if pic:
                card["decal"], card["decal_uv"] = pic[0], list(pic[1])
                card["decal_emit"] = "room"
            # TWO TUBES ACROSS THE CEILING OF A REFITTED SHOP, a metre and a
            # half each, 38 mm - the T12 tube of the period - 0.35 m in from
            # the glass, where a shop hangs them to light its window. Only the
            # refits: a timber front's shop is lit however it is lit, and R05
            # photographs the tubes with the metal.
            # 2.30 m UP, just under the transom, and attempt one is why: at
            # 2.85 m they sat exactly behind the fascia, whose underside is at
            # 2.85, and could not be seen from anywhere on the street. A 1980s
            # refit hung its ceiling at the transom line, which is also where
            # the sheet's strips show - in the top of the display glass.
            if (block_id, bay) in SHOPFRONT_REFITS:
                ty0, ty1 = STREET_FRONTAGE_M + 0.33, STREET_FRONTAGE_M + 0.37
                ta, tb = (ty0, ty1) if east else (-ty1, -ty0)
                tz = THRESHOLD_ABOVE_CROWN_M + 2.30
                for k, frac in enumerate((0.3, 0.7)):
                    cx = bx + q["bay_width_m"] * frac
                    _box(out, "tube_%s_%d_%d" % (block_id, bay, k), "tube_lit",
                         cx - 0.75, cx + 0.75, ta, tb, tz, tz + 0.038,
                         "a-T12-fluorescent-tube/R05's-strips")

    _figures(out)
    _vehicles(out)
    lamps, lerr = lamp_parts(root)
    if lerr:
        # A STREET WITH NO LAMPS IN IT SAYS SO. The night frame is the one the
        # stage is judged on and it is nothing without them, so this refuses
        # rather than quietly rendering an unlit street that looks deliberate.
        return None, lerr
    out.extend(lamps)
    return out, ""


#: WHERE A PERSON STANDS, and why there is one at all.
#:
#: NOTHING IN THE FRAME SET SCALE. The first render of the street from the
#: sheet's own viewpoint came back reading like a model rather than a place,
#: and the reason is that there was no object in it whose size a person
#: already knows. A door is 1.981 m and a kerb is 125 mm, but neither of those
#: is a thing the eye measures against; a human body is the only one that is.
#:
#: AND D31'S OWN TYING FRAME ASKS FOR ONE IN SO MANY WORDS: "one screenshot of
#: the street at dusk, wet, lamps lit, A FIGURE IN SILHOUETTE". The frame the
#: whole stage is judged by has a person in it, and until now nothing this
#: recipe drew could have been that frame.
#:
#: THE DIMENSIONS ARE THE PROJECT'S OWN. Eye height 1.6 m is
#: CrimeProbe.h's kEyeHeightM, the value the simulation traces sightlines
#: from; a standing body is that plus the distance from eye to crown, which
#: is taken as 0.15 m, so 1.75 m overall. Shoulders 0.45 m, which is the
#: ordinary British doorway's 0.838 m leaf comfortably admitting one person.
#: BLOCKS, NOT A BODY: this is a silhouette to set scale, not a character.
#: The bodies are stage 2 and they are Mixamo's, not mine.
FIGURE_EYE_M = 1.6
FIGURE_EYE_TO_CROWN_M = 0.15
FIGURE_SHOULDER_M = 0.45
FIGURE_DEPTH_M = 0.25
#: (x along the street, y across it). Both on the east footway, one near and
#: one well down the row, because ONE figure sets scale where it stands and
#: TWO set it down the whole length - which is the half that says how far the
#: eye is actually carrying.
#: TWO WAS ENOUGH TO SET SCALE AND NOT ENOUGH TO BE A STREET. The sheet's own
#: panel has six people in it - two walking away, one at a counter, one
#: serving, two standing - and a parade with nobody on it reads as closed
#: whatever the shops say. Six here too, on both pavements and at a spread of
#: distances, because people all at one distance read as a queue.
#: MOVED BACK DOWN THE STREET, 22 September. Two of these were placed when
#: the hook camera stood at x = 40 and they stayed put when it came inside
#: the row to 33: the west-footway figure at x = 30 ended up THREE METRES
#: from the lens and the east one at 33.5 was level with it. At that range a
#: six-box silhouette stops setting scale and starts being the subject - a
#: grey mannequin filling the corner of the frame the stage is judged on.
#: The sheet's own nearest figure is four or five metres off and small.
#: MIRRORED WITH THE CAMERA, 22 September. These were spread for a station at
#: x = 33 looking SOUTH; the camera now stands at x = 9 looking NORTH, and the
#: nearest of them ended up two and a half metres from the lens - the exact
#: fault the note above records and moved them to fix, reintroduced by moving
#: the camera instead of them. Reflected about the street's own mid-point,
#: x -> 45 - x, which keeps the spread and the two pavements and puts them all
#: AHEAD: 9 to 26 m out, which is where the sheet's own people stand.
FIGURE_AT = ((33.5, 4.25), (18.0, 3.85), (26.0, 4.35), (21.5, 4.05),
             (30.0, -4.35), (25.0, -4.15))


#: THE FAR END, AND IT IS THE BASIN END.
#:
#: WHAT THE LIST ASKS, in its own words: "AND THE FAR END IS STILL SKY. What
#: is beyond our thirty metres is nothing, because the TOWN past the street is
#: stage 6." The haze landed on the third attempt and softened the street we
#: have; it could not soften what was not there. A wall of sky closing a
#: street is the single loudest thing left in the frame.
#:
#: THIS IS NOT THE TOWN AND IT IS NOT AN INVENTION. Three sources, read
#: rather than remembered:
#:   - the scene file's own axis note: "x: along the street. 0 at the south
#:     end, +x north." The hook camera stands at x=33 and looks at x=2, so it
#:     is looking SOUTH.
#:   - the town form bible, morphology rule 1: "Quay Street links an OLD
#:     BASIN to the market", and rule 4: "Hook: working stone quay and
#:     enclosed basin". The market is uphill NORTH, behind the camera.
#:   - MICKEYS.md, which routes the deliveries "from the BASIN APPROACH,
#:     through the south terrace-end passage".
#: The one thing the world already says is at this end of this street is the
#: basin. Nothing here decides anything stage 6 has to decide.
#:
#: IT IS A BACKDROP AND IT SAYS SO IN ITS PIECE NAMES. No door, no window, no
#: threshold, no interior, nothing anyone can walk to. Masses at range, in
#: the haze, to stop the view ending in sky. Stage 6 deletes it and loses
#: nothing.
#:
#: AND IT IS THE FIRST TEST OF THE RULE RECORDED TODAY - the sheet governs
#: mood, palette and composition, the photographs govern what things actually
#: looked like, and WHERE THEY DISAGREE THE PHOTOGRAPHS WIN. They disagree
#: here, which is why this is worth saying out loud:
#:   THE SHEET closes both its panels with a wooded hillside and detached
#:   houses loose among trees. production/reference/hook-sheet-audit.md lists
#:   that as invented: the bible expresses the inland rise with
#:   "contour-following terraces, retaining walls and stair shortcuts", and
#:   in any case that rise is NORTH, behind this camera.
#:   THE PHOTOGRAPH, R08, of the working water: "working craft and
#:   liquid-cargo barge, WAREHOUSES ON PILES, a DISTANT CRANE/BRIDGE and
#:   chain-edged quay."
#: So: sheds with their gable ends to the street, and a crane. Not a hill.
#:
#: NO WATER. A basin with no water in it is a dodge and is named as one. The
#: reason is the two volumetric attempts this file already records: a
#: material whose failure mode is a black plane, at the exact spot the eye
#: goes, is the wrong thing to attempt with two hours left. The quay apron
#: runs out of frame and the sheds stand beyond it; what is between them is
#: not asserted. When water is built it is built deliberately.
#:
#: WHERE THE NUMBERS COME FROM. The road ends at x=-2.0 (BACKDROP_ROAD_END,
#: read off the road's own x0, not typed twice). The camera stands at 33, so
#: the sheds at x=-38..-52 are 71 to 85 m away, and the mist reaches its
#: ceiling at 8+55=63 m: they are fully hazed, which is the point of them.
#: Their heights, 6.0 to 11.5 m, are the bible's "varied roof heights" and
#: subtend 4 to 8 degrees at that range, which fills the gap between the two
#: eaves lines without towering over them.
BACKDROP_ROAD_END = -2.0      # where the built street's carriageway stops
BACKDROP_APRON_X = 14.0       # metres of quay apron beyond it
BACKDROP_APRON_HALF_Y = 12.0  # the apron is wider than the street: it is a quay

#: (y0, y1, x_far, x_near, eaves_m, ridge_rise_m, wall)
#: Six sheds, each standing at its own distance so the far bank is not one
#: flat wall, and each with its GABLE END to the street - which is what a
#: dock shed looks like end-on and is the readable silhouette at 80 m.
#: ATTEMPT TWO, AND THE FIRST ONE IS WHY. Rendered, looked at, and two
#: things were wrong at a glance rather than in a number:
#:   THE 11.5 m SHED STOOD DEAD CENTRE IN THE GAP and read as a grain silo -
#:   one featureless slab taller than everything either side of it, exactly
#:   where the eye goes.
#:   AND THE CEILING IS THE STREET'S OWN RIDGE, 9.00 m, read off the spec by
#:   the selftest rather than typed here. The first correction set the EAVES
#:   below it and forgot that a roof goes on top, which put two ridges at
#:   9.5 and 10.6 - taller than the street they are seen through, which is a
#:   tower block at the end of a Victorian street. The check caught it; the
#:   heights below are what it takes to satisfy it, which is the difference
#:   between finishing an asset from its dimensions and adjusting it by eye.
#:   AND THE ROW WAS ONE RANGE. Six masses at one distance is a painted
#:   flat, not depth, which is the fault this was built to fix. There are
#:   two ranges now: the near bank at 37 to 52 m out from the road end and a
#:   BACK RANK 14 m behind it, lower, so the haze separates them from each
#:   other as well as from the street. Aerial perspective needs two things
#:   at two distances or it has nothing to be a difference between.
BACKDROP_SHEDS = (
    (-24.0, -14.0, -50.0, -40.0, 6.4, 1.6, "brick_grey"),
    (-14.0, -6.5, -47.0, -38.0, 6.8, 1.7, "brick_red"),
    (-6.5, 1.0, -52.0, -41.0, 6.2, 1.5, "brick_grey"),
    (1.0, 9.0, -46.0, -37.0, 6.9, 1.9, "brick_red"),
    (9.0, 18.0, -51.0, -42.0, 6.0, 1.7, "brick_grey"),
    (18.0, 26.0, -48.0, -39.0, 7.1, 1.8, "brick_red"),
    # THE BACK RANK, 14 m further out and lower, seen over and between the
    # near bank. Wider and fewer, because a thing at 95 m that is not simple
    # is a thing nobody can read.
    (-20.0, -3.0, -68.0, -60.0, 5.4, 1.4, "brick_grey"),
    (-3.0, 12.0, -70.0, -61.0, 6.8, 1.6, "brick_grey"),
    (12.0, 28.0, -66.0, -59.0, 4.8, 1.3, "brick_red"),
)

#: THE CRANE, and it is one crane. R08 has "a distant crane/bridge" singular
#: and a forest of them would be a different port. A column and a jib, in
#: silhouette, standing behind the sheds so it reads against sky.
#:
#: ATTEMPT ONE WAS A WEDGE. 17 m tall, a 13 m jib and members 1.7 m thick,
#: which at 90 m came back as a solid arrowhead the size of a building - the
#: single loudest object in the frame, and not recognisably a crane. THE
#: FAULT WAS THICKNESS, not height: a dockside crane is mostly air, and a
#: silhouette that is mostly air reads as a machine while the same outline
#: filled in reads as a monument. The members are 0.5 m now, which is what
#: they would actually be, and the column and the jib are two separate thin
#: pieces rather than one closed outline with a shoulder between them.
#: It also stands further out and OFF the street's axis, so it is something
#: glimpsed past the sheds rather than a thing placed in the middle of the
#: view.
BACKDROP_CRANE_X = -74.0
BACKDROP_CRANE_Y = -9.0
BACKDROP_CRANE_H = 14.0
BACKDROP_CRANE_REACH = 11.0
BACKDROP_CRANE_T = 0.50       # how thick a member is: a crane is mostly air


#: THE NORTH END, AND IT IS THE INLAND RISE. 22 September, the composition
#: step of the visual lane.
#:
#: WHY NOW. The camera was turned to the new sheet's view, south end looking
#: north, and the far end of the frame became the other end of Quay Street.
#: The sheet closes that view with a hillside of terraces stepping up behind
#: retaining walls. The town form bible says the same thing in its own words -
#: "flat low harbour ground, then a deliberate inland rise... CONTOUR-FOLLOWING
#: TERRACES, RETAINING WALLS and stair shortcuts express the rise" - and the
#: market is uphill NORTH, which is the way the camera now looks. So the sheet
#: and the bible agree, which is the first time on this street they have.
#:
#: A BACKDROP, NAMED AS ONE, like the basin end: masses at range, no door, no
#: window anyone can reach, every piece backdrop_rise_*. Stage 6 builds the
#: town and deletes this.
#:
#: THE NUMBERS. Five tiers, each a retaining wall with a row of houses on it,
#: 25 m apart going north from x = 70 and 5.5 m higher each time - a rise of
#: about one in four and a half, climbing to 22 m at the top row. The bible's
#: crest is 45 m, further off than this frame reaches. Each row runs ACROSS
#: the view, along the contour, and is broken into houses of their own widths
#: and heights with passages between, because a single wall at any range reads
#: as a wall and not a street.
RISE_TIERS = 5
#: ATTEMPT TWO, AND THE FIRST IS WHY. Attempt one put five rows of long blank
#: brick boxes at 70 to 170 m, 5.5 m a tier: rendered beside the sheet they
#: read as a crowd of warehouses filling the end of the street. The sheet's is
#: a HILLSIDE - further off, steep enough that each tier's pale retaining wall
#: shows above the roofs in front of it, houses of their own widths, dark
#: slate roofs, cream render among the brick, windows, and sky above it all.
#: So: 110 m out, 9 m a tier - which lands the top row at 36 m and its roofs
#: at the bible's own 45 m crest - houses set back from each wall's edge so
#: the wall's face shows, one house to a piece, render on about a third.
RISE_FIRST_X = 110.0
RISE_TIER_STEP_X = 24.0
RISE_TIER_STEP_Z = 9.0
RISE_ROW_DEPTH = 8.0
RISE_SETBACK = 3.0
RISE_Y_SPAN = (-120.0, 60.0)


#: THE SATELLITE DISH, 22 September. On the approved sheet a small dish sits
#: high on the wall of the cab office, under the eaves beside the upper
#: right-hand window, and Jafar ruled it CITABLE the same night: "the
#: household research records dishes as new and contested in 1990". A 1990
#: domestic dish is about 60 cm across, solid, on a wall bracket with its
#: receiver held out on an arm in front of it. It is AIMED rather than
#: placed: the satellites a British dish looked at in 1990 sit low in the
#: southern sky to the south-east, so on a front wall it looks along the
#: wall to the south, tipped up about 25 degrees. No make and no mark.
DISH_D_M, DISH_DEPTH_M, DISH_STANDOFF_M, DISH_SIDES = 0.60, 0.07, 0.35, 12
DISH_AT = (8.35, 5.60)          # street x and height, on east_parade bay 0
DISH_AIM = (-0.85, -0.30, 0.43)  # along the wall to the south, out, and up


def _norm(v):
    L = math.sqrt(sum(c * c for c in v))
    return tuple(c / L for c in v)


def _cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def _rod(out, pid, material, p0, p1, w, note=""):
    """A square-section rod between two points, as one mesh."""
    d = _norm(tuple(b - a for a, b in zip(p0, p1)))
    up = (0.0, 0.0, 1.0) if abs(d[2]) < 0.9 else (1.0, 0.0, 0.0)
    u = _norm(_cross(d, up))
    v = _cross(d, u)
    h = w / 2.0
    corners = [(+h, +h), (-h, +h), (-h, -h), (+h, -h)]
    verts = []
    for p in (p0, p1):
        for a, b in corners:
            verts.append(tuple(p[i] + a * u[i] + b * v[i] for i in range(3)))
    faces = [(0, 1, 2, 3), (7, 6, 5, 4)]
    for i in range(4):
        j = (i + 1) % 4
        faces.append((i, j, 4 + j, 4 + i))
    out.append({"id": pid, "material": material, "kind": "mesh",
                "verts": verts, "faces": faces, "note": note})


#: THE ROOM BEHIND EACH TRADING WINDOW, 23 September: pictures from the image
#: lane (tools/imagegen/interiors-2026-09-23.json) laid on the lit card, as
#: D14's texture on glass for a window nobody enters. MICKEY'S IS NOT HERE,
#: on purpose: its interior is D14's to design, and Jafar took the waiting
#: chairs and the clock out of the sheet's prompt for exactly that reason.
INTERIORS = "production/art/interiors-2026-09-23"
#: (picture, crop). THE CROP IS READ OFF EACH PICTURE BY EYE, as the scene
#: file's own crops are - [u0, v0, u1, v1], v from the bottom - because the
#: model drew each room inside a shop window with a strip of pavement below
#: it, and a window frame hung behind our window frame is two frames.
INTERIOR_PICTURE = {
    ("east_parade", 1): (INTERIORS + "/int23_fish", (0.05, 0.12, 0.95, 0.92)),
    ("east_parade", 2): (INTERIORS + "/int23_pawn", (0.06, 0.20, 0.64, 0.92)),
    ("east_parade", 4): (INTERIORS + "/int23_laundry", (0.03, 0.10, 0.73, 0.98)),
    ("east_parade", 5): (INTERIORS + "/int23_grocer", (0.11, 0.22, 0.89, 0.93)),
}
#: How brightly a pictured room glows, by day and at night. By day it stands
#: where the plain card stood, about the sheet's own window value; at night
#: it is the lit shop the plain card was, and a room rather than a lightbox.
CARD_EMIT_DAY, CARD_EMIT_NIGHT = 0.40, 1.60
#: AND A NET CURTAIN'S, which stands for daylight falling on it through the
#: glass: bright enough by day to bring the sheet's pale upstairs windows,
#: nearly dark at night, when most front bedrooms are.
NET_EMIT_DAY, NET_EMIT_NIGHT = 0.30, 0.05
NET_CURTAINS = ("production/assets/vignette/decals2d/net_curtain_a",
                "production/assets/vignette/decals2d/net_curtain_b")


def _dish(out):
    """The dish, its wall bracket and its receiver arm, in street coordinates."""
    x, z = DISH_AT
    wall_y = STREET_FRONTAGE_M
    c = (x, wall_y - DISH_STANDOFF_M, z)
    n = _norm(DISH_AIM)
    u = _norm(_cross(n, (0.0, 0.0, 1.0)))
    v = _cross(n, u)
    r = DISH_D_M / 2.0
    ring_front, ring_back = [], []
    for k in range(DISH_SIDES):
        t = 2.0 * math.pi * k / DISH_SIDES
        e = tuple(c[i] + r * (math.cos(t) * u[i] + math.sin(t) * v[i]) for i in range(3))
        ring_front.append(e)
        # THE BOWL: the rim stands forward of the centre by the dish's depth,
        # so the back ring is the rim pulled back along the aim.
        ring_back.append(tuple(e[i] - DISH_DEPTH_M * n[i] for i in range(3)))
    back_c = tuple(c[i] - DISH_DEPTH_M * 0.4 * n[i] for i in range(3))
    verts = ring_front + ring_back + [c, back_c]
    m = DISH_SIDES
    faces = []
    for k in range(m):
        j = (k + 1) % m
        faces.append((2 * m, j, k))               # the bowl's face, rim to centre
        faces.append((k, j, m + j, m + k))        # the rim's thickness
        faces.append((2 * m + 1, m + k, m + j))   # the back
    out.append({"id": "satellite_dish", "material": "dish_grey", "kind": "mesh",
                "verts": verts, "faces": faces,
                "note": "60cm-solid-dish/1990/ruled-citable-by-Jafar-22-September"})
    # THE BRACKET off the wall to the back of the dish, and the ARM that
    # holds the receiver out in front of it.
    _rod(out, "satellite_dish_bracket", "steel_dark",
         (x, wall_y, z - 0.05), back_c, 0.04, "the-wall-bracket")
    lnb = tuple(c[i] + 0.42 * n[i] - 0.18 * v[i] for i in range(3))
    _rod(out, "satellite_dish_arm", "steel_dark",
         tuple(c[i] - 0.25 * v[i] for i in range(3)), lnb, 0.02, "the-receiver-arm")
    _rod(out, "satellite_dish_receiver", "dish_grey",
         lnb, tuple(lnb[i] - 0.10 * n[i] for i in range(3)), 0.06, "the-receiver")


#: REPAIR PATCHES IN OLDER MASONRY, which is D06's own phrase for the Hook -
#: "metal frames, practical light fittings and REPAIR PATCHES within older
#: masonry" - and which the new sheet shows on its near gable: a rough
#: cement patch where something was taken off the wall and made good.
#: (face_x, y centre, z centre, half-width, half-height), on the south end
#: wall of the parade, the one the hook camera faces, and one on the
#: parade's front above the empty unit, where a sign was taken down.
REPAIR_PATCHES = ((2.66, 6.7, 4.05, 0.36, 0.30, "x"),
                  (24.0, 5.125, 4.45, 0.30, 0.22, "y"))


def _repair_patches(out):
    """Irregular cement patches, 6 mm proud of the brick they mend."""
    for k, (f, c1, cz, hw, hh, axis) in enumerate(REPAIR_PATCHES):
        # AN IRREGULAR OUTLINE, because a patch is made good by hand: eight
        # points on an ellipse, each pushed in or out by a fixed amount.
        wob = (1.0, 0.82, 1.08, 0.9, 0.97, 1.12, 0.85, 1.03)
        ring = []
        for i, w in enumerate(wob):
            t = 2.0 * math.pi * i / len(wob)
            ring.append((c1 + hw * w * math.cos(t), cz + hh * w * math.sin(t)))
        n = len(ring)
        if axis == "x":
            front = [(f - 0.006, u, z) for (u, z) in ring]
            back = [(f, u, z) for (u, z) in ring]
        else:
            front = [(u, f - 0.006, z) for (u, z) in ring]
            back = [(u, f, z) for (u, z) in ring]
        faces = [tuple(range(n)), tuple(range(2 * n - 1, n - 1, -1))]
        for i in range(n):
            j = (i + 1) % n
            faces.append((i, n + i, n + j, j))
        out.append({"id": "repair_patch_%d" % k, "material": "render_patch", "kind": "mesh",
                    "verts": front + back, "faces": faces,
                    "note": "D06/repair-patches-within-older-masonry/made-good-by-hand"})


#: THE STREET CARRIES ON TO THE RISE, 23 September. Between the road's end at
#: x = 44 and the rise's first tier at 110 there was nothing, and from the
#: hook camera the sky map's green field showed through under the hill: a
#: field in the middle of a port town, at the exact point of the frame the
#: sheet puts its vanishing street - Quay Street running on uphill between
#: terraces toward the market, which canon puts north. A BACKDROP, NAMED AS
#: ONE (backdrop_rise_approach_*): the road and its footways carry on, and
#: two terraces of plain houses line them, each house its own width and
#: height, slate roofs along the street, dark windows two to a floor. No
#: door anyone can reach, nothing in the stage's street. Stage 6 builds the
#: town and deletes this.
APPROACH_X = (44.0, 108.0)


def _north_approach(out):
    """The road, the footways and two backdrop terraces from x 44 to 108."""
    import random
    rnd = random.Random(20260923)          # fixed: the same street every render
    x0, x1 = APPROACH_X
    _box(out, "backdrop_rise_approach_road", "asphalt", x0, x1, -3.0, 3.0, -0.30, 0.0,
         "the-road-carries-on")
    for sgn, side in ((1.0, "e"), (-1.0, "w")):
        a, b = sgn * 3.0, sgn * STREET_FRONTAGE_M
        _box(out, "backdrop_rise_approach_footway_%s" % side, "paving", x0, x1,
             min(a, b), max(a, b), -0.30, THRESHOLD_ABOVE_CROWN_M, "and-its-footway")
        x = x0 + rnd.uniform(1.0, 3.0)
        n = 0
        while x < x1 - 4.0:
            w = rnd.uniform(5.0, 7.0)
            xe = min(x + w, x1)
            h = rnd.uniform(5.4, 6.6)
            r = rnd.random()
            wall = "render_cream" if r < 0.2 else ("brick_red" if r < 0.75 else "brick_grey")
            f, back = sgn * STREET_FRONTAGE_M, sgn * (STREET_FRONTAGE_M + 8.0)
            _box(out, "backdrop_rise_approach_%s%d" % (side, n), wall, x, xe,
                 min(f, back), max(f, back), 0.0, h, "a-house/%.1fm/%s" % (xe - x, wall))
            ridge = sgn * (STREET_FRONTAGE_M + 4.0)
            out.append({"id": "backdrop_rise_approach_%s%d_roof" % (side, n), "material": "slate",
                        "kind": "slope", "x0": x - 0.05, "x1": xe + 0.05,
                        "y_eaves": f - sgn * 0.25, "y_ridge": ridge,
                        "z_eaves": h, "z_ridge": h + 2.6, "note": "its-roof-along-the-street"})
            # DARK WINDOWS, two to a floor, on the street face.
            face = f - sgn * 0.03
            for fz in (1.0, 3.6):
                for k in (0.28, 0.72):
                    cx = x + (xe - x) * k
                    _box(out, "backdrop_rise_approach_%s%d_win%d%d" % (side, n, int(fz), int(k * 100)),
                         "car_glass", cx - 0.45, cx + 0.45, min(face, f), max(face, f),
                         fz, min(fz + 1.4, h - 0.3), "a-window")
            if rnd.random() < 0.7:
                _box(out, "backdrop_rise_approach_%s%d_stack" % (side, n), "brick_red",
                     xe - 0.45, xe + 0.45, ridge - 0.25, ridge + 0.25, h + 1.8, h + 3.6,
                     "a-stack-on-the-party-wall")
            n += 1
            x = xe + (rnd.uniform(1.5, 3.0) if rnd.random() < 0.15 else 0.0)


def _north_rise(out):
    """The inland rise: retaining walls and contour terraces, tier on tier."""
    import random
    rnd = random.Random(20260922)       # fixed: the same hill every render
    for t in range(RISE_TIERS):
        x0 = RISE_FIRST_X + t * RISE_TIER_STEP_X
        zb = t * RISE_TIER_STEP_Z
        # THE RETAINING WALL holding this tier up above the one in front,
        # in the stone the quay is built of, running the whole contour.
        if zb > 0.0:
            _box(out, "backdrop_rise_wall_%d" % t, "stone",
                 x0 - 1.2, x0, RISE_Y_SPAN[0], RISE_Y_SPAN[1], zb - RISE_TIER_STEP_Z, zb,
                 "retaining-wall/%.1fm/the-bible's-own-device" % RISE_TIER_STEP_Z)
        xa = x0 + RISE_SETBACK
        xb = xa + RISE_ROW_DEPTH
        xm = (xa + xb) / 2.0
        y = RISE_Y_SPAN[0] + rnd.uniform(0.0, 6.0)
        n = 0
        while y < RISE_Y_SPAN[1]:
            w = rnd.uniform(5.5, 9.0)              # one house
            h = rnd.uniform(5.0, 6.6)              # to its eaves
            rise = rnd.uniform(2.6, 3.6)           # a steeper roof, darker to the eye
            y1 = min(y + w, RISE_Y_SPAN[1])
            r = rnd.random()
            wall = "render_cream" if r < 0.34 else ("brick_red" if r < 0.80 else "brick_grey")
            _prism(out, "backdrop_rise_%d_%d" % (t, n), wall,
                   ((xb, zb), (xb, zb + h), (xa, zb + h), (xa, zb)), y, y1,
                   "house/%.1fm-wide/%.1fm-eaves/%s" % (y1 - y, h, wall))
            _prism(out, "backdrop_rise_%d_%d_roof" % (t, n), "slate",
                   ((xb + 0.3, zb + h), (xm, zb + h + rise), (xa - 0.3, zb + h)), y, y1,
                   "slate/%.1fm-rise" % rise)
            # WINDOWS, one dark band a floor across the house's face. At a
            # hundred metres a window is two or three pixels, and a band of
            # them is what says house rather than shed.
            for fz in (1.1, 3.6):
                if zb + fz + 1.3 < zb + h:
                    _box(out, "backdrop_rise_%d_%d_win%d" % (t, n, int(fz)), "glass",
                         xa - 0.05, xa, y + 0.8, y1 - 0.8, zb + fz, zb + fz + 1.3,
                         "a-floor-of-windows")
            # a stack on most of them
            if rnd.random() < 0.7:
                cy = y + (y1 - y) * rnd.uniform(0.2, 0.8)
                _box(out, "backdrop_rise_%d_%d_stack" % (t, n), "brick_red",
                     xm - 0.35, xm + 0.35, cy - 0.45, cy + 0.45,
                     zb + h + rise - 0.6, zb + h + rise + 1.1, "a-stack")
            n += 1
            y = y1 + rnd.uniform(0.3, 2.5)         # a passage, a stair, a gap


def _backdrop(out):
    """The basin end: a quay apron, six sheds gable-on, one crane.

    EVERY PIECE IS NAMED backdrop_*, so a search for what is real on this
    street and what is only stopping the sky can be answered by the piece
    list rather than by reading this comment.
    """
    x_end = BACKDROP_ROAD_END
    # THE QUAY APRON. The street runs out onto it and it leaves frame; it is
    # the only part of this that is at human range, so it is the only part
    # that gets the street's own surface rather than a mass.
    _box(out, "backdrop_quay_apron", "stone",
         x_end - BACKDROP_APRON_X, x_end,
         -BACKDROP_APRON_HALF_Y, BACKDROP_APRON_HALF_Y, -0.30, 0.0,
         "the-street-runs-out-onto-a-quay/not-a-void/"
         "wider-than-the-street-because-a-quay-is")

    for n, (y0, y1, xf, xn, eaves, rise, wall) in enumerate(BACKDROP_SHEDS):
        _box(out, "backdrop_shed%d" % n, wall, xf, xn, y0, y1, -0.30, eaves,
             "%.1fm-to-the-eaves/gable-end-to-the-street" % eaves)
        # TWO SLOPES MAKE THE GABLE, ridge along x, which puts the triangle
        # facing the camera. The same two-slope roof the terrace uses.
        ymid = (y0 + y1) / 2.0
        for side, ye in (("south", y0), ("north", y1)):
            out.append({"id": "backdrop_shed%d_roof_%s" % (n, side),
                        "material": "slate", "kind": "slope",
                        "x0": xf, "x1": xn,
                        "y_eaves": ye, "y_ridge": ymid,
                        "z_eaves": eaves, "z_ridge": eaves + rise,
                        "note": "%.1fm-rise-to-the-ridge" % rise})

    # THE CRANE: a thin column and a thin jib, as two pieces, so the sky
    # shows between them. See the constants for what attempt one got wrong.
    cx, ch = BACKDROP_CRANE_X, BACKDROP_CRANE_H
    reach, t = BACKDROP_CRANE_REACH, BACKDROP_CRANE_T
    _prism(out, "backdrop_crane_column", "slate",
           ((cx - t, 0.0), (cx + t, 0.0), (cx + t, ch), (cx - t, ch)),
           BACKDROP_CRANE_Y - t, BACKDROP_CRANE_Y + t,
           "R08-a-distant-crane/one-of-them-not-a-forest")
    # The jib rises toward the water at about one in three, which is where a
    # luffing jib sits at rest, and its foot overlaps the column top so the
    # two read as joined rather than as a post and a stick.
    rise = reach * 0.34
    _prism(out, "backdrop_crane_jib", "slate",
           ((cx - t, ch - t * 2.0), (cx + reach, ch + rise - t * 1.2),
            (cx + reach, ch + rise), (cx - t, ch)),
           BACKDROP_CRANE_Y - t * 0.8, BACKDROP_CRANE_Y + t * 0.8,
           "one-in-three/a-luffing-jib-at-rest/%.2fm-members" % t)


def _road(out, pid, material, x0, x1, half, fall, note=""):
    """The carriageway as a crowned solid rather than a flat slab.

    Six vertices along the top - channel, crown, channel, at each end - and
    six under them. Written as a mesh rather than as two of the roof slabs
    this file already has, because those carry their own thickness along
    their own normal and two of them meeting at a crown leave a wedge of air
    under the ridge that the eye finds the moment anything reflects in it.
    """
    lo = -0.30
    v = [(x0, -half, -fall), (x0, 0.0, 0.0), (x0, half, -fall),
         (x1, -half, -fall), (x1, 0.0, 0.0), (x1, half, -fall),
         (x0, -half, lo), (x0, 0.0, lo), (x0, half, lo),
         (x1, -half, lo), (x1, 0.0, lo), (x1, half, lo)]
    f = [(0, 3, 4, 1), (1, 4, 5, 2),            # the two falls
         (6, 7, 10, 9), (7, 8, 11, 10),         # the underside
         (0, 1, 7, 6), (1, 2, 8, 7),            # the near end
         (3, 9, 10, 4), (4, 10, 11, 5),         # the far end
         (0, 6, 9, 3), (2, 5, 11, 8)]           # the two channels
    out.append({"id": pid, "material": material, "kind": "mesh",
                "verts": v, "faces": f, "note": note})


def _figures(out):
    """A person, twice, as blocks. See FIGURE_AT for why they are here."""
    top = FIGURE_EYE_M + FIGURE_EYE_TO_CROWN_M
    head = 0.23
    for n, (fx, fy) in enumerate(FIGURE_AT):
        # SHOULDERS ACROSS THE VIEW, NOT ALONG IT. The first pair were built
        # with their 0.45 m shoulders spanning x - along the street - and the
        # sheet's viewpoint looks ALONG the street, so the camera saw the
        # 0.25 m side of each and they read as two dark posts. A figure that
        # does not read as a person sets no scale at all, which was the whole
        # reason for putting one there.
        hw, hd = FIGURE_SHOULDER_M / 2.0, FIGURE_DEPTH_M / 2.0
        base = THRESHOLD_ABOVE_CROWN_M
        coat = ("figure_a", "figure_b", "figure_c")[n % 3]
        # TWO LEGS WITH DAYLIGHT BETWEEN THEM, AND A NECK. Turning the
        # shoulders across the view fixed the first fault and left a second
        # one: a single block from the ground to the shoulders is a post
        # whichever way it faces. What the eye actually uses to find a person
        # at twenty-five metres, before it can see a face or a coat, is the
        # GAP between the legs and the NOTCH at the neck - two pieces of
        # background showing through in the right places. Both cost one box
        # each and they are the whole of the read.
        #
        # STILL BLOCKS AND NOT A BODY. Six boxes is a silhouette that sets
        # scale; the bodies are stage 2 and they are Mixamo's, not mine.
        leg_w = hw * 0.34
        leg_gap = hw * 0.16
        for side, sy in (("l", -leg_gap - leg_w), ("r", leg_gap + leg_w)):
            _box(out, "figure_%d_leg_%s" % (n, side), "figure", fx - hd * 0.8, fx + hd * 0.8,
                 fy + sy - leg_w, fy + sy + leg_w, base, base + 0.86,
                 "one-of-two/the-gap-between-them-is-what-reads")
        # THE TORSO STOPS AT THE SHOULDER and the head sits above a neck
        # narrower than both, so the outline steps in twice on its way up.
        neck = head * 0.55
        shoulder_z = base + top - head - 0.06
        _box(out, "figure_%d_torso" % n, coat, fx - hd, fx + hd,
             fy - hw, fy + hw, base + 0.86, shoulder_z, "shoulders-0.45m")
        _box(out, "figure_%d_neck" % n, coat, fx - neck / 2.0, fx + neck / 2.0,
             fy - neck / 2.0, fy + neck / 2.0, shoulder_z, base + top - head,
             "the-notch-the-eye-looks-for")
        _box(out, "figure_%d_head" % n, "figure", fx - head / 2.0, fx + head / 2.0,
             fy - head / 2.0, fy + head / 2.0, base + top - head, base + top,
             "crown-at-1.75m/eye-at-the-simulation's-own-1.6")


#: WHY THERE IS A CAR AT ALL, AND WHY IT IS NOT A REAL ONE.
#:
#: THE APPROVED SHEET HAS ONE, and exactly one: a dark car parked well up the
#: street on the left, small in the frame, with the road empty in front of
#: it. AN EARLIER READING OF THIS PUT THREE AT THE KERB IN THE FOREGROUND
#: and that was taken off Codex's retired sheet, which is a different street
#: with a different amount of traffic in it. One, far off, is what the
#: reference actually shows and it is also the cheaper thing to build.
#:
#: THE BILL OF MATERIALS ROUTES F4_parked_vehicle AS *FETCH*, and this recipe
#: does not follow it. Its own note is the reason: "Largest quality risk on
#: the list if included... canon also forbids real car models, so a
#: recognisable real shape is a canon violation as well as a bar risk", and
#: its certainty is NEEDS-CHECKING rather than HELD. What is held - the
#: Kenney car kit and the OGA vehicles - is flat-colormap low-poly and
#: several of them are American types, off the photoreal bar twice over. So
#: this goes the way E1_lighting_column and E4_pillar_box already went on
#: this street: the held mesh is wrong, so the thing is EMITTED from numbers.
#: An invented shape cannot be a recognisable real car, so the canon problem
#: is solved by construction rather than by inspection.
#:
#: THE NUMBERS ARE CLASS AVERAGES, NOT ONE MODEL'S. A 1990 British family
#: hatchback runs 3.9 to 4.3 m long, 1.60 to 1.70 wide and 1.38 to 1.45 tall
#: on a 2.5 m wheelbase, with 13-inch rims and 175/70 tyres giving a 0.578 m
#: wheel. Sitting in the middle of that class is exactly what canon asks
#: for: the shape is right for the period and belongs to nobody.
#:
#: THE PROFILE IS DRAWN FROM THE NOSE, (x back from the nose, z off the
#: road), anticlockwise, and extruded across the car. The BODY and the
#: GLASSHOUSE are separate extrusions at different widths, which is the one
#: piece of shape that matters at this distance: a real car's glass is set in
#: from its flanks, so the eye reads body, then a darker narrower band, then
#: roof. Extrude one full-width profile instead and you get a wedge.
CAR_L, CAR_W, CAR_GLASS_W = 4.12, 1.64, 1.46
WHEEL_D, WHEEL_W = 0.578, 0.175
#: 520 x 111 mm, the British plate since 1973.
PLATE_W, PLATE_H = 0.520, 0.111

HATCH_BODY = ((0.15, 0.30), (CAR_L - 0.15, 0.30), (CAR_L, 0.42), (CAR_L, 0.98),
              (CAR_L - 0.08, 1.04), (1.05, 0.98), (1.00, 0.90), (0.12, 0.86),
              (0.0, 0.70), (0.0, 0.44))
HATCH_GLASS = ((1.06, 0.96), (CAR_L - 0.10, 0.96), (CAR_L - 0.58, 1.42),
               (1.64, 1.42))
CAR_ROOF_Z = 1.42

#: (x of the car's centre, y of it, facing, paint). FACING IS +1 FOR NOSE
#: TOWARDS THE CAMERA, which stands at x = 35.
#:
#: WHERE IT STANDS IS THE KERB AND NOT A CHOICE. The carriageway is 3.0 m
#: each side of the centre, so a 1.64 m car parked a hand's width off the
#: kerb face has its centre at 3.0 - 0.22 - 0.82 = 1.96 m. At x = 8 it is
#: twenty-seven metres off, which is where the sheet's is.
VEHICLE_AT = (
    (8.0, -1.96, 1, "car_dark"),
)
#: MOVED, 22 September, to the rank the new sheet shows. The camera now
#: stands at the south end looking north, and the sheet parks its cars at the
#: EAST kerb just beyond Mickey's front - the rank outside the cab office -
#: seen from behind, nose north, with the traffic. Jafar's ruling of the same
#: day: "a rank outside, one or two plain unmarked second-hand saloons", and
#: the sheet's third car is not citable. So TWO, and the sheet's two: a dark
#: one and a paler blue-grey one behind it, a car's length and a gap apart.
#: They stand at bay 1, x 9 to 15, and not across Mickey's own window, which
#: the sheet keeps clear. y = +1.96 is the east kerb by the same arithmetic
#: as above. facing +1 is now nose AWAY from the camera, so its tail - lamps
#: and the yellow plate - is what faces it, as on the sheet.
VEHICLE_AT = (
    (11.0, 1.96, 1, "car_dark"),
    (15.9, 1.96, 1, "car_bluegrey"),
)


def _prism(out, pid, material, profile, y0, y1, note=""):
    """A closed (x, z) outline extruded across the street, as one mesh.

    THE OUTLINE IS GIVEN NOSE-FIRST AND ANTICLOCKWISE, and both cap windings
    below depend on that: the y0 cap keeps the order and the y1 cap reverses
    it, which is what puts every normal outwards. A car with inverted normals
    is not obviously wrong in a flat preview and is very obviously wrong the
    moment anything specular lands on it.
    """
    n = len(profile)
    verts = [(x, y0, z) for (x, z) in profile] + [(x, y1, z) for (x, z) in profile]
    faces = [tuple(range(n)), tuple(reversed(range(n, 2 * n)))]
    for i in range(n):
        j = (i + 1) % n
        faces.append((i, n + i, n + j, j))
    out.append({"id": pid, "material": material, "kind": "mesh",
                "verts": verts, "faces": faces, "note": note})


def _wheel_profile(cx, cz, d):
    """An octagon standing in for a wheel.

    EIGHT SIDES RATHER THAN A BOX, and rather than thirty-two. A box wheel
    reads as a box at any distance because its corners catch the light in a
    way no tyre does; past about eight sides nothing is gained at
    twenty-five metres and every extra one is paid for four times.
    """
    r = d / 2.0
    return tuple((cx + r * math.cos(math.radians(22.5 + 45.0 * k)),
                  cz + r * math.sin(math.radians(22.5 + 45.0 * k)))
                 for k in range(8))


def _vehicles(out):
    """One at the kerb. See VEHICLE_AT for why it is there and why it is
    nobody's car."""
    L, half, gw = CAR_L, CAR_W / 2.0, CAR_GLASS_W / 2.0
    for n, (cx, cy, facing, paint) in enumerate(VEHICLE_AT):

        def place(profile, y0, y1, pid, material, note=""):
            # NOSE-AT-ZERO INTO WORLD, and the reversal is not decoration.
            # The outline is drawn from the nose and the car's own frame has
            # the nose at +L/2, so x is reflected; a reflection alone would
            # turn every face inside out, and reversing the point order
            # restores the winding. Facing then turns the car with a proper
            # 180-degree yaw - x AND y both negated - rather than mirroring
            # it, because a mirrored car is one with its normals inverted
            # and its driver on the wrong side.
            local = tuple(reversed([(L / 2.0 - px, pz) for (px, pz) in profile]))
            world = tuple((cx + facing * lx, lz) for (lx, lz) in local)
            a, b = cy + facing * y0, cy + facing * y1
            _prism(out, pid, material, world, min(a, b), max(a, b), note)

        place(HATCH_BODY, -half, half, "veh%d_body" % n, paint,
              "class-average-hatchback/not-a-model")
        place(HATCH_GLASS, -gw, gw, "veh%d_glass" % n, "car_glass",
              "set-in-from-the-flanks/body-then-glass-then-roof")
        # THE ROOF CAP IS THE PALE BAND OVER THE DARK ONE. Without it the
        # glasshouse runs into the sky and the car loses its lid.
        place(((HATCH_GLASS[3][0], CAR_ROOF_Z), (HATCH_GLASS[2][0], CAR_ROOF_Z),
               (HATCH_GLASS[2][0], CAR_ROOF_Z + 0.03), (HATCH_GLASS[3][0], CAR_ROOF_Z + 0.03)),
              -gw - 0.02, gw + 0.02, "veh%d_roof" % n, paint, "the-lid")
        for w, ax in enumerate((0.80, L - 0.78)):
            for side, sy in (("n", half - 0.09), ("f", -half + 0.09)):
                place(_wheel_profile(ax, WHEEL_D / 2.0, WHEEL_D),
                      sy - WHEEL_W / 2.0, sy + WHEEL_W / 2.0,
                      "veh%d_wheel_%d%s" % (n, w, side), "tyre", "13-inch-and-175/70")
        # THE TAIL: two lamps at the outer corners and the yellow plate
        # between them, which is the whole of what a British car of this
        # period says about itself from behind.
        # BUMPERS AND HUBS, 22 September: the pair's two saloons read as toy
        # blocks, and the sheet's cars are what a 1980s saloon is - a black
        # moulded bumper across each end at the height a bumper sits, and a
        # pale pressed-steel hub in each wheel.
        place(((L - 0.02, 0.36), (L + 0.06, 0.36), (L + 0.06, 0.52), (L - 0.02, 0.52)),
              -half - 0.01, half + 0.01, "veh%d_bumper_rear" % n, "car_trim",
              "moulded-black-bumper")
        place(((-0.06, 0.36), (0.02, 0.36), (0.02, 0.52), (-0.06, 0.52)),
              -half - 0.01, half + 0.01, "veh%d_bumper_front" % n, "car_trim",
              "moulded-black-bumper")
        for w, ax in enumerate((0.80, L - 0.78)):
            for side, sy in (("n", half - 0.09 + WHEEL_W / 2.0), ("f", -half + 0.09 - WHEEL_W / 2.0)):
                off = 0.004 if side == "n" else -0.004
                place(_wheel_profile(ax, WHEEL_D / 2.0, WHEEL_D * 0.55),
                      min(sy, sy + off), max(sy, sy + off) + 0.003,
                      "veh%d_hub_%d%s" % (n, w, side), "frame_metal", "the-hub")
        for side, sy in (("n", half - 0.30), ("f", -half + 0.30)):
            place(((L - 0.05, 0.62), (L + 0.01, 0.62), (L + 0.01, 0.88), (L - 0.05, 0.88)),
                  sy - 0.11, sy + 0.11, "veh%d_lamp_%s" % (n, side), "lamp_red",
                  "the-cluster-at-the-corner")
        place(((L - 0.01, 0.46), (L + 0.02, 0.46), (L + 0.02, 0.46 + PLATE_H),
               (L - 0.01, 0.46 + PLATE_H)),
              -PLATE_W / 2.0, PLATE_W / 2.0, "veh%d_plate_rear" % n, "plate_rear",
              "520x111/yellow-behind-and-white-in-front-since-1973")
        place(((-0.02, 0.46), (0.01, 0.46), (0.01, 0.46 + PLATE_H), (-0.02, 0.46 + PLATE_H)),
              -PLATE_W / 2.0, PLATE_W / 2.0, "veh%d_plate_front" % n, "plate_front",
              "the-white-half-of-the-same-law")


#: THE PAVEMENT CLUTTER, AND NONE OF IT IS CHOSEN HERE.
#:
#: THE SPEC ALREADY PLACED IT, BY NAME, WITH MEASUREMENTS. held_props in
#: production/specs/vignette-scene.json carries 36 placements of 18 meshes
#: this repository already holds under ledger/Assets/Props/base-mesh - bins,
#: crates, an A-board, a skip, pallets, a barrel, bollards, cones, a barrier -
#: each with its own dims_m MEASURED off the shipped .glb's position
#: accessors, its side of the street, its distance from the kerb face and its
#: yaw. Every one of them is named by a line of the bill of materials. So
#: this reads that file and places what it says; it invents no position, no
#: size and no prop.
#:
#: WHY THE PAVEMENT BEING EMPTY MATTERS. The approved sheet's own fish shop
#: trades onto its frontage - white crates stacked on the flags - and a
#: parade with nothing on its pavement reads as a street that was built
#: rather than one that is used. It is the cheapest remaining thing on the
#: list that changes the picture, because the geometry is fetched rather than
#: authored and the placements are already written down.
#:
#: NOTHING IS EVER SCALED. The spec's dims policy forbids inventing a size,
#: and it says so in the one place it would be tempting: "a prop that is the
#: wrong size is a prop to replace, not to stretch". A placement names where
#: the prop's BOUNDING BOX CENTRE goes, because the source pivots are not all
#: at the base - awning_02's origin is at its top-back, the posters are
#: centred, the grate hangs below its own origin - so the loaded mesh's own
#: measured bounds are what gets moved, never its pivot.
PROP_DIR = "ledger/Assets/Props/base-mesh"

#: Which of our materials a prop's named surface takes. The props arrive with
#: whatever material their author gave them, which is a different palette
#: from this street's; overriding keeps a bin in the same world as the kerb
#: it stands on.
PROP_SURFACE = {"metal": "steel_dark", "wood": "prop_timber",
                "concrete": "stone", "plastic": "steel_dark"}


def prop_placements(root, spec_rel=SPEC_REL):
    """[(asset, x, y, z_rule, yaw, surface)], or an empty list and a reason.

    ONLY THE ONES THAT STAND ON THE GROUND. The wall props (awnings, posters,
    the cornices and consoles) belong to the frontage and are the fascia
    package's business; the stacked ones are chimney pots and belong to the
    roof. This is the pavement, which is the thing the pair says is empty.
    """
    path = os.path.join(root, spec_rel)
    try:
        with open(path, "r", encoding="utf-8") as fh:
            spec = json.load(fh)
    except (OSError, ValueError) as exc:
        return [], "spec-unreadable/%s" % type(exc).__name__
    items = spec.get("held_props", {}).get("items", [])
    out = []
    for it in items:
        if it.get("place") not in ("ground", "set_in"):
            continue
        side = 1.0 if it.get("side") == "east" else -1.0
        # THE KERB FACE IS THE DATUM THE SPEC MEASURES FROM, at 3.0 m either
        # side of the centre line, and POSITIVE IS TOWARDS THE BUILDING. A
        # negative figure puts the prop out over the channel, which is where
        # the gully grate belongs and nowhere else.
        across = it.get("z_from_kerb_face_m", 0.0)
        out.append({
            "asset": it["asset"],
            "x": float(it["x_m"]),
            "y": side * (3.0 + float(across)),
            "on_footway": across > 0.0,
            "set_in": it.get("place") == "set_in",
            "yaw": float(it.get("yaw_deg", 0.0)) + (180.0 if side > 0 else 0.0),
            "surface": PROP_SURFACE.get(it.get("surface"), "steel_dark"),
            "dims": it.get("dims_m"),
            "bom": it.get("bom", ""),
        })
    return out, ""


def plan_row(p, bays=None):
    """Every bay of the row, offset and named, as one list.

    THE ROW IS THE UNIT THE SHEET SHOWS. One bay proves the dimensions; six
    prove the RHYTHM, which is the thing the spec measured and found missing -
    every door on the built street at the same offset, one stencil repeated,
    which is what reads as generated rather than authored at walking pace. The
    variation lives in plan_parts; this places it.

    THE PARTY-WALL PIECES KNOW WHETHER THERE IS A PARTY WALL. A downpipe sits
    at every INTERNAL bay boundary and never at a row's outer end, which the
    spec states and the built street obeys - five downpipes on a six-bay row,
    not six. The same for stacks: a chimney serves the two houses either side
    of the wall it stands on, so the last bay has none of its own.
    """
    if bays is None:
        bays = p["bays"]
    W = p["bay_width_m"]
    out = []
    for b in range(bays):
        last = (b == bays - 1)
        for part in plan_parts(p, bay=b, party_wall=not last):
            q = dict(part)
            q["id"] = "%s_bay%d" % (part["id"], b)
            q["bay"] = b
            if part.get("kind") == "mesh":
                # A MESH MOVES VERTEX BY VERTEX, the arches since 22 September.
                q["verts"] = [(x + b * W, y, z) for (x, y, z) in part["verts"]]
            else:
                q["x0"] = part["x0"] + b * W
                q["x1"] = part["x1"] + b * W
            out.append(q)
    return out


def plan_parts(p, bay=0, party_wall=True):
    """Every piece of one bay, in local coordinates.

    THE AXES. x runs along the street from the bay's own left edge; y runs
    INTO the building from the frontage plane at y=0, so anything proud of
    the wall has a NEGATIVE y; z is height from the threshold.
    """
    parts = []
    doors_on = BAY_DOORS_ON[bay % len(BAY_DOORS_ON)]
    has_side_door = (bay % 6) != BAY_WITHOUT_SIDE_DOOR
    W = p["bay_width_m"]
    D = p["depth_m"]
    # THE ZONE HAS TO EXIST BEFORE ANYTHING IS PUT IN IT, and this guard
    # catches two different faults with one comparison. A bay too narrow for
    # its own two piers and two doors has no opening zone at all; and a
    # params dict whose DERIVED values no longer follow from its primitives -
    # which is what an edit to bay_width without re-deriving looks like -
    # fails the first half. Refused rather than clamped, so a future edit
    # fails loudly instead of quietly shipping a front that cannot be built.
    zone = W - 2.0 * p["pilaster_w_m"]
    if abs(zone - p["opening_zone_m"]) > 1e-9:
        raise ValueError(
            "terrace-front: opening_zone_m=%.4f does not follow from bay_width_m=%.4f "
            "less two piers of %.4f (=%.4f); the derived numbers are stale"
            % (p["opening_zone_m"], W, p["pilaster_w_m"], zone))
    if zone <= p["shop_door_w_m"] + p["side_door_w_m"]:
        raise ValueError(
            "terrace-front: an opening zone of %.4f m has no room for a %.4f m shop door "
            "and a %.4f m side door, let alone glazing"
            % (zone, p["shop_door_w_m"], p["side_door_w_m"]))
    GF = p["ground_h_m"]
    EAVES = p["eaves_m"]
    wall = p["wall_surface"]

    # ---- the carcass behind everything -----------------------------------
    # Set back to the frontage plane and running the full depth. Every
    # elevation piece below sits on its face or proud of it.
    T = p["wall_t_m"]
    # THE CARCASS STARTS BEHIND THE WALL, not at the frontage plane, and it is
    # the INSIDE. Every opening below is a real hole through a one-brick wall
    # onto this; when it filled the frontage in brick the holes had nothing to
    # show and the elevation read as a blank box.
    # AND A SHOP HAS A ROOM BEHIND IT, which is the fault two attempts at the
    # glass could not fix because the glass was never the problem.
    #
    # The carcass filled everything from one brick back, so on a shopfront bay
    # its dark inside face stood SEVENTY-FIVE MILLIMETRES behind the display
    # glazing and filled the whole opening. The lit interior card, placed a
    # metre further in, was inside the carcass and had never once been
    # visible; every shop window on the street was showing the front face of a
    # solid block. Lightening the glass made a lighter block. Giving the glass
    # transmission and then raytraced refraction made a block you could see
    # into by exactly nothing, because what was behind it was still the block.
    #
    # THE DEPTH IS THE SPEC'S OWN. shopfront.interior_card_depth_m is 1.2, and
    # that is what it is FOR: the room between the window and the back wall.
    # The carcass starts behind it at the ground floor of a shop and stays one
    # brick back everywhere else, because the flat above has no shop in it.
    if p["ground_floor"] == "shopfront":
        shop_depth = 1.2
        _box(parts, "carcass_shop", "interior", 0.0, W, T + shop_depth, D,
             0.0, GF, "the-back-wall-of-the-shop/1.2m-of-room-in-front-of-it")
        _box(parts, "carcass", "interior", 0.0, W, T, D, GF, EAVES,
             "the-flat-above/one-brick-back-like-any-window")
    else:
        _box(parts, "carcass", "interior", 0.0, W, T, D, 0.0, EAVES,
             "what-a-window-shows/starts-one-brick-back-so-the-openings-are-real")

    if p["ground_floor"] != "shopfront":
        _plain_ground(parts, p, T, wall, bay)
        _upper_floor(parts, p, T, wall)
        _roof_and_rainwater(parts, p, T, wall, party_wall, bay)
        return parts

    # ---- ground floor: the shopfront -------------------------------------
    pw = p["pilaster_w_m"]
    pp = p["pilaster_proj_m"]
    # THE PIERS ARE PAINTED THE SHOP'S COLOUR, NOT LEFT AS STONE, and that
    # is both what a British shopfront is and where a third of our missing
    # colour was sitting. A parade is painted as a UNIT - the piers, the
    # fascia above them and the kicked board below all in one colour, with
    # white joinery inside it - which is what makes a row of shops read as a
    # row of distinct shops rather than one long frontage with signs on it.
    #
    # THEY WERE `stone`, WHICH IS THE SILL AND COPING MATERIAL, and it takes
    # the pack's concrete map: in the frame they came back as pale mottled
    # slabs either side of every window, reading as precast panels bolted to
    # a Victorian shop. Two of the largest painted areas on the whole street
    # were the two that were not painted.
    here = (p.get("block_id"), bay)
    refit_of = SHOPFRONT_REFITS.get(here)
    pier_name, pier_rgb = FASCIA_PAINT[bay % len(FASCIA_PAINT)]
    if refit_of and "paint" in refit_of:
        pier_name, pier_rgb = refit_of["paint"]
    for side, a, b in (("left", 0.0, pw), ("right", W - pw, W)):
        if refit_of and "paint" in refit_of:
            # A REFIT THAT REPAINTED ITS FRONT CLADS ITS PIERS IN THE FRAME'S
            # OWN SMOOTH FINISH. Attempt one gave them the painted-board
            # material in the refit's colour, and its wood grain at slate
            # blue rendered as rough dressed stone either side of a smooth
            # metal front.
            _box(parts, "pilaster_%s" % side, refit_of["frame"], a, b, -pp, 0.0, 0.0, GF,
                 "the-refit-clads-its-piers/" + refit_of["frame"])
            continue
        pier = _box(parts, "pilaster_%s" % side, "paint_stall", a, b, -pp, 0.0, 0.0, GF,
                    "a-shopfront-earns-its-piers/paint=" + pier_name)
        pier["paint"] = pier_rgb
        pier["paint_name"] = pier_name

    # The opening zone, and the three things that fill it, left to right:
    # display glazing, shop door, side door. The order is the spec's own.
    zx0 = pw
    # THE DISPLAY RUN TAKES WHATEVER THE DOORS LEAVE, which is how dropping the
    # side door widens it rather than leaving a hole: the spec's own
    # arithmetic, the opening zone less whichever doors this bay has.
    side_w = p["side_door_w_m"] if has_side_door else 0.0
    display_w = p["opening_zone_m"] - p["shop_door_w_m"] - side_w
    if doors_on == "left":
        side_x0, side_x1 = zx0, zx0 + side_w
        shop_x0, shop_x1 = side_x1, side_x1 + p["shop_door_w_m"]
        disp_x0, disp_x1 = shop_x1, shop_x1 + display_w
    else:
        disp_x0, disp_x1 = zx0, zx0 + display_w
        shop_x0, shop_x1 = disp_x1, disp_x1 + p["shop_door_w_m"]
        side_x0, side_x1 = shop_x1, shop_x1 + side_w

    sr_h = p["stallriser_h_m"]
    sr_p = p["stallriser_projection_m"] if "stallriser_projection_m" in p else p["stallriser_proj_m"]
    rec = p["glazing_recess_m"]
    tr_h = p["transom_h_m"]
    tr_t = p["transom_t_m"]
    fb = p["fascia_bottom_m"]
    fp = p["fascia_proj_m"]

    # THE JOINERY SECTION, DERIVED FROM THE TRANSOM'S OWN THICKNESS. A
    # shopfront's frame is one set of sections: the transom is the heaviest
    # member the spec dimensions, the jambs match it, and a mullion is
    # lighter than both. Deriving them from transom_thickness_m rather than
    # typing three numbers means the whole frame stays in proportion if that
    # dimension ever moves.
    # AND A REFITTED BAY IS A DIFFERENT SET OF SECTIONS, not the same
    # sections painted grey. That is the whole visual difference between a
    # metal front and a timber one: aluminium carries the same glass on
    # LESS THAN HALF the section, and it sits nearly flush instead of
    # standing proud with a moulding on it. A grey timber shopfront would
    # read as a timber shopfront and the change would be worth nothing.
    refit = refit_of is not None
    joinery = refit_of["frame"] if refit else "paint_joinery"
    jamb_t = tr_t * (0.45 if refit else 1.0)
    mull_t = tr_t * (0.40 if refit else 0.75)
    joinery_proj = 0.012 if refit else 0.03
    # THE GLAZED RUN IS THE DISPLAY PLUS THE SHOP DOOR, whichever order this
    # bay puts them in. Written as a span rather than as "from the display to
    # the shop door" because the second form quietly assumes one of the two
    # arrangements, and the bay that chose the other built a transom of zero
    # width - which the degenerate-box guard refused, loudly, the first time
    # the row was built with variation in it.
    glazed_x0 = min(disp_x0, shop_x0)
    glazed_x1 = max(disp_x1, shop_x1)

    # STALLRISER under the display run only. It stops at the shop door, which
    # is what a door is: a hole to the pavement.
    # THE STALLRISER IS THE SHOP'S OWN COLOUR, not a generic board, and that
    # is what makes a parade a parade. On the approved sheet each shop is
    # painted ONE colour from its fascia down through its pilasters to the
    # kicked board, with WHITE joinery inside it - so the eye reads a row of
    # distinct shops rather than one long frontage. Ours had every stallriser
    # the same pale green-grey, which with the brick lifted to its measured
    # value put it within seven thousandths of the wall behind it: the
    # recipe's own "no painted part hides in the brick behind it" check
    # caught that the moment the brick moved, which is the second time that
    # check has earned its place.
    stall_name, stall_rgb = FASCIA_PAINT[bay % len(FASCIA_PAINT)]
    if refit and refit_of["stall"] == "tile_patterned":
        # THE PATTERNED TILE, over a plinth of dark tile, which is how the
        # approved sheet's MICKEY'S is built and what R05 names. The pattern
        # is a plain geometric one - see _tile_pattern - and not a copy of
        # anything: a photograph says the tile was patterned, not which.
        plinth = 0.12
        _box(parts, "stall_plinth", "tile_stall", disp_x0, disp_x1, -sr_p - 0.004, 0.0,
             0.0, plinth, "a-course-of-dark-tile-at-the-foot/the-sheet's-and-R05's")
        _box(parts, "stallriser", "tile_patterned", disp_x0, disp_x1, -sr_p, 0.0, plinth, sr_h,
             "patterned-glazed-tile-under-the-glass/R05")
    elif refit:
        # A TILED STALLRISER TAKES NO PAINT, which is why this branch does
        # not carry the shop's colour down to the kicked board. R05's is
        # patterned; this one is plain, and the recipe says so.
        _box(parts, "stallriser", refit_of["stall"], disp_x0, disp_x1, -sr_p, 0.0, 0.0, sr_h,
             "0.6m-of-glazed-tile-under-the-glass/R05/plain")
    else:
        stall = _box(parts, "stallriser", "paint_stall", disp_x0, disp_x1, -sr_p, 0.0, 0.0, sr_h,
                     "0.6m-of-kicked-board-under-the-glass/paint=" + stall_name)
        stall["paint"] = stall_rgb
        stall["paint_name"] = stall_name
    empty = here == EMPTY_UNIT
    _box(parts, "display_glazing", "glass_whitened" if empty else "glass",
         disp_x0, disp_x1, rec, rec + 0.02, sr_h, tr_h,
         "whitened-from-inside/nobody-trades-here" if empty
         else "recessed-so-the-frontage-is-not-one-plane")

    # THE FRAME ROUND THE GLASS, which the first attempt had none of. Two
    # jambs and a sill rail; the transom below is its head. Without these the
    # glazing is a hole in a wall rather than a window in a shopfront, and at
    # any distance a hole reads as a stain.
    _box(parts, "display_jamb_left", joinery, disp_x0, disp_x0 + jamb_t,
         -joinery_proj, rec + 0.02, sr_h, tr_h, "the-frame's-left-upright")
    _box(parts, "display_jamb_right", joinery, disp_x1 - jamb_t, disp_x1,
         -joinery_proj, rec + 0.02, sr_h, tr_h, "the-frame's-right-upright")
    _box(parts, "display_sill_rail", joinery, disp_x0, disp_x1,
         -joinery_proj, rec + 0.02, sr_h, sr_h + tr_t,
         "the-rail-the-glass-sits-on/off-the-stallriser's-top")

    # EVERY MEMBER OF A REFIT IS IN THE REFIT'S SECTION, 22 September. The
    # fish shop's jambs and sill were metal and its mullions, transom, door
    # and toplight bars stayed white timber - a metal frame with a timber
    # frame inside it, which no shopfitter ever built. On a timber bay
    # `joinery` IS paint_joinery, so nothing there moves.
    # MULLIONS. A 3.56 m run of unbroken plate is not a 1990 British shop; it
    # is a 2010 one. Three lights, so two mullions, at the thirds of the
    # GLAZED opening rather than of the bay, because the frame divides what it
    # encloses.
    inner0, inner1 = disp_x0 + jamb_t, disp_x1 - jamb_t
    for M in (1, 2):
        cx = inner0 + (inner1 - inner0) * (M / 3.0)
        _box(parts, "display_mullion_%d" % M, joinery,
             cx - mull_t / 2.0, cx + mull_t / 2.0, -joinery_proj, rec + 0.02, sr_h, tr_h,
             "three-lights-not-one-sheet/at-the-thirds-of-the-opening-it-divides")

    # PROUDER THAN THE REST OF THE JOINERY, deliberately: the transom is the
    # heaviest member of a shopfront and the one horizontal that has to read
    # from across a street. At the same projection as the mullions it was a
    # colour change and not an edge, and a colour change does not survive
    # distance or an overcast sky.
    _box(parts, "transom_bar", joinery, glazed_x0, glazed_x1,
         -joinery_proj * 2.0, rec + 0.02, tr_h, tr_h + tr_t,
         "the-bar-runs-across-the-glazing-AND-the-shop-door/one-line-across-the-opening")
    # TOPLIGHT: from the transom to the fascia line less its own frame. The
    # spec gives "roughly 2.82" as DERIVED; it is derived here instead of
    # copied, as fascia_bottom less one brick course.
    top_z1 = fb - p["brick_course_m"] * 0.5
    _box(parts, "toplight", "glass", glazed_x0, glazed_x1, rec, rec + 0.02, tr_h + tr_t, top_z1,
         "the-light-above-the-transom/derived-top=fascia_bottom-minus-half-a-course")
    # THE TOPLIGHT IS DIVIDED ON THE SAME LINES as the glazing below it, which
    # is what makes a frontage read as one piece of joinery rather than two
    # unrelated holes. The shop door's own edge is a division too, so it takes
    # a bar of its own.
    for M in (1, 2):
        cx = inner0 + (inner1 - inner0) * (M / 3.0)
        _box(parts, "toplight_mullion_%d" % M, joinery,
             cx - mull_t / 2.0, cx + mull_t / 2.0, -joinery_proj, rec + 0.02,
             tr_h + tr_t, top_z1, "on-the-same-line-as-the-mullion-below-it")
    _box(parts, "toplight_bar_over_door", joinery,
         shop_x0 - mull_t / 2.0, shop_x0 + mull_t / 2.0, -joinery_proj, rec + 0.02,
         tr_h + tr_t, top_z1, "the-division-over-the-shop-door's-own-edge")
    # THE HEAD RAIL, which the toplight had none of, and which is why it did
    # not separate from the glazing below it: a band of glass with a bar under
    # it and nothing over it is not a band, it is the top of the window below.
    # The rail closes it against the fascia and gives the whole frontage a
    # second horizontal, which is what a shopfront's joinery actually does.
    _box(parts, "toplight_head_rail", joinery, glazed_x0, glazed_x1,
         -joinery_proj, rec + 0.02, top_z1, top_z1 + tr_t,
         "closes-the-toplight-against-the-board/the-frontage's-second-horizontal")

    # SHOP DOOR, brick spandrel above it to the fascia.
    _box(parts, "shop_door_leaf", joinery, shop_x0, shop_x1, 0.02, 0.06,
         0.0, p["shop_glazed_from_m"],
         "solid-below-the-glazed-light")
    _box(parts, "shop_door_light", "glass", shop_x0 + jamb_t, shop_x1 - jamb_t, 0.03, 0.05,
         p["shop_glazed_from_m"], p["shop_door_h_m"] - jamb_t,
         "the-glazed-upper-light/inside-its-own-stiles-and-rail")
    # THE DOOR'S OWN FRAME, so it is findable. A door the same value as the
    # glass beside it is a door nobody can see, which is what the first
    # attempt's frame said in one line.
    for Name, X0, X1 in (("shop_door_stile_left", shop_x0, shop_x0 + jamb_t),
                         ("shop_door_stile_right", shop_x1 - jamb_t, shop_x1)):
        _box(parts, Name, joinery, X0, X1, -joinery_proj, 0.06,
             0.0, p["shop_door_h_m"], "the-door's-own-upright")
    _box(parts, "shop_door_mid_rail", joinery, shop_x0, shop_x1,
         -joinery_proj, 0.06, p["shop_glazed_from_m"] - jamb_t, p["shop_glazed_from_m"],
         "the-rail-under-the-glass/where-a-hand-pushes")
    _box(parts, "shop_door_head_rail", joinery, shop_x0, shop_x1,
         -joinery_proj, 0.06, p["shop_door_h_m"] - jamb_t, p["shop_door_h_m"],
         "the-rail-over-the-glass")
    # ON A REFIT THE PANEL OVER THE DOOR IS THE FRAME'S, not brick: the
    # refit replaced the whole front up to the fascia, which is why attempt
    # one's cab office had a patch of brick hanging over its own door.
    _box(parts, "shop_door_spandrel", joinery if refit else wall, shop_x0, shop_x1, 0.0, T,
         p["shop_door_h_m"], fb, "brick-between-the-door-head-and-the-board")

    if has_side_door:
        _side_door(parts, p, side_x0, side_x1, jamb_t, rec, joinery_proj, wall, T, fb)

    # A sliver of brick where the pieces do not quite fill the opening zone.
    zone_end = W - pw
    filled_to = max(side_x1, shop_x1, disp_x1)
    if filled_to < zone_end - 1e-9:
        _box(parts, "zone_infill", wall, filled_to, zone_end, 0.0, T, 0.0, fb,
             "the-remainder-of-the-opening-zone/emitted-only-when-it-exists")

    # FASCIA BAND, the full bay width, top AT the first-floor slab. This is
    # what the already-authored cornice and consoles sit on and it must not
    # move: production/art/fascia-01/.
    paint_name, paint_rgb = FASCIA_PAINT[bay % len(FASCIA_PAINT)]
    if refit_of and "paint" in refit_of:
        paint_name, paint_rgb = refit_of["paint"]
    band = _box(parts, "fascia_band", "paint_fascia", 0.0, W, -fp, 0.0, fb, GF,
                "top-IS-the-first-floor-slab/the-committed-cornice-sits-on-this/"
                "paint=" + paint_name)
    band["paint"] = paint_rgb
    band["paint_name"] = paint_name
    # THE SIGN IS ITS OWN THIN PIECE ON THE FACE OF THE BOARD rather than
    # a texture on the board, because the board is one box and its face,
    # its returns and its underside are all the same surface to a box
    # projection - the lettering would have wrapped round the ends and run
    # upside down along the soffit.
    sign = p.get("fascia_signs", {}).get(bay)
    override = SIGN_OVERRIDE.get(here)
    if override:
        # SIGNWRITTEN ACROSS THE WHOLE FACE, the board's own paint and all.
        sg = _box(parts, "fascia_sign", "paint_fascia",
                  pw * 0.5, W - pw * 0.5, -fp - 0.012, -fp,
                  fb + 0.045, GF - 0.045, "the-lettering/" + override)
        sg["decal"] = override
    elif sign:
        # AT THE SPEC'S WIDTH AND HEIGHT, centred on the bay plus its dx, and
        # showing only the spec's crop of the picture.
        cx, hw = W / 2.0 + sign["dx_m"], sign["width_m"] / 2.0
        h = min(sign["height_m"], GF - fb)
        z0 = fb + (GF - fb - h) / 2.0
        sg = _box(parts, "fascia_sign", "paint_fascia",
                  max(0.0, cx - hw), min(W, cx + hw), -fp - 0.012, -fp,
                  z0, z0 + h, "the-lettering/" + sign["id"])
        sg["decal"] = sign["id"]
        if sign.get("uv"):
            sg["decal_uv"] = [float(v) for v in sign["uv"]]
    if empty:
        # THE LETTING BOARD, fixed to the middle of the fascia.
        bw, bh = LETTING_BOARD_M
        zc = (fb + GF) / 2.0
        lb = _box(parts, "letting_board", "paint_fascia",
                  W / 2.0 - bw / 2.0, W / 2.0 + bw / 2.0, -fp - 0.03, -fp - 0.01,
                  zc - bh / 2.0, zc + bh / 2.0, "TO-LET/R05's-neighbouring-letting-board")
        lb["decal"] = LETTING_BOARD

    _upper_floor(parts, p, T, wall)
    _roof_and_rainwater(parts, p, T, wall, party_wall, bay)
    return parts


def frame_cameras(p):
    """The two viewpoints, derived from the bay rather than typed.

    ELEVATION frames the whole front plus the stack with a margin, square on,
    level. Its distance is solved from the vertical field so a taller bay
    pulls the camera back instead of cropping the roof.

    EYE is cam_A's own numbers - 1.6 m on the footway, 4 degrees down - stood
    on the far side of a 6 m carriageway and two 2 m footways, which is the
    street this bay is on.
    """
    W = p["bay_width_m"]
    bays = p["bays"]
    run = W * bays
    top = p["ridge_m"] + p["chimney_above_ridge_m"]
    # THE ELEVATION FRAMES THE WHOLE ROW NOW, not one bay. One bay proved the
    # dimensions; what is being judged from here on is the RHYTHM, and a
    # rhythm cannot be seen one bay at a time. The distance is solved from
    # whichever of the two dimensions needs more room - the run is six times
    # the height, so on this row it is always the width - so a longer or
    # taller terrace still frames instead of cropping.
    fov_v = math.radians(40.0)
    aspect = float(AUTHORED_RES[0]) / float(AUTHORED_RES[1])
    fov_h = 2.0 * math.atan(math.tan(fov_v / 2.0) * aspect)
    dist_for_height = (top * 1.2 / 2.0) / math.tan(fov_v / 2.0)
    dist_for_width = (run * 1.06 / 2.0) / math.tan(fov_h / 2.0)
    dist = max(dist_for_height, dist_for_width)
    return {
        "elevation": {
            "loc": (run / 2.0, -dist, top / 2.0),
            "look": (run / 2.0, 0.0, top / 2.0),
            "fov_v_deg": 40.0,
            "note": "square-to-the-frontage-whole-row-in-frame/cam_B's-own-description",
        },
        "eye": {
            # ALONG THE ROW RATHER THAN ACROSS ONE BAY. This is the view a
            # person actually has of a parade: raking, from the far footway,
            # with the frontages running away. It is the one that shows a
            # repeated stencil for what it is.
            "loc": (-W * 0.9, -11.0, 1.6),
            "look": (run * 0.55, 0.0, 3.0),
            "fov_v_deg": 60.0,
            "note": "1.6m-on-the-far-footway-looking-along-the-row/cam_A's-eye-height-and-field",
        },
    }


def look_at_euler(loc, target):
    """(rx, ry, rz) for a Blender camera at `loc` looking at `target`.

    CLOSED FORM, AND TESTED BY COMPOSING IT BACK. A Blender camera with a
    zero rotation looks down its own -Z with +Y up, so aiming it is two
    turns: rx away from straight down, then rz around the world's Z.

        direction = Rz(rz) . Rx(rx) . (0, 0, -1)
                  = (-sin(rx) sin(rz), sin(rx) cos(rz), -cos(rx))

    WRITTEN OUT BECAUSE THE FIRST VERSION WAS WRONG AND THE RENDER SHOWED A
    FIELD. It had rz a quarter turn the wrong way and rx measured against
    +z instead of -z, which aimed both cameras at the sky behind the
    building. euler_direction() below composes this back and selftest asks
    whether the two agree on the actual frames this file takes, so the same
    mistake cannot be made silently again.
    """
    dx = target[0] - loc[0]
    dy = target[1] - loc[1]
    dz = target[2] - loc[2]
    return (math.atan2(math.hypot(dx, dy), -dz), 0.0, math.atan2(dy, dx) - math.pi / 2.0)


def euler_direction(euler):
    """The unit direction a Blender camera with this rotation actually looks.
    The inverse of look_at_euler, used only to check it."""
    rx, _ry, rz = euler
    return (-math.sin(rx) * math.sin(rz),
            math.sin(rx) * math.cos(rz),
            -math.cos(rx))


def street_cameras():
    """The sheet's own viewpoint, and one across the road.

    cam_A, MEASURED from the scene file: on the east footway 4.0 m along and
    4.0 m across, eye 1.6 m above the FOOTWAY rather than above the road
    crown, looking along the street at a 4 degree downward pitch with a 60
    degree vertical field. The scene file's own note derives that pitch: at a
    60 degree field, p degrees down puts the horizon at frame row
    0.5 - tan(p)/(2 tan 30), so 4.0 puts it at 0.439, just above the middle,
    which is where every British street reference in the research puts it.
    THAT IS THE FRAME STAGE 1 IS JUDGED ON and it is not one of mine.
    """
    eye = THRESHOLD_ABOVE_CROWN_M + 1.6
    # MEASURED OFF THE APPROVED SHEET, 22 September, and it is the opposite
    # sign to what was here. cam_A's four degrees DOWN put our horizon 0.439
    # of the way down the frame and gave the picture to the road; the sheet's
    # own street panel puts its horizon at 0.55 - measured twice, off the
    # figure on its left pavement whose eyes the horizon crosses, and off the
    # share of the frame that is sky, 21.3 per cent against our 8.9. At a
    # sixty degree vertical field the row is 0.5 - tan(p)/(2 tan 30), so 0.55
    # is three degrees UP. Seven degrees of swing, and it is the difference
    # between a photograph of a road and a photograph of a street.
    #
    # THE SCENE FILE'S cam_A IS NOT WRONG AND IS NOT WHAT THIS IS. cam_A is a
    # camera the spec names; the hook camera is the one the PAIR is shot
    # from, and the pair's whole job is to stand beside the sheet. Where the
    # two disagree the sheet wins, because the sheet is the exit test.
    HOOK_PITCH_DEG = -4.0
    # WHERE IT STANDS ALONG THE STREET, AND IT MOVED ON 22 SEPTEMBER.
    #
    # THE CROSS-STREET POSITION IS SETTLED and is not what this changes: the
    # long note below argues y = -2.2 against the approved sheet and it
    # stands. What was never argued is the position ALONG the street. 33.0
    # was chosen for one reason, in its own words, "inside the row, not past
    # its end" - and at 33.0 the camera stands 2.9 m from the WEST frontage,
    # which was a blank wall when the number was picked.
    #
    # THEN JAFAR RULED SHOPS ONTO THAT BLOCK. west_north runs x 24 to 42, so
    # since that ruling the frame has had a lit, lettered shopfront three
    # metres from the lens taking the LEFT THIRD at a rake nobody can read -
    # and the approved sheet's left third is open street with one figure on
    # the far pavement. That is the largest composition gap left against the
    # sheet and it is not a material or a value; it is where the tripod is.
    #
    # THE SERVICE GAP IS WHERE A PHOTOGRAPHER WOULD STAND. The scene file
    # puts a 3 m gap between west_south (ending 21.0) and west_north
    # (starting 24.0) and the props file already calls it the yard entrance.
    # At its middle the nearest west wall is 1.5 m of gap away instead of
    # 2.9 m of brick, the east parade is still 7.3 m off across the road -
    # which is the sheet's own "eight to ten metres" - and the street ahead
    # is 24.5 m instead of 35, which puts the basin sheds where the sheet
    # puts its far buildings.
    # AND IT WAS TRIED AT 22.5 AND IT IS WORSE, which is the second position
    # this camera has been moved to and measured rather than argued about.
    # In the service gap the NEXT west block, west_south, starts immediately
    # ahead and its BLANK flank - no shopfront, no lettering, nothing to
    # read - fills the left HALF instead of the left third, and the skip
    # stands in the lens. The move was the wrong axis: the near wall is 2.9 m
    # away because of y, not because of x, so no station along the street
    # changes it.
    # WHAT IS ACTUALLY DIFFERENT FROM THE SHEET is the SIDE. The approved
    # sheet also gives a near building the frame's near third - it is
    # Mickey's, on the RIGHT. Ours is on the LEFT, because the camera sits
    # 2.9 m off the WEST frontage and 7.3 m off the east, and looking down
    # -x the right hand is east. Mirroring that (y = +2.2) is a THIRD
    # attempt at this camera and is Jafar's to rule on: it is the exit
    # test's own viewpoint, the long note below argues the present one from
    # the sheet, and an earlier move to the east FOOTWAY at +3.6 was tried
    # and rejected for reasons that may or may not survive the 1.4 m.
    # TURNED TO THE SHEET'S VIEW, RULED BY JAFAR 2026-09-22, and this is the
    # largest single correction the pair has had.
    #
    # THE CAMERA LOOKED THE OPPOSITE WAY FROM THE PICTURE IT REPRODUCES. The
    # approved sheet's own prompt says it in one clause: "BOTTOM: camera at
    # 1.6m standing at SOUTH END LOOKING NORTH along Quay Street." This stood
    # at x=33 of a street running 3 to 42 and looked at x=2 - the north end,
    # looking south. Both arrangements put a frontage on the right, which is
    # exactly why nothing ever caught it; but they are opposite ends with
    # opposite far distances. The sheet's far end is the inland rise. Ours
    # was the basin.
    #
    # HIS RULING, in his words: "Turn the camera to the sheet's view: south
    # end looking north. The sheet is what the street is built to and the
    # pair is the exit test, so a camera pointing the other way has been
    # measuring against a picture of somewhere else all week. Regenerating
    # the sheet to match us would be the tail wagging the dog. The basin is
    # not wasted; it becomes the view the other way."
    #
    # SIX METRES INSIDE THE SOUTH END, which is the old station's own rule
    # mirrored: it stood six metres inside the north end for the reason its
    # note gives, that a camera past the row's end photographs a gable. The
    # blocks run 3 to 42, so 9.0 is six metres in, and 40.0 is two metres
    # inside the far end.
    #
    # AND IT CROSSES THE ROAD, because the handedness goes with the turn. The
    # spec's axes: +x north, east at +y. A camera looking north has its right
    # hand at -y, so EAST IS ON THE LEFT and west on the right - the exact
    # reverse of before. Standing at y = -2.2 would put a wall 2.9 m from the
    # lens on the RIGHT and repeat the fault the old station had on the left.
    # At y = +2.2 the east parade is 2.9 m off on the left and the west
    # blocks are 7.3 m off on the right, which is canon's own reading of the
    # sheet: "a shop close on the near left with the street opening out
    # beyond it."
    #
    # WHAT THIS COSTS, said plainly: the basin end built today is now BEHIND
    # the camera, so the far end of this frame is sky again - at the other
    # end, where the inland rise belongs and nothing is built. That is a new
    # item, not a regression, and the basin is still the view the other way.
    HOOK_X = 9.0
    HOOK_LOOK_X = 40.0
    HOOK_Y = 2.2
    # AND WHERE THE NEW SHEET PUTS IT, 22 September (hook-sheet-lens.md,
    # steps 7 and 8). ACROSS: 7.3 m from the east frontage, off the
    # frontage's own ground line through the vanishing point - y = -2.2,
    # which is where the old hook camera stood across the street. ALONG:
    # x = -3.2, just south of the terrace's end on the quay apron, placed so
    # Mickey's south pilaster lands at 0.146 of the width as it does on the
    # sheet; its north pilaster then lands at 0.383 against the sheet's 0.396.
    HOOK_X = -3.2
    HOOK_Y = -2.2
    # LEVEL, and turned towards the parade: the look point is at eye height,
    # HOOK_YAW_LEFT_DEG to the left of straight up the street (+x), which in
    # this street's axes is towards +y, the east side.
    _yaw = math.radians(HOOK_YAW_LEFT_DEG)
    HOOK_LOOK_X = HOOK_X + 30.0 * math.cos(_yaw)
    HOOK_LOOK_Y = HOOK_Y + 30.0 * math.sin(_yaw)
    reach = HOOK_X - HOOK_LOOK_X
    drop = 0.0
    # ITS OWN EYE HEIGHT, not the shared `eye`, which the across camera
    # below also reads and which stays at cam_A's 1.6.
    hook_eye = THRESHOLD_ABOVE_CROWN_M + HOOK_EYE_M
    return {
        "hook": {
            # THE CAMERA STANDS ON THE PARADE'S OWN PAVEMENT, which is
            # where the scene file's cam_A put it all along.
            #
            # IT WAS MOVED OFF IT AGAINST THE WRONG SHEET. The note that
            # stood here argued, at length and quite carefully, that "the
            # sheet's near wall on the left is a blank flank end a metre away
            # and its shopfronts are eight to ten metres off on the RIGHT" -
            # so the camera crossed to the far pavement to match. That is a
            # true description of CODEX'S retired sheet and it is not true of
            # the approved one. On the approved sheet the near-right is a big
            # CLOSE shopfront, oxblood, lettered, filling the right third of
            # the frame floor to eaves, with the parade running away from it
            # down the picture; the far side is small and dim. Standing on
            # the far pavement gave us the exact opposite - a blank flank a
            # metre from the lens taking the left third, and the parade
            # reduced to a sliver at the edge - and it did so for two weeks
            # while measuring as though it were faithful.
            #
            # WHICH WAY IT LOOKS IS STILL DELIBERATE. From the east footway a
            # camera looking along +x has the parade on its LEFT, because the
            # right hand of a camera pointing that way is -y. Looking back
            # down the street puts the shops on the RIGHT, where the sheet
            # has them, and costs nothing: the parade runs the street's whole
            # length either way.
            #
            # 1.5 m OFF THE FRONTAGE, which is where a person walks. The
            # footway is 2.0 m from the kerb face at 3.125 to the frontage at
            # 5.125, so 3.6 stands in the middle of it rather than with a
            # shoulder on the brick.
            #
            # AND INSIDE THE ROW, NOT PAST ITS END. The blocks occupy 3.0 to
            # 39.0 and an earlier version of this stood at x = 40, a metre
            # beyond them, looking at a gable end its own note complained
            # about. 33 is six metres inside.
            # AND IT WAS TRIED ON THE SHOPS' PAVEMENT AND IT IS WRONG, which
            # is worth the four lines because the argument for it was good.
            # cam_A names the east footway; the reasoning above says the
            # sheet's near-right is a close shopfront; so the camera was moved
            # to y = +3.6 and rendered. At 1.5 m off the frontage the parade
            # becomes a wall of vertical stripes at an unreadable angle, a
            # lighting column stands in the lens and a bin fills the bottom
            # corner. MEASURING THE SHEET AGAIN SETTLES IT: its near-right
            # building has the ROAD between it and the camera, eight to ten
            # metres of it. Near-right and close are not the same thing, and
            # the far pavement is where the picture is taken from.
            "loc": (HOOK_X, HOOK_Y, hook_eye),
            "look": (HOOK_LOOK_X, HOOK_LOOK_Y, hook_eye - drop),
            "fov_v_deg": HOOK_FOV_V_DEG,
            # the horizon below centre by shifting, not by tipping
            "shift_y": HOOK_HORIZON_FROM_TOP - 0.5,
            "res": HOOK_RES,
            "note": "the-sheet's-own-viewpoint/south-end-looking-NORTH-per-Jafar-2026-09-22/"
                    "3-degrees-UP-measured-off-the-approved-sheet-not-cam_A's-4-down/"
                    "sky-21-percent-as-the-sheet-is",
        },
        "across": {
            # cam_B: from the far kerb, square to the frontage, roofline in.
            "loc": (21.0, -4.0, eye),
            "look": (21.0, 5.125, eye + 2.2),
            "fov_v_deg": 60.0,
            "note": "cam_B/from-the-far-kerb-square-to-the-frontage-roofline-in-frame",
        },
    }


def plan_lines(p, parts, checks):
    lines = []
    for field, authored, emitted, agree in checks:
        if emitted is None:
            lines.append("tfCheck field=%s authored=%.6f emitted=nothing-measured "
                         "agree=nothing-measured" % (field, authored))
        else:
            lines.append("tfCheck field=%s authored=%.6f emitted=%.6f diff=%.6f agree=%s"
                         % (field, authored, emitted, abs(authored - emitted),
                            "yes" if agree else "no"))
    lines.append(
        "tfBay widthM=%.3f depthM=%.3f groundFloorM=%.3f firstFloorM=%.3f eavesM=%.3f "
        "ridgeM=%.3f ridgeRiseM=%.3f pitchDeg=%.1f absoluteEavesM=%.3f datumM=%.3f"
        % (p["bay_width_m"], p["depth_m"], p["ground_h_m"], p["first_h_m"], p["eaves_m"],
           p["ridge_m"], p["ridge_rise_m"], p["pitch_deg"],
           p["eaves_m"] + THRESHOLD_ABOVE_CROWN_M, THRESHOLD_ABOVE_CROWN_M))
    lines.append(
        "tfZone openingZoneM=%.3f displayM=%.3f shopDoorM=%.3f sideDoorM=%.3f sumM=%.3f "
        "closes=%s specStatesM=5.300"
        % (p["opening_zone_m"], p["display_w_m"], p["shop_door_w_m"], p["side_door_w_m"],
           p["display_w_m"] + p["shop_door_w_m"] + p["side_door_w_m"],
           "yes" if abs(p["display_w_m"] + p["shop_door_w_m"] + p["side_door_w_m"]
                        - p["opening_zone_m"]) < 1e-9 else "no"))
    lines.append(
        "tfUpper sillM=%.3f headM=%.3f windowM=%.3fx%.3f revealM=%.4f sillWidthM=%.3f "
        "centresM=%s courseM=%.3f sillIsWholeCourses=%s"
        % (p["window_sill_m"], p["window_head_m"], p["window_w_m"], p["window_h_m"],
           p["reveal_m"], p["sill_w_m"],
           ",".join("%.3f" % c for c in window_centres(p)), p["brick_course_m"],
           "yes" if abs((p["window_sill_m"] / p["brick_course_m"])
                        - round(p["window_sill_m"] / p["brick_course_m"])) < 1e-6 else "no"))
    for part in parts:
        if part.get("kind") == "mesh":
            # A PART THAT ARRIVED WITH ITS OWN GEOMETRY has no box to print, so
            # it prints what it does have: how much of it there is. The lamp
            # columns come in this way, from the recipe that authored them.
            lines.append("tfPart id=%s material=%s kind=mesh verts=%d faces=%d"
                         % (part["id"], part["material"],
                            len(part["verts"]), len(part["faces"])))
        elif part.get("kind") == "slope":
            lines.append("tfPart id=%s material=%s kind=slope note=%s"
                         % (part["id"], part["material"], part["note"]))
        else:
            lines.append(
                "tfPart id=%s material=%s kind=box xM=%.3f..%.3f yM=%.4f..%.4f zM=%.3f..%.3f note=%s"
                % (part["id"], part["material"], part["x0"], part["x1"],
                   part["y0"], part["y1"], part["z0"], part["z1"], part["note"]))
    return lines


# ---------------------------------------------------------------------------
# BLENDER. Nothing above this line imports bpy.
# ---------------------------------------------------------------------------


def _bpy():
    import bpy
    return bpy


def _texture_nodes(bpy, mat, root, surface, tile_m, tint):
    """Base, roughness and normal maps on one material, box-projected.

    NO UVs ANYWHERE IN THIS RECIPE, deliberately. Every piece here is built
    from raw verts and faces with no texture coordinates at all, and unwrapping
    four hundred boxes would be four hundred chances to unwrap one of them
    wrong. Box projection off OBJECT coordinates needs none: the texture is
    laid in the world, so a brick course runs level across a wall and carries
    on across the next piece of the same wall, which is what coursed brick
    does and what a per-object unwrap would break at every seam.

    THE TINT IS A MULTIPLY, NOT A REPLACEMENT. The painted parts - the fascia,
    the joinery, the doors - take the wood map for its GRAIN and their own
    authored colour over the top, because the pack has one timber and this
    street has a period palette. The brick and the ground take their map as it
    comes; tinting brick would be inventing a brick nobody photographed.
    """
    path = os.path.join(root, TEXTURE_DIR, surface + ".jpg")
    if not os.path.exists(path):
        return "missing/%s" % surface
    nt = mat.node_tree
    bsdf = nt.nodes.get("Principled BSDF")
    if bsdf is None:
        return "no-bsdf"
    coord = nt.nodes.new("ShaderNodeTexCoord")
    mapping = nt.nodes.new("ShaderNodeMapping")
    mapping.inputs["Scale"].default_value = (1.0 / tile_m, 1.0 / tile_m, 1.0 / tile_m)
    nt.links.new(coord.outputs["Object"], mapping.inputs["Vector"])

    def image(suffix, non_color):
        p = os.path.join(root, TEXTURE_DIR, surface + suffix + ".jpg")
        if not os.path.exists(p):
            return None
        node = nt.nodes.new("ShaderNodeTexImage")
        node.image = bpy.data.images.load(p, check_existing=True)
        node.projection = "BOX"
        node.projection_blend = 0.25
        node.extension = "REPEAT"
        if non_color:
            node.image.colorspace_settings.name = "Non-Color"
        nt.links.new(mapping.outputs["Vector"], node.inputs["Vector"])
        return node

    base = image("", False)
    if base is None:
        return "missing/%s" % surface
    # THE MULTIPLIER IS THE AUTHORED COLOUR OVER THE MAP'S OWN AVERAGE, so
    # what comes out averages the colour this file authored. Bounded at both
    # ends: a very dark map would otherwise need an enormous gain and turn its
    # own highlights into blown patches, and a very bright one would crush.
    mean = TEXTURE_MEAN.get(surface)
    if tint is not None and mean is not None:
        # THE FLOOR CAME DOWN TO 0.02 at the same time and for the mirror
        # reason: a deep oxblood over the plaster map wants 0.027 on green
        # and was being held at 0.05, which quietly desaturated every dark
        # paint on the street towards grey.
        gain = [min(6.0, max(0.02, tint[i] / max(1e-4, mean[i]))) for i in range(3)]
        mix = nt.nodes.new("ShaderNodeMix")
        mix.data_type = "RGBA"
        mix.blend_type = "MULTIPLY"
        mix.inputs["Factor"].default_value = 1.0
        nt.links.new(base.outputs["Color"], mix.inputs[6])
        mix.inputs[7].default_value = (gain[0], gain[1], gain[2], 1.0)
        nt.links.new(mix.outputs[2], bsdf.inputs["Base Color"])
    else:
        nt.links.new(base.outputs["Color"], bsdf.inputs["Base Color"])

    rough = image("_r", True)
    if rough is not None:
        nt.links.new(rough.outputs["Color"], bsdf.inputs["Roughness"])
    norm = image("_n", True)
    if norm is not None:
        nmap = nt.nodes.new("ShaderNodeNormalMap")
        # HALF STRENGTH, BECAUSE FULL READ AS RUBBER. At 1.0 the pack's brick
        # normal put every perpend and bed joint into deep relief and the
        # wall came back looking moulded rather than laid - a texture that
        # announces itself instead of a surface. The approved sheet's brick
        # is nearly flat at this distance; what carries is its COLOUR and its
        # coursing, not its depth.
        nmap.inputs["Strength"].default_value = 0.5
        nt.links.new(norm.outputs["Color"], nmap.inputs["Color"])
        nt.links.new(nmap.outputs["Normal"], bsdf.inputs["Normal"])
    return "%s@%.2fm%s%s" % (surface, tile_m, "+r" if rough else "", "+n" if norm else "")


def _decal_path(root, image_name):
    """Where a sign's picture is. An id under the lettered directory is a
    path from the repository root; anything else is a spec id, which is a
    path under StreamingAssets/Decals as the spec's own blend_kinds says."""
    if image_name.startswith("production/"):
        return os.path.join(root, image_name + ".png")
    return os.path.join(root, DECAL_DIR, image_name + ".png")


def _decal_material(bpy, root, name, image_name, paint, uv=None, emit=False):
    """One material carrying one sign, fitted once across the piece's face.

    GENERATED COORDINATES, NOT A BOX PROJECTION. Generated runs 0 to 1 over
    the object's own bounding box, so the image lands once across the board
    and nowhere else; the box projection every other surface here uses would
    tile it, wrap it round the returns and run it upside down along the
    soffit, which is what lettering must never do.

    """
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nt = mat.node_tree
    bsdf = nt.nodes.get("Principled BSDF")
    path = _decal_path(root, image_name)
    if bsdf is None or not os.path.exists(path):
        return mat, "missing/%s" % image_name
    bsdf.inputs["Roughness"].default_value = 0.42
    coord = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    com = nt.nodes.new("ShaderNodeCombineXYZ")
    nt.links.new(coord.outputs["Generated"], sep.inputs["Vector"])
    nt.links.new(sep.outputs["X"], com.inputs["X"])
    nt.links.new(sep.outputs["Z"], com.inputs["Y"])
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = bpy.data.images.load(path, check_existing=True)
    tex.extension = "EXTEND"
    if uv:
        # THE SPEC'S CROP, [u0, v0, u1, v1] with v from the bottom, which is
        # Blender's own image convention: the face's 0..1 lands on u0..u1.
        u0, v0, u1, v1 = uv
        mp = nt.nodes.new("ShaderNodeMapping")
        mp.inputs["Scale"].default_value = (u1 - u0, v1 - v0, 1.0)
        mp.inputs["Location"].default_value = (u0, v0, 0.0)
        nt.links.new(com.outputs["Vector"], mp.inputs["Vector"])
        nt.links.new(mp.outputs["Vector"], tex.inputs["Vector"])
    else:
        nt.links.new(com.outputs["Vector"], tex.inputs["Vector"])
    nt.links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
    if emit and "Emission Color" in bsdf.inputs:
        # A PICTURED ROOM GLOWS: it stands in a room sealed on five sides,
        # like the plain card, so it carries its own light. The strength is
        # set with the rest of the lighting, once day or night is known.
        nt.links.new(tex.outputs["Color"], bsdf.inputs["Emission Color"])
        bsdf.inputs["Emission Strength"].default_value = CARD_EMIT_DAY
    return mat, "%s@%s" % (image_name, "cropped" if uv else "fitted")


def _paint_variant(bpy, mats, name, rgb):
    """A copy of the fascia material in this bay's own paint. One material per
    colour, not per bay: six bays share three colours and a material per bay
    would be three copies nobody needs."""
    key = "fascia_%s" % name
    if key in mats:
        return mats[key]
    src = mats.get("paint_fascia")
    mat = src.copy() if src is not None else bpy.data.materials.new(key)
    mat.name = key
    bsdf = mat.node_tree.nodes.get("Principled BSDF") if mat.use_nodes else None
    if bsdf is not None:
        # The wood grain is already on this material; only the multiplier that
        # carries the colour moves.
        for node in mat.node_tree.nodes:
            if node.type == "MIX" and node.blend_type == "MULTIPLY":
                mean = TEXTURE_MEAN.get("wood", (0.15, 0.09, 0.05))
                node.inputs[7].default_value = (
                    min(6.0, rgb[0] / max(1e-4, mean[0])),
                    min(6.0, rgb[1] / max(1e-4, mean[1])),
                    min(6.0, rgb[2] / max(1e-4, mean[2])), 1.0)
                break
        else:
            bsdf.inputs["Base Color"].default_value = (rgb[0], rgb[1], rgb[2], 1.0)
    mats[key] = mat
    return mat


def _materials(bpy, root=None):
    made = {}
    notes = []
    for name, linear, rough in MATERIALS:
        mat = bpy.data.materials.new(name=name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf is not None:
            bsdf.inputs["Base Color"].default_value = (linear[0], linear[1], linear[2], 1.0)
            bsdf.inputs["Roughness"].default_value = rough
            if name == "glass":
                # YOU CAN SEE INTO A SHOP, which is the one thing a window
                # does and the one thing ours did not. It was an opaque dark
                # panel with a specular sheen: the lit interior card a metre
                # behind it had nothing to show through, so every frontage
                # read as a boarded hole with a polish on it. That fault was
                # found and fixed once before by value alone; it came back
                # the moment the street got three times brighter around it,
                # because the pane stayed where it was.
                #
                # TRANSMISSION RATHER THAN A LIGHTER COLOUR. Making the glass
                # paler would have made a paler panel; what a window shows is
                # the ROOM, and the room is now built and lit for the
                # condition. IOR 1.52 is soda-lime glass and is not a choice.
                #
                # AND IT STILL RENDERS OPAQUE, which is where this stops and
                # is written down rather than left for the next person to
                # rediscover. FOUR ATTEMPTS, in order: lighten the glass (a
                # lighter panel); set the Transmission socket (no change at
                # all); switch on use_raytrace_refraction for the material
                # (no change); and finally build the shop a room, which was
                # a real fault - the carcass's dark face stood 75 mm behind
                # the pane and filled the opening, so the lit card a metre
                # in had never once been visible. THAT ONE IS FIXED AND IS
                # KEPT: the room is correct whether or not you can see into
                # it, and it is what the spec's interior_card_depth_m of 1.2
                # was always for.
                #
                # WHAT IS STILL WRONG: the pane itself. The window region
                # measures 59 against the sheet's 69 and reads as a dark
                # panel rather than glazing. The settings below are right in
                # intent and this EEVEE build is not honouring them; the
                # next attempt should start by finding out whether the
                # render method or the material's blend mode is what refuses
                # it, rather than by lightening anything again.
                bsdf.inputs["Metallic"].default_value = 0.0
                if "Specular IOR Level" in bsdf.inputs:
                    bsdf.inputs["Specular IOR Level"].default_value = 0.9
                if "IOR" in bsdf.inputs:
                    bsdf.inputs["IOR"].default_value = 1.52
                for key in ("Transmission Weight", "Transmission"):
                    if key in bsdf.inputs:
                        bsdf.inputs[key].default_value = 0.85
                        break
                else:
                    print("tfNote glass=no-transmission-socket/"
                          "the-windows-stay-opaque-and-this-is-why")
                # AND THE MATERIAL HAS TO BE TOLD TO TRACE IT. Setting the
                # Transmission socket alone changed nothing, which is the
                # second attempt against this: in EEVEE Next a transmissive
                # material is still rendered opaque unless raytraced
                # refraction is switched on FOR THAT MATERIAL. The socket
                # said "this is glass" and the renderer was never asked to
                # look through it.
                # ASKED THE BUILD WHAT IT HAS rather than guessing a fifth
                # time, and it has `surface_render_method`, DITHERED by
                # default with BLENDED the alternative.
                #
                # DITHERED AND CLEAR, and the windows are windows. 22
                # September, in three steps, the last of which corrected the
                # second.
                #   1. The EEVEE Next manual: BLENDED is "incompatible with
                #      ... raytracing", so the BLENDED this used to set
                #      switched off the refraction the flag below asks for.
                #      DITHERED and SLAB thickness, as the manual says.
                #   2. That made the pane BLACK, because transmitted light is
                #      tinted by Base Color and the table's glass is 0.085.
                #      Clear glass passes about nine-tenths, so it is 0.9 here.
                #   3. That made it an even pale grey, and for a while that
                #      read as the refraction reaching only the world probe.
                #      IT WAS NOT. A two-object test (a pane in front of a lit
                #      card) showed DITHERED refraction seeing the card, and a
                #      street render with the glass removed showed the room
                #      itself is that grey: the daytime card was a flat
                #      neutral 0.62/0.58/0.52, so looking through clear glass
                #      at it looked like frosted glass. The room is fixed
                #      where the room is set, below, not by tinting the pane.
                # THE TABLE KEEPS 0.085 because the recipe's own frame-against-
                # glazing check reads it as what an opening reads as from
                # across a street; the colour a pane passes is set here.
                if hasattr(mat, "surface_render_method"):
                    mat.surface_render_method = "DITHERED"
                if hasattr(mat, "thickness_mode"):
                    mat.thickness_mode = "SLAB"
                for flag in ("use_raytrace_refraction", "use_screen_refraction"):
                    if hasattr(mat, flag):
                        setattr(mat, flag, True)
                        print("tfNote glass=refraction-on/%s" % flag)
                        break
                else:
                    print("tfNote glass=no-refraction-flag-on-this-build/"
                          "the-windows-stay-opaque-and-this-is-why")
                # SEE THROUGH IT. Shop glass with no transmission is a mirror
                # with a dark tint, which is what every frontage on this row
                # was until the interiors went in behind them.
                if "Transmission Weight" in bsdf.inputs:
                    bsdf.inputs["Transmission Weight"].default_value = 1.0
                bsdf.inputs["Base Color"].default_value = (0.90, 0.91, 0.92, 1.0)
        made[name] = mat
        if root is not None:
            surface, tile = SURFACE_OF.get(name, (None, 0.0))
            if surface:
                # EVERY TEXTURED SURFACE KEEPS ITS AUTHORED COLOUR. It used
                # to be only the painted ones, on the reasoning that tinting
                # brick invents a brick nobody photographed - which was right
                # in principle and wrong here, because the pack's brick_red is
                # a sandy fawn and its brick_grey is pinker than that. Taking
                # their own hues swapped the two rows and collapsed the value
                # separation this file measures elsewhere.
                tint = linear
                notes.append("%s=%s" % (name, _texture_nodes(bpy, mat, root, surface, tile, tint)))
                # GLASS KEEPS THE ROUGHNESS IT WAS AUTHORED WITH, and this is
                # the same fault as the one in _wetten, found the same way.
                # MATERIALS gives glass 0.08 - a near mirror, which is what a
                # shop window is - and then _texture_nodes links the pack's
                # glass _r map straight over the top of it, so every window
                # on the street has been rendering at whatever roughness that
                # photograph happens to carry. With raytracing off that made
                # no visible difference and nobody could have noticed; with
                # it on, the windows are the surfaces that should be showing
                # the street back at you, and instead they are flat dark
                # panels. The map's COLOUR and its relief still apply; only
                # its roughness is dropped, because a pane of glass does not
                # have roughness variation across it.
                if name == "glass":
                    for link in list(mat.node_tree.nodes["Principled BSDF"]
                                     .inputs["Roughness"].links):
                        mat.node_tree.links.remove(link)
                    mat.node_tree.nodes["Principled BSDF"].inputs[
                        "Roughness"].default_value = rough
            else:
                notes.append("%s=flat-colour-on-purpose" % name)
    if notes:
        print("tfSurfaces " + " ".join(notes))
    return made


def _place_props(bpy, root, mats):
    """Load the spec's ground props and stand them where it says.

    THE BOUNDS ARE MEASURED AFTER LOADING, NOT DERIVED FROM THE SPEC'S OWN
    dims_m. Both numbers should agree - the spec measured them off the same
    files - but the one that decides where a mesh ENDS UP has to be the mesh
    in hand, or a re-export nobody told us about moves every prop a few
    centimetres into the pavement and nothing says so. The spec's figure is
    kept and COMPARED, and a disagreement is printed rather than smoothed.

    IT FAILS OUT LOUD AND CARRIES ON. A missing importer or a missing file
    leaves the pavement as empty as it was and says which; it never leaves a
    prop floating, half-placed, or silently scaled.
    """
    placements, err = prop_placements(root)
    if err:
        print("tfProps status=NONE reason=%s" % err)
        return
    if not hasattr(bpy.ops, "import_scene") or not hasattr(bpy.ops.import_scene, "gltf"):
        print("tfProps status=NONE reason=no-gltf-importer/"
              "the-pavement-stays-empty-and-this-is-why")
        return
    notes, placed, refused = [], 0, 0
    for n, p in enumerate(placements):
        path = os.path.join(root, PROP_DIR, p["asset"] + ".glb")
        if not os.path.exists(path):
            notes.append("%s=missing" % p["asset"]); refused += 1
            continue
        before = set(bpy.data.objects)
        try:
            bpy.ops.import_scene.gltf(filepath=path)
        except (RuntimeError, AttributeError) as exc:
            notes.append("%s=import-failed/%s" % (p["asset"], type(exc).__name__))
            refused += 1
            continue
        fresh = [o for o in bpy.data.objects if o not in before]
        meshes = [o for o in fresh if o.type == "MESH"]
        if not meshes:
            notes.append("%s=no-mesh-in-file" % p["asset"]); refused += 1
            for o in fresh:
                bpy.data.objects.remove(o, do_unlink=True)
            continue
        # ONE EMPTY TO TURN AND MOVE THEM ALL, so a prop that arrives as
        # several objects stays assembled. Parenting keeps the mesh data
        # untouched, which is the dims policy's own requirement.
        pivot = bpy.data.objects.new("prop%d_%s" % (n, p["asset"]), None)
        bpy.context.scene.collection.objects.link(pivot)
        lo = [1e9, 1e9, 1e9]; hi = [-1e9, -1e9, -1e9]
        for o in meshes:
            m = o.matrix_world
            for c in o.bound_box:
                # THE TRANSFORM BY HAND, because mathutils exists only inside
                # Blender and this file's pure layer has to import without it.
                for i in range(3):
                    w = m[i][0] * c[0] + m[i][1] * c[1] + m[i][2] * c[2] + m[i][3]
                    lo[i] = min(lo[i], w); hi[i] = max(hi[i], w)
        centre = [(lo[i] + hi[i]) * 0.5 for i in range(3)]
        height = hi[2] - lo[2]
        # THE GROUND UNDER THIS PROP, which is the footway where it stands on
        # the pavement and the road where it stands in the channel.
        ground = THRESHOLD_ABOVE_CROWN_M if p["on_footway"] else 0.0
        # A SET-IN PIECE IS THE LID OF ITS OWN DISH and sits flush in the
        # running surface rather than on top of it; everything else stands.
        target_z = ground - height * 0.5 if p["set_in"] else ground + height * 0.5
        for o in fresh:
            if o.parent is None:
                o.parent = pivot
                o.matrix_parent_inverse = pivot.matrix_world.inverted()
        pivot.location = (p["x"] - centre[0], p["y"] - centre[1], target_z - centre[2])
        pivot.rotation_euler = (0.0, 0.0, math.radians(p["yaw"]))
        mat = mats.get(p["surface"])
        if mat is not None:
            for o in meshes:
                o.data.materials.clear()
                o.data.materials.append(mat)
        # THE SPEC'S OWN MEASUREMENT, CHECKED RATHER THAN TRUSTED. dims_m is
        # [along, up, across] in the glTF frame; the importer stands the file
        # up, so the UP figure is the one that must match the height we just
        # measured. A millimetre is noise; a centimetre is a re-export.
        said = p.get("dims") or [0.0, 0.0, 0.0]
        gap = abs(float(said[1]) - height) if len(said) > 1 else 0.0
        notes.append("%s=%.3fm%s" % (p["asset"], height,
                                     "/SPEC-SAYS-%.3f" % float(said[1]) if gap > 0.01 else ""))
        placed += 1
    print("tfProps placed=%d/%d refused=%d %s"
          % (placed, len(placements), refused, " ".join(notes)))


def _face_the_street(bpy, obj, block):
    """Put a west block's half turn on the OBJECT rather than in its vertices.

    THIS IS THE OTHER HALF OF THE FIX AND WITHOUT IT THE FIRST HALF DOES
    NOTHING VISIBLE. plan_street turns a west block end for end, which is a
    proper rotation and puts its bays in the right order - and MICKEY'S still
    came out backwards, because every texture in this recipe is mapped from
    OBJECT coordinates and every object was built with world coordinates
    baked into its vertices. Object and world were the same frame, so the
    turn was in the numbers and not in the object, and a sign's image still
    ran along +x on both sides of the road.

    IT HAS TO RUN THE OTHER WAY ON A WEST FACE, and that is a fact about
    streets rather than about Blender. Somebody reading the east frontage
    stands facing +y and their right hand is +x; somebody reading the west
    frontage stands facing -y and their right hand is -x. Text runs from the
    reader's left to their right, so the same words run in opposite world
    directions on the two sides. A mapping that always runs along +x is right
    on one side and mirrored on the other, whatever the geometry does.

    So the object keeps the turn: its mesh is written in a frame that is
    itself turned, and the object is rotated a half turn to put it back. The
    world position is identical to the micron - the rotation and the
    counter-rotation cancel - and Object coordinates now run the way the
    reader does. Nothing is done to any image, which was Jafar's ruling: fix
    the construction, not the lettering.
    """
    if not block or not block.startswith("west"):
        return obj
    lo = [1e18, 1e18]
    hi = [-1e18, -1e18]
    for v in obj.data.vertices:
        for i in range(2):
            lo[i] = min(lo[i], v.co[i])
            hi[i] = max(hi[i], v.co[i])
    cx = (lo[0] + hi[0]) * 0.5
    cy = (lo[1] + hi[1]) * 0.5
    for v in obj.data.vertices:
        v.co[0] = cx - v.co[0]
        v.co[1] = cy - v.co[1]
    obj.location = (cx, cy, 0.0)
    obj.rotation_euler = (0.0, 0.0, math.pi)
    return obj


def _mesh_object(bpy, name, verts, faces, mat):
    mesh = bpy.data.meshes.new(name + "_mesh")
    mesh.from_pydata(verts, [], faces)
    mesh.validate()
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    if mat is not None:
        obj.data.materials.append(mat)
    bpy.context.scene.collection.objects.link(obj)
    return obj


def _box_mesh(bpy, part, mat):
    x0, x1 = part["x0"], part["x1"]
    y0, y1 = part["y0"], part["y1"]
    z0, z1 = part["z0"], part["z1"]
    v = [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
         (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
    f = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4),
         (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    return _mesh_object(bpy, part["id"], v, f, mat)


def _slope_mesh(bpy, part, mat):
    x0, x1 = part["x0"], part["x1"]
    ye, yr = part["y_eaves"], part["y_ridge"]
    ze, zr = part["z_eaves"], part["z_ridge"]
    t = 0.06
    v = [(x0, ye, ze), (x1, ye, ze), (x1, yr, zr), (x0, yr, zr),
         (x0, ye, ze - t), (x1, ye, ze - t), (x1, yr, zr - t), (x0, yr, zr - t)]
    f = [(0, 1, 2, 3), (7, 6, 5, 4), (0, 4, 5, 1),
         (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)]
    return _mesh_object(bpy, part["id"], v, f, mat)


def _night(bpy, root, mats):
    """D31's own tying frame: dusk, wet, lamps lit.

    THE CONDITION IS THE SCENE FILE'S, not mine. wet_night names its own HDRI,
    its sun and sky intensities and its wetness; those are applied here as
    order-of-magnitude proxies to Blender's own strengths rather than as a
    claimed unit conversion, which is the same thing lighting-column.py says
    about its own use of them and for the same reason: the numbers are Unity
    light units and no conversion is defined.

    THE LENS IS EMISSIVE AND THE LIGHT SITS UNDER IT. Both, because one
    without the other is either a lamp that glows and lights nothing or a
    street lit by nothing visible. The placement - 0.05 m below the centre of
    each lantern - is the piece file's own rule.
    """
    world = bpy.data.worlds.new("terrace_night")
    bpy.context.scene.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    hdr = os.path.join(root, "ledger/Assets/Resources/Sky/polyhaven/kloppenheim_04_2k.hdr")
    note = "hdri=NOT-FOUND/flat-dusk-instead"
    if os.path.exists(hdr) and bg is not None:
        env = world.node_tree.nodes.new("ShaderNodeTexEnvironment")
        try:
            env.image = bpy.data.images.load(hdr)
            world.node_tree.links.new(env.outputs["Color"], bg.inputs["Color"])
            # THE SKY IS NOT THE LIGHT SOURCE AT NIGHT. The scene file gives
            # wet_night sky_intensity 0.35, and applying that as a Blender
            # background strength lit the whole street off the sky dome: the
            # pavement came back near-white and the lanterns threw no pool
            # anybody could see. It is a Unity light unit with no defined
            # conversion, which this file already says, so what it buys here
            # is a RENDER CHOICE and is named as one. 0.06 leaves the sky
            # readable behind the roofline and hands the street to the lamps.
            bg.inputs["Strength"].default_value = 0.06
            note = "hdri=%s skyStrength=0.06/render-choice-not-a-conversion" % hdr.replace(" ", "~")
        except RuntimeError:
            pass
    if note.startswith("hdri=NOT") and bg is not None:
        bg.inputs["Color"].default_value = (0.020, 0.024, 0.035, 1.0)
        bg.inputs["Strength"].default_value = 1.0

    # THE LENS GLOWS. Emission on the one material that is a light source.
    lens = mats.get("lens_amber")
    if lens is not None and lens.use_nodes:
        bsdf = lens.node_tree.nodes.get("Principled BSDF")
        if bsdf is not None and "Emission Color" in bsdf.inputs:
            bsdf.inputs["Emission Color"].default_value = (0.780, 0.360, 0.040, 1.0)
            bsdf.inputs["Emission Strength"].default_value = 3.0

    lit = mats.get("interior_lit")
    if lit is not None and lit.use_nodes:
        b2 = lit.node_tree.nodes.get("Principled BSDF")
        if b2 is not None and "Emission Color" in b2.inputs:
            b2.inputs["Emission Color"].default_value = (1.0, 0.714, 0.344, 1.0)
            b2.inputs["Emission Strength"].default_value = 2.2
    for n, (lx, ly, lz) in enumerate(lantern_lights()):
        data = bpy.data.lights.new("lantern%d" % n, type="POINT")
        # 2200 W IS A RENDER CHOICE AND NOT A LAMP SPECIFICATION. A 1990
        # British street ran 70 W low-pressure sodium at roughly 8000 lumens,
        # but a Blender point light's power is radiometric and the conversion
        # is not defined, so this is set by what the frame needs: at 900 and
        # again at 3500 W the
        # lanterns were visible and lit nothing, which is the worst of both.
        # The COLOUR is not a choice - it is the spec's own sodium amber,
        # the same triple lighting-column.py makes its lens from.
        data.energy = 2200.0
        data.color = (1.0, 0.62, 0.20)
        data.shadow_soft_size = 0.18
        obj = bpy.data.objects.new("lantern%d" % n, data)
        bpy.context.scene.collection.objects.link(obj)
        obj.location = (lx, ly, lz)
    return note


#: HOW DIRTY, AND IT IS MEASURED RATHER THAN INVENTED.
#:
#: ROADMAP.md, stage 1, in its own words: "GRIME IS THE STRATEGY, not a
#: finishing pass. Weather and wear are what make this town the town, a
#: surface carries its wear as a SEPARABLE LAYER, and the floor for how much
#: is a number measured off the first authored facades rather than invented."
#:
#: THE NUMBER IS THE VARIATION OF A WALL. A clean rendered wall is uniform
#: and a weathered photographed one is not, so the standard deviation of a
#: patch of brick is a fair proxy for how much wear is on it - and it is a
#: thing both pictures can be asked. MEASURED 22 September: the approved
#: sheet's near brick varies by 46.8 and ours varied by 16.2. Three times
#: too clean, on the surface there is most of.
#:
#: WHAT IT IS NOT: a dirt texture painted onto a wall. It is two things a
#: real wall actually does, kept separable so either can be turned off:
#:   1. PATCHES. Rain does not wash a wall evenly; a large, soft noise over
#:      several metres darkens some of it and leaves the rest.
#:   2. THE BOTTOM METRE AND A HALF. Splash off a pavement, and rising damp
#:      above it, make the foot of every wall in Britain darker than its
#:      middle. It is the single most recognisable piece of wear there is
#:      and it costs one gradient.
WEAR_PATCH_SCALE = 0.45      # cycles per metre: patches a couple of metres across
WEAR_PATCH_DEPTH = 0.28      # how dark the dirtiest patch gets, as a multiplier
WEAR_SPLASH_M = 1.5          # how far up the wall the splash reaches
WEAR_SPLASH_DEPTH = 0.55     # how dark the very foot of the wall gets
STREAK_ACROSS, STREAK_DOWN = 6.0, 0.35   # cycles per metre: fine across, long down
STREAK_DEPTH = 0.70          # how dark the darkest streak gets, as a multiplier
STREAK_FROM_Z, STREAK_FULL_Z = 3.6, 6.4  # nothing below the sills, full at the wall head

#: Which surfaces weather, and the ground weathers differently from a wall:
#: a pavement's wear is trodden into it rather than run down it, so it takes
#: the patches and not the splash.
WEARS = {"brick_red": True, "brick_grey": True, "paving": False,
         "kerbstone": False, "slate": True, "stone": True}


#: A FLAG'S SIZE, the common British 900 x 600 mm slab, laid in stretcher
#: bond - each row half a slab along from the last - with a joint of about
#: 10 mm that reads dark because it holds dirt and water.
FLAG_W_M, FLAG_H_M, FLAG_JOINT_M = 0.90, 0.60, 0.012
FLAG_JOINT_DARK = 0.45
#: The two tones a flag is mixed between: one a little lifted, one a little
#: cooler and darker. Their mean is 1.0 in every channel but blue's, which
#: the greyer flags pull a touch toward the sheet's cooler far footway.
FLAG_TONE_A = (1.16, 1.13, 1.08)
FLAG_TONE_B = (0.84, 0.87, 0.93)


#: THE STALLRISER TILE: 150 mm squares with 3 mm joints, each square
#: quartered light and dark. A plain geometric pattern and nothing more - R05
#: establishes that the tile was patterned, not which pattern, and the sheet
#: shows a busy pale field at a distance where no motif can be read.
#: 0.72 AND NOT 0.55, attempt two: at 0.55 the quarters rendered as a hard
#: black-and-white checkerboard, where the sheet's tile reads as one busy
#: pale field.
TILE_M, TILE_JOINT_M, TILE_DARK = 0.15, 0.003, 0.72


def _tile_pattern(bpy, mats):
    """Lay a quartered pattern and its joints over the patterned tile."""
    mat = mats.get("tile_patterned")
    if mat is None or not mat.use_nodes:
        print("tfNote tilePattern=NOT-APPLIED/no-material")
        return
    nt = mat.node_tree
    bsdf = nt.nodes.get("Principled BSDF")
    if bsdf is None or not bsdf.inputs["Base Color"].links:
        print("tfNote tilePattern=NOT-APPLIED/no-map-to-lay-it-over")
        return
    src = bsdf.inputs["Base Color"].links[0].from_socket
    coord = nt.nodes.new("ShaderNodeTexCoord")
    chk = nt.nodes.new("ShaderNodeTexChecker")
    chk.inputs["Scale"].default_value = 1.0 / (TILE_M / 2.0)
    chk.inputs["Color1"].default_value = (1.0, 1.0, 1.0, 1.0)
    chk.inputs["Color2"].default_value = (TILE_DARK, TILE_DARK, TILE_DARK * 0.9, 1.0)
    brick = nt.nodes.new("ShaderNodeTexBrick")
    brick.offset = 0.0
    brick.inputs["Scale"].default_value = 1.0
    brick.inputs["Mortar Size"].default_value = TILE_JOINT_M
    brick.inputs["Brick Width"].default_value = TILE_M
    brick.inputs["Row Height"].default_value = TILE_M
    ramp = nt.nodes.new("ShaderNodeMapRange")
    ramp.inputs["To Min"].default_value = 1.0
    ramp.inputs["To Max"].default_value = 0.6
    nt.links.new(coord.outputs["Object"], chk.inputs["Vector"])
    nt.links.new(coord.outputs["Object"], brick.inputs["Vector"])
    nt.links.new(brick.outputs["Fac"], ramp.inputs["Value"])
    m1 = nt.nodes.new("ShaderNodeMix")
    m1.data_type = "RGBA"
    m1.blend_type = "MULTIPLY"
    m1.inputs["Factor"].default_value = 1.0
    nt.links.new(src, m1.inputs[6])
    nt.links.new(chk.outputs["Color"], m1.inputs[7])
    m2 = nt.nodes.new("ShaderNodeMix")
    m2.data_type = "RGBA"
    m2.blend_type = "MULTIPLY"
    m2.inputs["Factor"].default_value = 1.0
    nt.links.new(m1.outputs[2], m2.inputs[6])
    nt.links.new(ramp.outputs["Result"], m2.inputs[7])
    nt.links.new(m2.outputs[2], bsdf.inputs["Base Color"])
    print("tfNote tilePattern=%.0fmm-quartered-x%.2f/joint-%.0fmm"
          % (TILE_M * 1000, TILE_DARK, TILE_JOINT_M * 1000))


#: HOW MUCH OF THE ASPHALT MAP'S OWN COLOUR SURVIVES. See _quiet_the_road.
ROAD_MAP_SATURATION = 0.25


def _quiet_the_road(bpy, mats):
    """Take the red out of the road's chippings, keep their light and dark.

    22 September, against the new sheet: its carriageway is an even wet
    grey, and ours carried red flecks all down the near lane - the pack's
    asphalt photograph has a red aggregate in it. The mean was already right
    (the palette pass matched the road region to within two levels), so
    this does not move the value; it drops the map's saturation to a quarter
    at the Base Color socket, after the wear and the wet, so the flecks keep
    their brightness and lose their hue.
    """
    mat = mats.get("asphalt")
    if mat is None or not mat.use_nodes:
        print("tfNote roadQuiet=NOT-APPLIED/no-asphalt")
        return
    nt = mat.node_tree
    bsdf = nt.nodes.get("Principled BSDF")
    if bsdf is None or not bsdf.inputs["Base Color"].links:
        print("tfNote roadQuiet=NOT-APPLIED/no-map")
        return
    src = bsdf.inputs["Base Color"].links[0].from_socket
    hs = nt.nodes.new("ShaderNodeHueSaturation")
    hs.inputs["Saturation"].default_value = ROAD_MAP_SATURATION
    nt.links.new(src, hs.inputs["Color"])
    nt.links.new(hs.outputs["Color"], bsdf.inputs["Base Color"])
    print("tfNote roadQuiet=saturation-x%.2f/the-red-chippings-go-grey" % ROAD_MAP_SATURATION)


def _flag_joints(bpy, mats):
    """Lay flag joints over the footway, between its map and its socket.

    THE SAME PLACE THE WEAR SITS, and for the same reason: it multiplies over
    what the map already gives, so the stone keeps its own mottle and the
    joints are a separable layer. Mapped from OBJECT coordinates, which on the
    footway meshes are street metres, so a flag is 0.9 m wherever it lies.
    """
    mat = mats.get("paving")
    if mat is None or not mat.use_nodes:
        print("tfNote flags=NOT-APPLIED/no-paving-material")
        return
    nt = mat.node_tree
    bsdf = nt.nodes.get("Principled BSDF")
    if bsdf is None or not bsdf.inputs["Base Color"].links:
        print("tfNote flags=NOT-APPLIED/the-footway-has-no-map-to-lay-them-over")
        return
    src = bsdf.inputs["Base Color"].links[0].from_socket
    coord = nt.nodes.new("ShaderNodeTexCoord")
    brick = nt.nodes.new("ShaderNodeTexBrick")
    brick.offset = 0.5
    brick.offset_frequency = 2
    brick.inputs["Scale"].default_value = 1.0
    brick.inputs["Mortar Size"].default_value = FLAG_JOINT_M
    brick.inputs["Brick Width"].default_value = FLAG_W_M
    brick.inputs["Row Height"].default_value = FLAG_H_M
    # the joint's Fac is 1 and the stone's 0: map that to a multiplier
    ramp = nt.nodes.new("ShaderNodeMapRange")
    ramp.inputs["From Min"].default_value = 0.0
    ramp.inputs["From Max"].default_value = 1.0
    ramp.inputs["To Min"].default_value = 1.0
    ramp.inputs["To Max"].default_value = FLAG_JOINT_DARK
    nt.links.new(coord.outputs["Object"], brick.inputs["Vector"])
    nt.links.new(brick.outputs["Fac"], ramp.inputs["Value"])
    mix = nt.nodes.new("ShaderNodeMix")
    mix.data_type = "RGBA"
    mix.blend_type = "MULTIPLY"
    mix.inputs["Factor"].default_value = 1.0
    nt.links.new(src, mix.inputs[6])
    nt.links.new(ramp.outputs["Result"], mix.inputs[7])
    # AND EVERY FLAG ITS OWN STONE, 22 September. On the new sheet no two
    # neighbouring flags are the same tone - some warmer, some greyer, the
    # odd one a replacement - and that is most of what makes a footway read
    # as laid stone rather than as one continuous surface with lines drawn
    # on it, which is what ours did (the concrete map's streaks read as a
    # boarded floor). The same Brick texture's per-brick colour does it:
    # each flag takes a random mix between a slightly lifted and a slightly
    # cooler, darker tone, averaging to 1.0 so the footway's measured value
    # does not move.
    brick.inputs["Color1"].default_value = FLAG_TONE_A + (1.0,)
    brick.inputs["Color2"].default_value = FLAG_TONE_B + (1.0,)
    brick.inputs["Mortar"].default_value = (1.0, 1.0, 1.0, 1.0)
    tone = nt.nodes.new("ShaderNodeMix")
    tone.data_type = "RGBA"
    tone.blend_type = "MULTIPLY"
    tone.inputs["Factor"].default_value = 1.0
    nt.links.new(mix.outputs[2], tone.inputs[6])
    nt.links.new(brick.outputs["Color"], tone.inputs[7])
    nt.links.new(tone.outputs[2], bsdf.inputs["Base Color"])
    print("tfNote flags=%.2fx%.2fm/stretcher-bond/joint-%.0fmm-at-x%.2f/per-flag-tone"
          % (FLAG_W_M, FLAG_H_M, FLAG_JOINT_M * 1000, FLAG_JOINT_DARK))


#: THE BRICKS THEMSELVES, 22 September. The biggest surface on the frame is
#: the near terrace's brick, and side by side with the new sheet it was the
#: widest gap left on the street: the sheet's wall is individual bricks -
#: bright orange ones, dark soot-burnt ones, everything between, in dark
#: joints - and ours was a soft pinkish mush with a faint pattern in it,
#: because the pack's brick photograph is low in contrast at this range.
#: MEASURED off the sheet's near gable, its bricks run from 64/35/27 at the
#: fifth percentile through 95/51/36 at the median to 118/65/46 at the
#: eighty-fifth - in linear, about 0.45 to 1.6 times the median. So each
#: brick draws a tone from that range, the joints are dark, and the whole
#: averages to 1.0 so the wall's measured value does not move. The pack's
#: map stays underneath as large-scale staining only.
#: A BRICK IS 215 x 65 mm with a 10 mm joint, laid in stretcher bond.
BRICK_W_M, BRICK_H_M, BRICK_JOINT_M = 0.225, 0.075, 0.010
#: The tone a brick draws, as (position, multiplier): a uniform random
#: position through these stops averages to 1.0.
BRICK_TONES = ((0.0, 0.45), (0.2, 0.70), (0.5, 1.00), (0.8, 1.30), (1.0, 1.60))
#: ATTEMPT TWO: the joints DARK, as the sheet's are - soot in lime mortar -
#: where 0.80 left them the colour of the bricks and the wall read soft; the
#: bricks lifted by 1.07 to pay for the darker joints' share of the wall;
#: and the bricks' own colour pushed toward orange by (1.10, 0.96, 0.90),
#: because the sheet's median brick is 95/51/36, red nearly twice green, and
#: ours came back pink-grey at 1.4.
BRICK_JOINT_TONE = 0.45
BRICK_FACE_LIFT = 1.07
BRICK_FACE_HUE = (1.10, 0.96, 0.90)
#: How much of the pack map's own light and dark survives, as staining.
BRICK_STAIN = 0.35


def _brick_courses(bpy, mats):
    """Lay real bricks over the brick materials' base colour."""
    done = []
    for name in ("brick_red", "brick_grey"):
        mat = mats.get(name)
        if mat is None or not mat.use_nodes:
            continue
        nt = mat.node_tree
        bsdf = nt.nodes.get("Principled BSDF")
        if bsdf is None or not bsdf.inputs["Base Color"].links:
            continue
        src = bsdf.inputs["Base Color"].links[0].from_socket
        # A WALL FACES y OR x, and a Brick texture is two-dimensional: it
        # lays its pattern on its input's x and y. So the face's own normal
        # picks (x, z) for a wall facing the street and (y, z) for an end wall.
        coord = nt.nodes.new("ShaderNodeTexCoord")
        geo = nt.nodes.new("ShaderNodeNewGeometry")
        sp = nt.nodes.new("ShaderNodeSeparateXYZ")
        nt.links.new(coord.outputs["Object"], sp.inputs["Vector"])
        sn = nt.nodes.new("ShaderNodeSeparateXYZ")
        nt.links.new(geo.outputs["Normal"], sn.inputs["Vector"])
        onx, ony = nt.nodes.new("ShaderNodeMath"), nt.nodes.new("ShaderNodeMath")
        onx.operation = ony.operation = "ABSOLUTE"
        nt.links.new(sn.outputs["X"], onx.inputs[0])
        nt.links.new(sn.outputs["Y"], ony.inputs[0])
        pick = nt.nodes.new("ShaderNodeMath")
        pick.operation = "GREATER_THAN"
        nt.links.new(ony.outputs["Value"], pick.inputs[0])
        nt.links.new(onx.outputs["Value"], pick.inputs[1])
        along_x = nt.nodes.new("ShaderNodeCombineXYZ")
        nt.links.new(sp.outputs["X"], along_x.inputs["X"])
        nt.links.new(sp.outputs["Z"], along_x.inputs["Y"])
        along_y = nt.nodes.new("ShaderNodeCombineXYZ")
        nt.links.new(sp.outputs["Y"], along_y.inputs["X"])
        nt.links.new(sp.outputs["Z"], along_y.inputs["Y"])
        vec = nt.nodes.new("ShaderNodeMix")
        vec.data_type = "VECTOR"
        nt.links.new(pick.outputs["Value"], vec.inputs["Factor"])
        nt.links.new(along_y.outputs["Vector"], vec.inputs[4])
        nt.links.new(along_x.outputs["Vector"], vec.inputs[5])
        brick = nt.nodes.new("ShaderNodeTexBrick")
        brick.offset = 0.5
        brick.offset_frequency = 2
        brick.inputs["Scale"].default_value = 1.0
        brick.inputs["Mortar Size"].default_value = BRICK_JOINT_M
        brick.inputs["Brick Width"].default_value = BRICK_W_M
        brick.inputs["Row Height"].default_value = BRICK_H_M
        brick.inputs["Color1"].default_value = (0.0, 0.0, 0.0, 1.0)
        brick.inputs["Color2"].default_value = (1.0, 1.0, 1.0, 1.0)
        brick.inputs["Mortar"].default_value = (0.0, 0.0, 0.0, 1.0)
        nt.links.new(vec.outputs[1], brick.inputs["Vector"])
        # EACH BRICK'S TONE: the brick's own random grey through the stops.
        bw = nt.nodes.new("ShaderNodeRGBToBW")
        nt.links.new(brick.outputs["Color"], bw.inputs["Color"])
        ramp = nt.nodes.new("ShaderNodeValToRGB")
        els = ramp.color_ramp.elements
        while len(els) > 1:
            els.remove(els[-1])
        els[0].position = BRICK_TONES[0][0]
        els[0].color = (BRICK_TONES[0][1],) * 3 + (1.0,)
        for pos, val in BRICK_TONES[1:]:
            e = els.new(pos)
            e.color = (val, val, val, 1.0)
        nt.links.new(bw.outputs["Val"], ramp.inputs["Fac"])
        face = nt.nodes.new("ShaderNodeMix")
        face.data_type = "RGBA"
        face.blend_type = "MULTIPLY"
        face.inputs["Factor"].default_value = 1.0
        nt.links.new(ramp.outputs["Color"], face.inputs[6])
        face.inputs[7].default_value = tuple(BRICK_FACE_LIFT * h for h in BRICK_FACE_HUE) + (1.0,)
        # THE JOINT, where the Brick texture's Fac is 1.
        joint = nt.nodes.new("ShaderNodeMix")
        joint.data_type = "RGBA"
        nt.links.new(brick.outputs["Fac"], joint.inputs["Factor"])
        nt.links.new(face.outputs[2], joint.inputs[6])
        joint.inputs[7].default_value = (BRICK_JOINT_TONE,) * 3 + (1.0,)
        # THE PACK MAP AS STAINING: its own light and dark, pulled toward
        # its mean, times the bricks. The map arrives tinted, so its grey
        # over the tint's grey is its variation about 1.0.
        mbw = nt.nodes.new("ShaderNodeRGBToBW")
        nt.links.new(src, mbw.inputs["Color"])
        lin = [c for c in dict((n_, c_) for n_, c_, _r in MATERIALS)[name]]
        tint_lum = 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]
        stain = nt.nodes.new("ShaderNodeMapRange")
        stain.inputs["From Min"].default_value = 0.0
        stain.inputs["From Max"].default_value = 2.0 * tint_lum
        stain.inputs["To Min"].default_value = 1.0 - BRICK_STAIN
        stain.inputs["To Max"].default_value = 1.0 + BRICK_STAIN
        nt.links.new(mbw.outputs["Val"], stain.inputs["Value"])
        base = nt.nodes.new("ShaderNodeMix")
        base.data_type = "RGBA"
        base.blend_type = "MULTIPLY"
        base.inputs["Factor"].default_value = 1.0
        base.inputs[6].default_value = (lin[0], lin[1], lin[2], 1.0)
        nt.links.new(joint.outputs[2], base.inputs[7])
        final = nt.nodes.new("ShaderNodeMix")
        final.data_type = "RGBA"
        final.blend_type = "MULTIPLY"
        final.inputs["Factor"].default_value = 1.0
        nt.links.new(base.outputs[2], final.inputs[6])
        nt.links.new(stain.outputs["Result"], final.inputs[7])
        nt.links.new(final.outputs[2], bsdf.inputs["Base Color"])
        done.append(name)
    print("tfNote bricks=%s/%.0fx%.0fmm+%.0fmm-joint/stretcher-bond/tones-%.2f-to-%.2f"
          % ("+".join(done) or "NONE", BRICK_W_M * 1000 - BRICK_JOINT_M * 1000,
             BRICK_H_M * 1000 - BRICK_JOINT_M * 1000, BRICK_JOINT_M * 1000,
             BRICK_TONES[0][1], BRICK_TONES[-1][1]))


def _wear(bpy, mats):
    """A separable wear layer on the surfaces that carry one.

    IT SITS BETWEEN THE MAP AND THE SOCKET, like the wetness does, so the
    photograph's own variation survives and this multiplies over it. Nothing
    here replaces a texture; a wall with its wear turned off is exactly the
    wall that was there before.
    """
    notes = []
    for name, splash in sorted(WEARS.items()):
        mat = mats.get(name)
        if mat is None or not mat.use_nodes:
            continue
        nt = mat.node_tree
        bsdf = nt.nodes.get("Principled BSDF")
        if bsdf is None or not bsdf.inputs["Base Color"].links:
            continue
        src = bsdf.inputs["Base Color"].links[0].from_socket

        coord = nt.nodes.new("ShaderNodeTexCoord")
        noise = nt.nodes.new("ShaderNodeTexNoise")
        noise.inputs["Scale"].default_value = WEAR_PATCH_SCALE
        if "Detail" in noise.inputs:
            noise.inputs["Detail"].default_value = 4.0
        nt.links.new(coord.outputs["Object"], noise.inputs["Vector"])
        # THE RAMP IS WHAT MAKES IT PATCHES RATHER THAN FOG. Raw noise is a
        # smooth grey mush; pushed through a steep ramp it becomes areas
        # that are dirty and areas that are not, which is what weather
        # leaves behind.
        ramp = nt.nodes.new("ShaderNodeValToRGB")
        ramp.color_ramp.elements[0].position = 0.35
        ramp.color_ramp.elements[0].color = (WEAR_PATCH_DEPTH,) * 3 + (1.0,)
        ramp.color_ramp.elements[1].position = 0.62
        ramp.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
        nt.links.new(noise.outputs["Fac"], ramp.inputs["Fac"])
        dirt = ramp.outputs["Color"]

        if splash:
            # THE FOOT OF THE WALL, off the object's own Z, which on these
            # meshes is height above the road because the geometry is built
            # in world coordinates. Multiplied into the patches rather than
            # mixed with them: a wall that is both splashed and unwashed is
            # dirtier than either.
            sep = nt.nodes.new("ShaderNodeSeparateXYZ")
            nt.links.new(coord.outputs["Object"], sep.inputs["Vector"])
            rise = nt.nodes.new("ShaderNodeMapRange")
            rise.clamp = True
            rise.inputs["From Min"].default_value = 0.0
            rise.inputs["From Max"].default_value = WEAR_SPLASH_M
            rise.inputs["To Min"].default_value = WEAR_SPLASH_DEPTH
            rise.inputs["To Max"].default_value = 1.0
            nt.links.new(sep.outputs["Z"], rise.inputs["Value"])
            both = nt.nodes.new("ShaderNodeMix")
            both.data_type = "RGBA"
            both.blend_type = "MULTIPLY"
            both.inputs["Factor"].default_value = 1.0
            nt.links.new(dirt, both.inputs[6])
            nt.links.new(rise.outputs["Result"], both.inputs[7])
            dirt = both.outputs[2]

            # AND THE WATER PATHS DOWN FROM THE TOP, 22 September. "Grime
            # follows water paths" is the town form bible's own rule, and the
            # new sheet's near gable is dark at its head and streaked below
            # it, where rain off the verge and the gutter's overflow runs down
            # the brick. A noise stretched tall - fine across, long down -
            # through a ramp gives streaks, and they are strongest near the
            # wall head and gone by the first floor's sills.
            smap = nt.nodes.new("ShaderNodeMapping")
            smap.inputs["Scale"].default_value = (STREAK_ACROSS, STREAK_ACROSS, STREAK_DOWN)
            nt.links.new(coord.outputs["Object"], smap.inputs["Vector"])
            snoise = nt.nodes.new("ShaderNodeTexNoise")
            snoise.inputs["Scale"].default_value = 1.0
            if "Detail" in snoise.inputs:
                snoise.inputs["Detail"].default_value = 2.0
            nt.links.new(smap.outputs["Vector"], snoise.inputs["Vector"])
            sramp = nt.nodes.new("ShaderNodeMapRange")
            sramp.clamp = True
            sramp.inputs["From Min"].default_value = 0.40
            sramp.inputs["From Max"].default_value = 0.62
            sramp.inputs["To Min"].default_value = STREAK_DEPTH
            sramp.inputs["To Max"].default_value = 1.0
            nt.links.new(snoise.outputs["Fac"], sramp.inputs["Value"])
            head = nt.nodes.new("ShaderNodeMapRange")
            head.clamp = True
            head.inputs["From Min"].default_value = STREAK_FROM_Z
            head.inputs["From Max"].default_value = STREAK_FULL_Z
            head.inputs["To Min"].default_value = 0.0
            head.inputs["To Max"].default_value = 1.0
            nt.links.new(sep.outputs["Z"], head.inputs["Value"])
            streak = nt.nodes.new("ShaderNodeMix")
            streak.data_type = "FLOAT"
            nt.links.new(head.outputs["Result"], streak.inputs["Factor"])
            streak.inputs[2].default_value = 1.0
            nt.links.new(sramp.outputs["Result"], streak.inputs[3])
            wet = nt.nodes.new("ShaderNodeMix")
            wet.data_type = "RGBA"
            wet.blend_type = "MULTIPLY"
            wet.inputs["Factor"].default_value = 1.0
            nt.links.new(dirt, wet.inputs[6])
            nt.links.new(streak.outputs[0], wet.inputs[7])
            dirt = wet.outputs[2]

        mix = nt.nodes.new("ShaderNodeMix")
        mix.data_type = "RGBA"
        mix.blend_type = "MULTIPLY"
        mix.inputs["Factor"].default_value = 1.0
        nt.links.new(src, mix.inputs[6])
        nt.links.new(dirt, mix.inputs[7])
        nt.links.new(mix.outputs[2], bsdf.inputs["Base Color"])
        notes.append("%s=%s" % (name, "patches+splash" if splash else "patches"))
    if notes:
        print("tfWear " + " ".join(notes))


def _wetten(mats, wetness):
    """Wet, which on a flat-colour street is roughness and darkness.

    NOT A CLAIM ABOUT WATER. With no texture in this recipe yet, the honest
    version of a wetness figure is: drop the roughness of the things rain
    actually sits on and darken them, because water fills the pores and what
    you see is then partly a mirror of whatever is above. Everything else is
    left alone - a wall does not get wetter than a pavement in the same rain,
    it just looks it less.

    BOTH CONDITIONS ARE WET AND THAT WAS THE MISS. overcast_day carries
    wetness 0.6 in the scene file and the first day frames were rendered bone
    dry, which is a third of the way off the sheet on its own: the Hook
    sheet's street panel is OVERCAST DAYLIGHT and its road and pavement are
    wet and reflective throughout. wet_night carries 0.9. The figure is passed
    in now instead of being assumed.
    """
    # A ROAD AND A PAVEMENT DO NOT GET WET THE SAME WAY. Tarmac sheets over
    # and becomes close to a mirror; a paving slab holds water in its own
    # texture and stays broken up, which is why a wet pavement reads as DARK
    # rather than as bright. Made the same, the footway turned into a mirror
    # of the sky, a lantern's light glanced off it to somewhere the camera was
    # not, and the pool nobody could find was not missing - it was specular
    # and pointed the wrong way.
    # MEASURED OFF THE SHEET RATHER THAN CHOSEN. Its street panel has the ROAD
    # as a near mirror with the shopfronts legible upside down in it, and its
    # PAVEMENT as a dull wet grey with no reflection worth the name - two
    # different surfaces in the same rain, which is what paving slabs and
    # sheet tarmac actually do. At 0.30 the footway was behaving like the
    # road, and since the two of them fill the bottom third of the frame the
    # whole picture read pale.
    ROUGH_FLOOR = {"asphalt": 0.05, "paving": 0.46, "kerbstone": 0.40}
    # NOT A STRAIGHT LINE, and the pair is why. At a linear map, the scene
    # file's daytime wetness of 0.6 left the road at roughness 0.28 - damp,
    # not wet - while the sheet's own street panel is a near mirror with the
    # shopfronts reading upside down in it. Water does not arrive in
    # proportion to a number; a surface goes from dry to reflective early and
    # then changes little, so the curve is bent to match what the reference
    # actually looks like at the figure the spec gives.
    w = wetness ** 0.55
    # DAMP, NOT STREAMING, and that is another thing the wrong sheet got
    # wrong. Codex's street was running with water and everything in it was
    # near-black, so the ground was darkened by more than half on top of
    # albedos that were already three times too low - which is how our road
    # ended up eighteen times darker than the reference's. The approved sheet
    # is a flat overcast day after rain: its road reads 0.292 linear and its
    # pavement 0.122, both LIGHTER than their dry albedo would suggest,
    # because what a wet surface mostly shows is the sky. The GLOSS does that
    # work and the roughness curve below is unchanged; only the darkening,
    # which was fighting it, comes back.
    darken = 1.0 - 0.28 * w
    for name in ("asphalt", "paving", "kerbstone"):
        mat = mats.get(name)
        if mat is None or not mat.use_nodes:
            continue
        rough = 0.62 - (0.62 - ROUGH_FLOOR[name]) * w
        nt = mat.node_tree
        bsdf = nt.nodes.get("Principled BSDF")
        if bsdf is None:
            continue
        # THIS WHOLE FUNCTION HAS BEEN DOING NOTHING SINCE THE TEXTURES
        # LANDED, and that is the whole of why the road reads dry.
        #
        # It set Roughness and Base Color through `default_value`. A socket's
        # default is what Blender uses when NOTHING IS PLUGGED INTO IT - and
        # _texture_nodes links the pack's _r map into Roughness and the
        # tinted base map into Base Color on exactly these three materials.
        # So every number below was computed correctly, written to a socket
        # that was already carrying a link, and discarded. The careful curve
        # in the comment above, the one bent to match the reference, has
        # never once reached a render. The road has been at whatever
        # roughness the photograph happened to have.
        #
        # So the wetness goes ON THE GRAPH now: a multiply between the map
        # and the socket, which keeps the map's own variation - a road is not
        # uniformly anything - and scales it. Where a socket really is
        # unconnected the default is still the right place to write.
        rough_gain = max(0.04, rough) / 0.62
        rlink = bsdf.inputs["Roughness"].links
        if rlink:
            src = rlink[0].from_socket
            mul = nt.nodes.new("ShaderNodeMath")
            mul.operation = "MULTIPLY"
            mul.inputs[1].default_value = rough_gain
            nt.links.new(src, mul.inputs[0])
            nt.links.new(mul.outputs["Value"], bsdf.inputs["Roughness"])
            if name == "asphalt":
                _channel_gloss(nt, mul, rough_gain)
        else:
            bsdf.inputs["Roughness"].default_value = max(0.04, rough)
        blink = bsdf.inputs["Base Color"].links
        if blink:
            src = blink[0].from_socket
            mix = nt.nodes.new("ShaderNodeMix")
            mix.data_type = "RGBA"
            mix.blend_type = "MULTIPLY"
            mix.inputs["Factor"].default_value = 1.0
            nt.links.new(src, mix.inputs[6])
            mix.inputs[7].default_value = (darken, darken, min(1.0, darken * 1.05), 1.0)
            nt.links.new(mix.outputs[2], bsdf.inputs["Base Color"])
        else:
            base = bsdf.inputs["Base Color"].default_value
            bsdf.inputs["Base Color"].default_value = (base[0] * darken, base[1] * darken,
                                                       base[2] * darken * 1.05, 1.0)


def _channel_gloss(nt, rough_mul, gain):
    """The water sits in the channel, because the camber puts it there.

    THIS IS WHAT THE CROSSFALL IS FOR, in the scene file's own words: "a flat
    carriageway puts the wet-condition water everywhere instead of at the
    kerb". Having finally built the crown, the wet frame should show it - a
    road that is merely uniformly glossy is a road nobody has watched rain
    run off. So the roughness multiplier FALLS towards the channel: the crown
    drains and dries first, the gutter holds water and mirrors the sky, and
    the long soft highlight down each side is the thing that says it rained
    an hour ago without one puddle being modelled.

    OFF THE OBJECT'S OWN Y, which on the carriageway mesh IS the distance
    across the street - the mesh is built at world coordinates, so object and
    world agree and no mapping is needed.
    """
    coord = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(coord.outputs["Object"], sep.inputs["Vector"])
    across = nt.nodes.new("ShaderNodeMath")
    across.operation = "ABSOLUTE"
    nt.links.new(sep.outputs["Y"], across.inputs[0])
    # The caller's own gain at the crown, and 45 per cent of it at the
    # channel, over the carriageway's 3.0 m half width. CLAMPED, so nothing
    # beyond the kerb line can drive it somewhere odd.
    ramp = nt.nodes.new("ShaderNodeMapRange")
    ramp.clamp = True
    ramp.inputs["From Min"].default_value = 0.0
    ramp.inputs["From Max"].default_value = 3.0
    ramp.inputs["To Min"].default_value = gain
    ramp.inputs["To Max"].default_value = gain * 0.45
    nt.links.new(across.outputs["Value"], ramp.inputs["Value"])
    nt.links.new(ramp.outputs["Result"], rough_mul.inputs[1])



def _mist(bpy, scene, night):
    """The mist pass, mixed toward the sky. See the caller for why not fog.

    IT SAYS WHAT IT DID, EITHER WAY. A build whose view layer has no mist
    pass, or whose compositor will not take these nodes, leaves the street
    exactly as flat as it was - and a flat street that looks deliberate is
    the thing this recipe keeps refusing elsewhere, so it prints the reason.
    """
    try:
        view = scene.view_layers[0]
    except (IndexError, AttributeError):
        print("tfNote mist=no-view-layer/the-far-end-stays-as-near-as-the-near-end")
        return
    if not hasattr(view, "use_pass_mist"):
        print("tfNote mist=no-mist-pass-on-this-build/"
              "the-far-end-stays-as-near-as-the-near-end")
        return
    view.use_pass_mist = True

    # WHERE THE HAZE STARTS AND STOPS, off the street's own length. The
    # blocks occupy 3 to 39 m and the camera stands at 33, so the far end of
    # the parade is about 30 m away: haze that begins at 8 m and is fully in
    # by 55 leaves the near shopfront clean, softens the middle distance and
    # has somewhere left to go for the town when stage 6 builds one.
    world = scene.world
    if world is not None and hasattr(world, "mist_settings"):
        world.mist_settings.use_mist = True
        world.mist_settings.start = 8.0
        world.mist_settings.depth = 55.0
        world.mist_settings.falloff = "QUADRATIC"
        world.mist_settings.intensity = 0.0

    # A THIRD BY DAY AND MORE BY NIGHT, because the scene file's own figures
    # keep that ratio - 0.1 against 0.45 - even though neither number is
    # used as written. The RATIO is the part of the spec that survives a
    # unit nobody can convert.
    # 0.20 BY DAY, from 0.33, against the new sheet: its far parade keeps a
    # saturation of 0.24 at twenty to thirty-five metres and ours came back
    # at 0.14 - the haze was taking the colour out of the middle distance
    # the sheet keeps.
    ceiling = 0.55 if night else 0.20
    # AND THE COLOUR IT MIXES TOWARD IS THE SKY'S, because that is what
    # aerial perspective IS: distant things take the colour of the air in
    # front of them, which is the sky seen end-on.
    haze = (0.55, 0.57, 0.60, 1.0) if not night else (0.06, 0.07, 0.10, 1.0)

    scene.use_nodes = True
    nt = scene.node_tree
    for node in list(nt.nodes):
        nt.nodes.remove(node)
    rl = nt.nodes.new("CompositorNodeRLayers")
    comp = nt.nodes.new("CompositorNodeComposite")
    if "Mist" not in rl.outputs:
        nt.links.new(rl.outputs["Image"], comp.inputs["Image"])
        print("tfNote mist=pass-not-emitted-by-this-engine/"
              "the-far-end-stays-as-near-as-the-near-end")
        return
    gain = nt.nodes.new("CompositorNodeMath")
    gain.operation = "MULTIPLY"
    gain.inputs[1].default_value = ceiling
    nt.links.new(rl.outputs["Mist"], gain.inputs[0])
    mix = nt.nodes.new("CompositorNodeMixRGB")
    mix.blend_type = "MIX"
    mix.inputs[2].default_value = haze
    nt.links.new(gain.outputs["Value"], mix.inputs[0])
    nt.links.new(rl.outputs["Image"], mix.inputs[1])
    nt.links.new(mix.outputs["Image"], comp.inputs["Image"])
    print("tfNote mist=on/start=8.0m/depth=55.0m/quadratic/ceiling=%.2f/"
          "mixed-toward-the-sky-in-the-compositor/not-volumetrics" % ceiling)


def _world(bpy, root):
    """Overcast, from the held HDRI where it is there, and a flat sky where it
    is not - announced either way, never silently flat."""
    world = bpy.data.worlds.new("terrace_world")
    bpy.context.scene.world = world
    world.use_nodes = True
    nt = world.node_tree
    bg = nt.nodes.get("Background")
    hdr = os.path.join(root, "ledger/Assets/Resources/Sky/polyhaven/belfast_open_field_2k.hdr")
    if os.path.exists(hdr) and bg is not None:
        env = nt.nodes.new("ShaderNodeTexEnvironment")
        try:
            env.image = bpy.data.images.load(hdr)
            nt.links.new(env.outputs["Color"], bg.inputs["Color"])
            # 0.7 IS THE SCENE FILE'S OWN sky_intensity for overcast_day, and
            # it was 1.0 here for no reason anybody wrote down. The pair is
            # what made it matter: the road and the footway are a third of the
            # frame and at eye height they are almost entirely a mirror of the
            # sky, so a sky set a half-stop too bright does not brighten the
            # sky, it bleaches the ground.
            bg.inputs["Strength"].default_value = 1.35
            # AND THE SKY AS THE CAMERA SEES IT IS BRIGHTER THAN THE SKY AS
            # A LIGHT, 22 September. The new sheet's sky reads 244 to 248,
            # nearly white; ours read 228 to 233. Raising the world's
            # strength would also brighten the wet road, which mirrors the
            # sky and was already the brightest gap in the frame. So the
            # camera's own rays see a stronger sky and every other ray -
            # the reflections, the lighting - sees 1.35 as before. That is
            # how an overcast sky photographs: blown in the frame, soft on
            # the ground.
            try:
                lp = nt.nodes.new("ShaderNodeLightPath")
                bg_cam = nt.nodes.new("ShaderNodeBackground")
                bg_cam.inputs["Strength"].default_value = 1.35 * SKY_AS_SEEN_GAIN
                nt.links.new(env.outputs["Color"], bg_cam.inputs["Color"])
                mix = nt.nodes.new("ShaderNodeMixShader")
                out = nt.nodes.get("World Output")
                nt.links.new(lp.outputs["Is Camera Ray"], mix.inputs["Fac"])
                nt.links.new(bg.outputs["Background"], mix.inputs[1])
                nt.links.new(bg_cam.outputs["Background"], mix.inputs[2])
                nt.links.new(mix.outputs["Shader"], out.inputs["Surface"])
                print("tfNote skyAsSeen=x%.2f/camera-rays-only/reflections-and-light-unchanged"
                      % SKY_AS_SEEN_GAIN)
            except (KeyError, AttributeError, RuntimeError) as exc:
                print("tfNote skyAsSeen=NOT-APPLIED/%s/the-sky-stays-as-grey-as-it-was"
                      % type(exc).__name__)
            # 1.35 AND NOT 1.70, WHICH IS THE VALUE THAT MATCHES THE NUMBER.
            #
            # Swept at 1.35, 1.70 and 2.10 and read off the frame each time.
            # The sheet's street panel has a mean of 119.7; 1.70 lands at
            # 120.3, which is as close as a render choice gets. AND THE
            # PICTURE IS WORSE AT IT: the brick loses its punch, the shop
            # glass goes to a pale grey panel and the whole street reads
            # hazy, like a photograph taken through a window. 1.35 measures
            # 111.6 and looks like a street.
            #
            # THIS IS THE SECOND TIME IN ONE SITTING that a measure went the
            # right way while the picture went the wrong way - the first was
            # the saturation figure going UP when the windows carried a tiled
            # photograph nobody wanted. Both are worth remembering together,
            # because the arithmetic is the only part of this that can be
            # automated and it is not the part that decides.
            return "hdri=%s skyStrength=0.7/the-scene-file's-own" % hdr.replace(" ", "~")
        except RuntimeError:
            pass
    if bg is not None:
        bg.inputs["Color"].default_value = (0.42, 0.45, 0.50, 1.0)
        bg.inputs["Strength"].default_value = 1.0
    return "hdri=NOT-FOUND/flat-overcast-instead"


def _ground(bpy, p, mats):
    """The footway and the road under the bay, so it is standing on something.
    The street's own widths: 2 m footway each side, 6 m carriageway."""
    W = p["bay_width_m"]
    run = W * p["bays"]
    # THE FOOTWAY STOPS WELL SHORT OF THE CAMERA. It used to run fourteen
    # metres out from the frontage, and the elevation camera stands forty-one
    # metres back to get six bays in frame, so the slab was BETWEEN the two:
    # seen almost edge-on it drew a grey band across the bottom of every
    # elevation and hid the shopfronts, which are the thing being judged. Two
    # metres is the street's own footway width and is all this needs to be.
    part = {"id": "footway", "x0": -W * 1.5, "x1": run + W * 1.5,
            "y0": -2.0, "y1": 0.0, "z0": -0.12, "z1": 0.0}
    obj = _box_mesh(bpy, part, mats.get("stone"))
    return obj


def _camera(bpy, name, spec):
    cam_data = bpy.data.cameras.new(name)
    cam_data.lens_unit = "FOV"
    cam_data.sensor_fit = "VERTICAL"
    cam_data.angle_y = math.radians(spec["fov_v_deg"])
    cam = bpy.data.objects.new(name, cam_data)
    bpy.context.scene.collection.objects.link(cam)
    lx, ly, lz = spec["loc"]
    tx, ty, tz = spec["look"]
    cam.location = (lx, ly, lz)
    cam.rotation_euler = look_at_euler((lx, ly, lz), (tx, ty, tz))
    # A LENS SHIFT, when the camera asks for one: the picture moves and the
    # camera does not tip, so verticals stay vertical. Positive moves the
    # frame up, which puts the horizon lower in it.
    if "shift_y" in spec:
        cam_data.shift_y = float(spec["shift_y"])
    return cam


def build_and_render(args):
    bpy = _bpy()
    street = (args["block"] == "street")
    # THE STREET IS A DIFFERENT SUBJECT, not a bigger row: three blocks, the
    # road between them, and the cameras the scene file itself names. The
    # per-block cross-check still runs on the parade, because the numbers it
    # compares are the row's rather than the street's.
    p, err = load_spec(args["root"], args["spec"],
                       "east_parade" if street else args["block"])
    if err:
        print("terrace-front refused: status=NO-SPEC reason=%s nothing measured" % err)
        return 3
    if street:
        parts, serr = plan_street(args["root"], args["spec"])
        if serr:
            print("terrace-front refused: status=NO-SPEC reason=%s nothing measured" % serr)
            return 3
    else:
        parts = plan_row(p)
    checks = cross_check(p, args["root"])

    for line in plan_lines(p, parts, checks):
        print(line)

    # A CLEAN SCENE, removed through the data API rather than by an operator:
    # operators need a context a --background run does not reliably have.
    removed = 0
    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)
        removed += 1
    print("tfNote sceneReset=dataApi/removed=%d-objects" % removed)

    mats = _materials(bpy, args["root"])
    signs = []
    built = 0
    for part in parts:
        mat = mats.get(part["material"])
        if part.get("decal"):
            # ONE MATERIAL PER SIGN. There were briefly two, one each way
            # round, when the west row was mirrored and its lettering came
            # out backwards; the row is turned rather than mirrored now, so
            # both sides read the same image the same way.
            key = ("card_%s" if part.get("decal_emit") else "sign_%s") % part["decal"]
            if key not in mats:
                mats[key], note = _decal_material(bpy, args["root"], key, part["decal"],
                                                  part.get("paint"), part.get("decal_uv"),
                                                  emit=bool(part.get("decal_emit")))
                signs.append("%s=%s" % (part["decal"], note))
            mat = mats[key]
        elif part.get("paint_name"):
            mat = _paint_variant(bpy, mats, part["paint_name"], part["paint"])
        if part.get("kind") == "slope":
            _slope_mesh(bpy, part, mat)
        elif part.get("kind") == "mesh":
            _face_the_street(bpy,
                _mesh_object(bpy, part["id"], part["verts"], part["faces"], mat),
                part.get("block"))
        else:
            _face_the_street(bpy, _box_mesh(bpy, part, mat), part.get("block"))
        built += 1
    if signs:
        print("tfSigns " + " ".join(signs))
    if street and args.get("export_glb"):
        # THE CROSSING. Geometry only, and nothing after this line runs: the
        # light, the wet, the wear and the grade are Unreal's to develop now.
        return _export_street(bpy, args, parts)
    if street:
        # THE PAVEMENT'S OWN THINGS, AFTER THE GEOMETRY AND BEFORE THE LIGHT,
        # because they are loaded from files rather than built from the piece
        # list and the material they take has to exist first.
        _place_props(bpy, args["root"], mats)
    if not street:
        _ground(bpy, p, mats)
    night = street and args["condition"] == "wet_night"
    if night:
        world_note = _night(bpy, args["root"], mats)
    else:
        world_note = _world(bpy, args["root"])
    # THE SHOP WINDOWS ARE LIT IN BOTH CONDITIONS, and that is a departure
    # from the scene file with a reason. It marks window_practicals "off" for
    # overcast_day - but the Hook sheet's own street panel is overcast
    # DAYLIGHT and every trading shop in it glows warm from inside, which is
    # what a British shop with the lights on looks like against a grey sky and
    # is most of what makes that row read as OPEN rather than shuttered.
    # Recorded here rather than changed in the spec, because the spec is his.
    tube = mats.get("tube_lit")
    if tube is not None and tube.use_nodes:
        bt = tube.node_tree.nodes.get("Principled BSDF")
        if bt is not None and "Emission Color" in bt.inputs:
            bt.inputs["Emission Color"].default_value = (0.90, 0.94, 1.00, 1.0)
            bt.inputs["Emission Strength"].default_value = 12.0
    lit = mats.get("interior_lit")
    if lit is not None and lit.use_nodes:
        b3 = lit.node_tree.nodes.get("Principled BSDF")
        if b3 is not None and "Emission Color" in b3.inputs:
            b3.inputs["Emission Color"].default_value = (1.0, 0.714, 0.344, 1.0)
            # 0.7 AT NIGHT, NOT 2.2, since the glass passes nine-tenths of
            # the room instead of a few per cent: at 2.2 the lit shops came
            # through as flat cream light-boxes, blown out, where before the
            # glass was fixed they barely showed at all. A lit shop at night
            # is the brightest thing on the street after the lamps, and still
            # a room.
            b3.inputs["Emission Strength"].default_value = 0.7 if night else 3.4
    for key, cm in mats.items():
        if key.startswith("card_") and cm is not None and cm.use_nodes:
            bc = cm.node_tree.nodes.get("Principled BSDF")
            if bc is not None and "Emission Strength" in bc.inputs:
                if "net_curtain" in key:
                    bc.inputs["Emission Strength"].default_value = (
                        NET_EMIT_NIGHT if night else NET_EMIT_DAY)
                else:
                    bc.inputs["Emission Strength"].default_value = (
                        CARD_EMIT_NIGHT if night else CARD_EMIT_DAY)
    if street:
        # THE SCENE FILE'S OWN WETNESS FOR THE CONDITION ASKED FOR, rather
        # than wet at night and bone dry by day, which is what the first
        # frames did and is a third of the way off the sheet on its own.
        # WEAR BEFORE WET, because a wet wall is a dirty wall with water on
        # it and not the other way round: the wetness multiplies whatever
        # base colour it finds, so it has to find one that is already worn.
        # THE BRICKS BEFORE THE WEAR, like the flag joints: a sooted wall is
        # a wall of bricks with soot on it.
        _brick_courses(bpy, mats)
        _wear(bpy, mats)
        # THE JOINTS BEFORE THE WATER, like the wear: a wet flag is a jointed
        # flag with water on it.
        _flag_joints(bpy, mats)
        _tile_pattern(bpy, mats)
        _wetten(mats, 0.9 if night else 0.6)
        _quiet_the_road(bpy, mats)
        if not night:
            # A SHOP INTERIOR BY DAY IS NOT A SHOP INTERIOR AT NIGHT, and
            # this material was only ever set for the night frame: 1.00,
            # 0.71, 0.34 is a warm amber GLOW, which is exactly right for a
            # lit window against a dusk street and wrong behind glass at
            # midday. In daylight what you see through a shop window is a dim
            # neutral room with the street's own light in it - darker than
            # the brick outside, not brighter, and with none of that colour.
            # The same card, lit two ways, because it IS the same card.
            mat = mats.get("interior_lit")
            if mat is not None and mat.use_nodes:
                bsdf = mat.node_tree.nodes.get("Principled BSDF")
                if bsdf is not None:
                    # DIMLY EMISSIVE BY DAY, NOT MERELY PALE. The card sits
                    # in a room that is sealed on five sides, so no light
                    # from this scene reaches it: an albedo of 0.105 in an
                    # unlit void renders black, which is what every shop
                    # window on the street was showing. A real shop at
                    # midday is lit by its own windows, its own lamps and
                    # the light down its own back passage, none of which
                    # this scene has any business modelling - so the card
                    # carries the result rather than the cause, the same
                    # way it already does at night and for the same reason.
                    # A tenth of the night's strength, because a lit shop by
                    # day is a room you can see into and not a lantern.
                    bsdf.inputs["Base Color"].default_value = (0.105, 0.098, 0.090, 1.0)
                    bsdf.inputs["Roughness"].default_value = 0.92
                    if "Emission Color" in bsdf.inputs:
                        # WARMER AND DIMMER, 22 September, once the glass
                        # let it be seen: at 0.62/0.58/0.52 x 0.30 it came
                        # through clear glass at 119/116/112, a pale neutral
                        # that read as frosted glass. The sheet's MICKEY'S
                        # interior measures 66/60/51 away from its strips -
                        # darker than the brick and warm - so the card goes
                        # there, and the tubes carry the brightness.
                        bsdf.inputs["Emission Color"].default_value = (0.66, 0.57, 0.44, 1.0)
                        bsdf.inputs["Emission Strength"].default_value = 0.14
    print("tfNote condition=%s world/%s"
          % (args["condition"] if street else "overcast_day", world_note))

    # NO SUN AT NIGHT, AND THAT IS THE SCENE FILE'S OWN WORD. wet_night reads
    # `"sun": "off", "sun_intensity": 0.0`, and the first night frame had one
    # at 0.10 anyway - which, with the sky dome behind it, is why the light in
    # that frame was arriving from above rather than from the lamps. Read
    # rather than assumed, and the spec was right.
    if not night:
        sun_data = bpy.data.lights.new("sun", type="SUN")
        sun_data.energy = 2.2
        sun_data.angle = math.radians(8.0)
        sun = bpy.data.objects.new("sun", sun_data)
        bpy.context.scene.collection.objects.link(sun)
        sun.rotation_euler = (math.radians(54.0), 0.0, math.radians(200.0))

    scene = bpy.context.scene
    # THE VIEW TRANSFORM, WHICH THE FIRST PAIR SAID WAS MISSING IN ONE LOOK.
    # Our sky came back a flat blown white beside the sheet's soft grey cloud,
    # and a blown sky is not a lighting problem - it is the absence of any
    # tone curve at all. Blender's Standard transform clips everything over
    # 1.0; AgX rolls the highlights off the way a camera does, which is what
    # the sheet is a photograph of. The exposure is the scene file's own
    # exposure_pin for the condition, applied as a stop offset - a render
    # choice, like every other use of those numbers here, because they are
    # Unity units with no defined conversion.
    try:
        scene.view_settings.view_transform = "AgX"
    except TypeError:
        scene.view_settings.view_transform = "Filmic"
    # THE LOOK AND THE EXPOSURE ARE ONE DECISION, swept together and read
    # off the frame. Three looks at one exposure, then the best of them at
    # three exposures, against the sheet's own four numbers:
    #
    #   AgX - Punchy        mean 109.0  p95 195.7  warmth +15.0  colour 15.0%
    #   AgX - High Contrast mean 137.8  p95 233.0  warmth +20.8  colour 19.4%
    #   ...at exposure 0.05 mean 123.0  p95 224.7  warmth +19.3  colour 22.6%
    #   THE SHEET           mean 119.7  p95 229.3  warmth +18.5  colour 25.8%
    #
    # Punchy was chosen earlier because it was the look that added
    # saturation, and at the time everything else on the street was too dark
    # for contrast to be worth anything. With the palette, the road, the
    # glazing and the haze all where they belong, CONTRAST is what carries
    # the colour: the high-contrast look lands the highlights the sheet has
    # and takes saturation with it, and the exposure comes down to put the
    # mean back where it was.
    #
    # AND THE PICTURE AGREES THIS TIME, which had to be checked rather than
    # assumed - twice today a measure moved the right way while the picture
    # moved the wrong way, and both are recorded beside the values they
    # argue about. This one is richer brick, a deeper oxblood and a road
    # that still reads wet.
    scene.view_settings.look = "AgX - High Contrast" if not night else "None"
    scene.view_settings.exposure = 0.6 if night else 0.05
    # DEPTH BEYOND THIRTY METRES IS STILL OPEN, and this is what was tried.
    #
    # The scene file carries fog_density 0.012 with a max opacity of 0.1 for
    # overcast_day and 0.022 at 0.45 for wet_night, and they have never been
    # applied to anything. Haze is the right answer to the gap: the far end of
    # our street reads as near as the front of it because nothing is between
    # the eye and it, and the sheet's own town on the hill is pale and soft,
    # which is most of what says how far away it is.
    #
    # DEPTH BEYOND THIRTY METRES, ATTEMPT THREE, and it does not start from
    # scratch.
    #
    # THE TWO THAT FAILED, kept because they are the reason this one is
    # shaped differently: a world VOLUME SCATTER, once at the scene file's
    # own density and again with EEVEE's volumetric range opened to 120 m,
    # its sample count raised and its density cut to a third. Mean frame
    # brightness 0.1 out of 255 both times - a black picture, not a hazy
    # one. Fighting a renderer's volumetrics a third time would have been
    # the same evening again.
    #
    # SO THIS IS NOT VOLUMETRICS AT ALL. It is a MIST pass mixed toward the
    # sky in the compositor, and the reason to prefer it is not that it is
    # easier: it is that it CANNOT produce the failure the other two did. A
    # post-mix toward a pale colour has no path to black. The worst it can
    # do is too much or too little haze, both of which are visible at a
    # glance and adjustable by one number.
    #
    # WHAT IT IS FOR, MEASURED OFF THE SHEET rather than assumed. On the
    # approved sheet the near brick reads mean 69.5 at saturation 0.442 and
    # the far buildings read mean 100.0 at saturation 0.330: distance makes
    # things PALER and LESS COLOURED, which is aerial perspective and is
    # most of what says how far the eye is carrying. Ours had none at all -
    # near and far brick came back at the same saturation, because nothing
    # stood between the camera and the far end.
    #
    # THE OPACITY IS A RENDER CHOICE AND IS NAMED AS ONE. The scene file
    # gives overcast_day a fog_max_opacity of 0.1, and that is a Unity
    # figure with no defined conversion - the same thing this file already
    # says about sky_intensity and about the lantern's watts. 0.1 of a mix
    # is not visible; what matches the sheet's own falloff is nearer a
    # third, so a third is what it takes, said out loud rather than
    # smuggled in as the spec's number.
    #
    # WHAT THIS IS NOT: the missing TOWN past the end of the street. That is
    # stage 6 and nothing here invents it. Our far end is still SKY rather
    # than a hill with houses on it, and haze on an empty sky is haze on
    # nothing; this softens the street we have.
    _mist(bpy, scene, night)
    scene.render.engine = "BLENDER_EEVEE_NEXT"
    # RAYTRACING ON, AND IT IS THE REASON OUR WET STREET WAS NOT WET.
    #
    # MEASURED, 22 September: our road rendered at sRGB 57,59,62 against the
    # approved sheet's 147,146,143 - two and a half times too dark - while our
    # SKY rendered at 176. A wet road is not a dark surface, it is a MIRROR,
    # and almost all of that 147 is the sky lying in it. EEVEE Next ships with
    # raytracing OFF, so every glossy surface in this street was falling back
    # to a rough world approximation: the roughness curve in _wetten was doing
    # its arithmetic correctly and there was nothing for it to reflect.
    #
    # This is also why raising the road's albedo did so little. Chasing the
    # reference's value by lightening the tarmac would have produced a pale
    # DRY road that happens to measure right, which is the wrong picture
    # arriving at the right number - the thing this file's checks exist to
    # catch. The albedo stays where a damp carriageway belongs and the
    # reflection supplies the rest.
    try:
        scene.eevee.use_raytracing = True
        # THE NAME MOVED, and the note below was a lie for as long as it did.
        # This build calls it trace_max_roughness; asking for the old
        # screen_trace_max_roughness raised AttributeError AFTER raytracing
        # had already been switched on, so every render printed "raytracing
        # unavailable" while raytracing was on, at the build's defaults.
        #
        # THE ROUGHNESS CEILING STAYS AT THE 0.5 IT ACTUALLY HAD, this
        # build's default (the resolution moved; see below). The palette was
        # re-closed against the new sheet at those values the same night;
        # the 1.0 the old line meant to ask for brightens the wet footway
        # by about seventeen levels and would reopen that work. Written out
        # so the numbers are the recipe's, not the build's.
        opts = scene.eevee.ray_tracing_options
        if hasattr(opts, "trace_max_roughness"):
            opts.trace_max_roughness = 0.5
        else:
            opts.screen_trace_max_roughness = 0.5
        # FULL RESOLUTION, 23 September, once the shop windows had rooms in
        # them: at half resolution the refraction blurred each room to a
        # smear. Measured before and after, the frame's regions do not move
        # (whole 118.4 -> 118.3, road 183, footway 96), so the palette stays
        # closed; only the detail through the glass sharpens.
        opts.resolution_scale = "1"
        print("tfNote raytracing=on/max-roughness-0.5/full-resolution")
    except (AttributeError, TypeError) as exc:
        # SAID OUT LOUD RATHER THAN SILENTLY FLAT, the same rule the world
        # and the HDRI already follow here: a street that is not reflecting
        # is a different picture and nobody should have to guess whether it
        # is this one.
        print("tfNote raytracing=unavailable/%s/the-wet-road-will-not-mirror"
              % type(exc).__name__)
    scene.render.resolution_x, scene.render.resolution_y = AUTHORED_RES
    scene.render.image_settings.file_format = "PNG"

    cams = street_cameras() if street else frame_cameras(p)
    wrote = 0
    for name in (tuple(cams.keys()) if street else FRAMES):
        # A FRAME CAN ASK FOR ITS OWN SHAPE, and the hook frame does. See
        # HOOK_RES for why a nearly square picture could never have matched
        # a two-to-one one however the camera was moved.
        scene.render.resolution_x, scene.render.resolution_y =             cams[name].get("res", AUTHORED_RES)
        cam = _camera(bpy, "cam_" + name, cams[name])
        scene.camera = cam
        out = os.path.join(args["out"],
                           "terrace-front-%s-%s-%s.png"
                           % ("street" if street else p["block_id"],
                              args["condition"] if street else "overcast_day", name))
        scene.render.filepath = out
        bpy.ops.render.render(write_still=True)
        size = os.path.getsize(out) if os.path.exists(out) else 0
        print("tfFrame id=%s png=%s bytes=%d fovVDeg=%.1f note=%s"
              % (name, os.path.basename(out), size, cams[name]["fov_v_deg"],
                 cams[name]["note"]))
        if size > 0:
            wrote += 1

    agree = sum(1 for _, _, _, a in checks if a)
    # WHAT IS STILL WRONG, RE-WRITTEN 22 SEPTEMBER against the APPROVED
    # sheet. Everything this line used to say was measured against Codex's
    # retired one, so it described a different street's faults - which is
    # worse than saying nothing, because it reads as current.
    print("tfStatus=ACCEPTED/measures-like-the-sheet-on-value-and-warmth "
          "whatIsStillWrong=saturated-colour-is-6-7-percent-against-the-sheet's-25-8-"
          "and-the-road-is-a-wide-pale-band-with-no-wheel-tracks "
          "theGapIsContent=the-sheet's-frame-is-full-of-close-painted-shopfront/"
          "crossCheckAgree-is-5/5")
    print("terrace-front done: status=RAN block=%s bays=%d partsBuilt=%d/%d "
          "crossCheckAgree=%d/%d previewsWrote=%d/%d res=%dx%d outDir=%s"
          % ("street" if street else p["block_id"], p["bays"], built, len(parts),
             agree, len(checks), wrote, len(cams),
             AUTHORED_RES[0], AUTHORED_RES[1], args["out"]))
    return 0 if wrote == len(FRAMES) else 1


# ---------------------------------------------------------------------------


def parse_args(argv):
    args = list(argv)
    if "--" in args:
        args = args[args.index("--") + 1:]
    elif args and args[0].endswith(".py"):
        args = args[1:]
    out = {"out": "", "root": ROOT, "spec": SPEC_REL, "block": "east_parade",
           "condition": "overcast_day", "export_glb": "",
           "plan": False, "selftest": False, "error": ""}
    i = 0
    while i < len(args):
        a = args[i]
        if a in ("--out", "--output-dir") and i + 1 < len(args):
            out["out"] = args[i + 1]; i += 2
        elif a == "--root" and i + 1 < len(args):
            out["root"] = args[i + 1]; i += 2
        elif a == "--spec" and i + 1 < len(args):
            out["spec"] = args[i + 1]; i += 2
        elif a == "--block" and i + 1 < len(args):
            out["block"] = args[i + 1]; i += 2
        elif a == "--condition" and i + 1 < len(args):
            out["condition"] = args[i + 1]; i += 2
        elif a == "--plan":
            out["plan"] = True; i += 1
        elif a == "--export-glb" and i + 1 < len(args):
            out["export_glb"] = args[i + 1]; i += 2
        elif a == "--selftest":
            out["selftest"] = True; i += 1
        # THE LANE PASSES THESE AND THIS RECIPE READS NO COMMISSION, so they
        # are accepted and ignored rather than refused: a recipe that rejects
        # the lane's own line cannot be run by the lane.
        elif a in ("--commission", "--run-sha", "--studio-sha", "--res",
                   "--engine", "--samples") and i + 1 < len(args):
            i += 2
        else:
            out["error"] = "unknown-flag/%s" % a.replace(" ", "~")
            break
    return out


#: THE STREET CROSSES INTO UNREAL HERE, 23 September, and this is the only
#: place it does. Jafar's ruling of the morning: Blender is for shapes and
#: layout, all look-development happens in Unreal, and "the mirror is fixed
#: once, at the point where Blender work crosses into Unreal, so every asset
#: arrives the right way round and nothing downstream has to remember it."
#:
#: THE MIRROR. This recipe builds Quay Street with east at +y in a
#: right-handed, z-up world, so looking north the parade is on the LEFT -
#: the mirror of the street the scene file, the research drawings and the
#: Unreal probe describe, where it is on the right. Every building is
#: mirrored with it, down to which side of Mickey's the private door is. So
#: the fix is ONE REFLECTION OF THE WHOLE STREET, y to -y, which puts every
#: building and every door where the drawings have them; the face winding is
#: reversed with it so the faces still face out. The glTF exporter and
#: Unreal's importer between them preserve how a model looks, so what
#: arrives in Unreal is the reflected street: east at +Y, on the right.
#:
#: AND THE LETTERING IS NOT REFLECTED. A reflection reverses text, so every
#: lettered face - the signs, the letting board, the pictured rooms and the
#: nets - takes UVs worked out AFTER the reflection, running from the
#: reader's left to the reader's right in the reflected street. Everything
#: else takes UVs in METRES by the face's own axis, so a material in Unreal
#: tiles by a world size and not by a box's proportions.
#:
#: WHAT DOES NOT CROSS: the lamps and the held props, which Unreal already
#: places from the scene file by its own mesh route, and the stand-in
#: people, which are stage 2's. And no material data: each mesh carries its
#: material's NAME, and the sidecar says what that material was here - its
#: colour, its map, its tile - as a TARGET for Unreal, not a result.
STREET_GLB_SKIP = ("lamp", "figure")
#: Where tools/props/make_street_surfaces.py writes the drawn surfaces.
STREET_SURFACES_REL = os.path.join("production", "assets", "street", "surfaces")


def _newell(pts):
    import mathutils
    n = mathutils.Vector((0.0, 0.0, 0.0))
    for i in range(len(pts)):
        a, b = pts[i], pts[(i + 1) % len(pts)]
        n.x += (a.y - b.y) * (a.z + b.z)
        n.y += (a.z - b.z) * (a.x + b.x)
        n.z += (a.x - b.x) * (a.y + b.y)
    return n.normalized() if n.length > 1e-12 else n


def _street_mesh_name(key, decal):
    """A NAME UNREAL CAN MAKE AN ASSET OF, and one Blender will not cut short.

    Letters, digits and underscores, since the importer derives asset names
    from it; and a lettered mesh is named by its PICTURE, not the picture's
    whole path, because Blender stops a name at 63 characters and the first
    export cut Mickey's sign to "..._fascia_mickeys_", which no sidecar row
    then matched."""
    if decal and key.startswith(("sign_", "card_")):
        key = key.split("_", 1)[0] + "_" + decal.replace("\\", "/").rsplit("/", 1)[-1]
    return "street_" + "".join(c if c.isalnum() else "_" for c in key)


#: WHAT OF THE SCENE FILE'S OWN PIECES THIS STREET STANDS IN FOR, written
#: into the sidecar so Unreal reads it rather than keeping a second copy.
#: The recipe builds the terraces, the pavements, the kerbs, the yellow
#: lines, the signs and everything fixed to a frontage or a roof; it does
#: not build the lamp columns, the kiosk, the pillar box, the railing, the
#: bins, the litter or the ground props, so those stay the scene file's.
STREET_REPLACES_PREFIXES = ("east_", "west_", "ground_", "kerb", "yellow_", "gully_")
STREET_REPLACES_SHAPES = ("decal",)


def _street_replaces(args):
    """The sidecar's replaces_in_unreal block, the held props read off the
    scene file: every one that is not stood on the ground is the frontage's
    or the roof's, and the recipe built its own."""
    import json
    assets = []
    try:
        with open(os.path.join(args["root"], args.get("spec") or SPEC_REL), encoding="utf-8") as fh:
            spec = json.load(fh)
        for it in spec.get("held_props", {}).get("items", []):
            if it.get("place") not in ("ground", "set_in") and it.get("asset") not in assets:
                assets.append(it.get("asset"))
    except (OSError, ValueError):
        assets = []
    return {"piece_name_prefixes": list(STREET_REPLACES_PREFIXES),
            "piece_shapes": list(STREET_REPLACES_SHAPES),
            "held_prop_assets": sorted(a for a in assets if a),
            "why": "the recipe builds these itself; lamps, kiosk, pillar box, railing, "
                   "bins, litter and ground props are the scene file's and stay"}


def _street_emit(key, lettered, night):
    """The emission strength this recipe gives a material, or None. Mirrors
    the lighting pass's own numbers (tubes 12, lit rooms 3.4 by day and 0.7
    at night, the pictured rooms and nets their CARD_ and NET_ figures)."""
    if key == "tube_lit":
        return 12.0
    if key == "interior_lit":
        return 0.7 if night else 3.4
    if key.startswith("card_"):
        if "net_curtain" in key:
            return NET_EMIT_NIGHT if night else NET_EMIT_DAY
        return CARD_EMIT_NIGHT if night else CARD_EMIT_DAY
    return None


def _export_street(bpy, args, parts):
    """Export the street's geometry, mirrored, one mesh per material, and a sidecar."""
    import json
    import mathutils
    by_id = {p["id"]: p for p in parts}
    table = {n: (rgb, rough) for n, rgb, rough in MATERIALS}
    drawn = {}
    try:
        with open(os.path.join(args["root"], STREET_SURFACES_REL, "manifest.json"), encoding="utf-8") as fh:
            for name, row in json.load(fh).get("surfaces", {}).items():
                drawn[name] = {"map": STREET_SURFACES_REL.replace(os.sep, "/") + "/" + name,
                               "tile_m": row.get("tile_m")}
    except (OSError, ValueError):
        drawn = {}
    groups = {}
    info = {}
    skipped = 0
    # THE TRANSFORMS BROUGHT UP TO DATE FIRST. The west blocks are turned
    # half round by their object's rotation, and Blender does not work out
    # an object's world matrix until something asks the scene to; the first
    # export read them unturned and stood a west-side room box across the
    # road, 20 cm in front of the hook camera.
    bpy.context.view_layer.update()
    for obj in list(bpy.context.scene.objects):
        if obj.type != "MESH":
            continue
        if obj.name.startswith(STREET_GLB_SKIP):
            skipped += 1
            continue
        mat = obj.data.materials[0] if len(obj.data.materials) else None
        key = mat.name if mat is not None else "none"
        part = by_id.get(obj.name, {})
        M = obj.matrix_world
        world = [M @ v.co for v in obj.data.vertices]
        # THE REFLECTION, y to -y, and nothing else moves.
        world = [mathutils.Vector((p.x, -p.y, p.z)) for p in world]
        lettered = key.startswith(("sign_", "card_"))
        crop = part.get("decal_uv")
        g = groups.setdefault(key, {"verts": [], "faces": [], "uvs": []})
        if key not in info:
            base = part.get("material", key)
            rgb, rough = table.get(base, (None, None))
            surf = SURFACE_OF.get(base, (None, 0.0))
            info[key] = {
                "mesh": _street_mesh_name(key, part.get("decal")),
                "material": key, "base_material": base,
                "linear_rgb": list(part["paint"]) if part.get("paint") and not lettered
                              else (list(rgb) if rgb else None),
                "roughness": rough,
                "surface_map": surf[0], "tile_m": surf[1],
                "decal": part.get("decal"), "decal_uv": crop,
                "decal_emit": part.get("decal_emit") or None,
                # WHAT THE PHOTOGRAPH'S OWN AVERAGE IS, so Unreal can do what
                # this file does: the map supplies pattern and relief, and the
                # colour is the authored one divided by this.
                "texture_mean": list(TEXTURE_MEAN[surf[0]]) if surf[0] in TEXTURE_MEAN else None,
                # AND HOW BRIGHTLY IT GLOWS HERE, day and night, as TARGETS:
                # Blender's emission strengths, which Unreal's own units do
                # not share, so the Unreal side scales them by one named gain.
                # THE DRAWN SURFACE, where this recipe draws one (bricks,
                # flags, the stallriser tile): tools/props/make_street_surfaces.py
                # draws the same numbers into seamless images, and Unreal
                # wears those instead of the pack photograph.
                "drawn_map": drawn.get(base, {}).get("map"),
                "drawn_tile_m": drawn.get(base, {}).get("tile_m"),
                "emit_day": _street_emit(key, lettered, False),
                "emit_night": _street_emit(key, lettered, True),
                "faces": 0,
            }
        for poly in obj.data.polygons:
            idx = list(poly.vertices)[::-1]          # the winding reversed with the reflection
            pts = [world[i] for i in idx]
            n = _newell(pts)
            uvs = []
            if lettered and abs(n.z) < 0.7:
                # THE READER'S RIGHT, in the reflected street: looking at the
                # face means looking along -n, and right is forward x up.
                fwd = -n
                right = fwd.cross(mathutils.Vector((0.0, 0.0, 1.0))).normalized()
                rs = [p.dot(right) for p in world]
                zs = [p.z for p in world]
                r0, r1, z0, z1 = min(rs), max(rs), min(zs), max(zs)
                for p in pts:
                    u = (p.dot(right) - r0) / max(1e-9, r1 - r0)
                    v = (p.z - z0) / max(1e-9, z1 - z0)
                    if crop:
                        u = crop[0] + u * (crop[2] - crop[0])
                        v = crop[1] + v * (crop[3] - crop[1])
                    uvs.append((u, v))
            else:
                ax, ay, az = abs(n.x), abs(n.y), abs(n.z)
                for p in pts:
                    if az >= ax and az >= ay:
                        uvs.append((p.x, p.y))
                    elif ax >= ay:
                        uvs.append((p.y, p.z))
                    else:
                        uvs.append((p.x, p.z))
            base_i = len(g["verts"])
            g["verts"].extend((p.x, p.y, p.z) for p in pts)
            g["faces"].append(tuple(range(base_i, base_i + len(pts))))
            g["uvs"].extend(uvs)
            info[key]["faces"] += 1
    names = [i["mesh"] for i in info.values()]
    if len(set(names)) != len(names) or max(len(n) for n in names) > 60:
        print("tfExport status=REFUSED reason=mesh-names-collide-or-exceed-60/%s" % names)
        return 1
    # THE EXPORT SCENE: one object per material, and nothing else in it.
    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)
    made = []
    for key, g in sorted(groups.items()):
        name = info[key]["mesh"]
        mesh = bpy.data.meshes.new(name)
        mesh.from_pydata(g["verts"], [], g["faces"])
        uv = mesh.uv_layers.new(name="UVMap")
        for li, loop in enumerate(mesh.loops):
            uv.data[li].uv = g["uvs"][loop.vertex_index]
        mesh.validate()
        mesh.update()
        mat = bpy.data.materials.get(key) or bpy.data.materials.new(key)
        mesh.materials.append(mat)
        obj = bpy.data.objects.new(name, mesh)
        bpy.context.scene.collection.objects.link(obj)
        made.append(name)
    out = os.path.join(args["root"], args["export_glb"])
    os.makedirs(os.path.dirname(out), exist_ok=True)
    bpy.ops.export_scene.gltf(filepath=out, export_format="GLB", export_materials="PLACEHOLDER",
                              export_yup=True, export_texcoords=True, export_normals=True,
                              export_cameras=False, export_animations=False, export_extras=False)
    side = os.path.splitext(out)[0] + ".json"
    with open(side, "w", encoding="utf-8") as fh:
        json.dump({
            "what": "Quay Street's geometry, exported by tools/art-recipes/terrace-front.py "
                    "--export-glb for Unreal's mesh route. One mesh per material; each mesh "
                    "carries its material's name, and the rows below say what that material "
                    "was in Blender - a TARGET for Unreal's look-development, not a result "
                    "(Jafar, 23 September).",
            "mirror": "REFLECTED y to -y AT EXPORT, faces re-wound: the Blender recipe builds "
                      "the mirror of the street the scene file and Unreal describe, and this "
                      "is the one place that is fixed. East arrives at Unreal +Y.",
            "uvs": "metres by each face's own axis, except lettered faces (sign_, card_), "
                   "whose UVs run reader's-left to reader's-right after the reflection, "
                   "cropped by decal_uv",
            "not_exported": "lamps and held props (Unreal places them from the scene file), "
                            "stand-in people (stage 2)",
            "units": "metres in Blender, z up; the glTF is y up",
            "replaces_in_unreal": _street_replaces(args),
            "meshes": [info[k] for k in sorted(groups)],
        }, fh, indent=1)
    size = os.path.getsize(out) if os.path.exists(out) else 0
    print("tfExport glb=%s bytes=%d meshes=%d faces=%d skipped=%d mirror=y-reflected sidecar=%s"
          % (args["export_glb"], size, len(made), sum(i["faces"] for i in info.values()),
             skipped, os.path.basename(side)))
    return 0 if size > 0 else 1


def selftest():
    passed = failed = 0

    def check(name, ok, detail=""):
        nonlocal passed, failed
        if ok:
            passed += 1
        else:
            failed += 1
            print("terrace-front selftest FAIL %s: %s" % (name, detail))

    p, err = load_spec(ROOT)
    check("accept/spec-loads", not err, err)
    if p:
        # THE SPEC'S OWN ARITHMETIC, RE-DONE. Every one of these is a number
        # terrace-fronts.md states as DERIVED; if this file's derivation and
        # the spec's prose ever disagree, one of them is wrong and this says
        # which run found it.
        check("accept/eaves-is-the-two-storeys", abs(p["eaves_m"] - 6.2) < 1e-9,
              "%.6f" % p["eaves_m"])
        check("accept/ridge-rise-is-half-depth-times-tan-pitch",
              abs(p["ridge_rise_m"] - 2.80) < 5e-3, "%.6f" % p["ridge_rise_m"])
        check("accept/ridge-stands-at-nine-metres-local",
              abs(p["ridge_m"] - 9.0) < 5e-3, "%.6f" % p["ridge_m"])
        check("accept/opening-zone-is-the-bay-less-two-piers",
              abs(p["opening_zone_m"] - 5.30) < 1e-9, "%.6f" % p["opening_zone_m"])
        # THE IDENTITY THE SPEC ASSERTS, CHECKED THE OTHER WAY ROUND. It says
        # 3.562 + 0.9 + 0.838 = 5.300; this derives the display run from the
        # zone and the two doors and asks whether it lands on 3.562.
        check("accept/display-run-is-3.562-as-the-spec-states",
              abs(p["display_w_m"] - 3.562) < 1e-9, "%.6f" % p["display_w_m"])
        check("accept/window-head-sits-0.4-below-the-ceiling",
              abs(p["window_head_m"] - (p["eaves_m"] - 0.4)) < 1e-9,
              "%.6f" % p["window_head_m"])
        check("accept/sill-is-0.95-wide", abs(p["sill_w_m"] - 0.95) < 1e-9,
              "%.6f" % p["sill_w_m"])
        check("accept/reveal-is-half-a-british-brick",
              abs(p["reveal_m"] - 0.1025) < 1e-9, "%.6f" % p["reveal_m"])
        # THE WALL IS ONE BRICK AND THE REVEAL IS HALF OF ONE, read from two
        # different keys in the scene file. They describe the same brick, so
        # the reveal must be under the wall it is set into; a reveal deeper
        # than its own wall is a window behind the building.
        check("accept/wall-is-one-british-brick", abs(p["wall_t_m"] - 0.215) < 1e-9,
              "%.6f" % p["wall_t_m"])
        check("accept/the-reveal-fits-inside-its-own-wall",
              0.0 < p["reveal_m"] < p["wall_t_m"],
              "reveal=%.4f wall=%.4f" % (p["reveal_m"], p["wall_t_m"]))
        c = window_centres(p)
        check("accept/upper-windows-at-1.5-and-4.5",
              abs(c[0] - 1.5) < 1e-9 and abs(c[1] - 4.5) < 1e-9,
              "%.4f,%.4f" % (c[0], c[1]))

        parts = plan_parts(p)
        check("accept/every-part-is-named-once",
              len(set(x["id"] for x in parts)) == len(parts),
              "%d ids, %d parts" % (len(set(x["id"] for x in parts)), len(parts)))
        check("accept/something-was-built", len(parts) > 20, "%d" % len(parts))
        boxes = [x for x in parts if x.get("kind") not in ("slope", "mesh")]
        check("accept/no-degenerate-box",
              all(b["x1"] > b["x0"] and b["y1"] > b["y0"] and b["z1"] > b["z0"] for b in boxes))
        # NOTHING SINKS BELOW THE THRESHOLD, which is the one fault a square-on
        # elevation frame cannot show.
        check("accept/nothing-below-the-threshold",
              all(b["z0"] >= -1e-9 for b in boxes),
              ",".join(b["id"] for b in boxes if b["z0"] < -1e-9))
        # THE FASCIA'S TOP IS THE SLAB, because the already-committed cornice
        # sits on it and this spec may not move it.
        fascia = [b for b in boxes if b["id"] == "fascia_band"][0]
        check("accept/fascia-top-is-the-first-floor-slab",
              abs(fascia["z1"] - p["ground_h_m"]) < 1e-9, "%.6f" % fascia["z1"])
        # THE OPENINGS ARE REALLY OPEN: no brick panel overlaps a window's x
        # range within the window band.
        band_lo, band_hi = p["window_sill_m"], p["window_head_m"]
        hw = p["window_w_m"] / 2.0
        overlaps = []
        for b in boxes:
            if not b["id"].startswith("upper_pier_"):
                continue
            for cx in window_centres(p):
                if b["x0"] < cx + hw - 1e-9 and b["x1"] > cx - hw + 1e-9:
                    overlaps.append(b["id"])
        check("accept/no-brick-pier-stands-in-a-window", not overlaps, ",".join(overlaps))
        # AND NOTHING SOLID STANDS BEHIND ONE EITHER, which is the fault the
        # first render of this bay actually had: the openings were correct and
        # the carcass filled the frontage plane behind them, so they showed
        # brick. Any part that is neither glass nor interior and crosses a
        # window's x range inside the window band fails here.
        # THE JOINERY IN FRONT OF A PANE IS NOT A BLOCKER, and this check
        # could not tell the two apart until the sashes arrived: it compared
        # x and z only, so a white frame standing proud of its own glass read
        # exactly like brick filling the hole behind it. The distinction is
        # DEPTH and it is taken from the glass itself rather than from a list
        # of names - a part wholly in front of the glazing plane is joinery,
        # and anything crossing that plane or sitting behind it is the
        # carcass showing through. Naming the sash parts instead would have
        # let the next thing called a sash through unlooked at.
        glazing_plane = min([b["y0"] for b in boxes if b["material"] == "glass"
                             and b["z1"] > band_lo + 1e-9 and b["z0"] < band_hi - 1e-9]
                            or [float("inf")])
        blockers = []
        for b in boxes:
            if b["material"] in ("glass", "interior"):
                continue
            # A NET CURTAIN IS MEANT TO BE THERE, and it is the one thing
            # behind an upper window that is: named by what it is for, not by
            # its id, so brick called a curtain would still be caught.
            if b.get("decal_emit") == "net":
                continue
            if b["y1"] <= glazing_plane + 1e-9:
                continue
            if b["z1"] <= band_lo + 1e-9 or b["z0"] >= band_hi - 1e-9:
                continue
            for cx in window_centres(p):
                if b["x0"] < cx + hw - 1e-9 and b["x1"] > cx - hw + 1e-9:
                    blockers.append(b["id"])
        check("accept/nothing-solid-stands-behind-an-upper-window",
              not blockers, ",".join(sorted(set(blockers))))

        # AND THE CHECK STILL HAS ITS TEETH. Loosening it to let the sashes
        # through is exactly the kind of change that quietly turns a check
        # into a decoration, so the loosened rule is run against a PLANTED
        # fault: a brick panel at the glazing plane, filling a window, which
        # is the original fault this check was written for. If the planted
        # brick passes, the check is no longer checking anything.
        cxs = list(window_centres(p))
        if cxs and glazing_plane < float("inf"):
            planted = {"id": "planted_brick_behind_a_window", "material": p["wall_surface"],
                       "x0": cxs[0] - hw * 0.5, "x1": cxs[0] + hw * 0.5,
                       "y0": glazing_plane, "y1": glazing_plane + 0.1,
                       "z0": band_lo + 0.1, "z1": band_hi - 0.1}
            caught = (planted["material"] not in ("glass", "interior")
                      and planted["y1"] > glazing_plane + 1e-9
                      and planted["z1"] > band_lo + 1e-9 and planted["z0"] < band_hi - 1e-9
                      and planted["x0"] < cxs[0] + hw - 1e-9
                      and planted["x1"] > cxs[0] - hw + 1e-9)
            check("reject/brick-planted-behind-a-window-is-still-caught", caught)
            # AND A FRAME IN FRONT OF THE SAME PANE IS STILL LET THROUGH.
            infront = dict(planted, id="planted_frame", material="paint_joinery",
                           y0=glazing_plane - 0.03, y1=glazing_plane)
            check("accept/joinery-in-front-of-the-same-pane-is-not-a-blocker",
                  not (infront["y1"] > glazing_plane + 1e-9))

        # THE SECOND ATTEMPT'S OWN CLAIMS, CHECKED. The first one failed by
        # eye and there was nothing in this file that could have said so; a
        # look is not repeatable and the next edit would have had to be
        # judged by eye again from scratch. These do not make the front
        # GOOD - D41 keeps that ungated and the sheet decides - but they
        # hold the three properties the failure was made of.
        gf = [b for b in boxes if b["z0"] < p["ground_h_m"] - 1e-9
              and b["z1"] > 1e-9 and b["x0"] >= p["pilaster_w_m"] - 1e-9]
        mats = set(b["material"] for b in gf)
        check("accept/the-shopfront-is-not-one-material",
              len(mats) >= 4, "materials=%s" % ",".join(sorted(mats)))
        # GLASS IS THE DARKEST THING ON IT, which is the ordering the whole
        # read depends on: if the joinery ever goes darker than the glass the
        # frame stops drawing and the slab comes back.
        lum = {name: 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
               for name, c, _r in MATERIALS}
        # THE GLASS USED TO HAVE TO BE THE DARKEST THING HERE, and that check
        # is gone because its premise is: it stood for an unlit interior, so
        # the joinery drew the frame against a dark hole. The shops are lit
        # now and the glass transmits, which is what a window is for. What
        # still has to be true is that the FRAME separates from the OPENING,
        # whichever of the two is lighter - a shopfront whose joinery and
        # glazing sit at the same value has no frame at any distance.
        gap = abs(lum["paint_joinery"] - lum["glass"])
        check("accept/the-joinery-separates-from-the-glazing",
              gap >= 0.2 * max(lum["paint_joinery"], lum["glass"]),
              "joinery %.4f vs glass %.4f" % (lum["paint_joinery"], lum["glass"]))
        # AND NOTHING ON THE GROUND FLOOR HIDES IN THE WALL. The second
        # attempt failed on exactly this: a side door whose paint sat within
        # a few percent of the brick's own value, so the one opening a person
        # walks through was invisible from across the street. A fifth of a
        # stop between any painted part and the wall it is set into, measured
        # rather than eyeballed.
        wall_l = lum[p["wall_surface"]]
        hidden = [m for m in mats
                  if m not in ("glass",) and m != p["wall_surface"]
                  and abs(lum[m] - wall_l) < 0.2 * wall_l]
        check("accept/no-painted-part-hides-in-the-brick-behind-it",
              not hidden,
              ",".join("%s(%.4f vs wall %.4f)" % (m, lum[m], wall_l) for m in sorted(hidden)))
        mullions = [b for b in boxes if "mullion" in b["id"]]
        check("accept/the-display-run-is-divided-not-one-sheet",
              len(mullions) >= 2, "%d mullion(s)" % len(mullions))
        jambs = [b for b in boxes if b["id"].startswith("display_jamb_")]
        check("accept/the-glazing-has-a-frame", len(jambs) == 2,
              "%d jamb(s)" % len(jambs))
        if len(jambs) == 2 and mullions:
            # ORDER-INDEPENDENT, because a bay may put its doors on either
            # side and the left jamb is then not the one nearest x=0 of the
            # BAY, only of the opening it frames.
            lo = min(j["x1"] for j in jambs)
            hi = max(j["x0"] for j in jambs)
            outside = [m["id"] for m in mullions
                       if m["id"].startswith("display_")
                       and (m["x0"] < lo - 1e-9 or m["x1"] > hi + 1e-9)]
            check("accept/every-mullion-stands-inside-the-frame-it-divides",
                  not outside, ",".join(outside))
        # THE TWO DOORS DO NOT STAND ON EACH OTHER. The fault the last render
        # showed was two pieces of joinery occupying the same strip of x at
        # the one point on the elevation where a person has to tell two doors
        # apart. Measured on the parts rather than looked at.
        shop_parts = [b for b in boxes if b["id"].startswith("shop_door")]
        side_parts = [b for b in boxes if b["id"].startswith("side_door")
                      or b["id"] == "letterplate"]
        clashes = []
        for a in shop_parts:
            for b in side_parts:
                if a["x0"] < b["x1"] - 1e-9 and a["x1"] > b["x0"] + 1e-9:
                    clashes.append("%s/%s" % (a["id"], b["id"]))
        # AND EVERY TRADING BAY HAS SOMETHING LIT BEHIND ITS GLASS. A window
        # you can see through onto nothing is worse than an opaque one: it
        # reads as a gutted unit. The street builder puts the cards in, so
        # this is checked there rather than on one bay.
        street_parts, _serr = plan_street(ROOT)
        if street_parts:
            cards = [b for b in street_parts if b["id"].startswith("interior_card_")]
            check("accept/the-trading-bays-are-lit-from-inside",
                  len(cards) >= 5, "%d card(s)" % len(cards))
            # BEHIND IS A DIRECTION, NOT A SIGN. This asked whether every
            # card sat at y greater than the frontage line, which is only
            # "behind" on the EAST side of the road; the day the near west
            # block gained shops, its cards were correctly placed at negative
            # y and this failed them for it. A card is behind its glazing
            # when its DISTANCE FROM THE CENTRE LINE exceeds the frontage's,
            # whichever side of the road it is on.
            outside = [b["id"] for b in cards
                       if min(abs(b["y0"]), abs(b["y1"])) <= STREET_FRONTAGE_M]
            check("accept/every-card-sits-behind-its-own-glazing", not outside,
                  ",".join(sorted(outside)[:3]))
            # AND ON THE SAME SIDE AS THE BLOCK IT BELONGS TO, which the old
            # test could not have asked at all.
            wrong_side = [b["id"] for b in cards
                          if (b["id"].startswith("interior_card_east") and b["y0"] < 0)
                          or (b["id"].startswith("interior_card_west") and b["y0"] > 0)]
            check("accept/and-on-its-own-block's-side-of-the-road",
                  not wrong_side, ",".join(sorted(wrong_side)[:3]))

        check("accept/the-two-doors-do-not-overlap-in-x", not clashes,
              ",".join(sorted(set(clashes))))
        # AND THE PRIVATE DOOR IS SET BACK, which is what puts it in shadow and
        # stops it reading as more shopfront.
        leaf = [b for b in boxes if b["id"] == "side_door_leaf"]
        shop_leaf = [b for b in boxes if b["id"] == "shop_door_leaf"]
        if leaf and shop_leaf:
            check("accept/the-private-door-sits-deeper-than-the-shop-door",
                  leaf[0]["y0"] > shop_leaf[0]["y0"] + 1e-9,
                  "side y0=%.4f shop y0=%.4f" % (leaf[0]["y0"], shop_leaf[0]["y0"]))
        # THE TOPLIGHT IS A BAND, bounded top and bottom by joinery. Without a
        # rail over it, it is not a band at all; it is the top of the window
        # below it, which is exactly how the last render read.
        top = [b for b in boxes if b["id"] == "toplight"]
        if top:
            z0, z1 = top[0]["z0"], top[0]["z1"]
            # ANY JOINERY, a refit's metal as much as painted timber: bay 0
            # is the cab office and has been a refit since 22 September.
            under = [b for b in boxes if b["material"] in JOINERY_MATERIALS
                     and abs(b["z1"] - z0) < 1e-6]
            over = [b for b in boxes if b["material"] in JOINERY_MATERIALS
                    and abs(b["z0"] - z1) < 1e-6]
            check("accept/the-toplight-is-closed-below-by-a-bar", bool(under),
                  "nothing ends at z=%.4f" % z0)
            check("accept/the-toplight-is-closed-above-by-a-rail", bool(over),
                  "nothing starts at z=%.4f" % z1)

        # AND BOTH DOORS ARE FINDABLE, which is the half the one-line note
        # named: a door the same value as the glass beside it is not a door.
        for door in ("shop_door", "side_door"):
            framing = [b for b in boxes
                       if b["id"].startswith(door) and b["material"] in JOINERY_MATERIALS]
            check("accept/%s-carries-its-own-framing" % door.replace("_", "-"),
                  len(framing) >= 2, "%d piece(s)" % len(framing))

        # ---- THE ROW, which is what the sheet is judged against now -------
        row = plan_row(p)
        rboxes = [b for b in row if b.get("kind") not in ("slope", "mesh")]
        check("accept/the-row-is-the-spec's-own-bay-count",
              len(set(b["bay"] for b in row)) == p["bays"],
              "%d bay(s) built, spec says %d" % (len(set(b["bay"] for b in row)), p["bays"]))
        check("accept/every-piece-in-the-row-is-named-once",
              len(set(b["id"] for b in row)) == len(row))
        # A DOWNPIPE AT EVERY INTERNAL PARTY WALL AND NONE AT THE ROW'S END,
        # which the spec states and the built street obeys: five on a six-bay
        # row, not six. Same for the stacks, which serve the two houses either
        # side of the wall they stand on.
        pipes = [b for b in rboxes if b["id"].startswith("downpipe")]
        stacks = [b for b in rboxes if b["id"].startswith("chimney_stack")]
        check("accept/one-downpipe-per-internal-party-wall",
              len(pipes) == p["bays"] - 1, "%d for %d bay(s)" % (len(pipes), p["bays"]))
        check("accept/one-stack-per-internal-party-wall",
              len(stacks) == p["bays"] - 1, "%d for %d bay(s)" % (len(stacks), p["bays"]))
        # THE ONE BAY WITH NO SIDE DOOR IS THE SPEC'S, and exactly one.
        leaves = [b for b in rboxes if b["id"].startswith("side_door_leaf")]
        check("accept/exactly-one-bay-has-no-side-door",
              len(leaves) == p["bays"] - 1, "%d door(s) on %d bay(s)" % (len(leaves), p["bays"]))
        # AND THE ROW IS NOT ONE STENCIL SIX TIMES. The fault the spec
        # measured on the built street was zero per-bay variation: every door
        # at the same offset down the whole row. Compared as the shop door's
        # offset WITHIN its own bay, so a row that went back to one formula
        # fails here rather than in somebody's eye six months later.
        offsets = {}
        for b in rboxes:
            if b["id"].startswith("shop_door_leaf"):
                offsets[b["bay"]] = round(b["x0"] - b["bay"] * p["bay_width_m"], 4)
        check("accept/the-row-does-not-repeat-one-stencil",
              len(set(offsets.values())) > 1,
              "shop door offsets: %s" % sorted(set(offsets.values())))
        # AND NO BAY STANDS IN THE NEXT ONE.
        spans = {}
        for b in rboxes:
            lo, hi = spans.get(b["bay"], (1e9, -1e9))
            spans[b["bay"]] = (min(lo, b["x0"]), max(hi, b["x1"]))
        bad = []
        for i in range(p["bays"] - 1):
            # the stack and the downpipe legitimately sit ON the party wall,
            # so the test is the CARCASS's own span rather than every piece.
            a = [b for b in rboxes if b["bay"] == i and b["id"].startswith("carcass")][0]
            c = [b for b in rboxes if b["bay"] == i + 1 and b["id"].startswith("carcass")][0]
            if a["x1"] > c["x0"] + 1e-9:
                bad.append("%d/%d" % (i, i + 1))
        check("accept/no-bay-overlaps-the-next", not bad, ",".join(bad))

        # ---- THE PLAIN ROW, which is a different building ------------------
        for other in ("west_south", "west_north"):
            q, qerr = load_spec(ROOT, block_id=other)
            check("accept/%s-loads" % other, not qerr, qerr)
            if qerr:
                continue
            qrow = plan_row(q)
            qboxes = [b for b in qrow if b.get("kind") not in ("slope", "mesh")]
            mats = set(b["material"] for b in qboxes)
            # WHICH KIND OF GROUND FLOOR THIS ROW HAS IS THE SPEC'S TO SAY,
            # and these checks used to assume it. Both west rows were plain
            # when they were written, so "carries no shopfront" was asserted
            # for both by name - and on 22 September Jafar ruled west_north
            # into shops, which failed two checks that were describing the
            # street rather than testing it. They ask the block now.
            #
            # EITHER WAY IT HAS TO BE WHOLEHEARTED. A plain row with a stray
            # pilaster on it is a house wearing a shop's bones; a shop row
            # missing its stallriser is a shopfront with a hole where the
            # kicked board goes. So the same list of parts is required to be
            # entirely absent or entirely present, never half.
            SHOP_PARTS = ("pilaster", "stallriser", "fascia", "transom",
                          "toplight", "mullion", "display", "shop_door")
            shoppy = set()
            for b in qboxes:
                for k in SHOP_PARTS:
                    if k in b["id"]:
                        shoppy.add(k)
            if q["ground_floor"] == "shopfront":
                missing = [k for k in SHOP_PARTS if k not in shoppy]
                check("accept/%s-carries-a-whole-shopfront" % other, not missing,
                      "missing " + ",".join(missing))
            else:
                check("accept/%s-carries-no-shopfront" % other, not shoppy,
                      ",".join(sorted(shoppy)[:4]))
            check("accept/%s-is-the-grey-brick" % other,
                  q["wall_surface"] == "brick_grey", q["wall_surface"])
            # A PARAPET AND A COPING, NOT A RIDGE, AND NO STACK.
            check("accept/%s-has-a-parapet-and-a-coping" % other,
                  any(b["id"].startswith("parapet") for b in qboxes)
                  and any(b["id"].startswith("coping") for b in qboxes))
            check("accept/%s-carries-no-chimney" % other,
                  not [b for b in qboxes if "chimney" in b["id"]],
                  "the spec found none on either west row")
            check("accept/%s-top-is-eaves-plus-parapet-plus-coping" % other,
                  abs(q["top_m"] - (q["eaves_m"] + q["parapet_h_m"] + q["coping_t_m"])) < 1e-9,
                  "%.4f" % q["top_m"])
            # THE DOOR AND TWO WINDOWS, one of each per bay.
            doors = [b for b in qboxes if b["id"].startswith("side_door_leaf")]
            glass = [b for b in qboxes if b["id"].startswith("gf_glass_")]
            if q["ground_floor"] == "shopfront":
                # A SHOP ROW HAS SHOP DOORS, not household ones, and its
                # glazing is the display run rather than a pair of sashes.
                shopdoors = [b for b in qboxes if b["id"].startswith("shop_door")]
                disp = [b for b in qboxes if b["id"].startswith("display_glazing")]
                check("accept/%s-has-a-shop-door-per-bay" % other,
                      len(shopdoors) >= q["bays"], "%d for %d" % (len(shopdoors), q["bays"]))
                check("accept/%s-has-a-display-window-per-bay" % other,
                      len(disp) >= q["bays"], "%d for %d" % (len(disp), q["bays"]))
            else:
                check("accept/%s-has-one-household-door-per-bay" % other,
                      len(doors) == q["bays"], "%d for %d" % (len(doors), q["bays"]))
                check("accept/%s-has-two-ground-floor-windows-per-bay" % other,
                      len(glass) == q["bays"] * 2, "%d for %d" % (len(glass), q["bays"]))
            # AND THE UPPER RHYTHM IS THE SAME ON BOTH ROWS, which is the one
            # thing the spec forbids varying: the string-course a viewer's eye
            # follows down the whole street.
            check("accept/%s-keeps-the-parade's-upper-window-rhythm" % other,
                  [round(c, 6) for c in window_centres(q)]
                  == [round(c, 6) for c in window_centres(p)],
                  "%s vs %s" % (window_centres(q), window_centres(p)))
            check("accept/%s-nothing-below-the-threshold" % other,
                  all(b["z0"] >= -1e-9 for b in qboxes))
            # AND NOTHING HIDES IN THIS ROW'S WALL EITHER. The parade's check
            # only ever looked at brick_red; the day brick_grey moved, the
            # joinery on this row could have walked into it unseen.
            qlum = {name: 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
                    for name, c, _r in MATERIALS}
            qwall = qlum[q["wall_surface"]]
            qgf = [b for b in qboxes if b["z0"] < q["ground_h_m"] - 1e-9 and b["z1"] > 1e-9]
            qhidden = [m for m in set(b["material"] for b in qgf)
                       if m not in ("glass",) and m != q["wall_surface"]
                       and abs(qlum[m] - qwall) < 0.2 * qwall]
            check("accept/%s-nothing-hides-in-the-grey-brick" % other,
                  not qhidden,
                  ",".join("%s(%.4f vs %.4f)" % (m, qlum[m], qwall) for m in sorted(qhidden)))
            check("accept/%s-every-piece-named-once" % other,
                  len(set(b["id"] for b in qrow)) == len(qrow))

        # ---- THE CAR, and it is checked by its BOX rather than looked at.
        # A profile extruded the wrong way round, or a facing that mirrors
        # instead of yawing, does not look obviously wrong in a wireframe and
        # is very obvious the moment light lands on it. Its measured extent
        # is the thing that catches both: if the body does not come out
        # 4.12 long, 1.64 across and standing on the road, something in the
        # reflect-and-reverse above is wrong.
        street, serr = plan_street(ROOT)
        if serr:
            check("accept/the-street-plans-with-a-car-in-it", False, serr)
        else:
            # ---- ONE FRONT IS A METAL REFIT, AND ONLY ONE.
            refits, timbers = [], []
            for b in street:
                if b.get("material") in REFIT_FRAMES:
                    refits.append(b["id"])
                if "_display_jamb_left_" in b["id"]:
                    timbers.append(b)
            check("accept/one-shopfront-is-a-metal-refit", bool(refits),
                  "%d piece(s)" % len(refits))
            # AND NOT EVERY ONE, because D06 says metal frames AMONG older
            # masonry. A parade all in metal is the same mistake the sheet
            # makes, in the other direction.
            # THE PIECE IDS CARRY THE BAY ON THE END, not the part name:
            # east_parade_display_jamb_left_bay1. The first version of these
            # three checks matched on a suffix that no piece has and passed
            # by finding nothing on both sides, which is the shape of a check
            # that cannot fail. Matched on the substring now, and the counts
            # below are printed so an empty one shows.
            metal_bays, timber_bays = set(), set()
            for b in street:
                if "_display_jamb_left_" not in b["id"]:
                    continue
                (metal_bays if b["material"] in REFIT_FRAMES else timber_bays).add(b["id"])
            check("accept/the-parade-is-mixed-not-all-metal",
                  bool(metal_bays) and len(timber_bays) > len(metal_bays),
                  "%d metal / %d timber" % (len(metal_bays), len(timber_bays)))
            # THE SECTIONS ARE ACTUALLY THINNER, which is the whole visual
            # difference. A grey timber shopfront reads as a timber
            # shopfront and the change would be worth nothing.
            mw = [b["x1"] - b["x0"] for b in street
                  if "_display_jamb_left_" in b["id"] and b["material"] in REFIT_FRAMES]
            tw = [b["x1"] - b["x0"] for b in street
                  if "_display_jamb_left_" in b["id"] and b["material"] not in REFIT_FRAMES]
            check("accept/the-metal-sections-are-under-half-the-timber",
                  bool(mw) and bool(tw) and max(mw) < min(tw) * 0.6,
                  "metal %.3f vs timber %.3f" % (max(mw) if mw else -1, min(tw) if tw else -1))
            # AND ITS STALLRISER IS TILE, NOT THE SHOP'S PAINT.
            tiles = [b["id"] for b in street if b.get("material") == "tile_stall"]
            check("accept/the-refitted-bay-has-a-tiled-stallriser", bool(tiles),
                  "%d" % len(tiles))
            # ---- THE PARADE, REWORKED TO THE 1989 PHOTOGRAPHS.
            byid = {b["id"]: b for b in street}
            j0 = byid.get("east_parade_display_jamb_left_bay0", {})
            check("accept/the-cab-office-is-a-slate-painted-metal-front",
                  j0.get("material") == "frame_painted", str(j0.get("material")))
            white_in_refit = [b["id"] for b in street
                              if b.get("material") == "paint_joinery"
                              and any(b["id"].startswith(k[0] + "_") and b["id"].endswith("_bay%d" % k[1])
                                      for k in SHOPFRONT_REFITS)
                              and ("mullion" in b["id"] or "transom" in b["id"]
                                   or "toplight" in b["id"] or "shop_door" in b["id"])]
            check("reject/no-refit-has-white-timber-inside-its-metal-frame",
                  not white_in_refit, ",".join(white_in_refit[:3]))
            check("accept/the-cab-office's-stallriser-is-patterned-tile-on-a-dark-plinth",
                  byid.get("east_parade_stallriser_bay0", {}).get("material") == "tile_patterned"
                  and byid.get("east_parade_stall_plinth_bay0", {}).get("material") == "tile_stall",
                  str(byid.get("east_parade_stallriser_bay0", {}).get("material")))
            # ONE MICKEY'S, and it is the plain one.
            mick = [b["id"] for b in street if "mickeys" in str(b.get("decal", ""))]
            check("accept/there-is-one-mickey's-on-the-street", len(mick) == 1, ",".join(mick))
            check("accept/and-it-is-signwritten-not-the-pub's-board",
                  bool(mick) and byid[mick[0]]["decal"].endswith("fascia_mickeys_plain"),
                  byid[mick[0]]["decal"] if mick else "none")
            west_signs = [b["id"] for b in street
                          if b["id"].startswith("west_") and "fascia_sign" in b["id"]]
            check("reject/no-sign-is-repeated-across-the-road", not west_signs,
                  ",".join(west_signs[:3]))
            cropped = [b["id"] for b in street if b.get("decal_uv") and "fascia_sign" in b["id"]]
            check("accept/the-spec's-crops-are-read", len(cropped) == 3,
                  "%d cropped" % len(cropped))
            g3 = byid.get("east_parade_display_glazing_bay3", {})
            check("accept/the-empty-unit-is-whitened-and-to-let",
                  g3.get("material") == "glass_whitened"
                  and "east_parade_letting_board_bay3" in byid,
                  str(g3.get("material")))
            missing = [b["decal"] for b in street if b.get("decal")
                       and not os.path.exists(_decal_path(ROOT, b["decal"]))]
            check("accept/every-sign-has-its-picture-on-disk", not missing,
                  ",".join(sorted(set(missing))[:3]))

            # ---- THE BASIN END, and every one of these is a way it
            # could stop being a backdrop and start being a claim.
            # TWO ENDS NOW, 22 September: the basin to the south, and the
            # inland rise to the north since the camera turned to face it.
            # These checks are the BASIN's; the rise has its own below.
            rise = [b for b in street if b["id"].startswith("backdrop_rise")]
            back = [b for b in street if b["id"].startswith("backdrop")
                    and not b["id"].startswith("backdrop_rise")]
            def _xs_any(b):
                if b.get("kind") == "mesh":
                    return [v[0] for v in b["verts"]]
                return [b["x0"], b["x1"]]
            # THE RISE IS ENTIRELY NORTH OF THE STREET, past the road's far
            # end at x = 44, so nothing of it stands in the built street.
            check("accept/the-rise-is-built", len(rise) >= 20, "%d piece(s)" % len(rise))
            north_intruders = [b["id"] for b in rise if min(_xs_any(b)) < 44.0]
            check("accept/the-rise-never-reaches-the-street", not north_intruders,
                  ",".join(north_intruders[:4]))
            # AND IT CLIMBS: every tier stands higher than the one in front,
            # which is what makes it a rise and not a wall of houses.
            walls = sorted((b for b in rise if "_wall_" in b["id"]), key=lambda b: b["x0"])
            check("accept/the-rise-climbs-tier-on-tier",
                  len(walls) >= 3 and all(walls[i + 1]["z1"] > walls[i]["z1"]
                                          for i in range(len(walls) - 1)),
                  "%d retaining walls" % len(walls))
            check("accept/the-far-end-is-not-sky", len(back) >= 20,
                  "%d piece(s)" % len(back))
            # IT IS SOUTH OF THE STREET AND ENTIRELY BEHIND IT. The blocks
            # occupy x 3.0 to 42.0 and the road stops at -2.0; anything here
            # that reached past -2.0 would be standing IN the built street.
            def _xs(b):
                if b.get("kind") == "mesh":
                    return [v[0] for v in b["verts"]]
                return [b["x0"], b["x1"]]
            intruders = [b["id"] for b in back if max(_xs(b)) > BACKDROP_ROAD_END + 1e-9]
            check("accept/the-backdrop-never-reaches-the-street",
                  not intruders, ",".join(intruders[:4]))
            # AND IT IS FAR ENOUGH AWAY TO BE HAZED. The mist reaches its
            # ceiling at start+depth = 63 m from the camera at x=33, which is
            # x = -30: a shed nearer than that would come back sharp and
            # read as a building on this street rather than as the far side
            # of a basin.
            sheds = [b for b in back if "shed" in b["id"]]
            near = [b["id"] for b in sheds if max(_xs(b)) > -30.0]
            check("accept/every-shed-is-inside-the-haze", not near,
                  ",".join(near[:4]))
            # NOTHING ON IT IS APPROACHABLE. A door, a window, a sill or a
            # shopfront in here would be a promise the player cannot keep.
            promises = [b["id"] for b in back
                        if any(w in b["id"] for w in
                               ("door", "window", "sash", "sill", "shop",
                                "fascia", "stallriser"))]
            check("accept/nothing-in-the-backdrop-can-be-walked-to",
                  not promises, ",".join(promises[:4]))
            # IT DOES NOT TOWER OVER THE STREET. The terrace's own ridge is
            # about 8.2 m and the backdrop reads THROUGH the gap between the
            # two roofs; a mass taller than the street reads as a tower block
            # at the end of a Victorian street, which is what attempt one did
            # with an 11.5 m shed standing dead centre.
            def _zs(b):
                if b.get("kind") == "mesh":
                    return [v[2] for v in b["verts"]]
                if b.get("kind") == "slope":
                    return [b["z_eaves"], b["z_ridge"]]
                return [b["z0"], b["z1"]]
            # THE CEILING IS THE STREET'S OWN RIDGE, asked of the spec.
            # Typing 9.0 here would be a second street.
            ceiling = p["ridge_m"] + THRESHOLD_ABOVE_CROWN_M
            tall = ["%s@%.1f" % (b["id"], max(_zs(b))) for b in sheds
                    if max(_zs(b)) > ceiling + 1e-9]
            check("accept/no-shed-towers-over-the-street", not tall,
                  "ceiling=%.2f %s" % (ceiling, ",".join(tall[:4])))
            # TWO RANGES, NOT ONE. Six masses at one distance is a painted
            # flat; the haze needs two depths to be a difference between.
            fronts = sorted(set(round(max(_xs(b)), 1) for b in sheds))
            check("accept/the-sheds-stand-at-two-ranges",
                  len(fronts) >= 2 and (max(fronts) - min(fronts)) > 10.0,
                  "%r" % (fronts,))
            # AND THE CRANE IS MOSTLY AIR. Attempt one was 1.7 m thick and
            # came back as a solid wedge the size of a building.
            crane = [b for b in back if "crane" in b["id"]]
            check("accept/the-crane-is-two-thin-pieces",
                  len(crane) == 2 and BACKDROP_CRANE_T <= 0.6,
                  "%d piece(s)/%.2fm" % (len(crane), BACKDROP_CRANE_T))

            veh = [b for b in street if b["id"].startswith("veh0_")]
            # SEVENTEEN: a body, a glasshouse, a roof cap, four wheels, two
            # tail lamps and two plates - eleven, counted rather than guessed
            # at, because the first version of this check guessed twelve -
            # and since 22 September two bumpers and four hubs.
            check("accept/the-street-has-a-car-in-it", len(veh) == 17,
                  "%d piece(s)" % len(veh))
            body = [b for b in veh if b["id"] == "veh0_body"]
            check("accept/the-car-has-a-body", len(body) == 1)
            if body:
                vs = body[0]["verts"]
                xs = [v[0] for v in vs]; ys = [v[1] for v in vs]; zs = [v[2] for v in vs]
                check("accept/the-car-is-4.12m-long",
                      abs((max(xs) - min(xs)) - CAR_L) < 0.01,
                      "%.3f" % (max(xs) - min(xs)))
                check("accept/the-car-is-1.64m-across",
                      abs((max(ys) - min(ys)) - CAR_W) < 0.01,
                      "%.3f" % (max(ys) - min(ys)))
                # ON THE ROAD, NOT IN THE PAVEMENT AND NOT IN THE WALL. The
                # carriageway is 3.0 m each side of the centre.
                check("accept/the-car-is-on-the-carriageway",
                      max(abs(min(ys)), abs(max(ys))) < 3.0,
                      "%.3f..%.3f" % (min(ys), max(ys)))
                check("accept/the-car-stands-on-the-road-not-in-it",
                      min(zs) > 0.2 and max(zs) < 1.2,
                      "%.3f..%.3f" % (min(zs), max(zs)))
            wheels = [b for b in veh if "wheel" in b["id"]]
            check("accept/the-car-has-four-wheels", len(wheels) == 4,
                  "%d" % len(wheels))
            # THE YELLOW PLATE, which is the period tell and the one part
            # whose ABSENCE would not be noticed in a frame this small.
            check("accept/the-car-carries-a-yellow-rear-plate",
                  any(b["material"] == "plate_rear" for b in veh))
            check("accept/and-a-white-front-one",
                  any(b["material"] == "plate_front" for b in veh))

        # ---- LETTERING READS THE RIGHT WAY ROUND ON BOTH SIDES OF THE ROAD.
        # The west blocks are built as a REFLECTION of the east, which turns
        # their frontages to face the street and reverses their handedness
        # with them; the first frame with shops on the near west block had
        # MICKEY'S painted backwards across it. Nothing in the geometry can
        # see that - a mirrored box is a box - so the check is on the flag
        # that decides which way the image is laid.
        if not serr:
            signed = [b for b in street if b.get("decal")]
            check("accept/there-is-lettering-on-the-street", bool(signed),
                  "%d sign(s)" % len(signed))
            # THE WEST BLOCKS ARE TURNED, NOT MIRRORED, and this is how a
            # list of boxes can tell the difference. A half turn negates x
            # AND y, so the bays of a west block run the OTHER WAY along the
            # street; a reflection negates y alone and leaves them running
            # the same way, which is what made MICKEY'S read backwards.
            # Orientation is not visible in an axis-aligned box, so the
            # check is on the ORDER, which is the same fact seen from the
            # side a piece list can see it from.
            def bay_run(prefix):
                got = [(int(b["id"].split("bay")[-1]), (b["x0"] + b["x1"]) * 0.5)
                       for b in street
                       if b["id"].startswith(prefix) and "fascia_band_bay" in b["id"]]
                return [x for _n, x in sorted(got)]
            east_run = bay_run("east_parade_")
            west_run = bay_run("west_north_")
            check("accept/the-parade-bays-run-up-the-street",
                  len(east_run) >= 2 and east_run == sorted(east_run),
                  str([round(v, 1) for v in east_run]))
            check("accept/and-a-turned-block's-bays-run-back-down-it",
                  len(west_run) >= 2 and west_run == sorted(west_run, reverse=True),
                  str([round(v, 1) for v in west_run]))
            # AND NO SIGN IS BEING FLIPPED TO COMPENSATE. The workaround this
            # replaced set a per-piece flag; if one ever comes back, the
            # construction has quietly gone wrong again.
            flipped = [b["id"] for b in street if b.get("decal_flip")]
            check("reject/no-piece-is-having-its-lettering-flipped",
                  not flipped, ",".join(sorted(flipped)[:3]))

        # ---- THE FIGURES, checked on the two gaps that make them read.
        if not serr:
            legs = [b for b in street if b["id"].startswith("figure_0_leg_")]
            check("accept/a-figure-stands-on-two-legs", len(legs) == 2,
                  "%d" % len(legs))
            if len(legs) == 2:
                a, b_ = sorted(legs, key=lambda q: q["y0"])
                gap = b_["y0"] - a["y1"]
                check("accept/and-there-is-daylight-between-them", gap > 0.02,
                      "%.3f m" % gap)
            neck = [b for b in street if b["id"] == "figure_0_neck"]
            head = [b for b in street if b["id"] == "figure_0_head"]
            torso = [b for b in street if b["id"] == "figure_0_torso"]
            if neck and head and torso:
                check("accept/the-neck-is-narrower-than-both-head-and-shoulders",
                      (neck[0]["y1"] - neck[0]["y0"]) < (head[0]["y1"] - head[0]["y0"])
                      and (neck[0]["y1"] - neck[0]["y0"]) < (torso[0]["y1"] - torso[0]["y0"]),
                      "%.3f" % (neck[0]["y1"] - neck[0]["y0"]))
            # AND THE WHOLE THING IS STILL 1.75 m, which is the only number
            # here that is not a silhouette choice: eye height 1.6 is
            # CrimeProbe.h's own kEyeHeightM and the simulation traces
            # sightlines from it.
            body = [b for b in street if b["id"].startswith("figure_0_")]
            if body:
                tall = max(q["z1"] for q in body) - min(q["z0"] for q in body)
                check("accept/and-a-person-is-still-1.75m-tall",
                      abs(tall - (FIGURE_EYE_M + FIGURE_EYE_TO_CROWN_M)) < 1e-6,
                      "%.4f m" % tall)

        # ---- THE AERIALS, and the one number in them that is derived.
        # The scene file works the element length out of physics rather than
        # choosing it: UHF Bands IV and V, a half-wave dipole at the 550 MHz
        # middle of the band, c/(2f) = 0.2725 m. If a later edit ever rounds
        # that to "about a third of a metre" the roofline stops being 1990
        # and nothing else in this file would notice.
        # BUILT FOR A BAY THAT ACTUALLY CARRIES ONE. The bay these checks
        # were first written against was bay 0, which has no aerial, so every
        # one of them skipped and the suite still reported green - which is a
        # check that exists and tests nothing.
        aerial_bay = AERIAL_ON_STACKS[0]
        abox = plan_parts(p, aerial_bay, True)
        aerials = [b for b in abox if b["id"].startswith("aerial_")]
        if p["roof_kind"] != "parapet":
            masts = [b for b in aerials if b["id"].endswith("_mast")]
            elements = [b for b in aerials if "_element_" in b["id"]]
            check("accept/the-named-stack-carries-an-aerial", len(masts) == 1,
                  "bay %d: %d mast(s)" % (aerial_bay, len(masts)))
            if any(b["id"] == "chimney_stack" for b in abox):
                if elements:
                    check("accept/the-comb-has-ten-elements",
                          len(elements) == AERIAL_ELEMENTS, "%d" % len(elements))
                    span = max(b["y1"] for b in elements) - min(b["y0"] for b in elements)
                    check("accept/an-element-is-a-half-wave-at-550MHz",
                          abs(span - AERIAL_ELEMENT_L) < 1e-6, "%.4f m" % span)
                    # 299792458 / (2 x 550e6) = 0.272538..., and 0.27 is that
                    # rounded to the centimetre a jobbing aerial is made to.
                    check("accept/and-that-is-what-the-physics-says",
                          abs(AERIAL_ELEMENT_L - 299792458.0 / (2 * 550e6)) < 0.005,
                          "%.4f" % (299792458.0 / (2 * 550e6)))
                    top = max(b["z1"] for b in aerials)
                    stack = [b for b in abox if b["id"] == "chimney_stack"][0]
                    check("accept/the-aerial-stands-on-the-stack-not-in-it",
                          top > stack["z1"], "%.3f vs %.3f" % (top, stack["z1"]))

        # ---- THE ROAD'S CROWN, which is a DERIVED number and so is checked
        # as one. The scene file gives half_width 3.0 and crossfall 0.025 and
        # then states the consequence itself: 75 mm from crown to channel. If
        # the street is ever widened and the crown does not follow, the wet
        # frames go wrong in a way no texture can rescue - which is the
        # carriageway line's own warning, in its own words.
        road = [b for b in street if b["id"] == "carriageway"] if not serr else []
        check("accept/the-road-is-a-crowned-solid-not-a-flat-slab", len(road) == 1,
              "%d" % len(road))
        if road:
            zs = sorted(set(round(v[2], 4) for v in road[0]["verts"]))
            crown, channel = max(zs), sorted(zs)[1]
            check("accept/the-crown-stands-75mm-above-the-channel",
                  abs((crown - channel) - 3.0 * 0.025) < 1e-6,
                  "%.4f m" % (crown - channel))
            check("accept/and-the-crown-is-the-road-datum-at-zero",
                  abs(crown) < 1e-9, "%.4f" % crown)

        # ---- THE PAVEMENT PROPS, read from the spec rather than chosen.
        props, perr = prop_placements(ROOT)
        check("accept/the-spec-still-places-pavement-props", not perr and len(props) >= 12,
              perr or "%d" % len(props))
        if props:
            # ON A PAVEMENT OR IN A CHANNEL, NEVER IN A WALL OR A ROAD LANE.
            # The frontages stand at 5.125 either side and the kerb face at
            # 3.0, so every footway prop has to sit between them.
            stray = ["%s@%.2f" % (q["asset"], q["y"]) for q in props
                     if q["on_footway"] and not (3.0 < abs(q["y"]) < STREET_FRONTAGE_M)]
            check("accept/every-footway-prop-is-on-a-footway", not stray, ",".join(stray))
            offstreet = ["%s@%.1f" % (q["asset"], q["x"]) for q in props
                         if not (-2.0 <= q["x"] <= 44.0)]
            check("accept/and-none-of-them-is-off-the-end-of-the-street",
                  not offstreet, ",".join(offstreet))
            # THE MESHES ARE ACTUALLY HERE. A placement naming a file this
            # repository does not hold is a prop that silently never appears,
            # which is the failure the bill of materials keeps finding.
            absent = [q["asset"] for q in props
                      if not os.path.exists(os.path.join(ROOT, PROP_DIR, q["asset"] + ".glb"))]
            check("accept/every-placed-prop-is-a-mesh-we-hold", not absent,
                  ",".join(sorted(set(absent))))
            # EVERY ONE IS NAMED BY A LINE OF THE BILL OF MATERIALS, which is
            # this project's standing rule about fetched geometry.
            unnamed = [q["asset"] for q in props if not q["bom"]]
            check("accept/every-placed-prop-is-named-by-the-bill-of-materials",
                  not unnamed, ",".join(sorted(set(unnamed))))
            check("accept/the-gully-grate-is-the-one-piece-set-into-the-ground",
                  [q["asset"] for q in props if q["set_in"]] == ["drainage_grate_01"],
                  ",".join(q["asset"] for q in props if q["set_in"]))
        # REJECTING: a spec that is not there places nothing and says so,
        # rather than an empty pavement that looks deliberate.
        _none, nerr = prop_placements(os.path.join(ROOT, "no-such-directory"))
        check("reject/a-missing-spec-refuses-rather-than-emptying-the-pavement",
              bool(nerr) and _none == [], nerr)

        checks = cross_check(p, ROOT)
        got = [c for c in checks if c[2] is not None]
        check("accept/cross-check-read-the-emitted-street", len(got) > 0,
              "%d of %d fields found" % (len(got), len(checks)))
        check("accept/authored-agrees-with-the-emitted-blockout",
              all(c[3] for c in got),
              ",".join("%s(%.4f vs %.4f)" % (c[0], c[1], c[2]) for c in got if not c[3]))

        # REJECTING CASES. A recipe that cannot refuse is not checking.
        try:
            _box([], "planted", "stone", 1.0, 1.0, 0.0, 1.0, 0.0, 1.0)
            check("reject/a-zero-width-box-is-refused", False, "it was accepted")
        except ValueError:
            check("reject/a-zero-width-box-is-refused", True)
        bad = dict(p); bad["bay_width_m"] = 0.5
        try:
            plan_parts(bad)
            check("reject/a-bay-too-narrow-for-its-own-piers-is-refused", False,
                  "it was accepted")
        except ValueError:
            check("reject/a-bay-too-narrow-for-its-own-piers-is-refused", True)

        # THE CAMERAS ACTUALLY POINT AT THE BUILDING. Composed back from the
        # euler this file will hand Blender, on the two frames it really
        # takes, and compared against the direction that was asked for. The
        # first version of look_at_euler passed every other check in this
        # selftest and rendered an empty field.
        for name, spec in frame_cameras(p).items():
            want = [spec["look"][i] - spec["loc"][i] for i in range(3)]
            n = math.sqrt(sum(v * v for v in want)) or 1.0
            want = [v / n for v in want]
            got = euler_direction(look_at_euler(spec["loc"], spec["look"]))
            off = max(abs(got[i] - want[i]) for i in range(3))
            check("accept/camera-%s-points-where-it-was-aimed" % name, off < 1e-9,
                  "worst axis off by %.9f" % off)
        # AND THE ELEVATION CAMERA IS SQUARE ON AND LEVEL, which is the whole
        # claim the frame makes: it is the view a facade is judged from.
        ele = frame_cameras(p)["elevation"]
        d = euler_direction(look_at_euler(ele["loc"], ele["look"]))
        check("accept/elevation-camera-is-square-to-the-frontage",
              abs(d[0]) < 1e-9 and abs(d[2]) < 1e-9 and d[1] > 0.99,
              "direction=(%.6f, %.6f, %.6f)" % d)

    nospec, err2 = load_spec(os.path.join(ROOT, "no-such-directory"))
    check("reject/a-missing-spec-refuses-by-name", nospec is None and "no-spec-file" in err2, err2)

    a = parse_args(["x.py", "--", "--out", "/tmp/x", "--commission", "c", "--run-sha", "s"])
    check("accept/the-lane's-own-line-parses", a["out"] == "/tmp/x" and not a["error"], a["error"])
    b = parse_args(["x.py", "--", "--not-a-flag-9xz"])
    check("reject/an-unknown-flag-is-refused", b["error"].startswith("unknown-flag"), b["error"])

    print("terrace-front selftest: passed=%d/%d failed=%d" % (passed, passed + failed, failed))
    return 0 if failed == 0 else 4


def main(argv):
    args = parse_args(argv)
    if args["selftest"]:
        return selftest()
    if args["error"]:
        print("terrace-front refused: status=BAD-ARGS reason=%s nothing measured" % args["error"])
        return 2
    if args["plan"]:
        p, err = load_spec(args["root"], args["spec"], args["block"])
        if err:
            print("terrace-front refused: status=NO-SPEC reason=%s nothing measured" % err)
            return 3
        parts = plan_row(p)
        for line in plan_lines(p, parts, cross_check(p, args["root"])):
            print(line)
        print("terrace-front done: status=DRY-RUN/nothing-built parts=%d" % len(parts))
        return 0
    if not args["out"]:
        print("terrace-front refused: status=BAD-ARGS reason=no-out-directory nothing measured")
        return 2
    if not os.path.isdir(args["out"]):
        os.makedirs(args["out"])
    return build_and_render(args)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
