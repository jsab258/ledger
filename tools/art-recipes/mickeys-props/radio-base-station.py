"""The dispatcher's two-way radio for Mickey's front office: a late-1980s
desk-top base station of the usual kind (a vehicle transceiver clipped on top
of a mains power-supply housing that carries the loudspeaker), with its desk
microphone on a weighted stand and the coiled lead between them. Generic, no
maker's name, badge or layout.

    blender.exe -b --factory-startup -P tools/art-recipes/mickeys-props/radio-base-station.py [-- --no-render]

SIZES (read 6 October 2026):
- The form: Pye Museum, "Fixed Mobiles": desk-top stations of the 1980s were a
  mobile on a mains PSU (AC90PU 1984, "the mobile clipping onto the top of the
  PSU case"; PS900 1988; FM1000 1990 "small desk-top AC mains PSU"),
  https://www.pyemuseum.org/divisions/communications/pye_telecom/products/f_mobiles.php
- The transceiver: Philips FM1000 (1989-1998), 180 x 60 x 210 mm (W x H x D),
  https://www.radiomuseum.org/r/philips_vhfuhf_mobile_transceiver_fm1000_fm1100.html
- The desk microphone: Kenwood MC-60 desk microphone, base 170 x 160 mm with
  90 mm, microphone 170 mm long, https://www.rigpix.com/microphones/kenwood_mc60.htm
The power-supply housing is this recipe's own size (230 x 90 x 236 mm), a little
wider than the set it carries, as in the Pye description.
Origin: centre of the power-supply housing's feet, z = 0; front toward -Y.
The microphone stands in front of the set, to the right.
"""
import math
import os
import sys

from mathutils import Vector

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _desk_common as C  # noqa: E402


def build():
    C.reset()
    paint = C.material("radio_painted_metal", (0.20, 0.21, 0.215), 0.55)
    black = C.material("radio_black_plastic", (0.045, 0.045, 0.047), 0.42)
    red = C.material("radio_red_acrylic", (0.42, 0.03, 0.025), 0.08)

    # ---- power-supply housing with the loudspeaker -------------------------
    FY0, FY1 = -0.118, 0.118          # case front and back
    Z0, Z1 = 0.008, 0.098             # case bottom and top (feet below)
    C.box_z("psu_case", -0.115, 0.115, FY0, FY1, Z0, Z1, paint, bevel=0.0025, segs=3)
    for sx in (-1, 1):
        for sy in (-1, 1):
            C.cyl("foot", 0.009, 0.008, (sx * 0.095, sy * 0.098, 0.004), mat=black, segs=16,
                  bevel=0.0015)
    # front bezel, black, standing 3 mm proud of the case
    C.box_z("psu_bezel", -0.111, 0.111, FY0 - 0.003, FY0 + 0.004, Z0 + 0.006, Z1 - 0.006, black,
            bevel=0.0018, segs=2)
    # speaker grille: painted louvres over a recess in the bezel's left part
    C.box_z("grille_recess", -0.102, 0.034, FY0 - 0.0034, FY0 - 0.001, 0.022, 0.084, black,
            bevel=0.0008, segs=1)
    for i in range(9):
        z = 0.0255 + i * 0.0068
        C.box_z("louvre", -0.100, 0.032, FY0 - 0.0062, FY0 - 0.0028, z, z + 0.0040, paint,
                bevel=0.0012, segs=2)
    # mains rocker, pilot lamp and transmit lamp at the right of the bezel
    C.box_z("rocker_frame", 0.058, 0.090, FY0 - 0.0055, FY0 - 0.002, 0.044, 0.064, black,
            bevel=0.0012, segs=2)
    C.box("rocker", (0.026, 0.006, 0.014), (0.074, FY0 - 0.0068, 0.054), black,
          rot=(math.radians(8), 0, 0), bevel=0.0015, segs=2)
    C.cyl("pilot", 0.0032, 0.004, (0.064, FY0 - 0.0045, 0.031), (math.pi / 2, 0, 0), red, segs=16,
          bevel=0.0008)
    C.cyl("tx_lamp", 0.0032, 0.004, (0.084, FY0 - 0.0045, 0.031), (math.pi / 2, 0, 0), red, segs=16,
          bevel=0.0008)
    # vent slots along the top rear of the case
    for i in range(7):
        x = -0.072 + i * 0.024
        C.box_z("vent", x - 0.008, x + 0.008, 0.050, 0.104, Z1 - 0.0004, Z1 + 0.0012, black,
                bevel=0.0006, segs=1)

    # ---- the transceiver, clipped into a cradle on top ----------------------
    TW, TH, TD = 0.180, 0.060, 0.210
    ty0 = FY0 + 0.004                 # its front face sits 4 mm behind the bezel
    tz0 = Z1 + 0.004                  # on rubber pads
    for sx in (-1, 1):
        for sy in (-1, 1):
            C.box_z("pad", sx * 0.070 - 0.010, sx * 0.070 + 0.010, ty0 + 0.05 + (sy + 1) * 0.05,
                    ty0 + 0.07 + (sy + 1) * 0.05, Z1, tz0, black)
    C.box_z("trx_body", -TW / 2 + 0.002, TW / 2 - 0.002, ty0 + 0.012, ty0 + TD, tz0, tz0 + TH - 0.004,
            paint, bevel=0.003, segs=3)
    # cast fins over the rear two thirds of the top
    for i in range(13):
        x = -0.072 + i * 0.012
        C.box_z("fin", x - 0.0014, x + 0.0014, ty0 + 0.075, ty0 + TD - 0.006, tz0 + TH - 0.006,
                tz0 + TH, paint, bevel=0.0007, segs=2)
    # front control panel
    fz = tz0 + TH / 2 - 0.002
    C.box_z("trx_panel", -TW / 2, TW / 2, ty0, ty0 + 0.014, tz0 - 0.001, tz0 + TH - 0.003, black,
            bevel=0.0025, segs=3)
    py = ty0 - 0.0002
    # volume and squelch knobs with skirts and pointer lines
    for name, x, r in (("volume", -0.062, 0.0115), ("squelch", -0.030, 0.0085)):
        C.cyl(name + "_skirt", r + 0.0022, 0.003, (x, py - 0.0015, fz), (math.pi / 2, 0, 0), black,
              segs=32, bevel=0.0008)
        C.cyl(name, r, 0.014, (x, py - 0.010, fz), (math.pi / 2, 0, 0), black, segs=32,
              r2=r * 0.94, bevel=0.0015)
        C.box(name + "_line", (0.0016, 0.0012, r * 0.8), (x, py - 0.0173, fz + r * 0.45), red,
              rot=(0, math.radians(-35 if name == "volume" else 20), 0))
    # channel readout: a red window with the channel switch beside it
    C.box_z("display_bezel", 0.000, 0.044, py - 0.0016, py + 0.001, fz - 0.0115, fz + 0.0115, black,
            bevel=0.001, segs=2)
    C.box_z("display", 0.003, 0.041, py - 0.0024, py - 0.0004, fz - 0.0085, fz + 0.0085, red,
            bevel=0.0008, segs=1)
    for dz in (0.007, -0.007):
        C.box_z("ch_key", 0.050, 0.064, py - 0.005, py, fz + dz - 0.005, fz + dz + 0.005, paint,
                bevel=0.0014, segs=2)
    # microphone socket at the right, with the lead's plug in it
    C.cyl("mic_socket", 0.0075, 0.003, (0.077, py - 0.0012, fz), (math.pi / 2, 0, 0), paint,
          segs=24, bevel=0.0007)
    C.cyl("mic_plug", 0.0062, 0.022, (0.077, py - 0.013, fz), (math.pi / 2, 0, 0), black,
          segs=24, r2=0.0050, bevel=0.0012)
    # cradle: side plates on the case with knurled thumbscrews into the set
    for sx in (-1, 1):
        x = sx * (TW / 2 + 0.0035)
        C.box_z("cradle", x - 0.0015, x + 0.0015, ty0 + 0.050, ty0 + 0.150, Z1 - 0.012, tz0 + 0.042,
                paint, bevel=0.0010, segs=2)
        C.cyl("thumbscrew", 0.0105, 0.009, (x + sx * 0.006, ty0 + 0.100, tz0 + 0.026),
              (0, math.pi / 2, 0), black, segs=24, bevel=0.0012)
        C.cyl("thumbscrew_cap", 0.0060, 0.004, (x + sx * 0.0115, ty0 + 0.100, tz0 + 0.026),
              (0, math.pi / 2, 0), paint, segs=20, bevel=0.0008)

    # ---- the desk microphone on its weighted stand --------------------------
    mx, my, mrot = 0.105, -0.270, math.radians(14)
    M = C.mat4((mx, my, 0), (0, 0, mrot))

    def mpt(x, y, z):
        return M @ Vector((x, y, z))
    BW, BD = 0.170, 0.160
    # base: a low wedge, 30 mm at the front rising to 50 mm at the back
    wedge = [(-BD / 2, 0.003), (BD / 2, 0.003), (BD / 2, 0.050), (-BD / 2, 0.030)]
    C.extrude_profile("mic_base", wedge, -BW / 2, BW / 2, paint, plane="YZ")
    base = C.PARTS[-1]
    base.data.transform(M)
    C.bevel_part(base, 0.006, 3, angle=25)
    for sx in (-1, 1):
        for sy in (-1, 1):
            C.cyl("mic_foot", 0.008, 0.003, mpt(sx * 0.068, sy * 0.062, 0.0015)[:], mat=black, segs=16)
    # press-to-talk bar along the front slope, and a lock lever beside it
    C.box("ptt_bar", (0.120, 0.022, 0.010), mpt(0.0, -0.058, 0.034)[:], black,
          rot=(math.radians(9), 0, mrot), bevel=0.003, segs=2)
    C.box("lock_lever", (0.012, 0.018, 0.008), mpt(0.072, -0.052, 0.035)[:], paint,
          rot=(math.radians(9), 0, mrot), bevel=0.002, segs=2)
    # stalk, swivel and the microphone head tipped toward the speaker
    sb = mpt(0.0, 0.045, 0.044)
    C.cyl("stalk_collar", 0.011, 0.010, (sb + Vector((0, 0, 0.005)))[:], mat=black, segs=24,
          bevel=0.0015)
    STALK = 0.109                               # stalk + head = the MC-60's 170 mm
    C.cyl("stalk", 0.0055, STALK, (sb + Vector((0, 0, 0.005 + STALK / 2)))[:], mat=paint, segs=20)
    top = sb + Vector((0, 0, 0.005 + STALK))
    C.cyl("swivel", 0.009, 0.016, top[:], (0, math.pi / 2, mrot), black, segs=20, bevel=0.002)
    tilt = math.radians(62)                     # head axis tipped forward from vertical
    axis = Vector((0, -math.sin(tilt), math.cos(tilt)))
    axis.rotate(C.mat4((0, 0, 0), (0, 0, mrot)).to_3x3())
    hc = top + axis * 0.030
    rot_q = axis.to_track_quat("Z", "Y").to_euler()
    C.cyl("mic_head", 0.021, 0.056, hc[:], rot_q[:], black, segs=32, r2=0.024, bevel=0.003, bsegs=3)
    C.cyl("mic_grille_ring", 0.0255, 0.006, (hc + axis * 0.028)[:], rot_q[:], paint, segs=32,
          bevel=0.0012)
    C.cyl("mic_grille", 0.0215, 0.003, (hc + axis * 0.0305)[:], rot_q[:], black, segs=32,
          bevel=0.0008)
    head_far = hc + axis * 0.032
    mic_len = STALK + (head_far - top).length       # collar top to grille face
    mic_base = (BW, BD)

    # ---- the coiled lead from the microphone base to the set -----------------
    exitp = mpt(0.030, BD / 2 + 0.004, 0.020)
    plug_end = Vector((0.077, py - 0.024, fz))
    straight_a = [mpt(0.030, BD / 2 - 0.010, 0.020), exitp, mpt(0.034, BD / 2 + 0.016, 0.012)]
    coil_path = C.catmull([straight_a[-1], mpt(0.042, BD / 2 + 0.040, 0.0065),
                           Vector((0.128, -0.150, 0.0065)), Vector((0.124, -0.134, 0.030)),
                           Vector((0.104, -0.136, 0.070)), Vector((0.086, py - 0.034, fz - 0.010))],
                          per_seg=10)
    pts = C.coil(coil_path, coil_r=0.0042, pitch=0.0052, step=0.0052 / 8, floor_z=0.0016)
    C.tube("lead_coil", pts, 0.0015, sides=5, mat=black, caps=True)
    C.tube("lead_tail_a", C.resample(C.catmull(straight_a, 4), 0.003)[0], 0.0022, sides=8, mat=black)
    tail_b = C.resample(C.catmull([Vector((0.086, py - 0.034, fz - 0.010)),
                                   Vector((0.080, py - 0.028, fz - 0.002)), plug_end], 4), 0.003)[0]
    C.tube("lead_tail_b", tail_b, 0.0022, sides=8, mat=black)
    for ob in C.PARTS:
        if ob.name.startswith("lead"):
            ob["no_wn"] = True
            ob["sharp_angle"] = 89.0
        if ob.name.startswith(("fin", "louvre", "vent")):
            ob["no_dense"] = True       # many small repeats; ends not buried

    # measurement of the transceiver alone (body + panel), before joining
    trx = [o for o in C.PARTS if o.name.startswith(("trx_body", "trx_panel", "fin"))]
    lo = Vector((1, 1, 1))
    hi = Vector((-1, -1, -1))
    for o in trx:
        for v in o.data.vertices:
            lo = Vector((min(lo.x, v.co.x), min(lo.y, v.co.y), min(lo.z, v.co.z)))
            hi = Vector((max(hi.x, v.co.x), max(hi.y, v.co.y), max(hi.z, v.co.z)))
    trx_size = hi - lo

    o = C.cli()
    ob, info = C.finish_prop("radio-base-station", "radio_base_station", ao_distance=0.04,
                             edge_span=0.10, render=o["render"],
                             preview_kw={"azimuth": -34, "elevation": 24, "fill": 0.95})
    info["transceiver_vs_FM1000"] = {
        "model_m": [round(trx_size.x, 4), round(trx_size.z, 4), round(trx_size.y, 4)],
        "ref_m": [TW, TH, TD],
        "diff_pct": [round(100 * (a - b) / b, 2) for a, b in
                     zip((trx_size.x, trx_size.z, trx_size.y), (TW, TH, TD))]}
    info["desk_mic_vs_MC60"] = {"base_model_m": list(mic_base), "base_ref_m": [0.170, 0.160],
                                "length_model_m": round(mic_len, 4), "length_ref_m": 0.170,
                                "length_diff_pct": round(100 * (mic_len - 0.170) / 0.170, 2)}
    C.report("radio-base-station", info)


if __name__ == "__main__":
    build()
