// THE 30 SEPTEMBER HIGH FAULTS, RUN AGAIN THROUGH THE PATH THE GAME TAKES NOW,
// and the new cases the fixes opened, in the C++ the game ships.
//
// Each block builds a small case out of the game's own headers and prints what
// they return. Where the game's step lives in CrimeProbe.cpp (Unreal-only), the
// block repeats that step's few lines and names them. What the game takes from
// Unreal (line traces, the body's exact place) is assumed and said so: every
// sightline here is open, and the people stand where the game's own
// OnlookersAt and BodySpotFor put them.
//
//   g++ -std=c++17 -O1 -w -I ue-probe/Source/LedgerProbe/Public \
//       -I ue-probe/tests/unreal-shim -o /tmp/recheck \
//       production/audits/review-2026-10-01/probes/recheck.cpp \
//       ue-probe/Source/LedgerProbe/Private/Perception.cpp
//   /tmp/recheck content/dialogue/crime-witness-v1.json production/specs/hook-cast.json
#include "CrimeProbe.h"
#include "PlayerIdentity.h"
#include "PoliceFile.h"
#include "TownWeek.h"

#include <cmath>
#include <cstdio>
#include <fstream>
#include <map>
#include <set>
#include <sstream>
#include <string>

using namespace LedgerCore;

static std::string ReadAll(const char* Path)
{
	std::ifstream In(Path);
	std::stringstream S; S << In.rdbuf();
	return S.str();
}

static std::shared_ptr<GossipMill> NewMill()
{
	return std::make_shared<GossipMill>(std::make_shared<SocialGraph>());
}

static GossiperPtr NewPerson(const std::string& Id, double Loyalty = 0.5)
{
	return std::make_shared<Gossiper>(Id, Id, std::make_shared<MemoryStore>(Id), std::make_shared<KnowledgeBase>(), "day", 0.5, 0.5, Loyalty);
}

static std::string Memories(const GossiperPtr& G)
{
	std::string S;
	if (!G || !G->Memory) return "(no memory store)";
	for (const MemoryEvent& E : G->Memory->Events) S += "\n      \"" + E.Text + "\"";
	return S.empty() ? std::string(" (none)") : S;
}

// Tom at Rita's glass, as the game's reach allows (kLiveReachM), facing it.
static const LedgerCrime::P3 kGlass(18.869, 1.6, 4.985);       // east_parade_glass2 (vignette-pieces.json)
static const LedgerCrime::P3 kTomHead(18.869, 1.75, 3.9);

// One onlooker's reading as MeasureOnlooker (CrimeProbe.cpp 5816-5853) takes it:
// feet where OnlookersAt puts them, heading StreetFacingYaw, light and
// familiarity as DeedOnlookers (5858-5897) sets them. Sightlines assumed open.
static LedgerCrime::Reading Onlooker(const LedgerCrime::OnlookerAt& O, double Light, double Familiarity)
{
	using namespace LedgerCrime;
	Reading R;
	R.WitnessId = O.Id;
	R.EventId = "A";
	R.SecondsWatching = kDeedSeconds;
	R.WitnessAt = P3(O.At.X, 0.08, O.At.Z);
	R.EyeAt = P3(O.At.X, 0.08 + kEyeHeightM, O.At.Z);
	R.WitnessYawDeg = O.YawDeg;
	R.ActorHeadAt = kTomHead;
	R.ActorYawDeg = 90.0;
	R.VictimAt = kGlass;
	R.ActorMetres = Metres(R.EyeAt, R.ActorHeadAt);
	R.ActorOffAxisDeg = OffAxisDeg(R.EyeAt, R.WitnessYawDeg, R.ActorHeadAt);
	R.VictimMetres = Metres(R.EyeAt, R.VictimAt);
	R.VictimOffAxisDeg = OffAxisDeg(R.EyeAt, R.WitnessYawDeg, R.VictimAt);
	R.Light = Light;
	R.Familiarity = Familiarity;
	Resolve(R, MakeDeed("crime_a", "player", "east_parade_glass2"));
	return R;
}

static const char* FilesName(LedgerCrime::WitnessFiles F)
{
	return F == LedgerCrime::WitnessFiles::NoiseOnly ? "the damage heard" : F == LedgerCrime::WitnessFiles::StoryAboutHim ? "a story about him" : "nothing";
}

// ---- A1 and A2 together: who stands where at the deed, and what each files --
static void OnlookerTable(const CastDay& Cast, const std::string& Bank, int Day, int Hour, const LedgerCrime::MeetingBook& Met, double LampReach)
{
	using namespace LedgerCrime;
	const bool bNight = NightAt(Hour);
	const double Light = LightOnHim(bNight, LampReach);
	std::printf("\n  D%d %02d:00, %s, light on him %.2f%s\n", Day, Hour, bNight ? "night" : "day", Light,
		bNight ? (LampReach > 0 ? " (a lamp reaches him)" : " (no lamp reaches him)") : "");
	const std::vector<OnlookerAt> All = OnlookersAt(Cast, Day, Hour, { "lena", "sam", "rocco" });
	if (All.empty()) std::printf("    nobody on Quay Street can see him\n");
	for (const OnlookerAt& O : All)
	{
		const Reading R = Onlooker(O, Light, FamiliarityFromMeetings(Met.DaysMet(O.Id)));
		std::string Id, Text, Clause, Speaker, Why;
		int Variants = 0;
		const bool bWords = R.bFiled && BankPick(Bank, "witness_summary", R.O.Rung, 1, Id, Text, Clause, Speaker, Variants, Why);
		const WitnessFiles F = R.bFiled ? WhatWitnessFiles(R.O.Rung, bWords) : WitnessFiles::Nothing;
		std::printf("    %-10s %-16s %s %5.1f m %4.0f deg off  rung %d  certainty %.2f  files %s%s%s\n",
			O.Id.c_str(), O.Place.c_str(), O.bBody ? "body  " : "window", R.ActorMetres, R.ActorOffAxisDeg, R.O.Rung, R.O.Certainty,
			FilesName(F), CanNameHim(R.O.Rung) ? ", names him" : "", O.Id == "lena" && R.bFiled && WitnessShouts(R.O.Rung) ? ", Sheila shouts" : "");
	}
}

static void ProveA1A2(const CastDay& Cast, const std::string& Bank)
{
	using namespace LedgerCrime;
	std::printf("\n[A1, A2, A4] Who sees Rita's window go, from where, in what light (OnlookersAt, LightOnHim, FamiliarityFromMeetings)\n");
	MeetingBook Nobody;
	MeetingBook Morning;   // the walk round with Sheila and a word with Darren before the deed
	Morning.Met("lena", 0); Morning.Met("sam", 0);
	OnlookerTable(Cast, Bank, 0, 12, Nobody, 0.0);
	OnlookerTable(Cast, Bank, 0, 16, Morning, 0.0);
	OnlookerTable(Cast, Bank, 0, 21, Morning, 0.0);
	OnlookerTable(Cast, Bank, 0, 21, Morning, 0.6);
	OnlookerTable(Cast, Bank, 1, 2, Morning, 0.0);

	// The game's rung-0 branch (CrimeProbe.cpp 2408-2425), for whoever only heard it.
	std::printf("\n  the rung-0 branch, as the game files it for Sheila:\n");
	auto Mill = NewMill();
	Mill->Add(NewPerson("lena"));
	const GossiperPtr G = Mill->Get("lena");
	const size_t Before = G->Memory->Events.size();
	Mill->Witness("lena", Fact(std::string(TownNews::Subject), std::string("rita_window"), std::string("heard")), "somebody put Rita's window in", false, GameTime(0, 12, 5), 0.9);
	G->Memory->KeepFirst((int)Before);
	G->Memory->Append(MemoryEvent(GameTime(0, 12, 5), "observation", 0.6, "I heard glass go over at Rita's. I never saw who did it."));
	bool bAboutHim = false, bDiag = false;
	for (const RumorPtr& R : G->Rumors) { if (R && R->Content.Subject == "player") bAboutHim = true; if (R && IsUnreadableSummary(R->Summary)) bDiag = true; }
	std::printf("    files a story about him: %s; a diagnostic's words anywhere: %s; shouts: %s\n    her memory:%s\n",
		bAboutHim ? "YES" : "no", bDiag ? "YES" : "no", WitnessShouts(0) ? "YES" : "no", Memories(G).c_str());
}

// ---- A3: the deed's story key in free play -----------------------------------
static void ProveA3()
{
	using namespace LedgerCrime;
	std::printf("\n[A3] Darren holds Rita's window (day 0) at rung 1; what the talk and keep-quiet see now (DeedKeyNow = player.window_d0)\n");
	auto Mill = NewMill();
	Mill->Add(NewPerson("sam"));
	Mill->Witness("sam", Fact("player", "window_d0", "ritas"), "a window went in and nobody saw more than a shape", true, GameTime(0, 11, 0), 0.46, false, 1);
	GossiperPtr Sam = Mill->Get("sam");
	const std::string Key = "player.window_d0";
	const std::string Deed = DeedJson(*Sam, Key, 0, 11, std::string());
	std::printf("  deed field sent to the talk: %s\n", Deed.empty() ? "(EMPTY)" : Deed.c_str());
	KeepQuiet(*Sam, Key);
	std::printf("  kept quiet suppresses player.window_d0: %s\n", Sam->SuppressedHas(Key) ? "yes" : "NO");
	RumorPtr Own = OwnedUpStory(Key, "sam", "ritas", "the new owner told me himself that he put Rita's window in");
	std::printf("  owning up files: %s = \"%s\", sensitive=%s\n", Own->TopicKey().c_str(), Own->Summary.c_str(), Own->Sensitive ? "yes" : "no");
}

// ---- A4: from a recognition to the constable --------------------------------
static void Week(const char* Title, const std::vector<std::pair<std::string, int> >& Saw, const CastDay& Cast, double Loyalty)
{
	std::printf("  %s\n", Title);
	auto Mill = NewMill();
	for (const auto& S : Saw) Mill->Add(NewPerson(S.first, Loyalty));
	TownWeek W;
	// As DeedFollows does after ResolveAndFile has filed each story (CrimeProbe.cpp 5448-5460).
	for (const auto& S : Saw) Mill->Witness(S.first, Fact("player", "window_d0", "ritas"), "seen", true, GameTime(0, 12, 5), 0.9, false, S.second);
	W.Deed(nullptr, GameTime(0, 12, 5), "ritas", "rita_window", "somebody put Rita's window in", Saw, "window_d0", std::string(), 1.0, true);
	for (int Day = 1; Day <= 3; ++Day)
	{
		const std::vector<std::string> Went = W.NineReports(Mill.get(), &Cast, GameTime(Day, 9, 0));
		for (const std::string& Who : Went)
		{
			std::string How = "?";
			for (const auto& E : W.Police.Entries()) { if (E.Who == Who) How = KnownName(E.How); }
			std::printf("    D%d 09:00 %s goes to the police (%s)\n", Day, Who.c_str(), How.c_str());
		}
		std::shared_ptr<Custody> C = W.TenConstable(Mill.get(), &Cast, GameTime(Day, 10, 0), "ritas");
		if (C) std::printf("    D%d 10:00 the constable takes him in: %s\n", Day, CustodyEndName(C->End()));
	}
	std::printf("    taken in: %s\n", W.TakenFirst.c_str());
}

static void ProveA4(const CastDay& Cast)
{
	using namespace LedgerCrime;
	std::printf("\n[A4] Can a witness in free play report him now?\n");
	int Best0 = 0, Best1 = 0;
	for (double M = 0.5; M <= 40.0; M += 0.5)
	{
		Best0 = std::max(Best0, Perception::IdRung(M, 1.0, FamiliarityFromMeetings(0), false, true));
		Best1 = std::max(Best1, Perception::IdRung(M, 1.0, FamiliarityFromMeetings(1), false, true));
	}
	std::printf("  best rung at any distance, full light, facing him: never met -> %d; met on one day -> %d\n", Best0, Best1);
	const std::string Topic = "player.window_d0";
	for (const char* Id : { "lena", "sam", "rocco", "rita" })
	{
		GossiperPtr P = NewPerson(Id);
		std::printf("  WouldReport(damage) for %-6s at the middle (0.5)%s: %s\n", Id, Cast.NeverToPolice(Id) ? ", never to police" : "",
			PoliceFile::WouldReport(P.get(), Offence::Damage, false, &Topic, Cast.NeverToPolice(Id)) ? "yes" : "no");
	}
	Week("Darren recognised him (rung 4):", { { "sam", 4 } }, Cast, 0.5);
	Week("Ron recognised him (rung 4):", { { "rocco", 4 } }, Cast, 0.5);
	Week("Rita's staff saw his face, never having met him (rung 3):", { { "ines", 3 }, { "marta", 3 } }, Cast, 0.5);
}

// ---- A5: a shape no longer marks its holder for DS Ellis ---------------------
static void ProveA5()
{
	std::printf("\n[A5] Does the rung matter to the police now?\n");
	for (int Rung : { 0, 1, 3, 4 })
	{
		auto Mill = NewMill();
		Mill->Add(NewPerson("lena"));
		Mill->Witness("lena", Fact("player", "window_d0", "ritas"), "seen", true, GameTime(0, 11, 0), 0.6, false, Rung);
		std::vector<std::string> Asked = PoliceFile::WhoSheAsks(Mill.get());
		std::printf("  a rung-%d story: names him %s; WhoSheAsks = [%s]\n", Rung, Mill->Get("lena")->Rumors[0]->NamesHim() ? "yes" : "no", Asked.empty() ? "" : Asked[0].c_str());
	}
}

// ---- B1: Sheila's week's-end question ----------------------------------------
static void ProveB1()
{
	std::printf("\n[B1] Sheila's week's-end question, as the game now asks it (AsksNow at the office, then Ask)\n");
	const GameTime Times[] = { GameTime(6, 10, 30), GameTime(6, 11, 59), GameTime(6, 12, 5), GameTime(6, 17, 0), GameTime(7, 10, 0), GameTime(8, 9, 0) };
	for (const GameTime& T : Times)
	{
		TownWeek W;
		const bool bAsks = W.Week.AsksNow(T, true) && W.Week.Ask(T, false, true);
		std::printf("  talking with her at the office at %s: she asks %s\n", T.ToString().c_str(), bAsks ? "yes" : "no");
	}
}

// ---- Who can ever see the deed, and who can ever know his face ----------------
static void WhoEver(const CastDay& Cast)
{
	using namespace LedgerCrime;
	std::printf("\n[NEW] Over days 0 to 6, every hour: who OnlookersAt ever lists, and who the game ever lets him meet\n");
	std::map<std::string, int> Hours;
	for (int D = 0; D <= 6; ++D)
		for (int H = 0; H < 24; ++H)
			for (const OnlookerAt& O : OnlookersAt(Cast, D, H, { "lena", "sam", "rocco" })) Hours[O.Id]++;
	std::string S;
	for (const auto& P : Hours) S += " " + P.first + "(" + std::to_string(P.second) + "h)";
	std::printf("  ever an onlooker:%s\n", S.c_str());
	std::printf("  Ada ever an onlooker: %s\n", Hours.count("ada") ? "yes" : "NO");
	// GMet.Met is called for: whoever he talks to (LiveAsk, CrimeProbe.cpp 4342), Ron at
	// the door (5504), Ada at her tea (5588), Sheila on the walk round (6937).
	const std::set<std::string> CanMeet = { "lena", "sam", "rocco", "ada" };
	std::string Both;
	for (const auto& P : Hours) if (CanMeet.count(P.first)) Both += " " + P.first;
	std::printf("  onlookers he can ever have met, so who can ever name him (rung 4):%s\n", Both.c_str());
}

// ---- NEW: a recognition names him "Nowak", whether or not his name is known ----
static void ProveNowak(const std::string& Bank)
{
	using namespace LedgerCrime;
	std::printf("\n[NEW] A rung-4 witness's words (the bank's three rung-4 clauses), now that rung 4 is reachable\n");
	for (int Seed = 0; Seed < 3; ++Seed)
	{
		std::string Id, Text, Clause, Speaker, Why;
		int Variants = 0;
		if (BankPick(Bank, "witness_summary", 4, Seed, Id, Text, Clause, Speaker, Variants, Why))
			std::printf("  %s: \"%s\" (says Nowak: %s)\n", Id.c_str(), Clause.c_str(), Clause.find("Nowak") != std::string::npos ? "YES" : "no");
	}
	// Darren met him (a word on day 0, no name given), saw him do it at 1.5 m,
	// and files the clause as the game does (ResolveAndFile, CrimeProbe.cpp 2441-2446).
	auto Graph = std::make_shared<SocialGraph>();
	Graph->Link("sam", "rocco", 0.9);
	auto Mill = std::make_shared<GossipMill>(Graph);
	Mill->Add(NewPerson("sam"));
	Mill->Add(NewPerson("rocco"));
	std::string Id, Text, Clause, Speaker, Why;
	int Variants = 0;
	BankPick(Bank, "witness_summary", 4, 0, Id, Text, Clause, Speaker, Variants, Why);
	Mill->Witness("sam", Fact("player", "window_d0", "ritas"), Clause, true, GameTime(0, 12, 5), 1.0, false, 4);
	for (int M = 6; M <= 60; M += 6) Mill->Tick(GameTime(0, 12, M));
	const GossiperPtr Ron = Mill->Get("rocco");
	bool bRonSays = false;
	for (const MemoryEvent& E : Ron->Memory->Events) if (E.Text.find("Nowak") != std::string::npos) bRonSays = true;
	std::printf("  Darren holds his name: %s; Ron holds his name: %s; Ron's memory after an hour of talk says Nowak: %s%s\n",
		PlayerIdentity::HoldsHisName(Mill->Get("sam").get()) ? "yes" : "no", PlayerIdentity::HoldsHisName(Ron.get()) ? "yes" : "no",
		bRonSays ? "YES" : "no", Memories(Ron).c_str());
}

int main(int Argc, char** Argv)
{
	const std::string Bank = ReadAll(Argc > 1 ? Argv[1] : "content/dialogue/crime-witness-v1.json");
	const std::string CastText = ReadAll(Argc > 2 ? Argv[2] : "production/specs/hook-cast.json");
	CastDay Cast;
	std::string Err;
	if (Bank.empty() || !CastDay::Parse(CastText, Cast, Err)) { std::printf("bank or cast not read: %s\n", Err.c_str()); return 2; }
	ProveA1A2(Cast, Bank);
	ProveA3();
	ProveA4(Cast);
	ProveA5();
	ProveB1();
	WhoEver(Cast);
	ProveNowak(Bank);
	return 0;
}
