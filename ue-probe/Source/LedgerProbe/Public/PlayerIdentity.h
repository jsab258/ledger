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
			// TOLD, NOT SEEN, AND THEIRS FIRST-HAND (the port's independent check,
			// 30 September): through the mill's sighting, somebody who had heard
			// his name at full certainty was never made first-hand, kept the
			// teller as its source, was "told" again every time, and remembered
			// "I saw it myself". The story is made theirs here, in place when they
			// already hold it second-hand.
			const Fact What("player", "name", Surname);
			const std::string Said = std::string("Mickey's nephew is called ") + Surname;
			RumorPtr Held;
			for (const RumorPtr& R : G->Rumors) { if (IsNameStory(R) && (!Held || R->Confidence > Held->Confidence)) Held = R; }
			if (!Held)
			{
				RumorPtr R = std::make_shared<Rumor>(What);
				R->OriginId = Who; R->Summary = Said; R->Confidence = 1.0; R->Hops = 0; R->Sensitive = false;
				G->Rumors.push_back(R);
			}
			else
			{
				Held->Content = What;
				Held->OriginId = Who;
				Held->Summary = Said;
				Held->Confidence = 1.0;
				Held->Hops = 0;
				Held->Sensitive = false;
			}
			if (G->Knowledge) G->Knowledge->Learn(What);
			if (G->Memory) G->Memory->Append(MemoryEvent(At, "observation", 0.6, "He told me himself: " + Said));
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
