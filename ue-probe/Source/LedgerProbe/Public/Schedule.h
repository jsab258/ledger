// TRANSLITERATION of the SCHEDULE section of ledger/Assets/Scripts/Core/Population.cs:
// IsRestDay, OutdoorsAt, OutdoorPosition and TripHours - who in the crowd is
// out of doors at a given day and hour, and where along their walk between
// home and work.
//
// WHY THIS FILE EXISTS, 23 September. ROADMAP's stage 3 is the crime loop in
// the stage-1 street "with the engine of consequence underneath it -
// perception, memory, gossip, schedules and save on the shipping engine".
// The Unreal port had perception, memory, gossip, the arrest and save; it had
// no schedules. Schedules matter to the moat because gossip only moves between
// people who are together, and who is together is decided here: the rumour-
// reach study of the same day (game-design/rumour-reach-2026-09-23.md) found
// the routines cut reach by about two thirds.
//
// TRANSLITERATION, NOT REWRITE, by the same rule as every other file here:
// the C# is the behavioural definition, every constant and branch matches its
// source, and the golden table is the proof rather than this comment: the
// IsRestDay, OutdoorsAt, OutdoorPositionX/Z and ScheduleConst rows, emitted by
// ledger/PerceptionGolden and answered in CoreGolden.h's Evaluate.
//
// THE ARITHMETIC IS C#'S `unchecked` int, EXACTLY. The per-person hashes rely
// on 32-bit wraparound on multiply and add, and on `>>` sign-extending a
// negative int. In C++ a signed overflow is undefined and a signed right shift
// was implementation-defined until C++20, so both are done here on uint32 and
// converted back, which is what the C# does in two's complement.
//
// SCOPE: the Core's schedule functions and nothing else. The crowd's
// generation (Population.Generate) draws from .NET's System.Random and is NOT
// PORTED; a resident arrives here as the four numbers the schedule reads.
// Where an indoor resident stands (work in working hours, else home) is the
// Game layer's PopulationHost.WhereIs and is NOT PORTED either. The named
// cast's authored routines are the next rung.
//
// CHECKED INDEPENDENTLY, 23 September, and it held: 1,753,729 inputs
// bit-exact against the real C# (int.MinValue and int.MaxValue for index,
// coordinates, day and hour included), about 8.8 billion more by checksum,
// and Sar against floor division over all 2^32 values. The golden rows were
// widened on its findings (every day of the week, a negative index, sixty
// people at every hour to pin the chance bands). ONE THING THE TABLE DOES
// NOT CARRY, on purpose: homes and works so far apart that their difference
// overflows. Sub wraps it as the C# does, but the shipping build's fast
// floating point differs in the last bit past about three million metres,
// beyond the table's 1e-9 bound, and the in-engine check would fail on
// arithmetic the game never meets.
//
// NO UNREAL TYPE IS IN THIS FILE, as with every Core module in the port: the
// arithmetic lives where the tests run.
#pragma once

#include <cstdint>

namespace LedgerCore
{
	namespace Schedule
	{
		/// What the schedule reads of a resident: its place in the population
		/// list, and where it sleeps and works, as the C# Resident's ints.
		struct Resident
		{
			int Index;
			int HomeX, HomeZ, WorkX, WorkZ;
			Resident() : Index(0), HomeX(0), HomeZ(0), WorkX(0), WorkZ(0) {}
		};

		/// How long one trip across the city lasts, in hours.
		const int TripHours = 3;

		namespace Detail
		{
			inline int32_t Mul(int32_t A, int32_t B) { return (int32_t)((uint32_t)A * (uint32_t)B); }
			inline int32_t Add(int32_t A, int32_t B) { return (int32_t)((uint32_t)A + (uint32_t)B); }
			inline int32_t Sub(int32_t A, int32_t B) { return (int32_t)((uint32_t)A - (uint32_t)B); }
			// C#'s >> on an int: arithmetic, the sign bit copied in.
			inline int32_t Sar(int32_t A, int N)
			{
				return A >= 0 ? (A >> N) : (int32_t)~((~(uint32_t)A) >> N);
			}
			inline int Mod(int V, int M) { return ((V % M) + M) % M; }
		}

		/// Day 0 is a Monday, so days 5 and 6 of each week are the rest days.
		inline bool IsRestDay(int Day) { return Detail::Mod(Day, 7) >= 5; }

		/// Is this person out of doors at this day and hour. Deterministic per
		/// person, day and hour.
		inline bool OutdoorsAt(const Resident& R, int Day, int Hour)
		{
			using namespace Detail;
			const int H = Mod(Hour, 24);
			const int Dy = Mod(Day, 7);
			int32_t Seed = Add(Add(Mul(R.Index, 486187739), Mul(H, 97)), Mul(Dy, 40503));
			Seed ^= Sar(Seed, 13);
			Seed = Mul(Seed, 1274126177);
			Seed ^= Sar(Seed, 16);
			const double Roll = (double)(Seed & 0x7FFFFFF) / (double)0x8000000;
			const double Chance = IsRestDay(Day)
				? (H >= 24 || H < 6 ? 0.03 :
				   H < 9 ? 0.06 :
				   H < 11 ? 0.14 :
				   H < 16 ? 0.22 :
				   H < 19 ? 0.17 :
				   H < 23 ? 0.14 :
				   0.05)
				: (H >= 23 || H < 5 ? 0.03 :
				   H < 7 ? 0.07 :
				   H < 9 ? 0.20 :
				   H < 12 ? 0.13 :
				   H < 14 ? 0.18 :
				   H < 17 ? 0.13 :
				   H < 19 ? 0.20 :
				   0.10);
			return Roll < Chance;
		}

		/// Where an outdoor resident is: along the line from home to work at a
		/// per-person, per-trip fraction, walking one way for the whole block
		/// of TripHours. False when they are indoors, and X and Z are then 0.
		inline bool OutdoorPosition(const Resident& R, int Day, int Hour, double& X, double& Z)
		{
			using namespace Detail;
			X = Z = 0.0;
			const int BlockStart = Mod(Hour, 24) / TripHours * TripHours;
			if (!OutdoorsAt(R, Day, BlockStart)) { return false; }
			const int H = Mod(Hour, 24);
			const int Block = H / TripHours;
			const int Dy = Mod(Day, 7);
			int32_t Seed = Add(Add(Add(Mul(R.Index, 486187739), Mul(Block, 40503)),
			                       Mul(Dy, 374761393)), 7);
			Seed ^= Sar(Seed, 15);
			Seed = Mul(Seed, 668265263);
			Seed ^= Sar(Seed, 13);
			const double Along = (double)(Seed & 0x7FFFFFF) / (double)0x8000000;
			const bool bOutbound = (Seed & 0x8000000) == 0;
			const double Through = ((double)(H % TripHours) + Along) / TripHours;
			double T = bOutbound ? Through : 1.0 - Through;
			T = 0.15 + 0.70 * T;
			X = (double)R.HomeX + (double)Sub(R.WorkX, R.HomeX) * T;
			Z = (double)R.HomeZ + (double)Sub(R.WorkZ, R.HomeZ) * T;
			return true;
		}
	}
}
