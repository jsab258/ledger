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
