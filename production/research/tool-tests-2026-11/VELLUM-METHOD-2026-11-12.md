Method note for the Vellum third try (12 Nov 2026)

All pages read 2026-11-12 (SideFX docs read through a page-reading tool, not raw HTML; vellumdrape and vellumconstraints pages were read only to character 100,000 of about 250,000: later parts unread).

## 1. SideFX garment workflow
- Two routes ([paneling_draping](https://www.sidefx.com/docs/houdini/vellum/paneling_draping.html)). Paneling: Configure Cloth, then Vellum Stitch Points per seam pair with Rest Length Scale 0, then Vellum Weld Points, then the solver. The page says stitch-before-weld is optional but helps: "welding pulls fabric together instantly and can push it through the character; a stitch pass lets the cloth settle first". Draping: Configure Cloth, then Vellum Drape.
- Vellum Drape ([vellumdrape](https://www.sidefx.com/docs/houdini/nodes/sop/vellumdrape.html)): a pre-roll. Stage 1, soft springs pull each seam's two point halves together with gravity off (Attraction Stiffness, Welding Frame Delay frames). Stage 2, points weld and gravity turns on. Freeze at Frame outputs a settled frame; chain several Drapes with it. Seams need ordered point groups (Cycle, Reverse fix mismatches); add seams one at a time. Add Bend across Welds stops cusps at seams. Inflate Collisions (Initial Deflation, Final Inflation over Inflation Frames) resolves a cloth that starts inside the collider.
- SideFX tip: if the cloth cannot wrap the body, make panels larger.
- Not stated: numbers for Weld Frame Delay, Attraction Stiffness, Interior Edge Length. The Constraints page gives no method for closing stitches over time beyond Drape's own delay (Plasticity, Breaking and Constraint Property named, not explained).

## 2. Fabric values
- Constraints page ([vellumconstraints](https://www.sidefx.com/docs/houdini/nodes/sop/vellumconstraints.html)): no defaults or fabric numbers; change stiffness "by factors of 10". Higher-resolution cloth needs higher bend stiffness and compression stiffness for the same look. Triangle Stretch converges faster at high resolution; Distance Along Edges supports warp/weft anisotropy. Damping ratio below 1.
- Density: cloth 0.1 by default; Calculate Varying mass and uniform thickness (average edge length times Edge Length Scale) are defaults ([mass_thickness](https://www.sidefx.com/docs/houdini/vellum/mass_thickness.html)).
- Cloth page ([clothsimulation](https://www.sidefx.com/docs/houdini/vellum/clothsimulation.html)): bend 0 gives many wrinkles; higher is stiffer.
- Knit or rib values: none found in SideFX pages. A community summary (search result only, unread in full, older H17 guide, unverified) gives silk bend 0.0001, denim 1, compression about 100,000. 
- Marvelous Designer to Vellum conversion: none found (search 2026-11-12). Per-fabric tuning is the only route found.
- Resolution caveat (Tomas Slancik, [SideFX forum](https://www.sidefx.com/forum/topic/87356)): Vellum is not scale- or resolution-invariant for stiffer cloth; keep resolution consistent per material.

## 3. Collision, thickness, settling
- Substeps 5 for clothing; "1 substep per 100 iterations generally makes cloth very stretchy" (clothsimulation). Drape page: if too stretchy, raise substeps first.
- Constraint iterations: rough minimum is the longest shortest path in edges (Drape page: about the geometry's diameter in edges; [vellumtips](https://sidefx.com/docs/houdini/vellum/vellumtips.html)).
- Collision Passes about 10; more substeps beat more passes. Post Collision Passes: layers plus 2 (Drape page).
- Thickness (pscale): large but below edge length; an input pscale overrides default; default 0.01 may be too big ([clothsimulation](https://www.sidefx.com/docs/houdini/vellum/clothsimulation.html)). Raising the static friction coefficient helps garments stay on the body.
- Collider that self-intersects: pin attribute, Peak SOP to thicken ([tutorial](https://sidefx.com/tutorials/vellum-cloth-tips-tricks), 2019, H18).
- Thin cloth driving a thick mesh: suggested by Slancik (forum above).
- No published settle-still iteration count found.

## 4. Layering
- Integer `layer` point attribute; only differences matter; lower layers act heavier in collision so upper layers yield; Layer Shock tunes one-way to two-way (Drape page, vellumtips). Raise Post Collision Passes per layer (vellumtips). Tutorial above also layers separately simulated garments. No jacket-over-knit example found.

## 5. Apprentice limits ([product page](https://www.sidefx.com/products/houdini-apprentice/))
- Non-commercial; renders limited to 1920x1080; non-.picnc renders watermarked; no third-party renderers; Houdini Engine assets barred. The page does not name Alembic or FBX; the project's own step 0 found both ROPs blocked (PLAN-2026-11-11.md). OBJ and bgeo work.

## Unreached
- vellum/cloth.html and vellum/fabrics.html (404). Rest of the two long node pages. The ikrima.dev and sidefx forum seam posts were found in search only, not read.
