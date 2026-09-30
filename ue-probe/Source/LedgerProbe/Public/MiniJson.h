// TRANSLITERATION of ledger/Assets/Scripts/Core/MiniJson.cs's reader
// (Deserialize and what it calls), 29 September, for CastDay.h.
//
// WHY A SECOND READER when VignetteSpec.h has one. The independent check of
// the CastDay port (29 September) found the two readers disagree on files a
// person or a script writes: Python's json.dump writes every accented letter
// as an escape, which VignetteSpec.h's reader turns into '?', so a name with
// an accent would come out with a '?' and two places differing only by an
// accent would become one (today's cast files are plain ASCII, but a name
// with an accent is one edit away); "9-17" read as 9 and "5.5.2" as
// 5.5 where the C# refuses both, while "+5" and ".5", which the C# accepts,
// were refused; a key written twice kept its first value where the C# keeps
// its last; and whitespace the C# skips (a no-break space, \v, \f) was an
// error. The cast file is read by both engines and must mean the same thing
// in both, so it is read the C#'s way. VignetteSpec.h's reader stays as it is
// for the street's own files, which it has read correctly since September.
//
// THE SAME RULES, IN THE SAME ORDER: a value nested deeper than 200 is
// refused; whitespace is char.IsWhiteSpace's (the ASCII six, U+0085, U+00A0,
// U+1680, U+2000 to U+200A, U+2028, U+2029, U+202F, U+205F, U+3000); an
// object keeps a repeated key's last value in its first place (a C#
// Dictionary assigned twice); a string's escapes are the JSON eight and
// \uXXXX, anything else refused; a number is the longest run of
// "-+.eE0123456789", read as .NET's double.TryParse reads it under
// NumberStyles.Float and the invariant culture (an optional sign, digits with
// an optional point, or a point and digits, an optional exponent with digits)
// and refused otherwise; anything after the value is ignored. Strings are
// UTF-8: a \u escape becomes that character's UTF-8, a surrogate pair one
// character, a lone surrogate U+FFFD. Where the C# fails with an exception
// other than FormatException (a file cut off right after '{' or ',', or
// "\u-001"), this refuses by name.
//
// NO UNREAL TYPE IS IN THIS FILE. The value type is VignetteSpec.h's.
#pragma once

#include "VignetteSpec.h"   // LedgerVignette::Value

#include <clocale>
#include <cstdio>
#include <cstdlib>
#include <string>

namespace LedgerCore
{
namespace MiniJson
{
	struct FReader
	{
		const std::string& S;
		size_t P;
		std::string Err;
		explicit FReader(const std::string& InS) : S(InS), P(0) {}

		bool Fail(const std::string& Why)
		{
			if (Err.empty())
			{
				char Buf[32];
				std::snprintf(Buf, sizeof(Buf), " at %llu", (unsigned long long)P);
				Err = Why + Buf;
			}
			return false;
		}

		// The character at P, decoded from UTF-8, and its length in bytes.
		unsigned CharAt(size_t At, size_t& Len) const
		{
			const unsigned char C = (unsigned char)S[At];
			if (C < 0x80) { Len = 1; return C; }
			const int N = C >= 0xF0 ? 4 : C >= 0xE0 ? 3 : C >= 0xC0 ? 2 : 1;
			if (N == 1 || At + N > S.size()) { Len = 1; return 0xFFFD; }
			// A follower that is not 10xxxxxx makes the lead one bad byte, as .NET's
			// decoder does before the C# ever sees the text (the hints port's
			// independent check, 30 September: E2 80 41 read as U+2001 and ate the A).
			for (int I = 1; I < N; ++I) { if (((unsigned char)S[At + I] & 0xC0) != 0x80) { Len = 1; return 0xFFFD; } }
			unsigned Cp = C & (N == 2 ? 0x1F : N == 3 ? 0x0F : 0x07);
			for (int I = 1; I < N; ++I) Cp = (Cp << 6) | ((unsigned char)S[At + I] & 0x3F);
			// An overlong form, a surrogate or past U+10FFFF is a bad byte too, as
			// .NET decodes it (the police port's independent check, 30 September:
			// C0 A0 read as a space loaded a save the C# refuses).
			if ((N == 2 && Cp < 0x80) || (N == 3 && Cp < 0x800) || (N == 4 && (Cp < 0x10000 || Cp > 0x10FFFF)) || (Cp >= 0xD800 && Cp <= 0xDFFF) || C >= 0xF8)
			{
				Len = 1;
				return 0xFFFD;
			}
			Len = (size_t)N;
			return Cp;
		}

		static bool IsWhiteSpace(unsigned Cp)
		{
			return (Cp >= 0x09 && Cp <= 0x0D) || Cp == 0x20 || Cp == 0x85 || Cp == 0xA0 || Cp == 0x1680
			    || (Cp >= 0x2000 && Cp <= 0x200A) || Cp == 0x2028 || Cp == 0x2029 || Cp == 0x202F
			    || Cp == 0x205F || Cp == 0x3000;
		}

		void SkipWhitespace()
		{
			while (P < S.size())
			{
				size_t Len = 1;
				if (!IsWhiteSpace(CharAt(P, Len))) return;
				P += Len;
			}
		}

		static void AppendUtf8(std::string& Out, unsigned Cp)
		{
			if (Cp < 0x80) { Out += (char)Cp; }
			else if (Cp < 0x800) { Out += (char)(0xC0 | (Cp >> 6)); Out += (char)(0x80 | (Cp & 0x3F)); }
			else if (Cp < 0x10000) { Out += (char)(0xE0 | (Cp >> 12)); Out += (char)(0x80 | ((Cp >> 6) & 0x3F)); Out += (char)(0x80 | (Cp & 0x3F)); }
			else { Out += (char)(0xF0 | (Cp >> 18)); Out += (char)(0x80 | ((Cp >> 12) & 0x3F)); Out += (char)(0x80 | ((Cp >> 6) & 0x3F)); Out += (char)(0x80 | (Cp & 0x3F)); }
		}

		bool Hex4(size_t At, unsigned& Out) const
		{
			if (At + 4 > S.size()) return false;
			Out = 0;
			for (int I = 0; I < 4; ++I)
			{
				const char H = S[At + I];
				Out <<= 4;
				if (H >= '0' && H <= '9') Out |= (unsigned)(H - '0');
				else if (H >= 'a' && H <= 'f') Out |= (unsigned)(H - 'a' + 10);
				else if (H >= 'A' && H <= 'F') Out |= (unsigned)(H - 'A' + 10);
				else return false;
			}
			return true;
		}

		bool ParseString(std::string& Out)
		{
			if (P >= S.size() || S[P] != '"') return Fail("Expected string");
			++P;
			Out.clear();
			while (P < S.size())
			{
				const char C = S[P++];
				if (C == '"') return true;
				if (C != '\\') { Out += C; continue; }
				if (P >= S.size()) break;
				const char E = S[P++];
				switch (E)
				{
					case '"': Out += '"'; break;
					case '\\': Out += '\\'; break;
					case '/': Out += '/'; break;
					case 'n': Out += '\n'; break;
					case 'r': Out += '\r'; break;
					case 't': Out += '\t'; break;
					case 'b': Out += '\b'; break;
					case 'f': Out += '\f'; break;
					case 'u':
					{
						unsigned Cp = 0;
						if (!Hex4(P, Cp)) return Fail("Bad \\u escape");
						P += 4;
						// A PAIR IS ONE CHARACTER, as the two UTF-16 units the C#
						// appends are one; a lone half is U+FFFD.
						if (Cp >= 0xD800 && Cp <= 0xDBFF)
						{
							unsigned Lo = 0;
							if (P + 1 < S.size() && S[P] == '\\' && S[P + 1] == 'u' && Hex4(P + 2, Lo) && Lo >= 0xDC00 && Lo <= 0xDFFF)
							{
								P += 6;
								Cp = 0x10000 + ((Cp - 0xD800) << 10) + (Lo - 0xDC00);
							}
							else { Cp = 0xFFFD; }
						}
						else if (Cp >= 0xDC00 && Cp <= 0xDFFF) { Cp = 0xFFFD; }
						AppendUtf8(Out, Cp);
						break;
					}
					default: return Fail(std::string("Bad escape '\\") + E + "'");
				}
			}
			return Fail("Unterminated string");
		}

		// .NET's double.TryParse under NumberStyles.Float, for the characters
		// the slice can hold: [sign] digits [. digits] | [sign] . digits, then
		// [e [sign] digits].
		static bool IsFloat(const std::string& T)
		{
			size_t I = 0;
			if (I < T.size() && (T[I] == '+' || T[I] == '-')) ++I;
			size_t D1 = 0, D2 = 0;
			while (I < T.size() && T[I] >= '0' && T[I] <= '9') { ++I; ++D1; }
			if (I < T.size() && T[I] == '.')
			{
				++I;
				while (I < T.size() && T[I] >= '0' && T[I] <= '9') { ++I; ++D2; }
			}
			if (D1 + D2 == 0) return false;
			if (I < T.size() && (T[I] == 'e' || T[I] == 'E'))
			{
				++I;
				if (I < T.size() && (T[I] == '+' || T[I] == '-')) ++I;
				size_t D3 = 0;
				while (I < T.size() && T[I] >= '0' && T[I] <= '9') { ++I; ++D3; }
				if (D3 == 0) return false;
			}
			return I == T.size();
		}

		bool ParseNumber(double& Out)
		{
			const size_t Start = P;
			while (P < S.size() && std::string("-+.eE0123456789").find(S[P]) != std::string::npos) ++P;
			std::string T = S.substr(Start, P - Start);
			if (!IsFloat(T)) { P = Start; return Fail("Bad number '" + T + "'"); }
			// THE POINT IS THE LOCALE'S, whatever that is: strtod reads the
			// C library's current decimal point, so a '.' is handed to it as
			// that (the one character in the slice a locale changes).
			const char* Dp = std::localeconv() != 0 ? std::localeconv()->decimal_point : 0;
			if (Dp != 0 && Dp[0] != '\0' && Dp[0] != '.' && Dp[1] == '\0')
				for (size_t I = 0; I < T.size(); ++I) if (T[I] == '.') T[I] = Dp[0];
			Out = std::strtod(T.c_str(), 0);
			return true;
		}

		bool Expect(const char* Literal)
		{
			const std::string L(Literal);
			if (P + L.size() > S.size() || S.compare(P, L.size(), L) != 0) return Fail("Expected '" + L + "'");
			P += L.size();
			return true;
		}

		bool ParseValue(LedgerVignette::Value& Out, int Depth)
		{
			using namespace LedgerVignette;
			if (Depth > 200) return Fail("JSON nested too deeply (>200)");
			SkipWhitespace();
			if (P >= S.size()) return Fail("Unexpected end of JSON");
			const char C = S[P];
			if (C == '{') return ParseObject(Out, Depth);
			if (C == '[') return ParseArray(Out, Depth);
			if (C == '"') { Out.Type = T_STR; return ParseString(Out.Str); }
			if (C == 't') { Out.Type = T_BOOL; Out.Bool = true; return Expect("true"); }
			if (C == 'f') { Out.Type = T_BOOL; Out.Bool = false; return Expect("false"); }
			if (C == 'n') { Out.Type = T_NULL; return Expect("null"); }
			Out.Type = T_NUM;
			return ParseNumber(Out.Num);
		}

		bool ParseObject(LedgerVignette::Value& Out, int Depth)
		{
			using namespace LedgerVignette;
			Out.Type = T_OBJ;
			++P;
			SkipWhitespace();
			if (P < S.size() && S[P] == '}') { ++P; return true; }
			for (;;)
			{
				SkipWhitespace();
				std::string Key;
				if (!ParseString(Key)) return false;
				SkipWhitespace();
				if (P >= S.size() || S[P] != ':') return Fail("Expected ':'");
				++P;
				Value V;
				if (!ParseValue(V, Depth + 1)) return false;
				// dict[key] = value: a repeated key keeps its first place and
				// takes the last value
				bool bSet = false;
				for (size_t I = 0; I < Out.Obj.size() && !bSet; ++I)
					if (Out.Obj[I].first == Key) { Out.Obj[I].second = V; bSet = true; }
				if (!bSet) Out.Obj.push_back(std::make_pair(Key, V));
				SkipWhitespace();
				if (P >= S.size()) return Fail("Unterminated object");
				if (S[P] == ',') { ++P; continue; }
				if (S[P] == '}') { ++P; return true; }
				return Fail("Expected ',' or '}'");
			}
		}

		bool ParseArray(LedgerVignette::Value& Out, int Depth)
		{
			using namespace LedgerVignette;
			Out.Type = T_ARR;
			++P;
			SkipWhitespace();
			if (P < S.size() && S[P] == ']') { ++P; return true; }
			for (;;)
			{
				Value V;
				if (!ParseValue(V, Depth + 1)) return false;
				Out.Arr.push_back(V);
				SkipWhitespace();
				if (P >= S.size()) return Fail("Unterminated array");
				if (S[P] == ',') { ++P; continue; }
				if (S[P] == ']') { ++P; return true; }
				return Fail("Expected ',' or ']'");
			}
		}
	};

	/// MiniJson.Deserialize: false with the reason where the C# throws.
	inline bool Deserialize(const std::string& Json, LedgerVignette::Value& Out, std::string& Err)
	{
		FReader R(Json);
		Out = LedgerVignette::Value();
		const bool bOk = R.ParseValue(Out, 0);
		Err = R.Err;
		return bOk;
	}

	/// string.Trim(): char.IsWhiteSpace at both ends, over UTF-8.
	inline std::string Trim(const std::string& S)
	{
		FReader R(S);
		size_t B = 0;
		while (B < S.size())
		{
			size_t Len = 1;
			if (!FReader::IsWhiteSpace(R.CharAt(B, Len))) break;
			B += Len;
		}
		size_t E = S.size();
		while (E > B)
		{
			size_t Start = E - 1;
			while (Start > B && ((unsigned char)S[Start] & 0xC0) == 0x80) --Start;
			size_t Len = 1;
			if (!FReader::IsWhiteSpace(R.CharAt(Start, Len))) break;
			E = Start;
		}
		return S.substr(B, E - B);
	}
}
}
