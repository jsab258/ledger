// TRANSLITERATION of ledger/Assets/Scripts/Core/WeeksEnd.cs, 30 September
// (the town's handover 6ca, "Sheila's trust and the week's end";
// production/handovers/6ca-sheila-and-the-week.md).
//
// THE WEEK'S END: from the week's seventh day, the first time he talks with
// her at the office Sheila puts the question, "So which is it going to be?",
// over Mickey's real book if she trusts him and the day-book if not. On a
// Sunday, her day off, she waits at the office from ten till twelve, and
// once she has asked, till six. His plain answer (wind it down, take it over,
// or won't say) is filed as the street's story, first-hand for her and for
// anybody the cast has where she is; a day she asked that ends unanswered is
// his refusal to say. Winding it down ends Mickey's arrangement that night.
//
// NOT HERE: Sounds and Confirms, the reading of his line as an answer, which
// the talk program does; the game hears the result.
//
// TRANSLITERATION, NOT REWRITE, as Gossip.h states the method: the C#'s
// nullable GameTime is a bool beside a value here. Checked against
// PerceptionGolden's EmitWeeksEnd rows (WeekAsk, WeekFiled, RecognitionWeek,
// WeekShows, RecognitionOutfitWound) in ue-probe/perception-golden.txt.
//
// NO UNREAL TYPE IS IN THIS FILE, as every file of the port.
#pragma once

#include "Arrangement.h"
#include "CastDay.h"
#include "GameTime.h"
#include "Gossip.h"
#include "MemoryStore.h"
#include "MiniJson.h"

#include <cmath>
#include <string>

namespace LedgerCore
{
	/// His answer to Sheila's question at the week's end.
	enum class WeekAnswer { None, WindDown, TakeOver, WontSay };

	inline const char* WeekAnswerName(WeekAnswer A)
	{
		switch (A)
		{
		case WeekAnswer::WindDown: return "WindDown";
		case WeekAnswer::TakeOver: return "TakeOver";
		case WeekAnswer::WontSay: return "WontSay";
		default: return "None";
		}
	}

	class WeeksEnd
	{
	public:
		static constexpr const char* Sheila = "lena";
		static constexpr int After = 6;
		static constexpr int WaitFrom = 10, WaitUntil = 12;
		static constexpr int StayUntil = 18;
		static constexpr const char* Office = "mickeys_office";
		static constexpr const char* Question = "So which is it going to be?";
		static constexpr const char* StillAsks = "You heard me. Wind it down, take it over, or won't you say?";
		static constexpr const char* TopicPrefix = "player.week_d";

		explicit WeeksEnd(int InFirstDay = 0) : FirstDayValue(InFirstDay > 0 ? InFirstDay : 0) {}

		int FirstDay() const { return FirstDayValue; }
		/// The day she first asks.
		int Day() const { return FirstDayValue + After; }
		bool AskedAt(GameTime& Out) const { if (!bAsked) return false; Out = AskedAtValue; return true; }
		bool RealBook() const { return bRealBook; }
		WeekAnswer Answer() const { return AnswerValue; }
		bool AnsweredAt(GameTime& Out) const { if (!bAnsweredAt) return false; Out = AnsweredAtValue; return true; }
		bool Answered() const { return AnswerValue != WeekAnswer::None; }

		static std::string Opening(bool bRealBook, bool bDayOff = false)
		{
			return std::string(bDayOff ? "I don't come in Sundays. " : "") + (bRealBook
				? "That's Mickey's real book. Everything he ran, in his own hand. You've had your week. " + std::string(Question)
				: "That's the day-book. The other one stays where it is. You've had your week. " + std::string(Question));
		}

		/// Her plain question back when his line sounds like an answer; empty for None.
		static std::string AskPlainly(WeekAnswer A, bool bArrangementEnded = false)
		{
			switch (A)
			{
			case WeekAnswer::WindDown: return bArrangementEnded
				? "Wind it down, then? A cab firm and nothing more, and Mickey's arrangements are finished already. Say yes and I'll close the book on it."
				: "Wind it down, then? Mickey's arrangements finished, and this a cab firm and nothing more. Say yes and I'll close the book on it.";
			case WeekAnswer::TakeOver: return bArrangementEnded
				? "Take it over, then? The office and the book, yours. Mickey's arrangements are finished, and that doesn't change. Say yes and it's your book."
				: "Take it over, then? Mickey's arrangements and everything that comes with them, yours. Say yes and it's your book.";
			case WeekAnswer::WontSay: return "You won't say, then? Say yes and I'll take that as your answer.";
			default: return std::string();
			}
		}

		static const char* Took(WeekAnswer A)
		{
			return A == WeekAnswer::WindDown ? "Right. I'll close the book on it."
			     : A == WeekAnswer::TakeOver ? "Right. Then it's your book."
			     : A == WeekAnswer::WontSay ? "Suit yourself. The street will decide for you, then." : "";
		}

		/// What the street says of it: the story's summary.
		static const char* Said(WeekAnswer A)
		{
			return A == WeekAnswer::WindDown ? "The new owner told Sheila he's winding Mickey's business down."
			     : A == WeekAnswer::TakeOver ? "The new owner told Sheila he's taking Mickey's business on, all of it."
			     : A == WeekAnswer::WontSay ? "Sheila asked the new owner what he means to do with Mickey's business, and he wouldn't say." : "";
		}

		/// What she remembers of it.
		static const char* Remembered(WeekAnswer A)
		{
			return A == WeekAnswer::WindDown ? "I asked Mickey's nephew, the new owner, which it was going to be, and he told me plainly: he's winding Mickey's business down."
			     : A == WeekAnswer::TakeOver ? "I asked Mickey's nephew, the new owner, which it was going to be, and he told me plainly: he's taking Mickey's business on, all of it."
			     : A == WeekAnswer::WontSay ? "I asked Mickey's nephew, the new owner, which it was going to be, and he wouldn't say." : "";
		}

		static bool IsWeekAnswer(const RumorPtr& R)
		{
			const std::string P = TopicPrefix;
			return R && R->Content.Subject == "player" && R->TopicKey().compare(0, P.size(), P) == 0;
		}

		static const char* Value(WeekAnswer A) { return A == WeekAnswer::WindDown ? "winddown" : A == WeekAnswer::TakeOver ? "takeover" : "wontsay"; }

		/// Whether she is at the office for him on the seventh day when it is a
		/// Sunday: ten till twelve, and once she has asked, while her question
		/// stands, till six.
		bool Waits(const GameTime& Now) const
		{
			if (Now.Day != Day() || CastDay::Weekday(Day()) != 6 || Now.Hour < WaitFrom) return false;
			if (Answered() || (bAsked && AskedAtValue.Day != Day())) return false;
			if (Now.Hour < WaitUntil) return true;
			return bAsked && Stands(Now) && Now.Hour < StayUntil;
		}

		/// Whether she puts the question now: true once, the turn she asks.
		bool Ask(const GameTime& Now, bool bInRealBook, bool bAtOffice = true)
		{
			if (bAsked || Now.Day < Day() || !bAtOffice) return false;
			bAsked = true;
			AskedAtValue = Now;
			bRealBook = bInRealBook;
			return true;
		}

		/// Whether the question stands at Now: asked, unanswered, the same day.
		bool Stands(const GameTime& Now) const
		{
			return bAsked && !Answered() && Now.Day == AskedAtValue.Day && Now.TotalMinutes() >= AskedAtValue.TotalMinutes();
		}

		/// His plain answer, given while the question stands; filed as the
		/// street's story and her memory. With the arrangement, winding it down
		/// ends it that night.
		bool Give(WeekAnswer A, const GameTime& Now, GossipMill* Mill, const CastDay* Cast, Arrangement* Asks = nullptr)
		{
			if (A == WeekAnswer::None || !Stands(Now)) return false;
			const bool bAtOffice = Waits(Now);
			AnswerValue = A;
			bAnsweredAt = true;
			AnsweredAtValue = Now;
			File(Mill, Cast, Now, bAtOffice);
			if (A == WeekAnswer::WindDown && Asks != nullptr) Asks->WoundDown(Now, Mill);
			return true;
		}

		/// The day she asked ended unanswered: his refusal to say, from midnight.
		bool Close(const GameTime& Now, GossipMill* Mill, const CastDay* Cast)
		{
			if (!bAsked || Answered() || Now.Day <= AskedAtValue.Day) return false;
			AnswerValue = WeekAnswer::WontSay;
			bAnsweredAt = true;
			AnsweredAtValue = GameTime(AskedAtValue.Day + 1, 0, 0);
			File(Mill, Cast, AnsweredAtValue, false, false);
			return true;
		}

		/// Her line for the talk while the question stands.
		static std::string StandingLine(bool bInRealBook)
		{
			return std::string("Today you put it to him, over ") + (bInRealBook ? "Mickey's real book" : "the day-book, the real one kept back")
				+ ", as you promised Mickey you would: which is it going to be? Wind Mickey's business down, take it over, or will he not say? "
				+ "Never answer it for him and never take a half answer for one; never say you will close the book or that it is his. "
				+ "If he dodges it, tell him you'll have his answer before the day's out.";
		}

		/// {"first", "asked" and "realBook" once asked, "answer" and "answered"
		/// once answered}, as MiniJson.Serialize writes the C#'s, in its order.
		std::string ToJson() const
		{
			std::string J = "{\"first\":" + std::to_string(FirstDayValue);
			if (bAsked) J += ",\"asked\":" + std::to_string(AskedAtValue.TotalMinutes()) + ",\"realBook\":" + (bRealBook ? "true" : "false");
			if (Answered() && bAnsweredAt) J += std::string(",\"answer\":\"") + WeekAnswerName(AnswerValue) + "\",\"answered\":" + std::to_string(AnsweredAtValue.TotalMinutes());
			return J + "}";
		}

		/// From ToJson's text, through Ask and Give (no mill); a fresh one for
		/// anything it cannot read. Text that is no JSON object is no save.
		static WeeksEnd FromJson(const std::string& SavedJson)
		{
			LedgerVignette::Value Parsed;
			std::string Err;
			if (!MiniJson::Deserialize(SavedJson, Parsed, Err) || Parsed.Type != LedgerVignette::T_OBJ) return WeeksEnd();
			return FromValue(&Parsed);
		}

		/// The same from a value already read; none, or no object, is a fresh one.
		static WeeksEnd FromValue(const LedgerVignette::Value* RootP)
		{
			if (RootP == nullptr || RootP->Type != LedgerVignette::T_OBJ) return WeeksEnd();
			const LedgerVignette::Value& Root = *RootP;
			const LedgerVignette::Value* F = Last(Root, "first");
			const int First = F != nullptr && F->Type == LedgerVignette::T_NUM && F->Num >= 0 && F->Num <= 100000 && F->Num == std::floor(F->Num) ? (int)F->Num : 0;
			WeeksEnd W(First);
			const LedgerVignette::Value* A = Last(Root, "asked");
			if (!(A != nullptr && A->Type == LedgerVignette::T_NUM && A->Num >= 0 && A->Num <= 1e8 && A->Num == std::floor(A->Num))) return W;
			const LedgerVignette::Value* Rb = Last(Root, "realBook");
			const bool bReal = Rb != nullptr && Rb->Type == LedgerVignette::T_BOOL && Rb->Bool;
			if (!W.Ask(GameTime::FromTotalMinutes((long long)A->Num), bReal)) return WeeksEnd(First);
			const LedgerVignette::Value* An = Last(Root, "answer");
			if (An == nullptr || An->Type != LedgerVignette::T_STR) return W;
			WeekAnswer Ans = WeekAnswer::None;
			bool bKnown = false;
			for (int I = 0; I <= (int)WeekAnswer::WontSay; ++I) { if (An->Str == WeekAnswerName((WeekAnswer)I)) { Ans = (WeekAnswer)I; bKnown = true; break; } }
			if (!bKnown) return W;
			const LedgerVignette::Value* T = Last(Root, "answered");
			if (!(T != nullptr && T->Type == LedgerVignette::T_NUM && T->Num >= 0 && T->Num <= 1e8 && T->Num == std::floor(T->Num))) return W;
			const GameTime When = GameTime::FromTotalMinutes((long long)T->Num);
			if (Ans == WeekAnswer::WontSay && When.Day > W.AskedAtValue.Day && When.Hour == 0 && When.Minute == 0) W.Close(When, nullptr, nullptr);
			else W.Give(Ans, When, nullptr, nullptr);
			return W;
		}

	private:
		int FirstDayValue;
		bool bAsked = false;
		GameTime AskedAtValue;
		bool bRealBook = false;
		WeekAnswer AnswerValue = WeekAnswer::None;
		bool bAnsweredAt = false;
		GameTime AnsweredAtValue;

		static const LedgerVignette::Value* Last(const LedgerVignette::Value& Obj, const char* Key)
		{
			const LedgerVignette::Value* Out = nullptr;
			for (const auto& Kv : Obj.Obj) { if (Kv.first == Key) Out = &Kv.second; }
			return Out;
		}

		// Filed once: her memory and the story, first-hand for her and for
		// anybody the cast has where she is then (never when the day closes
		// unanswered at midnight, when she is not there to be overheard).
		void File(GossipMill* Mill, const CastDay* Cast, const GameTime& At, bool bAtOffice, bool bOverheard = true)
		{
			if (Mill == nullptr) return;
			const Fact What("player", "week_d" + std::to_string(AskedAtValue.Day), Value(AnswerValue));
			const GossiperPtr She = Mill->Get(Sheila);
			if (She && She->Memory) She->Memory->Append(MemoryEvent(At, "conversation", 0.9, Remembered(AnswerValue)));
			Mill->Witness(Sheila, What, Said(AnswerValue), false, At, 1.0);
			// The day closing unanswered at midnight: she is not there to be
			// overheard. Said by the caller, never read from the clock (the port's
			// independent check, 30 September: a plain answer at 00:00 was heard
			// by Sheila alone).
			if (Cast == nullptr || !bOverheard) return;
			// Where she is when he answers: the office on her Sunday off, or her
			// routine's place; anywhere else, nobody overhears it. The C#'s null
			// area is kept apart from one named "".
			// Sheila not in the cast has no place (the C#'s null), so nobody
			// overhears; one-argument PlaceOf would give "", a place a cast may
			// name (the week's independent check, 30 September).
			std::string Place = Office, Area;
			if (!bAtOffice && !Cast->PlaceOf(Sheila, At.Day, At.Hour, Place)) return;
			if (!Cast->AreaOf(Place, Area)) return;
			for (const std::string& P : Cast->People())
			{
				std::string Theirs;
				if (P != Sheila && Cast->AreaOf(Cast->PlaceOf(P, At.Day, At.Hour), Theirs) && Theirs == Area)
					Mill->Witness(P, What, Said(AnswerValue), false, At, 1.0);
			}
		}
	};
}
