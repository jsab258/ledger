# What each kind of picture means

ADOPTED 2026-10-06 (ADOPTED-2026-10-06.md). None of the pictures below is in git: the branch's originals are archived unchanged in F:/LedgerTools/atlas-01-2026-09-22, the map redrawn on adoption in F:/LedgerTools/atlas-01-2026-10-06, with two reduced previews in production/previews/ (atlas-01-*-2026-10-06.jpg). Rows for the earlier Mickey's fit-out (its plans, elevations, targets, text proofs, Blender recipe and image prompts) were left out with those files.

Continuation provenance: `previews/evidence-revisions`, `town-work-and-home` and `hook-uses` are original SVG design studies, rasterised with the existing Sharp bundle. `previews/mesh-*` project actual studio GLB triangles with node transforms; they are neither lit Blender renders nor engine frames. No new AI image generation, Blender render or Unreal frame occurred in this continuation. The initial concepts below remain unchanged.

All new design work is a proposal dated 2026-09-08, based on the owner's pin 7722b45cb3dcee2fbcee26675fae4fef641cbba7. [data/source-lock.json](data/source-lock.json) records source-document hashes and the owner's overrides. No studio pin was invented.

| Files (archive) | Origin | Evidential limit |
|---|---|---|
| concepts/hook, copper, exchange, parade, fairview, ironside, gullwing.png | Built-in OpenAI image_gen service, generated for this commission and selectively edited after visual inspection | AI concepts made before the content rule's full application and canon D19; not to be reused as they stand. Model version and random seed were not exposed by the tool; these are not deterministic renders |
| previews/atlas-overview, gameplay-overlay, hook-detail and district-*-plan.svg/png | Original authored coordinates in data/atlas.json, Python SVG drawing, Sharp PNG rasterisation | Broad layout and relationships are intentional; no real town graph was traced. Contours are schematic, not a surveyed heightfield. Superseded by the 2026-10-06 drawings |
| 2026-10-06: atlas-overview, gameplay-overlay, hook-detail, district-*-plan.svg/png | scripts/draw.py over the adopted data/atlas.json and production/specs/vignette-scene.json; PNGs by headless Chrome (installed, no network, no GPU) | As above; the Hook detail follows the built street, its climb and its bend |
| previews/reference-hull and reference-kasbah.svg/png | Original annotations/diagrams and embedded dated reference evidence | Reference photographs/maps, not Meridian concept or game geometry. See references/RIGHTS.md |
| references/source-street-day.png and street-evidence-contact.png | Retained images from the pinned project's production/d1-probe directory | Earlier game evidence, not a new run. Contact sheet contains camA/camB day/night and walk 00 through 04 |

Concept art may still contain incidental lettering and approximated small objects; no incidental mark is approved as an exportable logo, vehicle design or production texture.

Maps were reviewed for coastline, north direction, seven district identities, named destinations, label separation and the source street connection. The image edits corrected an early-period costume/vehicle bias, oversized skyline churches, a reversed fish-shop order, an invented harbour view through a service lane and a wheeled bin. These are art corrections, not proof of photoreal game performance.

The inherited art/asset/Blender conventions were searched at the pin and were not found. This package therefore defines only commission-local assumptions in INTERFACE-NOTES.md. No review record, art acceptance or integration receipt has been manufactured.
