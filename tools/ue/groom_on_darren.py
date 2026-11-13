"""Loomwright hair round 2 (advisor 119/120): its strands on Darren in the editor, beside his current hair. Scratch only.

    set LEDGER_MH_SCRIPT=groom_on_darren
    set LEDGER_GROOM_ABC=F:/.../hair_strands.abc   (Loomwright's output, its own frame: metres, Y up, face +Z)
    set LEDGER_GROOM_OUT=F:/LedgerTools/tool-tests-2026-11/loomwright-r2/ue
    set LEDGER_GROOM_OFFSET=0,1.52,16.89            (cm, from darren_scalp.py's scalp.json: the skull centre)
    UnrealEditor.exe C:/LedgerTools/mh-assemble/MHAssemble.uproject -unattended -EnablePlugins=AlembicHairImporter
    (the Alembic hair translator is its own plugin, off in this project; the flag loads it for this run only)

WHY, 13 November 2026. Round 1 (production/research/tool-tests-2026-11/LOOMWRIGHT-HAIR-ROUND1-2026-11-12.md) grew hair on
the tool's own proxy head; round 2 grows it on Darren's scalp (darren_scalp.py) and must judge it on him. The strands are
imported with the groom importer's Maya conversion (rotation 90,0,0; scale 1,-1,1; the tool's frame is Maya's, in metres,
so times 100) into /Game/Scratch/LoomwrightR2, then two of his MetaHumans stand 60 cm apart in the unsaved level: A with
his current hair, B with the tool's strands in place of it (his own hair material on them, so only the strands differ).
The offset moves the tool's skull centre (0, 1.62 m, 0) to his. Checks written to groom_on_darren.json: curves, the hair's
top against his crown (B's hair bounds against his face mesh), and pictures at talk distance (1.2 m) from the front and
from behind at four exposures each. Nothing is saved; the scratch folder is deleted at the end.
"""
import json
import os
import time

DEST = "/Game/Scratch/LoomwrightR2"
BP = "/Game/Ledger/MetaHumans/MH_SamS6/BP_MH_SamS6"
HAIR_MI = "/Game/Ledger/MetaHumans/MH_SamS6/Grooms/MI_WI_Hair_S_Casual_Hair"


def main_after_idle(seconds=20.0):
    import unreal
    ABC = os.environ.get("LEDGER_GROOM_ABC", "")
    OUT = os.environ.get("LEDGER_GROOM_OUT", "")
    OFF = [float(x) for x in os.environ.get("LEDGER_GROOM_OFFSET", "0,0,0").split(",")]
    os.makedirs(OUT, exist_ok=True)
    res = {"abc": ABC, "offset_cm": OFF, "stages": []}
    st = {"t0": time.time(), "h": None, "phase": 0, "t1": 0.0, "actors": [], "lights": []}

    def save():
        with open(os.path.join(OUT, "groom_on_darren.json"), "w") as fh:
            json.dump(res, fh, indent=1)

    def note(stage, **kw):
        kw["stage"] = stage
        res["stages"].append({k: (v if isinstance(v, (int, float, str, bool, list, dict, type(None))) else str(v)) for k, v in kw.items()})
        save()

    def vec(v):
        return [round(v.x, 2), round(v.y, 2), round(v.z, 2)]

    def import_groom():
        opts = unreal.GroomImportOptions()
        conv = opts.get_editor_property("conversion_settings")
        conv.set_editor_property("rotation", unreal.Vector(90.0, 0.0, 0.0))
        conv.set_editor_property("scale", unreal.Vector(100.0, -100.0, 100.0))
        opts.set_editor_property("conversion_settings", conv)
        t = unreal.AssetImportTask()
        t.set_editor_property("filename", ABC)
        t.set_editor_property("destination_path", DEST)
        t.set_editor_property("destination_name", "Groom_Loomwright")
        t.set_editor_property("automated", True)
        t.set_editor_property("replace_existing", True)
        t.set_editor_property("save", False)
        t.set_editor_property("options", opts)
        # the static-mesh Alembic importer takes the file unless the groom importer is named (13 Nov, first run)
        t.set_editor_property("factory", unreal.HairStrandsFactory())
        unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([t])
        paths = list(t.get_editor_property("imported_object_paths"))
        g = next((unreal.load_asset(p) for p in paths if isinstance(unreal.load_asset(p), unreal.GroomAsset)), None)
        info = None
        if g is not None:
            try:
                info = [{"curves": x.get_editor_property("num_curves"), "points": x.get_editor_property("num_curve_vertices")}
                        for x in g.get_editor_property("hair_groups_info")]
            except Exception as e:
                info = str(e)
        note("import", ok=g is not None, paths=paths, groups=info)
        return g

    def hair_component(actor):
        for c in actor.get_components_by_class(unreal.GroomComponent):
            ga = c.get_editor_property("groom_asset")
            if ga and ga.get_name().startswith("Hair_"):
                return c
        return None

    def face_component(actor):
        for c in actor.get_components_by_class(unreal.SkeletalMeshComponent):
            if c.get_name().lower() == "face":
                return c
        return None

    def setup(groom):
        cls = unreal.EditorAssetLibrary.load_blueprint_class(BP)
        a = unreal.EditorLevelLibrary.spawn_actor_from_class(cls, unreal.Vector(0, 0, 0), unreal.Rotator(0, 0, 0))
        b = unreal.EditorLevelLibrary.spawn_actor_from_class(cls, unreal.Vector(60, 0, 0), unreal.Rotator(0, 0, 0))
        st["actors"] = [a, b]
        hb = hair_component(b)
        face = face_component(b)
        note("actors", a=a.get_name(), b=b.get_name(), hair_found=hb is not None, face_found=face is not None,
             hair_asset=hb.get_editor_property("groom_asset").get_name() if hb else None)
        if hb is not None and groom is not None:
            try:
                hb.set_editor_property("binding_asset", None)
            except Exception as e:
                note("binding", error=str(e))
            hb.set_groom_asset(groom) if hasattr(hb, "set_groom_asset") else hb.set_editor_property("groom_asset", groom)
            hb.set_relative_location(unreal.Vector(*OFF), False, False)
            mi = unreal.load_asset(HAIR_MI)
            if mi is not None:
                hb.set_material(0, mi)
        # light: a key from front-left above, a fill, a rim from behind
        for loc, rot, inten in (((300, 250, 260), (-30, -140, 0), 8.0), ((-250, 250, 200), (-15, -50, 0), 3.0), ((50, -300, 250), (-25, 80, 0), 5.0)):
            l = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.DirectionalLight, unreal.Vector(*loc), unreal.Rotator(*rot))
            l.get_component_by_class(unreal.DirectionalLightComponent).set_intensity(inten)
            st["lights"].append(l)

    def measure():
        a, b = st["actors"]
        face = face_component(b)
        hb = hair_component(b) or next(iter(b.get_components_by_class(unreal.GroomComponent)), None)
        out = {}
        if face is not None:
            fo, fe, _r = unreal.SystemLibrary.get_component_bounds(face)
            out["face_top_z"] = round(fo.z + fe.z, 2)
            out["face_bounds"] = [vec(fo - fe), vec(fo + fe)]
        for c in b.get_components_by_class(unreal.GroomComponent):
            bo_o, bo_e, _r = unreal.SystemLibrary.get_component_bounds(c)
            out.setdefault("b_grooms", []).append({"name": c.get_name(), "asset": c.get_editor_property("groom_asset").get_name() if c.get_editor_property("groom_asset") else None,
                                                   "min": vec(bo_o - bo_e), "max": vec(bo_o + bo_e)})
        ha = hair_component(a)
        if ha is not None:
            bo_o, bo_e, _r = unreal.SystemLibrary.get_component_bounds(ha)
            out["a_hair"] = {"min": vec(bo_o - bo_e), "max": vec(bo_o + bo_e)}
        note("measure", **out)
        return out

    def capture(face_z):
        rt = unreal.RenderingLibrary.create_render_target2d(unreal.EditorLevelLibrary.get_editor_world(), 1600, 1000,
                                                            unreal.TextureRenderTargetFormat.RTF_RGBA8)
        cap = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.SceneCapture2D, unreal.Vector(0, 0, 0))
        cc = cap.get_component_by_class(unreal.SceneCaptureComponent2D)
        cc.set_editor_property("texture_target", rt)
        cc.set_editor_property("capture_source", unreal.SceneCaptureSource.SCS_FINAL_COLOR_LDR)
        cc.set_editor_property("fov_angle", 45.0)
        z = face_z - 12.0
        shots = {"front": (unreal.Vector(30, 120, z), unreal.Rotator(0, -90, 0)),
                 "behind": (unreal.Vector(30, -120, z), unreal.Rotator(0, 90, 0))}
        files = []
        for name, (loc, rot) in shots.items():
            cap.set_actor_location_and_rotation(loc, rot, False, False)
            for bias in (-1.0, 0.5, 2.0, 3.5):
                pp = cc.get_editor_property("post_process_settings")
                pp.set_editor_property("override_auto_exposure_method", True)
                pp.set_editor_property("auto_exposure_method", unreal.AutoExposureMethod.AEM_MANUAL)
                pp.set_editor_property("override_auto_exposure_bias", True)
                pp.set_editor_property("auto_exposure_bias", bias)
                pp.set_editor_property("override_auto_exposure_apply_physical_camera_exposure", True)
                pp.set_editor_property("auto_exposure_apply_physical_camera_exposure", False)
                cc.set_editor_property("post_process_settings", pp)
                cc.capture_scene()
                fn = "darren_%s_ev%+.1f.png" % (name, bias)
                unreal.RenderingLibrary.export_render_target(unreal.EditorLevelLibrary.get_editor_world(), rt, OUT, fn)
                files.append(fn)
        note("pictures", files=files, note="A (his current hair) on the left of the front view at x 0; B (the tool's strands) at x 60")
        unreal.EditorLevelLibrary.destroy_actor(cap)

    def tick(delta):
        now = time.time()
        try:
            if st.get("busy"):
                return
            if st["phase"] == 0 and now - st["t0"] > seconds:
                # an import pumps editor ticks, so this callback re-enters during it (13 Nov, second run): hold it off
                st["busy"] = True
                st["phase"] = 1
                g = import_groom()
                setup(g)
                st["t1"] = time.time()
                st["busy"] = False
            elif st["phase"] == 1 and now - st["t1"] > 25.0:
                st["phase"] = 2
                m = measure()
                capture(m.get("face_top_z", 190.0) - 2.0)
                st["t1"] = now
            elif st["phase"] == 2 and now - st["t1"] > 3.0:
                st["phase"] = 3
                for x in st["actors"] + st["lights"]:
                    unreal.EditorLevelLibrary.destroy_actor(x)
                unreal.EditorAssetLibrary.delete_directory(DEST)
                note("cleanup", scratch_gone=not unreal.EditorAssetLibrary.does_directory_exist(DEST))
                unreal.unregister_slate_post_tick_callback(st["h"])
                unreal.SystemLibrary.quit_editor()
        except Exception as e:
            import traceback
            note("RAISED", error=repr(e), phase=st["phase"], trace=traceback.format_exc())
            st["phase"] = 3
            unreal.unregister_slate_post_tick_callback(st["h"])
            unreal.SystemLibrary.quit_editor()

    st["h"] = unreal.register_slate_post_tick_callback(tick)
