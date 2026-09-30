// TRANSLITERATION of ledger/Assets/Scripts/Core/FirstWeek.cs, 30 September
// (the town's handover 6bg, "Ada's tea"; production/handovers/6bg-adas-tea.md).
//
// ADA'S TEA, THE FIRST HOUR'S DAY-3 SCENE: on the evening of the outfit's
// second ask she asks him in for tea (the pot on at nine). To count as having
// come he is there by half past nine and sits with her through half past ten,
// never away more than ten minutes between. Going down to the landing for the
// ask that night while she sits at her window, he is seen going. What it
// leaves is her regard for him (Loyalty): stayed, it rises; stood up, it
// falls. Never the game.
//
// TRANSLITERATION, NOT REWRITE, as Gossip.h states the method. Checked
// against PerceptionGolden's EmitTea rows (Tea, TeaAsked, TeaBefore11,
// TeaClosed, TeaSeenGoing, TeaSeenGoingOnce, TeaSave) in
// ue-probe/perception-golden.txt.
//
// NO UNREAL TYPE IS IN THIS FILE, as every file of the port.
#pragma once

#include "Arrangement.h"
#include "GameTime.h"
#include "Gossip.h"
#include "MemoryStore.h"
#include "MiniJson.h"

#include <cmath>
#include <memory>
#include <set>
#include <string>

namespace LedgerCore
{
	/// How Ada's tea went.
	enum class TeaState { NotAsked, Asked, Stayed, LeftEarly, StoodUp };

	inline const char* TeaStateName(TeaState S)
	{
		switch (S)
		{
		case TeaState::NotAsked: return "NotAsked";
		case TeaState::Asked: return "Asked";
		case TeaState::Stayed: return "Stayed";
		case TeaState::LeftEarly: return "LeftEarly";
		default: return "StoodUp";
		}
	}

	class AdasTea
	{
	public:
		static constexpr const char* Ada = "ada";
		/// The evening: the pot on at nine; the evening closes at eleven.
		static constexpr int From = 21, Until = 23;
		static constexpr int ArriveByMinute = 21 * 60 + 30, StayUntilMinute = 22 * 60 + 30, LongestAway = 10;
		static constexpr double StayedGain = 0.25, LeftEarlyGain = 0.05, StoodUpCost = 0.15;
		static constexpr const char* Invite = "There'll be a pot on at nine tonight, if you want it. I don't ask twice, mind.";

		int Day() const { return DayValue; }
		TeaState State() const { return StateValue; }
		/// The minutes of the evening (from midnight) he was with her.
		const std::set<int>& Minutes() const { return MinutesSet; }
		int LatestMinute() const { return MinutesSet.empty() ? -1 : *MinutesSet.rbegin(); }
		bool SeenGoing() const { return bSeenGoing; }

		/// THE TEA FOR THIS RUN: on the night of the outfit's second ask, for a
		/// man who has met her by then; none (nullptr) for one who has not.
		static std::unique_ptr<AdasTea> For(int FirstAskDay, bool bMetAdaByThen)
		{
			if (!bMetAdaByThen || FirstAskDay < 0) return nullptr;
			std::unique_ptr<AdasTea> T(new AdasTea());
			T->DayValue = FirstAskDay + Arrangement::Every;
			return T;
		}

		/// She sees him on the tea's day before nine and asks him, once: her
		/// line into Out, or false when it is not the moment.
		bool SheSeesHim(const GameTime& Now, std::string& Out)
		{
			if (StateValue != TeaState::NotAsked || Now.Day != DayValue || Now.Hour >= From) return false;
			StateValue = TeaState::Asked;
			Out = Invite;
			return true;
		}

		/// He is in her house at this minute: counted between nine and eleven
		/// on the tea's day, once she has asked.
		void WithHer(const GameTime& Now)
		{
			if (StateValue != TeaState::Asked || Now.Day != DayValue || Now.Hour < From || Now.Hour >= Until) return;
			MinutesSet.insert(Now.Hour * 60 + Now.Minute);
		}

		/// The evening closes (eleven, or any later call): how it went, and
		/// what it leaves with her.
		TeaState Close(Gossiper* AdaG, const GameTime& Now)
		{
			if (StateValue != TeaState::Asked) return StateValue;
			// Not before the evening is over (the time-and-state sweep: closed on
			// an earlier day, the tea was a stand-up before it was poured).
			if (Now.Day < DayValue || (Now.Day == DayValue && Now.Hour < Until)) return StateValue;
			StateValue = Judge();
			if (AdaG != nullptr)
			{
				if (StateValue == TeaState::Stayed)
				{
					AdaG->Loyalty = DotNetMin(1.0, AdaG->Loyalty + StayedGain);
					AdaG->Suspicion.Lower(0.1, "Mickey's nephew sat with me over a pot of tea");
					if (AdaG->Memory) AdaG->Memory->Append(MemoryEvent(Now, "conversation", 0.7,
						"Mickey's nephew came for his tea and sat with me till gone half ten. There's more to him than they're saying."));
				}
				else if (StateValue == TeaState::LeftEarly)
				{
					AdaG->Loyalty = DotNetMin(1.0, AdaG->Loyalty + LeftEarlyGain);
					if (AdaG->Memory) AdaG->Memory->Append(MemoryEvent(Now, "conversation", 0.6,
						"Mickey's nephew came for his tea and was off again before the pot was cold. Somewhere to be, had he."));
				}
				else
				{
					AdaG->Loyalty = DotNetMax(0.0, AdaG->Loyalty - StoodUpCost);
					if (AdaG->Memory) AdaG->Memory->Append(MemoryEvent(Now, "observation", 0.65,
						"I asked Mickey's nephew in for his tea. He never came. I'll not ask again."));
				}
			}
			return StateValue;
		}

		/// He went down to the landing for the outfit's ask on the tea's night,
		/// having been asked in: she saw him go from her window, once.
		void WentToTheLanding(GossipMill* Mill, const GameTime& Now, bool bForTheAsk)
		{
			if (bSeenGoing || Mill == nullptr || !bForTheAsk || StateValue == TeaState::NotAsked) return;
			const bool bThatNight = (Now.Day == DayValue && Now.Hour >= From) || (Now.Day == DayValue + 1 && Now.Hour < 1);
			// Nobody sees him go when Ada is not in the mill (the port's
			// independent check, 30 September: he was marked seen, and nobody
			// held it).
			if (!bThatNight || !Mill->Get(Ada)) return;
			bSeenGoing = true;
			Mill->Witness(Ada, Fact("player", "left_tea_for_landing_d" + std::to_string(DayValue), "seen"),
			              "Mickey's nephew went off down towards the ferry, late, the night I'd asked him in for his tea", true, Now, 1.0, false, 4);
		}

		/// {"day", "state", "minutes", "seenGoing"}, as MiniJson.Serialize writes the C#'s.
		std::string ToJson() const
		{
			std::string J = "{\"day\":" + std::to_string(DayValue) + ",\"state\":\"" + TeaStateName(StateValue) + "\",\"minutes\":[";
			bool bFirst = true;
			for (int M : MinutesSet) { J += (bFirst ? "" : ",") + std::to_string(M); bFirst = false; }
			return J + "],\"seenGoing\":" + (bSeenGoing ? "true" : "false") + "}";
		}

		/// From ToJson's text; none when there is no readable day, and what it
		/// cannot read it skips. Text that is no JSON object is no save.
		static std::unique_ptr<AdasTea> FromJson(const std::string& SavedJson)
		{
			LedgerVignette::Value Parsed;
			std::string Err;
			if (!MiniJson::Deserialize(SavedJson, Parsed, Err) || Parsed.Type != LedgerVignette::T_OBJ) return nullptr;
			return FromValue(&Parsed);
		}

		/// The same from a value already read; none, or no object, is none.
		static std::unique_ptr<AdasTea> FromValue(const LedgerVignette::Value* RootP)
		{
			if (RootP == nullptr || RootP->Type != LedgerVignette::T_OBJ) return nullptr;
			const LedgerVignette::Value& Root = *RootP;
			const LedgerVignette::Value* D = Last(Root, "day");
			if (D == nullptr || D->Type != LedgerVignette::T_NUM || !(D->Num >= 0 && D->Num < 100000 && D->Num == std::floor(D->Num))) return nullptr;
			std::unique_ptr<AdasTea> T(new AdasTea());
			T->DayValue = (int)D->Num;
			const LedgerVignette::Value* S = Last(Root, "state");
			if (S != nullptr && S->Type == LedgerVignette::T_STR)
			{
				for (int I = 0; I <= (int)TeaState::StoodUp; ++I) { if (S->Str == TeaStateName((TeaState)I)) { T->StateValue = (TeaState)I; break; } }
			}
			// Minutes only once asked, and only the evening's.
			const LedgerVignette::Value* Ms = Last(Root, "minutes");
			if (T->StateValue != TeaState::NotAsked && Ms != nullptr && Ms->Type == LedgerVignette::T_ARR)
			{
				for (const LedgerVignette::Value& X : Ms->Arr)
				{
					if (X.Type == LedgerVignette::T_NUM && X.Num >= From * 60 && X.Num < Until * 60 && X.Num == std::floor(X.Num)) T->MinutesSet.insert((int)X.Num);
				}
			}
			// A closed evening is what its minutes say, whatever the file says.
			if (T->StateValue == TeaState::Stayed || T->StateValue == TeaState::LeftEarly || T->StateValue == TeaState::StoodUp) T->StateValue = T->Judge();
			const LedgerVignette::Value* Sg = Last(Root, "seenGoing");
			if (Sg != nullptr && Sg->Type == LedgerVignette::T_BOOL) T->bSeenGoing = Sg->Bool && T->StateValue != TeaState::NotAsked;
			return T;
		}

	private:
		int DayValue = 0;
		TeaState StateValue = TeaState::NotAsked;
		std::set<int> MinutesSet;
		bool bSeenGoing = false;

		AdasTea() {}

		// How the evening went, from the minutes alone.
		TeaState Judge() const
		{
			if (MinutesSet.empty()) return TeaState::StoodUp;
			if (*MinutesSet.begin() > ArriveByMinute || *MinutesSet.rbegin() < StayUntilMinute) return TeaState::LeftEarly;
			int LastM = -1;
			for (int M : MinutesSet)
			{
				// The minutes away are those between two he was there: stamps
				// eleven apart are ten away, which is allowed (the port's
				// independent check, 30 September).
				if (LastM >= 0 && M - LastM - 1 > LongestAway) return TeaState::LeftEarly;
				LastM = M;
			}
			return TeaState::Stayed;
		}

		/// A key given twice keeps its last value, as the C#'s dictionary does.
		static const LedgerVignette::Value* Last(const LedgerVignette::Value& Obj, const char* Key)
		{
			const LedgerVignette::Value* Out = nullptr;
			for (const auto& Kv : Obj.Obj) { if (Kv.first == Key) Out = &Kv.second; }
			return Out;
		}
	};
}
