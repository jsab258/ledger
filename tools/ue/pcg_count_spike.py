"""PHASE 5 RESEARCH, ONE COUNT (7 November 2026): what a cooked level really holds of a saved PCG result.

PCG-RESULT-HOME-2026-11-03.md and PCG-SOURCE-ANSWERS-2026-11-07.md read from Unreal 5.8's source that a saved CPU
result ships as plain instanced meshes when its graph is not cooked, and said "unverified until one packaged count".
This runs in a throwaway project (never ue-probe), in the full editor because PCG generates on the editor's tick.
Copy it to the project's Content/Python/init_unreal.py and open the project with -RenderOffscreen -unattended
-nosplash; -ExecutePythonScript will not do, since the editor exits as soon as the script returns (7 Nov). It makes one graph (grid, random offset and turn, mesh spawner), a level with one volume, generates twice to compare
every transform, takes the time, turns the graph's Should Cook off, saves and quits. It writes result.json beside
the project. The packaged game's own object list is the other half of the count.
"""
import hashlib
import json
import os
import time

import unreal

PROJECT = unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
OUT = os.path.join(PROJECT, "result.json")
result = {"steps": []}


def note(text):
    result["steps"].append(text)
    unreal.log("PCGCOUNT " + text)
    write()


def write():
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=1)


def make_graph():
    tools = unreal.AssetToolsHelpers.get_asset_tools()
    graph = tools.create_asset("G_Count", "/Game", unreal.PCGGraph, unreal.PCGGraphFactory())
    grid_node, grid = graph.add_node_of_type(unreal.PCGCreatePointsGridSettings)
    grid.set_editor_property("grid_extents", unreal.Vector(7000, 7000, 0))
    grid.set_editor_property("cell_size", unreal.Vector(100, 100, 100))
    move_node, move = graph.add_node_of_type(unreal.PCGTransformPointsSettings)
    move.set_editor_property("offset_min", unreal.Vector(-30, -30, 0))
    move.set_editor_property("offset_max", unreal.Vector(30, 30, 0))
    move.set_editor_property("rotation_max", unreal.Rotator(0, 0, 180))
    spawn_node, spawn = graph.add_node_of_type(unreal.PCGStaticMeshSpawnerSettings)
    selector = spawn.get_editor_property("mesh_selector_parameters")
    entry = unreal.PCGMeshSelectorWeightedEntry()
    descriptor = entry.get_editor_property("descriptor")
    descriptor.set_editor_property("static_mesh", unreal.load_asset("/Engine/BasicShapes/Cube.Cube"))
    entry.set_editor_property("descriptor", descriptor)
    selector.set_editor_property("mesh_entries", [entry])
    graph.add_edge(grid_node, "Out", move_node, "In")
    graph.add_edge(move_node, "Out", spawn_node, "In")
    return graph


def fingerprint(actor):
    """Every instance's transform to a tenth of a millimetre, sorted, so the order of components does not count."""
    rows, per_component = [], []
    for comp in actor.get_components_by_class(unreal.InstancedStaticMeshComponent):
        count = comp.get_instance_count()
        per_component.append([comp.get_class().get_name(), count])
        for i in range(count):
            t = comp.get_instance_transform(i, True)
            q = t.rotation
            rows.append("%.1f %.1f %.1f %.4f %.4f %.4f %.4f" % (
                t.translation.x, t.translation.y, t.translation.z, q.x, q.y, q.z, q.w))
    rows.sort()
    return len(rows), hashlib.sha256("\n".join(rows).encode()).hexdigest()[:16], per_component


graph = volume = component = None
state = {"stage": "wait", "ticks": 0, "started": time.time(), "last": -1, "still": 0, "seen": 0}


def begin():
    global graph, volume, component
    # A blank plain level, not LevelEditorSubsystem.new_level: from the open-world start map it failed to save and
    # the editor then crashed inside the level editor (7 Nov, first run).
    unreal.EditorLoadingAndSavingUtils.new_blank_map(False)
    graph = make_graph()
    volume = unreal.get_editor_subsystem(unreal.EditorActorSubsystem).spawn_actor_from_class(
        unreal.PCGVolume, unreal.Vector(0, 0, 0))
    volume.set_actor_scale3d(unreal.Vector(100, 100, 10))
    component = volume.get_component_by_class(unreal.PCGComponent)
    component.set_graph(graph)
    component.set_editor_property("generation_trigger", unreal.PCGComponentGenerationTrigger.GENERATE_ON_DEMAND)
    note("made graph and volume")
    state.update(stage="first", started=time.time())
    component.generate(True)


def finish():
    graph.set_editor_property("should_cook", unreal.PerPlatformBool(default=False))
    unreal.EditorAssetLibrary.save_loaded_asset(graph)
    world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
    result["level_saved"] = unreal.EditorLoadingAndSavingUtils.save_map(world, "/Game/CountMap")
    result["saved_count"] = fingerprint(volume)[0]
    note("saved with Should Cook off")
    write()
    unreal.unregister_slate_post_tick_callback(handle)
    unreal.SystemLibrary.quit_editor()


def tick(_delta):
    now = time.time()
    if now - state["started"] > 300:
        note("timed out in stage " + state["stage"])
        result["failed"] = True
        write()
        unreal.unregister_slate_post_tick_callback(handle)
        unreal.SystemLibrary.quit_editor()
        return
    count, digest, parts = fingerprint(volume) if state["last"] != -2 else (0, "", [])
    if count == 0 or count != state["last"]:
        if count:
            state["seen"] = now
        state["last"], state["still"] = count, 0
        return
    state["still"] += 1
    if state["still"] < 10:
        return
    if state["stage"] == "first":
        result["first"] = {"instances": count, "hash": digest, "components": parts,
                           "seconds_to_stable": round(state["seen"] - state["started"], 2)}
        note("first generation: %d instances, %s" % (count, digest))
        write()
        component.cleanup_local(True)
        state.update(stage="cleared", last=-1, still=0, started=now)
    elif state["stage"] == "second":
        result["second"] = {"instances": count, "hash": digest, "components": parts,
                            "seconds_to_stable": round(state["seen"] - state["started"], 2)}
        result["same_every_transform"] = digest == result["first"]["hash"]
        note("second generation: %d instances, %s" % (count, digest))
        finish()


def tick_guarded(delta):
    try:
        if state["stage"] == "wait":
            # init_unreal.py runs before the editor's world is ready: give it some ticks
            state["ticks"] += 1
            if state["ticks"] >= 120:
                begin()
            return
        if state["stage"] == "cleared":
            if not volume.get_components_by_class(unreal.InstancedStaticMeshComponent):
                state.update(stage="second", last=-1, still=0, started=time.time())
                component.generate(True)
            elif time.time() - state["started"] > 60:
                state.update(stage="second", last=-1, still=0, started=time.time())
                component.generate(True)
            return
        tick(delta)
    except Exception as err:
        note("failed: %s" % err)
        result["failed"] = True
        write()
        unreal.unregister_slate_post_tick_callback(handle)
        unreal.SystemLibrary.quit_editor()


handle = unreal.register_slate_post_tick_callback(tick_guarded)
write()
