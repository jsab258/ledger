// A mirror of CrimeProbe.cpp's free-play clock (ClockTick / ClockHours /
// ConsequenceHour / ConstableHour / WaitKeyTick) driving the game's own
// headers (TownWeek.h, Waiting.h, LiveClock.h, CrimeProbe.h's WaitHourByHour).
// Unreal-only parts (bodies, Say on screen, saves) are replaced by printing.
#include "TownWeek.h"
#include "Waiting.h"
#include "LiveClock.h"
#include "StreetVoice.h"

#include <cstdio>
#include <fstream>
#include <memory>
#include <set>
#include <sstream>
#include <string>
#include <vector>

using namespace LedgerCore;

// Verbatim copy of CrimeProbe.h 1646-1665 (WaitHourByHour), so this harness
// does not pull the whole CrimeProbe.h.
template <class FStopAt, class FAdvance>
long long WaitHourByHour(long long FromM, long long UntilM, FStopAt StopAt, FAdvance Advance, bool& bStopped)
{
	bStopped = false;
	long long NowM = FromM;
	while (NowM < UntilM)
	{
		const long long HourEnd = (NowM >= 0 ? NowM / 60 + 1 : -((-NowM) / 60)) * 60;
		const long long SegEnd = HourEnd < UntilM ? HourEnd : UntilM;
		long long At = 0;
		if (StopAt(NowM, SegEnd, At) && At >= NowM && At <= SegEnd)
		{
			bStopped = true;
			return Advance(At, true);
		}
		const long long Landed = Advance(SegEnd, false);
		if (Landed > SegEnd) return Landed;
		NowM = SegEnd;
	}
	return NowM;
}

static CastDay GCast;

struct Sim
{
	std::unique_ptr<GossipMill> Mill;
	TownWeek W;
	LiveClock Clock;
	GameTime Now;
	bool bHeldPending = false;
	GameTime HeldUntil;
	std::set<std::string> WaitShown;
	bool bQuiet = false;
	int VisitDayLog = -1;

	Sim()
	{
		auto Graph = std::make_shared<SocialGraph>();
		for (const CastDay::Tie& T : GCast.Ties()) Graph->Link(T.A, T.B, T.W);
		Mill.reset(new GossipMill(Graph));
		for (const std::string& P : GCast.People())
			Mill->Add(std::make_shared<Gossiper>(P, P, std::make_shared<MemoryStore>(P), std::make_shared<KnowledgeBase>(), GCast.CircleOf(P)));
		Now = GameTime(0, 9, 0);
		Clock = LiveClock(Now);
		W.RoundsTo(Mill.get(), &GCast, Now);   // ClockTick's first call
	}
	void Say(const std::string& S) { if (!bQuiet) std::printf("  [%s] %s\n", Now.ToString().c_str(), S.c_str()); }

	// CrimeProbe.cpp ConstableHour (5411-5430)
	void ConstableHour(const GameTime& H)
	{
		const std::shared_ptr<Custody> C = W.TenConstable(Mill.get(), &GCast, H, "mickeys");
		if (!C) return;
		Say("A constable: " + C->ArrestWords().substr(0, 60) + "...  (out at " + C->OutAt().ToString() + ")");
		bHeldPending = true;
		HeldUntil = C->OutAt();
	}
	// CrimeProbe.cpp ConsequenceHour (5475-5512)
	void ConsequenceHour(const GameTime& H)
	{
		W.Six(Mill.get(), H);
		W.DamageTick(Mill.get(), &GCast, H);
		for (const std::string& Who : W.NineReports(Mill.get(), &GCast, H)) Say(Who + " goes to the police about " + W.DeedTopic);
		const std::string Why = W.NineEllis(Mill.get(), H, &GCast);
		if (!Why.empty()) Say("DS Ellis is on Quay Street this morning, asking after you. (" + Why + ")");
		ConstableHour(H);
		std::string Invite;
		if (W.TenTea(H, Invite)) Say("Ada, from her step: \"" + Invite + "\"");
		if (W.TwentyRon(Mill.get(), H)) Say("Ron's at the door with an envelope for you");
		W.TwentyThreeTea(Mill.get(), H);
		W.HourEnd(Mill.get(), &GCast, H);
	}
	// CrimeProbe.cpp ClockHours (5610-5632)
	void ClockHours(const std::vector<GameTime>& Hours)
	{
		for (const GameTime& H : Hours)
		{
			W.RoundsTo(Mill.get(), &GCast, H.AddMinutes(-1));
			ConsequenceHour(H);
		}
		if (bHeldPending)
		{
			bHeldPending = false;
			const std::vector<GameTime> Held = Clock.JumpTo(HeldUntil);
			Now = Clock.Now();
			ClockHours(Held);
			if (W.Latest()) Say("release: " + W.Latest()->ReleaseWords().substr(0, 50) + "...");
		}
	}
	// ClockTick, a game minute at a time (5940-5955)
	void PlayMinute()
	{
		const std::vector<GameTime> Hours = Clock.JumpTo(Clock.Now().AddMinutes(1));
		Now = Clock.Now();
		ClockHours(Hours);
		W.RoundsTo(Mill.get(), &GCast, Now);
	}
	void PlayTo(const GameTime& T) { while (Now.TotalMinutes() < T.TotalMinutes()) PlayMinute(); }

	// CrimeProbe.cpp WaitKeyTick (5979-6068)
	bool Wait(bool bAtAdas = false, std::string* KeyOut = nullptr)
	{
		WaitBeats B;
		B.Asks = &W.Asks; B.Tea = W.Tea.get(); B.Police = &W.Police; B.Mill = Mill.get(); B.Week = &W.Week;
		std::shared_ptr<Custody> Held = W.Holding(Now);
		B.CustodyOf = Held.get();
		B.AtAdas = bAtAdas;
		B.WalkRoundDone = true;
		B.Shown = WaitShown;
		const GameTime From = Now, Until = Now.AddMinutes(8 * 60);
		WaitStop S;
		auto ReadStop = [&](long long FromM, long long ToM) -> bool
		{
			Held = W.Holding(Now);
			B.CustodyOf = Held.get();
			B.Shown = WaitShown;
			return Waiting::Next(GameTime::FromTotalMinutes(FromM), GameTime::FromTotalMinutes(ToM), &B, S);
		};
		auto StopAt = [&](long long FromM, long long ToM, long long& AtM) -> bool
		{
			bool bFound = ReadStop(FromM, ToM);
			if (!bFound || S.At.TotalMinutes() >= ToM)
			{
				W.RoundsTo(Mill.get(), &GCast, GameTime::FromTotalMinutes(ToM - 1));
				bFound = ReadStop(FromM, ToM);
			}
			if (!bFound) return false;
			AtM = S.At.TotalMinutes();
			return true;
		};
		auto Advance = [&](long long ToM, bool bStop) -> long long
		{
			const GameTime SegFrom = Now;
			const std::vector<GameTime> Hours = Clock.JumpTo(GameTime::FromTotalMinutes(ToM));
			Now = Clock.Now();
			if (bAtAdas && W.Tea)
				for (GameTime M = SegFrom.AddMinutes(1); M.TotalMinutes() <= Now.TotalMinutes(); M = M.AddMinutes(1))
					if (M.Day == W.Tea->Day() && M.Hour >= AdasTea::From && M.Hour < AdasTea::Until) W.Tea->WithHer(M);
			if (bStop)
			{
				Say("WAIT STOPS: \"" + std::string(S.Line) + "\" (" + S.Key + ")");
				Waiting::Showed(&B, &S);
				WaitShown = B.Shown;
			}
			ClockHours(Hours);
			return Now.TotalMinutes();
		};
		bool bStopped = false;
		WaitHourByHour(From.TotalMinutes(), Until.TotalMinutes(), StopAt, Advance, bStopped);
		Say(std::string("wait from ") + From.ToString() + " ended" + (bStopped ? " (stopped)" : " (ran out)"));
		if (KeyOut) *KeyOut = bStopped ? S.Key : std::string();
		return bStopped;
	}
};

int main(int Argc, char** Argv)
{
	std::ifstream F(Argv[1], std::ios::binary);
	std::stringstream SS;
	SS << F.rdbuf();
	std::string Err;
	if (!CastDay::Parse(SS.str(), GCast, Err)) { std::fprintf(stderr, "cast: %s\n", Err.c_str()); return 2; }
	const std::string Which = Argc > 2 ? Argv[2] : "all";

	if (Which == "all" || Which == "tea-cells")
	{
		std::printf("\n[S1] Monday's window seen and recognised (rung 4) by Darren; then a wait from Wednesday 09:30\n");
		Sim G;
		G.PlayTo(GameTime(0, 12, 0));
		G.W.Deed(G.Mill.get(), G.Now, "ritas", "rita_window", "somebody put Rita's window in", { { "sam", 4 } }, "window_d0", "the new owner put Rita's window in", 0.94, true);
		G.Say("the deed (Darren, rung 4)");
		G.PlayTo(GameTime(2, 9, 30));
		G.Wait();
		std::printf("  tea state now %d (1=Asked); custody holds at 10:30? %s\n", (int)G.W.Tea->State(),
			G.W.Arrests.empty() ? "none" : (G.W.Arrests[0]->Holds(GameTime(2, 10, 30)) ? "yes" : "no"));
	}

	if (Which == "all" || Which == "ellis-scan")
	{
		std::printf("\n[S2] Scan: does the street's talk reach DS Ellis's loudness (3) during the 09:00 hour's rounds, after NineEllis decided?\n");
		int Found = 0;
		// He takes the envelope each ask night at a chosen minute; a window on a chosen day and hour, seen by a chosen witness at rung 4.
		const char* Witnesses[] = { "none", "lena", "sam", "ada", "ines", "marla" };
		for (const char* Wit : Witnesses)
		for (int DeedDay = 0; DeedDay <= 3 && Found < 3; ++DeedDay)
		for (int DeedHour : { 11, 12, 13, 15, 17 })
		for (int HandMin : { 0, 30, 90, 170 })
		{
			if (std::string(Wit) == "none" && (DeedDay > 0 || DeedHour != 11)) continue;
			Sim G;
			G.bQuiet = true;
			bool bDeed = std::string(Wit) == "none";
			for (int Step = 0; Step < 6 * 24 * 60 && Found < 3; ++Step)
			{
				// his envelope, at the landing on each ask night
				const int Night = Arrangement::NightOf(G.Now);
				const GameTime Hand = GameTime(Night, 22, 0).AddMinutes(HandMin);
				if (G.W.Asks.AskStands(G.Now) && G.Now.TotalMinutes() == Hand.TotalMinutes()) G.W.AnswerAsk(Night, NightAnswer::Did, G.Mill.get(), G.Now);
				if (!bDeed && G.Now.Day == DeedDay && G.Now.Hour == DeedHour)
				{
					G.W.Deed(G.Mill.get(), G.Now, "ritas", "rita_window", "somebody put Rita's window in", { { Wit, 4 } },
						"window_d" + std::to_string(DeedDay), "the new owner put Rita's window in", 0.94, true);
					bDeed = true;
				}
				const int Before = PoliceFile::Loudness(G.Mill.get());
				G.PlayMinute();
				const int After = PoliceFile::Loudness(G.Mill.get());
				if (G.Now.Hour == 9 && G.Now.Day >= PoliceFile::TalkNoSoonerThan && Before < PoliceFile::LoudAt && After >= PoliceFile::LoudAt
				    && G.W.Police.Visits().empty())
				{
					++Found;
					std::printf("  witness=%s deed day %d %02d:00, envelope at 22:00+%d min: loudness %d -> %d at %s; DS Ellis's visits so far: %zu\n",
						Wit, DeedDay, DeedHour, HandMin, Before, After, G.Now.ToString().c_str(), G.W.Police.Visits().size());
					// He presses Z a few minutes later in that hour.
					G.PlayTo(G.Now.AddMinutes(2));
					G.bQuiet = false;
					std::string Key;
					G.Wait(false, &Key);
					std::printf("  => DS Ellis's visits recorded on day %d: ", G.Now.Day);
					for (const auto& V : G.W.Police.Visits()) std::printf("[day %d, %s] ", V.first, V.second.c_str());
					std::printf("\n");
					break;
				}
			}
		}
		if (Found == 0) std::printf("  no case found in the scan\n");
	}
	if (Which == "loud-when")
	{
		const char* Witnesses[] = { "none", "lena", "sam", "ada", "ines", "marla" };
		for (const char* Wit : Witnesses)
		for (int DeedDay : {0, 1, 2, 3})
		for (int DeedHour : { 12, 17 })
		for (int Takes : {0, 1})
		{
			if (std::string(Wit) == "none" && (DeedDay > 0 || DeedHour != 12)) continue;
			Sim G; G.bQuiet = true; bool bDeed = std::string(Wit) == "none";
			std::string Trans;
			int Last = 0;
			for (int Step = 0; Step < 6 * 24 * 60; ++Step)
			{
				const int Night = Arrangement::NightOf(G.Now);
				if (Takes && G.W.Asks.AskStands(G.Now) && G.Now.Hour == 22 && G.Now.Minute == 30) G.W.AnswerAsk(Night, NightAnswer::Did, G.Mill.get(), G.Now);
				if (!bDeed && G.Now.Day == DeedDay && G.Now.Hour == DeedHour)
				{ G.W.Deed(G.Mill.get(), G.Now, "ritas", "rita_window", "x", { { Wit, 4 } }, "window_d" + std::to_string(DeedDay), "the new owner put Rita's window in", 0.94, true); bDeed = true; }
				G.PlayMinute();
				const int L = PoliceFile::Loudness(G.Mill.get());
				if (L != Last) { Trans += " " + G.Now.ToString() + "=" + std::to_string(L); Last = L; }
			}
			std::string V; for (const auto& X : G.W.Police.Visits()) V += " [d" + std::to_string(X.first) + " " + X.second + "]";
			std::printf("wit=%s deed d%d %02d takes=%d | loud:%s | visits:%s\n", Wit, DeedDay, DeedHour, Takes, Trans.substr(0, 300).c_str(), V.c_str());
		}
	}
	if (Which == "ellis-false")
	{
		std::printf("\n[S3] No envelopes (he never goes down); Thursday (day 3) 17:00 Sheila, on Rita's step by her day, sees the window at rung 4. Friday he presses Z at 09:05.\n");
		Sim G;
		G.PlayTo(GameTime(3, 17, 0));
		G.W.Deed(G.Mill.get(), G.Now, "ritas", "rita_window", "somebody put Rita's window in", { { "lena", 4 } }, "window_d3", "the new owner put Rita's window in", 0.94, true);
		G.Say(std::string("the deed; Sheila's place by her routine now: ") + GCast.PlaceOf("lena", 3, 17));
		G.bQuiet = true;
		G.PlayTo(GameTime(4, 8, 59));
		G.bQuiet = false;
		G.Say("loudness at 08:59: " + std::to_string(PoliceFile::Loudness(G.Mill.get())));
		G.PlayTo(GameTime(4, 9, 0));
		G.Say("loudness after the 09:00 hour's events and its 09:00 round: " + std::to_string(PoliceFile::Loudness(G.Mill.get())) + "; visits " + std::to_string(G.W.Police.Visits().size()));
		G.PlayTo(GameTime(4, 9, 5));
		G.Wait();
		std::printf("  DS Ellis's visits so far: ");
		for (const auto& V : G.W.Police.Visits()) std::printf("[day %d, %s] ", V.first, V.second.c_str());
		std::printf("(none on day 4)\n");
		G.Wait();
		G.Wait();
		std::printf("  DS Ellis's visits so far: ");
		for (const auto& V : G.W.Police.Visits()) std::printf("[day %d, %s] ", V.first, V.second.c_str());
		std::printf("\n");
	}
	if (Which == "ellis-false-night")
	{
		std::printf("\n[S3b] As S3, but he presses Z on Friday at 02:00 (asleep through the morning).\n");
		Sim G;
		G.bQuiet = true;
		G.PlayTo(GameTime(3, 17, 0));
		G.W.Deed(G.Mill.get(), G.Now, "ritas", "rita_window", "somebody put Rita's window in", { { "lena", 4 } }, "window_d3", "the new owner put Rita's window in", 0.94, true);
		G.PlayTo(GameTime(4, 2, 0));
		G.bQuiet = false;
		G.Wait();
		std::printf("  DS Ellis's visits so far: %zu\n", G.W.Police.Visits().size());
		G.Wait();
		G.Wait();
		G.Wait();
		std::printf("  DS Ellis's visits: ");
		for (const auto& V : G.W.Police.Visits()) std::printf("[day %d, %s] ", V.first, V.second.c_str());
		std::printf("\n");
	}
	if (Which == "no-late")
	{
		std::printf("\n[S4] Night 0: Ron's plain question at 22:58, his yes read at 23:03 (refusedAt 22:58), as CrimeProbe.cpp 4536-4552 answers it.\n");
		Sim G;
		G.bQuiet = true;
		G.PlayTo(GameTime(0, 23, 3));
		const GameTime At(0, 22, 58);
		const bool Ok = G.W.AnswerAsk(Arrangement::NightOf(At), NightAnswer::Refused, G.Mill.get(), At);
		auto Has = [&]() { const GossiperPtr M = G.Mill->Get("outfit_man"); for (const RumorPtr& R : M->Rumors) if (R && R->TopicKey() == "player.outfit_d0") return true; return false; };
		std::printf("  answered: %s; NoWordAt pending: %s\n", Ok ? "yes" : "no", G.W.Asks.NoNight() >= 0 ? "yes" : "no");
		G.PlayTo(GameTime(0, 23, 30));
		std::printf("  23:30: the man at the landing holds the no: %s\n", Has() ? "yes" : "no");
		G.PlayTo(GameTime(0, 23, 59));
		std::printf("  23:59: the man at the landing holds the no: %s (the 23:00..23:54 rounds have run)\n", Has() ? "yes" : "no");
		G.PlayTo(GameTime(1, 0, 0));
		std::printf("  00:00: holds it: %s; his memory of it stamped: ", Has() ? "yes" : "no");
		const GossiperPtr M = G.Mill->Get("outfit_man");
		for (const auto& E : M->Memory->Events) if (E.Text.find("told them no") != std::string::npos) std::printf("%s ", E.Time.ToString().c_str());
		std::printf("\n");
	}
	if (Which == "tea")
	{
		std::printf("\n[S5] Ada's tea, judged (FirstWeek.h): first minute..last minute -> state\n");
		const int Cases[][2] = { {21*60, 22*60+29}, {21*60, 22*60+30}, {21*60+45, 22*60+40}, {22*60, 22*60+30}, {22*60+1, 22*60+59}, {21*60+31, 22*60+35}, {21*60+5, 21*60+5} };
		for (const auto& C : Cases)
		{
			std::unique_ptr<AdasTea> T = AdasTea::For(0, true);
			std::string Inv; T->SheSeesHim(GameTime(2, 10, 0), Inv);
			for (int M = C[0]; M <= C[1]; ++M) T->WithHer(GameTime(2, M / 60, M % 60));
			auto Ada = std::make_shared<Gossiper>("ada", "ada", std::make_shared<MemoryStore>("ada"), std::make_shared<KnowledgeBase>(), "day");
			const TeaState St = T->Close(Ada.get(), GameTime(2, 23, 0));
			std::printf("  %02d:%02d..%02d:%02d -> %s, loyalty %.2f: %s\n", C[0] / 60, C[0] % 60, C[1] / 60, C[1] % 60, TeaStateName(St), Ada->Loyalty,
				Ada->Memory->Events.empty() ? "" : Ada->Memory->Events.back().Text.c_str());
		}
	}
	if (Which == "misc")
	{
		std::printf("\n[S6] SpellCouldBe: a saved arrest out at 00:05 on the call's day (the call is at 10:00)\n");
		const std::string J = "{\"entries\":[{\"who\":\"sam\",\"topic\":\"player.window_d0\",\"offence\":\"Damage\",\"how\":\"Statement\",\"day\":1}],"
			"\"visits\":[],\"calls\":[[2,\"player.window_d0\"]],\"taken\":[[\"player.window_d0\"," + std::to_string(2 * 1440 + 5) + "]]}";
		PoliceFile P = PoliceFile::FromJson(J);
		std::printf("  loaded: in the cells at D2 00:01? %s; at D2 09:00? %s\n", P.InTheCells(GameTime(2, 0, 1)) ? "yes" : "no", P.InTheCells(GameTime(2, 9, 0)) ? "yes" : "no");
		const std::string J2 = "{\"entries\":[{\"who\":\"sam\",\"topic\":\"player.window_d0\",\"offence\":\"Damage\",\"how\":\"Statement\",\"day\":1}],"
			"\"visits\":[],\"calls\":[[2,\"player.window_d0\"]],\"taken\":[[\"player.window_d0\"," + std::to_string(3 * 1440 + 20 * 60) + "]]}";
		PoliceFile P2 = PoliceFile::FromJson(J2);
		std::printf("  a spell out at D3 20:00 for a call on D2 10:00 (34 h; Damage is at most 6 h): kept? %s\n", P2.InTheCells(GameTime(3, 19, 0)) ? "yes" : "no");

		std::printf("\n[S7] Arrangement.Answer(Refused) before Ron has brought the ask\n");
		Arrangement A(0);
		std::unique_ptr<GossipMill> M; { auto Gr = std::make_shared<SocialGraph>(); M.reset(new GossipMill(Gr)); }
		const GameTime T(0, 15, 0);
		std::printf("  with a time, undelivered: %s\n", A.Answer(0, NightAnswer::Refused, M.get(), &T) ? "accepted" : "refused");
		std::printf("  without a time (no mill), undelivered: %s\n", A.Answer(0, NightAnswer::Refused) ? "accepted" : "refused");

		std::printf("\n[S8] WeeksEnd.AsksNow at the office\n");
		WeeksEnd W;
		const GameTime Ts[] = { GameTime(6, 9, 59), GameTime(6, 10, 0), GameTime(6, 11, 59), GameTime(6, 12, 0), GameTime(6, 23, 0), GameTime(7, 3, 0), GameTime(7, 9, 0), GameTime(13, 10, 0) };
		for (const GameTime& X : Ts) std::printf("  %s (weekday %d): %s\n", X.ToString().c_str(), CastDay::Weekday(X.Day), W.AsksNow(X, true) ? "asks" : "no");
		std::printf("  Sheila's place by her day: D7 03:00 %s, D7 12:30 %s, D7 17:30 %s\n", GCast.PlaceOf("lena", 7, 3).c_str(), GCast.PlaceOf("lena", 7, 12).c_str(), GCast.PlaceOf("lena", 7, 17).c_str());
	}
	if (Which == "b5")
	{
		std::printf("\n[S9] A window at D2 00:30 (Tuesday night), seen at rung 4 by Darren\n");
		Sim G;
		G.bQuiet = true;
		G.PlayTo(GameTime(2, 0, 30));
		G.W.Deed(G.Mill.get(), G.Now, "ritas", "rita_window", "somebody put Rita's window in", { { "sam", 4 } }, "window_d2", "the new owner put Rita's window in", 0.94, true);
		G.bQuiet = false;
		std::printf("  mended at %s; first report morning %s\n", G.W.Damage[0].MendedAt().ToString().c_str(), Aftermath::FirstReportMorning(G.W.DeedAt).ToString().c_str());
		G.PlayTo(GameTime(3, 11, 0));
	}
	if (Which == "ahead-scan")
	{
		const char* Wits[] = { "lena", "sam", "ada", "marta", "jelena", "ines", "iva", "noor", "zora" };
		int Found = 0;
		for (const char* Wit : Wits)
		for (int DeedDay : { 2, 3, 4 })
		for (int DeedHour : { 10, 12, 14, 16, 17, 18 })
		for (int Takes : { 0, 1 })
		{
			if (Found >= 2) break;
			Sim G; G.bQuiet = true;
			bool bDeed = false;
			while (G.Now.TotalMinutes() < GameTime(6, 10, 0).TotalMinutes())
			{
				const int Night = Arrangement::NightOf(G.Now);
				if (Takes && G.W.Asks.AskStands(G.Now) && G.Now.Hour == 22 && G.Now.Minute == 30) G.W.AnswerAsk(Night, NightAnswer::Did, G.Mill.get(), G.Now);
				if (!bDeed && G.Now.Day == DeedDay && G.Now.Hour == DeedHour)
				{ G.W.Deed(G.Mill.get(), G.Now, "ritas", "rita_window", "x", { { Wit, 4 } }, "window_d" + std::to_string(DeedDay), "the new owner put Rita's window in", 0.94, true); bDeed = true; }
				G.PlayMinute();
				if (G.Now.Hour == 9 && G.Now.Minute == 0 && G.Now.Day >= 3 && G.W.Police.Visits().empty() && PoliceFile::Loudness(G.Mill.get()) < 3)
				{
					// What would the hour's rounds bring? Run a copy.
					Sim Copy = std::move(G);
					// (Sim is not copyable; re-run below instead)
					G = std::move(Copy);
					// look ahead minute by minute in place, then report
					std::vector<std::string> Trail;
					int CrossAt = -1;
					// save nothing: just play through the hour and note the crossing
					for (int M = 1; M < 60; ++M)
					{
						G.PlayMinute();
						if (CrossAt < 0 && PoliceFile::Loudness(G.Mill.get()) >= 3) CrossAt = M;
					}
					if (CrossAt > 0)
					{
						++Found;
						std::printf("FOUND wit=%s deed d%d %02d takes=%d: loudness reaches 3 at D%d 09:%02d\n", Wit, DeedDay, DeedHour, Takes, G.Now.Day, CrossAt);
					}
				}
			}
		}
		if (!Found) std::printf("no crossing at 09:06..09:54 found\n");
	}
	if (Which == "ellis-true")
	{
		std::printf("\n[S10] Wednesday 17:00 window seen by Sheila at rung 4, no envelopes; Z on Friday at 02:00\n");
		Sim G; G.bQuiet = true;
		G.PlayTo(GameTime(2, 17, 0));
		G.W.Deed(G.Mill.get(), G.Now, "ritas", "rita_window", "x", { { "lena", 4 } }, "window_d2", "the new owner put Rita's window in", 0.94, true);
		G.PlayTo(GameTime(4, 2, 0));
		G.bQuiet = false;
		G.Say("loudness " + std::to_string(PoliceFile::Loudness(G.Mill.get())) + ", visits " + std::to_string(G.W.Police.Visits().size()));
		G.Wait();
	}
	return 0;
}
