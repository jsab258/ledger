"""Raw data of the front-doors-all target: the photographs read, every pixel measurement with its box, the palette, the furniture,
the wear, the per-house choices, the owed lines. make_target.py turns this into target.json; make_doc.py writes TARGET.md from that.
All lengths in millimetres unless a name says metres. No em dashes anywhere (Jafar's lines), no real maker's name anywhere."""
import sys

sys.dont_write_bytecode = True

# --------------------------------------------------------------------------------------------------------------------------
# 1. The photographs. "id" is this target's; "gid" the Geograph number. Photographs are for measuring only, never placed in the
#    game, never traced into a texture, never fed to an image model. Every page below was opened by this writer on 13 Oct 2026.
# --------------------------------------------------------------------------------------------------------------------------
PHOTOS = {
    "P1": {"src": "front-door target (3.1)", "title": "Front door, 69 Lower Brimley Road, Teignmouth", "author": "Robin Stott",
           "licence": "CC BY-SA 2.0", "taken": "2012-05-06", "period": "later; the type is the 1890s four-panel door",
           "used_for": "T1 and F1 (kept), the bell push's plain oblong, the brass plate, the rim night latch",
           "preview": "production/previews/cloud-week/refs/front-door/door-photo-01-teignmouth-four-panel-red.jpg", "reached_by_me": "preview only (3.1's page not reachable then)"},
    "P2": {"src": "front-door target (3.1)", "title": "Doorway Philip Lane Tottenham London England", "author": "Acabashi",
           "licence": "CC BY-SA 4.0", "taken": "2024-02-03", "period": "later; an unrestored door of the old type",
           "used_for": "F2 six-panel, centre knob, plugged keyhole, wear",
           "preview": "production/previews/cloud-week/refs/front-door/door-photo-02-tottenham-six-panel-black.jpg", "reached_by_me": "preview only"},
    "D1": {"gid": "7292055", "title": "Carrville Terrace", "author": "David M Clark", "licence": "CC BY-SA 2.0", "taken": "1975-01-22",
           "url": "https://www.geograph.org.uk/photo/7292055", "size_px": [534, 800], "period": "the period (1975)",
           "shows": "two doors in white frames under painted-cement hoods, each with a transom light: a deep teal door of two long panels, and a blue-grey door of four stacked lights with a low letter plate in its bottom rail; a white painted step",
           "used_for": "F3 two long panels, the low letter plate, the stacked lights (vertical rows only: the leaves are seen at an angle from the right)",
           "preview": "d1-durham-carrville-terrace-1975-two-doors.jpg"},
    "D2": {"gid": "2238747", "title": "Terraced housing in Railway Street", "author": "P L Chadwick", "licence": "CC BY-SA 2.0", "taken": "1987-08-09",
           "url": "https://www.geograph.org.uk/photo/2238747", "size_px": [800, 529], "period": "the period (1987)",
           "shows": "a stone terrace: a mustard door of three long narrow lights, a khaki flush door with a tall slit light, a lever handle and a small plate under the slit (white frame, dark transom), a white door with an oval plaque",
           "used_for": "F4 three long lights, F5 slit-light flush door, the lever handle, the slit plate",
           "preview": "d2-railway-street-1987-three-doors.jpg"},
    "D3": {"gid": "2321423", "title": "Terraced House - Ratcliffe Street, Levenshulme", "author": "Anthony Parkes", "licence": "CC BY-SA 2.0", "taken": "1994-06-10",
           "url": "https://www.geograph.org.uk/photo/2321423", "size_px": [658, 1024], "period": "the period (1994); the door is a 1930s type kept in 1994",
           "shows": "a brick terrace front square on: a white door of four stacked lights with nets, a leaded diamond fanlight, a dark vertical pull handle on the left stile",
           "used_for": "T2 four stacked lights, the leaded fanlight, the bar pull",
           "preview": "d3-levenshulme-ratcliffe-street-1994-four-light-door.jpg"},
    "D4": {"gid": "689253", "title": "Nos. 34, 32 and 30, Frederick Street, Barnoldswick", "author": "Dr Neil Clifton", "licence": "CC BY-SA 2.0", "taken": "1990-04-10",
           "url": "https://www.geograph.org.uk/photo/689253", "size_px": [640, 550], "period": "the period (1990), black and white; the page says 'mostly modernised with double glazing'",
           "shows": "three doors of a stone terrace: a pale flush door with a tall slit light, a dark door in a white frame with a transom and a low plate at its foot, a white moulded door with a small arched light, an oblong letter plate and two embossed panels",
           "used_for": "T3 moulded modern door, the slit light's height, the low letter plate",
           "preview": "d4-barnoldswick-frederick-street-1990-three-doors.jpg"},
    "D5": {"gid": None, "title": "Hazlehead I, Provost Graham Avenue (SC 1141987)", "author": "Miles Glendinning (Tower Block Archive, Edinburgh College of Art)",
           "licence": "CC BY 4.0", "taken": "1987",
           "url": "https://commons.wikimedia.org/wiki/File:Hazlehead_I,_Provost_Graham_Avenue_(SC_1141987).png", "size_px": [4000, 2646],
           "period": "the period (1987); a flush door of a council flat's landing, the same leaf the council fitted to its houses",
           "shows": "an olive-green flush door with an oblong letter plate at its middle, a lever handle on the right stile, a spyhole above the plate, white frame with a reeded transom and reeded sidelight",
           "used_for": "F6 council flush door, the chrome-look oblong plate, the lever handle, reeded glass",
           "preview": "d5-aberdeen-hazlehead-1987-council-flush-door.jpg", "read_by_me": "file page via the Commons API (date 1987, CC BY 4.0, uploaded with the University of Edinburgh); the 1920 px copy was measured"},
    "D6": {"gid": "7982731", "title": "Rensburg Street, Kingston upon Hull", "author": "Bernard Sharp", "licence": "CC BY-SA 2.0", "taken": "1982-03-19",
           "url": "https://www.geograph.org.uk/photo/7982731", "size_px": [1024, 660], "period": "the period (1982)",
           "shows": "a Hull terrace in 1982: recessed doorways under painted hoods in blue and red, a bright blue door with a white numeral painted on it, a black door with a yellow foot, painted brick surrounds",
           "used_for": "the bright blue and the red door colours (a box inside the leaf), the painted numeral, the hood", "preview": "d6-hull-rensburg-street-1982-blue-door.jpg"},
    "D7": {"gid": "3462921", "title": "Abbey Street, Kingston upon Hull", "author": "Bernard Sharp", "licence": "CC BY-SA 2.0", "taken": "1986-06-08",
           "url": "https://www.geograph.org.uk/photo/3462921", "size_px": [1024, 661], "period": "the period (1986)",
           "shows": "the same kind of street, arched recessed doorways with a rendered arch, a lime-green door, red and brown doors, a blue painted gutter",
           "used_for": "the lime-green and brown door colours, the recess", "preview": "d7-hull-abbey-street-1986-arched-doorways.jpg"},
    "D8": {"gid": "3462940", "title": "Brazil Street, Kingston upon Hull", "author": "Bernard Sharp", "licence": "CC BY-SA 2.0", "taken": "1986-06-08",
           "url": "https://www.geograph.org.uk/photo/3462940", "size_px": [1024, 669], "period": "the period (1986)",
           "shows": "a street of Hull terraces with brightly painted frames, canopies and doors (red, blue, yellow, sky blue)",
           "used_for": "the finding that these streets paint frames and doors in bright colours, set against Jafar's white-frames ruling (owed line 2); no number taken from it",
           "preview": "d8-hull-brazil-street-1986-painted-frames.jpg"},
    "D9": {"gid": "2876894", "title": "Newburn Council Houses", "author": "Kevin Hall", "licence": "CC BY-SA 2.0", "taken": "1989-08-01",
           "url": "https://www.geograph.org.uk/photo/2876894", "size_px": [1024, 686], "period": "the period (mid to late 1989)",
           "shows": "1960s council houses: flush doors under small concrete canopies, one painted turquoise",
           "used_for": "the council turquoise (a box inside the leaf)", "preview": "d9-newburn-council-houses-1989-turquoise-door.jpg"},
    "D10": {"gid": "3911943", "title": "Old Town, Poole: in search of the boot scraper", "author": "Mike Searle", "licence": "CC BY-SA 2.0", "taken": "2014-03-30",
            "url": "https://www.geograph.org.uk/photo/3911943", "size_px": [640, 427],
            "period": "later (2014). The object is a cast-iron scraper set by a town house's step in the 19th century and left in place; iron fittings of this kind were never renewed, so its form is the period's",
            "shows": "a cast-iron boot scraper beside a painted step: a straight blade between two end standards with scroll tops",
            "used_for": "the boot scraper's form (the sizes are Judgement, the photograph has no scale in its plane)", "preview": "d10-poole-boot-scraper-2014.jpg"},
}

BOOKS = {
    "H": {"title": "P. N. Hasluck, Cassell's Carpentry and Joinery", "year": 1907, "pages": "pp.312-317, Figs. 1015-1039 (ledged, ledged and braced, framed and braced doors)",
          "url": "https://archive.org/details/cassellscarpentr00hasl", "how_read": "the OCR text (djvu.txt) of the page range; the page images were not opened by me",
          "says": "boards 3 in to 7 in wide, 3/4 in to 1 1/4 in thick, grooved and tongued, edges beaded or chamfered to a V joint; ledges nailed across with wrought-iron nails driven from the face and clenched; hook-and-plate hinges; the frame square with no beads or stops, the door overhanging"},
    "E": {"title": "George Ellis, Modern Practical Joinery", "year": 1902, "pages": "pp.92, 93 (via the 3.1 target)", "how_read": "through production/cloud-week/targets/front-door/TARGET.md"},
    "R": {"title": "J. W. Riley, A Manual of Carpentry and Joinery", "year": 1905, "pages": "p.357 (via the 3.1 target)", "how_read": "through production/cloud-week/targets/front-door/TARGET.md"},
}

# --------------------------------------------------------------------------------------------------------------------------
# 2. Pixel measurements. Every box is [x0, y0, x1, y1] in the photograph's own pixels as the file named in `file` (the largest
#    size Geograph serves, or the Commons file reduced to 1920 px wide). A reviewer reproduces a row by cutting that box.
# --------------------------------------------------------------------------------------------------------------------------
MEAS = {
    # D3, left door of Ratcliffe Street (kind T2). Square on; 10.14 mm a pixel (the visible face of frame set T, 1927.6 / 190 px).
    "D3_leaf": {"photo": "D3", "box": [45.75, 443.75, 124.25, 633.75], "leaf_mm": [772.0, 1927.6], "error_px": 1.5,
                "what": "the door leaf: left stile's outer edge, right stile's outer edge, top of the top rail, foot of the bottom rail"},
    "D3_rows": {"photo": "D3", "rows_px": {"light1": [449.5, 488.75], "light2": [491.75, 531.25], "light3": [534.25, 574.25], "light4": [577.0, 613.75]},
                "what": "the four lights, top and foot row of each (the glass between the bars)", "error_px": 1.5},
    "D3_stiles": {"photo": "D3", "left_px": [45.75, 55.5], "right_px": [114.5, 124.25], "what": "the two stiles (outer edge to the glass)", "error_px": 1.5},
    "D3_handle": {"photo": "D3", "box": [46.0, 498.25, 52.0, 524.25], "what": "the dark vertical pull handle on the left stile", "error_px": 1.5},
    "D3_fanlight": {"photo": "D3", "box": [40.0, 376.0, 122.0, 436.0], "what": "the leaded fanlight over the leaf (taller than the T frame's 267 mm light: the type is taken, not the height)", "error_px": 2.0},
    # D4, right door of Frederick Street (kind T3). 21.7 mm a pixel (visible face of frame set T, 1927.6 / 89 px).
    "D4_T3_leaf": {"photo": "D4", "box": [545.0, 345.0, 581.0, 434.0], "leaf_mm": [772.0, 1927.6], "error_px": 1.5, "what": "the white moulded door's outer edge"},
    "D4_T3_light": {"photo": "D4", "box": [559.0, 363.0, 568.0, 384.0], "what": "the small arched light (its square foot)", "error_px": 1.0},
    "D4_T3_plate": {"photo": "D4", "box": [558.0, 392.5, 570.0, 395.6], "what": "the oblong letter plate", "error_px": 1.0},
    "D4_T3_upper": {"photo": "D4", "box": [550.6, 350.6, 577.0, 388.7], "what": "the upper embossed panel's outline", "error_px": 1.5},
    "D4_T3_lower": {"photo": "D4", "box": [555.0, 400.0, 574.0, 419.0], "what": "the lower embossed panel's inner outline", "error_px": 1.5},
    "D4_T3_handle": {"photo": "D4", "box": [581.0, 394.0, 583.0, 398.0], "what": "the small lever at the lock edge", "error_px": 1.5},
    "D4_slit": {"photo": "D4", "box": [357.0, 340.0, 363.0, 383.75], "leaf_box": [345.0, 332.0, 370.0, 408.0], "what": "the pale door's slit light and its leaf (the leaf is seen a little obliquely: rows only)", "error_px": 1.5},
    "D4_low_plate": {"photo": "D4", "box": [392.0, 405.0, 402.0, 408.0], "leaf_box": [384.0, 335.0, 407.0, 410.0], "what": "the low letter plate at the dark door's foot (rows only)", "error_px": 1.0},
    # D2 middle door (kind F5). Square on; 23.8 mm a pixel (visible face of frame set F, 1960.6 / 82.5 px).
    "D2_F5_leaf": {"photo": "D2", "box": [561.0, 280.5, 595.5, 363.0], "leaf_mm": [797.2, 1960.6], "error_px": 1.5, "what": "the khaki flush door, top edge below the transom rail, foot at the step"},
    "D2_F5_slit": {"photo": "D2", "box": [574.0, 287.0, 582.8, 324.5], "what": "the slit light", "error_px": 1.0},
    "D2_F5_plate": {"photo": "D2", "box": [572.5, 327.5, 583.5, 329.5], "what": "the small pale plate under the slit", "error_px": 1.0},
    "D2_F5_handle": {"photo": "D2", "box": [561.5, 315.5, 565.0, 319.0], "what": "the small pale handle at the left stile", "error_px": 1.0},
    # D2 left door (kind F4). 26.6 mm a pixel (the visible width 797.2 = 30 px).
    "D2_F4_cols": {"photo": "D2", "leaf_x_px": [374.5, 404.5], "light_x_px": [[381.5, 387.5], [389.5, 396.0], [398.5, 404.5]], "bar_x_px": [[388.0, 389.5], [396.5, 398.0]],
                   "what": "the three long narrow lights and the two bars between them, across; the leaf's right edge is hidden in shadow", "error_px": 1.0},
    "D2_F4_top": {"photo": "D2", "rows_px": {"top_rail": [270.0, 273.0]}, "what": "the top rail", "error_px": 1.0},
    # D5, Hazlehead flush door (kind F6). 1920 px copy; 2.37 mm a pixel (the leaf, shown whole: 1981 / 835 px).
    "D5_leaf": {"photo": "D5", "box": [450.0, 137.0, 775.0, 970.0], "leaf_mm": [762.0, 1981.0], "error_px": 3.0, "what": "the leaf: left edge, right edge, top, the floor line"},
    "D5_plate": {"photo": "D5", "box": [561.0, 570.0, 668.0, 600.0], "what": "the oblong letter plate", "error_px": 3.0},
    "D5_handle": {"photo": "D5", "box": [725.0, 582.5, 770.0, 597.5], "what": "the lever handle on the right stile", "error_px": 3.0},
    "D5_spy": {"photo": "D5", "box": [595.0, 330.0, 630.0, 342.0], "what": "the round spyhole, its place only (blurred)", "error_px": 5.0},
    # D1, Carrville Terrace (vertical rows only; the leaves are seen obliquely from the right). 13.2 mm a pixel (leaf 1981 / 150 px).
    "D1_L": {"photo": "D1", "leaf_rows_px": [517.0, 667.0], "transom_rows_px": [480.0, 509.0], "what": "the teal door: leaf top and foot, the transom light", "error_px": 1.5},
    "D1_R": {"photo": "D1", "leaf_rows_px": [517.0, 667.0], "light_rows_px": [[517.0, 548.0], [552.0, 582.0], [588.0, 617.0], [622.0, 655.0]], "plate_rows_px": [659.0, 662.5],
             "what": "the blue-grey door: the four lights and the low plate", "error_px": 1.5},
}

# Paint colours measured as the median of a box inside the leaf (film of 1975 to 1994, so a hue family, never a target value).
COLOUR_BOXES = {
    "D1_L_teal": {"photo": "D1", "box": [48, 525, 66, 640], "median_rgb": [28, 39, 29], "note": "shade; almost black-green"},
    "D2_F4_mustard": {"photo": "D2", "box": [375, 282, 380, 330], "median_rgb": [142, 136, 39], "note": "yellow-olive"},
    "D2_F5_khaki": {"photo": "D2", "box": [563, 290, 572, 325], "median_rgb": [136, 132, 83], "note": "grey-olive"},
    "D5_olive": {"photo": "D5", "box": [470, 200, 740, 500], "median_rgb": [114, 102, 65], "note": "olive, inside; flat"},
    "D6_blue": {"photo": "D6", "box": [838, 335, 850, 415], "median_rgb": [26, 67, 117], "note": "strong blue"},
    "D7_lime": {"photo": "D7", "box": [648, 400, 664, 560], "median_rgb": [119, 119, 41], "note": "lime-olive"},
    "D9_turquoise": {"photo": "D9", "box": [393, 620, 399, 630], "median_rgb": [22, 108, 126], "note": "turquoise, a small box low on the leaf"},
}

# --------------------------------------------------------------------------------------------------------------------------
# 3. Palette. sRGB, plain name, weight in the street, source. The Hook sheet and the 3.1 colours first (they win for the street's look).
# --------------------------------------------------------------------------------------------------------------------------
PALETTE = [
    {"id": "black", "name": "gloss black, faintly blue", "srgb": [35, 36, 40], "class": "dark_neutral", "src": "3.1 (P2 median 39,40,45)"},
    {"id": "dark_green", "name": "dark green", "srgb": [28, 59, 41], "class": "dark_chroma", "src": "3.1; the shopfront kit's door green"},
    {"id": "maroon", "name": "maroon, the sheet's deep red", "srgb": [92, 26, 32], "class": "dark_chroma", "src": "3.1; terrace-front.py reads the sheet's doors as 'a deep teal and a deep red'"},
    {"id": "navy", "name": "dark blue", "srgb": [24, 38, 78], "class": "dark_neutral", "src": "3.1"},
    {"id": "brown", "name": "dark brown", "srgb": [74, 48, 34], "class": "dark_neutral", "src": "3.1"},
    {"id": "deep_teal", "name": "deep teal, the sheet's other door", "srgb": [22, 64, 66], "class": "dark_chroma", "src": "terrace-front.py comment on the Hook sheet; D1 left door (a teal gone dark in shade, median 28,39,29); value Judgement"},
    {"id": "cream", "name": "cream", "srgb": [222, 212, 184], "class": "light", "src": "3.1 frame cream; D3's door reads white-cream"},
    {"id": "white_gloss", "name": "white gloss (plastic-look moulded door)", "srgb": [226, 224, 214], "class": "light", "src": "3.1 frame white; D3, D4, D2 white doors"},
    {"id": "council_turquoise", "name": "council turquoise", "srgb": [30, 112, 128], "class": "bright", "src": "D9 box median (22,108,126) lifted for film; value Judgement"},
    {"id": "olive", "name": "olive (the 1960s council colour)", "srgb": [114, 102, 65], "class": "mid", "src": "D5 box median"},
    {"id": "khaki", "name": "khaki", "srgb": [128, 124, 78], "class": "mid", "src": "D2 middle door box median (136,132,83) darkened a little for film"},
    {"id": "mustard", "name": "mustard", "srgb": [140, 128, 40], "class": "bright", "src": "D2 left door box median (142,136,39)"},
    {"id": "bright_blue", "name": "bright blue (Hull 1980s)", "srgb": [30, 78, 140], "class": "bright", "src": "D6 box median (26,67,117) lifted for film; value Judgement"},
    {"id": "lime", "name": "lime green (Hull 1980s)", "srgb": [112, 118, 44], "class": "bright", "src": "D7 box median (119,119,41)"},
    {"id": "red", "name": "bright red", "srgb": [201, 41, 32], "class": "bright", "src": "3.1 (P1 median)"},
    {"id": "varnish", "name": "natural varnished timber (a stained door)", "srgb": [122, 76, 40], "class": "mid", "src": "Judgement: no photograph read shows one on these streets"},
]
FRAME_COLOURS = [
    {"id": "white", "name": "gloss white, yellowed", "srgb": [226, 224, 214], "src": "3.1 (P1 240,239,245 fresh; P2 222,225,229 old); the Hook sheet's surrounds are white"},
    {"id": "white_grimy", "name": "white, grimed", "srgb": [208, 205, 192], "src": "3.1 white x 0.92, the windows target's white_grimy"},
]
# 3.1 allowed a cream frame (weight 0.3). Dropped here: the Hook sheet's door surrounds are white and Jafar's ruling of 3 October is "windows with white frames";
# the fanlight is a window. See owed line 2.

# --------------------------------------------------------------------------------------------------------------------------
# 4. Wear. Numbers quoted from the wear target (production/cloud-week/targets/wear/target.json) so the PC takes the layer's own masks.
# --------------------------------------------------------------------------------------------------------------------------
CONDITIONS = {
    "kept": {"paint_flake_share": 0.03, "paint_fade": 0.3, "crazing": "none", "chips": "0 to 2 chips of 8 to 15 mm on the leaf's lower arrises",
             "bottom_rail": "clean; a dark splash band to 0.24 m only", "kick_marks": "0 to 2 scuffs, 20 to 40 mm, on the bottom rail",
             "polish": "the brass is polished: a bright ring 12 mm wide round the letter plate's flap and the knob (kept bright), the rest dull gold",
             "frame": "white, sound, a yellowing at the foot", "roughness": 0.35, "src": "wear target paint_flake range low end 0.03; 3.1 'new' 0.35"},
    "tired": {"paint_flake_share": 0.063, "paint_fade": 0.6, "crazing": "cells 2 to 4 mm over 30 per cent of the leaf (P2's)",
              "chips": "4 to 8 chips of 10 to 40 mm on arrises and the mouldings' lower lips, bare wood or undercoat showing",
              "bottom_rail": "darkened by splash to 0.33 m, a paint loss of 20 per cent on the rail",
              "kick_marks": "3 to 6 scuffs and one boot print band 60 mm high at the lock side",
              "polish": "brass dull; a brighter ring where the flap is pushed (10 to 14 mm wide), a dark grease halo 0.17 m round the handle (handle_wear)",
              "frame": "yellowed, a hairline crack at the stop's foot", "roughness": 0.55, "src": "wear target paint_flake typical 0.063, handle_wear halo p50 0.17 m; 3.1 'weathered' 0.55"},
    "neglected": {"paint_flake_share": 0.40, "paint_fade": 1.0, "crazing": "cells 2 to 4 mm over the whole leaf (P2's old door)",
                  "chips": "12 to 20 chips and two sheets of 80 to 250 mm off the rail and stile feet, grey bare timber below",
                  "bottom_rail": "rotted: an eroded notch 25 mm high and 60 to 200 mm wide, 3 mm deep, in the lower arris at the hinge side, bare grey wood, a soft dark wet stain to 0.5 m",
                  "kick_marks": "8 to 15 scuffs and dents, a split 120 mm long in the bottom panel's lower edge",
                  "polish": "brass dark and green-brown; the plate's flap rubbed bright in a ring 10 mm wide only where fingers push; no polish elsewhere",
                  "frame": "peeling down to a darker undercoat, a dirty foot", "roughness": 0.65, "src": "wear target paint_flake neglected up to 0.40; 3.1 weather side low down 0.65"},
}
WEAR_KINDS_USED = ["paint_flake", "paint_fade", "handle_wear", "wall_foot_splash", "iron_wear"]
WEAR_NOT_COVERED = [
    "crazing in 2 to 4 mm cells: the layer's paint_flake crazing cells are 0.14 to 0.23 m (render); a timber-door tile is owed",
    "kick marks and boot prints on a bottom rail: not a kind of the layer (the nearest is wall_foot_splash)",
    "a letter plate's bright polish ring: not a kind (the layer's handle_wear is a dark grease halo); owed as a small brightening mask in the brass's own material",
    "rot as geometry (the eroded notch): the layer is a texture, so the notch is a build parameter of the door",
]

# --------------------------------------------------------------------------------------------------------------------------
# 5. Per-house choices. house id -> kind, paint, frame, condition, furniture, number form, and why. Street order is by x on each side.
# --------------------------------------------------------------------------------------------------------------------------
HOUSE_CHOICES = {
    "east_parade_bay0": {"kind": "F1", "paint": "maroon", "frame": "white_grimy", "condition": "tired",
                         "furniture": {"letter_plate": "LP1", "handle": "HD1", "latch": "LK2", "knocker": "KN0", "bell": "BL0", "number": "NM1", "scraper": "BS0"},
                         "why": "Mickey's side door, the four-panel door as built in 3.1 (the recipe already gave it four panels and a knob: a plain slab failed a review on 4 October); maroon is the sheet's deep red"},
    "east_parade_bay1": {"kind": "F2", "paint": "black", "frame": "white", "condition": "kept",
                         "furniture": {"letter_plate": "LP2", "handle": "HD1", "latch": "LK2", "knocker": "KN0", "bell": "BL0", "number": "NM1", "scraper": "BS0"},
                         "why": "the fishmonger's flat, an old six-panel door as P2 shows; kept because a working shop keeps its own door"},
    "east_parade_bay2": {"kind": "F1", "paint": "dark_green", "frame": "white", "condition": "kept",
                         "furniture": {"letter_plate": "LP1", "handle": "HD1", "latch": "LK2", "knocker": "KN0", "bell": "BL0", "number": "NM0", "scraper": "BS0"},
                         "why": "Rita's: the shopfront kit's own side door (a fanlight over it); four-panel as built, dark green against the cream painted front (the 4 October reading of the sheet's third house)"},
    "east_parade_bay3": {"kind": "F4", "paint": "brown", "frame": "white_grimy", "condition": "neglected",
                         "furniture": {"letter_plate": "LP5", "handle": "HD2b", "latch": "LK0", "knocker": "KN0", "bell": "BL0", "number": "NM0", "scraper": "BS0"},
                         "why": "the empty unit to let (whitewashed): its flat is empty too; an old three-light glazed door, neglected, with a low plate in its bottom rail"},
    "east_parade_bay4": {"kind": "F6", "paint": "council_turquoise", "frame": "white", "condition": "tired",
                         "furniture": {"letter_plate": "LP4", "handle": "HD2a", "latch": "LK0", "knocker": "KN0", "bell": "BL0", "number": "NM0", "scraper": "BS0"},
                         "why": "the launderette's flat, modernised (the windows target gave it replacement windows): a council-style flush door in the 1980s turquoise that D9 shows; the only bright door on the east side"},
    "east_chandler_bay0": {"kind": "F5", "paint": "navy", "frame": "white", "condition": "kept",
                           "furniture": {"letter_plate": "LP7", "handle": "HD2b", "latch": "LK0", "knocker": "KN0", "bell": "BL0", "number": "NM0", "scraper": "BS0"},
                           "why": "the chandler's flat, modernised (replacement windows, a metal refit below): a flush door with a slit light as D2 and D4 show"},
    "west_south_bay2": {"kind": "T1", "paint": "deep_teal", "frame": "white_grimy", "condition": "tired",
                        "furniture": {"letter_plate": "LP1", "handle": "HD0", "latch": "LK1", "knocker": "KN0", "bell": "BL1", "number": "NM1", "scraper": "BS1"},
                        "why": "the cottage nearest the quay, four-panel as built in 3.1 with its plain oblong bell push; the sheet's deep teal; the one boot scraper, by the step (owed: no period photograph shows one here)"},
    "west_south_bay1": {"kind": "T3", "paint": "white_gloss", "frame": "white", "condition": "kept",
                        "furniture": {"letter_plate": "LP6", "handle": "HD2c", "latch": "LK0", "knocker": "KN0", "bell": "BL0", "number": "NM0", "scraper": "BS0"},
                        "why": "the cottage with replacement windows: the white moulded door with a small arched light that D4 shows next to its replacement windows"},
    "west_south_bay0": {"kind": "T2", "paint": "cream", "frame": "white", "condition": "tired",
                        "furniture": {"letter_plate": "LP5", "handle": "HD3", "latch": "LK0", "knocker": "KN0", "bell": "BL0", "number": "NM4", "scraper": "BS0"},
                        "why": "the cottage by the yard slot: the 1930s four-light glazed door of D3 with its leaded fanlight; a painted number on the glass"},
    "west_north_bay2": {"kind": "F7", "paint": "navy", "frame": "white_grimy", "condition": "neglected",
                        "furniture": {"letter_plate": "LP0", "handle": "HD4", "latch": "LK0", "knocker": "KN0", "bell": "BL0", "number": "NM0", "scraper": "BS0"},
                        "why": "beside the yard slot, in a one-storey shop row: a service door to the back passage, ledged and braced (owed line 3: if the PC wants flats in this row it takes F1 instead)"},
    "west_north_bay1": {"kind": "F3", "paint": "black", "frame": "white", "condition": "tired",
                        "furniture": {"letter_plate": "LP1", "handle": "HD3", "latch": "LK0", "knocker": "KN0", "bell": "BL0", "number": "NM3", "scraper": "BS0"},
                        "why": "a household door in the row: two long panels as D1's left door, a bar pull on the left stile"},
    "west_north_bay0": {"kind": "F1", "paint": "maroon", "frame": "white", "condition": "kept",
                        "furniture": {"letter_plate": "LP1", "handle": "HD1", "latch": "LK2", "knocker": "KN0", "bell": "BL0", "number": "NM0", "scraper": "BS0"},
                        "why": "the north end of the row: the four-panel door as built"},
}
BACKDROP_RULE = ("The 12 doors of the hill's rows (backdrop_rise_approach_e0 e1, w0 to w4, x0 to x4) are seen at 44 m and more: leaf kind and paint, nothing else. "
                 "Door i takes kind BACKDROP_KINDS[i mod 6] and paint BACKDROP_PAINTS[(i + 2) mod 6], so that no two doors of a row, taken in their order, share a kind or a paint. "
                 "No furniture, no step, no wear mask beyond the foot band.")
BACKDROP_IDS = ["e0", "e1", "w0", "w1", "w2", "w3", "w4", "x0", "x1", "x2", "x3", "x4"]
BACKDROP_KINDS = ["F1", "F2", "F3", "F4", "T1", "T2"]
BACKDROP_PAINTS = ["black", "maroon", "navy", "dark_green", "brown", "deep_teal"]

OWED = [
    "Door colours: dark doors as the Hook sheet shows, with two lighter ones from 1980s photographs (one white, one council turquoise)? Yes, two (recommended), or all dark?",
    "Door surrounds: all white as you ruled for windows on 3 October (recommended), or the painted surrounds the 1980s Hull streets show, as on the windows line?",
    "The west shop row has one storey: its three side doors become a service door and two household doors (recommended), or flats in its roof with household doors on all three?",
]
