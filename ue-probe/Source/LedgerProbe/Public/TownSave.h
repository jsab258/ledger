// TRANSLITERATION of ledger/Assets/Scripts/Core/TownSave.cs, 30 September
// (the town's one save, town list 6bl; production/handovers/README.md).
//
// ONE SAVE FOR THE TOWN'S PIECES: the hints shown, the outfit's asks, Ada's
// tea, the police file, what he has heard, the town's news filed, each deed's
// damage, each arrest, the hours the town has talked, and Sheila's week's end
// travel together, one object each way with a version: every piece restored
// from what it can read and made fresh where it cannot, so one forgotten
// piece can never be a reload where the town forgets it.
//
// TRANSLITERATION, NOT REWRITE, as Gossip.h states the method: the C#'s
// SaveIncompatibleException for a later version is a false return with its
// words. Checked against PerceptionGolden's EmitTownSave rows (TownSaveWritten,
// TownSaveBack, TownSaveSame, TownSaveLaterRefused, TownSaveJunk).
//
// NO UNREAL TYPE IS IN THIS FILE, as every file of the port.
#pragma once

#include "Arrangement.h"
#include "FirstMoments.h"
#include "FirstWeek.h"
#include "MemoryStore.h"
#include "MiniJson.h"
#include "PoliceFile.h"
#include "StreetVoice.h"
#include "TownNews.h"
#include "TownRounds.h"
#include "WeeksEnd.h"

#include <algorithm>
#include <memory>
#include <string>
#include <vector>

namespace LedgerCore
{
	class TownSave
	{
	public:
		/// The bundle's version: a file from a later one is refused.
		static constexpr int Version = 1;

		FirstMoments Hints;
		Arrangement Asks = Arrangement(0);
		std::unique_ptr<AdasTea> Tea;
		PoliceFile Police;
		StreetVoice::RemarkLedger Heard;
		std::vector<std::string> NewsFiled;
		std::vector<Aftermath> Damage;
		std::vector<std::shared_ptr<Custody> > Arrests;
		TownHours Hours;
		WeeksEnd Week;

		std::string ToJson() const
		{
			std::string J = "{\"version\":" + std::to_string(Version) + ",\"hints\":" + Hints.ToJson() + ",\"asks\":" + Asks.ToJson()
				+ ",\"police\":" + Police.ToJson() + ",\"heard\":" + Heard.ToJson() + ",\"news\":[";
			for (size_t I = 0; I < NewsFiled.size(); ++I) J += (I ? "," : "") + PoliceJson::Str(NewsFiled[I]);
			J += "]";
			if (Tea) J += ",\"tea\":" + Tea->ToJson();
			J += ",\"damage\":[";
			for (size_t I = 0; I < Damage.size(); ++I) J += (I ? "," : "") + Damage[I].ToJson();
			J += "],\"arrests\":[";
			for (size_t I = 0; I < Arrests.size(); ++I) J += (I ? "," : "") + Arrests[I]->ToJson();
			return J + "],\"hours\":" + Hours.ToJson() + ",\"week\":" + Week.ToJson() + "}";
		}

		/// From ToJson's text: each piece from what it can read, fresh where it
		/// cannot. False, with why, for a version later than this build's.
		static bool FromJson(const std::string& Json, TownSave& Out, std::string& Err)
		{
			LedgerVignette::Value Root;
			std::string JErr;
			const bool bRead = MiniJson::Deserialize(Json, Root, JErr) && Root.Type == LedgerVignette::T_OBJ;
			return FromValue(bRead ? &Root : nullptr, Out, Err);
		}

		static bool FromValue(const LedgerVignette::Value* RootP, TownSave& T, std::string& Err)
		{
			using LedgerVignette::Value;
			T = TownSave();
			if (RootP == nullptr || RootP->Type != LedgerVignette::T_OBJ) return true;
			const Value& Root = *RootP;
			const Value* V = PoliceJson::Last(Root, "version");
			if (V != nullptr && V->Type == LedgerVignette::T_NUM && V->Num > Version)
			{
				Err = "the town's save is version " + ShortestRoundTrip(V->Num) + ", this build reads " + std::to_string(Version);
				return false;
			}
			auto Obj = [&Root](const char* K) -> const Value* {
				const Value* X = PoliceJson::Last(Root, K);
				return X != nullptr && X->Type == LedgerVignette::T_OBJ ? X : nullptr;
			};
			T.Hints = FirstMoments::FromValue(Obj("hints"));
			T.Asks = Arrangement::FromValue(Obj("asks"));
			T.Tea = AdasTea::FromValue(Obj("tea"));
			const Value* P = Obj("police");
			T.Police = P != nullptr ? PoliceFile::FromValue(*P) : PoliceFile();
			T.Heard = StreetVoice::RemarkLedger::FromValue(Obj("heard"));
			const Value* N = PoliceJson::Last(Root, "news");
			if (N != nullptr && N->Type == LedgerVignette::T_ARR)
				for (const Value& X : N->Arr)
				{
					if (X.Type == LedgerVignette::T_STR && !X.Str.empty() && std::find(T.NewsFiled.begin(), T.NewsFiled.end(), X.Str) == T.NewsFiled.end())
						T.NewsFiled.push_back(X.Str);
				}
			const Value* Dm = PoliceJson::Last(Root, "damage");
			if (Dm != nullptr && Dm->Type == LedgerVignette::T_ARR)
				for (const Value& X : Dm->Arr)
				{
					Aftermath A;
					if (X.Type != LedgerVignette::T_OBJ || !Aftermath::FromValue(X, A)) continue;
					bool bHave = false;
					for (const Aftermath& O : T.Damage) { if (O.Key() == A.Key()) bHave = true; }
					if (!bHave) T.Damage.push_back(A);
				}
			// Each deed he was taken in for (the police file says which), once,
			// the earliest of any given twice, in the order taken.
			std::vector<std::shared_ptr<Custody> > Taken;
			const Value* Ar = PoliceJson::Last(Root, "arrests");
			if (Ar != nullptr && Ar->Type == LedgerVignette::T_ARR)
				for (const Value& X : Ar->Arr)
				{
					if (X.Type != LedgerVignette::T_OBJ) continue;
					const std::shared_ptr<Custody> C = Custody::FromValue(X);
					if (C && T.Police.WasTaken(C->Topic())) Taken.push_back(C);
				}
			std::stable_sort(Taken.begin(), Taken.end(), [](const std::shared_ptr<Custody>& A, const std::shared_ptr<Custody>& B) {
				if (A->TakenAt().TotalMinutes() != B->TakenAt().TotalMinutes()) return A->TakenAt().TotalMinutes() < B->TakenAt().TotalMinutes();
				return A->Topic() < B->Topic();   // string.CompareOrdinal on the ASCII ids
			});
			for (const std::shared_ptr<Custody>& C : Taken)
			{
				bool bHave = false;
				for (const std::shared_ptr<Custody>& O : T.Arrests) { if (O->Topic() == C->Topic()) bHave = true; }
				if (!bHave) T.Arrests.push_back(C);
			}
			T.Hours = TownHours::FromValue(Obj("hours"));
			T.Week = WeeksEnd::FromValue(Obj("week"));
			return true;
		}
	};
}
