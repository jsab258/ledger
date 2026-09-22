// TRANSLITERATION of the ARREST section of ledger/Assets/Scripts/Core/Reaction.cs
// ("CAUGHT IN THE ACT - spec 15.2, approved: ARREST, NO CHASE").
//
// WHY THIS FILE EXISTS, 22 September. ROADMAP's stage-3 gate carries a clause
// on purpose: "arrest reachable from live play, its callers outside Core
// counted and printed rather than zero". Counted on 22 September, the C# rule
// had five callers and all five were in CoreTests - and the Unreal port, which
// is the engine the game SHIPS on (D16), had no arrest at all. The end of the
// consequence chain existed only in the engine that does not ship, and there
// only as a test. Jafar: "the single most important thing wrong with the game
// right now".
//
// TRANSLITERATION, NOT REWRITE, by the same rule as every other file here:
// the C# is the behavioural definition, every constant and branch matches its
// source, and the golden table is the proof rather than this comment: the
// Confront, CataloguesYourCoat, IsPublicEvent and ReactionConst rows, emitted
// by ledger/PerceptionGolden and answered in CoreGolden.h's Evaluate.
//
// SCOPE: Lawful, Confront, ResistPressure, CataloguesYourCoat, IsPublicEvent -
// the arrest section and nothing else. The rest of Reaction.cs (the reaction
// ladder, loudness, the survivor) is NOT PORTED, and says so here rather than
// by being absent.
//
// NO UNREAL TYPE IS IN THIS FILE, as with every Core module in the port: the
// arithmetic lives where the tests run.
#pragma once

#include "Observation.h"

namespace LedgerCore
{
	namespace Reaction
	{
		enum class Lawful
		{
			/// He cannot place you. The escape hatch is social, not athletic.
			NothingToArrest,
			/// A hand on your arm, the street watching, and everything in your
			/// coat now in a drawer at the station.
			Arrest,
			/// You resisted. Permitted, and catastrophic.
			ResistedArrest,
		};

		/// A constable who watched it happen closes, and being taken is the
		/// outcome. There is deliberately NO CHASE: a foot chase is a
		/// different genre and would be the least distinguished thing in this
		/// game. Running still works, through the systems that already exist -
		/// you get away because he could not identify you, because the street
		/// was busy, because you had somewhere to be. Not because you outran
		/// him round a corner.
		///
		/// THE NULL CASE IS A POINTER HERE and a null reference in C#: "the
		/// constable saw nothing at all" is a real input in both engines, and
		/// it must answer NothingToArrest in both rather than crash in one.
		inline Lawful Confront(const Observation* ConstablesView, bool bPlayerResists)
		{
			if (ConstablesView == nullptr) { return Lawful::NothingToArrest; }
			const bool bCanPlaceYou = ConstablesView->Has(Slot::Actor) && ConstablesView->Rung >= 4;
			if (!bCanPlaceYou) { return Lawful::NothingToArrest; }
			return bPlayerResists ? Lawful::ResistedArrest : Lawful::Arrest;
		}

		/// RESISTING IS ALLOWED AND IT IS THE WORST OUTCOME IN THE GAME.
		/// **The game does not warn you.** The prompt says what it always says.
		static const double ResistPressure = 1.15;

		/// What an arrest hands over: everything you were carrying is now
		/// catalogued, and provenance becomes the interrogation.
		inline bool CataloguesYourCoat(Lawful Outcome)
		{
			return Outcome == Lawful::Arrest || Outcome == Lawful::ResistedArrest;
		}

		/// Being taken is itself an event with witnesses. Half the street
		/// watched Tom Novak get walked to a car, and that is a fact the mill
		/// carries like any other.
		inline bool IsPublicEvent(Lawful Outcome) { return CataloguesYourCoat(Outcome); }

		/// The name the golden table and the verdict both print, so the two
		/// engines are compared on the same word rather than on an integer
		/// whose order nobody promised to keep.
		inline const char* Name(Lawful Outcome)
		{
			switch (Outcome)
			{
				case Lawful::Arrest:         return "Arrest";
				case Lawful::ResistedArrest: return "ResistedArrest";
				default:                     return "NothingToArrest";
			}
		}
	}
}
