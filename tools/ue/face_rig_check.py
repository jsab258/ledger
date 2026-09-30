"""Whether each cast face runs Epic's face rig, in the MetaHuman project.

    set LEDGER_MH_SCRIPT=face_rig_check
    UnrealEditor.exe C:/LedgerTools/mh-assemble/MHAssemble.uproject -unattended

WHY, 30 September. The mouths now move with the voice through the face
rig's own controls (PersonAnim.h SpeakTick), read by the face mesh's
post-process animation, which runs the rig (RigLogic). Sheila's and Ron's
mouths move; Darren's (MH_SamC5) stays frozen at every level, and his
blinks do not show either. This writes, for each approved face: its
skeleton, its post-process animation, and its DNA asset, so the one that
differs shows. face-rig-check.txt beside the project.
"""
import os
import time

FACES = {"Sheila": "MH_LenaS4", "Ron": "MH_RoccoP2", "Darren": "MH_SamC5"}


def main_after_idle(seconds=20.0):
    import unreal
    st = {"t0": time.time(), "h": None, "done": False}
    out = os.path.join(unreal.Paths.project_dir(), "face-rig-check.txt")

    def run():
        lines = []
        for who, mh in FACES.items():
            path = "/Game/Ledger/MetaHumans/%s/Face/SKM_%s_FaceMesh" % (mh, mh)
            mesh = unreal.load_asset(path)
            if mesh is None:
                lines.append("%s: MISSING %s" % (who, path))
                continue
            skel = mesh.get_editor_property("skeleton")
            pp = mesh.get_editor_property("post_process_anim_blueprint")
            lines.append("%s (%s): skeleton %s; post-process %s" % (
                who, mh, skel.get_path_name() if skel else "none", pp.get_path_name() if pp else "NONE"))
            for prop in ("lod_settings", "physics_asset"):
                try:
                    v = mesh.get_editor_property(prop)
                    lines.append("  %s: %s" % (prop, v.get_path_name() if v else "none"))
                except Exception as e:
                    lines.append("  %s: %r" % (prop, e))
            try:
                data = unreal.EditorAssetLibrary.find_package_referencers_for_asset(path, False)
                lines.append("  used by: %s" % ", ".join(sorted(str(d) for d in data)[:6]))
            except Exception as e:
                lines.append("  used by: %r" % e)
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
                fh.write("RAISED %r\n" % e)
        finally:
            unreal.SystemLibrary.quit_editor()

    st["h"] = unreal.register_slate_post_tick_callback(tick)
