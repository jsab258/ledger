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
// MickeysOwn). NOT HERE: the
// talk program's own reads (SpokenAreas, Fits, AreaFor, WhoNamed, Described,
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
