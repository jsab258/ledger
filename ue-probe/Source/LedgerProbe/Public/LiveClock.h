// THE CLOCK THAT RUNS WITH PLAY, 30 September (Jafar's list after the outside
// audit, item 1: "the clock running as the first-week handovers need it ...
// with no waiting forty seconds and no jump to day four").
//
// The town's own figure (production/handovers/6ci-the-wait.md; the first hour
// on paper, game-design/first-hour-on-paper-2026-09-29.md): the day runs at two
// game minutes a real second, twelve real minutes a day, so the first real hour
// of play reaches day 5 from nine on day 1. Held (it does not move) while the
// caller says so: paused, and wherever the game decides time stands still.
//
// Every hour it crosses is handed back, in order, each exactly once, whether
// crossed by play or by a wait: the town's hourly work (its talk, the damage
// found, the morning's police) runs once per hour and never twice, the rule
// TownHours.RunTo already keeps for the talk. A wait jumps to its end the same
// way, an hour at a time, so nothing scheduled inside it is stepped over.
//
// Saved as whole minutes and the fraction of one; a load puts the clock back
// exactly where it was.
//
// NO UNREAL TYPE IS IN THIS FILE, so the port's standalone test can run it
// (ue-probe/tests/core-port-test.cpp).
#pragma once

#include "GameTime.h"

#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <string>
#include <vector>

namespace LedgerCore
{
	class LiveClock
	{
	public:
		/// Two game minutes a real second (the town, 29 September).
		static constexpr double MinutesPerRealSecond = 2.0;
		/// A real frame longer than this counts as this much (a hitch, a
		/// breakpoint, a slow load): the street never loses an afternoon to a stall.
		static constexpr double LongestStepSeconds = 1.0;

		LiveClock() {}
		explicit LiveClock(const GameTime& Start) : Minutes(Start.TotalMinutes()) {}

		GameTime Now() const { return GameTime::FromTotalMinutes(Minutes); }
		long long TotalMinutes() const { return Minutes; }
		double Fraction() const { return Frac; }

		/// Play moves the clock by RealSeconds, unless held. Returns the start
		/// of each hour crossed, in order.
		std::vector<GameTime> Advance(double RealSeconds, bool bHeld)
		{
			std::vector<GameTime> Hours;
			if (bHeld || !(RealSeconds > 0.0)) return Hours;   // also refuses NaN
			const double Step = RealSeconds > LongestStepSeconds ? LongestStepSeconds : RealSeconds;
			Frac += Step * MinutesPerRealSecond;
			// A billionth of a minute's tolerance: sixty frames a second add a
			// thirtieth of a minute each, which never sums to exactly one in
			// floating point, and a day came out a minute short without it.
			const double Whole = std::floor(Frac + 1e-9);
			Frac -= Whole;
			if (Frac < 0.0) Frac = 0.0;
			return MoveBy((long long)Whole);
		}

		/// A wait (or a black screen) moves the clock straight to To, if it is
		/// later. Returns the start of each hour crossed, in order.
		std::vector<GameTime> JumpTo(const GameTime& To)
		{
			const long long Target = To.TotalMinutes();
			if (Target <= Minutes) return std::vector<GameTime>();
			Frac = 0.0;
			return MoveBy(Target - Minutes);
		}

		/// "minutes|fraction", read back by FromText.
		std::string ToText() const
		{
			char Buf[64];
			std::snprintf(Buf, sizeof(Buf), "%lld|%.6f", Minutes, Frac);
			return Buf;
		}

		/// False, leaving the clock as it is, for anything it cannot read.
		bool FromText(const std::string& Text)
		{
			const std::string::size_type Bar = Text.find('|');
			if (Bar == std::string::npos) return false;
			char* End = nullptr;
			const std::string M = Text.substr(0, Bar), F = Text.substr(Bar + 1);
			const long long Mins = std::strtoll(M.c_str(), &End, 10);
			if (M.empty() || End == nullptr || *End != '\0' || Mins < 0) return false;
			const double Fr = std::strtod(F.c_str(), &End);
			if (F.empty() || End == nullptr || *End != '\0' || !(Fr >= 0.0 && Fr < 1.0)) return false;
			Minutes = Mins;
			Frac = Fr;
			return true;
		}

	private:
		long long Minutes = 0;
		double Frac = 0.0;

		std::vector<GameTime> MoveBy(long long Delta)
		{
			std::vector<GameTime> Hours;
			const long long From = Minutes;
			Minutes += Delta;
			// Every hour start in (From, Minutes].
			for (long long H = (From / 60 + 1) * 60; H <= Minutes; H += 60)
				Hours.push_back(GameTime::FromTotalMinutes(H));
			return Hours;
		}
	};
}
