# Step 9 metal trim sheet: CC0 painted-metal reading, 3 November 2026

Licence allowlist read first (ledger-v2/research/license-allowlist.md): CC0 libraries (Poly Haven, ambientCG) are ship-safe, item 2.

Method note: pages were fetched by URL and read through the fetch tool's page summary (a small model's extract of the whole page), not as raw HTML or pictures. No picture of any texture was seen, so look, flatness and colour are only as stated in page text or tags. No downloads, cookies or logins.

## 1. ambientCG (all reached; all state CC0 via the site FAQ line "All assets are released under the Creative Commons CC0 license"; none states a real-world size)

Base URL: https://ambientcg.com/view?id=<Id>. Read 3 Nov 2026.

| Id | Tags on page | Resolutions |
|---|---|---|
| PaintedMetal001 | painted, scratches, yellow | 1K, 2K, 4K |
| PaintedMetal002 | blue, painted, scratched | 1K, 2K, 4K |
| PaintedMetal003 | blue, painted | 1K, 2K, 4K |
| PaintedMetal004 | red, painted; procedural (parent PaintedMetalSubstance001) | 1K, 2K, 4K |
| PaintedMetal005 | green, painted; procedural | 1K, 2K, 4K |
| PaintedMetal006 | green, painted, rust; procedural | 1K to 8K |
| PaintedMetal007 | blue, painted, rust; procedural | 1K to 8K |
| PaintedMetal008 | orange, painted, rust | 1K to 8K |
| PaintedMetal009 | yellow, painted, rust | 1K to 8K |
| PaintedMetal010 | white, painted, rust | 1K to 8K |
| PaintedMetal011 | painted, rust (no colour tag) | 1K to 8K |
| PaintedMetal012 | white, painted, rust | 1K to 8K |
| PaintedMetal013 | painted, rust (no colour tag) | 1K to 8K |
| PaintedMetal014 | grey, painted, rust | 1K to 8K |
| PaintedMetal015 | painted, rust (no colour tag) | 1K to 8K |
| PaintedMetal016 | yellow, stripes, painted, rust | 1K to 8K |
| PaintedMetal017 | danger sign, painted, rust | 1K to 8K |

Finding: no ambientCG page says flat or corrugated, black paint, or chips; page text carries tags only. No page is tagged black. PaintedMetal011, 013 and 015 have no colour tag, so their colour is unverified. Flatness and edge chipping of all 17 are unverified (would need the preview picture). Metal0xx and MetalPlates ids were not tried.

## 2. Poly Haven (all reached, all CC0 on the page; read 3 Nov 2026)

| Page | Size covered | Flat? | Colour / wear |
|---|---|---|---|
| https://polyhaven.com/a/rusty_metal_02 | 1 m wide; 1K 10.2, 2K 20.5, 4K 41, 8K 81.9 px/cm | Flat (category Flat Sheet), displacement map | "weathered painted metal with orange-brown rust speckles"; base paint colour not stated |
| https://polyhaven.com/a/green_metal_rust | 1 m wide; 1K to 8K | Flat (Flat Sheet) | green paint, rust streaks round fasteners; tags painted, ship, tank |
| https://polyhaven.com/a/metal_plate_02 | 2 m wide; 8K = 41 px/cm | Flat (Flat Sheet) | rusty oxidised iron, worn; not painted-tagged |
| https://polyhaven.com/a/blue_metal_plate | 2.5 m wide; up to 16K | Flat (Flat Sheet) | painted blue steel, scratched and scuffed; no rust stated |
| https://polyhaven.com/a/metal_plate | 0.5 m wide | Raised diamond pattern, not flat | grey steel, chipped green paint, rust |
| https://polyhaven.com/a/rusty_metal | 1.5 m wide | Not flat (dented corrugated shutter) | brown-orange corrosion |

Not reached: https://polyhaven.com/a/painted_metal_02 (HTTP 404; the slug does not exist).

## 3. Best candidate (a reading, not the decision)

Poly Haven Rusty Metal 02: flat, described as painted, worn, rust speckles, CC0, 1 m tile. At 1 m per tile, 512 px/m is 512 px per tile; the 1K download (about 1024 px/m, 10.2 px/cm) already exceeds the target, so scale needs no change (use 1K, or mip down). Needs changing: base colour (not stated, orange-brown rust seen only in text) must be darkened or tinted to near-black paint, keeping the rust speckles as chips at edges; roughness raised for old gloss paint. Whether the speckle density reads as chipped cast iron is unverified until the preview is looked at.

Runner-up: Green Metal Rust (flat, painted, 1 m, rust at fasteners); the same dark tint needed. ambientCG offers nothing confirmed flat and dark.
