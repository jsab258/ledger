# Small worn and carried pieces: spectacles and chain, handbag, tights, pager

Research note, 30 September 2026. D = documented (source number); I = inference.

## In short

1. Spectacles: a static mesh on a socket on the body skeleton's `head` bone, 1-2 mm clear of the nose. Lenses: Thin Translucent, light brown tint, darker at the top. MetaHuman Creator has no eyewear slot (D [13]); this is ours to build.
2. Chain: a thin skinned strip modelled in Blender, round the back of the neck, weighted `head` (arm tips) to `neck_02`, `neck_01`, `spine_05`. Not a cable simulation: fixed at both ends it would fall through the neck (I, from [16]).
3. Handbag: structured brown leather, about 27 x 20 x 8 cm (D [7][9]), a static mesh on a `hand_r` socket with a held-grip hand pose; add swing only if it looks stiff.
4. Tights: a masked change to the legs' skin material (warm "American Tan", smoother, faint sheen, darker at the leg's edges); no mesh unless the gate finds it looks painted (I).
5. Pager: black matt plastic, about 80 x 50 x 25 mm, small numeric screen, spring clip (D [1][2][3]); a static mesh on a `pelvis` socket at the right front hip. The sheet says "on his belt", so Darren needs a belt.
6. Both concept portraits break their sheets: Sheila's glasses are clear and slim with no chain; Darren's pager is centre-front with no belt. Build to the sheets.

## What each piece looked like

- **Pager.** Science Museum BT pagers are black plastic with a clip: Message Master 1200, 75 x 85 x 30 mm, 110 g, rectangular screen, two silver buttons; Tone Master and a Motorola tone pager, 85 x 45 x 30 mm, 60 g (D [1][2][3]). The Motorola Bravo numeric (1986) became the world's best-selling pager (D [4]). He rings back from phone boxes, so numeric, not tone-only (I). Racal Vodapage was licensed 1987, Hutchison only 1992 (D, summary [18]).
- **Spectacles.** A Science Museum "female style" frame of 1980: photochromic, nickel-plated steel and plastic, 130 mm across (D [5]). British Reactolite Rapide lens, 1986-87: grey, 90% light passed indoors, 8% in sun (D [6]). Light plastic lenses made big frames wearable; tints were fashionable (D, our looks.md section 3). No dated museum example or catalogue of a large square women's frame was found. Likely: lens 54-58 mm wide by 46-52 mm high, front 135-140 mm, gold metal or brown plastic (I).
- **Chain.** By the 1980s a "granny" item (D [11]), often thin cord (D [10]); rubber loops slip over the arm tips (D [10]). Worn, it loops from behind both ears round the back of the neck onto the collar; about 60-70 cm, links 1-2 mm (I).
- **Handbag.** V&A: Dot Cotton's EastEnders handbag, about 1990: black leather, gold-coloured clasp, short strap; 27 cm wide, 18 cm tall, 34 cm with strap (D [7]); a 1980s Russell & Bromley leather bag (D [8]); a period Launer 28 x 20 x 7.6 cm (D, summary [9]). Sheila's: mid-brown, semi-matt, worn corners, not glossy (I).
- **Tights.** Pretty Polly's "American Tan" was the everyday British flesh shade (D, summary [12]); sheer is 15-20 denier (D, summary [19]).

## How to attach and fit each

- Creator's wardrobe slots are hair grooms and garments only (D [13]). Epic names static accessories on sockets only as something a custom C++ pipeline could do, and Creator runs no custom pipelines in 5.8 (D [14]). Community practice: `head` socket plus attach (D [20][21]); recorded face animation may need baking to Control Rig first (D [22]).
- The face copies the body's `head`, so that socket suffices; the nose and brows move on face bones, hence the gap (I). No source names a nose-bridge bone.
- A groom does not collide with a static mesh: lay the arms in the hair's parting above the ear and check in the game hair (I).
- The Cable Component is a particle rope with fixed ends; its world collision is experimental and costly (D [16]).
- Thin Translucent gives white highlights and a tinted background in one pass (D, summary [17]).

## Tights

A separate mesh gives true sheen but needs the body under it hidden and can clip under a swinging skirt; a material change cannot clip (I). Both are in use: a Fab pantyhose set on MetaHuman bodies with adjustable transparency (D [23]); a community body-material mask (D [24]). The sheer look: skin showing through, a tan cast, darker edges seen side-on, no pores or hair (D, summary [19]; I).

## Budgets (triangles, highest detail)

MetaHuman head 24,000 vertices, body 30,500 (D [15]). Game glasses usually under 2,000 (D, summary [25]). Suggested (I): spectacles 2,000-4,000; chain 300-800 (tube of 4-6 sides); handbag 3,000-6,000; pager 500-1,500; tights none.

## What a reviewer sees first

- Spectacles: floating off or sunk into the nose; lenses hiding the eyes; frames too small or modern.
- Chain: thick, rigid, or through the collar or neck.
- Handbag: fingers through the handle; through the leg or skirt; too glossy or new.
- Pager: too big, rounded and modern, floating, no belt.
- Tights: bare-looking legs, or grey plastic.

## Sources

"Opened" means read; "summary" means search summary only.

1. BT Message Master series 1200 pager, model 31D. Science Museum Group, undated. https://collection.sciencemuseumgroup.org.uk/objects/co8054903 (opened)
2. BT Tone Master pager, model 36C. Science Museum Group, undated. https://collection.sciencemuseumgroup.org.uk/objects/co8054904 (opened)
3. BT Tone pager Motorola 3BMXB/1. Science Museum Group, undated. https://collection.sciencemuseumgroup.org.uk/objects/co8054902 (opened)
4. How do radio pagers work? C. Woodford, Explain that Stuff, 19 Sep 2024. https://www.explainthatstuff.com/howpagerswork.html (opened)
5. Pair of photochromic spectacles, female style. Science Museum Group, undated. https://collection.sciencemuseumgroup.org.uk/objects/co4715 (opened)
6. Ophthalmic lens blank in Reactolite Rapide. Science Museum Group, undated. https://collection.sciencemuseumgroup.org.uk/objects/co3523 (opened)
7. Handbag used by June Brown as Dot Cotton, O1757997. V&A, undated. https://collections.vam.ac.uk/item/O1757997 (opened)
8. Woman's handbag, Russell & Bromley, O350819. V&A, undated. https://collections.vam.ac.uk/item/O350819 (opened)
9. Vintage Launer blue leather bag. 1stDibs, undated. https://www.1stdibs.com/fashion/handbags-purses-bags/shoulder-bags/vintage-launer-blue-leather-bag/id-v_18276722 (summary)
10. Return of the glasses chain. Peep Eyewear, "May 9", year not shown. https://www.peepeyewear.co.uk/vintage-blog/return-of-the-frame-chain (opened)
11. History of glasses chains. Retropeepers, 23 Jun 2023. https://retropeepers.com/blogs/retropeepers-edit/history-of-glasses-chains (opened)
12. American Tan Tights. Do You Remember?, undated. https://www.doyouremember.co.uk/memory/american-tan-tights (summary)
13. Hair and Clothing Tools. Epic, MetaHuman docs, undated. https://dev.epicgames.com/documentation/metahuman/hair-and-clothing-tools (opened)
14. MetaHuman Collections in Unreal Engine. Epic, undated (5.8). https://dev.epicgames.com/documentation/metahuman/metahuman-collections-in-unreal-engine (opened)
15. Platform Support and LOD Specifications for MetaHumans. Epic, undated. https://dev.epicgames.com/documentation/en-us/metahuman/platform-support-and-lod-specifications-for-metahumans (opened)
16. Cable Components in Unreal Engine. Epic, UE 5.8 docs, undated. https://dev.epicgames.com/documentation/en-us/unreal-engine/cable-components-in-unreal-engine (opened)
17. Shading Models in Unreal Engine. Epic, undated. https://dev.epicgames.com/documentation/en-us/unreal-engine/shading-models-in-unreal-engine (summary)
18. Radio-paging code No. 1 and related pages. Wikipedia, undated. https://en.wikipedia.org/wiki/Radio-paging_code_No._1 (summary)
19. Matte and Sheer pantyhose/stocking shader settings. Daz 3D forums, undated. https://www.daz3d.com/forums/discussion/145611 (summary)
20. Workflow to add glasses and props to metahumans. Epic forums, Apr 2021 to Feb 2023. https://forums.unrealengine.com/t/workflow-to-add-glasses-and-props-to-metahumans/226167 (opened)
21. Adding glasses / shades to MetaHuman. Epic forums, Apr to Jun 2021. https://forums.unrealengine.com/t/adding-glasses-shades-to-metahuman/225100 (opened)
22. How to attach sunglasses to metahuman live link animation. Epic forums, Jul to Aug 2021. https://forums.unrealengine.com/t/how-to-attach-sunglasses-to-metahuman-live-link-animation/242754 (opened)
23. JTC Pantyhose for Metahuman on UE 5.6. Epic forums, 19 Aug 2025. https://forums.unrealengine.com/t/jerrythecat-jtc-pantyhose-for-metahuman-on-ue-5-6/2647032 (opened)
24. Body Mask for Metahumans in UE 5.6. F. Vilanova, Epic community, 8 Jul 2025. https://dev.epicgames.com/community/learning/tutorials/5XbX (opened; video, title only)
25. How to Make a 3D Eyeglasses Model. Tripo3D blog, undated. https://www.tripo3d.ai/blog/explore/how-to-make-eyeglasses-3d-model (summary)

Not found: a dated museum example or catalogue of a large square women's frame of 1988-92; the Motorola Bravo's measurements; a museum pair of flesh tights of the period; any official Epic word on glasses or chains.
