"""Author tool: the prose and the check list of target.json (sources, photographs, disagreements, the failures answered, reuse, checks, what is not settled)."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DATE = "2026-10-12"

SOURCES = [
    {"id": "P1", "what": "A fishmonger's front, Worcester (a Geograph photograph; the page's title names the real firm, which this target does not repeat): an old shop front left as it was: divided timber lights, a black-tiled stallriser, a half-glazed timber door, the slab visible through the glass",
     "url": "https://www.geograph.org.uk/photo/2192169", "read": DATE, "author": "Helen Iwanczuk", "licence": "CC BY-SA 2.0", "taken": "May 2000 (the page: 'taken May 2000')",
     "shows": "the front a fish shop kept for decades (the author: the premises 'remained in this condition'): door leaf 335 px high by 140 wide (0.42), glass foot 0.413 of the leaf, two panes divided by a bar at 0.685, a letter plate at 0.32, stallriser tiled to 0.28 of the leaf, the window slab and the room dark behind reflections",
     "dated_object": "a period object: a later photograph of a front unchanged since before 1990 (the page says so); 2000 is the earliest dated photograph of a fish-shop window reached", "used": "measured (photo_measurements.json), cropped below the fascia for the preview with the door's number plate and two window stickers masked grey, the main photograph of the self-check's overlay"},
    {"id": "P2", "what": "A grocer's shop, Bath Road (a Geograph photograph, March 1999; the page names the real firm, which this target does not repeat): an open-fronted stock window, tiered stands, goods stacked to the glass, the shop's back shelves visible",
     "url": "https://www.geograph.org.uk/photo/2184467", "read": DATE, "author": "Helen Iwanczuk", "licence": "CC BY-SA 2.0", "taken": "March 1999",
     "shows": "density of a grocer's window and the depth of its stock (tins, jars, crates on tiered timber stands); a person stands at the door (masked in the preview)", "dated_object": "a long-established shop (the page: established 1898); 1999 shows a 1990 window",
     "used": "yes: the tiered stand and the density in the grocer's display; preview cropped to the left window and stand (the shop door, with a person at it, and the right-hand shelves are outside the crop)"},
    {"id": "P3", "what": "Shops in Cannon Lane, Pinner (Geograph): a hardware store's and a newsagent's windows, one lit and readable, one dark",
     "url": "https://www.geograph.org.uk/photo/5945841 (and 3403654, the same parade)", "read": DATE, "author": "Carl Grove", "licence": "CC BY-SA 2.0", "taken": "20 February 1989",
     "shows": "a 1989 high-street parade: the hardware window's dark interior with stock to the ceiling behind reflections; the newsagent's lit interior with racks; deep recessed doors; cars of 1989", "dated_object": "a photograph of the period itself",
     "used": "yes: the black-void question (the glass is mostly reflection by day, the room dim; a lit shop reads); preview cropped to the two windows below their fascias (the parade's other signs, a drink merchant's, are outside the crop)"},
    {"id": "P4", "what": "A ship chandler's shut shopfront, High Street, Hull (Geograph): green timber front, lower lights screened inside with woven galvanised mesh",
     "url": "https://www.geograph.org.uk/photo/3378991", "read": DATE, "author": "Bernard Sharp", "licence": "CC BY-SA 2.0", "taken": "1 January 1983 (the feed's date; the page says taken before redevelopment)",
     "shows": "the chandler's front: three tall lights, mullions in green, mesh screens over the lower lights, a plaque on the door post", "dated_object": "a photograph of the period itself",
     "used": "yes: the night mesh screens (chandler), the green; preview cropped below the fascia with the door-post board, the glass lettering and a red sign masked grey (a real firm's name)"},
    {"id": "P5", "what": "Launderette in Hambledon Parade (Geograph): a 1960s-80s aluminium-framed launderette front with a script fascia and a striped blind, the room dark behind the glass",
     "url": "https://www.geograph.org.uk/photo/1633924", "read": DATE, "author": "Basher Eyre", "licence": "CC BY-SA 2.0", "taken": "26 December 2009",
     "shows": "the type of front (full-height glazing, glazed door, machines faintly seen); LATER than 1995: used only for the type and for what a launderette window does by day", "dated_object": "a later photograph; the front's pattern is the 1970s-80s one (not dated by the author)",
     "used": "as a type reference only; preview cropped to the front"},
    {"id": "P6", "what": "A derelict grocer and draper's shop, Kames (Geograph): glass dark or blank, paint gone, a pillar box at the kerb",
     "url": "https://www.geograph.org.uk/photo/27024", "read": DATE, "author": "Andrew Longton", "licence": "CC BY-SA 2.0", "taken": "24 May 1995",
     "shows": "an unlet shop in 1995: the glass reads grey-blue and blank, not black; no whitewash", "dated_object": "a photograph of the period itself", "used": "for the empty unit's glass: it must read as a pale blank, not a black hole; preview cropped below the eaves with the old fascia band (the firm's name and trades) and the neighbouring shop's board masked grey (disagreement D10)"},
    {"id": "H1", "what": "Poly Haven catalogue (api.polyhaven.com/assets?t=models, and /files/<id> for each of the 105 models used): 521 models, 868 textures; each model's name, size, triangles, date, authors and glTF file read; thumbnails (cdn.polyhaven.com) looked at on three contact sheets",
     "url": "https://api.polyhaven.com/assets?t=models", "read": DATE, "author": "Poly Haven contributors", "licence": "CC0", "taken": "n/a", "shows": "every id in the inventory exists with a 1k glTF", "dated_object": "n/a", "used": "yes (inventory.polyhaven)"},
    {"id": "H2", "what": "ambientCG API (ambientcg.com/api/v2/full_json): ids checked to exist as CC0 materials", "url": "https://ambientcg.com/api/v2/full_json", "read": DATE, "author": "ambientCG", "licence": "CC0", "taken": "n/a",
     "shows": "Tiles032, Tiles040, Ice001, Ice002, Marble012, Rope001, Rope002, Candy001, Candy002, Fabric020, Fabric021, Fabric028, Fabric029, Cardboard002, Wicker010B, Terrazzo004 and the imperfection sets exist (a search call reset twice and is not relied on)", "dated_object": "n/a", "used": "yes (inventory.ambientcg_checked)"},
    {"id": "H3", "what": "Sketchfab API v3 (anonymous): the ffishAsia / floraZia CC0 scans (cod, mackerel x2, herring, flounder x2, crab, prawn x2, apple, cabbage, potato, satsuma, pear, lemon): name, licence 'CC0 Public Domain', faces, publish date, downloadable true; the download endpoint answers 401 without a login",
     "url": "https://api.sketchfab.com/v3/models/<uid>", "read": DATE, "author": "ffish.asia / floraZia.com", "licence": "CC0 Public Domain", "taken": "scans published 2021 to 2026", "shows": "the goods that no Poly Haven model gives are real scans, on the allowlist ('Sketchfab CC0 filter'), and need only Jafar's login",
     "dated_object": "n/a", "used": "yes (inventory.sketchfab_checked); not downloaded"},
    {"id": "H4", "what": "Smithsonian Open Access 3D API (3d-api.si.edu/api/v1.0/content/file/search): answers from the cloud; queries for mackerel, flounder, haddock, plaice, lobster, Gadus, Clupea and Scomber return nothing; 'cod' and 'herring' return only unrelated objects (a horseshoe crab, a flight suit); 'crab' returns a king crab (Lithodidae), 'shrimp' a mantis shrimp",
     "url": "https://3d-api.si.edu/", "read": DATE, "author": "Smithsonian", "licence": "CC0 (per item; not on the allowlist by name)", "taken": "n/a", "shows": "no British fish are there", "dated_object": "n/a", "used": "no: nothing fits and it is not named on the allowlist"},
    {"id": "G1", "what": "Wikimedia Commons (API, one request at a time; many 429s): category listings for launderettes, fishmongers, ship chandlers, tea rooms, pawnbrokers; the 1968 'Twthill laundrette, Caernarfon' (CC BY-SA 4.0, Geoff Charles) was seen and has children in the frame",
     "url": "https://commons.wikimedia.org/", "read": DATE, "author": "various", "licence": "various", "taken": "see text", "shows": "no photograph from 1975 to 1995 of a pawnbroker's or a launderette's window or room was reached; the Caernarfon launderette (1968) is NOT used (children)", "dated_object": "n/a", "used": "no"},
    {"id": "R", "what": "Project files read: canon.md, TOWN.md, RULINGS.md, DECISIONS.md 236 and 243, production/specs/shop-interiors.json, vignette-scene.json, vignette-pieces.json, hook-cast.json, tools/ue/make_interior_material.py, tools/art-recipes/shop-room.py, fetch_polyhaven.py, make_label_atlas.py, terrace-front.py 2385-2417, production/research/shop-window-interiors/*, shop-hours-1990, targets/shopfronts (2.2), targets/fascia-signs (4.1), kit/shopfront/NOTES.md, 2d/fascias/NOTES.md, HANDOVER.md, commit 2f475f5 and NOW.md as of it",
     "url": "-", "read": DATE, "author": "studio", "licence": "own", "taken": "-", "shows": "the game's format, the three failures of 3 October, the ten units, the lit list, the hours", "dated_object": "-", "used": "yes"},
]

UNREACHED = [
    "Peter Marshall's Hull and 1990 London photographs (Flickr): named in NOTE.md as links only; not requested in this unit, so no number rests on them.",
    "Picture Sheffield t13140 and t13138 (the fishmonger of 1989 and 1990): read by the builder on 3 October (FISHMONGER-2026-10-03.md), not re-read today; used only as that note reports them.",
    "Any photograph from 1975 to 1995 of a pawnbroker's window or room, a launderette's window or room, or a ship chandler's interior: none was reached (Geograph's category 'Pawnbroker' starts in 2006 and 'Launderette' in 2005; Commons returned US, Irish and foreign shops and a 1968 launderette with children).",
    "Historic England and the Black Country Living Museum's pawnbroker (a 1930s reconstruction): not used.",
    "A Sketchfab download of any scan: needs Jafar's login (401 without).",
]

# The six photographs' previews: the crop in the original's pixels and every mask (flat grey 120,120,120) in the original's pixels. make_previews.py
# draws the masks on EVERY rebuild and checks each is flat grey in the JPEG; self_check.py reads the JPEGs against this list (PRV-01 to PRV-03).
MASK_GREY = (120, 120, 120)
PREVIEW_PHOTOS = [
    {"id": "P1", "gid": "2192169", "url": "https://s0.geograph.org.uk/geophotos/02/19/21/2192169_36cb6ecc.jpg", "name": "P1-worcester-fish-front-below-fascia", "crop": [0, 108, 640, 480],
     "cropped_away": "the fascia board (the shop's name, its street number and telephone number) is above the crop; the red car at the left edge shows only its rear lamp and bumper (no number plate is in the picture)",
     "masks": [
         {"what": "the orange window sticker (a fish picture and a fish merchant's firm name) on the right-hand window's left pane", "shape": "rect", "box": [383, 108, 436, 146]},
         {"what": "the second orange sticker of the same fish merchant's firm name, on the right-hand window's right pane", "shape": "rect", "box": [557, 94, 611, 134]},
         {"what": "the door's number plate (the street number of the real shop), the oval at the foot of the glass", "shape": "rect", "box": [284, 329, 313, 347]}]},
    {"id": "P2", "gid": "2184467", "url": "https://s0.geograph.org.uk/geophotos/02/18/44/2184467_941cf948.jpg", "name": "P2-bath-grocer-window-stock", "crop": [30, 388, 192, 582],
     "cropped_away": "the shop's fascia, its door and the person standing at it, and the right-hand shelves are outside the crop; no lettering in the crop is large enough to read (162 x 194 px)", "masks": []},
    {"id": "P3", "gid": "5945841", "url": "https://s1.geograph.org.uk/geophotos/05/94/58/5945841_dc1c2255_1024x1024.jpg", "name": "P3-pinner-hardware-newsagent-windows", "crop": [300, 326, 690, 520],
     "cropped_away": "the parade's fascias and a drink merchant's sign are above and beside the crop; the one strip of a fascia at the top right and a notice at the top of the hardware window are a few pixels high and not legible",
     "masks": []},
    {"id": "P4", "gid": "3378991", "url": "https://s3.geograph.org.uk/geophotos/03/37/89/3378991_95b1bbed_1024x1024.jpg", "name": "P4-hull-chandler-front-mesh", "crop": [225, 548, 600, 990],
     "cropped_away": "the shop's fascia and sign are above the crop",
     "masks": [
         {"what": "the painted board on the door post, which names the firm, its office and its trades (the large grey box in the middle)", "shape": "rect", "box": [405, 655, 478, 748]},
         {"what": "the gilt lettering on the upper glass at the left, which names the firm (the grey box at the top left)", "shape": "rect", "box": [300, 580, 350, 645]},
         {"what": "the red sign on the glass below that lettering (a firm's or an alarm company's mark)", "shape": "rect", "box": [308, 644, 332, 690]}]},
    {"id": "P5", "gid": "1633924", "url": "https://s0.geograph.org.uk/geophotos/01/63/39/1633924_c4220c3e.jpg", "name": "P5-launderette-front-type-2009", "crop": [0, 262, 330, 425],
     "cropped_away": "only the trade word 'Launderet(te)' of the fascia and a small notice on the door are in the crop; neither is a firm's name", "masks": []},
    {"id": "P6", "gid": "27024", "url": "https://s0.geograph.org.uk/photos/02/70/027024_2285cb8f.jpg", "name": "P6-kames-unlet-shop-1995", "crop": [56, 296, 417, 420],
     "cropped_away": "the upper floors and the roof are above the crop (they carry no lettering)",
     "masks": [
         {"what": "the whole fascia band of the old shop, which carries the firm's name and its trades in painted lettering (the Geograph page's own title repeats them): a slanted band from the eaves line to the window heads",
          "shape": "poly", "poly": [[66, 284], [272, 262], [272, 306], [258, 306], [212, 303], [165, 315], [125, 319], [66, 326]]},
         {"what": "the neighbouring shop's board, at the right (a second firm's name)", "shape": "rect", "box": [346, 290, 417, 327]}]},
]

# ---- the marks on the Poly Haven models' base-colour maps (the 1k glTF maps, 1024 x 1024; read by eye by the writer on 12 October after the review) -------------------------
# Every placed model whose 1k base-colour map carries a maker's name, a trademark, a price or barcode, a foreign-currency or place sticker, a person's or artist's
# name or a cartoon figure is listed with the exact map, the boxes (pixels of the 1024 x 1024 map, [x0, y0, x1, y1]) and what to paint them to. The 104 models'
# maps were all looked at (25 contact sheets at 512 px); a model not listed showed no mark at that size: the builder still opens every map at 1k before placing
# it (step 0), and anything found there is added here with its box.
BLANK_STEP = ("script step (one per listed map, before the model is placed): open the map; for each box, take the fill (the median colour of a 6 px ring just outside the box, "
              "the sampled value is given for reference), paint the whole box to it, then copy a same-size patch of the map's own grain from the nearest clean area over it "
              "(no flat patch); write <map>_clean.jpg beside it; point the glTF material's baseColorTexture at the clean map. 'Whole label area' means every box listed for that map. "
              "The normal and roughness maps are not touched (a print has no relief at 1k).")
FINAL_CHECK = {
    "script": "after the step, for each listed box of the FINAL texture: the largest difference from the ring colour on any channel is at most 24 levels and fewer than 2 per cent of the box's pixels have a gradient above 40 levels: an erased box is the ring colour plus grain, with no glyph edge in it; a box that fails fails the build; where a whole map is replaced (boxes [0, 0, 1024, 1024]: cigarette_pack, the picture frames' artworks) the script checks that the final map is a different file from the downloaded one (its hash differs) and that the glTF points at the project's print",
    "visual": "the builder opens the final map at 100 per cent beside the original and reads every printed word (a mark outside the listed boxes, a half-erased glyph and a seam are what no script can test); any word, number, logo, face or sticker still legible is a fault, and a new mark found goes into this list with its box",
}


def _m(marks, blank, keep=None, note=None):
    d = {"marks": marks, "blank": blank, "keep": keep}
    if note:
        d["note"] = note
    return d


MARKS = {
    "cassette_player": _m("red roundel, 'Dixons' and 'TR12 Cassette Recorder' above the cassette window: painted out of the base-colour map to the case's brushed grey; the tape's handwritten label kept",
                          [{"map": "cassette_player_body_diff_1k.jpg", "boxes": [[380, 794, 540, 820]], "fill": "the case's brushed grey (sampled 151, 152, 151)", "reads": "a red roundel, the word 'Dixons' and the line 'TR12 Cassette Recorder', printed upside down on the map at the foot of the light-grey panel"}],
                          keep="the tape's own label (cassette_player_tape_orangeblue_diff_1k.jpg: 'Classic Rock Vol. 1', 'HIGH FIDELITY', '90 MINUTES': no maker) and the control legends (Record, Play, Rewind, MIC, VOLUME)",
                          note="the real British high-street retailer's name; 'dixons' is in brand_blocklist; the same model is in the approved recipe's stock (see could_not_settle)"),
    "portable_cassette_player": _m("'SDQ' logos and 'SUPER PRECISION RIGID CASSETTE MECHANISM' on the cassette inserts, 'PORTABLE CASSETTE PLAYER' printed along the side, 'pro' on the speaker plate: maker's name painted out",
                                   [{"map": "portable_cassette_player_diff_1k.jpg", "boxes": [[45, 515, 345, 695], [0, 700, 300, 775], [95, 330, 145, 510], [735, 765, 760, 815]], "fill": "the cassette's dark blue-grey (sampled 52, 57, 60) for the first two; the case's grey-blue (sampled 90, 105, 110) for the others", "reads": "SDQ, SUPER PRECISION RIGID CASSETTE MECHANISM, SIDE A / SIDE B, the side lettering, 'pro'"}],
                                   keep="the cassette's window and the control symbols without words"),
    "boombox": _m("a maker's plate with 'Tv - Mw/Fm STEREO CASSETTE RECORDER' and a logo at the top left of the map, and three stickers: a cartoon figure playing a guitar (a young person: the children rule), a skull and a cartoon skeleton",
                  [{"map": "boombox_diff_1k.jpg", "boxes": [[0, 100, 320, 230]], "fill": "the case's dark grey (sampled 52, 52, 52)", "reads": "the plate's printed legends and logo"},
                   {"map": "boombox_diff_1k.jpg", "boxes": [[555, 385, 685, 505], [740, 515, 830, 635], [720, 775, 835, 890]], "fill": "the case's grey (sampled 112, 112, 112)", "reads": "the guitar-playing cartoon (a child-like figure), the skull, the skeleton"}],
                  keep="the speaker grilles and the cassette door"),
    "television_02": _m("a rotated model-plate strip on the back/side panel (about 10 px high, unreadable at 1k scale on the screen)", [{"map": "television_02_diff_1k.jpg", "boxes": [[268, 452, 296, 542]], "fill": "the case's dark brown-grey (sampled 54, 52, 48)", "reads": "a model number strip"}]),
    "Camera_01": _m("a Leica look-alike with the real firm's names: 'LEICA SUMMILUX-M 1:1.4/50 ASPH. E 46 4004490' on the lens ring, 'ERNST LEITZ GMBH WETZLAR GERMANY', 'DEP' and 'M3-785000' on the body plate, a red-and-white emblem on the film-speed dial, 'close - zu / open - auf' on the shutter ring, and a red island on the lens map: maker's lettering painted out",
                    [{"map": "Camera_01_lens_body_diff_1k.jpg", "boxes": [[16, 203, 604, 237], [828, 88, 1024, 462]], "fill": "the lens ring's black (sampled 10, 10, 10)", "reads": "the whole lens-ring engraving line (LEICA SUMMILUX ...) and the red island (a red-dot emblem)"},
                     {"map": "Camera_01_body_diff_1k.jpg", "boxes": [[748, 566, 902, 624], [620, 646, 737, 680], [398, 196, 460, 258], [833, 428, 927, 550]], "fill": "the body leatherette black (sampled 19, 16, 15); the dial emblem to the dial's white", "reads": "ERNST LEITZ GMBH WETZLAR GERMANY / DEP, M3-785000, the dial's emblem, 'close - zu', 'open - auf'"}],
                    keep="the distance and aperture numerals (no maker), the film-speed numerals", note="'leica' and 'leitz' are in brand_blocklist"),
    "wall_clock": _m("'URBAN quartz' under the 12 on the dial: maker's mark painted out", [{"map": "wall_clock_diff_1k.jpg", "boxes": [[248, 616, 312, 664]], "fill": "the dial's white (sampled 224, 224, 224)", "reads": "URBAN / quartz"}], keep="the numerals and ticks"),
    "vintage_lighter": _m("'TROP(R)' (a trademark) on the case and a logo plate: maker's mark painted out", [{"map": "vintage_lighter_diff_1k.jpg", "boxes": [[60, 452, 295, 522], [20, 700, 296, 1002]], "fill": "the brushed brass-grey (sampled 147, 125, 112)", "reads": "TROP(R), and the engraved logo plate with its triangle emblem"}], keep="the scratches and wear"),
    "measuring_tape_01": _m("a yellow label '3m / Q-TECH / QC PASSED': makers' names painted out (the label's yellow kept as a plain tape-case sticker)", [{"map": "measuring_tape_01_diff_1k.jpg", "boxes": [[555, 255, 725, 422]], "fill": "the case's black-grey (sampled 28, 28, 28); a plain 60 x 40 yellow sticker may stand over the middle of the box", "reads": "3m, Q-TECH, QC PASSED"}]),
    "CashRegister_01": _m("the readout's '$' ('$021.37'), the drawer plate 'TITCH BANKS', a 'TITCH CO.' label, a Canadian banknote, three place badges ('I (heart) LAS VEGAS', 'I (heart) TORONTO', 'I (heart) QUEBEC': a gambling place and two foreign places), and printed receipt slips: the '$' painted out (no '(pound)' is drawn: the readout shows digits only), every name, badge and slip blanked",
                          [{"map": "CashRegister_01_diff_1k.jpg", "boxes": [[468, 227, 486, 248]], "fill": "the readout panel's dark grey (sampled 52, 52, 52)", "reads": "the dollar sign in the readout"},
                           {"map": "CashRegister_01_diff_1k.jpg", "boxes": [[780, 438, 802, 532]], "fill": "the plate's dark grey (sampled 52, 52, 52)", "reads": "TITCH BANKS (the plate on the drawer, printed upright on the map)"},
                           {"map": "CashRegister_01_diff_1k.jpg", "boxes": [[905, 317, 942, 386]], "fill": "the label paper's grey (sampled 190, 192, 196)", "reads": "TITCH CO. and its small print"},
                           {"map": "CashRegister_01_diff_1k.jpg", "boxes": [[195, 338, 232, 380], [222, 490, 300, 532]], "fill": "the brass-brown of the surround (sampled 150, 105, 60) for the first, the dark grey (sampled 30, 30, 30) for the second", "reads": "I (heart) LAS VEGAS; I (heart) TORONTO, I (heart) QUEBEC"},
                           {"map": "CashRegister_01_diff_1k.jpg", "boxes": [[395, 85, 450, 184], [778, 165, 862, 238], [855, 545, 920, 603]], "fill": "the surrounding dark grey (sampled 52, 52, 52) for the banknote; the slips' paper (sampled 215, 205, 195) for the slips", "reads": "a Canadian banknote ('CANADA'); printed receipt slips with 'TOTAL' and amounts"}],
                          keep="the key legends (digits, A, B, R, X, Y, Z) and the receipt roll's plain paper", note="the register stands in six shops (not in Mickey's real room): at the close view its readout is about 3 px high; the rule is applied anyway"),
    "cement_bag": _m("the bag's print is post-1992: a red logo (an arrow and 'CEMENT' in red), 'CEM I 42,5 R / CEM 42.5 N' (the EN 197-1 designation of 2000), 'EN 197-1', a green panel of modern safety pictograms, a barcode, a maker's name ('SOLIDUS RESOURCES') and a 'CE' mark: all of the print is replaced by a plain stamp",
                     [{"map": "cement_bag_diff_1k.jpg", "boxes": [[60, 138, 618, 566], [52, 568, 618, 1004], [662, 398, 924, 994], [66, 44, 380, 118], [602, 40, 914, 110]], "fill": "the kraft paper (sampled 194, 164, 135); the red areas around the panels and in the two top bands are painted to the same kraft colour with a faint warm stain from the map's own luma", "reads": "every printed panel (back, front, side) and the two red top bands with 'CEMENT' reversed out"}],
                     keep="nothing of the print", note="then a plain stamp is drawn: the single word 'CEMENT' and '50 kg' in a dark grey sans (the project's OFL font, 70 px tall) centred on the front panel [52, 568, 618, 1004] and on the back panel [60, 138, 618, 566]; no maker, no standard, no pictogram, no barcode"),
    "lifebuoy": _m("'Lighthouse' and 'PH . SA . 20' lettered round the ring: replaced by a made-up vessel name or blanked", [{"map": "lifebuoy_diff_1k.jpg", "boxes": [[780, 190, 962, 402], [630, 690, 782, 902], [560, 612, 750, 696]], "fill": "the ring's red (sampled 163, 50, 50) for the first two, the white band's grey (sampled 190, 190, 190) for the third", "reads": "'Lighthouse' (rotated) and 'PH . SA . 20' (rotated), and the lettering that runs on over the white band"}],
                   note="the made-up name, if the builder wants lettering: 'MARY ANN' in white sans on the ring, drawn by script over the first box"),
    "rubber_boots": _m("two small embossed 'MICKY' badges (a maker's logo) on the boot map", [{"map": "rubber_boots_diff_1k.jpg", "boxes": [[446, 48, 502, 74], [648, 400, 704, 424]], "fill": "the boot's dark green (sampled 13, 52, 33)", "reads": "MICKY (two badges)"}], keep="the sole and the lining"),
    "cleaner_tin_01": _m("the 'PolyClean' brand, 'ANTISEPTIC HAND CLEANSER', a price '1'9', a barcode and a flame warning: the whole label area is replaced by the project's atlas tile", [{"map": "cleaner_tin_01_diff_1k.jpg", "boxes": [[0, 0, 372, 490], [0, 590, 1024, 1024]], "fill": "the tin's red (sampled 234, 36, 15) for the label band, the lid's white-grey (sampled 200, 200, 196) for the lid", "reads": "the lid print and the whole red label band"}], note="then the atlas tile (a fictional maker) is laid over the label band"),
    "drain_cleaner": _m("'DRAIN UNBLOCKER', hazard text, pictograms and a 'Keep out of reach of children' line: the whole label area is replaced by the project's atlas tile", [{"map": "drain_cleaner_diff_1k.jpg", "boxes": [[0, 636, 152, 1004], [286, 640, 646, 792]], "fill": "the tin's yellow (sampled 168, 144, 59)", "reads": "the two printed labels"}], note="then the atlas tile (the yellow can's fictional label) is laid over the front label"),
    "cigarette_pack": _m("the real brand 'Kentucky Ace' with 'PREMIUM FILTERS', 'KING SIZE' and a 'SURGEON GENERAL'S WARNING' (a US pack): the whole map is replaced by the atlas's tobacco tile", [{"map": "cigarette_pack_diff_1k.jpg", "boxes": [[0, 0, 1024, 1024]], "fill": "not a fill: the map is replaced by the atlas tile laid on the pack's net (shape only is kept)", "reads": "the whole pack"}], note="'kentucky' is in brand_blocklist"),
    "adjustable_wrench": _m("a 'STEELBOX TOOLS' diamond logo on the jaw ('DROP FORGED STEEL' is a stamp, not a name, and stays)", [{"map": "adjustable_wrench_diff_1k.jpg", "boxes": [[612, 358, 724, 422]], "fill": "the steel's mid grey (sampled 120, 120, 118)", "reads": "STEELBOX TOOLS (diamond)"}]),
    "hatchet": _m("a 'UC' trademark with (R) stamped on the blade", [{"map": "hatchet_diff_1k.jpg", "boxes": [[490, 964, 534, 1010]], "fill": "the blade's grey (sampled 110, 110, 110)", "reads": "UC (R)"}]),
    "pocket_watch": _m("the dial reads 'Lorex' (a look-alike of a real watchmaker's name)", [{"map": "pocket_watch_diff_1k.jpg", "boxes": [[220, 132, 294, 170]], "fill": "the dial's cream (sampled 228, 226, 214)", "reads": "Lorex"}], keep="the numerals"),
    "vintage_pocket_watch": _m("'AVVENTURA' lettered on the inner dial (a watch brand name)", [{"map": "vintage_pocket_watch_diff_1k.jpg", "boxes": [[620, 630, 765, 790]], "fill": "the inner dial's grey (sampled 180, 182, 184)", "reads": "AVVENTURA (rotated)"}]),
    "screwdriver": _m("'LANSTEY' on the handle (a look-alike of a real tool maker)", [{"map": "screwdriver_diff_1k.jpg", "boxes": [[168, 630, 400, 692]], "fill": "the handle's red-orange (sampled 232, 66, 40)", "reads": "LANSTEY"}]),
    "tire_pump": _m("'POLYLUFT' and a round logo on the pump's label plate, and an orange label", [{"map": "tire_pump_diff_1k.jpg", "boxes": [[570, 520, 664, 880], [800, 20, 900, 100]], "fill": "the label plate's grey (sampled 150, 150, 150); the dark body grey for the second", "reads": "POLYLUFT (rotated), the roundel logo, the orange label"}]),
    "Ukulele_01": _m("a 'KOLO' maker's label inside the headstock area", [{"map": "Ukulele_01_diff_1k.jpg", "boxes": [[520, 195, 640, 305]], "fill": "the wood's brown (sampled 150, 95, 50)", "reads": "KOLO label"}]),
    "vintage_video_camera": _m("'PH JNL 7' and 'PH.JNL - OPTICAL CO., LTD' plates and a red-and-black label (a maker's marks)", [{"map": "vintage_video_camera_diff_1k.jpg", "boxes": [[10, 388, 202, 650], [28, 808, 192, 932]], "fill": "the body's dark olive (sampled 60, 62, 50)", "reads": "PH JNL 7; PH.JNL - OPTICAL CO., LTD; the red and black label"}]),
    "filmstrip_projector_8mm": _m("a 'SIRIUS steering' label plate (a maker's name)", [{"map": "filmstrip_projector_8mm_diff_1k.jpg", "boxes": [[270, 474, 400, 574]], "fill": "the plate's cream (sampled 230, 220, 190)", "reads": "SIRIUS steering"}]),
    "garden_gloves_01": _m("a printed size-and-maker label on the glove", [{"map": "garden_gloves_01_diff_1k.jpg", "boxes": [[172, 690, 286, 770]], "fill": "the glove's teal (sampled 70, 190, 160)", "reads": "a printed label ('S.BOX' / size)"}]),
    "garden_sprinkler_01": _m("small print ('Polyplast ...') at the foot of the body map", [{"map": "garden_sprinkler_01_diff_1k.jpg", "boxes": [[30, 960, 210, 996]], "fill": "the body's yellow (sampled 230, 185, 40)", "reads": "a maker's line of small print"}]),
    "plastic_broom": _m("a 'MICKY' label on the handle", [{"map": "plastic_broom_diff_1k.jpg", "boxes": [[728, 830, 772, 926]], "fill": "the handle's cream (sampled 240, 235, 220)", "reads": "MICKY"}]),
    "pipe_wrench": _m("'SES' and '18' stamped on the handles (a maker's initials)", [{"map": "pipe_wrench_diff_1k.jpg", "boxes": [[40, 100, 100, 175], [320, 100, 380, 175]], "fill": "the handle's red-grey (sampled 150, 90, 80)", "reads": "SES / 18"}]),
    "lightbulb_01": _m("a 'Lumen' print with a wattage line on the bulb's cap", [{"map": "lightbulb_01_diff_1k.jpg", "boxes": [[90, 110, 230, 200]], "fill": "the cap's dark grey (sampled 40, 40, 42)", "reads": "Lumen and its small print"}]),
    "stationery_supplies": _m("pencil boxes and pads printed 'Nova Presents HB' and similar (a maker's name)", [{"map": "stationery_supplies_diff_1k.jpg", "boxes": [[0, 20, 840, 420], [820, 0, 1024, 1024]], "fill": "each box is painted to the median of its own band (blue, yellow, red, cream): whole label area", "reads": "the pencil boxes' lettering and the pads' printing"}]),
    "ceramic_vase_01": _m("a price label with a barcode stuck on the vase", [{"map": "ceramic_vase_01_diff_1k.jpg", "boxes": [[580, 84, 626, 164]], "fill": "the glaze's off-white (sampled 232, 230, 224)", "reads": "a barcode sticker"}]),
    "hanging_picture_frame_01": _m("the artwork map is a placeholder reading 'Ray Homes / Photo: 76cm x 51cm / Frame: 84cm x 59cm' (an artist's name)", [{"map": "hanging_picture_frame_01_artwork_diff_1k.jpg", "boxes": [[0, 0, 1024, 1024]], "fill": "not a fill: the whole artwork map is replaced by one of the project's own invented prints (an oil-painted seascape or flower piece by script)", "reads": "the placeholder and its credit"}]),
    "hanging_picture_frame_02": _m("the artwork is a painting of a real palace signed 'Celine F.' (an artist's name and a real landmark)", [{"map": "hanging_picture_frame_02_artwork_diff_1k.jpg", "boxes": [[0, 0, 1024, 1024]], "fill": "not a fill: the whole artwork map is replaced by the project's own invented print", "reads": "the painting and its signature"}]),
    "hanging_picture_frame_03": _m("the artwork is a photograph of a real foreign castle (a landmark: the project's pictures show nothing foreign)", [{"map": "hanging_picture_frame_03_artwork_diff_1k.jpg", "boxes": [[0, 0, 1024, 1024]], "fill": "not a fill: replaced by the project's own invented print", "reads": "the photograph"}]),
    "standing_picture_frame_01": _m("the artwork is a photograph of a canal street of a foreign city with a parked van", [{"map": "standing_picture_frame_01_artwork_diff_1k.jpg", "boxes": [[0, 0, 1024, 1024]], "fill": "not a fill: replaced by the project's own invented print", "reads": "the photograph"}]),
    "standing_picture_frame_02": _m("the artwork is a beach photograph with small figures on the sand (no person may be recognisable, and none may be a child: they are 3 to 6 px high but the rule is no persons)", [{"map": "standing_picture_frame_02_artwork_diff_1k.jpg", "boxes": [[0, 0, 1024, 1024]], "fill": "not a fill: replaced by the project's own invented print", "reads": "the photograph with its figures"}]),
}


PHOTO_MEASUREMENTS = {
    "main_photograph": "P1 (Geograph 2192169, 640 x 480)",
    "method": "the photograph is nearly face-on; every edge was read by eye off a 4x enlargement with a 10-pixel grid (error +-3 px); ONE dimension fits the scale: the door leaf's height, 335 px, taken as the street's 2040 mm (6.09 mm a pixel), so every other number is a ratio of the leaf's height and is Photo only to that assumption (a 2100 leaf would put the glass foot at 896 above the footway: 0.413 x 2100 + 28)",
    "rows": [
        {"what": "door leaf top (underside of the transom's board)", "y_px": 122.0}, {"what": "door leaf bottom / threshold", "y_px": 457.5},
        {"what": "glass top", "y_px": 137.5}, {"what": "glazing bar, centre", "y_px": 228.0}, {"what": "glass foot", "y_px": 319.0},
        {"what": "letter plate, centre", "y_px": 350.5}, {"what": "number plate, centre", "y_px": 338.0}, {"what": "handle, centre", "y_px": 316.0},
        {"what": "lower panel field, top", "y_px": 372.5}, {"what": "lower panel field, bottom", "y_px": 422.5}, {"what": "stallriser top (tile cap)", "y_px": 362.0},
        {"what": "leaf left edge", "x_px": 230.0}, {"what": "leaf right edge", "x_px": 370.0}, {"what": "glass left", "x_px": 251.0}, {"what": "glass right", "x_px": 350.5},
    ],
    "derived_mm_from_the_leaf_height_2040": {},
}

DISAGREEMENTS = [
    {"id": "D1", "what": "where a timber shop door's glass starts", "target_2_2": "600 (level with the sill; Leadenhall 2019 at 0.304 of the leaf; DOR-06); the approved game door (rita-day-kit-2026-10-06.jpg, the door Jafar has seen) has its glass from about 1000, one pane, no bar", "photograph": "871 +-30 above the footway (843 above the leaf's foot: 0.413 of the leaf, Geograph 2192169, a fish shop's untouched front, May 2000); the lock rail runs 549 to 871 with the letter plate in it at 678",
     "chosen": "the photograph: T1 door glass from 871 above the footway (843 above the leaf's foot), the lock rail 549 to 871, the letter plate at 678, one glazing bar at 1423; the aluminium and bronze doors keep 2.2's numbers",
     "why": "Leadenhall is a 2019 heritage restoration of a London arcade; the Worcester front is a working shop in the period's condition and the nearer match; 2.2's DOR-06 (door glass foot = sill top) is replaced for T1 doors only. Flagged for Jafar (Needs you) with three options: 871, 600, about 1000."},
    {"id": "D2", "what": "the glass of the window lights", "target_2_2": "one sheet per light, no astragal bars (Rita's approved window)", "photograph": "Geograph 2192169 shows each light divided by one bar at the door's bar height; Pinner 1989 shows single large sheets (hardware) and aluminium-framed sheets (newsagent)",
     "chosen": "single sheets per light as 2.2 (Rita's window is the model and approved); the divided pattern is recorded as a possible variant, not adopted", "why": "RULINGS 2 Oct; the photographs split"},
    {"id": "D3", "what": "the door leaf's width", "target_2_2": "900 in a 1006 slot", "photograph": "about 853 (140 px of a 335 px leaf) in an older door", "chosen": "900 as 2.2: the slot is fixed by the bay; the photograph is within 6 per cent of it", "why": "inside the error"},
    {"id": "D4", "what": "the stallriser's height", "target_2_2": "600", "photograph": "571 +-18 (94 px of the leaf's 335)", "chosen": "600", "why": "inside the error (5 per cent)"},
    {"id": "D5", "what": "how bright the room reads from the street by day", "target_2_2": "the game's day brightness 0.15", "photograph": "P1 and P3: the glass is mostly reflection, the room dim; only a lit, bright shop (Pinner's newsagent) shows its goods by day",
     "chosen": "the game's 0.15 kept for every shop (the spec's values are the game's)", "why": "the research (NOTE.md section 3 and 8) and these photographs agree: over-bright day interiors are the commonest giveaway"},
    {"id": "D6", "what": "an open-fronted grocer's window", "target": "a glazed window with a 1930s bronze front", "photograph": "P2 shows stock stood out on stands in an open front", "chosen": "glazed, as 2.2", "why": "the street's grocer is a 1930s refit with glass; the density and the stands are taken, not the open front"},
    {"id": "D7", "what": "mesh over a chandler's lower lights", "target_2_2": "none", "photograph": "P4 shows woven galvanised mesh screens inside the lower lights of a shut chandler's", "chosen": "added as the chandler's night furniture (three panels)", "why": "the photograph shows it"},
    {"id": "D9", "what": "the chandler's paint", "target_2_2": "navy on piers, consoles, board and cornice, natural aluminium window", "photograph": "P4 (Hull, 1983) shows a chandler's front in dark green", "chosen": "navy as 2.2 and 4.1 (the street's board is navy); the photograph's green is used for the room's dado", "why": "the Hull shop is another shop; the street's colours are fixed by 4.1"},
    {"id": "D8", "what": "the street's lit list against the hours", "target": "vignette-pieces lit_names: 6 units lit at night", "photograph/research": "the hours research: everything shut by 8 pm; newsagent 17:30; the grocer, ironmonger and chandler not found", "chosen": "the street file's list is kept (RULINGS 1 Oct: lit windows, not one wash); the hours are the town's and are noted", "why": "a conflict between two files of the project; not mine to resolve"},
    {"id": "D10", "what": "an unlet shop's glass: whitewashed or not", "target": "4.1 and Jafar's ruling of 3 October (DECISIONS 3 Oct; 4.1 `glass/empty_unit/window_whitewash`; 2.2 alterations.empty_unit, whitewash coverage 1.0): every pane of the empty unit is whitewashed from inside",
     "photograph": "P6 (Kames, 24 May 1995) shows an unlet shop's glass blank and grey-blue with no whitewash at all", "chosen": "whitewash, as the ruling",
     "why": "Jafar's ruling of 3 October settles it, and a ruling outranks a photograph; P6 is used only for what the glass reads like (a pale blank, not black: LIT-03)"},
    {"id": "D11", "what": "the launderette's toplight: one long pane or divided", "target_2_2": "one long toplight pane over both lights (pattern 2L-1T)",
     "photograph": "P5 (Hambledon Parade, a 2009 photograph of a front of the 1970s to 80s pattern, used as a type reference only) shows the upper lights divided on the lower lights' lines",
     "chosen": "the photograph: the mullion is carried up and the toplight is two panes of 1600 (pattern 2L-2T-aligned), the same rule as every other front (kit departure D6, the 3.2 street review's fault 1)",
     "why": "photographs win; P5 is later than 1995 but its pattern is the earlier one, and the rule for the other nine fronts says the same"},
    {"id": "D12", "what": "the door lever's height", "target_2_2": "1000 on a 240 x 40 backplate (the kit's)", "photograph": "P1's handle stands at 0.42 of the leaf, about 890 above the footway (a different door: a rim knob, not a lever)",
     "chosen": "1000, the kit's and 2.2's",
     "why": "the approved game door's lever (rita-day-kit-2026-10-06.jpg, the door Jafar has seen) stands at about 1050, so the kit and the game agree against one photograph of one door; a lever 160 mm lower would change a door he has approved"},
]

FAILURES = [
    {"id": "F1", "failure": "goods made by hand (3 Oct, first review: 'toys beside Rita's scanned stock')",
     "answer": "105 Poly Haven models (CC0, each read from the API today) carry every shop's goods; what has no CC0 model is a SCAN named by uid (Sketchfab ffishAsia CC0, checked today) needing Jafar's login, or a short scripted form whose reason is written beside it (`scripted` in target.json: 52 kinds, each with a why); hand-modelled fish are forbidden; packaged goods are bevelled shapes carrying the project's fictional label atlas (production/assets/shop-goods/labels.jpg), never plain colour blocks",
     "checks": ["INV-01", "INV-02", "INV-03", "INV-04", "INV-05"]},
    {"id": "F2", "failure": "named faults (3 Oct, second round)",
     "answer": [
         "displays placed as if the door were on Rita's side (half behind the door): each display's range is the window zone of the 2.2 bay table for that shop's door end (DSP-01)",
         "a black chiller panel smeared across the fish shop's floor: the chiller is a white counter against the back wall, nothing free in the room (SO-01)",
         "the white slab burnt out at night: the fish shop is dark at night; no picture has more than 1 per cent of pixels at 250 or above (PIC-05)",
         "Gothic chairs and empty frames in the tea room: WoodenChair_01 and the Gothic set are denied; the frames carry the project's own prints; chairs and tables exist only in the window (INV-02, SO-02)",
         "an explosives sign on a drum at the chandler's: Barrel_01 is denied; no drum stands in the display (INV-02)",
         "a gold ribbon drawn across the newsagent's window and every stood card outside the glass: a check that nothing but the listed lettering, the OPEN sign, the hours plate and SB1 lies in front of the glass (GLS-01)",
         "faceted fruit: fruit are scans (Poly Haven apple, lemon, onion, bananas; ffishAsia cabbage, potato, satsuma, pear); the one scripted fruit, the tomato, is a one-try item set aside if it reads as toys",
         "slab laundry: laundry is stacks of bevelled towels with a woven-towel material and a lean, parcels with string and tags, baskets of displaced cloth",
         "counters, chairs and dryers standing off the walls: no fixture stands off a surface by more than the budget (SO-01 to SO-04)"]},
    {"id": "F3", "failure": "what a projected room cannot do at a metre or two (3 Oct, third round)",
     "answer": "the numbers from the game's own rule: stock only on the back wall (0.30 deep is true, a 0.60 counter or machine against it is tolerated), the side walls carry boards and racks at most 0.10 (0.05 true), the floor and ceiling only flat things (0.025); anything else stands in the display, which is real geometry in the near 0.55 m. The CLOSE view stands at 1.5 m from the glass, 35 degrees off, because there the whole window is seen at under 62 degrees (the glass's hand-over) and the surfaces are sharp at 4096 wide; the slide numbers are in TARGET.md section 3 (`method.honest_range`); the picture is 4096 wide because at 2048 it is soft over 4 per cent of the glass at 1.5 m and 13 per cent at 0.5 m",
     "checks": ["SO-01", "SO-02", "SO-03", "SO-04", "PIC-01", "PRJ-01", "PRJ-02", "PRJ-03"]},
]

REUSE = [
    {"part": "the method (research NOTE.md, CLOSE-RANGE, GOODS, DRESSING, FISHMONGER, hours, glass reflections, FRONTAGE)", "keeps": "a pre-projected picture per room and state, the near metre real, lights per state, the never-list, the trades' goods and fittings",
     "changes": "the room is no longer allowed to hold anything the picture cannot honestly show (the budgets); CLOSE-RANGE's 'real rooms' recommendation is NOT followed here (the brief asks for textures); its 'keep everything flat against the walls' is the rule"},
    {"part": "production/specs/shop-interiors.json", "keeps": "the camera rule, the three states, the never list, the two entries (mickeys unchanged; pawnbroker's room, card, camera_d, brightness, lit values unchanged)",
     "changes": "eight entries added (spec_entries in target.json: fishmonger, launderette, grocer, chandler, tea_room, ironmonger, newsagent; the pawnbroker's pixels_wide 2048 to 4096 and its display x0/x1 noted against the 3.2 front); no entry for the empty unit (no card)"},
    {"part": "tools/art-recipes/shop-room.py", "keeps": "the box, the camera rule, the three renders, the JSON beside each, model() from Poly Haven, texmat(), --display, --export-room (inert)",
     "changes": "the room builders for the seven trades are rewritten to the fixtures in target.json (free-standing counters and units removed); pixels_wide 4096; the maker-mark pass; the inventory.json"},
    {"part": "tools/ue/make_interior_material.py", "keeps": "everything: its `trace` is the rule the cloud gate imports; the HLSL is unchanged", "changes": "none"},
    {"part": "tools/art-recipes/fetch_polyhaven.py", "keeps": "the fetcher and the SETS", "changes": "SETS gain the ids of the inventory; none of the denied"},
    {"part": "production/assets/shop-goods/labels.jpg and make_label_atlas.py", "keeps": "the 32 fictional products", "changes": "twelve tiles added (paint, varnish, twine, tobacco, crab paste, detergent) in the same fonts"},
    {"part": "production/assets/shop-displays/pawnbroker-display.glb", "keeps": "as built, with its 23 models", "changes": "maker marks blanked; the night grille added; no piece repeated more than twice"},
    {"part": "the 3.2 kit (production/cloud-week/kit/shopfront)", "keeps": "pilaster (panel), console (scroll), fascia board, cornice (150 as built, 12 Oct), sill, stallriser (panel, three panels), window frame T1 (3 lights, nine toplights as built): Rita's front is complete but for the doors and the band above them", "changes": "nine variants are missing for the other fronts (front.missing_from_3_2 in each shop; front.build_from names the exact keys of 2.2's target.json, at commit dd706f6, that build each); the doors, the lobbies and the band above the doors are specified here, from that JSON, with three changes (D1, D11, D12) and the bell"},
    {"part": "2.2 (targets/shopfronts/target.json, at commit dd706f6)", "keeps": "the ten fronts' table, paints, door ends and hinges; its JSON is the second versioned input of every front's build (`front.build_from`)",
     "changes": "T1 door: glass foot, lock rail, letter plate, a glazing bar (D1); the bell; the toplight layout on seven fronts (the kit's D6 rule: mullions carried up, each light's toplight split equally); the band above the doors (fanlight, transom, three toplights over the shop door, a panel over the side door, the head) written into every shop's `door`; M1 letter plate in the bottom rail"},
    {"part": "4.1 (2d/fascias)", "keeps": "the ten boards, the four hanging signs, the glass rows, the whitewash and the letting board, unchanged", "changes": "none; each shop names its board"},
    {"part": "4.2 to 4.4 (2d/paper)", "keeps": "the OPEN/CLOSED sign, the newsagent's board SB1, the letting boards", "changes": "none"},
    {"part": "3.1 doors", "keeps": "F1 for every side door", "changes": "none"},
    {"part": "the set-aside branch shops-wip-2026-10-03 (a local branch on the PC, not in this clone)", "keeps": "nothing taken: it was not reachable and its goods were made by hand", "changes": "replaced; the reason is F1"},
]

COULD_NOT_SETTLE = [
    "FOR JAFAR (a fact, no decision): the Poly Haven model `cassette_player` carries the real British retailer's name 'Dixons' (with a red roundel and 'TR12 Cassette Recorder') on its base-colour map. The same model is in the approved recipe's stock pool (tools/art-recipes/shop-room.py, `pool`), so the approved pawnbroker pictures (production/art/shop-rooms/pawnbroker_day.png, _night_lit.png, _night_dark.png, 6 October) MAY ALREADY CARRY THE FIRM'S NAME on the back wall, about 4 px high at 2048 wide (the writer looked at pawnbroker_day.png's back wall at 2x on 12 October and read no word on the small cassette players, but a 4 px mark cannot be ruled out; the two night pictures were not looked at). The builder must look at those three pictures' back wall at full size before anything else and report what it finds; this target blanks the mark on every new picture (inventory `marks`, check INV-06).",
    "The fish, crab and prawn scans, and the grocer's cabbage, potato, satsuma and pear: CC0 (Sketchfab, ffishAsia, checked today) but downloadable only with Jafar's login (the API answers 401). Until he gives it the fishmonger's slab and ice and trays are built and the fish row is marked 'goods pending'; the fishmonger cannot pass the CLOSE review without them. Named plainly: a failed capability of the cloud, not a plan to dress the window another way.",
    "No 1975 to 1995 photograph of a pawnbroker's or a launderette's window or room was reached (Geograph's categories start in 2005 and 2006; Commons returned a 1968 launderette with children in frame, not used). Rita's room rests on the approved pictures (RULINGS 2 Oct); no period photograph of a pawnbroker's room was reached. The launderette rests on the research's text and one 2009 front (P5).",
    "Maker marks: only thumbnails of the Poly Haven models were looked at on 12 October by the writer and the reviewer (about 45 at 384 to 1200 px), and thumbnails missed 'Dixons'. After the review the writer opened the 1k base-colour maps (see `inventory.polyhaven[id].marks`: every mark found, its map, its region and its blanking step). The builder looks at every one of the inventory's models at 1k BEFORE placing it (step 0 of the build, a contact sheet of 12 maps at a time), not at the gate.",
    "The T1 door numbers (D1) rest on one photograph of one door, scaled by assuming a 2040 leaf; the door bell is Judgement (no photograph of one was reached). Both are narrow points a reviewer can overturn with a better photograph.",
    "4.1's fanlight street number: 4.1 puts it on the SIDE door's fanlight (x 20.18 for Rita's, the side door's centre) at z 2.18 in its street frame (above the crown: 2080 above the footway, below the shop door's fanlight). The review reads it as on the shop door's fanlight; this target follows the review (the number at the shop door's centre, baseline 2200 above the footway) and records the move of 4.1's x and z for its owner (`door.fanlight.street_number`).",
    "The hours of the grocer, ironmonger and chandler were not found; they are settled from the Shops Act (a Judgement). The street's lit list lights three shops that the hours (or, for the grocer and chandler, the Judgement from the Shops Act) say are shut by dusk in winter: the newsagent (17:30), the grocer and the chandler; kept as the street file has it (the street file and RULINGS 1 Oct settle it); the town should say which is right.",
    "Hal's shop (hook-cast.json, the coin shop, street x 39) stands inside the newsagent's bay (x 36 to 42): not resolved.",
    "Canon names no count of twelve shops: the street has ten units as built; 'twelve' and 'the other eleven' are the superseded atlas proposal's words.",
    "The picture's box floor is the card's bottom edge, 0.55 above the shop's real floor, which the stallriser hides from the street: the room reads as a stage whose floor is the window bed carried back. A truer floor needs a taller card, which terrace-front.py fixes at 0.65 to 3.05.",
    "The display can be only 0.55 m deep (the card stands 0.61 m behind the glass): the tea room's table and chairs and the launderette's baskets are tight. Moving the card back to the scene file's 1.2 m would give a deeper real zone; the brief fixes the card.",
    "The game's glass, Lumen's light on the display, the card's motion vectors under TSR, the exposure and the frame time cannot be shown from the cloud; they stay owed on the PC (`owed_on_pc`). PRJ-02 runs on the gate's own `trace` bake, so it proves the gate, not the game.",
    "Scripted goods with no CC0 model that may not pass the CLOSE review at the first try and are set aside under the two-tries rule: tomatoes, sweet jars, folded towels, newspapers and magazines, fish fillets. Each is named in `scripted`.",
]

NEEDS_YOU = [
    {"q": "May the builder have one Sketchfab login (a token, read-only, never in the repository) to download about fifteen CC0 scans (ten kinds: cod, mackerel, herring, flounder, crab, prawn, cabbage, potato, satsuma, pear)?", "recommended": "Yes", "why": "without them the fishmonger and the grocer's produce cannot pass the close view; all are on the allowlist ('Sketchfab CC0 filter') and cost nothing"},
    {"q": "Timber shop doors: glass from 871 mm above the pavement (the Worcester photograph), from 600 mm (the earlier target, from a restored arcade), or from about 1000 mm (the door he has already approved in the game, one pane and no bar: rita-day-kit-2026-10-06.jpg)?", "recommended": "871 (the photograph)", "why": "photographs win; the 8 October door review failed on exactly such details; 1000 would keep the approved door as it is, 600 is the earlier target's"},
    {"q": "Rita's room flattened so nothing smears at 1.5 m (the counter goes to the back wall, both side units go and become flat boards, the long-case clock and the cabinet go, the stock wall is 0.30 deep): approve?", "recommended": "Yes", "why": "Rita's room is the approved model (RULINGS 2 Oct) and its composition changes, so it comes to him on one page before merging; before: the approved pawnbroker_day.png (6 October); after: D3 (production/previews/cloud-week/refs/shop-windows/D3-ritas-room-plan-picture.jpg) until the builder's first render replaces it"},
]


def checks(t):
    C = []

    def add(id_, name, what, expected, tol, applies, kind, how):
        C.append({"id": id_, "name": name, "what": what, "expected": expected, "tolerance": tol, "applies_to": applies, "kind": kind, "how": how})
    rooms = [s["id"] for s in t["shops"] if s.get("room")]
    lit = [s["id"] for s in t["shops"] if s.get("room") and s["lit_at_night"]]
    dark = [s["id"] for s in t["shops"] if s.get("room") and not s["lit_at_night"]]
    allshops = [s["id"] for s in t["shops"]]
    add("PIC-01", "picture files", "each state's PNG is 4096 x 1855, 8-bit sRGB, with the JSON beside it holding w, h, d, camera_d, pixels, states", "w 5.3, h 2.4, d per shop, camera_d 5.3", "exact", rooms, "picture", "read the files")
    add("PIC-02", "no black void in the picture", "mean Rec.709 luma of the day / night_lit picture; the share of pixels under 12; the largest connected region under 12",
        "day mean >= 83.7 and night_lit mean >= 55.9 (0.7 of Rita's approved 119.5 and 79.8); share under 12 <= 0.03; no region under 12 larger than 3 per cent of the area", "none", rooms, "picture", "numpy on the PNG")
    add("PIC-03", "night_dark is dark, not black", "mean luma of the night_dark picture", "12.4 to 40 (Rita's approved 17.7, 0.7 to 2.3 times)", "none", rooms, "picture", "numpy")
    add("PIC-04", "the floor line and the back wall where the rule puts them", "a flat-colour pass (one colour a surface) of the room; the back wall's four corners in the 4096 x 1855 picture",
        "for D 4.5: top-left and bottom-right corners as method.floor_and_back_wall.back_wall_in_picture.px_4096 (about (940, 426) and (3156, 1429)); for another D recomputed by the rule", "+-8 px on each corner", rooms, "picture", "project(x, y, z) of tools/ue/make_interior_material.py against the pass")
    add("PIC-05", "nothing burnt", "share of pixels with any channel at 250 or above", "<= 0.01 in every picture", "none", rooms, "picture", "numpy")
    add("PIC-06", "each surface has texture", "the standard deviation of the luma inside the back wall's rectangle, the floor's trapezoid and each side wall's trapezoid", ">= 6 levels in each (not a flat colour)", "none", rooms, "picture", "from the flat-colour pass masks")
    add("PRJ-01", "the identity camera", "from the render camera (card centre, 5.3 m in front, mid height) every card point shows its own picture pixel", "|u - u0| and |v - v0| <= 1 px at 4096", "1 px", rooms, "projection", "trace() on a grid of 41 x 21 card points")
    add("PRJ-02", "the room shifts with the eye", "between CLOSE_35 and CLOSE_35_B (2.0 m apart along the street) the back wall's centre point lands at picture columns that differ by the rule's value, and the whole card picture differs",
        "the column difference equals target.json's `parallax_test.expected_du_px` per shop; the mean absolute difference of the two baked card pictures >= 8 levels", "+-1.5 px; none", rooms, "projection", "trace() for both cameras; compare to the builder's render. THIS RUNS ON THE GATE'S OWN `trace` BAKE, so it proves the gate, not the game: the game's own card is owed on the PC (owed_on_pc PC-01)")
    add("PRJ-03", "the gate shows the game's rule", "the baked card picture for a camera equals the picture sampled through trace() for the same camera and card", "mean absolute difference <= 0.5 level, no pixel off by more than 3", "none", rooms, "projection", "recompute with the imported trace")
    add("SO-01", "back wall stand-off", "the stand-off (depth) of every fixture on the back wall", "shelf units and their goods <= 0.30 (the written rule; the named exceptions in method.standoff_rules_m.shelf_named_exceptions: Rita's R-back-tv-tiers 0.35, within the 20 px budget at the card's middle), counters, machines and free pieces at the wall <= 0.60 tolerated, nothing deeper", "none", rooms, "room", "fixtures[].depth_m against method.standoff_rules_m (the builder also measures the built meshes' bounding boxes)")
    add("SO-02", "side wall stand-off", "the stand-off of every fixture and every placed good on a side wall", "<= 0.05 flat, <= 0.10 tolerated, nothing deeper", "none", rooms, "room", "as SO-01")
    add("SO-03", "floor and ceiling stand-off", "the height of every thing on the floor, the drop of every thing from the ceiling", "<= 0.025 true, <= 0.05 tolerated (a batten fitting 0.045)", "none", rooms, "room", "as SO-01")
    add("SO-04", "nothing in the middle of the room", "any mesh whose bounding box is more than 0.60 m from every wall and more than 0.05 above the floor", "none", "none", rooms, "room", "scan the built scene")
    add("SO-05", "nothing stands across a door", "back-wall fixtures of kind door against every other back-wall fixture: no shelf unit, counter or machine overlaps a door's x range below the door's top (Rita's back door x 1.45 to 2.35, z 0 to 2.0: the stock wall ends at x 1.35 and only one tier of boxes at z 2.05 to 2.25 stands over it); the built shelves stop at the door and the night_dark back-room light has its opening", "no overlap", "none", rooms, "room", "fixtures[] extents; the builder's bounding boxes")
    add("DSP-01", "the display stands in the window", "every display item's extent against the window zone and the envelope: u inside the window zone, v 0 to 0.55 from the back of the glass, w from the bed to height_max_w", "all inside; none in front of the shop door or the side door", "5 mm", rooms, "display", "bounding boxes of the built display against the 2.2 zones")
    add("DSP-02", "real geometry in the display", "every display item is a mesh (no card, no picture), none a flat alpha cut-out except price cards 3 mm thick", "true", "none", rooms, "display", "scan the glb")
    add("INV-01", "inventory exists", "each Poly Haven id in the inventory exists with a 1k glTF", "true for every model in the inventory", "none", rooms, "inventory", "self_check.py (offline from polyhaven_checked.json; --live re-asks the API)")
    add("INV-02", "nothing denied is placed", "the build's inventory.json against inventory.denied", "no denied id", "none", rooms, "inventory", "set difference")
    add("INV-03", "every model is allowed", "every model placed is in inventory.polyhaven, inventory.scripted or a Sketchfab uid of inventory.sketchfab_checked", "true", "none", rooms, "inventory", "set difference")
    add("INV-04", "scripted goods are the listed ones and carry a why", "every scripted object name is a key of inventory.scripted; no fish, crab or prawn is a scripted body", "true", "none", rooms, "inventory", "set difference and a name scan ('fish', 'cod', 'mackerel', 'crab', 'prawn' only from a scan uid)")
    add("INV-05", "no maker marks", "every base-colour map of every placed model and every label tile is searched (by eye on a 2k sheet at the gate; by script: the manifest text, which cannot see a printed word) for inventory.brand_blocklist words; the approved pawnbroker pictures (pawnbroker_day, _night_lit, _night_dark) are searched by eye at full size for the same mark ('Dixons' on cassette_player, 4 px high at 2048 wide); every model's 1k maps are looked at before the build (step 0), not only at the gate", "none found", "none", rooms, "inventory", "text scan of manifests and the glyph lists; eyes on the sheet and on the approved pictures")
    add("INV-06", "the final textures carry no mark", "for every model with `marks` in the inventory: the blanking step ran on the listed map and boxes (inventory.texture_marks.step) and the model's glTF points at the clean map; the final texture is tested in each listed box and looked at in full", "script: in each box the largest difference from the ring colour is at most 24 levels and under 2 per cent of the pixels have a gradient above 40; visual (where a script cannot test it): the builder reads the final map at 100 per cent beside the original and no word, number, logo, face or sticker is legible", "24 levels; 2 per cent", rooms, "inventory", "numpy on the clean maps for the boxes; the builder's eyes for the rest (a mark outside the boxes is a new entry)")
    add("NEV-01", "no people, drink, betting, children", "object, material and text names and every glyph string of the build against inventory.content_blocklist", "no match", "none", allshops, "never", "string scan")
    add("NEV-02", "nothing after 1992", "no model from inventory.denied; no modern phone, flat screen, cordless-drill or LED lamp in any inventory", "true", "none", allshops, "never", "inventory")
    add("FRN-01", "the front's parts at their sizes", "the 3.2 check's rows for the assembled bay (pilaster 350 slot / 290 shaft / 140 proud, console 240 x 205 x 550, fascia 5410 x 550 x 120, cornice 150, sill 75, stallriser 600, window frame at the shop's variant, transom 2400 to 2480 and head 2790 to 2850 over the window; what stands over the DOORS is FRN-07's)", "as 2.2's checks", "as 2.2's", allshops, "front", "check_shopfront.py rows that apply")
    add("FRN-02", "window and door zones", "u of the window, shop door and side door against front.zones_u_mm; their centres against front.centres_street_x_m", "equal", "2 mm; 3 mm", allshops, "front", "bounding boxes")
    add("FRN-03", "the shop door", "T1: leaf 900 x 2040 at z 28, glass 871 to 1973 with one bar at 1423 (28 wide), lock rail 549 to 871, letter plate 250 x 40 at z 678, lever side and hinge side as the table, the bell at z 1950 to 2050 inside; M1: glass 198 to 1968 and the letter plate centred in the 170 bottom rail at z 113 (outside the glass); M2: glass from 600 and the plate at 545 in the kick panel; the plate's z range never overlaps the door's glass (door.glass_z_mm)", "equal", "5 mm", allshops, "front", "bounding boxes")
    add("FRN-04", "the glass and the toplight layout", "per shop: the number of lights and toplights; 6 mm plate at d 30; no pane in front of another; the toplight bars' centres, the bar on every mullion line and the width of every toplight (D6: each mullion carried up as a bar of its own width, each light's toplight split equally)",
        "lights = n_mullions + 1; toplights = front.toplights_as_built = glazing_layout.toplights (Rita's and the newsagent's: nine of 326.9, bars at 390.9, 745.8, 1497.6, 1852.5, 2604.2, 2959.1 plus the two mullions carried up; the empty unit nine of 324.7; the ironmonger six of 509.7; the grocer six of 683.0; the tea room six of 504.4; the launderette two of 1600); a bar on every mullion line; every toplight at least 250 wide; the toplights of one light equal within 1 mm; no toplight sliver beside a mullion; the over-door toplights are three equal panes (door.toplights_over_shop_door)",
        "bar centres +-2 mm; widths +-1 mm", allshops, "front", "bounding boxes of the glass and the bars against glazing_layout (the count alone passed the unaligned layout the 3.2 street review failed)")
    add("FRN-05", "paint colours", "the base colour of each painted part against front.paint_srgb", "within 6 levels per channel (aged paint: the 2.2 values)", "6", allshops, "front", "material values")
    add("FRN-06", "lobby", "the grocer's door recessed 600 and the launderette's 300, floors as 2.2", "equal", "5 mm", ["grocer", "steam_laundry"], "front", "bounding boxes")
    add("FRN-07", "no opening in the front", "on the elevation drawn from target.json (target_drawing.front_polys), every point between the pilasters' inner edges (u 350 to 5650) from z 0 to 2850 lies on a part: stallriser, sill, window frame, glass, door (threshold, jambs, stop, leaf), fanlight, transom, toplight, panel, head, hood; Rita's: the band above the doors is door.fanlight (u 1344 to 2250, z 2131 to 2400), door.transom (u 350 to 2300, z 2400 to 2480), door.toplights_over_shop_door (three of 283.3, bars at 1641.3 and 1952.7, z 2480 to 2790), door.panel_over_side_door (844 wide field in a 944 slot, z 2480 to 2790) and door.head (u 350 to 2300, z 2790 to 2850)",
    "the largest uncovered rectangle is at most 5 x 5 mm", "5 x 5 mm", allshops, "front", "self_check.py computes it on the drawing's parts (rectangles grown by 0.05 mm against rounding); the built front's bounding boxes are held to the same list by the build")
    add("FAS-01", "the fascia's sign in place", "the 4.1 board texture on the fascia board (sample 12 points of the board's front: the render's base colour against the PNG at the same u, v); the applied sign (Mickey's letters, laundry and newsagent box, tea room panel) at the 2.2 u and z", "equal", "3 levels; 5 mm", allshops, "fascia", "render with the shop's light off; compare")
    add("FAS-02", "hanging signs", "Rita's three balls, the laundry's box, the ironmonger's and the chandler's boards at their 4.1 mounts", "equal", "10 mm", ["ritas", "steam_laundry", "ironmonger", "chandler"], "fascia", "bounding boxes")
    add("GLS-01", "nothing across the glass", "every object between the glass and the street plane is one of: the 4.1 glass rows, the OPEN/CLOSED sign, the hours plate, SB1 (newsagent), the letting board (empty unit), the night grille (Rita's) or mesh (chandler)", "true", "none", allshops, "glass", "scan")
    add("LIT-01", "lit shops lit at night, dark shops dark", "mean luma of the room-only composite (picture x brightness 0.7, glass reflection off) over the glass lights in STREET_SQUARE at night", "lit: >= 45; dark: 10 to 35; the difference between a lit shop and the same shop dark >= 25", "none", rooms, "night", "the cloud gate's render; lit = %s; dark = %s" % (", ".join(lit), ", ".join(dark)))
    add("LIT-02", "no black void in the street view", "mean luma of the room-only composite over the glass lights, by day, in STREET_SQUARE, STREET_30 and CLOSE_35", ">= 33 by day; >= 45 at night for the lit shops", "none", rooms, "composite", "the cloud gate's render; room-only = picture x 0.15 (day) or x 0.7 (night), tone-mapped Standard")
    add("LIT-03", "the empty unit is a pale blank by day, not black", "mean luma of the whitewashed glass in STREET_SQUARE by day", ">= 150 (4.1's whitewash 214,212,204 under the day light); by night <= 40", "none", ["empty_unit"], "composite", "the cloud gate's render")
    add("LIT-04", "Rita's grille", "AT NIGHT the lattice over the window zone: bar 20 x 4, diamond 120, rails 40 x 40 at the transom (z 2.50 above the crown, 2400 above the footway) and 0.70 above the crown, plane 100 in front of the glass; the lit window seen through it. BY DAY the lattice is lifted out and stored inside and only the top rail and the bottom channel (powder black, with their fixing plates on the pilaster shafts) stand", "equal", "5 mm", ["ritas"], "night", "bounding boxes and the night render (by day: the rail and channel only)")
    add("LIT-05", "the display is lit at night", "in STREET_SQUARE at night, for each of the six lit shops, the display zone (the window lights' lowest 0.85 m, over the bed: z 0.70 to 1.55 above the crown, across the window zone) has a mean luma of at least 45, with the spec's spill modelled in the gate (the 350 lm rect light in the window head, tipped 62 degrees down, lighting channel 1: shop-interiors.json pawnbroker.lit_note); LIT-01 and LIT-02 are room-only and cannot see a dark window bed in a lit shop", ">= 45 for %s" % ", ".join(sorted(s_["id"] for s_ in t["shops"] if s_["lit_at_night"])), "none", sorted(s_["id"] for s_ in t["shops"] if s_["lit_at_night"]), "night", "the cloud gate's render with the spill light modelled")
    add("LIT-06", "the sodium wash is the game's", "every room's night_dark sodium wash colour against production/specs/unreal-look.json lantern_linear_rgb (linear 1.0, 0.25, 0.0; the scene file's 1.0, 0.7055, 0.0 is stale: QUEUE.md 9 Oct 12:10)", "equal", "0.01", rooms, "night", "the render's light colour")
    add("PRV-01", "the previews show nothing they must not", "every mask of the photograph previews (extras.PREVIEW_PHOTOS, original pixels) is flat grey in the committed JPEG; no real firm's name, door number, face, drink or gambling sign or child is legible in any of the eleven previews", "flat grey (120) in each mask; nothing legible", "6 levels, std 4", allshops, "previews", "make_previews.py reads each mask back from the written JPEG; self_check.py reads the committed JPEGs; a look by eye at every preview")
    add("CAM-01", "the cameras are the named ones", "each render's camera against cameras.definitions and the shop's eye and aim", "equal", "5 mm; 0.1 degree", rooms, "camera", "read the render's camera")
    return C


def merge(t):
    n_models = len(t["inventory"]["polyhaven"])
    n_scripted = len(t["inventory"]["scripted"])
    t["summary_line"] = ("Shop windows: ten units as built (twelve not found); eight rooms of %d checked CC0 models and %d named scripted forms, rendered 4096 wide to the game's own `trace` rule, "
                         "stock only where that rule can show it and the near 0.55 m a real display; the fish scans wait on one login." % (n_models, n_scripted))
    for fl in FAILURES:
        if isinstance(fl["answer"], str):
            fl["answer"] = fl["answer"].replace("105 Poly Haven models", "%d Poly Haven models" % n_models).replace("52 kinds", "%d kinds" % n_scripted)
    for s_ in SOURCES:
        s_["what"] = s_["what"].replace("each of the 105 models used", "each of the %d models used" % n_models)
    t["sources"] = SOURCES
    t["unreached"] = UNREACHED
    pm = json.loads(json.dumps(PHOTO_MEASUREMENTS))
    rr = {r_["what"]: r_ for r_ in pm["rows"]}
    top_, bot_ = rr["door leaf top (underside of the transom's board)"]["y_px"], rr["door leaf bottom / threshold"]["y_px"]
    k_ = 2040.0 / (bot_ - top_)
    def zz(w_):
        return round((bot_ - rr[w_]["y_px"]) * k_ + 28.0, 0)
    pm["derived_mm_from_the_leaf_height_2040"] = {"mm_per_pixel": round(k_, 4), "heights_above_the_footway_mm": {w_: zz(w_) for w_ in ("glass top", "glazing bar, centre", "glass foot", "letter plate, centre", "number plate, centre", "handle, centre", "lower panel field, top", "lower panel field, bottom", "stallriser top (tile cap)")},
                                                  "leaf_width_mm": round((rr["leaf right edge"]["x_px"] - rr["leaf left edge"]["x_px"]) * k_), "glass_width_mm": round((rr["glass right"]["x_px"] - rr["glass left"]["x_px"]) * k_),
                                                  "error": "+-3 px = +-18 mm a row, plus the assumption that the leaf is 2040 high (a 2100 leaf moves every height by 3 per cent)"}
    t["photographs"] = pm
    t["disagreements_photographs_win"] = DISAGREEMENTS
    t["previous_failures_answered"] = FAILURES
    t["reuse"] = REUSE
    t["could_not_settle"] = COULD_NOT_SETTLE
    t["needs_you"] = NEEDS_YOU
    t["checks"] = checks(t)
    # ---- the maps' marks: every model carries `marks` (what was seen) and, where there is one, the exact blanking step ---------------------------------------
    inv = t["inventory"]
    for mid, rec in inv["polyhaven"].items():
        if mid in MARKS:
            m_ = MARKS[mid]
            rec["marks"] = m_["marks"]
            rec["blank"] = m_["blank"]
            rec["keep"] = m_["keep"]
            if m_.get("note"):
                rec["marks_note"] = m_["note"]
        else:
            rec["marks"] = None
            rec["looked_at_1k"] = "no mark seen on the 1k base-colour map at 512 px (writer, 12 Oct); the builder re-reads it at 1k before placing it (step 0)"
    inv["texture_marks"] = {"models_with_marks": sorted(k for k in MARKS if k in inv["polyhaven"]), "marks_for_models_not_in_the_inventory": sorted(k for k in MARKS if k not in inv["polyhaven"]),
                            "step": BLANK_STEP, "final_check": FINAL_CHECK, "map_frame": "pixels of the model's 1k glTF base-colour map, 1024 x 1024, origin top left, [x0, y0, x1, y1]",
                            "looked_at": "all %d models' 1k base-colour maps on 12 October after the review (25 contact sheets at 512 px; the marked ones at 1k with the boxes drawn on them); thumbnails alone had missed 'Dixons'" % len(inv["polyhaven"]),
                            "the_approved_pictures": "pawnbroker_day.png, _night_lit.png, _night_dark.png (approved 6 October) were made with cassette_player and Camera_01 among the stock: the builder reads their back walls at full size for the marks above (could_not_settle, first item)"}
    inv["rule"] = ("every model a build places is listed in its inventory.json; each must be in `polyhaven`, `scripted` or a Sketchfab uid of `sketchfab_checked`; none in `denied`; no object, material or text "
                   "contains a word of the blocklists; every Poly Haven model's 1k maps are looked at BEFORE the build (step 0) and every maker's mark is painted out of its base-colour map exactly as that model's `blank` step says "
                   "(`texture_marks`); the gate then tests the listed boxes and the builder looks at the final map (INV-06); the approved pawnbroker pictures are searched by eye at full size for the same marks (INV-05)")
    for e_ in t["shops"]:
        if e_.get("room"):
            for row in e_["room"]["goods"] + e_["display"]["items"]:
                if row["model"] in MARKS:
                    nt = row.get("note") or ""
                    if not any(w_ in nt for w_ in ("blanked", "painted out", "replaced", "atlas")):
                        row["note"] = (nt + "; " if nt else "") + "mark blanked as `inventory.polyhaven[%s].marks` says" % row["model"]
    t["owed_on_pc"] = [
        {"id": "PC-01", "for": "PRJ-02", "what": "from CLOSE_35 and CLOSE_35_B in the packaged game, a marker at the picture's centre moves as `trace` predicts (Rita's: 1322 px of 4096, +-20)", "why": "PRJ-02 runs on the gate's own trace() bake and proves the gate, not the game"},
        {"id": "PC-02", "for": "LIT-05", "what": "in the packaged game at night, the lit shops' window beds read at a mean luma of 45 or more in STREET_SQUARE with the game's own spill light", "why": "the gate models the spill; Lumen's own light on the display is the game's"},
        {"id": "PC-03", "for": "the glass, TSR, exposure", "what": "the game's glass reflection, the card's motion vectors under TSR, the exposure and the frame time", "why": "named in gate_in_the_cloud.what_it_cannot_show"},
    ]
    t["previews"] = {"folder": "production/previews/cloud-week/refs/shop-windows/", "grey": list(MASK_GREY), "photos": PREVIEW_PHOTOS,
                     "drawings": {"D1": "Rita's bay in millimetres, every part including the band above the doors (fanlight, transom, three toplights, panel, head)", "D2": "the ten fronts, the same", "D3": "Rita's room: plan, back wall with stand-off classes and side walls, the picture's layout", "D4": "the stand-off chart and the camera plan"},
                     "rule": "every preview is looked at by eye after each rebuild; make_previews.py draws the masks and reads them back from the JPEG it wrote; the files are JPEG, at most 1200 px, under 300 KB"}
    # the parallax test per shop: the predicted shift of the back wall's centre point between the two close cameras
    import sw_common as S
    scene = S.load_scene()
    for s in t["shops"]:
        if not s.get("room"):
            continue
        card = S.card_of(scene, s["block"], s["bay"])
        D = s["room"]["d"]
        res = {}
        for cn in ("CLOSE_35", "CLOSE_35_B"):
            import numpy as np
            wc = s["front"]["centres_street_x_m"]["window"]
            eye, _ = S.camera_pose(cn, card, wc)
            # the game's trace on a card of this side: the eye and the point in the card frame; for a west card trace's own side=-1 rule applies
            side = card["side"]
            ec = S.to_card(eye, card)
            P = np.array([S.W / 2.0, 0.0, S.H / 2.0])                       # the card's centre
            u, v = S.trace(tuple(P), tuple(ec), (S.W, S.H, D), S.CAMERA_D, side)
            res[cn] = [u, v]
        du = (res["CLOSE_35_B"][0] - res["CLOSE_35"][0]) * 4096.0
        s["parallax_test"] = {"point": "the card's centre", "u_v_close_35": [round(x, 5) for x in res["CLOSE_35"]], "u_v_close_35_b": [round(x, 5) for x in res["CLOSE_35_B"]], "expected_du_px": round(du, 2),
                              "rule": "tools/ue/make_interior_material.py trace(), side %+d, card frame" % (1 if s["side"] == "east" else -1)}
