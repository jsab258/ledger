// Probe 1: who counts as an onlooker by routine, and who the damage's
// Aftermath says "was there when it happened", on the real cast file.
#include "CrimeProbe.h"
#include "TownWeek.h"
#include <cstdio>
#include <fstream>
#include <sstream>

using namespace LedgerCore;

static std::string ReadAll(const char* P) { std::ifstream In(P); std::stringstream S; S << In.rdbuf(); return S.str(); }

int main(int argc, char** argv)
{
	CastDay Cast; std::string Err;
	if (!CastDay::Parse(ReadAll(argv[1]), Cast, Err)) { std::printf("parse: %s\n", Err.c_str()); return 1; }
	const int Day = 0;   // Monday
	for (int Hour : { 11, 13, 17, 19, 20, 21 })
	{
		std::printf("\n== day %d %02d:00 (night=%d)\n", Day, Hour, (int)LedgerCrime::NightAt(Hour));
		for (const auto& O : LedgerCrime::OnlookersAt(Cast, Day, Hour, { "lena", "sam", "rocco" }))
			std::printf("  onlooker %-8s at %-16s body=%d spot=(%.1f,%.1f) yaw=%.0f\n", O.Id.c_str(), O.Place.c_str(), (int)O.bBody, O.At.X, O.At.Z, O.YawDeg);
		// people in Rita's area, and whether they count
		for (const std::string& P : Cast.People())
		{
			std::string Pl, Ar;
			if (!Cast.PlaceOf(P, Day, Hour, Pl) || !Cast.AreaOf(Pl, Ar) || Ar != "ritas") continue;
			bool bOn = false;
			for (const auto& O : LedgerCrime::OnlookersAt(Cast, Day, Hour, { "lena", "sam", "rocco" })) if (O.Id == P) bOn = true;
			std::printf("  in Rita's area: %-8s at %-14s onlooker=%d\n", P.c_str(), Pl.c_str(), (int)bOn);
		}
	}

	// The deed at 17:30 Monday: nobody filed a story (no body on Rita's step can see at night? it's day).
	// Aftermath as the game does it: DeedFollows passes Saw (story holders) and Heard (noise only).
	std::printf("\n== the deed at Mon 17:30, Rita's window; witnesses none, heard-only none\n");
	auto Graph = std::make_shared<SocialGraph>();
	GossipMill Mill(Graph);
	for (const std::string& P : Cast.People())
		Mill.Add(std::make_shared<Gossiper>(P, P, std::make_shared<MemoryStore>(P), std::make_shared<KnowledgeBase>(), Cast.CircleOf(P)));
	TownWeek W;
	const GameTime At(0, 17, 30);
	std::vector<std::pair<std::string, int>> Saw;
	std::vector<std::string> Heard;
	W.Deed(nullptr, At, "ritas", "rita_window", "somebody put Rita's window in", Saw, "window_d0", std::string(), 1.0, true, &Heard);
	for (const auto& F : W.DamageTick(&Mill, &Cast, At))
	{
		const GossiperPtr G = Mill.Get(F.first);
		std::printf("  %-8s at %s: \"%s\"\n", F.first.c_str(), F.second.ToString().c_str(), G->Memory->Events.back().Text.c_str());
	}

	// Rita heard it only (rung 0): she is left out of the damage, so her only memory is the game's
	// "I heard glass go over at Rita's" (CrimeProbe.cpp 2421).
	std::printf("\n== the deed at Mon 10:30; Rita heard it only (rung 0), Ines saw a face (rung 3)\n");
	GossipMill Mill2(Graph);
	for (const std::string& P : Cast.People())
		Mill2.Add(std::make_shared<Gossiper>(P, P, std::make_shared<MemoryStore>(P), std::make_shared<KnowledgeBase>(), Cast.CircleOf(P)));
	TownWeek W2;
	const GameTime At2(0, 10, 30);
	std::vector<std::pair<std::string, int>> Saw2 = { { "ines", 3 } };
	std::vector<std::string> Heard2 = { "rita" };
	W2.Deed(nullptr, At2, "ritas", "rita_window", "somebody put Rita's window in", Saw2, "window_d0", std::string(), 1.0, true, &Heard2);
	int RitaFound = 0;
	for (const auto& F : W2.DamageTick(&Mill2, &Cast, At2)) { if (F.first == "rita") ++RitaFound; std::printf("  found: %s\n", F.first.c_str()); }
	for (int H = 11; H <= 18; ++H) for (const auto& F : W2.DamageTick(&Mill2, &Cast, GameTime(0, H, 0))) { if (F.first == "rita") ++RitaFound; std::printf("  found: %s at %02d:00\n", F.first.c_str(), H); }
	std::printf("  rita found her own window via Aftermath: %d time(s); her memories: %zu\n", RitaFound, Mill2.Get("rita")->Memory->Events.size());
	return 0;
}
