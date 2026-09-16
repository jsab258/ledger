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
#include <cmath>
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

	// ---- QUEUE 325: WHAT THE CAPTURE HAD DONE WHEN THE SHUTTER FIRED -----
	//
	// A BLANK FRAME AND A FRAME THAT WAS NOT READY LOOK IDENTICAL TODAY, and
	// that is why the blank cannot be diagnosed. Run 46 blanked none of 43,
	// run 47 blanked pinset_night_2 and _3, run 48 blanked pinset_night_1: a
	// different shot each run at one condition, one camera, one capture
	// path, which is a race and not a scene. `shotBlank` on this same line
	// is the structural half and says WHETHER; these two say what the rig
	// had done by the time it asked for the picture.
	//
	// NEITHER IS A BOUND AND NEITHER GATES ANYTHING. They are the first
	// measurement this diagnosis has ever had, and queue 325 asks for a
	// cause named by a measurement rather than by a story. PER-CAPTURE:
	// every number here is true of ONE shutter and of nothing else.
	inline std::string CaptureTimingSegment(int WarmTicks, int WarmTicksAsked,
	                                        int TimedSamples, int TimedSamplesAsked,
	                                        double SecondsToSettle, bool bSettled)
	{
		char Settle[64];
		if (bSettled) { std::snprintf(Settle, sizeof(Settle), "%.2f", SecondsToSettle); }
		else          { std::snprintf(Settle, sizeof(Settle), "nothing-measured/no-file-settled"); }
		char Buf[420];
		std::snprintf(Buf, sizeof(Buf),
			"shotCaptureWarmTicks=%d/of=%d shotCaptureTimedSamples=%d/of=%d "
			"shotCaptureSecondsToSettle=%s "
			"shotCaptureTimingStat=per-capture/warm-ticks-and-timed-samples-are-what-this-shutter-"
			"waited-for-before-it-asked/secondsToSettle-is-wall-time-from-the-request-to-the-file-"
			"size-standing-still/read-them-beside-shotBlank-which-is-the-structural-half",
			WarmTicks, WarmTicksAsked, TimedSamples, TimedSamplesAsked, Settle);
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

	// ---- QUEUES 329 AND 332: WHAT A PROBED LIGHT ACTUALLY IS ------------
	//
	// SIX OUTCOMES, AND THEY PARTITION `lightsProbed` EXACTLY. Run 48 is why
	// there are six and not two. Its done line read `lightsAboveFloor=17/28`
	// and the 2026-09-16 06:35Z ruling re-derived all 48 of its light lines:
	// eight of the seventeen YESes are a probe frame that failed to render
	// (a black frame means every pixel rose, so a broken capture scores as
	// the largest contribution any light can show), six more sit over a
	// control whose two renders of one unchanged scene differ by more than
	// the surplus they certify, and ten of the eleven NOs are not readings
	// either: seven of them came back BRIGHTER with the light off, across
	// 831241 to 921600 pixels of 921600. Three lights of the forty-two were
	// measured, all window practicals at one shot, and not one lantern.
	//
	// NO ABSOLUTE BOUND IS SET HERE AND NONE MAY BE. The screen is RELATIVE,
	// from queue 332's own sentence: a control that disagrees with itself by
	// more than the surplus it is certifying has certified nothing. Six
	// control samples, two of them blanks, is not a series, and the ruling
	// REFUSED the 0.001 proposed in the 640-fold gap between 0.00005 and
	// 0.02572. The column keeps printing; a bound comes off that series
	// later or off nothing at all.
	//
	// BLANKNESS IS NOT DECIDED HERE, ON PURPOSE AND NOT BY OVERSIGHT. It is
	// FrameStats::Measure's structural rule (one colour bucket, or no
	// non-black pixel) run on the decoded probe frame by the .cpp, which is
	// the only layer that holds pixels. This layer is handed the bit. A
	// blank frame is never handed to MeasureLightDelta at all, which is
	// queue 329's rule in one sentence, so for a blank frame there is no
	// delta here to classify.
	enum ELightRead
	{
		LightReadBlankShot = 0,      // this shot's reference or control frame was blank
		LightReadNoPair,             // a good floor, but no comparable delta for this light
		LightReadBlankProbeFrame,    // 329: THIS light's own OFF frame was blank
		LightReadExposureSwung,      // 332 (a): the pair was photographed at two exposures
		LightReadVoidControl,        // 332 (b): certified by a control that moved more
		LightReadMeasured,           // 332 (c): a difference, and the 326 edge test decides
		LightReadKinds
	};

	inline const char* LightReadWord(int R)
	{
		switch (R)
		{
		case LightReadBlankShot:       return "BLANK-SHOT";
		case LightReadNoPair:          return "NO-PAIR";
		case LightReadBlankProbeFrame: return "BLANK-PROBE-FRAME";
		case LightReadExposureSwung:   return "EXPOSURE-SWUNG";
		case LightReadVoidControl:     return "VOID-CONTROL";
		case LightReadMeasured:        return "MEASURED";
		default:                       return "NOTHING-MEASURED";
		}
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
	//
	// AND THE BEST PAIR IS SCANNED OVER MEASURED LIGHTS ONLY, 2026-09-16.
	// Scanned over all of them it names run 48's blank probe frames, whose
	// surplus is the whole reference frame: the largest number on the line
	// would be the one thing on it that is not a reading.
	struct LightFloor
	{
		std::string ShotId, CameraId, ConditionId;
		bool       bHaveControl = false;
		// WHY THIS SHOT HAS NO FLOOR, IN WORDS, when it has none. Empty means
		// it has one. `blank-control-frame` and `blank-reference-frame` are
		// two different faults (queue 329: run 48's pinset_night_2 lost the
		// control's re-render and pinset_night_1 lost the shot frame itself)
		// and a reader who cannot tell them apart cannot chase either.
		std::string NoControlWhy;
		LightDelta Control;
		int        Lights = 0;          // lights PROBED here, whatever became of them
		int        Read   = 0;          // ... MEASURED and above this shot's own control
		// THE SIX BUCKETS OF ELightRead, per shot, summing to Lights.
		int        Bucket[LightReadKinds] = {0, 0, 0, 0, 0, 0};
		int        LanternsProbed = 0, LanternsMeasured = 0;
		std::string BestId;             // the light at the best surplus, MEASURED ones only
		int        BestEdge    = -1;    // and the edge that surplus is AT
		long long  BestLightPx = 0;     // its RoseAtLeast at that edge
		long long  BestCtrlPx  = 0;     // the control's MovedAtLeast there
		double     BestMeanFull = 0.0;  // that same light's whole-frame mean
		bool       bHaveBest   = false;
		// QUEUE 337: the two eye-adaptation SPEEDS this shot's probe pass
		// asked for and what the component read back, captured once at the
		// start of the pass. THIS PINS NO EXPOSURE VALUE: only the rates.
		bool       bHoldAsked = false;
		double     HoldAskedUp = 0.0, HoldAskedDown = 0.0;
		bool       bHoldRead  = false;
		double     HoldReadUp = 0.0, HoldReadDown = 0.0;
	};

	// THIS SHOT'S CONTROL'S OWN SELF-AGREEMENT, AS A MAGNITUDE. One number,
	// not a second one: it is the absolute value of `Control.MeanDeltaFull`,
	// the signed whole-frame mean between two renders of one scene with
	// nothing toggled. Named rather than re-derived at each site so the
	// screen and the printed column cannot drift apart.
	inline double LightFloorCtrlGap(const LightFloor& F)
	{
		const double G = F.Control.MeanDeltaFull;
		return (G < 0.0) ? -G : G;
	}

	// THE SCREEN, IN THE RULING'S OWN ORDER, AND EVERY TEST IN IT RELATIVE.
	//
	// (0) A shot whose reference or control frame was blank has no floor at
	//     all, and that fact outranks anything about this light: run 48's
	//     pinset_night_1 lost its shot frame, so two of its seven probe
	//     frames are ALSO blank and would otherwise be filed under 329 as
	//     though the shot had been fine.
	// (a) A light whose whole-frame mean FELL with the light on by more than
	//     the control's gap was photographed at a different exposure from
	//     its reference. Physically a light cannot darken the frame, so this
	//     is the header's own darker rule turned from a suspicion into a
	//     status word. It printed NO before, which is a false negative from
	//     the same instrument that printed the false positives.
	// (b) A light whose rise OVER the control's gap does not itself exceed
	//     that gap is certified by nothing.
	// (c) The rest are MEASURED and take the 326 edge test unchanged.
	inline int ClassifyLightRead(const LightFloor& F, const LightDelta& D,
	                             bool bProbeFrameBlank)
	{
		if (!F.bHaveControl)  { return LightReadBlankShot; }
		if (bProbeFrameBlank) { return LightReadBlankProbeFrame; }
		if (!D.Comparable)    { return LightReadNoPair; }
		const double Gap = LightFloorCtrlGap(F);
		if (D.MeanDeltaFull < -Gap)       { return LightReadExposureSwung; }
		if (D.MeanDeltaFull - Gap <= Gap) { return LightReadVoidControl; }
		return LightReadMeasured;
	}

	// A SHOT READS WHEN AT LEAST ONE OF ITS LIGHTS WAS MEASURED AND BEAT ITS
	// OWN CONTROL. With no control there is nothing to read against, and
	// with a control that certified no light there is nothing to read
	// either; those are three different facts and each gets its own word on
	// the line (NO-CONTROL, NOT-USABLE, NO-READ).
	inline bool LightFloorUsable(const LightFloor& F)
	{
		return F.bHaveControl && F.Bucket[LightReadMeasured] > 0 && F.Read > 0;
	}

	// AND THE SHOT WHOSE CONTROL CERTIFIED NOTHING, queue 332's own verdict.
	inline bool LightFloorNotUsable(const LightFloor& F)
	{
		return F.bHaveControl && F.Bucket[LightReadMeasured] == 0;
	}

	inline void LightFloorSetControl(LightFloor& F, const LightDelta& D)
	{
		F.Control = D;
		F.bHaveControl = D.Comparable;
	}

	// Returns WHICH OF THE SIX this light is, so the caller never re-derives
	// it and the line, the shot tally and the run tally are one decision. The
	// surplus scan runs high edge to low so a tie on the surplus keeps the
	// STRONGER edge, which is the more informative half of the pair.
	//
	// `Kind` is the caller's word, the same one the light line prints, and it
	// is read here only to split lanterns from practicals: the run's headline
	// sentence is about lanterns and a whole-run count that cannot see kind
	// cannot say it.
	inline int LightFloorAddLight(LightFloor& F, const std::string& LightId,
	                              const std::string& Kind, const LightDelta& D,
	                              bool bProbeFrameBlank)
	{
		++F.Lights;
		const bool bLantern = (Kind == "lantern");
		if (bLantern) { ++F.LanternsProbed; }
		const int R = ClassifyLightRead(F, D, bProbeFrameBlank);
		++F.Bucket[R];
		if (R != LightReadMeasured) { return R; }
		if (bLantern) { ++F.LanternsMeasured; }
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
		return R;
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

	// ---- QUEUE 329: THE PROBE FRAME'S OWN STRUCTURAL NUMBERS -------------
	//
	// THE HALF OF THE DIFFERENCE NOTHING EVER PRINTED. A probe frame is one
	// of the two frames every light reading is made of, and until now the
	// only thing said about it was the delta it produced. Run 48's eight
	// false YESes were all one fault, a frame that failed to render, and the
	// only way anybody found them was by noticing that `meanOffFull` sat at
	// a camera's black level. That was a VALUE being read where the test is
	// STRUCTURAL, and it under-counted: the pinset camera writes its blanks
	// at 0.00152 and cam_A writes its at 0.00075, so a filter on the literal
	// string missed three of the eight. These keys remove the guess.
	//
	// ON EVERY DECODED PROBE FRAME AND NOT ONLY THE BLANK ONES, so the
	// column is a SERIES rather than an alarm: run 48's whole set of probe
	// frames arrives with its own structure printed, which is the thing rule
	// 2 asks for before anybody sets a bound on how dark a frame may be.
	// Nothing here is a bound. `Blank` is FrameStats' structural zero.
	//
	// ITS OWN KEY FAMILY AND NOT `shot*`, for the reason LightPinSegment
	// gives below: the shot line's `shotMeanLuma` counts SHOTS, and a second
	// family under the same names would make every one of them ambiguous
	// across a file that holds both. Queue 329's acceptance names the three
	// numbers and the way PixelLine prints them, which is what is copied:
	// the same statistics at the same precision under a prefix that cannot
	// collide. The deviation is deliberate and recorded here.
	inline std::string LightProbeFrameSegment(const FrameStats& S, bool bDecoded)
	{
		if (!bDecoded || S.Pixels == 0)
		{
			return std::string(
				"lightProbeFrameBlank=nothing-measured "
				"lightProbeFrameMeanLuma=nothing-measured "
				"lightProbeFrameNonBlackPixels=nothing-measured "
				"lightProbeFrameDistinctBuckets=nothing-measured "
				"lightProbeFrameStat=per-probe-frame/no-frame-decoded-for-this-line");
		}
		char Buf[420];
		std::snprintf(Buf, sizeof(Buf),
			"lightProbeFrameBlank=%s lightProbeFrameMeanLuma=%.4f "
			"lightProbeFrameNonBlackPixels=%lld/of=%lld "
			"lightProbeFrameDistinctBuckets=%d/32768 "
			"lightProbeFrameStat=per-probe-frame/the-OFF-half-of-THIS-lines-difference/"
			"same-statistics-and-precision-as-the-shot-lines-PixelLine-under-a-prefix-that-"
			"cannot-collide-with-it/blank-is-FrameStats-structural-rule-one-colour-bucket-or-"
			"no-non-black-pixel-and-is-NOT-a-threshold",
			S.Blank ? "yes" : "no", S.MeanLuma, S.NonBlack, S.Pixels, S.DistinctBuckets);
		return std::string(Buf);
	}

	// ---- QUEUE 337: THE TWO SPEEDS THE PROBE PASS HELD, ASKED BESIDE READ -
	//
	// WHY IT IS HERE AT ALL. Every OFF frame is photographed after the loop
	// has re-adapted to a scene with one light fewer, because the pass
	// re-enters Warm with the exposure rate snapped to 10000, so under AUTO
	// every difference is the light plus the loop's answer to it. Run 48 is
	// what that looks like: seven lights whose OFF frame came back brighter
	// across 831241 to 921600 pixels of 921600, and no lantern measured in
	// either direction, 0 of 24.
	//
	// THIS PINS NO EXPOSURE VALUE AND MAY NOT. The adapted value is a
	// render-thread quantity this process never reads, and the 2026-09-10
	// ruling forbids deriving a night pin; a DIFFERENTIAL needs only the two
	// frames at ONE value, whatever that value is. So only the two RATES are
	// written, and the per-shot write restores the snap on the next shot.
	//
	// ASKED BESIDE READ, ONE PAIR PER LINE. An engine that clamps the value
	// says so here rather than in a gap nobody can attribute, and an engine
	// that treats zero as instant leaves the control gaps where they are:
	// both outcomes are readable off this line and the control's own gap.
	inline std::string LightProbeHoldSegment(const LightFloor& F)
	{
		char Buf[420];
		char Asked[64];
		char Read[64];
		if (F.bHoldAsked) { std::snprintf(Asked, sizeof(Asked), "%.1f/%.1f", F.HoldAskedUp, F.HoldAskedDown); }
		else              { std::snprintf(Asked, sizeof(Asked), "nothing-measured"); }
		if (F.bHoldRead)  { std::snprintf(Read, sizeof(Read), "%.1f/%.1f", F.HoldReadUp, F.HoldReadDown); }
		else              { std::snprintf(Read, sizeof(Read), "nothing-measured"); }
		std::snprintf(Buf, sizeof(Buf),
			"lightProbeHoldAsked=%s lightProbeHoldRead=%s "
			"lightProbeHoldStat=per-shot/AutoExposureSpeedUp..then..SpeedDown/written-once-at-"
			"the-start-of-THIS-shots-probe-pass-after-the-reference-frame-is-on-disk-and-before-"
			"the-controls-re-render/restored-by-the-next-shots-own-per-shot-write/"
			"THIS-PINS-NO-EXPOSURE-VALUE-only-the-two-rates",
			Asked, Read);
		return std::string(Buf);
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
	//
	// AND SINCE 2026-09-16 IT REPORTS YES OR NO ONLY FOR A LIGHT THAT WAS
	// MEASURED. `Read` is ClassifyLightRead's answer, handed in rather than
	// re-derived, so the word on this segment, the word in `lightStatus` and
	// the shot's bucket counts are one decision taken once. A light that was
	// not measured prints `nothing-measured/` and the reason: run 48 printed
	// YES for eight blank frames and six lights over a void control, and NO
	// for seven whose OFF frame was simply brighter, and every one of those
	// fourteen words came out of this one snprintf.
	//
	// THE PAIR THAT DECIDED IT RIDES HERE TOO, one entry, both moments:
	// `lightVsCtrlGapMeanFull` is this light's own signed whole-frame mean
	// beside the absolute self-agreement gap of the control it was screened
	// against. Two keys whose relationship a reader has to remember is the
	// shape this project keeps paying for.
	inline std::string LightFloorSegment(const LightFloor& F, const LightDelta& D,
	                                     bool bIsControl, int Read)
	{
		char Buf[820];
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
					"lightVsFloorPx=nothing-measured "
					"lightVsCtrlGapMeanFull=nothing-measured");
				return std::string(Buf);
			}
			std::snprintf(Buf, sizeof(Buf),
				"lightAboveFloor=IS-THE-FLOOR lightAboveFloorEdge=not-applicable/this-line-is-the-"
				"control lightVsFloorPx=not-applicable/this-line-is-the-control "
				"lightVsCtrlGapMeanFull=not-applicable/this-line-is-the-control");
			return std::string(Buf);
		}
		// THE GAP PAIR, WHEN THERE IS A DELTA TO PAIR WITH IT. Captured at
		// the one instant the screen was applied, so the two halves of the
		// comparison cannot be greped into two moments.
		char GapPair[80];
		if (D.Comparable && F.bHaveControl)
		{
			std::snprintf(GapPair, sizeof(GapPair), "%+.5f..vs..%.5f",
			              D.MeanDeltaFull, LightFloorCtrlGap(F));
		}
		else
		{
			std::snprintf(GapPair, sizeof(GapPair), "nothing-measured");
		}
		// A LIGHT THAT WAS NEVER PHOTOGRAPHED HAS NO BUCKET, and saying
		// NO-PAIR of it would put it in one it is not in. Its own
		// `lightStatus` on this same line is the fact (SKIPPED-ALREADY-OFF,
		// NO-FILE, UNDECODABLE, NOT-COMPARABLE), and it is not in
		// `lightsProbed` either.
		if (Read < 0)
		{
			std::snprintf(Buf, sizeof(Buf),
				"lightAboveFloor=nothing-measured/this-light-was-never-photographed-see-"
				"lightStatus-on-this-line lightAboveFloorEdge=nothing-measured "
				"lightVsFloorPx=nothing-measured lightVsCtrlGapMeanFull=nothing-measured");
			return std::string(Buf);
		}
		if (Read != LightReadMeasured)
		{
			std::snprintf(Buf, sizeof(Buf),
				"lightAboveFloor=nothing-measured/%s lightAboveFloorEdge=nothing-measured "
				"lightVsFloorPx=nothing-measured lightVsCtrlGapMeanFull=%s "
				"lightVsCtrlGapStat=per-light/this-lights-signed-whole-frame-mean..vs..this-shots-"
				"controls-own-absolute-self-agreement-gap/the-RELATIVE-screen-of-queue-332/"
				"no-absolute-bound-is-set-anywhere-in-it",
				LightReadWord(Read), GapPair);
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
			"lightVsFloorPx=%lld..vs..%lld lightVsCtrlGapMeanFull=%s "
			"lightAboveFloorRule=this-lights-pixels-risen-at-that-edge-strictly-exceed-the-pixels-"
			"this-shots-own-control-MOVED-at-it/integer-counts/no-epsilon/YES-names-the-highest-"
			"edge-it-won-at-and-NO-reports-the-32-code-edge/"
			"ONLY-A-MEASURED-LIGHT-GETS-THIS-WORD-AT-ALL-since-queue-332",
			(E >= 0) ? "YES" : "NO", DeltaCodeEdge(At),
			D.RoseAtLeast[At], F.Control.MovedAtLeast[At], GapPair);
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
		// FOUR VERDICTS AND NOT THREE SINCE QUEUE 332. NOT-USABLE is a shot
		// whose control certified no light at all: it has a floor, and the
		// floor turned out to be bigger than everything it was asked to
		// certify. Folded into NO-READ it would say the control beat the
		// lights, which is a different and stronger claim than "nothing in
		// this shot was measurable".
		char Head[320];
		const int HeadNeeded = std::snprintf(Head, sizeof(Head),
			"lightfloor shot=%s camera=%s condition=%s lightFloorVerdict=%s",
			F.ShotId.c_str(), F.CameraId.c_str(), F.ConditionId.c_str(),
			!F.bHaveControl ? "NO-CONTROL"
			                : (LightFloorNotUsable(F) ? "NOT-USABLE"
			                                          : (F.Read > 0 ? "FLOOR-USABLE" : "NO-READ")));
		const bool bHeadCut = (HeadNeeded < 0 || (size_t)HeadNeeded >= sizeof(Head));
		std::string Out(Head);
		// THE BUCKETS OF THIS SHOT, ONE ENTRY, WITH THEIR ORDER NAMED BESIDE
		// THEM AND THEIR OWN DENOMINATOR INSIDE THE VALUE. Six counts that
		// sum to the lights this shot probed, so a reader can attribute the
		// run line's buckets to shots without re-deriving anything.
		char Buckets[200];
		std::snprintf(Buckets, sizeof(Buckets),
			" lightFloorBuckets=%d/%d/%d/%d/%d/%d/of=%d "
			"lightFloorBucketStat=per-shot/measured..blankShot..noPair..blankProbeFrame.."
			"exposureSwung..voidControl/they-sum-to-the-lights-this-shot-probed",
			F.Bucket[LightReadMeasured], F.Bucket[LightReadBlankShot],
			F.Bucket[LightReadNoPair], F.Bucket[LightReadBlankProbeFrame],
			F.Bucket[LightReadExposureSwung], F.Bucket[LightReadVoidControl],
			F.Lights);
		if (!F.bHaveControl)
		{
			Out += " lightsReadThisShot=nothing-measured/";
			char N[48]; std::snprintf(N, sizeof(N), "%d-lights-probed-in-this-shot", F.Lights);
			Out += N;
			Out += " lightFloorCtrl=nothing-measured/";
			Out += F.NoControlWhy.empty() ? "no-comparable-control-frame-for-this-shot"
			                              : F.NoControlWhy;
			Out += Buckets;
			Out += " ";
			Out += LightProbeHoldSegment(F);
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
			Best = "lightFloorBest=nothing-measured/no-MEASURED-light-in-this-shot "
			       "lightFloorBestPx=nothing-measured lightFloorBestMeanFull=nothing-measured";
		}
		// AND THE READ COUNT'S DENOMINATOR IS THE MEASURED LIGHTS, NOT ALL
		// OF THEM. `3/7` at run 48's pinset_night_4 would read as four lights
		// that failed, when the other four were three blank frames and one
		// exposure swing that nobody measured at all. With nothing measured
		// the count may not print 0, which is rule 3b's shape exactly.
		char ReadPair[80];
		if (F.Bucket[LightReadMeasured] > 0)
		{
			std::snprintf(ReadPair, sizeof(ReadPair), "%d/%d",
			              F.Read, F.Bucket[LightReadMeasured]);
		}
		else
		{
			std::snprintf(ReadPair, sizeof(ReadPair),
			              "nothing-measured/0-of-%d-lights-in-this-shot-were-measurable",
			              F.Lights);
		}
		// 1700 IS A HEADROOM NUMBER AND ITS SERIES IS nothing measured YET.
		// The 1100 it replaces DID come off a printed series: at the real
		// frame width this body measured 678 characters before this batch,
		// and the batch adds the bucket entry, the hold pair and a longer
		// stat string, which 1100 would cut. What the body measures AFTER
		// the batch has not been printed, so no figure for it is written
		// here. frame-stats-test.cpp prints it on every run as
		// floorLineChars, head plus body; read that and set this from it.
		// The announcer below fires either way, which is why a wrong-but-
		// generous buffer is a cost and not a silence.
		char Buf[1700];
		const int Needed = std::snprintf(Buf, sizeof(Buf),
			" lightsReadThisShot=%s lightFloorCtrlMeanFull=%+.5f "
			"lightFloorCtrlMovedAtLeast=%lld/%lld/%lld/%lld/%lld/%lld "
			"lightFloorCtrlDarker=%lld/%lld lightFloorCtrlPxOf=%lld "
			"lightFloorCodeEdges=1/2/4/8/16/32 %s%s %s "
			"lightFloorStat=per-shot/lightsReadThisShot-is-the-count-of-this-shots-MEASURED-lights-"
			"whose-risen-pixels-beat-this-shots-own-control-at-some-code-edge-over-the-lights-this-"
			"shot-MEASURED/lightFloorBest-is-the-largest-surplus-among-those-and-its-two-counts-"
			"are-at-the-one-edge-that-surplus-is-AT/"
			"lightFloorCtrlMeanFull-is-this-controls-OWN-SELF-AGREEMENT-the-signed-whole-frame-"
			"mean-between-two-renders-of-one-scene-with-nothing-toggled-and-its-ABSOLUTE-value-is-"
			"the-relative-screen-queue-332-applies-to-every-light-in-this-shot/"
			"lightFloorCtrlMovedAtLeast-is-the-per-pixel-noise-floor-and-stays-the-326-edge-test/"
			"a-NOT-USABLE-shot-certified-no-light-and-a-NO-READ-shot-measured-lights-and-none-beat-"
			"the-floor",
			ReadPair, F.Control.MeanDeltaFull,
			F.Control.MovedAtLeast[0], F.Control.MovedAtLeast[1], F.Control.MovedAtLeast[2],
			F.Control.MovedAtLeast[3], F.Control.MovedAtLeast[4], F.Control.MovedAtLeast[5],
			F.Control.PixelsDarkerWithLightOn, F.Control.Pixels, F.Control.Pixels,
			Best.c_str(), Buckets, LightProbeHoldSegment(F).c_str());
		Out += Buf;
		// BOTH HALVES OF THE LINE ARE WATCHED, and the marker names which one
		// bit: a cut head loses the shot id and a cut body loses the counts,
		// and both read as a line that simply did not carry them.
		if (bHeadCut)                                       { Out += " lightFloorLineCut=yes/at-320-chars-of-head"; }
		if (Needed < 0 || (size_t)Needed >= sizeof(Buf))    { Out += " lightFloorLineCut=yes/at-1700-chars-of-body"; }
		return Out;
	}

	// QUEUE 329: WHAT THE PROBE'S OWN FRAMES WERE, counted by the .cpp as
	// each one decodes. WHOLE-RUN AND CUMULATIVE over every probe frame of
	// every probed shot, control frames included, which is why it rides the
	// done line and not a shot line. A blank frame is the OFF half of a
	// difference that failed to render, and run 48 had nine of them.
	struct LightProbeFrames
	{
		int Decoded = 0;   // probe frames that decoded to pixels at all
		int Blank   = 0;   // ... of those, structurally blank per FrameStats::Measure
	};

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
	// refuses them by the shot line's own structural Blank rule.
	//
	// QUEUES 329 AND 332 CHANGED WHAT R IS AND WHAT IT IS OVER, 2026-09-16.
	// `lightsAboveFloor` now counts reads over the lights their shots
	// MEASURED, and `lightsMeasured` over `lightsProbed` is the denominator
	// that says how much of the run was a measurement at all.
	//
	// WHAT THIS PRINTS ON RUN 48'S OWN LINES IS nothing measured BY THIS
	// CODE YET. The partition below was derived BY HAND off the committed
	// verdict's 48 light lines and agrees with the 06:35Z ruling's
	// prediction, but a hand derivation of a rule is a prediction ABOUT this
	// function and not a reading OF it:
	//
	//   3 measured of 42, 3 above the floor of 3, 0 lanterns of 24,
	//   buckets 14 blank-shot / 0 no-pair / 8 blank-frame / 7 swung /
	//   10 void-control, and lightProbesBlank 9 of 48 frames decoded.
	//
	// The replay that would turn that into a reading belongs in
	// frame-stats-test.cpp with run 48's integers as its fixtures. Until it
	// is there, this comment is a claim about arithmetic nobody has run.
	inline std::string LightProbeDoneLine(int Probed, int Eligible,
	                                      const std::vector<LightFloor>& Floors,
	                                      int SkippedAlreadyOff, int SkippedBudget,
	                                      int NoFile, int RestoreMismatch,
	                                      int ShotsProbed, int ShotsAsked,
	                                      double BudgetSeconds, double SpentSeconds,
	                                      int FramesBeforeShot, int Controls,
	                                      const LightProbeFrames& PF = LightProbeFrames())
	{
		// THE TALLY IS TAKEN HERE AND NOWHERE ELSE, so the per-shot lines and
		// the run line cannot disagree: both are reductions of the same
		// vector, and the .cpp no longer counts anything about reads.
		//
		// FOUR SHOT BUCKETS SINCE QUEUE 332, AND THEY WERE THREE. A shot whose
		// control never measured is not a shot whose control swamped its
		// lights, and folding the first into NO-READ put a word on the run
		// line that the per-shot line refutes: `lightFloorShotStat` says
		// NO-READ means the control beat the lights, which is false of a shot
		// that had no control to beat them with. NOT-USABLE is the fourth: a
		// shot that HAS a floor and certified nothing with it, which run 48
		// has three of. Every floor lands in exactly one, so the four sum to
		// the floor count and a reader can check them against the
		// `lightfloor` lines.
		int ShotsUsable = 0, ShotsNoRead = 0, ShotsNoControl = 0, ShotsNotUsable = 0;
		int Reached = 0, MeasuredInUsable = 0;
		// AND SIX LIGHT BUCKETS, WHICH PARTITION `lightsProbed` EXACTLY.
		// `lightsInNoReadShots` and `lightsInNoControlShots` are GONE with
		// this batch and the test asserts them absent: they cut the same
		// lights a second, coarser way, and two partitions of one variable
		// under two key families is one number printed twice. The shot
		// counts above answer the shot question; these answer the light one.
		int Bucket[LightReadKinds] = {0, 0, 0, 0, 0, 0};
		int LanternsProbed = 0, LanternsMeasured = 0;
		// THE WORST FLOOR AND ITS SHOT'S OWN BEST LIGHT, CAPTURED AT THE SAME
		// INSTANT AND NAMED SO. The control's whole-frame movement is the
		// numerator's floor, so the light printed beside it is that shot's,
		// never the run's best light from somewhere else.
		const LightFloor* Worst = 0;
		for (size_t I = 0; I < Floors.size(); ++I)
		{
			const LightFloor& F = Floors[I];
			for (int B = 0; B < LightReadKinds; ++B) { Bucket[B] += F.Bucket[B]; }
			LanternsProbed   += F.LanternsProbed;
			LanternsMeasured += F.LanternsMeasured;
			if (LightFloorUsable(F))
			{
				++ShotsUsable;
				MeasuredInUsable += F.Bucket[LightReadMeasured];
				Reached          += F.Read;
			}
			else if (!F.bHaveControl)      { ++ShotsNoControl; }
			else if (LightFloorNotUsable(F)) { ++ShotsNotUsable; }
			else                           { ++ShotsNoRead; }
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
			// AND THE DENOMINATOR IS THE LIGHTS THOSE SHOTS MEASURED, not
			// every light they probed. Run 48's one usable shot probed seven
			// and measured three; `3/7` would report four lights that failed
			// when three of the four were blank frames and one was an
			// exposure swing, all of which measured nothing.
			std::snprintf(Reach, sizeof(Reach), "%d/%d", Reached, MeasuredInUsable);
		}
		// THE FIVE NOTHING-MEASURED BUCKETS AND THE MEASURED ONE, EACH BESIDE
		// `lightsProbed` SO NO ZERO IS BARE. A pass that probed nothing says
		// the words rather than printing six zeroes over a zero.
		std::string BucketSeg;
		{
			char B[420];
			if (Probed == 0)
			{
				std::snprintf(B, sizeof(B),
					"lightsMeasured=nothing-measured lightsNothingMeasuredBlankShot=nothing-measured "
					"lightsNothingMeasuredNoPair=nothing-measured "
					"lightsNothingMeasuredBlankProbeFrame=nothing-measured "
					"lightsNothingMeasuredExposureSwung=nothing-measured "
					"lightsNothingMeasuredVoidControl=nothing-measured");
			}
			else
			{
				std::snprintf(B, sizeof(B),
					"lightsMeasured=%d/%d lightsNothingMeasuredBlankShot=%d/%d "
					"lightsNothingMeasuredNoPair=%d/%d "
					"lightsNothingMeasuredBlankProbeFrame=%d/%d "
					"lightsNothingMeasuredExposureSwung=%d/%d "
					"lightsNothingMeasuredVoidControl=%d/%d",
					Bucket[LightReadMeasured], Probed,
					Bucket[LightReadBlankShot], Probed,
					Bucket[LightReadNoPair], Probed,
					Bucket[LightReadBlankProbeFrame], Probed,
					Bucket[LightReadExposureSwung], Probed,
					Bucket[LightReadVoidControl], Probed);
			}
			BucketSeg = B;
		}
		// LANTERNS ON THEIR OWN, because the sentence the run is judged by is
		// about lanterns and a count that cannot see kind cannot say it. A
		// run that probed no lantern prints the words: "0 lanterns measured"
		// with no denominator is exactly what the 06:35Z ruling refused.
		std::string KindSeg;
		{
			char K[300];
			if (LanternsProbed == 0)
			{
				std::snprintf(K, sizeof(K),
					"lanternsMeasured=nothing-measured/no-lantern-was-probed-in-this-run "
					"practicalsMeasured=%d/%d",
					Bucket[LightReadMeasured] - LanternsMeasured, Probed - LanternsProbed);
			}
			else
			{
				std::snprintf(K, sizeof(K),
					"lanternsMeasured=%d/%d practicalsMeasured=%d/%d",
					LanternsMeasured, LanternsProbed,
					Bucket[LightReadMeasured] - LanternsMeasured, Probed - LanternsProbed);
			}
			KindSeg = K;
		}
		// QUEUE 329'S DENOMINATOR: the blank probe frames over the probe
		// frames that DECODED, control frames included. A run that decoded
		// none may not print 0.
		std::string BlankSeg;
		{
			char BL[220];
			if (PF.Decoded == 0)
			{
				std::snprintf(BL, sizeof(BL),
					"lightProbesBlank=nothing-measured/no-probe-frame-decoded-in-this-run");
			}
			else
			{
				std::snprintf(BL, sizeof(BL), "lightProbesBlank=%d/%d", PF.Blank, PF.Decoded);
			}
			BlankSeg = BL;
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
		// 2600 IS A HEADROOM NUMBER AND ITS SERIES IS nothing measured YET.
		// The 1500 it replaces came off a printed series; this batch adds
		// six bucket keys, two kind keys, a blank pair, a fourth shot bucket
		// and three stat strings, which 1500 would cut. What the line
		// measures AFTER the batch has not been printed, so no figure for it
		// is written here. frame-stats-test.cpp prints it on every run as
		// doneLineChars and plants an id long enough to make the announcer
		// fire; read that and set this from it.
		char Buf[2600];
		const int Needed = std::snprintf(Buf, sizeof(Buf),
			"lightProbeStatus=%s lightsProbed=%d/%d lightsAboveFloor=%s "
			"%s %s %s "
			"lightsSkippedAlreadyOff=%d lightsSkippedBudget=%d lightProbesNoFile=%d "
			"lightRestoreMismatch=%d/%d controlProbes=%d "
			"lightFloorShotsUsable=%d/%d lightFloorShotsNotUsable=%d/%d "
			"lightFloorShotsNoRead=%d/%d lightFloorShotsNoControl=%d/%d %s "
			"shotsProbed=%d/%d lightProbeBudgetSeconds=%.1f lightProbeSpentSeconds=%.1f "
			"lightProbeFramesBeforeShot=%d/same-as-reference "
			"lightProbeMethod=one-light-off-vs-reference/same-camera-condition-framecount "
			"lightsAboveFloorStat=whole-run/count-of-MEASURED-lights-that-beat-their-OWN-shots-"
			"control-at-some-code-edge/denominator-is-the-lights-MEASURED-in-shots-with-a-usable-"
			"floor-and-NOT-every-light-they-probed/"
			"RENAMED-BY-QUEUE-326-from-lightsReachedFrame-which-counted-one-pixel-rising-by-one-"
			"code-value-through-run-47-and-is-not-comparable/"
			"RE-DENOMINATED-BY-QUEUE-332-on-2026-09-16-so-runs-before-that-are-not-comparable-"
			"either "
			"lightBucketStat=whole-run/lightsMeasured-and-the-five-nothing-measured-buckets-"
			"partition-lightsProbed-exactly/blankShot-is-a-shot-whose-reference-or-control-frame-"
			"was-structurally-blank/blankProbeFrame-is-THIS-lights-own-OFF-frame-blank-queue-329/"
			"exposureSwung-is-a-whole-frame-mean-that-FELL-by-more-than-its-controls-own-gap/"
			"voidControl-is-a-rise-over-that-gap-that-does-not-itself-exceed-it-queue-332/"
			"the-screen-is-RELATIVE-and-NO-ABSOLUTE-BOUND-IS-SET-ANYWHERE-IN-IT "
			"lightProbesBlankStat=whole-run/cumulative-over-every-probe-frame-that-decoded-"
			"control-frames-included/blank-is-FrameStats-structural-rule-and-not-a-threshold "
			"lightFloorShotStat=whole-run/a-shot-is-usable-when-at-least-one-of-its-lights-was-"
			"MEASURED-and-beat-its-own-control/NOT-USABLE-means-the-control-certified-no-light-at-"
			"all/NO-READ-means-lights-were-measured-and-none-beat-the-floor-not-that-the-lights-"
			"are-dark",
			Probed == 0 ? "NOTHING-MEASURED" : (SkippedBudget > 0 ? "PARTIAL-BUDGET-BIT" : "ALL"),
			Probed, Eligible, Reach,
			BucketSeg.c_str(), KindSeg.c_str(), BlankSeg.c_str(),
			SkippedAlreadyOff, SkippedBudget, NoFile,
			RestoreMismatch, Probed, Controls,
			ShotsUsable, (int)Floors.size(), ShotsNotUsable, (int)Floors.size(),
			ShotsNoRead, (int)Floors.size(), ShotsNoControl, (int)Floors.size(),
			WorstSeg.c_str(),
			ShotsProbed, ShotsAsked, BudgetSeconds, SpentSeconds, FramesBeforeShot);
		std::string Out(Buf);
		if (Needed < 0 || (size_t)Needed >= sizeof(Buf))
		{
			Out += " lightProbeDoneLineCut=yes/at-2600-chars";
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

// =======================================================================
// QUEUE 333: IS THE LANTERN THE BRIGHTEST WARM THING IN ITS OWN CORNER OF
// THE PICTURE. The pixel half of the lamp acceptance instrument; the other
// half is LedgerSurface::PieceScreenBox, which says WHERE on the frame the
// lamp head is and nothing about what is there. This file carries no spec
// type on purpose, so the rectangle arrives as four doubles and this half
// never learns what a Piece is.
//
// WHAT IT PRINTS AND WHAT IT DOES NOT. It prints a SERIES: the peaks and
// means inside the lantern's own projected rectangle, and the same numbers
// for the ring of picture around it. IT SETS NO BOUND. Queue 333's reference
// numbers, measured off the approved Hook sheet under D41 (globe maxLuma 242
// of 255, maxWarm 140, meanLuma 188 over 141 pixels, against a sky at 181),
// are what a lit lamp looks like; they are NOT a gate and nothing here
// compares against them. Rule 2: ship the printer, read real runs, set the
// number afterwards.
//
// THE ONE THING IT DOES DECIDE IS A COMPARISON AND NOT A THRESHOLD. yes
// means the brightest pixel of the lamp's own rectangle is strictly brighter
// than the brightest pixel of the ring around it AND the warmest pixel of
// the rectangle is strictly warmer than the warmest of the ring. Both sides
// of that come out of the same frame, so no constant is chosen anywhere:
// a flat field ties and reads no, a dark head against a pale sky reads no,
// and a lit globe against the same sky reads yes. That sentence is the
// item's acceptance, which asks for the fixture to be "measurably the
// brightest warm thing in its own neighbourhood".
//
// THE UNITS ARE sRGB BYTES, not the 0-to-1 luma the rest of this file
// prints, because the reference above was measured in bytes and a reading
// that cannot be put beside its reference is half a reading. Same weights,
// different scale, and the scale is named on the line.
namespace LedgerFrame
{
	// THE SAME WEIGHTS AS Luma ON THE BYTE SCALE, rounded to nearest.
	inline int LumaByte(unsigned char R, unsigned char G, unsigned char B)
	{
		return (int)(Luma(R, G, B) * 255.0 + 0.5);
	}

	// WARM IS R MINUS B IN sRGB BYTES, the same quantity queue 333 measured
	// the reference globe and the probe's night frame with, so the three
	// numbers are comparable. It is SIGNED: a cold pixel is negative, and a
	// max over a cold region is negative rather than zero.
	inline int WarmByte(unsigned char R, unsigned char B)
	{
		return (int)R - (int)B;
	}

	// THE RING IS A NEIGHBOURHOOD DEFINITION, NOT A THRESHOLD. It is the
	// lamp's own projected box grown by its own longer side on every edge,
	// so a lamp near the camera and one far down the street are each read
	// against a ring in proportion to themselves rather than against a fixed
	// number of pixels that means something different at every distance. The
	// floor of 1 is "at least one pixel of ring to compare with", not a tuned
	// value, and both rectangles are printed in pixels so any reader can
	// re-derive the whole thing from the line.
	inline int LampRingPadPx(int CoreW, int CoreH)
	{
		const int Bigger = (CoreW > CoreH) ? CoreW : CoreH;
		return (Bigger > 1) ? Bigger : 1;
	}

	// EVERY VALUE ON A VERDICT LINE IS SPLIT ON WHITESPACE BY EVERY READER
	// HERE, so an id that carries a space would truncate the token silently.
	// Sanitised in the tested layer rather than trusted from the caller.
	inline std::string LampSafeId(const std::string& Id)
	{
		std::string Out;
		for (size_t I = 0; I < Id.size(); ++I)
		{
			const char C = Id[I];
			Out += (C > ' ' && C != '=') ? C : '_';
		}
		return Out.empty() ? std::string("unnamed") : Out;
	}

	// ONE LANTERN'S READING. Measured false means this lantern produced NO
	// reading at all and Why says which of the ways: it is not a "no", and
	// the segment below never counts it as one.
	//
	// WHAT EACH NUMBER IS A STATISTIC OF:
	//   CoreMaxLuma          PEAK luma over the lamp's own rectangle
	//   CoreWarmAtMaxLuma    the warmth of THAT pixel, captured at the peak
	//   CoreMaxWarm          PEAK warmth over the same rectangle
	//   CoreLumaAtMaxWarm    the luma of THAT pixel, captured at the peak
	//   CoreMeanLuma         mean luma over the rectangle, its denominator
	//                        being CorePixels
	//   Ring*                the same four statistics over the annulus
	// The two peaks are usually two different pixels, which is why each
	// carries its companion: the reference sheet's globe reads 242 and 140
	// the same way.
	struct LampPatch
	{
		bool        Measured = false;
		std::string Id       = "unnamed";
		std::string Why      = "nothing-measured";
		int         CX0 = 0, CY0 = 0, CX1 = 0, CY1 = 0;
		int         RX0 = 0, RY0 = 0, RX1 = 0, RY1 = 0;
		long long   CorePixels = 0, RingPixels = 0;
		int         CoreMaxLuma = 0, CoreWarmAtMaxLuma = 0;
		int         CoreMaxWarm = 0, CoreLumaAtMaxWarm = 0;
		int         RingMaxLuma = 0, RingWarmAtMaxLuma = 0;
		int         RingMaxWarm = 0, RingLumaAtMaxWarm = 0;
		double      CoreMeanLuma = 0.0, RingMeanLuma = 0.0;
	};

	// BGRA8, top row first, the same convention Measure and MeasureBand are
	// given. The rectangle is the projection's four doubles, unrounded, and
	// the rounding happens HERE so the caller in the module does no
	// arithmetic: floor and ceil, so a lamp narrower than a pixel still
	// covers the pixel it falls in instead of rounding away to nothing.
	//
	// bBoxMeasured IS THE PROJECTION'S OWN VERDICT and it outranks the
	// numbers: a box with a corner behind the eye reports nothing-measured
	// here rather than a rectangle computed from the corners that happened
	// to be in front.
	inline LampPatch MeasureLampPatch(const unsigned char* Bgra, int W, int H,
	                                  const std::string& Id, bool bBoxMeasured,
	                                  double X0, double Y0, double X1, double Y1)
	{
		LampPatch P;
		P.Id = LampSafeId(Id);
		if (Bgra == 0 || W <= 0 || H <= 0)
		{
			P.Why = "no-decoded-frame";
			return P;
		}
		if (!bBoxMeasured)
		{
			P.Why = "the-projection-did-not-answer-for-this-lantern";
			return P;
		}
		int CX0 = (int)std::floor(X0), CX1 = (int)std::ceil(X1);
		int CY0 = (int)std::floor(Y0), CY1 = (int)std::ceil(Y1);
		if (CX1 <= CX0) { CX1 = CX0 + 1; }
		if (CY1 <= CY0) { CY1 = CY0 + 1; }
		// THE PAD IS TAKEN FROM THE UNCLIPPED BOX, deliberately: a lamp half
		// off the edge of the frame is still its own size, and scaling the
		// ring to the visible sliver would read it against a neighbourhood
		// that shrinks as the lamp leaves the picture.
		const int Pad = LampRingPadPx(CX1 - CX0, CY1 - CY0);
		int RX0 = CX0 - Pad, RX1 = CX1 + Pad;
		int RY0 = CY0 - Pad, RY1 = CY1 + Pad;
		if (CX0 < 0) { CX0 = 0; }
		if (CY0 < 0) { CY0 = 0; }
		if (CX1 > W) { CX1 = W; }
		if (CY1 > H) { CY1 = H; }
		if (RX0 < 0) { RX0 = 0; }
		if (RY0 < 0) { RY0 = 0; }
		if (RX1 > W) { RX1 = W; }
		if (RY1 > H) { RY1 = H; }
		P.CX0 = CX0; P.CY0 = CY0; P.CX1 = CX1; P.CY1 = CY1;
		P.RX0 = RX0; P.RY0 = RY0; P.RX1 = RX1; P.RY1 = RY1;
		if (CX1 <= CX0 || CY1 <= CY0)
		{
			P.Why = "the-lanterns-box-falls-outside-this-frame";
			return P;
		}
		double CoreSum = 0.0, RingSum = 0.0;
		bool bFirstCore = true, bFirstRing = true;
		for (int Y = RY0; Y < RY1; ++Y)
		{
			for (int X = RX0; X < RX1; ++X)
			{
				const long long At = (long long)Y * (long long)W + (long long)X;
				const unsigned char B = Bgra[At * 4];
				const unsigned char G = Bgra[At * 4 + 1];
				const unsigned char R = Bgra[At * 4 + 2];
				const int L = LumaByte(R, G, B);
				const int Wm = WarmByte(R, B);
				const bool bCore = (X >= CX0 && X < CX1 && Y >= CY0 && Y < CY1);
				if (bCore)
				{
					++P.CorePixels;
					CoreSum += (double)L;
					if (bFirstCore || L > P.CoreMaxLuma)
					{
						P.CoreMaxLuma = L; P.CoreWarmAtMaxLuma = Wm;
					}
					if (bFirstCore || Wm > P.CoreMaxWarm)
					{
						P.CoreMaxWarm = Wm; P.CoreLumaAtMaxWarm = L;
					}
					bFirstCore = false;
				}
				else
				{
					++P.RingPixels;
					RingSum += (double)L;
					if (bFirstRing || L > P.RingMaxLuma)
					{
						P.RingMaxLuma = L; P.RingWarmAtMaxLuma = Wm;
					}
					if (bFirstRing || Wm > P.RingMaxWarm)
					{
						P.RingMaxWarm = Wm; P.RingLumaAtMaxWarm = L;
					}
					bFirstRing = false;
				}
			}
		}
		if (P.CorePixels == 0)
		{
			P.Why = "the-lanterns-box-covers-no-pixel-of-this-frame";
			return P;
		}
		// A RING WITH NO PIXELS IS NOT A NEIGHBOURHOOD, and a comparison
		// against nothing may not print as a no: a lamp whose box fills the
		// whole frame has no outside to be brighter than.
		if (P.RingPixels == 0)
		{
			P.Why = "this-lantern-has-no-ring-pixel-on-this-frame";
			return P;
		}
		P.CoreMeanLuma = CoreSum / (double)P.CorePixels;
		P.RingMeanLuma = RingSum / (double)P.RingPixels;
		P.Measured = true;
		P.Why = "measured";
		return P;
	}

	// STRICTLY GREATER ON BOTH, so a tie is a no. Nothing else is decided
	// here and no constant appears: both sides come off the same frame.
	inline bool LampPatchLit(const LampPatch& P)
	{
		if (!P.Measured) { return false; }
		return P.CoreMaxLuma > P.RingMaxLuma && P.CoreMaxWarm > P.RingMaxWarm;
	}

	// THREE WORDS AND NOT TWO. An unmeasured lantern is not a dark one.
	inline const char* LampPatchWord(const LampPatch& P)
	{
		if (!P.Measured) { return "nothing-measured"; }
		return LampPatchLit(P) ? "yes" : "no";
	}

	inline std::string LampPatchToken(int Index, const LampPatch& P)
	{
		char T[640];
		int Needed;
		if (!P.Measured)
		{
			Needed = std::snprintf(T, sizeof(T), "lampGlow%d=%s/nothing-measured/%s",
			                       Index, P.Id.c_str(), P.Why.c_str());
		}
		else
		{
			Needed = std::snprintf(T, sizeof(T),
				"lampGlow%d=%s/%s"
				"/coreMaxLuma=%d/coreWarmAtMaxLuma=%d"
				"/coreMaxWarm=%d/coreLumaAtMaxWarm=%d"
				"/coreMeanLuma=%.1f/corePx=%lld"
				"/ringMaxLuma=%d/ringWarmAtMaxLuma=%d"
				"/ringMaxWarm=%d/ringLumaAtMaxWarm=%d"
				"/ringMeanLuma=%.1f/ringPx=%lld"
				"/box=x%d..%d/y%d..%d/ring=x%d..%d/y%d..%d",
				Index, P.Id.c_str(), LampPatchWord(P),
				P.CoreMaxLuma, P.CoreWarmAtMaxLuma,
				P.CoreMaxWarm, P.CoreLumaAtMaxWarm,
				P.CoreMeanLuma, P.CorePixels,
				P.RingMaxLuma, P.RingWarmAtMaxLuma,
				P.RingMaxWarm, P.RingLumaAtMaxWarm,
				P.RingMeanLuma, P.RingPixels,
				P.CX0, P.CX1, P.CY0, P.CY1,
				P.RX0, P.RX1, P.RY0, P.RY1);
		}
		std::string Out(T);
		// snprintf TRUNCATES IN SILENCE and a cut token reads as a short one,
		// which is what a key that was never emitted looks like.
		if (Needed < 0 || (size_t)Needed >= sizeof(T)) { Out += "/lampTokenCut=yes/at-640-chars"; }
		return Out;
	}

	// THE PER-SHOT SEGMENT, FOR ANY SHOT LINE THAT HAS A DECODED FRAME.
	//
	// EVERY NUMBER HERE IS TRUE OF ONE FRAME. None of it may ride a done
	// line, which is the same separation WetRedriveSegment and WetShotFields
	// keep, and the key family is its own so a grep for a lamp key cannot
	// return the scene line's lampGain.
	//
	// RULED 2026-09-16, section 3.4: it prints on EVERY shot line with a
	// decoded frame and not only on probed shots, because a day row is never
	// a probed shot and "no at day, yes at night in one run" is this item's
	// acceptance sentence. A segment that could only print at night could
	// never be refuted.
	//
	// THE DENOMINATORS, all three, because a zero here has three different
	// meanings (rule 3b). inFile is how many emissive pieces the street file
	// carries; examined is how many of them the run could hand this function
	// a rectangle for, which is smaller whenever a lantern fell down an
	// unpainted exit and has no instance; and `of` beside the lit count is
	// how many of those examined produced a reading at all.
	//
	// THE CAP ANNOUNCES ITSELF. instruments.md dictates `(+N more not
	// shown)`, and that phrasing carries spaces, which every reader of these
	// lines splits on; so the same fact is carried space-free as
	// lampGlowShown=<k>/notShown=<n>, which prints on every line and not only
	// when it bites. MaxShown of 0 or less means no cap.
	inline std::string LampGlowSegment(const std::vector<LampPatch>& Patches,
	                                   int LanternsInFile, bool bDecodedFrame,
	                                   int MaxShown)
	{
		char Head[400];
		if (!bDecodedFrame)
		{
			std::snprintf(Head, sizeof(Head),
				"lampGlow=nothing-measured/this-shot-line-carries-no-decoded-frame"
				" lampGlowExamined=0/inFile=%d", LanternsInFile);
			return std::string(Head);
		}
		if (LanternsInFile <= 0)
		{
			return std::string("lampGlow=nothing-measured/this-street-carries-no-emissive-piece"
			                   " lampGlowExamined=0/inFile=0");
		}
		if (Patches.empty())
		{
			std::snprintf(Head, sizeof(Head),
				"lampGlow=nothing-measured/no-lantern-could-be-examined-on-this-frame"
				" lampGlowExamined=0/inFile=%d", LanternsInFile);
			return std::string(Head);
		}
		int Read = 0, Lit = 0;
		for (size_t I = 0; I < Patches.size(); ++I)
		{
			if (!Patches[I].Measured) { continue; }
			++Read;
			if (LampPatchLit(Patches[I])) { ++Lit; }
		}
		int Shown = (int)Patches.size();
		if (MaxShown > 0 && Shown > MaxShown) { Shown = MaxShown; }
		const int NotShown = (int)Patches.size() - Shown;
		const int Needed = std::snprintf(Head, sizeof(Head),
			"lampGlowStat=per-lantern/this-frame-only"
			"/lamps-own-box-peak-vs-the-peak-of-the-ring-around-it/strictly-greater-on-both"
			" lampGlowUnits=srgb-bytes/luma=0.299r+0.587g+0.114b/warm=r-minus-b"
			" lampGlowLit=%d/of=%d/examined=%d/inFile=%d"
			" lampGlowShown=%d/notShown=%d",
			Lit, Read, (int)Patches.size(), LanternsInFile, Shown, NotShown);
		std::string Out(Head);
		if (Needed < 0 || (size_t)Needed >= sizeof(Head))
		{
			Out += " lampGlowHeadCut=yes/at-400-chars";
		}
		for (int I = 0; I < Shown; ++I)
		{
			Out += " ";
			Out += LampPatchToken(I + 1, Patches[(size_t)I]);
		}
		return Out;
	}
}
