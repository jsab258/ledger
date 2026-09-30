// TRANSLITERATION of ledger/Assets/Scripts/Core/DayOne.cs, 30 September
// (the town's handover 6cg, "day one"; production/handovers/6cg-day-one.md),
// with the one piece of PlayerIdentity.cs it reads (IsNameStory, town list
// 6ch; the rest of the name comes with its own rows).
//
// DAY ONE'S WORDS: Sheila's walk-round, stop by stop, in her own voice; its
// end, played or skipped, is the talk hint's moment (FirstMoments.h). And his
// arrival, the street's first story of him: first-hand for whoever is about
// Mickey's when he comes, and for Ada on her step, filed once; nobody's
// secret, never in anybody's manner, never voiced in an overheard exchange,
// said to his face once (StreetVoice::ArrivalLine).
//
// TRANSLITERATION, NOT REWRITE, as Gossip.h states the method. Checked
// against PerceptionGolden's EmitArrival rows (WalkRound, ArrivalSeen,
// RecognitionArrival, ArrivalLine) in ue-probe/perception-golden.txt.
//
// NO UNREAL TYPE IS IN THIS FILE, as every file of the port.
#pragma once

#include "CastDay.h"
#include "FirstMoments.h"
#include "Gossip.h"

#include <set>
#include <string>
#include <vector>

namespace LedgerCore
{
	namespace PlayerIdentity
	{
		static const char* const NameTopic = "player.name";
		inline bool IsNameStory(const RumorPtr& R) { return R && R->Content.Subject == "player" && R->TopicKey() == NameTopic; }
	}

	namespace DayOne
	{
		static const char* const Sheila = "lena";
		static const char* const Ada = "ada";
		/// His family on the street, who never greet him as a stranger: June,
		/// Mickey's daughter.
		inline const std::set<std::string>& Family() { static const std::set<std::string> F = { "june" }; return F; }

		struct Stop { const char* Name; const char* Line; };

		/// Sheila's walk-round, stop by stop, in order; her last line is the
		/// talk hint's own (FirstMoments, Moment::CanTalk).
		static const Stop WalkRound[] = {
			{ "door", "New management. Sheila Dunn, I keep the books. Come on, I'll show you round before you start looking lost." },
			{ "office", "Phone, radio, and the fare book. Every fare goes in the book. That was Mickey's rule, and it's mine now." },
			{ "drivers", "One driver by day, one by night, and the radio in between. The takings have been thin since the docks laid men off." },
			{ "mickeys-door", "That's Mickey's office. It's been locked since he died, and I've the key. Not today." },
			{ "flat", "Your flat's upstairs, over the office. His things are still in it. I didn't have the heart." },
		};
		static const int WalkRoundCount = (int)(sizeof(WalkRound) / sizeof(WalkRound[0]));

		/// The walk-round is over, played or skipped: the same state either
		/// way; the moment to talk has come, and its hint shows when the hints
		/// are next asked (FirstMoments::Due), never over another.
		inline bool WalkRoundEnds(FirstMoments* Hints, double At, Hint& Out)
		{
			return Hints != nullptr && Hints->Happened(Moment::CanTalk, At, Out);
		}

		/// His arrival's story: its topic, and how it is told.
		static const char* const ArrivalTopic = "player.arrived";
		static const char* const ArrivalSaid = "Mickey's nephew has come to take on the office";
		inline bool IsArrival(const RumorPtr& R) { return R && R->Content.Subject == "player" && R->TopicKey() == ArrivalTopic; }

		/// HE ARRIVES at `At`: whoever the cast has about Mickey's then, and Ada
		/// if she is on her step, hold it first-hand, once. Returns who.
		inline std::vector<std::string> Arrived(GossipMill* Mill, const CastDay* Cast, const GameTime& At, int FirstDay = 0)
		{
			std::vector<std::string> Saw;
			// Only on the game's first day, and once.
			if (Mill == nullptr || Cast == nullptr || At.Day != FirstDay) return Saw;
			for (const GossiperPtr& A : Mill->Agents())
			{
				if (!A) continue;
				for (const RumorPtr& R : A->Rumors) { if (IsArrival(R)) return Saw; }
			}
			const std::string Mickeys = Cast->AreaOf("mickeys_office");
			const Fact What("player", "arrived", "mickeys");
			for (const std::string& P : Cast->People())
			{
				// The C#'s null is empty here: a place not on the street has no area.
				const std::string Area = Cast->AreaOf(Cast->PlaceOf(P, At.Day, At.Hour));
				if (Area.empty() || !(Area == Mickeys || (P == Ada && Area == Cast->AreaOf("adas_step")))) continue;
				const GossiperPtr G = Mill->Get(P);
				if (!G) continue;
				bool bHeld = false;
				for (const RumorPtr& R : G->Rumors) { if (IsArrival(R) && R->Hops == 0) { bHeld = true; break; } }
				if (bHeld) continue;
				Mill->Witness(P, What, ArrivalSaid, false, At, 1.0);
				Saw.push_back(P);
			}
			return Saw;
		}
	}
}
