Method researched: this note, building on HILL-METHODS-2026-10-04.md and TARGET-HILL-CROWNS-2026-11-17.md.

## Review corrections (fresh review PASS WITH FIXES, 17 Nov; REVIEW-HILL-CROWNS-2026-11-17.md). Read this first; it overrides the text below.

- Season: bake October leaf state (canon names no month; the story design and the target say October). The November leaf notes below are kept for reference only.
- No licence pick for him: Sapling Tree Gen runs as a tool on his PC and ships no code; the allowlist governs what ships. One DECISIONS line citing GPL-3.0-or-later and the GNU FAQ on output is enough; step 1 does not wait on him.
- The cost test must be able to fail: GPU time over three runs with and without the 100 copies; pass only if the mean added plus the spread is at most 0.2 ms.
- Add a whole-hill memory cap: six tree types at 4096 is about 256 MB on a card already about 330 MB over budget; plan 2048 bakes or fewer types unless measured otherwise.
- Remove the fail clause that contradicts step 4 (see the review).
- Try count: the parent, the 5 Nov closure and CLAUDE.md say a further try needs his yes; RULINGS 7 Nov says nobody asks him. The main session settles which applies before a third try; the lane does not.


# Hill crowns: research and one-tree test plan (17 Nov 2026)

## In plain words

1. The tree maker (a free Blender add-on) is current, works with the Blender already on the PC, and the trees it makes are ours to use in a sold game.
2. The leaf pictures from ambientCG are free for any use; sycamore and oak leaves exist there, ash and hawthorn were not found.
3. Unreal's own "impostor" tool (a flat card that shows a pre-made picture of the tree from the right angle) is the right fit; Unreal's newer foliage system is still marked experimental.
4. (Corrected after review.) The story design and the parent target set the hill in October, not November: mostly in leaf, so the soft edge must come from the impostor itself, not from bare branches.
5. One test tree first, about 7 to 9 hours; most cost numbers stay unproven until that test measures them on his card.

## Findings

1. Sapling Tree Gen 1.0.0 is an extension, released 4 Nov 2026, "all-new code", replacing "the add-on that was part of Blender until version 4.1"; Blender 5.2 LTS or newer; GPL-3.0-or-later; 29 presets, wind, armature, "Make Mesh" bakes a plain mesh; 0.3.7 failed on Blender 5.0 and 5.1 (extensions.blender.org/add-ons/sapling-tree-gen, read 17 Nov 2026). The PC has Blender 5.2.2 LTS on F: (blender-mcp/SUMMARY-2026-09-28.md line 15). The target's "4.4+" and 0.3.7 are out of date.
2. Its output is ours. GNU: "The output of a program is not, in general, covered by the copyright on the code of the program", except art or text copied from the program (gnu.org/licenses/gpl-faq, read 17 Nov 2026, first 100,000 of 140,592 characters). Blender: "What you create with Blender is your sole property" (blender.org/?p=658, read 17 Nov 2026). The add-on's code never ships.
3. ambientCG: "All ambientCG assets are provided under the Creative Commons CC0 1.0 Universal License", no credit needed, no AI clause (docs.ambientcg.com/license, read 17 Nov 2026). Asset pages could not be opened today, so LeafSet027 (maple, sycamore's genus), 016 and 012 (oak) rest on the 4 Oct note. No CC0 ash or hawthorn atlas found (U); at 5 to 10 cm a pixel leaf shape is invisible, so a tinted generic atlas may serve (I).
4. Impostor Baker: listed under BUILT-IN > Mesh, off by default, maturity not stated (page read is the 5.9 one). 8 triangles a card against a billboard's 72; three nearest frames blended; Epic's distance foliage uses 12 x 12 frames at 2048; capture at twice the subframe size; base colour and normal suffice; no translucent sources; Upper Hemisphere "not meant to be viewed from underneath"; the blend costs more pixel shading than a billboard (dev.epicgames.com impostor-baker-plugin-in-unreal-engine, read 17 Nov 2026).
5. Nanite Foliage (assemblies, voxels, skinning) is still "Experimental ... use caution when shipping", voxel settings "likely to change or be removed" (dev.epicgames.com nanite-foliage, 5.9 page, read 17 Nov 2026); 5.8.1 and 5.8.2 fixed a voxel GPU crash and voxels not rendering (5.8 released forum thread, read 17 Nov 2026). UE 5.8 (17 Jun 2026) adds an Experimental Procedural Vegetation Editor (unrealengine.com 5.8 news, read 17 Nov 2026). Route B stays out; the editor is an untested later route.
6. Pro numbers: Fortnite's non-Nanite trees about 10,000 to 20,000 vertices, Nanite trees 300,000 to 500,000; opaque leaves usually faster than masked; "Preserve Area" stops distant canopies thinning (unrealengine.com tech-blog bringing-nanite-to-fortnite-battle-royale-in-chapter-4, read 17 Nov 2026). SpeedTree: 3 to 5 models scaled and rotated "go a long way"; overdraw is the risk (SpeedTree SDK gpu-performance, read 17 Nov 2026). No published cost per hundred impostors on a mid card found.
7. Mafia's Unreal interview failed again (unreached); no Warhorse or Mafia Definitive Edition write-up on distant trees found. Reference: none found; no number to copy.
8. Season. Nature's Calendar 2018: ash bare 4 Nov, the earliest; oak full tint 4 Nov, bare 29 Nov, the last (naturescalendar 2019 autumn analysis PDF, read 17 Nov 2026). Sycamore bare: "late October to early December" (Nature's Calendar sycamore bare-tree page, read 17 Nov 2026). Mid-November, therefore: ash bare grey twig domes; sycamore thin, yellow-brown; oak dense brown-yellow; hawthorn mostly bare (I); coastal wind thins crowns earlier (I).
9. Conflict: the story has Tom arriving in October (asset-plan/5-VEGETATION-AND-DISTANCE.md line 64); this brief says November. Check canon before baking leaf state.
10. The street camera sees the tier trees from slightly below, which Upper Hemisphere impostors do not cover (finding 4): plan on Full Sphere unless the test's angles say otherwise (I).

## Corrected numbers

| Target's number | Status now |
|---|---|
| Sapling GPL-3.0, Blender 4.4+ | Corrected: 1.0.0, Blender 5.2 LTS+, GPL-3.0-or-later (R) |
| Impostor 8 tris vs billboard 72, three frames | Checked (R) |
| Impostor Baker experimental | Corrected: built-in plugin, off by default, status not stated (R) |
| Pixel 4.8 cm at 110 m, 9 cm at 206 m | Recomputed from its own 64 degrees across 2,560 px: 5.4 cm and 10.1 cm (I, arithmetic) |
| 10 m tree 165 to 220 px at 125 m | 164 px for 10 m, 262 px for a 16 m ridge tree (I, arithmetic) |
| 2048 frame (170 px) suffices past about 150 m | Revised: 2048 at 12 x 12 suffices past about 120 m for 10 m trees, about 195 m for 16 m; 4096 at 12 x 12 gives 341 px and covers all tiers (I) |
| Impostor memory | New: about 11 MB a tree type at 2048, about 43 MB at 4096 (base colour with mask plus normal, compressed, with mips) (I); six types at 4096 about 256 MB, against a card already 330 MB over at High peak |
| Near-tier tree 3,000 to 8,000 triangles | Unverified; Fortnite's pro range is 10,000 to 20,000 vertices for a full tree (R) |
| Under 0.2 ms for a few hundred impostors | Unverified; to be measured |
| Leaf cards 0.5 ms for 40 trees | Unverified; to be measured |
| Whole hill 0.5 to 1.2 ms; 8 to 16 h | Unverified |
| About 30 trees on the hill | Design choice, not a fact |

## One-tree test plan (main session)

1. Space check (retention.py), then install Sapling 1.0.0 into F:\LedgerTools Blender 5.2.2 after the licence pick below. 0.5 h.
2. Grow one 12 m sycamore from the nearest broadleaf preset, crown pruned to an envelope, leaf state as canon's month (part-bare if November), LeafSet027 tinted, Make Mesh, no translucency; record triangles. 2 h.
3. Import through the asset-import skill at real size. 0.5 h.
4. Bake three impostors: Full Sphere 12 x 12 at 2048, the same at 4096, Upper Hemisphere at 2048; base colour and normal. 1.5 h.
5. Place copies on the two near tiers and a far-wood row; hook camera, reverse view, night; then 100 copies for cost. 1.5 h.
6. Measure: frame time with and without the 100 (hook frame, scalability 2, five-second average); added texture memory; elevation angle and screen height at each tier; shimmer and ghosting in a 10-second pan. 1 h.
7. Fresh reviewer against the last good picture, the Hook sheet and the KCD2 frames. 1 h.

Pass: a broken, soft-edged mass, not lumps; no sky holes with fog off; no ghosting, frame snap or wrong underside in the pan; 100 impostors at most 0.2 ms and 50 MB added; the reviewer passes it. Fail: a lump, lollipop, stylised look, visible card or blend, or cost over those lines; the other step-4 variant is tried before the method is questioned.

About 8 hours (7 to 9). A second species and three ages only after a pass.

## Licence pick for Jafar (one)

Sapling Tree Gen is a new tool not on the allowlist; earlier tools (ast-grep, PresentMon) went on by his pick. Question: may the builder use the free Blender tree maker Sapling (GPL; it never ships, and the trees it makes are ours)? A: yes, as a tool on his PC only (recommended). B: no, try Unreal's own experimental vegetation editor instead.

## Unverified points

ambientCG leaf sets (pages unreached) and any ash or hawthorn atlas; Impostor Baker in 5.8 (page read is 5.9); every cost figure here; impostor lighting under Lumen at 110 to 250 m; Mafia's and KCD2's methods; 1990's own autumn dates; the game's month; Sapling's presets page (blocked).
