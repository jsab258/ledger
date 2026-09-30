// TRANSLITERATION of the Core part of ledger/Assets/Scripts/Core/PlayerIdentity.cs,
// 30 September (the town's handover 6ch, "what the town calls him";
// production/handovers/6ch-names.md): his name as the street's fact.
//
// When he gives his name to somebody (a talk reply's "gaveName"), they hold
// it first-hand as a plain street fact, once, and the town's rounds pass it
// on. It is news of him, not of anything done: it never enters anybody's
// manner (StreetVoice::RegardFor), is never voiced in an overheard exchange,
// and never keeps the arrival's line from being said (ArrivalLine). The
// ladder of what each person calls him runs in the talk program, not here.
//
// TRANSLITERATION, NOT REWRITE, as Gossip.h states the method. Checked
// against PerceptionGolden's EmitNames rows (NameStoryIs, NameTold,
// NameRegard, NameArrival) in ue-probe/perception-golden.txt.
//
// NO UNREAL TYPE IS IN THIS FILE, as every file of the port.
#pragma once

#include "GameTime.h"
#include "Gossip.h"

#include <string>

namespace LedgerCore
{
	namespace PlayerIdentity
	{
		static constexpr const char* NameTopic = "player.name";
		/// His surname, as the street says it (PlayerIdentity.Surname).
		static constexpr const char* Surname = "Nowak";

		inline bool IsNameStory(const RumorPtr& R) { return R && R->Content.Subject == "player" && R->TopicKey() == NameTopic; }

		/// HE TOLD `Who` HIS NAME at `At`: they hold it first-hand, once. False,
		/// changing nothing, for nobody in the mill or somebody who holds it
		/// first-hand already.
		inline bool NameTold(GossipMill* Mill, const std::string& Who, const GameTime& At)
		{
			if (Mill == nullptr || Who.empty()) return false;
			const GossiperPtr G = Mill->Get(Who);
			if (!G) return false;
			for (const RumorPtr& R : G->Rumors) { if (IsNameStory(R) && R->Hops == 0) return false; }
			Mill->Witness(Who, Fact("player", "name", Surname), std::string("Mickey's nephew is called ") + Surname, false, At, 1.0);
			return true;
		}

		/// Whether they hold the street's story of his name at all.
		inline bool HoldsHisName(const Gossiper* G)
		{
			if (G == nullptr) return false;
			for (const RumorPtr& R : G->Rumors) { if (IsNameStory(R)) return true; }
			return false;
		}
	}
}
