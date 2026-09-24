"""Import Epic's free MetaHuman clothing packages (.mhpkg from Fab) and list what they hold.

    set LEDGER_MH_SCRIPT=import_fab_clothes
    set LEDGER_FAB_DIR=F:\\LedgerTools\\fab
    UnrealEditor.exe <a MetaHuman scratch project>

WHY, 24 September (overnight). Jafar: "dress the current cast plainly with
Epic's free clothing so nobody is barefoot." Epic's garments come from Fab as
MetaHuman packages; the MetaHuman SDK registers a factory for .mhpkg
(MetaHumanPackageFactory), so an ordinary automated import task brings each in.
This imports every package in LEDGER_FAB_DIR under /Game/Fab/<name> and writes
fab-clothes.json to the project folder: per package, every asset it made with
its class, so the dressing step can find the wardrobe items by what they are.
"""
import json
import os
import time


def main_after_idle(seconds=20.0):
    import unreal
    st = {"t0": time.time(), "h": None, "done": False}
    out = os.path.join(unreal.Paths.project_dir(), "fab-clothes.json")
    src = os.environ.get("LEDGER_FAB_DIR", r"F:\LedgerTools\fab")

    def run():
        tools = unreal.AssetToolsHelpers.get_asset_tools()
        lib = unreal.EditorAssetLibrary
        # ONE PACKAGE A RUN when LEDGER_FAB_ONLY names it: importing all seven
        # in one editor ran this PC out of memory (24 September, overnight:
        # "the paging file is too small"), with C: too full for Windows to
        # grow its swap file. The report is merged into the existing one.
        only = os.environ.get("LEDGER_FAB_ONLY", "").strip()
        report = {"from": src, "packages": {}}
        if only and os.path.exists(out):
            try:
                with open(out, encoding="utf-8") as fh:
                    report = json.load(fh)
            except (OSError, ValueError):
                pass
        for f in sorted(os.listdir(src)):
            if not f.lower().endswith(".mhpkg"):
                continue
            if only and os.path.splitext(f)[0] != only:
                continue
            stem = os.path.splitext(f)[0]
            dest = "/Game/Fab/" + stem
            t = unreal.AssetImportTask()
            t.set_editor_property("filename", os.path.join(src, f))
            t.set_editor_property("destination_path", dest)
            t.set_editor_property("automated", True)
            t.set_editor_property("replace_existing", True)
            t.set_editor_property("save", True)
            t0 = time.time()
            try:
                tools.import_asset_tasks([t])
                made = list(t.get_editor_property("imported_object_paths") or [])
            except Exception as e:
                made = []
                report["packages"][stem] = {"error": repr(e)}
                continue
            # WHAT IS THERE AFTERWARDS, WHEREVER IT LANDED: the package may
            # keep its own folder layout rather than the destination asked.
            listed = []
            for root in {dest, "/Game"}:
                for p in lib.list_assets(root, recursive=True, include_folder=False):
                    if stem.split("_", 1)[-1].lower() in p.lower() or p.startswith(dest):
                        listed.append(p)
            classes = {}
            for p in sorted(set(listed + [str(m) for m in made])):
                a = lib.find_asset_data(p)
                classes[p] = str(a.asset_class_path.asset_name) if a and a.is_valid() else "?"
            report["packages"][stem] = {"seconds": round(time.time() - t0, 1), "imported": [str(m) for m in made],
                                        "assets": classes}
        with open(out, "w", encoding="utf-8") as fh:
            json.dump(report, fh, indent=1)

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
