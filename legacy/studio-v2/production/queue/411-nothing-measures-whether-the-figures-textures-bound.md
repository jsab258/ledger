line: engine (the figure IS the visual slice)
spec: FILED BY THE RESIDENT ON THE RULING OF 2026-09-21 (`game-design/decision-2026-09-21-ruling-the-shortfall-is-zero-the-recount-is-not-a-repair-and-the-card-leaves-the-hero-frame.md`, item 19), which
  put it at the TOP OF THE ENGINE LINE behind that batch, because the figure is
  the visual slice and this is the question standing under it.

  THE QUESTION NOBODY CAN ANSWER TODAY: why does the figure render with flat
  yellow legs. It is not `paint_yellow`, which is road paint and renders as the
  kerb line. It is the figure's own material, and NOTHING MEASURES IT.

  WHAT IS PRINTED, read out of `production/d1-probe/ue-build.txt` by the
  resident: `figureImportStatus=IMPORTED`, `figureMaterials=1`,
  `figureImportVia=AssetImportTask/made=7`, plus bones, skin verts, bounds,
  anim and placement. WHAT IS NOT PRINTED: any `figureTexture*` key at all.
  Confirmed by listing every `figure` key on the page, 44 of them, and no
  texture among them.

  SO A MATERIAL EXISTS AND WHETHER ANY TEXTURE BOUND TO IT IS UNKNOWN. That is
  queue 123's fault ("the sampler reads the engine default") one level up,
  applied to the figure instead of to a street surface.

  A WARNING WRITTEN FROM THE DAY'S OWN MISTAKE. A builder reported that
  `Michelle.fbx` carries "four embedded textures in a .fbm folder" and the
  resident repeated it in two documents without checking. BOTH HALVES ARE
  FALSE: `find` returns NO .fbm directory anywhere in the tree,
  `ledger/Assets/Characters/` holds exactly one file (Michelle.fbx,
  20,974,352 bytes), and the number four is printed nowhere. SO THE EMBEDDED
  COUNT MUST BE MEASURED OFF THE FBX AND NEVER TYPED, which is why the
  acceptance below says so in those words.
acceptance: `figureTexturesEmbedded=N` MEASURED off the FBX rather than typed,
  printed beside `figureTexturesBound=n/N` so a zero can be told from a
  never-asked; BOTH ARMS WATCHED, meaning a run where a texture binds and a run
  where one does not both print distinguishably; and the frame OPENED
  afterwards, because the question that started this is what colour the legs
  are and no key answers that on its own
max_sessions: 2
status: READY 2026-09-21. The MEASUREMENT is instrument work under D45, a test
  and no review. The BINDING itself, when its turn comes, is VISUAL work under
  D41: no director, no written predictions, the Hook sheet is the reference.

  RULED BY: the ruling above, which named this the resident's to file and put
  it first in the engine line behind the surface batch.
