"""List the Fab clothing packages' files that built cast MetaHumans actually depend on.

    set LEDGER_MH_SCRIPT=fab_closure
    set LEDGER_MH_TAKE=T2
    UnrealEditor.exe <the dressing project>

WHY, 24 September (overnight). A MetaHuman built in Epic's clothes keeps
references to the clothing packages' parent materials and their textures, so
the game needs those files beside the cast. The seven packages are 4.5 GB and
drive C: has less than twice that free; only the part the cast uses is copied.
Writes fab-closure.txt to the project folder: one /Game/Fab package path per
line, every package under /Game/Fab reachable from the takes' built folders.
"""
import os
import time

BUILD_ROOT = "/Game/Ledger/MetaHumans/"
WHO = ("Lena", "Rocco", "Sam")


def main_after_idle(seconds=20.0):
    import unreal
    st = {"t0": time.time(), "h": None, "done": False}
    out = os.path.join(unreal.Paths.project_dir(), "fab-closure.txt")
    take = os.environ.get("LEDGER_MH_TAKE", "T2")

    def run():
        reg = unreal.AssetRegistryHelpers.get_asset_registry()
        opts = unreal.AssetRegistryDependencyOptions(include_soft_package_references=True, include_hard_package_references=True,
                                                     include_searchable_names=False, include_soft_management_references=False,
                                                     include_hard_management_references=False)
        seen, todo = set(), []
        for w in WHO:
            for p in unreal.EditorAssetLibrary.list_assets(BUILD_ROOT + "MH_" + w + take, recursive=True, include_folder=False):
                todo.append(p.split(".")[0])
        while todo:
            pkg = todo.pop()
            deps = reg.get_dependencies(pkg, opts) or []
            for d in deps:
                d = str(d)
                if d.startswith("/Game/Fab/") and d not in seen:
                    seen.add(d)
                    todo.append(d)
        with open(out, "w", encoding="utf-8") as fh:
            fh.write("\n".join(sorted(seen)) + "\n")

    def tick(delta):
        if st["done"] or time.time() - st["t0"] < seconds:
            return
        st["done"] = True
        unreal.unregister_slate_post_tick_callback(st["h"])
        try:
            run()
        except Exception as e:
            with open(out, "w", encoding="utf-8") as fh:
                fh.write("RAISED %r\n" % e)
        finally:
            unreal.SystemLibrary.quit_editor()

    st["h"] = unreal.register_slate_post_tick_callback(tick)
