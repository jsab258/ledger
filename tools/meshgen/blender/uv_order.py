"""The maps' UV layout as a garment's first layer, the one Unreal's material reads (imported by skin_garment.py and
mend_limb_weights.py before their FBX export).

WHY, 30 October 2026 (his order C9; Tom's jacket with built cuffs, withdrawn on 29 October after holes in the back,
the chest and the right sleeve in the packaged game): uv_pack_low.py adds "UVMap" (the layout the colour, normal
and packed maps are baked on) after the retopology's "pattern" (each piece flat at true size), and the built cuffs'
jacket reached its export with "pattern" first, so the game read the maps through the flat pattern's layout and the
colour map's alpha cut holes. Drape 19's had "UVMap" first by another route. Blender cannot reorder UV layers, so
each is copied anew, the maps' first.
"""


def maps_layout_first(o, name="UVMap"):
    layers = [u.name for u in o.data.uv_layers]
    if not layers or layers[0] == name or name not in layers:
        return False
    order = [name] + [n for n in layers if n != name]
    data = {n: [d.uv.copy() for d in o.data.uv_layers[n].data] for n in layers}
    for n in layers:
        o.data.uv_layers[n].name = n + "_was"
    for n in order:
        u = o.data.uv_layers.new(name=n)
        for d, uv in zip(u.data, data[n]):
            d.uv = uv
    for n in layers:
        o.data.uv_layers.remove(o.data.uv_layers[n + "_was"])
    o.data.uv_layers.active = o.data.uv_layers[name]
    o.data.uv_layers[name].active_render = True
    return True
