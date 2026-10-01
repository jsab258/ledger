// Probe 4: Darren's regard after he recognised Tom at the deed. RegardTick
// (CrimeProbe.cpp 5086-5089) passes Darren a fixed 0.20; DeedOnlookers passed
// FamiliarityFromMeetings (0.4 after one meeting) to recognise him at the deed.
#include "CrimeProbe.h"
#include "StreetVoice.h"
#include <cstdio>

using namespace LedgerCore;

int main()
{
	auto Graph = std::make_shared<SocialGraph>();
	GossipMill Mill(Graph);
	Mill.Add(std::make_shared<Gossiper>("sam", "Darren", std::make_shared<MemoryStore>("sam"), std::make_shared<KnowledgeBase>(), "day"));
	// What ResolveAndFile files for a rung-4 reading (CrimeProbe.cpp 2441-2450).
	Mill.Witness("sam", Fact("player", "window_d0", "ritas"), "it was Nowak that put the window in on Quay Street", true, GameTime(0, 10, 30), 1.0, false, 4);
	const GossiperPtr D = Mill.Get("sam");
	for (double Fam : { LedgerCrime::kLadFamiliarity, LedgerCrime::FamiliarityFromMeetings(1) })
	{
		const StreetVoice::Regard R = StreetVoice::RegardFor(D.get(), Mill.MinConfidenceToShare, false, nullptr, Fam, false);
		std::printf("familiarity %.2f: knowsItIsHim=%d knowing=%s stance=%s -> KnowingJson sends %s\n", Fam, (int)R.bKnowsItIsHim,
			StreetVoice::KnowingName(R.HowMuch), StreetVoice::StanceName(R.Stance),
			(!R.bKnowsItIsHim || R.HowMuch == StreetVoice::Knowing::Nothing || !R.Story) ? "{\"level\":\"nothing\"}" : "the story");
	}
	std::printf("his memory: %s\n", D->Memory->Events.back().Text.c_str());
	return 0;
}
