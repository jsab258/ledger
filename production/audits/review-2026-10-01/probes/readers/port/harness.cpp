#include "CoreGolden.h"
#include <cstdio>
#include <string>
#include <vector>
#include <algorithm>
using namespace LedgerCore;

static std::string D(double d) { char b[64]; std::snprintf(b, sizeof(b), "%.6f", d); return b; }
static std::string B(bool b) { return b ? "True" : "False"; }
static void Out(const std::string& s) { std::printf("%s\n", s.c_str()); }
static std::string T(const GameTime& t) { char b[32]; std::snprintf(b, sizeof(b), "D%d %02d:%02d", t.Day, t.Hour, t.Minute); return b; }

static CastDay ParseOrDie(const std::string& J) { CastDay C; std::string E; if (!CastDay::Parse(J, C, E)) { std::printf("PARSEFAIL %s\n", E.c_str()); } return C; }
static void AddAll(GossipMill& M, const CastDay& C) { for (const std::string& Id : C.People()) M.Add(std::make_shared<Gossiper>(Id, Id, std::make_shared<MemoryStore>(Id), std::make_shared<KnowledgeBase>())); }
static void DumpMem(GossipMill& M, const CastDay& C, const std::string& Tag)
{
	std::vector<std::string> Ids = C.People(); std::sort(Ids.begin(), Ids.end());
	for (const std::string& Id : Ids)
	{
		GossiperPtr G = M.Get(Id);
		for (const MemoryEvent& E : G->Memory->Events) Out(Tag + " M " + Id + " " + std::to_string(E.Time.Day) + ":" + std::to_string(E.Time.Hour) + ":" + std::to_string(E.Time.Minute) + "|" + E.Kind + "|" + D(E.Importance) + "|" + E.Text);
		for (const RumorPtr& R : G->Rumors) Out(Tag + " R " + Id + " " + R->TopicKey() + "|" + R->Content.Value + "|" + D(R->Confidence) + "|" + std::to_string(R->Hops) + "|" + std::to_string(R->OriginRung) + "|" + R->Summary);
	}
}
static std::string FoundStr(const std::vector<std::pair<std::string, GameTime> >& V) { std::string J; for (size_t I = 0; I < V.size(); ++I) J += (I ? "," : "") + V[I].first + "@" + std::to_string(V[I].second.TotalMinutes()); return J; }

int main()
{
	CastDay Kept = ParseOrDie("{\"talk_range_m\":6,\"places\":{\"counter\":{\"x_m\":0,\"z_m\":0,\"inside\":true},\"step\":{\"x_m\":0,\"z_m\":3}},"
		"\"areas\":{\"shop\":{\"places\":[\"counter\",\"step\"],\"names\":[\"Rita's\",\"the pawn shop\"],\"keeper\":\"rita\"}},"
		"\"people\":[{\"id\":\"rita\",\"routine\":[[0,\"off\"],[9,\"counter\"],[17,\"off\"]]},{\"id\":\"passer\",\"routine\":[[0,\"off\"],[12,\"step\"],[15,\"off\"]]},{\"id\":\"hal\",\"routine\":[[0,\"off\"],[11,\"counter\"],[12,\"off\"]]}],\"ties\":[]}");
	struct Case { GameTime Done; bool bMend; GameTime Mend; std::vector<std::string> Leave; bool bLeave; };
	std::vector<Case> Cases = {
		{ GameTime(0, 12, 5), false, GameTime(0,0,0), {}, false },
		{ GameTime(0, 11, 30), true, GameTime(0, 11, 50), {}, false },
		{ GameTime(0, 11, 30), true, GameTime(0, 11, 30), {}, false },
		{ GameTime(0, 11, 59), true, GameTime(0, 12, 0), {}, false },
		{ GameTime(0, 2, 0), false, GameTime(0,0,0), { "passer" }, true },
		{ GameTime(1, 0, 30), false, GameTime(0,0,0), {}, false },
	};
	for (const Case& K : Cases)
	{
		GossipMill M(std::make_shared<SocialGraph>()); AddAll(M, Kept);
		Aftermath A; Aftermath::Make("shop", "k", "somebody put Rita's window in", K.Done, K.bMend ? &K.Mend : nullptr, K.bLeave ? &K.Leave : nullptr, A);
		std::string F1 = FoundStr(A.Tick(&M, &Kept, GameTime(0, 11, 45)));
		std::string F2 = FoundStr(A.Tick(&M, &Kept, GameTime(2, 20, 0)));
		Out("AFT " + T(K.Done) + " " + F1 + " | " + F2 + " | " + A.ToJson());
		DumpMem(M, Kept, "AFT");
	}
	CastDay Names = ParseOrDie("{\"talk_range_m\":6,\"places\":{\"counter\":{\"x_m\":0,\"z_m\":0}},"
		"\"areas\":{\"shop\":{\"places\":[\"counter\"],\"names\":[\"Rita's\",\"the pawn shop\",\"Rita's place\",\"pawn\"],\"keeper\":\"rita\"},\"bare\":{\"places\":[],\"names\":[],\"keeper\":\"rita\"}},"
		"\"people\":[{\"id\":\"rita\",\"routine\":[[0,\"counter\"]]}],\"ties\":[]}");
	for (const char* Said : { "somebody put Rita's window in", "the pawn shop's window was put in", "somebody put rita's window in.", "glass all over Rita's place step", "the pawn's door kicked", "  somebody put Rita's window in . . ", "\xC3\xA9something at Rita's", "somebody smashed RITA'S window", "pawn shop glass" })
		for (const char* Area : { "shop", "bare" })
			for (bool There : { false, true })
			{
				Aftermath A; Aftermath::Make(Area, "k", Said, GameTime(0, 2, 0), nullptr, nullptr, A);
				Out(std::string("KMO ") + Area + " " + B(There) + " [" + Said + "] => " + A.KeeperMemoryOf(&Names, There) + " || " + A.PresentMemoryOf() + " || " + A.MemoryOf());
			}
	struct Tea { const char* How; std::vector<std::pair<int,int> > Spans; };
	std::vector<Tea> Teas = {
		{ "slipped", { {21*60+5, 21*60+40}, {21*60+55, 22*60+40} } },
		{ "neareleven", { {22*60+10, 22*60+50} } },
		{ "lateleft", { {21*60+45, 22*60+20} } },
		{ "ten", { {22*60, 22*60+40} } },
		{ "tenone", { {22*60+1, 22*60+40} } },
		{ "ontime-tolast", { {21*60+30, 22*60+30} } },
		{ "late-gap", { {21*60+45, 22*60+5}, {22*60+16, 22*60+40} } },
		{ "one", { {22*60+59, 22*60+59} } },
	};
	for (const Tea& Tt : Teas)
	{
		GossipMill M{std::shared_ptr<SocialGraph>()};
		M.Add(std::make_shared<Gossiper>("ada", "ada", std::make_shared<MemoryStore>("ada"), std::make_shared<KnowledgeBase>()));
		GossiperPtr Ada = M.Get("ada");
		std::unique_ptr<AdasTea> Te = AdasTea::For(0, true);
		std::string L; Te->SheSeesHim(GameTime(2, 10, 0), L);
		for (auto& Sp : Tt.Spans) for (int Mm = Sp.first; Mm <= Sp.second; ++Mm) Te->WithHer(GameTime(2, Mm / 60, Mm % 60));
		TeaState St = Te->Close(Ada.get(), GameTime(2, 23, 0));
		std::unique_ptr<AdasTea> Back = AdasTea::FromJson(Te->ToJson());
		Out(std::string("TEA ") + Tt.How + " " + TeaStateName(St) + " " + D(Ada->Loyalty) + " " + D(Ada->Suspicion.Value()) + " " + (Ada->Memory->Events.empty() ? std::string("none") : Ada->Memory->Events.back().Text) + " back=" + TeaStateName(Back->State()));
	}
	auto Base = [](const std::string& PlaceExtra, const std::string& AreaExtra) { return "{\"talk_range_m\":6,\"places\":{\"a\":{\"x_m\":0,\"z_m\":0" + PlaceExtra + "}},\"areas\":{\"A\":{\"places\":[\"a\"]" + AreaExtra + "}},\"people\":[{\"id\":\"p\",\"routine\":[[0,\"a\"]]}],\"ties\":[]}"; };
	std::vector<std::pair<std::string, std::string> > Ps = {
		{"inside-yes", Base(",\"inside\":\"yes\"", "")}, {"inside-1", Base(",\"inside\":1", "")}, {"inside-null", Base(",\"inside\":null", "")}, {"inside-false", Base(",\"inside\":false", "")},
		{"keeper-nobody", Base("", ",\"keeper\":\"nobody\"")}, {"keeper-empty", Base("", ",\"keeper\":\" \"")}, {"keeper-num", Base("", ",\"keeper\":3")}, {"keeper-null", Base("", ",\"keeper\":null")},
		{"keeper-spaced", Base("", ",\"keeper\":\" p \"")}, {"street-1", Base("", ",\"street\":1")}, {"street-null", Base("", ",\"street\":null")}, {"street-true", Base("", ",\"street\":true")},
		{"hours-text", Base("", ",\"hours\":\"x\"")}, {"hours-bad-day", Base("", ",\"hours\":{\"funday\":[9,17]}")}, {"hours-25", Base("", ",\"hours\":{\"mon\":[9,49]}")},
		{"hours-backwards", Base("", ",\"hours\":{\"mon\":[17,9]}")}, {"hours-quarter", Base("", ",\"hours\":{\"mon\":[9.25,17]}")}, {"breaks-no-hours", Base("", ",\"breaks\":{\"mon\":[[12,13]]}")},
		{"hours-ok", Base("", ",\"hours\":{\"mon\":[9,17.5]}")}, {"keeper-twice-last-bad", Base("", ",\"keeper\":\"p\",\"keeper\":\"zz\"")},
	};
	for (auto& Pp : Ps)
	{
		CastDay C; std::string E;
		if (CastDay::Parse(Pp.second, C, E)) { std::string K = C.KeeperOf("A"); Out("PARSE " + Pp.first + " accepted keeper=" + (K.empty() ? std::string("null") : K) + " inside=" + B(C.IsInside("a")) + " street=" + B(C.OnQuayStreet("p", 0, 9))); }
		else Out("PARSE " + Pp.first + " refused");
	}
	CastDay Walls = ParseOrDie("{\"talk_range_m\":6,\"places\":{\"ia\":{\"x_m\":0,\"z_m\":0,\"inside\":true},\"ia2\":{\"x_m\":1,\"z_m\":0,\"inside\":true},\"ib\":{\"x_m\":2,\"z_m\":0,\"inside\":true},\"oc\":{\"x_m\":3,\"z_m\":0},\"od\":{\"x_m\":4,\"z_m\":0},\"ie\":{\"x_m\":5,\"z_m\":0,\"inside\":true},\"oa\":{\"x_m\":0,\"z_m\":1}},"
		"\"areas\":{\"A\":{\"places\":[\"ia\",\"ia2\",\"oa\"]},\"B\":{\"places\":[\"ib\"]},\"C\":{\"places\":[\"oc\"]}},"
		"\"people\":[{\"id\":\"ia\",\"routine\":[[0,\"ia\"]]},{\"id\":\"ia2\",\"routine\":[[0,\"ia2\"]]},{\"id\":\"ib\",\"routine\":[[0,\"ib\"]]},{\"id\":\"oc\",\"routine\":[[0,\"oc\"]]},{\"id\":\"od\",\"routine\":[[0,\"od\"]]},{\"id\":\"ie\",\"routine\":[[0,\"ie\"]]},{\"id\":\"oa\",\"routine\":[[0,\"oa\"]]},{\"id\":\"off\",\"routine\":[[0,\"off\"]]}],\"ties\":[]}");
	for (const std::string& X : Walls.People()) { std::string S; for (const std::string& Y : Walls.People()) S += Walls.Together(X, Y, 0, 9) ? "1" : "0"; Out("TOG " + X + " " + S); }
	int Rs[] = { -1, 0, 1, 3, 4, 5 };
	for (int X : Rs) { std::string S; for (int I = 0; I < 6; ++I) S += (I ? "," : "") + std::to_string(Rumor::MergeRung(X, Rs[I])); Out("MERGE " + std::to_string(X) + " " + S); }
	std::vector<std::pair<int,int> > Looks = { {-1,1},{1,-1},{4,2},{2,4},{-1,4},{0,3} };
	for (auto& Lk : Looks)
	{
		GossipMill M{std::shared_ptr<SocialGraph>()};
		M.Add(std::make_shared<Gossiper>("w", "w", std::make_shared<MemoryStore>("w"), std::make_shared<KnowledgeBase>()));
		M.Witness("w", Fact("player", "x_d1", "v"), "s", true, GameTime(1, 10, 0), 0.5, false, Lk.first);
		M.Witness("w", Fact("player", "x_d1", "v"), "s2", true, GameTime(1, 11, 0), 0.7, false, Lk.second);
		GossiperPtr G = M.Get("w");
		std::string Rr, Mm;
		for (size_t I = 0; I < G->Rumors.size(); ++I) Rr += (I ? ";" : "") + std::to_string(G->Rumors[I]->OriginRung) + "/" + D(G->Rumors[I]->Confidence) + "/" + G->Rumors[I]->Summary;
		for (size_t I = 0; I < G->Memory->Events.size(); ++I) Mm += (I ? ";" : "") + G->Memory->Events[I].Text;
		Out("LOOK " + std::to_string(Lk.first) + " " + std::to_string(Lk.second) + " " + Rr + " mem=" + Mm);
	}
	CastDay Small = ParseOrDie("{\"talk_range_m\":6,\"places\":{\"a\":{\"x_m\":0,\"z_m\":0}},\"people\":[{\"id\":\"p\",\"routine\":[[0,\"a\"]]},{\"id\":\"q\",\"routine\":[[0,\"a\"]]},{\"id\":\"r\",\"routine\":[[0,\"off\"],[13,\"a\"]]}],\"ties\":[[\"p\",\"q\",0.9],[\"q\",\"r\",0.9]]}");
	std::vector<std::vector<int> > Seqs = { {723,779,850}, {720,721,722,726,900}, {779,780,3000}, {-30,5,70} };
	for (auto& Seq : Seqs)
	{
		auto G = std::make_shared<SocialGraph>(); for (const CastDay::Tie& Ti : Small.Ties()) G->Link(Ti.A, Ti.B, Ti.W);
		GossipMill M(G); AddAll(M, Small);
		M.Witness("p", Fact("player", "seen_d0", "here"), "the new owner was here", true, GameTime(0, 12, 0), 0.9, false, 4);
		TownHours Th;
		std::string Log, SeqS;
		for (size_t I = 0; I < Seq.size(); ++I)
		{
			int Ran = Th.RunTo(&M, &Small, GameTime::FromTotalMinutes(Seq[I]));
			Log += (I ? " " : "") + std::to_string(Seq[I]) + ":" + std::to_string(Ran) + ":" + Th.ToJson();
			SeqS += (I ? "," : "") + std::to_string(Seq[I]);
		}
		Out("HOURS " + SeqS + " " + Log);
		for (const std::string& Id : Small.People()) for (const RumorPtr& R : M.Get(Id)->Rumors) Out("HOURS  R " + Id + " " + R->TopicKey() + " " + D(R->Confidence) + " " + std::to_string(R->Hops));
		for (const std::string& Id : Small.People()) for (const MemoryEvent& E : M.Get(Id)->Memory->Events) Out("HOURS  M " + Id + " " + T(E.Time) + " " + E.Text);
	}
	for (const char* Js : { "{\"round\":726}", "{\"round\":727}", "{\"next\":12}", "{\"round\":-6,\"next\":3}", "{\"round\":-1}", "{\"round\":-7,\"next\":3}", "{\"round\":6e8,\"next\":2}", "{\"round\":\"6\",\"next\":2}", "{\"next\":-1}", "{\"round\":-0.0}", "{\"round\":12.0}", "{\"round\":599999994}" })
		Out(std::string("HJSON ") + Js + " => " + TownHours::FromJson(Js).ToJson());
	{
		GossipMill M{std::shared_ptr<SocialGraph>()};
		M.Add(std::make_shared<Gossiper>("w", "w", std::make_shared<MemoryStore>("w"), std::make_shared<KnowledgeBase>()));
		M.Witness("w", Fact("player", "week_d6", "takeover"), "heard", false, GameTime(6, 9, 0), 0.4);
		M.WitnessRemembering("w", Fact("player", "week_d6", "takeover"), "told", true, GameTime(6, 10, 0), "remembered");
		M.WitnessRemembering("w", Fact("player", "week_d6", "takeover"), "told2", false, GameTime(6, 11, 0), "");
		GossiperPtr G = M.Get("w");
		std::string Rr, Mm;
		for (size_t I = 0; I < G->Rumors.size(); ++I) Rr += (I ? ";" : "") + G->Rumors[I]->Summary + "/" + D(G->Rumors[I]->Confidence) + "/" + B(G->Rumors[I]->Sensitive) + "/" + std::to_string(G->Rumors[I]->Hops);
		for (size_t I = 0; I < G->Memory->Events.size(); ++I) Mm += (I ? ";" : "") + G->Memory->Events[I].Kind + "/" + D(G->Memory->Events[I].Importance) + "/" + G->Memory->Events[I].Text;
		Out("WREM " + Rr + " mem=" + Mm);
	}
	return 0;
}
