// WHAT A FRAME MEASURES, IN A FILE THAT COMPILES WITHOUT UNREAL.
//
// THE RULE THIS EXISTS FOR, ruled standing on 25 August after the third
// instance: measurement arithmetic and formatting live where the tests run.
// In a project whose top layer does not compile locally, a formatter written
// there ships UNRUN, and an unrun formatter printing a plausible string is
// the silent-instrument failure. So the tally, the maths and the string are
// here, in plain C++ with no engine type anywhere in it, and
// ue-probe/tests/frame-stats-test.cpp compiles and runs them with g++ before
// anything is dispatched. The Unreal module supplies only the pixels.
//
// THE WEIGHTS ARE THE UNITY SIM'S WEIGHTS, deliberately. SimDirector.cs reads
// meanLuma as (0.299R + 0.587G + 0.114B) / 255 over every pixel, and D1 is a
// comparison: a UE frame measured by a different ruler would not be
// comparable to the Unity frames sitting in game-design/sim-shots.
//
// WHAT EACH NUMBER IS A STATISTIC OF, said once, here, and repeated into the
// verdict as comment lines:
//   MeanLuma        mean over EVERY pixel of the decoded image, 0 to 1
//   MinLuma/MaxLuma extremes over that same pixel set
//   NonBlack        count of pixels with ANY channel above zero
//   NonBlackPct     that count over Pixels, which is its denominator
//   DistinctBuckets distinct 5-bit-per-channel colour buckets, out of 32768
//
// THE BLANK RULE IS A STRUCTURAL ZERO, NOT A TUNED BOUND. One colour bucket
// over a whole frame means a flat field; no non-black pixel means the
// renderer put nothing there. Neither number was chosen from a series, which
// is why they may be set before one exists. Any bound on how BRIGHT a frame
// ought to be waits for the series these functions print.
#pragma once

#include <algorithm>
#include <cstdio>
#include <string>
#include <vector>

namespace LedgerFrame
{
	struct FrameStats
	{
		int       Width           = 0;
		int       Height          = 0;
		long long Pixels          = 0;
		long long NonBlack        = 0;
		double    MeanLuma        = 0.0;
		double    MinLuma         = 0.0;
		double    MaxLuma         = 0.0;
		double    NonBlackPct     = 0.0;
		int       DistinctBuckets = 0;
		// True for a frame with one colour bucket or no non-black pixel, AND
		// true for a frame with no pixels at all: nothing measured is not the
		// same as measured and fine, and neither may read as a pass.
		bool      Blank           = true;
	};

	inline double Luma(unsigned char R, unsigned char G, unsigned char B)
	{
		return (0.299 * R + 0.587 * G + 0.114 * B) / 255.0;
	}

	// BGRA8, top row first, which is what IImageWrapper::GetRaw returns for
	// ERGBFormat::BGRA at 8 bits. Named in the parameter rather than assumed
	// in the caller.
	inline FrameStats Measure(const unsigned char* Bgra, int W, int H)
	{
		FrameStats S;
		S.Width = W;
		S.Height = H;
		if (Bgra == nullptr || W <= 0 || H <= 0)
		{
			return S;  // Pixels stays 0 and Blank stays true: nothing measured.
		}
		S.Pixels = (long long)W * (long long)H;
		std::vector<unsigned char> Seen(32768, 0);
		double Sum = 0.0;
		double Mn = 1.0;
		double Mx = 0.0;
		for (long long P = 0; P < S.Pixels; ++P)
		{
			const unsigned char B = Bgra[P * 4];
			const unsigned char G = Bgra[P * 4 + 1];
			const unsigned char R = Bgra[P * 4 + 2];
			const double L = Luma(R, G, B);
			Sum += L;
			if (L < Mn) { Mn = L; }
			if (L > Mx) { Mx = L; }
			if (R > 0 || G > 0 || B > 0) { ++S.NonBlack; }
			const int Bucket = ((R >> 3) << 10) | ((G >> 3) << 5) | (B >> 3);
			if (Seen[Bucket] == 0) { Seen[Bucket] = 1; ++S.DistinctBuckets; }
		}
		S.MeanLuma    = Sum / (double)S.Pixels;
		S.MinLuma     = Mn;
		S.MaxLuma     = Mx;
		S.NonBlackPct = 100.0 * (double)S.NonBlack / (double)S.Pixels;
		S.Blank       = (S.DistinctBuckets <= 1) || (S.NonBlack == 0);
		return S;
	}

	// THE DONE LINE. Whole-run numbers, one moment, one line, and NO SPACES
	// INSIDE ANY VALUE: every reader in this project splits on whitespace and
	// truncates silently when a value contains one. Structure goes in `/`.
	inline std::string DoneLine(const FrameStats& S,
	                            const std::string& Attempt,
	                            const std::string& File,
	                            long long Bytes,
	                            double SecondsWaited,
	                            int Ticks,
	                            const std::string& Note)
	{
		char Buf[768];
		std::snprintf(Buf, sizeof(Buf),
			"shotStatus=%s shotAttempt=%s shotFile=%s shotBytes=%lld shotW=%d shotH=%d "
			"shotPixels=%lld shotMeanLuma=%.4f shotMinLuma=%.4f shotMaxLuma=%.4f "
			"shotNonBlackPixels=%lld shotNonBlackPct=%.2f shotDistinctBuckets=%d/32768 "
			"shotSecondsWaited=%.2f shotTicks=%d shotNote=%s",
			S.Pixels == 0 ? "NOTHING-MEASURED" : (S.Blank ? "BLANK" : "WROTE"),
			Attempt.c_str(), File.c_str(), Bytes, S.Width, S.Height,
			S.Pixels, S.MeanLuma, S.MinLuma, S.MaxLuma,
			S.NonBlack, S.NonBlackPct, S.DistinctBuckets,
			SecondsWaited, Ticks, Note.c_str());
		return std::string(Buf);
	}

	// THE SAME PIXEL NUMBERS, FOR A LINE THAT DESCRIBES ONE SAMPLE.
	//
	// DoneLine above carries whole-run keys, `shotSecondsWaited` and
	// `shotTicks`, which are true of a RUN and not of a frame. Phase B takes
	// four frames in one run, so putting DoneLine on each of them would
	// print the run's elapsed time four times as if it were each shot's, and
	// the project's rule is that whole-run numbers sit on the done line and
	// per-sample numbers on the sample line. This is the per-sample half:
	// everything here is a statistic of THIS image and nothing else.
	//
	// Every number keeps the name it has on the done line, because a reader
	// comparing a Phase B frame to run 16's single frame should not have to
	// learn two vocabularies for one measurement.
	inline std::string PixelLine(const FrameStats& S)
	{
		char Buf[512];
		std::snprintf(Buf, sizeof(Buf),
			"shotW=%d shotH=%d shotPixels=%lld shotMeanLuma=%.4f shotMinLuma=%.4f "
			"shotMaxLuma=%.4f shotNonBlackPixels=%lld shotNonBlackPct=%.2f "
			"shotDistinctBuckets=%d/32768 shotBlank=%s",
			S.Width, S.Height, S.Pixels, S.MeanLuma, S.MinLuma, S.MaxLuma,
			S.NonBlack, S.NonBlackPct, S.DistinctBuckets,
			S.Pixels == 0 ? "NOTHING-MEASURED" : (S.Blank ? "yes" : "no"));
		return std::string(Buf);
	}

	// THE PICTURE IN WORDS, for a channel that cannot open a PNG. The same
	// ascii-luma dump the Unity sim writes beside its stills: a reader with
	// nothing but the verdict file can still tell a lit frame from an empty
	// one. Every row is prefixed so no key reader ever parses it as data.
	inline std::string AsciiLuma(const unsigned char* Bgra, int W, int H,
	                             int Cols = 48, int Rows = 27)
	{
		if (Bgra == nullptr || W <= 0 || H <= 0 || Cols <= 0 || Rows <= 0)
		{
			return std::string("# ascii-luma: nothing measured, no pixels to draw");
		}
		static const char* Ramp = " .:-=+*#%@";
		const int RampN = 10;
		std::string Art;
		Art.reserve((size_t)(Cols + 3) * Rows);
		for (int Ry = 0; Ry < Rows; ++Ry)
		{
			Art += "# ";
			const int Y0 = (Ry * H) / Rows;
			int Y1 = ((Ry + 1) * H) / Rows;
			if (Y1 <= Y0) { Y1 = Y0 + 1; }
			for (int Rx = 0; Rx < Cols; ++Rx)
			{
				const int X0 = (Rx * W) / Cols;
				int X1 = ((Rx + 1) * W) / Cols;
				if (X1 <= X0) { X1 = X0 + 1; }
				double Sum = 0.0;
				int N = 0;
				for (int Y = Y0; Y < Y1 && Y < H; ++Y)
				{
					for (int X = X0; X < X1 && X < W; ++X)
					{
						const long long I = ((long long)Y * W + X) * 4;
						Sum += Luma(Bgra[I + 2], Bgra[I + 1], Bgra[I]);
						++N;
					}
				}
				const double L = (N > 0 ? Sum / N : 0.0);
				int Idx = (int)(L * (RampN - 1) + 0.5);
				if (Idx < 0) { Idx = 0; }
				if (Idx > RampN - 1) { Idx = RampN - 1; }
				Art += Ramp[Idx];
			}
			if (Ry + 1 < Rows) { Art += "\n"; }
		}
		return Art;
	}
}

// ============================================================================
// QUEUE 059: A PLACED LANTERN IS NOT A LIT STREET.
//
// Run 17's scene line read lanternsPlaced=4/4 and every word of it was true.
// It answers "were four lantern lights created". It was never asked "did any
// of them reach a pixel", and both night frames were almost black. At the
// other end of the range shotMeanLuma=0.5030 sat over a day frame whose whole
// ground plane was clipped to flat white, because a mean cannot see clipping.
//
// So there are two measurements below and they live here, in the file g++
// compiles, for the standing reason: an unrun formatter printing a plausible
// string is the quietest instrument fault this project has.
//
// NO BOUND IS SET IN THIS FILE. Every number here is a printer. The counts
// are structural (a channel at 255 is at the top of the 8-bit range; a code
// value of 1 is the quantisation floor) and the histogram edges are powers of
// two, so that a bound can be read off a real series later rather than
// invented now.
// ============================================================================

namespace LedgerFrame
{
	// ---- (b) WHAT THE TONE MAPPER DID, AS COUNTS WITH DENOMINATORS -------
	//
	// Every field is a COUNT over Pixels, never a mean. shotMeanLuma=0.5030
	// and a fully clipped ground plane are the same reading, which is rule
	// 3b's shape: a healthy summary over a population that is not healthy.
	struct ExposureStats
	{
		bool      Measured  = false;   // false means no pixels, not "clean"
		long long Pixels    = 0;
		// Pixels with ANY 8-bit channel at 255. A sodium lamp clipping only
		// its red channel is clipping, and the all-three count below is what
		// separates that from a blown white ground.
		long long ClipHiAny = 0;
		long long ClipHiAll = 0;
		// All three channels at zero. This is the exact complement of
		// FrameStats::NonBlack and is printed anyway, with the complement
		// named in its rule, so that a reader asking about the bottom of the
		// range does not have to do the subtraction and does not read it as a
		// second independent number.
		long long ClipLoAll = 0;
		// EIGHT EQUAL LUMA BANDS OVER 0..1, which is a printed series and not
		// a threshold. Band 0 is the crushed end, band 7 the blown end.
		long long Bands[8]  = {0, 0, 0, 0, 0, 0, 0, 0};
	};

	inline ExposureStats MeasureExposure(const unsigned char* Bgra, int W, int H)
	{
		ExposureStats E;
		if (Bgra == nullptr || W <= 0 || H <= 0) { return E; }
		E.Measured = true;
		E.Pixels = (long long)W * (long long)H;
		for (long long P = 0; P < E.Pixels; ++P)
		{
			const unsigned char B = Bgra[P * 4];
			const unsigned char G = Bgra[P * 4 + 1];
			const unsigned char R = Bgra[P * 4 + 2];
			if (R == 255 || G == 255 || B == 255) { ++E.ClipHiAny; }
			if (R == 255 && G == 255 && B == 255) { ++E.ClipHiAll; }
			if (R == 0 && G == 0 && B == 0)       { ++E.ClipLoAll; }
			int Band = (int)(Luma(R, G, B) * 8.0);
			if (Band < 0) { Band = 0; }
			if (Band > 7) { Band = 7; }
			++E.Bands[Band];
		}
		return E;
	}

	inline double Pct(long long Part, long long Of)
	{
		return Of > 0 ? (100.0 * (double)Part / (double)Of) : 0.0;
	}

	// PER-SAMPLE KEYS ONLY: everything here is a statistic of THIS image.
	// A frame with no pixels prints the words rather than eight zeros that
	// would read as a clean exposure.
	inline std::string ExposureLine(const ExposureStats& E)
	{
		if (!E.Measured || E.Pixels == 0)
		{
			return std::string("shotClipStatus=NOTHING-MEASURED "
			                   "shotClipNote=no-pixels-decoded/nothing-examined");
		}
		char Buf[1200];
		std::snprintf(Buf, sizeof(Buf),
			"shotClipStatus=MEASURED "
			"shotClipHiAny=%lld/%lld shotClipHiAnyPct=%.2f shotClipHiAnyRule=any8bitRGB-at-255 "
			"shotClipHiAll=%lld/%lld shotClipHiAllPct=%.2f shotClipHiAllRule=all8bitRGB-at-255 "
			"shotClipLoAll=%lld/%lld shotClipLoAllPct=%.2f "
			"shotClipLoAllRule=all8bitRGB-at-0/complement-of-shotNonBlackPixels "
			"shotLumaBands=%lld/%lld/%lld/%lld/%lld/%lld/%lld/%lld shotLumaBandsOf=%lld "
			"shotLumaBandEdges=0..1/8equal shotLumaBandStat=pixel-count-per-band/band0-is-darkest",
			E.ClipHiAny, E.Pixels, Pct(E.ClipHiAny, E.Pixels),
			E.ClipHiAll, E.Pixels, Pct(E.ClipHiAll, E.Pixels),
			E.ClipLoAll, E.Pixels, Pct(E.ClipLoAll, E.Pixels),
			E.Bands[0], E.Bands[1], E.Bands[2], E.Bands[3],
			E.Bands[4], E.Bands[5], E.Bands[6], E.Bands[7], E.Pixels);
		return std::string(Buf);
	}

	// ---- (a) DID THIS LIGHT REACH A PIXEL --------------------------------
	//
	// A CONTRIBUTION IS A DIFFERENCE AND NEEDS BOTH HALVES NAMED: the same
	// camera, the same condition, the same frame counts, one light toggled,
	// and the sample region stated. A lantern lighting the far end of the
	// street contributes nothing to a crop of the near end and that is not a
	// failure, so the region this reads is printed beside the number.
	//
	// THE REGION IS A FIXED NAMED GRID, cols by rows over the frame. The
	// whole-frame reading is named `full`; the peak tile is named `cXrY`
	// with its pixel rectangle, so both halves of the difference are
	// attributable to the same rectangle without opening the image.
	//
	// THE CODE-VALUE HISTOGRAM IS A SERIES, NOT A BOUND. Counts of pixels
	// whose luma ROSE by at least 1, 2, 4, 8, 16 and 32 eight-bit code
	// values when the light was on. Powers of two, so no number here was
	// chosen; a bound comes later from real runs. Temporal antialiasing and
	// dither move pixels by a code value or two on their own, which is why
	// the caller is expected to run a CONTROL probe that toggles nothing:
	// the control's histogram is this run's own noise floor and no invented
	// epsilon is needed.
	//
	// AND FOR SIX WEEKS NOTHING READ IT, queue 326. The comment below on
	// `reached the frame` said in as many words that "the control line beside
	// it is what says whether that edge means anything in this run"; the
	// count was taken against `RoseAtLeast[0] > 0` regardless, one pixel
	// rising by one code value. On run 47 at vign_camA_night the control that
	// toggled NOTHING moved the whole frame by 0.25060 of the luma range and
	// four of seven lanterns reported that same number to five decimals, so
	// `lightsReachedFrame=30/42` was a count standing on a floor that swamped
	// it. The pairing is done below now, per shot, against that shot's own
	// control, and a shot whose control is bigger than its lights prints
	// NO-READ with both numbers instead of a count.
	struct LightDelta
	{
		bool      Comparable = false;   // two decoded frames of equal size
		int       Width = 0, Height = 0;
		long long Pixels = 0;
		double    MeanOnFull = 0.0, MeanOffFull = 0.0, MeanDeltaFull = 0.0;
		double    MaxRise = 0.0;        // largest single-pixel luma rise
		double    MaxDrop = 0.0;        // largest single-pixel luma fall
		// Pixels that got BRIGHTER with the light OFF. Physically impossible
		// for a light in isolation, so a non-trivial count here is the
		// auto-exposure compensating and the whole difference is suspect.
		long long PixelsDarkerWithLightOn = 0;
		static const int Edges = 6;     // 1,2,4,8,16,32 code values
		long long RoseAtLeast[6] = {0, 0, 0, 0, 0, 0};
		// AND THE SAME HISTOGRAM WITHOUT THE SIGN: pixels whose luma MOVED by
		// at least that many code values in EITHER direction. RoseAtLeast
		// alone cannot floor anything, which the series said and nobody had
		// looked: run 47's pinset_night_2 control has RoseAtLeast=0/0/0/0/0/0
		// and reads like a pristine floor, while its mean is -0.37873 and all
		// 921600 of its pixels got DARKER. A probe that toggled nothing and
		// moved the frame by a third of the luma range has no floor left to
		// lend, whichever way it moved, so the floor is measured on |delta|.
		long long MovedAtLeast[6] = {0, 0, 0, 0, 0, 0};
		int       Cols = 0, Rows = 0;
		int       PeakCol = -1, PeakRow = -1;
		int       PeakX0 = 0, PeakX1 = 0, PeakY0 = 0, PeakY1 = 0;
		double    PeakMeanDelta = 0.0, PeakMeanOn = 0.0, PeakMeanOff = 0.0;
	};

	inline int DeltaCodeEdge(int I)
	{
		const int E[6] = {1, 2, 4, 8, 16, 32};
		return (I >= 0 && I < 6) ? E[I] : 0;
	}

	// On and Off are BGRA8 buffers of the SAME dimensions, top row first.
	// Different dimensions is not a small problem to paper over: it means the
	// two halves are not the same frame and Comparable stays false.
	inline LightDelta MeasureLightDelta(const unsigned char* On, const unsigned char* Off,
	                                    int W, int H, int Cols = 8, int Rows = 4)
	{
		LightDelta D;
		if (On == nullptr || Off == nullptr || W <= 0 || H <= 0 || Cols <= 0 || Rows <= 0)
		{
			return D;
		}
		D.Comparable = true;
		D.Width = W; D.Height = H;
		D.Pixels = (long long)W * (long long)H;
		D.Cols = Cols; D.Rows = Rows;
		std::vector<double> TileOn((size_t)Cols * Rows, 0.0);
		std::vector<double> TileOff((size_t)Cols * Rows, 0.0);
		std::vector<long long> TileN((size_t)Cols * Rows, 0);
		double SumOn = 0.0, SumOff = 0.0;
		for (int Y = 0; Y < H; ++Y)
		{
			int Ty = (Y * Rows) / H;
			if (Ty >= Rows) { Ty = Rows - 1; }
			for (int X = 0; X < W; ++X)
			{
				const long long I = ((long long)Y * W + X) * 4;
				const double LOn  = Luma(On[I + 2], On[I + 1], On[I]);
				const double LOff = Luma(Off[I + 2], Off[I + 1], Off[I]);
				const double Rise = LOn - LOff;
				SumOn += LOn; SumOff += LOff;
				if (Rise > D.MaxRise) { D.MaxRise = Rise; }
				if (-Rise > D.MaxDrop) { D.MaxDrop = -Rise; }
				if (Rise < 0.0) { ++D.PixelsDarkerWithLightOn; }
				const double Codes = Rise * 255.0;
				const double Moved = (Codes < 0.0) ? -Codes : Codes;
				for (int E = 0; E < LightDelta::Edges; ++E)
				{
					// The edges climb, so the first one not met ends it. A RISE
					// is a MOVE, so the move test is the outer one and no rise
					// can be cut short by it.
					const double Edge = (double)DeltaCodeEdge(E) - 1e-9;
					if (Moved < Edge) { break; }
					++D.MovedAtLeast[E];
					if (Codes >= Edge) { ++D.RoseAtLeast[E]; }
				}
				int Tx = (X * Cols) / W;
				if (Tx >= Cols) { Tx = Cols - 1; }
				const size_t T = (size_t)Ty * Cols + Tx;
				TileOn[T] += LOn; TileOff[T] += LOff; ++TileN[T];
			}
		}
		D.MeanOnFull    = SumOn / (double)D.Pixels;
		D.MeanOffFull   = SumOff / (double)D.Pixels;
		D.MeanDeltaFull = D.MeanOnFull - D.MeanOffFull;
		// THE PEAK TILE, AND ITS TWO HALVES CAPTURED AT THE SAME INSTANT it
		// peaks: the on and off means printed beside it are that tile's, not
		// the frame's, so the number and its denominator describe one region.
		double Best = 0.0;
		for (int Ry = 0; Ry < Rows; ++Ry)
		{
			for (int Rx = 0; Rx < Cols; ++Rx)
			{
				const size_t T = (size_t)Ry * Cols + Rx;
				if (TileN[T] <= 0) { continue; }
				const double MOn  = TileOn[T] / (double)TileN[T];
				const double MOff = TileOff[T] / (double)TileN[T];
				const double Dl   = MOn - MOff;
				if (D.PeakCol < 0 || Dl > Best)
				{
					Best = Dl;
					D.PeakCol = Rx; D.PeakRow = Ry;
					D.PeakMeanDelta = Dl; D.PeakMeanOn = MOn; D.PeakMeanOff = MOff;
					D.PeakX0 = (Rx * W) / Cols; D.PeakX1 = ((Rx + 1) * W) / Cols;
					D.PeakY0 = (Ry * H) / Rows; D.PeakY1 = ((Ry + 1) * H) / Rows;
				}
			}
		}
		return D;
	}

	// ---- QUEUE 326: THE READING IS A COMPARISON, NOT A COUNT -------------
	//
	// WHICH CODE EDGE, IF ANY, THIS LIGHT BEAT ITS OWN SHOT'S CONTROL AT.
	// Returns the HIGHEST edge index with a surplus, or -1 for none.
	//
	// IT IS ASYMMETRIC ON PURPOSE AND THE ASYMMETRY IS THE PHYSICS. The
	// numerator is pixels the light RAISED, because the probe frame is the
	// one with the light switched OFF and taking a light away can only take
	// light away; a frame that came back BRIGHTER with the light off is the
	// auto-exposure answering, which is what `deltaPixelsDarkerWithLightOn`
	// already counts, and counting it as a contribution is the false green
	// this pairing exists to stop. The floor is pixels the control MOVED in
	// either direction, because the control toggled nothing, so every pixel
	// it moved is this run's own disturbance whichever way it went.
	//
	// NO EPSILON AND NO BOUND. Both sides are integer pixel counts at the
	// same printed code edge, compared with a strict `>`, so nothing here was
	// chosen: a light that matches its control to the pixel is not a reading,
	// and on run 47's vign_camA_night four lanterns matched it at all six
	// edges exactly. Comparing the floats would have been a coin toss at
	// those four, which is why the decision rides the counts.
	inline int LightReadEdge(const LightDelta& Control, const LightDelta& Light)
	{
		if (!Control.Comparable || !Light.Comparable)   { return -1; }
		if (Control.Pixels != Light.Pixels)             { return -1; }
		for (int E = LightDelta::Edges - 1; E >= 0; --E)
		{
			if (Light.RoseAtLeast[E] > Control.MovedAtLeast[E]) { return E; }
		}
		return -1;
	}

	// ONE SHOT'S FLOOR PASS. The .cpp hands this the shot's control delta and
	// then each light's delta as it lands, in probe order; every comparison,
	// tally and string is here, where g++ runs them before any dispatch.
	//
	// THE BEST PAIR IS CAPTURED AT ONE EDGE, whichever edge decided it, so
	// the light's count and the control's count on the line are the same
	// instant and not two moments a reader has to relate. When a light won,
	// the surplus is positive and that edge is where it won; when none did,
	// the surplus is zero or negative and that edge is where a light came
	// CLOSEST, which is the number a NO-READ has to carry to be worth
	// anything. One shape, both cases, key names that never move.
	struct LightFloor
	{
		std::string ShotId, CameraId, ConditionId;
		bool       bHaveControl = false;
		LightDelta Control;
		int        Lights = 0;          // lights whose delta was measured here
		int        Read   = 0;          // ... that beat this shot's own control
		std::string BestId;             // the light at the best surplus
		int        BestEdge    = -1;    // and the edge that surplus is AT
		long long  BestLightPx = 0;     // its RoseAtLeast at that edge
		long long  BestCtrlPx  = 0;     // the control's MovedAtLeast there
		double     BestMeanFull = 0.0;  // that same light's whole-frame mean
		bool       bHaveBest   = false;
	};

	// A SHOT READS WHEN AT LEAST ONE OF ITS LIGHTS BEAT ITS OWN CONTROL.
	// With no control there is nothing to read against, which is not the same
	// fact and gets its own word on the line.
	inline bool LightFloorUsable(const LightFloor& F)
	{
		return F.bHaveControl && F.Read > 0;
	}

	inline void LightFloorSetControl(LightFloor& F, const LightDelta& D)
	{
		F.Control = D;
		F.bHaveControl = D.Comparable;
	}

	// Returns whether this light read above its shot's floor, so the caller
	// never re-derives it. The surplus scan runs high edge to low so a tie on
	// the surplus keeps the STRONGER edge, which is the more informative half
	// of the pair.
	inline bool LightFloorAddLight(LightFloor& F, const std::string& LightId,
	                               const LightDelta& D)
	{
		++F.Lights;
		if (!F.bHaveControl || !D.Comparable) { return false; }
		const int ReadAt = LightReadEdge(F.Control, D);
		if (ReadAt >= 0) { ++F.Read; }
		for (int E = LightDelta::Edges - 1; E >= 0; --E)
		{
			const long long Surplus = D.RoseAtLeast[E] - F.Control.MovedAtLeast[E];
			const long long BestSoFar = F.BestLightPx - F.BestCtrlPx;
			if (F.bHaveBest && Surplus <= BestSoFar) { continue; }
			F.bHaveBest  = true;
			F.BestId     = LightId;
			F.BestEdge   = E;
			F.BestLightPx = D.RoseAtLeast[E];
			F.BestCtrlPx  = F.Control.MovedAtLeast[E];
			F.BestMeanFull = D.MeanDeltaFull;
		}
		return ReadAt >= 0;
	}

	// ONE LINE PER PROBED LIGHT. Status is the caller's, because a light that
	// was already off in this condition, a probe the budget cut, and a probe
	// whose frame would not decode are three different facts and none of them
	// is a light that contributed nothing.
	//
	// `lightIndex` is 1-based and carries its denominator so a truncated
	// series is visible from any one line.
	inline std::string LightDeltaLine(const std::string& LightId, const std::string& Kind,
	                                  int Index, int OfN, const std::string& ShotId,
	                                  const std::string& CameraId, const std::string& ConditionId,
	                                  const std::string& Status, const LightDelta& D,
	                                  const std::string& Note)
	{
		char Head[420];
		std::snprintf(Head, sizeof(Head),
			"light %s kind=%s lightIndex=%d/%d shot=%s camera=%s condition=%s lightStatus=%s",
			LightId.c_str(), Kind.c_str(), Index, OfN, ShotId.c_str(),
			CameraId.c_str(), ConditionId.c_str(), Status.c_str());
		std::string Out(Head);
		if (!D.Comparable)
		{
			Out += " lightDelta=NOTHING-MEASURED lightDeltaNote=";
			Out += (Note.empty() ? std::string("no-comparable-pair") : Note);
			return Out;
		}
		char Body[1400];
		const int Needed = std::snprintf(Body, sizeof(Body),
			" deltaStat=luma-on-minus-off/per-pixel "
			"region=full deltaMeanFull=%.5f meanOnFull=%.5f meanOffFull=%.5f "
			"peakRegion=c%dr%d/of%dx%d peakRegionPx=x%d..%d/y%d..%d "
			"deltaMeanPeak=%.5f meanOnPeak=%.5f meanOffPeak=%.5f "
			"deltaMaxRise=%.5f deltaMaxDrop=%.5f "
			"deltaCodeEdges=1/2/4/8/16/32 deltaPixelsRoseAtLeast=%lld/%lld/%lld/%lld/%lld/%lld "
			"deltaPixelsMovedAtLeast=%lld/%lld/%lld/%lld/%lld/%lld "
			"deltaPixelsOf=%lld deltaHistStat=pixel-count-with-luma-rise-at-or-above-edge-in-8bit-codes "
			"deltaMovedHistStat=same-edges-on-absolute-luma-change-either-direction/this-is-what-a-"
			"control-floors-with "
			"deltaPixelsDarkerWithLightOn=%lld/%lld "
			"deltaDarkerRule=auto-exposure-suspected-if-large lightDeltaNote=%s",
			D.MeanDeltaFull, D.MeanOnFull, D.MeanOffFull,
			D.PeakCol, D.PeakRow, D.Cols, D.Rows,
			D.PeakX0, D.PeakX1, D.PeakY0, D.PeakY1,
			D.PeakMeanDelta, D.PeakMeanOn, D.PeakMeanOff,
			D.MaxRise, D.MaxDrop,
			D.RoseAtLeast[0], D.RoseAtLeast[1], D.RoseAtLeast[2],
			D.RoseAtLeast[3], D.RoseAtLeast[4], D.RoseAtLeast[5],
			D.MovedAtLeast[0], D.MovedAtLeast[1], D.MovedAtLeast[2],
			D.MovedAtLeast[3], D.MovedAtLeast[4], D.MovedAtLeast[5],
			D.Pixels, D.PixelsDarkerWithLightOn, D.Pixels,
			(Note.empty() ? "none" : Note.c_str()));
		Out += Body;
		// QUEUE 310'S RULE, APPLIED RATHER THAN HOPED: snprintf truncates in
		// SILENCE and a cut line reads as a short one, which is what a key
		// that was never emitted looks like. The series this buffer was sized
		// from is printed by frame-stats-test.cpp on every run; the longest
		// light line in the committed run 47 verdict is 704 characters and
		// this body is the larger part of it.
		if (Needed < 0 || (size_t)Needed >= sizeof(Body))
		{
			Out += " lightLineCut=yes/at-1400-chars";
		}
		return Out;
	}

	// ---- QUEUE 326 (b): WHAT EXPOSURE THE PAIR WAS PHOTOGRAPHED UNDER ----
	//
	// Every probed shot on run 47 ran shotExposurePin=AUTO reading back
	// 0.0300/8.0000, and every light line on that run carried
	// deltaPixelsDarkerWithLightOn beside a rule that says in as many words
	// `auto-exposure-suspected-if-large` - 332097 of 921600 at camA. A reader
	// holding one light line could not tell an exposure artefact from a
	// light, because the two halves of that sentence were on different lines.
	// They ride together now.
	//
	// THE WORD IS NOT DECIDED HERE. LedgerVignette::ExposurePinWord is the
	// one implementation of that idea in this tree and this header cannot
	// see it, so the .cpp hands the answer across and this only names and
	// formats it. Its own key prefix, `lightExposurePin*`, because the shot
	// line's `shotExposurePin*` counts shots and a second family under the
	// same names would make every one of them ambiguous across a file that
	// holds both.
	struct LightPin
	{
		std::string Word;               // ExposurePinWord's answer, handed across
		bool   bRead = false;           // did a camera component answer at all
		double ReadMin = 0.0, ReadMax = 0.0;
		LightPin() : Word("NOT-READ") {}
	};

	inline std::string LightPinSegment(const LightPin& P)
	{
		// 420 AND NOT 220: g++ -Wformat-truncation reads the pin word as up
		// to 256 characters and said so, which is the buffer series being
		// printed by the compiler rather than guessed at by the author.
		char Buf[420];
		char Read[64];
		if (P.bRead) { std::snprintf(Read, sizeof(Read), "%.4f/%.4f", P.ReadMin, P.ReadMax); }
		else         { std::snprintf(Read, sizeof(Read), "nothing-measured/nothing-measured"); }
		std::snprintf(Buf, sizeof(Buf),
			"lightExposurePin=%s lightExposurePinRead=%s "
			"lightExposurePinStat=per-light-line/the-shots-own-pin-word-and-clamp-range-read-back-"
			"after-the-write/read-it-beside-deltaPixelsDarkerWithLightOn",
			P.Word.empty() ? "NOT-READ" : P.Word.c_str(), Read);
		return std::string(Buf);
	}

	// ---- QUEUE 326 (a): THIS LIGHT AGAINST ITS OWN SHOT'S CONTROL --------
	//
	// THE PAIR IS ON ONE LINE AT ONE EDGE. lightVsFloorPx carries the light's
	// count and the control's count at the SAME code edge, so the number and
	// the thing it had to beat cannot be greped apart into two moments.
	// bIsControl is the caller's: the control is the floor and cannot be
	// measured against itself, and printing 0 for it would read as a light
	// that failed.
	inline std::string LightFloorSegment(const LightFloor& F, const LightDelta& D,
	                                     bool bIsControl)
	{
		char Buf[420];
		if (bIsControl)
		{
			// A CONTROL THAT NEVER MEASURED IS NOT THE FLOOR. The .cpp emits a
			// control line with Seq = -1 for a shot whose REFERENCE never
			// decoded, and that line carries lightDelta=NOTHING-MEASURED;
			// IS-THE-FLOOR beside it names a floor that does not exist, on the
			// one line a reader goes to for the floor. Reachable in the live
			// rig today, so it is planted rather than argued.
			if (!D.Comparable)
			{
				std::snprintf(Buf, sizeof(Buf),
					"lightAboveFloor=nothing-measured/the-control-did-not-measure-so-this-shot-has-"
					"no-floor lightAboveFloorEdge=nothing-measured "
					"lightVsFloorPx=nothing-measured");
				return std::string(Buf);
			}
			std::snprintf(Buf, sizeof(Buf),
				"lightAboveFloor=IS-THE-FLOOR lightAboveFloorEdge=not-applicable/this-line-is-the-"
				"control lightVsFloorPx=not-applicable/this-line-is-the-control");
			return std::string(Buf);
		}
		if (!F.bHaveControl || !D.Comparable)
		{
			std::snprintf(Buf, sizeof(Buf),
				"lightAboveFloor=nothing-measured/%s lightAboveFloorEdge=nothing-measured "
				"lightVsFloorPx=nothing-measured",
				F.bHaveControl ? "this-light-has-no-comparable-delta"
				               : "this-shot-has-no-comparable-control");
			return std::string(Buf);
		}
		const int E = LightReadEdge(F.Control, D);
		// THE EDGE A NO IS REPORTED AT is the strongest one, 32 code values,
		// because that is where a light with any real contribution is least
		// likely to be buried; the whole histogram is on the same line for a
		// reader who wants the rest.
		const int At = (E >= 0) ? E : (LightDelta::Edges - 1);
		std::snprintf(Buf, sizeof(Buf),
			"lightAboveFloor=%s lightAboveFloorEdge=%dcodes "
			"lightVsFloorPx=%lld..vs..%lld "
			"lightAboveFloorRule=this-lights-pixels-risen-at-that-edge-strictly-exceed-the-pixels-"
			"this-shots-own-control-MOVED-at-it/integer-counts/no-epsilon/YES-names-the-highest-"
			"edge-it-won-at-and-NO-reports-the-32-code-edge",
			(E >= 0) ? "YES" : "NO", DeltaCodeEdge(At),
			D.RoseAtLeast[At], F.Control.MovedAtLeast[At]);
		return std::string(Buf);
	}

	// ---- QUEUE 326 (c): ONE LINE PER PROBED SHOT -------------------------
	//
	// PER-SHOT NUMBERS ON THE PER-SHOT LINE. The count of lights that read is
	// true of THIS shot and of no other, and run 47 is the reason it cannot
	// live only on the done line: four of its six shots had no usable floor
	// and two did, and a single whole-run count cannot say that.
	//
	// A NO-READ CARRIES BOTH NUMBERS. A shot whose control beat every light
	// is not a shot with zero lights working; it is a shot that measured
	// nothing about its lights, and the two numbers that say so are the
	// control's own whole-frame movement and the closest a light came to it.
	inline std::string LightFloorLine(const LightFloor& F)
	{
		char Head[320];
		const int HeadNeeded = std::snprintf(Head, sizeof(Head),
			"lightfloor shot=%s camera=%s condition=%s lightFloorVerdict=%s",
			F.ShotId.c_str(), F.CameraId.c_str(), F.ConditionId.c_str(),
			!F.bHaveControl ? "NO-CONTROL" : (F.Read > 0 ? "FLOOR-USABLE" : "NO-READ"));
		const bool bHeadCut = (HeadNeeded < 0 || (size_t)HeadNeeded >= sizeof(Head));
		std::string Out(Head);
		if (!F.bHaveControl)
		{
			Out += " lightsReadThisShot=nothing-measured/";
			char N[48]; std::snprintf(N, sizeof(N), "%d", F.Lights);
			Out += N;
			Out += " lightFloorCtrl=nothing-measured/no-comparable-control-frame-for-this-shot";
			if (bHeadCut) { Out += " lightFloorLineCut=yes/at-320-chars-of-head"; }
			return Out;
		}
		// THE LIGHT ID IS THE ONE UNBOUNDED INPUT AND IT IS NOT CAPPED HERE.
		// A second cap of its own would truncate it silently BEFORE the body
		// buffer ever saw it, which would leave the body's announcer unable to
		// fire at all - a guard that cannot fire is a comment. So the id goes
		// in as a string and the body's single cap is the one that announces.
		std::string Best;
		if (F.bHaveBest)
		{
			char T[160];   // bounded: an edge, two pixel counts and a mean
			std::snprintf(T, sizeof(T),
				"/at%dcodes lightFloorBestPx=%lld..vs..%lld lightFloorBestMeanFull=%+.5f",
				DeltaCodeEdge(F.BestEdge), F.BestLightPx, F.BestCtrlPx, F.BestMeanFull);
			Best = "lightFloorBest=" + F.BestId + T;
		}
		else
		{
			Best = "lightFloorBest=nothing-measured/no-comparable-light-in-this-shot "
			       "lightFloorBestPx=nothing-measured lightFloorBestMeanFull=nothing-measured";
		}
		// 1100 FROM A PRINTED SERIES, NOT FROM A GUESS. At the real frame
		// width this body measures 678 characters (frame-stats-test.cpp
		// prints it on every run as floorLineChars, head plus body); 820
		// would have left seventeen per cent, which is one added key.
		char Buf[1100];
		const int Needed = std::snprintf(Buf, sizeof(Buf),
			" lightsReadThisShot=%d/%d lightFloorCtrlMeanFull=%+.5f "
			"lightFloorCtrlMovedAtLeast=%lld/%lld/%lld/%lld/%lld/%lld "
			"lightFloorCtrlDarker=%lld/%lld lightFloorCtrlPxOf=%lld "
			"lightFloorCodeEdges=1/2/4/8/16/32 %s "
			"lightFloorStat=per-shot/lightsReadThisShot-is-the-count-of-this-shots-lights-whose-"
			"risen-pixels-beat-this-shots-own-control-at-some-code-edge/lightFloorBest-is-the-"
			"largest-surplus-found-and-its-two-counts-are-at-the-one-edge-that-surplus-is-AT/"
			"a-NO-READ-shot-measured-nothing-about-its-lights-and-is-not-a-shot-with-no-lights-"
			"working",
			F.Read, F.Lights, F.Control.MeanDeltaFull,
			F.Control.MovedAtLeast[0], F.Control.MovedAtLeast[1], F.Control.MovedAtLeast[2],
			F.Control.MovedAtLeast[3], F.Control.MovedAtLeast[4], F.Control.MovedAtLeast[5],
			F.Control.PixelsDarkerWithLightOn, F.Control.Pixels, F.Control.Pixels,
			Best.c_str());
		Out += Buf;
		// BOTH HALVES OF THE LINE ARE WATCHED, and the marker names which one
		// bit: a cut head loses the shot id and a cut body loses the counts,
		// and both read as a line that simply did not carry them.
		if (bHeadCut)                                       { Out += " lightFloorLineCut=yes/at-320-chars-of-head"; }
		if (Needed < 0 || (size_t)Needed >= sizeof(Buf))    { Out += " lightFloorLineCut=yes/at-1100-chars-of-body"; }
		return Out;
	}

	// THE WHOLE-RUN SUMMARY FOR THE LIGHT PASS, on its own line, carrying
	// only numbers that are true of the RUN. A pass that probed nothing says
	// the words instead of printing 0/0 as though it had looked.
	//
	// `lightsAboveFloor` REPLACES `lightsReachedFrame`, RENAMED BY THE RULING
	// OF 2026-09-16 03:27Z, and the rename is the finding. The old key counted
	// every probed light whose `RoseAtLeast[0]` was above zero, one pixel
	// rising by one code value, over every light probed. This one counts the
	// lights that beat their OWN shot's control at some code edge, over the
	// lights probed in shots WITH A USABLE FLOOR. Rule and denominator both
	// changed, so the two are one series under one name only to a grep, and
	// the evidence channel here is a committed file with a git history of the
	// same path: a key-grep over it would have plotted two instruments on one
	// axis. No tombstone key, because `lightProbeStatus` on this same line
	// already says whether the pass ran; the old name is gone and the test
	// asserts it ABSENT on every done line it builds.
	//
	// APPLIED TO RUN 47'S COMMITTED NUMBERS, from the ruling's own per-shot
	// table read off verdict lines 275 to 322: three of six probed shots
	// usable, six of twenty-one certain and at most twelve of twenty-one,
	// twenty-one of forty-two lights in NO-READ shots, where the line said
	// 30 of 42. AND FOUR OF THOSE SIX CERTAIN READS ARE BLANK PROBE FRAMES,
	// which this rule cannot see: a probe frame that came back blank
	// differences against the reference as the whole reference, the largest
	// surplus any light can show, and the control floor catches a blank
	// CONTROL but not a blank LIGHT frame under a good control. Queue item A
	// refuses them by the shot line's own structural Blank rule. Until it
	// lands, R is not a number to report.
	inline std::string LightProbeDoneLine(int Probed, int Eligible,
	                                      const std::vector<LightFloor>& Floors,
	                                      int SkippedAlreadyOff, int SkippedBudget,
	                                      int NoFile, int RestoreMismatch,
	                                      int ShotsProbed, int ShotsAsked,
	                                      double BudgetSeconds, double SpentSeconds,
	                                      int FramesBeforeShot, int Controls)
	{
		// THE TALLY IS TAKEN HERE AND NOWHERE ELSE, so the per-shot lines and
		// the run line cannot disagree: both are reductions of the same
		// vector, and the .cpp no longer counts anything about reads.
		//
		// THREE BUCKETS AND NOT TWO. A shot whose control never measured is not
		// a shot whose control swamped its lights, and folding the first into
		// NO-READ put a word on the run line that the per-shot line refutes:
		// `lightFloorShotStat` says NO-READ means the control beat the lights,
		// which is false of a shot that had no control to beat them with.
		// Every floor lands in exactly one of the three, so a + b + c is the
		// floor count and a reader can check it against the `lightfloor` lines.
		int ShotsUsable = 0, ShotsNoRead = 0, ShotsNoControl = 0;
		int Reached = 0, InUsable = 0, InNoRead = 0, InNoControl = 0;
		// THE WORST FLOOR AND ITS SHOT'S OWN BEST LIGHT, CAPTURED AT THE SAME
		// INSTANT AND NAMED SO. The control's whole-frame movement is the
		// numerator's floor, so the light printed beside it is that shot's,
		// never the run's best light from somewhere else.
		const LightFloor* Worst = 0;
		for (size_t I = 0; I < Floors.size(); ++I)
		{
			const LightFloor& F = Floors[I];
			if (LightFloorUsable(F)) { ++ShotsUsable;    InUsable    += F.Lights; Reached += F.Read; }
			else if (F.bHaveControl) { ++ShotsNoRead;    InNoRead    += F.Lights; }
			else                     { ++ShotsNoControl; InNoControl += F.Lights; }
			if (!F.bHaveControl) { continue; }
			double Mag = F.Control.MeanDeltaFull; if (Mag < 0) { Mag = -Mag; }
			double Cur = Worst ? Worst->Control.MeanDeltaFull : 0.0; if (Cur < 0) { Cur = -Cur; }
			if (Worst == 0 || Mag > Cur) { Worst = &F; }
		}
		char Reach[96];   // bounded: two counts, or one fixed phrase and a count
		if (Probed == 0 || Floors.empty())
		{
			std::snprintf(Reach, sizeof(Reach), "nothing-measured/no-shot-carried-a-floor-pass");
		}
		else if (ShotsUsable == 0)
		{
			// R/U MAY NOT PRINT 0/0 OVER A SET NO SHOT COULD HAVE READ FROM.
			// With no usable floor anywhere, InUsable is zero by construction,
			// and `0/0` is the shape rule 3b refuses: it cannot be told apart
			// from a run whose lights all failed against a floor that worked.
			std::snprintf(Reach, sizeof(Reach),
			              "nothing-measured/no-usable-floor-in-any-of-%d-shots", (int)Floors.size());
		}
		else
		{
			std::snprintf(Reach, sizeof(Reach), "%d/%d", Reached, InUsable);
		}
		// CONDITION C5: THE WORST SEGMENT IS A STRING, NOT A PRE-CAP. It was
		// two fixed buffers, and each carried an UNBOUNDED id: a shot id
		// through a 300-byte buffer and a light id through a 40-byte one, both
		// truncating in silence before the done line's own 1500-character
		// announcer could ever see the overflow. That is the fault the comment
		// in LightFloorLine names and avoids for `Best`, applied at one site
		// and not the other. The ids go in as strings and only the two means
		// go through a bounded snprintf, so the line has ONE cap and that cap
		// announces.
		std::string WorstSeg;
		if (Worst == 0)
		{
			WorstSeg = "lightFloorWorstShot=nothing-measured "
			           "lightFloorWorstCtrlMeanFull=nothing-measured "
			           "lightFloorBestLightMeanFullAtWorst=nothing-measured";
		}
		else
		{
			char CtrlMean[48];   // bounded: one mean
			std::snprintf(CtrlMean, sizeof(CtrlMean), "%+.5f", Worst->Control.MeanDeltaFull);
			WorstSeg  = "lightFloorWorstShot=" + Worst->ShotId;
			WorstSeg += " lightFloorWorstCtrlMeanFull=";
			WorstSeg += CtrlMean;
			WorstSeg += " lightFloorBestLightMeanFullAtWorst=";
			if (Worst->bHaveBest)
			{
				char BestMean[48];   // bounded: one mean
				std::snprintf(BestMean, sizeof(BestMean), "%+.5f", Worst->BestMeanFull);
				WorstSeg += BestMean;
				WorstSeg += "/";
				WorstSeg += Worst->BestId;
			}
			else
			{
				WorstSeg += "nothing-measured";
			}
		}
		char Buf[1500];
		const int Needed = std::snprintf(Buf, sizeof(Buf),
			"lightProbeStatus=%s lightsProbed=%d/%d lightsAboveFloor=%s "
			"lightsSkippedAlreadyOff=%d lightsSkippedBudget=%d lightProbesNoFile=%d "
			"lightRestoreMismatch=%d/%d controlProbes=%d "
			"lightFloorShotsUsable=%d/%d lightFloorShotsNoRead=%d/%d "
			"lightFloorShotsNoControl=%d/%d "
			"lightsInNoReadShots=%d/%d lightsInNoControlShots=%d/%d %s "
			"shotsProbed=%d/%d lightProbeBudgetSeconds=%.1f lightProbeSpentSeconds=%.1f "
			"lightProbeFramesBeforeShot=%d/same-as-reference "
			"lightProbeMethod=one-light-off-vs-reference/same-camera-condition-framecount "
			"lightsAboveFloorStat=whole-run/count-of-lights-that-beat-their-OWN-shots-control-at-"
			"some-code-edge/denominator-is-lights-probed-in-shots-with-a-usable-floor-and-"
			"lightsInNoReadShots-and-lightsInNoControlShots-are-the-rest-of-lightsProbed/"
			"RENAMED-BY-QUEUE-326-from-lightsReachedFrame-which-counted-one-pixel-rising-by-one-"
			"code-value-through-run-47-and-is-not-comparable "
			"lightFloorShotStat=whole-run/a-shot-is-usable-when-at-least-one-of-its-lights-beat-its-"
			"own-control-and-NO-READ-means-the-control-swamped-them-not-that-the-lights-are-dark",
			Probed == 0 ? "NOTHING-MEASURED" : (SkippedBudget > 0 ? "PARTIAL-BUDGET-BIT" : "ALL"),
			Probed, Eligible, Reach,
			SkippedAlreadyOff, SkippedBudget, NoFile,
			RestoreMismatch, Probed, Controls,
			ShotsUsable, (int)Floors.size(), ShotsNoRead, (int)Floors.size(),
			ShotsNoControl, (int)Floors.size(),
			InNoRead, Probed, InNoControl, Probed, WorstSeg.c_str(),
			ShotsProbed, ShotsAsked, BudgetSeconds, SpentSeconds, FramesBeforeShot);
		std::string Out(Buf);
		if (Needed < 0 || (size_t)Needed >= sizeof(Buf))
		{
			Out += " lightProbeDoneLineCut=yes/at-1500-chars";
		}
		return Out;
	}
}

// ============================================================================
// QUEUE 186: THE STREET HAS NO SKY, AND NOTHING PRINTS WHAT THE SKY IS.
//
// WHAT THIS EXISTS FOR. On 2026-09-09 the UE verdict carried
// skyModel=none-black as a HARDCODED STRING in a format literal, and the
// frames refute it: the top of ue-vign_camA_day.png measures 249.5/250.0/250.5
// mean RGB over 8858 pixels, which is a near-white field and not a black one.
// The string described what the author believed. Worse, the two conditions'
// backgrounds carry their own fog inscattering colour's CHANNEL ORDER: the day
// band reads R<G<B against a day fog colour of 0.55/0.58/0.62, and the night
// band reads R>G=B against a night fog colour of 0.06/0.05/0.05. The
// background is the height fog at the far plane, blown up by auto exposure,
// and nothing in the run said so.
//
// So this section prints WHAT THE SKY IS IN THE FRAME. A key that says what
// was asked for cannot catch a sky that never arrived; a band of pixels read
// out of the committed file can.
//
// WHAT EACH NUMBER IS A STATISTIC OF, and every one is per-frame:
//   Pixels      pixels inside this band in THIS image, its own denominator
//   MeanLuma    mean over those pixels, 0 to 1, the Unity sim's weights
//   P05/P50/P95 order statistics over those same pixels
//   Spread      P95 minus P05, the band's own within-band variation
//   MeanR/G/B   channel means 0..255, because a fog colour and a sky colour
//               are told apart by their channel ORDER and a luma cannot see it
//   ClipHiAny   count of pixels with any channel at 255, over Pixels
//
// NO BOUND IS SET HERE AND NONE MAY BE. There is no series yet. The reference
// numbers a bound would eventually come from are recorded in the report of
// 2026-09-09, measured off Codex's Hook panel with these same weights: its sky
// region reads meanLuma 0.7514 with p50 0.8075 over 48800 px, and its near wet
// road reads meanLuma 0.5321 with spread 0.4318 over 39000 px. Those are the
// reference's numbers, not ours, and they are written in a comment rather than
// in code precisely so that nothing here can compare against them by accident.
// ============================================================================

namespace LedgerFrame
{
	struct BandStats
	{
		// false means the band had no pixels: nothing measured is not the
		// same as measured and dark, and neither may read as the other.
		bool        Measured = false;
		std::string Name     = "unnamed";
		int         X0 = 0, Y0 = 0, X1 = 0, Y1 = 0;
		long long   Pixels    = 0;
		double      MeanLuma  = 0.0;
		double      P05 = 0.0, P50 = 0.0, P95 = 0.0;
		double      MeanR = 0.0, MeanG = 0.0, MeanB = 0.0;
		long long   ClipHiAny = 0;
		// ---- A2, 2026-09-09: THE TWO RAILS AND THE SORTED SAMPLE ---------
		//
		// RailLo counts pixels with every channel at 0 and RailHi is
		// ClipHiAny by another name, any channel at 255. They are the
		// VALIDITY DENOMINATOR of any rank claim made about this band: a
		// tonemap plus 8-bit quantisation is strictly monotone in the middle
		// and FLAT at both ends, so at the rails the order between two
		// scene values is not preserved and an invariance claim stops being
		// true there. Printed beside the rank key always, per rule 3b.
		long long   RailLo = 0;
		// THE BAND'S OWN LUMA SAMPLE, SORTED, KEPT so a rank comparison
		// against another band of the SAME frame can be counted without a
		// second pass over the image. About 1.5 MB for a ground band at
		// 1280x720 and freed with the struct.
		std::vector<double> Sorted;
	};

	// A BAND OF ONE FRAME, GIVEN AS FRACTIONS OF THE FRAME so one call site
	// serves every resolution this project shoots at. The rectangle is
	// clamped to the image and PRINTED IN PIXELS, because a fraction that
	// rounded to an empty rectangle and a band that is genuinely empty are
	// different faults and the pixel rectangle separates them.
	inline BandStats MeasureBand(const unsigned char* Bgra, int W, int H,
	                             const char* Name,
	                             double Fx0, double Fy0, double Fx1, double Fy1)
	{
		BandStats S;
		S.Name = (Name != 0 && Name[0] != '\0') ? Name : "unnamed";
		if (Bgra == 0 || W <= 0 || H <= 0) { return S; }
		int X0 = (int)(Fx0 * (double)W), X1 = (int)(Fx1 * (double)W);
		int Y0 = (int)(Fy0 * (double)H), Y1 = (int)(Fy1 * (double)H);
		if (X0 < 0) { X0 = 0; }
		if (Y0 < 0) { Y0 = 0; }
		if (X1 > W) { X1 = W; }
		if (Y1 > H) { Y1 = H; }
		S.X0 = X0; S.Y0 = Y0; S.X1 = X1; S.Y1 = Y1;
		if (X1 <= X0 || Y1 <= Y0) { return S; }
		std::vector<double> L;
		L.reserve((size_t)((X1 - X0) * (Y1 - Y0)));
		double SumR = 0.0, SumG = 0.0, SumB = 0.0;
		for (int Y = Y0; Y < Y1; ++Y)
		{
			for (int X = X0; X < X1; ++X)
			{
				const long long P = (long long)Y * (long long)W + (long long)X;
				const unsigned char B = Bgra[P * 4];
				const unsigned char G = Bgra[P * 4 + 1];
				const unsigned char R = Bgra[P * 4 + 2];
				if (R == 255 || G == 255 || B == 255) { ++S.ClipHiAny; }
				if (R == 0 && G == 0 && B == 0) { ++S.RailLo; }
				SumR += (double)R; SumG += (double)G; SumB += (double)B;
				L.push_back(Luma(R, G, B));
			}
		}
		S.Measured = true;
		S.Pixels = (long long)L.size();
		std::sort(L.begin(), L.end());
		double Sum = 0.0;
		for (size_t I = 0; I < L.size(); ++I) { Sum += L[I]; }
		S.MeanLuma = Sum / (double)L.size();
		// INDEXED, NOT INTERPOLATED, and clamped so a one-pixel band cannot
		// index past the end. The same convention tools/road-brightness.py
		// uses, so the two rulers agree on what a p95 is.
		size_t I05 = (size_t)(0.05 * (double)L.size());
		size_t I50 = (size_t)(0.50 * (double)L.size());
		size_t I95 = (size_t)(0.95 * (double)L.size());
		if (I05 >= L.size()) { I05 = L.size() - 1; }
		if (I50 >= L.size()) { I50 = L.size() - 1; }
		if (I95 >= L.size()) { I95 = L.size() - 1; }
		S.P05 = L[I05]; S.P50 = L[I50]; S.P95 = L[I95];
		S.MeanR = SumR / (double)L.size();
		S.MeanG = SumG / (double)L.size();
		S.MeanB = SumB / (double)L.size();
		// SORTED ALREADY, HANDED ON AS IT IS. The rank key below counts
		// against a threshold taken from ANOTHER BAND OF THE SAME FRAME, and
		// a sorted sample answers that by binary search rather than by a
		// second pass over the image.
		S.Sorted = L;
		return S;
	}

	// THE BANDS THIS PROJECT READS, AS FRACTIONS, NAMED ONCE HERE.
	//
	// WHY A BAND AND NOT A MASK. Nothing in this run knows which pixels are
	// sky; a depth-aware mask is a second measurement and this is the first.
	// So the bands are geometric, they are NAMED for what they cover rather
	// than for what is hoped to be in them, and the name travels with every
	// number. skyTop is the top eighth full width and in these cameras it
	// carries roofline and building as well as sky; skyCentre is the middle
	// fifth of that band, which in cam_A and cam_hook is sky and nothing
	// else. Reading both is what stops a dark roofline being reported as a
	// dark sky.
	inline double SkyTopY1()     { return 0.125; }
	inline double SkyCentreX0()  { return 0.400; }
	inline double SkyCentreX1()  { return 0.600; }
	// The bottom fifth, full width, which in every camera here is ground.
	inline double GroundY0()     { return 0.800; }

	// PER-SAMPLE KEYS ONLY. Every number on this line is a statistic of THIS
	// frame, and a band with no pixels prints the words rather than zeros
	// that would read as a black sky.
	inline std::string BandLine(const BandStats& S)
	{
		if (!S.Measured || S.Pixels == 0)
		{
			char Empty[300];
			std::snprintf(Empty, sizeof(Empty),
				"band.%s=NOTHING-MEASURED band.%s.rectPx=%d/%d/%d/%d "
				"band.%s.why=no-pixels-in-this-rectangle/not-a-dark-band",
				S.Name.c_str(), S.Name.c_str(), S.X0, S.Y0, S.X1, S.Y1,
				S.Name.c_str());
			return std::string(Empty);
		}
		char Buf[700];
		std::snprintf(Buf, sizeof(Buf),
			"band.%s=MEASURED band.%s.px=%lld band.%s.rectPx=%d/%d/%d/%d "
			"band.%s.meanLuma=%.4f band.%s.p05=%.4f band.%s.p50=%.4f band.%s.p95=%.4f "
			"band.%s.spread=%.4f band.%s.meanRGB=%.1f/%.1f/%.1f "
			"band.%s.clipHiAny=%lld/%lld",
			S.Name.c_str(), S.Name.c_str(), S.Pixels,
			S.Name.c_str(), S.X0, S.Y0, S.X1, S.Y1,
			S.Name.c_str(), S.MeanLuma, S.Name.c_str(), S.P05,
			S.Name.c_str(), S.P50, S.Name.c_str(), S.P95,
			S.Name.c_str(), S.P95 - S.P05,
			S.Name.c_str(), S.MeanR, S.MeanG, S.MeanB,
			S.Name.c_str(), S.ClipHiAny, S.Pixels);
		return std::string(Buf);
	}

	// ========================================================================
	// A2, RULED 2026-09-09: THE TWO STATISTICS THAT SURVIVE A MOVING EXPOSURE,
	// AND THE WORD "INVARIANT" IS NOT FREE.
	//
	// WHAT WENT WRONG FIRST. Every cross-frame number this rig has printed is
	// void: run 38 photographed eleven frames under unsnapped histogram auto
	// exposure (ppAutoExposureMethod=0, cvarDefaultAutoExposure=1), and its
	// own null pair, two shots of the SAME condition at the SAME camera,
	// differ by 0.1106 of whole-frame mean luma. A number from this rig is
	// worth something only if it is a comparison INSIDE one photograph.
	//
	// AND THE CORRECTION THAT DECIDES THESE KEYS. A ratio is NOT invariant
	// under this tonemapper. "A difference scales with k and a ratio does
	// not" is true of a linear multiplier and false of what runs here, which
	// is an exposure multiply followed by a filmic curve. That curve is
	// MONOTONE, NOT LINEAR: under a monotone map a ratio moves, a difference
	// moves, and what survives EXACTLY is ORDER. So there are three classes
	// and every key below says which one it is in:
	//
	//   ABSOLUTE          a luma, a percentile, a mean. May be printed, may
	//                     NOT be compared across cells.
	//   ROBUST            a within-frame ratio. Moves with exposure, far less
	//                     than either end does. Quotable across cells only
	//                     when the null cell says the exposure held.
	//   EXACTLY INVARIANT a RANK statistic, meaning a quantity whose
	//                     definition mentions only comparisons between pixels
	//                     of the SAME frame.
	//
	// AND THE EXCEPTIONS ARE NAMED RATHER THAN IMPLIED, because "invariant"
	// with no exceptions is the claim this project refuses: bloom, a lens
	// vignette, grain and LOCAL tonemapping are not whole-frame monotone
	// curves, and a rank statistic is not invariant under any of them.
	// ========================================================================

	// THE ROBUST RATIO, p95 OVER p05, OF THE GROUND BAND OF ONE FRAME.
	//
	// It is the statistic the reference gap is largest on: the reference
	// street reads ground p05 0.1932 and p95 0.7281, a ratio of 3.77, and the
	// frame this rig ships reads 0.5785 and 0.9304, a ratio of 1.61. Our road
	// is three times brighter at the dark end and carries under half the
	// contrast. Those four numbers are recorded in the ruling of 2026-09-09
	// and are NOT in code, so nothing here can compare against them by
	// accident.
	inline std::string GroundRobustRatioKeys(const BandStats& Ground)
	{
		const std::string N = "band." + Ground.Name;
		std::string Out;
		if (!Ground.Measured || Ground.Pixels == 0 || Ground.P05 <= 0.0)
		{
			Out += N + ".p95OverP05=NOTHING-MEASURED";
			Out += " " + N + ".p95OverP05Why=";
			Out += (!Ground.Measured || Ground.Pixels == 0)
			     ? "no-pixels-in-this-band/not-a-flat-band"
			     : "the-p05-of-this-band-is-zero/a-ratio-over-a-rail-is-not-a-contrast";
		}
		else
		{
			char Buf[64];
			std::snprintf(Buf, sizeof(Buf), "%.4f", Ground.P95 / Ground.P05);
			Out += N + ".p95OverP05=" + Buf;
		}
		Out += " " + N + ".p95OverP05Stat=within-one-frame-ratio-of-two-indexed-order-statistics/"
		       "not-interpolated/ROBUST-NOT-INVARIANT/"
		       "a-tonemap-is-monotone-not-linear-so-this-moves-when-the-exposure-moves/"
		       "quotable-across-cells-only-when-the-null-cell-held";
		return Out;
	}

	// THE RANK KEY, AND ITS DEFINITION MENTIONS ONLY COMPARISONS BETWEEN
	// PIXELS OF THE SAME FRAME, which is the one rule the ruling set on it.
	//
	//   darkerThanSkyMedianPct = the percentage of GROUND band pixels whose
	//   luma is strictly below the MEDIAN PIXEL OF THE skyCentre BAND OF THE
	//   SAME FRAME.
	//
	// WHY THIS ONE. Exposure and a filmic curve move every luma in the frame
	// through one strictly monotone map, and a strictly monotone map cannot
	// reorder two pixels: if a road pixel was darker than the sky's middle
	// pixel before the curve, it is darker after. So this number is EXACTLY
	// the same under any exposure the rig drifts to, which no percentile and
	// no mean on this line can claim. What it measures is the thing the grid
	// is being read for: how much of the road sits below the sky, which is
	// what a picture with a dark end in it has and ours has not.
	//
	// WHERE THE CLAIM STOPS BEING TRUE, PRINTED BESIDE IT ALWAYS:
	//   Ties   ground pixels EXACTLY AT the threshold. The comparison is
	//          strict, so a tie falls outside the count, and 8-bit
	//          quantisation is what makes ties exist at all.
	//   Rails  ground pixels at the bottom of the range (every channel 0) and
	//          at the top (any channel 255). The curve is FLAT there, not
	//          strictly monotone, so order is not preserved among them.
	// A rank number quoted without these two is a claim without its
	// denominator, which is rule 3b.
	inline std::string GroundRankKeys(const BandStats& Ground, const BandStats& SkyCentre)
	{
		const std::string N = "band." + Ground.Name;
		const std::string Stat =
			" " + N + ".darkerThanSkyMedianPctStat="
			"a-rank-comparison-between-pixels-of-ONE-frame/"
			"EXACTLY-invariant-under-any-strictly-monotone-whole-frame-curve-including-exposure-and-this-tonemap/"
			"NOT-invariant-under-bloom-vignette-grain-or-local-tonemapping-which-are-not-whole-frame-monotone/"
			"threshold-is-the-skyCentre-band-median-pixel-of-the-SAME-frame";
		std::string Out;
		if (!Ground.Measured || Ground.Pixels == 0 || Ground.Sorted.empty()
		    || !SkyCentre.Measured || SkyCentre.Pixels == 0)
		{
			Out += N + ".darkerThanSkyMedianPct=NOTHING-MEASURED";
			Out += " " + N + ".darkerThanSkyMedianPctWhy=";
			Out += (!SkyCentre.Measured || SkyCentre.Pixels == 0)
			     ? "the-skyCentre-band-had-no-pixels-so-there-is-no-threshold-to-rank-against"
			     : "the-ground-band-had-no-pixels-to-rank";
			Out += Stat;
			Out += " " + N + ".darkerThanSkyMedianPctTies=nothing-measured";
			Out += " " + N + ".darkerThanSkyMedianPctRails=nothing-measured";
			return Out;
		}
		const double Threshold = SkyCentre.P50;
		const long long Below = (long long)(std::lower_bound(
			Ground.Sorted.begin(), Ground.Sorted.end(), Threshold) - Ground.Sorted.begin());
		const long long AtOrBelow = (long long)(std::upper_bound(
			Ground.Sorted.begin(), Ground.Sorted.end(), Threshold) - Ground.Sorted.begin());
		const long long Ties = AtOrBelow - Below;
		char Buf[96];
		std::snprintf(Buf, sizeof(Buf), "%.4f", 100.0 * (double)Below / (double)Ground.Pixels);
		Out += N + ".darkerThanSkyMedianPct=" + Buf + "/of=" + std::to_string(Ground.Pixels);
		Out += Stat;
		Out += " " + N + ".darkerThanSkyMedianPctTies=" + std::to_string(Ties)
		     + "/of=" + std::to_string(Ground.Pixels);
		Out += " " + N + ".darkerThanSkyMedianPctRails=" + std::to_string(Ground.RailLo)
		     + "/" + std::to_string(Ground.ClipHiAny)
		     + "/of=" + std::to_string(Ground.Pixels);
		Out += " " + N + ".darkerThanSkyMedianPctTiesRailsStat="
		       "ties-are-ground-pixels-EXACTLY-at-the-threshold-and-the-comparison-is-strict-so-they-are-outside-the-count/"
		       "rails-are-lo-then-hi-where-the-curve-is-flat-rather-than-strictly-monotone-and-the-invariance-claim-does-not-hold";
		return Out;
	}

	// THE THREE BANDS OF ONE SHOT, ON ONE LINE, plus the one derived number
	// that is worth having and its named limit.
	//
	// groundOverSky IS A RATIO OF TWO MEASURED MEANS AND NOTHING ELSE. It
	// does not say the ground reflects the sky: a ground lit by a sky and a
	// ground mirroring a sky both raise it. What separates them is the
	// GROUND BAND'S OWN SPREAD, printed above, because a mirror adds
	// variation and a lamp does not. Said here so the ratio is never read as
	// the answer to the reflection question.
	inline std::string SkyBandLine(const BandStats& SkyTop,
	                               const BandStats& SkyCentre,
	                               const BandStats& Ground)
	{
		std::string Out = BandLine(SkyTop);
		Out += " ";
		Out += BandLine(SkyCentre);
		Out += " ";
		Out += BandLine(Ground);
		Out += " ";
		// A2: THE ROBUST RATIO AND THE RANK KEY, BOTH OF THE GROUND BAND,
		// both per-sample, both on the sample line. Printed before the
		// absolute ratio below so a reader meets the two quotable numbers
		// before the one that is void across cells.
		Out += GroundRobustRatioKeys(Ground);
		Out += " ";
		Out += GroundRankKeys(Ground, SkyCentre);
		Out += " ";
		if (!SkyCentre.Measured || !Ground.Measured
		    || SkyCentre.Pixels == 0 || Ground.Pixels == 0
		    || SkyCentre.MeanLuma <= 0.0)
		{
			Out += "bandGroundOverSky=NOTHING-MEASURED "
			       "bandGroundOverSkyWhy=one-of-the-two-bands-had-no-pixels-or-a-zero-sky";
			return Out;
		}
		char Buf[420];
		std::snprintf(Buf, sizeof(Buf),
			"bandGroundOverSky=%.4f "
			"bandGroundOverSkyStat=ground-band-mean-luma-over-skyCentre-band-mean-luma/one-frame "
			"bandGroundOverSkyLimit=a-lit-ground-and-a-mirroring-ground-both-raise-this/"
			"the-ground-bands-own-spread-is-what-separates-them "
			"bandStat=per-frame-geometric-bands/named-for-what-they-cover-not-for-what-is-in-them",
			Ground.MeanLuma / SkyCentre.MeanLuma);
		Out += Buf;
		return Out;
	}
}

// ============================================================================
// THE RIG'S OWN DETERMINISM, MEASURED RATHER THAN ASSERTED.
//
// WHY THIS EXISTS, AND THE READING THAT MADE IT NECESSARY. Run 38 photographed
// vign_camA_day as shot 1 of 11 and vign_ladder_sun003 as shot 6. Their two
// condition rows differ on `id` and `note` and on nothing else of eleven keys,
// both are cam_A, both read sun 3.000 and sky 1.000 back off the live
// components on their own shot lines, and every one of 921600 pixels differs,
// the later frame darker, whole-frame mean 0.7048 against 0.5942. THE SAME RUN
// SAID WHY, one line further down: `light control_no_toggle` photographs the
// scene a second time with NOTHING TOGGLED, and its two takes differ by 0.0038
// of mean luma with 715552 of 921600 pixels darker in the first. A rig whose
// output depends on when a frame was taken cannot compare frames, which is the
// only thing this rig is for.
//
// SO THE RUN PROVES IT RATHER THAN CLAIMING IT. The probe photographs the
// FIRST shot's camera and condition again as the LAST thing it does, and this
// is the difference between the two. Identical inputs, maximum order
// separation: every other shot, every condition change and every light probe
// stood between them. IDENTICAL is the only reading that lets a cross-shot
// comparison mean anything; any other number says how much of the next
// comparison is the rig rather than the street.
//
// WHAT EACH NUMBER IS A STATISTIC OF, all whole-frame, one per run:
//   DiffPixels     COUNT of pixels differing in any of B, G, R, over Pixels
//   MaxAbsChannel  the WORST single channel difference in 8-bit codes, 0..255
//   MeanLumaFirst  mean luma of the first shot's committed frame
//   MeanLumaRepeat mean luma of the repeat, taken last
//   MeanLumaDelta  repeat MINUS first, so a negative number means the rig
//                  drifted DARKER over the run
namespace LedgerFrame
{
	struct RepeatDiff
	{
		bool      Comparable;        // two decoded frames of equal, non-zero size
		long long Pixels;            // the denominator, pixels examined
		long long DiffPixels;        // of those, how many differ in any channel
		int       MaxAbsChannel;     // worst channel difference, 8-bit codes
		double    MeanLumaFirst;
		double    MeanLumaRepeat;
		double    MeanLumaDelta;     // repeat minus first
		RepeatDiff() : Comparable(false), Pixels(0), DiffPixels(0), MaxAbsChannel(0),
		               MeanLumaFirst(0.0), MeanLumaRepeat(0.0), MeanLumaDelta(0.0) {}
	};

	// First and Repeat are BGRA8 buffers of the SAME dimensions, top row
	// first. Different dimensions is not a small problem to paper over: it
	// means the two are not the same frame and Comparable stays false, which
	// prints the words rather than a zero that would read as agreement.
	inline RepeatDiff MeasureRepeat(const unsigned char* First,
	                                const unsigned char* Repeat, int W, int H)
	{
		RepeatDiff D;
		if (First == 0 || Repeat == 0 || W <= 0 || H <= 0) { return D; }
		D.Comparable = true;
		D.Pixels = (long long)W * (long long)H;
		double SumA = 0.0, SumB = 0.0;
		for (long long P = 0; P < D.Pixels; ++P)
		{
			const long long I = P * 4;
			const int B0 = First[I],  G0 = First[I + 1],  R0 = First[I + 2];
			const int B1 = Repeat[I], G1 = Repeat[I + 1], R1 = Repeat[I + 2];
			const int DB = B1 - B0 >= 0 ? B1 - B0 : B0 - B1;
			const int DG = G1 - G0 >= 0 ? G1 - G0 : G0 - G1;
			const int DR = R1 - R0 >= 0 ? R1 - R0 : R0 - R1;
			int Worst = DB > DG ? DB : DG;
			if (DR > Worst) { Worst = DR; }
			if (Worst > 0) { ++D.DiffPixels; }
			if (Worst > D.MaxAbsChannel) { D.MaxAbsChannel = Worst; }
			SumA += Luma((unsigned char)R0, (unsigned char)G0, (unsigned char)B0);
			SumB += Luma((unsigned char)R1, (unsigned char)G1, (unsigned char)B1);
		}
		D.MeanLumaFirst  = SumA / (double)D.Pixels;
		D.MeanLumaRepeat = SumB / (double)D.Pixels;
		D.MeanLumaDelta  = D.MeanLumaRepeat - D.MeanLumaFirst;
		return D;
	}

	// THE RATIO, BECAUSE THE FAULT IS STATED IN ONE. production/NOW.md records
	// the original reading as "the later shot darker by a luma ratio of 0.82",
	// and until now the line printed only the DIFFERENCE, so the number a
	// reader came looking for had to be divided by hand off two other keys.
	// It is repeat OVER first, so under 1 means the run got darker, and a
	// first frame at zero luma has no ratio rather than an infinite one.
	inline bool RepeatRatioExists(const RepeatDiff& D)
	{
		return D.Comparable && D.MeanLumaFirst > 0.0;
	}

	inline double RepeatLumaRatio(const RepeatDiff& D)
	{
		if (!RepeatRatioExists(D)) { return 0.0; }
		return D.MeanLumaRepeat / D.MeanLumaFirst;
	}

	// ONE LINE, WHOLE-RUN, AND THE WORD IS DECIDED FROM THE COUNT AND NEVER
	// FROM A TOLERANCE. There is no epsilon here on purpose: the claim being
	// tested is that two frames with identical inputs are the same picture,
	// and the honest bound for that is zero. A run that could not take the
	// repeat prints the words rather than a zero difference, because "no
	// repeat" and "no difference" are the two readings this key exists to
	// keep apart.
	inline std::string RigDeterminismLine(const std::string& RepeatOfShotId,
	                                      int ShotsBetween, int ShotsAsked,
	                                      const std::string& Status,
	                                      const RepeatDiff& D)
	{
		char Buf[1200];
		const bool bMeasured = (Status == "MEASURED") && D.Comparable && D.Pixels > 0;
		if (!bMeasured)
		{
			std::snprintf(Buf, sizeof(Buf),
				"rigDeterminism=NOTHING-MEASURED rigRepeatStatus=%s rigRepeatOf=%s "
				"rigRepeatAfterShots=%d/%d "
				"rigDiffPixels=nothing-measured rigDiffPct=nothing-measured "
				"rigMaxAbsChannelDiff=nothing-measured "
				"rigMeanLumaFirst=nothing-measured rigMeanLumaRepeat=nothing-measured "
				"rigMeanLumaDelta=nothing-measured rigMeanLumaRatio=nothing-measured "
				"rigStat=per-pixel-difference-between-the-first-shots-frame-and-a-repeat-of-its-"
				"camera-and-condition-photographed-last/whole-frame/one-per-run "
				"rigRule=identical-inputs-must-be-the-same-picture/"
				"any-nonzero-here-means-a-cross-shot-luma-comparison-in-this-run-is-partly-a-"
				"comparison-of-the-rig-and-not-of-the-street",
				(Status.empty() ? "NOT-RUN" : Status.c_str()),
				(RepeatOfShotId.empty() ? "none" : RepeatOfShotId.c_str()),
				ShotsBetween, ShotsAsked);
			return std::string(Buf);
		}
		char Ratio[48];
		if (RepeatRatioExists(D))
		{
			std::snprintf(Ratio, sizeof(Ratio), "%.4f", RepeatLumaRatio(D));
		}
		else
		{
			// A FIRST FRAME AT ZERO LUMA HAS NO RATIO. Printing 0.0000 there
			// would read as the darkest possible drift when the truth is that
			// the division has no denominator.
			std::snprintf(Ratio, sizeof(Ratio),
			              "nothing-measured/the-first-frames-mean-luma-is-zero");
		}
		std::snprintf(Buf, sizeof(Buf),
			"rigDeterminism=%s rigRepeatStatus=MEASURED rigRepeatOf=%s "
			"rigRepeatAfterShots=%d/%d "
			"rigDiffPixels=%lld/%lld rigDiffPct=%.2f rigMaxAbsChannelDiff=%d/255 "
			"rigMeanLumaFirst=%.4f rigMeanLumaRepeat=%.4f rigMeanLumaDelta=%+.4f "
			"rigMeanLumaRatio=%s "
			"rigRatioStat=repeat-over-first/whole-frame/one-per-run/under-1-means-the-run-got-"
			"darker/1.0000-is-the-only-reading-a-same-picture-claim-may-rest-on "
			"rigStat=per-pixel-difference-between-the-first-shots-frame-and-a-repeat-of-its-"
			"camera-and-condition-photographed-last/whole-frame/one-per-run "
			"rigRule=identical-inputs-must-be-the-same-picture/"
			"any-nonzero-here-means-a-cross-shot-luma-comparison-in-this-run-is-partly-a-"
			"comparison-of-the-rig-and-not-of-the-street",
			D.DiffPixels == 0 ? "IDENTICAL" : "DIFFERS",
			(RepeatOfShotId.empty() ? "none" : RepeatOfShotId.c_str()),
			ShotsBetween, ShotsAsked,
			D.DiffPixels, D.Pixels, Pct(D.DiffPixels, D.Pixels), D.MaxAbsChannel,
			D.MeanLumaFirst, D.MeanLumaRepeat, D.MeanLumaDelta, Ratio);
		return std::string(Buf);
	}
}
