// SaveCodec.h - the rumour half of the save, read the way the C# reads it.
//
// WHAT THIS IS FOR. A memory's save format IS the markdown: SaveCodec's own
// summary in the C# says NPC memories persist separately as markdown and are
// not in the save file, and MemoryStore already writes and reads that text on
// both engines. A RUMOUR is not in that markdown. It lives in the GossipMill,
// and the mill goes into the save FILE as JSON under "agents" - each agent's
// loyalty, leash, suspicion, suppressed topics, rumours and learned facts.
// That is a different format with a different parser and a different set of
// ways to lose something, and this port had none of it. Until it does, a
// rumour in flight cannot be shown to survive a restart in the engine the
// game actually ships in.
//
// WHY A SCANNER AND NOT A JSON MODULE, which is the same answer CrimeProbe.h
// gives for the same question and for the same reason: LedgerProbe.Build.cs
// names Core, CoreUObject, Engine, ImageWrapper and InputCore and nothing
// else, and every dependency beyond those is time added to every cycle this
// project exists to measure. What is needed here is one object of one array,
// two arrays of objects inside it and one array of strings - not a JSON
// implementation, and a partial one that admits what it is beats a general
// one nobody audited.
//
// IT IS NESTED, WHICH CrimeProbe.h's IS NOT. That scanner walks the top-level
// objects of one flat array; this file has arrays inside objects inside an
// array, so the brace and bracket counting has to nest and has to stay
// string-aware - a brace inside a rumour's summary must not close its object.
// That is the whole of the difference and it is why this is its own file.
//
// WHAT IT DOES NOT DO, said plainly rather than discovered later:
//   - SUSPICION IS NOT RESTORED. SuspicionTracker is out of scope in this
//     port (Gossip.h says so at its head and prints
//     gossipSuspicionPorted=no), so the "suspicion" key is read past and
//     dropped. The golden table does not pin it for the same reason.
//   - No escapes beyond the two CrimeProbe.h handles, and \u is passed
//     through as characters rather than decoded. Nothing this codec writes
//     produces one.
//   - Numbers are read with strtod, which is what the C++ side already does
//     everywhere else it parses one.
#pragma once

#include <clocale>
#include <cstdio>
#include <cstdlib>
#include <string>
#include <vector>

#include "Gossip.h"

namespace LedgerCore
{
namespace Save
{
	typedef std::string::size_type Pos;
	struct Span { Pos Begin; Pos End; };

	inline Pos SkipWs(const std::string& S, Pos I)
	{
		while (I < S.size() && (S[I] == ' ' || S[I] == '\t' || S[I] == '\n' || S[I] == '\r')) { ++I; }
		return I;
	}

	// EVERY ESCAPE MiniJson WRITES, UNESCAPED THE WAY MiniJson UNESCAPES IT.
	//
	// A first version of this handled \n and \t by turning them into spaces
	// and "passed everything else through" by dropping the backslash, on the
	// stated grounds that "nothing this codec writes produces one". That was
	// FALSE and an independent reviewer proved it end to end: MiniJson's
	// EscapeString emits \", \\, \/, \b, \f, \n, \r, \t and \uXXXX, and a
	// witness whose summary contained a carriage return came back through the
	// real C# byte-identical and through this reader with a stray letter `r`
	// sitting in the middle of prose a player reads. \u0041 became the four
	// characters u0041.
	//
	// THE TWO-TO-A-SPACE RULE IS GONE WITH IT. That came from CrimeProbe.h,
	// whose bank file is one line per record and cannot carry a real newline;
	// a save file can, and a summary that contained one should come back
	// containing one.
	//
	// \uXXXX IS DECODED TO UTF-8 rather than passed through, because the C#
	// hands back a real character and a comparison of two strings is the only
	// thing this port is for. A surrogate pair is joined; a lone surrogate or
	// a malformed escape answers false, which refuses the file rather than
	// inventing a character - see the whole-file check below for why refusing
	// is now safe.
	inline void AppendUtf8(std::string& Out, unsigned long Cp)
	{
		if (Cp < 0x80UL) { Out += static_cast<char>(Cp); }
		else if (Cp < 0x800UL)
		{
			Out += static_cast<char>(0xC0UL | (Cp >> 6));
			Out += static_cast<char>(0x80UL | (Cp & 0x3FUL));
		}
		else if (Cp < 0x10000UL)
		{
			Out += static_cast<char>(0xE0UL | (Cp >> 12));
			Out += static_cast<char>(0x80UL | ((Cp >> 6) & 0x3FUL));
			Out += static_cast<char>(0x80UL | (Cp & 0x3FUL));
		}
		else
		{
			Out += static_cast<char>(0xF0UL | (Cp >> 18));
			Out += static_cast<char>(0x80UL | ((Cp >> 12) & 0x3FUL));
			Out += static_cast<char>(0x80UL | ((Cp >> 6) & 0x3FUL));
			Out += static_cast<char>(0x80UL | (Cp & 0x3FUL));
		}
	}

	inline bool ReadHex4(const std::string& S, Pos I, unsigned long& Out)
	{
		if (I + 4 > S.size()) { return false; }
		Out = 0;
		for (int K = 0; K < 4; ++K)
		{
			const char C = S[I + K];
			unsigned long D;
			if (C >= '0' && C <= '9')      { D = static_cast<unsigned long>(C - '0'); }
			else if (C >= 'a' && C <= 'f') { D = static_cast<unsigned long>(C - 'a' + 10); }
			else if (C >= 'A' && C <= 'F') { D = static_cast<unsigned long>(C - 'A' + 10); }
			else { return false; }
			Out = (Out << 4) | D;
		}
		return true;
	}

	inline bool ReadString(const std::string& S, Pos& I, std::string& Out)
	{
		Out.clear();
		if (I >= S.size() || S[I] != '"') { return false; }
		++I;
		while (I < S.size())
		{
			const char C = S[I];
			if (C == '\\')
			{
				if (I + 1 >= S.size()) { return false; }
				const char E = S[I + 1];
				if      (E == 'n')  { Out += '\n'; }
				else if (E == 't')  { Out += '\t'; }
				else if (E == 'r')  { Out += '\r'; }
				else if (E == 'b')  { Out += '\b'; }
				else if (E == 'f')  { Out += '\f'; }
				else if (E == '"' || E == '\\' || E == '/') { Out += E; }
				else if (E == 'u')
				{
					unsigned long Cp;
					if (!ReadHex4(S, I + 2, Cp)) { return false; }
					I += 6;
					if (Cp >= 0xD800UL && Cp <= 0xDBFFUL)
					{
						unsigned long Low;
						if (I + 1 >= S.size() || S[I] != '\\' || S[I + 1] != 'u') { return false; }
						if (!ReadHex4(S, I + 2, Low)) { return false; }
						if (Low < 0xDC00UL || Low > 0xDFFFUL) { return false; }
						I += 6;
						Cp = 0x10000UL + ((Cp - 0xD800UL) << 10) + (Low - 0xDC00UL);
					}
					else if (Cp >= 0xDC00UL && Cp <= 0xDFFFUL) { return false; }
					AppendUtf8(Out, Cp);
					continue;
				}
				else { return false; }
				I += 2;
				continue;
			}
			if (C == '"') { ++I; return true; }
			Out += C;
			++I;
		}
		return false;
	}

	// Walks forward from Open (which must be at '{' or '[') to just past its
	// matching close, counting nesting and skipping over strings so that a
	// brace inside a summary cannot end an object early. Answers npos when
	// the container never closes.
	inline Pos MatchClose(const std::string& S, Pos Open)
	{
		if (Open >= S.size()) { return std::string::npos; }
		const char OpenCh = S[Open];
		const char CloseCh = OpenCh == '{' ? '}' : (OpenCh == '[' ? ']' : '\0');
		if (CloseCh == '\0') { return std::string::npos; }
		int Depth = 0;
		Pos I = Open;
		while (I < S.size())
		{
			const char C = S[I];
			if (C == '"')
			{
				std::string Ignored;
				if (!ReadString(S, I, Ignored)) { return std::string::npos; }
				continue;
			}
			if (C == OpenCh) { ++Depth; }
			else if (C == CloseCh)
			{
				--Depth;
				if (Depth == 0) { return I + 1; }
			}
			++I;
		}
		return std::string::npos;
	}

	// THE KEY IS FOUND AT THIS OBJECT'S OWN LEVEL, never inside a child.
	// A plain find() would have matched "id" inside a nested rumour and
	// answered a sibling's value, which is the classic way a hand-rolled
	// scanner reads a file correctly on the fixture and wrongly on the save.
	// So this steps over every nested container it meets.
	inline bool FindValue(const std::string& S, Span Obj, const std::string& Key, Span& Out)
	{
		bool Found = false;
		Pos I = SkipWs(S, Obj.Begin);
		if (I >= Obj.End || S[I] != '{') { return false; }
		++I;
		while (I < Obj.End)
		{
			I = SkipWs(S, I);
			if (I >= Obj.End || S[I] == '}') { return Found; }
			std::string Name;
			if (S[I] != '"') { return Found; }
			if (!ReadString(S, I, Name)) { return Found; }
			I = SkipWs(S, I);
			if (I >= Obj.End || S[I] != ':') { return Found; }
			I = SkipWs(S, I + 1);
			if (I >= Obj.End) { return Found; }
			const Pos ValueBegin = I;
			Pos ValueEnd;
			if (S[I] == '{' || S[I] == '[')
			{
				ValueEnd = MatchClose(S, I);
				if (ValueEnd == std::string::npos) { return Found; }
			}
			else if (S[I] == '"')
			{
				Pos J = I;
				std::string Ignored;
				if (!ReadString(S, J, Ignored)) { return Found; }
				ValueEnd = J;
			}
			else
			{
				Pos J = I;
				while (J < Obj.End && S[J] != ',' && S[J] != '}' && S[J] != ']') { ++J; }
				ValueEnd = J;
			}
			if (Name == Key)
			{
				// THE LAST ONE WINS, NOT THE FIRST. MiniJson builds a
				// dictionary with `dict[key] = value`, so a repeated key
				// overwrites; this used to return on the first match and
				// answer 0.1 where the C# answered 0.9. Duplicate keys are
				// not something the codec writes - they are something a
				// hand-edited or merged save has - and the two engines
				// disagreeing about which one counts is exactly the kind of
				// difference this port exists to make impossible.
				Out.Begin = ValueBegin;
				Out.End = ValueEnd;
				Found = true;
			}
			I = SkipWs(S, ValueEnd);
			if (I < Obj.End && S[I] == ',') { ++I; }
		}
		return Found;
	}

	// THE SCALARS ANSWER THE WAY MiniJson's HELPERS DO, WHICH IS NOT THE WAY
	// JSON DOES, and the difference is the whole of this block.
	//
	// The C# reads every one of these through three one-line helpers, and
	// each is stricter than it looks:
	//   GetString  is `v as string`  - so a value that is JSON null, a
	//              number, a bool, an object or an array answers NULL, not
	//              a rendering of itself. An EMPTY string answers "".
	//   Flag       is `v is bool b && b` - so ONLY a real JSON true. The
	//              number 1 is not true. The string "true" is not true.
	//   Num        is `v != null ? Convert.ToDouble(v) : 0` - so a missing
	//              key and a null both read 0.
	//
	// A QUOTED NUMBER IS NOT PINNED, deliberately. Convert.ToDouble on a
	// STRING uses the current culture, so `"loyalty":"0.25"` reads as 0.25
	// on a machine whose decimal separator is a point and as something else
	// on one whose separator is a comma. That is a real property of the C#
	// and worth knowing, and it is exactly what must not go in a golden
	// table: a row that depends on the machine turns the table from a
	// contract into a coincidence. Nothing this codec WRITES is a quoted
	// number, so the case is left unpinned and both engines are free.
	//
	// A first version of this file read every value as text and asked
	// whether the text was empty, which got four cases wrong in two
	// directions at once: `"subj":null` kept a rumour whose subject was the
	// word "null", `"subj":5` kept one whose subject was "5", `"subj":""`
	// DROPPED a rumour the C# keeps, and `"leashed":1` leashed an agent the
	// C# would have left alone. Every one of those is a belief that differs
	// between the two engines after reading the same file, which is the one
	// thing this port exists to make impossible.
	//
	// So presence, quotedness and emptiness are three separate answers here
	// rather than one.
	struct Raw { bool Found; bool Quoted; std::string Text; };

	inline Raw FieldRaw(const std::string& S, Span Obj, const std::string& Key)
	{
		Raw Out;
		Out.Found = false;
		Out.Quoted = false;
		Span V;
		if (!FindValue(S, Obj, Key, V)) { return Out; }
		Out.Found = true;
		Pos I = V.Begin;
		if (I < S.size() && S[I] == '"')
		{
			Out.Quoted = ReadString(S, I, Out.Text);
			if (!Out.Quoted) { Out.Found = false; }
			return Out;
		}
		Out.Text.assign(S, V.Begin, V.End - V.Begin);
		// Trailing whitespace before the comma is not part of the value.
		while (!Out.Text.empty() &&
		       (Out.Text[Out.Text.size() - 1] == ' ' || Out.Text[Out.Text.size() - 1] == '\t' ||
		        Out.Text[Out.Text.size() - 1] == '\n' || Out.Text[Out.Text.size() - 1] == '\r'))
		{
			Out.Text.erase(Out.Text.size() - 1);
		}
		return Out;
	}

	/// `v as string`: only a genuine JSON string answers. An empty one is a
	/// string and answers true with an empty Out.
	inline bool FieldString(const std::string& S, Span Obj, const std::string& Key, std::string& Out)
	{
		const Raw R = FieldRaw(S, Obj, Key);
		if (!R.Found || !R.Quoted) { Out.clear(); return false; }
		Out = R.Text;
		return true;
	}

	/// strtod IN THE C LOCALE, ALWAYS. strtod reads the decimal point of the
	/// CURRENT locale, so under a comma-decimal LC_NUMERIC "0.375" stops at
	/// the point and answers 0 - every loyalty and every confidence in the
	/// save silently truncating to an integer. MiniJson's own ParseNumber
	/// names CultureInfo.InvariantCulture for exactly this reason, and this
	/// project already defends against it in two other places (VignetteSpec.h
	/// and VignetteShot.cpp both call setlocale here). This file did not.
	inline double StrToDoubleC(const std::string& Text, bool& Ok)
	{
		const char* Was = std::setlocale(LC_NUMERIC, 0);
		const std::string Saved = Was ? std::string(Was) : std::string("C");
		std::setlocale(LC_NUMERIC, "C");
		const char* Start = Text.c_str();
		char* Stop = 0;
		const double V = std::strtod(Start, &Stop);
		Ok = Stop != Start;
		std::setlocale(LC_NUMERIC, Saved.c_str());
		return V;
	}

	/// `v != null ? Convert.ToDouble(v) : 0`. An absent key and a null both
	/// give the fallback.
	///
	/// A JSON BOOL IS A NUMBER TO Convert.ToDouble, which is the case an
	/// independent reviewer caught: `Convert.ToDouble(true)` is 1.0, so a
	/// save carrying `"conf":true` gives a rumour of confidence 1 in Unity
	/// and confidence 0 here. MinConfidenceToShare is 0.2, so the same file
	/// produced a rumour that spread in one engine and sat inert in the
	/// other. The exemption written here for "text that is not a number"
	/// covered the case where the C# THROWS; for a bool it does not throw,
	/// it answers 1.
	///
	/// A QUOTED NUMBER IS NOT PINNED, deliberately: Convert.ToDouble on a
	/// STRING uses the current CULTURE, so it is machine-dependent on the C#
	/// side and a golden row that depended on it would be a coincidence
	/// rather than a contract. Nothing this codec writes is a quoted number.
	inline double FieldNumber(const std::string& S, Span Obj, const std::string& Key, double Fallback)
	{
		const Raw R = FieldRaw(S, Obj, Key);
		if (!R.Found) { return Fallback; }
		if (!R.Quoted)
		{
			if (R.Text == "null")  { return Fallback; }
			if (R.Text == "true")  { return 1.0; }
			if (R.Text == "false") { return 0.0; }
		}
		bool Ok = false;
		const double V = StrToDoubleC(R.Text, Ok);
		return Ok ? V : Fallback;
	}

	/// `GetInt`, WHICH IS NOT `Num`. MiniJson's GetInt requires `v is double`
	/// - a QUOTED number is a string and answers 0, where Num would have
	/// parsed it - and it SATURATES rather than casting, because casting a
	/// double outside int's range is undefined in C# and on x86 yields
	/// int.MinValue. Its own comment records why: SaveChaos found twenty-four
	/// of these in one run "and every single one had flipped sign, which is
	/// the worst shape an overflow can take".
	///
	/// `hops` is read with GetInt in the C# and was being read with Num here,
	/// then handed to a static_cast - so a quoted hop count disagreed, and an
	/// enormous one reintroduced the exact sign flip the C# comment documents
	/// fixing. Both halves are here now.
	inline int FieldInt(const std::string& S, Span Obj, const std::string& Key)
	{
		const Raw R = FieldRaw(S, Obj, Key);
		if (!R.Found || R.Quoted) { return 0; }
		if (R.Text == "null" || R.Text == "true" || R.Text == "false") { return 0; }
		bool Ok = false;
		const double V = StrToDoubleC(R.Text, Ok);
		if (!Ok) { return 0; }
		if (V >= 2147483647.0)  { return 2147483647; }
		if (V <= -2147483648.0) { return -2147483647 - 1; }
		return static_cast<int>(V);
	}

	/// `v is bool b && b`. ONLY an unquoted JSON true. Not 1, not "true",
	/// not "True" - MiniJson produces lower-case literals and the C# asks
	/// whether the boxed value IS a bool before it asks what it is.
	inline bool FieldFlag(const std::string& S, Span Obj, const std::string& Key)
	{
		const Raw R = FieldRaw(S, Obj, Key);
		return R.Found && !R.Quoted && R.Text == "true";
	}

	// Every top-level element of an array, as spans. Used for the objects in
	// "agents", "rumors" and "facts"; strings come back as their own spans
	// and are read with ReadString by the caller.
	inline void ArrayElements(const std::string& S, Span Arr, std::vector<Span>& Out)
	{
		Out.clear();
		Pos I = SkipWs(S, Arr.Begin);
		if (I >= Arr.End || S[I] != '[') { return; }
		++I;
		while (I < Arr.End)
		{
			I = SkipWs(S, I);
			if (I >= Arr.End || S[I] == ']') { return; }
			Span E;
			E.Begin = I;
			if (S[I] == '{' || S[I] == '[')
			{
				const Pos Close = MatchClose(S, I);
				if (Close == std::string::npos) { return; }
				E.End = Close;
			}
			else if (S[I] == '"')
			{
				Pos J = I;
				std::string Ignored;
				if (!ReadString(S, J, Ignored)) { return; }
				E.End = J;
			}
			else
			{
				Pos J = I;
				while (J < Arr.End && S[J] != ',' && S[J] != ']') { ++J; }
				E.End = J;
			}
			Out.push_back(E);
			I = SkipWs(S, E.End);
			if (I < Arr.End && S[I] == ',') { ++I; }
		}
	}

	// A RUMOUR THAT LOST ITS SUBJECT IS NOT A RUMOUR, and this is the place
	// the decision is made, exactly as C#'s FactOrNull makes it. The C# side
	// cannot construct a Fact from a null and the codec drops the record; in
	// C++ a std::string cannot be null, so the MISSING KEY has to be caught
	// here or the refusal would vanish in translation and a rumour about
	// nobody would walk into a conversation. SaveChaos found this from the
	// other end by deleting one key from a save file.
	inline bool FactOrNull(const std::string& S, Span Obj, Fact& Out)
	{
		// AN EMPTY SUBJECT IS KEPT AND A NULL ONE IS NOT, which looks
		// inconsistent and is exactly what the C# does: `subj == null` drops
		// the record and `subj == ""` builds a Fact with an empty subject,
		// because an empty string is a string. Matching the engine matters
		// more here than tidiness - SameTopic compares subject and
		// predicate, so a gutted fact matches other gutted facts, and if the
		// two engines disagree about WHICH records are gutted they disagree
		// about what contradicts what.
		std::string Subject, Predicate, Value;
		if (!FieldString(S, Obj, "subj", Subject)) { return false; }
		if (!FieldString(S, Obj, "pred", Predicate)) { return false; }
		if (!FieldString(S, Obj, "val", Value)) { return false; }
		Out = Fact(Subject, Predicate, Value);
		return true;
	}

	/// Overlays a save's "agents" array onto an already-authored mill, the
	/// way C#'s SaveCodec.RestoreMillAgents does.
	///
	/// A RESTORE REPLACES RATHER THAN APPENDS. Rumours, suppressed topics and
	/// known facts are all CLEARED before the saved ones go in, because the
	/// front end rebuilds the world from the authoring and then lays the save
	/// over it - append would double every rumour on the second load, which
	/// is a thing a player does by reloading.
	///
	/// AN AGENT NOBODY AUTHORED IS SKIPPED WHOLE rather than created, which
	/// is also the C#'s behaviour: `mill.Get(id)` answers null and the loop
	/// continues. A save naming a character this build does not have is a
	/// save from another version, and inventing the character would be worse
	/// than losing them.
	/// MiniJson's OWN DEPTH LIMIT. Named because it is a fact about the
	/// reader this file has to agree with, not a number chosen here: a
	/// document nested deeper than this makes the C# throw, which makes
	/// RestoreMillAgents a no-op, and a port that quietly read it anyway
	/// would restore a save the game refuses.
	const int MaxDepth = 200;

	/// WELL-FORMED, ALL THE WAY THROUGH, BEFORE ANYTHING IS TOUCHED.
	///
	/// THIS IS THE ONE AN INDEPENDENT REVIEWER SAID TO FIX FIRST and it is
	/// the worst thing this file did. The C# parses the WHOLE document first:
	/// `MiniJson.Deserialize` throws on a trailing comma, a malformed number,
	/// an unterminated string or anything nested past 200, `RestoreMillAgents`
	/// catches it and returns, and the mill is left exactly as it was. He
	/// seeded a mill with a rumour and a loyalty, handed it a save with one
	/// bad byte at the end, and both were still there afterwards.
	///
	/// THIS FILE HAD NO WHOLE-FILE CHECK. It found "agents" opportunistically
	/// and then, for every record it could read, CLEARED that agent's
	/// rumours, suppressed topics and known facts before writing back
	/// whatever it managed to parse. So a truncated or hand-mangled save was
	/// a harmless no-op in Unity and silently destroyed gossip state in
	/// Unreal - the same file, the same player, two different worlds, and no
	/// error anywhere.
	///
	/// It is a VALIDATOR rather than a parser: it walks the document and
	/// answers whether MiniJson would have accepted it, and the scanning
	/// above still does the reading. That keeps one implementation of the
	/// reading and adds the one guarantee that was missing.
	inline bool WellFormed(const std::string& S, Pos& I, int Depth);

	inline bool SkipNumber(const std::string& S, Pos& I)
	{
		const Pos Start = I;
		if (I < S.size() && (S[I] == '-' || S[I] == '+')) { ++I; }
		bool AnyDigit = false;
		while (I < S.size() && S[I] >= '0' && S[I] <= '9') { ++I; AnyDigit = true; }
		if (I < S.size() && S[I] == '.')
		{
			++I;
			while (I < S.size() && S[I] >= '0' && S[I] <= '9') { ++I; AnyDigit = true; }
		}
		if (AnyDigit && I < S.size() && (S[I] == 'e' || S[I] == 'E'))
		{
			++I;
			if (I < S.size() && (S[I] == '-' || S[I] == '+')) { ++I; }
			bool ExpDigit = false;
			while (I < S.size() && S[I] >= '0' && S[I] <= '9') { ++I; ExpDigit = true; }
			if (!ExpDigit) { I = Start; return false; }
		}
		if (!AnyDigit) { I = Start; return false; }
		return true;
	}

	inline bool SkipWord(const std::string& S, Pos& I, const char* Word)
	{
		Pos J = I;
		for (const char* W = Word; *W; ++W)
		{
			if (J >= S.size() || S[J] != *W) { return false; }
			++J;
		}
		I = J;
		return true;
	}

	inline bool WellFormed(const std::string& S, Pos& I, int Depth)
	{
		if (Depth > MaxDepth) { return false; }
		I = SkipWs(S, I);
		if (I >= S.size()) { return false; }
		const char C = S[I];
		if (C == '{' || C == '[')
		{
			const char Close = C == '{' ? '}' : ']';
			++I;
			I = SkipWs(S, I);
			if (I < S.size() && S[I] == Close) { ++I; return true; }
			for (;;)
			{
				I = SkipWs(S, I);
				if (C == '{')
				{
					std::string Name;
					if (I >= S.size() || S[I] != '"') { return false; }
					if (!ReadString(S, I, Name)) { return false; }
					I = SkipWs(S, I);
					if (I >= S.size() || S[I] != ':') { return false; }
					++I;
				}
				if (!WellFormed(S, I, Depth + 1)) { return false; }
				I = SkipWs(S, I);
				if (I < S.size() && S[I] == ',') { ++I; continue; }
				if (I < S.size() && S[I] == Close) { ++I; return true; }
				return false;
			}
		}
		if (C == '"')
		{
			std::string Ignored;
			return ReadString(S, I, Ignored);
		}
		if (C == 't') { return SkipWord(S, I, "true"); }
		if (C == 'f') { return SkipWord(S, I, "false"); }
		if (C == 'n') { return SkipWord(S, I, "null"); }
		return SkipNumber(S, I);
	}

	inline bool WellFormed(const std::string& S)
	{
		Pos I = 0;
		if (!WellFormed(S, I, 1)) { return false; }
		I = SkipWs(S, I);
		return I >= S.size();
	}

	// ---- WRITING ONE -------------------------------------------------------
	//
	// WHY THE PORT NEEDS A WRITER AT ALL. Reading a save proved the port and
	// the engine agree about a file the C# wrote. It does not let the probe
	// perform a RESTART: for that the probe has to save what it has, build
	// the world again from the authoring, and lay the save back over it -
	// and the middle of those three is the only one it could already do.
	//
	// AGENTS ONLY, AND IT SAYS SO. The C#'s Capture writes the whole save -
	// version, clock, wallet, campaign, secrets, beats, debts - and the port
	// has none of those and has no business inventing them. What it writes is
	// the "agents" array inside a root that carries nothing else, which is
	// exactly the part RestoreMillAgents reads and exactly the part a rumour
	// lives in. A file this writes is NOT a save the game can load, and
	// calling it one would be the kind of half-truth this project keeps
	// finding in its own old notes.
	//
	// THE KEY ORDER AND THE NUMBER FORMAT ARE THE C#'s, not a choice. The
	// same reader has to take either file without noticing which engine
	// wrote it, and a reader is a thing that gets rewritten; a format that
	// only works because both ends happen to agree today is a format that
	// breaks the day one end is tidied.
	inline void EscapeInto(std::string& Out, const std::string& S)
	{
		for (std::string::size_type I = 0; I < S.size(); ++I)
		{
			const unsigned char C = (unsigned char)S[I];
			if      (C == '"')  { Out += "\\\""; }
			else if (C == '\\') { Out += "\\\\"; }
			else if (C == '/')  { Out += "\\/"; }
			else if (C == '\b') { Out += "\\b"; }
			else if (C == '\f') { Out += "\\f"; }
			else if (C == '\n') { Out += "\\n"; }
			else if (C == '\r') { Out += "\\r"; }
			else if (C == '\t') { Out += "\\t"; }
			else if (C < 0x20)
			{
				static const char* Hex = "0123456789abcdef";
				Out += "\\u00";
				Out += Hex[(C >> 4) & 0xF];
				Out += Hex[C & 0xF];
			}
			else { Out += (char)C; }
		}
	}

	inline void QuotedInto(std::string& Out, const std::string& S)
	{
		Out += '"';
		EscapeInto(Out, S);
		Out += '"';
	}

	/// The mill's agents as the JSON the C#'s own codec writes for them.
	inline std::string CaptureMillAgents(const GossipMill& Mill)
	{
		std::string Out = "{\"agents\":[";
		const std::vector<GossiperPtr>& Agents = Mill.Agents();
		for (std::vector<GossiperPtr>::size_type I = 0; I < Agents.size(); ++I)
		{
			const GossiperPtr& G = Agents[I];
			if (!G) { continue; }
			if (I) { Out += ','; }
			Out += "{\"id\":";
			QuotedInto(Out, G->Id);
			Out += ",\"loyalty\":" + ShortestRoundTrip(G->Loyalty);
			Out += ",\"leashed\":";
			Out += G->Leashed ? "true" : "false";
			// SUSPICION IS WRITTEN AS ZERO AND THAT IS NOT A MEASUREMENT.
			// SuspicionTracker is out of scope in this port, so there is no
			// value here to write; the key is present because the C#'s
			// reader expects the shape, and zero is what an unported field
			// honestly holds. A save this writes must never be mistaken for
			// one that carries a suspicion this build never tracked.
			Out += ",\"suspicion\":0";
			Out += ",\"suppressed\":[";
			for (std::vector<std::string>::size_type T = 0; T < G->Suppressed.size(); ++T)
			{
				if (T) { Out += ','; }
				QuotedInto(Out, G->Suppressed[T]);
			}
			Out += "],\"rumors\":[";
			for (std::vector<RumorPtr>::size_type Rn = 0; Rn < G->Rumors.size(); ++Rn)
			{
				const RumorPtr& Rm = G->Rumors[Rn];
				if (!Rm) { continue; }
				if (Rn) { Out += ','; }
				Out += "{\"subj\":";
				QuotedInto(Out, Rm->Content.Subject);
				Out += ",\"pred\":";
				QuotedInto(Out, Rm->Content.Predicate);
				Out += ",\"val\":";
				QuotedInto(Out, Rm->Content.Value);
				Out += ",\"origin\":";
				QuotedInto(Out, Rm->OriginId);
				Out += ",\"summary\":";
				QuotedInto(Out, Rm->Summary);
				Out += ",\"conf\":" + ShortestRoundTrip(Rm->Confidence);
				Out += ",\"hops\":";
				{
					char Buf[32];
					std::sprintf(Buf, "%d", Rm->Hops);
					Out += Buf;
				}
				Out += ",\"sensitive\":";
				Out += Rm->Sensitive ? "true" : "false";
				Out += ",\"indelible\":";
				Out += Rm->Indelible ? "true" : "false";
				Out += '}';
			}
			Out += "],\"facts\":[";
			if (G->Knowledge)
			{
				for (std::vector<Fact>::size_type F = 0; F < G->Knowledge->Facts.size(); ++F)
				{
					if (F) { Out += ','; }
					Out += "{\"subj\":";
					QuotedInto(Out, G->Knowledge->Facts[F].Subject);
					Out += ",\"pred\":";
					QuotedInto(Out, G->Knowledge->Facts[F].Predicate);
					Out += ",\"val\":";
					QuotedInto(Out, G->Knowledge->Facts[F].Value);
					Out += '}';
				}
			}
			Out += "]}";
		}
		Out += "]}";
		return Out;
	}

	inline void RestoreMillAgents(const std::string& Json, GossipMill& Mill)
	{
		// NOTHING IS TOUCHED UNTIL THE WHOLE FILE READS. See WellFormed: the
		// C# parses first and throws, so a bad save changes nothing at all;
		// this used to clear an agent's rumours and then discover it could
		// not read their replacements.
		if (!WellFormed(Json)) { return; }
		Span Root;
		Root.Begin = 0;
		Root.End = Json.size();
		Span Agents;
		if (!FindValue(Json, Root, "agents", Agents)) { return; }
		std::vector<Span> Records;
		ArrayElements(Json, Agents, Records);
		for (std::vector<Span>::size_type I = 0; I < Records.size(); ++I)
		{
			std::string Id;
			if (!FieldString(Json, Records[I], "id", Id)) { continue; }
			GossiperPtr G = Mill.Get(Id);
			if (!G) { continue; }

			G->Loyalty = FieldNumber(Json, Records[I], "loyalty", 0.0);
			G->Leashed = FieldFlag(Json, Records[I], "leashed");

			G->Suppressed.clear();
			Span Suppressed;
			if (FindValue(Json, Records[I], "suppressed", Suppressed))
			{
				std::vector<Span> Topics;
				ArrayElements(Json, Suppressed, Topics);
				for (std::vector<Span>::size_type T = 0; T < Topics.size(); ++T)
				{
					Pos At = Topics[T].Begin;
					std::string Topic;
					if (!ReadString(Json, At, Topic)) { continue; }
					// IT IS A HashSet IN THE C# AND A vector HERE, so a save
					// listing the same topic twice suppressed one topic there
					// and counted two here. The container cannot change - the
					// rest of Gossip.h is written against the vector - so the
					// SET BEHAVIOUR is done at the door, which is the only
					// place the difference can arise.
					bool Already = false;
					for (std::vector<std::string>::size_type K = 0;
					     K < G->Suppressed.size(); ++K)
					{
						if (G->Suppressed[K] == Topic) { Already = true; break; }
					}
					if (!Already) { G->Suppressed.push_back(Topic); }
				}
			}

			G->Rumors.clear();
			Span Rumors;
			if (FindValue(Json, Records[I], "rumors", Rumors))
			{
				std::vector<Span> Each;
				ArrayElements(Json, Rumors, Each);
				for (std::vector<Span>::size_type R = 0; R < Each.size(); ++R)
				{
					Fact Content("", "", "");
					if (!FactOrNull(Json, Each[R], Content)) { continue; }
					RumorPtr Made(new Rumor(Content));
					FieldString(Json, Each[R], "origin", Made->OriginId);
					FieldString(Json, Each[R], "summary", Made->Summary);
					Made->Confidence = FieldNumber(Json, Each[R], "conf", 0.0);
					Made->Hops = FieldInt(Json, Each[R], "hops");
					Made->Sensitive = FieldFlag(Json, Each[R], "sensitive");
					Made->Indelible = FieldFlag(Json, Each[R], "indelible");
					G->Rumors.push_back(Made);
				}
			}

			if (G->Knowledge)
			{
				G->Knowledge->Facts.clear();
				Span Facts;
				if (FindValue(Json, Records[I], "facts", Facts))
				{
					std::vector<Span> Each;
					ArrayElements(Json, Facts, Each);
					for (std::vector<Span>::size_type F = 0; F < Each.size(); ++F)
					{
						Fact Known("", "", "");
						if (FactOrNull(Json, Each[F], Known)) { G->Knowledge->Learn(Known); }
					}
				}
			}
		}
	}
}
}
