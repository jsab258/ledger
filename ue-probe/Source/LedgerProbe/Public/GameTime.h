// TRANSLITERATION of ledger/Assets/Scripts/Core/GameTime.cs, D1 probe.
//
// TRANSLITERATION, NOT REWRITE, and the distinction is the whole method: the
// C# suite is the behavioural definition, so every constant and every branch
// here matches its source line for line, and where the C# is subtle the
// comment explaining why travels with it. A port that "improved" something
// would make the two engines incomparable, which is the one thing D1 must
// not allow.
//
// SCOPE, from the crime ruling section 1 item 3: GameTime.cs 9 to 22 and 51.
// Day, Hour, Minute, the constructor, TotalMinutes, ToString and, from
// 2026-09-22, TryParse. THE COMMENT BELOW USED TO SAY "NO PARSING" and it was
// right until the crime encounter needed a witness's memory to survive a save
// and a reload: the save format is the memory markdown, reading it back means
// reading "D2 19:40" back, and that is this function. What is still not here
// is named here instead. NO SLOTS: TimeSlot, FromTotalMinutes, AddMinutes,
// HoursUntil, Slot, CompareTo, Equals and GetHashCode are not ported, because
// nothing the crime run does reads them and a member ported without a caller
// is a member nobody checks.
//
// NO UNREAL TYPE IS IN THIS FILE, deliberately, and it is the standing rule
// from 25 August rather than a preference: measurement arithmetic and
// formatting live where the tests run. This project's top layer does not
// compile in the container that writes it, so a formatter written there
// ships UNRUN and an unrun formatter printing a plausible string is the
// quietest instrument fault there is. ue-probe/tests/core-port-test.cpp
// compiles this with g++ and checks every line of it against a table the
// REAL C# emitted.
#pragma once

#include <string>
#include <vector>

#include <cstdio>
#include <string>

namespace LedgerCore
{
	// GameTime.cs 9 to 22. In-game time. Day 1 starts at 06:00; a "day" for
	// scheduling purposes runs 06:00..05:59. Engine-independent so the sim
	// and the tests can run headless, which is exactly why it ports at all.
	struct GameTime
	{
		int Day;
		int Hour;
		int Minute;

		GameTime() : Day(0), Hour(0), Minute(0) {}
		GameTime(int InDay, int InHour, int InMinute)
			: Day(InDay), Hour(InHour), Minute(InMinute) {}

		// GameTime.cs 22. long, not int, in the C# and long long here: the
		// product is days times 1440 and a campaign is allowed to be long.
		long long TotalMinutes() const
		{
			return ((long long)Day * 24 + Hour) * 60 + Minute;
		}

		// GameTime.cs 51: $"D{Day} {Hour:D2}:{Minute:D2}".
		//
		// THE ONE DIFFERENCE BETWEEN D2 AND %02d IS THE SIGN, and it is named
		// rather than left to be discovered: C# renders (-5).ToString("D2") as
		// "-05" and printf renders %02d as "-5". No negative hour or minute
		// can reach here (the only producer is a GameTime built by the probe
		// from a clock), so the two agree on every value this port sees, and
		// the golden table holds a row for the zero and the two-digit case.
		std::string ToString() const
		{
			char Buf[64];
			std::snprintf(Buf, sizeof(Buf), "D%d %02d:%02d", Day, Hour, Minute);
			return std::string(Buf);
		}

		// GameTime.cs 54 to 64. The inverse of ToString, and the C# branch by
		// branch: refuse empty or whitespace, refuse anything not starting
		// 'D', split the rest on spaces and colons DROPPING EMPTY PIECES, and
		// require exactly three integers.
		//
		// WHAT "int.TryParse" ACCEPTS, so this accepts the same and no more:
		// optional surrounding whitespace, an optional leading sign, then
		// digits. No decimal point, no exponent, no thousands separator under
		// the invariant culture's default integer style. A piece that is only
		// a sign is not a number and is refused, which C# also does.
		static bool TryParse(const std::string& S, GameTime& Out)
		{
			Out = GameTime();
			const std::string& T = S;
			// INDEX ZERO, NOT THE FIRST NON-BLANK, and the difference is a
			// real disagreement that was measured rather than reasoned about.
			// The C# is `IsNullOrWhiteSpace(s) || s[0] != 'D'` - it looks at
			// the FIRST CHARACTER. A port that skipped leading whitespace
			// first accepted "- [ D2 19:40] (...)" and loaded an event the C#
			// would have refused, which is exactly the hand-edit the
			// skip-the-bad-line behaviour exists to survive. An all-whitespace
			// string also fails this test, because its first character is not
			// 'D', so the two conditions collapse into one.
			if (T.empty() || T[0] != 'D') { return false; }
			std::vector<std::string> Parts;
			std::string Cur;
			for (std::string::size_type I = 1; I <= T.size(); ++I)
			{
				const char C = (I < T.size()) ? T[I] : ' ';
				if (C == ' ' || C == ':')
				{
					if (!Cur.empty()) { Parts.push_back(Cur); Cur.clear(); }   // RemoveEmptyEntries
				}
				else { Cur.push_back(C); }
			}
			if (Parts.size() != 3) { return false; }
			int V[3] = { 0, 0, 0 };
			for (int I = 0; I < 3; ++I)
			{
				if (!TryParseInt(Parts[I], V[I])) { return false; }
			}
			Out = GameTime(V[0], V[1], V[2]);
			return true;
		}

		// C# int.TryParse over the invariant culture's Integer style.
		static bool TryParseInt(const std::string& S, int& Out)
		{
			std::string::size_type B = S.find_first_not_of(" \t\r\n\f\v");
			std::string::size_type E = S.find_last_not_of(" \t\r\n\f\v");
			if (B == std::string::npos) { return false; }
			std::string T = S.substr(B, E - B + 1);
			std::string::size_type I = 0;
			bool bNeg = false;
			if (T[0] == '+' || T[0] == '-') { bNeg = (T[0] == '-'); I = 1; }
			if (I >= T.size()) { return false; }                   // a sign is not a number
			long long Acc = 0;
			for (; I < T.size(); ++I)
			{
				if (T[I] < '0' || T[I] > '9') { return false; }
				Acc = Acc * 10 + (T[I] - '0');
				// THE BOUND IS int's, AND IT IS NOT SYMMETRIC. int.MinValue is
				// -2147483648 and int.MaxValue is 2147483647, so a negative
				// number may reach one further than a positive one. Testing
				// the magnitude against MaxValue BEFORE applying the sign
				// refused "D-2147483648 0:0", which the C# accepts - measured
				// against the real C#, not reasoned about. Kept inside a long
				// long throughout so the accumulation itself cannot overflow.
				if (Acc > 2147483648LL) { return false; }
			}
			if (bNeg) { if (Acc > 2147483648LL) { return false; } }
			else      { if (Acc > 2147483647LL) { return false; } }
			Out = (int)(bNeg ? -Acc : Acc);
			return true;
		}
	};
}
