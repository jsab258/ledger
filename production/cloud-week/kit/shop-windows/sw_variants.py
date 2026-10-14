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
        if v == "clad":
            return self._clad_pilaster(tag)
        if v == "render":
            return self._render_pilaster(tag)
        raise NotImplementedError("pilaster variant " + v)

    def _drop(self, name):
        old = self.get(name)
        self.objs.remove(old)
        self.meta.pop(old.name, None)
        me = old.data
        bpy.data.objects.remove(old, do_unlink=True)
        bpy.data.meshes.remove(me)

    def _render_pilaster(self, tag):
        """The painted render pier on a stepped plinth with a hollow-moulded head (batch B, 14 October 2026: the launderette's re-clad pier and the 1930s grocer's; 3.2 target parts.pilaster.variants.render):
        the kit's backing core, capital and die tablet are the panel pilaster's (the render variant's elevation has the same capital members, z 2540 up), the plinth is the stepped profile
        `plinth_stepped_side` (block 0 to 360, a step to 450 four back, a step to 484 eight back, a hollow (cavetto) to 579 and a flat band to 600) with the free side's insets (the elevation's widths
        350, 342, 336, 328), and the shaft is the plain `shaft_render_plan` face from the core's front (d 95) to d 140, z 600 to 2540. The downpipe's chase at the party line is cut through every
        plinth block, as the kit does for the panel plinth."""
        pil = self.P["pilaster"]
        d = pil["dims"]
        pr = pil["profiles"]
        bs.Builder.pilaster(self, tag)
        for nm in ("plinth_body", "plinth_cap", "shaft", "ogee"):
            self._drop("pil%s_%s" % (tag, nm))
        n = lambda s_: "pil%s_%s" % (tag, s_)
        side = [tuple(p) for p in pr["plinth_stepped_side"]["points"]]
        el = {q["name"]: q["pts"] for q in pil["variants"]["render"]["elevation"]}
        W_ = d["slot_width"]
        cw, cd = d["downpipe_chase"]["width"] / 2.0, d["downpipe_chase"]["from_d"]

        def width_of(name):
            pts = el[name]
            return max(p[0] for p in pts)
        z_steps = pil["variants"]["render"]["step_heights_z"]            # 360, 450, 484, 600
        blocks = [("plinth_block1", 0.0, z_steps[0], side[1][0]), ("plinth_block2", z_steps[0], z_steps[1], side[4][0]), ("plinth_block3", z_steps[1], z_steps[2], side[6][0])]
        for nm, za, zb, dd in blocks:
            ob = self.add(n(nm), bs.prism_dz([(0.0, za), (dd, za), (dd, zb), (0.0, zb)], 0.0, width_of(nm)), "oxblood")
            bs.bool_op(ob, *bs.box(-1.0, cw, cd, 400.0, za - 1.0, zb + 1.0), "DIFFERENCE")
        head = [(0.0, z_steps[2])] + side[6:12] + [(0.0, z_steps[3])]       # the hollow and the flat band: from (172, 484) to (148, 600)
        ob = self.add(n("plinth_head"), bs.prism_dz(head, 0.0, max(width_of("plinth_cavetto"), width_of("plinth_band"))), "oxblood")
        bs.bool_op(ob, *bs.box(-1.0, cw, cd, 400.0, z_steps[2] - 1.0, z_steps[3] + 1.0), "DIFFERENCE")
        core_d = d["relief_beside_frames"]["frame_fronts_d"]["T1"]
        plan = pr["shaft_render_plan"]["points"]
        poly = [(p[0], core_d if p[1] == 0.0 else p[1]) for p in plan]
        self.add(n("shaft"), bs.prism_ud(poly, d["plinth_top_z"], d["neck_z"]), "oxblood")
        return self

    # ---------------------------------------------------------------------------------------------- consoles
    def console(self, tag="", uc=175.0):
        v = self.var["console"]
        if v == "scroll":
            return super().console(tag, uc)
        if v == "block":
            return self._console_block(tag, uc)
        raise NotImplementedError("console variant " + v)

    def _console_block(self, tag, uc):
        """The plain block console of the 1930s grocer (3.2 target parts.console.variants.block): the scroll's own 240 x 205 x 550 envelope, flaring from the 172 foot to the 205 cap, no leaf, three bosses. The
        body is lofted from the variant's side points exactly as the kit lofts the scroll body (side chamfer 12); the three bosses are 30 mm roundels 6 proud on the front face at z 380, 440 and 500
        above the foot (a Judgement: the target says 'three bosses' and not where)."""
        C = self.P["console"]
        d = C["dims"]
        sil = C["variants"]["block"]["points_side"]
        hw, ch = d["width"] / 2.0, d["side_chamfer"]
        z0 = d["z_bottom"]
        n = lambda s_: "con%s_%s" % (tag, s_)
        front = [tuple(p) for p in sil[1:-1]]                      # from (172, 0) to (205, 550)
        rings = []
        for dv, z in front:
            zz = z0 + z
            rings.append([(uc - hw, 0.0, zz), (uc + hw, 0.0, zz), (uc + hw, -(dv - ch), zz), (uc + hw - ch, -dv, zz), (uc - hw + ch, -dv, zz), (uc - hw, -(dv - ch), zz)])
        self.add(n("body"), bs.loft_rings(rings), "oxblood", bev=None)
        for k, zl in enumerate((380.0, 440.0, 500.0)):
            a = np.linspace(0, 2 * math.pi, 14, endpoint=False)
            dfront = front[-1][0]
            V = []
            for dd in (dfront - 1.0, dfront + 6.0):
                for t in a:
                    V.append((uc + 15.0 * math.cos(t), -dd, z0 + zl + 15.0 * math.sin(t)))
            nn = len(a)
            F = [tuple(range(nn))[::-1], tuple(range(nn, 2 * nn))] + [(i, (i + 1) % nn, nn + (i + 1) % nn, nn + i) for i in range(nn)]
            self.add(n("boss_%d" % k), (np.array(V), F), "oxblood", bev=None)
        return self

    def _clad_pilaster(self, tag):
        """The clad pier (Mickey's: a 1960s-80s flush steel-clad pier, no plinth, no capital): three sheets 350 wide and 140 proud (the profile `clad_plan`: a 4 x 4 chamfer on the front edges), z 0 to
        1200, 1200 to 2400, 2400 to 2850, a 6 mm joint between them (3.2 target: parts.pilaster.variants.clad)."""
        pil = self.P["pilaster"]
        plan = [tuple(p) for p in pil["profiles"]["clad_plan"]["points"]]
        cd = pil["variants"]["clad"]["dims"]
        j = cd["joint_width"] / 2.0
        edges = [0.0] + [v for z in cd["sheet_joints_z"] for v in (z - j, z + j)] + [2850.0]
        for k in range(3):
            self.add("pil%s_clad_%d" % (tag, k + 1), bs.prism_ud(plan, edges[2 * k], edges[2 * k + 1]), "oxblood")
        return self

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
        if v == "M1":
            return self._window_frame_param(mullion_key="mullion_m1_plan", mullion_face=50.0, glaze_key="glazing_bead_gasket", jamb_key="jamb_m1_plan", transom_key="transom_m1")
        if v == "M2":
            # (batch B) the 1930s bronze-plated bar window: every bar (mullions, the bars between a light's toplights, the mullions carried up) is `bar_m2_plan`, 28 wide with its front at d 40 and rounded, the glass
            # held in the bar's own 3 mm rebates (no beads); the jambs are the same bar cut square (`jamb_key` None: made from the bar's own profile here); the transom is M1's (the only metal transom in 2.2: the
            # target's Judgement)
            return self._window_frame_param(mullion_key="bar_m2_plan", mullion_face=28.0, glaze_key=None, jamb_key=None, transom_key="transom_m1", bar_key="bar_m2_plan", rjamb=3.0, rmull=3.0, rbar=3.0)
        raise NotImplementedError("window frame variant " + v)

    def _window_frame_param(self, mullion_key, mullion_face, glaze_key, jamb_key="jamb_t1_plan", transom_key="transom_t1", bar_key="toplight_bar_plan", rjamb=10.0, rmull=8.0, rbar=4.0):
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
        if jamb_key is None:
            # M2: the jamb is the bar cut square: its wall side flat (u 0), the glass side the bar's own half-profile shifted 14 (rebate and rounded front), the front flat across to the wall side
            bp_ = [tuple(p) for p in pr[bar_key]["points"]]
            jp = [(0.0, 0.0)] + [(p[0] + 14.0, p[1]) for p in bp_[:9]] + [(0.0, bp_[8][1])]
        else:
            jp = pr[jamb_key]["points"]
        jl = [(u0 + p[0], p[1]) for p in jp]
        jr = [(u1 - p[0], p[1]) for p in jp][::-1]
        self.add("win_jamb_l", bs.prism_ud(jl, z_seat0, z_h1), "white")
        self.add("win_jamb_r", bs.prism_ud(jr, z_seat0, z_h1), "white")
        for nm, poly in (("win_jamb_foot_l", jl), ("win_jamb_foot_r", jr)):
            xs = [p[0] for p in poly]
            clip = Polygon(poly).buffer(0).intersection(sbox(min(xs) + (0.3 if nm.endswith("_l") else 0.0), 60.5, max(xs) - (0.3 if nm.endswith("_r") else 0.0), 1e5))
            if clip.is_empty or clip.geom_type != "Polygon":
                continue                 # (M2's jamb is 40 deep: nothing of it stands beyond d 60.5)
            self.add(nm, bs.prism_ud(list(clip.exterior.coords)[:-1], z_foot, z_seat0), "white", bev=None)
        ui0, ui1 = u0 + jf, u1 - jf
        self.add("win_seat", bs.box(ui0, ui1, 0.0, 60.0, z_seat0, z_seat1), "white")
        tz = [(p[0], p[1] + z_tr0) for p in pr[transom_key]["points"]]
        self.add("win_transom", bs.prism_dz(tz, ui0, ui1), "white")
        if transom_key != "transom_t1":
            # M1's transom is a 50 high box; the elevation keeps 2.2's 80 high band (2400 to 2480), "the box carrying a 30 mm snap-on cover plate on its top" (3.2 target, transom_m1's note)
            z_box = z_tr0 + max(p[1] for p in pr[transom_key]["points"])
            self.add("win_transom_cover", bs.box(ui0, ui1, 0.0, 60.0, z_box, z_tr1), "white")
        hz = [(p[0], p[1] + z_h0) for p in pr["head_section"]["points"]]
        self.add("win_head", bs.prism_dz(hz, ui0, ui1), "white")
        mp = pr[mullion_key]["points"]
        mc = [u0 + c for c in gl["mullion_centres"]]
        for k, c in enumerate(mc):
            self.add("win_mullion_%d" % k, bs.prism_ud([(c + p[0], p[1]) for p in mp], z_seat1, z_tr0), "white")
        bp = pr[bar_key]["points"]
        bc = [u0 + c for c in gl["toplight_bar_centres"]]
        for k, c in enumerate(bc):
            self.add("win_bar_%d" % k, bs.prism_ud([(c + p[0], max(p[1], 1.0)) for p in bp], z_tr1 - 6.0, z_h0 + 3.0), "white")
        mbc = [u0 + c for c in gl.get("toplight_mullion_bar_centres", [])]
        for k, c in enumerate(mbc):
            self.add("win_mbar_%d" % k, bs.prism_ud([(c + p[0], max(p[1], 1.0)) for p in mp], z_tr1 - 6.0, z_h0 + 3.0), "white")
        tb = sorted([(c, 14.0, rbar) for c in bc] + [(c, mullion_face / 2.0, rmull) for c in mbc])
        gz = d["glass_d"]
        gt = d["glass_thickness"]
        g0, g1 = gz, gz + gt
        lower_edges = [(ui0 - rjamb)] + [x for c in mc for x in (c - mullion_face / 2.0 + rmull, c + mullion_face / 2.0 - rmull)] + [ui1 + rjamb]
        for k in range(len(mc) + 1):
            a, b = lower_edges[2 * k], lower_edges[2 * k + 1]
            self.add("win_glass_lower_%d" % k, bs.box(a, b, g0, g1, z_seat1, z_tr0), "glass", bev=None)
        up = [(ui0 - rjamb)] + [x for c, hw_, rb_ in tb for x in (c - hw_ + rb_, c + hw_ - rb_)] + [ui1 + rjamb]
        for k in range(len(tb) + 1):
            a, b = up[2 * k], up[2 * k + 1]
            self.add("win_glass_top_%d" % k, bs.box(a, b, g0, g1, z_tr1, z_h0), "glass", bev=None)
        if glaze_key is None:
            return self                      # M2: the glass sits in the bars' own rebates, no beads
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
        if v in ("render", "boarded", "tile_patterned", "tile_square"):
            return self._stallriser_flat(v)
        if v == "slab":
            return self._stallriser_slab()
        raise NotImplementedError("stallriser variant " + v)

    def _stallriser_flat(self, variant):
        """A plain stallriser across the window zone: the panel variant's own section (plinth 120, face at d 125, z 0 to 525) with no panels. render: painted render (coat 12) or painted
        hardboard (the tea rooms); boarded: the empty unit's panelling painted out and a ply sheet (1200 x 525 x 9) screwed over it with 12 screws; tile_patterned: the Mickey's tiled face
        (the skirting and capping profile of the `tile` variant; the pattern is a texture)."""
        sv = self.P["stallriser"]["variants"]
        u0, u1 = self.S["zones_u"]["window"]
        if variant == "tile_patterned":
            sec = [tuple(p) for p in sv["tile"]["section"]["points"]]
        elif variant == "tile_square":
            # (batch B) the `tile` section with the square-tile variant's own heights: a black skirting 100 (the `tile` variant's is 120) and a bullnose cap 35 (`tile`: 33), so the courses fall as the
            # variant's dims say: 100 + 2 x 155.4 + 79.2 + 35 = 525
            dm = sv["tile_square"]["dims"]
            base = [tuple(p) for p in sv["tile"]["section"]["points"]]
            z_skirt_old, z_cap_old = base[2][1], base[4][1]
            z_cap_new = self.P["stallriser"]["dims"]["z_range"][1] - dm["capping_height"]
            sec = []
            for d_, z_ in base:
                if z_ == z_skirt_old:
                    z_ = dm["skirting"]
                elif z_cap_old <= z_ < base[-1][1] and z_ > z_skirt_old:
                    z_ = z_ + (z_cap_new - z_cap_old)
                sec.append((d_, z_))
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

    def _stallriser_slab(self):
        """The grocer's stallriser (3.2 target parts.stallriser.variants.slab): opaque coloured structural glass in three slabs, bottle green, polished, 3 mm black mastic joints, a 6 mm chrome capping 18 high.
        Built across the window zone: a black backing (the mastic) 100 deep, three slabs 25 thick (d 100 to the stallriser's face, 125) with 2 mm bevels and 3 mm joints between them, z 0 to 507, and the
        chrome capping (z 507 to 525, to d 128) over them. The slabs are paint_ materials (bottle green, the target's stallriser paint), polished (roughness 0.08)."""
        sv = self.P["stallriser"]["variants"]["slab"]
        dm = sv["dims"]
        u0, u1 = self.S["zones_u"]["window"]
        face = self.P["stallriser"]["dims"]["face_d"]
        z_top = self.P["stallriser"]["dims"]["z_range"][1]
        cap_h = dm["capping"]["height"]
        j = dm["joint"]
        n = int(dm["slabs"])
        zc = z_top - cap_h
        self.add("sta_backing", bs.box(u0, u1, 0.0, face - 25.0, 0.0, z_top), "oxblood", bev=None)
        w = ((u1 - u0) - (n - 1) * j) / n
        for k in range(n):
            a = u0 + k * (w + j)
            self.add("sta_slab_%d" % k, bs.box(a, a + w, face - 25.0, face, 0.0, zc), "oxblood", bev=dm["bevel"])
        for k in range(n - 1):
            a = u0 + (k + 1) * w + k * j
            self.add("sta_mastic_%d" % k, bs.box(a, a + j, face - 25.0, face - 1.0, 0.0, zc), "oxblood", bev=None)
        self.add("sta_capping", bs.box(u0, u1, face - 25.0, face + 3.0, zc, z_top), "oxblood", bev=2.0)
        self.openings = []
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
