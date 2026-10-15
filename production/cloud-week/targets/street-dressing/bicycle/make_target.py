"""bicycle: writes target.json and TARGET.md (cloud week 42, unit 13, family 7: an adult's roadster leaning on a wall)."""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import sd_lib as L
import sd_family as SF
from sd_lib import B, CY

FAMILY = "bicycle"
R, TS = 330.0, 38.0            # wheel outer radius (26 x 1 3/8: a 660 mm tyre), tyre section
NSEG = 16
HEAD = math.radians(68.0)
SEAT = math.radians(72.0)
Z_AXLE = R
BB = (449.0, 300.0)
SEAT_TOP = (BB[0] - 560.0 * math.cos(SEAT), BB[1] + 560.0 * math.sin(SEAT))
HT1 = (SEAT_TOP[0] + 570.0, SEAT_TOP[1] + 7.0)
HT2 = (HT1[0] + 150.0 * math.cos(HEAD), HT1[1] - 150.0 * math.sin(HEAD))
RAKE = 45.0
FX = HT2[0] + (HT2[1] - Z_AXLE) / math.tan(HEAD) + RAKE      # the front axle's x = the wheelbase
STEM_TOP = (HT1[0] - 170.0 * math.cos(HEAD), HT1[1] + 170.0 * math.sin(HEAD))
# the parts the review of 13 October found missing (each a Judgement unless said): the drive, the guard, the rims, the brakes, the carrier
PITCH = 12.7                         # a 1/2 inch roller chain
N_RING, N_SPR = 44, 18               # teeth: the 44 tooth chainring (pitch circle 180) and the 18 tooth rear sprocket (73 across)
R_RING = PITCH / (2.0 * math.sin(math.pi / N_RING))     # 88.9
R_SPR = PITCH / (2.0 * math.sin(math.pi / N_SPR))       # 36.6
CH_Y, CH_W, CH_T = 55.0, 8.0, 6.0    # the chain line (the chainring's plane), the chain's width and thickness
STAY_Y = 40.0                        # the chain and seat stays stand 40 off the centre line (their outer face 48), so the chain, sprocket and ring run outboard of them
RIM_W, RIM_D = 25.0, 10.0            # rim width and depth (radial), its own ring inside the tyre
GUARD_DEPTH, GUARD_T, GUARD_GAP = 60.0, 1.0, 13.0       # chainguard: 60 deep, 1 thick, 13 mm over the chain's pitch line
LEVER_L, ROD_D = 120.0, 8.0          # bar levers 120 long, rods 8 across
CARRIER_X = (-101.0, 239.0)          # the carrier's platform: 340 long ...
CARRIER_W, CARRIER_Z = 130.0, 780.0  # ... 130 wide, at 780 above the ground
LEAN = 12.0


def tube(id, a, b, r, mat, y=0.0, **kw):
    return CY(id, (a[0], y, a[1]), (b[0], y, b[1]), r, mat, **kw)


def wheel(tag, cx):
    P = []
    rc = R - TS / 2
    ch = 2 * rc * math.tan(math.pi / NSEG)
    for k in range(NSEG):
        a = 2 * math.pi * k / NSEG
        c = [cx + rc * math.cos(a), 0.0, Z_AXLE + rc * math.sin(a)]
        P.append({"id": "%s_tyre%d" % (tag, k + 1), "type": "box", "c": [round(v, 2) for v in c], "s": [round(ch, 1), TS, TS], "rot": [0, -(math.degrees(a) + 90.0), 0], "material": "tyre",
                  "note": "tyre and rim segment (16 round the wheel), section 38 x 38"})
    # the rim: its own ring of 16 segments inside the tyre, 25 wide and 10 deep (radial), its outer face at the tyre's inner face (292)
    rr = R - TS - RIM_D / 2.0
    rch = 2 * rr * math.tan(math.pi / NSEG)
    for k in range(NSEG):
        a = 2 * math.pi * k / NSEG
        c = [cx + rr * math.cos(a), 0.0, Z_AXLE + rr * math.sin(a)]
        P.append({"id": "%s_rim%d" % (tag, k + 1), "type": "box", "c": [round(v, 2) for v in c], "s": [round(rch, 1), RIM_W, RIM_D], "rot": [0, -(math.degrees(a) + 90.0), 0], "material": "steel",
                  "note": "rim segment (16 round the wheel): 25 wide, 10 deep, dull steel, the tyre's seat; Judgement"})
    P.append(CY("%s_hub" % tag, (cx, -50.0, Z_AXLE), (cx, 50.0, Z_AXLE), 22.0, "steel", note="hub 44 across, 100 long"))
    for k in range(8):
        a = 2 * math.pi * (k + 0.5) / 8
        r0, r1 = 24.0, R - TS - 2.0
        P.append(CY("%s_spoke%d" % (tag, k + 1), (cx + r0 * math.cos(a), 0.0, Z_AXLE + r0 * math.sin(a)), (cx + r1 * math.cos(a), 0.0, Z_AXLE + r1 * math.sin(a)), 1.2, "steel", note="spoke 2.4 across (8 drawn of 36)"))
    return P


def guard(tag, cx, a0, a1):
    P = []
    n = 5
    rg = R + 8.0
    chord = 2 * rg * math.tan(math.radians((a1 - a0) / n / 2)) + 2.0
    for k in range(n):
        a = math.radians(a0 + (k + 0.5) * (a1 - a0) / n)
        P.append({"id": "%s_guard%d" % (tag, k + 1), "type": "box", "c": [round(cx + rg * math.cos(a), 2), 0.0, round(Z_AXLE + rg * math.sin(a), 2)], "s": [round(chord, 1), 60.0, 2.0], "rot": [0, -(math.degrees(a) + 90.0), 0], "material": "paint_black",
                  "note": "mudguard segment, 60 wide, 2 thick"})
    return P


def bike():
    P = []
    P += wheel("rw", 0.0) + wheel("fw", FX)
    P += guard("rw", 0.0, 20.0, 160.0) + guard("fw", FX, 20.0, 150.0)
    P.append(tube("seat_tube", BB, SEAT_TOP, 14.0, "paint_black", note="seat tube 28 across, 560 centre to top, 72 degrees"))
    P.append(tube("top_tube", SEAT_TOP, HT1, 14.0, "paint_black", note="top tube 28, 570 long, level"))
    P.append(tube("down_tube", BB, HT2, 15.0, "paint_black", note="down tube 30"))
    P.append(tube("head_tube", HT2, HT1, 18.0, "paint_black", note="head tube 36 across, 150 long, 68 degrees"))
    for s, y in (("l", -STAY_Y), ("r", STAY_Y)):
        P.append(tube("chain_stay_%s" % s, BB, (0.0, Z_AXLE), 8.0, "paint_black", y=y, note="chain stay 16, 450 long, 40 off the centre line (80 apart): the chain runs outboard of the right one"))
        P.append(tube("seat_stay_%s" % s, SEAT_TOP, (0.0, Z_AXLE), 8.0, "paint_black", y=y, note="seat stay 16"))
    for s, y in (("l", -55.0), ("r", 55.0)):
        P.append(tube("fork_%s" % s, HT2, (FX, Z_AXLE), 11.0, "paint_black", y=y * 1.05, note="fork blade 22, rake 45 at the foot"))
    P.append(B("seat_bridge", SEAT_TOP[0] - 8, SEAT_TOP[0] + 8, -STAY_Y - 5.0, STAY_Y + 5.0, SEAT_TOP[1] - 10, SEAT_TOP[1] + 10, "paint_black", note="seat-stay bridge"))
    P.append(B("fork_crown", HT2[0] - 12, HT2[0] + 12, -62.0, 62.0, HT2[1] - 30, HT2[1] - 6, "paint_black", note="fork crown"))
    P.append(CY("seat_post", (SEAT_TOP[0], 0.0, SEAT_TOP[1]), (SEAT_TOP[0] - 45.0, 0.0, 985.0), 11.0, "steel", note="seat post 22"))
    P.append(B("saddle", SEAT_TOP[0] - 45.0 - 150.0, SEAT_TOP[0] - 45.0 + 130.0, -90.0, 90.0, 985.0, 1035.0, "saddle_black", edge="nose r 30, edges r 8", note="saddle 280 x 180 x 50, leather-look, springs not modelled"))
    P.append(tube("stem", HT1, STEM_TOP, 11.0, "steel", note="stem 22, 170 above the head tube"))
    P.append(CY("bar_mid", (STEM_TOP[0], -190.0, STEM_TOP[1]), (STEM_TOP[0], 190.0, STEM_TOP[1]), 11.0, "steel", note="handlebar: the straight middle, 22 across, 380 wide"))
    for s, y in (("l", -1.0), ("r", 1.0)):
        P.append(CY("bar_sweep_%s" % s, (STEM_TOP[0], y * 190.0, STEM_TOP[1]), (STEM_TOP[0] - 85.0, y * 290.0, STEM_TOP[1] + 12.0), 11.0, "steel", note="swept-back end, 100 across to 580 over the grips"))
        P.append(CY("grip_%s" % s, (STEM_TOP[0] - 85.0, y * 290.0, STEM_TOP[1] + 12.0), (STEM_TOP[0] - 90.0, y * 395.0, STEM_TOP[1] + 14.0), 14.0, "grip_black", note="grip 28 across, 105 long"))
    P.append(CY("bell", (STEM_TOP[0] + 5.0, -150.0, STEM_TOP[1] + 14.0), (STEM_TOP[0] + 5.0, -150.0, STEM_TOP[1] + 40.0), 26.0, "steel", note="bell 52 across, a plain dome"))
    P.append(CY("bb_spindle", (BB[0], -70.0, BB[1]), (BB[0], 70.0, BB[1]), 12.0, "steel", note="bottom bracket spindle"))
    P.append(CY("chainring", (BB[0], 52.0, BB[1]), (BB[0], 58.0, BB[1]), 90.0, "steel", note="chainring 180 across, 6 thick (the chainguard is not modelled)"))
    P.append(B("crank_r", BB[0] - 10.0, BB[0] + 170.0, 58.0, 70.0, BB[1] - 10.0, BB[1] + 10.0, "steel", note="right crank arm 170 long"))
    P.append(B("crank_l", BB[0] - 170.0, BB[0] + 10.0, -70.0, -58.0, BB[1] - 10.0, BB[1] + 10.0, "steel", note="left crank arm 170 long"))
    P.append(B("pedal_r", BB[0] + 100.0, BB[0] + 200.0, 70.0, 175.0, BB[1] - 12.0, BB[1] + 12.0, "steel", note="pedal 100 x 105 x 24, rubber blocks not modelled"))
    P.append(B("pedal_l", BB[0] - 200.0, BB[0] - 100.0, -175.0, -70.0, BB[1] - 12.0, BB[1] + 12.0, "steel"))
    return P


def _unit(v):
    n = math.hypot(*v)
    return (v[0] / n, v[1] / n)


def _seg(id, a, b, y, w, t, mat, off=0.0, **kw):
    """A strip in the x-z plane from a to b (width w along y, thickness t across the strip), its centre line shifted by off along the strip's left normal."""
    dx, dz = b[0] - a[0], b[1] - a[1]
    L_ = math.hypot(dx, dz)
    ux, uz = dx / L_, dz / L_
    nx, nz = -uz, ux
    cx_, cz_ = (a[0] + b[0]) / 2.0 + off * nx, (a[1] + b[1]) / 2.0 + off * nz
    phi = math.degrees(math.atan2(dz, dx))
    d = {"id": id, "type": "box", "c": [round(cx_, 2), y, round(cz_, 2)], "s": [round(L_, 2), w, t], "rot": [0, -phi, 0], "material": mat}
    d.update(kw)
    return d


def chain_geometry():
    """The pitch-circle geometry of the drive, in one place (the self-check recomputes it from the parts)."""
    c1, c2 = BB, (0.0, Z_AXLE)
    d = math.hypot(c1[0] - c2[0], c1[1] - c2[1])
    u = ((c1[0] - c2[0]) / d, (c1[1] - c2[1]) / d)
    perp = (-u[1], u[0])
    k = -(R_RING - R_SPR) / d
    cc = math.sqrt(1 - k * k)
    n_top = (k * u[0] + cc * perp[0], k * u[1] + cc * perp[1])
    n_bot = (k * u[0] - cc * perp[0], k * u[1] - cc * perp[1])
    th_top = math.atan2(n_top[1], n_top[0])
    th_bot = math.atan2(n_bot[1], n_bot[0])
    if th_top < th_bot:
        th_top += 2 * math.pi
    return dict(c1=c1, c2=c2, d=d, n_top=n_top, n_bot=n_bot, th_top=th_top, th_bot=th_bot,
                run=math.sqrt(d * d - (R_RING - R_SPR) ** 2), ring_span=th_top - th_bot, spr_span=2 * math.pi - (th_top - th_bot))


def drive():
    """The chain (geometry on the pitch circles), the rear sprocket, the chainguard and its fixings."""
    P = []
    G = chain_geometry()
    c1, c2 = G["c1"], G["c2"]
    P.append(CY("sprocket", (0.0, CH_Y - 7.0, Z_AXLE), (0.0, CH_Y + 3.0, Z_AXLE), 36.5, "steel",
                note="rear sprocket: 18 teeth, 73 across (pitch circle %.1f), 10 thick, on the hub's drive end; Judgement (the review's 18 tooth, 73 mm)" % (2 * R_SPR)))
    runs = {}
    for nm, n in (("top", G["n_top"]), ("bot", G["n_bot"])):
        a = (c2[0] + R_SPR * n[0], c2[1] + R_SPR * n[1])
        b = (c1[0] + R_RING * n[0], c1[1] + R_RING * n[1])
        runs[nm] = (a, b)
        P.append(_seg("chain_%s" % nm, a, b, CH_Y, CH_W, CH_T, "chain_dark", note="chain run (%s): %.1f long = %.1f links of 12.7, 8 wide, 6 thick, on the pitch circles' common tangent; Judgement" % (nm, math.dist(a, b), math.dist(a, b) / PITCH)))

    def wrap(tag, cen, rad, a0, a1, n):
        out = []
        for j in range(n):
            t0 = a0 + (a1 - a0) * j / n
            t1 = a0 + (a1 - a0) * (j + 1) / n
            p0 = (cen[0] + rad * math.cos(t0), cen[1] + rad * math.sin(t0))
            p1 = (cen[0] + rad * math.cos(t1), cen[1] + rad * math.sin(t1))
            out.append(_seg("chain_%s%02d" % (tag, j + 1), p0, p1, CH_Y, CH_W, CH_T, "chain_dark",
                            note="chain on the %s: %.1f links of 12.7 in this strip; Judgement" % ("chainring" if tag == "c" else "sprocket", rad * abs(a1 - a0) / n / PITCH)))
        return out
    P += wrap("c", c1, R_RING, G["th_bot"], G["th_top"], 14)
    P += wrap("s", c2, R_SPR, G["th_top"], G["th_bot"] + 2 * math.pi, 12)
    # the chainguard: sheet steel over the top run, 60 deep, 1 thick, from the sprocket's centre to 40 mm behind the chainring's front, 13 over the pitch line
    ta, tb = runs["top"]
    x_front = BB[0] + 90.0 - 40.0

    def on_run(x):
        t = (x - ta[0]) / (tb[0] - ta[0])
        return (x, ta[1] + (tb[1] - ta[1]) * t)
    ga, gb = on_run(0.0), on_run(x_front)
    P.append(_seg("chainguard", ga, gb, CH_Y, GUARD_DEPTH, GUARD_T, "paint_black", off=GUARD_GAP, edge="edges rolled 3 mm",
                  note="chainguard: sheet steel 60 deep, 1 thick, from the sprocket's centre (x 0) to x %.0f (40 mm behind the chainring's front), %d over the chain's pitch line; Judgement (the review's numbers)" % (x_front, GUARD_GAP)))
    stay_top = Z_AXLE - 30.0 * (15.0 / 449.0) + 8.0
    gz = on_run(15.0)[1] + GUARD_GAP - GUARD_T
    P.append(B("chainguard_clip", 8.0, 22.0, STAY_Y - 4.0, STAY_Y + 4.0, stay_top - 1.0, gz + 1.0, "paint_black", note="clip 14 x 8 from the right chain stay up to the guard's rear end"))
    zf = on_run(x_front)[1] + GUARD_GAP - GUARD_T
    seat_x = BB[0] - (zf - 20.0 - BB[1]) / math.tan(SEAT)
    P.append(CY("chainguard_strap", (x_front - 4.0, 36.0, zf), (seat_x + 10.0, 10.0, zf - 20.0), 3.0, "paint_black", note="strap rod 6 across from the guard's front end to the seat tube"))
    return P


def stirrup(tag, cx, m0, m1, y_m):
    """A rod brake's stirrup under the rim: the frame member (m0 to m1, at y = +-y_m) meets the wheel's 360 radius at a point M; the stirrup's
    crossbar (6 across, 56 wide) lies under the rim at radius 270 on the same radius line; two arms run from its ends to the member on each
    side; a bridge joins the two members at M, above the tyre and its mudguard (radius 360); two pads 40 x 14 x 14 sit on the crossbar against the rim's inner face (282)."""
    P = []
    a = (m0[0] - cx, m0[1] - Z_AXLE)
    b = (m1[0] - cx, m1[1] - Z_AXLE)
    dx, dz = b[0] - a[0], b[1] - a[1]
    Ln = math.hypot(dx, dz)
    dx, dz = dx / Ln, dz / Ln
    B_ = 2 * (a[0] * dx + a[1] * dz)
    C_ = a[0] ** 2 + a[1] ** 2 - 360.0 ** 2
    disc = B_ * B_ - 4 * C_
    t = (-B_ + math.sqrt(disc)) / 2.0
    if t < 0 or t > Ln:
        t = (-B_ - math.sqrt(disc)) / 2.0
    M = (a[0] + t * dx, a[1] + t * dz)
    ang = math.atan2(M[1], M[0])
    ca, sa = math.cos(ang), math.sin(ang)
    Mx, Mz = cx + M[0], Z_AXLE + M[1]
    Cx, Cz = cx + 270.0 * ca, Z_AXLE + 270.0 * sa
    P.append(CY("%s_stirrup_bar" % tag, (Cx, -28.0, Cz), (Cx, 28.0, Cz), 3.0, "steel", note="stirrup crossbar 6 across, 56 wide, under the rim at radius 270 (the rim's inner face is 282), at %.1f degrees on the wheel; Judgement" % math.degrees(ang)))
    for sd, y in (("l", -1.0), ("r", 1.0)):
        P.append(CY("%s_stirrup_arm_%s" % (tag, sd), (Cx, y * 28.0, Cz), (Mx, y * y_m, Mz), 3.0, "steel", note="stirrup arm 6 across from the crossbar's end to the frame member"))
    P.append(B("%s_brake_bridge" % tag, Mx - 8.0, Mx + 8.0, -y_m, y_m, Mz - 8.0, Mz + 8.0, "paint_black", note="brake bridge 16 x 16 between the two members at radius 360, above the mudguard"))
    for sd, y in (("l", -12.0), ("r", 12.0)):
        pr = 274.0
        Px, Pz = cx + pr * ca, Z_AXLE + pr * sa
        P.append({"id": "%s_pad_%s" % (tag, sd), "type": "box", "c": [round(Px, 2), y, round(Pz, 2)], "s": [40.0, 14.0, 14.0], "rot": [0, -(math.degrees(ang) + 90.0), 0], "material": "grip_black",
                  "note": "brake pad 40 x 14 x 14 on the stirrup, against the rim's inner face (rod brake); Judgement"})
    return P, (Mx, Mz, y_m)


def brakes():
    """Roadster rod brakes: two 120 mm bar levers, two 8 mm rods, a stirrup under each rim (the review's list)."""
    P = []
    pf, mf = stirrup("fw", FX, HT2, (FX, Z_AXLE), 55.0)
    pr, mr = stirrup("rw", 0.0, SEAT_TOP, (0.0, Z_AXLE), STAY_Y)
    P += pf + pr
    ang = math.radians(-35.0)
    for sd, y in (("l", -1.0), ("r", 1.0)):
        gx, gz = STEM_TOP[0] - 87.0, STEM_TOP[1] + 13.0
        p0 = (gx, y * 330.0, gz - 14.0)
        p1 = (gx + LEVER_L * math.cos(ang), y * 330.0, gz - 14.0 + LEVER_L * math.sin(ang))
        P.append(CY("brake_lever_%s" % sd, p0, p1, 6.0, "steel", note="bar lever 120 long, 12 across, clamped under the grip's inner end; the left works the front brake, the right the rear; Judgement"))
        tgt = mf if sd == "l" else mr
        P.append(CY("brake_rod_%s" % ("f" if sd == "l" else "r"), p1, (tgt[0], y * tgt[2], tgt[1]), ROD_D / 2.0, "steel", note="brake rod 8 across from the lever's tip to the stirrup's joint on the %s; Judgement" % ("fork blade" if sd == "l" else "seat stay")))
    return P


def guards_extra():
    """Two 5 mm stays per mudguard to the drop-outs, and the red reflector on the rear mudguard."""
    P = []
    rg = R + 8.0
    for tag, cx, a0, a1, which in (("fw", FX, 20.0, 150.0, "lo"), ("rw", 0.0, 20.0, 160.0, "hi")):
        # the free end of the end strip: the strip is a flat plate tangent at its middle, so its end lies on the tangent, off the circle
        n_ = 5
        j = 0 if which == "lo" else n_ - 1
        am = math.radians(a0 + (j + 0.5) * (a1 - a0) / n_)
        chord = 2 * rg * math.tan(math.radians((a1 - a0) / n_ / 2)) + 2.0
        sgn = -1.0 if which == "lo" else 1.0
        gx = cx + rg * math.cos(am) + sgn * (chord / 2.0 - 2.0) * (-math.sin(am))
        gz = Z_AXLE + rg * math.sin(am) + sgn * (chord / 2.0 - 2.0) * math.cos(am)
        for sd, y in (("l", -1.0), ("r", 1.0)):
            P.append(CY("%s_guard_stay_%s" % (tag, sd), (gx, y * 28.0, gz), (cx, y * 57.0, Z_AXLE), 2.5, "paint_black", note="mudguard stay 5 across from the guard's %s end to the drop-out; Judgement" % ("front" if tag == "fw" else "rear")))
    am = math.radians(20.0 + 4.5 * (160.0 - 20.0) / 5.0)
    chord = 2 * rg * math.tan(math.radians((160.0 - 20.0) / 5 / 2)) + 2.0
    rx = rg * math.cos(am) - (chord / 2.0 - 2.0) * (-math.sin(am))
    rz = Z_AXLE + rg * math.sin(am) - (chord / 2.0 - 2.0) * math.cos(am)
    P.append(CY("rw_reflector", (rx + 1.0, 0.0, rz), (rx - 5.0, 0.0, rz), 30.0, "reflector_red", note="rear reflector 60 across, 6 thick, on the rear mudguard's tail, facing back; Judgement"))
    return P


def carrier():
    """The rear carrier S1's own row lists: a 340 x 130 platform of 10 mm tube at 780 over the rear wheel, two stays to the drop-outs."""
    P = []
    x0, x1 = CARRIER_X
    z0 = CARRIER_Z
    hw = CARRIER_W / 2.0
    P.append(B("carrier_deck", x0, x1, -hw, hw, z0 - 4.0, z0, "paint_black", note="carrier platform 340 x 130, a 4 mm sheet on the tube frame, top at 780; Judgement"))
    for sd, y in (("l", -hw), ("r", hw)):
        P.append(CY("carrier_rail_%s" % sd, (x0, y, z0 - 9.0), (x1, y, z0 - 9.0), 5.0, "paint_black", note="carrier side rail, 10 mm tube, 340 long"))
    P.append(CY("carrier_cross_rear", (x0, -hw, z0 - 9.0), (x0, hw, z0 - 9.0), 5.0, "paint_black", note="carrier rear cross rail, 10 mm tube"))
    for sd, y in (("l", -1.0), ("r", 1.0)):
        P.append(CY("carrier_stay_%s" % sd, (x0, y * hw, z0 - 9.0), (-42.0, y * 57.0, Z_AXLE + 10.0), 5.0, "paint_black", note="carrier stay, 10 mm tube, from the rail's rear end to the drop-out; Judgement"))
    return P


def extras():
    return drive() + brakes() + guards_extra() + carrier()


def build():
    P1 = bike() + extras()
    # the leaning variant: the same parts rolled 12 degrees about the line of the two tyre contacts (the x axis at the ground) toward +y, with a wall
    lean = 12.0
    P2 = []
    for p in P1:
        q = json.loads(json.dumps(p))
        q["xf"] = {"rot": [0, 0, lean], "t": [0, 0, 0], "pivot": [0, 0, 0]}
        P2.append(q)
    ps2 = L.PartSet(P2)
    # the roll [0, 0, +12] tips the top toward -y (a point (0, 0, 1000) goes to y -208): the bicycle leans toward -y, so the wall stands on the -y side and
    # the LEFT grip end is what touches it (the first version put the wall on the +y side, against the right grip: the bicycle leaned away from it)
    wall_y = float(min(ps2.part_bbox(n)[0][1] for n in ("grip_l", "bar_sweep_l", "pedal_l")))
    P2.append(B("wall", -600.0, 2000.0, wall_y - 200.0, wall_y, -50.0, 2400.0, "wall_brick", note="the wall (a stand-in slab) on the side the bicycle leans toward (-y)"))
    ps1 = L.PartSet(P1)
    lo, hi = ps1.bbox()
    T = {
        "family": FAMILY, "title": "Quay Street's bicycle against a wall",
        "units": "millimetres; angles in degrees; z up; x forward (the front wheel at +x); y to the rider's right; the pivot is the rear wheel's ground contact; BI2 leans toward -y, the rider's left, where its wall stands",
        "status": "fixes applied, not re-reviewed", "sample": "BI2",
        "materials": {
            "paint_black": {"name": "black enamel, chipped and rusting at the welds", "srgb": [24, 26, 26], "rough": 0.45, "rough_words": "semi-gloss", "metal": True, "note": "frame, forks, mudguards: chipped to red-brown rust at the dropouts, the lower head tube and the mudguard stays"},
            "steel": {"name": "chrome-plated steel gone dull", "srgb": [150, 152, 150], "rough": 0.4, "rough_words": "dull satin", "metal": True, "note": "bars, stem, cranks, hubs, spokes: pitted with orange rust spots, never mirror bright"},
            "tyre": {"name": "black rubber tyre, cracked, grey-white dust", "srgb": [30, 30, 30], "rough": 0.8, "rough_words": "matt", "metal": False, "note": "a pale grey bloom of dust on the sidewalls; the rim is its own ring inside it (steel)"},
            "saddle_black": {"name": "saddle black leather-look, cracked", "srgb": [34, 30, 28], "rough": 0.55, "rough_words": "semi-matt", "metal": False, "note": "cracked and shiny at the nose, a worn nose edge"},
            "grip_black": {"name": "grips black rubber, worn", "srgb": [22, 22, 22], "rough": 0.7, "rough_words": "matt", "metal": False, "note": "also the brake pads"},
            "chain_dark": {"name": "chain, brown with oil and rust", "srgb": [62, 46, 34], "rough": 0.6, "rough_words": "matt", "metal": True, "note": "the plates rust-brown, the rollers oily black; a line of oil spots on the right chain stay below it"},
            "reflector_red": {"name": "rear reflector, red plastic, scratched", "srgb": [150, 18, 22], "rough": 0.3, "rough_words": "glossy, scratched", "metal": False, "note": "the only saturated colour on the bicycle: 60 mm across"},
            "wall_brick": {"name": "soot-blackened brick (the street's)", "srgb": [78, 64, 58], "rough": 0.9, "rough_words": "rough", "metal": False, "note": "a stand-in"},
        },
        "variants": {
            "BI1": {"name": "BI1: an adult's roadster standing upright (a stand-in for a bicycle held up by its rider)", "parts": P1, "overall": {"w": round(float(hi[0] - lo[0]), 1), "d": round(float(hi[1] - lo[1]), 1), "h": round(float(hi[2] - lo[2]), 1)}, "overall_tol": 2.0, "contact_tol": 3.0,
                    "joins": [["seat_tube", "top_tube"], ["top_tube", "head_tube"], ["down_tube", "head_tube"], ["down_tube", "seat_tube"], ["rw_hub", "chain_stay_l"], ["fw_hub", "fork_l"], ["rw_tyre2", "rw_spoke1"], ["fw_tyre2", "fw_spoke1"], ["rw_hub", "rw_spoke1"], ["bar_mid", "stem"], ["grip_r", "bar_sweep_r"], ["saddle", "seat_post"], ["crank_r", "bb_spindle"], ["pedal_r", "crank_r"],
                              ["rw_rim1", "rw_tyre1"], ["fw_rim1", "fw_tyre1"], ["rw_spoke1", "rw_rim2"], ["fw_spoke1", "fw_rim2"], ["sprocket", "rw_hub"], ["chain_bot", "chain_c01"], ["chain_c14", "chain_top"], ["chain_top", "chain_s01"], ["chain_s12", "chain_bot"],
                              ["chain_c07", "chainring"], ["chain_s06", "sprocket"], ["chainguard", "chainguard_clip"], ["chainguard_clip", "chain_stay_r"], ["chainguard_strap", "chainguard"], ["chainguard_strap", "seat_tube"],
                              ["brake_lever_l", "grip_l"], ["brake_lever_r", "grip_r"], ["brake_rod_f", "brake_lever_l"], ["brake_rod_r", "brake_lever_r"], ["brake_rod_f", "fork_l"], ["brake_rod_r", "seat_stay_r"],
                              ["fw_stirrup_arm_l", "fork_l"], ["fw_stirrup_arm_r", "fork_r"], ["fw_stirrup_bar", "fw_stirrup_arm_l"], ["fw_pad_l", "fw_stirrup_bar"], ["fw_brake_bridge", "fork_l"],
                              ["rw_stirrup_arm_l", "seat_stay_l"], ["rw_stirrup_arm_r", "seat_stay_r"], ["rw_stirrup_bar", "rw_stirrup_arm_l"], ["rw_pad_l", "rw_stirrup_bar"], ["rw_brake_bridge", "seat_stay_l"],
                              ["fw_guard_stay_l", "fw_guard1"], ["fw_guard_stay_r", "fw_guard1"], ["rw_guard_stay_l", "rw_guard5"], ["rw_guard_stay_r", "rw_guard5"], ["rw_reflector", "rw_guard5"],
                              ["carrier_deck", "carrier_rail_l"], ["carrier_rail_l", "carrier_cross_rear"], ["carrier_stay_l", "carrier_cross_rear"], ["carrier_stay_r", "carrier_cross_rear"], ["carrier_deck", "seat_stay_l"]],
                    "embeds": [["seat_tube", "top_tube", 14.0], ["seat_tube", "down_tube", 14.0], ["head_tube", "top_tube", 16.0], ["head_tube", "down_tube", 16.0], ["head_tube", "fork_crown", 12.0], ["head_tube", "stem", 12.0], ["seat_tube", "seat_post", 12.0], ["seat_tube", "seat_bridge", 12.0], ["seat_tube", "chain_stay_l", 8.0], ["seat_tube", "chain_stay_r", 8.0],
                               ["down_tube", "chain_stay_l", 8.0], ["down_tube", "chain_stay_r", 8.0], ["chain_stay_l", "bb_spindle", 12.0], ["chain_stay_r", "bb_spindle", 12.0], ["down_tube", "bb_spindle", 12.0], ["seat_tube", "bb_spindle", 12.0], ["rw_hub", "chain_stay_l", 22.0], ["rw_hub", "chain_stay_r", 22.0], ["rw_hub", "seat_stay_l", 22.0], ["rw_hub", "seat_stay_r", 22.0],
                               ["fw_hub", "fork_l", 22.0], ["fw_hub", "fork_r", 22.0], ["bar_mid", "stem", 12.0], ["bar_mid", "bar_sweep_l", 12.0], ["bar_mid", "bar_sweep_r", 12.0], ["bell", "bar_mid", 12.0], ["grip_l", "bar_sweep_l", 12.0], ["grip_r", "bar_sweep_r", 12.0], ["crank_r", "chainring", 12.0], ["crank_r", "bb_spindle", 12.0], ["crank_l", "bb_spindle", 12.0],
                               ["pedal_r", "crank_r", 12.0], ["pedal_l", "crank_l", 12.0], ["seat_bridge", "seat_stay_l", 8.0], ["top_tube", "stem", 8.0], ["down_tube", "fork_crown", 9.0], ["fork_l", "fork_crown", 9.0], ["fork_r", "fork_crown", 9.0], ["seat_bridge", "seat_stay_r", 8.0], ["fork_crown", "fork_l", 12.0], ["fork_crown", "fork_r", 12.0], ["saddle", "seat_post", 12.0], ["seat_post", "top_tube", 12.0], ["stem", "head_tube", 12.0]],
                    "overlap_allow": 6.0, "faces": []},
            "BI2": {"name": "BI2: the roadster leaning 12 degrees toward a brick wall, its left grip end against it (the sample)", "parts": P2, "overlap_allow": 6.0, "contact_tol": 3.0, "joins": [["grip_l", "wall"]], "embeds": "SAME_AS_BI1", "faces": []},
        },
        "drawing": {"views": ["front", "left", "plan"], "sections": [{"id": "y0", "axis": "y", "at": 0.0}, {"id": "x449", "axis": "x", "at": 449.0}]},
        "numbers": [
            {"id": "N1", "what": "tyre outer diameter (the wheel)", "value": 2 * R, "kind": "Judgement", "source": "a 26 x 1 3/8 inch roadster tyre: 590 mm bead seat plus two 35 mm sections is about 660 (the ISO number is from memory: not reached on a page this session); error 10", "tol": 10.0, "measure": {"kind": "bbox", "axis": "z", "parts": ["rw_tyre%d" % k for k in range(1, 17)]}, "variant": "BI1"},
            {"id": "N2", "what": "wheelbase (axle to axle)", "value": round(FX, 1), "kind": "Judgement", "source": "a gent's roadster's wheelbase is about 1100 to 1140; from the stated tube lengths and angles: %.0f; error 40" % FX, "tol": 40.0, "measure": {"kind": "centre_dx", "axis": "x", "a": "rw_hub", "b": "fw_hub"}, "variant": "BI1"},
            {"id": "N3", "what": "saddle top above the ground", "value": 1035.0, "kind": "Judgement", "source": "a rider of 1.75 m sits with the saddle about 1.0 m up; error 40", "tol": 40.0, "measure": {"kind": "edge", "axis": "z", "part": "saddle", "side": "hi"}, "variant": "BI1"},
            {"id": "N4", "what": "handlebar grips above the ground", "value": round(STEM_TOP[1] + 13.0 + 14.0, 1), "kind": "Judgement", "source": "roadster bars stand about as high as the saddle or just above it; error 40", "tol": 40.0, "measure": {"kind": "edge", "axis": "z", "part": "grip_r", "side": "hi"}, "variant": "BI1"},
            {"id": "N5", "what": "bottom bracket height", "value": 300.0, "kind": "Judgement", "source": "a roadster's bottom bracket is about 300 mm up (30 mm below the axles); error 15", "tol": 15.0, "measure": {"kind": "centre", "axis": "z", "part": "bb_spindle"}, "variant": "BI1"},
            {"id": "N6", "what": "handlebar width over the grips", "value": 790.0, "kind": "Judgement", "source": "swept-back roadster bars are 560 to 620 between the bends and about 790 over the grips' ends; error 50", "tol": 50.0, "measure": {"kind": "span", "axis": "y", "a": "grip_l", "b": "grip_r"}, "variant": "BI1"},
            {"id": "N8", "what": "rear sprocket diameter (18 teeth)", "value": 73.0, "kind": "Judgement", "source": "the review of 13 October: an 18 tooth sprocket 73 mm across (12.7 pitch: pitch circle 73.2); S1 shows a rusted wheel in which no sprocket reads; error 3", "tol": 3.0, "measure": {"kind": "extent", "axis": "z", "part": "sprocket"}, "variant": "BI1"},
            {"id": "N9", "what": "chainguard depth across the bicycle", "value": 60.0, "kind": "Judgement", "source": "the review: sheet steel 60 deep, 1 thick; no chainguard reads in S1; error 5", "tol": 5.0, "measure": {"kind": "extent", "axis": "y", "part": "chainguard"}, "variant": "BI1"},
            {"id": "N10", "what": "rim width", "value": RIM_W, "kind": "Judgement", "source": "the review: rims 25 wide, 10 deep, as their own ring (a 26 x 1 3/8 steel rim is about 22 to 25 wide); S1's rims read as thin rings; error 3", "tol": 3.0, "measure": {"kind": "extent", "axis": "y", "part": "fw_rim1"}, "variant": "BI1"},
            {"id": "N11", "what": "carrier platform length", "value": 340.0, "kind": "Judgement", "source": "the review: a 340 x 130 platform of 10 mm tube at 780 over the rear wheel; S1's own row lists a rear carrier but at 430 px no number reads; error 20", "tol": 20.0, "measure": {"kind": "extent", "axis": "x", "part": "carrier_deck"}, "variant": "BI1"},
            {"id": "N12", "what": "carrier platform width", "value": CARRIER_W, "kind": "Judgement", "source": "the review (130); error 15", "tol": 15.0, "measure": {"kind": "extent", "axis": "y", "part": "carrier_deck"}, "variant": "BI1"},
            {"id": "N13", "what": "carrier platform top above the ground", "value": CARRIER_Z, "kind": "Judgement", "source": "the review (780 over the rear wheel, 120 over the mudguard's top at 668); error 30", "tol": 30.0, "measure": {"kind": "edge", "axis": "z", "part": "carrier_deck", "side": "hi"}, "variant": "BI1"},
            {"id": "N14", "what": "rear reflector diameter", "value": 60.0, "kind": "Judgement", "source": "the review: a red reflector 60 across on the rear mudguard; error 3", "tol": 3.0, "measure": {"kind": "extent", "axis": "z", "part": "rw_reflector"}, "variant": "BI1"},
            {"id": "N7", "what": "crank length", "value": 170.0, "kind": "Judgement", "source": "170 mm, the usual crank; error 6", "tol": 6.0, "measure": {"kind": "span", "axis": "x", "a": "crank_l", "b": "crank_r"}, "variant": "BI1"},
        ],
        "photos": [], "sources": [], "previews": [], "checks": [], "owed": [],
    }
    T["variants"]["BI2"]["embeds"] = T["variants"]["BI1"]["embeds"]
    n7 = [n for n in T["numbers"] if n["id"] == "N7"][0]
    n7["value"] = 340.0
    n7["what"] = "crank span: the two arms' outer ends along x (two cranks of 170, crossing at the spindle)"
    T["drive"] = {"pitch_mm": PITCH, "ring_teeth": N_RING, "sprocket_teeth": N_SPR, "links": 102, "chain_width_mm": CH_W, "chain_thickness_mm": CH_T, "chain_y_mm": CH_Y, "stay_y_mm": STAY_Y,
                  "ring_pitch_radius_mm": round(R_RING, 2), "sprocket_pitch_radius_mm": round(R_SPR, 2), "guard": {"depth_mm": GUARD_DEPTH, "thickness_mm": GUARD_T, "over_chain_mm": GUARD_GAP, "front_behind_ring_front_mm": 40.0},
                  "rims": {"width_mm": RIM_W, "depth_mm": RIM_D, "outer_face_radius_mm": R - TS}, "brakes": {"lever_mm": LEVER_L, "rod_mm": ROD_D, "stirrup_radius_mm": 270.0, "rim_inner_radius_mm": R - TS - RIM_D, "bridge_radius_mm": 360.0},
                  "mudguard_stays": {"per_guard": 2, "diameter_mm": 5.0}, "carrier": {"length_mm": 340.0, "width_mm": CARRIER_W, "top_mm": CARRIER_Z, "tube_mm": 10.0, "stays": 2}, "reflector_mm": 60.0,
                  "source": "the review of 13 October (TARGET-REVIEW.md, bicycle fault 1); every number a Judgement unless S1 or S3 shows otherwise (none reads at the size seen)"}
    T["lean"] = {"deg": lean, "wall_y_mm": round(wall_y, 1), "toward": "-y, the rider's left (the roll [0, 0, +12] tips the top toward -y)", "touching": "grip_l"}
    return T


def finish(T):
    T["sources"] = [
        {"id": "S1", "url": "https://www.geograph.org.uk/photo/2932507", "read": "2026-10-13", "author": "Jeremy Bolwell", "licence": "CC BY-SA 2.0 (read on the page)", "taken": "2012-05-06", "kind": "photograph",
         "shows": "a rusted gent's roadster leaning on a stone wall in a ruined building: a diamond frame with a level top tube, two big spoked wheels with mudguards, swept-back bars, a sprung saddle, a rear carrier; the rear wheel nearer the camera so the perspective is strong",
         "used": True, "not_used_for": "any number (the camera is oblique and close, the picture low in contrast); the rust is a wear state, not the sample's; the layout of the missing parts (no brake rod, chain or carrier reads in the 430 px crop, a rusted dark machine)",
         "period": "2012, and an INTERIOR: the machine rests in a ruined chapel room, on its page 'maybe 50 years' (the Pant y Celyn Baptist ruin), so it dates the type, a roadster of the 1950s or before, not the street; the roadster for 1990 stays a Judgement (an older rider's bicycle, plausible in a port town); the alternative, named and not written, is a 1980s utility frame (a town bicycle on 26 x 1 3/8 wheels with cable callipers and a rear rack)"},
        {"id": "S2", "url": "https://www.geograph.org.uk/photo/4155634", "read": "2026-10-13", "author": "DS Pugh", "licence": "CC BY-SA 2.0 (read on the page)", "taken": "2014-09-01", "kind": "photograph",
         "shows": "a modern road bicycle leaning with its front tyre against a dry-stone wall: shows how a bicycle leans on a wall (front wheel and bar end against the stone, the rear wheel on the ground at a lean of about 10 to 15 degrees); a pannier and a bottle (brands masked)",
         "used": True, "not_used_for": "the bicycle's form (modern: 700c wheels, derailleur, drop frame) and any number", "period": "2014; used only for the leaning pose"},
        {"id": "S3", "url": "https://www.geograph.org.uk/photo/4811433", "read": "2026-10-13", "author": "Bill Nicholls", "licence": "CC BY-SA 2.0 (read on the page)", "taken": "2014-09-21", "kind": "photograph",
         "shows": "a black gent's roadster on a display stand in a museum room: the diamond frame in a clean side view, swept bars, a plain saddle, 28 inch wheels",
         "used": False, "not_used_for": "everything (an interior display of an older machine, not a street photograph: looked at for the frame's layout only)", "period": "2014 interior of a heritage machine"},
        {"id": "S4", "url": "https://api.polyhaven.com/assets?t=models", "read": "2026-10-13", "author": "Poly Haven artists", "licence": "CC0 1.0", "taken": "n/a (the list of 521 models)", "kind": "model list",
         "shows": "no bicycle", "used": False, "not_used_for": "everything: no CC0 bicycle exists, so it is made by script", "period": "n/a"},
        {"id": "S5", "url": "https://api.geograph.org.uk/syndicator.php (terms bicycle, bicycles, bicycle wall, bike leaning; takenyear 1975 to 1996 and without a year)", "read": "2026-10-13", "author": "Geograph contributors", "licence": "CC BY-SA 2.0 (each page)", "taken": "1975 to 1996 searched", "kind": "search record",
         "shows": "1975 to 1996: a 1991 timbered house with a bicycle at its door, a 1992 station platform with cyclists, a 1993 night view of parked bicycles, a 1994 trail rider, a 1996 sporting photograph; none of a bicycle against a wall close up",
         "used": False, "not_used_for": "measuring", "period": "n/a"},
        {"id": "S6", "url": "canon.md, the content rule (D18)", "read": "2026-10-13", "author": "this project", "licence": "own work", "taken": "n/a", "kind": "own",
         "shows": "the content rule keeps young people out of every image and every prop: the bicycle is an adult's, the frame 560 mm, no small wheels, no stabilisers, no basket", "used": True, "not_used_for": "shape", "period": "n/a"},
    ]
    T["previews"] = [
        {"file": "p1-ruin-roadster-leaning.jpg", "source": "S1", "credit": "Jeremy Bolwell, Geograph 2932507, CC BY-SA 2.0, 2012-05-06, cropped to the bicycle", "masked": ["nothing to mask: no person, no lettering"], "looked_at_full_size": True, "no_people_no_drink_no_betting_no_names": True},
    ]
    T["night"] = {"lantern_linear": L.LANTERN_LINEAR, "note": "the bicycle stands against the blank wall between lamp pools; the chrome catches the lantern colour (1.0, 0.25, 0.0) as thin glints on the rims and bars, the black frame vanishes"}
    wall_y = T["lean"]["wall_y_mm"]
    T["placement"] = {
        "slot": "west side, against the soot-brick wall of the west_south block (the plain ground floor: no shopfront), the bicycle parallel to the wall facing +x (up the street), its LEFT grip end touching the brick, leaning 12 degrees toward the wall (the first version leaned it away from the wall: the wall stood on the side the top tips away from), its tyres 0.60 m from the wall at the ground; the rear tyre's back at x 14.12, the front tyre's front at x 15.88 (centre x 15.0), the grip's contact at x 15.15 on brick between the cottage door at x 13.5 (the doorstep to x 14.0) and the cottage window at x 15.9 (its sill from x 15.425); the wall at z -5.125",
        "x_m": 15.0, "wall_z_m": -5.125, "footway_mm": 2000.0, "min_clear_mm": 1000.0, "length_mm": T["variants"]["BI1"]["overall"]["w"],
        "openings_named": {"door": {"id": "west_south_bay1", "x": [13.081, 13.919], "step_to_x": 14.0, "step_depth_mm": 352.5}, "window": {"id": "west_south_bay0_gf_w1", "x": [15.475, 16.325], "sill_x": [15.425, 16.375], "sill_above_crown_m": 0.8236},
                           "source": "the DRAWN street: terrace-front.py's plain-row rule (a household door at bay start + 1.5 m, windows at + 3.3 and + 5.1, the west rows turned: street x = the bay's high end less the local x), as the front-doors-all target (street.houses) and the house-windows target (sites) list them; the scene file's own coarse boxes put a door at x 16.5 and a window at x 14.1 (vignette-pieces.json west_south_door2), which the drawn street does not use"},
        "reasons": [
            "the soot-brick wall of the cottages is where small things lean (the poster wall of the scene, x 11.4); it is NOT blank at x 14.1 to 15.9: the drawn plain row has a household door at x 13.5 (opening 13.08 to 13.92, a doorstep 0.998 wide and 0.35 m deep to x 14.0), a cottage window at x 15.9 (opening 15.475 to 16.325, sill 0.82 m above the crown, its stone sill 50 mm proud from x 15.425) and another at x 17.7; the first version's 'no door (the side door is at x 25.5)' read x 25.5 on the west_north block and missed all of it",
            "the slot keeps the grip's contact on brick: the left grip's end touches the wall at x 15.15, 0.28 m from the window's sill and 1.15 m from the doorstep's edge; both tyres stand clear of the door: the rear tyre's back (x 14.12) is 0.2 m past the door's approach (x 13.92) and 0.12 m past the doorstep's end (x 14.0), and the tyres stand 0.6 m out, 0.25 m beyond the step's front edge (0.35 m)",
            "leaning, it takes a footway depth of its roll: a 12 degree lean puts the left grip end 0.60 m from the tyres' line and the right pedal and grip 0.18 m on the other side, so the bicycle takes 0.78 m of the 2.0 m footway and leaves 1.22 m clear on the kerb side (the first version's 0.34 m and 1.64 m came from the same wall on the wrong side)",
            "it is an adult's bicycle, ambient dressing that belongs to no one on the street's list of residents",
        ],
        "poses": [{"id": "bicycle", "variant": "BI2", "x_m": 14.45, "z_m": round(-5.125 - wall_y / 1000.0, 4), "yaw_deg": 0.0, "zone": "west_footway", "ignore_parts": ["wall"], "leans_on": ["C1_terrace_carcass"], "contact_tol_m": 0.03, "head_check": False}],
    }
    T["wear"] = [
        "enamel chipped to red-brown rust at the dropouts, the head tube's lower end, the seat-stay bridge and the mudguard stays; paint dulled, a few small dents in the mudguards",
        "chrome gone to dull grey with orange pitting on the bars, rims and spokes; the chain brown with oil and rust, a line of oil spots below the lower run",
        "tyres hard, cracked at the sidewalls, one slightly soft (flat at the ground by 8 mm: a seed), grey dust bloom",
        "the saddle cracked and shiny at the nose; the grips worn smooth at their ends",
        "a wet street under it: darkness on the lowest 150 mm of the tyres and a grit splash on the mudguard",
        "NOT shown: a lock or chain bar (a chain through the wheel is a variant, a seed), a basket, stabilisers, any maker's badge on the head tube (a real bicycle has one; this has a blank plate)",
    ]
    T["disagreements"] = [
        {"id": "W1", "what": "which bicycle", "book": "the research notes list none; the brief asks for a bicycle against a wall", "photo": "S1 shows an old roadster leaning on a wall (the type of the period's older riders); S2 shows the leaning pose with a modern bicycle", "chose": "the roadster, upright geometry from the tube lengths and angles, the leaning pose from S2"},
        {"id": "W3", "what": "the missing parts", "book": "the first version: a frame, wheels, bars, saddle, cranks and bell only; 'the carrier, lamp and chain guard are textures; the chain is not modelled'", "photo": "S1's own row lists a rear carrier; a street bicycle always shows brakes, a chain and rims (the review of 13 October); none reads at the 430 px of the crop, so every added number is the review's Judgement", "chose": "the chain, sprocket, chainguard, rims, rod brakes, mudguard stays, carrier and reflector are geometry, each with a row"},
        {"id": "W4", "what": "the wall's side", "book": "the first version leaned the bicycle toward -y and put the wall on the +y side, against the right grip", "photo": "n/a (arithmetic): the roll [0, 0, +12] tips a point (0, 0, 1000) to y -208, so the top moves toward -y and only a wall on the -y side can hold it", "chose": "the wall on the -y side, the left grip's end against it (found while checking the slot's neighbours; the review did not list it)"},
        {"id": "W2", "what": "the lean", "book": "none", "photo": "S2: the rear tyre on the ground, the front tyre and the bar end on the wall, a lean of about 12 degrees", "chose": "12 degrees, the wall touching the left grip's end"},
    ]
    T["variants_note"] = [
        "BI2 (the sample): the roadster leaning 12 degrees toward the wall, its left grip end against the brick.",
        "BI1: the same upright (for a bicycle held by a figure or standing on a stand).",
        "a ten-speed with drop bars is the second kind of adult bicycle of 1990: not written (its frame would be a new target); one kind only, as the street needs one bicycle.",
        "conditions (materials): C0 sound, C1 worn (the sample's wear), C2 rusted solid (S1's state, a derelict leaning for years).",
    ]
    T["owed"] = []
    T["not_settled"] = [
        "no 1975 to 1995 bicycle photograph was measurable and S1 and S2 are oblique and low in contrast: every number is Judgement (a gent's roadster's usual geometry), checked for internal consistency and against ranges, not against pixels",
        "the 26 x 1 3/8 wheel's exact tyre diameter (660 mm is from memory; the page that gives the ISO 590 bead seat was not reached)",
        "whether the street's bicycle should be a roadster or a ten-speed (the roadster is chosen because S1 is a street-leaning roadster)",
        "added after the review of 13 October (each a Judgement from its list, none readable in S1 or S3 at the size they are seen): the chain on its pitch circles, the 18 tooth sprocket, the chainguard, the rims as their own ring, rod brakes (two 120 mm levers, two 8 mm rods, a stirrup under each rim), two 5 mm stays on each mudguard, the 340 x 130 carrier at 780 and the 60 mm red reflector; the lamp is not modelled (a dynamo lamp, a texture and decal if wanted); the chain's links are lumped in strips (each says how many links it stands for)",
        "the brake type: rod brakes with stirrups under the rims are the review's first choice and fit a roadster; side-pull callipers with a 60 mm reach are the cable alternative (a 1980s town bicycle) and are not written",
        "the lean's wall contact is by the left grip end (S2 shows the front tyre against the wall): either is a seed",
    ]
    T["content_rule_note"] = "an adult's bicycle only: no small frame, no stabilisers, no child seat, no toy (a statement of the content rule)."
    T["builder_notes"] = [
        "build by script: the tubes as cylinders from the end points in target.json (a part's p0 and p1), the tyres as one torus of section 38 (the 16 boxes are the engine's approximation), the 36 spokes (8 drawn) in the real wheel; the mudguards as one swept strip per wheel",
        "BI2 is BI1 with the part transform (a roll of 12 degrees about the x axis through the tyre contacts) and the wall; the builder places the bicycle with the transform",
        "no maker's badge, no transfer, no lettering of any kind",
        "the left grip end is the point that touches the wall (the lean tips the top toward -y, the rider's left; the first version put the wall on the other side); stand the sample at the pose in target.json (yaw 0, x 14.45, z from the wall less the grip's reach)",
        "the chain: strips of 8 x 6 mm on the pitch circles (88.9 and 36.6 radius) joined by two runs on the common tangents; build real links of 12.7 pitch along the same path (102 links); the chain, ring and sprocket lie in the plane y = 55, outboard of the chain stays at y = +-40",
    ]
    C = []
    for n in T["numbers"]:
        C.append({"name": "%s: %s" % (n["id"], n["what"]), "measure": "measure it on the built mesh in millimetres (%s)" % n["measure"].get("kind"), "expect": "%.0f mm" % n["value"], "tol": "+-%.0f mm" % n["tol"]})
    C += [
        {"name": "C1: both wheels the same diameter, on the ground", "measure": "the tyres' bounding boxes", "expect": "660 mm, z 0", "tol": "+-10 mm"},
        {"name": "C2: no part floats; the bicycle touches the ground and the wall", "measure": "the contact graph", "expect": "connected", "tol": "0 floating"},
        {"name": "C3: the frame's tube angles", "measure": "seat tube 72 degrees, head tube 68 degrees", "expect": "72 and 68", "tol": "+-2 degrees"},
        {"name": "C4: no lettering, no badge", "measure": "textures and text", "expect": "none", "tol": "exact"},
        {"name": "C5: the drive", "measure": "chain 8 x 6 on the pitch circles of the 44 tooth ring (88.9) and the 18 tooth sprocket (36.6, 73 across), 102 links of 12.7 (within half a link), outboard of the stays", "expect": "as stated", "tol": "+-1.5 mm"},
        {"name": "C6: the chainguard, rims, brakes, stays, carrier and reflector are present with their numbers", "measure": "guard 60 deep 1 thick over the top run; two 25 x 10 rim rings; two 120 levers, two 8 rods, two stirrups under the rims; two 5 mm stays per mudguard; carrier 340 x 130 at 780; reflector 60", "expect": "as stated", "tol": "see numbers"},
        {"name": "C7: the contact on brick", "measure": "the left grip's end touches the wall at a street x outside every drawn opening (door, doorstep, window and its sill)", "expect": "x 15.15 on brick", "tol": "0.1 m clear"},
    ]
    T["checks"] = C
    return T


SUMMARY = ("The bicycle is an adult's gent's roadster (26 x 1 3/8 wheels 660 mm over the tyre, a 1097 mm wheelbase, a level top tube on a 72 degree seat tube and a 68 degree head tube, swept-back bars 790 over the grips, a sprung saddle at 1035, mudguards with their stays and a red reflector, a plain bell, 170 mm cranks, a chain on an 18 tooth rear sprocket under a chainguard, rims as their own rings, rod brakes with 120 mm bar levers and stirrups under the rims, and a rear carrier 340 x 130 at 780) in the enamel-chipped, dull-chromed state of a street bicycle, no badge or lettering, shown leaning 12 degrees toward the soot-brick wall of the cottages (centre x 15.0, its left grip end on brick between the door at x 13.5 and the window at x 15.9: the wall is not blank, and the first version's lean was away from its wall); "
           "no period photograph was measurable (the two street photographs are oblique and low in contrast), so every number is Judgement within stated ranges and the target is checked for internal consistency, the tube angles and the ranges, not against pixels; an adult's bicycle only.")


def story(T):
    return {
        "no": "7", "title": "Quay Street's bicycle against a wall: the exact target", "summary": SUMMARY, "previews_list": "p1 (S1 cropped; no overlay: the photograph is too oblique and low in contrast to lay a drawing on)",
        "rulings": {"ruling_2oct": "not a car, skip or pallet; plain street dressing", "sources_order": "no CC0 bicycle exists (S4); so own work by script",
                    "content": "an adult's bicycle only; the data scan finds none of what the rule forbids", "noai": "S1 to S3 are CC BY-SA 2.0 Geograph photographs used only to look at; no NoAI source",
                    "look": "dull chrome, rust spots and a wet street: grime is the strategy", "night": "chrome glints, the frame vanishes"},
        "searched": "What was searched: Poly Haven's model list (no bicycle); Geograph's feed for `bicycle`, `bicycles`, `bicycle wall`, `bike leaning` with each year 1975 to 1996 and without a year. Wikimedia Commons was not asked.",
        "reuse": [
            ["Poly Haven models", "no bicycle", "NOT USED", "S4"],
            ["vignette-scene.json, the asset plan, the research notes", "no bicycle anywhere", "NONE to reuse", "this is a new prop"],
            ["git branches (git log --all for bicycle, bike)", "none", "none to reuse", ""],
        ],
        "axes": "Axes: x forward (the front wheel at +x), y to the rider's right, z up from the ground at the tyres' contact. Cylinders for tubes, spokes and the hub, boxes for the tyre and rim segments, the chain strips, the saddle, the cranks and the pedals; BI2 adds a transform that tips the top toward -y and a wall on that side.",
        "assembly": [
            "**Wheels**: 26 x 1 3/8, 660 over the tyre (a ring of 16 segments 38 x 38), a hub 44 across and 100 long, spokes 2.4 across (8 drawn of 36), mudguards 60 wide and 2 thick 8 mm over the tyre round the top 140 degrees.",
            "**Frame**: seat tube 28 across, 560 from the bottom bracket centre, 72 degrees; level top tube 28 across, 570 long; down tube 30 across; head tube 36 across and 150 long at 68 degrees; chain stays 16 across and 450 long, seat stays 16 across; the bottom bracket 300 up (30 below the axles).",
            "**Fork**: two blades 22 across with 45 rake at the foot, a crown 24 x 124 x 24.",
            "**Cockpit**: a stem 22 across rising 170 along the steering axis, a bar of 22 across, 380 straight between swept-back ends to 580 over the bends and 790 over the 105 mm grips, a bell 52 across.",
            "**Saddle and post**: a post 22 across to z 985, a saddle 280 x 180 x 50 at 985 to 1035.",
            "**Drive**: a spindle 24 across, a chainring 180 across (44 teeth, pitch circle 177.8), cranks 170, pedals 100 x 105 x 24; an 18 tooth sprocket 73 across on the rear hub; a chain 8 wide and 6 thick on the pitch circles (88.9 and 36.6 radius) with two runs on the common tangents (446.9 long) and 26 wrap strips, 102 links of 12.7 in all, in the plane y = 55, outboard of the chain stays at y = +-40; a chainguard of sheet steel 60 deep and 1 thick, 13 over the top run, from the sprocket's centre to 40 mm behind the chainring's front, on a clip to the right chain stay and a strap to the seat tube.",
            "**Rims and brakes**: each wheel has its own rim ring of 16 segments, 25 wide and 10 deep (radial) inside the tyre (outer face 292); rod brakes: two bar levers 120 long clamped under the grips (the left works the front), two rods 8 across running to a stirrup under each rim (a crossbar 56 wide at radius 270 with two arms to the fork blades and the seat stays, a bridge above the mudguard, two pads against the rim's inner face at 281); Judgement, the review's list.",
            "**Mudguard stays, reflector and carrier**: two 5 mm stays per mudguard to the drop-outs; a red reflector 60 across on the rear mudguard's tail; a rear carrier of 10 mm tube with a 340 x 130 platform at 780 over the rear wheel, its two stays running to the drop-outs (S1's own row lists a carrier; no number reads in the photograph).",
        ],
        "own_rows": "the tube angles from the parts' own end points, the ranges for a roadster, the drive (pitch circles, tangent runs, 102 links, the plane outboard of the stays), the chainguard, rims, rod brakes, mudguard stays, carrier and reflector with their numbers, the lean toward the wall and the wall contact, the contact on brick clear of every drawn opening, the slot against the street's pieces and door zones",
    }


if __name__ == "__main__":
    T = finish(build())
    SF.write_all(HERE, T, story(T))
