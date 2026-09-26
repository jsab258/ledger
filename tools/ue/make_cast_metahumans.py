"""Make the slice's cast as MetaHumans, by script, in the full editor.

    set LEDGER_MH_STEP=prepare   (or build)
    UnrealEditor.exe C:/LedgerTools/mh-assemble/MHAssemble.uproject
        with Content/Python/init_unreal.py calling main_after_idle()
    python tools/ue/make_cast_metahumans.py --selftest     # runs without Unreal

WHY, 24 September. Jafar: "MetaHumans replace the Mixamo stand-ins for the
slice's cast, starting with Rocco, Lena and Sam, in plain clothes for now."
Each starts from the nearest of the 29 people the MetaHuman plugin ships,
chosen from their preview pictures against the cards: Rocco, twenty years on
the door, big and slow, from Jorge; Lena, thirty-one years on the books, from
Grace; Sam, the fast talker who walks the street, from Orlando. A choice of
look, not canon, and his to overrule.

TWO STEPS, TWO EDITOR RUNS, because the preview holds several GB and a build
beside it runs out of memory (assemble_metahuman.py's own finding):

  prepare  duplicate the preset into /Game/Cast/MH_<name>, open it for edit,
           put it in the plugin's one plain garment, ask Epic's service to
           rig it and to send its textures, and wait until it can be built;
           one character at a time, never re-entered.
  build    build each with the Optimized pipeline at High into
           /Game/Ledger/MetaHumans, where the probe's build step copies from.

THE FILES STAY OUT OF THE REPOSITORY: they are made in the scratch project
outside it, and backed up to Dropbox (DECISIONS, 24 September).

ONE LINE PER CHARACTER PER STEP, appended to ue-material.txt in the project
folder: who, from which preset, what happened, how long.
"""
import os
import sys
import time

CAST = [("rocco", "Jorge"), ("lena", "Grace"), ("sam", "Orlando")]
PRESET_DIR = "/MetaHumanCharacter/Optional/Presets/"
CAST_DIR = "/Game/Cast/"
BUILD_ROOT = "/Game/Ledger/MetaHumans"
GARMENT = "/MetaHumanCharacter/Optional/Clothing/WI_DefaultGarment.WI_DefaultGarment"
# EPIC'S FREE CLOTHES ON FAB (sweater, jeans, boots, flats, sneakers...) come
# as .mhpkg files, downloadable only when Jafar is signed in to fab.com. The
# MetaHuman SDK registers a factory for .mhpkg (MetaHumanPackageFactory), so
# an unreal.AssetImportTask on the file should bring each in by script; its
# wardrobe item then takes GARMENT's place above (24 September, untried).
# WHAT EACH WEARS, plain and of the period, from Epic's free Fab items (their
# .mhpkg file names, as the listings give them for the jeans: oa_jeans.mhpkg;
# the rest are guesses until downloaded). Dropped in FAB_DOWNLOADS, imported
# by import_fab_packages(), then put on in place of GARMENT.
FAB_DOWNLOADS = os.path.join(os.path.expanduser("~"), "Downloads")
FAB_IMPORT_DIR = "/Game/Fab/"
OUTFITS = {
    "lena": ("sweater", "jeans", "flats"),
    "rocco": ("sweater", "jeans", "boots"),
    "sam": ("tshirt", "slimjeans", "sneakers"),
}
# THE WARDROBE ITEMS THE PACKAGES MAKE, as imported on 24 September (overnight)
# by import_fab_clothes.py: each package lands under /Game/Fab/<file name>.
FAB_ITEMS = {
    "sweater": "/Game/Fab/oa_sweater/WI_OA_Sweater",
    "jeans": "/Game/Fab/oa_jeans/WI_OA_Jeans",
    "slimjeans": "/Game/Fab/oa_slimjeansvariants/WI_OA_Jeans_slm",
    "tshirt": "/Game/Fab/oa_tshirtvariants/WI_OA_TshirtLngSlv",
    "boots": "/Game/Fab/oa_boots/WI_OA_Boots",
    "flats": "/Game/Fab/oa_flats/WI_OA_Flats",
    "sneakers": "/Game/Fab/oa_casualsneakers/WI_OA_CasualSneakers",
}


# PLAIN 1990 COLOURS, not Epic's grey with electric-blue trim (24 September,
# overnight). Linear colour per garment's two diffuse colours, from the
# casting sheets: Sheila's beige cardigan and brown shoes, Ron's navy jumper
# and black boots, Darren's off-white shirt and grubby white trainers. Set on
# the built clothing materials after the build, like the hair (the wardrobe's
# own parameter lookup is not open to scripts). Keys are the garment's stem in
# the built material's name, MI_WI_OA_<stem>_...
CLOTH_COLOURS = {
    "lena": {"Sweater": {"diffuse_color_1": (0.42, 0.34, 0.24), "diffuse_color_2": (0.36, 0.29, 0.20)},
             "Flats": {"diffuse_color_1": (0.09, 0.045, 0.02), "diffuse_color_2": (0.09, 0.045, 0.02)}},
    "rocco": {"Sweater": {"diffuse_color_1": (0.018, 0.022, 0.038), "diffuse_color_2": (0.015, 0.018, 0.03)},
              "Boots": {"diffuse_color_1": (0.012, 0.011, 0.010), "diffuse_color_2": (0.012, 0.011, 0.010)}},
    "sam": {"TshirtLngSlv": {"diffuse_color_1": (0.62, 0.60, 0.56), "diffuse_color_2": (0.62, 0.60, 0.56)},
            "CasualSneakers": {"diffuse_color_1": (0.55, 0.54, 0.51), "diffuse_color_2": (0.50, 0.49, 0.47)}},
}


def cloth_materials(who, paths):
    """(path, garment stem) for each built clothing material of one of the cast that CLOTH_COLOURS recolours."""
    out = []
    for p in paths:
        name = p.split("/")[-1].split(".")[0]
        if "/Clothing/" not in p or not name.startswith("MI_WI_OA_"):
            continue
        for stem in CLOTH_COLOURS.get(who, {}):
            if name.startswith("MI_WI_OA_" + stem + "_"):
                out.append((p, stem))
    return out


def recolour_cloth(who, made):
    """Sets CLOTH_COLOURS on the built clothing materials; how many."""
    import unreal
    n = 0
    for path, stem in cloth_materials(who, made):
        mi = unreal.load_asset(path)
        if not isinstance(mi, unreal.MaterialInstanceConstant):
            continue
        for pname, (r, g, b) in CLOTH_COLOURS[who][stem].items():
            unreal.MaterialEditingLibrary.set_material_instance_vector_parameter_value(mi, pname, unreal.LinearColor(r, g, b, 1.0))
        n += 1
    return n


def outfit_paths(who):
    """The wardrobe items one of the cast is dressed in, as loadable object paths."""
    return ["%s.%s" % (FAB_ITEMS[w], FAB_ITEMS[w].split("/")[-1]) for w in OUTFITS.get(who, ())]


def fab_packages(names):
    """The MetaHuman package files among these file names."""
    return [n for n in names if n.lower().endswith(".mhpkg")]


def import_fab_packages():
    """Imports every .mhpkg in FAB_DOWNLOADS under FAB_IMPORT_DIR; the paths it made."""
    import unreal
    files = fab_packages(os.listdir(FAB_DOWNLOADS)) if os.path.isdir(FAB_DOWNLOADS) else []
    tasks = []
    for f in files:
        t = unreal.AssetImportTask()
        t.set_editor_property("filename", os.path.join(FAB_DOWNLOADS, f))
        t.set_editor_property("destination_path", FAB_IMPORT_DIR + os.path.splitext(f)[0])
        t.set_editor_property("automated", True)
        t.set_editor_property("save", True)
        tasks.append(t)
    if tasks:
        unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)
    return [p for t in tasks for p in (t.get_editor_property("imported_object_paths") or [])]
NEED_FREE_GB = 10.0
CLOUD_TIMEOUT_S = 15 * 60


BARE = os.environ.get("LEDGER_MH_BARE", "") == "1"
# A SECOND TAKE BESIDE THE FIRST (24 September): LEDGER_MH_TAKE=T2 makes
# MH_LenaT2 and so on, cast to the brief below, and leaves the stand-ins be.
TAKE = os.environ.get("LEDGER_MH_TAKE", "")


def asset_name(who, bare=False, take=None):
    return "MH_" + who.capitalize() + ("Bare" if bare else "") + (TAKE if take is None else take)


# CAST TO A BRIEF, 24 September. Jafar: "Why is Lena a middle aged chinese
# woman? Need a proper casting for faces and bodies." Canon says only "Rocco
# (old muscle), Lena (older bookkeeper)"; the voice cards make Sam a fast-
# talking Scot. The brief (his to strike, FOR-JAFAR 24 September): Lena
# British, about sixty, small and neat; Rocco British with an Italian name,
# late fifties, big and heavy; Sam Scottish, late twenties, wiry. Each is
# the base preset (its eyes, brows, wardrobe) with its face shape a weighted
# mix of shipped faces, its skin tone and skin texture set (the texture
# carries age: 121 is the aged set Walter and Grace share), its body held to
# measurements, and a haircut from the plugin's grooms. Skin U runs light
# (0.2, Vivian) to dark (0.95, Zuri); measurements are centimetres, and Fat,
# Muscularity and Masculine/Feminine the creator's own sliders.
GROOMS = "/MetaHumanCharacter/Optional/Grooms/Bindings/Hair/"
CASTING = {
    "lena": {"base": "Vivian", "face": {"Vivian": 0.55, "Celeste": 0.25, "Walter": 0.2},
             "skin": {"u": 0.24, "v": 0.45, "face_texture_index": 121},
             "body": {"Height": 160.0, "Fat": 0.6, "Muscularity": -0.8},
             "hair": "WI_Hair_M_BobCurly", "hair_colour": {"hairMelanin": 0.4, "hairRedness": 0.05, "WhiteAmount": 0.45,
                                                               "MelaninVariationFine": 0.3, "MelaninVariationRough": 0.2},
             "no_makeup": True},
    "rocco": {"base": "Jorge", "face": {"Jorge": 0.35, "Walter": 0.35, "Bruce": 0.3},
              "skin": {"u": 0.34, "v": 0.5, "face_texture_index": 121},
              "body": {"Height": 186.0, "Fat": 1.3, "Muscularity": 0.6},
              "hair": "WI_Hair_S_HairLoss", "hair_colour": {"WhiteAmount": 0.45}},
    "sam": {"base": "Orlando", "face": {"Orlando": 0.45, "Victor": 0.55},
            "skin": {"u": 0.2, "v": 0.45, "face_texture_index": 28},
            "body": {"Height": 173.0, "Fat": -1.0, "Muscularity": -0.3},
            "hair": "WI_Hair_S_Messy"},
}


# CANDIDATES, 25 September. Jafar's ruling: faces are cast in MetaHuman
# first; several candidates per character from the casting sheet, shown front,
# profile and speaking in the game's light, and the one he approves becomes
# the concept. Five each, as takes C1 to C5 (MH_LenaC1 ...), every one a
# different blend of the plugin's light-skinned people within the sheet: age
# carried by the skin texture (121 is the aged set Walter and Grace share),
# height and build held to the sheet, a haircut, and facial hair for Ron (his
# moustache) and Darren (stubble). Grace's face is left out: Lena taken from
# her read as East Asian (24 September).
FACIAL = "/MetaHumanCharacter/Optional/Grooms/Bindings/"


def _c(base, face, tex, u, v, height, fat, musc, hair, colour=None, beard=None, mustache=None, makeup=False):
    b = {"base": base, "face": face, "skin": {"u": u, "v": v} if tex is None else {"u": u, "v": v, "face_texture_index": tex},
         "body": {"Height": height, "Fat": fat, "Muscularity": musc}, "hair": hair}
    if colour:
        b["hair_colour"] = colour
    if beard:
        b["beard"] = beard
    if mustache:
        b["mustache"] = mustache
    if not makeup:
        b["no_makeup"] = True
    return b


GREY_BROWN = {"hairMelanin": 0.45, "hairRedness": 0.05, "WhiteAmount": 0.4}
GREY = {"hairMelanin": 0.4, "WhiteAmount": 0.55}
CANDIDATES = {
    "C1": {"lena": _c("Vivian", {"Vivian": 0.5, "Walter": 0.25, "Celeste": 0.25}, 121, 0.22, 0.45, 160.0, 0.6, -0.8, "WI_Hair_M_BobCurly", GREY_BROWN),
           "rocco": _c("Walter", {"Walter": 0.45, "Bruce": 0.35, "Victor": 0.2}, 121, 0.36, 0.6, 186.0, 1.3, 0.6, "WI_Hair_S_HairLoss", GREY, mustache="WI_Mustache_L_Full"),
           "sam": _c("Orlando", {"Orlando": 0.45, "Victor": 0.55}, 28, 0.2, 0.45, 175.0, -1.0, -0.3, "WI_Hair_S_Messy", beard="WI_Beard_S_Stubble")},
    "C2": {"lena": _c("Jelena", {"Jelena": 0.5, "Walter": 0.3, "Vivian": 0.2}, 121, 0.21, 0.5, 160.0, 0.4, -0.8, "WI_Hair_S_BobLayered", GREY_BROWN),
           "rocco": _c("Bruce", {"Bruce": 0.5, "Walter": 0.3, "Kelvin": 0.2}, 13, 0.38, 0.7, 186.0, 1.1, 0.8, "WI_Hair_S_BaldingStubble", GREY, mustache="WI_Mustache_S_Full"),
           "sam": _c("Victor", {"Victor": 0.5, "Kelvin": 0.3, "Orlando": 0.2}, 28, 0.22, 0.4, 175.0, -1.0, -0.5, "WI_Hair_M_SideSweptFringe", beard="WI_Beard_S_Stubble")},
    "C3": {"lena": _c("Celeste", {"Celeste": 0.45, "Vivian": 0.3, "Walter": 0.25}, 58, 0.25, 0.5, 161.0, 0.8, -0.8, "WI_Hair_S_SweptUp", GREY_BROWN),
           "rocco": _c("Walter", {"Walter": 0.5, "Lorenzo": 0.3, "Bruce": 0.2}, 121, 0.4, 0.55, 185.0, 1.4, 0.4, "WI_Hair_S_RecedeMessy", GREY, mustache="WI_Mustache_L_Messy"),
           "sam": _c("Kelvin", {"Kelvin": 0.5, "Victor": 0.3, "Lorenzo": 0.2}, 27, 0.24, 0.35, 174.0, -0.9, -0.4, "WI_Hair_S_Casual", beard="WI_Beard_S_Stubble")},   # BobMessy ran the card out of video memory at build
    "C4": {"lena": _c("Vivian", {"Vivian": 0.35, "Jelena": 0.35, "Walter": 0.3}, 121, 0.2, 0.42, 158.0, 0.2, -0.8, "WI_Hair_M_Layered", GREY_BROWN),
           "rocco": _c("Bruce", {"Bruce": 0.4, "Walter": 0.4, "Victor": 0.2}, 121, 0.34, 0.65, 188.0, 1.5, 0.5, "WI_Hair_S_HairLoss", GREY, mustache="WI_Mustache_S_Full"),
           "sam": _c("Orlando", {"Orlando": 0.4, "Kelvin": 0.3, "Lorenzo": 0.3}, 85, 0.26, 0.42, 176.0, -1.0, -0.6, "WI_Hair_L_MessyClumps", beard="WI_Beard_S_Stubble")},
    "C5": {"lena": _c("Jelena", {"Jelena": 0.4, "Celeste": 0.3, "Walter": 0.3}, 17, 0.24, 0.48, 162.0, 0.6, -0.7, "WI_Hair_S_Pixie", GREY_BROWN),
           "rocco": _c("Kelvin", {"Kelvin": 0.35, "Walter": 0.4, "Bruce": 0.25}, 137, 0.42, 0.6, 186.0, 1.2, 0.7, "WI_Hair_S_BaldingStubble", GREY, mustache="WI_Mustache_L_Full"),
           "sam": _c("Victor", {"Victor": 0.4, "Lorenzo": 0.35, "Orlando": 0.25}, 151, 0.23, 0.45, 175.0, -0.8, -0.4, "WI_Hair_S_CurlyFade")},
    # WHY THEY READ EAST ASIAN, 25 September (evening; Jafar: "they all look
    # kinda Asian"). The faces are blends of European presets, but each had
    # its skin set swapped by number, and a skin set carries the scanned
    # person's eyelids, nose and cheeks as well as colour. Two tests on
    # Sheila's approved face (C1): E1 keeps her base preset's own skin set,
    # E2 the aged set 121 she was built with.
    "E1": {"lena": _c("Vivian", {"Vivian": 0.5, "Walter": 0.25, "Celeste": 0.25}, None, 0.22, 0.45, 160.0, 0.6, -0.8, "WI_Hair_M_BobCurly", GREY_BROWN)},
    "E2": {"lena": _c("Vivian", {"Vivian": 1.0}, 121, 0.22, 0.45, 160.0, 0.6, -0.8, "WI_Hair_M_BobCurly", GREY_BROWN)},
    # E3, the control: Vivian as Epic ships her, own face and own skin.
    "E3": {"lena": _c("Vivian", {"Vivian": 1.0}, None, 0.22, 0.45, 160.0, 0.6, -0.8, "WI_Hair_M_BobCurly", GREY_BROWN)},
    # E4, Vivian wholly as Epic ships her: her own hair and make-up too (E3 still
    # had Sheila's haircut and no make-up), to compare with Epic's own picture.
    "E4": {"lena": _c("Vivian", {"Vivian": 1.0}, None, 0.22, 0.45, 160.0, 0.6, -0.8, None, makeup=True)},
    # F1, THE FIX (25 September, night): E4, Vivian wholly as shipped, looked
    # like Epic's own picture of her, so the build is sound; what read East
    # Asian was the dark straight bob with a heavy side fringe on Sheila (with
    # all make-up gone, under the street's dim light). Her approved face, C1,
    # with the sheet's hair: short and off the face like a set, a lighter
    # greying brown.
    "F1": {"lena": _c("Vivian", {"Vivian": 0.5, "Walter": 0.25, "Celeste": 0.25}, 121, 0.22, 0.45, 160.0, 0.6, -0.8, "WI_Hair_S_SweptUp",
                      {"hairMelanin": 0.3, "hairRedness": 0.08, "WhiteAmount": 0.5})},
}


# THE NEW CANDIDATES, 26 September (Jafar: rebuild the three "from northern
# European presets, following their casting sheets, with hair, eye colour and
# make-up to match"). What made the last ones read East Asian: even blends of
# several faces (they average toward the model's middle face: a flat mid-face,
# low nose bridge), a dark fringed bob, all make-up removed, brown eyes. So each
# face is one European preset, or one leading at least 80%; eyes at the chart
# places Epic's own European presets use (tools/ue/preset_facts.py: Walter's
# grey-blue, Orlando's blue); the base preset's own beard or moustache taken
# off unless the sheet has one; Sheila in the light make-up of a woman of 53 in
# 1990 (a thin liner, natural lips, a touch of blush), the men in none.
GREY_BLUE = {"pattern": "IRIS008", "u": 0.34, "v": 0.79}      # Walter's
BLUE = {"pattern": "IRIS008", "u": 0.45, "v": 0.6}            # Orlando's
GREYING_SET = {"hairMelanin": 0.3, "hairRedness": 0.1, "WhiteAmount": 0.45}
GREY_SIDES = {"hairMelanin": 0.4, "hairRedness": 0.05, "WhiteAmount": 0.55}
LIGHT_BROWN = {"hairMelanin": 0.25, "hairRedness": 0.15, "WhiteAmount": 0.0}
SHEILA_MAKEUP = {"eyes": {"type": "THIN_LINER", "opacity": 0.25, "primary_color": (0.12, 0.09, 0.07)},
                 "lips": {"type": "NATURAL", "opacity": 0.3, "color": (0.45, 0.2, 0.2)},
                 "blush": {"type": "LOW_SWEEP", "intensity": 0.12, "color": (0.6, 0.3, 0.3)}}


def _n(base, face, tex, u, v, height, fat, musc, hair, colour, eyes, clear=(), beard=None, mustache=None, makeup=None):
    b = _c(base, face, tex, u, v, height, fat, musc, hair, colour, beard=beard, mustache=mustache, makeup=bool(makeup))
    b["eyes"] = eyes
    b["clear"] = list(clear)
    if makeup:
        b["makeup"] = makeup
    return b


NEW = {
    "N1": {"lena": _n("Vivian", {"Vivian": 1.0}, 121, 0.2, 0.45, 160.0, 0.6, -0.8, "WI_Hair_M_BobCurly", GREYING_SET, GREY_BLUE, makeup=SHEILA_MAKEUP),
           "rocco": _n("Walter", {"Walter": 1.0}, 121, 0.3, 0.75, 186.0, 1.3, 0.6, "WI_Hair_S_HairLoss", GREY_SIDES, GREY_BLUE, ("Beard",), mustache="WI_Mustache_L_Full"),
           "sam": _n("Orlando", {"Orlando": 1.0}, None, 0.18, 0.45, 175.0, -1.0, -0.3, "WI_Hair_M_BobCurly", LIGHT_BROWN, BLUE, ("Mustache",), beard="WI_Beard_S_Stubble")},
    "N2": {"lena": _n("Jelena", {"Jelena": 1.0}, 121, 0.2, 0.45, 160.0, 0.6, -0.8, "WI_Hair_M_BobCurly", GREYING_SET, GREY_BLUE, makeup=SHEILA_MAKEUP),
           "rocco": _n("Bruce", {"Bruce": 1.0}, 121, 0.3, 0.75, 186.0, 1.3, 0.6, "WI_Hair_S_HairLoss", GREY_SIDES, GREY_BLUE, ("Beard",), mustache="WI_Mustache_S_Full"),
           "sam": _n("Victor", {"Victor": 1.0}, None, 0.18, 0.45, 175.0, -1.0, -0.3, "WI_Hair_L_MessyClumps", LIGHT_BROWN, BLUE, ("Mustache",), beard="WI_Beard_S_Stubble")},
    "N3": {"lena": _n("Celeste", {"Celeste": 1.0}, 121, 0.2, 0.45, 160.0, 0.6, -0.8, "WI_Hair_S_Updo", GREYING_SET, GREY_BLUE, makeup=SHEILA_MAKEUP),
           "rocco": _n("Walter", {"Walter": 0.8, "Bruce": 0.2}, 121, 0.3, 0.75, 186.0, 1.3, 0.6, "WI_Hair_S_BaldingStubble", GREY_SIDES, GREY_BLUE, ("Beard",), mustache="WI_Mustache_L_Full"),
           "sam": _n("Orlando", {"Orlando": 0.8, "Victor": 0.2}, None, 0.18, 0.45, 175.0, -1.0, -0.3, "WI_Hair_M_BobCurly", LIGHT_BROWN, BLUE, ("Mustache",), beard="WI_Beard_S_Stubble")},
    "N4": {"lena": _n("Jelena", {"Jelena": 0.8, "Vivian": 0.2}, 99, 0.2, 0.45, 160.0, 0.6, -0.8, "WI_Hair_M_BobCurly", GREYING_SET, GREY_BLUE, makeup=SHEILA_MAKEUP),
           "rocco": _n("Bruce", {"Bruce": 0.8, "Walter": 0.2}, 13, 0.3, 0.75, 186.0, 1.3, 0.6, "WI_Hair_S_HairLoss", GREY_SIDES, GREY_BLUE, ("Beard",), mustache="WI_Mustache_L_Full"),
           "sam": _n("Victor", {"Victor": 0.8, "Orlando": 0.2}, None, 0.18, 0.45, 175.0, -1.0, -0.3, "WI_Hair_M_Layered", LIGHT_BROWN, BLUE, ("Mustache",), beard="WI_Beard_S_Stubble")},
    "N5": {"lena": _n("Vivian", {"Vivian": 0.8, "Celeste": 0.2}, 58, 0.2, 0.45, 160.0, 0.6, -0.8, "WI_Hair_S_Updo", GREYING_SET, GREY_BLUE, makeup=SHEILA_MAKEUP),
           "rocco": _n("Walter", {"Walter": 0.85, "Victor": 0.15}, 121, 0.3, 0.75, 186.0, 1.3, 0.6, "WI_Hair_S_BaldingStubble", GREY_SIDES, GREY_BLUE, ("Beard",), mustache="WI_Mustache_S_Full"),
           "sam": _n("Orlando", {"Orlando": 0.85, "Bruce": 0.15}, None, 0.18, 0.45, 175.0, -1.0, -0.3, "WI_Hair_S_Messy", LIGHT_BROWN, BLUE, ("Mustache",), beard="WI_Beard_S_Stubble")},
}
CANDIDATES.update(NEW)

# THE SECOND ATTEMPT, 26 September, from the N1 portraits against the sheets.
# Sheila's M_BobCurly is a shoulder-length fringe over one eye, not "a short
# shampoo-and-set perm"; her make-up is "none but a plain lipstick". Ron's skin
# read olive, not "weathered and ruddy", and his fringe and moustache too dark
# for "grey". Darren's cut was long and straight, not "a grown-out perm with
# bleached tips": the hair material's ombre lightens the ends. The hair colour
# itself was right in the game (ue-probe LedgerHair.h logged it); the street's
# shade darkens it.
SET_GREYING = {"hairMelanin": 0.4, "hairRedness": 0.1, "WhiteAmount": 0.45}
GREY_FRINGE = {"hairMelanin": 0.35, "hairRedness": 0.05, "WhiteAmount": 0.7}
BLEACHED_TIPS = {"hairMelanin": 0.3, "hairRedness": 0.15, "WhiteAmount": 0.0,
                 "Ombre": 1.0, "OmbreMelanin": 0.05, "OmbreRedness": 0.1, "OmbreShift": 0.55, "OmbreContrast": 0.5, "OmbreIntensity": 1.0}
PLAIN_LIPSTICK = {"lips": {"type": "NATURAL", "opacity": 0.5, "color": (0.55, 0.14, 0.14)}}
SECOND = {
    "P1": {"lena": _n("Vivian", {"Vivian": 1.0}, 121, 0.2, 0.45, 160.0, 0.6, -0.8, "WI_Hair_S_BobLayered", SET_GREYING, GREY_BLUE, makeup=PLAIN_LIPSTICK),
           "rocco": _n("Walter", {"Walter": 1.0}, 121, 0.22, 0.7, 186.0, 1.3, 0.6, "WI_Hair_S_HairLoss", GREY_FRINGE, GREY_BLUE, ("Beard",), mustache="WI_Mustache_L_Full"),
           "sam": _n("Orlando", {"Orlando": 1.0}, None, 0.18, 0.45, 175.0, -1.0, -0.3, "WI_Hair_M_BobMessy", BLEACHED_TIPS, BLUE, ("Mustache",), beard="WI_Beard_S_Stubble")},
    "P2": {"lena": _n("Jelena", {"Jelena": 1.0}, 121, 0.2, 0.45, 160.0, 0.6, -0.8, "WI_Hair_S_BobLayered", SET_GREYING, GREY_BLUE, makeup=PLAIN_LIPSTICK),
           "rocco": _n("Bruce", {"Bruce": 1.0}, 121, 0.22, 0.7, 186.0, 1.3, 0.6, "WI_Hair_S_HairLoss", GREY_FRINGE, GREY_BLUE, ("Beard",), mustache="WI_Mustache_L_Full"),
           "sam": _n("Victor", {"Victor": 1.0}, None, 0.18, 0.45, 175.0, -1.0, -0.3, "WI_Hair_S_Messy", BLEACHED_TIPS, BLUE, ("Mustache",), beard="WI_Beard_S_Stubble")},
    "P3": {"lena": _n("Celeste", {"Celeste": 1.0}, 121, 0.2, 0.45, 160.0, 0.6, -0.8, "WI_Hair_S_BobLayered", SET_GREYING, GREY_BLUE, makeup=PLAIN_LIPSTICK),
           "rocco": _n("Walter", {"Walter": 0.8, "Bruce": 0.2}, 121, 0.22, 0.7, 186.0, 1.3, 0.6, "WI_Hair_S_BaldingStubble", GREY_FRINGE, GREY_BLUE, ("Beard",), mustache="WI_Mustache_L_Full"),
           "sam": _n("Orlando", {"Orlando": 0.8, "Victor": 0.2}, None, 0.18, 0.45, 175.0, -1.0, -0.3, "WI_Hair_M_BobMessy", BLEACHED_TIPS, BLUE, ("Mustache",), beard="WI_Beard_S_Stubble")},
    "P4": {"lena": _n("Jelena", {"Jelena": 0.8, "Vivian": 0.2}, 99, 0.2, 0.45, 160.0, 0.6, -0.8, "WI_Hair_S_SweptUp", SET_GREYING, GREY_BLUE, makeup=PLAIN_LIPSTICK),
           "rocco": _n("Bruce", {"Bruce": 0.8, "Walter": 0.2}, 13, 0.22, 0.7, 186.0, 1.3, 0.6, "WI_Hair_S_HairLoss", GREY_FRINGE, GREY_BLUE, ("Beard",), mustache="WI_Mustache_L_Full"),
           "sam": _n("Victor", {"Victor": 0.8, "Orlando": 0.2}, None, 0.18, 0.45, 175.0, -1.0, -0.3, "WI_Hair_M_Layered", BLEACHED_TIPS, BLUE, ("Mustache",), beard="WI_Beard_S_Stubble")},
    "P5": {"lena": _n("Vivian", {"Vivian": 0.8, "Celeste": 0.2}, 58, 0.2, 0.45, 160.0, 0.6, -0.8, "WI_Hair_S_SweptUp", SET_GREYING, GREY_BLUE, makeup=PLAIN_LIPSTICK),
           "rocco": _n("Walter", {"Walter": 0.85, "Victor": 0.15}, 121, 0.22, 0.7, 186.0, 1.3, 0.6, "WI_Hair_S_BaldingStubble", GREY_FRINGE, GREY_BLUE, ("Beard",), mustache="WI_Mustache_S_Full"),
           "sam": _n("Orlando", {"Orlando": 0.85, "Bruce": 0.15}, None, 0.18, 0.45, 175.0, -1.0, -0.3, "WI_Hair_S_Messy", BLEACHED_TIPS, BLUE, ("Mustache",), beard="WI_Beard_S_Stubble")},
}
CANDIDATES.update(SECOND)


def brief(who):
    """The brief the current take builds `who` to: a candidate's, the cast's, or none (a stand-in)."""
    if TAKE in CANDIDATES:
        return CANDIDATES[TAKE].get(who)
    return CASTING.get(who) if TAKE else None


def use_take(take):
    global TAKE
    TAKE = take


def hair_materials(who, paths):
    """The built haircut's (and moustache's) own material instances among a take's asset paths."""
    c = brief(who) if TAKE else CASTING.get(who)
    if not c or not c.get("hair_colour"):
        return []
    stems = [c[k][len("WI_"):] for k in ("hair", "mustache", "beard") if c.get(k)]
    out = []
    for path in paths:
        name = path.split("/")[-1].split(".")[0]
        if "/Grooms/" in path and name.startswith("MI_") and any(s in name for s in stems):
            out.append(path)
    return out


def recolour_hair(who, made):
    """Sets the brief's hair colour on the built haircut's materials; how many."""
    import unreal
    n = 0
    for path in hair_materials(who, made) if TAKE else []:
        mi = unreal.load_asset(path)
        if not isinstance(mi, unreal.MaterialInstanceConstant):
            continue
        for pname, value in brief(who)["hair_colour"].items():
            unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(mi, pname, value)
        n += 1
    return n


def blend(vectors_and_weights):
    """The weighted mean of equal-length coefficient lists."""
    total = sum(w for _, w in vectors_and_weights)
    n = len(vectors_and_weights[0][0])
    out = [0.0] * n
    for vec, w in vectors_and_weights:
        for i in range(n):
            out[i] += float(vec[i]) * w / total
    return out


def status_line(step, who, preset, status, seconds, note):
    return ("castMetahuman step=%s who=%s preset=%s status=%s seconds=%.0f note=%s"
            % (step, who, preset, status, seconds, (note or "none").replace(" ", "~")[:220]))


def free_gb():
    try:
        import ctypes

        class MEMORYSTATUSEX(ctypes.Structure):
            _fields_ = [("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong),
                        ("ullTotalPhys", ctypes.c_ulonglong), ("ullAvailPhys", ctypes.c_ulonglong),
                        ("ullTotalPageFile", ctypes.c_ulonglong), ("ullAvailPageFile", ctypes.c_ulonglong),
                        ("ullTotalVirtual", ctypes.c_ulonglong), ("ullAvailVirtual", ctypes.c_ulonglong),
                        ("ullAvailExtendedVirtual", ctypes.c_ulonglong)]
        m = MEMORYSTATUSEX()
        m.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
        if not ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m)):
            return None
        return m.ullAvailPhys / (1024.0 ** 3)
    except Exception:
        return None


def main_after_idle(seconds=20.0, settle=15.0):
    import unreal
    step_name = os.environ.get("LEDGER_MH_STEP", "prepare")
    only = [w.strip() for w in os.environ.get("LEDGER_MH_ONLY", "").split(",") if w.strip()]
    takes = [t.strip() for t in os.environ.get("LEDGER_MH_TAKES", "").split(",") if t.strip()] or [TAKE]
    # every take asked for, each of the cast in it: (who, preset, take)
    cast = [(w, p, t) for t in takes for (w, p) in CAST if not only or w in only]
    st = {"t0": time.time(), "h": None, "i": 0, "phase": "wait", "busy": False}
    out = os.path.join(unreal.Paths.project_dir(), "ue-material.txt")
    sub = unreal.get_editor_subsystem(unreal.MetaHumanCharacterEditorSubsystem)

    def write(l):
        with open(out, "a", encoding="utf-8") as fh:
            fh.write(l + "\n")
        print("make_cast_metahumans: " + l)

    def close_current():
        ch = st.get("ch")
        if ch is not None and sub.is_object_added_for_editing(ch):
            sub.remove_object_to_edit(ch)
        if ch is not None:
            unreal.EditorAssetLibrary.save_loaded_asset(ch, only_if_is_dirty=False)
        st["ch"] = None

    def next_character():
        close_current()
        st["i"] += 1
        st["phase"] = "open" if st["i"] < len(cast) else "quit"

    def open_character():
        who, preset, take = cast[st["i"]]
        use_take(take)
        if brief(who):
            preset = brief(who)["base"]
        dest = CAST_DIR + asset_name(who, BARE)
        st["who"], st["preset"], st["tc"] = who, preset, time.time()
        if not unreal.EditorAssetLibrary.does_asset_exist(dest):
            if step_name != "prepare":
                write(status_line(step_name, who, preset, "NOT-PREPARED", 0, dest + " does not exist"))
                return False
            made = unreal.EditorAssetLibrary.duplicate_asset(PRESET_DIR + preset + "." + preset, dest)
            if made is None:
                write(status_line(step_name, who, preset, "NO-DUPLICATE", 0, "duplicate_asset refused " + preset))
                return False
            unreal.EditorAssetLibrary.save_loaded_asset(made, only_if_is_dirty=False)
        ch = unreal.load_asset(dest)
        if ch is None:
            write(status_line(step_name, who, preset, "NO-LOAD", 0, dest))
            return False
        if step_name == "build":
            f = free_gb()
            if f is not None and f < NEED_FREE_GB:
                write(status_line(step_name, who, preset, "REFUSED", 0, "free %.1f GB under %.0f" % (f, NEED_FREE_GB)))
                return False
        if not sub.try_add_object_to_edit(ch):
            write(status_line(step_name, who, preset, "NOT-EDITABLE", 0, "try_add_object_to_edit refused"))
            return False
        st["ch"] = ch
        st["opened"] = time.time()
        return True

    def apply_casting(ch, who):
        c = brief(who)
        notes = []
        vw = []
        for name, w in c["face"].items():
            src = unreal.load_asset(PRESET_DIR + name + "." + name)
            if src is None:
                notes.append("no-" + name)
                continue
            opened_here = not sub.is_object_added_for_editing(src)
            if opened_here and not sub.try_add_object_to_edit(src):
                notes.append("closed-" + name)
                continue
            vw.append((list(sub.get_face_model_coefficients(src)), w))
            if opened_here:
                sub.remove_object_to_edit(src)
        if vw and all(len(v) == len(vw[0][0]) for v, _ in vw):
            sub.set_face_model_coefficients(ch, blend(vw))
            sub.commit_face_state(ch)
            # The base preset's rig fits the base preset's face, not this one.
            sub.remove_face_rig(ch)
            notes.append("face-of-%d" % len(vw))
        ss = ch.get_editor_property("skin_settings")
        skin = ss.get_editor_property("skin")
        for k, v in c["skin"].items():
            skin.set_editor_property(k, v)
        ss.set_editor_property("skin", skin)
        # 4K FACE TEXTURES, not the default 2K: the close-up shows the difference.
        res = ss.get_editor_property("desired_texture_sources_resolutions")
        for k in ("face_albedo", "face_normal", "face_cavity"):
            try:
                res.set_editor_property(k, unreal.RequestTextureResolution.RES4K)
            except Exception:
                notes.append("no-4k-" + k)
        ss.set_editor_property("desired_texture_sources_resolutions", res)
        sub.commit_skin_settings(ch, ss)
        notes.append("skin")
        cons = sub.get_body_constraints(ch, False)
        held = 0
        for con in cons:
            n = str(con.get_editor_property("name"))
            if n in c["body"]:
                con.set_editor_property("target_measurement", c["body"][n])
                con.set_editor_property("is_active", True)
                held += 1
        sub.set_body_constraints(ch, cons)
        sub.commit_body_state(ch)
        notes.append("body-%d" % held)
        hair = unreal.load_asset(GROOMS + c["hair"] + "." + c["hair"]) if c.get("hair") else None   # none: the preset keeps its own
        if hair is not None:
            col = ch.internal_collection
            item = col.try_add_item_from_wardrobe_item("Hair", hair)
            # SWAPPED, NOT ADDED (take T3): adding a selection left the base
            # preset's haircut on as well, two grooms on one head.
            try:
                col.default_instance.set_single_slot_selection("Hair", item)
                notes.append("hair-swapped")
            except AttributeError:
                col.default_instance.try_add_slot_selection(
                    unreal.MetaHumanPipelineSlotSelection(slot_name="Hair", selected_item=item))
                notes.append("hair-added")
            # THE HAIR'S COLOUR is set on the built hair materials after the
            # build (recolour_hair): the wardrobe's own parameter lookup is not
            # open to scripts. Their names are the hair material's own,
            # hairMelanin and WhiteAmount (probe_hair_materials.py): take T3
            # first set "Melanin" and "Whiteness", which do not exist, and
            # nothing changed.
        # THE BASE PRESET'S OWN FACIAL HAIR OFF where the sheet has none (26
        # September: Ron's candidates kept Walter's and Bruce's beards).
        for slot in c.get("clear", []):
            try:
                ch.internal_collection.default_instance.set_single_slot_selection(slot, unreal.MetaHumanPaletteItemKey())
                notes.append("cleared-" + slot)
            except Exception as e:
                notes.append("clear-%s-refused-%s" % (slot, type(e).__name__))
        # FACIAL HAIR (the candidates): Ron's moustache, Darren's stubble.
        for key, folder, slot in (("mustache", "Mustaches", "Mustache"), ("beard", "Beards", "Beard")):
            name = c.get(key)
            if not name:
                continue
            wi = unreal.load_asset(FACIAL + folder + "/" + name + "." + name)
            if wi is None:
                notes.append("no-" + name)
                continue
            try:
                col = ch.internal_collection
                item = col.try_add_item_from_wardrobe_item(slot, wi)
                col.default_instance.set_single_slot_selection(slot, item)
                notes.append(key)
            except Exception as e:
                notes.append("%s-refused-%s" % (key, type(e).__name__))
        if c.get("no_makeup"):
            sub.commit_makeup_settings(ch, unreal.MetaHumanCharacterMakeupSettings())
            notes.append("no-makeup")
        # THE SHEET'S EYES (26 September): a place on the iris colour chart.
        if c.get("eyes"):
            try:
                e = c["eyes"]
                iris = unreal.MetaHumanCharacterEyeIrisProperties()
                iris.pattern = getattr(unreal.MetaHumanCharacterEyesIrisPattern, e["pattern"])
                iris.primary_color_u = e["u"]
                iris.primary_color_v = e["v"]
                es = ch.get_editor_property("eyes_settings")
                es.eye_left.iris = iris
                es.eye_right.iris = iris
                sub.commit_eyes_settings(character=ch, eyes_settings=es)
                notes.append("eyes")
            except Exception as ex:
                notes.append("eyes-refused-%s" % type(ex).__name__)
        # LIGHT MAKE-UP where the sheet's person would wear it.
        if c.get("makeup"):
            try:
                m = c["makeup"]
                ms = unreal.MetaHumanCharacterMakeupSettings()
                if "eyes" in m:
                    ep = unreal.MetaHumanCharacterEyeMakeupProperties()
                    ep.type = getattr(unreal.MetaHumanCharacterEyeMakeupType, m["eyes"]["type"])
                    ep.opacity = m["eyes"]["opacity"]
                    ep.primary_color = unreal.LinearColor(*m["eyes"]["primary_color"], 1.0)
                    ms.eyes = ep
                if "lips" in m:
                    lp = unreal.MetaHumanCharacterLipsMakeupProperties()
                    lp.type = getattr(unreal.MetaHumanCharacterLipsMakeupType, m["lips"]["type"])
                    lp.opacity = m["lips"]["opacity"]
                    lp.color = unreal.LinearColor(*m["lips"]["color"], 1.0)
                    ms.lips = lp
                if "blush" in m:
                    bp = unreal.MetaHumanCharacterBlushMakeupProperties()
                    bp.type = getattr(unreal.MetaHumanCharacterBlushMakeupType, m["blush"]["type"])
                    bp.intensity = m["blush"]["intensity"]
                    bp.color = unreal.LinearColor(*m["blush"]["color"], 1.0)
                    ms.blush = bp
                sub.commit_makeup_settings(ch, ms)
                notes.append("makeup")
            except Exception as ex:
                notes.append("makeup-refused-%s" % type(ex).__name__)
        return notes

    def ask_cloud():
        ch = st["ch"]
        notes = []
        if brief(st["who"]):
            notes += apply_casting(ch, st["who"])
        # THE PLAIN GARMENT, added after the character is open (with it
        # already in the collection, opening crashed: dress_metahuman.py).
        # BARE, FOR FITTING (24 September): the same preset with no garment,
        # because a built body has its skin removed wherever clothes cover it,
        # and a jacket needs the torso to be fitted to.
        garment = None if BARE else unreal.load_asset(GARMENT)
        # DRESSED AT ONCE (LEDGER_MH_DRESSED=1, 25 September): the plain
        # clothes go on here instead of the plugin's garment, saving the dress
        # step's editor run (one editor holding many candidates ran out of
        # memory).
        dressed = [] if BARE or os.environ.get("LEDGER_MH_DRESSED", "") != "1" else [unreal.load_asset(x) for x in outfit_paths(st["who"])]
        if dressed and all(w is not None for w in dressed):
            col = ch.internal_collection
            for i, wi in enumerate(dressed):
                item = col.try_add_item_from_wardrobe_item("Outfits", wi)
                if i == 0:
                    col.default_instance.set_single_slot_selection("Outfits", item)
                else:
                    col.default_instance.try_add_slot_selection(
                        unreal.MetaHumanPipelineSlotSelection(slot_name="Outfits", selected_item=item))
            notes.append("dressed-%d" % len(dressed))
            garment = None
        elif BARE:
            notes.append("bare")
        elif garment is not None:
            col = ch.internal_collection
            item = col.try_add_item_from_wardrobe_item("Outfits", garment)
            col.default_instance.try_add_slot_selection(
                unreal.MetaHumanPipelineSlotSelection(slot_name="Outfits", selected_item=item))
            notes.append("garment")
        elif not any(n.startswith("dressed") for n in notes):
            notes.append("no-garment")
        sub.request_auto_rigging(ch, unreal.MetaHumanCharacterAutoRiggingRequestParams())
        sub.request_texture_sources(ch, unreal.MetaHumanCharacterTextureRequestParams())
        st["asked"] = time.time()
        st["last"] = 0.0
        write(status_line(step_name, st["who"], st["preset"], "ASKED", time.time() - st["tc"],
                          "+".join(notes) + ";rig-and-textures-requested"))

    def poll_cloud():
        ch = st["ch"]
        now = time.time()
        if now - st["last"] < 3.0:
            return
        st["last"] = now
        rigged = sub.can_build_meta_human(ch, False)
        textured = bool(ch.get_editor_property("has_high_resolution_textures"))
        # A cast take's duplicate may still say "textured" from its base
        # preset before the service answers: the service took 30 s at least.
        early = bool(brief(st["who"])) and now - st["asked"] < 30.0
        if rigged and textured and not early:
            write(status_line(step_name, st["who"], st["preset"], "READY", now - st["tc"],
                              "rigged-and-textured-after-%.0fs" % (now - st["asked"])))
            next_character()
        elif now - st["asked"] > CLOUD_TIMEOUT_S:
            write(status_line(step_name, st["who"], st["preset"], "TIMED-OUT", now - st["tc"],
                              "rigged=%s textured=%s after %d min" % (rigged, textured, CLOUD_TIMEOUT_S // 60)))
            next_character()

    def build():
        ch = st["ch"]
        if not sub.can_build_meta_human(ch, True):
            write(status_line(step_name, st["who"], st["preset"], "CANNOT-BUILD", time.time() - st["tc"], "see the log"))
            return
        p = unreal.MetaHumanCharacterEditorBuildParameters()
        p.set_editor_property("pipeline_type", unreal.MetaHumanDefaultPipelineType.OPTIMIZED)
        # LEDGER_MH_QUALITY=medium (25 September): a build whose hair ran this
        # PC out of memory at High (the swap file cannot grow on a full C:).
        q = os.environ.get("LEDGER_MH_QUALITY", "high").lower()
        p.set_editor_property("pipeline_quality", unreal.MetaHumanQualityLevel.MEDIUM if q == "medium" else unreal.MetaHumanQualityLevel.HIGH)
        p.set_editor_property("absolute_build_path", BUILD_ROOT)
        sub.build_meta_human(ch, p)
        made = unreal.EditorAssetLibrary.list_assets(BUILD_ROOT + "/" + asset_name(st["who"], BARE), recursive=True, include_folder=False)
        recoloured = recolour_hair(st["who"], made)
        # ONLY THIS CHARACTER'S FOLDER (25 September): saving the whole build
        # root with only_if_is_dirty=False loaded every candidate built before
        # it, so each build ran heavier than the last until this PC ran out.
        unreal.EditorAssetLibrary.save_directory(BUILD_ROOT + "/" + asset_name(st["who"], BARE), only_if_is_dirty=False, recursive=True)
        write(status_line(step_name, st["who"], st["preset"], "BUILT", time.time() - st["tc"],
                          "%d-assets-optimized-%s;hair-materials-recoloured-%d" % (len(made), os.environ.get("LEDGER_MH_QUALITY", "high").lower(), recoloured)))

    # LEDGER_MH_STEP=dress: Epic's plain clothes on a prepared take, nothing
    # else changed (24 September, overnight): the plugin's T-shirt and shorts
    # come off the Outfits slot and OUTFITS' three items go on, top, bottom and
    # shoes. The face, skin, body and hair stay as they were; the build step
    # then builds the take as usual.
    if step_name == "dress":
        def dress_tick(delta):
            if time.time() - st["t0"] < seconds or st["busy"]:
                return
            st["busy"] = True
            unreal.unregister_slate_post_tick_callback(st["h"])
            try:
                for who, preset, take in cast:
                    use_take(take)
                    t0 = time.time()
                    ch = unreal.load_asset(CAST_DIR + asset_name(who, BARE))
                    if ch is None:
                        write(status_line(step_name, who, preset, "NOT-PREPARED", 0, CAST_DIR + asset_name(who, BARE)))
                        continue
                    if not sub.try_add_object_to_edit(ch):
                        write(status_line(step_name, who, preset, "NOT-EDITABLE", 0, "try_add_object_to_edit refused"))
                        continue
                    col = ch.internal_collection
                    on, missing = [], []
                    for i, path in enumerate(outfit_paths(who)):
                        wi = unreal.load_asset(path)
                        if wi is None:
                            missing.append(path.split("/")[-1].split(".")[0])
                            continue
                        item = col.try_add_item_from_wardrobe_item("Outfits", wi)
                        if not on:
                            col.default_instance.set_single_slot_selection("Outfits", item)
                        else:
                            col.default_instance.try_add_slot_selection(
                                unreal.MetaHumanPipelineSlotSelection(slot_name="Outfits", selected_item=item))
                        on.append(path.split("/")[-1].split(".")[0])
                    sub.remove_object_to_edit(ch)
                    unreal.EditorAssetLibrary.save_loaded_asset(ch, only_if_is_dirty=False)
                    write(status_line(step_name, who, preset, "DRESSED" if on and not missing else "PART-DRESSED",
                                      time.time() - t0, "on:" + ",".join(on) + (";missing:" + ",".join(missing) if missing else "")))
            except Exception as e:
                write(status_line(step_name, "none", "none", "RAISED", time.time() - st["t0"], repr(e)))
            finally:
                unreal.SystemLibrary.quit_editor()
        st["h"] = unreal.register_slate_post_tick_callback(dress_tick)
        return

    # LEDGER_MH_STEP=recolour: only the hair colour, on a take already built.
    if step_name == "recolour":
        def recolour_tick(delta):
            if time.time() - st["t0"] < seconds or st["busy"]:
                return
            st["busy"] = True
            unreal.unregister_slate_post_tick_callback(st["h"])
            try:
                for who, preset, take in cast:
                    use_take(take)
                    made = unreal.EditorAssetLibrary.list_assets(BUILD_ROOT + "/" + asset_name(who, BARE), recursive=True, include_folder=False)
                    n = recolour_hair(who, made)
                    c = recolour_cloth(who, made)
                    unreal.EditorAssetLibrary.save_directory(BUILD_ROOT + "/" + asset_name(who, BARE), only_if_is_dirty=False, recursive=True)
                    write(status_line(step_name, who, preset, "RECOLOURED", time.time() - st["t0"], "%d-hair-materials;%d-clothing-materials" % (n, c)))
            except Exception as e:
                write(status_line(step_name, "none", "none", "RAISED", time.time() - st["t0"], repr(e)))
            finally:
                unreal.SystemLibrary.quit_editor()
        st["h"] = unreal.register_slate_post_tick_callback(recolour_tick)
        return

    def step():
        now = time.time()
        ph = st["phase"]
        if ph == "wait":
            if now - st["t0"] >= seconds:
                st["phase"] = "open" if cast else "quit"
        elif ph == "open":
            if open_character():
                st["phase"] = "settle"
            else:
                next_character()
        elif ph == "settle":
            if now - st["opened"] < settle:
                return
            if step_name == "prepare":
                # A CAST TAKE IS ALWAYS ASKED: its duplicate carries the base
                # preset's rig and textures, which the casting then changes.
                if not brief(st["who"]) and sub.can_build_meta_human(st["ch"], False) and st["ch"].get_editor_property("has_high_resolution_textures"):
                    write(status_line(step_name, st["who"], st["preset"], "ALREADY-READY", now - st["tc"], "nothing asked"))
                    next_character()
                    return
                ask_cloud()
                st["phase"] = "poll"
            else:
                build()
                next_character()
        elif ph == "poll":
            poll_cloud()
        if st["phase"] == "quit":
            unreal.unregister_slate_post_tick_callback(st["h"])
            unreal.SystemLibrary.quit_editor()

    def tick(delta):
        # NEVER RE-ENTERED: opening for edit and saving both pump the editor's
        # ticks (dress_metahuman.py and request_metahuman_textures.py).
        if st["busy"]:
            return
        st["busy"] = True
        try:
            step()
        except Exception as e:
            write(status_line(step_name, st.get("who", "none"), st.get("preset", "none"), "RAISED",
                              time.time() - st["t0"], repr(e)))
            try:
                next_character()
            except Exception:
                st["phase"] = "quit"
            if st["phase"] == "quit":
                unreal.unregister_slate_post_tick_callback(st["h"])
                unreal.SystemLibrary.quit_editor()
        finally:
            st["busy"] = False

    st["h"] = unreal.register_slate_post_tick_callback(tick)


def selftest():
    ok = bad = 0

    def check(name, cond):
        nonlocal ok, bad
        if cond:
            ok += 1
        else:
            bad += 1
            print("make_cast_metahumans selftest FAIL " + name)
    check("three of the slice's cast", [w for w, _ in CAST] == ["rocco", "lena", "sam"])
    check("each from a shipped preset", all(p for _, p in CAST))
    check("the asset name is the MetaHuman convention", asset_name("rocco") == "MH_Rocco")
    check("the build lands where the probe copies from", BUILD_ROOT == "/Game/Ledger/MetaHumans")
    check("the line names who and what", "who=lena" in status_line("prepare", "lena", "Grace", "READY", 1, "x")
          and "status=READY" in status_line("prepare", "lena", "Grace", "READY", 1, "x"))
    check("a note keeps no spaces", " " not in status_line("p", "w", "p", "S", 1, "a b c").split("note=")[1])
    check("a take sits beside the first", asset_name("lena", take="T2") == "MH_LenaT2")
    check("each of the cast has a brief", sorted(CASTING) == ["lena", "rocco", "sam"])
    check("each brief blends shipped faces and is based on one of them",
          all(c["base"] in c["face"] and abs(sum(c["face"].values()) - 1.0) < 1e-6 for c in CASTING.values()))
    check("the blend is a weighted mean", blend([([0.0, 2.0], 1.0), ([2.0, 4.0], 3.0)]) == [1.5, 3.5])
    check("the hair colour uses the hair material's own names",
          all(k in ("hairMelanin", "hairRedness", "WhiteAmount", "MelaninVariationFine", "MelaninVariationRough")
              for c in CASTING.values() for k in c.get("hair_colour", {})))
    check("only the haircut's own materials are recoloured",
          hair_materials("lena", ["/Game/x/Grooms/MI_WI_Hair_M_BobCurly_None_1_Hair.x", "/Game/x/Grooms/MI_WI_Eyebrows_M_SlightArch_Hair.x",
                                  "/Game/x/Grooms/Hair_M_BobCurly.x"]) == ["/Game/x/Grooms/MI_WI_Hair_M_BobCurly_None_1_Hair.x"])
    check("everyone is dressed head to foot, shoes included",
          sorted(OUTFITS) == ["lena", "rocco", "sam"] and all(len(o) == 3 for o in OUTFITS.values()))
    check("only MetaHuman packages are imported", fab_packages(["oa_jeans.mhpkg", "notes.txt", "x.zip"]) == ["oa_jeans.mhpkg"])
    check("every outfit word names an imported wardrobe item", all(w in FAB_ITEMS for o in OUTFITS.values() for w in o))
    check("an outfit path is a loadable object path", outfit_paths("rocco")[2] == "/Game/Fab/oa_boots/WI_OA_Boots.WI_OA_Boots")
    check("everyone has shoes", all(o[2] in ("flats", "boots", "sneakers") for o in OUTFITS.values()))
    check("only a recoloured garment's built material is picked",
          cloth_materials("rocco", ["/G/MH_RoccoT2/Clothing/MI_WI_OA_Boots_M_shs_boots.x", "/G/MH_RoccoT2/Clothing/MI_WI_OA_Jeans_M_btm.x",
                                    "/G/MH_RoccoT2/Face/MI_WI_OA_Boots_M.x"]) == [("/G/MH_RoccoT2/Clothing/MI_WI_OA_Boots_M_shs_boots.x", "Boots")])
    check("no colour is brighter than cloth", all(0.0 <= v <= 1.0 for g in CLOTH_COLOURS.values() for p in g.values() for c in p.values() for v in c))
    check("skin tone inside the picker", all(0.0 <= c["skin"]["u"] <= 1.0 and 0.0 <= c["skin"]["v"] <= 1.0 for c in CASTING.values()))
    cands = [(t, w, c) for t, byw in CANDIDATES.items() for w, c in byw.items()]
    FIVE = [t for t in CANDIDATES if t.startswith("C")]   # the five he chose from; E takes are tests
    check("five candidates for each of the three", FIVE == ["C1", "C2", "C3", "C4", "C5"]
          and all(sorted(byw) == ["lena", "rocco", "sam"] for t, byw in CANDIDATES.items() if t in FIVE))
    check("every candidate blends shipped faces around its base, weights summing to one",
          all(c["base"] in c["face"] and abs(sum(c["face"].values()) - 1.0) < 1e-6 for _, _, c in cands))
    check("no candidate is made from Grace's face", all("Grace" not in c["face"] for _, _, c in cands))
    check("the candidates of one person all differ", all(len({repr(sorted(CANDIDATES[t][w]["face"].items())) + CANDIDATES[t][w]["hair"]
                                                            for t in FIVE}) == 5 for w in ("lena", "rocco", "sam")))
    check("heights are the sheets' (Sheila about 160, Ron about 186, Darren about 175)",
          all(abs(CANDIDATES[t][w]["body"]["Height"] - h) <= 3 for t in FIVE for w, h in (("lena", 160), ("rocco", 186), ("sam", 175))))
    check("Ron always has his moustache", all(CANDIDATES[t]["rocco"].get("mustache") for t in FIVE))
    use_take("C3")
    check("a candidate take builds to its own brief", brief("rocco") is CANDIDATES["C3"]["rocco"] and asset_name("rocco") == "MH_RoccoC3")
    check("its moustache is recoloured with its hair", hair_materials("rocco", ["/G/MH_RoccoC3/Grooms/MI_WI_Mustache_L_Messy_Hair.x"]) == ["/G/MH_RoccoC3/Grooms/MI_WI_Mustache_L_Messy_Hair.x"])
    use_take("")
    print("make_cast_metahumans selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    print("make_cast_metahumans runs inside the editor; see the header")
