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
		Row() : bHasRgb(false), R(0), G(0), B(0), Roughness(-1.0) {}
	};

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
