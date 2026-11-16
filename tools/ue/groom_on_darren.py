"""Loomwright hair round 2 (advisor 119/120): its strands on Darren in the editor, beside his current hair. Scratch only.

    set LEDGER_MH_SCRIPT=groom_on_darren
    set LEDGER_GROOM_ABC=F:/.../hair_strands.abc   (Loomwright's output, its own frame: metres, Y up, face +Z)
    set LEDGER_GROOM_OUT=F:/LedgerTools/tool-tests-2026-11/loomwright-r2/ue
    set LEDGER_GROOM_OFFSET=0,1.52,16.89            (cm, from darren_scalp.py's scalp.json: the skull centre)
    set LEDGER_GROOM_DIAG=1                         (17 Nov diagnosis: B's face, body and grooms hidden, groom detached, one
                                                     side camera, pictures over 60 ticks plus one at r.HairStrands.ViewMode 36)
    UnrealEditor.exe C:/LedgerTools/mh-assemble/MHAssemble.uproject -unattended -EnablePlugins=AlembicHairImporter
    (the Alembic hair translator is its own plugin, off in this project; the flag loads it for this run only)

WHY, 13 November 2026. Round 1 (production/research/tool-tests-2026-11/LOOMWRIGHT-HAIR-ROUND1-2026-11-12.md) grew hair on
the tool's own proxy head; round 2 grows it on Darren's scalp (darren_scalp.py) and must judge it on him. The strands are
imported with the groom importer's Maya conversion (rotation 90,0,0; scale 1,-1,1; run 5 showed
times 100 is wrong) into /Game/Scratch/LoomwrightR2, then two of his MetaHumans stand 60 cm apart in the unsaved level: A with
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
    DIAG = os.environ.get("LEDGER_GROOM_DIAG", "") == "1"
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
        # run 5 (13 Nov): times 100 made the strands 25 m wide; the groom importer already brings this file in at
        # head size, so only the Maya mirror is kept (scale 1, -1, 1)
        conv.set_editor_property("scale", unreal.Vector(1.0, -1.0, 1.0))
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
        # run 8 (13 Nov): the tool's strands sit 1 to 2.6 cm off his skin in its own file and land in the same place here,
        # yet draw almost nothing: the likely cause is the strand width (0.07 mm in metres, not scaled with the points).
        # Read the width the import kept; with LEDGER_GROOM_WIDTH_CM set, override it (MetaHuman hair is about 0.007 cm).
        if g is not None:
            try:
                rs = list(g.get_editor_property("hair_groups_rendering"))
                before = []
                want = os.environ.get("LEDGER_GROOM_WIDTH_CM", "")
                for r in rs:
                    gs = r.get_editor_property("geometry_settings")
                    before.append({"width": gs.get_editor_property("hair_width"),
                                   "override": gs.get_editor_property("hair_width_override")})
                    if want:
                        gs.set_editor_property("hair_width", float(want))
                        gs.set_editor_property("hair_width_override", True)
                        r.set_editor_property("geometry_settings", gs)
                if want:
                    g.set_editor_property("hair_groups_rendering", rs)
                after = [r.get_editor_property("geometry_settings").get_editor_property("hair_width")
                         for r in g.get_editor_property("hair_groups_rendering")]
                note("width", before=before, set_cm=want or None, after=after)
            except Exception as e:
                note("width", error=str(e))
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
            # run 4 (13 Nov): swapping the groom on B's own Hair component did nothing visible, the blueprint's
            # construction puts his own groom back. So his Hair is hidden and the tool's strands come in their own
            # GroomActor, attached rigidly to his face at the skull-centre offset (a still picture needs no binding).
            hb.set_visibility(False, False)
            ga = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.GroomActor, b.get_actor_location(), unreal.Rotator(0, 0, 0))
            gc = ga.get_component_by_class(unreal.GroomComponent)
            gc.set_groom_asset(groom) if hasattr(gc, "set_groom_asset") else gc.set_editor_property("groom_asset", groom)
            ga.attach_to_component(face, "", unreal.AttachmentRule.SNAP_TO_TARGET, unreal.AttachmentRule.SNAP_TO_TARGET,
                                   unreal.AttachmentRule.KEEP_WORLD, False)
            gc.set_relative_location(unreal.Vector(*OFF), False, False)
            # run 10 (13 Nov): the engine source (GroomComponent.cpp 2179-2234, 2825-2847) treats a groom whose parent is a
            # skeletal mesh differently (bounds from the mesh, binding and deformation paths); LEDGER_GROOM_DETACH=1 keeps
            # the place it reached and detaches it, so the groom draws as a plain actor with no skeletal parent
            if os.environ.get("LEDGER_GROOM_DETACH", "") == "1" or DIAG:
                ga.detach_from_actor(unreal.DetachmentRule.KEEP_WORLD, unreal.DetachmentRule.KEEP_WORLD,
                                     unreal.DetachmentRule.KEEP_WORLD)
                note("detach", parent=str(gc.get_attach_parent()), at=vec(gc.get_world_location()),
                     rot=str(gc.get_world_rotation()), scale=vec(gc.get_world_scale()))
            # run 9 (13 Nov): his MetaHuman hair material may colour each strand from attributes the tool's file
            # lacks (root UV, groom textures); LEDGER_GROOM_MI=none keeps Epic's default strands material instead
            mi = None if os.environ.get("LEDGER_GROOM_MI", "") == "none" else unreal.load_asset(HAIR_MI)
            note("material", override=mi.get_name() if mi is not None else "default strands material")
            if mi is not None:
                gc.set_material(0, mi)
            st["actors_extra"] = [ga]
            if DIAG and os.environ.get("LEDGER_GROOM_DIAG_HIDE", "1") != "0":
                # 17 Nov diagnosis (CAPTURE-DIAGNOSIS-2026-11-17.md): hair buried in the head can never show from behind,
                # so B's face, body and own grooms are hidden and only the tool's (detached) strands remain to be seen
                hidden = []
                for c in b.get_components_by_class(unreal.PrimitiveComponent):
                    c.set_visibility(False, False)
                    hidden.append(c.get_name())
                note("diag_hidden", components=hidden)
            note("swap", groom_actor=ga.get_name(), attached_to=face.get_name(), b_hair_hidden=not hb.is_visible())
        # light: a key from front-left above, a fill, a rim from behind
        for loc, rot, inten in (((300, 250, 260), (-30, -140, 0), 8.0), ((-250, 250, 200), (-15, -50, 0), 3.0), ((50, -300, 250), (-25, 80, 0), 5.0)):
            l = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.DirectionalLight, unreal.Vector(*loc), unreal.Rotator(roll=0.0, pitch=float(rot[0]), yaw=float(rot[1])))
            lc = l.get_component_by_class(unreal.DirectionalLightComponent)
            # run 5 (13 Nov): in the new empty level every picture was black even at +3.5 EV: spawned lights are
            # stationary and a new level has no built lighting, so they are made movable and a sky light added
            lc.set_mobility(unreal.ComponentMobility.MOVABLE)
            lc.set_intensity(inten)
            st["lights"].append(l)
        try:
            sky = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.SkyLight, unreal.Vector(0, 0, 400))
            sc = sky.get_component_by_class(unreal.SkyLightComponent)
            sc.set_mobility(unreal.ComponentMobility.MOVABLE)
            sc.set_editor_property("source_type", unreal.SkyLightSourceType.SLS_SPECIFIED_CUBEMAP)
            cube = unreal.load_asset("/Engine/MapTemplates/Sky/DaylightAmbientCubemap")
            if cube is not None:
                sc.set_editor_property("cubemap", cube)
            sc.set_intensity(1.0)
            sc.recapture_sky()
            st["lights"].append(sky)
            note("skylight", cubemap=cube is not None)
        except Exception as e:
            note("skylight", error=str(e))

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
        for x in st.get("actors_extra", []):
            c = x.get_component_by_class(unreal.GroomComponent)
            bo_o, bo_e, _r = unreal.SystemLibrary.get_component_bounds(c)
            out["tool_hair"] = {"min": vec(bo_o - bo_e), "max": vec(bo_o + bo_e)}
            if face is not None:
                out["tool_hair_top_minus_face_top_cm"] = round(bo_o.z + bo_e.z - out["face_top_z"], 2)
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
        # run 6 (13 Nov): unreal.Rotator's positional order is roll, pitch, yaw, so (0, -90, 0) looked straight down
        # (run 4's "walls" were the floor tiles) and (0, 90, 0) straight up at the sky: angles by keyword only
        shots = {"front": (unreal.Vector(30, 120, z), unreal.Rotator(roll=0.0, pitch=0.0, yaw=-90.0)),
                 "behind": (unreal.Vector(30, -120, z), unreal.Rotator(roll=0.0, pitch=0.0, yaw=90.0))}
        files = []
        for name, (loc, rot) in shots.items():
            cap.set_actor_location_and_rotation(loc, rot, False, False)
            note("camera", shot=name, at=vec(cap.get_actor_location()), rot=str(cap.get_actor_rotation()))
            for bias in (-1.0, 0.5, 2.0, 3.5):
                pp = cc.get_editor_property("post_process_settings")
                pp.set_editor_property("override_auto_exposure_method", True)
                pp.set_editor_property("auto_exposure_method", unreal.AutoExposureMethod.AEM_MANUAL)
                pp.set_editor_property("override_auto_exposure_bias", True)
                pp.set_editor_property("auto_exposure_bias", bias)
                pp.set_editor_property("override_auto_exposure_apply_physical_camera_exposure", True)
                pp.set_editor_property("auto_exposure_apply_physical_camera_exposure", False)
                cc.set_editor_property("post_process_settings", pp)
                # 17 Nov diagnosis run (ue11-diag): strands are absent from a scene capture's first frames and fully drawn
                # by the 60th tick; captures repeated inside one tick are untested as a warm-up (default 0): the proven
                # way is LEDGER_GROOM_DIAG=1 with LEDGER_GROOM_DIAG_HIDE=0, which warms over ticks and adds front and behind
                for _w in range(int(os.environ.get("LEDGER_GROOM_WARMUP", "0"))):
                    cc.capture_scene()
                cc.capture_scene()
                fn = "darren_%s_ev%+.1f.png" % (name, bias)
                unreal.RenderingLibrary.export_render_target(unreal.EditorLevelLibrary.get_editor_world(), rt, OUT, fn)
                files.append(fn)
        note("pictures", files=files, note="A (his current hair) on the left of the front view at x 0; B (the tool's strands) at x 60")
        unreal.EditorLevelLibrary.destroy_actor(cap)

    DIAG_VIEWS = {"side": ((180, 0), 180.0), "front": ((60, 120), -90.0), "behind": ((60, -120), 90.0)}

    def diag_shot(face_z, k, view_mode=None, view="side"):
        # one side picture per call, spread over many ticks so streamed strand data has time to arrive
        if "diag_cap" not in st:
            rt = unreal.RenderingLibrary.create_render_target2d(unreal.EditorLevelLibrary.get_editor_world(), 1600, 1000,
                                                                unreal.TextureRenderTargetFormat.RTF_RGBA8)
            cap = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.SceneCapture2D, unreal.Vector(0, 0, 0))
            cc = cap.get_component_by_class(unreal.SceneCaptureComponent2D)
            cc.set_editor_property("texture_target", rt)
            cc.set_editor_property("capture_source", unreal.SceneCaptureSource.SCS_FINAL_COLOR_LDR)
            cc.set_editor_property("fov_angle", 45.0)
            pp = cc.get_editor_property("post_process_settings")
            pp.set_editor_property("override_auto_exposure_method", True)
            pp.set_editor_property("auto_exposure_method", unreal.AutoExposureMethod.AEM_MANUAL)
            pp.set_editor_property("override_auto_exposure_bias", True)
            pp.set_editor_property("auto_exposure_bias", 0.5)
            pp.set_editor_property("override_auto_exposure_apply_physical_camera_exposure", True)
            pp.set_editor_property("auto_exposure_apply_physical_camera_exposure", False)
            cc.set_editor_property("post_process_settings", pp)
            st["diag_cap"], st["diag_cc"], st["diag_rt"] = cap, cc, rt
        if st.get("diag_view") != view:
            # views of B (x 60), level, by keyword (Rotator order is roll, pitch, yaw)
            (x, y), yaw = DIAG_VIEWS[view]
            st["diag_cap"].set_actor_location_and_rotation(unreal.Vector(x, y, face_z - 12.0), unreal.Rotator(roll=0.0, pitch=0.0, yaw=yaw), False, False)
            st["diag_view"] = view
            note("camera", shot="diag_" + view, at=vec(st["diag_cap"].get_actor_location()), rot=str(st["diag_cap"].get_actor_rotation()))
        world = unreal.EditorLevelLibrary.get_editor_world()
        if view_mode is not None:
            unreal.SystemLibrary.execute_console_command(world, "r.HairStrands.ViewMode %d" % view_mode)
        st["diag_cc"].capture_scene()
        if k < 0:
            return
        fn = "diag_%s_t%02d%s.png" % (view, k, "" if view_mode is None else "_vm%d" % view_mode)
        unreal.RenderingLibrary.export_render_target(world, st["diag_rt"], OUT, fn)
        note("diag_picture", file=fn, tick=k, view_mode=view_mode)

    def tick(delta):
        now = time.time()
        try:
            if st.get("busy"):
                return
            if st["phase"] == 0 and now - st["t0"] > seconds:
                # an import pumps editor ticks, so this callback re-enters during it (13 Nov, second run): hold it off
                st["busy"] = True
                st["phase"] = 1
                # runs 5 and 6 tried an empty level: unlit once, refused once; the start level stays (its floor
                # was what run 4 photographed, through the camera pointing down)
                g = import_groom()
                setup(g)
                st["t1"] = time.time()
                st["busy"] = False
            elif st["phase"] == 1 and now - st["t1"] > 25.0 and DIAG:
                # diagnosis: a side picture at ticks 0, 15, 30, 45 and 60, then one frame at strand view mode 36
                k = st.setdefault("diag_k", 0)
                if k == 0:
                    st["diag_face_z"] = measure().get("face_top_z", 190.0) - 2.0
                if k <= 60:
                    # every tick captures (the warm-up); five are written
                    diag_shot(st["diag_face_z"], k if k % 15 == 0 else -1)
                if k == 62:
                    diag_shot(st["diag_face_z"], k, view_mode=36)
                if 65 <= k <= 84:
                    diag_shot(st["diag_face_z"], 84 if k == 84 else -1, view="front")
                if 85 <= k <= 104:
                    diag_shot(st["diag_face_z"], 104 if k == 104 else -1, view="behind")
                if k == 64:
                    diag_shot(st["diag_face_z"], k, view_mode=0)
                if k == 105:
                    unreal.EditorLevelLibrary.destroy_actor(st["diag_cap"])
                    st["phase"] = 2
                    st["t1"] = now
                st["diag_k"] = k + 1
            elif st["phase"] == 1 and now - st["t1"] > 25.0:
                st["phase"] = 2
                m = measure()
                capture(m.get("face_top_z", 190.0) - 2.0)
                st["t1"] = now
            elif st["phase"] == 2 and now - st["t1"] > 3.0:
                st["phase"] = 3
                for x in st.get("actors_extra", []) + st["actors"] + st["lights"]:
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
