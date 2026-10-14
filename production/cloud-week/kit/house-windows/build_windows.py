"""One command rebuilds everything of unit 8 (the street windows): `python3 build_windows.py [stage ...]` (stages: assets kit manifest rooms gate check; none = all, in that order).

  assets    the Poly Haven models and textures of the thirteen rooms at 1k (CC0), the marks painted out (hw_models.py)
  kit       hw_S22.glb, hw_S11.glb, hw_RC.glb, hw_RC2.glb, hw_room_card_gf.glb into production/assets/cloud-week/house-windows/ (hw_kit.py), and hw_manifest.json
  rooms     the thirteen rooms' three pictures and JSON each into SCRATCH/rooms (hw_roomgen.py), in the order of the review views; rooms already rendered are kept (delete a room's .json to redo it)
  gate      the review views and the measuring frames (hw_gate_run.py), what is already rendered is kept
  check     check_windows.py: "N of M rows pass", checks/check_windows_v2.json (v1 stays as the record of try 1)

Heavy outputs (the rooms' pictures, the gate's frames, the models) go to SCRATCH (LEDGER_HW_SCRATCH, default /home/user/ledger-scratch/house-windows), never into git; the kit glbs, the review previews and
the check are small and are. Python: /home/user/.bpyenv/bin/python (bpy 5.2.2); run it under `nice -n 15`, one render at a time (the machine is shared).
"""
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import hw_t as T  # noqa: E402

PY = "/home/user/.bpyenv/bin/python"
GLB_NAMES = {"S22": "hw_S22.glb", "S11": "hw_S11.glb", "RC": "hw_RC.glb", "RC2": "hw_RC2.glb", "GF": "hw_room_card_gf.glb"}
ROOM_ORDER = ["up_lounge_1", "up_lounge_2", "up_bedroom_1", "up_landing_1", "up_landing_2", "gf_front_1", "up_empty_1", "up_empty_2", "up_lounge_3", "up_bedroom_2", "up_bedroom_3", "gf_front_2", "gf_front_3"]


def run(args, log=print):
    log("$ " + " ".join(args))
    r = subprocess.run(["nice", "-n", "15"] + args, cwd=HERE)
    if r.returncode:
        raise SystemExit("failed: %s" % " ".join(args))


def stage_assets():
    run([PY, "hw_models.py"])


def stage_kit():
    os.makedirs(T.ASSETS, exist_ok=True)
    for k in ("S22", "S11", "RC", "RC2", "GF"):
        run([PY, "hw_kit.py", k])
        shutil.copyfile(os.path.join(T.KITWORK, "out", GLB_NAMES[k]), os.path.join(T.ASSETS, GLB_NAMES[k]))
    stage_manifest()


def stage_manifest():
    """hw_manifest.json: for each of the twenty sites the kit piece, where it stands (the placement of target 8), its paint, net, drape and room (the PC's import reads it)."""
    P = T.paints()
    out = {"made_by": "production/cloud-week/kit/house-windows/build_windows.py", "frame": "kit frame in metres: x across (the viewer's right), y into the wall, z up; pivot the opening's bottom-edge centre on the brick face",
           "placement": T.target()["kit_pieces"]["placement"], "paint_note": "each glb carries its kind's default paint (S22 and S11 paint_white_fresh, RC and RC2 paint_white_upvc); the house's own paint is set on the slot by name from `paints`",
           "glass_note": "glass_house: base colour 0.03, roughness 0.03, metallic 0, KHR_materials_specular colour 2.0 (Cycles Specular IOR Level 1.0, F0 0.08), opaque; COLOR_0 on each pane is the dirt mask (1.0 clean, 0.8 the 6 mm band and the lowest 25 mm). Every pane is a closed slab 2.5 mm thick (a front and a back face): the pane the PC builds is one surface whose reflectance is the FRONT face's alone (F0 0.08 stands for both faces, target 5.1); the cloud gate's pane is Fresnel x (1 - Backfacing) for the same reason (14 Oct, from the try 1 reviews)",
           "grime_note": "a window whose condition is grimy carries the target 4.2 grime band: the lowest 30 mm of paint_joinery__lower_bottom_rail (RC and RC2: paint_joinery__frame_sill_rail), measured up from the part's own lowest point, and the top faces of paint_joinery__oak_sill at x 0.75 of the paint, on top of the x 0.85 those parts already take; sites[].grime_band lists them. It is the house's condition, not the kit piece's, so it is not baked into COLOR_0 (the glb carries the default paint of every house of its kind)",
           "cottage_note": "a cottage's two windows share one room card and one pendant: hw_room_card_gf.glb, centred between them; the window pieces' own room__card and pendant__shade are not placed on a cottage", "sites": []}
    for s in T.sites():
        ex = s.get("extra") or {}
        net = s["net"]
        nodes = []
        if net["kind"] != "N0":
            nodes += ["net__N1_torn" if net.get("torn") else "net__" + net["kind"], "net_rod__" + net["kind"], "net_bracket__%s_L" % net["kind"], "net_bracket__%s_R" % net["kind"]]
        if ex.get("kind") in ("C1", "C2"):
            nodes += (["curtain__C1_drawn"] if ex["kind"] == "C1" else ["curtain__C2_open_L", "curtain__C2_open_R"]) + ["curtain_pole", "curtain_finial__L", "curtain_finial__R", "curtain_bracket__L", "curtain_bracket__R"]
        if ex.get("kind") in ("B1", "B2", "B3"):
            nodes += ["blind__" + ex["kind"]] + {"B1": ["blind_headrail__B1"], "B2": ["blind_roller__B2"], "B3": ["blind_headrail__B3"]}[ex["kind"]]
        if s["card"]["room_family"] == "UP" and T.room(s["room"])["pendant"]:
            nodes.append("pendant__shade")
        pl = {"x": round(-s["x_centre"], 4), "y": 5.125 * s["side"], "z": s["sill_z_above_crown"], "turn_deg": 0.0 if s["side"] > 0 else 180.0}
        out["sites"].append({"id": s["id"], "kind": s["kind"], "glb": "hw_%s.glb" % s["kind"], "street_x_centre": s["x_centre"], "side": s["side"], "sill_z_above_crown": s["sill_z_above_crown"], "paint": s["paint"], "paint_srgb": P[s["paint"]]["srgb"],
                             "paint_roughness": P[s["paint"]]["rough"], "condition": s["condition"], "switch_on": nodes, "net_colour": net.get("colour"), "drape": ex or None, "room": s["room"], "card": s["card"], "lit_at_20_30": s["id"] in T.lit_at("20:30"),
                             "room_card_node": "room__card" if s["card"]["room_family"] == "UP" else "hw_room_card_gf.glb",
                             "grime_band": ({"parts": (["paint_joinery__lower_bottom_rail (its lowest 30 mm)", "paint_joinery__oak_sill (top faces)"] if s["kind"] in ("S22", "S11") else ["paint_joinery__frame_sill_rail (its lowest 30 mm)"]), "height_mm": 30, "factor": 0.75} if s["condition"] == "grimy" else None)})
    json.dump(out, open(os.path.join(T.ASSETS, "hw_manifest.json"), "w"), indent=1)


def stage_rooms():
    T.ensure(T.ROOMS)
    for rid in ROOM_ORDER:
        if os.path.exists(os.path.join(T.ROOMS, rid + ".json")):
            print("room %s kept" % rid)
            continue
        run([PY, "hw_roomgen.py", rid, T.ROOMS, "24", "1.0"])


def stage_gate():
    run([PY, "hw_gate_run.py"] + sys.argv[2:])


def stage_check():
    run([PY, "check_windows.py"])


STAGES = {"assets": stage_assets, "kit": stage_kit, "manifest": stage_manifest, "rooms": stage_rooms, "gate": stage_gate, "check": stage_check}

if __name__ == "__main__":
    which = [a for a in sys.argv[1:] if a in STAGES] or ["assets", "kit", "rooms", "gate", "check"]
    for w in which:
        print("== stage", w, flush=True)
        STAGES[w]()
