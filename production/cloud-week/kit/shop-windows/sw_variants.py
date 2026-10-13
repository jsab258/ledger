"""The front parts the 3.2 kit did not build: the flute pilaster, the T2 (putty-glazed, flat-faced mullion) window frame, the render, boarded and patterned-tile stallrisers, and the sill and the
sealing strip at either end of the window. A subclass of the kit's `Builder` (production/cloud-week/kit/shopfront/build_shopfront.py, imported, not edited): for a variant the kit built (panel
pilaster, T1 window, panel stallriser) every call goes straight to the kit's own method, so Rita's front and any front made of the kit's parts is the kit's, mesh for mesh.

What each variant is comes from the 3.2 target (production/cloud-week/targets/shopfronts/target.json, which the kit reads: parts.pilaster.variants.flute, profiles shaft_flute_plan; parts.window_frame.profiles
mullion_t2_plan, glazing_putty; parts.stallriser.variants.render / boarded / tile_patterned): numbers read from it, not typed here.
"""
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO, "production", "cloud-week", "kit", "shopfront"))
sys.path.insert(0, os.path.join(REPO, "production", "cloud-week", "kit", "tools"))

import bpy  # noqa: E402
import build_shopfront as bs  # noqa: E402
import joinery  # noqa: E402
from shapely.geometry import Polygon, box as sbox  # noqa: E402


class VBuilder(bs.Builder):
    def __init__(self, T, shop, variants):
        super().__init__(T, shop)
        self.var = variants                       # the shop's front.variants (pilaster, console, cornice, stallriser, window_frame, shop_door, side_door)
        self.pilaster_side = None                 # set by the front: "l" when the window's left end meets a pilaster (the doors at the right), "r" otherwise

    # ---------------------------------------------------------------------------------------------- pilasters
    def pilaster(self, tag=""):
        v = self.var["pilaster"]
        if v == "panel":
            return super().pilaster(tag)
        if v == "flute":
            super().pilaster(tag)                 # the plinth, base ogee, backing core, capital and die tablet are the panel pilaster's (the flute elevation has the same members)
            return self._flute_shaft(tag)
        raise NotImplementedError("pilaster variant " + v)

    def _flute_shaft(self, tag):
        """Replace the panel pilaster's shaft by the flute variant's: a bottom rail (z 600 to 740) and a top rail (2430 to 2540) at the shaft's face (d 140), and between them the five
        segmental flutes, 12 deep between 12 mm fillets (profile shaft_flute_plan), standing from the backing core's face (d 95) to the front, as the panel shaft does."""
        pil = self.P["pilaster"]
        d = pil["dims"]
        pr = pil["profiles"]
        n = lambda s: "pil%s_%s" % (tag, s)
        old = self.get(n("shaft"))
        self.objs.remove(old)
        self.meta.pop(old.name, None)
        me = old.data
        bpy.data.objects.remove(old, do_unlink=True)
        bpy.data.meshes.remove(me)
        core_d = d["relief_beside_frames"]["frame_fronts_d"]["T1"]            # 95: the backing core's front, as in the kit
        sh0, sh1 = d["shaft_u_in_slot"]
        SP = d["shaft_proud"]
        PT, NK = d["plinth_top_z"], d["neck_z"]
        z0, z1 = d["shaft_bottom_rail_top_z"], d["shaft_top_rail_bottom_z"]
        plan = pr["shaft_flute_plan"]["points"]
        poly = [(p[0], core_d if p[1] == 0.0 else p[1]) for p in plan]         # the plan's back edge (d 0) is cut to the core's front
        self.add(n("shaft"), bs.prism_ud(poly, z0, z1), "oxblood")
        self.add(n("shaft_rail_b"), bs.box(sh0, sh1, core_d, SP, PT, z0), "oxblood")
        self.add(n("shaft_rail_t"), bs.box(sh0, sh1, core_d, SP, z1, NK), "oxblood")
        return self

    # ---------------------------------------------------------------------------------------------- the sill, at whichever end meets a pilaster
    def sill(self, u0=None, u1=None):
        win = self.S["zones_u"]["window"]
        if self.pilaster_side == "l":              # the window's left end meets the pilaster's plinth: the sill stops 3 short of it
            return super().sill(win[0] + 3.0, win[1])
        return super().sill(u0, u1)

    # ---------------------------------------------------------------------------------------------- the window frame
    def window_frame(self):
        v = self.var["window_frame"]
        if v == "T1":
            return super().window_frame()
        if v == "T2":
            return self._window_frame_param(mullion_key="mullion_t2_plan", mullion_face=80.0, glaze_key="glazing_putty")
        raise NotImplementedError("window frame variant " + v)

    def _window_frame_param(self, mullion_key, mullion_face, glaze_key):
        """The kit's window_frame (T1) with the mullion section, the mullion face and the glazing section as parameters: jambs, seat, transom, head, toplight bars, glass and the six-sided
        joinery are the kit's own numbers and order; T2 differs in its 80 x 92 flat-faced quirk-bead mullions (and the bars carried up on them) and in putty fillets where T1 has ovolo beads."""
        W = self.P["window_frame"]
        d = W["dims"]
        pr = W["profiles"]
        gl = self.S["glazing_layout"]
        win = self.S["zones_u"]["window"]
        u0, u1 = win
        z_seat0, z_seat1 = d["bottom_rail"]
        z_tr0, z_tr1 = d["transom"]
        z_h0, z_h1 = d["head"]
        jf = d["jamb_face"]
        z_foot = z_seat0 - bs.SEAT_EMBED
        jp = pr["jamb_t1_plan"]["points"]
        jl = [(u0 + p[0], p[1]) for p in jp]
        jr = [(u1 - p[0], p[1]) for p in jp][::-1]
        self.add("win_jamb_l", bs.prism_ud(jl, z_seat0, z_h1), "white")
        self.add("win_jamb_r", bs.prism_ud(jr, z_seat0, z_h1), "white")
        for nm, poly in (("win_jamb_foot_l", jl), ("win_jamb_foot_r", jr)):
            xs = [p[0] for p in poly]
            clip = Polygon(poly).buffer(0).intersection(sbox(min(xs) + (0.3 if nm.endswith("_l") else 0.0), 60.5, max(xs) - (0.3 if nm.endswith("_r") else 0.0), 1e5))
            self.add(nm, bs.prism_ud(list(clip.exterior.coords)[:-1], z_foot, z_seat0), "white", bev=None)
        ui0, ui1 = u0 + jf, u1 - jf
        self.add("win_seat", bs.box(ui0, ui1, 0.0, 60.0, z_seat0, z_seat1), "white")
        tz = [(p[0], p[1] + z_tr0) for p in pr["transom_t1"]["points"]]
        self.add("win_transom", bs.prism_dz(tz, ui0, ui1), "white")
        hz = [(p[0], p[1] + z_h0) for p in pr["head_section"]["points"]]
        self.add("win_head", bs.prism_dz(hz, ui0, ui1), "white")
        mp = pr[mullion_key]["points"]
        mc = [u0 + c for c in gl["mullion_centres"]]
        for k, c in enumerate(mc):
            self.add("win_mullion_%d" % k, bs.prism_ud([(c + p[0], p[1]) for p in mp], z_seat1, z_tr0), "white")
        bp = pr["toplight_bar_plan"]["points"]
        bc = [u0 + c for c in gl["toplight_bar_centres"]]
        for k, c in enumerate(bc):
            self.add("win_bar_%d" % k, bs.prism_ud([(c + p[0], max(p[1], 1.0)) for p in bp], z_tr1 - 6.0, z_h0 + 3.0), "white")
        mbc = [u0 + c for c in gl.get("toplight_mullion_bar_centres", [])]
        for k, c in enumerate(mbc):
            self.add("win_mbar_%d" % k, bs.prism_ud([(c + p[0], max(p[1], 1.0)) for p in mp], z_tr1 - 6.0, z_h0 + 3.0), "white")
        tb = sorted([(c, 14.0, 4.0) for c in bc] + [(c, mullion_face / 2.0, 8.0) for c in mbc])
        gz = d["glass_d"]
        gt = d["glass_thickness"]
        g0, g1 = gz, gz + gt
        rjamb, rmull = 10.0, 8.0
        lower_edges = [(ui0 - rjamb)] + [x for c in mc for x in (c - mullion_face / 2.0 + rmull, c + mullion_face / 2.0 - rmull)] + [ui1 + rjamb]
        for k in range(len(mc) + 1):
            a, b = lower_edges[2 * k], lower_edges[2 * k + 1]
            self.add("win_glass_lower_%d" % k, bs.box(a, b, g0, g1, z_seat1, z_tr0), "glass", bev=None)
        up = [(ui0 - rjamb)] + [x for c, hw_, rb_ in tb for x in (c - hw_ + rb_, c + hw_ - rb_)] + [ui1 + rjamb]
        for k in range(len(tb) + 1):
            a, b = up[2 * k], up[2 * k + 1]
            self.add("win_glass_top_%d" % k, bs.box(a, b, g0, g1, z_tr1, z_h0), "glass", bev=None)
        bd = pr[glaze_key]["points"]
        prof = [(p[0], -p[1]) for p in bd]
        lights = []
        edges_l = [ui0] + [x for c in mc for x in (c - mullion_face / 2.0, c + mullion_face / 2.0)] + [ui1]
        for k in range(len(mc) + 1):
            lights.append((edges_l[2 * k], z_seat1, edges_l[2 * k + 1], z_tr0))
        edges_t = [ui0] + [x for c, hw_, rb_ in tb for x in (c - hw_, c + hw_)] + [ui1]
        for k in range(len(tb) + 1):
            lights.append((edges_t[2 * k], z_tr1, edges_t[2 * k + 1], z_h0))
        for k, (a, b, c2, e) in enumerate(lights):
            V, F = joinery.sweep_frame(prof, a, b, c2, e, -g1)
            self.add("win_bead_%d" % k, (V, [tuple(int(i) for i in f) for f in F]), "white", bev=None)
        return self

    # ---------------------------------------------------------------------------------------------- the stallriser
    def stallriser(self):
        v = self.var["stallriser"]
        if v == "panel":
            return super().stallriser()
        if v in ("render", "boarded", "tile_patterned"):
            return self._stallriser_flat(v)
        raise NotImplementedError("stallriser variant " + v)

    def _stallriser_flat(self, variant):
        """A plain stallriser across the window zone: the panel variant's own section (plinth 120, face at d 125, z 0 to 525) with no panels. render: painted render (coat 12) or painted
        hardboard (the tea rooms); boarded: the empty unit's panelling painted out and a ply sheet (1200 x 525 x 9) screwed over it with 12 screws; tile_patterned: the Mickey's tiled face
        (the skirting and capping profile of the `tile` variant; the pattern is a texture)."""
        sv = self.P["stallriser"]["variants"]
        u0, u1 = self.S["zones_u"]["window"]
        if variant == "tile_patterned":
            sec = [tuple(p) for p in sv["tile"]["section"]["points"]]
        else:
            sec = [tuple(p) for p in sv["panel"]["section"]["points"]]
        # the section is (d, z) from the foot: a plain prism across the zone
        self.add("sta_panel", bs.prism_dz(sec, u0, u1), "oxblood")
        self.openings = []
        if variant == "boarded":
            dm = sv["boarded"]["dims"]
            face = self.P["stallriser"]["dims"]["face_d"]
            t = dm["sheet_thickness"]
            mid = (u0 + u1) / 2.0
            self.add("sta_sheet", bs.box(mid - 600.0, mid + 600.0, face, face + t, 0.0 + 1.0, 525.0 - 1.0), "oxblood")
            n = int(dm["screws"])
            for k in range(n):
                row, col = k // 6, k % 6
                cu = mid - 550.0 + col * 220.0
                cz = 90.0 + row * 340.0
                V, F = _screw(cu, face + t, cz)
                self.add("sta_screw_%d" % k, (V, F), "white", bev=None)
        return self


def _screw(u, d, z, r=5.0, h=3.0, n=8):
    """A round screw head standing on a face at depth d (axis along d)."""
    a = np.linspace(0, 2 * math.pi, n, endpoint=False)
    V = []
    for dd in (d, d + h):
        for t in a:
            V.append((u + r * math.cos(t), -dd, z + r * math.sin(t)))
    V = np.array(V)
    F = [tuple(range(n))[::-1], tuple(range(n, 2 * n))] + [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
    return V, F
