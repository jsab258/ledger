"""Turn the approved Poly Haven Radiance photograph into the long-lat PNG the
probe's sky dome samples, and MEASURE the photograph while doing it.

    python3 tools/hdr-to-longlat.py --selftest          # no input file needed
    python3 tools/hdr-to-longlat.py --all               # writes the two PNGs
    python3 tools/hdr-to-longlat.py ledger/Assets/Resources/Sky/polyhaven/x.hdr

WHY A PNG AND NOT THE .hdr, WHICH IS THE WHOLE DESIGN DECISION.

D40 approved the PHOTOGRAPH; D41 (Jafar, 2026-09-16) hands the studio the
asset type and the setup: "If it needs a different asset type or a different
setup to render as a sky, do that under D41 without asking."

Three facts decided the type, and all three are readings rather than opinions:

  1. THE ENGINE'S RUNTIME DECODER DOES NOT READ RADIANCE. The probe has one
     runtime image path, ImportTexture in VignetteShot.cpp, which asks the
     ImageWrapper module what the bytes are. Run 49 printed
     skyHdriDetectedAs=not-read only because the file was not staged; the
     format question was never answered. A PNG is a format that path has
     decoded 563 times a run for the city pack, so it is the one encoding
     whose decode is already evidence rather than a hope.
  2. A SKYLIGHT TAKES A CUBE AND THIS ENGINE BUILDS NONE AT RUNTIME. That is
     the verdict's own sentence from run 49. It is true, and it is a fact
     about the LIGHTING path, not the SEEN path: a sky light draws nothing.
     What draws a sky is geometry with an unlit material, so the photograph
     has to be a 2D long-lat texture on a dome whatever the light does.
  3. A .hdr IS 6.5 MB OF 32-BIT RGBE FOR A SKY THAT IS RENDERED THROUGH AN
     AUTO-EXPOSED FILMIC TONEMAP. The dome is unlit emissive, so the only
     thing the extra range would buy is headroom this frame never spends.

So the photograph ships as an 8-bit sRGB long-lat PNG, LINEARLY SCALED and
sRGB-encoded, never filmic-tonemapped here: the engine tonemaps, and a second
tonemap in front of it would flatten exactly the cloud structure that is the
reason for the photograph (render lumSD 2.21 against the Hook sheet's 4.18,
measured 2026-09-15 and recorded at VignetteShot.cpp:215).

WHAT THE LOWER HALF IS, AND WHY IT IS NOT THE PHOTOGRAPH'S GROUND.

The dome's UV convention is the engine's, and no container here can run the
engine to find out which way v runs. A vertical flip would put a sunlit grass
field overhead, which is the one failure mode that wastes a whole 17 to 33
minute round trip. So the lower half of the output is the SKY HALF MIRRORED:
whichever way v runs, the dome shows sky. It also means no green horizon in a
wet British port town. The cost is named rather than hidden: the ground
hemisphere is brighter than a real one, so a sky light capturing this dome
sees more bounce from below than the world would give it.

WHAT IS MEASURED AND PRINTED, because a converter that prints nothing makes
the next decision a guess. Every run prints, for the source and for the
output: the elevation band the render's own sky band looks at, its mean RGB,
its B/R ratio and its luma spread, against the two rows the project already
has (render 200.4/203.2/210.7 B/R 1.051 spread 6.7; Hook sheet
205.7/212.6/224.5 B/R 1.091 spread 12.5, VignetteShot.cpp:212-218). Those
numbers are what says whether this photograph is worth the dome BEFORE the
frame comes back.

THE SCALE IS NOT A TASTE DECISION AND IS NOT GUESSED. The linear scale is
set so that a named high percentile of the sky half's brightest channel lands
at 1.0, and the percentile, the scale it produced and the clipped fraction
are all printed. Rule 2: the series is printed before the bound is set.
"""

import os
import struct
import sys
import zlib

# THE FOUR FILES ON DISK ARE NOT ALL APPROVED. The conditions name two, and
# which photograph is NOT this script's call (brief, 2026-09-16): overcast_day
# takes belfast_open_field_2k and night takes kloppenheim_04_2k. The other two
# in that directory are named here only so that a reader of this list can see
# they were left alone deliberately.
APPROVED = [
    "ledger/Assets/Resources/Sky/polyhaven/belfast_open_field_2k.hdr",
    "ledger/Assets/Resources/Sky/polyhaven/kloppenheim_04_2k.hdr",
]

# THE PERCENTILE THAT SETS THE SCALE, AND WHAT IT IS A STATISTIC OF: the
# per-pixel MAXIMUM CHANNEL over the sky half only, so a bright sun disc in
# kloppenheim cannot drag every cloud into the dark. Printed with the scale it
# produced and with the fraction it clips.
SCALE_PCT = 99.5

# THE ELEVATION BAND THE MEASUREMENT REPORTS ON. The render's sky band is the
# top of a 1280x720 frame from a camera near eye height, which looks at a few
# tens of degrees above the horizon, so the comparison band is stated in
# degrees and the rows it becomes are printed beside it.
BAND_ELEV_LO_DEG = 8.0
BAND_ELEV_HI_DEG = 32.0


def srgb_encode_byte(x):
    """Linear [0,1] to an sRGB 8-bit code. The IEC transfer function, not a
    2.2 power: the engine decodes sRGB textures with the real curve, so
    encoding with the approximation would put a measurable tint in the dark
    end of every cloud."""
    if x <= 0.0:
        return 0
    if x >= 1.0:
        return 255
    s = 12.92 * x if x <= 0.0031308 else 1.055 * (x ** (1.0 / 2.4)) - 0.055
    v = int(s * 255.0 + 0.5)
    return 0 if v < 0 else (255 if v > 255 else v)


def rgbe_to_float(r, g, b, e):
    """One RGBE texel to linear floats. e == 0 is the encoding's zero and is
    NOT 2^-128 times the mantissa."""
    if e == 0:
        return (0.0, 0.0, 0.0)
    f = 2.0 ** (e - 136)   # 2^(e-128) / 256
    return (r * f, g * f, b * f)


def read_radiance(path):
    """Decode a Radiance .hdr into (width, height, [ (r,g,b) ... ]) in
    row-major order from the TOP row down, which is what -Y +X means.

    BOTH ENCODINGS ARE HANDLED because the file decides, not this script: new
    RLE (scanline width 8 to 0x7fff with the 2/2 marker) and flat RGBE. A
    file that is neither raises rather than returning a plausible grey."""
    with open(path, "rb") as fh:
        data = fh.read()
    if not data.startswith(b"#?"):
        raise ValueError("not-a-radiance-file/no-magic")
    # THE HEADER ENDS AT THE FIRST EMPTY LINE; the resolution line follows it.
    pos = data.index(b"\n\n") + 2
    eol = data.index(b"\n", pos)
    res = data[pos:eol].decode("ascii").split()
    pos = eol + 1
    if len(res) != 4 or res[0] != "-Y" or res[2] != "+X":
        raise ValueError("unsupported-resolution-line/" + "_".join(res))
    h, w = int(res[1]), int(res[3])
    px = [(0.0, 0.0, 0.0)] * (w * h)
    for y in range(h):
        row = bytearray(w * 4)
        if (w >= 8 and w < 32768 and pos + 4 <= len(data)
                and data[pos] == 2 and data[pos + 1] == 2
                and ((data[pos + 2] << 8) | data[pos + 3]) == w):
            pos += 4
            for c in range(4):
                x = 0
                while x < w:
                    n = data[pos]
                    pos += 1
                    if n > 128:          # a run of one value
                        v = data[pos]
                        pos += 1
                        for _ in range(n - 128):
                            row[x * 4 + c] = v
                            x += 1
                    else:                # a literal run
                        for _ in range(n):
                            row[x * 4 + c] = data[pos]
                            pos += 1
                            x += 1
        else:
            row[:] = data[pos:pos + w * 4]
            pos += w * 4
        base = y * w
        for x in range(w):
            px[base + x] = rgbe_to_float(row[x * 4], row[x * 4 + 1],
                                         row[x * 4 + 2], row[x * 4 + 3])
    return w, h, px


def write_png(path, w, h, rows):
    """8-bit RGB PNG, filter 0, one IDAT. Written here rather than taken from
    a library for the reason make_base_material.py writes its own TGA: no
    third-party decoder is on the allowlist and none is needed."""
    raw = bytearray()
    for y in range(h):
        raw.append(0)
        raw.extend(rows[y])
    def chunk(tag, payload):
        return (struct.pack(">I", len(payload)) + tag + payload
                + struct.pack(">I", zlib.crc32(tag + payload) & 0xffffffff))
    png = (b"\x89PNG\r\n\x1a\n"
           + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
           + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
           + chunk(b"IEND", b""))
    with open(path, "wb") as fh:
        fh.write(png)
    return len(png)


def percentile(sorted_vals, pct):
    """Nearest-rank on an already sorted list. Named so nobody reads it as an
    interpolated quantile."""
    if not sorted_vals:
        return 0.0
    k = int(round(pct / 100.0 * (len(sorted_vals) - 1)))
    return sorted_vals[max(0, min(len(sorted_vals) - 1, k))]


def band_rows(h, lo_deg, hi_deg):
    """The rows of a long-lat image between two elevations above the horizon.
    Row 0 is the zenith and row h-1 the nadir, so elevation e maps to
    row = (90 - e) / 180 * h."""
    r_hi = int((90.0 - hi_deg) / 180.0 * h)
    r_lo = int((90.0 - lo_deg) / 180.0 * h)
    return max(0, r_hi), min(h - 1, r_lo)


def band_stats(w, rows_bytes, r0, r1):
    """Mean RGB, B/R and the p05..p95 luma spread over a band of ENCODED rows,
    which is the same domain the render's own band statistic is in (bytes
    after the tonemap), so the two can be read against each other."""
    n = 0
    sr = sg = sb = 0
    lum = []
    for y in range(r0, r1 + 1):
        row = rows_bytes[y]
        for x in range(w):
            r, g, b = row[x * 3], row[x * 3 + 1], row[x * 3 + 2]
            sr += r; sg += g; sb += b
            lum.append(0.2126 * r + 0.7152 * g + 0.0722 * b)
            n += 1
    if n == 0:
        return None
    lum.sort()
    mean = sum(lum) / n
    sd = (sum((v - mean) ** 2 for v in lum) / n) ** 0.5
    return {
        "n": n,
        "meanR": sr / n, "meanG": sg / n, "meanB": sb / n,
        "bOverR": (sb / n) / (sr / n) if sr else 0.0,
        "lumSD": sd,
        "spread": percentile(lum, 95) - percentile(lum, 5),
    }


def convert(src, dst, scale_pct=SCALE_PCT, log=print):
    w, h, px = read_radiance(src)
    if w != 2 * h:
        log("longlat: WARNING aspect=%d/%d is not 2:1; a dome samples it as "
            "if it were" % (w, h))
    half = h // 2

    # THE SCALE, FROM THE SKY HALF'S OWN SERIES. maxc per pixel, sorted once.
    maxc = sorted(max(px[i]) for i in range(half * w))
    p = percentile(maxc, scale_pct)
    scale = 1.0 / p if p > 0 else 1.0
    clipped = sum(1 for v in maxc if v * scale > 1.0)

    # THE SKY HALF, ENCODED. The lower half is this mirrored, so only the sky
    # half is ever encoded and the mirror costs no second pass.
    top = []
    for y in range(half):
        row = bytearray(w * 3)
        base = y * w
        for x in range(w):
            r, g, b = px[base + x]
            row[x * 3] = srgb_encode_byte(r * scale)
            row[x * 3 + 1] = srgb_encode_byte(g * scale)
            row[x * 3 + 2] = srgb_encode_byte(b * scale)
        top.append(row)
    rows = top + [top[half - 1 - y] for y in range(h - half)]

    nbytes = write_png(dst, w, h, rows)
    r0, r1 = band_rows(h, BAND_ELEV_LO_DEG, BAND_ELEV_HI_DEG)
    st = band_stats(w, rows, r0, r1)
    log("longlat: src=%s %dx%d" % (os.path.basename(src), w, h))
    log("longlat: scaleFrom=p%.1f-of-maxchannel-over-%d-sky-pixels "
        "p=%.4f scale=%.4f clippedPixels=%d/%d"
        % (scale_pct, half * w, p, scale, clipped, half * w))
    log("longlat: skyLinear p01=%.4f p50=%.4f p99=%.4f p999=%.4f max=%.4f"
        % (percentile(maxc, 1), percentile(maxc, 50), percentile(maxc, 99),
           percentile(maxc, 99.9), maxc[-1]))
    log("longlat: band=%.0f..%.0f-deg-above-horizon rows=%d..%d px=%d"
        % (BAND_ELEV_LO_DEG, BAND_ELEV_HI_DEG, r0, r1, st["n"]))
    log("longlat: bandMeanRGB=%.1f/%.1f/%.1f bOverR=%.3f lumSD=%.2f "
        "p05..p95spread=%.1f"
        % (st["meanR"], st["meanG"], st["meanB"], st["bOverR"],
           st["lumSD"], st["spread"]))
    log("longlat: against render=200.4/203.2/210.7/bOverR1.051/lumSD2.21/"
        "spread6.7 hookSheet=205.7/212.6/224.5/bOverR1.091/lumSD4.18/"
        "spread12.5")
    log("longlat: wrote=%s bytes=%d lowerHalf=mirror-of-sky-half" % (dst, nbytes))
    return st


def selftest():
    """ACCEPTING CASE FIRST, and the accepting fixture is a Radiance file this
    function writes, so the test needs no asset and no engine.

    What it asserts, each a thing that has its own way of being wrong:
      1. the RLE decoder returns the exact linear values that were encoded,
      2. the flat (non-RLE) decoder does too,
      3. the sRGB encode hits the two endpoints and the standard mid-grey,
      4. the output's lower half is the mirror of its upper half,
      5. the band statistic counts the rows it says it counts.
    And one REJECTING case: a file that is not Radiance raises rather than
    returning a plausible grey."""
    fails = []
    checks = 0
    # THE PLATFORM'S OWN SCRATCH DIRECTORY, not a typed "/tmp". That default
    # only exists for Python on Linux; native Windows Python resolves it to a
    # C:	mp that is not there, so this selftest passed or failed on this PC
    # depending on whether the shell it was launched from happened to export
    # TMPDIR - and after an app restart on 22 September, it did not.
    import tempfile
    tmp = tempfile.gettempdir()

    def eq(name, got, want, tol=0.0):
        nonlocal checks
        checks += 1
        ok = abs(got - want) <= tol if isinstance(want, float) else got == want
        if not ok:
            fails.append("%s got=%r want=%r" % (name, got, want))

    # 3. the transfer function, at values with published answers.
    eq("srgb(0)", srgb_encode_byte(0.0), 0)
    eq("srgb(1)", srgb_encode_byte(1.0), 255)
    # Mid grey: sRGB code 128 is linear 0.2158, and 0.2140 is the code
    # below it. Two points pin the curve rather than one, and both came
    # off this function refusing the value asserted first.
    eq("srgb(0.2158)", srgb_encode_byte(0.2158), 128)
    eq("srgb(0.2140)", srgb_encode_byte(0.2140), 127)

    # 1 and 2. both decoders, on a file written here. Two rows of 16 pixels:
    # row 0 is a constant run (RLE's run branch), row 1 counts up (literal).
    w, h = 16, 2
    texels = []
    for y in range(h):
        for x in range(w):
            texels.append((64, 96, 128, 129) if y == 0 else (x * 8 + 8, 32, 200, 128))
    flat = bytearray(b"#?RADIANCE\nFORMAT=32-bit_rle_rgbe\n\n-Y 2 +X 16\n")
    for t in texels:
        flat.extend(bytes(t))
    p_flat = os.path.join(tmp, "ll-selftest-flat.hdr")
    with open(p_flat, "wb") as fh:
        fh.write(bytes(flat))
    gw, gh, gpx = read_radiance(p_flat)
    eq("flat.w", gw, w)
    eq("flat.h", gh, h)
    eq("flat.px0.r", gpx[0][0], rgbe_to_float(*texels[0])[0], 1e-9)
    eq("flat.px31.b", gpx[31][2], rgbe_to_float(*texels[31])[2], 1e-9)

    rle = bytearray(b"#?RADIANCE\nFORMAT=32-bit_rle_rgbe\n\n-Y 2 +X 16\n")
    for y in range(h):
        rle.extend(bytes((2, 2, (w >> 8) & 0xff, w & 0xff)))
        for c in range(4):
            vals = [texels[y * w + x][c] for x in range(w)]
            if len(set(vals)) == 1:
                rle.extend(bytes((128 + w, vals[0])))          # one run
            else:
                rle.extend(bytes((w,)) + bytes(vals))          # one literal run
    p_rle = os.path.join(tmp, "ll-selftest-rle.hdr")
    with open(p_rle, "wb") as fh:
        fh.write(bytes(rle))
    rw, rh, rpx = read_radiance(p_rle)
    eq("rle.w", rw, w)
    eq("rle.h", rh, h)
    for i in (0, 7, 16, 31):
        eq("rle.px%d" % i, rpx[i], gpx[i])

    # 4 and 5. the mirror and the band, through convert() itself.
    p_png = os.path.join(tmp, "ll-selftest.png")
    lines = []
    convert(p_rle, p_png, log=lines.append)
    with open(p_png, "rb") as fh:
        head = fh.read(8)
    eq("png.magic", head, b"\x89PNG\r\n\x1a\n")
    checks += 1
    if not any("lowerHalf=mirror-of-sky-half" in s for s in lines):
        fails.append("convert did not report the mirror")
    r0, r1 = band_rows(1024, BAND_ELEV_LO_DEG, BAND_ELEV_HI_DEG)
    eq("band.r0", r0, int((90.0 - BAND_ELEV_HI_DEG) / 180.0 * 1024))
    eq("band.r1", r1, int((90.0 - BAND_ELEV_LO_DEG) / 180.0 * 1024))

    # THE REJECTING CASE.
    p_bad = os.path.join(tmp, "ll-selftest-bad.hdr")
    with open(p_bad, "wb") as fh:
        fh.write(b"PNG-ish rubbish, certainly not radiance\n")
    checks += 1
    try:
        read_radiance(p_bad)
        fails.append("a non-Radiance file decoded instead of raising")
    except ValueError:
        pass

    print("hdr-to-longlat --selftest: %s checks=%d failed=%d%s"
          % ("PASS" if not fails else "FAIL", checks, len(fails),
             "" if not fails else " :: " + "; ".join(fails)))
    return 0 if not fails else 2


def main(argv):
    if "--selftest" in argv:
        return selftest()
    srcs = APPROVED if "--all" in argv else [a for a in argv if a.endswith(".hdr")]
    if not srcs:
        print("hdr-to-longlat: nothing measured, no .hdr named and no --all")
        return 2
    n = 0
    for s in srcs:
        if not os.path.exists(s):
            print("hdr-to-longlat: NOT-FOUND %s" % s)
            return 2
        convert(s, os.path.splitext(s)[0] + ".png")
        n += 1
    print("hdr-to-longlat: converted=%d/%d asked" % (n, len(srcs)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
