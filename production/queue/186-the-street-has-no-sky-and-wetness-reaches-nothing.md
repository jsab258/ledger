line: art (the visual bar) and engine, jointly
spec: The Unreal probe binds a sky and a reflection source, and Wetness reaches the
  material. All three, because none of them works alone.
acceptance: a frame from cam_hook in which the road reflects something, judged by Jafar
  beside Codex's Hook sheet
max_sessions: 2
status: READY 2026-09-09, and it is RUNG 1's real obstacle. Found while measuring queue
  176, not by looking for it.
  CORRECTED 2026-09-09 09:55Z BEFORE ANY BUILD: "none-black" was a hardcoded printf
  and never a reading. The far field is the height fog's inscattering colour lifted to
  near white by auto-exposure, proven by channel order (day 249.5/250.0/250.5 with
  R<G<B against day fog 0.55/0.58/0.62; night 188.4/179.6/179.3 with R>G=B against
  night fog 0.06/0.05/0.05). THE STRUCTURAL CLAIM STANDS, there is no sky actor, but
  A SKY BEHIND AN OPAQUE FOG IS INVISIBLE, so the fog's max opacity must come down in
  the same change or the dispatch returns today's frame.
  ORIGINALLY MEASURED: skyModel=none-black/phase-C-owns-the-hdri and
  ambientModel=trilight-3-directional/not-a-captured-sky. The condition NAMES an HDRI,
  belfast_open_field_2k, that the Unreal probe never binds. There is no skylight, no
  reflection capture and no captured cubemap: three directional lights and fog.

  TWO OF THE THREE PARTS ARE ALREADY BUILT, MEASURED 2026-09-14 ON RUN ce99814,
  AND THIS ITEM'S OWN TITLE IS NOW HALF WRONG. THE STREET HAS A SKY.
  skyAtmosphere=yes, skyAtmosphereComponent=yes,
  skyModel=skyatmosphere+skylight-realtime-capture/not-an-hdri, with
  ASkyAtmosphere spawned at VignetteShot.cpp:1294. THE REFLECTION SOURCE IS
  BOUND: ASkyLight at SLS_CapturedScene, skyRealTimeCaptureRead=yes,
  ambientModel=skylight-captured-sky/ONE-OWNER/trilight-retired-to-zero,
  fillsRetiredToZero=yes, cvarReflectionMethod=2. The "skyModel=none-black,
  three directional lights and fog" reading above is from 2026-09-09 and was
  overtaken without this item being told.
  SO THE ITEM'S CLAIM THAT NONE OF THE THREE WORKS ALONE IS FALSIFIED IN THE
  DIRECTION THAT MATTERED: two of them shipped without the third. The surviving
  coupling is the other one, and it is not the sky. WETNESS NEEDS THE MATERIAL.
  /Game/Ledger/M_LedgerSurface exposes three texture parameters and exactly two
  scalars, TilingU and TilingV, measured in production/d1-probe/ue-material-log.txt
  on ce99814 rather than read off the script that builds it. Base colour is
  wired straight from its sampler and roughness straight from its sampler's R,
  so THERE IS NO PARAMETER A READ SITE COULD DRIVE, and a dynamic instance
  asking for one that does not exist sets nothing, returns nothing and logs
  nothing. A read site added alone is a dead write that READS BACK GREEN AND
  MOVES NO PIXEL.
  THE HDRI IS NOT REACHABLE and that is measured too:
  skyHdriFoundAt=NOT-FOUND, skyHdriBytes=0, skyHdriDetectedAs=not-read. The
  file exists in the repository at
  ledger/Assets/Resources/Sky/polyhaven/belfast_open_field_2k.hdr and nothing
  stages it: the workflow stages CityPackTextures by name and has no SkyHdri
  step. Not a missing asset, a missing staging line.
  AND THE C# IS NOT A PORT ANYONE CAN COPY. AssetLibrary.SetWetness is
  Unity-Standard-specific, driving _Glossiness or _GlossMapScale normalised by
  each roughness map's own mean. The portable part is two functions in
  Core/LightModel.cs:594-604, Smoothness and AlbedoScale, and by the standing
  rule those belong in SurfaceBind.h where g++ runs them.
  ONE MORE FOR WHOEVER TAKES IT: ApplyCondition has no handle on the material
  instances. MIDs are created per piece in BindSurfaces and assigned to
  components; nothing keeps them. Per-condition wetness needs that list kept,
  which is a new global and wants an owner named.
  WETNESS IS PARSED AND READ BY NOTHING in this engine. Three hits across the whole
  ue-probe tree, all in VignetteSpec.h: the field at 246, its initialiser at 248, its
  parse at 434. No read anywhere. It is NOT dead project-wide:
  ledger/Assets/Scripts/Game/StreetVignetteHost.cs:715 calls AssetLibrary.SetWetness in
  Unity. It is dead in the engine that takes rung 1's frame.
  WHY THESE ARE ONE ITEM AND NOT THREE. Codex's panel is lit BY its sky and its lower
  half is mostly sky and buildings reflected in standing water. Wiring Wetness alone
  makes the road darker and smoother WITH NOTHING TO REFLECT, which is a black road
  rather than a wet one. A builder given only the wetness half would discover that the
  expensive way.

  QUEUE 299 OPENS THE DOOR THIS ITEM NEEDS, noted 2026-09-15 while measuring
  the materials for queue 181 and not while looking for it. 299 gives
  M_LedgerSurface a colour parameter so the Unreal side can apply Unity's
  static albedo grade, which it has never applied. Core/LightModel.cs:601
  AlbedoScale(rain) = clamp(1.0 - 0.45 * rain, 0.55, 1.0) is a MULTIPLIER ON
  ALBEDO and wants the same parameter. So the two grades multiply into one
  colour and 299 is the half of this item that has no per-condition problem in
  it. The line beside it, LightModel.cs:588-593, is why it matters here and it
  is this item's own thesis in the original author's words: "Raising smoothness
  alone gives a bright shiny road that reads as polished plastic. Dropping
  albedo at the same time is what makes the lamps' reflections POP off a dark
  road, which is the entire look of a rainy street at night."
  WHAT 299 DOES NOT SOLVE, so that nobody reads this note as more than it is.
  The grade is per SURFACE and static, so it is set once at bind time and needs
  no handle on anything. Wetness is per CONDITION, so it still needs the MID
  list this item already says nothing keeps. 299 is the easy half arriving
  first; the hard half is untouched.

  AND THE HDRI HALF IS TWO PIECES OF WORK, NOT ONE, checked 2026-09-15 because
  Jafar's order for the visual slice puts "the sky itself" second and this item
  is where that lands. Both halves were read rather than recalled.
  THE ASSET IS ON DISK: ledger/Assets/Resources/Sky/polyhaven/
  belfast_open_field_2k.hdr, and overcast_day plus every grid_ condition names
  it. So "not a missing asset, a missing staging line" above is TRUE and stays.
  BUT STAGING IT ALONE MOVES NO PIXEL, and the code says so in its own words.
  VignetteShot.cpp:431 heads the three globals with "THE HDRI THE SHARED FILE
  NAMES: looked for, measured, NOT bound." LookForNamedHdri() is called at 1435
  and only measures. Line 36 of the same file lists what is deliberately absent:
  "No textures, no materials, no HDRI". So a staging line would move
  skyHdriFoundAt off NOT-FOUND and skyHdriBytes off 0 and change nothing a
  judge can see, which is exactly the shape CLAUDE.md rule 6 is about.
  AND THE SECOND PIECE IS A DESIGN CALL WITH A WRITTEN POSITION AGAINST IT.
  VignetteShot.cpp:163-171 argues for the atmosphere and the captured skylight
  over "the HDRI the shared file names", on the ground that what is LIT and
  what is REFLECTED are then the same object, "which an HDRI ambient beside an
  atmosphere backdrop would not", and it closes "The HDRI is the next rung".
  Swapping the sky model is therefore a ruling and not a task: the code holds a
  reasoned position, the position may well be right, and a resident does not
  overturn it by staging a file. PUT TO JAFAR RATHER THAN DECIDED HERE.
