// TRANSLITERATION of ledger/Assets/Scripts/Core/Suspecting.cs, town list 6n.
//
// TRANSLITERATION, NOT REWRITE, and the distinction is the whole method: the
// C# suite is the behavioural definition, so every constant, every branch
// and every string here matches its source line for line. A port that
// "improved" something would make the two engines incomparable.
//
// SCOPE, only what the golden table's rows read (PerceptionGolden
// EmitOriginRung): DeedAccount 6 to 34, Nearness 37 to 51, and Suspecting
// 73 to 218 whole (CanTieSighting, AccountOf, Derive, Seen, Place). Of
// Acquaintance.cs, the three rungs Derive and the rows read: Stranger,
// HeardOfYou and Close. SuspicionLevel is Suspicion.cs 68, in Suspicion.h
// where the C# keeps it.
//
// A std::string CANNOT BE NULL, so an empty Summary stands for the C#'s
// null. Every read of it goes through string.IsNullOrWhiteSpace, which
// answers null and empty alike, so no branch can tell the difference.
// Trim and IsNullOrWhiteSpace are char.IsWhiteSpace's, over UTF-8, through
// MemoryStore.h's TrimUnicode.
//
// NO UNREAL TYPE IS IN THIS FILE, deliberately: the standing rule from 25
// August is that the decisions and the strings live where the tests run.
#pragma once

#include "Gossip.h"
#include "MemoryStore.h"     // TrimUnicode
#include "Perception.h"      // LedgerCore::Clamp
#include "Suspicion.h"       // SuspicionLevel

#include <string>

namespace LedgerCore
{
	// Acquaintance.cs 33 to 60, the three rungs read here. Only the ORDER of
	// these and their place against Perception::RecognitionFamiliarity
	// (0.35) carry meaning; the C# says so at length.
	namespace Acquaintance
	{
		const double Stranger   = 0.0;
		const double HeardOfYou = 0.20;
		const double Close      = 0.80;
	}

	// Suspecting.cs 6 to 34. What one person holds about a deed: the account
	// that reached them. The C# struct's default is every field zero, and
	// AccountOf sets Rung to -1 itself, as the C# does.
	struct DeedAccount
	{
		/// They hold an account of the deed at all.
		bool Held;
		/// They saw it themselves (hop 0) rather than heard it.
		bool SawItMyself;
		/// How well the account identifies the man, on the five-rung ladder
		/// (0 someone, 1 silhouette, 2 a mark, 3 a face, 4 recognition), or -1
		/// when the account does not carry it. NOT READ OFF THE CERTAINTY: a
		/// sighting is capped at 0.94 by Observe.CertaintyFor, so the 0.95
		/// line can never name anybody (independent check, 24 September).
		int Rung;
		/// A heard account whose first teller named him (they recognised
		/// him). Rumor::OriginRung carries the teller's rung through every
		/// retelling (town list 6n).
		bool NamesHim;
		/// The account's confidence as it reached them, 0..1: that of the copy
		/// whose words are in Summary.
		double Confidence;
		/// How surely the naming reached them, 0..1, when NamesHim: it places
		/// the number when the naming is what decides the case.
		double NamingConfidence;
		/// What they were told or saw, as a clause. Empty for the C#'s null.
		std::string Summary;

		DeedAccount() : Held(false), SawItMyself(false), Rung(0), NamesHim(false),
		                Confidence(0.0), NamingConfidence(0.0) {}
	};

	// Suspecting.cs 37 to 51. What one person holds about who was near the
	// deed at the time.
	struct Nearness
	{
		/// They saw the player near it themselves, well enough to know him
		/// again (see Suspecting::CanTieSighting).
		bool SawHimMyself;
		/// Somebody told them the player, BY NAME, was near it. Talk alone
		/// must not let the town identify him.
		bool HeardHeWasNear;
		/// How many OTHER people they know were near it at the time.
		int OthersNear;
		/// What they saw or heard of him, as a clause. Empty for the C#'s null.
		std::string Summary;

		Nearness() : SawHimMyself(false), HeardHeWasNear(false), OthersNear(0) {}
	};

	// Suspecting.cs 73 to 218. WHY SOMEBODY HAS REASON TO SUSPECT TOM OF A
	// DEED, from three things they hold: what they know about the deed, who
	// they know was near it, and how they know Tom. Deterministic and in
	// Core, by canon: the model is handed the level and the reason in words
	// and never decides whether to suspect. NO NEW THRESHOLD: each case is
	// placed on one of the four existing SuspicionTracker bands, and within
	// the band the account's own confidence sets where the number sits.
	namespace Suspecting
	{
		/// Suspecting.cs 79. A sighting ties the man seen to the man in front
		/// of you only if it was good enough to know him again: a mark (rung
		/// 2), a face (rung 3) or recognition (rung 4). A silhouette is half
		/// the street.
		inline bool CanTieSighting(int Rung) { return Rung >= 2; }

		/// Suspecting.cs 93 to 130. THE ACCOUNT A PERSON HOLDS, read off the
		/// rumours they hold (town list 6n): seen themselves when it is
		/// first-hand, with the rung they reached; heard, and naming him, when
		/// whoever first told it recognised him (rung 4), however many mouths
		/// it passed through. EVERY COPY THEY HOLD, not the surest one (the
		/// independent check): a vaguer, surer copy must not hide a
		/// recognition. The C#'s null Gossiper is a null pointer here.
		inline DeedAccount AccountOf(const Gossiper* G, const std::string& TopicKey)
		{
			DeedAccount Acc;
			Acc.Rung = -1;
			if (G == 0 || TopicKey.empty()) return Acc;   // C#: string.IsNullOrEmpty
			// The words come from the copy that decides the case (the second
			// pass: the rung from one look and the words from another made
			// one line say "a shape by the glass; and I'd know him again").
			RumorPtr Best, OwnDeciding, Naming;
			for (std::vector<RumorPtr>::size_type I = 0; I < G->Rumors.size(); ++I)
			{
				const RumorPtr& R = G->Rumors[I];
				if (R->TopicKey() != TopicKey) continue;
				Acc.Held = true;
				if (!Best || R->Confidence > Best->Confidence) Best = R;
				if (R->Hops == 0)
				{
					Acc.SawItMyself = true;
					if (!OwnDeciding || R->OriginRung > OwnDeciding->OriginRung
					    || (R->OriginRung == OwnDeciding->OriginRung && R->Confidence > OwnDeciding->Confidence)) OwnDeciding = R;
				}
				else if (R->OriginRung >= 4)
				{
					Acc.NamesHim = true;
					if (!Naming || R->Confidence > Naming->Confidence) Naming = R;
				}
			}
			if (!Acc.Held) return Acc;
			if (OwnDeciding) Acc.Rung = OwnDeciding->OriginRung;
			// What they saw, when they saw anything (the line opens "I saw it
			// myself"), at the look that sets the rung; else the telling that
			// named him. The number is that same copy's, so the words and the
			// doubt agree (the third pass).
			const RumorPtr Deciding = OwnDeciding ? OwnDeciding : (Naming ? Naming : Best);
			Acc.Summary = Deciding->Summary;
			Acc.Confidence = Deciding->Confidence;
			if (Naming) Acc.NamingConfidence = Naming->Confidence;
			return Acc;
		}

		/// The C#'s (value, level, why) tuple. `bWhy` false is the C#'s null
		/// why, which only the first return gives.
		struct Derived
		{
			double         Value;
			SuspicionLevel Level;
			std::string    Why;
			bool           bWhy;
			Derived(double InValue, SuspicionLevel InLevel, const std::string& InWhy, bool bInWhy)
				: Value(InValue), Level(InLevel), Why(InWhy), bWhy(bInWhy) {}
		};

		/// string.IsNullOrWhiteSpace, for a string that cannot be null.
		inline bool IsNullOrWhiteSpace(const std::string& S) { return TrimUnicode(S).empty(); }

		/// Suspecting.cs 201 to 202.
		inline std::string Seen(const Nearness& Near)
		{
			return IsNullOrWhiteSpace(Near.Summary) ? std::string() : " (" + TrimUnicode(Near.Summary) + ")";
		}

		/// Suspecting.cs 206 to 217. The band's floor plus up to half its
		/// width, by the account's confidence: the level is the case's, the
		/// number carries the doubt.
		inline double Place(SuspicionLevel Band, double Confidence)
		{
			double Lo, Hi;
			switch (Band)
			{
				case SuspicionLevel::Uneasy:      Lo = 0.25; Hi = 0.50; break;
				case SuspicionLevel::Suspicious:  Lo = 0.50; Hi = 0.80; break;
				case SuspicionLevel::Confronting: Lo = 0.80; Hi = 1.00; break;
				default: return 0.0;
			}
			return Lo + (Hi - Lo) * 0.5 * Clamp(Confidence, 0.0, 1.0);
		}

		/// Suspecting.cs 132 to 199.
		inline Derived Derive(const DeedAccount& Account, const Nearness& Near, double Familiarity)
		{
			if (!Account.Held)
				return Derived(0.0, SuspicionLevel::Trusting, std::string(), false);
			const std::string Told = IsNullOrWhiteSpace(Account.Summary)
				? std::string(Account.SawItMyself ? "I saw what happened" : "I heard about what happened")
				: (Account.SawItMyself ? "I saw it myself: " + TrimUnicode(Account.Summary)
				                       : "I heard that " + TrimUnicode(Account.Summary));
			const int Others = Near.OthersNear > 0 ? Near.OthersNear : 0;   // C#: Math.Max(0, near.OthersNear)

			SuspicionLevel Band;
			std::string Why;
			double Sure = Account.Confidence;
			if (Account.SawItMyself && Account.Rung >= 4)
			{
				Band = SuspicionLevel::Confronting;
				Why = Told + ", and it was him, I would swear to it";
			}
			else if (Account.SawItMyself && CanTieSighting(Account.Rung))
			{
				// THE WITNESS WHO SAW HIS FACE AT IT: she would know him
				// again, and now he is standing in front of her.
				Band = SuspicionLevel::Suspicious;
				Why = Told + "; and I'd know him again, and here he is";
			}
			else if (Account.NamesHim && Familiarity >= Acquaintance::HeardOfYou)
			{
				// Told by somebody who knew him, and they know who "Novak"
				// is: a stranger to the name can tie nobody to it (the
				// independent check, 28 September). Their own vaguer look, if
				// they had one, does not undo what they were told.
				Band = SuspicionLevel::Suspicious;
				Why = Account.SawItMyself ? Told + "; and somebody who saw it plainer than I did named him"
				                          : Told + ", and whoever saw it named him";
				if (Account.SawItMyself) Sure = Account.NamingConfidence;
			}
			else if (Near.SawHimMyself && Others == 0)
			{
				Band = SuspicionLevel::Suspicious;
				Why = Told + "; and I saw him near it at the time" + Seen(Near) + ", and nobody else about";
			}
			else if (Near.SawHimMyself)
			{
				Band = SuspicionLevel::Uneasy;
				Why = Told + "; and I saw him near it at the time" + Seen(Near) + ", though others were about too";
			}
			else if (Near.HeardHeWasNear && Familiarity >= Acquaintance::HeardOfYou)
			{
				// Hearsay that "Novak was about" means something only to
				// somebody who knows who Novak is.
				Band = SuspicionLevel::Uneasy;
				Why = Told + "; and I heard he was near it at the time";
			}
			else
			{
				return Derived(0.0, SuspicionLevel::Trusting, Told + ", but nothing I know ties him to it", true);
			}

			// HOW THEY KNOW HIM. His own people, crew and household, give him
			// the benefit of the doubt: one band lower. Knowing is the gate
			// for naming, not for liking, and this is the liking half.
			if (Familiarity >= Acquaintance::Close && Band > SuspicionLevel::Trusting)
			{
				Band = (SuspicionLevel)((int)Band - 1);
				Why += "; but he is one of my own, and I would rather it was not him";
			}
			return Derived(Place(Band, Sure), Band, Why, true);
		}
	}
}
