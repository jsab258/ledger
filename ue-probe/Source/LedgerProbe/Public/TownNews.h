// TRANSLITERATION of ledger/Assets/Scripts/Core/TownNews.cs, 30 September
// (the town's handover 6aq, "the town's news sample", and the Aftermath of
// handover 6ar; production/handovers/6aq-town-news.md).
//
// THE TOWN'S OWN NEWS: happenings among the named cast are data
// (production/specs/town-news.json), each at a place and hour, seen by
// everybody in that area then and filed as any sighting is, so spread by the
// same rounds and told by StreetVoice's news bank. A story not about him
// raises nobody's suspicion; its parties hold it but never pass it on.
// THE DAMAGE FOUND AFTERWARDS (Aftermath): whoever comes into a deed's area,
// hour by hour until it is mended, finds it, naming nobody.
//
// TRANSLITERATION, NOT REWRITE, as Gossip.h states the method: the C#'s
// FormatException is a false return with its words; its HashSets are kept in
// the order things were added, as a HashSet without removals enumerates.
// ONE KNOWN DEVIATION (the independent check, 30 September): a file that is
// not JSON at all is refused here as "town news: not an object", where the C#
// passes on MiniJson's own words ("Unexpected end of JSON", "Expected string
// at 1"): the C++ reader's messages were never made word for word, and only a
// log reads them; both refuse the same files.
// Checked against PerceptionGolden's EmitTownNews rows (TownNews,
// TownNewsWitnesses) in ue-probe/perception-golden.txt, and its own rows.
//
// NO UNREAL TYPE IS IN THIS FILE, as every file of the port.
#pragma once

#include "CastDay.h"
#include "GameTime.h"
#include "Gossip.h"
#include "MemoryStore.h"
#include "MiniJson.h"
#include "PoliceFile.h"   // PoliceJson: the C#'s own JSON writing and reading helpers

#include <algorithm>
#include <cmath>
#include <set>
#include <string>
#include <utility>
#include <vector>

namespace LedgerCore
{
	/// A set that remembers the order things were added in (a HashSet never removed from).
	struct OrderedIds
	{
		std::vector<std::string> List;
		std::set<std::string> Has;
		bool Add(const std::string& S) { if (!Has.insert(S).second) return false; List.push_back(S); return true; }
		bool Contains(const std::string& S) const { return Has.count(S) > 0; }
		void Clear() { List.clear(); Has.clear(); }
	};

	class TownNews
	{
	public:
		struct Story
		{
			std::string Id, Summary, Area;
			int Day = 0, Hour = 0;
			Fact What = Fact("", "", "");
			double Confidence = 0.9;
			/// The people the story is about: they hold it, never pass it on,
			/// and keep no "I saw" memory of their own doings.
			std::vector<std::string> Parties;
			bool IsParty(const std::string& P) const { return std::find(Parties.begin(), Parties.end(), P) != Parties.end(); }
		};

		static constexpr const char* Subject = "town";

		std::vector<Story> Stories;

		const std::vector<std::string>& Filed() const { return FiledIds.List; }
		void FromFiled(const std::vector<std::string>& Ids) { FiledIds.Clear(); for (const std::string& Id : Ids) FiledIds.Add(Id); }

		/// Reads the news file: false, with what is wrong, where the C# throws.
		static bool Parse(const std::string& Json, TownNews& Out, std::string& Err)
		{
			using LedgerVignette::Value;
			Value Root;
			std::string JErr;
			if (!MiniJson::Deserialize(Json, Root, JErr) || Root.Type != LedgerVignette::T_OBJ) { Err = "town news: not an object"; return false; }
			const Value* Ss = PoliceJson::Last(Root, "stories");
			if (Ss == nullptr || Ss->Type != LedgerVignette::T_ARR) { Err = "town news: no stories"; return false; }
			TownNews News;
			for (const Value& So : Ss->Arr)
			{
				if (So.Type != LedgerVignette::T_OBJ) { Err = "town news: a story that is not an object"; return false; }
				Story St;
				PoliceJson::GetString(So, "id", St.Id);
				PoliceJson::GetString(So, "summary", St.Summary);
				PoliceJson::GetString(So, "area", St.Area);
				if (St.Id.empty() || St.Summary.empty() || St.Area.empty()) { Err = "town news: a story needs an id, a summary and an area"; return false; }
				const Value* D = PoliceJson::Last(So, "day");
				const Value* H = PoliceJson::Last(So, "hour");
				if (D == nullptr || D->Type != LedgerVignette::T_NUM || H == nullptr || H->Type != LedgerVignette::T_NUM || H->Num < 0 || H->Num > 23)
				{
					Err = "town news: " + St.Id + " needs a day and an hour";
					return false;
				}
				St.Day = (int)D->Num;
				St.Hour = (int)H->Num;
				const Value* F = PoliceJson::Last(So, "fact");
				if (F == nullptr || F->Type != LedgerVignette::T_ARR || F->Arr.size() != 3 || F->Arr[0].Type != LedgerVignette::T_STR
				    || F->Arr[1].Type != LedgerVignette::T_STR || F->Arr[2].Type != LedgerVignette::T_STR)
				{
					Err = "town news: " + St.Id + " needs a fact [subject, predicate, value]";
					return false;
				}
				// The town's own subject, and only it: StreetVoice tells "town"
				// stories as news, never a killing or anything about the player.
				if (F->Arr[0].Str != Subject) { Err = "town news: " + St.Id + "'s fact must have the subject \"town\""; return false; }
				for (const Story& Other : News.Stories)
				{
					if (Other.Id == St.Id || (Other.What.Subject == F->Arr[0].Str && Other.What.Predicate == F->Arr[1].Str))
					{
						Err = "town news: " + St.Id + " repeats an id or a fact";
						return false;
					}
				}
				St.What = Fact(F->Arr[0].Str, F->Arr[1].Str, F->Arr[2].Str);
				const Value* C = PoliceJson::Last(So, "confidence");
				if (C != nullptr && C->Type == LedgerVignette::T_NUM) St.Confidence = DotNetMax(0.0, DotNetMin(1.0, C->Num));
				const Value* Ps = PoliceJson::Last(So, "parties");
				if (Ps != nullptr && Ps->Type == LedgerVignette::T_ARR)
					for (const Value& P : Ps->Arr) { if (P.Type == LedgerVignette::T_STR && !P.Str.empty()) St.Parties.push_back(P.Str); }
				News.Stories.push_back(St);
			}
			Out = News;
			return true;
		}

		/// Files every story whose hour has come and that is not yet filed, as
		/// seen by everybody in its area at that hour; returns the ids filed.
		std::vector<std::string> Seed(GossipMill* Mill, const CastDay* Cast, const GameTime& Now)
		{
			std::vector<std::string> Out;
			if (Mill == nullptr || Cast == nullptr) return Out;
			for (const Story& St : Stories)
			{
				if (FiledIds.Contains(St.Id)) continue;
				const GameTime At(St.Day, St.Hour, 0);
				if (Now.TotalMinutes() < At.TotalMinutes()) continue;
				FiledIds.Add(St.Id);
				for (const std::string& P : Cast->People())
				{
					if (!(Cast->AreaOf(Cast->PlaceOf(P, St.Day, St.Hour)) == St.Area || St.IsParty(P))) continue;
					const GossiperPtr G = Mill->Get(P);
					const size_t Memories = G && G->Memory ? G->Memory->Events.size() : 0;
					Mill->Witness(P, St.What, St.Summary, false, At, St.Confidence);
					if (G && St.IsParty(P))
					{
						// Theirs to know, not to tell, and not to remember as seen.
						const std::string Topic = St.What.Subject + "." + St.What.Predicate;
						if (!G->SuppressedHas(Topic)) G->Suppressed.push_back(Topic);
						if (G->Memory && G->Memory->Events.size() > Memories) G->Memory->Events.erase(G->Memory->Events.begin() + Memories, G->Memory->Events.end());
					}
				}
				Out.push_back(St.Id);
			}
			return Out;
		}

		/// Who saw a story: everybody in its area at its hour.
		std::vector<std::string> WitnessesOf(const Story* St, const CastDay* Cast) const
		{
			std::vector<std::string> W;
			if (St == nullptr || Cast == nullptr) return W;
			for (const std::string& P : Cast->People()) { if (Cast->AreaOf(Cast->PlaceOf(P, St->Day, St->Hour)) == St->Area) W.push_back(P); }
			return W;
		}

	private:
		OrderedIds FiledIds;
	};

	/// THE DAMAGE FOUND AFTERWARDS (TownNews.cs Aftermath).
	class Aftermath
	{
	public:
		static constexpr int LongestUnmendedDays = 90;

		const std::string& Area() const { return AreaValue; }
		const std::string& Key() const { return KeyValue; }
		const std::string& Said() const { return SaidValue; }
		const GameTime& DoneAt() const { return DoneAtValue; }
		const GameTime& MendedAt() const { return MendedAtValue; }
		const std::vector<std::string>& FoundBy() const { return Found.List; }

		/// Boarded that morning, the glazier by four the working day after, never a Sunday.
		static GameTime DefaultMend(const GameTime& Done)
		{
			int D = Done.Hour < 6 ? Done.Day : Done.Day + 1;
			while (CastDay::Weekday(D) == 6) ++D;
			return GameTime(D, 16, 0);
		}

		std::string MemoryOf() const { return "I came by and saw it for myself: " + SaidValue + ". I never saw who did it."; }

		/// A deed's damage; false (the C#'s ArgumentException) without an area, a key and words.
		static bool Make(const std::string& InArea, const std::string& InKey, const std::string& InSaid, const GameTime& Done,
		                 const GameTime* Mended, const std::vector<std::string>* LeaveOut, Aftermath& Out)
		{
			if (InArea.empty() || InKey.empty() || InSaid.empty()) return false;
			Aftermath A;
			A.AreaValue = InArea; A.KeyValue = InKey; A.SaidValue = InSaid; A.DoneAtValue = Done;
			const GameTime Mend = Mended != nullptr ? *Mended : DefaultMend(Done);
			const long long Longest = Done.TotalMinutes() + LongestUnmendedDays * 24LL * 60;
			A.MendedAtValue = Mend.TotalMinutes() > Longest ? GameTime::FromTotalMinutes(Longest) : Mend;
			if (LeaveOut != nullptr) for (const std::string& P : *LeaveOut) A.LeaveOutIds.Add(P);
			A.NextHour = FloorDiv(Done.TotalMinutes(), 60) + 1;
			Out = A;
			return true;
		}

		/// THE HOURS SINCE THE LAST CALL, up to Now or its mending: whoever came
		/// into the area in them finds it. Returns who, and when.
		std::vector<std::pair<std::string, GameTime> > Tick(GossipMill* Mill, const CastDay* Cast, const GameTime& Now)
		{
			std::vector<std::pair<std::string, GameTime> > Out;
			if (Mill == nullptr || Cast == nullptr) return Out;
			const long long NowM = Now.TotalMinutes(), MendM = MendedAtValue.TotalMinutes();
			const Fact What(TownNews::Subject, KeyValue, "found");
			long long H = NextHour;
			for (; H * 60 <= NowM && (H + 1) * 60 <= MendM; ++H)
			{
				const int Day = (int)FloorDiv(H, 24), Hour = (int)(H - (long long)Day * 24);
				for (const std::string& P : Cast->People())
				{
					if (Found.Contains(P) || LeaveOutIds.Contains(P)) continue;
					if (Cast->AreaOf(Cast->PlaceOf(P, Day, Hour)) != AreaValue) continue;
					const GossiperPtr G = Mill->Get(P);
					if (!G) continue;
					Found.Add(P);
					// Heard it before coming by: they see it, and keep the one copy.
					bool bHeld = false;
					for (const RumorPtr& R : G->Rumors) { if (R && R->Content.Subject == TownNews::Subject && R->Content.Predicate == KeyValue) { bHeld = true; break; } }
					if (bHeld) continue;
					const GameTime At(Day, Hour, 0);
					const size_t Memories = G->Memory ? G->Memory->Events.size() : 0;
					Mill->Witness(P, What, SaidValue, false, At, 0.9);
					if (G->Memory)
					{
						if (G->Memory->Events.size() > Memories) G->Memory->Events.erase(G->Memory->Events.begin() + Memories, G->Memory->Events.end());
						G->Memory->Append(MemoryEvent(At, "observation", 0.6, MemoryOf()));
					}
					Out.push_back(std::make_pair(P, At));
				}
			}
			if (H > NextHour) NextHour = H;
			return Out;
		}

		std::string ToJson() const
		{
			std::string J = "{\"area\":" + PoliceJson::Str(AreaValue) + ",\"key\":" + PoliceJson::Str(KeyValue) + ",\"said\":" + PoliceJson::Str(SaidValue)
				+ ",\"done\":" + std::to_string(DoneAtValue.TotalMinutes()) + ",\"mended\":" + std::to_string(MendedAtValue.TotalMinutes()) + ",\"leaveOut\":[";
			for (size_t I = 0; I < LeaveOutIds.List.size(); ++I) J += (I ? "," : "") + PoliceJson::Str(LeaveOutIds.List[I]);
			J += "],\"found\":[";
			for (size_t I = 0; I < Found.List.size(); ++I) J += (I ? "," : "") + PoliceJson::Str(Found.List[I]);
			return J + "],\"next\":" + std::to_string(NextHour) + "}";
		}

		/// From ToJson's text; false for anything it cannot read.
		static bool FromJson(const std::string& SavedJson, Aftermath& Out)
		{
			LedgerVignette::Value Root;
			std::string Err;
			if (!MiniJson::Deserialize(SavedJson, Root, Err) || Root.Type != LedgerVignette::T_OBJ) return false;
			return FromValue(Root, Out);
		}

		static bool FromValue(const LedgerVignette::Value& Root, Aftermath& Out)
		{
			using LedgerVignette::Value;
			std::string InArea, InKey, InSaid;
			PoliceJson::GetString(Root, "area", InArea);
			PoliceJson::GetString(Root, "key", InKey);
			PoliceJson::GetString(Root, "said", InSaid);
			if (InArea.empty() || InKey.empty() || InSaid.empty()) return false;
			auto ReadMinutes = [&Root](const char* K, long long& V) {
				V = 0;
				const Value* O = PoliceJson::Last(Root, K);
				if (O == nullptr || O->Type != LedgerVignette::T_NUM || std::fabs(O->Num) > 1e8 || O->Num != std::floor(O->Num)) return false;
				V = (long long)O->Num;
				return true;
			};
			long long Done = 0, Mended = 0, Next = 0;
			if (!ReadMinutes("done", Done) || !ReadMinutes("mended", Mended) || Mended < Done) return false;
			std::vector<std::string> Leave;
			const Value* Ls = PoliceJson::Last(Root, "leaveOut");
			if (Ls != nullptr && Ls->Type == LedgerVignette::T_ARR)
				for (const Value& X : Ls->Arr) { if (X.Type == LedgerVignette::T_STR && !X.Str.empty()) Leave.push_back(X.Str); }
			const GameTime MendedAt = GameTime::FromTotalMinutes(Mended);
			Aftermath A;
			Make(InArea, InKey, InSaid, GameTime::FromTotalMinutes(Done), &MendedAt, &Leave, A);
			const Value* Fs = PoliceJson::Last(Root, "found");
			if (Fs != nullptr && Fs->Type == LedgerVignette::T_ARR)
				for (const Value& X : Fs->Arr) { if (X.Type == LedgerVignette::T_STR && !X.Str.empty()) A.Found.Add(X.Str); }
			// Never before the hour after the deed, never past its mending.
			if (ReadMinutes("next", Next)) A.NextHour = std::max(A.NextHour, std::min(Next, FloorDiv(Mended, 60) + 1));
			Out = A;
			return true;
		}

	private:
		std::string AreaValue, KeyValue, SaidValue;
		GameTime DoneAtValue, MendedAtValue;
		OrderedIds LeaveOutIds, Found;
		long long NextHour = 0;

		static long long FloorDiv(long long A, long long B) { return A >= 0 ? A / B : -((-A + B - 1) / B); }
	};
}
