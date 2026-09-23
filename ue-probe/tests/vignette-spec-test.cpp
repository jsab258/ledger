// THE SCENE READER, COMPILED AND RUN HERE, AGAINST THE REAL COMMITTED FILE.
//
// WHY THIS EXISTS. The Unreal module cannot be compiled in the container
// that writes it, so anything put there ships UNRUN and the first thing that
// finds out whether it works is a 25-minute round trip on Jafar's PC. The
// standing rule from 25 August is therefore that measurement arithmetic and
// formatting live where the tests run, and VignetteSpec.h is written to that
// rule: it has no Unreal type in it, so this file compiles it with g++ and
// runs it before any dispatch.
//
// THE ACCEPTING FIXTURE IS THE LIVE CODEBASE, which is the rule for tools
// that check the project itself: production/specs/vignette-pieces.json as
// committed. The rejecting fixtures are synthetic, because a rejection has
// to be provoked and the repository has no broken street in it.
//
// WHAT IT CANNOT SEE, said plainly rather than left to be assumed: nothing
// here proves an actor spawns, that a light reaches a pixel, or that a
// screenshot lands. Those are the run's business. This proves that the file
// is read correctly and that every string this run will print is the string
// it was meant to print.
#include "../Source/LedgerProbe/Public/VignetteSpec.h"
#include "../Source/LedgerProbe/Public/SurfaceBind.h"
#include "../Source/LedgerProbe/Public/StreetMeshes.h"

#include <clocale>
#include <cstdio>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <sstream>
#include <vector>

static int gChecks = 0;
static int gFailed = 0;

static void Check(bool Cond, const char* Name, const std::string& Detail = std::string())
{
	++gChecks;
	if (Cond)
	{
		std::printf("  ok - %s\n", Name);
		return;
	}
	++gFailed;
	std::printf("  FAILED - %s%s%s\n", Name,
	            Detail.empty() ? "" : " : ", Detail.c_str());
}

static std::string Slurp(const char* Path, bool& Ok)
{
	std::ifstream In(Path, std::ios::binary);
	if (!In) { Ok = false; return std::string(); }
	std::ostringstream SS;
	SS << In.rdbuf();
	Ok = true;
	return SS.str();
}

// EVERY KEY NAME ON ONE LINE. Used to prove two lines cannot collide, which
// is the write-time half of the rule tools/verdict-dupkeys.py enforces at read
// time: a key that means one thing per surface and another thing per run is
// returned by whichever line a grep reaches first.
static void KeysOf(const std::string& Line, std::vector<std::string>& Out)
{
	std::istringstream In(Line);
	std::string Tok;
	while (In >> Tok)
	{
		const size_t At = Tok.find('=');
		if (At == std::string::npos || At == 0) { continue; }
		Out.push_back(Tok.substr(0, At));
	}
}

// EVERY TOKEN IS A KEY WITH A VALUE, AND NO VALUE CARRIES WHITESPACE. The
// rule that matters for this project's readers, which all split on space: a
// value may hold several equals signs (propCentreWorstMm=0.00/on=x/of=0 does,
// and so does every row-shaped value in the prop segment), but a value that
// holds a SPACE is silently truncated by every one of them.
static bool EveryTokenIsKeyValue(const std::string& Line)
{
	std::istringstream In(Line);
	std::string Tok;
	int Tokens = 0;
	while (In >> Tok)
	{
		++Tokens;
		const size_t At = Tok.find('=');
		if (At == std::string::npos || At == 0 || At + 1 >= Tok.size()) { return false; }
	}
	return Tokens > 0;
}

static bool NoSpacePastPrefix(const std::string& Line, const char* From)
{
	const size_t At = Line.find(From);
	if (At == std::string::npos) { return false; }
	std::istringstream In(Line.substr(At));
	std::string Tok;
	int Tokens = 0, Equals = 0;
	while (In >> Tok)
	{
		++Tokens;
		int E = 0;
		for (size_t I = 0; I < Tok.size(); ++I) { if (Tok[I] == '=') { ++E; } }
		if (E != 1) { return false; }
		Equals += E;
	}
	return Tokens > 0 && Tokens == Equals;
}

// THE VALUE OF ONE KEY ON A key=value LINE, up to the next space, so a list
// can be compared for EQUALITY rather than for containment: a find() of
// "nullSeriesIds=a;b" is satisfied by "nullSeriesIds=a;b;c", which is the
// one comparison a growing list must not pass.
static std::string ValueOfKey(const std::string& Line, const char* Key)
{
	const size_t At = Line.find(Key);
	if (At == std::string::npos) { return std::string("key-not-on-the-line"); }
	const size_t From = At + std::string(Key).size();
	const size_t End = Line.find(' ', From);
	return Line.substr(From, End == std::string::npos ? std::string::npos : End - From);
}

static void SplitOn(const std::string& In, char Sep, std::vector<std::string>& Out)
{
	size_t At = 0;
	while (At <= In.size())
	{
		size_t End = In.find(Sep, At);
		if (End == std::string::npos) { End = In.size(); }
		Out.push_back(In.substr(At, End - At));
		if (End == In.size()) { break; }
		At = End + 1;
	}
}

// ---- THE PIN INVARIANT OF 2026-09-14, ONE EVALUATOR, FIVE RUNS -----------
//
// RULED in game-design/decision-2026-09-14-ruling-the-pin-belongs-to-the-rig-
// and-the-render-waits-for-it.md section 6, replacing "the only rows asking
// for a pin are the ladder rungs". THE OLD GUARD WAS RIGHT ON 10 SEPTEMBER
// AND IS WRONG NOW, and the reason is a reading rather than a preference: on
// 10 September no value had been read off the ladder, so any row outside it
// carried a guess. Run 41 lines 189 to 213 then photographed twenty five rows
// under automatic exposure, six of them one identical-input group at cam_hook
// reading 0.5800, 0.6057, 0.0765, 0.5741, 0.9591 and 0.6057: a spread of
// 0.8826 against that run's smallest sky step of 0.0023, verdict NO-READ. The
// four pinned rungs on the same run agree within 0.0001, four pairs of four,
// across an intervening night frame. So what has to be refused is not "a pin
// outside the ladder" but what the old comment actually said, "an exposure
// nobody chose": a pin value that is neither a rung's nor the one live value
// whose provenance the file names.
//
// ONE EVALUATOR, CALLED ONCE ON THE LIVE FILE AND ONCE PER PLANT, so a plant
// cannot pass by being judged with different arithmetic from the accepting
// case. Every count it reports is a whole-file tally over the conditions it
// was handed, never a statistic of one row.
struct PinReading
{
	int DayPinned, DayUnpinned, NightPinned, NightUnpinned;
	int LiveRows, Rungs, Count, ProvPinTokens;
	double Live, RungLo, RungHi;
	bool bSame;
	bool bA, bB, bC, bD;
	std::string ProvPin;      // the pinX.XXXX token's value, or nothing-declared
	std::string ProvRungId;   // the condition cond.<id> names, or none-named
	std::string RungState;    // present-and-equal / present-and-differs / absent-token-stands-alone
	std::string Line;         // the series, printed before any bound is read
	PinReading() : DayPinned(0), DayUnpinned(0), NightPinned(0), NightUnpinned(0),
	               LiveRows(0), Rungs(0), Count(0), ProvPinTokens(0),
	               Live(0.0), RungLo(0.0), RungHi(0.0), bSame(true),
	               bA(false), bB(false), bC(false), bD(false),
	               ProvPin("nothing-declared"), ProvRungId("none-named"),
	               RungState("absent-token-stands-alone") {}
};

// A LADDER RUNG BY THE ID SHAPE THE RULING NAMES, `pin_` with
// `pin_setter_night` excluded: the setter is the night row that proves the
// pin from the shot before it does not survive into an unpinned frame, so it
// is a rung of the mechanism and not of the value.
static bool IsLadderRung(const std::string& Id)
{
	return Id.compare(0, 4, "pin_") == 0 && Id != "pin_setter_night";
}

// THE PROVENANCE IS A SLASH-SEPARATED LIST AND IS READ AS TOKENS, NOT AS A
// SUBSTRING. `find("pin0.3000")` would be satisfied by `pin0.30001` and by
// `notapin0.3000`; a token walk cannot be. The count comes back too, because
// two tokens carrying two values is not the same fact as one.
static void ProvenanceTokens(const std::string& Prov, const std::string& Prefix,
                             std::vector<std::string>& Out)
{
	size_t At = 0;
	while (At <= Prov.size())
	{
		size_t End = Prov.find('/', At);
		if (End == std::string::npos) { End = Prov.size(); }
		const std::string Tok = Prov.substr(At, End - At);
		if (Tok.size() > Prefix.size() && Tok.compare(0, Prefix.size(), Prefix) == 0)
		{
			Out.push_back(Tok.substr(Prefix.size()));
		}
		if (End == Prov.size()) { break; }
		At = End + 1;
	}
}

static PinReading ReadPins(const std::vector<LedgerVignette::Condition>& Conds,
                           const std::string& Provenance)
{
	PinReading R;
	R.Count = (int)Conds.size();
	for (size_t I = 0; I < Conds.size(); ++I)
	{
		const LedgerVignette::Condition& C = Conds[I];
		const bool bAsked = LedgerVignette::ExposurePinAsked(C.ExposurePin);
		const bool bRung = IsLadderRung(C.Id);
		if (C.SunOn) { if (bAsked) { ++R.DayPinned; } else { ++R.DayUnpinned; } }
		else         { if (bAsked) { ++R.NightPinned; } else { ++R.NightUnpinned; } }
		if (bRung)
		{
			if (R.Rungs == 0 || C.ExposurePin < R.RungLo) { R.RungLo = C.ExposurePin; }
			if (R.Rungs == 0 || C.ExposurePin > R.RungHi) { R.RungHi = C.ExposurePin; }
			++R.Rungs;
		}
		if (C.SunOn && !bRung)
		{
			if (R.LiveRows == 0) { R.Live = C.ExposurePin; }
			else if (std::fabs(C.ExposurePin - R.Live) > 1e-12) { R.bSame = false; }
			++R.LiveRows;
		}
	}
	// (a) EVERY CONDITION ANSWERS THE PIN QUESTION, kept from the guard this
	// replaces. It is an identity over the same loop and the other three
	// counts are read against it.
	R.bA = (R.DayPinned + R.DayUnpinned + R.NightPinned + R.NightUnpinned == R.Count)
	       && R.Count > 0;
	// (b) SUN ON IMPLIES A PIN, SUN OFF IMPLIES NONE, with both denominators
	// required to be non-zero so neither half can be vacuously true on a file
	// that carries no day rows or no night rows.
	R.bB = (R.DayUnpinned == 0) && (R.NightPinned == 0)
	       && R.DayPinned > 0 && R.NightUnpinned > 0;
	// (c) ONE LIVE VALUE ON EVERY SUN-ON ROW THAT IS NOT A RUNG.
	R.bC = R.LiveRows > 0 && R.bSame && LedgerVignette::ExposurePinAsked(R.Live);
	// (d) AND THAT LIVE VALUE IS THE ONE THE PROVENANCE NAMES, to the four
	// decimals the shot line prints, so a value edited onto the rows without
	// re-reading the ladder series is refused. While the rung the provenance
	// names is still in the file its own pin must agree with the token; when
	// the one-run rows leave, the token stands alone and the clause still
	// bites.
	char Want[32];
	std::snprintf(Want, sizeof(Want), "%.4f", R.Live);
	std::vector<std::string> PinToks, CondToks;
	ProvenanceTokens(Provenance, "pin", PinToks);
	ProvenanceTokens(Provenance, "cond.", CondToks);
	R.ProvPinTokens = (int)PinToks.size();
	if (R.ProvPinTokens >= 1) { R.ProvPin = PinToks[0]; }
	if (!CondToks.empty())
	{
		R.ProvRungId = CondToks[0];
		for (size_t I = 0; I < Conds.size(); ++I)
		{
			if (Conds[I].Id != R.ProvRungId) { continue; }
			char Has[32];
			std::snprintf(Has, sizeof(Has), "%.4f", Conds[I].ExposurePin);
			R.RungState = (R.ProvPin == std::string(Has)) ? "present-and-equal"
			                                             : "present-and-differs";
		}
	}
	R.bD = (R.ProvPinTokens == 1) && (R.ProvPin == std::string(Want))
	       && R.RungState != std::string("present-and-differs");
	char Buf[640];
	std::snprintf(Buf, sizeof(Buf),
		"pins: dayPinned=%d dayUnpinned=%d nightPinned=%d nightUnpinned=%d "
		"live=%.4f liveRows=%d liveAgree=%s rungs=%d span=%.3f..%.3f "
		"provenancePin=%s provenancePinTokens=%d provenanceRung=%s/%s "
		"of %d conditions",
		R.DayPinned, R.DayUnpinned, R.NightPinned, R.NightUnpinned,
		R.Live, R.LiveRows, R.bSame ? "yes" : "no", R.Rungs, R.RungLo, R.RungHi,
		R.ProvPin.c_str(), R.ProvPinTokens, R.ProvRungId.c_str(),
		R.RungState.c_str(), R.Count);
	R.Line = Buf;
	return R;
}

// ---- THE REFERENCE CELL AGAINST THE JUDGED DAY ROW, 2026-09-14 -----------
//
// Ruled at 18:23Z in game-design/decision-2026-09-14-ruling-the-null-series-
// follows-the-judged-row.md. The grid's reference cell exists to carry the
// judged row's inputs, which is the whole reason the judged hook frame is
// itself a member of the null series. Its fields were a COPY of overcast_day's
// taken on 9 September and nothing in the spec derives them, so when the
// judged row moved to fog_max_opacity 0.100 the copy went stale in silence and
// the judged frame walked out of its own noise floor. This comparison is the
// pair that move owes.
//
// IT NAMES THE FIRST FIELD THAT DIFFERS AND BOTH VALUES, because "the two rows
// differ" sends the reader back to the JSON and "fog_max_opacity ref=0.450000
// judged=0.100000" does not.
//
// WETNESS IS IN THE COMPARISON AND IS NOT IN THE APPLIED-INPUT FINGERPRINT,
// which is deliberate and not an oversight: `wetness` has no read site in
// VignetteShot.cpp on this commit (queue 186), so two rows differing only in
// it render one street HERE, but a reference cell that has drifted in wetness
// is a false reference the day queue 186 wires it. The fingerprint says what
// this engine renders; this says what the reference cell is FOR.
//
// AND WIRING IT IS TWO CHANGES AND NOT ONE, which the excludes value now says
// rather than leaving to a grep: M_LedgerSurface carries TilingU and TilingV
// and no other scalar, so the read site needs a material parameter to write
// to before it can move a pixel.
//
// THE CASCADE, COUNTED ON THE COMMITTED SPEC RATHER THAN REASONED ABOUT. The
// day the fingerprint gains wetness, the largest identical-input group at
// cam_hook goes from NINE rows to SEVEN and the distinct-group count from 28
// to 30. Only vign_wet_000 and vign_wet_100 leave: vign_wet_060 carries 0.6000,
// which is the judged row's own wetness, so it STAYS in the group. The obvious
// guess is six, all three wetness rows leaving, and it is wrong for that
// reason; the number is written here because it was measured and not because
// it was expected. Seven is still above the two samples a spread needs, so
// nullSeriesStatus stays READ across the change.
static std::string NullRefFieldStr(double V)
{
	char Buf[64];
	std::snprintf(Buf, sizeof(Buf), "%.6f", V);
	return std::string(Buf);
}

static std::string RefCellAgainstJudged(const LedgerVignette::Condition& Ref,
                                        const LedgerVignette::Condition& Day)
{
	if (Ref.Hdri != Day.Hdri)
	{
		return "hdri ref=" + Ref.Hdri + " judged=" + Day.Hdri;
	}
	if (Ref.SunOn != Day.SunOn)
	{
		return std::string("sun ref=") + (Ref.SunOn ? "on" : "off")
		     + " judged=" + (Day.SunOn ? "on" : "off");
	}
	if (Ref.LanternsOn != Day.LanternsOn)
	{
		return std::string("lanterns ref=") + (Ref.LanternsOn ? "on" : "off")
		     + " judged=" + (Day.LanternsOn ? "on" : "off");
	}
	if (Ref.WindowsOn != Day.WindowsOn)
	{
		return std::string("window_practicals ref=") + (Ref.WindowsOn ? "on" : "off")
		     + " judged=" + (Day.WindowsOn ? "on" : "off");
	}
	if (std::fabs(Ref.SunIntensity - Day.SunIntensity) > 1e-12)
	{
		return "sun_intensity ref=" + NullRefFieldStr(Ref.SunIntensity)
		     + " judged=" + NullRefFieldStr(Day.SunIntensity);
	}
	if (std::fabs(Ref.SkyIntensity - Day.SkyIntensity) > 1e-12)
	{
		return "sky_intensity ref=" + NullRefFieldStr(Ref.SkyIntensity)
		     + " judged=" + NullRefFieldStr(Day.SkyIntensity);
	}
	if (std::fabs(Ref.Wetness - Day.Wetness) > 1e-12)
	{
		return "wetness ref=" + NullRefFieldStr(Ref.Wetness)
		     + " judged=" + NullRefFieldStr(Day.Wetness);
	}
	if (std::fabs(Ref.FogDensity - Day.FogDensity) > 1e-12)
	{
		return "fog_density ref=" + NullRefFieldStr(Ref.FogDensity)
		     + " judged=" + NullRefFieldStr(Day.FogDensity);
	}
	if (std::fabs(Ref.FogMaxOpacity - Day.FogMaxOpacity) > 1e-12)
	{
		return "fog_max_opacity ref=" + NullRefFieldStr(Ref.FogMaxOpacity)
		     + " judged=" + NullRefFieldStr(Day.FogMaxOpacity);
	}
	if (std::fabs(Ref.ExposurePin - Day.ExposurePin) > 1e-12)
	{
		return "exposure_pin ref=" + NullRefFieldStr(Ref.ExposurePin)
		     + " judged=" + NullRefFieldStr(Day.ExposurePin);
	}
	return std::string();
}

// TWO CONDITIONS ARE ONE FAMILY when they match in every field this engine
// applies EXCEPT sky, which is the no-sky fingerprint written out field by
// field. Written here rather than reached for through SampleKey, because the
// checks that use it exist to disagree with the emitter when the emitter is
// wrong, and a check calling the code it audits can only ever agree with it.
static bool SameNullFamily(const LedgerVignette::Condition& A,
                           const LedgerVignette::Condition& B)
{
	return A.Hdri == B.Hdri && A.SunOn == B.SunOn
	    && A.LanternsOn == B.LanternsOn && A.WindowsOn == B.WindowsOn
	    && std::fabs(A.SunIntensity - B.SunIntensity) < 1e-12
	    && std::fabs(A.Wetness - B.Wetness) < 1e-12
	    && std::fabs(A.FogDensity - B.FogDensity) < 1e-12
	    && std::fabs(A.FogMaxOpacity - B.FogMaxOpacity) < 1e-12
	    && std::fabs(A.ExposurePin - B.ExposurePin) < 1e-12;
}

// THE NULL CELL'S POSITION, RESTATED TO THE THING IT PROTECTS. Section 4 of
// game-design/decision-2026-09-16-ruling-the-floor-is-read-in-a-family-that-
// holds-a-step-and-the-settle-rows-are-outside-it-by-their-own-fields.md.
// The check used to read "the null cell is the last shot in the LIST", which
// its own comment explained as identical inputs at maximum order separation.
// The 06:35Z ruling then placed queue 334's six settle rows at the end of the
// list for a measured reason (so no existing row's predecessor changes, which
// is what keeps the first run carrying them comparable with run 48), and the
// two sentences cannot both hold. The separation the value comes from is
// separation from the null cell's OWN family: six frames of another family
// sitting after it neither shorten it nor could lengthen it. So the invariant
// is restated to the last shot at the reference cell's camera whose condition
// matches the reference cell in every field but sky, and every case the old
// sentence caught for its stated purpose this one still catches: a family row
// placed after the null cell fails it.
//
// Returns the index of that shot, or -1 when the reference cell has no shot
// of its own. The family shots walked are handed back so the assertion's zero
// can never read as a clean result.
static int LastShotOfRefFamily(const LedgerVignette::Spec& S, const char* RefCondId,
                               int& OutFamilyShots)
{
	OutFamilyShots = 0;
	const LedgerVignette::Condition* RefC = 0;
	for (size_t I = 0; I < S.Conditions.size(); ++I)
	{
		if (S.Conditions[I].Id == RefCondId) { RefC = &S.Conditions[I]; }
	}
	if (RefC == 0) { return -1; }
	std::string RefCam;
	for (size_t I = 0; I < S.Shots.size() && RefCam.empty(); ++I)
	{
		if (S.Shots[I].ConditionId == RefC->Id) { RefCam = S.Shots[I].CameraId; }
	}
	if (RefCam.empty()) { return -1; }
	int Last = -1;
	for (size_t I = 0; I < S.Shots.size(); ++I)
	{
		if (S.Shots[I].CameraId != RefCam) { continue; }
		const LedgerVignette::Condition* C = 0;
		for (size_t J = 0; J < S.Conditions.size(); ++J)
		{
			if (S.Conditions[J].Id == S.Shots[I].ConditionId) { C = &S.Conditions[J]; }
		}
		if (C == 0 || !SameNullFamily(*C, *RefC)) { continue; }
		++OutFamilyShots;
		Last = (int)I;
	}
	return Last;
}

// THE FAMILY TALLY, RECOUNTED HERE RATHER THAN READ OFF THE LINE IT CHECKS.
// Section 3 of the same ruling moved the floor from the largest identical-
// input group to the largest one WHOSE NO-SKY FAMILY HOLDS A SKY-ONLY PAIR,
// because a spread with no step in its own family has nothing to be read
// against. Every number this file asserts about that rule is counted here, so
// a row entering or leaving the spec moves both sides together and none of
// these numbers is typed.
//
// WHAT IS SHARED AND WHAT IS NOT, stated rather than claimed. The family and
// group IDENTITIES come from SampleKey, which the emitter also calls: the
// tally beside the discovery has always worked this way and the comment there
// says what that costs, which is that the two cannot disagree about which
// frames share a fingerprint. What this recount can catch is a MISCOUNT: the
// loop, the denominator, the largest-of, the qualification, the tie. The STEP
// TEST here is the conditions' own sky values compared to each other, not the
// emitter's IsSkyOnlyPair, and the sun flag is the condition's own boolean
// handed in by the caller rather than a substring sniffed out of a key, so
// "does this family hold a step" is answered by two different routes.
struct NullFamilyTally
{
	int Families;             // distinct no-sky families over MEASURED frames
	int StepFamilies;         // of those, holding at least one sky-only pair
	int SunOffFamilies;       // of those, whose condition has the sun off
	int StepFamiliesSunOff;   // THE RATCHET: step-holding AND sun off
	int OutsideFrames;        // measured frames whose family holds no step
	int DistinctGroups;       // distinct identical-input groups over measured frames
	int QualifyingGroups;     // of those, whose own family holds a step
	int Largest;              // frames in the largest group BY SIZE ALONE, the old rule
	int LargestQualifying;    // frames in the largest QUALIFYING group, the rule now
	std::string LargestKey;            // the key size alone would have kept
	std::string LargestQualifyingKey;  // the key the family rule keeps
	std::vector<std::string> OutsideIds;   // shot order, uncapped: callers cap their own print
	// THE FAMILY ROWS THEMSELVES, in shot order of first appearance, so the
	// series can be PRINTED before any bound is read off it and the next rung
	// (production/queue/346) has the shape it needs already on the page.
	std::vector<std::string> FamilyKeys;
	std::vector<int> FamilyStep, FamilySunOff, FamilyFrames;
	NullFamilyTally() : Families(0), StepFamilies(0), SunOffFamilies(0),
	                    StepFamiliesSunOff(0), OutsideFrames(0), DistinctGroups(0),
	                    QualifyingGroups(0), Largest(0), LargestQualifying(0) {}
};

static NullFamilyTally TallyNullFamilies(
	const std::vector<LedgerVignette::FrameSample>& Samples,
	const std::vector<int>& SunOff)
{
	NullFamilyTally T;
	std::vector<std::string>& FamKeys = T.FamilyKeys;
	std::vector<int>& FamStep = T.FamilyStep;
	std::vector<int>& FamSunOff = T.FamilySunOff;
	std::vector<double> FamFirstSky;
	for (size_t I = 0; I < Samples.size(); ++I)
	{
		if (!Samples[I].bMeasured) { continue; }
		const std::string F = LedgerVignette::SampleKey(Samples[I], false);
		size_t At = FamKeys.size();
		for (size_t Q = 0; Q < FamKeys.size(); ++Q)
		{
			if (FamKeys[Q] == F) { At = Q; break; }
		}
		if (At == FamKeys.size())
		{
			FamKeys.push_back(F);
			FamFirstSky.push_back(Samples[I].SkyIntensity);
			FamStep.push_back(0);
			FamSunOff.push_back(I < SunOff.size() ? SunOff[I] : 0);
			T.FamilyFrames.push_back(1);
			continue;
		}
		++T.FamilyFrames[At];
		// A FAMILY HOLDS A STEP the moment one of its frames sits at another
		// sky value than the first one seen: if any two of its frames differ,
		// at least one of them differs from the first, so one comparison per
		// frame finds every family that holds a pair.
		if (std::fabs(Samples[I].SkyIntensity - FamFirstSky[At]) > 1e-12) { FamStep[At] = 1; }
	}
	T.Families = (int)FamKeys.size();
	for (size_t Q = 0; Q < FamKeys.size(); ++Q)
	{
		if (FamStep[Q]) { ++T.StepFamilies; }
		if (FamSunOff[Q]) { ++T.SunOffFamilies; }
		if (FamStep[Q] && FamSunOff[Q]) { ++T.StepFamiliesSunOff; }
	}
	std::vector<std::string> GroupKeys;
	std::vector<int> GroupSizes, GroupStep;
	for (size_t I = 0; I < Samples.size(); ++I)
	{
		if (!Samples[I].bMeasured) { continue; }
		const std::string K = LedgerVignette::SampleKey(Samples[I], true);
		const std::string F = LedgerVignette::SampleKey(Samples[I], false);
		int Holds = 0;
		for (size_t Q = 0; Q < FamKeys.size(); ++Q)
		{
			if (FamKeys[Q] == F) { Holds = FamStep[Q]; break; }
		}
		if (!Holds)
		{
			++T.OutsideFrames;
			T.OutsideIds.push_back(Samples[I].ShotId);
		}
		size_t At = GroupKeys.size();
		for (size_t Q = 0; Q < GroupKeys.size(); ++Q)
		{
			if (GroupKeys[Q] == K) { At = Q; break; }
		}
		if (At == GroupKeys.size())
		{
			GroupKeys.push_back(K); GroupSizes.push_back(0); GroupStep.push_back(Holds);
			At = GroupKeys.size() - 1;
		}
		++GroupSizes[At];
	}
	T.DistinctGroups = (int)GroupKeys.size();
	for (size_t Q = 0; Q < GroupKeys.size(); ++Q)
	{
		if (GroupSizes[Q] > T.Largest) { T.Largest = GroupSizes[Q]; T.LargestKey = GroupKeys[Q]; }
		if (!GroupStep[Q]) { continue; }
		++T.QualifyingGroups;
		if (GroupSizes[Q] > T.LargestQualifying)
		{
			T.LargestQualifying = GroupSizes[Q];
			T.LargestQualifyingKey = GroupKeys[Q];
		}
	}
	return T;
}

// THE PROVENANCE STRING IS READ OFF THE SCENE FILE BESIDE THE PIECE LIST, AND
// THIS IS A MEASUREMENT AND NOT A CONVENIENCE. production/specs/vignette-
// scene.json is where the resident writes the string; the piece list is
// generated from it by StreetVignettePieces.cs, whose condition writer (line
// 496) copies `exposure_pin` and NOT `exposure_pin_provenance`, so the root
// key ParseSpec reads at VignetteSpec.h line 415 is absent from the generated
// file and the run's own `expPinProvenance=` reads nothing-declared. Both
// readings are printed at the call site so the gap is a number rather than a
// remark. FAIL-CLOSED: no scene file, or no key in it, and clause (d) goes
// red naming what was missing, because a clause that quietly skips is the
// silent-instrument failure this file exists to prevent.
static std::string ScenePathBeside(const char* SpecPath)
{
	const std::string P(SpecPath);
	const size_t At = P.find_last_of("/\\");
	return (At == std::string::npos ? std::string() : P.substr(0, At + 1))
	     + "vignette-scene.json";
}

// ONE ROOT-LEVEL STRING OUT OF A JSON FILE, by scan rather than by parse: the
// value wanted carries no escape and no quote (it is space-free by the
// project's own key=value rule), and the alternative is a second reader in a
// test whose subject is the first one.
static std::string JsonStringField(const std::string& Text, const char* Key, bool& Found)
{
	Found = false;
	const std::string Needle = std::string("\"") + Key + "\"";
	size_t At = Text.find(Needle);
	if (At == std::string::npos) { return std::string(); }
	At = Text.find(':', At + Needle.size());
	if (At == std::string::npos) { return std::string(); }
	const size_t Open = Text.find('"', At);
	if (Open == std::string::npos) { return std::string(); }
	const size_t Close = Text.find('"', Open + 1);
	if (Close == std::string::npos) { return std::string(); }
	Found = true;
	return Text.substr(Open + 1, Close - Open - 1);
}

int main(int argc, char** argv)
{
	const char* SpecPath = (argc > 1) ? argv[1] : "production/specs/vignette-pieces.json";
	std::printf("VignetteSpec, against %s\n", SpecPath);

	bool Ok = false;
	const std::string Text = Slurp(SpecPath, Ok);
	Check(Ok && !Text.empty(),
	      "the committed piece list is on disk and not empty",
	      Ok ? "read but empty" : "could not open");
	if (!Ok || Text.empty())
	{
		std::printf("NOTHING MEASURED: no piece list at %s\n", SpecPath);
		return 1;
	}

	LedgerVignette::Spec S;
	std::string Err;
	const bool Parsed = LedgerVignette::ParseSpec(Text, S, Err);
	Check(Parsed, "the reader parses the committed piece list", Err);
	if (!Parsed) { std::printf("%d of %d check(s) failed\n", gFailed, gChecks); return 1; }

	// ---- THE ACCEPTING CASE, WITH ITS DENOMINATORS ----------------------
	std::printf("    read: pieces=%d header=%d cameras=%d conditions=%d shots=%d\n",
	            (int)S.Pieces.size(), S.HeaderPieces, (int)S.Cameras.size(),
	            (int)S.Conditions.size(), (int)S.Shots.size());
	Check((int)S.Pieces.size() == S.HeaderPieces,
	      "every piece the header claims is under it");
	Check(S.Pieces.size() > 500,
	      "the street read back is a street and not a handful of pieces");
	// THREE CAMERAS, FIVE JUDGED SHOTS AND TWENTY PROBE ROWS, AND THE SPLIT
	// IS NAMED RATHER THAN SUMMED.
	//
	// cam_A and cam_B by the two conditions are the FOUR MATCHED PAIRS the
	// engine decision is judged on, cam_hook under overcast_day is a fifth
	// judged shot that is deliberately not part of that pairing, and the
	// twenty rows this batch adds are ONE-RUN PROBE ROWS that the item
	// reading the run removes. A bare 25 would read as the pairing having
	// changed, so the three groups are counted apart.
	//
	// THE LADDER IS GONE, 2026-09-09, section 9 of the grid ruling, and its
	// series is preserved in section 3 of that record: five rungs across a
	// HUNDREDFOLD of sun moved band.ground.p05 by 1.06 of the null measured
	// between two shots of one condition.
	{
		int Matched = 0, ProbeShots = 0, ProbeAtHook = 0, JudgedAtHook = 0;
		for (size_t I = 0; I < S.Shots.size(); ++I)
		{
			const bool bJudged = (S.Shots[I].ConditionId == "overcast_day"
			                      || S.Shots[I].ConditionId == "wet_night");
			if (!bJudged)
			{
				++ProbeShots;
				if (S.Shots[I].CameraId == "cam_hook") { ++ProbeAtHook; }
			}
			else if (S.Shots[I].CameraId == "cam_A" || S.Shots[I].CameraId == "cam_B")
			{
				++Matched;
			}
			else if (S.Shots[I].CameraId == "cam_hook")
			{
				++JudgedAtHook;
			}
		}
		int JudgedConds = 0, ProbeConds = 0;
		for (size_t I = 0; I < S.Conditions.size(); ++I)
		{
			if (S.Conditions[I].Id == "overcast_day" || S.Conditions[I].Id == "wet_night")
			{
				++JudgedConds;
			}
			else { ++ProbeConds; }
		}
		std::printf("    rows: cameras=%d judgedConds=%d probeConds=%d shots=%d "
		            "matchedPairs=%d probeShots=%d probeAtHook=%d judgedAtHook=%d\n",
		            (int)S.Cameras.size(), JudgedConds, ProbeConds, (int)S.Shots.size(),
		            Matched, ProbeShots, ProbeAtHook, JudgedAtHook);
		// THE TOTAL IS READ AND NOT PINNED, QUEUE 235. Rows are added to this
		// file by the item that needs them and removed by the item that reads
		// them, so a literal total is a check that fails for the wrong reason
		// every time the file legitimately grows. WHAT MUST STAY TRUE is the
		// pairing and the classification: three cameras, two judged
		// conditions, the four judged pairs still exactly four, and every
		// shot falling into exactly one of the classes counted below, which
		// is the identity a bare total cannot state.
		Check(S.Cameras.size() == 3 && JudgedConds == 2 && Matched == 4,
		      "three cameras, two judged conditions, and the four judged pairs are still "
		      "exactly four whatever else the file has grown");
		Check((int)S.Shots.size() == Matched + ProbeShots + JudgedAtHook
		      && JudgedAtHook > 0,
		      "every shot in the file is one of the four judged pairs, a probe row, or a "
		      "judged row at the hook camera, and the classes sum to the total read",
		      "a shot in none of them is a row nothing in this test describes");
		// EVERY PROBE ROW STANDS AT cam_hook, and that is an instrument
		// repair as much as it is Jafar's judging camera: the three control
		// quads are HIDDEN on this camera (controlQuadHidden named
		// vign_hook_day on run 38), so no whole-frame key on a probe row
		// photographs the instrument, and at fovV 39.0 band.skyCentre is sky
		// rather than the rooftops it holds at fovV 60.0.
		// THE INVARIANT, NOT THE COUNT. The number of probe rows moves with
		// the file; the thing that must never move is that ALL of them stand
		// at one camera, because a group spanning two cameras is two pixel
		// populations read as one, which is the fault the batch review caught
		// in a group of nine. Queue 235's twelve exposure rows are at cam_hook
		// for exactly this reason, including the night rows that give the
		// after-night half of each rung its darkness.
		Check(ProbeShots > 0 && ProbeAtHook == ProbeShots,
		      "every probe row stands at cam_hook, the camera rung 1 is judged from",
		      "a probe row at another camera would be two pixel populations read as one");
		// THE NULL CELL IS SHOT LAST OF ITS OWN FAMILY. Identical inputs at
		// maximum order separation is the whole of its value, and the
		// separation that value comes from is separation from the frames it is
		// a null sample OF. Restated by section 4 of the 2026-09-16 ruling
		// when the 06:35Z placement put six rows of another family after it
		// for a measured reason; LastShotOfRefFamily above carries the
		// reasoning and walks the list field by field, calling no shared
		// function. ACCEPTING CASE FIRST, on the live file.
		{
			int FamilyShots = 0;
			const int LastFam = LastShotOfRefFamily(S, "grid_sky070_sun003", FamilyShots);
			std::printf("    null cell position: shots of the reference cell's family at its "
			            "camera=%d of %d walked, last=%s/%s, last shot in the whole list=%s\n",
			            FamilyShots, (int)S.Shots.size(),
			            LastFam < 0 ? "nothing-measured" : S.Shots[LastFam].Id.c_str(),
			            LastFam < 0 ? "nothing-measured" : S.Shots[LastFam].ConditionId.c_str(),
			            S.Shots.empty() ? "nothing-measured" : S.Shots[S.Shots.size() - 1].Id.c_str());
			Check(FamilyShots > 0 && LastFam >= 0
			      && S.Shots[LastFam].ConditionId == "grid_null_repeat",
			      "the null cell is the last shot of its own family at the reference camera, "
			      "as far from the frames it is a null sample of as the run allows",
			      LastFam < 0 ? std::string("no shot of the reference cell's family")
			                  : (S.Shots[LastFam].Id + "/" + S.Shots[LastFam].ConditionId
			                     + " over " + std::to_string(FamilyShots) + " family shot(s)"));
			// AND BOTH PLANTED CASES, because the restatement is only worth
			// the old sentence if it still refuses what the old sentence
			// refused. The rows are built from the reference cell itself
			// rather than from a named row of the spec, so doing the work this
			// file prompts can never break the check.
			const LedgerVignette::Condition* RefC = 0;
			for (size_t I = 0; I < S.Conditions.size(); ++I)
			{
				if (S.Conditions[I].Id == "grid_sky070_sun003") { RefC = &S.Conditions[I]; }
			}
			std::string RefCam;
			for (size_t I = 0; I < S.Shots.size() && RefCam.empty() && RefC != 0; ++I)
			{
				if (S.Shots[I].ConditionId == RefC->Id) { RefCam = S.Shots[I].CameraId; }
			}
			if (RefC != 0 && !RefCam.empty())
			{
				// REFUSED: a row of the null cell's OWN family placed after it,
				// which is the thing that shortens the separation.
				LedgerVignette::Spec T = S;
				LedgerVignette::Condition Fam = *RefC;
				Fam.Id = "planted_family_row_at_another_sky";
				Fam.SkyIntensity = RefC->SkyIntensity * 0.5 + 0.01;
				T.Conditions.push_back(Fam);
				LedgerVignette::Shot FamShot;
				FamShot.Id = "planted_family_shot";
				FamShot.CameraId = RefCam;
				FamShot.ConditionId = Fam.Id;
				T.Shots.push_back(FamShot);
				int PlantedFamShots = 0;
				const int PlantedLast = LastShotOfRefFamily(T, "grid_sky070_sun003",
				                                            PlantedFamShots);
				std::printf("    planted family row after the null cell: familyShots=%d "
				            "last=%s\n", PlantedFamShots,
				            PlantedLast < 0 ? "nothing-measured"
				                            : T.Shots[PlantedLast].Id.c_str());
				Check(PlantedLast >= 0
				      && T.Shots[PlantedLast].ConditionId != "grid_null_repeat"
				      && PlantedFamShots == FamilyShots + 1,
				      "a row of the null cell's own family placed after it FAILS the restated "
				      "check, which is the case the old sentence caught and this one must too",
				      PlantedLast < 0 ? std::string("no family shot")
				                      : T.Shots[PlantedLast].Id);
				// ACCEPTED: a row of ANOTHER family after it, which is what
				// the six settle rows are and what the 06:35Z placement chose.
				LedgerVignette::Spec U = S;
				LedgerVignette::Condition Other = *RefC;
				Other.Id = "planted_other_family_row";
				Other.FogMaxOpacity = RefC->FogMaxOpacity + 0.25;
				U.Conditions.push_back(Other);
				LedgerVignette::Shot OtherShot;
				OtherShot.Id = "planted_other_family_shot";
				OtherShot.CameraId = RefCam;
				OtherShot.ConditionId = Other.Id;
				U.Shots.push_back(OtherShot);
				int OtherFamShots = 0;
				const int OtherLast = LastShotOfRefFamily(U, "grid_sky070_sun003",
				                                          OtherFamShots);
				std::printf("    planted other-family row after the null cell: familyShots=%d "
				            "last=%s\n", OtherFamShots,
				            OtherLast < 0 ? "nothing-measured" : U.Shots[OtherLast].Id.c_str());
				Check(OtherLast >= 0
				      && U.Shots[OtherLast].ConditionId == "grid_null_repeat"
				      && OtherFamShots == FamilyShots,
				      "and a row of another family placed after it PASSES, which is what the "
				      "six settle rows are and why the 06:35Z placement stands",
				      OtherLast < 0 ? std::string("no family shot")
				                    : U.Shots[OtherLast].Id);
			}
		}
	}

	// ---- A1: THE GRID, ITS NULL CELL, AND THE TWO PROBE SERIES ----------
	//
	// PRINTED BEFORE IT IS ASSERTED, because this is the series the next
	// commit sets constants from and rule 2 says the printer ships first.
	{
		std::printf("    grid:");
		for (size_t I = 0; I < S.Conditions.size(); ++I)
		{
			std::printf(" %s=sun%.2f/sky%.2f/wet%.2f/fogMaxOp%.3f",
			            S.Conditions[I].Id.c_str(), S.Conditions[I].SunIntensity,
			            S.Conditions[I].SkyIntensity, S.Conditions[I].Wetness,
			            S.Conditions[I].FogMaxOpacity);
		}
		std::printf("\n");
		double DaySun = -1.0, DaySky = -1.0, DayCap = -1.0;
		double NightSun = -1.0, NightSky = -1.0;
		for (size_t I = 0; I < S.Conditions.size(); ++I)
		{
			const LedgerVignette::Condition& C = S.Conditions[I];
			if (C.Id == "overcast_day")
			{
				DaySun = C.SunIntensity; DaySky = C.SkyIntensity; DayCap = C.FogMaxOpacity;
			}
			if (C.Id == "wet_night") { NightSun = C.SunIntensity; NightSky = C.SkyIntensity; }
		}
		// THE TWO JUDGED ROWS CARRY THE OLD LITERALS UNCHANGED, which is what
		// makes "the field replaced the literal and moved no number" a check
		// rather than a claim. 3.0f was the bare literal at
		// VignetteShot.cpp:1240; 1.0 and 0.35 were kSkyIntensityDay and
		// kSkyIntensityNight; 0.45f was kFogMaxOpacityWithSky.
		// The sky moved on 2026-09-14 (ruling of 20:01Z): a RENDERED cell,
		// vign_fog010_sky070 on 622bc39, verdict line 217, band.skyCentre.p50
		// 0.8035 against the sheet's 0.808 and band.ground.p05 0.2003 against
		// its 0.1935.
		Check(std::fabs(DaySun - 3.0) < 1e-9,
		      "the day condition carries the retired sun literal unchanged");
		Check(std::fabs(DaySky - 0.70) < 1e-9,
		      "the judged day row's sky is 0.70, moved by the ruling of 2026-09-14 20:01Z "
		      "from the sky cross on 622bc39, row vign_fog010_sky070");
		Check(std::fabs(NightSun) < 1e-9 && std::fabs(NightSky - 0.35) < 1e-9,
		      "the night condition carries the night sky constant with its sun at zero");
		// THE JUDGED ROW MOVED, 2026-09-14, AND THIS IS THE OTHER HALF OF THE
		// MATCHED SET: CoreTests asserts the same number in the same commit, so
		// the two engines cannot disagree about what the street is judged at.
		// Until today this read 0.450 under the sentence "the field replaced the
		// literal and moved no number", which was true on 9 September and is
		// deliberately false now. A RENDERED cell, not an interpolation:
		// vign_fog_maxop0100 on 32bae70, verdict line 208, band.skyCentre.meanLuma
		// 0.7979 against the sheet's 0.808 and band.ground.p05 0.2532 against
		// its 0.1935.
		Check(std::fabs(DayCap - 0.100) < 1e-9,
		      "the judged day row's fog cap is 0.100, moved by the ruling of 2026-09-14 "
		      "from the fog series on 32bae70");
		// THE GRID IS THE CROSS AND NOTHING ELSE, counted out of the file.
		const double Skies[4] = { 1.00, 0.70, 0.50, 0.35 };
		const double Suns[3]  = { 3.0, 10.0, 30.0 };
		int Cells = 0, GridRows = 0;
		for (int A = 0; A < 4; ++A)
		{
			for (int B = 0; B < 3; ++B)
			{
				for (size_t I = 0; I < S.Conditions.size(); ++I)
				{
					const LedgerVignette::Condition& C = S.Conditions[I];
					if (C.Id.compare(0, 8, "grid_sky") != 0) { continue; }
					if (std::fabs(C.SkyIntensity - Skies[A]) < 1e-9
					    && std::fabs(C.SunIntensity - Suns[B]) < 1e-9) { ++Cells; break; }
				}
			}
		}
		for (size_t I = 0; I < S.Conditions.size(); ++I)
		{
			if (S.Conditions[I].Id.compare(0, 8, "grid_sky") == 0) { ++GridRows; }
		}
		Check(Cells == 12 && GridRows == 12,
		      "the grid is four skies crossed with three suns, twelve cells, none missing and none extra",
		      std::to_string(Cells) + " of 12 cells over " + std::to_string(GridRows) + " rows");
		// A1(a), BLOCKING: THE NULL CELL IS A DUPLICATE OR IT IS NOTHING.
		// Run 38 carried this test as ladder_sun003 against vign_camA_day and
		// IT FAILED, by 0.1106 of whole-frame mean luma, and nobody read it.
		// Asserted field by field here rather than by reading two rows of
		// JSON side by side.
		const LedgerVignette::Condition* Ref = 0;
		const LedgerVignette::Condition* Null = 0;
		for (size_t I = 0; I < S.Conditions.size(); ++I)
		{
			if (S.Conditions[I].Id == "grid_sky070_sun003") { Ref = &S.Conditions[I]; }
			if (S.Conditions[I].Id == "grid_null_repeat")    { Null = &S.Conditions[I]; }
		}
		Check(Ref != 0 && Null != 0,
		      "the grid has a reference cell and a null cell that repeats it");
		Check(Ref != 0 && Null != 0
		      && Null->Hdri == Ref->Hdri && Null->SunOn == Ref->SunOn
		      && Null->LanternsOn == Ref->LanternsOn && Null->WindowsOn == Ref->WindowsOn
		      && std::fabs(Null->SunIntensity - Ref->SunIntensity) < 1e-12
		      && std::fabs(Null->SkyIntensity - Ref->SkyIntensity) < 1e-12
		      && std::fabs(Null->Wetness - Ref->Wetness) < 1e-12
		      && std::fabs(Null->FogDensity - Ref->FogDensity) < 1e-12
		      && std::fabs(Null->FogMaxOpacity - Ref->FogMaxOpacity) < 1e-12,
		      "the null cell is the reference cell in every field that lights a frame",
		      "a null pair that differs in any input measures that difference and not the rig");
		// AND THE OTHER HALF OF THE SAME CLAIM, ADDED 2026-09-14 BY THE
		// RULING OF 18:23Z (game-design/decision-2026-09-14-ruling-the-null-
		// series-follows-the-judged-row.md): THE REFERENCE CELL IS THE JUDGED
		// DAY ROW. The check above proves the null cell repeats the reference
		// cell; nothing proved the reference cell was still the row Jafar
		// judges. It was not, from the moment overcast_day moved to
		// fog_max_opacity 0.100 and the five rows sharing its cell kept their
		// 9 September copies of 0.450, and the guard that went red was the one
		// at the far end of the file, one round trip later. ACCEPTING CASE
		// FIRST, then the planted rejection below.
		const LedgerVignette::Condition* JudgedDay = 0;
		for (size_t I = 0; I < S.Conditions.size(); ++I)
		{
			if (S.Conditions[I].Id == "overcast_day") { JudgedDay = &S.Conditions[I]; }
		}
		std::string RefDiff = "nothing measured: overcast_day or grid_sky070_sun003 is not in the spec";
		if (Ref != 0 && JudgedDay != 0) { RefDiff = RefCellAgainstJudged(*Ref, *JudgedDay); }
		Check(Ref != 0 && JudgedDay != 0 && RefDiff.empty(),
		      "the grid's reference cell is the judged day row in every field that lights a "
		      "frame, because the reference cell exists to carry the judged row's inputs and "
		      "a judged frame that is not in its own null series has walked out of the floor "
		      "that speaks for it",
		      RefDiff);
		// THE REJECTING CASE, PLANTED, so this is watched on every run and not
		// only on the night it was written (rule 5b). A copy of the parsed
		// reference cell with its fog set back to the 0.450 it carried before
		// the ruling: the comparison must refuse it, and must refuse it BY
		// NAMING fog_max_opacity, since a refusal for some other reason would
		// pass a check that had stopped reading the field it is about.
		std::string PlantedDiff = "nothing measured: no reference cell to plant into";
		if (Ref != 0 && JudgedDay != 0)
		{
			LedgerVignette::Condition Planted = *Ref;
			Planted.FogMaxOpacity = 0.450;
			PlantedDiff = RefCellAgainstJudged(Planted, *JudgedDay);
		}
		Check(PlantedDiff.rfind("fog_max_opacity ", 0) == 0,
		      "and the comparison refuses a reference cell planted back at the retired fog cap, "
		      "naming fog_max_opacity and both values",
		      PlantedDiff.empty() ? std::string("accepted a planted 0.450 as equal") : PlantedDiff);
		// AND THE FIELD THAT WENT STALE TONIGHT, PLANTED IN THE SAME SHAPE,
		// 2026-09-14 20:01Z. The plant above watches the field that went stale
		// at 18:23Z; this one watches the field that went stale two hours
		// later, when Jafar took sky 0.70 and the reference-cell role moved to
		// grid_sky070_sun003. A copy of the parsed reference cell with its sky
		// set back to the 1.00 it carried before: the comparison must refuse
		// it, and must name sky_intensity, because sky is compared before fog
		// and a refusal naming any other field would mean this guard had
		// stopped reading the field it is about.
		std::string SkyPlantedDiff = "nothing measured: no reference cell to plant into";
		if (Ref != 0 && JudgedDay != 0)
		{
			LedgerVignette::Condition SkyPlanted = *Ref;
			SkyPlanted.SkyIntensity = 1.00;
			SkyPlantedDiff = RefCellAgainstJudged(SkyPlanted, *JudgedDay);
		}
		Check(SkyPlantedDiff.rfind("sky_intensity ", 0) == 0,
		      "and the comparison refuses a reference cell planted back at the retired sky, "
		      "naming sky_intensity and both values",
		      SkyPlantedDiff.empty() ? std::string("accepted a planted 1.00 as equal")
		                             : SkyPlantedDiff);
		// C6, MECHANICALLY: THE SHOT ORDER RISES AND FALLS IN SKY. The
		// retired ladder rendered in increasing order, so a drift ordered by
		// shot was perfectly confounded with a response to the light.
		bool bRose = false, bFell = false;
		double PrevSky = -1.0;
		std::printf("    gridShotOrder:");
		for (size_t I = 0; I < S.Shots.size(); ++I)
		{
			if (S.Shots[I].ConditionId.compare(0, 8, "grid_sky") != 0) { continue; }
			double Sky = -1.0;
			for (size_t K = 0; K < S.Conditions.size(); ++K)
			{
				if (S.Conditions[K].Id == S.Shots[I].ConditionId)
				{
					Sky = S.Conditions[K].SkyIntensity;
				}
			}
			std::printf(" sky%.2f", Sky);
			if (PrevSky >= 0.0 && Sky > PrevSky + 1e-12) { bRose = true; }
			if (PrevSky >= 0.0 && Sky < PrevSky - 1e-12) { bFell = true; }
			PrevSky = Sky;
		}
		std::printf("\n");
		Check(bRose && bFell,
		      "the grid's shot order rises and falls in sky, so no drift ordered by shot passes as a sky response",
		      "rose and fell are both required, which is condition C6");
		// A4, THE FOG SERIES, AND A3, THE WETNESS SERIES.
		// SEVEN VALUES SINCE 2026-09-14, section 2.5 item 2 of the prune-and-fog
		// ruling, and the three added are the ones nothing has photographed: the
		// four rendered on 32bae70 read skyCentre 0.9268 / 0.8822 / 0.7979 /
		// 0.6222 and ground.p05 0.4617 / 0.3625 / 0.2532 / 0.0862 against the
		// sheet's 0.808 and 0.1935, so the sky crosses the sheet just above 0.100
		// while the dark end is still 0.060 over it, and the whole disagreement
		// between the two statistics lies inside 0.100 to 0.000.
		// THE ROW COUNT IS ASSERTED BESIDE THE VALUE COUNT: an eighth fog row
		// nobody named would otherwise ride in behind seven satisfied values.
		const double WantFog[7] = { 0.450, 0.250, 0.100, 0.080, 0.050, 0.020, 0.000 };
		int FogValues = 0, FogRows = 0;
		for (int A = 0; A < 7; ++A)
		{
			for (size_t I = 0; I < S.Conditions.size(); ++I)
			{
				if (S.Conditions[I].Id.compare(0, 9, "fog_maxop") != 0) { continue; }
				if (std::fabs(S.Conditions[I].FogMaxOpacity - WantFog[A]) < 1e-9)
				{
					++FogValues; break;
				}
			}
		}
		for (size_t I = 0; I < S.Conditions.size(); ++I)
		{
			if (S.Conditions[I].Id.compare(0, 9, "fog_maxop") == 0) { ++FogRows; }
		}
		Check(FogValues == 7 && FogRows == 7,
		      "seven fog rows at 0.450, 0.250, 0.100, 0.080, 0.050, 0.020 and 0.000, which is a "
		      "series across the bracket the sheet is crossed in and not a pair",
		      std::to_string(FogValues) + " of 7 asked values found over "
		      + std::to_string(FogRows) + " fog_maxop rows examined");
		// AND THE THREE SKY ROWS THAT CROSS THE NEW CAP, FIELD BY FIELD against
		// the judged day cell: a sky rung that also moved the wetness would
		// measure the wetness. The twelve-cell grid was shot with fog pinned at
		// 0.450, so this cross has never been rendered.
		{
			const LedgerVignette::Condition* Day = 0;
			for (size_t I = 0; I < S.Conditions.size(); ++I)
			{
				if (S.Conditions[I].Id == "overcast_day") { Day = &S.Conditions[I]; }
			}
			const double WantCrossSky[3] = { 0.35, 0.50, 0.70 };
			int CrossRows = 0, CrossMatching = 0, CrossSkies = 0;
			for (size_t I = 0; I < S.Conditions.size(); ++I)
			{
				const LedgerVignette::Condition& C = S.Conditions[I];
				if (C.Id.compare(0, 10, "fog010_sky") != 0) { continue; }
				++CrossRows;
				if (Day != 0 && C.Hdri == Day->Hdri && C.SunOn == Day->SunOn
				    && C.LanternsOn == Day->LanternsOn && C.WindowsOn == Day->WindowsOn
				    && std::fabs(C.SunIntensity - Day->SunIntensity) < 1e-12
				    && std::fabs(C.Wetness - Day->Wetness) < 1e-12
				    && std::fabs(C.FogDensity - Day->FogDensity) < 1e-12
				    && std::fabs(C.ExposurePin - Day->ExposurePin) < 1e-12
				    && std::fabs(C.FogMaxOpacity - 0.100) < 1e-12) { ++CrossMatching; }
			}
			for (int A = 0; A < 3; ++A)
			{
				for (size_t I = 0; I < S.Conditions.size(); ++I)
				{
					if (S.Conditions[I].Id.compare(0, 10, "fog010_sky") != 0) { continue; }
					if (std::fabs(S.Conditions[I].SkyIntensity - WantCrossSky[A]) < 1e-9)
					{
						++CrossSkies; break;
					}
				}
			}
			Check(CrossRows == 3 && CrossMatching == 3 && CrossSkies == 3,
			      "three sky rows cross the new fog cap at 0.35, 0.50 and 0.70, each the judged "
			      "day cell in every field but the sky it moves",
			      std::to_string(CrossRows) + " rows, " + std::to_string(CrossMatching)
			      + " matching the judged cell at fog 0.100, " + std::to_string(CrossSkies)
			      + " of 3 asked sky values found");
		}
		const double WantWet[3] = { 0.0, 0.60, 1.0 };
		int WetRows = 0;
		for (int A = 0; A < 3; ++A)
		{
			for (size_t I = 0; I < S.Conditions.size(); ++I)
			{
				if (S.Conditions[I].Id.compare(0, 4, "wet_") != 0) { continue; }
				if (std::fabs(S.Conditions[I].Wetness - WantWet[A]) < 1e-9) { ++WetRows; break; }
			}
		}
		Check(WetRows == 3,
		      "three wetness rows at 0.0, 0.60 and 1.0, both ends and the value the judged rows carry",
		      std::to_string(WetRows) + " of 3");

		// ---- WHICH WETNESS THE BIND CHOOSES, ON THE LIVE FILE ----------
		// ACCEPTING CASE FIRST AND THE LIVE SPEC IS THE FIXTURE, which is
		// this project's rule for anything that checks the project itself.
		{
			const LedgerSurface::WetnessChoice W =
				LedgerSurface::WetnessForBind(S);
			std::printf("    wetnessForBind: value=%.4f from=%s/%s shots=%d/%d "
			            "conds=%d/%d\n", W.Value, W.FromCondition.c_str(),
			            W.Why, W.ShotsAtValue, W.ShotsExamined,
			            W.CondsAtValue, W.CondsExamined);
			Check(!W.FromCondition.empty() && W.FromCondition != "none",
			      "the choice NAMES the condition it came from, so a value on "
			      "the verdict line can be traced to a row of the shared file",
			      W.FromCondition);
			Check(!S.Shots.empty()
			      && W.FromCondition == S.Shots[0].ConditionId
			      && std::string(W.Why) == std::string("first-shot-condition"),
			      "on the committed file the bind takes the FIRST SHOT'S "
			      "condition, which is the interactive path's own rule at "
			      "VignetteShot.cpp:4420 rather than a second opinion about "
			      "which condition is the street's",
			      W.FromCondition + "/" + W.Why);
			Check(W.ShotsExamined == (int)S.Shots.size()
			      && W.CondsExamined == (int)S.Conditions.size()
			      && W.ShotsAtValue > 0 && W.ShotsAtValue <= W.ShotsExamined,
			      "and every count ships the denominator it was taken over: "
			      "shots examined is the shot list and conditions examined is "
			      "the condition list",
			      std::to_string(W.ShotsAtValue) + "/"
			      + std::to_string(W.ShotsExamined));
			// THE COMPROMISE IS A NUMBER AND NOT A WORD. A static bind is
			// wrong for every shot whose condition carries a different
			// wetness, and the gap is what a reader needs to size it.
			Check(W.ShotsAtValue < W.ShotsExamined,
			      "the committed file HAS shots at another wetness, so this "
			      "reading is not a tautology: the static bind is right for "
			      "some and wrong for the rest, and the line says how many",
			      std::to_string(W.ShotsExamined - W.ShotsAtValue)
			      + " shot(s) at another wetness");
		}
	}

	// REJECTING CASE, SYNTHESISED FROM THE LIVE FILE BY DELETING ONE KEY,
	// so the fixture cannot drift from the accepting case above. A
	// condition with no sun_intensity must stop the parse and NAME the
	// key: a silent default is the fault queue 205 repairs, and the value
	// it would fall back on was tuned against three fills that no longer
	// exist.
	{
		const std::string Key = "\"sun_intensity\":";
		const size_t At = Text.find(Key);
		Check(At != std::string::npos,
		      "the committed piece list carries sun_intensity at all, so the deletion below bites");
		if (At != std::string::npos)
		{
			size_t End = Text.find(',', At);
			std::string Broken = Text;
			if (End != std::string::npos) { Broken.erase(At, End - At + 1); }
			LedgerVignette::Spec B;
			std::string BErr;
			const bool BParsed = LedgerVignette::ParseSpec(Broken, B, BErr);
			std::printf("    rejecting: parsed=%s err=%s\n",
			            BParsed ? "yes" : "no", BErr.c_str());
			Check(!BParsed && BErr.find("sun_intensity") != std::string::npos,
			      "REJECTING CASE - a condition with no sun_intensity refuses and names the key",
			      BErr.empty() ? "(no error raised)" : BErr);
		}
	}

	// AND THE SAME RUNG FOR sky_intensity, BECAUSE A REQUIRED FIELD NOT
	// PROVEN REQUIRED IS A DEFAULTED FIELD. The parse calls NeedNum on
	// both, and only one of the two had a rejecting case until this rung.
	//
	// CUT FROM THE COMMA BEFORE IT, NOT TO THE COMMA AFTER IT, and the
	// difference decides what this proves: sky_intensity is the LAST key
	// of its object, so a cut forward to the next comma would take the
	// closing brace with it and the parse would then refuse the SHAPE
	// rather than the missing key. The check below would still pass and
	// would be about the wrong thing.
	{
		const std::string Key = "\"sky_intensity\":";
		const size_t At = Text.find(Key);
		Check(At != std::string::npos,
		      "the committed piece list carries sky_intensity at all, so the deletion below bites");
		if (At != std::string::npos)
		{
			const size_t Cut = Text.rfind(',', At);
			const size_t End = Text.find_first_of(",}", At);
			std::string Broken = Text;
			if (Cut != std::string::npos && End != std::string::npos && End > Cut)
			{
				Broken.erase(Cut, End - Cut);
			}
			Check(Broken.size() < Text.size(),
			      "the sky_intensity fixture actually removed something, so the check below is not vacuous");
			LedgerVignette::Spec B;
			std::string BErr;
			const bool BParsed = LedgerVignette::ParseSpec(Broken, B, BErr);
			std::printf("    rejecting: parsed=%s err=%s\n",
			            BParsed ? "yes" : "no", BErr.c_str());
			Check(!BParsed && BErr.find("sky_intensity") != std::string::npos,
			      "REJECTING CASE - a condition with no sky_intensity refuses and names the key",
			      BErr.empty() ? "(no error raised)" : BErr);
		}
	}

	// ROLL, WHICH IS THE FIELD A READER LOSES WITHOUT CHANGING A COUNT.
	int Rolled = 0, Pitched = 0, Yawed = 0;
	for (size_t I = 0; I < S.Pieces.size(); ++I)
	{
		if (std::fabs(S.Pieces[I].RollDeg)  > 1e-9) ++Rolled;
		if (std::fabs(S.Pieces[I].PitchDeg) > 1e-9) ++Pitched;
		if (std::fabs(S.Pieces[I].YawDeg)   > 1e-9) ++Yawed;
	}
	std::printf("    rotations: rolled=%d pitched=%d yawed=%d multi=%d of %d pieces\n",
	            Rolled, Pitched, Yawed,
	            LedgerVignette::MultiRotationCount(S.Pieces), (int)S.Pieces.size());
	Check(Rolled > 0,
	      "roll survived the read, so the rolled cylinders will lie down rather than stand up",
	      "rolled=0 of the file's own nine");
	Check(LedgerVignette::MultiRotationCount(S.Pieces) == S.HeaderMultiRotation,
	      "the reader counts the same multi-rotation pieces the file's header claims",
	      "reader disagrees with counts.multi_rotation");
	// AT ZERO THE EULER COMPOSITION ORDER IS UNEXERCISED, which is the only
	// reason this engine may compose in whatever order its API prefers. The
	// day it stops being zero the emitter owes a statement of what the pair
	// meant before either engine is trusted with it.
	Check(S.HeaderMultiRotation == 0,
	      "no piece carries two rotations at once, so composition order cannot differ between engines",
	      "multi_rotation is no longer zero: the emitter's rotation order is now load-bearing");

	int Boxes = LedgerVignette::ShapeCount(S.Pieces, "box");
	int Cyls  = LedgerVignette::ShapeCount(S.Pieces, "cyl");
	int Mesh  = LedgerVignette::ShapeCount(S.Pieces, "mesh");
	int Decal = LedgerVignette::ShapeCount(S.Pieces, "decal");
	std::printf("    shapes: box=%d cyl=%d mesh=%d decal=%d unknown=%d of %d\n",
	            Boxes, Cyls, Mesh, Decal,
	            (int)S.Pieces.size() - Boxes - Cyls - Mesh - Decal, (int)S.Pieces.size());
	Check(Boxes + Cyls + Mesh + Decal == (int)S.Pieces.size(),
	      "every piece has a shape this emitter knows how to stand up",
	      "some piece carries a shape string the emitter would silently skip");

	// THE LAMP AND THE PRACTICALS, INCLUDING THE COLOUR SPACE.
	std::printf("    lantern: space=%s rgb=%.4f/%.4f/%.4f range=%.2f intensity=%.2f emissive=%d\n",
	            S.Lantern.ColourSpace.c_str(), S.Lantern.R, S.Lantern.G, S.Lantern.B,
	            S.Lantern.RangeM, S.Lantern.Intensity,
	            LedgerVignette::EmissiveCount(S.Pieces));
	Check(S.Lantern.ColourSpace == "gamma-sRGB",
	      "the lamp colour names the space it is in, so the conversion has something to be checked against",
	      S.Lantern.ColourSpace);
	Check(LedgerVignette::EmissiveCount(S.Pieces) > 0,
	      "there are emissive pieces to hang the lanterns on");
	std::printf("    practicals: space=%s lit=%d/%d flatLit=%d/%d shopIntensity=%.2f\n",
	            S.Windows.ColourSpace.c_str(), (int)S.Windows.LitNames.size(),
	            S.Windows.ShopCards, (int)S.Windows.FlatLitNames.size(),
	            S.Windows.FlatCards, S.Windows.ShopIntensity);
	Check((int)S.Windows.LitNames.size() == 3 && S.Windows.ShopCards == 6,
	      "the file lights three of the six shop interiors and this reader sees the names",
	      "the practicals block did not read back as three of six");
	Check(S.Windows.FlatLitNames.empty() && S.Windows.FlatCards == 0,
	      "the flat practicals light nothing today and the reader carries the empty list rather than a default");
	// EVERY NAME THE FILE ASKS TO BE LIT MUST NAME A PIECE. A name that
	// matched nothing would light nothing and the count would be right by
	// accident, which is the failure the Unity host had before queue 040.
	int Matched = 0;
	for (size_t I = 0; I < S.Windows.LitNames.size(); ++I)
		for (size_t J = 0; J < S.Pieces.size(); ++J)
			if (S.Pieces[J].Name == S.Windows.LitNames[I]) { ++Matched; break; }
	Check(Matched == (int)S.Windows.LitNames.size(),
	      "every name in lit_names is a piece in this file, so no practical can be asked for and never placed",
	      "matched fewer names than the file lists");

	// THE CAMERAS, AND THE GROUND UNDER THEM THAT THIS ENGINE MUST NOT
	// RE-DERIVE. Both cameras stand on a footway that falls 1 in 40, so the
	// two ground levels differ and a shared constant would be wrong for one.
	for (size_t I = 0; I < S.Cameras.size(); ++I)
	{
		const LedgerVignette::Camera& C = S.Cameras[I];
		std::printf("    camera %s: x=%.2f z=%.2f groundFound=%d groundY=%.4f on=%s eye=%.4f fovV=%.1f fovH=%.1f\n",
		            C.Id.c_str(), C.X, C.Z, (int)C.GroundFound, C.GroundY,
		            C.GroundEdge.c_str(), C.GroundY + C.EyeHeightM, C.FovVerticalDeg,
		            LedgerVignette::HorizontalFovDeg(C.FovVerticalDeg, 1280, 720));
		Check(C.GroundFound,
		      "the file found ground under this camera, so the eye height has a datum to sit on",
		      C.Id + " ground_found=false");
	}

	// THE FOV CONVERSION, WHICH IS THE TRAP. Unity's fieldOfView is
	// vertical; Unreal's is horizontal. At 16:9 a vertical 60 is a
	// horizontal 91.5, and handing 60 to Unreal would photograph a
	// different street from a third of the width.
	const double HFov = LedgerVignette::HorizontalFovDeg(60.0, 1280, 720);
	std::printf("    fov: vertical=60.0 horizontal=%.2f at 1280x720\n", HFov);
	Check(HFov > 91.0 && HFov < 92.0,
	      "a vertical 60 at 16:9 converts to a horizontal 91.5, not to 60",
	      "conversion produced something else");
	Check(std::fabs(LedgerVignette::HorizontalFovDeg(60.0, 100, 100) - 60.0) < 1e-9,
	      "and at 1:1 the two are the same number, which is the case that would hide a broken conversion");

	// THE SUN. The two engines derive the same direction two ways and the
	// pair of yaws differs by exactly 90 degrees under this frame's own
	// conventions; asserting the relationship is what makes the pair a
	// check rather than two independent guesses.
	const double UeYaw = LedgerVignette::SunYawDeg(S.SunAzimuthDeg);
	const double UnityYaw = LedgerVignette::UnitySunYawDeg(S.SunAzimuthDeg);
	std::printf("    sun: elevation=%.1f azimuth=%.1f ueYaw=%.1f unityYaw=%.1f\n",
	            S.SunElevationDeg, S.SunAzimuthDeg, UeYaw, UnityYaw);
	Check(std::fabs(S.SunElevationDeg - 36.0) < 1e-9,
	      "the sun elevation is the file's, not a default");
	// THE TWO ENGINES' YAWS ARE ONE DIRECTION SAID TWICE, and the identity
	// between them is what makes the pair a check. A facing at bearing b is
	// Unity yaw 90-b and this engine's yaw b, so the two must differ by
	// exactly that. Without this, both conversions could be wrong in the
	// same way and every frame would agree with every other frame.
	Check(std::fabs(LedgerVignette::Wrap360(90.0 - UnityYaw) - UeYaw) < 1e-9,
	      "the two engines' sun yaws are the same bearing expressed twice, not two guesses",
	      "ue and unity yaws do not satisfy ueYaw = 90 - unityYaw");
	Check(std::fabs(LedgerVignette::SunPitchDeg(S.SunElevationDeg) + S.SunElevationDeg) < 1e-9,
	      "a sun above the horizon sends its light below it");

	// THE COLOUR CONVERSION, ON BOTH ENDS AND IN THE MIDDLE.
	Check(std::fabs(LedgerVignette::SrgbToLinear(0.0) - 0.0) < 1e-12
	      && std::fabs(LedgerVignette::SrgbToLinear(1.0) - 1.0) < 1e-12,
	      "gamma to linear fixes both ends exactly");
	Check(std::fabs(LedgerVignette::SrgbToLinear(0.8573) - 0.7055) < 5e-4,
	      "and the lantern's own gamma green converts to the linear green the scene file states beside it",
	      "the scene file says linear_srgb 0.7055 for gamma 0.8573");
	Check(LedgerVignette::SrgbToLinear(0.5) < 0.5,
	      "a mid grey darkens, which is the direction that catches the conversion being applied backwards");

	// THE MEDIAN, INCLUDING THE CASE THAT MUST NOT READ AS A FAST FRAME.
	std::vector<double> Ms;
	Check(LedgerVignette::MedianMs(Ms) < 0.0,
	      "a timing that never ran reports a negative rather than a zero millisecond frame");
	Ms.push_back(10.0); Ms.push_back(1.0); Ms.push_back(100.0);
	Check(std::fabs(LedgerVignette::MedianMs(Ms) - 10.0) < 1e-9,
	      "an odd series takes the middle value and is not dragged by the outlier",
	      "a mean would read 37");
	Ms.push_back(11.0);
	Check(std::fabs(LedgerVignette::MedianMs(Ms) - 10.5) < 1e-9,
	      "an even series averages the middle pair");

	// THE STRINGS, CHECKED FOR THE FAULT THAT TRUNCATES EVERY READER.
	const std::string Line = LedgerVignette::ShotLine(
		"vign_camA_day", "cam_A", "overcast_day", 1.5723, "east_footway",
		12.34, 24, 8, 1280, 720, 60.0, 91.49, 240000, "WROTE",
		"ue-vign_camA_day.png", "none");
	std::printf("    %s\n", Line.c_str());
	Check(Line.find("frameMedianMs=12.34/of=24warm8") != std::string::npos,
	      "the shot line says the frame time is a median and of how many frames", Line);
	Check(Line.find(": ") == std::string::npos,
	      "the shot line carries no colon-space that would read as prose");
	size_t Sp = Line.find("shot ");
	Check(Sp != std::string::npos, "the shot line is prefixed so a reader can find it");
	// NO VALUE MAY CONTAIN A SPACE. Split on whitespace and every token
	// carrying an '=' must have a non-empty right hand side.
	{
		std::istringstream Toks(Line);
		std::string T;
		int Pairs = 0, Bad = 0;
		while (Toks >> T)
		{
			const size_t Eq = T.find('=');
			if (Eq == std::string::npos) continue;
			++Pairs;
			if (Eq + 1 >= T.size()) ++Bad;
		}
		std::printf("    shot line: keyValuePairs=%d emptyValues=%d/%d\n", Pairs, Bad, Pairs);
		Check(Pairs >= 10 && Bad == 0,
		      "every key on the shot line carries a value with no space in it");
	}
	const std::string Scene = LedgerVignette::SceneLine(S, S.HeaderPieces, 404, 146, 20,
	                                                    23, 20, 4, 3, 0, "none");
	std::printf("    %s\n", Scene.c_str());
	Check(Scene.find("sceneStatus=WHOLE") != std::string::npos,
	      "a scene that stood up everything the file asked for says WHOLE", Scene);
	Check(Scene.find("flatsLit=0/0 nothing-to-light") != std::string::npos,
	      "and the flat practicals say the words rather than printing a bare zero", Scene);
	const std::string ScenePartial = LedgerVignette::SceneLine(S, 0, 0, 0, 0, 0, 0, 0, 0,
	                                                           S.HeaderPieces, "spawn-refused");
	Check(ScenePartial.find("sceneStatus=NOTHING-EMITTED") != std::string::npos,
	      "a scene that stood up nothing says so rather than reporting a whole street of zeros",
	      ScenePartial);
	const std::string Done = LedgerVignette::CaptureDoneLine(0, 0, 0, 0, 0.0, 0);
	Check(Done.find("captureStatus=NOTHING-MEASURED") != std::string::npos,
	      "a capture that photographed nothing says the words", Done);
	const std::string DonePart = LedgerVignette::CaptureDoneLine(2, 4, 1, 1, 31.5, 900);
	std::printf("    %s\n", DonePart.c_str());
	Check(DonePart.find("shotsWrote=2/4") != std::string::npos
	      && DonePart.find("captureStatus=PARTIAL") != std::string::npos,
	      "and a partial capture carries every count over its denominator", DonePart);

	// ---- THE MESH ROUTE'S SEGMENT, BOTH HALVES, BOTH DIRECTIONS ---------
	//
	// WHY THESE ROWS EXIST, amendments A5 and A6 of the ruling of
	// 2026-09-08, queue 161 and 162. The street side's collision reading and
	// its string were built in VignetteShot.cpp, which this container cannot
	// compile, so they shipped UNRUN and three faults rode in them for three
	// landed runs. Everything they assert now runs here with g++ before any
	// dispatch.
	//
	// ACCEPTING CASE FIRST, EVERY TIME, and the planted cases second. The
	// live committed street is the accepting fixture for the burial half; the
	// rejecting and the planted fixtures are built in this file, because a
	// repository with a prop sunk in the road on purpose is not one anybody
	// wants, and because a guard pinned to a real asset's current fault goes
	// RED THE DAY THE ASSET IS FIXED. So the live street's burial numbers are
	// PRINTED here as a series and never asserted as a verdict; the verdicts
	// are asserted on boxes this file makes and nobody can repair.
	{
		using namespace LedgerVignette;

		// A. THE CLASSIFIER. Accepting case first: an asset with a body setup
		// and one simple primitive is the case the importer was built to
		// produce and the one a capsule is stopped by.
		Check(ReadPropCollision(true, 1, false, true) == PropCollision_Yes,
		      "ACCEPTING CASE - a body setup with a simple primitive reads YES");
		Check(ReadPropCollision(true, 6, false, true) == PropCollision_Yes,
		      "and so does one with six of them");
		// THE FAULT A5 WAS RAISED FOR. A mesh collidable by a
		// complex-as-simple trace flag holds ZERO aggregate elements and
		// stops a capsule perfectly. The count said 0 and the old key called
		// that no collision.
		Check(ReadPropCollision(true, 0, true, true) == PropCollision_Yes,
		      "a body setup with ZERO primitives and complex-as-simple over real "
		      "geometry reads YES");
		Check(ReadPropCollision(true, 0, true, true) != PropCollision_No,
		      "and the same reading is NOT NO, which is what a count of primitives "
		      "called it for three runs");
		// AND THE OTHER HALF OF A5. No body setup is a question nobody
		// answered, not an answer of no.
		Check(ReadPropCollision(false, 0, false, true) == PropCollision_Unknown,
		      "no body setup reads UNKNOWN");
		Check(ReadPropCollision(false, 0, false, true) != PropCollision_No,
		      "and NOT NO, whatever the primitive count beside it says");
		Check(ReadPropCollision(false, 3, true, true) == PropCollision_Unknown,
		      "no body setup is still UNKNOWN even when the other three inputs "
		      "would each have said yes, because there is nothing for them to be "
		      "true of");
		// THE REAL NO, WHICH IS THE CASE THE WHOLE THREE-VALUED READING
		// EXISTS TO LEAVE ROOM FOR. A guard that can only say YES and
		// UNKNOWN is a ratchet.
		Check(ReadPropCollision(true, 0, false, true) == PropCollision_No,
		      "a body setup holding nothing, with no complex-as-simple flag, reads NO");
		Check(ReadPropCollision(true, 0, true, false) == PropCollision_No,
		      "and complex-as-simple over a mesh with NO EXTENT reads NO, because a "
		      "flag pointing at nothing stops nothing");
		// A REFUSED COUNT IS NOT A ZERO. The importer printed
		// propCollisionPrims=0/15 over fifteen refusals and the zero was the
		// lie, not the minus one.
		Check(ReadPropCollision(true, -1, false, true) == PropCollision_Unknown,
		      "a refused primitive count reads UNKNOWN and never NO");
		Check(std::string(PropCollisionWord(PropCollision_Yes)) == "YES"
		      && std::string(PropCollisionWord(PropCollision_No)) == "NO"
		      && std::string(PropCollisionWord(PropCollision_Unknown)) == "UNKNOWN",
		      "and the three words are the three words");

		// B. THE TALLY AND THE STRING. A run with one of each.
		PropSegmentIn In;
		In.MeshPiecesInFile = ShapeCount(S.Pieces, "mesh");
		In.PackageDir = "/Game/Ledger/Props";
		In.NamePrefix = "SM_";
		In.PlacedAsMesh = 3;
		In.PlacedAsBox = In.MeshPiecesInFile - 3;
		In.FellBackOn.push_back("prop_pallet_0=no-uasset-for-pallet");
		In.CentreWorstMm = 0.47; In.CentreWorstOn = "prop_drainage_grate_01_0";
		In.SizeWorstMm = 44.02; In.SizeWorstOn = "prop_wooden_crate_01_0";
		In.SizeComparable = 3;
		In.bInteractive = true;
		In.Collision.Add("prop_drainage_grate_01_0", PropCollision_Yes);
		In.Collision.Add("prop_pavement_sign_0", PropCollision_No);
		In.Collision.Add("prop_skip_0", PropCollision_Unknown);
		const std::string Seg3 = PropMeshSegment(In);
		std::printf("    %s\n", Seg3.c_str());
		Check(Seg3.find("propPlacedWithCollision=1/3") != std::string::npos,
		      "the placed-with-collision count ships the readings TAKEN as its "
		      "denominator, not the 23 the file asked for", Seg3);
		Check(Seg3.find("propPlacedCollisionUnread=1/3") != std::string::npos,
		      "the unread count ships the same denominator, on the same line, at "
		      "the same instant", Seg3);
		Check(Seg3.find("propPlacedCollisionNoOn=prop_pavement_sign_0") != std::string::npos,
		      "and the piece that read NO is NAMED, because a count cannot be fixed "
		      "and a name can", Seg3);
		Check(Seg3.find("propPlacedCollisionStat=placed-prop-mesh-components-whose-asset-"
		                "reports-collision/over-placed-prop-meshes/PROXY-only-a-sweep-"
		                "answers-whether-a-capsule-is-stopped") != std::string::npos,
		      "the stat names the population AND carries PROXY, because only a sweep "
		      "answers whether a capsule is stopped and this reads an asset", Seg3);
		// A9 OF THE RULING OF 2026-09-09: THE DIVERGENCE ON THE LINE WHERE THE
		// NUMBERS MEET. The importer calls a missing body setup NO over saved
		// assets; this side calls it UNKNOWN over assets loaded at runtime,
		// ruled 2026-09-08. A reader holding both files saw two words for one
		// case and could not tell a decision from a bug, so the decision rides
		// the value and not a header comment twelve hundred lines away.
		Check(Seg3.find("/a-missing-body-setup-reads-UNKNOWN-here-and-NO-in-"
		                "import_prop_meshes.py/ruled-2026-09-08/two-populations-at-"
		                "two-times/never-added-never-differenced") != std::string::npos,
		      "the stat names the RULED DIVERGENCE with the importer, in its own "
		      "value, where a reader meets the number", Seg3);
		Check(Seg3.find("propPlacedCollisionStat=") != std::string::npos
		      && Seg3.find("UNKNOWN-here-and-NO-in-import_prop_meshes.py")
		         > Seg3.find("propPlacedCollisionStat="),
		      "and it rides propPlacedCollisionStat rather than a second key, so the "
		      "two tallies are never printed as a pair without their populations",
		      Seg3);
		// THE RENAME, WHICH IS HALF OF A5. The old key counted MESHES under a
		// name that said PRIMS and collided with a key of the same name that
		// tools/ue/import_prop_meshes.py emits over a different population.
		// A SYNTHETIC REJECTING FIXTURE: these two strings now exist nowhere
		// in this segment, so doing the work this tool prompts cannot break it.
		Check(Seg3.find("propCollisionPrims") == std::string::npos,
		      "REJECTING CASE - the old propCollisionPrims name is gone from the "
		      "street side, so it cannot collide with the importer's key of the "
		      "same name over a different population", Seg3);
		Check(Seg3.find("propCollisionEnabled") == std::string::npos,
		      "REJECTING CASE - propCollisionEnabled is gone too: it restated the "
		      "bool that set it and could not fail", Seg3);
		Check(Seg3.find("propCollisionAsked=QueryOnly/the-walk-path/NOT-A-MEASUREMENT-"
		                "restates-bInteractive") != std::string::npos,
		      "what is left of it says in its own value that it is not a measurement, "
		      "and still tells a reader which path built the street", Seg3);
		// THE ZERO DENOMINATOR, WHICH IS THE OTHER HALF OF A5. The last
		// landed walk run printed propCollisionPrims=0/0 with
		// propCollisionUnread=0 beside it.
		PropSegmentIn None;
		None.MeshPiecesInFile = ShapeCount(S.Pieces, "mesh");
		None.PackageDir = "/Game/Ledger/Props";
		None.NamePrefix = "SM_";
		None.PlacedAsBox = None.MeshPiecesInFile;
		const std::string SegNone = PropMeshSegment(None);
		std::printf("    %s\n", SegNone.c_str());
		Check(SegNone.find("propPlacedWithCollision=nothing-measured/0") != std::string::npos,
		      "a run that placed no prop mesh PRINTS THE WORDS nothing measured "
		      "rather than a zero over a zero", SegNone);
		Check(SegNone.find("propPlacedCollisionUnread=nothing-measured/0") != std::string::npos,
		      "and so does the unread count, which used to print a bare 0 with no "
		      "denominator at all", SegNone);
		Check(SegNone.find("propPlacedWithCollision=0/0") == std::string::npos,
		      "REJECTING CASE - 0/0 cannot appear on that key, because a clean "
		      "result and a result that examined nothing must not read alike",
		      SegNone);
		// THE CAP ON THE NAMED LIST, BOTH WAYS ROUND.
		PropSegmentIn Many = In;
		Many.Collision = PropCollisionTally();
		for (int I = 0; I < 5; ++I)
		{
			char N[64];
			std::snprintf(N, sizeof(N), "prop_synthetic_%d", I);
			Many.Collision.Add(N, PropCollision_No);
		}
		const std::string SegMany = PropMeshSegment(Many);
		Check(SegMany.find("propPlacedCollisionNoOn=prop_synthetic_0;prop_synthetic_1;"
		                   "prop_synthetic_2;prop_synthetic_3;(+1~more~not~shown)")
		      != std::string::npos,
		      "a cap that BITES announces itself and says how many it withheld",
		      SegMany);
		Check(Seg3.find("propPlacedCollisionNoOn=prop_pavement_sign_0 ") != std::string::npos,
		      "and the same cap, NOT biting on one name, says nothing at all about a "
		      "cap", Seg3);
		// THE IDENTITY BETWEEN TWO COUNTERS IN TWO DIFFERENT FILES, both ways
		// round. Every placed prop mesh is asked exactly once, so the
		// readings taken and the meshes placed are one number; they are kept
		// by two counters in VignetteShot.cpp and a silent disagreement
		// between them is what makes a denominator a lie.
		Check(Seg3.find("propCollisionReadingsMismatch") == std::string::npos,
		      "ACCEPTING CASE - three readings over three placed meshes prints no "
		      "mismatch key at all", Seg3);
		Check(Seg3.find("propPlacedCollisionUnknownOn=prop_skip_0") != std::string::npos,
		      "the piece that read UNKNOWN is named too, in its own key, because a "
		      "NO is an asset to fix and an UNKNOWN is a reading to chase", Seg3);
		Check(SegNone.find("propPlacedCollisionUnknownOn=none") != std::string::npos,
		      "and a run with no readings at all says none there rather than naming "
		      "a piece nobody asked about", SegNone);
		PropSegmentIn Off = In;
		Off.PlacedAsMesh = 4;
		Check(PropMeshSegment(Off).find(
		          "propCollisionReadingsMismatch=readings=3/meshesPlaced=4")
		      != std::string::npos,
		      "PLANTED CASE - one reading short of the meshes placed says so, with "
		      "both numbers, rather than printing a denominator nobody asked",
		      PropMeshSegment(Off));

		// C. THE BURIAL HALF, PLANTED FIRST BECAUSE THE VERDICTS LIVE HERE.
		// A LADDER OF TWO RUNGS, ONE CONTRIBUTOR TOGGLED, SAME VANTAGE, SAME
		// RUN: the identical prop read under an open sky and then under a
		// slab. The difference between the rungs is the reading.
		std::vector<PlacedBox> Lad;
		PlacedBox Prop;
		Prop.Name = "prop_planted_0"; Prop.Edge = "planted_edge"; Prop.Region = "x00_06";
		Prop.bProp = true; Prop.bFromAsset = true;
		Prop.MinX = 1.8; Prop.MaxX = 2.2; Prop.MinY = -0.10; Prop.MaxY = -0.085;
		Prop.MinZ = 2.6; Prop.MaxZ = 3.0;
		Lad.push_back(Prop);
		std::vector<BurialRead> Rung1 = ReadBurials(Lad);
		Check(Rung1.size() == 1 && Rung1[0].Cells == BurialGridSide() * BurialGridSide(),
		      "ACCEPTING CASE - a prop with nothing over it is still EXAMINED, and "
		      "says how many cells it examined");
		Check(Rung1.size() == 1 && Rung1[0].Buried == 0 && Rung1[0].Open == Rung1[0].Cells,
		      "and it reads every cell OPEN, which is what a correctly placed prop "
		      "on an open street must read");
		// RUNG 2: one slab added, nothing else changed, and it STRADDLES the
		// prop's top the way ground_east_channel straddles the grate's.
		PlacedBox Slab;
		Slab.Name = "planted_slab"; Slab.Edge = "planted_edge"; Slab.Region = "x00_06";
		Slab.MinX = 0.0; Slab.MaxX = 42.0; Slab.MinY = -0.37; Slab.MaxY = -0.0718;
		Slab.MinZ = 2.6; Slab.MaxZ = 3.0;
		Lad.push_back(Slab);
		std::vector<BurialRead> Rung2 = ReadBurials(Lad);
		std::printf("    ladder: rung1 buried=%d/%d open=%d  rung2 buried=%d/%d "
		            "deepestMm=%.2f by=%s\n",
		            Rung1[0].Buried, Rung1[0].Cells, Rung1[0].Open,
		            Rung2[0].Buried, Rung2[0].Cells, Rung2[0].DeepestMm,
		            Rung2[0].DeepestBy.c_str());
		Check(Rung2.size() == 1 && Rung2[0].Buried == Rung2[0].Cells
		      && Rung2[0].FullyBuried(),
		      "PLANTED CASE - the same prop under a slab that straddles its top "
		      "reads every cell BURIED");
		Check(Rung2.size() == 1 && Rung2[0].DeepestBy == "planted_slab"
		      && Rung2[0].DeepestMm > 13.0 && Rung2[0].DeepestMm < 13.5,
		      "the covering piece is NAMED and the depth is the millimetres it "
		      "would have to rise to clear it");
		Check(Rung1[0].Buried != Rung2[0].Buried,
		      "and the two rungs DIFFER, which is the only thing a ladder measures: "
		      "a rung that reads the same under both is measuring neither");
		// THE PREDICATE IS STRADDLE AND NOT ANYTHING-ABOVE, which is the
		// difference between a buried grate and a prop under an awning.
		std::vector<PlacedBox> Awn;
		Awn.push_back(Prop);
		PlacedBox Over = Slab;
		Over.Name = "planted_awning";
		Over.MinY = -0.0800; Over.MaxY = 2.95;
		Awn.push_back(Over);
		std::vector<BurialRead> Hung = ReadBurials(Awn);
		std::printf("    overhead: buried=%d/%d overhung=%d open=%d headroomMm=%.2f by=%s\n",
		            Hung[0].Buried, Hung[0].Cells, Hung[0].Overhung, Hung[0].Open,
		            Hung[0].HeadroomMm, Hung[0].HeadroomBy.c_str());
		Check(Hung[0].Buried == 0 && Hung[0].Overhung == Hung[0].Cells,
		      "PLANTED CASE - a piece entirely ABOVE the prop's top reads OVERHUNG "
		      "and not buried, so an awning cannot print as a burial");
		Check(Hung[0].HeadroomMm > 4.9 && Hung[0].HeadroomMm < 5.1
		      && Hung[0].HeadroomBy == "planted_awning",
		      "and the gap to it is measured in millimetres with the piece named, "
		      "because five millimetres of daylight is the whole difference");
		// AND THE THREE BUCKETS ARE A PARTITION, which is the arithmetic a
		// reader of three percentages is entitled to assume.
		bool bPartition = true;
		for (size_t I = 0; I < Hung.size(); ++I)
		{
			if (Hung[I].Buried + Hung[I].Overhung + Hung[I].Open != Hung[I].Cells)
			{
				bPartition = false;
			}
		}
		Check(bPartition,
		      "buried plus overhung plus open is every cell examined and not one more");

		// D. THE LIVE STREET, WHICH IS THE ACCEPTING FIXTURE, PRINTED AND
		// NOT JUDGED. These are the numbers the next walk run will print,
		// taken here off the FILE rather than off the engine's placement, so
		// the two can be compared when the run lands. No assertion below
		// says the street is correct: a guard that goes red when the street
		// spec is FIXED is a ratchet, and A6 is a measurement order, not a
		// bound.
		std::vector<PlacedBox> Live;
		for (size_t I = 0; I < S.Pieces.size(); ++I)
		{
			Live.push_back(SpecBoxBounds(S.Pieces[I]));
		}
		// WORST FIRST, THROUGH THE HEADER'S OWN SORTER, so this printed series
		// and the propBuriedOn key under it are in one order and not two.
		const std::vector<BurialRead> LiveReads = SortedBurials(ReadBurials(Live));
		// A8 OF THE RULING OF 2026-09-09, FIRST PART: EVERY BURIED PROP, NOT
		// THE WORST THREE AND NOT THE WORST SIX. propAnyBuried=10/23 was the
		// line nobody had read: the verdict key names three and announces
		// seven held, which is honest about the cap and silent about the
		// seven, and a header comment accounting for five of them as AABBs
		// touching at 0.00 mm is an analysis and not evidence. THERE IS NO CAP
		// ON THIS PRINTOUT, which is why nothing here announces one; the
		// verdict line's cap of three stays where it is because that line has
		// a buffer, and a reader who wants all ten has this series. The cell
		// count rides each row because 5.0 percent of 400 cells is 20 cells
		// and a percentage alone cannot say that.
		std::printf("    burial series, %d prop(s) read of %d mesh piece(s) in the file, "
		            "EVERY buried prop, no cap:\n",
		            (int)LiveReads.size(), ShapeCount(S.Pieces, "mesh"));
		int Shown = 0;
		for (size_t I = 0; I < LiveReads.size(); ++I)
		{
			if (LiveReads[I].Buried <= 0) { continue; }
			std::printf("      %-28s edge=%-16s buried=%5.1f%%/%3d-of-%d-cells "
			            "overhung=%5.1f%% open=%5.1f%% deepestMm=%8.2f by=%s\n",
			            LiveReads[I].Name.c_str(), LiveReads[I].Edge.c_str(),
			            LiveReads[I].BuriedPct(), LiveReads[I].Buried, LiveReads[I].Cells,
			            LiveReads[I].OverhungPct(), LiveReads[I].OpenPct(),
			            LiveReads[I].DeepestMm, LiveReads[I].DeepestBy.c_str());
			++Shown;
		}
		// THE ZERO'S DENOMINATOR, ON THE SAME LINE AS THE ZERO. A clean street
		// and a street nobody examined print different words here.
		std::printf("      buriedProps=%d/%d examined, %d read no buried cell at all%s\n",
		            Shown, (int)LiveReads.size(), (int)LiveReads.size() - Shown,
		            LiveReads.empty() ? " (nothing measured: no prop was examined)" : "");
		if (Shown == 0 && !LiveReads.empty())
		{
			std::printf("      no prop read a buried cell, over %d prop(s) examined\n",
			            (int)LiveReads.size());
		}
		Check((int)LiveReads.size() == ShapeCount(S.Pieces, "mesh"),
		      "ACCEPTING CASE - every mesh piece in the committed street got a "
		      "footprint reading, and the denominator is the file's own count");
		bool bOrdered = true;
		for (size_t I = 1; I < LiveReads.size(); ++I)
		{
			if (WorseBurial(LiveReads[I], LiveReads[I - 1])) { bOrdered = false; }
		}
		Check(bOrdered,
		      "the series comes back worst first, by the one ordering rule the "
		      "summary key uses, so a reader cannot be shown a worst that is not "
		      "the top of the list");
		Check(WorseBurial(Rung2[0], Rung1[0]) && !WorseBurial(Rung1[0], Rung2[0]),
		      "and that rule is antisymmetric on the planted pair: the buried rung "
		      "is worse than the open one and the open one is not worse than it");
		const int Subject = BurialIndexOf(LiveReads, BurialSubjectName());
		Check(Subject >= 0,
		      "the piece A6 names by hand is still in the committed street under that "
		      "name, so a rename goes red here rather than printing not-placed for ever",
		      BurialSubjectName());
		if (Subject >= 0)
		{
			const BurialRead& G = LiveReads[(size_t)Subject];
			// no-asset-to-read is what the run prints for this piece TODAY,
			// because propsAsMesh=0/23: the fixture says the same rather than
			// inventing a word the run could not have produced.
			const std::string Row = BurialRowValue(G, "no-asset-to-read");
			std::printf("    A6 subject, from the FILE (the run prints the same read "
			            "off the ENGINE): %s\n", Row.c_str());
			std::printf("    A6 covers, deepest first: %s\n",
			            CappedList(G.ByCover, 4, G.CoverCount, ";", "none").c_str());
			Check(G.Buried + G.Overhung + G.Open == G.Cells,
			      "and its three buckets partition its footprint");
			Check(Row.find(' ') == std::string::npos && Row.find('\t') == std::string::npos,
			      "the subject row is one whitespace-free token, so a reader that "
			      "splits on space cannot truncate it", Row);
			Check(Row.find("/collision=no-asset-to-read/") != std::string::npos,
			      "and it carries the piece's OWN collision word beside its burial, "
			      "because Jafar's item 2 is one sentence with two halves and a "
			      "tally of 23 answers neither of them for one piece", Row);
			Check(BurialRowValue(G, "YES").find("/collision=YES/") != std::string::npos,
			      "PLANTED CASE - the same row with the asset reading YES says YES "
			      "there, so that field can move while the burial stands still");
		}

		// D2. A8, SECOND PART: THE PER-CELL DEPTH SERIES ACROSS THE SUBJECT'S
		// FOOTPRINT, WITH EACH CELL'S Z BESIDE IT, AND BOTH READINGS OF EVERY
		// POINT.
		//
		// WHAT IT SETTLES. Two numbers were argued in prose for the
		// carriageway's cover over this grate, 18.7 mm and 19.90 mm, and
		// neither was a named statistic: one is a SAMPLED CELL CENTRE and the
		// other is the FOOTPRINT EDGE, on one plane, and a series shows that
		// where two paragraphs could not. Rule 2 in its own order: the printer
		// first, the real run second, a bound only after and only if one is
		// ever wanted. NOTHING HERE IS A BOUND and nothing below asserts a
		// live millimetre.
		//
		// THE PLANTED PAIR CARRIES THE VERDICTS, as everywhere else in this
		// section, because a guard pinned to the street's current fault goes
		// red the day the street is fixed.
		{
			// ACCEPTING CASE FIRST: the pitch arithmetic on a slab whose
			// answer can be done by hand. A 45 degree slab 0.2 m thick
			// through its own centre: the top face is at HY*cos45 above the
			// centre minus the z it has fallen, which is 0.141421 at z=0, and
			// the vertical cut through it is 0.2/cos45 = 0.282843 thick.
			Piece Flat;
			Flat.Name = "planted_pitched_slab"; Flat.Shape = "box";
			Flat.X = 0; Flat.Y = 0; Flat.Z = 0;
			Flat.SX = 2; Flat.SY = 0.2; Flat.SZ = 2; Flat.PitchDeg = 45;
			double Lo = 0, Hi = 0;
			std::string SpanWhy;
			const bool bSpan = PitchedSpanAtXZ(Flat, 0.0, 0.0, Lo, Hi, SpanWhy);
			std::printf("    A8 pitch span, 45deg slab at its centre: ok=%d loY=%.6f "
			            "hiY=%.6f thickness=%.6f why=%s\n",
			            bSpan ? 1 : 0, Lo, Hi, Hi - Lo, SpanWhy.c_str());
			Check(bSpan && Hi > 0.14142 && Hi < 0.14143 && Lo < -0.14142 && Lo > -0.14143,
			      "ACCEPTING CASE - the pitched top face at a point is the face and "
			      "not the bounding box: 0.141421 where the AABB top is 0.777817");
			Check(bSpan && (Hi - Lo) > 0.28284 && (Hi - Lo) < 0.28285,
			      "and the vertical cut through a 45 degree slab 0.200 m thick is "
			      "0.282843 m, which is the arithmetic being checked and not a name");
			// THE TWO REFUSALS, BOTH BY NAME, because a refusal that read as
			// clear sky would make this instrument the thing it corrects.
			Piece Yawed = Flat;
			Yawed.Name = "planted_yawed_slab"; Yawed.PitchDeg = 0; Yawed.YawDeg = 30;
			Check(!PitchedSpanAtXZ(Yawed, 0.0, 0.0, Lo, Hi, SpanWhy)
			      && SpanWhy.find("yawed-or-rolled") != std::string::npos,
			      "REJECTING CASE - a yawed cover is refused BY NAME rather than "
			      "answered wrongly, and the street carries 44 of them", SpanWhy);
			Check(!PitchedSpanAtXZ(Flat, 0.0, 1.9, Lo, Hi, SpanWhy)
			      && SpanWhy.find("the-solid-does-not-reach-this-point") != std::string::npos,
			      "REJECTING CASE - a point past the slab's own turned extent is not "
			      "covered by it, and the reason says so rather than a zero", SpanWhy);

			// A PLANTED STREET OF TWO PIECES, WHICH IS THE LADDER FOR THIS
			// READING: one prop, one cross-falling slab over it, and the three
			// statistics of one plane printed together. The numbers are
			// arithmetic off these two rows and nothing can repair them.
			std::vector<Piece> Plant;
			Piece PProp;
			PProp.Name = "prop_planted_grate_0"; PProp.Shape = "mesh";
			PProp.Edge = "planted_edge"; PProp.Region = "x00_06";
			PProp.X = 0; PProp.Y = -0.1; PProp.Z = 0;
			PProp.SX = 0.4; PProp.SY = 0.02; PProp.SZ = 0.4;
			Piece PSlab;
			PSlab.Name = "planted_cross_fall"; PSlab.Shape = "box";
			PSlab.Edge = "planted_edge"; PSlab.Region = "x00_06";
			PSlab.X = 0; PSlab.Y = -0.2; PSlab.Z = 0;
			PSlab.SX = 10; PSlab.SY = 0.3; PSlab.SZ = 1.0;
			PSlab.PitchDeg = 1.432096;
			Plant.push_back(PProp);
			Plant.push_back(PSlab);
			std::string PlantWhy;
			const std::vector<CoverCell> PlantProf =
				ReadCoverProfile(Plant, "prop_planted_grate_0", PlantWhy);
			std::printf("    A8 planted profile: %s\n",
			            CoverProfileValue(PlantProf, PlantWhy).c_str());
			// EACH STATISTIC COUNTED UNDER ITS OWN NAME, which is the whole
			// point of the three Where values: a loop that lumped the edges
			// and the centre line together would be the 18.7 against 19.90
			// mistake committed inside the test that was written to settle it.
			int PlantCentres = 0, PlantEdges = 0, PlantMiddles = 0;
			double PlantWorstCentre = -1, PlantWorstEdge = -1, PlantAabb = -1;
			for (size_t I = 0; I < PlantProf.size(); ++I)
			{
				if (PlantProf[I].Where == "cell-centre")
				{
					++PlantCentres;
					if (PlantProf[I].bLocal && PlantProf[I].LocalDepthMm > PlantWorstCentre)
					{
						PlantWorstCentre = PlantProf[I].LocalDepthMm;
					}
				}
				else if (PlantProf[I].Where == "footprint-edge")
				{
					++PlantEdges;
					if (PlantProf[I].bLocal && PlantProf[I].LocalDepthMm > PlantWorstEdge)
					{
						PlantWorstEdge = PlantProf[I].LocalDepthMm;
					}
				}
				else { ++PlantMiddles; }
				if (PlantProf[I].bAabb && PlantProf[I].AabbDepthMm > PlantAabb)
				{
					PlantAabb = PlantProf[I].AabbDepthMm;
				}
			}
			Check(PlantCentres == BurialGridSide() && PlantEdges == 2 && PlantMiddles == 1,
			      "PLANTED CASE - the profile samples the tally's own cell centres "
			      "AND the two footprint edges the tally never samples AND the "
			      "footprint centre line, and says which each point is");
			Check(PlantWorstEdge > 45.0 && PlantWorstEdge < 45.1,
			      "the deepest cover over the footprint is 45.05 mm at its edge, "
			      "which is arithmetic off the planted rows");
			Check(PlantWorstCentre > 44.7 && PlantWorstCentre < 44.9,
			      "and the deepest over SAMPLED CELL CENTRES is 44.80 mm, a quarter "
			      "of a millimetre shallower: one plane, two statistics, which is "
			      "the whole of the 18.7 against 19.90 argument");
			Check(PlantWorstEdge > PlantWorstCentre,
			      "the edge reading is the deeper of the two and a reader is shown "
			      "both rather than one under a name that fits either");
			Check(PlantAabb > 52.4 && PlantAabb < 52.5 && PlantAabb > PlantWorstEdge,
			      "PLANTED CASE - and the AABB reading of the same slab is 52.46 mm, "
			      "which OVERSTATES the deepest real cover, because an AABB top is "
			      "the slab's high edge");
			// THE TWO-POINT FIGURE, PLANTED TOO, because it is the one the
			// ruling's 70.10 mm is and the one a reader computes by hand off a
			// comment. 52.45 mm of AABB depth at the worst cell less 40.05 mm
			// of real cover at the centre line is 12.40 mm here.
			const std::string PlantValue = CoverProfileValue(PlantProf, PlantWhy);
			Check(PlantValue.find("/aabbWorstMinusThis=12.40mm/TWO-POINTS-and-says-so")
			      != std::string::npos,
			      "PLANTED CASE - the two-point overstatement is printed AND carries "
			      "the words TWO-POINTS, so it cannot be read as the same-point "
			      "figure beside it", PlantValue);
			// THE THIRD BUCKET OF THE LOCAL COLUMN, PLANTED: the same slab
			// lifted clear leaves the prop OVERHUNG and not buried, so a zero
			// in the depth column can never mean two things.
			std::vector<Piece> Lift;
			Lift.push_back(PProp);
			Piece PHigh = PSlab;
			PHigh.Name = "planted_lifted_slab";
			// ITS UNDERSIDE NOW CLEARS THE PROP'S TOP. The span's floor at the
			// +z footprint edge is -0.015050, which is 74.95 mm of daylight
			// over a top at -0.090, and that is the number asserted below:
			// arithmetic off these two planted rows and nothing else.
			PHigh.Y = 0.14;
			Lift.push_back(PHigh);
			std::string LiftWhy;
			const std::vector<CoverCell> LiftProf =
				ReadCoverProfile(Lift, "prop_planted_grate_0", LiftWhy);
			int LiftBuried = 0, LiftOverhung = 0;
			double LiftHeadroom = -1;
			for (size_t I = 0; I < LiftProf.size(); ++I)
			{
				if (LiftProf[I].bLocal) { ++LiftBuried; }
				else if (LiftProf[I].bLocalAbove)
				{
					++LiftOverhung;
					if (LiftHeadroom < 0 || LiftProf[I].LocalAboveHeadroomMm < LiftHeadroom)
					{
						LiftHeadroom = LiftProf[I].LocalAboveHeadroomMm;
					}
				}
			}
			std::printf("    A8 planted lifted slab: buriedAt=%d/%d overhungAt=%d/%d "
			            "leastHeadroomMm=%.2f\n", LiftBuried, (int)LiftProf.size(),
			            LiftOverhung, (int)LiftProf.size(), LiftHeadroom);
			Check(LiftBuried == 0 && LiftOverhung == (int)LiftProf.size()
			      && LiftHeadroom > 74.8 && LiftHeadroom < 75.1,
			      "PLANTED CASE - lift the same slab clear and every point reads "
			      "OVERHUNG with 74.95 mm of daylight rather than a 0.00 mm that "
			      "could mean open sky");

			// THE LIVE STREET, PRINTED AND NEVER JUDGED. This is the series
			// A8 ordered and the one any future bound would be read off.
			std::string ProfWhy;
			const std::vector<CoverCell> Prof =
				ReadCoverProfile(S.Pieces, BurialSubjectName(), ProfWhy);
			std::printf("    A8 cover profile of %s, %d point(s), NO CAP, "
			            "pitch-aware local top beside the AABB depth at the same "
			            "point:\n", BurialSubjectName(), (int)Prof.size());
			if (Prof.empty())
			{
				std::printf("      nothing measured: %s\n", ProfWhy.c_str());
			}
			for (size_t I = 0; I < Prof.size(); ++I)
			{
				char Idx[24];
				if (Prof[I].Index >= 0) { std::snprintf(Idx, sizeof(Idx), "iz=%-2d", Prof[I].Index); }
				else { std::snprintf(Idx, sizeof(Idx), "at   "); }
				// THE LOCAL COLUMN SAYS WHICH OF THREE IT IS, never a bare
				// zero: buried to a depth, overhung with daylight under it,
				// or nothing overhead at all.
				char Local[96];
				if (Prof[I].bLocal)
				{
					std::snprintf(Local, sizeof(Local), "buried%8.2fmm/by=%s",
					              Prof[I].LocalDepthMm, Prof[I].LocalBy.c_str());
				}
				else if (Prof[I].bLocalAbove)
				{
					std::snprintf(Local, sizeof(Local), "overhung+%7.2fmm/by=%s",
					              Prof[I].LocalAboveHeadroomMm, Prof[I].LocalAboveBy.c_str());
				}
				else
				{
					std::snprintf(Local, sizeof(Local), "nothing-overhead");
				}
				std::printf("      %s %-14s z=%.6f x=%.4f top=%.6f "
				            "aabb=%8.2fmm/by=%-24s local=%-46s over=%8.2fmm\n",
				            Idx, Prof[I].Where.c_str(), Prof[I].Z, Prof[I].X, Prof[I].PropTopM,
				            Prof[I].bAabb ? Prof[I].AabbDepthMm : 0.0,
				            Prof[I].bAabb ? Prof[I].AabbBy.c_str() : "none",
				            Local,
				            (Prof[I].bAabb && Prof[I].bLocal) ? Prof[I].OverstatementMm() : 0.0);
			}
			const std::string ProfValue = CoverProfileValue(Prof, ProfWhy);
			std::printf("    A8 cover profile value: %s\n", ProfValue.c_str());
			Check(ProfValue.find(' ') == std::string::npos
			      && ProfValue.find('\t') == std::string::npos,
			      "the profile's whole reading is one whitespace-free token, so a "
			      "reader that splits on space cannot truncate it", ProfValue);
			// THE SYNTHETIC REJECTING FIXTURE, which is this project's rule for
			// a tool that checks the project itself: a name that exists in no
			// street, so doing the work the tool prompts can never break it.
			std::string GoneWhy;
			const std::vector<CoverCell> Gone =
				ReadCoverProfile(S.Pieces, "prop_synthetic_nowhere_0", GoneWhy);
			const std::string GoneValue = CoverProfileValue(Gone, GoneWhy);
			std::printf("    A8 cover profile, synthetic subject: %s\n", GoneValue.c_str());
			Check(Gone.empty() && GoneValue.find("nothing-measured/0-points-sampled") == 0
			      && GoneValue.find("prop_synthetic_nowhere_0") != std::string::npos,
			      "REJECTING CASE - a subject that is in no street prints the words "
			      "nothing measured with the name it was asked for, and never a zero "
			      "that reads as no cover", GoneValue);
		}

		// E. THE WHOLE SEGMENT AS A READER SEES IT: concatenated onto the
		// scene line, which is what GSceneLine is, so a key repeated across
		// the two halves would be returned by whichever one a grep reached
		// first.
		PropSegmentIn LiveIn;
		LiveIn.MeshPiecesInFile = ShapeCount(S.Pieces, "mesh");
		LiveIn.PackageDir = "/Game/Ledger/Props";
		LiveIn.NamePrefix = "SM_";
		LiveIn.PlacedAsBox = LiveIn.MeshPiecesInFile;
		LiveIn.Burials = LiveReads;
		LiveIn.bInteractive = true;
		const std::string LiveSeg = PropMeshSegment(LiveIn);
		const std::string Whole = Scene + " " + LiveSeg;
		std::printf("    %s\n", LiveSeg.c_str());
		std::printf("    segment: chars=%d wholeSceneLineChars=%d\n",
		            (int)LiveSeg.size(), (int)Whole.size());
		Check(LiveSeg.find("propSegmentTruncated") == std::string::npos,
		      "no chunk of the segment overran its buffer, and a chunk that did "
		      "would have said so in its own key", LiveSeg);
		Check(EveryTokenIsKeyValue(LiveSeg),
		      "every token of the segment is a key with a non-empty value and no "
		      "whitespace inside it, which is what every reader in this project "
		      "splits on", LiveSeg);
		// AND THE LINE THE RUN ACTUALLY PRINTS, WHICH IS THIS SEGMENT
		// CONCATENATED ONTO SceneLine. NOT asserted, because SceneLine has
		// one token of its own that carries no equals: the zero case of
		// flatsLit prints "flatsLit=0/0 nothing-to-light", so a grep for
		// flatsLit gets the zero WITHOUT the words beside it and a
		// whitespace-splitting reader gets a stray token. That is a fault in
		// a key amendments A5 and A6 do not own, and the count is printed
		// here rather than fixed or hidden.
		{
			std::istringstream WIn(Whole);
			std::string WTok;
			int Loose = 0;
			std::string LooseNames;
			while (WIn >> WTok)
			{
				if (WTok.find('=') != std::string::npos && WTok.find('=') != 0) { continue; }
				++Loose;
				if (Loose <= 3)
				{
					if (!LooseNames.empty()) { LooseNames += ","; }
					LooseNames += WTok;
				}
			}
			std::printf("    whole scene line: tokens carrying no key=value: %d (%s)\n",
			            Loose, Loose == 0 ? "none" : LooseNames.c_str());
		}
		{
			std::vector<std::string> K;
			KeysOf(Whole, K);
			std::string Dup;
			for (size_t I = 0; I < K.size(); ++I)
			{
				for (size_t J = I + 1; J < K.size(); ++J)
				{
					if (K[I] == K[J]) { Dup = K[I]; }
				}
			}
			std::printf("    keys on the whole scene line: %d, duplicated: %s\n",
			            (int)K.size(), Dup.empty() ? "none" : Dup.c_str());
			Check(Dup.empty(),
			      "no key appears twice once the segment is appended to the scene "
			      "line, because both halves end up on ONE line and every reader "
			      "here greps", Dup);
		}
		// THE NUMBER COMES OFF THE FILE, NOT OUT OF THIS LINE, repaired
		// 2026-09-10. It read propFootprintsRead=23/23 as a literal, and the
		// fascia package took the street to 40 mesh pieces, so a correct
		// layout change turned this check red while the thing it asserts held
		// perfectly. WHAT IT ASSERTS IS A RELATION AND NOT A COUNT, and its
		// own message says so: the count EXAMINED over the count the FILE
		// ASKED FOR, equal, with the denominator being the file's and not a
		// number typed here. So the expected string is built from the live
		// spec's own mesh-piece count. A zero is refused separately, because
		// propFootprintsRead=0/0 satisfies the equality and would mean the
		// burial half measured nothing at all.
		int MeshPiecesHere = 0;
		for (size_t I = 0; I < S.Pieces.size(); ++I)
		{
			if (S.Pieces[I].Shape == "mesh") { ++MeshPiecesHere; }
		}
		char WantFootprints[64];
		std::snprintf(WantFootprints, sizeof(WantFootprints),
		              "propFootprintsRead=%d/%d", MeshPiecesHere, MeshPiecesHere);
		Check(MeshPiecesHere > 0,
		      "the committed street asks for at least one mesh piece, so the burial "
		      "half has a population to examine at all", WantFootprints);
		Check(LiveSeg.find(WantFootprints) != std::string::npos,
		      "the burial half ships the count it examined over the count the file "
		      "asked for", std::string(WantFootprints) + " | " + LiveSeg);
		Check(LiveSeg.find("propFootprintGrid=20x20/400-cells-per-prop/a-gap-narrower-"
		                   "than-one-cell-is-invisible-here") != std::string::npos,
		      "and it says what its own sampler cannot see, rather than leaving the "
		      "resolution to be assumed", LiveSeg);
		Check(LiveSeg.find("propBuriedByEdge=") != std::string::npos
		      && LiveSeg.find("east_channel=") != std::string::npos,
		      "the breakdown is per EDGE, which is an axis placement varies on, and "
		      "names the edges the props sit on", LiveSeg);
		// AND THE NEVER-RAN CASE FOR THE BURIAL HALF TOO.
		PropSegmentIn NoProps;
		NoProps.MeshPiecesInFile = 0;
		NoProps.PackageDir = "/Game/Ledger/Props";
		NoProps.NamePrefix = "SM_";
		const std::string SegEmpty = PropMeshSegment(NoProps);
		std::printf("    %s\n", SegEmpty.c_str());
		Check(SegEmpty.find("propFootprintsRead=nothing-measured/0") != std::string::npos,
		      "a run that examined no footprint at all PRINTS THE WORDS nothing "
		      "measured", SegEmpty);
		Check(SegEmpty.find("propFullyBuried=nothing-measured/0") != std::string::npos,
		      "and the count of buried props says the words too, because 0 buried of "
		      "0 examined is not a clean street", SegEmpty);
		Check(SegEmpty.find("propBurialWorst=nothing-measured/of=0") != std::string::npos
		      && SegEmpty.find(std::string("propBurialSubject=not-placed/asked=")
		                       + BurialSubjectName()) != std::string::npos,
		      "and the named subject says NOT PLACED rather than printing a clean "
		      "row for a piece nobody spawned", SegEmpty);
	}

	// ---- THE REJECTING FIXTURES, WHICH HAVE TO BE PLANTED --------------
	//
	// A GUARD MUST BE TESTED ON THE CASE IT SHOULD PASS FIRST, which is
	// everything above, AND on the case it should refuse, which is here. A
	// reader that accepted a wrong-schema file, a truncated file or a file
	// with a field missing would build a street nobody asked for and every
	// count would agree with it.
	{
		LedgerVignette::Spec Bad;
		std::string BadErr;
		std::string Wrong(Text);
		const size_t At = Wrong.find("ledger.vignette-pieces/1");
		Wrong.replace(At, 24, "ledger.vignette-pieces/9");
		Check(!LedgerVignette::ParseSpec(Wrong, Bad, BadErr),
		      "a piece list from a future schema is refused rather than half-read", BadErr);
		Check(BadErr.find("schema") != std::string::npos,
		      "and the refusal names the schema as the reason", BadErr);
	}
	{
		LedgerVignette::Spec Bad;
		std::string BadErr;
		Check(!LedgerVignette::ParseSpec(Text.substr(0, Text.size() / 2), Bad, BadErr),
		      "a truncated piece list is refused rather than read as a shorter street", BadErr);
	}
	{
		LedgerVignette::Spec Bad;
		std::string BadErr;
		std::string NoRoll(Text);
		// THE LAST OCCURRENCE, WHICH IS A PIECE. The first is in the frame
		// header, where roll_deg is a prose description of the convention;
		// renaming that one changes nothing and the fixture would have
		// planted no fault at all while reporting a pass.
		std::string NoRollKey = NoRoll;
		const size_t At = NoRoll.rfind("\"roll_deg\"");
		NoRoll.replace(At, 10, "\"rollXdeg\"");
		Check(!LedgerVignette::ParseSpec(NoRoll, Bad, BadErr),
		      "a piece with roll_deg missing is refused rather than defaulted to upright", BadErr);
		Check(BadErr.find("roll_deg") != std::string::npos,
		      "and the refusal names the field that went missing", BadErr);
	}
	{
		LedgerVignette::Spec Bad;
		std::string BadErr;
		std::string NoGround(Text);
		const size_t At = NoGround.find("\"ground_y_m\"");
		NoGround.replace(At, 12, "\"groundXy_m\"");
		Check(!LedgerVignette::ParseSpec(NoGround, Bad, BadErr),
		      "a camera with no ground level is refused rather than stood at y=0", BadErr);
	}
	{
		LedgerVignette::Spec Bad;
		std::string BadErr;
		Check(!LedgerVignette::ParseSpec("{\"schema\":\"ledger.vignette-pieces/1\"}", Bad, BadErr),
		      "a file with a right schema and nothing else is refused", BadErr);
		Check(!LedgerVignette::ParseSpec("", Bad, BadErr),
		      "an empty file is refused rather than read as an empty street", BadErr);
		Check(!LedgerVignette::ParseSpec("[1,2,3]", Bad, BadErr),
		      "a file that is not an object is refused", BadErr);
	}
	{
		// THE HEADER AND THE ARRAY MUST AGREE. A truncated write leaves a
		// header claiming 593 above 400 lines and every other check here
		// reads one or the other.
		//
		// THE FIXTURE READS THE LIVE COUNT, 2026-09-09, AND NO LONGER PINS
		// ONE. It carried the literal `"pieces":593` and went red the first
		// time the street legitimately grew, which is a fixture failing for
		// the one reason a fixture must not: the work moved the number it was
		// typed against. The count comes out of the header this run just
		// parsed, so the planted fault is a DECREMENT OF WHATEVER IS THERE
		// and the fixture cannot decay. It still says nothing-measured rather
		// than passing if the key is absent.
		LedgerVignette::Spec Bad;
		std::string BadErr;
		std::string Miscount(Text);
		const std::string Key = "\"pieces\":" + std::to_string(S.HeaderPieces);
		const size_t At = Miscount.find(Key);
		if (At != std::string::npos)
		{
			const std::string Wrong = "\"pieces\":" + std::to_string(S.HeaderPieces - 2);
			Miscount.replace(At, Key.size(), Wrong);
			std::printf("    miscountFixture: planted %s in place of %s\n",
			            Wrong.c_str(), Key.c_str());
			Check(!LedgerVignette::ParseSpec(Miscount, Bad, BadErr),
			      "a header that claims fewer pieces than are under it is refused", BadErr);
		}
		else
		{
			// NOTHING MEASURED rather than a pass: the fixture planted no
			// fault, so the check it stands for did not run.
			Check(false, "the miscount fixture could not be planted",
			      "nothing measured: the header key " + Key
			      + " is not in the committed file in that form");
		}
	}
	{
		// THE C LOCALE, ASSERTED RATHER THAN ASSUMED. Under a comma-decimal
		// locale strtod reads "1.5" as 1 and every coordinate in this street
		// loses its fraction while every count stays green.
		std::setlocale(LC_NUMERIC, "C");
		LedgerVignette::Spec Loc;
		std::string LocErr;
		// THE FIXTURE HAS TO BE A COORDINATE THAT ACTUALLY CARRIES A
		// FRACTION, found rather than assumed: the first piece in this file
		// is a 42 metre road plane whose sx_m is a whole number, and
		// asserting on it would pass under a broken locale.
		double Frac = 0.0;
		int FracAt = -1;
		for (size_t I = 0; I < S.Pieces.size() && FracAt < 0; ++I)
		{
			const double V = S.Pieces[I].Y;
			if (std::fabs(V - (double)(long long)V) > 1e-6) { Frac = V; FracAt = (int)I; }
		}
		std::printf("    locale: fractionalFixture=piece%d y=%.6f of %d pieces examined\n",
		            FracAt, Frac, (int)S.Pieces.size());
		Check(FracAt >= 0,
		      "the file carries at least one fractional coordinate to test the numeric locale with",
		      "nothing measured: no piece in the file has a fractional y_m");
		Check(FracAt >= 0 && LedgerVignette::ParseSpec(Text, Loc, LocErr)
		      && std::fabs(Loc.Pieces[FracAt].Y - Frac) < 1e-12,
		      "a fractional coordinate reads back as a fraction under the C numeric locale",
		      "it came back changed, which is what a comma-decimal locale does to every coordinate");
	}

	// ---- PHASE C: WHICH SURFACE ASKS FOR WHICH FILE --------------------
	//
	// ACCEPTING CASE FIRST, AND THE ACCEPTING FIXTURE IS THE LIVE STREET.
	// The sixteen surface names are not written down here: they are counted
	// out of the committed piece list, so a surface added to the street
	// enlarges this test's denominator instead of slipping past it.
	{
		const std::vector<LedgerSurface::Ask> Asked = LedgerSurface::SurfacesAsked(S.Pieces);
		int Sum = 0;
		std::string Names;
		for (size_t I = 0; I < Asked.size(); ++I)
		{
			Sum += Asked[I].Pieces;
			if (I > 0) { Names += " "; }
			Names += Asked[I].Surface + "=" + std::to_string(Asked[I].Pieces);
		}
		std::printf("    surfaces asked by the street: %d over %d piece(s)\n      %s\n",
		            (int)Asked.size(), Sum, Names.c_str());
		Check(Sum == (int)S.Pieces.size(),
		      "every piece in the file is under exactly one surface name");
		Check(Asked.size() >= 10,
		      "the street asks for a real spread of surfaces and not one or two");
		bool bSorted = true, bNamed = true;
		for (size_t I = 0; I < Asked.size(); ++I)
		{
			if (Asked[I].Surface.empty()) { bNamed = false; }
			if (I > 0 && !(Asked[I - 1].Surface < Asked[I].Surface)) { bSorted = false; }
		}
		Check(bSorted, "the surfaces come back in one stable order, so two runs read alike");
		Check(bNamed, "no surface comes back nameless");

		// THE FILENAME RULE IS THE UNITY HOST'S, IN ITS ORDER.
		const std::vector<std::string> C = LedgerSurface::Candidates("asphalt", 0);
		Check(C.size() == 3 && C[0] == "asphalt.png" && C[1] == "asphalt.jpg"
		      && C[2] == "asphalt.jpeg",
		      "the albedo candidates are png then jpg then jpeg, as AssetLibrary tries them");
		const std::vector<std::string> N = LedgerSurface::Candidates("asphalt", 1);
		const std::vector<std::string> R = LedgerSurface::Candidates("asphalt", 2);
		Check(N[1] == "asphalt_n.jpg" && R[1] == "asphalt_r.jpg",
		      "the normal and roughness suffixes are _n and _r, as the pack names them");
	}
	// TILING, WHICH IS THE DIFFERENCE BETWEEN A ROAD AND ONE STRETCHED TILE.
	{
		LedgerVignette::Piece Road;
		Road.SX = 42.0; Road.SY = 0.3; Road.SZ = 2.745858;
		const LedgerSurface::Tiling T = LedgerSurface::TilingFor(Road, 2.0);
		std::printf("    tiling: road 42.00x0.30x2.75 at 2.00 m/tile -> %.2f x %.2f\n", T.U, T.V);
		Check(std::fabs(T.U - 21.0) < 1e-9,
		      "a 42 metre carriageway repeats 21 times along its length at 2 m a tile");
		Check(std::fabs(T.V - 2.745858 / 2.0) < 1e-9,
		      "and across its width, which is its second largest dimension and not its 0.3 thickness");
		LedgerVignette::Piece Small;
		Small.SX = 0.4; Small.SY = 0.1; Small.SZ = 0.2;
		const LedgerSurface::Tiling TS = LedgerSurface::TilingFor(Small, 2.0);
		Check(TS.U >= 1.0 && TS.V >= 1.0,
		      "a piece smaller than one tile shows one whole tile rather than a crop of one");
	}
	// THE TWO LINES, BOTH OUTCOMES WATCHED, ACCEPTING FIRST.
	{
		LedgerSurface::Bound B;
		B.Surface = "asphalt"; B.Pieces = 2; B.PiecesAssigned = 2; B.Status = "RESOLVED";
		B.MapFound[0] = true; B.MapFile[0] = "asphalt.jpg";
		B.MapW[0] = 2048; B.MapH[0] = 2048; B.MapLoadedAs[0] = "JPEG-BGRA8";
		B.MapFound[1] = true; B.MapFile[1] = "asphalt_n.jpg";
		B.MapW[1] = 2048; B.MapH[1] = 2048; B.MapLoadedAs[1] = "JPEG-BGRA8";
		B.TileU = 21.0; B.TileV = 1.37; B.Reason = "none";
		const std::string L = LedgerSurface::SurfaceLine(B);
		std::printf("    %s\n", L.c_str());
		Check(L.find("albedoLoadedAs=2048x2048/JPEG-BGRA8") != std::string::npos,
		      "a resolved surface says what the decoder returned, not what the filename claims");
		Check(L.find("roughnessFile=ABSENT") != std::string::npos
		      && L.find("roughnessTried=asphalt_r.png/asphalt_r.jpg/asphalt_r.jpeg")
		         != std::string::npos,
		      "and a map it did not find names every candidate it tried");
		Check(L.find("piecesAssigned=2/2") != std::string::npos,
		      "the assigned count ships with the piece count that is its denominator");

		// THE REJECTING FIXTURE IS SYNTHETIC, and it changed on 10 September
		// with queue 223. It used to be `card`, which made this check assert
		// the exact thing that item found wrong: card is a decal BLEND MODE
		// and not a library surface, so card.png is a file that by design can
		// never exist and three candidate filenames beside it were three
		// filenames nobody should ever have gone looking for. A surface name
		// that exists nowhere is the honest way to watch the absent case.
		LedgerSurface::Bound A;
		A.Surface = "brick_blue"; A.Pieces = 10; A.Status = "ABSENT";
		A.Reason = "no-file-in-citypack-textures/the-unity-host-generates-this-one-procedurally";
		const std::string AL = LedgerSurface::SurfaceLine(A);
		std::printf("    %s\n", AL.c_str());
		Check(AL.find("surfaceStatus=ABSENT") != std::string::npos
		      && AL.find("albedoTried=brick_blue.png/brick_blue.jpg/brick_blue.jpeg")
		         != std::string::npos
		      && AL.find("procedurally") != std::string::npos,
		      "an absent surface is named with what was tried and why it is missing");
		// NO SPACE INSIDE ANY VALUE, on both lines, mechanically.
		Check(NoSpacePastPrefix(L, "surfaceStatus=") && NoSpacePastPrefix(AL, "surfaceStatus="),
		      "every surface value is space-free and carries exactly one equals");
	}
	{
		std::vector<LedgerSurface::Bound> All;
		LedgerSurface::Bound A;
		A.Surface = "asphalt"; A.Pieces = 2; A.PiecesAssigned = 2; A.MapFound[0] = true;
		A.MapFound[1] = true; A.MapFound[2] = true;
		LedgerSurface::Bound B;
		B.Surface = "concrete"; B.Pieces = 150; B.PiecesAssigned = 150; B.MapFound[0] = true;
		LedgerSurface::Bound C;
		C.Surface = "card"; C.Pieces = 10;
		// QUEUE 227: THE THREE OUTCOMES A LIBRARY SURFACE CAN HAVE ARE ALL IN
		// THE FIXTURE, because a population split that only ever sees resolved
		// surfaces cannot tell PROCEDURAL from ABSENT. paint_yellow is
		// procedural by design and brick_blue is a name that exists nowhere,
		// which is the only genuine fault of the three and the one that has to
		// keep this line below ALL.
		LedgerSurface::Bound P;
		P.Surface = "paint_yellow"; P.Pieces = 4;
		LedgerSurface::Bound X;
		X.Surface = "brick_blue"; X.Pieces = 3;
		All.push_back(A); All.push_back(B); All.push_back(C);
		All.push_back(P); All.push_back(X);
		std::vector<std::string> Tried;
		Tried.push_back("C:/staged/LedgerProbe/CityPackTextures");
		Tried.push_back("C:/staged/LedgerProbe/Binaries/Win64/CityPackTextures");
		const std::string D = LedgerSurface::MaterialsDoneLine(
			All, "/Game/Ledger/M_LedgerSurface", true, "C:/pack/textures", 51, Tried,
			593, 4, 152, 2.0);
		std::printf("    %s\n", D.c_str());
		Check(D.find("surfacesResolved=2/4") != std::string::npos,
		      "the resolved count ships over the LIBRARY surfaces the street asked "
		      "for, and the blend mode is not one of them");
		Check(D.find("surfacesAbsent=brick_blue") != std::string::npos
		      && D.find("surfacesAbsentCount=1/4") != std::string::npos,
		      "and absent means no pack file AND no spec entry, named on the run's "
		      "own line with the population it is counted over");
		Check(D.find("surfacesProcedural=1/4") != std::string::npos
		      && D.find("surfacesProceduralNames=paint_yellow") != std::string::npos
		      && D.find("surfacesAccountedFor=3/4") != std::string::npos,
		      "a surface the Unity host paints from the spec tint is counted as "
		      "accounted for and NAMED, never as a missing file");
		Check(D.find("decalBlendsAsked=1") != std::string::npos
		      && D.find("decalBlendNames=card") != std::string::npos,
		      "the decal blend modes are counted and named apart, because "
		      "card.png is a file that by design can never exist");
		Check(D.find("mapsFound=4/9") != std::string::npos,
		      "the map count ships over three maps per library surface whose "
		      "albedo is expected from the pack, and a procedural surface asks "
		      "for none");
		Check(D.find("piecesTextured=152/593") != std::string::npos,
		      "the textured pieces ship over every piece in the file");
		Check(D.find("materialsStatus=PARTIAL") != std::string::npos,
		      "two of three resolved is PARTIAL and says so");
		Check(NoSpacePastPrefix(D, "materialsStatus="),
		      "every value on the materials line is space-free");
		// THE ACCEPTING CASE, WHICH IS WHAT QUEUE 227 IS ABOUT AND WHAT
		// NOTHING WATCHED BEFORE: every library surface accounted for, with
		// two blend modes still in the vector, reads ALL. Under the old
		// denominator this exact input read PARTIAL and named two blend modes
		// as missing files, and the only way to green it was to write
		// card.png and multiply.png into the pack.
		std::vector<LedgerSurface::Bound> Clean;
		Clean.push_back(A); Clean.push_back(B); Clean.push_back(C); Clean.push_back(P);
		LedgerSurface::Bound M2;
		M2.Surface = "multiply"; M2.Pieces = 10;
		Clean.push_back(M2);
		const std::string CleanLine = LedgerSurface::MaterialsDoneLine(
			Clean, "/Game/Ledger/M_LedgerSurface", true, "C:/pack/textures", 51, Tried,
			593, 4, 152, 2.0);
		std::printf("    %s\n", CleanLine.c_str());
		Check(CleanLine.find("materialsStatus=ALL") != std::string::npos
		      && CleanLine.find("surfacesAsked=3") != std::string::npos
		      && CleanLine.find("surfacesAccountedFor=3/3") != std::string::npos
		      && CleanLine.find("surfacesAbsent=none") != std::string::npos
		      && CleanLine.find("surfacesAbsentCount=0/3") != std::string::npos,
		      "two resolved and one procedural, with two blend modes beside them, "
		      "is ALL and a zero that ships its denominator");
		Check(CleanLine.find("decalBlendsAsked=2") != std::string::npos
		      && CleanLine.find("decalBlendNames=card/multiply") != std::string::npos,
		      "and the blend modes are still counted and named, so ALL cannot be "
		      "read as a run that never saw them");
		Check(CleanLine.find("materialsStatusMeans=ALL-is-every-library-surface-"
		                     "accounted-for") != std::string::npos,
		      "ALL says on its own line what it now means, because the word kept "
		      "its name while its test changed");
		Check(CleanLine.find("surfacePopulationChanged=queue-227/") != std::string::npos
		      && CleanLine.find("is-a-recount-and-not-a-repair") != std::string::npos,
		      "and the line says on its own key that PARTIAL to ALL over the same "
		      "pack is a recount, ruled 2026-09-21");
		Check(EveryTokenIsKeyValue(CleanLine.substr(CleanLine.find("surfacesAccountedFor="))),
		      "and every key the population segment adds is one space-free token "
		      "with one equals");
		Check(CleanLine.find("surfacePopulationCut=") == std::string::npos,
		      "the population segment's 900-char cap did not bite on the longest "
		      "case this fixture can produce");
		// A BASE MATERIAL THAT NEVER LOADED DOMINATES, because sixteen
		// resolved textures bound to nothing is not a partial success.
		const std::string NoBase = LedgerSurface::MaterialsDoneLine(
			All, "/Game/Ledger/M_LedgerSurface", false, "C:/pack/textures", 51, Tried,
			593, 4, 0, 2.0);
		Check(NoBase.find("materialsStatus=NO-BASE-MATERIAL") != std::string::npos
		      && NoBase.find("materialBase=MISSING") != std::string::npos,
		      "a missing base material is its own status and outranks the texture count");
		// AND A PASS WITH NOTHING TO DO SAYS THE WORDS.
		const std::vector<LedgerSurface::Bound> None;
		const std::string Empty = LedgerSurface::MaterialsDoneLine(
			None, "/Game/Ledger/M_LedgerSurface", true, "", 0, Tried, 0, 0, 0, 2.0);
		Check(Empty.find("materialsStatus=NOTHING-ASKED") != std::string::npos
		      && Empty.find("texRoot=NOT-FOUND") != std::string::npos,
		      "a pass with no surfaces says nothing-asked and a root it never found says so");
		// AND IT NAMES WHERE IT LOOKED. This is the half run 19 did not have:
		// `texRoot=NOT-FOUND` alone cannot tell a pack in the wrong place
		// from a search in the wrong place.
		Check(Empty.find("texRootTried=C:/staged/LedgerProbe/CityPackTextures,"
		                 "C:/staged/LedgerProbe/Binaries/Win64/CityPackTextures")
		      != std::string::npos,
		      "a texture root that was not found NAMES every directory it asked about");
		Check(NoSpacePastPrefix(Empty, "materialsStatus="),
		      "and the candidate list is still one space-free value with one equals");
	}
	// ---- THE MID READBACK, WHICH IS THE HALF NOBODY HAD -----------------
	//
	// WHAT THESE PROVE AND WHAT THEY CANNOT. Nothing here runs an engine, so
	// none of this says a parameter arrives anywhere. It says that when the
	// engine answers, the answer is counted, worded and printed correctly,
	// and that the three outcomes a reader has to tell apart print three
	// different strings: same, different, and never asked. The last one is
	// the one that cost this project days elsewhere.
	{
		// THE ACCEPTING CASE FIRST. A surface whose instance answered with
		// exactly what went into it.
		LedgerSurface::Bound B;
		B.Surface = "brick_red"; B.Pieces = 41; B.PiecesAssigned = 41;
		B.Status = "RESOLVED"; B.Reason = "none";
		B.MapFound[0] = true; B.MapFile[0] = "brick_red.jpg";
		B.MapW[0] = 2048; B.MapH[0] = 1024;
		B.TileU = 1.90; B.TileV = 1.00;
		B.Read.bAsked = true;
		B.Read.bTexSame = true; B.Read.bScalarSame = true;
		B.Read.bResourceValid = true; B.Read.bCompIsMid = true;
		B.Read.TexGot = "/Engine/Transient.Texture2D_7";
		B.Read.CompGot = "/Game/Ledger/M_LedgerSurface";
		B.Read.SetU = 1.90; B.Read.GotU = 1.90;
		B.Read.SetV = 1.00; B.Read.GotV = 1.00;
		const std::string L = LedgerSurface::SurfaceLine(B);
		std::printf("    %s\n", L.c_str());
		Check(L.find("midTexReadback=same-pointer") != std::string::npos,
		      "an instance that answered with the pointer that went in says so");
		Check(L.find("midTilingReadback=same-value") != std::string::npos,
		      "and the scalar half is a SEPARATE word on the same line, not the same one twice");
		Check(L.find("midTexResource=valid") != std::string::npos
		      && L.find("midCompMaterial=is-the-instance-we-made") != std::string::npos,
		      "the resource and the component's material are their own readings");
		Check(L.find("midTilingSetGot=U.1.9000..1.9000/V.1.0000..1.0000") != std::string::npos,
		      "both halves of every scalar comparison are printed, set and got");
		Check(NoSpacePastPrefix(L, "midTexReadback="),
		      "every readback value is one space-free token with one equals");
		// THE REJECTING CASE, PLANTED, because a guard that cannot tell a
		// regression from an improvement is a ratchet. This is candidate B as
		// it would print: the scalars land and the texture does not, and what
		// came back instead is NAMED rather than left as a no.
		LedgerSurface::Bound Bad = B;
		Bad.Read.bTexSame = false;
		Bad.Read.TexGot = "/Engine/EngineResources/DefaultTexture.DefaultTexture";
		Bad.Read.bResourceValid = false;
		const std::string BL = LedgerSurface::SurfaceLine(Bad);
		Check(BL.find("midTexReadback=OTHER/"
		              "/Engine/EngineResources/DefaultTexture.DefaultTexture")
		      != std::string::npos,
		      "an instance that answered with something else NAMES what came back");
		Check(BL.find("midTexResource=NULL") != std::string::npos
		      && BL.find("midTilingReadback=same-value") != std::string::npos,
		      "a failed texture readback does not drag the scalar reading down with it");
		Check(NoSpacePastPrefix(BL, "midTexReadback="),
		      "and an engine path name still leaves one equals per token");
		// AND THE CASE THAT WAS NEVER ASKED. A `no` here would say the engine
		// answered wrongly; nothing was ever set, and that is a different
		// fact with a different next action.
		LedgerSurface::Bound Never;
		Never.Surface = "card"; Never.Pieces = 10; Never.Status = "ABSENT";
		const std::string NL = LedgerSurface::SurfaceLine(Never);
		Check(NL.find("midTexReadback=not-asked") != std::string::npos
		      && NL.find("midTilingReadback=not-asked") != std::string::npos
		      && NL.find("midTilingSetGot=not-asked") != std::string::npos,
		      "a surface no instance was made for says not-asked and never prints a no");
	}
	// NO KEY MEANS TWO THINGS ON TWO LINES, ASSERTED RATHER THAN INTENDED.
	// The per-surface readback and the run's readback totals are different
	// moments, and a key carrying both would be returned by a grep from
	// whichever line it reached first. This walks the two lines the run
	// actually prints and fails on any key name they share.
	{
		LedgerSurface::Bound B;
		B.Surface = "kerb"; B.Pieces = 95; B.PiecesAssigned = 95;
		B.MapFound[0] = true; B.Status = "RESOLVED";
		B.Read.bAsked = true; B.Read.bScalarSame = true;
		B.Read.bResourceValid = true; B.Read.bCompIsMid = true;
		std::vector<LedgerSurface::Bound> All;
		All.push_back(B);
		std::vector<std::string> Tried;
		Tried.push_back("C:/staged/LedgerProbe/CityPackTextures");
		const std::string Surf = LedgerSurface::SurfaceLine(B);
		const std::string Done = LedgerSurface::MaterialsDoneLine(
			All, "/Game/Ledger/M_LedgerSurface", true, "C:/pack", 51, Tried,
			593, 3, 95, 2.0);
		std::vector<std::string> SurfKeys, DoneKeys;
		KeysOf(Surf, SurfKeys);
		KeysOf(Done, DoneKeys);
		std::string Shared;
		for (size_t I = 0; I < SurfKeys.size(); ++I)
		{
			for (size_t J = 0; J < DoneKeys.size(); ++J)
			{
				if (SurfKeys[I] == DoneKeys[J])
				{
					if (!Shared.empty()) { Shared += "/"; }
					Shared += SurfKeys[I];
				}
			}
		}
		std::printf("    keys: surface line %d, materials line %d, shared %s\n",
		            (int)SurfKeys.size(), (int)DoneKeys.size(),
		            Shared.empty() ? "none" : Shared.c_str());
		Check(Shared.empty(),
		      "the surface line and the materials line share no key name at all",
		      Shared);
		Check(SurfKeys.size() > 5 && DoneKeys.size() > 5,
		      "and both lines were actually read, so an empty intersection is a "
		      "finding rather than an empty examination");
	}
	// THE SCALAR COMPARISON ON ITS OWN, both ways, because the tolerance is
	// the only judgement in the readback and an exact comparison would print
	// a mismatch that belongs to the float conversion.
	{
		Check(LedgerSurface::ScalarMatches(21.0, 21.0),
		      "a value that survived the trip intact matches");
		Check(LedgerSurface::ScalarMatches(1.3719, 1.37190002),
		      "and one the engine kept as a float still matches");
		Check(!LedgerSurface::ScalarMatches(1.90, 1.00),
		      "a tiling that came back as the material's own default does NOT match");
		Check(!LedgerSurface::ScalarMatches(21.0, 0.0),
		      "and a scalar that came back as nothing at all does not match either");
	}
	// THE RUN'S READBACK TOTALS, ON THE MATERIALS DONE LINE, over the
	// denominator that counts what was actually set rather than what the
	// street asked for.
	{
		std::vector<LedgerSurface::Bound> All;
		LedgerSurface::Bound R1, R2, Absent;
		R1.Surface = "asphalt"; R1.Pieces = 2; R1.PiecesAssigned = 2;
		R1.MapFound[0] = true; R1.Status = "RESOLVED";
		R1.Read.bAsked = true; R1.Read.bScalarSame = true;
		R1.Read.bResourceValid = true; R1.Read.bCompIsMid = true;
		R1.Read.bTexSame = false;    // candidate B, as it would land
		R2 = R1; R2.Surface = "brick_red";
		// A LIBRARY NAME AND NOT `card`, QUEUE 227: the readback denominator
		// is now the library population, so a blend mode here would make the
		// never-asked case print 0/0 and a clean zero is the one reading this
		// check exists to prevent.
		Absent.Surface = "brick_blue"; Absent.Pieces = 10; Absent.Status = "ABSENT";
		All.push_back(R1); All.push_back(R2); All.push_back(Absent);
		std::vector<std::string> Tried;
		Tried.push_back("C:/staged/LedgerProbe/CityPackTextures");
		const std::string D = LedgerSurface::MaterialsDoneLine(
			All, "/Game/Ledger/M_LedgerSurface", true, "C:/pack/textures", 51, Tried,
			593, 2, 43, 2.0);
		std::printf("    %s\n", D.c_str());
		Check(D.find("midReadbackAsked=2/3") != std::string::npos,
		      "the readback denominator counts the surfaces a parameter was set on, "
		      "over the surfaces the street asked for");
		Check(D.find("midParamReadback=0/2") != std::string::npos
		      && D.find("midScalarReadback=2/2") != std::string::npos,
		      "the texture half and the scalar half are counted apart, which is "
		      "what separates candidate A from candidate B");
		Check(D.find("texResourceValid=2/2") != std::string::npos
		      && D.find("compMaterialIsMid=2/2") != std::string::npos,
		      "and the resource and component readings ship over the same denominator");
		Check(D.find("midReadbackStat=") != std::string::npos
		      && D.find("game-thread-copy-not-the-render-proxy") != std::string::npos,
		      "the line says what the number is a statistic OF, and what it cannot see");
		Check(NoSpacePastPrefix(D, "midReadbackAsked="),
		      "every readback total is one space-free token with one equals");
		// A RUN THAT SET NOTHING SAYS THE WORDS. `0/0` reads exactly like a
		// pass that ran and found nothing wrong.
		std::vector<LedgerSurface::Bound> NoneSet;
		NoneSet.push_back(Absent);
		const std::string N = LedgerSurface::MaterialsDoneLine(
			NoneSet, "/Game/Ledger/M_LedgerSurface", true, "", 0, Tried, 593, 0, 0, 2.0);
		Check(N.find("midParamReadback=nothing-measured") != std::string::npos
		      && N.find("midScalarReadback=nothing-measured") != std::string::npos,
		      "a pass that set no parameter prints the words rather than a clean zero");
		Check(N.find("midReadbackAsked=0/1") != std::string::npos,
		      "and the zero still ships the count of what was examined");
	}
	// ---- QUEUE 223: EVERY PIECE TAKES EXACTLY ONE PAINT ROUTE -----------
	//
	// THE ACCEPTING FIXTURE IS THE LIVE STREET, which is this project's rule
	// for a check on the project itself. The census below is taken off the
	// committed piece list with the pack ASSUMED PRESENT for the twelve
	// surfaces that carry a file, so it answers the question the item is
	// about: how many pieces the old `continue` left with no material at all.
	{
		int Pack = 0, Tint = 0, Card = 0, Multiply = 0, None = 0;
		for (size_t I = 0; I < S.Pieces.size(); ++I)
		{
			const LedgerVignette::Piece& P = S.Pieces[I];
			// THE TWELVE THAT RESOLVE ARE THE ONES THAT ARE NEITHER A BLEND
			// NOR IN THE PROCEDURAL TABLE, which is what the run itself
			// measured: surfacesResolved=12/16 with card, interior, multiply
			// and paint_yellow absent.
			const bool bPackAnswered =
				!LedgerSurface::IsDecalBlend(P.Surface)
				&& LedgerSurface::ProceduralSurfaceIndex(P.Surface) < 0;
			switch (LedgerSurface::RouteFor(P.Surface, P.Shape == "decal", bPackAnswered))
			{
			case LedgerSurface::Paint_Pack:          ++Pack; break;
			case LedgerSurface::Paint_Tint:          ++Tint; break;
			case LedgerSurface::Paint_DecalCard:     ++Card; break;
			case LedgerSurface::Paint_DecalMultiply: ++Multiply; break;
			default:                                 ++None; break;
			}
		}
		std::printf("    paint routes over the live street: pack=%d tint=%d "
		            "card=%d multiply=%d none=%d of %d piece(s)\n",
		            Pack, Tint, Card, Multiply, None, (int)S.Pieces.size());
		Check(Pack + Tint + Card + Multiply + None == (int)S.Pieces.size(),
		      "every piece in the file takes exactly one route and none takes two");
		Check(None == 0,
		      "no piece in the committed street is left with no rule to paint it, "
		      "which is the whole of queue 223");
		Check(Tint == 10,
		      "the tint route covers the six interiors and the four yellow bands");
		Check(Card == 10 && Multiply == 10,
		      "the twenty decals split ten opaque cards and ten stains");
		// AND THE REJECTING CASE, PLANTED: a library surface the pack does not
		// answer for still has no route, because inventing one would be
		// painting over the gate.
		Check(LedgerSurface::RouteFor("brick_blue", false, false)
		      == LedgerSurface::Paint_None,
		      "a library surface with no pack file is NOT painted by a made-up rule");
		Check(LedgerSurface::RouteFor("brick_blue", false, true)
		      == LedgerSurface::Paint_Pack,
		      "and the same surface with a file takes the pack route");
		// ProceduralOnly OUTRANKS A PACK FILE, which is the one thing that
		// stops a paint_yellow.jpg dropped into the pack from making the two
		// engines render one surface from two different inputs.
		Check(LedgerSurface::RouteFor("paint_yellow", false, true)
		      == LedgerSurface::Paint_Tint,
		      "paint_yellow renders from the tint even when a pack file exists");
	}
	// THE TINT ITSELF, WHICH IS A NUMBER THIS FILE CAN CHECK AND THE ENGINE
	// CANNOT. Both grades, the byte quantisation and the two colour space
	// conversions, asserted against values computed by hand from the Unity
	// literals.
	{
		Check(LedgerSurface::ProceduralSurfaceCount() == 2,
		      "two surfaces are painted from the tint, and they are named");
		Check(std::string(LedgerSurface::ProceduralSurfaceName(0)) == "interior"
		      && std::string(LedgerSurface::ProceduralSurfaceName(1)) == "paint_yellow",
		      "interior and paint_yellow, in that order");
		const LedgerSurface::Texel Y =
			LedgerSurface::ProceduralAlbedoTexel("paint_yellow");
		const LedgerSurface::Texel In =
			LedgerSurface::ProceduralAlbedoTexel("interior");
		std::printf("    tint texels: paint_yellow %d.%d.%d interior %d.%d.%d\n",
		            Y.R, Y.G, Y.B, In.R, In.G, In.B);
		// THESE TWO DID NOT MOVE ON 2026-09-15 AND THAT IS THE ASSERTION.
		// Jafar's walk-back is applied at exactly one site, AlbedoGradeFor,
		// where only the vector parameter sees it. This texel REPRODUCES A
		// UNITY VALUE and an Unreal-only correction inside it would make it
		// stop equalling the thing it is defined to equal. A builder did put
		// the 0.85 in the shared chain that day; these values are what caught
		// it, and they would have read 154.133.36 and 33.24.15 if it had
		// stayed. HAND-COMPUTED from the Unity literals, unchanged:
		//   0.78 as a byte is 0.78 x 255 + 0.5 = 199.4 -> 199, /255 = 0.78039216
		//   TextureGrade red 0.74, NOT walked back
		//   linear 0.57112483 x 0.50707851 = 0.28960382 -> sRGB -> 147
		Check(Y.R == 147 && Y.G == 127 && Y.B == 35,
		      "worn municipal yellow at 0.78/0.66/0.18, quantised as Unity quantises "
		      "it and multiplied by TextureGrade in linear");
		Check(In.R == 31 && In.G == 22 && In.B == 14,
		      "and the shop interior at 0.18/0.13/0.08 through the same arithmetic");
		// AND THE WALK-BACK IS ASSERTED NOT TO HAVE REACHED THIS ROUTE, by
		// name and in both directions, because the failure is silent: the
		// texel would still be a plausible colour and only its parity meaning
		// would be gone. The rejecting case is the exact value the shared-chain
		// mistake produced.
		Check(Y.R != 154 && In.R != 33,
		      "the walk-back did NOT reach the procedural texel, which reproduces a "
		      "Unity value and may not carry an engine-local correction; 154 and 33 "
		      "are what it read while the 0.85 was wrongly in the shared chain");
		// THE GRADE ACTUALLY DARKENS, which is the half a typo would not move:
		// a grade applied in the wrong direction, or not at all, leaves the
		// raw byte standing.
		Check(Y.R < 199 && Y.G < 168 && Y.B < 46,
		      "the graded texel is darker than the raw tint byte on every channel");
		Check(LedgerSurface::ProceduralRoughnessTexel("paint_yellow") == 242
		      && LedgerSurface::ProceduralRoughnessTexel("interior") == 230,
		      "roughness is the complement of the spec smoothness, as the host's "
		      "gloss map is");
		Check(LedgerSurface::DecalCardRoughnessTexel() == 235,
		      "and an opaque card carries the host's own 0.08 smoothness");
		// THE TRANSFER PAIR IS AN EXACT ROUND TRIP OVER EVERY BYTE, because a
		// tint baked through an approximate inverse would shift every
		// procedural surface by a fraction of a stop.
		int Bad = 0;
		for (int V = 0; V <= 255; ++V)
		{
			const double L = LedgerVignette::SrgbToLinear((double)V / 255.0);
			if (LedgerVignette::ByteOf(LedgerVignette::LinearToSrgb(L)) != V) { ++Bad; }
		}
		Check(Bad == 0, "sRGB to linear and back is a byte-exact round trip",
		      "bytes that did not survive: " + std::to_string(Bad) + " of 256");
		Check(LedgerSurface::MapsFrom("interior") == "window",
		      "the interior borrows the window's maps, which is AssetLibrary.cs:611");
		Check(LedgerSurface::MapsFrom("window") == "window"
		      && LedgerSurface::MapsFrom("asphalt") == "asphalt",
		      "and every other surface wears its own");
		Check(LedgerSurface::IsGroundSurface("kerb")
		      && !LedgerSurface::IsGroundSurface("paint_yellow"),
		      "the ground family is the host's WetSurfaces, and the road paint is "
		      "not in it");
	}
	// THE DECAL ASSET STRING, SPLIT, AGAINST EVERY DECAL IN THE LIVE FILE.
	{
		int Decals = 0, Cropped = 0, Refused = 0;
		for (size_t I = 0; I < S.Pieces.size(); ++I)
		{
			if (S.Pieces[I].Shape != "decal") { continue; }
			++Decals;
			const LedgerSurface::DecalAsset A =
				LedgerSurface::SplitDecalAsset(S.Pieces[I].Asset);
			if (!A.bOk) { ++Refused; continue; }
			if (A.bCropped) { ++Cropped; }
		}
		std::printf("    decal assets: %d parsed, %d cropped, %d refused\n",
		            Decals, Cropped, Refused);
		Check(Decals == 20 && Refused == 0,
		      "every decal asset string in the committed street parses");
		Check(Cropped == 10,
		      "ten carry a crop rectangle and the ten ambientCG sets do not");
		const LedgerSurface::DecalAsset A =
			LedgerSurface::SplitDecalAsset("generated/fascia_mickeys#0.0391,0.2773,0.9766,0.7168");
		Check(A.bOk && A.bCropped && A.Id == "generated/fascia_mickeys",
		      "the id is everything before the hash and the crop is what follows");
		Check(std::fabs(A.U0 - 0.0391) < 1e-9 && std::fabs(A.V1 - 0.7168) < 1e-9,
		      "and all four numbers arrive, u then v, in the file's own order");
		const LedgerSurface::DecalAsset Whole =
			LedgerSurface::SplitDecalAsset("ambientcg/Moss001");
		Check(Whole.bOk && !Whole.bCropped && Whole.U1 == 1.0 && Whole.V1 == 1.0,
		      "no fragment means the whole image, which is 0,0,1,1");
		// FAILS CLOSED, BOTH WAYS, exactly as StreetVignette.SplitAsset does.
		Check(!LedgerSurface::SplitDecalAsset("generated/x#1,2").bOk,
		      "a fragment that is not four numbers is REFUSED and not guessed at");
		Check(!LedgerSurface::SplitDecalAsset("generated/x#a,b,c,d").bOk,
		      "and a fragment that is not numbers at all is refused too");
		Check(LedgerSurface::DecalCardLeaf("generated/poster_gig_bill")
		      == "generated/poster_gig_bill.png",
		      "a card asks for one filename and does not search, as the host does not");
	}
	// THE CROP IN TEXELS, AND THE ROW ORDER IS THE WHOLE OF IT.
	{
		LedgerSurface::DecalAsset Bottom;
		Bottom.bOk = true; Bottom.bCropped = true;
		Bottom.U0 = 0.0; Bottom.V0 = 0.0; Bottom.U1 = 1.0; Bottom.V1 = 0.5;
		const LedgerSurface::CropPx B = LedgerSurface::CropPixels(Bottom, 100, 100);
		std::printf("    crop of the bottom half: x%d..%d y%d..%d (%dx%d)\n",
		            B.X, B.X + B.W, B.Y, B.Y + B.H, B.W, B.H);
		Check(B.X == 0 && B.W == 100 && B.Y == 50 && B.H == 50 && !B.bClamped,
		      "v is measured from the BOTTOM and image rows arrive top down, so the "
		      "bottom half of a picture is the LAST fifty rows");
		LedgerSurface::DecalAsset Top = Bottom;
		Top.V0 = 0.5; Top.V1 = 1.0;
		const LedgerSurface::CropPx T = LedgerSurface::CropPixels(Top, 100, 100);
		Check(T.Y == 0 && T.H == 50,
		      "and the top half is the FIRST fifty, which is the flip that would "
		      "otherwise put a photograph's sky on a fascia");
		// A REAL ONE, at the size the committed fascia picture is.
		const LedgerSurface::DecalAsset M = LedgerSurface::SplitDecalAsset(
			"generated/fascia_mickeys#0.0391,0.2773,0.9766,0.7168");
		const LedgerSurface::CropPx MC = LedgerSurface::CropPixels(M, 1024, 1024);
		std::printf("    fascia_mickeys at 1024 square: x%d..%d y%d..%d (%dx%d)\n",
		            MC.X, MC.X + MC.W, MC.Y, MC.Y + MC.H, MC.W, MC.H);
		Check(MC.W == 960 && MC.H == 450 && !MC.bClamped,
		      "the committed crop takes a wide band out of the middle of the picture");
		Check(MC.Y == 290,
		      "and it starts 290 rows down, which is (1 - v1) and not v0");
		// THE REJECTING CASES, PLANTED, because a clamp that is silent cannot
		// be told from a crop that fitted.
		LedgerSurface::DecalAsset Over = Bottom;
		Over.U1 = 1.6;
		const LedgerSurface::CropPx OC = LedgerSurface::CropPixels(Over, 100, 100);
		Check(OC.bClamped && OC.X + OC.W == 100,
		      "a rectangle past the edge is clamped to the image AND says so");
		LedgerSurface::DecalAsset Inside = Bottom;
		Inside.U0 = 0.5; Inside.U1 = 0.5; Inside.V0 = 0.5; Inside.V1 = 0.5;
		const LedgerSurface::CropPx IC = LedgerSurface::CropPixels(Inside, 100, 100);
		Check(IC.W >= 1 && IC.H >= 1 && IC.bClamped,
		      "a zero-sized rectangle gives one texel rather than an empty upload");
		const LedgerSurface::CropPx NoImage = LedgerSurface::CropPixels(Bottom, 0, 0);
		Check(NoImage.W == 0 && NoImage.H == 0,
		      "and nothing decoded gives nothing cropped, not a one-texel invention");
	}
	// THE CENSUS LINE, ITS IDENTITY, ITS ZERO CASE AND ITS KEYS.
	{
		LedgerSurface::PaintTally T;
		T.Examined = 610; T.Pack = 580; T.Tint = 10; T.DecalCard = 10;
		T.DecalNoStainMaterial = 10; T.Hidden = 10;
		const std::string Seg = LedgerSurface::PaintRouteSegment(T);
		std::printf("   %s\n", Seg.c_str());
		Check(LedgerSurface::PaintedCount(T) == 600
		      && LedgerSurface::UnpaintedCount(T) == 10,
		      "painted plus unpainted is the pieces examined, and neither is derived "
		      "from the other by subtraction");
		Check(Seg.find("piecesUnpainted=10/610") != std::string::npos
		      && Seg.find("piecesPainted=600/610") != std::string::npos,
		      "both halves ship over the pieces EXAMINED");
		Check(Seg.find("paintRoutes=pack.580/tint.10/decal-card.10/decal-multiply.0")
		      != std::string::npos,
		      "and the routes are named with their own counts, not summed into one");
		Check(Seg.find("decal-needs-a-stain-material.10") != std::string::npos,
		      "every unpainted piece says WHICH rule declined it");
		LedgerSurface::PaintTally Zero;
		const std::string ZSeg = LedgerSurface::PaintRouteSegment(Zero);
		Check(ZSeg.find("piecesUnpainted=nothing-measured") != std::string::npos,
		      "a run that examined no piece prints the words and not a clean zero");
		// NO KEY MEANS TWO THINGS ON TWO LINES. The census rides the materials
		// line, so it must share no key with the surface lines or the decal
		// lines beside it.
		LedgerSurface::Bound B;
		B.Surface = "interior"; B.Pieces = 6; B.PiecesAssigned = 6;
		B.Status = "PROCEDURAL"; B.Route = "tint"; B.bTintBuilt = true;
		B.Tint = LedgerSurface::ProceduralAlbedoTexel("interior");
		B.MapBorrowed[1] = true; B.BorrowedFrom = "window";
		B.MapFile[1] = "window_n.jpg"; B.MapW[1] = 2048; B.MapH[1] = 2048;
		B.MapLoadedAs[1] = "JPEG-BGRA8/srgb=no";
		const std::string SurfLine = LedgerSurface::SurfaceLine(B);
		std::printf("    %s\n", SurfLine.c_str());
		Check(SurfLine.find("surfaceStatus=PROCEDURAL") != std::string::npos
		      && SurfLine.find("surfaceRoute=tint") != std::string::npos
		      && SurfLine.find("tintTexel=31.22.14") != std::string::npos,
		      "a procedural surface says so, names its route and prints the texel it "
		      "was painted with");
		Check(SurfLine.find("albedoFile=BUILT-IN-CODE") != std::string::npos
		      && SurfLine.find("albedoTried=card.png") == std::string::npos,
		      "and it never names a candidate file it had no reason to look for");
		Check(SurfLine.find("normalBorrowedFrom=window") != std::string::npos
		      && SurfLine.find("normalFile=window_n.jpg") != std::string::npos,
		      "a borrowed map names the surface it came from");
		LedgerSurface::Bound Blend;
		Blend.Surface = "card"; Blend.Pieces = 10; Blend.Status = "DECAL-BLEND";
		Blend.Route = "decal-card";
		const std::string BlendLine = LedgerSurface::SurfaceLine(Blend);
		std::printf("    %s\n", BlendLine.c_str());
		Check(BlendLine.find("albedoFile=NOT-A-LIBRARY-SURFACE") != std::string::npos,
		      "a decal blend is not a library surface and stops claiming to be one");
		Check(BlendLine.find("card.png") == std::string::npos,
		      "and it names no candidate filename, because card.png can never exist");

		// ---- THE ALBEDO GRADE, QUEUE 299 -----------------------------
		//
		// WHAT THIS PROVES AND WHAT IT CANNOT. It proves the ARITHMETIC and
		// the STRINGS. It cannot prove a frame: no Unreal module compiles in
		// this container and nothing here renders a pixel, so whether the
		// street comes out looking right is the landed run's business and
		// this suite must never be quoted as though it had seen one.
		//
		// ACCEPTING CASE FIRST, which is the half that goes unrun. The
		// accepting case here is the one that must NOT change anything: a
		// material instance that never sets AlbedoGrade renders exactly as
		// it does today, and the default that makes that true is white.
		{
			// 1. THE DEFAULT. A Grade nobody filled in is white in both
			// spaces and says it decided nothing. If this ever became any
			// other colour, every control quad and every decal card in the
			// frame would darken without one line of code asking them to.
			LedgerSurface::Grade Fresh;
			Check(Fresh.R == 1.0 && Fresh.G == 1.0 && Fresh.B == 1.0,
			      "a grade nobody set is WHITE, so an instance that never sets "
			      "the parameter renders exactly as it did before this existed");
			Check(Fresh.GammaR == 1.0 && Fresh.GammaG == 1.0
			      && Fresh.GammaB == 1.0 && !Fresh.bGround,
			      "and its gamma half is white too, so neither space can be the "
			      "one that quietly darkens");
			const LedgerSurface::Texel FreshT = LedgerSurface::GradeTexel(Fresh);
			Check(FreshT.R == 255 && FreshT.G == 255 && FreshT.B == 255,
			      "white as a texel is 255.255.255, which is the multiply having "
			      "no effect on any albedo byte");

			// 2. A SURFACE THAT IS NOT GROUND TAKES TextureGrade, WALKED
			// BACK. HAND-COMPUTED, WRITTEN DOWN, so this check is not the
			// implementation restated back to itself:
			//   TextureGrade red 0.74, walked back at strength 0.85:
			//   1 - 0.85 x (1 - 0.74) = 1 - 0.221 = 0.779
			//   ((0.779 + 0.055) / 1.055) ^ 2.4
			// = (0.79052133) ^ 2.4
			// = 0.56884326, and 0.779 as a byte is 0.779 x 255 + 0.5 = 199.
			// UNTIL 2026-09-15 THESE READ 0.74 / 0.50707851 / 189, which was
			// the full legacy grade run 44 landed and Jafar judged too dark.
			const LedgerSurface::Grade Wall =
				LedgerSurface::AlbedoGradeFor("brick_red", true);
			Check(!Wall.bGround, "brick_red is not a ground surface");
			Check(std::fabs(Wall.GammaR - 0.779) < 1e-12
			      && std::fabs(Wall.GammaG - 0.796) < 1e-12
			      && std::fabs(Wall.GammaB - 0.830) < 1e-12,
			      "a non-ground pack surface takes TextureGrade and nothing else "
			      "of the legacy pair, walked back at 0.85 in gamma");
			Check(std::fabs(Wall.R - (0.56884326)) < 1e-7
			      && std::fabs(Wall.G - (0.59706971)) < 1e-7
			      && std::fabs(Wall.B - (0.65593068)) < 1e-7,
			      "and the linear triple is the hand-computed sRGB transfer of the "
			      "walked-back 0.779/0.796/0.830, because an Unreal vector "
			      "parameter is read AS linear and is never converted for us");
			const LedgerSurface::Texel WallT = LedgerSurface::GradeTexel(Wall);
			Check(WallT.R == 199 && WallT.G == 203 && WallT.B == 212,
			      "a white texel under the non-ground grade comes out 199.203.212, "
			      "which is 0.779/0.796/0.830 x 255 rounded and checkable on paper");

			// 3. A SURFACE THAT IS GROUND TAKES TextureGrade TIMES
			// GroundGrade, THEN THE WALK-BACK, ALL MULTIPLIED IN GAMMA AND
			// CONVERTED ONCE, which is ProceduralAlbedoTexel's own order and
			// not a second opinion.
			// HAND-COMPUTED: 0.74 x 0.55 = 0.407, walked back at 0.85:
			//   1 - 0.85 x (1 - 0.407) = 1 - 0.50405 = 0.49595, and
			//   ((0.49595 + 0.055) / 1.055) ^ 2.4
			// = (0.52222749) ^ 2.4
			// = 0.21031166. As a byte, 0.49595 x 255 + 0.5 = 126.97 -> 126.
			// UNTIL 2026-09-15 THESE READ 0.407 / 0.13782717 / 104.
			const LedgerSurface::Grade Road =
				LedgerSurface::AlbedoGradeFor("kerb", true);
			Check(Road.bGround, "kerb IS a ground surface");
			Check(std::fabs(Road.GammaR - (0.49595)) < 1e-12
			      && std::fabs(Road.GammaG - (0.50530)) < 1e-12
			      && std::fabs(Road.GammaB - (0.52400)) < 1e-12,
			      "a ground pack surface folds GroundGrade in IN GAMMA, 0.74 x "
			      "0.55 = 0.407, and the walk-back lands it at 0.49595, which is "
			      "the order AssetLibrary.BaseColour uses with one term added");
			Check(std::fabs(Road.R - (0.21031166)) < 1e-7
			      && std::fabs(Road.G - (0.21897957)) < 1e-7
			      && std::fabs(Road.B - (0.23693142)) < 1e-7,
			      "and the conversion to linear happens ONCE, on the whole gamma "
			      "product, so the linear red is the hand-computed 0.21031166");
			const LedgerSurface::Texel RoadT = LedgerSurface::GradeTexel(Road);
			Check(RoadT.R == 126 && RoadT.G == 129 && RoadT.B == 134,
			      "a white texel under the ground grade comes out 126.129.134");
			// AND THE ORDER IS LOAD-BEARING, so the wrong order is asserted
			// to be a DIFFERENT number rather than left as a claim. Walking
			// back in LINEAR instead would give 1 - 0.85 x (1 - 0.13782717)
			// = 0.26715, which is a different picture: the ground would come
			// up by 1.94x instead of 1.53x.
			Check(std::fabs(Road.R - (1.0 - 0.85 * (1.0 - 0.13782717))) > 1e-4,
			      "walking back in linear rather than in gamma would be a "
			      "different colour, not a rounding difference, and it is not "
			      "what this does");

			// 4. EVERY MEMBER OF THE GROUND FAMILY, ONE AT A TIME. A rule
			// that happens to be right for kerb and wrong for concrete
			// passes any single-case test and mis-grades 150 of the
			// street's 610 pieces, so the four are named separately and a
			// non-member is asserted beside them.
			const char* Ground[4] = {"asphalt", "sidewalk", "kerb", "concrete"};
			for (int I = 0; I < 4; ++I)
			{
				const LedgerSurface::Grade G =
					LedgerSurface::AlbedoGradeFor(Ground[I], true);
				Check(LedgerSurface::IsGroundSurface(Ground[I]) && G.bGround
				      && std::fabs(G.GammaR - (0.49595)) < 1e-12,
				      (std::string("the ground surface ") + Ground[I]
				       + " takes TextureGrade x GroundGrade walked back to "
				         "0.49595").c_str());
			}
			const char* NotGround[5] = {"metal", "wood", "window", "plaster",
			                            "glass"};
			for (int I = 0; I < 5; ++I)
			{
				const LedgerSurface::Grade G =
					LedgerSurface::AlbedoGradeFor(NotGround[I], true);
				Check(!LedgerSurface::IsGroundSurface(NotGround[I]) && !G.bGround
				      && std::fabs(G.GammaR - 0.779) < 1e-12,
				      (std::string("the non-ground surface ") + NotGround[I]
				       + " takes TextureGrade only, walked back to 0.779").c_str());
			}

			// 5. THE ONE WAY THIS GOES WRONG IS TWICE. A procedural surface's
			// texel ALREADY carries both grades, so its parameter must be
			// white or the street is graded squared: interior would render
			// at 0.74 x 0.74 = 0.5476 of its tint.
			const LedgerSurface::Grade Proc =
				LedgerSurface::AlbedoGradeFor("interior", true);
			Check(Proc.R == 1.0 && Proc.G == 1.0 && Proc.B == 1.0,
			      "a procedural surface gets WHITE, because ProceduralAlbedoTexel "
			      "already baked both grades into the flat texel it built");
			Check(std::string(Proc.Why).find("already-baked") != std::string::npos,
			      "and it says WHY it is white, so white-by-rule and "
			      "white-by-accident are different readings on the line");
			const LedgerSurface::Grade Paint =
				LedgerSurface::AlbedoGradeFor("paint_yellow", true);
			Check(Paint.R == 1.0 && Paint.G == 1.0 && Paint.B == 1.0,
			      "and so does paint_yellow, the other procedural surface");
			// THE GUARD RUN WHERE THE CONDITION IT ASSERTS CAN HAPPEN: the
			// tint texel is unchanged by this whole change, so the number
			// the suite already pinned above still holds.
			const LedgerSurface::Texel Unchanged =
				LedgerSurface::ProceduralAlbedoTexel("interior");
			Check(Unchanged.R == 31 && Unchanged.G == 22 && Unchanged.B == 14,
			      "and the procedural texel itself did not move, so nothing was "
			      "double-graded and nothing was un-graded");

			// 6. A DECAL BLEND GETS WHITE, because StreetVignetteHost.
			// EmitDecal never assigns mat.color: Unity's decals are
			// ungraded and a graded one here would OPEN a difference.
			for (int I = 0; I < 2; ++I)
			{
				const char* Blend2 = (I == 0) ? "card" : "multiply";
				const LedgerSurface::Grade G =
					LedgerSurface::AlbedoGradeFor(Blend2, true);
				Check(G.R == 1.0 && G.G == 1.0 && G.B == 1.0,
				      (std::string("the decal blend ") + Blend2
				       + " gets white, because Unity sets no colour on a decal").c_str());
			}

			// 7. AN UNTEXTURED SURFACE GETS WHITE, because Unity's
			// BaseColour takes its other branch there and uses
			// SurfaceSpec.Tint, a table this side has two rows of. Same
			// surface, other argument, so the argument is proven live.
			const LedgerSurface::Grade Bare =
				LedgerSurface::AlbedoGradeFor("kerb", false);
			Check(Bare.R == 1.0 && Bare.G == 1.0 && Bare.B == 1.0
			      && !Bare.bGround,
			      "a surface with no albedo bound gets white even when it is in "
			      "the ground family, because Unity would be using a tint there");
			Check(std::string(Bare.Why) != std::string(Road.Why),
			      "and the two kerbs give different reasons, so bTextured is a "
			      "live argument and not decoration");

			// 8. THE PARAMETER HAS ONE SPELLING and the generator reads it.
			Check(std::string(LedgerSurface::AlbedoGradeParam()) == "AlbedoGrade",
			      "the vector parameter is spelled AlbedoGrade in the one place "
			      "tools/ue/make_base_material.py --selftest looks for it");

			// 9. THE FOUR DEAD FIELDS, NOW CARRYING THE GRADE, AND NO NEW
			// KEY. Every pack surface printed tintTexel=not-built
			// tintFrom=not-built tintPattern=not-built
			// roughnessTexel=not-built until this change.
			LedgerSurface::Bound K;
			K.Surface = "kerb"; K.Pieces = 95; K.PiecesAssigned = 95;
			K.Status = "RESOLVED"; K.Route = "pack";
			K.MapFound[0] = true; K.MapFile[0] = "kerb.jpg";
			K.MapW[0] = 2048; K.MapH[0] = 1024;
			K.MapLoadedAs[0] = "JPEG-BGRA8/srgb=yes";
			K.MapFound[2] = true; K.MapFile[2] = "kerb_r.jpg";
			K.MapW[2] = 2048; K.MapH[2] = 1024;
			K.MapLoadedAs[2] = "JPEG-BGRA8/srgb=no";
			K.Graded = LedgerSurface::AlbedoGradeFor("kerb", true);
			K.bGradeSet = true;
			const std::string KLine = LedgerSurface::SurfaceLine(K);
			std::printf("    %s\n", KLine.c_str());
			Check(KLine.find("not-built") == std::string::npos,
			      "a graded pack surface has no not-built field left on its line: "
			      "four dead fields turned live without one new key");
			// MOVED 2026-09-15 BY JAFAR'S WALK-BACK, AND STILL PINNED
			// EXACTLY. These read grade-on-white.104.107.112 and
			// linear.0.1378.0.1458.0.1626 while the parameter carried the
			// full legacy grade. HAND-COMPUTED from the new arithmetic:
			//   0.74 x 0.55 = 0.407; walked back 1 - 0.85 x 0.593 = 0.49595
			//   as a byte 0.49595 x 255 + 0.5 = 126.97 -> 126
			//   ((0.49595 + 0.055) / 1.055) ^ 2.4 = 0.21031166 -> 0.2103
			// NEITHER CHECK IS LOOSENED TO A TOLERANCE OR A SHORTER
			// SUBSTRING. The whole value of this pair is that it pins the
			// exact printed string a reader will recompute the grade from.
			Check(KLine.find("tintTexel=grade-on-white.126.129.134")
			      != std::string::npos,
			      "tintTexel on a pack line is the grade on a white reference "
			      "texel, and the VALUE says which of the two it is");
			Check(KLine.find("/groundGrade.0.55") != std::string::npos
			      && KLine.find("/linear.0.2103.0.2190.0.2369") != std::string::npos,
			      "tintFrom carries the gamma inputs AND the linear triple the "
			      "parameter actually holds, so it can be recomputed off the line");
			// AND THE WALK-BACK IS ON THE LINE WITH ITS DATE, so no frame can
			// be read against this grade without the reader learning that the
			// number is provisional and whose it is. NO NEW KEY: this is
			// inside tintFrom's existing `/`-separated value.
			Check(KLine.find("/jafarWalkBack.0.85..ruled.2026-09-15")
			      != std::string::npos,
			      "the walked-back grade names its strength and the date it was "
			      "ruled, inside tintFrom rather than in a key of its own");
			Check(KLine.find("tintPattern=pack-jpeg-times-AlbedoGradeParam")
			      != std::string::npos,
			      "tintPattern says the albedo is a file with a parameter on it "
			      "rather than a flat card");
			Check(KLine.find("roughnessTexel=from-the-pack-roughness-file")
			      != std::string::npos,
			      "and roughnessTexel says where the roughness came from instead "
			      "of claiming a texel this run never computed");
			// AND THE REJECTING CASE FOR THE SAME LINE. A surface the
			// material pass never reached must still print the words, or
			// "no grade was set" becomes unreadable as "the grade is white".
			LedgerSurface::Bound Never;
			Never.Surface = "kerb"; Never.Pieces = 95;
			Never.Status = "NOT-REACHED";
			const std::string NeverLine = LedgerSurface::SurfaceLine(Never);
			Check(NeverLine.find("tintTexel=not-built") != std::string::npos
			      && NeverLine.find("tintFrom=not-built") != std::string::npos
			      && NeverLine.find("tintPattern=not-built") != std::string::npos
			      && NeverLine.find("roughnessTexel=not-built") != std::string::npos,
			      "a surface the material pass never reached STILL prints not-built "
			      "on all four, because nothing-happened is not white");
			// 10. THE PROCEDURAL LINE SAYS ITS PARAMETER IS WHITE, so a
			// reader of two adjacent lines cannot think the tint surfaces
			// were graded twice.
			Check(SurfLine.find("AlbedoGradeParam.white-because-the-product-is-"
			                    "already-in-this-texel") != std::string::npos,
			      "the procedural line names the parameter as white beside the "
			      "grade baked into its texel, which is where a double-apply "
			      "would show");
			// 11. NO SPACES, on both new shapes, because every reader of
			// this file splits on whitespace.
			Check(EveryTokenIsKeyValue(KLine.substr(KLine.find("surfaceStatus=")))
			      && KLine.find("  ") == std::string::npos,
			      "the graded pack surface line is key=value throughout with no "
			      "value carrying a space");
		}

		// ---- WETNESS, QUEUE 186, AND THE TRAP IS THE UNITS --------------
		//
		// THE ACCEPTING CASE FIRST, EVERYWHERE IN THIS BLOCK, and for this
		// feature the accepting case is DRY: a material generated and never
		// driven must render exactly what it renders today. Every guard
		// below is asserted on the case it should PASS before the case it
		// should refuse, and the refusing case is PLANTED rather than waited
		// for.
		{
			// 1. THE PORT ITSELF, AGAINST HAND-COMPUTED VALUES FROM
			// Core/LightModel.cs:594-604. Written out here so these checks
			// are not the implementation restated back to itself:
			//   Smoothness(0.18, 0.6) = 0.18 + (0.92 - 0.18) x 0.6
			//                         = 0.18 + 0.444 = 0.624
			//   Smoothness(0.18, 0.0) = 0.18 exactly, the dry value untouched
			//   Smoothness(0.18, 1.0) = 0.92, the ceiling
			//   AlbedoScale(0.6)      = 1 - 0.45 x 0.6 = 0.73
			//   AlbedoScale(0.9)      = 1 - 0.405     = 0.595
			//   AlbedoScale(1.0)      = 0.55, which IS the lower clamp
			Check(std::fabs(LedgerSurface::WetSmoothness(0.18, 0.6) - 0.624) < 1e-12,
			      "Smoothness(0.18, 0.60) is the hand-computed 0.624",
			      std::to_string(LedgerSurface::WetSmoothness(0.18, 0.6)));
			Check(LedgerSurface::WetSmoothness(0.18, 0.0) == 0.18,
			      "and at rain zero it is the dry value EXACTLY, not nearly: "
			      "this is the accepting case the whole default-is-dry chain "
			      "rests on");
			Check(std::fabs(LedgerSurface::WetSmoothness(0.18, 1.0)
			                - LedgerSurface::WetSmoothnessCeiling()) < 1e-12,
			      "and at rain one it is the 0.92 ceiling whatever the dry value");
			Check(std::fabs(LedgerSurface::WetAlbedoScale(0.6) - 0.73) < 1e-12
			      && std::fabs(LedgerSurface::WetAlbedoScale(0.9) - 0.595) < 1e-12,
			      "AlbedoScale(0.60) is 0.73 and AlbedoScale(0.90) is 0.595");
			Check(LedgerSurface::WetAlbedoScale(0.0) == 1.0,
			      "and at rain zero it is EXACTLY 1.0, so a dry surface is not "
			      "multiplied by something that merely rounds to one");

			// 2. THE CLAMPS, BOTH WAYS ROUND, AND ONE OF THEM IS
			// STRUCTURAL RATHER THAN ACTIVE. SAID OUT LOUD BECAUSE A GREEN
			// CHECK OVER A CLAMP THAT CANNOT FIRE IS A CLAIM: over the whole
			// domain rain is clamped to [0,1] FIRST, so 1 - 0.45 r never
			// goes below 0.55 and the lower bound is touched only at r = 1,
			// where it is reached exactly and not exceeded. The bound is
			// kept because it is the other engine's line character for
			// character, and the case in which it WOULD bite is planted here
			// with the coefficient it would take.
			Check(std::fabs(LedgerSurface::WetAlbedoScale(1.0) - 0.55) < 1e-12,
			      "AlbedoScale reaches its lower bound exactly at rain 1.0");
			Check(1.0 - 0.45 * 1.0 >= 0.55 - 1e-12
			      && 1.0 - 0.60 * 1.0 < 0.55,
			      "PLANTED: at the shipped 0.45 coefficient the lower clamp can "
			      "never bite for any rain in [0,1], and at 0.60 it would, so the "
			      "bound is structural today and is not decoration tomorrow");
			Check(LedgerSurface::WetSmoothness(0.18, 2.0)
			      == LedgerSurface::WetSmoothness(0.18, 1.0)
			      && LedgerSurface::WetSmoothness(0.18, -1.0)
			      == LedgerSurface::WetSmoothness(0.18, 0.0),
			      "rain outside [0,1] is clamped before it is used, both ends, so "
			      "a spec row with 1.5 in it cannot drive a surface past the ceiling");
			Check(LedgerSurface::WetSmoothness(1.5, 0.0) == 1.0
			      && LedgerSurface::WetSmoothness(-0.5, 0.0) == 0.0,
			      "and the RESULT is clamped too, which is what stops a dry value "
			      "outside [0,1] leaving the surface outside it");

			// 3. THE TRAP. UNITY'S PARAMETER IS SMOOTHNESS AND UNREAL'S IS
			// ROUGHNESS, AND THEY ARE OPPOSITES. A direct port of Smoothness
			// into a roughness pin gives a road that gets ROUGHER as it gets
			// wetter, which reads plausible in every number and is exactly
			// backwards in the frame. The two directions are asserted
			// SEPARATELY, so this cannot pass by both moving the same way.
			const double DrySmooth = 0.18;               // asphalt, AssetLibrary
			const double DryRough  = 1.0 - DrySmooth;    // 0.82
			Check(LedgerSurface::WetSmoothness(DrySmooth, 0.6) > DrySmooth,
			      "wetter is SMOOTHER in Unity's units, which is the number the "
			      "port starts from");
			Check(LedgerSurface::WetRoughness(DryRough, 0.6) < DryRough,
			      "and wetter is LESS ROUGH in Unreal's units, which is the trap: "
			      "the same physical change is a rise in one engine and a fall in "
			      "the other");
			Check(std::fabs(LedgerSurface::WetRoughness(DryRough, 0.6) - 0.376) < 1e-12,
			      "WetRoughness(0.82, 0.60) is the hand-computed 0.376, which is "
			      "1 - 0.624");
			// PLANTED: THE WRONG PORT, WRITTEN OUT, AND ASSERTED TO BE A
			// DIFFERENT NUMBER IN THE OTHER DIRECTION. Rule 5b wants a run in
			// which the thing the guard asserts CAN happen; this is that run,
			// and it is the mistake this whole block is named for.
			const double WrongPort = LedgerSurface::WetSmoothness(DryRough, 0.6);
			Check(WrongPort > DryRough
			      && std::fabs(WrongPort - LedgerSurface::WetRoughness(DryRough, 0.6)) > 0.4,
			      "PLANTED: feeding the dry ROUGHNESS straight to Smoothness and "
			      "calling the answer a roughness gives 0.892 where the right "
			      "answer is 0.376, and it moves UP with rain instead of down",
			      std::to_string(WrongPort));

			// 4. THE CONVERSION HAS ONE SITE AND THE SITE IS AN INVOLUTION.
			Check(LedgerSurface::RoughnessFromSmoothness(0.92) ==
			      LedgerSurface::SmoothnessFromRoughness(0.92),
			      "the two names are the same arithmetic, which is why only one "
			      "of them may be a second copy of it");
			Check(std::fabs(LedgerSurface::WetRoughnessFloor() - 0.08) < 1e-12,
			      "the roughness floor is 1 - 0.92 = 0.08, DERIVED from the "
			      "ceiling rather than typed beside it");
			for (int I = 0; I <= 20; ++I)
			{
				const double S = 0.05 * (double)I;
				if (std::fabs(LedgerSurface::SmoothnessFromRoughness(
				              LedgerSurface::RoughnessFromSmoothness(S)) - S) > 1e-12)
				{
					Check(false, "the smoothness/roughness flip round-trips over "
					             "the whole 0..1 range", std::to_string(S));
					break;
				}
			}
			Check(true, "the smoothness/roughness flip round-trips at all 21 "
			            "sampled points of 0..1, examined=21");

			// 5. THE LERP IDENTITY, WHICH IS WHAT LETS THE MATERIAL GRAPH BE
			// ONE NODE. Lerp(RoughnessMap.R, 0.08, Wetness) per texel IS
			// WetRoughness per texel, so the shader and this header cannot
			// mean two different things. SWEPT rather than spot-checked,
			// because the identity is the load-bearing claim.
			int LerpSamples = 0, LerpBad = 0;
			double LerpWorst = 0.0;
			for (int RI = 0; RI <= 20; ++RI)
			{
				for (int WI = 0; WI <= 20; ++WI)
				{
					const double R = 0.05 * (double)RI;
					const double W = 0.05 * (double)WI;
					const double Mine = LedgerSurface::WetRoughness(R, W);
					const double Lerp = R * (1.0 - W)
					                  + LedgerSurface::WetRoughnessFloor() * W;
					const double D = std::fabs(Mine - Lerp);
					++LerpSamples;
					if (D > LerpWorst) { LerpWorst = D; }
					if (D > 1e-12) { ++LerpBad; }
				}
			}
			std::printf("    wetness lerp identity: %d sample(s) examined, %d "
			            "disagreement(s), worst |diff| %.3e\n",
			            LerpSamples, LerpBad, LerpWorst);
			Check(LerpSamples == 441 && LerpBad == 0,
			      "WetRoughness IS Lerp(dryRoughness, 0.08, wetness) over a 21x21 "
			      "sweep, 441 examined, which is the arithmetic the material "
			      "graph performs per texel",
			      std::to_string(LerpBad) + "/" + std::to_string(LerpSamples));
			// AND THE SWEEP CAN FAIL. A floor of 0.10 instead of 0.08 is a
			// plausible typo and it breaks the identity at every wetness
			// above zero, so the denominator above is not counting a
			// tautology.
			int PlantedBad = 0;
			for (int RI = 0; RI <= 20; ++RI)
			{
				for (int WI = 1; WI <= 20; ++WI)
				{
					const double R = 0.05 * (double)RI;
					const double W = 0.05 * (double)WI;
					if (std::fabs(LedgerSurface::WetRoughness(R, W)
					              - (R * (1.0 - W) + 0.10 * W)) > 1e-12)
					{
						++PlantedBad;
					}
				}
			}
			Check(PlantedBad == 420,
			      "PLANTED: a floor of 0.10 disagrees at all 420 of the 420 "
			      "wet samples, so the identity check above is a measurement "
			      "and not a tautology",
			      std::to_string(PlantedBad));

			// 6. MONOTONE IN RAIN, WHICH IS THE ONLY PROPERTY A FRAME CAN
			// BE JUDGED AGAINST WITHOUT A REFERENCE. Strictly down for
			// roughness, strictly up for smoothness, over the same sweep.
			int RoughDown = 0, SmoothUp = 0, Steps = 0;
			for (int I = 1; I <= 20; ++I)
			{
				const double Lo = 0.05 * (double)(I - 1);
				const double Hi = 0.05 * (double)I;
				++Steps;
				if (LedgerSurface::WetRoughness(DryRough, Hi)
				    < LedgerSurface::WetRoughness(DryRough, Lo)) { ++RoughDown; }
				if (LedgerSurface::WetSmoothness(DrySmooth, Hi)
				    > LedgerSurface::WetSmoothness(DrySmooth, Lo)) { ++SmoothUp; }
			}
			Check(Steps == 20 && RoughDown == 20 && SmoothUp == 20,
			      "roughness falls at every one of 20 steps and smoothness rises "
			      "at every one, over 20 examined, so the direction is a reading "
			      "and not a spot check",
			      std::to_string(RoughDown) + "/" + std::to_string(SmoothUp)
			      + " of " + std::to_string(Steps));

			// 7. THE DRY-SMOOTHNESS DATUM TABLE, WHICH IS A SECOND COPY OF
			// AssetLibrary.SurfaceSpec.For AND IS GUARDED AS ONE. The four
			// are asserted ONE AT A TIME for the reason IsGroundSurface's
			// four are: a table right about kerb and wrong about concrete
			// passes any single-surface check and misquotes 150 of the
			// street's 610 pieces.
			Check(std::fabs(LedgerSurface::GroundDrySmoothness("asphalt") - 0.18) < 1e-12,
			      "asphalt's dry smoothness is AssetLibrary's 0.18");
			Check(std::fabs(LedgerSurface::GroundDrySmoothness("sidewalk") - 0.10) < 1e-12,
			      "sidewalk's is 0.10");
			Check(std::fabs(LedgerSurface::GroundDrySmoothness("kerb") - 0.12) < 1e-12,
			      "kerb's is 0.12");
			Check(std::fabs(LedgerSurface::GroundDrySmoothness("concrete") - 0.10) < 1e-12,
			      "concrete's is 0.10");
			Check(LedgerSurface::GroundDrySmoothness("brick_red") < 0.0
			      && LedgerSurface::GroundDrySmoothness("") < 0.0,
			      "a surface with no row answers -1 and not 0.0, because no datum "
			      "and a datum of zero are different facts");
			Check(LedgerSurface::GroundDryTableAgreesWithWetSurfaces(),
			      "every surface in the datum table is in AssetLibrary.WetSurfaces");
			{
				// AND THE OTHER DIRECTION, which the function above cannot
				// see: a member of WetSurfaces with no row would get the
				// shine with no datum to quote it against.
				const char* Wet[4] = {"asphalt", "sidewalk", "kerb", "concrete"};
				int Rows = 0;
				for (int I = 0; I < 4; ++I)
				{
					if (LedgerSurface::GroundDrySmoothness(Wet[I]) >= 0.0) { ++Rows; }
				}
				Check(Rows == 4 && LedgerSurface::GroundDryCount() == 4,
				      "and all four members of WetSurfaces have a row, 4 examined",
				      std::to_string(Rows));
			}

			// 8. WHO GETS WET. AssetLibrary's own list, and its own reason:
			// "Ground the rain lands on. Walls and roofs are deliberately
			// absent - a vertical brick face does not pool water."
			{
				const LedgerSurface::WetBind Wall =
					LedgerSurface::WetBindFor("brick_red", true, 1.0);
				Check(!Wall.bWet && !Wall.bAlbedo && Wall.Wetness == 0.0
				      && Wall.AlbedoScale == 1.0,
				      "a wall takes no wetness at all even at rain 1.0, and its "
				      "albedo scale is EXACTLY 1.0 so nothing multiplies it");
				const LedgerSurface::WetBind Road =
					LedgerSurface::WetBindFor("kerb", true, 0.6);
				Check(Road.bWet && Road.bAlbedo
				      && std::fabs(Road.Wetness - 0.6) < 1e-12
				      && std::fabs(Road.AlbedoScale - 0.73) < 1e-12,
				      "a textured ground surface takes both halves: the scalar at "
				      "0.60 and the albedo multiplier at 0.73");
				const LedgerSurface::WetBind Bare =
					LedgerSurface::WetBindFor("kerb", false, 0.6);
				Check(Bare.bWet && !Bare.bAlbedo && Bare.AlbedoScale == 1.0,
				      "a ground surface with NO albedo bound takes the shine and "
				      "not the darkening, which is the polished-plastic failure "
				      "the thesis names, and the struct says so rather than "
				      "hiding it");
				Check(std::string(Bare.Why) != std::string(Road.Why)
				      && std::string(Wall.Why) != std::string(Road.Why),
				      "and all three reasons differ, so bTextured and the ground "
				      "test are live arguments and not decoration");
				const LedgerSurface::WetBind Over =
					LedgerSurface::WetBindFor("asphalt", true, 2.0);
				Check(std::fabs(Over.Wetness - 1.0) < 1e-12,
				      "a spec row asking for 2.0 is clamped at the bind, so the "
				      "parameter can never carry a value the material's lerp "
				      "would read as an extrapolation");
			}

			// 9. THE GRADE WITH WETNESS IN IT. THE ACCEPTING CASE FIRST AND
			// IT IS THE WHOLE SAFETY ARGUMENT: at wetness zero the grade is
			// BIT FOR BIT the grade that ships today, so this change cannot
			// darken anything by existing.
			{
				const LedgerSurface::Grade Today =
					LedgerSurface::AlbedoGradeFor("kerb", true);
				const LedgerSurface::Grade Dry =
					LedgerSurface::WetGradeFor("kerb", true,
					                           LedgerSurface::WetnessDry());
				Check(Dry.R == Today.R && Dry.G == Today.G && Dry.B == Today.B
				      && Dry.GammaR == Today.GammaR
				      && Dry.GammaG == Today.GammaG
				      && Dry.GammaB == Today.GammaB
				      && Dry.bGround == Today.bGround,
				      "at WetnessDry() the wet grade is the shipped grade EXACTLY, "
				      "every one of six channels, which is what makes a material "
				      "that is generated and never driven render today's frame");
				Check(LedgerSurface::WetnessDry() == 0.0,
				      "and dry is zero, which is the material parameter's default");

				// AND THE WET CASE, HAND-COMPUTED so this is not the
				// implementation restated:
				//   kerb gamma today = 0.49595 (0.74 x 0.55, walked back 0.85)
				//   AlbedoScale(0.6) = 0.73
				//   0.49595 x 0.73  = 0.36204350
				//   ((0.3620435 + 0.055) / 1.055) ^ 2.4 = 0.10780263
				//   as a byte: LinearToSrgb back to 0.3620435, x 255 -> 92
				const LedgerSurface::Grade Wet =
					LedgerSurface::WetGradeFor("kerb", true, 0.6);
				Check(std::fabs(Wet.GammaR - 0.36204350) < 1e-9
				      && std::fabs(Wet.GammaG - 0.36886900) < 1e-9
				      && std::fabs(Wet.GammaB - 0.38252000) < 1e-9,
				      "the wetness multiplies into the grade IN GAMMA, which is "
				      "where AssetLibrary.SetWetness multiplies it, giving the "
				      "hand-computed 0.36204350");
				Check(std::fabs(Wet.R - 0.10780263) < 1e-7,
				      "and the conversion to linear still happens ONCE, on the "
				      "whole gamma product including the wetness term");
				const LedgerSurface::Texel WT = LedgerSurface::GradeTexel(Wet);
				Check(WT.R == 92 && WT.G == 94 && WT.B == 98,
				      "a white texel under the wet ground grade comes out 92.94.98 "
				      "against the dry 126.129.134, which is the road going DARK "
				      "as it goes shiny");
				Check(WT.R < LedgerSurface::GradeTexel(Today).R,
				      "and the direction is asserted as a comparison rather than "
				      "left to a reader of two constants: wet is darker than dry");

				// THE ORDER IS LOAD-BEARING AND THE WRONG ORDER IS A
				// DIFFERENT NUMBER. Folding wetness in BEFORE the walk-back
				// would put Jafar's 0.85 on a darkening he has never seen in
				// a frame: 0.407 x 0.73 = 0.29711, walked back to
				// 1 - 0.85 x 0.70289 = 0.4025435, which is LIGHTER than the
				// 0.36204350 this produces.
				Check(std::fabs(Wet.GammaR - (1.0 - 0.85 * (1.0 - 0.407 * 0.73)))
				      > 1e-4,
				      "PLANTED: applying the walk-back after the wetness instead "
				      "of before would give 0.4025 where this gives 0.3620, a "
				      "different picture and not a rounding difference");

				// A WALL STAYS WHERE IT WAS AT ANY RAIN.
				const LedgerSurface::Grade WallDry =
					LedgerSurface::AlbedoGradeFor("brick_red", true);
				const LedgerSurface::Grade WallWet =
					LedgerSurface::WetGradeFor("brick_red", true, 1.0);
				Check(WallWet.GammaR == WallDry.GammaR
				      && WallWet.R == WallDry.R,
				      "brick at rain 1.0 is the same colour it was dry, because "
				      "walls are not in WetSurfaces");

				// AND THE THREE WHITE BRANCHES STAY WHITE.
				const LedgerSurface::Grade BareWet =
					LedgerSurface::WetGradeFor("kerb", false, 1.0);
				Check(BareWet.R == 1.0 && BareWet.G == 1.0 && BareWet.B == 1.0,
				      "an untextured ground surface stays WHITE at rain 1.0: a "
				      "wetness multiply on a white that means -unity would use a "
				      "tint here- would turn an honest gap into a number");
				const LedgerSurface::Grade ProcWet =
					LedgerSurface::WetGradeFor("interior", true, 1.0);
				Check(ProcWet.R == 1.0 && ProcWet.G == 1.0 && ProcWet.B == 1.0,
				      "and a procedural surface stays white, so the grade baked "
				      "into its texel can never be multiplied twice");
			}

			// 10. THE PARAMETER HAS ONE SPELLING, for the reason
			// AlbedoGradeParam has one.
			Check(std::string(LedgerSurface::WetnessParam()) == "Wetness",
			      "the scalar parameter is spelled Wetness in the one place "
			      "tools/ue/make_base_material.py --selftest looks for it");

			// 11. THE FALLBACK LADDER, SYNTHETIC, ALL FOUR RUNGS. The live
			// file exercises only the first, so the other three would ship
			// unrun; they are the ones that decide what a spec with no shots
			// or no conditions renders, and a wrong answer there is a street
			// bound at somebody's guess.
			{
				LedgerVignette::Spec Sp;
				LedgerVignette::Condition A; A.Id = "overcast_day"; A.Wetness = 0.6;
				LedgerVignette::Condition B; B.Id = "wet_night";    B.Wetness = 0.9;
				Sp.Conditions.push_back(B);   // deliberately NOT first
				Sp.Conditions.push_back(A);
				// RUNG 2: no shots, so overcast_day by name, NOT conditions[0].
				const LedgerSurface::WetnessChoice NoShots =
					LedgerSurface::WetnessForBind(Sp);
				Check(std::fabs(NoShots.Value - 0.6) < 1e-12
				      && NoShots.FromCondition == "overcast_day"
				      && NoShots.ShotsExamined == 0 && NoShots.ShotsAtValue == 0,
				      "with no shots the bind takes overcast_day BY NAME and not "
				      "the first row, and the shot counts print 0 of 0 rather "
				      "than a fraction of nothing",
				      NoShots.FromCondition + "/" + NoShots.Why);
				// RUNG 1 BEATS RUNG 2: a shot naming the other condition wins.
				LedgerVignette::Shot Sh;
				Sh.Id = "s1"; Sh.CameraId = "cam_A"; Sh.ConditionId = "wet_night";
				Sp.Shots.push_back(Sh);
				const LedgerSurface::WetnessChoice FromShot =
					LedgerSurface::WetnessForBind(Sp);
				Check(std::fabs(FromShot.Value - 0.9) < 1e-12
				      && FromShot.FromCondition == "wet_night"
				      && FromShot.ShotsAtValue == 1 && FromShot.ShotsExamined == 1,
				      "and a first shot naming wet_night beats overcast_day, so "
				      "rung 1 is live rather than shadowed by rung 2",
				      FromShot.FromCondition + "/" + FromShot.Why);
				// RUNG 3: a first shot naming a condition that does not exist
				// AND no overcast_day falls to conditions[0], not to dry.
				LedgerVignette::Spec Sp3;
				LedgerVignette::Condition C; C.Id = "fog_only"; C.Wetness = 0.25;
				Sp3.Conditions.push_back(C);
				LedgerVignette::Shot Sh3;
				Sh3.Id = "s"; Sh3.ConditionId = "a-condition-nobody-declared";
				Sp3.Shots.push_back(Sh3);
				const LedgerSurface::WetnessChoice Fallback =
					LedgerSurface::WetnessForBind(Sp3);
				Check(std::fabs(Fallback.Value - 0.25) < 1e-12
				      && Fallback.FromCondition == "fog_only"
				      && std::string(Fallback.Why).find("conditions0")
				         != std::string::npos,
				      "a shot naming a condition that does not exist falls to "
				      "conditions[0] and SAYS SO, rather than binding dry and "
				      "leaving a reader to think the street is dry on purpose",
				      Fallback.FromCondition + "/" + Fallback.Why);
				Check(Fallback.ShotsAtValue == 0 && Fallback.ShotsExamined == 1,
				      "and the unresolvable shot counts in the denominator and "
				      "not in the numerator, so 0 of 1 is the honest reading");
				// RUNG 4: nothing at all. The value is the same 0.0 a dry
				// spec would give and ONLY THE REASON TELLS THEM APART.
				LedgerVignette::Spec Empty;
				const LedgerSurface::WetnessChoice None =
					LedgerSurface::WetnessForBind(Empty);
				Check(None.Value == 0.0 && None.FromCondition == "none"
				      && std::string(None.Why).find("named-no-condition")
				         != std::string::npos,
				      "a spec with no condition at all binds dry AND says the "
				      "file named none, because nothing-measured and a chosen "
				      "zero are different findings with the same number",
				      None.Why);
				LedgerVignette::Spec Dry;
				LedgerVignette::Condition D; D.Id = "wet_000"; D.Wetness = 0.0;
				Dry.Conditions.push_back(D);
				const LedgerSurface::WetnessChoice Zero =
					LedgerSurface::WetnessForBind(Dry);
				Check(Zero.Value == None.Value
				      && std::string(Zero.Why) != std::string(None.Why),
				      "and the two zeroes carry the SAME value and DIFFERENT "
				      "reasons, which is the whole point of printing a reason");
			}

			// 12. THE PER-SURFACE LINE. THE ACCEPTING CASE FIRST: a surface
			// nothing was set on prints the words, because "no wetness was
			// set" and "the wetness is zero" are different findings.
			{
				LedgerSurface::Bound NoWet;
				NoWet.Surface = "kerb"; NoWet.Pieces = 95;
				const std::string NW = LedgerSurface::WetFields(NoWet);
				Check(NW.find("wetSet=not-set") != std::string::npos
				      && NW.find("wetRoughAt=not-set") != std::string::npos,
				      "a surface the material pass never reached prints not-set "
				      "on every wetness field", NW);
				LedgerSurface::Bound Wk;
				Wk.Surface = "asphalt"; Wk.Pieces = 2; Wk.PiecesAssigned = 2;
				Wk.bWetSet = true;
				Wk.Wet = LedgerSurface::WetBindFor("asphalt", true, 0.6);
				const std::string WL = LedgerSurface::WetFields(Wk);
				std::printf("    %s\n", WL.c_str());
				// HAND-COMPUTED: asphalt dry smoothness 0.18 -> dry roughness
				// 0.82; at 0.60 the lerp gives 0.82 x 0.40 + 0.08 x 0.60
				// = 0.328 + 0.048 = 0.376.
				Check(WL.find("wetSet=0.6000") != std::string::npos
				      && WL.find("wetRoughAt=dry.0.8200..wet.0.3760")
				         != std::string::npos,
				      "a wet ground surface prints the value it was set to AND "
				      "the dry and wet roughness it produces, so the DIRECTION "
				      "is readable from the numbers with no second file", WL);
				Check(WL.find("datum.unity-surfacespec-smoothness.0.18")
				      != std::string::npos
				      && WL.find("NOT-the-pack-roughness-texel") != std::string::npos,
				      "and the datum is NAMED in the value, because the material's "
				      "roughness is a 2048x2048 file lerped per texel and this "
				      "number is not a byte of it", WL);
				Check(WL.find("wetAlbedoScale=0.7300") != std::string::npos
				      && WL.find("wetApplied=roughness-and-albedo/AssetLibrary-"
				                 "SetWetness-shape") != std::string::npos,
				      "and the albedo half is on the same line with its own "
				      "number, so a road that went shiny without going dark "
				      "would be visible as 1.0000 here", WL);
				// A WALL, WHICH TAKES NEITHER HALF.
				LedgerSurface::Bound Wall2;
				Wall2.Surface = "brick_red"; Wall2.bWetSet = true;
				Wall2.Wet = LedgerSurface::WetBindFor("brick_red", true, 0.6);
				const std::string BL = LedgerSurface::WetFields(Wall2);
				Check(BL.find("wetSet=0.0000") != std::string::npos
				      && BL.find("wetApplied=none") != std::string::npos
				      && BL.find("wetRoughAt=no-datum") != std::string::npos,
				      "a wall prints 0.0000 and no-datum rather than a roughness "
				      "pair computed from a dry smoothness it does not have", BL);
				Check(EveryTokenIsKeyValue(WL.substr(1))
				      && EveryTokenIsKeyValue(BL.substr(1))
				      && EveryTokenIsKeyValue(NW.substr(1)),
				      "all three wetness shapes are key=value with no value "
				      "carrying a space");
			}

			// 13. THE WHOLE-RUN SEGMENT. A ZERO SHIPS ITS DENOMINATOR AND A
			// RUN THAT SET NOTHING SAYS SO.
			{
				std::vector<LedgerSurface::Bound> Few;
				LedgerSurface::Bound G1; G1.Surface = "asphalt"; G1.bWetSet = true;
				G1.Wet = LedgerSurface::WetBindFor("asphalt", true, 0.6);
				LedgerSurface::Bound G2; G2.Surface = "brick_red"; G2.bWetSet = true;
				G2.Wet = LedgerSurface::WetBindFor("brick_red", true, 0.6);
				LedgerSurface::Bound G3; G3.Surface = "sidewalk";   // never bound
				Few.push_back(G1); Few.push_back(G2); Few.push_back(G3);
				LedgerSurface::WetnessChoice Ch;
				Ch.Value = 0.6; Ch.Why = "first-shot-condition";
				Ch.FromCondition = "overcast_day";
				Ch.ShotsAtValue = 35; Ch.ShotsExamined = 43;
				Ch.CondsAtValue = 29; Ch.CondsExamined = 33;
				const std::string Seg2 = LedgerSurface::WetnessDoneSegment(Few, Ch);
				std::printf("   %s\n", Seg2.c_str());
				std::printf("    wetness done segment: %d of 700 buffer byte(s) "
				            "(no note appended on this shape)\n", (int)Seg2.size());
				Check(Seg2.find("wetnessBindValue=0.6000") != std::string::npos
				      && Seg2.find("wetnessBindFrom=overcast_day/first-shot-condition")
				         != std::string::npos,
				      "the done line carries the SEED value and the row it came "
				      "from", Seg2);
				// THE KEYS MOVED WITH THEIR MEANING, QUEUE 309, AND THE OLD
				// NAMES ARE ASSERTED ABSENT. wetnessValue meant "the one value
				// handed to every instance this run" and there is no such
				// value any more; leaving the name on the seed would hand a
				// reader who greps it a number that answers a different
				// question. A run carrying both names would be worse still.
				Check(Seg2.find("wetnessValue=") == std::string::npos
				      && Seg2.find(" wetnessFrom=") == std::string::npos,
				      "and the superseded key names are gone rather than left "
				      "beside the new ones, so a grep for the old meaning returns "
				      "nothing instead of a number that no longer means it", Seg2);
				Check(Seg2.find("wetnessModel=per-condition-since-queue-309")
				      != std::string::npos
				      && Seg2.find("write-on-change-keyed-on-the-last-applied-wetness")
				         != std::string::npos
				      && Seg2.find("static-at-bind-time") == std::string::npos,
				      "the model token says per-condition with the guard named, "
				      "and the word static is not on the line anywhere", Seg2);
				Check(Seg2.find("the-gap-is-the-compromise") == std::string::npos,
				      "and the stat no longer calls the shotsAtValue gap a "
				      "compromise, because since 309 every shot is photographed "
				      "at its own wetness", Seg2);
				Check(Seg2.find("wetnessSurfacesSet=2/3") != std::string::npos
				      && Seg2.find("wetnessSurfacesWet=1/2") != std::string::npos
				      && Seg2.find("wetnessSurfacesDarkened=1/2") != std::string::npos,
				      "every count ships its denominator, and the denominators "
				      "are DIFFERENT on purpose: set is over surfaces the file "
				      "asked for, wet is over surfaces actually set", Seg2);
				Check(Seg2.find("wetnessShotsAtValue=35/43") != std::string::npos,
				      "and the count of shots at the seed value is a number on "
				      "the line, and it is not a count of walks", Seg2);
				Check(EveryTokenIsKeyValue(Seg2.substr(1)),
				      "the wetness segment is key=value throughout", Seg2);
				Check(Seg2.find("not-shots-that-skipped-a-walk") != std::string::npos,
				      "the done segment reaches its last token, so the 700-byte "
				      "buffer that carries it did not truncate", Seg2);
				// THE ZERO CASES, BOTH OF THEM, BECAUSE THEY ARE DIFFERENT
				// FINDINGS WITH THE SAME NUMBER.
				std::vector<LedgerSurface::Bound> NoneSet;
				NoneSet.push_back(G3);
				const std::string SegNone =
					LedgerSurface::WetnessDoneSegment(NoneSet, Ch);
				Check(SegNone.find("wetnessSurfacesSet=0/1") != std::string::npos
				      && SegNone.find("wetnessNote=no-surface-reached-an-instance")
				         != std::string::npos,
				      "a run that set nothing prints 0 over what it examined AND "
				      "says no surface reached an instance", SegNone);
				LedgerSurface::WetnessChoice DryCh;
				DryCh.Value = 0.0; DryCh.Why = "first-shot-condition";
				DryCh.FromCondition = "wet_000";
				DryCh.ShotsAtValue = 1; DryCh.ShotsExamined = 43;
				std::vector<LedgerSurface::Bound> DrySet;
				LedgerSurface::Bound D1; D1.Surface = "asphalt"; D1.bWetSet = true;
				D1.Wet = LedgerSurface::WetBindFor("asphalt", true, 0.0);
				DrySet.push_back(D1);
				const std::string SegDry =
					LedgerSurface::WetnessDoneSegment(DrySet, DryCh);
				Check(SegDry.find("wetnessBindValue=0.0000") != std::string::npos
				      && SegDry.find("wetnessSurfacesSet=1/1") != std::string::npos
				      && SegDry.find("the-SEED-condition-is-DRY-at-0.0000")
				         != std::string::npos,
				      "and a spec whose SEED wetness IS zero prints that it was "
				      "zero with the count of what was set, rather than printing "
				      "nothing and reading like a feature that never ran", SegDry);
				Check(SegDry.find("says-nothing-about-any-frame-since-queue-309")
				      != std::string::npos,
				      "and the dry note no longer claims the frame is today's "
				      "frame, because since 309 the seed says nothing about what "
				      "any shot was photographed at", SegDry);
				Check(SegDry.find("wetnessNote=no-surface-reached-an-instance")
				      == std::string::npos,
				      "and the two zero notes are not the same note, so a dry "
				      "street cannot be read as a dead pass");
			}

			// 14. THE READBACK, WHICH IS THE KEY THAT ANSWERS -DEAD WRITE-.
			// A material with no such parameter accepts the set and answers
			// zero, so the pair of numbers is the whole reading.
			{
				LedgerSurface::Bound R1; R1.Surface = "asphalt";
				R1.Read.bAsked = true; R1.Read.bWetAsked = true;
				R1.Read.SetWet = 0.6; R1.Read.GotWet = 0.6;
				R1.Read.bWetSame = true;
				const std::string F1 = LedgerSurface::ReadbackFields(R1.Read);
				Check(F1.find("midWetReadback=same-value") != std::string::npos
				      && F1.find("midWetSetGot=0.6000..0.6000") != std::string::npos,
				      "the accepting readback prints same-value AND both numbers",
				      F1);
				LedgerSurface::Bound R2; R2.Surface = "asphalt";
				R2.Read.bAsked = true; R2.Read.bWetAsked = true;
				R2.Read.SetWet = 0.6; R2.Read.GotWet = 0.0;
				R2.Read.bWetSame = false;
				const std::string F2 = LedgerSurface::ReadbackFields(R2.Read);
				Check(F2.find("midWetReadback=DIFFERENT") != std::string::npos
				      && F2.find("midWetSetGot=0.6000..0.0000") != std::string::npos,
				      "PLANTED: a 0.6000 that comes back 0.0000 is the dead-write "
				      "failure queue 186 predicted, and it reads as DIFFERENT "
				      "with both numbers rather than as a grey road", F2);
				LedgerSurface::Bound R3; R3.Surface = "asphalt";
				const std::string F3 = LedgerSurface::ReadbackFields(R3.Read);
				Check(F3.find("midWetReadback=not-asked") != std::string::npos,
				      "and a surface nothing was set on prints not-asked, which "
				      "is not the same as an engine answering wrongly", F3);
				std::vector<LedgerSurface::Bound> RAll;
				RAll.push_back(R1); RAll.push_back(R2); RAll.push_back(R3);
				const std::string RSeg = LedgerSurface::ReadbackDoneSegment(RAll);
				Check(RSeg.find("midWetReadbackAll=1/2/") != std::string::npos,
				      "the run total counts wetness readbacks over surfaces ASKED "
				      "and not over surfaces examined, so a surface nothing was "
				      "set on cannot read as a failure", RSeg);
				std::vector<LedgerSurface::Bound> RNone;
				RNone.push_back(R3);
				Check(LedgerSurface::ReadbackDoneSegment(RNone)
				      .find("midWetReadbackAll=nothing-measured")
				      != std::string::npos,
				      "and a run that asked nothing prints nothing-measured "
				      "rather than a clean 0/0");
			}

			// 15. QUEUE 309: THE PER-CONDITION RE-DRIVE AND ITS GUARD.
			//
			// EVERYTHING THE .cpp's WALK DECIDES IS HERE, which is the point:
			// VignetteShot.cpp does not compile in this container, so a guard
			// written up there would ship unrun and the first thing to find
			// out whether it works would be a 28-minute round trip.
			{
				std::printf("  queue 309, the per-condition wetness re-drive\n");

				// 15a. WHICH ROUTES A RE-DRIVE MAY TOUCH. The decal card's
				// instance is real and carries NEITHER parameter on purpose,
				// so a walk that wrote to every MID it found would put an
				// AlbedoGrade on ten shop signs and ten posters in the judged
				// frame. Every route the enum has is examined, so the zero
				// below has the enum's own size as its denominator.
				{
					int Examined = 0, Touched = 0;
					const LedgerSurface::EPaintRoute All[5] = {
						LedgerSurface::Paint_None, LedgerSurface::Paint_Pack,
						LedgerSurface::Paint_Tint, LedgerSurface::Paint_DecalCard,
						LedgerSurface::Paint_DecalMultiply };
					for (int I = 0; I < 5; ++I)
					{
						++Examined;
						if (LedgerSurface::WetRedriveTouches(All[I])) { ++Touched; }
					}
					std::printf("    routes examined=%d touched=%d (%s)\n",
					            Examined, Touched, "pack and tint only");
					Check(Examined == 5 && Touched == 2
					      && LedgerSurface::WetRedriveTouches(LedgerSurface::Paint_Pack)
					      && LedgerSurface::WetRedriveTouches(LedgerSurface::Paint_Tint),
					      "the two routes whose instances BindSurfaces sets the "
					      "pair on are the two a re-drive may touch, of five "
					      "routes examined");
					Check(!LedgerSurface::WetRedriveTouches(LedgerSurface::Paint_DecalCard)
					      && !LedgerSurface::WetRedriveTouches(LedgerSurface::Paint_DecalMultiply)
					      && !LedgerSurface::WetRedriveTouches(LedgerSurface::Paint_None),
					      "PLANTED: a decal card carries a real dynamic instance "
					      "and neither parameter, and the walk refuses it, so a "
					      "poster cannot be graded by a wetness re-drive");
				}

				// 15b. THE GUARD, ACCEPTING CASE FIRST: A CHANGED WETNESS IS
				// WRITTEN. Two outcomes, both watched, and the accepting one
				// runs before the refusing one.
				{
					LedgerSurface::WetRedrive G;
					Check(LedgerSurface::WetRedriveNeeded(G, 0.6),
					      "a guard that has never applied anything needs a walk, "
					      "because the instances carry the bind seed and the "
					      "first condition may disagree with it");
					LedgerSurface::WetRedriveAsked(G);
					LedgerSurface::WetRedriveWalked(G, 0.6, "overcast_day");
					Check(LedgerSurface::WetRedriveNeeded(G, 0.9),
					      "and a wetness that MOVED needs a walk: 0.6 latched, "
					      "0.9 asked");
					// 15c. THE PLANTED REJECTING CASE, WHICH IS THE HALF THAT
					// GOES UNRUN. The thing the guard asserts can happen is a
					// settle loop re-entering with a wetness that has not
					// moved, so the condition is PLANTED and the bound is not
					// loosened: not one write may happen.
					Check(!LedgerSurface::WetRedriveNeeded(G, 0.6),
					      "PLANTED: the same wetness asked again is refused, "
					      "which is the whole guard");
					Check(!LedgerSurface::WetRedriveNeeded(G, 0.6 + 1e-9),
					      "PLANTED: and a float round trip through the engine is "
					      "not a change, because the comparison is the project's "
					      "one tolerance and not an equality");
					Check(LedgerSurface::WetRedriveNeeded(G, 0.6 + 1e-2),
					      "while a real move of 0.01 still needs a walk, so the "
					      "tolerance is not a rounding-away of the feature");
				}

				// 15d. THE SETTLE LOOP ITSELF, RUN. The guard's claim is
				// arithmetic about a loop, so the loop is executed here rather
				// than reasoned about: three conditions, forty ticks each,
				// four hundred pieces. WHAT WOULD HAPPEN WITHOUT THE GUARD is
				// computed beside it from the same numbers, so the saving is a
				// ratio with both terms printed and not an assertion.
				{
					LedgerSurface::WetRedrive G;
					const double Conds[3] = {0.6, 0.9, 0.6};
					const int kTicks = 40, kPieces = 400;
					int Writes = 0;
					for (int C = 0; C < 3; ++C)
					{
						for (int T = 0; T < kTicks; ++T)
						{
							LedgerSurface::WetRedriveAsked(G);
							if (!LedgerSurface::WetRedriveNeeded(G, Conds[C]))
							{
								LedgerSurface::WetRedriveSkipped(G);
								continue;
							}
							LedgerSurface::WetRedriveWalked(G, Conds[C], "cond");
							for (int P = 0; P < kPieces; ++P)
							{
								LedgerSurface::WetRedriveVisit(
									G, LedgerSurface::WetRedrive_Wrote);
								++Writes;
							}
						}
					}
					const int Naive = 3 * kTicks * kPieces;
					std::printf("    settle loop: calls=%d walks=%d skipped=%d "
					            "pieceWrites=%d naiveWouldBe=%d\n",
					            G.Calls, G.Walks, G.Skipped, Writes, Naive);
					Check(G.Calls == 120 && G.Walks == 3 && G.Skipped == 117
					      && Writes == 1200 && Naive == 48000,
					      "over 120 asks the guard let three walks through, one "
					      "per CHANGED wetness, and refused 117; 1200 piece "
					      "writes against the 48000 a naive re-drive would have "
					      "made, of 120 asks examined",
					      std::to_string(G.Walks) + "/" + std::to_string(G.Calls));
					// AND THE THIRD CONDITION IS THE ONE THAT MATTERS: it
					// returns to 0.6, which the guard has NOT been holding
					// since 0.9 came through, so it must walk again. A guard
					// keyed on "have we ever seen this value" instead of "the
					// last one applied" would photograph the third condition
					// at 0.9 and no number would say so.
					Check(G.Walks == 3,
					      "and a wetness returning to a value the run has already "
					      "used still walks, because the key is the LAST applied "
					      "value and not the set of values seen");
					const std::string RS = LedgerSurface::WetRedriveSegment(G);
					std::printf("    %s\n", RS.c_str());
					std::printf("    redrive segment: %d of 860 buffer byte(s)\n",
					            (int)RS.size());
					Check(RS.find("wetnessRedriveWalks=3/of=120/ApplyCondition-calls")
					      != std::string::npos
					      && RS.find("wetnessRedriveSkipped=117/of=120/ApplyCondition-calls")
					         != std::string::npos,
					      "the guard's writes-per-tick prints WITH ITS "
					      "DENOMINATOR, walks and skips both over the asks", RS);
					Check(RS.find("wetnessRedriveWrote=1200/of=1200/piece-visits")
					      != std::string::npos
					      && RS.find("wetnessNow=0.6000") != std::string::npos
					      && RS.find("wetnessRedriveTallyMismatch") == std::string::npos,
					      "and the pieces written ship the visits they were taken "
					      "over, the latched value is the last condition's, and "
					      "the identity walks+skipped==calls holds so no mismatch "
					      "key appears", RS);
					Check(EveryTokenIsKeyValue(RS.substr(1)),
					      "the re-drive segment is key=value with no value "
					      "carrying a space", RS);
					// THE SERIES THE BUFFER IS SIZED FROM, PRINTED BEFORE THE
					// NUMBER IS SET. Two shapes measured above; the third is
					// the worst this function can build, and it is built here
					// rather than guessed: the longest condition id the
					// committed file carries is pin_setter_night at 16, the
					// counters are widened to five digits, and the readback
					// note is appended OUTSIDE the buffer so it is measured
					// apart. A snprintf that overruns truncates silently, and
					// the key that would lose its tail is the last one in the
					// buffer.
					LedgerSurface::WetRedrive Worst = G;
					Worst.LastFrom = "pin_setter_night_and_then_some";
					Worst.Calls = 99999; Worst.Walks = 99999;
					Worst.Skipped = 0; Worst.PieceVisits = 99999;
					Worst.Out[LedgerSurface::WetRedrive_Wrote] = 99999;
					for (int I = 1; I < LedgerSurface::WetRedrive_OutcomeCount; ++I)
					{
						Worst.Out[I] = 99999;
					}
					LedgerSurface::WetRedriveReadback(Worst, 0.6, 0.6);
					const std::string WS = LedgerSurface::WetRedriveSegment(Worst);
					// WHAT THESE NUMBERS ARE: the WHOLE returned string in
					// each case. Only the snprintf portion is capped; the
					// readback note and the tally-mismatch key are std::string
					// concatenations appended after it and cannot overrun
					// anything. So the worst shape below is the worst BUFFER
					// portion by construction, because it takes the readback
					// (no note) and holds the identity (no mismatch key),
					// while the live shape above is longer only because it
					// carries an appended note outside the cap.
					std::printf("    redrive segment series, whole string: live=%d "
					            "(carries an appended note outside the cap) "
					            "nothingMeasured=%d (no snprintf at all) "
					            "worstBufferShape=%d of 860, %d free\n",
					            (int)RS.size(),
					            (int)LedgerSurface::WetRedriveSegment(
					                LedgerSurface::WetRedrive()).size(),
					            (int)WS.size(), 860 - (int)WS.size());
					Check((int)WS.size() < 860
					      && WS.find("wetnessRedriveStat=whole-run") != std::string::npos
					      && WS.find("readback-is-the-last-walks-first-written-piece")
					         != std::string::npos,
					      "the worst shape this function can build fits the "
					      "buffer that carries it AND still reaches its last "
					      "token, which is the measurement the size is set from",
					      std::to_string((int)WS.size()) + "/860");
				}

				// 15e. THE REFUSALS ARE COUNTED AND NAMED. A walk that wrote
				// nothing and a walk that found nothing it was allowed to
				// write on are different findings, and a bare wrote=0 reads as
				// the first when it is usually the second.
				{
					LedgerSurface::WetRedrive G;
					LedgerSurface::WetRedriveAsked(G);
					LedgerSurface::WetRedriveWalked(G, 0.9, "wet_night");
					LedgerSurface::WetRedriveVisit(G, LedgerSurface::WetRedrive_NotOurRoute);
					LedgerSurface::WetRedriveVisit(G, LedgerSurface::WetRedrive_NoActor);
					LedgerSurface::WetRedriveVisit(G, LedgerSurface::WetRedrive_NoComponent);
					LedgerSurface::WetRedriveVisit(G, LedgerSurface::WetRedrive_NoMid);
					LedgerSurface::WetRedriveVisit(G, LedgerSurface::WetRedrive_NoBind);
					const std::string RS = LedgerSurface::WetRedriveSegment(G);
					Check(RS.find("wetnessRedriveWrote=0/of=5/piece-visits")
					      != std::string::npos
					      && RS.find("wetnessRedriveRefused=notOurRoute.1/noBind.1/"
					                 "noActor.1/noComponent.1/noMid.1")
					         != std::string::npos,
					      "PLANTED: a walk that wrote nothing prints 0 over the "
					      "visits it made AND the bucket each refusal fell in, so "
					      "a dead walk cannot read as a clean one", RS);
					Check(RS.find("wetnessRedriveReadback=not-asked") != std::string::npos
					      && RS.find("wetnessRedriveReadNote=no-piece-was-written")
					         != std::string::npos,
					      "and the readback pair says not-asked with a note, "
					      "because 0.0000..0.0000 is also what a dead write on a "
					      "dry condition prints", RS);
					// THE MISMATCH KEY, PLANTED, because a key that only ever
					// appears when something is wrong is a key nothing proves
					// works. The identity is broken by hand here.
					LedgerSurface::WetRedrive Broken = G;
					Broken.Calls = 9;
					Check(LedgerSurface::WetRedriveSegment(Broken)
					      .find("wetnessRedriveTallyMismatch=walks=1/skipped=0/calls=9")
					      != std::string::npos,
					      "PLANTED: walks plus skipped not summing to calls prints "
					      "all three numbers, so a broken denominator announces "
					      "itself instead of being divided by");
				}

				// 15f. A RUN THAT NEVER APPLIED A CONDITION SAYS SO. Rule 3b:
				// 0/0 and "the owner was never called" read alike to a grep.
				{
					LedgerSurface::WetRedrive G;
					const std::string RS = LedgerSurface::WetRedriveSegment(G);
					Check(RS.find("wetnessNow=nothing-measured") != std::string::npos
					      && RS.find("wetnessRedriveWalks=nothing-measured/of=0/")
					         != std::string::npos
					      && RS.find("ApplyCondition-was-never-called") != std::string::npos,
					      "a run whose owner was never called prints the words and "
					      "never a clean zero", RS);
					Check(EveryTokenIsKeyValue(RS.substr(1)),
					      "and the nothing-measured re-drive segment is space-free "
					      "too", RS);
				}

				// 15g. THE PER-FRAME KEY, WHICH IS THE ONLY EVIDENCE 309 CAN
				// OFFER. The surface line's wetSet is last-wins over the run
				// and cannot tell "re-driven per condition" from "set once to
				// the last condition's value". This can: one run shows 0.9000
				// on a night row and 0.0000 on wet_000, on the two rows' own
				// lines, which is what the item asked for under the one key
				// name this file's naming law allows (midWetSetGot is a
				// statement about ONE SURFACE and may not also be a statement
				// about one frame).
				{
					LedgerSurface::WetShotIn N;
					N.Asked = 0.9; N.AskedFrom = "wet_night";
					N.bEverApplied = true; N.OnPieces = 0.9; N.WalkedAt = "wet_night";
					const std::string NF = LedgerSurface::WetShotFields(N);
					LedgerSurface::WetShotIn Z;
					Z.Asked = 0.0; Z.AskedFrom = "wet_000";
					Z.bEverApplied = true; Z.OnPieces = 0.0; Z.WalkedAt = "wet_000";
					const std::string ZF = LedgerSurface::WetShotFields(Z);
					std::printf("   night:%s\n", NF.c_str());
					std::printf("   wet000:%s\n", ZF.c_str());
					std::printf("    shot wetness fields: %d and %d of 420 "
					            "buffer byte(s)\n", (int)NF.size(), (int)ZF.size());
					Check(NF.find("shotWetness=0.9000") != std::string::npos
					      && NF.find("shotWetnessOnPieces=0.9000") != std::string::npos
					      && NF.find("shotWetnessAgrees=yes") != std::string::npos,
					      "a night row prints 0.9000 asked, 0.9000 carried, and "
					      "agrees", NF);
					Check(ZF.find("shotWetness=0.0000") != std::string::npos
					      && ZF.find("shotWetnessOnPieces=0.0000") != std::string::npos
					      && ZF.find("shotWetnessAgrees=yes") != std::string::npos,
					      "and the dry end of the ladder prints 0.0000 on the same "
					      "keys in the same run, which is the difference a "
					      "last-wins surface line cannot show", ZF);
					// THE FAULT, PLANTED AND NAMED BEFORE ANY RUN: a frame
					// photographed at a wetness the street is not wearing. It
					// is what a guard keyed on the wrong thing, or a walk that
					// wrote nothing, would produce.
					LedgerSurface::WetShotIn Bad;
					Bad.Asked = 0.9; Bad.AskedFrom = "wet_night";
					Bad.bEverApplied = true; Bad.OnPieces = 0.6;
					Bad.WalkedAt = "overcast_day";
					const std::string BF = LedgerSurface::WetShotFields(Bad);
					Check(BF.find("shotWetnessAgrees=NO") != std::string::npos
					      && BF.find("shotWetness=0.9000") != std::string::npos
					      && BF.find("shotWetnessOnPieces=0.6000") != std::string::npos
					      && BF.find("shotWetnessWalkedAt=overcast_day") != std::string::npos,
					      "PLANTED: a frame shot at a wetness the street is not "
					      "wearing reads NO with both numbers and the condition "
					      "the last walk ran for, rather than as a grey road", BF);
					// AND A SKIP IS NOT A FAULT. Two conditions at one wetness
					// mean the second never walks, so walkedAt names the first
					// while the numbers agree; a reader must be able to tell
					// that from the fault above.
					LedgerSurface::WetShotIn Skip;
					Skip.Asked = 0.6; Skip.AskedFrom = "grid_sky070_sun003";
					Skip.bEverApplied = true; Skip.OnPieces = 0.6;
					Skip.WalkedAt = "overcast_day";
					const std::string SF = LedgerSurface::WetShotFields(Skip);
					Check(SF.find("shotWetnessAgrees=yes") != std::string::npos
					      && SF.find("shotWetnessFrom=grid_sky070_sun003") != std::string::npos
					      && SF.find("shotWetnessWalkedAt=overcast_day") != std::string::npos,
					      "a shot the guard skipped agrees while naming a "
					      "different walk, so the guard working does not read as "
					      "the fault above", SF);
					LedgerSurface::WetShotIn None;
					const std::string NoneF = LedgerSurface::WetShotFields(None);
					Check(NoneF.find("shotWetness=nothing-measured") != std::string::npos
					      && NoneF.find("shotWetnessAgrees=nothing-measured")
					         != std::string::npos,
					      "and a frame taken before any walk ran prints the words "
					      "rather than a 0.0000 that reads as a dry street",
					      NoneF);
					Check(EveryTokenIsKeyValue(NF.substr(1))
					      && EveryTokenIsKeyValue(BF.substr(1))
					      && EveryTokenIsKeyValue(NoneF.substr(1)),
					      "all three shot-wetness shapes are space-free");
				}

				// 15h. THE SURFACE LINE NAMES THE CONDITION ITS VALUE CAME
				// FROM. A last-wins number with no condition beside it cannot
				// say which frame it describes.
				{
					LedgerSurface::Bound B; B.Surface = "asphalt"; B.bWetSet = true;
					B.Wet = LedgerSurface::WetBindFor("asphalt", true, 0.9);
					B.WetFrom = "wet_night";
					const std::string F = LedgerSurface::WetFields(B);
					std::printf("   %s\n", F.c_str());
					Check(F.find("wetSet=0.9000") != std::string::npos
					      && F.find("wetSetFrom=wet_night") != std::string::npos
					      && F.find("wetSetStat=per-surface/LAST-WINS") != std::string::npos,
					      "the per-surface line prints the value, the condition it "
					      "came from and the word LAST-WINS, so a reader is never "
					      "left inferring which condition a number belongs to", F);
					LedgerSurface::Bound Seed; Seed.Surface = "asphalt";
					Seed.bWetSet = true;
					Seed.Wet = LedgerSurface::WetBindFor("asphalt", true, 0.6);
					const std::string SF = LedgerSurface::WetFields(Seed);
					Check(SF.find("wetSetFrom=bind-time-seed/no-condition-was-"
					              "applied-after-it") != std::string::npos,
					      "and a surface no condition ever re-drove says the value "
					      "is the bind's own seed, which is not the same finding "
					      "as a condition having chosen it", SF);
					LedgerSurface::Bound Un; Un.Surface = "asphalt";
					Check(LedgerSurface::WetFields(Un).find("wetSetFrom=") != std::string::npos,
					      "and a surface nothing was set on still carries the key, "
					      "so a grep over the surface lines has the same "
					      "denominator on every row");
				}
			}
		}
		// EveryTokenIsKeyValue AND NOT THE ONE-EQUALS FORM, and the reason is
		// a value this project already prints: a decoder's own words are
		// `JPEG-BGRA8/srgb=no`, so a map line legitimately carries a second
		// equals inside one value. The rule that matters is the one every
		// reader here depends on, which is no WHITESPACE inside a value.
		// FROM surfaceStatus ONWARD, because a surface line opens with the word
		// `surface` and the surface's name, which are a row label and not keys.
		// EveryTokenIsKeyValue and not the one-equals form, for a reason this
		// project's own strings establish: a decoder's words are
		// `JPEG-BGRA8/srgb=no`, so a map value legitimately carries a second
		// equals. The rule every reader here depends on is no WHITESPACE in a
		// value.
		Check(EveryTokenIsKeyValue(SurfLine.substr(SurfLine.find("surfaceStatus=")))
		      && EveryTokenIsKeyValue(BlendLine.substr(BlendLine.find("surfaceStatus=")))
		      && NoSpacePastPrefix(Seg, "piecesPainted="),
		      "every value on all three is space-free and is a key with a value");
		std::vector<LedgerSurface::Bound> All;
		All.push_back(B);
		std::vector<std::string> Tried;
		Tried.push_back("C:/staged/LedgerProbe/CityPackTextures");
		const std::string Done = LedgerSurface::MaterialsDoneLine(
			All, "/Game/Ledger/M_LedgerSurface", true, "C:/pack", 51, Tried,
			610, 3, 600, 2.0) + Seg;
		std::vector<std::string> DoneKeys, SurfKeys;
		KeysOf(Done, DoneKeys);
		KeysOf(SurfLine, SurfKeys);
		std::string Shared;
		for (size_t I = 0; I < SurfKeys.size(); ++I)
		{
			for (size_t J = 0; J < DoneKeys.size(); ++J)
			{
				if (SurfKeys[I] == DoneKeys[J])
				{
					if (!Shared.empty()) { Shared += "/"; }
					Shared += SurfKeys[I];
				}
			}
		}
		Check(Shared.empty(),
		      "the census on the materials line shares no key with a surface line",
		      Shared);
		Check(EveryTokenIsKeyValue(Done),
		      "and the joined materials line is every token a key with a value");
	}
	// ONE LINE PER DECAL, AND THE PASS'S OWN DONE LINE.
	{
		LedgerSurface::DecalResult Card;
		Card.Piece = "decal_00_fascia_mickeys"; Card.Blend = "card";
		Card.Id = "generated/fascia_mickeys"; Card.bCropAsked = true;
		Card.bLoaded = true; Card.bPainted = true;
		Card.FullW = 1024; Card.FullH = 1024;
		Card.LoadedAs = "PNG-BGRA8/srgb=yes";
		Card.Crop = LedgerSurface::CropPixels(LedgerSurface::SplitDecalAsset(
			"generated/fascia_mickeys#0.0391,0.2773,0.9766,0.7168"), 1024, 1024);
		Card.Note = "opaque-card/cropped-at-decode";
		const std::string CL = LedgerSurface::DecalLine(Card);
		std::printf("    %s\n", CL.c_str());
		Check(CL.find("decalStatus=PAINTED") != std::string::npos
		      && CL.find("decalCropSize=960x450") != std::string::npos,
		      "a painted card names its picture, its status and the size it was cut to");
		Check(CL.find("decalRowOrder=") != std::string::npos,
		      "and every decal line carries which way round the rows went");
		LedgerSurface::DecalResult Stain;
		Stain.Piece = "decal_17_Moss001"; Stain.Blend = "multiply";
		Stain.Id = "ambientcg/Moss001"; Stain.bHidden = true;
		Stain.Note = "needs-a-modulate-material";
		const std::string SL = LedgerSurface::DecalLine(Stain);
		Check(SL.find("decalStatus=HIDDEN") != std::string::npos
		      && SL.find("decalLoadedAs=not-loaded") != std::string::npos,
		      "a stain that could not be drawn says HIDDEN and never prints a size it "
		      "does not have");
		Check(EveryTokenIsKeyValue(CL) && EveryTokenIsKeyValue(SL),
		      "both decal lines are space-free keys with values, the rule every "
		      "reader of this file depends on");
		std::vector<LedgerSurface::DecalResult> All;
		All.push_back(Card); All.push_back(Stain);
		std::vector<std::string> Tried;
		Tried.push_back("C:/staged/LedgerProbe/LedgerDecals");
		const std::string D = LedgerSurface::DecalsDoneLine(All, "C:/staged/LedgerDecals",
		                                                    40, Tried);
		std::printf("   %s\n", D.c_str());
		Check(D.find("decalsPainted=1/2") != std::string::npos
		      && D.find("decalsHidden=1/2") != std::string::npos
		      && D.find("decalsByBlend=card.1/multiply.1") != std::string::npos,
		      "the pass's totals ship over the decal pieces it examined");
		Check(D.find("decalsStatus=PARTIAL") != std::string::npos,
		      "one of two painted is PARTIAL and says so");
		Check(D.find("decalFlip=rows.no/cols.no") != std::string::npos,
		      "the uv winding lever is printed rather than hidden in the source");
		const std::vector<LedgerSurface::DecalResult> NoneAtAll;
		const std::string ND = LedgerSurface::DecalsDoneLine(NoneAtAll, "", 0, Tried);
		Check(ND.find("decalsPainted=nothing-measured") != std::string::npos
		      && ND.find("decalRoot=NOT-FOUND") != std::string::npos
		      && ND.find("decalRootTried=C:/staged/LedgerProbe/LedgerDecals")
		         != std::string::npos,
		      "a pass that reached no decal prints the words, and a root it did not "
		      "find NAMES where it looked");
		std::vector<std::string> DoneKeys, LineKeys;
		KeysOf(D, DoneKeys);
		KeysOf(CL, LineKeys);
		std::string Shared;
		for (size_t I = 0; I < LineKeys.size(); ++I)
		{
			for (size_t J = 0; J < DoneKeys.size(); ++J)
			{
				if (LineKeys[I] == DoneKeys[J])
				{
					if (!Shared.empty()) { Shared += "/"; }
					Shared += LineKeys[I];
				}
			}
		}
		Check(Shared.empty(),
		      "the per-decal line and the decal done line share no key name", Shared);
	}
	// ---- THE CONTROL QUADS, PLACED AGAINST THE COMMITTED CAMERA ---------
	//
	// THE ACCEPTING FIXTURE IS THE LIVE FILE, which is this project's rule
	// for a tool that checks the project itself: the quads are placed from
	// the camera the committed spec carries, so a camera moved in the file
	// moves them here and this test says whether they are still in frame.
	{
		const LedgerVignette::Camera* CtrlCam = 0;
		for (size_t I = 0; I < S.Cameras.size(); ++I)
		{
			if (S.Cameras[I].Id == LedgerSurface::ControlCameraId())
			{
				CtrlCam = &S.Cameras[I];
			}
		}
		if (CtrlCam == 0)
		{
			std::printf("    control quads: nothing measured, the spec carries no camera "
			            "named by ControlCameraId\n");
		}
		else
		{
			Check(LedgerSurface::ControlQuadCount() == 3,
			      "three controls: one for the texture path and a PAIR for the scalar path");
			int InFrame = 0, Ahead = 0;
			for (int I = 0; I < LedgerSurface::ControlQuadCount(); ++I)
			{
				const LedgerSurface::QuadPlace P = LedgerSurface::ControlQuadPlace(*CtrlCam, I);
				const LedgerSurface::ScreenBox B =
					LedgerSurface::ControlQuadBox(*CtrlCam, P, 1280, 720);
				std::printf("    quad %-6s at %.2f/%.2f/%.2f m  centre %.0f/%.0f px  "
				            "box x%.0f..%.0f y%.0f..%.0f  dist %.2f m  inFrame %d/4\n",
				            P.Id.c_str(), P.XM, P.YM, P.ZM, B.CxPx, B.CyPx,
				            B.X0, B.X1, B.Y0, B.Y1, B.DistM, B.CornersInFrame);
				if (B.CornersAhead == 4) { ++Ahead; }
				if (B.CornersInFrame == 4) { ++InFrame; }
			}
			Check(Ahead == LedgerSurface::ControlQuadCount(),
			      "every control stands in front of the camera, all four corners of it");
			Check(InFrame == LedgerSurface::ControlQuadCount(),
			      "and every corner of every control lands inside 1280x720, which is "
			      "the whole point of placing them from the camera's own numbers");
			// THE ROW IS TO THE LEFT, WHICH IS A DECISION ABOUT THE EVIDENCE
			// FRAME AND IS ASSERTED SO IT CANNOT DRIFT SILENTLY: the frame is
			// cam_B, the control camera since 2026-09-21, which no judged
			// reading is taken from.
			const LedgerSurface::QuadPlace P0 = LedgerSurface::ControlQuadPlace(*CtrlCam, 0);
			const LedgerSurface::QuadPlace P2 = LedgerSurface::ControlQuadPlace(*CtrlCam, 2);
			const LedgerSurface::ScreenBox B0 =
				LedgerSurface::ControlQuadBox(*CtrlCam, P0, 1280, 720);
			const LedgerSurface::ScreenBox B2 =
				LedgerSurface::ControlQuadBox(*CtrlCam, P2, 1280, 720);
			Check(B0.CxPx < 640.0 && B2.CxPx < B0.CxPx,
			      "the controls sit left of centre and in the order they are numbered");
			Check(LedgerSurface::ControlQuadTiling(1) != LedgerSurface::ControlQuadTiling(2)
			      && LedgerSurface::ControlQuadPlace(*CtrlCam, 1).SizeM
			         == LedgerSurface::ControlQuadPlace(*CtrlCam, 2).SizeM,
			      "the two tile quads differ in their tiling and in NOTHING else, "
			      "which is what makes the pair readable in one still");
			Check(LedgerSurface::ControlQuadBindsTexture(0)
			      && !LedgerSurface::ControlQuadBindsTexture(1)
			      && !LedgerSurface::ControlQuadBindsTexture(2),
			      "exactly one control binds a texture, so the checker on the other "
			      "two is the base material's own default and not an accident");
			// THE ROTATION IS DERIVED FROM THE CAMERA, and a quad facing away
			// is culled or lit from behind, which is the sign error the decal
			// quads paid for once already.
			Check(P0.EnginePitchDeg == 90.0 && P0.EngineYawDeg == CtrlCam->YawDeg,
			      "the plane is pitched a quarter turn so its normal faces the camera, "
			      "and it carries the camera's yaw so it does at any yaw");
			// AND THE FOUR COLOURS, WHICH ARE THE WHOLE READING.
			int MinChroma = 255;
			for (int I = 0; I < LedgerSurface::ControlColourCount(); ++I)
			{
				int R = 0, G = 0, B = 0;
				LedgerSurface::ControlColour(I, R, G, B);
				const int Hi = (R > G ? (R > B ? R : B) : (G > B ? G : B));
				const int Lo = (R < G ? (R < B ? R : B) : (G < B ? G : B));
				if (Hi - Lo < MinChroma) { MinChroma = Hi - Lo; }
			}
			Check(MinChroma == 255,
			      "every control colour is at a corner of the cube, so none of them "
			      "can be confused with a frame whose measured maximum chroma is 15");
			// ONE QUAD'S LINE, BOTH WAYS ROUND THE TRANSFORM READBACK.
			LedgerSurface::QuadResult R;
			R.bSpawned = true; R.bMidMade = true; R.bTexMade = true;
			R.bTexResource = true; R.bTexReadback = true; R.bCompIsMid = true;
			R.bRead = true;
			R.ReadXCm = P0.XCm; R.ReadYCm = P0.YCm; R.ReadZCm = P0.ZCm;
			const std::string QL = LedgerSurface::ControlQuadLine(*CtrlCam, P0, R, 1280, 720);
			std::printf("    %s\n", QL.c_str());
			Check(QL.find("controlQuad=colour") == 0,
			      "the control line names itself first, as the surface lines do");
			Check(QL.find("quadTexels=texel0.red.255.0.0/texel1.green.0.255.0/"
			              "texel2.blue.0.0.255/texel3.yellow.255.255.0") != std::string::npos,
			      "the line carries the four colours ASKED FOR, in the order the "
			      "memcpy writes them, so the still can be read against it");
			Check(QL.find("quadDeltaCm=0.00") != std::string::npos,
			      "a quad that landed where it was asked to prints a zero delta");
			Check(QL.find("quadCentrePx=") != std::string::npos
			      && QL.find("quadBoxPx=x") != std::string::npos,
			      "and it says WHERE ON SCREEN to look, in pixels, not in prose");
			Check(NoSpacePastPrefix(QL, "quadStatus="),
			      "every value on a control line is one space-free token with one equals");
			LedgerSurface::QuadResult NoRead = R;
			NoRead.bRead = false;
			const std::string QN = LedgerSurface::ControlQuadLine(*CtrlCam, P0, NoRead, 1280, 720);
			Check(QN.find("quadReadXYZcm=not-read") != std::string::npos
			      && QN.find("quadDeltaCm=not-read") != std::string::npos,
			      "an actor that never answered for its transform says so rather than "
			      "printing the request back as though it were a reading");
			// THE PASS'S OWN DONE LINE, both ways round the empty case.
			std::vector<LedgerSurface::QuadResult> Quads;
			const std::string Empty = LedgerSurface::ControlQuadsDoneLine(Quads, true);
			Check(Empty.find("controlQuadsStatus=NOT-REACHED") != std::string::npos
			      && Empty.find("controlQuads=nothing-measured/3") != std::string::npos,
			      "a control pass that spawned nothing says the words and still ships "
			      "the count of what it was asked for");
			Quads.push_back(R); Quads.push_back(R); Quads.push_back(R);
			const std::string Done = LedgerSurface::ControlQuadsDoneLine(Quads, true);
			std::printf("    %s\n", Done.c_str());
			Check(Done.find("controlQuadsStatus=ALL") != std::string::npos
			      && Done.find("controlQuads=3/3") != std::string::npos
			      && Done.find("controlQuadMids=3/3") != std::string::npos,
			      "a control pass that made all three prints all three with denominators");
			Check(NoSpacePastPrefix(Done, "controlQuadsStatus="),
			      "and the done line is space-free past its first key");
		}
	}
	// ---- cam_hook, RUNG 1 OF production/ladder.md ------------------------
	//
	// THE VIEWPOINT OF THE LOWER PANEL of the Hook concept sheet, checked
	// against the panel's own MEASURED composition rather than against a
	// number anybody liked the look of. The three panel numbers quoted below
	// were read off the file at production/art/atlas-01/concepts/hook.png on
	// branch origin/art/atlas-01, whose street panel is 1002 by 617 pixels:
	// the horizon at row 348 (0.5640 of the height), the street axis
	// vanishing at column 332 (0.3313 of the width), and the nearest ground
	// at the bottom edge 4.15 m ahead. They are the reference, so a check
	// against them is a check against a measurement.
	//
	// AND THE HALF NOBODY WOULD THINK TO ASK FOR: the three material control
	// quads are placed 3.5 m in front of LedgerSurface::ControlCameraId(),
	// cam_B since the 2026-09-21 ruling and not this camera, so nothing in
	// their placement knows this camera exists. A frame with colour swatches
	// standing in the road is not a frame anybody can judge a street by, so
	// where they land in THIS camera's frame is measured here rather than
	// discovered in the still.
	{
		const LedgerVignette::Camera* Hook = 0;
		// AND THE CAMERA THE QUADS ARE PLACED FROM, looked up by the SAME rule
		// the engine reads, LedgerSurface::ControlCameraId(), so this block
		// cannot drift from the placement it claims to measure.
		const LedgerVignette::Camera* QuadCam = 0;
		for (size_t I = 0; I < S.Cameras.size(); ++I)
		{
			if (S.Cameras[I].Id == "cam_hook") { Hook = &S.Cameras[I]; }
			if (S.Cameras[I].Id == LedgerSurface::ControlCameraId())
			{
				QuadCam = &S.Cameras[I];
			}
		}
		Check(QuadCam != 0,
		      "the committed spec carries the camera ControlCameraId names, "
		      "which is the accepting case for the rule the engine reads");
		Check(!S.Shots.empty()
		      && std::string(LedgerSurface::ControlCameraId()) != S.Shots[0].CameraId
		      && std::string(LedgerSurface::ControlCameraId()) != "cam_hook",
		      "and the controls stand in front of neither the first shot's camera "
		      "(the figure's frame) nor cam_hook (the sheet's), ruled 2026-09-21");
		if (Hook == 0 || QuadCam == 0)
		{
			std::printf("    cam_hook: nothing measured, the committed spec carries no "
			            "camera of that id or no camera named by ControlCameraId\n");
		}
		else
		{
			std::printf("    cam_hook at x=%.2f z=%.2f groundY=%.4f (%s) eye=%.2f "
			            "yaw=%.1f pitch=%.1f vfov=%.1f hfov=%.2f\n",
			            Hook->X, Hook->Z, Hook->GroundY, Hook->GroundEdge.c_str(),
			            Hook->EyeHeightM, Hook->YawDeg, Hook->PitchDeg,
			            Hook->FovVerticalDeg,
			            LedgerVignette::HorizontalFovDeg(Hook->FovVerticalDeg, 1280, 720));
			// THE CAMERA STANDS ON THE QUAY APRON, 23 September. It stood in
			// the west carriageway while it reproduced the RETIRED panel; the
			// approved sheet's lens puts it 3.2 m south of where this street
			// starts, on the apron at crown level, which the scene file does
			// not build, so it DECLARES that ground and the emitter names it
			// as declared. What this still refuses is a camera on no ground.
			Check(Hook->GroundFound && Hook->GroundEdge == "declared/quay_apron_at_crown_level",
			      "cam_hook stands on the quay apron it declares, where the approved "
			      "sheet's lens puts it",
			      Hook->GroundEdge);
			Check(Hook->Z > -3.0 + 0.255 && Hook->Z < -0.5,
			      "and it is between the west channel and the crown, which is the "
			      "near-kerb half of the carriageway rather than the middle of it");
			// THE HORIZON AND THE VANISHING POINT, against the panel's own
			// rows and columns. The tolerance is one percent of the frame,
			// which is 7 rows of 720, and both numbers are printed.
			const LedgerSurface::ScreenAt Hor = LedgerSurface::ProjectFilePoint(
				*Hook, Hook->X + 2000.0, Hook->GroundY + Hook->EyeHeightM, Hook->Z,
				1280, 720);
			const LedgerSurface::ScreenAt Van = LedgerSurface::ProjectFilePoint(
				*Hook, Hook->X + 2000.0, Hook->GroundY, Hook->Z, 1280, 720);
			const double HorFrac = Hor.Py / 720.0;
			const double VanFrac = Van.Px / 1280.0;
			std::printf("    cam_hook horizonRowFrac=%.4f panel=0.5640 "
			            "vanishColFrac=%.4f panel=0.3313\n", HorFrac, VanFrac);
			Check(Hor.bAhead && HorFrac > 0.5,
			      "the horizon sits BELOW the middle of the frame, as the panel's "
			      "does, which is what a camera tilted slightly up looks like");
			Check(std::fabs(HorFrac - 0.5640) < 0.01,
			      "and it lands within one percent of the frame height of the row "
			      "measured off the panel");
			Check(Van.bAhead && VanFrac < 0.5,
			      "the street axis vanishes LEFT of centre, as the panel's does, "
			      "which for a pinhole camera can only be a rotation");
			// WHERE THE THREE CONTROL QUADS LAND IN THIS FRAME. Their centres
			// and their two lateral extremes, because a centre just outside
			// the edge with 0.35 m of quad beside it is still in the picture.
			int CentresIn = 0, EdgesIn = 0, Ahead4 = 0;
			for (int I = 0; I < LedgerSurface::ControlQuadCount(); ++I)
			{
				const LedgerSurface::QuadPlace P =
					LedgerSurface::ControlQuadPlace(*QuadCam, I);
				// The quad faces the camera it was placed from, so its own
				// width runs along THAT camera's right vector and not along
				// this one's.
				const double QuadCamYaw = LedgerSurface::DegToRad(QuadCam->YawDeg);
				const double Rx = -std::sin(QuadCamYaw), Rz = std::cos(QuadCamYaw);
				const double Half = LedgerSurface::ControlQuadSizeM() * 0.5;
				const LedgerSurface::ScreenAt C0 = LedgerSurface::ProjectFilePoint(
					*Hook, P.XM, P.YM, P.ZM, 1280, 720);
				const LedgerSurface::ScreenAt L = LedgerSurface::ProjectFilePoint(
					*Hook, P.XM - Rx * Half, P.YM, P.ZM - Rz * Half, 1280, 720);
				const LedgerSurface::ScreenAt R2 = LedgerSurface::ProjectFilePoint(
					*Hook, P.XM + Rx * Half, P.YM, P.ZM + Rz * Half, 1280, 720);
				const bool CIn = C0.bAhead && C0.Px >= 0 && C0.Px <= 1280
				                 && C0.Py >= 0 && C0.Py <= 720;
				const bool EIn = (L.bAhead && L.Px >= 0 && L.Px <= 1280
				                  && L.Py >= 0 && L.Py <= 720)
				                 || (R2.bAhead && R2.Px >= 0 && R2.Px <= 1280
				                     && R2.Py >= 0 && R2.Py <= 720);
				if (C0.bAhead && L.bAhead && R2.bAhead) { ++Ahead4; }
				if (CIn) { ++CentresIn; }
				if (EIn) { ++EdgesIn; }
				std::printf("    quad %-6s seen from cam_hook: centre %.0f/%.0f px "
				            "edges %.0f..%.0f px fwd %.2f m inFrameCentre=%s "
				            "inFrameEitherEdge=%s\n",
				            P.Id.c_str(), C0.Px, C0.Py, L.Px, R2.Px, C0.ForwardM,
				            CIn ? "yes" : "no", EIn ? "yes" : "no");
			}
			std::printf("    cam_hook controlQuadsInFrame centres=%d/%d "
			            "eitherEdge=%d/%d ahead=%d/%d\n",
			            CentresIn, LedgerSurface::ControlQuadCount(),
			            EdgesIn, LedgerSurface::ControlQuadCount(),
			            Ahead4, LedgerSurface::ControlQuadCount());
			// AND THE RULE THAT KEEPS THEM OUT OF THE JUDGED FRAME, both
			// outcomes watched and the ACCEPTING one first: the camera the
			// quads were placed from still sees them, and every other camera
			// does not. The measurement above is why the rule exists, and it
			// is printed whatever the rule says, so a future placement that
			// stops intruding shows up as a reading rather than as silence.
			Check(LedgerSurface::ControlQuadsVisibleFor(QuadCam->Id, QuadCam->Id),
			      "the camera the controls were placed from still photographs them, "
			      "which is the frame the material evidence is read from");
			Check(!LedgerSurface::ControlQuadsVisibleFor(Hook->Id, QuadCam->Id),
			      "and cam_hook does not, which is what stops an instrument standing "
			      "in the picture rung 1 is judged by");
			Check(!LedgerSurface::ControlQuadsVisibleFor("", QuadCam->Id)
			      && !LedgerSurface::ControlQuadsVisibleFor(QuadCam->Id, ""),
			      "an unnamed camera on either side hides them rather than guessing");
			std::printf("    cam_hook controlQuadIntrusion=%s centres=%d/%d edges=%d/%d "
			            "(this is WHY the rule above exists, and it is measured "
			            "rather than assumed; since 2026-09-21 the hide rule is the "
			            "only guard and the word says so)\n",
			            EdgesIn == 0 ? "none-reaches-the-frame"
			            : (CentresIn == 0 ? "edges-only-reach-the-frame"
			                              : "centres-in-frame/hidden-by-the-rule-alone"),
			            CentresIn, LedgerSurface::ControlQuadCount(),
			            EdgesIn, LedgerSurface::ControlQuadCount());
			const std::string VLine =
				LedgerSurface::ControlQuadVisibilityLine(5, 1, "vign_hook_day");
			std::printf("    %s\n", VLine.c_str());
			Check(VLine.find("controlQuadHidden=1/5") != std::string::npos
			      && VLine.find("controlQuadHiddenOn=vign_hook_day") != std::string::npos,
			      "the visibility line carries the count, its denominator and the ids");
			Check(LedgerSurface::ControlQuadVisibilityLine(0, 0, "").find(
			          "nothing-measured") != std::string::npos,
			      "a run that took no shot says nothing measured rather than zero");
			// A1(d): EVERY SAMPLE LINE DECLARES WHETHER ITS OWN WHOLE-FRAME
			// KEYS INCLUDE THE INSTRUMENT. Accepting case first, and the
			// accepting case is the camera that DOES carry them, because that
			// is the line a reader of shotMeanLuma has to be warned about.
			// The boxes are projected here rather than quoted from a document:
			// the percentage moves if the camera, the field of view or the
			// placement constants move, which is what a frozen literal could
			// not do.
			const std::string QA = LedgerSurface::ShotControlQuadLine(
				*QuadCam, QuadCam->Id, LedgerSurface::ControlQuadCount(), true, 1280, 720);
			const std::string QH = LedgerSurface::ShotControlQuadLine(
				*Hook, QuadCam->Id, LedgerSurface::ControlQuadCount(), true, 1280, 720);
			std::printf("    %s\n    %s\n", QA.c_str(), QH.c_str());
			Check(QA.find("shotWholeFrameIncludesControlQuads=yes/whole-frame-keys-on-this-"
			              "line-include-them/boxes=see-controlQuadVisibility-and-the-quad-"
			              "lines/PROJECTED-BOXES-NOT-MEASURED-COVERAGE") != std::string::npos,
			      "the shot taken from the camera the controls were placed from declares "
			      "that its own whole-frame keys include them, in the words the ruling "
			      "dictated", QA);
			Check(QA.find("shotControlQuadsBoxed=3/of=3/") != std::string::npos
			      && QA.find("shotControlQuadsBoxPx=x") != std::string::npos,
			      "and it carries the projected boxes with their denominator rather than "
			      "a literal copied out of a document", QA);
			Check(QH == "shotWholeFrameIncludesControlQuads=no/hidden-for-this-camera",
			      "a shot from any other camera declares no, which is the case rung 1's "
			      "own frame is in", QH);
			// AND THE THREE REFUSALS, because "no" is a claim about a frame
			// and a run that did not know its camera, did not spawn the quads
			// or did not measure the frame must not make it.
			Check(LedgerSurface::ShotControlQuadLine(*QuadCam, "", 3, true, 1280, 720)
			          .find("nothing-measured/no-camera-identity-answered") != std::string::npos
			      && LedgerSurface::ShotControlQuadLine(*QuadCam, QuadCam->Id, 0, true,
			                                            1280, 720)
			          .find("no/no-control-quads-were-spawned-in-this-build")
			          != std::string::npos
			      && LedgerSurface::ShotControlQuadLine(*QuadCam, QuadCam->Id, 3, false,
			                                            1280, 720)
			          .find("nothing-measured/this-line-carries-no-whole-frame-keys")
			          != std::string::npos,
			      "an unnamed camera, a build that spawned no quads and a line with no "
			      "whole-frame keys each say so rather than answering yes or no");
			Check(EveryTokenIsKeyValue(QA) && EveryTokenIsKeyValue(QH),
			      "both control-quad declarations are space-free, every token a key "
			      "with a value", QA);
			// THE AT-MOST PERCENTAGE IS A PROJECTION AND THE SERIES IS PRINTED
			// BEFORE ANY BOUND IS SET. No gate reads it tonight; the point of
			// printing three fields of view is that a later session sets its
			// bound off a read series rather than off one frame, which is what
			// froze the number the earlier ruling dictated as a literal.
			//
			// THE VARIABLE IS THE FIELD OF VIEW AND NOT THE FRAME SIZE, and
			// that is itself a reading taken here: the union box scales with
			// the frame, so 1280x720 and 640x360 return the SAME percentage
			// and printing both would be one number twice. The fov moves it.
			{
				const double Fovs[3] = {QuadCam->FovVerticalDeg, 39.0, 90.0};
				std::printf("    controlQuadAtMost series, one projection per field of "
				            "view, 1280x720 throughout, 3 of 3 shown:");
				for (int FI = 0; FI < 3; ++FI)
				{
					LedgerVignette::Camera Vary = *QuadCam;
					Vary.FovVerticalDeg = Fovs[FI];
					const std::string L = LedgerSurface::ShotControlQuadLine(
						Vary, QuadCam->Id, 3, true, 1280, 720);
					const size_t At = L.find("shotControlQuadsAtMostPctOfFrame=");
					std::printf(" fovV=%.1f/%s", Fovs[FI],
					            At == std::string::npos ? "not-printed"
					            : L.substr(At + 33, L.find(' ', At) - At - 33).c_str());
				}
				std::printf("\n");
				LedgerVignette::Camera Narrow = *QuadCam;
				Narrow.FovVerticalDeg = 39.0;
				const std::string N = LedgerSurface::ShotControlQuadLine(
					Narrow, QuadCam->Id, 3, true, 1280, 720);
				Check(QA.find("shotControlQuadsAtMostPctOfFrame=0.00") == std::string::npos
				      && N != QA,
				      "the at-most percentage is a projection that moves with the field of "
				      "view and not a literal, which is why no bound is set on it here",
				      QA + " | " + N);
			}
		}
	}
	// THE SEARCH-PATH FORMATTER ON ITS OWN, both ways round the cap, because
	// a cap that is never exercised is a claim rather than a measurement.
	{
		std::vector<std::string> P;
		Check(LedgerSurface::PathListValue(P, 8) == "nothing-tried",
		      "a search that asked about no directory at all says the words, not empty");
		P.push_back("D:/a/one two/CityPackTextures");
		Check(LedgerSurface::PathListValue(P, 8) == "D:/a/one~two/CityPackTextures",
		      "a path with a space in it cannot split a key=value reader's line");
		P.push_back("D:/b/CityPackTextures");
		Check(LedgerSurface::PathListValue(P, 8)
		      == "D:/a/one~two/CityPackTextures,D:/b/CityPackTextures",
		      "two candidates join on a comma, because a slash is inside every path");
		Check(LedgerSurface::PathListValue(P, 8).find("more-not-shown") == std::string::npos,
		      "and a cap that did not bite says nothing at all");
		Check(LedgerSurface::PathListValue(P, 1)
		      == "D:/a/one~two/CityPackTextures,+1-more-not-shown",
		      "a cap that BITES announces itself and prints how many it withheld");
	}
	// ---- THE PACK ON DISK, WHICH IS THE HALF THAT ANSWERS D1's QUESTION --
	//
	// This is the accepting fixture for the RESOLUTION rule: the same
	// filenames the Unreal run will try, tried here against the same
	// committed pack. It is skipped rather than failed where the pack is not
	// checked out, and a skip PRINTS ITS DENOMINATOR so that "nothing found"
	// and "nothing looked at" cannot read alike.
	{
		std::string Root(SpecPath);
		const size_t Cut = Root.find("production/specs/");
		if (Cut == std::string::npos) { Root.clear(); }
		else { Root = Root.substr(0, Cut) + "ledger/Assets/StreamingAssets/CityPack/textures/"; }
		const std::vector<LedgerSurface::Ask> Asked = LedgerSurface::SurfacesAsked(S.Pieces);
		int Resolved = 0, Absent = 0, Examined = 0;
		std::string AbsentNames;
		for (size_t I = 0; I < Asked.size() && !Root.empty(); ++I)
		{
			++Examined;
			bool bFound = false;
			const std::vector<std::string> C = LedgerSurface::Candidates(Asked[I].Surface, 0);
			for (size_t J = 0; J < C.size() && !bFound; ++J)
			{
				std::ifstream F((Root + C[J]).c_str(), std::ios::binary);
				if (F.good()) { bFound = true; }
			}
			if (bFound) { ++Resolved; }
			else
			{
				++Absent;
				if (!AbsentNames.empty()) { AbsentNames += "/"; }
				AbsentNames += Asked[I].Surface;
			}
		}
		if (Examined == 0)
		{
			std::printf("    pack: nothing measured, no CityPack textures directory under %s\n",
			            SpecPath);
		}
		else
		{
			std::printf("    pack: albedoResolved=%d/%d albedoAbsent=%s root=%s\n",
			            Resolved, Examined, AbsentNames.empty() ? "none" : AbsentNames.c_str(),
			            Root.c_str());
			Check(Resolved + Absent == Examined,
			      "every surface examined against the pack is either resolved or named absent");
			Check(Resolved > 0,
			      "the committed pack answers at least one surface, so the rule is exercised");
		}
	}

	// ---- QUEUE 186: THE SKY SEGMENT, ACCEPTING CASE FIRST ----------------
	//
	// Rule 5b, in the order it says: the case this must PASS is a whole sky
	// with the fills retired, because that is the state the change exists to
	// produce and a formatter that cannot print it is worth nothing. The
	// refusals come after, each with the condition PLANTED rather than
	// waited for.
	{
		LedgerVignette::SkyIn In;
		In.bSkyLightActor = true; In.bSkyLightComponent = true;
		In.bAtmosphereActor = true; In.bAtmosphereComponent = true;
		In.bFogComponent = true;
		In.SourceTypeRead = 0;
		In.bRealTimeCaptureRead = true;
		In.SkyIntensityRead = 1.0;
		In.FogDensityRead = 0.012;
		In.FogMaxOpacityRead = 0.45;
		In.bFillsRetired = true;
		In.FillsSpawned = 3;
		In.ApplyCalls = 12; In.SkyWrites = 2;
		In.HdriAsked = "Sky/polyhaven/belfast_open_field_2k";
		In.HdriFoundAt = "NOT-FOUND";
		In.HdriDetectedAs = "not-read";
		In.HdriBoundAs = "NOTHING/no-cube-texture-is-built-at-runtime-in-this-change";
		const std::string L = LedgerVignette::SkySegment(In);
		std::printf("    %s\n", L.c_str());
		Check(L.find("skyModel=skyatmosphere+skylight-realtime-capture/not-an-hdri")
		      != std::string::npos,
		      "a whole sky names its mechanism and says it is not an HDRI");
		Check(L.find("ambientModel=skylight-captured-sky/ONE-OWNER/trilight-retired-to-zero")
		      != std::string::npos,
		      "and names one owner for the ambient when the fills are retired");
		Check(L.find("skyWrites=2/of=12/") != std::string::npos,
		      "write-on-change prints both counts, so a per-tick rebuild would be visible");
		Check(L.find("skyRealTimeCaptureRead=yes") != std::string::npos
		      && L.find("skySourceTypeRead=0") != std::string::npos,
		      "the capture mode is printed as the component reported it, enum value and all");
		Check(L.find("fogMaxOpacityRead=0.450") != std::string::npos
		      && L.find("fogDensityRead=0.0120") != std::string::npos,
		      "the fog's two numbers are read back beside the sky that now shares the far field");
		Check(L.find("skyHdriBoundAs=NOTHING/") != std::string::npos,
		      "the named HDRI reports plainly that nothing was bound from it");
		Check(EveryTokenIsKeyValue(L),
		      "every sky value is space-free, so no reader truncates it silently");
	}
	{
		// AN ATMOSPHERE WITH NO SKYLIGHT: visible sky, nothing capturing it,
		// so nothing to reflect. It must not read as a whole sky.
		LedgerVignette::SkyIn In;
		In.bAtmosphereActor = true; In.bAtmosphereComponent = true;
		In.FillsSpawned = 3;
		const std::string L = LedgerVignette::SkySegment(In);
		Check(!In.Whole()
		      && L.find("skyModel=SKYLIGHT-MISSING/") != std::string::npos,
		      "an atmosphere with no skylight names the half that is missing");
		Check(L.find("ambientModel=trilight-3-directional/not-a-captured-sky/the-sky-is-not-whole")
		      != std::string::npos,
		      "and the ambient stays with the tri-light rather than claiming a captured sky");
	}
	{
		// A SKYLIGHT WITH NO ATMOSPHERE captures a black scene. That is the
		// exact failure the fill-light comment in VignetteShot.cpp warned
		// about, and it must be a NAMED state and not a dark frame.
		LedgerVignette::SkyIn In;
		In.bSkyLightActor = true; In.bSkyLightComponent = true;
		In.FillsSpawned = 3;
		const std::string L = LedgerVignette::SkySegment(In);
		Check(L.find("skyModel=ATMOSPHERE-MISSING/skylight-would-capture-a-black-scene")
		      != std::string::npos,
		      "a skylight with nothing to capture says so instead of reporting a sky");
	}
	{
		// NOTHING SPAWNED AT ALL. The far field is then still the height fog,
		// which is what the frames of 2026-09-09 actually showed, and the
		// word must say that rather than "black".
		const LedgerVignette::SkyIn In;
		const std::string L = LedgerVignette::SkySegment(In);
		std::printf("    %s\n", L.c_str());
		Check(L.find("skyModel=SPAWN-FAILED/no-sky-of-any-kind/the-far-field-is-the-height-fog")
		      != std::string::npos,
		      "no sky at all names the height fog as what fills the far field");
		Check(L.find("skyHdriAsked=none") != std::string::npos
		      && L.find("skyHdriFoundAt=NOT-LOOKED-FOR") != std::string::npos,
		      "a run that never looked for the HDRI says so rather than printing NOT-FOUND");
		Check(L.find("skyWrites=0/of=0/") != std::string::npos,
		      "zero writes ship the zero calls they are over");
		Check(EveryTokenIsKeyValue(L), "the spawn-failed sky line is space-free too");
	}
	{
		// A WHOLE SKY THAT DID NOT TAKE THE AMBIENT. Two contributors is a
		// real state and the line must name it as two rather than as one.
		LedgerVignette::SkyIn In;
		In.bSkyLightActor = true; In.bSkyLightComponent = true;
		In.bAtmosphereActor = true; In.bAtmosphereComponent = true;
		In.bFillsRetired = false; In.FillsSpawned = 3;
		const std::string L = LedgerVignette::SkySegment(In);
		Check(L.find("ambientModel=skylight+trilight/TWO-CONTRIBUTORS/") != std::string::npos,
		      "a sky that did not take ownership prints two contributors, not one owner");
	}

	// ---- AMENDMENT A1: THE WORD IS DERIVED FROM A READ, NOT ASSERTED -----
	//
	// WHAT WAS WRONG. skyModel said the atmosphere behind the dome "lights
	// and is captured" whenever a photograph was bound and the sky was
	// whole, from two booleans neither of which knows what the sky light
	// captured. The sky light is SLS_CapturedScene with real-time capture
	// on, and a closed 2000 m dome whose material carries the sky flag is
	// the only thing that capture can see. The word now comes off the flag.
	//
	// RULE 5b, ACCEPTING CASE FIRST: the case this must PASS is the one the
	// batch exists to produce, a photograph on a sky-flagged dome. The other
	// two are PLANTED, not waited for, and there are three because a read
	// has three outcomes. Rule 3b is the third: a refused read is
	// nothing-measured and must never print as a flag that was false.
	size_t A1Longest = 0;
	{
		LedgerVignette::SkyIn In;
		In.bSkyLightActor = true; In.bSkyLightComponent = true;
		In.bAtmosphereActor = true; In.bAtmosphereComponent = true;
		In.bFogComponent = true;
		In.bRealTimeCaptureRead = true; In.SourceTypeRead = 0;
		In.bFillsRetired = true; In.FillsSpawned = 3;
		In.ApplyCalls = 12; In.SkyWrites = 2;
		In.HdriAsked = "Sky/polyhaven/belfast_open_field_2k";
		In.HdriBoundAs = "photograph-longlat-png-on-an-unlit-sky-dome/lastWins=belfast";
		In.bPhotoDomeBound = true;
		In.DomeMatIsSky = LedgerVignette::SkyFlag_Yes;
		In.DomeMatIsSkyFrom = "bIsSky";
		In.DomeMatTwoSided = LedgerVignette::SkyFlag_Yes;
		In.DomeMatTwoSidedFrom = "TwoSided";
		In.DomeMatShadingModel = 0;
		In.DomeMatShadingModelFrom = "ShadingModel";
		In.SkyLightLowerHemiSolid = LedgerVignette::SkyFlag_No;
		In.SkyLightLowerHemiSolidFrom = "bLowerHemisphereIsBlack";
		const std::string L = LedgerVignette::SkySegment(In);
		std::printf("    %s\n", L.c_str());
		std::printf("    a1CapturedLineChars=%d/of=3600/buffer\n", (int)L.size());
		if (L.size() > A1Longest) { A1Longest = L.size(); }
		Check(L.find("skyModel=photograph-longlat-png-on-an-unlit-dome/isSkyFlagRead=yes/")
		      != std::string::npos
		      && L.find("the-photograph-is-captured/the-skyatmosphere-behind-it-is-OCCLUDED")
		      != std::string::npos,
		      "a sky flag that READ yes says the capture reads the photograph and the "
		      "atmosphere behind it is occluded from that capture");
		Check(L.find("ambientModel=skylight-captured-sky=THE-PHOTOGRAPH-ON-THE-DOME/")
		      != std::string::npos
		      && L.find("ONE-OWNER/trilight-retired-to-zero") != std::string::npos,
		      "and the ambient names the photograph as what the sky light captured, with "
		      "the trilight fact still beside it");
		Check(L.find("skyatmosphere-behind-it-lights-and-is-captured") == std::string::npos,
		      "and the sentence no run could have known is gone from the line");
		Check(L.find("skyDomeMatIsSky=yes/from=bIsSky") != std::string::npos
		      && L.find("skyDomeMatTwoSided=yes/from=TwoSided") != std::string::npos,
		      "each flag prints its value AND the property name it was read off");
		Check(L.find("skyDomeMatShadingModelRead=0-MSM_Unlit/from=ShadingModel")
		      != std::string::npos,
		      "the shading model prints the engine's own enum value and the local reading "
		      "of it, not one without the other");
		Check(L.find("skyLightLowerHemisphereSolid=no/from=bLowerHemisphereIsBlack")
		      != std::string::npos,
		      "and the sky light's lower hemisphere is read, which decides whether the "
		      "dome's mirrored half reaches the capture at all");
		Check(EveryTokenIsKeyValue(L),
		      "the grown line is still space-free, so no reader truncates the four reads");
	}
	{
		// THE FLAG READ NO. The seen sky and the lit sky are then two
		// different things, which is the failure the one-object position
		// warned about, and the word must say so rather than say photograph.
		LedgerVignette::SkyIn In;
		In.bSkyLightActor = true; In.bSkyLightComponent = true;
		In.bAtmosphereActor = true; In.bAtmosphereComponent = true;
		In.bFillsRetired = true; In.FillsSpawned = 3;
		In.bPhotoDomeBound = true;
		In.DomeMatIsSky = LedgerVignette::SkyFlag_No;
		In.DomeMatIsSkyFrom = "bIsSky";
		In.DomeMatTwoSided = LedgerVignette::SkyFlag_Yes;
		In.DomeMatTwoSidedFrom = "TwoSided";
		In.DomeMatShadingModel = 1;
		In.DomeMatShadingModelFrom = "ShadingModel";
		In.SkyLightLowerHemiSolid = LedgerVignette::SkyFlag_Yes;
		In.SkyLightLowerHemiSolidFrom = "bLowerHemisphereIsBlack";
		const std::string L = LedgerVignette::SkySegment(In);
		std::printf("    %s\n", L.c_str());
		if (L.size() > A1Longest) { A1Longest = L.size(); }
		Check(L.find("skyModel=photograph-longlat-png-on-an-unlit-dome/isSkyFlagRead=no/")
		      != std::string::npos
		      && L.find("the-skyatmosphere-behind-it-is-what-lights-the-street")
		      != std::string::npos,
		      "a sky flag that read NO says the capture does not read the dome and the "
		      "atmosphere is what lights");
		Check(L.find("ambientModel=TWO-OBJECTS/seenSky=the-photograph-on-the-dome/")
		      != std::string::npos,
		      "and the ambient names two objects, the seen sky and the lit sky");
		Check(L.find("skyDomeMatIsSky=no/from=bIsSky") != std::string::npos
		      && L.find("skyDomeMatShadingModelRead=1-MSM_DefaultLit/") != std::string::npos,
		      "a flag that read no prints no, and a lit dome prints the value that says so");
		Check(EveryTokenIsKeyValue(L), "the two-objects line is space-free too");
	}
	{
		// THE READ REFUSED. Rule 3b: this is nothing-measured, it is NOT a
		// no, and the difference is the whole amendment. The container that
		// writes this file cannot compile the engine module, so the property
		// spellings are a guess until a run answers; the line prints what it
		// looked for, which is what turns the next guess into a reading.
		LedgerVignette::SkyIn In;
		In.bSkyLightActor = true; In.bSkyLightComponent = true;
		In.bAtmosphereActor = true; In.bAtmosphereComponent = true;
		In.bFillsRetired = false; In.FillsSpawned = 3;
		In.bPhotoDomeBound = true;
		In.DomeMatIsSkyFrom = "bIsSky..IsSky";
		In.DomeMatTwoSidedFrom = "TwoSided..bTwoSided";
		In.DomeMatShadingModelFrom = "ShadingModel..ShadingModels";
		In.SkyLightLowerHemiSolidFrom =
			"bLowerHemisphereIsBlack..bLowerHemisphereIsSolidColor";
		const std::string L = LedgerVignette::SkySegment(In);
		std::printf("    %s\n", L.c_str());
		if (L.size() > A1Longest) { A1Longest = L.size(); }
		Check(L.find("skyModel=photograph-longlat-png-on-an-unlit-dome/"
		             "isSkyFlagRead=nothing-measured/") != std::string::npos
		      && L.find("neither-the-photograph-nor-the-atmosphere-may-be-claimed-as-what-lights")
		      != std::string::npos,
		      "an unread flag claims NEITHER sky as what lights the street");
		Check(L.find("ambientModel=nothing-measured/the-is-sky-flag-was-not-read-so-")
		      != std::string::npos,
		      "and the ambient word says nothing-measured rather than naming a sky");
		Check(L.find("isSkyFlagRead=no/") == std::string::npos
		      && L.find("skyDomeMatIsSky=no/") == std::string::npos,
		      "and a refused read is NOWHERE printed as a flag that was false");
		Check(L.find("skyDomeMatIsSky=nothing-measured/lookedFor=bIsSky..IsSky")
		      != std::string::npos
		      && L.find("skyLightLowerHemisphereSolid=nothing-measured/lookedFor="
		                "bLowerHemisphereIsBlack..bLowerHemisphereIsSolidColor")
		      != std::string::npos,
		      "and every unmeasured read names every spelling it looked for");
		Check(L.find("skyDomeMatShadingModelRead=nothing-measured/lookedFor=ShadingModel..")
		      != std::string::npos,
		      "including the shading model, which prints no number when it read none");
		Check(EveryTokenIsKeyValue(L), "the nothing-measured line is space-free too");
	}
	{
		// THE BOUND FIELDS CHANGE NOTHING WHEN NO DOME IS BOUND. Every
		// reader that predates this amendment reads what it read before.
		LedgerVignette::SkyIn In;
		In.bSkyLightActor = true; In.bSkyLightComponent = true;
		In.bAtmosphereActor = true; In.bAtmosphereComponent = true;
		In.bFillsRetired = true; In.FillsSpawned = 3;
		In.DomeMatIsSky = LedgerVignette::SkyFlag_Yes;
		In.DomeMatIsSkyFrom = "bIsSky";
		const std::string L = LedgerVignette::SkySegment(In);
		if (L.size() > A1Longest) { A1Longest = L.size(); }
		Check(L.find("skyModel=skyatmosphere+skylight-realtime-capture/not-an-hdri")
		      != std::string::npos
		      && L.find("ambientModel=skylight-captured-sky/ONE-OWNER/trilight-retired-to-zero")
		      != std::string::npos,
		      "a run with no dome bound prints exactly the two words it printed before "
		      "this amendment, whatever the material flags say");
	}
	// THE BUFFER BOUND IS MEASURED, NOT GUESSED (rule 2). Every line planted
	// above prints its own length; this is the longest of them against the
	// char array SkySegment composes into, and it is checked here because
	// snprintf truncates in silence and the keys that vanish first are the
	// ones this amendment added at the end.
	std::printf("    a1LongestSkyLineChars=%d/of=3600/buffer/stat=peak-over-%d-planted-lines\n",
	            (int)A1Longest, 4);
	Check(A1Longest > 0 && A1Longest + 64 < 3600,
	      "the longest sky line the tests can plant fits the buffer with headroom, so no "
	      "key is lost to a silent truncation");

	// ---- QUEUE 205: THE FOUR SUN KEYS, OFF THE COMPONENT ----------------
	{
		LedgerVignette::SkyIn In;
		In.bSkyLightActor = true; In.bSkyLightComponent = true;
		In.bAtmosphereActor = true; In.bAtmosphereComponent = true;
		In.SkyIntensityRead = 0.35;
		In.bSunActor = true; In.bSunComponent = true;
		In.SunIntensityRead = 30.0;
		In.bSunCastShadowsRead = true;
		// THE YAW SLOT CARRIES A YAW, NOT AN AZIMUTH. Until 2026-09-09 this
		// fixture read 205.0, which is the file's azimuth_deg; the converted
		// yaw is SunYawDeg(205) = 25.0, and a reader learning the key from
		// this test learned it wrong. Nothing depended on it, and a key
		// taught wrong by its own test is how a unit survives a review.
		In.SunPitchRead = -36.0; In.SunYawRead = LedgerVignette::SunYawDeg(205.0);
		In.SunMobilityRead = 2;
		const std::string L = LedgerVignette::SkySegment(In);
		std::printf("    %s\n", L.c_str());
		Check(L.find("sunIntensityRead=30.000") != std::string::npos,
		      "the sun's intensity is printed as the component reported it");
		Check(L.find("sunCastShadowsRead=yes") != std::string::npos,
		      "and whether it casts, which sun=yes never said");
		Check(L.find("sunPitchYawRead=-36.0/25.0") != std::string::npos,
		      "and where it points, as one pair with no space in it, the CONVERTED yaw and not the azimuth");
		Check(L.find("sunMobilityRead=2") != std::string::npos
		      && L.find("sunMobilityKey=0-static/1-stationary/2-movable/") != std::string::npos,
		      "and its mobility as the engine's own enum value with the key beside it");
		Check(L.find("sunReadStat=one-per-run/last-wins/") != std::string::npos,
		      "and the line says WHICH moment the four are a reading of");
		Check(L.find("skyIntensityRead=0.350") != std::string::npos,
		      "the sky it is being read against is still on the same line");
		Check(EveryTokenIsKeyValue(L),
		      "the grown line is still space-free, so no reader truncates the sun keys");
	}
	{
		// A SUN THAT DID NOT SPAWN PRINTS WORDS, NOT ZEROS. sun=SPAWN-FAILED
		// with sunIntensityRead=0.000 would be the same string a sun that
		// is switched off prints, and those are different facts.
		LedgerVignette::SkyIn In;
		const std::string L = LedgerVignette::SkySegment(In);
		Check(L.find("sun=SPAWN-FAILED") != std::string::npos
		      && L.find("sunIntensityRead=nothing-measured") != std::string::npos
		      && L.find("sunMobilityRead=nothing-measured") != std::string::npos,
		      "a sun that never spawned says nothing-measured rather than printing a zero");
		Check(EveryTokenIsKeyValue(L), "the nothing-measured sun line is space-free too");
	}
	{
		// PER-SAMPLE, ON THE SAMPLE LINE. A ladder renders six conditions
		// in one run and the scene line is one-per-run, so this is the
		// half that can attribute a rung to the sun that lit it.
		const std::string L = LedgerVignette::ShotLightLine(
			true, 300.0, 300.0, true, -36.0, LedgerVignette::SunYawDeg(205.0), 2, true, 1.0, 1.0);
		std::printf("    %s\n", L.c_str());
		Check(L.find("shotSunIntensityRead=300.000") != std::string::npos
		      && L.find("shotSkyIntensityRead=1.000") != std::string::npos,
		      "the frame's own line carries both intensities as the components read them");
		// A1(c), CONDITION C5: THE ASK IS ON THE SAME LINE AS THE READ, and
		// the cell says whether they agreed. Run 38 printed five rungs that
		// all read sky 1.000 and never printed what any of them asked for.
		Check(L.find("shotSunIntensityAsked=300.000") != std::string::npos
		      && L.find("shotSkyIntensityAsked=1.000") != std::string::npos
		      && L.find("shotCellAgrees=yes") != std::string::npos,
		      "a cell lit by the numbers it asked for prints both halves and says it agreed");
		// AND THE PLANTED DISAGREEMENT, which is the case the key exists for:
		// the grid's middle skies are the cells that have never been rendered,
		// so a row reading back the old 1.000 must refuse rather than report.
		const std::string Wrong = LedgerVignette::ShotLightLine(
			true, 3.0, 3.0, true, -36.0, 25.0, 2, true, 0.70, 1.000);
		std::printf("    %s\n", Wrong.c_str());
		Check(Wrong.find("shotSkyIntensityAsked=0.700") != std::string::npos
		      && Wrong.find("shotSkyIntensityRead=1.000") != std::string::npos
		      && Wrong.find("shotCellAgrees=NO/the-frame-was-lit-by-numbers-this-row-did-not-ask-for")
		         != std::string::npos,
		      "a cell that asked for a middle sky and read back 1.000 says NO on its own line");
		Check(EveryTokenIsKeyValue(Wrong), "the disagreeing cell line is space-free");
		Check(L.find("shotLightStat=read-off-the-components-while-THIS-frame-stood/"
		             "per-sample-not-per-run") != std::string::npos,
		      "and says it is a per-sample reading, so it is never read as a whole-run number");
		Check(EveryTokenIsKeyValue(L), "the shot light line is space-free");
		const std::string M = LedgerVignette::ShotLightLine(
			false, 3.0, 0.0, false, 0.0, 0.0, -1, false, 1.0, 0.0);
		Check(M.find("shotSunIntensityRead=nothing-measured") != std::string::npos
		      && M.find("shotSkyIntensityRead=nothing-measured") != std::string::npos,
		      "a frame taken with no sun component says nothing-measured on its own line");
		// AND A CELL THAT WAS NOT READ IS NOT A CELL THAT AGREED. The ask is
		// still printed, because the row existed; the agreement is not.
		Check(M.find("shotSunIntensityAsked=3.000") != std::string::npos
		      && M.find("shotCellAgrees=nothing-measured/no-component-answered-on-this-frame")
		         != std::string::npos,
		      "an unread cell prints what it asked for and refuses to claim agreement");
		Check(EveryTokenIsKeyValue(M), "the unread cell line is space-free too");

		// ---- THE WHOLE-RUN TALLY, AND ITS NEVER-RAN CASE -----------------
		const std::string T = LedgerVignette::CellAgreeLine(25, 25, 25);
		std::printf("    %s\n", T.c_str());
		Check(T.find("cellAgree=25/of=25/read") != std::string::npos
		      && T.find("cellAgreeRead=25/of=25/asked") != std::string::npos,
		      "the run line counts agreeing cells over the cells READ and the cells read over the shots ASKED");
		Check(LedgerVignette::CellAgreeLine(11, 12, 25).find("cellAgree=11/of=12/read")
		      != std::string::npos,
		      "and one cell short of twelve reads as eleven of twelve rather than as a pass");
		const std::string Z = LedgerVignette::CellAgreeLine(0, 0, 25);
		Check(Z.find("cellAgree=nothing-measured/of=25/shots-asked") != std::string::npos,
		      "a run that read no cell says nothing measured over the shots it was asked for, never 0/0");
		Check(EveryTokenIsKeyValue(T) && EveryTokenIsKeyValue(Z),
		      "both forms of the cell tally are space-free");
	}

	{
		// ---- QUEUE 208: THE CAMERA ON THE FRAME'S OWN LINE ---------------
		//
		// ACCEPTING CASE FIRST, and it is the one the tool has to read:
		// cam_hook as run 38 placed it. x_m 4.0 and z_m -2.1 map to X 400.0
		// and Y -210.0, ground -0.0525 plus eye 1.65 is Z 159.8, and the
		// file's pitch of -2.6 down is a POSITIVE 2.6 in this engine. Those
		// are the numbers tools/frame-shadow-probe.py compares against the
		// shared json, so if this string is wrong the tool refuses.
		LedgerVignette::ShotCamIn In;
		In.CamId = "cam_hook";
		In.Status = "MEASURED";
		In.AskedXCm = 400.0; In.AskedYCm = -210.0; In.AskedZCm = 159.75;
		In.ReadXCm  = 400.0; In.ReadYCm  = -210.0; In.ReadZCm  = 159.75;
		In.AskedPitchDeg = 2.6; In.AskedYawDeg = 11.0;
		In.ReadPitchDeg  = 2.6; In.ReadYawDeg  = 11.0;
		const std::string L = LedgerVignette::ShotCamSegment(In);
		std::printf("    %s\n", L.c_str());
		Check(L.find("shotCamId=cam_hook") != std::string::npos
		      && L.find("shotCamReadXYZcm=400.0/-210.0/159.8") != std::string::npos
		      && L.find("shotCamReadPitchYaw=2.6/11.0") != std::string::npos,
		      "the frame's own line carries the camera it was taken from and the pose read back");
		Check(L.find("shotCamDeltaCm=0.00") != std::string::npos,
		      "a camera that landed where it was sent prints a zero distance, not a claim");
		Check(L.find("shotCamStat=asked-against-read-back-off-the-player-view-point-while-THIS-"
		             "frame-stood/per-sample-not-per-run") != std::string::npos,
		      "and says it is a per-sample reading, so it is never read as a whole-run number");
		Check(EveryTokenIsKeyValue(L), "the shot camera segment is space-free");

		// ---- AND THE PLANTED CASE: A CAMERA THAT DID NOT ARRIVE ----------
		//
		// Rule 5b, the other outcome watched. The distance is computed here
		// rather than in the module, so a camera that was sent somewhere and
		// ended up somewhere else says so with a number.
		LedgerVignette::ShotCamIn Off = In;
		Off.ReadZCm = 159.75 - 40.0;
		const std::string M = LedgerVignette::ShotCamSegment(Off);
		Check(M.find("shotCamDeltaCm=40.00") != std::string::npos
		      && M.find("shotCamAskedXYZcm=400.0/-210.0/159.8") != std::string::npos
		      && M.find("shotCamReadXYZcm=400.0/-210.0/119.8") != std::string::npos,
		      "a camera that did not arrive prints both halves and the distance between them");

		// ---- AND A SHOT THAT HAD NO CAMERA TO READ -----------------------
		LedgerVignette::ShotCamIn None;
		None.CamId = "cam_A";
		None.Status = "NO-WORLD";
		const std::string N = LedgerVignette::ShotCamSegment(None);
		std::printf("    %s\n", N.c_str());
		Check(N.find("shotCamRead=NO-WORLD") != std::string::npos
		      && N.find("shotCamReadXYZcm=nothing-measured") != std::string::npos
		      && N.find("shotCamDeltaCm=nothing-measured") != std::string::npos,
		      "a shot whose camera could not be read says the words rather than printing an origin");
		Check(EveryTokenIsKeyValue(N), "the nothing-measured camera segment is space-free too");
		// A ZERO POSE AND AN UNREAD POSE ARE DIFFERENT FACTS, and the second
		// may never print as the first: an unread camera at 0/0/0 would read
		// as a camera that really was at the world origin.
		Check(N.find("0.0/0.0/0.0") == std::string::npos,
		      "an unread camera never prints the origin it was default-constructed at");
	}

	// ---- A6: THE LIGHTS, ASKED AGAINST READ, AND THE GUARD'S TWO CASES ---
	//
	// WHAT WAS MISSING AND WHAT IT COST. The sun's conversion was tested at
	// line 404 of this file and its format string at 2058, and the engine
	// rendered a sun 46.0 degrees from the asked one for every run the key
	// has existed, because no test asked whether the number ARRIVED. These
	// run in the layer that compiles here; the arrival itself is measured on
	// the run, which is what lightAimStatus refuses on.
	//
	// ACCEPTING CASE FIRST, PER RULE 5b, AND ON THE LIVE VALUES: the asked
	// pair is the committed file's own sun put through the same two
	// converters the spawner calls, so this fixture cannot drift from the
	// scene.
	{
		const double AskedPitch = LedgerVignette::SunPitchDeg(S.SunElevationDeg);
		const double AskedYaw   = LedgerVignette::SunYawDeg(S.SunAzimuthDeg);
		std::printf("    lightAim: liveAskedPitchYaw=%.1f/%.1f from elevation=%.1f azimuth=%.1f\n",
		            AskedPitch, AskedYaw, S.SunElevationDeg, S.SunAzimuthDeg);
		std::vector<LedgerVignette::LightAim> Lights;
		LedgerVignette::LightAim Sun;
		Sun.Name = "sun"; Sun.bSpawned = true; Sun.bRead = true;
		Sun.AskedPitch = AskedPitch; Sun.AskedYaw = AskedYaw;
		Sun.ReadPitch = AskedPitch;  Sun.ReadYaw = AskedYaw;
		Lights.push_back(Sun);
		// THE THREE FILLS, WITH THE LITERALS VignetteShot.cpp SPAWNS THEM
		// FROM, and fill B is the case that matters: it asks for yaw 200.0
		// and an FRotator normalises that to -160.0, which is the same
		// direction. A residual that did not wrap would refuse a light aimed
		// exactly where it was sent, and the guard would have been a ratchet.
		const double FillPitch[3] = { -80.0, -10.0,  60.0 };
		const double FillYaw[3]   = {  20.0, 200.0,  90.0 };
		const double FillReadYaw[3] = { 20.0, -160.0, 90.0 };
		const char* FillName[3] = { "fillA", "fillB", "fillC" };
		for (int K = 0; K < 3; ++K)
		{
			LedgerVignette::LightAim F;
			F.Name = FillName[K]; F.bSpawned = true; F.bRead = true;
			F.AskedPitch = FillPitch[K]; F.AskedYaw = FillYaw[K];
			F.ReadPitch = FillPitch[K];  F.ReadYaw = FillReadYaw[K];
			Lights.push_back(F);
		}
		const std::string L = LedgerVignette::LightAimLine(Lights, 4);
		std::printf("    %s\n", L.c_str());
		Check(L.find("lightAimStatus=AGREES") != std::string::npos,
		      "four lights aimed where they were sent print the one passing word");
		Check(L.find("lightAimAgreeing=4/of=4/read") != std::string::npos
		      && L.find("lightAimRead=4/of=4/spawned") != std::string::npos
		      && L.find("lightAimSpawned=4/of=4/") != std::string::npos,
		      "and every count ships the denominator it is over");
		Check(L.find("lightAim.sun.askedPitchYaw=-36.0/25.0") != std::string::npos
		      && L.find("lightAim.sun.readPitchYaw=-36.0/25.0") != std::string::npos,
		      "the sun's asked pair is the live file's -36.0/25.0 and it is printed beside the read pair",
		      "the committed spec asks elevation 36 azimuth 205");
		Check(L.find("lightAim.sun.residualPitchYawDeg=0.0000/0.0000") != std::string::npos,
		      "a light that arrived prints a zero residual on both axes to four decimals");
		Check(L.find("lightAim.fillB.askedPitchYaw=-10.0/200.0") != std::string::npos
		      && L.find("lightAim.fillB.readPitchYaw=-10.0/-160.0") != std::string::npos
		      && L.find("lightAim.fillB.residualPitchYawDeg=0.0000/0.0000") != std::string::npos,
		      "a yaw of 200 reading back as -160 is the same direction and wraps to a zero residual",
		      "an unwrapped subtraction would print -360.0000 and refuse a correct light");
		Check(L.find("lightAimWorstResidualDeg=0.0000/on=") != std::string::npos,
		      "and the worst residual over the population is named with the light and axis it is on");
		Check(L.find("lightAimRefuseAtDeg=1.0/NOT-A-MEASURED-TOLERANCE/") != std::string::npos,
		      "the bound says in its own value that it is a class separator and not a measurement");
		Check(EveryTokenIsKeyValue(L), "the lightAim line is space-free, every token a key with a value");

		// ---- THE PLANTED OFFSET, WHICH MUST REFUSE -----------------------
		//
		// 46.0 degrees of pitch is not an invented number: it is the exact
		// displacement the committed verdict carried, asked -36.0 against
		// read -82.0. The guard is tested on the fault it exists for.
		std::vector<LedgerVignette::LightAim> Planted = Lights;
		Planted[0].ReadPitch = AskedPitch - 46.0;
		const std::string M = LedgerVignette::LightAimLine(Planted, 4);
		std::printf("    %s\n", M.c_str());
		Check(M.find("lightAimStatus=REFUSED") != std::string::npos,
		      "a sun 46 degrees from its ask refuses rather than reporting");
		Check(M.find("lightAim.sun.readPitchYaw=-82.0/25.0") != std::string::npos
		      && M.find("lightAim.sun.residualPitchYawDeg=-46.0000/0.0000") != std::string::npos,
		      "and the line carries the run-38 pair and the signed 46 degree residual",
		      "the committed verdict read sunPitchYawRead=-82.0/25.0 against an asked -36.0/25.0");
		Check(M.find("lightAim.sun=REFUSED") != std::string::npos
		      && M.find("lightAim.fillA=AGREES") != std::string::npos,
		      "the refusal names WHICH light, so three agreeing lights do not hide the fourth");
		Check(M.find("lightAimAgreeing=3/of=4/read") != std::string::npos,
		      "and the count over the population moves with it");
		Check(M.find("lightAimWorstResidualDeg=-46.0000/on=sun/axis=pitch") != std::string::npos,
		      "the at-worst residual is signed and names the light and the axis it was worst on");
		// AND A HALF DEGREE MUST NOT REFUSE, which is the other side of the
		// class separator: the bound exists to catch 46.0 and not a float
		// round trip, and a guard that cannot tell them apart is a ratchet.
		std::vector<LedgerVignette::LightAim> Small = Lights;
		Small[0].ReadYaw = AskedYaw + 0.5;
		Check(LedgerVignette::LightAimLine(Small, 4).find("lightAimStatus=AGREES")
		      != std::string::npos,
		      "half a degree does not refuse, because 1.0 separates the 46.0 fault from rounding");

		// ---- AND A RUN THAT READ NOTHING, WHICH IS NOT A PASS ------------
		std::vector<LedgerVignette::LightAim> NoneRead;
		LedgerVignette::LightAim Dead;
		Dead.Name = "sun"; Dead.bSpawned = true; Dead.bRead = false;
		Dead.AskedPitch = AskedPitch; Dead.AskedYaw = AskedYaw;
		NoneRead.push_back(Dead);
		const std::string N = LedgerVignette::LightAimLine(NoneRead, 4);
		std::printf("    %s\n", N.c_str());
		Check(N.find("lightAimStatus=NOTHING-MEASURED") != std::string::npos
		      && N.find("lightAim.sun=NO-COMPONENT") != std::string::npos
		      && N.find("lightAim.sun.readPitchYaw=nothing-measured") != std::string::npos,
		      "a light with no component prints the words rather than a zero that reads as the horizon");
		Check(N.find("lightAimWorstResidualDeg=nothing-measured/") != std::string::npos
		      && N.find("lightAimRead=0/of=1/spawned") != std::string::npos,
		      "a run that read no light says so with its denominators and never prints a zero residual");
		Check(N.find("lightAimStatus=AGREES") == std::string::npos,
		      "and NOTHING-MEASURED is not the passing word, so the guard fails closed");
		Check(EveryTokenIsKeyValue(N), "the nothing-measured lightAim line is space-free too");
	}

	// ---- THE NULL SERIES, DISCOVERED ON THE LIVE FILE --------------------
	//
	// C4 as amended: the noise floor is a SPREAD over every frame this engine
	// renders identically, not one subtraction. The accepting fixture is the
	// committed spec, which is this project's rule for a tool that checks the
	// project itself, and the thing being checked is the DISCOVERY: the group
	// is found from the conditions, so nobody has to keep a list of shot ids
	// in a header. The statistics are synthetic, because no frame exists in
	// this container, and the model is named rather than assumed: a signal
	// linear in sky intensity plus a bounded per-shot noise.
	{
		std::printf("  null series, the spread that C4 reads the grid against\n");
		// THE SIGNAL AND THE NOISE, BOTH CHOSEN HERE SO THE EXPECTED VERDICT
		// IS ARITHMETIC AND NOT A GUESS. Signal: 0.20 of luma per unit of sky,
		// so the smallest sky step in the grid (0.35 to 0.50) is 0.0300.
		// Noise: 0.0005 times the shot index modulo 4, so no spread over any
		// identical-input group can exceed 0.0015.
		std::vector<LedgerVignette::FrameSample> Samples;
		// THE SUN FLAG RIDES BESIDE THE SAMPLES AND IS NEVER SNIFFED OUT OF A
		// KEY: the condition's own boolean, one entry per sample, which is
		// what the ratchet below counts step-holding families by.
		std::vector<int> SunOff;
		for (size_t I = 0; I < S.Shots.size(); ++I)
		{
			const LedgerVignette::Condition* C = 0;
			for (size_t J = 0; J < S.Conditions.size(); ++J)
			{
				if (S.Conditions[J].Id == S.Shots[I].ConditionId) { C = &S.Conditions[J]; }
			}
			if (C == 0) { continue; }
			LedgerVignette::FrameSample F;
			F.ShotId = S.Shots[I].Id;
			F.CameraId = S.Shots[I].CameraId;
			F.Applied      = LedgerVignette::AppliedFieldsUnreal(*C, true);
			F.AppliedNoSky = LedgerVignette::AppliedFieldsUnreal(*C, false);
			F.SkyIntensity = C->SkyIntensity;
			F.bMeasured = true;
			F.MeanLuma  = 0.30 + 0.20 * C->SkyIntensity + 0.0005 * (double)(I % 4);
			F.GroundP05 = F.MeanLuma * 0.50;
			F.GroundP50 = F.MeanLuma * 0.80;
			Samples.push_back(F);
			SunOff.push_back(C->SunOn ? 0 : 1);
		}
		const std::string NS = LedgerVignette::NullSeriesLine(Samples);
		std::printf("    %s\n", NS.c_str());
		// THE GROUP SIZE AND THE DENOMINATORS ARE COUNTED HERE, NOT PINNED.
		// Rows enter and leave this file by the item that needs them, so a
		// literal 7 of 25 fails for the wrong reason the first time a row is
		// added. WHAT IS BEING CHECKED IS THE DISCOVERY, so the expected
		// numbers are recomputed from the same conditions by the tally here.
		// THIS TALLY IS NOT INDEPENDENT OF THE DISCOVERY and said it was
		// until 2026-09-14: it calls the same SampleKey NullSeriesLine calls,
		// so the two agree on a group by construction and only a MISCOUNT
		// (the loop, the denominator, the largest-of) can separate them. What
		// anchors the group to the review's own is the list DERIVED below
		// from the reference cell, field by field, which calls no shared
		// function at all.
		const NullFamilyTally NT = TallyNullFamilies(Samples, SunOff);
		char WantMeasured[96];
		std::snprintf(WantMeasured, sizeof(WantMeasured), "nullSeriesMeasured=%d/of=%d/",
		              (int)Samples.size(), (int)S.Shots.size());
		std::printf("    counted independently: largestBySizeAlone=%d largestQualifying=%d "
		            "distinctGroups=%d qualifyingGroups=%d families=%d stepFamilies=%d "
		            "sunOffFamilies=%d stepFamiliesSunOff=%d outsideFrames=%d samples=%d "
		            "of shots=%d\n",
		            NT.Largest, NT.LargestQualifying, NT.DistinctGroups, NT.QualifyingGroups,
		            NT.Families, NT.StepFamilies, NT.SunOffFamilies, NT.StepFamiliesSunOff,
		            NT.OutsideFrames, (int)Samples.size(), (int)S.Shots.size());
		Check(NS.find(WantMeasured) != std::string::npos,
		      "the live file's measured count is what an independent tally over the same "
		      "conditions counts, over the shots the file actually carries",
		      std::string(WantMeasured) + " against: " + NS);
		// ---- THE RULE THAT PICKED THE GROUP, ASSERTED AS WELL AS THE GROUP --
		//
		// SIZE ALONE WOULD HAVE KEPT ANOTHER GROUP SINCE 2026-09-16, and this
		// is where the two are told apart. The emitter keeps the largest
		// identical-input group whose no-sky family holds a sky-only pair; the
		// key beside it names what size alone would have kept, which on the
		// live file is the ten-frame night group queue 334's six settle rows
		// completed. Every number here is NT's, counted above, so none of them
		// is typed and a row entering or leaving the spec moves both sides.
		{
			char WantBySize[96];
			std::snprintf(WantBySize, sizeof(WantBySize), "/n=%d/spreadMeanLuma=", NT.Largest);
			const std::string BySize = ValueOfKey(NS, "nullSeriesBySizeAlone=");
			const std::string Applied = ValueOfKey(NS, "nullSeriesApplied=");
			std::printf("    bySizeAlone=%s\n", BySize.c_str());
			Check(BySize.find(NT.LargestKey) == 0
			      && BySize.find(WantBySize) != std::string::npos,
			      "the line names the group SIZE ALONE would have kept, with the size an "
			      "independent tally counts, so a floor that moves moves on the line",
			      "wanted " + NT.LargestKey + WantBySize + " got " + BySize);
			Check(BySize.size() > 17
			      && BySize.compare(BySize.size() - 17, 17, "DIFFERS-FROM-KEPT") == 0
			      && NT.LargestKey != NT.LargestQualifyingKey
			      && Applied == NT.LargestQualifyingKey,
			      "and on the live file it DIFFERS from the kept group, which is the six "
			      "settle rows joining the four pinset rows into a night group of ten while "
			      "the floor stays on the day family that holds a step",
			      "bySizeAlone=" + BySize + " applied=" + Applied);
			// ONE ENTRY CARRYING BOTH MOMENTS, IN ORDER: the group, then its
			// size, then ITS OWN spread, then the word. A reader never has to
			// hold two keys' relationship in their head, and a buffer that
			// truncated anywhere loses the tail this asserts.
			const size_t AtN = BySize.find("/n=");
			const size_t AtSpread = BySize.find("/spreadMeanLuma=");
			const size_t AtWord = BySize.find("DIFFERS-FROM-KEPT");
			Check(AtN != std::string::npos && AtSpread != std::string::npos
			      && AtWord != std::string::npos && AtN < AtSpread && AtSpread < AtWord,
			      "and the size, the spread and the verdict word ride in that order inside "
			      "one value, so the size and the spread on it are of one group",
			      BySize);
		}
		// ---- THE FAMILIES AND THE FRAMES OUTSIDE THEM -----------------------
		{
			char WantFam[128], WantOutside[128];
			std::snprintf(WantFam, sizeof(WantFam),
			              "nullSeriesFamilies=%d/of=%d/no-sky-families-holding-a-sky-only-pair/",
			              NT.StepFamilies, NT.Families);
			std::snprintf(WantOutside, sizeof(WantOutside),
			              "nullSeriesOutsideStepFamilies=%d/of=%d/measured-frames-whose-family-"
			              "holds-no-sky-only-pair/ids=", NT.OutsideFrames, (int)Samples.size());
			Check(NS.find(WantFam) != std::string::npos,
			      "the step-holding families print with the families examined as their "
			      "denominator, both counted independently and neither typed", WantFam);
			Check(NS.find(WantOutside) != std::string::npos,
			      "and the measured frames whose family holds no sky-only pair print with the "
			      "measured frames as theirs, so a reader sees how much of the run no floor "
			      "can be read off", WantOutside);
			// THE CAP BITES ON THE LIVE FILE AND MUST SAY SO. Twelve ids, and
			// the live file has more frames outside than that, so the tail is
			// the announcement rather than a silent truncation. The number is
			// computed from the same count, never typed.
			const std::string OutIds = ValueOfKey(NS, "nullSeriesOutsideStepFamilies=");
			const size_t IdsAt = OutIds.find("/ids=");
			std::vector<std::string> Shown;
			SplitOn(IdsAt == std::string::npos ? std::string("no-ids-segment-on-the-key")
			                                   : OutIds.substr(IdsAt + 5), ';', Shown);
			char WantMore[64];
			std::snprintf(WantMore, sizeof(WantMore), "/+%d-more-not-shown",
			              NT.OutsideFrames - 12);
			std::printf("    outside-step ids shown=%d of %d outside, capBites=%s/cap=12\n",
			            (int)Shown.size(), NT.OutsideFrames,
			            NT.OutsideFrames > 12 ? "yes" : "no");
			Check(NT.OutsideFrames <= 12
			      ? OutIds.find("-more-not-shown") == std::string::npos
			      : OutIds.find(WantMore) != std::string::npos,
			      "and the id list's cap announces itself when it bites, with the number it "
			      "withheld, so a capped list cannot read as the whole of a finding",
			      std::string(WantMore) + " against " + OutIds);
			// EVERY FRAME OF A SUN-OFF CONDITION AT THE REFERENCE CAMERA IS
			// OUTSIDE, which is the ruling's own statement of where the settle
			// and pinset rows now sit. Section 3 predicted this count would BE
			// the outside total; the tree says it is a SUBSET of it, because
			// the two other cameras and the fog and wetness ladders hold no
			// sky-only pair either. The subset is asserted and the two numbers
			// are printed side by side, since a prediction corrected by a count
			// is worth more than a prediction repeated.
			int RefCamSunOff = 0;
			std::string RefCam;
			for (size_t I = 0; I < S.Shots.size() && RefCam.empty(); ++I)
			{
				if (S.Shots[I].ConditionId == "grid_sky070_sun003") { RefCam = S.Shots[I].CameraId; }
			}
			bool bAllOutside = true;
			for (size_t I = 0; I < Samples.size(); ++I)
			{
				if (Samples[I].CameraId != RefCam || !SunOff[I]) { continue; }
				++RefCamSunOff;
				bool bFound = false;
				for (size_t J = 0; J < NT.OutsideIds.size(); ++J)
				{
					if (NT.OutsideIds[J] == Samples[I].ShotId) { bFound = true; break; }
				}
				if (!bFound) { bAllOutside = false; }
			}
			std::printf("    sun-off frames at the reference camera=%d, all outside a "
			            "step-holding family=%s, outside frames in the whole run=%d\n",
			            RefCamSunOff, bAllOutside ? "yes" : "no", NT.OutsideFrames);
			Check(RefCamSunOff > 0 && bAllOutside && NT.OutsideFrames >= RefCamSunOff,
			      "every sun-off frame at the reference camera sits outside any step-holding "
			      "family, which is where the six settle rows and the four pinset rows are by "
			      "their own fields and not by a key any row declares",
			      std::to_string(RefCamSunOff) + " sun-off at " + RefCam + " of "
			      + std::to_string(NT.OutsideFrames) + " outside");
		}
		// ---- THE ANCHOR, DERIVED FROM ONE NAMED ID AND NOT TYPED --------
		//
		// THE LIST USED TO BE SEVEN IDS TYPED IN, and the comment above says
		// why: to anchor the discovery to the review's own group, since the
		// tally beside it calls the same SampleKey the discovery calls and is
		// therefore not independent of it. The typed list has two scheduled
		// reasons to change in one week: the pin batch grows it to nine
		// (`expPin` is part of the fingerprint at VignetteSpec.h 2574, so the
		// two shots of rung 0.300 are correctly null samples of the live
		// rows), and D28 step 5 wires wetness, after which wet_000 and
		// wet_100 leave it. A typed list would fail for the wrong reason
		// twice.
		//
		// SO THE ANCHOR IS BUILT THE WAY THE NULL-CELL CHECK ABOVE COMPARES
		// TWO CONDITIONS, field by field, from ONE named id: the reference
		// cell grid_sky070_sun003 that the grid ruling defined. Walk the
		// shots in shot order, keep those standing at the reference cell's
		// own camera whose condition matches it in every field that lights a
		// frame plus exposure_pin, excluding the one field the line itself
		// says it excludes. Nothing here calls SampleKey.
		{
			const LedgerVignette::Condition* RefC = 0;
			for (size_t I = 0; I < S.Conditions.size(); ++I)
			{
				if (S.Conditions[I].Id == "grid_sky070_sun003") { RefC = &S.Conditions[I]; }
			}
			std::string RefCam = "no-shot-for-the-reference-cell";
			for (size_t I = 0; I < S.Shots.size() && RefC != 0; ++I)
			{
				if (S.Shots[I].ConditionId == RefC->Id
				    && RefCam == "no-shot-for-the-reference-cell")
				{
					RefCam = S.Shots[I].CameraId;
				}
			}
			std::vector<std::string> SameConds;
			for (size_t I = 0; I < S.Conditions.size() && RefC != 0; ++I)
			{
				const LedgerVignette::Condition& C = S.Conditions[I];
				// NOTHING IS EXCLUDED SINCE QUEUE 309 and the line beside
				// this one says so: wetness joined the fingerprint when
				// ApplyCondition began re-driving it per condition, so it is
				// compared here like every other field the engine reads, the
				// pin included. A field left out of this list while the
				// emitter reads it would make the derived anchor WIDER than
				// the discovered group and the comparison below would fail,
				// which is what keeps the two sides honest about each other.
				if (std::fabs(C.Wetness - RefC->Wetness) < 1e-12
				    && C.Hdri == RefC->Hdri && C.SunOn == RefC->SunOn
				    && C.LanternsOn == RefC->LanternsOn && C.WindowsOn == RefC->WindowsOn
				    && std::fabs(C.SunIntensity - RefC->SunIntensity) < 1e-12
				    && std::fabs(C.SkyIntensity - RefC->SkyIntensity) < 1e-12
				    && std::fabs(C.FogDensity - RefC->FogDensity) < 1e-12
				    && std::fabs(C.FogMaxOpacity - RefC->FogMaxOpacity) < 1e-12
				    && std::fabs(C.ExposurePin - RefC->ExposurePin) < 1e-12)
				{
					SameConds.push_back(C.Id);
				}
			}
			std::vector<std::string> WantIds;
			for (size_t I = 0; I < S.Shots.size(); ++I)
			{
				if (S.Shots[I].CameraId != RefCam) { continue; }
				for (size_t J = 0; J < SameConds.size(); ++J)
				{
					if (SameConds[J] == S.Shots[I].ConditionId)
					{
						WantIds.push_back(S.Shots[I].Id);
						break;
					}
				}
			}
			// THE CAP THE EMITTER APPLIES IS MIRRORED HERE AND ANNOUNCES
			// WHETHER IT BIT, because a derived list longer than the cap must
			// expect the emitter's own "+N-more-not-shown" tail rather than
			// the whole list.
			const size_t kIdCap = 12;
			std::string WantLine;
			for (size_t I = 0; I < WantIds.size() && I < kIdCap; ++I)
			{
				if (!WantLine.empty()) { WantLine += ";"; }
				WantLine += WantIds[I];
			}
			if (WantIds.size() > kIdCap)
			{
				char More[64];
				std::snprintf(More, sizeof(More), "/+%d-more-not-shown",
				              (int)(WantIds.size() - kIdCap));
				WantLine += More;
			}
			const std::string GotLine = ValueOfKey(NS, "nullSeriesIds=");
			std::vector<std::string> GotIds;
			SplitOn(GotLine, ';', GotIds);
			std::printf("    derived from grid_sky070_sun003: camera=%s condsMatching=%d/of=%d "
			            "shotsWalked=%d derivedIds=%d discoveredIds=%d capBites=%s/cap=%d\n",
			            RefCam.c_str(), (int)SameConds.size(), (int)S.Conditions.size(),
			            (int)S.Shots.size(), (int)WantIds.size(), (int)GotIds.size(),
			            WantIds.size() > kIdCap ? "yes" : "no", (int)kIdCap);
			std::printf("    derivedIds=%s\n",
			            WantLine.empty() ? "none" : WantLine.c_str());
			Check(RefC != 0 && !WantIds.empty() && GotLine == WantLine,
			      "the discovered null series is EXACTLY the group derived from the reference "
			      "cell field by field at its own camera, in shot order, re-derived every run "
			      "rather than typed, so a row entering or leaving moves both sides together",
			      "derived=" + WantLine + " discovered=" + GotLine);
			// THREE ASSERTIONS THE TYPED LIST CARRIED IMPLICITLY, kept.
			bool bHookIn = false;
			for (size_t I = 0; I < GotIds.size(); ++I)
			{
				if (GotIds[I] == "vign_hook_day") { bHookIn = true; }
			}
			Check(bHookIn,
			      "the judged hook frame is one of the null samples, which is what makes the "
			      "group a statement about the frame Jafar looks at", GotLine);
			Check(!GotIds.empty() && GotIds[GotIds.size() - 1] == "vign_grid_null_repeat",
			      "and the null cell is the last of them, identical inputs at the maximum "
			      "order separation the run allows", GotLine);
			bool bRefIn = false, bNullIn = false;
			for (size_t I = 0; I < GotIds.size(); ++I)
			{
				if (GotIds[I] == "vign_grid_sky070_sun003") { bRefIn = true; }
				if (GotIds[I] == "vign_grid_null_repeat")   { bNullIn = true; }
			}
			Check(bRefIn && bNullIn && (int)GotIds.size() >= 2,
			      "and the group holds the grid's reference cell and its null cell, the pair "
			      "the grid ruling defined, so the spread is read over the comparison the "
			      "grid exists for", GotLine + " over " + std::to_string((int)GotIds.size())
			      + " ids");
			// AND THE COUNT ON THE LINE IS THE LENGTH OF THAT DERIVED LIST,
			// which is where nullSeriesSamples is anchored since 2026-09-16.
			// It used to be anchored to the largest group by size, and that is
			// the number that moved when the six settle rows landed: the count
			// and the ids would have disagreed about which group was read, one
			// of them silently. The size-alone number has not left the line, it
			// has moved to the key that names what it is a count OF.
			char WantSamples[96];
			std::snprintf(WantSamples, sizeof(WantSamples), "nullSeriesSamples=%d/of=%d/",
			              (int)WantIds.size(), (int)S.Shots.size());
			Check(NS.find(WantSamples) != std::string::npos
			      && (int)WantIds.size() == NT.LargestQualifying,
			      "the count of null samples is the length of the derived list and the size of "
			      "the largest qualifying group an independent tally counts, so the number and "
			      "the ids on this line are of one group",
			      std::string(WantSamples) + " derived=" + std::to_string((int)WantIds.size())
			      + " qualifying=" + std::to_string(NT.LargestQualifying));
			Check(NS.find("nullSeriesSamples=" + std::to_string((int)WantIds.size())
			              + "/of=" + std::to_string((int)S.Shots.size())
			              + "/measured-frames-sharing-the-largest-identical-applied-input-"
			                "group-at-one-camera/within-a-family-that-holds-a-sky-only-pair")
			      != std::string::npos,
			      "and the descriptor beside it names BOTH rules that picked them, the largest "
			      "identical-input group and the family holding a sky-only pair, so the count "
			      "keeps its name while the rule that chose it is printed in full",
			      ValueOfKey(NS, "nullSeriesSamples="));
		}
		// THE EXCLUSION ENDED ON 2026-09-15 AT QUEUE 309, having survived one
		// earlier rewrite of its reason. The field was out because
		// VignetteShot.cpp had no read site for it; then because the read site
		// queue 186 added was STATIC, one value for the whole run; it is in
		// now because ApplyCondition re-drives it per condition, so two
		// conditions differing only in wetness render two different streets.
		// Both halves of the new value are asserted, because a value carrying
		// only the first would read as a field somebody forgot.
		Check(NS.find("nullSeriesExcludes=none/every-field-this-engine-applies-"
		              "is-in-the-fingerprint-since-queue-309") != std::string::npos
		      && NS.find("wetness-JOINED-2026-09-15-when-ApplyCondition-began-"
		                 "re-driving-it-per-condition") != std::string::npos,
		      "the line says nothing is excluded any more AND says which field "
		      "joined, when, and what changed to let it", NS);
		// AND BOTH SUPERSEDED REASONS ARE GONE RATHER THAN LEFT BESIDE THE
		// NEW ONE. A verdict carrying a true and a false explanation of the
		// same thing is worse than one carrying neither, because the reader
		// who finds the false one first stops reading. THE SECOND TOKEN IS
		// THE ONE THAT MATTERS HERE: `nullSeriesExcludes=wetness` was true
		// this morning and is false tonight, and it is the string a reader
		// coming from the 07:55Z ruling would grep for.
		Check(NS.find("has-no-read-site-for-it-on-this-commit") == std::string::npos
		      && NS.find("nullSeriesExcludes=wetness") == std::string::npos
		      && NS.find("per-condition-needs-a-MID-list-nothing-keeps")
		         == std::string::npos,
		      "and neither superseded reason survives: not the one that said "
		      "there is no read site, and not the one that said the read site is "
		      "static and per-condition needs a list nothing keeps", NS);
		// AND THE FINGERPRINT ITSELF CARRIES THE FIELD, not just the prose
		// about it. nullSeriesApplied is the winning group's key, so a wet
		// token on it is the proof that AppliedFieldsUnreal reads the value
		// rather than that this comment believes it does.
		Check(ValueOfKey(NS, "nullSeriesApplied=").find("/wet") != std::string::npos,
		      "and the applied fingerprint the group was formed on carries a wet "
		      "term, so the exclusion ended in the arithmetic and not only in the "
		      "sentence about it", ValueOfKey(NS, "nullSeriesApplied="));
		// THE VALUE ABOVE IS BUILT IN A char Buf[960] AND QUEUE 309 GAVE
		// CHARACTERS BACK. Measured on the committed spec by the printer three
		// lines down rather than hand-counted: the buffer portion ran 615 of
		// 960 before queue 186, 768 after it, and this edit shortens the
		// excludes value while AppliedFieldsUnreal's new /wet%.4f term
		// lengthens nullSeriesApplied. A snprintf that overruns TRUNCATES
		// SILENTLY and the key that would lose its tail is the last one in the
		// buffer, which is this one. So the tail token is asserted present AND
		// asserted to be followed by the key appended after the buffer: a cut
		// line fails both halves rather than reading as a short one.
		{
			const size_t Tail = NS.find("no-longer-a-null-sample-of-the-day-group");
			const size_t Ids  = NS.find(" nullSeriesIds=");
			Check(Tail != std::string::npos && Ids != std::string::npos && Ids > Tail,
			      "the excludes value reaches its last token and the next key follows "
			      "it, so the capped buffer that carries it did not truncate", NS);
			// THE SERIES, PRINTED, WHICH IS WHAT A BOUND IS READ OFF. The
			// buffer portion is everything up to the first key appended after
			// it, and nullSeriesIds is that key on every shape this function
			// can build.
			std::printf("    nullSeries buffer portion: %d of 960 byte(s), "
			            "%d free, whole line %d byte(s)\n",
			            (int)Ids, 960 - (int)Ids, (int)NS.size());
			Check((int)Ids < 960,
			      "and the measured buffer portion is inside the buffer that "
			      "carries it, which is the number the size is set from rather "
			      "than a hand count", std::to_string((int)Ids) + "/960");
		}
		// ---- THE WET LADDER'S ROWS, COUNTED RATHER THAN PREDICTED --------
		//
		// QUEUE 309's ACCEPTANCE SAID THE GROUP DROPS "THE THREE wet_ ROWS"
		// AND THE COMMITTED FILE SAYS TWO. wet_000 is at wetness 0.0 and
		// wet_100 at 1.0, so both leave; wet_060 is at 0.6, which IS the
		// wetness the reference cell carries, so it stays and it is right that
		// it stays: it is a genuine null sample of the day group in this
		// engine. The number is counted off the discovered ids here rather
		// than typed, so a later row entering or leaving moves it.
		{
			const std::string Ids = ValueOfKey(NS, "nullSeriesIds=");
			std::vector<std::string> Got;
			SplitOn(Ids, ';', Got);
			int WetRows = 0;
			for (size_t I = 0; I < Got.size(); ++I)
			{
				if (Got[I].find("vign_wet_") == 0) { ++WetRows; }
			}
			std::printf("    wet ladder rows still in the null group: %d of 3 "
			            "offered (wet_000 0.0, wet_060 0.6, wet_100 1.0)\n", WetRows);
			Check(WetRows == 1
			      && Ids.find("vign_wet_060") != std::string::npos
			      && Ids.find("vign_wet_000") == std::string::npos
			      && Ids.find("vign_wet_100") == std::string::npos,
			      "exactly the wet-ladder rows at ANOTHER wetness leave the null "
			      "group, and the one at the reference cell's own 0.6 stays, which "
			      "is one row of the three and not three", Ids);
		}
		Check(NS.find("nullSeriesStatus=READ") != std::string::npos
		      && NS.find("nullSeriesVerdict=CLEAR") != std::string::npos
		      && NS.find("nullSeriesClear=3/of=3/") != std::string::npos,
		      "on a fixture whose noise is 0.0015 at most and whose smallest sky step is "
		      "0.0300, all three statistics read CLEAR and the denominator says three",
		      NS);
		// THE SKY STEP IS READ OFF THE LINE AND CHECKED AS A NUMBER, with the
		// tolerance being the noise the fixture itself plants: 0.20 per unit of
		// sky times the 0.15 step is 0.0300, plus or minus 0.0015.
		{
			const size_t At = NS.find("skyStepSmallestMeanLuma=");
			const double Step = At == std::string::npos ? -1.0
			                  : std::atof(NS.c_str() + At + 24);
			std::printf("    skyStepSmallestMeanLuma read back as %.4f, fixture "
			            "arithmetic says 0.0300 plus or minus 0.0015\n", Step);
			Check(Step > 0.0285 - 1e-9 && Step < 0.0315 + 1e-9,
			      "the smallest sky step is the 0.35-to-0.50 step of the grid, within "
			      "the noise the fixture plants, and it is found without naming a cell",
			      NS);
		}
		// 0.0010 FROM 23 SEPTEMBER, and 0.0015 before it: the day group held
		// the pin_030 rung while 0.300 was the live pin, and the fixture's
		// widest sample was that rung's. The Unreal look's tuning moved the
		// live pin to 2.000, no rung asks 2.000, so the group is five frames
		// and its widest is vign_wet_060's planted 0.4410.
		Check(NS.find("nullSpreadMeanLuma=0.0010/max=") != std::string::npos
		      && NS.find("nullDriftMeanLuma=") != std::string::npos
		      && NS.find("nullOrderMeanLuma=") != std::string::npos,
		      "the spread, the one-pair drift in shot order and whether the group is "
		      "monotone all print, which is what separates a drift from a step", NS);
		Check(EveryTokenIsKeyValue(NS),
		      "the null series line is space-free, every token a key with a value", NS);
		// AND THE CASE THE GATE MUST REFUSE, PLANTED RATHER THAN WAITED FOR.
		// Rule 5b: a guard needs a run where the thing it asserts CAN happen.
		// The same frames with the noise raised to 0.05 per step is a rig whose
		// own repeat moves further than the grid's smallest sky step, which is
		// exactly the condition that made the sun ladder unreadable.
		{
			std::vector<LedgerVignette::FrameSample> Loud = Samples;
			for (size_t I = 0; I < Loud.size(); ++I)
			{
				const double N2 = 0.05 * (double)(I % 4);
				Loud[I].MeanLuma  = 0.30 + 0.20 * Loud[I].SkyIntensity + N2;
				Loud[I].GroundP05 = Loud[I].MeanLuma * 0.50;
				Loud[I].GroundP50 = Loud[I].MeanLuma * 0.80;
			}
			const std::string LN = LedgerVignette::NullSeriesLine(Loud);
			std::printf("    planted: %s\n", LN.substr(0, 220).c_str());
			Check(LN.find("nullSeriesVerdict=NO-READ/no-cell-may-be-quoted")
			      != std::string::npos
			      && LN.find("nullFloorMeanLuma=NOT-SMALLER/") != std::string::npos,
			      "a rig whose null spread is wider than the smallest sky step makes the "
			      "grid a NO-READ, and the key names which statistic failed", LN);
		}
		// ---- THE FAMILY RULE, REFUSED AND FIRED ------------------------------
		//
		// RULE 5b BOTH WAYS. The accepting case is the whole block above, run
		// on the live file: the day group of seven is kept because its own
		// family holds the 0.35/0.50/0.70 sky steps at fog010. The refusing
		// case cannot be waited for, so it is planted: the same run with the
		// reference family's sky-only siblings marked UNMEASURED, which is
		// what a run where those frames fail to land looks like. The day
		// family then holds no step, the day group stops qualifying, and the
		// line must say so rather than quietly reading the floor off it.
		{
			const LedgerVignette::FrameSample* RefS = 0;
			for (size_t I = 0; I < Samples.size(); ++I)
			{
				if (Samples[I].ShotId == "vign_grid_sky070_sun003") { RefS = &Samples[I]; }
			}
			std::vector<LedgerVignette::FrameSample> NoStep = Samples;
			std::vector<int> NoStepSunOff = SunOff;
			int Blanked = 0;
			if (RefS != 0)
			{
				const std::string RefFam = LedgerVignette::SampleKey(*RefS, false);
				const double RefSky = RefS->SkyIntensity;
				for (size_t I = 0; I < NoStep.size(); ++I)
				{
					if (LedgerVignette::SampleKey(NoStep[I], false) != RefFam) { continue; }
					if (std::fabs(NoStep[I].SkyIntensity - RefSky) < 1e-12) { continue; }
					NoStep[I].bMeasured = false;
					++Blanked;
				}
			}
			const NullFamilyTally NST = TallyNullFamilies(NoStep, NoStepSunOff);
			const std::string NSL = LedgerVignette::NullSeriesLine(NoStep);
			std::printf("    planted, the day family's sky-only siblings unmeasured: "
			            "blanked=%d stepFamilies=%d of %d families, kept=%s\n",
			            Blanked, NST.StepFamilies, NST.Families,
			            ValueOfKey(NSL, "nullSeriesApplied=").c_str());
			Check(Blanked > 0 && NST.StepFamilies == NT.StepFamilies - 1,
			      "the plant lands: blanking the reference family's sky-only siblings leaves "
			      "one fewer step-holding family than the live file has, counted both times "
			      "and typed neither",
			      std::to_string(Blanked) + " blanked, " + std::to_string(NST.StepFamilies)
			      + " step families against the live " + std::to_string(NT.StepFamilies));
			Check(ValueOfKey(NSL, "nullSeriesApplied=") != NT.LargestQualifyingKey
			      && ValueOfKey(NSL, "nullSeriesIds=").find("vign_grid_sky070_sun003")
			         == std::string::npos,
			      "and the day group is NOT kept once its own family holds no step, which is "
			      "the case the rule exists to refuse",
			      "applied=" + ValueOfKey(NSL, "nullSeriesApplied="));
			Check(NSL.find("nullSeriesOutsideStepFamilies=") != std::string::npos
			      && ValueOfKey(NSL, "nullSeriesOutsideStepFamilies=")
			         .find("vign_grid_sky070_sun003") != std::string::npos,
			      "and the words say why: the reference cell is named among the measured "
			      "frames whose family holds no sky-only pair",
			      ValueOfKey(NSL, "nullSeriesOutsideStepFamilies="));
			Check(EveryTokenIsKeyValue(NSL),
			      "the planted no-step line is space-free too", NSL);
		}
		// ---- THE RATCHET, AND THE RUN WHERE IT FIRES -------------------------
		//
		// SECTION 3 OF THE 2026-09-16 RULING. The family rule is a SCREEN and
		// not a reading: today exactly one family qualifies, so one floor is
		// printed and "which family" never arises. It arises the moment a
		// second one does, and the first candidate is a night sky-only pair,
		// because a night grid would then have a qualifying night family and
		// SIZE would choose between families again. Until per-family floors
		// land (production/queue/346-the-floor-is-read-per-family-so-a-night-
		// grid-has-a-night-floor.md), this suite refuses that spec rather than
		// reading it, and the refusal is here rather than in anyone's memory.
		//
		// THE SERIES IS PRINTED FIRST, one row per family, because no run has
		// yet printed two qualifying families and 346's builder reads the
		// shape off this print rather than off a description of it.
		{
			const size_t kFamCap = 24;
			for (size_t Q = 0; Q < NT.FamilyKeys.size() && Q < kFamCap; ++Q)
			{
				std::printf("    family[%d] frames=%d holdsStep=%s sunOff=%s key=%s\n",
				            (int)Q, NT.FamilyFrames[Q],
				            NT.FamilyStep[Q] ? "yes" : "no",
				            NT.FamilySunOff[Q] ? "yes" : "no",
				            NT.FamilyKeys[Q].c_str());
			}
			if (NT.FamilyKeys.size() > kFamCap)
			{
				std::printf("    (+%d more family row(s) not shown, cap=%d)\n",
				            (int)(NT.FamilyKeys.size() - kFamCap), (int)kFamCap);
			}
			std::printf("    RATCHET: step-holding families with the sun off = %d of %d "
			            "step-holding families, over %d families and %d sun-off families\n",
			            NT.StepFamiliesSunOff, NT.StepFamilies, NT.Families, NT.SunOffFamilies);
			Check(NT.StepFamilies > 0 && NT.StepFamiliesSunOff == 0,
			      "NO step-holding family in the live spec has the sun off, so exactly one "
			      "kind of family can be the floor and size never chooses between families; "
			      "a night sky-only pair entering the spec fails HERE until the per-family "
			      "floor of production/queue/346 lands, which retires this assertion in the "
			      "same diff",
			      std::to_string(NT.StepFamiliesSunOff) + "/of="
			      + std::to_string(NT.StepFamilies) + " step-holding families, "
			      + std::to_string(NT.SunOffFamilies) + " sun-off families of "
			      + std::to_string(NT.Families));
			// AND THE RUN WHERE IT FIRES, PLANTED: one night frame moved to
			// another sky value is a night sky-only pair, which is exactly the
			// spec change this assertion refuses. A guard that cannot be made
			// to fail is a ratchet, so it is made to fail here on purpose.
			std::vector<LedgerVignette::FrameSample> NightStep = Samples;
			std::vector<int> NightSunOff = SunOff;
			int Moved = -1;
			for (size_t I = 0; I < NightStep.size(); ++I)
			{
				if (!NightSunOff[I] || NightStep[I].CameraId != "cam_hook") { continue; }
				Moved = (int)I;
			}
			if (Moved >= 0)
			{
				// The sky value moves and the applied fingerprint moves with
				// it, which is what a spec row at another sky would produce.
				NightStep[Moved].SkyIntensity += 0.25;
				NightStep[Moved].Applied += "/planted-night-sky-sibling";
				NightStep[Moved].MeanLuma += 0.05;
				const NullFamilyTally RT = TallyNullFamilies(NightStep, NightSunOff);
				const std::string RL = LedgerVignette::NullSeriesLine(NightStep);
				std::printf("    planted night sky-only pair on %s: stepFamiliesSunOff=%d "
				            "of %d step-holding, kept=%s\n",
				            NightStep[Moved].ShotId.c_str(), RT.StepFamiliesSunOff,
				            RT.StepFamilies, ValueOfKey(RL, "nullSeriesApplied=").c_str());
				Check(RT.StepFamiliesSunOff == 1
				      && RT.StepFamilies == NT.StepFamilies + 1,
				      "planting one night sky-only pair makes the ratchet's count ONE rather "
				      "than zero, so the assertion above can fail and is not a ratchet that "
				      "only ever reads clean",
				      std::to_string(RT.StepFamiliesSunOff) + "/of="
				      + std::to_string(RT.StepFamilies));
				// AND THE RATCHET'S OWN PREDICATE, EVALUATED ON THE PLANTED
				// FIXTURE AND ASSERTED FALSE. The check above reads the two
				// counts; this one reads the SENTENCE the assertion is made
				// of, so nobody has to derive that it would have failed.
				const bool bRatchetHolds = (RT.StepFamilies > 0 && RT.StepFamiliesSunOff == 0);
				Check(!bRatchetHolds,
				      "and the ratchet's own predicate is FALSE on that fixture: the same "
				      "sentence that passes on the live file refuses the planted spec, which "
				      "is the run where the guard is seen firing",
				      std::string("predicate=") + (bRatchetHolds ? "held" : "refused"));
				Check(ValueOfKey(RL, "nullSeriesApplied=").find("/sun.off/")
				      != std::string::npos
				      && ValueOfKey(RL, "nullSeriesApplied=") != NT.LargestQualifyingKey,
				      "and the floor moves onto the night family in that run, which is WHY "
				      "the assertion above refuses the spec change until a floor is read per "
				      "family", ValueOfKey(RL, "nullSeriesApplied="));
			}
			else
			{
				Check(false, "the ratchet's planted case needs a sun-off frame at the hook "
				             "camera and the live file offered none",
				      "nothing measured: no sun-off frame at cam_hook");
			}
		}
		// AND A RUN THAT MEASURED NOTHING, WHICH IS NOT A CLEAN RESULT.
		std::vector<LedgerVignette::FrameSample> None;
		const std::string Z = LedgerVignette::NullSeriesLine(None);
		std::printf("    %s\n", Z.c_str());
		Check(Z.find("nullSeriesStatus=NOTHING-MEASURED") != std::string::npos
		      && Z.find("nullSeriesSamples=nothing-measured/of=0/") != std::string::npos
		      && Z.find("nullSeriesVerdict=CLEAR") == std::string::npos,
		      "a run with no measured frame prints the words and never the passing "
		      "verdict, so an empty series cannot read as a clear one", Z);
		// ONE MEASURED FRAME IS NOT A SPREAD EITHER, AND SINCE 2026-09-16 IT
		// IS REFUSED ONE STEP EARLIER AND SAYS SO. A single frame is a family
		// of one, which holds no sky-only pair, so no group qualifies and the
		// status is the word for that rather than TOO-FEW-SAMPLES: the two
		// sentences are both true of this fixture and the line prints the one
		// that is checked FIRST, which is the ruling's own order. The
		// too-few-samples word is still reachable and is checked on the
		// fixture below, where a family DOES hold a step and its largest
		// qualifying group is a single frame.
		std::vector<LedgerVignette::FrameSample> One;
		if (!Samples.empty()) { One.push_back(Samples[0]); }
		const std::string O = LedgerVignette::NullSeriesLine(One);
		std::printf("    one measured frame: %s\n", O.substr(0, 260).c_str());
		Check(O.find("nullSeriesStatus=NO-FAMILY-HOLDS-A-STEP") != std::string::npos
		      && O.find("nullSeriesIds=none") != std::string::npos
		      && O.find("nullSeriesVerdict=nothing-measured/no-group-has-a-family-that-holds-"
		                "a-sky-only-pair") != std::string::npos
		      && O.find("nullSeriesVerdict=CLEAR") == std::string::npos
		      && O.find("nullSeriesFamilies=0/of=1/") != std::string::npos,
		      "one frame is a family of one, so no group qualifies, the line says which rule "
		      "refused it, the ids are none and the zero ships the one family it examined", O);
		// AND THE TOO-FEW-SAMPLES WORD, ON THE FIXTURE THAT CAN STILL REACH
		// IT: two frames of one family at two sky values, which holds a step,
		// so both its groups qualify and the largest qualifying group is one
		// frame. Built from the live file's own first sample so it carries a
		// real fingerprint, with the sky moved to make the sibling.
		std::vector<LedgerVignette::FrameSample> Pair;
		if (!Samples.empty())
		{
			LedgerVignette::FrameSample A = Samples[0];
			LedgerVignette::FrameSample B = Samples[0];
			B.ShotId = A.ShotId + "_sky_sibling";
			B.SkyIntensity = A.SkyIntensity + 0.25;
			B.Applied = A.Applied + "/planted-sky-sibling";   // another group, same family
			B.MeanLuma = A.MeanLuma + 0.05;
			B.GroundP05 = B.MeanLuma * 0.50;
			B.GroundP50 = B.MeanLuma * 0.80;
			Pair.push_back(A);
			Pair.push_back(B);
		}
		const std::string P2 = LedgerVignette::NullSeriesLine(Pair);
		std::printf("    two frames, one family, two groups: %s\n", P2.substr(0, 300).c_str());
		Check(P2.find("nullSeriesStatus=TOO-FEW-SAMPLES") != std::string::npos
		      && P2.find("nullSeriesVerdict=nothing-measured/one-frame-cannot-hold-a-spread")
		         != std::string::npos
		      && P2.find("nullSeriesFamilies=1/of=1/") != std::string::npos
		      && P2.find("nullSeriesTiedGroups=1/of=2/qualifying-groups-examined/")
		         != std::string::npos,
		      "a family that holds a step whose largest qualifying group is one frame still "
		      "says TOO-FEW-SAMPLES rather than printing a spread of zero, so the two refusals "
		      "are told apart by the line and not by the reader", P2);
		Check(EveryTokenIsKeyValue(Z) && EveryTokenIsKeyValue(O) && EveryTokenIsKeyValue(P2),
		      "all three refusing null series lines are space-free too");
		// AMENDMENT 5: THE TIE COUNTER COUNTS GROUPS, AND THIS IS THE RUN THAT
		// FAILS ON THE CODE THAT COUNTED FRAMES.
		//
		// Section 9 of game-design/decision-2026-09-10-ruling-the-four-lane-
		// batch.md. The old loop in NullSeriesLine ran over FRAMES and
		// incremented once per frame of a rival group, so ONE rival group of
		// seven frames printed nullSeriesTiedGroups=7 and read as seven rival
		// groups. Nothing in the repository asserted the key: one grep hit, the
		// emit itself, which is how it stayed latent while the live spec had a
		// single largest group.
		//
		// WHAT MAKES THESE CATCHING RUNS AND NOT DECORATION. On the old
		// frame-counting code the two-way fixture below prints 3 and the
		// three-way fixture prints 6, because every frame of every rival group
		// incremented once. Both Checks fail there and pass here. The ties are
		// PLANTED, because the committed spec has exactly one largest group and
		// a tie cannot be waited for; the accepting case is the live line NS
		// above, read by name so the no-tie reading is watched too.
		//
		// AND THE DENOMINATOR IS QUALIFYING GROUPS SINCE 2026-09-16, not
		// distinct ones: a group the rule never weighed is not a rival this
		// count may claim to have weighed. On the live file that is 15 of the
		// 30 distinct groups, both counted by the tally above and neither
		// typed here.
		char WantTies[112];
		std::snprintf(WantTies, sizeof(WantTies),
		              "nullSeriesTiedGroups=0/of=%d/qualifying-groups-examined/",
		              NT.QualifyingGroups);
		Check(NS.find(WantTies) != std::string::npos && NT.QualifyingGroups < NT.DistinctGroups,
		      "the live spec has ONE largest qualifying group so the tie count is zero, and "
		      "the zero ships as its denominator the number of qualifying groups an "
		      "independent tally over the same conditions examined, which is fewer than the "
		      "distinct groups because the night groups are not among them",
		      std::string(WantTies) + " over " + std::to_string(NT.DistinctGroups)
		      + " distinct against: " + NS);
		{
			// TWO GROUPS OF THREE PLUS A SINGLETON, so the tie count and the
			// denominator are different numbers and neither can stand in for
			// the other. One rival group: the answer is 1, never 3.
			//
			// ONE FAMILY, THREE SKY VALUES, AMENDED 2026-09-16. The three
			// groups used to carry one sky value and their own no-sky key
			// each, which under the family rule means no family holds a step
			// and nothing qualifies: the fixture would have printed
			// NO-FAMILY-HOLDS-A-STEP and tested the tie counter on nothing.
			// They now sit in ONE no-sky family at three sky values, which is
			// the grid's own shape and is internally consistent in the way the
			// real fingerprint is: same applied key means same sky, same
			// family at another sky means another applied key. The tie count
			// and its denominator are unchanged by the amendment, so this is
			// still the run that fails on the frame-counting code.
			const char* Two[7] = { "gA", "gA", "gA", "gB", "gB", "gB", "gC" };
			const double TwoSky[7] = { 1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 3.0 };
			std::vector<LedgerVignette::FrameSample> Tie;
			for (int I = 0; I < 7; ++I)
			{
				LedgerVignette::FrameSample F;
				char Sid[32];
				std::snprintf(Sid, sizeof(Sid), "tie_%02d", I);
				F.ShotId = Sid;
				F.CameraId = "cam_tie";
				F.Applied = Two[I];
				F.AppliedNoSky = "fam_tie";
				F.SkyIntensity = TwoSky[I];
				F.bMeasured = true;
				F.MeanLuma = 0.50;
				F.GroundP05 = 0.25;
				F.GroundP50 = 0.40;
				Tie.push_back(F);
			}
			const std::string T2 = LedgerVignette::NullSeriesLine(Tie);
			std::printf("    planted two-way tie: %s\n",
			            T2.substr(0, 260).c_str());
			Check(T2.find("nullSeriesTiedGroups=1/of=3/qualifying-groups-examined/"
			              "groups-not-frames/") != std::string::npos,
			      "one rival group of three frames prints ONE tied GROUP of three "
			      "qualifying groups examined, where the frame-counting code printed 3",
			      T2);
			Check(T2.find("nullSeriesFamilies=1/of=1/") != std::string::npos
			      && T2.find("nullSeriesOutsideStepFamilies=0/of=7/") != std::string::npos,
			      "and all seven frames are inside the one family that holds a step, so the "
			      "tie is weighed over every group this fixture offers", T2);
			Check(T2.find("nullSeriesIds=tie_00;tie_01;tie_02") != std::string::npos,
			      "and the kept group on a tie is still the first in shot order, which "
			      "the strict greater-than preserves", T2);
			Check(EveryTokenIsKeyValue(T2),
			      "the tied line is space-free, every token a key with a value", T2);
		}
		{
			// THREE GROUPS OF THREE, A SINGLETON, AND ONE UNMEASURED FRAME
			// CARRYING A KEY OF ITS OWN. Two rival groups, four qualifying
			// groups examined, and the unmeasured frame must enter NEITHER
			// number: a denominator larger than the set examined turns a clean
			// result into a false claim with a number on it. One family at
			// four sky values, for the reason the fixture above carries.
			const char* Three[11] = { "gA", "gA", "gA", "gB", "gB", "gB",
			                          "gC", "gC", "gC", "gD", "gZ" };
			const double ThreeSky[11] = { 1.0, 1.0, 1.0, 2.0, 2.0, 2.0,
			                              3.0, 3.0, 3.0, 4.0, 5.0 };
			std::vector<LedgerVignette::FrameSample> Tie3;
			for (int I = 0; I < 11; ++I)
			{
				LedgerVignette::FrameSample F;
				char Sid[32];
				std::snprintf(Sid, sizeof(Sid), "t3_%02d", I);
				F.ShotId = Sid;
				F.CameraId = "cam_tie";
				F.Applied = Three[I];
				F.AppliedNoSky = "fam_tie3";
				F.SkyIntensity = ThreeSky[I];
				F.bMeasured = (I != 10);
				F.MeanLuma = 0.50;
				F.GroundP05 = 0.25;
				F.GroundP50 = 0.40;
				Tie3.push_back(F);
			}
			const std::string T3 = LedgerVignette::NullSeriesLine(Tie3);
			std::printf("    planted three-way tie: %s\n",
			            T3.substr(0, 260).c_str());
			Check(T3.find("nullSeriesTiedGroups=2/of=4/qualifying-groups-examined/"
			              "groups-not-frames/") != std::string::npos,
			      "two rival groups of three frames each print TWO tied GROUPS of four "
			      "qualifying groups examined, where the frame-counting code printed 6",
			      T3);
			Check(T3.find("nullSeriesMeasured=10/of=11/shots-offered") != std::string::npos
			      && T3.find("nullSeriesOutsideStepFamilies=0/of=10/") != std::string::npos,
			      "and the unmeasured frame is outside the tie count, the qualifying-group "
			      "denominator and the outside-frames denominator alike, while the measured "
			      "count still names the eleven offered", T3);
			Check(EveryTokenIsKeyValue(T3),
			      "the three-way tied line is space-free too", T3);
		}
	}

	// ---- QUEUE 235: THE EXPOSURE PIN AND ITS LADDER ----------------------
	//
	// ACCEPTING CASE FIRST, on the live file, then the rejecting cases
	// planted, because a rejection has to be provoked: the repository has no
	// row whose pin failed to land.
	{
		std::printf("  the exposure pin, asked beside read, and the ladder it sets a value from\n");
		// THE LIVE FILE IS THE ACCEPTING FIXTURE, AND THE SERIES IS PRINTED
		// BEFORE ANY BOUND IS READ OFF IT, which is rule 2's order. Four
		// clauses, dictated in section 6 of the 2026-09-14 ruling, evaluated
		// by ReadPins above; the rungs' own values are read off the file and
		// never retyped here.
		bool SceneOk = false;
		const std::string ScenePath = ScenePathBeside(SpecPath);
		const std::string SceneText = Slurp(ScenePath.c_str(), SceneOk);
		bool ProvFound = false;
		const std::string Prov = SceneOk
		    ? JsonStringField(SceneText, "exposure_pin_provenance", ProvFound)
		    : std::string();
		// BOTH READINGS, SO THE GAP BETWEEN THE TWO FILES IS A NUMBER. The
		// piece list is what the Unreal run reads and it is generated without
		// this key; the scene file is where the string is written.
		std::printf("    provenanceFrom=%s sceneRead=%s keyFound=%s "
		            "provenanceChars=%d pieceListDeclares=%s\n",
		            ScenePath.c_str(), SceneOk ? "yes" : "NO-FILE",
		            ProvFound ? "yes" : "NO-KEY", (int)Prov.size(),
		            S.ExposurePinProvenance.c_str());
		const PinReading LivePins = ReadPins(S.Conditions, Prov);
		std::printf("    %s\n", LivePins.Line.c_str());
		// (a) KEPT FROM THE GUARD THIS REPLACES. It cannot be planted from a
		// file and that is not an omission: VignetteSpec.h line 519 requires
		// `exposure_pin` on every condition through NeedNum, fail-closed, so
		// a row that does not answer the pin question never reaches this
		// evaluator; the parse refused the file one step earlier.
		Check(LivePins.bA,
		      "(a) every condition in the live file answers the pin question, pinned plus "
		      "unpinned summing to the condition count",
		      LivePins.Line);
		Check(LivePins.bB,
		      "(b) every sun-on condition asks for a pin and every sun-off condition asks "
		      "for none, both denominators counted so neither half is vacuous",
		      LivePins.Line);
		Check(LivePins.bC,
		      "(c) every sun-on row that is not a ladder rung carries one and the same live "
		      "value, so the run has one live pin and not a scatter",
		      LivePins.Line);
		Check(LivePins.bD,
		      "(d) and that live value is the one the file's exposure_pin_provenance names, "
		      "to the four decimals the shot line prints, with the named rung agreeing while "
		      "it is still in the file",
		      LivePins.Line + " provenance=" + (Prov.empty() ? std::string("EMPTY") : Prov));
		Check(LivePins.RungHi > LivePins.RungLo * 100.0,
		      "the ladder spans more than two decades of the engine's own clamp range, which "
		      "is a bracket rather than a guess",
		      "the value cannot be computed from any committed luma, so the rungs have to "
		      "straddle the answer");
		// ---- FOUR PLANTED REJECTIONS, ALL WATCHED, ACCEPTING CASE ABOVE --
		//
		// Rule 5b: a guard needs a run where the thing it asserts CAN happen.
		// Each plant is the live conditions with ONE edit, judged by the same
		// ReadPins, and each Check names the clause it targets AND asserts
		// the invariant as a whole goes false.
		{
			// 1. A DAY ROW LEFT AT AUTO, planted on the LAST sun-on non-rung
			// row so the live value still reads off the first. This one plant
			// breaks two clauses by construction and the check says so: an
			// auto row is both an unpinned day row and not the live value.
			std::vector<LedgerVignette::Condition> P1 = S.Conditions;
			std::string P1Id = "none";
			for (size_t I = 0; I < P1.size(); ++I)
			{
				if (P1[I].SunOn && !IsLadderRung(P1[I].Id)) { P1Id = P1[I].Id; }
			}
			for (size_t I = 0; I < P1.size(); ++I)
			{
				if (P1[I].Id == P1Id) { P1[I].ExposurePin = 0.0; }
			}
			const PinReading R1 = ReadPins(P1, Prov);
			std::printf("    planted day-row-at-auto on %s: %s\n", P1Id.c_str(), R1.Line.c_str());
			Check(!R1.bB && !R1.bC && R1.bA && !(R1.bA && R1.bB && R1.bC && R1.bD),
			      "planted: one day row left at auto is refused, clause (b) going false and "
			      "clause (c) with it because an auto row is also not the live value",
			      R1.Line);
			// 2. A NIGHT ROW GIVEN A PIN, which clause (c) cannot see because
			// night rows are not live rows: this is (b)'s other direction.
			std::vector<LedgerVignette::Condition> P2 = S.Conditions;
			std::string P2Id = "none";
			for (size_t I = 0; I < P2.size(); ++I)
			{
				if (!P2[I].SunOn && P2Id == "none") { P2Id = P2[I].Id; P2[I].ExposurePin = 0.300; }
			}
			const PinReading R2 = ReadPins(P2, Prov);
			std::printf("    planted night-row-pinned on %s: %s\n", P2Id.c_str(), R2.Line.c_str());
			Check(!R2.bB && R2.bA && R2.bC && R2.bD,
			      "planted: one night row given a day value is refused by clause (b) alone, "
			      "the night staying at auto until a settled night reference exists",
			      R2.Line);
			// 3. TWO DAY ROWS DISAGREEING, both pinned, so (b) holds and (c)
			// is the only clause that can see it.
			std::vector<LedgerVignette::Condition> P3 = S.Conditions;
			std::string P3Id = "none";
			for (size_t I = 0; I < P3.size(); ++I)
			{
				if (P3[I].SunOn && !IsLadderRung(P3[I].Id)) { P3Id = P3[I].Id; }
			}
			for (size_t I = 0; I < P3.size(); ++I)
			{
				if (P3[I].Id == P3Id) { P3[I].ExposurePin = LivePins.Live * 2.0; }
			}
			const PinReading R3 = ReadPins(P3, Prov);
			std::printf("    planted two-day-values on %s: %s\n", P3Id.c_str(), R3.Line.c_str());
			Check(!R3.bC && R3.bA && R3.bB,
			      "planted: two day rows carrying different pins are refused by clause (c), "
			      "which is the scatter a per-row edit would produce",
			      R3.Line);
			// 4. A LIVE VALUE THE PROVENANCE DOES NOT NAME, moved on EVERY
			// live row at once so (a), (b) and (c) all still hold: this is
			// the case no count can catch and the reason clause (d) exists.
			// 0.4102 is the reference sheet's own figure, the number the
			// ruling records as NOT interpolated toward.
			std::vector<LedgerVignette::Condition> P4 = S.Conditions;
			int Moved = 0;
			for (size_t I = 0; I < P4.size(); ++I)
			{
				if (P4[I].SunOn && !IsLadderRung(P4[I].Id)) { P4[I].ExposurePin = 0.4102; ++Moved; }
			}
			const PinReading R4 = ReadPins(P4, Prov);
			std::printf("    planted live-value-not-in-provenance on %d rows: %s\n",
			            Moved, R4.Line.c_str());
			Check(!R4.bD && R4.bA && R4.bB && R4.bC && Moved > 0,
			      "planted: a live value edited onto every day row without re-reading the "
			      "series passes (a), (b) and (c) and is refused by clause (d), which is the "
			      "whole of that clause's reason for existing",
			      R4.Line);
		}
		// THE SEGMENT, FOUR CASES, IN THE ORDER THE RULE ASKS FOR.
		LedgerVignette::ExposurePinIn Held;
		Held.Asked = 0.300; Held.ReadMin = 0.300000011920929; Held.ReadMax = 0.300000011920929;
		Held.bOverMin = true; Held.bOverMax = true; Held.bRead = true; Held.bSunOn = true;
		const std::string HS = LedgerVignette::ExposurePinSegment(Held);
		std::printf("    %s\n", HS.c_str());
		Check(HS.find("shotExposurePin=PINNED-HELD") != std::string::npos
		      && HS.find("shotExposurePinAsked=0.3000") != std::string::npos
		      && HS.find("shotExposurePinRead=0.3000/0.3000") != std::string::npos
		      && HS.find("shotExposurePinOverrides=1/1") != std::string::npos
		      && HS.find("shotExposurePinFamily=day") != std::string::npos,
		      "a pin written as a double and read back as a float is HELD, because the "
		      "separator is one part in a thousand and a float round trip is of order 1e-7",
		      HS);
		Check(EveryTokenIsKeyValue(HS), "the held pin segment is space-free", HS);
		// REJECTING, PLANTED: the readback is the engine's own default range,
		// which is what a write that never reached the component looks like.
		LedgerVignette::ExposurePinIn Lost;
		Lost.Asked = 0.300; Lost.ReadMin = 0.0300; Lost.ReadMax = 8.0000;
		Lost.bOverMin = false; Lost.bOverMax = false; Lost.bRead = true; Lost.bSunOn = false;
		const std::string LS = LedgerVignette::ExposurePinSegment(Lost);
		std::printf("    planted: %s\n", LS.c_str());
		Check(LS.find("shotExposurePin=PINNED-DIFFERS") != std::string::npos
		      && LS.find("shotExposurePinRead=0.0300/8.0000") != std::string::npos
		      && LS.find("shotExposurePinResidual=-0.270000/+7.700000") != std::string::npos
		      && LS.find("shotExposurePinOverrides=0/0") != std::string::npos
		      && LS.find("shotExposurePinFamily=night") != std::string::npos,
		      "a pin that read back as the engine default is DIFFERS, with both signed "
		      "residuals printed, and HELD is not the word", LS);
		Check(!LedgerVignette::ExposurePinHeld(Lost)
		      && LedgerVignette::ExposurePinHeld(Held),
		      "the held test accepts the float round trip and refuses the default range, "
		      "which is the pair of outcomes rule 5b asks for");
		// AND A PIN THAT LANDED ON THE VALUES WITH THE OVERRIDES OFF IS STILL
		// NOT IN FORCE, which is the case a value-only comparison would pass.
		LedgerVignette::ExposurePinIn NoFlags = Held;
		NoFlags.bOverMin = false;
		Check(!LedgerVignette::ExposurePinHeld(NoFlags),
		      "a value that matches with its override flag off is not a pin in force, "
		      "because an unoverridden value is not the value the renderer uses");
		// AUTO, which is not a failure and must not read as one.
		LedgerVignette::ExposurePinIn Auto;
		Auto.Asked = 0.0; Auto.ReadMin = 0.0300; Auto.ReadMax = 8.0000;
		Auto.bRead = true; Auto.bSunOn = true;
		const std::string AS = LedgerVignette::ExposurePinSegment(Auto);
		Check(AS.find("shotExposurePin=AUTO") != std::string::npos
		      && AS.find("shotExposurePinResidual=not-applicable/no-pin-asked") != std::string::npos
		      && AS.find("shotExposurePinRead=0.0300/8.0000") != std::string::npos,
		      "a condition asking for no pin reads AUTO and prints the engine's own clamp "
		      "range rather than a residual against a number nobody asked for", AS);
		// ---- THE LEAK, PLANTED FROM THE ROW THAT REALLY HAPPENED --------
		//
		// vign_grid_null_repeat at f6508b3: asked 0.0000, read 10.0000/10.0000,
		// overrides 1/1, printed as AUTO, frame at 0.0610 which is the pin-10
		// neighbourhood and not auto exposure. THE ACCEPTING CASE IS `Auto`
		// DIRECTLY ABOVE, which has the same asked value and no override and
		// must keep reading AUTO; this is the rejecting one.
		LedgerVignette::ExposurePinIn Leaked;
		Leaked.Asked = 0.0; Leaked.ReadMin = 10.0; Leaked.ReadMax = 10.0;
		Leaked.bOverMin = true; Leaked.bOverMax = true;
		Leaked.bRead = true; Leaked.bSunOn = true;
		const std::string LK = LedgerVignette::ExposurePinSegment(Leaked);
		std::printf("    %s\n", LK.c_str());
		Check(LK.find("shotExposurePin=LEAKED-PIN") != std::string::npos
		      && LK.find("shotExposurePin=AUTO") == std::string::npos
		      && LK.find("shotExposurePinRead=10.0000/10.0000") != std::string::npos,
		      "a row asking for no pin whose component still carries an override is "
		      "LEAKED-PIN and never AUTO, which is the word the run at f6508b3 printed "
		      "over four frames photographed at an earlier rung's exposure", LK);
		Check(LedgerVignette::ExposurePinLeaked(Leaked)
		      && !LedgerVignette::ExposurePinLeaked(Auto)
		      && !LedgerVignette::ExposurePinLeaked(Held),
		      "and the predicate the run tally counts on agrees with the word: the leaked "
		      "row yes, the genuinely auto row no, the pinned row no");
		Check(EveryTokenIsKeyValue(LK), "the leaked shot segment is space-free", LK);
		// ---- WHAT THE WRITE SITE IS TOLD TO DO, BOTH BRANCHES ------------
		//
		// THE BUG WAS AN `if` WITH NO `else` IN THE LAYER THAT DOES NOT
		// COMPILE HERE, so the decision moved into the header and this is the
		// test that could not have existed before. Accepting case first: a
		// pinned condition writes the override on with its value.
		{
			const LedgerVignette::ExposurePinWriteOut WPin =
				LedgerVignette::ExposurePinWriteFor(0.3, true, 0.03, 8.0, 10.0, 10.0);
			Check(WPin.bOverride && WPin.Min == 0.3 && WPin.Max == 0.3,
			      "a condition asking for a pin writes both overrides on and both "
			      "brightnesses to the asked value");
			// AND THE REJECTING CASE, which is the whole fault: an unpinned
			// condition must CLEAR the override and put back what was
			// captured, not leave the last rung standing.
			const LedgerVignette::ExposurePinWriteOut WAuto =
				LedgerVignette::ExposurePinWriteFor(0.0, true, 0.03, 8.0, 10.0, 10.0);
			Check(!WAuto.bOverride && WAuto.Min == 0.03 && WAuto.Max == 8.0,
			      "a condition asking for NO pin clears both overrides and restores the "
			      "CAPTURED values, so the next unpinned frame is not photographed at the "
			      "last rung's exposure");
			// AND WITH NOTHING CAPTURED, the values are left where they are
			// rather than invented: a number typed in here would be this
			// file's idea of the engine's default.
			const LedgerVignette::ExposurePinWriteOut WNone =
				LedgerVignette::ExposurePinWriteFor(0.0, false, 0.0, 0.0, 10.0, 10.0);
			Check(!WNone.bOverride && WNone.Min == 10.0 && WNone.Max == 10.0,
			      "with nothing captured the flags still clear and the values are left "
			      "alone, because an uncaptured default would be a guess");
		}
		// AND NOTHING READ, which is not a zero.
		LedgerVignette::ExposurePinIn Never;
		Never.Asked = 3.0;
		const std::string NV = LedgerVignette::ExposurePinSegment(Never);
		Check(NV.find("shotExposurePin=NOT-READ") != std::string::npos
		      && NV.find("shotExposurePinRead=nothing-measured/nothing-measured") != std::string::npos
		      && NV.find("shotExposurePinResidual=nothing-measured") != std::string::npos,
		      "a placement that reached no camera component prints the words and never a "
		      "zero residual that would read as agreement", NV);
		Check(EveryTokenIsKeyValue(AS) && EveryTokenIsKeyValue(NV) && EveryTokenIsKeyValue(LS),
		      "the auto, not-read and planted pin segments are all space-free");
		// AND ALL FOUR CASES CARRY ONE KEY SET, WHICH IS THE DUPKEYS RULE AT
		// WRITE TIME. A key is ambiguous when it takes different values under
		// two different line SHAPES, and a file holding pinned rows and
		// unpinned rows holds both shapes. Counted rather than eyeballed.
		{
			std::vector<std::string> KH, KA, KN, KL;
			KeysOf(HS, KH); KeysOf(AS, KA); KeysOf(NV, KN); KeysOf(LS, KL);
			bool bSame = (KH.size() == KA.size() && KH.size() == KN.size()
			              && KH.size() == KL.size());
			for (size_t I = 0; bSame && I < KH.size(); ++I)
			{
				if (KH[I] != KA[I] || KH[I] != KN[I] || KH[I] != KL[I]) { bSame = false; }
			}
			std::printf("    pin segment keys: held=%d auto=%d notRead=%d planted=%d same=%s\n",
			            (int)KH.size(), (int)KA.size(), (int)KN.size(), (int)KL.size(),
			            bSame ? "yes" : "no");
			Check(bSame && KH.size() == 8,
			      "a pinned row, an unpinned row, a row that read nothing and a row whose pin "
			      "did not hold print the SAME eight keys in the same order, so no key on a "
			      "shot line is ambiguous across the shapes one file holds",
			      "the values say which case it is; the key names never move");
		}
		// ---- THE LADDER LINE, ACCEPTING CASE FIRST ----------------------
		//
		// TWO RUNGS, BOTH HALVES EACH, AND THE NUMBERS ARE THE 83dec33
		// READINGS so the expected difference is arithmetic rather than a
		// guess: the run's own first frame read 0.6102 and its repeat 0.9562,
		// a difference of 0.3460, and that pair is what the rung at the wrong
		// pin is expected to look like.
		std::vector<LedgerVignette::ExposureLadderSample> L;
		{
			LedgerVignette::ExposureLadderSample A;
			A.ShotId = "vign_pin_003_afterday"; A.Pin = 0.030; A.bAfterNight = false;
			A.bMeasured = true; A.bPinHeld = true; A.MeanLuma = 0.9562;
			A.ClipHi = 604972; A.ClipLo = 0; A.Pixels = 921600;
			L.push_back(A);
			LedgerVignette::ExposureLadderSample B;
			B.ShotId = "vign_pin_003_afternight"; B.Pin = 0.030; B.bAfterNight = true;
			B.bMeasured = true; B.bPinHeld = true; B.MeanLuma = 0.6102;
			B.ClipHi = 10283; B.ClipLo = 0; B.Pixels = 921600;
			L.push_back(B);
			LedgerVignette::ExposureLadderSample C;
			C.ShotId = "vign_pin_300_afterday"; C.Pin = 3.000; C.bAfterNight = false;
			C.bMeasured = true; C.bPinHeld = true; C.MeanLuma = 0.4010;
			C.ClipHi = 0; C.ClipLo = 12; C.Pixels = 921600;
			L.push_back(C);
			LedgerVignette::ExposureLadderSample D;
			D.ShotId = "vign_pin_300_afternight"; D.Pin = 3.000; D.bAfterNight = true;
			D.bMeasured = true; D.bPinHeld = true; D.MeanLuma = 0.4008;
			D.ClipHi = 0; D.ClipLo = 12; D.Pixels = 921600;
			L.push_back(D);
		}
		const std::string LL = LedgerVignette::ExposureLadderLine(L);
		std::printf("    %s\n", LL.c_str());
		Check(LL.find("ladderStatus=ALL") != std::string::npos
		      && LL.find("ladderRows=4/of=4/ladder-rows-offered") != std::string::npos
		      && LL.find("ladderPinsPaired=2/of=2/") != std::string::npos
		      && LL.find("ladderRowsHeld=4/of=4/") != std::string::npos,
		      "four rows over two rungs, both halves each, with every count shipping its "
		      "denominator", LL);
		Check(LL.find("ladder.pin0.0300.afterDayMinusAfterNightMeanLuma=+0.3460")
		      != std::string::npos
		      && LL.find("ladder.pin3.0000.afterDayMinusAfterNightMeanLuma=+0.0002")
		         != std::string::npos,
		      "the pairing prints as a signed DIFFERENCE per rung, and on the 83dec33 pair "
		      "it is the 0.3460 that run measured between one camera and its own repeat", LL);
		Check(LL.find("ladderSmallestDiffPin=3.0000") != std::string::npos
		      && LL.find("ladderSmallestDiff=0.0002") != std::string::npos
		      && LL.find("ladderVerdict=SERIES-ONLY/") != std::string::npos
		      && LL.find("ladderVerdict=CLEAR") == std::string::npos,
		      "the smallest difference is NAMED and nothing is called agreement, because no "
		      "bound on this difference has been measured yet", LL);
		Check(LL.find("ladder.pin0.0300.afterDayClipHi=604972/921600") != std::string::npos
		      && LL.find("ladder.pin3.0000.afterNightClipLo=12/921600") != std::string::npos,
		      "both clip counts ride the line with their denominators, because a mean cannot "
		      "see a blown frame and a pin chosen on the mean alone would crush or blow one "
		      "end of the run", LL);
		Check(EveryTokenIsKeyValue(LL), "the ladder line is space-free", LL);
		// REJECTING, PLANTED: A RUNG WITH ONE HALF IS NOT A RUNG.
		{
			std::vector<LedgerVignette::ExposureLadderSample> Half;
			Half.push_back(L[0]);
			const std::string HL = LedgerVignette::ExposureLadderLine(Half);
			std::printf("    planted: %s\n", HL.c_str());
			Check(HL.find("ladderPinsPaired=0/of=1/") != std::string::npos
			      && HL.find("ladder.pin0.0300.missing=the-after-night-half") != std::string::npos
			      && HL.find("ladder.pin0.0300.afterDayMinusAfterNightMeanLuma=nothing-measured")
			         != std::string::npos
			      && HL.find("ladderSmallestDiff=nothing-measured") != std::string::npos,
			      "a rung photographed only after a day frame names the half it is missing "
			      "and prints no difference, because a difference against an absent frame "
			      "would be a number with nothing in it", HL);
			Check(EveryTokenIsKeyValue(HL), "the half-rung ladder line is space-free", HL);
		}
		// AND A ROW THAT NEVER LANDED IS OUTSIDE THE MEASURED COUNT AND STILL
		// INSIDE THE DENOMINATOR, which is rule 3b.
		{
			std::vector<LedgerVignette::ExposureLadderSample> Lost2 = L;
			Lost2[1].bMeasured = false;
			const std::string XL = LedgerVignette::ExposureLadderLine(Lost2);
			Check(XL.find("ladderStatus=PARTIAL") != std::string::npos
			      && XL.find("ladderRows=3/of=4/ladder-rows-offered") != std::string::npos
			      && XL.find("ladderPinsPaired=1/of=2/") != std::string::npos,
			      "a row whose frame never landed leaves the measured count and stays in "
			      "the denominator, and its rung stops being paired", XL);
		}
		// AND A RUN WITH NO LADDER AT ALL SAYS SO.
		{
			std::vector<LedgerVignette::ExposureLadderSample> None2;
			const std::string ZL = LedgerVignette::ExposureLadderLine(None2);
			std::printf("    %s\n", ZL.c_str());
			Check(ZL.find("ladderStatus=NOTHING-MEASURED") != std::string::npos
			      && ZL.find("ladderRows=0/of=0/ladder-rows-offered") != std::string::npos
			      && ZL.find("ladderSmallestDiff=nothing-measured") != std::string::npos,
			      "a run that photographed no ladder row prints the words, and its zero "
			      "ships a denominator", ZL);
			Check(EveryTokenIsKeyValue(ZL), "the nothing-measured ladder line is space-free", ZL);
		}
		// ---- THE WHOLE-RUN PIN LINE, AND THE COST ON IT ------------------
		LedgerVignette::ExposurePinRun RunIn;
		RunIn.RowsAsking = 8; RunIn.RowsHeld = 8; RunIn.RowsRead = 37;
		RunIn.RowsLeaked = 0; RunIn.RowsOffered = 37;
		RunIn.CondsWithPin = 24; RunIn.CondsOffered = 27;
		RunIn.Provenance = "run41/f6508b3/cond.pin_030/cam_hook";
		const std::string PD = LedgerVignette::ExposurePinDoneLine(RunIn);
		std::printf("    %s\n", PD.c_str());
		Check(PD.find("expPinStatus=ALL-HELD") != std::string::npos
		      && PD.find("expPinRowsAsking=8/of=37/shots-offered") != std::string::npos
		      && PD.find("expPinRowsHeld=8/of=8/shots-asking-for-a-pin") != std::string::npos
		      && PD.find("expPinRowsLeaked=0/of=29/shots-asking-for-NO-pin") != std::string::npos,
		      "the run line carries the counts with their denominators, and the zero leak "
		      "ships the count of rows that COULD have leaked rather than the shot total", PD);
		Check(PD.find("expPinConditions=24/of=27/conditions-in-the-spec") != std::string::npos
		      && PD.find("expPinConstantSet=yes/") != std::string::npos
		      && PD.find("expPinProvenance=run41/f6508b3/cond.pin_030/cam_hook")
		         != std::string::npos,
		      "a spec carrying a live pin reads expPinConstantSet=yes and names where the "
		      "value came from, which is queue 219's acceptance", PD);
		Check(PD.find("expPinCost=a-pinned-frame-can-never-judge-an-adaptation-moment/"
		              "walking-out-of-a-dark-alley-is-the-example") != std::string::npos,
		      "and the cost of the pin is restated where a reader of the verdict meets it, "
		      "not only in a comment", PD);
		// THE ACCEPTING CASE FOR THE OTHER BRANCH: a spec carrying no pin at
		// all must still read `no`, which is what the line said unconditionally
		// before 2026-09-14 whatever the spec held.
		{
			LedgerVignette::ExposurePinRun NoPin = RunIn;
			NoPin.CondsWithPin = 0; NoPin.RowsAsking = 0; NoPin.RowsHeld = 0;
			NoPin.Provenance = "";
			const std::string PN = LedgerVignette::ExposurePinDoneLine(NoPin);
			Check(PN.find("expPinConstantSet=no/") != std::string::npos
			      && PN.find("expPinConditions=0/of=27/conditions-in-the-spec") != std::string::npos
			      && PN.find("expPinProvenance=nothing-declared") != std::string::npos
			      && PN.find("expPinStatus=NONE-ASKED") != std::string::npos,
			      "a spec carrying no pin reads no, and a file that declared no provenance "
			      "prints the words rather than an empty value", PN);
		}
		// ---- THE LEAK, AND IT OUTRANKS ALL-HELD --------------------------
		//
		// THE RUN THIS IS PLANTED FROM IS REAL. At f6508b3 the line read
		// expPinStatus=ALL-HELD while four rows of thirty seven were
		// photographed at an earlier rung's exposure, because nothing counted
		// them. Planting the count is the rejecting case; the accepting case
		// is RunIn above, whose leak is zero over a denominator of 29.
		{
			LedgerVignette::ExposurePinRun Leak = RunIn;
			Leak.RowsLeaked = 4;
			const std::string PL = LedgerVignette::ExposurePinDoneLine(Leak);
			std::printf("    %s\n", PL.c_str());
			Check(PL.find("expPinStatus=LEAKED") != std::string::npos
			      && PL.find("expPinStatus=ALL-HELD") == std::string::npos
			      && PL.find("expPinRowsLeaked=4/of=29/shots-asking-for-NO-pin")
			         != std::string::npos,
			      "four leaked rows outrank eight held pins, which is the reading the run "
			      "at f6508b3 could not give", PL);
			Check(EveryTokenIsKeyValue(PL), "the leaked run line is space-free", PL);
		}
		LedgerVignette::ExposurePinRun ZeroIn;
		const std::string PZ = LedgerVignette::ExposurePinDoneLine(ZeroIn);
		Check(PZ.find("expPinStatus=NOTHING-MEASURED") != std::string::npos
		      && PZ.find("expPinStatus=ALL-HELD") == std::string::npos,
		      "a run that offered no shot is NOTHING-MEASURED and not all-held over zero", PZ);
		LedgerVignette::ExposurePinRun PartIn = RunIn;
		PartIn.RowsHeld = 7;
		const std::string PP2 = LedgerVignette::ExposurePinDoneLine(PartIn);
		Check(PP2.find("expPinStatus=PARTIAL") != std::string::npos
		      && PP2.find("expPinRowsHeld=7/of=8/") != std::string::npos,
		      "one row of eight whose pin did not hold makes the run PARTIAL, which is the "
		      "reading a count without a denominator could not give", PP2);
		Check(EveryTokenIsKeyValue(PD) && EveryTokenIsKeyValue(PZ) && EveryTokenIsKeyValue(PP2),
		      "all three whole-run pin lines are space-free");
		// AND THE TWO LINES MAY NOT COLLIDE ON A KEY NAME, which is the
		// write-time half of the rule tools/verdict-dupkeys.py enforces at
		// read time. KEY NAMES AND NOT SUBSTRINGS: the run line's own prose
		// says it prints the ladder series only, and a substring test on the
		// word would refuse a line that shares no key at all.
		{
			std::vector<std::string> LK, PK;
			KeysOf(LL, LK);
			KeysOf(PD, PK);
			int Shared = 0;
			for (size_t A = 0; A < LK.size(); ++A)
			{
				for (size_t B = 0; B < PK.size(); ++B)
				{
					if (LK[A] == PK[B]) { ++Shared; }
				}
			}
			std::printf("    ladder keys=%d runLine keys=%d shared=%d\n",
			            (int)LK.size(), (int)PK.size(), Shared);
			Check(Shared == 0 && !LK.empty() && !PK.empty(),
			      "the ladder line and the run line share no key name over the keys each "
			      "carries, so a grep for either cannot return the other's value",
			      "and the zero ships both denominators");
		}
	}

	// ---- QUEUE 333: WHERE THE LANTERN'S SOLID LANDS ON THE FRAME ---------
	//
	// THE ACCEPTING FIXTURE IS THE LIVE FILE'S OWN LANTERN, which is this
	// project's rule for anything that checks the project itself: the piece
	// comes out of production/specs/vignette-pieces.json as committed, with
	// its real 0.55 by 0.2 by 0.3 box, and only the camera is synthetic. A
	// camera built here rather than taken from the scene file is deliberate:
	// it is placed at the lamp's own height looking straight along +x, which
	// is the one arrangement whose projection has a closed form, so the check
	// below is an ARITHMETIC IDENTITY and not a re-statement of the code.
	//
	// The rejecting fixtures are synthetic because a refusal has to be
	// provoked: the committed street has no lantern behind the camera in it.
	{
		std::printf("  -- queue 333: the lantern's eight corners --\n");
		int LanternAt = -1;
		for (size_t I = 0; I < S.Pieces.size(); ++I)
		{
			if (S.Pieces[I].Emissive) { LanternAt = (int)I; break; }
		}
		Check(LanternAt >= 0,
		      "the committed street carries an emissive piece for the lamp instrument "
		      "to be exercised against");
		if (LanternAt >= 0)
		{
			const LedgerVignette::Piece& L = S.Pieces[(size_t)LanternAt];
			const int FW = 1280, FH = 720;
			const double Pi = 3.14159265358979323846;
			std::printf("    lantern %s box %.3fx%.3fx%.3f at (%.3f,%.3f,%.3f)\n",
			            L.Name.c_str(), L.SX, L.SY, L.SZ, L.X, L.Y, L.Z);
			Check(L.PitchDeg == 0.0 && L.YawDeg == 0.0 && L.RollDeg == 0.0,
			      "and it is unrotated in the file, which is what lets the closed form "
			      "below be written down at all");

			LedgerVignette::Camera C;
			C.Id = "queue333_synthetic";
			C.GroundY = 0.0;
			C.EyeHeightM = L.Y;     // dead level with the lamp head
			C.FovVerticalDeg = 50.0;
			C.YawDeg = 0.0;         // forward is +x, right is +z
			C.PitchDeg = 0.0;
			const double D = 10.0;
			C.X = L.X - D;
			C.Z = L.Z;

			const LedgerSurface::ScreenBox B = LedgerSurface::PieceScreenBox(C, L, FW, FH);
			std::printf("    ahead=%d inFrame=%d x %.3f..%.3f y %.3f..%.3f dist=%.3f\n",
			            B.CornersAhead, B.CornersInFrame, B.X0, B.X1, B.Y0, B.Y1, B.DistM);
			Check(B.bMeasured && B.CornersAhead == 8 && B.CornersInFrame == 8,
			      "a lantern square in front of the camera answers on all eight corners");
			Check(std::fabs(B.CxPx - FW * 0.5) < 1e-6
			      && std::fabs(B.CyPx - FH * 0.5) < 1e-6
			      && B.X0 < B.CxPx && B.CxPx < B.X1
			      && B.Y0 < B.CyPx && B.CyPx < B.Y1,
			      "its centre lands in the middle of the frame and inside its own box");

			// THE CLOSED FORM. The widest corner is the NEAR face's, at
			// sz/2 to the side and sx/2 closer than the centre, so a box
			// measured from the centre depth alone would be too narrow. This
			// is the half of the reading that four corners of one face could
			// not give.
			const double TanH = std::tan(LedgerVignette::HorizontalFovDeg(
				C.FovVerticalDeg, FW, FH) * 0.5 * Pi / 180.0);
			const double TanV = std::tan(C.FovVerticalDeg * 0.5 * Pi / 180.0);
			const double WantX1 = FW * (0.5 + 0.5 * ((L.SZ * 0.5) / (D - L.SX * 0.5)) / TanH);
			const double WantY0 = FH * (0.5 - 0.5 * ((L.SY * 0.5) / (D - L.SX * 0.5)) / TanV);
			std::printf("    x1 got %.6f want %.6f | y0 got %.6f want %.6f\n",
			            B.X1, WantX1, B.Y0, WantY0);
			Check(std::fabs(B.X1 - WantX1) < 1e-6 && std::fabs(B.Y0 - WantY0) < 1e-6,
			      "and its edges are the near face's corners to six decimal places, "
			      "which is the pinhole written out independently rather than the "
			      "function asked twice");

			// THE YAW PATH, WHICH IS THE PART THAT WAS COPIED AND THEREFORE
			// THE PART MOST WORTH WATCHING. Turned a quarter turn, the file's
			// own rotation takes +x toward +z, so the 0.55 m side faces the
			// camera where the 0.30 m side did and the box gets WIDER by a
			// ratio nothing in the code computes.
			LedgerVignette::Piece Turned = L;
			Turned.YawDeg = 90.0;
			const LedgerSurface::ScreenBox T =
				LedgerSurface::PieceScreenBox(C, Turned, FW, FH);
			const double Plain  = B.X1 - B.X0;
			const double Yawed  = T.X1 - T.X0;
			const double WantRatio = ((L.SX / (D - L.SZ * 0.5)) / (L.SZ / (D - L.SX * 0.5)));
			std::printf("    widthPlain=%.4f widthYawed=%.4f ratio=%.4f want=%.4f\n",
			            Plain, Yawed, Yawed / Plain, WantRatio);
			Check(T.bMeasured && std::fabs((Yawed / Plain) - WantRatio) < 1e-6,
			      "a quarter turn in yaw presents the long side, by the exact ratio the "
			      "file's own rotation order predicts");

			// REJECTING (1): THE LANTERN BEHIND THE CAMERA. Nothing ahead,
			// nothing measured, and the box is not a box.
			LedgerVignette::Camera Away = C;
			Away.YawDeg = 180.0;
			const LedgerSurface::ScreenBox Behind =
				LedgerSurface::PieceScreenBox(Away, L, FW, FH);
			Check(!Behind.bMeasured && Behind.CornersAhead == 0
			      && Behind.CornersInFrame == 0,
			      "a lantern behind the camera measures nothing on all eight corners");

			// REJECTING (2), AND IT IS THE CASE THE EIGHT-CORNER RULE EXISTS
			// FOR: the camera standing level with the lamp at its own x, so
			// four corners are in front of the eye plane and four behind. A
			// bounding box of the four that answered would be a drawing. The
			// count is on the struct either way, so a caller can tell this
			// from behind-the-camera without guessing.
			LedgerVignette::Camera Inside = C;
			Inside.X = L.X;
			const LedgerSurface::ScreenBox Straddle =
				LedgerSurface::PieceScreenBox(Inside, L, FW, FH);
			std::printf("    straddling the eye plane: ahead=%d of 8\n",
			            Straddle.CornersAhead);
			Check(!Straddle.bMeasured && Straddle.CornersAhead == 4,
			      "a lantern straddling the eye plane reports four of eight and refuses "
			      "to call itself measured");
		}
	}

	// ---- QUEUE 361: THE SKY DOME'S LUMINANCE, PER CONDITION -------------
	//
	// WHAT THIS IS FOR. The dome is an UNLIT surface, so it renders at its
	// own value whatever the lights do, and its value was one global
	// constant written once at build: a night row rendered at 3.3 times the
	// mean of the same file shot the run before. The drive that fixes it
	// keeps its arithmetic, its guard and its string here, where g++ runs
	// them, because the engine file they are called from cannot be compiled
	// in the container that writes it and an unrun formatter printing a
	// plausible string is the silent-instrument failure.
	//
	// ACCEPTING CASE FIRST, AND IT IS THE TWO NUMBERS THE LIVE SCENE FILE
	// CARRIES: overcast_day at 0.70 and the night conditions at 0.35.
	{
		const double Day   = LedgerVignette::SkyDomeLuminance(0.70, 1.0);
		const double Night = LedgerVignette::SkyDomeLuminance(0.35, 1.0);
		std::printf("    skyDomeLuminance: day=%.3f night=%.3f gain=1.000\n",
		            Day, Night);
		Check(std::fabs(Day - 0.70) < 1e-12 && std::fabs(Night - 0.35) < 1e-12,
		      "the dome's luminance is the condition's sky_intensity times the gain, "
		      "for both of the live file's values");
		Check(Day != Night,
		      "and a day row and a night row therefore cannot land on one dome value, "
		      "which is the whole of what queue 361 is");
		Check(std::fabs(LedgerVignette::SkyDomeLuminance(0.35, 2.0) - 0.70) < 1e-12,
		      "the gain scales the condition, so a second value of the series moves "
		      "every condition by the same factor");
		// REJECTING: A NEGATIVE EMISSIVE IS NOT A DARKER SKY. A hand-edited
		// condition asking for one lands on the floor, not on a value the
		// renderer would swallow silently.
		Check(LedgerVignette::SkyDomeLuminance(-0.5, 1.0) == 0.0,
		      "a negative sky_intensity floors at zero rather than reaching the dome");

		// THE GUARD, BOTH OUTCOMES WATCHED. The drive is re-entered on every
		// tick while a condition settles, so the SKIP is the case that costs
		// a parameter write per tick when it is wrong.
		LedgerVignette::SkyLumDrive D;
		Check(LedgerVignette::SkyLumNeeded(D, Night),
		      "the first condition of the run is a write, because nothing has been "
		      "applied yet");
		D.bHaveLast = true; D.Last = Night;
		Check(!LedgerVignette::SkyLumNeeded(D, Night),
		      "a second tick of the SAME condition is skipped");
		Check(LedgerVignette::SkyLumNeeded(D, Day),
		      "and a day row after a night row is a write");

		// THE STRING, WHICH IS THE HALF THAT SHIPS UNRUN IF IT IS WRITTEN
		// ANYWHERE ELSE. Never called first: a drive that never ran and a
		// drive that ran and wrote nothing are different facts.
		LedgerVignette::SkyLumDrive Never;
		const std::string NeverSeg = LedgerVignette::SkyLumDriveSegment(Never, 1.0);
		std::printf("    skyLumDrive never called:%s\n", NeverSeg.c_str());
		Check(NeverSeg.find("nothing-measured") != std::string::npos
		      && NeverSeg.find("skyLumValue=") == std::string::npos,
		      "a drive that was never called says the words and prints no plausible "
		      "zero beside them", NeverSeg);
		Check(NeverSeg.find("skyLumGain=1.000/unitless/FIRST-VALUE-OF-A-SERIES")
		      != std::string::npos,
		      "and still prints the gain, saying on the line that it is the first "
		      "value of a series", NeverSeg);

		LedgerVignette::SkyLumDrive Ran;
		Ran.Calls = 43; Ran.Walks = 2; Ran.Skipped = 41; Ran.Wrote = 2;
		Ran.bHaveLast = true; Ran.Last = Night; Ran.LastAsked = 0.35;
		// A SPACE IN THE ID ON PURPOSE: NoSpaces is what keeps this line
		// readable by a reader that splits on whitespace, and it escapes to
		// a tilde rather than dropping the character.
		Ran.LastFrom = "pin setter night";
		Ran.bReadTaken = true; Ran.ReadSet = Night; Ran.ReadGot = 0.34999999403953552;
		const std::string RanSeg = LedgerVignette::SkyLumDriveSegment(Ran, 1.0);
		std::printf("    skyLumDrive walked:%s\n", RanSeg.c_str());
		Check(RanSeg.find("skyLumValue=0.350") != std::string::npos
		      && RanSeg.find("skyLumSkyIntensity=0.350") != std::string::npos
		      && RanSeg.find("skyLumFrom=pin~setter~night") != std::string::npos,
		      "a drive that walked prints the value applied, the condition field it "
		      "came from and the condition's id", RanSeg);
		Check(RanSeg.find("skyLumDriveWrote=2/ofWalks=2/noInstance=0") != std::string::npos
		      && RanSeg.find("skyLumDriveAsked=43/walked=2/skipped=41") != std::string::npos,
		      "and every zero on the line ships its denominator", RanSeg);
		Check(RanSeg.find("set=0.350/got=0.350/same=yes") != std::string::npos,
		      "the readback of a float parameter widened back agrees with what was set",
		      RanSeg);
		// REJECTING: A DEAD WRITE MUST NOT READ AS AGREEMENT.
		LedgerVignette::SkyLumDrive Dead = Ran;
		Dead.ReadGot = 1.0;
		const std::string DeadSeg = LedgerVignette::SkyLumDriveSegment(Dead, 1.0);
		Check(DeadSeg.find("same=NO/") != std::string::npos,
		      "an instance that kept its old value reads as NO and not as yes",
		      DeadSeg);
		// REJECTING: A WALK THAT FOUND NO DOME IS NOT A WALK THAT WROTE.
		LedgerVignette::SkyLumDrive NoDome;
		NoDome.Calls = 4; NoDome.Walks = 2; NoDome.Skipped = 2; NoDome.NoMid = 2;
		NoDome.bHaveLast = true; NoDome.Last = Night; NoDome.LastAsked = 0.35;
		const std::string NoDomeSeg = LedgerVignette::SkyLumDriveSegment(NoDome, 1.0);
		Check(NoDomeSeg.find("skyLumDriveWrote=0/ofWalks=2/noInstance=2") != std::string::npos
		      && NoDomeSeg.find("skyLumReadback=nothing-measured") != std::string::npos,
		      "a run whose dome never spawned prints zero writes over two walks and "
		      "measures no readback", NoDomeSeg);

		// AND THE RULE EVERY READER OF THESE LINES DEPENDS ON: no spaces
		// inside a value, because every reader splits on whitespace and
		// truncates silently. Every token of every segment above must be a
		// key=value.
		const std::string All[4] = { NeverSeg, RanSeg, DeadSeg, NoDomeSeg };
		int Tokens = 0, Bad = 0;
		std::string BadOne;
		for (int I = 0; I < 4; ++I)
		{
			std::string Tok;
			std::string Line = All[I] + " ";
			for (size_t K = 0; K < Line.size(); ++K)
			{
				if (Line[K] != ' ') { Tok += Line[K]; continue; }
				if (!Tok.empty())
				{
					++Tokens;
					if (Tok.find('=') == std::string::npos)
					{
						++Bad;
						if (BadOne.empty()) { BadOne = Tok; }
					}
					Tok.clear();
				}
			}
		}
		std::printf("    skyLumDrive tokens examined=%d bare=%d\n", Tokens, Bad);
		Check(Tokens > 0 && Bad == 0,
		      "every token of every sky-luminance segment is a key=value, over the "
		      "count of tokens examined",
		      Bad == 0 ? std::string() : ("first bare token: " + BadOne));
	}

	// ---- SURFACE TILING, 23 September ------------------------------------
	// The file has always carried surface_tiling and this reader ignored it;
	// now it reads it, so the committed file's brick has to come back at the
	// measured 0.55 m, a surface the table does not name has to take the
	// file's default, and a file with no table has to keep the caller's
	// convention - which is how every piece list before this one rendered.
	{
		std::printf("   %s\n", LedgerVignette::TilingSegment(S).c_str());
		Check(S.TilingM.count("brick_red") == 1
		      && std::fabs(S.TilingM["brick_red"] - 0.55) < 1e-9
		      && std::fabs(S.TilingM["brick_grey"] - 0.55) < 1e-9,
		      "the committed piece list's brick tiles at the measured 0.55 m, and this reader sees it");
		Check(std::fabs(LedgerVignette::MetresPerTileFor(S, "brick_red", 2.0) - 0.55) < 1e-9,
		      "a named surface takes the file's figure, not the 2 m convention");
		Check(S.TilingDefaultM > 0.0
		      && std::fabs(LedgerVignette::MetresPerTileFor(S, "no_such_surface", 2.0) - S.TilingDefaultM) < 1e-9,
		      "a surface the table does not name takes the file's default");
		LedgerVignette::Spec Empty;
		Check(std::fabs(LedgerVignette::MetresPerTileFor(Empty, "brick_red", 2.0) - 2.0) < 1e-9,
		      "a file with no table keeps the caller's convention, as every older one rendered");
		Check(LedgerVignette::TilingSegment(S).find("tilingFromFile=yes") != std::string::npos
		      && LedgerVignette::TilingSegment(Empty).find("tilingFromFile=no") != std::string::npos,
		      "the materials line says whether the tiling came from the file");
	}

	// ---- THE STREET FROM BLENDER, 23 September ----------------------------
	// The committed export's sidecar parses, every mesh has a name Unreal can
	// make an asset of and Blender did not cut short, and the list of the
	// scene file's pieces the street stands in for keeps the lamps and the
	// pavement furniture while taking the terraces, the ground and the signs.
	{
		bool SOk = false;
		const std::string SText = Slurp("production/assets/street/quay-street.json", SOk);
		LedgerStreet::Sidecar Sc;
		std::string SErr;
		const bool SParsed = SOk && LedgerStreet::ParseSidecar(SText, Sc, SErr);
		Check(SParsed, "the street export's sidecar is on disk and parses", SOk ? SErr : "could not open");
		int LongNames = 0, Dupes = 0, Pictures = 0, Coloured = 0;
		bool MickeysPictured = false;
		for (size_t I = 0; I < Sc.Rows.size(); ++I)
		{
			const LedgerStreet::Row& Rw = Sc.Rows[I];
			if (Rw.Mesh.size() > 60) { ++LongNames; }
			for (size_t J = I + 1; J < Sc.Rows.size(); ++J) { if (Sc.Rows[J].Mesh == Rw.Mesh) { ++Dupes; } }
			if (!Rw.Decal.empty()) { ++Pictures; }
			if (Rw.bHasRgb) { ++Coloured; }
			if (Rw.Mesh == "street_sign_fascia_mickeys_plain" && !Rw.Decal.empty()) { MickeysPictured = true; }
		}
		std::printf("    street: meshes=%d pictured=%d coloured=%d longNames=%d dupes=%d\n",
		            (int)Sc.Rows.size(), Pictures, Coloured, LongNames, Dupes);
		Check(Sc.Rows.size() >= 40 && LongNames == 0 && Dupes == 0,
		      "every street mesh is named once and under Blender's 63-character cut");
		Check(MickeysPictured, "Mickey's sign arrives under its full name with its picture");
		Check(Coloured + Pictures >= (int)Sc.Rows.size() - 2,
		      "all but a couple of street meshes carry a colour or a picture to paint");
		Check(LedgerStreet::ObjectPath("street_slate")
		      == "/Game/Ledger/Street/quay-street/StaticMeshes/street_slate.street_slate",
		      "a mesh's object path is the one the import measured");
		int Kept = 0, Gone = 0, KeptTerrace = 0, GoneFurniture = 0;
		for (size_t I = 0; I < S.Pieces.size(); ++I)
		{
			const LedgerVignette::Piece& P = S.Pieces[I];
			const bool R = LedgerStreet::Replaced(Sc.Replaced, P.Name, P.Shape, P.Asset);
			if (R) { ++Gone; } else { ++Kept; }
			if (!R && (P.Name.compare(0, 5, "east_") == 0 || P.Name.compare(0, 5, "west_") == 0)) { ++KeptTerrace; }
			if (R && (P.Name.compare(0, 6, "column") == 0 || P.Name.compare(0, 7, "lantern") == 0
			          || P.Name.compare(0, 5, "kiosk") == 0 || P.Name.compare(0, 9, "pillarbox") == 0))
			{
				++GoneFurniture;
			}
		}
		std::printf("    street stands in for %d of %d pieces, keeps %d\n", Gone, (int)S.Pieces.size(), Kept);
		Check(Gone > 300 && KeptTerrace == 0,
		      "the street stands in for every terrace piece of the scene file");
		Check(GoneFurniture == 0 && Kept > 100,
		      "and keeps the lamps, the kiosk and the pillar box, which it does not build");
		Check(LedgerStreet::Replaced(Sc.Replaced, "prop_roll_top_chimney_0", "mesh", "roll_top_chimney")
		      && !LedgerStreet::Replaced(Sc.Replaced, "prop_skip_0", "mesh", "skip")
		      && LedgerStreet::Replaced(Sc.Replaced, "decal_anything", "decal", ""),
		      "a roof or wall prop goes, a ground prop stays, a decal goes");
		LedgerStreet::Replaces None;
		Check(!LedgerStreet::Replaced(None, "east_parade_bay0", "box", ""),
		      "a sidecar with no list stands in for nothing");
		Check(LedgerStreet::SrgbByte(0.0) == 0 && LedgerStreet::SrgbByte(1.0) == 255
		      && LedgerStreet::SrgbByte(0.2159) == 128 && LedgerStreet::LinearByte(0.5) == 128,
		      "linear colours become the sRGB bytes a flat albedo texel is read as");
		LedgerStreet::Sidecar Bad;
		Check(!LedgerStreet::ParseSidecar("{\"meshes\": []}", Bad, SErr) && !SErr.empty(),
		      "an empty sidecar is refused with a reason", SErr);

		// THE LOOK'S FIRST STEP: every textured surface can be laid the way
		// Blender lays it - photograph, size, and the palette over it.
		int Textured = 0, TexturedWhole = 0, Glowing = 0;
		const LedgerStreet::Row* Brick = nullptr;
		for (size_t I = 0; I < Sc.Rows.size(); ++I)
		{
			const LedgerStreet::Row& Rw = Sc.Rows[I];
			if (!Rw.SurfaceMap.empty())
			{
				++Textured;
				if (Rw.bHasMean && LedgerStreet::TilesPerMetre(Rw) > 0.0) { ++TexturedWhole; }
			}
			if (Rw.EmitDay >= 0.0) { ++Glowing; }
			if (Rw.Mesh == "street_brick_red") { Brick = &Rw; }
		}
		std::printf("    street look: textured=%d whole=%d glowing=%d\n", Textured, TexturedWhole, Glowing);
		Check(Textured >= 20 && TexturedWhole == Textured,
		      "every textured street surface carries its photograph's average and its tile size");
		Check(Glowing >= 6, "the tubes, the lit rooms, the pictured rooms and the nets carry a glow");
		Check(Brick != nullptr && std::fabs(LedgerStreet::TilesPerMetre(*Brick) - 1.0 / 0.55) < 1e-9,
		      "brick tiles at the measured 0.55 m in the metre UVs, 1.82 copies a metre");
		// AND THE DRAWN SURFACES WIN OVER THE PHOTOGRAPH where the recipe
		// draws one: both bricks, the flags and the tile, each with a size.
		int Drawn = 0;
		for (size_t I = 0; I < Sc.Rows.size(); ++I)
		{
			const LedgerStreet::Row& Rw = Sc.Rows[I];
			if (!Rw.DrawnMap.empty() && Rw.DrawnW > 0.0 && Rw.DrawnH > 0.0)
			{
				++Drawn;
				bool DOk = false;
				Slurp((Rw.DrawnMap + ".png").c_str(), DOk);
				Check(DOk, "a drawn surface the sidecar names is on disk", Rw.DrawnMap);
			}
		}
		Check(Drawn == 4 && Brick != nullptr && Brick->DrawnMap == "production/assets/street/surfaces/brick_red"
		      && std::fabs(Brick->DrawnW - 7.2) < 1e-9,
		      "the two bricks, the flags and the stallriser tile are drawn, the parade's a whole wall high, 7.2 m a copy");
		if (Brick != nullptr)
		{
			const LedgerStreet::Grade Gb = LedgerStreet::PaletteOverPhoto(*Brick);
			Check(Gb.R > Gb.G && Gb.G > Gb.B && std::fabs(Gb.R * Brick->MeanR - Brick->R) < 1e-9,
			      "the parade's red lands on the sandy photograph as a red, and exactly the authored red");
		}
		// WET AS BLENDER WETS IT: the road reaches its near-mirror floor at
		// the day's 0.6 on the one material scalar, the flags stay dull, and
		// a wall takes no water at all.
		Check(LedgerStreet::WetnessParamFor("asphalt", 1.0) == 1.0
		      && std::fabs(LedgerStreet::WetnessParamFor("paving", 1.0) - 0.16 / 0.54) < 1e-9
		      && LedgerStreet::WetnessParamFor("brick_red", 0.9) == 0.0,
		      "the road can reach its floor, the paving only its own share, a wall none");
		Check(std::fabs(LedgerStreet::WetnessParamFor("paving", 1.0, 0.20) - 0.42 / 0.54) < 1e-9
		      && LedgerStreet::WetnessParamFor("brick_red", 1.0, 0.20) == 0.0,
		      "the look file's wet floor moves a wet surface's shine and gives a wall none");
		Check(std::fabs(LedgerStreet::WetDarken("paving", 0.6) - (1.0 - 0.28 * std::pow(0.6, 0.55))) < 1e-9
		      && LedgerStreet::WetDarken("slate", 0.6) == 1.0 && LedgerStreet::WetDarken("asphalt", 0.0) == 1.0,
		      "wet ground darkens by the recipe's 0.28 of the bent figure; dry ground and walls do not");
		// THE LOOK FILE: the committed one parses and supplies all four;
		// a file missing a key keeps that constant; a broken file says so.
		{
			bool LOk = false;
			const std::string LText = Slurp("production/specs/unreal-look.json", LOk);
			LedgerStreet::Look Lk;
			std::string LErr;
			Check(LOk && LedgerStreet::ParseLook(LText, Lk, LErr) && Lk.Read == 17 && Lk.bFromFile,
			      "the committed look file parses and supplies all seventeen settings", LErr);
			LedgerStreet::Look Part;
			Check(LedgerStreet::ParseLook("{\"sky_seen_gain\": 2.5}", Part, LErr) && Part.Read == 1
			      && Part.SkySeenGain == 2.5 && Part.GlowGain == 0.10 && Part.FogFalloff == 0.02,
			      "a key the file leaves out keeps the probe's old constant");
			LedgerStreet::Look Broken;
			Check(!LedgerStreet::ParseLook("not json", Broken, LErr) && !Broken.bFromFile
			      && Broken.SkySeenGain == 1.0,
			      "a broken look file is refused and the constants stand");
		}
		LedgerStreet::Row Plain;
		const LedgerStreet::Grade Gp = LedgerStreet::PaletteOverPhoto(Plain);
		Check(Gp.R == 1.0 && Gp.G == 1.0 && Gp.B == 1.0 && LedgerStreet::TilesPerMetre(Plain) == 0.0,
		      "a surface with no photograph gets no grade and no tiling");
	}

	std::printf("%s: %d of %d check(s) failed\n",
	            gFailed == 0 ? "PASS" : "FAIL", gFailed, gChecks);
	return gFailed == 0 ? 0 : 1;
}
