// THE ROUTE'S ACCEPTANCE ROWS, IN C++, 30 September (the town's half of the
// route, production/handovers/ROUTE.md, section 4). The Core's own week,
// ledger/TownReach/Program.cs WeekRows with the wait that stops and walks of
// 30, 120 and 30 game minutes, transliterated, driving the game's TownWeek
// (ue-probe/Source/LedgerProbe/Public/TownWeek.h) with the Core's stand-ins
// for what the player does. It prints the sixteen rows and the first row's
// stops exactly as TownReach --week-waits prints them; tools/route_week_check.py
// compares the two. Agreement means the game's hour, driven the same way,
// gives the Core's week.
//
//   route-week-test production/specs/hook-cast.json
#include "TownWeek.h"
#include "StreetVoice.h"
#include "Waiting.h"

#include <cstdio>
#include <fstream>
#include <set>
#include <sstream>
#include <string>
#include <vector>

using namespace LedgerCore;

namespace
{
	const int kTrustDaysTalked = 3;   // Trust.cs DaysTalked

	// TownReach's TrustsNow: three different days of talk, no deed of his she
	// saw, and nothing sensitive showing in her.
	bool TrustsNow(const GossipMill& Mill, const std::set<int>& TalkDays, bool bSheSaw, int Today)
	{
		int Days = 0;
		for (int D : TalkDays) if (D <= Today) ++Days;
		if (Days < kTrustDaysTalked || bSheSaw) return false;
		const GossiperPtr She = Mill.Get("lena");
		if (!She) return true;
		const RumorPtr R = StreetVoice::StoryThatShows(*She, Mill.MinConfidenceToShare);
		return !R || !R->Sensitive;
	}

	std::string Two(int N) { char B[8]; std::snprintf(B, sizeof(B), "%02d", N); return B; }

	void WeekRows(const CastDay& Cast, std::vector<std::string>& Rows, std::vector<std::string>& Stops, int& Missed,
	              int TeaLead, int LandingLead, int OfficeLead)
	{
		const std::vector<std::string>& People = Cast.People();
		int Miss = 0;
		for (bool bTakes : { true, false })
		for (bool bSits : { true, false })
		// Who sees the window (TownReach, 1 October): Sheila, one of Mickey's own, who
		// never goes to the police about him (Jafar's ruling of 1 October); Darren, at
		// the fish front with a body at Tuesday noon, who does (the review of 1
		// October, M4: behind her window Ada could never see Rita's glass in play);
		// nobody; or no window at all.
		for (const char* SeenByC : { "lena", "sam", "nobody", "none" })
		{
			const std::string SeenBy = SeenByC;
			auto Graph = std::make_shared<SocialGraph>();
			for (const CastDay::Tie& T : Cast.Ties()) Graph->Link(T.A, T.B, T.W);
			GossipMill Mill(Graph);
			for (const std::string& P : People)
				Mill.Add(std::make_shared<Gossiper>(P, P, std::make_shared<MemoryStore>(P), std::make_shared<KnowledgeBase>(), Cast.CircleOf(P)));
			TownWeek W;
			std::string Trust = "never";
			std::set<int> TalkDays;
			const bool bSheSaw = SeenBy == "lena";
			int HandOverAt = -1;
			const bool bFirst = bTakes && bSits && SeenBy == "lena";
			std::set<std::string> StopWhy, ShownLines;
			Mill.Age(GameTime(0, 9, 0));
			for (int Abs = 9; Abs < 24 * 7 + 12; ++Abs)
			{
				const int Day = Abs / 24, Hod = Abs % 24;
				const GameTime Now(Day, Hod, 0);
				auto InWait = [&W](int H) { return H >= 18 && (H % 24 >= 18 || H % 24 < (H / 24 == W.Week.Day() ? 12 : 10)); };
				const bool bWaitingOn = InWait(Abs) && InWait(Abs - 1);
				if (InWait(Abs) && !InWait(Abs - 1)) StopWhy.clear();
				std::shared_ptr<Custody> Held0 = W.Latest();
				if (bWaitingOn)
				{
					const int WakeDay = Hod >= 18 ? Day + 1 : Day;
					const GameTime Wake(WakeDay, WakeDay == W.Week.Day() ? 12 : 10, 0);
					WaitBeats B;
					B.Asks = &W.Asks; B.Tea = W.Tea.get(); B.Police = &W.Police; B.Mill = &Mill; B.Week = &W.Week; B.CustodyOf = Held0.get();
					B.Shown = ShownLines;
					B.TeaLead = TeaLead; B.LandingLead = LandingLead; B.OfficeLead = OfficeLead;
					B.AtAdas = bSits && Day == W.Tea->Day() && (Hod - 1 == 21 || Hod - 1 == 22);
					WaitStop St;
					while (Waiting::Next(Now.AddMinutes(-60), Wake, &B, St) && St.At.TotalMinutes() <= Now.TotalMinutes())
					{
						Waiting::Showed(&B, &St);
						StopWhy.insert(St.Why);
						if (bFirst) Stops.push_back("day " + std::to_string(St.At.Day + 1) + " " + Two(St.At.Hour) + ":" + Two(St.At.Minute) + " " + St.Why + ": \"" + St.Line + "\"");
					}
					ShownLines = B.Shown;
				}
				auto Skip = [&](const std::string& Why, bool bCount) -> bool
				{
					if (!bWaitingOn) return false;
					if (!StopWhy.count(Why)) { if (bCount) ++Miss; return true; }
					return false;
				};
				// The rounds before minute M of this hour (TownReach's Before; the review's A12).
				auto Before = [&](int M) { W.RoundsTo(&Mill, &Cast, Now.AddMinutes(M - 1)); };
				W.Six(&Mill, Now);
				// The slice's window, at noon on the Tuesday.
				if (SeenBy != "none" && Day == 1 && Hod == 12)
				{
					std::vector<std::pair<std::string, int> > Saw;
					if (SeenBy != "nobody") Saw.push_back(std::make_pair(SeenBy, -1));
					W.Deed(&Mill, Now, "ritas", "rita_window", "somebody put Rita's window in", Saw, "window_d1", "the new owner put Rita's window in", 1.0, false);
				}
				W.DamageTick(&Mill, &Cast, Now);
				W.NineReports(&Mill, &Cast, Now, 4);
				W.NineEllis(&Mill, Now, &Cast);
				if (Hod == 10 && W.Arrests.empty()) W.TenConstable(&Mill, &Cast, Now, "mickeys");
				const std::shared_ptr<Custody> C = W.Latest();
				const bool bHeld = C && C->Holds(Now);
				if (Hod == 10 && !bHeld && Day < W.Week.Day() && Cast.AreaOf(Cast.PlaceOf("lena", Day, Hod)) == "mickeys") TalkDays.insert(Day);
				if (Trust == "never" && Hod == 11 && TrustsNow(Mill, TalkDays, bSheSaw, Day)) Trust = "day " + std::to_string(Day + 1);
				std::string Invite;
				W.TenTea(Now, Invite);
				if (Hod == 20 && W.Asks.AsksOn(Day) && !Skip("ron", true)) W.TwentyRon(&Mill, Now);
				if (bSits && Day == W.Tea->Day() && Hod == 21 && !Skip("tea", true))
					for (int M = 0; M < 60; ++M) W.Tea->WithHer(GameTime(Day, 21, M));
				if (bSits && Day == W.Tea->Day() && Hod == 22 && !Skip("tea", false))
					for (int M = 0; M <= 30; ++M) W.Tea->WithHer(GameTime(Day, 22, M));
				W.TwentyThreeTea(&Mill, Now);
				// Not sitting with her, he sets off at 21:45 and is seen going in its own
				// hour, after the rounds before it, as TownReach files it (the review of 1
				// October, D2: this filed it in hour 22's pass, after rounds run without it).
				if (Hod == 21 && !bSits && bTakes && Day == W.Tea->Day() && W.Asks.AsksOn(Day) && !bHeld && W.Asks.WasDelivered(Day) && !Skip("landing", true))
				{
					Before(45);
					W.Tea->WentToTheLanding(&Mill, GameTime(Day, 21, 45), true);
					HandOverAt = Abs + 2;
				}
				if (Hod == 22 && W.Asks.AsksOn(Day) && !bHeld && W.Asks.WasDelivered(Day) && !(!bSits && bTakes && Day == W.Tea->Day())
				    && !Skip(bTakes ? "landing" : "ron", true))
				{
					const NightAnswer Answer = bTakes ? NightAnswer::Did : NightAnswer::Refused;
					if (Answer == NightAnswer::Did && Day == W.Tea->Day())
					{
						Before(31);
						W.Tea->WentToTheLanding(&Mill, GameTime(Day, 22, 31), true);
						HandOverAt = Abs + 2;
					}
					else { Before(30); W.AnswerAsk(Day, Answer, &Mill, GameTime(Day, 22, 30)); }
				}
				if (Abs == HandOverAt && W.Asks.AsksOn(W.Tea->Day()) && !Skip("landing", false))
				{
					Before(45);
					W.AnswerAsk(W.Tea->Day(), NightAnswer::Did, &Mill, GameTime(Day, Hod, 45));
				}
				// The week's end: her question at half past ten on the Sunday.
				if (Day == W.Week.Day() && Hod == 10 && W.Week.AsksNow(GameTime(Day, 10, 30), true) && !Skip("sheila", true))
				{
					W.Week.Ask(GameTime(Day, 10, 30), Trust != "never");
					Before(40);
					W.Week.Give(WeekAnswer::TakeOver, GameTime(Day, 10, 40), &Mill, &Cast, &W.Asks);
				}
				// The rest of the hour's rounds.
				const GameTime HourEndsAt = Now.AddMinutes(59);
				W.HourEnd(&Mill, &Cast, Now, &HourEndsAt);
			}
			int HoldAnswer = 0;
			for (const GossiperPtr& A : Mill.Agents())
			{
				for (const RumorPtr& R : A->Rumors) { if (WeeksEnd::IsWeekAnswer(R)) { ++HoldAnswer; break; } }
			}
			const std::string Arr = W.Asks.Ended() ? "ended (" + W.Asks.EndedWhy() + ")" : "stands (" + std::to_string(W.Asks.Nights().size()) + " nights)";
			GameTime AskedAt;
			const std::string Book = !W.Week.AskedAt(AskedAt) ? "not asked" : W.Week.RealBook() ? "the real book" : "the day-book";
			Rows.push_back("| " + std::string(bTakes ? "takes it every night" : "tells Ron no") + " | " + (bSits ? "sits with her" : "stands her up") + " | "
				+ (SeenBy == "none" ? "no window" : SeenBy) + " | " + W.EllisFirst + " | " + W.TakenFirst + " | " + Trust + " | " + Book + " | " + Arr
				+ " | " + std::to_string(HoldAnswer) + " of " + std::to_string(People.size()) + " |");
		}
		Missed = Miss;
	}
}

int main(int Argc, char** Argv)
{
	if (Argc < 2) { std::fprintf(stderr, "usage: route-week-test CAST.json\n"); return 2; }
	std::ifstream F(Argv[1], std::ios::binary);
	std::stringstream S;
	S << F.rdbuf();
	CastDay Cast;
	std::string Err;
	if (!CastDay::Parse(S.str(), Cast, Err)) { std::fprintf(stderr, "cast file: %s\n", Err.c_str()); return 2; }
	std::vector<std::string> Rows, Stops;
	int Missed = 0;
	WeekRows(Cast, Rows, Stops, Missed, 30, 120, 30);
	std::printf("with walks 30, 120, 30: missed %d\n", Missed);
	for (const std::string& R : Rows) std::printf("%s\n", R.c_str());
	std::printf("the stops, first row (takes the envelope, sits with Ada, Sheila sees the window):\n");
	for (const std::string& St : Stops) std::printf("  %s\n", St.c_str());
	return 0;
}
