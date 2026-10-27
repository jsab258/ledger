// Sighting.cs, ported (27 October 2026, phase 3's port; the 5 October sweep's G1): who saw the window go, and what
// they do. The rules' home is the Core; this is its port, checked by the Sighting* golden rows. The geography (who
// stands where on Quay Street at the hour) stays in CrimeProbe.h for now.
#pragma once

#include <algorithm>

namespace LedgerCore
{
	/// What a witness files about the deed (the review's A1; Jafar's A5 ruling, 30 September).
	enum class WitnessFiles { Nothing, NoiseOnly, StoryAboutHim };

	namespace Sighting
	{
		/// The swing and the glass going: anybody with a clear line on him watched that long.
		const double DeedSeconds = 1.0;

		/// Night is the game's own, from 19:00 to 07:00; an hour outside the day wraps round it.
		inline bool NightAt(int Hour)
		{
			const int H = ((Hour % 24) + 24) % 24;
			return H >= 19 || H < 7;
		}

		/// Daylight and the lamps that reach him, saturating; a lamp's reach held to 0 to 1.
		inline double LightOnHim(bool bNight, double LampReach)
		{
			const double Day = bNight ? 0.0 : 1.0;
			const double L = std::max(0.0, std::min(1.0, LampReach));
			return std::max(0.0, std::min(1.0, Day + L - Day * L));
		}

		/// A story about him only from a sighting the witness bank has words for; a noise alone is the damage heard.
		inline WitnessFiles WhatWitnessFiles(int Rung, bool bBankHasWords)
		{
			if (Rung <= 0) return WitnessFiles::NoiseOnly;
			return bBankHasWords ? WitnessFiles::StoryAboutHim : WitnessFiles::Nothing;
		}

		/// Only somebody who saw it shouts at him.
		inline bool WitnessShouts(int Rung) { return Rung >= 1; }
	}
}
