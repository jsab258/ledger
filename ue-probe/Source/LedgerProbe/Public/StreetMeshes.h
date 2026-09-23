// StreetMeshes.h - THE STREET FROM BLENDER, AS UNREAL READS IT. 23 September.
//
// Jafar's ruling of the morning: Blender is for shapes and layout, all
// look-development happens in Unreal against the sheet, and the mirror is
// fixed once where Blender work crosses into Unreal. The crossing is
// tools/art-recipes/terrace-front.py --export-glb, which writes
// production/assets/street/quay-street.glb (the geometry, reflected so it
// arrives the right way round) and quay-street.json beside it (what each mesh
// was in Blender, and which of the scene file's own pieces the street stands
// in for). tools/ue/import_street.py makes the GLB into static meshes; this
// header is the pure half of reading the JSON, so g++ and cl run it in
// ue-probe/tests/vignette-spec-test.cpp before the engine ever does.
//
// NOTHING HERE DECIDES A LOOK. The colours and roughness in the sidecar are
// Blender's, carried as TARGETS; the first Unreal frame paints them flat so
// the geometry can be checked, and the textured look is the next item.

#pragma once

#include "VignetteSpec.h"

#include <cmath>
#include <string>
#include <vector>

namespace LedgerStreet
{
	// Where the importer puts a mesh: Interchange makes a folder named after
	// the file and a StaticMeshes folder inside it, and names each mesh after
	// its glTF node. Measured on UE 5.8 on 23 September by a throwaway import,
	// not assumed: 52 of 52 landed at exactly this path.
	inline const char* PackageDir() { return "/Game/Ledger/Street/quay-street/StaticMeshes"; }

	inline std::string ObjectPath(const std::string& Mesh)
	{
		return std::string(PackageDir()) + "/" + Mesh + "." + Mesh;
	}

	struct Row
	{
		std::string Mesh;          // street_brick_red
		std::string Material;      // brick_red, sign_generated/fascia_ritas_pawn
		std::string Base;          // the recipe's base material name
		bool        bHasRgb;
		double      R, G, B;       // LINEAR, as Blender held them
		double      Roughness;     // -1 when the sidecar did not say
		std::string Decal;         // "" or the picture, repository-relative or under the decal root
		std::string Emit;          // "" or room/net
		// THE PHOTOGRAPH THIS SURFACE WEARS, and how many metres of wall one
		// copy of it covers: the export's UVs are in metres, so the tiling
		// is one over this. "" and 0 for a flat-painted surface.
		std::string SurfaceMap;
		double      TileM;
		// THE PHOTOGRAPH'S OWN AVERAGE, linear, so the authored colour can be
		// laid over its pattern the way Blender lays it.
		bool        bHasMean;
		double      MeanR, MeanG, MeanB;
		// BLENDER'S GLOW, day and night, a target in Blender's units; below
		// zero means the surface does not glow.
		double      EmitDay, EmitNight;
		// A DRAWN SURFACE, repository-relative without its .png, and the
		// width and height one copy covers. It already carries the authored
		// colour, so it is graded by one, and it wins over the photograph.
		std::string DrawnMap;
		double      DrawnW, DrawnH;
		Row() : bHasRgb(false), R(0), G(0), B(0), Roughness(-1.0), TileM(0.0),
		        bHasMean(false), MeanR(0), MeanG(0), MeanB(0), EmitDay(-1.0), EmitNight(-1.0),
		        DrawnW(0.0), DrawnH(0.0) {}
	};

	// HOW MANY COPIES OF THE PHOTOGRAPH PER METRE, or 0 when there is no
	// photograph or no size to tile it at.
	inline double TilesPerMetre(const Row& Rw)
	{
		return (!Rw.SurfaceMap.empty() && Rw.TileM > 1e-6) ? 1.0 / Rw.TileM : 0.0;
	}

	// THE COLOUR LAID OVER THE PHOTOGRAPH: the authored colour over the map's
	// own average, per channel, capped at 6 as the recipe caps it. White when
	// either half is missing, which leaves the photograph's own colour.
	struct Grade { double R, G, B; };
	inline Grade PaletteOverPhoto(const Row& Rw)
	{
		Grade Gr = {1.0, 1.0, 1.0};
		if (!Rw.bHasRgb || !Rw.bHasMean) { return Gr; }
		const double In[3] = {Rw.R, Rw.G, Rw.B};
		const double Mn[3] = {Rw.MeanR, Rw.MeanG, Rw.MeanB};
		double Out[3];
		for (int I = 0; I < 3; ++I)
		{
			const double V = Mn[I] > 1e-4 ? In[I] / Mn[I] : 1.0;
			Out[I] = V < 0.0 ? 0.0 : (V > 6.0 ? 6.0 : V);
		}
		Gr.R = Out[0]; Gr.G = Out[1]; Gr.B = Out[2];
		return Gr;
	}

	struct Replaces
	{
		std::vector<std::string> Prefixes;
		std::vector<std::string> Shapes;
		std::vector<std::string> HeldPropAssets;
	};

	struct Sidecar
	{
		std::vector<Row> Rows;
		Replaces         Replaced;
	};

	inline void StrList(const LedgerVignette::Value* V, std::vector<std::string>& Out)
	{
		if (V == 0 || V->Type != LedgerVignette::T_ARR) { return; }
		for (size_t I = 0; I < V->Arr.size(); ++I)
		{
			if (V->Arr[I].Type == LedgerVignette::T_STR) { Out.push_back(V->Arr[I].Str); }
		}
	}

	inline std::string StrOr(const LedgerVignette::Value& O, const char* Key)
	{
		const LedgerVignette::Value* V = O.Find(Key);
		return (V != 0 && V->Type == LedgerVignette::T_STR) ? V->Str : std::string();
	}

	// FAILS CLOSED ON THE SHAPE AND SOFT ON THE DETAIL. A file that is not the
	// sidecar is an error with a reason; a row missing its colour is kept with
	// bHasRgb false, because a mesh with no colour is still geometry to see.
	inline bool ParseSidecar(const std::string& Text, Sidecar& Out, std::string& Err)
	{
		using namespace LedgerVignette;
		Err.clear();
		Out = Sidecar();
		Reader R(Text);
		Value Root;
		if (!R.ReadValue(Root)) { Err = "sidecar-unreadable/" + R.Err; return false; }
		if (Root.Type != T_OBJ) { Err = "sidecar-not-an-object"; return false; }
		const Value* Meshes = Root.Find("meshes");
		if (Meshes == 0 || Meshes->Type != T_ARR) { Err = "sidecar-has-no-meshes-list"; return false; }
		for (size_t I = 0; I < Meshes->Arr.size(); ++I)
		{
			const Value& M = Meshes->Arr[I];
			if (M.Type != T_OBJ) { continue; }
			Row Rw;
			Rw.Mesh = StrOr(M, "mesh");
			if (Rw.Mesh.empty()) { continue; }
			Rw.Material = StrOr(M, "material");
			Rw.Base = StrOr(M, "base_material");
			Rw.Decal = StrOr(M, "decal");
			Rw.Emit = StrOr(M, "decal_emit");
			const Value* Rgb = M.Find("linear_rgb");
			if (Rgb != 0 && Rgb->Type == T_ARR && Rgb->Arr.size() >= 3
			    && Rgb->Arr[0].Type == T_NUM && Rgb->Arr[1].Type == T_NUM && Rgb->Arr[2].Type == T_NUM)
			{
				Rw.bHasRgb = true;
				Rw.R = Rgb->Arr[0].Num; Rw.G = Rgb->Arr[1].Num; Rw.B = Rgb->Arr[2].Num;
			}
			const Value* Ro = M.Find("roughness");
			if (Ro != 0 && Ro->Type == T_NUM) { Rw.Roughness = Ro->Num; }
			Rw.SurfaceMap = StrOr(M, "surface_map");
			const Value* Tm = M.Find("tile_m");
			if (Tm != 0 && Tm->Type == T_NUM) { Rw.TileM = Tm->Num; }
			const Value* Mean = M.Find("texture_mean");
			if (Mean != 0 && Mean->Type == T_ARR && Mean->Arr.size() >= 3
			    && Mean->Arr[0].Type == T_NUM && Mean->Arr[1].Type == T_NUM && Mean->Arr[2].Type == T_NUM)
			{
				Rw.bHasMean = true;
				Rw.MeanR = Mean->Arr[0].Num; Rw.MeanG = Mean->Arr[1].Num; Rw.MeanB = Mean->Arr[2].Num;
			}
			Rw.DrawnMap = StrOr(M, "drawn_map");
			const Value* Dt = M.Find("drawn_tile_m");
			if (Dt != 0 && Dt->Type == T_ARR && Dt->Arr.size() >= 2
			    && Dt->Arr[0].Type == T_NUM && Dt->Arr[1].Type == T_NUM)
			{
				Rw.DrawnW = Dt->Arr[0].Num; Rw.DrawnH = Dt->Arr[1].Num;
			}
			if (Rw.DrawnW <= 1e-6 || Rw.DrawnH <= 1e-6) { Rw.DrawnMap.clear(); }
			const Value* Ed = M.Find("emit_day");
			if (Ed != 0 && Ed->Type == T_NUM) { Rw.EmitDay = Ed->Num; }
			const Value* En = M.Find("emit_night");
			if (En != 0 && En->Type == T_NUM) { Rw.EmitNight = En->Num; }
			Out.Rows.push_back(Rw);
		}
		if (Out.Rows.empty()) { Err = "sidecar-meshes-list-is-empty"; return false; }
		if (const Value* Rep = Root.Find("replaces_in_unreal"))
		{
			StrList(Rep->Find("piece_name_prefixes"), Out.Replaced.Prefixes);
			StrList(Rep->Find("piece_shapes"), Out.Replaced.Shapes);
			StrList(Rep->Find("held_prop_assets"), Out.Replaced.HeldPropAssets);
		}
		return true;
	}

	// DOES THE STREET STAND IN FOR THIS PIECE OF THE SCENE FILE. By its name's
	// prefix, by its shape, or - for a held prop - by its asset. A piece named
	// in none of the three stays, which is the safe way round: a doubled lamp
	// is visible in the frame, a vanished one is not.
	inline bool Replaced(const Replaces& Rp, const std::string& Name,
	                     const std::string& Shape, const std::string& Asset)
	{
		for (size_t I = 0; I < Rp.Prefixes.size(); ++I)
		{
			const std::string& P = Rp.Prefixes[I];
			if (!P.empty() && Name.compare(0, P.size(), P) == 0) { return true; }
		}
		for (size_t I = 0; I < Rp.Shapes.size(); ++I)
		{
			if (Shape == Rp.Shapes[I]) { return true; }
		}
		if (Shape == "mesh")
		{
			for (size_t I = 0; I < Rp.HeldPropAssets.size(); ++I)
			{
				if (Asset == Rp.HeldPropAssets[I]) { return true; }
			}
		}
		return false;
	}

	// ---- WET, AS BLENDER WETS IT ---------------------------------------------
	// tools/art-recipes/terrace-front.py _wetten: only the road, the paving and
	// the kerb take water; the figure is bent (w ^ 0.55, "a surface goes from
	// dry to reflective early and then changes little"); each is darkened by
	// 0.28 of that and its roughness pulled from 0.62 towards ITS OWN floor -
	// the road near a mirror (0.05), the flags dull (0.46), the kerb 0.40.
	// M_LedgerSurface has one Wetness scalar that pulls roughness towards one
	// floor of 0.08, so each surface's share of that pull is how far its own
	// floor is from dry over how far 0.08 is: the same end roughness, carried
	// by the one parameter the material has.
	inline double WetCurve(double W)
	{
		const double C = W < 0.0 ? 0.0 : (W > 1.0 ? 1.0 : W);
		return std::pow(C, 0.55);
	}
	inline double WetFloorOf(const std::string& Base)
	{
		if (Base == "asphalt") { return 0.05; }
		if (Base == "paving") { return 0.46; }
		if (Base == "kerbstone") { return 0.40; }
		return -1.0;
	}
	inline bool TakesWater(const std::string& Base) { return WetFloorOf(Base) >= 0.0; }
	// FloorOverride, when zero or more, replaces the recipe's floor for a
	// surface that takes water - the look file's wet_floor, because the
	// approved sheet's flags are shinier than the one Blender was tuned to.
	inline double WetnessParamFor(const std::string& Base, double W, double FloorOverride = -1.0)
	{
		double Floor = WetFloorOf(Base);
		if (Floor < 0.0) { return 0.0; }
		if (FloorOverride >= 0.0) { Floor = FloorOverride; }
		const double Share = (0.62 - Floor) / (0.62 - 0.08);
		const double V = WetCurve(W) * Share;
		return V < 0.0 ? 0.0 : (V > 1.0 ? 1.0 : V);
	}
	inline double WetDarken(const std::string& Base, double W)
	{
		return TakesWater(Base) ? 1.0 - 0.28 * WetCurve(W) : 1.0;
	}

	// ---- THE LOOK'S OWN SETTINGS, production/specs/unreal-look.json ---------
	// The few numbers the look is tuned by that were constants in the probe,
	// read at run time so the tuning pass against the sheet is a file edit
	// and a frame rather than a build. FAIL-SOFT: a missing file or key keeps
	// the constant the probe has always used, and the line says which.
	struct Look
	{
		double SkySeenGain;      // the sky dome as SEEN, over the sky intensity that lights
		double GlowGain;         // Blender's glow strengths into this engine's emissive
		double FogDayR, FogDayG, FogDayB;   // the day fog's colour
		double FogFalloff;       // how fast the fog thins with height
		// FROM WHAT WETNESS THE GROUND IS A FILM OF WATER: the road, the
		// paving and the kerb lose their relief map, because the pack's
		// relief scattered every reflection a wet road should show (23
		// September, found by rendering the road without it). Above 1 never.
		double WetFilmFrom;
		// HOW MUCH BRIGHTER A PICTURED ROOM READS than the facade's own light,
		// standing in for the glow Blender gives it: the base material's
		// glow is one flat colour and would wash a picture out.
		double RoomGain;
		// THE DISPLAY GLASS LEFT OUT, because the base material cannot be
		// see-through and an opaque pane hides the lit room behind it.
		bool   bGlassSeeThrough;
		// THE UNREAL LOOK'S SUN AND SKY LIGHT, as multipliers of the scene
		// file's own sun_intensity and sky_intensity. Multipliers and not
		// new values because those two numbers are in the names of the scene
		// file's grid rows, and the tuning is this engine's, not the file's.
		double SunGain;
		double SkyLightGain;
		// PER-SURFACE COLOUR IN THIS ENGINE, a multiplier on the grade by the
		// surface's base material name. Blender's colours are targets set
		// through Blender's own light and camera curve; this is where they are
		// reached again here, against the sheet, surface by surface.
		std::vector<std::pair<std::string, Grade> > SurfaceGains;
		// THE NIGHT'S OWN: the three sky and sun gains above are the DAY's,
		// tuned against a daylight sheet, and a night sky fifteen times as
		// bright as its light is not a night. The night keeps the file's own
		// sky unless these say otherwise, and its automatic exposure can be
		// biased in stops, since the night carries no pin until a settled
		// night reference exists.
		double SkySeenGainNight;
		double SkyLightGainNight;
		double NightExposureBias;
		// THE SEE-THROUGH GLASS, when M_LedgerGlass is in the build: how much
		// of a window is glass and how much is the room, and how smooth.
		double GlassOpacity;
		double GlassRoughness;
		// A WET SURFACE'S ROUGHNESS FLOOR IN THIS ENGINE, by base material,
		// where it differs from the recipe's (road 0.05, paving 0.46, kerb 0.40).
		std::vector<std::pair<std::string, double> > WetFloors;
		// THE BLENDER STREET IN THE PLAYABLE GAME TOO (the walk, the crime,
		// a plain launch): shown in place of the scene file's own pieces,
		// which stay as the collision - hidden, not removed - so walking,
		// blocking and every sight line behave exactly as they did.
		bool   bStreetInPlay;
		// THE DAY'S FOG CAP IN THIS ENGINE, a multiplier on the scene file's
		// fog_max_opacity by day only: the file's 0.100 is in the names of
		// its fog-series rows and was ruled for another street, and the far
		// end's depth against the sheet wants more haze than it allows.
		double FogCapGainDay;
		// THE NIGHT'S EXPOSURE, HELD, for a night row that asks the scene
		// file for no pin. Left automatic, the lit rooms seen through the
		// see-through glass throw the meter: a frame beside a shop window
		// read as bright as noon and came out black (cam_A, 23 September).
		// Held at what a healthy dusk frame's automatic exposure settles to.
		double NightExposurePin;
		// THE STREET'S OWN WALLS IN PLAY, 23 September, off until a run
		// proves the crime holds on them. On: the Blender street collides
		// with its own triangles (complex-as-simple, set at import), the
		// see-through glass stays out of every sight line, and the scene
		// file's pieces it replaces lose their collision.
		bool   bStreetCollision;
		int    Read;             // how many of the twenty the file supplied
		bool   bFromFile;
		Look() : SkySeenGain(1.0), GlowGain(0.10), FogDayR(0.55), FogDayG(0.58), FogDayB(0.62),
		         FogFalloff(0.02), WetFilmFrom(2.0), RoomGain(1.0), bGlassSeeThrough(false),
		         SunGain(1.0), SkyLightGain(1.0), SkySeenGainNight(1.0), SkyLightGainNight(1.0),
		         NightExposureBias(0.0), GlassOpacity(0.25), GlassRoughness(0.05),
		         bStreetInPlay(false), FogCapGainDay(1.0), NightExposurePin(0.0),
		         bStreetCollision(false),
		         Read(0), bFromFile(false) {}
	};

	// THE COLOUR GAIN FOR ONE SURFACE, white when the file names none.
	inline Grade SurfaceGainFor(const Look& Lk, const std::string& Base)
	{
		for (size_t I = 0; I < Lk.SurfaceGains.size(); ++I)
		{
			if (Lk.SurfaceGains[I].first == Base) { return Lk.SurfaceGains[I].second; }
		}
		Grade White = {1.0, 1.0, 1.0};
		return White;
	}

	// THE LOOK FILE'S WET FLOOR FOR ONE SURFACE, or -1 for the recipe's own.
	inline double WetFloorOverride(const Look& Lk, const std::string& Base)
	{
		for (size_t I = 0; I < Lk.WetFloors.size(); ++I)
		{
			if (Lk.WetFloors[I].first == Base) { return Lk.WetFloors[I].second; }
		}
		return -1.0;
	}

	// THE PEOPLE IN THE STREET, 23 September: production/specs/street-people.json,
	// for the presentable checklist's "a handful of people stand or walk in the
	// street". Street metres as the scene file gives them; FaceDeg the Unreal
	// yaw the person faces; Phase where in its loop each one starts.
	struct Person
	{
		std::string Glb;
		double X, Z, Y, FaceDeg, Phase;
		Person() : X(0.0), Z(0.0), Y(0.0), FaceDeg(0.0), Phase(0.0) {}
	};

	// ONE READER FOR ANYTHING PLACED BY A GLB NAME AND STREET METRES: the
	// people (key "people") and the parked cars (key "vehicles", in
	// production/specs/street-vehicles.json, 23 September).
	inline bool ParsePlaced(const std::string& Text, const char* Key, std::vector<Person>& Out,
	                        std::string& Err)
	{
		using namespace LedgerVignette;
		Out.clear();
		Err.clear();
		Reader R(Text);
		Value Root;
		if (!R.ReadValue(Root) || Root.Type != T_OBJ) { Err = std::string(Key) + "-file-unreadable"; return false; }
		const Value* L = Root.Find(Key);
		if (L == 0 || L->Type != T_ARR) { Err = std::string(Key) + "-file-has-no-list"; return false; }
		for (size_t I = 0; I < L->Arr.size(); ++I)
		{
			const Value& P = L->Arr[I];
			if (P.Type != T_OBJ) { continue; }
			Person Q;
			Q.Glb = StrOr(P, "glb");
			const Value* X = P.Find("x_m");
			const Value* Z = P.Find("z_m");
			if (Q.Glb.empty() || X == 0 || Z == 0 || X->Type != T_NUM || Z->Type != T_NUM) { continue; }
			Q.X = X->Num;
			Q.Z = Z->Num;
			const Value* Y = P.Find("y_m");
			if (Y != 0 && Y->Type == T_NUM) { Q.Y = Y->Num; }
			const Value* F = P.Find("face_deg");
			if (F != 0 && F->Type == T_NUM) { Q.FaceDeg = F->Num; }
			const Value* Ph = P.Find("phase");
			if (Ph != 0 && Ph->Type == T_NUM && Ph->Num >= 0.0 && Ph->Num <= 1.0) { Q.Phase = Ph->Num; }
			Out.push_back(Q);
		}
		return true;
	}

	inline bool ParsePeople(const std::string& Text, std::vector<Person>& Out, std::string& Err)
	{
		return ParsePlaced(Text, "people", Out, Err);
	}

	inline bool ParseVehicles(const std::string& Text, std::vector<Person>& Out, std::string& Err)
	{
		return ParsePlaced(Text, "vehicles", Out, Err);
	}

	// THE STREET'S SOUND, 23 September: production/specs/street-sounds.json.
	// Beds at a place in street metres; voices riding on a person, named by the
	// person's glb, each with its pre-voiced clips (voice/leaf.wav).
	struct SoundBed
	{
		std::string Wav;
		double X, Z, Y, InnerM, FalloffM, Volume;
		SoundBed() : X(0.0), Z(0.0), Y(1.0), InnerM(4.0), FalloffM(40.0), Volume(1.0) {}
	};

	struct SoundVoice
	{
		std::string Person;
		std::vector<std::string> Clips;
	};

	struct Sounds
	{
		std::vector<SoundBed> Beds;
		std::vector<SoundVoice> Voices;
		double VoiceInnerM, VoiceFalloffM, EveryMinS, EveryMaxS;
		Sounds() : VoiceInnerM(1.5), VoiceFalloffM(16.0), EveryMinS(18.0), EveryMaxS(40.0) {}
	};

	inline double NumOr(const LedgerVignette::Value& V, const char* Key, double Or)
	{
		const LedgerVignette::Value* N = V.Find(Key);
		return (N != 0 && N->Type == LedgerVignette::T_NUM) ? N->Num : Or;
	}

	inline bool ParseSounds(const std::string& Text, Sounds& Out, std::string& Err)
	{
		using namespace LedgerVignette;
		Out = Sounds();
		Err.clear();
		Reader R(Text);
		Value Root;
		if (!R.ReadValue(Root) || Root.Type != T_OBJ) { Err = "sounds-file-unreadable"; return false; }
		Out.VoiceInnerM = NumOr(Root, "voice_inner_m", Out.VoiceInnerM);
		Out.VoiceFalloffM = NumOr(Root, "voice_falloff_m", Out.VoiceFalloffM);
		const Value* E = Root.Find("voice_every_s");
		if (E != 0 && E->Type == T_ARR && E->Arr.size() >= 2 && E->Arr[0].Type == T_NUM && E->Arr[1].Type == T_NUM
		    && E->Arr[0].Num > 0.0 && E->Arr[1].Num >= E->Arr[0].Num)
		{
			Out.EveryMinS = E->Arr[0].Num;
			Out.EveryMaxS = E->Arr[1].Num;
		}
		const Value* B = Root.Find("ambience");
		if (B != 0 && B->Type == T_ARR)
		{
			for (size_t I = 0; I < B->Arr.size(); ++I)
			{
				const Value& A = B->Arr[I];
				if (A.Type != T_OBJ) { continue; }
				SoundBed S;
				S.Wav = StrOr(A, "wav");
				if (S.Wav.empty() || A.Find("x_m") == 0 || A.Find("z_m") == 0) { continue; }
				S.X = NumOr(A, "x_m", 0.0);
				S.Z = NumOr(A, "z_m", 0.0);
				S.Y = NumOr(A, "y_m", S.Y);
				S.InnerM = NumOr(A, "inner_m", S.InnerM);
				S.FalloffM = NumOr(A, "falloff_m", S.FalloffM);
				S.Volume = NumOr(A, "volume", S.Volume);
				Out.Beds.push_back(S);
			}
		}
		const Value* V = Root.Find("voices");
		if (V != 0 && V->Type == T_ARR)
		{
			for (size_t I = 0; I < V->Arr.size(); ++I)
			{
				const Value& P = V->Arr[I];
				if (P.Type != T_OBJ) { continue; }
				SoundVoice S;
				S.Person = StrOr(P, "person");
				const Value* C = P.Find("clips");
				if (S.Person.empty() || C == 0 || C->Type != T_ARR) { continue; }
				for (size_t J = 0; J < C->Arr.size(); ++J)
				{
					if (C->Arr[J].Type == T_STR && !C->Arr[J].Str.empty()) { S.Clips.push_back(C->Arr[J].Str); }
				}
				if (!S.Clips.empty()) { Out.Voices.push_back(S); }
			}
		}
		if (Out.Beds.empty() && Out.Voices.empty()) { Err = "sounds-file-names-nothing"; return false; }
		return true;
	}

	// THE SLICE'S CAST, 23 September: production/specs/quay-cast.json - the
	// places in street metres, each person's day as (hour it starts, place),
	// and the ties between them - for the walkers the slice puts on the
	// street. "off" is off the street.
	struct CastPlace
	{
		std::string Id;
		double X, Z;
		CastPlace() : X(0.0), Z(0.0) {}
	};

	struct CastPerson
	{
		std::string Id, Voice;
		std::vector<std::pair<int, std::string> > Routine;
	};

	struct CastTie
	{
		std::string A, B;
		double Weight;
		CastTie() : Weight(0.0) {}
	};

	struct Cast
	{
		std::vector<CastPlace> Places;
		std::vector<CastPerson> People;
		std::vector<CastTie> Ties;
		double TalkRangeM;
		Cast() : TalkRangeM(0.0) {}
	};

	inline bool ParseCast(const std::string& Text, Cast& Out, std::string& Err)
	{
		using namespace LedgerVignette;
		Out = Cast();
		Err.clear();
		Reader R(Text);
		Value Root;
		if (!R.ReadValue(Root) || Root.Type != T_OBJ) { Err = "cast-file-unreadable"; return false; }
		Out.TalkRangeM = NumOr(Root, "talk_range_m", 0.0);
		const Value* Pl = Root.Find("places");
		if (Pl == 0 || Pl->Type != T_OBJ) { Err = "cast-file-has-no-places"; return false; }
		for (size_t I = 0; I < Pl->Obj.size(); ++I)
		{
			const Value& V = Pl->Obj[I].second;
			if (V.Type != T_OBJ || V.Find("x_m") == 0 || V.Find("z_m") == 0) { continue; }
			CastPlace C;
			C.Id = Pl->Obj[I].first;
			C.X = NumOr(V, "x_m", 0.0);
			C.Z = NumOr(V, "z_m", 0.0);
			Out.Places.push_back(C);
		}
		const Value* Pe = Root.Find("people");
		if (Pe == 0 || Pe->Type != T_ARR) { Err = "cast-file-has-no-people"; return false; }
		for (size_t I = 0; I < Pe->Arr.size(); ++I)
		{
			const Value& V = Pe->Arr[I];
			if (V.Type != T_OBJ) { continue; }
			CastPerson P;
			P.Id = StrOr(V, "id");
			P.Voice = StrOr(V, "voice");
			const Value* Ro = V.Find("routine");
			if (P.Id.empty() || Ro == 0 || Ro->Type != T_ARR) { continue; }
			for (size_t J = 0; J < Ro->Arr.size(); ++J)
			{
				const Value& E = Ro->Arr[J];
				if (E.Type == T_ARR && E.Arr.size() >= 2 && E.Arr[0].Type == T_NUM && E.Arr[1].Type == T_STR)
				{
					P.Routine.push_back(std::make_pair((int)E.Arr[0].Num, E.Arr[1].Str));
				}
			}
			if (!P.Routine.empty()) { Out.People.push_back(P); }
		}
		const Value* Ti = Root.Find("ties");
		if (Ti != 0 && Ti->Type == T_ARR)
		{
			for (size_t I = 0; I < Ti->Arr.size(); ++I)
			{
				const Value& E = Ti->Arr[I];
				if (E.Type == T_ARR && E.Arr.size() >= 3 && E.Arr[0].Type == T_STR && E.Arr[1].Type == T_STR
				    && E.Arr[2].Type == T_NUM)
				{
					CastTie T;
					T.A = E.Arr[0].Str;
					T.B = E.Arr[1].Str;
					T.Weight = E.Arr[2].Num;
					Out.Ties.push_back(T);
				}
			}
		}
		if (Out.People.empty()) { Err = "cast-file-names-nobody"; return false; }
		return true;
	}

	// WHERE SOMEONE IS AT AN HOUR: the routine's latest entry starting at or
	// before it, "off" before the first.
	inline std::string PlaceAt(const CastPerson& P, int Hour)
	{
		std::string At = "off";
		int Best = -1;
		for (size_t I = 0; I < P.Routine.size(); ++I)
		{
			if (P.Routine[I].first <= Hour && P.Routine[I].first > Best)
			{
				Best = P.Routine[I].first;
				At = P.Routine[I].second;
			}
		}
		return At;
	}

	inline const CastPlace* FindCastPlace(const Cast& C, const std::string& Id)
	{
		for (size_t I = 0; I < C.Places.size(); ++I) { if (C.Places[I].Id == Id) { return &C.Places[I]; } }
		return 0;
	}

	// THE ASSET A CLIP BECAME in tools/ue/import_sounds.py: "crowd_m1/461561fe.wav"
	// is /Game/Ledger/Sounds/Voice/crowd_m1/461561fe.
	inline std::string VoiceAssetPath(const std::string& Clip)
	{
		const size_t Slash = Clip.find('/');
		if (Slash == std::string::npos || Slash == 0 || Slash + 1 >= Clip.size()) { return std::string(); }
		std::string Leaf = Clip.substr(Slash + 1);
		const size_t Dot = Leaf.rfind('.');
		if (Dot != std::string::npos) { Leaf = Leaf.substr(0, Dot); }
		if (Leaf.empty()) { return std::string(); }
		return "/Game/Ledger/Sounds/Voice/" + Clip.substr(0, Slash) + "/" + Leaf + "." + Leaf;
	}

	inline bool ParseLook(const std::string& Text, Look& Out, std::string& Err)
	{
		using namespace LedgerVignette;
		Out = Look();
		Err.clear();
		Reader R(Text);
		Value Root;
		if (!R.ReadValue(Root) || Root.Type != T_OBJ) { Err = "look-file-unreadable"; return false; }
		Out.bFromFile = true;
		const Value* V = Root.Find("sky_seen_gain");
		if (V != 0 && V->Type == T_NUM && V->Num > 0.0) { Out.SkySeenGain = V->Num; ++Out.Read; }
		V = Root.Find("street_glow_gain");
		if (V != 0 && V->Type == T_NUM && V->Num >= 0.0) { Out.GlowGain = V->Num; ++Out.Read; }
		V = Root.Find("fog_day_colour");
		if (V != 0 && V->Type == T_ARR && V->Arr.size() >= 3 && V->Arr[0].Type == T_NUM
		    && V->Arr[1].Type == T_NUM && V->Arr[2].Type == T_NUM)
		{
			Out.FogDayR = V->Arr[0].Num; Out.FogDayG = V->Arr[1].Num; Out.FogDayB = V->Arr[2].Num; ++Out.Read;
		}
		V = Root.Find("fog_height_falloff");
		if (V != 0 && V->Type == T_NUM && V->Num > 0.0) { Out.FogFalloff = V->Num; ++Out.Read; }
		V = Root.Find("wet_film_from");
		if (V != 0 && V->Type == T_NUM) { Out.WetFilmFrom = V->Num; ++Out.Read; }
		V = Root.Find("picture_room_gain");
		if (V != 0 && V->Type == T_NUM && V->Num >= 0.0) { Out.RoomGain = V->Num; ++Out.Read; }
		V = Root.Find("glass_see_through");
		if (V != 0 && V->Type == T_BOOL) { Out.bGlassSeeThrough = V->Bool; ++Out.Read; }
		V = Root.Find("sun_gain");
		if (V != 0 && V->Type == T_NUM && V->Num >= 0.0) { Out.SunGain = V->Num; ++Out.Read; }
		V = Root.Find("sky_light_gain");
		if (V != 0 && V->Type == T_NUM && V->Num >= 0.0) { Out.SkyLightGain = V->Num; ++Out.Read; }
		V = Root.Find("sky_seen_gain_night");
		if (V != 0 && V->Type == T_NUM && V->Num > 0.0) { Out.SkySeenGainNight = V->Num; ++Out.Read; }
		V = Root.Find("sky_light_gain_night");
		if (V != 0 && V->Type == T_NUM && V->Num >= 0.0) { Out.SkyLightGainNight = V->Num; ++Out.Read; }
		V = Root.Find("night_exposure_bias");
		if (V != 0 && V->Type == T_NUM) { Out.NightExposureBias = V->Num; ++Out.Read; }
		V = Root.Find("glass_opacity");
		if (V != 0 && V->Type == T_NUM && V->Num >= 0.0 && V->Num <= 1.0) { Out.GlassOpacity = V->Num; ++Out.Read; }
		V = Root.Find("glass_roughness");
		if (V != 0 && V->Type == T_NUM && V->Num >= 0.0 && V->Num <= 1.0) { Out.GlassRoughness = V->Num; ++Out.Read; }
		V = Root.Find("street_collision");
		if (V != 0 && V->Type == T_BOOL) { Out.bStreetCollision = V->Bool; ++Out.Read; }
		V = Root.Find("night_exposure_pin");
		if (V != 0 && V->Type == T_NUM && V->Num >= 0.0) { Out.NightExposurePin = V->Num; ++Out.Read; }
		V = Root.Find("fog_cap_gain_day");
		if (V != 0 && V->Type == T_NUM && V->Num > 0.0) { Out.FogCapGainDay = V->Num; ++Out.Read; }
		V = Root.Find("street_in_play");
		if (V != 0 && V->Type == T_BOOL) { Out.bStreetInPlay = V->Bool; ++Out.Read; }
		V = Root.Find("wet_floor");
		if (V != 0 && V->Type == T_OBJ)
		{
			for (size_t I = 0; I < V->Obj.size(); ++I)
			{
				if (V->Obj[I].second.Type == T_NUM && V->Obj[I].second.Num >= 0.0)
				{
					Out.WetFloors.push_back(std::make_pair(V->Obj[I].first, V->Obj[I].second.Num));
				}
			}
			++Out.Read;
		}
		V = Root.Find("surface_gain");
		if (V != 0 && V->Type == T_OBJ)
		{
			for (size_t I = 0; I < V->Obj.size(); ++I)
			{
				const Value& G = V->Obj[I].second;
				if (G.Type == T_ARR && G.Arr.size() >= 3 && G.Arr[0].Type == T_NUM
				    && G.Arr[1].Type == T_NUM && G.Arr[2].Type == T_NUM)
				{
					Grade Gr = {G.Arr[0].Num, G.Arr[1].Num, G.Arr[2].Num};
					Out.SurfaceGains.push_back(std::make_pair(V->Obj[I].first, Gr));
				}
			}
			++Out.Read;
		}
		return true;
	}

	// LINEAR TO AN sRGB BYTE, because the flat albedo texture is sampled as
	// sRGB like every albedo map and the sidecar's colours are linear.
	inline int SrgbByte(double Linear)
	{
		double L = Linear < 0.0 ? 0.0 : (Linear > 1.0 ? 1.0 : Linear);
		const double S = L <= 0.0031308 ? 12.92 * L : 1.055 * std::pow(L, 1.0 / 2.4) - 0.055;
		int B = (int)(S * 255.0 + 0.5);
		return B < 0 ? 0 : (B > 255 ? 255 : B);
	}

	// A ROUGHNESS MAP IS LINEAR DATA, one byte straight.
	inline int LinearByte(double V)
	{
		double L = V < 0.0 ? 0.0 : (V > 1.0 ? 1.0 : V);
		return (int)(L * 255.0 + 0.5);
	}

	// WHERE A ROW'S PICTURE IS. A path under production/ is from the
	// repository root; anything else is under the decal root, as the recipe's
	// own _decal_path says. Returned with its .png, "" for no picture.
	inline std::string PictureLeaf(const Row& Rw, bool& bFromRepo)
	{
		bFromRepo = false;
		if (Rw.Decal.empty()) { return std::string(); }
		bFromRepo = Rw.Decal.compare(0, 11, "production/") == 0;
		return Rw.Decal + ".png";
	}
}
