"""A cloud kit piece made ready for the held-props route: its parts joined into one mesh, its
material slots kept by name, written to ledger/Assets/Props/base-mesh/<name>.glb, the held-props folder
the street reads by name (listed there in THIRD-PARTY.md as the project's own work).

    blender -b --factory-startup --python tools/art-recipes/kit_for_game.py -- \
        production/assets/cloud-week/lamp-posts/lamp_post_C.glb ledger/Assets/Props/base-mesh/lamp_post_C.glb

WHY, 21 October 2026 (his order, item 5, lamp post C first): the kit's .glb files hold one node per
part (lamp post C has dozens: the column, its door plate and screws, the lantern's canopy, bowl,
glass and tube), and the street's prop importer (tools/ue/import_prop_meshes.py) makes ONE static
mesh per file, finding it by name; a many-part file would come in as many meshes. The street's own
rooms are joined before export for the same reason (tools/art-recipes/shop-room.py export_room).
Nothing else changes: no transform, no scale, the same vertices and the same named slots, so the
model's measured bounds and the kit's checks still hold. The source stays the cloud's, rebuilt by
its own build script; this is a copy for the game.
"""
import os
import sys


def main(argv):
    import bpy
    src, dst = os.path.abspath(argv[0]), os.path.abspath(argv[1])
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=src)
    meshes = [o for o in bpy.context.scene.objects if o.type == "MESH"]
    if not meshes:
        print("kit_for_game: no mesh in %s" % src)
        return 2
    before_slots = sorted({s.material.name for o in meshes for s in o.material_slots if s.material})
    for o in bpy.context.scene.objects:
        o.select_set(False)
    for o in meshes:
        mw = o.matrix_world.copy()
        o.parent = None
        o.matrix_world = mw
        o.select_set(True)
    bpy.context.view_layer.objects.active = meshes[0]
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    if len(meshes) > 1:
        bpy.ops.object.join()
    joined = bpy.context.view_layer.objects.active
    joined.name = os.path.splitext(os.path.basename(dst))[0]
    for o in [o for o in bpy.context.scene.objects if o.type != "MESH"]:
        bpy.data.objects.remove(o, do_unlink=True)
    after_slots = sorted({s.material.name for s in joined.material_slots if s.material})
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    bpy.ops.object.select_all(action="DESELECT")
    joined.select_set(True)
    bpy.ops.export_scene.gltf(filepath=dst, export_format="GLB", use_selection=True, export_apply=True,
                              export_materials="EXPORT", export_yup=True)
    tris = sum(len(p.vertices) - 2 for p in joined.data.polygons)
    print("kit_for_game: %s -> %s parts=%d slots=%d (%s) slotsKept=%s triangles=%d"
          % (os.path.basename(src), dst, len(meshes), len(after_slots), ",".join(after_slots),
             "yes" if before_slots == after_slots else "NO", tris))
    return 0 if before_slots == after_slots else 2


if __name__ == "__main__":
    args = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    if len(args) != 2:
        print(__doc__)
        sys.exit(1)
    sys.exit(main(args))
