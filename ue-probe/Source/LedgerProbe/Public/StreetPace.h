// TRANSLITERATION of the street's PACE OF TALK from
// ledger/Assets/Scripts/Core/StreetVoice.cs (the sweep's U6, 6 November 2026):
// StreetVoice.ChatterLevel (about line 1570), StreetVoice.AmbientEverySeconds in
// both its forms (1578 and 1584) and ClearWordsEverySeconds (the 45-second floor
// of Jafar's ruling of 29 September), with the one-line Clamp01 they use.
//
// TRANSLITERATION, NOT REWRITE: the C# is the behavioural definition, every
// number and branch is its own, in its order, and the golden table
// (PerceptionGolden's EmitStreetPace, answered in CoreGolden.h's Evaluate) is the
// proof rather than this comment.
//
// NOT WIRED. The game calls none of it: it rests each person 45 s on their own
// (CrimeProbe.cpp), the same number by a different rule. Ported and pinned.
//
// NO UNREAL TYPE IS IN THIS FILE and no exception is thrown
// (LEDGER_CORE_NO_EXCEPTIONS holds).
#pragma once

#include "Perception.h"

#include <cfloat>

namespace LedgerCore
{
	namespace StreetPace
	{
		/// StreetVoice.ClearWordsEverySeconds: the neighbours' words no oftener than this.
		constexpr double ClearWordsEverySeconds = 45.0;

		/// StreetVoice.Clamp01 (v < 0 ? 0 : v > 1 ? 1 : v): NaN falls through unchanged,
		/// which LedgerCore::Clamp01 does by its bits.
		inline double Clamp01(double V) { return LedgerCore::Clamp01(V); }

		/// Math.Max(a, b) as .NET writes it: a NaN in either is the answer.
		inline double CsMax(double A, double B)
		{
			if (IsNaNBits(A)) { return A; }
			if (IsNaNBits(B)) { return B; }
			return A > B ? A : B;
		}

		/// StreetVoice.ChatterLevel: how loud the street is about you, 0..1.
		inline double ChatterLevel(double DayCircleHeat, int PeopleInEarshot)
		{
			return Clamp01(0.25 + 0.75 * Clamp01(DayCircleHeat)) * Clamp01(PeopleInEarshot / 6.0);
		}

		/// StreetVoice.AmbientEverySeconds(heat, people, floorSeconds). Fewer than two
		/// people in earshot is double.MaxValue. A heat that is not a number counts as none.
		inline double AmbientEverySeconds(double DayCircleHeat, int PeopleInEarshot, double FloorSeconds)
		{
			if (PeopleInEarshot < 2) { return DBL_MAX; }
			if (IsNaNBits(DayCircleHeat)) { DayCircleHeat = 0.0; }
			const double Busy = 0.5 + 0.5 * Clamp01(DayCircleHeat);
			const int Crowd = PeopleInEarshot > 1 ? PeopleInEarshot : 1;
			return CsMax(FloorSeconds, 26.0 / Busy / (double)Crowd * 3.0);
		}

		/// The two-argument form: the floor is ClearWordsEverySeconds.
		inline double AmbientEverySeconds(double DayCircleHeat, int PeopleInEarshot)
		{
			return AmbientEverySeconds(DayCircleHeat, PeopleInEarshot, ClearWordsEverySeconds);
		}
	}
}
