#!/usr/bin/env python3
"""Blender headless: import one mesh, measure it, normalise it, LOD it, export.

    blender --background --factory-startup --python clean_lod.py -- \
        --in SRC --out-dir DIR --id lamp_post_01 \
        --lods LOD0=1.0,LOD1=0.5,LOD2=0.25 --result DIR/blender-result.json \
        [--target-height 3.0] [--pivot base-centre] \
        [--kind prop|garment] [--keep-mesh Jacket]

A GARMENT IS NOT A PROP, 24 September. The research on clothing found that
four lines here, each right for a kerb, silently ruin a coat: only meshes were
selected, so the armature was dropped; the mesh was scaled and re-pivoted
without it, which walks the cloth off the body; EVERY modifier was applied,
including the Armature modifier that binds it; and the export took only the
meshes. --kind garment keeps the coat where it was on the body, at the body's
scale, applies only this script's own modifiers, and exports the armature with
it when there is one. It also writes <id>_source.glb, the kept meshes as they
came in with nothing cleaned, which is the reference the garment checker
(meshgen.py --garment-check) measures the cleaned file against. --keep-mesh
keeps only the meshes whose name contains that text, so one garment can be
taken off a character file. Prop mode is unchanged.

UNRUN WHERE IT WAS WRITTEN. There is no Blender in the container this was
authored in, so every line below is untested against a real bpy. What IS tested
(tools/meshgen/meshgen.py --selftest) is the seam: that this file parses as
Python, and that every flag meshgen.py passes is a flag this argument parser
accepts. A driver and a script that disagree about one flag name is the
cheapest possible way to lose a night, and it is the one thing about this file
that can be checked from here.

IT ALWAYS WRITES THE RESULT FILE, including when it fails, and the caller reads
that file rather than the exit code. Blender exits 0 when a --python script
raises after its last operator, and it exits 0 having written nothing when the
file it was pointed at held no mesh. Both look identical to a return code.
"""
import json
import os
import sys
import traceback

try:
    import addon_utils
    import bpy
    import mathutils
except ImportError:                       # not inside Blender: say so plainly
    addon_utils = None
    bpy = None
    mathutils = None


def parse_args(argv):
    """Deliberately hand-rolled and permissive about ORDER, because argparse
    inside Blender has bitten every project that has tried it: Blender eats
    everything before `--` and argparse's error path calls sys.exit, which
    inside Blender means no result file and therefore no diagnosis."""
    args = {"lods": "LOD0=1.0", "pivot": "base-centre", "target-height": None,
            "in": None, "out-dir": None, "id": None, "result": None,
            "kind": "prop", "keep-mesh": None}
    i = 0
    while i < len(argv):
        a = argv[i]
        if a.startswith("--"):
            key = a[2:]
            val = argv[i + 1] if i + 1 < len(argv) and not argv[i + 1].startswith("--") else "1"
            if key not in args:
                raise ValueError(f"unknown flag --{key}. Known: "
                                 + ", ".join("--" + k for k in sorted(args)))
            args[key] = val
            i += 2
        else:
            i += 1
    for need in ("in", "out-dir", "id", "result"):
        if not args[need]:
            raise ValueError(f"--{need} is required")
    if args["kind"] not in ("prop", "garment"):
        raise ValueError(f"--kind is prop or garment, not {args['kind']!r}")
    if args["kind"] == "garment" and args["target-height"]:
        raise ValueError("a garment keeps its body's scale: --target-height would size it "
                         "off the body, so it is refused rather than ignored")
    return args


def ensure_addon(module):
    if addon_utils is None:
        return False
    try:
        loaded, enabled = addon_utils.check(module)
        if not enabled:
            addon_utils.enable(module, default_set=False, persistent=True)
        return True
    except Exception:                                            # noqa: BLE001
        return False


def import_any(path):
    """Import by extension, and say which importer refused rather than
    'nothing happened'."""
    ext = os.path.splitext(path)[1].lower()
    if ext in (".glb", ".gltf"):
        ensure_addon("io_scene_gltf2")
        bpy.ops.import_scene.gltf(filepath=path)
    elif ext == ".fbx":
        ensure_addon("io_scene_fbx")
        bpy.ops.import_scene.fbx(filepath=path)
    elif ext == ".obj":
        # Blender 4.x renamed this operator. Try the new one, fall back.
        if hasattr(bpy.ops.wm, "obj_import"):
            bpy.ops.wm.obj_import(filepath=path)
        else:
            ensure_addon("io_scene_obj")
            bpy.ops.import_scene.obj(filepath=path)
    else:
        raise ValueError(f"no importer for {ext!r} ({path})")


def mesh_objects():
    return [o for o in bpy.context.scene.objects if o.type == "MESH"]


def world_bounds(objs):
    lo = [float("inf")] * 3
    hi = [float("-inf")] * 3
    for o in objs:
        for corner in o.bound_box:
            w = o.matrix_world @ mathutils.Vector(corner)
            for k in range(3):
                lo[k] = min(lo[k], w[k])
                hi[k] = max(hi[k], w[k])
    if lo[0] == float("inf"):
        raise ValueError("the imported file contains no mesh geometry at all")
    return lo, hi


def counts(objs):
    v = sum(len(o.data.vertices) for o in objs)
    t = sum(len(o.data.loop_triangles) or len(o.data.polygons) for o in objs)
    return v, t


def armatures():
    return [o for o in bpy.context.scene.objects if o.type == "ARMATURE"]


def select_only(objs):
    bpy.ops.object.select_all(action="DESELECT")
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0] if objs else None


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]
    result = {"ok": False, "error": "the script did not reach its own end",
              "blender": None, "outputs": {}}
    args = None
    try:
        args = parse_args(argv)
        result_path = args["result"]
        if bpy is None:
            raise RuntimeError("this script must run inside Blender "
                               "(blender --background --python clean_lod.py)")
        result["blender"] = bpy.app.version_string
        os.makedirs(args["out-dir"], exist_ok=True)

        bpy.ops.wm.read_factory_settings(use_empty=True)
        import_any(args["in"])
        garment = args["kind"] == "garment"
        if args["keep-mesh"]:
            want = args["keep-mesh"].lower()
            drop = [o for o in mesh_objects() if want not in o.name.lower()]
            for o in drop:
                bpy.data.objects.remove(o, do_unlink=True)
            result["kept"] = [o.name for o in mesh_objects()]
        objs = mesh_objects()
        if not objs:
            raise ValueError(f"{args['in']} imported without a single mesh object"
                             + (f" named like {args['keep-mesh']!r}" if args["keep-mesh"] else ""))
        result["kind"] = args["kind"]
        result["armatures"] = [a.name for a in armatures()]
        if garment:
            # THE REFERENCE, before anything is touched: the same importer and
            # the same exporter, and none of the cleaning in between.
            ref = os.path.join(args["out-dir"], f"{args['id']}_source.glb")
            select_only(objs + armatures())
            bpy.ops.export_scene.gltf(filepath=ref, export_format="GLB", use_selection=True)
            result["reference"] = ref

        for o in objs:
            o.data.calc_loop_triangles()
        v0, t0 = counts(objs)
        lo, hi = world_bounds(objs)
        dims = [hi[k] - lo[k] for k in range(3)]
        result["source"] = {"verts": v0, "tris": t0,
                            "dims_m": [round(d, 4) for d in dims],
                            "objects": len(objs)}

        # NORMALISE. Scale is uniform - a per-axis fit would silently distort a
        # prop to hit a number, which is worse than a prop that is the wrong
        # size, because the wrong size is visible and the distortion reads as
        # bad modelling.
        scale = 1.0
        if args["target-height"] and not garment:
            want = float(args["target-height"])
            if dims[2] > 1e-9 and dims[2] >= dims[1]:
                have = dims[2]      # glTF/Blender Z-up on import from FBX/OBJ
            else:
                have = max(dims[1], dims[2])
            if have > 1e-9:
                scale = want / have
        select_only(objs)
        if abs(scale - 1.0) > 1e-6:
            bpy.ops.transform.resize(value=(scale, scale, scale))
            bpy.ops.object.transform_apply(location=False, rotation=False,
                                           scale=True)
            lo, hi = world_bounds(objs)
            dims = [hi[k] - lo[k] for k in range(3)]
        result["scale_applied"] = round(scale, 6)

        # PIVOT. base-centre means x/y centred on the footprint and z=0 at the
        # bottom face, which is the only convention that lets a placer drop a
        # prop on a pavement without knowing anything about it.
        if garment:
            args["pivot"] = "kept-on-the-body"
        elif args["pivot"] == "base-centre":
            dx = -(lo[0] + hi[0]) / 2.0
            dy = -(lo[1] + hi[1]) / 2.0
            dz = -lo[2]
            select_only(objs)
            bpy.ops.transform.translate(value=(dx, dy, dz))
            bpy.ops.object.transform_apply(location=True, rotation=False,
                                           scale=False)
        result["pivot"] = args["pivot"]

        base = [o for o in mesh_objects()]
        outputs = {}
        ladder = {}
        for pair in args["lods"].split(","):
            if not pair.strip():
                continue
            name, _, ratio_s = pair.partition("=")
            name, ratio = name.strip(), float(ratio_s or 1.0)
            bpy.ops.object.select_all(action="DESELECT")
            copies = []
            for o in base:
                c = o.copy()
                c.data = o.data.copy()
                bpy.context.collection.objects.link(c)
                copies.append(c)
            select_only(copies)
            for c in copies:
                c.modifiers.new("ledger_tri", "TRIANGULATE")
                if ratio < 1.0:
                    dec = c.modifiers.new("ledger_dec", "DECIMATE")
                    dec.decimate_type = "COLLAPSE"
                    dec.ratio = ratio
                bpy.context.view_layer.objects.active = c
                if garment:
                    # ONLY OUR OWN, AND FIRST: the Armature modifier that binds
                    # the coat to the body stays, unapplied, below them.
                    for mod in ("ledger_dec", "ledger_tri"):
                        if mod in c.modifiers:
                            bpy.ops.object.modifier_move_to_index(modifier=mod, index=0)
                    for mod in ("ledger_tri", "ledger_dec"):
                        if mod in c.modifiers:
                            bpy.ops.object.modifier_apply(modifier=mod)
                else:
                    for m in list(c.modifiers):
                        bpy.ops.object.modifier_apply(modifier=m.name)
            for c in copies:
                c.data.calc_loop_triangles()
            v, t = counts(copies)
            path = os.path.join(args["out-dir"], f"{args['id']}_{name}.glb")
            select_only(copies + (armatures() if garment else []))
            if garment:
                # THE ORIGINALS STAY OUT OF THE FILE: hidden from the selection
                # by being deselected is not enough when they share the armature.
                for o in base:
                    o.select_set(False)
            bpy.ops.export_scene.gltf(filepath=path, export_format="GLB",
                                      use_selection=True)
            if not os.path.exists(path):
                raise RuntimeError(f"the exporter returned without writing {path}")
            outputs[name] = path
            ladder[name] = {"ratio": ratio, "verts": v, "tris": t,
                            "bytes": os.path.getsize(path)}
            for c in copies:
                bpy.data.objects.remove(c, do_unlink=True)

        result["outputs"] = outputs
        result["ladder"] = ladder
        result["dims_m"] = [round(d, 4) for d in dims]
        result["ok"] = True
        result["error"] = None
    except Exception as e:                                       # noqa: BLE001
        result["ok"] = False
        result["error"] = f"{type(e).__name__}: {e}"
        result["traceback"] = traceback.format_exc()[-2000:]
    finally:
        path = (args or {}).get("result")
        if path:
            try:
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(result, f, indent=2)
            except OSError as e:
                sys.stderr.write(f"could not write the result file: {e}\n")
        else:
            sys.stderr.write(json.dumps(result) + "\n")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
