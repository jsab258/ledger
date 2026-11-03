# Sodium light in an RGB renderer: first-pass reading

Read 3 November 2026. Lists methods found; no recommendation. Few sources were reached; most of the answers are gaps.

## Q1. Monochromatic source in RGB: a scalar reflectance at 589 nm

- Jakob and Hanika 2019 (sigmoid of a quadratic polynomial per RGB triple, stored in a coefficient table): only the abstract page was read (https://rgl.epfl.ch/publications/Jakob2019Spectral, read 3 Nov 2026). It says a spectral value at any wavelength costs about six floating-point operations and the fit is exact across sRGB. The page gives no value or weight at 589 nm, and no coefficients. The full PDF (rgl.s3.eu-central-1.amazonaws.com/.../Jakob2019Spectral.pdf) returned HTTP 403 and was not used.
- The method, as the abstract states it, would give reflectance at 589 nm from the surface's RGB albedo by evaluating the fitted curve at 589 nm. The per-colour numbers for brick are UNVERIFIED (not obtained).
- Smits 1999: not reached. Any weights are UNVERIFIED.
- Compare: the plain luminance of an albedo is not a published estimate of 589 nm reflectance. This is the writer's note, not a source.

## Q2. How games and film VFX handled sodium light

- No write-up on sodium street light in games or VFX was found. A standard search returned only general Unreal desaturation threads (https://forums.unrealengine.com/t/local-desaturation/310266, https://forums.unrealengine.com/t/desaturated-global-light-saturated-spotlights/295099/1). Those were seen as search results only and not read in full; their content is UNVERIFIED.
- Techniques the search results described (UNVERIFIED, from snippets): desaturating inside a mask from custom-depth spheres; a sphere-mask post process; a global desaturate node in a post-process material.
- GDC and SIGGRAPH talks, Unity forums, and technical-artist posts on sodium: not found, not reached.

## Q3. Unreal Engine 5: a per-surface monochrome light

All pages read in full by fetch on 3 Nov 2026.

- Light functions (https://dev.epicgames.com/documentation/en-us/unreal-engine/using-light-functions-in-unreal-engine): a material in the Light Function domain feeds Emissive Color and filters the light's intensity. Default atlas format is grayscale; 8-bit RGB is possible and "Colored light functions require the project setting Deferred Lighting Uses Light Function Atlas". Lights must be Movable or Stationary. In the atlas path "You cannot sample the GBuffer" or depth buffer or world position. So per the page, a light function cannot read the lit surface's albedo. It can filter the light's own colour or intensity by position in the light's projection.
- Lighting channels (https://dev.epicgames.com/documentation/en-us/unreal-engine/using-lighting-channels-in-unreal-engine): up to 3 channels; a light affects only actors sharing a channel. Dynamic lights only (Stationary or Movable); opaque surfaces only for direct light; translucent and masked excluded. The page does not mention Lumen, so the Lumen behaviour is UNVERIFIED. The page offers no per-surface colour change, only inclusion or exclusion.
- Post-process materials (https://dev.epicgames.com/documentation/en-us/unreal-engine/post-process-materials-in-unreal-engine): can read SceneTexture (PostProcessInput0, GBuffer on the deferred path, Custom Depth, Custom Depth Stencil). Before Tonemapping gives HDR colour. The page warns that SceneColor lookups may not give right results, and GBuffer pixels do not map 1:1 under anti-aliasing. The page does not name base colour as a GBuffer field; UNVERIFIED. It does show a mask (custom depth/stencil) can limit an effect to chosen meshes, but not "inside a lamp's pool" directly.
- The lamp's light colour only sets RGB multiplied by albedo; no engine page read says otherwise. A custom shading model: no documentation page read; UNVERIFIED, and no page fetched on Substrate.

## Q4. 1980s and 1990s photographs and films of SOX-lit streets

- Wikipedia, Sodium-vapor lamp (https://en.wikipedia.org/wiki/Sodium-vapor_lamp, read 3 Nov 2026): low-pressure sodium emits "virtually monochromatic light averaging a 589.3 nm wavelength" (two lines at 589.0 and 589.6 nm); colours are "difficult to distinguish"; a photo caption has a bright red car looking black. No CRI number given.
- Cinematography Mailing List thread (https://cinematography.net/edited-pages/Street_Lighting.htm, read 3 Nov 2026, no post dates shown): Brian Heller, "LPS ... near Zero CRI" and "every object with colour will be seen as a shade of brown or black"; David Perrault: "there is a big green spike" that is "usually problematic" and "a disappointing skew to the colour and it's pretty easy to underexpose". The thread is about modern shooting, not 1980s or 1990s stock.
- Photrio thread "shooting color film under sodium vapor lights" (https://www.photrio.com/forum/threads/shooting-color-film-under-sodium-vapor-lights.64780): HTTP 403, not read. A search snippet claimed colour negative is "insensitive to the yellow light", UNVERIFIED and unused.
- The brief's "greenish cast on colour negative": not confirmed by any page read, except Perrault's "green spike" remark above, whose source (lamp or film) is unclear. Period photographs and period film frames of SOX streets: not reached.

## Not reached

Jakob and Hanika PDF (403); Smits 1999; Photrio thread (403); the Unreal forum threads (snippets only); any GDC, SIGGRAPH or Unity sources; Epic pages on custom shading models or Substrate; period photographs and film-stock datasheets.
