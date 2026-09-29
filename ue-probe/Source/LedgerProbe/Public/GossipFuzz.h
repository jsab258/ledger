// THE SEEDED GOSSIP GENERATOR, THE C++ TWIN OF A FAMILY OF GOLDEN ROWS.
//
// WHAT IT IS. A seeded random world of two to five people, their ties,
// sightings (Witness), rumours put straight into their heads, facts, bribes,
// leashes, rounds of talk (Tick) and questions asked outright (CompareNotes),
// with every agent's rumours, knowledge, suspicion and new memory lines
// written out after every step, and then what each of them would say (Best,
// BestOfValue, Suspecting::AccountOf and Derive). And a seeded hand-mangled
// save read back by Save::RestoreMillAgents. Each world's whole trace is
// hashed (FNV-1a 64 over its bytes, which are ASCII, so its UTF-8 bytes) and
// CoreGolden.h compares the hash and the line count with the row the C#
// wrote:
//
//   GossipFuzz|scenario|seed|nan 0/1|hash|lines
//   GossipFuzz|save|seed|hash|lines
//
// WHY (the independent reviewer's finding, 29 September). He wrote this
// generator twice, in C# and in C++, and the two agreed byte for byte on
// 12,000 worlds and 3,000 saves once Gossiper::Best and BestOfValue ranked a
// NaN as the C#'s OrderByDescending does. It caught every one of 37 faults
// planted in the port that the hand-written rows missed. So it is part of the
// table now, rather than something one reviewer once ran.
//
// THE TWO MUST BE CHANGED TOGETHER. The C# twin is
// ledger/PerceptionGolden/GossipFuzz.cs, which emits the rows from the real
// Core; this draws the same random numbers in the same order and writes the
// same lines. Any change here (a step, a draw, a word in a line) is made there
// in the same commit, or every row goes red, which is the point.
//
// NO STATE OUTLIVES A ROW: the random stream, the NaN switch and the running
// hash live in one Gen per call, so no row changes what another row draws.
// No Unreal type, C++11 (g++ compiles it as C++11, MSVC as C++14, and the
// module as whatever Unreal uses), and no exceptions (the module has none).
#pragma once

#include "Gossip.h"
#include "SaveCodec.h"
#include "Suspecting.h"

#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <limits>
#include <map>
#include <memory>
#include <string>
#include <vector>

namespace LedgerCore
{
namespace GossipFuzz
{
	// WHICH SEEDS is the C#'s to say (GossipFuzz.cs: worlds 1 to 1500 with
	// NaN and without, saves 1000001 to 1000500); a row names its own seed,
	// and this answers whichever seed it names.

	/// What one row reads: the trace's FNV-1a 64 as sixteen hex digits, and
	/// how many lines it had.
	struct Digest
	{
		std::string Hash;
		long long   Lines;
		Digest() : Lines(0) {}
	};

	class Gen
	{
	public:
		Gen(unsigned long long Seed, bool bWithNaN)
			: State(Seed), bNaN(bWithNaN), Fnv(0xcbf29ce484222325ULL), LineCount(0) {}

		Digest Result() const
		{
			Digest Out;
			char Buf[32];
			std::snprintf(Buf, sizeof(Buf), "%016llx", Fnv);
			Out.Hash = Buf;
			Out.Lines = LineCount;
			return Out;
		}

		void RunScenario(unsigned long long Seed)
		{
			L("SEED " + U(Seed));
			const int N = 2 + R(4);
			std::vector<std::string> Ids((std::vector<std::string>::size_type)N);
			std::shared_ptr<SocialGraph> Graph = std::make_shared<SocialGraph>();
			GossipMill Mill(Graph);
			for (int Ix = 0; Ix < N; Ix++)
			{
				Ids[(size_t)Ix] = "a" + I(Ix);
				const std::string Circle = Circles(R(3));
				Mill.Add(std::make_shared<Gossiper>(Ids[(size_t)Ix], "N" + I(Ix), std::make_shared<MemoryStore>(Ids[(size_t)Ix]),
				                                    std::make_shared<KnowledgeBase>(), Circle));
			}
			for (int Ix = 0; Ix < N; Ix++)
			{
				for (int Jx = Ix + 1; Jx < N; Jx++)
				{
					const int K = R(4);
					if (K == 0) continue;
					const double Wt = PickW();
					if (K == 1) Graph->Link(Ids[(size_t)Jx], Ids[(size_t)Ix], Wt); else Graph->Link(Ids[(size_t)Ix], Ids[(size_t)Jx], Wt);
				}
			}
			std::map<std::string, size_t> MemSeen;
			const int Steps = 6 + R(20);
			for (int St = 0; St < Steps; St++)
			{
				const GameTime Now(1 + St / 20, St % 20, St % 60);
				const int Kind = R(16);
				L("STEP " + I(St) + " kind " + I(Kind));
				if (Kind <= 4)
				{
					const int Ai = R(N + 1);
					const int Fi = R(5);
					const int Sm = R(6);
					const bool bSens = R(2) == 1;
					const double Conf = PickC();
					const bool bIndel = R(5) == 0;
					const int Rung = RungAt(R(10));
					const std::string Summary = Sm == 0 ? " s" + I(St) + " " : (Sm == 1 ? std::string("   ") : "s" + I(St));
					const std::string Wid = Ai == N ? std::string("zz") : Ids[(size_t)Ai];
					Mill.Witness(Wid, FactAt(Fi), Summary, bSens, Now, Conf, bIndel, Rung);
				}
				else if (Kind <= 6)
				{
					const int Ai = R(N);
					const int Fi = R(5);
					const int Oi = R(N);
					const double Conf = PickC();
					const int Hops = HopsAt(R(5));
					const bool bSens = R(2) == 1;
					const bool bIndel = R(6) == 0;
					const int Rung = DRungAt(R(7));
					RumorPtr Put = std::make_shared<Rumor>(FactAt(Fi));
					Put->OriginId = Ids[(size_t)Oi]; Put->Summary = "d" + I(St); Put->Confidence = Conf; Put->Hops = Hops;
					Put->Sensitive = bSens; Put->Indelible = bIndel; Put->OriginRung = Rung;
					Mill.Get(Ids[(size_t)Ai])->Rumors.push_back(Put);
				}
				else if (Kind == 7)
				{
					const int Ai = R(N);
					const int Fi = R(5);
					Mill.Get(Ids[(size_t)Ai])->Knowledge->Learn(FactAt(Fi));
				}
				else if (Kind == 8)
				{
					const int Ai = R(N);
					const int Fi = R(5);
					// C#: a HashSet's Add.
					const std::string Topic = std::string(FactPart(Fi, 0)) + "." + FactPart(Fi, 1);
					const GossiperPtr Holder = Mill.Get(Ids[(size_t)Ai]);
					if (!Holder->SuppressedHas(Topic)) Holder->Suppressed.push_back(Topic);
				}
				else if (Kind == 9)
				{
					const int Ai = R(N);
					if (R(3) == 0) Mill.Get(Ids[(size_t)Ai])->Leashed = true;
				}
				else if (Kind <= 12)
				{
					const int Mode = R(3);
					std::vector<std::vector<bool> > Met((size_t)N, std::vector<bool>((size_t)N, false));
					for (int Ix = 0; Ix < N; Ix++) for (int Jx = 0; Jx < N; Jx++) Met[(size_t)Ix][(size_t)Jx] = R(3) != 0;
					GossipMill::TogetherFn Tog;
					if (Mode == 1)
					{
						Tog = [Met](const std::string& X, const std::string& Y)
						{
							return (bool)Met[(size_t)std::atoi(X.c_str() + 1)][(size_t)std::atoi(Y.c_str() + 1)];
						};
					}
					else if (Mode == 2)
					{
						Tog = [](const std::string&, const std::string&) { return true; };
					}
					DumpEvents(Mill.Tick(Now, Tog));
				}
				else if (Kind <= 14)
				{
					const int Ci = R(N + 1);
					const int Pi = R(N);
					const std::string Cid = Ci == N ? std::string("zz") : Ids[(size_t)Ci];
					DumpEvents(Mill.CompareNotes(Cid, Ids[(size_t)Pi], Now));
				}
				else
				{
					const int Ai = R(N);
					const int Bi = R(N);
					const double Wt = PickW();
					Graph->Link(Ids[(size_t)Ai], Ids[(size_t)Bi], Wt);
				}
				DumpAgents(Mill, Ids, MemSeen);
			}
			// Final reads.
			static const char* const Topics[6] = { "player.window_d1", "player.killed_d1", "bob.location_d1", "player.where_d1", "player.nothing", "" };
			const double Fams[6] = { 0.0, 0.2, 0.5, 0.8, 1.0, std::numeric_limits<double>::quiet_NaN() };
			for (size_t Kx = 0; Kx < Ids.size(); ++Kx)
			{
				const std::string& Id = Ids[Kx];
				const GossiperPtr G = Mill.Get(Id);
				for (int Fx = 0; Fx < 5; ++Fx)
				{
					const std::string Topic = std::string(FactPart(Fx, 0)) + "." + FactPart(Fx, 1);
					const RumorPtr Bv = G->BestOfValue(Topic, FactPart(Fx, 2));
					const RumorPtr Bt = G->Best(Topic);
					L("BV " + Id + " " + Topic + "=" + FactPart(Fx, 2) + " "
					  + (Bv ? B(Bv->Confidence) + "/" + Bv->Summary : std::string("none"))
					  + " best " + (Bt ? B(Bt->Confidence) + "/" + Bt->Summary : std::string("none")));
				}
				for (int Tx = 0; Tx < 6; ++Tx)
				{
					const DeedAccount Acc = Suspecting::AccountOf(G.get(), Topics[Tx]);
					// C#: acc.Summary ?? "<null>". The C#'s Summary is null
					// exactly when nothing is held.
					L("AC " + Id + " [" + Topics[Tx] + "] h" + Bit(Acc.Held) + " s" + Bit(Acc.SawItMyself) + " r" + I(Acc.Rung)
					  + " n" + Bit(Acc.NamesHim) + " " + B(Acc.Confidence) + " " + B(Acc.NamingConfidence)
					  + " [" + (Acc.Held ? Acc.Summary : std::string("<null>")) + "]");
					for (int Nv = 0; Nv < 5; Nv++)
					{
						Nearness Near;
						if (Nv == 1) { Near.SawHimMyself = true; Near.Summary = " by the glass "; }
						if (Nv == 2) { Near.SawHimMyself = true; Near.OthersNear = 2; }
						if (Nv == 3) { Near.HeardHeWasNear = true; Near.OthersNear = -3; }
						if (Nv == 4) { Near.SawHimMyself = true; Near.OthersNear = -1; Near.Summary = "  "; }
						for (int Fam = 0; Fam < 6; ++Fam)
						{
							const Suspecting::Derived Dv = Suspecting::Derive(Acc, Near, Fams[Fam]);
							L("DV " + I(Nv) + " " + B(Fams[Fam]) + " " + B(Dv.Value) + " " + SuspicionLevelName(Dv.Level)
							  + " [" + (Dv.bWhy ? Dv.Why : std::string("<null>")) + "]");
						}
					}
				}
			}
		}

		void RunSave(unsigned long long Seed)
		{
			L("SAVE " + U(Seed));
			const int K = 1 + R(6);
			std::string Json = "{\"agents\":[{\"id\":\"w\",\"rumors\":[";
			for (int Ix = 0; Ix < K; Ix++)
			{
				if (Ix > 0) Json += ',';
				const std::string Ht = TokAt(R(TokCount()));
				const std::string Rt = TokAt(R(TokCount()));
				const int Form = R(6);
				Json += "{\"subj\":\"player\",\"pred\":\"p" + I(Ix) + "\",\"val\":\"v\",\"conf\":0.5,\"hops\":" + Ht;
				if (Form == 0) {}
				else if (Form == 1) { const std::string Third = TokAt(R(TokCount())); Json += ",\"rung\":" + Rt + ",\"rung\":" + Third; }
				else if (Form == 2) Json += ",\"ru\\u006eg\" : " + Rt;
				else if (Form == 3) Json += ",\"inner\":{\"rung\":" + Rt + "},\"rung\":1";
				else Json += ",\"rung\":" + Rt;
				Json += '}';
			}
			Json += "]}]}";
			L("JSON " + Json);
			GossipMill Mill(std::make_shared<SocialGraph>());
			Mill.Add(std::make_shared<Gossiper>("w", "w", std::make_shared<MemoryStore>("w"), std::make_shared<KnowledgeBase>()));
			RumorPtr Sentinel = std::make_shared<Rumor>(Fact(std::string("player"), std::string("sentinel"), std::string("v")));
			Sentinel->OriginId = "w"; Sentinel->Summary = "x"; Sentinel->Confidence = 0.5; Sentinel->Hops = 7; Sentinel->OriginRung = 3;
			Mill.Get("w")->Rumors.push_back(Sentinel);
			Save::RestoreMillAgents(Json, Mill);
			const GossiperPtr G = Mill.Get("w");
			for (size_t Jx = 0; Jx < G->Rumors.size(); ++Jx)
			{
				L("SR " + G->Rumors[Jx]->Content.Predicate + " h" + I(G->Rumors[Jx]->Hops) + " r" + I(G->Rumors[Jx]->OriginRung)
				  + " " + B(G->Rumors[Jx]->Confidence));
			}
		}

	private:
		unsigned long long State;
		bool               bNaN;
		unsigned long long Fnv;
		long long          LineCount;

		// ---- the draws, in the C#'s order -------------------------------

		unsigned long long Next()
		{
			State += 0x9E3779B97F4A7C15ULL;
			unsigned long long Z = State;
			Z = (Z ^ (Z >> 30)) * 0xBF58476D1CE4E5B9ULL;
			Z = (Z ^ (Z >> 27)) * 0x94D049BB133111EBULL;
			return Z ^ (Z >> 31);
		}

		int R(int Below) { return (int)(Next() % (unsigned long long)Below); }

		// The weight and confidence tables, with the C#'s NaN at the end of
		// each; a world without NaN draws 0.5 there instead.
		double PickW()
		{
			static const double Weights[10] = { 0.0, 0.1, 0.25, 0.3, 0.5, 0.7, 0.9, 1.0, 1.5, -0.2 };
			int Ix = R(21);
			if (Ix >= 11) Ix -= 11;
			if (Ix == 10) return bNaN ? std::numeric_limits<double>::quiet_NaN() : 0.5;
			return Weights[Ix];
		}

		double PickC()
		{
			static const double Confs[15] = { 0.05, 0.1, 0.19, 0.2, 0.25, 0.3, 0.5, 0.6, 0.8, 0.9, 0.94, 0.95, 1.0, 1.3, -0.1 };
			int Ix = R(31);
			if (Ix >= 16) Ix -= 16;
			if (Ix == 15) return bNaN ? std::numeric_limits<double>::quiet_NaN() : 0.5;
			return Confs[Ix];
		}

		static int RungAt(int Ix)  { static const int T[10] = { -5, -1, -1, 0, 1, 2, 3, 4, 4, 7 }; return T[Ix]; }
		static int DRungAt(int Ix) { static const int T[7] = { -1, 0, 1, 2, 3, 4, 4 }; return T[Ix]; }
		static int HopsAt(int Ix)  { static const int T[5] = { 0, 1, 1, 2, 3 }; return T[Ix]; }

		static const char* FactPart(int Fx, int Part)
		{
			static const char* const T[5][3] = {
				{ "player", "window_d1", "seen" }, { "player", "window_d1", "other" }, { "player", "killed_d1", "docker" },
				{ "bob", "location_d1", "docks" }, { "player", "where_d1", "docks" } };
			return T[Fx][Part];
		}

		static Fact FactAt(int Fx)
		{
			return Fact(std::string(FactPart(Fx, 0)), std::string(FactPart(Fx, 1)), std::string(FactPart(Fx, 2)));
		}

		static const char* Circles(int Ix)
		{
			static const char* const T[3] = { "day", "night", "both" };
			return T[Ix];
		}

		// The value tokens a mangled save's hops and rung are drawn from.
		static const char* Toks(int Ix, int& Count)
		{
			static const char* const T[] = { "4","2.7","-0.5","1e300","-1e300","1e400","-1e400","\"3\"","null","true","false","4.",".5","+3","-1","-2","0","1E1","3e-1","-0","1e-400","2147483648","-2147483649","4.9999999999999999","00","007","[4]","{}","4abc","0x4","NaN","Infinity","1e","-","4.5.6","+.5","1.e0","-00","2147483647","-2147483648","3 ", "1", "2", "3", "4" };
			Count = (int)(sizeof(T) / sizeof(T[0]));
			return Ix >= 0 && Ix < Count ? T[Ix] : "";
		}
		static int TokCount() { int Count = 0; Toks(0, Count); return Count; }
		static std::string TokAt(int Ix) { int Count = 0; return std::string(Toks(Ix, Count)); }

		// ---- the trace ----------------------------------------------------

		/// One line of the trace, hashed as its bytes and a newline.
		void L(const std::string& Line)
		{
			for (size_t Ix = 0; Ix < Line.size(); ++Ix)
			{
				Fnv ^= (unsigned long long)(unsigned char)Line[Ix];
				Fnv *= 0x100000001b3ULL;
			}
			Fnv ^= (unsigned long long)(unsigned char)'\n';
			Fnv *= 0x100000001b3ULL;
			++LineCount;
		}

		/// The double's bits as sixteen hex digits, and any NaN as "NaN": the
		/// two engines' NaNs need not carry the same bits. By the bits, for
		/// the fast-math reason Perception.h gives.
		static std::string B(double V)
		{
			if (IsNaNBits(V)) return "NaN";
			unsigned long long Bits = 0ULL;
			std::memcpy(&Bits, &V, sizeof(Bits));
			char Buf[32];
			std::snprintf(Buf, sizeof(Buf), "%016llx", Bits);
			return std::string(Buf);
		}

		static std::string I(long long V)
		{
			char Buf[32];
			std::snprintf(Buf, sizeof(Buf), "%lld", V);
			return std::string(Buf);
		}

		static std::string U(unsigned long long V)
		{
			char Buf[32];
			std::snprintf(Buf, sizeof(Buf), "%llu", V);
			return std::string(Buf);
		}

		static std::string Bit(bool V) { return V ? "1" : "0"; }

		void DumpAgents(const GossipMill& Mill, const std::vector<std::string>& Ids, std::map<std::string, size_t>& MemSeen)
		{
			L("OFF " + I(Mill.WitnessesOffered()) + " " + I(Mill.WitnessesDropped()));
			for (size_t Kx = 0; Kx < Ids.size(); ++Kx)
			{
				const std::string& Id = Ids[Kx];
				const GossiperPtr G = Mill.Get(Id);
				L("A " + Id + " susp=" + B(G->Suspicion.Value()) + " leash=" + Bit(G->Leashed) + " n=" + I((long long)G->Rumors.size()));
				for (size_t Jx = 0; Jx < G->Rumors.size(); ++Jx)
				{
					const RumorPtr& Rm = G->Rumors[Jx];
					L("R " + Rm->TopicKey() + "=" + Rm->Content.Value + "|" + Rm->OriginId + "|" + Rm->Summary + "|" + B(Rm->Confidence)
					  + "|" + I(Rm->Hops) + "|" + Bit(Rm->Sensitive) + Bit(Rm->Indelible) + "|" + I(Rm->OriginRung));
				}
				for (size_t Jx = 0; Jx < G->Knowledge->Facts.size(); ++Jx)
				{
					const Fact& Known = G->Knowledge->Facts[Jx];
					L("K " + Known.Subject + "." + Known.Predicate + "=" + Known.Value);
				}
				const std::map<std::string, size_t>::const_iterator Was = MemSeen.find(Id);
				const size_t Seen = Was == MemSeen.end() ? 0 : Was->second;
				for (size_t Ex = Seen; Ex < G->Memory->Events.size(); ++Ex)
				{
					const MemoryEvent& E = G->Memory->Events[Ex];
					L("M " + E.Time.ToString() + "|" + E.Kind + "|" + B(E.Importance) + "|" + E.Text);
				}
				MemSeen[Id] = G->Memory->Events.size();
			}
		}

		void DumpEvents(const std::vector<GossipEvent>& Ev)
		{
			L("EV " + I((long long)Ev.size()));
			for (size_t Ex = 0; Ex < Ev.size(); ++Ex)
			{
				const GossipEvent& E = Ev[Ex];
				L("E " + E.FromId + ">" + E.ToId + " c" + Bit(E.Contradiction) + " x" + Bit(E.Exposure) + " "
				  + E.RumorRef->TopicKey() + "=" + E.RumorRef->Content.Value + " " + B(E.RumorRef->Confidence)
				  + " h" + I(E.RumorRef->Hops) + " r" + I(E.RumorRef->OriginRung) + " i" + Bit(E.RumorRef->Indelible));
			}
		}
	};

	/// One world, seeded, with or without NaN in its draws.
	inline Digest Scenario(unsigned long long Seed, bool bWithNaN)
	{
		Gen G(Seed, bWithNaN);
		G.RunScenario(Seed);
		return G.Result();
	}

	/// One hand-mangled save, seeded.
	inline Digest SaveRead(unsigned long long Seed)
	{
		Gen G(Seed, true);
		G.RunSave(Seed);
		return G.Result();
	}
}
}
