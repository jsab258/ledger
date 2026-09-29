// TRANSLITERATION of StreetVoice.Exchange's COMPOSITION, from
// ledger/Assets/Scripts/Core/StreetVoice.cs 131 to 296 plus the five helpers
// it needs (Pick 692, Answer 734, Hash 737, Trim 745, Cap 768).
//
// WHY IT EXISTS, in one sentence from queue 147: the probe's overheard beat
// read a dialogue bank, chose a row by the rung the memory reached and a
// variant by a seed, which is a PICK, and the town's reply was therefore one
// of N pre-written strings. Exchange is the rung above that: the teller's
// sentence is BUILT around the rumour's own Summary, so what the player
// overhears carries the thing that actually happened rather than naming a row
// that happened to be filed.
//
// TRANSLITERATION, NOT REWRITE, exactly as Gossip.h states the method: the C#
// suite is the behavioural definition, so every band, every boundary and every
// character of every line matches its source. The 98 lines of dialogue below
// were EXTRACTED FROM THE C# MECHANICALLY rather than retyped, and all 98 were
// diffed against StreetVoice.cs 146 to 283 for content AND ORDER by the
// director ruling of 2026-09-08, BY READING. NO MACHINE CHECKS THEM YET: there
// is no street_voice scenario in ledger/PerceptionGolden and therefore no
// golden row that would go red if a template changed. Queue 160 owes one row
// per template over two summaries, one a lowercase clause and one opening on a
// proper noun.
//
// SCOPE, queue 147: SpokenLine 43 to 72; Exchange 131 to 296; Pick, Answer,
// Hash, Trim, Cap; since 23 September StanceKind, Stance, GazeMetres,
// StoryThatShows and RemarkLedger; and since 29 September the knowing
// section (StoryHalfRemembered, Stance's knowsALittle, the look, the faint
// remark, RegardFor) and Recognition (the sections at the end). OUT OF SCOPE
// AND NOT HERE, so a reader can tell a missing member from a forgotten one:
// Ambient, ChatterLevel, AmbientEverySeconds, RemarkLedger's Fresh and its
// save (town list 6k and 6o), Clamp01 (LedgerCore::Clamp01 in Perception.h
// is the same arithmetic).
//
// THE DEVIATIONS FROM THE C#, NAMED, in the shape the eight of
// game-design/decision-2026-09-08-the-core-port-and-its-eight-deviations.md
// use. Each is also named at its site below.
//
//   9.  THE LINES ARE TEMPLATES WITH {what} AND {What}, RENDERED, where the
//       C# is a compiler-generated concatenation of an interpolated string.
//       The C# source IS template text ($"...{what}..."), so the literals are
//       identical; what differs is that the substitution is a function here.
//       Render is the one piece of logic with no C# counterpart, and every
//       string it can produce is pinned by a golden row emitted by the C#.
//   10. THE THREE-WAY CONFIDENCE CONDITIONAL AND THE FOUR-WAY DISPOSITION
//       CONDITIONAL ARE FACTORED INTO TellBandIndex AND AnswerBandIndex.
//       Exchange calls them, so there is exactly one copy of each boundary,
//       and the probe's verdict can NAME the band that spoke without
//       re-deriving the condition. A second copy of `>= 0.8` in an instrument
//       is how a verdict comes to describe a branch the run did not take.
//   11. AN OPTIONAL ExchangeTrace OUT-PARAMETER. The C# returns the two
//       lines and nothing about how they were chosen. The four-argument
//       Exchange has the C# signature and behaviour; the five-argument one
//       additionally reports which band and which index, because
//       overheardReplyMode has to be a reading rather than a claim. No
//       branch depends on it.
//   12. ASCII-ONLY Trim, Cap AND Hash, which is deviation 4 of the port
//       ruling restated for three more functions: a C# char is a UTF-16 unit
//       and a C++ std::string iterates bytes, char.IsLower and
//       ToUpperInvariant know every alphabet and these know twenty-six
//       letters. Measured 2026-09-08: 0 non-ASCII bytes in
//       content/dialogue/crime-witness-v1.json (1 file examined), which is
//       the only producer of a Summary this run can compose from. The day a
//       non-ASCII summary enters a bank the mill reads, this and
//       GossipMill::IsWordChar are the two places the engines can part.
//       AND THE DENOMINATOR ABOVE IS THE WRONG ONE FOR Hash. Hash reads
//       REPLIER IDS, not summaries, so the bank measurement above is not its
//       denominator: canon.md carries 0 non-ASCII bytes (1 file examined,
//       2026-09-08), which is the set the cast ids derive from.
//   13. Answer's ARITHMETIC IS DONE IN uint32 AND CAST BACK. C# int
//       arithmetic is unchecked and wraps; C++ signed overflow is undefined,
//       so `seed * 97 + 31 + hash % 9973` would be UB for a large seed. The
//       two agree bit for bit on every two's-complement machine and the port
//       is defined rather than undefined where the C# merely wraps.
//   14. A NULL Summary CANNOT EXIST HERE. Rumor::Summary is a std::string, so
//       the C#'s `string.IsNullOrEmpty(what)` guard is an empty-string guard.
//       Same outcome on every input the C# defines: no lines, no speech.
//
// NO UNREAL TYPE IS IN THIS FILE, deliberately, the standing rule from 25
// August: this project's top layer does not compile in the container that
// writes it, so the decisions and the strings live where the tests run.
// ue-probe/tests/crime-probe-test.cpp and ue-probe/tests/core-port-test.cpp
// compile and RUN every line below with g++ before anything is dispatched.
//
// WHAT THIS FILE CANNOT SEE: whether anybody was in earshot, whether a frame
// was captioned with the sentence it composed, or whether the summary it
// composed from describes what the witness actually saw. Those are the run's
// business and the crime verdict's keys are how they are read.
#pragma once

#include "Gossip.h"      // Rumor, Gossiper, RumorPtr, GossiperPtr

#include <limits>
#include <memory>
#include <set>
#include <string>
#include <vector>

namespace LedgerCore
{
	// StreetVoice.cs 43 to 72. One thing somebody says out loud, with the
	// state that justifies it.
	struct SpokenLine
	{
		std::string SpeakerId;
		std::string Text;
		// True when this is about the player: those carry a lead if heard.
		bool        AboutPlayer;
		// The rumour behind it. The player who overhears this learns exactly
		// this, which is why hearing is knowing.
		RumorPtr    Source;
		// TRUE WHEN THE WORDS WERE ASSEMBLED AT RUN TIME, so no recording of
		// them can exist and none ever will. VoiceBank.ClipName keys a clip
		// by (voice, EXACT text), and a line built as template-plus-summary is
		// a different clip for every rumour the street has ever carried. Only
		// the TELLING is marked, exactly as StreetVoice.cs 289 to 295 marks
		// it: the answer is a literal from a band and is bankable as written.
		bool        Composed;
		// The bank the line was drawn from ("faint", "recognition/sensitive"),
		// as the C#'s SpokenLine.Bank. Set by Recognition and FaintRemark;
		// Exchange's banks come with the port of town list 6k.
		std::string Bank;

		SpokenLine() : AboutPlayer(false), Composed(false) {}
	};

	namespace StreetVoice
	{
		// ---- the helpers, StreetVoice.cs 692 to 772 ----------------------

		// StreetVoice.cs 692. Deviation 13 does not apply: the modulus and the
		// negative correction are the C#'s own, and C++11 truncates a negative
		// remainder the same way C# does.
		inline int PickIndex(int Seed, int Count)
		{
			if (Count <= 0) { return -1; }
			int I = Seed % Count;
			if (I < 0) { I += Count; }
			return I;
		}

		inline std::string Pick(int Seed, const char* const* Options, int Count)
		{
			const int I = PickIndex(Seed, Count);
			if (I < 0 || Options == 0) { return std::string(); }
			return std::string(Options[I]);
		}

		// StreetVoice.cs 737. FNV-1a rather than GetHashCode, which is
		// randomised per process on .NET Core: the same save would otherwise
		// produce different conversations on each launch. Deviation 12, ASCII.
		inline unsigned int Hash(const std::string& S)
		{
			unsigned int H = 2166136261u;
			for (std::string::size_type I = 0; I < S.size(); ++I)
			{
				H ^= (unsigned int)(unsigned char)S[I];
				H *= 16777619u;
			}
			return H;
		}

		// StreetVoice.cs 734, and the three attempts its docstring records.
		// The reply's seed is mixed with WHO IS REPLYING, because two indices
		// that are both functions of one number give fourteen fixed
		// conversations however prime the multiplier is. Deviation 13: the
		// wrap is done in uint32 so a large seed is defined rather than UB.
		inline int AnswerSeed(int Seed, const std::string& ReplierId)
		{
			const unsigned int Mixed = (unsigned int)Seed * 97u + 31u + (Hash(ReplierId) % 9973u);
			return (int)Mixed;
		}

		// StreetVoice.cs 745. s.Trim() then one trailing full stop. Deviation
		// 12: ASCII whitespace, which is every byte the banks can carry.
		inline std::string Trim(const std::string& S)
		{
			if (S.empty()) { return S; }
			std::string::size_type B = 0, E = S.size();
			while (B < E && (S[B] == ' ' || S[B] == '\t' || S[B] == '\n' || S[B] == '\r'
			                 || S[B] == '\v' || S[B] == '\f')) { ++B; }
			while (E > B && (S[E - 1] == ' ' || S[E - 1] == '\t' || S[E - 1] == '\n' || S[E - 1] == '\r'
			                 || S[E - 1] == '\v' || S[E - 1] == '\f')) { --E; }
			std::string Out = S.substr(B, E - B);
			if (!Out.empty() && Out[Out.size() - 1] == '.') { Out.erase(Out.size() - 1); }
			return Out;
		}

		// StreetVoice.cs 768. A Rumor.Summary is a lowercase clause written to
		// be spliced into the middle of a sentence, and half the templates do
		// exactly that; the other half open on it or follow a full stop, and
		// every one of those was rendering "Don't quote me. the new owner was
		// at the warehouse on Tuesday" in a subtitle. ONLY THE FIRST
		// CHARACTER MOVES: a summary that already starts with a proper noun is
		// left exactly as it is. Deviation 12, ASCII.
		inline std::string Cap(const std::string& S)
		{
			if (S.empty()) { return S; }
			if (!(S[0] >= 'a' && S[0] <= 'z')) { return S; }
			std::string Out = S;
			Out[0] = (char)(S[0] - 'a' + 'A');
			return Out;
		}

		// DEVIATION 9. The C# writes $"I'm telling you, {what}." and the
		// compiler concatenates; the literal below is that same template text
		// and this substitutes. {what} is the trimmed summary, {What} is
		// Cap(what), and a token this does not know is left standing so a
		// mistyped placeholder shows up in the string rather than vanishing.
		inline std::string Render(const std::string& Template, const std::string& What)
		{
			const std::string Capped = Cap(What);
			std::string Out;
			for (std::string::size_type I = 0; I < Template.size(); )
			{
				if (Template.compare(I, 6, "{what}") == 0) { Out += What;   I += 6; continue; }
				if (Template.compare(I, 6, "{What}") == 0) { Out += Capped; I += 6; continue; }
				Out += Template[I];
				++I;
			}
			return Out;
		}

		// ---- the bands --------------------------------------------------
		//
		// FOURTEEN A BAND RATHER THAN TWO OR THREE, and the C# records why:
		// BarkGen measured the old banks and EVERY slot in the game repeated
		// inside ninety seconds. A street that says the same eight sentences
		// all evening is a street the player stops hearing, and it takes the
		// gossip system down with it, because the whole point is that what you
		// overhear is causally true and nobody listens to a loop.

	// StreetVoice.cs 146 to 175, the band for confidence at or above 0.80:
	// somebody who saw it. TWO OF THE FOURTEEN DELIBERATELY LEAD WITH THE
	// STORY, which the C# records as a judgement rather than an oversight: at
	// this confidence, stating the thing flatly and letting it sit is what
	// certainty sounds like.
	inline const char* const* TellCertain(int& OutCount)
	{
		static const char* const Lines[14] = {
			"I'm telling you, {what}.",
			"{What}. I know what I saw.",
			"You want to know why I've been quiet? {What}.",
			"{What}. I'd say it in front of him.",
			"I was there. {What}, and that's the end of it.",
			"Don't look at me like that. {What}.",
			"My own eyes, not somebody's mouth. {What}.",
			"You can believe what you like. {What}.",
			"I've not slept right since. {What}.",
			"I wish I hadn't seen it, but I did: {what}.",
			"Ask me again in a year and I'll tell you the same: {what}.",
			"There's no other way to read it: {what}.",
			"I'm not guessing. {What}.",
			"Nobody's done a thing about it. {What}.",
		};
		OutCount = 14;
		return Lines;
	}

	// StreetVoice.cs 176 to 192, confidence 0.50 to 0.80: somebody who was
	// told, repeating it with the attribution still attached.
	inline const char* const* TellSecondHand(int& OutCount)
	{
		static const char* const Lines[14] = {
			"They're saying {what}.",
			"Word is {what}.",
			"Somebody told me {what}. Make of it what you like.",
			"It's going round that {what}.",
			"Two people told me {what}. And those two don't speak.",
			"I had it off someone who'd know: {what}.",
			"You've heard, then. {What}.",
			"The way I heard it, {what}. Others tell it worse.",
			"{What}, if you believe the market.",
			"I'd not repeat it, but {what}.",
			"The talk is {what}. Take that how you like.",
			"Somebody at the docks reckons {what}.",
			"{What}. That's the third time this week I've heard it.",
			"I'll say this much: {what}.",
		};
		OutCount = 14;
		return Lines;
	}

	// StreetVoice.cs 193 to 209, confidence below 0.50: a whisper the teller
	// half believes and says anyway.
	inline const char* const* TellWhisper(int& OutCount)
	{
		static const char* const Lines[14] = {
			"There's a story going round that {what}. Probably nothing.",
			"You hear all sorts. {What}, apparently.",
			"Somebody's saying {what}. Somebody's always saying something.",
			"{What}, supposedly. People talk.",
			"I heard {what}, but not from anybody I'd trust.",
			"Bit of nonsense going about. {What}.",
			"They'll tell you {what}. They'll tell you anything.",
			"Half the street reckons {what}. Half the street's wrong.",
			"{What}? I'd want it from somebody with sense.",
			"You know how it is. {What}, they say.",
			"There's a whisper that {what}. Not worth much.",
			"{What}, or so I'm told, by people who weren't there.",
			"Don't quote me. {What}, maybe.",
			"I'd give it a week before somebody says the opposite: {what}.",
		};
		OutCount = 14;
		return Lines;
	}

	// StreetVoice.cs 216 to 232. The hearer has nerve above 0.65 and the
	// rumour is sensitive: they will not have it said out loud near them.
	inline const char* const* AnswerFrightened(int& OutCount)
	{
		static const char* const Lines[14] = {
			"Say that where it can be heard and see what it costs you.",
			"I'd keep that behind my teeth if I were you.",
			"Not here. Not with that door open.",
			"You're a braver man than me, saying it out loud.",
			"I didn't hear that. Understand me. I didn't hear it.",
			"Whatever you think you know, forget it.",
			"There's people who'd pay to hear you say that again.",
			"Stop. I mean it. Stop.",
			"You want to be careful whose name you put in a sentence.",
			"I've got my mother to think of. Talk about the weather.",
			"Some things you carry. You don't hand them round.",
			"That's the kind of talk that ends with somebody moving away.",
			"Say it quieter or don't say it.",
			"I'm going to walk off now, and you're going to let me.",
		};
		OutCount = 14;
		return Lines;
	}

	// StreetVoice.cs 233 to 249. Loyalty above 0.65: they defend the player,
	// which is what makes friendship mechanically worth having.
	inline const char* const* AnswerLoyal(int& OutCount)
	{
		static const char* const Lines[14] = {
			"That's talk. People love talk.",
			"I've known better people do worse for less.",
			"And you believed it, did you?",
			"There'll be a reason. There usually is.",
			"That's not how he's struck me.",
			"I'd want to hear it from him before I said it again.",
			"People are quick to have an opinion about a stranger.",
			"Mickey's family. That still means something to me.",
			"You'd say the same about anyone with a bit of money coming in.",
			"Half of that's true and the wrong half's the loud one.",
			"I'll not be the one carrying that any further.",
			"Give it a month. It'll be somebody else's turn.",
			"That's a hard thing to say about a man who's done me no harm.",
			"I've heard that story before, about somebody else.",
		};
		OutCount = 14;
		return Lines;
	}

	// StreetVoice.cs 250 to 266. Greed above 0.65: they hear a price on it.
	inline const char* const* AnswerGreedy(int& OutCount)
	{
		static const char* const Lines[14] = {
			"Interesting, that. Worth something to somebody.",
			"Who else knows?",
			"How long have you been sitting on it?",
			"There's people who'd want that. Paying people.",
			"That's not gossip. That's leverage.",
			"Keep it to yourself for a day or two. Do us both a favour.",
			"Who'd you tell before me?",
			"And what's he doing about it, that's the question.",
			"You could do something with that, you know.",
			"Does he know you know?",
			"I'd not give that away for nothing.",
			"Say that again, slowly.",
			"Now that IS worth hearing.",
			"Everything's worth something to the right ear.",
		};
		OutCount = 14;
		return Lines;
	}

	// StreetVoice.cs 267 to 283. No disposition above 0.65: an ordinary
	// neighbour hearing something about somebody they know.
	inline const char* const* AnswerPlain(int& OutCount)
	{
		static const char* const Lines[14] = {
			"Who told you that?",
			"Since when?",
			"God. And here?",
			"On this street?",
			"Are you sure it was him?",
			"That's the first I've heard of it.",
			"Well. That's the week made interesting.",
			"Since when has anybody round here been surprised by that?",
			"Hm. Does Sheila know?",
			"I'd rather not have heard that, if I'm honest.",
			"What, and nobody's said anything?",
			"That would explain a few things.",
			"You're serious.",
			"There's always something.",
		};
		OutCount = 14;
		return Lines;
	}
		// ---- which band, named once ---------------------------------------
		//
		// DEVIATION 10. StreetVoice.cs 145 to 148 writes the three-way
		// conditional inline; this is the same two boundaries, in one place, so
		// the instrument that names the band reads the band the run took
		// instead of a second copy of `>= 0.8`.
		//
		// 0 = at or above 0.80, the teller saw it themselves. 1 = 0.50 to
		// 0.80, somebody told them. 2 = below 0.50, a whisper they half
		// believe. The boundaries are INCLUSIVE at the top of each band,
		// exactly as the C# >= reads.
		inline int TellBandIndex(double Confidence)
		{
			if (Confidence >= 0.8) { return 0; }
			if (Confidence >= 0.5) { return 1; }
			return 2;
		}

		inline const char* const* TellBand(int BandIndex, int& OutCount)
		{
			if (BandIndex == 0) { return TellCertain(OutCount); }
			if (BandIndex == 1) { return TellSecondHand(OutCount); }
			return TellWhisper(OutCount);
		}

		// DEVIATION 10 again, for the hearer. StreetVoice.cs 211 to 214: a
		// frightened man and a greedy one have to hear the same news
		// differently or the disposition numbers under all of this are
		// decoration. ORDER IS THE BEHAVIOUR: nerve-with-a-sensitive-rumour
		// outranks loyalty, loyalty outranks greed, and > 0.65 is strict.
		//
		// 0 = will not have it said out loud. 1 = defends the player. 2 = sees
		// a price on it. 3 = an ordinary neighbour hearing something.
		inline int AnswerBandIndex(const Gossiper& To, bool Sensitive)
		{
			if (To.Nerve > 0.65 && Sensitive) { return 0; }
			if (To.Loyalty > 0.65)            { return 1; }
			if (To.Greed > 0.65)              { return 2; }
			return 3;
		}

		inline const char* const* AnswerBand(int BandIndex, int& OutCount)
		{
			if (BandIndex == 0) { return AnswerFrightened(OutCount); }
			if (BandIndex == 1) { return AnswerLoyal(OutCount); }
			if (BandIndex == 2) { return AnswerGreedy(OutCount); }
			return AnswerPlain(OutCount);
		}

		// The band names, for an instrument that has to print WHICH. Values
		// with no spaces, because every reader of this project's key=value
		// lines splits on whitespace and truncates in silence.
		inline const char* TellBandName(int BandIndex)
		{
			return BandIndex == 0 ? "confidence-at-or-above-0.80"
			     : BandIndex == 1 ? "confidence-0.50-to-0.80"
			                      : "confidence-below-0.50";
		}

		inline const char* AnswerBandName(int BandIndex)
		{
			return BandIndex == 0 ? "nerve-above-0.65-and-sensitive"
			     : BandIndex == 1 ? "loyalty-above-0.65"
			     : BandIndex == 2 ? "greed-above-0.65"
			                      : "no-disposition-above-0.65";
		}

		// ---- what the two of them SAY -------------------------------------
		//
		// DEVIATION 11. Which band spoke and which line it took, for the
		// verdict. Nothing in Exchange branches on it.
		struct ExchangeTrace
		{
			int  TellBand, TellIndex, TellCount;
			int  AnswerBand, AnswerIndex, AnswerCount;
			int  AnswerSeedValue;
			bool bComposed;      // true when a tell was actually built
			std::string Refused; // why not, when it was not

			ExchangeTrace()
				: TellBand(-1), TellIndex(-1), TellCount(0),
				  AnswerBand(-1), AnswerIndex(-1), AnswerCount(0),
				  AnswerSeedValue(0), bComposed(false), Refused("nothing-measured")
			{
			}
		};

		/// StreetVoice.cs 131. What the two of them SAY when a rumour passes
		/// between them.
		///
		/// The teller names the story; the hearer answers in the way their own
		/// disposition dictates. Both lines carry the rumour, so a player in
		/// earshot learns it by listening: the ledger row becomes a side
		/// effect of having heard rather than the event itself.
		///
		/// THE TELLING IS THE COMPOSED HALF AND THE ANSWER IS NOT, and the C#
		/// says so at 289 to 295 rather than marking both: the tell carries
		/// the summary inside it and is a new sentence every time, while the
		/// answer is a literal from a band and is in a bank as written.
		/// Marking both would be tidier and would put a renderable hole in the
		/// structural bucket the first time a reply went missing.
		inline std::vector<SpokenLine> Exchange(const RumorPtr& R, const GossiperPtr& From,
		                                        const GossiperPtr& To, int Seed,
		                                        ExchangeTrace* OutTrace)
		{
			std::vector<SpokenLine> Lines;
			if (OutTrace != 0) { OutTrace->Refused = "none"; }
			if (!R || !From || !To)
			{
				if (OutTrace != 0) { OutTrace->Refused = "no-rumour-or-no-speaker"; }
				return Lines;
			}
			// DEVIATION 14: the C#'s IsNullOrEmpty guard is an empty-string
			// guard here. Same outcome, no speech.
			const std::string What = Trim(R->Summary);
			if (What.empty())
			{
				if (OutTrace != 0) { OutTrace->Refused = "summary-carried-no-text"; }
				return Lines;
			}

			int TellCount = 0;
			const int TellBandI = TellBandIndex(R->Confidence);
			const char* const* Tells = TellBand(TellBandI, TellCount);
			const int TellI = PickIndex(Seed, TellCount);
			const std::string Tell = Render(std::string(Tells[TellI]), What);

			int AnswerCount = 0;
			const int AnswerBandI = AnswerBandIndex(*To, R->Sensitive);
			const char* const* Answers = AnswerBand(AnswerBandI, AnswerCount);
			const int ASeed = AnswerSeed(Seed, To->Id);
			const int AnswerI = PickIndex(ASeed, AnswerCount);
			const std::string Answer(Answers[AnswerI]);

			SpokenLine L1;
			L1.SpeakerId = From->Id; L1.Text = Tell;
			L1.AboutPlayer = true;   L1.Source = R; L1.Composed = true;
			SpokenLine L2;
			L2.SpeakerId = To->Id;   L2.Text = Answer;
			L2.AboutPlayer = true;   L2.Source = R; L2.Composed = false;
			Lines.push_back(L1);
			Lines.push_back(L2);

			if (OutTrace != 0)
			{
				OutTrace->TellBand = TellBandI;
				OutTrace->TellIndex = TellI;
				OutTrace->TellCount = TellCount;
				OutTrace->AnswerBand = AnswerBandI;
				OutTrace->AnswerIndex = AnswerI;
				OutTrace->AnswerCount = AnswerCount;
				OutTrace->AnswerSeedValue = ASeed;
				OutTrace->bComposed = true;
			}
			return Lines;
		}

		/// The C# signature, for a caller that wants the two lines and nothing
		/// about how they were chosen.
		inline std::vector<SpokenLine> Exchange(const RumorPtr& R, const GossiperPtr& From,
		                                        const GossiperPtr& To, int Seed)
		{
			return Exchange(R, From, To, Seed, 0);
		}

		// ---- THE REACTION LADDER AND DECISION 7 (a), ported 23 September ----
		//
		// TRANSLITERATION of StreetVoice.cs Stance, the private Rung, GazeMetres
		// and StoryThatShows, and of RemarkLedger, for the playable slice: a
		// hearer's faint knowledge shows in how they treat the player, once per
		// story and then the look. Every answer is checked against rows the C#
		// emitted (PerceptionGolden EmitStance): 9,856 stance cells over both
		// sides of every rung, the coat's 0.12 and 0.7, the loyalty weights and
		// the leash; the gazes; twelve story holders; the remark keys and the
		// recording rule. The arithmetic is in the C#'s order, operation for
		// operation, because a reordered sum is a different double.

		enum class StanceKind { Indifferent = 0, Notices = 1, Watches = 2, Comments = 3,
		                        Avoids = 4, Refuses = 5, Confronts = 6 };

		inline const char* StanceName(StanceKind K)
		{
			switch (K)
			{
				case StanceKind::Indifferent: return "Indifferent";
				case StanceKind::Notices:     return "Notices";
				case StanceKind::Watches:     return "Watches";
				case StanceKind::Comments:    return "Comments";
				case StanceKind::Avoids:      return "Avoids";
				case StanceKind::Refuses:     return "Refuses";
				case StanceKind::Confronts:   return "Confronts";
			}
			return "unknown";
		}

		// StreetVoice.cs's own Clamp01 is `v < 0 ? 0 : v > 1 ? 1 : v`, which
		// is LedgerCore::Clamp01 (Perception.h) for every value but NaN, and
		// both pass NaN through.
		inline StanceKind Rung(double Pressure, bool bLeashed)
		{
			if (Pressure >= 0.86 && !bLeashed) return StanceKind::Confronts;
			if (Pressure >= 0.72) return StanceKind::Refuses;
			if (Pressure >= 0.58) return StanceKind::Avoids;
			if (Pressure >= 0.42) return bLeashed ? StanceKind::Watches : StanceKind::Comments;
			if (Pressure >= 0.26) return StanceKind::Watches;
			if (Pressure >= 0.12) return StanceKind::Notices;
			return StanceKind::Indifferent;
		}

		inline StanceKind Stance(double Suspicion, double Loyalty, double StrongestAboutPlayer,
		                         bool bLeashed, bool bWearingCoat, bool bKnowsSomething = false,
		                         bool bRemarkedAlready = false, bool bKnowsALittle = false)
		{
			double Pressure = Clamp01(0.55 * Clamp01(Suspicion) + 0.45 * Clamp01(StrongestAboutPlayer));
			Pressure -= 0.35 * Clamp01(Loyalty - 0.5) * 2.0 * (Pressure < 0.85 ? 1.0 : 0.4);
			if (bWearingCoat && Pressure < 0.7) Pressure -= 0.12;
			Pressure = Clamp01(Pressure);
			StanceKind R = Rung(Pressure, bLeashed);
			if (bKnowsSomething)
			{
				const StanceKind Floor = bWearingCoat ? StanceKind::Notices
				                       : (bLeashed || bRemarkedAlready) ? StanceKind::Watches
				                       : StanceKind::Comments;
				if ((int)R < (int)Floor) R = Floor;
			}
			// KNOWING A LITTLE SHOWS TOO (Jafar's list, 28 September): a story
			// held under the share floor is a floor of its own, Notices; in
			// the coat, unsure it is him, nothing.
			if (bKnowsALittle && !bWearingCoat && (int)R < (int)StanceKind::Notices) R = StanceKind::Notices;
			return R;
		}

		inline double GazeMetres(StanceKind K)
		{
			return (int)K <= (int)StanceKind::Indifferent ? 0
			     : K == StanceKind::Notices ? 6
			     : K == StanceKind::Watches ? 14
			     : K == StanceKind::Comments ? 12
			     : K == StanceKind::Avoids ? 18
			     : 22;
		}

		// Arrangement.cs 54 and 77: a story of one of the outfit's nights.
		namespace Arrangement
		{
			inline bool IsNight(const RumorPtr& R)
			{
				static const std::string TopicPrefix = "player.outfit_d";
				return R && R->TopicKey().compare(0, TopicPrefix.size(), TopicPrefix) == 0;
			}
		}

		inline RumorPtr StoryThatShows(const Gossiper& G, double ShareFloor)
		{
			RumorPtr Best;
			for (std::vector<RumorPtr>::size_type I = 0; I < G.Rumors.size(); ++I)
			{
				const RumorPtr& R = G.Rumors[I];
				// His night, or what he did with the outfit's ask (town list 6z).
				if (!R || R->Content.Subject != "player" || !(R->Sensitive || Arrangement::IsNight(R))) continue;
				if (!R->Indelible && G.SuppressedHas(R->TopicKey())) continue;
				if (!(R->Confidence >= ShareFloor)) continue;
				if (!Best || R->Confidence > Best->Confidence) Best = R;
			}
			return Best;
		}

		/// RemarkLedger: who has had their say on which story. An empty key is
		/// the C#'s null (no story).
		class RemarkLedger
		{
			std::set<std::string> Said;
		public:
			static std::string KeyFor(const std::string& PersonId, const RumorPtr& R)
			{
				if (!R) return std::string();
				return PersonId + "|" + R->Content.Subject + "." + R->Content.Predicate + "=" + R->Content.Value;
			}
			bool HasRemarked(const std::string& PersonId, const RumorPtr& R) const
			{
				const std::string K = KeyFor(PersonId, R);
				return !K.empty() && Said.count(K) > 0;
			}
			bool Record(const std::string& PersonId, const RumorPtr& R, StanceKind SaidAt, bool bHeard)
			{
				if (!bHeard || SaidAt != StanceKind::Comments) return false;
				const std::string K = KeyFor(PersonId, R);
				return !K.empty() && Said.insert(K).second;
			}
			// A half-remembered story's one remark: heard, or it does not
			// count, under the story's own key, so one remark per person per
			// story whichever came first.
			bool RecordFaint(const std::string& PersonId, const RumorPtr& R, bool bHeard)
			{
				if (!bHeard) return false;
				const std::string K = KeyFor(PersonId, R);
				return !K.empty() && Said.insert(K).second;
			}
			std::size_t Count() const { return Said.size(); }
		};

		// ---- knowing a little, and the look (29 September) ----------------
		//
		// TRANSLITERATED from StreetVoice.cs's knowing section, the town list's
		// handover 1 (Jafar's list, 28 September: "someone who has heard a
		// little about Tom behaves exactly like someone who has heard nothing"
		// was the fault). Checked against PerceptionGolden EmitKnowing: the
		// half-remembered story over fifteen holders and two floors, Stance
		// with knowsALittle over 4,800 cells, the look for every stance and
		// its five constants, the faint draw over forty people and the share's
		// edge, the faint lines, RecordFaint, and RegardFor over 2,880 holders.
		// The research behind the look: production/research/gaze-and-knowing.

		/// The strongest story of his night a person still holds but would no
		/// longer pass on (under the share floor, above nothing), or null.
		inline RumorPtr StoryHalfRemembered(const Gossiper& G, double ShareFloor)
		{
			RumorPtr Best;
			for (std::vector<RumorPtr>::size_type I = 0; I < G.Rumors.size(); ++I)
			{
				const RumorPtr& R = G.Rumors[I];
				if (!R || R->Content.Subject != "player" || !(R->Sensitive || Arrangement::IsNight(R))) continue;
				if (!R->Indelible && G.SuppressedHas(R->TopicKey())) continue;
				if (!(R->Confidence > 0.0) || R->Confidence >= ShareFloor) continue;
				if (!Best || R->Confidence > Best->Confidence) Best = R;
			}
			return Best;
		}

		/// The fixed draw, 0 to 0.9999, from FNV-1a over the remark key.
		inline double FaintDraw(const std::string& Key)
		{
			return (Hash(Key) % 10000u) / 10000.0;
		}

		/// Whether somebody who knows a little says so, once: their fixed draw
		/// under the story's confidence as a share of the floor.
		inline bool MayRemarkFaintly(const std::string& PersonId, const RumorPtr& R, double ShareFloor)
		{
			const std::string K = RemarkLedger::KeyFor(PersonId, R);
			if (K.empty() || !(ShareFloor > 0.0)) return false;
			return FaintDraw(K) < R->Confidence / ShareFloor;
		}

		/// Where a stranger's glance lands: the median measured look distance,
		/// 10.3 m (Fotios and others, Sheffield, 2015), rounded.
		static const double CivilGlanceMetres = 10.0;
		/// A stranger's glance, 0.48 s (Fotios and others, 2015), rounded.
		static const double CivilGlanceSeconds = 0.5;
		/// The passing zone's near end, 3.0 to 3.7 m (Patterson and others, 2002).
		static const double PassingZoneMetres = 3.0;
		/// The knowing look: the top of the intensified glance still held at
		/// close range, 0.39 to 1.52 s (Arminen and Heino, 2023).
		static const double KnowingLookSeconds = 1.5;
		/// Where a stranger's eyes drop: Goffman's eight feet (1963).
		static const double CivilLookAwayMetres = 2.4;

		/// Where the first look lands as he comes towards them, in metres.
		inline double FirstLookMetres(StanceKind K)
		{
			const double Gaze = GazeMetres(K);
			return CivilGlanceMetres > Gaze ? CivilGlanceMetres : Gaze;
		}

		/// How long the first look holds: a glance, or for as long as he is in
		/// range (infinity) for those who watch him.
		inline double LookHoldSeconds(StanceKind K)
		{
			return K == StanceKind::Watches || K == StanceKind::Comments || K == StanceKind::Confronts
				? std::numeric_limits<double>::infinity() : CivilGlanceSeconds;
		}

		/// Where the second, knowing look comes, or 0 for none.
		inline double SecondLookMetres(StanceKind K)
		{
			return K == StanceKind::Notices ? PassingZoneMetres : 0.0;
		}

		/// Where the eyes go elsewhere as he comes close, or 0 for those who
		/// keep looking.
		inline double LookAwayMetres(StanceKind K)
		{
			return (int)K <= (int)StanceKind::Indifferent || K == StanceKind::Avoids || K == StanceKind::Refuses
				? CivilLookAwayMetres : 0.0;
		}

		/// Whether they look back after he has passed.
		inline bool LooksBack(StanceKind K)
		{
			return K == StanceKind::Watches || K == StanceKind::Comments || K == StanceKind::Confronts;
		}

		/// How much of a story about the player somebody holds.
		enum class Knowing { Nothing = 0, ALittle = 1, Enough = 2 };

		inline const char* KnowingName(Knowing K)
		{
			switch (K)
			{
				case Knowing::Nothing: return "Nothing";
				case Knowing::ALittle: return "ALittle";
				case Knowing::Enough:  return "Enough";
			}
			return "unknown";
		}

		/// One person's bearing toward the player right now (RegardFor).
		struct Regard
		{
			Knowing    HowMuch;
			RumorPtr   Story;
			StanceKind Stance;
			bool       bKnowsItIsHim;
			double     FirstLookMetres;
			double     FirstLookSeconds;
			double     SecondLookMetres;
			double     SecondLookSeconds;
			double     LookAwayMetres;
			bool       bLooksBack;
			bool       bRemarkedAlready;
			bool       bSpeaks;
			bool       bFaint;

			Regard() : HowMuch(Knowing::Nothing), Stance(StanceKind::Indifferent), bKnowsItIsHim(false),
			           FirstLookMetres(0.0), FirstLookSeconds(0.0), SecondLookMetres(0.0),
			           SecondLookSeconds(0.0), LookAwayMetres(0.0), bLooksBack(false),
			           bRemarkedAlready(false), bSpeaks(false), bFaint(false) {}
		};

		/// HOW ONE PERSON TREATS THE PLAYER RIGHT NOW, in one call, as the C#.
		/// `Familiarity` is how well they know him by sight (Acquaintance): a
		/// story shows only in somebody who can tell it is him
		/// (Acquaintance.CanNameYou is Perception's RecognitionFamiliarity).
		/// `Remarks` may be null: nobody has had their say.
		inline Regard RegardFor(const Gossiper* G, double ShareFloor, bool bWearingCoat,
		                        const RemarkLedger* Remarks, double Familiarity, bool bCompanionNear)
		{
			Regard Out;
			if (!G) return Out;
			RumorPtr Strongest;
			for (std::vector<RumorPtr>::size_type I = 0; I < G->Rumors.size(); ++I)
			{
				const RumorPtr& R = G->Rumors[I];
				if (!R || R->Content.Subject != "player") continue;
				if (!(R->Confidence >= 0.0)) continue;   // a NaN must not hide a real story
				if (!Strongest || R->Confidence > Strongest->Confidence) Strongest = R;
			}
			const RumorPtr Shows = StoryThatShows(*G, ShareFloor);
			const RumorPtr Little = !Shows ? StoryHalfRemembered(*G, ShareFloor) : RumorPtr();
			Out.Story = Shows ? Shows : Little;
			Out.HowMuch = Shows ? Knowing::Enough : Little ? Knowing::ALittle : Knowing::Nothing;
			Out.bKnowsItIsHim = Familiarity >= Perception::RecognitionFamiliarity;
			const bool bShows1 = Shows && Out.bKnowsItIsHim;
			const bool bLittle1 = Little && Out.bKnowsItIsHim;
			const bool bHad = Remarks && Remarks->HasRemarked(G->Id, Out.Story);
			Out.bRemarkedAlready = bHad;
			const double AboutHim = Out.bKnowsItIsHim && Strongest ? Strongest->Confidence : 0.0;
			Out.Stance = Stance(G->Suspicion.Value(), G->Loyalty, AboutHim, G->Leashed, bWearingCoat,
			                    bShows1, bHad, bLittle1);
			Out.FirstLookMetres = FirstLookMetres(Out.Stance);
			Out.FirstLookSeconds = LookHoldSeconds(Out.Stance);
			Out.SecondLookMetres = SecondLookMetres(Out.Stance);
			Out.SecondLookSeconds = Out.SecondLookMetres > 0 ? KnowingLookSeconds : 0.0;
			Out.LookAwayMetres = LookAwayMetres(Out.Stance);
			Out.bLooksBack = LooksBack(Out.Stance);
			// In the coat, unsure it is him: whoever the coat leaves noticing
			// him only glances and looks away, as a stranger does.
			if (bWearingCoat && Out.Stance == StanceKind::Notices)
			{
				Out.SecondLookMetres = 0.0;
				Out.SecondLookSeconds = 0.0;
				Out.LookAwayMetres = CivilLookAwayMetres;
			}
			if ((int)Out.Stance >= (int)StanceKind::Comments)
			{
				Out.bSpeaks = true;
			}
			else if (bLittle1 && bCompanionNear && !bHad && !G->Leashed && !bWearingCoat
			         && MayRemarkFaintly(G->Id, Little, ShareFloor))
			{
				Out.bSpeaks = true;
				Out.bFaint = true;
			}
			return Out;
		}

		/// Fourteen, as every band is.
		inline const char* const* FaintLines(int& OutCount)
		{
			static const char* const Lines[14] = {
				"That's Mickey's nephew, that is.",
				"Is that him? The nephew?",
				"Somebody was saying something about him. I forget what.",
				"I've heard his name somewhere. Can't place it.",
				"There was talk about that one. Or was it somebody else.",
				"Him. Something went round about him. It'll come to me.",
				"I've heard a thing or two about him. Nothing I'd swear to.",
				"His name came up. I wasn't really listening.",
				"Didn't somebody say something about him? Never mind.",
				"He's the one people were on about. Only talk, mind.",
				"Something was said about him. It's gone now.",
				"People have been saying things about him. Half of it rubbish, I expect.",
				"I heard something about him. Can't remember who from.",
				"Keeps busy, that one, so I hear. Or so somebody said.",
			};
			OutCount = 14;
			return Lines;
		}

		/// What somebody who knows a little says, once, to a companion, about
		/// him, as he goes past; null (an empty pointer) with no one or no
		/// story. The seed alone chooses (the C#'s `heard` overload, which
		/// picks a line he has not heard lately, comes with town list 6k).
		inline std::shared_ptr<SpokenLine> FaintRemark(const Gossiper* G, const RumorPtr& About, int Seed)
		{
			if (!G || !About) return std::shared_ptr<SpokenLine>();
			int Count = 0;
			const char* const* Lines = FaintLines(Count);
			std::shared_ptr<SpokenLine> Line = std::make_shared<SpokenLine>();
			Line->SpeakerId = G->Id;
			Line->Text = Pick(Seed, Lines, Count);
			Line->AboutPlayer = true;
			Line->Source = About;
			Line->Bank = "faint";
			return Line;
		}

		// ---- Recognition (29 September) ---------------------------------
		//
		// StreetVoice.cs's Recognition, left out of the port on 8 September and
		// brought in with the knowing section: something said as the player
		// goes past, by somebody holding a story about him, at Comments or
		// above. Every line invites being stopped. Checked against
		// PerceptionGolden EmitRecognition: every stance, no story, a plain one
		// and one of his night, over sixteen seeds. The seed alone chooses, as
		// for FaintRemark.

		inline const char* const* RecognitionConfronts(int& OutCount)
		{
			static const char* const Lines[14] = {
				"You and I need a word. Not here.",
				"I've been waiting to see you, as it happens.",
				"Don't walk past me. Not today.",
				"Stop there. You know why.",
				"I've been rehearsing this. Give me a minute of it.",
				"There you are. I've had four days to think about this.",
				"You're going to stand there and hear it.",
				"A word. It won't take long and it won't be pleasant.",
				"I want to hear you say it to my face.",
				"You've been avoiding this street. I noticed.",
				"No. You'll not just nod and walk on.",
				"Two minutes. You owe me that much.",
				"I'd like an answer, and I'd like it today.",
				"Look at me when I'm talking to you.",
			};
			OutCount = 14;
			return Lines;
		}

		inline const char* const* RecognitionRefuses(int& OutCount)
		{
			static const char* const Lines[14] = {
				"I've nothing for you today.",
				"Whatever it is, no.",
				"Door's shut. Try somebody else.",
				"Not for you. Not any more.",
				"I'd rather not, and I'd rather not explain why.",
				"We're closed. To you.",
				"You'll want to ask somebody who doesn't know you.",
				"No. And don't ask twice.",
				"There's nothing here you want.",
				"I've made up my mind about you.",
				"Save your breath.",
				"Not today. Not tomorrow either.",
				"I've heard enough to know my answer.",
				"Ask me in a year.",
			};
			OutCount = 14;
			return Lines;
		}

		inline const char* const* RecognitionAvoids(int& OutCount)
		{
			static const char* const Lines[14] = {
				"...",
				"Excuse me.",
				"Sorry, in a hurry.",
				"Can't stop.",
				"Another time.",
				"Mm.",
				"I'm late as it is.",
				"Not now. Sorry.",
				"Right. Right.",
				"Somebody's waiting on me.",
				"Yes. No. Sorry.",
				"I've got to be somewhere.",
				"Mind yourself.",
				"...Evening.",
			};
			OutCount = 14;
			return Lines;
		}

		// What he did with the outfit's ask (town list 6z): six a bank, from
		// somebody who heard it.
		inline const char* const* RecognitionOutfitDid(int& OutCount)
		{
			static const char* const Lines[6] = {
				"Heard you did Mickey's run.",
				"Down the landing after dark, I hear. Same as Mickey.",
				"They say you've picked up where Mickey left off.",
				"Word is you kept Mickey's arrangement. I'd keep that quiet.",
				"Late one, was it? Down by the ferry.",
				"So you're doing Mickey's rounds now.",
			};
			OutCount = 6;
			return Lines;
		}

		inline const char* const* RecognitionOutfitRefused(int& OutCount)
		{
			static const char* const Lines[6] = {
				"Heard you told them no.",
				"Heard you sent Ron back with it.",
				"They say you turned Mickey's lot down.",
				"Word is you said no to them. Brave or daft, I've not decided.",
				"You told them no, then. Not like Mickey, that.",
				"Not doing Mickey's errands, I hear.",
			};
			OutCount = 6;
			return Lines;
		}

		inline const char* const* RecognitionOutfitNoShow(int& OutCount)
		{
			static const char* const Lines[6] = {
				"Heard they waited on you at the landing.",
				"Somebody stood by the ferry half the night, I'm told.",
				"They say you never turned up.",
				"Word is you left them waiting. They'll not like that.",
				"Mickey'd never have kept them waiting, they say.",
				"Busy, were you? Not at the landing, anyway.",
			};
			OutCount = 6;
			return Lines;
		}

		inline const char* const* RecognitionSensitive(int& OutCount)
		{
			static const char* const Lines[14] = {
				"There he is. The busy one.",
				"Heard your name this week. More than once.",
				"Funny hours you keep.",
				"You get about, don't you.",
				"Sleeping all right?",
				"You want to be careful, a man as talked-about as you.",
				"Someone was asking after you. I said I hadn't seen you.",
				"Busy week, was it.",
				"Odd, the places a name turns up.",
				"I'd not say what I've heard. But I've heard it.",
				"You'll know what people are saying.",
				"Still standing. That surprises some.",
				"Careful on that corner. People watch it.",
				"You and I should have a proper talk one day.",
			};
			OutCount = 14;
			return Lines;
		}

		inline const char* const* RecognitionOrdinary(int& OutCount)
		{
			static const char* const Lines[14] = {
				"Mickey's nephew. Still standing, then.",
				"All right.",
				"How's Mickey's treating you?",
				"Cold enough for you?",
				"Your uncle'd have hated this weather.",
				"Tell Sheila I said hello.",
				"Still open, is it?",
				"You've the look of him, you know. Around the eyes.",
				"Long day?",
				"Mind how you go.",
				"That step of yours needs seeing to.",
				"Good to see the lights on down there.",
				"You'll be at the market Thursday, I expect.",
				"Evening.",
			};
			OutCount = 14;
			return Lines;
		}

		inline std::shared_ptr<SpokenLine> Recognition(const Gossiper* G, const RumorPtr& About, StanceKind K, int Seed)
		{
			if (!G || (int)K < (int)StanceKind::Comments) return std::shared_ptr<SpokenLine>();
			const bool bNight = Arrangement::IsNight(About) && About->Hops > 0;
			const char* Bank = 0;
			const char* const* Lines = 0;
			int Count = 0;
			if ((int)K >= (int)StanceKind::Confronts)          { Bank = "recognition/confronts";      Lines = RecognitionConfronts(Count); }
			else if (K == StanceKind::Refuses)                 { Bank = "recognition/refuses";        Lines = RecognitionRefuses(Count); }
			else if (K == StanceKind::Avoids)                  { Bank = "recognition/avoids";         Lines = RecognitionAvoids(Count); }
			else if (bNight && About->Content.Value == "did")     { Bank = "recognition/outfit-did";     Lines = RecognitionOutfitDid(Count); }
			else if (bNight && About->Content.Value == "refused") { Bank = "recognition/outfit-refused"; Lines = RecognitionOutfitRefused(Count); }
			else if (bNight && About->Content.Value == "noshow")  { Bank = "recognition/outfit-noshow";  Lines = RecognitionOutfitNoShow(Count); }
			else if (About && About->Sensitive)                { Bank = "recognition/sensitive";      Lines = RecognitionSensitive(Count); }
			else                                               { Bank = "recognition/ordinary";       Lines = RecognitionOrdinary(Count); }
			std::shared_ptr<SpokenLine> Line = std::make_shared<SpokenLine>();
			Line->SpeakerId = G->Id;
			Line->Text = Pick(Seed, Lines, Count);
			Line->AboutPlayer = (bool)About;
			Line->Source = About;
			Line->Bank = Bank;
			return Line;
		}
	}
}
