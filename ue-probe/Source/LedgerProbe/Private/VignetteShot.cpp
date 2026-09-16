// PHASE B: THE SHARED STREET BUILT FROM THE SHARED JSON, LIT TWO WAYS, AND
// PHOTOGRAPHED FROM THE TWO NAMED CAMERAS.
//
// WHAT MAKES THE FRAME ADMISSIBLE, which is the only reason any of this is
// as careful as it is. D1b requires every object in each engine to arrive
// from one shared JSON through a generator, and forbids a hand-edited scene
// or a hand-made uasset. So: nothing here is authored. Every actor's class,
// position, size and rotation comes out of production/specs/vignette-pieces.json,
// which Ledger.Core wrote from production/specs/vignette-scene.json; the
// reader is VignetteSpec.h, which has no Unreal type in it and is compiled
// and RUN by g++ before this is ever dispatched. This file contributes
// actors, lights and pixels, and NOT ONE DIMENSION.
//
// THE FRAME CONVERSION, DONE ONCE, HERE.
//   The file's frame: x along the street, y up, z across with +z east; yaw
//   is a bearing from +x turning toward +z; pitch is about +x and positive
//   tips the +z end down; roll is about +z and lays a cylinder along the
//   street; sizes are FULL sizes in metres, not half extents; the position
//   is the CENTRE of the piece.
//   This engine: X forward, Y right, Z up, centimetres, and FRotator's
//   Pitch is about Y, Yaw about Z, Roll about X.
//   So (X,Y,Z) = (x, z, y) * 100, and
//      Yaw = yaw_deg, Roll = -pitch_deg, Pitch = roll_deg.
//   Each of those three lines was derived from the convention rather than
//   tried: the file's yaw takes +x toward +z, which under this mapping is
//   +X toward +Y and is exactly a positive Unreal yaw; the file's pitch
//   takes +y toward +z, which is +Z toward +Y and is a NEGATIVE Unreal
//   roll; the file's roll takes +x toward +y, which is +X toward +Z and is
//   a positive Unreal pitch.
//   THE COMPOSITION ORDER IS UNEXERCISED and the reader proves it every
//   run: counts.multi_rotation is 0, so no piece in this scene carries two
//   non-zero rotations at once and the two engines cannot differ on the
//   order they compose them in. The run PRINTS that count rather than
//   trusting it, because the day it stops being zero this comment is wrong.
//
// WHAT IS DELIBERATELY NOT HERE. No textures, no materials, no HDRI: Phase
// C owns those and an untextured frame is the honest state of Phase B. The
// twenty-three prop pieces are boxes of the prop's own stated size, counted
// and named as stand-ins on the verdict so nobody reads a placed box as a
// loaded model, and the twenty decals are flat quads for the same reason.
// The sky is black, which is a Phase C hole and is named on the scene line
// rather than left for a reader to notice.
//
// ONE OWNER PER GLOBAL, WHICH THIS PROJECT HAS PAID FOR TWICE. ApplyCondition
// below is the ONLY writer of the fog, the sun and the ambient fill, and it
// writes all three every time a condition changes. Two writers on one render
// setting is how a fog calibration was lost for a week. SINCE QUEUE 309 it
// owns the street's WETNESS on the same terms, through ReDriveWetness: the
// Wetness scalar and the AlbedoGrade vector on every ground piece's material
// instance are written by that function and by nothing else once BindSurfaces
// has seeded them, and it is the only caller.
#include "VignetteShot.h"
#include "VignetteSpec.h"
#include "FrameStats.h"
#include "SurfaceBind.h"

#include "CoreMinimal.h"
#include "UObject/UnrealType.h"
#include "Misc/Paths.h"
#include "Misc/FileHelper.h"
#include "Misc/CommandLine.h"
#include "Misc/Parse.h"
#include "Misc/DateTime.h"
#include "HAL/FileManager.h"
#include "HAL/PlatformMisc.h"
#include "HAL/PlatformProcess.h"
#include "HAL/PlatformTime.h"
#include "Containers/Ticker.h"
#include "Modules/ModuleManager.h"
#include "UnrealClient.h"

#include "Engine/Engine.h"
#include "Engine/World.h"
#include "Engine/StaticMesh.h"
#include "Engine/StaticMeshActor.h"
#include "Components/StaticMeshComponent.h"
// UBodySetup and its AggGeom, for READING BACK how many simple collision
// primitives the imported prop mesh actually carries. A mesh with none
// renders perfectly and lets a walking Character straight through it.
#include "PhysicsEngine/BodySetup.h"
#include "Engine/PointLight.h"
#include "Components/PointLightComponent.h"
#include "Engine/DirectionalLight.h"
#include "Components/DirectionalLightComponent.h"
#include "Engine/ExponentialHeightFog.h"
#include "Components/ExponentialHeightFogComponent.h"
// QUEUE 186: THE SKY. ASkyLight is the ambient and the reflection source;
// ASkyAtmosphere is the visible sky it captures. ASkyAtmosphere is declared
// at the bottom of Components/SkyAtmosphereComponent.h in this engine and
// has no header of its own, which is the one include here nothing in this
// container can check.
#include "Engine/SkyLight.h"
#include "Components/SkyLightComponent.h"
#include "Components/SkyAtmosphereComponent.h"
#include "GameFramework/PlayerController.h"
#include "GameFramework/PlayerStart.h"
#include "Camera/CameraActor.h"
#include "Camera/CameraComponent.h"
#include "Engine/Texture2D.h"
#include "Materials/MaterialInterface.h"
#include "Materials/MaterialInstanceDynamic.h"
#include "HAL/IConsoleManager.h"
#include "IImageWrapper.h"
#include "IImageWrapperModule.h"

#include <clocale>
#include <string>
#include <vector>

namespace
{
	using namespace LedgerVignette;

	// ---- the shot's dimensions, and what they are ----------------------
	//
	// 1280x720 is the Unity host's ShotWidth and ShotHeight, character for
	// character, because a pair judged at two resolutions is not a pair.
	const int32 kShotW = 1280;
	const int32 kShotH = 720;
	// THE SAME WARM AND TIMED COUNTS THE UNITY HOST USES, for the same
	// reason: the first frames after a condition change compile shader
	// variants, which is a real cost and not the one a comparison is about.
	const int32 kWarmFrames  = 8;
	const int32 kTimedFrames = 24;

	// CEILINGS ON A HANG, NOT TARGETS. Each one prints the phase it killed,
	// so a slow world and a world that never came cannot read alike.
	const double kWorldCeiling = 45.0;
	const double kFileCeiling  = 25.0;
	const double kSettleAfterCondition = 0.5;

	// UNITY POINT LIGHT INTENSITY IS NOT UNREAL CANDELAS, and this number is
	// the first value of a series that has never been printed. The file says
	// intensity 3.2 for a sodium lantern, which is a Unity number; this
	// engine's point lights are in candelas by default and in a unitless
	// legacy scale when told to be. The lights are set to Unitless so the
	// two numbers are at least the same KIND of number, and this gain is
	// what multiplies the file's value. Rule 2 forbids calling it anything
	// better than a starting point: no series exists yet, the verdict prints
	// the value applied, and the first night frame is what a bound comes
	// from.
	const float kLampGainUnitless = 1.0f;
	// QUEUE 333: AND THE LAMP'S OWN GLASS, WHICH IS A DIFFERENT NUMBER ABOUT
	// A DIFFERENT THING. kLampGainUnitless above scales the point light the
	// lantern CASTS. This scales the EmissiveColor the lamp head's own
	// material CARRIES, which is the lit element the fixture never had: the
	// emissive flag spawned a light under the box and left the box itself
	// rendering through the ordinary metal surface, so the head was a dark
	// rectangle with an invisible lamp under it.
	//
	// THIS IS THE FIRST VALUE OF A SERIES THAT HAS NEVER BEEN PRINTED, and
	// rule 2 forbids calling it anything better. 1.0 unitless times the
	// file's lantern colour converted to linear gives (1.00, 0.70, 0.00)
	// linear, while the approved reference globe reads 242 of 255 against a
	// sky at 181 (queue 333, measured off the Hook sheet under D41), SO THIS
	// MAY WELL BE UNDER. It is deliberately NOT guessed upward to
	// compensate: the instrument that prints the series ships in the same
	// run (lampGlow on every shot line) so the second value comes off a
	// reading instead of off an argument.
	const float kLampEmissiveUnitless = 1.0f;
	// AND THE FOG. Unity's fogDensity is an exponential-squared coefficient
	// per metre; this engine's height fog density is a different
	// parameterisation entirely. Named, applied, printed, and NOT called
	// equivalent.
	const float kFogDensityGain = 1.0f;
	// THE AMBIENT FILL. Unity's host sets AmbientMode.Trilight with a sky, an
	// equator and a ground colour; this engine has no ambient mode, so the
	// same three colours arrive as three directional lights from above, from
	// the side and from below. It is the same statement about ambient light
	// made with the tool this engine has, it needs no captured sky and no
	// asset, and it cannot come back black the way a sky light with nothing
	// to capture can. It is NAMED on the scene line as a model so nobody
	// reads it as a physical sky.
	const float kFillSky = 0.55f, kFillEquator = 0.35f, kFillGround = 0.18f;
	// ---- QUEUE 186: THE SKY, AND WHY IT IS THIS SKY ---------------------
	//
	// WHAT WAS MEASURED FIRST, because none of the numbers below mean
	// anything without it. The day frame's top band reads 249.5/250.0/250.5
	// mean RGB over 8858 pixels and the night frame's SAME band reads
	// 188.4/179.6/179.3. Those two channel orders are the two fog
	// inscattering colours set eighty lines below: day 0.55/0.58/0.62 is
	// R<G<B and night 0.06/0.05/0.05 is R>G=B. THE FAR FIELD IN EVERY FRAME
	// THIS PROJECT HAS SHOT IS THE HEIGHT FOG, lifted to near white by auto
	// exposure. The scene line called it none-black and it was never black.
	//
	// WHY AN ATMOSPHERE AND A CAPTURED SKYLIGHT, and not the HDRI the shared
	// file names. A USkyLightComponent takes a CUBE texture and this engine
	// builds none at runtime; the pack's belfast_open_field_2k.hdr is a
	// long-lat Radiance file that would need resampling into six faces AND a
	// staging step to reach a packaged binary, which is three unverifiable
	// links instead of one. A SkyAtmosphere needs no asset at all, and a
	// SkyLight capturing it makes the thing that is SEEN and the thing that
	// is REFLECTED the same object, which an HDRI ambient beside an
	// atmosphere backdrop would not. The HDRI is the next rung and this run
	// prints whether the file is even reachable so that rung is a fact
	// rather than a guess.
	//
	// ---- THE PARAGRAPH ABOVE IS OVERTURNED IN PART, 2026-09-15 ----------
	//
	// IT IS KEPT RATHER THAN DELETED because two thirds of it are still
	// true and are still the work. What was overturned, and by whom:
	//
	// OVERTURNED: THE THIRD REASON, ON AESTHETICS, BY JAFAR, 2026-09-15.
	// The record is ledger-v2/respec/decision-register/D40. "The photograph
	// becomes the sky." The reasoned position above was written before
	// anyone had compared a rendered sky against the reference sheet, and
	// the comparison is what defeats it. Making the seen thing and the
	// reflected thing one object is a real virtue and it is not what is in
	// dispute; what is in dispute is that the object in question cannot be
	// made to look like the reference. Scattering constants move a physical
	// sky along a physical-sky axis, and the gap is not on that axis.
	//
	// WHAT THE GAP ACTUALLY IS, MEASURED, because a false reason inside a
	// correction is worse than no correction. Measured on the brightest 30
	// per cent of the top band of each, render against the Hook sheet:
	//     render      meanRGB 200.4/203.2/210.7  B/R 1.051
	//                 lumSD 2.21  p05-p95 spread 6.7
	//     Hook sheet  meanRGB 205.7/212.6/224.5  B/R 1.091
	//                 lumSD 4.18  p05-p95 spread 12.5
	// THE RENDER IS LESS BLUE THAN THE REFERENCE, NOT MORE: B/R 1.051
	// against 1.091. So this correction does NOT say the atmosphere renders
	// clear-sky blue, because it measurably does not, and anyone writing
	// that here later should read these six numbers first. What the numbers
	// do say is that the sheet has about TWICE THE STRUCTURE (lumSD 4.18
	// against 2.21, spread 12.5 against 6.7) and is 6 points brighter. THE
	// ATMOSPHERE RENDERS FLAT WHERE AN OVERCAST SKY HAS CLOUD STRUCTURE,
	// and flatness is what the spread measures. No scattering constant adds
	// cloud, because cloud is not a scattering term. A photograph has the
	// structure already.
	//
	// NOT OVERTURNED: REASONS ONE AND TWO. THEY WERE NEVER ARGUMENTS, THEY
	// ARE WORK, and a ruling on taste does not do any of it. They stand as
	// the cost of the rung, restated as tasks:
	//
	//   1. THE CUBE. A USkyLightComponent in SLS_SpecifiedCubemap takes a
	//      UTextureCube and this engine builds none at runtime. NOTE, for
	//      whoever takes the rung, that this component is already in
	//      SLS_CapturedScene (spawn site below) and that a captured skylight
	//      never needed a cube: the engine builds one internally from what
	//      is in the scene. The question that path turns into is therefore
	//      not "how do we build a cube" but "what puts the photograph in
	//      front of the capture", which is a backdrop mesh and an unlit
	//      material, neither of which exists here yet. That is a different
	//      and smaller problem than the sentence above states, but it is
	//      not no problem and it is not done.
	//
	//   2. THE STAGING. Still exactly true and still not done. Measured
	//      2026-09-15 rather than assumed: the workflow stages
	//      CityPackTextures and LedgerDecals by name and HAS NO SKY STEP AT
	//      ALL, which is why GHdriFoundAt reads NOT-FOUND. One detail for
	//      whoever writes that step, because it is easy to get wrong: the
	//      shared file's hdri field is "Sky/polyhaven/belfast_open_field_2k"
	//      and CARRIES ITS SUBDIRECTORY, so a flat copy answers nothing and
	//      the destination has to be SkyHdri/Sky/polyhaven/, the way the
	//      decal step keeps `generated`. Radiance decoding is the link after
	//      that and it is UNMEASURED: LookForNamedHdri already asks the
	//      ImageWrapper module what the file is, and skyHdriDetectedAs will
	//      answer it the first run the file is reachable, at the cost of no
	//      new key.
	//
	// ---- AND THE RUNG WAS TAKEN, 2026-09-16, UNDER D41 ------------------
	//
	// Both costs above are paid and neither is paid the way the paragraph
	// expected. THE CUBE WAS NEVER NEEDED: a sky light draws nothing, so the
	// thing that puts a photograph in a frame is geometry, and the dome is an
	// engine sphere with an unlit two-sided material (kSkyDomeMeshPath and
	// kSkyMaterialPath above). THE STAGING IS A WORKFLOW STEP that copies
	// ledger/Assets/Resources/Sky beside the project and beside the exe,
	// subdirectory and all, the way the decal step keeps `generated`. And the
	// RADIANCE DECODE was answered by not needing one: the photograph ships
	// as an 8-bit sRGB long-lat PNG made by tools/hdr-to-longlat.py, which is
	// a format this binary's own decoder reads 563 times a run.
	//
	// THE ATMOSPHERE IS KEPT AND IS NOT THE SEEN SKY ANY MORE. It still feeds
	// the sky light's real-time capture and still owns aerial perspective, so
	// nothing this file has calibrated moves; the dome sits in front of it.
	// skyModel names both halves and skyHdriBoundAs names the photograph.
	//
	// THE FOUR ATMOSPHERE NUMBERS ARE A STARTING POINT AND SAY SO. Rule 2
	// forbids calling them anything better: no series exists. Rayleigh is
	// cut because Rayleigh is the blue and Meridian is not blue; Mie is
	// raised because Mie is the pale haze an overcast sky is made of;
	// anisotropy is dropped toward zero because a forward-scattering halo is
	// a clear-sky look and the reference is flat; multi-scattering is taken
	// to its top because that is what fills a shaded sky.
	//
	// "EVERY ONE IS PRINTED" WAS FALSE AND IS CORRECTED, 2026-09-14. NONE of
	// the four is printed. Grepped the whole tree and the committed verdict:
	// there is no mie, rayleigh or scatter KEY anywhere in
	// production/d1-probe/ue-vignette-verdict.txt; the single textual hit is
	// the word "inscattering" in a prose line about meanRGB. The only uses of
	// these four are this declaration and the setters below.
	// AND NO RUN HAS EVER VARIED ONE. The atmosphere actor and all four
	// constants landed in a single commit, 884f049c on 2026-09-09, and nothing
	// has moved them since, so NOT ONE OF THE FOUR HAS EVER BEEN SHOWN TO MOVE
	// A PIXEL. That is queue 286's real first question and it is why 286's
	// series carries a Mie 0.000 rung as its own positive control: Mie off
	// against Mie at eighty times the engine default must change a sky if the
	// setter works, and if the rungs come back identical the run can then tell
	// "Mie is not the lever" from "the setter never took".
	const float kSkyRayleighScale   = 0.004f;   // engine default 0.0331
	const float kSkyMieScale        = 0.040f;   // engine default 0.003996
	const float kSkyMieAnisotropy   = 0.05f;    // engine default 0.8
	const float kSkyMultiScattering = 1.0f;     // engine default 1.0, named anyway
	// THE SKYLIGHT'S INTENSITY IS NO LONGER IN THIS FILE, QUEUE 205.
	// It was kSkyIntensityDay = 1.0f and kSkyIntensityNight = 0.35f,
	// chosen here by whether the sun was on. Both values now ride on the
	// CONDITION as sky_intensity, carried unchanged into overcast_day and
	// wet_night on 9 September; overcast_day's moved to 0.70 on 2026-09-14 by
	// Jafar's ruling off the sky cross on 622bc39
	// (decision-2026-09-14-ruling-the-reference-cell-is-the-grid-cell-at-the-judged-sky.md),
	// because the ladder's control row needs a day condition
	// with the sky at 0.35 and a constant keyed on SunOn cannot express
	// one. THEY ARE DELETED RATHER THAN LEFT UNUSED: a constant that
	// still looks live and feeds nothing is a number a later session
	// would change to no effect, which is the quietest fault there is.
	// The value in force is read back on every verdict as
	// skyIntensityRead and per frame as shotSkyIntensityRead.
	// HOW MUCH OF THE FAR FIELD THE HEIGHT FOG MAY STILL OWN, now that
	// something else is behind it. DERIVED, WITH ITS UNKNOWN NAMED. The
	// current far field measures 0.980 luma and the reference panel's sky
	// measures 0.808 (p50, 48800 px, Codex's Hook sheet, same luma weights).
	// If the atmosphere renders at S and the fog covers fraction M, the far
	// field is M*0.980 + (1-M)*S; S is the unknown and for S between 0.60
	// and 0.70 the M that lands on 0.81 is between 0.55 and 0.39. 0.45 sits
	// inside that range. IT IS NOT A MEASURED BOUND, it is one number
	// derived from two measured ones and one unknown, and the printed sky
	// band series is what replaces the unknown next run.
	// RETIRED 2026-09-09 BY A4: the value lives on every condition row of
	// production/specs/vignette-scene.json as fog_max_opacity, required in
	// both readers, and four probe rows at the grid's reference cell print
	// the series 0.450 / 0.250 / 0.100 / 0.000 that a constant would be set
	// from. The two judged conditions carried 0.450 when this was retired,
	// so nothing moved that day; overcast_day moved to 0.100 on 2026-09-14
	// by ruling off the rendered series, and the rows sharing its cell
	// followed it (ruling of 18:23Z).
	// The derivation is kept because it is what the series is read against:
	// the far field measured 0.980 luma against the reference panel's 0.808,
	// and for an atmosphere rendering at S between 0.60 and 0.70 the cap that
	// lands on 0.81 is between 0.55 and 0.39.
	// THE HDRI THE SHARED FILE NAMES, LOOKED FOR AND NOT BOUND. The pack
	// lives under the Unity tree and the workflow stages CityPackTextures by
	// name; nothing stages this, so NOT-FOUND is the expected answer and it
	// is worth having as a fact rather than as an assumption.
	const TCHAR* kSkyHdriExt = TEXT(".hdr");
	// ---- QUEUE 186 / D41: WHAT THE PHOTOGRAPH SHIPS AS ------------------
	//
	// PNG FIRST AND THE .hdr SECOND, and the order is the decision. The one
	// runtime image path this binary owns is ImportTexture below, which asks
	// the ImageWrapper module what the bytes are; that module has decoded a
	// PNG 563 times a run for the city pack and has never been shown to read
	// Radiance here. tools/hdr-to-longlat.py turns the approved Radiance file
	// into an 8-bit sRGB long-lat PNG beside it, measuring the photograph as
	// it goes. The .hdr is kept as the second candidate rather than dropped:
	// if this engine can read it, skyHdriDetectedAs says so on the first run
	// that reaches it, at the cost of no new key.
	const TCHAR* kSkyPhotoExts[2] = { TEXT(".png"), TEXT(".hdr") };
	// THE DOME, AND WHY A DOME AT ALL. A sky light DRAWS NOTHING: it lights
	// and it reflects. The only thing that puts a photograph in a frame is
	// geometry with an unlit material, which is also what the correction of
	// 2026-09-15 above says the rung turns into. One engine sphere, seen from
	// inside, big enough to enclose every piece the street spawns and small
	// enough that nothing here goes near the world bounds: the cameras sit
	// within about 100 m of the origin, so a 1 km radius moves the horizon by
	// under 6 degrees between them, and an overcast sky has no feature that
	// reading could be wrong about. The engine's basic shapes are one metre,
	// so the scale IS the diameter in metres, exactly as the piece loop says.
	const TCHAR* kSkyDomeMeshPath  = TEXT("/Engine/BasicShapes/Sphere.Sphere");
	const float  kSkyDomeDiameterM = 2000.0f;
	// THE MATERIAL, MADE BY tools/ue/make_sky_material.py IN THE EDITOR STEP,
	// never by hand, for the reason make_base_material.py's docstring gives:
	// a material is compiled shader code and a packaged game can only make
	// INSTANCES of materials that already exist as assets.
	const TCHAR* kSkyMaterialPath   = TEXT("/Game/Ledger/M_LedgerSky.M_LedgerSky");
	const TCHAR* kSkyMapParam       = TEXT("SkyMap");
	const TCHAR* kSkyLuminanceParam = TEXT("SkyLuminance");
	// THE FIRST VALUE OF A SERIES THAT HAS NEVER BEEN PRINTED, and rule 2
	// forbids calling it anything better. The dome is unlit, so this is an
	// absolute emissive going into an auto-exposed filmic tonemap whose key
	// nothing in the container that wrote this line can compute. 1.0 is the
	// identity and is deliberately NOT guessed upward to compensate for
	// anything: the frame's own sky band is the reading the second value
	// comes off, exactly as the lamp glow constant above is handled.
	//
	// ---- QUEUE 361, AND THE NAME CHANGED WITH THE MEANING ---------------
	//
	// IT IS A GAIN NOW AND NOT THE VALUE. It was written into the instance
	// once at build and served day and night alike, which is why a night row
	// rendered at 3.3 times its previous mean. The value in force is this
	// gain times the CONDITION's sky_intensity, computed by
	// LedgerVignette::SkyDomeLuminance where g++ runs it and written by
	// ReDriveSkyLuminance, which is the ONLY writer of this parameter: the
	// build no longer writes it, for the reason this file's own header gives
	// about two writers on one setting.
	//
	// 1.0 IS STILL THE IDENTITY AND STILL UNMEASURED. It is deliberately NOT
	// guessed in either direction to compensate for anything, and in
	// particular it is NOT tuned to land a night frame back on run 49's mean
	// of 43.6: that frame had no dome in it at all, so matching it would be
	// matching an absence. The frame's own sky band is the reading the second
	// value comes off, exactly as the lamp glow constant above is handled.
	const float  kSkyLuminanceGain = 1.0f;
	// HOW FAR A DECAL QUAD IS LIFTED OFF THE SURFACE IT SITS ON. Not in the
	// file: the file describes a decal, which has no thickness and no
	// z-fighting, and this engine is drawing it as a quad until Phase C.
	// One centimetre is a millimetre-scale artefact at any distance the two
	// cameras see, and it is printed so nobody has to find it in code.
	const float kDecalLiftCm = 1.0f;

	// ---- queue 059: what it takes to ask whether a light reached a pixel --
	//
	// THE PROBE GRID. The peak sample region is a cell of this grid and the
	// verdict prints the cell and its pixel rectangle, so a reader knows
	// WHERE the contribution landed without opening the frame. Eight by four
	// over 1280x720 is a 160x180 cell, which is about the size a lantern's
	// pool of light covers at this camera distance. It is a reporting
	// resolution, not a bound.
	const int32 kProbeGridCols = 8;
	const int32 kProbeGridRows = 4;
	// A CEILING ON THE PASS, NOT A TARGET, AND IT ANNOUNCES WHEN IT BITES.
	// Every probe frame is a screenshot round trip and the file ceiling above
	// is 25 seconds, so a machine that stops writing files could otherwise
	// spend fourteen of them here. When this bites, the lights it cost are
	// counted on the light-pass line and the status reads PARTIAL-BUDGET-BIT.
	const double kLightProbeBudgetSeconds = 240.0;
	// ONE SCRATCH NAME FOR EVERY PROBE FRAME, deleted when the run ends.
	const TCHAR* kProbePngLeaf = TEXT("ue-lightprobe.png");
	// AND ONE FOR THE DETERMINISM REPEAT, which is half of a difference and
	// not evidence, exactly as a probe frame is. Deleted when the run ends.
	const TCHAR* kRepeatPngLeaf = TEXT("ue-rigrepeat.png");

	// ---- THE EXPOSURE IS PINNED IN TIME, NOT IN VALUE --------------------
	//
	// WHAT THIS NUMBER IS AND WHERE IT CAME FROM. Eye adaptation blends the
	// current exposure toward the histogram's target by a factor that decays
	// exponentially with the frame's own delta time, so the number below is
	// a RATE, not a threshold on any measurement, and it is chosen to be far
	// enough above the run's own frame rate that the blend completes inside
	// one frame. Run 38's slowest shot measured frameMedianMs=5.26, and at
	// 5.26 ms a rate of 10000 leaves less than one part in 10^15 of the old
	// exposure, which is below a float's ability to hold it. The 32 frames
	// this rig stands still for before every shutter cover any frame time
	// from 0.1 ms up.
	//
	// WHY A RATE AND NOT A FIXED EXPOSURE VALUE. Pinning the VALUE would need
	// a number nothing here has measured: the adapted exposure is a render
	// thread quantity this process never reads, and rule 2 forbids inventing
	// it. Pinning the RATE removes the temporal state without moving the
	// exposure policy, so a still keeps the level a player standing on that
	// spot would settle at; only the transition is gone. If the rig repeat
	// still reads DIFFERS after this, the follow-up pins the value off the
	// series this run prints, in that order.
	const double kExposureSnapSpeed = 10000.0;

	// ---- AND THE RATE SNAP DID NOT SETTLE IT, QUEUE 235 -------------------
	//
	// WHAT THE ACCEPTANCE TEST SAID. On 83dec33, with the rate already at
	// 10000, one camera under one condition photographed first and again last
	// read rigDeterminism=DIFFERS, rigDiffPixels=921600/921600,
	// rigMeanLumaFirst=0.6102 against rigMeanLumaRepeat=0.9562. Five frames
	// of twenty five were blown, up to 604972/921600 pixels clipped, and one
	// was nearly black at 0.0623. THE RATE IS THE WRONG LEVER and that is a
	// measurement, not an argument: it is already at 10000 and the fault
	// survived it.
	//
	// THERE IS NO EXPOSURE CONSTANT IN THIS FILE, AND THAT IS DELIBERATE.
	// The next lever is the VALUE: AutoExposureMinBrightness equal to
	// AutoExposureMaxBrightness leaves the histogram nothing to move. The
	// value cannot be computed from anything this project has committed,
	// because shotMeanLuma is the mean of a tonemapped 8-bit frame and these
	// two clamps are scene-luminance inputs read before the tonemap, with no
	// arithmetic joining them. So the number lives in the shared file as
	// `exposure_pin` on the CONDITION, four ladder rungs bracket the engine's
	// own default range, and the run prints what each rung came out at. A
	// later commit sets the value from that series. Ship the printer, read the
	// runs, set the bound, in that order, and NO VALUE IS CHOSEN HERE.
	//
	// THE COST, PAID THE MOMENT A PIN IS IN FORCE, written here rather than
	// in a commit message because this is where a future session will look:
	// A PINNED FRAME CAN NEVER JUDGE AN ADAPTATION MOMENT. Walking out of a
	// dark alley and having the street bloom open is exactly the thing this
	// rig stops being able to photograph while a pin is on. That cost was
	// accepted in writing when the rate was snapped, section 2.3 of
	// game-design/decision-2026-09-09-ruling-the-settled-exposure-and-the-
	// two-lanes.md, and it is larger now: with the two clamps equal the
	// exposure does not merely settle instantly, it does not respond to the
	// scene at all, so a condition that genuinely is darker renders darker
	// and a frame can legitimately clip. That is the point of a photometric
	// rig and it is a loss for anything judging an eye.

	// ---- phase C: the pack's maps and the one asset a script had to make --
	//
	// THE BASE MATERIAL IS A BUILD PRODUCT, NOT A HAND-MADE ASSET. Unreal
	// compiles materials in the editor and a packaged game can only INSTANCE
	// one, so Phase C needs exactly one binary asset;
	// tools/ue/make_base_material.py makes it in the cook step and the cook
	// carries it in through +DirectoriesToAlwaysCook=(Path="/Game/Ledger").
	// If it is not there this run says so on the materials line and the
	// street still renders untextured: a missing material is a finding, not
	// a black frame.
	const TCHAR* kBaseMaterialPath = TEXT("/Game/Ledger/M_LedgerSurface.M_LedgerSurface");
	// HOW MANY METRES ONE TILE OF A PACK TEXTURE COVERS. A convention, named
	// and printed, not a measured bound: the pack ships no scale and this is
	// the first value of a series nothing has printed yet.
	const double kMetresPerTile = 2.0;

	enum class EPhase : uint8
	{
		WaitWorld, Build, ApplyShot, Warm, Timed, Ask, WaitFile, Done
	};

	Spec        GSpec;
	std::string GSpecErr = "not-read";
	FString     GSpecPath;
	std::vector<std::string> GSpecTried;

	FTSTicker::FDelegateHandle GTicker;
	EPhase  GPhase       = EPhase::WaitWorld;
	int32   GTicks       = 0;      // cumulative ticker calls since armed
	int32   GPhaseTicks  = 0;      // ticks inside the current phase
	double  GStart       = 0.0;
	double  GPhaseStart  = 0.0;
	double  GLastTick    = 0.0;
	int32   GShotIndex   = 0;
	bool    GUseHighRes  = false;  // set once, after candidate A fails once
	bool    GTriedHighResThisShot = false;
	int64   GSizeTracker = -1;
	FString GAskedPath;
	FString GNote        = TEXT("none");

	std::vector<double> GFrameMs;                 // the current shot's series
	std::vector<std::string> GShotLines;          // one per shot, in order
	std::string GSceneLine = "sceneStatus=NOTHING-EMITTED piecesEmitted=0/0";
	std::string GArt;                             // ascii luma of the first frame that decoded
	int32 GWrote = 0, GBlank = 0, GNoFile = 0;

	AActor* GSceneRoot = nullptr;
	ADirectionalLight* GSun = nullptr;
	ADirectionalLight* GFillA = nullptr;
	ADirectionalLight* GFillB = nullptr;
	ADirectionalLight* GFillC = nullptr;
	AExponentialHeightFog* GFog = nullptr;
	// A1(c) AND CONDITION C5: HOW MANY CELLS READ BACK WHAT THEY ASKED FOR.
	// Whole-run counters, incremented once per photographed shot by
	// ShotLightNow and read once by the verdict. The determinism repeat is
	// NOT counted: it re-photographs shot 0, so counting it would put a
	// denominator of 26 over a shot list of 25, which is rule 3b's exact
	// fault (a denominator larger than the set examined).
	int32 GCellsAgree = 0, GCellsRead = 0;
	// A6: THE ROTATION EACH DIRECTIONAL LIGHT WAS ASKED FOR, RECORDED AT THE
	// SPAWN CALL AND NEVER RE-DERIVED. Re-deriving the sun's asked pitch from
	// the spec at readback time would compare SunPitchDeg against itself and
	// agree however the spawner mangled the value; this holds the pair that
	// was actually handed to SpawnDirectional. Four entries, the four lights
	// this rig spawns, and kDirectionalLights is their denominator.
	const int kDirectionalLights = 4;
	std::vector<LedgerVignette::LightAim> GLightAsked;
	void RecordAsked(const char* Name, ADirectionalLight* L, const FRotator& Rot)
	{
		LedgerVignette::LightAim A;
		A.Name = Name;
		A.bSpawned = (L != nullptr);
		A.AskedPitch = (double)Rot.Pitch;
		A.AskedYaw = (double)Rot.Yaw;
		GLightAsked.push_back(A);
	}
	// QUEUE 186. Both are written by ApplyCondition and by nothing else, the
	// same rule the sun, the fills and the fog already live under.
	ASkyLight*      GSky        = nullptr;
	ASkyAtmosphere* GAtmosphere = nullptr;
	// WRITE ONCE PER SHOT, NEVER PER SETTLE TICK, AND BOTH HALVES COUNTED.
	// ApplyCondition is re-entered every tick while a condition settles, so a
	// recapture written per tick is a rebuild asked for a hundred times over,
	// and the two counters are what prove the guard is doing its job rather
	// than being trusted to.
	//
	// IT USED TO BE KEYED ON THE CONDITION ID, WHICH MADE THE AGE OF A
	// FRAME'S SKY A FUNCTION OF THE SHOT ORDER. Two shots naming the same
	// condition in a row got ONE capture between them, so the second was
	// photographed against a cubemap a whole shot older than the first's,
	// and which shots those were depended entirely on the order the file
	// lists them in. MEASURED, AND IT IS A LATENT PATH RATHER THAN RUN 38's
	// FAULT: that run's eleven shots name no condition twice in a row, so it
	// wrote the sky eleven times over eleven shots and no frame in it carries
	// a stale capture. The epoch is bumped once per photographed pass
	// instead, so the shot list can be reordered or extended without the
	// question coming back.
	int32       GSkyEpoch     = -1;   // the pass the sky was last written for
	int32       GWantSkyEpoch = 0;    // bumped once per pass, at build and per shot
	int32       GApplyCalls   = 0;
	int32       GSkyWrites    = 0;
	// THE PHOTOGRAPH THE SHARED FILE NAMES: looked for, measured, AND NOW
	// BOUND. GHdriFoundAt is sanitised for the verdict line; GHdriFoundPath
	// is the same path as the file system spells it, because a key that has
	// had its spaces taken out is not a path any longer.
	std::string GHdriFoundAt    = "NOT-LOOKED-FOR";
	long long   GHdriBytes      = 0;
	std::string GHdriDetectedAs = "not-read";
	FString     GHdriFoundPath;
	// WHAT BECAME OF IT, WHICH IS THE ONE KEY A READER TRUSTS. Only the two
	// functions that own the dome write it, and a failure writes NOTHING with
	// its reason rather than a plausible silence.
	std::string GHdriBoundAs    = "NOTHING/not-attempted";
	// LAST-WINS: which photograph is on the dome right now. Per-condition,
	// because the night condition names a different one and a day sky over a
	// night street is worse than the sky this replaces.
	std::string GSkyPhotoNow    = "none";
	// CUMULATIVE over the run: texture writes to the dome. Under write-on-
	// change this is the number of CHANGES and not the number of shots, so it
	// is smaller than the shot count by design and says so here.
	int         GSkyPhotoBinds  = 0;
	AStaticMeshActor*         GSkyDome    = nullptr;
	UMaterialInstanceDynamic* GSkyDomeMid = nullptr;
	// THE MATERIAL THE INSTANCE WAS MADE FROM. is-sky, two-sided and the
	// shading model are the PARENT material's properties; a dynamic instance
	// does not carry them, so reading them off GSkyDomeMid would report
	// nothing-measured for ever. Set only where the instance is made, so it
	// is non-null exactly when a dome stands.
	UMaterialInterface*       GSkyDomeParent = nullptr;
	// One decoded photograph per NAME, so a 43-shot plan decodes two files
	// and not forty-three.
	TMap<FString, UTexture2D*> GSkyPhotoCache;
	ACameraActor* GCam = nullptr;
	TArray<APointLight*> GLanterns;
	TArray<APointLight*> GWindows;
	TMap<FString, AStaticMeshActor*> GByName;
	// A SEPARATE MAP FOR THE CRIME PROBE'S OWN PIECES, ruling of 2026-09-08
	// section 2. Shards, a brick, two stand-in bodies and a yard floor are
	// NOT street pieces: they are not in vignette-pieces.json, nothing
	// regenerates them and no count of the street may include them. Keeping
	// them out of GByName is what leaves piecesEmitted=593/593, propStandIns,
	// the surface binds and every other vignette counter reading exactly what
	// they read before this map existed.
	TMap<FString, AStaticMeshActor*> GProbeByName;
	// THE NAMES OF THE LIGHTS, IN THE ORDER THEY WERE SPAWNED. A per-light
	// reading whose subject is called "light 3" is not attributable to
	// anything in the file, so the piece name the lantern hangs under and the
	// lit_bays name the practical sits in are kept beside the pointers.
	std::vector<std::string> GLanternNames;
	std::vector<std::string> GWindowNames;

	// ---- the light pass ---------------------------------------------------
	bool    GProbing        = false;
	int32   GProbeSeq       = -1;     // -1 is the control, then 0..N-1
	bool    GProbeVisWas    = true;   // CAPTURED, never assumed, before a toggle
	double  GProbeStarted   = 0.0;    // when the first probe of the run began
	double  GProbeSpent     = 0.0;    // cumulative seconds inside the pass
	TArray64<uint8> GRefBgra;         // the reference frame, kept to diff against
	int32   GRefW = 0, GRefH = 0;
	std::string GRefShotId;
	std::vector<std::string> GLightLines;
	int GProbed = 0, GEligible = 0, GSkippedOff = 0;
	int GSkippedBudget = 0, GProbeNoFile = 0, GRestoreMismatch = 0;
	int GShotsProbed = 0, GControls = 0;
	// QUEUE 326: THE FLOOR PASS, WHICH IS WHERE `REACHED` NOW COMES FROM.
	// `GReached` used to be counted here against `RoseAtLeast[0] > 0`, one
	// pixel rising by one code value, which run 47's control cleared while
	// toggling nothing. Nothing in this file counts a read any more: the
	// shot's control and its lights go into a LedgerFrame::LightFloor and
	// every comparison and tally happens in the header where g++ runs them.
	LedgerFrame::LightFloor GFloor;                    // the shot in flight
	std::vector<LedgerFrame::LightFloor> GFloors;      // one per probed shot
	// QUEUE 329: WAS THIS SHOT'S OWN REFERENCE FRAME BLANK. Read off
	// FrameStats::Measure in MeasureShot, which is the one place this module
	// measures a shot frame, and carried here so the probe pass never
	// differences anything against a frame that failed to render.
	bool GRefBlank = false;
	// QUEUE 329: the whole-run count of probe frames and the blank ones among
	// them, cumulative, control frames included.
	LedgerFrame::LightProbeFrames GProbeFrames;
	FString GToneLine = TEXT("tonemapRead=NOT-REACHED");

	// ---- QUEUE 325: WHAT THE CAPTURE HAD DONE WHEN THE SHUTTER FIRED -----
	//
	// Per-capture, last-wins, overwritten by every capture including the
	// probe's: the shot line reads them for its own capture, which is the
	// one that just landed when MeasureShot runs.
	int32  GWarmTicksAtAsk   = 0;     // ticks the Warm phase actually ran
	int32  GTimedAtAsk       = 0;     // timed samples held when the shutter fired
	double GAskStarted       = 0.0;   // when the capture was requested
	double GSecondsToSettle  = -1.0;  // ... to SizeSettled; negative means none
	bool   GCaptureSettled   = false;

	// ---- the rig's own determinism (the shot-order exposure fault) -------
	//
	// THE FIRST SHOT'S PIXELS, KEPT FOR THE WHOLE RUN so the repeat at the
	// end has something to be identical to. One frame of BGRA8 at 1280x720
	// is 3.7 MB and it is held once, not once per shot.
	TArray64<uint8> GFirstBgra;
	int32       GFirstW = 0, GFirstH = 0;
	std::string GFirstShotId;
	bool        GRepeating = false;   // the repeat pass is in flight
	bool        GRepeatRan = false;   // and it is taken exactly once
	std::string GRigLine = LedgerFrame::RigDeterminismLine(
		std::string(), 0, 0, "NOT-RUN", LedgerFrame::RepeatDiff());
	// ONE PASS IS ONE PHOTOGRAPHED SHOT OR THE REPEAT. The preamble each pass
	// writes (the control quads' visibility, the sky recapture) is written
	// once per pass and never per settle tick, and keying it on the PASS
	// rather than on the shot index is what lets the repeat re-run shot 0's
	// preamble in full instead of inheriting the last shot's.
	int32 GShotPass     = 0;
	int32 GPassPrepared = -1;
	// WHICH CAPTURE PATH TOOK THIS FRAME. GUseHighRes is adopted for the
	// whole run the first time candidate A writes nothing, so a run can
	// legitimately contain frames from two different capture paths and
	// nothing on the shot line said which. Per-sample, on the sample line.
	std::string GCaptureVia = "requestscreenshot";
	// THE CAMERA THAT TOOK THIS FRAME, QUEUE 208. Filled by PlaceCamera and
	// read by MeasureShot, so the pose rides the shot line rather than the
	// one-per-run line the shot loop used to overwrite.
	LedgerVignette::ShotCamIn GShotCam;

	// ---- the exposure pin, queue 235 --------------------------------------
	//
	// THE PIN THE CONDITION IN FORCE ASKED FOR. Set by ApplyCondition, which
	// is the one place that holds the Condition, and read by PlaceCamera,
	// which is the one place that writes post-process values. Two globals and
	// one writer each: the alternative was handing the condition to
	// PlaceCamera and giving the exposure a second owner.
	double GExposurePinNow = 0.0;
	// WHICH LIGHTING FAMILY THE CONDITION IN FORCE STANDS IN, carried beside
	// the pin so the shot line can say day or night without a second lookup.
	bool   GExposurePinFamilySunOn = false;
	// AND WHAT THE COMPONENT SAID AFTER THE WRITE, PER SHOT. The run-wide
	// tonemap line is one-per-run and last-wins, which is section 7 fault 5 of
	// the 2026-09-09 ruling: the action is per camera placement and the
	// evidence for it was not, and only the evidence is committed.
	LedgerVignette::ExposurePinIn GShotPin;
	int32 GPinAsking = 0, GPinRead = 0, GPinHeld = 0, GPinLeaked = 0;
	// ---- WHAT THE COMPONENT SAID BEFORE THIS MODULE TOUCHED IT ----------
	//
	// CAPTURED, NEVER ASSUMED. A shot that asks for no pin has to put the two
	// brightness fields back to something, and the only honest something is
	// what was there first. Typing the engine defaults in from memory would
	// make an unpinned frame carry this file's idea of the engine's policy;
	// the run at f6508b3 read them as 0.0300 and 8.0000, which is evidence
	// about ONE engine version and not a constant.
	// Captured ONCE, at the first camera placement of the run, before the
	// first write. bCaptured false means no camera component ever answered.
	bool   GPinCaptured    = false;
	double GPinCapturedMin = 0.0, GPinCapturedMax = 0.0;
	// THE LADDER'S ROWS, COLLECTED IN SHOT ORDER. Only rows whose condition
	// asks for a pin enter this, and the predecessor's lighting family is READ
	// off the shot photographed before this one rather than off the row's name.
	std::vector<LedgerVignette::ExposureLadderSample> GLadder;
	bool GPrevShotWasDay  = false;
	bool GPrevShotExists  = false;

	// ---- the material pass -------------------------------------------------
	FString GTexRoot;
	int32   GTexRootFiles = 0;
	// WHERE THE SEARCH LOOKED, kept because `texRoot=NOT-FOUND` on its own
	// cannot say whether the pack or the search is in the wrong place.
	std::vector<std::string> GTexRootTried;
	UMaterialInterface* GBaseMaterial = nullptr;
	std::vector<LedgerSurface::Bound> GBinds;
	int32 GTexturesImported = 0, GMidsCreated = 0;
	// ---- the decal pass, queue 223 ----------------------------------------
	// WHERE THE TWENTY PICTURES ARE, AND WHAT EACH QUAD DID WITH ITS OWN.
	// Separate from the texture root on purpose: the pack and the decals are
	// staged by two different steps and a single `NOT-FOUND` covering both
	// would not say which one is missing.
	FString GDecalRoot;
	int32   GDecalRootFiles = 0;
	std::vector<std::string> GDecalRootTried;
	std::vector<LedgerSurface::DecalResult> GDecalResults;
	std::string GDecalsLine =
		"decalsStatus=NOT-REACHED decalsPainted=nothing-measured"
		" decalsNote=the-material-pass-never-ran";
	// THE RUN'S PAINT CENSUS, ONE INCREMENT PER PIECE. Whole-run counters,
	// filled by the piece loop in BindSurfaces and read once by the materials
	// line. Its denominator is the pieces the loop EXAMINED, never the count
	// the file asked for.
	LedgerSurface::PaintTally GPaint;
	// THE WETNESS THIS RUN SEEDS ITS INSTANCES WITH, QUEUE 186. Chosen once,
	// in SurfaceBind.h where g++ runs the choosing, and read by the piece
	// loop below. IT IS A SEED AND NOT THE RUN'S WETNESS SINCE QUEUE 309:
	// BindSurfaces runs inside BuildScene, before any condition exists, so
	// this is what every instance is MADE with and nothing more. What each
	// frame is photographed at is driven per condition by ReDriveWetness
	// below, and the verdict prints both under different names.
	LedgerSurface::WetnessChoice GWetness;
	// THE PER-CONDITION RE-DRIVE'S GUARD AND ITS TALLIES, QUEUE 309. Written
	// by ReDriveWetness and by nothing else, which is the same rule the sun,
	// the fills, the fog and the sky already live under; ReDriveWetness in
	// turn is called by ApplyCondition and by nothing else. The decision, the
	// counts and every string are in SurfaceBind.h where g++ runs them.
	LedgerSurface::WetRedrive GWetRedrive;

	// ---- QUEUE 333: THE EMISSIVE PIECES, AND THE INSTANCE EACH ONE HOLDS -
	//
	// RECORDED BY THE PAINT LOOP, NEVER MADE HERE. Every non-decal piece
	// already gets one UMaterialInstanceDynamic of its own under the ONE
	// INSTANCE PER PIECE comment below, and the four lanterns are
	// shape=box surface=metal so they come through exactly that route. This
	// keeps a SECOND REFERENCE to the instance that route made, so the
	// per-condition drive can write EmissiveColor on the instance the
	// renderer is actually using instead of making a second one nothing
	// draws.
	//
	// THE LIFETIME IS THE COMPONENT'S AND NOT THIS VECTOR'S: the same
	// instance is held by Comp->SetMaterial(0, Mid) on an actor in the
	// world, which is what keeps it from being collected. This is never the
	// only reference to it, in the same way GLanterns is never the only
	// reference to a point light actor.
	//
	// AND THE DENOMINATOR FALLS OUT OF THE SIZE. A lantern that fell down
	// any of the paint loop's unpainted exits (no bind record, no actor, no
	// component, no instance) is never pushed here, so held over
	// EmissiveCount is the count that can glow over the count the file
	// asks for, and the two differ exactly when one was lost.
	struct LampPiece
	{
		size_t                    PieceIndex;   // into GSpec.Pieces
		UMaterialInstanceDynamic* Mid;
		UStaticMeshComponent*     Comp;
	};
	std::vector<LampPiece> GLampPieces;

	// ---- QUEUE 333: THE WRITE-ON-CHANGE GUARD FOR THAT DRIVE ------------
	//
	// WHY THIS STRUCT IS IN THIS FILE AND NOT BESIDE LedgerSurface::
	// WetRedrive IN THE TESTED HEADER, said here rather than left to be
	// found: this change was scoped to one file. It therefore ships UNRUN,
	// which is the silent-instrument risk instruments.md names, so the
	// arithmetic in it is held down to counter increments and one boolean
	// compare: there is no division, no percentage and no derived statistic
	// anywhere in it or in its segment. Moving it into SurfaceBind.h beside
	// WetRedrive, where g++ runs it, is the named next step.
	//
	// WHAT EACH NUMBER IS A STATISTIC OF: Calls, Skipped, Walks, Visits,
	// Wrote and NoMid are CUMULATIVE over the run; bWantOn and LastFrom are
	// LAST-WINS, the state the most recent walk wrote.
	struct LampDrive
	{
		int         Calls;         // drive entries, one per ApplyCondition
		int         Skipped;       // entries the guard turned away
		int         Walks;         // entries that wrote
		int         Visits;        // emissive pieces stepped over
		int         Wrote;         // pieces whose instance took the write
		int         NoMid;         // kept pointer came back null
		bool        bEverApplied;
		bool        bWantOn;       // last-wins
		bool        bHaveWant;
		std::string LastFrom;      // last-wins: the condition id
		bool        bCompIsMidAsked;
		bool        bCompIsMid;
		std::string CompIsMidOn;   // which lantern answered it
		LampDrive()
			: Calls(0), Skipped(0), Walks(0), Visits(0), Wrote(0), NoMid(0),
			  bEverApplied(false), bWantOn(false), bHaveWant(false),
			  LastFrom("none"), bCompIsMidAsked(false), bCompIsMid(false),
			  CompIsMidOn("none") {}
	};
	LampDrive GLampDrive;
	// QUEUE 361: THE DOME'S LUMINANCE GUARD, AND ITS STRUCT, ITS ARITHMETIC
	// AND ITS STRING ALL LIVE IN THE TESTED HEADER, which is the named next
	// step LampDrive above is still owed. Nothing about this drive ships
	// unrun except the three engine calls, and every one of those has a
	// signature already compiled in this file.
	LedgerVignette::SkyLumDrive GSkyLumDrive;
	std::string GMaterialsLine =
		"materialsStatus=NOT-REACHED materialsNote=the-material-pass-never-ran";

	// ---- the control quads, which are this pass's accepting case ---------
	// One extra plane per control in front of the camera the first shot
	// uses. They carry no street data and are not pieces: they exist so that
	// a frame can show what a WORKING material instance looks like beside
	// the street that is not showing one.
	std::vector<LedgerSurface::QuadResult> GQuads;
	// C4 AS AMENDED: THE NULL SERIES IS A SPREAD OVER SEVEN FRAMES AND NOT
	// ONE PAIR, so the run keeps the three statistics C4 reads per shot
	// instead of discarding the band stats at the end of the scoped block
	// that measured them. One record per MEASURED shot, in shot order,
	// which is the only order that can answer whether a drift is monotone.
	// The grouping, the arithmetic and every string are in VignetteSpec.h,
	// where g++ runs them before any dispatch.
	std::vector<LedgerVignette::FrameSample> GFrameSamples;
	std::vector<std::string> GQuadLines;
	// THE CONTROL QUAD ACTORS THEMSELVES, KEPT so that a shot which is not
	// the one they were placed for can hide them. They are an instrument, and
	// vignette-spec-test measures one of them reaching column 1274 of
	// cam_hook's 1280 wide frame, which is an instrument standing in the
	// picture rung 1 is judged by. The RULE is LedgerSurface::
	// ControlQuadsVisibleFor and lives in the header the test compiles; this
	// is only its call site and its tally.
	TArray<AStaticMeshActor*> GQuadActors;
	int   GQuadShotsSeen = 0;     // shots that reached the write, over which the tally is taken
	int   GQuadHidden = 0;        // of those, how many had the controls hidden
	std::string GQuadHiddenIds;

	std::string GQuadDone =
		"controlQuadsStatus=NOT-REACHED controlQuads=nothing-measured"
		" controlQuadsNote=the-control-pass-never-ran";
	UTexture2D* GControlTex = nullptr;

	// DECLARED HERE, DEFINED BELOW. BuildScene calls them and is written
	// above them, and the pack import needs DecodeBgra's neighbours to be in
	// scope.
	void BindSurfaces();
	// QUEUE 186. Defined beside the texture search it borrows its candidate
	// list from; declared here because BuildScene calls it.
	void LookForNamedHdri();
	void BuildSkyDome(UWorld* World);
	void BindSkyPhoto(const std::string& Name);
	void SpawnControlQuads(UWorld* World, UStaticMesh* Plane);
	// A1(d): the per-sample control-quad declaration needs the camera the
	// quads were placed from, and MeasureShot is written above the lookup.
	const Camera* ControlCamera();

	FString NoSp(const FString& In) { return In.Replace(TEXT(" "), TEXT("~")); }

	// MOBILITY LIVES ON THE ROOT COMPONENT, NOT ON THE ACTOR. AActor has no
	// SetMobility; AStaticMeshActor happens to, and a light does not. It is
	// not cosmetic: a spawned light defaults to a mobility that needs BUILT
	// lighting, and this project has no built lighting and never will in a
	// runtime-generated scene, so a static light would simply not light
	// anything and the frame would come back black with every count green.
	void MakeMovable(AActor* A)
	{
		if (A == nullptr) { return; }
		if (USceneComponent* Root = A->GetRootComponent())
		{
			Root->SetMobility(EComponentMobility::Movable);
		}
	}

	FString AbsProject(const TCHAR* Leaf)
	{
		return FPaths::ConvertRelativePathToFull(FPaths::Combine(FPaths::ProjectDir(), Leaf));
	}

	FString ShaFromCommandLine()
	{
		FString Sha;
		if (!FParse::Value(FCommandLine::Get(), TEXT("LedgerCommit="), Sha) || Sha.IsEmpty())
		{
			Sha = TEXT("SHA-UNKNOWN");
		}
		return NoSp(Sha);
	}

	// THE SPEC IS LOOKED FOR IN SEVERAL PLACES AND THE ONE USED IS NAMED,
	// exactly as the golden table is. A packaged build's ProjectDir is the
	// STAGED project, not the source tree, so one hard-coded location works
	// in exactly one of the two ways this binary gets run. Searching is
	// fine; searching silently is not.
	//
	// UNTIL RUN 19 THIS LIST WENT NOWHERE. It was filled, assigned to a
	// global and never printed, so a piece list that could not be found named
	// nothing at all; the search that does print its candidates is the golden
	// table's, in LedgerProbe.cpp. It is emitted below now, through the same
	// tested formatter the texture root uses.
	FString FindSpec(std::vector<std::string>& OutTried)
	{
		TArray<FString> Candidates;
		Candidates.Add(FPaths::Combine(FPaths::ProjectDir(), TEXT("vignette-pieces.json")));
		Candidates.Add(FPaths::Combine(FPaths::ProjectContentDir(), TEXT("vignette-pieces.json")));
		Candidates.Add(FPaths::Combine(FPaths::LaunchDir(), TEXT("vignette-pieces.json")));
		Candidates.Add(FPaths::Combine(
			FPaths::GetPath(FPlatformProcess::ExecutablePath()), TEXT("vignette-pieces.json")));
		for (const FString& C : Candidates)
		{
			const FString Full = FPaths::ConvertRelativePathToFull(C);
			OutTried.push_back(std::string(TCHAR_TO_UTF8(*Full)));
			if (FPaths::FileExists(C)) { return C; }
		}
		return FString();
	}

	// FINDS, LOADS AND PARSES THE SHARED STREET FILE, ONCE PER RUN. Both
	// entry points that need the street (the automation's Start() and the
	// interactive BuildInteractiveStreet() below) call this and fill the
	// same GSpec/GSpecPath/GSpecErr/GSpecTried globals either way, so a
	// reader asking "which file answered" gets one answer whichever entry
	// point ran. A run only ever takes one of the two paths, so nothing
	// here has to guard against being called twice.
	//
	// ON FAILURE, GSceneLine CARRIES THE REASON in the exact shape the
	// automation verdict already prints it, and the caller decides what to
	// do with a street that could not be read: the automation writes a
	// verdict and quits, the interactive path logs it and leaves the
	// player standing in whatever the level would otherwise be.
	bool LoadSpec()
	{
		// THE C NUMERIC LOCALE, SET BEFORE ANYTHING IS PARSED. Under a
		// comma-decimal locale strtod reads "1.5" as 1, and every coordinate
		// in this street would lose its fraction while every count stayed
		// green. The g++ test asserts the same thing on the same file.
		std::setlocale(LC_NUMERIC, "C");

		GSpecPath = FindSpec(GSpecTried);
		if (GSpecPath.IsEmpty())
		{
			// AND IT SAYS WHERE IT LOOKED, on the line a reader already has.
			GSceneLine = "sceneStatus=NOTHING-EMITTED piecesEmitted=0/0"
			             " sceneNote=piece-list-not-found-beside-the-binary-or-the-project"
			             " specTried=" + LedgerSurface::PathListValue(GSpecTried, 8);
			return false;
		}
		FString Contents;
		if (!FFileHelper::LoadFileToString(Contents, *GSpecPath))
		{
			GSceneLine = "sceneStatus=NOTHING-EMITTED piecesEmitted=0/0"
			             " sceneNote=piece-list-found-but-would-not-open specFrom="
			           + std::string(TCHAR_TO_UTF8(*NoSp(GSpecPath)));
			return false;
		}
		const std::string Text(TCHAR_TO_UTF8(*Contents));
		if (!ParseSpec(Text, GSpec, GSpecErr))
		{
			// A FILE THAT WILL NOT PARSE IS A DIFFERENT FACT FROM A FILE THAT
			// IS NOT THERE, and the reason is what says which.
			GSceneLine = "sceneStatus=NOTHING-EMITTED piecesEmitted=0/0 sceneNote="
			           + std::string(TCHAR_TO_UTF8(*NoSp(FString(UTF8_TO_TCHAR(GSpecErr.c_str())))))
			           + " specFrom=" + std::string(TCHAR_TO_UTF8(*NoSp(GSpecPath)));
			return false;
		}
		return true;
	}

	// GUARDS THE ONE CALLER THAT MATTERS: ALedgerGameMode::InitGame runs
	// once per process for a plain launch, and there is no reason for a
	// second call today, but a guard here costs one bool and stops the
	// street from ever being spawned twice if that ever changes.
	bool GInteractiveBuilt = false;

	UWorld* GameWorld()
	{
		if (!GEngine) { return nullptr; }
		for (const FWorldContext& Ctx : GEngine->GetWorldContexts())
		{
			if (Ctx.WorldType == EWorldType::Game && Ctx.World() != nullptr) { return Ctx.World(); }
		}
		return nullptr;
	}

	FLinearColor LinearFromGamma(double R, double G, double B)
	{
		// THE FILE STATES ITS COLOUR SPACE AND THIS ENGINE'S LIGHTS TAKE
		// LINEAR. The conversion is SrgbToLinear in the tested header, not a
		// pow(2.2) written here, and the verdict names both spaces.
		return FLinearColor((float)SrgbToLinear(R), (float)SrgbToLinear(G), (float)SrgbToLinear(B), 1.0f);
	}

	// ---- the street ----------------------------------------------------

	UStaticMesh* LoadShape(const TCHAR* Path)
	{
		return LoadObject<UStaticMesh>(nullptr, Path);
	}

	// ---- THE MESH PIECE KIND'S PATH CONTRACT -----------------------------
	//
	// tools/ue/import_prop_meshes.py writes one static mesh per held prop the
	// street names, at kPropPackageDir/kPropNamePrefix<asset>, and its
	// --selftest READS THESE TWO LITERALS OUT OF THIS FILE and compares them
	// to its own constants. That check runs in the container before any
	// dispatch, which is the only reason the two can be trusted to agree: a
	// path this file builds and nothing resolves returns null silently, the
	// piece falls back to a box, and the frame looks like a street with a
	// crate in it instead of a crate.
	const TCHAR* kPropPackageDir = TEXT("/Game/Ledger/Props");
	const TCHAR* kPropNamePrefix = TEXT("SM_");

	// The piece's own `asset` field and nothing else decides the path. A
	// hyphen is the one character an asset id may carry that a package name
	// may not, and the Python maps it the same way; every other illegal
	// character is refused by the importer BEFORE an asset is made, so a
	// piece naming one cannot have a uasset to find here.
	FString PropObjectPath(const std::string& AssetId)
	{
		FString Name = FString(kPropNamePrefix) + FString(UTF8_TO_TCHAR(AssetId.c_str()));
		Name.ReplaceInline(TEXT("-"), TEXT("_"));
		return FString(kPropPackageDir) + TEXT("/") + Name + TEXT(".") + Name;
	}

	// THE MESH, OR NULL, AND NULL IS A MEASUREMENT. Loading a cooked asset
	// that was never cooked is the likeliest failure on this route and it is
	// indistinguishable from a missing GLB unless the reason is carried out,
	// so the caller gets one and puts it on the verdict.
	UStaticMesh* LoadPropMesh(const std::string& AssetId, std::string& WhyNot)
	{
		if (AssetId.empty()) { WhyNot = "piece-names-no-asset"; return nullptr; }
		const FString Path = PropObjectPath(AssetId);
		UStaticMesh* M = LoadObject<UStaticMesh>(nullptr, *Path);
		if (M == nullptr)
		{
			// THE ASSET, NOT THE PATH. Four full object paths overran the
			// scene line's segment buffer, and snprintf truncates in
			// silence; propPackageDir and propNamePattern are on the same
			// line, so the path is derivable from this and shorter.
			WhyNot = "no-uasset-for-" + AssetId;
			return nullptr;
		}
		return M;
	}

	// WHAT THE LOADED ASSET SAYS ABOUT COLLISION. ASKED HERE, DECIDED IN THE
	// TESTED HEADER, amendment A5 of the ruling of 2026-09-08 (queue 161).
	//
	// WHAT THIS REPLACES AND WHY. PropCollisionPrims returned a COUNT of
	// aggregate elements, and a count reads 0 for two opposite facts: an
	// asset with no body setup under it, where nothing answered the question,
	// and an asset whose body setup holds zero simple elements, which a
	// complex-as-simple trace flag makes perfectly solid against a capsule.
	// The tally on the verdict then called both of them no collision. The
	// rule is now LedgerVignette::ReadPropCollision, which g++ runs in the
	// container over every case including the two nothing here can plant, and
	// this function does nothing but ask the engine the four questions it can
	// answer.
	//
	// THE IMPORTER READS THE SAME FOUR THINGS OFF A SAVED ASSET IN AN EDITOR
	// (tools/ue/import_prop_meshes.py collidable_word) and calls the
	// no-body-setup case NO rather than UNKNOWN. Different population, and
	// ruled UNKNOWN on this side because a null body setup at runtime is also
	// what a reader gets when nothing has built one yet. Written down in the
	// header beside the rule so the divergence reads as a decision.
	LedgerVignette::EPropCollisionRead PropCollisionOf(UStaticMesh* M)
	{
		if (M == nullptr) { return LedgerVignette::PropCollision_Unknown; }
		UBodySetup* BS = M->GetBodySetup();
		const bool bHasBody = (BS != nullptr);
		const int Elements = bHasBody ? BS->AggGeom.GetElementCount() : 0;
		const bool bComplexAsSimple =
			bHasBody && BS->CollisionTraceFlag == CTF_UseComplexAsSimple;
		// GEOMETRY UNDER THE FLAG, because complex-as-simple over an empty
		// mesh stops nothing. Read off the mesh's OWN bounds, which is the
		// same question the importer asks as boundsUu-nonzero and the same
		// call the pivot correction above already makes on this pointer.
		const FVector Extent = M->GetBounds().BoxExtent;
		const bool bGeometry = (Extent.X > 0.0 || Extent.Y > 0.0 || Extent.Z > 0.0);
		return LedgerVignette::ReadPropCollision(bHasBody, Elements, bComplexAsSimple,
		                                         bGeometry);
	}

	AStaticMeshActor* SpawnPiece(UWorld* World, UStaticMesh* Mesh, const Piece& P,
	                             const FVector& ScaleUU, bool bInteractive)
	{
		FActorSpawnParameters Params;
		Params.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
		AStaticMeshActor* A = World->SpawnActor<AStaticMeshActor>(
			AStaticMeshActor::StaticClass(), FVector::ZeroVector, FRotator::ZeroRotator, Params);
		if (A == nullptr) { return nullptr; }
		// A SPAWNED StaticMeshActor IS STATIC MOBILITY AND CANNOT BE MOVED,
		// and a scene lit only by movable lights needs movable geometry
		// anyway: a static actor with no built lighting renders unlit.
		// Setting this BEFORE the transform is not optional.
		MakeMovable(A);
		UStaticMeshComponent* C = A->GetStaticMeshComponent();
		if (C != nullptr)
		{
			C->SetMobility(EComponentMobility::Movable);
			C->SetStaticMesh(Mesh);
			// CreatePrimitive-style collision is not wanted in the timed
			// automation pass: 593 bodies cost simulation time in a frame
			// that pass is timing. A person walking this same street needs
			// exactly the opposite, or a Character's capsule falls straight
			// through a pavement with NoCollision on it and the whole
			// deliverable is a screen showing the sky forever. QueryOnly is
			// enough for a capsule sweep and costs nothing physics does.
			C->SetCollisionEnabled(bInteractive ? ECollisionEnabled::QueryOnly
			                                     : ECollisionEnabled::NoCollision);
			C->SetCastShadow(true);
		}
		A->SetActorScale3D(ScaleUU);
		A->SetActorLocationAndRotation(
			FVector(P.X * 100.0, P.Z * 100.0, P.Y * 100.0),
			FRotator((float)P.RollDeg, (float)P.YawDeg, (float)-P.PitchDeg));
#if WITH_EDITOR
		A->SetActorLabel(UTF8_TO_TCHAR(P.Name.c_str()));
#endif
		return A;
	}

	APointLight* SpawnPointLight(UWorld* World, const FVector& AtUU, const FLinearColor& Colour,
	                             float RangeM, float Intensity, bool bShadows)
	{
		FActorSpawnParameters Params;
		Params.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
		APointLight* L = World->SpawnActor<APointLight>(
			APointLight::StaticClass(), AtUU, FRotator::ZeroRotator, Params);
		if (L == nullptr) { return nullptr; }
		MakeMovable(L);
		UPointLightComponent* C = Cast<UPointLightComponent>(L->GetLightComponent());
		if (C != nullptr)
		{
			// UNITLESS RATHER THAN CANDELAS, so the file's Unity-shaped
			// number is at least the same kind of number. Named on the
			// verdict; not called equivalent.
			C->SetIntensityUnits(ELightUnits::Unitless);
			C->SetAttenuationRadius(RangeM * 100.0f);
			C->SetLightColor(Colour);
			C->SetIntensity(Intensity);
			C->SetCastShadows(bShadows);
		}
		return L;
	}

	// A6, 2026-09-09: THE ROTATION IS SET ON THE COMPONENT, NOT ONLY ON THE
	// ACTOR, AND THAT IS THE WHOLE BUG.
	//
	// Until this line existed, this function handed its FRotator to
	// SpawnActor as the ACTOR rotation and then touched only SetCastShadows
	// and SetIntensity. A directional light's direction is the forward axis
	// of its LIGHT COMPONENT's world transform, which is also what
	// GetComponentRotation reads back on the verdict, so whatever relative
	// rotation the component carried was composed on top of the ask. The spec
	// asked for a sun 36 degrees above the horizon (asked pitch -36.0) and
	// every run of this rig rendered -82.0, with the yaw agreeing to the
	// decimal: a constant pitch displacement and nothing else.
	//
	// IT DOES NOT MATTER WHAT THE COMPONENT WAS CARRYING, and that is the
	// point of writing it this way. -46 degrees of component relative pitch
	// is a plausible mechanism and NOBODY HAS CONFIRMED it is Unreal's
	// shipped default, so nothing here subtracts 46 or assumes a default:
	// SetWorldRotation states the world rotation absolutely, so the asked
	// value arrives whatever the relative rotation was. The light is made
	// movable first, one line up, because a static component refuses a
	// transform write.
	//
	// AND IT IS MEASURED RATHER THAN TRUSTED: the caller records the asked
	// pair, MeasureLightAim reads the component back, and lightAimStatus on
	// the verdict refuses the run if the two disagree by a degree or more.
	ADirectionalLight* SpawnDirectional(UWorld* World, const FRotator& Rot, bool bShadows)
	{
		FActorSpawnParameters Params;
		Params.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
		ADirectionalLight* L = World->SpawnActor<ADirectionalLight>(
			ADirectionalLight::StaticClass(), FVector(0, 0, 3000), Rot, Params);
		if (L == nullptr) { return nullptr; }
		MakeMovable(L);
		if (ULightComponent* C = L->GetLightComponent())
		{
			C->SetWorldRotation(Rot);
			C->SetCastShadows(bShadows);
			C->SetIntensity(0.0f);
		}
		return L;
	}

	void SetDirectional(ADirectionalLight* L, const FLinearColor& Colour, float Intensity)
	{
		if (L == nullptr) { return; }
		if (ULightComponent* C = L->GetLightComponent())
		{
			C->SetLightColor(Colour);
			C->SetIntensity(Intensity);
		}
	}

	// BUILD THE WHOLE STREET ONCE. Every count is captured as it happens and
	// the denominator comes off the FILE, before any spawning, so a run that
	// dies halfway still prints what it was asked for.
	//
	// bInteractive IS NAMED AT EVERY CALL SITE, NEVER DEFAULTED: it turns
	// collision on for every spawned piece and skips the materials-test
	// control quads, both of which are wrong to add to a frame the
	// automation is timing and both of which are required for a person to
	// walk here at all. The automation's own call (Tick's WaitWorld case)
	// passes false; ALedgerGameMode's (LedgerVignetteShot::BuildInteractiveStreet,
	// this file) passes true.
	void BuildScene(UWorld* World, bool bInteractive)
	{
		int Boxes = 0, Cyls = 0, Planes = 0, Props = 0, Decals = 0, Skipped = 0, Emitted = 0;
		std::string Note = "none";

		// ---- THE MESH PIECE KIND'S OWN INSTRUMENT ------------------------
		// Props counts every mesh-kind piece that got an actor of any sort;
		// Meshes counts the ones that got a LOADED PROP MESH, and StandIns
		// the ones that fell back to a box. Meshes + StandIns == Props is the
		// identity the verdict can be checked against, and StandIns is what
		// now goes to SceneLine's propStandIns, whose denominator is the mesh
		// piece count: 0/23 means every prop is real, 23/23 means the import
		// step never ran.
		int Meshes = 0, StandIns = 0;
		// THE COLLISION TALLY AND ITS NAMES, KEPT BY THE TESTED HEADER. Its
		// denominator is Placed(), the readings actually taken, never the 23
		// the file asked for: a denominator larger than the set examined
		// turns a clean result into a false claim with a number on it.
		LedgerVignette::PropCollisionTally CollisionTally;
		// WHICH PROP NAMES GOT A REAL ASSET, so the burial reading below can
		// say whether a row's bounds came from the loaded mesh or from the
		// box stand-in. At most one entry per mesh piece.
		std::vector<std::string> FromAssetNames;
		// AND THE NAMED SUBJECT'S OWN READING, CAPTURED AT THE INSTANT IT WAS
		// ASKED. A6's subject is one piece, and the run's tally of twenty-three
		// cannot answer a question about one of them. The default says there
		// was no asset to ask rather than printing a word that would read as
		// a measurement of the box stand-in.
		std::string SubjectCollision = "no-asset-to-read";
		// PLACEMENT, MEASURED AGAINST THE BOX IT REPLACED, AT WORST over the
		// placed meshes with the piece it was worst ON captured at the same
		// instant. Two halves, because they answer different questions and
		// only one of them survives rotation:
		//   Centre: how far the placed mesh's WORLD bounds centre is from the
		//           x_m/y_m/z_m the file named. Valid at every rotation,
		//           because rotating about the bounds centre leaves the
		//           centre where it was, and it is the number the contract in
		//           vignette-scene.json's held_props.pivot_note is about.
		//   Size:   whether the loaded mesh is the size the spec box was.
		//           ONLY COMPARABLE on an axis-aligned piece: a world AABB
		//           around a mesh yawed 20 degrees is legitimately bigger
		//           than the box, so the comparable count ships its own
		//           denominator rather than letting two of twenty-three
		//           rotated props read as a size fault.
		double WorstCentreMm = 0.0, WorstSizeMm = 0.0;
		std::string WorstCentreOn = "nothing-measured";
		std::string WorstSizeOn = "nothing-measured";
		int SizeComparable = 0;
		// WHY A PIECE FELL BACK, capped, and the cap announces itself.
		std::vector<std::string> FellBack;

		UStaticMesh* Cube  = LoadShape(TEXT("/Engine/BasicShapes/Cube.Cube"));
		UStaticMesh* Cyl   = LoadShape(TEXT("/Engine/BasicShapes/Cylinder.Cylinder"));
		UStaticMesh* Plane = LoadShape(TEXT("/Engine/BasicShapes/Plane.Plane"));
		// A MISSING BASIC SHAPE IS THE ONE FAILURE THAT WOULD LOOK LIKE AN
		// EMPTY STREET AND HAS NOTHING TO DO WITH THE STREET. The engine's
		// basic shapes are only in a packaged build because DefaultGame.ini
		// asks for the directory to be cooked; if that is undone, this says
		// which mesh was missing rather than reporting 0 of 593 pieces.
		if (Cube == nullptr || Cyl == nullptr || Plane == nullptr)
		{
			Note = std::string("basic-shape-missing/cube=") + (Cube ? "yes" : "NO")
			     + "/cylinder=" + (Cyl ? "yes" : "NO") + "/plane=" + (Plane ? "yes" : "NO")
			     + "/is-Engine-BasicShapes-in-DirectoriesToAlwaysCook";
		}

		for (size_t I = 0; I < GSpec.Pieces.size(); ++I)
		{
			const Piece& P = GSpec.Pieces[I];
			// SIZES ARE FULL SIZES IN METRES AND THE ENGINE'S BASIC SHAPES
			// ARE ONE METRE, so the scale IS the size. That is a fact about
			// the meshes, and it is asserted rather than assumed: a cube of
			// 100 uu scaled by sx_m is sx_m metres across only while the
			// mesh is 100 uu, and the verdict's placement instrument is what
			// would catch it if the engine ever changed them.
			const FVector Scale((float)P.SX, (float)P.SZ, (float)P.SY);
			AStaticMeshActor* A = nullptr;
			if (P.Shape == "box") { A = SpawnPiece(World, Cube, P, Scale, bInteractive); if (A) ++Boxes; }
			else if (P.Shape == "cyl")
			{
				// THE CYLINDER'S AXIS IS LOCAL +y IN THE FILE'S FRAME, which
				// under this mapping is local +Z, and that is this engine's
				// cylinder's own axis. Height is sy_m and the diameter is
				// sx_m and sz_m, so the same scale vector is correct for
				// both shapes and no special case is needed.
				A = SpawnPiece(World, Cyl, P, Scale, bInteractive); if (A) ++Cyls;
			}
			else if (P.Shape == "decal")
			{
				// A DECAL IS A QUAD UNTIL PHASE C. sz_m is zero and the
				// engine's plane is 100 uu square in its local XY with the
				// normal on +Z; the file says the quad is sx_m by sy_m with
				// its normal on -z before rotation, so the plane is turned
				// to face -z and scaled in the two axes that are left.
				Piece Q = P;
				// TURNING THE PLANE ONTO THE FILE'S FACING, AND THE SIGN IS
				// THE WHOLE OF IT. The engine's plane spans its local X and
				// Y with the normal on local +Z, which under this mapping is
				// the file's local +y. The file says the quad is sx_m by
				// sy_m with its normal on -z before rotation. A quarter turn
				// about the file's x takes +y onto -z, and the file's pitch
				// is exactly that turn, so the pitch goes DOWN by 90 and not
				// up: up by 90 lands the normal on +z, which is the same
				// plane facing backwards, and an untextured quad facing away
				// is culled or lit from behind. The in-plane axes come out
				// right either way, which is why the sign would not show in
				// a count.
				Q.PitchDeg = P.PitchDeg - 90.0;
				const FVector QScale((float)P.SX, (float)P.SY, 1.0f);
				A = SpawnPiece(World, Plane, Q, QScale, bInteractive);
				if (A)
				{
					// A CO-PLANAR QUAD Z-FIGHTS WITH THE SURFACE UNDER IT,
					// and this is the emitter's decision rather than the
					// file's, so it is a named constant and it is printed.
					// The file puts a ground decal at the ground level
					// because it is describing a decal, and this engine has
					// no decal here yet: Phase C replaces the quad with a
					// real deferred decal and this lift goes with it.
					A->AddActorWorldOffset(
						A->GetActorRotation().RotateVector(FVector(0.0f, 0.0f, 1.0f)) * kDecalLiftCm);
					++Planes; ++Decals;
				}
			}
			else if (P.Shape == "mesh")
			{
				// THE MESH PIECE KIND, WHICH IS A REAL MESH WHEN THE IMPORT
				// STEP RAN AND THE BOX STAND-IN WHEN IT DID NOT.
				//
				// The GLBs under ledger/Assets/Props/base-mesh become uassets
				// in a build step, by tools/ue/import_prop_meshes.py, never by
				// a human in an editor. This engine still has no runtime
				// importer and does not need one: the piece names an asset,
				// the path is derived from that name alone, and a path that
				// resolves to nothing falls back to the box this branch used
				// to always spawn, COUNTED AND NAMED, so a missing import can
				// never read as a loaded model.
				std::string WhyNot;
				UStaticMesh* PropMesh = LoadPropMesh(P.Asset, WhyNot);
				if (PropMesh != nullptr)
				{
					// SCALE 1, AND NEVER ANYTHING ELSE. The dims policy in
					// production/specs/vignette-scene.json forbids inventing a
					// size, and tools/ue/import_prop_meshes.py --selftest has
					// MEASURED that each spec box is its GLB's own dimensions
					// (worst 0.0000 mm over 16 assets): so the mesh is already
					// the size the street drew, and passing Scale here would
					// square it.
					A = SpawnPiece(World, PropMesh, P, FVector(1.0f, 1.0f, 1.0f), bInteractive);
					if (A != nullptr)
					{
						// THE PIVOT CORRECTION, FROM THE ENGINE'S OWN READING
						// OF THE MESH AND NOT FROM A CONVENTION. The file
						// names where the prop's BOUNDING BOX CENTRE goes;
						// the source pivots are measured to be all over the
						// place (awning_02's origin is at its top-back,
						// the posters are centred, drainage_grate_01 hangs
						// 15 mm below its origin, the rest stand on it), so
						// the correction is the mesh's own local bounds
						// centre, which the engine hands back, rotated into
						// the actor's frame the same way the decal lift above
						// is. Scale is 1 here, which is the only reason this
						// offset needs no scale term.
						const FVector LocalCentre = PropMesh->GetBounds().Origin;
						A->AddActorWorldOffset(
							A->GetActorRotation().RotateVector(-LocalCentre));

						// READ BACK WHERE IT LANDED. 1 uu is 1 cm, so uu * 10
						// is mm.
						FVector WOrg(0, 0, 0), WExt(0, 0, 0);
						A->GetActorBounds(false, WOrg, WExt);
						const FVector WantUU(P.X * 100.0, P.Z * 100.0, P.Y * 100.0);
						const double CentreMm = (WOrg - WantUU).Size() * 10.0;
						if (CentreMm > WorstCentreMm || WorstCentreOn == "nothing-measured")
						{
							WorstCentreMm = CentreMm;
							WorstCentreOn = NoSpaces(P.Name);
						}

						// THE SIZE HALF, ON AXIS-ALIGNED PIECES ONLY.
						const double AbsYaw = P.YawDeg < 0 ? -P.YawDeg : P.YawDeg;
						const bool bQuarter = (AbsYaw > 89.0 && AbsYaw < 91.0)
						                   || (AbsYaw > 269.0 && AbsYaw < 271.0);
						const bool bHalf = (AbsYaw < 1.0) || (AbsYaw > 179.0 && AbsYaw < 181.0)
						                || (AbsYaw > 359.0);
						if (P.PitchDeg == 0.0 && P.RollDeg == 0.0 && (bQuarter || bHalf))
						{
							double WantX = P.SX * 100.0, WantY = P.SZ * 100.0;
							const double WantZ = P.SY * 100.0;
							if (bQuarter) { const double T = WantX; WantX = WantY; WantY = T; }
							const double DX = (WExt.X * 2.0 - WantX) * 10.0;
							const double DY = (WExt.Y * 2.0 - WantY) * 10.0;
							const double DZ = (WExt.Z * 2.0 - WantZ) * 10.0;
							double Worst = DX < 0 ? -DX : DX;
							const double AY = DY < 0 ? -DY : DY;
							const double AZ = DZ < 0 ? -DZ : DZ;
							if (AY > Worst) { Worst = AY; }
							if (AZ > Worst) { Worst = AZ; }
							++SizeComparable;
							if (Worst > WorstSizeMm || WorstSizeOn == "nothing-measured")
							{
								WorstSizeMm = Worst;
								WorstSizeOn = NoSpaces(P.Name);
							}
						}

						// COLLISION, READ OFF THE ASSET RATHER THAN TRUSTED
						// FROM THE IMPORT STEP'S OWN VERDICT, AND
						// THREE-VALUED: YES, NO, or UNKNOWN for an asset that
						// answered nothing. The tally and the string are the
						// tested header's.
						const LedgerVignette::EPropCollisionRead Read =
							PropCollisionOf(PropMesh);
						CollisionTally.Add(P.Name, Read);
						FromAssetNames.push_back(P.Name);
						if (P.Name == LedgerVignette::BurialSubjectName())
						{
							SubjectCollision = LedgerVignette::PropCollisionWord(Read);
						}

						++Meshes; ++Props;
					}
					else
					{
						WhyNot = "spawn-refused";
					}
				}
				if (A == nullptr)
				{
					// THE BOX STAND-IN, UNCHANGED, AND STILL THE RIGHT
					// FALLBACK. A box of the prop's OWN stated size holds the
					// space so the frame stays comparable to the Unity pair.
					A = SpawnPiece(World, Cube, P, Scale, bInteractive);
					if (A != nullptr)
					{
						++Boxes; ++Props; ++StandIns;
						if (FellBack.size() < 4)
						{
							FellBack.push_back(NoSpaces(P.Name) + "=" + NoSpaces(WhyNot));
						}
					}
				}
			}
			else
			{
				// A SHAPE THIS EMITTER DOES NOT KNOW IS COUNTED, NOT
				// IGNORED. The g++ test asserts the file contains none, so
				// reaching this is a schema change nobody told the emitter
				// about.
				++Skipped;
				continue;
			}
			if (A == nullptr) { ++Skipped; continue; }
			++Emitted;
			GByName.Add(FString(UTF8_TO_TCHAR(P.Name.c_str())), A);
		}

		// H4: A POINT LIGHT UNDER EVERY EMISSIVE PIECE, which is what the
		// file's lantern block says in as many words: one point light 0.05 m
		// below the centre of each emissive piece.
		const FLinearColor Lamp = LinearFromGamma(GSpec.Lantern.R, GSpec.Lantern.G, GSpec.Lantern.B);
		for (size_t I = 0; I < GSpec.Pieces.size(); ++I)
		{
			const Piece& P = GSpec.Pieces[I];
			if (!P.Emissive) { continue; }
			APointLight* L = SpawnPointLight(
				World, FVector(P.X * 100.0, P.Z * 100.0, (P.Y - 0.05) * 100.0),
				Lamp, (float)GSpec.Lantern.RangeM,
				(float)GSpec.Lantern.Intensity * kLampGainUnitless, true);
			if (L != nullptr)
			{
				GLanterns.Add(L);
				GLanternNames.push_back(NoSpaces(P.Name));
			}
		}

		// H5: THE WINDOW PRACTICALS, AT THE NAMES THE FILE LISTS AND NOWHERE
		// ELSE. Not "every piece whose name contains _interior": that rule is
		// what the Unity host had, and by 2 September it also matched three
		// decal cards. The file resolves lit_bays to names in Core and both
		// engines light the names.
		const FLinearColor Warm = LinearFromGamma(GSpec.Windows.R, GSpec.Windows.G, GSpec.Windows.B);
		int WindowsUnplaced = 0;
		for (size_t I = 0; I < GSpec.Windows.LitNames.size(); ++I)
		{
			AStaticMeshActor** Found = GByName.Find(FString(UTF8_TO_TCHAR(GSpec.Windows.LitNames[I].c_str())));
			if (Found == nullptr || *Found == nullptr) { ++WindowsUnplaced; continue; }
			const FVector At = (*Found)->GetActorLocation() + FVector(0, 0, 40.0f);
			APointLight* L = SpawnPointLight(World, At, Warm,
				(float)GSpec.Windows.ShopRangeM,
				(float)GSpec.Windows.ShopIntensity * kLampGainUnitless, false);
			if (L != nullptr)
			{
				GWindows.Add(L);
				GWindowNames.push_back(NoSpaces(GSpec.Windows.LitNames[I]));
			}
			else { ++WindowsUnplaced; }
		}
		if (WindowsUnplaced > 0)
		{
			// APPENDED, NOT ASSIGNED. A missing basic shape and an unplaced
			// practical are two findings and the second must not erase the
			// first, which is the one that explains an empty street.
			if (Note == "none") { Note.clear(); } else { Note += "/"; }
			Note += "practicals-unplaced=" + std::to_string(WindowsUnplaced)
			      + "-of-" + std::to_string((int)GSpec.Windows.LitNames.size());
		}
		if (Note.empty()) { Note = "none"; }

		// THE SUN, THE FILL AND THE FOG, SPAWNED HERE AND WRITTEN ONLY BY
		// ApplyCondition. One owner per global.
		//
		// A6: EVERY ASK IS RECORDED BESIDE THE SPAWN THAT CARRIED IT. The
		// three fills go through the same helper as the sun, so the same
		// displacement applied to all four and the comment claiming a fill
		// points at (-80/20) was a decayed claim on every run the key has
		// existed. They are retired to zero intensity by ApplyCondition when
		// the sky is whole, so no pixel of today's frames depends on them;
		// printing their rotations is what retires the claim rather than
		// repeating it.
		const FRotator SunRot((float)SunPitchDeg(GSpec.SunElevationDeg),
		                      (float)SunYawDeg(GSpec.SunAzimuthDeg), 0.0f);
		const FRotator FillARot(-80.0f,  20.0f, 0.0f);
		const FRotator FillBRot(-10.0f, 200.0f, 0.0f);
		const FRotator FillCRot( 60.0f,  90.0f, 0.0f);
		GSun   = SpawnDirectional(World, SunRot,   true);
		GFillA = SpawnDirectional(World, FillARot, false);
		GFillB = SpawnDirectional(World, FillBRot, false);
		GFillC = SpawnDirectional(World, FillCRot, false);
		GLightAsked.clear();
		RecordAsked("sun",   GSun,   SunRot);
		RecordAsked("fillA", GFillA, FillARot);
		RecordAsked("fillB", GFillB, FillBRot);
		RecordAsked("fillC", GFillC, FillCRot);
		{
			FActorSpawnParameters Params;
			Params.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
			GFog = World->SpawnActor<AExponentialHeightFog>(
				AExponentialHeightFog::StaticClass(), FVector(0, 0, 0), FRotator::ZeroRotator, Params);
			MakeMovable(GFog);
			// QUEUE 186: THE SKY, SPAWNED HERE AND WRITTEN ONLY BY
			// ApplyCondition, exactly as the fog above it is.
			//
			// ORDER MATTERS AND IS NOT COSMETIC: the atmosphere is the thing
			// the sky light captures, so it exists first. A sky light that
			// captures before there is anything to capture holds a black
			// cubemap, which is the exact failure the fill-light constant
			// block above named ("it cannot come back black the way a sky
			// light with nothing to capture can") before any of this existed.
			GAtmosphere = World->SpawnActor<ASkyAtmosphere>(
				ASkyAtmosphere::StaticClass(), FVector(0, 0, 0), FRotator::ZeroRotator, Params);
			MakeMovable(GAtmosphere);
			GSky = World->SpawnActor<ASkyLight>(
				ASkyLight::StaticClass(), FVector(0, 0, 300), FRotator::ZeroRotator, Params);
			MakeMovable(GSky);
			// FOUND BY COMPONENT CLASS, NOT BY THE ACTOR'S NAMED GETTER,
			// which is the rule this file already follows for the fog and
			// for the same reason: a named accessor has been renamed across
			// engine versions and this container cannot compile one line of
			// this file to find out.
			if (GSky != nullptr)
			{
				if (USkyLightComponent* SC = GSky->FindComponentByClass<USkyLightComponent>())
				{
					// CAPTURED SCENE, IN REAL TIME. The thing that is SEEN
					// and the thing that is REFLECTED are then the same
					// object, which is the whole reason this is not an HDRI
					// ambient standing behind an unrelated backdrop.
					SC->SourceType = ESkyLightSourceType::SLS_CapturedScene;
					SC->bRealTimeCapture = true;
					SC->SetIntensity(0.0f);
					SC->MarkRenderStateDirty();
				}
			}
		}

		// StandIns, NOT Props, IS WHAT propStandIns MEANS. Its denominator in
		// SceneLine is the mesh piece count, so 0/23 reads "every prop is a
		// real mesh" and 23/23 reads "the import step did not reach this
		// build". Passing Props here, as this call did while every mesh piece
		// was a box, would have made those two indistinguishable the moment
		// one prop became real.
		GSceneLine = SceneLine(GSpec, Emitted, Boxes, Cyls, Planes, StandIns, Decals,
		                       GLanterns.Num(), GWindows.Num(), Skipped, Note);

		// ---- THE MESH ROUTE'S OWN SEGMENT, APPENDED --------------------
		// Appended rather than folded into SceneLine because SceneLine is the
		// tested header's shared shape and both engines read it; these keys
		// are this engine's mesh route and nothing in Unity has them.
		//
		// NOT ONE NUMBER AND NOT ONE CHARACTER OF THIS STRING IS DECIDED
		// HERE, amendment A5 of the ruling of 2026-09-08. The tally, the
		// arithmetic and the formatting are LedgerVignette::PropMeshSegment,
		// which g++ compiles and RUNS in the container before any dispatch;
		// this block supplies membership, order and live state. The version
		// this replaces built its own string in this file, which nothing here
		// can compile, and shipped three faults in one eight-line stretch for
		// three landed runs.
		{
			// THE PLACED BOUNDS OF EVERY PIECE, READ BACK OFF THE ENGINE AND
			// NEVER RECOMPUTED FROM THE FILE. This is the half of the
			// placement metric propCentreWorstMm cannot see: a piece sits
			// 0.00 mm from where the file put it and is still inside the
			// road. GByName holds exactly the actors this BuildScene spawned,
			// so the population is the street's own pieces and nothing the
			// crime probe added to its separate map.
			std::vector<LedgerVignette::PlacedBox> Placed;
			Placed.reserve(GSpec.Pieces.size());
			for (size_t I = 0; I < GSpec.Pieces.size(); ++I)
			{
				const Piece& P = GSpec.Pieces[I];
				AStaticMeshActor** Found =
					GByName.Find(FString(UTF8_TO_TCHAR(P.Name.c_str())));
				if (Found == nullptr || *Found == nullptr) { continue; }
				FVector WOrg(0, 0, 0), WExt(0, 0, 0);
				(*Found)->GetActorBounds(false, WOrg, WExt);
				LedgerVignette::PlacedBox B;
				B.Name = P.Name; B.Edge = P.Edge; B.Region = P.Region;
				B.bProp = (P.Shape == "mesh");
				for (size_t K = 0; K < FromAssetNames.size(); ++K)
				{
					if (FromAssetNames[K] == P.Name) { B.bFromAsset = true; break; }
				}
				// BACK INTO THE FILE'S FRAME AND INTO METRES, which is the
				// only frame the tested header knows and the frame every
				// number in vignette-pieces.json is in: (X,Y,Z) uu is
				// (x,z,y) m, so the engine's Z is the file's y and 1 uu is
				// 1 cm. Inverting the one conversion this file does at spawn,
				// rather than carrying a second convention into the header.
				B.MinX = (WOrg.X - WExt.X) / 100.0; B.MaxX = (WOrg.X + WExt.X) / 100.0;
				B.MinY = (WOrg.Z - WExt.Z) / 100.0; B.MaxY = (WOrg.Z + WExt.Z) / 100.0;
				B.MinZ = (WOrg.Y - WExt.Y) / 100.0; B.MaxZ = (WOrg.Y + WExt.Y) / 100.0;
				Placed.push_back(B);
			}
			LedgerVignette::PropSegmentIn Seg;
			Seg.MeshPiecesInFile = ShapeCount(GSpec.Pieces, "mesh");
			Seg.PlacedAsMesh = Meshes;
			Seg.PlacedAsBox = StandIns;
			Seg.FellBackOn = FellBack;
			Seg.PackageDir = TCHAR_TO_UTF8(kPropPackageDir);
			Seg.NamePrefix = TCHAR_TO_UTF8(kPropNamePrefix);
			Seg.CentreWorstMm = WorstCentreMm;
			Seg.CentreWorstOn = WorstCentreOn;
			Seg.SizeWorstMm = WorstSizeMm;
			Seg.SizeWorstOn = WorstSizeOn;
			Seg.SizeComparable = SizeComparable;
			Seg.Collision = CollisionTally;
			Seg.SubjectCollision = SubjectCollision;
			Seg.Burials = LedgerVignette::ReadBurials(Placed);
			Seg.bInteractive = bInteractive;
			GSceneLine += " ";
			GSceneLine += LedgerVignette::PropMeshSegment(Seg);
		}
		// THE SPAWNS THAT ARE NOT PIECES, READ BACK RATHER THAN ASSUMED. A
		// null here is why a frame would be black, and it is a different
		// fault from an empty street.
		// `sun=` USED TO BE PRINTED HERE AND IS NOT ANY MORE, QUEUE 205.
		// It said a directional light had been SPAWNED and nothing about
		// what that light is, and it is now one key of five that
		// LedgerVignette::SunSegment prints off the live component. Two
		// producers for one key on one line would make the reader's answer
		// depend on which token it split first.
		char Buf[640];
		// QUEUE 333: lampEmissive RIDES HERE BESIDE lampGain, which is the
		// other unmeasured lamp number, so the two first-values-of-a-series
		// are read together. ITS KEY IS NOT lampColourSpace: that key is
		// already produced by LedgerVignette::SceneLine off the file's own
		// stated space, and two producers for one key on one line would make
		// a reader's answer depend on which token it split first, which is
		// the fault that retired `sun=` from this same snprintf in queue 205.
		const int SceneNeeded = std::snprintf(Buf, sizeof(Buf),
			" fill=%d/3 fog=%s"
			" lampGain=%.2f fogGain=%.2f"
			" lampEmissive=%.2f/unitless/first-value-of-a-series/never-measured"
			" lampEmissiveSpace=lantern-gamma>linear/gain-applied-after-the-conversion"
			" lightUnits=unitless/not-candelas decalLiftCm=%.1f decalModel=quad/phase-C-owns-the-decal",
			(GFillA ? 1 : 0) + (GFillB ? 1 : 0) + (GFillC ? 1 : 0),
			GFog ? "yes" : "SPAWN-FAILED",
			kLampGainUnitless, kFogDensityGain,
			kLampEmissiveUnitless, kDecalLiftCm);
		GSceneLine += Buf;
		// AND THE CAP ANNOUNCES ITSELF, instruments.md. snprintf truncates in
		// silence and a cut tail reads exactly like a key that was never
		// emitted, which is what this segment looked like before it grew.
		if (SceneNeeded < 0 || (size_t)SceneNeeded >= sizeof(Buf))
		{
			GSceneLine += " sceneTailCut=yes/at-640-chars";
		}
		// ---- QUEUE 186: LOOK FOR THE HDRI THE SHARED FILE NAMES --------
		//
		// Done here, once, while the spec is loaded, and NOT bound to
		// anything. The reading rides the sky segment, which is taken when
		// the line is READ rather than now: see SkySegmentNow below.
		LookForNamedHdri();
		// AND BIND IT. The look is the reading and the build is the work; they
		// are two calls so that a run which finds the file and cannot use it
		// still prints where the file was.
		BuildSkyDome(World);
		// PHASE C, AFTER EVERY PIECE IS SPAWNED AND NAMED. It reads GByName,
		// so it cannot run before the pieces are in it.
		BindSurfaces();
		// AND THE CONTROLS AFTER IT, because they instance the base material
		// BindSurfaces loads. A control quad in front of the camera is not a
		// piece and is not counted as one: the scene line's denominators come
		// off the file and none of them moves.
		//
		// SKIPPED FOR A PERSON WALKING HERE. The three colour-swatch planes
		// exist only to prove a material instance can be told apart from the
		// street around it in a photograph; standing them in front of the
		// player's own spawn point would be the first thing anyone sees, and
		// it answers a materials question nobody playing is asking.
		if (!bInteractive)
		{
			SpawnControlQuads(World, Plane);
		}
		else
		{
			GQuadDone = "controlQuadsStatus=SKIPPED controlQuads=nothing-measured"
			            " controlQuadsNote=interactive-build-does-not-spawn-the-materials-test-quads";
		}
	}

	const Camera* FindCamera(const std::string& Id)
	{
		for (size_t I = 0; I < GSpec.Cameras.size(); ++I)
			if (GSpec.Cameras[I].Id == Id) return &GSpec.Cameras[I];
		return nullptr;
	}

	const Condition* FindCondition(const std::string& Id)
	{
		for (size_t I = 0; I < GSpec.Conditions.size(); ++I)
			if (GSpec.Conditions[I].Id == Id) return &GSpec.Conditions[I];
		return nullptr;
	}

	// IS THE SKY STRUCTURALLY THERE. Both actors and both components, asked
	// at the moment of the question and never remembered from the spawn: a
	// sky light with no atmosphere captures a black scene, and the two
	// halves fail independently.
	bool SkyIsWhole()
	{
		if (GSky == nullptr || GAtmosphere == nullptr) { return false; }
		return GSky->FindComponentByClass<USkyLightComponent>() != nullptr
		    && GAtmosphere->FindComponentByClass<USkyAtmosphereComponent>() != nullptr;
	}

	// ---- QUEUE 309: THE WETNESS, RE-DRIVEN ON THE INSTANCES THE SCENE
	// ALREADY KEEPS -------------------------------------------------------
	//
	// RULED 2026-09-15 07:55Z: NO NEW GLOBAL AND NO SECOND LIST. Queue 186
	// bound one wetness for the whole run because nothing kept the material
	// instances it made. The scene DOES keep them: every piece actor holds a
	// static mesh component and BindSurfaces called Comp->SetMaterial(0, Mid)
	// on it, which run ce99814 proved by asking rather than by assuming
	// (compMaterialIsMid=is-the-instance-we-made on every reached line). So
	// this is the owner, the list is the scene, and no second one exists.
	//
	// WHY THE WALK IS OVER GSpec.Pieces AND NOT OVER GByName'S KEYS, which
	// is the one place this departs from the ruling's wording and is worth a
	// reader's minute. The ruling says "walk GByName". GByName maps a piece
	// NAME to an actor and carries no surface, and WetBindFor's membership
	// test is IsGroundSurface(surface): a walk over the map alone cannot ask
	// the question. This walks the shared file's pieces, which is where the
	// surface is, and resolves each one through GByName.Find, which is the
	// idiom BindSurfaces itself uses at its piece loop and the lit-window
	// pass uses before it. Nothing is stored, nothing is listed, and the
	// membership is still IsGroundSurface via the same two tested functions.
	//
	// WHAT THIS FILE DECIDES: nothing. Whether a walk happens at all
	// (WetRedriveNeeded), which pieces may be touched (WetRedriveTouches),
	// what each parameter becomes (WetBindFor, WetGradeFor) and every printed
	// string are in SurfaceBind.h, which g++ compiles and runs before any
	// dispatch. This supplies the walk and live state only.
	void ReDriveWetness(const Condition& C)
	{
		LedgerSurface::WetRedriveAsked(GWetRedrive);
		const double Want = LedgerSurface::WetClamp01(C.Wetness);
		// THE WRITE-ON-CHANGE GUARD, AND IT IS HERE FOR A MEASURED REASON
		// rather than a feared one: this function's caller is re-entered on
		// EVERY tick while a condition settles, so a naive re-drive is one
		// parameter write per piece per tick over 593 pieces. The sky in
		// ApplyCondition below carries the same guard for the same reason.
		// Both counters ride the materials done line, so nobody has to take
		// this comment's word for it.
		if (!LedgerSurface::WetRedriveNeeded(GWetRedrive, Want))
		{
			LedgerSurface::WetRedriveSkipped(GWetRedrive);
			return;
		}
		LedgerSurface::WetRedriveWalked(GWetRedrive, Want, C.Id);
		// ONE READBACK PER SURFACE PER WALK, WHICH IS THE BIND'S OWN RULE.
		// A flag per surface and not per piece: 593 pieces would answer one
		// question about the material 593 times. This is
		// a local of this walk and not a kept list; it is sized by the bind
		// records, which exist either way.
		std::vector<bool> ReadTaken(GBinds.size(), false);
		bool bRunReadTaken = false;
		for (size_t P = 0; P < GSpec.Pieces.size(); ++P)
		{
			const Piece& Pc = GSpec.Pieces[P];
			int32 Idx = -1;
			for (size_t I = 0; I < GBinds.size(); ++I)
			{
				if (GBinds[I].Surface == Pc.Surface) { Idx = (int32)I; break; }
			}
			if (Idx < 0)
			{
				LedgerSurface::WetRedriveVisit(GWetRedrive, LedgerSurface::WetRedrive_NoBind);
				continue;
			}
			// THE SAME DECISION THE BIND MADE, RE-RUN FROM THE SAME THREE
			// INPUTS rather than remembered. A decal card's instance is real
			// and carries neither of these two parameters on purpose, so a
			// walk that wrote to every MID it found would put an AlbedoGrade
			// on ten shop signs and ten posters in the judged frame.
			const LedgerSurface::EPaintRoute Route = LedgerSurface::RouteFor(
				Pc.Surface, Pc.Shape == "decal",
				LedgerSurface::IsResolved(GBinds[(size_t)Idx]));
			if (!LedgerSurface::WetRedriveTouches(Route))
			{
				LedgerSurface::WetRedriveVisit(GWetRedrive, LedgerSurface::WetRedrive_NotOurRoute);
				continue;
			}
			AStaticMeshActor** Found = GByName.Find(FString(UTF8_TO_TCHAR(Pc.Name.c_str())));
			if (Found == nullptr || *Found == nullptr)
			{
				LedgerSurface::WetRedriveVisit(GWetRedrive, LedgerSurface::WetRedrive_NoActor);
				continue;
			}
			UStaticMeshComponent* Comp = (*Found)->GetStaticMeshComponent();
			if (Comp == nullptr)
			{
				LedgerSurface::WetRedriveVisit(GWetRedrive, LedgerSurface::WetRedrive_NoComponent);
				continue;
			}
			// THE INSTANCE, OFF THE COMPONENT, AND THE CAST IS THE WHOLE
			// TEST. A component still wearing the parent material answers
			// with a UMaterialInterface that is not a dynamic instance, and
			// setting a parameter on that is a write to the asset rather than
			// to this piece. Cast returning null is counted and named, never
			// worked around.
			UMaterialInstanceDynamic* Mid =
				Cast<UMaterialInstanceDynamic>(Comp->GetMaterial(0));
			if (Mid == nullptr)
			{
				LedgerSurface::WetRedriveVisit(GWetRedrive, LedgerSurface::WetRedrive_NoMid);
				continue;
			}
			// BOTH PARAMETERS, THROUGH THE TWO FUNCTIONS THE BIND USED, with
			// the same two inputs: the surface name and whether that surface's
			// albedo texture actually bound. The second is read off the bind
			// record because the texture array that answered it lives inside
			// BindSurfaces and is gone by now.
			const bool bAlbedoBound = GBinds[(size_t)Idx].bAlbedoBound;
			const LedgerSurface::WetBind Wet =
				LedgerSurface::WetBindFor(GBinds[(size_t)Idx].Surface, bAlbedoBound, Want);
			const LedgerSurface::Grade Graded =
				LedgerSurface::WetGradeFor(GBinds[(size_t)Idx].Surface, bAlbedoBound, Want);
			Mid->SetVectorParameterValue(
				FName(UTF8_TO_TCHAR(LedgerSurface::AlbedoGradeParam())),
				FLinearColor((float)Graded.R, (float)Graded.G,
				             (float)Graded.B, 1.0f));
			Mid->SetScalarParameterValue(
				FName(UTF8_TO_TCHAR(LedgerSurface::WetnessParam())),
				(float)Wet.Wetness);
			LedgerSurface::WetRedriveVisit(GWetRedrive, LedgerSurface::WetRedrive_Wrote);
			// AND THE SURFACE'S OWN RECORD FOLLOWS THE WRITE, so the
			// per-surface line and the frame cannot disagree about which
			// condition's wetness the street is wearing. LAST-WINS by
			// construction, and wetSetStat says so on the line.
			GBinds[(size_t)Idx].Wet = Wet;
			GBinds[(size_t)Idx].bWetSet = true;
			GBinds[(size_t)Idx].Graded = Graded;
			GBinds[(size_t)Idx].bGradeSet = true;
			GBinds[(size_t)Idx].WetFrom = C.Id;
			// AND THE READBACK, ONCE PER SURFACE PER WALK, ON THE FIRST PIECE
			// OF THAT SURFACE THE WALK WROTE. Asked in the same few statements
			// as the set, so nothing in between can explain a difference, and
			// it is the key that answers "dead write or not" for the re-drive
			// exactly as the bind's own readback answers it for the bind.
			// WHAT IT CANNOT SEE is what the bind's readback cannot see: this
			// is the game thread's copy, not the render proxy, and the control
			// quads are the render side of that question.
			//
			// bAsked IS NOT TOUCHED HERE, deliberately. It means "the bind
			// made an instance for this surface and asked it for its texture
			// and tiling back", and a re-drive asks neither; widening it would
			// move what a key means without moving its name. The wetness half
			// of the readback is the half a re-drive owns, and the run's copy
			// of it rides wetnessRedriveSetGot on the done line where no
			// bAsked gate stands in front of it.
			if (!ReadTaken[(size_t)Idx])
			{
				ReadTaken[(size_t)Idx] = true;
				const double Got = (double)Mid->K2_GetScalarParameterValue(
					FName(UTF8_TO_TCHAR(LedgerSurface::WetnessParam())));
				LedgerSurface::Readback& RB = GBinds[(size_t)Idx].Read;
				RB.bWetAsked = true;
				RB.SetWet = Wet.Wetness;
				RB.GotWet = Got;
				RB.bWetSame = LedgerSurface::ScalarMatches(RB.SetWet, RB.GotWet);
				if (!bRunReadTaken)
				{
					bRunReadTaken = true;
					LedgerSurface::WetRedriveReadback(GWetRedrive, Wet.Wetness, Got);
				}
			}
		}
	}

	// ---- QUEUE 333: THE LAMP HEAD'S OWN GLASS, DRIVEN BY THE CONDITION ---
	//
	// WHAT THIS EXISTS FOR, in one sentence: emissive=true on a piece spawned
	// a point light 0.05 m under it and did NOTHING to the piece, so the
	// fixture was a dark box with an invisible lamp beneath it and no lit
	// element existed anywhere in the scene. This writes the material
	// parameter that makes the head itself emit.
	//
	// THE WRITE-ON-CHANGE GUARD IS HERE FOR THE SAME MEASURED REASON as
	// ReDriveWetness above and the sky below: ApplyCondition is RE-ENTERED
	// ON EVERY TICK while a condition settles, so an unguarded drive is one
	// vector write per lantern per tick. The asked count and the walk count
	// both ride the materials done line, so the guard can be checked instead
	// of believed.
	//
	// WHAT THIS FUNCTION DECIDES: nothing about pixels. It supplies
	// membership (the pieces the paint loop recorded as emissive), order
	// (the file's own) and live state (the condition's LanternsOn). The
	// colour conversion is the same one LinearFromGamma uses at the point
	// light spawn, so the bulb and the glass cannot end up disagreeing about
	// the colour of sodium.
	void ReDriveLampEmissive(const Condition& C)
	{
		++GLampDrive.Calls;
		const bool bWant = C.LanternsOn;
		if (GLampDrive.bHaveWant && GLampDrive.bWantOn == bWant)
		{
			++GLampDrive.Skipped;
			return;
		}
		GLampDrive.bHaveWant = true;
		GLampDrive.bWantOn = bWant;
		GLampDrive.bEverApplied = true;
		GLampDrive.LastFrom = NoSpaces(C.Id);
		++GLampDrive.Walks;
		// THE VALUE, AND OFF IS EXACTLY BLACK. SrgbToLinear is the tested
		// header's conversion and the one LinearFromGamma calls, so this is
		// the file's stated colour space converted once and not a second
		// pow() written here. Lanterns off multiplies by a hard 0.0f, which
		// lands exactly (0,0,0,1): the material's own default for this
		// parameter, so a day condition leaves the glass at the value the
		// asset ships with rather than at a small lit number.
		const double Gain = bWant ? (double)kLampEmissiveUnitless : 0.0;
		const FLinearColor Value(
			(float)(SrgbToLinear(GSpec.Lantern.R) * Gain),
			(float)(SrgbToLinear(GSpec.Lantern.G) * Gain),
			(float)(SrgbToLinear(GSpec.Lantern.B) * Gain),
			1.0f);
		for (size_t I = 0; I < GLampPieces.size(); ++I)
		{
			++GLampDrive.Visits;
			UMaterialInstanceDynamic* Mid = GLampPieces[I].Mid;
			if (Mid == nullptr) { ++GLampDrive.NoMid; continue; }
			Mid->SetVectorParameterValue(FName(TEXT("EmissiveColor")), Value);
			++GLampDrive.Wrote;
			// AND THE READBACK, IN THE SAME FEW STATEMENTS AS THE SET, so
			// nothing in between can explain a difference. ONCE PER WALK and
			// not once per lantern: four lanterns would answer one question
			// about the material four times.
			//
			// WHAT IT ASKS AND WHAT IT DELIBERATELY DOES NOT. It asks the
			// component whether the material it will be DRAWN with is still
			// the instance this write went to, which is the dead-write
			// question a game-thread parameter echo cannot answer. It does
			// NOT ask the value back, for two reasons: the value's real
			// readback is the frame, where lampGlow on every shot line is
			// the render side of this write and is the item's acceptance
			// instrument; and the engine call that would echo a VECTOR
			// parameter has no signature readable in the container this was
			// written in and no precedent anywhere in this repository, while
			// every call above it does. An unverified signature costs a
			// whole CI round trip and buys a weaker answer than the frame.
			if (!GLampDrive.bCompIsMidAsked && GLampPieces[I].Comp != nullptr)
			{
				GLampDrive.bCompIsMidAsked = true;
				UMaterialInterface* CompMat = GLampPieces[I].Comp->GetMaterial(0);
				GLampDrive.bCompIsMid = (CompMat == (UMaterialInterface*)Mid);
				const size_t At = GLampPieces[I].PieceIndex;
				if (At < GSpec.Pieces.size())
				{
					GLampDrive.CompIsMidOn = NoSpaces(GSpec.Pieces[At].Name);
				}
			}
		}
	}

	// ---- QUEUE 361: THE SKY DOME'S LUMINANCE, DRIVEN BY THE CONDITION ---
	//
	// THE SAME SHAPE AS THE TWO DRIVES ABOVE AND DELIBERATELY NOT A THIRD
	// ONE: a guard keyed on the last applied value, re-entered on every tick
	// while a condition settles, counters on the materials done line, and
	// the readback taken in the same few statements as the set.
	//
	// WHAT IT DECIDES: nothing. It supplies live state (the condition's
	// sky_intensity) and order; the multiplication, the floor and the whole
	// printed string are in VignetteSpec.h where the tests run.
	//
	// THE GUARD COMPARES EXACTLY AND NOT WITHIN A TOLERANCE. Both sides come
	// out of the same function over the same two inputs, so equal conditions
	// give bit-identical doubles; a tolerance here would buy nothing and
	// would silently swallow a deliberate change smaller than itself. The
	// READBACK below is the comparison that needs one, because the parameter
	// is a float and the echo is a float widened back.
	void ReDriveSkyLuminance(const Condition& C)
	{
		++GSkyLumDrive.Calls;
		const double Want = LedgerVignette::SkyDomeLuminance(
			C.SkyIntensity, (double)kSkyLuminanceGain);
		if (!LedgerVignette::SkyLumNeeded(GSkyLumDrive, Want))
		{
			++GSkyLumDrive.Skipped;
			return;
		}
		GSkyLumDrive.bHaveLast = true;
		GSkyLumDrive.Last      = Want;
		GSkyLumDrive.LastAsked = C.SkyIntensity;
		GSkyLumDrive.LastFrom  = NoSpaces(C.Id);
		++GSkyLumDrive.Walks;
		// NO DOME IS COUNTED, NOT WORKED AROUND. A sky that failed to spawn
		// leaves nothing to write to, and walks minus wrote is the
		// denominator that says so on the line.
		if (GSkyDomeMid == nullptr) { ++GSkyLumDrive.NoMid; return; }
		GSkyDomeMid->SetScalarParameterValue(FName(kSkyLuminanceParam),
		                                     (float)Want);
		++GSkyLumDrive.Wrote;
		// AND THE READBACK, IN THE SAME FEW STATEMENTS AS THE SET, through
		// the one echo call this repository already compiles: ReDriveWetness
		// asks K2_GetScalarParameterValue for its wetness in exactly this
		// shape. LAST-WINS, one pair, because 43 shots answering the same
		// question 43 times is one fact printed 43 times.
		//
		// WHAT IT CANNOT SEE, said here rather than discovered later: this is
		// the game thread's copy of the parameter, not the render proxy, and
		// it says nothing whatever about how bright the sky LOOKS. The render
		// side of this write is the frame, and the sky band on the shot lines
		// is the acceptance instrument for this item.
		const double Got = (double)GSkyDomeMid->K2_GetScalarParameterValue(
			FName(kSkyLuminanceParam));
		GSkyLumDrive.bReadTaken = true;
		GSkyLumDrive.ReadSet    = Want;
		GSkyLumDrive.ReadGot    = Got;
	}

	// THE DRIVE'S TALLIES, AND EVERY ZERO HERE SHIPS ITS DENOMINATOR.
	// WHOLE-RUN NUMBERS ONLY: this rides the materials done line, never a
	// shot line, which is the separation WetRedriveSegment keeps. The
	// per-frame half of this item is lampGlow and it is on the shot lines.
	//
	// A RUN WHERE THE DRIVE NEVER RAN PRINTS THE WORDS "nothing measured"
	// and still prints inFile, because a street with no emissive piece and a
	// drive that was never called are different facts and a bare 0 cannot
	// tell them apart.
	std::string LampDriveSegment()
	{
		const int InFile = LedgerVignette::EmissiveCount(GSpec.Pieces);
		const int Held = (int)GLampPieces.size();
		char B[560];
		if (GLampDrive.Calls == 0)
		{
			std::snprintf(B, sizeof(B),
				" lampDrive=nothing-measured/the-drive-was-never-called"
				" lampDriveHeld=%d/inFile=%d", Held, InFile);
			return std::string(B);
		}
		std::snprintf(B, sizeof(B),
			" lampDriveStat=cumulative-over-the-run/value-and-from-are-last-wins"
			" lampDriveAsked=%d/walked=%d/skipped=%d"
			" lampDriveWrote=%d/visits=%d/nullInstance=%d"
			" lampDriveHeld=%d/inFile=%d"
			" lampDriveOn=%s lampDriveFrom=%s lampDriveValue=%.2f/unitless"
			" lampDriveCompIsMid=%s/on=%s"
			" lampDriveValueReadback=the-frame/lampGlow-on-the-shot-lines"
			"/not-a-game-thread-echo",
			GLampDrive.Calls, GLampDrive.Walks, GLampDrive.Skipped,
			GLampDrive.Wrote, GLampDrive.Visits, GLampDrive.NoMid,
			Held, InFile,
			GLampDrive.bWantOn ? "yes" : "no",
			GLampDrive.LastFrom.c_str(),
			GLampDrive.bWantOn ? kLampEmissiveUnitless : 0.0f,
			GLampDrive.bCompIsMidAsked
				? (GLampDrive.bCompIsMid ? "is-the-instance-we-wrote"
				                         : "SOMETHING-ELSE")
				: "nothing-measured",
			GLampDrive.CompIsMidOn.c_str());
		return std::string(B);
	}

	// THE ONLY WRITER OF THE SUN, THE FILL, THE FOG, THE SKY AND THE WETNESS.
	// Every condition change writes all of them, so no setting can carry over
	// from the previous shot and be attributed to this one.
	//
	// THE FILLS ARE RETIRED WHEN THE SKY IS WHOLE, AND ONLY THEN. Two
	// sources of ambient light in one scene is the fault this file's own
	// header calls the one this project has paid for twice, and a captured
	// sky is a strictly better statement of the same thing than three
	// directional lights standing in for an ambient mode. But a sky that
	// failed to spawn must not take the street's light away with it, so the
	// retirement is conditional on the structure being there and the scene
	// line prints which of the two happened.
	//
	// WHAT THIS CANNOT SEE, said here rather than discovered later: a sky
	// light whose capture comes back BLACK is structurally whole and would
	// retire the fills anyway. Nothing in this process can read the captured
	// cubemap's brightness. What answers it is the frame, and the sky and
	// ground bands on every shot line are that answer.
	void ApplyCondition(const Condition& C)
	{
		++GApplyCalls;
		// THE EXPOSURE THIS CONDITION ASKS TO BE PHOTOGRAPHED AT, QUEUE 235,
		// HANDED TO THE ONE PLACE THAT WRITES POST-PROCESS VALUES. Zero or
		// less is a condition asking for nothing, which is what every
		// condition written before 2026-09-10 says, and PlaceCamera then
		// writes the override flags FALSE and restores the captured clamp
		// values, 2026-09-14; see the LEAK block at the write site.
		GExposurePinNow = C.ExposurePin;
		// THE SKY THIS CONDITION NAMES, ON THE DOME. Write-on-change: a
		// condition naming the photograph already up costs nothing, and a day
		// photograph left over a night street is the failure this prevents.
		BindSkyPhoto(C.Hdri);
		// AND THE DOME'S OTHER PARAMETER IN THE SAME BREATH, QUEUE 361. The
		// line above decides WHICH photograph the dome wears; this decides
		// HOW BRIGHT it renders, off the same condition. They are written
		// together so no condition can change one without the other, which
		// is the failure this item is: one luminance served a day row and a
		// night row and the night rendered like noon.
		ReDriveSkyLuminance(C);
		GExposurePinFamilySunOn = C.SunOn;
		const FLinearColor DaySky(0.42f, 0.46f, 0.52f, 1.0f);
		const FLinearColor NightSky(0.05f, 0.05f, 0.07f, 1.0f);
		const FLinearColor Sky = C.SunOn ? DaySky : NightSky;
		const bool bWhole = SkyIsWhole();
		// THE SUN'S INTENSITY COMES OFF THE CONDITION, QUEUE 205. It was the
		// bare literal 3.0f here, the only light in this file with no named
		// constant, and it was tuned against three directional fills that
		// the captured sky retired four lines below on 9 September: the
		// value stood while the thing it was calibrated against was
		// deleted, and no number moved, so no gate could see it. NIGHT IS
		// STILL A HARD ZERO and the gate stays: a sun-off condition that
		// names a bright sun must not light the night, whatever its data
		// row says.
		SetDirectional(GSun, FLinearColor(0.95f, 0.96f, 1.0f, 1.0f),
		               C.SunOn ? (float)C.SunIntensity : 0.0f);
		// THE FILLS AT ZERO ALSO STOP THEM BEING SUNS. A directional light
		// is an atmosphere sun light by default in this engine, so three
		// fills left burning would put up to two extra sun discs in the sky
		// the atmosphere renders. Zeroing them is one change that answers
		// two problems, and it is why no atmosphere-sun property is touched
		// anywhere in this file.
		const float FillScale = bWhole ? 0.0f : 1.0f;
		SetDirectional(GFillA, Sky, kFillSky * FillScale);
		SetDirectional(GFillB, Sky * 0.75f, kFillEquator * FillScale);
		SetDirectional(GFillC, Sky * 0.45f, kFillGround * FillScale);
		for (int32 I = 0; I < GLanterns.Num(); ++I)
			if (ULightComponent* L = GLanterns[I]->GetLightComponent()) L->SetVisibility(C.LanternsOn);
		// AND THE LAMP HEADS THEMSELVES, QUEUE 333, IMMEDIATELY BESIDE THE
		// LIGHTS THEY BELONG TO. The two lines above switch the light the
		// fixture CASTS; this switches the glass the fixture IS. They are
		// driven off the same C.LanternsOn in the same breath so no
		// condition can light one without the other.
		ReDriveLampEmissive(C);
		for (int32 I = 0; I < GWindows.Num(); ++I)
			if (ULightComponent* L = GWindows[I]->GetLightComponent()) L->SetVisibility(C.WindowsOn);
		if (GFog != nullptr)
		{
			// FOUND BY CLASS RATHER THAN BY AN ACCESSOR. The actor's named
			// getter has been renamed across engine versions and this
			// container cannot compile a single line of this file; a lookup
			// by component class is the API least likely to have moved.
			if (UExponentialHeightFogComponent* F =
			        GFog->FindComponentByClass<UExponentialHeightFogComponent>())
			{
				F->SetFogDensity((float)C.FogDensity * kFogDensityGain);
				F->SetFogInscatteringColor(C.SunOn ? FLinearColor(0.55f, 0.58f, 0.62f, 1.0f)
				                                   : FLinearColor(0.06f, 0.05f, 0.05f, 1.0f));
				F->SetFogHeightFalloff(0.02f);
				// AND THE FOG STOPS OWNING THE FAR FIELD, which is the
				// measurement that started this: with nothing behind it the
				// fog saturates at the far plane and IS the sky in every
				// frame this project has shot. Capped only when there is
				// something behind it to see; with no sky the fog keeps the
				// far field it has always had, so a failed spawn does not
				// also silently change the fog.
				// A4, 2026-09-09: THE CAP COMES OUT OF THE CONDITION NOW.
				// kFogMaxOpacityWithSky 0.45f was one number derived from two
				// measured ones and an unknown, and it was never a series.
				// The field is required in both readers, so there is no path
				// where this silently falls back to the literal; the verdict
				// prints fogMaxOpacityRead ONCE PER RUN on the sky line, read
				// off the component after the last condition applied
				// (SkySegmentNow, last-wins), with nothing asked beside it;
				// the per-shot read beside the ask is queue 287.
				F->SetFogMaxOpacity(bWhole ? (float)C.FogMaxOpacity : 1.0f);
			}
		}
		// ---- THE SKY, WRITTEN ON CHANGE AND NOT PER TICK ---------------
		//
		// This function is re-entered every tick while a condition settles.
		// A recapture per tick is a rebuild asked for a hundred times, and
		// the count of asks against the count of writes rides the scene line
		// so nobody has to take this comment's word for it.
		//
		// ONCE PER PASS, NOT ONCE PER CONDITION CHANGE. Keyed on the pass
		// epoch rather than on the condition id, because two shots naming the
		// same condition are two frames and the second would otherwise be
		// photographed against a capture one whole shot older. The sky is not
		// a light value and none of the four scattering constants or the
		// intensity above changes here: this decides only WHEN the same write
		// happens. skyWrites therefore reads one per pass rather than one per
		// condition change, and a pass is a shot or the determinism repeat.
		if (bWhole && GSkyEpoch != GWantSkyEpoch)
		{
			GSkyEpoch = GWantSkyEpoch;
			++GSkyWrites;
			if (USkyAtmosphereComponent* A =
			        GAtmosphere->FindComponentByClass<USkyAtmosphereComponent>())
			{
				// PALE, FLAT AND LOW CONTRAST, which is what the reference
				// sheet's sky is and what a British overcast is. The four
				// values are named constants with their reasons at the top
				// of this file; none of them is measured and the verdict
				// says so.
				A->SetRayleighScatteringScale(kSkyRayleighScale);
				A->SetMieScatteringScale(kSkyMieScale);
				A->SetMieAnisotropy(kSkyMieAnisotropy);
				A->SetMultiScatteringFactor(kSkyMultiScattering);
			}
			if (USkyLightComponent* SC = GSky->FindComponentByClass<USkyLightComponent>())
			{
				// OFF THE CONDITION, NOT OFF A CONSTANT KEYED ON SunOn. The
				// ladder's control row is a DAY condition with the sky at
				// 0.35, which the old pair of constants could not say.
				SC->SetIntensity((float)C.SkyIntensity);
				// RECAPTURED EXPLICITLY ON THE CHANGE. Real-time capture
				// refreshes on its own, but a shot is photographed a fixed
				// number of frames after the condition changes and a sky
				// still carrying the previous condition would be attributed
				// to this one.
				SC->RecaptureSky();
			}
		}
		// ---- AND THE WETNESS, QUEUE 309, ON THE SAME WRITE-ON-CHANGE RULE
		//
		// LAST IN THE FUNCTION AND NOT FIRST, for one reason: everything
		// above writes a handful of components and this walks the street, so
		// a condition that fails to light is not also a condition that spent
		// its tick in a piece loop. The order has no other meaning; a
		// material parameter and a light are not read by each other.
		ReDriveWetness(C);
	}

	// ---- AMENDMENT A1: FOUR FLAGS, READ OFF THE LIVE OBJECTS -------------
	//
	// WHY REFLECTION AND NOT A MEMBER ACCESS, which is a constraint of this
	// project and not a preference. This module cannot be compiled in the
	// container that writes it, so a member spelled wrong is a compile error
	// found on a machine 17 to 33 minutes away, and the next reading is a
	// day later. A property name spelled wrong HERE is a nothing-measured on
	// the verdict naming every spelling it tried, which the next run fixes
	// with no round trip at all. The cost is real and is stated: a property
	// this engine version does carry under a third name reads as unmeasured
	// rather than as read.
	//
	// AND IT CAN ONLY EVER RETURN nothing-measured, NEVER no (rule 3b). A
	// flag nobody could read must not print as a flag that was false: this
	// whole amendment exists because a verdict said which sky lights the
	// street from state that was never read.
	int ReadFlagProp(const UObject* Obj, const TCHAR* const* Names, int Count,
	                 std::string& FromOut)
	{
		std::string Tried;
		for (int I = 0; I < Count; ++I)
		{
			if (I > 0) { Tried += ".."; }
			Tried += std::string(TCHAR_TO_UTF8(Names[I]));
		}
		FromOut = NoSpaces(Tried);
		if (Obj == nullptr) { return LedgerVignette::SkyFlag_NotMeasured; }
		for (int I = 0; I < Count; ++I)
		{
			if (FBoolProperty* Prop =
			        FindFProperty<FBoolProperty>(Obj->GetClass(), FName(Names[I])))
			{
				FromOut = NoSpaces(std::string(TCHAR_TO_UTF8(Names[I])));
				return Prop->GetPropertyValue_InContainer(Obj)
				     ? LedgerVignette::SkyFlag_Yes : LedgerVignette::SkyFlag_No;
			}
		}
		return LedgerVignette::SkyFlag_NotMeasured;
	}

	// THE SHADING MODEL IS A TEnumAsByte, which the reflection system carries
	// as a byte property. Its VALUE is returned, not a word: the word is the
	// header's, where g++ runs it.
	int ReadEnumByteProp(const UObject* Obj, const TCHAR* const* Names, int Count,
	                     std::string& FromOut)
	{
		std::string Tried;
		for (int I = 0; I < Count; ++I)
		{
			if (I > 0) { Tried += ".."; }
			Tried += std::string(TCHAR_TO_UTF8(Names[I]));
		}
		FromOut = NoSpaces(Tried);
		if (Obj == nullptr) { return LedgerVignette::SkyFlag_NotMeasured; }
		for (int I = 0; I < Count; ++I)
		{
			if (FByteProperty* Prop =
			        FindFProperty<FByteProperty>(Obj->GetClass(), FName(Names[I])))
			{
				FromOut = NoSpaces(std::string(TCHAR_TO_UTF8(Names[I])));
				return (int)Prop->GetPropertyValue_InContainer(Obj);
			}
		}
		return LedgerVignette::SkyFlag_NotMeasured;
	}

	// ---- QUEUE 186: WHAT THE SKY ACTUALLY IS, READ WHEN IT IS ASKED ------
	//
	// skyModel and ambientModel used to be two literals inside a format
	// string in BuildScene. One of them was false and no run could have said
	// so, because a literal in a printf cannot be wrong about the world in
	// any way a test can catch. Both words now come out of
	// LedgerVignette::SkySegment, which g++ runs before any dispatch, from
	// state READ BACK off the components.
	//
	// AND IT IS TAKEN HERE RATHER THAN AT BUILD TIME, which is not a detail:
	// BuildScene runs BEFORE any condition is applied, so a reading taken
	// there would report fillsRetiredToZero=no and skyWrites=0/of=0 on every
	// run for ever, and both would be stale rather than wrong-in-a-visible-
	// way. This runs when a verdict asks for the line, by which time every
	// condition the run applied has been applied.
	std::string SkySegmentNow()
	{
		LedgerVignette::SkyIn In;
		In.bSkyLightActor   = (GSky != nullptr);
		In.bAtmosphereActor = (GAtmosphere != nullptr);
		if (GSky != nullptr)
		{
			if (USkyLightComponent* SC = GSky->FindComponentByClass<USkyLightComponent>())
			{
				In.bSkyLightComponent   = true;
				In.SourceTypeRead       = (int)SC->SourceType;
				In.bRealTimeCaptureRead = (SC->bRealTimeCapture != 0);
				In.SkyIntensityRead     = (double)SC->Intensity;
			}
		}
		if (GAtmosphere != nullptr)
		{
			In.bAtmosphereComponent =
				(GAtmosphere->FindComponentByClass<USkyAtmosphereComponent>() != nullptr);
		}
		if (GFog != nullptr)
		{
			if (UExponentialHeightFogComponent* F =
			        GFog->FindComponentByClass<UExponentialHeightFogComponent>())
			{
				In.bFogComponent     = true;
				In.FogDensityRead    = (double)F->FogDensity;
				In.FogMaxOpacityRead = (double)F->FogMaxOpacity;
			}
		}
		// ---- QUEUE 205: THE SUN, OFF ITS OWN COMPONENT ------------------
		//
		// The verdict said `sun=yes` and that was the whole of what any run
		// has ever known about this light: that something spawned. Every
		// value below is asked of the live component, so a sun whose
		// intensity never took, whose shadows were turned off by something
		// else, or which is pointing somewhere else, says so itself
		// instead of being inferred from the number that was written.
		if (GSun != nullptr)
		{
			In.bSunActor = true;
			if (ULightComponent* LC = GSun->GetLightComponent())
			{
				In.bSunComponent        = true;
				In.SunIntensityRead     = (double)LC->Intensity;
				In.bSunCastShadowsRead  = (LC->CastShadows != 0);
				const FRotator R        = LC->GetComponentRotation();
				In.SunPitchRead         = (double)R.Pitch;
				In.SunYawRead           = (double)R.Yaw;
				In.SunMobilityRead      = (int)LC->Mobility.GetValue();
			}
		}
		In.FillsSpawned = (GFillA ? 1 : 0) + (GFillB ? 1 : 0) + (GFillC ? 1 : 0);
		// RETIRED IS READ OFF THE LIGHT, NEVER PREDICTED FROM THE RULE THAT
		// SETS IT. ApplyCondition zeroes the fills when the sky is whole;
		// asking the fill what its intensity IS is a different statement
		// from repeating the condition under which it should be zero, and
		// the two disagreeing is exactly what this key exists to show.
		In.bFillsRetired = false;
		if (GFillA != nullptr)
		{
			if (ULightComponent* LC = GFillA->GetLightComponent())
			{
				In.bFillsRetired = (LC->Intensity <= 0.0f) && In.Whole();
			}
		}
		In.ApplyCalls = (int)GApplyCalls;
		In.SkyWrites  = (int)GSkyWrites;
		// THE NAME COMES OUT OF THE SHARED FILE, not out of this file. The
		// condition block has always carried it and nothing has ever read it;
		// printing what was asked for beside what became of it is what turns
		// "the probe never binds the HDRI" from an analysis into a reading.
		In.HdriAsked = GSpec.Conditions.empty() ? std::string("none")
		                                       : GSpec.Conditions[0].Hdri;
		if (In.HdriAsked.empty()) { In.HdriAsked = "none"; }
		In.HdriFoundAt    = GHdriFoundAt;
		In.HdriBytes      = GHdriBytes;
		In.HdriDetectedAs = GHdriDetectedAs;
		// WHAT IT BOUND TO, NOT WHAT IT WAS ASKED FOR. The string is composed
		// where the bind happens and is read here; a run that bound nothing
		// carries NOTHING and the reason, which is a different reading from a
		// run that bound and must never be printable by one that did not.
		In.HdriBoundAs    = GHdriBoundAs;
		In.bPhotoDomeBound = (GSkyDome != nullptr && GSkyDomeMid != nullptr
		                      && GSkyPhotoBinds > 0);
		// ---- AMENDMENT A1. FOUR READS, HERE WITH EVERY OTHER WHOLE-RUN
		// READ, so they are taken after the last condition applied and off
		// the same objects the run rendered with.
		{
			static const TCHAR* const kIsSkyNames[] =
				{ TEXT("bIsSky"), TEXT("IsSky") };
			static const TCHAR* const kTwoSidedNames[] =
				{ TEXT("TwoSided"), TEXT("bTwoSided") };
			static const TCHAR* const kShadingNames[] =
				{ TEXT("ShadingModel"), TEXT("ShadingModels") };
			// NOT SET BY THIS FILE AND NEVER HAS BEEN: a grep for
			// LowerHemisphere over this module returns this block and
			// nothing else. It sits at the engine default and this is the
			// first run to print what that default is. READ, NOT WRITTEN.
			static const TCHAR* const kLowerHemiNames[] =
				{ TEXT("bLowerHemisphereIsBlack"),
				  TEXT("bLowerHemisphereIsSolidColor") };
			// NOTHING IS READ OFF THE MATERIAL WHEN NO DOME STANDS. The
			// parent asset would answer the same three flags whether or not
			// anything in this run was wearing it, and that reading would be
			// true about the asset and false about the frame.
			const UObject* DomeMat = (GSkyDome != nullptr && GSkyDomeMid != nullptr)
			                       ? (const UObject*)GSkyDomeParent : nullptr;
			In.DomeMatIsSky = ReadFlagProp(DomeMat, kIsSkyNames,
				(int)(sizeof(kIsSkyNames) / sizeof(kIsSkyNames[0])),
				In.DomeMatIsSkyFrom);
			In.DomeMatTwoSided = ReadFlagProp(DomeMat, kTwoSidedNames,
				(int)(sizeof(kTwoSidedNames) / sizeof(kTwoSidedNames[0])),
				In.DomeMatTwoSidedFrom);
			In.DomeMatShadingModel = ReadEnumByteProp(DomeMat, kShadingNames,
				(int)(sizeof(kShadingNames) / sizeof(kShadingNames[0])),
				In.DomeMatShadingModelFrom);
			const UObject* SkyComp = nullptr;
			if (GSky != nullptr)
			{
				SkyComp = GSky->FindComponentByClass<USkyLightComponent>();
			}
			In.SkyLightLowerHemiSolid = ReadFlagProp(SkyComp, kLowerHemiNames,
				(int)(sizeof(kLowerHemiNames) / sizeof(kLowerHemiNames[0])),
				In.SkyLightLowerHemiSolidFrom);
		}
		return LedgerVignette::SkySegment(In);
	}

	// ONE PRODUCER FOR THE LINE ALL FOUR VERDICTS PRINT. The vignette, the
	// walk and the crime runs each print the street's scene line, and a sky
	// appended in one of those places and not the others would be three
	// answers to one question.
	std::string SceneLineWithSky()
	{
		return GSceneLine + " " + SkySegmentNow();
	}

	// A CVAR THIS ENGINE VERSION DOES NOT CARRY PRINTS THE WORD `absent`.
	// A missing cvar read as 0 is the same string a disabled feature prints,
	// and the two are different facts.
	FString CVarIntOrAbsent(const TCHAR* Name)
	{
		if (IConsoleVariable* V = IConsoleManager::Get().FindConsoleVariable(Name))
		{
			return FString::Printf(TEXT("%d"), V->GetInt());
		}
		return TEXT("absent");
	}

	// PLACE THE CAMERA AND READ THE PLACEMENT BACK. Asking for a transform
	// and printing the transform you asked for is not evidence that anything
	// moved.
	FString GCamLine = TEXT("shotCamPlaced=NOT-REACHED");
	double  GEyeY = 0.0;
	FString GCamEdge = TEXT("none");

	void PlaceCamera(UWorld* World, const Camera& C)
	{
		// THE PIN READING IS CLEARED FIRST, QUEUE 235, so a placement that
		// never reaches a camera component prints NOT-READ rather than the
		// LAST shot's reading under this shot's name. The asked value and the
		// family survive the clear because they are facts about the condition
		// in force and not about the component.
		{
			const double Asked = GExposurePinNow;
			const bool   bDay  = GExposurePinFamilySunOn;
			GShotPin = LedgerVignette::ExposurePinIn();
			GShotPin.Asked  = Asked;
			GShotPin.bSunOn = bDay;
		}
		if (World == nullptr)
		{
			// A WORLD THAT WENT AWAY BETWEEN TWO TICKS IS A FINDING, and it
			// must not read as a camera that was placed at the origin.
			GCamLine = TEXT("shotCamPlaced=NO-WORLD shotCamReason=the-game-world-vanished-between-ticks");
			GShotCam = LedgerVignette::ShotCamIn();
			GShotCam.CamId  = C.Id;
			GShotCam.Status = "NO-WORLD";
			return;
		}
		// EYE HEIGHT IS MEASURED FROM THE PAVEMENT UNDER THE CAMERA and the
		// pavement level comes OUT OF THE FILE. The footway falls 1 in 40,
		// so a camera at a fixed y stands at a different height on each side
		// of the street and the matched pair is not matched at all.
		GEyeY = C.GroundY + C.EyeHeightM;
		GCamEdge = FString(UTF8_TO_TCHAR(C.GroundEdge.c_str()));
		const FVector Want(C.X * 100.0, C.Z * 100.0, GEyeY * 100.0);
		// PITCH IS NEGATED AND FOV IS CONVERTED. The file's camera pitch is
		// positive DOWN, as Unity's is; this engine's is positive up. The
		// file's fov is VERTICAL, as Unity's is; this engine's is
		// HORIZONTAL, and handing 60 straight over would photograph a third
		// of the street the Unity frame shows.
		const FRotator WantRot((float)-C.PitchDeg, (float)C.YawDeg, 0.0f);
		if (GCam == nullptr)
		{
			FActorSpawnParameters Params;
			Params.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
			GCam = World->SpawnActor<ACameraActor>(ACameraActor::StaticClass(), Want, WantRot, Params);
		}
		else
		{
			GCam->SetActorLocationAndRotation(Want, WantRot);
		}
		if (GCam != nullptr)
		{
			if (UCameraComponent* CC = GCam->GetCameraComponent())
			{
				CC->SetFieldOfView((float)HorizontalFovDeg(C.FovVerticalDeg, kShotW, kShotH));
				CC->SetAspectRatio((float)kShotW / (float)kShotH);
				CC->SetConstraintAspectRatio(true);
				// WHAT THE TONE MAPPER IS SET TO, READ BACK RATHER THAN
				// ASSUMED, because a clipped ground plane is a question about
				// exposure and this probe overrides nothing. The camera's own
				// post-process values are printed WITH their override flags,
				// since a value that is not overridden is not the value in
				// force; the cvars beside them are what actually decides, and
				// a cvar this engine version does not have prints `absent`
				// rather than a zero that would read as "off".
				// ---- THE ONE THING THIS PROBE NOW OVERRIDES, AND WHY ----
				//
				// MEASURED, NOT ARGUED. Run 38's `light control_no_toggle`
				// line photographs a shot a second time with NOTHING
				// TOGGLED: 715552 of 921600 pixels came back darker in the
				// first take and the whole-frame mean moved 0.09107 to
				// 0.09490, 0.28 s apart, same camera, same condition, same
				// sky capture. The eight successive frames of that shot's
				// probe pass then rise MONOTONICALLY, 0.09490 to 0.10780,
				// while lights are being switched OFF one at a time. A frame
				// getting brighter as the scene loses lights is not the
				// scene: it is a gain applied after it, still moving two
				// seconds in. Eye adaptation is temporal and every shutter
				// here falls 0.65 s after its condition change, so no frame
				// in that run was photographed at a settled exposure and
				// every cross-shot luma comparison it supports is partly a
				// comparison of the adaptation's starting point.
				//
				// ONE OWNER PER GLOBAL. This is written HERE and nowhere
				// else: the only other post-process writer in this module is
				// the readback below, which reads. It is the camera's own
				// component rather than a cvar, so nothing outside this
				// probe's view is touched, and the override flags are set
				// beside the values because a value that is not overridden
				// is not the value in force.
				FPostProcessSettings& PPW = CC->PostProcessSettings;
				PPW.bOverride_AutoExposureSpeedUp   = true;
				PPW.AutoExposureSpeedUp             = (float)kExposureSnapSpeed;
				PPW.bOverride_AutoExposureSpeedDown = true;
				PPW.AutoExposureSpeedDown           = (float)kExposureSnapSpeed;
				// ---- AND THE VALUE, QUEUE 235, WHEN THE CONDITION ASKS ----
				//
				// THE TWO CLAMPS SET TO ONE NUMBER IS WHAT REMOVES ADAPTATION:
				// the histogram's own answer is clamped into a range of zero
				// width, so the exposure cannot move however the scene moves.
				// A condition asking for nothing (exposure_pin 0.0, which is
				// every condition older than queue 235) writes NO override
				// here, so the rows that were already being photographed are
				// photographed exactly as before and this change moves no
				// frame that existed before it.
				//
				// SAME OWNER AS THE SPEEDS. This is the only writer of any
				// post-process value in this module; the block below reads.
				// The write sits at the camera placement, which happens once
				// per shot, so the pin is per frame and not per run.
				//
				// ---- THE LEAK, AND WHY THERE IS NO `if` WITHOUT AN `else`
				// HERE ANY MORE, 2026-09-14 ----
				//
				// THE COMMENT ABOVE WAS FALSE AND THE VERDICT SAID SO FOR A
				// WHOLE RUN. "A condition asking for nothing writes NO
				// override here, so the rows that were already being
				// photographed are photographed exactly as before" is only
				// true of a camera that is thrown away between shots. This
				// one is SPAWNED ONCE AND MOVED, which the run line prints
				// as shotCamActorStat=one-per-run, so an override written by
				// a pinned shot stayed in force for every shot after it.
				// Four rows of thirty seven at f6508b3 asked for no pin and
				// read back 0.0300, 0.3000, 3.0000 and 10.0000 with
				// overrides 1/1, and the determinism repeat, an overcast_day
				// frame asking for nothing, came back at 0.0518 against the
				// same shot's 0.6099 at the top of the run.
				//
				// SO THE FLAGS ARE WRITTEN ON EVERY SHOT, true or false, and
				// the decision is made in VignetteSpec.h where g++ runs it.
				// An unpinned shot restores the values CAPTURED off the
				// component before the run's first write.
				if (!GPinCaptured)
				{
					GPinCaptured    = true;
					GPinCapturedMin = (double)PPW.AutoExposureMinBrightness;
					GPinCapturedMax = (double)PPW.AutoExposureMaxBrightness;
				}
				const LedgerVignette::ExposurePinWriteOut PinWrite =
					LedgerVignette::ExposurePinWriteFor(
						GExposurePinNow, GPinCaptured, GPinCapturedMin, GPinCapturedMax,
						(double)PPW.AutoExposureMinBrightness,
						(double)PPW.AutoExposureMaxBrightness);
				PPW.bOverride_AutoExposureMinBrightness = PinWrite.bOverride;
				PPW.bOverride_AutoExposureMaxBrightness = PinWrite.bOverride;
				PPW.AutoExposureMinBrightness           = (float)PinWrite.Min;
				PPW.AutoExposureMaxBrightness           = (float)PinWrite.Max;
				const FPostProcessSettings& PP = CC->PostProcessSettings;
				// ASKED BESIDE READ, PER SHOT, THE WAY THE LIGHT AIM LINE
				// DOES IT. A value that lands on the game thread and never
				// reaches the render proxy reads back as the same pointer it
				// was written through, so this is necessary and not
				// sufficient: the row's own frame luma is the other half and
				// it rides the same shot line.
				GShotPin.Asked    = GExposurePinNow;
				GShotPin.bSunOn   = GExposurePinFamilySunOn;
				GShotPin.ReadMin  = PP.AutoExposureMinBrightness;
				GShotPin.ReadMax  = PP.AutoExposureMaxBrightness;
				GShotPin.bOverMin = PP.bOverride_AutoExposureMinBrightness;
				GShotPin.bOverMax = PP.bOverride_AutoExposureMaxBrightness;
				GShotPin.bRead    = true;
				GToneLine = FString::Printf(
					TEXT("tonemapRead=camera-postprocess-and-cvars ")
					TEXT("ppAutoExposureMethod=%d ppAutoExposureBias=%.3f ")
					TEXT("ppAutoExposureMinBrightness=%.4f ppAutoExposureMaxBrightness=%.4f ")
					TEXT("ppOverridesMethod/Bias/Min/Max=%d/%d/%d/%d ")
					TEXT("cvarDefaultAutoExposure=%s cvarDefaultAutoExposureMethod=%s ")
					TEXT("cvarEyeAdaptationMethodOverride=%s cvarExtendDefaultLuminanceRange=%s ")
					TEXT("ppAutoExposureSpeedUpRead=%.1f ppAutoExposureSpeedDownRead=%.1f ")
					TEXT("ppOverridesSpeedUp/SpeedDown=%d/%d ppBlendWeightRead=%.3f ")
					TEXT("tonemapStat=last-camera-placement/one-per-run ")
					TEXT("ppNote=this-probe-overrides-the-two-eye-adaptation-SPEEDS-always-and-the-")
					TEXT("two-BRIGHTNESS-clamps-on-any-shot-whose-condition-names-an-exposure_pin/")
					TEXT("queue-235/the-values-above-are-the-game-threads-copy-after-the-write/")
					TEXT("cvars-are-what-is-in-force-for-everything-else/")
					TEXT("THIS-LINE-IS-ONE-PER-RUN-AND-LAST-WINS-so-the-pin-that-photographed-a-")
					TEXT("GIVEN-frame-is-on-that-frames-shot-line-under-shotExposurePin"),
					(int32)PP.AutoExposureMethod, PP.AutoExposureBias,
					PP.AutoExposureMinBrightness, PP.AutoExposureMaxBrightness,
					PP.bOverride_AutoExposureMethod ? 1 : 0,
					PP.bOverride_AutoExposureBias ? 1 : 0,
					PP.bOverride_AutoExposureMinBrightness ? 1 : 0,
					PP.bOverride_AutoExposureMaxBrightness ? 1 : 0,
					*CVarIntOrAbsent(TEXT("r.DefaultFeature.AutoExposure")),
					*CVarIntOrAbsent(TEXT("r.DefaultFeature.AutoExposure.Method")),
					*CVarIntOrAbsent(TEXT("r.EyeAdaptation.MethodOverride")),
					*CVarIntOrAbsent(TEXT("r.DefaultFeature.AutoExposure.ExtendDefaultLuminanceRange")),
					PP.AutoExposureSpeedUp, PP.AutoExposureSpeedDown,
					PP.bOverride_AutoExposureSpeedUp ? 1 : 0,
					PP.bOverride_AutoExposureSpeedDown ? 1 : 0,
					CC->PostProcessBlendWeight);
				// ---- QUEUE 186: WHAT, IF ANYTHING, THE ROAD CAN REFLECT --
				//
				// A sky that lights a scene and a sky that is MIRRORED in
				// wet stone are two different renderer paths, and only the
				// second is what the reference panel's lower half is made
				// of. Which paths this build has is not a thing to reason
				// about from documentation: these four cvars decide it and
				// the run can simply read them. `absent` is a real answer
				// and different from 0, which is why CVarIntOrAbsent exists.
				//
				// HOW TO READ THEM. reflectionMethod 1 is Lumen and 2 is
				// screen space in this engine's numbering; a 0 means the
				// only reflection any surface gets is the sky light's own
				// cubemap. skylightRealTimeReflectionCapture is the one that
				// decides whether the cubemap this run captures is used for
				// reflections at all, and a 0 there would mean the sky lights
				// the street and NOTHING mirrors it.
				GToneLine += FString::Printf(
					TEXT(" cvarReflectionMethod=%s cvarDynamicGI=%s ")
					TEXT("cvarSkyLightRealTimeReflectionCapture=%s cvarSkyAtmosphere=%s ")
					TEXT("reflectStat=cvars-read-at-the-last-camera-placement/one-per-run ")
					TEXT("reflectNote=these-say-which-reflection-paths-exist/NOT-that-any-surface-is-wet"),
					*CVarIntOrAbsent(TEXT("r.ReflectionMethod")),
					*CVarIntOrAbsent(TEXT("r.DynamicGlobalIlluminationMethod")),
					*CVarIntOrAbsent(TEXT("r.SkyLight.RealTimeReflectionCapture")),
					*CVarIntOrAbsent(TEXT("r.SkyAtmosphere")));
			}
		}
		FVector GotLoc = FVector::ZeroVector;
		FRotator GotRot = FRotator::ZeroRotator;
		// A POSE NOBODY ANSWERED IS NOT A POSE AT THE ORIGIN. Without a
		// player controller there is no view point to ask, and the two zero
		// vectors below would otherwise print as a camera that really was at
		// the world origin looking down the street.
		bool bReadViewPoint = false;
		if (APlayerController* PC = World->GetFirstPlayerController())
		{
			if (GCam != nullptr) { PC->SetViewTarget(GCam); }
			PC->GetPlayerViewPoint(GotLoc, GotRot);
			bReadViewPoint = true;
		}
		// ---- QUEUE 208: THE POSE IS A PER-SAMPLE FACT AND HAS MOVED -----
		//
		// This line keeps ONLY what is true of the run: that a camera actor
		// exists at all, and which map it is in. The actor is spawned once
		// and moved, so both are run facts. Everything the shot loop used to
		// overwrite here now rides the shot line through ShotCamSegment,
		// which is formatted and tested in VignetteSpec.h. No key is printed
		// in both places: one key with two values under two line shapes is
		// what tools/verdict-dupkeys.py exists to catch.
		GCamLine = FString::Printf(
			TEXT("shotCamPlaced=%s shotWorld=%s ")
			TEXT("shotCamActorStat=one-per-run/the-camera-actor-is-spawned-once-and-moved-per-shot ")
			TEXT("shotCamPoseStat=the-pose-and-the-camera-id-are-per-sample-and-are-on-each-shot-line/")
			TEXT("shotCamId-shotCamAskedXYZcm-shotCamReadXYZcm-shotCamDeltaCm-shotCamAskedPitchYaw-shotCamReadPitchYaw"),
			GCam != nullptr ? TEXT("yes") : TEXT("SPAWN-FAILED"),
			*NoSp(World->GetMapName()));
		// AND THE PAIRED READING FOR THIS FRAME, ASKED AGAINST READ BACK.
		// The distance between the halves is computed in the tested header,
		// never here.
		GShotCam = LedgerVignette::ShotCamIn();
		GShotCam.CamId  = C.Id;
		GShotCam.Status = (GCam == nullptr) ? "SPAWN-FAILED"
		                                   : (bReadViewPoint ? "MEASURED" : "NO-VIEWPOINT");
		GShotCam.AskedXCm = (double)Want.X;
		GShotCam.AskedYCm = (double)Want.Y;
		GShotCam.AskedZCm = (double)Want.Z;
		GShotCam.ReadXCm  = (double)GotLoc.X;
		GShotCam.ReadYCm  = (double)GotLoc.Y;
		GShotCam.ReadZCm  = (double)GotLoc.Z;
		GShotCam.AskedPitchDeg = (double)WantRot.Pitch;
		GShotCam.AskedYawDeg   = (double)WantRot.Yaw;
		GShotCam.ReadPitchDeg  = (double)GotRot.Pitch;
		GShotCam.ReadYawDeg    = (double)GotRot.Yaw;
	}

	// ---- A6: THE FOUR LIGHTS, ASKED AGAINST READ, ONCE PER RUN ----------
	//
	// READ OFF THE COMPONENT'S WORLD ROTATION, which is the same transform
	// the renderer takes the light's direction from and the same one the
	// per-sample shotSunPitchYawRead reads. There is no arrangement in which
	// this readback says one thing and the render lights another way, which
	// is why the read is the truth and the ask is what had to arrive.
	//
	// The asked halves were recorded at the spawn call. This fills the read
	// halves in place, so a light that never spawned keeps its ask and prints
	// nothing-measured for its read rather than a zero that would read as a
	// light aimed at the horizon.
	std::string LightAimNow()
	{
		std::vector<LedgerVignette::LightAim> Aims = GLightAsked;
		ADirectionalLight* const Actors[kDirectionalLights] = { GSun, GFillA, GFillB, GFillC };
		const char* const Names[kDirectionalLights] = { "sun", "fillA", "fillB", "fillC" };
		for (size_t I = 0; I < Aims.size(); ++I)
		{
			for (int K = 0; K < kDirectionalLights; ++K)
			{
				if (Aims[I].Name != Names[K]) { continue; }
				if (Actors[K] == nullptr) { Aims[I].bSpawned = false; break; }
				Aims[I].bSpawned = true;
				if (ULightComponent* LC = Actors[K]->GetLightComponent())
				{
					const FRotator R = LC->GetComponentRotation();
					Aims[I].bRead = true;
					Aims[I].ReadPitch = (double)R.Pitch;
					Aims[I].ReadYaw = (double)R.Yaw;
				}
				break;
			}
		}
		return LedgerVignette::LightAimLine(Aims, kDirectionalLights);
	}

	// ---- the verdict ----------------------------------------------------

	void WriteVerdict(const std::string& DoneLine)
	{
		TArray<FString> Out;
		Out.Add(FString::Printf(TEXT("# UE vignette shot %s @%lld"),
		                        *ShaFromCommandLine(), (long long)FDateTime::UtcNow().ToUnixTimestamp()));
		Out.Add(TEXT("# Line 1 names the commit this was measured on, as the Unity verdict does."));
		Out.Add(TEXT("# THE STREET IS BUILT FROM production/specs/vignette-pieces.json AND NOTHING ELSE."));
		Out.Add(TEXT("#   Nothing here is authored: every position, size and rotation came out of that"));
		Out.Add(TEXT("#   file, which Ledger.Core wrote from the shared scene json. Untextured on"));
		Out.Add(TEXT("#   purpose: materials, the props and the HDRI are Phase C and Phase D."));
		Out.Add(TEXT("# frameMedianMs: MEDIAN of 24 engine frame deltas after 8 discarded warm-up"));
		Out.Add(TEXT("#   frames, in milliseconds. NOT the Unity host's number even though both are a"));
		Out.Add(TEXT("#   median of 24 after 8: Unity times one Camera.Render plus GL.Flush and this"));
		Out.Add(TEXT("#   times a whole engine frame. frameStat on each line names which one it is."));
		Out.Add(TEXT("# shotMeanLuma: mean over EVERY pixel of the committed file, 0 to 1,"));
		Out.Add(TEXT("#   luma=(0.299R+0.587G+0.114B)/255, the same weights the Unity sim uses."));
		Out.Add(TEXT("# shotNonBlackPct: percent of shotPixels with any channel above zero."));
		Out.Add(TEXT("# shotDistinctBuckets: distinct 5-bit-per-channel colour buckets, of 32768."));
		Out.Add(TEXT("# a shot status of WROTE needs a decoded file with more than one bucket and"));
		Out.Add(TEXT("#   at least one non-black pixel. BLANK, UNDECODABLE and NO-FILE are the three"));
		Out.Add(TEXT("#   ways it fails, and the step exits non-zero for all three with the evidence"));
		Out.Add(TEXT("#   still committed."));
		Out.Add(TEXT("# QUEUE 059, THE TWO MEASUREMENTS RUN 17 DID NOT HAVE. Its lantern count read"));
		Out.Add(TEXT("#   four of four and answered `were four lights created`, while both night"));
		Out.Add(TEXT("#   frames were black; its mean luma read 0.5030 over a day frame whose ground"));
		Out.Add(TEXT("#   plane was entirely clipped. Neither number could see it. These can:"));
		Out.Add(TEXT("# shotClipHiAny/shotClipHiAll/shotClipLoAll: COUNTS of pixels at the top and"));
		Out.Add(TEXT("#   bottom of the 8-bit range over shotPixels, never a mean. shotLumaBands is"));
		Out.Add(TEXT("#   eight equal luma bands, band 0 darkest: a printed series, not a bound."));
		Out.Add(TEXT("# band.skyTop / band.skyCentre / band.ground: THREE GEOMETRIC BANDS of THIS"));
		Out.Add(TEXT("#   frame, named for what they COVER and not for what is in them. skyTop is"));
		Out.Add(TEXT("#   the top eighth full width and carries roofline as well as sky; skyCentre"));
		Out.Add(TEXT("#   is the middle fifth of it; ground is the bottom fifth. Each ships its own"));
		Out.Add(TEXT("#   pixel count as its denominator and its own rectangle in pixels, and a"));
		Out.Add(TEXT("#   rectangle covering no pixel reads NOTHING-MEASURED rather than dark."));
		Out.Add(TEXT("#   meanRGB is printed because a sky and a fog inscattering colour are told"));
		Out.Add(TEXT("#   apart by CHANNEL ORDER: before the sky landed, the day far field read"));
		Out.Add(TEXT("#   249.5/250.0/250.5 and the night one 188.4/179.6/179.3, which are the day"));
		Out.Add(TEXT("#   and night fog colours and not a sky. A printed series, not a bound."));
		Out.Add(TEXT("# bandGroundOverSky: one ratio of two measured means. A ground LIT by a sky"));
		Out.Add(TEXT("#   and a ground MIRRORING one both raise it; the ground band's own spread is"));
		Out.Add(TEXT("#   what separates them, because a mirror adds variation and a lamp does not."));
		Out.Add(TEXT("# skyModel / ambientModel: READ BACK off the components after the write. Both"));
		Out.Add(TEXT("#   were hardcoded literals in a format string until 2026-09-09 and one of"));
		Out.Add(TEXT("#   them was false. skyWrites=N/of=M is write-on-change: M is how many times"));
		Out.Add(TEXT("#   ApplyCondition ran and N how many times the sky was rewritten, and N<M is"));
		Out.Add(TEXT("#   the point rather than a fault. skyHdriBoundAs names WHAT THE SKY BOUND"));
		Out.Add(TEXT("#   TO: the approved photograph as a long-lat PNG on an unlit dome, or NOTHING"));
		Out.Add(TEXT("#   and the reason. Those are different readings and one may never print the"));
		Out.Add(TEXT("#   other. The atmosphere and the sky light are unchanged and still light it."));
		Out.Add(TEXT("# shotSunIntensityAsked / shotSkyIntensityAsked: A1(c), 2026-09-09. THE"));
		Out.Add(TEXT("#   VALUE THE CONDITION ROW ASKED FOR, beside the one the component read"));
		Out.Add(TEXT("#   back, with shotCellAgrees per frame and cellAgree=N/of=M once per run."));
		Out.Add(TEXT("#   Run 38 printed five rungs that all read sky 1.000 and one control row at"));
		Out.Add(TEXT("#   0.350 and never printed the cross, so the cell that mattered had never"));
		Out.Add(TEXT("#   been rendered and nothing said so. The repeat shot is excluded from the"));
		Out.Add(TEXT("#   run tally, because it re-photographs shot 0 and would make the"));
		Out.Add(TEXT("#   denominator larger than the shot list."));
		Out.Add(TEXT("# shotExposurePin*: QUEUE 235, 2026-09-10. WHAT EXPOSURE THIS FRAME WAS"));
		Out.Add(TEXT("#   ASKED TO HOLD, BESIDE WHAT THE CAMERA COMPONENT READ BACK, PER SHOT. The"));
		Out.Add(TEXT("#   rate snap of 2026-09-09 did not settle the rig: at speed 10000 the run on"));
		Out.Add(TEXT("#   83dec33 still read rigDeterminism=DIFFERS with 921600 of 921600 pixels"));
		Out.Add(TEXT("#   changed between one camera's first frame and its own repeat. The next lever"));
		Out.Add(TEXT("#   is the VALUE: AutoExposureMinBrightness equal to MaxBrightness leaves the"));
		Out.Add(TEXT("#   histogram nothing to move. asked comes from the CONDITION, exposure_pin in"));
		Out.Add(TEXT("#   the shared file, where 0.0 asks for nothing and is what every condition"));
		Out.Add(TEXT("#   older than this change carries, so AUTO on a row is not a failure. HELD is"));
		Out.Add(TEXT("#   the game thread's agreement and NOT a pixel's: a value written through a"));
		Out.Add(TEXT("#   pointer reads back off that pointer whatever the render proxy did, which is"));
		Out.Add(TEXT("#   why the row's own frame luma rides the same line. The separator is one part"));
		Out.Add(TEXT("#   in a thousand and is NOT a measured tolerance: a float round trip is of"));
		Out.Add(TEXT("#   order 1e-7 and a pin that never landed reads back as the engine default."));
		Out.Add(TEXT("# ladder.pin*: THE SERIES THE PINNED VALUE IS SET FROM, AND IT IS NOT SET IN"));
		Out.Add(TEXT("#   THIS RUN. The value cannot be computed from anything committed: shotMeanLuma"));
		Out.Add(TEXT("#   is the mean of a tonemapped 8-bit frame and the pin is a scene-luminance"));
		Out.Add(TEXT("#   input read before the tonemap, with no arithmetic joining them, and the"));
		Out.Add(TEXT("#   adapted exposure is a render-thread quantity this process never reads. So"));
		Out.Add(TEXT("#   four rungs bracket the engine's own default clamp range and EVERY RUNG IS"));
		Out.Add(TEXT("#   PHOTOGRAPHED TWICE, once after a night frame and once after a day frame,"));
		Out.Add(TEXT("#   because the fault under test is a frame coming out blown because the one"));
		Out.Add(TEXT("#   before it was dark. afterDay and afterNight name the frame photographed"));
		Out.Add(TEXT("#   IMMEDIATELY BEFORE the row, read off the shot loop and never off the row's"));
		Out.Add(TEXT("#   name. The pairing prints as a signed DIFFERENCE, never a ratio, because"));
		Out.Add(TEXT("#   this tonemap is monotone and not linear. ladderSmallestDiffPin NAMES the"));
		Out.Add(TEXT("#   smallest and calls nothing agreement: a bound on that difference has not"));
		Out.Add(TEXT("#   been measured, so ladderVerdict stays SERIES-ONLY and a later commit sets"));
		Out.Add(TEXT("#   the number. Both clip counts ride each rung with their denominators,"));
		Out.Add(TEXT("#   because a mean cannot see a blown frame and a value chosen on the mean"));
		Out.Add(TEXT("#   alone would crush or blow one end of the run."));
		Out.Add(TEXT("# expPin*: the run's tally, with the cost of the pin on the line. A PINNED"));
		Out.Add(TEXT("#   FRAME CAN NEVER JUDGE AN ADAPTATION MOMENT, walking out of a dark alley"));
		Out.Add(TEXT("#   being the example, and expPinConstantSet=no says this run printed the"));
		Out.Add(TEXT("#   series and chose nothing from it."));
		Out.Add(TEXT("# lightAim*: A6, 2026-09-09. EVERY DIRECTIONAL LIGHT'S ASKED ROTATION BESIDE"));
		Out.Add(TEXT("#   THE ONE ITS COMPONENT READS BACK, with the signed residual per axis to"));
		Out.Add(TEXT("#   four decimals. The spec has asked for a sun at pitch -36.0 since it was"));
		Out.Add(TEXT("#   written and this rig rendered -82.0 on every run: the arithmetic was"));
		Out.Add(TEXT("#   tested, the format string was tested, and nothing tested that the number"));
		Out.Add(TEXT("#   reached the light. lightAimStatus=AGREES is the only passing word and the"));
		Out.Add(TEXT("#   step refuses on anything else WITH THIS FILE STILL COMMITTED. The bound"));
		Out.Add(TEXT("#   is 1.0 degree and it is NOT a measured tolerance: it separates the 46.0"));
		Out.Add(TEXT("#   fault from a float round trip of order 1e-4. A residual printed between"));
		Out.Add(TEXT("#   0.001 and 1.0 is what a real bound would then be read off."));
		Out.Add(TEXT("# light lines: one per probed light, the SAME camera, condition and frame"));
		Out.Add(TEXT("#   counts as its shot with that one light switched off. deltaMeanFull is the"));
		Out.Add(TEXT("#   whole frame, deltaMeanPeak is the named grid cell in peakRegion, and both"));
		Out.Add(TEXT("#   halves of every difference are printed beside it (meanOn.. and meanOff..)."));
		Out.Add(TEXT("# THE CONTROL LINE TOGGLES NOTHING and is this run's own noise floor. A"));
		Out.Add(TEXT("#   lantern whose histogram does not clear the control's did not light the"));
		Out.Add(TEXT("#   frame. No threshold is set here: read the series, set the bound after."));
		Out.Add(TEXT("# NO BOUND IN THIS RUN. lampGain and fogGain are unchanged first values and"));
		Out.Add(TEXT("#   the picture is not to be fixed before it is measured."));
		Out.Add(TEXT("# PHASE C, MATERIALS. One surface line per surface the shared file asked for,"));
		Out.Add(TEXT("#   with what each map LOADED AS rather than what its filename claims, and the"));
		Out.Add(TEXT("#   candidates tried for every map that is not there. The base material is a"));
		Out.Add(TEXT("#   BUILD PRODUCT made by tools/ue/make_base_material.py in the cook step: no"));
		Out.Add(TEXT("#   human opens the editor, which is D1 measurement (a) in one line."));
		Out.Add(TEXT("#   materialBase reads MISSING when the cook did not carry the asset, and"));
		Out.Add(TEXT("#   every surface below is then untextured however many maps decoded."));
		Out.Add(TEXT("# PHASE C, THE READBACK. Each surface line carries what the material"));
		Out.Add(TEXT("#   instance answered when asked for the texture and the two tiling"));
		Out.Add(TEXT("#   scalars straight back, and the materials line carries the run's"));
		Out.Add(TEXT("#   totals over the surfaces a parameter was actually set on. It is the"));
		Out.Add(TEXT("#   GAME thread's copy: a value that lands there and never reaches the"));
		Out.Add(TEXT("#   render proxy still reads back as the same pointer."));
		Out.Add(TEXT("# PHASE C, THE CONTROL QUADS. Three planes of one size at one distance"));
		Out.Add(TEXT("#   in front of the first shot's camera, off the same base material,"));
		Out.Add(TEXT("#   carrying no street data. The first binds a 2x2 texture built in code"));
		Out.Add(TEXT("#   from four saturated colours, with no file and no decode; the other"));
		Out.Add(TEXT("#   two bind no texture at all and differ only in their tiling scalars."));
		Out.Add(TEXT("#   Four colours on the first means a texture override reaches the"));
		Out.Add(TEXT("#   sampler. Two different cell counts on the other two means the scalar"));
		Out.Add(TEXT("#   overrides reach the shader. THE FRAME IS WHAT ANSWERS, not a count:"));
		Out.Add(TEXT("#   the quad lines say only where to look and what was asked for."));
		Out.Add(TEXT("#   The controls occupy their printed boxes, so any whole-frame statistic"));
		Out.Add(TEXT("#   taken from this run includes them and must exclude those boxes first."));
		Out.Add(TEXT("# QUEUE 208, THE CAMERA. shotCamId and the asked-against-read pose ride"));
		Out.Add(TEXT("#   EACH SHOT LINE, because the camera a frame was taken from is a"));
		Out.Add(TEXT("#   per-sample fact. The one-per-run shotCam line keeps only what is true"));
		Out.Add(TEXT("#   of the run: that a camera actor exists, and the map it is in. It used"));
		Out.Add(TEXT("#   to carry the pose, last-wins, and tools/frame-shadow-probe.py refused"));
		Out.Add(TEXT("#   every frame whose camera was not the last one the run placed."));
		Out.Add(TEXT("# THE RIG LINE, rigDeterminism, IS THIS RUN ASKING WHETHER IT CAN BE"));
		Out.Add(TEXT("#   COMPARED AT ALL. The first shot's camera and condition are"));
		Out.Add(TEXT("#   photographed again as the last thing the run does, to a scratch file"));
		Out.Add(TEXT("#   that is not committed, and rigDiffPixels is the count of pixels that"));
		Out.Add(TEXT("#   differ over the whole frame. There is no epsilon: identical inputs"));
		Out.Add(TEXT("#   must be the same picture, so the honest bound is zero. Anything else"));
		Out.Add(TEXT("#   means a cross-shot luma comparison in this run is partly a comparison"));
		Out.Add(TEXT("#   of the rig. The eye adaptation SPEEDS are the one thing this probe"));
		Out.Add(TEXT("#   overrides, named on the tonemap line; the exposure VALUE is still the"));
		Out.Add(TEXT("#   engine's own, so a still is still the level a player would settle at."));
		Out.Add(TEXT("# QUEUE 223, THE THIRTY PIECES NOTHING PAINTED. Until this run a piece"));
		Out.Add(TEXT("#   whose surface did not resolve to a pack file got no material instance"));
		Out.Add(TEXT("#   at all and rendered the engine default: ten card decals, ten multiply"));
		Out.Add(TEXT("#   decals, six shop interiors and four runs of yellow road paint. Four"));
		Out.Add(TEXT("#   routes now paint a piece and the census is on the materials line:"));
		Out.Add(TEXT("#   piecesPainted, piecesUnpainted, paintRoutes and paintUnpaintedWhy,"));
		Out.Add(TEXT("#   over the pieces the loop EXAMINED and not over what the file asked"));
		Out.Add(TEXT("#   for. pack is the twelve surfaces the pack answers for; tint is"));
		Out.Add(TEXT("#   interior and paint_yellow, built in code from the SurfaceSpec tint"));
		Out.Add(TEXT("#   because one is ProceduralOnly in the Unity host and the other has no"));
		Out.Add(TEXT("#   pack file; decal-card is the piece's own picture, cropped at decode."));
		Out.Add(TEXT("#   THE INTERIOR WEARS THE WINDOW'S NORMAL AND ROUGHNESS, which is the"));
		Out.Add(TEXT("#   Unity host's own rule, and a borrowed map is named on the surface"));
		Out.Add(TEXT("#   line and counted APART from a found one: mapsFound still means this"));
		Out.Add(TEXT("#   surface's own candidate answered."));
		Out.Add(TEXT("# THE MULTIPLY DECALS ARE HIDDEN AND SAY SO. A stain is a material blend"));
		Out.Add(TEXT("#   mode, not an instance parameter, and this build ships one opaque base"));
		Out.Add(TEXT("#   material, so the grime cannot be drawn here yet. Hiding is the Unity"));
		Out.Add(TEXT("#   host's own rule for a decal whose image does not load, and it is the"));
		Out.Add(TEXT("#   lesser of the two wrongs: ten grey rectangles in the carriageway are"));
		Out.Add(TEXT("#   louder in a judged frame than ten absent stains. The pair differs by"));
		Out.Add(TEXT("#   the grime until that material exists, and decalsMultiplyNote says so."));
		Out.Add(TEXT("# THE CARD DECALS ARE CROPPED AT DECODE AND NOT BY AN ST PAIR. The base"));
		Out.Add(TEXT("#   material has tiling scalars and no uv offset, so the rectangle the"));
		Out.Add(TEXT("#   asset string carries is cut out of the decoded buffer instead. The"));
		Out.Add(TEXT("#   crop's v is measured from the BOTTOM and image rows arrive top down;"));
		Out.Add(TEXT("#   that flip is in CropPixels, which g++ runs here before dispatch, and"));
		Out.Add(TEXT("#   decalRowOrder on every decal line names which way round it went."));
		Out.Add(TEXT("#   WHAT NO NUMBER HERE CAN SEE is whether the engine's plane carries the"));
		Out.Add(TEXT("#   same uv winding as the Unity quad, so a lettered fascia could arrive"));
		Out.Add(TEXT("#   mirrored. The frame is what answers that, and the answer is one"));
		Out.Add(TEXT("#   character in SurfaceBind.h if it is wrong."));
		Out.Add(TEXT("# NO COMMENT IN THIS HEADER WRITES A KEY WITH AN EQUALS AND A VALUE."));
		Out.Add(TEXT("#   Run 19 spelled this key out with MISSING beside it up here and"));
		Out.Add(TEXT("#   measured it as loaded down there, which tools/verdict-dupkeys.py"));
		Out.Add(TEXT("#   reads as one key with two values in one run. Every reader here"));
		Out.Add(TEXT("#   greps, and one of them takes the FIRST match. Keys are named in"));
		Out.Add(TEXT("#   prose above and measured below, never both."));
		Out.Add(TEXT(""));
		Out.Add(FString(UTF8_TO_TCHAR(SceneLineWithSky().c_str())));
		Out.Add(GCamLine);
		Out.Add(GToneLine);
		if (GShotLines.empty())
		{
			Out.Add(TEXT("NOTHING MEASURED - no shot reached the measuring step on this commit."));
		}
		else
		{
			for (size_t I = 0; I < GShotLines.size(); ++I)
			{
				Out.Add(FString(UTF8_TO_TCHAR(GShotLines[I].c_str())));
			}
		}
		for (size_t I = 0; I < GBinds.size(); ++I)
		{
			Out.Add(FString(UTF8_TO_TCHAR(LedgerSurface::SurfaceLine(GBinds[I]).c_str())));
		}
		if (GBinds.empty())
		{
			Out.Add(TEXT("# no surface line: the material pass did not reach a surface."));
		}
		// THE RE-DRIVE'S TALLIES ARE APPENDED HERE AND NOT BUILT INTO
		// GMaterialsLine, AND THE REASON IS A TIMING ONE. That line is
		// composed at the end of BindSurfaces, which runs inside BuildScene
		// before any condition has been applied, so a re-drive count built
		// there would read 0 walks of 0 calls on every run for ever: stale
		// rather than wrong in a way anybody could see. This is the same
		// reason SkySegmentNow is taken when a verdict asks for the line.
		// AND THE LAMP DRIVE'S TALLIES WITH THEM, QUEUE 333, FOR THE SAME
		// TIMING REASON: GMaterialsLine is composed at the end of
		// BindSurfaces, which runs before any condition has been applied, so
		// a lamp-drive count built there would read 0 walks of 0 calls on
		// every run for ever.
		Out.Add(FString(UTF8_TO_TCHAR(
			(GMaterialsLine + LedgerSurface::WetRedriveSegment(GWetRedrive)
			 + LampDriveSegment()
			 + LedgerVignette::SkyLumDriveSegment(
			       GSkyLumDrive, (double)kSkyLuminanceGain)).c_str())));
		// THE DECALS, AFTER THE SURFACES, because card and multiply appear on
		// both: as two surface names that are NOT library surfaces, and here as
		// twenty pieces each carrying its own picture. A cap on the lines would
		// announce itself; there are twenty pieces and twenty lines, so nothing
		// is capped and nothing has to say so.
		for (size_t I = 0; I < GDecalResults.size(); ++I)
		{
			Out.Add(FString(UTF8_TO_TCHAR(
				LedgerSurface::DecalLine(GDecalResults[I]).c_str())));
		}
		if (GDecalResults.empty())
		{
			Out.Add(TEXT("# no decal line: the material pass reached no decal piece."));
		}
		Out.Add(FString(UTF8_TO_TCHAR(GDecalsLine.c_str())));
		// THE CONTROLS, AFTER THE SURFACES THEY ARE THE CONTROL FOR. One line
		// per quad with its own placement and where it should land on the
		// frame, then the pass's own totals. A run that spawned none of them
		// still prints the done line, which says so in words.
		for (size_t I = 0; I < GQuadLines.size(); ++I)
		{
			Out.Add(FString(UTF8_TO_TCHAR(GQuadLines[I].c_str())));
		}
		if (GQuadLines.empty())
		{
			Out.Add(TEXT("# no control quad line: the control pass reached no quad."));
		}
		Out.Add(FString(UTF8_TO_TCHAR(GQuadDone.c_str())));
		// AND WHETHER THE CONTROLS WERE IN THE FRAME OR NOT, per shot,
		// formatted in the tested header.
		Out.Add(FString(UTF8_TO_TCHAR(LedgerSurface::ControlQuadVisibilityLine(
			GQuadShotsSeen, GQuadHidden, GQuadHiddenIds).c_str())));
		if (GLightLines.empty())
		{
			Out.Add(TEXT("# no light was probed on this commit; the pass line below says why."));
		}
		else
		{
			for (size_t I = 0; I < GLightLines.size(); ++I)
			{
				Out.Add(FString(UTF8_TO_TCHAR(GLightLines[I].c_str())));
			}
		}
		// QUEUE 326: ONE FLOOR LINE PER PROBED SHOT, BEFORE THE RUN LINE THAT
		// REDUCES THEM. Per-shot counts on the per-shot line; the run's own
		// counts on the done line. A run that probed no shot prints the words
		// rather than leaving the reader to read absence as agreement.
		for (size_t I = 0; I < GFloors.size(); ++I)
		{
			Out.Add(FString(UTF8_TO_TCHAR(LedgerFrame::LightFloorLine(GFloors[I]).c_str())));
		}
		if (GFloors.empty())
		{
			Out.Add(TEXT("# no lightfloor line: no shot ran a light-probe floor pass on this "
			             "commit; lightsAboveFloor below says nothing-measured."));
		}
		Out.Add(FString(UTF8_TO_TCHAR(LedgerFrame::LightProbeDoneLine(
			GProbed, GEligible, GFloors, GSkippedOff, GSkippedBudget, GProbeNoFile,
			GRestoreMismatch, GShotsProbed, (int)GSpec.Shots.size(),
			kLightProbeBudgetSeconds, GProbeSpent,
			kWarmFrames + kTimedFrames, GControls,
			// QUEUE 329: THE PROBE'S OWN FRAME TALLY, WHICH THIS CALL DID NOT
			// PASS. The parameter is defaulted, so the omission compiled and
			// printed lightProbesBlank=nothing-measured on a run that decoded
			// 48 probe frames and found nine of them blank. A false nothing
			// measured is worse than a missing key: it reads as an absence
			// somebody checked.
			GProbeFrames).c_str())));
		// A1(c) AND CONDITION C5: DID EVERY CELL READ BACK WHAT IT ASKED FOR.
		// A whole-run count over the shots whose components answered, beside
		// the per-sample shotCellAgrees word each shot line carries.
		Out.Add(FString(UTF8_TO_TCHAR(LedgerVignette::CellAgreeLine(
			(int)GCellsAgree, (int)GCellsRead, (int)GSpec.Shots.size()).c_str())));
		// C4 AS AMENDED, AND AMENDMENT 2'S ENGINE FORM: THE NOISE FLOOR IS A
		// SPREAD OVER EVERY FRAME THIS ENGINE RENDERS IDENTICALLY AT ONE
		// CAMERA, with its denominator, its extreme pair named, the one-pair
		// drift in shot order beside it, and the grid's smallest sky step to
		// read it against. A whole-run line, because every number on it is a
		// statistic OVER the run's frames and none is true of one frame.
		Out.Add(FString(UTF8_TO_TCHAR(
			LedgerVignette::NullSeriesLine(GFrameSamples).c_str())));
		// A6: WHERE THE FOUR DIRECTIONAL LIGHTS WERE AIMED, ASKED BESIDE READ.
		// A WHOLE-RUN LINE, because the rotation is written once at spawn and
		// never rewritten, and it sits beside the other whole-run lines for
		// the same reason. lightAimStatus is the key the CI step refuses on.
		Out.Add(FString(UTF8_TO_TCHAR(LightAimNow().c_str())));
		// QUEUE 235: THE EXPOSURE LADDER AND THE RUN'S PIN TALLY, IMMEDIATELY
		// BEFORE THE DETERMINISM LINE THEY EXIST TO REPAIR. The ladder is the
		// series the pinned value was read off; the run line says how many
		// rows asked for a pin, how many held it, HOW MANY WERE PHOTOGRAPHED
		// AT AN EXPOSURE NOBODY ASKED FOR, and where the live value came from.
		Out.Add(FString(UTF8_TO_TCHAR(
			LedgerVignette::ExposureLadderLine(GLadder).c_str())));
		{
			LedgerVignette::ExposurePinRun PinRun;
			PinRun.RowsAsking  = (int)GPinAsking;
			PinRun.RowsHeld    = (int)GPinHeld;
			PinRun.RowsRead    = (int)GPinRead;
			PinRun.RowsLeaked  = (int)GPinLeaked;
			PinRun.RowsOffered = (int)GSpec.Shots.size();
			// THE CONDITION HALF IS COUNTED OFF THE SPEC, not off the shots:
			// a condition carrying a pin and a shot taking one are different
			// facts and a run can photograph none of the conditions that
			// carry one.
			PinRun.CondsWithPin = LedgerVignette::ConditionsCarryingAPin(GSpec.Conditions);
			PinRun.CondsOffered = (int)GSpec.Conditions.size();
			PinRun.Provenance   = GSpec.ExposurePinProvenance;
			Out.Add(FString(UTF8_TO_TCHAR(
				LedgerVignette::ExposurePinDoneLine(PinRun).c_str())));
		}
		// THE RIG'S OWN DETERMINISM, BESIDE THE PASS SUMMARIES IT QUALIFIES.
		Out.Add(FString(UTF8_TO_TCHAR(GRigLine.c_str())));
		Out.Add(FString(UTF8_TO_TCHAR(DoneLine.c_str())));
		if (!GArt.empty())
		{
			Out.Add(TEXT("# ascii-luma of the FIRST frame that decoded, 48x27 cells, top row first."));
			Out.Add(FString(UTF8_TO_TCHAR(GArt.c_str())));
		}
		Out.Add(TEXT("shotReached=end"));
		const FString Body = FString::Join(Out, TEXT("\n")) + TEXT("\n");
		FFileHelper::SaveStringToFile(Body, *AbsProject(TEXT("ue-vignette-verdict.txt")));
		FFileHelper::SaveStringToFile(Body, *FPaths::Combine(
			FPaths::GetPath(FPlatformProcess::ExecutablePath()), TEXT("ue-vignette-verdict.txt")));
	}

	void Finish(const std::string& DoneLine)
	{
		GPhase = EPhase::Done;
		WriteVerdict(DoneLine);
		// THE PROBE'S SCRATCH FRAME IS NOT EVIDENCE AND DOES NOT SURVIVE THE
		// RUN. Scoped to exactly the two files these passes wrote, by name.
		IFileManager::Get().Delete(*AbsProject(kProbePngLeaf), false, true, true);
		IFileManager::Get().Delete(*AbsProject(kRepeatPngLeaf), false, true, true);
		FPlatformMisc::RequestExit(false);
	}

	void FinishNormally()
	{
		Finish(CaptureDoneLine(GWrote, (int)GSpec.Shots.size(), GBlank, GNoFile,
		                       FPlatformTime::Seconds() - GStart, GTicks));
	}

	bool DecodeBgra(const FString& PngPath, TArray64<uint8>& OutBgra, int32& OutW, int32& OutH,
	                std::string& OutNote)
	{
		TArray<uint8> Compressed;
		if (!FFileHelper::LoadFileToArray(Compressed, *PngPath) || Compressed.Num() == 0)
		{
			OutNote = "file-would-not-load-or-was-empty";
			return false;
		}
		IImageWrapperModule* Mod =
			FModuleManager::Get().LoadModulePtr<IImageWrapperModule>(FName("ImageWrapper"));
		if (Mod == nullptr) { OutNote = "imagewrapper-module-missing"; return false; }
		TSharedPtr<IImageWrapper> Wrapper = Mod->CreateImageWrapper(EImageFormat::PNG);
		if (!Wrapper.IsValid()) { OutNote = "no-png-wrapper"; return false; }
		if (!Wrapper->SetCompressed(Compressed.GetData(), (int64)Compressed.Num()))
		{
			OutNote = "setcompressed-refused-the-bytes";
			return false;
		}
		OutW = Wrapper->GetWidth();
		OutH = Wrapper->GetHeight();
		if (OutW <= 0 || OutH <= 0) { OutNote = "decoded-size-was-zero"; return false; }
		if (!Wrapper->GetRaw(ERGBFormat::BGRA, 8, OutBgra)) { OutNote = "getraw-refused"; return false; }
		return OutBgra.Num() >= (int64)OutW * (int64)OutH * 4;
	}

	// A FILE THAT EXISTS IS NOT A FILE THAT IS FINISHED. Two consecutive
	// polls agreeing on a non-zero size is the cheap version of waiting for
	// the writer and it costs one frame.
	bool SizeSettled(const FString& Path, int64& Tracker)
	{
		const int64 Size = IFileManager::Get().FileSize(*Path);
		if (Size <= 0) { Tracker = -1; return false; }
		const bool bSame = (Size == Tracker);
		Tracker = Size;
		return bSame;
	}

	FString NewestPngUnder(const FString& Dir, int32& OutCount)
	{
		TArray<FString> Found;
		IFileManager::Get().FindFilesRecursive(Found, *Dir, TEXT("*.png"), true, false, false);
		OutCount = Found.Num();
		FString Best;
		FDateTime BestTime = FDateTime::MinValue();
		for (const FString& F : Found)
		{
			const FDateTime T = IFileManager::Get().GetTimeStamp(*F);
			if (Best.IsEmpty() || T > BestTime) { Best = F; BestTime = T; }
		}
		return Best;
	}

	// ---- queue 059 (a): the lights this pass can ask about ---------------
	//
	// ONE ORDER, ONE PLACE. The lanterns first and the practicals after, and
	// every accessor below reads that one order, so a light's index on its
	// verdict line and the light this code toggled cannot drift apart.
	int32 ProbeTargetCount()
	{
		return GLanterns.Num() + GWindows.Num();
	}

	APointLight* ProbeLight(int32 I)
	{
		if (I < 0) { return nullptr; }
		if (I < GLanterns.Num()) { return GLanterns[I]; }
		const int32 J = I - GLanterns.Num();
		return (J < GWindows.Num()) ? GWindows[J] : nullptr;
	}

	std::string ProbeId(int32 I)
	{
		if (I >= 0 && I < GLanterns.Num())
		{
			return (size_t)I < GLanternNames.size() ? GLanternNames[(size_t)I]
			                                        : std::string("lantern-unnamed");
		}
		const int32 J = I - GLanterns.Num();
		if (J >= 0 && (size_t)J < GWindowNames.size()) { return GWindowNames[(size_t)J]; }
		return std::string("light-unnamed");
	}

	const char* ProbeKind(int32 I)
	{
		return (I < GLanterns.Num()) ? "lantern" : "practical";
	}

	// A SHOT IS PROBED IF ITS CONDITION HAS ANY OF THESE LIGHTS ON. Probing a
	// condition that turned the lanterns off would measure a difference of
	// zero and print it beside the word lantern, which is exactly the false
	// reading this item exists to stop.
	bool ShouldProbeShot(const Shot& S)
	{
		const Condition* C = FindCondition(S.ConditionId);
		if (C == nullptr) { return false; }
		return (C->LanternsOn && GLanterns.Num() > 0) || (C->WindowsOn && GWindows.Num() > 0);
	}

	// WHAT THE TWO LIGHTS WERE WHILE THIS FRAME STOOD, QUEUE 205.
	//
	// Called from MeasureShot, which runs after the screenshot and before
	// the next condition is applied, so these are readings of the light
	// that took the picture. The scene line's sun keys are one-per-run and
	// last-wins; a ladder renders six conditions in one run, so without
	// this five of its six frames would carry no component reading at all
	// and a rung could only be attributed by trusting a data file.
	// A1(c): THE ASK COMES FROM THE CONDITION THIS FRAME WAS PHOTOGRAPHED
	// UNDER, looked up by the shot's own condition id rather than taken from
	// whatever was applied last. The value applied last would be the same on a
	// well-behaved run and the point of the key is the run that is not one.
	std::string ShotLightNow(const Shot& S)
	{
		double SunAsked = 0.0, SkyAsked = 0.0;
		if (const Condition* C = FindCondition(S.ConditionId))
		{
			SunAsked = C->SunIntensity;
			SkyAsked = C->SkyIntensity;
		}
		bool bSunComp = false, bCast = false, bSkyComp = false;
		double Intensity = 0.0, Pitch = 0.0, Yaw = 0.0, SkyIntensity = 0.0;
		int Mobility = -1;
		if (GSun != nullptr)
		{
			if (ULightComponent* LC = GSun->GetLightComponent())
			{
				bSunComp     = true;
				Intensity    = (double)LC->Intensity;
				bCast        = (LC->CastShadows != 0);
				const FRotator R = LC->GetComponentRotation();
				Pitch        = (double)R.Pitch;
				Yaw          = (double)R.Yaw;
				Mobility     = (int)LC->Mobility.GetValue();
			}
		}
		if (GSky != nullptr)
		{
			if (USkyLightComponent* SC = GSky->FindComponentByClass<USkyLightComponent>())
			{
				bSkyComp     = true;
				SkyIntensity = (double)SC->Intensity;
			}
		}
		// THE TALLY IS COUNTED HERE AND NOWHERE ELSE, so the per-sample word
		// and the whole-run count cannot disagree: both come from
		// LedgerVignette::CellAgrees.
		if (bSunComp && bSkyComp && !GRepeating)
		{
			++GCellsRead;
			if (LedgerVignette::CellAgrees(SunAsked, Intensity)
			    && LedgerVignette::CellAgrees(SkyAsked, SkyIntensity))
			{
				++GCellsAgree;
			}
		}
		return LedgerVignette::ShotLightLine(bSunComp, SunAsked, Intensity, bCast, Pitch, Yaw,
		                                     Mobility, bSkyComp, SkyAsked, SkyIntensity);
	}

	// ---- QUEUE 208 AND THE CAPTURE PATH, ON EVERY SHOT LINE -------------
	//
	// ONE PRODUCER FOR BOTH, because a shot line assembled twice drifts the
	// moment either half changes, and all four of MeasureShot's exits print
	// it. The camera segment is formatted in the tested header; the capture
	// path is the one word that says WHICH of the two screenshot candidates
	// wrote this file, which was invisible before: GUseHighRes is adopted for
	// the whole run the first time candidate A writes nothing, so a run can
	// hold frames from two different capture paths and only the shot that
	// switched carries a note about it.
	std::string ShotCamAndCaptureNow()
	{
		return LedgerVignette::ShotCamSegment(GShotCam)
		     + " shotCaptureVia=" + GCaptureVia
		     + " shotCaptureViaStat=per-sample/the-path-is-adopted-run-wide-once-candidate-A-fails-once"
		     + " " + LedgerFrame::CaptureTimingSegment(
		         (int)GWarmTicksAtAsk, (int)kWarmFrames,
		         (int)GTimedAtAsk, (int)kTimedFrames,
		         GSecondsToSettle, GCaptureSettled);
	}

	// WHAT EXPOSURE THIS FRAME WAS ASKED TO HOLD AND WHAT THE COMPONENT SAID,
	// QUEUE 235. PURE: the tally is taken once per shot at the top of
	// MeasureShot, not here, because a formatter that counts is a formatter
	// that counts twice the day something calls it twice. The string itself is
	// in VignetteSpec.h, where g++ runs it before any dispatch.
	std::string ExposurePinNow()
	{
		return LedgerVignette::ExposurePinSegment(GShotPin);
	}

	// ONE LADDER ROW, RECORDED FROM EVERY PATH THAT ENDS A SHOT, QUEUE 235.
	//
	// A ROW WHOSE FRAME NEVER LANDED IS STILL A ROW THE FILE ASKED FOR. Left
	// out, `ladderRows=4/of=4` would read as a complete ladder over the four
	// rows that happened to survive, which is a denominator smaller than the
	// set examined and the exact shape rule 3b refuses. So the failing paths
	// record the row with bMeasured false and no luma, and the ladder line
	// counts it in the denominator and outside the reading.
	void NoteLadderRow(const std::string& ShotId, bool bAfterNight, bool bMeasured,
	                   double MeanLuma, long long ClipHi, long long ClipLo, long long Pixels)
	{
		if (!LedgerVignette::ExposurePinAsked(GShotPin.Asked)) { return; }
		LedgerVignette::ExposureLadderSample LS;
		LS.ShotId      = ShotId;
		LS.Pin         = GShotPin.Asked;
		LS.bAfterNight = bAfterNight;
		LS.bMeasured   = bMeasured;
		LS.bPinHeld    = LedgerVignette::ExposurePinHeld(GShotPin);
		LS.MeanLuma    = MeanLuma;
		LS.ClipHi      = ClipHi;
		LS.ClipLo      = ClipLo;
		LS.Pixels      = Pixels;
		GLadder.push_back(LS);
	}

	// A1(d), AMENDMENT 1 OF THE BATCH REVIEW: WHETHER THIS LINE'S OWN
	// WHOLE-FRAME KEYS INCLUDE THE INSTRUMENT. Every string and every
	// projection is in SurfaceBind.h where the test runs; this supplies the
	// camera, the control camera's identity, how many quad actors the build
	// spawned, and whether this line carries whole-frame keys at all. A line
	// written because no file landed carries none, and says so rather than
	// making a claim about a frame that does not exist.
	std::string ShotControlQuadsNow(const Shot& S, bool bWholeFrameKeysOnThisLine)
	{
		const Camera* C = FindCamera(S.CameraId);
		if (C == nullptr)
		{
			return std::string("shotWholeFrameIncludesControlQuads=nothing-measured"
			                   "/no-camera-of-that-id-in-the-spec");
		}
		const Camera* QuadCam = ControlCamera();
		return LedgerSurface::ShotControlQuadLine(
			*C, QuadCam != nullptr ? QuadCam->Id : std::string(),
			(int)GQuadActors.Num(), bWholeFrameKeysOnThisLine, kShotW, kShotH);
	}

	// ---- QUEUE 333: IS THE LAMP THE BRIGHTEST WARM THING IN ITS CORNER ---
	//
	// ON EVERY SHOT LINE, RULED 2026-09-16 SECTION 3.4, and the reason is
	// the whole acceptance sentence. ShouldProbeShot is true only when the
	// condition has lanterns or practicals on, so a segment that printed
	// only on probed shots could never produce the DAY row that refutes it,
	// and "no at day, yes at night, in one run" is what this item is
	// accepted on. A prediction that cannot be reached is not a prediction.
	//
	// AND ON THE TWO EXITS WITH NO FRAME BEHIND THEM TOO, where the tested
	// formatter prints its nothing-measured branch with inFile beside it: a
	// shot whose file never landed MEASURED NOTHING, which is a different
	// fact from a lantern that came out dark, and the line has to say which.
	//
	// NOTHING IS DECIDED HERE. The rectangle is LedgerSurface::
	// PieceScreenBox and the pixels, the yes-or-no comparison, the three
	// denominators and every printed string are LedgerFrame's, both in
	// headers g++ compiles and runs before this file is built. This supplies
	// membership (which pieces are emissive), order (the file's own) and
	// live state (the camera and the frame just decoded).
	std::string LampGlowNow(const Shot& S, const unsigned char* Bgra, int W, int H)
	{
		const int InFile = LedgerVignette::EmissiveCount(GSpec.Pieces);
		const bool bDecoded = (Bgra != nullptr && W > 0 && H > 0);
		std::vector<LedgerFrame::LampPatch> Patches;
		// THE CAMERA THE FILE NAMES FOR THIS ROW, not the camera the world
		// happens to be standing at: the projection is a model of where the
		// solid SHOULD land taken from the same file the frame was shot
		// from. A row naming a camera that is not in the file contributes no
		// patch and the segment says so with examined=0 beside inFile.
		const Camera* C = bDecoded ? FindCamera(S.CameraId) : nullptr;
		if (C != nullptr)
		{
			for (size_t I = 0; I < GSpec.Pieces.size(); ++I)
			{
				const Piece& Pc = GSpec.Pieces[I];
				if (!Pc.Emissive) { continue; }
				const LedgerSurface::ScreenBox Box =
					LedgerSurface::PieceScreenBox(*C, Pc, W, H);
				Patches.push_back(LedgerFrame::MeasureLampPatch(
					Bgra, W, H, Pc.Name, Box.bMeasured,
					Box.X0, Box.Y0, Box.X1, Box.Y1));
			}
		}
		// NO CAP, AND THAT IS A DECISION WITH A REASON rather than an
		// oversight. MaxShown of 0 or less means no cap; the file carries
		// four emissive pieces today, so a cap would be a number nobody has
		// measured (rule 2) standing in front of a list of four. The cap
		// announces itself either way: lampGlowShown/notShown prints on
		// every line whether or not it bites, so the day the file grows is
		// visible in the line rather than in a silence.
		return LedgerFrame::LampGlowSegment(Patches, InFile, bDecoded, 0);
	}

	// MEASURE THE FILE THAT IS ABOUT TO BE COMMITTED, not the buffer the
	// engine had in memory, and let the maths and the string come from the
	// tested header.
	void MeasureShot(const Shot& S, const FString& PngPath, bool bHaveFile)
	{
		// THE PIN TALLY IS TAKEN ONCE PER SHOT, HERE, ABOVE EVERY EARLY
		// RETURN. A row whose frame never landed still asked for an exposure
		// and still read one back, and leaving it out of the denominator would
		// turn a run that lost frames into a run that held every pin.
		// PESSIMISTIC UNTIL THE FRAME IS MEASURED, so a shot whose file never
		// landed cannot leave the PREVIOUS shot's answer standing under this
		// shot's name. Set for real below, where the frame is measured.
		GRefBlank = true;
		bool bAfterNight = false;
		if (!GRepeating)
		{
			if (GShotPin.bRead) { ++GPinRead; }
			if (LedgerVignette::ExposurePinAsked(GShotPin.Asked))
			{
				++GPinAsking;
				if (LedgerVignette::ExposurePinHeld(GShotPin)) { ++GPinHeld; }
			}
			// AND THE ROWS THAT ASKED FOR NOTHING AND GOT SOMEBODY ELSE'S
			// EXPOSURE. Counted here, above every early return, for the same
			// reason the other three are: a row whose frame never landed was
			// still photographed at whatever the component carried.
			else if (LedgerVignette::ExposurePinLeaked(GShotPin)) { ++GPinLeaked; }
			// WHAT THIS ROW FOLLOWED, READ BEFORE THE MEMORY MOVES ON. The
			// pairing is the measurement and the predecessor is read off the
			// shot loop, never off the row's name.
			bAfterNight = GPrevShotExists && !GPrevShotWasDay;
			// AND THE MEMORY MOVES HERE, ABOVE EVERY EARLY RETURN, because a
			// shot whose FILE never landed still rendered its condition for
			// the fifty-six frames before the shutter: what the adaptation
			// saw is the scene, not the file.
			GPrevShotWasDay = GShotPin.bSunOn;
			GPrevShotExists = true;
		}
		const double VFov = FindCamera(S.CameraId) ? FindCamera(S.CameraId)->FovVerticalDeg : 0.0;
		const double HFov = HorizontalFovDeg(VFov, kShotW, kShotH);
		const double Median = MedianMs(GFrameMs);
		if (!bHaveFile)
		{
			++GNoFile;
			GShotLines.push_back(ShotLine(S.Id, S.CameraId, S.ConditionId, GEyeY,
				TCHAR_TO_UTF8(*GCamEdge), Median, kTimedFrames, kWarmFrames,
				kShotW, kShotH, VFov, HFov, 0, "NO-FILE", "none",
				std::string(TCHAR_TO_UTF8(*GNote)))
				+ " " + ShotCamAndCaptureNow()
				+ " " + ShotControlQuadsNow(S, false)
				+ " " + ExposurePinNow()
				+ " " + LampGlowNow(S, nullptr, 0, 0));
			NoteLadderRow(S.Id, bAfterNight, false, 0.0, 0, 0, 0);
			return;
		}
		const int64 Bytes = IFileManager::Get().FileSize(*PngPath);
		TArray64<uint8> Bgra;
		int32 W = 0, H = 0;
		std::string Note(TCHAR_TO_UTF8(*GNote));
		if (!DecodeBgra(PngPath, Bgra, W, H, Note))
		{
			++GNoFile;
			GShotLines.push_back(ShotLine(S.Id, S.CameraId, S.ConditionId, GEyeY,
				TCHAR_TO_UTF8(*GCamEdge), Median, kTimedFrames, kWarmFrames,
				0, 0, VFov, HFov, (long long)Bytes, "UNDECODABLE",
				TCHAR_TO_UTF8(*FPaths::GetCleanFilename(PngPath)), Note)
				+ " " + ShotCamAndCaptureNow()
				+ " " + ShotControlQuadsNow(S, false)
				+ " " + ExposurePinNow()
				+ " " + LampGlowNow(S, nullptr, 0, 0));
			NoteLadderRow(S.Id, bAfterNight, false, 0.0, 0, 0, 0);
			return;
		}
		const LedgerFrame::FrameStats St =
			LedgerFrame::Measure((const unsigned char*)Bgra.GetData(), W, H);
		if (St.Blank) { ++GBlank; } else { ++GWrote; }
		// QUEUE 329: THIS SHOT'S REFERENCE FRAME IS THE ON HALF OF EVERY
		// DIFFERENCE ITS PROBE PASS IS ABOUT TO TAKE, so its structural
		// blankness decides whether any of them is a measurement at all. Read
		// here, where the frame is measured, and never re-derived.
		GRefBlank = St.Blank;
		// THE PIXEL STATISTICS RIDE ON THE SAME LINE AS THE SHOT'S OWN KEYS,
		// through the tested formatter, so the frame and the numbers about it
		// cannot be separated by a grep.
		std::string Line = ShotLine(S.Id, S.CameraId, S.ConditionId, GEyeY,
			TCHAR_TO_UTF8(*GCamEdge), Median, kTimedFrames, kWarmFrames,
			W, H, VFov, HFov, (long long)Bytes,
			St.Blank ? "BLANK" : "WROTE",
			TCHAR_TO_UTF8(*FPaths::GetCleanFilename(PngPath)), Note);
		// PER-SAMPLE NUMBERS ON THE SAMPLE LINE. FrameStats' own done line
		// carries whole-run keys (seconds waited, ticks) that would be a lie
		// four times over on four shot lines, so the pixel statistics come
		// through PixelLine, which carries only what is true of THIS frame.
		Line += " ";
		Line += LedgerFrame::PixelLine(St);
		// AND WHAT THE TONE MAPPER DID TO THIS FRAME, as counts with their
		// denominator at both ends. shotMeanLuma=0.5030 sat over a day frame
		// whose whole ground plane was clipped, because a mean cannot see
		// clipping; these keys can, and the eight luma bands are the series a
		// bound gets read off later rather than invented now.
		const LedgerFrame::ExposureStats Exp =
			LedgerFrame::MeasureExposure((const unsigned char*)Bgra.GetData(), W, H);
		Line += " ";
		Line += LedgerFrame::ExposureLine(Exp);
		// AND WHAT THE SKY AND THE GROUND ARE IN THIS FRAME, QUEUE 186.
		// shotMeanLuma is a mean over the whole picture and cannot tell a
		// sky that arrived from a fog colour that never left; three named
		// geometric bands can, and their channel means are what separate a
		// sky's colour from an inscattering colour. Per-sample keys on the
		// sample line, because these are statistics of THIS frame.
		{
			const unsigned char* Px = (const unsigned char*)Bgra.GetData();
			const LedgerFrame::BandStats SkyTop = LedgerFrame::MeasureBand(
				Px, W, H, "skyTop", 0.0, 0.0, 1.0, LedgerFrame::SkyTopY1());
			const LedgerFrame::BandStats SkyCentre = LedgerFrame::MeasureBand(
				Px, W, H, "skyCentre", LedgerFrame::SkyCentreX0(), 0.0,
				LedgerFrame::SkyCentreX1(), LedgerFrame::SkyTopY1());
			const LedgerFrame::BandStats Ground = LedgerFrame::MeasureBand(
				Px, W, H, "ground", 0.0, LedgerFrame::GroundY0(), 1.0, 1.0);
			Line += " ";
			Line += LedgerFrame::SkyBandLine(SkyTop, SkyCentre, Ground);
			// AND KEPT, for the null-series spread on the done line. The
			// determinism repeat is deliberately NOT kept: it is not a shot
			// the file asked for, and counting it would put one frame in the
			// group twice.
			if (!GRepeating)
			{
				LedgerVignette::FrameSample FS;
				FS.ShotId   = S.Id;
				FS.CameraId = S.CameraId;
				if (const Condition* CC = FindCondition(S.ConditionId))
				{
					FS.Applied      = LedgerVignette::AppliedFieldsUnreal(*CC, true);
					FS.AppliedNoSky = LedgerVignette::AppliedFieldsUnreal(*CC, false);
					FS.SkyIntensity = CC->SkyIntensity;
				}
				FS.bMeasured = Ground.Measured && !St.Blank;
				FS.MeanLuma  = St.MeanLuma;
				FS.GroundP05 = Ground.P05;
				FS.GroundP50 = Ground.P50;
				GFrameSamples.push_back(FS);
			}
		}
		// AND WHAT LIT IT, READ OFF THE COMPONENTS RATHER THAN OFF THE ROW
		// OF THE FILE THAT ASKED FOR IT. Per-sample keys on the sample line.
		Line += " ";
		Line += ShotLightNow(S);
		// AND WHAT TOOK IT: the camera this frame was photographed from, and
		// which of the two capture paths wrote the file. Per-sample, queue
		// 208, and the reason tools/frame-shadow-probe.py can bind a shot
		// that is not the last one the run placed.
		Line += " ";
		Line += ShotCamAndCaptureNow();
		// AND WHETHER THE WHOLE-FRAME KEYS ABOVE INCLUDE THE THREE CONTROL
		// QUADS, A1(d). shotMeanLuma, the exposure bands and band.ground are
		// means over every pixel of this frame, so on the camera the controls
		// were placed from they include three saturated swatches standing in
		// the carriageway, and a reader comparing cells across cameras had no
		// way to tell which lines carry them.
		Line += " ";
		Line += ShotControlQuadsNow(S, true);
		// AND WHAT EXPOSURE THIS FRAME WAS ASKED TO HOLD, QUEUE 235, asked
		// beside read with the residual. Per-sample, because the write happens
		// at every camera placement and the run-wide tonemap line is
		// last-wins.
		Line += " ";
		Line += ExposurePinNow();
		// AND WHAT WETNESS THIS FRAME WAS PHOTOGRAPHED AT, QUEUE 309, asked
		// beside carried. PER-SAMPLE AND UNDER ITS OWN KEY NAMES, because the
		// surface line's wetSet is last-wins over the run and cannot tell a
		// value re-driven per condition from a value set once to the last
		// condition's number. shotWetnessAgrees is the whole reading: the
		// wetness this row's condition ASKS for against the wetness the
		// street is CARRYING at the moment the shutter opens.
		{
			LedgerSurface::WetShotIn WS;
			WS.AskedFrom = S.ConditionId;
			if (const Condition* WC = FindCondition(S.ConditionId))
			{
				WS.Asked = WC->Wetness;
			}
			WS.bEverApplied = GWetRedrive.bEverApplied;
			WS.OnPieces     = GWetRedrive.LastWetness;
			WS.WalkedAt     = GWetRedrive.LastFrom;
			// NO SEPARATOR ADDED: WetShotFields opens with its own space, the
			// habit every Wet* segment in SurfaceBind.h follows, and a second
			// one here would put two spaces in a line every reader splits on
			// whitespace.
			Line += LedgerSurface::WetShotFields(WS);
		}
		// AND WHETHER THE LAMPS ARE LIT IN THIS FRAME, QUEUE 333. PER-SAMPLE
		// and off the pixels of the frame just decoded: every number in it is
		// true of this one picture, which is why none of it rides the
		// materials done line where the drive's cumulative tallies are.
		Line += " ";
		Line += LampGlowNow(S, (const unsigned char*)Bgra.GetData(), W, H);
		GShotLines.push_back(Line);
		// ---- THE LADDER'S ROWS, AND WHAT CAME BEFORE THEM -----------------
		//
		// A ROW'S PREDECESSOR IS READ OFF THE SHOT LOOP, NEVER OFF ITS NAME.
		// The pairing is the measurement: the fault under test is a frame
		// coming out blown because the frame before it was dark, so a row
		// whose predecessor is not what its name claims must report what it
		// actually followed. The repeat pass is excluded from both the ladder
		// and the predecessor memory, because it is not a shot the file asked
		// for.
		if (!GRepeating)
		{
			NoteLadderRow(S.Id, bAfterNight, !St.Blank && Exp.Measured,
			              St.MeanLuma, Exp.ClipHiAny, Exp.ClipLoAll, Exp.Pixels);
		}
		// ---- THE FIRST SHOT'S PIXELS, KEPT FOR THE REPEAT AT THE END -----
		//
		// A COPY, taken before the light probe may move this buffer out from
		// under it. Only the first shot is kept, and only once: the repeat
		// is one difference, not eleven.
		if (GFirstBgra.Num() == 0 && GShotIndex == 0)
		{
			GFirstBgra = Bgra;
			GFirstW = W; GFirstH = H; GFirstShotId = S.Id;
		}
		if (GArt.empty())
		{
			GArt = LedgerFrame::AsciiLuma((const unsigned char*)Bgra.GetData(), W, H);
		}
		// THE REFERENCE HALF OF EVERY DIFFERENCE THIS SHOT IS ABOUT TO TAKE.
		// Kept only when the shot is going to be probed, and dropped
		// otherwise, so no later probe can diff against another shot's frame.
		if (ShouldProbeShot(S))
		{
			GRefBgra = MoveTemp(Bgra);
			GRefW = W; GRefH = H;
			GRefShotId = S.Id;
		}
		else
		{
			GRefBgra.Empty();
			GRefW = 0; GRefH = 0;
			GRefShotId.clear();
		}
	}

	FString ShotPngPath(const Shot& S)
	{
		return AbsProject(*FString::Printf(TEXT("ue-%s.png"), UTF8_TO_TCHAR(S.Id.c_str())));
	}

	// ONE SCRATCH PATH, OVERWRITTEN BY EVERY PROBE AND DELETED AT THE END.
	// A probe frame is half of a difference and the difference is the
	// finding, so fourteen of them are not evidence worth committing; the
	// step stages by name and would not collect them in any case.
	FString ProbePngPath()
	{
		return AbsProject(kProbePngLeaf);
	}

	// AND ONE FOR THE DETERMINISM REPEAT, for the same reason: the repeat is
	// half of a difference and the difference is the finding, so the frame
	// itself is not committed and the step stages by name in any case.
	FString RepeatPngPath()
	{
		return AbsProject(kRepeatPngLeaf);
	}

	// ---- IS THIS RIG DETERMINISTIC, ASKED OF THE RUN ITSELF -------------
	//
	// The first shot's camera and condition, photographed again as the last
	// thing the run does. Identical inputs and maximum order separation, so
	// anything other than IDENTICAL is the rig's own drift and every
	// cross-shot comparison the run supports carries it. The arithmetic and
	// the string are in FrameStats.h, where g++ runs them before any
	// dispatch; this supplies the two buffers and a status word.
	void MeasureRigRepeat(const FString& PngPath, bool bHaveFile)
	{
		LedgerFrame::RepeatDiff D;
		const int OfShots = (int)GSpec.Shots.size();
		if (!bHaveFile)
		{
			GRigLine = LedgerFrame::RigDeterminismLine(
				GFirstShotId, OfShots, OfShots, "NO-FILE", D);
			return;
		}
		TArray64<uint8> Bgra;
		int32 W = 0, H = 0;
		std::string Note("none");
		if (!DecodeBgra(PngPath, Bgra, W, H, Note))
		{
			GRigLine = LedgerFrame::RigDeterminismLine(
				GFirstShotId, OfShots, OfShots, "UNDECODABLE", D);
			return;
		}
		if (GFirstBgra.Num() == 0)
		{
			GRigLine = LedgerFrame::RigDeterminismLine(
				GFirstShotId, OfShots, OfShots, "NO-FIRST-FRAME", D);
			return;
		}
		if (W != GFirstW || H != GFirstH)
		{
			// TWO SIZES ARE NOT TWO TAKES OF ONE PICTURE, and a difference
			// taken across them would be arithmetic on unrelated pixels.
			GRigLine = LedgerFrame::RigDeterminismLine(
				GFirstShotId, OfShots, OfShots, "SIZE-MISMATCH", D);
			return;
		}
		D = LedgerFrame::MeasureRepeat(
			(const unsigned char*)GFirstBgra.GetData(),
			(const unsigned char*)Bgra.GetData(), W, H);
		GRigLine = LedgerFrame::RigDeterminismLine(
			GFirstShotId, OfShots, OfShots, "MEASURED", D);
	}

	// QUEUE 326: THE LINE, ITS FLOOR VERDICT AND THE EXPOSURE IT WAS TAKEN
	// UNDER, ASSEMBLED IN ONE PLACE. Every string below is formatted in
	// FrameStats.h; this supplies membership (which light, which shot), the
	// control it is being read against, and the live pin state. The pin WORD
	// comes from LedgerVignette::ExposurePinWord, which is this tree's one
	// implementation of that idea, and is handed across rather than re-decided.
	void EmitLightLine(const Shot& S, int32 Seq, const char* Status,
	                   const LedgerFrame::LightDelta& D, const std::string& Note,
	                   int Read = -1,
	                   const LedgerFrame::FrameStats& ProbePx = LedgerFrame::FrameStats(),
	                   bool bProbeDecoded = false)
	{
		const std::string Id = (Seq < 0) ? std::string("control_no_toggle") : ProbeId(Seq);
		const char* Kind = (Seq < 0) ? "control" : ProbeKind(Seq);
		LedgerFrame::LightPin Pin;
		Pin.Word    = LedgerVignette::ExposurePinWord(GShotPin);
		Pin.bRead   = GShotPin.bRead;
		Pin.ReadMin = GShotPin.ReadMin;
		Pin.ReadMax = GShotPin.ReadMax;
		GLightLines.push_back(LedgerFrame::LightDeltaLine(
			Id, Kind, Seq + 1, ProbeTargetCount(), S.Id, S.CameraId, S.ConditionId,
			Status, D, Note)
			+ " " + LedgerFrame::LightFloorSegment(GFloor, D, Seq < 0, Read)
			+ " " + LedgerFrame::LightProbeFrameSegment(ProbePx, bProbeDecoded)
			+ " " + LedgerFrame::LightPinSegment(Pin));
	}

	// ADVANCE TO THE NEXT THING TO PHOTOGRAPH, OR END THE PASS.
	//
	// Sequence -1 is the CONTROL: the same camera, the same condition, the
	// same frame counts and NOTHING TOGGLED. Its delta against the reference
	// is this run's own noise floor, which is why no epsilon had to be
	// invented for "did this light reach a pixel".
	//
	// A LIGHT ALREADY OFF IN THIS CONDITION IS NOT PHOTOGRAPHED. Toggling it
	// would measure a difference of zero and print it beside the word
	// lantern, which is the false reading this whole item exists to stop.
	bool BeginNextProbe(const Shot& S)
	{
		while (true)
		{
			++GProbeSeq;
			if (GProbeSeq == -1)
			{
				++GControls;
				GProbeStarted = FPlatformTime::Seconds();
				return true;
			}
			if (GProbeSeq >= ProbeTargetCount()) { return false; }
			APointLight* L = ProbeLight(GProbeSeq);
			ULightComponent* LC = (L != nullptr) ? L->GetLightComponent() : nullptr;
			if (LC == nullptr)
			{
				EmitLightLine(S, GProbeSeq, "NO-LIGHT-COMPONENT", LedgerFrame::LightDelta(),
				              "the-spawned-actor-carried-no-light-component");
				continue;
			}
			// READ BACK WHAT THE CONDITION LEFT, never assume it.
			const bool bOn = LC->IsVisible();
			if (!bOn)
			{
				++GSkippedOff;
				EmitLightLine(S, GProbeSeq, "SKIPPED-ALREADY-OFF", LedgerFrame::LightDelta(),
				              "off-in-this-condition/nothing-to-difference");
				continue;
			}
			++GEligible;
			if (GProbeSpent >= kLightProbeBudgetSeconds)
			{
				// THE CAP ANNOUNCES WHEN IT BITES, and the loop keeps
				// counting the rest so the denominator stays true.
				++GSkippedBudget;
				continue;
			}
			GProbeVisWas = bOn;
			LC->SetVisibility(false);
			GProbeStarted = FPlatformTime::Seconds();
			return true;
		}
	}

	// PUT BACK WHAT WAS CAPTURED, THEN READ IT BACK. A probe that restores a
	// value it guessed at leaves the run's evidence frames lit by the
	// probe's idea of the scene, and a restore nobody read back is a claim.
	void RestoreProbeLight()
	{
		if (GProbeSeq < 0) { return; }
		APointLight* L = ProbeLight(GProbeSeq);
		ULightComponent* LC = (L != nullptr) ? L->GetLightComponent() : nullptr;
		if (LC == nullptr) { return; }
		LC->SetVisibility(GProbeVisWas);
		if (LC->IsVisible() != GProbeVisWas) { ++GRestoreMismatch; }
	}

	// THE DIFFERENCE, TAKEN IN THE TESTED HEADER. On is the reference frame,
	// which had this light lit; Off is the frame just taken with it dark.
	void MeasureProbe(const Shot& S, const FString& Path, bool bHaveFile)
	{
		GProbeSpent += FPlatformTime::Seconds() - GProbeStarted;
		LedgerFrame::LightDelta NoPair;
		if (!bHaveFile)
		{
			++GProbeNoFile;
			EmitLightLine(S, GProbeSeq, "NO-FILE", NoPair, std::string(TCHAR_TO_UTF8(*GNote)));
			return;
		}
		TArray64<uint8> Bgra;
		int32 W = 0, H = 0;
		std::string Note("none");
		if (!DecodeBgra(Path, Bgra, W, H, Note))
		{
			++GProbeNoFile;
			EmitLightLine(S, GProbeSeq, "UNDECODABLE", NoPair, Note);
			return;
		}
		if (GRefBgra.Num() == 0 || W != GRefW || H != GRefH)
		{
			EmitLightLine(S, GProbeSeq, "NOT-COMPARABLE", NoPair,
			              "probe-and-reference-differ-in-size-or-the-reference-is-gone");
			return;
		}
		// QUEUE 329: THE PROBE FRAME IS MEASURED BEFORE IT IS DIFFERENCED,
		// and a structurally blank one is NEVER handed to MeasureLightDelta.
		// A frame that failed to render is black, and against a good
		// reference a black frame makes every pixel "rise": run 48 scored
		// eight of those as YES, the largest contributions on the file. The
		// test is FrameStats' structural rule and not a value: cam_A writes
		// its blanks at 0.00075 and the pinset camera writes its at 0.00152,
		// so a filter on either number misses the other camera's.
		const LedgerFrame::FrameStats PS =
			LedgerFrame::Measure((const unsigned char*)Bgra.GetData(), W, H);
		++GProbeFrames.Decoded;
		if (PS.Blank) { ++GProbeFrames.Blank; }
		// AND THE REFERENCE HALF COUNTS TOO. If the shot's own frame came
		// back blank there is nothing to difference against, whatever this
		// frame is, so no pair of that shot is a measurement.
		const bool bNoPair = PS.Blank || GRefBlank;
		LedgerFrame::LightDelta D;
		if (!bNoPair)
		{
			D = LedgerFrame::MeasureLightDelta(
				(const unsigned char*)GRefBgra.GetData(), (const unsigned char*)Bgra.GetData(),
				W, H, kProbeGridCols, kProbeGridRows);
		}
		// QUEUE 326: THE CONTROL IS THE SHOT'S FLOOR AND IT IS PROBED FIRST,
		// at sequence -1, so by the time any light of this shot lands the
		// thing it has to beat is already in hand. REACHED THE FRAME is no
		// longer counted here: it was `RoseAtLeast[0] > 0`, one pixel rising
		// by one code value, which run 47's control cleared at four shots
		// while toggling nothing. The comparison is LightFloorAddLight's.
		if (GProbeSeq < 0)
		{
			// A BLANK CONTROL AND A BLANK REFERENCE ARE TWO DIFFERENT
			// FAULTS AND THE FLOOR LINE SAYS WHICH. Run 48 had one of each:
			// pinset_night_2 lost the control's re-render and
			// pinset_night_1 lost the shot frame itself.
			if (PS.Blank)
			{
				GFloor.NoControlWhy = "blank-control-frame";
				EmitLightLine(S, GProbeSeq, "BLANK-PROBE-FRAME", D,
				              "the-controls-own-re-render-came-back-structurally-blank",
				              LedgerFrame::LightReadBlankProbeFrame, PS, true);
				return;
			}
			if (GRefBlank)
			{
				GFloor.NoControlWhy = "blank-reference-frame";
				EmitLightLine(S, GProbeSeq, "BLANK-SHOT", D,
				              "this-shots-own-reference-frame-came-back-structurally-blank",
				              LedgerFrame::LightReadBlankShot, PS, true);
				return;
			}
			LedgerFrame::LightFloorSetControl(GFloor, D);
			EmitLightLine(S, GProbeSeq, "MEASURED", D, "none",
			              LedgerFrame::LightReadMeasured, PS, true);
			return;
		}
		++GProbed;
		const int Read = LedgerFrame::LightFloorAddLight(
			GFloor, ProbeId(GProbeSeq), ProbeKind(GProbeSeq), D, PS.Blank);
		EmitLightLine(S, GProbeSeq, LedgerFrame::LightReadWord(Read), D, "none",
		              Read, PS, true);
	}

	// ---- QUEUE 337: HOLD THE TWO EYE-ADAPTATION SPEEDS FOR THIS PASS -----
	//
	// WHAT IT FIXES. The pass re-enters the Warm phase after every toggle
	// with the exposure rate snapped to 10000 (the per-shot write above), so
	// every OFF frame is photographed after the loop has fully re-adapted to
	// a scene with one light fewer. Under AUTO the difference is then the
	// light PLUS the loop's answer to it, and run 48 is what that looks
	// like: seven lights whose OFF frame came back brighter across 831241 to
	// 921600 pixels of 921600, and 0 lanterns measured of 24.
	//
	// WHAT IT IS NOT. It pins NO exposure VALUE. The adapted value is a
	// render-thread quantity this process never reads, the 2026-09-10 ruling
	// forbids deriving a night pin, and queue 276's settling series has not
	// run. A DIFFERENTIAL needs only the two frames at ONE value, whatever
	// that value turns out to be, so only the two RATES are written and the
	// per-shot write at the camera placement restores the snap on the next
	// shot. `exposure_pin` is untouched and no determinism gate reads this.
	//
	// ASKED BESIDE READ, ON THIS SHOT'S FLOOR LINE. A component that clamps
	// the value says so on the line rather than in a gap nobody can
	// attribute, and an engine that treats zero as instant leaves the
	// control gaps where they are: both outcomes are readable.
	void HoldExposureSpeedsForProbe()
	{
		GFloor.bHoldAsked    = true;
		GFloor.HoldAskedUp   = 0.0;
		GFloor.HoldAskedDown = 0.0;
		if (GCam == nullptr) { return; }
		UCameraComponent* CC = GCam->GetCameraComponent();
		if (CC == nullptr) { return; }
		FPostProcessSettings& PPW = CC->PostProcessSettings;
		PPW.bOverride_AutoExposureSpeedUp   = true;
		PPW.AutoExposureSpeedUp             = 0.0f;
		PPW.bOverride_AutoExposureSpeedDown = true;
		PPW.AutoExposureSpeedDown           = 0.0f;
		const FPostProcessSettings& PP = CC->PostProcessSettings;
		GFloor.bHoldRead   = true;
		GFloor.HoldReadUp   = (double)PP.AutoExposureSpeedUp;
		GFloor.HoldReadDown = (double)PP.AutoExposureSpeedDown;
	}

	bool StartLightProbe(const Shot& S)
	{
		if (!ShouldProbeShot(S)) { return false; }
		// THE FLOOR IS CLEARED BEFORE ANY LINE OF THIS SHOT IS WRITTEN,
		// including the NO-REFERENCE line below, because a floor left over
		// from the previous shot would print the previous shot's control
		// beside this shot's lights. That is the cross-shot pairing this
		// whole item exists to stop, and it would have been invisible.
		GFloor = LedgerFrame::LightFloor();
		GFloor.ShotId      = S.Id;
		GFloor.CameraId    = S.CameraId;
		GFloor.ConditionId = S.ConditionId;
		// THE HOLD IS WRITTEN HERE AND NOWHERE ELSE, which is after the
		// reference frame is on disk (MeasureShot has run) and before the
		// control's re-render (BeginNextProbe below asks for it).
		HoldExposureSpeedsForProbe();
		if (GRefBgra.Num() == 0 || GRefShotId != S.Id)
		{
			GFloor.NoControlWhy = "the-reference-frame-did-not-decode";
			EmitLightLine(S, -1, "NO-REFERENCE", LedgerFrame::LightDelta(),
			              "the-reference-frame-did-not-decode/nothing-to-difference-against");
			// A SHOT THAT TRIED AND HAD NOTHING TO DIFFERENCE AGAINST IS IN
			// THE DENOMINATOR, with the verdict NO-CONTROL on its own line.
			// Dropped, the floor totals would describe a smaller set than the
			// one examined, which is the shape rule 3b refuses.
			GFloors.push_back(GFloor);
			return false;
		}
		GProbing = true;
		GProbeSeq = -2;
		++GShotsProbed;
		if (!BeginNextProbe(S)) { GProbing = false; return false; }
		return true;
	}

	// WHAT HAPPENS WHEN A FRAME LANDS, IN ONE PLACE. The reference path and
	// the probe path differ only in what they measure, and a second copy of
	// this would drift the moment either changed.
	void AfterFrame(bool bHaveFile)
	{
		const Shot& S = GSpec.Shots[GShotIndex];
		if (GRepeating)
		{
			// THE REPEAT PUSHES NO SHOT LINE. Its frame is half of a
			// difference, not evidence, and a twelfth shot line would put a
			// frame nothing committed into every denominator on the file.
			MeasureRigRepeat(GAskedPath, bHaveFile);
			GRepeating = false;
			GShotIndex = (int32)GSpec.Shots.size();
			GPhase = EPhase::ApplyShot;
			return;
		}
		if (GProbing)
		{
			MeasureProbe(S, GAskedPath, bHaveFile);
			RestoreProbeLight();
			if (BeginNextProbe(S))
			{
				// THE SAME FRAME COUNTS AS THE REFERENCE, which is why the
				// series is cleared: Timed stops when it holds 24 samples,
				// and a series left full from the reference would send the
				// probe to the camera after no settling at all.
				GFrameMs.clear();
				GPhase = EPhase::Warm;
				return;
			}
			GProbing = false;
			// THE SHOT'S FLOOR IS CLOSED HERE, WHERE ITS LAST LIGHT LANDED,
			// so the per-shot line's counts are that shot's and the run line
			// is a reduction over the same vector rather than a second tally.
			GFloors.push_back(GFloor);
			GRefBgra.Empty();
			GRefW = 0; GRefH = 0; GRefShotId.clear();
			++GShotIndex;
			++GShotPass;
			GPhase = EPhase::ApplyShot;
			return;
		}
		MeasureShot(S, GAskedPath, bHaveFile);
		if (bHaveFile && StartLightProbe(S))
		{
			GFrameMs.clear();
			GPhase = EPhase::Warm;
			return;
		}
		++GShotIndex;
		++GShotPass;
		GPhase = EPhase::ApplyShot;
	}

	// ---- PHASE C: THE PACK'S MAPS, IMPORTED AT RUNTIME -------------------
	//
	// MEASURE THE ASSET BEFORE PLACING IT, AND SAY WHAT IT LOADED AS. A file
	// is not what its extension claims: the decoder is asked what the bytes
	// are and the answer is printed beside the size it came back at, because
	// an import assumption that goes unread is this project's most expensive
	// recurring fault.
	//
	// THE FILENAME RULE IS THE UNITY HOST'S, read out of SurfaceBind.h,
	// which is the tested layer. Nothing here decides which file a surface
	// wants; this code only asks the disk and the decoder, and hands the
	// answers back to be counted and formatted where the tests run.
	const TCHAR* ImageFormatName(EImageFormat F)
	{
		switch (F)
		{
		case EImageFormat::PNG:  return TEXT("PNG");
		case EImageFormat::JPEG: return TEXT("JPEG");
		case EImageFormat::BMP:  return TEXT("BMP");
		case EImageFormat::EXR:  return TEXT("EXR");
		default:                 return TEXT("UNRECOGNISED");
		}
	}

	// THE TEXTURE ROOT IS LOOKED FOR IN NAMED PLACES AND THE ONE THAT
	// ANSWERED IS PRINTED, exactly as the spec file is. A packaged build runs
	// from Packaged/Windows and the checkout sits four directories above it;
	// a staged copy beside the exe is tried first so the step can choose to
	// carry the pack rather than reach for it.
	//
	// THE FIRST TWO CANDIDATES ARE THE CONTRACT. The workflow copies the
	// pack to `CityPackTextures` beside the staged project and beside the
	// binary, by name, exactly as it copies the piece list, and this search
	// is not widened to guess at a repository layout from a packaged binary.
	// Run 19 found nothing in all four because nothing had ever created the
	// first two and a packaged exe is not four directories under a checkout.
	//
	// EVERY CANDIDATE IS RECORDED WHETHER OR NOT IT ANSWERED. `NOT-FOUND`
	// with no list beside it cost run 19 a round trip: the question is which
	// of the pack and the search is in the wrong place, and only the list
	// answers it. The joining and the cap are in SurfaceBind.h, where g++
	// runs them before a dispatch.
	FString FindTexRoot(int32& OutFiles, std::vector<std::string>& OutTried)
	{
		const FString ExeDir = FPaths::GetPath(FPlatformProcess::ExecutablePath());
		TArray<FString> Cands;
		Cands.Add(AbsProject(TEXT("CityPackTextures")));
		Cands.Add(FPaths::ConvertRelativePathToFull(FPaths::Combine(ExeDir, TEXT("CityPackTextures"))));
		Cands.Add(AbsProject(TEXT("../ledger/Assets/StreamingAssets/CityPack/textures")));
		Cands.Add(FPaths::ConvertRelativePathToFull(FPaths::Combine(
			ExeDir, TEXT("../../../../ledger/Assets/StreamingAssets/CityPack/textures"))));
		// RECORDED AS IT IS ASKED, and the search still stops at the first
		// answer: a list of every candidate whether or not it was reached
		// would be named wrongly, since `tried` and `would have tried next`
		// are different facts. On a run that finds the pack the list ends
		// with the directory that answered.
		OutFiles = 0;
		for (int32 I = 0; I < Cands.Num(); ++I)
		{
			OutTried.push_back(std::string(TCHAR_TO_UTF8(*Cands[I])));
			if (!IFileManager::Get().DirectoryExists(*Cands[I])) { continue; }
			TArray<FString> Found;
			IFileManager::Get().FindFiles(Found, *(Cands[I] / TEXT("*.*")), true, false);
			if (Found.Num() == 0) { continue; }
			OutFiles = Found.Num();
			return Cands[I];
		}
		return FString();
	}

	// THE DECAL ROOT, LOOKED FOR THE SAME WAY THE PACK IS, AND COUNTED
	// RECURSIVELY BECAUSE IT HAS SUBDIRECTORIES.
	//
	// The twenty pictures this street asks for live under
	// ledger/Assets/StreamingAssets/Decals as `generated/<id>.png` and
	// `ambientcg/<set>/`, and the asset string in the shared file carries that
	// relative path, so the layout has to survive staging. The workflow copies
	// the generated directory to `LedgerDecals` beside the staged project and
	// beside the exe, by name, exactly as it copies CityPackTextures, and this
	// search is not widened to guess at a repository layout from a packaged
	// binary.
	//
	// A NON-RECURSIVE FILE COUNT WOULD HAVE READ ZERO HERE and skipped a
	// directory that is perfectly staged: the root holds no files at all, only
	// the two subdirectories. That is the same shape as FindTexRoot's
	// `Found.Num() == 0` guard and it would have been invisible except as a
	// decalRoot=NOT-FOUND over a staged tree.
	FString FindDecalRoot(int32& OutFiles, std::vector<std::string>& OutTried)
	{
		const FString ExeDir = FPaths::GetPath(FPlatformProcess::ExecutablePath());
		TArray<FString> Cands;
		Cands.Add(AbsProject(TEXT("LedgerDecals")));
		Cands.Add(FPaths::ConvertRelativePathToFull(FPaths::Combine(ExeDir, TEXT("LedgerDecals"))));
		Cands.Add(AbsProject(TEXT("../ledger/Assets/StreamingAssets/Decals")));
		Cands.Add(FPaths::ConvertRelativePathToFull(FPaths::Combine(
			ExeDir, TEXT("../../../../ledger/Assets/StreamingAssets/Decals"))));
		OutFiles = 0;
		for (int32 I = 0; I < Cands.Num(); ++I)
		{
			OutTried.push_back(std::string(TCHAR_TO_UTF8(*Cands[I])));
			if (!IFileManager::Get().DirectoryExists(*Cands[I])) { continue; }
			TArray<FString> Found;
			IFileManager::Get().FindFilesRecursive(Found, *Cands[I], TEXT("*.png"), true, false);
			if (Found.Num() == 0) { continue; }
			OutFiles = Found.Num();
			return Cands[I];
		}
		return FString();
	}

	// DECODE A FILE AND UPLOAD IT, WHOLE OR CROPPED, BY ONE PATH.
	//
	// THE CROP IS WHY THIS FUNCTION GREW AND NOT WHY A SECOND ONE WAS
	// WRITTEN. A decal's asset string carries the rectangle of the picture
	// that is the subject (see SurfaceBind.h SplitDecalAsset), and the base
	// material exposes tiling scalars but NO uv offset, so the rectangle
	// cannot be expressed as an ST pair the way the Unity host expresses it.
	// It is cut out of the decoded buffer instead, which needs no material
	// change at all. Two copies of a decode is this project's most repeated
	// fault, so there is one decode here and the crop is a parameter.
	//
	// OutW and OutH STAY THE WHOLE IMAGE'S SIZE, which is what the surface
	// line has always called loadedAs: the thing the decoder said the file
	// IS. The rectangle that was taken out of it rides OutCrop, and the
	// arithmetic that turns four uv numbers into texels is CropPixels, in the
	// tested header, because the row order is the whole of it.
	UTexture2D* ImportTexture(const FString& FullPath, bool bSrgb,
	                          int32& OutW, int32& OutH, FString& OutLoadedAs,
	                          const LedgerSurface::DecalAsset* CropFrom = nullptr,
	                          LedgerSurface::CropPx* OutCrop = nullptr)
	{
		OutW = 0; OutH = 0;
		OutLoadedAs = TEXT("not-read");
		TArray<uint8> Bytes;
		if (!FFileHelper::LoadFileToArray(Bytes, *FullPath) || Bytes.Num() == 0)
		{
			OutLoadedAs = TEXT("file-would-not-load-or-was-empty");
			return nullptr;
		}
		IImageWrapperModule* Mod =
			FModuleManager::Get().LoadModulePtr<IImageWrapperModule>(FName("ImageWrapper"));
		if (Mod == nullptr) { OutLoadedAs = TEXT("imagewrapper-module-missing"); return nullptr; }
		// WHAT THE BYTES ARE, ASKED RATHER THAN INFERRED FROM THE SUFFIX.
		const EImageFormat Fmt = Mod->DetectImageFormat(Bytes.GetData(), (int64)Bytes.Num());
		TSharedPtr<IImageWrapper> Wrapper = Mod->CreateImageWrapper(Fmt);
		if (!Wrapper.IsValid())
		{
			OutLoadedAs = FString::Printf(TEXT("no-wrapper-for-%s"), ImageFormatName(Fmt));
			return nullptr;
		}
		if (!Wrapper->SetCompressed(Bytes.GetData(), (int64)Bytes.Num()))
		{
			OutLoadedAs = FString::Printf(TEXT("%s-setcompressed-refused"), ImageFormatName(Fmt));
			return nullptr;
		}
		const int32 W = Wrapper->GetWidth();
		const int32 H = Wrapper->GetHeight();
		TArray64<uint8> Raw;
		if (W <= 0 || H <= 0 || !Wrapper->GetRaw(ERGBFormat::BGRA, 8, Raw))
		{
			OutLoadedAs = FString::Printf(TEXT("%s-getraw-refused"), ImageFormatName(Fmt));
			return nullptr;
		}
		// THE RECTANGLE, DECIDED IN THE TESTED HEADER, OR THE WHOLE IMAGE.
		LedgerSurface::CropPx Rect;
		Rect.X = 0; Rect.Y = 0; Rect.W = W; Rect.H = H;
		if (CropFrom != nullptr)
		{
			Rect = LedgerSurface::CropPixels(*CropFrom, W, H);
		}
		if (OutCrop != nullptr) { *OutCrop = Rect; }
		if (Rect.W <= 0 || Rect.H <= 0)
		{
			OutLoadedAs = FString::Printf(TEXT("%s-crop-came-out-empty"), ImageFormatName(Fmt));
			return nullptr;
		}
		UTexture2D* Tex = UTexture2D::CreateTransient(Rect.W, Rect.H, PF_B8G8R8A8);
		if (Tex == nullptr)
		{
			OutLoadedAs = FString::Printf(TEXT("%s-createtransient-returned-null"), ImageFormatName(Fmt));
			return nullptr;
		}
		// COLOUR SPACE IS SET BY WHAT THE MAP IS FOR, not by what the file
		// is: a normal or a roughness map read as sRGB is wrong by a gamma
		// curve, and the verdict prints which each one was treated as.
		Tex->SRGB = bSrgb;
		// KEPT ALIVE EXPLICITLY. A transient texture whose only reference is
		// a dynamic material instance is exactly the shape of object this
		// engine collects between two ticks.
		Tex->AddToRoot();
		uint8* Dest = (uint8*)Tex->GetPlatformData()->Mips[0].BulkData.Lock(LOCK_READ_WRITE);
		if (CropFrom == nullptr)
		{
			// THE PACK'S OWN PATH, BYTE FOR BYTE WHAT IT ALWAYS WAS. Only a
			// decal asks for a rectangle, so only a decal takes the row loop.
			FMemory::Memcpy(Dest, Raw.GetData(), (SIZE_T)Raw.Num());
		}
		else
		{
			// ROW BY ROW, FOUR BYTES A TEXEL, AND THE ROW INDEX IS THE ONLY
			// THING THAT COULD BE WRONG HERE. Rect.Y is already a TOP-DOWN
			// row, turned from the file's bottom-up v by CropPixels. The two
			// flips are the lever for the one question this container cannot
			// answer (the engine plane's uv winding) and both are off today.
			const int64 SrcStride = (int64)W * 4;
			const int64 DstStride = (int64)Rect.W * 4;
			const bool bFlipRows = LedgerSurface::DecalFlipRows();
			const bool bFlipCols = LedgerSurface::DecalFlipCols();
			for (int32 Row = 0; Row < Rect.H; ++Row)
			{
				const int32 SrcRow = bFlipRows ? (Rect.Y + Rect.H - 1 - Row) : (Rect.Y + Row);
				const uint8* Src = Raw.GetData() + (int64)SrcRow * SrcStride + (int64)Rect.X * 4;
				uint8* Dst = Dest + (int64)Row * DstStride;
				if (!bFlipCols)
				{
					FMemory::Memcpy(Dst, Src, (SIZE_T)DstStride);
					continue;
				}
				for (int32 Col = 0; Col < Rect.W; ++Col)
				{
					FMemory::Memcpy(Dst + (int64)Col * 4,
					                Src + (int64)(Rect.W - 1 - Col) * 4, 4);
				}
			}
		}
		Tex->GetPlatformData()->Mips[0].BulkData.Unlock();
		Tex->UpdateResource();
		OutW = W; OutH = H;
		OutLoadedAs = FString::Printf(TEXT("%s-BGRA8/srgb=%s"),
		                              ImageFormatName(Fmt), bSrgb ? TEXT("yes") : TEXT("no"));
		return Tex;
	}

	// A FLAT TEXTURE OF ONE COLOUR, BUILT IN CODE, NO FILE AND NO DECODER.
	//
	// THIS IS THE WHOLE OF THE TINT ROUTE ON THIS SIDE. The Unity host paints
	// interior and paint_yellow from the SurfaceSpec tint because the pack
	// answers for neither, and the Unreal base material has a base colour MAP
	// and no base colour parameter, so the tint arrives as a texture. Two by
	// two rather than one by one for the reason the control texture is 2x2: a
	// one-texel mip chain is a shape nothing else here uses, and four
	// identical texels cost nothing.
	//
	// THE TEXEL COMES OUT OF THE TESTED HEADER. Nothing here decides a colour:
	// ProceduralAlbedoTexel takes the Unity literal, the byte quantisation and
	// both grades and returns the byte triple, and g++ runs that before this
	// file is ever compiled.
	UTexture2D* MakeFlatTexture(int32 R, int32 G, int32 B, bool bSrgb, const TCHAR* Name)
	{
		UTexture2D* Tex = UTexture2D::CreateTransient(2, 2, PF_B8G8R8A8);
		if (Tex == nullptr) { return nullptr; }
		Tex->SRGB = bSrgb;
		Tex->Filter = TF_Nearest;
		Tex->AddToRoot();
		const uint8 Px[4] = {(uint8)B, (uint8)G, (uint8)R, 255};
		uint8* Dest = (uint8*)Tex->GetPlatformData()->Mips[0].BulkData.Lock(LOCK_READ_WRITE);
		for (int32 I = 0; I < 4; ++I)
		{
			FMemory::Memcpy(Dest + I * 4, Px, 4);
		}
		Tex->GetPlatformData()->Mips[0].BulkData.Unlock();
		Tex->UpdateResource();
		(void)Name;
		return Tex;
	}

	// QUEUE 186: IS THE NAMED HDRI EVEN REACHABLE FROM THIS BINARY.
	//
	// NOTHING IS BOUND HERE AND NOTHING MAY BE. A USkyLightComponent takes a
	// cube texture and this engine builds none at runtime, so a decoded
	// long-lat Radiance image would have nowhere to go. What this answers is
	// the ONE question the next rung turns on: whether the file the shared
	// condition block has always named can be opened from a packaged build
	// at all, or whether that rung needs a staging step in the workflow
	// first. Asking it costs one file-exists and one format detect; guessing
	// it costs a round trip on his PC.
	//
	// THE CANDIDATE LIST MIRRORS FindTexRoot's, deliberately, because the
	// pack and the sky would be staged by the same kind of step and a
	// different search would answer a different question. EVERY CANDIDATE IS
	// RECORDED whether or not it answered, for the reason run 19 established:
	// NOT-FOUND with no list beside it does not say whether the file or the
	// search is in the wrong place.
	// EVERY PLACE A NAMED PHOTOGRAPH COULD BE, IN ONE LIST, so the probe that
	// REPORTS and the bind that USES can never search different places and
	// disagree about whether a file exists. Four roots times two extensions;
	// the roots are FindTexRoot's, deliberately, because the pack and the sky
	// are staged by the same kind of step.
	void SkyPhotoCandidates(const std::string& Name, TArray<FString>& Out)
	{
		const FString Base = FString(UTF8_TO_TCHAR(Name.c_str()));
		const FString ExeDir = FPaths::GetPath(FPlatformProcess::ExecutablePath());
		for (int32 E = 0; E < 2; ++E)
		{
			const FString Leaf = Base + FString(kSkyPhotoExts[E]);
			Out.Add(AbsProject(*(FString(TEXT("SkyHdri/")) + Leaf)));
			Out.Add(FPaths::ConvertRelativePathToFull(
				FPaths::Combine(ExeDir, TEXT("SkyHdri"), *Leaf)));
			Out.Add(AbsProject(*(FString(TEXT("../ledger/Assets/Resources/")) + Leaf)));
			Out.Add(FPaths::ConvertRelativePathToFull(FPaths::Combine(
				ExeDir, TEXT("../../../../ledger/Assets/Resources"), *Leaf)));
		}
	}

	void LookForNamedHdri()
	{
		if (GSpec.Conditions.empty() || GSpec.Conditions[0].Hdri.empty())
		{
			GHdriFoundAt = "NOT-LOOKED-FOR/the-shared-file-named-no-hdri";
			return;
		}
		TArray<FString> Cands;
		SkyPhotoCandidates(GSpec.Conditions[0].Hdri, Cands);
		std::string Tried;
		for (int32 I = 0; I < Cands.Num(); ++I)
		{
			if (!Tried.empty()) { Tried += ";"; }
			Tried += NoSpaces(std::string(TCHAR_TO_UTF8(*Cands[I])));
			if (!IFileManager::Get().FileExists(*Cands[I])) { continue; }
			GHdriFoundAt   = NoSpaces(std::string(TCHAR_TO_UTF8(*Cands[I])));
			GHdriFoundPath = Cands[I];
			GHdriBytes     = (long long)IFileManager::Get().FileSize(*Cands[I]);
			// WHAT THE BYTES ARE, ASKED RATHER THAN INFERRED FROM THE SUFFIX,
			// the same rule ImportTexture follows. The enum VALUE is printed
			// beside the name because this file's ImageFormatName knows four
			// formats and Radiance is not one of them: UNRECOGNISED/enum=8
			// and UNRECOGNISED/enum=-1 are different answers and the number
			// is what separates them.
			TArray<uint8> Head;
			if (FFileHelper::LoadFileToArray(Head, *Cands[I]) && Head.Num() > 0)
			{
				IImageWrapperModule* Mod =
					FModuleManager::Get().LoadModulePtr<IImageWrapperModule>(FName("ImageWrapper"));
				if (Mod != nullptr)
				{
					const EImageFormat Fmt =
						Mod->DetectImageFormat(Head.GetData(), (int64)Head.Num());
					// THE NAME IS TURNED INTO AN std::string BEFORE THE
					// FORMAT CALL rather than handed to a variadic as a
					// conversion temporary, which is the shape this file
					// already uses everywhere it crosses that boundary.
					const std::string FmtName(TCHAR_TO_UTF8(ImageFormatName(Fmt)));
					char B[160];
					std::snprintf(B, sizeof(B), "%s/enum=%d", FmtName.c_str(), (int)Fmt);
					GHdriDetectedAs = NoSpaces(std::string(B));
				}
				else { GHdriDetectedAs = "imagewrapper-module-missing"; }
			}
			else { GHdriDetectedAs = "file-would-not-load-or-was-empty"; }
			return;
		}
		GHdriFoundAt = "NOT-FOUND/tried=" + Tried;
	}

	// ---- QUEUE 186 / D41: THE PHOTOGRAPH BECOMES THE SKY ----------------
	//
	// D40 approved the photograph. D41, 2026-09-16: "I approved the
	// photograph, not a particular binding. If it needs a different asset
	// type or a different setup to render as a sky, do that under D41 without
	// asking." So the asset type and the setup are the studio's, and both are
	// named here rather than left to be inferred from the code: an 8-bit
	// sRGB LONG-LAT PNG, made from the approved Radiance file by
	// tools/hdr-to-longlat.py, sampled by an unlit two-sided material on an
	// engine sphere seen from inside.
	//
	// WHAT IS NOT TOUCHED, AND THIS IS THE OWNERSHIP RULE RATHER THAN
	// TIMIDITY. The atmosphere stays, the sky light stays on
	// SLS_CapturedScene in real time, the fog keeps its calibrated maximum
	// opacity, and not one of their values is written here. The dome is
	// GEOMETRY: it occludes the atmosphere's backdrop for the camera and it
	// leaves every global this file already has an owner for exactly where
	// that owner put it. That is also what makes the change fail soft: if any
	// one of the mesh, the material or the photograph is missing, no dome is
	// spawned and the frame is the frame this project has been shooting all
	// along, with skyHdriBoundAs naming which of the three was missing.
	UTexture2D* LoadSkyPhoto(const std::string& Name, std::string& OutNote)
	{
		// OutNote CARRIES THE READING IN BOTH DIRECTIONS: on success it is what
		// the decoder said the file WAS (size and format, read back off the
		// import and never off the suffix); on failure it is why not.
		const FString Key = FString(UTF8_TO_TCHAR(Name.c_str()));
		if (UTexture2D** Hit = GSkyPhotoCache.Find(Key))
		{
			OutNote = "already-decoded";
			return *Hit;
		}
		TArray<FString> Cands;
		SkyPhotoCandidates(Name, Cands);
		std::string Tried;
		for (int32 I = 0; I < Cands.Num(); ++I)
		{
			if (!Tried.empty()) { Tried += ";"; }
			Tried += NoSpaces(std::string(TCHAR_TO_UTF8(*Cands[I])));
			if (!IFileManager::Get().FileExists(*Cands[I])) { continue; }
			int32 W = 0, H = 0;
			FString LoadedAs;
			UTexture2D* Tex = ImportTexture(Cands[I], true, W, H, LoadedAs);
			if (Tex == nullptr)
			{
				OutNote = "decode-refused/"
				        + NoSpaces(std::string(TCHAR_TO_UTF8(*LoadedAs)));
				return nullptr;
			}
			Tex->AddToRoot();
			GSkyPhotoCache.Add(Key, Tex);
			char B[192];
			std::snprintf(B, sizeof(B), "%dx%d/%s", W, H,
			              TCHAR_TO_UTF8(*LoadedAs));
			OutNote = NoSpaces(std::string(B));
			return Tex;
		}
		OutNote = "NOT-FOUND/tried=" + Tried;
		return nullptr;
	}

	// WRITE ON CHANGE, NEVER PER SHOT. Setting a texture parameter asks the
	// renderer to rebuild the instance, and 43 shots that name two
	// photographs must cost two writes. The count of writes is printed, so
	// the fight is visible if anything else ever starts writing this.
	void BindSkyPhoto(const std::string& Name)
	{
		if (GSkyDomeMid == nullptr || Name.empty()) { return; }
		if (Name == GSkyPhotoNow) { return; }
		std::string Note;
		UTexture2D* Tex = LoadSkyPhoto(Name, Note);
		if (Tex == nullptr)
		{
			// THE DOME KEEPS THE LAST PHOTOGRAPH THAT DID LOAD rather than
			// going grey, and the verdict says a photograph was refused. Both
			// halves are needed: a grey dome would read as a bound sky.
			GHdriBoundAs = "PARTIAL/dome-holds=" + NoSpaces(GSkyPhotoNow)
			             + "/refused=" + NoSpaces(Name) + "/" + Note;
			return;
		}
		GSkyDomeMid->SetTextureParameterValue(FName(kSkyMapParam), Tex);
		GSkyPhotoNow = Name;
		++GSkyPhotoBinds;
		char B[512];
		std::snprintf(B, sizeof(B),
			"photograph-longlat-png-on-an-unlit-sky-dome/lastWins=%s/%s/"
			"mesh=%s/diameterM=%.0f/lumGain=%.3f"
			"/lumPerCondition=skyLumDrive-on-the-materials-line"
			"/writes=%d-on-change/photos=%d",
			NoSpaces(GSkyPhotoNow).c_str(), Note.c_str(),
			TCHAR_TO_UTF8(kSkyDomeMeshPath), kSkyDomeDiameterM, kSkyLuminanceGain,
			GSkyPhotoBinds, GSkyPhotoCache.Num());
		GHdriBoundAs = NoSpaces(std::string(B));
	}

	void BuildSkyDome(UWorld* World)
	{
		if (World == nullptr) { GHdriBoundAs = "NOTHING/no-world"; return; }
		if (GSpec.Conditions.empty() || GSpec.Conditions[0].Hdri.empty())
		{
			GHdriBoundAs = "NOTHING/the-shared-file-named-no-photograph";
			return;
		}
		UMaterialInterface* SkyMat =
			LoadObject<UMaterialInterface>(nullptr, kSkyMaterialPath);
		if (SkyMat == nullptr)
		{
			GHdriBoundAs = "NOTHING/sky-material-missing/"
			               "did-tools-ue-make_sky_material.py-run/path="
			             + NoSpaces(std::string(TCHAR_TO_UTF8(kSkyMaterialPath)));
			return;
		}
		UStaticMesh* Dome = LoadShape(kSkyDomeMeshPath);
		if (Dome == nullptr)
		{
			GHdriBoundAs = "NOTHING/dome-mesh-missing/"
			               "is-Engine-BasicShapes-in-DirectoriesToAlwaysCook/path="
			             + NoSpaces(std::string(TCHAR_TO_UTF8(kSkyDomeMeshPath)));
			return;
		}
		std::string Note;
		if (LoadSkyPhoto(GSpec.Conditions[0].Hdri, Note) == nullptr)
		{
			GHdriBoundAs = "NOTHING/photograph-unreadable/" + Note;
			return;
		}
		FActorSpawnParameters Params;
		Params.SpawnCollisionHandlingOverride =
			ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
		GSkyDome = World->SpawnActor<AStaticMeshActor>(
			AStaticMeshActor::StaticClass(), FVector::ZeroVector,
			FRotator::ZeroRotator, Params);
		if (GSkyDome == nullptr)
		{
			GHdriBoundAs = "NOTHING/dome-actor-would-not-spawn";
			return;
		}
		MakeMovable(GSkyDome);
		UStaticMeshComponent* C = GSkyDome->GetStaticMeshComponent();
		if (C == nullptr)
		{
			GHdriBoundAs = "NOTHING/dome-actor-has-no-static-mesh-component";
			return;
		}
		C->SetMobility(EComponentMobility::Movable);
		C->SetStaticMesh(Dome);
		// THE COLLIDER THE MESH SHIPS WITH IS NOT WANTED, and a sky that casts
		// a shadow is a black street. Neither is left to a default: both are
		// sites this project has already been bitten at.
		C->SetCollisionEnabled(ECollisionEnabled::NoCollision);
		C->SetCastShadow(false);
		GSkyDome->SetActorScale3D(FVector(kSkyDomeDiameterM, kSkyDomeDiameterM,
		                                  kSkyDomeDiameterM));
		GSkyDomeMid = UMaterialInstanceDynamic::Create(SkyMat, GSkyDome);
		if (GSkyDomeMid == nullptr)
		{
			// AND THE DOME GOES WITH IT. Without this the sphere stays
			// spawned carrying the DEFAULT material, a 2 km enclosure round
			// the whole street, while the verdict below says NOTHING bound:
			// a wrecked frame reported as no sky at all. Ruled 2026-09-16.
			GSkyDome->Destroy();
			GSkyDome = nullptr;
			GHdriBoundAs = "NOTHING/could-not-instance-the-sky-material";
			return;
		}
		GSkyDomeParent = SkyMat;
		// THE LUMINANCE IS NOT WRITTEN HERE ANY MORE, QUEUE 361, AND THE
		// ABSENCE IS THE POINT. This site wrote a global constant once, at a
		// moment when no condition had been applied and none could be, and
		// nothing ever re-drove it: one value served day and night and the
		// night rendered like noon. ReDriveSkyLuminance is the ONE OWNER of
		// this parameter now, and it is called from ApplyCondition before
		// any frame is photographed. Until it first runs the dome carries
		// the value M_LedgerSky itself ships with, exactly as a lamp head
		// carries its material's own emissive until the first condition
		// lands; skyLumDriveAsked on the materials done line is what proves
		// the drive ran at all.
		C->SetMaterial(0, GSkyDomeMid);
		// AND THE FIRST PHOTOGRAPH. Every later shot rebinds only when its
		// condition names a different one.
		BindSkyPhoto(GSpec.Conditions[0].Hdri);
	}

	// BIND EVERY SURFACE THE SHARED FILE ASKED FOR, and count what did not
	// answer. A Phase C that renders and cannot say what it failed to load is
	// worth less than one that loads less and says so.
	void BindSurfaces()
	{
		// THE WETNESS, DECIDED BEFORE THE FIRST INSTANCE IS MADE, because an
		// instance is the only thing that can carry the parameter and this
		// function is the only place instances are made. The rule, the counts
		// and every printed string are in SurfaceBind.h where g++ runs them
		// before this file is compiled; this supplies the spec and nothing
		// else.
		GWetness = LedgerSurface::WetnessForBind(GSpec);
		GBaseMaterial = LoadObject<UMaterialInterface>(nullptr, kBaseMaterialPath);
		GTexRoot = FindTexRoot(GTexRootFiles, GTexRootTried);
		// THE DECALS ARE A SECOND ROOT AND A SECOND READING. They are staged by
		// their own step, so one NOT-FOUND covering both would not say which of
		// the two is missing.
		GDecalRoot = FindDecalRoot(GDecalRootFiles, GDecalRootTried);
		const std::vector<LedgerSurface::Ask> Asked = LedgerSurface::SurfacesAsked(GSpec.Pieces);
		// One imported texture per map per surface, kept beside its bind so
		// no file is decoded twice for the 150 pieces that share a surface.
		TArray<UTexture2D*> Maps;
		Maps.SetNumZeroed((int32)Asked.size() * LedgerSurface::MapCount());
		for (size_t I = 0; I < Asked.size(); ++I)
		{
			LedgerSurface::Bound B;
			B.Surface = Asked[I].Surface;
			B.Pieces  = Asked[I].Pieces;
			// ---- QUEUE 223, RULE ONE: A BLEND MODE IS NOT A SURFACE --------
			//
			// card and multiply never reach the texture root, and that is the
			// correction rather than an optimisation: asking for card.png asks
			// for a file that BY DESIGN can never exist, so three candidate
			// filenames on the verdict were three filenames nobody should ever
			// go looking for. The picture comes from the piece's own asset
			// field, per piece, in the loop below.
			if (LedgerSurface::IsDecalBlend(B.Surface))
			{
				B.Status = "DECAL-BLEND";
				B.Reason = "not-a-library-surface/StreetVignette.cs-57-declares-"
				           "card-and-multiply-as-the-two-decal-blends/the-picture-"
				           "is-the-piece-own-asset-under-StreamingAssets-Decals";
				B.Route = LedgerSurface::PaintRouteName(
					LedgerSurface::IsMultiplyBlend(B.Surface)
						? LedgerSurface::Paint_DecalMultiply
						: LedgerSurface::Paint_DecalCard);
				GBinds.push_back(B);
				continue;
			}
			// ---- QUEUE 223, RULE TWO: THE SurfaceSpec TINT FALLBACK --------
			//
			// interior has no pack file and paint_yellow is ProceduralOnly, so
			// the pack is not asked about either of them. The tint texel, both
			// grades and the byte quantisation are in SurfaceBind.h where g++
			// runs them; this builds the two textures and records what it
			// built. IT IS BEFORE THE TEXTURE ROOT CHECK ON PURPOSE: a run
			// whose pack did not stage should still paint the surfaces that
			// never needed one.
			if (LedgerSurface::ProceduralSurfaceIndex(B.Surface) >= 0)
			{
				const LedgerSurface::Texel T =
					LedgerSurface::ProceduralAlbedoTexel(B.Surface);
				UTexture2D* Flat = MakeFlatTexture(T.R, T.G, T.B, true,
				                                   TEXT("tint-albedo"));
				if (Flat != nullptr)
				{
					Maps[(int32)I * LedgerSurface::MapCount() + 0] = Flat;
					++GTexturesImported;
					B.bTintBuilt = true;
					B.Tint = T;
				}
				// THE ROUGHNESS, FROM THE SAME SPEC ROW, because the base
				// material has a roughness MAP and no roughness scalar. It is
				// overwritten below if this surface borrows a real one.
				const int RoughTexel = LedgerSurface::ProceduralRoughnessTexel(B.Surface);
				UTexture2D* Rough = MakeFlatTexture(RoughTexel, RoughTexel, RoughTexel,
				                                    false, TEXT("tint-roughness"));
				if (Rough != nullptr)
				{
					Maps[(int32)I * LedgerSurface::MapCount() + 2] = Rough;
					++GTexturesImported;
				}
				B.Status = (GBaseMaterial == nullptr) ? "NO-BASE-MATERIAL" : "PROCEDURAL";
				B.Reason = Flat != nullptr
					? "painted-from-the-SurfaceSpec-tint/AssetLibrary.cs-1613-marks-"
					  "paint_yellow-ProceduralOnly-and-interior-has-no-pack-file"
					: "tint-texture-would-not-build";
				B.Route = LedgerSurface::PaintRouteName(LedgerSurface::Paint_Tint);
				GBinds.push_back(B);
				continue;
			}
			if (GTexRoot.IsEmpty())
			{
				B.Status = "ABSENT";
				B.Reason = "no-texture-root-found-in-any-named-candidate";
				GBinds.push_back(B);
				continue;
			}
			// A MAP THAT WOULD NOT DECODE IS RECORDED WITHOUT DISQUALIFYING
			// THE SURFACE. A broken roughness map is not a reason to leave
			// the road untextured; only a missing or broken ALBEDO is, and
			// the difference is which of these two strings ends up where.
			std::string DecodeFail;
			for (int32 M = 0; M < LedgerSurface::MapCount(); ++M)
			{
				const std::vector<std::string> Cands = LedgerSurface::Candidates(B.Surface, M);
				for (size_t C = 0; C < Cands.size() && !B.MapFound[M]; ++C)
				{
					const FString Full = GTexRoot / FString(UTF8_TO_TCHAR(Cands[C].c_str()));
					if (IFileManager::Get().FileSize(*Full) <= 0) { continue; }
					int32 W = 0, H = 0;
					FString LoadedAs;
					// ONLY THE ALBEDO IS sRGB. The normal and roughness maps
					// are data, not colour.
					UTexture2D* Tex = ImportTexture(Full, M == 0, W, H, LoadedAs);
					B.MapFile[M] = Cands[C];
					B.MapLoadedAs[M] = TCHAR_TO_UTF8(*LoadedAs);
					B.MapW[M] = W; B.MapH[M] = H;
					if (Tex != nullptr)
					{
						B.MapFound[M] = true;
						Maps[(int32)I * LedgerSurface::MapCount() + M] = Tex;
						++GTexturesImported;
					}
					else
					{
						// A FILE THAT IS THERE AND WILL NOT DECODE IS A
						// DIFFERENT FACT from a file that is not there, and
						// the decoder's own words are the reason.
						if (!DecodeFail.empty()) { DecodeFail += "/"; }
						DecodeFail += std::string(LedgerSurface::MapName(M)) + "-"
						            + std::string(TCHAR_TO_UTF8(*LoadedAs));
					}
				}
			}
			if (!B.MapFound[0])
			{
				// THE ALBEDO IS WHAT DECIDES. Not there and there-but-broken
				// are two findings with two next actions, and the decoder's
				// own words are what separates them.
				B.Status = DecodeFail.empty() ? "ABSENT" : "UNDECODABLE";
				B.Reason = DecodeFail.empty() ? "no-candidate-file-under-texRoot" : DecodeFail;
			}
			else if (GBaseMaterial == nullptr)
			{
				B.Status = "NO-BASE-MATERIAL";
				B.Reason = "the-maps-decoded-but-there-is-nothing-to-instance";
			}
			else
			{
				B.Status = "RESOLVED";
				// A SURFACE CAN BE RESOLVED AND STILL HAVE LOST A MAP, and
				// the reason says which one rather than reading as clean.
				B.Reason = DecodeFail.empty() ? "none" : ("albedo-ok/lost-" + DecodeFail);
				B.Route = LedgerSurface::PaintRouteName(LedgerSurface::Paint_Pack);
			}
			GBinds.push_back(B);
		}

		// ---- QUEUE 223, RULE THREE: THE INTERIOR BORROWS THE WINDOW'S MAPS --
		//
		// AssetLibrary.cs:611 in one line: mapsFrom = logical == Interior ?
		// Window : logical. The interior's albedo is its own tint and its
		// relief is the window's, which is what makes a lit shop read as a room
		// behind glass instead of a flat card.
		//
		// A SECOND PASS, AND THE REASON IS THE SORT ORDER. The surfaces are
		// asked in alphabetical order, so `interior` is reached before `window`
		// and the window's files are not decoded yet when the interior is
		// built. Borrowing afterwards reuses the texture the window already
		// decoded rather than decoding a 2048 square jpeg a second time, and a
		// borrowed map is recorded in MapBorrowed and NOT in MapFound: one is
		// "this surface's own candidate answered" and the other is "it is
		// wearing somebody else's", and mapsFound must keep meaning the first.
		for (size_t I = 0; I < GBinds.size(); ++I)
		{
			const std::string From = LedgerSurface::MapsFrom(GBinds[I].Surface);
			if (From == GBinds[I].Surface) { continue; }
			int32 Src = -1;
			for (size_t J = 0; J < GBinds.size(); ++J)
			{
				if (GBinds[J].Surface == From) { Src = (int32)J; break; }
			}
			if (Src < 0)
			{
				GBinds[I].Reason += "/maps-borrow-asked-for-" + LedgerVignette::NoSpaces(From)
				                  + "-and-no-such-surface-is-in-this-street";
				continue;
			}
			for (int32 M = 1; M < LedgerSurface::MapCount(); ++M)
			{
				UTexture2D* Tex = Maps[Src * LedgerSurface::MapCount() + M];
				if (Tex == nullptr || !GBinds[(size_t)Src].MapFound[M]) { continue; }
				Maps[(int32)I * LedgerSurface::MapCount() + M] = Tex;
				GBinds[I].MapBorrowed[M] = true;
				GBinds[I].BorrowedFrom = From;
				GBinds[I].MapFile[M] = GBinds[(size_t)Src].MapFile[M];
				GBinds[I].MapLoadedAs[M] = GBinds[(size_t)Src].MapLoadedAs[M];
				GBinds[I].MapW[M] = GBinds[(size_t)Src].MapW[M];
				GBinds[I].MapH[M] = GBinds[(size_t)Src].MapH[M];
			}
		}

		// ONE INSTANCE PER PIECE, because the tiling is the piece's own size
		// and two pieces of one surface are rarely one size.
		//
		// ---- QUEUE 223: EVERY PIECE IS PAINTED BY ONE OF FOUR ROUTES -------
		//
		// THE LINE THIS REPLACED WAS THE WHOLE FAULT:
		//     if (Idx < 0 || GBinds[Idx].Status != "RESOLVED") { continue; }
		// A piece whose surface did not resolve to a pack file got NO MATERIAL
		// INSTANCE AT ALL and rendered the engine's default grey: ten card
		// decals, ten multiply decals, six shop interiors and four runs of
		// yellow road paint, which is 30 of the pieces and every lettered
		// fascia, poster, notice, lit interior and road marking in the frame
		// rung 1 is judged on. The route is decided by RouteFor in the tested
		// header and EVERY OUTCOME IS COUNTED, so a piece that still goes
		// unpainted says which rule declined it.
		//
		// ONE SHARED ROUGHNESS FOR THE CARDS, BUILT ONCE AND LAZILY. Ten
		// decals do not need ten identical two-texel textures, and a texture
		// built before the loop would be built on a run with no decals in it.
		UTexture2D* CardRough = nullptr;
		for (size_t P = 0; P < GSpec.Pieces.size(); ++P)
		{
			const Piece& Pc = GSpec.Pieces[P];
			++GPaint.Examined;
			int32 Idx = -1;
			for (size_t I = 0; I < GBinds.size(); ++I)
			{
				if (GBinds[I].Surface == Pc.Surface) { Idx = (int32)I; break; }
			}
			if (Idx < 0)
			{
				// A PIECE WHOSE SURFACE NAME IS IN NO BIND RECORD. The only way
				// in is an empty surface field, which SurfacesAsked skips.
				++GPaint.NoBind;
				continue;
			}
			const bool bPackAnswered = LedgerSurface::IsResolved(GBinds[(size_t)Idx]);
			const LedgerSurface::EPaintRoute Route = LedgerSurface::RouteFor(
				Pc.Surface, Pc.Shape == "decal", bPackAnswered);
			if (Route == LedgerSurface::Paint_None) { ++GPaint.NoBind; continue; }
			AStaticMeshActor** Found = GByName.Find(FString(UTF8_TO_TCHAR(Pc.Name.c_str())));
			if (Found == nullptr || *Found == nullptr) { ++GPaint.NoActor; continue; }
			UStaticMeshComponent* Comp = (*Found)->GetStaticMeshComponent();
			if (Comp == nullptr) { ++GPaint.NoComponent; continue; }

			// ---- THE DECAL ROUTES, WHICH CARRY THEIR OWN PICTURE ----------
			//
			// A DECAL THIS ENGINE CANNOT DRAW IS HIDDEN, AND THAT IS THE UNITY
			// HOST'S OWN RULE rather than an invention here: EmitDecal returns
			// before it creates a GameObject when the image does not load, so
			// an undrawable decal is ABSENT from that scene, not grey in it.
			// Ten grey rectangles standing in the carriageway and on the
			// facades are the worse of the two wrongs in a frame a person is
			// being asked to judge a street by, and every hidden quad is
			// counted and named.
			if (Route == LedgerSurface::Paint_DecalCard
			    || Route == LedgerSurface::Paint_DecalMultiply)
			{
				LedgerSurface::DecalResult D;
				D.Piece = Pc.Name;
				D.Blend = Pc.Surface;
				const LedgerSurface::DecalAsset A = LedgerSurface::SplitDecalAsset(Pc.Asset);
				D.Id = A.Id;
				D.bCropAsked = A.bCropped;
				if (Route == LedgerSurface::Paint_DecalMultiply)
				{
					// A STAIN NEEDS A MODULATE MATERIAL AND THIS BUILD HAS ONE
					// OPAQUE BASE. Blend mode is a property of a MATERIAL and
					// not of an instance, so no parameter on M_LedgerSurface
					// can turn an opaque card into something that only ever
					// darkens what is under it. Pasting the grime opaque would
					// make the count green and the picture worse, which is
					// exactly what this item forbids.
					D.Note = "needs-a-modulate-or-deferred-decal-material/"
					         "make_base_material.py-ships-one-opaque-base";
					D.bHidden = true;
					(*Found)->SetActorHiddenInGame(true);
					++GPaint.DecalNoStainMaterial;
					++GPaint.Hidden;
					GDecalResults.push_back(D);
					continue;
				}
				if (!A.bOk)
				{
					D.Note = "crop-unparseable/fails-closed-exactly-as-"
					         "StreetVignette.SplitAsset-does";
					D.bHidden = true;
					(*Found)->SetActorHiddenInGame(true);
					++GPaint.DecalCropRefused;
					++GPaint.Hidden;
					GDecalResults.push_back(D);
					continue;
				}
				UTexture2D* Pic = nullptr;
				FString LoadedAs = TEXT("decal-root-not-found");
				if (!GDecalRoot.IsEmpty())
				{
					const FString Full = GDecalRoot
						/ FString(UTF8_TO_TCHAR(LedgerSurface::DecalCardLeaf(A.Id).c_str()));
					int32 FW = 0, FH = 0;
					LedgerSurface::CropPx Rect;
					if (IFileManager::Get().FileSize(*Full) > 0)
					{
						Pic = ImportTexture(Full, true, FW, FH, LoadedAs, &A, &Rect);
						D.FullW = FW; D.FullH = FH;
						D.Crop = Rect;
					}
					else
					{
						LoadedAs = TEXT("no-png-at-that-path-under-the-decal-root");
					}
				}
				D.LoadedAs = std::string(TCHAR_TO_UTF8(*LoadedAs));
				if (Pic == nullptr)
				{
					D.Note = "image-did-not-load/" + D.LoadedAs;
					D.bHidden = true;
					(*Found)->SetActorHiddenInGame(true);
					++GPaint.DecalImageMissing;
					++GPaint.Hidden;
					GDecalResults.push_back(D);
					continue;
				}
				D.bLoaded = true;
				UMaterialInstanceDynamic* DMid =
					UMaterialInstanceDynamic::Create(GBaseMaterial, *Found);
				if (DMid == nullptr)
				{
					D.Note = "instance-refused/base-material-" + std::string(
						GBaseMaterial != nullptr ? "loaded" : "MISSING");
					D.bHidden = true;
					(*Found)->SetActorHiddenInGame(true);
					++GPaint.NoInstance;
					++GPaint.Hidden;
					GDecalResults.push_back(D);
					continue;
				}
				DMid->SetTextureParameterValue(
					FName(UTF8_TO_TCHAR(LedgerSurface::MapParam(0))), Pic);
				if (CardRough == nullptr)
				{
					const int RT = LedgerSurface::DecalCardRoughnessTexel();
					CardRough = MakeFlatTexture(RT, RT, RT, false, TEXT("card-roughness"));
				}
				if (CardRough != nullptr)
				{
					DMid->SetTextureParameterValue(
						FName(UTF8_TO_TCHAR(LedgerSurface::MapParam(2))), CardRough);
				}
				// TILING ONE, AND IT IS NOT THE PIECE'S SIZE. The crop IS the
				// fit: a sign tiled 1.1 times across a fascia would repeat a
				// tenth of its own lettering, and TilingFor would hand exactly
				// that for a 2.2 metre band at two metres per tile.
				DMid->SetScalarParameterValue(FName(TEXT("TilingU")), 1.0f);
				DMid->SetScalarParameterValue(FName(TEXT("TilingV")), 1.0f);
				Comp->SetMaterial(0, DMid);
				++GMidsCreated;
				++GPaint.DecalCard;
				++GBinds[(size_t)Idx].PiecesAssigned;
				GBinds[(size_t)Idx].TileU = 1.0;
				GBinds[(size_t)Idx].TileV = 1.0;
				D.bPainted = true;
				D.Note = "opaque-card/cropped-at-decode/roughness-from-the-host-0.08-smoothness";
				GDecalResults.push_back(D);
				continue;
			}

			UMaterialInstanceDynamic* Mid = UMaterialInstanceDynamic::Create(GBaseMaterial, *Found);
			if (Mid == nullptr) { ++GPaint.NoInstance; continue; }
			for (int32 M = 0; M < LedgerSurface::MapCount(); ++M)
			{
				UTexture2D* Tex = Maps[Idx * LedgerSurface::MapCount() + M];
				if (Tex == nullptr) { continue; }
				Mid->SetTextureParameterValue(
					FName(UTF8_TO_TCHAR(LedgerSurface::MapParam(M))), Tex);
			}
			const LedgerSurface::Tiling T = LedgerSurface::TilingFor(Pc, kMetresPerTile);
			Mid->SetScalarParameterValue(FName(TEXT("TilingU")), (float)T.U);
			Mid->SetScalarParameterValue(FName(TEXT("TilingV")), (float)T.V);
			// THE ALBEDO GRADE, QUEUE 299, AND THE ARITHMETIC IS NOT HERE.
			// AlbedoGradeFor is in SurfaceBind.h where g++ runs it before
			// this file is compiled; this supplies the surface name and one
			// piece of live state (whether an albedo texture actually bound)
			// and nothing else. The value is LINEAR because an Unreal vector
			// parameter is read as linear with no conversion, and the header
			// is where that conversion happens and where it is tested.
			//
			// THIS INSTANCE COVERS BOTH ROUTES AND THAT IS THE TRAP. The tint
			// route arrives here too, and its texel ALREADY carries both
			// grades; AlbedoGradeFor returns white for it, which is why the
			// surface name is passed rather than a bare bool.
			const bool bAlbedoBound =
				Maps[Idx * LedgerSurface::MapCount() + 0] != nullptr;
			// THE WETNESS, QUEUE 186, AND BOTH HALVES OF IT GO THROUGH ONE
			// DECISION. WetBindFor says whether this surface is in
			// AssetLibrary's WetSurfaces at all and whether its albedo bound,
			// and WetGradeFor folds the albedo term into the SAME vector
			// parameter the grade already uses: there is no second colour
			// parameter to keep in step. The roughness half is the scalar
			// below, and Unreal's pin is ROUGHNESS where Unity's is
			// SMOOTHNESS, which is why the conversion lives at one named site
			// in the header and not in this file.
			const LedgerSurface::WetBind Wet =
				LedgerSurface::WetBindFor(GBinds[(size_t)Idx].Surface,
				                          bAlbedoBound, GWetness.Value);
			const LedgerSurface::Grade Graded =
				LedgerSurface::WetGradeFor(GBinds[(size_t)Idx].Surface,
				                           bAlbedoBound, GWetness.Value);
			Mid->SetVectorParameterValue(
				FName(UTF8_TO_TCHAR(LedgerSurface::AlbedoGradeParam())),
				FLinearColor((float)Graded.R, (float)Graded.G,
				             (float)Graded.B, 1.0f));
			// SET ON EVERY SURFACE AND NOT ONLY ON THE WET ONES. A dry
			// surface is set to exactly 0.0, which is the material's own
			// default and therefore changes nothing, and the verdict can then
			// say "every instance was set" with a denominator instead of
			// leaving a reader to work out whether a missing write was a
			// decision or a bug.
			Mid->SetScalarParameterValue(
				FName(UTF8_TO_TCHAR(LedgerSurface::WetnessParam())),
				(float)Wet.Wetness);
			Comp->SetMaterial(0, Mid);
			++GMidsCreated;
			// QUEUE 333: AND AN EMISSIVE PIECE KEEPS A REFERENCE TO THE
			// INSTANCE THIS LOOP JUST MADE. Not a second instance: this is
			// the one the component is now wearing, recorded so the
			// per-condition drive can write EmissiveColor on it without
			// re-running the four decisions above and without making a MID
			// the renderer is not using.
			//
			// RECORDED HERE AND NOT ON THE DECAL ROUTE ABOVE, and that is
			// correct rather than an omission: the four lanterns read
			// shape=box surface=metal in the file, so they arrive here, and
			// a decal card carries neither this parameter nor a lamp. Any
			// emissive piece that fell down one of the exits above is
			// absent from this vector, which is what makes held/inFile on
			// the done line a real denominator instead of a restatement.
			if (Pc.Emissive)
			{
				LampPiece LP;
				LP.PieceIndex = P;
				LP.Mid = Mid;
				LP.Comp = Comp;
				GLampPieces.push_back(LP);
			}
			if (Route == LedgerSurface::Paint_Tint) { ++GPaint.Tint; }
			else                                    { ++GPaint.Pack; }
			++GBinds[(size_t)Idx].PiecesAssigned;
			GBinds[(size_t)Idx].TileU = T.U;
			GBinds[(size_t)Idx].TileV = T.V;
			GBinds[(size_t)Idx].Graded = Graded;
			GBinds[(size_t)Idx].bGradeSet = true;
			GBinds[(size_t)Idx].Wet = Wet;
			GBinds[(size_t)Idx].bWetSet = true;
			// AND WHETHER THE ALBEDO BOUND, QUEUE 309, recorded rather than
			// recomputed: ReDriveWetness has to hand WetBindFor and
			// WetGradeFor the SAME second argument this line just did, and
			// Maps is local to this function. bAlbedo on the WetBind above
			// cannot stand in for it, because a wall's albedo can bind and
			// still leave bAlbedo false: that flag is albedo-bound AND
			// in-WetSurfaces, and this is only the first half.
			GBinds[(size_t)Idx].bAlbedoBound = bAlbedoBound;

			// THE READBACK, ONCE PER SURFACE, ON THE FIRST INSTANCE MADE FOR
			// IT. The engine is asked for the parameter straight back, in the
			// same few statements that set it, so nothing in between can
			// explain a difference. 563 pieces would print 563 identical
			// answers to a question that is about the material.
			//
			// NOTHING HERE DECIDES ANYTHING. The comparison, the tolerance,
			// the counts and every printed string are in SurfaceBind.h where
			// g++ runs them before this file is compiled; this supplies the
			// live state and nothing else.
			//
			// WHAT IT CANNOT SEE: this is the game thread's copy. A value
			// that lands here and never reaches the render proxy still reads
			// back same-pointer, which is what the control quads answer.
			LedgerSurface::Readback& RB = GBinds[(size_t)Idx].Read;
			if (!RB.bAsked)
			{
				RB.bAsked = true;
				UTexture2D* Albedo = Maps[Idx * LedgerSurface::MapCount() + 0];
				const FName AlbedoParam(UTF8_TO_TCHAR(LedgerSurface::MapParam(0)));
				UTexture* Back = Mid->K2_GetTextureParameterValue(AlbedoParam);
				RB.bTexSame = (Back != nullptr && Back == (UTexture*)Albedo);
				if (Back == nullptr)
				{
					RB.TexGot = "null";
				}
				else
				{
					// THE ENGINE'S OWN PATH NAME. "Not the same pointer"
					// cannot say whether the answer was the parent's default
					// texture or something else, and those have different
					// next actions.
					const FString Path = Back->GetPathName();
					RB.TexGot = std::string(TCHAR_TO_UTF8(*Path));
				}
				// AFTER UpdateResource, WHICH RAN IN ImportTexture. A texture
				// with no render resource is bound to nothing however good
				// the pointer is.
				RB.bResourceValid = (Albedo != nullptr && Albedo->GetResource() != nullptr);
				RB.SetU = T.U;
				RB.SetV = T.V;
				RB.GotU = (double)Mid->K2_GetScalarParameterValue(FName(TEXT("TilingU")));
				RB.GotV = (double)Mid->K2_GetScalarParameterValue(FName(TEXT("TilingV")));
				RB.bScalarSame = LedgerSurface::ScalarMatches(RB.SetU, RB.GotU)
				              && LedgerSurface::ScalarMatches(RB.SetV, RB.GotV);
				// AND THE WETNESS, ASKED STRAIGHT BACK IN THE SAME BREATH.
				// THIS IS THE KEY THAT ANSWERS "DEAD WRITE OR NOT". A
				// material that does not carry the parameter accepts the set
				// silently and answers zero, so a 0.6000 that comes back
				// 0.0000 is the exact failure queue 186 predicted, and it is
				// a NUMBER on the line rather than an inference from a grey
				// road. WHAT IT CANNOT SEE is what the tiling readback
				// cannot see either: this is the game thread's copy, and a
				// value that lands here and never reaches the render proxy
				// still reads back same-value. The control quads are the
				// render-side half of that question.
				RB.bWetAsked = true;
				RB.SetWet = Wet.Wetness;
				RB.GotWet = (double)Mid->K2_GetScalarParameterValue(
					FName(UTF8_TO_TCHAR(LedgerSurface::WetnessParam())));
				RB.bWetSame = LedgerSurface::ScalarMatches(RB.SetWet, RB.GotWet);
				UMaterialInterface* CompMat = Comp->GetMaterial(0);
				RB.bCompIsMid = (CompMat == (UMaterialInterface*)Mid);
				if (CompMat == nullptr)
				{
					RB.CompGot = "null";
				}
				else
				{
					const FString CompPath = CompMat->GetPathName();
					RB.CompGot = std::string(TCHAR_TO_UTF8(*CompPath));
				}
			}
		}

		// THE RUN'S PAINT CENSUS RIDES THE MATERIALS DONE LINE, which is the
		// line a reader already holds when they ask how much of the street is
		// painted. Appended rather than formatted into that function's buffer
		// for the same reason texRootTried and the readback totals are: the
		// buffer is a cap and a cut line reads as a short one. Every number in
		// the segment is computed in SurfaceBind.h.
		GMaterialsLine = LedgerSurface::MaterialsDoneLine(
			GBinds, TCHAR_TO_UTF8(kBaseMaterialPath), GBaseMaterial != nullptr,
			TCHAR_TO_UTF8(*GTexRoot), GTexRootFiles, GTexRootTried,
			(int)GSpec.Pieces.size(),
			GTexturesImported, GMidsCreated, kMetresPerTile)
			+ LedgerSurface::PaintRouteSegment(GPaint)
			+ LedgerSurface::WetnessDoneSegment(GBinds, GWetness);
		GDecalsLine = LedgerSurface::DecalsDoneLine(
			GDecalResults, std::string(TCHAR_TO_UTF8(*GDecalRoot)),
			GDecalRootFiles, GDecalRootTried);
	}

	// ---- THE CONTROL QUADS -------------------------------------------------
	//
	// A 2x2 TEXTURE BUILT IN CODE. No file, no decoder, no texture root: if
	// this one renders its colours and the pack's textures do not, the fault
	// is downstream of the decode; if neither renders, the fault is not in
	// the pack at all. Every colour and the buffer order come out of
	// SurfaceBind.h, so the verdict names the same four colours the memcpy
	// wrote rather than a second copy of them typed here.
	UTexture2D* MakeControlTexture()
	{
		UTexture2D* Tex = UTexture2D::CreateTransient(2, 2, PF_B8G8R8A8);
		if (Tex == nullptr) { return nullptr; }
		Tex->SRGB = true;
		// NEAREST, BECAUSE A 2x2 BILINEAR TEXTURE IS A GRADIENT RATHER THAN
		// FOUR COLOURS. The reading survives either filter, since a blend of
		// four saturated corners is still nothing like a grey checker, but
		// four flat quadrants can be sampled with one patch.
		Tex->Filter = TF_Nearest;
		// KEPT ALIVE EXPLICITLY, for the reason the imported textures are: a
		// transient texture whose only reference is a material instance is
		// the shape of object this engine collects between two ticks.
		Tex->AddToRoot();
		uint8 Px[16];
		for (int32 I = 0; I < LedgerSurface::ControlColourCount(); ++I)
		{
			int R = 0, G = 0, B = 0;
			LedgerSurface::ControlColour(I, R, G, B);
			Px[I * 4 + 0] = (uint8)B;   // the platform data is BGRA
			Px[I * 4 + 1] = (uint8)G;
			Px[I * 4 + 2] = (uint8)R;
			Px[I * 4 + 3] = 255;
		}
		void* Dest = Tex->GetPlatformData()->Mips[0].BulkData.Lock(LOCK_READ_WRITE);
		FMemory::Memcpy(Dest, Px, sizeof(Px));
		Tex->GetPlatformData()->Mips[0].BulkData.Unlock();
		Tex->UpdateResource();
		return Tex;
	}

	// THE CONTROLS STAND IN FRONT OF THE CAMERA THE FIRST SHOT USES, read out
	// of the file rather than named here, so a spec whose first shot moves
	// takes its controls with it. Which camera answered is printed on every
	// quad line.
	const Camera* ControlCamera()
	{
		if (GSpec.Cameras.empty()) { return nullptr; }
		for (size_t I = 0; I < GSpec.Cameras.size() && !GSpec.Shots.empty(); ++I)
		{
			if (GSpec.Cameras[I].Id == GSpec.Shots[0].CameraId) { return &GSpec.Cameras[I]; }
		}
		return &GSpec.Cameras[0];
	}

	// THREE PLANES, ONE SIZE, ONE DISTANCE. The placement, the rotation, the
	// projection and every printed string are in SurfaceBind.h; this asks the
	// engine for actors and reads back what it got.
	void SpawnControlQuads(UWorld* World, UStaticMesh* Plane)
	{
		const Camera* C = ControlCamera();
		if (World == nullptr || Plane == nullptr || C == nullptr || GBaseMaterial == nullptr)
		{
			// NOTHING SPAWNED IS A FINDING AND IT NAMES WHICH OF THE FOUR
			// THINGS WAS MISSING: no plane mesh in the build and no base
			// material to instance are different next actions, and neither is
			// "the control quads did not help".
			GQuadDone = LedgerSurface::ControlQuadsDoneLine(GQuads, GBaseMaterial != nullptr);
			GQuadDone += std::string(" controlQuadsMissing=world.")
			           + (World == nullptr ? "NO" : "yes")
			           + "/plane." + (Plane == nullptr ? "NO" : "yes")
			           + "/camera." + (C == nullptr ? "NO" : "yes")
			           + "/base." + (GBaseMaterial == nullptr ? "NO" : "yes");
			return;
		}
		for (int32 I = 0; I < LedgerSurface::ControlQuadCount(); ++I)
		{
			const LedgerSurface::QuadPlace P = LedgerSurface::ControlQuadPlace(*C, I);
			LedgerSurface::QuadResult R;
			FActorSpawnParameters Params;
			Params.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
			AStaticMeshActor* A = World->SpawnActor<AStaticMeshActor>(
				AStaticMeshActor::StaticClass(), FVector::ZeroVector, FRotator::ZeroRotator, Params);
			if (A != nullptr)
			{
				R.bSpawned = true;
				// MOBILITY BEFORE THE TRANSFORM, for the reason SpawnPiece
				// sets it: a spawned StaticMeshActor is static mobility and
				// cannot be moved, and a static actor with no built lighting
				// renders unlit.
				MakeMovable(A);
				UStaticMeshComponent* Comp = A->GetStaticMeshComponent();
				if (Comp != nullptr)
				{
					Comp->SetMobility(EComponentMobility::Movable);
					Comp->SetStaticMesh(Plane);
					Comp->SetCollisionEnabled(ECollisionEnabled::NoCollision);
					// A CONTROL CASTS NO SHADOW. It is not part of the street
					// and a shadow of it falling across the road would be a
					// change to the frame the street is measured in.
					Comp->SetCastShadow(false);
				}
				GQuadActors.Add(A);
				A->SetActorScale3D(FVector((float)P.SizeM, (float)P.SizeM, 1.0f));
				A->SetActorLocationAndRotation(
					FVector(P.XCm, P.YCm, P.ZCm),
					FRotator((float)P.EnginePitchDeg, (float)P.EngineYawDeg,
					         (float)P.EngineRollDeg));
				// READ BACK, NEVER ASSUMED. A transform that was asked for is
				// not a transform that took.
				const FVector Got = A->GetActorLocation();
				R.bRead = true;
				R.ReadXCm = (double)Got.X;
				R.ReadYCm = (double)Got.Y;
				R.ReadZCm = (double)Got.Z;
				UMaterialInstanceDynamic* Mid = UMaterialInstanceDynamic::Create(GBaseMaterial, A);
				if (Mid != nullptr)
				{
					R.bMidMade = true;
					if (P.bBindTexture)
					{
						if (GControlTex == nullptr) { GControlTex = MakeControlTexture(); }
						if (GControlTex != nullptr)
						{
							R.bTexMade = true;
							const FName Param(UTF8_TO_TCHAR(LedgerSurface::MapParam(0)));
							Mid->SetTextureParameterValue(Param, GControlTex);
							UTexture* Back = Mid->K2_GetTextureParameterValue(Param);
							R.bTexReadback = (Back != nullptr && Back == (UTexture*)GControlTex);
							R.bTexResource = (GControlTex->GetResource() != nullptr);
						}
					}
					// THE SCALARS GO ON EVERY CONTROL, INCLUDING THE COLOUR
					// ONE. tile1 and tile8 differ in nothing else, which is
					// what makes the pair readable.
					Mid->SetScalarParameterValue(FName(TEXT("TilingU")), (float)P.TileU);
					Mid->SetScalarParameterValue(FName(TEXT("TilingV")), (float)P.TileV);
					if (Comp != nullptr)
					{
						Comp->SetMaterial(0, Mid);
						R.bCompIsMid = (Comp->GetMaterial(0) == (UMaterialInterface*)Mid);
					}
				}
#if WITH_EDITOR
				A->SetActorLabel(FString(TEXT("control_quad_"))
				                 + FString(UTF8_TO_TCHAR(P.Id.c_str())));
#endif
			}
			GQuads.push_back(R);
			GQuadLines.push_back(
				LedgerSurface::ControlQuadLine(*C, P, R, kShotW, kShotH));
		}
		GQuadDone = LedgerSurface::ControlQuadsDoneLine(GQuads, GBaseMaterial != nullptr);
	}

	bool Tick(float)
	{
		++GTicks;
		++GPhaseTicks;
		const double Now = FPlatformTime::Seconds();
		if (GStart == 0.0) { GStart = Now; GPhaseStart = Now; GLastTick = Now; }
		const double Delta = Now - GLastTick;
		GLastTick = Now;

		switch (GPhase)
		{
		case EPhase::WaitWorld:
		{
			UWorld* World = GameWorld();
			if (World == nullptr && (Now - GPhaseStart) <= kWorldCeiling) { return true; }
			if (World == nullptr)
			{
				// A WORLD THAT NEVER CAME IS A FINDING, and it is a different
				// one from a street that would not build.
				GSceneLine = "sceneStatus=NOTHING-EMITTED piecesEmitted=0/"
				           + std::to_string(GSpec.HeaderPieces)
				           + " sceneNote=world-ceiling-bit-at-45s";
				Finish(CaptureDoneLine(0, 0, 0, 0, Now - GStart, GTicks));
				return false;
			}
			BuildScene(World, /*bInteractive=*/false);
			// UNCAP THE FRAME RATE BEFORE ANYTHING IS TIMED. A frame time
			// measured against a 60 Hz cap is a measurement of the cap, and
			// it would read as a suspiciously round 16.67 in the verdict.
			if (GEngine != nullptr)
			{
				GEngine->Exec(World, TEXT("t.MaxFPS 0"));
				GEngine->Exec(World, TEXT("r.VSync 0"));
			}
			GPhase = EPhase::ApplyShot;
			GPhaseStart = Now; GPhaseTicks = 0;
			return true;
		}
		case EPhase::ApplyShot:
		{
			if (GShotIndex >= (int32)GSpec.Shots.size())
			{
				// ---- THE DETERMINISM REPEAT, LAST, OF THE FIRST SHOT -----
				//
				// The same camera and the same condition as shot 1, arrived
				// at from the opposite end of the run: every other shot,
				// every condition change and every light probe stood between
				// the two. It writes to a scratch path, pushes no shot line
				// and moves no tally; the only thing it produces is one
				// difference, and that difference is what says whether any
				// cross-shot comparison in this run means anything.
				if (!GRepeatRan && !GSpec.Shots.empty() && GFirstBgra.Num() > 0)
				{
					GRepeatRan  = true;
					GRepeating  = true;
					GShotIndex  = 0;
					++GShotPass;
					GPhaseStart = Now; GPhaseTicks = 0;
					return true;
				}
				if (!GRepeatRan)
				{
					// NOTHING TO BE IDENTICAL TO IS ITS OWN READING and is
					// not a zero difference.
					LedgerFrame::RepeatDiff Nothing;
					GRigLine = LedgerFrame::RigDeterminismLine(
						GFirstShotId, GShotIndex, (int)GSpec.Shots.size(),
						"NO-FIRST-FRAME", Nothing);
				}
				FinishNormally();
				return false;
			}
			const Shot& S = GSpec.Shots[GShotIndex];
			const Camera* C = FindCamera(S.CameraId);
			const Condition* Cond = FindCondition(S.ConditionId);
			if (C == nullptr || Cond == nullptr)
			{
				// A SHOT NAMING A CAMERA OR A CONDITION THE FILE DOES NOT
				// CARRY IS COUNTED, not skipped in silence.
				++GNoFile;
				GShotCam = LedgerVignette::ShotCamIn();
				GShotCam.CamId  = S.CameraId;
				GShotCam.Status = "NO-SUCH-CAMERA";
				GShotLines.push_back(ShotLine(S.Id, S.CameraId, S.ConditionId, 0.0, "none",
					-1.0, kTimedFrames, kWarmFrames, kShotW, kShotH, 0.0, 0.0, 0,
					"NO-SUCH-CAMERA-OR-CONDITION", "none", "nothing-measured")
					+ " " + ShotCamAndCaptureNow()
					+ " " + ShotControlQuadsNow(S, false));
				++GShotIndex;
				// A SKIPPED SHOT IS STILL A PASS. Without this the NEXT
				// shot's preamble would read as already written and it
				// would inherit this one's control quads and sky capture.
				++GShotPass;
				return true;
			}
			// THE CONTROLS ARE HIDDEN FOR EVERY SHOT BUT THEIR OWN, and the
			// write happens ONCE PER SHOT rather than once per settle tick,
			// because this phase is re-entered while the condition settles
			// and a per-tick write is both a lie in the tally and a rebuild
			// asked for four times. A run with no quads spawned counts
			// nothing, so the verdict line reads nothing-measured rather
			// than claiming a hide that had nothing to hide.
			// ONCE PER PASS, NOT ONCE PER SETTLE TICK AND NOT ONCE PER SHOT
			// INDEX. This phase is re-entered while the condition settles, so
			// a per-tick write is both a lie in the tally and a rebuild asked
			// for a hundred times; keying it on the PASS is what lets the
			// determinism repeat re-run shot 1's preamble in full rather than
			// inheriting whatever the last shot left behind. The sky epoch is
			// bumped here for the same reason.
			if (GPassPrepared != GShotPass)
			{
				GPassPrepared = GShotPass;
				++GWantSkyEpoch;
				if (GQuadActors.Num() > 0)
				{
					const Camera* QuadCam = ControlCamera();
					const bool bShow = LedgerSurface::ControlQuadsVisibleFor(
						S.CameraId, QuadCam != nullptr ? QuadCam->Id : std::string());
					for (int32 QI = 0; QI < GQuadActors.Num(); ++QI)
					{
						if (GQuadActors[QI] != nullptr)
						{
							GQuadActors[QI]->SetActorHiddenInGame(!bShow);
						}
					}
					// THE REPEAT IS NOT A SHOT AND IS NOT COUNTED AS ONE. It
					// writes the same visibility so its picture matches, and
					// stays out of the tally so the denominator keeps
					// counting the shots the file asked for.
					if (!GRepeating)
					{
						++GQuadShotsSeen;
						if (!bShow)
						{
							++GQuadHidden;
							if (!GQuadHiddenIds.empty()) { GQuadHiddenIds += ";"; }
							GQuadHiddenIds += S.Id;
						}
					}
				}
			}
			ApplyCondition(*Cond);
			PlaceCamera(GameWorld(), *C);
			GFrameMs.clear();
			GNote = TEXT("none");
			GTriedHighResThisShot = false;
			GSizeTracker = -1;
			if ((Now - GPhaseStart) < kSettleAfterCondition) { return true; }
			GPhase = EPhase::Warm;
			GPhaseStart = Now; GPhaseTicks = 0;
			return true;
		}
		case EPhase::Warm:
		{
			// WARM-UP FRAMES ARE DISCARDED, and they are discarded for a
			// named reason: the first frames after a condition change compile
			// shader variants, which is a real cost and not the one a
			// comparison is about.
			if (GPhaseTicks < kWarmFrames) { return true; }
			// QUEUE 325: WHAT THIS CAPTURE ACTUALLY WAITED FOR, recorded at
			// the moment the phase ends rather than assumed from the constant.
			GWarmTicksAtAsk = GPhaseTicks;
			GPhase = EPhase::Timed;
			GPhaseStart = Now; GPhaseTicks = 0;
			return true;
		}
		case EPhase::Timed:
		{
			if ((int32)GFrameMs.size() < kTimedFrames)
			{
				GFrameMs.push_back(Delta * 1000.0);
				return true;
			}
			GPhase = EPhase::Ask;
			GPhaseStart = Now; GPhaseTicks = 0;
			return true;
		}
		case EPhase::Ask:
		{
			const Shot& S = GSpec.Shots[GShotIndex];
			GAskedPath = GProbing ? ProbePngPath()
			                      : (GRepeating ? RepeatPngPath() : ShotPngPath(S));
			IFileManager::Get().Delete(*GAskedPath, false, true, true);
			GSizeTracker = -1;
			// QUEUE 325: THE SHUTTER'S OWN CLOCK STARTS HERE, and the two
			// series counts are what this capture had when it fired. Per
			// capture, overwritten by the next one, read by the line that
			// describes the frame this one produced.
			GTimedAtAsk      = (int32)GFrameMs.size();
			GAskStarted      = Now;
			GSecondsToSettle = -1.0;
			GCaptureSettled  = false;
			if (!GUseHighRes)
			{
				// CANDIDATE A, AND AN ABSOLUTE PATH ON PURPOSE: a relative
				// one resolves against the engine's screenshot directory,
				// which would put the file where nothing is looking and read
				// as no file at all.
				FScreenshotRequest::RequestScreenshot(GAskedPath, false, false);
			}
			else
			{
				if (GEngine != nullptr)
				{
					GEngine->Exec(GameWorld(), *FString::Printf(TEXT("HighResShot %dx%d"), kShotW, kShotH));
				}
			}
			GPhase = EPhase::WaitFile;
			GPhaseStart = Now; GPhaseTicks = 0;
			return true;
		}
		case EPhase::WaitFile:
		{
			if (!GUseHighRes)
			{
				if (SizeSettled(GAskedPath, GSizeTracker))
				{
					// QUEUE 325: STOPPED BEFORE THE FRAME IS MEASURED, so the
					// number on the line is the wait and not the wait plus
					// whatever measuring it cost.
					GSecondsToSettle = Now - GAskStarted;
					GCaptureSettled  = true;
					AfterFrame(true);
					GPhaseStart = Now; GPhaseTicks = 0;
					return true;
				}
			}
			else
			{
				int32 Count = 0;
				const FString Newest = NewestPngUnder(
					FPaths::ConvertRelativePathToFull(FPaths::ProjectSavedDir()), Count);
				if (!Newest.IsEmpty() && SizeSettled(Newest, GSizeTracker))
				{
					GSecondsToSettle = Now - GAskStarted;
					GCaptureSettled  = true;
					// ONE NAME FOR THE FILE THE STEP COLLECTS, whatever
					// produced it: HighResShot picks its own filename under
					// Saved and the step should not have to know which
					// candidate won.
					IFileManager::Get().Copy(*GAskedPath, *Newest, true, true);
					IFileManager::Get().Delete(*Newest, false, true, true);
					AfterFrame(true);
					GPhaseStart = Now; GPhaseTicks = 0;
					return true;
				}
			}
			if ((Now - GPhaseStart) < kFileCeiling) { return true; }
			if (!GUseHighRes && !GTriedHighResThisShot)
			{
				// CANDIDATE B, TRIED ONCE AND THEN ADOPTED FOR THE WHOLE RUN.
				// Both are documented and neither has ever produced a file on
				// this machine, so one dispatch answers which works rather
				// than two; trying A first on every shot afterwards would
				// cost 25 wasted seconds per shot for no new information.
				GNote = TEXT("requestScreenshot-wrote-nothing-in-25s/switched-to-HighResShot");
				GUseHighRes = true;
				GCaptureVia = "highresshot";
				GTriedHighResThisShot = true;
				GPhase = EPhase::Ask;
				GPhaseStart = Now; GPhaseTicks = 0;
				return true;
			}
			GNote = GUseHighRes ? TEXT("neither-candidate-wrote-a-file-in-25s")
			                    : TEXT("requestScreenshot-wrote-nothing-in-25s");
			AfterFrame(false);
			GPhaseStart = Now; GPhaseTicks = 0;
			return true;
		}
		default:
			return false;
		}
	}
}

namespace LedgerVignetteShot
{
	void Start()
	{
		if (!LoadSpec())
		{
			GPhase = EPhase::Done;
			WriteVerdict("captureStatus=NOTHING-MEASURED shotsWrote=0/0 shotsBlank=0/0"
			             " shotsNoFile=0/0 captureSeconds=0.00 captureTicks=0");
			FPlatformMisc::RequestExit(false);
			return;
		}
		GPhase = EPhase::WaitWorld;
		GTicker = FTSTicker::GetCoreTicker().AddTicker(
			FTickerDelegate::CreateStatic(&Tick), 0.0f);
	}

	// QUEUE 138 ITEM 1. See VignetteShot.h for the call-site contract; this
	// is what it does.
	void BuildInteractiveStreet(UWorld* World)
	{
		if (GInteractiveBuilt) { return; }
		if (World == nullptr) { return; }
		GInteractiveBuilt = true;

		if (!LoadSpec())
		{
			UE_LOG(LogTemp, Error, TEXT("LedgerProbe interactive street: %s"),
			       *FString(UTF8_TO_TCHAR(GSceneLine.c_str())));
			return;
		}

		BuildScene(World, /*bInteractive=*/true);

		// LIGHT IT. BuildScene spawns the sun and the three fill lights at
		// zero intensity (ApplyCondition is their one owner, named at the
		// top of this file) and the automation only ever turns them on by
		// applying one of the file's named conditions per shot; this path
		// has no shots, so it has to call the same owner directly or a
		// person would be walking a street lit only by the lanterns and
		// window practicals, which are the ones NOT zeroed at spawn.
		// overcast_day is conditions[0] in the shared file and the
		// condition the automation's own first shot uses, so this is not a
		// second opinion about which light is "the" street light.
		const Condition* Day = FindCondition("overcast_day");
		if (Day != nullptr) { ApplyCondition(*Day); }
		else if (!GSpec.Conditions.empty()) { ApplyCondition(GSpec.Conditions[0]); }
		else
		{
			UE_LOG(LogTemp, Error,
			       TEXT("LedgerProbe interactive street: the shared file named no condition at all"));
		}

		// PLACE THE PLAYER. cam_A is the shared file's own first camera and
		// the position the automation photographs from a human eye height
		// on the east footway; starting a person there rather than at an
		// invented coordinate is the same "no second opinion about the
		// street" rule PlaceCamera already follows for the automation
		// camera. Spawned rather than hand-placed: this project's rule
		// against a hand-edited scene applies to a PlayerStart exactly as
		// it does to a wall, and /Engine/Maps/Entry is an engine map this
		// project does not own to edit.
		const Camera* StartCam = FindCamera("cam_A");
		if (StartCam == nullptr && !GSpec.Cameras.empty()) { StartCam = &GSpec.Cameras[0]; }
		if (StartCam == nullptr)
		{
			UE_LOG(LogTemp, Error,
			       TEXT("LedgerProbe interactive street: the shared file named no camera to start the player at"));
			return;
		}
		// A GENEROUS NAMED CLEARANCE ABOVE THE GROUND, NOT A MEASURED
		// CAPSULE HALF-HEIGHT. ALedgerCharacter sets its own capsule to
		// 34x88 (LedgerCharacter.cpp), but matching that number here
		// exactly would be a second copy of it that could drift from the
		// first; a spawn that starts clear of the pavement and falls the
		// rest of the way under gravity does not need to match it, and a
		// spawn that starts too LOW would not correct itself the same way.
		const float kClearAboveGroundM = 1.1f;
		const FVector At(StartCam->X * 100.0, StartCam->Z * 100.0,
		                 (StartCam->GroundY + kClearAboveGroundM) * 100.0);
		// FACING DOWN THE STREET, AT THE SAME YAW cam_A USES. The file's
		// yaw is already this engine's yaw with no conversion, exactly as
		// PlaceCamera uses it above; no pitch or roll on a PlayerStart, the
		// character stands upright.
		const FRotator Facing(0.0f, (float)StartCam->YawDeg, 0.0f);
		FActorSpawnParameters Params;
		Params.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
		APlayerStart* PStart = World->SpawnActor<APlayerStart>(
			APlayerStart::StaticClass(), At, Facing, Params);
		// READ BACK, NEVER ASSUMED: a spawn that returned null is a
		// GameMode with nowhere to start a player, and this is the one
		// line that would say so.
		UE_LOG(LogTemp, Log,
		       TEXT("LedgerProbe interactive street: playerStart=%s at %s facing yaw %.1f, street pieces=%d"),
		       PStart != nullptr ? TEXT("spawned") : TEXT("SPAWN-FAILED"),
		       *At.ToString(), Facing.Yaw, (int32)GSpec.Pieces.size());
	}

	// THE WALK PROBE'S THREE READS. Declared in VignetteShot.h; each one
	// returns a global this same translation unit already maintains, so a
	// walk run and a vignette run can never report two different counts
	// for one fact. None of the three builds anything: a run that never
	// called BuildScene reads GSceneLine's untouched default
	// ("piecesEmitted=0/0"), GQuads empty, and GByName empty, which is
	// exactly the "nothing measured" state a caller that starts too early
	// ought to see.
	FString StreetSceneLine()
	{
		return FString(UTF8_TO_TCHAR(SceneLineWithSky().c_str()));
	}

	int32 ControlQuadsSpawnedCount()
	{
		return (int32)GQuads.size();
	}

	AActor* FindStreetPiece(const FString& Name)
	{
		AStaticMeshActor* const* Found = GByName.Find(Name);
		return (Found != nullptr) ? static_cast<AActor*>(*Found) : nullptr;
	}

	// THE CRIME PROBE'S ONE HELPER, NOT FIVE. Ruling of 2026-09-08 section 2:
	// a thin export over the SpawnPiece this file already uses for all 593
	// street pieces, so a shard, a brick, a stand-in body and the yard floor
	// are placed by the same code path, with the same frame mapping, the same
	// movable mobility and the same interactive collision as a kerbstone.
	//
	// CentreM AND SizeM ARE IN THE SHARED FILE'S OWN FRAME (x along, y up, z
	// across), exactly as a Piece states them, and NOT in the engine's. The
	// one place that converts between the two is SpawnPiece, three hundred
	// lines above; a second converter at a call site is how two frames drift
	// apart, and this probe's whole geometry would then be wrong in a way no
	// count could see.
	//
	// bInteractive=true, ALWAYS: every caller of this is a person-scale
	// object in a street somebody is walking and tracing through. The
	// automation's collision-off saving applies to a frame it is timing, and
	// nothing here is in one.
	//
	// THE SURFACE IS RECORDED AND NOT BOUND. BindSurfaces runs once inside
	// BuildScene, over GSpec.Pieces, long before any of these exist, so a
	// piece spawned here carries the mesh's default material. The crime
	// verdict prints that as probePiecesMaterialBound=0/N with the reason
	// rather than leaving a reader to wonder why a shard is grey.
	AActor* SpawnProbePiece(UWorld* World, const FString& Name,
	                        const FVector& CentreM, const FVector& SizeM,
	                        const FString& Shape, const FString& Surface)
	{
		if (World == nullptr) { return nullptr; }
		UStaticMesh* Cube = LoadShape(TEXT("/Engine/BasicShapes/Cube.Cube"));
		UStaticMesh* Cyl  = LoadShape(TEXT("/Engine/BasicShapes/Cylinder.Cylinder"));
		const bool bCyl = (Shape == TEXT("cyl"));
		UStaticMesh* Mesh = bCyl ? Cyl : Cube;
		if (Mesh == nullptr) { return nullptr; }

		// QUALIFIED, not leaned on the using-directive inside the unnamed
		// namespace three hundred lines above: this function is outside that
		// block and the leak of a using-directive out of an unnamed namespace
		// is a rule most readers would have to look up.
		LedgerVignette::Piece P;
		P.Name    = std::string(TCHAR_TO_UTF8(*Name));
		P.Shape   = bCyl ? "cyl" : "box";
		P.Surface = std::string(TCHAR_TO_UTF8(*Surface));
		P.X = CentreM.X; P.Y = CentreM.Y; P.Z = CentreM.Z;
		P.SX = SizeM.X;  P.SY = SizeM.Y;  P.SZ = SizeM.Z;
		// The same scale mapping BuildScene uses for a box and a cylinder
		// alike: the engine's basic shapes are one metre, so the scale IS the
		// size, and the cylinder's axis is local +Z which is the file's +y.
		const FVector Scale((float)P.SX, (float)P.SZ, (float)P.SY);
		AStaticMeshActor* A = SpawnPiece(World, Mesh, P, Scale, /*bInteractive=*/true);
		if (A == nullptr) { return nullptr; }
		GProbeByName.Add(Name, A);
		return static_cast<AActor*>(A);
	}

	// THE NAME A TRACE HIT, WHICH IS THE HALF OF AN OCCLUSION READING THAT
	// SAYS ANYTHING. SpawnPiece only calls SetActorLabel under WITH_EDITOR,
	// so in a packaged build every one of these actors answers GetName() with
	// StaticMeshActor_NNN and a verdict saying actorBlocker=StaticMeshActor_213
	// names nothing a reader can look up. FindStreetPiece is name-to-actor
	// only, so this is its reverse and it is the reason this export exists.
	//
	// READ-ONLY, AND BOTH MAPS. It adds to neither, so the ruling's own
	// check (one grep for the street map's single Add call) still finds
	// exactly one site, in BuildScene. The probe map is searched
	// second so a street piece can never be shadowed by a probe piece of the
	// same name, and a blocker that IS a probe piece (the yard floor, a
	// stand-in body) names itself rather than falling through to the engine's
	// number.
	FString StreetPieceNameOf(const AActor* Actor)
	{
		if (Actor == nullptr) { return FString(); }
		for (TMap<FString, AStaticMeshActor*>::TConstIterator It(GByName); It; ++It)
		{
			if (It.Value() == Actor) { return It.Key(); }
		}
		for (TMap<FString, AStaticMeshActor*>::TConstIterator It(GProbeByName); It; ++It)
		{
			if (It.Value() == Actor) { return It.Key(); }
		}
		return FString();
	}
}
