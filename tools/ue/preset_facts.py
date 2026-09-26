"""What Epic's MetaHuman presets are made of: eyes, skin, make-up, hair, and the choices the API offers.

    set LEDGER_MH_SCRIPT=preset_facts
    UnrealEditor.exe F:/LedgerTools/mh-dress/MHAssemble.uproject -unattended

WHY, 26 September. The faces read East Asian because of our choices on top of
sound builds (FINDINGS). To rebuild Sheila, Ron and Darren from northern
European presets with the sheets' eye colour and make-up, the numbers must
come from somewhere: the API's eye colour is a position on a chart and its
make-up types are names, so this reads what each shipped preset uses (the
presets whose own pictures show blue or grey eyes give the chart's blue and
grey), and lists every choice the enums offer. Writes preset-facts.json beside
the project. Reads only; changes nothing.
"""
import json
import os
import time

PRESET_DIR = "/MetaHumanCharacter/Optional/Presets/"
NAMES = ["Ada", "Aera", "Aoi", "Asha", "Bo", "Bruce", "Cameron", "Celeste", "Dominic", "Etta", "Grace", "Isaiah", "Jelena",
         "Jorge", "Kelvin", "Lani", "Lorenzo", "Mateo", "Mikel", "Omari", "Orlando", "Sook-ja", "Sunita", "Trey", "Tuya",
         "Victor", "Vivian", "Walter", "Zuri"]


def plain(v, depth=0):
    """A struct or value as plain data, as far as Python can see into it."""
    import unreal
    if depth > 4:
        return str(v)
    if isinstance(v, (int, float, str, bool)) or v is None:
        return v
    if isinstance(v, unreal.EnumBase):
        return str(v.name)
    if isinstance(v, unreal.LinearColor):
        return [round(v.r, 3), round(v.g, 3), round(v.b, 3)]
    if isinstance(v, unreal.StructBase):
        out = {}
        for name in dir(v):
            if name.startswith("_") or callable(getattr(v, name, None)):
                continue
            try:
                out[name] = plain(v.get_editor_property(name), depth + 1)
            except Exception:
                pass
        return out
    return str(v)


def enum_names(e):
    return [n for n in dir(e) if n.isupper()]


def main_after_idle(seconds=20.0):
    import unreal
    st = {"t0": time.time(), "h": None, "done": False}
    out = os.path.join(unreal.Paths.project_dir(), "preset-facts.json")

    def run():
        facts = {"enums": {}, "presets": {}}
        for e in ("MetaHumanCharacterEyeMakeupType", "MetaHumanCharacterLipsMakeupType", "MetaHumanCharacterBlushMakeupType",
                  "MetaHumanCharacterEyesIrisPattern"):
            facts["enums"][e] = enum_names(getattr(unreal, e))
        for n in NAMES:
            ch = unreal.load_asset(PRESET_DIR + n + "." + n)
            if ch is None:
                facts["presets"][n] = "missing"
                continue
            p = {}
            for prop in ("eyes_settings", "makeup_settings", "skin_settings"):
                try:
                    p[prop] = plain(ch.get_editor_property(prop))
                except Exception as ex:
                    p[prop] = "unreadable: %s" % ex
            facts["presets"][n] = p
        # the wardrobe's slot calls, to take a preset's own beard off
        ch = unreal.load_asset(PRESET_DIR + "Walter.Walter")
        col = ch.internal_collection
        inst = col.default_instance
        facts["api"] = {"collection": [m for m in dir(col) if "slot" in m.lower() or "item" in m.lower()],
                        "instance": [m for m in dir(inst) if "slot" in m.lower() or "select" in m.lower()]}
        try:
            facts["api"]["walterSelections"] = [str(x) for x in inst.get_editor_property("slot_selections")]
        except Exception as ex:
            facts["api"]["walterSelections"] = "unreadable: %s" % ex
        with open(out, "w", encoding="utf-8") as fh:
            json.dump(facts, fh, indent=1)

    def tick(delta):
        if st["done"] or time.time() - st["t0"] < seconds:
            return
        st["done"] = True
        unreal.unregister_slate_post_tick_callback(st["h"])
        try:
            run()
        except Exception as e:
            with open(out, "w", encoding="utf-8") as fh:
                json.dump({"raised": repr(e)}, fh)
        finally:
            unreal.SystemLibrary.quit_editor()

    st["h"] = unreal.register_slate_post_tick_callback(tick)
