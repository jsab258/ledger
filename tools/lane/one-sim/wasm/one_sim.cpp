// ONE SIMULATION IN THE BROWSER: the front door (first slice, 19 November 2026).
//
// This file holds NO town rule. Every rule it runs is the game's own C++ port,
// included from ue-probe/Source/LedgerProbe/Public exactly as the Unreal module
// and the port's golden test include it. This file only lets JavaScript call
// those rules: make a town from a cast file, run a game hour in the game's own
// order (TownWeek::RunHour), do what the player does between hours, and read
// the state back as text.
//
// Two builds come from this one file (tools/lane/one-sim/one-sim.sh wasm):
//   one-sim.wasm        the brain a page would load;
//   one-sim-check.wasm  the same, plus the port's golden reader (CoreGolden.h),
//                       so a test can ask it any row of the C# Core's table.
//                       Never shipped: it is the proof, not the product.
//
// Text in, text out. A returned pointer stays good until the next call.
// Days count from 0 (Monday of the first week), hours 0 to 23, as GameTime does.
// A call with no town yet, or with a time that is no time (a day before the first, an hour
// outside 0 to 23, a minute outside 0 to 59), does nothing and answers empty, 0 or -1.

#include "CastDay.h"
#include "Gossip.h"
#include "MemoryStore.h"
#include "TownWeek.h"

#ifdef ONE_SIM_CHECK
#include "CoreGolden.h"
#endif

#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <map>
#include <memory>
#include <string>
#include <utility>
#include <vector>

using namespace LedgerCore;

#define OS_EXPORT(Name) __attribute__((export_name(#Name)))

namespace
{
	struct FTown
	{
		CastDay Cast;
		std::shared_ptr<SocialGraph> Graph;
		std::unique_ptr<GossipMill> Mill;
		std::unique_ptr<TownWeek> Week;
	};

	std::unique_ptr<FTown> gTown;
	std::string gOut, gErr;

	const char* Out(const std::string& S) { gOut = S; return gOut.c_str(); }
	std::string Int(long long V) { char B[32]; std::snprintf(B, sizeof(B), "%lld", V); return B; }
	std::string Bit(bool B) { return B ? "1" : "0"; }
	// The golden table's own escaping (CoreGolden.h Escape), so a row made here reads as a row made there.
	std::string Esc(const std::string& S)
	{
		std::string O;
		for (char C : S) { if (C == ' ') O += '~'; else if (C == '\n') O += '^'; else if (C == '\r') {} else if (C == '|') O += '!'; else O += C; }
		return O;
	}
	std::string Str(const char* P) { return P ? std::string(P) : std::string(); }
	// A text as JSON writes it: quotes, backslashes and control characters escaped.
	std::string Json(const std::string& S)
	{
		std::string O = "\"";
		for (unsigned char C : S)
		{
			if (C == '"') O += "\\\"";
			else if (C == '\\') O += "\\\\";
			else if (C == '\n') O += "\\n";
			else if (C == '\r') O += "\\r";
			else if (C == '\t') O += "\\t";
			else if (C < 0x20) { char B[8]; std::snprintf(B, sizeof(B), "\\u%04x", (unsigned)C); O += B; }
			else O += (char)C;
		}
		return O + "\"";
	}
	GameTime At(int Day, int Hour, int Minute) { return GameTime(Day, Hour, Minute); }
	// A time the game's clock could show. The door refuses anything else, so no rule is asked about a time that is none.
	bool Time(int Day, int Hour, int Minute = 0) { return Day >= 0 && Hour >= 0 && Hour <= 23 && Minute >= 0 && Minute <= 59; }

	// "sam:4,ron:2" -> who saw it and at what rung.
	std::vector<std::pair<std::string, int> > Saw(const std::string& S)
	{
		std::vector<std::pair<std::string, int> > V;
		std::string::size_type I = 0;
		while (I < S.size())
		{
			std::string::size_type E = S.find(',', I);
			if (E == std::string::npos) E = S.size();
			const std::string One = S.substr(I, E - I);
			const std::string::size_type C = One.find(':');
			if (!One.empty()) V.push_back(std::make_pair(One.substr(0, C), C == std::string::npos ? -1 : std::atoi(One.c_str() + C + 1)));
			I = E + 1;
		}
		return V;
	}

#ifdef ONE_SIM_CHECK
	std::map<std::string, std::string>& CastTexts() { static std::map<std::string, std::string> M; return M; }
	bool ReadCastFromHost(const std::string& Name, std::string& Text)
	{
		const std::map<std::string, std::string>::const_iterator It = CastTexts().find(Name);
		if (It == CastTexts().end()) return false;
		Text = It->second;
		if (Text.size() >= 3 && (unsigned char)Text[0] == 0xEF && (unsigned char)Text[1] == 0xBB && (unsigned char)Text[2] == 0xBF) Text.erase(0, 3);
		return true;
	}
#endif
}

extern "C"
{
	// ---- text passing -------------------------------------------------------
	OS_EXPORT(os_alloc) char* os_alloc(int Bytes) { return (char*)std::malloc(Bytes > 0 ? (size_t)Bytes : 1); }
	OS_EXPORT(os_free) void os_free(char* P) { std::free(P); }
	OS_EXPORT(os_error) const char* os_error() { return gErr.c_str(); }
	OS_EXPORT(os_version) const char* os_version()
	{
#ifdef ONE_SIM_CHECK
		return "one-sim 1 (check build: the game's port plus its golden reader)";
#else
		return "one-sim 1 (the game's port, ue-probe/Source/LedgerProbe/Public)";
#endif
	}

	// ---- the town -----------------------------------------------------------
	/// A new town from a cast file's text (production/specs/hook-cast.json or
	/// quay-cast.json): the people, their ties, each with an empty memory, and a
	/// fresh week. Built as the port's own week rows build it. 1, or 0 with os_error.
	OS_EXPORT(os_town_new) int os_town_new(const char* CastJson)
	{
		std::unique_ptr<FTown> T(new FTown());
		std::string Text = Str(CastJson), Err;
		if (Text.size() >= 3 && (unsigned char)Text[0] == 0xEF && (unsigned char)Text[1] == 0xBB && (unsigned char)Text[2] == 0xBF) Text.erase(0, 3);
		if (!CastDay::Parse(Text, T->Cast, Err)) { gErr = "cast not read: " + Err; return 0; }
		T->Graph = std::make_shared<SocialGraph>();
		for (const CastDay::Tie& Tie : T->Cast.Ties()) T->Graph->Link(Tie.A, Tie.B, Tie.W);
		T->Mill.reset(new GossipMill(T->Graph));
		for (const std::string& P : T->Cast.People())
			T->Mill->Add(std::make_shared<Gossiper>(P, P, std::make_shared<MemoryStore>(P), std::make_shared<KnowledgeBase>(), T->Cast.CircleOf(P)));
		T->Week.reset(new TownWeek());
		gTown = std::move(T);
		gErr.clear();
		return 1;
	}

	/// The people of the cast, comma separated.
	OS_EXPORT(os_people) const char* os_people()
	{
		if (!gTown) return Out("");
		std::string S;
		for (const std::string& P : gTown->Cast.People()) S += (S.empty() ? "" : ",") + P;
		return Out(S);
	}

	/// ROUTINES: where a person is at an hour of a day (CastDay::PlaceOf).
	OS_EXPORT(os_place_of) const char* os_place_of(const char* Person, int Day, int Hour)
	{
		if (!gTown) return Out("");
		return Out(gTown->Cast.PlaceOf(Str(Person), Day, Hour));
	}

	/// The town's talk aged to a moment (GossipMill::Age), as a week's first hour does.
	OS_EXPORT(os_age) void os_age(int Day, int Hour, int Minute) { if (gTown && Time(Day, Hour, Minute)) gTown->Mill->Age(At(Day, Hour, Minute)); }

	/// ONE GAME HOUR, the scheduled steps in the game's order (TownWeek::RunHour).
	/// Returns thirteen fields joined by '|', the same thirteen, in the same
	/// words, as the C# Core's TownWeekHour golden rows: who found the damage,
	/// who went to the police, why DS Ellis came, the custody taken, Ada's
	/// invitation, Ron's envelope, the tea's state, held or not, the asks, what
	/// the outfit's man holds, how many stories the town holds, her first
	/// visit, his first arrest.
	OS_EXPORT(os_hour) const char* os_hour(int Day, int Hour, const char* Area)
	{
		if (!gTown || !Time(Day, Hour)) return Out("");
		TownWeek& W = *gTown->Week;
		GossipMill& Mill = *gTown->Mill;
		const GameTime Now = At(Day, Hour, 0);
		const TownWeek::HourDone Done = W.RunHour(&Mill, &gTown->Cast, Now, Str(Area));
		std::string FoundS, WentS, Nights, Outfit;
		for (const auto& Fd : Done.Found) FoundS += (FoundS.empty() ? "" : ",") + Fd.first + "@" + Int(Fd.second.TotalMinutes());
		for (const std::string& Wh : Done.Went) WentS += (WentS.empty() ? "" : ",") + Wh;
		for (const auto& Kv : W.Asks.Nights()) Nights += (Nights.empty() ? "" : ",") + Int(Kv.first) + "=" + Arrangement::Value(Kv.second);
		const GossiperPtr Man = Mill.Get(Arrangement::OutfitMan);
		if (Man)
		{
			for (const RumorPtr& R : Man->Rumors)
				if (R && R->TopicKey().compare(0, 15, "player.outfit_d") == 0) Outfit += (Outfit.empty() ? "" : ",") + R->Content.Predicate + "=" + R->Content.Value;
		}
		long long Stories = 0;
		for (const GossiperPtr& G : Mill.Agents()) { if (G) Stories += (long long)G->Rumors.size(); }
		std::string Row = (FoundS.empty() ? "-" : FoundS);
		Row += "|" + (WentS.empty() ? std::string("-") : WentS);
		Row += "|" + (Done.Why.empty() ? std::string("-") : Done.Why);
		Row += "|" + (Done.Taken ? std::string(CustodyEndName(Done.Taken->End())) : std::string("-"));
		Row += "|" + Bit(Done.bInvite);
		Row += "|" + Bit(Done.bRon);
		Row += "|" + std::string(TeaStateName(W.Tea->State()));
		Row += "|" + Bit(W.Holding(Now) != nullptr);
		Row += "|" + Esc(Int(W.Asks.NextNight()) + ";" + Nights + ";" + (W.Asks.Ended() ? W.Asks.EndedWhy() : std::string("stands")));
		Row += "|" + (Outfit.empty() ? std::string("-") : Outfit);
		Row += "|" + Int(Stories);
		Row += "|" + Esc(W.EllisFirst);
		Row += "|" + Esc(W.TakenFirst);
		return Out(Row);
	}

	// ---- what the player does, between the hours ----------------------------
	/// The town's talk run up to a moment (before something he does at a minute).
	OS_EXPORT(os_rounds_to) void os_rounds_to(int Day, int Hour, int Minute)
	{
		if (gTown && Time(Day, Hour, Minute)) gTown->Week->RoundsTo(gTown->Mill.get(), &gTown->Cast, At(Day, Hour, Minute));
	}

	/// THE DEED: the damage kept, and each witness ("sam:4,ron:2", id and the
	/// rung they saw him at) holding the story first-hand. Then whoever is in
	/// the area finds it at once (TownWeek::DamageTick), as the game does.
	OS_EXPORT(os_deed) void os_deed(int Day, int Hour, int Minute, const char* Area, const char* Thing, const char* Said,
	                                const char* Witnesses, const char* StoryFact, const char* StorySaid, double Certainty)
	{
		if (!gTown || !Time(Day, Hour, Minute)) return;
		const GameTime When = At(Day, Hour, Minute);
		gTown->Week->Deed(gTown->Mill.get(), When, Str(Area), Str(Thing), Str(Said), Saw(Str(Witnesses)), Str(StoryFact), Str(StorySaid), Certainty);
		gTown->Week->DamageTick(gTown->Mill.get(), &gTown->Cast, When);
	}

	/// His answer to a night's ask: 0 the envelope handed over, 1 a no, 2 no show, 3 never reached.
	OS_EXPORT(os_answer_ask) int os_answer_ask(int AskDay, int What, int Day, int Hour, int Minute)
	{
		if (!gTown || What < 0 || What > 3 || AskDay < 0 || !Time(Day, Hour, Minute)) return 0;
		return gTown->Week->AnswerAsk(AskDay, (NightAnswer)What, gTown->Mill.get(), At(Day, Hour, Minute)) ? 1 : 0;
	}
	OS_EXPORT(os_asks_on) int os_asks_on(int Day) { return gTown && gTown->Week->Asks.AsksOn(Day) ? 1 : 0; }
	OS_EXPORT(os_ask_delivered) int os_ask_delivered(int Day) { return gTown && gTown->Week->Asks.WasDelivered(Day) ? 1 : 0; }

	/// Ada's tea: its day, and a minute he spends with her.
	OS_EXPORT(os_tea_day) int os_tea_day() { return gTown ? gTown->Week->Tea->Day() : -1; }
	OS_EXPORT(os_tea_with_her) void os_tea_with_her(int Day, int Hour, int Minute) { if (gTown && Time(Day, Hour, Minute)) gTown->Week->Tea->WithHer(At(Day, Hour, Minute)); }

	/// The week's end: its day, whether Sheila asks now, her question put, and
	/// his answer (1 wind it down, 2 take it over, 3 won't say).
	OS_EXPORT(os_week_day) int os_week_day() { return gTown ? gTown->Week->Week.Day() : -1; }
	OS_EXPORT(os_week_asks_now) int os_week_asks_now(int Day, int Hour, int Minute, int AtOffice)
	{
		return gTown && Time(Day, Hour, Minute) && gTown->Week->Week.AsksNow(At(Day, Hour, Minute), AtOffice != 0) ? 1 : 0;
	}
	OS_EXPORT(os_week_ask) int os_week_ask(int Day, int Hour, int Minute) { return gTown && Time(Day, Hour, Minute) && gTown->Week->Week.Ask(At(Day, Hour, Minute), true) ? 1 : 0; }
	OS_EXPORT(os_week_give) int os_week_give(int Answer, int Day, int Hour, int Minute)
	{
		if (!gTown || Answer < 0 || Answer > 3 || !Time(Day, Hour, Minute)) return 0;
		return gTown->Week->Week.Give((WeekAnswer)Answer, At(Day, Hour, Minute), gTown->Mill.get(), &gTown->Cast, &gTown->Week->Asks) ? 1 : 0;
	}

	/// The police file: a report filed by hand (offence 0 suspicious, 1 damage,
	/// 2 assault, 3 wounding, 4 robbery, 5 killing), and him taken in for a topic.
	OS_EXPORT(os_police_report) int os_police_report(const char* Who, const char* Topic, int Offence_, int Rung, int Day)
	{
		if (!gTown || Offence_ < 0 || Offence_ > 5 || Day < 0) return 0;
		return gTown->Week->Police.Report(Str(Who), Str(Topic), (Offence)Offence_, Rung, Day) ? 1 : 0;
	}
	OS_EXPORT(os_take_in) int os_take_in(const char* Topic, int Day, int Hour, int Minute)
	{
		if (!gTown || !Time(Day, Hour, Minute)) return 0;
		const std::string T = Str(Topic);
		const std::shared_ptr<Custody> C = gTown->Week->Police.TakeIn(&T, At(Day, Hour, Minute), false, false);
		gTown->Week->Arrests.push_back(C);
		return C ? 1 : 0;
	}

	// ---- reading the town back ----------------------------------------------
	/// The week's state as the game's own save pieces write it (each piece's
	/// own ToJson, the ones TownSave bundles), as one JSON text.
	OS_EXPORT(os_state) const char* os_state()
	{
		if (!gTown) return Out("{}");
		const TownWeek& W = *gTown->Week;
		std::string J = "{\"asks\":" + W.Asks.ToJson() + ",\"police\":" + W.Police.ToJson();
		if (W.Tea) J += ",\"tea\":" + W.Tea->ToJson();
		J += ",\"damage\":[";
		for (size_t I = 0; I < W.Damage.size(); ++I) J += (I ? "," : "") + W.Damage[I].ToJson();
		J += "],\"arrests\":[";
		bool bFirst = true;
		for (const auto& C : W.Arrests) { if (C) { J += (bFirst ? "" : ",") + C->ToJson(); bFirst = false; } }
		J += "],\"hours\":" + W.Hours.ToJson() + ",\"week\":" + W.Week.ToJson() + "}";
		return Out(J);
	}

	/// WHO HOLDS WHAT: one line a person, "id: topic=predicate=value; ...", the
	/// stories each holds, in the order they hold them. What a Ledger screen
	/// would be drawn from.
	OS_EXPORT(os_stories) const char* os_stories()
	{
		if (!gTown) return Out("");
		std::string S;
		for (const GossiperPtr& G : gTown->Mill->Agents())
		{
			if (!G) continue;
			S += G->Id + ":";
			for (const RumorPtr& R : G->Rumors) { if (R) S += " " + R->TopicKey() + "=" + R->Content.Value + ";"; }
			S += "\n";
		}
		return Out(S);
	}

	/// THE LEDGER'S FACTS: who knows what, and how. A JSON list, one entry for
	/// each person and each story they hold: "who"; "topic" and "value" (the
	/// story); "saw" (true: they witnessed it themselves; false: they were
	/// told); "hops" (how many tellings from the one who saw it); "from" (who
	/// first saw it); "rung" (how well that first witness saw the man: 0
	/// someone, 1 a silhouette, 2 a mark, 3 a face, 4 recognised; -1 when the
	/// story is no sighting); "names" (whether the story names him); "sure" (0
	/// to 1, null if it is no number); "private" (about his hidden life);
	/// "said" (the story's words). Nothing is worked out here: every field is
	/// the port's own Rumor, read as it stands.
	OS_EXPORT(os_knows) const char* os_knows()
	{
		if (!gTown) return Out("[]");
		std::string J = "[";
		bool bFirst = true;
		for (const GossiperPtr& G : gTown->Mill->Agents())
		{
			if (!G) continue;
			for (const RumorPtr& R : G->Rumors)
			{
				if (!R) continue;
				char Sure[40];
				if (std::isfinite(R->Confidence)) std::snprintf(Sure, sizeof(Sure), "%.6f", R->Confidence);
				else std::snprintf(Sure, sizeof(Sure), "null");
				J += bFirst ? "" : ",";
				J += "{\"who\":" + Json(G->Id) + ",\"topic\":" + Json(R->TopicKey()) + ",\"value\":" + Json(R->Content.Value);
				J += std::string(",\"saw\":") + (R->Hops == 0 ? "true" : "false") + ",\"hops\":" + Int(R->Hops) + ",\"from\":" + Json(R->OriginId);
				J += ",\"rung\":" + Int(R->OriginRung) + ",\"names\":" + (R->NamesHim() ? "true" : "false") + ",\"sure\":" + Sure;
				J += std::string(",\"private\":") + (R->Sensitive ? "true" : "false") + ",\"said\":" + Json(R->Summary) + "}";
				bFirst = false;
			}
		}
		return Out(J + "]");
	}

#ifdef ONE_SIM_CHECK
	// ---- the proof (check build only) ---------------------------------------
	/// A cast file's text by name, for the golden rows that name one. The page
	/// has no files, so the host hands the text in.
	OS_EXPORT(os_check_cast_file) void os_check_cast_file(const char* Name, const char* Text)
	{
		CastTexts()[Str(Name)] = Str(Text);
		Golden::CastFileReader() = &ReadCastFromHost;
	}

	/// ONE ROW OF THE C# CORE'S GOLDEN TABLE, asked of this build: the row's
	/// whole text in ("Rule|arg|...|expected"), and back "ok", "skip:<kind>"
	/// (the named holes: the unported claims rows, the rows that need
	/// exceptions), "short", "unknown", or "MISMATCH got=<answer>".
	/// The comparison is the port test's own (ue-probe/tests/core-port-test.cpp):
	/// numbers to 1e-9, everything else exactly.
	OS_EXPORT(os_check_row) const char* os_check_row(const char* Line)
	{
		using namespace LedgerCore::Golden;
		const std::vector<std::string> F = SplitPipe(Str(Line));
		if (F.size() < FewestFields) return Out("short");
		const std::string Kind = SkipKind(F);
		if (!Kind.empty()) return Out("skip:" + Kind);
		const Answer A = Evaluate(F);
		if (!A.Known) return Out("unknown");
		if (Agrees(A.Got, F[F.size() - 1], 1e-9)) return Out("ok");
		return Out("MISMATCH got=" + A.Got);
	}
#endif
}
