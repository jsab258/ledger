# Fabric properties from public sources, for Kiln

In short: published papers give reliable weights and thicknesses for most target cloths and stretch, bend and shear numbers for plain cotton, wool and polyester; denim, nylon shell, melton and rib stiffness are still gaps.

Date read: 2026-11-18 (every source below was read on this date unless marked not reached).
Purpose: replace Kiln fabric and solver values that came from another product's files with values from papers, public datasets and official manuals only. No product files, presets or binaries were opened.

Status words used below:
- verified: the number was read in the primary source (paper PDF or official manual page) during this run.
- derived: computed here from verified numbers; the arithmetic is shown.
- unverified: seen only in a snippet, a retailer page, or a source whose units were not stated.
- gap: nothing public was found in this run.

## Short answer

1. Usable measured numbers exist for density and thickness of every target fabric except the knit jumper (thickness only) and the nylon shell (weight only, from a retailer). Small-strain tensile moduli with warp, weft and bias exist for plain cotton, plain wool and plain polyester (Penava 2014). KES bending and shear exist for a plain wool, a wool/polyester blend and a polyester (Kim and Son 2006).
2. No source read in this run gives measured stretch or bending numbers for denim, a 1980s light nylon taffeta, wool melton, or a 1x1 / 2x2 rib in a form that can be copied straight in. Those cells are gaps or proxies, named in the table.
3. The graphics datasets (Wang 2011, Clyde 2017) give density and thickness tables in the paper, but their fitted stiffness curves are not printed as numbers in the text read; Wang's data is in a separate download whose licence was not reached.
4. XPBD compliance is simply inverse stiffness, scaled by the time step squared inside the solver. With a membrane stiffness per unit width Y (N/m) on a regular grid, edge compliance is about 1/Y and does not depend on resolution. Mass per point is areal density times one third of the area of the triangles touching it.
5. Official manuals give very few numeric solver defaults. The ones found are listed in section 3 with their exact source.

## 1. Measured datasets and papers

### 1.1 Wang, O'Brien, Ramamoorthi 2011
- Title: Data-Driven Elastic Models for Cloth: Modeling and Measurement. ACM Transactions on Graphics 30(4) (SIGGRAPH 2011).
- URL read: https://wanghmin.github.io/publication/wang-2011-dde/Wang-2011-DDE.pdf (read 2026-11-18).
- What was measured: ten fabrics. Stretching by a loaded-sheet test (400 x 400 mm samples at 0, 45 and 90 degrees, bottom weights 0 to 600 g, side weights 0 to 400 g, 35 tests per sample, tracked by a calibrated camera). Bending by a cantilever drape of 4 cm strips at 0, 45 and 90 degrees.
- Densities printed in Table 1 (kg/m2), verified:
  - 11oz Black Denim, 99% cotton 1% spandex, jeans: 0.324 (weave not stated in Table 1)
  - Royal Target, 65% cotton 35% polyester, "pants": 0.220 (weave not stated)
  - Ivory Rib Knit, 95% cotton 5% spandex: 0.276
  - Gray Interlock, 60% cotton 40% polyester, T-shirt: 0.187
  - Navy Sparkle Sweat, 96% polyester 4% spandex, sweater: 0.224
  - Camel Ponte Roma, 60% polyester 40% rayon, jacket: 0.284
  - Tango Red Jet Set, 100% polyester, dress: 0.113
  - White Dots on Black, 100% polyester: 0.128
  - Pink Ribbon Brown, 100% polyester: 0.228
  - White Swim Solid, 87% nylon 13% spandex: 0.204
- Stiffness: given only as plotted piecewise curves (c11, c12, c22, c33 against strain) and one bending plot; no thickness. No numeric stiffness was taken from the paper text.
- Data and terms: the paper says the database (raw images, fitted parameters, textures) is downloadable from a Berkeley page named in the paper. That page was not fetched in this run, so its licence is unknown. The paper itself carries the ACM notice allowing personal or classroom copies without fee; commercial use needs permission. Whether that applies to the data is not stated. Treat the fitted parameters as not cleared until the data page's terms are read.

### 1.2 Miguel et al. 2012
- Title: Data-Driven Estimation of Cloth Simulation Models. E. Miguel, D. Bradley, B. Thomaszewski, B. Bickel, W. Matusik, M. A. Otaduy, S. Marschner. Computer Graphics Forum 31(2), Eurographics 2012. DOI 10.1111/j.1467-8659.2012.03031.x
- URL read: https://diglib.eg.org/items/47cce290-0a8f-4daf-8e2a-1ff6a2c23d2b/full (metadata and abstract only, read 2026-11-18).
- What was measured (from the abstract only): full 3D deformation of cloth samples under several tests, used to fit and compare several nonlinear cloth models.
- Not reached: the PDF. The MIT link in search results returned a publication index, not the paper. Fabric list, values and data terms are therefore unknown from this run.

### 1.3 Clyde, Teran, Tamstorf 2017
- Title: Modeling and Data-Driven Parameter Estimation for Woven Fabrics. D. Clyde, J. Teran, R. Tamstorf. SCA 2017. DOI 10.1145/3099564.3099577
- URL read: https://www.math.ucdavis.edu/~jteran/papers/CTT17.pdf (read 2026-11-18).
- Tests: uniaxial tensile on an Instron 5569 (modified ASTM D5035, strips 75 x 50 mm, 150 mm for denim and wool) at warp, weft and bias; bending by ASTM D1388 cantilever (25 x 200 mm strip, 41.5 degree plane); density by ASTM D3776; thickness by ASTM D1777. Testing by Vartest Laboratories.
- Table 2, verified:
  - Canvas, basket: 294.0 g/m2, 0.53 mm, 108 x 56 threads/inch
  - Cotton poplin, plain: 103.6 g/m2, 0.18 mm, 140 x 86
  - Silk charmeuse, satin: 83.0 g/m2, 0.18 mm
  - Wool coating, twill: 480.6 g/m2, 1.28 mm, 32 x 28
  - Denim, twill: 400.0 g/m2, 0.66 mm, 70 x 47
- Fitted moduli: the paper's text read here lists parameter names but not fitted values; it reports fit errors and bend-test angles (for example canvas warp 54.6 degrees, weft 23.7 degrees against a 41.5 degree target). A supplemental document was not reached.
- Data terms: not stated in the paper. The density and thickness figures are cited facts from a published paper.

### 1.4 Kawabata Evaluation System (KES) values
KES-FB reports, per direction: EMT (tensile strain at the maximum test load, %), LT (linearity), WT (tensile energy), B (bending rigidity, gf cm2/cm), 2HB (bending hysteresis), G (shear rigidity, gf/cm/degree), 2HG.

- Kim, J.-J. and Son, Y.-K. 2006. Physical Properties of Ultra-fine Denier Filament Yarn Fabric. Journal of Fashion Business 10(3), 23-30. URL read: https://koreascience.kr/article/JAKO200633063796294.pdf (read 2026-11-18). Verified values (warp / weft):
  - Wool 100%: 181.2 g/m2, 0.579 mm (T0); EMT 5.69 / 8.52 %; B 0.0593 / 0.0459 gf cm2/cm; G 0.61 / 0.56 gf/cm deg
  - Wool 50 / polyester 50: 181.4 g/m2, 0.630 mm; EMT 9.71 / 3.46 %; B 0.0720 / 0.1027; G 0.66 / 0.64
  - Polyester 100% (ultra-fine filament): 155.1 g/m2, 0.659 mm; EMT 3.88 / 1.63 %; B 0.0398 / 0.0525; G 1.20 / 0.85
  - Weave not stated in the extract.
- Ramaiah, G., Radhalakshmi, Y. C., Nachane, R. P. (year not stated). Comparative Analysis of Low-Stress Mechanical Properties of Woven and Knitted Apparel Fabrics. URL read: https://static.fibre2fashion.com/articleresources/PdfFiles/60/5963.pdf (read 2026-11-18). Woven cotton shirting, plain: B 0.0270, G 0.52, thickness 0.610, weight 12.52; units not printed in the table (unverified units; if weight is mg/cm2 that is 125.2 g/m2). Also cotton single jersey B 0.0066, G 0.47.
- Adamu, B. F. 2021. Denim Fabric Surface, Low-stress Tensile and Shear Properties Evaluation based on KES. JTATM 12(2). URL read: https://jtatm.textiles.ncsu.edu/index.php/JTATM/article/download/18650/8785/71325 (read 2026-11-18). Denim, 3/1 twill, 100% cotton warp. Absolute EMT, B, G values are only in figures, which were not readable; text gives 2HG values 30.778, 29.452, 24.696, 21.97 with an unclear direction. Not usable for numbers.
- KES test load: the standard KES-FB1 maximum tensile load of 500 gf/cm is from memory and was not confirmed in a source read in this run (unverified). EMT should be read as strain at that load once confirmed.

### 1.5 Penava and other textile-engineering papers
- Penava, Z., Simic Penava, D., Knezic, Z. 2014. Determination of the Elastic Constants of Plain Woven Fabrics by a Tensile Test in Various Directions. Fibres and Textiles in Eastern Europe 22(2), 57-63. URL read: https://yadda.icm.edu.pl/baztech/element/bwmeta1.element.baztech-8353b6e3-7672-4a6f-9f3d-a82c2908ffee/c/FTEE_104_57.pdf (read 2026-11-18).
  - Method: ISO 13934-1 strip test, 350 x 50 mm, 200 mm gauge, 100 mm/min, seven directions 0 to 90 degrees, conditioned 65% RH, 20 C, video grid tracking. Initial modulus from the elastic region.
  - Verified (all plain weave), initial modulus E in MPa, warp (90 deg) / weft (0 deg) / bias (45 deg):
    - Cotton 100%: 150.3 g/m2, 0.318 mm; 12.436 / 32.559 / 0.821
    - Wool 100%: 234.8 g/m2, 0.568 mm; 8.149 / 21.860 / 0.170
    - Wool 95 / lycra 5: 178.2 g/m2, 0.328 mm; 0.851 / 0.250 / 0.076
    - Polyester 100%: 164.6 g/m2, 0.252 mm; 11.674 / 5.152 / 0.478
  - One low-load point, verified: cotton weft 5.69 N at 1.10% elongation on the 50 mm strip.
  - Licence of the article was not checked.
- Bharathi, D., Alagirusamy, R., Joshi, M., Eswara Prasad, N., Das, B. R. 2020. Flexing behaviour of high strength coated fabrics. Indian Journal of Fibre and Textile Research 45, 381-387. URL read: https://core.ac.uk/download/386787264.pdf (read 2026-11-18). Nylon 6,6 plain, uncoated: 180 g/m2, 0.32 mm, breaking elongation 39.8 / 31.7 % warp / weft. Coated version: 297 g/m2, 0.36 mm, flexural rigidity 302 / 322 microN m. This is a high-strength technical cloth, much heavier and stiffer than a cheap jacket shell; use only as an upper bound. The extract warned the tables were garbled in places.
- Yea, S. J. and Kim, I. Y. 2012. Physical Properties of 1x1 Rib Knitted Fabrics Using A/W (acrylic/wool 70/30). Journal of the Korean Society for Clothing Industry 14(4), 629-634. URL read: https://koreascience.kr/article/JAKO201230554943398.pdf (read 2026-11-18). Thickness 1.592 to 2.362 mm across nine knitting settings. No fabric weight and no KES values.

### 1.6 Later datasets
- Ju, E., Kim, K., Yoon, S., Shim, E., Kang, G.-C., Chang, P. S., Choi, M. G. 2024. Estimating Cloth Simulation Parameters From Tag Information and Cusick Drape Test. Computer Graphics Forum 43(2). URL read: https://diglib7.eg.org/bitstream/handle/10.1111/cgf15027/v43i2_20_15027.pdf (read 2026-11-18). About 5,000 commercial fabrics with expert-tuned simulator parameters. The data come from a commercial service and are not released; no reuse terms. Not usable. The paper confirms the usual practice is to convert KES or FAST measurements into a given simulator's parameters, with no general formula published.
- Search results also listed Feng et al. 2022 (learning-based bending stiffness from a drape tester) and Wang's parameter-estimation work; not read in this run.

## 2. Converting measurements into XPBD parameters

Primary source: Macklin, M., Mueller, M., Chentanez, N. 2016. XPBD: Position-Based Simulation of Compliant Constrained Dynamics. Motion in Games 2016. URL read: https://matthias-research.github.io/pages/publications/XPBD.pdf (read 2026-11-18). Verified points:
- Compliance alpha is "inverse stiffness". Inside the solver alpha-tilde = alpha / dt^2.
- Update per constraint j: delta-lambda = (-C_j - alpha-tilde_j x lambda_j) / (grad C_j M^-1 grad C_j^T + alpha-tilde_j); delta-x = M^-1 grad C^T delta-lambda.
- Damping: beta is a damping stiffness, beta-tilde = dt^2 x beta, gamma = alpha-tilde x beta-tilde / dt.
- For triangle finite elements the paper sets the compliance to the inverse of the element stiffness matrix written with Lame parameters (its Eq. 28). The paper gives no units and no direct cloth table.
- Example settings in the paper: cantilever dt = 0.008 s with 20 iterations visually matching a Newton reference; chain with alpha = 1e-8; cloth grid 64 x 64 with 20 to 160 iterations (cloth dt not stated).

Unit conversions (derived here, SI):
- KES bending B: 1 gf cm2/cm = 9.80665e-3 N x 1e-4 m2 / 1e-2 m = 9.807e-5 N m (bending rigidity per unit width). Example: wool warp 0.0593 gives 5.82e-6 N m.
- KES shear G: 1 gf/cm per degree = 0.9807 N/m per degree = 56.19 N/m per radian. Example: wool 0.61 gives 34.3 N/m per radian.
- Tensile modulus E (MPa) to membrane stiffness per unit width Y (N/m): Y = E x thickness. Example: Penava cotton weft 32.559 MPa x 0.318 mm = 10,354 N/m. Check against Penava's own low-load point: 5.69 N / 0.05 m / 0.011 = 10,345 N/m. They agree, which supports reading Penava's E as based on the measured thickness.
- Areal density: g/m2 / 1000 = kg/m2.

Mapping into a position-based solver (derived; the method is standard but the formulas below were not read in a source during this run, so check them against a continuum reference before use):
- Mass per particle: m_i = rho_A x (one third of the summed rest area of the triangles touching particle i). Houdini's official Vellum page confirms the same approach in words: mass from triangle area times material density, with a "varying" mode giving each point the surrounding area (https://www.sidefx.com/docs/houdini/vellum/mass_thickness.html, read 2026-11-18).
- Distance (edge) constraints on a regular square grid with spacing h: an edge of length h carrying a strip of width h has spring stiffness k = Y x h / h = Y, so alpha_edge = 1 / Y (m/N). This is independent of resolution, which is the point of XPBD. On irregular triangle meshes this is only approximate; per-triangle strain constraints with compliance from the inverse of (membrane stiffness matrix x rest area) are the professional route and are what the XPBD paper's Eq. 28 does.
- Warp, weft and bias: use direction-specific edge compliance along warp and weft (from E_warp and E_weft), and set shear (diagonal edges or the triangle shear term) from the bias modulus or from KES G. In Penava's data the bias modulus is roughly 10 to 130 times lower than warp or weft (cotton 15 / 40, wool 48 / 129, polyester 24 / 11), so shear compliance must be far larger than stretch compliance.
- Bending: a dihedral-angle constraint per interior edge, with an angular stiffness that scales as bending rigidity B times edge length squared divided by the two adjacent triangle areas (the discrete-shell form). Compliance is its inverse, units 1/(N m) per radian squared. The exact constant was not confirmed in this run.
- Stretch limit: a practical low-load limit can be read from EMT (strain at the KES maximum load) or from the strain at which the Penava curves leave the elastic region. Use it as a hard cap on edge strain (long-range attachment or a clamp), not as a compliance.

## 3. Public solver defaults (official pages only)

Houdini Vellum (SideFX, Houdini 21.0 docs):
- Cloth simulation page, https://www.sidefx.com/docs/houdini/vellum/clothsimulation.html (read 2026-11-18): "A good starting point for clothing is 5 substeps"; thickness is reset to the default 0.01 when a new Vellum Cloth is created (scene units; Houdini's unit is metres, so 1 cm, unit itself not stated on the page).
- Vellum Solver node page, https://www.sidefx.com/docs/houdini/nodes/dop/vellumsolver.html (read 2026-11-18): smoothing iterations default 10; collision passes "in practice we find 10 to be correct for most situations"; constraint iterations "a good starting point is the diameter of the geometry" (no number); no substep or gravity number on the parts read (the page says the default substeps "can be very aggressive" and suggests 2 or 5 if cloth is too stretchy; reviewer read 2026-11-18, first 100,000 characters only).
- Mass and thickness page (above): default cloth density 0.1, units not stated; thickness defaults to the average edge length times an edge length scale.

Marvelous Designer, official help, Simulation Properties, https://support.marvelousdesigner.com/hc/en-us/articles/47358125463321/ (read 2026-11-18):
- Gravity default -9800 (unit not printed; consistent with mm/s2).
- Time step: no number given, "The default values are recommended". Simulations per frame and CG iteration count: described, no numbers. Particle distance and skin offset: not on this page.

CLO, official help (page titles not visible in the fetch):
- https://support.clo3d.com/hc/en-us/articles/115012227227 (read 2026-11-18): "The default value of the Particle Distance is 20." (no unit on this page; the next page uses mm)
- https://support.clo3d.com/hc/en-us/articles/115000414447 (read 2026-11-18): 20 mm for fast dressing, under 5 mm for final quality; accepted range 0.8 to 700.
- https://support.clo3d.com/hc/en-us/articles/30201166554649 (read 2026-11-18): time step and gravity, defaults recommended, no numbers.

Blender cloth, official manual:
- Physical Properties, https://docs.blender.org/manual/en/4.2/physics/cloth/settings/physical_properties.html (read 2026-11-18): describes vertex mass, air viscosity, linear or angular bending model, tension, compression, shear and bending stiffness and damping; no default values or units printed.
- Collisions, https://docs.blender.org/manual/en/dev/physics/cloth/settings/collisions.html (read 2026-11-18): object and self-collision distance and quality are described; no defaults printed.

Unreal Engine Chaos Cloth, official API and docs:
- UChaosClothConfig (4.27), https://docs.unrealengine.com/4.27/API/Plugins/ChaosCloth/ChaosCloth/UChaosClothConfig/index.html (read 2026-11-18): gravity in cm/s2; EdgeStiffness "only use lower than 1 values for very stretchy materials" (a normalised 0 to 1 stiffness, not a physical one); density, collision thickness, damping, friction described with no defaults.
- UChaosClothSharedSimConfig (4.27), https://docs.unrealengine.com/4.27/API/Plugins/ChaosCloth/ChaosCloth/UChaosClothSharedSimConfig/index.html (read 2026-11-18): IterationCount and SubdivisionCount (substeps) described, no defaults.
- Clothing tool properties reference, https://dev.epicgames.com/documentation/unreal-engine/clothing-tool-in-unreal-engine---properties-reference?lang=en-US (read 2026-11-18): stiffness and stretch limit per constraint group, collision thickness, solver frequency; no numbers.

What this means for Kiln: the only public numeric defaults found are gravity (9.81 m/s2 in any unit system), a starting point of about 5 substeps per frame for clothing (Houdini), roughly 10 collision passes (Houdini), a particle spacing of 20 mm for dressing and under 5 mm for finals (CLO), and a cloth thickness of about 1 cm by default in Houdini, which SideFX itself warns may be too big. Kiln's other solver numbers should be chosen and recorded as Kiln's own decisions, not taken from any product.

## 4. Table

Units: density g/m2; thickness mm; stretch as membrane stiffness per width Y in N/m (warp / weft / bias) unless noted; bending as KES B in gf cm2/cm (warp / weft), multiply by 9.807e-5 for N m; stretch limit as % strain.

| Garment fabric | Density | Thickness | Stretch stiffness | Bending | Stretch limit at low load |
|---|---|---|---|---|---|
| Nylon shell, cheap 1980s jacket | 40 to 60 (380T nylon taffeta, retailer page textiledetails.com, unverified) | gap | gap (upper bound only: high-strength nylon 6,6 plain, 180 g/m2, Bharathi 2020, no modulus) | gap (coated heavy nylon 302 / 322 microN m, Bharathi 2020, upper bound only) | gap (breaking elongation 39.8 / 31.7 %, Bharathi 2020, not a low-load limit) |
| Cotton or poly-cotton twill, work trousers | 220 (65/35 cotton-poly "pants", Wang 2011, verified; weave not stated) | gap for twill; 0.318 for plain cotton proxy (Penava 2014) | proxy plain cotton: 3,955 / 10,354 / 261 (derived from Penava 2014) | gap for twill | proxy: about 1.1 % at about 114 N/m (Penava 2014 cotton weft point, derived) |
| Denim, jeans | 400 (Clyde 2017, verified); 324 for 11 oz with 1% spandex (Wang 2011, verified) | 0.66 (Clyde 2017, verified) | gap (Clyde fits not printed; Adamu 2021 values only in figures) | gap | gap |
| Wool or acrylic knit jumper body | gap for wool/acrylic; 224 for polyester sweater knit (Wang 2011, verified, proxy) | 1.59 to 2.36 for acrylic/wool 1x1 rib (Yea and Kim 2012, verified) | gap | gap (cotton single jersey B 0.0066, Ramaiah, units unverified, proxy) | gap |
| 1x1 or 2x2 rib, cuffs and waistband | 276 (cotton/spandex rib knit, Wang 2011, verified, proxy) | 1.59 to 2.36 (Yea and Kim 2012, acrylic/wool 70/30 1x1 rib, verified) | gap | gap | gap |
| Heavy wool melton or donkey-jacket cloth | 480.6 (wool coating twill, Clyde 2017, verified, nearest match) | 1.28 (Clyde 2017, verified) | proxy plain wool 234.8 g/m2: 4,629 / 12,416 / 97 (derived from Penava 2014); a melton will be stiffer | proxy plain wool 181 g/m2: 0.0593 / 0.0459 (Kim and Son 2006, verified); melton will be much stiffer | proxy wool: EMT 5.69 / 8.52 % at KES max load (Kim and Son 2006, verified; load value unverified) |
| Polyester pleated skirt fabric | 164.6 plain polyester (Penava 2014, verified); 155.1 filament polyester (Kim and Son 2006, verified) | 0.252 (Penava) or 0.659 (Kim and Son), verified | 2,942 / 1,298 / 120 (derived from Penava 2014) | 0.0398 / 0.0525 (Kim and Son 2006, verified); shear G 1.20 / 0.85 gf/cm deg | EMT 3.88 / 1.63 % (Kim and Son 2006, verified) |
| Cotton shirting | 103.6 cotton poplin (Clyde 2017, verified); 150.3 plain cotton (Penava 2014, verified) | 0.18 (Clyde) or 0.318 (Penava), verified | 3,955 / 10,354 / 261 for the 150 g/m2 cotton (derived from Penava 2014) | 0.0270 single value (Ramaiah, units unverified) | about 1.1 % at about 114 N/m weft (Penava 2014, derived) |

Extra row for scale, wool/polyester 50/50 plain-weight suiting (Kim and Son 2006, verified): 181.4 g/m2, 0.630 mm, B 0.0720 / 0.1027, G 0.66 / 0.64, EMT 9.71 / 3.46 %.

## 5. Could not reach or did not read

- Miguel et al. 2012 full paper (only the Eurographics metadata page was reached).
- Wang 2011 database page and its terms (named in the paper, not fetched, since it did not appear in search results).
- Clyde 2017 supplemental document with fitted values.
- Adamu 2021 figures with denim KES values.
- Lam and Postle, wool and wool-blend KES study (fibre2fashion page had the abstract only).
- A PMC table on fabric properties (blocked by a browser check).
- NCSU TPACC Kawabata page (in search results, not fetched).
- Numeric defaults for Houdini substeps and gravity, Marvelous Designer time step and particle distance, Blender cloth, and Unreal Chaos cloth: the official pages read do not print them.
- No public measured stiffness for a light nylon taffeta, a denim, a melton or a knitted rib was found in this run. These are the main gaps.

## 6. Recommended next steps for Kiln

1. Use the verified density and thickness figures now; they cover every fabric except knit density and nylon thickness.
2. Use Penava's three plain wovens (cotton, wool, polyester) for warp, weft and bias stretch, via Y = E x thickness and alpha = 1/Y, and Kim and Son for bending and shear. Record each as a proxy where the weave differs.
3. For denim, melton, nylon taffeta and rib, either read the Wang 2011 database terms (it has denim, rib knit and a 65/35 trouser cloth) or commission or perform a cheap cantilever bend test (ASTM D1388 style) and a hanging-weight stretch test on real swatches; both methods are fully described in Clyde 2017 and Wang 2011.
4. Confirm the KES-FB1 standard maximum load and the discrete-shell bending constant from a primary source before locking numbers.
