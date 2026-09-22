// TRANSLITERATION of ledger/Assets/Scripts/Core/MemoryStore.cs, D1 probe.
//
// TRANSLITERATION, NOT REWRITE, and the distinction is the whole method: the
// C# suite is the behavioural definition, so every constant and every branch
// here matches its source line for line, and where the C# is subtle the
// comment explaining why travels with it. A port that "improved" something
// would make the two engines incomparable, which is the one thing D1 must
// not allow.
//
// SCOPE, from the crime ruling section 1 item 4: MemoryEvent 8 to 24;
// MemoryStore 52 to 91 IN MEMORY ONLY (Append), EventsOnDay 231 to 232,
// ToMarkdown 255 to 266. The markdown IS the artefact of "permanently
// remember" and the crime run commits it. MaxEvents, PruneTo and Prune were
// in that scope until the queue 115 ruling of 2026-09-14 deleted them from
// the C# and from here in the same change.
//
// _filePath WAS ALWAYS NULL HERE, and from 2026-09-22 that is only half
// true. The crime encounter has to prove that what a witness knows survives a
// save, a restart and a reload, and in this engine THE SAVE FORMAT IS THE
// MARKDOWN: SaveCodec's own summary says NPC memories persist separately as
// markdown and are not in the save file, ToMarkdown writes that text and
// LoadFrom reads the very same text back. So LoadFrom and MemoryEvent.FromLine
// ARE PORTED NOW, checked against the C# by the save_reload rows of the golden
// table. Save and AppendToFile are still not here - writing the file is the
// caller's business in this build, and it writes exactly ToMarkdown's string -
// and neither is ReplaceBeliefs. Each site where the C# would have touched a
// file still says so below.
//
// NO UNREAL TYPE IS IN THIS FILE, deliberately, and it is the standing rule
// from 25 August rather than a preference: measurement arithmetic and
// formatting live where the tests run, because a formatter written in this
// project's top layer ships UNRUN and an unrun formatter printing a
// plausible string is the quietest instrument fault there is.
#pragma once

#include "GameTime.h"
#include "Perception.h"   // LedgerCore::Clamp

#include <cstdio>
#include <limits>
#include <cstring>
#include <cstdlib>
#include <string>
#include <vector>

namespace LedgerCore
{
	// C# Trim() over ASCII. C#'s Trim removes Unicode whitespace and this
	// removes the six ASCII ones; every string this probe builds is ASCII by
	// construction (ids, bank lines, the summaries in Gossip.cs), so the two
	// agree on everything in the crime run, and the difference is named here
	// rather than assumed away.
	inline std::string TrimAscii(const std::string& S)
	{
		const char* Ws = " \t\n\v\f\r";
		const std::string::size_type A = S.find_first_not_of(Ws);
		if (A == std::string::npos) { return std::string(); }
		const std::string::size_type B = S.find_last_not_of(Ws);
		return S.substr(A, B - A + 1);
	}

	// C# string.Replace(old, new): EVERY occurrence, not the first.
	inline std::string ReplaceAll(const std::string& S, const std::string& From,
	                              const std::string& To)
	{
		if (From.empty()) { return S; }
		std::string Out;
		std::string::size_type P = 0;
		for (;;)
		{
			const std::string::size_type At = S.find(From, P);
			if (At == std::string::npos) { Out.append(S, P, S.size() - P); return Out; }
			Out.append(S, P, At - P);
			Out += To;
			P = At + From.size();
		}
	}

	// THE SHORTEST DECIMAL THAT READS BACK AS THIS DOUBLE, which is what
	// .NET's "R" and .NET Core 3.0's default double formatting produce. Used
	// by the golden table to write a double, and NOT by FormatTwoDecimals:
	// see the measurement below.
	inline std::string ShortestRoundTrip(double V)
	{
		char Buf[64];
		for (int Prec = 1; Prec <= 17; ++Prec)
		{
			std::snprintf(Buf, sizeof(Buf), "%.*g", Prec, V);
			if (std::strtod(Buf, 0) == V) { return std::string(Buf); }
		}
		return std::string(Buf);
	}

	// Increment a string of decimal digits by one, carrying leftwards.
	inline std::string IncrementDigits(const std::string& In)
	{
		std::string D = In;
		for (int I = (int)D.size() - 1; I >= 0; --I)
		{
			if (D[I] != '9') { D[I] = (char)(D[I] + 1); return D; }
			D[I] = '0';
		}
		return "1" + D;
	}

	// FIFTEEN SIGNIFICANT DIGITS, which is where .NET starts a custom format
	// string. Not the shortest round-trip: the two differ and the difference
	// is measured below.
	inline std::string FifteenSignificantDigits(double V)
	{
		char Buf[64];
		std::snprintf(Buf, sizeof(Buf), "%.15g", V);
		return std::string(Buf);
	}

	// C#'s Importance.ToString("0.00", InvariantCulture), AND IT IS NEITHER
	// printf("%.2f") NOR A ROUNDING OF THE SHORTEST ROUND-TRIP. Two
	// measurements, both taken in this container against .NET 8 and glibc,
	// and the second one exists because the first was set from a series that
	// did not contain the case the rule is about (rule 2).
	//
	// MEASUREMENT ONE, six values, C# "0.00" against C printf %.2f:
	//
	//     value    C# "0.00"    C printf %.2f
	//     0.125      0.13           0.12
	//     0.015      0.02           0.01
	//     0.045      0.05           0.04
	//     0.345      0.35           0.34
	//     0.135      0.14           0.14
	//     0.005      0.01           0.01
	//
	// printf rounds the exact BINARY value half to even, so 0.125 (exactly
	// representable) goes down to 0.12. C# rounds a DECIMAL digit buffer half
	// away from zero, so it goes up to 0.13. A port using %.2f would have
	// written a different importance into the memory markdown the crime run
	// COMMITS, for every value on a binary-exact or below-half boundary, and
	// the difference would have been invisible until somebody diffed two
	// engines' memory files by eye.
	//
	// MEASUREMENT TWO, ordered by the director's ruling of 2026-09-08 because
	// the first left the rule underdetermined. Which decimal buffer? .NET's
	// Number.Formatting.cs sets DoublePrecisionCustomFormat = 15, so a custom
	// format renders FIFTEEN SIGNIFICANT DIGITS first; the alternative reading
	// was the shortest decimal that round-trips. Both agree on every value in
	// measurement one, the longest of which is five digits. They part one ulp
	// below a half, which is exactly what a product of three factors makes.
	// Measured, C# on the two neighbour doubles:
	//
	//     Math.BitDecrement(0.125) = 0.12499999999999999 -> "0.00" gives 0.13
	//     Math.BitDecrement(0.135) = 0.13499999999999998 -> "0.00" gives 0.14
	//
	// So the fifteen-digit reading is the right one and the shortest
	// round-trip reading is wrong: it would have rendered 0.12499999999999999
	// and printed 0.12. glibc's %.15g gives 0.125 and 0.135 for those two
	// doubles, which is the same buffer .NET builds, and the golden table
	// carries both rows so the rule is a thing the table checked rather than
	// a thing this comment claims.
	inline std::string FormatTwoDecimals(double V)
	{
		// THE THREE VALUES THAT ARE NOT NUMBERS, and they reach here for real
		// rather than in theory. C# Math.Clamp(NaN, 0, 1) is NaN, so a NaN
		// importance survives the constructor and arrives at ToLine, where
		// C#'s "0.00" format renders it as the invariant culture's own symbol,
		// "NaN" - and the engine then writes that into a memory file and reads
		// it straight back. The digit path below produced "nan.00" for it,
		// which the golden table caught the moment a NaN row existed to catch
		// it. The infinities cannot survive Clamp on this path, but this is a
		// general formatter.
		//
		// ONLY NaN IS HANDLED, and the two infinities deliberately are not.
		// Clamp turns them into 1.0 and 0.0 before ToLine ever sees them, so a
		// branch for either could never run, and a branch nothing can reach is
		// a branch no test can check. NaN is different: Clamp passes it
		// through, every comparison against it being false, which is why it
		// arrives here and why the golden table now carries a row for it.
		//
		// NOT `V != V`, AND NOT std::isnan, AND THE REASON IS THE WHOLE POINT
		// OF HAVING A REAL BUILD. Unreal compiles this module with fast
		// floating point, under which the compiler is entitled to assume no
		// NaN can exist and folds both of those tests to false. The container
		// where the port's tests run does not, so the same source answered
		// "NaN" on every machine a test runs on and "0.00" inside the engine,
		// and the golden table caught it on the first real build - the
		// in-engine comparison went red with one mismatch while g++ and MSVC
		// both said the port agreed. The bits are the only test that survives
		// the optimiser: exponent all ones, fraction not zero.
		if (IsNaNBits(V)) { return "NaN"; }
		const bool bNeg = V < 0.0;
		const std::string S = FifteenSignificantDigits(bNeg ? -V : V);

		// value = Digits * 10^(Exp - FracLen)
		std::string Mant = S;
		int Exp = 0;
		const std::string::size_type EAt = S.find_first_of("eE");
		if (EAt != std::string::npos)
		{
			Mant = S.substr(0, EAt);
			Exp = std::atoi(S.c_str() + EAt + 1);
		}
		int FracLen = 0;
		std::string Digits;
		const std::string::size_type Dot = Mant.find('.');
		if (Dot == std::string::npos) { Digits = Mant; }
		else
		{
			Digits = Mant.substr(0, Dot) + Mant.substr(Dot + 1);
			FracLen = (int)(Mant.size() - Dot - 1);
		}
		if (Digits.empty()) { Digits = "0"; }

		// Shift so the last kept digit is the hundredths place.
		const int Shift = (Exp - FracLen) + 2;
		std::string Kept;
		if (Shift >= 0)
		{
			Kept = Digits;
			Kept.append((std::string::size_type)Shift, '0');
		}
		else
		{
			const int Drop = -Shift;
			char FirstDropped = '0';
			if (Drop >= (int)Digits.size())
			{
				if (Drop == (int)Digits.size()) { FirstDropped = Digits[0]; }
				Kept = "0";
			}
			else
			{
				FirstDropped = Digits[Digits.size() - (std::string::size_type)Drop];
				Kept = Digits.substr(0, Digits.size() - (std::string::size_type)Drop);
			}
			// HALF AWAY FROM ZERO, on the fifteen-digit decimal buffer, which
			// is the rule both measurements above support. Half to even here
			// would print 0.12 for 0.125.
			if (FirstDropped >= '5') { Kept = IncrementDigits(Kept); }
		}

		while (Kept.size() < 3) { Kept = "0" + Kept; }
		std::string Whole = Kept.substr(0, Kept.size() - 2);
		// Strip the leading zeros C# would not print, but keep one digit.
		std::string::size_type NZ = Whole.find_first_not_of('0');
		Whole = (NZ == std::string::npos) ? std::string("0") : Whole.substr(NZ);
		return (bNeg ? "-" : "") + Whole + "." + Kept.substr(Kept.size() - 2);
	}

	// C# string.Trim() REMOVES UNICODE WHITESPACE, not just the six ASCII
	// ones, and that mattered from the day this file's markdown became a save
	// people are invited to hand-edit. "## Beliefs" followed by a non-breaking
	// space is a section heading to the C# and a heading called
	// "Beliefs\u00a0" to an ASCII-only trim, so every belief under it was
	// dropped by one engine and kept by the other. Measured, not reasoned
	// about.
	//
	// THE LIST IS char.IsWhiteSpace's, in UTF-8. Everything the C# would strip
	// and nothing else: NEL, NBSP, OGHAM SPACE, the EN/EM quad family, LINE
	// and PARAGRAPH SEPARATOR, NARROW NO-BREAK, MEDIUM MATHEMATICAL and
	// IDEOGRAPHIC SPACE.
	// ASCII case folding, which is all the invariant culture does for these
	// three symbols.
	inline bool EqualsIgnoreAsciiCase(const std::string& A, const std::string& B)
	{
		if (A.size() != B.size()) { return false; }
		for (std::string::size_type I = 0; I < A.size(); ++I)
		{
			char X = A[I], Y = B[I];
			if (X >= 'A' && X <= 'Z') { X = (char)(X - 'A' + 'a'); }
			if (Y >= 'A' && Y <= 'Z') { Y = (char)(Y - 'A' + 'a'); }
			if (X != Y) { return false; }
		}
		return true;
	}

	inline bool IsUnicodeSpaceAt(const std::string& S, std::string::size_type I,
	                             std::string::size_type& Width)
	{
		const unsigned char A = (unsigned char)S[I];
		const unsigned char B = (I + 1 < S.size()) ? (unsigned char)S[I + 1] : 0;
		const unsigned char C = (I + 2 < S.size()) ? (unsigned char)S[I + 2] : 0;
		if (A == 0xC2 && (B == 0x85 || B == 0xA0)) { Width = 2; return true; }
		if (A == 0xE1 && B == 0x9A && C == 0x80)   { Width = 3; return true; }  // U+1680
		if (A == 0xE2 && B == 0x80 && C <= 0x8A && C >= 0x80) { Width = 3; return true; }
		if (A == 0xE2 && B == 0x80 && (C == 0xA8 || C == 0xA9 || C == 0xAF))
		{
			Width = 3; return true;
		}
		if (A == 0xE2 && B == 0x81 && C == 0x9F)   { Width = 3; return true; }  // U+205F
		if (A == 0xE3 && B == 0x80 && C == 0x80)   { Width = 3; return true; }  // U+3000
		Width = 0;
		return false;
	}

	inline std::string TrimUnicode(const std::string& S)
	{
		std::string::size_type B = 0, E = S.size();
		for (;;)
		{
			if (B >= E) { return std::string(); }
			std::string::size_type W = 0;
			const char Ch = S[B];
			if (Ch == ' ' || Ch == '\t' || Ch == '\r' || Ch == '\n' || Ch == '\f' || Ch == '\v')
			{
				++B; continue;
			}
			if (IsUnicodeSpaceAt(S, B, W)) { B += W; continue; }
			break;
		}
		for (;;)
		{
			if (E <= B) { break; }
			const char Ch = S[E - 1];
			if (Ch == ' ' || Ch == '\t' || Ch == '\r' || Ch == '\n' || Ch == '\f' || Ch == '\v')
			{
				--E; continue;
			}
			bool bTrimmed = false;
			for (std::string::size_type W = 2; W <= 3; ++W)
			{
				std::string::size_type Got = 0;
				if (E >= B + W && IsUnicodeSpaceAt(S, E - W, Got) && Got == W)
				{
					E -= W; bTrimmed = true; break;
				}
			}
			if (!bTrimmed) { break; }
		}
		return S.substr(B, E - B);
	}

	// MemoryStore.cs 8 to 24.
	class MemoryEvent
	{
	public:
		GameTime    Time;
		std::string Kind;        // conversation | observation | heard | reflection
		double      Importance;  // 0..1
		std::string Text;

		MemoryEvent(const GameTime& InTime, const std::string& InKind,
		            double InImportance, const std::string& InText)
			: Time(InTime), Kind(InKind),
			  Importance(Clamp(InImportance, 0.0, 1.0)),
			  Text(TrimAscii(ReplaceAll(InText, "\n", " ")))
		{
		}

		// MemoryStore.cs 22 to 23.
		std::string ToLine() const
		{
			return "- [" + Time.ToString() + "] (" + FormatTwoDecimals(Importance)
			     + "|" + Kind + ") " + Text;
		}

		// MemoryStore.cs 26 to 50, branch for branch. Returns false where the
		// C# returns null, and every one of the C#'s eight refusals is here:
		// a line not starting "- [", no closing bracket, an unparseable time,
		// no opening paren, no closing paren AFTER it, a metadata field count
		// that is not two, and an unparseable importance.
		//
		// THE CLOSING PAREN IS SEARCHED FOR FROM THE OPENING ONE, which is the
		// C#'s own comment and its own bug once: a ')' earlier in the line -
		// a hand-edited ":)" before the metadata - would otherwise be picked
		// up, the substring length would go negative and throw, and ONE
		// MALFORMED LINE WOULD ABORT THE WHOLE MEMORY LOAD. On this path that
		// is a witness who saw the crime forgetting it because somebody edited
		// a file. Skip the line; keep the memory.
		static bool TryFromLine(const std::string& Line, MemoryEvent& Out)
		{
			const std::string T = TrimUnicode(Line);
			if (T.size() < 3 || T.compare(0, 3, "- [") != 0) { return false; }
			const std::string::size_type CloseBracket = T.find(']');
			if (CloseBracket == std::string::npos) { return false; }
			GameTime Time;
			if (!GameTime::TryParse(T.substr(3, CloseBracket - 3), Time)) { return false; }

			const std::string::size_type OpenParen = T.find('(', CloseBracket);
			if (OpenParen == std::string::npos) { return false; }
			const std::string::size_type CloseParen = T.find(')', OpenParen);
			if (CloseParen == std::string::npos) { return false; }

			const std::string Meta = T.substr(OpenParen + 1, CloseParen - OpenParen - 1);
			std::vector<std::string> Fields;
			std::string Cur;
			for (std::string::size_type I = 0; I <= Meta.size(); ++I)
			{
				if (I == Meta.size() || Meta[I] == '|') { Fields.push_back(Cur); Cur.clear(); }
				else { Cur.push_back(Meta[I]); }
			}
			if (Fields.size() != 2) { return false; }
			double Importance = 0.0;
			if (!TryParseDouble(Fields[0], Importance)) { return false; }

			Out = MemoryEvent(Time, Fields[1], Importance,
			                  TrimUnicode(T.substr(CloseParen + 1)));
			return true;
		}

		// C# double.TryParse under NumberStyles.Float and the invariant
		// culture: optional surrounding whitespace, an optional leading sign,
		// digits with at most one '.', and an optional exponent. NOT hex, and
		// NOT the bare "inf" that strtod would take.
		//
		// BUT NaN AND Infinity ARE ACCEPTED, and the first version of this
		// function had that backwards. On .NET Core 3.0 and later TryParse
		// falls back to the culture's NaN and Infinity symbols OUTSIDE the
		// NumberStyles check, so "NaN", "nan", "Infinity", "+Infinity",
		// "-Infinity" and "INFINITY" all parse while "inf" does not - measured
		// against the real C#, not reasoned about.
		//
		// AND IT IS NOT A CURIOSITY. Math.Clamp(NaN, 0, 1) is NaN, and ToLine
		// renders NaN as the literal "NaN", so the C# ENGINE ITSELF writes
		// "(NaN|heard)" into a memory file and reads it straight back. A port
		// that refused it would silently drop a memory the C# keeps, on a file
		// the C# wrote.
		static bool TryParseDouble(const std::string& S, double& Out)
		{
			std::string::size_type B = S.find_first_not_of(" \t\r\n\f\v");
			std::string::size_type E = S.find_last_not_of(" \t\r\n\f\v");
			if (B == std::string::npos) { return false; }
			const std::string T = S.substr(B, E - B + 1);
			if (EqualsIgnoreAsciiCase(T, "nan"))
			{
				Out = std::numeric_limits<double>::quiet_NaN(); return true;
			}
			if (EqualsIgnoreAsciiCase(T, "infinity") || EqualsIgnoreAsciiCase(T, "+infinity"))
			{
				Out = std::numeric_limits<double>::infinity(); return true;
			}
			if (EqualsIgnoreAsciiCase(T, "-infinity"))
			{
				Out = -std::numeric_limits<double>::infinity(); return true;
			}
			std::string::size_type I = 0;
			if (T[I] == '+' || T[I] == '-') { ++I; }
			int Digits = 0, Dots = 0;
			for (; I < T.size(); ++I)
			{
				if (T[I] >= '0' && T[I] <= '9') { ++Digits; continue; }
				if (T[I] == '.') { if (++Dots > 1) { return false; } continue; }
				if (T[I] == 'e' || T[I] == 'E') { break; }
				return false;
			}
			if (Digits == 0) { return false; }
			if (I < T.size())                       // an exponent, and it must be whole
			{
				++I;
				if (I < T.size() && (T[I] == '+' || T[I] == '-')) { ++I; }
				int ExpDigits = 0;
				for (; I < T.size(); ++I)
				{
					if (T[I] < '0' || T[I] > '9') { return false; }
					++ExpDigits;
				}
				if (ExpDigits == 0) { return false; }
			}
			Out = std::strtod(T.c_str(), 0);
			return true;
		}
	};

	// MemoryStore.cs 52 to 91, 231 to 232, 255 to 266. One character's
	// persistent memory: an append-only event stream plus a small set of
	// distilled beliefs. Stored as human-readable markdown so memories can be
	// inspected, debugged and hand-edited.
	class MemoryStore
	{
	public:
		// MemoryStore.cs 52 to 71. NOTHING IS EVER WIPED: canon.md line 99
		// and pillar 1. MaxEvents = 600 and PruneTo = 500 stood here, ported
		// from the C#, until Jafar ruled queue 115 on 2026-09-14 ("canon
		// stands, the code changes"), and both sides dropped them together.
		// They are named here because a reader of the D1 probe's record will
		// come looking for them: the golden scenario that pinned them is now
		// mem_permanent and pins their absence instead.
		//
		// THE BUDGET HALF IS NOT PORTED: BytesPerEvent, ProjectedBytes,
		// AffordableEventsPerNpcPerDay, BudgetLine and the four constants
		// beside them (MemoryStore.cs 93 to 206). They model the .NET heap,
		// which is not what this engine allocates, so a transliteration of
		// them would be a number that looked measured and was not. Their live
		// caller is SimDirector's verdict line, which is Unity and outside
		// this port's scope entirely.

		std::string CharacterId;

		// THE BELIEFS LIST IS PORTED AND IS ALWAYS EMPTY, and saying so is
		// the point. ToMarkdown writes a "## Beliefs" section whether or not
		// anything fills it, so dropping the field would have changed the
		// committed artefact. Nothing in scope can fill it: ReplaceBeliefs
		// (113 to 122) and LoadFrom (127 to 146) are the only two writers in
		// the C# and neither is ported.
		std::vector<std::string> Beliefs;
		std::vector<MemoryEvent> Events;

		explicit MemoryStore(const std::string& InCharacterId)
			: CharacterId(InCharacterId)
		{
			// MemoryStore.cs 80 to 85: the constructor's second argument is
			// the file path and it is null here by the ruling, so the
			// LoadFrom(File.ReadAllText(...)) branch cannot be taken and is
			// not ported.
		}

		// MemoryStore.cs 87 to 91.
		void Append(const MemoryEvent& E)
		{
			Events.push_back(E);
			// C# branch: if (!AppendToFile(e)) Save(). For an in-memory store
			// AppendToFile returns true at its first line, so nothing
			// happens; not ported. The cap-and-prune branch that stood above
			// this one went with the queue 115 ruling on both sides.
		}

		// MemoryStore.cs 231 to 232.
		// MemoryStore.cs 234 to 253. THE RELOAD, and it is the other half of
		// ToMarkdown rather than a second format: the string this reads is
		// exactly the string that writes.
		//
		// IT REPLACES, IT DOES NOT APPEND. Beliefs and Events are cleared
		// first, which is the difference between restoring a save and
		// doubling it, and the golden table holds a row for loading the same
		// markdown twice.
		//
		// A LINE IT CANNOT READ IS SKIPPED, NOT FATAL. Anything outside a
		// "## " section is ignored, a Beliefs line that is not "- ..." is
		// ignored, and an Events line TryFromLine refuses is ignored. One
		// hand-edited line must not cost a witness everything she saw.
		void LoadFrom(const std::string& Markdown)
		{
			Beliefs.clear();
			Events.clear();
			const std::string Text = ReplaceAll(Markdown, "\r\n", "\n");
			std::string Section;
			std::string Raw;
			for (std::string::size_type I = 0; I <= Text.size(); ++I)
			{
				if (I < Text.size() && Text[I] != '\n') { Raw.push_back(Text[I]); continue; }
				if (Raw.size() >= 3 && Raw.compare(0, 3, "## ") == 0)
				{
					Section = TrimUnicode(Raw.substr(3));
				}
				else if (Section == "Beliefs")
				{
					const std::string T = TrimUnicode(Raw);
					if (T.size() >= 2 && T.compare(0, 2, "- ") == 0)
					{
						Beliefs.push_back(TrimUnicode(T.substr(2)));
					}
				}
				else if (Section == "Events")
				{
					MemoryEvent E(GameTime(), "", 0.0, "");
					if (MemoryEvent::TryFromLine(Raw, E)) { Events.push_back(E); }
				}
				Raw.clear();
			}
		}

		std::vector<MemoryEvent> EventsOnDay(int Day) const
		{
			std::vector<MemoryEvent> Out;
			for (std::vector<MemoryEvent>::size_type I = 0; I < Events.size(); ++I)
			{
				if (Events[I].Time.Day == Day) { Out.push_back(Events[I]); }
			}
			return Out;
		}

		// MemoryStore.cs 255 to 266. AppendLine is "\n" here: the C# uses
		// StringBuilder.AppendLine, whose separator is Environment.NewLine
		// and is therefore "\r\n" on Jafar's Windows PC and "\n" on the Linux
		// container. THE PORT WRITES "\n" ALWAYS and the golden comparison
		// normalises, because a line ending is a platform fact and not a
		// behaviour of the memory model; the committed artefact is compared
		// line by line, never byte by byte.
		std::string ToMarkdown() const
		{
			std::string Sb;
			Sb += "# Memory: " + CharacterId + "\n";
			Sb += "\n";
			Sb += "## Beliefs\n";
			for (std::vector<std::string>::size_type I = 0; I < Beliefs.size(); ++I)
			{
				Sb += "- " + Beliefs[I] + "\n";
			}
			Sb += "\n";
			Sb += "## Events\n";
			for (std::vector<MemoryEvent>::size_type I = 0; I < Events.size(); ++I)
			{
				Sb += Events[I].ToLine() + "\n";
			}
			return Sb;
		}

	};
}
