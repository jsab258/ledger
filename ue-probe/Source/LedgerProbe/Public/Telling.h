// TRANSLITERATION of the TELLING half of ledger/Assets/Scripts/Core/Observation.cs
// (the sweep's U4, 6 November 2026): Observe.Willingness (about line 364),
// Observe.Misattribute (410), Observe.RetellingsPerRung and Observe.Retell
// (436), and the class Delivery (478), "a witness is a deadline".
//
// TRANSLITERATION, NOT REWRITE, by the same rule as every other file here: the
// C# is the behavioural definition, every number and branch is its own, in its
// order, and the golden table (PerceptionGolden's EmitTelling, answered in
// CoreGolden.h's Evaluate) is the proof rather than this comment.
//
// WHAT IS ALSO HERE BECAUSE ONLY THESE NEED IT: System.Random(seed).NextDouble(),
// the one draw Misattribute makes. A seeded System.Random is the same legacy
// subtractive generator (Knuth, Numerical Recipes) in every .NET since 1.0, and
// a different draw would name a different man for the same seed, so it is
// carried in full (Net5CompatSeedImpl) and pinned by its own golden rows.
//
// NOT WIRED. The game calls none of it: the witness reports at 09:00 the next
// morning (TownWeek.h), no one walks to tell, and nothing yet threatens or pays
// a witness in transit. Ported and pinned, as Reaction.h's ladder was.
//
// NO UNREAL TYPE IS IN THIS FILE, no exception is thrown (LEDGER_CORE_NO_EXCEPTIONS
// holds), and nothing here allocates but the seeded generator's own table.
#pragma once

#include "Observation.h"

#include <string>

namespace LedgerCore
{
	namespace Telling
	{
		/// Observe.Willingness: WILL THEY SAY IT, separate from believing it.
		/// Observation.cs's weights, in its order; the top of the range does not
		/// saturate, and own secret is the strongest lever (0.85).
		inline double Willingness(double Nerve, double LoyaltyToPlayer, double OwnSecret, double FearOfOutfit,
		                          double SympathyForVictim)
		{
			const double W = 0.45
			               + 0.35 * Clamp01(Nerve)
			               + 0.35 * Clamp01(SympathyForVictim)
			               - 0.55 * Clamp01(LoyaltyToPlayer)
			               - 0.85 * Clamp01(OwnSecret)
			               - 0.45 * Clamp01(FearOfOutfit);
			return Clamp01(W);
		}

		/// System.Random(seed) and its NextDouble(), the legacy seeded generator.
		/// Ints are 32-bit and the subtractions are done in int arithmetic as the
		/// .NET source does; no value here can overflow (all stay under MBIG).
		class SeededRandom
		{
		public:
			explicit SeededRandom(int Seed)
			{
				const int MBig = 2147483647;
				const int MSeed = 161803398;
				// Math.Abs(Int32.MinValue) throws in .NET, so the source maps it first.
				const int Subtraction = (Seed == (-2147483647 - 1)) ? 2147483647 : (Seed < 0 ? -Seed : Seed);
				int MJ = MSeed - Subtraction;
				SeedArray[55] = MJ;
				int MK = 1;
				for (int I = 1; I < 55; ++I)
				{
					const int II = (21 * I) % 55;
					SeedArray[II] = MK;
					MK = MJ - MK;
					if (MK < 0) { MK += MBig; }
					MJ = SeedArray[II];
				}
				for (int K = 1; K < 5; ++K)
				{
					for (int I = 1; I < 56; ++I)
					{
						SeedArray[I] -= SeedArray[1 + (I + 30) % 55];
						if (SeedArray[I] < 0) { SeedArray[I] += MBig; }
					}
				}
				INext = 0;
				INextP = 21;
			}

			double NextDouble()
			{
				const int MBig = 2147483647;
				int LocINext = INext;
				int LocINextP = INextP;
				if (++LocINext >= 56) { LocINext = 1; }
				if (++LocINextP >= 56) { LocINextP = 1; }
				int RetVal = SeedArray[LocINext] - SeedArray[LocINextP];
				if (RetVal == MBig) { --RetVal; }
				if (RetVal < 0) { RetVal += MBig; }
				SeedArray[LocINext] = RetVal;
				INext = LocINext;
				INextP = LocINextP;
				return (double)RetVal * (1.0 / (double)MBig);
			}

		private:
			int SeedArray[56];
			int INext;
			int INextP;
		};

		/// Observe.Misattribute: a partial identification plus expectation names
		/// the wrong man. Rung 1 (a bare silhouette) misattributes at 0.45, rung 2
		/// and 3 (a mark) at 0.25; below 1 is too little and 4 is certain. The
		/// C# returns AccusedId, which may be null; here the empty string is null
		/// (Observation.h), and an empty expected id is "no one expected".
		inline std::string Misattribute(const Observation& O, const std::string& ExpectedId, int Seed)
		{
			if (O.Rung < 1 || O.Rung >= 4) { return O.AccusedId; }
			if (ExpectedId.empty()) { return O.AccusedId; }
			const double P = O.Rung == 1 ? 0.45 : 0.25;
			SeededRandom R(Seed);
			return R.NextDouble() < P ? ExpectedId : O.AccusedId;
		}

		/// Observe.RetellingsPerRung.
		static const int RetellingsPerRung = 4;

		/// Observe.Retell: MEMORY HARDENS AS IT DECAYS. Certainty +0.10 each
		/// time, capped at 0.94 (never indelible); every fourth telling climbs a
		/// rung below 4, and climbing to a name without evidence takes the one
		/// they expected. A null or empty observation is untouched. The count
		/// wraps as a C# int does (unchecked), done unsigned so it is not UB.
		inline void Retell(Observation* O, const std::string& ExpectedId = std::string())
		{
			if (O == nullptr || O->Empty()) { return; }
			O->Retellings = (int)((unsigned int)O->Retellings + 1u);
			O->Certainty = Clamp(O->Certainty + 0.10, 0.0, 0.94);
			if (O->Retellings % RetellingsPerRung == 0 && O->Rung < 4)
			{
				O->Rung++;
				if (O->Rung >= 4 && O->AccusedId.empty()) { O->AccusedId = ExpectedId; }
			}
		}

		/// Math.Max(double, double), NaN-propagating as .NET's is.
		inline double MaxOf(double A, double B)
		{
			if (A != B)
			{
				if (!IsNaNBits(A)) { return B < A ? A : B; }
				return A;
			}
			return B;
		}

		/// class Delivery: A WITNESS IS A DEADLINE. Between observing and the
		/// street knowing, the witness is a person walking somewhere.
		struct Delivery
		{
			std::string WitnessId;
			std::string DestinationId;
			double MinutesRemaining = 0.0;
			bool Running = false;
			bool Arrived = false;
			bool Intercepted = false;

			/// A frightened witness (nerve under 0.35) runs, at 0.45 of the walk;
			/// an unsure one (willingness under 0.5) sits with it first, 20 plus
			/// 70 times the unwillingness minutes. Never under half a minute.
			static Delivery Begin(const std::string& WitnessId, const std::string& DestinationId, double WalkMinutes,
			                      double Nerve, double Willingness)
			{
				const bool bFrightened = Nerve < 0.35;
				const double Delay = Willingness < 0.5 ? 20 + 70 * (1 - Willingness) : 0;
				Delivery D;
				D.WitnessId = WitnessId;
				D.DestinationId = DestinationId;
				D.Running = bFrightened;
				D.MinutesRemaining = MaxOf(0.5, WalkMinutes * (bFrightened ? 0.45 : 1.0) + Delay);
				return D;
			}

			/// True on the tick it arrives, exactly once.
			bool Tick(double Minutes)
			{
				if (Arrived || Intercepted || !(Minutes > 0)) { return false; }
				MinutesRemaining -= Minutes;
				if (MinutesRemaining > 0) { return false; }
				MinutesRemaining = 0;
				Arrived = true;
				return true;
			}

			/// Paid, threatened, talked round, or killed: leaves no trace before
			/// arrival; after it, nothing helps.
			bool Intercept()
			{
				if (Arrived) { return false; }
				Intercepted = true;
				return true;
			}

			bool InFlight() const { return !Arrived && !Intercepted; }
		};
	}
}
