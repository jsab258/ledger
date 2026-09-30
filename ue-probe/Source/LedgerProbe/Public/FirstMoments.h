// TRANSLITERATION of ledger/Assets/Scripts/Core/FirstMoments.cs, 30 September
// (the town's handover 6y, "the hints, each the first time it matters";
// production/handovers/6y-hints.md; the twenty a friend would notice, 7).
//
// HINTS THAT FIRE THE FIRST TIME THEY MATTER. The game reports each moment
// every time it happens, and each hint shows once, the first time it can mean
// something: walking first in a new game, never two within twelve seconds, a
// spoken beat or a screen's own line at once, and a hint about what just
// happened dropped unshown once it has waited past its moment. The words are
// the town's (game-design/first-moments-2026-09-29.md); the game fills in the
// keys as the player has them bound (Fill).
//
// TRANSLITERATION, NOT REWRITE, as Gossip.h states the method: the same
// clock that never runs backwards, the same refusals of NaN and infinities,
// the same save ({"done":[names]}, sorted), read the C#'s way (MiniJson.h: a
// key given twice keeps its last value; only a moment's exact name counts).
// Checked against PerceptionGolden's EmitHints rows (HintDue, HintHappened,
// HintSave, HintAfterLoad, HintFill) in ue-probe/perception-golden.txt.
//
// NO UNREAL TYPE IS IN THIS FILE, as every file of the port.
#pragma once

#include "MiniJson.h"

#include <algorithm>
#include <cmath>
#include <functional>
#include <limits>
#include <set>
#include <string>
#include <utility>
#include <vector>

namespace LedgerCore
{
	enum class Moment
	{
		StandingStill,       // he has not moved a few seconds after a new game begins
		CanTalk,             // Sheila's walk-round has ended at the office door
		FirstAsk,            // Ron hands him the coat and the outfit's envelope
		SeenAtDeed,          // somebody saw him do something the town will talk about
		OverheardAboutHim,   // he overheard a remark about himself
		LedgerOpened,        // he opened the Ledger
	};

	inline const char* MomentName(Moment M)
	{
		switch (M)
		{
		case Moment::StandingStill: return "StandingStill";
		case Moment::CanTalk: return "CanTalk";
		case Moment::FirstAsk: return "FirstAsk";
		case Moment::SeenAtDeed: return "SeenAtDeed";
		case Moment::OverheardAboutHim: return "OverheardAboutHim";
		default: return "LedgerOpened";
		}
	}

	/// The C#'s Enum.GetNames, in declaration order.
	inline bool MomentFromName(const std::string& S, Moment& Out)
	{
		for (int I = 0; I <= (int)Moment::LedgerOpened; ++I)
		{
			if (S == MomentName((Moment)I)) { Out = (Moment)I; return true; }
		}
		return false;
	}

	/// One hint. Speaker (a cast id, empty for none) says Line in their own
	/// voice when they are with him; Key is plain text and always shows; keys
	/// in braces are the game's to fill (FirstMoments::Fill).
	struct Hint
	{
		Moment M;
		std::string Speaker;   // "" is the C#'s null
		bool bLine;            // false is the C#'s null Line
		std::string Line;
		std::string Key;
		bool AtOnce;
		double StaleAfter;
	};

	class FirstMoments
	{
	public:
		/// Real seconds between two hints, so none overlaps another.
		static constexpr double Gap = 12.0;
		/// Real seconds standing still in a new game before he is told how to walk.
		static constexpr double StillFor = 4.0;

		/// The words, one hint a moment.
		static const Hint& Words(Moment M)
		{
			static const Hint W[] = {
				{ Moment::StandingStill, "", false, "",
				  "{Move} walks, {Run} runs. People on this street notice who's about.", false, std::numeric_limits<double>::infinity() },
				{ Moment::CanTalk, "lena", true,
				  "That's Ron on the rank. Go and say hello. Everyone out there wants a look at you.",
				  "Walk up to anyone and press {Talk}. What you tell them, they remember.", false, 45 },
				{ Moment::FirstAsk, "rocco", true,
				  "If you go tonight, boss, wear that. In the dark nobody looks twice at a coat.",
				  "{Coat} puts the coat on or takes it off: in the dark it makes you harder to recognise.", true, 0 },
				{ Moment::SeenAtDeed, "", false, "",
				  "Somebody saw that. What they make of it can go round.", false, 15 },
				{ Moment::OverheardAboutHim, "", false, "",
				  "That was about you. {Ledger} shows what you believe the street knows.", false, 15 },
				{ Moment::LedgerOpened, "", false, "",
				  "What you believe the street now knows about you.", true, 0 },
			};
			return W[(int)M];
		}

		/// The moments whose hints have shown (or no longer can), for the save.
		const std::set<Moment>& Done() const { return DoneSet; }

		/// A session begins at this real second: a new game, which starts the
		/// hints over, or a load (SavedJson, ToJson's text), whose moments are
		/// done. The gap holds across a load; a clock the game restarted is
		/// taken up from where it is now. Only a new game tells him how to walk.
		void Begin(double At, bool NewGame, const std::string* SavedJson = nullptr)
		{
			Waiting.clear();
			bMoved = false;
			if (NewGame) { DoneSet.clear(); }
			else
			{
				// Text that is no JSON object is the C#'s null save: what was
				// done stays (the independent check; its row is HintLoadBad).
				if (SavedJson != nullptr && IsObject(*SavedJson)) { DoneSet.clear(); Read(*SavedJson, DoneSet); }
				DoneSet.insert(Moment::StandingStill);
			}
			if (std::isnan(At) || std::isinf(At)) { Began = std::numeric_limits<double>::quiet_NaN(); bFresh = false; return; }
			if (At < Latest)
			{
				// The game's clock started again: the last hint was that long before now.
				const double Shift = Latest - At;
				LastShown -= Shift;
				Latest = At;
			}
			Clock(At);
			Began = At;
			bFresh = NewGame;
		}

		/// He moved: nobody tells him how, in this game or after a load.
		void Moved(double /*At*/)
		{
			bMoved = true;
			DoneSet.insert(Moment::StandingStill);
			RemoveWaiting(Moment::StandingStill);
		}

		/// The moment happened at this real second. A hint shown at once is
		/// returned now (true, into Out); any other waits for Due.
		bool Happened(Moment M, double At, Hint& Out)
		{
			// A moment outside the six is nothing here; the C# throws on it, and
			// reading past Words crashed the game (the independent check).
			if ((int)M < 0 || (int)M > (int)Moment::LedgerOpened) return false;
			if (!Clock(At) || M == Moment::StandingStill || DoneSet.count(M)) return false;
			const Hint& H = Words(M);
			if (H.AtOnce)
			{
				DoneSet.insert(M);
				RemoveWaiting(M);
				LastShown = At;
				Out = H;
				return true;
			}
			for (std::vector<std::pair<Moment, double> >::size_type I = 0; I < Waiting.size(); ++I)
			{
				if (Waiting[I].first == M) { Waiting[I] = std::make_pair(M, At); return false; }   // happened again: fresh again
			}
			Waiting.push_back(std::make_pair(M, At));
			return false;
		}

		/// The hint to show at this real second (true, into Out), or none: at
		/// most one, never inside the gap after the last, walking before
		/// anything else in a new game, and nothing that has gone stale.
		bool Due(double At, Hint& Out)
		{
			if (!Clock(At)) return false;
			const bool bWalkFirst = bFresh && !bMoved && !DoneSet.count(Moment::StandingStill) && !std::isnan(Began);
			if (bWalkFirst && At - Began >= StillFor && !IsWaiting(Moment::StandingStill))
			{
				Waiting.insert(Waiting.begin(), std::make_pair(Moment::StandingStill, At));
			}
			Waiting.erase(std::remove_if(Waiting.begin(), Waiting.end(),
				[At](const std::pair<Moment, double>& W) { return At - W.second > Words(W.first).StaleAfter; }), Waiting.end());
			if (Waiting.empty() || At - LastShown < Gap) return false;
			// Until he has walked or been told how, only the walking hint shows.
			int Pick = 0;
			if (bWalkFirst)
			{
				Pick = -1;
				for (std::vector<std::pair<Moment, double> >::size_type I = 0; I < Waiting.size(); ++I)
				{
					if (Waiting[I].first == Moment::StandingStill) { Pick = (int)I; break; }
				}
			}
			if (Pick < 0) return false;
			const Moment M = Waiting[Pick].first;
			Waiting.erase(Waiting.begin() + Pick);
			DoneSet.insert(M);
			LastShown = At;
			Out = Words(M);
			return true;
		}

		/// A hint's text with the keys as the player has them bound; a key the
		/// game does not name, or names as nothing but spaces, stays in its braces.
		/// (The C#'s Regex \{(\w+)\}: a word of letters, digits or underscores.
		/// ASCII only: .NET's \w also takes other alphabets' letters and digits,
		/// and the keys are the game's own words, never those.)
		static std::string Fill(const std::string& Text, const std::function<bool(const std::string&, std::string&)>& KeyFor)
		{
			if (Text.empty() || !KeyFor) return Text;
			std::string Out;
			std::string::size_type I = 0;
			while (I < Text.size())
			{
				if (Text[I] == '{')
				{
					std::string::size_type J = I + 1;
					while (J < Text.size() && IsWord(Text[J])) ++J;
					if (J > I + 1 && J < Text.size() && Text[J] == '}')
					{
						const std::string Name = Text.substr(I + 1, J - I - 1);
						std::string K;
						const bool bGot = KeyFor(Name, K);
						// string.IsNullOrWhiteSpace: every character char.IsWhiteSpace,
						// U+00A0 and the rest included, read over UTF-8.
						bool bBlank = true;
						MiniJson::FReader R(K);
						for (size_t At = 0; At < K.size();)
						{
							size_t Len = 1;
							if (!MiniJson::FReader::IsWhiteSpace(R.CharAt(At, Len))) { bBlank = false; break; }
							At += Len;
						}
						Out += (!bGot || bBlank) ? Text.substr(I, J - I + 1) : K;
						I = J + 1;
						continue;
					}
				}
				Out += Text[I];
				++I;
			}
			return Out;
		}

		/// The moments done, for any save's JSON: {"done":[their names, sorted]}.
		std::string ToJson() const
		{
			std::vector<std::string> Names;
			for (Moment M : DoneSet) Names.push_back(MomentName(M));
			std::sort(Names.begin(), Names.end());
			std::string J = "{\"done\":[";
			for (std::vector<std::string>::size_type I = 0; I < Names.size(); ++I) { J += (I ? ",\"" : "\"") + Names[I] + "\""; }
			return J + "]}";
		}

		/// From ToJson's text: only a moment's exact name counts, and what it
		/// cannot read it skips, so a damaged save shows a hint again.
		static FirstMoments FromJson(const std::string& SavedJson)
		{
			FirstMoments F;
			Read(SavedJson, F.DoneSet);
			return F;
		}

	private:
		std::set<Moment> DoneSet;
		std::vector<std::pair<Moment, double> > Waiting;
		double Began = std::numeric_limits<double>::quiet_NaN();
		bool bFresh = false, bMoved = false;
		double LastShown = -std::numeric_limits<double>::infinity();
		double Latest = -std::numeric_limits<double>::infinity();

		static bool IsWord(char C) { return (C >= 'a' && C <= 'z') || (C >= 'A' && C <= 'Z') || (C >= '0' && C <= '9') || C == '_'; }

		// A clock that never runs backwards, whatever the game sends; NaN or
		// an infinity is no time.
		bool Clock(double& At)
		{
			if (std::isnan(At) || std::isinf(At)) return false;
			if (At < Latest) At = Latest;
			Latest = At;
			return true;
		}

		bool IsWaiting(Moment M) const
		{
			for (const auto& W : Waiting) { if (W.first == M) return true; }
			return false;
		}

		void RemoveWaiting(Moment M)
		{
			Waiting.erase(std::remove_if(Waiting.begin(), Waiting.end(),
				[M](const std::pair<Moment, double>& W) { return W.first == M; }), Waiting.end());
		}

		static bool IsObject(const std::string& SavedJson)
		{
			LedgerVignette::Value Root;
			std::string Err;
			return MiniJson::Deserialize(SavedJson, Root, Err) && Root.Type == LedgerVignette::T_OBJ;
		}

		static void Read(const std::string& SavedJson, std::set<Moment>& Into)
		{
			LedgerVignette::Value Root;
			std::string Err;
			if (!MiniJson::Deserialize(SavedJson, Root, Err) || Root.Type != LedgerVignette::T_OBJ) return;
			// A key given twice keeps its last value, as the C#'s dictionary does.
			const LedgerVignette::Value* Done = nullptr;
			for (std::vector<std::pair<std::string, LedgerVignette::Value> >::size_type I = 0; I < Root.Obj.size(); ++I)
			{
				if (Root.Obj[I].first == "done") Done = &Root.Obj[I].second;
			}
			if (Done == nullptr || Done->Type != LedgerVignette::T_ARR) return;
			for (const LedgerVignette::Value& N : Done->Arr)
			{
				Moment M;
				if (N.Type == LedgerVignette::T_STR && MomentFromName(N.Str, M)) Into.insert(M);
			}
		}
	};
}
