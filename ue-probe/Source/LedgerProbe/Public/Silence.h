// TRANSLITERATION of the street's side of ledger/Assets/Scripts/Core/Silence.cs,
// 30 September (the town's handover 6cd, "a threat to keep quiet"; Jafar ruled
// on the town's page that morning: a line about a deed is read for a threat by
// the checking model beside the reply, in the talk program).
//
// A THREAT, AS THE STREET'S STORY: the one he threatened holds it first-hand,
// not sensitive (nobody is ashamed to say they were threatened), under the
// deed it was about ("player.threat_window_d1"), once a person and deed; the
// street then says so to his face (StreetVoice::Recognition's two threat
// banks). And by Jafar's ruling of 1 October a threat talks them round: they
// keep the deed to themselves, a body excepted. Reading his words for a
// threat, and whether anybody keeps quiet, stay in the talk program: the port
// never reads what he said.
//
// TRANSLITERATION, NOT REWRITE, as Gossip.h states the method. Checked
// against PerceptionGolden's EmitThreats rows (ThreatIs, ThreatFiled,
// ThreatHeld, RecognitionThreat) and ThreatSilences in
// ue-probe/perception-golden.txt.
//
// NO UNREAL TYPE IS IN THIS FILE, as every file of the port.
#pragma once

#include "Gossip.h"

#include <string>

namespace LedgerCore
{
	namespace Silence
	{
		/// The street's story of it, and how it is told.
		static const char* const ThreatPrefix = "player.threat_";
		static const char* const ThreatSaid = "The new owner has been threatening people to keep them quiet";
		/// What the one he threatened remembers of it (Silence.cs ThreatMemory).
		static const char* const ThreatMemory = "The new owner threatened me to my face, to keep me quiet.";

		inline bool IsThreat(const RumorPtr& R)
		{
			const std::string P = ThreatPrefix;
			return R && R->Content.Subject == "player" && R->TopicKey().compare(0, P.size(), P) == 0;
		}

		/// THE THREAT, FILED (town list 6cd): the one he threatened holds it
		/// first-hand, under the deed it was about; once per deed and person;
		/// and it talks them round: the deed is suppressed for them (Jafar's
		/// ruling of 1 October). False when it could not be.
		inline bool FileThreat(GossipMill* Mill, const std::string& Who, const std::string& DeedTopic, const GameTime& At)
		{
			if (Mill == 0 || Who.empty() || DeedTopic.empty()) return false;
			GossiperPtr G = Mill->Get(Who);
			if (!G) return false;
			const std::string Player = "player.";
			const std::string Stem = DeedTopic.compare(0, Player.size(), Player) == 0 ? DeedTopic.substr(Player.size()) : DeedTopic;
			const Fact What("player", "threat_" + Stem, "threatened");
			for (const RumorPtr& R : G->Rumors)
			{
				// Filed once a deed and person; threatened again, the silence holds even
				// for a save from before Jafar's ruling of 1 October, which had none.
				if (R && R->TopicKey() == std::string(ThreatPrefix) + Stem && R->Hops == 0)
				{
					if (!G->SuppressedHas(DeedTopic)) G->Suppressed.push_back(DeedTopic);
					return false;
				}
			}
			// Threatened to their face: remembered as that, never "I saw it myself" (B7).
			Mill->WitnessRemembering(Who, What, ThreatSaid, false, At, ThreatMemory);
			// A THREAT TALKS THEM ROUND (Jafar's ruling of 1 October; the independent
			// review of 1 October, N3): frightened quiet about the deed, as one bought
			// is, so they go to nobody about it (PoliceFile::WouldReport); never about a
			// body, which is indelible and which no bribe or threat moves. The C#'s
			// HashSet: added once.
			if (!G->SuppressedHas(DeedTopic)) G->Suppressed.push_back(DeedTopic);
			return true;
		}
	}
}
