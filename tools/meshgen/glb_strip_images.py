"""Rewrite a .glb without its images (and the textures and samplers that use them), keeping every accessor's
bytes as they were: geometry and UVs unchanged, only the embedded pictures dropped.

    python -I tools/meshgen/glb_strip_images.py IN.glb OUT.glb [--flat MATERIAL=R,G,B ...]

WHY, 3 November (the corner plan's step 10): the street's recipe takes a clutter model's geometry and flat colours
only (terrace-front.py _read_glb, its MATERIALS table), and git takes a model under 1 MB; the A-board's model carried
its 3.8 MB paint picture. --flat gives a material that wore a picture the flat colour of that picture's ground (sRGB
0 to 255, written linear), so the model's own colour is the paint's and the recipe's table can match it.
"""
import json
import struct
import sys

src, dst = sys.argv[1], sys.argv[2]
FLAT = {}
for k, a in enumerate(sys.argv):
    if a == "--flat" and k + 1 < len(sys.argv):
        name, rgb = sys.argv[k + 1].split("=")
        FLAT[name] = [round(((c / 255.0 + 0.055) / 1.055) ** 2.4 if c / 255.0 > 0.04045 else c / 255.0 / 12.92, 4)
                      for c in (float(x) for x in rgb.split(","))]
data = open(src, "rb").read()
assert data[:4] == b"glTF"
jlen = struct.unpack_from("<I", data, 12)[0]
doc = json.loads(data[20:20 + jlen].decode("utf-8"))
boff = 20 + jlen
blob = data[boff + 8:boff + 8 + struct.unpack_from("<I", data, boff)[0]]

image_views = {im["bufferView"] for im in doc.get("images", []) if "bufferView" in im}
for key in ("images", "textures", "samplers"):
    doc.pop(key, None)
for m in doc.get("materials", []):
    pbr = m.get("pbrMetallicRoughness", {})
    for k in ("baseColorTexture", "metallicRoughnessTexture"):
        pbr.pop(k, None)
    for k in ("normalTexture", "occlusionTexture", "emissiveTexture"):
        m.pop(k, None)
    if m.get("name") in FLAT:
        m.setdefault("pbrMetallicRoughness", {})["baseColorFactor"] = FLAT[m["name"]] + [1.0]

# keep every buffer view but the images', packed again on 4-byte boundaries
new_blob = bytearray()
remap = {}
views = []
for i, v in enumerate(doc["bufferViews"]):
    if i in image_views:
        continue
    while len(new_blob) % 4:
        new_blob.append(0)
    start = v.get("byteOffset", 0)
    chunk = blob[start:start + v["byteLength"]]
    nv = dict(v)
    nv["byteOffset"] = len(new_blob)
    new_blob.extend(chunk)
    remap[i] = len(views)
    views.append(nv)
doc["bufferViews"] = views
for a in doc.get("accessors", []):
    if "bufferView" in a:
        a["bufferView"] = remap[a["bufferView"]]
while len(new_blob) % 4:
    new_blob.append(0)
doc["buffers"] = [{"byteLength": len(new_blob)}]

js = json.dumps(doc, separators=(",", ":")).encode("utf-8")
js += b" " * ((4 - len(js) % 4) % 4)
total = 12 + 8 + len(js) + 8 + len(new_blob)
out = struct.pack("<III", 0x46546C67, 2, total) + struct.pack("<II", len(js), 0x4E4F534A) + js \
      + struct.pack("<II", len(new_blob), 0x004E4942) + bytes(new_blob)
open(dst, "wb").write(out)
print("stripped images=%d bytes %d -> %d" % (len(image_views), len(data), len(out)))
