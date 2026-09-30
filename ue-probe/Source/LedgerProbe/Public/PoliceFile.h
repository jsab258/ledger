// TRANSLITERATION of ledger/Assets/Scripts/Core/PoliceFile.cs and Custody.cs,
// 30 September (the town's handover 6ar, "after a deed: the damage, the
// police, DS Ellis, an arrest"; production/handovers/6ar-after-a-deed.md),
// with Homicide.cs's Inquiry and Police.SummonsEllis, which Ellis's visits read.
//
// WHO TELLS THE POLICE, WHAT THE POLICE DO, WHEN DS ELLIS COMES: most offences
// are never reported; a victim reports far more than a witness; damage brings
// a uniformed constable, a wounding, robbery or killing a detective; talk is
// grounds to ask, never to charge: an arrest waits for a statement that names
// him. An arrest costs hours, not the game (Custody): held for about as long
// as the Home Office found for his offence in the late 1980s, then cautioned or
// charged and bailed. Her asking after him is the street's news, not his secret.
//
// TRANSLITERATION, NOT REWRITE, as Gossip.h states the method: the C#'s
// nullable returns are false or nullptr here.
// TWO KNOWN DEVIATIONS (the independent check, 30 September). FromJson sorts
// the visits and calls by day with a stable sort, where the C#'s List.Sort is
// not stable (two or three with the same day can come back swapped, and a
// reload swaps them again); only their order and the save's bytes differ, no
// decision, and the C# is asked to sort stably (FINDINGS, for the town).
// WhoSheAsks orders ids by UTF-8 bytes where the C# orders UTF-16 units; the
// same for every id outside the astral planes and the high BMP, and the cast's
// ids are plain ASCII. Checked against PerceptionGolden's EmitTaken and EmitPoliceAsked
// rows in ue-probe/perception-golden.txt, and through the wait's rows.
//
// NO UNREAL TYPE IS IN THIS FILE, as every file of the port.
#pragma once

#include "CastDay.h"
#include "GameTime.h"
#include "Gossip.h"
#include "MemoryStore.h"
#include "MiniJson.h"

#include <algorithm>
#include <cmath>
#include <cstdio>
#include <functional>
#include <memory>
#include <set>
#include <string>
#include <utility>
#include <vector>

namespace LedgerCore
{
	/// What was done, as the law of 1990 grades it.
	enum class Offence { Suspicious, Damage, Assault, Wounding, Robbery, Killing };
	/// How the police came to hold something.
	enum class Known { Talk, Description, Statement };
	/// Homicide.cs 83: the body's inquiry, which brings Ellis at Procedure or beyond.
	enum class Inquiry { None, Procedure, Investigation, Manhunt };

	inline const char* OffenceName(Offence O)
	{
		switch (O)
		{
		case Offence::Suspicious: return "Suspicious";
		case Offence::Damage: return "Damage";
		case Offence::Assault: return "Assault";
		case Offence::Wounding: return "Wounding";
		case Offence::Robbery: return "Robbery";
		default: return "Killing";
		}
	}
	inline bool OffenceFromName(const std::string& S, Offence& Out)
	{
		for (int I = 0; I <= (int)Offence::Killing; ++I) { if (S == OffenceName((Offence)I)) { Out = (Offence)I; return true; } }
		return false;
	}
	inline const char* KnownName(Known K) { return K == Known::Talk ? "Talk" : K == Known::Description ? "Description" : "Statement"; }
	inline bool KnownFromName(const std::string& S, Known& Out)
	{
		for (int I = 0; I <= (int)Known::Statement; ++I) { if (S == KnownName((Known)I)) { Out = (Known)I; return true; } }
		return false;
	}

	namespace Police
	{
		/// Homicide.cs 459.
		inline bool SummonsEllis(Inquiry I) { return (int)I >= (int)Inquiry::Procedure; }
	}

	namespace PoliceJson
	{
		/// MiniJson.cs EscapeString, byte for byte on UTF-8 (only ASCII is escaped).
		inline std::string Str(const std::string& S)
		{
			std::string O = "\"";
			for (unsigned char C : S)
			{
				switch (C)
				{
				case '"': O += "\\\""; break;
				case '\\': O += "\\\\"; break;
				case '\n': O += "\\n"; break;
				case '\r': O += "\\r"; break;
				case '\t': O += "\\t"; break;
				case '\b': O += "\\b"; break;
				case '\f': O += "\\f"; break;
				default:
					if (C < 0x20) { char B[8]; std::snprintf(B, sizeof(B), "\\u%04x", (unsigned)C); O += B; }
					else O += (char)C;
				}
			}
			return O + "\"";
		}

		/// A key given twice keeps its last value, as the C#'s dictionary does.
		inline const LedgerVignette::Value* Last(const LedgerVignette::Value& Obj, const char* Key)
		{
			const LedgerVignette::Value* Out = nullptr;
			for (const auto& Kv : Obj.Obj) { if (Kv.first == Key) Out = &Kv.second; }
			return Out;
		}

		/// MiniJson.GetString: the value when it is a string, else false (null).
		inline bool GetString(const LedgerVignette::Value& Obj, const char* Key, std::string& Out)
		{
			const LedgerVignette::Value* V = Last(Obj, Key);
			if (V == nullptr || V->Type != LedgerVignette::T_STR) return false;
			Out = V->Str;
			return true;
		}
	}

	/// How a spell in custody ends.
	enum class CustodyEnd { Cautioned, Charged, BailedToReturn };
	inline const char* CustodyEndName(CustodyEnd E) { return E == CustodyEnd::Cautioned ? "Cautioned" : E == CustodyEnd::Charged ? "Charged" : "BailedToReturn"; }

	class PoliceFile;

	/// WHAT AN ARREST DOES (Custody.cs): hours in the cells, then a caution, or
	/// a charge and bail to the next sitting, never the game.
	class Custody
	{
	public:
		static constexpr const char* TakenPrefix = "player.taken_d";
		static constexpr const char* TakenSaid = "the police took Mickey's nephew away in a car";
		static constexpr const char* Caution = "You do not have to say anything unless you wish to do so, but what you say may be given in evidence.";
		static constexpr const char* Rights = "You can have someone told you're here. You can see a solicitor, and the duty solicitor is free. You can read the codes of practice. You don't have to do any of that now.";

		const std::string& Topic() const { return TopicValue; }
		Offence OffenceOf() const { return OffenceValue; }
		const GameTime& TakenAt() const { return TakenAtValue; }
		const GameTime& OutAt() const { return OutAtValue; }
		CustodyEnd End() const { return EndValue; }
		bool CoatKept() const { return bCoatKept; }
		int AnswerDay() const { return AnswerDayValue; }

		/// Arrestable(O) as PoliceFile.Arrestable (declared here to keep one header).
		static bool Arrestable(Offence O) { return O == Offence::Damage || (int)O >= (int)Offence::Wounding; }

		/// HE IS TAKEN IN at At; none, and nothing done, for an offence no arrest is for.
		static std::shared_ptr<Custody> Take(const std::string& InTopic, Offence O, const GameTime& At, bool bOwnsUp, bool bInTheCoat)
		{
			if (InTopic.empty() || !Arrestable(O)) return nullptr;
			double Hours;
			CustodyEnd E;
			switch (O)
			{
			case Offence::Damage: E = bOwnsUp ? CustodyEnd::Cautioned : CustodyEnd::Charged; Hours = bOwnsUp ? 2 : 6; break;
			case Offence::Wounding: E = CustodyEnd::Charged; Hours = 8; break;
			case Offence::Robbery: E = CustodyEnd::Charged; Hours = 12; break;
			default: E = CustodyEnd::BailedToReturn; Hours = 22; break;
			}
			// Math.Round of a whole number of minutes is that number.
			const GameTime Out = At.AddMinutes((int)std::llround(Hours * 60));
			std::shared_ptr<Custody> C(new Custody());
			C->TopicValue = InTopic;
			C->OffenceValue = O;
			C->TakenAtValue = At;
			C->OutAtValue = Out;
			C->EndValue = E;
			C->bCoatKept = bInTheCoat && E != CustodyEnd::Cautioned;
			C->AnswerDayValue = E == CustodyEnd::Cautioned ? -1 : E == CustodyEnd::Charged ? NextSitting(Out.Day) : Out.Day + 28;
			return C;
		}

		/// The magistrates' first sitting after the day he is let go: the next weekday.
		static int NextSitting(int Day)
		{
			int D = Day + 1;
			while (CastDay::Weekday(D) >= 5) ++D;
			return D;
		}

		static const char* OffenceWords(Offence O)
		{
			return O == Offence::Damage ? "criminal damage" : O == Offence::Wounding ? "wounding" : O == Offence::Robbery ? "robbery"
			     : O == Offence::Killing ? "murder" : O == Offence::Assault ? "assault" : "being suspicious";
		}

		std::string ArrestWords() const { return std::string("I'm arresting you on suspicion of ") + OffenceWords(OffenceValue) + ". " + Caution; }

		std::string ReleaseWords() const
		{
			static const char* const Weekdays[7] = { "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday" };
			const std::string Coat = bCoatKept ? " We're keeping the coat you had on, as evidence." : "";
			const std::string Day = AnswerDayValue >= 0 ? Weekdays[CastDay::Weekday(AnswerDayValue)] : "";
			switch (EndValue)
			{
			case CustodyEnd::Cautioned:
				return std::string("You've been cautioned for the ") + OffenceWords(OffenceValue) + ": you admitted it, so there's no charge, but the caution stays on your record and can be mentioned in court if you're ever back. You're free to go.";
			case CustodyEnd::Charged:
				return std::string("You are charged with the offence(s) shown below. ") + Caution + " The offence: " + OffenceWords(OffenceValue) + ". You're bailed to appear at the magistrates' court on " + Day
					+ " at ten o'clock. Not turning up is an offence in itself." + Coat;
			default:
				return "You're released on bail without charge, while enquiries continue. You're to come back to this station in four weeks, on a " + Day
					+ ", at ten o'clock. Not turning up is an offence in itself." + Coat;
			}
		}

		bool Holds(const GameTime& Now) const { return Now.TotalMinutes() >= TakenAtValue.TotalMinutes() && Now.TotalMinutes() < OutAtValue.TotalMinutes(); }

		static bool IsTaken(const RumorPtr& R)
		{
			const std::string P = TakenPrefix;
			return R && R->TopicKey().compare(0, P.size(), P) == 0;
		}

		/// THE STREET SEES HIM TAKEN: everybody of the cast in that area at that
		/// hour, once a person a day. Returns who saw it.
		static std::vector<std::string> SeenTaken(GossipMill* Mill, const CastDay* Cast, const std::string& Area, const GameTime& At)
		{
			std::vector<std::string> Saw;
			if (Mill == nullptr || Cast == nullptr || Area.empty()) return Saw;
			const Fact What("player", "taken_d" + std::to_string(At.Day), "police");
			const std::string Topic = std::string(TakenPrefix) + std::to_string(At.Day);
			for (const std::string& P : Cast->People())
			{
				std::string Theirs;
				if (!Cast->AreaOf(Cast->PlaceOf(P, At.Day, At.Hour), Theirs) || Theirs != Area) continue;
				const GossiperPtr G = Mill->Get(P);
				if (!G) continue;
				bool bHeld = false;
				for (const RumorPtr& R : G->Rumors) { if (R && R->TopicKey() == Topic && R->Hops == 0) { bHeld = true; break; } }
				if (bHeld) continue;
				Mill->Witness(P, What, TakenSaid, false, At, 1.0);
				Saw.push_back(P);
			}
			return Saw;
		}

		std::string ToJson() const
		{
			return "{\"topic\":" + PoliceJson::Str(TopicValue) + ",\"offence\":\"" + OffenceName(OffenceValue) + "\",\"taken\":" + std::to_string(TakenAtValue.TotalMinutes())
				+ ",\"ownsUp\":" + (EndValue == CustodyEnd::Cautioned ? "true" : "false") + ",\"coat\":" + (bCoatKept ? "true" : "false") + "}";
		}

		/// From ToJson's text, taken again through Take; none for anything it cannot read.
		static std::shared_ptr<Custody> FromJson(const std::string& SavedJson)
		{
			LedgerVignette::Value Root;
			std::string Err;
			if (!MiniJson::Deserialize(SavedJson, Root, Err) || Root.Type != LedgerVignette::T_OBJ) return nullptr;
			return FromValue(Root);
		}

		static std::shared_ptr<Custody> FromValue(const LedgerVignette::Value& Root)
		{
			std::string InTopic, Os;
			if (!PoliceJson::GetString(Root, "topic", InTopic) || InTopic.empty()) return nullptr;
			Offence O;
			if (!PoliceJson::GetString(Root, "offence", Os) || !OffenceFromName(Os, O)) return nullptr;
			const LedgerVignette::Value* T = PoliceJson::Last(Root, "taken");
			if (T == nullptr || T->Type != LedgerVignette::T_NUM || T->Num < 0 || T->Num > 1e8 || T->Num != std::floor(T->Num)) return nullptr;
			const LedgerVignette::Value* Ou = PoliceJson::Last(Root, "ownsUp");
			const LedgerVignette::Value* Co = PoliceJson::Last(Root, "coat");
			const bool bOwnsUp = Ou != nullptr && Ou->Type == LedgerVignette::T_BOOL && Ou->Bool;
			const bool bCoat = Co != nullptr && Co->Type == LedgerVignette::T_BOOL && Co->Bool;
			return Take(InTopic, O, GameTime::FromTotalMinutes((long long)T->Num), bOwnsUp, bCoat);
		}

	private:
		std::string TopicValue;
		Offence OffenceValue = Offence::Suspicious;
		GameTime TakenAtValue, OutAtValue;
		CustodyEnd EndValue = CustodyEnd::Cautioned;
		bool bCoatKept = false;
		int AnswerDayValue = -1;

		Custody() {}
	};

	class PoliceFile
	{
	public:
		static constexpr int LoudAt = 3;
		static constexpr int TalkNoSoonerThan = 3;
		static constexpr const char* AskingPrefix = "player.police_d";
		static constexpr const char* AskedSaid = "that detective, Ellis, was on Quay Street asking after Mickey's nephew";
		static constexpr const char* AskedMemory = "DS Ellis, the detective, stopped me on Quay Street and asked me about Mickey's nephew, the new owner.";

		struct Entry
		{
			std::string Who;     // the person the police heard it from (a cast id)
			std::string Topic;   // the deed's topic key
			Offence Offence_;
			Known How;
			int Day;
		};

		const std::vector<Entry>& Entries() const { return EntriesList; }
		const std::vector<std::pair<int, std::string> >& Visits() const { return VisitsList; }
		int EllisCameOn() const { return VisitsList.empty() ? -1 : VisitsList[0].first; }
		/// The first visit's reason, or false (the C#'s null).
		bool EllisCameFor(std::string& Out) const { if (VisitsList.empty()) return false; Out = VisitsList[0].second; return true; }
		const std::vector<std::pair<int, std::string> >& ConstableCalls() const { return CallsList; }

		/// WHETHER A CONSTABLE CALLS TODAY TO TAKE HIM IN: the deed's topic into
		/// Out, recorded, or false.
		bool ConstableComes(int Day, std::string& Out)
		{
			if (!ConstableWouldCome(Day, Out)) return false;
			CallsList.push_back(std::make_pair(Day, Out));
			return true;
		}

		/// The deed a constable would call for on Day, nothing recorded.
		bool ConstableWouldCome(int Day, std::string& Out) const
		{
			for (const auto& C : CallsList) { if (C.first == Day) return false; }
			for (const Entry& E : EntriesList)
			{
				if (E.Offence_ != Offence::Damage || E.How != Known::Statement || E.Day >= Day || WasTaken(E.Topic)) continue;
				bool bCalled = false;
				for (const auto& C : CallsList) { if (C.second == E.Topic) { bCalled = true; break; } }
				if (bCalled) continue;
				Out = E.Topic;
				return true;
			}
			return false;
		}

		bool WasTaken(const std::string& Topic) const
		{
			for (const auto& T : TakenList) { if (T.first == Topic) return true; }
			return false;
		}

		/// HE IS TAKEN IN for a deed they can arrest him for; none, and nothing
		/// done, when there is no arrest to make or he is already in the cells.
		std::shared_ptr<Custody> TakeIn(const std::string* Topic, const GameTime& Now, bool bOwnsUp, bool bInTheCoat)
		{
			if (Topic == nullptr || !CanArrest(Topic)) return nullptr;
			for (const auto& T : TakenList) { if (T.second > Now.TotalMinutes()) return nullptr; }
			Offence O = Offence::Suspicious;
			for (const Entry& E : EntriesList) { if (E.Topic == *Topic && E.How == Known::Statement && Custody::Arrestable(E.Offence_)) { O = E.Offence_; break; } }
			std::shared_ptr<Custody> C = Custody::Take(*Topic, O, Now, bOwnsUp, bInTheCoat);
			if (C) TakenList.push_back(std::make_pair(*Topic, C->OutAt().TotalMinutes()));
			return C;
		}

		static bool Arrestable(Offence O) { return Custody::Arrestable(O); }

		/// WOULD THIS PERSON GO TO THE POLICE with what they saw or suffered?
		static bool WouldReport(const Gossiper* G, Offence O, bool bVictim, const std::string* Topic, bool bNeverToPolice = false)
		{
			if (G == nullptr || bNeverToPolice || O == Offence::Suspicious || G->Leashed) return false;
			if (Topic != nullptr && G->SuppressedHas(*Topic) && O != Offence::Killing) return false;
			if (bVictim)
			{
				if (O == Offence::Killing) return false;
				if (O == Offence::Damage) return true;
				const double Settle = O == Offence::Assault ? 0.4 : 0.6;
				const double Fear = O == Offence::Assault ? 0.5 : 0.3;
				return G->Loyalty < Settle && G->Nerve >= Fear;
			}
			if (!Detective(O) && O != Offence::Damage) return false;
			if (O == Offence::Killing) return G->Loyalty < 0.5;
			return G->Nerve >= 0.4 && G->Loyalty < 0.5;
		}

		/// A report, as the police hold it; the entry, or false when this person
		/// has already given as good a statement about this deed.
		bool Report(const std::string& Who, const std::string& Topic, Offence O, int Rung, int Day)
		{
			if (Who.empty() || Topic.empty()) return false;
			for (Entry& E : EntriesList)
			{
				if (E.Who == Who && E.Topic == Topic && E.How != Known::Talk)
				{
					if (E.How == Known::Description && Rung >= 4) { E.How = Known::Statement; E.Day = Day; return true; }
					return false;
				}
			}
			EntriesList.push_back(Entry{ Who, Topic, O, Rung >= 4 ? Known::Statement : Known::Description, Day });
			return true;
		}

		/// Talk reaching her on her enquiries, once a person a deed.
		void Heard(const std::string& Who, const std::string& Topic, Offence O, int Day)
		{
			if (Who.empty() || Topic.empty()) return;
			for (const Entry& E : EntriesList) { if (E.Who == Who && E.Topic == Topic && E.How == Known::Talk) return; }
			EntriesList.push_back(Entry{ Who, Topic, O, Known::Talk, Day });
		}

		/// HOW LOUD THE STREET IS about his nights.
		static int Loudness(const GossipMill* Mill)
		{
			if (Mill == nullptr) return 0;
			int N = 0;
			for (const GossiperPtr& A : Mill->Agents()) { if (A && !TalkOf(*Mill, *A).empty()) ++N; }
			return N;
		}

		/// WHAT THE STREET TELLS HER when she comes for its talk.
		void HearTheStreet(const GossipMill* Mill, int Day, const std::function<Offence(const std::string&)>& OffenceOf)
		{
			if (Mill == nullptr) return;
			for (const GossiperPtr& A : Mill->Agents())
			{
				if (!A) continue;
				for (const RumorPtr& R : TalkOf(*Mill, *A)) Heard(A->Id, R->TopicKey(), OffenceOf ? OffenceOf(R->TopicKey()) : Offence::Suspicious, Day);
			}
		}

		/// WHETHER SHE COMES TO QUAY STREET TODAY, and for what: the reason into
		/// Out, recorded, or false.
		bool EllisComes(const GossipMill* Mill, int Day, Inquiry I, std::string& Out)
		{
			const std::vector<std::string> All = EllisWouldComeAll(Mill, Day, I);
			if (All.empty()) return false;
			Out = All[0];
			VisitsList.push_back(std::make_pair(Day, Out));
			return true;
		}

		/// Every reason that would bring her on Day, in EllisComes' order, nothing recorded.
		std::vector<std::string> EllisWouldComeAll(const GossipMill* Mill, int Day, Inquiry I = Inquiry::None) const
		{
			std::vector<std::string> All;
			auto Fresh = [this, &All](const std::string& Why) {
				for (const auto& V : VisitsList) { if (V.second == Why) return false; }
				return std::find(All.begin(), All.end(), Why) == All.end();
			};
			if (Police::SummonsEllis(I) && Fresh("body")) All.push_back("body");
			for (const Entry& E : EntriesList)
			{
				const std::string Why = std::string(OffenceName(E.Offence_)) + " " + E.Topic;
				if (Detective(E.Offence_) && E.How != Known::Talk && Fresh(Why)) All.push_back(Why);
			}
			if (Day >= TalkNoSoonerThan && Loudness(Mill) >= LoudAt && Fresh("talk")) All.push_back("talk");
			return All;
		}

		static bool IsAsking(const RumorPtr& R)
		{
			const std::string P = AskingPrefix;
			return R && R->TopicKey().compare(0, P.size(), P) == 0;
		}

		/// WHO SHE ASKS on a visit about him: everybody of his day world who
		/// holds a story of his nights, in order.
		static std::vector<std::string> WhoSheAsks(const GossipMill* Mill)
		{
			std::vector<std::string> Who;
			if (Mill == nullptr) return Who;
			for (const GossiperPtr& A : Mill->Agents())
			{
				if (!A || A->Circle != "day") continue;
				for (const RumorPtr& R : A->Rumors)
				{
					if (R && R->Content.Subject == "player" && R->Sensitive && R->Confidence > 0) { Who.push_back(A->Id); break; }
				}
			}
			std::sort(Who.begin(), Who.end());
			return Who;
		}

		/// SHE ASKED THEM: each remembers it and has it to pass on as the
		/// street's news. Returns how many she asked.
		static int Asked(GossipMill* Mill, const std::vector<std::string>* Who, const std::string& Why, const GameTime& Now)
		{
			if (Mill == nullptr || Who == nullptr || Why.empty() || Why == "body") return 0;
			const Fact What("player", "police_d" + std::to_string(Now.Day), "asking");
			const std::string Topic = std::string(AskingPrefix) + std::to_string(Now.Day);
			std::set<std::string> Seen;
			int N = 0;
			for (const std::string& Id : *Who)
			{
				const GossiperPtr G = Mill->Get(Id);
				if (!G || !Seen.insert(Id).second) continue;
				bool bHeld = false;
				for (const RumorPtr& R : G->Rumors) { if (R && R->TopicKey() == Topic && R->Hops == 0) { bHeld = true; break; } }
				if (bHeld) continue;
				const size_t Memories = G->Memory ? G->Memory->Events.size() : 0;
				Mill->Witness(Id, What, AskedSaid, false, Now, 1.0);
				// Their memory of it is being asked, not a sighting of their own.
				if (G->Memory)
				{
					if (G->Memory->Events.size() > Memories) G->Memory->Events.erase(G->Memory->Events.begin() + Memories, G->Memory->Events.end());
					G->Memory->Append(MemoryEvent(Now, "observation", 0.7, AskedMemory));
				}
				++N;
			}
			return N;
		}

		/// WHAT SHE CAN PUT TO HIM about one deed: the strongest thing she holds, or false.
		bool Strongest(const std::string& Topic, Known& Out) const
		{
			bool bAny = false;
			for (const Entry& E : EntriesList)
			{
				if (E.Topic == Topic && (!bAny || (int)E.How > (int)Out)) { Out = E.How; bAny = true; }
			}
			return bAny;
		}

		/// WHETHER THEY ARREST HIM for it: a statement that names him, about an arrestable offence.
		bool CanArrest(const std::string* Topic) const
		{
			if (Topic == nullptr || WasTaken(*Topic)) return false;
			for (const Entry& E : EntriesList) { if (E.Topic == *Topic && E.How == Known::Statement && Arrestable(E.Offence_)) return true; }
			return false;
		}

		std::string ToJson() const
		{
			std::string J = "{\"entries\":[";
			for (size_t I = 0; I < EntriesList.size(); ++I)
			{
				const Entry& E = EntriesList[I];
				J += (I ? ",{" : "{") + std::string("\"who\":") + PoliceJson::Str(E.Who) + ",\"topic\":" + PoliceJson::Str(E.Topic)
					+ ",\"offence\":\"" + OffenceName(E.Offence_) + "\",\"how\":\"" + KnownName(E.How) + "\",\"day\":" + std::to_string(E.Day) + "}";
			}
			J += "],\"visits\":[";
			for (size_t I = 0; I < VisitsList.size(); ++I) J += (I ? ",[" : "[") + std::to_string(VisitsList[I].first) + "," + PoliceJson::Str(VisitsList[I].second) + "]";
			J += "],\"calls\":[";
			for (size_t I = 0; I < CallsList.size(); ++I) J += (I ? ",[" : "[") + std::to_string(CallsList[I].first) + "," + PoliceJson::Str(CallsList[I].second) + "]";
			J += "],\"taken\":[";
			for (size_t I = 0; I < TakenList.size(); ++I) J += (I ? ",[" : "[") + PoliceJson::Str(TakenList[I].first) + "," + std::to_string(TakenList[I].second) + "]";
			return J + "]}";
		}

		/// From ToJson's text; what it cannot read it skips. Text that is no JSON
		/// object is the C#'s null save: an empty file.
		static PoliceFile FromJson(const std::string& SavedJson)
		{
			LedgerVignette::Value Root;
			std::string Err;
			if (!MiniJson::Deserialize(SavedJson, Root, Err) || Root.Type != LedgerVignette::T_OBJ) return PoliceFile();
			return FromValue(Root);
		}

		static PoliceFile FromValue(const LedgerVignette::Value& Root)
		{
			using LedgerVignette::Value;
			PoliceFile F;
			auto DayOf = [](const Value& V, int& Out) {
				if (V.Type != LedgerVignette::T_NUM || V.Num < 0 || V.Num >= 100000 || V.Num != std::floor(V.Num)) return false;
				Out = (int)V.Num;
				return true;
			};
			const Value* Es = PoliceJson::Last(Root, "entries");
			if (Es != nullptr && Es->Type == LedgerVignette::T_ARR)
				for (const Value& X : Es->Arr)
				{
					if (X.Type != LedgerVignette::T_OBJ) continue;
					std::string Who, Topic, Off, How;
					const bool bWho = PoliceJson::GetString(X, "who", Who), bTopic = PoliceJson::GetString(X, "topic", Topic);
					PoliceJson::GetString(X, "offence", Off);
					PoliceJson::GetString(X, "how", How);
					if (!bWho || Who.empty() || !bTopic || Topic.empty()) continue;
					Offence O;
					Known K;
					if (!OffenceFromName(Off, O) || !KnownFromName(How, K)) continue;
					const Value* Dv = PoliceJson::Last(X, "day");
					int Day;
					if (Dv == nullptr || !DayOf(*Dv, Day)) continue;
					bool bDup = false;
					for (const Entry& E : F.EntriesList) { if (E.Who == Who && E.Topic == Topic && (E.How == Known::Talk) == (K == Known::Talk)) bDup = true; }
					if (!bDup) F.EntriesList.push_back(Entry{ Who, Topic, O, K, Day });
				}
			const Value* Vs = PoliceJson::Last(Root, "visits");
			if (Vs != nullptr && Vs->Type == LedgerVignette::T_ARR)
				for (const Value& X : Vs->Arr)
				{
					int Day;
					if (X.Type != LedgerVignette::T_ARR || X.Arr.size() != 2 || !DayOf(X.Arr[0], Day) || X.Arr[1].Type != LedgerVignette::T_STR || !KnownWhy(X.Arr[1].Str)) continue;
					bool bDup = false;
					for (const auto& V : F.VisitsList) { if (V.second == X.Arr[1].Str) bDup = true; }
					if (!bDup) F.VisitsList.push_back(std::make_pair(Day, X.Arr[1].Str));
				}
			std::stable_sort(F.VisitsList.begin(), F.VisitsList.end(), [](const std::pair<int, std::string>& A, const std::pair<int, std::string>& B) { return A.first < B.first; });
			const Value* Cs = PoliceJson::Last(Root, "calls");
			if (Cs != nullptr && Cs->Type == LedgerVignette::T_ARR)
				for (const Value& X : Cs->Arr)
				{
					int Day;
					if (X.Type != LedgerVignette::T_ARR || X.Arr.size() != 2 || !DayOf(X.Arr[0], Day) || X.Arr[1].Type != LedgerVignette::T_STR) continue;
					const std::string& Topic = X.Arr[1].Str;
					bool bStatement = false, bCalled = false;
					for (const Entry& E : F.EntriesList) { if (E.Topic == Topic && E.Offence_ == Offence::Damage && E.How == Known::Statement && E.Day < Day) bStatement = true; }
					for (const auto& C : F.CallsList) { if (C.second == Topic) bCalled = true; }
					if (bStatement && !bCalled) F.CallsList.push_back(std::make_pair(Day, Topic));
				}
			std::stable_sort(F.CallsList.begin(), F.CallsList.end(), [](const std::pair<int, std::string>& A, const std::pair<int, std::string>& B) { return A.first < B.first; });
			const Value* Tk = PoliceJson::Last(Root, "taken");
			if (Tk != nullptr && Tk->Type == LedgerVignette::T_ARR)
				for (const Value& X : Tk->Arr)
				{
					if (X.Type != LedgerVignette::T_ARR || X.Arr.size() != 2 || X.Arr[0].Type != LedgerVignette::T_STR || X.Arr[1].Type != LedgerVignette::T_NUM) continue;
					const double Om = X.Arr[1].Num;
					if (Om < 0 || Om >= 1e8 || Om != std::floor(Om) || !F.CanArrest(&X.Arr[0].Str)) continue;
					F.TakenList.push_back(std::make_pair(X.Arr[0].Str, (long long)Om));
				}
			return F;
		}

	private:
		std::vector<Entry> EntriesList;
		std::vector<std::pair<int, std::string> > VisitsList;
		std::vector<std::pair<int, std::string> > CallsList;
		std::vector<std::pair<std::string, long long> > TakenList;

		static bool Detective(Offence O) { return (int)O >= (int)Offence::Wounding; }

		// Talk a person of his day world would pass on: his hidden life, heard
		// from somebody, at the share floor, not bought or hooked quiet.
		static std::vector<RumorPtr> TalkOf(const GossipMill& Mill, const Gossiper& A)
		{
			std::vector<RumorPtr> Out;
			if (A.Circle != "day") return Out;
			for (const RumorPtr& R : A.Rumors)
			{
				if (R && R->Content.Subject == "player" && R->Sensitive && R->Hops >= 1
				    && (R->Indelible || (R->Confidence >= Mill.MinConfidenceToShare && !A.Leashed && !A.SuppressedHas(R->TopicKey()))))
					Out.push_back(R);
			}
			return Out;
		}

		static bool KnownWhy(const std::string& Why)
		{
			if (Why == "talk" || Why == "body") return true;
			const std::string::size_type Sp = Why.find(' ');
			if (Sp == std::string::npos || Sp == 0) return false;
			Offence O;
			if (!OffenceFromName(Why.substr(0, Sp), O)) return false;
			const std::string Topic = Why.substr(Sp + 1);
			// topic.Trim() == topic, with .NET's whitespace: the ASCII six and the rest, over UTF-8.
			bool bTrimmed = !Topic.empty();
			if (bTrimmed)
			{
				MiniJson::FReader R(Topic);
				size_t Len = 1;
				if (MiniJson::FReader::IsWhiteSpace(R.CharAt(0, Len))) bTrimmed = false;
				// the last character: walk to it
				size_t At = 0, LastAt = 0;
				while (At < Topic.size()) { LastAt = At; size_t L = 1; R.CharAt(At, L); At += L; }
				size_t L2 = 1;
				if (MiniJson::FReader::IsWhiteSpace(R.CharAt(LastAt, L2))) bTrimmed = false;
			}
			return Detective(O) && bTrimmed && Topic.find(' ') == std::string::npos;
		}
	};
}
