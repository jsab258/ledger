"""The wet road's numbers: what each measured region asks of the reflection, in linear light.

    python road_numbers.py      -> prints the table used in ROAD-NOTES.md

1. Frame values (8-bit, the builder's gate measurements) to the tone-mapped linear value
   (sRGB transfer), then back through the engine's own inverse of its film curve
   (UE 5.8.2 Engine/Shaders/Private/TonemapCommon.ush:227-256, FilmToneMapInverse, default curve).
2. The road is nearly all reflection (asphalt surface gain 0.13), so the ratio target/now in
   scene-linear light is the factor the reflection must fall by.
3. The engine's reflectance of a smooth wet surface at each angle above the road:
   E = W (A F0 + B F90), F90 = saturate(50 F0)  (ShadingEnergyConservationTemplate.ush:46-63, 66-87;
   ShadingCommon.ush:161), A and B the split-sum GGX integrals (Karis 2013, as SystemTextures.cpp
   builds PreIntegratedGF), integrated here numerically.
"""
import math

import numpy as np


def srgb_to_linear(v8):
    c = v8 / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def film_inverse(w):
    """TonemapCommon.ush FilmToneMapInverse for a grey value (desaturation steps are identities)."""
    toe = 0.374816 * (0.9 / min(w, 0.8) - 1) ** -0.588729
    shoulder = 0.227986 * (1.56 / (1.04 - w) - 1) ** 1.02046
    t = min(max((w - 0.35) / (0.45 - 0.35), 0.0), 1.0)
    t = (3 - 2 * t) * t * t
    return toe + (shoulder - toe) * t


def scene_linear(v8):
    return film_inverse(srgb_to_linear(v8))


def split_sum(roughness, nov, n=4096):
    """Karis's split-sum terms A, B (reflectance = A F0 + B F90) for GGX, importance sampled."""
    a = roughness ** 2
    V = np.array([math.sqrt(1 - nov * nov), 0.0, nov])
    i = np.arange(n)
    u1 = (i + 0.5) / n
    u2 = np.array([int('{:032b}'.format(k)[::-1], 2) / 2 ** 32 for k in i])
    phi = 2 * math.pi * u2
    cos_t = np.sqrt((1 - u1) / (1 + (a * a - 1) * u1))
    sin_t = np.sqrt(1 - cos_t ** 2)
    H = np.stack([sin_t * np.cos(phi), sin_t * np.sin(phi), cos_t], 1)
    VoH = H @ V
    L = 2 * VoH[:, None] * H - V
    NoL = np.clip(L[:, 2], 0, 1)
    NoH = np.clip(H[:, 2], 0, 1)
    VoH = np.clip(VoH, 0, 1)
    ok = NoL > 0
    k = a / 2
    def g1(x):
        return x / (x * (1 - k) + k)
    G = g1(nov) * g1(NoL)
    Gv = np.where(ok, G * VoH / np.maximum(NoH * nov, 1e-9), 0)
    Fc = (1 - VoH) ** 5
    A = np.mean((1 - Fc) * Gv)
    B = np.mean(Fc * Gv)
    return A, B


def engine_reflectance(roughness, elev_deg, specular=0.5):
    """UE 5.8 with energy conservation on (r.Shading.EnergyConservation defaults to 1)."""
    F0 = 0.08 * specular
    F90 = min(max(50 * F0, 0.0), 1.0)
    nov = math.sin(math.radians(elev_deg))
    A, B = split_sum(roughness, nov)
    Ex = A + B
    W = 1 + F0 * (1 - Ex) / Ex
    return W * (A * F0 + B * F90)


def fresnel_water(elev_deg, n=1.333):
    ti = math.radians(90 - elev_deg)
    ci = math.cos(ti)
    st = math.sin(ti) / n
    ct = math.sqrt(1 - st * st)
    rs = ((ci - n * ct) / (ci + n * ct)) ** 2
    rp = ((ct - n * ci) / (ct + n * ci)) ** 2
    return 0.5 * (rs + rp)


def row_angle(row, height=1440, vfov=46.0, pitch=-3.4):
    f = (height / 2) / math.tan(math.radians(vfov / 2))
    return math.degrees(math.atan((row - height / 2) / f)) - pitch   # degrees below the horizon


if __name__ == "__main__":
    regions = [  # view, region, now, sheet (8-bit, the builder's gate, GATE-SKY-REVIEW.md 17-18)
        ("hook", "near lane", 207, 152),
        ("reverse", "centre", 196, 164),
        ("reverse", "middle", 222, 183),
    ]
    print("view     region     now sheet  lin_now lin_sheet  factor")
    for v, r, a, b in regions:
        ln, lt = scene_linear(a), scene_linear(b)
        print("%-8s %-9s %4d %5d  %7.3f %9.3f  %6.2f" % (v, r, a, b, ln, lt, lt / ln))
    print()
    print("rows -> degrees below the horizon (= the mirrored sky's elevation)")
    for row in (900, 1000, 1100, 1200, 1300, 1440):
        print("  row %4d: %.1f deg" % (row, row_angle(row)))
    print()
    print("elev  water-Fresnel  engine r=0.10 S=0.5  r=0.10 S=0.25  r=0.10 S=0.15  r=0.30 S=0.5")
    for e in (3, 5, 8, 10, 12, 15, 20, 25):
        print("%4d   %6.3f        %6.3f            %6.3f         %6.3f         %6.3f" % (
            e, fresnel_water(e), engine_reflectance(0.10, e), engine_reflectance(0.10, e, 0.25),
            engine_reflectance(0.10, e, 0.15), engine_reflectance(0.30, e)))


def to_frame(x):
    """Scene-linear back to 8-bit: invert film_inverse by bisection, then the sRGB transfer."""
    lo, hi = 1e-4, 0.999
    for _ in range(60):
        m = 0.5 * (lo + hi)
        if film_inverse(m) < x:
            lo = m
        else:
            hi = m
    w = 0.5 * (lo + hi)
    c = 12.92 * w if w <= 0.0031308 else 1.055 * w ** (1 / 2.4) - 0.055
    return 255 * c


def predict():
    """Each region with the film's Specular lowered: the reflection scales by the engine's own
    ratio at the region's typical angle (the diffuse part, asphalt gain 0.13, is left aside)."""
    regions = [("hook", "near lane", 207, 152, 20.0), ("reverse", "centre", 196, 164, 20.0),
               ("reverse", "middle", 222, 183, 13.0)]
    print("\nSpecular  " + "  ".join("%s %s (sheet %d)" % (v, r, b) for v, r, a, b, e in regions))
    for S in (0.5, 0.25, 0.15, 0.135, 0.125, 0.115, 0.10):
        cells = []
        for v, r, a, b, e in regions:
            k = engine_reflectance(0.10, e, S) / engine_reflectance(0.10, e, 0.5)
            cells.append("%5.0f (%+4.0f, x%.2f)" % (to_frame(scene_linear(a) * k), to_frame(scene_linear(a) * k) - b, k))
        print("%6.3f    " % S + "   ".join(cells))


if __name__ == "__main__":
    predict()
