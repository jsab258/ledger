"""Printed goods from photographs (14 October 2026, try 2; the newsagent's close review, fault 2: "the printed goods read as clip-art placeholders at 100 per cent: about eight flat vector pictures"; the brief's step 0 i).

Every magazine cover, newspaper front page, greeting card and postcard is made here from a photograph and from text laid out by script:

  * the pictures are crops of Poly Haven's CC0 HDRI photographs (the 2k files in SCRATCH/polyhaven/_hdri, fetched by `fetch_sources`; each crop is a row of PHOTOS: which HDRI, which view), tone-mapped the way
    `sw_assets.harbour_print` tones the framed prints (middle grey from the median, a soft shoulder, saturation 0.7, a slight warm cast, paper grain), no person in any view (each view was looked at);
  * the words are the project's own (invented titles and cover lines) and, for the newspapers' body columns, public-domain prose (Project Gutenberg's The Natural History of Selborne, 1789, and The Voyage of
    the Beagle, 1839: both long out of copyright), filtered for the content rule (no alcohol, gambling or children) and cut into columns by script;
  * no repeated vector clip-art: every good takes its own photograph (`USED` records which, so that the checks can compare), a magazine's masthead sits on the top 18 per cent, 3 to 5 cover lines in two sizes lie
    over the photograph, the price (95p to 1.50) and OCTOBER 1990 stand in the top corner, no barcode, a spine strip on the left edge.

Nothing here knows a shop: the layouts (sw_shops_news.py, sw_shops_tea.py, sw_room_gen.py) ask for an atlas and get the rectangle of each good in it.
"""
import json
import math
import os
import random
import re

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from scipy import ndimage

import sw_assets as A
import sw_gen as GEN

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
FONTS = os.path.join(REPO, "production", "fonts")
SCRATCH = os.environ.get("LEDGER_SW_SCRATCH", "/home/user/ledger-scratch")
HDRI_DIR = os.path.join(SCRATCH, "polyhaven", "_hdri")
TEXT_DIR = os.path.join(SCRATCH, "shop-windows", "prints")

USED = {}                  # {good's id: photo id}: written to prints_used.json beside each shop's pictures, read by the checks
FIT = {}                   # {paper's masthead: [the headline's lines]} as drawn: the check joins them and compares with the headline (every word whole)
TEXTS = []                 # every string drawn (the brand-blocklist check reads them)

# ---------------------------------------------------------------------------------------------------------------------------------------------------------- the photographs
# id: (HDRI, yaw, pitch, horizontal field, what it shows (the caption words), grade). Every view was looked at: no person, no sign, no modern block in it.
PHOTOS = {
    "garden_shrubs":   ("garden_nook", 0, 4, 62, "a garden of shrubs", "warm"),
    "garden_oak":      ("garden_nook", 90, 4, 62, "an oak in a park", "warm"),
    "garden_lawn":     ("garden_nook", 180, 6, 62, "a tree on the lawn", "warm"),
    "park_gold":       ("autumn_park", 0, 6, 62, "autumn trees", "warm"),
    "park_elms":       ("autumn_park", 90, 6, 62, "elms in autumn", "warm"),
    "park_fence":      ("autumn_park", 180, 4, 62, "a field and a fence", "warm"),
    "park_birch":      ("autumn_park", 270, 6, 62, "birches in a field", "warm"),
    "hills_wide":      ("autumn_hill_view", 0, 3, 66, "the hills", "warm"),
    "hills_valley":    ("autumn_hill_view", 90, 3, 62, "a valley in autumn", "warm"),
    "hills_ridge":     ("autumn_hill_view", 180, 4, 60, "the ridge", "warm"),
    "hills_village":   ("autumn_hill_view", 270, 3, 58, "a village in the valley", "warm"),
    "field_bush":      ("autumn_field", 90, 4, 60, "a thorn tree in a field", "warm"),
    "field_wide":      ("autumn_field", 180, 3, 62, "open fields", "warm"),
    "road_bend":       ("autumn_road", 90, 2, 62, "a country road", "neutral"),
    "road_hedge":      ("autumn_road", 270, 2, 60, "the road and the hedge", "neutral"),
    "farm_track":      ("farm_road", 0, 3, 62, "a farm track", "neutral"),
    "farm_track2":     ("farm_road", 180, 3, 62, "the farm road", "neutral"),
    "farm_rows":       ("farmland_overcast", 90, 3, 62, "furrows to the hedge", "neutral"),
    "farm_green":      ("farmland_overcast", 270, 3, 62, "a green field", "neutral"),
    "farmhouse_oak":   ("belfast_farmhouse", 180, 3, 62, "an old oak by a farm", "warm"),
    "farmhouse_reeds": ("belfast_farmhouse", 0, 3, 62, "reeds on the hill", "warm"),
    "farmhouse_trees": ("belfast_farmhouse", 270, 3, 60, "trees on the bank", "warm"),
    "meadow_trees":    ("belfast_open_field", 90, 3, 62, "trees across a meadow", "cool"),
    "meadow_wood":     ("belfast_open_field", 270, 3, 60, "a wood across the meadow", "cool"),
    "hay_rows":        ("hay_bales", 0, 4, 62, "stubble and bales", "warm"),
    "hay_bales":       ("hay_bales", 90, 3, 62, "a round bale", "warm"),
    "hay_trees":       ("hay_bales", 180, 3, 62, "bales under the trees", "warm"),
    "hay_hill":        ("hay_bales", 270, 3, 62, "bales and clouds", "warm"),
    "rocks_range":     ("kiara_5_noon", 0, 4, 66, "the high hills", "warm"),
    "rocks_crag":      ("kiara_5_noon", 180, 4, 60, "a crag in the hills", "warm"),
    "river_lake":      ("near_the_river_01", 90, 3, 62, "the lake shore", "cool"),
    "river_path":      ("near_the_river_01", 180, 3, 62, "a path by the river", "cool"),
    "river_bare":      ("near_the_river_01", 0, 3, 62, "bare trees by the water", "cool"),
    "river2_birch":    ("near_the_river_02", 270, 3, 60, "birches on the bank", "cool"),
    "river2_pool":     ("near_the_river_02", 180, 3, 62, "a quiet pool", "cool"),
    "river2_reeds":    ("near_the_river_02", 0, 3, 62, "the reed bed", "cool"),
    "falls":           ("monbachtal_riverbank", 0, 3, 60, "a waterfall in the wood", "neutral"),
    "wood_rock":       ("monbachtal_riverbank", 90, 3, 58, "a mossy rock in the wood", "neutral"),
    "wood_log":        ("monbachtal_riverbank", 180, 3, 58, "a fallen log", "neutral"),
    "wood_ledge":      ("monbachtal_riverbank", 270, 3, 58, "a rock ledge", "neutral"),
    "lake_sun":        ("lake_pier", 0, 3, 62, "the lake in the sun", "cool"),
    "lake_pier":       ("lake_pier", 180, 3, 62, "the pier and the masts", "cool"),
    "lake_harbour":    ("lake_pier", 225, 3, 56, "the harbour wall", "cool"),
    "lake_open":       ("lake_pier", 90, 3, 62, "open water", "cool"),
    "pier_posts":      ("ouchy_pier", 0, 3, 62, "posts in the bay", "cool"),
    "pier_calm":       ("ouchy_pier", 180, 3, 62, "a calm bay", "cool"),
    "jetty":           ("bell_park_pier", 270, 3, 62, "the jetty", "cool"),
    "jetty_hills":     ("bell_park_pier", 0, 3, 62, "hills over the water", "cool"),
    "jetty_water":     ("bell_park_pier", 180, 3, 62, "a green hill by the water", "cool"),
    "cliff_mist":      ("white_cliff_top", 0, 3, 64, "mist on the cape", "cool"),
    "cliff_rocks":     ("white_cliff_top", 90, 3, 60, "rocks at the cliff top", "cool"),
    "cliff_sea":       ("white_cliff_top", 180, 4, 62, "the open sea", "cool"),
    "cliff_surf":      ("white_cliff_top", 270, 3, 60, "surf on the rocks", "cool"),
    "headland_seats":  ("dalkey_view", 90, 3, 62, "seats on the headland", "cool"),
    "headland_cedar":  ("dalkey_view", 180, 3, 60, "a cedar over the sea", "cool"),
    "headland_island": ("dalkey_view", 270, 3, 62, "the island in the bay", "cool"),
    "beach_huts":      ("fish_hoek_beach", 195, 6, 52, "the beach huts", "warm"),
    "beach_dusk":      ("fish_hoek_beach", 90, 4, 62, "the beach at dusk", "warm"),
    "beach_sunrise":   ("blouberg_sunrise_1", 0, 3, 62, "the bay at sunrise", "warm"),
    "beach_sunrise2":  ("blouberg_sunrise_1", 90, 3, 62, "the shore at sunrise", "warm"),
    "lakeshore":       ("lakeside", 0, 3, 62, "a shore of trees", "cool"),
    "lakeside_calm":   ("lakeside", 90, 3, 62, "the calm lake", "cool"),
    "lakeside_hill":   ("lakeside", 180, 3, 62, "the hill over the lake", "cool"),
    "reeds_water":     ("gray_pier", 0, 3, 62, "reeds and reflections", "cool"),
    "pond_planks":     ("gray_pier", 90, 3, 62, "a boardwalk to the pond", "cool"),
    "pond_birch":      ("gray_pier", 270, 3, 62, "birches over the pond", "cool"),
    "dunes":           ("poolbeg", 0, 3, 62, "the dunes", "warm"),
    "dune_path":       ("poolbeg", 270, 3, 62, "a path through the dunes", "warm"),
}


def font_file(folder, name, size):
    return ImageFont.truetype(os.path.join(FONTS, folder, name), size)


WEIGHT = {"josefin-sans": 700, "jost": 500, "archivo": 800, "oswald": 500, "libre-franklin": 700, "fraunces": 700}       # the variable faces' default is their thinnest or their regular: the weight a masthead or a cover line wants


def fnt(folder, size, name=None):
    f = font_file(folder, name, size) if name else GEN.font(folder, size)
    if not name and folder in WEIGHT:
        try:
            axes = f.get_variation_axes()
            vals = []
            for ax in axes:
                nm = ax["name"] if isinstance(ax["name"], str) else ax["name"].decode()
                vals.append(min(max(WEIGHT[folder], ax["minimum"]), ax["maximum"]) if "eight" in nm else ax["default"])
            f.set_variation_by_axes(vals)
        except Exception:                                    # noqa: BLE001
            pass
    return f


# ---------------------------------------------------------------------------------------------------------------------------------------------------------- sources
def fetch_sources(log=print):
    """The HDRIs the photographs need, if missing (Poly Haven, CC0; tools/art-recipes/fetch_polyhaven.py's neighbour in the scratchpad did the first fetch)."""
    import subprocess
    os.makedirs(HDRI_DIR, exist_ok=True)
    for h in sorted({v[0] for v in PHOTOS.values()}):
        p = os.path.join(HDRI_DIR, h + "_2k.hdr")
        if os.path.exists(p) and os.path.getsize(p) > 1e6:
            continue
        meta = json.loads(subprocess.check_output(["curl", "-sS", "-m", "60", "https://api.polyhaven.com/files/%s" % h]))
        url = meta["hdri"]["2k"]["hdr"]["url"]
        subprocess.check_call(["curl", "-sS", "-m", "240", "-o", p, url])
        log("fetched HDRI %s (%d bytes)" % (h, os.path.getsize(p)))


_ENV = {}


def _env(h):
    if h not in _ENV:
        _ENV[h] = A._load_hdri(os.path.join(HDRI_DIR, h + "_2k.hdr"))
    return _ENV[h]


GRADE = {"warm": np.array([1.06, 1.0, 0.90]), "neutral": np.array([1.03, 1.0, 0.95]), "cool": np.array([0.98, 1.0, 1.03])}


def photo(pid, w, h, seed=1, mono=False, contrast=1.0, mid=0.24, grain=True):
    """The photograph `pid` cropped to w x h px (float 0..1, rows top first): the HDRI view at the crop's own shape, tone-mapped (middle grey `mid` from the median, a soft shoulder, saturation 0.7 (0 when
    `mono`), a warm or cool cast by its grade), a little contrast, paper grain."""
    hd, yaw, pitch, fov, _, grade = PHOTOS[pid]
    # the field is for a 4:3 view; a taller crop (a magazine cover) takes a narrower horizontal field (the view is rectilinear: nothing is stretched)
    view = A._rect_view(_env(hd), yaw, pitch, fov * 0.80 if h > w else fov, w, h)
    lum = 0.2126 * view[..., 0] + 0.7152 * view[..., 1] + 0.0722 * view[..., 2]
    view = view * (mid / max(float(np.median(lum)), 1e-4))
    view = view / (1.0 + view * 0.55)
    view = np.clip(view, 0, 1) ** (1 / 2.2)
    if contrast != 1.0:
        view = np.clip(0.5 + (view - 0.5) * contrast, 0, 1)
    g = (0.2126 * view[..., 0] + 0.7152 * view[..., 1] + 0.0722 * view[..., 2])[..., None]
    view = g + (view - g) * (0.0 if mono else 0.72)
    view = view * (np.array([1.0, 1.0, 1.0]) if mono else GRADE[grade])
    if grain:
        rng = np.random.default_rng(seed)
        view = view + ndimage.gaussian_filter(rng.normal(0, 0.020, view.shape), (0.6, 0.6, 0)) + rng.normal(0, 0.006, view.shape)
    return np.clip(view, 0, 1).astype(np.float32)


def pil(arr):
    return Image.fromarray((np.clip(arr, 0, 1) * 255 + 0.5).astype(np.uint8))


# ---------------------------------------------------------------------------------------------------------------------------------------------------------- public-domain prose
BAD = re.compile(r"\b(wine|beer|ale|brandy|gin|rum|whisky|whiskey|liquor|drunk|drunken|tavern|inn|alehouse|publican|spirits|cider|mead|brew|bet|bets|betting|wager|gamble|gaming|lottery|dice|cards|children|child|boy|boys|girl|girls|infant|infants|baby|babies|school|schoolboy|nurse|nursery|slave|slaves|slavery|native|natives|savage|savages|negro|negroes|kill|killed|murder|blood|dead|death|died|die|slaughter|naked|gun|guns|shot|musket|pistol|war|battle|massacre)\b", re.I)
_BODY = {}


def body_sentences(book="1408"):
    """Sentences of a Project Gutenberg book (public domain), without the licence header, cut by script and filtered by BAD; cached."""
    if book in _BODY:
        return _BODY[book]
    p = os.path.join(TEXT_DIR, "g%s.txt" % book)
    if not os.path.exists(p):
        os.makedirs(TEXT_DIR, exist_ok=True)
        import subprocess
        subprocess.check_call(["curl", "-sS", "-m", "120", "-L", "-o", p, "https://www.gutenberg.org/cache/epub/%s/pg%s.txt" % (book, book)])
    t = open(p, encoding="utf-8", errors="ignore").read()
    i = t.find("*** START")
    j = t.find("*** END")
    t = t[t.find("\n", i) + 1:j] if i >= 0 else t
    t = t[len(t) // 12:]                       # past the preface
    t = re.sub(r"\[[^\]]*\]", " ", t)
    t = re.sub(r"_", "", t)
    t = re.sub(r"\s+", " ", t)
    sents = [s.strip() for s in re.split(r"(?<=[.!?])\s+(?=[A-Z])", t)]
    out = [s for s in sents if 40 <= len(s) <= 220 and not BAD.search(s) and not re.search(r"\d", s) and s.count(",") <= 4 and "Project Gutenberg" not in s and "CHAPTER" not in s and "LETTER" not in s]
    _BODY[book] = out
    return out


def body_text(n_words, seed, book="1408"):
    rnd = random.Random(seed)
    ss = body_sentences(book)
    words, out = 0, []
    i = rnd.randrange(len(ss))
    while words < n_words:
        s = ss[i % len(ss)]
        out.append(s)
        words += len(s.split())
        i += 1
    return " ".join(out)


# ---------------------------------------------------------------------------------------------------------------------------------------------------------- layout helpers
def _wrap(d, text, f, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= width or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def _fit(d, text, folder, name, width, size0, size_min, max_lines, step=2, line_gap=1.08):
    """The largest type size (stepping down by `step` px) at which `text` wraps to at most `max_lines` lines of `width`, every word whole (the newsagent's close narrow 1: two headlines lost their last word):
    returns (font, lines)."""
    s = size0
    while s >= size_min:
        f = fnt(folder, s, name)
        lines = _wrap(d, text, f, width)
        if len(lines) <= max_lines and all(d.textlength(w, font=f) <= width for w in text.split()):
            return f, lines
        s -= step
    f = fnt(folder, size_min, name)
    return f, _wrap(d, text, f, width)


def _shadow_text(im, xy, text, f, fill, shadow=(0, 0, 0), blur=2, offset=1, alpha=0.8):
    """Text with a soft shadow, on a PIL RGB image."""
    sh = Image.new("L", im.size, 0)
    ImageDraw.Draw(sh).text((xy[0] + offset, xy[1] + offset), text, font=f, fill=int(255 * alpha))
    sh = sh.filter(ImageFilter.GaussianBlur(blur))
    im.paste(Image.new("RGB", im.size, shadow), (0, 0), sh)
    ImageDraw.Draw(im).text(xy, text, font=f, fill=fill)


def _gradient(im, y0, y1, a0, a1, colour=(10, 10, 12)):
    """A dark gradient band from row y0 (alpha a0) to row y1 (alpha a1) over the image."""
    w, h = im.size
    ys = np.arange(h, dtype=np.float32)
    a = np.clip((ys - y0) / max(y1 - y0, 1), 0, 1) * (a1 - a0) + a0
    a = np.where((ys >= min(y0, y1)) & (ys <= max(y0, y1)), a, np.where(ys < min(y0, y1), a0 if y0 < y1 else a1, a1 if y0 < y1 else a0))
    arr = np.asarray(im).astype(np.float32)
    arr = arr * (1 - a[:, None, None]) + np.array(colour, np.float32)[None, None, :] * a[:, None, None]
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))


# ---------------------------------------------------------------------------------------------------------------------------------------------------------- magazines
MAGAZINES = [
    # title, folder/font file for the masthead, photo, grade tweaks (mono), cover lines (the first is the big one)
    ("GARDEN LOG", "abril-fatface", None, "garden_shrubs", False, ["SPRING BULBS NOW", "Pruning roses, step by step", "A greenhouse in a weekend", "Leaves: what to keep"]),
    ("THE GARDENER'S YEAR", "marcellus-sc", None, "garden_lawn", False, ["A MONTH BY MONTH CALENDAR", "Planting out for the spring", "The autumn lawn", "Hedges and boundaries"]),
    ("THE ANGLER'S WEEK", "alfa-slab-one", None, "river_lake", False, ["PIKE FROM THE SHORE", "River reports from the west", "New rods tried", "Float or spinner?"]),
    ("QUAYSIDE MODELLER", "alfa-slab-one", None, "lake_pier", False, ["A HARBOUR IN OO GAUGE", "Scenery in a day", "Building a tug from card", "The quay in miniature"]),
    ("FARMHOUSE COOKING", "fraunces", None, "hay_rows", False, ["THE HARVEST SUPPER", "Bread, puddings and preserves", "Seasonal suppers", "A roast guide"]),
    ("MOTOR WORLD", "alfa-slab-one", None, "road_bend", False, ["THE ROADS OF THE WEST", "Used cars tested", "Twelve cars under 1000 pounds", "Winter care"]),
    ("YACHT AND DINGHY", "old-standard-tt", None, "pier_posts", False, ["THE AUTUMN REGATTAS", "Refitting a small cruiser", "Sails for the winter", "Moorings of the bay"]),
    ("COTTAGE HOMES", "fraunces", None, "farmhouse_oak", False, ["DECORATING ON A BUDGET", "A colour guide for halls", "The country kitchen", "Fireplaces restored"]),
    ("THE WALKER", "oswald", None, "hills_valley", False, ["TEN COASTAL PATHS", "Boots reviewed", "Maps and routes", "The high ridge in autumn"]),
    ("COUNTRY DIARY", "old-standard-tt", None, "park_elms", False, ["HEDGEROWS IN AUTUMN", "Birds of the estuary", "A year in the village", "The last of the leaves"]),
    ("PHOTO MONTHLY", "josefin-sans", None, "cliff_surf", True, ["LANDSCAPES IN BLACK AND WHITE", "Cameras compared", "Filters for the coast", "Printing at home"]),
    ("COAST & SEA", "marcellus-sc", None, "cliff_rocks", False, ["THE WORKING COAST", "Lighthouses of the west", "A walk along the cliffs", "Tides and weather"]),
    ("BIRDWATCH MONTHLY", "archivo", None, "river2_birch", False, ["WINTER VISITORS ARRIVE", "Birds of the estuary", "Hides and how to use them", "Counting the flocks"]),
    ("LAKES & RIVERS", "fraunces", None, "falls", False, ["A DAY BY THE FALLS", "Wild swimming spots", "Canals revisited", "Walks by water"]),
    ("SEASIDE WEEKEND", "abril-fatface", None, "beach_huts", False, ["A WEEKEND BY THE SEA", "Beach huts: a guide", "Where to stay", "The last of the summer"]),
    ("BOAT & HARBOUR", "old-standard-tt", None, "lake_sun", False, ["THE WORKING HARBOUR", "Moorings and berths", "Engines serviced", "The winter lay-up"]),
    ("FARM & FIELD", "oswald", None, "farm_rows", False, ["AFTER THE HARVEST", "Ploughing matches", "The hedge and the ditch", "Machinery sales"]),
    ("VILLAGE LIFE", "marcellus-sc", None, "hills_village", False, ["THE VILLAGE IN AUTUMN", "The church and the green", "Fetes and fairs", "Footpaths reopened"]),
    ("HILL COUNTRY", "alfa-slab-one", None, "rocks_range", False, ["HIGH HILLS IN OCTOBER", "A ridge walk", "Weather in the hills", "Maps and compasses"]),
    ("THE WEEKLY TRAIL", "josefin-sans", None, "jetty", False, ["TO THE END OF THE JETTY", "Short walks for the weekend", "Bridleways", "Kit for the rain"]),
    ("OLD HARBOURS", "abril-fatface", None, "reeds_water", False, ["QUIET WATER", "Harbours of the west coast", "The reed beds", "A painter's view"]),
    ("WILD COAST", "archivo", None, "headland_island", False, ["ISLANDS OF THE BAY", "Cliff paths", "Seabirds in autumn", "A headland walk"]),
    ("THE ALLOTMENT", "fraunces", None, "meadow_trees", False, ["LIFTING THE ROOTS", "Winter digging", "Sheds and tools", "Leeks for the show"]),
    ("WEST COUNTRY WALKS", "oswald", None, "field_bush", False, ["THE OPEN FIELDS", "Stiles and gates", "Thorn and hawthorn", "Maps for October"]),
]
SPINE = (0.10, 0.10, 0.11)


def magazine_cover(idx, size=(384, 512), seed=0):
    """Cover `idx` of MAGAZINES: the photograph full bleed, the masthead across the top 18 per cent over a soft dark band, 3 to 5 cover lines in two sizes over a dark foot, OCTOBER 1990 and the price in the top
    corner, no barcode, a 2 mm spine strip down the left edge (3 px here). Returns a PIL RGB image; registers the photograph in USED."""
    title, mfont, _, pid, mono, lines = MAGAZINES[idx % len(MAGAZINES)]
    w, h = size
    rnd = random.Random(1000 + idx)
    ph = photo(pid, w, h, seed=seed + idx, mono=mono, contrast=1.12)
    im = pil(ph)
    im = _gradient(im, 0, int(h * 0.27), 0.70, 0.0)
    im = _gradient(im, int(h * 0.60), h, 0.0, 0.70)
    d = ImageDraw.Draw(im)
    # the masthead: the title, as large as fits the width in one line (two for a long one), in the cover's own face
    mname = None
    mw = w - 28
    top = int(h * 0.045)
    f, ml = _fit(d, title, mfont, mname, mw, 70, 20, 2 if len(title) > 14 else 1, step=2)
    y = top + int(h * 0.035)
    cream = (246, 240, 226)
    for ln in ml:
        tw = d.textlength(ln, font=f)
        _shadow_text(im, ((w - tw) / 2, y), ln, f, cream, blur=2, offset=2)
        y += int(f.size * 1.05)
    TEXTS.append(title)
    # the date and the price, small, in the top-left corner above the masthead
    price = rnd.choice(["95p", "£1.10", "£1.20", "£1.25", "£1.35", "£1.50"])
    small = fnt("jost", 12)
    d.text((14, 6), "OCTOBER 1990   %s" % price, font=small, fill=(240, 236, 222))
    TEXTS.append("OCTOBER 1990 %s" % price)
    # the cover lines: the first in a large condensed face, the rest smaller, from the lower left
    big = fnt("oswald", 36)
    mid = fnt("jost", 17)
    yy = int(h * 0.64)
    bl = _wrap(d, lines[0], big, w - 40)
    for ln in bl[:2]:
        _shadow_text(im, (16, yy), ln, big, (250, 246, 232), blur=2, offset=2)
        yy += 40
    yy += 6
    for ln in lines[1:4]:
        _shadow_text(im, (16, yy), ln, mid, (240, 236, 222), blur=1, offset=1)
        yy += 24
    TEXTS.extend(lines[:4])
    arr = np.asarray(im).astype(np.float32)
    arr[:, 0:3] = arr[:, 0:3] * 0.45 + np.array([20, 20, 22], np.float32) * 0.55           # the spine
    USED["magazine:%s" % title] = pid
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))


# ---------------------------------------------------------------------------------------------------------------------------------------------------------- newspapers
PAPERS = [
    # masthead, headline, standfirst (two lines), photograph (greys), the masthead's face
    ("THE MERIDIAN HERALD", "COUNCIL APPROVES NEW BRIDGE", "Work to begin on the river crossing in the spring", "river2_pool", "old"),
    ("MERIDIAN EVENING NEWS", "HARBOUR REPAIRS TO BEGIN", "Quay wall closed for six weeks, ferry times change", "lake_harbour", "league"),
    ("WEST COAST DAILY", "RAIN FORECAST FOR THE WEEKEND", "Gales expected on the coast, bridge open", "cliff_sea", "old"),
    ("THE QUAYSIDE MAIL", "TRAWLER BACK IN PORT", "Crew safe after engine failure off the point", "pier_calm", "league"),
    ("MERIDIAN MORNING GAZETTE", "BUS FARES TO RISE IN MAY", "Operator blames fuel costs; passengers protest", "road_hedge", "old"),
    ("THE WEST COUNTRY CHRONICLE", "NEW LIBRARY OPENS ON FRIDAY", "Reading rooms and a lending section for all", "farmhouse_trees", "old"),
    ("THE MERIDIAN LANTERN", "LIGHTS TO BE FITTED ON THE QUAY", "Lamps along the harbour road by the new year", "hay_hill", "league"),
    ("WEST COAST BULLETIN", "GALE DAMAGE TO THE PIER", "Planking lost at the seaward end, repairs promised", "jetty_water", "league"),
]


def halftone(gray, pitch=3.0, angle=45.0, soft=0.9):
    """A dot-screen halftone of a float grey picture (0..1): dots on a rotated grid of `pitch` px, a dot's size by the luma, softened over `soft` px (a screen of 1.2 mm at 2.5 px a mm)."""
    h, w = gray.shape
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    a = math.radians(angle)
    u = (xx * math.cos(a) + yy * math.sin(a)) / pitch
    v = (-xx * math.sin(a) + yy * math.cos(a)) / pitch
    screen = 0.5 - 0.25 * (np.cos(2 * math.pi * u) + np.cos(2 * math.pi * v))        # 0..1, low at the dot's centre
    k = 1.0 / max(soft / pitch * 2.0, 1e-3)
    return np.clip(0.5 + (gray - screen) * k * 0.5, 0, 1)


def newspaper_front(idx, size=(580, 380), seed=0):
    """The visible half of a folded tabloid (0.29 x 0.19 m at 2 px a mm): the masthead between two rules and the date line, a headline that fits (type shrunk in 2 px steps until every word is whole in three
    lines), a halftone of a photograph in greys, and 3 mm body columns of public-domain prose (four columns) below. Returns a PIL RGB image."""
    name, head, sub, pid, face = PAPERS[idx % len(PAPERS)]
    w, h = size
    rnd = random.Random(2000 + idx)
    paper = np.array(rnd.choice([(236, 232, 218), (232, 228, 214), (238, 235, 224)]), np.float32)
    im = Image.new("RGB", size, tuple(int(v) for v in paper))
    d = ImageDraw.Draw(im)
    ink = (26, 26, 30)
    m = 14
    # masthead
    if face == "old":
        f, ml = _fit(d, name, "old-standard-tt", None, w - 2 * m, 46, 22, 1, step=2)
    else:
        f, ml = _fit(d, name, "evening-paper", "LeagueGothic-Regular.ttf", w - 2 * m, 62, 24, 1, step=2)
    d.line((m, 10, w - m, 10), fill=ink, width=3)
    tw = d.textlength(ml[0], font=f)
    d.text(((w - tw) / 2, 14), ml[0], font=f, fill=ink)
    yb = 14 + int(f.size * 1.18)
    d.line((m, yb, w - m, yb), fill=ink, width=1)
    fd = fnt("libre-franklin", 11)
    d.text((m, yb + 3), "WEDNESDAY 17 OCTOBER 1990", font=fd, fill=ink)
    d.text((w - m - d.textlength("PRICE 25p", font=fd), yb + 3), "PRICE 25p", font=fd, fill=ink)
    TEXTS.extend([name, "WEDNESDAY 17 OCTOBER 1990", "PRICE 25p"])
    y = yb + 20
    # headline in the left 58 per cent, the photograph at the right, the standfirst under the headline
    hw = int((w - 2 * m) * 0.60)
    hf, hl = _fit(d, head, "alfa-slab-one", None, hw, 40, 18, 3, step=2, line_gap=1.0)
    yy = y
    for ln in hl:
        d.text((m, yy), ln, font=hf, fill=ink)
        yy += int(hf.size * 1.04)
    TEXTS.append(head)
    FIT[name] = list(hl)
    sf, sl = _fit(d, sub, "evening-paper", "OldStandard-Italic.ttf", hw, 17, 11, 3, step=1)
    yy += 4
    for ln in sl:
        d.text((m, yy), ln, font=sf, fill=ink)
        yy += int(sf.size * 1.2)
    TEXTS.append(sub)
    px0 = m + hw + 12
    ph_w, ph_h = w - m - px0, int(yy - y + 36)
    g = photo(pid, ph_w, ph_h, seed=3 + idx, mono=True, contrast=1.15, mid=0.30)
    gray = 0.2126 * g[..., 0] + 0.7152 * g[..., 1] + 0.0722 * g[..., 2]
    ht = halftone(gray, pitch=3.0)
    ph_im = Image.fromarray((np.clip(ht, 0, 1) * 255).astype(np.uint8)).convert("RGB")
    im.paste(ph_im, (px0, y))
    d.rectangle((px0, y, px0 + ph_w - 1, y + ph_h - 1), outline=ink, width=1)
    y2 = max(yy + 6, y + ph_h + 6)
    d.line((m, y2, w - m, y2), fill=ink, width=1)
    # body: four columns of tiny type of public-domain prose (3 mm = 6 px), each with a small bold run-in head
    ncol = 4
    gut = 8
    cw = (w - 2 * m - gut * (ncol - 1)) / ncol
    bf = fnt("evening-paper", 8, "OldStandard-Regular.ttf")
    hf2 = fnt("libre-franklin", 9)
    txt = body_text(700, seed=idx * 7 + 1)
    heads = ["NATURAL NOTES", "FROM THE PARISH", "THE WEATHER", "LOCAL NEWS", "ON THE FARMS", "THE QUAY"]
    words = txt.split()
    wi = 0
    for c in range(ncol):
        x = m + c * (cw + gut)
        yy = y2 + 6
        hd = rnd.choice(heads)
        d.text((x, yy), hd, font=hf2, fill=ink)
        yy += 13
        while yy < h - 12:
            line, n = "", 0
            while wi < len(words):
                t = (line + " " + words[wi]).strip()
                if d.textlength(t, font=bf) > cw:
                    break
                line = t
                wi += 1
            if not line:
                if wi >= len(words):
                    break
                wi += 1
                continue
            d.text((x, yy), line, font=bf, fill=(36, 36, 40))
            yy += 9.5
        if c < ncol - 1:
            d.line((x + cw + gut / 2, y2 + 4, x + cw + gut / 2, h - 8), fill=(120, 120, 124), width=1)
        TEXTS.append(hd)
    # newsprint grain and a faint ground tone
    arr = np.asarray(im).astype(np.float32)
    rng = np.random.default_rng(40 + idx)
    arr += ndimage.gaussian_filter(rng.normal(0, 5.5, (h, w)), 0.8)[..., None]
    USED["paper:%s" % name] = pid
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))


# ---------------------------------------------------------------------------------------------------------------------------------------------------------- cards
CARDS = [
    ("BIRTHDAY GREETINGS", "garden_oak", "gilt"), ("BEST WISHES", "park_gold", "red"), ("GET WELL SOON", "garden_shrubs", "gilt"), ("THANK YOU", "hills_wide", "gilt"),
    ("HAPPY ANNIVERSARY", "farmhouse_oak", "red"), ("WITH SYMPATHY", "wood_ledge", "gilt"), ("CONGRATULATIONS", "hills_ridge", "red"), ("GOOD LUCK", "jetty_hills", "gilt"),
    ("HAPPY RETIREMENT", "lakeshore", "gilt"), ("NEW HOME", "garden_lawn", "red"),
]
CARD_LINES = {"BIRTHDAY GREETINGS": "With love on your birthday", "BEST WISHES": "With all good wishes", "GET WELL SOON": "Thinking of you", "THANK YOU": "With many thanks",
              "HAPPY ANNIVERSARY": "To mark the day", "WITH SYMPATHY": "With deepest sympathy", "CONGRATULATIONS": "On your good news", "GOOD LUCK": "Every good wish",
              "HAPPY RETIREMENT": "A long and happy rest", "NEW HOME": "In your new home"}


def greeting_card(idx, size=(230, 320), seed=0):
    """A greetings card: a library photograph over the upper 72 per cent in a thin gilt or white frame, the greeting in a serif or a script in gilt (200, 160, 70) or deep red on a cream panel."""
    word, pid, ink = CARDS[idx % len(CARDS)]
    w, h = size
    rnd = random.Random(3000 + idx)
    cream = (240, 234, 218)
    im = Image.new("RGB", size, cream)
    d = ImageDraw.Draw(im)
    ph_h = int(h * 0.70)
    g = photo(pid, w - 24, ph_h - 12, seed=seed + idx, contrast=1.08)
    im.paste(pil(g), (12, 12))
    d.rectangle((12, 12, w - 13, ph_h - 1), outline=(190, 160, 90), width=2)
    col = (200, 160, 70) if ink == "gilt" else (140, 30, 36)
    f, ls = _fit(d, word, "old-standard-tt", None, w - 30, 30, 16, 2, step=2)
    y = ph_h + 8
    for ln in ls:
        tw = d.textlength(ln, font=f)
        d.text(((w - tw) / 2, y), ln, font=f, fill=col)
        y += int(f.size * 1.05)
    sf = fnt("evening-paper", 13, "OldStandard-Italic.ttf")
    line = CARD_LINES[word]
    tw = d.textlength(line, font=sf)
    d.text(((w - tw) / 2, h - 28), line, font=sf, fill=(110, 90, 70))
    TEXTS.extend([word, line])
    arr = np.asarray(im).astype(np.float32)
    arr += np.random.default_rng(60 + idx).normal(0, 2.0, (h, w, 1)).astype(np.float32)
    USED["card:%s" % word] = pid
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))


POSTCARDS = [
    ("GREETINGS FROM MERIDIAN: THE HARBOUR WALL", "lake_harbour"), ("POSTS IN THE BAY", "pier_posts"), ("MERIDIAN QUAY: THE PIER AND THE MASTS", "lake_pier"), ("MIST ON THE CAPE", "cliff_mist"),
    ("THE BEACH HUTS", "beach_huts"), ("THE BAY AT SUNRISE", "beach_sunrise"), ("SEATS ON THE HEADLAND", "headland_seats"), ("THE ISLAND IN THE BAY", "headland_island"),
    ("THE FALLS IN THE WOOD", "falls"), ("THE JETTY", "jetty"), ("BALES AT HARVEST", "hay_bales"), ("A VALLEY IN AUTUMN", "hills_valley"),
]


def postcard(idx, size=(405, 280), seed=0):
    """A postcard: the photograph full bleed inside a 3 mm white border (9 px at 3 px a mm), the caption in a small italic at the foot of the picture, in white with a shadow. The caption names what the photograph shows
    (`PHOTOS`' words: a check compares the two)."""
    cap, pid = POSTCARDS[idx % len(POSTCARDS)]
    w, h = size
    b = 9
    im = Image.new("RGB", size, (244, 242, 236))
    g = photo(pid, w - 2 * b, h - 2 * b, seed=seed + idx, contrast=1.1)
    pim = _gradient(pil(g), int((h - 2 * b) * 0.78), h - 2 * b, 0.0, 0.5)
    im.paste(pim, (b, b))
    f = fnt("evening-paper", 17, "OldStandard-Italic.ttf")
    _shadow_text(im, (b + 10, h - b - 26), cap, f, (250, 248, 240), blur=1, offset=1)
    TEXTS.append(cap)
    USED["postcard:%s" % cap] = pid
    return im


# ---------------------------------------------------------------------------------------------------------------------------------------------------------- atlases
def atlas(path, tiles, cols):
    """Tiles (PIL images of one size) in a grid atlas saved at `path`; returns {index: (u0, v0, u1, v1)} (v 0 at the bottom). Aspect is kept: the atlas is cols x rows tiles."""
    tw, th = tiles[0].size
    rows = (len(tiles) + cols - 1) // cols
    im = Image.new("RGB", (cols * tw, rows * th), (236, 232, 224))
    out = {}
    for k, t in enumerate(tiles):
        c, r = k % cols, k // cols
        im.paste(t, (c * tw, r * th))
        out[k] = ((c * tw) / (cols * tw), 1.0 - ((r + 1) * th) / (rows * th), ((c + 1) * tw) / (cols * tw), 1.0 - (r * th) / (rows * th))
    im.save(path)
    return out


def magazine_atlas(path, n=24, size=(384, 512), cols=6):
    return atlas(path, [magazine_cover(i, size) for i in range(n)], cols)


def paper_atlas(path, n=8, size=(580, 380), cols=2):
    return atlas(path, [newspaper_front(i, size) for i in range(n)], cols)


def card_atlas(path, n=10, size=(230, 320), cols=5):
    return atlas(path, [greeting_card(i, size) for i in range(n)], cols)


def postcard_atlas(path, n=12, size=(405, 280), cols=3):
    return atlas(path, [postcard(i, size) for i in range(n)], cols)


def write_used(path):
    json.dump({"used": USED, "fit": FIT, "headlines": {p_[0]: p_[1] for p_ in PAPERS}, "postcards": {c_: p_ for c_, p_ in POSTCARDS}, "subjects": {k: v[4] for k, v in PHOTOS.items()},
               "photos": {k: list(v) for k, v in PHOTOS.items() if k in set(USED.values())}}, open(path, "w"), indent=1)


# ---------------------------------------------------------------------------------------------------------------------------------------------------------- cartons (200 cigarettes), sweets, jar labels
def carton_front(idx, size=(560, 180)):
    """The front of a carton of 200 (280 x 90 mm at 2 px a mm): the maker's block (a fictional maker, sw_gen.PACK_BRANDS), 200 CIGARETTES, and the 1990 band along the foot in 2.5 mm type: MIDDLE TAR as defined
    by H.M. Government, and the Government health warning (the newsagent's close review, narrow 3: "20 CIGARETTES" and a band reading only HEALTH WARNING)."""
    brand, kind, bg, ink, accent = GEN.PACK_BRANDS[idx % len(GEN.PACK_BRANDS)]
    w, h = size
    im = Image.new("RGB", size, bg)
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, w - 1, 22), fill=accent)
    d.rectangle((0, 28, w - 1, 31), fill=ink)
    f1 = fnt("alfa-slab-one", 56)
    f1, l1 = _fit(d, brand, "alfa-slab-one", None, w - 60, 56, 24, 1, step=2)
    tw = d.textlength(l1[0], font=f1)
    d.text(((w - tw) / 2, 40), l1[0], font=f1, fill=ink)
    f2 = fnt("oswald", 28)
    tw = d.textlength(kind, font=f2)
    d.text(((w - tw) / 2, 40 + int(f1.size * 1.15)), kind, font=f2, fill=ink)
    f3 = fnt("jost", 24)
    t3 = "200 CIGARETTES"
    d.text((20, 6), t3, font=f3, fill=bg if sum(accent) < 500 else ink)
    d.text((w - 20 - d.textlength("25 x 8", font=f3), 6), "25 x 8", font=f3, fill=bg if sum(accent) < 500 else ink)
    band_y = h - 34
    d.rectangle((0, band_y, w - 1, h - 1), fill=(240, 238, 230))
    f4 = fnt("libre-franklin", 11)
    d.text((8, band_y + 3), "MIDDLE TAR  As defined by H.M. Government.", font=f4, fill=(20, 20, 24))
    d.text((8, band_y + 18), "DANGER: Government Health WARNING: CIGARETTES CAN SERIOUSLY DAMAGE YOUR HEALTH", font=f4, fill=(20, 20, 24))
    TEXTS.extend([brand, kind, t3, "MIDDLE TAR As defined by H.M. Government.", "DANGER: Government Health WARNING: CIGARETTES CAN SERIOUSLY DAMAGE YOUR HEALTH"])
    arr = np.asarray(im).astype(np.float32) + np.random.default_rng(80 + idx).normal(0, 1.8, (h, w, 1)).astype(np.float32)
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))


def carton_atlas(path, n=6, size=(560, 180), cols=2):
    return atlas(path, [carton_front(i, size) for i in range(n)], cols)


JARS = [("HUMBUGS", "stripes", (238, 236, 228), (34, 26, 26)), ("PEAR DROPS", "dots", (206, 220, 120), (150, 170, 60)), ("MINT IMPERIALS", "dots", (240, 242, 238), (210, 218, 212)),
        ("FRUIT DROPS", "mix", (204, 60, 48), (236, 190, 56)), ("TOFFEES", "dots", (150, 96, 50), (100, 60, 30)), ("SHERBET LEMONS", "dots", (240, 212, 70), (212, 176, 42)),
        ("ACID DROPS", "mix", (232, 182, 58), (186, 62, 60)), ("BARLEY SUGAR", "dots", (228, 172, 70), (194, 124, 40)), ("CHERRY LIPS", "dots", (194, 40, 52), (136, 22, 32)),
        ("LIQUORICE MIXED", "mix", (34, 30, 34), (206, 84, 94))]


def sweets_texture(idx, size=(512, 192)):
    """The contents of a sweet jar as one picture (u wraps round the jar, v up it): single sweets, each a rounded lump about 28 px across (a Voronoi cell shaded toward its middle, a highlight up and to the left, a dark
    seam where two meet), in the jar's own colours: humbugs black and white striped across each lump, the rest one colour with a few paler or darker, `mix` three colours."""
    from scipy.spatial import cKDTree
    name, kind, c1, c2 = JARS[idx % len(JARS)]
    w, h = size
    rng = np.random.default_rng(500 + idx)
    n = int(w * h / (27 * 27))
    pts = np.column_stack([rng.uniform(0, w, n), rng.uniform(0, h, n)])
    # the picture wraps in u: three copies of the points
    P = np.concatenate([pts - [w, 0], pts, pts + [w, 0]])
    tree = cKDTree(P)
    yy, xx = np.mgrid[0:h, 0:w]
    q = np.column_stack([xx.ravel() + 0.5, yy.ravel() + 0.5])
    dist, ids = tree.query(q, k=2)
    d1, d2 = dist[:, 0].reshape(h, w), dist[:, 1].reshape(h, w)
    cell = ids[:, 0].reshape(h, w) % n
    cols = [np.array(c1, np.float32), np.array(c2, np.float32)]
    if kind == "mix":
        cols = [np.array(c1, np.float32), np.array(c2, np.float32), np.array((230, 228, 220), np.float32) * 0.9]
    pick = rng.integers(0, len(cols), n)
    tint = rng.uniform(0.86, 1.08, n)
    base = (np.stack(cols)[pick] * tint[:, None])[cell]
    if kind == "stripes":
        ang = rng.uniform(0, math.pi, n)[cell]
        u = (xx * np.cos(ang) + yy * np.sin(ang)) / 5.0
        stripe = (np.floor(u) % 2).astype(np.float32)[..., None]
        base = np.array(c1, np.float32) * (1 - stripe) + np.array(c2, np.float32) * stripe
    edge = np.clip((d2 - d1) / 5.0, 0, 1)[..., None]                       # a seam where two lumps meet
    mid = np.clip(1.0 - d1 / 15.0, 0, 1)[..., None]
    shade = 0.62 + 0.38 * np.sqrt(edge) + 0.22 * mid
    cx = P[ids[:, 0]][:, 0].reshape(h, w)
    cy = P[ids[:, 0]][:, 1].reshape(h, w)
    hl = np.exp(-(((xx - (cx - 4)) ** 2 + (yy - (cy - 4)) ** 2) / 14.0))[..., None] * 0.30
    img = np.clip(base * shade + 255 * hl, 0, 255)
    return Image.fromarray(img.astype(np.uint8))


def jar_label(idx, size=(256, 128)):
    """A jar's paper label: the sweet's name over the weight and price, in a serif on cream with a thin rule; the project's own wording."""
    name, kind, c1, c2 = JARS[idx % len(JARS)]
    w, h = size
    im = Image.new("RGB", size, (240, 234, 214))
    d = ImageDraw.Draw(im)
    d.rectangle((4, 4, w - 5, h - 5), outline=(120, 40, 36), width=2)
    f, ls = _fit(d, name, "old-standard-tt", None, w - 30, 30, 14, 2, step=2)
    y = 14
    for ln in ls:
        tw = d.textlength(ln, font=f)
        d.text(((w - tw) / 2, y), ln, font=f, fill=(120, 40, 36))
        y += int(f.size * 1.05)
    f2 = fnt("evening-paper", 16, "OldStandard-Italic.ttf")
    t2 = "2 oz 25p   4 oz 48p"
    tw = d.textlength(t2, font=f2)
    d.text(((w - tw) / 2, h - 34), t2, font=f2, fill=(60, 50, 44))
    TEXTS.extend([name, t2])
    return im


def jar_atlases(content_path, label_path, n=10):
    """The sweets' pictures (one 512 x 192 strip each, stacked) and the labels (256 x 128, two columns); returns ({i: uv}, {i: uv})."""
    cont = atlas(content_path, [sweets_texture(i) for i in range(n)], 1)
    lab = atlas(label_path, [jar_label(i) for i in range(n)], 2)
    return cont, lab


# ---------------------------------------------------------------------------------------------------------------------------------------------------------- the tea rooms' cork and notices
def cork_png(path, size=512, seed=6):
    """A granular cork (the tea rooms' close review, narrow 7: "a flat orange slab"): granules of a few pixels (2 mm at 0.3 m to the 512 px), two tones, (176, 132, 88) and (150, 108, 70), each granule a rounded lump with
    a dark seam, specks of lighter and darker; the map is a plain tile."""
    from scipy.spatial import cKDTree
    rng = np.random.default_rng(seed)
    n = size
    m = int(n * n / 14.0)
    pts = np.column_stack([rng.uniform(0, n, m), rng.uniform(0, n, m)])
    P = np.concatenate([pts + [dx, dy] for dx in (-n, 0, n) for dy in (-n, 0, n)])
    tree = cKDTree(P)
    yy, xx = np.mgrid[0:n, 0:n]
    dist, ids = tree.query(np.column_stack([xx.ravel() + 0.5, yy.ravel() + 0.5]), k=2)
    d1, d2 = dist[:, 0].reshape(n, n), dist[:, 1].reshape(n, n)
    cell = ids[:, 0].reshape(n, n) % m
    mix = rng.uniform(0, 1, m)
    a, b = np.array((176, 132, 88), np.float32), np.array((150, 108, 70), np.float32)
    base = (a[None, :] * mix[:, None] + b[None, :] * (1 - mix[:, None]))[cell]
    shade = 0.70 + 0.30 * np.sqrt(np.clip((d2 - d1) / 3.0, 0, 1))[..., None] + 0.08 * np.clip(1.0 - d1 / 5.0, 0, 1)[..., None]
    arr = base * shade + rng.normal(0, 3.0, (n, n, 1))
    Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).save(path)
    return path


NOTICES = [("TABLES\nBOOKED", "Please ask at the counter", (240, 236, 222)), ("TEAS FROM\n25p", "All day, every day", (226, 236, 240)), ("OPEN\n6.30 - 10", "Six days; Sundays 8 - 12", (244, 238, 206)),
           ("CAKES\nMADE HERE", "Fresh each morning", (240, 226, 224)), ("THANK\nYOU", "For calling in", (232, 238, 226)), ("LUNCH\n12 - 2", "Soup, rolls and cakes", (240, 236, 222))]


def notice_sheet(idx, size=(256, 160), seed=0):
    """A notice for a cork board: a coloured sheet of paper with grain, the heading hand-lettered (a letter at a time, a degree or two out), a line of small print under it; the project's own wording."""
    head, small, ground = NOTICES[idx % len(NOTICES)]
    w, h = size
    rnd = random.Random(900 + idx)
    im = Image.new("RGB", size, ground)
    d = ImageDraw.Draw(im)
    f = fnt("patrick-hand", 40)
    lines = head.split("\n")
    y = 14
    for ln in lines:
        adv = [d.textlength(ch, font=f) for ch in ln]
        x = (w - sum(adv)) / 2.0
        for ch, a_ in zip(ln, adv):
            if ch != " ":
                tile = Image.new("L", (int(a_ + 20), 70), 0)
                ImageDraw.Draw(tile).text((10, 6), ch, font=f, fill=255)
                tile = tile.rotate(rnd.uniform(-3, 3), resample=Image.BICUBIC, center=(10 + a_ / 2, 40))
                im.paste(Image.new("RGB", tile.size, (30, 30, 56)), (int(x - 10), int(y + rnd.uniform(-2, 2))), tile)
            x += a_
        y += 44
    f2 = fnt("evening-paper", 14, "OldStandard-Italic.ttf")
    tw = d.textlength(small, font=f2)
    d.text(((w - tw) / 2, h - 26), small, font=f2, fill=(60, 56, 70))
    d.rectangle((3, 3, w - 4, h - 4), outline=tuple(int(c * 0.82) for c in ground), width=1)
    TEXTS.extend([head.replace("\n", " "), small])
    arr = np.asarray(im).astype(np.float32) + np.random.default_rng(70 + idx).normal(0, 2.2, (h, w, 1)).astype(np.float32)
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))


def notice_atlas(path, n=6, size=(256, 160), cols=3):
    return atlas(path, [notice_sheet(i, size) for i in range(n)], cols)


def menu_card_png(path, text="TEAS FROM 25p", size=(300, 100)):
    """The small card under the chalk menu (the tea rooms' close review, narrow 6): paper (235, 232, 222), ink (25, 25, 50), one line of at most 14 characters, big."""
    w, h = size
    im = Image.new("RGB", size, (235, 232, 222))
    d = ImageDraw.Draw(im)
    f, ls = _fit(d, text, "oswald", None, w - 24, 60, 18, 1, step=2)
    tw = d.textlength(ls[0], font=f)
    d.text(((w - tw) / 2, (h - f.size * 1.2) / 2), ls[0], font=f, fill=(25, 25, 50))
    arr = np.asarray(im).astype(np.float32) + np.random.default_rng(81).normal(0, 2.0, (h, w, 1)).astype(np.float32)
    Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).save(path)
    TEXTS.append(text)
    return path
