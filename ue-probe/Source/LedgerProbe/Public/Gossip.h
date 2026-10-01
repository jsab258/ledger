// TRANSLITERATION of ledger/Assets/Scripts/Core/Gossip.cs, D1 probe.
//
// TRANSLITERATION, NOT REWRITE, and the distinction is the whole method: the
// C# suite is the behavioural definition, so every constant and every branch
// here matches its source line for line, and where the C# is subtle the
// comment explaining why travels with it. A port that "improved" something
// would make the two engines incomparable, which is the one thing D1 must
// not allow.
//
// WHAT THIS FILE IS FOR, in one sentence from the crime ruling: THE ONE RULE
// THAT DECIDES WHETHER ONE CHARACTER PASSES A RUMOUR TO ANOTHER is
// GossipMill.Tick, Gossip.cs 433 to 541, and its heart is 471: passed =
// r.Confidence * tie * HopDecay, then a floor. CompareNotes, 631 to 724, is
// the same rule for a question asked outright; nothing else in 1188 lines
// decides a hop.
//
// SCOPE, from the ruling section 1 item 6 and town list 6n (29 September):
// SocialGraph 9 to 32; Rumor 37 to 67, with OriginRung 52; Gossiper 72 to
// 126 (Suspicion as its number, 29 September); GossipEvent 130 to 136; and
// from GossipMill only _agents, _graph, the four tunables 149 to 152, the
// constructor 154, Tie 160, Add 162, Get 186 to 187, WitnessesOffered and
// WitnessesDropped 202 to 203, SummariesSaying, SaysWord and IsWordChar 233
// to 264, Witness 270 to 378 with its rung, Tick 433 to 541 with together as
// a function argument, Telling, SurestFirst, TellingSlot, TellingSlots and
// Weigh 559 to 623 with SameStrength, CompareNotes 631 to 724, (town
// list 6bs, 29 September, for the town's hourly rounds in TownRounds.h) Age
// 1104 to 1131 with RumorHalfLifeHours, and (30 September, the town's fix
// of his arrival) PlainFactOfHim, Leads with Lead, and ExposureOf with
// Exposure's numbers (not its Sentence), and (1 October, Jafar's ruling that
// Mickey's own handle it privately) KeepsHisDeedsFor, KeepsHisDeeds and
// KeepsHisDeedsToThemselves.
//
// OUT OF SCOPE AND NOT HERE, so a reader can tell a missing member from a
// forgotten one: Forget, PlayerClaims, KnowsSecret, DayCircleHeat, Bribe,
// Intimidate, Discredit, UseHook (whose own use of PlainFactOfHim waits
// with it), HoldsIndelible, Contain, Backfire, RestoreDiscredited and
// StrongestSurvivingPlayerLead.
//
// SUSPICION IS RAISED AS THE C# RAISES IT since town list 6n: Tick's two
// Suspicion.Raise calls (Gossip.cs 513 and 523) and CompareNotes' two (707
// and 713) are here, on the value-only SuspicionTracker of Suspicion.h,
// which takes each reason and drops it because its reasons trail is not
// ported. The crime verdict prints gossipSuspicionPorted=yes.
//
// REFERENCE SEMANTICS, AND WHERE THIS PORT KEEPS THEM. C# Rumor, Gossiper,
// MemoryStore and KnowledgeBase are classes, and the mill MUTATES them
// through handles it got from a list: Witness raises an existing rumour's
// confidence in place, Tick appends to a listener it fetched by id. Those
// four are therefore shared_ptr here, because a value copy would silently
// make the mutation land on a temporary and the rumour would never firm up.
// Fact is the one class this port holds BY VALUE: its three fields are
// written only by its constructor and no ported line mutates a Fact after
// it exists, so sharing it buys nothing and costs every call site a
// dereference. That is a deviation and it is named rather than hidden.
//
// NO UNREAL TYPE IS IN THIS FILE, deliberately, and it is the standing rule
// from 25 August: the decisions and the strings live where the tests run,
// because this project's top layer does not compile in the container that
// writes it. The probe module supplies distances, ids and live world state
// and nothing else.
#pragma once

#include "GameTime.h"
#include "MemoryStore.h"
#include "Perception.h"      // LedgerCore::Clamp
#include "Suspicion.h"

#include <algorithm>
#include <cctype>
#include <cmath>
#include <functional>
#include <memory>
#include <string>
#include <utility>
#include <vector>

namespace LedgerCore
{
	// C#'s Math.Max(double, double), NaN and signed zero included: a NaN on
	// either side is the answer, and +0 beats -0. The plain `a > b ? a : b`
	// this file used before answers the other operand for a NaN on the left,
	// and a NaN is a value the save and the memory markdown can both carry
	// (Perception.h, IsNaNBits). By its bits, for the fast-math reason
	// Perception.h gives.
	inline double DotNetMax(double A, double B)
	{
		if (IsNaNBits(A)) { return A; }
		if (IsNaNBits(B)) { return B; }
		if (A != B) { return B < A ? A : B; }
		return std::signbit(B) ? A : B;
	}

	// C#'s Math.Min(double, double), the same way: a NaN on either side is the
	// answer, and -0 beats +0 (the independent check of Ada's tea, 30
	// September: std::fmin gave a NaN regard full marks).
	inline double DotNetMin(double A, double B)
	{
		if (IsNaNBits(A)) { return A; }
		if (IsNaNBits(B)) { return B; }
		if (A != B) { return A < B ? A : B; }
		return std::signbit(A) ? A : B;
	}

	// C#'s double.CompareTo, which is what OrderByDescending sorts by: a NaN
	// is smaller than every number and equal to another NaN, so the order is
	// a total one even where `>` is not.
	inline int DotNetCompare(double A, double B)
	{
		const bool bNanA = IsNaNBits(A), bNanB = IsNaNBits(B);
		if (bNanA || bNanB) { return bNanA ? (bNanB ? 0 : -1) : 1; }
		return A < B ? -1 : (A > B ? 1 : 0);
	}
	// Gossip.cs 9 to 32. Undirected weighted acquaintance graph: how likely,
	// and how faithfully, two NPCs pass talk about a third party (usually the
	// player). Weight is 0..1.
	//
	// A VECTOR OF ROWS RATHER THAN A HASH MAP, AND THE ORDER IS THE REASON.
	// Tick walks Contacts(speaker) and the events it returns come out in that
	// order, so the container's iteration order is part of the observable
	// behaviour. C#'s Dictionary enumerates in insertion order in practice
	// when nothing is ever removed, and nothing here removes (Forget is the
	// only remover in the C# and it is out of scope). Insertion order is
	// therefore the honest transliteration, and a hash map would have made
	// the two engines disagree about which event came first for no reason a
	// reader could see.
	class SocialGraph
	{
	public:
		void Link(const std::string& A, const std::string& B, double Weight)
		{
			if (A == B) return;
			Put(A, B, Weight);
			Put(B, A, Weight);
		}

		double Tie(const std::string& A, const std::string& B) const
		{
			const Row* R = FindRow(A);
			if (R == 0) return 0.0;
			for (std::vector<Edge>::size_type I = 0; I < R->Edges.size(); ++I)
			{
				if (R->Edges[I].To == B) return R->Edges[I].Weight;
			}
			return 0.0;
		}

		std::vector<std::string> Contacts(const std::string& Id) const
		{
			std::vector<std::string> Out;
			const Row* R = FindRow(Id);
			if (R == 0) return Out;      // C#: Enumerable.Empty<string>()
			for (std::vector<Edge>::size_type I = 0; I < R->Edges.size(); ++I)
			{
				Out.push_back(R->Edges[I].To);
			}
			return Out;
		}

	private:
		struct Edge { std::string To; double Weight; };
		struct Row  { std::string From; std::vector<Edge> Edges; };
		std::vector<Row> Ties;

		const Row* FindRow(const std::string& From) const
		{
			for (std::vector<Row>::size_type I = 0; I < Ties.size(); ++I)
			{
				if (Ties[I].From == From) return &Ties[I];
			}
			return 0;
		}

		void Put(const std::string& From, const std::string& To, double W)
		{
			const double Clamped = Clamp(W, 0.0, 1.0);   // C#: Math.Clamp
			for (std::vector<Row>::size_type I = 0; I < Ties.size(); ++I)
			{
				if (Ties[I].From != From) continue;
				for (std::vector<Edge>::size_type J = 0; J < Ties[I].Edges.size(); ++J)
				{
					// row[to] = w: an existing key keeps its position.
					if (Ties[I].Edges[J].To == To) { Ties[I].Edges[J].Weight = Clamped; return; }
				}
				Edge E; E.To = To; E.Weight = Clamped;
				Ties[I].Edges.push_back(E);
				return;
			}
			Row R; R.From = From;
			Edge E; E.To = To; E.Weight = Clamped;
			R.Edges.push_back(E);
			Ties.push_back(R);
		}
	};

	// Gossip.cs 37 to 67. A propagating piece of talk about someone. Content
	// is a structured Fact so it can be checked against what an NPC already
	// knows; Confidence decays each hop so third-hand rumour carries less
	// weight than an eyewitness account.
	class Rumor
	{
	public:
		Fact        Content;      // e.g. player.location_d2_evening = warehouse
		std::string OriginId;     // the first-hand source
		std::string Summary;      // human or model readable phrasing of the content
		double      Confidence;   // 0..1
		int         Hops;         // 0 = witnessed first-hand
		bool        Sensitive;    // pertains to the player's hidden (night) life

		/// HOW WELL THE FIRST TELLER SAW THE MAN (town list 6n, 28
		/// September): the rung they reached on the five-rung ladder (0
		/// someone, 1 a silhouette, 2 a mark, 3 a face, 4 recognition),
		/// carried unchanged through every retelling, or -1 when nobody gave
		/// it. FINDINGS, 24 September: a retold rumour did not carry it, so
		/// hearsay whose first teller had named the player could never raise
		/// anyone's suspicion (Suspecting::AccountOf reads it).
		int         OriginRung;

		/// A FACT, not a story. Set only by a killing (combat spec 7b).
		///
		/// Every other rumour in this game can be muddied, bought quiet,
		/// scared quiet, held on a leash or simply left to go cold. None of
		/// that machinery touches a corpse: Age, Discredit, Contain and the
		/// hop decay in Tick all step over an indelible rumour. That
		/// asymmetry against literally everything else in the mill is the
		/// whole reason killing a witness is terrifying rather than
		/// efficient: it works, and it is the one thing you can never take
		/// back.
		bool Indelible;

		Rumor(const Fact& InContent)
			: Content(InContent), Confidence(0.0), Hops(0),
			  Sensitive(false), OriginRung(-1), Indelible(false)
		{
		}

		/// WHETHER THE STORY NAMES HIM (Gossip.cs NamesHim; Jafar's A5 ruling,
		/// 30 September: a witness's story is only as sure as the witness was):
		/// its first teller recognised him (rung 4), or it is no sighting at all
		/// (no rung: a thing told as known). A noise, a shape, a mark or a face
		/// is Suspecting's alone.
		bool NamesHim() const { return OriginRung == -1 || OriginRung >= 4; }

		/// Gossip.cs MergeRung: a vaguer look of one's own never erases a naming.
		static int MergeRung(int A, int B)
		{
			const bool NA = A == -1 || A >= 4, NB = B == -1 || B >= 4;
			if (NA && NB) return A > B ? A : B;
			if (NA) return A;
			if (NB) return B;
			return A > B ? A : B;
		}

		std::string TopicKey() const { return Content.Subject + "." + Content.Predicate; }
	};

	typedef std::shared_ptr<Rumor> RumorPtr;

	// Gossip.cs 72 to 126. One NPC's social side: their memory, what they
	// factually know, the rumours they carry, and which of the player's two
	// faces they belong to.
	//
	// SuspicionTracker came on 29 September as its number alone (the member
	// Suspicion below); the constructor's fifth argument is still absent, and
	// a new tracker always starts at 0, as the C#'s default one does.
	class Gossiper
	{
	public:
		std::string Id;
		std::string DisplayName;
		std::string Circle;       // "day" | "night" | "both"
		std::shared_ptr<MemoryStore>   Memory;
		std::shared_ptr<KnowledgeBase> Knowledge;
		std::vector<RumorPtr>          Rumors;

		// How the player's damage control lands on this NPC. Greed: how
		// readily they take a bribe. Nerve: how hard they are to intimidate
		// (high means will not scare). Loyalty: goodwill toward the player.
		// All 0..1. Nothing in scope reads them; they are here because the
		// constructor sets them and the ruling ported the constructor.
		double Greed;
		double Nerve;
		double Loyalty;

		// Topics this NPC has agreed (or been made) to keep quiet about: they
		// still remember, but they will not pass it on.
		std::vector<std::string> Suppressed;

		// Standing coercion (design doc 6.3, strong hook): the player holds
		// something over them, and NOTHING about the player leaves their
		// lips, current topics and future ones alike. They remember
		// everything.
		bool Leashed;

		// How much this person suspects the player: the number alone since
		// 29 September (Suspicion.h), for StreetVoice::RegardFor. The mill
		// raises it in Tick and CompareNotes (town list 6n), as the C# does.
		SuspicionTracker Suspicion;

		Gossiper(const std::string& InId, const std::string& InDisplayName,
		         const std::shared_ptr<MemoryStore>& InMemory,
		         const std::shared_ptr<KnowledgeBase>& InKnowledge,
		         const std::string& InCircle = "day",
		         double InGreed = 0.5, double InNerve = 0.5, double InLoyalty = 0.5)
			: Id(InId), DisplayName(InDisplayName), Circle(InCircle),
			  Memory(InMemory), Knowledge(InKnowledge),
			  Greed(InGreed), Nerve(InNerve), Loyalty(InLoyalty), Leashed(false)
		{
			// C#: Memory = memory ?? new MemoryStore(id), and the same for
			// Knowledge. The SuspicionTracker line between them is the
			// member's own default, a tracker at 0.
			if (!Memory)    { Memory    = std::make_shared<MemoryStore>(InId); }
			if (!Knowledge) { Knowledge = std::make_shared<KnowledgeBase>(); }
		}

		bool SuppressedHas(const std::string& TopicKey) const
		{
			for (std::vector<std::string>::size_type I = 0; I < Suppressed.size(); ++I)
			{
				if (Suppressed[I] == TopicKey) return true;
			}
			return false;
		}

		bool Holds(const std::string& TopicKey, const std::string& Value) const
		{
			for (std::vector<RumorPtr>::size_type I = 0; I < Rumors.size(); ++I)
			{
				if (Rumors[I]->TopicKey() == TopicKey && Rumors[I]->Content.Value == Value) return true;
			}
			return false;
		}

		// OrderByDescending(Confidence).FirstOrDefault(). C#'s OrderBy is a
		// STABLE sort, so among equal confidences the earliest-added rumour
		// wins; a strictly-greater test reproduces that without sorting at all.
		//
		// BY double.CompareTo, NOT BY `>` (the independent reviewer, 29
		// September). OrderByDescending ranks a NaN below every number, so a
		// NaN copy held first never wins; `>` against a NaN is false both
		// ways, so the NaN held first stayed "best" and hid every real
		// number after it. A save or a planted rumour can carry a NaN.
		RumorPtr Best(const std::string& TopicKey) const
		{
			RumorPtr BestR;
			for (std::vector<RumorPtr>::size_type I = 0; I < Rumors.size(); ++I)
			{
				if (Rumors[I]->TopicKey() != TopicKey) continue;
				if (!BestR || DotNetCompare(Rumors[I]->Confidence, BestR->Confidence) > 0) BestR = Rumors[I];
			}
			return BestR;
		}

		/// The strongest telling of this PARTICULAR version of the story. The
		/// re-tell guards compare against this rather than Best(): two agents
		/// holding conflicting values must settle, not re-copy each other's
		/// version every round (audit 2026-07-27).
		///
		/// Ranked by double.CompareTo, as Best is and for the same reason: a
		/// NaN copy held first must not hide a real one (the independent
		/// reviewer, 29 September; Weigh and Witness read this).
		RumorPtr BestOfValue(const std::string& TopicKey, const std::string& Value) const
		{
			RumorPtr BestR;
			for (std::vector<RumorPtr>::size_type I = 0; I < Rumors.size(); ++I)
			{
				if (Rumors[I]->TopicKey() != TopicKey) continue;
				if (Rumors[I]->Content.Value != Value) continue;
				if (!BestR || DotNetCompare(Rumors[I]->Confidence, BestR->Confidence) > 0) BestR = Rumors[I];
			}
			return BestR;
		}
	};

	typedef std::shared_ptr<Gossiper> GossiperPtr;

	// Gossip.cs 130 to 136. One thing that happened during a gossip round,
	// for the sim report and for the player-facing heat readout.
	struct GossipEvent
	{
		std::string FromId, ToId;
		// C# names this field Rumor. g++ refuses a field whose name changes
		// the meaning of its own type, so the field carries Ref; the type
		// keeps the C# name.
		RumorPtr RumorRef;
		bool Contradiction;   // the rumour collided with a claim the player made to ToId
		bool Exposure;        // a night-life rumour reached a day-circle NPC

		GossipEvent() : Contradiction(false), Exposure(false) {}
	};

	// Gossip.cs 1219 to 1224 (its last class, here before the mill that
	// returns it): one person carrying talk the player can work from.
	struct Lead
	{
		std::string HolderId, HolderName, SourceId, TopicKey, Summary;
		double Confidence = 0;
		bool Sensitive = false;
	};

	// Gossip.cs 142 onward. The rumour network. Seeds first-hand sightings
	// and, each round, lets socially tied NPCs who are together pass talk
	// along.
	class GossipMill
	{
	public:
		// Gossip.cs 149 to 152. Tunables. Confidence is multiplied by tie
		// strength and this factor per hop; a rumour stops spreading once it
		// drops below the share floor.
		double HopDecay;
		double MinConfidenceToShare;
		double ContradictionSuspicion;   // scaled by rumour confidence
		double LeakSuspicion;            // day NPC hears a night rumour, no prior lie
		double RumorHalfLifeHours;       // Gossip.cs 1129: Age's half-life

		// Gossip.cs 154.
		explicit GossipMill(const std::shared_ptr<SocialGraph>& InGraph)
			: HopDecay(0.8), MinConfidenceToShare(0.2),
			  ContradictionSuspicion(0.35), LeakSuspicion(0.12), RumorHalfLifeHours(96),
			  Graph(InGraph ? InGraph : std::make_shared<SocialGraph>()),
			  Offered(0), Dropped(0)
		{
		}

		/// Gossip.cs 160. How strongly two people are connected, 0..1.
		/// Exposed as a passthrough rather than by handing out the graph:
		/// callers outside the mill want to ASK about a relationship, not to
		/// hold and possibly mutate the thing that defines every
		/// relationship.
		double Tie(const std::string& A, const std::string& B) const { return Graph->Tie(A, B); }

		/// Gossip.cs 162: _agents[g.Id] = g. An existing id is REPLACED in
		/// place and keeps its position, which is what a C# Dictionary does
		/// and what Tick's iteration order depends on.
		void Add(const GossiperPtr& G)
		{
			for (std::vector<GossiperPtr>::size_type I = 0; I < AgentList.size(); ++I)
			{
				if (AgentList[I]->Id == G->Id) { AgentList[I] = G; return; }
			}
			AgentList.push_back(G);
		}

		/// Gossip.cs 186 to 187. NULL IS A MISS, NOT A THROW.
		/// Dictionary.TryGetValue(null) raises ArgumentNullException, the one
		/// lookup method whose whole purpose is not to throw. SaveChaos
		/// reached it through SaveCodec, from a saved agent record whose id
		/// key had been deleted, and the exception escaped Restore past the
		/// only type the front end catches. "No agent by that name" is the
		/// honest answer for a name that is not there. A std::string cannot
		/// be null, so the C#'s null guard has nothing to guard here and the
		/// miss is the only outcome left; an empty id simply matches no
		/// agent.
		GossiperPtr Get(const std::string& Id) const
		{
			for (std::vector<GossiperPtr>::size_type I = 0; I < AgentList.size(); ++I)
			{
				if (AgentList[I]->Id == Id) return AgentList[I];
			}
			return GossiperPtr();
		}

		const std::vector<GossiperPtr>& Agents() const { return AgentList; }

		/// Gossip.cs 202 to 203. HOW MANY SIGHTINGS WERE OFFERED TO THIS
		/// MILL, AND HOW MANY IT REFUSED BECAUSE IT HAD NEVER HEARD OF THE
		/// WITNESS.
		///
		/// Instance fields rather than statics: a test builds several mills
		/// and a static count would sum them into a number describing no
		/// world at all. Dropped is a subset of Offered by construction, both
		/// incremented on the same call before and after the one branch, so
		/// the ratio is a real fraction and not two counters that happen to
		/// sit near each other.
		///
		/// A non-zero Dropped is not automatically a bug. It IS automatically
		/// a question, and there was no way to ask it before.
		int WitnessesOffered() const { return Offered; }
		int WitnessesDropped() const { return Dropped; }

		/// Gossip.cs 233 to 244. How many rumour summaries say `word` out
		/// loud.
		///
		/// WHY THIS IS IN CORE AND NOT A GREP. A rumour has two halves that
		/// look alike and are not: Content is a FACT, keyed on ids, and
		/// Summary is PROSE that a person reads on the ledger screen and a
		/// model reads in a prompt. The id for the player is the literal
		/// string "player", which is correct in a Fact and is not a word any
		/// character in this game would ever say. It shipped: a panel
		/// readback from 0eeee6d held four rumours reading "Mitch says it was
		/// player, and came to say so". A grep cannot find it because the
		/// leak is in the RUNNING world, not in the source.
		int SummariesSaying(const std::string& Word) const
		{
			if (Word.empty()) return 0;
			int N = 0;
			for (std::vector<GossiperPtr>::size_type I = 0; I < AgentList.size(); ++I)
			{
				const GossiperPtr& G = AgentList[I];
				if (!G) continue;
				for (std::vector<RumorPtr>::size_type J = 0; J < G->Rumors.size(); ++J)
				{
					if (G->Rumors[J] && SaysWord(G->Rumors[J]->Summary, Word)) N++;
				}
			}
			return N;
		}

		/// Gossip.cs 248 to 262. Does `text` contain `word` as a whole word?
		/// Case-insensitive, because a sentence that starts "Player was
		/// seen..." is the same bug. WHOLE WORDS: "a player's entrance" is a
		/// leak; "two players" is a different word and matching it would make
		/// the number un-actionable.
		static bool SaysWord(const std::string& Text, const std::string& Word)
		{
			if (Text.empty() || Word.empty()) return false;
			for (std::string::size_type I = 0; I + Word.size() <= Text.size(); )
			{
				const std::string::size_type At = IndexOfIgnoreCase(Text, Word, I);
				if (At == std::string::npos) return false;
				const std::string::size_type End = At + Word.size();
				const bool bLeftFree  = At == 0 || !IsWordChar(Text[At - 1]);
				const bool bRightFree = End >= Text.size() || !IsWordChar(Text[End]);
				if (bLeftFree && bRightFree) return true;
				I = At + 1;
			}
			return false;
		}

		/// Gossip.cs 264. char.IsLetterOrDigit is Unicode-aware in C# and
		/// this is ASCII, which is the same answer for every string this
		/// probe builds and is named here rather than assumed.
		static bool IsWordChar(char C)
		{
			return std::isalnum((unsigned char)C) != 0 || C == '_';
		}

		/// Gossip.cs 270 to 378. A first-hand sighting enters the network.
		/// Confidence defaults to certain; a disguise (or distance, or
		/// darkness) passes less than 1.0: the witness saw SOMETHING but
		/// cannot swear to who, and everything downstream (spread, heat,
		/// bribe prices) inherits that doubt. `Rung` is how well they saw the
		/// man (Rumor::OriginRung), -1 when the caller does not give it.
		/// Gossip.cs WitnessRemembering (the review's B7): filed first-hand, but
		/// remembered as what happened, never "I saw it myself" of something
		/// said to their face; no memory at all when Remembered is empty.
		void WitnessRemembering(const std::string& WitnessId, const Fact& Content, const std::string& Summary,
		                        bool bSensitive, const GameTime& Now, const std::string& Remembered, double Confidence = 1.0)
		{
			const GossiperPtr G = Get(WitnessId);
			const size_t Before = G && G->Memory ? G->Memory->Events.size() : 0;
			Witness(WitnessId, Content, Summary, bSensitive, Now, Confidence);
			if (!G || !G->Memory) return;
			G->Memory->KeepFirst((int)Before);
			if (!Remembered.empty()) G->Memory->Append(MemoryEvent(Now, "conversation", bSensitive ? 0.9 : 0.6, Remembered));
		}

		void Witness(const std::string& WitnessId, const Fact& Content,
		             const std::string& Summary, bool bSensitive, const GameTime& Now,
		             double Confidence = 1.0, bool bIndelible = false, int Rung = -1)
		{
			GossiperPtr W = Get(WitnessId);
			// A DROPPED WITNESS IS NOW A NUMBER, BECAUSE IT WAS NOTHING AT
			// ALL AND IT COST THE PROJECT ITS ENTIRE CROWD.
			//
			// This line was `if (w == null) return;`, an early return with no
			// trace. Every crowd walker's body was spawned under a person's
			// name while their agent was registered under r0000-style ids, so
			// seven hundred people witnessed things for months and not one
			// observation was ever stored. Nothing anywhere went red: a mill
			// that files nothing and a mill that is never told anything
			// produce identical output, which is rule 3b in its purest form.
			//
			// The behaviour is unchanged on purpose: refusing an unknown
			// witness is CORRECT, and creating one here would invent people
			// the world does not have. What changes is that it leaves a mark.
			//
			// Offered is the denominator and it counts BEFORE the refusal, so
			// "nothing was offered" and "everything offered was refused"
			// cannot read the same.
			Offered++;
			// A SIGHTING AT NaN IS DROPPED AND COUNTED (town list 6bw).
			if (!W || IsNaNBits(Confidence)) { Dropped++; return; }
			Confidence = Clamp(Confidence, 0.0, 1.0);
			if (Confidence >= 0.95) W->Knowledge->Learn(Content);   // only certainty becomes hard knowledge
			Rung = Rung < -1 ? -1 : (Rung > 4 ? 4 : Rung);         // C#: Math.Clamp(rung, -1, 4)
			const std::string Topic = Content.Subject + "." + Content.Predicate;
			// WHERE A LOOK IS KNOWN, THEIR OWN SIGHTING IS KEPT BESIDE WHAT
			// THEY HEARD (town list 6n, the independent check): folded into
			// the one copy, a vaguer look of their own erased a telling that
			// had named him, and a heard body at certainty meant a later look
			// of their own was never theirs. Where nobody gave a rung, nothing
			// below changes.
			bool bRungKnown = Rung >= 0;
			for (std::vector<RumorPtr>::size_type I = 0; I < W->Rumors.size(); ++I)
			{
				const RumorPtr& X = W->Rumors[I];
				if (X->TopicKey() == Topic && X->Content.Value == Content.Value && X->OriginRung >= 0) bRungKnown = true;
			}
			if (bRungKnown)
			{
				RumorPtr Own;
				for (std::vector<RumorPtr>::size_type I = 0; I < W->Rumors.size(); ++I)
				{
					const RumorPtr& X = W->Rumors[I];
					if (X->TopicKey() == Topic && X->Content.Value == Content.Value && X->Hops == 0
					    && (!Own || NotFiniteBits(Own->Confidence) || X->Confidence > Own->Confidence)) Own = X;
				}
				if (!Own)
				{
					RumorPtr R = std::make_shared<Rumor>(Content);
					R->OriginId = WitnessId; R->Summary = Summary;
					R->Confidence = Confidence; R->Hops = 0; R->Sensitive = bSensitive;
					R->Indelible = bIndelible; R->OriginRung = Rung;
					W->Rumors.push_back(R);
				}
				else
				{
					// A second look of their own: the better of the two, as below.
					Own->OriginRung = Rumor::MergeRung(Own->OriginRung, Rung);
					if (bIndelible && !Own->Indelible)
					{
						Own->Indelible = true;
						Own->Confidence = NotFiniteBits(Own->Confidence) ? Confidence : DotNetMax(Own->Confidence, Confidence);
						Own->Summary = Summary;
						if (Own->Confidence >= 0.95) W->Knowledge->Learn(Content);
					}
					else if (Confidence > Own->Confidence || NotFiniteBits(Own->Confidence))   // a copy at NaN gives way (town list 6bw)
					{
						Own->Confidence = Confidence;
						Own->Summary = Summary;
					}
				}
			}
			else
			{
				RumorPtr Already = W->BestOfValue(Topic, Content.Value);
				if (!Already)
				{
					RumorPtr R = std::make_shared<Rumor>(Content);
					R->OriginId = WitnessId; R->Summary = Summary;
					R->Confidence = Confidence; R->Hops = 0; R->Sensitive = bSensitive;
					R->Indelible = bIndelible;
					W->Rumors.push_back(R);
				}
				else if (bIndelible && !Already->Indelible)
				{
					// Somebody who half-heard a scuffle later learns there was a
					// body in it. The doubtful version does not survive that: it
					// is upgraded in place, at whatever certainty the body
					// carries, rather than sitting alongside as a live maybe.
					Already->Indelible = true;
					Already->Confidence = NotFiniteBits(Already->Confidence) ? Confidence : DotNetMax(Already->Confidence, Confidence);
					Already->Hops = 0;
					Already->Summary = Summary;
					if (Already->Confidence >= 0.95) W->Knowledge->Learn(Content);
				}
				else if (Confidence > Already->Confidence || NotFiniteBits(Already->Confidence))   // a copy at NaN gives way (town list 6bw)
				{
					// A clearer second look strengthens a doubtful first one.
					// This used to drop the repeat on the floor, so no later
					// sighting could ever firm up an early maybe (audit
					// 2026-07-27).
					Already->Confidence = Confidence;
					Already->Hops = 0;
					Already->Summary = Summary;
				}
			}
			// THE MEMORY LINE IS WRITTEN ON EVERY CALL, including the fourth
			// branch where nothing about the rumour changed: seeing it again
			// is a thing that happened to them.
			//
			// THE COMMA IN "I think I saw it, couldn't swear to it" IS A
			// CORRECTION MADE IN BOTH ENGINES IN ONE BATCH. Gossip.cs 324 had
			// an em-dash there, and this run writes that string into a
			// committed memory file, which the formatting law forbids. The C#
			// was changed to the comma in the same commit as this port, so
			// the two still agree line for line and the golden table pins the
			// exact sentence.
			W->Memory->Append(MemoryEvent(Now, "observation", bSensitive ? 0.9 : 0.6,
				Confidence >= 0.95 ? "I saw it myself: " + Summary
				                   : "I think I saw it, couldn't swear to it: " + Summary));
		}

		/// MICKEY'S OWN HANDLE IT PRIVATELY (Jafar's ruling of 1 October: "Ron and
		/// Sheila ... handle what they saw privately: a word with him, a warning, a
		/// favour owed"; grassing is the last thing a loyal person does): who keeps
		/// his deeds to themselves, set from the cast (CastDay::MickeysOwn) whenever
		/// the town's rounds run with it. They pass a story of his deeds (a
		/// sensitive story about him) to nobody, and their talk is not the street's
		/// (PoliceFile::Loudness); what shows to his face is still theirs. A body is
		/// not a story: it travels as ever. Unset (the C#'s null): nobody does, as before.
		std::function<bool(const std::string&)> KeepsHisDeedsFor;

		bool KeepsHisDeeds(const Gossiper* Teller, const RumorPtr& R) const
		{
			return KeepsHisDeedsFor && Teller != nullptr && R && !R->Indelible && R->Sensitive
			    && R->Content.Subject == "player" && KeepsHisDeedsFor(Teller->Id);
		}

		/// Whether this person keeps his deeds to themselves (KeepsHisDeedsFor).
		bool KeepsHisDeedsToThemselves(const std::string& Id) const { return KeepsHisDeedsFor && KeepsHisDeedsFor(Id); }

		/// Gossip.cs 433 to 541. One gossip round. `together` decides which
		/// tied pairs are actually in a position to talk this round
		/// (co-located in game, or always true in tests). Returns everything
		/// that propagated, for logging.
		typedef std::function<bool(const std::string&, const std::string&)> TogetherFn;

		std::vector<GossipEvent> Tick(const GameTime& Now, const TogetherFn& Together = TogetherFn())
		{
			std::vector<GossipEvent> Events;

			// Snapshot each agent's rumours so a rumour picked up THIS round
			// does not also hop again in the same round (keeps spread to one
			// hop per round, and the loop deterministic and terminating).
			std::vector<std::pair<std::string, std::vector<RumorPtr> > > Snapshot;
			for (std::vector<GossiperPtr>::size_type I = 0; I < AgentList.size(); ++I)
			{
				Snapshot.push_back(std::make_pair(AgentList[I]->Id, AgentList[I]->Rumors));
			}

			for (std::vector<GossiperPtr>::size_type SI = 0; SI < AgentList.size(); ++SI)
			{
				const GossiperPtr Speaker = AgentList[SI];
				// The speaker's copies in telling order, built once per speaker
				// (the fourth pass: once per pair it cost four times the tick).
				const std::vector<TellingSlot> Slots = TellingSlots(SnapshotOf(Snapshot, Speaker->Id));
				const std::vector<std::string> Contacts = Graph->Contacts(Speaker->Id);
				for (std::vector<std::string>::size_type CI = 0; CI < Contacts.size(); ++CI)
				{
					const std::string& ListenerId = Contacts[CI];
					GossiperPtr Listener = Get(ListenerId);
					if (!Listener) continue;
					// C#: if (together != null && !together(a, b)) continue.
					// An unset std::function is the null.
					if (Together && !Together(Speaker->Id, ListenerId)) continue;

					const double TieW = Graph->Tie(Speaker->Id, ListenerId);
					if (TieW <= 0) continue;
					// One story, one telling a round: where a rung is involved a
					// speaker may hold their own look and what they heard side by
					// side, and each copy raised the listener's suspicion again
					// (the independent check's second pass). The surest copy of a
					// version is the telling; the rest go in quietly (the third pass).
					// C#: a HashSet made on first use; its absence and its
					// emptiness answer every Add alike.
					std::vector<std::string> ToldThisRound, NamedThisTelling;
					const double Hop = HopDecay;
					const std::vector<Told> Order = SurestFirst(Slots,
						[TieW, Hop](const Rumor& X) { return X.Indelible ? X.Confidence : X.Confidence * TieW * Hop; });
					for (std::vector<Told>::size_type RI = 0; RI < Order.size(); ++RI)
					{
						const RumorPtr& R = Order[RI].R;
						// NEVER TOLD AT NaN OR AN INFINITY (town list 6bw); a
						// copy at either is not held (Gossip.cs NotFinite).
						if (NotFiniteBits(R->Confidence)) continue;
						if (R->Confidence < MinConfidenceToShare && !R->Indelible) continue;
						// Money and hooks buy silence about STORIES. Nobody
						// keeps a body to themselves because they were paid to.
						if (!R->Indelible && Speaker->SuppressedHas(R->TopicKey())) continue;   // bribed or scared into silence
						if (KeepsHisDeeds(Speaker.get(), R)) continue;   // Mickey's own handle it privately
						if (!R->Indelible && Speaker->Leashed && R->Content.Subject == "player") continue;   // held by a hook
						// A body arrives at the far end of the street exactly
						// as true as it left. Hop decay is how a story turns
						// into a maybe; this is not a story.
						const double Passed = R->Indelible ? R->Confidence : R->Confidence * TieW * HopDecay;
						if (NotFiniteBits(Passed) || Passed < MinConfidenceToShare) continue;   // a tie at NaN passes nothing (town list 6bw)

						// Do not re-tell something the listener already holds
						// at least as strongly: stops rumours amplifying by
						// bouncing back and forth. Compared against the
						// listener's best rumour OF THIS VALUE, not the
						// topic's best overall: when two agents hold
						// conflicting values, comparing against the overall
						// best let each re-add an identical copy of the
						// other's version every round, growing Rumors and
						// Memory without bound (audit 2026-07-27).
						Telling Weighed = Weigh(*Listener, *R, Passed);
						if (Weighed == Telling::Held) continue;
						if (Weighed == Telling::New && Order[RI].bHasVersion && !AddOnce(ToldThisRound, Order[RI].Version)) Weighed = Telling::Quiet;

						RumorPtr Heard = std::make_shared<Rumor>(R->Content);
						Heard->OriginId = R->OriginId; Heard->Summary = R->Summary;
						// C#'s int + 1 wraps (unchecked); a signed overflow is
						// undefined in C++, and a save can set hops to INT_MAX
						// (the independent reviewer, 29 September). So the
						// addition is done unsigned and wraps as the C#'s does.
						Heard->Confidence = Passed; Heard->Hops = (int)((unsigned)R->Hops + 1u);
						Heard->Sensitive = R->Sensitive; Heard->Indelible = R->Indelible;
						Heard->OriginRung = R->OriginRung;
						Listener->Rumors.push_back(Heard);
						// THE LEAK AND THE CONTRADICTION FIRE ONCE A TELLING, on the
						// first copy that names him and reaches the listener (the
						// town's A5 fix and its independent check, 30 September).
						const bool bFirstNaming = Heard->NamesHim() && AddOnce(NamedThisTelling, R->TopicKey());
						const std::string WhyContra = "a rumor about " + R->TopicKey() + " contradicts what the new owner told me";
						const char* const WhyLeak = "heard something that doesn't fit the person I thought I knew";
						if (Weighed == Telling::Quiet)
						{
							// A naming is new to them though the story is not: it
							// is remembered, so they can say who told them (the
							// third pass).
							if (Heard->OriginRung >= 4)
								Listener->Memory->Append(MemoryEvent(Now, "heard", Clamp(Passed * 0.8, 0.2, 0.85),
									"I heard from " + Speaker->DisplayName + " that " + R->Summary));
							if (bFirstNaming && NamingReaches(*Listener, *R, Passed, WhyContra, WhyLeak).first)
								Listener->Memory->Append(MemoryEvent(Now, "observation", 0.85,
									"What I heard about " + ReplaceAll(R->TopicKey(), "player.", "")
									+ " doesn't match what they told me to my face."));
							if (Heard->Indelible && Heard->Confidence >= 0.95) Listener->Knowledge->Learn(Heard->Content);
							continue;
						}
						Listener->Memory->Append(MemoryEvent(Now, "heard",
							Clamp(Passed * 0.8, 0.2, 0.85),
							"I heard from " + Speaker->DisplayName + " that " + R->Summary));

						GossipEvent Ev;
						Ev.FromId = Speaker->Id; Ev.ToId = ListenerId; Ev.RumorRef = Heard;

						// Consequence 1: the rumour collides with a claim the
						// player made to this listener, and the lie is
						// exposed. Consequence 2: a night-life secret reaches
						// someone from the player's daytime world, and the
						// double life springs a leak. Both only on a telling
						// that names him (NamingReaches).
						if (bFirstNaming)
						{
							const std::pair<bool, bool> Reached = NamingReaches(*Listener, *R, Passed, WhyContra, WhyLeak);
							if (Reached.first)
								Listener->Memory->Append(MemoryEvent(Now, "observation", 0.85,
									"What I heard about " + ReplaceAll(R->TopicKey(), "player.", "")
									+ " doesn't match what they told me to my face."));
							Ev.Contradiction = Reached.first;
							Ev.Exposure = Reached.second;
						}

						// AFTER the contradiction check, never before: an
						// indelible rumour arrives at certainty however many
						// mouths it crossed, and certainty is hard knowledge.
						// Learning it first would make the listener's own new
						// fact agree with itself and swallow the very
						// contradiction the killing is supposed to expose.
						if (Heard->Indelible && Heard->Confidence >= 0.95)
						{
							Listener->Knowledge->Learn(Heard->Content);
						}

						Events.push_back(Ev);
					}
				}
			}
			return Events;
		}

		/// Gossip.cs 543 to 559. WHAT A TELLING GIVES A LISTENER: nothing, if
		/// they hold this version of the story at least as surely (the old
		/// guard, which stops stories breeding), and, when the telling
		/// carries its first teller's rung, a copy at least as well
		/// identified (town list 6n, the independent check: a telling that
		/// named him was dropped because a vaguer version was already held
		/// more surely). With no rung it is the old guard exactly.
		///
		/// Only a naming counts (a heard rung matters only at 4), and only a
		/// naming held at least as surely stops it (the second pass: a faded
		/// one at 0.1 blocked a fresh one). A telling let through for its
		/// naming alone, or a second copy of a version already told this
		/// round, is the same story already held, so it is kept quietly: no
		/// second raise of suspicion and no event. A memory only when it
		/// names him, for the name is news and they must be able to say who
		/// told them (the third pass).
		enum class Telling { New, Held, Quiet };

		/// Gossip.cs 631 to 724. Suspicion-driven escalation (design doc
		/// 6.4): a suspicious NPC does not wait for chance encounters, they
		/// seek someone out and ASK. A directed, deterministic exchange: the
		/// partner tells the checker everything they are willing to share
		/// about the player (suppression and leashes respected; leashed
		/// checkers do not check, the hook's protection). Same consequence
		/// rules as organic gossip: contradictions with the player's claims
		/// and cross-circle leaks move the checker's suspicion further.
		std::vector<GossipEvent> CompareNotes(const std::string& CheckerId, const std::string& PartnerId,
		                                      const GameTime& Now)
		{
			std::vector<GossipEvent> Events;
			GossiperPtr Checker = Get(CheckerId);
			GossiperPtr Partner = Get(PartnerId);
			if (!Checker || !Partner || Checker->Leashed) return Events;

			Checker->Memory->Append(MemoryEvent(Now, "conversation", 0.6,
				"I asked " + Partner->DisplayName + " straight out what they knew about the new owner."));

			const double TieW = DotNetMax(Graph->Tie(CheckerId, PartnerId), 0.5);   // asking directly beats a weak tie
			// A BODY SURVIVES ALL THREE OF THESE, AND HERE IT DID NOT (the
			// C#, 4 August): Tick exempts an INDELIBLE rumour from the
			// confidence floor, from suppression and from the leash, and this
			// method exempted it from none of them, so a hook or a bribe on a
			// witness stopped them answering a direct question about a corpse
			// they saw while the same witness would still have volunteered it
			// in ordinary talk. AND THE PARTNER'S LEASH IS NO LONGER TESTED
			// INSIDE THE LOOP: it does not depend on the rumour.
			std::vector<std::string> AskedToldThisRound, AskedNamed;
			const double Hop = HopDecay;
			const std::vector<RumorPtr> Asked = Partner->Rumors;   // C#: partner.Rumors.ToList()
			const std::vector<Told> Order = SurestFirst(TellingSlots(Asked),
				[TieW, Hop](const Rumor& X) { return X.Indelible ? X.Confidence : X.Confidence * TieW * Hop; });
			for (std::vector<Told>::size_type RI = 0; RI < Order.size(); ++RI)
			{
				const RumorPtr& R = Order[RI].R;
				if (NotFiniteBits(R->Confidence)) continue;   // never told at NaN or an infinity, as Tick (town list 6bw)
				if (R->Content.Subject != "player") continue;
				if (R->Confidence < MinConfidenceToShare && !R->Indelible) continue;
				if (!R->Indelible && Partner->SuppressedHas(R->TopicKey())) continue;
				if (!R->Indelible && Partner->Leashed) continue;
				if (KeepsHisDeeds(Partner.get(), R)) continue;   // Mickey's own handle it privately

				// A BODY ARRIVES AS TRUE AS IT LEFT, asked about or not (town
				// list 6n): this used the decay and dropped the mark, so asking
				// a witness about a killing gave a weakened copy that could be
				// talked away, while ordinary talk (Tick) passed it on whole.
				const double Passed = R->Indelible ? R->Confidence : R->Confidence * TieW * HopDecay;
				if (NotFiniteBits(Passed) || Passed < MinConfidenceToShare) continue;   // as Tick
				// Value-aware for the same reason as Tick's guard: conflicting
				// versions must settle, not breed (audit 2026-07-27).
				Telling Weighed = Weigh(*Checker, *R, Passed);
				if (Weighed == Telling::Held) continue;
				if (Weighed == Telling::New && Order[RI].bHasVersion && !AddOnce(AskedToldThisRound, Order[RI].Version)) Weighed = Telling::Quiet;

				RumorPtr Heard = std::make_shared<Rumor>(R->Content);
				Heard->OriginId = R->OriginId; Heard->Summary = R->Summary;
				// Wraps as the C#'s int + 1 does, as in Tick.
				Heard->Confidence = Passed; Heard->Hops = (int)((unsigned)R->Hops + 1u);
				Heard->Sensitive = R->Sensitive; Heard->Indelible = R->Indelible;
				Heard->OriginRung = R->OriginRung;
				Checker->Rumors.push_back(Heard);
				const bool bFirstNaming = Heard->NamesHim() && AddOnce(AskedNamed, R->TopicKey());
				const std::string WhyContra = "what " + Partner->DisplayName + " told me contradicts what the new owner said to my face";
				const char* const WhyLeak = "I went asking, and I did not like the answer";
				if (Weighed == Telling::Quiet)
				{
					if (Heard->OriginRung >= 4)
						Checker->Memory->Append(MemoryEvent(Now, "heard", Clamp(Passed * 0.8, 0.2, 0.85),
							Partner->DisplayName + " told me, when I asked: " + R->Summary));
					if (bFirstNaming) NamingReaches(*Checker, *R, Passed, WhyContra, WhyLeak);
					if (Heard->Indelible && Heard->Confidence >= 0.95) Checker->Knowledge->Learn(Heard->Content);
					continue;
				}
				Checker->Memory->Append(MemoryEvent(Now, "heard",
					Clamp(Passed * 0.8, 0.2, 0.85),
					Partner->DisplayName + " told me, when I asked: " + R->Summary));

				GossipEvent Ev;
				Ev.FromId = PartnerId; Ev.ToId = CheckerId; Ev.RumorRef = Heard;
				if (bFirstNaming)
				{
					const std::pair<bool, bool> Reached = NamingReaches(*Checker, *R, Passed, WhyContra, WhyLeak);
					Ev.Contradiction = Reached.first;
					Ev.Exposure = Reached.second;
				}
				// A body heard of at certainty is hard knowledge, as in Tick,
				// and after the contradiction check for the same reason (the
				// independent check: asked about, it was held but never
				// learned).
				if (Heard->Indelible && Heard->Confidence >= 0.95)
				{
					Checker->Knowledge->Learn(Heard->Content);
				}
				Events.push_back(Ev);
			}
			return Events;
		}

	private:
		/// Gossip.cs 579 to 584. One place in a speaker's telling: a copy
		/// told as it always was, or every copy of a version that carries a
		/// rung, grouped where the first of them stood. Built once per
		/// speaker, the key once per copy; only the order within a group
		/// waits for the listener, since it turns on the tie between them.
		/// C#'s `Copies == null` is bGrouped false here.
		struct TellingSlot
		{
			RumorPtr              Single;
			std::string           Version;
			std::vector<RumorPtr> Copies;
			bool                  bGrouped;
			TellingSlot() : bGrouped(false) {}
		};

		/// One copy as SurestFirst yields it, with its version ("topic=value")
		/// when the version carries a rung; C#'s null version is bHasVersion
		/// false.
		struct Told
		{
			RumorPtr    R;
			std::string Version;
			bool        bHasVersion;
			Told() : bHasVersion(false) {}
		};

		/// Gossip.cs 586 to 612.
		static std::vector<TellingSlot> TellingSlots(const std::vector<RumorPtr>& Copies)
		{
			std::vector<TellingSlot> Slots;
			Slots.reserve(Copies.size());
			bool bAnyRung = false;
			for (std::vector<RumorPtr>::size_type I = 0; I < Copies.size(); ++I)
			{
				if (Copies[I]->OriginRung >= 0) { bAnyRung = true; break; }
			}
			if (!bAnyRung)
			{
				for (std::vector<RumorPtr>::size_type I = 0; I < Copies.size(); ++I)
				{
					TellingSlot S; S.Single = Copies[I];
					Slots.push_back(S);
				}
				return Slots;
			}
			std::vector<std::string> Keys(Copies.size());
			std::vector<std::string> RungVersions;   // C#: HashSet
			for (std::vector<RumorPtr>::size_type I = 0; I < Copies.size(); ++I)
			{
				Keys[I] = Copies[I]->TopicKey() + "=" + Copies[I]->Content.Value;
				if (Copies[I]->OriginRung >= 0) AddOnce(RungVersions, Keys[I]);
			}
			std::vector<std::pair<std::string, std::vector<TellingSlot>::size_type> > At;   // C#: Dictionary
			for (std::vector<RumorPtr>::size_type I = 0; I < Copies.size(); ++I)
			{
				if (!Contains(RungVersions, Keys[I]))
				{
					TellingSlot S; S.Single = Copies[I];
					Slots.push_back(S);
					continue;
				}
				bool bFound = false;
				for (std::vector<std::pair<std::string, std::vector<TellingSlot>::size_type> >::size_type K = 0;
				     K < At.size(); ++K)
				{
					if (At[K].first == Keys[I]) { Slots[At[K].second].Copies.push_back(Copies[I]); bFound = true; break; }
				}
				if (bFound) continue;
				At.push_back(std::make_pair(Keys[I], Slots.size()));
				TellingSlot S; S.bGrouped = true; S.Version = Keys[I]; S.Copies.push_back(Copies[I]);
				Slots.push_back(S);
			}
			return Slots;
		}

		/// Gossip.cs 561 to 577. The copies a speaker tells, in their own
		/// order, except that where a version carries a rung its copies are
		/// told surest first, so the round's one telling is the surest as it
		/// would arrive (the third pass: a faint heard copy was told in full
		/// and the speaker's own sure look went in quietly, so the listener's
		/// suspicion rose by a third). With no rung anywhere the order is
		/// exactly as held.
		///
		/// EAGER RATHER THAN A C# ITERATOR, and the same list: the C# yields
		/// lazily, but nothing the loops over it do between two copies can
		/// change a speaker's copy (a telling makes a NEW rumour for the
		/// listener), so a group ordered when it is reached and a group
		/// ordered up front are one order. OrderByDescending is a stable
		/// sort on double.CompareTo, and so is this.
		static std::vector<Told> SurestFirst(const std::vector<TellingSlot>& Slots,
		                                     const std::function<double(const Rumor&)>& PassedOf)
		{
			std::vector<Told> Out;
			for (std::vector<TellingSlot>::size_type I = 0; I < Slots.size(); ++I)
			{
				const TellingSlot& Slot = Slots[I];
				if (!Slot.bGrouped)
				{
					Told T; T.R = Slot.Single;
					Out.push_back(T);
					continue;
				}
				std::vector<std::pair<double, RumorPtr> > Keyed;
				for (std::vector<RumorPtr>::size_type C = 0; C < Slot.Copies.size(); ++C)
				{
					Keyed.push_back(std::make_pair(PassedOf(*Slot.Copies[C]), Slot.Copies[C]));
				}
				if (Keyed.size() != 1)
				{
					std::stable_sort(Keyed.begin(), Keyed.end(),
						[](const std::pair<double, RumorPtr>& A, const std::pair<double, RumorPtr>& B)
						{ return DotNetCompare(A.first, B.first) > 0; });
				}
				for (std::vector<std::pair<double, RumorPtr> >::size_type C = 0; C < Keyed.size(); ++C)
				{
					Told T; T.R = Keyed[C].second; T.Version = Slot.Version; T.bHasVersion = true;
					Out.push_back(T);
				}
			}
			return Out;
		}

		/// Gossip.cs 614 to 623.
		/// Gossip.cs 619 to 625. How much stronger a telling must be than what
		/// the listener holds to be news to them. Not zero: ageing multiplies
		/// both copies by the same factor, and the same story told again the
		/// same way then comes out one rounding step stronger about half the
		/// time, and was taken for news, a copy and a raise each time (town
		/// list 6bs).
		static constexpr double SameStrength = 1e-9;

		/// Gossip.cs NamingReaches: the contradiction, or else the leak, of a
		/// telling that names him; (contradiction, exposure).
		std::pair<bool, bool> NamingReaches(Gossiper& Listener, const Rumor& R, double Passed,
		                                    const std::string& Why, const std::string& WhyLeak)
		{
			if (Listener.Knowledge->CheckClaim(R.Content) == ClaimResult::Contradiction)
			{
				Listener.Suspicion.Raise(ContradictionSuspicion * Passed, Why);
				return std::make_pair(true, false);
			}
			if (R.Sensitive && Listener.Circle == "day")
			{
				Listener.Suspicion.Raise(LeakSuspicion * Passed, WhyLeak);
				return std::make_pair(false, true);
			}
			return std::make_pair(false, false);
		}

		static Telling Weigh(const Gossiper& Listener, const Rumor& R, double Passed)
		{
			const RumorPtr Existing = Listener.BestOfValue(R.TopicKey(), R.Content.Value);
			if (!Existing || NotFiniteBits(Existing->Confidence) || Existing->Confidence < Passed - SameStrength) return Telling::New;
			if (!R.NamesHim()) return Telling::Held;
			for (std::vector<RumorPtr>::size_type I = 0; I < Listener.Rumors.size(); ++I)
			{
				const RumorPtr& X = Listener.Rumors[I];
				if (X->TopicKey() == R.TopicKey() && X->Content.Value == R.Content.Value
				    && X->NamesHim() && !NotFiniteBits(X->Confidence) && X->Confidence >= Passed - SameStrength)
					return Telling::Held;
			}
			return Telling::Quiet;
		}

		/// HashSet<string>.Add: true if it was not there and now is.
		static bool AddOnce(std::vector<std::string>& Set, const std::string& V)
		{
			if (Contains(Set, V)) return false;
			Set.push_back(V);
			return true;
		}

		static bool Contains(const std::vector<std::string>& Set, const std::string& V)
		{
			for (std::vector<std::string>::size_type I = 0; I < Set.size(); ++I)
			{
				if (Set[I] == V) return true;
			}
			return false;
		}

	public:
		/// HIS NAME AND HIS ARRIVAL, the street's plain facts about him: never a
		/// lead, never his exposure, never what a hook is spent silencing (the
		/// port's independent check, 30 September: a hook could be spent on
		/// "Mickey's nephew has come" while a deed still showed). Gossip.cs 800:
		/// PlayerIdentity.IsNameStory(r) || DayOne.IsArrival(r). Both headers
		/// include this one, so their two tests are spelled here as
		/// PlayerIdentity::IsNameStory and DayOne::IsArrival spell them (topics
		/// "player.name" and "player.arrived"); the golden's FixArrival row
		/// pins them.
		static bool PlainFactOfHim(const RumorPtr& R)
		{
			return R && R->Content.Subject == "player" && (R->TopicKey() == "player.name" || R->TopicKey() == "player.arrived");
		}

		/// Gossip.cs 802 to 834, ported 30 September for the town's fix of his
		/// arrival. Everyone currently carrying (and willing to spread) talk
		/// about the subject, strongest first: the leads the player works from
		/// to decide who to lean on. A leash holds everything except a body;
		/// his name and his arrival are never a lead. OrderByDescending is a
		/// stable sort on double.CompareTo, and so is this.
		std::vector<Lead> Leads(const std::string& Subject = "player") const
		{
			const std::string Subj = ToLowerInvariantAscii(Subject);
			std::vector<Lead> List;
			for (std::vector<GossiperPtr>::size_type I = 0; I < AgentList.size(); ++I)
			{
				const GossiperPtr& A = AgentList[I];
				const bool bLeashed = A->Leashed && Subj == "player";
				for (std::vector<RumorPtr>::size_type J = 0; J < A->Rumors.size(); ++J)
				{
					const RumorPtr& R = A->Rumors[J];
					// His name and his arrival are the street's plain facts, never a lead
					// (the fourth review of 6ch; the port's review, 30 September, of the arrival).
					if (R->Content.Subject == Subj && R->Confidence >= MinConfidenceToShare && !PlainFactOfHim(R)
					    && (!bLeashed || R->Indelible)
					    && (!A->SuppressedHas(R->TopicKey()) || R->Indelible))
					{
						Lead L;
						L.HolderId = A->Id; L.HolderName = A->DisplayName; L.SourceId = R->OriginId;
						L.TopicKey = R->TopicKey(); L.Summary = R->Summary; L.Confidence = R->Confidence; L.Sensitive = R->Sensitive;
						List.push_back(L);
					}
				}
			}
			std::stable_sort(List.begin(), List.end(), [](const Lead& X, const Lead& Y) { return DotNetCompare(X.Confidence, Y.Confidence) > 0; });
			return List;
		}

		/// Gossip.cs 887 to 905: the split of what the street holds about him,
		/// his own face against his people's. Its Sentence (the words the
		/// ledger screen reads) is not ported.
		struct Exposure
		{
			int Yours = 0, Delegated = 0;
			double YoursWeight = 0, DelegatedWeight = 0;
			int Stories() const { return Yours + Delegated; }
			double Weight() const { return YoursWeight + DelegatedWeight; }
			/// The share of the case against him his own face put there; -1 when
			/// there is no case at all.
			double YoursShare() const { return Weight() <= 0 ? -1 : YoursWeight / Weight(); }
		};

		/// Gossip.cs 868 to 884, ported 30 September for the town's fix of his
		/// arrival: how much of what the street holds about him came from him
		/// being seen, and how much from his people. ViaOthers decides which
		/// predicates are somebody else's round; empty is the C#'s null (none
		/// of it delegated). An empty Subject is the C#'s null, "player".
		Exposure ExposureOf(const std::string& Subject, const std::function<bool(const std::string&)>& ViaOthers) const
		{
			Exposure E;
			const std::string Subj = ToLowerInvariantAscii(Subject.empty() ? std::string("player") : Subject);
			for (std::vector<GossiperPtr>::size_type I = 0; I < AgentList.size(); ++I)
			{
				const GossiperPtr& A = AgentList[I];
				if (!A) continue;
				for (std::vector<RumorPtr>::size_type J = 0; J < A->Rumors.size(); ++J)
				{
					const RumorPtr& R = A->Rumors[J];
					if (!R || R->Content.Subject != Subj || PlainFactOfHim(R)) continue;
					const bool bTheirs = ViaOthers && ViaOthers(R->Content.Predicate);
					if (bTheirs) { E.Delegated++; E.DelegatedWeight += R->Confidence; }
					else { E.Yours++; E.YoursWeight += R->Confidence; }
				}
			}
			return E;
		}

		/// Gossip.cs 1104 to 1128. Rumours fade if nobody keeps them alive,
		/// the "lie low and let it cool" option. Call once per in-game hour;
		/// confidence decays on a multi-day half-life and spent rumours drop
		/// out entirely. The town's hourly rounds age the mill (TownRounds.h).
		void Age(const GameTime& Now)
		{
			if (bAged)
			{
				const double Hrs = (double)(Now.TotalMinutes() - LastAge.TotalMinutes()) / 60.0;
				if (Hrs > 0)
				{
					const double F = std::pow(0.5, Hrs / RumorHalfLifeHours);
					for (std::vector<GossiperPtr>::size_type I = 0; I < AgentList.size(); ++I)
					{
						std::vector<RumorPtr>& Rs = AgentList[I]->Rumors;
						// A body does not go cold the way a story does. Lying
						// low is the answer to talk; it is not the answer to
						// a corpse.
						for (std::vector<RumorPtr>::size_type J = 0; J < Rs.size(); ++J)
						{
							if (!Rs[J]->Indelible) Rs[J]->Confidence *= F;
						}
						// A copy at NaN or an infinity never fades and was
						// never forgotten: it goes now, indelible or not (town
						// list 6bw).
						Rs.erase(std::remove_if(Rs.begin(), Rs.end(), [](const RumorPtr& R)
							{ return NotFiniteBits(R->Confidence) || (R->Confidence < 0.03 && !R->Indelible); }), Rs.end());
					}
				}
			}
			// Never back (the time-and-state sweep, 30 September: a late call for
			// eleven after one for noon set the clock back, and the hour faded twice).
			if (!bAged || Now.TotalMinutes() > LastAge.TotalMinutes()) LastAge = Now;
			bAged = true;
		}

	private:
		std::shared_ptr<SocialGraph> Graph;
		std::vector<GossiperPtr>     AgentList;
		int Offered;
		int Dropped;
		GameTime LastAge;        // Gossip.cs 1130 and 1131
		bool bAged = false;

		static const std::vector<RumorPtr>& SnapshotOf(
			const std::vector<std::pair<std::string, std::vector<RumorPtr> > >& Snapshot,
			const std::string& Id)
		{
			for (std::vector<std::pair<std::string, std::vector<RumorPtr> > >::size_type I = 0;
			     I < Snapshot.size(); ++I)
			{
				if (Snapshot[I].first == Id) return Snapshot[I].second;
			}
			// Unreachable: every agent is in the snapshot by construction,
			// exactly as snapshot[speaker.Id] assumes in the C#. An empty
			// list rather than a throw keeps the failure quiet in the shape
			// the C# would fail in (a KeyNotFoundException there would be a
			// crash; here the speaker simply says nothing), and it can only
			// be reached if the snapshot loop above stops matching the agent
			// loop below it.
			static const std::vector<RumorPtr> None;
			return None;
		}

		static std::string::size_type IndexOfIgnoreCase(const std::string& Text,
		                                                const std::string& Word,
		                                                std::string::size_type From)
		{
			if (Word.size() > Text.size()) return std::string::npos;
			for (std::string::size_type I = From; I + Word.size() <= Text.size(); ++I)
			{
				std::string::size_type J = 0;
				for (; J < Word.size(); ++J)
				{
					const int A = std::tolower((unsigned char)Text[I + J]);
					const int B = std::tolower((unsigned char)Word[J]);
					if (A != B) break;
				}
				if (J == Word.size()) return I;
			}
			return std::string::npos;
		}
	};
}
