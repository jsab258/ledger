// Probe 3: the route's consequence in free play, with the game's own headers.
//  [E] the evidence the talk is sent (CrimeProbe.cpp 2730 reads "player.broke_a_window")
//  [R] the reports, the constable, keep-quiet and a threat (TownWeek, PoliceFile, Silence)
//  [B] what a rung-4 witness files from the bank
#include "CrimeProbe.h"
#include "TownWeek.h"
#include "Silence.h"
#include "Suspecting.h"
#include <cstdio>
#include <fstream>
#include <sstream>

using namespace LedgerCore;
static std::string ReadAll(const char* P) { std::ifstream In(P); std::stringstream S; S << In.rdbuf(); return S.str(); }

struct Town
{
	std::shared_ptr<SocialGraph> Graph = std::make_shared<SocialGraph>();
	std::unique_ptr<GossipMill> Mill;
	TownWeek W;
	Town(const CastDay& Cast)
	{
		for (const CastDay::Tie& T : Cast.Ties()) Graph->Link(T.A, T.B, T.W);
		Mill.reset(new GossipMill(Graph));
		for (const std::string& P : Cast.People())
			Mill->Add(std::make_shared<Gossiper>(P, P, std::make_shared<MemoryStore>(P), std::make_shared<KnowledgeBase>(), Cast.CircleOf(P)));
	}
	// As the game files it (CrimeProbe.cpp 2441-2450, then DeedFollows 5444-5460).
	void Deed(const CastDay& Cast, const GameTime& At, const std::vector<std::pair<std::string, int>>& Saw, double Certainty)
	{
		for (const auto& S : Saw)
			Mill->Witness(S.first, Fact("player", "window_d" + std::to_string(At.Day), "ritas"), "a clause", true, At, Certainty, false, S.second);
		std::vector<std::string> Heard;
		W.Deed(nullptr, At, "ritas", "rita_window", "somebody put Rita's window in", Saw, "window_d" + std::to_string(At.Day), std::string(), 1.0, true, &Heard);
		W.DamageTick(Mill.get(), &Cast, At);
	}
	// ConsequenceHour, in its order (CrimeProbe.cpp 5474-5515).
	void Hour(const CastDay& Cast, const GameTime& H)
	{
		W.RoundsTo(Mill.get(), &Cast, H.AddMinutes(-1));
		W.Six(Mill.get(), H);
		W.DamageTick(Mill.get(), &Cast, H);
		for (const auto& Who : W.NineReports(Mill.get(), &Cast, H)) std::printf("    %s: %s goes to the police\n", H.ToString().c_str(), Who.c_str());
		const std::string Why = W.NineEllis(Mill.get(), H, &Cast);
		if (!Why.empty()) std::printf("    %s: DS Ellis comes for %s\n", H.ToString().c_str(), Why.c_str());
		if (auto C = W.TenConstable(Mill.get(), &Cast, H, "ritas")) std::printf("    %s: a constable takes him (%s)\n", H.ToString().c_str(), C->Topic().c_str());
		W.HourEnd(Mill.get(), &Cast, H);
	}
	void RunTo(const CastDay& Cast, const GameTime& From, int Hours)
	{
		for (int I = 1; I <= Hours; ++I) Hour(Cast, GameTime::FromTotalMinutes(((From.TotalMinutes() / 60) + I) * 60));
	}
};

int main(int argc, char** argv)
{
	CastDay Cast; std::string Err;
	if (!CastDay::Parse(ReadAll(argv[1]), Cast, Err)) { std::printf("parse: %s\n", Err.c_str()); return 1; }
	const std::string Bank = ReadAll(argv[2]);

	std::printf("[F] familiarity from days met: 0:%.2f 1:%.2f 2:%.2f 3:%.2f 4:%.2f 6:%.2f\n",
		LedgerCrime::FamiliarityFromMeetings(0), LedgerCrime::FamiliarityFromMeetings(1), LedgerCrime::FamiliarityFromMeetings(2),
		LedgerCrime::FamiliarityFromMeetings(3), LedgerCrime::FamiliarityFromMeetings(4), LedgerCrime::FamiliarityFromMeetings(6));
	std::printf("    IdRung at 1.5 m, daylight, met once: %d; never met: %d\n",
		Perception::IdRung(1.5, 1.0, LedgerCrime::FamiliarityFromMeetings(1), false, true), Perception::IdRung(1.5, 1.0, 0.0, false, true));

	// [E] Darren (sam) recognised him at the deed (rung 4), Monday 10:30.
	{
		Town T(Cast);
		const GameTime At(0, 10, 30);
		T.Deed(Cast, At, { { "sam", 4 } }, 0.94);
		const GossiperPtr Darren = T.Mill->Get("sam");
		const DeedAccount Old = Suspecting::AccountOf(Darren.get(), "player.broke_a_window");     // what EvidenceFor asks (CrimeProbe.cpp 2730)
		const DeedAccount Right = Suspecting::AccountOf(Darren.get(), "player.window_d0");         // the key free play files
		Nearness Near; Near.SawHimMyself = false; Near.HeardHeWasNear = false; Near.OthersNear = 0;
		const auto D1 = Suspecting::Derive(Old, Near, 0.4);
		const auto D2 = Suspecting::Derive(Right, Near, 0.4);
		std::printf("\n[E] Darren holds player.window_d0 at rung 4, hop 0\n");
		std::printf("    AccountOf(\"player.broke_a_window\"): held=%d -> Derive %s %.2f\n", (int)Old.Held, SuspicionLevelName(D1.Level), D1.Value);
		std::printf("    AccountOf(\"player.window_d0\"):     held=%d rung=%d -> Derive %s %.2f (%s)\n", (int)Right.Held, Right.Rung, SuspicionLevelName(D2.Level), D2.Value, D2.Why.c_str());
		std::printf("    DeedJson(window_d0) = %s\n", LedgerCrime::DeedJson(*Darren, "player.window_d0", 0, 10, "ritas_step").c_str());
	}

	// [R1] the route as played: Darren saw at rung 4, Ines (ritas_counter) a face at rung 3, Rita a face at rung 3.
	std::printf("\n[R1] Mon 10:30: Darren rung 4, Ines rung 3, Rita rung 3; nothing said to anybody\n");
	{
		Town T(Cast);
		T.Deed(Cast, GameTime(0, 10, 30), { { "sam", 4 }, { "ines", 3 }, { "rita", 3 } }, 0.9);
		T.RunTo(Cast, GameTime(0, 10, 30), 60);
		for (const auto& E : T.W.Police.Entries()) std::printf("    file: %s %s how=%d day=%d\n", E.Who.c_str(), E.Topic.c_str(), (int)E.How, E.Day);
	}
	// [R2] the same, but he threatens Darren over it on Monday at 11:00 (the talk's "threatened").
	std::printf("\n[R2] the same; he threatens Darren over it at Mon 11:00 (Silence::FileThreat, as TakeClaimsFromReply does)\n");
	{
		Town T(Cast);
		T.Deed(Cast, GameTime(0, 10, 30), { { "sam", 4 } }, 0.9);
		const bool bFiled = Silence::FileThreat(T.Mill.get(), "sam", "player.window_d0", GameTime(0, 11, 0));
		const std::string Topic = "player.window_d0";
		std::printf("    threat filed=%d; WouldReport after it=%d\n", (int)bFiled, (int)PoliceFile::WouldReport(T.Mill->Get("sam").get(), Offence::Damage, false, &Topic));
		T.RunTo(Cast, GameTime(0, 10, 30), 60);
	}
	// [R3] the same, but Darren agrees to keep it quiet (the talk's keepsQuiet, CrimeProbe.cpp 4505).
	std::printf("\n[R3] the same; Darren keeps it quiet at Mon 11:00 (KeepQuiet with the deed field's topic)\n");
	{
		Town T(Cast);
		T.Deed(Cast, GameTime(0, 10, 30), { { "sam", 4 } }, 0.9);
		LedgerCrime::KeepQuiet(*T.Mill->Get("sam"), "player.window_d0");
		T.RunTo(Cast, GameTime(0, 10, 30), 60);
		std::printf("    (nothing above = no report, no constable)\n");
	}

	// [B] what a rung-4 witness files: the bank's clause.
	{
		std::string Id, Text, Clause, Speaker, Why; int Variants = 0;
		std::printf("\n[B] rung-4 clauses filed as the story's summary:\n");
		for (int Seed = 0; Seed < 3; ++Seed)
			if (LedgerCrime::BankPick(Bank, "witness_summary", 4, Seed, Id, Text, Clause, Speaker, Variants, Why)) std::printf("    %s: %s\n", Id.c_str(), Clause.c_str());
	}
	return 0;
}
