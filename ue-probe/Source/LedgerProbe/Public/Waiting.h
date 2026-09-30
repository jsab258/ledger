// TRANSLITERATION of ledger/Assets/Scripts/Core/Waiting.cs, 30 September
// (the town's handover 6ci, "a way to wait, and the clock";
// production/handovers/6ci-the-wait.md), with Homicide.cs's
// Police.AsksAboutYou, which a wait's line reads.
//
// A WAIT THAT STOPS FOR WHAT THE TOWN HAS FOR HIM: to the Core a wait is
// skipped hours, and through the week's beats each would pass silently or
// turn against him (the night's ask never brought, Ada's tea a stand-up, the
// constable, DS Ellis and Sheila's Sunday question all while he was away).
// Next reads each piece's own state and says when a wait must end and why,
// or none when it may run on. Each beat's line stops a wait once, early
// enough for his walk there or at once. In the cells the wait runs to his
// release and nothing else stops it; during Sheila's walk-round there is no
// wait at all. Nothing is changed.
//
// TRANSLITERATION, NOT REWRITE, as Gossip.h states the method: the C#'s int?
// leads are WaitLead, its nullable pieces pointers. Checked against
// PerceptionGolden's EmitWaits rows (Wait) in ue-probe/perception-golden.txt.
//
// NO UNREAL TYPE IS IN THIS FILE, as every file of the port.
#pragma once

#include "Arrangement.h"
#include "CastDay.h"
#include "FirstWeek.h"
#include "GameTime.h"
#include "Gossip.h"
#include "PoliceFile.h"
#include "WeeksEnd.h"

#include <algorithm>
#include <memory>
#include <set>
#include <string>
#include <vector>

namespace LedgerCore
{
	namespace Police
	{
		/// Homicide.cs 462: she asks about the player by name.
		inline bool AsksAboutYou(Inquiry I) { return (int)I >= (int)Inquiry::Investigation; }
	}

	/// Where a wait must end, and why, in plain words for the player.
	struct WaitStop
	{
		GameTime At;
		/// "ron", "landing", "tea", "constable", "ellis", "sheila", "sheila_answer" or "released".
		std::string Why;
		std::string Line;
		/// The day it is for: for Ron and the landing, the ask's night.
		int ForDay = 0;
		/// What the game adds to WaitBeats.Shown once it has shown the line.
		std::string Key;

		WaitStop() {}
		WaitStop(const GameTime& InAt, const std::string& InWhy, const std::string& InLine, int InForDay, const std::string* InKey = nullptr)
			: At(InAt), Why(InWhy), Line(InLine), ForDay(InForDay), Key(InKey != nullptr ? *InKey : InWhy + "@" + std::to_string(InForDay)) {}
	};

	/// The C#'s int?: unset, or a number of game minutes (the port builds as
	/// C++14, which has no std::optional).
	struct WaitLead
	{
		bool bSet = false;
		int Minutes = 0;
		WaitLead& operator=(int M) { bSet = true; Minutes = M; return *this; }
	};

	/// What the game has running, for a wait to read (any may be none).
	struct WaitBeats
	{
		const Arrangement* Asks = nullptr;
		const AdasTea* Tea = nullptr;
		const PoliceFile* Police = nullptr;
		const GossipMill* Mill = nullptr;
		Inquiry InquiryOf = Inquiry::None;
		const WeeksEnd* Week = nullptr;
		const Custody* CustodyOf = nullptr;
		/// Sheila's walk-round is over.
		bool WalkRoundDone = true;
		/// He is waiting in Ada's house, where the minutes count as his tea.
		bool AtAdas = false;
		/// The lines the game has shown him (each stop's Key); it keeps them in its save.
		std::set<std::string> Shown;
		/// His walk, in game minutes, to Ada's, to the landing and to the office.
		WaitLead TeaLead, LandingLead, OfficeLead;
	};

	namespace Waiting
	{
		static constexpr int RonComesHour = 20;
		static constexpr int LandingFrom = 22;
		static constexpr int EllisHour = 9, ConstableHour = 10;
		static constexpr int AnswerBy = WeeksEnd::StayUntil;
		static constexpr int AnswerTime = 30;
		static constexpr int MaxLead = 180, DaysAhead = 14;

		static constexpr const char* WalkRoundLine = "Sheila's still showing you round.";
		static constexpr const char* RonLine = "Ron's at the door with something for you.";
		static constexpr const char* LandingLine = "They'll be expecting the envelope at the landing after ten.";
		static constexpr const char* TeaLine = "Ada's pot goes on at nine.";
		static constexpr const char* ConstableLine = "There's a constable asking for you.";
		static constexpr const char* EllisLine = "DS Ellis is on Quay Street, asking after you.";
		static constexpr const char* EllisBodyLine = "DS Ellis is on Quay Street.";
		static constexpr const char* SheilaLine = "Sheila's waiting for you in the office this morning, on her day off.";
		static constexpr const char* SheilaAnswerLine = "Sheila wants your answer before the day's out.";
		static constexpr const char* ReleasedLine = "They're letting you go.";

		inline GameTime At(int Day, int Hour) { return GameTime(Day, Hour, 0); }
		inline int Cmp(const GameTime& A, const GameTime& B) { return A.TotalMinutes() < B.TotalMinutes() ? -1 : A.TotalMinutes() > B.TotalMinutes() ? 1 : 0; }

		/// WHETHER NO WAIT MAY START AT ALL, and why (into Out): during Sheila's walk-round.
		inline bool Refused(const WaitBeats* B, std::string& Out)
		{
			if (B != nullptr && !B->WalkRoundDone) { Out = WalkRoundLine; return true; }
			return false;
		}

		/// The game has shown him this stop's line.
		inline void Showed(WaitBeats* B, const WaitStop* S) { if (B != nullptr && S != nullptr) B->Shown.insert(S->Key); }

		inline std::vector<WaitStop> Stops(const GameTime& Now, const GameTime& Until, const WaitBeats* B, int LeadMinutes)
		{
			std::vector<WaitStop> Found;
			std::string Why;
			if (B == nullptr || Cmp(Until, Now) <= 0) return Found;
			if (Refused(B, Why)) return Found;
			const std::set<std::string>& Shown = B->Shown;
			// In the cells: to his release, that minute included, and nothing else.
			const Custody* Held = B->CustodyOf;
			const std::string ReleasedKey = Held == nullptr ? std::string() : "released@" + std::to_string(Held->OutAt().TotalMinutes());
			if (Held != nullptr && Cmp(Now, Held->TakenAt()) >= 0 && Cmp(Now, Held->OutAt()) <= 0 && !Shown.count(ReleasedKey))
			{
				if (Cmp(Held->OutAt(), Until) <= 0) Found.push_back(WaitStop(Held->OutAt(), "released", ReleasedLine, Held->OutAt().Day, &ReleasedKey));
				return Found;
			}
			auto Lead = [LeadMinutes](const WaitLead& L) { return std::max(0, std::min((int)MaxLead, L.bSet ? L.Minutes : LeadMinutes)); };

			// A beat at `At0`, its line of use until `Last`, that minute included:
			// once, `Lead0` before it or at once; in time order, the first offered first on a tie.
			auto Beat = [&](const std::string& BeatWhy, int ForDay, const GameTime& At0, const GameTime& Last, int Lead0, const char* Line)
			{
				if (Shown.count(BeatWhy + "@" + std::to_string(ForDay)) || Cmp(Now, Last) > 0) return;
				GameTime T = At0.AddMinutes(-Lead0);
				if (Cmp(T, Now) < 0) T = Now;
				if (Cmp(T, Until) > 0) return;
				size_t I = Found.size();
				while (I > 0 && Cmp(T, Found[I - 1].At) < 0) --I;
				Found.insert(Found.begin() + I, WaitStop(T, BeatWhy, Line, ForDay));
			};

			const Arrangement* Asks = B->Asks;
			if (Asks != nullptr && !Asks->Ended() && Asks->NextNight() >= 0)
			{
				int N = Asks->NextNight();
				// A night past one in the morning, unanswered, counts at dawn: the
				// next is two nights on, unless that night away ends it.
				if (Cmp(Now, Arrangement::GaveUpAt(N)) >= 0)
					N = Asks->WasDelivered(N) && Asks->Patience() - Arrangement::PatienceLossPerNoShow <= 1e-9 ? -1 : N + Arrangement::Every;
				if (N >= 0)
				{
					const GameTime LastMinute = Arrangement::GaveUpAt(N).AddMinutes(-1);
					if (!Asks->WasDelivered(N)) Beat("ron", N, At(N, RonComesHour), LastMinute, 0, RonLine);
					else Beat("landing", N, At(N, LandingFrom), LastMinute, Lead(B->LandingLead), LandingLine);
				}
			}

			const AdasTea* Tea = B->Tea;
			// Not once he has been with her.
			if (Tea != nullptr && Tea->State() == TeaState::Asked && !B->AtAdas && Tea->LatestMinute() < 0)
				Beat("tea", Tea->Day(), At(Tea->Day(), AdasTea::From), At(Tea->Day(), AdasTea::Until).AddMinutes(-1), Lead(B->TeaLead), TeaLine);

			const PoliceFile* Police = B->Police;
			const int LastDay = std::min(Until.Day, Now.Day + DaysAhead);
			if (Police != nullptr)
			{
				for (int D = std::max(0, Now.Day); D <= LastDay; ++D)
				{
					const GameTime T = At(D, ConstableHour);
					std::string Topic;
					if (Cmp(T.AddMinutes(60), Now) > 0 && Police->ConstableWouldCome(D, Topic)) { Beat("constable", D, T, T.AddMinutes(59), 0, ConstableLine); break; }
				}
				for (int D = std::max(0, Now.Day); D <= LastDay; ++D)
				{
					const GameTime T = At(D, EllisHour);
					if (Cmp(T.AddMinutes(60), Now) <= 0) continue;
					const std::vector<std::string> Whys = Police->EllisWouldComeAll(B->Mill, D, B->InquiryOf);
					if (!Whys.empty())
					{
						// About him if any of the day's reasons is, or the inquiry asks about him.
						bool bAboutHim = Police::AsksAboutYou(B->InquiryOf);
						for (const std::string& W : Whys) { if (W != "body") bAboutHim = true; }
						Beat("ellis", D, T, T.AddMinutes(59), 0, bAboutHim ? EllisLine : EllisBodyLine);
						break;
					}
				}
			}

			const WeeksEnd* Week = B->Week;
			if (Week != nullptr && !Week->Answered())
			{
				GameTime Asked;
				const bool bAsked = Week->AskedAt(Asked);
				if (!bAsked && CastDay::Weekday(Week->Day()) == 6)
					Beat("sheila", Week->Day(), At(Week->Day(), WeeksEnd::WaitFrom), At(Week->Day(), WeeksEnd::WaitUntil).AddMinutes(-1), Lead(B->OfficeLead), SheilaLine);
				else if (bAsked && Week->Stands(Now))
				{
					// With her by half past five, less his walk, since she goes home at six.
					const GameTime By = At(Asked.Day, AnswerBy).AddMinutes(-AnswerTime);
					Beat("sheila_answer", Asked.Day, By, At(Asked.Day, AnswerBy).AddMinutes(-1), Lead(B->OfficeLead), SheilaAnswerLine);
				}
			}
			return Found;
		}

		/// Where a wait from Now towards Until must end (into Out), or false when it may run to Until.
		inline bool Next(const GameTime& Now, const GameTime& Until, const WaitBeats* B, WaitStop& Out, int LeadMinutes = 0)
		{
			const std::vector<WaitStop> All = Stops(Now, Until, B, LeadMinutes);
			if (All.empty()) return false;
			Out = All[0];
			return true;
		}

		/// EVERY KNOWN STOP from Now to Until, earliest first, for a "wait until" choice.
		inline std::vector<WaitStop> Ahead(const GameTime& Now, const GameTime& Until, const WaitBeats* B, int LeadMinutes = 0)
		{
			return Stops(Now, Until, B, LeadMinutes);
		}
	}
}
