// TRANSLITERATION of ledger/Assets/Scripts/Core/CastDay.cs, 29 September (the
// town list's handover 2, "friends who meet").
//
// WHERE THE TOWN'S NAMED PEOPLE ARE, HOUR BY HOUR, AND WHO IS WITH WHOM. Two
// friends pass a story on only while they stand within talking range of each
// other, so the routines decide who can ever hear what; the town session
// keeps them as data (production/specs/hook-cast.json, the forty named
// people and their eighty friendships; production/specs/quay-cast.json, the
// ten on the built street) and asserts every friendship meets. This is the
// same reader for the game, beside Schedule.h, so the street's walkers and
// the port's gossip graph read the same file the Core's tests do.
//
// TRANSLITERATION, NOT REWRITE, as Gossip.h states the method. Every refusal
// the C# throws is a refusal here (a false and the C#'s own words in Err),
// in the same order, so a file one engine refuses the other refuses too.
// Checked against PerceptionGolden EmitCastDay: every person's place at every
// hour of every weekday and every friendship's hours together over both
// committed files, small files for the wrap round midnight, an unsorted
// routine, a weekday's own routine and the six-metre edge, and thirteen files
// it must refuse.
//
// READ THE C#'S WAY (MiniJson.h), since the independent check found the
// street's own JSON reader parts from the C#'s on escapes, numbers, repeated
// keys and whitespace (an accented name would have come out with a '?').
//
// SCOPE: Parse (with its areas, "said", names, roles, "called", "keepsQuiet",
// circles and "namesHim", read as the C# reads them), PlaceOf, Where, Together,
// HoursTogetherPerWeek, DaysTogetherPerWeek, FriendsMeetDays, and the few
// lookups the game reads (NameOf, SaidOf, AreaOf, CircleOf, NeverToPolice,
// MickeysOwn); and since 28 October 2026 (the 5 October sweep's U2) the
// shops' hours: "hours", "hours_note" and "hours_breaks", refused as the C#
// refuses them, with AreaFor, OpenAt, HoursWords and HoursFor. NOT HERE: the
// talk program's own reads (SpokenAreas, Fits, WhoNamed,
// UsualWords, PeopleFor, QuietStance), which run in the C# beside the game.
//
// NO UNREAL TYPE IS IN THIS FILE, as every file of the port.
#pragma once

#include "MiniJson.h"       // the C#'s own reader, transliterated; LedgerVignette::Value

#include <algorithm>
#include <cmath>
#include <cstdio>
#include <map>
#include <set>
#include <string>
#include <utility>
#include <vector>

namespace LedgerCore
{
	class CastDay
	{
	public:
		typedef std::vector<std::pair<int, std::string> > Routine;
		struct Tie { std::string A, B; double W; };
		// An area's hours on one weekday (the C#'s (open, close)?): bOpen false where
		// the file leaves the weekday out and it is shut. Open and Close are hours
		// from that day's midnight, a close past 24 into the next morning.
		struct DayHours { bool bOpen; double Open, Close; DayHours() : bOpen(false), Open(0.0), Close(0.0) {} };
		typedef std::vector<DayHours> WeekHours;   // seven, Monday first
		// An area's breaks on each weekday, [from, to], sorted; empty for none.
		typedef std::vector<std::vector<std::pair<double, double> > > WeekBreaks;

		double TalkRangeM;

		CastDay() : TalkRangeM(0.0) {}

		static const char* Off() { return "off"; }
		static const char* const* WeekdayKeys()
		{
			static const char* const Keys[7] = { "mon", "tue", "wed", "thu", "fri", "sat", "sun" };
			return Keys;
		}

		const std::vector<std::string>& People() const { return PeopleList; }
		const std::vector<Tie>& Ties() const { return TieList; }

		static int Weekday(int Day) { return ((Day % 7) + 7) % 7; }

		// MiniJson's dictionary keeps a repeated key's LAST value.
		static const LedgerVignette::Value* Get(const LedgerVignette::Value* Obj, const char* Key)
		{
			if (Obj == 0 || Obj->Type != LedgerVignette::T_OBJ) return 0;
			const LedgerVignette::Value* Found = 0;
			for (size_t I = 0; I < Obj->Obj.size(); ++I)
				if (Obj->Obj[I].first == Key) Found = &Obj->Obj[I].second;
			return Found;
		}
		static const LedgerVignette::Value* GetObject(const LedgerVignette::Value* Obj, const char* Key)
		{
			const LedgerVignette::Value* V = Get(Obj, Key);
			return V != 0 && V->Type == LedgerVignette::T_OBJ ? V : 0;
		}
		static const LedgerVignette::Value* GetList(const LedgerVignette::Value* Obj, const char* Key)
		{
			const LedgerVignette::Value* V = Get(Obj, Key);
			return V != 0 && V->Type == LedgerVignette::T_ARR ? V : 0;
		}
		// A string value, or false (the C#'s null).
		static bool GetString(const LedgerVignette::Value* Obj, const char* Key, std::string& Out)
		{
			const LedgerVignette::Value* V = Get(Obj, Key);
			if (V == 0 || V->Type != LedgerVignette::T_STR) return false;
			Out = V->Str;
			return true;
		}
		// string.Trim(), over UTF-8 (MiniJson.h).
		static std::string Trim(const std::string& S) { return MiniJson::Trim(S); }
		static std::string Num(double V)
		{
			char Buf[64];
			std::snprintf(Buf, sizeof(Buf), "%.17g", V);
			return Buf;
		}

		/// Reads a cast file. False, with what is wrong in Err, where the C#
		/// throws a FormatException.
		static bool Parse(const std::string& Json, CastDay& C, std::string& Err)
		{
			using namespace LedgerVignette;
			C = CastDay();
			Err.clear();
			// READ AS THE C# READS IT (MiniJson.h): escapes, numbers, a key
			// written twice and whitespace mean the same in both engines.
			Value Root;
			std::string JsonErr;
			if (!MiniJson::Deserialize(Json, Root, JsonErr)) { Err = "cast file: " + JsonErr; return false; }
			if (Root.Type != T_OBJ) { Err = "cast file: not an object"; return false; }
			const Value* Tr = Get(&Root, "talk_range_m");
			if (Tr == 0 || Tr->Type != T_NUM || !(Tr->Num > 0)) { Err = "cast file: talk_range_m missing or not a positive number"; return false; }
			C.TalkRangeM = Tr->Num;
			const Value* Places = GetObject(&Root, "places");
			if (Places == 0) { Err = "cast file: no places"; return false; }
			for (size_t I = 0; I < Places->Obj.size(); ++I)
			{
				const std::string& Key = Places->Obj[I].first;
				const Value* P = &Places->Obj[I].second;
				const Value* X = Get(P, "x_m");
				const Value* Z = Get(P, "z_m");
				if (P->Type != T_OBJ || X == 0 || X->Type != T_NUM || Z == 0 || Z->Type != T_NUM)
				{
					Err = "cast file: place " + Key + " needs x_m and z_m"; return false;
				}
				if (Key == Off()) { Err = "cast file: 'off' is not a place"; return false; }
				C.PlaceAt[Key] = std::make_pair(X->Num, Z->Num);
				// INSIDE A BUILDING (CastDay.cs, the review's D): no talk through its walls.
				if (const Value* In = Get(P, "inside"))
				{
					if (In->Type != T_BOOL) { Err = "cast file: place " + Key + "'s inside must be true or false"; return false; }
					if (In->Bool) C.InsidePlaces.insert(Key);
				}
				std::string Said;
				if (GetString(P, "said", Said) && Trim(Said).size() > 0) C.Said[Key] = Trim(Said);
				// WHERE A BODY WAITS FOR THIS PLACE ON ITS PAVEMENT, optional (7 October): an inside
				// place's person stands on their own pavement until the room is built or unlocked
				// (CrimeProbe.h BodySpotFor), by default straight out from the place; "body_x_m"
				// moves them along it, to the shop's door. Only the game reads it.
				if (const Value* BX = Get(P, "body_x_m"))
				{
					if (BX->Type != T_NUM) { Err = "cast file: place " + Key + "'s body_x_m must be a number"; return false; }
					C.BodyXAt[Key] = BX->Num;
				}
			}
			// The areas, optional: each a list of its places and the names people use.
			if (const Value* Areas = GetObject(&Root, "areas"))
			{
				for (size_t I = 0; I < Areas->Obj.size(); ++I)
				{
					const std::string& Key = Areas->Obj[I].first;
					const Value* A = &Areas->Obj[I].second;
					std::string Within;
					if (GetString(A, "within", Within) && Within.size() > 0) C.WithinOf[Key] = Within;
					// WHO KEEPS IT and WHETHER IT IS QUAY STREET'S OWN (CastDay.cs, the
					// review's A9 and A11); refused as the C# refuses a bad value.
					if (const Value* Kp = Get(A, "keeper"))
					{
						if (Kp->Type != T_STR || Trim(Kp->Str).empty()) { Err = "cast file: area " + Key + "'s keeper must be a person's id"; return false; }
						C.KeeperOfArea[Key] = Trim(Kp->Str);
					}
					if (const Value* St = Get(A, "street"))
					{
						if (St->Type != T_BOOL) { Err = "cast file: area " + Key + "'s street must be true or false"; return false; }
						if (St->Bool) C.StreetAreas.insert(Key);
					}
					std::vector<std::string> Names;
					if (const Value* NL = GetList(A, "names"))
						for (size_t J = 0; J < NL->Arr.size(); ++J)
							if (NL->Arr[J].Type == T_STR && Trim(NL->Arr[J].Str).size() > 0) Names.push_back(Trim(NL->Arr[J].Str));
					C.AreaNames[Key] = Names;
					C.AreaOrder.push_back(Key);   // the file's order, which HoursFor says them in (the C#'s dictionary)
					// THE SHOP'S HOURS AND ITS BREAKS (28 October 2026, the 5 October sweep's U2: this
					// file read no "hours" at all, so thirteen bad files the C# refuses were taken here),
					// read and refused as CastDay.cs ReadHours and ReadBreaks do, in its order: the hours,
					// the note, then the breaks, which need the hours whatever order the file gives them.
					if (const Value* Hv = Get(A, "hours"))
					{
						WeekHours W;
						if (!ReadHours(Key, *Hv, W, Err)) return false;
						C.HoursOf[Key] = W;
					}
					std::string Note;
					if (GetString(A, "hours_note", Note) && Trim(Note).size() > 0) C.HoursNoteOf[Key] = Trim(Note);
					if (const Value* Bv = Get(A, "hours_breaks"))
					{
						std::map<std::string, WeekHours>::const_iterator Wk = C.HoursOf.find(Key);
						if (Wk == C.HoursOf.end()) { Err = "cast file: area " + Key + " has breaks but no hours"; return false; }
						WeekBreaks B;
						if (!ReadBreaks(Key, *Bv, Wk->second, B, Err)) return false;
						C.BreaksOf[Key] = B;
					}
					if (const Value* PL = GetList(A, "places"))
						for (size_t J = 0; J < PL->Arr.size(); ++J)
						{
							if (PL->Arr[J].Type != T_STR) continue;
							const std::string& Pls = PL->Arr[J].Str;
							if (!C.PlaceAt.count(Pls)) { Err = "cast file: area " + Key + " names a place " + Pls + " that \"places\" does not define"; return false; }
							C.AreaOfPlace[Pls] = Key;
						}
				}
			}
			const Value* People = GetList(&Root, "people");
			if (People == 0) { Err = "cast file: no people"; return false; }
			for (size_t I = 0; I < People->Arr.size(); ++I)
			{
				const Value* P = &People->Arr[I];
				std::string Id;
				if (!GetString(P, "id", Id) || Id.empty()) { Err = "cast file: a person with no id"; return false; }
				if (C.Daily.count(Id)) { Err = "cast file: " + Id + " twice"; return false; }
				C.PeopleList.push_back(Id);
				std::string S;
				if (GetString(P, "name", S) && Trim(S).size() > 0) C.Name[Id] = Trim(S);
				if (GetString(P, "role", S) && Trim(S).size() > 0) C.Role[Id] = Trim(S);
				if (GetString(P, "called", S) && Trim(S).size() > 0) C.Called[Id] = Trim(S);
				// WHOM THEY KEEP QUIET FOR (CastDay.cs, the file's "keepsQuiet"): only the
				// words it knows: a typo was read as a friend's silence, so Mickey's own
				// reported again (the independent check of 1 October).
				if (const Value* Kq = Get(P, "keepsQuiet"))
				{
					const std::string W = Kq->Type == T_STR ? Trim(Kq->Str) : std::string();
					if (Kq->Type != T_STR || !(W == "owner" || W == "anyone" || W == "nobody" || W == "friend"))
					{
						Err = "person " + Id + ": keepsQuiet must be \"owner\", \"anyone\", \"nobody\" or \"friend\""; return false;
					}
					C.KeepsQuiet[Id] = W;
				}
				// NEVER TO THE POLICE (CastDay.cs 126 to 131; the town's handover 6ar):
				// "police" is "never" or absent; the police file never takes a report
				// from them (PoliceFile::WouldReport's bNeverToPolice).
				if (const Value* Pol = Get(P, "police"))
				{
					if (Pol->Type != T_STR || Pol->Str != "never")
					{
						Err = "cast file: " + Id + "'s police must be \"never\" or absent"; return false;
					}
					C.NeverPolice.insert(Id);
				}
				if (const Value* Cr = Get(P, "circle"))
				{
					if (Cr->Type != T_STR || (Cr->Str != "day" && Cr->Str != "night" && Cr->Str != "both"))
					{
						Err = "cast file: " + Id + "'s circle must be \"day\", \"night\" or \"both\""; return false;
					}
					C.Circle[Id] = Cr->Str;
				}
				if (const Value* Nh = Get(P, "namesHim"))
				{
					if (Nh->Type != T_STR || Trim(Nh->Str) != "on-trust")
					{
						Err = "cast file: " + Id + "'s namesHim must be \"on-trust\" or absent"; return false;
					}
					C.NameOnTrust.insert(Id);
				}
				Routine Daily;
				if (!C.ReadRoutine(Id, GetList(P, "routine"), Daily, Err)) return false;
				C.Daily[Id] = Daily;
				const Value* Days = Get(P, "days");
				if (Days != 0 && Days->Type != T_OBJ) { Err = "cast file: " + Id + "'s days must be an object keyed mon to sun"; return false; }
				if (Days != 0)
				{
					std::vector<Routine> Week(7);
					std::vector<bool> Has(7, false);
					for (size_t J = 0; J < Days->Obj.size(); ++J)
					{
						int Wd = -1;
						for (int K = 0; K < 7; ++K) if (Days->Obj[J].first == WeekdayKeys()[K]) Wd = K;
						if (Wd < 0) { Err = "cast file: " + Id + " has a day '" + Days->Obj[J].first + "' (mon to sun)"; return false; }
						const Value* L = Days->Obj[J].second.Type == T_ARR ? &Days->Obj[J].second : 0;
						if (!C.ReadRoutine(Id + "." + Days->Obj[J].first, L, Week[Wd], Err)) return false;
						Has[Wd] = true;
					}
					C.ByWeekday[Id] = std::make_pair(Week, Has);
				}
			}
			const Value* TiesV = Get(&Root, "ties");
			if (TiesV != 0 && TiesV->Type != T_ARR) { Err = "cast file: ties must be a list"; return false; }
			std::set<std::string> Seen;
			for (size_t I = 0; TiesV != 0 && I < TiesV->Arr.size(); ++I)
			{
				const Value& T = TiesV->Arr[I];
				if (T.Type != T_ARR || T.Arr.size() < 3 || T.Arr[0].Type != T_STR || T.Arr[1].Type != T_STR || T.Arr[2].Type != T_NUM)
				{
					Err = "cast file: a tie that is not [a, b, strength]"; return false;
				}
				const std::string& A = T.Arr[0].Str;
				const std::string& B = T.Arr[1].Str;
				const double W = T.Arr[2].Num;
				if (!C.Daily.count(A) || !C.Daily.count(B)) { Err = "cast file: tie " + A + "-" + B + " names somebody who is not in the cast"; return false; }
				if (A == B) { Err = "cast file: " + A + " is tied to themselves"; return false; }
				if (!(W > 0.0 && W <= 1.0)) { Err = "cast file: tie " + A + "-" + B + " has strength " + Num(W) + ", not in (0, 1]"; return false; }
				const std::string Key = A.compare(B) < 0 ? A + "|" + B : B + "|" + A;
				if (!Seen.insert(Key).second) { Err = "cast file: tie " + A + "-" + B + " twice"; return false; }
				Tie Tt; Tt.A = A; Tt.B = B; Tt.W = W;
				C.TieList.push_back(Tt);
			}
			for (std::map<std::string, std::string>::const_iterator K = C.KeeperOfArea.begin(); K != C.KeeperOfArea.end(); ++K)
				if (!C.Daily.count(K->second)) { Err = "cast file: area " + K->first + "'s keeper " + K->second + " is not in the cast"; return false; }
			return true;
		}

		/// A SMALL TOWN'S RULE for how often friends meet: five days a week
		/// at 0.6 and above, three from 0.45, else one.
		static int FriendsMeetDays(double Tie) { return Tie >= 0.6 ? 5 : Tie >= 0.45 ? 3 : 1; }

		/// The place somebody is at on this game day and hour, "off" when off
		/// the street, or empty (the C#'s null) for somebody not in the cast.
		std::string PlaceOf(const std::string& Id, int Day, int Hour) const
		{
			std::string Place;
			return PlaceOf(Id, Day, Hour, Place) ? Place : std::string();
		}

		/// The same, false for somebody not in the cast: a place may be
		/// named "" and is then a place like any other (the independent check).
		bool PlaceOf(const std::string& Id, int Day, int Hour, std::string& Place) const
		{
			std::map<std::string, Routine>::const_iterator D = Daily.find(Id);
			if (D == Daily.end()) return false;
			const Routine* R = &D->second;
			std::map<std::string, std::pair<std::vector<Routine>, std::vector<bool> > >::const_iterator W = ByWeekday.find(Id);
			if (W != ByWeekday.end() && W->second.second[Weekday(Day)]) R = &W->second.first[Weekday(Day)];
			const int H = ((Hour % 24) + 24) % 24;
			Place = (*R)[R->size() - 1].second;
			for (size_t I = 0; I < R->size(); ++I) if ((*R)[I].first <= H) Place = (*R)[I].second;
			return true;
		}

		/// Where they stand; false when off the street or unknown.
		bool Where(const std::string& Id, int Day, int Hour, double& X, double& Z) const
		{
			std::string Place;
			if (!PlaceOf(Id, Day, Hour, Place) || Place == Off()) return false;
			std::map<std::string, std::pair<double, double> >::const_iterator P = PlaceAt.find(Place);
			if (P == PlaceAt.end()) return false;
			X = P->second.first;
			Z = P->second.second;
			return true;
		}

		/// Both on the street and within talking range: the game's own rule.
		bool Together(const std::string& A, const std::string& B, int Day, int Hour) const
		{
			double Ax = 0, Az = 0, Bx = 0, Bz = 0;
			if (!Where(A, Day, Hour, Ax, Az) || !Where(B, Day, Hour, Bx, Bz)) return false;
			const double Dx = Ax - Bx, Dz = Az - Bz;
			if (std::sqrt(Dx * Dx + Dz * Dz) > TalkRangeM) return false;
			// NO TALK THROUGH A WALL (CastDay.cs, the review's D): in the same area,
			// or both out on the pavement.
			std::string Pa, Pb, Aa, Ab;
			PlaceOf(A, Day, Hour, Pa);
			PlaceOf(B, Day, Hour, Pb);
			const bool bSameArea = AreaOf(Pa, Aa) && AreaOf(Pb, Ab) && Aa == Ab;
			return bSameArea || (!IsInside(Pa) && !IsInside(Pb));
		}

		/// A place inside a building (CastDay.cs IsInside).
		bool IsInside(const std::string& Place) const { return InsidePlaces.count(Place) > 0; }

		int HoursTogetherPerWeek(const std::string& A, const std::string& B) const
		{
			int N = 0;
			for (int D = 0; D < 7; ++D)
				for (int H = 0; H < 24; ++H)
					if (Together(A, B, D, H)) ++N;
			return N;
		}

		int DaysTogetherPerWeek(const std::string& A, const std::string& B) const
		{
			int N = 0;
			for (int D = 0; D < 7; ++D)
				for (int H = 0; H < 24; ++H)
					if (Together(A, B, D, H)) { ++N; break; }
			return N;
		}

		// What the street calls somebody, the place in plain words, a place's
		// area and a person's circle; empty where the C# gives null ("day"
		// for the circle, as the C#).
		std::string NameOf(const std::string& Id) const { return Lookup(Name, Id); }
		/// CastDay.cs RoleOf: the file's role without the name before its colon or its
		/// "(canon)" mark, spaces run together, trimmed of spaces, commas and semicolons.
		std::string RoleOf(const std::string& Id) const
		{
			std::map<std::string, std::string>::const_iterator I = Role.find(Id);
			if (I == Role.end()) return std::string();
			std::string R = I->second;
			for (size_t At = R.find("(canon)"); At != std::string::npos; At = R.find("(canon)")) R.replace(At, 7, " ");
			const size_t Colon = R.find(':');
			if (Colon != std::string::npos && !NameOf(Id).empty()) R = R.substr(Colon + 1);
			std::string Out;
			for (const char Ch : R)
			{
				const bool bSpace = Ch == ' ' || Ch == '\t' || Ch == '\n' || Ch == '\r';
				if (!bSpace) { Out += Ch; }
				else if (Out.empty() || Out.back() != ' ') { Out += ' '; }
			}
			const size_t First = Out.find_first_not_of(" ,;");
			if (First == std::string::npos) return std::string();
			return Out.substr(First, Out.find_last_not_of(" ,;") - First + 1);
		}
		/// CastDay.cs Described: somebody as another local would describe them, the
		/// file's "called", else their name and role, else the role, else the id.
		std::string Described(const std::string& Id) const
		{
			const std::string C = Lookup(Called, Id);
			if (!C.empty()) return C;
			const std::string N = NameOf(Id), R = RoleOf(Id);
			return !N.empty() ? (!R.empty() ? N + ", " + R : N) : (!R.empty() ? R : Id);
		}
		/// CastDay.cs Called: somebody as another person speaks of them in passing, by
		/// name or as the street describes them. 27 October: the town's mill took the id
		/// for anyone with no name, and the AI tester's walk heard Darren say "I heard
		/// from outfit_man that ..."; 32 of the cast have no name.
		std::string CalledOf(const std::string& Id) const { const std::string N = NameOf(Id); return !N.empty() ? N : Described(Id); }
		std::string SaidOf(const std::string& Place) const { return Lookup(Said, Place); }
		std::string AreaOf(const std::string& Place) const { return Lookup(AreaOfPlace, Place); }
		/// The C#'s AreaOf with its null kept apart from an area named "":
		/// false for a place in no area (day one's independent check, 30 September).
		bool AreaOf(const std::string& Place, std::string& Out) const
		{
			std::map<std::string, std::string>::const_iterator I = AreaOfPlace.find(Place);
			if (I == AreaOfPlace.end()) return false;
			Out = I->second;
			return true;
		}
		std::string CircleOf(const std::string& Id) const { const std::string C = Lookup(Circle, Id); return C.empty() ? "day" : C; }
		bool NamesHimOnlyOnTrust(const std::string& Id) const { return NameOnTrust.count(Id) > 0; }
		/// CastDay.cs NeverToPolice: whoever the cast file marks "police": "never",
		/// or Mickey's own people (the file's keepsQuiet "owner": Ron and Sheila),
		/// who never go to the police about one of their own, ever, and handle
		/// what they saw privately (Jafar's ruling of 1 October, on the
		/// independent review's N4). Read by PoliceFile::WouldReport and
		/// HearTheStreet.
		bool NeverToPolice(const std::string& Id) const { return NeverPolice.count(Id) > 0 || MickeysOwn(Id); }

		/// MICKEY'S OWN PEOPLE (the file's keepsQuiet "owner": Ron and Sheila), his
		/// inherited loyalists: they never go to the police about him and handle
		/// what they saw privately (Jafar's ruling of 1 October; GossipMill::
		/// KeepsHisDeedsFor).
		bool MickeysOwn(const std::string& Id) const
		{
			const std::map<std::string, std::string>::const_iterator I = KeepsQuiet.find(Id);
			return I != KeepsQuiet.end() && I->second == "owner";
		}

		/// Who keeps an area (CastDay.cs KeeperOf); empty for nobody.
		std::string KeeperOf(const std::string& Area) const { return Lookup(KeeperOfArea, Area); }

		/// ON QUAY STREET AT THAT HOUR (CastDay.cs OnQuayStreet, the review's
		/// A11): somewhere, not off, and in one of the street's own areas; a
		/// file that marks none counts anybody not off.
		bool OnQuayStreet(const std::string& Id, int Day, int Hour) const
		{
			std::string Place;
			if (!PlaceOf(Id, Day, Hour, Place) || Place == Off()) return false;
			if (StreetAreas.empty()) return true;
			std::string Area;
			return AreaOf(Place, Area) && StreetAreas.count(Area) > 0;
		}

		// THE PLACES AND WHAT PEOPLE CALL AN AREA (the C#'s Places and
		// AreaNames), for the game's own reads: where he was seen near a deed.
		std::vector<std::string> Places() const
		{
			std::vector<std::string> Out;
			for (std::map<std::string, std::pair<double, double> >::const_iterator I = PlaceAt.begin(); I != PlaceAt.end(); ++I) Out.push_back(I->first);
			return Out;
		}
		bool PlacePosition(const std::string& Place, double& X, double& Z) const
		{
			std::map<std::string, std::pair<double, double> >::const_iterator I = PlaceAt.find(Place);
			if (I == PlaceAt.end()) return false;
			X = I->second.first; Z = I->second.second;
			return true;
		}
		std::vector<std::string> AreaNamesOf(const std::string& Area) const
		{
			std::map<std::string, std::vector<std::string> >::const_iterator I = AreaNames.find(Area);
			return I == AreaNames.end() ? std::vector<std::string>() : I->second;
		}
		/// The place nearest a point within MaxM metres, or empty.
		/// Where a place stands in the street's metres (x along, z across); false
		/// for a place the file gives no position.
		bool PlaceXZ(const std::string& Place, double& OutX, double& OutZ) const
		{
			const auto It = PlaceAt.find(Place);
			if (It == PlaceAt.end()) return false;
			OutX = It->second.first;
			OutZ = It->second.second;
			return true;
		}

		/// Where along the street a body waits for this place on its pavement (the file's
		/// "body_x_m"); false where the file gives none, and the place's own x serves.
		bool BodyXOf(const std::string& Place, double& OutX) const
		{
			const auto It = BodyXAt.find(Place);
			if (It == BodyXAt.end()) return false;
			OutX = It->second;
			return true;
		}

		std::string NearestPlace(double X, double Z, double MaxM) const
		{
			std::string Best;
			double BestM = MaxM;
			for (std::map<std::string, std::pair<double, double> >::const_iterator I = PlaceAt.begin(); I != PlaceAt.end(); ++I)
			{
				const double Dx = I->second.first - X, Dz = I->second.second - Z;
				const double M = std::sqrt(Dx * Dx + Dz * Dz);
				if (M <= BestM) { BestM = M; Best = I->first; }
			}
			return Best;
		}

		// ---- OPEN AND SHUT (28 October 2026, the 5 October sweep's U2) ----------
		//
		// CastDay.cs AreaFor, OpenAt, HoursWords and HoursFor, transliterated: the
		// game reads the shops' hours from the same cast file as the talk program
		// (which runs the C# itself and tells the talk the street's hours), so a
		// shop the game shows open is one the talk says is open. Pinned by the
		// golden table's CastOpenAt, CastHoursWords and CastHoursFor rows.

		/// CastDay.cs AreaFor: a known place as the area it is in, else a known
		/// area as itself; false (the C#'s null) for anything else. A place's area
		/// comes first, so an area named as another area's place reads as that one.
		bool AreaFor(const std::string& PlaceOrArea, std::string& Out) const
		{
			if (AreaOf(PlaceOrArea, Out)) return true;
			if (AreaNames.count(PlaceOrArea) == 0) return false;
			Out = PlaceOrArea;
			return true;
		}

		/// CastDay.cs OpenAt: whether a place or area is open at this hour and
		/// minute of this day (a close past midnight counts on the next morning,
		/// a break shuts it), in bOpen; false (the C#'s null) when it has no
		/// hours, being no shop. The hour and minute wrap into the day as PlaceOf
		/// wraps them.
		bool OpenAt(const std::string& PlaceOrArea, int Day, int Hour, int Minute, bool& bOpen) const
		{
			bOpen = false;
			std::string Area;
			if (!AreaFor(PlaceOrArea, Area)) return false;
			const std::map<std::string, WeekHours>::const_iterator Wk = HoursOf.find(Area);
			if (Wk == HoursOf.end()) return false;
			const long long All = ((long long)Day * 24 + Hour) * 60 + Minute;
			const long long D0 = All >= 0 ? All / 1440 : -((-All + 1439) / 1440);
			const int D = (int)D0;
			const double T = (double)(All - D0 * 1440) / 60.0;
			const std::map<std::string, WeekBreaks>::const_iterator Br = BreaksOf.find(Area);
			const auto InBreak = [&Br, this](int Wd, double At) {
				if (Br == BreaksOf.end()) return false;
				for (const std::pair<double, double>& B : Br->second[Wd]) { if (B.first <= At && At < B.second) return true; }
				return false;
			};
			const DayHours& Today = Wk->second[Weekday(D)];
			if (Today.bOpen && Today.Open <= T && T < Today.Close) { bOpen = !InBreak(Weekday(D), T); return true; }
			const DayHours& Before = Wk->second[Weekday(D - 1)];
			if (Before.bOpen && T + 24 < Before.Close) { bOpen = !InBreak(Weekday(D - 1), T + 24); return true; }
			return true;
		}

		/// CastDay.cs HoursWords: an area's hours as people say them, its usual
		/// hours, the days that differ, its breaks and the days it is shut ("nine
		/// till half five, on Wednesdays it shuts at one, shut on Sundays"), or by
		/// its days when it opens three or fewer ("Tuesdays, Fridays and
		/// Saturdays, eight till four"), then the file's note. False (the C#'s
		/// null) when it has no hours. Takes the area's own id, as the C# does.
		bool HoursWords(const std::string& Area, std::string& Out) const
		{
			Out.clear();
			const std::map<std::string, WeekHours>::const_iterator Wk = HoursOf.find(Area);
			if (Wk == HoursOf.end()) return false;
			const WeekHours& Week = Wk->second;
			std::vector<std::pair<DayHours, std::vector<int> > > Groups;
			std::vector<int> Shut;
			for (int D = 0; D < 7; ++D)
			{
				if (!Week[D].bOpen) { Shut.push_back(D); continue; }
				size_t G = 0;
				while (G < Groups.size() && !(Groups[G].first.Open == Week[D].Open && Groups[G].first.Close == Week[D].Close)) ++G;
				if (G == Groups.size()) Groups.push_back(std::make_pair(Week[D], std::vector<int>(1, D)));
				else Groups[G].second.push_back(D);
			}
			const auto Span = [](const DayHours& H) {
				return H.Open == 0 && H.Close == 24 ? std::string("day and night") : TimeWords(H.Open, false) + " till " + TimeWords(H.Close, true);
			};
			std::vector<std::string> Bits;
			if (7 - (int)Shut.size() <= 3)
			{
				for (size_t G = 0; G < Groups.size(); ++G) Bits.push_back(DaysWords(Groups[G].second) + ", " + Span(Groups[G].first));
			}
			else if (!Groups.empty())
			{
				// The usual hours: the most days, the earliest first.
				size_t U = 0;
				for (size_t G = 1; G < Groups.size(); ++G) if (Groups[G].second.size() > Groups[U].second.size()) U = G;
				const DayHours Usual = Groups[U].first;
				Bits.push_back(Span(Usual) + (Groups.size() == 1 && Shut.empty() ? " every day" : ""));
				for (size_t G = 0; G < Groups.size(); ++G)
				{
					if (G == U) continue;
					const DayHours& H = Groups[G].first;
					Bits.push_back("on " + DaysWords(Groups[G].second) + (H.Close == Usual.Close ? " it opens at " + TimeWords(H.Open, false)
					                                                   : H.Open == Usual.Open ? " it shuts at " + TimeWords(H.Close, true)
					                                                   : " " + Span(H)));
				}
				const std::map<std::string, WeekBreaks>::const_iterator Br = BreaksOf.find(Area);
				if (Br != BreaksOf.end())
				{
					std::vector<std::pair<std::string, std::vector<int> > > ByBreak;
					for (int D = 0; D < 7; ++D)
					{
						if (Br->second[D].empty()) continue;
						std::string Spoken;
						for (size_t K = 0; K < Br->second[D].size(); ++K)
							Spoken += (K ? " and " : "") + std::string("from ") + TimeWords(Br->second[D][K].first, true) + " till " + TimeWords(Br->second[D][K].second, false);
						size_t G = 0;
						while (G < ByBreak.size() && ByBreak[G].first != Spoken) ++G;
						if (G == ByBreak.size()) ByBreak.push_back(std::make_pair(Spoken, std::vector<int>(1, D)));
						else ByBreak[G].second.push_back(D);
					}
					for (size_t G = 0; G < ByBreak.size(); ++G) Bits.push_back("on " + DaysWords(ByBreak[G].second) + " shut " + ByBreak[G].first);
				}
				if (!Shut.empty()) Bits.push_back("shut on " + DaysWords(Shut));
			}
			const std::map<std::string, std::string>::const_iterator Nt = HoursNoteOf.find(Area);
			if (Nt != HoursNoteOf.end()) Bits.push_back(Nt->second);
			for (size_t K = 0; K < Bits.size(); ++K) Out += (K ? ", " : "") + Bits[K];
			return true;
		}

		/// CastDay.cs HoursFor: every shop's hours and whether it is open at this
		/// hour and minute, one line for anybody's talk, in the file's order of
		/// areas; false (the C#'s null) when no area has hours. The first letter
		/// is raised as char.ToUpperInvariant raises it, for ASCII only: no area's
		/// first name starts outside it (28 October 2026).
		bool HoursFor(int Day, int Hour, int Minute, std::string& Out) const
		{
			Out.clear();
			std::vector<std::string> Hours;
			for (const std::string& Key : AreaOrder)
			{
				if (HoursOf.count(Key) == 0) continue;
				const std::vector<std::string> Names = AreaNamesOf(Key);
				std::string Label = Names.empty() ? Key : Names[0];
				if (!Label.empty() && Label[0] >= 'a' && Label[0] <= 'z') Label[0] = (char)(Label[0] - 'a' + 'A');
				std::string Words;
				HoursWords(Key, Words);
				bool bOpen = false;
				const bool bHas = OpenAt(Key, Day, Hour, Minute, bOpen);
				Hours.push_back(Label + ": " + Words + "; " + (bHas && bOpen ? "open now." : "shut now."));
			}
			if (Hours.empty()) return false;
			Out = "Opening hours, as everybody on the street knows them.";
			for (const std::string& H : Hours) Out += " " + H;
			return true;
		}

	private:
		std::map<std::string, std::pair<double, double> > PlaceAt;
		std::map<std::string, double> BodyXAt;   // the place's optional "body_x_m"
		std::map<std::string, std::string> Said, AreaOfPlace, WithinOf, Name, Role, Called, Circle;
		// The file's keepsQuiet word, trimmed (the C#'s _quiet, kept as its word).
		std::map<std::string, std::string> KeepsQuiet;
		std::map<std::string, std::vector<std::string> > AreaNames;
		std::map<std::string, Routine> Daily;
		std::map<std::string, std::pair<std::vector<Routine>, std::vector<bool> > > ByWeekday;
		std::vector<std::string> PeopleList;
		std::set<std::string> NameOnTrust;
		std::set<std::string> NeverPolice;
		std::set<std::string> StreetAreas;
		std::set<std::string> InsidePlaces;
		std::map<std::string, std::string> KeeperOfArea;
		std::vector<Tie> TieList;
		// The shops' hours, their notes and breaks, by area, and the areas in the
		// file's order (U2, 28 October 2026).
		std::map<std::string, WeekHours> HoursOf;
		std::map<std::string, std::string> HoursNoteOf;
		std::map<std::string, WeekBreaks> BreaksOf;
		std::vector<std::string> AreaOrder;

		static int WeekdayOf(const std::string& Key)
		{
			for (int K = 0; K < 7; ++K) if (Key == WeekdayKeys()[K]) return K;
			return -1;
		}
		static bool WholeOrHalf(double V) { return V * 2 == std::floor(V * 2); }

		// CastDay.cs ReadHours: each weekday it opens, [open, close] in whole or
		// half hours from that day's midnight, a close past 24 into the next
		// morning but never round to the next day's opening; a weekday left out
		// is shut. Refused with the C#'s words, in its order.
		static bool ReadHours(const std::string& Area, const LedgerVignette::Value& V, WeekHours& Week, std::string& Err)
		{
			using namespace LedgerVignette;
			if (V.Type != T_OBJ) { Err = "cast file: area " + Area + "'s hours must be an object of weekdays"; return false; }
			if (V.Obj.empty()) { Err = "cast file: area " + Area + "'s hours name no weekday; leave hours out for a place with none"; return false; }
			Week.assign(7, DayHours());
			for (size_t I = 0; I < V.Obj.size(); ++I)
			{
				const int Wd = WeekdayOf(V.Obj[I].first);
				if (Wd < 0) { Err = "cast file: area " + Area + "'s hours name no weekday: " + V.Obj[I].first; return false; }
				const Value& P = V.Obj[I].second;
				const bool bPair = P.Type == T_ARR && P.Arr.size() == 2 && P.Arr[0].Type == T_NUM && P.Arr[1].Type == T_NUM;
				const double Open = bPair ? P.Arr[0].Num : 0.0, Close = bPair ? P.Arr[1].Num : 0.0;
				if (!bPair || Open < 0 || Open >= 24 || Close <= Open || Close > 30 || Close - Open > 24 || !WholeOrHalf(Open) || !WholeOrHalf(Close))
				{
					Err = "cast file: area " + Area + "'s hours on " + V.Obj[I].first + " must be [open, close], whole or half hours, open before 24 and close after it, by six the next morning at the latest";
					return false;
				}
				Week[Wd].bOpen = true;
				Week[Wd].Open = Open;
				Week[Wd].Close = Close;
			}
			// A close past midnight must not run into the next day's opening.
			for (int Wd = 0; Wd < 7; ++Wd)
				if (Week[Wd].bOpen && Week[(Wd + 1) % 7].bOpen && Week[Wd].Close - 24 > Week[(Wd + 1) % 7].Open)
				{
					Err = "cast file: area " + Area + "'s hours on " + WeekdayKeys()[Wd] + " run past the next day's opening";
					return false;
				}
			return true;
		}

		// CastDay.cs ReadBreaks (town list 6by): on a weekday, [from, to], or a
		// list of them, in whole or half hours strictly inside that day's hours,
		// never overlapping; kept in order of their start.
		static bool ReadBreaks(const std::string& Area, const LedgerVignette::Value& V, const WeekHours& Week, WeekBreaks& Breaks, std::string& Err)
		{
			using namespace LedgerVignette;
			if (V.Type != T_OBJ) { Err = "cast file: area " + Area + "'s hours_breaks must be an object of weekdays"; return false; }
			Breaks.assign(7, std::vector<std::pair<double, double> >());
			for (size_t I = 0; I < V.Obj.size(); ++I)
			{
				const std::string& Key = V.Obj[I].first;
				const int Wd = WeekdayOf(Key);
				if (Wd < 0) { Err = "cast file: area " + Area + "'s hours_breaks name no weekday: " + Key; return false; }
				const Value& L = V.Obj[I].second;
				// a list whose first item is a list is a list of pairs; anything else is one pair
				std::vector<const Value*> Pairs;
				if (L.Type == T_ARR && !L.Arr.empty() && L.Arr[0].Type == T_ARR) { for (const Value& X : L.Arr) Pairs.push_back(&X); }
				else { Pairs.push_back(&L); }
				std::vector<std::pair<double, double> > Day;
				for (const Value* X : Pairs)
				{
					const bool bPair = X->Type == T_ARR && X->Arr.size() == 2 && X->Arr[0].Type == T_NUM && X->Arr[1].Type == T_NUM;
					const double From = bPair ? X->Arr[0].Num : 0.0, To = bPair ? X->Arr[1].Num : 0.0;
					bool bOverlaps = false;
					for (const std::pair<double, double>& B : Day) { if (From < B.second && B.first < To) bOverlaps = true; }
					if (!bPair || To <= From || !WholeOrHalf(From) || !WholeOrHalf(To) || !Week[Wd].bOpen || From <= Week[Wd].Open || To >= Week[Wd].Close || bOverlaps)
					{
						Err = "cast file: area " + Area + "'s breaks on " + Key + " must be [from, to], whole or half hours, strictly inside that day's hours, never overlapping";
						return false;
					}
					Day.push_back(std::make_pair(From, To));
				}
				// never overlapping, so no two start together and the order is the C#'s
				std::sort(Day.begin(), Day.end(), [](const std::pair<double, double>& A, const std::pair<double, double>& B) { return A.first < B.first; });
				Breaks[Wd] = Day;
			}
			return true;
		}

		// CastDay.cs TimeWords: a time as a local says it ("half five", "three in
		// the morning"); closing says a close (till seven in the morning).
		static std::string TimeWords(double T, bool bClosing)
		{
			static const char* const Numbers[12] = { "twelve", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven" };
			const int H = (int)std::floor(T);
			const bool bHalf = T - H >= 0.5;
			const std::string Spoken = std::string(bHalf ? "half " : "") + Numbers[H % 12];
			if (!bHalf && H % 24 == 0) return "midnight";
			if (bClosing ? (T > 24 || T <= 7) : T < 7) return Spoken + " in the morning";
			if (!bClosing && T >= 18) return Spoken + " in the evening";
			if (bClosing && T >= 20) return Spoken + " at night";
			return Spoken;
		}

		// CastDay.cs DaysWords: weekdays as a local says them ("Monday to
		// Friday", "Tuesdays and Fridays").
		static std::string DaysWords(std::vector<int> Days)
		{
			static const char* const DayNames[7] = { "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday" };
			std::sort(Days.begin(), Days.end());
			const bool bRun = Days.size() >= 3 && Days.back() - Days.front() == (int)Days.size() - 1;
			if (bRun) return std::string(DayNames[Days.front()]) + " to " + DayNames[Days.back()];
			if (Days.size() == 1) return std::string(DayNames[Days[0]]) + "s";
			std::string Out;
			for (size_t K = 0; K + 1 < Days.size(); ++K) Out += (K ? ", " : "") + std::string(DayNames[Days[K]]) + "s";
			return Out + " and " + DayNames[Days.back()] + "s";
		}

		static std::string Lookup(const std::map<std::string, std::string>& M, const std::string& K)
		{
			std::map<std::string, std::string>::const_iterator I = M.find(K);
			return I == M.end() ? std::string() : I->second;
		}

		bool ReadRoutine(const std::string& Who, const LedgerVignette::Value* Steps, Routine& Out, std::string& Err) const
		{
			using namespace LedgerVignette;
			Out.clear();
			if (Steps == 0 || Steps->Arr.empty()) { Err = "cast file: " + Who + " has no routine"; return false; }
			for (size_t I = 0; I < Steps->Arr.size(); ++I)
			{
				const Value& S = Steps->Arr[I];
				if (S.Type != T_ARR || S.Arr.size() < 2 || S.Arr[0].Type != T_NUM || S.Arr[1].Type != T_STR)
				{
					Err = "cast file: " + Who + " has a step that is not [hour, place]"; return false;
				}
				const double H = S.Arr[0].Num;
				if (H < 0 || H > 23 || H != std::floor(H)) { Err = "cast file: " + Who + " has hour " + Num(H); return false; }
				const std::string& Place = S.Arr[1].Str;
				if (Place != Off() && !PlaceAt.count(Place))
				{
					Err = "cast file: " + Who + " goes to '" + Place + "', which is not a place in the file"; return false;
				}
				Out.push_back(std::make_pair((int)H, Place));
			}
			// Sorted by hour; two steps at one hour are refused, so the order
			// among equals (List.Sort is not stable) never shows.
			std::stable_sort(Out.begin(), Out.end(),
			                 [](const std::pair<int, std::string>& X, const std::pair<int, std::string>& Y) { return X.first < Y.first; });
			for (size_t I = 1; I < Out.size(); ++I)
				if (Out[I].first == Out[I - 1].first)
				{
					char Buf[16];
					std::snprintf(Buf, sizeof(Buf), "%d", Out[I].first);
					Err = "cast file: " + Who + " is in two places at " + Buf + ":00"; return false;
				}
			return true;
		}
	};
}
