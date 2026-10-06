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
import json
import os
import sys
import time

CAST = [("rocco", "Jorge"), ("lena", "Grace"), ("sam", "Orlando"), ("tom", "Victor")]   # Tom since 6 October (item 1.2)
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
# NOTHING FROM FAB, 3 October (Jafar's licence ruling): Epic's seven garment
# packs (sweater, jeans, slim jeans, T-shirt variants, boots, flats, sneakers)
# are marked on Fab "Allows usage with AI: No" and left the project. The cast
# wear the plain garment the engine's own MetaHuman plugin ships (not a Fab
# item) under the garments the clothing session makes, which the game fits on
# top (tools/ue/import_garments.py); nothing under /Game/Fab is ever put on.
OUTFITS = {
    "lena": ("plain",),
    "rocco": ("plain",),
    "sam": ("plain",),
}
# THE WARDROBE ITEMS, by word. /Game/Fab/ is refused by outfit_paths().
FAB_ITEMS = {
    "plain": GARMENT.split(".")[0],
}
NOAI_ROOTS = ("/Game/Fab/",)


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
    """The wardrobe items one of the cast is dressed in, as loadable object paths; never a NoAI one."""
    out = ["%s.%s" % (FAB_ITEMS[w], FAB_ITEMS[w].split("/")[-1]) for w in OUTFITS.get(who, ())]
    bad = [x for x in out if x.startswith(NOAI_ROOTS)]
    if bad:
        raise ValueError("make_cast_metahumans: NoAI wardrobe items refused: %s" % bad)
    return out


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

# THE THIRD ATTEMPT, 28 September, after research (production/research/
# character-pipeline/eye-colour-2026-09-28.md and faces-and-hair-2026-09-28.md).
# EYES: Epic's own eye presets, every field (004 grey-blue for Sheila, 006 blue
# for Darren). SHEILA'S FACE: pushed along two directions in the face model's
# coefficients, written as a blend with negative weights (they still sum to
# one): European against East Asian among the presets' young women (Celeste,
# Jelena, Vivian against Aera, Lani, Tuya), so the push is not also an age
# change; and old against young among the East Asian women (Grace and Sook-ja
# against Aera, Lani, Tuya), so ethnicity cancels and age remains. Three bases,
# since her last candidates were all one face. DARREN keeps Orlando's face (it
# passed the reviewer) with softer, brassy bleached tips (ombre contrast 0,
# half intensity) on wavier cuts; the hair's shape is still the wardrobe's.
EYES_GREY_BLUE = {"pattern": "IRIS007", "u": 0.2359, "v": 0.7703, "secondary_u": 0.2837, "secondary_v": 0.4953, "blend": 0.6267,
                  "softness": 0.77, "method": "STRUCTURAL", "shadow": 0.5364, "ring_size": 0.8062, "ring_softness": 0.085,
                  "ring_grey": 0.84, "saturation": 0.76}
EYES_BLUE = {"pattern": "IRIS002", "u": 0.234, "v": 0.9891, "secondary_u": 0.2837, "secondary_v": 0.4953, "blend": 0.7327,
             "softness": 0.77, "method": "STRUCTURAL", "shadow": 0.89, "ring_size": 0.775, "ring_softness": 0.085,
             "ring_grey": 0.686, "saturation": 0.88}
SET_GREYING_BROWN = {"hairMelanin": 0.55, "hairRedness": 0.1, "WhiteAmount": 0.35}
SOFT_BLEACH = {"hairMelanin": 0.35, "hairRedness": 0.2, "WhiteAmount": 0.0,
               "Ombre": 1.0, "OmbreMelanin": 0.12, "OmbreRedness": 0.35, "OmbreShift": 0.5, "OmbreContrast": 0.0, "OmbreIntensity": 0.5}
MATTE_LIPSTICK = {"lips": {"type": "NATURAL", "opacity": 0.3, "color": (0.42, 0.14, 0.14)}}


def sheila_face(base, european, older):
    """Base preset + european x (European - East Asian, young women) + older x (old - young, East Asian women)."""
    w = {base: 1.0}
    for n in ("Celeste", "Jelena", "Vivian"):
        w[n] = w.get(n, 0.0) + european / 3.0
    for n in ("Aera", "Lani", "Tuya"):
        w[n] = w.get(n, 0.0) - european / 3.0 - older / 3.0
    for n in ("Grace", "Sook-ja"):
        w[n] = w.get(n, 0.0) + older / 2.0
    return w


THIRD = {
    "Q1": {"lena": _n("Jelena", sheila_face("Jelena", 0.6, 0.5), 121, 0.2, 0.45, 160.0, 0.6, -0.8, "WI_Hair_S_BobLayered", SET_GREYING_BROWN, EYES_GREY_BLUE, makeup=MATTE_LIPSTICK),
           "sam": _n("Orlando", {"Orlando": 1.0}, None, 0.18, 0.45, 175.0, -1.0, -0.3, "WI_Hair_M_Layered", SOFT_BLEACH, EYES_BLUE, ("Mustache",), beard="WI_Beard_S_Stubble")},
    "Q2": {"lena": _n("Jelena", sheila_face("Jelena", 1.0, 0.5), 121, 0.2, 0.45, 160.0, 0.6, -0.8, "WI_Hair_S_BobLayered", SET_GREYING_BROWN, EYES_GREY_BLUE, makeup=MATTE_LIPSTICK),
           "sam": _n("Orlando", {"Orlando": 1.0}, None, 0.18, 0.45, 175.0, -1.0, -0.3, "WI_Hair_M_BobMessy", SOFT_BLEACH, EYES_BLUE, ("Mustache",), beard="WI_Beard_S_Stubble")},
    "Q3": {"lena": _n("Vivian", sheila_face("Vivian", 0.8, 0.5), 121, 0.2, 0.45, 160.0, 0.6, -0.8, "WI_Hair_S_BobLayered", SET_GREYING_BROWN, EYES_GREY_BLUE, makeup=MATTE_LIPSTICK),
           "sam": _n("Orlando", {"Orlando": 0.5, "Victor": 0.5}, None, 0.18, 0.45, 175.0, -1.0, -0.3, "WI_Hair_M_Layered", SOFT_BLEACH, EYES_BLUE, ("Mustache",), beard="WI_Beard_S_Stubble")},
    "Q4": {"lena": _n("Celeste", sheila_face("Celeste", 0.8, 0.6), 121, 0.2, 0.45, 160.0, 0.6, -0.8, "WI_Hair_S_BobLayered", SET_GREYING_BROWN, EYES_GREY_BLUE, makeup=MATTE_LIPSTICK),
           "sam": _n("Victor", {"Victor": 1.0}, None, 0.18, 0.45, 175.0, -1.0, -0.3, "WI_Hair_M_Layered", SOFT_BLEACH, EYES_BLUE, ("Mustache",), beard="WI_Beard_S_Stubble")},
}
# Ron is P2, approved: the third attempt builds only Sheila and Darren (LEDGER_MH_ONLY=lena,sam).
for _t in THIRD:
    THIRD[_t]["rocco"] = SECOND["P2"]["rocco"]
CANDIDATES.update(THIRD)

# FINISHING THE THIRD ATTEMPT, 28 September, from its portraits against the
# sheets and concept portraits. Sheila's Q1 and Q2 read as white English
# women of her age with her grey-blue eyes, but the aged skin set reddens
# their lower lids (the "high" look of 26 September) and the matte lipstick
# reads mauve, where the sheet has "a plain lipstick" and the concept a red
# one. Q3 and Q4 stare or droop and have full mouths: dropped. Darren's
# bleach covers the whole head where the sheet has bleached tips on a grown-out
# perm, and Victor's lids redden too. The faces are kept; only the under-eye
# accent, the lipstick and the hair colour change, and Darren takes Q2's
# messier cut, nearest the concept's shape.
CALM_LIDS = {"under_eye": {"redness": 0.2, "saturation": 0.3, "lightness": 0.55}}
PLAIN_RED = {"lips": {"type": "NATURAL", "opacity": 0.45, "color": (0.5, 0.12, 0.12)}}
TIPPED = {"hairMelanin": 0.5, "hairRedness": 0.15, "WhiteAmount": 0.0,
          "Ombre": 1.0, "OmbreMelanin": 0.1, "OmbreRedness": 0.3, "OmbreShift": 0.6, "OmbreContrast": 0.3, "OmbreIntensity": 0.8}


def _finish(brief, **changes):
    b = json.loads(json.dumps(brief))
    b.update(changes)
    return b


FINISH = {
    "R1": {"lena": _finish(THIRD["Q1"]["lena"], accents=CALM_LIDS, makeup=PLAIN_RED),
           "sam": _finish(THIRD["Q2"]["sam"], accents=CALM_LIDS, hair_colour=TIPPED)},
    "R2": {"lena": _finish(THIRD["Q2"]["lena"], accents=CALM_LIDS, makeup=PLAIN_RED),
           "sam": _finish(THIRD["Q3"]["sam"], accents=CALM_LIDS, hair_colour=TIPPED, hair="WI_Hair_M_BobMessy")},
}
for _t in FINISH:
    FINISH[_t]["rocco"] = SECOND["P2"]["rocco"]
CANDIDATES.update(FINISH)

# FROM DIMENSIONS, 28 September. The blind reviewer failed R1 and R2: Sheila
# long-nosed, full-mouthed and gaunt against a rounder, softer concept with a
# thin mouth; Darren broad-jawed and older against a narrow, pointed concept;
# pink lids on both; Sheila's hair golden, Darren's blond all through in
# profile. Two attempts and the research are spent, so the faces are finished
# from measurements (CLAUDE.md): each concept portrait and each R1 front was
# measured with the eye-to-chin height as the ruler (production/casting/
# candidates-2026-09-28/MEASURES.md), and the landmarks are moved by the
# difference, in centimetres, at MetaHuman's scale (Sheila's eye-to-chin about
# 10.9 cm, Darren's about 12.5).
SHEILA_SHAPE = [
    {"at": "nose_tip", "move": [0.0, -0.1, 0.45]}, {"at": "nose_base", "move": [0.0, 0.0, 0.55]},
    {"at": "nose_wings", "move": [0.0, 0.0, 0.4]},
    {"at": "upper_lip", "move": [0.0, 0.0, 0.1]}, {"at": "upper_lip_sides", "move": [0.0, 0.0, 0.3]},
    {"at": "mouth_corners", "move": [0.0, 0.0, 0.44], "width": 0.875},
    {"at": "lower_lip", "move": [0.0, 0.0, 0.8]}, {"at": "lower_lip_sides", "move": [0.0, 0.0, 0.7], "width": 0.9},
    {"at": "cheeks", "width": 1.15}, {"at": "lower_cheeks", "width": 1.15}, {"at": "cheek_sides", "width": 1.12},
    {"at": "cheekbones", "width": 1.12}, {"at": "jaw_front", "width": 1.08}, {"at": "jaw_angle", "width": 1.08},
    {"at": "chin_sides", "width": 1.05}, {"at": "brows", "move": [0.0, 0.0, -0.1]},
]
DARREN_SHAPE = [
    {"at": "jaw_front", "width": 0.88}, {"at": "jaw_angle", "width": 0.88}, {"at": "chin_sides", "width": 0.85},
    {"at": "chin", "move": [0.0, 0.2, 0.0]}, {"at": "lower_cheeks", "width": 0.9},
    {"at": "cheeks", "move": [0.0, -0.3, 0.0], "width": 0.95},
    {"at": "eyes", "move": [0.2, 0.0, 0.0]}, {"at": "upper_lids", "move": [0.0, 0.0, 0.08]},
    {"at": "nose_tip", "move": [0.0, 0.0, 0.2]}, {"at": "nose_base", "move": [0.0, 0.0, 0.25]},
]
CALMER_LIDS = {"under_eye": {"redness": 0.1, "saturation": 0.2, "lightness": 0.55}}
RED_LIPSTICK = {"lips": {"type": "NATURAL", "opacity": 0.7, "color": (0.45, 0.08, 0.08)}}
ASH_GREYING = {"hairMelanin": 0.6, "hairRedness": 0.0, "WhiteAmount": 0.5}
TIPS_ONLY = dict(TIPPED, OmbreShift=0.8)


def _calm_eyes(eyes):
    return dict(eyes, veins=0.3, veins_cover=0.1)


DIMENSIONS = {
    "S1": {"lena": _finish(THIRD["Q1"]["lena"], accents=CALMER_LIDS, makeup=RED_LIPSTICK, hair_colour=ASH_GREYING,
                           eyes=_calm_eyes(EYES_GREY_BLUE), sculpt=SHEILA_SHAPE),
           "sam": _finish(THIRD["Q2"]["sam"], accents=CALMER_LIDS, hair_colour=TIPS_ONLY, eyes=_calm_eyes(EYES_BLUE),
                          sculpt=DARREN_SHAPE)},
}
for _t in DIMENSIONS:
    DIMENSIONS[_t]["rocco"] = SECOND["P2"]["rocco"]
CANDIDATES.update(DIMENSIONS)

# FROM DIMENSIONS, SECOND PASS, 28 September evening. The blind reviewer
# measured S1 close to Sheila's concept from the front (pupils 0.58 and 0.58,
# cheekbones 1.22 and 1.16, jaw 1.03 and 1.02, nose 0.40 and 0.40) but failed
# her colouring: hair about 1% grey against the concept's two thirds, dark
# brows, a glossy plum lipstick (Epic's lipstick is glossy and metallic by
# default), and a nose tip standing out past the chin twice the concept's.
# Darren: eyes too close (0.51 against 0.56), the lower face long (eyes to
# mouth 0.61 against 0.555), low brows and heavy lids reading sullen, the
# crown too dark and the bleach half the length. The reviewer's numbers, in
# centimetres at MetaHuman's scale, give the moves added here.
SHEILA_SHAPE_2 = SHEILA_SHAPE + [
    {"at": "nose_tip", "move": [0.0, -0.3, 0.0]},          # back toward the face
    {"at": "lower_lip", "move": [0.0, -0.1, 0.25]}, {"at": "lower_lip_sides", "move": [0.0, 0.0, 0.2]},
]
DARREN_SHAPE_2 = DARREN_SHAPE + [
    {"at": "eyes", "move": [0.3, 0.0, 0.0]},                # 0.51 to 0.56 of 12.5 cm: 0.6 cm more between the pupils
    {"at": "brows", "move": [0.0, 0.0, 0.25]}, {"at": "upper_lids", "move": [0.0, 0.0, 0.08]},
    {"at": "upper_lip", "move": [0.0, 0.0, 0.3]}, {"at": "upper_lip_sides", "move": [0.0, 0.0, 0.3]},
    {"at": "mouth_corners", "move": [0.0, 0.0, 0.4]},       # the mouth up with the rest, its corners a touch more
    {"at": "lower_lip", "move": [0.0, 0.0, 0.3]}, {"at": "lower_lip_sides", "move": [0.0, 0.0, 0.3]},
    {"at": "chin", "move": [0.0, 0.0, 0.4]},                # 0.61 to 0.555 of 12.5 cm: the lower face 0.6 cm shorter
]
HALF_GREY = {"hairMelanin": 0.4, "hairRedness": 0.02, "WhiteAmount": 0.65}
GREYING_BROWS = {"hairMelanin": 0.4, "hairRedness": 0.02, "WhiteAmount": 0.35}
PLAIN_MATTE_RED = {"lips": {"type": "NATURAL", "opacity": 0.75, "color": (0.38, 0.06, 0.06), "roughness": 0.75, "metalness": 0.0}}
ASH_TIPS = {"hairMelanin": 0.3, "hairRedness": 0.1, "WhiteAmount": 0.0,
            "Ombre": 1.0, "OmbreMelanin": 0.08, "OmbreRedness": 0.3, "OmbreShift": 0.9, "OmbreContrast": 0.4, "OmbreIntensity": 0.8}
CLEAR_LIDS = {"under_eye": {"redness": 0.05, "saturation": 0.15, "lightness": 0.6}}
DIMENSIONS_2 = {
    "S2": {"lena": _finish(DIMENSIONS["S1"]["lena"], sculpt=SHEILA_SHAPE_2, hair_colour=HALF_GREY, brow_colour=GREYING_BROWS,
                           makeup=PLAIN_MATTE_RED),
           "sam": _finish(DIMENSIONS["S1"]["sam"], sculpt=DARREN_SHAPE_2, hair_colour=ASH_TIPS, accents=CLEAR_LIDS)},
}
for _t in DIMENSIONS_2:
    DIMENSIONS_2[_t]["rocco"] = SECOND["P2"]["rocco"]
CANDIDATES.update(DIMENSIONS_2)

# THIRD PASS, 28 September night, from a fresh reviewer's S2 verdict: Sheila
# has a dark band round the lower lids and in the creases (52% of the cheek's
# brightness; the concept's 87%), reading as eye make-up or soreness, and her
# brows still dark; Darren's upper lids cover a third of the iris (drowsy),
# a grey-green band lies under his eyes, and in profile his hair is blond
# all through, no brown crown.
LIGHT_LIDS = {"under_eye": {"redness": 0.05, "saturation": 0.2, "lightness": 0.8}}
ASH_BROWS = {"hairMelanin": 0.25, "hairRedness": 0.02, "WhiteAmount": 0.5}
NEUTRAL_LIDS = {"under_eye": {"redness": 0.1, "saturation": 0.1, "lightness": 0.65}}
TIPS_ONLY_SHARP = dict(ASH_TIPS, OmbreShift=1.0, OmbreContrast=0.8)
SHEILA_SHAPE_3 = SHEILA_SHAPE_2 + [{"at": "lower_lids", "move": [0.0, 0.0, 0.05]}]
DARREN_SHAPE_3 = DARREN_SHAPE_2 + [{"at": "upper_lids", "move": [0.0, 0.0, 0.2]}]
DIMENSIONS_3 = {
    "S3": {"lena": _finish(DIMENSIONS_2["S2"]["lena"], sculpt=SHEILA_SHAPE_3, accents=LIGHT_LIDS, brow_colour=ASH_BROWS),
           "sam": _finish(DIMENSIONS_2["S2"]["sam"], sculpt=DARREN_SHAPE_3, accents=NEUTRAL_LIDS, hair_colour=TIPS_ONLY_SHARP)},
}
for _t in DIMENSIONS_3:
    DIMENSIONS_3[_t]["rocco"] = SECOND["P2"]["rocco"]
CANDIDATES.update(DIMENSIONS_3)

# FOURTH PASS, 28 September night, from S3's reviewer, in the studio light
# (the one light every take is now judged in): Sheila's hair reads warm and
# golden (saturation 0.16) where the concept's is a cool grey-brown (0.07),
# and her brows now pale (0.65 of full brightness against the concept's 0.33;
# S2's were called too dark, so between the two); Darren's hair is blond from
# root to tip (0.53 to 0.71 against the concept's dark brown base, 0.16 to
# 0.26), his lids still heavy (65% of the iris showing) and grey-green under
# the eyes (too little saturation there reads grey).
COOL_GREY_BROWN = {"hairMelanin": 0.6, "hairRedness": 0.0, "WhiteAmount": 0.5}
MID_BROWS = {"hairMelanin": 0.5, "hairRedness": 0.02, "WhiteAmount": 0.2}
BROWN_BLEACHED_ENDS = {"hairMelanin": 0.65, "hairRedness": 0.1, "WhiteAmount": 0.0,
                       "Ombre": 1.0, "OmbreMelanin": 0.15, "OmbreRedness": 0.25, "OmbreShift": 1.0, "OmbreContrast": 0.8, "OmbreIntensity": 0.8}
PLAIN_LIDS = {"under_eye": {"redness": 0.35, "saturation": 0.5, "lightness": 0.62}}
DARREN_SHAPE_4 = DARREN_SHAPE_3 + [{"at": "upper_lids", "move": [0.0, 0.0, 0.25]}, {"at": "lower_lids", "move": [0.0, 0.0, -0.05]}]
DIMENSIONS_4 = {
    "S4": {"lena": _finish(DIMENSIONS_3["S3"]["lena"], hair_colour=COOL_GREY_BROWN, brow_colour=MID_BROWS),
           "sam": _finish(DIMENSIONS_3["S3"]["sam"], sculpt=DARREN_SHAPE_4, accents=PLAIN_LIDS, hair_colour=BROWN_BLEACHED_ENDS)},
}
for _t in DIMENSIONS_4:
    DIMENSIONS_4[_t]["rocco"] = SECOND["P2"]["rocco"]
CANDIDATES.update(DIMENSIONS_4)

# DARREN'S HAIR, 29 September: Jafar picked Sheila's S4 and turned Darren's
# down for its "woman's haircut" (the long cut); curls grown in Blender were
# set aside after three attempts, so his S4 face gets Epic's two plain short
# men's cuts, his bleached ends kept: S5 the messy crop, S6 the casual cut
# with a fringe. Build them with LEDGER_MH_ONLY=sam.
DARREN_HAIR = {
    "S5": {"sam": _finish(DIMENSIONS_4["S4"]["sam"], hair="WI_Hair_S_Messy")},
    "S6": {"sam": _finish(DIMENSIONS_4["S4"]["sam"], hair="WI_Hair_S_Casual")},
}
for _t in DARREN_HAIR:
    DARREN_HAIR[_t]["lena"] = DIMENSIONS_4["S4"]["lena"]
    DARREN_HAIR[_t]["rocco"] = SECOND["P2"]["rocco"]
CANDIDATES.update(DARREN_HAIR)

# TOM, 6 October (phase 1, item 1.2: "one complete Tom"; production/research/pre-production/
# 3-PROOFS.md P8: "build Tom from his casting sheet by the scripted MetaHuman route"). His sheet
# (production/casting/tom-nowak/SHEET.md, approved as text 28 September): 32, son of a Polish
# post-war settler and Mickey's sister; about 175 cm, lean; clean-shaven, ordinary; short dark
# brown hair, short back and sides. The other three's faces are frozen (RULINGS 30 September):
# Ron from Bruce, Sheila from Jelena, Darren from Orlando, so Tom leads from a preset none of
# them leads from, Victor (his own picture reads a white European man in his thirties), or
# Lorenzo; each led by one preset at 80% or more (the 26 September lesson: even blends average
# toward a flat middle face), the preset's own skin set (a swapped set carries another person's
# lids and nose), its beard and moustache taken off, no make-up, his eyes the preset's own
# (Epic's chart places taken from Walter and Orlando came out green). A face is his to approve.
DARK_BROWN = {"hairMelanin": 0.8, "hairRedness": 0.12, "WhiteAmount": 0.0}
TOM_CLEAR = ("Beard", "Mustache")
TOM = {
    "A1": _c("Victor", {"Victor": 1.0}, None, 0.22, 0.45, 175.0, -0.5, 0.0, "WI_Hair_S_Clean", DARK_BROWN),
    "A2": _c("Victor", {"Victor": 0.8, "Lorenzo": 0.2}, None, 0.23, 0.47, 175.0, -0.5, 0.0, "WI_Hair_S_SideSweptFringe", DARK_BROWN),
    "A3": _c("Victor", {"Victor": 0.8, "Walter": 0.2}, None, 0.22, 0.48, 175.0, -0.6, -0.1, "WI_Hair_S_Clean", DARK_BROWN),
    "A4": _c("Lorenzo", {"Lorenzo": 0.8, "Victor": 0.2}, None, 0.24, 0.47, 175.0, -0.5, 0.0, "WI_Hair_S_Clean", DARK_BROWN),
    "A5": _c("Victor", {"Victor": 0.85, "Bruce": 0.15}, None, 0.23, 0.46, 175.0, -0.4, 0.1, "WI_Hair_S_SideSweptFringe", DARK_BROWN),
}
# THE SECOND TRY, 6 October afternoon. The blind reviewer failed all five: A1, A2, A3 and A5 were
# one face (Victor's, his blends too slight to differ), which from the front reads Central or part
# East Asian (narrow eyes under a heavy lid, broad flat cheekbones, a low wide nose bridge, olive
# skin), the profile European; A4 read 50 and South Asian or Latin American; the hair modern or
# gelled and near-black, a stubble shadow on lip and chin. So the method changes, not the dial:
# Victor's skin set (28) and Lorenzo's are left; the faces lead from the presets whose own faces
# read Northern European, Bruce's and Orlando's in an even pair and Walter's shape on Orlando's
# skin: Bruce's own skin set (13, which nobody wears: Ron wears the aged 121) or Orlando's (85,
# Darren's too, so the blind check is also asked whether any of them looks like Ron or Darren);
# fairer skin; the chin lightened against the
# scanned beard shadow; Epic's brush cut, a short back and sides; mid brown; the grey-blue eyes
# whose every field was set (Sheila's, which render grey-blue, not green).
MID_BROWN = {"hairMelanin": 0.62, "hairRedness": 0.18, "WhiteAmount": 0.0}
SHAVED_CHIN = {"chin": {"redness": 0.5, "saturation": 0.4, "lightness": 0.6}}
TOM_SECOND = {
    "B1": _c("Bruce", {"Bruce": 0.5, "Orlando": 0.5}, 13, 0.24, 0.5, 175.0, -0.5, 0.0, "WI_Hair_S_BrushCut", MID_BROWN),
    "B2": _c("Orlando", {"Orlando": 0.4, "Walter": 0.6}, 85, 0.22, 0.48, 175.0, -0.5, 0.0, "WI_Hair_S_BrushCut", MID_BROWN),
    "B3": _c("Bruce", {"Bruce": 0.4, "Walter": 0.3, "Orlando": 0.3}, 13, 0.23, 0.5, 175.0, -0.5, 0.0, "WI_Hair_S_Casual", MID_BROWN),
    "B4": _c("Orlando", {"Orlando": 0.5, "Bruce": 0.3, "Walter": 0.2}, 85, 0.23, 0.47, 175.0, -0.5, 0.0, "WI_Hair_S_BrushCut", MID_BROWN),
}
for _t, _b in TOM_SECOND.items():
    _b["eyes"] = EYES_GREY_BLUE
    _b["accents"] = SHAVED_CHIN
TOM.update(TOM_SECOND)
# THE THIRD STEP, from B2, 6 October afternoon. The blind reviewer passed B2 with narrow points:
# a clear Polish-English read, lean, no likeness to Ron; but he reads 25 to 27 (the sheet's 32),
# the brush cut's squared barber's edge reads a modern crop, the hair turns ginger in profile, and
# beside Darren (Orlando's face too, and his eyes) a "brothers" read is a small risk. So: B2's face,
# aged by Bruce's skin set (13, which read 42 on the heavier B1 face) or by more of Walter's shape
# and a shadow under the eyes on his own (85); a plain side-parted cut (Epic's casual or clean); the
# brown with less red; the brows darker, so his face reads apart from Darren's fair one.
TOM_BROWN = {"hairMelanin": 0.7, "hairRedness": 0.06, "WhiteAmount": 0.0}
TOM_BROWS = {"hairMelanin": 0.75, "hairRedness": 0.05, "WhiteAmount": 0.0}
OLDER_LIDS = {"under_eye": {"redness": 0.45, "saturation": 0.4, "lightness": 0.42}}
TOM_THIRD = {
    "D1": _c("Orlando", {"Orlando": 0.4, "Walter": 0.6}, 13, 0.22, 0.48, 175.0, -0.5, 0.0, "WI_Hair_S_Casual", TOM_BROWN),
    "D2": _c("Orlando", {"Orlando": 0.3, "Walter": 0.7}, 85, 0.22, 0.48, 175.0, -0.5, 0.0, "WI_Hair_S_Casual", TOM_BROWN),
    "D3": _c("Orlando", {"Orlando": 0.4, "Walter": 0.6}, 13, 0.22, 0.48, 175.0, -0.5, 0.0, "WI_Hair_S_Clean", TOM_BROWN),
}
for _t, _b in TOM_THIRD.items():
    _b["eyes"] = EYES_GREY_BLUE
    _b["accents"] = dict(SHAVED_CHIN, **(OLDER_LIDS if _b["skin"]["face_texture_index"] == 85 else {}))
    _b["brow_colour"] = TOM_BROWS
TOM.update(TOM_THIRD)
# THE FOURTH STEP, from D2, 6 October. The blind reviewer: D2 alone is his age (29), Slavic or
# Eastern European, ordinary, lean, clean-shaven and unlike Ron or Darren, "close" to going before
# him; what stops it is the hair (wet-looking strands, black from the front and brown in profile)
# and red spots on cheeks and chin. So: D2's face and skin; the hair dry and matt (the hair
# material's own roughness settings, read by tools/ue/probe_hair_materials.py, raised: it was the
# shine that read as gel and as black) in a lighter mid-dark brown, in the clean cut the reviewer
# called the best period one (G1) or D2's own (G2); the cheeks and chin calmed.
TOM_MATT_BROWN = {"hairMelanin": 0.6, "hairRedness": 0.08, "WhiteAmount": 0.0,
                  "RoughnessOverall": 0.75, "HairRoughness": 0.6, "RoughnessTRT": 0.6}
CALM_SKIN = {"cheeks": {"redness": 0.35, "saturation": 0.4, "lightness": 0.52},
             "chin": {"redness": 0.35, "saturation": 0.35, "lightness": 0.6}}
TOM_FOURTH = {
    "G1": _finish(TOM_THIRD["D2"], hair="WI_Hair_S_Clean", hair_colour=TOM_MATT_BROWN,
                  accents=dict(OLDER_LIDS, **CALM_SKIN)),
    "G2": _finish(TOM_THIRD["D2"], hair_colour=TOM_MATT_BROWN, accents=dict(OLDER_LIDS, **CALM_SKIN)),
}
TOM.update(TOM_FOURTH)
# THE FIFTH STEP, 6 October: G1 and G2 came out with frosted white brows and lashes and a darker
# face. Two changes were in them at once, the hair's roughness and the calmer skin, and the service
# had been asked to wait only 30 s; so the roughness is left out and the wait doubled, to tell which.
TOM_PLAIN_BROWN = {"hairMelanin": 0.6, "hairRedness": 0.08, "WhiteAmount": 0.0}
TOM_FIFTH = {
    "H1": _finish(TOM_THIRD["D2"], hair="WI_Hair_S_Clean", hair_colour=TOM_PLAIN_BROWN,
                  accents=dict(OLDER_LIDS, **CALM_SKIN)),
    "H2": _finish(TOM_THIRD["D2"], hair_colour=TOM_PLAIN_BROWN, accents=dict(OLDER_LIDS, **CALM_SKIN)),
}
TOM.update(TOM_FIFTH)
# THE SIXTH STEP, from H2, 6 October evening. The blind reviewer: H2's face is "the right man"
# (Slavic, pale, light grey-blue eyes, nothing of Ron), with narrow points: the hair near-black in
# front and mid brown with golden tips in profile, wet-looking, swept up (and in profile an echo of
# Darren's bleached tips); spots on the cheeks; tired eyes and a downturned mouth. Epic's grooms
# ship with their own highlights and ombre on (mh-hair-materials.txt: Highlights 1, Ombre 1 on
# some), which is the golden tips; so both off and the brown's variation lowered, the cheeks calmer,
# the upper lids lifted a little and the mouth's corners with them. I1 keeps D2's casual cut; I2
# the brush cut, a short back and sides with a flat top.
TOM_HAIR_PLAIN = {"hairMelanin": 0.62, "hairRedness": 0.06, "WhiteAmount": 0.0, "Ombre": 0.0, "Highlights": 0.0,
                  "MelaninVariationFine": 0.3, "MelaninVariationRough": 0.2}
CALMER_CHEEKS = {"cheeks": {"redness": 0.3, "saturation": 0.35, "lightness": 0.55},
                 "chin": {"redness": 0.35, "saturation": 0.35, "lightness": 0.6}}
TOM_RESTED = [{"at": "upper_lids", "move": [0.0, 0.0, 0.06]}, {"at": "mouth_corners", "move": [0.0, 0.0, 0.05]}]
TOM_SIXTH = {
    "I1": _finish(TOM_FIFTH["H2"], hair_colour=TOM_HAIR_PLAIN, accents=dict(OLDER_LIDS, **CALMER_CHEEKS), sculpt=TOM_RESTED),
    "I2": _finish(TOM_FIFTH["H2"], hair="WI_Hair_S_BrushCut", hair_colour=TOM_HAIR_PLAIN,
                  accents=dict(OLDER_LIDS, **CALMER_CHEEKS), sculpt=TOM_RESTED),
}
TOM.update(TOM_SIXTH)
# THE SEVENTH STEP, from I2, 6 October evening. The blind reviewer failed H2, I1 and I2 and ranked
# I2 first: its short back and sides is the sheet's cut and reads younger; what stops all three is a
# dead, tired stare (heavy lids, the dark under the eyes), an age of 35 to 40 against the sheet's 32,
# a soft full jaw and neck where the sheet says lean, and on I2 a bronze to ginger buzz-cut top with
# frosted tips and a hard, cap-like hairline. So: a true dark brown with no red and no lighter tips;
# Epic's side-swept fringe (J1) or its short messy cut (J2), each a few centimetres on top with a
# broken front line; the lids opened a little more, the under-eye lighter, not darker; the jaw and
# the body a little leaner. (The catchlight is the portrait's light, judged with -PortraitStudio.)
TOM_DARK_BROWN = {"hairMelanin": 0.8, "hairRedness": 0.03, "WhiteAmount": 0.0, "Ombre": 0.0, "Highlights": 0.0,
                  "MelaninVariationFine": 0.15, "MelaninVariationRough": 0.1}
YOUNGER_LIDS = {"under_eye": {"redness": 0.35, "saturation": 0.35, "lightness": 0.56}}
TOM_AWAKE = [{"at": "upper_lids", "move": [0.0, 0.0, 0.12]}, {"at": "mouth_corners", "move": [0.0, 0.0, 0.05]},
             {"at": "jaw_angle", "width": 0.95}, {"at": "jaw_front", "width": 0.97}]
TOM_LEAN = {"Height": 175.0, "Fat": -0.8, "Muscularity": 0.0}
TOM_SEVENTH = {
    "J1": _finish(TOM_FIFTH["H2"], hair="WI_Hair_S_SideSweptFringe", hair_colour=TOM_DARK_BROWN,
                  accents=dict(YOUNGER_LIDS, **CALMER_CHEEKS), sculpt=TOM_AWAKE, body=TOM_LEAN),
    "J2": _finish(TOM_FIFTH["H2"], hair="WI_Hair_S_Messy", hair_colour=TOM_DARK_BROWN,
                  accents=dict(YOUNGER_LIDS, **CALMER_CHEEKS), sculpt=TOM_AWAKE, body=TOM_LEAN),
}
TOM.update(TOM_SEVENTH)
# THE EIGHTH STEP, from J2, 6 October night. A fresh blind reviewer ranked J2 first: the eyes alive
# now (catchlights, lids fine), Polish and ordinary, about 28 to 30; what stops it: the messy cut
# worn as a tall glossy quiff (a 2020s read), brows mid brown under near-black hair, faint lashes, no
# shave shadow on a dark-haired man (the lower face smooth, the lips pink), soft jowls. So: brows and
# lashes as dark as the hair; a faint grey shadow on the chin; the lips' colour taken down
# (the skin's own accents, not make-up); the jaw a little narrower again. K1 keeps J2's cut; K2 tries the brush cut again in the dark
# brown (I2's cut was the sheet's, its colour and frosted tips what failed).
TOM_DARK_BROWS = {"hairMelanin": 0.9, "hairRedness": 0.02, "WhiteAmount": 0.0}
SHAVE_SHADOW = {"chin": {"redness": 0.25, "saturation": 0.2, "lightness": 0.45},
                "lips": {"redness": 0.35, "saturation": 0.3, "lightness": 0.5}}
TOM_FIRMER = TOM_AWAKE[:2] + [{"at": "jaw_angle", "width": 0.92}, {"at": "jaw_front", "width": 0.95},
                              {"at": "chin_sides", "width": 0.97}]
TOM_EIGHTH = {
    "K1": _finish(TOM_SEVENTH["J2"], brow_colour=TOM_DARK_BROWS, accents=dict(YOUNGER_LIDS, **dict(CALMER_CHEEKS, **SHAVE_SHADOW)),
                  sculpt=TOM_FIRMER),
    "K2": _finish(TOM_SEVENTH["J2"], hair="WI_Hair_S_BrushCut", brow_colour=TOM_DARK_BROWS,
                  accents=dict(YOUNGER_LIDS, **dict(CALMER_CHEEKS, **SHAVE_SHADOW)), sculpt=TOM_FIRMER),
}
TOM.update(TOM_EIGHTH)
# THE NINTH STEP, from K2, 6 October night. A fourth blind reviewer ranked K2 (the brush cut) ahead:
# about 32 to 36, eyes alive, nothing faulty in the face; what stops it: no shave shadow (the chin's
# accent too light to show), the lips lilac, the brows still lighter than the hair, faint lashes,
# and the cut a modern clipper crop where 1990's short back and sides has length on top, combed to
# a side parting. The sheet keeps him clean-shaven (no stubble groom: a check holds that), so the
# shadow is the skin's: the chin darker and greyer. The lips warmer. Epic's fine lashes in place
# of the preset's sparse ones. L1 tries Epic's clean cut in the dark brown with no highlights (its
# frosting in H1 was the groom's own highlights, off since I1); L2 its casual cut, combed.
SHAVEN = {"chin": {"redness": 0.2, "saturation": 0.15, "lightness": 0.36},
          "lips": {"redness": 0.5, "saturation": 0.45, "lightness": 0.5}}
TOM_NINTH = {
    "L1": _finish(TOM_EIGHTH["K2"], hair="WI_Hair_S_Clean", eyelashes="WI_Eyelashes_S_Fine",
                  accents=dict(YOUNGER_LIDS, **dict(CALMER_CHEEKS, **SHAVEN))),
    "L2": _finish(TOM_EIGHTH["K2"], hair="WI_Hair_S_Casual", eyelashes="WI_Eyelashes_S_Fine",
                  accents=dict(YOUNGER_LIDS, **dict(CALMER_CHEEKS, **SHAVEN))),
}
TOM.update(TOM_NINTH)
# THE TENTH STEP, from L1, 6 October night. A fifth blind reviewer: L1 (Epic's clean cut) "one narrow
# round of fixes away" - about 30 to 33, Polish and ordinary, the eyes alive, a good tapered short back
# and sides in profile; what stops it: still no shave shadow, the top glossy with light glints, the
# hair near-black where the sheet says dark brown, the brows lighter and sparse, the lips pale, the
# jaw soft. So: the brown warmed a little; Epic's dense brows (M1) or thick ones (M2) in the hair's
# own dark; the chin's shadow much stronger (the last was too light to show); the lips muted; the
# jaw narrower again.
TOM_WARM_DARK = {"hairMelanin": 0.72, "hairRedness": 0.09, "WhiteAmount": 0.0, "Ombre": 0.0, "Highlights": 0.0,
                 "MelaninVariationFine": 0.15, "MelaninVariationRough": 0.1}
TOM_MATCHED_BROWS = {"hairMelanin": 0.8, "hairRedness": 0.08, "WhiteAmount": 0.0}
SHAVEN_DARKER = {"chin": {"redness": 0.15, "saturation": 0.1, "lightness": 0.24},
                 "lips": {"redness": 0.42, "saturation": 0.32, "lightness": 0.48}}
TOM_LEANER = TOM_AWAKE[:2] + [{"at": "jaw_angle", "width": 0.9}, {"at": "jaw_front", "width": 0.94},
                              {"at": "chin_sides", "width": 0.96}, {"at": "lower_cheeks", "width": 0.95}]
TOM_TENTH = {
    "M1": _finish(TOM_NINTH["L1"], hair_colour=TOM_WARM_DARK, brow_colour=TOM_MATCHED_BROWS, eyebrows="WI_Eyebrows_M_Dense",
                  accents=dict(YOUNGER_LIDS, **dict(CALMER_CHEEKS, **SHAVEN_DARKER)), sculpt=TOM_LEANER),
    "M2": _finish(TOM_NINTH["L1"], hair_colour=TOM_WARM_DARK, brow_colour=TOM_MATCHED_BROWS, eyebrows="WI_Eyebrows_M_Thick",
                  accents=dict(YOUNGER_LIDS, **dict(CALMER_CHEEKS, **SHAVEN_DARKER)), sculpt=TOM_LEANER),
}
TOM.update(TOM_TENTH)
# THE ELEVENTH STEP, a new direction, 7 October (production/research/casting/TOM-FACE-METHOD-2026-10-07.md,
# experiment N1). After ten steps of the same blend the research found two causes the tweaks could not
# reach: the grooms' colours are the character's own parameters, baked into the face at build (so the
# brows stayed at the default 0.16), and Epic's table of skin textures lists 85 as carrying no stubble
# and medium marks. So L1's face and cut, its hair, brows and lashes coloured on the character before
# the build, on four skin textures: 85 (the control), 84 (low wrinkles, low marks, low stubble), 31 and
# 148 (low wrinkles and marks, medium stubble); no chin accent, the skin's own shadow doing it; the
# preset's sparse lashes replaced by Epic's fine ones and its brows by the dense ones.
TOM_GROOM_COLOUR = {"Hair": {"Melanin": 0.75, "Redness": 0.08, "Roughness": 0.55},
                    "Eyebrows": {"Melanin": 0.75, "Redness": 0.08},
                    "Eyelashes": {"Melanin": 0.8, "Redness": 0.05}}
TOM_ELEVENTH = {}
for _k, _tex in (("N1", 85), ("N2", 84), ("N3", 31), ("N4", 148)):
    _b = _finish(TOM_NINTH["L1"], eyebrows="WI_Eyebrows_M_Dense", eyelashes="WI_Eyelashes_S_Fine",
                 groom_params=TOM_GROOM_COLOUR, accents=dict(YOUNGER_LIDS, cheeks=CALMER_CHEEKS["cheeks"]))
    _b["skin"] = dict(_b["skin"], face_texture_index=_tex)
    TOM_ELEVENTH[_k] = _b
TOM.update(TOM_ELEVENTH)
for _t, _b in TOM.items():
    _b["clear"] = list(TOM_CLEAR)
    CANDIDATES[_t] = {"tom": _b}


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


def brow_materials(who, paths):
    """The built eyebrows' material instances among a take's asset paths, when the brief gives them a colour
    (28 September: the brows kept the base preset's, and Sheila's dark ones made her read darker and younger)."""
    c = brief(who) if TAKE else CASTING.get(who)
    if not c or not c.get("brow_colour"):
        return []
    return [p for p in paths if "/Grooms/" in p and p.split("/")[-1].split(".")[0].startswith("MI_") and "Eyebrows" in p]


def recolour_hair(who, made):
    """Sets the brief's hair colour on the built haircut's materials, and its brow colour on the eyebrows'; how many."""
    import unreal
    n = 0
    jobs = [(p, "hair_colour") for p in (hair_materials(who, made) if TAKE else [])]
    jobs += [(p, "brow_colour") for p in (brow_materials(who, made) if TAKE else [])]
    for path, key in jobs:
        mi = unreal.load_asset(path)
        if not isinstance(mi, unreal.MaterialInstanceConstant):
            continue
        for pname, value in brief(who)[key].items():
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


# THE FACE LANDMARKS (MetaHumanCharacterEditorSubsystem.get_face_landmarks, 88
# points; numbered from Jelena's, F:/LedgerTools/mh-dress/preset-coeffs.json,
# and a plot of them front and side, 28 September). Centimetres: x to the
# face's left (the viewer's right), y forward, z up.
MARK = {
    "nose_tip": [64], "nose_base": [65], "nose_bridge": [6], "nose_wings": [67, 45],
    "upper_lip": [5, 47, 31], "upper_lip_sides": [49, 34], "mouth_corners": [48, 32],
    "lower_lip": [4], "lower_lip_sides": [9, 16],
    "chin": [62], "chin_sides": [3, 30], "jaw_front": [63, 43], "jaw_angle": [68, 46],
    "cheeks": [2, 29], "lower_cheeks": [1, 28], "cheek_sides": [55, 21], "cheekbones": [66, 23],
    "upper_lids": [51, 44, 52, 36, 20, 35], "lower_lids": [53, 33, 37, 19],
    "brows": [10, 77, 24, 26],
    "eyes": [51, 44, 52, 53, 33, 22, 57, 36, 20, 35, 37, 19, 18, 40],
}


def sculpt_deltas(marks, ops):
    """The move for each landmark from a list of ops: {"at": MARK name, "move": [dx, dy, dz]}
    (the same move for each point; dx is outward from the middle, mirrored on the
    right) or {"at": name, "width": k} (distance from the middle times k). Summed."""
    out = {}
    for op in ops:
        for i in MARK[op["at"]]:
            x = marks[i][0]
            side = -1.0 if x < 0 else 1.0
            d = out.setdefault(i, [0.0, 0.0, 0.0])
            if "move" in op:
                dx, dy, dz = op["move"]
                d[0] += dx * side
                d[1] += dy
                d[2] += dz
            if "width" in op:
                d[0] += x * (op["width"] - 1.0)
    return {i: tuple(v) for i, v in out.items()}


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
    cast = [(w, p, t) for t in takes for (w, p) in CAST if (not only or w in only) and (t not in CANDIDATES or w in CANDIDATES[t])]
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
            if c.get("sculpt"):
                marks = [(v.x, v.y, v.z) for v in sub.get_face_landmarks(ch)]
                moves = sculpt_deltas(marks, c["sculpt"])
                sub.translate_face_landmarks(ch, sorted(moves), [unreal.Vector(*moves[i]) for i in sorted(moves)])
                sub.commit_face_state(ch)
                notes.append("sculpt-%d" % len(moves))
            # The base preset's rig fits the base preset's face, not this one.
            sub.remove_face_rig(ch)
            notes.append("face-of-%d" % len(vw))
        ss = ch.get_editor_property("skin_settings")
        skin = ss.get_editor_property("skin")
        for k, v in c["skin"].items():
            skin.set_editor_property(k, v)
        ss.set_editor_property("skin", skin)
        # ACCENTS: the skin's per-region redness, saturation and lightness
        # (0.5 is neutral); the aged skin set reddens the lower lids.
        if c.get("accents"):
            acc = ss.get_editor_property("accents")
            for region, vals in c["accents"].items():
                r = acc.get_editor_property(region)
                for k, v in vals.items():
                    r.set_editor_property(k, v)
                acc.set_editor_property(region, r)
            ss.set_editor_property("accents", acc)
            notes.append("accents")
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
        slot_items = {}   # the groom items set below, for their colours before the build
        hair = unreal.load_asset(GROOMS + c["hair"] + "." + c["hair"]) if c.get("hair") else None   # none: the preset keeps its own
        if hair is not None:
            col = ch.internal_collection
            item = col.try_add_item_from_wardrobe_item("Hair", hair)
            slot_items["Hair"] = item
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
        # AND THE LASHES (6 October: three reviewers in turn found Tom's preset lashes faint).
        for key, folder, slot in (("mustache", "Mustaches", "Mustache"), ("beard", "Beards", "Beard"),
                                  ("eyelashes", "Eyelashes", "Eyelashes"), ("eyebrows", "Eyebrows", "Eyebrows")):
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
                slot_items[slot] = item
                notes.append(key)
            except Exception as e:
                notes.append("%s-refused-%s" % (key, type(e).__name__))
        # THE GROOMS' COLOURS ON THE CHARACTER, BEFORE THE BUILD (7 October; production/research/casting/
        # TOM-FACE-METHOD-2026-10-07.md, section 2): each groom's Melanin, Redness and the rest are the
        # character's instance parameters, and the build bakes the brows' into the face skin as a
        # painted layer; recolour_hair's write to the built groom material afterwards left that layer
        # at the default 0.16, so the brows read pale ash under dark hair in four reviews. Epic's own
        # example (MetaHumanCharacter/Content/Python/examples/example_add_grooms.py): assemble for
        # preview, read the item's instance parameters, set_float.
        if c.get("groom_params"):
            try:
                sub.assemble_for_preview(character=ch)
                set_n = 0
                for slot, vals in c["groom_params"].items():
                    item = slot_items.get(slot)
                    if item is None:
                        notes.append("groom-params-%s-no-item" % slot)
                        continue
                    params = ch.internal_collection.default_instance.get_instance_parameters(
                        item_path=unreal.MetaHumanPaletteItemPath(item_key=item))
                    for prm in params:
                        if prm.name in vals:
                            prm.set_float(value=float(vals[prm.name]))
                            set_n += 1
                notes.append("groom-params-%d" % set_n)
            except Exception as e:
                notes.append("groom-params-refused-%s" % type(e).__name__)
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
                # EVERY FIELD, 28 September: a fresh iris keeps the C++ defaults
                # for the rest (an olive secondary at double saturation), which
                # turned every eye green (research: eye-colour-2026-09-28.md).
                if "secondary_u" in e:
                    iris.secondary_color_u = e["secondary_u"]
                    iris.secondary_color_v = e["secondary_v"]
                    iris.color_blend = e["blend"]
                    iris.color_blend_softness = e["softness"]
                    iris.blend_method = getattr(unreal.MetaHumanCharacterEyesBlendMethod, e["method"])
                    iris.shadow_details = e["shadow"]
                    iris.limbal_ring_size = e["ring_size"]
                    iris.limbal_ring_softness = e["ring_softness"]
                    iris.limbal_ring_color = unreal.LinearColor(e["ring_grey"], e["ring_grey"], e["ring_grey"], 1.0)
                    iris.global_saturation = e["saturation"]
                    iris.global_tint = unreal.LinearColor(1.0, 1.0, 1.0, 1.0)
                es = ch.get_editor_property("eyes_settings")
                es.eye_left.iris = iris
                es.eye_right.iris = iris
                # THE WHITES' VEINS (28 September; the blind reviewer: sore,
                # pink eyes): Epic's default is full intensity.
                if "veins" in e:
                    for eye in (es.eye_left, es.eye_right):
                        sc = eye.sclera
                        sc.vascularity_intensity = e["veins"]
                        sc.vascularity_coverage = e["veins_cover"]
                        eye.sclera = sc
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
                    # Epic's lipstick is glossy and metallic by default (roughness
                    # 0.25, metalness 1.0): a 1990 plain lipstick is neither.
                    if "roughness" in m["lips"]:
                        lp.roughness = m["lips"]["roughness"]
                    if "metalness" in m["lips"]:
                        lp.metalness = m["lips"]["metalness"]
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
        # 60 s, 6 October: Tom's G takes were READY at 30 s and built with frosted brows and lashes
        # and a darker face, which a build before the service's textures had come would give.
        early = bool(brief(st["who"])) and now - st["asked"] < 60.0
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
    check("the slice's three and Tom", [w for w, _ in CAST] == ["rocco", "lena", "sam", "tom"])
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
    grooms = ["/Game/x/Grooms/MI_WI_Hair_S_BobLayered_Hair.x", "/Game/x/Grooms/MI_WI_Eyebrows_M_SlightArch_Hair.x"]
    use_take("S2")
    check("a take that names a brow colour recolours the eyebrows and nothing else",
          brow_materials("lena", grooms) == ["/Game/x/Grooms/MI_WI_Eyebrows_M_SlightArch_Hair.x"] and brow_materials("sam", grooms) == [])
    use_take("")
    check("everyone wears the plugin's own plain garment under what the clothing session makes",
          sorted(OUTFITS) == ["lena", "rocco", "sam"] and all(o == ("plain",) for o in OUTFITS.values()))
    check("only MetaHuman packages are imported", fab_packages(["oa_jeans.mhpkg", "notes.txt", "x.zip"]) == ["oa_jeans.mhpkg"])
    check("every outfit word names an imported wardrobe item", all(w in FAB_ITEMS for o in OUTFITS.values() for w in o))
    check("an outfit path is a loadable object path", outfit_paths("rocco")[0] == GARMENT)
    check("nothing from Fab is ever put on (NoAI, 3 October)",
          not [x for w in OUTFITS for x in outfit_paths(w) if x.startswith(NOAI_ROOTS)])
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
    # NOT MADE FROM THE EAST ASIAN PRESETS (Grace was Lena's first base, 24
    # September): none is a base, and since the 28 September push uses them
    # with negative weight to steer away, their weights together are zero or
    # less, so no candidate leans on them.
    east_asian = ("Aera", "Aoi", "Bo", "Grace", "Kelvin", "Lani", "Sook-ja", "Tuya")
    check("no candidate is made from Grace's face",
          all(c["base"] != "Grace" and ("Grace" not in c["face"] or sum(w for n, w in c["face"].items() if n in east_asian) <= 1e-9)
              for _, _, c in cands))
    regions = {"scalp", "forehead", "nose", "under_eye", "cheeks", "lips", "chin", "ears"}
    check("skin accents name real regions and fields, each 0 to 1",
          all(set(c.get("accents", {})) <= regions and all(set(v) <= {"redness", "saturation", "lightness"} and all(0 <= x <= 1 for x in v.values())
                                                          for v in c.get("accents", {}).values()) for _, _, c in cands))
    marks = [(0.0, 0.0, 0.0)] * 88
    marks[48], marks[32] = (-2.0, 0.0, 0.0), (2.0, 0.0, 0.0)
    d = sculpt_deltas(marks, [{"at": "mouth_corners", "move": [0.1, 0.0, 0.2], "width": 0.5}])
    check("a sculpt is mirrored left and right and its width scales from the middle",
          abs(d[48][0] - 0.9) < 1e-9 and abs(d[32][0] + 0.9) < 1e-9 and d[48][2] == d[32][2] == 0.2)
    check("every landmark named is one of the 88", all(0 <= i < 88 for v in MARK.values() for i in v))
    check("finishing a take keeps its face", FINISH["R1"]["lena"]["face"] == THIRD["Q1"]["lena"]["face"]
          and FINISH["R2"]["sam"]["face"] == THIRD["Q3"]["sam"]["face"] and FINISH["R1"]["lena"] is not THIRD["Q1"]["lena"])
    check("the candidates of one person all differ", all(len({repr(sorted(CANDIDATES[t][w]["face"].items())) + CANDIDATES[t][w]["hair"]
                                                            for t in FIVE}) == 5 for w in ("lena", "rocco", "sam")))
    check("heights are the sheets' (Sheila about 160, Ron about 186, Darren about 175)",
          all(abs(CANDIDATES[t][w]["body"]["Height"] - h) <= 3 for t in FIVE for w, h in (("lena", 160), ("rocco", 186), ("sam", 175))))
    check("Ron always has his moustache", all(CANDIDATES[t]["rocco"].get("mustache") for t in FIVE))
    toms = [t for t in CANDIDATES if "tom" in CANDIDATES[t]]
    check("Tom's candidates: only Tom in each, thirty (five, four, three from B2, two and two from D2, two from H2, two from I2, two from J2, two from K2, two from L1, four on L1's face), all different",
          len(toms) == 30 and all(list(CANDIDATES[t]) == ["tom"] for t in toms)
          and len({repr(sorted(CANDIDATES[t]["tom"]["face"].items())) + CANDIDATES[t]["tom"]["hair"]
                   + str(CANDIDATES[t]["tom"]["skin"].get("face_texture_index"))
                   + repr(sorted(CANDIDATES[t]["tom"].get("accents", {}))) + repr(sorted(CANDIDATES[t]["tom"].get("hair_colour", {})))
                   + repr(CANDIDATES[t]["tom"].get("sculpt")) + str(CANDIDATES[t]["tom"].get("eyebrows")) for t in toms}) == 30)
    check("Tom to his sheet: about 175 cm, lean, clean-shaven, short dark hair",
          all(abs(CANDIDATES[t]["tom"]["body"]["Height"] - 175) <= 3 and CANDIDATES[t]["tom"]["body"]["Fat"] <= 0
              and set(CANDIDATES[t]["tom"]["clear"]) == {"Beard", "Mustache"} and not CANDIDATES[t]["tom"].get("beard")
              and not CANDIDATES[t]["tom"].get("mustache") and CANDIDATES[t]["tom"]["hair"].startswith("WI_Hair_S_")
              and CANDIDATES[t]["tom"]["hair_colour"]["WhiteAmount"] == 0.0 for t in toms))
    check("the first try led from a preset none of the frozen faces leads from, at 80% or more",
          all(CANDIDATES[t]["tom"]["base"] not in ("Bruce", "Jelena", "Orlando")
              and max(CANDIDATES[t]["tom"]["face"].values()) >= 0.8 for t in toms if t.startswith("A")))
    check("the second try leaves Victor's and Lorenzo's skin sets and Victor's face, and never the aged 121 (Ron's and Sheila's)",
          all(CANDIDATES[t]["tom"]["skin"].get("face_texture_index") in (13, 85) and "Victor" not in CANDIDATES[t]["tom"]["face"]
              and CANDIDATES[t]["tom"]["eyes"] == EYES_GREY_BLUE and CANDIDATES[t]["tom"]["accents"]["chin"]["lightness"] > 0.5
              for t in toms if t[0] in "BDGHI"))
    check("a Tom take builds nobody else", [w for (w, _) in CAST if "A1" not in CANDIDATES or w in CANDIDATES["A1"]] == ["tom"])
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
