// PHASE C: WHICH SURFACE GOT A TEXTURE, IN A FILE THAT COMPILES WITHOUT
// UNREAL.
//
// WHAT THIS IS FOR. The street's pieces carry sixteen surface names, of
// which FOURTEEN ARE LIBRARY SURFACES and two are decal blend modes, and the
// shared city pack carries a file for twelve of the fourteen; the other two
// are painted from the SurfaceSpec tint, as the Unity host paints them.
// Asking the pack for the other four was queue 227's mismeasurement, not a
// shortfall in the pack. Binding them is engine
// work; deciding WHICH FILE a surface asks for, counting what resolved and
// printing the answer is not, and it lives here for the standing reason: in
// a project whose top layer does not compile locally, a formatter written
// there ships UNRUN, and an unrun formatter printing a plausible string is
// the quietest instrument fault there is.
//
// THE FILENAME RULE IS THE UNITY HOST'S RULE, READ OUT OF IT RATHER THAN
// INVENTED HERE. AssetLibrary.LoadPackTexture tries `<logical><ext>` under
// StreamingAssets/CityPack/textures for `.png`, `.jpg`, `.jpeg` IN THAT
// ORDER; ResolveNormal and ResolveGloss try `<logical>_n<ext>` and
// `<logical>_r<ext>` the same way. D1 is a comparison, and an engine that
// picked a different file for the same surface name would not be comparing
// anything. There is one mapping and this is a second READER of it, not a
// second copy: the surface names come out of the shared pieces file and the
// suffixes are the three above.
//
// A PHASE C THAT RENDERS AND CANNOT SAY WHAT IT FAILED TO LOAD IS WORTH LESS
// THAN ONE THAT LOADS LESS AND SAYS SO. Every absent surface is NAMED with
// the candidates that were tried and how many pieces wear it, and every zero
// ships the count of what was examined.
//
// WHAT EACH NUMBER IS A STATISTIC OF:
//   Pieces          pieces in the shared file carrying this surface name
//   PiecesAssigned  of those, how many actually got a material instance
//   Resolved        surfaces whose ALBEDO file was found, decoded and bound
//   LoadedAs        what the decoder said the file IS, not what its name says
#pragma once

#include "VignetteSpec.h"

#include <algorithm>
#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <string>
#include <vector>

namespace LedgerSurface
{
	// THE EXTENSION ORDER IS THE UNITY HOST'S, character for character.
	inline int ExtCount() { return 3; }
	inline const char* Ext(int I)
	{
		const char* E[3] = {".png", ".jpg", ".jpeg"};
		return (I >= 0 && I < 3) ? E[I] : "";
	}

	// THE THREE MAPS A SURFACE CAN CARRY, named once. The suffix is what the
	// pack's filenames use; the parameter is what the base material exposes,
	// and the two are printed together so a mismatch is visible from the
	// verdict rather than only from a grey frame.
	inline int MapCount() { return 3; }
	inline const char* MapSuffix(int I)
	{
		const char* S[3] = {"", "_n", "_r"};
		return (I >= 0 && I < 3) ? S[I] : "";
	}
	inline const char* MapParam(int I)
	{
		const char* P[3] = {"BaseColorMap", "NormalMap", "RoughnessMap"};
		return (I >= 0 && I < 3) ? P[I] : "";
	}
	inline const char* MapName(int I)
	{
		const char* N[3] = {"albedo", "normal", "roughness"};
		return (I >= 0 && I < 3) ? N[I] : "";
	}

	// EVERY FILENAME A SURFACE WOULD ACCEPT FOR ONE MAP, in the order they
	// are tried. Printed into the verdict for an absent surface, so "not
	// found" says what was looked for rather than leaving a reader to guess.
	inline std::vector<std::string> Candidates(const std::string& Surface, int MapIndex)
	{
		std::vector<std::string> Out;
		for (int E = 0; E < ExtCount(); ++E)
		{
			Out.push_back(Surface + MapSuffix(MapIndex) + Ext(E));
		}
		return Out;
	}

	// A SEARCH THAT FAILED MUST SAY WHERE IT LOOKED. `texRoot=NOT-FOUND` with
	// nothing beside it cost run 19 a whole round trip: the four directories
	// the binary checked were known only to the binary, so the answer to "is
	// the pack in the wrong place or is the search in the wrong place" was
	// not in the evidence at all.
	//
	// THE SEPARATOR IS A COMMA AND NOT A SLASH. Every candidate here is
	// itself a path full of slashes, so a slash-joined list of paths cannot
	// be split back into the paths it was made from. No spaces, because every
	// reader of this file splits on whitespace.
	//
	// THE CAP ANNOUNCES WHEN IT BITES and is silent when it does not, which
	// is this project's rule: a cap nobody is told about is indistinguishable
	// from a finding.
	inline std::string PathListValue(const std::vector<std::string>& Paths, size_t Cap)
	{
		if (Paths.empty()) { return "nothing-tried"; }
		std::string Out;
		size_t Shown = 0;
		for (size_t I = 0; I < Paths.size() && Shown < Cap; ++I, ++Shown)
		{
			if (Shown > 0) { Out += ","; }
			Out += LedgerVignette::NoSpaces(Paths[I]);
		}
		if (Paths.size() > Shown)
		{
			char Tail[64];
			std::snprintf(Tail, sizeof(Tail), ",+%d-more-not-shown",
			              (int)(Paths.size() - Shown));
			Out += Tail;
		}
		return Out;
	}

	inline std::string CandidateList(const std::string& Surface, int MapIndex)
	{
		const std::vector<std::string> C = Candidates(Surface, MapIndex);
		std::string Out;
		for (size_t I = 0; I < C.size(); ++I)
		{
			if (I > 0) { Out += "/"; }
			Out += C[I];
		}
		return Out;
	}

	// WHAT THE FILE ASKED FOR, WHICH IS THE DENOMINATOR. Derived from the
	// pieces rather than hard-coded, so a surface added to the street next
	// week enlarges the denominator instead of vanishing from the report.
	// Sorted, so two runs print their surfaces in the same order.
	struct Ask
	{
		std::string Surface;
		int         Pieces = 0;
	};

	inline std::vector<Ask> SurfacesAsked(const std::vector<LedgerVignette::Piece>& Pieces)
	{
		std::vector<Ask> Out;
		for (size_t I = 0; I < Pieces.size(); ++I)
		{
			const std::string& S = Pieces[I].Surface;
			if (S.empty()) { continue; }
			bool bFound = false;
			for (size_t J = 0; J < Out.size(); ++J)
			{
				if (Out[J].Surface == S) { ++Out[J].Pieces; bFound = true; break; }
			}
			if (!bFound)
			{
				Ask A;
				A.Surface = S;
				A.Pieces = 1;
				Out.push_back(A);
			}
		}
		for (size_t I = 0; I + 1 < Out.size(); ++I)
		{
			for (size_t J = I + 1; J < Out.size(); ++J)
			{
				if (Out[J].Surface < Out[I].Surface) { std::swap(Out[I], Out[J]); }
			}
		}
		return Out;
	}

	// HOW MANY TIMES A TEXTURE REPEATS ACROSS A PIECE.
	//
	// THE ENGINE'S BASIC SHAPES CARRY 0..1 UVS, so a 42 metre carriageway
	// with no tiling shows ONE asphalt tile stretched forty-two metres, which
	// is not a photograph of a road. The two largest dimensions of the piece
	// are the ones a camera in the street sees: a 42.0 x 0.3 x 2.7 road slab
	// is seen along 42 and across 2.7, and its 0.3 thickness is the edge.
	// THIS IS A SIMPLIFICATION AND IS NAMED AS ONE on the verdict: it is not
	// per-face UVs, and a piece whose visible face is its smallest pair will
	// tile wrongly. MetresPerTile is a stated convention, not a measured
	// bound; it is printed beside the numbers it produced.
	struct Tiling
	{
		double U = 1.0;
		double V = 1.0;
	};

	inline Tiling TilingFor(const LedgerVignette::Piece& P, double MetresPerTile)
	{
		Tiling T;
		if (MetresPerTile <= 0.0) { return T; }
		double D[3] = {P.SX, P.SY, P.SZ};
		for (int I = 0; I < 3; ++I) { if (D[I] < 0.0) { D[I] = -D[I]; } }
		std::sort(D, D + 3);            // ascending, so D[2] and D[1] are the pair
		const double A = D[2], B = D[1];
		T.U = (A > 0.0) ? (A / MetresPerTile) : 1.0;
		T.V = (B > 0.0) ? (B / MetresPerTile) : 1.0;
		if (T.U < 1.0) { T.U = 1.0; }   // never below one repeat: a fraction of
		if (T.V < 1.0) { T.V = 1.0; }   // a tile is a crop, not a surface
		return T;
	}

	// ---- THE FOUR SURFACE NAMES THE PACK CANNOT ANSWER FOR ---------------
	//
	// WHAT THIS SECTION IS AND WHY IT IS NOT A FETCH. The street names sixteen
	// surfaces and the pack carries a file for twelve. Until this section
	// existed the piece loop below SKIPPED every piece whose surface did not
	// resolve, so thirty pieces got no material instance at all and rendered
	// the engine's default: ten card decals, ten multiply decals, six shop
	// interiors and four runs of yellow road paint. The Unity host paints all
	// thirty and has always painted them, by rules that are written down in
	// its own source, and the four missing rules are re-read here rather than
	// invented:
	//
	//   card, multiply      NOT LIBRARY SURFACES AT ALL. They are the two
	//                       DECAL BLEND MODES, declared in words at
	//                       ledger/Assets/Scripts/Core/StreetVignette.cs:57
	//                       and refused at 1651 if they are anything else.
	//                       The picture comes from the piece's own asset
	//                       field under StreamingAssets/Decals. Asking the
	//                       texture root for card.png asks for a file that by
	//                       design can never exist, which is why those two
	//                       surfaces print a blend note here rather than a
	//                       candidate list.
	//   paint_yellow        ProceduralOnly at AssetLibrary.cs:1613, so a pack
	//                       file for it is DELIBERATELY ignored and it renders
	//                       from the SurfaceSpec tint. Dropping a
	//                       paint_yellow.jpg into the pack would make the two
	//                       engines render one surface from two different
	//                       inputs, which is the single thing D1 exists to
	//                       avoid.
	//   interior            No pack file, and Unity needs none: it generates
	//                       from the tint and BORROWS its normal and roughness
	//                       from the window surface by the explicit rule at
	//                       AssetLibrary.cs:611, mapsFrom = logical ==
	//                       Interior ? Window : logical.
	//
	// WHY THE NUMBERS ARE HERE AND WHAT STOPS THEM DRIFTING. Unreal has no
	// way to read a C# table at runtime, so these are a SECOND READER of
	// AssetLibrary.SurfaceSpec and not a second opinion: every value below is
	// the literal from that switch, and tools/surface-tint-check.py parses
	// both files and refuses a disagreement. It is wired into ledger/verify.py
	// as surface_tint_agreement, so it runs before every commit; a grep for
	// its name is what proves that rather than this sentence.
	//
	// IT COMPARES TINTS ONLY. Smoothness, emission, tiling and pattern cross
	// this same boundary and are NOT compared, which the tool prints on its own
	// pass line. Do not read a green from it as a green about the whole table.
	//
	// THIS COMMENT PREVIOUSLY OVER-CLAIMED TWICE and is corrected here rather
	// than quietly rewritten: it said the tool refused "any disagreement" when
	// it compares tints, and that it ran "in the container, before a dispatch"
	// when for the first hour of its life NOTHING CALLED IT AT ALL. A comment
	// promising a guard is not a guard, and it is worse than no guard, because
	// a reader who believes it does not check.
	inline int ProceduralSurfaceCount() { return 2; }

	// THE TINT, IN GAMMA sRGB, WHICH IS THE SPACE THE LITERALS ARE IN. A
	// Unity shader property declared as a Color is converted from gamma to
	// linear on upload, so (0.78, 0.66, 0.18) is a gamma number and every
	// other colour this project shares (the lantern, the practicals) is
	// stated the same way and converted the same way.
	inline const char* ProceduralSurfaceName(int I)
	{
		const char* N[2] = {"interior", "paint_yellow"};
		return (I >= 0 && I < 2) ? N[I] : "out-of-range";
	}

	inline void ProceduralSurfaceTint(int I, double& R, double& G, double& B)
	{
		const double T[2][3] = {{0.18, 0.13, 0.08}, {0.78, 0.66, 0.18}};
		const int J = (I >= 0 && I < 2) ? I : 0;
		R = T[J][0]; G = T[J][1]; B = T[J][2];
	}

	// SMOOTHNESS, FROM THE SAME SWITCH, AND IT BECOMES A ROUGHNESS TEXEL.
	// The base material exposes a roughness MAP and no roughness scalar, so a
	// surface with no pack roughness file gets a flat one built from this
	// number by the same rule AssetLibrary.ResolveGloss uses in reverse
	// (alpha = 255 - roughness, so smoothness and roughness are complements).
	inline double ProceduralSurfaceSmoothness(int I)
	{
		const double S[2] = {0.10, 0.05};
		return (I >= 0 && I < 2) ? S[I] : 0.10;
	}

	inline int ProceduralSurfaceIndex(const std::string& Surface)
	{
		for (int I = 0; I < ProceduralSurfaceCount(); ++I)
		{
			if (Surface == ProceduralSurfaceName(I)) { return I; }
		}
		return -1;
	}

	// THE TWO GRADES EVERY UNITY ALBEDO IS MULTIPLIED BY, AND WHY THEY ARE
	// IN THIS CALCULATION. AssetLibrary.BuildMaterial sets mat.color =
	// BaseColour(logical, textured), which is TextureGrade for any surface
	// carrying a texture, times GroundGrade for the four ground surfaces.
	// Every surface in that host therefore renders its albedo DARKENED, and
	// for the two surfaces this section paints the product is baked into the
	// texel. Taken in LINEAR, because that is where Unity's shader takes it.
	//
	// THIS COMMENT PREVIOUSLY CLAIMED A GUARD THAT NEVER EXISTED and is
	// corrected here rather than quietly rewritten, which is the habit set
	// at ProceduralSurfaceCount above. It said the twelve pack surfaces were
	// bound at full brightness, which was TRUE, and then said "the gap is
	// named on the materials line as gradeAppliedTo, and it is one number,
	// not a taste", which was FALSE for the whole life of the sentence: a
	// grep for gradeAppliedTo over ue-probe returned this comment and
	// nothing else, no line carried the key and no code ever emitted it. A
	// reader of queue 181 believed it, went looking for the number, and
	// found only the promise. A comment promising a measurement is not a
	// measurement, and it is worse than none, because the reader who
	// believes it does not measure.
	//
	// WHAT IS TRUE NOW, queue 299. M_LedgerSurface carries a vector
	// parameter AlbedoGrade (tools/ue/make_base_material.py, VECTOR_PARAMS),
	// multiplied into Base Color after the BaseColorMap sample and
	// defaulting to white, and AlbedoGradeFor below is what VignetteShot.cpp
	// sets it from. So the twelve pack surfaces take the same grade Unity
	// gives them, the two painted here still take it baked into the texel,
	// and NO KEY WAS ADDED for it: the grade is on the surface line in
	// tintTexel, tintFrom, tintPattern and roughnessTexel, four fields that
	// printed not-built on every pack surface until this change.
	//
	// THE ONE WAY THIS GOES WRONG IS TWICE. A surface whose texel already
	// carries the product must be sent WHITE, or the street is graded
	// squared. That is why AlbedoGradeFor asks ProceduralSurfaceIndex first
	// and why the g++ suite checks both halves.
	inline void TextureGrade(double& R, double& G, double& B)
	{
		R = 0.74; G = 0.76; B = 0.80;
	}

	inline double GroundGrade() { return 0.55; }

	// ---- JAFAR'S WALK-BACK, RULED 2026-09-15, AND IT IS PROVISIONAL ------
	//
	// IT IS A SEPARATE TERM ON PURPOSE. The two constants above are the
	// legacy build's numbers, read off AssetLibrary and owed to parity. This
	// one is a judgement about THIS ENGINE made by the one person who may
	// make it (D23), and when wetness lands (queue 186) one of the two will
	// have to move. Folded into TextureGrade or GroundGrade they could not be
	// told apart, and a later session would read his placeholder as the
	// legacy table.
	//
	// IT HAS AN EXPIRY AND THE EXPIRY IS NAMED. Re-read when wetness lands,
	// not carried forward as settled. His words: "this value is provisional
	// and gets re-read when wetness lands rather than kept". A session that
	// finds 0.85 here and treats it as derived is reading a placeholder as a
	// result. It is ALSO not tuned toward the Hook sheet and may not be: "the
	// sheet is wet and the street is dry", so solving for the factor that
	// lands the sheet's 0.373 is forbidden rather than merely unnecessary.
	//
	// WHAT HE SAW. Run 44 landed full legacy parity and band.ground.p50 went
	// 0.5117 to 0.2711 against the sheet's 0.373. The gap CROSSED ZERO: the
	// render was 37 per cent brighter than the reference and came out 27 per
	// cent darker. "The full legacy grade overshoots in this engine, so take
	// it to about 0.85 of what landed and re-read."
	//
	// ---- WHICH OF THE FOUR READINGS THIS IS, AND WHY THE OTHER THREE ARE
	// NOT IT. "0.85 of what landed" is ambiguous and getting it wrong is
	// silent, so the reasoning is written down here rather than left in a
	// dispatch nobody will find.
	//
	// THE DIRECTION IS FIXED BY HIS OWN SENTENCE AND IS NOT A JUDGEMENT.
	// He says the grade OVERSHOOTS and that the frame is DARKER than his
	// reference. The grade multiplies base colour, so a smaller grade is a
	// darker frame, monotonically, in any engine and under any tonemap.
	// THEREFORE THE NEW GRADE MUST BE CLOSER TO WHITE THAN WHAT LANDED.
	// A plain 0.85x on the grade takes the ground gamma term 0.4070 to
	// 0.3460 and the frame FURTHER DOWN, deeper into the overshoot he asked
	// to have undone. It is the most literal reading of the words and it is
	// refuted by the clause in front of them.
	//
	// SO THE TERM IS A STRENGTH, MEASURED FROM WHITE: the new grade keeps
	// 0.85 of the DARKENING that landed. That is what makes his number
	// literally true of the quantity the grade IS. A grade's whole content
	// is its distance below 1.0; at strength 1.0 this reproduces run 44 byte
	// for byte, and at strength 0.0 it is white and the grade is off. Those
	// two anchors are why a strength is the right shape for a provisional
	// knob: it has the landed value as its identity.
	//
	// AND IT IS APPLIED IN GAMMA, WHICH IS NOT A FREE CHOICE EITHER. The
	// block at AlbedoGradeFor rules that grade terms compose in gamma and the
	// product is converted ONCE, because Unity's mat.color is a gamma number
	// and "any other order is a different colour, not a rounding difference".
	// This is a third grade term and it composes where the other two do. The
	// same walk-back applied in linear would take the ground term to 0.5537
	// in gamma rather than 0.4960, which is a different picture and not a
	// rounding difference.
	//
	// THE OTHER TWO DIRECTION-CORRECT READINGS ARE NAMED SO A RE-READ IS ONE
	// CONSTANT AND NOT AN ARCHAEOLOGY. G/0.85 gives a ground term of 0.4788
	// and G^0.85 gives 0.4658, against this reading's 0.4960. All three are
	// inside "about 0.85" and all three are far from the refuted 0.3460.
	// If his eye says this landed too bright, those are the next two rungs
	// down and the strength below is the only line that moves.
	//
	// WHAT THIS IS A STATISTIC OF: nothing. It is a judged constant with a
	// date and an owner, and the surface line prints it beside the two
	// legacy terms so a reader can recompute the product without this file.
	inline double JafarGradeStrength() { return 0.85; }

	// THE DATE AND THE OWNER TRAVEL WITH THE NUMBER onto the verdict line,
	// so a frame can never be read against this grade without the reader
	// learning that it is provisional and whose it is.
	inline const char* JafarGradeStrengthWhen() { return "2026-09-15"; }

	// KEEP 0.85 OF THE DARKENING THAT LANDED. Strength 1.0 is run 44 exactly,
	// strength 0.0 is white. Takes and returns a GAMMA grade term.
	inline double JafarWalkBack(double GammaGrade)
	{
		return 1.0 - JafarGradeStrength() * (1.0 - GammaGrade);
	}

	// THE GROUND FAMILY, AssetLibrary.WetSurfaces, character for character.
	// Neither surface the procedural section paints is in it, and the rule
	// was implemented rather than assumed away: the day a ground surface
	// needed the arithmetic it was already right, and queue 299 is that day.
	// FOUR MEMBERS AND EACH IS LOAD-BEARING SEPARATELY: kerb is 95 pieces
	// and concrete is 150 of the street's 610, so a list that happened to be
	// right about kerb and wrong about concrete would pass any one-surface
	// check and mis-grade a quarter of the street. The g++ suite asserts the
	// four one at a time and asserts a non-member with them.
	inline bool IsGroundSurface(const std::string& Surface)
	{
		return Surface == "asphalt" || Surface == "sidewalk"
		    || Surface == "kerb" || Surface == "concrete";
	}

	// THE WHOLE GAMMA CHAIN, IN ONE PLACE, BECAUSE IT HAS TWO CALLERS.
	// ProceduralAlbedoTexel bakes the product into a flat texel and
	// AlbedoGradeFor hands it to a material parameter; they must not be able
	// to drift, and before this existed the chain was written out twice. It
	// sits below IsGroundSurface because it needs it.
	//
	// THIS IS THE LEGACY PAIR AND ONLY THE LEGACY PAIR. JAFAR'S WALK-BACK IS
	// NOT IN IT, AND THAT IS THE WHOLE POINT OF THE SPLIT.
	//
	// A BUILDER PUT THE WALK-BACK IN HERE ON 2026-09-15 AND IT WAS WRONG.
	// The reasoning was "one street, one grade policy": the ten procedurally
	// painted pieces sit in the frame Jafar judged, so walking back only the
	// parameter route would leave them as an island at the full legacy grade.
	// That reasoning is about the FRAME and it is not baseless, but it loses
	// to what this particular value IS.
	//
	// WHAT THE PROCEDURAL TEXEL IS, AND WHY NO ENGINE-LOCAL NUMBER MAY ENTER
	// IT. ProceduralAlbedoTexel REPRODUCES A UNITY VALUE. It exists so that
	// the flat colour this engine paints on interior and paint_yellow is the
	// same byte Unity's AssetLibrary bakes into them, and the suite asserts
	// it against values hand-computed from the Unity literals. Jafar's 0.85
	// is an UNREAL-ONLY correction to how that grade lands in THIS renderer.
	// Multiplying it into the texel would make the texel stop equalling the
	// thing it is defined to equal, and the parity check above it would then
	// be asserting a number that no longer means parity. The grade would
	// still be applied exactly once per surface, so this is not a
	// double-grade; it is the quieter fault of a parity value that has
	// silently stopped being one.
	//
	// SO THE SPLIT IS: the legacy chain has one owner and both routes take
	// it, and the walk-back is applied at exactly one site, AlbedoGradeFor,
	// where only the vector parameter can see it.
	//
	// THE FRAME CONSEQUENCE IS REAL AND IS NOT HIDDEN. Ten pieces of 610
	// (interior and paint_yellow) stay at the full legacy grade while the
	// twelve pack surfaces come up by the walk-back, so those ten render
	// slightly darker relative to their neighbours than they did in run 44.
	// That is a reported residual for Jafar's eye, not a thing to fix by
	// putting an engine-local constant into a parity value.
	inline void GradeChainGamma(const std::string& Surface,
	                            double& R, double& G, double& B)
	{
		TextureGrade(R, G, B);
		if (IsGroundSurface(Surface))
		{
			R *= GroundGrade(); G *= GroundGrade(); B *= GroundGrade();
		}
	}

	// ONE TEXEL, THE WHOLE OF A PROCEDURAL SURFACE'S ALBEDO ON THIS SIDE.
	//
	// WHAT IT IS A STATISTIC OF: nothing. It is a computed value, printed
	// beside the two inputs it came from so a reader can recompute it.
	//
	// WHAT IT IS NOT. Unity's procedural albedo for paint_yellow is this
	// colour on every texel (the flat pattern), so that one matches; for
	// interior it is this colour with a 0.10 amplitude noise over it, so the
	// Unreal interior is the same colour with no grain in it. NAMED on the
	// surface line as tintPattern, because a flat card where the pair has
	// grain is a difference a judge can see and must not have to discover.
	struct Texel
	{
		int R, G, B;
		Texel() : R(0), G(0), B(0) {}
	};

	inline Texel ProceduralAlbedoTexel(const std::string& Surface)
	{
		Texel T;
		const int I = ProceduralSurfaceIndex(Surface);
		if (I < 0) { return T; }
		double Tr = 0.0, Tg = 0.0, Tb = 0.0;
		ProceduralSurfaceTint(I, Tr, Tg, Tb);
		double Gr = 0.0, Gg = 0.0, Gb = 0.0;
		// THE LEGACY CHAIN, AND DELIBERATELY NOT JAFAR'S WALK-BACK. This
		// texel reproduces a Unity value byte for byte and an Unreal-only
		// correction inside it would make it stop being the thing it is
		// asserted to equal. GradeChainGamma's comment carries the ruling.
		GradeChainGamma(Surface, Gr, Gg, Gb);
		// THE BYTE FIRST, BECAUSE UNITY STORES THE TINT AS A BYTE. Color32
		// rounds the float literal into a texel and the shader then reads
		// that texel, so the product starts from 199/255 and not from 0.78.
		const double Br = (double)LedgerVignette::ByteOf(Tr) / 255.0;
		const double Bg = (double)LedgerVignette::ByteOf(Tg) / 255.0;
		const double Bb = (double)LedgerVignette::ByteOf(Tb) / 255.0;
		T.R = LedgerVignette::ByteOf(LedgerVignette::LinearToSrgb(
			LedgerVignette::SrgbToLinear(Br) * LedgerVignette::SrgbToLinear(Gr)));
		T.G = LedgerVignette::ByteOf(LedgerVignette::LinearToSrgb(
			LedgerVignette::SrgbToLinear(Bg) * LedgerVignette::SrgbToLinear(Gg)));
		T.B = LedgerVignette::ByteOf(LedgerVignette::LinearToSrgb(
			LedgerVignette::SrgbToLinear(Bb) * LedgerVignette::SrgbToLinear(Gb)));
		return T;
	}

	// THE ROUGHNESS TEXEL FOR A SURFACE WITH NO ROUGHNESS FILE. LINEAR data,
	// never sRGB: a roughness is a number and a gamma curve would bend it.
	inline int ProceduralRoughnessTexel(const std::string& Surface)
	{
		const int I = ProceduralSurfaceIndex(Surface);
		if (I < 0) { return 255; }
		const double Rough = 1.0 - ProceduralSurfaceSmoothness(I);
		return LedgerVignette::ByteOf(Rough);
	}

	// WHICH SURFACE'S MAPS A SURFACE WEARS. AssetLibrary.cs:611 in one line,
	// and it is the reason a lit shop interior reads as glass with a room
	// behind it rather than as a flat card: the interior takes the window's
	// normal and roughness, which is also what keeps the Unity material's
	// keyword set intact.
	inline std::string MapsFrom(const std::string& Surface)
	{
		return (Surface == "interior") ? std::string("window") : Surface;
	}

	// ---- THE TWO DECAL BLENDS, WHICH ARE NOT SURFACES --------------------
	inline bool IsDecalBlend(const std::string& Surface)
	{
		return Surface == "card" || Surface == "multiply";
	}

	inline bool IsMultiplyBlend(const std::string& Surface)
	{
		return Surface == "multiply";
	}

	// ---- THE ALBEDO GRADE, WHICH IS WHAT A PACK SURFACE GETS INSTEAD -----
	//
	// This sits below IsDecalBlend rather than beside TextureGrade because it
	// needs that predicate; the grade block above points here.
	//
	// WHAT IT IS. The value VignetteShot.cpp sets on the AlbedoGrade vector
	// parameter of M_LedgerSurface, which is multiplied into Base Color after
	// the BaseColorMap sample. It is the SECOND READER of
	// AssetLibrary.BaseColour(logical, textured) and deliberately takes the
	// same two arguments that function takes, so the two can be compared by
	// eye: Unity's is `textured ? TextureGrade : SurfaceSpec.Tint`, then
	// times GroundGrade for the four in WetSurfaces.
	//
	// WHAT IT IS A STATISTIC OF: nothing. It is a computed constant per
	// surface, not a measurement, and the surface line prints the inputs
	// beside it so a reader can recompute it without this file.
	//
	// THE SPACE, WHICH IS THE WHOLE TRAP. Unity's mat.color is a gamma
	// number converted to linear on upload; Unreal's FLinearColor parameter
	// is used by the shader AS LINEAR, with no conversion. So the gamma
	// product is formed first and converted once, which is exactly the order
	// ProceduralAlbedoTexel uses one screen above: GroundGrade multiplies
	// the grade IN GAMMA, and SrgbToLinear is applied to the product. Any
	// other order is a different colour, not a rounding difference.
	//
	// THREE SURFACES GET WHITE, AND EACH FOR ITS OWN REASON.
	//   1. A PROCEDURAL SURFACE, because ProceduralAlbedoTexel has already
	//      baked both grades into the flat texel it built. Sending the grade
	//      again would square it: interior would render at 0.74 x 0.74. This
	//      is the failure mode this function most has to avoid and it is the
	//      first thing it tests.
	//   2. A DECAL BLEND, because StreetVignetteHost.EmitDecal builds its
	//      material with `new Material(sh) { mainTexture = tex }` and never
	//      assigns mat.color at all, so Unity's decals are UNGRADED and a
	//      graded one here would be a new difference rather than a closed
	//      one. Implemented rather than assumed away, on the habit of
	//      IsGroundSurface above, even though the decal path builds its own
	//      instance and does not call this.
	//   3. AN UNTEXTURED SURFACE, because Unity's BaseColour takes its OTHER
	//      branch there and uses SurfaceSpec.Tint, a table this side has only
	//      two rows of. White with the reason printed is the honest answer; a
	//      grade would be a guess wearing a constant's clothes.
	//
	// Why is a value a NAMED REASON rather than a comment: the surface line
	// prints it, so "this surface is white" and "white because the texel
	// already carries it" are never the same reading.
	struct Grade
	{
		double R, G, B;          // LINEAR, the space the parameter is read in
		double GammaR, GammaG, GammaB;  // the product before the conversion
		bool   bGround;          // was GroundGrade folded in
		const char* Why;
		Grade() : R(1.0), G(1.0), B(1.0), GammaR(1.0), GammaG(1.0),
		          GammaB(1.0), bGround(false),
		          Why("white/nothing-decided-yet") {}
	};

	// THE PARAMETER'S ONE SPELLING, and it is spelled ONCE. Named here for
	// the same reason MapParam is, so the generator and the binder cannot
	// drift apart without the container saying so before a dispatch.
	//
	// THE SELFTEST THAT HOLDS IT DOES NOT GREP FOR THIS LITERAL, and the
	// difference matters. A grep over the tree would be satisfied by the
	// line below and would print green over a parameter nothing ever sets,
	// which is the shape of every comment-shaped guard this file has had to
	// correct. make_base_material.py --selftest instead asks the .cpp files
	// for SetVectorParameterValue and for AlbedoGradeParam separately: the
	// declaration cannot satisfy either.
	inline const char* AlbedoGradeParam() { return "AlbedoGrade"; }

	inline Grade AlbedoGradeFor(const std::string& Surface, bool bTextured)
	{
		Grade Out;
		if (ProceduralSurfaceIndex(Surface) >= 0)
		{
			Out.Why = "white/the-grade-is-already-baked-into-the-procedural-texel";
			return Out;
		}
		if (IsDecalBlend(Surface))
		{
			Out.Why = "white/EmitDecal-sets-no-material-colour-so-unity-decals-are-ungraded";
			return Out;
		}
		if (!bTextured)
		{
			Out.Why = "white/no-albedo-bound-and-unity-would-use-the-SurfaceSpec-tint-here";
			return Out;
		}
		double Gr = 0.0, Gg = 0.0, Gb = 0.0;
		Out.bGround = IsGroundSurface(Surface);
		// THE LEGACY PAIR FIRST, FROM THE ONE OWNER OF THAT CHAIN, so this
		// route and the texel route cannot drift on it.
		GradeChainGamma(Surface, Gr, Gg, Gb);
		// AND THEN JAFAR'S WALK-BACK, AT THIS ONE SITE AND NOWHERE ELSE.
		// THIS IS THE ONLY PLACE THE 0.85 IS APPLIED IN THE WHOLE PROJECT.
		// It is here rather than inside GradeChainGamma because only the
		// vector parameter may see it: the other caller of that chain builds
		// a texel that reproduces a Unity value, and an engine-local
		// correction inside a parity value is a parity value that has
		// stopped being one. Still in GAMMA, still converted once below.
		Gr = JafarWalkBack(Gr); Gg = JafarWalkBack(Gg); Gb = JafarWalkBack(Gb);
		Out.GammaR = Gr; Out.GammaG = Gg; Out.GammaB = Gb;
		Out.R = LedgerVignette::SrgbToLinear(Gr);
		Out.G = LedgerVignette::SrgbToLinear(Gg);
		Out.B = LedgerVignette::SrgbToLinear(Gb);
		// THE REASON NAMES THE WALK-BACK, because a reader comparing this
		// frame against the legacy build must not read a walked-back grade as
		// parity. The number itself is on the line beside it.
		Out.Why = Out.bGround
			? "textureGrade-times-groundGrade-times-jafar-walkback-2026-09-15"
			: "textureGrade-times-jafar-walkback-2026-09-15";
		return Out;
	}

	// ---- WETNESS, QUEUE 186, AND THE TRAP IS IN THE UNITS ----------------
	//
	// WHAT THIS IS. Two functions out of ledger/Assets/Scripts/Core/
	// LightModel.cs, lines 594 and 601, ported here for the standing reason
	// the rest of this file exists: in a project whose top layer does not
	// compile locally, arithmetic written there ships UNRUN, and an unrun
	// formula producing a plausible number is the quietest fault there is.
	// They are a SECOND READER of that file, not a second copy with a new
	// opinion in it, and the g++ suite asserts them against values computed
	// from the C# by hand.
	//
	// THE THESIS, IN THE ORIGINAL AUTHOR'S WORDS AT LightModel.cs:588-593,
	// because it is the only reason both halves are one change: "Raising
	// smoothness alone gives a bright shiny road that reads as polished
	// plastic. Dropping albedo at the same time is what makes the lamps'
	// reflections POP off a dark road, which is the entire look of a rainy
	// street at night." A wet surface is not just shinier, it is DARKER: the
	// water film fills the micro-structure, so less light scatters back out
	// and more reflects specularly. Ship one half and the road reads as
	// plastic.
	//
	// ---- THE TRAP, NAMED BEFORE ANY CODE ---------------------------------
	//
	// UNITY'S PARAMETER IS SMOOTHNESS. UNREAL'S IS ROUGHNESS. They are
	// opposites: roughness = 1 - smoothness. A direct port of Smoothness
	// into a roughness pin gives a road that gets ROUGHER as it gets wetter,
	// which is the exact opposite of the look, and every number in the
	// verdict would read plausible while the frame was backwards. THE
	// CONVERSION HAPPENS AT ONE NAMED SITE, RoughnessFromSmoothness BELOW,
	// AND NOWHERE ELSE, and the suite asserts the direction rather than only
	// the value: wetter must mean a SMALLER roughness.
	inline double WetClamp01(double V)
	{
		// Feel.Clamp01's shape, written out because this header has no Feel.
		return V < 0.0 ? 0.0 : (V > 1.0 ? 1.0 : V);
	}

	inline double WetClamp(double V, double Lo, double Hi)
	{
		return V < Lo ? Lo : (V > Hi ? Hi : V);
	}

	// THE SMOOTHNESS A FULLY WET SURFACE APPROACHES. LightModel.Smoothness's
	// 0.92, named once so the roughness floor below is derived from it and
	// the two can never disagree by an edit.
	//
	// WHAT IT IS A STATISTIC OF: nothing. It is the other engine's constant,
	// copied, and guarded by tools/surface-tint-check.py.
	inline double WetSmoothnessCeiling() { return 0.92; }

	// LightModel.Smoothness(dry, rain), character for character.
	inline double WetSmoothness(double DrySmoothness, double Rain)
	{
		Rain = WetClamp01(Rain);
		return WetClamp01(DrySmoothness
		                  + (WetSmoothnessCeiling() - DrySmoothness) * Rain);
	}

	// LightModel.AlbedoScale(rain), character for character. A MULTIPLIER ON
	// ALBEDO, never a replacement for one: Unity applies it to the product
	// BaseColour already carries, so a wet road runs 0.55 x AlbedoScale and a
	// dry one runs 0.55 (AssetLibrary.SetWetness, lines 835-843).
	inline double WetAlbedoScale(double Rain)
	{
		Rain = WetClamp01(Rain);
		return WetClamp(1.0 - 0.45 * Rain, 0.55, 1.0);
	}

	// ---- THE ONE CONVERSION SITE -----------------------------------------
	//
	// roughness = 1 - smoothness. THIS IS THE ONLY PLACE IN THIS PROJECT
	// THAT SPELLS THAT, and every value that reaches an Unreal roughness pin
	// comes through it. ProceduralRoughnessTexel above writes the same
	// arithmetic inline and predates this function; it is left alone
	// deliberately rather than routed through here, because it reproduces a
	// Unity byte and the suite asserts it against a hand-computed value, and
	// that is a different job from this one. The suite asserts the two agree.
	inline double RoughnessFromSmoothness(double Smooth)
	{
		return 1.0 - Smooth;
	}

	inline double SmoothnessFromRoughness(double Rough)
	{
		return 1.0 - Rough;
	}

	// THE ROUGHNESS A FULLY WET SURFACE APPROACHES, derived from the ceiling
	// rather than typed. This is the number the material graph's lerp uses as
	// its B pin, and tools/ue/make_base_material.py reads it OUT OF THIS FILE
	// rather than carrying its own copy.
	inline double WetRoughnessFloor()
	{
		return RoughnessFromSmoothness(WetSmoothnessCeiling());
	}

	// THE SAME ARITHMETIC IN THE SPACE UNREAL ACTUALLY READS, and the whole
	// point of naming it: a caller reaching for a roughness never has to do
	// the flip itself.
	//
	// IT IS ALGEBRAICALLY A LERP, WHICH IS WHY THE MATERIAL GRAPH CAN BE ONE
	// NODE. With d = 1 - R:
	//     1 - Smoothness(d, r) = 1 - d - (0.92 - d) r
	//                          = R - (R - 0.08) r
	//                          = R (1 - r) + 0.08 r
	// so Lerp(RoughnessMap.R, WetRoughnessFloor(), Wetness) per texel IS
	// this function per texel, and at Wetness 0 it is the map untouched,
	// bit for bit. The suite asserts the identity over a sweep rather than
	// trusting the three lines above.
	inline double WetRoughness(double DryRoughness, double Rain)
	{
		return RoughnessFromSmoothness(
			WetSmoothness(SmoothnessFromRoughness(DryRoughness), Rain));
	}

	// THE DRY SMOOTHNESS OF THE FOUR SURFACES RAIN LANDS ON, read out of
	// AssetLibrary.SurfaceSpec.For and guarded against it by
	// tools/surface-tint-check.py. It is a SECOND READER of that switch.
	//
	// WHAT IT IS FOR, AND WHAT IT IS NOT FOR. It is not an input to anything
	// that reaches a pixel on this side: the roughness a pack surface renders
	// is its own 2048x2048 roughness file, lerped per texel, and no scalar
	// here replaces it. It is the DATUM the verdict quotes so the direction
	// is readable from the numbers alone, and it is the other engine's own
	// number so the two runs are quoting the same surface.
	inline int GroundDryCount() { return 4; }

	inline const char* GroundDryName(int I)
	{
		const char* N[4] = {"asphalt", "sidewalk", "kerb", "concrete"};
		return (I >= 0 && I < 4) ? N[I] : "out-of-range";
	}

	inline double GroundDrySmoothnessAt(int I)
	{
		const double S[4] = {0.18, 0.10, 0.12, 0.10};
		return (I >= 0 && I < 4) ? S[I] : -1.0;
	}

	// -1 FOR A SURFACE THAT HAS NO ROW, because a surface with no datum and a
	// surface whose datum is zero are different facts and a shared 0.0 would
	// merge them.
	inline double GroundDrySmoothness(const std::string& Surface)
	{
		for (int I = 0; I < GroundDryCount(); ++I)
		{
			if (Surface == GroundDryName(I)) { return GroundDrySmoothnessAt(I); }
		}
		return -1.0;
	}

	// THE TWO LISTS MUST BE THE SAME FOUR SURFACES. IsGroundSurface decides
	// WHO gets wet and this table says HOW ROUGH each of them is dry; a
	// surface in one and not the other is a silent half-treatment, so the
	// suite asserts them against each other in both directions.
	inline bool GroundDryTableAgreesWithWetSurfaces()
	{
		for (int I = 0; I < GroundDryCount(); ++I)
		{
			if (!IsGroundSurface(GroundDryName(I))) { return false; }
		}
		return true;
	}

	// ---- WHAT A SURFACE'S BIND DOES WITH A WETNESS -----------------------
	//
	// THE PARAMETER'S ONE SPELLING, for the reason AlbedoGradeParam has one:
	// the generator and the binder cannot drift apart without the container
	// saying so before a dispatch. THE SELFTEST THAT HOLDS IT DOES NOT GREP
	// FOR THIS LITERAL. A grep over the tree would be satisfied by the line
	// below and would print green over a parameter nothing ever sets, which
	// is the shape of every comment-shaped guard this file has had to
	// correct. make_base_material.py --selftest asks the .cpp files for a
	// scalar set call and for WetnessParam IN THE SAME FILE: the declaration
	// here cannot satisfy either.
	inline const char* WetnessParam() { return "Wetness"; }

	// DRY IS ZERO, AND ZERO IS THE MATERIAL'S DEFAULT. An instance that never
	// sets this parameter renders exactly what it renders today, bit for bit,
	// because the lerp at alpha 0 is its A pin untouched. That is the
	// accepting case and it is the half that ships unrun, so the generator
	// asserts the number rather than the presence.
	inline double WetnessDry() { return 0.0; }

	// WHO GETS WET, AND IT IS THE OTHER ENGINE'S LIST. AssetLibrary's own
	// comment: "Ground the rain lands on. Walls and roofs are deliberately
	// absent - a vertical brick face does not pool water". IsGroundSurface
	// above is AssetLibrary.WetSurfaces character for character and this
	// reuses it rather than writing a fifth list.
	struct WetBind
	{
		double Wetness;       // what the scalar parameter is set to
		double AlbedoScale;   // the gamma multiplier folded into the grade
		bool   bWet;          // did this surface take the wetness at all
		bool   bAlbedo;       // did the COLOUR half apply as well as the roughness
		const char* Why;
		WetBind() : Wetness(0.0), AlbedoScale(1.0), bWet(false), bAlbedo(false),
		            Why("dry/nothing-decided-yet") {}
	};

	// THE TWO HALVES CAN DISAGREE AND THE STRUCT SAYS SO. The roughness half
	// applies to any ground surface, because a roughness map or the
	// material's default is there either way. The COLOUR half applies only
	// where AlbedoGradeFor took its textured branch: on the three white-grade
	// branches the value means "Unity would use a tint table this side has
	// only two rows of", and multiplying a wetness into that white would turn
	// an honest gap into a number. A ground surface whose albedo never bound
	// therefore gets the shine and not the darkening, WHICH IS THE FAILURE
	// THE THESIS ABOVE NAMES, so it is printed rather than hidden. All four
	// ground surfaces bound their albedo on run ce99814, so this is a guard
	// against a future gap and not a description of today.
	inline WetBind WetBindFor(const std::string& Surface, bool bTextured,
	                          double Wetness)
	{
		WetBind Out;
		if (!IsGroundSurface(Surface))
		{
			Out.Why = "not-in-AssetLibrary-WetSurfaces/walls-and-roofs-do-not-pool-water";
			return Out;
		}
		Out.bWet = true;
		Out.Wetness = WetClamp01(Wetness);
		if (!bTextured)
		{
			Out.Why = "no-albedo-bound-so-the-grade-is-white-and-a-wet-multiply-on-white-would-be-a-guess";
			return Out;
		}
		Out.bAlbedo = true;
		Out.AlbedoScale = WetAlbedoScale(Out.Wetness);
		Out.Why = "AssetLibrary-SetWetness-shape/both-halves";
		return Out;
	}

	// THE GRADE WITH THE WETNESS IN IT, AND THE CHAIN'S LAW IS UNCHANGED:
	// grade terms compose IN GAMMA and the product is converted ONCE.
	//
	// WHY GAMMA IS NOT A FREE CHOICE HERE EITHER. AssetLibrary.SetWetness
	// writes `mat.color = baseCol * albedo` where baseCol is a gamma Color
	// and Unity converts the product on upload, so the wetness multiply
	// happens in the same space GroundGrade and the walk-back happen in.
	//
	// AND JAFAR'S WALK-BACK IS NOT RE-APPLIED AND DOES NOT MOVE. It is
	// applied inside AlbedoGradeFor, at the one site it has always been
	// applied at, to exactly the legacy pair it was measured against; the
	// wetness multiplies the result. THE ORDER MATTERS AND IS NOT A
	// PREFERENCE: the walk-back is affine (1 - s(1 - G)) rather than a
	// multiply, so folding wetness in before it would put his 0.85 on a
	// darkening he has never seen in a frame. His own expiry note at
	// JafarGradeStrength says the value gets RE-READ when wetness lands.
	// This change does not re-read it and does not move it; it leaves the
	// number and the date on the verdict line so he can.
	inline Grade WetGradeFor(const std::string& Surface, bool bTextured,
	                         double Wetness)
	{
		Grade Out = AlbedoGradeFor(Surface, bTextured);
		const WetBind W = WetBindFor(Surface, bTextured, Wetness);
		if (!W.bAlbedo) { return Out; }
		Out.GammaR *= W.AlbedoScale;
		Out.GammaG *= W.AlbedoScale;
		Out.GammaB *= W.AlbedoScale;
		Out.R = LedgerVignette::SrgbToLinear(Out.GammaR);
		Out.G = LedgerVignette::SrgbToLinear(Out.GammaG);
		Out.B = LedgerVignette::SrgbToLinear(Out.GammaB);
		Out.Why = Out.bGround
			? "textureGrade-times-groundGrade-times-jafar-walkback-times-wetAlbedoScale"
			: "textureGrade-times-jafar-walkback-times-wetAlbedoScale";
		return Out;
	}


	// ---- WHICH WETNESS THE BIND SEEDS ITS INSTANCES WITH -----------------
	//
	// THIS WAS "THE ONE WETNESS THE RUN USES" UNTIL QUEUE 309, 2026-09-15,
	// AND IT IS A SEED NOW. The paragraph the heading used to carry said
	// nothing keeps the instances, so ApplyCondition cannot re-drive a
	// parameter per condition, and called that a design call the batch did
	// not make. The ruling of 07:55Z made it: the scene was keeping every
	// instance all along, on the component of every piece actor, and
	// ApplyCondition re-drives both parameters off GetMaterial(0) per
	// condition. So the sentences below are about a SEED, and every count
	// this struct carries is a count about that seed and not about any frame.
	//
	// BindSurfaces STILL RUNS ONCE, inside BuildScene, BEFORE ANY CONDITION
	// IS APPLIED, and that has not changed: there is no condition in force at
	// the moment a material instance is made, and the instance is the only
	// thing that can carry a parameter. Something has to be handed to it, and
	// this is the rule for what.
	//
	// THE RULE IS THE INTERACTIVE PATH'S OWN, which is already the project's
	// answer to "which condition is THE street's condition": the shared
	// file's own first shot, then overcast_day, then conditions[0]. A second
	// opinion about that would put two answers in one project.
	//
	// WHAT THE COUNTS MEAN NOW. ShotsAtValue over ShotsExamined was the size
	// of the static bind's compromise, because the shots at another wetness
	// were photographed at the wrong one. Since 309 every shot is
	// photographed at its own, so the gap is no longer a compromise: it is
	// how many shots needed no re-drive at all, and wetnessRedriveWalks on
	// the done line is the number that says what the re-drive did. On the
	// committed spec the seed is right for 35 of 43 without a walk.
	struct WetnessChoice
	{
		double      Value;
		const char* Why;
		std::string FromCondition;
		int ShotsAtValue, ShotsExamined;
		int CondsAtValue, CondsExamined;
		WetnessChoice() : Value(0.0), Why("dry/nothing-examined"),
		                  FromCondition("none"),
		                  ShotsAtValue(0), ShotsExamined(0),
		                  CondsAtValue(0), CondsExamined(0) {}
	};

	inline const LedgerVignette::Condition* FindConditionIn(
		const LedgerVignette::Spec& S, const std::string& Id)
	{
		for (size_t I = 0; I < S.Conditions.size(); ++I)
		{
			if (S.Conditions[I].Id == Id) { return &S.Conditions[I]; }
		}
		return 0;
	}

	inline WetnessChoice WetnessForBind(const LedgerVignette::Spec& S)
	{
		WetnessChoice Out;
		Out.CondsExamined = (int)S.Conditions.size();
		Out.ShotsExamined = (int)S.Shots.size();
		const LedgerVignette::Condition* Pick = 0;
		if (!S.Shots.empty())
		{
			Pick = FindConditionIn(S, S.Shots[0].ConditionId);
			if (Pick != 0) { Out.Why = "first-shot-condition"; }
		}
		if (Pick == 0)
		{
			Pick = FindConditionIn(S, "overcast_day");
			if (Pick != 0) { Out.Why = "overcast_day/no-usable-first-shot"; }
		}
		if (Pick == 0 && !S.Conditions.empty())
		{
			Pick = &S.Conditions[0];
			Out.Why = "conditions0/no-overcast_day-either";
		}
		if (Pick == 0)
		{
			// NOTHING MEASURED IS NOT ZERO WETNESS THAT SOMEBODY CHOSE. The
			// value is the same 0.0 either way and the reason is what tells
			// them apart, which is why the reason is on the line.
			Out.Why = "dry/the-shared-file-named-no-condition-at-all";
			return Out;
		}
		Out.Value = WetClamp01(Pick->Wetness);
		Out.FromCondition = Pick->Id;
		for (size_t I = 0; I < S.Conditions.size(); ++I)
		{
			if (std::fabs(WetClamp01(S.Conditions[I].Wetness) - Out.Value) < 1e-9)
			{
				++Out.CondsAtValue;
			}
		}
		for (size_t I = 0; I < S.Shots.size(); ++I)
		{
			const LedgerVignette::Condition* C =
				FindConditionIn(S, S.Shots[I].ConditionId);
			if (C != 0
			    && std::fabs(WetClamp01(C->Wetness) - Out.Value) < 1e-9)
			{
				++Out.ShotsAtValue;
			}
		}
		return Out;
	}

	// THE GRADE AS A TEXEL, so the pack lines and the procedural lines carry
	// tintTexel in THE SAME UNITS. A procedural surface's tintTexel is the
	// albedo byte its one flat texel ends up at; a pack surface has 2048x2048
	// of them and no single byte, so the reference texel is WHITE and this is
	// what white comes out as. The value on the line names which of the two
	// it is, because one key may not mean two things unnoticed.
	//
	// White is the identity in either space (SrgbToLinear(1) is 1), so this
	// is ByteOf of the gamma product, and a reader can check it with a
	// calculator: 0.74 x 0.55 x 255 rounds to 104.
	inline Texel GradeTexel(const Grade& G)
	{
		Texel T;
		T.R = LedgerVignette::ByteOf(LedgerVignette::LinearToSrgb(G.R));
		T.G = LedgerVignette::ByteOf(LedgerVignette::LinearToSrgb(G.G));
		T.B = LedgerVignette::ByteOf(LedgerVignette::LinearToSrgb(G.B));
		return T;
	}

	// THE IMAGE A CARD DECAL ASKS FOR. The Unity host's rule, at
	// StreetVignetteHost.EmitDecal: <Decals>/<id>.png for a card, and a SET
	// DIRECTORY for a multiply (a colour map beside an opacity map, joined by
	// DecalLayer.LoadSet). One extension and no search, because there is one
	// generator and it writes png.
	inline std::string DecalCardLeaf(const std::string& Id)
	{
		return Id + ".png";
	}

	// AND HOW SHINY AN OPAQUE PICTURE IS. StreetVignetteHost.EmitDecal sets
	// _Glossiness 0.08 on a card so a painted signboard takes the street's
	// light like the fascia behind it instead of glowing, and a roughness map
	// is the only way to say that to the base material here. The literal is
	// the Unity host's, read out of it, and checked against it by
	// tools/surface-tint-check.py in the container.
	inline double DecalCardSmoothness() { return 0.08; }

	inline int DecalCardRoughnessTexel()
	{
		return LedgerVignette::ByteOf(1.0 - DecalCardSmoothness());
	}

	// ---- THE ONE THING NO NUMBER IN THIS CONTAINER CAN ANSWER ------------
	//
	// WHICH WAY ROUND THE ENGINE'S PLANE READS ITS UVS. The Unity host draws a
	// decal on DecalLayer.Quad, whose winding the piece list states in words;
	// this side draws it on /Engine/BasicShapes/Plane, and nothing here knows
	// that mesh's uv layout. A lettered fascia arriving mirrored or upside
	// down is the failure, and it is a PICTURE fault that no count can see.
	//
	// So it is a lever rather than a guess: both flips are off, both are
	// printed on the decals done line, and if the first frame shows mirrored
	// lettering the fix is one word here and not a hunt through an emitter.
	// Rule 2 forbids calling either value anything better than the starting
	// point, and the frame is what moves it.
	inline bool DecalFlipRows() { return false; }
	inline bool DecalFlipCols() { return false; }

	// THE CROP, SPLIT OFF THE ASSET STRING, AND IT FAILS CLOSED.
	//
	// The one parser for this is StreetVignette.SplitAsset, tested in Core,
	// and this is the second reader of the same rule: `generated/x#u0,v0,u1,v1`
	// is an image path and a rectangle of it, u then v, v FROM THE BOTTOM, no
	// fragment meaning the whole image. A fragment that is not four numbers
	// returns bOk false and the caller refuses rather than guessing a
	// rectangle, which is what Core does too.
	//
	// WHY THE CROP MATTERS AT ALL: the generated pictures are photographs of
	// a thing IN a street, so fascia_fish_market is a whole shopfront with a
	// pavement and a sky in it. Pasting all of it on a fascia band puts a
	// photograph of a street on a street.
	struct DecalAsset
	{
		std::string Id;
		double U0, V0, U1, V1;
		bool   bOk;
		bool   bCropped;
		DecalAsset() : U0(0), V0(0), U1(1), V1(1), bOk(false), bCropped(false) {}
	};

	inline bool ParseCropNumber(const std::string& S, double& Out)
	{
		if (S.empty()) { return false; }
		for (size_t I = 0; I < S.size(); ++I)
		{
			const char C = S[I];
			const bool bDigit = (C >= '0' && C <= '9');
			if (!bDigit && C != '.' && C != '-' && C != '+'
			    && C != 'e' && C != 'E') { return false; }
		}
		Out = std::strtod(S.c_str(), 0);
		return true;
	}

	inline DecalAsset SplitDecalAsset(const std::string& Asset)
	{
		DecalAsset D;
		D.Id = Asset;
		if (Asset.empty()) { return D; }
		const size_t Hash = Asset.find('#');
		if (Hash == std::string::npos) { D.bOk = true; return D; }
		D.Id = Asset.substr(0, Hash);
		D.bCropped = true;
		const std::string Frag = Asset.substr(Hash + 1);
		std::string Part;
		std::vector<std::string> Parts;
		for (size_t I = 0; I <= Frag.size(); ++I)
		{
			if (I == Frag.size() || Frag[I] == ',')
			{
				Parts.push_back(Part);
				Part.clear();
				continue;
			}
			Part += Frag[I];
		}
		if (Parts.size() != 4) { return D; }
		double V[4] = {0, 0, 1, 1};
		for (int I = 0; I < 4; ++I)
		{
			if (!ParseCropNumber(Parts[(size_t)I], V[I])) { return D; }
		}
		D.U0 = V[0]; D.V0 = V[1]; D.U1 = V[2]; D.V1 = V[3];
		D.bOk = true;
		return D;
	}

	// THE RECTANGLE IN TEXELS, AND THE ROW ORDER IS THE WHOLE OF IT.
	//
	// The crop's v is measured from the BOTTOM of the image and a decoded
	// image's rows arrive TOP DOWN, so the first row of the crop is at
	// (1 - v1) * Height and not at v0 * Height. Getting that backwards would
	// put the sky of a shopfront photograph on a fascia and nothing in a
	// count could see it, which is why it is computed here and asserted
	// against a planted case in the g++ test.
	//
	// IT CLAMPS AND SAYS SO. A rectangle that reaches past the image, or one
	// that is the wrong way round, gives at least one texel rather than a
	// zero-sized upload, and bClamped is what separates a crop that fitted
	// from one that was made to fit.
	struct CropPx
	{
		int  X, Y, W, H;
		bool bClamped;
		CropPx() : X(0), Y(0), W(0), H(0), bClamped(false) {}
	};

	inline CropPx CropPixels(const DecalAsset& D, int ImageW, int ImageH)
	{
		CropPx C;
		if (ImageW <= 0 || ImageH <= 0) { return C; }
		double U0 = D.U0, U1 = D.U1, V0 = D.V0, V1 = D.V1;
		if (U1 < U0) { const double T = U0; U0 = U1; U1 = T; C.bClamped = true; }
		if (V1 < V0) { const double T = V0; V0 = V1; V1 = T; C.bClamped = true; }
		if (U0 < 0.0) { U0 = 0.0; C.bClamped = true; }
		if (V0 < 0.0) { V0 = 0.0; C.bClamped = true; }
		if (U1 > 1.0) { U1 = 1.0; C.bClamped = true; }
		if (V1 > 1.0) { V1 = 1.0; C.bClamped = true; }
		int X0 = (int)(U0 * (double)ImageW + 0.5);
		int X1 = (int)(U1 * (double)ImageW + 0.5);
		// THE FLIP, ONCE, HERE. v from the bottom into a top-down row index.
		int Y0 = (int)((1.0 - V1) * (double)ImageH + 0.5);
		int Y1 = (int)((1.0 - V0) * (double)ImageH + 0.5);
		if (X0 < 0) { X0 = 0; }
		if (Y0 < 0) { Y0 = 0; }
		if (X1 > ImageW) { X1 = ImageW; }
		if (Y1 > ImageH) { Y1 = ImageH; }
		if (X1 <= X0) { X1 = X0 + 1; C.bClamped = true; }
		if (Y1 <= Y0) { Y1 = Y0 + 1; C.bClamped = true; }
		if (X1 > ImageW) { X0 = ImageW - 1; X1 = ImageW; }
		if (Y1 > ImageH) { Y0 = ImageH - 1; Y1 = ImageH; }
		C.X = X0; C.Y = Y0; C.W = X1 - X0; C.H = Y1 - Y0;
		return C;
	}

	// ---- WHICH ROUTE PAINTS A PIECE, DECIDED IN ONE PLACE ----------------
	//
	// THE FAULT THIS REPLACES WAS ONE LINE: a piece whose surface did not
	// resolve to a pack file got `continue` and no material instance at all.
	// Four routes now, and a piece takes exactly one of them, so the tally
	// below adds up to the pieces examined and a reader can see which rule
	// painted what.
	enum EPaintRoute
	{
		Paint_None = 0,        // nothing painted it, and the reason is counted
		Paint_Pack,            // the pack answered for this surface
		Paint_Tint,            // built in code from the SurfaceSpec tint
		Paint_DecalCard,       // the piece's own picture, opaque
		Paint_DecalMultiply    // the piece's own picture, as a stain
	};

	inline const char* PaintRouteName(EPaintRoute R)
	{
		switch (R)
		{
		case Paint_Pack:           return "pack";
		case Paint_Tint:           return "tint";
		case Paint_DecalCard:      return "decal-card";
		case Paint_DecalMultiply:  return "decal-multiply";
		default:                   return "none";
		}
	}

	// THE DECISION, AND THE ORDER IS LOAD-BEARING. A decal blend is tested
	// FIRST, because card and multiply are not library surfaces and a bind
	// record for them can only ever be absent; then the procedural table,
	// because paint_yellow is ProceduralOnly and a pack file for it must be
	// ignored even if one appears; then the pack.
	inline EPaintRoute RouteFor(const std::string& Surface, bool bIsDecalPiece,
	                            bool bBindResolved)
	{
		if (bIsDecalPiece || IsDecalBlend(Surface))
		{
			return IsMultiplyBlend(Surface) ? Paint_DecalMultiply : Paint_DecalCard;
		}
		if (ProceduralSurfaceIndex(Surface) >= 0) { return Paint_Tint; }
		return bBindResolved ? Paint_Pack : Paint_None;
	}

	// ---- WHAT THE RUN PAINTED, AND WHAT IT DID NOT -----------------------
	//
	// WHOLE-RUN COUNTERS, one increment per piece, and the identity the
	// verdict can be checked against is Painted + Unpainted == Examined. Every
	// reason a piece went unpainted is its own counter, because "the pack has
	// no file" and "the image was not staged" and "no modulate material
	// exists" are three findings with three different next actions.
	struct PaintTally
	{
		int Examined;
		int Pack, Tint, DecalCard, DecalMultiply;
		int NoBind, NoActor, NoComponent, NoInstance;
		int DecalImageMissing, DecalCropRefused, DecalNoStainMaterial;
		int Hidden;
		PaintTally() : Examined(0), Pack(0), Tint(0), DecalCard(0), DecalMultiply(0),
		               NoBind(0), NoActor(0), NoComponent(0), NoInstance(0),
		               DecalImageMissing(0), DecalCropRefused(0),
		               DecalNoStainMaterial(0), Hidden(0) {}
	};

	inline int PaintedCount(const PaintTally& T)
	{
		return T.Pack + T.Tint + T.DecalCard + T.DecalMultiply;
	}

	inline int UnpaintedCount(const PaintTally& T)
	{
		return T.NoBind + T.NoActor + T.NoComponent + T.NoInstance
		     + T.DecalImageMissing + T.DecalCropRefused + T.DecalNoStainMaterial;
	}

	// THE SEGMENT THAT CARRIES THE NUMBER THIS WHOLE SECTION EXISTS FOR.
	// piecesUnpainted over the pieces EXAMINED, never over what the file
	// asked for: a run that died halfway must not divide by a denominator it
	// never reached. A run that examined nothing prints the words.
	inline std::string PaintRouteSegment(const PaintTally& T)
	{
		if (T.Examined <= 0)
		{
			return std::string(" piecesUnpainted=nothing-measured"
			                   " piecesPainted=nothing-measured"
			                   " paintRoutes=nothing-measured"
			                   " paintRouteNote=the-piece-loop-examined-no-piece");
		}
		char Buf[700];
		std::snprintf(Buf, sizeof(Buf),
			" piecesPainted=%d/%d piecesUnpainted=%d/%d"
			" paintRoutes=pack.%d/tint.%d/decal-card.%d/decal-multiply.%d"
			" paintUnpaintedWhy=no-pack-file.%d/no-actor.%d/no-component.%d"
			"/instance-refused.%d/decal-image-missing.%d/decal-crop-refused.%d"
			"/decal-needs-a-stain-material.%d"
			" decalQuadsHidden=%d/%d"
			" paintRouteStat=cumulative-over-the-pieces-this-run-examined"
			" paintRouteRule=decal-blend-first/then-the-procedural-table/then-the-pack"
			" paintIdentity=painted-plus-unpainted-equals-examined",
			PaintedCount(T), T.Examined, UnpaintedCount(T), T.Examined,
			T.Pack, T.Tint, T.DecalCard, T.DecalMultiply,
			T.NoBind, T.NoActor, T.NoComponent, T.NoInstance,
			T.DecalImageMissing, T.DecalCropRefused, T.DecalNoStainMaterial,
			T.Hidden, T.DecalCard + T.DecalMultiply + T.DecalImageMissing
			        + T.DecalCropRefused + T.DecalNoStainMaterial);
		return std::string(Buf);
	}

	// ---- ONE LINE PER DECAL PIECE ----------------------------------------
	//
	// PER-SAMPLE NUMBERS ONLY. Which image a quad asked for, what the decoder
	// said it IS, the rectangle that was cut out of it and how big that came
	// out, because "the decal is on the wall" and "the right part of the
	// picture is on the wall" are different facts and only the second one is
	// worth a fascia.
	struct DecalResult
	{
		std::string Piece, Blend, Id, Note, LoadedAs;
		int  FullW, FullH;
		CropPx Crop;
		bool bCropAsked, bLoaded, bPainted, bHidden;
		DecalResult() : FullW(0), FullH(0), bCropAsked(false), bLoaded(false),
		                bPainted(false), bHidden(false) {}
	};

	inline std::string DecalLine(const DecalResult& D)
	{
		std::string Out = "decal=" + LedgerVignette::NoSpaces(D.Piece);
		char Buf[520];
		std::snprintf(Buf, sizeof(Buf),
			" decalBlend=%s decalImage=%s decalStatus=%s",
			LedgerVignette::NoSpaces(D.Blend).c_str(),
			LedgerVignette::NoSpaces(D.Id).c_str(),
			D.bPainted ? "PAINTED" : (D.bHidden ? "HIDDEN" : "NOT-PAINTED"));
		Out += Buf;
		if (D.bLoaded)
		{
			std::snprintf(Buf, sizeof(Buf),
				" decalLoadedAs=%dx%d/%s decalCropPx=x%d..%d/y%d..%d"
				" decalCropSize=%dx%d decalCropAsked=%s decalCropClamped=%s",
				D.FullW, D.FullH,
				D.LoadedAs.empty() ? "unknown"
				                   : LedgerVignette::NoSpaces(D.LoadedAs).c_str(),
				D.Crop.X, D.Crop.X + D.Crop.W, D.Crop.Y, D.Crop.Y + D.Crop.H,
				D.Crop.W, D.Crop.H,
				D.bCropAsked ? "yes" : "whole-image",
				D.Crop.bClamped ? "YES" : "no");
			Out += Buf;
		}
		else
		{
			Out += " decalLoadedAs=not-loaded decalCropPx=not-loaded"
			       " decalCropSize=not-loaded decalCropAsked=not-loaded"
			       " decalCropClamped=not-loaded";
		}
		Out += " decalRowOrder=crop-v-from-the-bottom/image-rows-top-down";
		Out += " decalNote=" + LedgerVignette::NoSpaces(D.Note);
		return Out;
	}

	// AND THE DECAL PASS'S OWN DONE LINE. A pass that reached no decal says
	// so in words: 0 of 0 reads exactly like twenty that worked.
	inline std::string DecalsDoneLine(const std::vector<DecalResult>& All,
	                                  const std::string& Root, int RootFiles,
	                                  const std::vector<std::string>& Tried)
	{
		int Painted = 0, Loaded = 0, Hidden = 0, Cards = 0, Multiplies = 0;
		for (size_t I = 0; I < All.size(); ++I)
		{
			if (All[I].bPainted) { ++Painted; }
			if (All[I].bLoaded)  { ++Loaded; }
			if (All[I].bHidden)  { ++Hidden; }
			if (IsMultiplyBlend(All[I].Blend)) { ++Multiplies; } else { ++Cards; }
		}
		std::string Line;
		if (All.empty())
		{
			Line = "decalsStatus=NOT-REACHED decalsPainted=nothing-measured"
			       " decalsLoaded=nothing-measured decalsHidden=nothing-measured"
			       " decalsNote=the-decal-pass-reached-no-piece";
		}
		else
		{
			char Buf[640];
			std::snprintf(Buf, sizeof(Buf),
				"decalsStatus=%s decalsPainted=%d/%d decalsLoaded=%d/%d"
				" decalsHidden=%d/%d decalsByBlend=card.%d/multiply.%d"
				" decalsStat=cumulative-over-the-decal-pieces-in-the-shared-file"
				" decalsCardRule=the-image-cropped-at-decode-and-bound-opaque"
				" decalsMultiplyRule=a-stain-needs-a-modulate-material-and-this-build-has-one-opaque-base"
				" decalsMultiplyNote=drawn-in-unity-and-hidden-here/the-pair-differs-by-the-grime-until-that-material-exists",
				(Painted == (int)All.size()) ? "ALL"
				                            : (Painted == 0 ? "NONE" : "PARTIAL"),
				Painted, (int)All.size(), Loaded, (int)All.size(),
				Hidden, (int)All.size(), Cards, Multiplies);
			Line = Buf;
		}
		Line += " decalRoot=" + (Root.empty() ? std::string("NOT-FOUND")
		                                      : LedgerVignette::NoSpaces(Root));
		char Tail[180];
		std::snprintf(Tail, sizeof(Tail),
			" decalRootFiles=%d decalFlip=rows.%s/cols.%s"
			" decalFlipNote=a-starting-point-not-a-measurement/the-engine-plane-uv-"
			"winding-is-unknown-here-and-the-frame-answers-it",
			RootFiles, DecalFlipRows() ? "yes" : "no", DecalFlipCols() ? "yes" : "no");
		Line += Tail;
		Line += " decalRootTried=" + PathListValue(Tried, 8);
		return Line;
	}

	// ---- WHAT THE INSTANCE HOLDS, ASKED RATHER THAN ASSUMED --------------
	//
	// THE ENGINE'S OPINION IS A MEASUREMENT. A dynamic material instance can
	// be handed a texture and two scalars and still render the base
	// material's own defaults, and until now nothing in this project has
	// asked an instance what it holds. The engine layer sets a parameter and
	// asks for it straight back in the same statement pair; what the answer
	// MEANS, and every count and string built from it, is decided here where
	// g++ runs it before a dispatch.
	//
	// THE TEXTURE AND THE SCALAR ARE A PAIR AND NEITHER IS READ ALONE. They
	// take different paths into the render proxy, so a full scalar readback
	// beside a short texture one is a finding about the texture path and two
	// short ones are a finding about every path. They are not one number
	// twice, which is the whole reason both are asked for.
	//
	// PER SURFACE, ON THE FIRST INSTANCE MADE FOR IT. 563 pieces would print
	// 563 identical answers to a question that is about the material.
	//
	// WHAT IT CANNOT SEE, SAID PLAINLY RATHER THAN LEFT TO BE ASSUMED: this
	// is the GAME thread's copy of the parameter. A value that lands here and
	// never reaches the render proxy still reads back same-pointer, which is
	// exactly why the control quads below ship in the same dispatch: they are
	// the render side of the same question and they answer in a picture.
	struct Readback
	{
		bool bAsked = false;          // a parameter was actually set on an instance
		bool bTexSame = false;        // what came back IS the pointer that went in
		bool bScalarSame = false;     // BOTH tiling scalars came back as they went in
		bool bResourceValid = false;  // Tex->GetResource() read AFTER UpdateResource
		bool bCompIsMid = false;      // the component renders the instance we made
		// WHAT CAME BACK WHEN IT WAS NOT WHAT WENT IN. The engine's own path
		// name, because "not the same pointer" does not say whether the
		// answer was null, the parent's default texture or something else,
		// and those are three different next actions.
		std::string TexGot  = "not-asked";
		std::string CompGot = "not-asked";
		double SetU = 0.0, GotU = 0.0;
		double SetV = 0.0, GotV = 0.0;
		// THE WETNESS SCALAR, ASKED STRAIGHT BACK. A parameter the material
		// does not carry SETS NOTHING, RETURNS NOTHING AND LOGS NOTHING, so
		// the only thing that can tell a live parameter from a dead write is
		// asking the instance what it now holds. bWetAsked false prints the
		// words: an instance nothing was set on is not an instance that
		// answered wrongly.
		bool   bWetAsked = false;
		bool   bWetSame = false;
		double SetWet = 0.0, GotWet = 0.0;
	};

	// ONE TOLERANCE, NAMED, BECAUSE THE ENGINE STORES A FLOAT AND THE FILE
	// CARRIES A DOUBLE. 21.0 survives that trip exactly and 1.371 does not,
	// so an exact comparison would print a mismatch that belongs to the
	// conversion rather than to the engine.
	inline double ScalarEpsilon() { return 1e-4; }

	inline bool ScalarMatches(double Set, double Got)
	{
		const double A = (Set < 0.0) ? -Set : Set;
		const double D = (Set > Got) ? (Set - Got) : (Got - Set);
		return D <= ScalarEpsilon() * ((A > 1.0) ? A : 1.0);
	}

	// ONE SURFACE'S OUTCOME. Status is set by the caller because the ways to
	// fail are different facts with different next actions: a file that is
	// not in the pack, a file the decoder refused, and a base material that
	// never loaded are three separate findings and none of them is "the
	// texture did not help".
	struct Bound
	{
		std::string Surface;
		int         Pieces = 0;           // pieces in the file wearing this surface
		int         PiecesAssigned = 0;   // of those, how many got an instance
		std::string Status = "NOT-REACHED";
		std::string Reason = "none";
		bool        MapFound[3] = {false, false, false};
		std::string MapFile[3];
		int         MapW[3] = {0, 0, 0};
		int         MapH[3] = {0, 0, 0};
		std::string MapLoadedAs[3];       // what the DECODER said it is
		// BORROWED MAPS ARE COUNTED APART FROM FOUND ONES, and that is not
		// pedantry: mapsFound is "this surface's own candidate answered" and
		// the interior's normal and roughness are the WINDOW's files, bound by
		// the rule at AssetLibrary.cs:611. Folding them into MapFound would
		// move mapsFound from 36/36 to 38/36, a fraction above one, and change
		// what that number means without changing its name, which is the
		// quietest way there is to lose a reading. They print on mapsBorrowed.
		// THE DENOMINATOR WAS 48 UNTIL QUEUE 227 and is now 36: three maps per
		// library surface whose albedo is expected from the pack, which is
		// twelve surfaces, not sixteen. Nothing about the pack changed.
		bool        MapBorrowed[3] = {false, false, false};
		std::string BorrowedFrom;         // the surface the maps came from
		// WHICH RULE PAINTED THIS SURFACE, and the tint it was painted with.
		// Empty Route means the material pass never reached a piece of it.
		std::string Route;
		Texel       Tint;
		bool        bTintBuilt = false;
		// WHAT WAS ACTUALLY HANDED TO THE AlbedoGrade PARAMETER, recorded at
		// the bind site rather than recomputed by the printer. The two are
		// the same number today and would stop being the same number the
		// first time a bind is skipped, which is precisely the case the line
		// has to be able to say out loud: bGradeSet false prints not-built,
		// exactly as bTintBuilt false does, so "no grade was set" can never
		// be read as "the grade was set to this".
		Grade       Graded;
		bool        bGradeSet = false;
		// AND WHAT THE WETNESS HALF DID, recorded at the bind site rather
		// than recomputed by the printer, for the reason Graded is: the two
		// would be the same number today and would stop being the same
		// number the first time a bind is skipped. bWetSet false prints the
		// words, exactly as bGradeSet false does, because "no wetness was
		// set" and "the wetness was set to zero" are different findings with
		// different next actions and one of them is a dead write.
		WetBind     Wet;
		bool        bWetSet = false;
		// WHICH CONDITION'S WETNESS THIS SURFACE IS CURRENTLY CARRYING,
		// QUEUE 309. Wet above used to be written once, at bind time, and
		// was therefore the whole story; ApplyCondition now re-drives it per
		// condition, so Wet is LAST-WINS over the conditions the run applied
		// and a value with no condition beside it would not say which frame
		// it describes. The words below are what a run that never re-drove
		// anything prints, so "the bind's own seed" can never read as "the
		// last condition asked for this".
		std::string WetFrom = "bind-time-seed/no-condition-was-applied-after-it";
		// WHETHER THIS SURFACE'S ALBEDO TEXTURE ACTUALLY BOUND, recorded at
		// the bind site for the reason Graded is: the re-drive has to hand
		// WetBindFor and WetGradeFor the SAME two inputs BindSurfaces handed
		// them or the two would disagree about the colour half, and the
		// texture array that answered the question at bind time is local to
		// that function and gone by the time a condition is applied.
		bool        bAlbedoBound = false;
		double      TileU = 0.0;          // the last piece's tiling, as a sample
		double      TileV = 0.0;
		// WHAT THE FIRST INSTANCE OF THIS SURFACE ANSWERED WHEN ASKED. Kept
		// on the same record the per-surface line and the run totals are both
		// built from, so a total and its lines cannot disagree.
		Readback    Read;
	};

	inline bool IsResolved(const Bound& B) { return B.MapFound[0]; }

	// ---- THE POPULATION A SURFACE COUNT IS OVER, QUEUE 227 ---------------
	//
	// A DECAL BLEND MODE IS NOT A LIBRARY SURFACE. card and multiply name the
	// two ways a decal is composited, declared in words at
	// ledger/Assets/Scripts/Core/StreetVignette.cs:57 and refused at 1651 if
	// they are anything else; the picture comes from the piece's own asset
	// field. Counting them in the denominator made surfacesResolved=16/16
	// reachable ONLY by writing card.png and multiply.png into the pack, and
	// doing that would paint one shared image across four different shop
	// fascias and three different interiors. A GREEN THAT REQUIRES SHIPPING
	// WRONG CONTENT IS A MISMEASUREMENT AND NOT A GATE, so the blend modes are
	// counted on their own key and the library count is what the surface
	// numbers divide by.
	inline int LibrarySurfaceCount(const std::vector<Bound>& All)
	{
		int N = 0;
		for (size_t I = 0; I < All.size(); ++I)
		{
			if (!IsDecalBlend(All[I].Surface)) { ++N; }
		}
		return N;
	}

	// A LIBRARY SURFACE IS ACCOUNTED FOR TWO WAYS AND ONLY TWO. Its albedo
	// came out of the pack, or the Unity host generates it from the
	// SurfaceSpec tint and this file carries the same literals. Anything else
	// is ABSENT: no pack file AND no spec entry, which IS a real fault and is
	// the only thing that should ever hold this status below ALL.
	inline bool IsProceduralSurface(const Bound& B)
	{
		return !IsDecalBlend(B.Surface) && !IsResolved(B)
		    && ProceduralSurfaceIndex(B.Surface) >= 0;
	}

	// THE READBACK, PER SURFACE, ON THE SURFACE'S OWN LINE. Per-sample
	// numbers on the sample line; the run's totals are on the done line
	// below and NO KEY MEANS TWO THINGS ON TWO LINES, which is why the
	// scalar reading is midTilingReadback here and midScalarReadback there:
	// one is a word about one surface and the other is a count over the run,
	// and a grep that found either under one name would take whichever line
	// it reached first.
	//
	// A SURFACE NOTHING WAS SET ON PRINTS THE WORDS. A `no` here would say
	// the engine answered wrongly, and "nothing was asked" is a different
	// fact with a different next action.
	inline std::string ReadbackFields(const Readback& R)
	{
		if (!R.bAsked)
		{
			return " midTexReadback=not-asked midTilingReadback=not-asked"
			       " midTexResource=not-asked midCompMaterial=not-asked"
			       " midTilingSetGot=not-asked midWetReadback=not-asked"
			       " midWetSetGot=not-asked";
		}
		const std::string TexWord = R.bTexSame
			? std::string("same-pointer")
			: ("OTHER/" + LedgerVignette::NoSpaces(R.TexGot));
		const std::string CompWord = R.bCompIsMid
			? std::string("is-the-instance-we-made")
			: ("OTHER/" + LedgerVignette::NoSpaces(R.CompGot));
		char Buf[220];
		std::snprintf(Buf, sizeof(Buf),
			" midTilingReadback=%s midTexResource=%s"
			" midTilingSetGot=U.%.4f..%.4f/V.%.4f..%.4f",
			R.bScalarSame ? "same-value" : "DIFFERENT",
			R.bResourceValid ? "valid" : "NULL",
			R.SetU, R.GotU, R.SetV, R.GotV);
		// THE WETNESS SCALAR'S OWN READBACK, AND IT IS THE ONE THAT ANSWERS
		// "IS THIS A DEAD WRITE". A material with no such parameter accepts
		// the set silently and returns the parameter's absence as zero, so a
		// value that went in as 0.6000 and comes back 0.0000 is the failure
		// queue 186 predicted, named, on the line, with both numbers.
		char WBuf[140];
		if (!R.bWetAsked)
		{
			std::snprintf(WBuf, sizeof(WBuf),
				" midWetReadback=not-asked midWetSetGot=not-asked");
		}
		else
		{
			std::snprintf(WBuf, sizeof(WBuf),
				" midWetReadback=%s midWetSetGot=%.4f..%.4f",
				R.bWetSame ? "same-value" : "DIFFERENT", R.SetWet, R.GotWet);
		}
		return " midTexReadback=" + TexWord + Buf + " midCompMaterial=" + CompWord
		     + WBuf;
	}

	// THE RUN'S READBACK TOTALS, COUNTED OVER THE SURFACES A PARAMETER WAS
	// ACTUALLY SET ON. That denominator is not the number of surfaces the
	// street asked for: a surface with no albedo file never reaches an
	// instance, and folding it into the denominator would report a bind that
	// never happened as a bind that failed. Both denominators are printed,
	// so neither reading is available only by subtraction.
	//
	// A RUN THAT SET NOTHING PRINTS THE WORDS RATHER THAN A ZERO. `0/0` and
	// "no instance was ever made" read alike to a grep, and this is the
	// difference between an engine that answered wrongly and a pass that
	// never ran.
	inline std::string ReadbackDoneSegment(const std::vector<Bound>& All)
	{
		int Asked = 0, Tex = 0, Scalar = 0, Res = 0, Comp = 0;
		// THE DENOMINATOR IS THE LIBRARY POPULATION AND NOT All.size(),
		// QUEUE 227: a parameter is never set on a decal blend mode, so
		// counting card and multiply here made 14/16 read as two surfaces
		// the readback missed when nothing was ever asked of them.
		const int LibN = LibrarySurfaceCount(All);
		// THE WETNESS READBACK HAS ITS OWN DENOMINATOR AND NOT THIS ONE.
		// A surface that is not in WetSurfaces is still asked, so folding it
		// into Asked would be right; but a run in which the scalar was never
		// asked at all must not read as a run in which it came back wrong,
		// so the count of ASKINGS is carried separately.
		int WetAsked = 0, WetSame = 0;
		for (size_t I = 0; I < All.size(); ++I)
		{
			if (All[I].Read.bWetAsked)
			{
				++WetAsked;
				if (All[I].Read.bWetSame) { ++WetSame; }
			}
			if (!All[I].Read.bAsked) { continue; }
			++Asked;
			if (All[I].Read.bTexSame)        { ++Tex; }
			if (All[I].Read.bScalarSame)     { ++Scalar; }
			if (All[I].Read.bResourceValid)  { ++Res; }
			if (All[I].Read.bCompIsMid)      { ++Comp; }
		}
		const std::string WetTotal = WetAsked == 0
			? std::string(" midWetReadbackAll=nothing-measured/no-surface-was-"
			              "asked-for-the-wetness-scalar")
			: (" midWetReadbackAll=" + std::to_string(WetSame) + "/"
			   + std::to_string(WetAsked)
			   + "/surfaces-whose-wetness-came-back-as-it-went-in-over-surfaces-asked");
		char Buf[520];
		if (Asked == 0)
		{
			std::snprintf(Buf, sizeof(Buf),
				" midReadbackAsked=0/%d midParamReadback=nothing-measured"
				" midScalarReadback=nothing-measured texResourceValid=nothing-measured"
				" compMaterialIsMid=nothing-measured"
				" midReadbackNote=no-surface-reached-an-instance/nothing-was-set-so-nothing-was-read-back",
				LibN);
			return std::string(Buf) + WetTotal;
		}
		std::snprintf(Buf, sizeof(Buf),
			" midReadbackAsked=%d/%d midParamReadback=%d/%d midScalarReadback=%d/%d"
			" texResourceValid=%d/%d compMaterialIsMid=%d/%d"
			" midReadbackStat=per-surface/first-instance-of-that-surface/game-thread-copy-not-the-render-proxy"
			" midReadbackPairRule=both-full-is-candidate-C/scalar-full-and-texture-short-is-B/both-short-is-A",
			Asked, LibN, Tex, Asked, Scalar, Asked,
			Res, Asked, Comp, Asked);
		return std::string(Buf) + WetTotal;
	}

	// ---- QUEUE 309: THE PER-CONDITION RE-DRIVE, AND ITS GUARD ------------
	//
	// RULED 2026-09-15 07:55Z: NO NEW GLOBAL AND NO SECOND LIST. Queue 186
	// left the wetness static because nothing kept the material instances it
	// made, and called a list of them a new global wanting an owner. The
	// ruling refused the list: the scene ALREADY keeps every instance, on the
	// component of every piece actor, and run ce99814 proved it by asking
	// (compMaterialIsMid=is-the-instance-we-made on every reached line). So
	// the owner is ApplyCondition, the list is the scene, and what lives here
	// is the decision, the counts and every printed string.
	//
	// WHAT THE .cpp SUPPLIES: the walk and live state. Which pieces exist,
	// which component answers with a dynamic instance, and the condition in
	// force. Not one word of the string below is decided up there, for the
	// reason this whole header exists: VignetteShot.cpp does not compile in
	// the container the tests run in, so arithmetic written there ships
	// UNRUN and an unrun formatter printing a plausible string is the
	// silent-instrument failure.
	//
	// WHY THIS BLOCK SITS HERE AND NOT BESIDE WetBindFor. The guard compares
	// two wetnesses, and this project has exactly ONE scalar tolerance,
	// ScalarMatches, declared above. A second epsilon written 600 lines
	// earlier so the block could sit with its relatives would be two
	// tolerances for one job, which is the shape every duplicated rule in
	// this file has been corrected back from.

	// WHICH PIECES A RE-DRIVE MAY TOUCH, AND IT IS NOT "EVERY PIECE THAT
	// CARRIES AN INSTANCE". THE TRAP, NAMED BEFORE THE CODE: the decal-card
	// route in BindSurfaces also creates a dynamic instance and deliberately
	// sets NEITHER AlbedoGrade NOR Wetness on it, so a walk that re-drove
	// every MID it found would write two parameters onto ten shop signs and
	// ten posters that have never carried them, and would do it in the frame
	// rung 1 is judged on. The routes below are exactly the ones whose
	// instances BindSurfaces sets the pair on: it handles both decal routes
	// and `continue`s, and everything that falls through is pack or tint.
	// RouteFor is the same decision the bind used, re-run from the same three
	// inputs, so no membership is stored anywhere.
	inline bool WetRedriveTouches(EPaintRoute R)
	{
		return R == Paint_Pack || R == Paint_Tint;
	}

	// EVERY OUTCOME OF ONE PIECE'S VISIT IS COUNTED, because "the walk wrote
	// nothing" and "the walk found nothing it was allowed to write on" are
	// different findings with different next actions, and a bare
	// piecesWritten=0 reads as the first when it is usually the second.
	enum EWetRedriveOutcome
	{
		WetRedrive_Wrote = 0,     // both parameters written on this piece
		WetRedrive_NotOurRoute,   // a decal card, a stain, or nothing painted it
		WetRedrive_NoActor,       // the piece name is in the file and not in the scene
		WetRedrive_NoComponent,   // the actor has no static mesh component
		WetRedrive_NoMid,         // GetMaterial(0) is not a dynamic instance
		WetRedrive_NoBind,        // the piece's surface is in no bind record
		WetRedrive_OutcomeCount
	};

	// THE WRITE-ON-CHANGE GUARD'S STATE AND ITS WHOLE-RUN TALLIES.
	//
	// WHY A GUARD AT ALL, and it is a measurement rather than a worry:
	// ApplyCondition is re-entered on EVERY tick while a condition settles,
	// and the sky above it carries the same guard for the same reason with
	// its own two counters. A naive re-drive is one parameter write per piece
	// per tick over 593 pieces, and nothing in a verdict would say so.
	//
	// WHAT EACH NUMBER IS A STATISTIC OF, and all of them are CUMULATIVE over
	// the whole run rather than per shot:
	//   Calls        times ApplyCondition asked for a wetness. Ticks, not
	//                shots: this is the denominator the guard is read against.
	//   Walks        times the guard let a walk run, which is once per
	//                CHANGED wetness and not once per tick. Walks + Skipped
	//                is Calls, and a line that breaks that identity says so.
	//   Skipped      asks the guard refused because the wetness had not moved.
	//   PieceVisits  pieces examined across every walk that ran.
	//   Out[]        what became of each of those visits, one bucket each.
	struct WetRedrive
	{
		double      LastWetness;
		bool        bEverApplied;
		std::string LastFrom;
		int         Calls, Walks, Skipped, PieceVisits;
		int         Out[WetRedrive_OutcomeCount];
		// THE READBACK TAKEN AT THE LAST WALK, on the first piece that walk
		// wrote. A value that lands on the game thread's copy and never
		// reaches the render proxy still reads back same-value, which is what
		// the control quads answer; this answers the other half, which is
		// whether the material carries the parameter at all.
		bool        bReadAsked;
		bool        bReadSame;
		double      ReadSet, ReadGot;
		WetRedrive()
			: LastWetness(0.0), bEverApplied(false),
			  LastFrom("no-condition-was-applied"),
			  Calls(0), Walks(0), Skipped(0), PieceVisits(0),
			  bReadAsked(false), bReadSame(false), ReadSet(0.0), ReadGot(0.0)
		{
			for (int I = 0; I < WetRedrive_OutcomeCount; ++I) { Out[I] = 0; }
		}
	};

	// THE DECISION, AND IT IS THE WHOLE GUARD. A first application always
	// writes, because "nothing has been applied yet" is not "the value has
	// not moved": the instances carry the bind-time seed and the first
	// condition may disagree with it. After that it is the one tolerance.
	inline bool WetRedriveNeeded(const WetRedrive& G, double Wetness)
	{
		if (!G.bEverApplied) { return true; }
		return !ScalarMatches(G.LastWetness, WetClamp01(Wetness));
	}

	inline void WetRedriveAsked(WetRedrive& G) { ++G.Calls; }

	inline void WetRedriveSkipped(WetRedrive& G) { ++G.Skipped; }

	// LATCHED ON THE ASK AND NOT ON A SUCCESSFUL WRITE, deliberately. The
	// guard's question is "has this value already been walked for", and a
	// scene in which no piece could be written is a scene where walking again
	// next tick would find the same nothing 593 times a second. What that
	// failure costs instead is visibility, and it is paid for in full: the
	// outcome buckets below print which refusal happened and how often, so a
	// walk that wrote zero pieces is a NUMBER on the line rather than a
	// silent re-walk nobody can see.
	inline void WetRedriveWalked(WetRedrive& G, double Wetness,
	                             const std::string& CondId)
	{
		G.LastWetness  = WetClamp01(Wetness);
		G.bEverApplied = true;
		G.LastFrom     = CondId;
		++G.Walks;
	}

	inline void WetRedriveVisit(WetRedrive& G, EWetRedriveOutcome O)
	{
		++G.PieceVisits;
		if ((int)O >= 0 && (int)O < WetRedrive_OutcomeCount) { ++G.Out[(int)O]; }
	}

	inline void WetRedriveReadback(WetRedrive& G, double Set, double Got)
	{
		G.bReadAsked = true;
		G.ReadSet    = Set;
		G.ReadGot    = Got;
		G.bReadSame  = ScalarMatches(Set, Got);
	}

	// THE WHOLE-RUN SEGMENT, FOR THE MATERIALS DONE LINE. Whole-run keys
	// only: every number here is cumulative over the run and none of them is
	// true of one frame, so none may ride a shot line. The per-frame half is
	// WetShotFields below and carries different key names on purpose.
	//
	// A RUN THAT NEVER APPLIED A CONDITION PRINTS THE WORDS. `0/0` and "the
	// owner was never called" read alike to a grep and are different facts.
	inline std::string WetRedriveSegment(const WetRedrive& G)
	{
		if (G.Calls == 0)
		{
			return " wetnessNow=nothing-measured wetnessNowFrom=no-condition-was-applied"
			       " wetnessRedriveWalks=nothing-measured/of=0/ApplyCondition-calls"
			       " wetnessRedriveSkipped=nothing-measured/of=0/ApplyCondition-calls"
			       " wetnessRedriveWrote=nothing-measured/of=0/piece-visits"
			       " wetnessRedriveRefused=nothing-measured"
			       " wetnessRedriveReadback=not-asked wetnessRedriveSetGot=not-asked"
			       " wetnessRedriveStat=whole-run/cumulative/ApplyCondition-was-never-"
			       "called-so-no-wetness-was-ever-driven-and-the-pieces-carry-the-bind-seed";
		}
		char Buf[860];
		std::snprintf(Buf, sizeof(Buf),
			" wetnessNow=%.4f wetnessNowFrom=%s"
			" wetnessRedriveWalks=%d/of=%d/ApplyCondition-calls/"
			"one-walk-per-CHANGED-wetness-and-not-one-per-settle-tick"
			" wetnessRedriveSkipped=%d/of=%d/ApplyCondition-calls/"
			"the-guard-refused-an-unchanged-wetness"
			" wetnessRedriveWrote=%d/of=%d/piece-visits-across-the-walks-that-ran"
			" wetnessRedriveRefused=notOurRoute.%d/noBind.%d/noActor.%d/"
			"noComponent.%d/noMid.%d"
			" wetnessRedriveReadback=%s wetnessRedriveSetGot=%.4f..%.4f"
			" wetnessRedriveStat=whole-run/cumulative-over-every-walk/"
			"walks-plus-skipped-is-calls/wrote-over-piece-visits-and-NOT-over-"
			"pieces-in-the-file/readback-is-the-last-walks-first-written-piece",
			G.bEverApplied ? G.LastWetness : 0.0,
			LedgerVignette::NoSpaces(G.LastFrom).c_str(),
			G.Walks, G.Calls, G.Skipped, G.Calls,
			G.Out[WetRedrive_Wrote], G.PieceVisits,
			G.Out[WetRedrive_NotOurRoute], G.Out[WetRedrive_NoBind],
			G.Out[WetRedrive_NoActor], G.Out[WetRedrive_NoComponent],
			G.Out[WetRedrive_NoMid],
			!G.bReadAsked ? "not-asked" : (G.bReadSame ? "same-value" : "DIFFERENT"),
			G.ReadSet, G.ReadGot);
		std::string Out(Buf);
		if (!G.bReadAsked)
		{
			// THE PAIR OF NUMBERS ABOVE IS 0.0000..0.0000 WHEN NOTHING WAS
			// ASKED, and that is the same string a dead write on a dry
			// condition prints. The word not-asked is on the readback key and
			// this says which of the two it is in prose, because the numbers
			// alone cannot.
			Out += " wetnessRedriveReadNote=no-piece-was-written-so-nothing-was-"
			       "asked-back/the-pair-above-is-a-placeholder-and-not-a-reading";
		}
		// ONE IDENTITY, PRINTED ONLY WHEN IT BREAKS, which is the shape
		// VignetteSpec.h's propCollisionReadingsMismatch already uses. Every
		// ask is either walked or skipped, from one counter each, and a key
		// that appears at all means one of the three is wrong.
		if (G.Walks + G.Skipped != G.Calls)
		{
			char M[128];
			std::snprintf(M, sizeof(M),
			              " wetnessRedriveTallyMismatch=walks=%d/skipped=%d/calls=%d",
			              G.Walks, G.Skipped, G.Calls);
			Out += M;
		}
		return Out;
	}

	// ---- QUEUE 309: THE WETNESS ONE FRAME WAS PHOTOGRAPHED AT ------------
	//
	// PER-SAMPLE KEYS ON THE SAMPLE LINE, AND THE NAMES ARE THE SURFACE
	// LINE'S WITH A shot PREFIX RATHER THAN THE SAME NAMES. midWetSetGot is a
	// statement about ONE SURFACE and lives on that surface's line; a key of
	// the same name on 43 shot lines would be the thing this file forbids
	// twice over already (midTilingReadback against midScalarReadback), where
	// a grep for either returns whichever line it reaches first.
	//
	// WHY THIS EXISTS AT ALL, which is the only evidence 309 can offer. The
	// surface line's wetSet is LAST-WINS over the run: it cannot tell "the
	// wetness was re-driven per condition" from "the wetness was set once, to
	// the last condition's value". Only a per-frame key can, and the way it
	// does it is shotWetnessAgrees: the wetness this frame's condition ASKS
	// for, against the wetness the pieces are CARRYING at the moment the
	// frame is taken.
	//
	//   shotWetness         what this frame's condition asks for. Not a
	//                       statistic: one number off one row of the file.
	//   shotWetnessOnPieces what the pieces carry, off the guard's latch.
	//   shotWetnessAgrees   the two compared with the one tolerance. NO is
	//                       the fault: the frame was photographed at a
	//                       wetness the street is not wearing.
	//   shotWetnessWalkedAt the condition the last walk ran for. It is
	//                       DIFFERENT from this shot's condition whenever the
	//                       guard skipped, which is the guard working and not
	//                       a fault, so both are printed rather than one.
	struct WetShotIn
	{
		double      Asked;         // this frame's condition's wetness
		std::string AskedFrom;     // this frame's condition id
		bool        bEverApplied;  // has any walk run at all
		double      OnPieces;      // the guard's latched value
		std::string WalkedAt;      // the condition the last walk ran for
		WetShotIn() : Asked(0.0), AskedFrom("none"), bEverApplied(false),
		              OnPieces(0.0), WalkedAt("no-condition-was-applied") {}
	};

	inline std::string WetShotFields(const WetShotIn& In)
	{
		if (!In.bEverApplied)
		{
			return " shotWetness=" + std::string("nothing-measured")
			     + " shotWetnessOnPieces=nothing-measured"
			     + " shotWetnessAgrees=nothing-measured"
			     + " shotWetnessWalkedAt=no-walk-ran-before-this-frame"
			     + " shotWetnessStat=per-sample/this-frame-only/"
			       "no-condition-had-been-applied-when-this-frame-was-taken";
		}
		char Buf[420];
		std::snprintf(Buf, sizeof(Buf),
			" shotWetness=%.4f shotWetnessFrom=%s"
			" shotWetnessOnPieces=%.4f shotWetnessAgrees=%s"
			" shotWetnessWalkedAt=%s"
			" shotWetnessStat=per-sample/this-frame-only/asked-is-off-this-rows-"
			"condition-and-onPieces-is-the-value-the-re-drive-last-latched/"
			"walkedAt-differing-from-From-is-the-guard-skipping-an-unchanged-"
			"wetness-and-is-not-a-fault",
			WetClamp01(In.Asked), LedgerVignette::NoSpaces(In.AskedFrom).c_str(),
			In.OnPieces,
			ScalarMatches(WetClamp01(In.Asked), In.OnPieces) ? "yes" : "NO",
			LedgerVignette::NoSpaces(In.WalkedAt).c_str());
		return std::string(Buf);
	}

	// THE WHOLE-RUN WETNESS SEGMENT, FOR THE MATERIALS DONE LINE.
	//
	// A SPEC WHOSE WETNESS IS ZERO PRINTS THAT IT WAS ZERO. "0.0000" and "no
	// wetness was applied" are different findings and a blank would merge
	// them, so the value is always printed and the reason always beside it.
	// EVERY ZERO SHIPS ITS DENOMINATOR: how many surfaces were examined, how
	// many the scalar was set on, and how many shots the one value is right
	// for.
	//
	// THE KEY WAS wetnessValue UNTIL QUEUE 309 AND IT IS wetnessBindValue
	// NOW, because the thing it names stopped being the thing it named. It
	// was "the one value handed to every instance this run" and it is now
	// "the value every instance was MADE with, before any condition existed";
	// the value in force is wetnessNow on the re-drive segment. A key whose
	// meaning moves under its own name is the quietest way this project has
	// found to lose a reading, so the name moved with the meaning and the
	// suite asserts the old token is NOT on the line: a reader greping the
	// old name on a new verdict gets nothing rather than a number that means
	// something else. Same for wetnessFrom, now wetnessBindFrom.
	//
	// WHAT EACH NUMBER IS A STATISTIC OF:
	//   wetnessBindValue    the value every instance was MADE with, chosen
	//                       once at bind time before any condition was
	//                       applied. Not a peak, not a median: there is one,
	//                       and it is a SEED rather than what any frame was
	//                       shot at.
	//   wetnessSurfacesSet  surfaces whose instances carry the scalar, over
	//                       surfaces the shared file asked for. MEMBERSHIP
	//                       and not a value: the bind sets it on the pack
	//                       and tint routes and the re-drive rewrites the
	//                       same set on every walk, so it is last-wins in
	//                       form and cannot move in value. A run in which it
	//                       moves is a run in which the walk reached a
	//                       surface the bind did not, and that is the finding.
	//   wetnessSurfacesWet  of those, how many are in WetSurfaces. Membership
	//                       again: bWet is IsGroundSurface and is true at
	//                       wetness 0.0 too, so this reads 4 after wet_000
	//                       and after wet_100 alike and never says what value
	//                       the four hold. wetnessNow and the shot lines do.
	//   wetnessSurfacesDarkened  of those, how many bound an albedo and so
	//                       took the colour half as well as the roughness
	//                       half. Membership, off bAlbedoBound recorded at
	//                       the bind and handed to the walk unchanged.
	//   wetnessShotsAtValue shots whose condition carries the SEED value,
	//                       over shots offered. Until 309 the gap was the
	//                       size of the static bind's compromise; it is not
	//                       that any more, because ApplyCondition re-drives
	//                       the value per condition and every shot is now
	//                       photographed at its own. The gap is NOT how many
	//                       shots skipped a walk: the guard is keyed on the
	//                       LAST applied value, so a seed-value shot after a
	//                       night row walks. On the committed file 35 shots
	//                       carry the seed and 26 skip. wetnessRedriveWalks
	//                       is the reading that matters.
	inline std::string WetnessDoneSegment(const std::vector<Bound>& All,
	                                      const WetnessChoice& Choice)
	{
		int Set = 0, Wet = 0, Albedo = 0;
		for (size_t I = 0; I < All.size(); ++I)
		{
			if (!All[I].bWetSet) { continue; }
			++Set;
			if (All[I].Wet.bWet)    { ++Wet; }
			if (All[I].Wet.bAlbedo) { ++Albedo; }
		}
		char Buf[700];
		std::snprintf(Buf, sizeof(Buf),
			" wetnessBindValue=%.4f wetnessBindFrom=%s/%s"
			" wetnessSurfacesSet=%d/%d wetnessSurfacesWet=%d/%d"
			" wetnessSurfacesDarkened=%d/%d"
			" wetnessShotsAtValue=%d/%d wetnessCondsAtValue=%d/%d"
			" wetnessParam=%s wetnessDryIs=%.4f"
			" wetnessModel=per-condition-since-queue-309/ApplyCondition-re-drives-"
			"the-instances-the-scene-already-keeps/write-on-change-keyed-on-the-"
			"last-applied-wetness"
			" wetnessStat=bindValue-is-one-seed-per-run-not-a-peak-or-a-median/"
			"surfacesSet-over-surfaces-the-file-asked-for/"
			"shotsAtValue-over-shots-offered-and-since-309-that-gap-is-NOT-a-"
			"compromise-shots-at-the-seed-value-not-shots-that-skipped-a-walk",
			Choice.Value,
			LedgerVignette::NoSpaces(Choice.FromCondition).c_str(), Choice.Why,
			Set, (int)All.size(), Wet, Set, Albedo, Set,
			Choice.ShotsAtValue, Choice.ShotsExamined,
			Choice.CondsAtValue, Choice.CondsExamined,
			WetnessParam(), WetnessDry());
		std::string Out(Buf);
		if (Set == 0)
		{
			Out += " wetnessNote=no-surface-reached-an-instance/nothing-was-set-"
			       "so-no-frame-can-be-read-against-this-value";
		}
		else if (Choice.Value <= 0.0)
		{
			// THE ZERO THAT IS A READING, NAMED. A seed of zero means every
			// instance was MADE dry, and that is a PASS and not a failure to
			// apply anything: the words are here so a reader never has to tell
			// the two apart by the absence of a key. IT NO LONGER SAYS
			// ANYTHING ABOUT A FRAME, queue 309: the seed is what the street
			// wore before the first condition, and what each frame was shot at
			// is shotWetness on that frame's own line.
			Out += " wetnessNote=the-SEED-condition-is-DRY-at-0.0000/every-"
			       "instance-was-made-dry/says-nothing-about-any-frame-since-"
			       "queue-309/see-shotWetness-per-shot-and-wetnessNow-for-last-wins";
		}
		return Out;
	}

	// THE WETNESS HALF OF ONE SURFACE'S LINE, APPENDED RATHER THAN FORMATTED
	// INTO SurfaceLine's CAPPED BUFFER. That buffer was measured at 426 of
	// 560 characters and a snprintf that overruns TRUNCATES SILENTLY, which
	// reads as a short line rather than as a cut one. The tint block already
	// carries the reason; this follows texRootTried's habit instead.
	//
	// WHAT EACH NUMBER IS A STATISTIC OF, per surface and never per run:
	//   wetSet         the value handed to this surface's Wetness parameter,
	//                  LAST-WINS over the conditions the run applied. It was
	//                  one value for the whole run until queue 309; since
	//                  ApplyCondition re-drives it, a bare number would not
	//                  say which frame it describes, so wetSetFrom names the
	//                  condition it belongs to and wetSetStat says last-wins
	//                  out loud. The per-frame answer is shotWetness, on that
	//                  frame's own line and under its own name.
	//   wetSetFrom     the condition whose wetness this surface is wearing.
	//   wetApplied     which halves reached it: both, roughness only, or
	//                  neither, with the reason in the value.
	//   wetAlbedoScale the gamma multiplier folded into AlbedoGrade. 1.0000
	//                  means the colour did not move.
	//   wetRoughAt     THE DIRECTION, READABLE FROM THE NUMBERS ALONE. The
	//                  dry and wet roughness of ONE NAMED DATUM: this
	//                  surface's dry smoothness in AssetLibrary.SurfaceSpec,
	//                  flipped to roughness. IT IS NOT THE PACK TEXEL. The
	//                  material's roughness is a 2048x2048 file lerped per
	//                  texel and no single byte of it is known in this
	//                  process, so the datum is named in the value and a
	//                  reader can never take one for the other.
	// THE TAIL IS CONCATENATED AND NOT FORMATTED, so it has no cap to
	// announce and cannot push the Buf[420] below over: the two keys it adds
	// are a spaceless condition id and a fixed sentence, neither of which
	// needs a number formatted.
	inline std::string WetFromFields(const Bound& B)
	{
		return " wetSetFrom=" + LedgerVignette::NoSpaces(B.WetFrom)
		     + " wetSetStat=per-surface/LAST-WINS-over-the-conditions-this-run-"
		       "applied/re-driven-per-condition-since-queue-309/"
		       "not-a-mean-and-not-the-bind-time-seed";
	}

	inline std::string WetFields(const Bound& B)
	{
		if (!B.bWetSet)
		{
			return " wetSet=not-set wetApplied=not-set wetAlbedoScale=not-set"
			       " wetRoughAt=not-set" + WetFromFields(B);
		}
		const double DrySmooth = GroundDrySmoothness(B.Surface);
		char Buf[420];
		const char* Applied = B.Wet.bAlbedo ? "roughness-and-albedo"
		                    : (B.Wet.bWet ? "roughness-only" : "none");
		if (DrySmooth < 0.0)
		{
			std::snprintf(Buf, sizeof(Buf),
				" wetSet=%.4f wetApplied=%s/%s wetAlbedoScale=%.4f"
				" wetRoughAt=no-datum/%s-is-not-in-AssetLibrary-WetSurfaces-so-"
				"no-dry-smoothness-is-quoted-for-it",
				B.Wet.Wetness, Applied, B.Wet.Why, B.Wet.AlbedoScale,
				LedgerVignette::NoSpaces(B.Surface).c_str());
			return std::string(Buf) + WetFromFields(B);
		}
		const double DryRough = RoughnessFromSmoothness(DrySmooth);
		std::snprintf(Buf, sizeof(Buf),
			" wetSet=%.4f wetApplied=%s/%s wetAlbedoScale=%.4f"
			" wetRoughAt=dry.%.4f..wet.%.4f/datum.unity-surfacespec-smoothness."
			"%.2f/NOT-the-pack-roughness-texel"
			" wetRoughFloor=%.4f",
			B.Wet.Wetness, Applied, B.Wet.Why, B.Wet.AlbedoScale,
			DryRough, WetRoughness(DryRough, B.Wet.Wetness), DrySmooth,
			WetRoughnessFloor());
		return std::string(Buf) + WetFromFields(B);
	}

	// ONE LINE PER SURFACE. Per-surface numbers only; the run's totals are on
	// the done line below, so no key means two different things on two lines.
	//
	// A SURFACE THAT RESOLVED PRINTS WHAT EACH MAP LOADED AS, not what its
	// filename claims. An `.hdr` that imports as a 2D texture and a `.jpg`
	// that decodes at half size are both invisible to a name.
	inline std::string SurfaceLine(const Bound& B)
	{
		char Head[420];
		std::snprintf(Head, sizeof(Head),
			"surface %s surfaceStatus=%s pieces=%d piecesAssigned=%d/%d",
			LedgerVignette::NoSpaces(B.Surface).c_str(),
			LedgerVignette::NoSpaces(B.Status).c_str(),
			B.Pieces, B.PiecesAssigned, B.Pieces);
		std::string Out(Head);
		// WHICH OF THE THREE KINDS OF SURFACE THIS IS, ASKED ONCE. A decal
		// blend has no library file by design and a candidate list beside it
		// is a lie with three filenames in it; a procedural surface's albedo
		// is a texel this run computed, and naming the file it did not look
		// for says nothing.
		const bool bBlend = IsDecalBlend(B.Surface);
		const bool bProcedural = (ProceduralSurfaceIndex(B.Surface) >= 0);
		for (int M = 0; M < MapCount(); ++M)
		{
			char Buf[420];
			if (B.MapFound[M])
			{
				std::snprintf(Buf, sizeof(Buf),
					" %sFile=%s %sLoadedAs=%dx%d/%s %sParam=%s",
					MapName(M), LedgerVignette::NoSpaces(B.MapFile[M]).c_str(),
					MapName(M), B.MapW[M], B.MapH[M],
					B.MapLoadedAs[M].empty() ? "unknown"
					                         : LedgerVignette::NoSpaces(B.MapLoadedAs[M]).c_str(),
					MapName(M), MapParam(M));
			}
			else if (B.MapBorrowed[M])
			{
				// THE BORROW IS NAMED WITH THE SURFACE IT CAME FROM, because
				// a normal map on the interior that nobody can attribute is
				// indistinguishable from the interior having its own.
				std::snprintf(Buf, sizeof(Buf),
					" %sFile=%s %sLoadedAs=%dx%d/%s %sParam=%s %sBorrowedFrom=%s",
					MapName(M), LedgerVignette::NoSpaces(B.MapFile[M]).c_str(),
					MapName(M), B.MapW[M], B.MapH[M],
					B.MapLoadedAs[M].empty() ? "unknown"
					                         : LedgerVignette::NoSpaces(B.MapLoadedAs[M]).c_str(),
					MapName(M), MapParam(M), MapName(M),
					LedgerVignette::NoSpaces(B.BorrowedFrom).c_str());
			}
			else if (bBlend)
			{
				std::snprintf(Buf, sizeof(Buf),
					" %sFile=NOT-A-LIBRARY-SURFACE %sTried=nothing/%s-is-a-decal-blend-mode-"
					"and-the-picture-comes-from-the-piece-own-asset-field",
					MapName(M), MapName(M), LedgerVignette::NoSpaces(B.Surface).c_str());
			}
			else if (bProcedural && M == 0)
			{
				std::snprintf(Buf, sizeof(Buf),
					" %sFile=BUILT-IN-CODE %sTried=nothing/this-surface-is-ProceduralOnly-"
					"or-has-no-pack-file-and-the-unity-host-generates-it-from-the-tint",
					MapName(M), MapName(M));
			}
			else
			{
				std::snprintf(Buf, sizeof(Buf),
					" %sFile=ABSENT %sTried=%s",
					MapName(M), MapName(M), CandidateList(B.Surface, M).c_str());
			}
			Out += Buf;
		}
		// THE ROUTE AND THE TEXEL, ON THE LINE THAT NAMES THE SURFACE THEY
		// BELONG TO. A tint nobody can read off the verdict is a number only
		// the source says, and the source is not evidence.
		//
		// THREE BRANCHES AND NO NEW KEY, QUEUE 299. Until this change a
		// pack surface printed tintTexel, tintFrom, tintPattern and
		// roughnessTexel all as not-built: four dead fields on twelve of
		// the sixteen lines, because the only thing that filled them was
		// the procedural tint. A graded pack surface has a real colour to
		// report, so it reports it THROUGH THOSE FOUR and adds nothing.
		// The standing rule is Jafar's: no new instrument this month
		// unless one is retired in the same batch, and none is.
		//
		// tintTexel MEANS ONE THING AND THE VALUE SAYS WHICH. On a
		// procedural line it is the albedo byte of the one flat texel this
		// run built. On a pack line there are 2048x2048 texels and no
		// single byte, so the number is the grade ON A WHITE REFERENCE
		// TEXEL, in the same units, and the value carries the word
		// grade-on-white so a grep can never take one for the other. That
		// is this file's rule about one key meaning two things, satisfied
		// in the value because the key may not move.
		//
		// NOT-BUILT STILL MEANS NOTHING HAPPENED. A surface the material
		// pass never reached prints the words, exactly as before, because
		// "no grade was set" and "the grade is white" are different
		// findings with different next actions.
		//
		// THE BUFFER IS MEASURED AND NOT GUESSED. The longest string this
		// block can produce is 426 characters, taken by sweeping every
		// surface name against both values of bTextured and measuring the
		// result; 420 left 22 characters of headroom and a surfaceRoute
		// longer than decal-multiply would have eaten it. A silently
		// truncated verdict line is the quietest instrument fault there is.
		//
		// RE-MEASURED 2026-09-15 AND IT MOVED, 398 to 426, because the
		// walk-back term added `/jafarWalkBack.0.85..ruled.2026-09-15` to
		// tintFrom on both branches. THE NUMBER WAS RE-SWEPT RATHER THAN
		// ADJUSTED BY ARITHMETIC: every surface name against every route,
		// both values of bTextured and both of bTintBuilt/bGradeSet. The
		// longest is still the white-grade pack branch, whose Why string is
		// longer than either graded one. 560 leaves 134 characters.
		{
			char Buf[560];
			if (B.bTintBuilt)
			{
				double Tr = 0.0, Tg = 0.0, Tb = 0.0, Gr = 0.0, Gg = 0.0, Gb = 0.0;
				const int ProcIdx = ProceduralSurfaceIndex(B.Surface);
				if (ProcIdx >= 0) { ProceduralSurfaceTint(ProcIdx, Tr, Tg, Tb); }
				TextureGrade(Gr, Gg, Gb);
				// THE WALK-BACK IS NAMED HERE OR THE TEXEL CANNOT BE
				// RECOMPUTED FROM THE INPUTS BESIDE IT. This branch prints
				// the legacy terms as the inputs and the texel as the
				// result, and since 2026-09-15 a third term sits between
				// them. Leaving it out would not be a missing detail, it
				// would make the line's own arithmetic fail to close.
				// NO NEW KEY: it goes inside tintFrom's value, which is
				// already a `/`-separated structure.
				std::snprintf(Buf, sizeof(Buf),
					" surfaceRoute=%s tintTexel=%d.%d.%d tintFrom=spec.%.2f.%.2f.%.2f"
					"/grade.%.2f.%.2f.%.2f%s/jafarWalkBack.%.2f..ruled.%s"
					"/AlbedoGradeParam.white-because-the-"
					"product-is-already-in-this-texel tintPattern=flat-here/%s"
					" roughnessTexel=%d",
					B.Route.empty() ? "none" : LedgerVignette::NoSpaces(B.Route).c_str(),
					B.Tint.R, B.Tint.G, B.Tint.B, Tr, Tg, Tb, Gr, Gg, Gb,
					IsGroundSurface(B.Surface) ? "/groundGrade.0.55" : "",
					JafarGradeStrength(), JafarGradeStrengthWhen(),
					B.Surface == "interior" ? "unity-adds-a-0.10-noise-over-it"
					                        : "unity-is-flat-too",
					ProceduralRoughnessTexel(B.Surface));
			}
			else if (B.bGradeSet)
			{
				// A PACK SURFACE, AND EVERY NUMBER HERE IS ONE THE BIND SITE
				// ACTUALLY HANDED THE ENGINE, carried on B.Graded rather than
				// recomputed from the surface name. tintFrom ends with the
				// LINEAR triple, which is the thing the parameter really
				// holds, so a reader comparing the verdict against a material
				// instance dump is comparing like with like.
				const Texel GT = GradeTexel(B.Graded);
				std::snprintf(Buf, sizeof(Buf),
					" surfaceRoute=%s tintTexel=grade-on-white.%d.%d.%d"
					" tintFrom=%s/grade.%.2f.%.2f.%.2f%s/jafarWalkBack.%.2f..ruled.%s"
					"/linear.%.4f.%.4f.%.4f"
					" tintPattern=pack-jpeg-times-AlbedoGradeParam/%s"
					" roughnessTexel=%s",
					B.Route.empty() ? "none" : LedgerVignette::NoSpaces(B.Route).c_str(),
					GT.R, GT.G, GT.B,
					B.Graded.Why,
					B.Graded.GammaR, B.Graded.GammaG, B.Graded.GammaB,
					B.Graded.bGround ? "/groundGrade.0.55" : "/groundGrade.not-a-ground-surface",
					// THE STRENGTH AND ITS DATE, SO NO FRAME IS READ AGAINST
					// THIS GRADE WITHOUT THE READER LEARNING IT IS PROVISIONAL.
					// grade.* is now the walked-back gamma triple, which is
					// what the parameter was built from; the two legacy terms
					// are the words in tintFrom's first field.
					JafarGradeStrength(), JafarGradeStrengthWhen(),
					B.Graded.R, B.Graded.G, B.Graded.B,
					B.MapFound[0] ? "the-albedo-is-the-file-and-the-grade-is-a-parameter-on-it"
					              : "no-albedo-file-bound-so-the-grade-sits-on-the-material-default",
					B.MapFound[2] ? "from-the-pack-roughness-file/not-computed-here"
					              : (B.MapBorrowed[2] ? "borrowed-with-the-maps/not-computed-here"
					                                 : "no-roughness-file-and-none-built/material-default"));
			}
			else
			{
				std::snprintf(Buf, sizeof(Buf),
					" surfaceRoute=%s tintTexel=not-built tintFrom=not-built"
					" tintPattern=not-built roughnessTexel=not-built",
					B.Route.empty() ? "none" : LedgerVignette::NoSpaces(B.Route).c_str());
			}
			Out += Buf;
		}
		// THE WETNESS, ON THE LINE THAT NAMES THE SURFACE IT WAS SET ON.
		Out += WetFields(B);
		char Tail[200];
		std::snprintf(Tail, sizeof(Tail),
			" tileUVsample=%.2fx%.2f surfaceReason=%s",
			B.TileU, B.TileV, LedgerVignette::NoSpaces(B.Reason).c_str());
		Out += Tail;
		// WHAT THE INSTANCE ANSWERED, ON THE LINE THAT NAMES THE SURFACE IT
		// WAS ASKED ABOUT. A readback with no surface name beside it cannot
		// say which texture was in the question.
		Out += ReadbackFields(B.Read);
		return Out;
	}

	// ---- WHAT THE SURFACE NUMBERS ARE OVER, QUEUE 227 -------------------
	//
	// THE KEYS ABOVE KEEP THEIR NAMES AND CHANGE THEIR DENOMINATOR, so this
	// segment exists to say so on the same line rather than leaving a reader
	// to diff two runs and guess. surfacesAsked went 16 to 14 and
	// surfacesAbsent went card/interior/multiply/paint_yellow to none, and
	// NEITHER MOVEMENT IS A REPAIR: nothing about the pack changed. Two of
	// the four were never surfaces and two of the four are painted from the
	// spec tint by design, which the per-surface lines have printed as
	// DECAL-BLEND and PROCEDURAL since queue 223 landed while this line was
	// still calling all four absent.
	//
	// WHAT EACH NUMBER IS A STATISTIC OF: all of them are counts over
	// DISTINCT SURFACE NAMES in the shared piece file, one row per name, not
	// per piece. The per-piece counts are piecesPainted and piecesUnpainted
	// and they live on the paint-route segment.
	//
	// A RUN THAT ASKED FOR NO LIBRARY SURFACE PRINTS THE WORDS, because
	// `0/0 accounted for` reads exactly like a clean pass.
	inline std::string SurfacePopulationSegment(int Resolved, int Procedural,
	                                            int AbsentN, int Asked,
	                                            int Blends,
	                                            const std::string& BlendNames,
	                                            const std::string& ProcNames,
	                                            int MapsBorrowed)
	{
		// THE BUFFER IS A CAP WITH A PRINTED SERIES: run 56 predicted 1147
		// chars, worst plausible 1173 (two more procedural names), so 1200
		// leaves 53 and 27. Whoever adds a key here or lengthens a name list
		// reprints those two numbers beside the change and raises this in the
		// same edit when the margin is smaller than what they add. A third
		// procedural surface in the live spec prints surfacePopulationCut on
		// the done line rather than truncating in silence. Ruled 2026-09-21.
		char Buf[1200];
		const int Needed = Asked <= 0
			? std::snprintf(Buf, sizeof(Buf),
				" surfacesAccountedFor=nothing-measured"
				" surfacesProcedural=nothing-measured"
				" surfacesProceduralNames=none surfacesAbsentCount=nothing-measured"
				" decalBlendsAsked=%d decalBlendNames=%s mapsBorrowed=%d"
				" surfacePopulationNote=no-library-surface-was-asked-for/only-blend-modes-or-nothing-at-all"
				" surfacePopulationStat=counts-over-distinct-surface-names/not-over-pieces",
				Blends, BlendNames.empty() ? "none" : BlendNames.c_str(), MapsBorrowed)
			: std::snprintf(Buf, sizeof(Buf),
				" surfacesAccountedFor=%d/%d surfacesProcedural=%d/%d"
				" surfacesProceduralNames=%s surfacesAbsentCount=%d/%d"
				" decalBlendsAsked=%d decalBlendNames=%s mapsBorrowed=%d"
				" surfacePopulationStat=counts-over-distinct-surface-names/not-over-pieces"
				" surfacesAskedOf=library-surfaces-only/blend-modes-are-counted-on-decalBlendsAsked"
				" mapsAskedOf=3-per-library-surface-whose-albedo-is-expected-from-the-pack"
				"/a-procedural-surface-asks-the-pack-for-no-albedo-so-its-normal-and-roughness-are-outside-this-denominator-and-print-on-its-own-surface-line"
				" materialsStatusMeans=ALL-is-every-library-surface-accounted-for"
				"/resolved-from-the-pack-or-procedural-by-design"
				"/ABSENT-is-no-pack-file-AND-no-spec-entry-and-IS-a-real-fault"
				" surfacePopulationChanged=queue-227/through-run-55-surfacesAsked-counted-16-names-with-2-blend-modes-in-it-and-called-the-2-procedural-surfaces-absent/from-run-56-it-counts-14-library-surfaces/PARTIAL-12-of-16-to-ALL-14-of-14-over-the-SAME-pack-is-a-recount-and-not-a-repair"
				" surfacePopulationRule=queue-227/card-and-multiply-are-decal-blend-modes"
				"/asking-texRoot-for-card.png-asks-for-a-file-that-by-design-can-never-exist",
				Resolved + Procedural, Asked, Procedural, Asked,
				ProcNames.empty() ? "none" : ProcNames.c_str(),
				AbsentN, Asked, Blends,
				BlendNames.empty() ? "none" : BlendNames.c_str(), MapsBorrowed);
		std::string Out(Buf);
		// THE CAP ANNOUNCES WHEN IT BITES, which is this project's rule: a
		// segment cut by snprintf loses its trailing keys and reads exactly
		// like a segment that was never written.
		if (Needed < 0 || (size_t)Needed >= sizeof(Buf))
		{
			Out += " surfacePopulationCut=yes/at-1200-chars";
		}
		return Out;
	}

	// THE WHOLE-RUN LINE FOR THE MATERIAL PASS. Every tally is computed here,
	// from the same vector the per-surface lines were printed from, so a
	// total and its lines cannot disagree.
	//
	// A PASS THAT BOUND NOTHING SAYS THE WORDS. `surfacesResolved=0/14` with
	// a base material that never loaded and `0/14` with fourteen missing files
	// are different findings, and materialBase is what separates them.
	//
	// THE DENOMINATOR IS FOURTEEN AND NOT SIXTEEN, QUEUE 227. It counts the
	// LIBRARY surfaces only; card and multiply are decal blend modes and are
	// counted on decalBlendsAsked. See SurfacePopulationSegment just above for
	// what moved and why none of the movement is a repair.
	// TexRootTried is the candidate directories the engine side actually
	// asked the file system about, in the order it asked. The top layer
	// supplies membership and order; the joining, the cap and the words are
	// here, where they are run by g++ before any dispatch.
	inline std::string MaterialsDoneLine(const std::vector<Bound>& All,
	                                     const std::string& BaseMaterialPath,
	                                     bool bBaseLoaded,
	                                     const std::string& TexRoot,
	                                     int TexRootFiles,
	                                     const std::vector<std::string>& TexRootTried,
	                                     int PiecesInFile,
	                                     int TexturesImported,
	                                     int MidsCreated,
	                                     double MetresPerTile)
	{
		int Resolved = 0, Procedural = 0, AbsentN = 0, Blends = 0;
		int Assigned = 0, PiecesUnderResolved = 0, MapsFound = 0, MapsAsked = 0;
		int MapsBorrowed = 0;
		std::string Absent, ProcNames, BlendNames;
		for (size_t I = 0; I < All.size(); ++I)
		{
			Assigned += All[I].PiecesAssigned;
			// A BLEND MODE ASKS THE PACK FOR NOTHING, so it enters no surface
			// tally and no map tally. It is counted, and named, on its own key.
			if (IsDecalBlend(All[I].Surface))
			{
				++Blends;
				if (!BlendNames.empty()) { BlendNames += "/"; }
				BlendNames += LedgerVignette::NoSpaces(All[I].Surface);
				continue;
			}
			if (IsResolved(All[I]))
			{
				++Resolved;
				PiecesUnderResolved += All[I].Pieces;
				MapsAsked += MapCount();
				for (int M = 0; M < MapCount(); ++M)
				{
					if (All[I].MapFound[M]) { ++MapsFound; }
				}
			}
			else if (IsProceduralSurface(All[I]))
			{
				// NO PACK FILE FOR THE ALBEDO BY DESIGN. Its normal and roughness
				// are tried or borrowed and print on its own line; folding three
				// candidates into MapsAsked for it would put a shortfall in the
				// denominator that nothing is ever going to fill. Borrowed maps
				// are counted apart, for the reason MapBorrowed exists.
				++Procedural;
				if (!ProcNames.empty()) { ProcNames += "/"; }
				ProcNames += LedgerVignette::NoSpaces(All[I].Surface);
				for (int M = 0; M < MapCount(); ++M)
				{
					if (All[I].MapBorrowed[M]) { ++MapsBorrowed; }
				}
			}
			else
			{
				// NO PACK FILE AND NO SPEC ENTRY. This is the only genuine
				// fault of the three and it keeps the key it always had.
				++AbsentN;
				if (!Absent.empty()) { Absent += "/"; }
				Absent += LedgerVignette::NoSpaces(All[I].Surface);
				MapsAsked += MapCount();
				for (int M = 0; M < MapCount(); ++M)
				{
					if (All[I].MapFound[M]) { ++MapsFound; }
				}
			}
		}
		if (Absent.empty()) { Absent = "none"; }
		if (ProcNames.empty()) { ProcNames = "none"; }
		if (BlendNames.empty()) { BlendNames = "none"; }
		const int Asked = Resolved + Procedural + AbsentN;   // library surfaces only
		const int Accounted = Resolved + Procedural;
		char Buf[1100];
		const int Needed = std::snprintf(Buf, sizeof(Buf),
			"materialsStatus=%s materialBase=%s materialBasePath=%s "
			"surfacesAsked=%d surfacesResolved=%d/%d surfacesAbsent=%s "
			"mapsFound=%d/%d texturesImported=%d midsCreated=%d "
			"piecesTextured=%d/%d piecesUnderResolvedSurfaces=%d/%d "
			"texRoot=%s texRootFiles=%d metresPerTile=%.2f "
			"tilingModel=two-largest-dimensions/not-per-face-uvs "
			"materialsStat=counts-over-the-LIBRARY-surfaces-the-shared-file-asked-for",
			Asked == 0 ? "NOTHING-ASKED"
			           : (!bBaseLoaded ? "NO-BASE-MATERIAL"
			                           : (Accounted == Asked ? "ALL"
			                                                 : (Accounted == 0 ? "NONE" : "PARTIAL"))),
			bBaseLoaded ? "loaded" : "MISSING",
			LedgerVignette::NoSpaces(BaseMaterialPath).c_str(),
			Asked, Resolved, Asked, Absent.c_str(),
			MapsFound, MapsAsked, TexturesImported, MidsCreated,
			Assigned, PiecesInFile, PiecesUnderResolved, PiecesInFile,
			TexRoot.empty() ? "NOT-FOUND" : LedgerVignette::NoSpaces(TexRoot).c_str(),
			TexRootFiles, MetresPerTile);
		std::string Line(Buf);
		// SNPRINTF TRUNCATES SILENTLY, and a cut line reads as a short one:
		// the keys past the cut simply are not there, which is exactly what a
		// feature that never ran looks like. The buffer is a cap, so it
		// announces itself when it bites and stays quiet when it does not.
		if (Needed < 0 || (size_t)Needed >= sizeof(Buf))
		{
			Line += " materialsLineCut=yes/at-1100-chars";
		}
		// THE SEARCH PATH GOES ON THE SAME WHOLE-RUN LINE AS ITS RESULT.
		// texRoot says what answered; texRootTried says what was asked, so
		// NOT-FOUND names the directories rather than leaving a reader to
		// read them out of the source of a binary they cannot run. Appended
		// as a string rather than formatted into the buffer above, because
		// four absolute Windows paths are what would push that buffer over.
		Line += " texRootTried=" + PathListValue(TexRootTried, 8);
		// THE RUN'S READBACK TOTALS, COUNTED FROM THE SAME VECTOR THE
		// SURFACE LINES WERE PRINTED FROM. Appended rather than formatted
		// into the buffer above for the reason texRootTried is: the buffer is
		// a cap and a cut line reads as a short one.
		Line += SurfacePopulationSegment(Resolved, Procedural, AbsentN, Asked,
		                                 Blends, BlendNames, ProcNames, MapsBorrowed);
		Line += ReadbackDoneSegment(All);
		return Line;
	}

	// ---- THE CONTROL QUADS, WHICH ARE THE ACCEPTING CASE -----------------
	//
	// WHY A CONTROL AT ALL. Every reading in this pass so far is a rejecting
	// one: the street is grey, the bay that carries brick_red renders cooler
	// than neutral where its albedo is warm. Nothing has ever shown this
	// material path WORKING, so there is no accepting case to compare a
	// failure against, and a diagnosis with no accepting case is a lead.
	//
	// WHY THREE AND NOT ONE. The open question is which of an instance's
	// parameters reaches the shader, and one quad answers only the texture
	// half:
	//
	//   colour  a texture BUILT IN CODE, four saturated colours, no file, no
	//           decode and no dependency on the texture root. Four colours on
	//           it means a texture override reaches the sampler and the fault
	//           is in the imported textures or their resources. A grey
	//           checker on it means no texture override reaches the shader.
	//   tile1   no texture override at all, the base material's own default
	//           texture, tiled once.
	//   tile4   the same, with the tiling scalars at four.
	//
	// tile1 AND tile4 SIDE BY SIDE ARE THE SCALAR HALF, AND THEY ARE THE
	// RENDER SIDE OF IT. The readback above can only see the game thread's
	// copy. Two quads of ONE size at ONE distance showing checkers of
	// DIFFERENT cell counts is a scalar override reaching the render proxy;
	// the same cell count on both is either the scalars not arriving or the
	// base material not rendering at all, and both of those are findings
	// about the material rather than about the texture. This is the reading
	// the withdrawn elimination tried to take from two street pieces of
	// unknown world size.
	//
	// PLACED FROM THE CAMERA'S OWN NUMBERS, never from a hard-coded spot, so
	// a camera moved in the spec file takes its controls with it.
	inline int ControlQuadCount() { return 3; }

	inline const char* ControlQuadId(int I)
	{
		const char* N[3] = {"colour", "tile1", "tile4"};
		return (I >= 0 && I < 3) ? N[I] : "out-of-range";
	}

	// THE TILING EACH QUAD ASKS FOR. colour is at one so its four texels are
	// four quadrants and not a chequer of them; tile1 and tile8 differ ONLY
	// here, which is what makes the pair readable.
	// FOUR AND NOT EIGHT, AND THE REASON IS THE MIP CHAIN. A checker tiled
	// densely enough mips down to flat grey, which is the same thing an
	// untextured surface looks like and is exactly the ambiguity that made
	// the street's own cell counts unreadable. Four repeats across a 0.70 m
	// quad at 3.5 m is about thirty pixels a tile in a 1280x720 frame, which
	// is far too coarse to filter away and still four times the other quad.
	inline double ControlQuadTiling(int I)
	{
		const double T[3] = {1.0, 1.0, 4.0};
		return (I >= 0 && I < 3) ? T[I] : 1.0;
	}

	inline bool ControlQuadBindsTexture(int I) { return I == 0; }

	// WHICH SHOTS MAY SEE THE CONTROLS, AND WHY THE ANSWER IS NOT "ALL OF
	// THEM". The quads are an INSTRUMENT: three swatches standing in the
	// carriageway that prove a material instance can be told from the
	// street around it.
	// They are placed 3.5 m in front of ControlCameraId()'s camera (cam_B
	// since 2026-09-21; the first shot's camera, cam_A, before that) and
	// nothing in that placement knows any other camera exists, so a second
	// camera pointed anywhere near the same stretch of road photographs
	// them. cam_hook, the rung 1 viewpoint, is exactly that case: from cam_A
	// vignette-spec-test measured one quad's left edge at column 1274 of a
	// 1280 wide frame; from cam_B it measures all three centres inside it
	// (about column 530, row 392, 17.5 to 19.4 m ahead). So this rule is the
	// ONLY thing keeping an instrument out of the picture a person is being
	// asked to judge a street by, and queue 339's second half is the pixel
	// proof that it holds.
	//
	// So the rule is one line and it lives here, where the test runs, rather
	// than as a condition buried in the shot loop: the controls are visible
	// ONLY in the frames of the camera they were placed from. Every other
	// shot sees the street. This is the same reasoning that already skips
	// them for an interactive build, generalised from one flag to the
	// camera identity that actually decides it.
	inline bool ControlQuadsVisibleFor(const std::string& ShotCameraId,
	                                   const std::string& ControlCameraId)
	{
		if (ShotCameraId.empty() || ControlCameraId.empty()) { return false; }
		return ShotCameraId == ControlCameraId;
	}

	// AND WHAT THE RUN SAYS IT DID, formatted here for the same reason.
	// WHOLE-RUN NUMBERS: how many shots were taken, how many of them had the
	// controls hidden, and the ids of those shots, so "the swatches were not
	// in that frame" is a reading rather than a belief. A run that took no
	// shot prints the words rather than a clean zero.
	inline std::string ControlQuadVisibilityLine(int Shots, int Hidden,
	                                             const std::string& HiddenIds)
	{
		if (Shots <= 0)
		{
			return std::string("controlQuadVisibility=nothing-measured "
			                   "controlQuadHiddenOn=none controlQuadShots=0 "
			                   "controlQuadVisibilityStat=no-shot-reached-the-loop");
		}
		// 512 AND NOT 160. The first version of this line was truncated by
		// snprintf at 160 bytes and g++ said so; a formatter that silently
		// drops its own stat suffix is the quiet instrument failure this
		// project keeps paying for, so the buffer is sized past the longest
		// string this can produce (about 210 bytes plus the ids).
		char Buf[512];
		std::snprintf(Buf, sizeof(Buf),
		              "controlQuadVisibility=hidden-for-every-shot-whose-camera-is-not-"
		              "the-one-they-were-placed-from controlQuadHidden=%d/%d "
		              "controlQuadHiddenOn=%s controlQuadVisibilityStat=cumulative-over-"
		              "the-shots-this-run-took",
		              Hidden, Shots, HiddenIds.empty() ? "none" : HiddenIds.c_str());
		return std::string(Buf);
	}

	// STATED CONVENTIONS, PRINTED BESIDE THE NUMBERS THEY PRODUCED. None of
	// these is a measured bound. The distance is far enough that a 0.70 m
	// quad is about a sixth of the frame height and near enough that the
	// four colours are unmistakable in a 1280x720 still.
	inline double ControlQuadAheadM()  { return 3.5; }
	inline double ControlQuadSizeM()   { return 0.70; }
	inline double ControlQuadPitchM()  { return 1.00; }  // centre to centre
	inline double ControlQuadFirstM()  { return 0.50; }  // first centre off the axis

	// THE ROW SITS TO THE CAMERA'S LEFT, AND THAT IS A DECISION ABOUT THE
	// EVIDENCE FRAME rather than about the engine. Negative is left, because
	// the camera's right is the file's +z after the yaw.
	//
	// CORRECTED under D43, 2026-09-21, AND THE JUSTIFICATION IS NOT REPLACED
	// WITH A NEW ONE. This read "At cam_A the right of the frame is the
	// shopfront the street is read for and the left is open carriageway, so
	// the controls stand over the carriageway and leave the half a reader is
	// judging the street from alone." That reasoning was cam_A's and the
	// control camera is now LedgerSurface::ControlCameraId(), cam_B.
	// vignette-scene.json's own note for cam_B: it stands on the WEST footway
	// at x=21.0, yaw 90, "looking due east across the street at the east
	// parade". So the old sentence is false on both halves.
	// WHAT IS LEFT OF CAM_B, AND WHETHER THAT HALF IS ONE A READER JUDGES THE
	// STREET FROM, IS NOT RE-DERIVED HERE and must not be guessed: the offset
	// decision stands as made, its old reason is struck, and a new reason is
	// owed by whoever next measures what cam_B's left half carries.
	//
	// DERIVED 2026-09-21 (ruling of that date, section 11.2), FROM PRINTED
	// NUMBERS AND NOT FROM A LOOK AT cam_B. The offset is two decisions and
	// they have different reasons now.
	//   THE SPACING (0.50 m first centre off the axis, 1.00 m pitch) is not
	//   arbitrary. Run 55's quad lines print the three boxes at x130..261,
	//   x309..437 and x488..614 on rows 298..422: 126 to 131 px wide, 177 to
	//   178 px centre to centre, 48 and 51 px of street between them,
	//   quadCornersInFrame=4/4 on all three at quadDistM=3.51. The row is
	//   centred on the view axis (ControlQuadPlace below) and cam_B's
	//   vertical field is the same 60 degrees as cam_A's, so those boxes are
	//   cam_B's boxes too. Three separate boxes, none overlapping, all
	//   inside the frame at one distance, is what the readback (queue 339)
	//   needs, and it is the whole of the spacing's reason.
	//   THE SIDE (the sign, left) was cam_A's composition reason and has no
	//   reader to serve on cam_B, where no reading is judged. It is kept
	//   because moving it moves every printed box for no measured gain. The
	//   boxes sit on rows 298..422, outside the skyTop band (rows 0..90) and
	//   the ground band (rows 576..720), so cam_B's band statistics carry no
	//   quad either way; its whole-frame keys do, and the shot line says so.
	//   If the control camera ever becomes one a reading is judged from, the
	//   side needs a measured reason again, and that is the day to re-derive
	//   it. Nothing about what cam_B's left half carries is asserted here.
	inline double ControlQuadOffsetM(int I)
	{
		return -(ControlQuadFirstM() + ControlQuadPitchM() * (double)I);
	}

	// WHERE ONE QUAD GOES, IN BOTH FRAMES AT ONCE. The metres are the file's
	// frame and are what the projection below reads; the centimetres are the
	// engine's and are what the emitter spawns at. The conversion happens
	// HERE so the top layer, which no test in this container can run, never
	// does arithmetic.
	//
	// THE ROTATION IS THE ENGINE'S AND IS DERIVED, NOT GUESSED. A pitch of
	// +90 takes the plane's local +Z, which is its normal, onto world -X, and
	// the yaw then turns that onto the reverse of the camera's own forward,
	// so the quad faces the camera at any yaw. Under the same pair the
	// plane's local X lands on world up and its local Y on the camera's
	// right, which is the frame the corners below are taken in.
	struct QuadPlace
	{
		std::string Id;
		double XM = 0.0, YM = 0.0, ZM = 0.0;        // file frame, metres
		double XCm = 0.0, YCm = 0.0, ZCm = 0.0;     // engine frame, centimetres
		double EnginePitchDeg = 90.0, EngineYawDeg = 0.0, EngineRollDeg = 0.0;
		double SizeM = 0.0, TileU = 1.0, TileV = 1.0;
		bool   bBindTexture = false;
	};

	inline double DegToRad(double D) { return D * 3.14159265358979323846 / 180.0; }

	// WHICH CAMERA THE CONTROLS STAND IN FRONT OF, AND IT IS SPELLED ONCE.
	// Ruled 2026-09-21: not the figure's camera (cam_A, the night frame he
	// judges by) and not the sheet's camera (cam_hook, 45 of the 49 shots);
	// cam_B is the one camera in the committed spec that is neither. Through
	// run 55 the rule was "the first shot's camera", which stood a four-colour
	// card across the figure's torso in ue-vign_camA_night.png (queue 313).
	// VignetteShot.cpp and the g++ suite both read the id from here, and the
	// engine prints which camera answered on every quad line as quadOn.
	inline const char* ControlCameraId() { return "cam_B"; }

	inline QuadPlace ControlQuadPlace(const LedgerVignette::Camera& C, int I)
	{
		QuadPlace Q;
		Q.Id = ControlQuadId(I);
		Q.SizeM = ControlQuadSizeM();
		Q.TileU = ControlQuadTiling(I);
		Q.TileV = ControlQuadTiling(I);
		Q.bBindTexture = ControlQuadBindsTexture(I);
		const double Yaw = DegToRad(C.YawDeg);
		// THE CAMERA'S OWN AXES IN THE FILE'S FRAME. Engine yaw turns about
		// up, so forward is (cos,0,sin) and right is (-sin,0,cos) in the
		// file's (x, y, z) with y up.
		const double Fx = std::cos(Yaw), Fz = std::sin(Yaw);
		const double Rx = -std::sin(Yaw), Rz = std::cos(Yaw);
		const double Ahead = ControlQuadAheadM();
		const double Off = ControlQuadOffsetM(I);
		Q.XM = C.X + Fx * Ahead + Rx * Off;
		Q.ZM = C.Z + Fz * Ahead + Rz * Off;
		// CENTRED ON THE VIEW AXIS RATHER THAN AT A FIXED HEIGHT. The file's
		// camera pitch is positive DOWN, so the axis has fallen by
		// Ahead*tan(pitch) at the row's distance and a quad at eye height
		// would sit above the middle of the frame.
		Q.YM = C.GroundY + C.EyeHeightM - Ahead * std::tan(DegToRad(C.PitchDeg));
		Q.XCm = Q.XM * 100.0;
		Q.YCm = Q.ZM * 100.0;   // the file's z is the engine's Y
		Q.ZCm = Q.YM * 100.0;   // the file's y is the engine's Z
		Q.EnginePitchDeg = 90.0;
		Q.EngineYawDeg = C.YawDeg;
		Q.EngineRollDeg = 0.0;
		return Q;
	}

	// ---- WHERE IT LANDS ON THE FRAME -------------------------------------
	//
	// A PINHOLE PROJECTION AND NOTHING MORE, and it is named as a model
	// rather than a reading: it is the same camera the spec file describes,
	// with no lens, no aspect constraint beyond the fov conversion the
	// emitter already uses, and no engine in the loop. It says where the quad
	// SHOULD land so a reader can find it in the still; the still is what
	// says what colour it is.
	struct ScreenAt
	{
		double Px = 0.0, Py = 0.0;
		double ForwardM = 0.0;
		bool   bAhead = false;
	};

	inline ScreenAt ProjectFilePoint(const LedgerVignette::Camera& C,
	                                 double XM, double YM, double ZM, int W, int H)
	{
		ScreenAt S;
		const double Yaw = DegToRad(C.YawDeg);
		// THE ENGINE'S PITCH IS POSITIVE UP AND THE FILE'S IS POSITIVE DOWN,
		// which is the same negation PlaceCamera does before it hands the
		// rotation to the engine.
		const double Pitch = DegToRad(-C.PitchDeg);
		const double Ex = C.X, Ey = C.GroundY + C.EyeHeightM, Ez = C.Z;
		const double Dx = XM - Ex, Dy = YM - Ey, Dz = ZM - Ez;
		const double Fx = std::cos(Pitch) * std::cos(Yaw);
		const double Fz = std::cos(Pitch) * std::sin(Yaw);
		const double Fy = std::sin(Pitch);
		const double Rx = -std::sin(Yaw), Rz = std::cos(Yaw), Ry = 0.0;
		const double Ux = -std::sin(Pitch) * std::cos(Yaw);
		const double Uz = -std::sin(Pitch) * std::sin(Yaw);
		const double Uy = std::cos(Pitch);
		const double Fwd = Dx * Fx + Dy * Fy + Dz * Fz;
		const double Rgt = Dx * Rx + Dy * Ry + Dz * Rz;
		const double Upd = Dx * Ux + Dy * Uy + Dz * Uz;
		S.ForwardM = Fwd;
		S.bAhead = (Fwd > 0.001);
		if (!S.bAhead) { return S; }
		const double TanH = std::tan(DegToRad(
			LedgerVignette::HorizontalFovDeg(C.FovVerticalDeg, W, H) * 0.5));
		const double TanV = std::tan(DegToRad(C.FovVerticalDeg * 0.5));
		S.Px = (double)W * (0.5 + 0.5 * (Rgt / Fwd) / TanH);
		S.Py = (double)H * (0.5 - 0.5 * (Upd / Fwd) / TanV);
		return S;
	}

	// THE BOX IS THE BOUNDING BOX OF FOUR PROJECTED CORNERS, not a width
	// scaled off the centre: the quad is flat and off-axis, so its projection
	// is a quadrilateral and a symmetric box round the centre would be a
	// drawing rather than a measurement. cornersAhead ships beside it,
	// because a box computed from two corners in front and two behind is not
	// a box.
	struct ScreenBox
	{
		bool   bMeasured = false;
		double CxPx = 0.0, CyPx = 0.0;
		double X0 = 0.0, X1 = 0.0, Y0 = 0.0, Y1 = 0.0;
		double DistM = 0.0;
		int    CornersAhead = 0;
		int    CornersInFrame = 0;
	};

	inline ScreenBox ControlQuadBox(const LedgerVignette::Camera& C,
	                                const QuadPlace& Q, int W, int H)
	{
		ScreenBox B;
		const double Yaw = DegToRad(C.YawDeg);
		const double Rx = -std::sin(Yaw), Rz = std::cos(Yaw);
		const double Half = Q.SizeM * 0.5;
		const ScreenAt Mid = ProjectFilePoint(C, Q.XM, Q.YM, Q.ZM, W, H);
		B.DistM = Mid.ForwardM;
		B.CxPx = Mid.Px;
		B.CyPx = Mid.Py;
		if (!Mid.bAhead) { return B; }
		for (int S = 0; S < 4; ++S)
		{
			const double SideSign = (S == 0 || S == 1) ? 1.0 : -1.0;
			const double UpSign   = (S == 0 || S == 2) ? 1.0 : -1.0;
			const ScreenAt P = ProjectFilePoint(
				C, Q.XM + Rx * Half * SideSign,
				Q.YM + Half * UpSign,
				Q.ZM + Rz * Half * SideSign, W, H);
			if (!P.bAhead) { continue; }
			if (B.CornersAhead == 0)
			{
				B.X0 = B.X1 = P.Px;
				B.Y0 = B.Y1 = P.Py;
			}
			else
			{
				if (P.Px < B.X0) { B.X0 = P.Px; }
				if (P.Px > B.X1) { B.X1 = P.Px; }
				if (P.Py < B.Y0) { B.Y0 = P.Py; }
				if (P.Py > B.Y1) { B.Y1 = P.Py; }
			}
			++B.CornersAhead;
			if (P.Px >= 0.0 && P.Px <= (double)W && P.Py >= 0.0 && P.Py <= (double)H)
			{
				++B.CornersInFrame;
			}
		}
		B.bMeasured = (B.CornersAhead == 4);
		return B;
	}

	// ---- QUEUE 333: WHERE A PIECE'S WHOLE SOLID LANDS ON THE FRAME -------
	//
	// THE SAME PINHOLE OVER EIGHT CORNERS INSTEAD OF FOUR. ControlQuadBox
	// above takes a flat quad. A lamp head is a box with depth, and four
	// corners of one face of it under-report its footprint on the picture by
	// however much the box is turned away from the camera. This is that
	// function with the corner walk widened, in the same header, exercised by
	// the same binary.
	//
	// THE ROTATION ORDER IS THE FILE'S OWN AND IS NOT RE-DECIDED HERE: pitch
	// about +x, then yaw about +y taking +x toward +z, then roll about +z.
	// That is the composition LedgerVignette::SpecBoxBounds walks
	// (VignetteSpec.h 1034), whose comment says in as many words that the day
	// a piece carries two rotations at once this order must not be quietly
	// picked a second time. Copied rather than invented, so the two cannot
	// disagree about where a turned piece is.
	//
	// WHAT IT IS AND IS NOT. A model of where the solid SHOULD land, from the
	// spec file and the camera the spec file describes, with no engine in the
	// loop. It says WHERE TO LOOK in the still and says nothing at all about
	// what colour is there: the pixels are read in FrameStats.h, where a test
	// can build a frame.
	//
	// bMeasured IS EIGHT CORNERS AHEAD, not four and not some. A box with a
	// corner behind the eye projects to something that is not a box, and a
	// half-answer must not read as a measurement. IT DIFFERS FROM
	// ControlQuadBox IN ONE WAY ON PURPOSE: the quad version returns early
	// when its centre is behind the camera, and this one walks all eight
	// corners anyway, because CornersAhead is then a NUMBER a caller can read
	// (0 is behind the camera, 1 to 7 is straddling the eye plane) instead of
	// a silence.
	inline ScreenBox PieceScreenBox(const LedgerVignette::Camera& C,
	                                const LedgerVignette::Piece& P, int W, int H)
	{
		ScreenBox B;
		const ScreenAt Mid = ProjectFilePoint(C, P.X, P.Y, P.Z, W, H);
		B.DistM = Mid.ForwardM;
		B.CxPx  = Mid.Px;
		B.CyPx  = Mid.Py;
		const double HX = P.SX * 0.5, HY = P.SY * 0.5, HZ = P.SZ * 0.5;
		const double CP = std::cos(DegToRad(P.PitchDeg));
		const double SP = std::sin(DegToRad(P.PitchDeg));
		const double CYw = std::cos(DegToRad(P.YawDeg));
		const double SYw = std::sin(DegToRad(P.YawDeg));
		const double CR = std::cos(DegToRad(P.RollDeg));
		const double SR = std::sin(DegToRad(P.RollDeg));
		for (int I = 0; I < 8; ++I)
		{
			double X = (I & 1) ? HX : -HX;
			double Y = (I & 2) ? HY : -HY;
			double Z = (I & 4) ? HZ : -HZ;
			double T;
			T = Y * CP - Z * SP;    Z = Y * SP + Z * CP;    Y = T;   // pitch about +x
			T = X * CYw - Z * SYw;  Z = X * SYw + Z * CYw;  X = T;   // yaw about +y
			T = X * CR - Y * SR;    Y = X * SR + Y * CR;    X = T;   // roll about +z
			const ScreenAt S = ProjectFilePoint(C, P.X + X, P.Y + Y, P.Z + Z, W, H);
			if (!S.bAhead) { continue; }
			if (B.CornersAhead == 0)
			{
				B.X0 = B.X1 = S.Px;
				B.Y0 = B.Y1 = S.Py;
			}
			else
			{
				if (S.Px < B.X0) { B.X0 = S.Px; }
				if (S.Px > B.X1) { B.X1 = S.Px; }
				if (S.Py < B.Y0) { B.Y0 = S.Py; }
				if (S.Py > B.Y1) { B.Y1 = S.Py; }
			}
			++B.CornersAhead;
			if (S.Px >= 0.0 && S.Px <= (double)W && S.Py >= 0.0 && S.Py <= (double)H)
			{
				++B.CornersInFrame;
			}
		}
		B.bMeasured = (B.CornersAhead == 8);
		return B;
	}

	// ---- DOES THIS SHOT'S OWN WHOLE-FRAME NUMBERS INCLUDE THE INSTRUMENT --
	//
	// A1(d), amendment 1 of
	// game-design/decision-2026-09-09-ruling-the-grid-batch-review.md, and it
	// is a DECLARATION ON THE SAMPLE LINE rather than a coverage measurement.
	// The distinction is the whole point. shotMeanLuma, the exposure bands and
	// band.ground are means over every pixel of the frame, so on the camera
	// the control quads were placed from they include three saturated swatches
	// standing in the carriageway, and the reader of a grid cell has no way to
	// tell from the line which frames carry them. The earlier ruling dictated
	// this as a literal string with pixel boxes and a percentage measured once
	// for one camera at one field of view; the review narrowed it, because a
	// measurement frozen as a literal inside an emit is a number nobody can
	// re-measure. So the boxes are PROJECTED HERE, by ControlQuadPlace and
	// ProjectFilePoint, the same two functions the tests exercise, from
	// whatever camera the file carries.
	//
	// WHAT THE PERCENTAGE IS AND IS NOT. It is the union of the three
	// projected boxes, clipped to the frame, over the frame area: an AT-MOST
	// bound on how much of the picture the swatches can own, and it overstates
	// that coverage because a bounding box is not a quad and three boxes that
	// overlap are counted once only through their union. It is not a pixel
	// readback, nothing here looked at a frame, and the key says so in its own
	// stat string. Covering the frame is what a still answers.
	//
	// IT FAILS CLOSED ON IDENTITY. A shot whose camera or control camera did
	// not answer prints nothing-measured rather than "no", because "no" is a
	// claim about a frame and silence is not.
	inline std::string ShotControlQuadLine(const LedgerVignette::Camera& ShotCam,
	                                       const std::string& ControlCameraId,
	                                       int QuadsSpawned,
	                                       bool bWholeFrameKeysOnThisLine,
	                                       int W, int H)
	{
		const std::string Key = "shotWholeFrameIncludesControlQuads=";
		if (!bWholeFrameKeysOnThisLine)
		{
			return Key + "nothing-measured/this-line-carries-no-whole-frame-keys";
		}
		if (ShotCam.Id.empty() || ControlCameraId.empty())
		{
			return Key + "nothing-measured/no-camera-identity-answered";
		}
		if (QuadsSpawned <= 0)
		{
			return Key + "no/no-control-quads-were-spawned-in-this-build";
		}
		if (!ControlQuadsVisibleFor(ShotCam.Id, ControlCameraId))
		{
			return Key + "no/hidden-for-this-camera";
		}
		// THE QUADS ARE VISIBLE ONLY IN THE FRAMES OF THE CAMERA THEY WERE
		// PLACED FROM, which ControlQuadsVisibleFor has just established, so
		// the placement camera and the shooting camera are the same camera and
		// the projection below is taken from the one this shot used.
		double X0 = 0.0, X1 = 0.0, Y0 = 0.0, Y1 = 0.0;
		int Boxed = 0;
		const int Asked = ControlQuadCount();
		for (int I = 0; I < Asked; ++I)
		{
			const QuadPlace P = ControlQuadPlace(ShotCam, I);
			const ScreenBox B = ControlQuadBox(ShotCam, P, W, H);
			if (!B.bMeasured) { continue; }
			if (Boxed == 0) { X0 = B.X0; X1 = B.X1; Y0 = B.Y0; Y1 = B.Y1; }
			else
			{
				if (B.X0 < X0) { X0 = B.X0; }
				if (B.X1 > X1) { X1 = B.X1; }
				if (B.Y0 < Y0) { Y0 = B.Y0; }
				if (B.Y1 > Y1) { Y1 = B.Y1; }
			}
			++Boxed;
		}
		std::string Out = Key
			+ "yes/whole-frame-keys-on-this-line-include-them"
			  "/boxes=see-controlQuadVisibility-and-the-quad-lines"
			  "/PROJECTED-BOXES-NOT-MEASURED-COVERAGE";
		char Buf[520];
		if (Boxed == 0)
		{
			std::snprintf(Buf, sizeof(Buf),
				" shotControlQuadsBoxed=0/of=%d/quads-with-four-corners-ahead"
				" shotControlQuadsBoxPx=nothing-measured/no-quad-projected-with-all-four-"
				"corners-ahead shotControlQuadsAtMostPctOfFrame=nothing-measured"
				" shotControlQuadsBoxStat=per-sample/projected-by-ControlQuadPlace-and-"
				"ProjectFilePoint/not-a-pixel-readback",
				Asked);
			Out += Buf;
			return Out;
		}
		const double CX0 = X0 < 0.0 ? 0.0 : (X0 > (double)W ? (double)W : X0);
		const double CX1 = X1 < 0.0 ? 0.0 : (X1 > (double)W ? (double)W : X1);
		const double CY0 = Y0 < 0.0 ? 0.0 : (Y0 > (double)H ? (double)H : Y0);
		const double CY1 = Y1 < 0.0 ? 0.0 : (Y1 > (double)H ? (double)H : Y1);
		const double Area = (CX1 - CX0) * (CY1 - CY0);
		const double Frame = (double)W * (double)H;
		const double Pct = (Frame > 0.0 && Area > 0.0) ? (Area * 100.0 / Frame) : 0.0;
		std::snprintf(Buf, sizeof(Buf),
			" shotControlQuadsBoxed=%d/of=%d/quads-with-four-corners-ahead"
			" shotControlQuadsBoxPx=x%.0f..%.0f/y%.0f..%.0f shotControlQuadsFrame=%dx%d"
			" shotControlQuadsAtMostPctOfFrame=%.2f"
			" shotControlQuadsBoxStat=per-sample/union-of-the-projected-boxes-clipped-to-"
			"the-frame/AT-MOST-because-a-box-is-not-a-quad/projected-by-ControlQuadPlace-"
			"and-ProjectFilePoint/not-a-pixel-readback",
			Boxed, Asked, X0, X1, Y0, Y1, W, H, Pct);
		Out += Buf;
		return Out;
	}

	// ---- THE FOUR COLOURS ------------------------------------------------
	//
	// SATURATED AND FAR APART, ON PURPOSE. The frame this is read against
	// tops out at chroma 15 and the warmest albedo in the pack means 32, so
	// a control that renders at chroma 20 would prove nothing. Every one of
	// these is at the corner of the cube: whatever the light and the tone
	// mapper do to them, four channel orderings this far apart cannot all
	// collapse onto the neutral grey the street is rendering now.
	inline int ControlColourCount() { return 4; }

	inline void ControlColour(int I, int& R, int& G, int& B)
	{
		const int V[4][3] = {{255, 0, 0}, {0, 255, 0}, {0, 0, 255}, {255, 255, 0}};
		const int J = (I >= 0 && I < 4) ? I : 0;
		R = V[J][0]; G = V[J][1]; B = V[J][2];
	}

	inline const char* ControlColourName(int I)
	{
		const char* N[4] = {"red", "green", "blue", "yellow"};
		return (I >= 0 && I < 4) ? N[I] : "out-of-range";
	}

	// THE BUFFER ORDER, AND IT IS NAMED AS THE BUFFER'S rather than as the
	// screen's. Texel 0 is the first in the row-major upload, which is the
	// texture's own origin; which screen corner that lands on depends on the
	// mesh's UV layout and this header does not assert one. The reading the
	// run needs is that four saturated colours appear at all.
	inline const char* ControlTexelSlot(int I)
	{
		const char* N[4] = {"texel0", "texel1", "texel2", "texel3"};
		return (I >= 0 && I < 4) ? N[I] : "out-of-range";
	}

	inline std::string ControlColoursValue()
	{
		std::string Out;
		for (int I = 0; I < ControlColourCount(); ++I)
		{
			int R = 0, G = 0, B = 0;
			ControlColour(I, R, G, B);
			char Buf[64];
			std::snprintf(Buf, sizeof(Buf), "%s%s.%s.%d.%d.%d",
			              I > 0 ? "/" : "", ControlTexelSlot(I),
			              ControlColourName(I), R, G, B);
			Out += Buf;
		}
		return Out;
	}

	// ---- WHAT THE EMITTER ANSWERED FOR ONE QUAD --------------------------
	//
	// The top layer fills this in with live state only: whether an actor
	// came back, whether the instance was made, what the engine said when
	// asked for the parameter back, and WHERE THE ACTOR ACTUALLY IS, read
	// off the actor rather than repeated from the request. Every count,
	// difference and word below is computed here.
	struct QuadResult
	{
		bool bSpawned = false;
		bool bMidMade = false;
		bool bTexMade = false;
		bool bTexResource = false;
		bool bTexReadback = false;
		bool bCompIsMid = false;
		bool bRead = false;                    // the actor answered for its transform
		double ReadXCm = 0.0, ReadYCm = 0.0, ReadZCm = 0.0;
		std::string Note = "none";
	};

	inline double QuadDeltaCm(const QuadPlace& P, const QuadResult& R)
	{
		if (!R.bRead) { return -1.0; }
		const double Dx = R.ReadXCm - P.XCm;
		const double Dy = R.ReadYCm - P.YCm;
		const double Dz = R.ReadZCm - P.ZCm;
		return std::sqrt(Dx * Dx + Dy * Dy + Dz * Dz);
	}

	// ONE LINE PER QUAD. Per-sample numbers only; the run's totals are on the
	// quads' own done line below.
	inline std::string ControlQuadLine(const LedgerVignette::Camera& C,
	                                   const QuadPlace& P, const QuadResult& R,
	                                   int W, int H)
	{
		const ScreenBox B = ControlQuadBox(C, P, W, H);
		const double Delta = QuadDeltaCm(P, R);
		std::string Out = "controlQuad=" + LedgerVignette::NoSpaces(P.Id);
		char Head[520];
		std::snprintf(Head, sizeof(Head),
			" quadStatus=%s quadMid=%s quadTexture=%s quadTexResource=%s"
			" quadTexReadback=%s quadCompMaterial=%s quadTiling=%.2fx%.2f quadSizeM=%.2f",
			R.bSpawned ? "SPAWNED" : "SPAWN-FAILED",
			R.bMidMade ? "made" : "NOT-MADE",
			P.bBindTexture ? (R.bTexMade ? "2x2-built-in-code/BGRA8/srgb.yes/filter.nearest"
			                             : "2x2-BUILD-FAILED")
			               : "none-bound/the-base-material-default",
			P.bBindTexture ? (R.bTexResource ? "valid" : "NULL") : "not-asked",
			P.bBindTexture ? (R.bTexReadback ? "same-pointer" : "OTHER-OR-NULL") : "not-asked",
			R.bCompIsMid ? "is-the-instance-we-made" : "OTHER",
			P.TileU, P.TileV, P.SizeM);
		Out += Head;
		// ASKED AND READ BACK, BOTH, because asking for a transform and
		// printing the transform you asked for is not evidence that anything
		// moved. An actor that did not answer prints the words rather than
		// repeating the request as though it were a reading.
		char Where[320];
		if (R.bRead)
		{
			std::snprintf(Where, sizeof(Where),
				" quadAskedXYZcm=%.1f/%.1f/%.1f quadReadXYZcm=%.1f/%.1f/%.1f"
				" quadDeltaCm=%.2f",
				P.XCm, P.YCm, P.ZCm, R.ReadXCm, R.ReadYCm, R.ReadZCm, Delta);
		}
		else
		{
			std::snprintf(Where, sizeof(Where),
				" quadAskedXYZcm=%.1f/%.1f/%.1f quadReadXYZcm=not-read"
				" quadDeltaCm=not-read",
				P.XCm, P.YCm, P.ZCm);
		}
		Out += Where;
		char Screen[420];
		std::snprintf(Screen, sizeof(Screen),
			" quadOn=%s/%dx%d quadCentrePx=%.0f/%.0f quadBoxPx=x%.0f..%.0f/y%.0f..%.0f"
			" quadDistM=%.2f quadCornersAhead=%d/4 quadCornersInFrame=%d/4"
			" quadProjection=pinhole-from-the-spec-camera/not-an-engine-readback",
			LedgerVignette::NoSpaces(C.Id).c_str(), W, H,
			B.CxPx, B.CyPx, B.X0, B.X1, B.Y0, B.Y1,
			B.DistM, B.CornersAhead, B.CornersInFrame);
		Out += Screen;
		Out += " quadTexels=" + ControlColoursValue();
		Out += std::string(" quadReads=") + (P.bBindTexture
			? "four-colours-means-a-texture-override-reaches-the-sampler/checker-means-it-does-not"
			: "cell-count-against-the-other-tile-quad/differing-means-the-scalars-reach-the-shader");
		Out += " quadNote=" + LedgerVignette::NoSpaces(R.Note);
		return Out;
	}

	// THE QUADS' OWN DONE LINE. Whole-run numbers only, and a pass that
	// spawned nothing says the words rather than printing a clean 0/0.
	inline std::string ControlQuadsDoneLine(const std::vector<QuadResult>& All,
	                                        bool bBaseLoaded)
	{
		const int Asked = ControlQuadCount();
		int Spawned = 0, Mids = 0;
		for (size_t I = 0; I < All.size(); ++I)
		{
			if (All[I].bSpawned) { ++Spawned; }
			if (All[I].bMidMade) { ++Mids; }
		}
		if (All.empty())
		{
			char Buf[420];
			std::snprintf(Buf, sizeof(Buf),
				"controlQuadsStatus=NOT-REACHED controlQuads=nothing-measured/%d"
				" controlQuadMids=nothing-measured controlQuadColours=%s"
				" controlQuadsNote=the-control-pass-never-ran",
				Asked, ControlColoursValue().c_str());
			return std::string(Buf);
		}
		char Buf[520];
		std::snprintf(Buf, sizeof(Buf),
			"controlQuadsStatus=%s controlQuads=%d/%d controlQuadMids=%d/%d"
			" controlQuadBase=%s controlQuadColours=%s"
			" controlQuadsStat=counts-over-the-controls-this-build-asks-for"
			" controlQuadsRule=the-colour-quad-answers-the-texture-path/the-two-tile-quads-answer-the-scalar-path",
			(Spawned == Asked && Mids == Asked) ? "ALL"
			                                    : (Spawned == 0 ? "NONE" : "PARTIAL"),
			Spawned, Asked, Mids, Asked,
			bBaseLoaded ? "loaded" : "MISSING",
			ControlColoursValue().c_str());
		return std::string(Buf);
	}
}
