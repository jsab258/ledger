# Mickey's front room: the other direction

4 October 2026; extends DRESSING, CLOSE-RANGE, NOTE and asset plan Family B. O = opened, S = search summary only, I = inference.

## In brief

- Dress the walk-in blockout (mickeys-office.json) from a small kit as the one real room; the window shows that room.
- KCD2 splits the work: a prop artist models hero props (Eliseo, O); a level artist furnishes and lights the rooms (Bejček, O).
- Compose in grey first; letter the glass itself; wear from baked masks and decals.
- About 8 to 9 builder-days (I). Nothing to buy.

## Method, ranked by fit and cost

1. **Compose for the window first (cheapest, biggest gain).**
   - Blockout, assets, then dressing; most assets "subordinate to the focal point" (McGowan, 80.lv, 2017, O); story as a chain of placed props (Smith and Worch, GDC 2010, S).
   - Today (I; 1.6 m eye, 7 m out): the sightline over the 1.05 m counter passes 1.02 m above the radio desk; the radio's top is 0.95 m, so neither desk nor chair shows.
   - Fixes within canon (DECISIONS): the set on a shelf at 1.2 to 1.4 m; a counter flap in line with the window; Mickey's high-backed chair turned to the glass under an anglepoise. Brixton, 1980: the booking man sits at the window (cab-office note 2, O).

2. **Lettering in the glass material.**
   - "Decals render into the g-buffer, which doesn't contain transparent pixels" (Epic forum, 2022, O); the standard answer is a mask in the glass's UVs (Epic forum, 2014, O).
   - In Thin Translucent, Opacity is a lit layer's coverage: at 1 it hides the room, reflection on top (UE 5.8 engine source, O). Gilt: metallic 1, gold, roughness 0.15 to 0.3, opacity 1, black shade (I).
   - The mask lives in one pane's UVs, so it cannot slide behind a bar; keep 40 mm clear (I). Fallback: a masked card 1 mm behind the inner face (forum, O).

3. **A small kit: shell, one trim sheet, tiling surfaces.**
   - Separate shell meshes, 10 cm or thicker (CLOSE-RANGE). One trim sheet: skirting, architrave, the reveal's timber lining (replacing the black scan), counter edging, dado; Olsen's strips with 45° bevel normals, mapped by script (GDC 2015, transcript O).
   - 1024 px/m for the room (Renault, 80.lv, 2020, O); 2048 within 2 m (I). ambientCG surfaces. Placed as a Level Instance (UE 5.8, O).

4. **Hero props: mid-poly, by hand in Blender.**
   - Bevel with Harden Normals plus Weighted Normal; no high-to-low bake (Blender manual, O; Resenberger-Loosmann, 80.lv, 2022, O).
   - Bake AO and Pointiness ("for dirt maps and wear-off effects") to textures or colour attributes (Blender manual, O); one master material blends ambientCG grunge through them (I).
   - Poly Haven's props run 3.7k to 14.8k triangles, clock to kettle (API, O).
   - Model: base station and desk mic, phone with coiled cord, Mickey's swivel chair, counter with flap, bench, filing cabinet, blind, convector heater, ashtray, mugs.
   - Sketchfab CC0 is museum scans only, one tagged NoAI (API, O); Poly Haven's SchoolChair_01 (navy plastic) fits, brand unchecked; its radio is WW2 military.

5. **Wear.**
   - Nanite meshes take no per-instance vertex paint; Texture Color Painting is "the only option" (UE 5.8, O). Elsewhere, vertex paint through a height-lerp grunge mask (Cheung, 80.lv, 2019, O).
   - Mesh decals, non-Nanite (Nanite lacks them, O): chipped edges (Demetriades, 2020, O), tea rings, leaks, the carpet path, ceiling nicotine. ambientCG smears on the glass (DRESSING).
   - Trace the daytime smear first: dirt mask off, then player off (I).

6. **Not recommended:** more script primitives; Substance (money; Adobe's AI clause, I); paid kits.

## Order of work (I, one builder)

Outsourcing guides quote 2 to 3 days per simple prop for a human artist (S).

1. Grey composition test, both views, day and night: 0.5.
2. Shell, trim sheet, finishes, reveal: 1.5.
3. Lettering mask: 0.5.
4. Ten to twelve hero props: 3 to 4.
5. Wear and decals: 1.
6. Lighting, frame time, packaged build, gate, fresh reviewer: 1 to 1.5.

About 8 to 9 days; the kit then serves the domestic rooms (B3).

## From Jafar (scope only)

The asset plan puts Mickey's second. **(A, recommended)** Mickey's front office first, 8 to 9 days: his window is the street's story. **(B)** the domestic proof first (5 to 7 days), then Mickey's. No money, no canon.

## Unreached

Olsen's slides (transcript read instead); handover.co.uk (403); GDC videos; Crumpler's texel-density PDF; how Warhorse lights window rooms; any measured frame cost.

## Sources (accessed 4 October 2026)

- https://www.artstation.com/artwork/8BPn5G
- https://www.artstation.com/artwork/rlDova
- https://www.artstation.com/artwork/Jl2gRD
- https://80.lv/articles/the-stages-of-environment-art-in-gamedev
- https://80.lv/articles/building-a-victorian-manor-modular-elements-texel-density-lighting
- https://80.lv/articles/creating-assets-within-the-mid-poly-workflow-in-ue5
- https://80.lv/articles/001agt-004adk-005cg-modular-scene-in-ue4-blockout-vertex-paint-decals
- https://gdcvault.com/play/1012647
- https://archive.org/stream/GDC2015Olsen2/GDC2015-Olsen-2_djvu.txt
- https://forums.unrealengine.com/t/decals-will-not-appear-on-translucent-glass/657012
- https://forums.unrealengine.com/t/glass-with-decals-help/4025
- Epic UE 5.8 docs and engine source; Blender 5.2 manual; Poly Haven and Sketchfab APIs.
