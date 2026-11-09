"""Every picture a glb import makes, set explicitly after the import (item n09-3, step 3).

    python tools/ue/glb_texture_settings.py --selftest        # runs without Unreal
    python tools/ue/glb_texture_settings.py --dry             # what each glb's pictures would get, from the files

WHY, 9 November 2026. production/research/frame-headroom/COOKING-PLAN-2026-11-09.md, section 5 step 3 and its review
fixes 1, 3, 4 and 13: Interchange's glTF import left the fronts' 5410x550 fascia boards and 50 smaller glb pictures on
TC_EditorIcon (uncompressed RGBA8) with no mips, never streamed: about 358 MB on the card. Resizing alone would leave
them uncompressed, so nothing is left to Interchange: tools/ue/import_vehicles.py import_glb calls apply() on its
destination after the import, and every Texture2D there gets every setting below, or a line saying why not.

THE SETTINGS, by the glTF slot the import bound the picture to (Interchange's glTF instances name their texture
parameters <Map>Texture: Engine/Plugins/Interchange/Runtime/Source/Import/Public/Gltf/InterchangeGLTFMaterial.h lines
18, 54 BaseColor, 59 MetallicRoughness, 81 Normal, 84 Emissive, 88 Occlusion):
  base colour   TC_Default, sRGB on       TEXTUREGROUP_World
  normal        TC_Normalmap, sRGB off    TEXTUREGROUP_WorldNormalMap
  orm/occlusion TC_Default, sRGB off      TEXTUREGROUP_WorldSpecular
  emissive      TC_Default, sRGB on       TEXTUREGROUP_World
and for all: MipGenSettings TMGS_FromTextureGroup; NeverStream off; CompressionNoAlpha on where the alpha is all
opaque (read from the source's channel range); where a side is not a power of two (or a side is over the folder's
texture_max), PowerOfTwoMode ResizeToSpecificResolution with ResizeDuringBuildX/Y: the fascia boards 4096x512, the rest
each side's nearest power of two (the plan's B2 table), halved together until neither side is over the folder's kind's
texture_max (production/specs/asset-budgets.json); otherwise PowerOfTwoMode None and 0x0.
A picture bound under any other parameter, under two roles that disagree, or not bound at all is logged and left,
never guessed. The sampler type the new settings derive (make_base_material.derived_sampler_type, the engine's rule)
is checked against the type each bound material's expression declares; a mismatch leaves the picture untouched.

SWITCH: LEDGER_GLB_TEXTURE_SETTINGS=0 turns the pass off (on by default). LEDGER_GLB_TEXTURE_STRICT=1 also refuses a
picture whose declared sampler type could not be read (default: set, counted as unchecked).
LINES: one "glbTexture ..." line per picture on stdout, and one "glbTextures=... " summary per glb, which
import_vehicles prints and appends to ue-material.txt.
"""
import glob
import json
import os
import re
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
BUDGETS = os.path.join(REPO, "production", "specs", "asset-budgets.json")
GAME_INPUTS = os.environ.get("LEDGER_GAME_INPUTS", r"F:\LedgerTools\game-inputs")

#: the glTF instance's texture parameter -> role (InterchangeGLTFMaterial.h, as above)
ROLE_BY_PARAM = {"BaseColorTexture": "basecolor", "NormalTexture": "normal", "MetallicRoughnessTexture": "orm",
                 "OcclusionTexture": "orm", "EmissiveTexture": "emissive"}
#: role -> (compression leaf, sRGB, texture group); TextureDefines.h 393/394 (TC_Default, TC_Normalmap), 30-32 (groups)
ROLE_SETTINGS = {"basecolor": ("TC_DEFAULT", True, "TEXTUREGROUP_WORLD"),
                 "normal": ("TC_NORMALMAP", False, "TEXTUREGROUP_WORLD_NORMAL_MAP"),
                 "orm": ("TC_DEFAULT", False, "TEXTUREGROUP_WORLD_SPECULAR"),
                 "emissive": ("TC_DEFAULT", True, "TEXTUREGROUP_WORLD")}
#: the glb's own material slots -> role (glTF 2.0 material schema), for the dry listing and the size/alpha fallback
GLTF_SLOTS = (("pbrMetallicRoughness", "baseColorTexture", "basecolor"),
              ("pbrMetallicRoughness", "metallicRoughnessTexture", "orm"),
              (None, "normalTexture", "normal"), (None, "occlusionTexture", "orm"), (None, "emissiveTexture", "emissive"))
FASCIA_SIZE = (4096, 512)


def switch_on():
    return os.environ.get("LEDGER_GLB_TEXTURE_SETTINGS", "1").strip() not in ("0", "off", "false", "no")


def strict_on():
    return os.environ.get("LEDGER_GLB_TEXTURE_STRICT", "0").strip() in ("1", "on", "true", "yes")


# ---- pure rules -----------------------------------------------------------------------------------------------------

def is_pow2(n):
    return n > 0 and (n & (n - 1)) == 0


def nearest_pow2(n):
    """The nearest power of two by distance, the smaller on a tie (the plan's B2 table: 380 -> 256, 409 -> 512)."""
    if n <= 1:
        return 1
    lo = 1 << (n.bit_length() - 1)
    hi = lo << 1
    return lo if n - lo <= hi - n else hi


def is_fascia(w, h):
    """A fascia board: wider than 4096 and at least eight times as wide as high (the fronts' 5410x550)."""
    return w > 4096 and h * 8 <= w


def kind_cap(dest, budgets=None):
    """The folder's kind's texture_max (longest folder wins, as asset_checks reads it); the global cap otherwise."""
    if budgets is None:
        with open(BUDGETS, encoding="utf-8") as fh:
            budgets = json.load(fh)
    glob_cap = int(budgets.get("texture_max_global", 4096))
    best = None
    for folder, kind in budgets.get("folders", []):
        if dest == folder or dest.startswith(folder.rstrip("/") + "/"):
            if best is None or len(folder) > len(best[0]):
                best = (folder, kind)
    if best is None:
        return glob_cap, None
    k = budgets.get("kinds", {}).get(best[1], {})
    cap = k.get("texture_max")
    return (min(int(cap), glob_cap) if cap else glob_cap), best[1]


def target_size(w, h, cap):
    """(tw, th) to resize to at build, or None to keep the source's size."""
    if is_pow2(w) and is_pow2(h) and max(w, h) <= cap:
        return None
    tw, th = (FASCIA_SIZE if is_fascia(w, h) else (nearest_pow2(w), nearest_pow2(h)))
    while max(tw, th) > cap and min(tw, th) > 1:
        tw, th = max(1, tw // 2), max(1, th // 2)
    return tw, th


def plan(role, w, h, alpha_used, cap):
    """Every setting for one picture. alpha_used: True, False or None (unknown: the alpha is kept)."""
    comp, srgb, group = ROLE_SETTINGS[role]
    size = target_size(w, h, cap) if w and h else None
    return {"compression": comp, "srgb": srgb, "lod_group": group, "mips": "TMGS_FROM_TEXTURE_GROUP",
            "never_stream": False, "no_alpha": alpha_used is False,
            "pot_mode": "RESIZE_TO_SPECIFIC_RESOLUTION" if size else "NONE",
            "resize": size or (0, 0)}


def compact(name):
    s = str(name or "").upper()
    m = re.search(r"SAMPLERTYPE_([A-Z_]+)", s)
    if m:
        s = m.group(1)
    return "".join(c for c in s if c.isalnum())


def expected_sampler(compression, srgb):
    sys.path.insert(0, HERE)
    import make_base_material as mbm
    return mbm.derived_sampler_type(compression, srgb)


def sampler_verdict(derived, declared):
    """'ok', 'mismatch' or 'unchecked' for the derived type against a list of declared ones (None = unread)."""
    if derived is None:
        return "mismatch"
    if not declared or any(d is None for d in declared):
        bad = [d for d in declared if d is not None and compact(d) != compact(derived)]
        return "mismatch" if bad else "unchecked"
    return "ok" if all(compact(d) == compact(derived) for d in declared) else "mismatch"


def texture_line(dest, name, role, src, alpha, p, derived, declared, result, reason=""):
    sz = "%dx%d" % p["resize"] if p and p["pot_mode"] != "NONE" else "keep"
    return ("glbTexture dest=%s tex=%s role=%s src=%s alpha=%s comp=%s srgb=%s group=%s mips=%s size=%s neverStream=0 "
            "noAlpha=%s sampler=%s declared=%s result=%s%s"
            % (dest, name, role or "?", "%dx%d" % src if src and src[0] else "?",
               {True: "used", False: "opaque", None: "?"}[alpha],
               p["compression"] if p else "-", (1 if p["srgb"] else 0) if p else "-", p["lod_group"] if p else "-",
               "FROM_TEXTURE_GROUP" if p else "-", sz if p else "-", (1 if p["no_alpha"] else 0) if p else "-",
               derived or "-", "/".join(str(d or "unread") for d in (declared or [])) or "-", result,
               (" reason=" + reason.replace(" ", "~")) if reason else ""))


def summary_line(dest, counts, on=True):
    if not on:
        return "glbTextures=OFF dest=%s" % dest
    bad = counts.get("refused", 0) + counts.get("readback_failed", 0) + counts.get("left", 0)
    return ("glbTextures=%s dest=%s textures=%d set=%d resized=%d refused=%d left=%d unchecked=%d readbackFailed=%d"
            % ("OK" if not bad else "PARTIAL", dest, counts.get("textures", 0), counts.get("set", 0),
               counts.get("resized", 0), counts.get("refused", 0), counts.get("left", 0), counts.get("unchecked", 0),
               counts.get("readback_failed", 0)))


# ---- the glb on disk (no Unreal) ------------------------------------------------------------------------------------

def _png_info(b):
    """(w, h, alpha channel or tRNS present) from PNG bytes, or None."""
    if b[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    w, h = struct.unpack(">II", b[16:24])
    ctype = b[25]
    alpha = ctype in (4, 6)
    i = 8
    while i + 8 <= len(b):
        ln, typ = struct.unpack(">I4s", b[i:i + 8])
        if typ == b"tRNS":
            alpha = True
        if typ in (b"IDAT", b"IEND"):
            break
        i += 12 + ln
    return w, h, alpha


def _jpeg_info(b):
    if b[:2] != b"\xff\xd8":
        return None
    i = 2
    while i + 9 < len(b):
        if b[i] != 0xFF:
            i += 1
            continue
        mk = b[i + 1]
        if mk in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
            h, w = struct.unpack(">HH", b[i + 5:i + 9])
            return w, h, False
        ln = struct.unpack(">H", b[i + 2:i + 4])[0]
        i += 2 + ln
    return None


def _alpha_used(b):
    """True/False when the alpha holds anything below opaque (PIL, if it is installed); None otherwise."""
    try:
        import io
        from PIL import Image
        im = Image.open(io.BytesIO(b))
        if "A" not in im.getbands() and "transparency" not in im.info:
            return False
        lo, _ = im.convert("RGBA").getchannel("A").getextrema()
        return lo < 255
    except Exception:
        return None


def glb_images(path, measure_alpha=False):
    """[{name, roles, w, h, alpha_channel, alpha_used}] for every image the glb's materials use."""
    with open(path, "rb") as fh:
        data = fh.read()
    if data[:4] != b"glTF":
        raise ValueError("not a glb")
    jlen = struct.unpack("<I", data[12:16])[0]
    js = json.loads(data[20:20 + jlen].decode("utf-8"))
    binp = 20 + jlen
    bin_chunk = b""
    if binp + 8 <= len(data):
        blen = struct.unpack("<I", data[binp:binp + 4])[0]
        bin_chunk = data[binp + 8:binp + 8 + blen]
    textures, images, views = js.get("textures", []), js.get("images", []), js.get("bufferViews", [])
    roles = {}
    for m in js.get("materials", []):
        for parent, key, role in GLTF_SLOTS:
            node = (m.get(parent) or {}) if parent else m
            ref = node.get(key)
            if ref is None:
                continue
            t = textures[ref["index"]] if ref.get("index", -1) < len(textures) else {}
            src = t.get("source")
            if src is not None:
                roles.setdefault(src, set()).add(role)
    out = []
    for i, im in enumerate(images):
        b = b""
        if "bufferView" in im:
            v = views[im["bufferView"]]
            off = v.get("byteOffset", 0)
            b = bin_chunk[off:off + v["byteLength"]]
        elif im.get("uri") and not im["uri"].startswith("data:"):
            p = os.path.join(os.path.dirname(path), im["uri"])
            if os.path.exists(p):
                b = open(p, "rb").read()
        info = _png_info(b) or _jpeg_info(b) or (0, 0, None)
        name = im.get("name") or os.path.splitext(os.path.basename(im.get("uri", "image%d" % i)))[0]
        out.append({"name": name, "roles": sorted(roles.get(i, ())), "w": info[0], "h": info[1],
                    "alpha_channel": info[2], "alpha_used": _alpha_used(b) if (measure_alpha and info[2]) else
                    (False if info[2] is False else None)})
    return out


def _newer(found, base, rel, pattern):
    for p in glob.glob(os.path.join(base, rel, pattern)):
        key = os.path.relpath(p, os.path.join(base, rel))
        if key not in found or os.path.getmtime(p) > os.path.getmtime(found[key]):
            found[key] = p


def import_sources():
    """(dest, glb) for every glb the build's import step passes through import_glb (vehicles, displays, fronts,
    rooms), each importer's own rule: vehicles from the checkout, the rest the newer of checkout and game inputs."""
    out = []
    for p in sorted(glob.glob(os.path.join(REPO, "production/assets/vehicles", "*.glb"))):
        st = os.path.splitext(os.path.basename(p))[0]
        out.append(("/Game/Ledger/Vehicles/%s" % st, p))
    for rel, root in (("production/assets/shop-displays", "/Game/Ledger/ShopDisplays"),
                      ("production/assets/shop-fronts", "/Game/Ledger/ShopFronts")):
        found = {}
        for base in (REPO, GAME_INPUTS):
            _newer(found, base, rel, "*.glb")
        for key in sorted(found):
            out.append(("%s/%s" % (root, os.path.splitext(key)[0]), found[key]))
    found = {}
    for base in (REPO, GAME_INPUTS):
        _newer(found, base, "production/assets/shop-rooms-3d", os.path.join("*", "*.glb"))
    for key in sorted(found):
        shop, part = os.path.split(os.path.splitext(key)[0])
        out.append(("/Game/Ledger/ShopRooms/%s/%s" % (shop, part), found[key]))
    return out


def dry(measure_alpha=True):
    """Each glb picture's settings as the editor pass would give them, from the files; the role from the glb's own
    material (the editor reads the bound instance instead). Returns (lines, totals)."""
    with open(BUDGETS, encoding="utf-8") as fh:
        budgets = json.load(fh)
    lines, tot = [], {"glbs": 0, "images": 0, "set": 0, "resized": 0, "left": 0, "fascia": 0}
    for dest, glb in import_sources():
        tot["glbs"] += 1
        cap, kind = kind_cap(dest, budgets)
        try:
            ims = glb_images(glb, measure_alpha)
        except Exception as e:
            lines.append("glbTexture dest=%s glb=%s result=UNREAD reason=%s" % (dest, glb, str(e)[:60].replace(" ", "~")))
            continue
        for im in ims:
            tot["images"] += 1
            roles = {r for r in im["roles"]}
            settings = {ROLE_SETTINGS[r] for r in roles}
            if not roles or len(settings) > 1:
                tot["left"] += 1
                lines.append(texture_line(dest, im["name"], "/".join(sorted(roles)) or None, (im["w"], im["h"]),
                                          im["alpha_used"], None, None, None, "LEFT",
                                          "unbound" if not roles else "roles-disagree"))
                continue
            role = sorted(roles)[0]
            p = plan(role, im["w"], im["h"], im["alpha_used"], cap)
            tot["set"] += 1
            tot["resized"] += p["pot_mode"] != "NONE"
            tot["fascia"] += p["resize"] == FASCIA_SIZE and is_fascia(im["w"], im["h"])
            lines.append(texture_line(dest, im["name"], role, (im["w"], im["h"]), im["alpha_used"], p,
                                      expected_sampler(p["compression"], p["srgb"]), None, "WOULD-SET",
                                      "cap=%d(%s)" % (cap, kind)))
    return lines, tot


# ---- the editor pass -------------------------------------------------------------------------------------------------

def _out(result, n=1):
    if isinstance(result, tuple):
        return result[-n:] if n > 1 else result[-1]
    return result


def _enum(unreal, enum_name, *leaves):
    e = getattr(unreal, enum_name, None)
    for leaf in leaves:
        v = getattr(e, leaf, None) if e is not None else None
        if v is not None:
            return v
    raise AttributeError("unreal.%s has none of %s" % (enum_name, "/".join(leaves)))


def declared_samplers(unreal, base, cache):
    """{parameter name: declared sampler type leaf or None} for one base material, through its function calls."""
    if base is None:
        return {}
    key = base.get_path_name()
    if key in cache:
        return cache[key]
    mel = unreal.MaterialEditingLibrary
    found, seen = {}, set()

    def walk(exprs, depth):
        for e in exprs or []:
            try:
                if isinstance(e, unreal.MaterialExpressionTextureSampleParameter):
                    name = str(e.get_editor_property("parameter_name"))
                    st = e.get_editor_property("sampler_type")
                    found.setdefault(name, compact(getattr(st, "name", None) or str(st)) or None)
                elif isinstance(e, unreal.MaterialExpressionMaterialFunctionCall) and depth < 6:
                    f = e.get_editor_property("material_function")
                    if f is not None and isinstance(f, unreal.MaterialFunction) and f.get_path_name() not in seen:
                        seen.add(f.get_path_name())
                        walk(mel.get_material_function_expressions(f), depth + 1)
            except Exception:
                continue
    try:
        walk(mel.get_material_expressions(base), 0)
    except Exception:
        pass
    cache[key] = found
    return found


def _bindings(unreal, dest, mesh):
    """{texture path: [(material path, parameter, role or None, declared or None)]} for the mesh's slots and every
    material under the destination."""
    lib, mel = unreal.EditorAssetLibrary, unreal.MaterialEditingLibrary
    mats, seen = [], set()
    if mesh is not None:
        for sm in mesh.get_editor_property("static_materials"):
            m = sm.get_editor_property("material_interface")
            if m is not None and m.get_path_name() not in seen:
                seen.add(m.get_path_name())
                mats.append(m)
    for p in lib.list_assets(dest, recursive=True, include_folder=False):
        a = lib.load_asset(p)
        if isinstance(a, unreal.MaterialInterface) and a.get_path_name() not in seen:
            seen.add(a.get_path_name())
            mats.append(a)
    cache, out = {}, {}
    for m in mats:
        try:
            base = m.get_base_material()
        except Exception:
            base = None
        decl = declared_samplers(unreal, base, cache)
        try:
            names = _out(mel.get_texture_parameter_names(m)) or []
        except Exception:
            names = []
        for n in names:
            n = str(n)
            try:
                if isinstance(m, unreal.MaterialInstanceConstant):
                    t = mel.get_material_instance_texture_parameter_value(m, n)
                else:
                    t = mel.get_material_default_texture_parameter_value(base, n)
            except Exception:
                t = None
            if t is None:
                continue
            out.setdefault(t.get_path_name(), []).append((m.get_path_name(), n, ROLE_BY_PARAM.get(n), decl.get(n)))
    return out


def _alpha_from_source(unreal, tex):
    try:
        mn, mx = _out(tex.compute_texture_source_channel_min_max(), 2)
        return mn.a < 1.0 - 0.5 / 255
    except Exception:
        return None


def apply(unreal, dest, mesh, glb=None, budgets=None):
    """Set every picture under dest; returns (summary line, counts). Prints one line per picture."""
    if not switch_on():
        line = summary_line(dest, {}, on=False)
        print(line)
        return line, {"off": 1}
    lib = unreal.EditorAssetLibrary
    cap, kind = kind_cap(dest, budgets)
    by_name = {}
    if glb and os.path.exists(glb):
        try:
            by_name = {im["name"]: im for im in glb_images(glb)}
        except Exception:
            by_name = {}
    binds = _bindings(unreal, dest, mesh)
    strict = strict_on()
    counts = {"textures": 0, "set": 0, "resized": 0, "refused": 0, "left": 0, "unchecked": 0, "readback_failed": 0}
    for path in lib.list_assets(dest, recursive=True, include_folder=False):
        tex = lib.load_asset(path)
        if not isinstance(tex, unreal.Texture2D):
            continue
        counts["textures"] += 1
        name = tex.get_name()
        b = binds.get(tex.get_path_name(), [])
        roles = {r for (_, _, r, _) in b if r}
        foreign = sorted({n for (_, n, r, _) in b if not r})
        src_w = int(tex.blueprint_get_size_x() or 0)
        src_h = int(tex.blueprint_get_size_y() or 0)
        gi = by_name.get(name, {})
        if not (src_w and src_h) and gi.get("w"):
            src_w, src_h = gi["w"], gi["h"]
        alpha = _alpha_from_source(unreal, tex)
        if alpha is None:
            alpha = gi.get("alpha_used") if gi.get("alpha_channel") is not None else None
        why = None
        if not b:
            why = "not-bound-by-any-material"
        elif not roles:
            why = "bound-only-under-" + "+".join(foreign)
        elif len({ROLE_SETTINGS[r] for r in roles}) > 1:
            why = "roles-disagree-" + "+".join(sorted(roles))
        if why:
            counts["left"] += 1
            print(texture_line(dest, name, "/".join(sorted(roles)) or None, (src_w, src_h), alpha, None, None, None,
                               "LEFT", why))
            continue
        role = sorted(roles)[0]
        p = plan(role, src_w, src_h, alpha, cap)
        derived = expected_sampler(p["compression"], p["srgb"])
        declared = [d for (_, _, r, d) in b if r]
        verdict = sampler_verdict(derived, declared)
        if verdict == "mismatch" or (verdict == "unchecked" and strict):
            counts["refused"] += 1
            print(texture_line(dest, name, role, (src_w, src_h), alpha, p, derived, declared, "REFUSED",
                               "sampler-%s:%s" % (verdict, ",".join("%s.%s" % (m.split("/")[-1], n)
                                                                   for (m, n, r, _) in b if r))))
            continue
        try:
            tex.modify()
            want = {"compression_settings": _enum(unreal, "TextureCompressionSettings", p["compression"]),
                    "srgb": p["srgb"],
                    "lod_group": _enum(unreal, "TextureGroup", p["lod_group"]),
                    "mip_gen_settings": _enum(unreal, "TextureMipGenSettings", p["mips"]),
                    "never_stream": False,
                    "compression_no_alpha": p["no_alpha"],
                    "power_of_two_mode": _enum(unreal, "TexturePowerOfTwoSetting", p["pot_mode"]),
                    "resize_during_build_x": int(p["resize"][0]),
                    "resize_during_build_y": int(p["resize"][1])}
            for k, v in want.items():
                tex.set_editor_property(k, v)
            bad = [k for k, v in want.items() if tex.get_editor_property(k) != v]
            lib.save_loaded_asset(tex, only_if_is_dirty=False)
        except Exception as e:
            bad = ["raised:" + str(e).splitlines()[0][:60] if str(e) else "raised"]
        if bad:
            counts["readback_failed"] += 1
            print(texture_line(dest, name, role, (src_w, src_h), alpha, p, derived, declared, "READBACK-FAILED",
                               ",".join(bad)))
            continue
        counts["set"] += 1
        counts["resized"] += p["pot_mode"] != "NONE"
        counts["unchecked"] += verdict == "unchecked"
        print(texture_line(dest, name, role, (src_w, src_h), alpha, p, derived, declared,
                           "SET" if verdict == "ok" else "SET-UNCHECKED", "cap=%d(%s)" % (cap, kind)))
    line = summary_line(dest, counts)
    print(line)
    return line, counts


# ---- selftest --------------------------------------------------------------------------------------------------------

def selftest():
    passed = failed = 0

    def ok(name, cond, detail=""):
        nonlocal passed, failed
        if cond:
            passed += 1
        else:
            failed += 1
            print("glb_texture_settings selftest FAIL %s: %s" % (name, detail))
    with open(BUDGETS, encoding="utf-8") as fh:
        budgets = json.load(fh)
    # the plan's B2 table, row by row (COOKING-PLAN-2026-11-09.md section 2)
    for (w, h), want in {(1215, 1120): (1024, 1024), (1243, 1050): (1024, 1024), (819, 1024): (1024, 1024),
                         (1150, 640): (1024, 512), (1006, 630): (1024, 512), (817, 409): (1024, 512),
                         (1006, 330): (1024, 256), (620, 450): (512, 512), (512, 597): (512, 512),
                         (512, 398): (512, 512), (907, 168): (1024, 128), (550, 380): (512, 256),
                         (512, 341): (512, 256), (341, 512): (256, 512), (1067, 144): (1024, 128),
                         (512, 171): (512, 128), (374, 186): (256, 128), (210, 296): (256, 256),
                         (475, 121): (512, 128), (414, 124): (512, 128), (300, 190): (256, 128),
                         (197, 188): (256, 128), (161, 188): (128, 128), (114, 191): (128, 128)}.items():
        ok("B2 %dx%d" % (w, h), target_size(w, h, 4096) == want, str(target_size(w, h, 4096)))
    ok("the fascia board 4096x512", target_size(5410, 550, 4096) == (4096, 512))
    ok("a power of two kept", target_size(1024, 512, 4096) is None)
    ok("over the cap halved together", target_size(4096, 1024, 2048) == (2048, 512))
    ok("the fronts' cap", kind_cap("/Game/Ledger/ShopFronts/chandler-front", budgets) == (4096, "frontage"))
    ok("the displays' cap", kind_cap("/Game/Ledger/ShopDisplays/x", budgets) == (2048, "display"))
    ok("the cars' cap", kind_cap("/Game/Ledger/Vehicles/hatch-navy", budgets) == (2048, "car"))
    p = plan("normal", 5410, 550, False, 4096)
    ok("normal plan", p["compression"] == "TC_NORMALMAP" and not p["srgb"] and p["resize"] == (4096, 512)
       and p["pot_mode"] == "RESIZE_TO_SPECIFIC_RESOLUTION" and p["mips"] == "TMGS_FROM_TEXTURE_GROUP"
       and p["no_alpha"] and not p["never_stream"], str(p))
    p = plan("orm", 512, 512, None, 4096)
    ok("orm plan, alpha unknown kept", p["compression"] == "TC_DEFAULT" and not p["srgb"] and not p["no_alpha"]
       and p["pot_mode"] == "NONE" and p["resize"] == (0, 0), str(p))
    ok("base colour and emissive sRGB on", plan("basecolor", 8, 8, True, 64)["srgb"] and plan("emissive", 8, 8, 1, 64)["srgb"])
    # the sampler each role derives (make_base_material's mirror of the engine's rule)
    ok("normal derives NORMAL", expected_sampler("TC_NORMALMAP", False) == "NORMAL")
    ok("orm derives LINEAR_COLOR", expected_sampler("TC_DEFAULT", False) == "LINEAR_COLOR")
    ok("colour derives COLOR", expected_sampler("TC_DEFAULT", True) == "COLOR")
    ok("declared enum spellings compared", sampler_verdict("LINEAR_COLOR", ["<MaterialSamplerType.SAMPLERTYPE_LINEAR_COLOR: 6>"]) == "ok"
       and sampler_verdict("LINEAR_COLOR", [compact("SAMPLERTYPE_LINEAR_COLOR")]) == "ok")
    ok("a mismatch refused", sampler_verdict("LINEAR_COLOR", ["MASKS"]) == "mismatch")
    ok("unread is unchecked", sampler_verdict("COLOR", [None]) == "unchecked")
    ok("a known mismatch beside an unread one is still a mismatch", sampler_verdict("COLOR", [None, "NORMAL"]) == "mismatch")
    ok("every glTF parameter has a role's settings", all(r in ROLE_SETTINGS for r in ROLE_BY_PARAM.values()))
    ok("summary line", summary_line("/Game/x", {"textures": 2, "set": 2}).startswith("glbTextures=OK dest=/Game/x textures=2 set=2")
       and summary_line("/Game/x", {"refused": 1}).startswith("glbTextures=PARTIAL"))
    ok("switch default on", switch_on() or os.environ.get("LEDGER_GLB_TEXTURE_SETTINGS") is not None)
    # a committed car reads from disk
    cars = sorted(glob.glob(os.path.join(REPO, "production/assets/vehicles", "*.glb")))
    if cars:
        try:
            ims = glb_images(cars[0])
            ok("a committed glb's pictures read", all("roles" in i for i in ims), cars[0])
        except Exception as e:
            ok("a committed glb's pictures read", False, str(e))
    print("glb_texture_settings selftest: passed=%d/%d failed=%d" % (passed, passed + failed, failed))
    return 1 if failed else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    if "--dry" in sys.argv:
        lines, tot = dry()
        for ln in lines:
            print(ln)
        print("glbTexturesDry glbs=%(glbs)d images=%(images)d wouldSet=%(set)d resized=%(resized)d fascia=%(fascia)d "
              "left=%(left)d" % tot)
        sys.exit(0)
    print(__doc__)
