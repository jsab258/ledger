// TRANSLITERATION of ledger/Assets/Scripts/Core/Arrangement.cs and
// TheLanding.cs, 30 September (the town's handover 6z, 6bn and 6cj, "the
// outfit's ask, Ron and the man at the landing";
// production/handovers/6z-the-ask.md).
//
// MICKEY'S ARRANGEMENT WITH THE OUTFIT: every other night from the first,
// Ron brings a coat and Mickey's envelope; he can take it to the man at the
// ferry landing after ten, tell Ron no (which ends it for good), or stay away
// (three such nights end it). Whatever he does is the outfit's talk, told first
// by the man at the landing; only the envelope handed over is a secret. Never
// a game over. The man at the landing has a few fixed lines, chosen by the
// arrangement's state (TheLanding).
//
// NOT HERE: SoundsLikeNo and ConfirmsNo, the reading of his line to Ron as a
// no, which the talk program does and the game only hears as "refusedAsk".
//
// TRANSLITERATION, NOT REWRITE, as Gossip.h states the method: the C#'s
// nullable GameTime is a pointer here (nullptr its null). Checked against
// PerceptionGolden's EmitAsks and EmitLanding rows (Ask, AskStory,
// AskRonRemembers, AskLoad, Landing) and, since the town's ten fixes of 30
// September, EmitPortReviewFixes' (FixAsk, AskSave, FixAskStory, FixLandingNo)
// and, since the review of 1 October (a night away passes at four, every
// story stamped when it is filed), LandingHours, in ue-probe/perception-golden.txt.
//
// NO UNREAL TYPE IS IN THIS FILE, as every file of the port.
#pragma once

#include "GameTime.h"
#include "Gossip.h"
#include "MemoryStore.h"
#include "MiniJson.h"

#include <cmath>
#include <map>
#include <set>
#include <string>
#include <vector>

namespace LedgerCore
{
	// The man at the landing is there from ten till one (TheLanding::There,
	// below): Answer asks it of the envelope.
	namespace TheLanding { inline bool There(const GameTime& Now); }

	/// What he did with one night's ask.
	enum class NightAnswer
	{
		Did,          // he handed the envelope over at the landing
		Refused,      // he told Ron no: the arrangement ends at once
		NoShow,       // he had the ask, said nothing and did not go
		Undelivered,  // Ron never reached him that night; nothing follows
	};

	class Arrangement
	{
	public:
		/// Nights between asks: 2, so the second falls on the third day.
		static constexpr int Every = 2;
		static constexpr double PatienceLossPerNoShow = 0.34;
		static constexpr double PatienceGainPerNight = 0.10;
		static constexpr const char* OutfitMan = "outfit_man";
		static constexpr const char* Doorman = "rocco";
		/// The hour of the morning after an ask night when the man at the landing gives up.
		static constexpr int GaveUpHour = 1;
		static constexpr const char* TopicPrefix = "player.outfit_d";
		/// The furthest day the arrangement walks to, as its save keeps it.
		static constexpr int LastDay = 100000;
		/// When Ron takes word down: eleven at night, or at once if later.
		static constexpr int RonGoesDownHour = 23;
		/// WeeksEnd.After (WeeksEnd.cs 44): the day from the first on which the
		/// week's end can wind Mickey's business down; WeeksEnd is not ported yet.
		static constexpr int WeeksEndAfter = 6;

		static constexpr const char* Terms = "I gave Mickey's nephew the envelope for the ferry landing: after ten tonight, to the man who asks for Mickey's. I told him that if he says no, Mickey's arrangement is finished.";
		static constexpr const char* HeardNo = "He told me no to the envelope, so I'm taking his answer down to the landing tonight: that's Mickey's arrangement finished.";
		static constexpr const char* HeardWoundDown = "He told Sheila he's winding Mickey's business down, so I'm taking word down to the landing: that's Mickey's arrangement finished.";
		static constexpr const char* SaidWoundDown = "Ron came down the landing to say Mickey's nephew is winding Mickey's business down: no more envelopes";
		static constexpr const char* HeardStopped = "Word came up from the landing: Mickey's nephew stayed away once too often, and Mickey's arrangement is finished. Nobody down there expects anything from him now.";

		explicit Arrangement(int InFirstDay = 0) : FirstDayValue(InFirstDay > 0 ? InFirstDay : 0) {}

		int FirstDay() const { return FirstDayValue; }
		bool Ended() const { return bEnded; }
		/// "refused", "stopped" or "wound down" once ended; empty (the C#'s null) before.
		const std::string& EndedWhy() const { return EndedWhyValue; }
		double Patience() const { return PatienceValue; }
		/// The nights answered, in order.
		const std::map<int, NightAnswer>& Nights() const { return NightsMap; }

		/// Wound down and Ron not yet down the landing with the word: when he
		/// goes (false: the C#'s null), and the night it answers (-1 otherwise).
		bool WoundWordAt(GameTime& Out) const { if (WoundTellNight < 0) return false; Out = WoundTellAt; return true; }
		int WoundNight() const { return WoundTellNight; }

		/// The night of the next ask, or -1 once the arrangement has ended.
		int NextNight() const { return bEnded ? -1 : FirstDayValue + Every * (int)NightsMap.size(); }
		bool AsksOn(int Day) const { return !bEnded && Day == NextNight(); }
		static GameTime GaveUpAt(int Day) { return GameTime(Day + 1, GaveUpHour, 0); }
		/// How long after he gives up a late no can still come: his yes to Ron's
		/// question counts for three game hours after it (the talk program's
		/// refusedAsk), and Ron asks only while the ask stands, before one.
		static constexpr int LateNoHours = 3;
		/// When a night he stayed away passes, as one: once no late no can come.
		static GameTime PassesAt(int Day) { return GaveUpAt(Day).AddMinutes(LateNoHours * 60); }
		/// The day whose night it is: until one in the morning, the day before's.
		static int NightOf(const GameTime& Now) { return Now.Hour < GaveUpHour ? Now.Day - 1 : Now.Day; }
		bool AskStands(const GameTime& Now) const { const int N = NightOf(Now); return AsksOn(N) && Delivered_.count(N) > 0; }
		static std::string TopicFor(int Day) { return std::string(TopicPrefix) + std::to_string(Day); }
		static bool IsNight(const RumorPtr& R)
		{
			const std::string P = TopicPrefix;
			return R && R->TopicKey().compare(0, P.size(), P) == 0;
		}

		static const char* Said(NightAnswer A)
		{
			return A == NightAnswer::Did ? "Mickey's nephew brought the envelope down the landing"
			     : A == NightAnswer::Refused ? "Ron came down the landing to say Mickey's nephew told them no"
			     : "Mickey's nephew never turned up at the landing";
		}
		static const char* Value(NightAnswer A)
		{
			return A == NightAnswer::Did ? "did" : A == NightAnswer::Refused ? "refused" : A == NightAnswer::NoShow ? "noshow" : "undelivered";
		}

		/// HE TOLD SHEILA HE IS WINDING IT DOWN (town list 6cc): the
		/// arrangement ends that night, as his no to Ron does. False, changing
		/// nothing, once it has ended.
		bool WoundDown(const GameTime& Now, GossipMill* Mill = nullptr)
		{
			if (bEnded) return false;
			PassedTo(NightOf(Now), Mill, Mill != nullptr ? &Now : nullptr);
			if (bEnded) return false;
			const int Day = NextNight();
			WoundDown_.insert(Day);
			Record(Day, NightAnswer::Refused, nullptr, nullptr);
			if (Mill != nullptr)
			{
				const GossiperPtr Ron = Mill->Get(Doorman);
				if (Ron && Ron->Memory) Ron->Memory->Append(MemoryEvent(Now, "observation", 0.8, HeardWoundDown));
			}
			const GameTime GoesDown(Now.Day, RonGoesDownHour, 0);
			WoundTellNight = Day;
			WoundTellAt = Now.Hour < GaveUpHour || Now.TotalMinutes() >= GoesDown.TotalMinutes() ? Now : GoesDown;
			TellWoundDown(Mill, &Now);
			return true;
		}

		/// RON REACHED HIM WITH TONIGHT'S ASK. With Ron and Now, Ron remembers
		/// the terms. False, changing nothing, unless the outfit asks tonight, he
		/// has not had it yet and, with Now, it is that night.
		bool Delivered(int Day, Gossiper* Ron = nullptr, const GameTime* Now = nullptr)
		{
			if (!AsksOn(Day) || (Now != nullptr && NightOf(*Now) != Day) || !Delivered_.insert(Day).second) return false;
			if (Ron != nullptr && Now != nullptr && Ron->Memory) Ron->Memory->Append(MemoryEvent(*Now, "observation", 0.8, Terms));
			return true;
		}
		bool WasDelivered(int Day) const { return Delivered_.count(Day) > 0; }

		/// AS EACH HOUR TURNS, before the rounds (Arrangement.cs TellDue, the
		/// review's B3): his no, or the winding down, reaches the landing when
		/// Ron goes down, not at dawn.
		/// AND A NIGHT HE STAYED AWAY, AS THE HOURS TURN (the independent review
		/// of 1 October, B3: still filed at dawn, stamped one): once no late no
		/// can still come (PassesAt, four: the builder's check of the port found
		/// a night passed at one lost his no confirmed at two past to Ron's
		/// question at two to one). Every story is stamped when it is filed,
		/// never before rounds that ran without it (the review's L4).
		void TellDue(GossipMill* Mill, const GameTime& Now) { PassedTo(Now.Day, Mill, &Now); }

		/// He answered this night's ask; see the C#. With a mill the night's
		/// story goes into the gossip, which needs Now (the C# throws without
		/// it; here the answer is refused). A no is answered as of when he said
		/// it, or as of Ron's question for a yes to it (Now), with ToldAt when
		/// he said it, which stamps what is told and remembered (nullptr: the
		/// C#'s null, Now stamps both).
		bool Answer(int Day, NightAnswer What, GossipMill* Mill = nullptr, const GameTime* Now = nullptr, const GameTime* ToldAt = nullptr)
		{
			if (Mill != nullptr && Now == nullptr) return false;
			if (What == NightAnswer::Undelivered || !AsksOn(Day)) return false;
			if (What == NightAnswer::NoShow && !Delivered_.count(Day)) return false;
			// A NO ONLY AFTER RON HAS BROUGHT THAT NIGHT'S ASK (the review's B4a).
			if (What == NightAnswer::Refused && Now != nullptr && !Delivered_.count(Day)) return false;
			if (What != NightAnswer::NoShow && Now != nullptr && Now->TotalMinutes() >= GaveUpAt(Day).TotalMinutes()) return false;
			// ONLY ON ITS OWN NIGHT (the port's independent check, 30 September:
			// an envelope two nights ahead could be done on the Monday, and a
			// night away filed before the landing opened): the envelope or the no
			// on that night, the night away once the man has given up waiting.
			if (Now != nullptr && What != NightAnswer::NoShow && NightOf(*Now) != Day) return false;
			// The envelope is handed over at the landing, while its man is there
			// (the independent check: done at nine that morning, he was filed as
			// seeing it at nine).
			if (Now != nullptr && What == NightAnswer::Did && !TheLanding::There(*Now)) return false;
			// A night away only once no late no can come (PassesAt; the independent check of 1 October).
			if (Now != nullptr && What == NightAnswer::NoShow && Now->TotalMinutes() < PassesAt(Day).TotalMinutes()) return false;
			Delivered_.insert(Day);
			// A PLAIN NO GOES DOWN WITH RON, as the wound-down word does (the
			// port's independent check): the man at the landing knows it only
			// when Ron has been down, at eleven or at once if later; Ron knows now.
			if (What == NightAnswer::Refused && Now != nullptr)
			{
				// Now is the night's "as of" (Ron's question, for a yes to it);
				// ToldAt, when he said it, stamps what is told and remembered (the
				// independent check of 1 October: one time for both put the story
				// before the rounds that ran without it).
				const GameTime Told = ToldAt != nullptr && ToldAt->TotalMinutes() > Now->TotalMinutes() ? *ToldAt : *Now;
				Record(Day, What, nullptr, Now);
				if (Mill != nullptr)
				{
					const GossiperPtr Ron = Mill->Get(Doorman);
					if (Ron && Ron->Memory) Ron->Memory->Append(MemoryEvent(Told, "observation", 0.8, HeardNo));
				}
				const GameTime GoesDown(Now->Day, RonGoesDownHour, 0);
				NoTellNight = Day;
				NoTellAt = Now->Hour < GaveUpHour || Now->TotalMinutes() >= GoesDown.TotalMinutes() ? *Now : GoesDown;
				TellWoundDown(Mill, &Told);
				return true;
			}
			return Record(Day, What, Mill, Now);
		}

		/// His no, not yet at the landing: when Ron takes it down (false: the
		/// C#'s null), and the night it answers (-1 when none waits).
		bool NoWordAt(GameTime& Out) const { if (NoTellNight < 0) return false; Out = NoTellAt; return true; }
		int NoNight() const { return NoTellNight; }

		/// The day is now Day: every ask night before it that nobody answered
		/// counts as one he stayed away if Ron had reached him with it (told
		/// when it is filed, at Now), and passes silently if not. With Now, a
		/// night does not pass until no late no can come (PassesAt).
		void PassedTo(int Day, GossipMill* Mill = nullptr, const GameTime* Now = nullptr)
		{
			if (Mill != nullptr && Now == nullptr) return;   // the C# throws
			TellWoundDown(Mill, Now);
			// NO FURTHER THAN A SAVE CAN HOLD (the port's independent check, 30
			// September: a far-future day was walked night by night, ten million
			// nights and a 244 MB save): the save keeps days under LastDay.
			if (Day > LastDay) Day = LastDay;
			while (!bEnded && NextNight() < Day && (Now == nullptr || PassesAt(NextNight()).TotalMinutes() <= Now->TotalMinutes()))
			{
				const int N = NextNight();
				// Stamped when it is filed (the review of 1 October, B3 and L4).
				if (Delivered_.count(N)) Record(N, NightAnswer::NoShow, Mill, Now);
				else Record(N, NightAnswer::Undelivered, nullptr, nullptr);
			}
		}

		/// {"first", "nights": [[day, answer]...], "delivered": [days], and
		/// "woundDown", "woundTell", "noTell" when there are any}, as MiniJson.Serialize
		/// writes the C#'s dictionary, in its order.
		std::string ToJson() const
		{
			std::string J = "{\"first\":" + std::to_string(FirstDayValue) + ",\"nights\":[";
			bool bFirst = true;
			for (const auto& Kv : NightsMap)
			{
				J += (bFirst ? "[" : ",[") + std::to_string(Kv.first) + ",\"" + Value(Kv.second) + "\"]";
				bFirst = false;
			}
			J += "],\"delivered\":[";
			bFirst = true;
			for (int D : Delivered_) { J += (bFirst ? "" : ",") + std::to_string(D); bFirst = false; }
			J += "]";
			if (!WoundDown_.empty())
			{
				J += ",\"woundDown\":[";
				bFirst = true;
				for (int D : WoundDown_) { J += (bFirst ? "" : ",") + std::to_string(D); bFirst = false; }
				J += "]";
			}
			if (WoundTellNight >= 0) J += ",\"woundTell\":[" + std::to_string(WoundTellNight) + "," + std::to_string(WoundTellAt.TotalMinutes()) + "]";
			if (NoTellNight >= 0) J += ",\"noTell\":[" + std::to_string(NoTellNight) + "," + std::to_string(NoTellAt.TotalMinutes()) + "]";
			return J + "}";
		}

		/// From ToJson's text, replayed in order through Answer: the first night
		/// play could not have reached, and all after it, is dropped. Text that
		/// is no JSON object is the C#'s null save.
		static Arrangement FromJson(const std::string& SavedJson)
		{
			LedgerVignette::Value Parsed;
			std::string Err;
			const bool bParsed = MiniJson::Deserialize(SavedJson, Parsed, Err) && Parsed.Type == LedgerVignette::T_OBJ;
			return FromValue(bParsed ? &Parsed : nullptr);
		}

		/// The same from a value already read; none, or no object, is the C#'s null save.
		static Arrangement FromValue(const LedgerVignette::Value* RootP)
		{
			const bool bRead = RootP != nullptr && RootP->Type == LedgerVignette::T_OBJ;
			static const LedgerVignette::Value Empty;
			const LedgerVignette::Value& Root = bRead ? *RootP : Empty;
			int First = 0;
			const LedgerVignette::Value* F = bRead ? Last(Root, "first") : nullptr;
			if (F != nullptr && F->Type == LedgerVignette::T_NUM && WholeIn(F->Num)) First = (int)F->Num;
			Arrangement A(First);
			if (!bRead) return A;
			std::set<int> Delivered;
			// A save from before the ask in talk (no "delivered") knew no night he never had.
			const LedgerVignette::Value* Dl = Last(Root, "delivered");
			const bool bBefore6bn = Dl == nullptr;
			if (Dl != nullptr && Dl->Type == LedgerVignette::T_ARR)
				for (const LedgerVignette::Value& X : Dl->Arr) if (X.Type == LedgerVignette::T_NUM && WholeIn(X.Num)) Delivered.insert((int)X.Num);
			std::set<int> Wound;
			const LedgerVignette::Value* Wl = Last(Root, "woundDown");
			if (Wl != nullptr && Wl->Type == LedgerVignette::T_ARR)
				for (const LedgerVignette::Value& X : Wl->Arr) if (X.Type == LedgerVignette::T_NUM && WholeIn(X.Num)) Wound.insert((int)X.Num);
			const LedgerVignette::Value* Ns = Last(Root, "nights");
			if (Ns != nullptr && Ns->Type == LedgerVignette::T_ARR)
				for (const LedgerVignette::Value& X : Ns->Arr)
				{
					if (X.Type != LedgerVignette::T_ARR || X.Arr.size() != 2 || X.Arr[0].Type != LedgerVignette::T_NUM
					    || X.Arr[1].Type != LedgerVignette::T_STR || X.Arr[0].Num != std::floor(X.Arr[0].Num)) break;
					const std::string& V = X.Arr[1].Str;
					NightAnswer Ans;
					if (V == "did") Ans = NightAnswer::Did;
					else if (V == "refused") Ans = NightAnswer::Refused;
					else if (V == "noshow") Ans = NightAnswer::NoShow;
					else if (V == "undelivered") Ans = NightAnswer::Undelivered;
					else break;
					// The C#'s (int)d; a day this far out is no night play reaches.
					if (!(std::fabs(X.Arr[0].Num) < 2147483647.0) || !A.AsksOn((int)X.Arr[0].Num)) break;
					const int Day = (int)X.Arr[0].Num;
					if (Ans == NightAnswer::Undelivered)
					{
						if (Delivered.count(Day)) break;
						A.Record(Day, NightAnswer::Undelivered, nullptr, nullptr);
						continue;
					}
					if (Ans == NightAnswer::NoShow && !Delivered.count(Day) && !bBefore6bn) break;
					if (Ans == NightAnswer::Refused && Wound.count(Day) && Day >= First + WeeksEndAfter)
					{
						// Delivered only if Ron had brought it before she closed the
						// book (the time-and-state sweep: brought at eight, wound down
						// at half past, a load forgot it had been).
						if (Delivered.count(Day)) A.Delivered_.insert(Day);
						A.WoundDown_.insert(Day);
						A.Record(Day, NightAnswer::Refused, nullptr, nullptr);
						continue;
					}
					if (!A.Answer(Day, Ans) && !(Ans == NightAnswer::NoShow && A.Delivered(Day) && A.Answer(Day, Ans))) break;
				}
			// Tonight's ask, had and not yet answered.
			if (!A.bEnded && Delivered.count(A.NextNight())) A.Delivered(A.NextNight());
			// A wound-down story the outfit's man has not had yet.
			const LedgerVignette::Value* Wt = Last(Root, "woundTell");
			if (Wt != nullptr && Wt->Type == LedgerVignette::T_ARR && Wt->Arr.size() == 2 && Wt->Arr[0].Type == LedgerVignette::T_NUM
			    && Wt->Arr[1].Type == LedgerVignette::T_NUM && std::fabs(Wt->Arr[0].Num) < 2147483647.0)
			{
				const double TnD = Wt->Arr[0].Num;
				const int Tn = (int)TnD;
				const double Tm = Wt->Arr[1].Num;
				// A whole night, and no later than play can make it: before one
				// (the time-and-state sweep: 6.5 was read as night 6, and one
				// o'clock itself was kept).
				if (TnD == std::floor(TnD) && TnD >= 0 && TnD < 100000
				    && A.WoundDown_.count(Tn) && Tm == std::floor(Tm)
				    && Tm >= (Tn - Every) * 24.0 * 60 && Tm < (Tn + 1) * 24.0 * 60 + GaveUpHour * 60)
				{
					A.WoundTellNight = Tn;
					A.WoundTellAt = GameTime::FromTotalMinutes((long long)Tm);
				}
			}
			// A plain no the outfit's man has not had yet: only for a night
			// answered no, not wound down, and taken down that night.
			const LedgerVignette::Value* Nt = Last(Root, "noTell");
			if (Nt != nullptr && Nt->Type == LedgerVignette::T_ARR && Nt->Arr.size() == 2 && Nt->Arr[0].Type == LedgerVignette::T_NUM
			    && Nt->Arr[1].Type == LedgerVignette::T_NUM)
			{
				const double Nn = Nt->Arr[0].Num;
				const double Nm = Nt->Arr[1].Num;
				if (Nn == std::floor(Nn) && Nn >= 0 && Nn < 100000)
				{
					// The C#'s `said`, renamed: Said is the class's own function.
					const std::map<int, NightAnswer>::const_iterator SaidThen = A.NightsMap.find((int)Nn);
					if (SaidThen != A.NightsMap.end() && SaidThen->second == NightAnswer::Refused
					    && !A.WoundDown_.count((int)Nn) && Nm == std::floor(Nm)
					    // Only when play could make it (the independent check): from Ron's
					    // hour that night until the man gives up waiting.
					    && Nm >= (int)Nn * 24.0 * 60 + RonGoesDownHour * 60 && Nm < ((int)Nn + 1) * 24.0 * 60 + GaveUpHour * 60)
					{
						A.NoTellNight = (int)Nn;
						A.NoTellAt = GameTime::FromTotalMinutes((long long)Nm);
					}
				}
			}
			return A;
		}

	private:
		int FirstDayValue;
		bool bEnded = false;
		std::string EndedWhyValue;
		double PatienceValue = 1.0;
		std::map<int, NightAnswer> NightsMap;
		std::set<int> Delivered_;
		std::set<int> WoundDown_;
		int WoundTellNight = -1;
		GameTime WoundTellAt;
		// A plain no waiting for Ron to take it down: the night and when he goes.
		int NoTellNight = -1;
		GameTime NoTellAt;

		static bool WholeIn(double D) { return D >= 0 && D < 100000 && D == std::floor(D); }

		/// A key given twice keeps its last value, as the C#'s dictionary does.
		static const LedgerVignette::Value* Last(const LedgerVignette::Value& Obj, const char* Key)
		{
			const LedgerVignette::Value* Out = nullptr;
			for (const auto& Kv : Obj.Obj) { if (Kv.first == Key) Out = &Kv.second; }
			return Out;
		}

		// The outfit's man has the wound-down story, or a plain no, once Ron has
		// been down (TellDue each hour; PassedTo at dawn; or later), stamped when
		// it is filed (the review of 1 October, B3 and L4).
		void TellWoundDown(GossipMill* Mill, const GameTime* Now)
		{
			if (Mill == nullptr || Now == nullptr) return;
			if (NoTellNight >= 0 && Now->TotalMinutes() >= NoTellAt.TotalMinutes())
			{
				Mill->Witness(OutfitMan, Fact("player", "outfit_d" + std::to_string(NoTellNight), Value(NightAnswer::Refused)), Said(NightAnswer::Refused), false, *Now, 1.0);
				NoTellNight = -1;
			}
			if (WoundTellNight < 0 || Now->TotalMinutes() < WoundTellAt.TotalMinutes()) return;
			Mill->Witness(OutfitMan, Fact("player", "outfit_d" + std::to_string(WoundTellNight), "wounddown"), SaidWoundDown, false, *Now, 1.0);
			WoundTellNight = -1;
		}

		bool Record(int Day, NightAnswer What, GossipMill* Mill, const GameTime* Now)
		{
			NightsMap[Day] = What;
			if (What == NightAnswer::Undelivered) return true;
			if (What == NightAnswer::Refused) { bEnded = true; EndedWhyValue = WoundDown_.count(Day) ? "wound down" : "refused"; }
			else if (What == NightAnswer::Did) PatienceValue = DotNetMin(1.0, PatienceValue + PatienceGainPerNight);
			else
			{
				PatienceValue = DotNetMax(0.0, PatienceValue - PatienceLossPerNoShow);
				if (PatienceValue <= 1e-9) { bEnded = true; EndedWhyValue = "stopped"; }
			}
			if (Mill != nullptr && Now != nullptr)
			{
				const bool bWound = WoundDown_.count(Day) > 0;
				Mill->Witness(OutfitMan, Fact("player", "outfit_d" + std::to_string(Day), Value(What)), bWound ? SaidWoundDown : Said(What),
				              What == NightAnswer::Did, *Now, 1.0);
				const GossiperPtr Ron = Mill->Get(Doorman);
				if (bEnded && Ron && Ron->Memory)
					Ron->Memory->Append(MemoryEvent(*Now, "observation", 0.8, bWound ? HeardWoundDown : What == NightAnswer::Refused ? HeardNo : HeardStopped));
			}
			return true;
		}
	};

	/// What happens with the man at the landing, as the game calls for his line.
	enum class LandingMoment { Comes, HandsOver, NothingToHand, TalksToHim };

	/// THE MAN AT THE LANDING (town list 6cj; TheLanding.cs): a few fixed
	/// lines, chosen by the arrangement's state. Plain text: no voice is cast
	/// for him without Jafar's yes.
	namespace TheLanding
	{
		/// He is at the landing from ten till one.
		static constexpr int From = 22;
		static constexpr const char* Asks = "Mickey's?";
		static constexpr const char* SameAgain = "Right. {0}, same again.";
		static constexpr const char* KeptWaiting = "You kept us waiting last time. Don't make a habit of it. {0}, same again.";
		static constexpr const char* NothingForMe = "Nothing for me? Then you've no business down here.";
		static constexpr const char* NotTonight = "Nothing tonight. {0}, after ten.";
		static constexpr const char* DoneRefused = "Ron's been down. We're done, you and us.";
		static constexpr const char* DoneStopped = "You had your chances. We're done, you and us.";
		static constexpr const char* DoneWound = "Winding it all up, Ron says. We're done, you and us.";
		static constexpr const char* DoneYourBit = "You've done your bit. Go home.";
		static constexpr const char* DoneGoOn = "We're done. Go on.";
		static const char* const BrushOff[3] = { "I've nothing to say to you.", "Not here. Go on.", "I don't do talking." };

		inline bool There(const GameTime& Now) { return Now.Hour >= From || Now.Hour < Arrangement::GaveUpHour; }

		/// GameTime.WeekdayName: day 0 a Monday.
		inline const char* WeekdayName(int Day)
		{
			static const char* const Names[7] = { "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday" };
			return Names[((Day % 7) + 7) % 7];
		}

		inline std::string When(int Next, int Night) { return Next == Night + 1 ? std::string("Tomorrow") : std::string(WeekdayName(Next)); }

		/// string.Format with the one {0}.
		inline std::string Format(const char* Text, const std::string& Arg)
		{
			std::string S = Text;
			const std::string::size_type At = S.find("{0}");
			if (At != std::string::npos) S.replace(At, 3, Arg);
			return S;
		}

		// The last ask night answered before this one was a night he stayed away.
		inline bool StayedAwayLast(const Arrangement& A, int Night)
		{
			NightAnswer LastAnswer = NightAnswer::Undelivered;
			for (const auto& Kv : A.Nights()) { if (Kv.first < Night && Kv.second != NightAnswer::Undelivered) LastAnswer = Kv.second; }
			return LastAnswer == NightAnswer::NoShow;
		}

		/// His line for this moment into Out, or false when he has nothing to
		/// say or is not there (the C#'s null).
		inline bool Line(const Arrangement* A, const GameTime& Now, LandingMoment M, int Seed, std::string& Out)
		{
			if (A == nullptr || !There(Now)) return false;
			const int Night = Arrangement::NightOf(Now);
			const std::map<int, NightAnswer>::const_iterator Tn = A->Nights().find(Night);
			const bool bDidTonight = Tn != A->Nights().end() && Tn->second == NightAnswer::Did;
			// Wound down, and Ron not yet down with the word: till then he waits
			// on Mickey's as ever.
			GameTime Word, NoWord;
			const bool bWoundNotHeard = A->Ended() && A->EndedWhy() == "wound down" && A->WoundWordAt(Word) && Now.TotalMinutes() < Word.TotalMinutes();
			// His plain no, the same: the man knows it once Ron has been down with
			// it (the independent check, 30 September: he said "Ron's been down"
			// while the no still waited for eleven).
			const bool bNoNotHeard = A->Ended() && A->EndedWhy() == "refused" && A->NoWordAt(NoWord) && Now.TotalMinutes() < NoWord.TotalMinutes();
			const bool bNotHeardYet = bWoundNotHeard || bNoNotHeard;
			const int WaitingNight = bWoundNotHeard ? A->WoundNight() : A->NoNight();
			if (M == LandingMoment::TalksToHim)
			{
				if (A->Ended() && !bNotHeardYet) { Out = DoneGoOn; return true; }
				if (bDidTonight) { Out = DoneYourBit; return true; }
				Out = BrushOff[((Seed % 3) + 3) % 3];
				return true;
			}
			if (bNotHeardYet)
			{
				if (Night == WaitingNight)
				{
					if (M == LandingMoment::Comes) { Out = Asks; return true; }
					if (M == LandingMoment::NothingToHand) { Out = NothingForMe; return true; }
					return false;
				}
				if (M == LandingMoment::Comes) { Out = Format(NotTonight, When(WaitingNight, Night)); return true; }
				return false;
			}
			if (A->Ended())
			{
				if (M != LandingMoment::Comes) return false;
				Out = A->EndedWhy() == "refused" ? DoneRefused : A->EndedWhy() == "wound down" ? DoneWound : DoneStopped;
				return true;
			}
			if (bDidTonight)
			{
				if (M != LandingMoment::HandsOver) return false;
				Out = Format(StayedAwayLast(*A, Night) ? KeptWaiting : SameAgain, When(A->NextNight(), Night));
				return true;
			}
			// Tonight's ask, unanswered, whether or not Ron reached him with it.
			if (A->AsksOn(Night))
			{
				if (M == LandingMoment::Comes) { Out = Asks; return true; }
				if (M == LandingMoment::NothingToHand) { Out = NothingForMe; return true; }
				return false;
			}
			// A night with no ask.
			if (M == LandingMoment::Comes) { Out = Format(NotTonight, When(A->NextNight(), Night)); return true; }
			return false;
		}
	}
}
