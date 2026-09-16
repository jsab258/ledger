// THE SELFTEST FOR THE FRAME INSTRUMENT, ACCEPTING CASE FIRST.
//
// Rule 5b: a guard must be tested on the case it should PASS, and shipping
// it means having watched both outcomes. The expensive failure for a blank
// guard is not that it misses a black frame; it is that it rejects every
// frame and the probe reports BLANK for ever while the renderer works.
//
// WHY IT CAN RUN AT ALL. Nothing in FrameStats.h touches an Unreal type, so
// g++ compiles it in this container while the module around it cannot be
// compiled outside CI. That is the whole reason the maths lives there: a
// formatter that ships unrun and prints a plausible string is the quietest
// instrument fault there is.
//
//   g++ -std=c++11 -O1 -Wall -o /tmp/frame-stats-test ue-probe/tests/frame-stats-test.cpp
//   /tmp/frame-stats-test
//
// THOSE ARE THE GATE'S OWN FLAGS, read off ledger/verify.py:1028 on
// 2026-09-16 and not chosen here. This line said -std=c++17 -O0 -Wall
// -Wextra until then, which is a LOOSER standard and a STRICTER warning
// set than the gate uses: code written against it could compile clean by
// hand and fail in CI on a c++14-or-later construct, which is the one
// direction this comment must never be wrong in. If the two ever
// disagree again, verify.py is the truth and this line is the decay.
#include "../Source/LedgerProbe/Public/FrameStats.h"

#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <sstream>
#include <string>
#include <vector>

using namespace LedgerFrame;

static int Failures = 0;
static int Checks   = 0;

static void Check(bool Ok, const std::string& What)
{
	++Checks;
	if (!Ok) { ++Failures; std::printf("  FAIL %s\n", What.c_str()); }
	else     { std::printf("  ok   %s\n", What.c_str()); }
}

static bool Near(double A, double B) { return std::fabs(A - B) < 1e-6; }

// A frame of one colour, which is how a flat field and an all-black frame are
// both built.
static std::vector<unsigned char> Flat(int W, int H, unsigned char B,
                                       unsigned char G, unsigned char R)
{
	std::vector<unsigned char> Px((size_t)W * H * 4, 255);
	for (long long P = 0; P < (long long)W * H; ++P)
	{
		Px[P * 4] = B; Px[P * 4 + 1] = G; Px[P * 4 + 2] = R; Px[P * 4 + 3] = 255;
	}
	return Px;
}

// EVERY VALUE IN THE DONE LINE IS SPACE-FREE, checked mechanically rather
// than by eye. Every reader in this project splits on whitespace, so a value
// with a space in it truncates silently: each whitespace-separated token must
// therefore be a key with a non-empty value, and a value that held a space
// would leave a fragment behind that is not one.
//
// ONE EQUALS PER TOKEN IS NOT THE RULE, and until 2026-09-09 this function
// asserted that it was. The project rule, `.claude/rules/instruments.md`, is
// "no spaces in key=value values; use / and .. for structure", and a value
// carrying its own denominator is this verdict's oldest shape: `skyWrites=0/
// of=0/...` and `propCentreWorstMm=0.00/on=x/of=0` have both shipped for
// weeks, and ue-probe/tests/vignette-spec-test.cpp's EveryTokenIsKeyValue
// accepts exactly that. A2's rank keys are dictated as
// `<key>=<v>/of=<pixels>`, so the denominator rides inside the value where a
// grep for the key cannot lose it. This is the sibling file's predicate,
// copied rather than re-invented so the two test binaries cannot disagree
// about what a verdict token is.
static bool ValuesHaveNoSpaces(const std::string& Line)
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

// A RECTANGLE OF ONE COLOUR PAINTED INTO A FRAME, which is how a lit globe
// and a warm window are both built. Clamped to the image so a fixture cannot
// walk off the end of the buffer.
static void Paint(std::vector<unsigned char>& Px, int W, int H,
                  int X0, int Y0, int X1, int Y1,
                  unsigned char B, unsigned char G, unsigned char R)
{
	if (X0 < 0) { X0 = 0; }
	if (Y0 < 0) { Y0 = 0; }
	if (X1 > W) { X1 = W; }
	if (Y1 > H) { Y1 = H; }
	for (int Y = Y0; Y < Y1; ++Y)
	{
		for (int X = X0; X < X1; ++X)
		{
			const long long P = (long long)Y * (long long)W + (long long)X;
			Px[(size_t)(P * 4)] = B;
			Px[(size_t)(P * 4 + 1)] = G;
			Px[(size_t)(P * 4 + 2)] = R;
			Px[(size_t)(P * 4 + 3)] = 255;
		}
	}
}

int main()
{
	// ---- THE SPACE CHECKER ITSELF, BOTH OUTCOMES, BEFORE IT IS TRUSTED ---
	//
	// It was relaxed on 2026-09-09 from "exactly one equals per token" to the
	// project's actual rule, so it ships with the case it must still REFUSE
	// rather than with an argument that it does. A space inside a value is
	// the fault: every reader here splits on whitespace and truncates in
	// silence, and one red check on a line with a space in it is what stood
	// between this verdict and a key nobody could read.
	{
		Check(ValuesHaveNoSpaces("a.b=1/of=2 c=3/x=4/y=5"),
		      "the space checker ACCEPTS a value carrying its own denominator, which is the dictated shape");
		Check(!ValuesHaveNoSpaces("band.ground.rank=nothing measured"),
		      "and REFUSES a value with a space in it, which is the fault it exists for");
		Check(!ValuesHaveNoSpaces("band.ground.rank= 0.5"),
		      "and refuses an empty value followed by a number, which reads as a key with nothing in it");
		Check(!ValuesHaveNoSpaces("noEqualsHere"), "and refuses a token that is not a key at all");
	}

	// ---- ACCEPTING CASE FIRST: a frame with content must read WROTE ----
	{
		const int W = 8, H = 4;
		std::vector<unsigned char> Px = Flat(W, H, 0, 0, 0);
		for (int Y = 0; Y < H; ++Y)
		{
			for (int X = 4; X < 8; ++X)
			{
				const long long I = ((long long)Y * W + X) * 4;
				Px[I] = 255; Px[I + 1] = 255; Px[I + 2] = 255;
			}
		}
		const FrameStats S = Measure(Px.data(), W, H);
		const std::string Line = DoneLine(S, "FScreenshotRequest::RequestScreenshot",
		                                  "ue-shot.png", 4242, 3.5, 118, "none");
		std::printf("accepting (half black, half white):\n  %s\n", Line.c_str());
		Check(!S.Blank, "a half-white frame is not blank");
		Check(S.Pixels == 32, "pixels counted 32");
		Check(S.NonBlack == 16, "16 non-black pixels");
		Check(Near(S.NonBlackPct, 50.0), "nonBlackPct 50.00 with 32 as its denominator");
		Check(Near(S.MeanLuma, 0.5), "meanLuma 0.5 over every pixel");
		Check(Near(S.MaxLuma, 1.0) && Near(S.MinLuma, 0.0), "min and max luma are the extremes");
		Check(S.DistinctBuckets == 2, "two colour buckets");
		Check(Line.find("shotStatus=WROTE") != std::string::npos, "status reads WROTE");
		Check(ValuesHaveNoSpaces(Line), "no value on the done line contains a space");
	}

	// ---- ACCEPTING, THE THIN CASE: one lit pixel is still a render ----
	{
		const int W = 100, H = 100;
		std::vector<unsigned char> Px = Flat(W, H, 0, 0, 0);
		Px[0] = 255; Px[1] = 255; Px[2] = 255;
		const FrameStats S = Measure(Px.data(), W, H);
		std::printf("accepting (one lit pixel of 10000): nonBlackPct=%.2f distinct=%d blank=%d\n",
		            S.NonBlackPct, S.DistinctBuckets, (int)S.Blank);
		Check(!S.Blank, "one non-black pixel in ten thousand is not blank");
		Check(Near(S.NonBlackPct, 0.01), "and its percentage is 0.01, not rounded to zero meaning");
	}

	// ---- REJECTING: an all-black frame ----
	{
		const int W = 16, H = 9;
		std::vector<unsigned char> Px = Flat(W, H, 0, 0, 0);
		const FrameStats S = Measure(Px.data(), W, H);
		const std::string Line = DoneLine(S, "HighResShot", "ue-shot.png", 900, 9.0, 40, "none");
		std::printf("rejecting (all black):\n  %s\n", Line.c_str());
		Check(S.Blank, "an all-black frame is blank");
		Check(S.NonBlack == 0 && S.Pixels == 144, "the zero ships its denominator: 0 of 144");
		Check(Line.find("shotStatus=BLANK") != std::string::npos, "status reads BLANK");
	}

	// ---- REJECTING, THE ONE A NON-BLACK CHECK ALONE WOULD PASS ----
	// A uniform grey frame has 129,600 non-black pixels and shows nothing.
	// This is the case that makes the distinct-bucket half of the rule earn
	// its place, and it is exactly what an offscreen render with no view
	// target can produce.
	{
		const int W = 480, H = 270;
		std::vector<unsigned char> Px = Flat(W, H, 128, 128, 128);
		const FrameStats S = Measure(Px.data(), W, H);
		const std::string Line = DoneLine(S, "HighResShot", "ue-shot.png", 5000, 9.0, 40, "none");
		std::printf("rejecting (uniform grey):\n  %s\n", Line.c_str());
		Check(S.NonBlack == S.Pixels, "every pixel is non-black, which is why the second half matters");
		Check(S.DistinctBuckets == 1, "one colour bucket");
		Check(S.Blank, "a uniform grey frame is blank");
		Check(Near(S.MeanLuma, 128.0 / 255.0), "the luma weights sum to one");
	}

	// ---- NOTHING MEASURED, IN WORDS ----
	{
		const FrameStats S = Measure(nullptr, 0, 0);
		const std::string Line = DoneLine(S, "NONE", "NONE", 0, 0.0, 0, "no-file-anywhere");
		std::printf("never-ran:\n  %s\n", Line.c_str());
		Check(Line.find("shotStatus=NOTHING-MEASURED") != std::string::npos,
		      "a frame with no pixels prints the words, never a clean zero");
		Check(S.Pixels == 0, "and its pixel count is zero");
		Check(ValuesHaveNoSpaces(Line), "the never-ran line is space-free too");
	}

	// ---- THE ASCII DUMP, WHICH IS THE ONLY VIEW A BLIND CHANNEL GETS ----
	{
		const int W = 96, H = 54;
		std::vector<unsigned char> Px = Flat(W, H, 0, 0, 0);
		for (int Y = 20; Y < 34; ++Y)
		{
			for (int X = 30; X < 66; ++X)
			{
				const long long I = ((long long)Y * W + X) * 4;
				Px[I] = 255; Px[I + 1] = 255; Px[I + 2] = 255;
			}
		}
		const std::string Art = AsciiLuma(Px.data(), W, H);
		int Lines = 1, Lit = 0;
		for (char C : Art) { if (C == '\n') { ++Lines; } if (C == '@') { ++Lit; } }
		std::printf("ascii-luma of a centred white block:\n%s\n", Art.c_str());
		Check(Lines == 27, "27 rows");
		Check(Art.rfind("# ", 0) == 0, "every row is a comment row so no reader parses it");
		Check(Lit > 0, "the block shows up in the dump");
		const std::string Empty = AsciiLuma(nullptr, 0, 0);
		Check(Empty.find("nothing measured") != std::string::npos,
		      "and a dump with no pixels says nothing measured");
	}

	// ---- PixelLine, the per-sample half (Phase B) ----------------------
	//
	// Four shots in one run means four sample lines, and the whole-run keys
	// on DoneLine would be printed four times as if each were that shot's.
	// This line must carry the pixel statistics and NOT those keys.
	{
		unsigned char Px[16];
		for (int I = 0; I < 4; ++I)
		{
			Px[I * 4 + 0] = (unsigned char)(I * 60);
			Px[I * 4 + 1] = (unsigned char)(I * 40);
			Px[I * 4 + 2] = (unsigned char)(I * 20);
			Px[I * 4 + 3] = 255;
		}
		const LedgerFrame::FrameStats S = LedgerFrame::Measure(Px, 2, 2);
		const std::string L = LedgerFrame::PixelLine(S);
		std::printf("    %s\n", L.c_str());
		Check(L.find("shotSecondsWaited") == std::string::npos
		      && L.find("shotTicks") == std::string::npos,
		      "the per-sample line carries no whole-run key that would be a lie on four lines");
		Check(L.find("shotDistinctBuckets=") != std::string::npos
		      && L.find("/32768") != std::string::npos,
		      "and it carries the bucket count with its denominator");
		Check(L.find("shotBlank=no") != std::string::npos,
		      "a frame with four different colours is not blank");
		const LedgerFrame::FrameStats Flat = LedgerFrame::Measure(Px, 0, 0);
		const std::string FL = LedgerFrame::PixelLine(Flat);
		Check(FL.find("shotBlank=NOTHING-MEASURED") != std::string::npos,
		      "and a frame with no pixels says nothing measured rather than blank");
		// NO SPACE INSIDE ANY VALUE, which is the fault that truncates every
		// reader in this project silently.
		int Pairs = 0, Bad = 0;
		std::string Tok;
		for (size_t I = 0; I <= L.size(); ++I)
		{
			if (I == L.size() || L[I] == ' ')
			{
				const size_t Eq = Tok.find('=');
				if (Eq != std::string::npos) { ++Pairs; if (Eq + 1 >= Tok.size()) ++Bad; }
				Tok.clear();
			}
			else { Tok += L[I]; }
		}
		std::printf("    pixel line: keyValuePairs=%d emptyValues=%d/%d\n", Pairs, Bad, Pairs);
		Check(Pairs >= 9 && Bad == 0, "every key on the per-sample line carries a value");
	}


	// ---- QUEUE 059 (b): CLIPPING, ACCEPTING CASE FIRST -----------------
	//
	// The accepting case for an exposure instrument is not a blown frame. It
	// is a frame with a KNOWN amount of clipping in it, counted exactly, so
	// that a run reading 13.4% blown is believed and a run reading 0.00% is
	// known to have looked. Rule 5b: the case it should pass, first.
	{
		const int W = 8, H = 4;              // 32 pixels, half of them white
		std::vector<unsigned char> Px = Flat(W, H, 128, 128, 128);
		for (int Y = 0; Y < H; ++Y)
		{
			for (int X = 4; X < W; ++X)
			{
				const size_t I = ((size_t)Y * W + X) * 4;
				Px[I] = 255; Px[I + 1] = 255; Px[I + 2] = 255;
			}
		}
		const ExposureStats E = MeasureExposure(Px.data(), W, H);
		Check(E.Measured && E.Pixels == 32, "exposure measured 32 pixels and says so");
		Check(E.ClipHiAll == 16, "sixteen pixels at 255 on all three channels are counted");
		Check(E.ClipHiAny == 16, "and the any-channel count agrees when the clip is white");
		Check(E.ClipLoAll == 0, "nothing is at the bottom of the range in this frame");
		Check(E.Bands[7] == 16 && E.Bands[4] == 16,
		      "the eight luma bands put the white half at the top and the grey half mid");
		long long BandSum = 0;
		for (int I = 0; I < 8; ++I) { BandSum += E.Bands[I]; }
		Check(BandSum == E.Pixels, "the bands account for every pixel, which is their denominator");
		const std::string L = ExposureLine(E);
		std::printf("    %s\n", L.c_str());
		Check(L.find("shotClipHiAll=16/32") != std::string::npos,
		      "the clip count ships with its denominator and never as a mean");
		Check(L.find("shotClipHiAllPct=50.00") != std::string::npos,
		      "and the percentage beside it");
		Check(L.find("shotLumaBandStat=") != std::string::npos,
		      "the line is not truncated: its last key is present");
		Check(ValuesHaveNoSpaces(L), "every exposure value is space-free and carries one equals");
	}
	// ONE CHANNEL AT THE TOP IS STILL CLIPPING, and the two counts are what
	// separate a blown white ground from a saturated sodium lamp.
	{
		const int W = 4, H = 2;
		std::vector<unsigned char> Px = Flat(W, H, 50, 100, 255);
		const ExposureStats E = MeasureExposure(Px.data(), W, H);
		Check(E.ClipHiAny == 8 && E.ClipHiAll == 0,
		      "a red channel at 255 counts as any-clip and not as white-clip");
	}
	// THE CRUSHED END, AND THE COMPLEMENT CLAIM IN ITS OWN RULE STRING
	// CHECKED RATHER THAN ASSERTED: shotClipLoAll is shotPixels minus
	// shotNonBlackPixels, which is what the printed rule says it is.
	{
		const int W = 6, H = 3;
		std::vector<unsigned char> Px = Flat(W, H, 0, 0, 0);
		for (size_t I = 0; I < 4; ++I) { Px[I * 4 + 1] = 9; }
		const ExposureStats E = MeasureExposure(Px.data(), W, H);
		const FrameStats S = Measure(Px.data(), W, H);
		Check(E.ClipLoAll == S.Pixels - S.NonBlack,
		      "the low-clip count equals pixels minus non-black, as its rule string claims");
		Check(E.Bands[0] == 18, "and a near-black frame puts every pixel in the darkest band");
	}
	// AND NOTHING MEASURED SAYS THE WORDS. Eight zeros with denominators
	// would read as a frame that was examined and found clean.
	{
		const std::string L = ExposureLine(MeasureExposure(nullptr, 0, 0));
		Check(L.find("shotClipStatus=NOTHING-MEASURED") != std::string::npos
		      && L.find("shotClipHiAny=") == std::string::npos,
		      "an undecoded frame prints nothing-measured and no clean-looking zeros");
	}

	// ---- QUEUE 059 (a): PER-LIGHT CONTRIBUTION, ACCEPTING CASE FIRST ----
	//
	// The accepting case is a pair that DIFFERS by a known amount in a known
	// place: right half brighter by 51 code values, which is a luma rise of
	// 0.2 exactly. If this instrument cannot see that, no reading it takes of
	// a real lantern means anything.
	{
		const int W = 8, H = 4;
		std::vector<unsigned char> Off = Flat(W, H, 10, 10, 10);
		std::vector<unsigned char> On  = Off;
		for (int Y = 0; Y < H; ++Y)
		{
			for (int X = 4; X < W; ++X)
			{
				const size_t I = ((size_t)Y * W + X) * 4;
				On[I] = 61; On[I + 1] = 61; On[I + 2] = 61;
			}
		}
		const LightDelta D = MeasureLightDelta(On.data(), Off.data(), W, H);
		Check(D.Comparable && D.Pixels == 32, "the pair is comparable and 32 pixels wide");
		Check(Near(D.MaxRise, 51.0 / 255.0), "the largest single-pixel rise is the one planted");
		Check(Near(D.MeanDeltaFull, 0.5 * 51.0 / 255.0),
		      "half the frame rising by 0.2 is a whole-frame mean delta of 0.1");
		Check(D.RoseAtLeast[0] == 16 && D.RoseAtLeast[5] == 16,
		      "all sixteen lit pixels clear every code edge up to 32");
		Check(D.PixelsDarkerWithLightOn == 0,
		      "and no pixel got darker with the light on, so no auto-exposure is suspected");
		Check(D.PeakCol == 4 && D.PeakRow == 0,
		      "the peak region is named as a grid cell and it is in the half that changed");
		Check(Near(D.PeakMeanOn - D.PeakMeanOff, D.PeakMeanDelta),
		      "the peak's two halves are that region's own means, captured where it peaks");
		const std::string L = LightDeltaLine("lantern_02", "lantern", 2, 4, "vign_camB_night",
		                                     "cam_B", "wet_night", "MEASURED", D, "");
		std::printf("    %s\n", L.c_str());
		Check(L.find("peakRegion=c4r0/of8x4") != std::string::npos
		      && L.find("peakRegionPx=x4..5/y0..1") != std::string::npos,
		      "the sample region is named in the line, in cells and in pixels");
		Check(L.find("deltaPixelsOf=32") != std::string::npos,
		      "the histogram ships its denominator");
		Check(L.find("lightDeltaNote=none") != std::string::npos,
		      "the line is not truncated: its last key is present");
		// The two leading tokens are the line's kind and the light's id, as
		// on the shot line; everything after them is key=value.
		const size_t Cut = L.find("kind=");
		Check(Cut != std::string::npos && ValuesHaveNoSpaces(L.substr(Cut)),
		      "every light value is space-free and carries one equals");
	}
	// THE CONTROL: TWO FRAMES OF THE SAME SCENE WITH NOTHING TOGGLED. This is
	// the run's own noise floor and the reason no epsilon had to be invented.
	// A zero here must still print its denominator.
	{
		const int W = 8, H = 4;
		std::vector<unsigned char> A = Flat(W, H, 30, 40, 50);
		const LightDelta D = MeasureLightDelta(A.data(), A.data(), W, H);
		Check(Near(D.MeanDeltaFull, 0.0) && D.RoseAtLeast[0] == 0,
		      "an untouched pair reads zero rise, which is what a control must read");
		const std::string L = LightDeltaLine("control_no_toggle", "control", 0, 0,
		                                     "vign_camB_night", "cam_B", "wet_night",
		                                     "MEASURED", D, "");
		Check(L.find("deltaPixelsRoseAtLeast=0/0/0/0/0/0") != std::string::npos
		      && L.find("deltaPixelsOf=32") != std::string::npos,
		      "the control's zeros ship the count of what was examined");
	}
	// A LIGHT THAT MAKES PIXELS DARKER IS THE AUTO-EXPOSURE TELL, and it is
	// counted rather than clamped away.
	{
		const int W = 4, H = 4;
		std::vector<unsigned char> Off = Flat(W, H, 90, 90, 90);
		std::vector<unsigned char> On  = Flat(W, H, 80, 80, 80);
		const LightDelta D = MeasureLightDelta(On.data(), Off.data(), W, H);
		Check(D.PixelsDarkerWithLightOn == 16 && D.MaxRise == 0.0,
		      "every pixel darker with the light on is counted, and no rise is invented");
	}
	// AND A PAIR THAT IS NOT A PAIR SAYS SO. A missing half is not a light
	// that contributed nothing.
	{
		const LightDelta D = MeasureLightDelta(nullptr, nullptr, 0, 0);
		const std::string L = LightDeltaLine("lantern_01", "lantern", 1, 4, "vign_camA_night",
		                                     "cam_A", "wet_night", "NO-FILE", D,
		                                     "probe-frame-never-arrived");
		Check(!D.Comparable && L.find("lightDelta=NOTHING-MEASURED") != std::string::npos
		      && L.find("lightStatus=NO-FILE") != std::string::npos,
		      "an absent probe frame prints nothing measured and keeps its own reason");
	}
	// ======================================================================
	// QUEUE 326: THE CONTROL IS READ NOW, AND BOTH OUTCOMES ARE WATCHED.
	//
	// THE ACCEPTING CASE IS FIRST AND IT IS THE EXPENSIVE ONE. The costly
	// failure for a floor rule is not that it misses a swamped shot; it is
	// that it refuses every shot and the probe reports NO-READ for ever while
	// the lanterns work. So a QUIET control with a light that genuinely moved
	// the frame must still COUNT, and that is asserted before anything is
	// asserted about rejection.
	// ======================================================================

	// A pair whose right-hand `Lit` pixels rise by `Codes`, everything else
	// flat. One builder for every fixture below, so no two of them can differ
	// in a way nobody meant.
	//
	// (this helper is local to the light-probe block and takes the same BGRA
	// shape as `Flat`, which it is built from)
	{
		const int W = 8, H = 4;                       // 32 pixels
		std::vector<unsigned char> Base = Flat(W, H, 10, 10, 10);

		// ---- ACCEPTING: A QUIET CONTROL STILL COUNTS ITS LIGHTS ---------
		//
		// The control is two takes of the SAME frame, which is what a quiet
		// control looks like: it moved nothing, in either direction.
		const LightDelta Quiet = MeasureLightDelta(Base.data(), Base.data(), W, H);
		Check(Quiet.MovedAtLeast[0] == 0 && Quiet.RoseAtLeast[0] == 0,
		      "a control that toggled nothing moved no pixel in either direction");

		std::vector<unsigned char> LitOn = Base;
		for (int Y = 0; Y < H; ++Y)
		{
			for (int X = 4; X < W; ++X)
			{
				const size_t I = ((size_t)Y * W + X) * 4;
				LitOn[I] = 61; LitOn[I + 1] = 61; LitOn[I + 2] = 61;   // +51 codes
			}
		}
		const LightDelta Real = MeasureLightDelta(LitOn.data(), Base.data(), W, H);
		const LightDelta Dark = MeasureLightDelta(Base.data(), Base.data(), W, H);

		LightFloor F;
		F.ShotId = "vign_camB_night"; F.CameraId = "cam_B"; F.ConditionId = "wet_night";
		LightFloorSetControl(F, Quiet);
		// THE RETURN IS A BUCKET, NOT A YES, AND IT IS NEVER TESTED FOR
		// TRUTH. It was a bool meaning "beat its own floor" and it is now
		// ClassifyLightRead's answer, so `if (Read)` reads the WORST outcome
		// on the list as false: LightReadBlankShot is 0. Held in an int and
		// compared against the named kind at every site below.
		const int ReadReal = LightFloorAddLight(F, "lantern1", "lantern", Real, false);
		const int ReadDark = LightFloorAddLight(F, "lantern2", "lantern", Dark, false);
		Check(ReadReal == LightReadMeasured,
		      "ACCEPTING CASE: a light that lit 16 pixels over a quiet control is MEASURED");
		Check(ReadDark == LightReadVoidControl,
		      "and a light that moved nothing over that same quiet control is certified by "
		      "nothing, which queue 332 files as VOID-CONTROL and not as a failed read");
		Check(LightFloorUsable(F) && F.Read == 1 && F.Lights == 2,
		      "so the shot has a usable floor and counts 1 of its 2 lights");
		const std::string FL = LightFloorLine(F);
		std::printf("    %s\n", FL.c_str());
		Check(FL.find("lightFloorVerdict=FLOOR-USABLE") != std::string::npos
		      && FL.find("lightsReadThisShot=1/1") != std::string::npos,
		      "the per-shot line says FLOOR-USABLE and carries that shot's own count, over "
		      "the lights this shot MEASURED and not over all 2 it probed: the second one "
		      "was screened out by its own control and never got as far as the floor");
		Check(FL.find("lightFloorBest=lantern1/at32codes") != std::string::npos
		      && FL.find("lightFloorBestPx=16..vs..0") != std::string::npos,
		      "and the winning pair is one entry at one edge, both counts together");
		Check(FL.find("lightFloorCtrlMovedAtLeast=0/0/0/0/0/0") != std::string::npos
		      && FL.find("lightFloorCtrlPxOf=32") != std::string::npos,
		      "the control's zeros ship the count of what was examined");
		Check(ValuesHaveNoSpaces(FL.substr(FL.find("shot="))),
		      "every value on the floor line is space-free");
		const std::string SegYes = LightFloorSegment(F, Real, false, ReadReal);
		const std::string SegNo  = LightFloorSegment(F, Dark, false, ReadDark);
		Check(SegYes.find("lightAboveFloor=YES") != std::string::npos
		      && SegYes.find("lightVsFloorPx=16..vs..0") != std::string::npos,
		      "the light's own line says YES and carries both counts at the deciding edge");
		// AND THE LIGHT THAT DID NOT CLEAR THE FLOOR NO LONGER GETS A WORD
		// AT ALL. It printed `NO` with a `0..vs..0` pair, which is a light
		// that was weighed; queue 332 screens it out one step earlier, as a
		// rise its own control cannot certify, and the segment says which
		// screen bit. `NO` is reserved for a MEASURED light that lost at
		// every edge, and no fixture in this file reaches that branch: with a
		// control that moved nothing, any measured light has risen pixels the
		// control does not, so it always wins. That gap is unfilled here and
		// named so rather than papered over with an assertion that passes.
		Check(SegNo.find("lightAboveFloor=nothing-measured/VOID-CONTROL") != std::string::npos
		      && SegNo.find("lightVsFloorPx=nothing-measured") != std::string::npos,
		      "and a light its own control cannot certify says which screen bit, rather "
		      "than a verdict on a comparison nobody was entitled to make");
		Check(SegNo.find("lightAboveFloor=NO") == std::string::npos,
		      "GUARD FIRES: the word that run 48 printed for seven lights whose OFF frame "
		      "was simply brighter is absent, not merely outranked");
		Check(LightFloorSegment(F, Quiet, true, LightReadMeasured)
		          .find("lightAboveFloor=IS-THE-FLOOR")
		      != std::string::npos,
		      "the control is not measured against itself and does not print a failed light");

		// THE RUN LINE OVER THAT ONE SHOT, which is the accepting case for
		// the done line: a quiet control must produce a COUNT, not NO-READ.
		std::vector<LightFloor> Good; Good.push_back(F);
		const std::string RG = LightProbeDoneLine(2, 2, Good, 0, 0, 0, 0, 1, 11, 240.0, 4.0, 32, 1);
		std::printf("    %s\n", RG.c_str());
		Check(RG.find("lightsAboveFloor=1/1") != std::string::npos
		      && RG.find("lightFloorShotsUsable=1/1") != std::string::npos
		      && RG.find("lightsMeasured=1/2") != std::string::npos
		      && RG.find("lightsNothingMeasuredVoidControl=1/2") != std::string::npos,
		      "ACCEPTING CASE ON THE DONE LINE: a quiet control still counts, and the "
		      "zero ships its denominator");
		// THE TWO COARSE KEYS WENT WITH THE SIX BUCKETS AND THEIR ABSENCE IS
		// ASSERTED, not assumed: they cut the same lights a second way, and
		// two partitions of one variable under two key families is one number
		// printed twice on a line a grep reads as two.
		Check(RG.find("lightsInNoReadShots=") == std::string::npos
		      && RG.find("lightsInNoControlShots=") == std::string::npos,
		      "and the two coarse light keys queue 332 removed are absent from the "
		      "accepting done line");
		Check(ValuesHaveNoSpaces(RG), "every light-pass value is space-free");
		// THE OLD KEY IS GONE AND ITS ABSENCE IS ASSERTED, not assumed. The
		// ruling of 2026-09-16 renamed it because its rule AND its denominator
		// changed, and the evidence channel is one committed path with a git
		// history: a key-grep over it plots every run under one name, so a
		// surviving `lightsReachedFrame=` anywhere on a done line would put
		// run 47's count and this one on one axis. No tombstone key either,
		// because `lightProbeStatus` on the same line already says whether the
		// pass ran. Checked on every done line this file builds, below.
		Check(RG.find("lightsReachedFrame=") == std::string::npos,
		      "RENAMED: the old key is absent from the accepting done line");
		Check(RG.find("lightsAboveFloorStat=whole-run/count-of-MEASURED-lights-that-beat-their-"
		              "OWN-shots-control-at-some-code-edge/denominator-is-the-lights-MEASURED-in-"
		              "shots-with-a-usable-floor-and-NOT-every-light-they-probed/"
		              "RENAMED-BY-QUEUE-326-from-lightsReachedFrame-which-counted-one-pixel-"
		              "rising-by-one-code-value-through-run-47-and-is-not-comparable/"
		              "RE-DENOMINATED-BY-QUEUE-332-on-2026-09-16-so-runs-before-that-are-not-"
		              "comparable-either") != std::string::npos,
		      "and the stat token names what the number is a statistic OF, what its "
		      "denominator counts, and BOTH of the two changes that make an older run "
		      "incomparable, as one space-free value a reader gets whole from the line "
		      "they greped");

		// ---- REJECTING: A CONTROL THAT EXCEEDS EVERY LIGHT --------------
		//
		// PLANTED AT THE SHAPE RUN 47 REPORTED, vign_camA_night: a control
		// that toggled nothing and moved the WHOLE frame, beside a light that
		// moved a corner of it, beside a light whose histogram equals the
		// control's to the pixel (four of that shot's seven lanterns read the
		// control's 0.25060 to five decimals). None of the three is a reading.
		std::vector<unsigned char> Swamped = Flat(W, H, 74, 74, 74);   // +64 codes, all 32 px
		const LightDelta Loud = MeasureLightDelta(Swamped.data(), Base.data(), W, H);
		Check(Loud.MovedAtLeast[5] == 32 && Loud.MeanDeltaFull > 0.2,
		      "the planted control moved every pixel past every code edge");

		std::vector<unsigned char> Corner = Base;
		for (int X = 0; X < 4; ++X)
		{
			const size_t I = ((size_t)0 * W + X) * 4;
			Corner[I] = 61; Corner[I + 1] = 61; Corner[I + 2] = 61;
		}
		const LightDelta Small = MeasureLightDelta(Corner.data(), Base.data(), W, H);
		const LightDelta Same  = MeasureLightDelta(Swamped.data(), Base.data(), W, H);

		LightFloor N;
		N.ShotId = "vign_camA_night"; N.CameraId = "cam_A"; N.ConditionId = "wet_night";
		LightFloorSetControl(N, Loud);
		Check(LightFloorAddLight(N, "lantern0", "lantern", Small, false) == LightReadVoidControl,
		      "REJECTING CASE: a light smaller than its own control is not a reading");
		Check(LightFloorAddLight(N, "lantern1", "lantern", Same, false) == LightReadVoidControl,
		      "and a light that equals the control to the pixel is not one either: a tie "
		      "is not a surplus and no epsilon was invented to make it one");
		Check(!LightFloorUsable(N) && N.Read == 0 && N.Lights == 2,
		      "so the shot has no usable floor at all");
		const std::string NL = LightFloorLine(N);
		std::printf("    %s\n", NL.c_str());
		Check(NL.find("lightFloorVerdict=NOT-USABLE") != std::string::npos,
		      "the per-shot line says NOT-USABLE rather than printing a count of zero: this "
		      "control certified no light at all, which is a weaker claim than NO-READ's "
		      "and queue 332 gave it its own word");
		Check(NL.find("lightsReadThisShot=nothing-measured/0-of-2-lights-in-this-shot-were-"
		              "measurable") != std::string::npos
		      && NL.find("lightFloorBest=nothing-measured/no-MEASURED-light-in-this-shot")
		         != std::string::npos
		      && NL.find("lightFloorCtrlMeanFull=+0.25098") != std::string::npos,
		      "and it carries the control's own whole-frame movement beside the words, "
		      "never a closest-light pair: 32..vs..32 named a nearest miss among lights "
		      "this control was never entitled to weigh");
		Check(ValuesHaveNoSpaces(NL.substr(NL.find("shot="))),
		      "the NO-READ line is space-free too");

		// ---- THE HOLE THE PRINTED SERIES FOUND --------------------------
		//
		// RUN 47's pinset_night_2 CONTROL HAS RoseAtLeast=0/0/0/0/0/0 AND A
		// MEAN OF -0.37873, every one of its 921600 pixels DARKER. Floored on
		// rises alone it reads as a pristine zero, and its lantern3 at 56
		// risen pixels would have been counted as a read. The floor is
		// measured on absolute movement for exactly this frame, and the
		// fixture below is that frame's shape at 32 pixels.
		std::vector<unsigned char> FellOff = Flat(W, H, 106, 106, 106);
		const LightDelta AllDarker = MeasureLightDelta(Base.data(), FellOff.data(), W, H);
		Check(AllDarker.RoseAtLeast[0] == 0 && AllDarker.MovedAtLeast[5] == 32
		      && AllDarker.MeanDeltaFull < -0.37,
		      "a control that only DARKENS has an empty rise histogram and a full moved one");
		std::vector<unsigned char> OnePx = Base;
		OnePx[0] = 11; OnePx[1] = 11; OnePx[2] = 11;            // one pixel, one code
		const LightDelta Faint = MeasureLightDelta(OnePx.data(), Base.data(), W, H);
		Check(Faint.RoseAtLeast[0] == 1, "and the planted light did rise, by one code value");
		LightFloor S;
		S.ShotId = "pinset_night_2"; S.CameraId = "cam_A"; S.ConditionId = "pin_setter_night";
		LightFloorSetControl(S, AllDarker);
		Check(LightFloorAddLight(S, "lantern3", "lantern", Faint, false) == LightReadVoidControl,
		      "GUARD FIRES: a one-pixel rise under a control that dragged the whole frame "
		      "down is NOT a read, which a rise-only floor would have called one");

		// ---- THE THIRD OUTCOME: A SHOT WITH NO CONTROL AT ALL -----------
		//
		// NOT NO-READ, AND THE DIFFERENCE IS THE WHOLE POINT. NO-READ means
		// this shot's control swamped its lights; NO-CONTROL means there was
		// never a floor to read against, which is what the live rig produces
		// when the reference frame does not decode (the .cpp emits the control
		// line with NO-REFERENCE and pushes the floor anyway) or when the
		// control's own probe frame never arrives. Both print branches below
		// existed and NOTHING RAN THEM: an unrun formatter printing a
		// plausible string is the silent-instrument failure this header's own
		// preamble is about, so the branch that was argued is now photographed.
		LightFloor NC;
		NC.ShotId = "pinset_night_5"; NC.CameraId = "cam_A";
		NC.ConditionId = "pin_setter_night";
		const LightDelta NoPair = LightDelta();   // never measured: Comparable is false
		LightFloorSetControl(NC, NoPair);
		Check(!NC.bHaveControl,
		      "a control whose frame never decoded leaves the shot with no floor");
		const int ReadNoCtrl = LightFloorAddLight(NC, "lantern1", "lantern", Real, false);
		Check(ReadNoCtrl == LightReadBlankShot,
		      "a light that DID measure cannot read above a floor that does not exist");
		Check(LightFloorAddLight(NC, "lantern2", "lantern", NoPair, false) == LightReadBlankShot,
		      "and neither can a light that did not measure either");
		Check(NC.Lights == 2 && NC.Read == 0,
		      "both are still counted as lights this shot examined, so the denominator "
		      "describes the set that was walked and not the set that worked");
		const std::string NCL = LightFloorLine(NC);
		std::printf("    %s\n", NCL.c_str());
		Check(NCL.find("lightFloorVerdict=NO-CONTROL") != std::string::npos,
		      "PLANTED BRANCH: the floor line says NO-CONTROL and not NO-READ");
		Check(NCL.find("lightsReadThisShot=nothing-measured/2") != std::string::npos,
		      "and its count is the words with the denominator beside them, never 0/2, "
		      "which would read as two lights that failed a floor there never was");
		Check(NCL.find("lightFloorCtrl=nothing-measured/no-comparable-control-frame-for-this-shot")
		      != std::string::npos,
		      "and the line names WHY there is no floor rather than leaving the key out");
		Check(ValuesHaveNoSpaces(NCL.substr(NCL.find("shot="))),
		      "every value on the NO-CONTROL floor line is space-free");

		// THE TWO no-comparable WORDS ON THE LIGHT'S OWN SEGMENT, both sides
		// of the same `if`: no control for this SHOT, and no delta for this
		// LIGHT under a control that worked. Neither had a fixture.
		const std::string SegNoCtrl = LightFloorSegment(NC, Real, false, ReadNoCtrl);
		Check(SegNoCtrl.find("lightAboveFloor=nothing-measured/BLANK-SHOT") != std::string::npos,
		      "PLANTED BRANCH: a light in a shot with no control prints the words and the "
		      "bucket it was filed under, which is the same word its lightStatus carries "
		      "and the same one the run line counts it in");
		// NO-PAIR IS THIS LIGHT'S OWN BUCKET AND IT IS HANDED IN, NOT
		// RE-DERIVED: this light WAS photographed under a control that
		// worked, and its pair is the thing that is not comparable. The other
		// two values the parameter takes would both be a different fact: -1
		// says the light was never photographed at all, and BLANK-SHOT says
		// the shot lost its own reference.
		const std::string SegNoDelta = LightFloorSegment(F, NoPair, false, LightReadNoPair);
		Check(SegNoDelta.find("lightAboveFloor=nothing-measured/NO-PAIR") != std::string::npos,
		      "PLANTED BRANCH: and a light that did not measure, under a control that did, "
		      "names the other half under its own bucket word");

		// THE CONTROL LINE OF A SHOT WHOSE CONTROL MEASURED NOTHING. It used
		// to print IS-THE-FLOOR, which is a floor claimed by a line whose own
		// lightDelta says NOTHING-MEASURED. Reachable today: EmitLightLine
		// passes Seq = -1 for a NO-REFERENCE shot.
		// -1 IS THE LIVE RIG'S OWN VALUE HERE. EmitLightLine defaults Read to
		// -1 and the control paths that reach this branch (NO-FILE,
		// UNDECODABLE, NOT-COMPARABLE) all take that default; the bIsControl
		// branch returns before reading it either way.
		const std::string SegCtrlDead = LightFloorSegment(NC, NoPair, true, -1);
		Check(SegCtrlDead.find("lightAboveFloor=nothing-measured/the-control-did-not-measure-so-"
		                       "this-shot-has-no-floor") != std::string::npos
		      && SegCtrlDead.find("lightAboveFloorEdge=nothing-measured") != std::string::npos
		      && SegCtrlDead.find("lightVsFloorPx=nothing-measured") != std::string::npos,
		      "GUARD FIRES: a control that never measured is not the floor, and the line "
		      "says so on all three keys instead of claiming IS-THE-FLOOR");
		Check(SegCtrlDead.find("IS-THE-FLOOR") == std::string::npos,
		      "and the word that was wrong is absent, not merely outranked");
		const std::string SegCtrlLive = LightFloorSegment(F, Quiet, true, LightReadMeasured);
		Check(SegCtrlLive.find("lightAboveFloor=IS-THE-FLOOR") != std::string::npos
		      && SegCtrlLive.find("nothing-measured") == std::string::npos,
		      "ACCEPTING CASE FOR THAT GUARD: a control that DID measure still reads "
		      "IS-THE-FLOOR with no nothing-measured word anywhere on it, so the refusal "
		      "is not a ratchet that eats every control");

		// THE RUN LINE OVER THAT SHOT ALONE: the third shot count and the
		// third light count, each with the denominator it was taken over.
		std::vector<LightFloor> NoCtrlRun; NoCtrlRun.push_back(NC);
		const std::string NCD = LightProbeDoneLine(2, 2, NoCtrlRun, 0, 0, 1, 0, 1, 11,
		                                           240.0, 3.0, 32, 1);
		std::printf("    %s\n", NCD.c_str());
		Check(NCD.find("lightFloorShotsNoControl=1/1") != std::string::npos
		      && NCD.find("lightsNothingMeasuredBlankShot=2/2") != std::string::npos
		      && NCD.find("lightsInNoControlShots=") == std::string::npos,
		      "the done line counts a NO-CONTROL shot and its lights on their OWN keys, "
		      "so no shot is folded under a word that says its control swamped it, and "
		      "the coarse key that used to hold them is gone rather than duplicated");
		Check(NCD.find("lightFloorShotsNoRead=0/1") != std::string::npos,
		      "and NO-READ's own count is a zero with its denominator, not silence");
		Check(NCD.find("lightsReachedFrame=") == std::string::npos,
		      "RENAMED: the old key is absent from the NO-CONTROL done line");
		Check(ValuesHaveNoSpaces(NCD), "every value on the NO-CONTROL run line is space-free");

		// ---- AND A PASS WITH NO FLOOR AT ALL ----------------------------
		std::vector<LightFloor> None;
		const std::string L = LightProbeDoneLine(0, 7, None, 0, 0, 0, 0, 0, 2, 90.0, 0.0, 32, 0);
		std::printf("    %s\n", L.c_str());
		Check(L.find("lightProbeStatus=NOTHING-MEASURED") != std::string::npos
		      && L.find("lightsAboveFloor=nothing-measured/") != std::string::npos
		      && L.find("lightFloorWorstShot=nothing-measured") != std::string::npos,
		      "a light pass that probed nothing says the words rather than printing 0/0");
		Check(L.find("lightsAboveFloor=0/0") == std::string::npos,
		      "and it may not read as a clean zero over a set it never examined");
		Check(L.find("lightsReachedFrame=") == std::string::npos,
		      "RENAMED: the old key is absent from the nothing-measured done line");

		// A RUN WITH FLOORS BUT NO USABLE ONE IS THE OTHER 0/0. Floors were
		// pushed, lights were probed, and not one shot had a floor to read
		// from: the numerator is zero and so is the denominator, and `0/0`
		// there cannot be told from a run whose lights all lost to a floor
		// that worked. The rejecting floor N alone is that run.
		std::vector<LightFloor> NoneUsable; NoneUsable.push_back(N);
		const std::string NUD = LightProbeDoneLine(2, 2, NoneUsable, 0, 0, 0, 0, 1, 11,
		                                           240.0, 8.0, 32, 1);
		std::printf("    %s\n", NUD.c_str());
		Check(NUD.find("lightsAboveFloor=nothing-measured/no-usable-floor-in-any-of-1-shots")
		      != std::string::npos,
		      "GUARD FIRES: with floors present and none usable the count is the words "
		      "and the shot count, never 0/0");
		Check(NUD.find("lightsAboveFloor=0/0") == std::string::npos,
		      "and the zero over a zero it would have printed is absent");
		Check(NUD.find("lightFloorShotsNotUsable=1/1") != std::string::npos
		      && NUD.find("lightFloorShotsNoRead=0/1") != std::string::npos
		      && NUD.find("lightsNothingMeasuredVoidControl=2/2") != std::string::npos,
		      "while the shot that DID have a control is still counted, as NOT-USABLE and "
		      "not as NO-READ, which is the fact the words above do not carry: its control "
		      "certified nothing rather than beating something");
		Check(NUD.find("lightsReachedFrame=") == std::string::npos,
		      "RENAMED: the old key is absent from the no-usable-floor done line");
		Check(ValuesHaveNoSpaces(NUD), "every value on the no-usable-floor line is space-free");

		// ---- THE RUN LINE OVER A MIXED RUN, which is run 47's shape -----
		std::vector<LightFloor> Mixed;
		Mixed.push_back(F); Mixed.push_back(N); Mixed.push_back(S);
		// PROBED = 5 AND ELIGIBLE = 6, WHICH IS THIS FIXTURE'S OWN ARITHMETIC.
		// It said 6 and 7, over three floors holding 2 + 2 + 1 = 5 lights, and
		// nothing checked it: the suite was green over a fixture that claims
		// run 47's shape and breaks the identity the whole line rests on. The
		// three floors hold five probed lights; one more light was skipped by
		// the budget, which makes six ELIGIBLE and five probed. The identity is
		// U + N + K = P, with U the denominator of lightsAboveFloor, N the
		// numerator of lightsInNoReadShots and K of lightsInNoControlShots,
		// and all four numbers are asserted below on this one line so a reader
		// can check it without holding two fixtures in their head.
		const std::string M = LightProbeDoneLine(5, 6, Mixed, 1, 1, 0, 0, 3, 11,
		                                         240.0, 61.5, 32, 3);
		std::printf("    %s\n", M.c_str());
		Check(M.find("lightProbeStatus=PARTIAL-BUDGET-BIT") != std::string::npos
		      && M.find("lightsSkippedBudget=1") != std::string::npos,
		      "a budget that bit announces itself with the count it cost");
		Check(M.find("lightFloorShotsUsable=1/3") != std::string::npos
		      && M.find("lightFloorShotsNotUsable=2/3") != std::string::npos
		      && M.find("lightFloorShotsNoRead=0/3") != std::string::npos
		      && M.find("lightFloorShotsNoControl=0/3") != std::string::npos,
		      "the done line separates shots with a usable floor from shots whose control "
		      "certified nothing, from shots whose lights all lost to a floor that worked, "
		      "and from shots that had no control, with all four counts over the same "
		      "denominator, and the four sum to the floors");
		Check(M.find("lightsProbed=5/6") != std::string::npos
		      && M.find("lightsAboveFloor=1/1") != std::string::npos
		      && M.find("lightsMeasured=1/5") != std::string::npos
		      && M.find("lightsNothingMeasuredVoidControl=4/5") != std::string::npos,
		      "and the numbers the accounting identity is read from are all on this one "
		      "line: 5 lights probed, 1 measured, 4 certified by nothing, and the one that "
		      "was measured beat its own floor");
		Check(M.find("lightsReachedFrame=") == std::string::npos,
		      "RENAMED: the old key is absent from the mixed done line");
		Check(M.find("lightFloorWorstShot=pinset_night_2") != std::string::npos
		      && M.find("lightFloorWorstCtrlMeanFull=-0.37647") != std::string::npos
		      && M.find("lightFloorBestLightMeanFullAtWorst=nothing-measured")
		         != std::string::npos,
		      "the worst floor and the best light UNDER IT are one pair from one shot, "
		      "named AtWorst, never the run's best light from somewhere else: the worst "
		      "shot here measured no light at all, so the half that would be the light "
		      "says so instead of reporting +0.00012 from a comparison that was void");
		Check(ValuesHaveNoSpaces(M), "every value on the mixed run line is space-free");

		// ---- THE EXPOSURE THE PAIR WAS PHOTOGRAPHED UNDER ---------------
		//
		// RUN 47's REAL VALUES: every probed shot ran AUTO reading back
		// 0.0300/8.0000, and the light lines carried no exposure key at all.
		LightPin P; P.Word = "AUTO"; P.bRead = true; P.ReadMin = 0.03; P.ReadMax = 8.0;
		const std::string PS = LightPinSegment(P);
		Check(PS.find("lightExposurePin=AUTO") != std::string::npos
		      && PS.find("lightExposurePinRead=0.0300/8.0000") != std::string::npos,
		      "the light line carries the pin word and the clamp range it was taken under");
		Check(LightPinSegment(LightPin()).find("lightExposurePinRead=nothing-measured/")
		      != std::string::npos,
		      "and a shot whose camera answered nothing prints the words, not 0.0000/0.0000");
		Check(ValuesHaveNoSpaces(PS), "the pin segment is space-free");

		// ---- THE LENGTH SERIES THESE BUFFERS ARE SIZED FROM -------------
		//
		// QUEUE 310: snprintf truncates in silence and a cut line reads as a
		// short one. The longest light line in the committed run 47 verdict
		// is 704 characters; the numbers below are what this build emits for
		// the same family, printed on every run so the next person to add a
		// key reads a series rather than guessing.
		// THE SIZES ARE MEASURED AT THE REAL FRAME'S WIDTH, not at the 32
		// pixels of the fixtures above: every count on these lines is six
		// digits at 1280x720 and two at 8x4, which is sixty characters of
		// difference across one line. The numbers below ARE run 47's, read
		// off the committed verdict for control_no_toggle at vign_camA_night,
		// so the buffer is sized against the longest line this has ever had
		// to print rather than against the shortest one a test can build.
		LightDelta R47;
		R47.Comparable = true; R47.Width = 1280; R47.Height = 720; R47.Pixels = 921600;
		R47.MeanOnFull = 0.25136; R47.MeanOffFull = 0.00075; R47.MeanDeltaFull = 0.25060;
		R47.MaxRise = 0.91607; R47.MaxDrop = 0.0;
		R47.PixelsDarkerWithLightOn = 332097;
		R47.Cols = 8; R47.Rows = 4; R47.PeakCol = 2; R47.PeakRow = 0;
		R47.PeakX0 = 320; R47.PeakX1 = 480; R47.PeakY0 = 0; R47.PeakY1 = 180;
		R47.PeakMeanDelta = 0.86557; R47.PeakMeanOn = 0.87298; R47.PeakMeanOff = 0.00741;
		const long long R47Hist[6] = {921600, 921315, 917618, 898971, 802512, 597624};
		for (int E = 0; E < LightDelta::Edges; ++E)
		{
			R47.RoseAtLeast[E] = R47Hist[E]; R47.MovedAtLeast[E] = R47Hist[E];
		}
		LightFloor R47F;
		R47F.ShotId = "vign_camA_night"; R47F.CameraId = "cam_A";
		R47F.ConditionId = "wet_night";
		LightFloorSetControl(R47F, R47);
		// KIND IS `practical` HERE, THE SAME WORD THE LIGHT LINE BELOW
		// PRINTS FOR THIS ID, so the lantern split on the done line and the
		// kind on the light line are one fact and not two.
		const int ReadR47 = LightFloorAddLight(R47F, "east_parade_interior5", "practical",
		                                       R47, false);
		const std::string FullLine =
			LightDeltaLine("east_parade_interior5", "practical", 8, 8, "vign_camA_night",
			               "cam_A", "wet_night", "MEASURED", R47, "")
			+ " " + LightFloorSegment(R47F, R47, false, ReadR47) + " " + LightPinSegment(P);
		const std::string R47L = LightFloorLine(R47F);
		const std::string R47D = LightProbeDoneLine(42, 42, Mixed, 0, 0, 0, 0, 6, 43,
		                                            240.0, 12.5, 32, 6);
		// EACH LENGTH AGAINST ITS OWN BUFFER, because the assembled line is
		// three buffers and a single total tells a reader nothing about which
		// one is close to biting.
		const std::string R47Delta =
			LightDeltaLine("east_parade_interior5", "practical", 8, 8, "vign_camA_night",
			               "cam_A", "wet_night", "MEASURED", R47, "");
		// EACH LENGTH IS PRINTED AGAINST THE BUFFER IT IS ACTUALLY WRITTEN
		// INTO, read off the declarations in FrameStats.h (Head[420]+Body[1400],
		// Head[320]+Buf[1700], Buf[2600], Buf[820], Buf[420]). Three of these
		// five denominators had gone stale: `doneLineChars=2238/of1500` names a
		// buffer that was raised to 2600, and a length printed over a
		// denominator smaller than itself reads as a truncation that did not
		// happen. The numerators below are what this build prints; no bound is
		// set from them here.
		std::printf("    atRealFrameWidth: deltaLineChars=%d/head420+body1400 "
		            "floorLineChars=%d/head320+body1700 doneLineChars=%d/of2600 "
		            "floorSegChars=%d/of820 pinSegChars=%d/of420 assembledChars=%d\n",
		            (int)R47Delta.size(), (int)R47L.size(), (int)R47D.size(),
		            (int)LightFloorSegment(R47F, R47, false, ReadR47).size(), (int)PS.size(),
		            (int)FullLine.size());
		std::printf("    atFixtureWidth:   deltaLineChars=%d floorLineChars=%d "
		            "doneLineChars=%d\n",
		            (int)(LightDeltaLine("l", "lantern", 1, 8, "s", "c", "w", "MEASURED",
		                                 Real, "").size()),
		            (int)NL.size(), (int)M.size());
		Check(FullLine.find("lightExposurePinStat=") != std::string::npos
		      && FullLine.find("lightLineCut=") == std::string::npos,
		      "at run 47's own numbers the assembled light line reaches its last key "
		      "and no buffer bit");
		Check(R47D.find("lightProbeDoneLineCut=") == std::string::npos
		      && R47L.find("lightFloorLineCut=") == std::string::npos
		      && M.find("lightProbeDoneLineCut=") == std::string::npos
		      && NL.find("lightFloorLineCut=") == std::string::npos,
		      "and neither the done line nor the floor line was truncated, at either width");
		// AND THE CUT MARKER ITSELF IS WATCHED FROM BOTH SIDES: a truncation
		// announcer nothing has ever seen fire is a comment. This plants a
		// shot id long enough to overrun the floor line's buffer.
		LightFloor Long = R47F;
		Long.ShotId = std::string(900, 'x');
		const std::string Cut = LightFloorLine(Long);
		Check(Cut.find("lightFloorLineCut=yes/at-320-chars-of-head") != std::string::npos,
		      "GUARD FIRES: a floor line that overran its buffer says so rather than "
		      "ending mid-key and reading as a missing measurement");
		LightFloor LongBest = R47F;
		LongBest.BestId = std::string(600, 'y');
		// bHaveBest IS PLANTED, NOT ASSUMED. Since queue 332 only a MEASURED
		// light sets it, and R47F's one light is screened out by its own
		// control, so the 600-character id would never reach the body buffer
		// and the cap under test would never bite. A guard that cannot fire is
		// a comment: the condition is planted here, and the bound is untouched.
		LongBest.bHaveBest = true;
		Check(LightFloorLine(LongBest).find("lightFloorLineCut=yes/at-1700-chars-of-body")
		      != std::string::npos,
		      "and the body's own cap announces itself separately from the head's");
		// AND THE DONE LINE'S OWN ANNOUNCER, WHICH COULD NOT FIRE BEFORE.
		// The worst-shot segment used to be built in two fixed buffers, a
		// 300-byte one carrying an unbounded SHOT id and a 40-byte one
		// carrying an unbounded LIGHT id, so an overlong id was cut to fit
		// BEFORE the 1500-character line ever saw it and the line's announcer
		// stayed silent over a truncation that had already happened. Both ids
		// ride a std::string now and this is the shot id that proves the one
		// remaining cap announces.
		LightFloor LongWorst = R47F;
		LongWorst.ShotId = std::string(900, 'z');
		std::vector<LightFloor> LongRun; LongRun.push_back(LongWorst);
		const std::string CutD = LightProbeDoneLine(1, 1, LongRun, 0, 0, 0, 0, 1, 43,
		                                            240.0, 12.5, 32, 1);
		Check(CutD.find("lightProbeDoneLineCut=yes/at-2600-chars") != std::string::npos,
		      "GUARD FIRES: a done line whose worst shot's id overran the buffer says so, "
		      "which a pre-cap on that id would have made impossible");
		Check(CutD.find(std::string(300, 'z')) != std::string::npos,
		      "and the id reached the line's own buffer rather than being cut to fit a "
		      "300-byte one on the way in");
		Check(R47D.find("lightsReachedFrame=") == std::string::npos
		      && CutD.find("lightsReachedFrame=") == std::string::npos,
		      "RENAMED: the old key is absent from the run-47-width done line and from the "
		      "truncated one, which is every done line this file builds");
	}

	// ---- QUEUE 186: THE SKY BANDS, ACCEPTING CASE FIRST ------------------
	//
	// THE ACCEPTING FIXTURE IS A FRAME SHAPED LIKE THE ONE THIS SHIPS FOR: a
	// pale sky over a darker ground, with the sky's channel order B>G>R the
	// way an overcast British sky reads and the way the day fog colour this
	// replaces also read. If MeasureBand cannot report that correctly it is
	// worth nothing, so it is checked before any refusal is.
	{
		const int W = 80, H = 80;
		std::vector<unsigned char> Px((size_t)W * H * 4, 255);
		for (int Y = 0; Y < H; ++Y)
		{
			for (int X = 0; X < W; ++X)
			{
				const long long P = (long long)Y * W + X;
				// Top quarter pale and cool, the rest mid grey.
				const bool bSky = (Y < H / 4);
				Px[P * 4]     = bSky ? 210 : 90;   // B
				Px[P * 4 + 1] = bSky ? 200 : 90;   // G
				Px[P * 4 + 2] = bSky ? 190 : 90;   // R
				Px[P * 4 + 3] = 255;
			}
		}
		const BandStats Sky = MeasureBand(Px.data(), W, H, "skyTop",
		                                  0.0, 0.0, 1.0, SkyTopY1());
		Check(Sky.Measured && Sky.Pixels == (long long)(W * (int)(SkyTopY1() * H)),
		      "the sky band measures exactly the pixels its own rectangle covers");
		Check(Near(Sky.MeanR, 190.0) && Near(Sky.MeanG, 200.0) && Near(Sky.MeanB, 210.0),
		      "the channel means come back in order, which is what tells a sky from a fog colour");
		Check(Near(Sky.MeanLuma, Luma(190, 200, 210)) && Near(Sky.P50, Sky.MeanLuma),
		      "a flat band's mean and median agree and match the shared luma weights");
		Check(Sky.ClipHiAny == 0,
		      "an unclipped pale band counts zero clipped pixels over its own denominator");
		const BandStats Ground = MeasureBand(Px.data(), W, H, "ground",
		                                     0.0, GroundY0(), 1.0, 1.0);
		Check(Ground.Measured && Near(Ground.MeanLuma, Luma(90, 90, 90)),
		      "the ground band reads the darker half and not the sky above it");
		const BandStats Centre = MeasureBand(Px.data(), W, H, "skyCentre",
		                                     SkyCentreX0(), 0.0, SkyCentreX1(), SkyTopY1());
		const std::string L = SkyBandLine(Sky, Centre, Ground);
		std::printf("    %s\n", L.c_str());
		Check(L.find("band.skyTop=MEASURED") != std::string::npos
		      && L.find("band.skyCentre=MEASURED") != std::string::npos
		      && L.find("band.ground=MEASURED") != std::string::npos,
		      "all three bands print their own name and their own status");
		Check(ValuesHaveNoSpaces(L), "every sky-band value is space-free");
		// THE RATIO IS GROUND OVER SKY AND NOT THE OTHER WAY UP, checked
		// against the arithmetic rather than against a remembered direction.
		char Want[64];
		std::snprintf(Want, sizeof(Want), "bandGroundOverSky=%.4f",
		              Luma(90, 90, 90) / Luma(190, 200, 210));
		Check(L.find(Want) != std::string::npos,
		      "the ratio is the ground band over the sky centre band");
	}
	{
		// ---- A2: THE ROBUST RATIO AND THE RANK KEY, ON A PLANTED FRAME ---
		//
		// ACCEPTING CASE FIRST, AND THE COUNTS ARE ARITHMETIC RATHER THAN A
		// REMEMBERED ANSWER. The ground band of this 80x80 frame is rows 64
		// to 79, 1280 pixels, planted in four populations:
		//   rows 64..70, 560 px, mid grey 90   strictly BELOW the sky median
		//   10 of those  replaced by pure black, which are the LO RAIL
		//   row 71,       80 px, the sky colour EXACTLY, which are the TIES
		//   rows 72..79, 640 px, 240 grey      strictly ABOVE, 5 of them white
		// so the rank key must read 560/1280 = 43.7500 per cent with 80 ties,
		// 10 on the lo rail and 5 on the hi rail. A tie is outside the count
		// because the comparison is strict, and that is why it is printed.
		const int W = 80, H = 80;
		std::vector<unsigned char> Px((size_t)W * H * 4, 255);
		for (int Y = 0; Y < H; ++Y)
		{
			for (int X = 0; X < W; ++X)
			{
				const long long P = (long long)Y * W + X;
				unsigned char B = 90, G = 90, R = 90;
				if (Y < H / 4) { B = 210; G = 200; R = 190; }      // the sky
				else if (Y >= 64 && Y <= 70)
				{
					if (Y == 64 && X < 10) { B = 0; G = 0; R = 0; } // the lo rail
				}
				else if (Y == 71) { B = 210; G = 200; R = 190; }    // the ties
				else if (Y >= 72)
				{
					B = 240; G = 240; R = 240;
					if (Y == 79 && X < 5) { B = 255; G = 255; R = 255; } // the hi rail
				}
				Px[P * 4] = B; Px[P * 4 + 1] = G; Px[P * 4 + 2] = R; Px[P * 4 + 3] = 255;
			}
		}
		const BandStats Centre = MeasureBand(Px.data(), W, H, "skyCentre",
		                                     SkyCentreX0(), 0.0, SkyCentreX1(), SkyTopY1());
		const BandStats Ground = MeasureBand(Px.data(), W, H, "ground",
		                                     0.0, GroundY0(), 1.0, 1.0);
		Check(Ground.Pixels == 1280 && Ground.RailLo == 10 && Ground.ClipHiAny == 5,
		      "the ground band counts its own pixels and both rails over that denominator");
		Check(Near(Centre.P50, Luma(190, 200, 210)),
		      "the threshold is the skyCentre band's own median pixel and this frame's sky is flat");
		const std::string L = SkyBandLine(Centre, Centre, Ground);
		std::printf("    %s\n", L.c_str());
		Check(L.find("band.ground.darkerThanSkyMedianPct=43.7500/of=1280") != std::string::npos,
		      "the rank key counts the ground pixels strictly below the sky's median over its own denominator");
		Check(L.find("band.ground.darkerThanSkyMedianPctTies=80/of=1280") != std::string::npos,
		      "the ties print beside it, because a strict comparison leaves them outside the count");
		Check(L.find("band.ground.darkerThanSkyMedianPctRails=10/5/of=1280") != std::string::npos,
		      "and both rails, lo then hi, which is where the curve stops being strictly monotone");
		// THE CLASS WORD IS NOT OPTIONAL ON EITHER KEY, and the word
		// "invariant" may not appear without the three exceptions beside it.
		Check(L.find("ROBUST-NOT-INVARIANT") != std::string::npos
		      && L.find("a-tonemap-is-monotone-not-linear-so-this-moves-when-the-exposure-moves")
		         != std::string::npos,
		      "the ratio declares itself robust and not invariant, and says why a tonemap makes it move");
		Check(L.find("EXACTLY-invariant-under-any-strictly-monotone-whole-frame-curve") != std::string::npos
		      && L.find("NOT-invariant-under-bloom-vignette-grain-or-local-tonemapping-which-are-not-"
		                "whole-frame-monotone") != std::string::npos,
		      "the rank key declares exact invariance AND names bloom, vignette and local tonemapping as the exceptions");
		// MECHANICAL, NOT A READING: every occurrence of the word must sit on
		// a line that also carries the exceptions clause. This is CONDITION
		// C7 of the ruling turned into a check, so nobody has to grep it by
		// hand a second time.
		{
			int Hits = 0;
			for (size_t At = L.find("nvariant"); At != std::string::npos;
			     At = L.find("nvariant", At + 1)) { ++Hits; }
			Check(Hits > 0 && L.find("NOT-invariant-under-bloom-vignette-grain-or-local-tonemapping")
			                  != std::string::npos,
			      "every use of the word invariant on this line ships the clause naming its exceptions");
			std::printf("    invariantHits=%d of 1 line examined, exceptionsClause=present\n", Hits);
		}
		// THE ROBUST RATIO IS THE BAND'S OWN TWO ORDER STATISTICS AND NOTHING
		// ELSE, checked against the arithmetic rather than a typed number.
		char WantRatio[80];
		std::snprintf(WantRatio, sizeof(WantRatio), "band.ground.p95OverP05=%.4f",
		              Ground.P95 / Ground.P05);
		Check(L.find(WantRatio) != std::string::npos,
		      "the robust ratio is this band's p95 over its own p05, indexed and not interpolated");
		Check(ValuesHaveNoSpaces(L), "every A2 value is space-free");

		// ---- AND THE REFUSALS, PLANTED ----------------------------------
		//
		// A ratio over a zero p05 is not a contrast and may not print a
		// number, and a rank key with no threshold to rank against may not
		// print a zero that would read as a road with no dark in it.
		const std::vector<unsigned char> Black = Flat(W, H, 0, 0, 0);
		const BandStats AllBlack = MeasureBand(Black.data(), W, H, "ground",
		                                       0.0, GroundY0(), 1.0, 1.0);
		const std::string Z = GroundRobustRatioKeys(AllBlack);
		std::printf("    %s\n", Z.c_str());
		Check(Z.find("band.ground.p95OverP05=NOTHING-MEASURED") != std::string::npos
		      && Z.find("a-ratio-over-a-rail-is-not-a-contrast") != std::string::npos,
		      "a band whose dark end is on the rail refuses the ratio rather than dividing by zero");
		Check(Z.find("ROBUST-NOT-INVARIANT") != std::string::npos,
		      "and the refusing line still carries the class word, so the key is never learned without it");
		const BandStats NoSky = MeasureBand(Px.data(), W, H, "skyCentre", 0.5, 0.5, 0.5, 0.5);
		const std::string NR = GroundRankKeys(Ground, NoSky);
		std::printf("    %s\n", NR.c_str());
		Check(NR.find("band.ground.darkerThanSkyMedianPct=NOTHING-MEASURED") != std::string::npos
		      && NR.find("the-skyCentre-band-had-no-pixels-so-there-is-no-threshold-to-rank-against")
		         != std::string::npos
		      && NR.find("Ties=nothing-measured") != std::string::npos
		      && NR.find("Rails=nothing-measured") != std::string::npos,
		      "a rank key with no threshold says nothing measured on all three of its numbers");
		Check(ValuesHaveNoSpaces(NR), "the nothing-measured rank line is space-free too");
		// AND THE INVARIANCE ITSELF, WHICH IS THE CLAIM THE KEY MAKES: put
		// every pixel of the frame through a strictly monotone curve and the
		// number must not move by a digit. A percentile would; this is the
		// whole reason the key exists and it is cheaper to prove than to
		// argue. The curve is a gamma of 0.45 applied to the 8-bit codes,
		// which is monotone, not linear, and is the shape of the exposure
		// plus filmic curve this rig cannot snap.
		std::vector<unsigned char> Curved = Px;
		for (size_t I = 0; I + 3 < Curved.size(); I += 4)
		{
			for (int C = 0; C < 3; ++C)
			{
				const double V = (double)Curved[I + C] / 255.0;
				Curved[I + C] = (unsigned char)(std::pow(V, 0.45) * 255.0 + 0.5);
			}
		}
		const BandStats CurvedCentre = MeasureBand(Curved.data(), W, H, "skyCentre",
		                                          SkyCentreX0(), 0.0, SkyCentreX1(), SkyTopY1());
		const BandStats CurvedGround = MeasureBand(Curved.data(), W, H, "ground",
		                                          0.0, GroundY0(), 1.0, 1.0);
		const std::string C2 = GroundRankKeys(CurvedGround, CurvedCentre);
		std::printf("    afterMonotoneCurve: %s\n", C2.c_str());
		Check(C2.find("band.ground.darkerThanSkyMedianPct=43.7500/of=1280") != std::string::npos,
		      "the rank key reads the SAME number after a strictly monotone curve, which is what it claims");
		Check(std::fabs(CurvedGround.P05 - Ground.P05) > 0.01,
		      "while the band's own p05 moved under that same curve, which is why no percentile is quotable across cells");
	}
	// AND THE REJECTING CASES, EACH PLANTED RATHER THAN WAITED FOR.
	{
		const int W = 40, H = 40;
		const std::vector<unsigned char> Px = Flat(W, H, 10, 10, 10);
		// A rectangle that rounds away to nothing must say nothing measured
		// and print the pixel rectangle that proves WHY, because an empty
		// band and a black band are different faults.
		const BandStats Empty = MeasureBand(Px.data(), W, H, "skyTop",
		                                    0.5, 0.5, 0.5, 0.5);
		const std::string E = BandLine(Empty);
		std::printf("    %s\n", E.c_str());
		Check(!Empty.Measured && Empty.Pixels == 0
		      && E.find("band.skyTop=NOTHING-MEASURED") != std::string::npos
		      && E.find("band.skyTop.rectPx=20/20/20/20") != std::string::npos,
		      "a rectangle that covers no pixel says nothing measured and prints the rectangle");
		Check(ValuesHaveNoSpaces(E), "the nothing-measured band line is space-free");
		// No image at all is a third state and may not read as either.
		const BandStats NoImage = MeasureBand(0, 0, 0, "ground", 0.0, 0.0, 1.0, 1.0);
		Check(!NoImage.Measured && NoImage.Pixels == 0,
		      "no image at all measures nothing rather than an empty rectangle");
		// A whole-frame band on a black frame IS measured, and reads black.
		// This is the case that separates "nothing measured" from "measured
		// and dark", which is the distinction the sky key exists for.
		const BandStats Black = MeasureBand(Px.data(), W, H, "ground",
		                                    0.0, 0.0, 1.0, 1.0);
		Check(Black.Measured && Black.Pixels == 1600 && Black.MeanLuma < 0.05,
		      "a dark band is MEASURED and dark, which is not the same as nothing measured");
		const std::string S = SkyBandLine(Empty, Empty, Black);
		Check(S.find("bandGroundOverSky=NOTHING-MEASURED") != std::string::npos,
		      "a ratio with an unmeasured denominator refuses rather than dividing");
		// AND THE CLIPPING HALF, PLANTED: a band at the top of the range must
		// count it, or a blown sky reads as a bright one.
		std::vector<unsigned char> Blown = Flat(W, H, 255, 255, 255);
		const BandStats Clip = MeasureBand(Blown.data(), W, H, "skyTop",
		                                   0.0, 0.0, 1.0, 1.0);
		Check(Clip.Measured && Clip.ClipHiAny == 1600,
		      "a blown band counts every clipped pixel over its own denominator");
	}

	{
		// ---- THE RIG'S OWN DETERMINISM, ACCEPTING CASE FIRST -------------
		//
		// The accepting case is the one that matters: two takes of the same
		// picture must read IDENTICAL with a zero count over a real
		// denominator, or the key can never clear and the guard is a ratchet.
		const int W = 40, H = 40;
		std::vector<unsigned char> A = Flat(W, H, 100, 110, 120);
		std::vector<unsigned char> B = A;
		const RepeatDiff Same = MeasureRepeat(A.data(), B.data(), W, H);
		const std::string L = RigDeterminismLine("vign_camA_day", 11, 11, "MEASURED", Same);
		std::printf("    %s\n", L.c_str());
		Check(Same.Comparable && Same.Pixels == 1600 && Same.DiffPixels == 0
		      && Same.MaxAbsChannel == 0 && Near(Same.MeanLumaDelta, 0.0),
		      "two identical frames differ in no pixel and no channel");
		Check(L.find("rigDeterminism=IDENTICAL") != std::string::npos
		      && L.find("rigDiffPixels=0/1600") != std::string::npos
		      && L.find("rigMaxAbsChannelDiff=0/255") != std::string::npos,
		      "and the line says IDENTICAL with the zero beside its denominator");
		Check(L.find("rigRepeatAfterShots=11/11") != std::string::npos,
		      "the repeat prints how many shots stood between it and the first frame");
		Check(ValuesHaveNoSpaces(L), "the rig determinism line is space-free");
		// AND THE RATIO THE FAULT IS STATED IN. production/NOW.md records the
		// original as "darker by a luma ratio of 0.82"; two identical frames
		// are 1.0000 and that is the only reading a same-picture claim rests
		// on. Accepting case first, here, on the identical pair.
		Check(RepeatRatioExists(Same) && Near(RepeatLumaRatio(Same), 1.0)
		      && L.find("rigMeanLumaRatio=1.0000") != std::string::npos,
		      "two identical frames print a luma ratio of exactly 1.0000");

		// ---- AND THE PLANTED CASE THE KEY EXISTS TO CATCH ----------------
		//
		// Rule 5b: the thing it asserts must be shown to be able to happen.
		// Three pixels moved, one of them by 7 codes, and the run 38 shape
		// planted in miniature: the repeat uniformly darker.
		B[0 * 4 + 1] = 103;                       // green, 7 codes down
		B[1 * 4 + 2] = 119;                       // red, 1 code down
		B[2 * 4 + 0] = 101;                       // blue, 1 code up
		const RepeatDiff Moved = MeasureRepeat(A.data(), B.data(), W, H);
		const std::string M = RigDeterminismLine("vign_camA_day", 11, 11, "MEASURED", Moved);
		std::printf("    %s\n", M.c_str());
		Check(Moved.DiffPixels == 3 && Moved.MaxAbsChannel == 7,
		      "three moved pixels are counted and the worst channel is the worst one");
		Check(M.find("rigDeterminism=DIFFERS") != std::string::npos
		      && M.find("rigDiffPixels=3/1600") != std::string::npos
		      && M.find("rigMaxAbsChannelDiff=7/255") != std::string::npos,
		      "a rig that moved says DIFFERS and prints how far, over its denominator");
		Check(Moved.MeanLumaRepeat < Moved.MeanLumaFirst
		      && M.find("rigMeanLumaDelta=-") != std::string::npos,
		      "a repeat that came back darker prints a signed negative delta");
		// AND WHAT THE RATIO CANNOT SEE, WHICH IS WHY IT SHIPS BESIDE THE
		// COUNT AND NEVER INSTEAD OF IT. Three moved pixels in 1600 move the
		// whole-frame ratio by about one part in a hundred thousand, so it
		// prints 1.0000 while rigDiffPixels prints 3/1600. A run read on the
		// ratio alone would call this pair the same picture.
		Check(RepeatLumaRatio(Moved) < 1.0
		      && M.find("rigMeanLumaRatio=1.0000") != std::string::npos
		      && M.find("rigDiffPixels=3/1600") != std::string::npos,
		      "three moved pixels leave the whole-frame ratio at 1.0000 to four decimals "
		      "while the per-pixel count sees them, which is why both are printed");
		// ---- THE RATIO PLANTED AT THE SIZE THE FAULT WAS REPORTED AT -----
		//
		// 0.82 in production/NOW.md and 0.0849 at f6508b3 (0.0518 over
		// 0.6099). A whole frame at 82 per cent of another whole frame is the
		// case the key exists to print, so it is planted rather than argued.
		{
			std::vector<unsigned char> Bright = Flat(W, H, 200, 200, 200);
			std::vector<unsigned char> Dim    = Flat(W, H, 164, 164, 164);
			const RepeatDiff Ratio82 = MeasureRepeat(Bright.data(), Dim.data(), W, H);
			const std::string R82 = RigDeterminismLine("vign_camA_day", 25, 25,
			                                           "MEASURED", Ratio82);
			std::printf("    %s\n", R82.c_str());
			Check(Near(RepeatLumaRatio(Ratio82), 0.82)
			      && R82.find("rigMeanLumaRatio=0.8200") != std::string::npos
			      && R82.find("rigDiffPixels=1600/1600") != std::string::npos,
			      "a repeat at 82 per cent of the first frame prints 0.8200 beside every "
			      "one of its 1600 differing pixels");
		}
		// AND A FIRST FRAME WITH NO LIGHT IN IT HAS NO RATIO, which is not a
		// zero: the division has no denominator and the line says so.
		{
			std::vector<unsigned char> Black = Flat(W, H, 0, 0, 0);
			std::vector<unsigned char> Lit   = Flat(W, H, 128, 128, 128);
			const RepeatDiff FromBlack = MeasureRepeat(Black.data(), Lit.data(), W, H);
			const std::string FB = RigDeterminismLine("vign_camA_day", 25, 25,
			                                          "MEASURED", FromBlack);
			Check(!RepeatRatioExists(FromBlack)
			      && FB.find("rigMeanLumaRatio=nothing-measured/") != std::string::npos
			      && FB.find("rigMeanLumaRatio=0.0000") == std::string::npos,
			      "a first frame at zero luma has no ratio rather than a ratio of zero");
			Check(ValuesHaveNoSpaces(FB), "and that line is space-free too");
		}

		// ---- AND A RUN THAT COULD NOT TAKE THE REPEAT --------------------
		//
		// No repeat and no difference are the two readings this key exists
		// to keep apart, so an unmeasured run may not print a zero.
		const RepeatDiff None = MeasureRepeat(A.data(), 0, W, H);
		const std::string N = RigDeterminismLine("", 0, 11, "NO-FIRST-FRAME", None);
		std::printf("    %s\n", N.c_str());
		Check(!None.Comparable && None.Pixels == 0,
		      "a missing half measures nothing rather than measuring agreement");
		Check(N.find("rigDeterminism=NOTHING-MEASURED") != std::string::npos
		      && N.find("rigRepeatStatus=NO-FIRST-FRAME") != std::string::npos
		      && N.find("rigDiffPixels=nothing-measured") != std::string::npos
		      && N.find("rigMeanLumaRatio=nothing-measured") != std::string::npos,
		      "and the line says the words rather than printing a zero difference");
		Check(ValuesHaveNoSpaces(N), "the nothing-measured rig line is space-free too");
		// A DECODED PAIR THE CALLER MARKED UNMEASURED STAYS UNMEASURED: the
		// status word is the caller's and it outranks the arithmetic.
		const std::string P = RigDeterminismLine("vign_camA_day", 11, 11, "NO-FILE", Same);
		Check(P.find("rigDeterminism=NOTHING-MEASURED") != std::string::npos
		      && P.find("rigRepeatStatus=NO-FILE") != std::string::npos,
		      "a repeat whose file never landed cannot read as IDENTICAL");
	}

	// ---- QUEUE 333: THE LAMP ACCEPTANCE INSTRUMENT, PIXEL HALF -----------
	//
	// ACCEPTING CASE FIRST (rule 5b). The expensive failure for this guard is
	// not that it misses a dark lamp; it is that it says no to a lamp that IS
	// lit and the studio spends a CI round trip raising a strength constant
	// that was never the problem. So the first fixture is a lit lamp and the
	// check is that it reads yes.
	//
	// WHAT THESE FRAMES ARE. Synthetic BGRA built by Flat and Paint, with the
	// cold background standing in for a night street (r30 g40 b60, warm -30)
	// and the blob standing in for a sodium globe (r250 g200 b10, warm 240).
	// Nothing here is measured off a render: this proves the arithmetic and
	// the strings, and what a real lamp reads is the run's business.
	{
		std::printf("  -- queue 333: the lantern against its own ring --\n");
		const int LW = 200, LH = 120;
		const int LanternsInFile = 4;

		// (1) ACCEPTING: a warm bright blob filling the lamp's own box.
		std::vector<unsigned char> Lit = Flat(LW, LH, 60, 40, 30);
		Paint(Lit, LW, LH, 90, 50, 110, 60, 10, 200, 250);
		const LampPatch Yes = MeasureLampPatch(Lit.data(), LW, LH, "lantern0",
		                                       true, 90.0, 50.0, 110.0, 60.0);
		std::printf("    core %d/%d ring %d/%d corePx=%lld ringPx=%lld word=%s\n",
		            Yes.CoreMaxLuma, Yes.CoreMaxWarm, Yes.RingMaxLuma, Yes.RingMaxWarm,
		            Yes.CorePixels, Yes.RingPixels, LampPatchWord(Yes));
		Check(Yes.Measured && LampPatchLit(Yes),
		      "a warm bright globe inside the lamp's own box reads as lit");
		Check(Yes.CoreMaxLuma == 193 && Yes.CoreWarmAtMaxLuma == 240
		      && Yes.CoreMaxWarm == 240 && Yes.CoreLumaAtMaxWarm == 193,
		      "and its two peaks each carry the companion measured at the same pixel");
		Check(Yes.CorePixels == 200 && Yes.RingPixels == 2800
		      && Near(Yes.CoreMeanLuma, 193.0),
		      "over 200 core pixels and a ring of 2800, the ring being the box grown "
		      "by its own longer side");
		Check(Yes.RingMaxLuma == 39 && Yes.RingMaxWarm == -30,
		      "the ring reads the cold background, and its warm peak is negative "
		      "rather than clamped to zero");

		// (2) REJECTING, AND THE CASE THE ITEM WAS FILED FOR: the same blob
		// moved into the RING. This is the silhouette the probe actually
		// renders today, a dark head against something brighter, and the
		// instrument must say no to it.
		std::vector<unsigned char> Silhouette = Flat(LW, LH, 60, 40, 30);
		Paint(Silhouette, LW, LH, 72, 32, 82, 42, 10, 200, 250);
		const LampPatch No = MeasureLampPatch(Silhouette.data(), LW, LH, "lantern0",
		                                      true, 90.0, 50.0, 110.0, 60.0);
		Check(No.Measured && !LampPatchLit(No)
		      && std::string(LampPatchWord(No)) == "no",
		      "a dark lamp head with the bright warm thing beside it rather than in "
		      "it reads no");
		Check(No.CoreMaxLuma == 39 && No.RingMaxLuma == 193,
		      "and the two numbers that decided it are both on the line");

		// (3) REJECTING, THE TIE: a flat field. Every pixel equal means the
		// core cannot be STRICTLY brighter than the ring, and a tie is not a
		// lit lamp. This is the case a bound chosen by eye would get wrong.
		std::vector<unsigned char> FlatField = Flat(LW, LH, 60, 40, 30);
		const LampPatch Tie = MeasureLampPatch(FlatField.data(), LW, LH, "lantern0",
		                                       true, 90.0, 50.0, 110.0, 60.0);
		Check(Tie.Measured && !LampPatchLit(Tie),
		      "a flat field ties on both axes and ties do not read as lit");

		// (4) AND THE THREE WAYS A LANTERN PRODUCES NO READING AT ALL, none
		// of which may print as a no.
		const LampPatch NoBox = MeasureLampPatch(Lit.data(), LW, LH, "lantern0",
		                                         false, 0.0, 0.0, 0.0, 0.0);
		Check(!NoBox.Measured && !LampPatchLit(NoBox)
		      && std::string(LampPatchWord(NoBox)) == "nothing-measured"
		      && NoBox.Why == "the-projection-did-not-answer-for-this-lantern",
		      "a lantern whose box the projection refused says the words rather than no");
		const LampPatch OffFrame = MeasureLampPatch(Lit.data(), LW, LH, "lantern0",
		                                            true, 500.0, 50.0, 520.0, 60.0);
		Check(!OffFrame.Measured
		      && OffFrame.Why == "the-lanterns-box-falls-outside-this-frame",
		      "a lantern projected off the edge of the picture measures nothing");
		const LampPatch NoFrame = MeasureLampPatch(0, LW, LH, "lantern0",
		                                           true, 90.0, 50.0, 110.0, 60.0);
		Check(!NoFrame.Measured && NoFrame.Why == "no-decoded-frame",
		      "and so does a shot with no decoded frame behind it");

		// (5) THE SEGMENT, WHICH IS THE THING THE SHOT LINE CARRIES.
		std::vector<LampPatch> Four;
		Four.push_back(Yes);
		Four.push_back(No);
		Four.push_back(Tie);
		Four.push_back(NoBox);
		const std::string Seg = LampGlowSegment(Four, LanternsInFile, true, 0);
		std::printf("    %s\n", Seg.c_str());
		Check(Seg.find("lampGlowLit=1/of=3/examined=4/inFile=4") != std::string::npos,
		      "the lit count ships all three of its denominators: read, examined and "
		      "in the file, which are three different numbers");
		Check(Seg.find("lampGlow1=lantern0/yes/") != std::string::npos
		      && Seg.find("lampGlow2=lantern0/no/") != std::string::npos
		      && Seg.find("lampGlow4=lantern0/nothing-measured/") != std::string::npos,
		      "and every lantern prints its own word on the same line, yes or no or "
		      "the words");
		Check(Seg.find("box=x90..110/y50..60") != std::string::npos
		      && Seg.find("ring=x70..130/y30..80") != std::string::npos,
		      "with both rectangles in pixels, so the ring can be re-derived from the "
		      "line rather than trusted");
		Check(ValuesHaveNoSpaces(Seg), "the lamp segment is space-free");

		// (6) A LANTERN THAT FELL DOWN AN UNPAINTED EXIT IS MISSING FROM THE
		// VECTOR ENTIRELY, and the line has to keep saying 4 were in the file.
		std::vector<LampPatch> One;
		One.push_back(Yes);
		const std::string Short = LampGlowSegment(One, LanternsInFile, true, 0);
		Check(Short.find("lampGlowLit=1/of=1/examined=1/inFile=4") != std::string::npos,
		      "a run that could only examine one of four lanterns says one of four "
		      "rather than one of one");

		// (7) THE CAP ANNOUNCES ITSELF, and it announces on every line rather
		// than only when it bites, so a reader never has to know the cap.
		const std::string Capped = LampGlowSegment(Four, LanternsInFile, true, 2);
		Check(Capped.find("lampGlowShown=2/notShown=2") != std::string::npos
		      && Capped.find("lampGlow3=") == std::string::npos,
		      "a capped line says how many it did not show, and does not show them");
		Check(Seg.find("lampGlowShown=4/notShown=0") != std::string::npos,
		      "and an uncapped line says so with a zero rather than with silence");
		Check(ValuesHaveNoSpaces(Capped), "the capped line is space-free too");

		// (8) THE TWO WHOLE-SEGMENT NOTHING-MEASURED CASES.
		const std::string NoDecode = LampGlowSegment(Four, LanternsInFile, false, 0);
		Check(NoDecode.find("lampGlow=nothing-measured/") != std::string::npos
		      && NoDecode.find("lampGlowLit=") == std::string::npos,
		      "a shot line with no decoded frame prints nothing-measured and no lit "
		      "count at all");
		const std::string NoLanterns = LampGlowSegment(std::vector<LampPatch>(), 0, true, 0);
		Check(NoLanterns.find("lampGlow=nothing-measured/") != std::string::npos
		      && NoLanterns.find("inFile=0") != std::string::npos,
		      "and a street with no emissive piece in it says that, with its zero");
		Check(ValuesHaveNoSpaces(NoDecode) && ValuesHaveNoSpaces(NoLanterns),
		      "both nothing-measured lines are space-free");

		// (9) AN ID WITH A SPACE IN IT WOULD TRUNCATE EVERY TOKEN AFTER IT.
		// Sanitised here, in the tested layer, rather than trusted from the
		// module that reads the name out of the file.
		const LampPatch Spaced = MeasureLampPatch(Lit.data(), LW, LH, "lantern 0 head",
		                                          true, 90.0, 50.0, 110.0, 60.0);
		std::vector<LampPatch> SpacedOne;
		SpacedOne.push_back(Spaced);
		const std::string SpacedSeg = LampGlowSegment(SpacedOne, 1, true, 0);
		Check(Spaced.Id == "lantern_0_head" && ValuesHaveNoSpaces(SpacedSeg),
		      "an id carrying spaces is sanitised before it reaches the line");
	}

	// ---- THE FIGURE AGAINST WHAT IS BEHIND IT, PIXEL HALF ----------------
	//
	// ACCEPTING CASE FIRST (rule 5b). The expensive failure for this guard is
	// not that it misses a bright figure; it is that it says no to a figure
	// that IS a silhouette, and the studio spends a CI round trip darkening a
	// character material that was never the problem. So the first fixture is
	// a dark figure on a light street and the check is that it reads yes.
	//
	// WHAT THESE FRAMES ARE. Synthetic BGRA built by Flat and Paint. The
	// background stands in for an overcast wet street (r120 g125 b130, luma
	// 124) and the figure for a dark coat against it (r20 g22 b24, luma 22).
	// NOTHING HERE IS MEASURED OFF A RENDER: this proves the arithmetic and
	// the strings. What a real figure on the real street reads is the run's
	// business, and the series this prints is what any future margin has to
	// be read off. There is no margin in the comparison today, deliberately.
	{
		std::printf("  -- the figure against what is behind it --\n");
		const int FW = 200, FH = 120;
		const int FiguresInScene = 4;
		// The figure's box: 18 wide, 60 tall, the proportions of a standing
		// person rather than a square, because the shared ring pads by the
		// LONGER side and a square would hide what that costs.
		const double BX0 = 90.0, BY0 = 30.0, BX1 = 108.0, BY1 = 90.0;

		// (1) ACCEPTING: a dark rectangle on a light field.
		std::vector<unsigned char> Dark = Flat(FW, FH, 130, 125, 120);
		Paint(Dark, FW, FH, 90, 30, 108, 90, 24, 22, 20);
		const FigurePatch Yes = MeasureFigurePatch(Dark.data(), FW, FH, "figure0",
		                                           true, BX0, BY0, BX1, BY1);
		std::printf("    core mean %.1f (min %d max %d) over %lld px, ring mean %.1f "
		            "(min %d max %d) over %lld px, gap %.1f, word %s\n",
		            Yes.CoreMeanLuma, Yes.CoreMinLuma, Yes.CoreMaxLuma, Yes.CorePixels,
		            Yes.RingMeanLuma, Yes.RingMinLuma, Yes.RingMaxLuma, Yes.RingPixels,
		            Yes.CoreMeanLuma - Yes.RingMeanLuma, FigureSilhouetteWord(Yes));
		Check(Yes.Measured && FigureReadsAsSilhouette(Yes)
		      && std::string(FigureSilhouetteWord(Yes)) == "yes",
		      "a dark figure on a light street reads as a silhouette");
		Check(Near(Yes.CoreMeanLuma, 22.0) && Near(Yes.RingMeanLuma, 124.0)
		      && Yes.CoreMinLuma == 22 && Yes.CoreMaxLuma == 22
		      && Yes.RingMinLuma == 124 && Yes.RingMaxLuma == 124,
		      "and both means and both pairs of extremes are on the patch, in sRGB "
		      "luma bytes");
		Check(Yes.CorePixels == 1080 && Yes.RingPixels == 15480,
		      "over 1080 core pixels and a ring of 15480, the ring being the box "
		      "grown by its own LONGER side and clipped to the frame");
		Check(Yes.CoreDarkerThanRingMeanPixels == 1080,
		      "with every one of its 1080 core pixels darker than the ring mean, "
		      "which is what tells a dark figure from a bright one in a dark hat");
		Check(Near(Yes.ProjW, 18.0) && Near(Yes.ProjH, 60.0) && Yes.ProjKnown,
		      "and the unrounded projected extent it was handed rides along with it");

		// (2) REJECTING, THE TIE: a uniform field. Every pixel equal means
		// the core cannot be STRICTLY darker than the ring, and a tie is not
		// a silhouette. This is the case a bound chosen by eye gets wrong.
		std::vector<unsigned char> Uniform = Flat(FW, FH, 130, 125, 120);
		const FigurePatch Tie = MeasureFigurePatch(Uniform.data(), FW, FH, "figure0",
		                                           true, BX0, BY0, BX1, BY1);
		Check(Tie.Measured && !FigureReadsAsSilhouette(Tie)
		      && std::string(FigureSilhouetteWord(Tie)) == "no"
		      && Tie.Why == "measured",
		      "a uniform field ties, and a tie reads no rather than nothing-measured: "
		      "it was measured, and the answer was no");
		Check(Near(Tie.CoreMeanLuma, Tie.RingMeanLuma)
		      && Tie.CoreDarkerThanRingMeanPixels == 0 && Tie.CorePixels == 1080,
		      "and its zero darker-than-ring count ships the 1080 it is out of");

		// (3) REJECTING, THE LIT FIGURE: a core BRIGHTER than its ring. A
		// figure standing in the lamp's pool is not a silhouette, and the
		// instrument must say so rather than reporting any strong contrast.
		std::vector<unsigned char> Bright = Flat(FW, FH, 130, 125, 120);
		Paint(Bright, FW, FH, 90, 30, 108, 90, 230, 235, 240);
		const FigurePatch Lit = MeasureFigurePatch(Bright.data(), FW, FH, "figure0",
		                                           true, BX0, BY0, BX1, BY1);
		Check(Lit.Measured && !FigureReadsAsSilhouette(Lit)
		      && Near(Lit.CoreMeanLuma, 236.0) && Near(Lit.RingMeanLuma, 124.0),
		      "a figure brighter than what is behind it reads no, however strong the "
		      "contrast is");

		// (3b) THE DARKER-THAN-RING COUNT IS A SECOND PASS OVER THE PIXELS
		// WITH ITS OWN CHANNEL EXPRESSION, and every fixture above is a grey
		// or near-grey where B, G and R swapped would read the same. So one
		// asymmetric fixture pins it: a core of PURE RED (luma 76) inside a
		// grey ring of luma 50. Read correctly the count is 0 of 1080,
		// because 76 is above 50; read with red and blue swapped the same
		// pixels would score 29 and the count would be 1080 of 1080. The two
		// answers are opposite, which is the only way this pass can be
		// checked at all.
		std::vector<unsigned char> Red = Flat(FW, FH, 50, 50, 50);
		Paint(Red, FW, FH, 90, 30, 108, 90, 0, 0, 255);
		const FigurePatch Chan = MeasureFigurePatch(Red.data(), FW, FH, "figure0",
		                                            true, BX0, BY0, BX1, BY1);
		std::printf("    channel fixture: core mean %.1f ring mean %.1f "
		            "darkerThanRingMean %lld of %lld\n",
		            Chan.CoreMeanLuma, Chan.RingMeanLuma,
		            Chan.CoreDarkerThanRingMeanPixels, Chan.CorePixels);
		Check(Near(Chan.CoreMeanLuma, 76.0) && Near(Chan.RingMeanLuma, 50.0),
		      "a pure red core reads 76 and not 29, so the first pass weights the "
		      "channels the way BGRA is laid out");
		Check(Chan.CoreDarkerThanRingMeanPixels == 0 && Chan.CorePixels == 1080
		      && !FigureReadsAsSilhouette(Chan),
		      "and the second pass agrees with it: none of the 1080 is darker than "
		      "the ring mean, which a swapped channel would turn into all 1080");

		// (4) THE SIX WAYS A FIGURE PRODUCES NO READING AT ALL, none of which
		// may print as a no.
		const FigurePatch NoBox = MeasureFigurePatch(Dark.data(), FW, FH, "figure0",
		                                             false, 0.0, 0.0, 0.0, 0.0);
		Check(!NoBox.Measured && !FigureReadsAsSilhouette(NoBox)
		      && std::string(FigureSilhouetteWord(NoBox)) == "nothing-measured"
		      && NoBox.Why == "the-projection-did-not-answer-for-this-figure"
		      && !NoBox.ProjKnown,
		      "a figure whose box the projection refused says the words rather than no");
		const FigurePatch NoFrame = MeasureFigurePatch(0, FW, FH, "figure0",
		                                               true, BX0, BY0, BX1, BY1);
		Check(!NoFrame.Measured && NoFrame.Why == "no-decoded-frame",
		      "and so does a shot with no decoded frame behind it");
		const FigurePatch Empty = MeasureFigurePatch(Dark.data(), FW, FH, "figure0",
		                                             true, 90.0, 30.0, 90.0, 90.0);
		Check(!Empty.Measured && Empty.ProjKnown && Near(Empty.ProjW, 0.0)
		      && Empty.Why == "the-figures-box-has-no-width-or-no-height-at-all",
		      "a box with no width at all is a degenerate projection, said in its own "
		      "words rather than folded into the too-small case");
		// A ONE-PIXEL FIGURE IS NOT A FIGURE. Deliberate and written down in
		// the header: the lamp floors and ceils because one pixel of GLOW is
		// a real reading, while a figure under a pixel wide has no interior
		// and its "silhouette" would be a reading of the antialiasing. It is
		// reported measured-but-too-small, with the extent that proves it.
		const FigurePatch Speck = MeasureFigurePatch(Dark.data(), FW, FH, "figure0",
		                                             true, 90.0, 30.0, 90.4, 30.6);
		Check(!Speck.Measured && Speck.ProjKnown
		      && Speck.Why == "the-figures-box-is-under-one-pixel-and-too-small-to-read",
		      "a figure whose box is under a pixel is too small to read rather than "
		      "rounded up into a reading");
		const FigurePatch OffFrame = MeasureFigurePatch(Dark.data(), FW, FH, "figure0",
		                                               true, 500.0, 30.0, 518.0, 90.0);
		Check(!OffFrame.Measured
		      && OffFrame.Why == "the-figures-box-falls-outside-this-frame",
		      "a figure projected off the edge of the picture measures nothing");
		const FigurePatch NoRing = MeasureFigurePatch(Dark.data(), FW, FH, "figure0",
		                                              true, 0.0, 0.0, 200.0, 120.0);
		Check(!NoRing.Measured
		      && NoRing.Why == "this-figure-has-no-ring-pixel-on-this-frame",
		      "and a figure whose box fills the frame has no outside to be darker "
		      "than, which is not the same as not being darker");

		// (5) CLIPPED BY THE FRAME EDGE. It still reads, and the line carries
		// both moments: the extent it was handed beside the box that survived
		// clipping, so a half-visible figure cannot pass for a small one.
		std::vector<unsigned char> Edge = Flat(FW, FH, 130, 125, 120);
		Paint(Edge, FW, FH, 0, 30, 10, 90, 24, 22, 20);
		const FigurePatch Clip = MeasureFigurePatch(Edge.data(), FW, FH, "figure0",
		                                            true, -8.0, 30.0, 10.0, 90.0);
		Check(Clip.Measured && FigureReadsAsSilhouette(Clip)
		      && Clip.CorePixels == 600 && Clip.RingPixels == 7800,
		      "a figure half off the left edge still reads, over the 600 core pixels "
		      "that are actually in the picture");
		Check(Clip.CX0 == 0 && Clip.CX1 == 10 && Near(Clip.ProjW, 18.0),
		      "and its clipped box prints beside the 18.00 pixels it was handed, so "
		      "the clip is visible rather than passing for a small figure");

		// (6) THE SEGMENT, WHICH IS THE THING THE SHOT LINE CARRIES.
		std::vector<FigurePatch> Four;
		Four.push_back(Yes);
		Four.push_back(Tie);
		Four.push_back(Lit);
		Four.push_back(NoBox);
		const std::string Seg = FigureSilhouetteSegment(Four, FiguresInScene, true, 0);
		std::printf("    %s\n", Seg.c_str());
		Check(Seg.find("figureSilYes=1/of=3/examined=4/inScene=4") != std::string::npos,
		      "the silhouette count ships all three of its denominators: read, "
		      "examined and in the scene, which are three different numbers");
		Check(Seg.find("figureSil1=figure0/yes/") != std::string::npos
		      && Seg.find("figureSil2=figure0/no/") != std::string::npos
		      && Seg.find("figureSil4=figure0/nothing-measured/") != std::string::npos,
		      "and every figure prints its own word on the same line, yes or no or "
		      "the words");
		Check(Seg.find("coreMeanLuma=22.0") != std::string::npos
		      && Seg.find("ringMeanLuma=124.0") != std::string::npos
		      && Seg.find("coreMinusRingMeanLuma=-102.0") != std::string::npos,
		      "the two numbers that decided it are both on the line, and so is the "
		      "signed gap between them, which is the series a margin would come from");
		Check(Seg.find("coreDarkerThanRingMean=1080/of=1080") != std::string::npos,
		      "the darker-than-ring count carries its denominator inside the value");
		Check(Seg.find("box=x90..108/y30..90") != std::string::npos
		      && Seg.find("ring=x30..168/y0..120") != std::string::npos,
		      "with both rectangles in pixels, so the ring can be re-derived from the "
		      "line rather than trusted");
		Check(Seg.find("figureSil4=figure0/nothing-measured/"
		               "the-projection-did-not-answer-for-this-figure"
		               "/projW=nothing-measured") != std::string::npos,
		      "and a figure with no projected extent says those words too rather than "
		      "printing a zero-sized box");
		Check(ValuesHaveNoSpaces(Seg), "the figure segment is space-free");

		// (7) A FIGURE THAT NEVER SPAWNED IS MISSING FROM THE VECTOR
		// ENTIRELY, and the line has to keep saying 4 were in the scene.
		std::vector<FigurePatch> One;
		One.push_back(Yes);
		const std::string Short = FigureSilhouetteSegment(One, FiguresInScene, true, 0);
		Check(Short.find("figureSilYes=1/of=1/examined=1/inScene=4") != std::string::npos,
		      "a run that could only examine one of four figures says one of four "
		      "rather than one of one");

		// (8) THE CAP ANNOUNCES ITSELF ON EVERY LINE, not only when it bites,
		// so a reader never has to know what the cap was.
		const std::string Capped = FigureSilhouetteSegment(Four, FiguresInScene, true, 2);
		Check(Capped.find("figureSilShown=2/notShown=2") != std::string::npos
		      && Capped.find("figureSil3=") == std::string::npos,
		      "a capped line says how many it did not show, and does not show them");
		Check(Seg.find("figureSilShown=4/notShown=0") != std::string::npos,
		      "and an uncapped line says so with a zero rather than with silence");
		Check(ValuesHaveNoSpaces(Capped), "the capped line is space-free too");

		// (9) THE FOUR NOTHING-MEASURED EXITS, EACH DISTINGUISHABLE. "0
		// silhouettes" and "no figure was in this frame" are different facts
		// and a reader who cannot tell them apart reports the second as the
		// first, which is rule 3b with a person in it.
		const std::string NoDecode = FigureSilhouetteSegment(Four, FiguresInScene, false, 0);
		std::printf("    %s\n", NoDecode.c_str());
		Check(NoDecode.find("figureSil=nothing-measured/"
		                    "this-shot-line-carries-no-decoded-frame") != std::string::npos
		      && NoDecode.find("figureSilYes=") == std::string::npos,
		      "exit 1: a shot line with no decoded frame prints the words and no "
		      "silhouette count at all");
		Check(NoDecode.find("figureSilShown=0/notShown=4") != std::string::npos,
		      "and it says the four patches it was handed went unprinted, so they "
		      "cannot vanish between the caller and the line");
		const std::string NoFigures =
			FigureSilhouetteSegment(std::vector<FigurePatch>(), 0, true, 0);
		std::printf("    %s\n", NoFigures.c_str());
		Check(NoFigures.find("figureSil=nothing-measured/"
		                     "no-figure-was-in-this-scene-to-look-for") != std::string::npos
		      && NoFigures.find("inScene=0") != std::string::npos,
		      "exit 2: a scene with no figure in it says that, with its zero");
		const std::string NoneExaminable =
			FigureSilhouetteSegment(std::vector<FigurePatch>(), FiguresInScene, true, 0);
		std::printf("    %s\n", NoneExaminable.c_str());
		Check(NoneExaminable.find("figureSil=nothing-measured/"
		                          "no-figure-could-be-examined-on-this-frame") != std::string::npos
		      && NoneExaminable.find("inScene=4") != std::string::npos,
		      "exit 3: four figures in the scene and none examinable here is a "
		      "different sentence from no figure at all, and keeps its four");
		std::vector<FigurePatch> NoneRead;
		NoneRead.push_back(NoBox);
		NoneRead.push_back(Speck);
		const std::string NoAnswer =
			FigureSilhouetteSegment(NoneRead, FiguresInScene, true, 0);
		std::printf("    %s\n", NoAnswer.c_str());
		Check(NoAnswer.find("figureSil=nothing-measured/"
		                    "no-figures-projection-answered-on-this-frame") != std::string::npos
		      && NoAnswer.find("figureSilYes=") == std::string::npos
		      && NoAnswer.find("figureSilRead=0/examined=2/inScene=4") != std::string::npos,
		      "exit 4: figures examined and not one readable prints the words and a "
		      "read count of zero over its two denominators, never a yes count of zero");
		Check(NoAnswer.find("/projW=0.40/projH=0.60") != std::string::npos,
		      "and the too-small figure carries the extent that proves it was too "
		      "small, rather than asking the reader to take the word for it");
		Check(ValuesHaveNoSpaces(NoDecode) && ValuesHaveNoSpaces(NoFigures)
		      && ValuesHaveNoSpaces(NoneExaminable) && ValuesHaveNoSpaces(NoAnswer),
		      "all four nothing-measured lines are space-free");

		// (10) AN ID WITH A SPACE IN IT WOULD TRUNCATE EVERY TOKEN AFTER IT.
		// Sanitised here, in the tested layer, rather than trusted from the
		// module that reads the actor's name.
		const FigurePatch Spaced2 = MeasureFigurePatch(Dark.data(), FW, FH, "figure 0 coat",
		                                               true, BX0, BY0, BX1, BY1);
		std::vector<FigurePatch> SpacedTwo;
		SpacedTwo.push_back(Spaced2);
		Check(Spaced2.Id == "figure_0_coat"
		      && ValuesHaveNoSpaces(FigureSilhouetteSegment(SpacedTwo, 1, true, 0)),
		      "an id carrying spaces is sanitised before it reaches the line");
	}

	std::printf("frame-stats-test: %d check(s), %d failure(s)\n", Checks, Failures);
	return Failures == 0 ? 0 : 2;
}
