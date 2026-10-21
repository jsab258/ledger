"""Shading for the front-doors-all kit (cloud week 42, unit 9, try 2): large flat faces are shaded flat.

3.1's finish shades every part smooth and keeps an edge sharp only where the two faces beside it differ by more than 35 degrees. An edge between a large flat face and a chamfer or a
curve that turns less than 35 degrees stayed soft, so the flat face's boundary vertices carried the averaged normal of the chamfer: F7's boards (V-joint chamfers 34 degrees off the
face) read as rounded staves in raking light (the close review's fault), and the same happened, less visibly, to the flat tops and fronts of the stone tread, T1's band and weatherboard,
a scraper's blade and a spyhole's ring. `sharpen_flat_faces` marks as sharp every edge on the boundary of a large flat face (a planar face of more than 100 mm2, at least 8 mm across),
so its normals are split at its arrises and it is flat; the smooth shading of a curved moulding (strips a few mm wide) is left alone. Run inside Blender, on a mesh in metres, after
`shade_smooth` and `set_sharp_from_angle`.
"""
import bmesh
from shapely.geometry import MultiPoint


def sharpen_flat_faces(me, min_area=1e-4, min_side=0.008, dot=0.99995, plane_tol=2e-5):
    """Mark the boundary edges of every large flat face sharp. Returns the number of large flat faces found. `me` is in metres: 100 mm2 = 1e-4 m2, 8 mm = 0.008 m."""
    bm = bmesh.new()
    bm.from_mesh(me)
    bm.faces.ensure_lookup_table()
    seen = set()
    found = 0
    for f in bm.faces:
        if f.index in seen or f.calc_area() < 1e-12:
            continue
        n0 = f.normal.copy()
        d0 = n0.dot(f.verts[0].co)
        grp, stack = [f], [f]
        seen.add(f.index)
        while stack:
            g = stack.pop()
            for e in g.edges:
                for h in e.link_faces:
                    if h.index in seen or h.calc_area() < 1e-12:
                        continue
                    if h.normal.dot(n0) >= dot and abs(n0.dot(h.verts[0].co) - d0) < plane_tol:
                        seen.add(h.index)
                        grp.append(h)
                        stack.append(h)
        if sum(g.calc_area() for g in grp) < min_area:
            continue
        # the narrower side of the face's oriented bounding rectangle (in the face's own plane)
        t = (1.0, 0.0, 0.0) if abs(n0[0]) < 0.9 else (0.0, 1.0, 0.0)
        u = n0.cross(type(n0)(t)).normalized()
        v = n0.cross(u)
        pts = {(round(vv.co.dot(u), 6), round(vv.co.dot(v), 6)) for g in grp for vv in g.verts}
        rect = MultiPoint(list(pts)).convex_hull
        if rect.geom_type != "Polygon":
            continue
        xy = list(rect.minimum_rotated_rectangle.exterior.coords)
        sides = sorted([((xy[0][0] - xy[1][0]) ** 2 + (xy[0][1] - xy[1][1]) ** 2) ** 0.5, ((xy[1][0] - xy[2][0]) ** 2 + (xy[1][1] - xy[2][1]) ** 2) ** 0.5])
        if sides[0] < min_side:
            continue
        found += 1
        ids = {g.index for g in grp}
        for g in grp:
            for e in g.edges:
                if any(h.index not in ids for h in e.link_faces) or len(e.link_faces) == 1:
                    e.smooth = False
    bm.to_mesh(me)
    bm.free()
    return found
