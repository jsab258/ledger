"""Dress the test MetaHuman in plain clothes and a haircut, by script, then build it again.

    UnrealEditor.exe <scratch project>   with Content/Python/init_unreal.py calling main_after_idle()
    python tools/ue/dress_metahuman.py --selftest     # runs without Unreal

WHY, 24 September. Jafar's ruling: "Dress MH_Test by script, in plain 1990
clothes and a haircut. He is a test figure, not a character; proper period
clothing is the clothing line's job." MH_Test stood in Mickey's corner bald,
in the Creator's underwear.

WHAT THERE IS TO DRESS HIM IN. The MetaHuman plugin ships one garment,
WI_DefaultGarment (a top and trousers whose colours are parameters), and
some forty haircuts; anything else is a download from Fab. So: that garment
in muted colours a 1990 street would not look twice at, and a plain
short cut (Jafar calls him "he"), in the character's own collection, the way the
plugin's own example scripts do it. Then the same Optimized/High build as
assemble_metahuman.py, into the same folder, so the probe's copy step picks
it up unchanged, in a second editor run.

ONE LINE, appended to ue-material.txt in the project folder: what was added,
which colour parameters were found and set, and the build's own line after it.
"""
import os
import sys
import time

CHARACTER = "/Game/MH_Test"
GARMENT = "/MetaHumanCharacter/Optional/Clothing/WI_DefaultGarment.WI_DefaultGarment"
HAIR_DIR = "/MetaHumanCharacter/Optional/Grooms/Bindings/Hair/"
HAIRS = ["WI_Hair_S_Casual", "WI_Hair_S_Clean", "WI_Hair_S_SideSweptFringe"]

# Muted, in linear colour: a dull slate knit, dark brown-grey trousers,
# near-black shoes. Matched by words in the garment's parameter names,
# because the names are the garment's and are only known once it is assembled.
COLOURS = [
    (("shoe", "boot", "sneaker"), (0.018, 0.016, 0.015)),
    (("pant", "trouser", "jean", "bottom", "leg"), (0.040, 0.034, 0.028)),
    (("shirt", "top", "sweater", "jumper", "hoodie"), (0.070, 0.085, 0.105)),
]
MELANIN = 0.72


def colour_for(name):
    """The colour a garment parameter gets, or None if it is not a colour this sets."""
    n = name.lower()
    if "color" not in n and "colour" not in n:
        return None
    for words, rgb in COLOURS:
        if any(w in n for w in words):
            return rgb
    return None


def status_line(status, hair, found, set_, seconds, note):
    return ("metahumanDress=%s metahumanHair=%s metahumanGarmentParams=%s metahumanColoursSet=%s "
            "metahumanDressSeconds=%.0f metahumanDressNote=%s"
            % (status, hair, found or "none", set_ or "none", seconds, (note or "none").replace(" ", "~")[:200]))


def main_after_idle(seconds=20.0, wait_params=240.0, settle=15.0):
    """The full editor's way, as in assemble_metahuman.py, but in steps across
    ticks, because the preview assembly that makes the garment's colour
    parameters exist finishes on later ticks, not in the call (24 September:
    asked for in the same tick, every parameter read failed with "the
    Collection is not built"). Add the garment and the haircut, open the
    character for edit and start the preview; poll until the garment's
    parameters appear; set the colours; close, save, quit. The character is
    opened for edit first and the garment and haircut added a step later. The build is a
    separate editor run (assemble_metahuman.py), because the preview holds
    several GB and the build's own memory check then refuses."""
    import unreal
    st = {"t0": time.time(), "h": None, "step": 0, "last": 0.0}
    out = os.path.join(unreal.Paths.project_dir(), "ue-material.txt")

    def write(l):
        with open(out, "a", encoding="utf-8") as fh:
            fh.write(l + "\n")
        print("dress_metahuman: " + l)

    def finish():
        unreal.unregister_slate_post_tick_callback(st["h"])
        sub = st.get("sub")
        ch = st.get("ch")
        if sub is not None and ch is not None and sub.is_object_added_for_editing(ch):
            sub.remove_object_to_edit(ch)
        if ch is not None:
            unreal.EditorAssetLibrary.save_loaded_asset(ch, only_if_is_dirty=False)
        unreal.SystemLibrary.quit_editor()

    def start():
        ch = unreal.load_asset(CHARACTER)
        if ch is None:
            write(status_line("NO-CHARACTER", "none", "", "", time.time() - st["t0"], CHARACTER))
            return False
        st["ch"] = ch
        # OPENED FOR EDIT FIRST, BEFORE ANYTHING IS ADDED (24 September: with
        # the garment and haircut already in the collection, opening for edit
        # crashed twice in the plugin on a null, with and without a pause
        # between; opening the undressed character works, as last night's
        # build and this morning's check both show).
        sub = unreal.get_editor_subsystem(unreal.MetaHumanCharacterEditorSubsystem)
        if not sub.try_add_object_to_edit(ch):
            write(status_line("NOT-EDITABLE", "none", "", "", time.time() - st["t0"], "try_add_object_to_edit refused"))
            return False
        st["sub"] = sub
        st["opened"] = time.time()
        return True

    def add_items():
        ch = st["ch"]
        col = ch.internal_collection
        inst = col.default_instance
        garment = unreal.load_asset(GARMENT)
        if garment is None:
            write(status_line("NO-GARMENT", "none", "", "", time.time() - st["t0"], GARMENT))
            return False
        st["outfit"] = col.try_add_item_from_wardrobe_item("Outfits", garment)
        inst.try_add_slot_selection(unreal.MetaHumanPipelineSlotSelection(slot_name="Outfits", selected_item=st["outfit"]))
        st["hair_name"], st["hair"] = "none", None
        for h in HAIRS:
            a = unreal.load_asset(HAIR_DIR + h + "." + h)
            if a is not None:
                st["hair"] = col.try_add_item_from_wardrobe_item("Hair", a)
                inst.try_add_slot_selection(unreal.MetaHumanPipelineSlotSelection(slot_name="Hair", selected_item=st["hair"]))
                st["hair_name"] = h
                break
        st["sub"].assemble_for_preview(character=ch)
        st["asked"] = time.time()
        return True

    def try_colour():
        inst = st["ch"].internal_collection.default_instance
        params = inst.get_instance_parameters(item_path=unreal.MetaHumanPaletteItemPath(item_key=st["outfit"]))
        if not params:
            return False
        found, done = [], []
        for p in params:
            found.append(str(p.name))
            rgb = colour_for(str(p.name))
            if rgb is not None:
                p.set_color(value=unreal.LinearColor(rgb[0], rgb[1], rgb[2], 1.0))
                done.append(str(p.name))
        if st["hair"] is not None:
            for p in inst.get_instance_parameters(item_path=unreal.MetaHumanPaletteItemPath(item_key=st["hair"])) or []:
                if str(p.name) == "Melanin":
                    p.set_float(value=MELANIN)
                    done.append("Melanin")
        write(status_line("DRESSED", st["hair_name"], ",".join(found), ",".join(done),
                          time.time() - st["t0"], "default-garment;params-after-%.0fs" % (time.time() - st["asked"])))
        return True

    def tick(delta):
        # NEVER RE-ENTERED (24 September): opening for edit waits on the face
        # mesh and ticks the editor while it waits, which called this again
        # mid-step; the second open started a second face import inside the
        # first and the plugin crashed on a null, three runs in four. The
        # runs that worked had unregistered before their one call.
        if st.get("busy"):
            return
        st["busy"] = True
        try:
            step(delta)
        finally:
            st["busy"] = False

    def step(delta):
        now = time.time()
        try:
            if st["step"] == 0:
                if now - st["t0"] < seconds:
                    return
                st["step"] = 1 if start() else 9
            elif st["step"] == 1:
                if now - st["opened"] < settle:
                    return
                st["step"] = 2 if add_items() else 9
            elif st["step"] == 2:
                if now - st["last"] < 2.0:
                    return
                st["last"] = now
                if try_colour():
                    st["step"] = 9
                elif now - st["asked"] > wait_params:
                    write(status_line("DRESSED-UNCOLOURED", st["hair_name"], "", "", now - st["t0"],
                                      "garment-parameters-never-appeared-in-%.0fs" % wait_params))
                    st["step"] = 9
            if st["step"] == 9:
                finish()
        except Exception as e:
            write(status_line("RAISED", st.get("hair_name", "none"), "", "", now - st["t0"], repr(e)))
            finish()

    st["h"] = unreal.register_slate_post_tick_callback(tick)


def selftest():
    ok = bad = 0

    def check(name, cond):
        nonlocal ok, bad
        if cond:
            ok += 1
        else:
            bad += 1
            print("dress_metahuman selftest FAIL " + name)
    check("the shirt colour is the shirt's", colour_for("PrimaryColorShirt") == COLOURS[2][1])
    check("trousers are not the shirt", colour_for("PrimaryColorPants") == COLOURS[1][1])
    check("a shoe is a shoe", colour_for("ShoeColor") == COLOURS[0][1])
    check("a non-colour parameter is left alone", colour_for("ShirtRoughness") is None)
    check("the first haircut is a plain short one", HAIRS[0] == "WI_Hair_S_Casual")
    check("the line names its status", "metahumanDress=DRESSED" in status_line("DRESSED", "h", "a", "b", 1.0, "x"))
    print("dress_metahuman selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    print("dress_metahuman runs inside the editor; see the header")
