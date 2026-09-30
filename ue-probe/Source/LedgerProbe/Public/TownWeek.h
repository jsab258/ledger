// THE TOWN'S WEEK, HOUR BY HOUR, 30 September (Jafar's list after the audit,
// item 1; the town's half of the route, production/handovers/ROUTE.md). The
// game's clock hands each game hour to this, and it runs the town's scheduled
// work in the order the Core's own week does (ledger/TownReach/Program.cs,
// WeekRows): six o'clock the asks' nights passed; the damage found; nine the
// witnesses to the police and DS Ellis; ten the constable and Ada's
// invitation; eight in the evening Ron at the door on an ask night; eleven the
// tea's close; every hour the week's end closed and the town's talk. What the
// player does (the deed, the envelope or a no, the tea, Sunday's answer) comes
// between those steps, called by the game when he does it, or by the route's
// acceptance replay (ue-probe/tests/route-week-test.cpp) at the moments the
// Core's week has it, which must give the Core's rows.
//
// Keyed by the cast's own ids (ROUTE.md step 0). One owner of the pieces, so
// the game's save is one TownSave of them.
//
// NO UNREAL TYPE IS IN THIS FILE, as every file of the port.
#pragma once

#include "Arrangement.h"
#include "CastDay.h"
#include "FirstWeek.h"
#include "Gossip.h"
#include "PoliceFile.h"
#include "TownNews.h"
#include "TownRounds.h"
#include "WeeksEnd.h"

#include <functional>
#include <memory>
#include <string>
#include <utility>
#include <vector>

namespace LedgerCore
{
	class TownWeek
	{
	public:
		Arrangement Asks = Arrangement(0);
		std::unique_ptr<AdasTea> Tea = AdasTea::For(0, true);
		PoliceFile Police;
		WeeksEnd Week;
		std::vector<Aftermath> Damage;
		std::vector<std::shared_ptr<Custody> > Arrests;
		TownHours Hours;

		/// The deed's story (ROUTE.md step 2), who saw it and at what rung;
		/// empty until he does one.
		std::string DeedTopic;
		int DeedDay = -1;
		GameTime DeedAt;   // when it was done: its night, and so its first report (the review's B5)
		std::vector<std::pair<std::string, int> > Witnesses;
		/// What the week has come to, as the Core's rows put it.
		std::string EllisFirst = "never", TakenFirst = "no";

		/// The custody holding him now, or none.
		std::shared_ptr<Custody> Holding(const GameTime& Now) const
		{
			for (const auto& C : Arrests) { if (C && C->Holds(Now)) return C; }
			return nullptr;
		}
		std::shared_ptr<Custody> Latest() const { return Arrests.empty() ? nullptr : Arrests.back(); }

		// ---- the scheduled steps, in the Core's order within an hour ----

		/// 06:00: the asks' nights passed (a night away filed).
		/// Also, as each hour turns and before anything else in it, his no or the
		/// winding down reaches the landing when Ron goes down (Arrangement's
		/// TellDue; the review's B3).
		void Six(GossipMill* Mill, const GameTime& Now)
		{
			Asks.TellDue(Mill, Now);
			if (Now.Hour == 6) Asks.PassedTo(Now.Day, Mill, &Now);
		}

		/// THE TOWN'S TALK UP TO A MOMENT (the review's A12): every round not yet
		/// run up to At, once; the game calls it as its minutes pass and before
		/// a talk turn, the reference week before each event's minute.
		void RoundsTo(GossipMill* Mill, const CastDay* Cast, const GameTime& At) { Hours.RunTo(Mill, Cast, At); }

		/// THE DEED (ROUTE.md step 2), when he does it: the damage kept, and
		/// each witness holding it first-hand as a sensitive story at the rung
		/// they saw him at (Rung < 0: as the Core's week, no rung).
		/// `bWitnessesLeftOut`: those who saw it done never "find" it (the
		/// town's card for the game); the Core's week leaves nobody out.
		void Deed(GossipMill* Mill, const GameTime& Now, const std::string& Area, const std::string& Thing, const std::string& Said,
		          const std::vector<std::pair<std::string, int> >& Saw, const std::string& StoryFact, const std::string& StorySaid, double Certainty,
		          bool bWitnessesLeftOut = true, const std::vector<std::string>* AlsoLeftOut = nullptr)
		{
			std::vector<std::string> LeaveOut;
			if (bWitnessesLeftOut) for (const auto& S : Saw) LeaveOut.push_back(S.first);
			// Those who only heard it go (the review's A1): they know the window
			// went, and never "find" it; they are not witnesses of him.
			if (AlsoLeftOut != nullptr) for (const std::string& H : *AlsoLeftOut) LeaveOut.push_back(H);
			Aftermath A;
			const GameTime Mend = Aftermath::DefaultMend(Now);
			if (Aftermath::Make(Area, Thing, Said, Now, &Mend, bWitnessesLeftOut ? &LeaveOut : nullptr, A)) Damage.push_back(A);
			DeedTopic = "player." + StoryFact;
			DeedDay = Now.Day;
			DeedAt = Now;
			Witnesses = Saw;
			if (Mill == nullptr) return;
			for (const auto& S : Saw)
				Mill->Witness(S.first, Fact("player", StoryFact, Area), StorySaid, true, Now, Certainty, false, S.second);
		}

		/// Every hour after the deed: whoever comes into the area finds it.
		std::vector<std::pair<std::string, GameTime> > DamageTick(GossipMill* Mill, const CastDay* Cast, const GameTime& Now)
		{
			std::vector<std::pair<std::string, GameTime> > Found;
			for (Aftermath& A : Damage) { for (const auto& F : A.Tick(Mill, Cast, Now)) Found.push_back(F); }
			return Found;
		}

		/// 09:00 from the day after it: each witness goes to the police once
		/// they would (ROUTE.md step 4). Returns who did.
		std::vector<std::string> NineReports(GossipMill* Mill, const CastDay* Cast, const GameTime& Now, int RungOverride = -1)
		{
			std::vector<std::string> Went;
			// From nine the morning after its night: a deed before six is the night before's (B5).
			if (Now.Hour != 9 || DeedDay < 0 || Now.TotalMinutes() < Aftermath::FirstReportMorning(DeedAt).TotalMinutes()
			    || DeedTopic.empty() || Mill == nullptr) return Went;
			for (const auto& W : Witnesses)
			{
				bool bGave = false;
				for (const auto& E : Police.Entries()) { if (E.Who == W.first && E.Topic == DeedTopic && E.How != Known::Talk) { bGave = true; break; } }
				if (bGave) continue;
				const GossiperPtr G = Mill->Get(W.first);
				const bool bNever = Cast != nullptr && Cast->NeverToPolice(W.first);
				if (!PoliceFile::WouldReport(G.get(), Offence::Damage, false, &DeedTopic, bNever)) continue;
				if (Police.Report(W.first, DeedTopic, Offence::Damage, RungOverride >= 0 ? RungOverride : W.second, Now.Day)) Went.push_back(W.first);
			}
			return Went;
		}

		/// 09:00: DS Ellis, while there is a reason (ROUTE.md step 5). The
		/// reason, or empty. Come for the street's talk, she hears it
		/// (PoliceFile.HearTheStreet, the game grading its deeds: a window is
		/// damage, the rest suspicious, as the Core's week grades them); she
		/// hears and asks only the people on the street at nine (the cast).
		static Offence GradeOf(const std::string& Topic) { return Topic.compare(0, 13, "player.window") == 0 ? Offence::Damage : Offence::Suspicious; }
		std::string NineEllis(GossipMill* Mill, const GameTime& Now, const CastDay* Cast)
		{
			if (Now.Hour != 9 || Now.Day < 1 || Mill == nullptr) return std::string();
			std::string Why;
			if (!Police.EllisComes(Mill, Now.Day, Inquiry::None, Why)) return std::string();
			if (Why == "talk") Police.HearTheStreet(Mill, Now.Day, &GradeOf, Cast, &Now);
			if (EllisFirst == "never") EllisFirst = "day " + std::to_string(Now.Day + 1) + ", for " + Why;
			const std::vector<std::string> Who = PoliceFile::WhoSheAsks(Mill, Cast, &Now);
			PoliceFile::Asked(Mill, &Who, Why, Now);
			return Why;
		}

		/// 10:00, if he is not held: a constable (ROUTE.md step 6). The
		/// custody taken, or none. `Area` is where he stands.
		std::shared_ptr<Custody> TenConstable(GossipMill* Mill, const CastDay* Cast, const GameTime& Now, const std::string& Area,
		                                      bool bOwnsUp = false, bool bInTheCoat = false)
		{
			if (Now.Hour != 10 || Holding(Now)) return nullptr;
			std::string Topic;
			if (!Police.ConstableComes(Now.Day, Topic, &Now)) return nullptr;
			std::shared_ptr<Custody> C = Police.TakeIn(&Topic, Now, bOwnsUp, bInTheCoat);
			if (!C) return nullptr;
			Custody::SeenTaken(Mill, Cast, Area, Now);
			Arrests.push_back(C);
			if (TakenFirst == "no") TakenFirst = "day " + std::to_string(Now.Day + 1) + ", " + CustodyEndName(C->End());
			return C;
		}

		/// 10:00 on the tea's day: Ada's invitation line, once.
		bool TenTea(const GameTime& Now, std::string& Out)
		{
			return Tea && Now.Day == Tea->Day() && Now.Hour == 10 && Tea->SheSeesHim(Now, Out);
		}

		/// 20:00 on an ask night: Ron at the door with the envelope.
		bool TwentyRon(GossipMill* Mill, const GameTime& Now)
		{
			if (Now.Hour != 20 || !Asks.AsksOn(Now.Day) || Mill == nullptr) return false;
			const GossiperPtr Ron = Mill->Get("rocco");
			return Asks.Delivered(Now.Day, Ron.get(), &Now);
		}

		/// 23:00 on the tea's day: her tea closed, however it went.
		void TwentyThreeTea(GossipMill* Mill, const GameTime& Now)
		{
			if (!Tea || Now.Day != Tea->Day() || Now.Hour != 23 || Mill == nullptr) return;
			const GossiperPtr Ada = Mill->Get(AdasTea::Ada);
			Tea->Close(Ada.get(), Now);
		}

		/// Every hour, last: the week's end closed, then the town's talk.
		/// The rounds run up to RoundsUpTo when given (the reference week: the
		/// hour's end), or to Now (the game, whose rounds follow its minutes).
		void HourEnd(GossipMill* Mill, const CastDay* Cast, const GameTime& Now, const GameTime* RoundsUpTo = nullptr)
		{
			Week.Close(Now, Mill, Cast);
			Hours.RunTo(Mill, Cast, RoundsUpTo != nullptr ? *RoundsUpTo : Now);
		}

		// ---- what he does, between them ----

		/// His answer to the night's ask: the envelope at the landing, or a no.
		bool AnswerAsk(int Day, NightAnswer What, GossipMill* Mill, const GameTime& Now) { return Asks.Answer(Day, What, Mill, &Now); }
	};
}
