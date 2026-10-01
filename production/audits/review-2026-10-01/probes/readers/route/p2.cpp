// Probe 2: the C++ side of the C#/C++ agreement check (Together, OnQuayStreet,
// WouldReport, the keeper's memory), printed in the same lines as cs/Program.cs.
#include "CrimeProbe.h"
#include "TownWeek.h"
#include <cstdio>
#include <fstream>
#include <sstream>

using namespace LedgerCore;
static std::string ReadAll(const char* P) { std::ifstream In(P); std::stringstream S; S << In.rdbuf(); return S.str(); }
static std::string D(double V) { char B[32]; std::snprintf(B, sizeof B, "%g", V); return B; }

int main(int argc, char** argv)
{
	CastDay Cast; std::string Err;
	if (!CastDay::Parse(ReadAll(argv[1]), Cast, Err)) { std::printf("parse: %s\n", Err.c_str()); return 1; }
	std::ofstream Out(argv[2]);
	const std::vector<std::string> People = Cast.People();
	int N = 0;
	for (int Dd = 0; Dd < 7; ++Dd)
		for (int H = 0; H < 24; ++H)
		{
			for (const auto& P : People) if (Cast.OnQuayStreet(P, Dd, H)) { Out << "Q|" << Dd << "|" << H << "|" << P << "\n"; ++N; }
			for (size_t I = 0; I < People.size(); ++I)
				for (size_t J = I + 1; J < People.size(); ++J)
					if (Cast.Together(People[I], People[J], Dd, H)) { Out << "T|" << Dd << "|" << H << "|" << People[I] << "|" << People[J] << "\n"; ++N; }
		}
	for (double L : { 0.5, 0.55, 0.575, 0.6, 0.75 })
		for (double Nn : { 0.35, 0.4, 0.5 })
		{
			Gossiper G("x", "x", std::shared_ptr<MemoryStore>(), std::shared_ptr<KnowledgeBase>(), "day", 0.5, Nn, L);
			const std::string T = "player.window_d0";
			Out << "W|" << D(L) << "|" << D(Nn) << "|" << (PoliceFile::WouldReport(&G, Offence::Damage, false, &T) ? "True" : "False") << "\n"; ++N;
		}
	Aftermath A;
	const GameTime Mend = Aftermath::DefaultMend(GameTime(0, 10, 30));
	Aftermath::Make("ritas", "rita_window", "somebody put Rita's window in", GameTime(0, 10, 30), &Mend, nullptr, A);
	Out << "K|" << A.KeeperMemoryOf(&Cast, true) << "\n";
	Out << "K|" << A.KeeperMemoryOf(&Cast, false) << "\n";
	N += 2;
	std::printf("lines %d\n", N);
	return 0;
}
