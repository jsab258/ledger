"""Test target.json against its own sources before anything is built to it.

1. every printed dimension used is reproduced (or, where a photograph overrode it, the photo value is);
2. the elevation's proportions against photographs P1 and P2, measured edge by edge with their error;
3. every disagreement resolved by the photographs-win rule;
4. internal consistency (panels in grooves, members add up, leaf in the rebate with its clearances).
Writes the result into target.json["self_check"] and prints a Markdown table for SOURCES.md.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
TP = HERE / "target.json"
T = json.loads(TP.read_text(encoding="utf-8"))
L, P, M, F, O = T["leaf"], T["panels"], T["mouldings"], T["frame"], T["opening"]
IN = 25.4
rows = []

def check(group, name, ok, detail):
    rows.append({"group": group, "check": name, "pass": bool(ok), "detail": detail})

def near(a, b, tol=0.15):
    return abs(a - b) <= tol

# ---- 1. printed dimensions ----
printed = [
    ("leaf width 2 ft 8 in, Hasluck p.347", 32 * IN, L["width_mm"]),
    ("leaf thickness 2 in, Ellis p.93 / Hasluck p.398", 2 * IN, L["thickness_mm"]),
    ("stile 4 1/2 in, Ellis p.93 / Riley p.357", 4.5 * IN, L["stile_mm"]),
    ("top rail 5 in, Riley p.357 (photo agrees; Ellis 4 1/2 in overridden, D8)", 5 * IN, L["top_rail_mm"]),
    ("lock rail 9 in, Ellis p.93 (photo agrees)", 9 * IN, L["lock_rail_mm"]),
    ("groove 1/2 in, Ellis p.92", 0.5 * IN, P["groove_depth_mm"]),
    ("panel side play 1/8 in, Ellis p.92", IN / 8, P["side_play_mm"]),
    ("bolection lap 3/16 in (1/8 to 3/16), Ellis p.92", 3 * IN / 16, M["outside_bolection"]["lap_over_framing_mm"]),
    ("reveal 4 1/2 in, Hasluck p.346", 4.5 * IN, O["reveal_depth_mm"]),
    ("frame 4 in across, Riley p.357", 4 * IN, F["jamb_face_mm"]),
    ("frame 5 in deep, Riley p.357", 5 * IN, F["jamb_depth_mm"]),
    ("panel one-third of door, Riley p.353", 2 * IN / 3, P["thickness_mm"]),
]
for name, src, val in printed:
    check("1 printed", name, near(src, val), f"source {src:.1f}, target {val:.1f}")
overridden = [  # printed value, target value, the photo value it must equal, decision id
    ("leaf height 6 ft 8 in, Hasluck p.347", 80 * IN, L["height_mm"], 1948.0, "D1"),
    ("muntin 4 in, Ellis p.93 / Riley p.357", 4 * IN, L["muntin_mm"], 132.2, "D2"),
    ("lock rail centre 2 ft 8 in less 6 in from a step, Ellis p.93 (Riley 2 ft 9 in)", 26 * IN, L["lock_rail_centre_above_leaf_bottom_mm"], 787.0, "D3"),
    ("bottom rail 9 in, Ellis p.93 (Riley 11 in)", 9 * IN, L["bottom_rail_mm"], 192.8, "D4"),
    ("jamb showing past brick, Hasluck Fig. 1148 scaled 39", 39.0, F["jamb_showing_past_brick_mm"], 55.0, "D5"),
    ("transom 4 in, Riley p.357", 4 * IN, F["transom"]["face_height_mm"], 65.0, "D6"),
    ("fanlight 1 ft 6 in, Hasluck p.347", 18 * IN, F["fanlight"]["glass_sight_mm"]["z1"] - F["fanlight"]["glass_sight_mm"]["z0"], 267.0, "D7"),
]
for name, src, val, photo, d in overridden:
    check("3 photo wins", f"{d}: {name}", near(val, photo, 0.6), f"book {src:.1f}, photo {photo:.1f}, target {val:.1f}")

# ---- 2. proportions against the photographs ----
# P1 (Teignmouth, door-photo-01, 480x640): edges in pixels, +-2 px each (read off 6x zooms and colour profiles)
p1 = {"vis_left": 117.9, "vis_right": 267.8, "vis_top": 155.5, "leaf_bottom": 530.0,
      "mould_x": [136.7, 182.0, 205.8, 251.7], "mould_z": [175.8, 356.7, 397.5, 493.5],
      "band": [363.3, 378.7], "weather": [515.0, 529.0], "glass": [92.5, 144.0], "head_top": 81.0,
      "jamb_l": [108.5, 117.9], "jamb_r": [267.8, 279.0]}
vis_x0, vis_x1 = F["jamb_x_mm"]["left"][1], F["jamb_x_mm"]["right"][0]
s = (vis_x1 - vis_x0) / (p1["vis_right"] - p1["vis_left"])          # mm per px, fitted on the width only
def px_x(x): return p1["vis_left"] + (x - vis_x0) / s
def px_z(z): return p1["leaf_bottom"] - (z - L["z0_mm"]) / s
lap = M["outside_bolection"]["lap_over_framing_mm"]
o = P["openings_leaf_uv_mm"]
tx = [L["x0_mm"] + o["top_left"]["u0"] - lap, L["x0_mm"] + o["top_left"]["u1"] + lap,
      L["x0_mm"] + o["top_right"]["u0"] - lap, L["x0_mm"] + o["top_right"]["u1"] + lap]
tz = [L["z0_mm"] + o["top_left"]["v1"] + lap, L["z0_mm"] + o["top_left"]["v0"] - lap,
      L["z0_mm"] + o["bottom_left"]["v1"] + lap, L["z0_mm"] + o["bottom_left"]["v0"] - lap]
edges = [("leaf visible top (transom stop)", px_z(F["transom"]["z_stop_underside"]), p1["vis_top"])]
edges += [(f"panel moulding x edge {i+1}", px_x(a), b) for i, (a, b) in enumerate(zip(tx, p1["mould_x"]))]
edges += [(f"panel moulding z edge {i+1}", px_z(a), b) for i, (a, b) in enumerate(zip(tz, p1["mould_z"]))]
lb, wb = M["lock_rail_band"]["z_above_leaf_bottom_mm"], M["weatherboard"]["z_above_leaf_bottom_mm"]
edges += [("lock band top", px_z(L["z0_mm"] + lb[1]), p1["band"][0]), ("lock band bottom", px_z(L["z0_mm"] + lb[0]), p1["band"][1]),
          ("weatherboard top", px_z(L["z0_mm"] + wb[1]), p1["weather"][0]),
          ("glass top", px_z(F["fanlight"]["glass_sight_mm"]["z1"]), p1["glass"][0]),
          ("glass bottom", px_z(F["fanlight"]["glass_sight_mm"]["z0"]), p1["glass"][1]),
          ("head top (brick)", px_z(O["brick_height_mm"]), p1["head_top"]),
          ("left brick edge", px_x(0.0), p1["jamb_l"][0]), ("right brick edge", px_x(O["brick_width_mm"]), p1["jamb_r"][1])]
for name, pred, meas in edges:
    check("2 photo P1", name, abs(pred - meas) <= 2.5, f"target {pred:.1f} px, photo {meas:.1f} px, diff {pred-meas:+.1f} (allowed 2.5)")
vh = F["transom"]["z_stop_underside"] - L["z0_mm"]; vw = vis_x1 - vis_x0
fr = [  # name, target fraction, photo fraction, error
    ("visible height / visible width", vh / vw, (p1["leaf_bottom"] - p1["vis_top"]) / (p1["vis_right"] - p1["vis_left"]), 0.04),
    ("stile showing / visible width", (tx[0] - vis_x0) / vw, (p1["mould_x"][0] - p1["vis_left"]) / (p1["vis_right"] - p1["vis_left"]), 0.014),
    ("top rail showing / visible height", (F["transom"]["z_stop_underside"] - tz[0]) / vh, (p1["mould_z"][0] - p1["vis_top"]) / 374.5, 0.008),
    ("top panel (moulding) / visible height", (tz[0] - tz[1]) / vh, (p1["mould_z"][1] - p1["mould_z"][0]) / 374.5, 0.008),
    ("lock rail showing / visible height", (tz[1] - tz[2]) / vh, (p1["mould_z"][2] - p1["mould_z"][1]) / 374.5, 0.008),
    ("bottom panel (moulding) / visible height", (tz[2] - tz[3]) / vh, (p1["mould_z"][3] - p1["mould_z"][2]) / 374.5, 0.008),
    ("bottom rail showing / visible height", (tz[3] - L["z0_mm"]) / vh, (p1["leaf_bottom"] - p1["mould_z"][3]) / 374.5, 0.008),
    ("lock rail centre / visible height", (L["lock_rail_centre_above_leaf_bottom_mm"]) / vh, (p1["leaf_bottom"] - (p1["mould_z"][1] + p1["mould_z"][2]) / 2) / 374.5, 0.008),
]
for name, t, p, e in fr:
    check("2 photo P1 fraction", name, abs(t - p) <= e, f"target {t:.3f}, photo {p:.3f} +-{e}")
# P2 (Tottenham, door-photo-02, six panels; measured on a 619x1100 copy, edges +-3 px, sides +-10 px)
p2 = {"w": 317.0, "h": 755.0, "stile": 34.0, "bottom": 76.0}
check("2 photo P2 fraction", "visible height / visible width (six-panel door)", abs(vh / vw - p2["h"] / p2["w"]) <= 0.08,
      f"target {vh/vw:.3f}, photo {p2['h']/p2['w']:.3f} +-0.08 (P2 not used for numbers; six panels, sides uncertain)")
check("2 photo P2 fraction", "stile showing / visible width", abs((tx[0] - vis_x0) / vw - p2["stile"] / p2["w"]) <= 0.03,
      f"target {(tx[0]-vis_x0)/vw:.3f}, photo {p2['stile']/p2['w']:.3f} +-0.03")
check("2 photo P2 fraction", "bottom rail showing / visible height", abs((tz[3] - L["z0_mm"]) / vh - p2["bottom"] / p2["h"]) <= 0.01,
      f"target {(tz[3]-L['z0_mm'])/vh:.3f}, photo {p2['bottom']/p2['h']:.3f} +-0.01")

# ---- 4. internal consistency ----
W, H = L["width_mm"], L["height_mm"]
check("4 consistency", "stiles + muntin + panel openings = leaf width",
      near(2 * L["stile_mm"] + L["muntin_mm"] + (o["top_left"]["u1"] - o["top_left"]["u0"]) + (o["top_right"]["u1"] - o["top_right"]["u0"]), W),
      f"{2*L['stile_mm'] + L['muntin_mm'] + (o['top_left']['u1']-o['top_left']['u0']) + (o['top_right']['u1']-o['top_right']['u0']):.1f} vs {W}")
sumv = L["bottom_rail_mm"] + (o["bottom_left"]["v1"] - o["bottom_left"]["v0"]) + L["lock_rail_mm"] + (o["top_left"]["v1"] - o["top_left"]["v0"]) + L["top_rail_mm"]
check("4 consistency", "rails + panel openings = leaf height", near(sumv, H), f"{sumv:.1f} vs {H}")
check("4 consistency", "lock rail centred on its stated height",
      near((o["bottom_left"]["v1"] + o["top_left"]["v0"]) / 2, L["lock_rail_centre_above_leaf_bottom_mm"]), f"{(o['bottom_left']['v1']+o['top_left']['v0'])/2:.1f}")
check("4 consistency", "muntin centred on the leaf", near((o["top_left"]["u1"] + o["top_right"]["u0"]) / 2, W / 2), "")
pw = (o["top_left"]["u1"] - o["top_left"]["u0"]) + 2 * P["groove_depth_mm"] - P["side_play_mm"]
check("4 consistency", "panel width fits the grooves with the side play",
      pw < (o["top_left"]["u1"] - o["top_left"]["u0"]) + 2 * P["groove_depth_mm"] and pw > (o["top_left"]["u1"] - o["top_left"]["u0"]),
      f"panel {pw:.1f}, groove to groove {(o['top_left']['u1']-o['top_left']['u0']) + 2*P['groove_depth_mm']:.1f}")
check("4 consistency", "panel thinner than the leaf and centred", P["thickness_mm"] < L["thickness_mm"], f"{P['thickness_mm']} in {L['thickness_mm']}")
bw = M["outside_bolection"]["width_on_face_mm"]
check("4 consistency", "bolection leaves a field on every panel", min(o[k]["u1"] - o[k]["u0"] for k in o) - 2 * (bw - lap) > 100, "field width > 100")
check("4 consistency", "lock band lies on the lock rail", o["bottom_left"]["v1"] - lap <= lb[0] and lb[1] <= o["top_left"]["v0"] + lap, f"band {lb}, rail {o['bottom_left']['v1']}-{o['top_left']['v0']}")
check("4 consistency", "weatherboard lies on the bottom rail below the moulding", wb[1] <= o["bottom_left"]["v0"] - lap, f"{wb[1]} <= {o['bottom_left']['v0'] - lap:.1f}")
reb_l = F["jamb_x_mm"]["left"][1] - F["rebate_width_mm"]; reb_r = F["jamb_x_mm"]["right"][0] + F["rebate_width_mm"]
check("4 consistency", "leaf + two clearances = rebate to rebate", near(W + 2 * L["edge_clearance_mm"], reb_r - reb_l), f"{W + 2*L['edge_clearance_mm']:.1f} vs {reb_r - reb_l:.1f}")
check("4 consistency", "leaf starts one clearance from the left rebate", near(L["x0_mm"], reb_l + L["edge_clearance_mm"]), f"x0 {L['x0_mm']}")
check("4 consistency", "leaf thickness fits the rebate depth", L["thickness_mm"] < F["rebate_depth_mm"], f"{L['thickness_mm']} < {F['rebate_depth_mm']}")
check("4 consistency", "leaf face sits on the stop", near(L["outside_face_y_mm"], F["frame_outside_face_y_mm"] + F["stop_depth_mm"]), "")
check("4 consistency", "stop + rebate = frame depth", near(F["stop_depth_mm"] + F["rebate_depth_mm"], F["jamb_depth_mm"]), "")
check("4 consistency", "leaf top + clearance = transom rebate", near(L["z0_mm"] + H + L["edge_clearance_mm"], F["transom"]["rebate_underside_z"]), "")
check("4 consistency", "transom stop covers the leaf top by the rebate width", near(F["transom"]["rebate_underside_z"] - F["transom"]["z_stop_underside"], F["rebate_width_mm"]), "")
check("4 consistency", "leaf clears the sill", L["z0_mm"] > F["sill"]["top_z"], "")
check("4 consistency", "jamb showing past brick + hidden part = jamb face", near(F["jamb_showing_past_brick_mm"] - F["jamb_x_mm"]["left"][0], F["jamb_face_mm"]), "")
check("4 consistency", "brick opening = clear between stops + jambs showing", near(O["brick_width_mm"], O["clear_between_stops_mm"] + 2 * F["jamb_showing_past_brick_mm"]), "")
g = F["fanlight"]["glass_sight_mm"]
check("4 consistency", "glass sits on the transom and under the head", near(g["z0"], F["transom"]["z_top"]) and near(g["z1"], F["head_section_mm"]["z0"]), "")
check("4 consistency", "head showing below brick = brick head - head underside", near(O["brick_height_mm"] - F["head_section_mm"]["z0"], F["head_section_mm"]["showing_below_brick"]), "")
check("4 consistency", "frame face set back by the reveal", near(F["frame_outside_face_y_mm"], O["reveal_depth_mm"]), "")

npass = sum(r["pass"] for r in rows)
summary = f"{npass} of {len(rows)} checks pass"
T["self_check"] = {"run": "self_check.py, 8 Oct 2026", "summary": summary, "photo_scale_mm_per_px_P1": round(s, 3),
                   "failures": [r for r in rows if not r["pass"]], "rows": rows}
TP.write_text(json.dumps(T, indent=1, ensure_ascii=False), encoding="utf-8")
print(summary, "| P1 scale", round(s, 3), "mm/px")
print("| Group | Check | Result | Detail |\n|---|---|---|---|")
for r in rows:
    print(f"| {r['group']} | {r['check']} | {'pass' if r['pass'] else 'FAIL'} | {r['detail']} |")
