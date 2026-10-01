// TRANSLITERATION of ledger/Assets/Scripts/Core/TownRounds.cs (town list
// 6bs, 29 September): TownRounds.Hour, CatchUp, HourStart and FloorDiv, and
// TownHours with RunTo, ToJson and FromJson. Transliteration, not rewrite:
// every branch matches its source line for line. The mill's ageing
// (GossipMill::Age) and Weigh's SameStrength that the rounds rest on are in
// Gossip.h.
//
// ONE DIFFERENCE OF FORM, NOT OF BEHAVIOUR: the cast is a template parameter,
// anything with Together(a, b, day, hour) and MickeysOwn(id) as CastDay.h has
// them (Hour and RunTo set the mill's KeepsHisDeedsFor from it, 1 October). The golden
// rows pass a CastDay; the game's mill knows Sheila, Darren and Ron by the
// probe's own ids (w1, n2, r3), so the game passes a CastDay that reads them
// as the cast file's (lena, sam, rocco).
//
// No Unreal type is in this file (the standing rule from 25 August):
// ue-probe/tests/core-port-test.cpp checks it against the C#'s table.
#pragma once

#include <cmath>
#include <functional>
#include <string>
#include <utility>
#include <vector>

#include "GameTime.h"
#include "Gossip.h"
#include "MiniJson.h"

namespace LedgerCore
{
	/// THE TOWN TALKS BY ITS ROUTINES. Every figure the first hour rests on
	/// comes from rounds run by the cast's routines: whoever is together by
	/// their routines this hour talks, six minutes a round, and the mill ages
	/// each hour. The game ran rounds only between people standing near each
	/// other on the street in front of him, so nobody off Quay Street talked,
	/// and nobody at all while he slept or sat in the cells. So: the game keeps
	/// one TownHours and calls its RunTo as each game hour starts (and after a
	/// load), which runs every hour not yet run, once, the hour now with the
	/// street as it stands (OnStreet, the people the game has walking there,
	/// whose rounds are its own by distance) and any hours skipped with nobody
	/// on it. A round passes stories only between the pairs it is given, so
	/// the game's rounds and these never tell the same pair twice; the ageing
	/// is here, once an hour, and nowhere else.
	namespace TownRounds
	{
		/// Game minutes between two rounds, as TownReach has always run them.
		constexpr int MinutesBetweenRounds = 6;

		/// The most hours one catch-up runs: two weeks. A longer gap (a save
		/// edited by hand, a clock set wrong) runs its last two weeks.
		constexpr int LongestCatchUpHours = 14 * 24;

		typedef std::function<bool(const std::string&)> OnStreetFn;

		inline long long FloorDiv(long long A, long long B) { return A >= 0 ? A / B : -((-A + B - 1) / B); }

		/// MICKEY'S OWN HANDLE IT PRIVATELY (Jafar, 1 October): the mill's
		/// KeepsHisDeedsFor set from the cast whenever the town's rounds run with
		/// it, as TownRounds.cs Hour and RunTo set it to cast.MickeysOwn (TCast
		/// has MickeysOwn(id) as CastDay.h has it). The function holds the cast
		/// as the C#'s delegate does, by reference, and the mill keeps it after
		/// the call, so THE CAST MUST LIVE AS LONG AS THE MILL TALKS: the game
		/// passes its own cast for the run (GCast, and the street's adapter of
		/// it, which lives as long), never one made for a single call.
		template <class TCast>
		void KeepHisDeeds(GossipMill* Mill, const TCast* Cast)
		{
			Mill->KeepsHisDeedsFor = [Cast](const std::string& Id) { return Cast->MickeysOwn(Id); };
		}

		/// The start of an hour counted from day 0's midnight, days rounded
		/// down (so hour -1 is the day before's eleven o'clock).
		inline GameTime HourStart(long long H)
		{
			const long long Day = FloorDiv(H, 24);
			return GameTime((int)Day, (int)(H - Day * 24), 0);
		}

		/// ONE GAME HOUR OF THE TOWN'S TALK from HourStartAt (its minutes are
		/// ignored): the rounds by the routines for every pair the street does
		/// not hold, then the hour's ageing. Returns how many stories passed.
		template <class TCast>
		int Hour(GossipMill* Mill, const TCast* Cast, const GameTime& HourStartAt, const OnStreetFn& OnStreet = OnStreetFn())
		{
			if (Mill == nullptr || Cast == nullptr) return 0;
			KeepHisDeeds(Mill, Cast);   // Mickey's own handle it privately (Jafar, 1 October)
			const int Day = HourStartAt.Day, H = HourStartAt.Hour;
			int Passed = 0;
			for (int M = 0; M < 60; M += MinutesBetweenRounds)
			{
				Passed += (int)Mill->Tick(GameTime(Day, H, M),
					[&OnStreet, Cast, Day, H](const std::string& A, const std::string& B)
					{ return !(OnStreet && OnStreet(A) && OnStreet(B)) && Cast->Together(A, B, Day, H); }).size();
			}
			Mill->Age(GameTime(Day, H, 0).AddMinutes(60));
			return Passed;
		}

		/// EVERY HOUR SKIPPED, from the hour From falls in up to (not
		/// including) the hour To falls in, as Hour does each, with nobody on
		/// the street: a night asleep, a spell in the cells, the time a load
		/// jumps. Returns how many hours ran.
		template <class TCast>
		int CatchUp(GossipMill* Mill, const TCast* Cast, const GameTime& From, const GameTime& To)
		{
			if (Mill == nullptr || Cast == nullptr) return 0;
			long long First = FloorDiv(From.TotalMinutes(), 60);
			const long long Last = FloorDiv(To.TotalMinutes(), 60);
			if (Last - First > LongestCatchUpHours) First = Last - LongestCatchUpHours;
			int Ran = 0;
			for (long long H = First; H < Last; H++, Ran++)
			{
				Hour(Mill, Cast, HourStart(H));
			}
			return Ran;
		}
	}

	/// THE HOURS THE TOWN HAS TALKED (an hour run twice, after a reload or a
	/// missed check, told the same pairs twice and aged twice). One per game,
	/// saved with the town.
	class TownHours
	{
		long long NextRoundValue = -1;
	public:
		/// The first round not yet run, in minutes from day 0's midnight; -1 before any.
		long long NextRound() const { return NextRoundValue; }
		/// The hour it falls in; -1 before any.
		long long NextHour() const { return NextRoundValue < 0 ? -1 : TownRounds::FloorDiv(NextRoundValue, 60); }

		/// AS GAME TIME PASSES (TownRounds.cs RunTo, the review's A12 and B3):
		/// every round not yet run up to Now, once, each at its own minute and
		/// none before it; the hours before Now's with nobody on the street, the
		/// hour now with OnStreet; the mill aged as each hour starts. While the
		/// game runs its own street it calls this at least once a round (every
		/// six game minutes) or oftener, and asked each round or each minute the
		/// town ends the same; whole hours gone by count as time the street did
		/// not run (the second independent check). Returns how many rounds ran.
		template <class TCast>
		int RunTo(GossipMill* Mill, const TCast* Cast, const GameTime& Now, const TownRounds::OnStreetFn& OnStreet = TownRounds::OnStreetFn())
		{
			if (Mill == nullptr || Cast == nullptr) return 0;
			TownRounds::KeepHisDeeds(Mill, Cast);   // Mickey's own handle it privately (Jafar, 1 October)
			const int Step = TownRounds::MinutesBetweenRounds;
			const long long NowM = Now.TotalMinutes();
			const long long HourNowStart = TownRounds::FloorDiv(NowM, 60) * 60;
			const long long LastRound = TownRounds::FloorDiv(NowM, Step) * Step;
			const bool bFirstCall = NextRoundValue == -1;   // a round before day 0 is a round (the builder's check)
			if (bFirstCall) NextRoundValue = HourNowStart;
			if (LastRound < NextRoundValue) return 0;
			// The mill's ageing clock is not in the save: started again at the
			// hour the last round ran in (the second independent check: from the
			// next round's, a save after a call at xx:54 to xx:59 lost an hour's
			// fading); on the first call, not at all.
			if (!bFirstCall) Mill->Age(AtMinute(TownRounds::FloorDiv(NextRoundValue - Step, 60) * 60));
			const long long Earliest = HourNowStart - TownRounds::LongestCatchUpHours * 60LL;
			if (NextRoundValue < Earliest) NextRoundValue = Earliest;
			int Ran = 0;
			for (long long R = NextRoundValue; R <= LastRound; R += Step, ++Ran)
			{
				const GameTime At = AtMinute(R);
				if (R % 60 == 0) Mill->Age(At);
				const bool bStreet = R >= HourNowStart && (bool)OnStreet;
				const int Day = At.Day, Hour = At.Hour;
				Mill->Tick(At, [&OnStreet, bStreet, Cast, Day, Hour](const std::string& A, const std::string& B)
					{ return !(bStreet && OnStreet(A) && OnStreet(B)) && Cast->Together(A, B, Day, Hour); });
			}
			NextRoundValue = LastRound + Step;
			return Ran;
		}

		/// A minute counted from day 0's midnight, days floored (TownRounds.cs At):
		/// before day 0 is the day before's, never a negative hour.
		static GameTime AtMinute(long long M)
		{
			const long long Day = TownRounds::FloorDiv(M, 24 * 60), Rem = M - Day * 24 * 60;
			return GameTime((int)Day, (int)(Rem / 60), (int)(Rem % 60));
		}

		/// {"next": the hour, as the C#'s MiniJson writes a double that is whole}.
		std::string ToJson() const { return "{\"next\":" + std::to_string(NextHour()) + ",\"round\":" + std::to_string(NextRoundValue) + "}"; }

		/// The C#'s FromJson: "next" a number from -1 to under 1e7 and whole,
		/// or else -1.
		static TownHours FromJson(const std::string& Saved)
		{
			LedgerVignette::Value Parsed;
			std::string Err;
			if (!MiniJson::Deserialize(Saved, Parsed, Err) || Parsed.Type != LedgerVignette::T_OBJ) return TownHours();
			return FromValue(&Parsed);
		}

		/// The same from a value already read; none, or no object, is a fresh one.
		static TownHours FromValue(const LedgerVignette::Value* RootP)
		{
			TownHours T;
			if (RootP == nullptr || RootP->Type != LedgerVignette::T_OBJ) return T;
			const LedgerVignette::Value& Root = *RootP;
			// The reader keeps a key given twice once, with its last value, as
			// the C#'s dictionary does.
			// "round" (minutes, a whole round or -1) first; else an old save's "next" (the hour's start).
			const LedgerVignette::Value* Round = nullptr;
			const LedgerVignette::Value* NextV = nullptr;
			for (std::vector<std::pair<std::string, LedgerVignette::Value> >::size_type I = 0; I < Root.Obj.size(); ++I)
			{
				if (Root.Obj[I].first == "round") Round = &Root.Obj[I].second;
				else if (Root.Obj[I].first == "next") NextV = &Root.Obj[I].second;
			}
			if (Round != nullptr && Round->Type == LedgerVignette::T_NUM && Round->Num > -6e8 && Round->Num < 6e8 && Round->Num == std::floor(Round->Num)
			    && (Round->Num == -1 || std::fmod(Round->Num, (double)TownRounds::MinutesBetweenRounds) == 0))
				T.NextRoundValue = (long long)Round->Num;
			else if (NextV != nullptr && NextV->Type == LedgerVignette::T_NUM && NextV->Num >= -1 && NextV->Num < 1e7 && NextV->Num == std::floor(NextV->Num))
				T.NextRoundValue = NextV->Num < 0 ? -1 : (long long)NextV->Num * 60;
			return T;
		}
	};
}
