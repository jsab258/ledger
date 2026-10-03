<!-- Research note, 3 October 2026. Separate helper, about 30 minutes, given the problem only. D = documented in a numbered source; I = my inference. -->

# Matching a fixed in-engine street view to a concept (research note, 3 October 2026)

## The method, start to finish

Every breakdown found follows the same order: camera first, grey masses against an overlay second, detail last.

1. **Fit the camera to the concept.** Artists solve the field of view with fSpy, then set an Unreal camera to that field of view and the concept's aspect ratio (D1, D2, D3). fSpy assumes a distortion-free pinhole camera and right-angled vanishing directions. It is poor on images whose perspective "has been tampered with" (D9). Two-point images are fiddly: only the principal point moves the focal length, so users iterate against test shapes (D11). Focal length carries over only if the sensor (Unreal's Filmback) matches; fSpy's Blender import is said to assume 36 mm (search summary only; see the last section). Unreal has no native lens shift (D12).
2. **Block out the masses in grey against an overlay of the concept.** Artists put the concept in a post-process material on the camera and place boxes until the masses sit on it (D2, D5). Others overlay a transparent copy outside the engine (D1), or overlay only the concept's outlines (D4). Keep real-world scale. Do not shrink objects and pull them toward the camera to fit the picture (D13). Save the main viewpoints and build the scene around them (D20). A Naughty Dog artist: "the blockout should look great at all stages, even with colors and boxes" (D15).
3. **Treat the concept as intent, not geometry.** Hand-drawn or generated concepts carry distortion you cannot match without warping meshes (search summary of a Polycount thread, unreached). Translate the concept's idea rather than copying it (D13). AI images in particular lack "object permanence": sizes and space drift between images (D18). When the 3D and the concept disagree, the studio answer is a **paintover**: the concept artist paints on a screenshot of the blockout to fix "proportion, silhouette, palette, and framing", and that becomes the new target (D17; also D16).
4. **Check composition at every pass.** Use the concept as the reference for value, hue and saturation (D3). Step back from the frame to see "what stands out" (D14). Bellard's GDC 2019 talk applies cinematography (depth, framing, value) to environments (D23; listing only, not watched). One counterpoint: a single screenshot is not a level (D24). That matters less here, because this is one fixed view.

## Making the far end open

- **Cullen's townscape theory** names the problem. A view ended by a building square to the street is "complete", a closed vista. A curving street "engages the eye", and an angled end building implies space beyond (D22). So a bend helps only if its outer side does not become the new end wall.
- **Geometry (I).** The hillside reads above the far roofs only where, from the camera, the hill's ridge stands higher than the roofline of the end buildings. A rising road and a falling terrace line both help. So does a gap or lower building on the outer side of the bend. Detail cannot fix a mass that blocks the sky.
- **Distant hillside towns** are built cheaply in layers. Reuse the near kit at low detail. Use painted cards or impostors for the farthest trees, houses and hills (D19, D20). Separate the layers by value with height fog and fog cards (D19, D21). Tony Arechiga (ex-Destiny 2): use fog and alpha cards to "break up a ridgeline and blend terrain seams", and "when in doubt – fog it out" (D19). HLOD is for open worlds, not one fixed shot (D25, search summary only).
- **Near-to-far seams.** Fog cards control "which shapes get more definition" and what blends into the background (D21). The near layer must be finished wherever the camera can see past it (I, following D15).

## Overlaying the concept in Unreal

- **Built in (UE 5.8 documentation, undated):** the Cinematic Viewport's composition overlays offer only grids, a crosshair, rabatment, safe frames and a letterbox. They cannot show an image (D6, D7). In 5.6 they appear only after the Cinematic Viewport is switched on (D7, 24 September 2025).
- **Post-process material (the usual way):**
  - set the material domain to Post Process and blend to Translucent;
  - read SceneTexture:PostProcessInput0 and Lerp it with the concept texture;
  - expose the opacity in a material instance;
  - add the instance to the camera's Post Process Materials;
  - make the image the camera's aspect ratio (D5, 3 August 2023; used in D2).
- **Outline variant:** a free material by Arthur Tasquin overlays hand-drawn guide lines from the reference (D4, 16 October 2024).
- **Image Plate plugin:** attaches an image to a Cine Camera's frustum and fills it (D8, 4.27 documentation, search summary only; the current page did not load).

## What this means for the problem

1. **Put the flipped concept on the game camera itself** as a post-process overlay, in two copies: half-opacity and outlines only. Judge every mass live, not after a render (D2, D4, D5). Check the overlay through the game's own exposure, since the concept is the value reference (D3).
2. **Keep the fitted camera and stop fitting points.** It already holds the vanishing point and horizon. Leave the remaining mismatch to the concept's inconsistency (D9, D18), and keep true scale (D13).
3. **Before any detail, block the whole view in grey, the hillside included.** Give every terrace its full roof, back and chimneys, so lowering a near building reveals finished mass, not holes (D15, D20).
4. **Set the bend and rise from the flipped concept, within canon.** The bend must turn the flipped concept's way. The outer side of the bend must stay below the hill's ridge from the camera (D22; geometry, I).
5. **Build the hillside town as layers:** reused terrace kit at low detail, cards for the farthest houses and trees, and height fog plus fog cards between layers so the seam never shows (D19, D20, D21).
6. **Where the engine and the concept disagree, paint over the engine frame** to settle what to keep, rather than iterating by number (D17, D16).

## Sources

1. Emile Van Den Berghe, "Breakdown: Realistic Environment in UE4", 80.lv, 2 May 2019. Opened.
2. Finn Bogaert, "A Stylized UE 5 Environment…", 80.lv, 2 April 2024. Opened.
3. Augustas Krivelis, "The Yard: 3D Environment Breakdown", 80.lv, 24 September 2020. Opened.
4. "Free UE5 Outline Reference Match Material" (Arthur Tasquin), 80.lv, 16 October 2024. Opened.
5. Alex Pearce, "Reference Images/Camera Overlays in Unreal Engine", LinkedIn, 3 August 2023. Opened.
6. Epic, "Cinematic Viewport Controls in Unreal Engine" (UE 5.8), undated. Opened.
7. Epic forums, "Cinematic Composition Overlay in 5.6", 24 September 2025. Opened.
8. Epic, "Image Plate" (UE 4.27). Search summary only; the current page loaded empty.
9. fSpy, "Basics", fspy.io, undated. Opened.
10. CG Channel, "Download neat new free camera matching tool fSpy", 21 November 2018. Opened.
11. fSpy GitHub issue 119, 21 August 2022. Opened.
12. Epic forums, "Shift lens option in UE5 camera", 29 October 2021 to 15 December 2023. Opened.
13. Jonni Zhang, The Rookies, 18 August 2021. Opened.
14. Danielle Villacorte, The Rookies, 11 March 2022. Opened.
15. Artem Brizitskiy (Naughty Dog), "Approach to Environment Design in AAA Games", 80.lv, 23 April 2019. Opened.
16. Daniel McGowan (Amazon Game Studios), "The Stages of Environment Art in Gamedev", 80.lv, 14 December 2017. Opened.
17. Dmytro Lunov, "Video game concept art", Game-Ace (an outsourcing firm's blog), 28 January 2020, updated 9 September 2026. Opened.
18. Rob Sandberg, "North was perfect. South was a different room.", Game Production Alchemist, 1 July 2026. Opened.
19. Tony Arechiga, "Creating Breathtaking Game Backgrounds", 80.lv, 25 October 2018. Opened.
20. Lara D'Adda, "Making a Ghibli-Inspired Mountain Village in UE5", 80.lv, 14 July 2023. Opened.
21. Liesbet Segaert, "Mastering fog: four levels of fog in Unreal", Magnopus, 15 January 2025. Opened.
22. Recivilization Urban Design Primer, on Gordon Cullen's serial vision and closure, undated. Opened.
23. Miriam Bellard (Rockstar North), GDC 2019 talk: listing and Game Developer article of 18 November 2019 opened; the video was not watched.
24. The Level Design Book, "Composition", undated. Opened.
25. Epic, "World Partition – Hierarchical Level of Detail". Search summary only.

## What could not be verified

- **Unreached (HTTP 403), so not evidence:** Polycount threads 163378, 178229 and 103265. Nothing is concluded from them; the distortion point in step 3 rests on D13 and D18.
- **Not seen in full:** the Image Plate page (D8) and the HLOD page (D25).
- **Not watched:** Bellard's talk (D23). Its content is known only from the listing.
- **Not found:** a studio talk that matches one fixed street shot to a concept. Sources are portfolio breakdowns plus AAA interviews.
- **Search summaries can be wrong:** one said Kristina Nakić's medieval-market article (80.lv, 17 June 2025) used fSpy and an overlay; the page itself mentions neither.
- **Sensor point unconfirmed:** that fSpy's Blender import assumes a 36 mm sensor comes from a search summary of fSpy-Blender issue 26 (not opened).
- The hillside geometry rule is my own inference, not sourced.
