// PROOFS FOR THE REVIEW'S HIGH FAULTS, in the C++ the game ships.
//
// Each block builds the smallest case from FAULTS.md out of the game's own
// headers and prints what they return. Nothing here edits the game; the
// numbers the game would take from Unreal (positions, headings, line traces)
// are the ruling's fixed positions and the street file's window, and each
// block says which of them it assumed.
//
//   g++ -std=c++11 -O1 -w -I ue-probe/Source/LedgerProbe/Public \
//       -I ue-probe/tests/unreal-shim -o /tmp/high-faults \
//       production/audits/review-2026-09-30/probes/high-faults.cpp \
//       ue-probe/Source/LedgerProbe/Private/Perception.cpp
//   /tmp/high-faults content/dialogue/crime-witness-v1.json
#include "CrimeProbe.h"
#include "PoliceFile.h"
#include "TownWeek.h"

#include <cmath>
#include <cstdio>
#include <fstream>
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
	auto Graph = std::make_shared<SocialGraph>();
	auto Mill = std::make_shared<GossipMill>(Graph);
	return Mill;
}

static GossiperPtr NewPerson(const std::string& Id, double Loyalty = 0.5)
{
	return std::make_shared<Gossiper>(Id, Id, std::shared_ptr<MemoryStore>(), std::shared_ptr<KnowledgeBase>(), "day", 0.5, 0.5, Loyalty);
}

static std::string LastMemory(const GossiperPtr& G)
{
	if (!G || !G->Memory || G->Memory->Events.empty()) return "(none)";
	return G->Memory->Events.back().Text;
}

// ---- A1: Sheila, facing Mickey's window, and Rita's window broken --------
static void ProveA1(const std::string& Bank, bool bVictimOccluded)
{
	using namespace LedgerCrime;
	std::printf("\n[A1] Sheila's stand-in and Rita's window (line to the glass %s)\n", bVictimOccluded ? "BLOCKED" : "open");
	Reading R;
	R.WitnessId = "lena";
	R.EventId = "A";
	R.SecondsWatching = 5.0;   // accrued on the walk before the deed (assumed; the game never resets it)
	R.WitnessAt = P3(kW1AX, 0.08, kW1AZ);
	R.EyeAt = P3(kW1AX, 0.08 + kEyeHeightM, kW1AZ);
	// FaceBody turns her to crime A, Mickey's window (CrimeProbe.cpp 2172).
	R.WitnessYawDeg = std::atan2(kCrimeAZ - kW1AZ, kCrimeAX - kW1AX) * 180.0 / 3.14159265358979;
	// Tom within reach of Rita's glass (kLiveReachM 2.2 m): on the footway in front of it.
	const P3 Glass(18.869, 1.6, 4.985);           // production/specs/vignette-pieces.json, east_parade_glass2
	R.ActorHeadAt = P3(18.869, 1.75, 3.9);
	R.ActorYawDeg = 90.0;                          // facing the window
	R.VictimAt = Glass;
	R.ActorMetres = Metres(R.EyeAt, R.ActorHeadAt);
	R.ActorOffAxisDeg = OffAxisDeg(R.EyeAt, R.WitnessYawDeg, R.ActorHeadAt);
	R.VictimMetres = Metres(R.EyeAt, R.VictimAt);
	R.VictimOffAxisDeg = OffAxisDeg(R.EyeAt, R.WitnessYawDeg, R.VictimAt);
	R.bActorOccluded = false;                      // a trace in Unreal; assumed open
	R.bVictimOccluded = bVictimOccluded;
	const Deed D = MakeDeed("crime_a", "player", "east_parade_glass2");
	Resolve(R, D);
	std::printf("  her heading %.1f deg; to Tom %.2f m at %.1f deg off axis; to the glass %.2f m at %.1f deg\n",
		R.WitnessYawDeg, R.ActorMetres, R.ActorOffAxisDeg, R.VictimMetres, R.VictimOffAxisDeg);
	std::printf("  observation: filed=%s rung=%d certainty=%.2f\n", R.bFiled ? "yes" : "no", R.O.Rung, R.O.Certainty);
	if (!R.bFiled) { std::printf("  => nothing filed in this variant\n"); return; }
	// The game's ResolveAndFile, 2326-2358: the summary starts as the sentinel
	// and is replaced only when the bank has a line for the rung reached.
	std::string Id, Text, Clause, Speaker, Why;
	int Variants = 0;
	std::string Summary = std::string(UnreadableSummaryPrefix()) + "none";   // GOverheard.WhyNot before a pick
	const bool bPicked = BankPick(Bank, "witness_summary", R.O.Rung, Seed(GameTime(0, 11, 0)), Id, Text, Clause, Speaker, Variants, Why);
	std::printf("  bank line for rung %d: %s (%s)\n", R.O.Rung, bPicked ? "found" : "NONE", bPicked ? Id.c_str() : Why.c_str());
	if (bPicked) { std::string W; Summary = SummaryToFile(Id, Clause, W); }
	auto Mill = NewMill();
	Mill->Add(NewPerson("lena"));
	Mill->Witness("lena", Fact("player", "window_d0", "ritas"), Summary, true, GameTime(0, 11, 0), R.O.Certainty, false, R.O.Rung);
	std::printf("  filed summary: \"%s\"\n", Summary.c_str());
	std::printf("  her memory now: \"%s\"\n", LastMemory(Mill->Get("lena")).c_str());
	std::printf("  => %s\n", IsUnreadableSummary(Summary) ? "PROVED: the town is handed the diagnostic string as her account" : "not reproduced");
}

// ---- A2: the light every witness reading uses ------------------------------
static void ProveA2()
{
	using namespace LedgerCrime;
	std::printf("\n[A2] The light a witness reading is judged in\n");
	Reading R;
	R.WitnessId = "sam";
	R.ActorMetres = 12.0; R.ActorOffAxisDeg = 0.0;
	R.VictimMetres = 12.0; R.VictimOffAxisDeg = 0.0;
	const Vantage V = VantageOf(R);
	std::printf("  VantageOf gives light %.2f to the actor and %.2f to the window, whatever the hour (kLightLevel)\n",
		V.ToActor.LightLevel, V.ToVictim.LightLevel);
	for (double Light : { 1.0, 0.3, 0.1 })
	{
		std::printf("  at 12 m, on axis, light %.1f: sees him %s, best rung %d\n", Light,
			Perception::InSight(12.0, 0.0, Light, false, 1.4) ? "yes" : "no",
			Perception::InSight(12.0, 0.0, Light, false, 1.4) ? Perception::IdRung(12.0, Light, 0.0, false, true) : 0);
	}
	std::printf("  => %s\n", V.ToActor.LightLevel == 1.0 ? "PROVED: the reading is fixed at full light; darker light would change what a witness sees" : "not reproduced");
}

// ---- A3: the free-play story key against the talk's deed key --------------
static void ProveA3()
{
	using namespace LedgerCrime;
	std::printf("\n[A3] Darren holds Rita's window at rung 1; what the talk and keep-quiet see\n");
	auto Mill = NewMill();
	Mill->Add(NewPerson("sam"));
	Mill->Witness("sam", Fact("player", "window_d0", "ritas"), "a window went in and nobody saw more than a shape", true, GameTime(0, 11, 0), 0.46, false, 1);
	GossiperPtr Sam = Mill->Get("sam");
	const std::string Deed = DeedJson(*Sam, WindowDeedKey(), 0, 11, std::string());
	std::printf("  the story he holds: %s   the key the talk asks with: %s\n", Sam->Rumors.empty() ? "(none)" : Sam->Rumors[0]->TopicKey().c_str(), WindowDeedKey());
	std::printf("  deed field sent to the talk: %s\n", Deed.empty() ? "(EMPTY: no deed, so no keep-quiet, owning up or threat)" : Deed.c_str());
	KeepQuiet(*Sam, WindowDeedKey());
	std::string S; for (size_t I = 0; I < Sam->Suppressed.size(); ++I) S += (I ? ", " : "") + Sam->Suppressed[I];
	std::printf("  kept quiet: [%s]; suppresses player.window_d0: %s\n", S.c_str(), Sam->SuppressedHas("player.window_d0") ? "yes" : "NO");
	RumorPtr Own = OwnedUpStory(WindowDeedKey(), "sam");
	std::printf("  owning up files: %s = \"%s\", sensitive=%s\n", Own->TopicKey().c_str(), Own->Summary.c_str(), Own->Sensitive ? "yes" : "no");
	std::printf("  => %s\n", Deed.empty() && !Sam->SuppressedHas("player.window_d0") ? "PROVED: the talk is never told the real deed, and keeping quiet leaves it spreading" : "not reproduced");
}

// ---- A4: no Statement, no report ------------------------------------------
static void ProveA4()
{
	std::printf("\n[A4] Can any witness in free play report him?\n");
	int Best0 = 0, Best35 = 0;
	for (double M = 0.5; M <= 40.0; M += 0.5)
	{
		const int R0 = Perception::IdRung(M, LedgerCrime::kLightLevel, LedgerCrime::kFamiliarity, false, true);
		const int R35 = Perception::IdRung(M, LedgerCrime::kLightLevel, Perception::RecognitionFamiliarity, false, true);
		if (R0 > Best0) Best0 = R0;
		if (R35 > Best35) Best35 = R35;
	}
	std::printf("  best rung at any distance, full light, facing him: familiarity 0.0 -> %d; familiarity 0.35 -> %d\n", Best0, Best35);
	const std::string Topic = "player.window_d0";
	GossiperPtr Default = NewPerson("sam");
	GossiperPtr Lower = NewPerson("sam", 0.4);
	std::printf("  WouldReport(damage), loyalty 0.5 (the default, never set in play): %s\n", PoliceFile::WouldReport(Default.get(), Offence::Damage, false, &Topic) ? "yes" : "NO");
	std::printf("  WouldReport(damage), loyalty 0.4: %s\n", PoliceFile::WouldReport(Lower.get(), Offence::Damage, false, &Topic) ? "yes" : "no");
	std::printf("  => %s\n", Best0 < 4 && !PoliceFile::WouldReport(Default.get(), Offence::Damage, false, &Topic)
		? "PROVED: with the game's familiarity (0.0) no reading reaches rung 4 (a Statement), and at the default loyalty nobody reports"
		: "not reproduced");
}

// ---- A5: a rung-0 story counts as "his" for the police --------------------
static void ProveA5()
{
	std::printf("\n[A5] Does the rung matter to the police?\n");
	auto Mill = NewMill();
	Mill->Add(NewPerson("lena"));
	Mill->Witness("lena", Fact("player", "window_d0", "ritas"), "heard glass go", true, GameTime(0, 11, 0), 0.40, false, 0);
	std::vector<std::string> Asked = PoliceFile::WhoSheAsks(Mill.get());
	std::printf("  a rung-0 (heard only) story: WhoSheAsks = [%s]; Loudness counts it: %d\n",
		Asked.empty() ? "" : Asked[0].c_str(), PoliceFile::Loudness(Mill.get()));
	std::printf("  => %s\n", !Asked.empty() ? "PROVED: a story from someone who only heard glass break marks her for DS Ellis's questions about him" : "not reproduced");
}

// ---- B1: Sheila's Sunday gate ---------------------------------------------
static void ProveB1()
{
	std::printf("\n[B1] Sheila's week's-end question (TownWeek's WeeksEnd, day %d)\n", TownWeek().Week.Day());
	TownWeek W;
	const GameTime Times[] = { GameTime(6, 10, 30), GameTime(6, 11, 59), GameTime(6, 12, 5), GameTime(7, 10, 0) };
	bool bLate = false;
	for (const GameTime& T : Times)
	{
		const bool bWaits = W.Week.Waits(T);
		std::printf("  Waits(%s) = %s\n", T.ToString().c_str(), bWaits ? "yes" : "no");
		if ((T.Day == 6 && T.Hour >= 12) || T.Day == 7) bLate = bLate || bWaits;
	}
	TownWeek Late;
	const bool bAsk = Late.Week.Ask(GameTime(7, 10, 0), false, true);
	std::printf("  but Ask(%s) itself accepts: %s\n", GameTime(7, 10, 0).ToString().c_str(), bAsk ? "yes" : "no");
	std::printf("  => %s\n", !bLate && bAsk ? "PROVED: the gate the game calls first (Waits) is shut after Sunday noon, though the week's own Ask would still put the question" : "not reproduced");
}

int main(int Argc, char** Argv)
{
	const std::string Bank = ReadAll(Argc > 1 ? Argv[1] : "content/dialogue/crime-witness-v1.json");
	if (Bank.empty()) { std::printf("the witness bank was not found\n"); return 2; }
	ProveA1(Bank, false);
	ProveA1(Bank, true);
	ProveA2();
	ProveA3();
	ProveA4();
	ProveA5();
	ProveB1();
	return 0;
}
