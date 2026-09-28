"""What Python can see and set on Epic's cloth and outfit graph templates, on this PC.

    set LEDGER_MH_SCRIPT=cloth_graph_probe
    UnrealEditor.exe F:/LedgerTools/mh-dress/MHAssemble.uproject -unattended

WHY, 28 September (Jafar's list, item 5; production/research/character-
pipeline/cloth-graph-python-2026-09-28.md). The installed engine exposes
DataflowEditorBlueprintLibrary (add, connect and set a node's property from
a string; paste a graph from text), and ships DF_StaticMeshClothTemplate,
MakeResizableOutfitTemplate and ResizeOutfitTemplate. The 24 September try
found "the graph's inputs protected from Python" without naming the call.
This reads only: for each template it writes what the asset exposes (its
Python-visible properties and methods), what copying it to text gives (the
node names and their properties, which SetDataflowNodeProperty takes), and
what DataflowEditorBlueprintLibrary offers, to cloth-graph-probe.txt beside
the project. Nothing is saved.
"""
import os
import time

TEMPLATES = [
    "/ChaosClothAsset/DF_StaticMeshClothTemplate.DF_StaticMeshClothTemplate",
    "/ChaosClothAsset/ClothAssetTemplate.ClothAssetTemplate",
    "/ChaosOutfitAsset/MakeResizableOutfitTemplate.MakeResizableOutfitTemplate",
    "/ChaosOutfitAsset/ResizeOutfitTemplate.ResizeOutfitTemplate",
]


def main_after_idle(seconds=20.0):
    import unreal
    st = {"t0": time.time(), "h": None, "done": False}
    out = os.path.join(unreal.Paths.project_dir(), "cloth-graph-probe.txt")

    def run():
        lines = []
        lib = getattr(unreal, "DataflowEditorBlueprintLibrary", None)
        lines.append("DataflowEditorBlueprintLibrary: %s" % ([n for n in dir(lib) if not n.startswith("_")] if lib else "NOT EXPOSED"))
        for path in TEMPLATES:
            a = unreal.load_asset(path)
            lines.append("== %s: %s" % (path, type(a).__name__ if a else "NOT FOUND"))
            if a is None:
                continue
            lines.append("  members: %s" % [n for n in dir(a) if not n.startswith("_")][:120])
            # Copy to text: the node names and properties in the asset's own export.
            try:
                txt = unreal.EditorAssetLibrary.get_metadata_tag_values(a)
                lines.append("  metadata: %s" % txt)
            except Exception as e:
                lines.append("  metadata: %r" % (e,))
            for prop in ("dataflow_asset", "dataflow_terminal", "dataflow", "graph", "variables", "dataflow_instance"):
                try:
                    lines.append("  %s = %r" % (prop, a.get_editor_property(prop)))
                except Exception as e:
                    lines.append("  %s: %s" % (prop, type(e).__name__))
        with open(out, "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines) + "\n")

    def tick(delta):
        if st["done"] or time.time() - st["t0"] < seconds:
            return
        st["done"] = True
        unreal.unregister_slate_post_tick_callback(st["h"])
        try:
            run()
        except Exception as e:
            with open(out, "a", encoding="utf-8") as fh:
                fh.write("raised %r\n" % (e,))
        finally:
            unreal.SystemLibrary.quit_editor()

    st["h"] = unreal.register_slate_post_tick_callback(tick)
