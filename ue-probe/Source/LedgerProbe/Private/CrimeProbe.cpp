// THE CRIME, THE WITNESS AND THE OVERHEARD CONSEQUENCE. -LedgerCrime.
//
// Ruling: game-design/decision-2026-09-08-the-crime-the-witness-and-the-
// overheard-consequence.md. A half-brick through a shop window, committed
// twice: once in a witness's sight and once with a terrace between her and
// it, which is the rule-5b pair. What she saw is decided by Observe.Resolve
// on real traced geometry, filed as a memory, carried to a second NPC by the
// ported GossipMill.Tick with a real together predicate, and spoken by him at
// the rung she actually reached.
//
// WHY ALedgerGameMode NEEDS NO CHANGE, AND NEITHER DO THE THREE EXISTING
// SWITCHES. InitGame checks the command line for -LedgerVignette,
// -LedgerShot and -LedgerGoldenTest and has never heard of -LedgerCrime, so a
// crime run falls through to the SAME branch a genuine human launch takes:
// DefaultPawnClass stays ALedgerCharacter and
// LedgerVignetteShot::BuildInteractiveStreet(GetWorld()) runs unmodified,
// collision on, PlayerStart at cam_A. A plain launch with no switch is
// bit-for-bit unaffected: Start() below is called from one place and only
// when the switch is present. Checked by reading LedgerGameMode.cpp and
// LedgerProbe.cpp before writing this file, not assumed from their names.
//
// WHERE EVERY DECISION IN THIS RUN IS MADE, WHICH IS NOT HERE. CrimeProbe.h
// carries the arithmetic, the selection and every printed string, because
// this project's top layer does not compile in the container that writes it
// and a formatter shipped unrun is the quietest instrument fault there is
// (.claude/rules/instruments.md, 25 August). g++ compiles and RUNS that
// header's Selftest before any dispatch, and this file calls the same
// Selftest at Start so its result is a number on the verdict rather than a
// claim in a comment. What is left here is what only a running engine can
// answer: where an actor is, what a trace hit, what a screenshot contains.
//
// TWO CORRECTIONS THIS FILE CARRIES AGAINST THE RULING, both measured:
//
//   1. THE VICTIM SIGHTLINE IS CAPTURED BEFORE THE DEED. Once
//      east_parade_glass0 is hidden with its collision off, a trace from the
//      witness's eye to the window centre passes through the empty pane and
//      hits east_parade_interior0 behind it, so victimOccluded would read yes
//      and the ACCEPTING case would print as a rejection. Every vantage is
//      therefore read at the before_crime milestone with the glass standing,
//      the deed follows, and each witness line says victimVantageAt=
//      before-the-deed/glass-standing.
//
//   2. actorBlocker=<piece name> NEEDS AN EXPORT THAT DID NOT EXIST.
//      SpawnPiece calls SetActorLabel under WITH_EDITOR only, so in a
//      packaged build a hit actor answers GetName() with StaticMeshActor_NNN.
//      LedgerVignetteShot::StreetPieceNameOf is the reverse of the
//      name-to-actor lookup that already existed; it mutates nothing.
//
// AND ONE PLACE THE RULING CONTRADICTS ITSELF. Section 4 item 7's example
// prints overheardLineIds=cw-ws-r3-02,cw-ov-r3-01, which one seed cannot
// produce: seed = Day * 31 + Hour is 43 at D1 12:00 and 43 % 3 is 1 for both
// contexts, so the pair is cw-ws-r3-02,cw-ov-r3-02. The RULE is followed and
// the seed, the modulus and the picked index are all printed so a reader can
// check the arithmetic rather than take this comment's word for it.
//
// WHAT THIS RUN DOES NOT DO, so nobody looks for it: no third NPC, no second
// crime kind, no night, no rain, no Mixamo body, no voice, no sound, no
// StreetVoice composition, no Attention accumulator (SecondsWatching is this
// probe's own count and RungFloor is 0, both printed), no suspicion
// consequences, no save file, no memory loading, and no yard in the street's
// own JSON.
#include "CrimeProbe.h"

#include "VignetteShot.h"
#include "PersonAnim.h"
#include "CastDay.h"
#include "TownRounds.h"
#include "LiveClock.h"
#include "TownNews.h"
#include "TownSave.h"
#include "Waiting.h"
#include "TownWeek.h"
#include "Suspecting.h"
#include "FrameStats.h"

#include "CoreMinimal.h"
#include "Misc/Paths.h"
#include "Misc/FileHelper.h"
#include "Misc/CommandLine.h"
#include "SaveCodec.h"
#include "Misc/App.h"
#include "TitleScreen.h"
#include "FirstMoments.h"
#include "DayOne.h"
#include "LedgerGarments.h"
#include "Misc/Parse.h"
#include "Misc/DateTime.h"
#include "HAL/FileManager.h"
#include "HAL/PlatformMisc.h"
#include "HAL/PlatformProcess.h"
#include "HAL/PlatformTime.h"
#include "Containers/Ticker.h"
#include "Modules/ModuleManager.h"
#include "UnrealClient.h"

#include "Engine/Engine.h"
#include "Engine/World.h"
#include "CollisionQueryParams.h"
#include "GameFramework/Actor.h"
#include "GameFramework/Pawn.h"
#include "GameFramework/PlayerController.h"
#include "IImageWrapper.h"
#include "IImageWrapperModule.h"
// THE INPUT PATH, FOR THE ACT. LedgerCharacter is the pawn that owns the
// binding; InputKeyEventArgs and the device mapper are what a key press is
// made of once Slate has finished with it, which is the shape the player
// controller's own InputKey takes.
#include "LedgerCharacter.h"
#include "SliceCharacter.h"
#include "LedgerSession.h"
#include "Misc/CoreDelegates.h"
#include "Engine/StaticMeshActor.h"
#include "Engine/StaticMesh.h"
#include "Components/StaticMeshComponent.h"
#include "Components/LocalLightComponent.h"
#include "UObject/UObjectIterator.h"
#include "AudioDevice.h"
#include "AudioMixerBlueprintLibrary.h"
#include "Components/AudioComponent.h"
#include "Animation/AnimSingleNodeInstance.h"
#include "Animation/AnimSequenceBase.h"
#include "Kismet/GameplayStatics.h"
#include "Sound/SoundAttenuation.h"
#include "Sound/SoundWave.h"
#include "InputKeyEventArgs.h"
#include "GenericPlatform/GenericPlatformInputDeviceMapper.h"
#include "Framework/Application/SlateApplication.h"
#include "Widgets/Input/SEditableTextBox.h"
#include "LedgerJacket.h"
#include "LedgerTalkLight.h"
#include "Camera/PlayerCameraManager.h"
#include "Camera/CameraActor.h"
#include "Camera/CameraComponent.h"
#include "Widgets/Layout/SBorder.h"
#include "Widgets/Layout/SBox.h"
#include "Widgets/SBoxPanel.h"
#include "Widgets/Text/STextBlock.h"
#include "Styling/CoreStyle.h"
#include "Engine/GameViewportClient.h"
#include "Components/CapsuleComponent.h"
#include "Sound/SoundWaveProcedural.h"
#include "Animation/SkeletalMeshActor.h"
#include "EngineUtils.h"
#include "UObject/UObjectIterator.h"

#include <map>
#include <set>
#include <string>
#include <vector>

using namespace LedgerCore;

namespace
{
	// ---- ceilings and durations, none of them a threshold ----------------
	const double kWorldCeiling          = 45.0;
	const double kPawnCeiling           = 30.0;
	const double kSettleAfterSpawn      = 0.5;
	const double kSettleAfterTeleport   = 0.5;
	// THE APPROACH IS THE CLIP'S OWN MATERIAL and the witness's watching
	// time, both at once: she accrues SecondsWatching for exactly as long as
	// her trace to him holds, which is what Perception.NoticeSeconds
	// documents as belonging there. Two seconds of ordinary movement input,
	// which the walk probe measured at about 2 m/s, is four metres of street.
	const double kApproachSeconds       = 2.0;
	const double kShotFileCeiling       = 15.0;
	const double kSeqFileCeiling        = 5.0;

	const TCHAR* kGlassA = TEXT("east_parade_glass0");
	// The light the story's "later that week, evening" is played in: the
	// shared scene file's own night row, lamps lit.
	const char* kEveningCondition = "wet_night";
	const TCHAR* kGlassB = TEXT("east_parade_glass1");
	// RITA'S WINDOW, 30 September (Jafar's list, item 1): free play's crime is
	// the pawn shop's window, two doors up from Mickey's, where the town's
	// consequences put it (production/handovers/6ar-after-a-deed.md); the
	// scripted encounter keeps Mickey's, which the regression measures.
	const TCHAR* kGlassR = TEXT("east_parade_glass2");
	bool bRitasWindow = false;
	// Rita's pane in the scene file as the street set it up (WindowLook puts it back so).
	bool bWindowGlassStartRead = false, bWindowGlassStartHidden = true, bWindowGlassStartCollides = false;

	// The bank, found the same way the piece list is (VignetteShot.cpp's
	// FindSpec): a packaged build's ProjectDir is the STAGED project, not the
	// source tree, so one hard-coded location works in exactly one of the two
	// ways this binary gets run. Searching is fine; searching silently is
	// not, so the candidates tried are printed.
	const TCHAR* kBankLeaf = TEXT("crime-witness-v1.json");
	const TCHAR* kBankRepoPath = TEXT("content/dialogue/crime-witness-v1.json");

	// ---- phases ----------------------------------------------------------
	enum class ECrimePhase : uint8
	{
		WaitWorld, WaitPawn, SettleAfterSpawn, PlaceProps,
		ShotStart,
		ApproachA, PlaceForA, SettleA, MeasureA, ShotBeforeA, SeqBeforeA,
		AwaitActA, CommitA, SeqAfterA, ShotAfterA, FleeYard, FleeWatch, Round1,
		MoveW1ToYard, ApproachB, PlaceForB, SettleB, MeasureB, ShotBeforeB,
		SeqBeforeB, AwaitActB, CommitB, SeqAfterB, ShotAfterB, Round2,
		MoveToOverhear, SettleOverhear, OverheardHold, ShotOverheard,
		MeetThird,
		Talk, SaveDisk, LoadDisk,
		LiveWaitDeed, LiveAfterDeed, LiveRoam,
		LiveTitle,
		LiveWalkRound,
		Done
	};

	// THE ENCOUNTER'S OWN CLOCK STANDS STILL WHILE THE WORLD IS PAUSED, 29
	// September (Esc pauses now: the twenty a friend would notice, 19). Its
	// scenes are timed by the wall clock, so without this the evening would
	// arrive while the game stood paused.
	double GPausedTotal = 0.0;
	double GPausedSince = -1.0;
	const TCHAR* const kPausedLine = TEXT("Paused. Esc to go on, Q to quit the game.");
	double NowS()
	{
		const double T = FPlatformTime::Seconds();
		return (GPausedSince >= 0.0 ? GPausedSince : T) - GPausedTotal;
	}

	FTSTicker::FDelegateHandle GTicker;
	ECrimePhase GPhase      = ECrimePhase::WaitWorld;
	double      GPhaseStart = 0.0;
	double      GRunStart   = 0.0;
	double      GLastTick   = 0.0;
	int32       GTicks      = 0;
	FString     GFinishReason = TEXT("process-completed-normally");

	void PlayShout();
	void WriteEncounterVerdict();

	// ---- the act, and what is known about how it arrived -----------------
	//
	// FOUR SEPARATE FACTS, PER CRIME, because an outside reader found that
	// collapsing any two of them lets the evidence say something that is not
	// so: where the press was delivered, how many times the character's own
	// binding fired, whether the deed was therefore attempted, and whether
	// the deed actually took. Every one of these is an array because a
	// whole-run global printed on a per-crime row reads as that crime's
	// answer while carrying the other one's.
	int32 GActPressesSent[2] = { 0, 0 };
	int32 GActRequestsSeen[2] = { 0, 0 };
	int32 GActStaleDropped[2] = { 0, 0 };
	// WHERE THE PRESS GOT TO, not whether a pointer was non-null. The three
	// answers are different failures with different fixes.
	const TCHAR* GActPressLanded[2] = { TEXT("not-attempted"), TEXT("not-attempted") };
	bool  GActGaveUp[2] = { false, false };
	bool  GActAttempted[2] = { false, false };
	bool  GActTook[2] = { false, false };
	const TCHAR* GActPawnClass[2] = { TEXT("not-asked"), TEXT("not-asked") };

	APawn*  GPawn = nullptr;

	// ---- THE INTEGRATED ENCOUNTER, Jafar 24 September --------------------
	//
	// -Encounter=play|reload|unseen, with -LedgerCrime -LedgerSlice. PLAY:
	// the new player character commits crime A by its own key, the witness
	// sees it through the perception above, shouts where she stands, the
	// gossip rounds carry it to the lad and his mate, the player questions
	// the lad through the conversation helper with the lad's own memories and
	// the simulation's day, and the town is saved TO DISK before the process
	// quits. RELOAD: a new process, the same authoring, the save READ BACK
	// FROM DISK, and the lad questioned again. UNSEEN: a clean start where
	// only crime B, the occluded one, is committed: nobody sees it and nobody
	// knows. Each writes ue-encounter-<mode>-verdict.txt; the crime module's
	// own files are renamed so the crime run's evidence is never overwritten.
	enum class EEncounter : uint8 { None, Play, Reload, Unseen, Live };
	EEncounter GEnc = EEncounter::None;
	std::string GFiledSummaryA;         // what the witness filed for crime A
	bool   bShoutPlaying = false, bShoutRecording = false, bShoutWavWritten = false;
	double GShoutAt = 0.0, GShoutPlayerM = -1.0;
	FString GShoutNote = TEXT("not-played");
	std::string GTalkWhy = "not-asked", GTalkReply = "none", GTalkHeard = "none", GTalkCard = "none";
	int    GTalkDay = 0, GTalkHour = 0, GTalkHeardCount = 0;
	bool   bTalkHeardCrime = false, bTalkQuestioned = false, bTalkFake = false;
	bool   bTalkAnswered = false;      // the model answered: not offline, not timed out, no error
	bool   bShoutSpatial = false;
	double GShoutFalloffM = 0.0;
	std::string GSavedByCommit = "none";
	// WHO HAD REASON TO SUSPECT HIM, 24 September: the lad's sighting of the
	// man running through the yard, and the level the Core derived for the lad
	// and for his mate from what each of them held.
	double GFleeSeconds = 0.0, GFleeMetres = -1.0, GFleeCertainty = 0.0;
	int    GFleeRung = -1;
	bool   bFleeSeen = false, bFleeFiled = false;
	std::string GFleeSummary = "none";
	std::string GSuspN2 = "not-asked", GSuspR3 = "not-asked", GSuspW1 = "not-asked", GSuspWhyN2 = "none";
	int    GFleeOthersSeen = 0;          // other people the lad could see while the man ran
	int    GW1RungA = -1;                // the rung the shopkeeper reached on crime A, saved with the town
	bool   bSavedToDisk = false, bLoadedFromDisk = false;
	int    GSavedBytes = 0, GLoadedBytes = 0;
	int    GClockDay = 0, GClockHour = 0, GClockMinute = 0;
	FString GSaveDirUsed = TEXT("none");
	AActor* GW1Body = nullptr;
	AActor* GN2Body = nullptr;
	AActor* GYardFloor = nullptr;
	AActor* GGlass[2] = { nullptr, nullptr };

	int32 GBodiesSpawned = 0, GShardsSpawned = 0, GBricksSpawned = 0, GFloorSpawned = 0;
	int32 GProbePiecesAsked = 0;

	// ---- what the run measured -------------------------------------------
	std::vector<LedgerCrime::Reading> GReadings;
	LedgerCrime::CrimeReading GCrime[2];
	LedgerCrime::RoundReading GRound1, GRound2;
	LedgerCrime::OverheardReading GOverheard;
	LedgerCrime::SelftestResult GSelftest;
	std::string GBankText;
	std::vector<std::string> GBankTried;
	// TWO STRINGS OFF ONE ROW, queue 157: the sentence she SAYS and the clause
	// the mill FILES. Both are on the verdict's bank line, because a reader who
	// can see only one cannot tell which one got spliced.
	std::string GSummaryText = "none", GReplyText = "none", GSummaryClause = "none";
	int GAchievedRung = 0;

	// THE RUMOUR THE MILL ACTUALLY CARRIED, queue 147. GossipMill::Tick hands
	// the LISTENER'S OWN COPY back on the event (Gossip.cs 386 to 398: the
	// heard rumour at the decayed confidence, not the speaker's), and
	// GossipDirector.cs 587 composes from exactly that copy. So this is what
	// the exchange is built from, and it is a handle on the object in n2's
	// Rumors rather than a reconstruction of it.
	RumorPtr GCarried;

	// SECONDS WATCHING, MEASURED, one accumulator per witness per crime. The
	// ticker adds this frame's delta for a witness whose sightline to the
	// actor holds RIGHT NOW, which is what Witnesses.cs 178 to 192 says
	// belongs in the field. -1 means the accumulators are off.
	int    GWatchSlot = -1;
	double GSeconds[2][2] = { { 0.0, 0.0 }, { 0.0, 0.0 } };

	// THE CONSTABLE, 22 September: a third body, NOT a witness. He is kept out
	// of GReadings on purpose, so nothing he sees is filed, offered to the mill
	// or counted by the control; his readings exist only to be handed to the
	// arrest. He accrues his own watching seconds by the same rule as w1 and
	// n2, because a constable who never looked long enough has not seen it.
	// NOT COUNTED IN GBodiesSpawned, whose verdict key reads "/2" and means the
	// two witnesses; he has his own flag.
	AActor* GC1Body = nullptr;
	bool    bC1Spawned = false;
	double  GC1Seconds[2] = { 0.0, 0.0 };
	LedgerCrime::Reading       GC1Reading[2];
	LedgerCrime::ArrestReading GArrest[2];
	int     GConfrontCalls = 0;
	int    GWatchTicks[2] = { 0, 0 };

	// ---- the mill --------------------------------------------------------
	GameTime GNow(1, 12, 0);
	// THE CLOCK THAT RUNS WITH PLAY (LiveClock.h; Jafar's list of 30 September,
	// item 1: no waiting forty seconds, no jump to day four), in free play only:
	// -LiveScript keeps the scripted encounter's fixed hours, which the build
	// machine's regression measures. A new game starts it at nine on day 1, as
	// the town's first hour on paper does; a load puts it back where it was.
	LiveClock GClock;
	bool bClockRuns = false;
	bool bLiveScript = false;    // -LiveScript, the scripted encounter (see THE LIVE ENCOUNTER, SCRIPTED)
	// THE THREE IN THE STREET BY THE CAST'S OWN IDS in free play (the town's
	// route, production/handovers/ROUTE.md, step 0: "key the mill by the
	// cast's ids (lena, sam, rocco), not w1, n2, r3, or Arrangement and
	// WeeksEnd find nobody"); the scripted encounter and the regression keep
	// the probe's own, which their measured rows name.
	std::string GIdW1 = "w1", GIdN2 = "n2", GIdR3 = "r3";
	// THE TOWN'S WEEK (TownWeek.h; production/handovers/ROUTE.md), in free
	// play: its asks, Ada's tea, the police file, the damage, the arrests,
	// the week's end and the hours the town has talked, run hour by hour in
	// the order the Core's own week runs them (tools/route_week_check.py
	// holds the two together). One TownSave of it, town.json.
	TownWeek GWeek;
	// The deed's story, as the mill holds it in free play: "player.window_d<day>"
	// (ROUTE.md step 2), set when he does it.
	std::string GWindowTopic = "player.window_d1";
	// Sheila's trust, as her talk reports it (the reply's trusts / trustEarned),
	// kept in the save: her week's question is over the real book once she has it.
	bool bSheilaTrusts = false;
	// THE DEED'S STORY KEY AS FILED (the review's A3): in free play
	// "player.window_dN", N its day; the scripted encounter keeps its own.
	std::string DeedKeyNow() { return bRitasWindow ? GWindowTopic : std::string(LedgerCrime::WindowDeedKey()); }
	// Those who only heard the smash (the review's A1): they hold the damage
	// heard, not a story about him; they never "find" it later either.
	std::set<std::string> GHeardOnly;
	// WHERE HE STOOD at the save (street metres, and his heading), so a
	// reload puts him back there rather than at the street's start.
	bool bLoadPlace = false;
	double GLoadX = 0.0, GLoadZ = 0.0, GLoadYaw = 0.0;
	int  GLightNight = -1;       // the street's light last applied: 1 night, 0 day
	/// What one exchange of talk costs, in game minutes: the clock is held while
	/// he talks, so a slow reply never costs him time (production/research/game-clock).
	constexpr int kTalkMinutes = 5;
	void ClockCharge(int Minutes);
	void ConsequenceHour(const GameTime& H);
	void ConstableHour(const GameTime& H);
	bool NearPlace(const char* Place, double Metres);
	void WindowLook();
	std::shared_ptr<SocialGraph> GGraph;
	std::shared_ptr<GossipMill>  GMill;
	GossiperPtr GW1, GN2;
	// THE THIRD RESIDENT, 22 September: in the mill from the start, tied to
	// the lad only, and WITHOUT A BODY until the meeting - the together test
	// measures bodies, so until then he is with nobody and hears nothing.
	GossiperPtr GR3;
	AActor* GR3Body = nullptr;
	LedgerCrime::RoundReading GRound3;

	// ---- the shot in flight, one at a time -------------------------------
	bool    GShotInFlight        = false;
	bool    GSeqInFlight         = false;
	FString GShotPath;
	FString GShotName;
	bool    GShotUsedHighRes     = false;
	bool    GShotTriedHighResOne = false;
	int64   GShotSizeTracker     = -1;
	double  GShotWaitStart       = 0.0;
	std::vector<std::string> GShotLines;
	int32   GShotsAttempted = 0, GShotsWrote = 0;
	double  GLastSeqCaptureTime = 0.0;
	int32   GSeqRequested = 0, GSeqWrote = 0, GSeqForced = 0;
	std::vector<std::string> GSeqKeys;

	// WHICH BEAT A SEQUENCE FRAME WAS TAKEN ON, carried on the frame's own
	// keys line for tools/clip-from-frames.py to caption from. Set at phase
	// transitions and read at capture, so a frame can never claim a beat that
	// was not running when the shutter opened.
	std::string GBeat = "start", GBeatSpeaker = "none", GBeatLineId = "none";
	// THE WORDS ON THE FRAME, and where they came from. A composed telling is
	// not in the bank and cannot be captioned by id, so the text rides on the
	// keys line beside the id.
	std::string GBeatLineText, GBeatLineTextSource;
	bool GBeatHeard = false;

	// ---- small engine helpers, the same shapes WalkProbe.cpp uses --------
	UWorld* GameWorld()
	{
		if (!GEngine) { return nullptr; }
		for (const FWorldContext& Ctx : GEngine->GetWorldContexts())
		{
			if (Ctx.WorldType == EWorldType::Game && Ctx.World() != nullptr) { return Ctx.World(); }
		}
		return nullptr;
	}

	FString AbsProject(const TCHAR* Leaf)
	{
		return FPaths::ConvertRelativePathToFull(FPaths::Combine(FPaths::ProjectDir(), Leaf));
	}

	FString ExeDir(const TCHAR* Leaf)
	{
		return FPaths::Combine(FPaths::GetPath(FPlatformProcess::ExecutablePath()), Leaf);
	}

	FString CrimeSha()
	{
		FString Sha;
		if (!FParse::Value(FCommandLine::Get(), TEXT("LedgerCommit="), Sha) || Sha.IsEmpty())
		{
			Sha = TEXT("SHA-UNKNOWN");
		}
		return Sha.Replace(TEXT(" "), TEXT("~"));
	}

	// BOTH PLACES, for the reason the walk verdict names: a packaged build's
	// ProjectDir is the staged project and the workflow step looks in three
	// candidates, so writing one file to one of them is a coin toss.
	const TCHAR* EncName()
	{
		switch (GEnc)
		{
		case EEncounter::Play:   return TEXT("play");
		case EEncounter::Reload: return TEXT("reload");
		case EEncounter::Unseen: return TEXT("unseen");
		case EEncounter::Live:   return TEXT("live");
		default:                 return TEXT("none");
		}
	}

	void SaveBoth(const FString& InLeaf, const FString& Body)
	{
		// AN ENCOUNTER RUN NEVER WRITES OVER THE CRIME RUN'S EVIDENCE: its
		// copies of the crime module's files carry the encounter's name.
		FString Leaf = InLeaf;
		if (GEnc != EEncounter::None && Leaf.StartsWith(TEXT("ue-crime")))
		{
			Leaf = FString::Printf(TEXT("ue-encounter-%s-crime%s"), EncName(), *Leaf.Mid(8));
		}
		FFileHelper::SaveStringToFile(Body, *AbsProject(*Leaf));
		FFileHelper::SaveStringToFile(Body, *ExeDir(*Leaf));
	}

	std::string Utf8(const FString& S) { return std::string(TCHAR_TO_UTF8(*S)); }
	FString Un(const std::string& S)   { return FString(UTF8_TO_TCHAR(S.c_str())); }

	// ---- the two frames, converted in exactly one place ------------------
	//
	// The shared file's frame is x along, y up, z across; the engine's X is
	// x*100, its Y is z*100 and its Z is y*100. VignetteShot.cpp's SpawnPiece
	// is the other converter and it is the one this matches.
	FVector ToUE(const LedgerCrime::P3& P)
	{
		return FVector((float)(P.X * 100.0), (float)(P.Z * 100.0), (float)(P.Y * 100.0));
	}

	LedgerCrime::P3 ToStreet(const FVector& V)
	{
		return LedgerCrime::P3((double)V.X / 100.0, (double)V.Z / 100.0, (double)V.Y / 100.0);
	}

	bool SizeSettled(const FString& Path, int64& Tracker)
	{
		const int64 Size = IFileManager::Get().FileSize(*Path);
		if (Size <= 0) { Tracker = -1; return false; }
		const bool bSame = (Size == Tracker);
		Tracker = Size;
		return bSame;
	}

	FString NewestPngUnder(const FString& Dir, int32& OutCount)
	{
		TArray<FString> Found;
		IFileManager::Get().FindFilesRecursive(Found, *Dir, TEXT("*.png"), true, false, false);
		OutCount = Found.Num();
		FString Best;
		FDateTime BestTime = FDateTime::MinValue();
		for (const FString& F : Found)
		{
			const FDateTime T = IFileManager::Get().GetTimeStamp(*F);
			if (Best.IsEmpty() || T > BestTime) { Best = F; BestTime = T; }
		}
		return Best;
	}

	// DECODE THE FILE THAT IS ABOUT TO BE COMMITTED, not a buffer the engine
	// held in memory: rule 4, read the artifact you are shipping. A fourth
	// copy of this decode; the other three are in LedgerProbe.cpp,
	// VignetteShot.cpp and WalkProbe.cpp, and this change's scope does not
	// reach into any of their capture paths to merge them.
	bool DecodeBgra(const FString& PngPath, TArray64<uint8>& OutBgra, int32& OutW, int32& OutH,
	                FString& OutNote)
	{
		TArray<uint8> Compressed;
		if (!FFileHelper::LoadFileToArray(Compressed, *PngPath) || Compressed.Num() == 0)
		{
			OutNote = TEXT("file-would-not-load-or-was-empty");
			return false;
		}
		IImageWrapperModule* Mod =
			FModuleManager::Get().LoadModulePtr<IImageWrapperModule>(FName("ImageWrapper"));
		if (Mod == nullptr) { OutNote = TEXT("imagewrapper-module-missing"); return false; }
		TSharedPtr<IImageWrapper> Wrapper = Mod->CreateImageWrapper(EImageFormat::PNG);
		if (!Wrapper.IsValid()) { OutNote = TEXT("no-png-wrapper"); return false; }
		if (!Wrapper->SetCompressed(Compressed.GetData(), (int64)Compressed.Num()))
		{
			OutNote = TEXT("setcompressed-refused-the-bytes");
			return false;
		}
		OutW = Wrapper->GetWidth();
		OutH = Wrapper->GetHeight();
		if (OutW <= 0 || OutH <= 0) { OutNote = TEXT("decoded-size-was-zero"); return false; }
		if (!Wrapper->GetRaw(ERGBFormat::BGRA, 8, OutBgra)) { OutNote = TEXT("getraw-refused"); return false; }
		return OutBgra.Num() >= (int64)OutW * (int64)OutH * 4;
	}

	// MEASURE, THEN JUDGE, WITH THE MATHS COMING FROM FrameStats.h, which g++
	// runs before this file compiles.
	std::string MeasureShotFile(const FString& Path, const FVector& Loc, bool& OutWrote)
	{
		OutWrote = false;
		const int64 Bytes = IFileManager::Get().FileSize(*Path);
		const std::string ShotNameUtf8(TCHAR_TO_UTF8(*GShotName));
		char Head[192];
		std::snprintf(Head, sizeof(Head), "crimeShot=%s crimeShotAtXYZcm=%.1f/%.1f/%.1f ",
			ShotNameUtf8.c_str(), Loc.X, Loc.Y, Loc.Z);
		TArray64<uint8> Bgra;
		int32 W = 0, H = 0;
		FString Note;
		if (!DecodeBgra(Path, Bgra, W, H, Note))
		{
			return std::string(Head) + "shotStatus=" + (Bytes > 0 ? "UNDECODABLE" : "NO-FILE")
			     + " shotBytes=" + std::to_string(Bytes)
			     + " shotNote=" + std::string(TCHAR_TO_UTF8(*Note));
		}
		const LedgerFrame::FrameStats St =
			LedgerFrame::Measure((const unsigned char*)Bgra.GetData(), W, H);
		OutWrote = !St.Blank;
		return std::string(Head) + LedgerFrame::PixelLine(St) + " shotBytes=" + std::to_string(Bytes);
	}

	void ShotBegin(const FString& Path, double Now)
	{
		GShotPath = Path;
		GShotUsedHighRes = false;
		GShotTriedHighResOne = false;
		GShotSizeTracker = -1;
		GShotWaitStart = Now;
		IFileManager::Get().Delete(*Path, false, true, true);
		FScreenshotRequest::RequestScreenshot(GShotPath, false, false);
	}

	bool ShotPump(double Now, const FVector& Loc, double Ceiling, bool bCountsTowardShotsWrote,
	              std::string& OutLine)
	{
		bool bReady = false;
		if (!GShotUsedHighRes)
		{
			bReady = SizeSettled(GShotPath, GShotSizeTracker);
		}
		else
		{
			int32 Count = 0;
			const FString Newest = NewestPngUnder(
				FPaths::ConvertRelativePathToFull(FPaths::ProjectSavedDir()), Count);
			if (!Newest.IsEmpty() && SizeSettled(Newest, GShotSizeTracker))
			{
				IFileManager::Get().Copy(*GShotPath, *Newest, true, true);
				IFileManager::Get().Delete(*Newest, false, true, true);
				bReady = true;
			}
		}
		if (bReady)
		{
			bool bWrote = false;
			OutLine = MeasureShotFile(GShotPath, Loc, bWrote);
			if (bWrote && bCountsTowardShotsWrote) { ++GShotsWrote; }
			if (bWrote && !bCountsTowardShotsWrote) { ++GSeqWrote; }
			return true;
		}
		if ((Now - GShotWaitStart) < Ceiling) { return false; }
		if (!GShotUsedHighRes && !GShotTriedHighResOne)
		{
			GShotUsedHighRes = true;
			GShotTriedHighResOne = true;
			GShotWaitStart = Now;
			GShotSizeTracker = -1;
			if (GEngine != nullptr) { GEngine->Exec(GameWorld(), TEXT("HighResShot 960x540")); }
			return false;
		}
		const std::string ShotNameUtf8(TCHAR_TO_UTF8(*GShotName));
		char Head[192];
		std::snprintf(Head, sizeof(Head), "crimeShot=%s crimeShotAtXYZcm=%.1f/%.1f/%.1f ",
			ShotNameUtf8.c_str(), Loc.X, Loc.Y, Loc.Z);
		OutLine = std::string(Head) + "shotStatus=NO-FILE shotNote=neither-candidate-wrote-a-file-in-"
		        + std::to_string((int)Ceiling) + "s";
		return true;
	}

	void WriteSeqKeys();

	// ONE SEQUENCE FRAME, REQUESTED NOW, whatever the phase. Its keys row is
	// written when the shutter opens rather than when the file lands, so the
	// beat on the row is the beat that was running at the moment of capture;
	// a row naming a frame that never wrote simply matches no file when the
	// stitcher globs, which is the harmless direction.
	bool BeginSeqFrame(double Now, bool bForced)
	{
		if (GSeqRequested >= LedgerCrime::kMaxSeqFrames) { return false; }
		const FString Leaf = FString::Printf(TEXT("ue-crimeseq_%03d.png"), GSeqRequested);
		GShotName = FString::Printf(TEXT("seq%03d"), GSeqRequested);
		ShotBegin(AbsProject(*Leaf), Now);
		GSeqInFlight = true;
		GSeqKeys.push_back(LedgerCrime::SeqKeyLine(Utf8(Leaf), GBeat, GBeatSpeaker,
		                                           GBeatLineId, GBeatLineText,
		                                           GBeatLineTextSource, GBeatHeard));
		WriteSeqKeys();
		++GSeqRequested;
		if (bForced) { ++GSeqForced; }
		GLastSeqCaptureTime = Now;
		return true;
	}

	// Pumps a sequence frame already in flight and, when none is, starts one
	// if the interval has passed. A COOLDOWN AGAINST THE LAST CAPTURE rather
	// than an absolute schedule, so a slow attempt cannot cause a burst of
	// catch-up frames afterwards.
	void MaybeCaptureSequence(double Now)
	{
		if (GShotInFlight) { return; }
		if (GSeqInFlight)
		{
			const FVector Loc = (GPawn != nullptr) ? GPawn->GetActorLocation() : FVector::ZeroVector;
			std::string Line;
			if (ShotPump(Now, Loc, kSeqFileCeiling, /*bCountsTowardShotsWrote=*/false, Line))
			{
				GSeqInFlight = false;
			}
			return;
		}
		if (GLastSeqCaptureTime == 0.0) { GLastSeqCaptureTime = Now; return; }
		if ((Now - GLastSeqCaptureTime) < LedgerCrime::kSeqIntervalSeconds) { return; }
		BeginSeqFrame(Now, /*bForced=*/false);
	}

	// A FORCED FRAME AS ITS OWN PHASE, so the cut either side of each deed is
	// not left to a cooldown that might or might not have expired. Returns
	// true while it is still working.
	bool RunForcedSeqPhase(ECrimePhase NextPhase, double Now)
	{
		if (!GSeqInFlight)
		{
			if (!BeginSeqFrame(Now, /*bForced=*/true))
			{
				GPhase = NextPhase; GPhaseStart = Now;
			}
			return true;
		}
		const FVector Loc = (GPawn != nullptr) ? GPawn->GetActorLocation() : FVector::ZeroVector;
		std::string Line;
		if (ShotPump(Now, Loc, kSeqFileCeiling, /*bCountsTowardShotsWrote=*/false, Line))
		{
			GSeqInFlight = false;
			GPhase = NextPhase;
			GPhaseStart = Now;
		}
		return true;
	}

	bool RunShotPhase(const TCHAR* Name, const TCHAR* Leaf, ECrimePhase NextPhase, double Now)
	{
		if (!GShotInFlight)
		{
			GShotName = Name;
			ShotBegin(AbsProject(Leaf), Now);
			GShotInFlight = true;
			return true;
		}
		const FVector Loc = (GPawn != nullptr) ? GPawn->GetActorLocation() : FVector::ZeroVector;
		std::string Line;
		if (ShotPump(Now, Loc, kShotFileCeiling, /*bCountsTowardShotsWrote=*/true, Line))
		{
			GShotLines.push_back(Line);
			++GShotsAttempted;
			GShotInFlight = false;
			GPhase = NextPhase;
			GPhaseStart = Now;
		}
		return true;
	}

	// ---- traces ----------------------------------------------------------
	//
	// THE NAME A TRACE HIT, AND WHAT IT MEANS WHEN THERE IS NONE. An actor
	// this module did not spawn (the pawn, a light, the world) has no piece
	// name, and printing the engine's StaticMeshActor_NNN is better than
	// printing nothing, so the fallback is named rather than blank.
	std::string BlockerName(const AActor* Hit)
	{
		if (Hit == nullptr) { return "none"; }
		const FString Named = LedgerVignetteShot::StreetPieceNameOf(Hit);
		if (!Named.IsEmpty()) { return Utf8(Named); }
		// AN UNNAMED ACTOR SAYS WHAT MESH IT IS (24 September): "unnamed/
		// StaticMeshActor_757" blocked every sight line in a local run and
		// named nothing a person could look for.
		if (const AStaticMeshActor* S = Cast<AStaticMeshActor>(Hit))
		{
			const UStaticMeshComponent* C = S->GetStaticMeshComponent();
			const UStaticMesh* M = C != nullptr ? C->GetStaticMesh() : nullptr;
			if (M != nullptr)
			{
				return "unnamed/" + Utf8(Hit->GetName()) + "/mesh=" + Utf8(M->GetName())
					+ "/scale=" + std::to_string((int)Hit->GetActorScale3D().X)
					+ "/collision=" + std::to_string((int)C->GetCollisionEnabled())
					+ "/owner=" + Utf8(Hit->GetOuter() ? Hit->GetOuter()->GetName() : FString(TEXT("none")));
			}
		}
		return "unnamed/" + Utf8(Hit->GetName());
	}

	// One line trace against the street's own collision. The target is
	// ignored (the question is what is BETWEEN, not whether the target is
	// solid) and so is the looker's own body, which the eye point sits inside
	// by construction.
	bool TraceBlocked(UWorld* World, const FVector& From, const FVector& To,
	                  const AActor* IgnoreA, const AActor* IgnoreB,
	                  std::string& OutBlocker, double& OutLenCm)
	{
		OutBlocker = "none";
		OutLenCm = (double)FVector::Dist(From, To);
		if (World == nullptr) { return false; }
		// DEFAULT CONSTRUCTED AND THEN SET, which is the plainest form of
		// this type there is: a tagged constructor and the SCENE_QUERY_STAT
		// macro are both conveniences whose exact shape is not worth a
		// 25-minute round trip to find out about.
		FCollisionQueryParams Params;
		Params.bTraceComplex = false;
		if (IgnoreA != nullptr) { Params.AddIgnoredActor(IgnoreA); }
		if (IgnoreB != nullptr) { Params.AddIgnoredActor(IgnoreB); }
		FHitResult Hit;
		const bool bHit = World->LineTraceSingleByChannel(Hit, From, To, ECC_Visibility, Params);
		if (!bHit) { return false; }
		OutBlocker = BlockerName(Hit.GetActor());
		OutLenCm = (double)FVector::Dist(From, Hit.ImpactPoint);
		return true;
	}

	// THE GROUND UNDER A POINT, MEASURED, NEVER TYPED. The east footway is
	// cambered (its litter sits at y 0.087 to 0.098 against a nominal ground
	// top of 0.075) and the yard has no ground plane at all until this probe
	// spawns one, so every height in this run comes from a downward trace and
	// the ones that found nothing say so.
	bool GroundYAt(UWorld* World, double StreetX, double StreetZ, double& OutY,
	               std::string& OutOn)
	{
		OutY = 0.0;
		OutOn = "nothing-found";
		if (World == nullptr) { return false; }
		const FVector From = ToUE(LedgerCrime::P3(StreetX, 4.0, StreetZ));
		const FVector To   = ToUE(LedgerCrime::P3(StreetX, -2.0, StreetZ));
		FCollisionQueryParams Params;
		Params.bTraceComplex = false;
		if (GPawn != nullptr) { Params.AddIgnoredActor(GPawn); }
		FHitResult Hit;
		if (!World->LineTraceSingleByChannel(Hit, From, To, ECC_Visibility, Params)) { return false; }
		OutY = (double)Hit.ImpactPoint.Z / 100.0;
		OutOn = BlockerName(Hit.GetActor());
		return true;
	}

	// ---- placing things --------------------------------------------------
	AActor* SpawnBox(UWorld* World, const FString& Name, const LedgerCrime::P3& CentreM,
	                 double SX, double SY, double SZ, const TCHAR* Surface)
	{
		return LedgerVignetteShot::SpawnProbePiece(
			World, Name,
			FVector((float)CentreM.X, (float)CentreM.Y, (float)CentreM.Z),
			FVector((float)SX, (float)SY, (float)SZ),
			TEXT("box"), Surface);
	}

	AActor* SpawnBody(UWorld* World, const FString& Name, double StreetX, double StreetZ,
	                  double GroundY)
	{
		return LedgerVignetteShot::SpawnProbePiece(
			World, Name,
			FVector((float)StreetX, (float)(GroundY + LedgerCrime::kBodyHeightM * 0.5), (float)StreetZ),
			FVector((float)LedgerCrime::kBodyDiameterM, (float)LedgerCrime::kBodyHeightM,
			        (float)LedgerCrime::kBodyDiameterM),
			TEXT("cyl"), TEXT("cloth_dark"));
	}

	// THE LIVE ENCOUNTER'S PEOPLE, 24 September: in play the perceivers stay
	// the probe's own bodies, measured exactly as in the regression, hidden;
	// a MetaHuman stands where each stands and faces where it faces. Lena is
	// the witness at Mickey's, Sam the lad in the yard, Rocco his mate.
	TMap<AActor*, TWeakObjectPtr<AActor>> GVisuals;
	int32 GVisualsPlaced = 0;
	// EACH ONE'S HEAD, 29 September (town list 1): the look on every part of
	// their MetaHuman that plays an idle, body and face alike, by body.
	TMap<AActor*, TArray<TWeakObjectPtr<ULedgerPersonAnim>>> GLooks;
	// EPIC'S OWN IDLE, BODY AND FACE (24 September, MetaHumanPortrait.cpp):
	// the elizabeth idle carried over from an old street figure put the
	// hands through the body; these are made on the cast's own skeletons.
	const TCHAR* kLiveIdles[] = {
		TEXT("/MetaHumanCharacter/Optional/Animation/TemplateAnimations/Technical_Loops/Idle/mhc_mh001_fmn_b_idle.mhc_mh001_fmn_b_idle"),
		TEXT("/MetaHumanCharacter/Optional/Animation/TemplateAnimations/Technical_Loops/Idle/mhc_mh001_fmn_f_idle.mhc_mh001_fmn_f_idle") };

	AActor* GVisualFor(AActor* Body)
	{
		if (Body == nullptr) { return nullptr; }
		TWeakObjectPtr<AActor>* V = GVisuals.Find(Body);
		return (V != nullptr && V->IsValid()) ? V->Get() : Body;
	}

	void SyncVisual(AActor* Body)
	{
		if (Body == nullptr) { return; }
		TWeakObjectPtr<AActor>* V = GVisuals.Find(Body);
		if (V == nullptr || !V->IsValid()) { return; }
		const FBox B = Body->GetComponentsBoundingBox();
		const FVector Feet(B.GetCenter().X, B.GetCenter().Y, B.Min.Z);
		// A MetaHuman faces its actor's +Y; the body's yaw is its gaze.
		(*V)->SetActorLocationAndRotation(Feet, FRotator(0.0f, Body->GetActorRotation().Yaw - 90.0f, 0.0f));
	}

	void DressBody(UWorld* World, AActor* Body, const TCHAR* Who)
	{
		if (GEnc != EEncounter::Live || World == nullptr || Body == nullptr) { return; }
		// THE FACES JAFAR APPROVED, 25 September (the casting page): each
		// character is the candidate he chose, Sheila C1, Ron C1, Darren C5
		// (make_cast_metahumans.py's CANDIDATES). -CastTake=T2 brings back the
		// cast made to the brief for all three, and -CastTake= with nothing
		// after it the first stand-ins. Where a take is not in this copy of the
		// game (the build machine's has no room for the candidates yet), the
		// next one down is used: the approved candidate, then T2, then the
		// stand-in.
		// RON'S FACE, 28 September: Jafar picked P2 on the 26 September weekend
		// page ("This is him"), rebuilt on Epic's Bruce; C1 stays next in line.
		// SHEILA'S FACE, 29 September: Jafar picked S4 on Wednesday's page
		// (finished from the concept portrait's measurements), with the hair it
		// wears; C1 stays next in line.
		const bool bRon = FCString::Strcmp(Who, TEXT("Rocco")) == 0;   // names-gate: allow (the asset MH_RoccoP2)
		const bool bLena = FCString::Strcmp(Who, TEXT("Lena")) == 0;   // names-gate: allow (the asset MH_LenaS4)
		const TCHAR* Approved = FCString::Strcmp(Who, TEXT("Sam")) == 0 ? TEXT("C5") : bRon ? TEXT("P2") : TEXT("S4");   // names-gate: allow (the asset MH_SamC5)
		TArray<FString> Takes = { Approved, TEXT("T2"), TEXT("") };
		if (bRon || bLena) { Takes.Insert(TEXT("C1"), 1); }
		FString Forced;
		if (FParse::Value(FCommandLine::Get(), TEXT("CastTake="), Forced))
		{
			Takes = { Forced, TEXT("") };
		}
		auto ClassFor = [](const FString& Name) {
			return LoadClass<AActor>(nullptr, *FString::Printf(TEXT("/Game/Ledger/MetaHumans/%s/BP_%s.BP_%s_C"), *Name, *Name, *Name)); };
		UClass* Cls = nullptr;
		for (const FString& Take : Takes)
		{
			Cls = ClassFor(FString(TEXT("MH_")) + Who + Take);
			if (Cls != nullptr)
			{
				UE_LOG(LogTemp, Display, TEXT("LedgerCast: %s is MH_%s%s"), Who, Who, *Take);
				break;
			}
		}
		if (Cls == nullptr) { return; }
		FActorSpawnParameters P;
		P.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
		AActor* A = World->SpawnActor<AActor>(Cls, Body->GetActorLocation(), FRotator::ZeroRotator, P);
		if (A == nullptr) { return; }
		A->Tags.Add(TEXT("LedgerCast"));   // the encounter's own cast, for the portrait tool's -PortraitInGame
		// NOBODY WALKS THROUGH THEM (the AI tester, 24 September: its camera
		// ended up inside Lena). The MetaHuman's own meshes collide with
		// nothing, so no sight line in the measured street changes; a capsule
		// of a person's size blocks the player, and only the player.
		TArray<UPrimitiveComponent*> Prims;
		A->GetComponents(Prims);
		for (UPrimitiveComponent* Pc : Prims) { if (Pc != nullptr) { Pc->SetCollisionEnabled(ECollisionEnabled::NoCollision); } }
		if (UCapsuleComponent* Cap = NewObject<UCapsuleComponent>(A, TEXT("LiveBodyBlock")))
		{
			Cap->InitCapsuleSize(30.0f, 88.0f);
			Cap->SetupAttachment(A->GetRootComponent());
			Cap->SetRelativeLocation(FVector(0.0f, 0.0f, 90.0f));
			Cap->SetCollisionEnabled(ECollisionEnabled::QueryAndPhysics);
			Cap->SetCollisionResponseToAllChannels(ECR_Ignore);
			Cap->SetCollisionResponseToChannel(ECC_Pawn, ECR_Block);
			Cap->SetHiddenInGame(true);
			Cap->RegisterComponent();
		}
		int32 PartsAnimated = 0;
		for (const TCHAR* IdlePath : kLiveIdles)
		{
			UAnimSequenceBase* Idle = LoadObject<UAnimSequenceBase>(nullptr, IdlePath);
			if (Idle == nullptr) { continue; }
			TArray<USkeletalMeshComponent*> Parts;
			A->GetComponents(Parts);
			for (USkeletalMeshComponent* C : Parts)
			{
				USkeletalMesh* M = C != nullptr ? C->GetSkeletalMeshAsset() : nullptr;
				if (M == nullptr || M->GetSkeleton() != Idle->GetSkeleton()) { continue; }
				// Not all in step: each starts at its own point in the loop.
				const float Start = FMath::Fmod((float)GVisualsPlaced * 2.3f, FMath::Max(Idle->GetPlayLength(), 1.0f));
				// THE HEAD TURNS TO HIM, 29 September (town list 1): the idle
				// through Unreal's Look At, as the street's people's
				// (PersonAnim.h), on the body and the face alike so the two
				// stay one head; how each looks comes from what they hold about
				// him (RegardTick). The portrait tool's shots never look.
				const bool bLooks = !FParse::Param(FCommandLine::Get(), TEXT("PortraitInGame"));
				C->SetAnimationMode(EAnimationMode::AnimationBlueprint);
				C->SetAnimInstanceClass(ULedgerPersonAnim::StaticClass());
				if (ULedgerPersonAnim* Look = Cast<ULedgerPersonAnim>(C->GetAnimInstance()))
				{
					Look->Setup(Idle, Start, 1.0f, bLooks);
					C->InitAnim(true);
					GLooks.FindOrAdd(Body).Add(Look);
					++PartsAnimated;
					UE_LOG(LogTemp, Display, TEXT("LedgerCast: %s's %s plays the idle and can speak"), Who, *C->GetName());
					continue;
				}
				C->SetAnimationMode(EAnimationMode::AnimationSingleNode);
				C->PlayAnimation(Idle, true);
				C->SetPosition(Start, false);
			}
		}
		UE_LOG(LogTemp, Display, TEXT("LedgerCast: %s has %d part(s) that can speak"), Who, PartsAnimated);
		LedgerJacket::Wear(A, Who);
		LedgerGarments::Wear(A, Who);
		Body->SetActorHiddenInGame(true);
		GVisuals.Add(Body, A);
		++GVisualsPlaced;
		SyncVisual(Body);
	}

	// A LINE ON THE SCREEN for the one playing: what is said, and what to do.
	// THE GAME'S OWN SUBTITLES, 24 September (overnight): these were engine
	// debug messages, which a release build does not draw, so in a shipped
	// game every word said would have vanished (the production pipeline
	// audit). Now a Slate panel of its own over the view, above the say box:
	// the newest line last, at most six, each gone after its seconds. Every
	// line also goes to the log, where the tester can read it.
	struct FSubLine { FString Text; FLinearColor Colour; double Until = 0.0; };
	TArray<FSubLine> GSubs;
	TSharedPtr<SVerticalBox> GSubBox;
	TSharedPtr<SWidget> GSubRoot;
	TWeakObjectPtr<UWorld> GSubWorld;

	void SubsRebuild()
	{
		if (!GSubBox.IsValid()) { return; }
		GSubBox->ClearChildren();
		for (const FSubLine& L : GSubs)
		{
			GSubBox->AddSlot().AutoHeight().Padding(FMargin(0.0f, 2.0f))
			[
				SNew(STextBlock)
				.Text(FText::FromString(L.Text))
				.ColorAndOpacity(FSlateColor(L.Colour))
				.Font(FCoreStyle::GetDefaultFontStyle("Regular", 17))
				.ShadowOffset(FVector2D(1.5f, 1.5f))
				.ShadowColorAndOpacity(FLinearColor(0.0f, 0.0f, 0.0f, 0.9f))
				// A FIXED WRAP, not AutoWrapText: the lines are rebuilt whenever
				// one is added, and auto-wrap waits a frame for its width, so
				// the frame a line was said in showed it running off the edge.
				.WrapTextAt(1060.0f)
			];
		}
	}

	void SubsEnsure()
	{
		if (GEngine == nullptr || GEngine->GameViewport == nullptr) { return; }
		// A NEW WORLD CLEARS THE VIEWPORT'S WIDGETS, so the panel is added
		// again whenever the game world is not the one it was added under.
		UWorld* W = GEngine->GameViewport->GetWorld();
		if (GSubRoot.IsValid() && GSubWorld.Get() == W) { return; }
		// AT MOST 1100 WIDE, NEVER WIDER THAN THE WINDOW: a fixed 1100 ran the
		// lines off the edge of a 960-wide window instead of wrapping them.
		SAssignNew(GSubRoot, SBox)
			.HAlign(HAlign_Center).VAlign(VAlign_Bottom).Padding(FMargin(40.0f, 0.0f, 40.0f, 150.0f))
			[
				SNew(SBox).MaxDesiredWidth(1100.0f)
				[
					SAssignNew(GSubBox, SVerticalBox)
				]
			];
		GEngine->GameViewport->AddViewportWidgetContent(GSubRoot.ToSharedRef(), 50);
		GSubWorld = W;
		SubsRebuild();
	}

	void SubsTick()
	{
		const double Now = NowS();
		const int32 Before = GSubs.Num();
		GSubs.RemoveAll([Now](const FSubLine& L) { return L.Until < Now; });
		if (GSubs.Num() != Before) { SubsRebuild(); }
	}

	// OFF WHILE THE LOOK IS FILMED: the yellow instructions to the player are
	// not part of the street (the second review: the walk-to-the-window prompt
	// sat on every frame).
	bool GSayInstructions = true;

	void Say(const FString& Line, float Seconds = 12.0f, FColor Colour = FColor::White)
	{
		UE_LOG(LogTemp, Display, TEXT("LedgerSay: %s"), *Line);
		if (!GSayInstructions && Colour == FColor::Yellow) { return; }
		SubsEnsure();
		FSubLine L;
		L.Text = Line;
		L.Colour = FLinearColor(Colour);
		L.Until = NowS() + Seconds;
		GSubs.Add(L);
		while (GSubs.Num() > 6) { GSubs.RemoveAt(0); }
		SubsRebuild();
	}

	// A BODY MOVES BY ITS OWN TRANSFORM, not by a second spawn: W1 stands at
	// P1 for crime A and at P2 for crime B, and spawning her twice would put
	// two shopkeepers in the frame and two entries in the probe map.
	void MoveBody(UWorld* World, AActor* Body, double StreetX, double StreetZ)
	{
		if (Body == nullptr) { return; }
		double GroundY = 0.0;
		std::string On;
		if (!GroundYAt(World, StreetX, StreetZ, GroundY, On)) { GroundY = 0.1; }
		Body->SetActorLocation(ToUE(LedgerCrime::P3(
			StreetX, GroundY + LedgerCrime::kBodyHeightM * 0.5, StreetZ)));
		SyncVisual(Body);
	}

	void FaceBody(AActor* Body, const LedgerCrime::P3& Toward)
	{
		if (Body == nullptr) { return; }
		const LedgerCrime::P3 At = ToStreet(Body->GetActorLocation());
		const double Yaw = LedgerCrime::YawToFace(At, Toward);
		Body->SetActorRotation(FRotator(0.0f, (float)Yaw, 0.0f));
		SyncVisual(Body);
	}

	void TeleportPawn(UWorld* World, double StreetX, double StreetZ, double YawDeg)
	{
		if (GPawn == nullptr) { return; }
		double GroundY = 0.0;
		std::string On;
		if (!GroundYAt(World, StreetX, StreetZ, GroundY, On)) { GroundY = 0.1; }
		// A GENEROUS NAMED CLEARANCE ABOVE THE MEASURED GROUND rather than a
		// second copy of the capsule's half height: gravity settles the rest
		// on the first tick, exactly as BuildInteractiveStreet's own player
		// start does, and a spawn that starts too low would not correct
		// itself the same way.
		const double kClearAboveGroundM = 1.1;
		GPawn->TeleportTo(ToUE(LedgerCrime::P3(StreetX, GroundY + kClearAboveGroundM, StreetZ)),
		                  FRotator(0.0f, (float)YawDeg, 0.0f), false, true);
	}

	// ---- the vantage, read off the engine --------------------------------
	//
	// EVERY NUMBER HERE IS A MEASUREMENT OF THE RUNNING WORLD: the witness's
	// own transform, the pawn's own bounds, two line traces. Nothing is taken
	// from the ruling's arithmetic, which is printed separately as the
	// prediction this run is read against.
	LedgerCrime::Reading MeasureVantage(UWorld* World, const std::string& WitnessId,
	                                    const std::string& EventId, AActor* Body,
	                                    AActor* Glass, double SecondsWatching)
	{
		LedgerCrime::Reading R;
		R.WitnessId = WitnessId;
		R.EventId = EventId;
		R.SecondsWatching = SecondsWatching;
		if (Body == nullptr || GPawn == nullptr) { R.FiledReason = "nothing-measured"; return R; }

		// The body's own bounds give its feet; the eye sits 1.6 m above them.
		const FBox BodyBox = Body->GetComponentsBoundingBox();
		const LedgerCrime::P3 Feet = ToStreet(FVector(
			BodyBox.GetCenter().X, BodyBox.GetCenter().Y, BodyBox.Min.Z));
		R.WitnessAt = Feet;
		R.EyeAt = LedgerCrime::P3(Feet.X, Feet.Y + LedgerCrime::kEyeHeightM, Feet.Z);
		R.WitnessYawDeg = (double)Body->GetActorRotation().Yaw;

		// The actor's head, from the pawn's OWN bounds rather than a second
		// copy of ALedgerCharacter's capsule half height.
		const FBox PawnBox = GPawn->GetComponentsBoundingBox();
		const FVector HeadUE(PawnBox.GetCenter().X, PawnBox.GetCenter().Y, PawnBox.Max.Z - 10.0f);
		R.ActorHeadAt = ToStreet(HeadUE);
		R.ActorYawDeg = (double)GPawn->GetActorRotation().Yaw;

		// The window centre, read off the actor the street actually spawned,
		// after scale and rotation, never the file's numbers a second time.
		const FVector EyeUE = ToUE(R.EyeAt);
		R.ActorMetres = LedgerCrime::Metres(R.EyeAt, R.ActorHeadAt);
		R.ActorOffAxisDeg = LedgerCrime::OffAxisDeg(R.EyeAt, R.WitnessYawDeg, R.ActorHeadAt);
		R.bActorOccluded = TraceBlocked(World, EyeUE, HeadUE, Body, GPawn,
		                                R.ActorBlocker, R.ActorTraceLenCm);

		// NO WINDOW, NO VICTIM HALF. The per-tick watching accumulator calls
		// this for the actor half alone, and a trace to the world origin sixty
		// times a second measures nothing while costing a query each time.
		if (Glass == nullptr)
		{
			R.VictimBlocker = "no-window-asked-for";
			return R;
		}
		// With non-colliding parts (23 September): when the street's own
		// walls are on, the scene file's pane never collides, and the
		// default bounds would put the victim at the origin.
		const FVector VictimUE = Glass->GetComponentsBoundingBox(true).GetCenter();
		R.VictimAt = ToStreet(VictimUE);
		R.VictimMetres = LedgerCrime::Metres(R.EyeAt, R.VictimAt);
		R.VictimOffAxisDeg = LedgerCrime::OffAxisDeg(R.EyeAt, R.WitnessYawDeg, R.VictimAt);
		R.bVictimOccluded = TraceBlocked(World, EyeUE, VictimUE, Body, Glass,
		                                 R.VictimBlocker, R.VictimTraceLenCm);
		return R;
	}

	// THE ACCUMULATOR. Called every tick while a crime's watching window is
	// open: a witness accrues this frame's delta only while her sightline to
	// the actor holds right now, which is the definition Perception.cs 65
	// carries and the one Witnesses.cs says belongs in the field.
	void AccrueWatching(UWorld* World, double Delta)
	{
		if (GWatchSlot < 0 || GWatchSlot > 1) { return; }
		AActor* Bodies[2] = { GW1Body, GN2Body };
		++GWatchTicks[GWatchSlot];
		for (int I = 0; I < 2; ++I)
		{
			if (Bodies[I] == nullptr || GPawn == nullptr) { continue; }
			const LedgerCrime::Reading R = MeasureVantage(
				World, I == 0 ? "w1" : "n2", "watch", Bodies[I], nullptr, 0.0);
			const bool bSees = Perception::InSight(R.ActorMetres, R.ActorOffAxisDeg,
			                                       LedgerCrime::kLightLevel, R.bActorOccluded, 1.4);
			if (bSees) { GSeconds[GWatchSlot][I] += Delta; }
		}
		// AND THE CONSTABLE, by exactly the same test.
		if (GC1Body != nullptr && GPawn != nullptr)
		{
			const LedgerCrime::Reading C = MeasureVantage(World, "c1", "watch", GC1Body, nullptr, 0.0);
			const bool bSees = Perception::InSight(C.ActorMetres, C.ActorOffAxisDeg,
			                                       LedgerCrime::kLightLevel, C.bActorOccluded, 1.4);
			if (bSees) { GC1Seconds[GWatchSlot] += Delta; }
		}
	}

	// Declared here and defined with the other writers below, the same shape
	// WriteSeqKeys already uses in this file: the act phase needs to leave a
	// breadcrumb and the writers live at the bottom.
	// SAVE, RESTART, RELOAD - INSIDE THE PACKAGED BUILD.
	//
	// WHY IT IS HERE AND NOT IN A TEST. The golden table already proves the
	// two engines agree about a save, and a test bench can prove a round
	// trip all day. What it cannot prove is that the rumour THIS RUN'S
	// CRIME PRODUCED, carried by the mill that actually ticked, written by
	// the engine the game ships in, survives the world being rebuilt. That
	// is the claim the list makes and it can only be made here.
	//
	// THE RESTART IS HONEST ABOUT WHAT A RESTART IS: the world is built
	// again from the AUTHORING - the same two people, the same tie, no play
	// in them - and the save is laid over it. Restoring into the mill that
	// already holds the rumours would prove nothing whatever, and is the
	// easy mistake to make here because that mill is right there.
	//
	// THE CONTROL IS THE LAD IN THE YARD. He heard the rumour from the
	// shopkeeper, so after a restart he must still have it; what he must
	// NOT have is the shopkeeper's OWN first-hand observation. A restore
	// that handed every agent the same records would pass every count and
	// fail that. Both are printed.
	struct RestartReading
	{
		bool bRan;
		int  SavedBytes;
		int  W1Before, W1After, N2Before, N2After;      // rumours
		int  W1MemBefore, W1MemAfter, N2MemBefore, N2MemAfter;  // memory events
		double W1ConfBefore, W1ConfAfter;
		int  W1HopsAfter, N2HopsAfter;
		bool bMemoryTextSame;
		// THE PAIR ACROSS THE RESTART, 22 September: rumours about the crime
		// somebody saw and about the one nobody could, counted over the mill
		// that ticked and again over the one rebuilt from the authoring.
		int  AboutABefore, AboutAAfter, AboutBBefore, AboutBAfter;
		// THE THIRD RESIDENT'S OWN RECORD, found missing by the independent
		// check: his rumour was counted in the pair but his MEMORY was never
		// saved or reloaded, and nothing said he came back two retellings out.
		bool bR3;
		int  R3Before, R3After, R3MemBefore, R3MemAfter, R3HopsAfter;
		RestartReading()
			: bRan(false), SavedBytes(0), W1Before(0), W1After(0), N2Before(0), N2After(0),
			  W1MemBefore(0), W1MemAfter(0), N2MemBefore(0), N2MemAfter(0),
			  W1ConfBefore(0.0), W1ConfAfter(0.0), W1HopsAfter(0), N2HopsAfter(0),
			  bMemoryTextSame(false),
			  AboutABefore(0), AboutAAfter(0), AboutBBefore(0), AboutBAfter(0),
			  bR3(false), R3Before(0), R3After(0), R3MemBefore(0), R3MemAfter(0), R3HopsAfter(0) {}
	};

	static double BestConfidence(const GossiperPtr& G)
	{
		double Best = 0.0;
		if (!G) { return Best; }
		for (std::vector<RumorPtr>::size_type I = 0; I < G->Rumors.size(); ++I)
		{
			if (G->Rumors[I] && G->Rumors[I]->Confidence > Best) { Best = G->Rumors[I]->Confidence; }
		}
		return Best;
	}

	static int BestHops(const GossiperPtr& G)
	{
		double Best = -1.0;
		int Hops = 0;
		if (!G) { return Hops; }
		for (std::vector<RumorPtr>::size_type I = 0; I < G->Rumors.size(); ++I)
		{
			if (G->Rumors[I] && G->Rumors[I]->Confidence > Best)
			{
				Best = G->Rumors[I]->Confidence;
				Hops = G->Rumors[I]->Hops;
			}
		}
		return Hops;
	}

	void RunRestartRoundTrip(RestartReading& Out)
	{
		if (!GMill || !GW1 || !GN2) { return; }
		Out.W1Before = (int)GW1->Rumors.size();
		Out.N2Before = (int)GN2->Rumors.size();
		Out.W1MemBefore = GW1->Memory ? (int)GW1->Memory->Events.size() : 0;
		Out.N2MemBefore = GN2->Memory ? (int)GN2->Memory->Events.size() : 0;
		Out.W1ConfBefore = BestConfidence(GW1);
		LedgerCrime::CountAboutCrimes(GMill->Agents(), Out.AboutABefore, Out.AboutBBefore);

		// THE SAVE. The mill goes out as the JSON the C# codec writes for it;
		// the memories go out as the markdown they already go out as, which
		// is their save format and always was.
		const std::string MillJson = Save::CaptureMillAgents(*GMill);
		const std::string W1Md = GW1->Memory ? GW1->Memory->ToMarkdown() : std::string();
		const std::string N2Md = GN2->Memory ? GN2->Memory->ToMarkdown() : std::string();
		const std::string R3Md = (GR3 && GR3->Memory) ? GR3->Memory->ToMarkdown() : std::string();
		if (GR3)
		{
			Out.bR3 = true;
			Out.R3Before = (int)GR3->Rumors.size();
			Out.R3MemBefore = GR3->Memory ? (int)GR3->Memory->Events.size() : 0;
		}
		Out.SavedBytes = (int)MillJson.size();
		SaveBoth(TEXT("ue-crime-save-agents.json"), Un(MillJson));

		// THE RESTART: the same authoring, none of the play.
		std::shared_ptr<SocialGraph> Graph = std::make_shared<SocialGraph>();
		Graph->Link("w1", "n2", LedgerCrime::kTie);
		GossipMill Fresh(Graph);
		GossiperPtr F1 = std::make_shared<Gossiper>("w1", "the shopkeeper",
			std::make_shared<MemoryStore>("w1"), std::shared_ptr<KnowledgeBase>(), "day");
		GossiperPtr F2 = std::make_shared<Gossiper>("n2", "the lad in the yard",
			std::make_shared<MemoryStore>("n2"), std::shared_ptr<KnowledgeBase>(), "day");
		Fresh.Add(F1);
		Fresh.Add(F2);
		// AND THE THIRD RESIDENT, because he is authoring too: tied to the
		// lad only, as at the start. Without him the rebuilt world has nobody
		// to lay his saved record on, RestoreMillAgents skips it, and the
		// pair's count of rumours about A falls by one across the restart for
		// a reason that has nothing to do with the save.
		GossiperPtr F3;
		if (GR3)
		{
			Graph->Link("n2", LedgerCrime::kR3Id, LedgerCrime::kR3Tie);
			F3 = std::make_shared<Gossiper>(LedgerCrime::kR3Id, LedgerCrime::kR3Name,
				std::make_shared<MemoryStore>(LedgerCrime::kR3Id),
				std::shared_ptr<KnowledgeBase>(), "day");
			Fresh.Add(F3);
		}

		// THE RELOAD.
		Save::RestoreMillAgents(MillJson, Fresh);
		if (F1->Memory) { F1->Memory->LoadFrom(W1Md); }
		if (F2->Memory) { F2->Memory->LoadFrom(N2Md); }
		if (F3 && F3->Memory) { F3->Memory->LoadFrom(R3Md); }
		if (F3)
		{
			Out.R3After = (int)F3->Rumors.size();
			Out.R3MemAfter = F3->Memory ? (int)F3->Memory->Events.size() : 0;
			Out.R3HopsAfter = BestHops(F3);
		}

		Out.W1After = (int)Fresh.Get("w1")->Rumors.size();
		Out.N2After = (int)Fresh.Get("n2")->Rumors.size();
		Out.W1MemAfter = F1->Memory ? (int)F1->Memory->Events.size() : 0;
		Out.N2MemAfter = F2->Memory ? (int)F2->Memory->Events.size() : 0;
		Out.W1ConfAfter = BestConfidence(Fresh.Get("w1"));
		Out.W1HopsAfter = BestHops(Fresh.Get("w1"));
		Out.N2HopsAfter = BestHops(Fresh.Get("n2"));
		// AND THE PAIR, over the REBUILT mill: the witnessed crime must come
		// back, and the one nobody saw must still have nothing about it. A
		// restore that invented a record, or dropped one, shows here.
		LedgerCrime::CountAboutCrimes(Fresh.Agents(), Out.AboutAAfter, Out.AboutBAfter);
		// THE MARKDOWN IS STABLE ACROSS THE TRIP, which is the memory half's
		// own version of the same question and is already a golden row.
		Out.bMemoryTextSame = F1->Memory && (F1->Memory->ToMarkdown() == W1Md);
		Out.bRan = true;
	}

	void WriteBreadcrumb(const TCHAR* Phase);

	// ---- the act, by input -----------------------------------------------
	//
	// THE PRESS GOES THROUGH THE PLAYER CONTROLLER, NOT ROUND IT. This is the
	// same call the engine makes when Slate hands it a keyboard event, so the
	// binding that fires is the binding a human's E fires, on the same pawn,
	// through the same input component. Nothing here reaches into
	// ALedgerCharacter to set a flag: if the binding is wrong, or the pawn is
	// not the player's, or input is not being processed at all, this returns
	// nothing and the run says so instead of committing a deed anyway.
	//
	// PRESSED THEN RELEASED, both sent. A press with no release leaves the key
	// latched down in the input stack, which is a state no human ever leaves
	// behind and which would quietly change what a later frame sees.
	// WHAT IT RETURNS IS WHERE THE PRESS GOT TO. It used to return true the
	// moment a player controller pointer was non-null, which made
	// keyRouted=yes mean "there is a controller" while reading as "the press
	// entered the input system": a press that never reaches UPlayerInput
	// then points the reader at the character's binding, one layer too far
	// down. The engine's own InputKey return value is not the answer either -
	// for a project with no action mappings it returns false on a perfectly
	// successful press - so what is reported is the last thing this code can
	// honestly know, which is that a UPlayerInput existed to receive it.
	const TCHAR* PressKey(UWorld* World, const FKey& Key)
	{
		APlayerController* PC = (World != nullptr) ? World->GetFirstPlayerController() : nullptr;
		if (PC == nullptr) { return TEXT("no-player-controller"); }
		if (PC->PlayerInput == nullptr) { return TEXT("no-player-input"); }
		const FInputDeviceId Device = IPlatformInputDeviceMapper::Get().GetDefaultInputDevice();
		const uint64 Stamp = FPlatformTime::Cycles64();
		FInputKeyEventArgs Pressed(nullptr, Device, Key, IE_Pressed, Stamp);
		PC->InputKey(Pressed);
		// RELEASED TOO, always. A press with no release leaves the key latched
		// in the input stack, a state no human leaves behind.
		FInputKeyEventArgs Released(nullptr, Device, Key, IE_Released, Stamp);
		PC->InputKey(Released);
		return TEXT("player-input");
	}

	const TCHAR* PressActKey(UWorld* World) { return PressKey(World, EKeys::E); }

	int32 TakeActRequests(int Index)
	{
		// THE SLICE'S OWN CHARACTER FIRST (24 September): the encounter's
		// crime is committed by the player character the slice ships with.
		if (ALedgerSliceCharacter* Slice = Cast<ALedgerSliceCharacter>(GPawn))
		{
			GActPawnClass[Index] = TEXT("LedgerSliceCharacter");
			return Slice->ConsumeActRequests();
		}
		ALedgerCharacter* Body = Cast<ALedgerCharacter>(GPawn);
		if (Body == nullptr)
		{
			GActPawnClass[Index] = (GPawn != nullptr) ? TEXT("not-a-LedgerCharacter") : TEXT("no-pawn");
			return 0;
		}
		GActPawnClass[Index] = TEXT("LedgerCharacter");
		return Body->ConsumeActRequests();
	}

	// WAIT, COMMIT, OR GIVE UP, and the choice belongs to LedgerCrime's own
	// gate so the container binary runs it before any dispatch. There is no
	// fourth branch in which the deed happens without a press.
	// THE VERDICT ROUTES THE PHASE, and that is the whole of the gate. It used
	// to route to the commit phase either way and let a second `if` inside
	// that phase decide whether to go through with it - one idea with two
	// implementations, the second of which lives in this file, which no test
	// in the repository compiles. Deleting that second `if` would have
	// restored the scripted crime with every check still green, which an
	// outside reader demonstrated. There is one decision now, it is
	// DecideAct, it lives in the header the container binary runs, and a
	// give-up never reaches the commit phase at all.
	//
	// STALE PRESSES ARE DROPPED ON ENTRY, AND COUNTED. ConsumeActRequests
	// clears the character's counter, and nothing else calls it, so a press
	// that arrived during any earlier phase - or one this phase gave up on -
	// sat in that counter waiting to be credited to the NEXT crime, on its
	// first tick, before that crime's own press could possibly have been
	// processed. The verdict would have read identically to a run where the
	// press genuinely worked. Whatever is in the counter when this phase
	// opens belongs to no crime, so it is discarded and the count is printed.
	bool RunAwaitActPhase(UWorld* World, int Index, ECrimePhase CommitPhase,
	                      ECrimePhase SkipPhase, double Now)
	{
		if (GActPressesSent[Index] == 0 && GActStaleDropped[Index] == 0)
		{
			GActStaleDropped[Index] = TakeActRequests(Index);
			GActPressLanded[Index] = PressActKey(World);
			// COUNTED ONLY WHEN IT WENT SOMEWHERE. pressesSent=1 beside a
			// press that was never sent is the same lie one layer along.
			if (FCString::Strcmp(GActPressLanded[Index], TEXT("player-input")) == 0)
			{
				++GActPressesSent[Index];
			}
		}
		GActRequestsSeen[Index] += TakeActRequests(Index);
		const LedgerCrime::ActVerdict V = LedgerCrime::DecideAct(
			GActRequestsSeen[Index], Now - GPhaseStart, LedgerCrime::kActCeilingSeconds);
		if (V == LedgerCrime::ActVerdict::Wait) { return true; }
		if (V == LedgerCrime::ActVerdict::GiveUp)
		{
			GActGaveUp[Index] = true;
			GWatchSlot = -1;
			WriteBreadcrumb(Index == 0 ? TEXT("act-a-never-arrived") : TEXT("act-b-never-arrived"));
			GPhase = SkipPhase;
			GPhaseStart = Now;
			return true;
		}
		GActAttempted[Index] = true;
		GPhase = CommitPhase;
		GPhaseStart = Now;
		return true;
	}

	// ---- the deed --------------------------------------------------------
	// What the smash of the first window laid down (shards, the brick), so
	// the glazier's mend can clear it (WindowLook).
	TArray<TWeakObjectPtr<AActor> > GWindowDebris;

	void CommitDeed(UWorld* World, int Index)
	{
		LedgerCrime::CrimeReading& C = GCrime[Index];
		C.Id = (Index == 0) ? "A" : "B";
		C.PieceName = Index == 0 ? Utf8(FString(bRitasWindow ? kGlassR : kGlassA)) : Utf8(FString(kGlassB));
		if (GPawn != nullptr)
		{
			C.ActorAt = ToStreet(GPawn->GetActorLocation());
			C.ActorYawDeg = (double)GPawn->GetActorRotation().Yaw;
		}
		AActor* Glass = GGlass[Index];
		if (Glass == nullptr)
		{
			C.bPieceFound = false;
			C.WhyNot = "piece-not-in-the-street-BuildScene-spawned";
			return;
		}
		C.bPieceFound = true;
		// READ BEFORE, ACT, READ AFTER. A hide that did not take and a hide
		// that was never needed are different facts, and only the pair can
		// tell them apart.
		C.bHiddenBefore = Glass->IsHidden();
		Glass->SetActorHiddenInGame(true);
		Glass->SetActorEnableCollision(false);
		C.bHiddenAfter = Glass->IsHidden();
		C.bCollisionAfter = Glass->GetActorEnableCollision();
		// AND THE PANE THE PLAYER ACTUALLY SEES, when the Blender street is
		// in play: its glass is one mesh per bay and floor, and the one that
		// meets this pane goes too, or the window the crime broke stays whole.
		// The pane's bounds WITH its non-colliding parts: its collision went
		// off two lines up, and the default bounds would be empty.
		C.StreetPanes = LedgerVignetteShot::HideStreetGlassNear(Glass->GetComponentsBoundingBox(true));
		// AND WHAT A SMASHED WINDOW LEAVES: glass still in the frame, glass
		// over the pavement (production/research/broken-window-look).
		UE_LOG(LogTemp, Log, TEXT("LedgerCrime smashed window %s: %d street pieces shown"),
		       Index == 0 ? (bRitasWindow ? TEXT("r") : TEXT("a")) : TEXT("b"),
		       LedgerVignetteShot::RevealStreetMeshes(Index == 0 ? (bRitasWindow ? "crime_r" : "crime_a") : "crime_b"));

		// The glass's own bounds give the window foot; the shards are laid on
		// the footway in front of it and each one sits on the ground a
		// downward trace found, never on a typed height.
		// WITH NON-COLLIDING PARTS, 23 September: the pane's collision is off
		// by now, and the engine's default bounds leave out components that
		// do not collide, so this box was empty and its centre the origin.
		const FBox GlassBox = Glass->GetComponentsBoundingBox(true);
		const LedgerCrime::P3 Centre = ToStreet(GlassBox.GetCenter());
		for (int I = 0; I < LedgerCrime::ShardOffsetCount(); ++I)
		{
			double DX = 0.0, DZ = 0.0;
			LedgerCrime::ShardOffset(I, DX, DZ);
			const double SX = Centre.X + DX, SZ = Centre.Z + DZ;
			double GroundY = 0.0;
			std::string On;
			if (!GroundYAt(World, SX, SZ, GroundY, On)) { continue; }
			const FString Name = FString::Printf(TEXT("probe_shard_%s%d"),
				Index == 0 ? TEXT("a") : TEXT("b"), I);
			if (AActor* Shard = SpawnBox(World, Name,
			             LedgerCrime::P3(SX, GroundY + LedgerCrime::kShardSY * 0.5, SZ),
			             LedgerCrime::kShardSX, LedgerCrime::kShardSY, LedgerCrime::kShardSZ,
			             TEXT("glass")))
			{
				if (Index == 0) { GWindowDebris.Add(Shard); }
				++C.Shards;
				++GShardsSpawned;
			}
		}
		{
			const double BX = Centre.X;
			const double BZ = LedgerCrime::kBrickInsideZ;
			double GroundY = 0.0;
			std::string On;
			if (GroundYAt(World, BX, BZ, GroundY, On))
			{
				const FString Name = FString::Printf(TEXT("probe_brick_%s"),
					Index == 0 ? TEXT("a") : TEXT("b"));
				if (AActor* Brick = SpawnBox(World, Name,
				             LedgerCrime::P3(BX, GroundY + LedgerCrime::kBrickSY * 0.5, BZ),
				             LedgerCrime::kBrickSX, LedgerCrime::kBrickSY, LedgerCrime::kBrickSZ,
				             TEXT("brick_grey")))
				{
					if (Index == 0) { GWindowDebris.Add(Brick); }
					++C.Bricks;
					++GBricksSpawned;
				}
			}
			else
			{
				C.WhyNot = "no-ground-under-the-brick-point";
			}
		}
	}

	// ---- the bank --------------------------------------------------------
	bool LoadBank()
	{
		TArray<FString> Candidates;
		Candidates.Add(FPaths::Combine(FPaths::ProjectDir(), kBankLeaf));
		Candidates.Add(FPaths::Combine(FPaths::ProjectContentDir(), kBankLeaf));
		Candidates.Add(FPaths::Combine(FPaths::LaunchDir(), kBankLeaf));
		Candidates.Add(FPaths::Combine(FPaths::GetPath(FPlatformProcess::ExecutablePath()), kBankLeaf));
		Candidates.Add(FPaths::Combine(FPaths::ProjectDir(), TEXT(".."), kBankRepoPath));
		// The game's own staged copy (tools/ue/stage_game_data.py), last.
		Candidates.Add(FPaths::Combine(FPaths::ProjectContentDir(), TEXT("LedgerData"), kBankRepoPath));
		for (const FString& C : Candidates)
		{
			const FString Full = FPaths::ConvertRelativePathToFull(C);
			GBankTried.push_back(Utf8(Full.Replace(TEXT(" "), TEXT("~"))));
			if (!FPaths::FileExists(C)) { continue; }
			FString Contents;
			if (!FFileHelper::LoadFileToString(Contents, *C)) { continue; }
			GBankText = Utf8(Contents);
			GOverheard.BankPath = Utf8(Full.Replace(TEXT(" "), TEXT("~")));
			GOverheard.bBankRead = true;
			return true;
		}
		GOverheard.BankPath = "not-found";
		GOverheard.WhyNot = "bank-not-found-beside-the-binary-or-the-project";
		return false;
	}

	// ---- the mill --------------------------------------------------------
	struct TogetherByDistance
	{
		double PairMetres(const std::string& A, const std::string& B) const
		{
			AActor* PA = (A == "w1" || A == GIdW1) ? GW1Body : ((A == "n2" || A == GIdN2) ? GN2Body
			           : ((A == LedgerCrime::kR3Id || A == GIdR3) ? GR3Body : nullptr));
			AActor* PB = (B == "w1" || B == GIdW1) ? GW1Body : ((B == "n2" || B == GIdN2) ? GN2Body
			           : ((B == LedgerCrime::kR3Id || B == GIdR3) ? GR3Body : nullptr));
			if (PA == nullptr || PB == nullptr) { return -1.0; }
			return (double)FVector::Dist(PA->GetActorLocation(), PB->GetActorLocation()) / 100.0;
		}

		bool operator()(const std::string& A, const std::string& B) const
		{
			const double M = PairMetres(A, B);
			return M >= 0.0 && M <= LedgerCrime::kTalkRangeM;
		}
	};

	double PairMetresNow(const std::string& A, const std::string& B)
	{
		TogetherByDistance T;
		return T.PairMetres(A, B);
	}

	void RunGossipRound(int Index, LedgerCrime::RoundReading& Out)
	{
		Out.Round = Index;
		Out.SpeakerId = "w1";
		Out.ListenerId = "n2";
		Out.PairMetres = PairMetresNow("w1", "n2");
		Out.bTogether = Out.PairMetres >= 0.0 && Out.PairMetres <= LedgerCrime::kTalkRangeM;
		Out.Tie = GMill ? GMill->Tie("w1", "n2") : 0.0;
		Out.HopDecay = GMill ? GMill->HopDecay : 0.0;
		Out.MinShare = GMill ? GMill->MinConfidenceToShare : 0.0;
		if (GW1)
		{
			Out.RumoursHeld = (int)GW1->Rumors.size();
			// THE STRONGEST TELLING THE SPEAKER HOLDS AS THE ROUND OPENS,
			// which is the number Tick multiplies by tie and hop decay.
			for (std::vector<RumorPtr>::size_type I = 0; I < GW1->Rumors.size(); ++I)
			{
				if (GW1->Rumors[I]->Confidence > Out.ConfidenceIn)
				{
					Out.ConfidenceIn = GW1->Rumors[I]->Confidence;
				}
			}
		}
		if (!GMill) { Out.bRan = false; return; }
		const std::vector<GossipEvent> Events =
			GMill->Tick(GNow, GossipMill::TogetherFn(TogetherByDistance()));
		for (std::vector<GossipEvent>::size_type I = 0; I < Events.size(); ++I)
		{
			if (Events[I].FromId != "w1" || Events[I].ToId != "n2") { continue; }
			++Out.Passed;
			if (Events[I].RumorRef)
			{
				Out.ConfidencePassed = Events[I].RumorRef->Confidence;
				Out.Hops = Events[I].RumorRef->Hops;
				// WHAT THE OVERHEARD BEAT WILL BE COMPOSED FROM. Last one
				// wins, which is the same rumour every time here: one topic,
				// one pair, one hop per round.
				GCarried = Events[I].RumorRef;
			}
			Out.bContradiction = Events[I].Contradiction;
			Out.bExposure = Events[I].Exposure;
		}
		// READ BACK OFF THE LISTENER'S OWN MEMORY, never recomputed from the
		// formula: the number that matters is the one that landed in the file
		// this run commits.
		if (Out.Passed > 0 && GN2 && GN2->Memory && !GN2->Memory->Events.empty())
		{
			Out.HeardImportance = GN2->Memory->Events[GN2->Memory->Events.size() - 1].Importance;
		}
		Out.bRan = true;
	}

	// THE SECOND RETELLING: the lad to his mate, a few days later. The same
	// shape as RunGossipRound and deliberately NOT that function: rounds 1
	// and 2 are the rule-5b pair the verdict judges and the overheard beat
	// composes from, and neither may be touched by a third round. This one
	// never sets GCarried.
	void RunRound3(LedgerCrime::RoundReading& Out)
	{
		Out.Round = 3;
		Out.SpeakerId = "n2";
		Out.ListenerId = LedgerCrime::kR3Id;
		Out.PairMetres = PairMetresNow("n2", LedgerCrime::kR3Id);
		Out.bTogether = Out.PairMetres >= 0.0 && Out.PairMetres <= LedgerCrime::kTalkRangeM;
		Out.Tie = GMill ? GMill->Tie("n2", LedgerCrime::kR3Id) : 0.0;
		Out.HopDecay = GMill ? GMill->HopDecay : 0.0;
		Out.MinShare = GMill ? GMill->MinConfidenceToShare : 0.0;
		if (GN2)
		{
			Out.RumoursHeld = (int)GN2->Rumors.size();
			// CRIME A ONLY, after the independent check: the strongest telling
			// of ANY story would describe a different rumour the day the lad
			// carries two.
			for (std::vector<RumorPtr>::size_type I = 0; I < GN2->Rumors.size(); ++I)
			{
				if (LedgerCrime::IsAboutCrimeA(GN2->Rumors[I])
				    && GN2->Rumors[I]->Confidence > Out.ConfidenceIn)
				{
					Out.ConfidenceIn = GN2->Rumors[I]->Confidence;
				}
			}
		}
		if (!GMill) { Out.bRan = false; return; }
		const std::vector<GossipEvent> Events =
			GMill->Tick(GNow, GossipMill::TogetherFn(TogetherByDistance()));
		for (std::vector<GossipEvent>::size_type I = 0; I < Events.size(); ++I)
		{
			if (Events[I].FromId != "n2" || Events[I].ToId != LedgerCrime::kR3Id) { continue; }
			if (!LedgerCrime::IsAboutCrimeA(Events[I].RumorRef)) { continue; }
			++Out.Passed;
			if (Events[I].RumorRef)
			{
				Out.ConfidencePassed = Events[I].RumorRef->Confidence;
				Out.Hops = Events[I].RumorRef->Hops;
			}
			Out.bContradiction = Events[I].Contradiction;
			Out.bExposure = Events[I].Exposure;
		}
		if (Out.Passed > 0 && GR3 && GR3->Memory && !GR3->Memory->Events.empty())
		{
			Out.HeardImportance = GR3->Memory->Events[GR3->Memory->Events.size() - 1].Importance;
		}
		Out.bRan = true;
	}

	// ---- the files this run commits --------------------------------------
	void WriteSeqKeys()
	{
		TArray<FString> Out;
		Out.Add(FString::Printf(TEXT("# UE crime sequence keys %s @%lld"),
		                        *CrimeSha(), (long long)FDateTime::UtcNow().ToUnixTimestamp()));
		Out.Add(TEXT("# One line per sequence frame. tools/clip-from-frames.py --frame-keys reads"));
		Out.Add(TEXT("#   this and burns the bank's text for lineId on frames whose heard is yes."));
		for (std::vector<std::string>::size_type I = 0; I < GSeqKeys.size(); ++I)
		{
			Out.Add(Un(GSeqKeys[I]));
		}
		SaveBoth(TEXT("ue-crimeseq-keys.txt"), FString::Join(Out, TEXT("\n")) + TEXT("\n"));
	}

	int WriteMemoryFiles()
	{
		int Wrote = 0;
		GossiperPtr Two[2] = { GW1, GN2 };
		const TCHAR* Leaves[2] = { TEXT("ue-crime-memory-w1.md"), TEXT("ue-crime-memory-n2.md") };
		for (int I = 0; I < 2; ++I)
		{
			if (!Two[I] || !Two[I]->Memory) { continue; }
			// THE MARKDOWN IS THE ARTEFACT OF "PERMANENTLY REMEMBER" and it
			// comes out of MemoryStore::ToMarkdown, the ported function, not
			// out of a formatter written here.
			SaveBoth(Leaves[I], Un(Two[I]->Memory->ToMarkdown()));
			++Wrote;
		}
		return Wrote;
	}

	void WriteBreadcrumb(const TCHAR* Phase)
	{
		TArray<FString> Out;
		Out.Add(FString::Printf(TEXT("# UE crime probe %s @%lld"),
		                        *CrimeSha(), (long long)FDateTime::UtcNow().ToUnixTimestamp()));
		Out.Add(TEXT("# Line 1 names the commit this was measured on, as the Unity verdict does."));
		Out.Add(TEXT(""));
		Out.Add(FString::Printf(TEXT("crimePhaseReached=%s"), Phase));
		Out.Add(TEXT("crimeReached=in-progress"));
		SaveBoth(TEXT("ue-crime-verdict.txt"), FString::Join(Out, TEXT("\n")) + TEXT("\n"));
	}

	std::string SummariesDenominator()
	{
		int N = 0;
		if (GMill)
		{
			const std::vector<GossiperPtr>& Agents = GMill->Agents();
			for (std::vector<GossiperPtr>::size_type I = 0; I < Agents.size(); ++I)
			{
				if (Agents[I]) { N += (int)Agents[I]->Rumors.size(); }
			}
		}
		return LedgerCrime::Int(N);
	}

	void WriteFinalVerdict()
	{
		const Deed DeedA = LedgerCrime::MakeDeed("crime_a", "player", Utf8(FString(kGlassA)));

		TArray<FString> Out;
		Out.Add(FString::Printf(TEXT("# UE crime probe %s @%lld"),
		                        *CrimeSha(), (long long)FDateTime::UtcNow().ToUnixTimestamp()));
		Out.Add(TEXT("# Line 1 names the commit this was measured on, as the Unity verdict does."));
		Out.Add(TEXT("# Ruling 2026-09-08, the crime, the witness and the overheard consequence."));
		Out.Add(TEXT("# THE ACT: crimeAct= lines say how the deed arrived, as FOUR separate facts,"));
		Out.Add(TEXT("#   because collapsing any two of them lets this file say something untrue."));
		Out.Add(TEXT("#   pressLanded is how far the injected press got - a controller, a"));
		Out.Add(TEXT("#   UPlayerInput to receive it, or neither - and NOT whether anything fired."));
		Out.Add(TEXT("#   requestsSeen is how many times ALedgerCharacter's own E binding actually"));
		Out.Add(TEXT("#   fired. attempted is whether the deed was therefore begun. took is whether"));
		Out.Add(TEXT("#   the window is really gone, read back off the actor after the fact."));
		Out.Add(TEXT("#   staleDropped is presses found waiting when the phase opened and discarded"));
		Out.Add(TEXT("#   as belonging to no crime; a non-zero there on a healthy run is a bug."));
		Out.Add(TEXT("#   THERE IS NO BRANCH THAT ATTEMPTS THE DEED WITHOUT A PRESS: the await"));
		Out.Add(TEXT("#   phase routes a give-up straight past the commit phase. So attempted=yes"));
		Out.Add(TEXT("#   is evidence that a key press caused it."));
		Out.Add(TEXT("#   WHAT IS NOT TRUE YET, said here rather than left to be assumed: no"));
		Out.Add(TEXT("#   automated check anywhere reads these lines, so a run in which the input"));
		Out.Add(TEXT("#   path was dead is committed and pushed GREEN. A human reading this file is"));
		Out.Add(TEXT("#   the only thing that catches it today."));
		for (int I = 0; I < 2; ++I)
		{
			Out.Add(FString::Printf(
				TEXT("crimeAct id=%s pressesSent=%d pressLanded=%s staleDropped=%d ")
				TEXT("requestsSeen=%d gaveUp=%s attempted=%s took=%s pawnClass=%s ")
				TEXT("ceilingSeconds=%.1f"),
				I == 0 ? TEXT("A") : TEXT("B"),
				GActPressesSent[I],
				GActPressLanded[I],
				GActStaleDropped[I],
				GActRequestsSeen[I],
				GActGaveUp[I] ? TEXT("yes") : TEXT("no"),
				GActAttempted[I] ? TEXT("yes") : TEXT("no"),
				GActTook[I] ? TEXT("yes") : TEXT("no"),
				GActPawnClass[I],
				LedgerCrime::kActCeilingSeconds));
		}
		Out.Add(TEXT("#   launchStatus is added by the workflow step from this file's presence, its"));
		Out.Add(TEXT("#   last crimePhaseReached and the process's exit code, because only something"));
		Out.Add(TEXT("#   watching from outside can tell a hang from a crash from a clean exit."));
		Out.Add(TEXT("# THE SCENE: the same piecesEmitted=N/M counters BuildScene emits, read back,"));
		Out.Add(TEXT("#   never recomputed. probe* counts are THIS module's own pieces, which are"));
		Out.Add(TEXT("#   not street pieces and are never in GByName."));
		Out.Add(TEXT("# THE WITNESS: every witness= line is one witness at one crime, measured off"));
		Out.Add(TEXT("#   the engine (two line traces, the actor's own bounds, an accumulated"));
		Out.Add(TEXT("#   watching time) and decided by Observe.Resolve, the transliterated C#."));
		Out.Add(TEXT("#   THE VANTAGE IS READ BEFORE THE DEED, with the glass standing: hiding the"));
		Out.Add(TEXT("#   pane first would let the trace through the empty frame onto the interior"));
		Out.Add(TEXT("#   wall and print the accepting case as a rejection."));
		Out.Add(TEXT("# THE MILL: gossipRound= lines are the rule-5b pair. Round 1 is the same two"));
		Out.Add(TEXT("#   people too far apart to talk; round 2 is the same two in the yard. Nothing"));
		Out.Add(TEXT("#   about the rumour changes between them except where they are standing."));
		Out.Add(TEXT("# THE LINE IS COMPOSED, NOT PICKED, since queue 147. The bank at"));
		Out.Add(TEXT("#   content/dialogue/crime-witness-v1.json still supplies the rung and the id"));
		Out.Add(TEXT("#   by the seed the game uses, Day*31+Hour, and the seed, the modulus and the"));
		Out.Add(TEXT("#   picked index are printed so that pick can still be checked. What the two"));
		Out.Add(TEXT("#   of them SAY is then built by the ported StreetVoice.Exchange around the"));
		Out.Add(TEXT("#   summary the mill actually carried. overheardReplyMode says which, with"));
		Out.Add(TEXT("#   the count of beats in each mode; the telling is the composed beat and the"));
		Out.Add(TEXT("#   answer is a literal from the HEARER'S disposition band, which is the C#'s"));
		Out.Add(TEXT("#   own accounting at StreetVoice.cs 289 to 295 and not a softening of it."));
		Out.Add(TEXT("# EVERY ZERO SHIPS ITS DENOMINATOR AND EVERY CAP ANNOUNCES ITSELF."));
		Out.Add(TEXT(""));

		// 1. The scene, and this module's own pieces.
		Out.Add(LedgerVignetteShot::StreetSceneLine());
		Out.Add(Un("probeFloor=" + LedgerCrime::Int(GFloorSpawned) + "/1"
		           " probeFloorNote=not-a-street-piece/the-street-owes-a-yard-behind-the-crossover"
		           " probeBodies=" + LedgerCrime::Int(GBodiesSpawned) + "/2"
		           " probeShards=" + LedgerCrime::Int(GShardsSpawned) + "/16"
		           " probeBricks=" + LedgerCrime::Int(GBricksSpawned) + "/2"
		           " probePiecesMaterialBound=0/" + LedgerCrime::Int(GProbePiecesAsked)
		         + " probePiecesMaterialNote=BindSurfaces-runs-inside-BuildScene/these-spawn-after-it"
		           " probePiecesNote=not-street-pieces/never-in-GByName"));

		// 2. The inputs, once, each beside the C# line it came from.
		Out.Add(Un("crimeGameTime=D1/12:00 crimeGameTimeSource=GameTime.cs-9-22"
		           " crimeLightLevel=" + LedgerCrime::F2(LedgerCrime::kLightLevel)
		         + " crimeLightLevelSource=Perceivers.cs-69-71/overcast_day-night-0-lanterns-off"
		           " crimeAmbientFloor=" + LedgerCrime::F1(LedgerCrime::kAmbientFloor)
		         + " crimeAmbientFloorSource=Perception.cs-228/AmbientDaytimeStreet"
		           " crimeLoudness=" + LedgerCrime::F1(DeedA.Loudness)
		         + " crimeLoudnessSource=Perception.cs-244/LoudBottleSmash"
		           " castTie=" + LedgerCrime::F2(LedgerCrime::kTie)
		         + " castTieSource=GossipDirector.cs-127-128"
		           " castFamiliarityW1=" + LedgerCrime::F2(LedgerCrime::kFamiliarity)
		         + " castFamiliarityN2=" + LedgerCrime::F2(LedgerCrime::kFamiliarity)
		         + " castFamiliaritySource=Witnesses.cs-142/strangers"
		           " castRungFloor=0 castRungFloorSource=Perception.Attention-out-of-scope"
		           " castAlertness=0 castBodies=cylinder-stand-in/no-mixamo-body-in-ue-probe"));
		Out.Add(Un(LedgerCrime::DeedInputsLine(DeedA)));

		// THE PREDICTION THE FIRST RUN IS READ AGAINST, ruling section 2. Hand
		// arithmetic from the piece list, printed so a disagreement between it
		// and the measurements above is a finding rather than a surprise.
		Out.Add(TEXT("crimePrediction=w1/A/actorM=2.28/victimM=2.15/victimOffAxisDeg=28.2")
		        TEXT("/faceDeg=69.4/rung=3/certainty=0.94/audibleRadiusM=13.1")
		        TEXT(" crimePredictionOccluded=w1/B,n2/A,n2/B/blocker=west_south_bay2")
		        TEXT("/audibleRadiusM=1.9/slots=none")
		        TEXT(" crimePredictionSource=ruling-section-2/hand-arithmetic-not-a-measurement"));

		// 3. The two deeds.
		for (int I = 0; I < 2; ++I) { Out.Add(Un(LedgerCrime::CrimeLine(GCrime[I]))); }

		// 4. The four witness readings, the per-sample moment.
		Out.Add(Un("witnessReadings=" + LedgerCrime::Int((int)GReadings.size()) + "/4"));
		if (GReadings.empty())
		{
			Out.Add(TEXT("NOTHING MEASURED - no vantage reached the resolver on this commit."));
		}
		// ONE DEED PER CRIME, NOT ONE FOR BOTH. The two are the same act at
		// the same loudness and differ only in which window they name, but the
		// hearing half of Resolve reads the deed the witness was resolved
		// against, so the line is printed against the same one.
		const Deed DeedB = LedgerCrime::MakeDeed("crime_b", "player", Utf8(FString(kGlassB)));
		for (std::vector<LedgerCrime::Reading>::size_type I = 0; I < GReadings.size(); ++I)
		{
			Out.Add(Un(LedgerCrime::WitnessLine(GReadings[I],
				GReadings[I].EventId == "A" ? DeedA : DeedB)));
		}

		// 5. The mill, whole run.
		Out.Add(Un("witnessesOffered=" + LedgerCrime::Int(GMill ? GMill->WitnessesOffered() : 0)
		         + " witnessesDropped=" + LedgerCrime::Int(GMill ? GMill->WitnessesDropped() : 0)
		         + "/" + LedgerCrime::Int(GMill ? GMill->WitnessesOffered() : 0)
		         + " summariesSayingPlayer=" + LedgerCrime::Int(GMill ? GMill->SummariesSaying("player") : 0)
		         + "/" + SummariesDenominator() + "-rumours"
		         + " summariesSayingPlayerStat=whole-run/every-agent-every-rumour"
		           " gossipSuspicionPorted=yes/town-list-6n"));

		// 6. The two rounds.
		Out.Add(Un(LedgerCrime::GossipRoundLine(GRound1)));
		Out.Add(Un(LedgerCrime::GossipRoundLine(GRound2)));
		// THE SECOND RETELLING AND WHAT IT ADDS UP TO. Holding counts the
		// PEOPLE who hold a rumour naming crime A's glass, not the rumours,
		// because the gate is about residents reached.
		{
			const int HoldingA = GMill ? LedgerCrime::ResidentsHoldingA(GMill->Agents()) : 0;
			Out.Add(Un(LedgerCrime::GossipRoundLine(GRound3)));
			// WHEN HE HEARD IT, OFF HIS OWN MEMORY: the last "heard" event.
			int HeardDay = -1, HeardHour = -1;
			if (GR3 && GR3->Memory)
			{
				const std::vector<MemoryEvent>& Ev = GR3->Memory->Events;
				for (std::vector<MemoryEvent>::size_type I = 0; I < Ev.size(); ++I)
				{
					if (Ev[I].Kind != "heard") { continue; }
					HeardDay = Ev[I].Time.Day;
					HeardHour = Ev[I].Time.Hour;
				}
			}
			Out.Add(Un(LedgerCrime::ReachLine(GRound3, HoldingA, GR3Body != nullptr,
			                                  LedgerCrime::kCrimeDay, LedgerCrime::kCrimeHour,
			                                  HeardDay, HeardHour)));
		}

		// 7. The overheard beat, and the prose on its own line under it.
		Out.Add(Un(LedgerCrime::OverheardLine(GOverheard)));
		Out.Add(Un(LedgerCrime::OverheardTextLine(GOverheard)));

		// 8. Memory, whole run.
		const int W1Events = (GW1 && GW1->Memory) ? (int)GW1->Memory->Events.size() : 0;
		const int N2Events = (GN2 && GN2->Memory) ? (int)GN2->Memory->Events.size() : 0;
		Out.Add(Un("memoryW1Events=" + LedgerCrime::Int(W1Events)
		         + " memoryN2Events=" + LedgerCrime::Int(N2Events)
		         + " memoryFiles=" + LedgerCrime::Int(WriteMemoryFiles()) + "/2"
		           " memoryFilePrefix=ue-crime-memory-"));

		// 8b. THE RESTART. Everything above is one run of the world; this is
		// that run saved, the world built again from the authoring, and the
		// save laid back over it. hopsAfter is the part worth reading twice:
		// the shopkeeper saw it first-hand and comes back at 0 hops, the lad
		// heard it and comes back at 1, so a restore that handed everyone
		// the same records shows up here and nowhere else.
		{
			RestartReading RT;
			RunRestartRoundTrip(RT);
			if (!RT.bRan)
			{
				Out.Add(TEXT("restart=NOT-RUN restartNote=no-mill-or-no-agents/"
				             "nothing-measured-about-surviving-a-restart"));
			}
			else
			{
				Out.Add(Un("restart=RAN savedBytes=" + LedgerCrime::Int(RT.SavedBytes)
				         + " saveLeaf=ue-crime-save-agents.json"
				           " w1RumoursBefore=" + LedgerCrime::Int(RT.W1Before)
				         + " w1RumoursAfter=" + LedgerCrime::Int(RT.W1After)
				         + " n2RumoursBefore=" + LedgerCrime::Int(RT.N2Before)
				         + " n2RumoursAfter=" + LedgerCrime::Int(RT.N2After)
				         + " w1MemoryBefore=" + LedgerCrime::Int(RT.W1MemBefore)
				         + " w1MemoryAfter=" + LedgerCrime::Int(RT.W1MemAfter)
				         + " n2MemoryBefore=" + LedgerCrime::Int(RT.N2MemBefore)
				         + " n2MemoryAfter=" + LedgerCrime::Int(RT.N2MemAfter)
				         + " w1ConfidenceBefore=" + LedgerCrime::F2(RT.W1ConfBefore)
				         + " w1ConfidenceAfter=" + LedgerCrime::F2(RT.W1ConfAfter)
				         + " w1HopsAfter=" + LedgerCrime::Int(RT.W1HopsAfter)
				         + " n2HopsAfter=" + LedgerCrime::Int(RT.N2HopsAfter)
				         + " memoryTextStable=" + std::string(RT.bMemoryTextSame ? "yes" : "no")
				         + " rumoursAboutABefore=" + LedgerCrime::Int(RT.AboutABefore)
				         + " rumoursAboutAAfter=" + LedgerCrime::Int(RT.AboutAAfter)
				         + " rumoursAboutBBefore=" + LedgerCrime::Int(RT.AboutBBefore)
				         + " rumoursAboutBAfter=" + LedgerCrime::Int(RT.AboutBAfter)
				         + (RT.bR3
				            ? " r3RumoursBefore=" + LedgerCrime::Int(RT.R3Before)
				              + " r3RumoursAfter=" + LedgerCrime::Int(RT.R3After)
				              + " r3MemoryBefore=" + LedgerCrime::Int(RT.R3MemBefore)
				              + " r3MemoryAfter=" + LedgerCrime::Int(RT.R3MemAfter)
				              + " r3HopsAfter=" + LedgerCrime::Int(RT.R3HopsAfter)
				            : std::string(" r3=not-in-this-run"))
				         + " restartNote=the-world-is-rebuilt-from-the-authoring-and-the-save-"
				           "laid-over-it/never-restored-into-the-mill-that-already-holds-them"));
			}
		}

		// 8c. THE UNWITNESSED CONTROL, AND IT IS ALREADY IN THIS RUN.
		//
		// The list asks for "the witnessed run and the unwitnessed control,
		// from equivalent clean starts... and the control producing no
		// mention". TWO RUNS WOULD BE A WEAKER TEST THAN THIS ONE. Two
		// separate starts differ in everything the engine does not pin -
		// tick order, frame timing, whatever the scheduler did that second -
		// and any of it could explain a difference. What is here instead is
		// two crimes in ONE run, with one witness position each:
		//
		//   CRIME A is seen. w1 stands a metre and a half away with a clear
		//   line to the actor and the victim, and files an observation.
		//   CRIME B is not. Both agents are behind west_south_bay2, the
		//   traces stop on the building, and neither files anything.
		//
		// Same build, same mill, same perception code, same frame. The only
		// thing that differs is whether anybody could see it, which is the
		// only thing a control is supposed to vary.
		//
		// WHAT MUST FOLLOW FROM THE ONE NOBODY SAW: nothing. No observation
		// filed, so no rumour about it, so nothing said about it. Each of
		// those is a separate fact and a separate way to fail - a rumour
		// with no observation behind it is a mill inventing, and a line
		// mentioning a crime no rumour carries is a voice inventing - so
		// each is counted rather than inferred from the one before it.
		{
			int SeenA = 0, SeenB = 0;
			for (std::vector<LedgerCrime::Reading>::size_type I = 0; I < GReadings.size(); ++I)
			{
				if (!GReadings[I].bFiled) { continue; }
				if (GReadings[I].EventId == "A") { ++SeenA; }
				else if (GReadings[I].EventId == "B") { ++SeenB; }
			}
			// RUMOURS ABOUT EACH CRIME, over every agent in the mill. The
			// predicate a witnessed break carries names the deed, so a
			// rumour about the control would have to name crime B's victim.
			// COUNTED BY THE HEADER'S CountAboutCrimes, the same rule the
			// restart line counts by after the reload, so the two lines
			// cannot disagree about what "about B" means.
			int RumoursA = 0, RumoursB = 0;
			if (GMill)
			{
				LedgerCrime::CountAboutCrimes(GMill->Agents(), RumoursA, RumoursB);
			}
			Out.Add(Un("control=RAN controlCrime=B controlWhy=both-agents-occluded-by-west_south_bay2"
			           " controlCountedOver=" + LedgerCrime::Int(GMill ? (int)GMill->Agents().size() : 0)
			         + "-agents-at-the-end-of-the-run/the-third-resident-included"
			           " seenA=" + LedgerCrime::Int(SeenA)
			         + " seenB=" + LedgerCrime::Int(SeenB)
			         + " rumoursAboutA=" + LedgerCrime::Int(RumoursA)
			         + " rumoursAboutB=" + LedgerCrime::Int(RumoursB)
			         + " controlNote=one-run-two-crimes-one-witness-position-each/"
			           "the-only-thing-that-differs-is-whether-anybody-could-see-it/"
			           "a-second-RUN-would-vary-everything-the-engine-does-not-pin"));
		}

		// 8d. THE ARREST. ROADMAP's stage-3 gate: "arrest reachable from live
		// play, its callers outside Core counted and printed rather than
		// zero". Printed here with its caller's name, the constable's rung and
		// whether he could see, for crime A and for the control, B.
		Out.Add(Un(LedgerCrime::ArrestLine(GArrest[0], GArrest[1], GConfrontCalls)
		         + std::string(" constableBody=") + (bC1Spawned ? "spawned" : "MISSING")));

		// 9. The three combined readings. Each needs both halves.
		Out.Add(Un("witnessStatus=" + LedgerCrime::WitnessStatus(GReadings)
		         + " witnessStatusNote=w1-filed-on-A-with-a-rung/w1-empty-on-B-occluded/n2-empty-on-both"
		           " gossipStatus=" + LedgerCrime::GossipStatus(GRound1, GRound2)
		         + " gossipStatusNote=round-1-not-together-passed-0/round-2-together-passed-1"
		           " combinedReadings=3/3"
		           " combinedReadingsNote=overheardStatus-is-on-the-overheard-line-above/never-printed-twice"));

		// 10. The frames.
		Out.Add(Un("crimeFramesRequested=" + LedgerCrime::Int(GShotsAttempted) + "/"
		         + LedgerCrime::Int(LedgerCrime::kMilestoneCount)
		         + " crimeFramesWrote=" + LedgerCrime::Int(GShotsWrote) + "/"
		         + LedgerCrime::Int(LedgerCrime::kMilestoneCount)));
		if (GShotLines.empty())
		{
			Out.Add(TEXT("NOTHING MEASURED - no frame reached the measuring step on this commit."));
		}
		for (std::vector<std::string>::size_type I = 0; I < GShotLines.size(); ++I)
		{
			Out.Add(Un(GShotLines[I]));
		}
		Out.Add(Un("crimeSeqFramesRequested=" + LedgerCrime::Int(GSeqRequested) + "/"
		         + LedgerCrime::Int(LedgerCrime::kMaxSeqFrames)
		         + " crimeSeqFramesWrote=" + LedgerCrime::Int(GSeqWrote) + "/"
		         + LedgerCrime::Int(LedgerCrime::kMaxSeqFrames)
		         + " crimeSeqIntervalSeconds=" + LedgerCrime::F1(LedgerCrime::kSeqIntervalSeconds)
		         + " crimeSeqForcedAtDeeds=" + LedgerCrime::Int(GSeqForced) + "/"
		         + LedgerCrime::Int(LedgerCrime::kForcedAtDeeds)
		         + " crimeSeqCapNote=32-is-a-clock-cap-not-a-target"
		           " crimeSeqKeysFile=ue-crimeseq-keys.txt"));

		// The instrument's own selftest, and the watching accumulator's
		// denominators. A run that measured nothing says so here too.
		Out.Add(Un("crimeSelftestChecks=" + LedgerCrime::Int(GSelftest.Checks)
		         + " crimeSelftestFailed=" + LedgerCrime::Int(GSelftest.Failed) + "/"
		         + LedgerCrime::Int(GSelftest.Checks)
		         + " crimeSelftestFirstFailure=" + GSelftest.FirstFailure
		         + " crimeSelftestNote=CrimeProbe.h-decisions-and-strings/run-again-here-on-the-machine"));
		Out.Add(Un("watchTicksA=" + LedgerCrime::Int(GWatchTicks[0])
		         + " watchTicksB=" + LedgerCrime::Int(GWatchTicks[1])
		         + " watchSecondsW1A=" + LedgerCrime::F2(GSeconds[0][0])
		         + " watchSecondsN2A=" + LedgerCrime::F2(GSeconds[0][1])
		         + " watchSecondsW1B=" + LedgerCrime::F2(GSeconds[1][0])
		         + " watchSecondsN2B=" + LedgerCrime::F2(GSeconds[1][1])
		         + " watchStat=accumulated-while-InSight-to-the-actor-held/Perception.cs-65"));
		// THE ROW'S TWO STRINGS, SIDE BY SIDE AND AT THE SAME MOMENT, queue 157.
		// bankSummaryText is what she SAYS; bankSummaryClause is what the mill
		// FILED and therefore what both splices carried. A reader holding only
		// one of them cannot tell which was spliced, which is how the sentence
		// reached a committed memory file unnoticed. The shape says
		// nothing-measured when no witness_summary was picked at all, so a
		// never-ran run cannot read as a missing clause.
		const std::string ClauseShapeValue = (GSummaryClause == "none")
			? std::string("nothing-measured/no-witness-summary-was-picked")
			: LedgerCrime::ClauseShape(GSummaryClause);
		Out.Add(Un("bankTried=" + LedgerCrime::Int((int)GBankTried.size())
		         + " bankFrom=" + GOverheard.BankPath
		         + " bankSummaryText=" + LedgerCrime::NoSpaces(GSummaryText)
		         + " bankSummaryClause=" + LedgerCrime::NoSpaces(GSummaryClause)
		         + " bankSummaryClauseShape=" + LedgerCrime::NoSpaces(ClauseShapeValue)
		         + " bankReplyText=" + LedgerCrime::NoSpaces(GReplyText)
		         + " bankTextNote=spaces-become-dashes-in-a-value/the-bank-file-holds-the-prose"
		           "/these-are-the-BANK-rows-at-the-rung/the-clause-is-what-the-mill-filed"
		           "/the-sentence-is-what-she-said/what-was-said-is-on-the-overheardTellText-line"));
		Out.Add(FString::Printf(TEXT("crimeTicks=%d crimeSeconds=%.2f crimeFinishReason=%s"),
		                        GTicks, NowS() - GRunStart, *GFinishReason));

		Out.Add(TEXT("crimePhaseReached=done"));
		Out.Add(TEXT("crimeReached=end"));
		SaveBoth(TEXT("ue-crime-verdict.txt"), FString::Join(Out, TEXT("\n")) + TEXT("\n"));
		WriteSeqKeys();
	}

	void Finish()
	{
		GPhase = ECrimePhase::Done;
		WriteFinalVerdict();
		if (GEnc != EEncounter::None) { WriteEncounterVerdict(); }
		FPlatformMisc::RequestExit(false);
	}

	// ---- the props -------------------------------------------------------
	void RespawnMate(UWorld* World);   // below; -CastAllNow calls it from here

	void PlaceProps(UWorld* World)
	{
		// + 1 FOR THE CONSTABLE, 22 September. He is spawned through the same
		// probe-piece path as the two witnesses, so a count that still read 21
		// would print one piece fewer than was asked for - the independent
		// check caught it.
		// + 1 MORE FOR THE THIRD RESIDENT, the same day: his body is a
		// probe piece too, spawned late, at the meeting.
		GProbePiecesAsked = 1 + 2 + 16 + 2 + 1 + 1;

		// THE YARD FLOOR FIRST: nothing else in the yard has anything to
		// stand on. ground_plot_2 ends at x 21 and ground_plot_3 starts at x
		// 24, and the gap between them is the only place a person can stand
		// with a terrace between them and a shop window.
		GYardFloor = SpawnBox(World, TEXT("probe_yard_floor"),
			LedgerCrime::P3(LedgerCrime::kYardX, LedgerCrime::kYardY, LedgerCrime::kYardZ),
			LedgerCrime::kYardSX, LedgerCrime::kYardSY, LedgerCrime::kYardSZ, TEXT("concrete"));
		if (GYardFloor != nullptr) { ++GFloorSpawned; }

		double GY = 0.0;
		std::string On;
		if (!GroundYAt(World, LedgerCrime::kW1AX, LedgerCrime::kW1AZ, GY, On)) { GY = 0.1; }
		GW1Body = SpawnBody(World, TEXT("probe_body_w1"),
		                    LedgerCrime::kW1AX, LedgerCrime::kW1AZ, GY);
		if (GW1Body != nullptr) { ++GBodiesSpawned; }

		if (!GroundYAt(World, LedgerCrime::kN2X, LedgerCrime::kN2Z, GY, On)) { GY = 0.1; }
		GN2Body = SpawnBody(World, TEXT("probe_body_n2"),
		                    LedgerCrime::kN2X, LedgerCrime::kN2Z, GY);
		if (GN2Body != nullptr) { ++GBodiesSpawned; }

		if (!GroundYAt(World, LedgerCrime::kC1AX, LedgerCrime::kC1AZ, GY, On)) { GY = 0.1; }
		// NO CONSTABLE IN PLAY: the cast has no policeman yet, and a grey
		// cylinder on the pavement is a stand-in.
		GC1Body = (GEnc == EEncounter::Live) ? nullptr : SpawnBody(World, TEXT("probe_body_c1"),
		                    LedgerCrime::kC1AX, LedgerCrime::kC1AZ, GY);
		bC1Spawned = (GC1Body != nullptr);
		FaceBody(GC1Body, LedgerCrime::P3(LedgerCrime::kCrimeAX, 0.0, LedgerCrime::kCrimeAZ));

		FaceBody(GW1Body, LedgerCrime::P3(LedgerCrime::kCrimeAX, 0.0, LedgerCrime::kCrimeAZ));
		// N2 faces +z, up the yard, by the ruling: he is not looking at
		// anything and the terrace is between him and both windows anyway.
		if (GN2Body != nullptr) { GN2Body->SetActorRotation(FRotator(0.0f, 90.0f, 0.0f)); }
		DressBody(World, GW1Body, TEXT("Lena"));   // names-gate: allow (the asset MH_LenaT2, not shown)
		DressBody(World, GN2Body, TEXT("Sam"));    // names-gate: allow (the asset MH_SamT2)
		// -CastAllNow, 25 September (evening): Ron joins the other two from the
		// start, where the story puts him later, so the portrait tool's
		// -PortraitInGame can photograph all three where the game stands them.
		if (GEnc == EEncounter::Live && FParse::Param(FCommandLine::Get(), TEXT("CastAllNow"))) { RespawnMate(World); }

		bRitasWindow = GEnc == EEncounter::Live && !bLiveScript;
		GGlass[0] = LedgerVignetteShot::FindStreetPiece(bRitasWindow ? kGlassR : kGlassA);
		GGlass[1] = LedgerVignetteShot::FindStreetPiece(kGlassB);
		if (GGlass[0] != nullptr)
		{
			bWindowGlassStartRead = true;
			bWindowGlassStartHidden = GGlass[0]->IsHidden();
			bWindowGlassStartCollides = GGlass[0]->GetActorEnableCollision();
		}

		// NO SLOT BETWEEN THE PARKED CARS AND THE KERB RAILING (the AI tester,
		// 30 September: by the fish market he pushed into it and stuck). The
		// railing runs x 10 to 16 m at z 3.375 (vignette-pieces.json, E8) and
		// the cars' near sides stand at z 2.78 (street-vehicles.json, 1.64 m
		// wide at z 1.96): 0.6 m, narrower than he is. An unseen wall there
		// stops him at its mouth; it blocks only people, so no sight line or
		// camera trace meets it. Free play only: the regression's street is its own.
		if (bRitasWindow)
		{
			if (AActor* Slot = SpawnBox(World, TEXT("free_car_rail_slot"), LedgerCrime::P3(13.0, 0.5, 3.08), 6.4, 1.2, 0.56, TEXT("concrete")))
			{
				Slot->SetActorHiddenInGame(true);
				if (AStaticMeshActor* M = Cast<AStaticMeshActor>(Slot))
				{
					UStaticMeshComponent* C = M->GetStaticMeshComponent();
					C->SetCollisionResponseToAllChannels(ECR_Ignore);
					C->SetCollisionResponseToChannel(ECC_Pawn, ECR_Block);
				}
			}
		}
	}

	// THE CAST FILE, once read (the ties, and the places where he is seen).
	CastDay GCast;
	bool bGCast = false;

	// THE HOURS THE TOWN HAS TALKED (town list 6bs): one per game, saved
	// beside the remarks. As each game hour starts, and after a load, the
	// town's rounds by the cast file's routines run every hour not yet run:
	// the hour now for every pair the street does not hold (Sheila, Darren
	// and Ron are on it and talk by distance, as they did), and any hours
	// skipped (the night a load passes) with nobody on the street, so whoever
	// the routines put together talks; and the mill ages once an hour. The
	// regression keeps its measured rounds without it.
	TownHours GTownHours;

	// The mill knows them by the probe's ids, the cast file by its own.
	struct FStreetCast
	{
		const CastDay* Cast = nullptr;
		static std::string CastId(const std::string& Id)
		{
			return Id == "w1" ? std::string("lena") : Id == "n2" ? std::string("sam")
			     : Id == LedgerCrime::kR3Id ? std::string("rocco") : Id;
		}
		bool Together(const std::string& A, const std::string& B, int Day, int Hour) const
		{
			return Cast != nullptr && Cast->Together(CastId(A), CastId(B), Day, Hour);
		}
	};

	void TownHoursTick()
	{
		if (GEnc != EEncounter::Live || !GMill || !bGCast || !bLiveScript) { return; }
		FStreetCast Street;
		Street.Cast = &GCast;
		// WHO THE STREET HOLDS: in the scripted encounter the game passes the
		// story between the three itself (its staged rounds), so the town's
		// hourly talk leaves those pairs alone. In free play nothing is staged
		// (Jafar's list, item 1): they talk by their routines, as the rest of
		// the town does, or the story never leaves the one who saw.
		const int Ran = GTownHours.RunTo(GMill.get(), &Street, GNow,
			[](const std::string& Id) { return bLiveScript && (Id == "w1" || Id == "n2" || Id == LedgerCrime::kR3Id); });
		if (Ran > 0)
		{
			UE_LOG(LogTemp, Display, TEXT("LedgerTownHours: %d hour(s) of the town's talk, to %s; next hour %lld"),
				Ran, *Un(GNow.ToString()), GTownHours.NextHour());
		}
	}

	// THE WINDOW AS A DEED THE TOWN HOLDS (town list 6ac, 6au): when it
	// happened, game time, and where each who saw him near it saw him (a
	// place id from the cast file), by gossip id.
	bool bDeedDone = false;
	int GDeedDay = -1, GDeedHour = -1;
	std::map<std::string, std::string> GSawHimAt;
	// WHOM HE HAS MET, AND ON WHICH DAYS (the review's A4): a conversation, the
	// walk round, Ada's tea, Ron's envelope. Who can recognise him grows from it.
	LedgerCrime::MeetingBook GMet;
	// How well somebody he talks to knows him now: the street has heard of the
	// new owner (kLadFamiliarity); in free play, his meetings with them raise it.
	double TalkFamiliarity(const std::string& Card)
	{
		if (bLiveScript) { return LedgerCrime::kLadFamiliarity; }
		return std::max(LedgerCrime::kLadFamiliarity, LedgerCrime::FamiliarityFromMeetings(GMet.DaysMet(Card)));
	}

	void MarkDeedTime()
	{
		if (bDeedDone) { return; }
		bDeedDone = true;
		GDeedDay = GNow.Day;
		GDeedHour = GNow.Hour;
	}

	// SEEN NEAR THE DEED (town list 6au): the place nearest where he stood,
	// kept as where this person saw him, and the story that he was there,
	// given to them for the gossip to carry.
	void SawHimNear(const GossiperPtr& G, double X, double Z, double Confidence, int Rung)
	{
		if (!G || !bGCast) { return; }
		MarkDeedTime();
		const std::string Place = GCast.NearestPlace(X, Z, 6.0);
		if (Place.empty()) { return; }
		GSawHimAt[G->Id] = Place;
		const std::string AreaId = GCast.AreaOf(Place);
		const std::string Area = AreaId.empty() ? Place : AreaId;
		const std::vector<std::string> Names = GCast.AreaNamesOf(Area);
		const std::string Words = !Names.empty() ? Names[0] : !GCast.SaidOf(Place).empty() ? GCast.SaidOf(Place) : Area;
		const std::string Topic = std::string("player.") + LedgerCrime::SightingPredicate(DeedKeyNow());
		for (const RumorPtr& R : G->Rumors) { if (R && R->TopicKey() == Topic) { return; } }
		RumorPtr At = LedgerCrime::SightingStory(DeedKeyNow(), Area, Words, GDeedDay, GDeedHour, G->Id, Confidence, Rung);
		G->Rumors.push_back(At);
		UE_LOG(LogTemp, Display, TEXT("LedgerDeed: %s saw him at %s: %s"), *Un(G->Id), *Un(Place), *Un(At->Summary));
	}

	// ---- filing what a witness got ---------------------------------------
	void ResolveAndFile(int Index)
	{
		const std::string EventId = (Index == 0) ? "A" : "B";
		const std::string VictimId = Index == 0 ? Utf8(FString(kGlassA)) : Utf8(FString(kGlassB));
		const Deed D = LedgerCrime::MakeDeed(Index == 0 ? "crime_a" : "crime_b", "player", VictimId);

		for (std::vector<LedgerCrime::Reading>::size_type I = 0; I < GReadings.size(); ++I)
		{
			LedgerCrime::Reading& R = GReadings[I];
			if (R.EventId != EventId) { continue; }
			LedgerCrime::Resolve(R, D);
			if (GEnc == EEncounter::Live && !bLiveScript && Index == 0)
			{
				LedgerSession::Write(TEXT("witness"), TEXT("\"who\":") + LedgerSession::Str(Un(R.WitnessId))
					+ FString::Printf(TEXT(",\"rung\":%d,\"saw\":%s,\"metres\":%.1f,\"light\":%.2f,\"familiarity\":%.2f"),
						R.O.Rung, R.bFiled ? TEXT("true") : TEXT("false"), R.ActorMetres, R.Light, R.Familiarity));
			}
			if (!R.bFiled) { continue; }

			// THE RUNG SHE ACTUALLY REACHED DECIDES THE WORDS, both of them.
			// The row's sentence is what she says out loud; the row's clause is
			// what Witness files and what the heard memory repeats. Neither may
			// claim more than the rung she reached, and the bank's spec holds
			// both to the same ceiling.
			if (R.O.Rung > GAchievedRung) { GAchievedRung = R.O.Rung; }
			std::string Id, Text, Clause, Speaker, Why;
			int Variants = 0;
			const int Seed = LedgerCrime::Seed(GNow);
			// THE SENTINEL LIVES IN THE HEADER, where the test that refuses to
			// compose from it lives: two copies of this string would let the
			// producer drift away from the check and the beat would speak a
			// diagnostic.
			std::string Summary = LedgerCrime::UnreadableSummaryPrefix() + GOverheard.WhyNot;
			bool bBankWords = false;
			if (LedgerCrime::BankPick(GBankText, "witness_summary", R.O.Rung, Seed,
			                          Id, Text, Clause, Speaker, Variants, Why))
			{
				bBankWords = true;
				// TWO STRINGS, TWO JOBS, queue 157. The SENTENCE is what she
				// says out loud and is the fallback the composer speaks when it
				// refuses. The CLAUSE is what the mill files as the Summary,
				// because both consumers splice it: Gossip.h 586 after "I heard
				// from the shopkeeper that ", and StreetVoice's templates into
				// the middle of a sentence. Filing the sentence is what shipped
				// "I heard from the shopkeeper that He looked straight at me
				// before he ran." in production/d1-probe/ue-crime-memory-n2.md.
				GSummaryText = Text;
				GSummaryClause = Clause.empty() ? std::string("none") : Clause;
				// THE DECISION AND ITS WORDING ARE IN THE HEADER, where g++ runs
				// them: a row with no clause refuses by name through the
				// sentinel the composer already refuses on, and never falls back
				// to the sentence.
				std::string WhyClause;
				Summary = LedgerCrime::SummaryToFile(Id, Clause, WhyClause);
				if (WhyClause != "none") { GOverheard.WhyNot = WhyClause; }
				GOverheard.SummaryId = Id;
				GOverheard.Variants = Variants;
				GOverheard.VariantPicked = LedgerCrime::VariantIndex(Seed, Variants);
				GOverheard.SeedValue = Seed;
				GOverheard.IdRung = R.O.Rung;
			}
			else
			{
				GOverheard.WhyNot = Why;
				GOverheard.SeedValue = Seed;
				GOverheard.IdRung = R.O.Rung;
			}
			// WHAT SHE FILES (the review's A1; Jafar's A5 ruling): a noise alone is
			// the damage heard, never a story about him and never a diagnostic;
			// a story about him only from a sighting the bank has words for.
			const LedgerCrime::WitnessFiles Files = LedgerCrime::WhatWitnessFiles(R.O.Rung, bBankWords
				&& Summary.compare(0, std::string(LedgerCrime::UnreadableSummaryPrefix()).size(), LedgerCrime::UnreadableSummaryPrefix()) != 0);
			if (GMill && Files == LedgerCrime::WitnessFiles::NoiseOnly)
			{
				if (bRitasWindow && Index == 0)
				{
					const GossiperPtr G = GMill->Get(R.WitnessId);
					const size_t Memories = G && G->Memory ? G->Memory->Events.size() : 0;
					GMill->Witness(R.WitnessId, Fact(std::string(TownNews::Subject), std::string("rita_window"), std::string("heard")),
					               "somebody put Rita's window in", false, GNow, 0.9);
					if (G && G->Memory)
					{
						if (G->Memory->Events.size() > Memories) G->Memory->Events.erase(G->Memory->Events.begin() + Memories, G->Memory->Events.end());
						G->Memory->Append(MemoryEvent(GNow, "observation", 0.6, "I heard glass go over at Rita's. I never saw who did it."));
					}
					GHeardOnly.insert(R.WitnessId);
				}
				UE_LOG(LogTemp, Display, TEXT("LedgerCrime: %s heard it only (rung 0): the damage heard, no story about him"), *Un(R.WitnessId));
				continue;
			}
			if (Files == LedgerCrime::WitnessFiles::Nothing)
			{
				UE_LOG(LogTemp, Display, TEXT("LedgerCrime: %s at rung %d: no words in the bank, nothing filed"), *Un(R.WitnessId), R.O.Rung);
				continue;
			}
			if (GMill)
			{
				// A first-hand sighting enters the network at the certainty
				// the resolver measured, which is what everything downstream
				// inherits.
				const Fact Content = bRitasWindow
					? Fact(std::string("player"), "window_d" + std::to_string(GNow.Day), std::string("ritas"))
					: Fact(std::string("player"), std::string("broke_a_window"), VictimId);
				// THE RUNG SHE REACHED travels with the story (town list 6n), so a
				// retelling whose first teller knew him can name him; since the
				// town's A5 fix of 30 September a story with no rung reads as known,
				// so the regression's carry its rung too.
				// EVERY SIGHTING CARRIES ITS RUNG (the town's handover of 30 September:
				// in the Core no rung now reads as a thing known, naming him).
				GMill->Witness(R.WitnessId, Content, Summary, /*bSensitive=*/bRitasWindow, GNow,
				               R.O.Certainty, /*bIndelible=*/false, R.O.Rung);
				// WHERE SHE SAW HIM (town list 6ac, 6au), in play, when what she
				// saw can be tied to him.
				if (GEnc == EEncounter::Live && Index == 0 && LedgerCrime::CanNameHim(R.O.Rung))
				{
					double Sx = LedgerCrime::kCrimeAX, Sz = LedgerCrime::kCrimeAZ;
					if (bRitasWindow && GGlass[0] != nullptr)
					{
						const LedgerCrime::P3 G = ToStreet(GGlass[0]->GetComponentsBoundingBox(true).GetCenter());
						Sx = G.X; Sz = G.Z;
					}
					SawHimNear(GMill->Get(R.WitnessId), Sx, Sz, R.O.Certainty, R.O.Rung);
				}
				if (GEnc != EEncounter::None && Index == 0 && R.WitnessId == GIdW1)
				{
					GW1RungA = R.O.Rung;
					GFiledSummaryA = Summary;
					if (LedgerCrime::WitnessShouts(R.O.Rung)) { PlayShout(); }
				}
			}
		}

		// THE ARREST, ASKED OF THE CONSTABLE, WITH THIS SAME DEED. This is the
		// call site outside Core that ROADMAP's stage-3 gate counts; the
		// verdict names it. Only if he was measured - a missing body is an
		// arrest that was not asked, and the verdict says NOT-RUN rather than
		// this line inventing one.
		if (bC1Spawned && GC1Reading[Index].WitnessId == "c1")
		{
			GArrest[Index] = LedgerCrime::ArrestFor(GC1Reading[Index], D, GConfrontCalls,
			                                        "CrimeProbe.cpp/ResolveAndFile");
		}
	}

	// ---- the encounter's parts --------------------------------------------

	std::string JsonEsc(const std::string& In)
	{
		std::string O;
		for (char Ch : In)
		{
			switch (Ch)
			{
			case '\\': O += "\\\\"; break;
			case '"':  O += "\\\""; break;
			case '\n': O += "\\n"; break;
			case '\r': O += "\\r"; break;
			case '\t': O += "\\t"; break;
			default:   O += Ch; break;
			}
		}
		return O;
	}

	FString EncSaveDir()
	{
		FString D;
		if (FParse::Value(FCommandLine::Get(), TEXT("EncounterSave="), D)) { return D; }
		return FPaths::ConvertRelativePathToFull(FPaths::ProjectSavedDir()
			/ (GEnc == EEncounter::Live ? TEXT("EncounterLive") : TEXT("Encounter")));
	}

	int AboutCrime(const GossiperPtr& G, bool bA)
	{
		if (!G) { return 0; }
		std::vector<GossiperPtr> One(1, G);
		int A = 0, B = 0;
		LedgerCrime::CountAboutCrimes(One, A, B);
		return bA ? A : B;
	}

	// A memory of a crime is one the street files about a deed: something
	// seen or something heard. Since 24 September the lad's sighting of the
	// man in the yard is an observation too, and is counted here: in the
	// play run the lad holds two (what he heard, what he saw).
	int HeardMemories(const GossiperPtr& G)
	{
		if (!G || !G->Memory) { return 0; }
		int N = 0;
		for (const MemoryEvent& E : G->Memory->Events) { if (E.Kind == "heard") { ++N; } }
		return N;
	}

	int CrimeMemories(const GossiperPtr& G)
	{
		if (!G || !G->Memory) { return 0; }
		int N = 0;
		for (const MemoryEvent& E : G->Memory->Events)
		{
			if (E.Kind == "observation" || E.Kind == "heard") { ++N; }
		}
		return N;
	}

	// THE AUDIBLE CONSEQUENCE: the witness shouts where she stands, a
	// spatialised clip from the crowd voices ("Stop. I mean it. Stop."), and
	// the street's output is recorded for four seconds so it can be heard.
	void PlayShout()
	{
		UWorld* World = GameWorld();
		if (World == nullptr || GW1Body == nullptr) { GShoutNote = TEXT("no-world-or-witness-body"); return; }
		USoundWave* Wave = LoadObject<USoundWave>(nullptr, TEXT("/Game/Ledger/Sounds/Voice/crowd_f1/bc9b402a.bc9b402a"));
		if (Wave == nullptr) { GShoutNote = TEXT("clip-not-in-the-build"); return; }
		if (World->GetAudioDevice().IsValid())
		{
			UAudioMixerBlueprintLibrary::StartRecordingOutput(World, 10.0f);
			bShoutRecording = true;
		}
		const FVector At = GW1Body->GetActorLocation() + FVector(0.0, 0.0, 160.0);
		// THE ATTENUATION GOES IN WITH THE SOUND, not after it: set on a
		// component that is already playing, it never reaches the voice, and
		// the shout plays flat and everywhere (the independent check).
		USoundAttenuation* Att = NewObject<USoundAttenuation>(GetTransientPackage());
		FSoundAttenuationSettings& A = Att->Attenuation;
		A.bAttenuate = true;
		A.bSpatialize = true;
		A.AttenuationShape = EAttenuationShape::Sphere;
		A.AttenuationShapeExtents = FVector(300.0f, 0.0f, 0.0f);
		A.FalloffDistance = 4000.0f;
		A.DistanceAlgorithm = EAttenuationDistanceModel::NaturalSound;
		UAudioComponent* C = UGameplayStatics::SpawnSoundAtLocation(World, Wave, At, FRotator::ZeroRotator,
			1.0f, 1.0f, 0.0f, Att);
		if (C != nullptr)
		{
			bShoutPlaying = C->IsPlaying();
			const FSoundAttenuationSettings* Live = C->GetAttenuationSettingsToApply();
			bShoutSpatial = Live != nullptr && Live->bSpatialize && Live->bAttenuate;
			GShoutFalloffM = Live != nullptr ? (Live->AttenuationShapeExtents.X + Live->FalloffDistance) / 100.0 : 0.0;
		}
		GShoutAt = NowS();
		if (GPawn != nullptr) { GShoutPlayerM = FVector::Dist(GPawn->GetActorLocation(), At) / 100.0; }
		GShoutNote = bShoutPlaying ? TEXT("playing") : TEXT("spawned-not-playing");
	}

	void StopShoutRecording(bool bForce)
	{
		if (!bShoutRecording) { return; }
		if (!bForce && NowS() - GShoutAt < 4.0) { return; }
		if (UWorld* World = GameWorld())
		{
			UAudioMixerBlueprintLibrary::StopRecordingOutput(World, EAudioRecordingExportType::WavFile,
				TEXT("ue-encounter-shout"), FPaths::ConvertRelativePathToFull(FPaths::ProjectDir()));
			bShoutWavWritten = true;
		}
		bShoutRecording = false;
	}

	double GLiveDeedAt = 0.0;
	GameTime GLiveDeedGameAt;
	// THE LIVE ENCOUNTER, SCRIPTED (-LiveScript): the same live phases, with
	// the probe walking where a player would and pressing the same keys
	// through the same input path, so the playable version is also checked
	// by the build. One step counter; nothing else differs. (The flag itself
	// is declared with the clock, which reads it earlier in this file.)
	bool bSheilaMet = false;   // her walk-round is over (day one, beside StartLive)
	LedgerCore::FirstMoments GHints;   // the hints (town list 6y, beside StartLive), saved with the story
	bool bHintsOn = false;
	// -AskAfterDeed (29 September): the scripted talk breaks the window first, as
	// -LiveScript does, and asks once the street holds the deed.
	bool bAskAfterDeed = false;
	bool bLiveFled = false;
	int32 GLiveStep = 0;
	double GLiveStepAt = 0.0;

	int32 TakeTalkRequests()
	{
		if (ALedgerSliceCharacter* Slice = Cast<ALedgerSliceCharacter>(GPawn)) { return Slice->ConsumeTalkRequests(); }
		return 0;
	}

	// HIS MATE, Rocco, in the yard with the lad from the week's end on.
	void RespawnMate(UWorld* World)
	{
		if (GR3Body != nullptr || World == nullptr) { return; }
		// IN FREE PLAY HE KEEPS MICKEY'S DOOR (the cast: "Ron Kirby, who keeps
		// Mickey's door and the rank"; the AI tester, 30 September: in the yard
		// the gap between the houses is shut by crates, so nobody could reach
		// him to answer his envelope): just along from the door, three metres
		// from Sheila, facing the street. The scripted story keeps its yard.
		const double RX = bRitasWindow ? 6.0 : LedgerCrime::kR3X, RZ = bRitasWindow ? 4.0 : LedgerCrime::kR3Z;
		double GY = 0.0;
		std::string On;
		if (!GroundYAt(World, RX, RZ, GY, On)) { GY = 0.1; }
		GR3Body = SpawnBody(World, TEXT("probe_body_r3"), RX, RZ, GY);
		if (bRitasWindow && GR3Body != nullptr) { FaceBody(GR3Body, LedgerCrime::P3(RX, GY, 0.0)); }
		DressBody(World, GR3Body, TEXT("Rocco"));   // names-gate: allow (the asset MH_RoccoT2)
	}

	// THE LAD'S SIGHTING OF THE MAN IN THE YARD, measured off the running
	// world like every witness: in sight long enough to notice, the rung his
	// distance, the light and his acquaintance allow, and the certainty the
	// resolver's own rule gives an actor seen fleeing. Filed only if it could
	// tie the man to anyone (a mark, a face or a name).
	void HintHappened(LedgerCore::Moment M);   // the hints, below StartLive

	void FileFleeSighting(UWorld* World)
	{
		if (GN2Body == nullptr || GPawn == nullptr || !GMill) { GFleeSummary = "no-lad-or-no-mill"; return; }
		LedgerCrime::Reading W = MeasureVantage(World, GIdN2, "flee", GN2Body, nullptr, GFleeSeconds);
		W.Familiarity = LedgerCrime::kLadFamiliarity;
		GFleeMetres = W.ActorMetres;
		bFleeSeen = GFleeSeconds >= Perception::NoticeSeconds
			&& Perception::InSight(W.ActorMetres, W.ActorOffAxisDeg, LedgerCrime::kLightLevel, W.bActorOccluded, 1.4);
		GFleeRung = bFleeSeen ? Perception::IdRung(W.ActorMetres, LedgerCrime::kLightLevel, W.Familiarity, false, W.FaceToward()) : 0;
		if (bFleeSeen) { HintHappened(LedgerCore::Moment::SeenAtDeed); }   // seen running from it (town list 6y)
		const LedgerCore::Slot Got = (LedgerCore::Slot)((int)LedgerCore::Slot::Actor | (int)LedgerCore::Slot::Flight);
		GFleeCertainty = bFleeSeen ? LedgerCore::Observe::CertaintyFor(Got, GFleeRung, true, false) : 0.0;
		// WHO ELSE WAS ABOUT, MEASURED RATHER THAN ASSERTED (the independent
		// check): every other person in the street, by the same sight test
		// from the lad's eye.
		GFleeOthersSeen = 0;
		AActor* Others[2] = { GW1Body, GC1Body };
		const FVector EyeUE = ToUE(W.EyeAt);
		for (AActor* O : Others)
		{
			if (O == nullptr) { continue; }
			const FBox B = O->GetComponentsBoundingBox();
			const FVector HeadUE(B.GetCenter().X, B.GetCenter().Y, B.Max.Z - 10.0f);
			const LedgerCrime::P3 Head = ToStreet(HeadUE);
			std::string Blocker; double Len = 0.0;
			const bool bBlocked = TraceBlocked(World, EyeUE, HeadUE, GN2Body, O, Blocker, Len);
			if (Perception::InSight(LedgerCrime::Metres(W.EyeAt, Head), LedgerCrime::OffAxisDeg(W.EyeAt, W.WitnessYawDeg, Head),
			                        LedgerCrime::kLightLevel, bBlocked, 0.0))
			{
				++GFleeOthersSeen;
			}
		}
		if (!bFleeSeen || !LedgerCrime::CanTieSighting(GFleeRung)) { GFleeSummary = "not-filed/rung-too-low-to-tie"; return; }
		GFleeSummary = GFleeRung >= 3
			? "a man came through the yard at a run just after the glass went, and I'd know his face again"
			: "a man came through the yard at a run just after the glass went";
		// FILED BY HAND, NOT THROUGH Witness(): that writes "I think I saw it,
		// couldn't swear to it", which reads as a sighting of the deed. This is
		// a sighting of the man, and the memory says so. The rumour is the one
		// Witness would add (hop 0, the measured certainty), so gossip carries
		// it and the save keeps it exactly as it keeps any other.
		RumorPtr Near = std::make_shared<Rumor>(Fact(std::string("player"), std::string(LedgerCrime::NearPredicate()),
		                                             std::string(LedgerCrime::NearValue())));
		Near->OriginId = GIdN2;
		Near->OriginRung = GFleeRung;
		Near->Summary = GFleeSummary;
		Near->Confidence = GFleeCertainty;
		Near->Hops = 0;
		if (GN2) { GN2->Rumors.push_back(Near); }
		if (GN2 && GN2->Memory)
		{
			GN2->Memory->Append(MemoryEvent(GNow, "observation", 0.6, "What I saw myself: " + GFleeSummary));
		}
		bFleeFiled = GN2 != nullptr;
		if (GEnc == EEncounter::Live && LedgerCrime::CanNameHim(GFleeRung)) { SawHimNear(GN2, LedgerCrime::kFleeX, LedgerCrime::kFleeZ, GFleeCertainty, GFleeRung); }
	}

	// WHAT ONE RESIDENT HOLDS, AS THE EVIDENCE THE CORE DERIVES SUSPICION
	// FROM (Suspecting.cs, in the helper): the best account of crime A they
	// hold, whether they saw or heard that he was near it, and how they know
	// him. Nobody else was seen near it in this street, so others is 0.
	std::string EvidenceFor(const GossiperPtr& G, double Familiarity, int OwnRungOnA)
	{
		RumorPtr Acc, Near;
		if (G)
		{
			for (const RumorPtr& R : G->Rumors)
			{
				if (!R) { continue; }
				if (LedgerCrime::IsAboutCrimeA(R)) { if (!Acc || R->Confidence > Acc->Confidence) { Acc = R; } }
				else if (R->Content.Predicate == LedgerCrime::NearPredicate() && R->Content.Value == LedgerCrime::NearValue())
				{
					if (!Near || R->Hops < Near->Hops) { Near = R; }
				}
			}
		}
		std::string J = "{\"account\":{";
		// IN PLAY, THE ACCOUNT AS THE CORE READS IT (town list 6n):
		// Suspecting::AccountOf over every copy they hold of the window's story,
		// its rung the one their own look reached, and a heard copy whose first
		// teller recognised him naming him. The regression keeps the account it
		// was measured with, below.
		if (GEnc == EEncounter::Live && G)
		{
			const DeedAccount A = Suspecting::AccountOf(G.get(), "player.broke_a_window");
			if (A.Held)
			{
				J += std::string("\"held\":true,\"seen\":") + (A.SawItMyself ? "true" : "false")
					+ ",\"rung\":" + std::to_string(A.Rung)
					+ ",\"names\":" + (A.NamesHim ? "true" : "false")
					+ ",\"confidence\":" + std::to_string(A.Confidence)
					+ (A.NamesHim ? ",\"namingConfidence\":" + std::to_string(A.NamingConfidence) : std::string())
					+ ",\"summary\":\"" + JsonEsc(A.Summary) + "\"";
			}
			else { J += "\"held\":false"; }
		}
		else if (Acc)
		{
			// THE RUNG, NOT THE CERTAINTY, says whether a first-hand account
			// names him: a sighting is capped at 0.94. A heard account does not
			// carry its teller's rung, so it never names him here.
			J += std::string("\"held\":true,\"seen\":") + (Acc->Hops == 0 ? "true" : "false")
				+ ",\"rung\":" + std::to_string(Acc->Hops == 0 ? OwnRungOnA : -1)
				+ ",\"names\":false"
				+ ",\"confidence\":" + std::to_string(Acc->Confidence)
				+ ",\"summary\":\"" + JsonEsc(Acc->Summary) + "\"";
		}
		else { J += "\"held\":false"; }
		J += "},\"near\":{";
		if (Near)
		{
			// A RETOLD SIGHTING TIES NOBODY unless its teller named him, and
			// the only sighting here is the lad's, who cannot: heard is false.
			J += std::string("\"sawHim\":") + (Near->Hops == 0 ? "true" : "false")
				+ ",\"heard\":false"
				+ ",\"others\":" + std::to_string(Near->Hops == 0 ? GFleeOthersSeen : 0)
				+ ",\"summary\":\"" + JsonEsc(Near->Summary) + "\"";
		}
		J += "},\"familiarity\":" + std::to_string(Familiarity) + "}";
		return J;
	}

	std::string JsonField(const std::string& Line, const std::string& Name)
	{
		const std::string K = "\"" + Name + "\":\"";
		std::string::size_type At = Line.find(K);
		if (At == std::string::npos) { return "none"; }
		std::string R;
		for (std::string::size_type I = At + K.size(); I < Line.size(); ++I)
		{
			if (Line[I] == '\\' && I + 1 < Line.size())
			{
				const char E = Line[++I];
				R += (E == 'n' || E == 'r' || E == 't') ? ' ' : E;
				continue;
			}
			if (Line[I] == '"') { break; }
			R += Line[I];
		}
		return R;
	}

	// THE LIVE TALK WITHOUT STOPPING THE GAME, 24 September. In the playable
	// encounter the helper is started once, when the street is ready, and
	// kept; a line is written when the player talks and the answer is read a
	// little every frame, so the street goes on while the model thinks. The
	// regression keeps its own talk (RunTalk), which waits, because a script
	// has nothing else to do. The helper ends by itself when the game closes
	// its pipe.
	struct FLiveHelper
	{
		FProcHandle Proc;
		void* OutRead = nullptr; void* OutWrite = nullptr; void* InRead = nullptr; void* InWrite = nullptr;
		std::string Buf;
		bool bStarted = false, bReady = false;
		int NextId = 1, PendingId = 0;
		FString PendingName;
		std::string PendingCard;
		AActor* PendingBody = nullptr;
		double AskedAt = 0.0;
		bool bFirstSaid = false;   // the answer's first sentence came early and is being spoken
		std::string PendingSaid;   // the sentence sent to the voice before its check (--pending), this turn
		double FirstAt = 0.0;      // when the answer's first words arrived (-AskScript's measure)
		// THE AI NOTICE, A REPORT, A PAUSE, 29 September (the town session's
		// handovers 6c and 6t): the helper's ready line carries the notice and
		// the report key's label; each reply may say live talk has paused.
		std::string NoticeTitle, NoticeText, ReportLabel;
		bool bNoticeShown = false, bPausedShown = false;
		int LastReplyId = 0;       // the turn R reports
		FString LastReplyName;
		// WALKING OFF MID-REPLY, 29 September (handover 6v): who is answering,
		// what of it has been said so far, and whether his leaving was sent.
		std::string AnswerCard, HeardSoFar;
		AActor* AnswerBody = nullptr;
		bool bWalkedSent = false, bWasNear = false;
		// THE TALK KEPT WITH THE SAVE, 29 September (handover 6r): each save
		// has a stamp, kept in its clock.txt and sent with the talk's own save,
		// so talk stamped for another save is never loaded; a load or a new
		// game is sent once the talk program is ready.
		std::string TalkStamp;
		bool bTalkLoad = false, bTalkReset = false;
		// A CONVERSATION STARTS AND ENDS, 29 September (handover 6ae): whom
		// he has talked to, and who has since been left (out of earshot, or
		// they closed it), so the next line to them starts afresh.
		std::set<std::string> Talked, Left;
		// HOW EACH ONE REGARDS HIM, 29 September (town list 1): the latest
		// StreetVoice::RegardFor for each card, who has had their say on which
		// story, when each last spoke up unasked, and what was said.
		std::map<std::string, StreetVoice::Regard> Regards;
		StreetVoice::RemarkLedger Remarks;
		std::map<std::string, double> LineAt;
		std::map<std::string, int32> SecondLooksSeen;   // the knowing looks already written to the session record
		double RegardAt = 0.0;
		int LinesSaid = 0, FaintSaid = 0, NextLineId = 900000;
	};

	// The named cast's bodies by their cast id (the talk program's "who").
	AActor* CardBody(const std::string& Card)
	{
		return Card == "sam" ? GN2Body : Card == "lena" ? GW1Body : Card == "rocco" ? GR3Body : nullptr;
	}
	FLiveHelper GLive;

	// THE NOTICE, plainly, before the first conversation and on F1: that the
	// street's people answer with an AI, and where typed words go (its text is
	// the helper's own, AiNotice, so the words live in one place).
	void ShowAiNotice()
	{
		if (GLive.NoticeText.empty() || GLive.NoticeText == "none") { return; }
		Say(Un(GLive.NoticeTitle == "none" ? std::string() : GLive.NoticeTitle + ": ") + Un(GLive.NoticeText), 16.0f, FColor(210, 210, 210));
		Say(TEXT("(F1 shows this again. R reports the last reply.)"), 16.0f, FColor(170, 170, 170));
		GLive.bNoticeShown = true;
	}

	// THE LAST REPLY REPORTED, with no note (R, or -AskReport after the
	// scripted first line): the helper keeps it with what was said and
	// answers with its thanks, shown when it comes back.
	void LiveReportLast()
	{
		if (GLive.LastReplyId == 0) { Say(TEXT("Nothing anybody has said to report yet."), 4.0f, FColor(210, 210, 210)); return; }
		const std::string Req = "{\"report\":" + std::to_string(GLive.LastReplyId) + ",\"why\":\"\"}\n";
		FPlatformProcess::WritePipe(GLive.InWrite, Un(Req));
		UE_LOG(LogTemp, Display, TEXT("LedgerTalk: reported turn %d (%s)"), GLive.LastReplyId, *GLive.LastReplyName);
	}

	// NO KEY BUT LEDGER'S OWN, AND ONLY WHILE SOMEBODY PLAYS (Jafar, 29
	// September: nothing in development calls the Anthropic API; the one
	// exception is the characters talking live while he plays, on LEDGER's own
	// key with a hard monthly cap, which no automated tool or workflow may
	// ever use). The talk program's key comes from one place, the live-talk
	// key file (%LOCALAPPDATA%\LEDGER\live-talk-key.txt), which nothing else
	// reads, and only in a run somebody is at: never -unattended, never a
	// scripted run (-LiveScript, -AskScript, -AskAfterDeed, -LookScript), never
	// -TalkFake. Every other run's talk is the stand-in. Either way a key the
	// game was started with is taken out of its environment first, so no talk
	// program inherits one (until 29 September the game, and the play
	// launcher, read another project's key from the game's secrets file).
	bool LiveTalkPlayed()
	{
		const TCHAR* Cmd = FCommandLine::Get();
		int32 AskN = 0;
		return !FParse::Param(Cmd, TEXT("unattended")) && !FParse::Param(Cmd, TEXT("TalkFake"))
		    && !FParse::Param(Cmd, TEXT("LiveScript")) && !FParse::Param(Cmd, TEXT("AskAfterDeed"))
		    && !FParse::Param(Cmd, TEXT("LookScript")) && !FParse::Value(Cmd, TEXT("AskScript="), AskN);
	}

	/// The talk program's key for this run, into the game's environment (the
	/// talk program inherits it) or out of it. True when a key was found for a
	/// played run; a played run without one leaves the talk offline.
	bool TalkKeyForThisRun()
	{
		FPlatformMisc::SetEnvironmentVar(TEXT("ANTHROPIC_API_KEY"), TEXT(""));
		if (!LiveTalkPlayed()) { return false; }
		FString Key;
		const FString Path = FPaths::Combine(FPlatformMisc::GetEnvironmentVariable(TEXT("LOCALAPPDATA")), TEXT("LEDGER"), TEXT("live-talk-key.txt"));
		if (!FFileHelper::LoadFileToString(Key, *Path)) { return false; }
		Key.TrimStartAndEndInline();
		if (Key.IsEmpty()) { return false; }
		FPlatformMisc::SetEnvironmentVar(TEXT("ANTHROPIC_API_KEY"), *Key);
		return true;
	}

	// Which path the talk takes this run: "live-key", "offline" or "stand-in".
	const TCHAR* GTalkPath = TEXT("none");

	void LiveHelperStart()
	{
		if (GLive.bStarted) { return; }
		FString Exe;
		if (!FParse::Value(FCommandLine::Get(), TEXT("TalkHelper="), Exe) || Exe.IsEmpty())
		{
			// THE TALK PROGRAM SHIPPED WITH THE GAME, 29 September (handover
			// 6aa): with none named, the game's own copy beside it
			// (tools/publish-talk-helper.ps1, published into the package by
			// the build): LedgerTalk.exe, needing no .NET, its cards beside it.
			// Only in the live encounter, where talk is played.
			// Never for a run nobody is at: the build machine's and the
			// scripts' runs pass -unattended, and must not make paid calls
			// unasked; they name their talk program when they want one.
			if (GEnc != EEncounter::Live || FParse::Param(FCommandLine::Get(), TEXT("unattended"))) { return; }
			const FString Cands[2] = { FPaths::Combine(FPaths::ProjectDir(), TEXT("../LedgerTalk/LedgerTalk.exe")),
			                           FPaths::Combine(FPaths::ProjectDir(), TEXT("LedgerTalk/LedgerTalk.exe")) };
			for (FString C : Cands)
			{
				C = FPaths::ConvertRelativePathToFull(C);
				FPaths::CollapseRelativeDirectories(C);
				if (FPaths::FileExists(C)) { Exe = C; break; }
			}
			if (Exe.IsEmpty()) { return; }
			UE_LOG(LogTemp, Display, TEXT("LedgerTalk: the game's own talk program, %s"), *Exe);
		}
		if (!FPlatformProcess::CreatePipe(GLive.OutRead, GLive.OutWrite) || !FPlatformProcess::CreatePipe(GLive.InRead, GLive.InWrite, true)) { return; }
		// --early (26 September; Jafar: about six seconds passed between his line
		// and the character speaking): the helper sends the answer's first
		// sentence the moment it is written and has passed its own check for
		// invented details, and the rest after; LiveHelperPump speaks each.
		// THE KEY, OR THE STAND-IN (29 September, above): a played run's talk is
		// real on LEDGER's own key, every other run's is the stand-in.
		const bool bPlayed = LiveTalkPlayed();
		const bool bKey = TalkKeyForThisRun();
		GTalkPath = !bPlayed ? TEXT("stand-in") : bKey ? TEXT("live-key") : TEXT("offline");
		UE_LOG(LogTemp, Display, TEXT("LedgerTalk: %s"), !bPlayed ? TEXT("the stand-in (a scripted or unattended run)")
			: bKey ? TEXT("live, on LEDGER's own key") : TEXT("offline: no live-talk key file"));
		// --pending (item 2, the delay; talk-protocol.md): the first sentence also
		// comes the moment it is written, before its check, so the voice can make
		// it while it is checked; it is played only if the checked words match.
		GLive.Proc = FPlatformProcess::CreateProc(*Exe, bPlayed ? TEXT("--early --pending") : TEXT("--fake --early --pending"),
			false, true, true, nullptr, 0, nullptr, GLive.OutWrite, GLive.InRead);
		GLive.bStarted = GLive.Proc.IsValid();
	}

	// THE CAST SPEAKS, 24 September: each answer is also sent to the voice
	// server beside the game (tools/voice-live/voice-server.py), which speaks
	// it in the character's cast voice and hands back a sound file; the game
	// plays it where they stand. Started only when the command line names the
	// voice's Python and script; without them the answers stay text.
	struct FLiveVoice
	{
		FProcHandle Proc;
		void* OutRead = nullptr; void* OutWrite = nullptr; void* InRead = nullptr; void* InWrite = nullptr;
		std::string Buf;
		bool bStarted = false, bReady = false;
		TMap<int32, TWeakObjectPtr<AActor>> Pending;   // line id -> who says it
		// SENTENCE BY SENTENCE: each piece is queued as it arrives and played
		// when the one before it has finished, so the first sentence is heard
		// while the rest are still being made.
		// A PIECE THAT CONTINUES THE ONE BEFORE ("joined", 26 September): a voice
		// that streams (tools/voice-live/pocket-server.py) sends a sentence in
		// pieces as its sound is made; each is added to the sound already
		// playing, with no gap, and the usual pause is left only between
		// sentences.
		struct FPiece { FString Wav; TWeakObjectPtr<AActor> Who; bool bJoined = false; int32 Id = 0; };
		// THE SENTENCE MADE BEFORE ITS CHECK (--pending, item 2, the delay): its
		// pieces wait here until the checked first sentence arrives with the same
		// words (released to the queue) or the turn goes another way (dropped,
		// and any of its pieces still to come are thrown away on arrival).
		TSet<int32> HeldIds, DroppedIds;
		TArray<FPiece> Held;
		TArray<FPiece> Queue;
		double BusyUntil = 0.0;
		bool bLastIn = false;
		TWeakObjectPtr<UAudioComponent> Playing;
		TWeakObjectPtr<USoundWaveProcedural> PlayingWave;
		double PlayingEnd = 0.0;
		// THE MOUTH'S COPY OF WHAT IS PLAYING (MouthTick): the samples queued
		// on the wave, and how many bytes, so the part being heard is known
		// from what the mixer has taken; and whose face it is.
		TArray<int16> Pcm;
		int32 PcmRate = 24000, PcmChannels = 1;
		int64 QueuedBytes = 0;
		TWeakObjectPtr<AActor> Speaker, LastSpeaker;
		double SpeakerQuietSince = -1.0;
		float PeakDb = -30.0f;   // the sentence's speaking level (MouthLevelFrom)
		TArray<float> WindowDb;  // every 40 ms of it, for that level
	};
	FLiveVoice GVoice;
	bool bVoiceAsked = false, bVoicePlayed = false, bVoiceRecording = false, bVoiceAllIn = false;
	double GVoiceSeconds = 0.0, GVoiceAskedAt = 0.0, GVoicePlayedAt = 0.0;
	double GVoiceStartedAt = 0.0;   // when the latest sentence's sound began to play
	// ONE LINE, END TO END (Jafar's list after the audit, item 2): from his
	// Enter to the reply's first words, to its first sentence handed to the
	// voice, to the first sound of it heard, one record a reply ("heard" in
	// the session record, and a LedgerTiming log line), marked with the path
	// the talk took: live on LEDGER's key, offline, or the stand-in.
	double GEnterAt = 0.0, GTimedWordsAt = 0.0, GTimedVoiceAskedAt = 0.0;
	// THE VOICE'S OWN SHARE, SPLIT (item 2, the delay): when the first
	// sentence's sound file came back from the voice server, how long the
	// server says it worked on it ("ms"), and how long the sound is.
	int32 GTimedVoiceId = -1;
	double GTimedPieceAt = 0.0, GTimedPieceWorkS = -1.0, GTimedPieceLenS = -1.0;
	bool bAwaitFirstSound = false;
	std::string GTimedCard;
	const TCHAR* TalkPathName();

	const TCHAR* TalkPathName() { return GTalkPath; }

	void LiveVoiceStart()
	{
		if (GVoice.bStarted) { return; }
		FString Py, Script;
		if (!FParse::Value(FCommandLine::Get(), TEXT("VoicePython="), Py) || !FParse::Value(FCommandLine::Get(), TEXT("VoiceScript="), Script))
		{
			// THE VOICE BESIDE THE GAME, 30 September (item 3's stopgap for a
			// friends' build, Jafar's ruling): a folder "Voice" next to the game
			// holding today's voice program with its own Python, torch and
			// weights (tools/voice-live, made portable), started with its own
			// paths, so a PC with nothing installed hears the cast. -NoVoice
			// leaves it off.
			const FString Voice = FPaths::ConvertRelativePathToFull(FPaths::Combine(FPaths::RootDir(), TEXT("Voice")));
			Py = Voice / TEXT("python/python.exe");
			Script = Voice / TEXT("tools/voice-live/voice-server.py");
			if (FParse::Param(FCommandLine::Get(), TEXT("NoVoice")) || !FPaths::FileExists(Py) || !FPaths::FileExists(Script)) { return; }
			FPlatformMisc::SetEnvironmentVar(TEXT("NANO_PKG"), *(Voice / TEXT("nano/src-master/src")));
			FPlatformMisc::SetEnvironmentVar(TEXT("NANO_WEIGHTS"), *(Voice / TEXT("nano/weights")));
			FPlatformMisc::SetEnvironmentVar(TEXT("NANO_VOICE_CACHE"), *(Voice / TEXT("nano/voice-cache")));
			FPlatformMisc::SetEnvironmentVar(TEXT("PYTHONNOUSERSITE"), TEXT("1"));
			const FString Path = FPlatformMisc::GetEnvironmentVariable(TEXT("PATH"));
			FPlatformMisc::SetEnvironmentVar(TEXT("PATH"), *(FPaths::ConvertRelativePathToFull(Voice / TEXT("python")) + TEXT(";")
				+ FPaths::ConvertRelativePathToFull(Voice / TEXT("python/Library/bin")) + TEXT(";") + Path));
			UE_LOG(LogTemp, Display, TEXT("LedgerVoice: the voice beside the game, %s"), *Voice);
		}
		GVoice.bStarted = true;   // one try, whatever happens
		if (!FPlatformProcess::CreatePipe(GVoice.OutRead, GVoice.OutWrite) || !FPlatformProcess::CreatePipe(GVoice.InRead, GVoice.InWrite, true)) { return; }
		// --prewarm: the cast voices are learned and run once before the server
		// says it is ready, not on the first line said to each (26 September).
		GVoice.Proc = FPlatformProcess::CreateProc(*Py, *FString::Printf(TEXT("\"%s\" --prewarm"), *Script), false, true, true,
			nullptr, 0, nullptr, GVoice.OutWrite, GVoice.InRead);
	}

	// The sound in a WAV the server wrote (16-bit PCM, soundfile's own header).
	bool ReadVoiceWav(const FString& Path, TArray<uint8>& Bytes, int32& Rate, int32& Channels, int32& DataAt, int32& DataLen)
	{
		Rate = 24000; Channels = 1; DataAt = -1; DataLen = 0;
		if (!FFileHelper::LoadFileToArray(Bytes, *Path) || Bytes.Num() < 44) { return false; }
		for (int32 I = 12; I + 8 <= Bytes.Num();)
		{
			const int32 Len = Bytes[I + 4] | (Bytes[I + 5] << 8) | (Bytes[I + 6] << 16) | (Bytes[I + 7] << 24);
			if (FMemory::Memcmp(&Bytes[I], "fmt ", 4) == 0 && I + 16 <= Bytes.Num())
			{
				Channels = Bytes[I + 10] | (Bytes[I + 11] << 8);
				Rate = Bytes[I + 12] | (Bytes[I + 13] << 8) | (Bytes[I + 14] << 16) | (Bytes[I + 15] << 24);
			}
			if (FMemory::Memcmp(&Bytes[I], "data", 4) == 0) { DataAt = I + 8; DataLen = FMath::Min(Len, Bytes.Num() - DataAt); break; }
			I += 8 + Len + (Len & 1);
		}
		return DataAt >= 0 && DataLen > 0;
	}

	// THE SENTENCE'S SPEAKING LEVEL, from every 40 ms of it queued so far: the
	// loudness four in five of its sounding windows stay under. Scaled to its
	// loudest single moment instead, Ron's quiet "Quiet one today." kept his
	// mouth shut under one loud spot (the reviewer, 30 September); on one
	// fixed scale Darren's quieter voice barely parted his lips.
	void MouthLevelFrom(int32 From)
	{
		const int32 Ch = FMath::Max(1, GVoice.PcmChannels);
		const int32 Span = FMath::Max(1, (int32)(0.04 * GVoice.PcmRate)) * Ch;
		for (int32 A = From; A + Span <= GVoice.Pcm.Num(); A += Span)
		{
			double Sum = 0.0;
			for (int32 S = A; S < A + Span; S += Ch) { const double V = GVoice.Pcm[S] / 32768.0; Sum += V * V; }
			GVoice.WindowDb.Add(10.0f * FMath::LogX(10.0f, (float)(Sum / (Span / Ch)) + 1e-12f));
		}
		TArray<float> Sounding;
		for (float D : GVoice.WindowDb) { if (D > -60.0f) { Sounding.Add(D); } }
		if (Sounding.Num() == 0) { return; }
		Sounding.Sort();
		GVoice.PeakDb = Sounding[FMath::Min(Sounding.Num() - 1, (int32)(Sounding.Num() * 0.8f))];
	}

	// A PIECE THAT CONTINUES the sound still playing: its sound is added to the
	// same wave, so there is no gap. Its length, or 0 if nothing is playing.
	double ContinueVoiceFile(const FString& Path)
	{
		TArray<uint8> Bytes;
		int32 Rate, Channels, DataAt, DataLen;
		if (!GVoice.PlayingWave.IsValid() || !GVoice.Playing.IsValid() || !ReadVoiceWav(Path, Bytes, Rate, Channels, DataAt, DataLen)) { return 0.0; }
		GVoice.PlayingWave->QueueAudio(&Bytes[DataAt], DataLen);
		const int32 Was = GVoice.Pcm.Num();
		GVoice.Pcm.Append(reinterpret_cast<const int16*>(&Bytes[DataAt]), DataLen / 2);
		GVoice.QueuedBytes += DataLen;
		MouthLevelFrom(Was);
		const double Len = (double)DataLen / (double)(2 * Channels * Rate);
		GVoiceSeconds += Len;
		return Len;
	}

	// A WAV THE SERVER WROTE, played as a procedural wave at the speaker, with
	// the shout's falloff. The wave plays until LiveVoicePump stops it at the
	// end of its sound, so a streaming voice's later pieces can be added to it.
	double PlayVoiceFile(const FString& Path, AActor* Who)
	{
		UWorld* World = GameWorld();
		TArray<uint8> Bytes;
		int32 Rate, Channels, DataAt, DataLen;
		if (World == nullptr || Who == nullptr || !ReadVoiceWav(Path, Bytes, Rate, Channels, DataAt, DataLen)) { return 0.0; }
		USoundWaveProcedural* W = NewObject<USoundWaveProcedural>(GetTransientPackage());
		W->SetSampleRate(Rate);
		W->NumChannels = Channels;
		W->Duration = INDEFINITELY_LOOPING_DURATION;
		W->bLooping = false;
		const float Seconds = (float)DataLen / (float)(2 * Channels * Rate);
		W->QueueAudio(&Bytes[DataAt], DataLen);
		USoundAttenuation* Att = NewObject<USoundAttenuation>(GetTransientPackage());
		Att->Attenuation.bAttenuate = true;
		Att->Attenuation.bSpatialize = true;
		Att->Attenuation.AttenuationShapeExtents = FVector(300.0f, 0.0f, 0.0f);
		Att->Attenuation.FalloffDistance = 2500.0f;
		GVoice.Playing = UGameplayStatics::SpawnSoundAtLocation(World, W, Who->GetActorLocation() + FVector(0.0f, 0.0f, 160.0f),
			FRotator::ZeroRotator, 1.0f, 1.0f, 0.0f, Att);
		GVoice.PlayingWave = W;
		GVoice.Pcm.Reset();
		GVoice.Pcm.Append(reinterpret_cast<const int16*>(&Bytes[DataAt]), DataLen / 2);
		GVoice.PcmRate = Rate;
		GVoice.PcmChannels = FMath::Max(1, Channels);
		GVoice.QueuedBytes = DataLen;
		GVoice.Speaker = Who;
		GVoice.PeakDb = -30.0f;
		GVoice.WindowDb.Reset();
		MouthLevelFrom(0);
		GVoiceStartedAt = NowS();
		if (bAwaitFirstSound && GEnterAt > 0.0)
		{
			bAwaitFirstSound = false;
			const double Words = GTimedWordsAt - GEnterAt, Asked = GTimedVoiceAskedAt - GEnterAt, Sound = GVoiceStartedAt - GEnterAt;
			const double Arrived = GTimedPieceAt > 0.0 ? GTimedPieceAt - GEnterAt : -1.0;
			LedgerSession::Write(TEXT("heard"), TEXT("\"who\":") + LedgerSession::Str(Un(GTimedCard)) + TEXT(",\"path\":") + LedgerSession::Str(TalkPathName())
				+ FString::Printf(TEXT(",\"enterToWords\":%.2f,\"enterToVoiceAsked\":%.2f,\"enterToSound\":%.2f,\"enterToPiece\":%.2f,\"voiceWork\":%.2f,\"pieceSeconds\":%.2f"),
					Words, Asked, Sound, Arrived, GTimedPieceWorkS, GTimedPieceLenS));
			UE_LOG(LogTemp, Display, TEXT("LedgerTiming: %s (%s) Enter to words %.2f s, to the voice asked %.2f s, to its sound file %.2f s (made in %.2f s, %.2f s long), to first sound %.2f s"),
				*Un(GTimedCard), TalkPathName(), Words, Asked, Arrived, GTimedPieceWorkS, GTimedPieceLenS, Sound);
		}
		if (!bVoicePlayed)
		{
			GVoicePlayedAt = NowS();
			// THE SCRIPTED RUN KEEPS WHAT THE STREET HEARD, so the voice can
			// be listened to rather than only counted.
			if (bLiveScript && World->GetAudioDevice().IsValid())
			{
				UAudioMixerBlueprintLibrary::StartRecordingOutput(World, 40.0f);
				bVoiceRecording = true;
			}
		}
		bVoicePlayed = true;
		GVoiceSeconds += Seconds;
		return Seconds;
	}

	std::string JsonField(const std::string& Line, const std::string& Name);

	// THE MOUTH FOLLOWS THE VOICE, 30 September (the twenty a friend would
	// notice, 12: lips roughly in time; the faces stood still while they
	// spoke). The part of the answer being heard is what the mixer has taken
	// from the wave, less about 30 ms still in its buffers; its loudness over
	// 40 ms, against the sentence's own speaking level (MouthLevelFrom), opens the speaker's jaw and
	// shapes their lips (ULedgerPersonAnim::SpeakTick), on every part of them
	// that plays our animation, so the face and body agree. When they stop,
	// the mouth eases back to the idle over a second.
	void MouthApply(AActor* Who, float Level, bool bSpeaking, float Dt)
	{
		if (Who == nullptr) { return; }
		TArray<USkeletalMeshComponent*> Parts;
		Who->GetComponents(Parts);
		for (USkeletalMeshComponent* C : Parts)
		{
			if (ULedgerPersonAnim* A = C != nullptr ? Cast<ULedgerPersonAnim>(C->GetAnimInstance()) : nullptr)
			{
				A->SpeakTick(Level, bSpeaking, Dt);
				// WHAT THE FACE IS DOING while it speaks, once a second for the
				// first twenty: Darren's stayed frozen at every level (the
				// reviewer, 30 September) though his face is set up as the others'.
				static TMap<FString, double> NextFaceLog;
				static int32 FaceLogs = 0;
				if (bSpeaking && C->GetName() == TEXT("Face") && FaceLogs < 20)
				{
					double& Next = NextFaceLog.FindOrAdd(Who->GetName());
					if (NowS() >= Next)
					{
						Next = NowS() + 1.0;
						++FaceLogs;
						UE_LOG(LogTemp, Log, TEXT("LedgerMouth: %s face at LOD %d, weight %.2f, jaw %.2f, anim ticks %s, visible %s"),
							*Who->GetName(), C->GetPredictedLODLevel(), A->SpeakWeight, A->MouthValues[0],
							C->bEnableUpdateRateOptimizations ? TEXT("with rate optimisation") : TEXT("every frame"),
							C->IsVisible() ? TEXT("yes") : TEXT("no"));
					}
				}
			}
		}
	}

	// -MouthFilm, 30 September: while someone speaks, their face filmed from
	// 60 cm, a frame every tenth of a second (Saved/MouthFilm/<who>), so the
	// mouth can be judged against the words, not guessed from a distance;
	// the player's own view comes back when they stop.
	struct FMouthFilm { TWeakObjectPtr<ACameraActor> Cam; double LastFrame = 0.0; int32 Frame = 0; bool bOn = false; };
	FMouthFilm GMouthFilm;

	void MouthFilmTick(UWorld* World, AActor* Who, bool bSpeaking)
	{
		static const bool bWanted = FParse::Param(FCommandLine::Get(), TEXT("MouthFilm"));
		if (!bWanted || World == nullptr) { return; }
		APlayerController* PC = World->GetFirstPlayerController();
		if (!bSpeaking || Who == nullptr)
		{
			if (GMouthFilm.bOn && PC != nullptr && PC->GetPawn() != nullptr) { PC->SetViewTargetWithBlend(PC->GetPawn(), 0.0f); }
			GMouthFilm.bOn = false;
			return;
		}
		FVector Head = Who->GetActorLocation() + FVector(0.0f, 0.0f, 160.0f);
		TArray<USkeletalMeshComponent*> Parts;
		Who->GetComponents(Parts);
		for (USkeletalMeshComponent* C : Parts) { if (C != nullptr && C->DoesSocketExist(TEXT("head"))) { Head = C->GetSocketLocation(TEXT("head")); break; } }
		// In front of the face: a MetaHuman faces its actor's +Y (SyncVisual).
		const FVector Toward = Who->GetActorRightVector().GetSafeNormal2D();
		// -MouthFilmWide: the whole person from 2.6 m instead, for what they wear.
		static const bool bWide = FParse::Param(FCommandLine::Get(), TEXT("MouthFilmWide"));
		const FVector Feet = Who->GetActorLocation();
		const FVector Look = bWide ? Feet + FVector(0.0f, 0.0f, 90.0f) : Head + FVector(0.0f, 0.0f, 2.0f);
		// The first way round him with nothing in between (Ron stands facing
		// the yard wall): in front, then to either side, then behind.
		FVector Dir = Toward;
		float Dist = 260.0f;
		if (bWide)
		{
			// Twelve ways round, nearest the front first, at 2.6 m, 2 m then
			// 1.6 m: Ron's yard is cramped.
			bool bFound = false;
			for (float Try : { 260.0f, 200.0f, 160.0f })
			{
				for (int32 K = 0; K < 12 && !bFound; ++K)
				{
					const float Deg = (K % 2 == 0 ? 1.0f : -1.0f) * 30.0f * ((K + 1) / 2);
					const FVector D = Toward.RotateAngleAxis(Deg, FVector::UpVector);
					FHitResult Hit;
					FCollisionQueryParams Q(TEXT("LedgerMouthFilm"), true, Who);
					if (!World->SweepSingleByChannel(Hit, Look, Feet + D * Try + FVector(0.0f, 0.0f, 100.0f), FQuat::Identity, ECC_Camera, FCollisionShape::MakeSphere(15.0f), Q))
					{
						Dir = D; Dist = Try; bFound = true;
					}
				}
				if (bFound) { break; }
			}
		}
		const FVector Eye = bWide ? Feet + Dir * Dist + FVector(0.0f, 0.0f, 100.0f) : Head + Toward * 60.0f + FVector(0.0f, 0.0f, 2.0f);
		if (!GMouthFilm.Cam.IsValid())
		{
			FActorSpawnParameters P;
			P.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
			GMouthFilm.Cam = World->SpawnActor<ACameraActor>(Eye, (Look - Eye).Rotation(), P);
		}
		if (!GMouthFilm.Cam.IsValid()) { return; }
		GMouthFilm.Cam->SetActorLocationAndRotation(Eye, (Look - Eye).Rotation());
		if (!GMouthFilm.bOn && PC != nullptr) { PC->SetViewTargetWithBlend(GMouthFilm.Cam.Get(), 0.0f); GMouthFilm.bOn = true; }
		const double T = FPlatformTime::Seconds();
		if (T - GMouthFilm.LastFrame >= 0.099 && GMouthFilm.Frame < 400)
		{
			GMouthFilm.LastFrame = T;
			FScreenshotRequest::RequestScreenshot(FPaths::ConvertRelativePathToFull(FPaths::ProjectSavedDir()
				/ TEXT("MouthFilm") / Who->GetName() / FString::Printf(TEXT("f_%03d.png"), GMouthFilm.Frame++)), false, false);
		}
	}

	// THE THINKING SOUND'S MOUTH, 30 September: its own face animation used
	// to replace the face's (a single-node animation, for good), so after the
	// first "Let me think." Darren's and Ron's faces neither spoke nor turned
	// (the reviewer: Darren's mouth frozen; Ron's shut for half his answer).
	// Now a face that plays our animation keeps it, and its mouth follows the
	// thinking sound's audio as it follows an answer's.
	struct FAckMouth { TArray<int16> Pcm; int32 Rate = 24000, Ch = 1; int64 Queued = 0; float RefDb = -30.0f;
	                   TWeakObjectPtr<USoundWaveProcedural> Wave; TWeakObjectPtr<AActor> Who; };
	FAckMouth GAckMouth;

	// The speaking level of a whole clip: the loudness four in five of its
	// sounding 40 ms windows stay under (as MouthLevelFrom).
	float ClipSpeakingDb(const TArray<int16>& Pcm, int32 Rate, int32 Ch)
	{
		const int32 Span = FMath::Max(1, (int32)(0.04 * Rate)) * Ch;
		TArray<float> Sounding;
		for (int32 A = 0; A + Span <= Pcm.Num(); A += Span)
		{
			double Sum = 0.0;
			for (int32 S = A; S < A + Span; S += Ch) { const double V = Pcm[S] / 32768.0; Sum += V * V; }
			const float D = 10.0f * FMath::LogX(10.0f, (float)(Sum / (Span / Ch)) + 1e-12f);
			if (D > -60.0f) { Sounding.Add(D); }
		}
		if (Sounding.Num() == 0) { return -30.0f; }
		Sounding.Sort();
		return Sounding[FMath::Min(Sounding.Num() - 1, (int32)(Sounding.Num() * 0.8f))];
	}

	// The loudness of the part being heard, 0 to 1 against the clip's speaking level.
	float HeardLevel(const TArray<int16>& Pcm, int32 Rate, int32 Ch, int64 Queued, USoundWaveProcedural* Wave, float RefDb, float& OutDb, int64& OutHeard)
	{
		const int64 Taken = Queued - Wave->GetAvailableAudioByteCount();
		OutHeard = Taken / (2 * Ch) - (int64)(0.03 * Rate);
		const int64 Span = (int64)(0.04 * Rate);
		double Sum = 0.0;
		int64 N = 0;
		for (int64 S = FMath::Max<int64>(0, OutHeard - Span); S < OutHeard && S * Ch < Pcm.Num(); ++S)
		{
			const double V = Pcm[S * Ch] / 32768.0;
			Sum += V * V;
			++N;
		}
		OutDb = N > 0 ? 10.0f * FMath::LogX(10.0f, (float)(Sum / N) + 1e-12f) : -120.0f;
		return FMath::Clamp((OutDb - (RefDb - 24.0f)) / 24.0f, 0.0f, 1.0f);
	}

	void MouthTick()
	{
		const float Dt = (float)FApp::GetDeltaTime();
		// THE THINKING SOUND, while no answer is playing.
		const bool bAnswer = GVoice.Playing.IsValid() && GVoice.PlayingWave.IsValid();
		if (!bAnswer && GAckMouth.Wave.IsValid() && GAckMouth.Who.IsValid() && GAckMouth.Pcm.Num() > 0)
		{
			float Db = -120.0f;
			int64 Heard = 0;
			const float Level = HeardLevel(GAckMouth.Pcm, GAckMouth.Rate, GAckMouth.Ch, GAckMouth.Queued, GAckMouth.Wave.Get(), GAckMouth.RefDb, Db, Heard);
			MouthApply(GAckMouth.Who.Get(), Level, true, Dt);
			GVoice.LastSpeaker = GAckMouth.Who;
			GVoice.SpeakerQuietSince = -1.0;
			return;
		}
		const bool bPlaying = GVoice.Playing.IsValid() && GVoice.PlayingWave.IsValid() && GVoice.Speaker.IsValid() && GVoice.Pcm.Num() > 0;
		MouthFilmTick(GameWorld(), GVoice.Speaker.Get(), bPlaying);
		if (!bPlaying)
		{
			if (GVoice.LastSpeaker.IsValid())
			{
				MouthApply(GVoice.LastSpeaker.Get(), 0.0f, false, Dt);
				if (GVoice.SpeakerQuietSince < 0.0) { GVoice.SpeakerQuietSince = NowS(); }
				if (NowS() - GVoice.SpeakerQuietSince > 1.0) { GVoice.LastSpeaker = nullptr; }
			}
			return;
		}
		if (GVoice.LastSpeaker.IsValid() && GVoice.LastSpeaker != GVoice.Speaker) { MouthApply(GVoice.LastSpeaker.Get(), 0.0f, false, Dt); }
		GVoice.LastSpeaker = GVoice.Speaker;
		GVoice.SpeakerQuietSince = -1.0;
		float Db = -120.0f;
		int64 Heard = 0;
		// Open fully at the sentence's speaking level, shut 24 dB below it.
		const float Level = HeardLevel(GVoice.Pcm, GVoice.PcmRate, GVoice.PcmChannels, GVoice.QueuedBytes, GVoice.PlayingWave.Get(), GVoice.PeakDb, Db, Heard);
		MouthApply(GVoice.Speaker.Get(), Level, true, Dt);
		// A LINE A FIFTH OF A SECOND for the first sixty, so a run shows the
		// mouth following the words.
		static double NextLog = 0.0;
		static int32 Logged = 0;
		if (Logged < 60 && NowS() >= NextLog)
		{
			NextLog = NowS() + 0.2;
			++Logged;
			UE_LOG(LogTemp, Log, TEXT("LedgerMouth: %s at %.2f s of the answer, %.0f dB, level %.2f"), *GVoice.Speaker->GetName(),
				(double)FMath::Max<int64>(0, Heard) / GVoice.PcmRate, Db, Level);
		}
	}

	void LiveVoicePump()
	{
		if (!GVoice.bStarted || GVoice.OutRead == nullptr) { return; }
		GVoice.Buf += Utf8(FPlatformProcess::ReadPipe(GVoice.OutRead));
		std::string::size_type Nl;
		while ((Nl = GVoice.Buf.find('\n')) != std::string::npos)
		{
			const std::string L = GVoice.Buf.substr(0, Nl);
			GVoice.Buf.erase(0, Nl + 1);
			if (L.find("\"ready\"") != std::string::npos) { GVoice.bReady = true; continue; }
			const std::string::size_type At = L.find("\"id\":");
			if (At == std::string::npos) { continue; }
			const int32 Id = atoi(L.c_str() + At + 5);
			TWeakObjectPtr<AActor>* Who = GVoice.Pending.Find(Id);
			const std::string Wav = JsonField(L, "wav");
			const bool bLast = L.find("\"last\":true") != std::string::npos || L.find("\"error\"") != std::string::npos;
			if (Id == GTimedVoiceId && GTimedPieceAt <= 0.0 && Wav != "none")
			{
				GTimedPieceAt = NowS();
				// Numbers, not strings: read after their key.
				auto Num = [&L](const char* Key) -> double {
					const std::string K = std::string("\"") + Key + "\":";
					const std::string::size_type P = L.find(K);
					return P == std::string::npos ? -1.0 : atof(L.c_str() + P + K.size());
				};
				const double Ms = Num("ms");
				GTimedPieceWorkS = Ms >= 0.0 ? Ms / 1000.0 : -1.0;
				GTimedPieceLenS = Num("seconds");
			}
			if (Who != nullptr && Wav != "none" && !GVoice.DroppedIds.Contains(Id))
			{
				FLiveVoice::FPiece Piece;
				Piece.Wav = Un(Wav);
				Piece.Who = *Who;
				Piece.bJoined = L.find("\"joined\":true") != std::string::npos;
				Piece.Id = Id;
				if (GVoice.HeldIds.Contains(Id)) { GVoice.Held.Add(Piece); }
				else { GVoice.Queue.Add(Piece); }
			}
			if (bLast) { GVoice.Pending.Remove(Id); bVoiceAllIn = true; }
		}
		const double Now = NowS();
		// A continuing piece goes straight onto the sound still playing.
		while (GVoice.Queue.Num() > 0 && GVoice.Queue[0].bJoined && GVoice.Playing.IsValid())
		{
			const double Len = ContinueVoiceFile(GVoice.Queue[0].Wav);
			GVoice.Queue.RemoveAt(0);
			GVoice.PlayingEnd = FMath::Max(GVoice.PlayingEnd, Now) + Len;
			GVoice.BusyUntil = GVoice.PlayingEnd + 0.15;
		}
		// The wave ends when its sound has; a streaming one gets a moment's grace for its next piece.
		if (GVoice.Playing.IsValid() && Now > GVoice.PlayingEnd + 0.12)
		{
			GVoice.Playing->Stop();
			GVoice.Playing = nullptr;
			GVoice.PlayingWave = nullptr;
		}
		if (GVoice.Queue.Num() > 0 && Now >= GVoice.BusyUntil)
		{
			FLiveVoice::FPiece Next = GVoice.Queue[0];
			GVoice.Queue.RemoveAt(0);
			if (Next.Who.IsValid())
			{
				if (GVoice.Playing.IsValid()) { GVoice.Playing->Stop(); }
				const double Len = PlayVoiceFile(Next.Wav, Next.Who.Get());
				GVoice.PlayingEnd = Now + Len;
				GVoice.BusyUntil = Now + Len + 0.15;
			}
		}
		MouthTick();
	}

	// THE PAUSE, COVERED (28 September; production/research/live-speech-
	// architecture/conversation-latency-2026-09-25.md: "pre-render several
	// character-specific breaths, 'Hmm' and brief acknowledgements; pair them
	// with gaze shifts ... Never force a filler to finish when the answer is
	// ready"; loading signs did not help). When a line is put to someone, one
	// of their own short sounds (content/voice/acks/<card>/*.wav, in their
	// approved voice, none of them agreeing to anything) plays at once where
	// they stand, with its face animation when one has been made
	// (/Game/Ledger/MetaHumans/Speech/AS_ack_<card>_<name>), and is cut off the
	// moment the answer's own sound begins. -NoAck leaves the pause bare.
	struct FAck
	{
		TWeakObjectPtr<UAudioComponent> Sound;
		TWeakObjectPtr<USkeletalMeshComponent> Face;
		TWeakObjectPtr<UAnimationAsset> FaceIdle;
		float FaceIdleAt = 0.0f;
		double Until = 0.0;
	};
	FAck GAck;
	int32 GAckTurn = 0;

	TArray<FString> AckFiles(const std::string& Card)
	{
		const FString Rel = FString(TEXT("content/voice/acks/")) + Un(Card);
		for (const FString& Dir : { FPaths::Combine(FPaths::ProjectDir(), TEXT(".."), Rel),
		                            FPaths::Combine(FPaths::ProjectContentDir(), TEXT("LedgerData"), Rel) })
		{
			TArray<FString> Found;
			IFileManager::Get().FindFiles(Found, *FPaths::Combine(Dir, TEXT("*.wav")), true, false);
			if (Found.Num() == 0) { continue; }
			Found.Sort();
			for (FString& F : Found) { F = FPaths::Combine(Dir, F); }
			return Found;
		}
		return TArray<FString>();
	}

	void AckEnd(bool bCut)
	{
		GAckMouth = FAckMouth();
		if (GAck.Sound.IsValid()) { GAck.Sound->Stop(); }
		if (GAck.Face.IsValid() && GAck.FaceIdle.IsValid())
		{
			GAck.Face->PlayAnimation(GAck.FaceIdle.Get(), true);
			GAck.Face->SetPosition(GAck.FaceIdleAt, false);
		}
		if (GAck.Sound.IsValid() || GAck.Face.IsValid()) { UE_LOG(LogTemp, Display, TEXT("LedgerAck: %s"), bCut ? TEXT("cut off by the answer") : TEXT("done")); }
		GAck = FAck();
	}

	void AckStart(const std::string& Card, AActor* Who)
	{
		static const bool bNo = FParse::Param(FCommandLine::Get(), TEXT("NoAck"));
		UWorld* World = GameWorld();
		AckEnd(true);
		if (bNo || World == nullptr || Who == nullptr) { return; }
		const TArray<FString> Files = AckFiles(Card);
		TArray<uint8> Bytes;
		int32 Rate, Channels, DataAt, DataLen;
		if (Files.Num() == 0) { UE_LOG(LogTemp, Display, TEXT("LedgerAck: none for %s"), *Un(Card)); return; }
		const FString Wav = Files[GAckTurn++ % Files.Num()];
		if (!ReadVoiceWav(Wav, Bytes, Rate, Channels, DataAt, DataLen)) { return; }
		USoundWaveProcedural* W = NewObject<USoundWaveProcedural>(GetTransientPackage());
		W->SetSampleRate(Rate);
		W->NumChannels = Channels;
		W->Duration = INDEFINITELY_LOOPING_DURATION;
		W->bLooping = false;
		W->QueueAudio(&Bytes[DataAt], DataLen);
		USoundAttenuation* Att = NewObject<USoundAttenuation>(GetTransientPackage());
		Att->Attenuation.bAttenuate = true;
		Att->Attenuation.bSpatialize = true;
		Att->Attenuation.AttenuationShapeExtents = FVector(300.0f, 0.0f, 0.0f);
		Att->Attenuation.FalloffDistance = 2500.0f;
		const double Seconds = (double)DataLen / (double)(2 * Channels * Rate);
		GAck.Sound = UGameplayStatics::SpawnSoundAtLocation(World, W, Who->GetActorLocation() + FVector(0.0f, 0.0f, 160.0f),
			FRotator::ZeroRotator, 1.0f, 1.0f, 0.0f, Att);
		GAck.Until = NowS() + Seconds;
		// THE GLANCE: the sound's own face animation, on the face (the part whose
		// skeleton the animation was made on), then back to the idle where it was.
		// Named as tools/ue/speech_faces.py names it: AS_ plus the sound's name, dashes as underscores.
		const FString Name = FString::Printf(TEXT("AS_ack_%s_%s"), *Un(Card), *FPaths::GetBaseFilename(Wav).Replace(TEXT("-"), TEXT("_")));
		UAnimSequenceBase* Anim = LoadObject<UAnimSequenceBase>(nullptr, *FString::Printf(TEXT("/Game/Ledger/MetaHumans/Speech/%s.%s"), *Name, *Name));
		// A FACE PLAYING OUR ANIMATION KEEPS IT (above): its mouth follows this
		// sound instead of the sound's own face animation.
		bool bOurFace = false;
		{
			TArray<USkeletalMeshComponent*> Parts;
			Who->GetComponents(Parts);
			for (USkeletalMeshComponent* C : Parts) { if (C != nullptr && C->GetName() == TEXT("Face") && Cast<ULedgerPersonAnim>(C->GetAnimInstance()) != nullptr) { bOurFace = true; } }
		}
		if (bOurFace)
		{
			GAckMouth.Pcm.Reset();
			GAckMouth.Pcm.Append(reinterpret_cast<const int16*>(&Bytes[DataAt]), DataLen / 2);
			GAckMouth.Rate = Rate;
			GAckMouth.Ch = FMath::Max(1, Channels);
			GAckMouth.Queued = DataLen;
			GAckMouth.RefDb = ClipSpeakingDb(GAckMouth.Pcm, GAckMouth.Rate, GAckMouth.Ch);
			GAckMouth.Wave = W;
			GAckMouth.Who = Who;
		}
		if (Anim != nullptr && !bOurFace)
		{
			TArray<USkeletalMeshComponent*> Parts;
			Who->GetComponents(Parts);
			for (USkeletalMeshComponent* C : Parts)
			{
				USkeletalMesh* M = C != nullptr ? C->GetSkeletalMeshAsset() : nullptr;
				if (M == nullptr || M->GetSkeleton() != Anim->GetSkeleton()) { continue; }
				if (UAnimSingleNodeInstance* Node = C->GetSingleNodeInstance())
				{
					GAck.FaceIdle = Node->GetAnimationAsset();
					GAck.FaceIdleAt = Node->GetCurrentTime();
				}
				C->PlayAnimation(Anim, false);
				GAck.Face = C;
				break;
			}
		}
		UE_LOG(LogTemp, Display, TEXT("LedgerAck: %s says %s, %.2f s, face %s"), *Un(Card), *FPaths::GetBaseFilename(Wav), Seconds,
			bOurFace ? TEXT("its mouth follows the sound") : GAck.Face.IsValid() ? TEXT("yes") : TEXT("no"));
	}

	// Each frame: the acknowledgement ends with its sound, or at once when the answer starts.
	void AckTick()
	{
		if (!GAck.Sound.IsValid() && !GAck.Face.IsValid()) { return; }
		if (GVoice.Playing.IsValid()) { AckEnd(true); return; }
		if (NowS() > GAck.Until + 0.1) { AckEnd(false); }
	}

	// The pending sentence's pieces to the queue (its words passed their check).
	void LiveVoiceRelease(int32 Id)
	{
		GVoice.HeldIds.Remove(Id);
		for (int32 I = 0; I < GVoice.Held.Num();)
		{
			if (GVoice.Held[I].Id == Id) { GVoice.Queue.Add(GVoice.Held[I]); GVoice.Held.RemoveAt(I); }
			else { ++I; }
		}
	}

	// The pending sentence thrown away (the turn went another way).
	void LiveVoiceDrop(int32 Id)
	{
		if (!GVoice.HeldIds.Contains(Id)) { return; }
		GVoice.HeldIds.Remove(Id);
		GVoice.DroppedIds.Add(Id);
		GVoice.Held.RemoveAll([Id](const FLiveVoice::FPiece& P) { return P.Id == Id; });
	}

	void LiveVoiceSay(int32 Id, const std::string& Card, const std::string& Text, AActor* Who, int32 Turn = 0)
	{
		if (!GVoice.bReady || GVoice.InWrite == nullptr || Text.empty() || Text == "none") { return; }
		// "turn": a conversation's turn, so the voice serves the newest first and
		// drops an older turn's unmade sentences (voice-server.py, pick).
		const std::string Req = "{\"id\":" + std::to_string(Id) + ",\"who\":\"" + JsonEsc(Card)
			+ "\",\"text\":\"" + JsonEsc(Text) + "\"" + (Turn > 0 ? ",\"turn\":" + std::to_string(Turn) : std::string()) + "}\n";
		FPlatformProcess::WritePipe(GVoice.InWrite, Un(Req));
		GVoice.Pending.Add(Id, Who);
		bVoiceAsked = true;
		GVoiceAskedAt = NowS();
		if (bAwaitFirstSound && GTimedVoiceAskedAt < GTimedWordsAt) { GTimedVoiceAskedAt = GVoiceAskedAt; GTimedVoiceId = Id; GTimedPieceAt = 0.0; }
	}

	// THE DEED A STORY IS ABOUT, by the key the session record and the talk
	// program use (29 September, town list 6ah): the window, whether seen
	// broken or seen as the man running from it, is "player.window_d1"; any
	// other story about him is its own topic; a story about somebody else is
	// none (empty).
	std::string DeedKeyOf(const RumorPtr& R)
	{
		if (!R || R->Content.Subject != "player") { return std::string(); }
		if (R->Content.Predicate == "broke_a_window" || R->Content.Predicate == LedgerCrime::NearPredicate()) { return "player.window_d1"; }
		return R->TopicKey();
	}

	std::string MemoriesJson(const GossiperPtr& G)
	{
		std::string Mem;
		if (G && G->Memory)
		{
			// WHICH STORY A MEMORY BELONGS TO (town list 6ah): the memories the
			// mill writes (a sighting, "I heard from ... that ...") carry the
			// story's own summary, so a memory holding the summary of a story
			// about him is tagged with that story's deed.
			std::vector<std::pair<std::string, std::string>> Stories;
			for (const RumorPtr& R : G->Rumors)
			{
				const std::string Key = DeedKeyOf(R);
				if (!Key.empty() && !R->Summary.empty()) { Stories.push_back({ R->Summary, Key }); }
			}
			for (const MemoryEvent& E : G->Memory->Events)
			{
				std::string Story;
				for (const auto& S : Stories) { if (E.Text.find(S.first) != std::string::npos) { Story = S.second; break; } }
				if (!Mem.empty()) { Mem += ","; }
				Mem += "{\"day\":" + std::to_string(E.Time.Day) + ",\"hour\":" + std::to_string(E.Time.Hour)
					+ ",\"minute\":" + std::to_string(E.Time.Minute) + ",\"kind\":\"" + JsonEsc(E.Kind)
					+ "\",\"importance\":" + std::to_string(E.Importance) + ",\"text\":\"" + JsonEsc(E.Text) + "\""
					+ (Story.empty() ? std::string() : ",\"story\":\"" + JsonEsc(Story) + "\"") + "}";
			}
		}
		return Mem;
	}

	// HOW THEY KNOW HIM (town list 6s): met, once he has talked with them in
	// this game (a conversation is a scene with him; the first hour's
	// walk-round, which would make Sheila's the first, is not built yet);
	// heard of him, once any story about him has reached them. No "calls":
	// the talk program then has them call him the new owner.
	std::string AcquaintanceJson(const GossiperPtr& G, const std::string& Card)
	{
		bool bHeardOf = false;
		if (G) { for (const RumorPtr& R : G->Rumors) { if (R && R->Content.Subject == "player") { bHeardOf = true; break; } } }
		// Sheila has met him once her walk-round is over (town list 6s, 6cg).
		const bool bMet = GLive.Talked.count(Card) > 0 || (Card == "lena" && bSheilaMet);
		// "knowsName" once they hold the street's story of his name (town list 6ch).
		return std::string(",\"acquaintance\":{\"met\":") + (bMet ? "true" : "false")
			+ ",\"heardOf\":" + (bHeardOf ? "true" : "false")
			+ (LedgerCore::PlayerIdentity::HoldsHisName(G.get()) ? ",\"knowsName\":true" : "") + "}";
	}

	// THE WEEK IN THE TALK (ROUTE.md section 2; production/specs/talk-protocol.md),
	// in free play: Ron knows the envelope is his to hear a no to while the
	// night's ask stands; Sheila puts her week's-end question the first time
	// he talks to her at Mickey's on the Sunday, and it stands after.
	std::string WeekTalkJson(const std::string& Card)
	{
		if (bLiveScript || !GMill) { return std::string(); }
		std::string J;
		if (Card == "rocco" && GWeek.Asks.AskStands(GNow)) { J += ",\"ask\":{\"tonight\":true}"; }
		if (Card == "lena")
		{
			if (GWeek.Week.Stands(GNow)) { J += ",\"week\":{\"stands\":true}"; }
			else if (GWeek.Week.Waits(GNow) && GWeek.Week.Ask(GNow, bSheilaTrusts, NearPlace("mickeys_office", 6.0)))
			{
				J += std::string(",\"week\":{\"ask\":true,\"realBook\":") + (bSheilaTrusts ? "true" : "false")
					+ ",\"dayOff\":" + (CastDay::Weekday(GNow.Day) == 6 ? "true" : "false")
					+ ",\"ended\":" + (GWeek.Asks.Ended() ? "true" : "false") + "}";
				UE_LOG(LogTemp, Display, TEXT("LedgerWeek: Sheila puts her question at %s (%s)"), *Un(GNow.ToString()),
					bSheilaTrusts ? TEXT("the real book") : TEXT("the day-book"));
			}
		}
		return J;
	}

	std::string EvidenceFor(const GossiperPtr& G, double Familiarity, int OwnRungOnA);
	std::string JsonField(const std::string& Line, const std::string& Name);
	void SaveEncounterToDisk();

	// WHAT OF A STORY ABOUT HIM HAS REACHED THEM (town list 1): RegardFor's
	// Knowing and Story, only when they can tell it is him; otherwise nothing.
	std::string KnowingJson(const std::string& Card)
	{
		auto It = GLive.Regards.find(Card);
		if (It == GLive.Regards.end()) { return std::string(); }
		const StreetVoice::Regard& R = It->second;
		if (!R.bKnowsItIsHim || R.HowMuch == StreetVoice::Knowing::Nothing || !R.Story)
		{
			return ",\"knowing\":{\"level\":\"nothing\"}";
		}
		return std::string(",\"knowing\":{\"level\":\"") + (R.HowMuch == StreetVoice::Knowing::ALittle ? "little" : "enough")
			+ "\",\"story\":\"" + JsonEsc(R.Story->Summary.empty() ? R.Story->TopicKey() : R.Story->Summary) + "\"}";
	}

	// Asks, and returns at once; the answer arrives in LiveHelperPump.
	bool LiveAsk(const GossiperPtr& G, const std::string& Card, const std::string& Who, int OwnRung, const FString& Name,
	             const std::string& Said)
	{
		if (!GLive.bStarted || !GLive.bReady || GLive.PendingId != 0) { return false; }
		const int Id = GLive.NextId++;
		// WHO IS THE CAST ID, AND THE SCENE IS THE WEATHER AND THE LIGHT, 29
		// September (the town session's handover 6u): the talk program now
		// tells each person where they are this hour from the cast's routines
		// (production/specs/hook-cast.json), keyed by "who" as the cast id
		// ("sam", not the street's "n2"), so the game no longer names a place.
		// The street is overcast and dry by day (Perceivers' overcast_day).
		const int H = GNow.Hour;
		const char* Light = (H >= 20 || H < 6) ? "Overcast and dry; dark, the street lamps on."
			: (H < 8 || H >= 18) ? "Overcast and dry; the light going." : "Overcast and dry; grey daylight.";
		// A NEW CONVERSATION (handover 6ae): the first with them, or the first
		// since he left them or they ended it; and WHO ELSE IS THERE (6ad): the
		// named people really within talking range of them (the cast file's
		// 6 m), not guessed from their routines.
		const bool bFresh = !GLive.Talked.count(Card) || GLive.Left.count(Card);
		const std::string Acquaintance = AcquaintanceJson(G, Card);
		// THE DEED THEY HOLD (town list 6ac, 6am, 6au).
		const std::string DeedField = (bDeedDone && G)
			? LedgerCrime::DeedJson(*G, DeedKeyNow(), GDeedDay, GDeedHour, GSawHimAt.count(G->Id) ? GSawHimAt[G->Id] : std::string())
			: std::string();
		GLive.Talked.insert(Card);
		GLive.Left.erase(Card);
		GMet.Met(Card, GNow.Day);
		std::string Present;
		if (AActor* Me = CardBody(Card))
		{
			for (const char* Other : { "sam", "lena", "rocco" })
			{
				AActor* B = CardBody(Other);
				if (Other == Card || B == nullptr) { continue; }
				if (FVector::Dist2D(Me->GetActorLocation(), B->GetActorLocation()) / 100.0 <= 6.0)
				{
					Present += std::string(Present.empty() ? "" : ",") + "\"" + Other + "\"";
				}
			}
		}
		const std::string Req = "{\"id\":" + std::to_string(Id) + ",\"to\":\"" + JsonEsc(Card)
			+ "\",\"who\":\"" + JsonEsc(Card) + "\",\"say\":\"" + JsonEsc(Said) + "\",\"day\":" + std::to_string(GNow.Day)
			+ ",\"hour\":" + std::to_string(GNow.Hour) + ",\"minute\":" + std::to_string(GNow.Minute)
			+ (bFresh ? ",\"fresh\":true" : "") + ",\"present\":[" + Present + "]"
			+ ",\"scene\":\"" + Light + "\",\"memories\":[" + MemoriesJson(G) + "]"
			+ ",\"evidence\":" + EvidenceFor(G, TalkFamiliarity(Card), OwnRung) + KnowingJson(Card) + Acquaintance + DeedField + WeekTalkJson(Card) + "}\n";
		FPlatformProcess::WritePipe(GLive.InWrite, Un(Req));
		UE_LOG(LogTemp, Display, TEXT("LedgerTalk: to %s%s%s%s evidence=%s"), *Un(Card), *Un(Acquaintance), *Un(KnowingJson(Card)), *Un(DeedField),
			*Un(EvidenceFor(G, TalkFamiliarity(Card), OwnRung)));
		GLive.PendingId = Id;
		GLive.PendingSaid.clear();
		GLive.PendingName = Name;
		GLive.PendingCard = Card;
		GLive.AnswerCard = Card;
		GLive.HeardSoFar.clear();
		GLive.bWalkedSent = false;
		GLive.bWasNear = false;
		GLive.AskedAt = NowS();
		return true;
	}

	// WALKING OFF MID-REPLY, 29 September (the town session's handover 6v): if
	// the player goes out of earshot (6 m, GossipDirector's) while someone is
	// still answering, the talk program is told once what he heard before he
	// left; the character then keeps only that, and remembers that he went.
	// THE SESSION RECORD'S HELPERS (handover 6p). The cast file, found where
	// the street file is found: -LedgerRepo, the checkout beside the project,
	// or the game's own staged copy.
	FString SessionCastFile()
	{
		TArray<FString> Cands;
		FString Repo;
		if (FParse::Value(FCommandLine::Get(), TEXT("LedgerRepo="), Repo) && !Repo.IsEmpty()) { Cands.Add(FPaths::Combine(Repo, TEXT("production/specs/hook-cast.json"))); }
		Cands.Add(AbsProject(TEXT("../production/specs/hook-cast.json")));
		Cands.Add(AbsProject(TEXT("../../../../production/specs/hook-cast.json")));
		Cands.Add(FPaths::ConvertRelativePathToFull(FPaths::Combine(FPaths::ProjectContentDir(), TEXT("LedgerData/production/specs/hook-cast.json"))));
		for (FString C : Cands)
		{
			FPaths::CollapseRelativeDirectories(C);
			if (FPaths::FileExists(C)) { return C; }
		}
		return FString();
	}

	// THE LIVE ENCOUNTER'S TIES FROM THE CAST FILE, 29 September (town list
	// handover 2): Sheila, Darren and Ron are tied to each other as
	// production/specs/hook-cast.json ties them (lena, sam and rocco there),
	// read through CastDay.h, the port of the reader the Core's tests use,
	// rather than by the probe's own 0.6. The regression keeps its measured
	// ties; a file that cannot be read leaves them too, and says so.
	void LiveTiesFromCast()
	{
		const FString Path = SessionCastFile();
		FString Text;
		CastDay Cast;
		std::string Err;
		if (Path.IsEmpty() || !FFileHelper::LoadFileToString(Text, *Path) || !CastDay::Parse(Utf8(Text), Cast, Err))
		{
			UE_LOG(LogTemp, Warning, TEXT("LedgerCast: the probe's own ties kept: %s"),
				Path.IsEmpty() ? TEXT("no hook-cast.json found") : *Un(Err.empty() ? std::string("unreadable") : Err));
			return;
		}
		const std::map<std::string, std::string> Street = { { "lena", GIdW1 }, { "sam", GIdN2 }, { "rocco", GIdR3 } };
		// THE WHOLE TOWN IN FREE PLAY (Jafar's list of 30 September, item 1:
		// gossip and the consequence in ordinary play). The three in the
		// street keep the ids the game has always given them (w1, n2 and the
		// mate's); everyone else in the cast file joins the mill by their own
		// id and circle, with every tie the file gives, so the town talks by
		// its routines, the damage can be found and the police can be told.
		// The scripted encounter keeps its three and their ties, as the
		// regression measures.
		auto IdOf = [&Street](const std::string& Cid) { const auto It = Street.find(Cid); return It != Street.end() ? It->second : Cid; };
		int Joined = 0;
		if (!bLiveScript)
		{
			for (const std::string& P : Cast.People())
			{
				if (Street.count(P) || GMill->Get(P)) { continue; }
				const std::string Name = Cast.NameOf(P);
				GMill->Add(std::make_shared<Gossiper>(P, Name.empty() ? P : Name, std::shared_ptr<MemoryStore>(),
					std::shared_ptr<KnowledgeBase>(), Cast.CircleOf(P)));
				++Joined;
			}
		}
		std::string Said;
		int Linked = 0;
		for (const CastDay::Tie& T : Cast.Ties())
		{
			if (bLiveScript && (!Street.count(T.A) || !Street.count(T.B))) { continue; }
			const std::string A = IdOf(T.A), B = IdOf(T.B);
			if (!GMill->Get(A) || !GMill->Get(B)) { continue; }
			GGraph->Link(A, B, T.W);
			++Linked;
			if (Street.count(T.A) && Street.count(T.B)) { Said += " " + A + "-" + B + "=" + LedgerCrime::F2(T.W); }
		}
		UE_LOG(LogTemp, Display, TEXT("LedgerCast: ties from %s:%s; %d more of the town in the mill, %d ties in all"),
			*Path, *Un(Said), Joined, Linked);
		GCast = Cast;
		bGCast = true;
	}

	// WHAT A REPLY SAYS OF HIS ANSWER, HIS OWNING UP AND A PROMISE TO KEEP
	// QUIET (town list 6am, 6al), into the town's gossip: a definite answer
	// about where he was becomes the story "he says he was at ..." held by
	// the one he told, carried like any story; owning up gives them the deed's
	// story as told by him; an agreement to keep it quiet holds back what they
	// know of it. NOT HERE: a fragile agreement taken back when somebody pays
	// or threatens them, since nobody in the game pays or threatens yet; and a
	// killing's "grave", since there is none.
	GossiperPtr GossiperOfCard(const std::string& Card)
	{
		return Card == "lena" ? GW1 : Card == "sam" ? GN2 : Card == "rocco" ? GR3 : GossiperPtr();
	}

	void TakeClaimsFromReply(const std::string& Line, const std::string& Card)
	{
		using namespace LedgerVignette;
		const GossiperPtr G = GossiperOfCard(Card);
		Value Root;
		std::string Err;
		if (!G || !MiniJson::Deserialize(Line, Root, Err) || Root.Type != T_OBJ) { return; }
		const Value* Claim = CastDay::GetObject(&Root, "claim");
		const Value* Definite = CastDay::Get(Claim, "definite");
		const Value* AreasV = CastDay::GetList(Claim, "areas");
		std::string Topic;
		if (Claim != nullptr && Definite != nullptr && Definite->Type == T_BOOL && Definite->Bool && AreasV != nullptr
		    && CastDay::GetString(Claim, "topic", Topic) && !Topic.empty())
		{
			std::vector<std::string> Areas;
			for (const Value& A : AreasV->Arr) { if (A.Type == T_STR && !A.Str.empty()) { Areas.push_back(A.Str); } }
			if (!Areas.empty())
			{
				const std::vector<std::string> Names = bGCast ? GCast.AreaNamesOf(Areas[0]) : std::vector<std::string>();
				RumorPtr Said = LedgerCrime::ClaimStory(Topic, Areas, Names.empty() ? Areas[0] : Names[0], G->Id);
				bool bHeld = false;
				for (const RumorPtr& R : G->Rumors) { if (R && R->TopicKey() == Said->TopicKey() && R->Content.Value == Said->Content.Value) { bHeld = true; } }
				if (!bHeld)
				{
					G->Rumors.push_back(Said);
					UE_LOG(LogTemp, Display, TEXT("LedgerDeed: %s heard him say: %s"), *Un(Card), *Un(Said->Summary));
				}
			}
		}
		const Value* Quiet = CastDay::GetObject(&Root, "keepsQuiet");
		const Value* Agreed = CastDay::Get(Quiet, "agreed");
		if (Quiet != nullptr && Agreed != nullptr && Agreed->Type == T_BOOL && Agreed->Bool && CastDay::GetString(Quiet, "topic", Topic) && !Topic.empty())
		{
			LedgerCrime::KeepQuiet(*G, Topic);
			UE_LOG(LogTemp, Display, TEXT("LedgerDeed: %s keeps %s quiet"), *Un(Card), *Un(Topic));
		}
		if (CastDay::GetString(&Root, "ownedUp", Topic) && !Topic.empty())
		{
			// In free play the deed's own story, about Rita's window (the review's A3).
			G->Rumors.push_back(bRitasWindow && Topic == GWindowTopic
				? LedgerCrime::OwnedUpStory(Topic, G->Id, "ritas", "the new owner told me himself that he put Rita's window in")
				: LedgerCrime::OwnedUpStory(Topic, G->Id));
			UE_LOG(LogTemp, Display, TEXT("LedgerDeed: he owned up to %s to %s"), *Un(Topic), *Un(Card));
		}
		// HE GAVE HIS NAME (town list 6ch): they hold it as the street's plain
		// fact, once, and the town's rounds pass it on (PlayerIdentity.h).
		const Value* Gave = CastDay::Get(&Root, "gaveName");
		if (Gave != nullptr && Gave->Type == T_BOOL && Gave->Bool && GMill && LedgerCore::PlayerIdentity::NameTold(GMill.get(), G->Id, GNow))
		{
			UE_LOG(LogTemp, Display, TEXT("LedgerNames: %s has his name now"), *Un(Card));
		}
		// A THREAT (the reply's "threatened"): the one threatened holds it
		// first-hand, warier, and it buys no silence (Silence.h).
		std::string Threat;
		if (GMill && CastDay::GetString(&Root, "threatened", Threat) && !Threat.empty() && Silence::FileThreat(GMill.get(), G->Id, Threat, GNow))
		{
			LedgerSession::Write(TEXT("deed"), TEXT("\"topic\":") + LedgerSession::Str(Un(Threat)) + TEXT(",\"seen\":[") + LedgerSession::Str(Un(G->Id)) + TEXT("]"));
			UE_LOG(LogTemp, Display, TEXT("LedgerDeed: he threatened %s over %s"), *Un(Card), *Un(Threat));
		}
		// THE WEEK, FROM THE TALK (ROUTE.md steps 12 and 14), in free play.
		if (bLiveScript || !GMill) { return; }
		const Value* Refused = CastDay::Get(&Root, "refusedAsk");
		if (Card == "rocco" && Refused != nullptr && Refused->Type == T_BOOL && Refused->Bool)
		{
			const int Night = Arrangement::NightOf(GNow);
			if (GWeek.AnswerAsk(Night, NightAnswer::Refused, GMill.get(), GNow))
			{
				LedgerSession::Write(TEXT("refused"), TEXT("\"night\":") + FString::FromInt(Night));
				UE_LOG(LogTemp, Display, TEXT("LedgerWeek: he tells Ron no, night %d, %s"), Night, *Un(GNow.ToString()));
			}
		}
		std::string Answer;
		if (Card == "lena" && CastDay::GetString(&Root, "weekAnswer", Answer) && !Answer.empty())
		{
			const WeekAnswer A = Answer == "WindDown" ? WeekAnswer::WindDown : Answer == "TakeOver" ? WeekAnswer::TakeOver
				: Answer == "WontSay" ? WeekAnswer::WontSay : WeekAnswer::None;
			if (GWeek.Week.Give(A, GNow, GMill.get(), &GCast, &GWeek.Asks))
			{
				LedgerSession::Write(TEXT("week"), TEXT("\"answer\":") + LedgerSession::Str(Un(Answer)));
				UE_LOG(LogTemp, Display, TEXT("LedgerWeek: his answer to Sheila, %s, at %s"), *Un(Answer), *Un(GNow.ToString()));
			}
		}
		const Value* Earned = CastDay::Get(&Root, "trustEarned");
		const Value* Trusts = CastDay::Get(&Root, "trusts");
		if (Card == "lena" && !bSheilaTrusts && ((Earned != nullptr && Earned->Type == T_BOOL && Earned->Bool) || (Trusts != nullptr && Trusts->Type == T_BOOL && Trusts->Bool)))
		{
			bSheilaTrusts = true;
			UE_LOG(LogTemp, Display, TEXT("LedgerWeek: Sheila trusts him from %s"), *Un(GNow.ToString()));
		}
	}

	// A list of strings out of a reply line: "name":["a","b"].
	TArray<FString> JsonList(const std::string& Line, const std::string& Name)
	{
		TArray<FString> Out;
		const std::string K = "\"" + Name + "\":[";
		std::string::size_type I = Line.find(K);
		if (I == std::string::npos) { return Out; }
		I += K.size();
		std::string Cur;
		bool bIn = false;
		for (; I < Line.size(); ++I)
		{
			const char C = Line[I];
			if (!bIn && C == ']') { break; }
			if (C == '"') { if (bIn) { Out.Add(Un(Cur)); Cur.clear(); } bIn = !bIn; continue; }
			if (bIn && C == '\\' && I + 1 < Line.size()) { Cur += Line[++I]; continue; }
			if (bIn) { Cur += C; }
		}
		return Out;
	}

	// THE SESSION'S END, when the game closes: the talk program's input is
	// closed, and the line it then writes says what this session's talk cost.
	void SessionEndAtExit()
	{
		double Usd = -1.0;
		if (GLive.bStarted && GLive.InWrite != nullptr)
		{
			FPlatformProcess::ClosePipe(GLive.InRead, GLive.InWrite);
			GLive.InRead = GLive.InWrite = nullptr;
			std::string Buf;
			const double T0 = NowS();
			while (NowS() - T0 < 3.0)
			{
				Buf += Utf8(FPlatformProcess::ReadPipe(GLive.OutRead));
				const std::string::size_type At = Buf.find("\"usd\":");
				if (At != std::string::npos) { Usd = atof(Buf.c_str() + At + 6); break; }
				FPlatformProcess::Sleep(0.05f);
			}
		}
		LedgerSession::End(TEXT("quit"), Usd);
	}

	void LiveWalkedAwayCheck()
	{
		if (GLive.AnswerCard.empty() || GLive.bWalkedSent || GPawn == nullptr) { return; }
		AActor* Body = GLive.AnswerBody != nullptr ? GLive.AnswerBody : GLive.PendingBody;
		if (Body == nullptr) { return; }
		const double Now = NowS();
		if (GLive.PendingId == 0 && Now >= GVoice.BusyUntil) { return; }
		const double M = FVector::Dist2D(GPawn->GetActorLocation(), Body->GetActorLocation()) / 100.0;
		// WALKING AWAY NEEDS HAVING BEEN THERE: a line put from further off
		// (the scripted ask, from 25 m) is not walked away from (29 September).
		if (M <= LedgerCrime::kEarshotM) { GLive.bWasNear = true; return; }
		if (!GLive.bWasNear) { return; }
		const std::string Req = "{\"walkedAway\":{\"to\":\"" + JsonEsc(GLive.AnswerCard) + "\",\"heard\":\"" + JsonEsc(GLive.HeardSoFar)
			+ "\"},\"day\":" + std::to_string(GNow.Day) + ",\"hour\":" + std::to_string(GNow.Hour) + ",\"minute\":" + std::to_string(GNow.Minute) + "}\n";
		FPlatformProcess::WritePipe(GLive.InWrite, Un(Req));
		GLive.bWalkedSent = true;
		UE_LOG(LogTemp, Display, TEXT("LedgerTalk: walked away from %s at %.1f m, having heard: %s"), UTF8_TO_TCHAR(GLive.AnswerCard.c_str()), M,
			UTF8_TO_TCHAR(GLive.HeardSoFar.c_str()));
	}

	void LiveHelperPump()
	{
		if (!GLive.bStarted) { return; }
		GLive.Buf += Utf8(FPlatformProcess::ReadPipe(GLive.OutRead));
		std::string::size_type Nl;
		while ((Nl = GLive.Buf.find('\n')) != std::string::npos)
		{
			const std::string L = GLive.Buf.substr(0, Nl);
			GLive.Buf.erase(0, Nl + 1);
			// THE TALK'S SAVE AND LOAD ANSWERED, never silently (the Continue run of
			// 30 September found every save refused for its file name, unseen).
			if (L.compare(0, 8, "{\"talk\":") == 0)
			{
				UE_LOG(LogTemp, Display, TEXT("LedgerTalk: the talk program says %s"), *Un(L));
				if (L.find("\"error\"") != std::string::npos || L.find("\"stale\":true") != std::string::npos
				    || L.find("\"missing\":true") != std::string::npos)
				{
					LedgerSession::Write(TEXT("talkSaveFailed"), TEXT("\"said\":") + LedgerSession::Str(Un(L)));
				}
				continue;
			}
			if (L.find("\"ready\"") != std::string::npos)
			{
				GLive.bReady = true;
				GLive.NoticeTitle = JsonField(L, "title");
				GLive.NoticeText = JsonField(L, "text");
				GLive.ReportLabel = JsonField(L, "report");
				continue;
			}
			// A REPORT ANSWERED: the helper keeps the line and thanks the player.
			if (L.find("\"reported\"") != std::string::npos)
			{
				const std::string Thanks = JsonField(L, "thanks");
				Say(Thanks == "none" ? FString(TEXT("Reported. Thank you.")) : Un(Thanks), 6.0f, FColor(210, 210, 210));
				continue;
			}
			if (GLive.PendingId != 0 && L.find("\"id\":" + std::to_string(GLive.PendingId) + ",") != std::string::npos)
			{
				// THE FIRST SENTENCE, BEFORE ITS CHECK (--pending): made by the voice
				// at once and held; nothing is shown or said yet.
				const std::string PendingWords = JsonField(L, "pending");
				if (PendingWords != "none" && JsonField(L, "first") == "none")
				{
					if (GVoice.bReady && GLive.PendingSaid.empty())
					{
						const int32 HeldId = GLive.PendingId * 10 + 7;
						GLive.PendingSaid = PendingWords;
						GVoice.HeldIds.Add(HeldId);
						LiveVoiceSay(HeldId, GLive.PendingCard, PendingWords, GVisualFor(GLive.PendingBody), GLive.PendingId);
						GTimedVoiceAskedAt = NowS();
						GTimedVoiceId = HeldId;
						GTimedPieceAt = 0.0;
					}
					continue;
				}
				// THE FIRST SENTENCE, EARLY: said and spoken at once; the answer's
				// line that follows carries only what is left to say ("rest").
				if (GLive.FirstAt < GLive.AskedAt)
				{
					GLive.FirstAt = NowS();
					// The line's clock: its words are here; its first sound is next
					// (already on its way when the pending sentence was sent).
					GTimedWordsAt = GLive.FirstAt;
					if (GLive.PendingSaid.empty()) { GTimedVoiceAskedAt = 0.0; }
					GTimedCard = GLive.PendingCard;
					bAwaitFirstSound = GVoice.bReady && GEnterAt > 0.0 && GEnterAt <= GLive.AskedAt;
				}
				const std::string First = JsonField(L, "first");
				if (First != "none")
				{
					Say(GLive.PendingName + TEXT(": ") + Un(First), 20.0f, FColor::White);
					const int32 HeldId = GLive.PendingId * 10 + 7;
					if (!GLive.PendingSaid.empty() && GLive.PendingSaid == First) { LiveVoiceRelease(HeldId); }
					else
					{
						LiveVoiceDrop(HeldId);
						LiveVoiceSay(GLive.PendingId * 10, GLive.PendingCard, First, GVisualFor(GLive.PendingBody), GLive.PendingId);
					}
					GLive.bFirstSaid = true;
					GLive.HeardSoFar = First;
					GLive.AnswerBody = GLive.PendingBody;
					continue;
				}
				const std::string Reply = JsonField(L, "reply");
				// LIVE TALK PAUSED, said once and plainly, not in a character's
				// voice (their brush-off still plays): why, and when it comes back.
				const std::string Paused = JsonField(L, "paused");
				if (Paused != "none" && !Paused.empty() && !GLive.bPausedShown)
				{
					Say(Un(Paused), 12.0f, FColor(210, 210, 210));
					GLive.bPausedShown = true;
				}
				// ONCE UNTIL IT COMES BACK (handover 6ax): a reply without it
				// means talk is back, so the next pause is said again.
				if (Paused == "none" || Paused.empty()) { GLive.bPausedShown = false; }
				// WALKED OFF (handover 6ay): he left while it was coming, and
				// the answer is only {"id","to","walkedOff":true}: nothing to
				// say or show, only the record's line.
				LiveVoiceDrop(GLive.PendingId * 10 + 7);
				if (L.find("\"walkedOff\":true") != std::string::npos)
				{
					LedgerSession::Write(TEXT("reply"), TEXT("\"who\":") + LedgerSession::Str(Un(GLive.PendingCard)) + TEXT(",\"how\":\"walkedOff\""));
					GLive.PendingId = 0;
					GLive.bFirstSaid = false;
					continue;
				}
				GLive.LastReplyId = GLive.PendingId;
				GLive.LastReplyName = GLive.PendingName;
				// THEY CLOSED IT (handover 6ae): his next line to them starts afresh.
				if (L.find("\"ends\":true") != std::string::npos) { GLive.Left.insert(GLive.PendingCard); }
				// THE SESSION RECORD (handover 6p): whom his line named, how the
				// answer went, and anything they put to him or drew on.
				{
					const FString Who = Un(GLive.PendingCard);
					const TArray<FString> Named = JsonList(L, "named");
					if (Named.Num() > 0)
					{
						LedgerSession::Write(TEXT("named"), TEXT("\"who\":") + LedgerSession::Str(Who) + TEXT(",\"names\":") + LedgerSession::List(Named));
					}
					const std::string Went = JsonField(L, "went");
					const double Secs = (GLive.FirstAt > GLive.AskedAt ? GLive.FirstAt : NowS()) - GLive.AskedAt;
					LedgerSession::Write(TEXT("reply"), TEXT("\"who\":") + LedgerSession::Str(Who)
						+ (Went != "none" ? TEXT(",\"how\":") + LedgerSession::Str(Un(Went)) : FString()) + FString::Printf(TEXT(",\"s\":%.1f"), Secs));
					for (const FString& Story : JsonList(L, "putToHim"))
					{
						LedgerSession::Write(TEXT("known"), TEXT("\"who\":") + LedgerSession::Str(Who) + TEXT(",\"how\":\"question\",\"story\":") + LedgerSession::Str(Story));
					}
					for (const FString& Story : JsonList(L, "spokeOf"))
					{
						LedgerSession::Write(TEXT("known"), TEXT("\"who\":") + LedgerSession::Str(Who) + TEXT(",\"how\":\"talk\",\"story\":") + LedgerSession::Str(Story));
					}
				}
				TakeClaimsFromReply(L, GLive.PendingCard);
				if (GLive.bFirstSaid)
				{
					const std::string Rest = JsonField(L, "rest");
					if (Rest != "none" && !Rest.empty())
					{
						Say(GLive.PendingName + TEXT(": ") + Un(Rest), 20.0f, FColor::White);
						LiveVoiceSay(GLive.PendingId * 10 + 1, GLive.PendingCard, Rest, GVisualFor(GLive.PendingBody), GLive.PendingId);
						GLive.HeardSoFar += " " + Rest;
					}
				}
				else
				{
					Say(GLive.PendingName + TEXT(": ") + Un(Reply == "none" ? std::string("...") : Reply), 20.0f, FColor::White);
					LiveVoiceSay(GLive.PendingId * 10, GLive.PendingCard, Reply, GVisualFor(GLive.PendingBody), GLive.PendingId);
					GLive.HeardSoFar = Reply == "none" ? std::string() : Reply;
					GLive.AnswerBody = GLive.PendingBody;
				}
				GLive.PendingId = 0;
				GLive.bFirstSaid = false;
				ClockCharge(kTalkMinutes);
				if (GPhase == ECrimePhase::LiveRoam) { SaveEncounterToDisk(); }
			}
		}
		// R: the last reply reported, with no note; F1: the notice again.
		int32 Reports = 0, Notices = 0;
		if (ALedgerSliceCharacter* Slice = Cast<ALedgerSliceCharacter>(GPawn))
		{
			Reports = Slice->ConsumeReportRequests();
			Notices = Slice->ConsumeNoticeRequests();
		}
		if (Notices > 0) { ShowAiNotice(); }
		if (Reports > 0) { LiveReportLast(); }
		LiveWalkedAwayCheck();
		// OUT OF EARSHOT OF SOMEBODY HE HAS TALKED TO: the next line to them
		// is a new conversation (handover 6ae).
		if (GPawn != nullptr)
		{
			for (const std::string& Card : GLive.Talked)
			{
				AActor* B = CardBody(Card);
				if (B != nullptr && FVector::Dist2D(GPawn->GetActorLocation(), B->GetActorLocation()) / 100.0 > LedgerCrime::kEarshotM)
				{
					GLive.Left.insert(Card);
				}
			}
		}
		// THE SAVE'S TALK LOADED, or a new game's talk cleared, once ready.
		if (GLive.bReady && (GLive.bTalkLoad || GLive.bTalkReset))
		{
			std::string Req;
			if (GLive.bTalkLoad)
			{
				const std::string Path = Utf8(FPaths::ConvertRelativePathToFull(EncSaveDir() / Un(LedgerCrime::TalkSaveFile())));
				Req = "{\"talk\":\"load\",\"path\":\"" + JsonEsc(Path) + "\",\"stamp\":\"" + GLive.TalkStamp + "\"}\n";
			}
			else { Req = "{\"talk\":\"reset\"}\n"; }
			FPlatformProcess::WritePipe(GLive.InWrite, Un(Req));
			UE_LOG(LogTemp, Display, TEXT("LedgerTalk: %s"), GLive.bTalkLoad ? TEXT("the save's talk loaded") : TEXT("a new game's talk cleared"));
			GLive.bTalkLoad = GLive.bTalkReset = false;
		}
		if (GLive.PendingId != 0 && NowS() - GLive.AskedAt > 30.0)
		{
			if (!GLive.bFirstSaid) { Say(GLive.PendingName + TEXT(" says nothing."), 6.0f, FColor::White); }
			GLive.PendingId = 0;
			GLive.bFirstSaid = false;
		}
	}

	// WHAT THE PLAYER SAYS, TYPED, 24 September: T near somebody opens a line
	// at the bottom of the screen; Enter says it, Esc leaves it. While it is
	// open the keys go to the line, not to the legs.
	struct FTalkTarget { GossiperPtr G; std::string Card, Id; int Rung = -1; FString Name; AActor* Body = nullptr; };
	FTalkTarget GTalkTarget;
	TSharedPtr<SWidget> GSayBox;
	TSharedPtr<SEditableTextBox> GSayText;
	bool bSayOpen = false, bSayCommitted = false, bSayCancelled = false;
	FString GSaid;
	double GSayOpenedAt = 0.0;

	void OpenSayBox(UWorld* World)
	{
		if (bSayOpen || GEngine == nullptr || GEngine->GameViewport == nullptr || World == nullptr) { return; }
		if (!GLive.bNoticeShown) { ShowAiNotice(); }
		LedgerSession::Write(TEXT("talk"), TEXT("\"who\":") + LedgerSession::Str(Un(GTalkTarget.Card)));
		bSayCommitted = bSayCancelled = false;
		GSaid.Reset();
		SAssignNew(GSayBox, SBox)
			.HAlign(HAlign_Center).VAlign(VAlign_Bottom).Padding(FMargin(0.0f, 0.0f, 0.0f, 90.0f))
			[
				SNew(SBox).WidthOverride(900.0f)
				[
					SAssignNew(GSayText, SEditableTextBox)
					.HintText(FText::FromString(FString(TEXT("Say something to ")) + GTalkTarget.Name + TEXT(", then Enter. Esc to leave it.")))
					.OnTextCommitted_Lambda([](const FText& T, ETextCommit::Type How)
					{
						if (How == ETextCommit::OnEnter || How == ETextCommit::OnCleared)
						{
							UE_LOG(LogTemp, Display, TEXT("LedgerSayBox: %s with %d characters"),
							       How == ETextCommit::OnEnter ? TEXT("sent") : TEXT("left with Esc"), T.ToString().Len());
						}
						// A BOX THAT NEVER HELD THE KEYBOARD, 29 September (the tester, with
						// real key presses, in a friend's plain copy): Slate cannot focus a
						// widget in the frame it is added, so the box lost a focus it never
						// had, closed itself, and the letters he typed went to the game (the
						// window smashed on "e", report on "r", Tom walked). Now only Enter or
						// Esc ends the line; a lost focus is won back (HumanTalkTick), and the
						// game ignores its keys while the box is open.
						if (How == ETextCommit::OnEnter) { GSaid = T.ToString(); bSayCommitted = true; GEnterAt = NowS(); }
						else if (How == ETextCommit::OnCleared) { bSayCancelled = true; }
					})
				]
			];
		GEngine->GameViewport->AddViewportWidgetContent(GSayBox.ToSharedRef(), 100);
		if (APlayerController* PC = World->GetFirstPlayerController())
		{
			FInputModeUIOnly M;
			M.SetWidgetToFocus(GSayText);
			PC->SetInputMode(M);
			// A key held as the box opens would stay down: Tom walked on while
			// the line was typed.
			PC->FlushPressedKeys();
		}
		FSlateApplication::Get().SetKeyboardFocus(GSayText);
		bSayOpen = true;
		UE_LOG(LogTemp, Display, TEXT("LedgerSayBox: open for %s, keyboard focus %s"), *GTalkTarget.Name,
		       FSlateApplication::Get().GetKeyboardFocusedWidget() == GSayText ? TEXT("in the box") : TEXT("NOT in the box"));
		GSayOpenedAt = NowS();
	}

	void CloseSayBox(UWorld* World)
	{
		if (!bSayOpen) { return; }
		if (GEngine != nullptr && GEngine->GameViewport != nullptr && GSayBox.IsValid())
		{
			GEngine->GameViewport->RemoveViewportWidgetContent(GSayBox.ToSharedRef());
		}
		GSayBox.Reset();
		GSayText.Reset();
		if (World != nullptr)
		{
			if (APlayerController* PC = World->GetFirstPlayerController()) { PC->SetInputMode(FInputModeGameOnly()); }
		}
		FSlateApplication::Get().SetAllUserFocusToGameViewport();
		bSayOpen = false;
	}

	void RunTalk();

	// THE DELAY, MEASURED IN THE GAME ITSELF (-AskScript=N, 26 September; Jafar:
	// "measure the path ... with the game running"). N lines are asked in turn
	// of Darren, Sheila and Ron down the player's own path (LiveAsk, the
	// helper's early first sentence, the voice beside the game), each once the
	// last has been heard out; for each, the seconds from the line sent to the
	// answer's first words and to its first sound playing are written to
	// ask-script.json in the game's log folder, and the game then closes.
	struct FAskScript { int32 Left = 0, N = 0; bool bWaiting = false, bReported = false; double SentAt = 0.0, HeardAt = 0.0; FString Rows; };
	FAskScript GAsk;

	void AskScriptTick(double Now)
	{
		if (GAsk.N == 0)
		{
			int32 N = 0;
			if (!FParse::Value(FCommandLine::Get(), TEXT("AskScript="), N) || N <= 0) { GAsk.N = -1; return; }
			GAsk.N = N;
			GAsk.Left = N;
		}
		if (GAsk.N < 0) { return; }
		if (bAskAfterDeed && GPhase != ECrimePhase::LiveRoam) { return; }
		static const char* Lines[] = { "What are you selling today, then?", "Evening. Anything going on round here?",
			"You look like you've been stood there a while.", "Who's the new owner, then?", "Is it always this quiet?",
			"Did you hear the glass go last night?" };
		struct Who { AActor* Body; GossiperPtr G; const char* Card; const char* Id; const TCHAR* Name; int Rung; };
		const Who People[3] = {
			{ GN2Body, GN2, "sam", GIdN2.c_str(), TEXT("Darren"), -1 },
			{ GW1Body, GW1, "lena", GIdW1.c_str(), TEXT("Sheila"), GW1RungA },
			{ GR3Body, GR3, "rocco", GIdR3.c_str(), TEXT("Ron"), -1 } };
		const bool bVoiceIdle = GVoice.Queue.Num() == 0 && GVoice.Pending.Num() == 0 && Now > GVoice.BusyUntil + 1.0;
		if (GAsk.bWaiting)
		{
			if (GAsk.HeardAt == 0.0 && GVoiceStartedAt > GAsk.SentAt) { GAsk.HeardAt = GVoiceStartedAt; }
			const bool bDone = GLive.PendingId == 0 && GAsk.HeardAt > 0.0 && bVoiceIdle;
			if (!bDone && Now - GAsk.SentAt < 45.0) { return; }
			const int32 I = GAsk.N - GAsk.Left;
			GAsk.Rows += FString::Printf(TEXT("%s{\"who\":\"%s\",\"firstWords\":%.2f,\"firstHeard\":%s}"), GAsk.Rows.IsEmpty() ? TEXT("") : TEXT(","),
				UTF8_TO_TCHAR(People[I % 3].Card), GLive.FirstAt > GAsk.SentAt ? GLive.FirstAt - GAsk.SentAt : -1.0,
				GAsk.HeardAt > 0.0 ? *FString::Printf(TEXT("%.2f"), GAsk.HeardAt - GAsk.SentAt) : TEXT("null"));
			UE_LOG(LogTemp, Display, TEXT("LedgerAskScript: line %d to %s: first words %.2f s, first sound %.2f s"), I + 1,
				UTF8_TO_TCHAR(People[I % 3].Card), GLive.FirstAt - GAsk.SentAt, GAsk.HeardAt > 0.0 ? GAsk.HeardAt - GAsk.SentAt : -1.0);
			GAsk.bWaiting = false;
			--GAsk.Left;
			if (GAsk.Left <= 0)
			{
				FFileHelper::SaveStringToFile(TEXT("{\"lines\":[") + GAsk.Rows + TEXT("]}"), *(FPaths::ProjectLogDir() / TEXT("ask-script.json")));
				FPlatformMisc::RequestExit(false);
			}
			return;
		}
		if (!GLive.bReady || GLive.PendingId != 0 || (GVoice.bStarted && !GVoice.bReady) || !bVoiceIdle) { return; }
		const int32 I = GAsk.N - GAsk.Left;
		if (I == 0 && !GLive.bNoticeShown) { ShowAiNotice(); }
		if (I == 1 && FParse::Param(FCommandLine::Get(), TEXT("AskReport")) && GAsk.Rows.Len() > 0 && !GAsk.bReported) { LiveReportLast(); GAsk.bReported = true; }
		const Who& P = People[I % 3];
		if (P.Body == nullptr || !P.G) { return; }
		if (LiveAsk(P.G, P.Card, P.Id, P.Rung, FString(P.Name), Lines[I % 6]))
		{
			GLive.PendingBody = P.Body;
			AckStart(P.Card, GVisualFor(P.Body));
			GAsk.SentAt = GLive.AskedAt;
			GAsk.HeardAt = 0.0;
			GAsk.bWaiting = true;
		}
	}

	// THE CONVERSATION LIGHT (LedgerTalkLight.h, 28 September): on whoever the
	// player is talking to, from the moment the line box opens until six
	// seconds after their answer has been heard out, placed from the player's
	// camera each frame. In the street's flat daylight a face is underlit; lit
	// this way it reads as it does in the studio (the fair pair, 28 September:
	// face brightness 42 to 115 at one held exposure), for 0.33 ms of the card.
	// -NoTalkLight turns it off.
	double GTalkLitUntil = 0.0;
	AActor* GTalkLitBody = nullptr;

	void TalkLightTick(UWorld* World, double Now)
	{
		static const bool bOff = FParse::Param(FCommandLine::Get(), TEXT("NoTalkLight"));
		AActor* Body = bSayOpen ? GTalkTarget.Body : GLive.PendingId != 0 ? GLive.PendingBody : nullptr;
		if (Body != nullptr)
		{
			if (Body != GTalkLitBody) { LedgerTalkLight::Off(); }
			GTalkLitBody = Body;
			GTalkLitUntil = FMath::Max(GTalkLitUntil, Now + 6.0);
		}
		if (GVoice.Playing.IsValid()) { GTalkLitUntil = FMath::Max(GTalkLitUntil, GVoice.PlayingEnd + 6.0); }
		APlayerController* PC = World != nullptr ? World->GetFirstPlayerController() : nullptr;
		AActor* Visual = GTalkLitBody != nullptr ? GVisualFor(GTalkLitBody) : nullptr;
		if (bOff || Now > GTalkLitUntil || Visual == nullptr || PC == nullptr || PC->PlayerCameraManager == nullptr)
		{
			// Only a light the game put on: the portrait tool lights people itself,
			// and this switched its light off the frame after (28 September).
			if (GTalkLitBody != nullptr) { LedgerTalkLight::Off(); }
			if (Now > GTalkLitUntil) { GTalkLitBody = nullptr; }
			return;
		}
		FVector Face = Visual->GetActorLocation() + FVector(0.0f, 0.0f, 160.0f);
		TArray<USkeletalMeshComponent*> Parts;
		Visual->GetComponents(Parts);
		for (USkeletalMeshComponent* C : Parts)
		{
			if (C != nullptr && C->DoesSocketExist(TEXT("head"))) { Face = C->GetSocketLocation(TEXT("head")) + FVector(0.0f, 0.0f, 6.0f); break; }
		}
		LedgerTalkLight::Key(World, Visual, PC->PlayerCameraManager->GetCameraLocation(), Face);
	}

	// THE PLAYER TALKS AT ANY POINT OF THE STORY, 24 September: before the
	// window, to people who know nothing yet; after it, to people who might.
	// Returns true while the typed line is open, when the rest of the phase
	// should wait.
	// HOW EACH OF THE CAST REGARDS HIM, each second (town list 1, 29
	// September): StreetVoice::RegardFor from what they hold, how well they
	// know him by sight, and whether anybody is beside them; it sets their
	// head's look, and a line is said when it says so and he is in earshot:
	// a half-remembered story as a word to the one beside them once he has
	// gone past (FaintRemark), otherwise as he comes by (Recognition), and
	// recorded only as heard. Nobody speaks up unasked while he is talking to
	// them, nor more often than the street's clear words (45 s). The lines
	// come through the ledger, so a bank does not repeat itself before he has
	// heard it through (town list 6k), and the ledger is kept in the save
	// (6o). NOT YET: the coat (the outfit's ask brings it, town list 6z).
	void RegardTick(UWorld* World, double Now)
	{
		if (World == nullptr || GPawn == nullptr || !GMill || Now - GLive.RegardAt < 1.0) { return; }
		GLive.RegardAt = Now;
		struct Who { AActor* Body; GossiperPtr G; const char* Card; const TCHAR* Name; double Familiarity; };
		// HOW WELL EACH KNOWS HIM BY SIGHT (Acquaintance): Sheila and Ron are
		// Mickey's, kept on, and have dealt with him (Known); Darren knows him
		// by name as Mickey's nephew and by face not at all (canon, 23
		// September: HeardOfYou), so nothing he holds shows.
		const Who People[3] = {
			{ GW1Body, GW1, "lena", TEXT("Sheila"), 0.50 },
			{ GN2Body, GN2, "sam", TEXT("Darren"), LedgerCrime::kLadFamiliarity },
			{ GR3Body, GR3, "rocco", TEXT("Ron"), 0.50 } };
		const FVector HimAt = GPawn->GetActorLocation();
		for (const Who& P : People)
		{
			if (P.Body == nullptr || !P.G) { continue; }
			const FVector At = P.Body->GetActorLocation();
			// ANYBODY BESIDE THEM to say it to: another of the cast, or one of
			// the street's people, within six metres.
			bool bCompanion = false;
			for (const Who& O : People)
			{
				if (&O != &P && O.Body != nullptr && FVector::Dist2D(At, O.Body->GetActorLocation()) <= 600.0) { bCompanion = true; }
			}
			for (TActorIterator<ASkeletalMeshActor> It(World); It && !bCompanion; ++It)
			{
				if (!It->IsHidden() && FVector::Dist2D(At, It->GetActorLocation()) <= 600.0) { bCompanion = true; }
			}
			const StreetVoice::Regard R = StreetVoice::RegardFor(P.G.get(), GMill->MinConfidenceToShare, false,
			                                                     &GLive.Remarks, P.Familiarity, bCompanion);
			auto Old = GLive.Regards.find(P.Card);
			if (Old == GLive.Regards.end() || Old->second.Stance != R.Stance || Old->second.HowMuch != R.HowMuch)
			{
				UE_LOG(LogTemp, Display, TEXT("LedgerRegard: %s %s knowing=%s itIsHim=%d firstLook=%.0fm/%.1fs second=%.0fm away=%.1fm back=%d speaks=%d faint=%d"),
					P.Name, UTF8_TO_TCHAR(StreetVoice::StanceName(R.Stance)), UTF8_TO_TCHAR(StreetVoice::KnowingName(R.HowMuch)),
					(int)R.bKnowsItIsHim, R.FirstLookMetres, FMath::IsFinite(R.FirstLookSeconds) ? R.FirstLookSeconds : -1.0,
					R.SecondLookMetres, R.LookAwayMetres, (int)R.bLooksBack, (int)R.bSpeaks, (int)R.bFaint);
			}
			GLive.Regards[P.Card] = R;
			int32 SecondLooks = 0;
			if (TArray<TWeakObjectPtr<ULedgerPersonAnim>>* Looks = GLooks.Find(P.Body))
			{
				for (const TWeakObjectPtr<ULedgerPersonAnim>& L : *Looks)
				{
					if (L.IsValid())
					{
						L->SetRegard(R.FirstLookMetres, R.FirstLookSeconds, R.SecondLookMetres, R.SecondLookSeconds,
						             R.LookAwayMetres, R.bLooksBack);
						SecondLooks = FMath::Max(SecondLooks, L->SecondLooks);   // body and face look together: counted once
					}
				}
			}
			// THE SECOND, LONGER LOOK IN THE SESSION RECORD (known, "look"), once
			// per look given, for a story about him that can be named.
			const std::string Deed = DeedKeyOf(R.Story);
			int32& Seen = GLive.SecondLooksSeen[P.Card];
			if (SecondLooks > Seen && R.bKnowsItIsHim && !Deed.empty())
			{
				LedgerSession::Write(TEXT("known"), TEXT("\"who\":") + LedgerSession::Str(Un(std::string(P.Card)))
					+ TEXT(",\"how\":\"look\",\"story\":") + LedgerSession::Str(Un(Deed)));
			}
			Seen = SecondLooks;
			// THE LINE, when it is due and he can hear it.
			const double M = FVector::Dist2D(HimAt, At) / 100.0;
			const bool bTalking = GLive.Talked.count(P.Card) && !GLive.Left.count(P.Card);
			auto Last = GLive.LineAt.find(P.Card);
			const bool bRested = Last == GLive.LineAt.end() || Now - Last->second >= 45.0;
			// A HUSH AFTER THE DEED'S SHOUT: for a minute after it nobody on the
			// street makes a passing remark (the AI tester, 29 September: Sheila
			// shouted "Stop. I mean it. Stop." and at once added the everyday
			// "Mind how you go.", her regard not yet holding what she had seen).
			const bool bHush = GShoutAt > 0.0 && NowS() - GShoutAt < 60.0;
			if (!R.bSpeaks || M > LedgerCrime::kEarshotM || bSayOpen || GLive.PendingId != 0 || bTalking || !bRested || bHush) { continue; }
			AActor* Visual = GVisualFor(P.Body);
			const FVector Facing = Visual != nullptr ? Visual->GetActorRightVector() : P.Body->GetActorForwardVector();
			const bool bPassed = FVector::DotProduct(Facing.GetSafeNormal2D(), (HimAt - At).GetSafeNormal2D()) < 0.0;
			const int Seed = (int)(StreetVoice::Hash(P.Card) % 100000u) + GNow.Day * 24 + GNow.Hour + GLive.LinesSaid;
			std::shared_ptr<SpokenLine> Line;
			if (R.bFaint)
			{
				if (!bPassed) { continue; }
				Line = StreetVoice::FaintRemark(P.G.get(), R.Story, Seed, &GLive.Remarks);
				if (Line) { GLive.Remarks.RecordFaint(P.G->Id, R.Story, true); ++GLive.FaintSaid; }
			}
			else
			{
				if (bPassed) { continue; }
				Line = StreetVoice::Recognition(P.G.get(), R.Story, R.Stance, Seed, &GLive.Remarks);
				if (Line) { GLive.Remarks.Record(P.G->Id, R.Story, R.Stance, true); }
			}
			if (!Line) { continue; }
			// HEARD, so its bank moves on (town list 6k): a line from a bank he
			// has not heard lately, and the one heard longest ago once he has
			// heard them all.
			GLive.Remarks.Heard(*Line);
			GLive.LineAt[P.Card] = Now;
			++GLive.LinesSaid;
			Say(FString(P.Name) + (R.bFaint ? TEXT(" (to the one beside them): ") : TEXT(": ")) + Un(Line->Text), 8.0f, FColor::White);
			LiveVoiceSay(GLive.NextLineId++, P.Card, Line->Text, Visual);
			UE_LOG(LogTemp, Display, TEXT("LedgerRegard: %s says (%s, %.1f m): %s"), P.Name, UTF8_TO_TCHAR(Line->Bank.c_str()), M, *Un(Line->Text));
			// AND IN THE SESSION RECORD (known): a remark to a companion, or a
			// line to his face from a story about him.
			if (!Deed.empty() && Line->Source)
			{
				LedgerSession::Write(TEXT("known"), TEXT("\"who\":") + LedgerSession::Str(Un(std::string(P.Card)))
					+ (R.bFaint ? TEXT(",\"how\":\"remark\",\"story\":") : TEXT(",\"how\":\"recognition\",\"story\":")) + LedgerSession::Str(Un(Deed)));
			}
			// KEPT AT ONCE, as a reply is: a remark made and then lost to a quit
			// would be made again after the reload.
			if (GPhase == ECrimePhase::LiveRoam) { SaveEncounterToDisk(); }
		}
	}

	// THE LOOK, WALKED PAST (-LookScript, 29 September, town list 1): he is
	// walked at a walking pace, 1.4 m/s, in a straight line past Sheila, from
	// 16 m in front of her to 8 m behind, 1.2 m to her side; each quarter
	// second her head's look and his distance go to look-script.json in the
	// log folder, with a picture as her first look comes, close in front, as
	// he passes and as she looks back (Saved/LookScript). -LookStory=little or
	// =enough first gives her a story of his night, half remembered or still
	// told, so each regard can be seen. The game then closes.
	// -LookCamera films it from in front of her instead, a frame every tenth of
	// a second (frames-<story> in -LookFrames=<folder>, or else in
	// Saved/LookScript), for the approval page; a film's frames are large, and
	// scratch goes to drive F. Film it on a fixed step (-benchmark -fps=30):
	// at the six frames a second a screenshot every frame allows, her hair's
	// simulation blew apart as her head turned back. The
	// walk runs on the game's clock, as the look does, so a slow frame rate
	// cannot stretch one against the other.
	struct FLookScript { int State = 0; double StartAt = 0.0, LastRow = 0.0, LastFrame = -1.0; int Frame = 0; bool bFilm = false;
	                     FVector From, To; FString Rows, Story, Frames; TSet<FString> Shot; };
	FLookScript GLook;

	void LookShot(const TCHAR* Name)
	{
		if (GLook.Shot.Contains(Name)) { return; }
		GLook.Shot.Add(Name);
		FScreenshotRequest::RequestScreenshot(FPaths::ConvertRelativePathToFull(FPaths::ProjectSavedDir()
			/ TEXT("LookScript") / FString::Printf(TEXT("look-%s-%s.png"), GLook.Story.IsEmpty() ? TEXT("none") : *GLook.Story, Name)), false, false);
	}

	void LookScriptTick(UWorld* World, double Now)
	{
		if (GLook.State < 0 || World == nullptr) { return; }
		if (GLook.State == 0)
		{
			if (!FParse::Param(FCommandLine::Get(), TEXT("LookScript"))) { GLook.State = -1; return; }
			AActor* Her = GVisualFor(GW1Body);
			if (Her == nullptr || GPawn == nullptr || !GW1) { return; }
			FParse::Value(FCommandLine::Get(), TEXT("LookStory="), GLook.Story);
			if (!GLook.Story.IsEmpty())
			{
				RumorPtr R = std::make_shared<Rumor>(Fact("player", "night_walk", "seen"));
				R->OriginId = "look-script";
				R->Summary = "the new owner was about the quay after midnight";
				R->Confidence = GLook.Story == TEXT("little") ? 0.1 : 0.5;
				R->Sensitive = true;
				R->Hops = 1;
				GW1->Rumors.push_back(R);
			}
			const FVector At = Her->GetActorLocation();
			const FVector Facing = Her->GetActorRightVector().GetSafeNormal2D();
			const FVector Side = FVector::CrossProduct(FVector::UpVector, Facing).GetSafeNormal2D();
			const double Z = GPawn->GetActorLocation().Z;
			GLook.From = At + Facing * 1600.0 + Side * 120.0;
			GLook.To = At - Facing * 1400.0 + Side * 120.0;   // past a look back's reach, so it is seen to end
			GLook.From.Z = Z;
			GLook.To.Z = Z;
			GLook.StartAt = World->GetTimeSeconds() + 3.0;   // three seconds at the start, for her regard to be read
			GLook.State = 1;
			GLook.bFilm = FParse::Param(FCommandLine::Get(), TEXT("LookCamera"));
			if (!FParse::Value(FCommandLine::Get(), TEXT("LookFrames="), GLook.Frames)) { GLook.Frames = FPaths::ProjectSavedDir() / TEXT("LookScript"); }
			GLook.Frames = FPaths::ConvertRelativePathToFull(GLook.Frames / FString::Printf(TEXT("frames-%s"), GLook.Story.IsEmpty() ? TEXT("none") : *GLook.Story));
			if (GLook.bFilm)
			{
				// OUT IN THE ROAD AHEAD OF HER AND ABOVE HIS HEAD, the first place
				// from which rays to her head and shoulders meet nothing but her
				// and his walk passes below the line to her face (the second
				// review: from nine metres up the pavement a post stood between
				// the lens and her, on exactly his side). She faces along the
				// pavement, the shop wall at her other side; he walks towards
				// her, past her and away. The lens holds her head and shoulders
				// and him beside her as he passes.
				const FVector Head = At + FVector(0.0, 0.0, 158.0);
				TArray<AActor*> Skip;
				Skip.Add(Her);
				Skip.Add(GW1Body);
				Skip.Add(GPawn);
				Her->GetAttachedActors(Skip, false, true);
				GW1Body->GetAttachedActors(Skip, false, true);
				GPawn->GetAttachedActors(Skip, false, true);
				FString Blocked;
				FCollisionQueryParams Q(TEXT("LedgerLookCamera"), /*bTraceComplex=*/true);
				Q.AddIgnoredActors(Skip);
				const double HisHeadZ = Z + GPawn->BaseEyeHeight + 12.0;
				auto Clear = [&](const FVector& E, bool bOfHim) -> bool
				{
					if (World->OverlapAnyTestByChannel(E, FQuat::Identity, ECC_Visibility, FCollisionShape::MakeSphere(30.0f), Q))
					{
						if (Blocked.IsEmpty()) { Blocked = TEXT("(the lens inside something)"); }
						return false;
					}
					const FVector Across = FVector::CrossProduct(FVector::UpVector, Head - E).GetSafeNormal();
					const FVector Down(0.0, 0.0, 35.0);
					const FVector Aims[] = { Head, Head + Across * 18.0, Head - Across * 18.0, Head - Down + Across * 25.0, Head - Down - Across * 25.0 };
					for (const FVector& T : Aims)
					{
						// A hit within a hand of where the ray is aimed is her.
						FHitResult H;
						if (World->LineTraceSingleByChannel(H, E, T, ECC_Visibility, Q) && (H.ImpactPoint - T).Size() > 25.0)
						{
							if (Blocked.IsEmpty()) { Blocked = H.GetActor() != nullptr ? H.GetActor()->GetName() : TEXT("?"); }
							return false;
						}
					}
					for (double Along = -400.0; bOfHim && Along <= 800.0; Along += 40.0)
					{
						FVector Him = At + Facing * Along + Side * 120.0;
						Him.Z = HisHeadZ;
						if ((FMath::ClosestPointOnSegment(Him, E, Head) - Him).Size() < 30.0) { return false; }
					}
					return true;
				};
				const double Fs[] = { 400.0, 300.0, 500.0, 600.0 };
				const double Ss[] = { 380.0, 300.0, 460.0 };
				const double Us[] = { 140.0, 110.0, 180.0 };
				FVector Eye = Head + Facing * 400.0 + Side * 380.0 + FVector(0.0, 0.0, 140.0);
				int32 Found = 0;
				for (int32 Pass = 0; Pass < 2 && Found == 0; ++Pass)
				{
					for (const double U : Us) { for (const double S : Ss) { for (const double F : Fs)
					{
						const FVector E = Head + Facing * F + Side * S + FVector(0.0, 0.0, U);
						if (Found == 0 && Clear(E, Pass == 0)) { Eye = E; Found = Pass + 1; }
					} } }
				}
				UE_LOG(LogTemp, Display, TEXT("LedgerLookScript: camera %s at %s (first in the way: %s)"),
					Found == 1 ? TEXT("clear of the street and of him") : Found == 2 ? TEXT("clear of the street only") : TEXT("NOT CLEAR"),
					*(Eye - Head).ToString(), Blocked.IsEmpty() ? TEXT("nothing") : *Blocked);
				const FVector Look = Head - FVector(0.0, 0.0, 20.0);
				const double Dist = (Look - Eye).Size();
				FActorSpawnParameters P;
				P.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
				if (ACameraActor* Cam = World->SpawnActor<ACameraActor>(Eye, (Look - Eye).Rotation(), P))
				{
					// about two and a half metres across at her
					Cam->GetCameraComponent()->SetFieldOfView((float)FMath::RadiansToDegrees(2.0 * FMath::Atan(130.0 / Dist)));
					Cam->GetCameraComponent()->bConstrainAspectRatio = false;
					if (APlayerController* PC = World->GetFirstPlayerController()) { PC->SetViewTargetWithBlend(Cam, 0.0f); }
				}
				// NO MOTION BLUR in the film: at five frames a second a quick turn
				// smeared the face.
				if (GEngine != nullptr) { GEngine->Exec(World, TEXT("r.MotionBlurQuality 0")); }
				GSayInstructions = false;
				GSubs.RemoveAll([](const FSubLine& L) { return L.Colour == FLinearColor(FColor::Yellow); });
				SubsRebuild();
			}
			UE_LOG(LogTemp, Display, TEXT("LedgerLookScript: walking past Sheila, story=%s"), GLook.Story.IsEmpty() ? TEXT("none") : *GLook.Story);
		}
		const FVector Dir = (GLook.To - GLook.From).GetSafeNormal();
		const double Len = (GLook.To - GLook.From).Size();
		const double WNow = World->GetTimeSeconds();
		const double Along = FMath::Clamp((WNow - GLook.StartAt) * 140.0, 0.0, Len);
		const FVector Pos = GLook.From + Dir * Along;
		GPawn->SetActorLocationAndRotation(Pos, Dir.Rotation(), false, nullptr, ETeleportType::TeleportPhysics);
		if (APlayerController* PC = World->GetFirstPlayerController()) { PC->SetControlRotation(FRotator(-8.0f, (float)Dir.Rotation().Yaw, 0.0f)); }
		if (GLook.bFilm && WNow - GLook.LastFrame >= 0.099 && WNow >= GLook.StartAt - 1.0)
		{
			GLook.LastFrame = WNow;
			FScreenshotRequest::RequestScreenshot(GLook.Frames / FString::Printf(TEXT("f_%03d.png"), GLook.Frame++), true, false);   // with the subtitles
		}
		AActor* Her = GVisualFor(GW1Body);
		ULedgerPersonAnim* Look = nullptr;
		if (TArray<TWeakObjectPtr<ULedgerPersonAnim>>* Looks = GLooks.Find(GW1Body))
		{
			for (const TWeakObjectPtr<ULedgerPersonAnim>& L : *Looks) { if (L.IsValid() && !L->HeadBone.IsNone()) { Look = L.Get(); break; } }
		}
		if (Her != nullptr && WNow - GLook.LastRow >= 0.25)
		{
			GLook.LastRow = WNow;
			const FVector To = Pos - Her->GetActorLocation();
			const double Ahead = FVector::DotProduct(To, Her->GetActorRightVector().GetSafeNormal2D()) / 100.0;
			const double M = To.Size2D() / 100.0;
			const float Alpha = Look != nullptr ? Look->LookAlpha : -1.0f;
			GLook.Rows += FString::Printf(TEXT("%s{\"t\":%.2f,\"ahead\":%.2f,\"m\":%.2f,\"alpha\":%.2f,\"first\":%d,\"second\":%d,\"back\":%d}"),
				GLook.Rows.IsEmpty() ? TEXT("") : TEXT(","), WNow - GLook.StartAt, Ahead, M, Alpha,
				Look != nullptr ? (int)Look->bFirstGiven : -1, Look != nullptr ? (int)Look->bSecondGiven : -1,
				Look != nullptr ? (int)Look->bLookingBack : -1);
			if (Look != nullptr && Look->bFirstGiven && Alpha > 0.6f) { LookShot(TEXT("1-first")); }
			if (Ahead > 1.5 && Ahead < 2.5) { LookShot(TEXT("2-close")); }
			if (Ahead < 0.3 && Ahead > -0.7) { LookShot(TEXT("3-passing")); }
			if (Look != nullptr && Look->bLookingBack && Alpha > 0.6f) { LookShot(TEXT("4-back")); }
		}
		if (Along >= Len && WNow - GLook.StartAt > Len / 140.0 + 2.0)
		{
			int32 First = 0, Second = 0, Back = 0, People = 0;
			for (TObjectIterator<ULedgerPersonAnim> It; It; ++It)
			{
				if (It->GetWorld() != World || !It->bLook) { continue; }
				++People; First += It->FirstLooks; Second += It->SecondLooks; Back += It->LooksBackGiven;
			}
			const StreetVoice::Regard* R = GLive.Regards.count("lena") ? &GLive.Regards["lena"] : nullptr;
			const FString Json = FString::Printf(TEXT("{\"story\":\"%s\",\"stance\":\"%s\",\"knowing\":\"%s\",\"linesSaid\":%d,\"faintSaid\":%d,")
				TEXT("\"heads\":%d,\"firstLooks\":%d,\"secondLooks\":%d,\"looksBack\":%d,\"rows\":[%s]}"),
				GLook.Story.IsEmpty() ? TEXT("none") : *GLook.Story,
				R != nullptr ? UTF8_TO_TCHAR(StreetVoice::StanceName(R->Stance)) : TEXT("none"),
				R != nullptr ? UTF8_TO_TCHAR(StreetVoice::KnowingName(R->HowMuch)) : TEXT("none"),
				GLive.LinesSaid, GLive.FaintSaid, People, First, Second, Back, *GLook.Rows);
			FFileHelper::SaveStringToFile(Json, *(FPaths::ProjectLogDir() / TEXT("look-script.json")));
			UE_LOG(LogTemp, Display, TEXT("LedgerLookScript: done, heads=%d firstLooks=%d secondLooks=%d looksBack=%d lines=%d"),
				People, First, Second, Back, GLive.LinesSaid);
			GLook.State = -1;
			FPlatformMisc::RequestExit(false);
		}
	}

	// ---- THE CONSEQUENCE, in free play (Jafar's list of 30 September, item
	// 1; the town's card, production/handovers/6ar-after-a-deed.md) ----------
	// At the deed: the damage, which whoever comes by finds in the morning and
	// the street takes up as news naming nobody (never those who saw it done),
	// and a report from each who saw it and would go to the police. Every game
	// hour: the damage found. Each morning at nine: whether DS Ellis comes
	// asking; at ten, whether a constable takes him. All of it saved with the
	// story (town.json, the town's own TownSave).

	// HELD UNTIL: set when a constable takes him, so the hours in the cells
	// pass once the hour that took him is done (never inside another hour).
	bool bHeldPending = false;
	GameTime GHeldUntil;

	// TEN O'CLOCK: a constable, for a deed a witness gave a statement about (the
	// card, step 4; ROUTE.md step 6, TownWeek::TenConstable). He is taken
	// where he stands; the street that sees it has it to talk of; the arrest
	// words, then his rights; the hours in the cells pass (the town's hours
	// running meanwhile); and he is let go with plain words.
	void ConstableHour(const GameTime& H)
	{
		std::string Area = "mickeys";
		if (GPawn != nullptr && bGCast)
		{
			const LedgerCrime::P3 At = ToStreet(GPawn->GetActorLocation());
			const std::string Place = GCast.NearestPlace(At.X, At.Z, 30.0);
			if (!Place.empty()) { GCast.AreaOf(Place, Area); }
		}
		const std::shared_ptr<Custody> C = GWeek.TenConstable(GMill.get(), &GCast, H, Area);
		if (!C) { return; }
		Say(FString(TEXT("A constable: \"")) + Un(C->ArrestWords()) + TEXT("\""), 14.0f, FColor::White);
		Say(FString(TEXT("At the station: ")) + Un(std::string(Custody::Rights)), 14.0f, FColor::Yellow);
		LedgerSession::Write(TEXT("taken"), TEXT("\"story\":") + LedgerSession::Str(Un(GWeek.DeedTopic)) + TEXT(",\"day\":") + FString::FromInt(H.Day)
			+ TEXT(",\"end\":") + LedgerSession::Str(Un(C->OutAt().ToString())));
		UE_LOG(LogTemp, Display, TEXT("LedgerAfter: taken at %s in %s, out at %s"), *Un(H.ToString()), *Un(Area), *Un(C->OutAt().ToString()));
		bHeldPending = true;
		GHeldUntil = C->OutAt();
	}


	// Who holds the deed first-hand, with the rung they saw him at.
	std::vector<std::pair<GossiperPtr, int> > DeedWitnesses()
	{
		std::vector<std::pair<GossiperPtr, int> > Out;
		if (!GMill) { return Out; }
		for (const GossiperPtr& G : GMill->Agents())
		{
			if (!G) { continue; }
			for (const RumorPtr& R : G->Rumors)
			{
				if (R && R->TopicKey() == GWindowTopic && R->Hops == 0) { Out.push_back({ G, R->OriginRung }); break; }
			}
		}
		return Out;
	}

	void DeedFollows()
	{
		if (bLiveScript || !GMill || !bGCast) { return; }
		GWindowTopic = "player.window_d" + std::to_string(GNow.Day);
		std::vector<std::pair<std::string, int> > Saw;
		for (const auto& W : DeedWitnesses()) { Saw.push_back({ W.first->Id, W.second }); }
		// ROUTE.md step 2: the damage (which those who saw it done never
		// "find") and who saw it, at the rung they saw him at; their stories
		// were filed as they saw it (ResolveAndFile), so the mill is not passed.
		const std::vector<std::string> Heard(GHeardOnly.begin(), GHeardOnly.end());
		GWeek.Deed(nullptr, GNow, "ritas", "rita_window", "somebody put Rita's window in", Saw,
			"window_d" + std::to_string(GNow.Day), std::string(), 1.0, true, &Heard);
		UE_LOG(LogTemp, Display, TEXT("LedgerAfter: the deed at %s (%s): %d saw it, the damage kept"),
			*Un(GNow.ToString()), *Un(GWindowTopic), (int32)Saw.size());
	}

	// ONE GAME HOUR OF THE TOWN'S WEEK (ROUTE.md section 1), in the Core's
	// order: six o'clock the asks' nights passed, the damage found, nine the
	// witnesses to the police (once each, from the day after it) and DS Ellis,
	// ten the constable and Ada's invitation, eight in the evening Ron at the
	// door, eleven the tea's close, then the week's end and the town's talk.
	void ConsequenceHour(const GameTime& H)
	{
		if (bLiveScript || !GMill || !bGCast) { return; }
		GWeek.Six(GMill.get(), H);
		for (const auto& Found : GWeek.DamageTick(GMill.get(), &GCast, H))
		{
			UE_LOG(LogTemp, Display, TEXT("LedgerAfter: %s finds the damage at %s"), *Un(Found.first), *Un(Found.second.ToString()));
		}
		for (const std::string& Who : GWeek.NineReports(GMill.get(), &GCast, H))
		{
			LedgerSession::Write(TEXT("police"), TEXT("\"who\":") + LedgerSession::Str(Un(Who)) + TEXT(",\"story\":") + LedgerSession::Str(Un(GWeek.DeedTopic)));
			UE_LOG(LogTemp, Display, TEXT("LedgerAfter: %s goes to the police about %s on day %d"), *Un(Who), *Un(GWeek.DeedTopic), H.Day);
		}
		const std::string Why = GWeek.NineEllis(GMill.get(), H, &GCast);
		if (!Why.empty())
		{
			Say(TEXT("DS Ellis is on Quay Street this morning, asking after you."), 8.0f, FColor::Yellow);
			LedgerSession::Write(TEXT("ellis"), TEXT("\"why\":") + LedgerSession::Str(Un(Why)) + TEXT(",\"day\":") + FString::FromInt(H.Day));
			UE_LOG(LogTemp, Display, TEXT("LedgerAfter: DS Ellis comes on day %d for %s"), H.Day, *Un(Why));
		}
		ConstableHour(H);
		std::string Invite;
		if (GWeek.TenTea(H, Invite))
		{
			Say(FString(TEXT("Ada, from her step: \"")) + Un(Invite) + TEXT("\""), 12.0f, FColor::White);
			UE_LOG(LogTemp, Display, TEXT("LedgerWeek: Ada asks him in for tea on day %d"), H.Day);
		}
		if (GWeek.TwentyRon(GMill.get(), H))
		{
			GMet.Met("rocco", H.Day);
			Say(TEXT("Ron's at the door with an envelope for you: for the ferry landing, after ten tonight, to the man who asks for Mickey's. The way down is past the quay at the bottom of the street."), 14.0f, FColor::Yellow);
			LedgerSession::Write(TEXT("ask"), TEXT("\"night\":") + FString::FromInt(H.Day));
			UE_LOG(LogTemp, Display, TEXT("LedgerWeek: Ron brings the envelope on night %d"), H.Day);
		}
		GWeek.TwentyThreeTea(GMill.get(), H);
		GWeek.HourEnd(GMill.get(), &GCast, H);
		WindowLook();
	}

	// RITA'S WINDOW LOOKS AS THE TOWN'S DAMAGE RECORD SAYS (30 September, the
	// AI tester: broken on day 3 though the glazier had mended it on day 1,
	// and whole after a reload whatever the hour): broken from the deed
	// until its mend (Aftermath: boarded that morning, the glazier by four
	// the working day after), whole after; on a load, whichever is true.
	int GWindowLooksBroken = -1;
	void WindowLook()
	{
		if (bLiveScript || !bRitasWindow || GGlass[0] == nullptr) { return; }
		bool bBroken = false;
		for (const Aftermath& A : GWeek.Damage)
		{
			if (A.Key() == "rita_window" && GNow.TotalMinutes() >= A.DoneAt().TotalMinutes() && GNow.TotalMinutes() < A.MendedAt().TotalMinutes()) { bBroken = true; }
		}
		if ((int)bBroken == GWindowLooksBroken) { return; }
		AActor* Glass = GGlass[0];
		// THE SCENE FILE'S PANE AS IT STARTED (the AI tester, 30 September, in
		// the packaged game: shown whole, it stood as a dark tiled panel over
		// Rita's front, since the street's own glass is what is seen and that
		// pane starts hidden). Whole puts it back as it was; broken hides it.
		if (GWindowLooksBroken < 0 && !bWindowGlassStartRead)
		{
			bWindowGlassStartRead = true;
			bWindowGlassStartHidden = Glass->IsHidden();
			bWindowGlassStartCollides = Glass->GetActorEnableCollision();
		}
		GWindowLooksBroken = bBroken ? 1 : 0;
		Glass->SetActorHiddenInGame(bBroken || bWindowGlassStartHidden);
		Glass->SetActorEnableCollision(!bBroken && bWindowGlassStartCollides);
		const FBox Box = Glass->GetComponentsBoundingBox(true);
		int32 Panes = 0, Pieces = 0;
		if (bBroken)
		{
			Panes = LedgerVignetteShot::HideStreetGlassNear(Box);
			Pieces = LedgerVignetteShot::RevealStreetMeshes("crime_r");
		}
		else
		{
			Panes = LedgerVignetteShot::ShowStreetGlassNear(Box);
			Pieces = LedgerVignetteShot::HideStreetMeshes("crime_r");
			for (const TWeakObjectPtr<AActor>& D : GWindowDebris) { if (D.IsValid()) { D->SetActorHiddenInGame(true); D->SetActorEnableCollision(false); } }
		}
		UE_LOG(LogTemp, Display, TEXT("LedgerAfter: Rita's window %s at %s (%d panes, %d pieces)"),
			bBroken ? TEXT("broken") : TEXT("whole"), *Un(GNow.ToString()), Panes, Pieces);
	}

	// WHERE HE STANDS, for the week: at Ada's step (her tea's minutes), at the
	// quay (the way down to the landing), at Mickey's (Sheila's question).
	bool NearPlace(const char* Place, double Metres)
	{
		double X = 0.0, Z = 0.0;
		if (GPawn == nullptr || !bGCast || !GCast.PlaceXZ(Place, X, Z)) { return false; }
		const LedgerCrime::P3 At = ToStreet(GPawn->GetActorLocation());
		return (At.X - X) * (At.X - X) + (At.Z - Z) * (At.Z - Z) <= Metres * Metres;
	}
	bool AtAdasNow() { return NearPlace("adas_step", 4.0); }

	// WHAT HE DOES IN THE WEEK, A FRAME AT A TIME (ROUTE.md steps 9 to 11):
	// each minute at Ada's step between nine and eleven on the tea's day is a
	// minute with her; on an ask night from ten, with the envelope and the
	// night unanswered, going down past the quay is the envelope handed over
	// (and on the tea's night, leaving her for it).
	int GTeaMinuteDone = -1;
	void WeekTick()
	{
		if (bLiveScript || !bClockRuns || !GMill || !bGCast || GWeek.Holding(GNow)) { return; }
		if (GWeek.Tea && GNow.Day == GWeek.Tea->Day() && GNow.Hour >= AdasTea::From && GNow.Hour < AdasTea::Until && AtAdasNow())
		{
			const int M = GNow.Hour * 60 + GNow.Minute;
			if (M != GTeaMinuteDone)
			{
				if (GTeaMinuteDone < 0) { UE_LOG(LogTemp, Display, TEXT("LedgerWeek: with Ada from %s"), *Un(GNow.ToString())); }
				GTeaMinuteDone = M;
				GWeek.Tea->WithHer(GNow);
				GMet.Met("ada", GNow.Day);
			}
		}
		const int Night = Arrangement::NightOf(GNow);
		if (GWeek.Asks.AskStands(GNow) && (GNow.Hour >= Waiting::LandingFrom || GNow.Hour < Arrangement::GaveUpHour) && NearPlace("quay", 8.0))
		{
			if (GWeek.Tea && Night == GWeek.Tea->Day()) { GWeek.Tea->WentToTheLanding(GMill.get(), GNow, true); }
			if (GWeek.AnswerAsk(Night, NightAnswer::Did, GMill.get(), GNow))
			{
				Say(TEXT("Down at the ferry landing a man asks for Mickey's. You hand him the envelope."), 10.0f, FColor::Yellow);
				LedgerSession::Write(TEXT("landing"), TEXT("\"night\":") + FString::FromInt(Night));
				UE_LOG(LogTemp, Display, TEXT("LedgerWeek: the envelope handed over at the landing, night %d, %s"), Night, *Un(GNow.ToString()));
			}
		}
	}

	// THE CLOCK, A FRAME AT A TIME (LiveClock.h): held while he talks (the box
	// open, or a reply on its way) and during Sheila's walk-round; each hour it
	// crosses is kept (an autosave, so a reload finds the street where he left
	// it), and the street's light follows the hour: night from seven in the
	// evening to seven in the morning, late September in the north.
	void ClockHours(const std::vector<GameTime>& Hours)
	{
		for (const GameTime& H : Hours)
		{
			UE_LOG(LogTemp, Display, TEXT("LedgerClock: %s (phase %d)"), *Un(H.ToString()), (int32)GPhase);
			ConsequenceHour(H);
		}
		if (!Hours.empty()) { SaveEncounterToDisk(); }
		// HIS HOURS IN THE CELLS, after the hour that took him: the clock goes to
		// his release, the town's hours running on, and the release words show.
		if (bHeldPending)
		{
			bHeldPending = false;
			const std::vector<GameTime> Held = GClock.JumpTo(GHeldUntil);
			GNow = GClock.Now();
			ClockHours(Held);
			if (GWeek.Latest()) { Say(Un(GWeek.Latest()->ReleaseWords()), 14.0f, FColor::Yellow); }
		}
	}

	// THE THREE THE PLAYER CAN SEE KEEP THEIR DAY (the independent review of
	// 30 September, A2): each hour Sheila, Darren and Ron stand where their
	// routine puts them on Quay Street (a place indoors from its own pavement
	// until the interiors are built), and leave the street when their day
	// does. Never while he talks with them or waits on their reply, and never
	// in front of his eyes: a move waits until neither where they stand nor
	// where they go is in his view (except on a new game or a Continue).
	std::map<std::string, int> GPlacedFor;
	std::set<std::string> GAway;
	std::map<std::string, double> GHeldBackSince;   // when a move first waited for his eyes
	bool bPlaceNow = false;
	// A MOVE WAITS FOR HIS EYES ONLY SO LONG (the independent check of 30
	// September: walking towards somebody, he would never see them go or come).
	constexpr double kPlaceWaitSeconds = 12.0;

	// THE FLOOR UNDER SOMEBODY'S FEET: searched from a metre up, never from
	// four (the first walk of 30 September stood Ron and Sheila on the shop
	// fronts' overhang by Mickey's), ignoring him and the three people.
	double FeetYAt(UWorld* World, double X, double Z)
	{
		if (World == nullptr) { return 0.1; }
		FCollisionQueryParams Params;
		Params.bTraceComplex = false;
		if (GPawn != nullptr) { Params.AddIgnoredActor(GPawn); }
		for (const char* C : { "lena", "sam", "rocco" }) { if (AActor* B = CardBody(C)) { Params.AddIgnoredActor(B); Params.AddIgnoredActor(GVisualFor(B)); } }
		FHitResult Hit;
		if (!World->LineTraceSingleByChannel(Hit, ToUE(LedgerCrime::P3(X, 1.0, Z)), ToUE(LedgerCrime::P3(X, -1.0, Z)), ECC_Visibility, Params)) { return 0.1; }
		return (double)Hit.ImpactPoint.Z / 100.0;
	}

	void PlaceBodyAt(AActor* Body, double X, double Z, double GroundY)
	{
		if (Body == nullptr) { return; }
		Body->SetActorLocation(ToUE(LedgerCrime::P3(X, GroundY + LedgerCrime::kBodyHeightM * 0.5, Z)));
		SyncVisual(Body);
	}

	void ShowPerson(AActor* Body, bool bShow)
	{
		TWeakObjectPtr<AActor>* V = GVisuals.Find(Body);
		if (V == nullptr || !V->IsValid()) { return; }
		(*V)->SetActorHiddenInGame(!bShow);
		TArray<AActor*> Worn;
		(*V)->GetAttachedActors(Worn, true, true);
		for (AActor* W : Worn) { if (W != nullptr) { W->SetActorHiddenInGame(!bShow); } }
	}

	bool InHisView(UWorld* World, const FVector& At)
	{
		APlayerController* PC = World != nullptr ? World->GetFirstPlayerController() : nullptr;
		if (PC == nullptr) { return false; }
		FVector Eye;
		FRotator Look;
		PC->GetPlayerViewPoint(Eye, Look);
		const FVector To = At - Eye;
		if (To.Size() > 6000.0f) { return false; }
		return FVector::DotProduct(To.GetSafeNormal(), Look.Vector()) > 0.64f;   // within about 50 degrees of where he looks
	}

	void PlaceBodiesByRoutine(UWorld* World)
	{
		if (!bRitasWindow || bLiveScript || !bGCast || GEnc != EEncounter::Live || World == nullptr) { return; }
		if (GPhase == ECrimePhase::LiveWalkRound) { return; }
		const int Key = GNow.Day * 24 + GNow.Hour;
		const char* Cards[3] = { "lena", "sam", "rocco" };
		bool bAny = false;
		for (const char* C : Cards) { if (GPlacedFor.count(C) == 0 || GPlacedFor[C] != Key) { bAny = true; } }
		if (!bAny) { return; }
		std::map<std::string, LedgerCrime::OnlookerAt> Here;
		for (const LedgerCrime::OnlookerAt& O : LedgerCrime::OnlookersAt(GCast, GNow.Day, GNow.Hour, { "lena", "sam", "rocco" }))
		{
			if (O.bBody) { Here[O.Id] = O; }
		}
		// HER APPOINTMENT OUTRANKS HER DAY OFF: the week's end keeps Sheila at the
		// office for him on the Sunday morning, and while her question stands.
		double OfficeX = 0.0, OfficeZ = 0.0;
		if (GWeek.Week.Waits(GNow) && GCast.PlaceXZ("mickeys_office", OfficeX, OfficeZ))
		{
			LedgerCrime::OnlookerAt O;
			O.Id = "lena";
			O.Place = "mickeys_office";
			O.bBody = true;
			O.At = LedgerCrime::BodySpotFor(OfficeX, OfficeZ);
			O.YawDeg = LedgerCrime::StreetFacingYaw(O.At.X, O.At.Z);
			Here["lena"] = O;
		}
		for (const char* C : Cards)
		{
			if (GPlacedFor.count(C) && GPlacedFor[C] == Key) { continue; }
			AActor* Body = CardBody(C);
			if (Body == nullptr) { GPlacedFor[C] = Key; continue; }
			if ((bSayOpen && GTalkTarget.Card == C) || (GLive.PendingId != 0 && GLive.PendingBody == Body)
			    || (GLive.Talked.count(C) && !GLive.Left.count(C))) { continue; }
			const auto It = Here.find(C);
			const bool bWaitedEnough = GHeldBackSince.count(C) && NowS() - GHeldBackSince[C] >= kPlaceWaitSeconds;
			if (It == Here.end())
			{
				if (!bPlaceNow && !bWaitedEnough && !GAway.count(C) && InHisView(World, Body->GetActorLocation()))
				{
					if (!GHeldBackSince.count(C)) { GHeldBackSince[C] = NowS(); }
					continue;
				}
				GHeldBackSince.erase(C);
				PlaceBodyAt(Body, -400.0, -400.0, 0.0);
				ShowPerson(Body, false);
				GAway.insert(C);
				GPlacedFor[C] = Key;
				UE_LOG(LogTemp, Display, TEXT("LedgerDay: %s off the street at %s"), *Un(C), *Un(GNow.ToString()));
				continue;
			}
			double X = It->second.At.X, Z = It->second.At.Z;
			// NEVER ONTO ANOTHER OF THE THREE, wherever they stand now (placed this
			// hour or held back by a conversation).
			for (int Pass = 0; Pass < 2; ++Pass)
			{
				for (const char* Other : Cards)
				{
					AActor* OtherBody = CardBody(Other);
					if (std::string(Other) == C || OtherBody == nullptr || GAway.count(Other)) { continue; }
					const LedgerCrime::P3 There = ToStreet(OtherBody->GetActorLocation());
					if (std::fabs(There.X - X) < 0.9 && std::fabs(There.Z - Z) < 0.9) { X += 1.1; }
				}
			}
			if (GPawn != nullptr)
			{
				const LedgerCrime::P3 Him = ToStreet(GPawn->GetActorLocation());
				if (std::fabs(Him.X - X) < 1.0 && std::fabs(Him.Z - Z) < 1.0) { X += 1.2; }
			}
			const FVector Goes = ToUE(LedgerCrime::P3(X, 1.0, Z));
			const bool bAppointment = It->second.Place == "mickeys_office" && std::string(C) == "lena" && GWeek.Week.Waits(GNow);
			if (!bPlaceNow && !bWaitedEnough && !bAppointment
			    && ((!GAway.count(C) && InHisView(World, Body->GetActorLocation())) || InHisView(World, Goes)))
			{
				if (!GHeldBackSince.count(C)) { GHeldBackSince[C] = NowS(); }
				continue;
			}
			GHeldBackSince.erase(C);
			PlaceBodyAt(Body, X, Z, FeetYAt(World, X, Z));
			Body->SetActorRotation(FRotator(0.0f, (float)It->second.YawDeg, 0.0f));
			SyncVisual(Body);
			ShowPerson(Body, true);
			GAway.erase(C);
			GPlacedFor[C] = Key;
			UE_LOG(LogTemp, Display, TEXT("LedgerDay: %s at %s (%.1f, %.1f) at %s"), *Un(C), *Un(It->second.Place), X, Z, *Un(GNow.ToString()));
		}
		bPlaceNow = false;
	}

	// GLASS IS SEEN THROUGH: a sightline that meets a pane goes on past it; so
	// does the painted interior card behind a shop window, which stands for the
	// room the people at the counter are in (the first walk of 30 September:
	// Rita and her staff were blind behind street_card_int23_pawn).
	bool TraceBlockedPastGlass(UWorld* World, const FVector& From, const FVector& To,
	                           const AActor* IgnoreA, const AActor* IgnoreB,
	                           std::string& OutBlocker, double& OutLenCm)
	{
		OutBlocker = "none";
		OutLenCm = (double)FVector::Dist(From, To);
		if (World == nullptr) { return false; }
		FCollisionQueryParams Params;
		Params.bTraceComplex = false;
		if (IgnoreA != nullptr) { Params.AddIgnoredActor(IgnoreA); }
		if (IgnoreB != nullptr) { Params.AddIgnoredActor(IgnoreB); }
		for (int Pass = 0; Pass < 6; ++Pass)
		{
			FHitResult Hit;
			if (!World->LineTraceSingleByChannel(Hit, From, To, ECC_Visibility, Params)) { return false; }
			const std::string Name = BlockerName(Hit.GetActor());
			if ((Un(Name).Contains(TEXT("glass")) || Un(Name).Contains(TEXT("_card_int"))) && Hit.GetActor() != nullptr) { Params.AddIgnoredActor(Hit.GetActor()); continue; }
			OutBlocker = Name;
			OutLenCm = (double)FVector::Dist(From, Hit.ImpactPoint);
			return true;
		}
		OutBlocker = "past-six-panes";   // never read as a clear line without looking further
		return true;
	}

	// THE LIGHT ON HIM NOW: the game's night (19:00 to 07:00) and the reach of
	// the lamps the street has lit around his head, as Perceivers.LevelAt adds them.
	double LampReachAt(UWorld* World, const FVector& At, std::string& OutLamp)
	{
		double Best = 0.0;
		OutLamp = "none";
		for (TObjectIterator<ULocalLightComponent> It; It; ++It)
		{
			const ULocalLightComponent* L = *It;
			if (L == nullptr || L->GetWorld() != World || !L->IsVisible() || L->Intensity <= 0.0f) { continue; }
			if (L->GetName().StartsWith(TEXT("Talk"))) { continue; }   // the conversation light (LedgerTalkLight.h) lights a face, not the street
			if (L->GetOwner() != nullptr && L->GetOwner()->IsHidden()) { continue; }
			const double Radius = (double)L->AttenuationRadius;
			if (Radius <= 1.0) { continue; }
			const double D = (double)FVector::Dist(L->GetComponentLocation(), At);
			if (D >= Radius) { continue; }
			const double Reach = 1.0 - D / Radius;
			if (Reach > Best) { Best = Reach; OutLamp = BlockerName(L->GetOwner()); }
		}
		return Best;
	}

	// ONE ONLOOKER'S VANTAGE, as MeasureVantage takes the regression's, from
	// where they stand (their body, or their place behind their window).
	LedgerCrime::Reading MeasureOnlooker(UWorld* World, const LedgerCrime::OnlookerAt& O, AActor* Body, AActor* Glass)
	{
		LedgerCrime::Reading R;
		R.WitnessId = O.Id;
		R.EventId = "A";
		R.SecondsWatching = LedgerCrime::kDeedSeconds;
		R.VantageAt = Body != nullptr ? "before-the-deed/glass-standing/where-he-sees-them" : "before-the-deed/glass-standing/behind-their-window";
		if (GPawn == nullptr) { R.FiledReason = "nothing-measured"; return R; }
		LedgerCrime::P3 Feet;
		if (Body != nullptr)
		{
			const FBox BodyBox = Body->GetComponentsBoundingBox();
			Feet = ToStreet(FVector(BodyBox.GetCenter().X, BodyBox.GetCenter().Y, BodyBox.Min.Z));
			R.WitnessYawDeg = (double)Body->GetActorRotation().Yaw;
		}
		else
		{
			Feet = LedgerCrime::P3(O.At.X, FeetYAt(World, O.At.X, O.At.Z), O.At.Z);
			R.WitnessYawDeg = O.YawDeg;
		}
		R.WitnessAt = Feet;
		R.EyeAt = LedgerCrime::P3(Feet.X, Feet.Y + LedgerCrime::kEyeHeightM, Feet.Z);
		const FBox PawnBox = GPawn->GetComponentsBoundingBox();
		const FVector HeadUE(PawnBox.GetCenter().X, PawnBox.GetCenter().Y, PawnBox.Max.Z - 10.0f);
		R.ActorHeadAt = ToStreet(HeadUE);
		R.ActorYawDeg = (double)GPawn->GetActorRotation().Yaw;
		const FVector EyeUE = ToUE(R.EyeAt);
		R.ActorMetres = LedgerCrime::Metres(R.EyeAt, R.ActorHeadAt);
		R.ActorOffAxisDeg = LedgerCrime::OffAxisDeg(R.EyeAt, R.WitnessYawDeg, R.ActorHeadAt);
		R.bActorOccluded = TraceBlockedPastGlass(World, EyeUE, HeadUE, Body, GPawn, R.ActorBlocker, R.ActorTraceLenCm);
		if (Glass == nullptr) { R.VictimBlocker = "no-window-asked-for"; return R; }
		const FVector VictimUE = Glass->GetComponentsBoundingBox(true).GetCenter();
		R.VictimAt = ToStreet(VictimUE);
		R.VictimMetres = LedgerCrime::Metres(R.EyeAt, R.VictimAt);
		R.VictimOffAxisDeg = LedgerCrime::OffAxisDeg(R.EyeAt, R.WitnessYawDeg, R.VictimAt);
		R.bVictimOccluded = TraceBlockedPastGlass(World, EyeUE, VictimUE, Body, Glass, R.VictimBlocker, R.VictimTraceLenCm);
		return R;
	}

	// THE ONLOOKERS AT A DEED IN PLAY (A2 and A4): whoever is really there at
	// this hour, from where they stand, in this hour's light, knowing his face
	// as well as their meetings with him allow.
	void DeedOnlookers(UWorld* World)
	{
		std::string Lamp;
		const FVector Head = GPawn != nullptr ? GPawn->GetComponentsBoundingBox().GetCenter() : FVector::ZeroVector;
		const bool bNight = LedgerCrime::NightAt(GNow.Hour);
		const double Reach = bNight ? LampReachAt(World, Head, Lamp) : 0.0;
		const double Light = LedgerCrime::LightOnHim(bNight, Reach);
		int Measured = 0;
		for (const LedgerCrime::OnlookerAt& O : LedgerCrime::OnlookersAt(GCast, GNow.Day, GNow.Hour, { "lena", "sam", "rocco" }))
		{
			AActor* Body = O.bBody ? CardBody(O.Id) : nullptr;
			if (O.bBody && (Body == nullptr || GAway.count(O.Id))) { continue; }
			LedgerCrime::Reading R = MeasureOnlooker(World, O, Body, GGlass[0]);
			R.Light = Light;
			R.Familiarity = LedgerCrime::FamiliarityFromMeetings(GMet.DaysMet(O.Id));
			UE_LOG(LogTemp, Display, TEXT("LedgerWitness: %s %s %s, %.1f m off-axis %.0f, sightline %s, light %.2f (lamp %s), met on %d day(s), familiarity %.2f"),
				*Un(O.Id), Body != nullptr ? TEXT("where he sees them, their day says") : TEXT("behind the window at"), *Un(O.Place), R.ActorMetres, R.ActorOffAxisDeg,
				*Un(R.bActorOccluded ? R.ActorBlocker : std::string("clear")), R.Light, *Un(Lamp), GMet.DaysMet(O.Id), R.Familiarity);
			GReadings.push_back(R);
			++Measured;
		}
		// The three still standing where they stood when their day moved on
		// (a conversation, his eyes on them) are there, and are measured there.
		for (const char* C : { "lena", "sam", "rocco" })
		{
			bool bIn = false;
			for (const LedgerCrime::Reading& R : GReadings) { if (R.EventId == "A" && R.WitnessId == C) { bIn = true; } }
			AActor* Body = CardBody(C);
			if (bIn || Body == nullptr || GAway.count(C)) { continue; }
			LedgerCrime::OnlookerAt O;
			O.Id = C; O.Place = "where-he-sees-them"; O.bBody = true;
			LedgerCrime::Reading R = MeasureOnlooker(World, O, Body, GGlass[0]);
			R.Light = Light;
			R.Familiarity = LedgerCrime::FamiliarityFromMeetings(GMet.DaysMet(C));
			GReadings.push_back(R);
			++Measured;
		}
		LedgerSession::Write(TEXT("onlookers"), FString::Printf(TEXT("\"hour\":%d,\"night\":%s,\"light\":%.2f,\"measured\":%d"),
			GNow.Hour, bNight ? TEXT("true") : TEXT("false"), Light, Measured));
	}

	void ClockLight()
	{
		const int Night = (GNow.Hour >= 19 || GNow.Hour < 7) ? 1 : 0;
		if (Night == GLightNight) { return; }
		GLightNight = Night;
		UE_LOG(LogTemp, Log, TEXT("LedgerClock light at %s: %s"), *Un(GNow.ToString()),
			*LedgerVignetteShot::ApplyPlayCondition(Night ? kEveningCondition : "overcast_day"));
	}

	void ClockTick(double Delta)
	{
		if (!bClockRuns) { return; }
		const bool bHeld = bSayOpen || GLive.PendingId != 0 || GPhase == ECrimePhase::LiveWalkRound;
		const std::vector<GameTime> Hours = GClock.Advance(Delta, bHeld);
		GNow = GClock.Now();
		ClockHours(Hours);
		if (GPawn != nullptr) { PlaceBodiesByRoutine(GPawn->GetWorld()); }
		ClockLight();
		WeekTick();
	}

	void ClockCharge(int Minutes)
	{
		if (!bClockRuns) { return; }
		const std::vector<GameTime> Hours = GClock.JumpTo(GClock.Now().AddMinutes(Minutes));
		GNow = GClock.Now();
		ClockHours(Hours);
		ClockLight();
	}

	// A WAY TO WAIT (the town's card 6ci; Jafar's list, item 1): Z, when he is
	// not talking, passes time until the next thing the town has for him
	// (Waiting::Next: the police's calls for now; the asks, the tea and the
	// week's end as they are wired), or eight hours if nothing is due, the
	// town's hours running through it as through play. Each stop's line is
	// shown once (its key kept in the save). Refused during Sheila's walk-round.
	std::set<std::string> GWaitShown;
	constexpr int kWaitMinutes = 8 * 60;

	void WaitKeyTick(UWorld* World)
	{
		if (!bClockRuns || World == nullptr) { return; }
		// THROUGH THE PAWN'S OWN BINDING, as E and T are: a key sampled here
		// missed a quick press when the frame was slow (the tester, at night).
		ALedgerSliceCharacter* Slice = Cast<ALedgerSliceCharacter>(GPawn);
		const bool bPressed = Slice != nullptr && Slice->ConsumeWaitRequests() > 0;
		if (!bPressed || bSayOpen || GLive.PendingId != 0) { return; }
		WaitBeats B;
		B.Asks = &GWeek.Asks;
		B.Tea = GWeek.Tea.get();
		B.Police = &GWeek.Police;
		B.Mill = GMill.get();
		B.Week = &GWeek.Week;
		const std::shared_ptr<Custody> Held = GWeek.Holding(GNow);
		B.CustodyOf = Held.get();
		B.AtAdas = AtAdasNow();
		B.WalkRoundDone = bSheilaMet;
		B.Shown = GWaitShown;
		std::string Refused;
		if (Waiting::Refused(&B, Refused)) { Say(Un(Refused), 5.0f, FColor::Yellow); return; }
		const GameTime Until = GNow.AddMinutes(kWaitMinutes);
		WaitStop S;
		const bool bStop = Waiting::Next(GNow, Until, &B, S);
		const GameTime To = bStop ? S.At : Until;
		UE_LOG(LogTemp, Display, TEXT("LedgerWait: from %s to %s%s"), *Un(GNow.ToString()), *Un(To.ToString()),
			bStop ? *(FString(TEXT(", stopped: ")) + Un(S.Key)) : TEXT(""));
		LedgerSession::Write(TEXT("wait"), TEXT("\"from\":") + LedgerSession::Str(Un(GNow.ToString())) + TEXT(",\"to\":") + LedgerSession::Str(Un(To.ToString())));
		const GameTime From = GNow;
		const std::vector<GameTime> Hours = GClock.JumpTo(To);
		GNow = GClock.Now();
		// Waiting at Ada's step on the tea's evening is time with her, counted
		// before the hours (her tea closes at eleven).
		if (B.AtAdas && GWeek.Tea)
		{
			for (GameTime M = From.AddMinutes(1); M.TotalMinutes() <= GNow.TotalMinutes(); M = M.AddMinutes(1))
			{
				if (M.Day == GWeek.Tea->Day() && M.Hour >= AdasTea::From && M.Hour < AdasTea::Until) { GWeek.Tea->WithHer(M); }
			}
		}
		ClockHours(Hours);
		ClockLight();
		Say(FString(TEXT("You wait. ")) + Un(GNow.ToString()) + TEXT("."), 5.0f, FColor::Yellow);
		if (bStop)
		{
			Say(Un(S.Line), 8.0f, FColor::Yellow);
			Waiting::Showed(&B, &S);
			GWaitShown = B.Shown;
		}
	}

	bool HumanTalkTick(UWorld* World, double Now)
	{
		LiveHelperStart();
		LiveHelperPump();
		LiveVoiceStart();
		LiveVoicePump();
		if (GPawn != nullptr) { LedgerSession::Look(GPawn->GetActorLocation(), bSayOpen); }
		RegardTick(World, Now);
		TownHoursTick();
		LookScriptTick(World, Now);
		AskScriptTick(Now);
		TalkLightTick(World, Now);
		AckTick();
		if (bSayOpen)
		{
			// THE KEYBOARD BACK INTO THE BOX whenever it leaves while the box is
			// open (above); the game ignores its keys meanwhile.
			if (GSayText.IsValid() && !bSayCommitted && !bSayCancelled
			    && FSlateApplication::Get().GetKeyboardFocusedWidget() != GSayText)
			{
				FSlateApplication::Get().SetUserFocus(0, GSayText, EFocusCause::SetDirectly);
				FSlateApplication::Get().SetKeyboardFocus(GSayText, EFocusCause::SetDirectly);
			}
			// THE T THAT OPENED THE LINE is not the first letter of it.
			if (GSayText.IsValid() && Now - GSayOpenedAt < 0.5)
			{
				const FString Cur = GSayText->GetText().ToString();
				if (Cur == TEXT("t") || Cur == TEXT("T")) { GSayText->SetText(FText::GetEmpty()); }
			}
			if (bSayCommitted)
			{
				const FString Said = GSaid.TrimStartAndEnd();
				CloseSayBox(World);
				if (!Said.IsEmpty() && LiveAsk(GTalkTarget.G, GTalkTarget.Card, GTalkTarget.Id, GTalkTarget.Rung, GTalkTarget.Name, Utf8(Said)))
				{
					GLive.PendingBody = GTalkTarget.Body;
					AckStart(GTalkTarget.Card, GVisualFor(GTalkTarget.Body));
					Say(FString(TEXT("You: ")) + Said, 10.0f, FColor::Cyan);
				}
			}
			else if (bSayCancelled) { CloseSayBox(World); }
			TakeTalkRequests();
			return true;
		}
		if (TakeTalkRequests() <= 0 || GPawn == nullptr) { return false; }
		struct Who { AActor* Body; GossiperPtr G; const char* Card; const char* Id; const TCHAR* Name; int Rung; };
		const Who People[3] = {
			{ GN2Body, GN2, "sam", GIdN2.c_str(), TEXT("Darren"), -1 },
			{ GW1Body, GW1, "lena", GIdW1.c_str(), TEXT("Sheila"), GW1RungA },
			{ GR3Body, GR3, "rocco", GIdR3.c_str(), TEXT("Ron"), -1 } };
		const Who* Near = nullptr;
		const Who* Closest = nullptr;
		double Best = LedgerCrime::kLiveTalkM, ClosestM = 1e9;
		for (const Who& P : People)
		{
			if (P.Body == nullptr || !P.G) { continue; }
			const double M = FVector::Dist2D(GPawn->GetActorLocation(), P.Body->GetActorLocation()) / 100.0;
			if (M <= Best) { Best = M; Near = &P; }
			if (M < ClosestM) { ClosestM = M; Closest = &P; }
		}
		if (Near == nullptr)
		{
			// SAY WHO IS WHERE: "nobody near" alone sent the tester round in
			// circles beside a stand-in.
			Say(Closest != nullptr
				? FString::Printf(TEXT("Nobody near enough to talk to. The nearest is %s, %.0f metres away."), Closest->Name, ClosestM)
				: FString(TEXT("Nobody near enough to talk to.")), 6.0f, FColor::White);
			return false;
		}
		if (GLive.PendingId != 0) { Say(TEXT("Wait for an answer first."), 4.0f, FColor::White); return false; }
		if (!GLive.bReady) { Say(TEXT("(The street's voices are still waking up. Try again in a moment.)"), 4.0f, FColor::White); return false; }
		GTalkTarget.G = Near->G; GTalkTarget.Card = Near->Card; GTalkTarget.Id = Near->Id;
		GTalkTarget.Rung = Near->Rung; GTalkTarget.Name = FString(Near->Name);
		GTalkTarget.Body = Near->Body;
		OpenSayBox(World);
		return true;
	}

	// WHO IS TALKED TO, 24 September: the lad by default (the regression);
	// in the playable encounter whichever of Sam, Lena and Rocco is nearest,
	// each on their own card and from their own memory.
	GossiperPtr GTalkWith;
	std::string GTalkWho = "n2", GTalkCardOverride;
	int GTalkOwnRung = -1;

	// THE CONVERSATION: the helper beside the game, one JSON line each way,
	// carrying the lad's own memories and the simulation's day and hour.
	void RunTalk()
	{
		const GossiperPtr Target = GTalkWith ? GTalkWith : GN2;
		FString Exe;
		if (!FParse::Value(FCommandLine::Get(), TEXT("TalkHelper="), Exe) || Exe.IsEmpty())
		{
			GTalkWhy = "no-TalkHelper-path-given";
			return;
		}
		// The stand-in unless somebody plays, and then only LEDGER's own key
		// (29 September, TalkKeyForThisRun).
		bTalkFake = !LiveTalkPlayed();
		TalkKeyForThisRun();
		FString Card = TEXT("sam");
		FParse::Value(FCommandLine::Get(), TEXT("TalkAs="), Card);
		GTalkCard = GTalkCardOverride.empty() ? Utf8(Card) : GTalkCardOverride;
		// THE SIMULATION'S OWN CLOCK: GNow, which the encounter leaves at the
		// third round's evening and the reload restores from the save and
		// moves on to the next morning.
		GTalkDay = GNow.Day; GTalkHour = GNow.Hour;
		void* OutRead = nullptr; void* OutWrite = nullptr; void* InRead = nullptr; void* InWrite = nullptr;
		if (!FPlatformProcess::CreatePipe(OutRead, OutWrite) || !FPlatformProcess::CreatePipe(InRead, InWrite, true))
		{
			GTalkWhy = "no-pipes";
			return;
		}
		FProcHandle Proc = FPlatformProcess::CreateProc(*Exe, bTalkFake ? TEXT("--fake") : TEXT(""), false, true, true,
			nullptr, 0, nullptr, OutWrite, InRead);
		if (!Proc.IsValid())
		{
			GTalkWhy = "helper-did-not-start";
			FPlatformProcess::ClosePipe(OutRead, OutWrite);
			FPlatformProcess::ClosePipe(InRead, InWrite);
			return;
		}
		std::string Buf;
		auto LineWith = [&](const char* Key, double Limit) -> std::string
		{
			const double T0 = NowS();
			while (NowS() - T0 < Limit)
			{
				Buf += Utf8(FPlatformProcess::ReadPipe(OutRead));
				std::string::size_type Nl;
				while ((Nl = Buf.find('\n')) != std::string::npos)
				{
					const std::string L = Buf.substr(0, Nl);
					Buf.erase(0, Nl + 1);
					if (L.find(Key) != std::string::npos) { return L; }
				}
				FPlatformProcess::Sleep(0.05f);
			}
			return std::string();
		};
		const std::string Ready = LineWith("\"ready\"", 45.0);
		if (Ready.empty())
		{
			GTalkWhy = "helper-never-ready";
		}
		else
		{
			std::string Mem;
			if (Target && Target->Memory)
			{
				for (const MemoryEvent& E : Target->Memory->Events)
				{
					if (!Mem.empty()) { Mem += ","; }
					Mem += "{\"day\":" + std::to_string(E.Time.Day) + ",\"hour\":" + std::to_string(E.Time.Hour)
						+ ",\"minute\":" + std::to_string(E.Time.Minute) + ",\"kind\":\"" + JsonEsc(E.Kind)
						+ "\",\"importance\":" + std::to_string(E.Importance) + ",\"text\":\"" + JsonEsc(E.Text) + "\"}";
				}
			}
			// AND WHAT HE HOLDS AGAINST THE MAN IN FRONT OF HIM, for the Core
			// to turn into a level and a reason (24 September).
			const std::string Req = "{\"id\":1,\"to\":\"" + JsonEsc(GTalkCard)
				+ "\",\"who\":\"" + JsonEsc(GTalkWho) + "\",\"say\":\"Evening. Anything going on round here?\",\"day\":" + std::to_string(GTalkDay)
				+ ",\"hour\":" + std::to_string(GTalkHour) + ",\"minute\":" + std::to_string(GNow.Minute)
				+ ",\"scene\":\"The yard behind the parade on Quay Street.\",\"memories\":[" + Mem + "]"
				+ ",\"evidence\":" + EvidenceFor(Target, LedgerCrime::kLadFamiliarity, GTalkOwnRung) + "}";
			FPlatformProcess::WritePipe(InWrite, Un(Req));
			std::string Rep = LineWith("\"id\":1", 45.0);
			if (Rep.empty() && Buf.find("\"error\"") != std::string::npos) { Rep = Buf; }
			if (Rep.empty())
			{
				GTalkWhy = "no-reply";
			}
			else if (Rep.find("\"error\"") != std::string::npos)
			{
				GTalkWhy = "helper-error";
				GTalkReply = Rep;
			}
			else
			{
				// ANSWERED MEANS THE MODEL ANSWERED: a brush-off because the
				// line was down or slow is the helper talking, not him.
				bTalkAnswered = Rep.find("\"offline\":false") != std::string::npos
					&& Rep.find("\"timedOut\":false") != std::string::npos
					&& Rep.find("\"heard\":[") != std::string::npos;
				GTalkWhy = bTalkAnswered ? "answered" : "brushed-off-or-malformed";
				const std::string K = "\"reply\":\"";
				std::string::size_type At = Rep.find(K);
				if (At != std::string::npos)
				{
					std::string R;
					for (std::string::size_type I = At + K.size(); I < Rep.size(); ++I)
					{
						// AN ESCAPED LINE BREAK IS A SPACE, not the letter n: a
						// live reply in two paragraphs read "right now.nnLook".
						if (Rep[I] == '\\' && I + 1 < Rep.size())
						{
							const char E = Rep[++I];
							R += (E == 'n' || E == 'r' || E == 't') ? ' ' : E;
							continue;
						}
						if (Rep[I] == '"') { break; }
						R += Rep[I];
					}
					GTalkReply = R;
				}
				std::string::size_type H = Rep.find("\"heard\":[");
				if (H != std::string::npos)
				{
					// THE LIST ENDS AT THE FIRST ] OUTSIDE A STRING, and its
					// entries are counted as strings, not as commas.
					int Quotes = 0;
					std::string::size_type E = std::string::npos;
					for (std::string::size_type I = H + 9; I < Rep.size(); ++I)
					{
						if (Rep[I] == '\\') { ++I; continue; }
						if (Rep[I] == '"') { ++Quotes; continue; }
						if (Rep[I] == ']' && Quotes % 2 == 0) { E = I; break; }
					}
					GTalkHeard = Rep.substr(H + 9, E == std::string::npos ? std::string::npos : E - H - 9);
					GTalkHeardCount = Quotes / 2;
				}
				GSuspN2 = JsonField(Rep, "level");
				GSuspWhyN2 = JsonField(Rep, "why");
				// THE CRIME IS IN WHAT HE WAS GIVEN AND IN WHAT HE SAID: the
				// clause the witness filed, which the gossip carried to him.
				const std::string Key = GFiledSummaryA.size() > 24 ? GFiledSummaryA.substr(0, 24) : GFiledSummaryA;
				bTalkHeardCrime = bTalkAnswered && !Key.empty() && GTalkHeard.find(JsonEsc(Key)) != std::string::npos;
				bTalkQuestioned = GTalkReply.find('?') != std::string::npos
					&& !Key.empty() && GTalkReply.find(Key) != std::string::npos;
				if (!bTalkFake)
				{
					// A LIVE MODEL WORDS IT ITS OWN WAY: questioned means he
					// asked something, with the crime in what he was given,
					// AND HE ASKED ABOUT IT: the reply names the deed or where
					// it happened. Any question mark at all let "You looking
					// for something?" pass as questioning (the independent
					// check, and the first live run, 24 September).
					std::string Low = GTalkReply;
					for (char& Ch : Low) { Ch = (char)std::tolower((unsigned char)Ch); }
					const char* Words[] = { "window", "glass", "yard", "shop", "smash", "broke" };
					bool bAbout = false;
					for (const char* Wd : Words) { if (Low.find(Wd) != std::string::npos) { bAbout = true; } }
					bTalkQuestioned = bTalkHeardCrime && GTalkReply.find('?') != std::string::npos && bAbout;
				}
			}
		}
		// HIS MATE, THE CONTROL: he heard about the window too, and the Core
		// is asked what he holds against the man, with no model call.
		if (!Ready.empty())
		{
			const std::string Req2 = "{\"id\":2,\"to\":\"" + JsonEsc(GTalkCard)
				+ "\",\"who\":\"r3\",\"noReply\":true,\"evidence\":" + EvidenceFor(GR3, LedgerCrime::kLadFamiliarity, -1) + "}";
			FPlatformProcess::WritePipe(InWrite, Un(Req2));
			const std::string Rep2 = LineWith("\"id\":2", 20.0);
			GSuspR3 = Rep2.empty() ? std::string("no-reply") : JsonField(Rep2, "level");
			// AND THE SHOPKEEPER, who saw his face at it: she has reason too.
			const std::string Req3 = "{\"id\":3,\"to\":\"" + JsonEsc(GTalkCard)
				+ "\",\"who\":\"w1\",\"noReply\":true,\"evidence\":" + EvidenceFor(GW1, LedgerCrime::kLadFamiliarity, GW1RungA) + "}";
			FPlatformProcess::WritePipe(InWrite, Un(Req3));
			const std::string Rep3 = LineWith("\"id\":3", 20.0);
			GSuspW1 = Rep3.empty() ? std::string("no-reply") : JsonField(Rep3, "level");
		}
		FPlatformProcess::ClosePipe(InRead, InWrite);
		const double TQuit = NowS();
		while (FPlatformProcess::IsProcRunning(Proc) && NowS() - TQuit < 5.0)
		{
			Buf += Utf8(FPlatformProcess::ReadPipe(OutRead));
			FPlatformProcess::Sleep(0.05f);
		}
		if (FPlatformProcess::IsProcRunning(Proc)) { FPlatformProcess::TerminateProc(Proc, true); }
		FPlatformProcess::CloseProc(Proc);
		FPlatformProcess::ClosePipe(OutRead, OutWrite);
	}

	// THE SAVE, TO DISK: the mill as the JSON the C# codec reads, each
	// resident's memory as its markdown, and the clock and the filed clause.
	void SaveEncounterToDisk()
	{
		const FString Dir = EncSaveDir();
		GSaveDirUsed = Dir;
		IFileManager::Get().MakeDirectory(*Dir, true);
		const std::string Json = GMill ? Save::CaptureMillAgents(*GMill) : std::string();
		bool Ok = !Json.empty() && FFileHelper::SaveStringToFile(Un(Json), *(Dir / TEXT("agents.json")),
			FFileHelper::EEncodingOptions::ForceUTF8WithoutBOM);
		const GossiperPtr Gs[3] = { GW1, GN2, GR3 };
		for (const GossiperPtr& G : Gs)
		{
			if (!G || !G->Memory) { Ok = false; continue; }
			Ok = FFileHelper::SaveStringToFile(Un(G->Memory->ToMarkdown()),
				*(Dir / FString::Printf(TEXT("memory-%s.md"), *Un(G->Id))),
				FFileHelper::EEncodingOptions::ForceUTF8WithoutBOM) && Ok;
		}
		// THE REST OF THE TOWN'S MEMORIES TOO, in free play (the whole cast is
		// in the mill there), so a reload loses nobody's (Jafar's list, item 1).
		if (!bLiveScript && GMill)
		{
			for (const GossiperPtr& G : GMill->Agents())
			{
				if (!G || !G->Memory || G == GW1 || G == GN2 || G == GR3) { continue; }
				Ok = FFileHelper::SaveStringToFile(Un(G->Memory->ToMarkdown()),
					*(Dir / FString::Printf(TEXT("memory-%s.md"), *Un(G->Id))),
					FFileHelper::EEncodingOptions::ForceUTF8WithoutBOM) && Ok;
			}
		}
		// A NEW STAMP ONLY WITH THE TALK SAVED BESIDE IT (the review's C1): a save
		// before the talk program is ready, or before it has loaded the save's
		// own talk, keeps the stamp the saved talk carries, so Continue finds it.
		const bool bTalkSavedNow = LedgerCrime::TalkSavedWithThisSave(GLive.bStarted && FPlatformProcess::IsProcRunning(GLive.Proc), GLive.bReady, GLive.bTalkLoad);
		GLive.TalkStamp = LedgerCrime::TalkStampForSave(GLive.TalkStamp, bTalkSavedNow, Utf8(FGuid::NewGuid().ToString(EGuidFormats::Digits)));
		const std::string Clock = "day=" + std::to_string(GNow.Day) + "\nhour=" + std::to_string(GNow.Hour)
			+ "\nminute=" + std::to_string(GNow.Minute) + "\nsummaryA=" + GFiledSummaryA
			+ "\nrungA=" + std::to_string(GW1RungA)
			+ "\nothersNear=" + std::to_string(GFleeOthersSeen)
			+ "\ntalkStamp=" + GLive.TalkStamp
			+ (bDeedDone ? "\ndeedDay=" + std::to_string(GDeedDay) + "\ndeedHour=" + std::to_string(GDeedHour) : std::string())
			+ [] { std::string S; for (const auto& Kv : GSawHimAt) { S += "\nsaw_" + Kv.first + "=" + Kv.second; } return S; }()
			+ [] { std::string S; for (const auto& W : GWeek.Witnesses) { S += "\nwitness_" + W.first + "=" + std::to_string(W.second); } return S; }()
			+ (bSheilaTrusts ? "\nsheilaTrusts=1" : "")
			+ GMet.SaveLines()
			+ [] {
				if (GPawn == nullptr || bLiveScript) { return std::string(); }
				const LedgerCrime::P3 At = ToStreet(GPawn->GetActorLocation());
				char B[96];
				FCStringAnsi::Snprintf(B, sizeof(B), "\nplace=%.2f,%.2f,%.1f", At.X, At.Z, (double)GPawn->GetActorRotation().Yaw);
				return std::string(B);
			}()
			+ "\nclock=" + GClock.ToText()
			+ "\ncommit=" + Utf8(CrimeSha()) + "\n";
		// THE TALK SAVED BESIDE IT, under the same stamp (handover 6r).
		if (bTalkSavedNow)
		{
			const std::string Path = Utf8(FPaths::ConvertRelativePathToFull(Dir / Un(LedgerCrime::TalkSaveFile())));
			FPlatformProcess::WritePipe(GLive.InWrite, Un("{\"talk\":\"save\",\"path\":\"" + JsonEsc(Path) + "\",\"stamp\":\"" + GLive.TalkStamp + "\"}\n"));
		}
		Ok = FFileHelper::SaveStringToFile(Un(Clock), *(Dir / TEXT("clock.txt")),
			FFileHelper::EEncodingOptions::ForceUTF8WithoutBOM) && Ok;
		// WHO HAS HAD THEIR SAY AND WHAT HE HAS HEARD (town list 6o), so a
		// reload neither lets anybody remark twice on a story nor starts a
		// bank over.
		Ok = FFileHelper::SaveStringToFile(Un(GLive.Remarks.ToJson()), *(Dir / TEXT("remarks.json")),
			FFileHelper::EEncodingOptions::ForceUTF8WithoutBOM) && Ok;
		// THE HOURS THE TOWN HAS TALKED (town list 6bs), so a reload runs no
		// hour twice and loses none.
		Ok = FFileHelper::SaveStringToFile(Un(GTownHours.ToJson()), *(Dir / TEXT("town-hours.json")),
			FFileHelper::EEncodingOptions::ForceUTF8WithoutBOM) && Ok;
		// THE CONSEQUENCE (free play): the police file, the damage and any
		// arrest, in the town's own save (TownSave), so a reload keeps them.
		if (!bLiveScript)
		{
			TownSave T;
			T.Asks = GWeek.Asks;
			if (GWeek.Tea) { T.Tea.reset(new AdasTea(*GWeek.Tea)); }
			T.Police = GWeek.Police;
			T.Damage = GWeek.Damage;
			T.Arrests = GWeek.Arrests;
			T.Hours = GWeek.Hours;
			T.Week = GWeek.Week;
			T.WaitShown = GWaitShown;
			Ok = FFileHelper::SaveStringToFile(Un(T.ToJson()), *(Dir / TEXT("town.json")),
				FFileHelper::EEncodingOptions::ForceUTF8WithoutBOM) && Ok;
		}
		// THE HINTS ALREADY SHOWN (town list 6y), so a load shows none twice.
		if (bHintsOn)
		{
			Ok = FFileHelper::SaveStringToFile(Un(GHints.ToJson()), *(Dir / TEXT("hints.json")),
				FFileHelper::EEncodingOptions::ForceUTF8WithoutBOM) && Ok;
		}
		bSavedToDisk = Ok;
		GSavedBytes = (int)Json.size();
	}

	// THE LOAD, FROM DISK, in a process that never saw the crime.
	void LoadEncounterFromDisk()
	{
		const FString Dir = EncSaveDir();
		GSaveDirUsed = Dir;
		bLoadPlace = false;
		bSheilaTrusts = false;
		GMet = LedgerCrime::MeetingBook();
		GPlacedFor.clear();
		GHeldBackSince.clear();
		GHeardOnly.clear();
		bPlaceNow = true;
		GWaitShown.clear();   // from the town's save (and an older save's clock file)
		FString J;
		bool Ok = FFileHelper::LoadFileToString(J, *(Dir / TEXT("agents.json")));
		if (Ok && GMill) { Save::RestoreMillAgents(Utf8(J), *GMill); GLoadedBytes = J.Len(); }
		const GossiperPtr Gs[3] = { GW1, GN2, GR3 };
		for (const GossiperPtr& G : Gs)
		{
			FString Md;
			if (G && G->Memory && FFileHelper::LoadFileToString(Md, *(Dir / FString::Printf(TEXT("memory-%s.md"), *Un(G->Id)))))
			{
				G->Memory->LoadFrom(Utf8(Md));
			}
			else { Ok = false; }
		}
		// THE REST OF THE TOWN'S MEMORIES, in free play, each where it was saved;
		// one missing (a save from before the town joined) leaves that person's
		// memory fresh, never the load.
		if (!bLiveScript && GMill)
		{
			for (const GossiperPtr& G : GMill->Agents())
			{
				if (!G || !G->Memory || G == GW1 || G == GN2 || G == GR3) { continue; }
				FString Md;
				if (FFileHelper::LoadFileToString(Md, *(Dir / FString::Printf(TEXT("memory-%s.md"), *Un(G->Id))))) { G->Memory->LoadFrom(Utf8(Md)); }
			}
		}
		// THE CONSEQUENCE (free play), from the town's save; a save without it
		// (from before) starts the police file empty, never the load.
		if (!bLiveScript)
		{
			FString TownText;
			TownSave T;
			GWeek = TownWeek();
			std::string Err;
			if (FFileHelper::LoadFileToString(TownText, *(Dir / TEXT("town.json"))) && TownSave::FromJson(Utf8(TownText), T, Err))
			{
				GWeek.Asks = T.Asks;
				GWeek.Tea.reset(T.Tea ? new AdasTea(*T.Tea) : nullptr);
				GWeek.Police = T.Police;
				GWeek.Damage = T.Damage;
				GWeek.Arrests = T.Arrests;
				GWeek.Hours = T.Hours;
				GWeek.Week = T.Week;
				GWaitShown.insert(T.WaitShown.begin(), T.WaitShown.end());
			}
		}
		FString ClockText;
		bool bClockRead = false;
		if (FFileHelper::LoadFileToString(ClockText, *(Dir / TEXT("clock.txt"))))
		{
			TArray<FString> Lines;
			ClockText.ParseIntoArrayLines(Lines);
			for (const FString& L : Lines)
			{
				FString Kv, V;
				if (!L.Split(TEXT("="), &Kv, &V)) { continue; }
				if (Kv == TEXT("day")) { GClockDay = FCString::Atoi(*V); }
				else if (Kv == TEXT("hour")) { GClockHour = FCString::Atoi(*V); }
				else if (Kv == TEXT("minute")) { GClockMinute = FCString::Atoi(*V); }
				else if (Kv == TEXT("summaryA")) { GFiledSummaryA = Utf8(V); }
				else if (Kv == TEXT("rungA")) { GW1RungA = FCString::Atoi(*V); }
				else if (Kv == TEXT("othersNear")) { GFleeOthersSeen = FCString::Atoi(*V); }
				else if (Kv == TEXT("talkStamp")) { GLive.TalkStamp = Utf8(V); }
				else if (Kv == TEXT("deedDay")) { GDeedDay = FCString::Atoi(*V); bDeedDone = true; GWindowTopic = "player.window_d" + std::to_string(GDeedDay); GWeek.DeedTopic = GWindowTopic; GWeek.DeedDay = GDeedDay; }
				else if (Kv.StartsWith(TEXT("witness_"))) { GWeek.Witnesses.push_back({ Utf8(Kv.Mid(8)), FCString::Atoi(*V) }); }
				else if (Kv == TEXT("sheilaTrusts")) { bSheilaTrusts = V == TEXT("1"); }
				else if (Kv == TEXT("place"))
				{
					TArray<FString> P;
					V.ParseIntoArray(P, TEXT(","));
					if (P.Num() == 3) { bLoadPlace = true; GLoadX = FCString::Atod(*P[0]); GLoadZ = FCString::Atod(*P[1]); GLoadYaw = FCString::Atod(*P[2]); }
				}
				else if (Kv == TEXT("deedHour")) { GDeedHour = FCString::Atoi(*V); }
				else if (Kv.StartsWith(TEXT("saw_"))) { GSawHimAt[Utf8(Kv.Mid(4))] = Utf8(V); }
				else if (GMet.TakeLine(Utf8(Kv), Utf8(V))) { }
				else if (Kv == TEXT("commit")) { GSavedByCommit = Utf8(V); }
				else if (Kv == TEXT("clock")) { bClockRead = GClock.FromText(Utf8(V)); }
				else if (Kv == TEXT("waitShown") && TownSave::IsStopKey(Utf8(V))) { GWaitShown.insert(Utf8(V)); }   // an older save's, checked as the town's save checks them
			}
		}
		else { Ok = false; }
		// A SAVE FROM ANOTHER BUILD IS NOT THIS ENCOUNTER'S: the reload
		// refuses it rather than reading an older town as this one.
		if (GSavedByCommit != Utf8(CrimeSha())) { Ok = false; }
		bLoadedFromDisk = Ok;
		// The remarks and the lines heard (town list 6o), only from a save the
		// load took; a save from before they were kept has none, and a damaged
		// one loses them, never the game.
		FString RemarksText;
		GLive.Remarks = Ok && FFileHelper::LoadFileToString(RemarksText, *(Dir / TEXT("remarks.json")))
			? StreetVoice::RemarkLedger::FromJson(Utf8(RemarksText)) : StreetVoice::RemarkLedger();
		// THE TALK COMES BACK TOO, once the talk program is ready (handover 6r).
		GLive.bTalkLoad = Ok && !GLive.TalkStamp.empty();
		GLive.bTalkReset = false;
		// The hours the town has talked (town list 6bs), from a save the load
		// took; without them the first hour after the load starts them again.
		FString HoursText;
		GTownHours = Ok && FFileHelper::LoadFileToString(HoursText, *(Dir / TEXT("town-hours.json")))
			? TownHours::FromJson(Utf8(HoursText)) : TownHours();
		// THE CLOCK COMES BACK WITH THE SAVE. In free play exactly where it was
		// (a real reload, item 1); the scripted encounter lets the night pass,
		// as its regression measures (the town's rounds run the hours).
		if (!bLiveScript && bClockRead && GClock.TotalMinutes() > 0) { GNow = GClock.Now(); }
		else { GNow = GameTime(GClockDay + 1, 9, 0); GClock = LiveClock(GNow); }
	}

	void WriteEncounterVerdict()
	{
		StopShoutRecording(true);
		const int AW1 = AboutCrime(GW1, true), AN2 = AboutCrime(GN2, true), AR3 = AboutCrime(GR3, true);
		const int BW1 = AboutCrime(GW1, false), BN2 = AboutCrime(GN2, false), BR3 = AboutCrime(GR3, false);
		const int MW1 = CrimeMemories(GW1), MN2 = CrimeMemories(GN2), MR3 = CrimeMemories(GR3);
		const int Ix = (GEnc == EEncounter::Unseen) ? 1 : 0;
		const bool bSlice = FCString::Strcmp(GActPawnClass[Ix], TEXT("LedgerSliceCharacter")) == 0;
		const bool bByInput = GActAttempted[Ix] && GActTook[Ix] && GActRequestsSeen[Ix] > 0
			&& FCString::Strcmp(GActPressLanded[Ix], TEXT("player-input")) == 0;
		const bool bBankReadable = !GFiledSummaryA.empty() && !LedgerCrime::IsUnreadableSummary(GFiledSummaryA);
		const bool bShoutHeard = bShoutPlaying && bShoutSpatial && GShoutPlayerM >= 0.0 && GShoutPlayerM < GShoutFalloffM;
		std::vector<std::pair<std::string, bool>> Need;
		if (GEnc == EEncounter::Play)
		{
			Need.push_back({ "new-player-character", bSlice });
			Need.push_back({ "crime-by-the-player's-own-key", bByInput });
			Need.push_back({ "witness-saw-it", AW1 > 0 && MW1 > 0 && bBankReadable });
			Need.push_back({ "shout-heard-in-the-street", bShoutHeard });
			Need.push_back({ "gossip-reached-the-lad", AN2 > 0 && HeardMemories(GN2) > 0 });
			Need.push_back({ "and-his-mate", AR3 > 0 });
			Need.push_back({ "the-lad-saw-him-run", bFleeFiled });
			Need.push_back({ "helper-answered-from-his-memory", bTalkHeardCrime });
			Need.push_back({ "the-lad-has-reason-to-suspect-him", GSuspN2 == "Suspicious" || GSuspN2 == "Confronting" });
			Need.push_back({ "the-witness-has-reason-too", GSuspW1 == "Suspicious" || GSuspW1 == "Confronting" });
			Need.push_back({ "his-mate-has-no-reason-to-question-him", GSuspR3 == "Trusting" || GSuspR3 == "Uneasy" });
			Need.push_back({ "he-questioned-the-player", bTalkQuestioned });
			Need.push_back({ "saved-to-disk", bSavedToDisk });
		}
		else if (GEnc == EEncounter::Reload)
		{
			Need.push_back({ "loaded-from-disk", bLoadedFromDisk });
			Need.push_back({ "the-lad-still-knows", AN2 > 0 && HeardMemories(GN2) > 0 && bBankReadable });
			Need.push_back({ "his-mate-still-knows", AR3 > 0 });
			Need.push_back({ "the-witness-still-knows", AW1 > 0 });
			Need.push_back({ "helper-answered-from-his-memory", bTalkHeardCrime });
			Need.push_back({ "the-lad-still-has-reason", GSuspN2 == "Suspicious" || GSuspN2 == "Confronting" });
			Need.push_back({ "the-witness-still-has-reason", GSuspW1 == "Suspicious" || GSuspW1 == "Confronting" });
			Need.push_back({ "he-questioned-the-player", bTalkQuestioned });
		}
		else if (GEnc == EEncounter::Live)
		{
			// THE PLAYABLE ENCOUNTER, SCRIPTED: the real people are there; a
			// first run commits the deed through the live phases, a second
			// run comes back to a town that still knows.
			Need.push_back({ "the-real-people-stand-there", GVisualsPlaced >= 2 });
			if (!bLoadedFromDisk)
			{
				Need.push_back({ "the-window-went", GActTook[0] });
				Need.push_back({ "lena-saw-it", AW1 > 0 && bBankReadable });
				Need.push_back({ "sam-saw-him-run", bFleeFiled });
				Need.push_back({ "gossip-reached-sam", AN2 > 0 && HeardMemories(GN2) > 0 });
				Need.push_back({ "saved-to-disk", bSavedToDisk });
			}
			else
			{
				Need.push_back({ "the-town-still-knows", AN2 > 0 && AW1 > 0 });
			}
			Need.push_back({ "sam-has-reason", GSuspN2 == "Suspicious" || GSuspN2 == "Confronting" });
			Need.push_back({ "sam-questioned-the-player", bTalkQuestioned });
		}
		else
		{
			Need.push_back({ "new-player-character", bSlice });
			Need.push_back({ "crime-by-the-player's-own-key", bByInput });
			Need.push_back({ "nobody-saw-it", AW1 + AN2 + AR3 + BW1 + BN2 + BR3 == 0 });
			Need.push_back({ "nobody-remembers-a-crime", MW1 + MN2 + MR3 == 0 });
			Need.push_back({ "the-helper-answered", bTalkAnswered });
			Need.push_back({ "he-knew-nothing", GTalkHeardCount == 0 && GTalkReply.find('?') == std::string::npos });
			Need.push_back({ "no-reason-to-suspect-him", GSuspN2 == "Trusting" });
		}
		std::string Failed;
		for (const auto& N : Need) { if (!N.second) { Failed += (Failed.empty() ? "" : ",") + N.first; } }
		FString V;
		V += FString::Printf(TEXT("encounterMode=%s\n"), EncName());
		V += FString::Printf(TEXT("encounterStatus=%s\n"), Failed.empty() ? TEXT("PASS") : TEXT("FAIL"));
		V += FString::Printf(TEXT("encounterFailed=%s\n"), Failed.empty() ? TEXT("none") : *Un(Failed));
		V += FString::Printf(TEXT("encounterCommit=%s\n"), *CrimeSha());
		V += FString::Printf(TEXT("pawnClass=%s actPressLanded=%s actRequestsSeen=%d actAttempted=%s\n"),
			GActPawnClass[Ix], GActPressLanded[Ix], GActRequestsSeen[Ix], GActAttempted[Ix] ? TEXT("yes") : TEXT("no"));
		V += FString::Printf(TEXT("aboutA w1=%d n2=%d r3=%d aboutB w1=%d n2=%d r3=%d crimeMemories w1=%d n2=%d r3=%d\n"),
			AW1, AN2, AR3, BW1, BN2, BR3, MW1, MN2, MR3);
		V += FString::Printf(TEXT("filedSummaryA=%s\n"), GFiledSummaryA.empty() ? TEXT("none") : *Un(GFiledSummaryA));
		V += FString::Printf(TEXT("shout=%s shoutSpatial=%s shoutClip=crowd_f1/bc9b402a shoutPlayerDistanceM=%.1f shoutReachM=%.1f shoutWav=%s\n"),
			*GShoutNote, bShoutSpatial ? TEXT("yes") : TEXT("no"), GShoutPlayerM, GShoutFalloffM,
			bShoutWavWritten ? TEXT("ue-encounter-shout.wav") : TEXT("none"));
		V += FString::Printf(TEXT("talk=%s talkAs=%s talkFake=%s talkDay=%d talkHour=%d heardCount=%d heardCrime=%s questioned=%s\n"),
			*Un(GTalkWhy), *Un(GTalkCard), bTalkFake ? TEXT("yes") : TEXT("no"), GTalkDay, GTalkHour, GTalkHeardCount,
			bTalkHeardCrime ? TEXT("yes") : TEXT("no"), bTalkQuestioned ? TEXT("yes") : TEXT("no"));
		V += FString::Printf(TEXT("talkReply=%s\n"), *Un(GTalkReply));
		V += FString::Printf(TEXT("suspicion lad=%s witness=%s mate=%s witnessRungA=%d flee=%s fleeSeconds=%.2f fleeMetres=%.1f fleeRung=%d fleeCertainty=%.2f othersTheLadSaw=%d\n"),
			*Un(GSuspN2), *Un(GSuspW1), *Un(GSuspR3), GW1RungA,
			bFleeFiled ? TEXT("filed") : (bFleeSeen ? TEXT("seen-not-filed") : TEXT("not-seen")),
			GFleeSeconds, GFleeMetres, GFleeRung, GFleeCertainty, GFleeOthersSeen);
		V += FString::Printf(TEXT("suspicionWhyLad=%s\n"), *Un(GSuspWhyN2));
		V += FString::Printf(TEXT("voiceFirstHeardAfterS=%.1f\n"), bVoicePlayed ? GVoicePlayedAt - GVoiceAskedAt : -1.0);
		V += FString::Printf(TEXT("voice=%s voiceSeconds=%.1f\n"),
			!GVoice.bStarted ? TEXT("not-asked") : (bVoicePlayed ? TEXT("played") : (bVoiceAsked ? TEXT("asked-never-came") : (GVoice.bReady ? TEXT("ready-not-used") : TEXT("never-ready")))),
			GVoiceSeconds);
		V += FString::Printf(TEXT("save=%s savedBytes=%d loaded=%s loadedBytes=%d savedByCommit=%s clockLoaded=D%d-%02d:%02d talkAnswered=%s bankReadable=%s saveDir=%s\n"),
			bSavedToDisk ? TEXT("written") : TEXT("not-written"), GSavedBytes, bLoadedFromDisk ? TEXT("yes") : TEXT("no"),
			GLoadedBytes, *Un(GSavedByCommit), GClockDay, GClockHour, GClockMinute,
			bTalkAnswered ? TEXT("yes") : TEXT("no"), bBankReadable ? TEXT("yes") : TEXT("no"), *GSaveDirUsed);
		const FString Leaf = FString::Printf(TEXT("ue-encounter-%s-verdict.txt"), EncName());
		FFileHelper::SaveStringToFile(V, *AbsProject(*Leaf), FFileHelper::EEncodingOptions::ForceUTF8WithoutBOM);
		FFileHelper::SaveStringToFile(V, *ExeDir(*Leaf), FFileHelper::EEncodingOptions::ForceUTF8WithoutBOM);
	}

	// ---- the ticker ------------------------------------------------------
	// A PROMPT ON WHAT HE CAN USE, 29 September (the twenty a friend would
	// notice, 8): near a person, "T  talk to Sheila"; before the deed, beside
	// Mickey's window, "E  the window". Its own line under the spoken ones,
	// hidden while he types; the same people and reach the keys act on.
	TSharedPtr<STextBlock> GPromptText;
	TSharedPtr<SWidget> GPromptRoot;
	TWeakObjectPtr<UWorld> GPromptWorld;
	FString GPromptNow;

	void PromptSet(const FString& Text)
	{
		if (GEngine == nullptr || GEngine->GameViewport == nullptr) { return; }
		UWorld* W = GEngine->GameViewport->GetWorld();
		if (!GPromptRoot.IsValid() || GPromptWorld.Get() != W)
		{
			SAssignNew(GPromptRoot, SBox)
				.HAlign(HAlign_Center).VAlign(VAlign_Bottom).Padding(FMargin(40.0f, 0.0f, 40.0f, 110.0f))
				[
					SAssignNew(GPromptText, STextBlock)
					.Font(FCoreStyle::GetDefaultFontStyle("Bold", 16))
					.ColorAndOpacity(FSlateColor(FLinearColor(0.95f, 0.92f, 0.8f, 1.0f)))
					.ShadowOffset(FVector2D(1.5f, 1.5f))
					.ShadowColorAndOpacity(FLinearColor(0.0f, 0.0f, 0.0f, 0.9f))
				];
			GEngine->GameViewport->AddViewportWidgetContent(GPromptRoot.ToSharedRef(), 49);
			GPromptWorld = W;
			GPromptNow = TEXT("(unset)");
		}
		if (Text == GPromptNow || !GPromptText.IsValid()) { return; }
		GPromptNow = Text;
		GPromptText->SetText(FText::FromString(Text));
	}

	void LivePromptTick(bool bBeforeDeed)
	{
		if (GPawn == nullptr || bSayOpen) { PromptSet(FString()); return; }
		const FVector At = GPawn->GetActorLocation();
		struct Who { AActor* Body; const GossiperPtr* G; const TCHAR* Name; };
		const Who People[3] = { { GN2Body, &GN2, TEXT("Darren") }, { GW1Body, &GW1, TEXT("Sheila") }, { GR3Body, &GR3, TEXT("Ron") } };
		const TCHAR* Near = nullptr;
		double Best = LedgerCrime::kLiveTalkM;
		for (const Who& P : People)
		{
			if (P.Body == nullptr || !*P.G) { continue; }
			const double M = FVector::Dist2D(At, P.Body->GetActorLocation()) / 100.0;
			if (M <= Best) { Best = M; Near = P.Name; }
		}
		FString Text;
		if (Near != nullptr) { Text = FString::Printf(TEXT("T  talk to %s"), Near); }
		if (bBeforeDeed && !GActAttempted[0] && GGlass[0] != nullptr
		    && FVector::Dist2D(At, GGlass[0]->GetComponentsBoundingBox(true).GetCenter()) / 100.0 <= LedgerCrime::kLiveReachM)
		{
			Text += (Text.IsEmpty() ? FString() : FString(TEXT("        "))) + TEXT("E  the window");
		}
		if (bClockRuns) { Text += (Text.IsEmpty() ? FString() : FString(TEXT("        "))) + TEXT("Z  wait"); }
		PromptSet(Text);
	}

	// A FRIEND'S GAME OPENS ON THE TITLE (TitleScreen.h); the automation's
	// scripted runs, the look filming and the talk timing never do.
	bool TitleWanted()
	{
		const TCHAR* C = FCommandLine::Get();
		int32 Ask = 0;
		return GEnc == EEncounter::Live && !FParse::Param(C, TEXT("LiveScript")) && !FParse::Param(C, TEXT("LookScript"))
			&& !FParse::Param(C, TEXT("NoTitle")) && !FParse::Param(C, TEXT("PortraitInGame")) && !FParse::Param(C, TEXT("CastAllNow"))
			&& !FParse::Value(C, TEXT("AskScript="), Ask);
	}
	bool bTitleAsked = false;

	// THE LIVE STORY STARTS, from the save when bTryLoad and one is there, or
	// new: straight from the street being placed, or from the title's choice.
	// THE HINTS, EACH THE FIRST TIME IT MATTERS, 30 September (town list 6y;
	// the twenty a friend would notice, 7; FirstMoments.h, the port checked
	// row for row against the C#). A line of plain text at the top of the
	// view, for nine seconds, never two within twelve. The moments this
	// street has: he stands still in a new game, he is free to talk (from
	// the start here, until day one's walk-round ends it), and somebody saw
	// the deed. The coat, the overheard remark and the Ledger wait for their
	// keys: a hint whose key the game does not have yet is never shown with
	// its braces, only logged. Sheila's and Ron's spoken lines wait for
	// takes that pass the accent gate; the plain line shows alone.
	bool bHintsMoved = false, bHintsFromSet = false;
	FVector GHintsFrom = FVector::ZeroVector;
	TSharedPtr<STextBlock> GHintText;
	TSharedPtr<SWidget> GHintBack;
	TSharedPtr<SWidget> GHintRoot;
	TWeakObjectPtr<UWorld> GHintWorld;
	double GHintUntil = -1.0;
	constexpr double kHintSeconds = 9.0;

	/// The keys as this game binds them (SliceCharacter.cpp).
	bool HintKey(const std::string& K, std::string& Out)
	{
		if (K == "Move") { Out = "W A S D"; return true; }
		if (K == "Run") { Out = "Shift"; return true; }
		if (K == "Talk") { Out = "T"; return true; }
		return false;
	}

	void HintSetText(const FString& Text)
	{
		if (GEngine == nullptr || GEngine->GameViewport == nullptr) { return; }
		UWorld* W = GEngine->GameViewport->GetWorld();
		if (!GHintRoot.IsValid() || GHintWorld.Get() != W)
		{
			SAssignNew(GHintRoot, SBox)
				.HAlign(HAlign_Center).VAlign(VAlign_Top).Padding(FMargin(40.0f, 64.0f, 40.0f, 0.0f))
				[
					SNew(SBox).MaxDesiredWidth(900.0f)
					[
						// A DARK BACKING, so the line reads over a white sky (the
						// tester, 30 September); hidden while there is no hint.
						SAssignNew(GHintBack, SBorder)
						.BorderImage(FCoreStyle::Get().GetBrush("WhiteBrush"))
						.BorderBackgroundColor(FLinearColor(0.0f, 0.0f, 0.0f, 0.5f))
						.Padding(FMargin(16.0f, 8.0f))
						.Visibility(EVisibility::Collapsed)
						[
							SAssignNew(GHintText, STextBlock)
							.Font(FCoreStyle::GetDefaultFontStyle("Regular", 17))
							.Justification(ETextJustify::Center)
							.AutoWrapText(true)
							.ColorAndOpacity(FSlateColor(FLinearColor(0.95f, 0.92f, 0.8f, 1.0f)))
							.ShadowOffset(FVector2D(1.0f, 1.0f))
							.ShadowColorAndOpacity(FLinearColor(0.0f, 0.0f, 0.0f, 0.8f))
						]
					]
				];
			GEngine->GameViewport->AddViewportWidgetContent(GHintRoot.ToSharedRef(), 48);
			GHintWorld = W;
		}
		if (GHintText.IsValid()) { GHintText->SetText(FText::FromString(Text)); }
		if (GHintBack.IsValid()) { GHintBack->SetVisibility(Text.IsEmpty() ? EVisibility::Collapsed : EVisibility::HitTestInvisible); }
	}

	void HintShow(const LedgerCore::Hint& H)
	{
		const std::string Text = LedgerCore::FirstMoments::Fill(H.Key, &HintKey);
		if (Text.find('{') != std::string::npos)
		{
			UE_LOG(LogTemp, Display, TEXT("LedgerHints: %s not shown, its key is not in the game yet: %s"),
			       *Un(LedgerCore::MomentName(H.M)), *Un(Text));
			return;
		}
		HintSetText(Un(Text));
		GHintUntil = NowS() + kHintSeconds;
		UE_LOG(LogTemp, Display, TEXT("LedgerHints: shown %s: %s"), *Un(LedgerCore::MomentName(H.M)), *Un(Text));
		LedgerSession::Write(TEXT("hint"), TEXT("\"moment\":") + LedgerSession::Str(Un(LedgerCore::MomentName(H.M))));
	}

	void HintHappened(LedgerCore::Moment M)
	{
		if (!bHintsOn) { return; }
		// A moment whose key the game does not have yet is not reported, so
		// its hint is not spent unseen and shows once the key exists (the
		// independent check, 30 September).
		if (LedgerCore::FirstMoments::Fill(LedgerCore::FirstMoments::Words(M).Key, &HintKey).find('{') != std::string::npos)
		{
			UE_LOG(LogTemp, Display, TEXT("LedgerHints: %s kept for later, its key is not in the game yet"), *Un(LedgerCore::MomentName(M)));
			return;
		}
		LedgerCore::Hint H;
		if (GHints.Happened(M, NowS(), H)) { HintShow(H); }
	}

	void HintsTick()
	{
		if (!bHintsOn) { return; }
		const double T = NowS();
		if (GPawn != nullptr && !bHintsMoved)
		{
			const FVector At = GPawn->GetActorLocation();
			if (!bHintsFromSet) { GHintsFrom = At; bHintsFromSet = true; }
			else if (FVector::Dist2D(At, GHintsFrom) > 50.0f) { GHints.Moved(T); bHintsMoved = true; }
		}
		LedgerCore::Hint H;
		if (GHints.Due(T, H)) { HintShow(H); }
		if (GHintUntil >= 0.0 && T >= GHintUntil) { HintSetText(FString()); GHintUntil = -1.0; }
	}

	const TCHAR* const kErrandMickeys = TEXT("Walk to Mickey's front window, the minicab office with the dark blue front, and press E. Press T near someone to talk to them first, if you like.");
	const TCHAR* const kErrandRitas = TEXT("Walk to Rita's pawn shop, two doors up from Mickey's (the minicab office with the dark blue front), and press E at her window. Press T near someone to talk to them first, if you like.");
	const TCHAR* ErrandLine() { return bRitasWindow ? kErrandRitas : kErrandMickeys; }

	// SHEILA'S WALK-ROUND, 30 September (town list 6cg, day one; the twenty a
	// friend would notice, 6: a clear first purpose). A new game opens on her
	// five stops in her own words (DayOne.h), as plain text until her voice
	// passes the accent gate, one at a time for its reading time or until he
	// presses Enter; he stands until she has done. Played or skipped, it ends
	// the same way: she has met him, the hints begin, the moment to talk has
	// come (its hint when the hints are next asked), and the errand is given.
	int32 GWalkStop = -1;
	double GWalkAt = 0.0, GWalkUntil = 0.0;
	bool bWalkLocked = false, bWalkEnterWasDown = true;   // true: a held Enter from the title is not a press
	FString GWalkLine;

	void WalkRoundEnd(UWorld* World)
	{
		if (!GWalkLine.IsEmpty()) { const FString Was = GWalkLine; GSubs.RemoveAll([&Was](const FSubLine& L) { return L.Text == Was; }); SubsRebuild(); }
		GWalkLine.Empty();
		PromptSet(FString());
		if (bWalkLocked)
		{
			if (APlayerController* PC = World != nullptr ? World->GetFirstPlayerController() : nullptr) { PC->ResetIgnoreMoveInput(); }
			bWalkLocked = false;
		}
		bSheilaMet = true;
		GMet.Met("lena", GNow.Day);
		bHintsOn = true;
		bHintsMoved = false;
		bHintsFromSet = false;   // where he stands now is where he starts
		GHints.Begin(NowS(), true);
		LedgerCore::Hint H;
		if (LedgerCore::DayOne::WalkRoundEnds(&GHints, NowS(), H)) { HintShow(H); }
		UE_LOG(LogTemp, Display, TEXT("LedgerDayOne: the walk-round ends at stop %d of %d; the hints begin"), GWalkStop, LedgerCore::DayOne::WalkRoundCount);
		Say(ErrandLine(), 40.0f, FColor::Yellow);
		GPhase = ECrimePhase::LiveWaitDeed;
	}

	void WalkRoundTick(UWorld* World)
	{
		// Nothing to use until she has shown him round.
		TakeActRequests(0);
		TakeTalkRequests();
		APlayerController* PC = World != nullptr ? World->GetFirstPlayerController() : nullptr;
		if (PC != nullptr && !bWalkLocked) { PC->SetIgnoreMoveInput(true); bWalkLocked = true; }
		const double T = NowS();
		// ENTER, SEEN AS A KEY GOING DOWN: this ticker runs outside the
		// frame's input, after "just pressed" is cleared (the tester pressed
		// Enter and nothing moved on, 30 September).
		const bool bEnterDown = PC != nullptr && PC->IsInputKeyDown(EKeys::Enter);
		const bool bNext = bEnterDown && !bWalkEnterWasDown && GWalkStop >= 0 && T - GWalkAt > 0.6;
		bWalkEnterWasDown = bEnterDown;
		if (GWalkStop < 0 || bNext || T >= GWalkUntil)
		{
			if (!GWalkLine.IsEmpty()) { const FString Was = GWalkLine; GSubs.RemoveAll([&Was](const FSubLine& L) { return L.Text == Was; }); SubsRebuild(); }
			++GWalkStop;
			if (GWalkStop >= LedgerCore::DayOne::WalkRoundCount) { WalkRoundEnd(World); return; }
			const LedgerCore::DayOne::Stop& S = LedgerCore::DayOne::WalkRound[GWalkStop];
			GWalkLine = FString(TEXT("Sheila: \"")) + Un(S.Line) + TEXT("\"");
			const double Seconds = 2.5 + 0.065 * (double)FCString::Strlen(*Un(S.Line));
			Say(GWalkLine, (float)Seconds + 1.0f);
			GWalkAt = T;
			GWalkUntil = T + Seconds;
			UE_LOG(LogTemp, Display, TEXT("LedgerDayOne: stop %d, %s"), GWalkStop, *Un(S.Name));
		}
		PromptSet(TEXT("Enter  go on"));
	}

	void StartLive(UWorld* World, bool bTryLoad)
	{
		// COME BACK AND THE TOWN STILL KNOWS: a save from before is
		// read, and the street goes straight to what they know.
		// -LiveFresh STARTS THE STORY AGAIN: the old save is left where it
		// is and written over once the new story reaches "later".
		if (bTryLoad && IFileManager::Get().FileExists(*(EncSaveDir() / TEXT("agents.json"))))
		{
			LoadEncounterFromDisk();
			if (bLoadedFromDisk && !bLiveScript)
			{
				// A REAL RELOAD (Jafar's list, item 1): the street as he left it,
				// the clock where it stood, the deed done or not yet, the light
				// the hour's.
				bClockRuns = true;
				GLightNight = -1;
				GPhase = bDeedDone ? ECrimePhase::LiveRoam : ECrimePhase::LiveWaitDeed;
				RespawnMate(World);   // Ron in the street, as in a new game
				GWindowLooksBroken = -1;
				WindowLook();         // Rita's window as the record has it at this hour
				if (bLoadPlace)
				{
					TeleportPawn(World, GLoadX, GLoadZ, GLoadYaw);
					// The camera behind him again, not only his heading (the tester:
					// after Continue he faced the camera).
					if (AController* C = GPawn != nullptr ? GPawn->GetController() : nullptr) { C->SetControlRotation(FRotator(0.0f, (float)GLoadYaw, 0.0f)); }
					UE_LOG(LogTemp, Display, TEXT("LedgerLoad: back where he stood, %.2f, %.2f"), GLoadX, GLoadZ);
				}
				Say(FString(TEXT("The street remembers. ")) + Un(GNow.ToString()) + TEXT("."), 8.0f, FColor::Yellow);
			}
			else if (bLoadedFromDisk)
			{
				RespawnMate(World);
				GPhase = ECrimePhase::LiveRoam;
				UE_LOG(LogTemp, Log, TEXT("LedgerCrime evening light: %s"),
				       *LedgerVignetteShot::ApplyPlayCondition(kEveningCondition));
				Say(TEXT("The street remembers. Darren, Sheila and Ron are in the yard across the road from Rita's pawn shop, through the gap between the houses. Press T near one of them to talk."), 40.0f, FColor::Yellow);
			}
		}
		if (GPhase == ECrimePhase::LiveWaitDeed && !bLoadedFromDisk)
		{
			// A NEW GAME: the talk program starts with nobody's talk
			// (handover 6r), not the last story's.
			GLive.bTalkReset = true;
			GLive.bTalkLoad = false;
			GLive.Remarks = StreetVoice::RemarkLedger();   // and nobody has said anything to him yet
			GTownHours = TownHours();                      // nor has the town talked an hour (town list 6bs)
			if (!bLiveScript)
			{
				GClock = LiveClock(GameTime(0, 9, 0));
				GNow = GClock.Now();
				bClockRuns = true;
				GWeek = TownWeek();
				bSheilaTrusts = false;
				GTeaMinuteDone = -1;
				GWaitShown.clear();
				GMet = LedgerCrime::MeetingBook();
				GPlacedFor.clear();
				GHeldBackSince.clear();
				GHeardOnly.clear();
				bPlaceNow = false;   // a new game: they take their places out of his sight
				// RON IS IN THE STREET FROM THE START in free play, at his place in
				// the yard across from Rita's (the tester, 30 September: only the
				// scripted story brought him on, so nobody could tell him no).
				RespawnMate(World);
				GLightNight = -1;
			}
			GWatchSlot = 0;
			// DAY ONE FIRST (town list 6cg; the twenty a friend would notice,
			// 6): in free play Sheila shows him round before he can walk, and
			// the errand follows it (WalkRoundEnd).
			if (bLiveScript) { Say(ErrandLine(), 40.0f, FColor::Yellow); }
			else
			{
				GPhase = ECrimePhase::LiveWalkRound;
				GWalkStop = -1;
			}
		}
		// THE SESSION RECORD STARTS (handover 6p): a new game or a
		// loaded save, and the deed the save holds.
		LedgerSession::Start(CrimeSha(), !bLoadedFromDisk, SessionCastFile());
		// THE HINTS BEGIN (town list 6y), in free play only, when he has
		// control: after a load at once, keeping those already shown; in a
		// new game when Sheila's walk-round ends (WalkRoundEnd). Sheila has
		// met him either way.
		if (!bLiveScript && bLoadedFromDisk)
		{
			FString Saved;
			const bool bSaved = FFileHelper::LoadFileToString(Saved, *(EncSaveDir() / TEXT("hints.json")));
			const std::string SavedJson = Utf8(Saved);
			bHintsOn = true;
			bHintsMoved = false;
			bHintsFromSet = false;
			GHints.Begin(NowS(), false, bSaved ? &SavedJson : nullptr);
			bSheilaMet = true;
			UE_LOG(LogTemp, Display, TEXT("LedgerHints: begun, a load, %d done"), (int32)GHints.Done().size());
		}
		if (bLoadedFromDisk)
		{
			TArray<FString> Deeds;
			if (bDeedDone || !GFiledSummaryA.empty()) { Deeds.Add(Un(DeedKeyNow())); }
			LedgerSession::Write(TEXT("load"), TEXT("\"from\":") + LedgerSession::Str(FPaths::ConvertRelativePathToFull(EncSaveDir()))
				+ TEXT(",\"deeds\":") + LedgerSession::List(Deeds));
		}
		FCoreDelegates::OnEnginePreExit.AddStatic(&SessionEndAtExit);
	}

	bool Tick(float)
	{
		// PAUSED: the clock held, the line shown, nothing else runs.
		{
			UWorld* PW = GameWorld();
			const bool bPausedNow = PW != nullptr && UGameplayStatics::IsGamePaused(PW);
			if (bPausedNow && GPausedSince < 0.0)
			{
				GPausedSince = FPlatformTime::Seconds();
				Say(kPausedLine, 86400.0f, FColor::Yellow);
			}
			else if (!bPausedNow && GPausedSince >= 0.0)
			{
				GPausedTotal += FPlatformTime::Seconds() - GPausedSince;
				GPausedSince = -1.0;
				GSubs.RemoveAll([](const FSubLine& L) { return L.Text == kPausedLine; });
				SubsRebuild();
			}
			if (bPausedNow) { return true; }
		}
		++GTicks;
		const double Now = NowS();
		if (GRunStart == 0.0) { GRunStart = Now; GPhaseStart = Now; GLastTick = Now; }
		const double Delta = Now - GLastTick;
		GLastTick = Now;
		UWorld* World = GameWorld();
		StopShoutRecording(false);
		SubsTick();
		HintsTick();
		// THE TITLE, as soon as there is a player to show it to; the street
		// goes on building behind it.
		if (!bTitleAsked && World != nullptr && World->GetFirstPlayerController() != nullptr)
		{
			bTitleAsked = true;
			if (TitleWanted()) { LedgerTitle::Show(World, IFileManager::Get().FileExists(*(EncSaveDir() / TEXT("agents.json")))); }
		}
		if (LedgerTitle::IsShown() && GPhase != ECrimePhase::LiveTitle
		    && LedgerTitle::Tick(World, false) == LedgerTitle::EChoice::Quit) { FPlatformMisc::RequestExit(false); }

		// THE WATCHING CLOCK RUNS UNDER EVERY PHASE INSIDE A CRIME'S WINDOW,
		// including the seconds the pawn stands at the window while a
		// milestone frame is being written: she is looking at him then too,
		// and pretending otherwise would understate the one number the
		// accepting case turns on.
		if (GWatchSlot >= 0) { AccrueWatching(World, Delta); }

		switch (GPhase)
		{
		case ECrimePhase::WaitWorld:
		{
			if (World == nullptr && (Now - GPhaseStart) <= kWorldCeiling) { return true; }
			if (World == nullptr)
			{
				GFinishReason = TEXT("world-ceiling-bit-at-45s");
				Finish();
				return false;
			}
			WriteBreadcrumb(TEXT("world-found"));
			GPhase = ECrimePhase::WaitPawn;
			GPhaseStart = Now;
			return true;
		}
		case ECrimePhase::WaitPawn:
		{
			APlayerController* PC = (World != nullptr) ? World->GetFirstPlayerController() : nullptr;
			APawn* P = (PC != nullptr) ? PC->GetPawn() : nullptr;
			if (P == nullptr && (Now - GPhaseStart) <= kPawnCeiling) { return true; }
			if (P == nullptr)
			{
				GFinishReason = TEXT("pawn-ceiling-bit-at-30s-no-player-controller-or-pawn");
				Finish();
				return false;
			}
			GPawn = P;
			WriteBreadcrumb(TEXT("pawn-found"));
			GPhase = ECrimePhase::SettleAfterSpawn;
			GPhaseStart = Now;
			return true;
		}
		case ECrimePhase::SettleAfterSpawn:
		{
			if ((Now - GPhaseStart) < kSettleAfterSpawn) { return true; }
			GPhase = ECrimePhase::PlaceProps;
			GPhaseStart = Now;
			return true;
		}
		case ECrimePhase::PlaceProps:
		{
			PlaceProps(World);
			LoadBank();
			// The pawn starts at S, facing down the street: +x, which is yaw 0
			// in this engine and in the shared file alike.
			TeleportPawn(World, LedgerCrime::kStartX, LedgerCrime::kStartZ, 0.0);
			WriteBreadcrumb(TEXT("props-placed"));
			GBeat = "start"; GBeatSpeaker = "none"; GBeatLineId = "none"; GBeatHeard = false;
			GPhase = (GEnc == EEncounter::Reload) ? ECrimePhase::LoadDisk
			       : (GEnc == EEncounter::Unseen) ? ECrimePhase::MoveW1ToYard
			       : (GEnc == EEncounter::Live) ? ECrimePhase::LiveWaitDeed
			       : ECrimePhase::ShotStart;
			// THE TITLE COMES FIRST in a friend's game (TitleScreen.h): the
			// story waits in LiveTitle for New game or Continue.
			if (GEnc == EEncounter::Live && LedgerTitle::IsShown())
			{
				GPhase = ECrimePhase::LiveTitle;
				GPhaseStart = Now;
				return true;
			}
			if (GEnc == EEncounter::Live) { StartLive(World, !FParse::Param(FCommandLine::Get(), TEXT("LiveFresh"))); }
			GPhaseStart = Now;
			return true;
		}
		case ECrimePhase::LiveTitle:
		{
			const LedgerTitle::EChoice Choice = LedgerTitle::Tick(World, true);
			if (Choice == LedgerTitle::EChoice::None) { return true; }
			if (Choice == LedgerTitle::EChoice::Quit) { FPlatformMisc::RequestExit(false); return true; }
			LedgerTitle::Hide(World);
			GPhase = ECrimePhase::LiveWaitDeed;
			StartLive(World, Choice == LedgerTitle::EChoice::Continue);
			GPhaseStart = Now;
			return true;
		}
		case ECrimePhase::ShotStart:
			return RunShotPhase(TEXT("start"), TEXT("ue-crime_00_start.png"),
			                    ECrimePhase::ApproachA, Now);
		case ECrimePhase::ApproachA:
		{
			if (GWatchSlot != 0) { GWatchSlot = 0; GBeat = "approach_a"; }
			if (GPawn != nullptr && !GSeqInFlight)
			{
				GPawn->AddMovementInput(GPawn->GetActorForwardVector(), 1.0f);
			}
			MaybeCaptureSequence(Now);
			if ((Now - GPhaseStart) < kApproachSeconds) { return true; }
			GPhase = ECrimePhase::PlaceForA;
			GPhaseStart = Now;
			return true;
		}
		case ECrimePhase::PlaceForA:
		{
			// AT THE WINDOW, FACING IT. Yaw 90 is +z in this engine and in
			// the shared file, which is across the footway into the glass.
			// A1, ruled 2026-09-08: the keys file records the CUT the clip
			// will show. clip-from-frames.py reads only heard and lineId from a
			// row, so a new beat name changes no caption and no selftest.
			GBeat = "at_window_a";
			TeleportPawn(World, LedgerCrime::kCrimeAX, LedgerCrime::kCrimeAZ, 90.0);
			GPhase = ECrimePhase::SettleA;
			GPhaseStart = Now;
			return true;
		}
		case ECrimePhase::SettleA:
		{
			MaybeCaptureSequence(Now);
			if ((Now - GPhaseStart) < kSettleAfterTeleport) { return true; }
			GPhase = ECrimePhase::MeasureA;
			GPhaseStart = Now;
			return true;
		}
		case ECrimePhase::MeasureA:
		{
			// BEFORE THE DEED, WITH THE GLASS STANDING. See this file's
			// header: measuring after the hide inverts the accepting case.
			GReadings.push_back(MeasureVantage(World, "w1", "A", GW1Body, GGlass[0],
			                                   GSeconds[0][0]));
			GReadings.push_back(MeasureVantage(World, "n2", "A", GN2Body, GGlass[0],
			                                   GSeconds[0][1]));
			if (GC1Body != nullptr)
			{
				GC1Reading[0] = MeasureVantage(World, "c1", "A", GC1Body, GGlass[0], GC1Seconds[0]);
				GC1Reading[0].Familiarity = LedgerCrime::kConstableFamiliarity;
			}
			WriteBreadcrumb(TEXT("vantage-a-measured"));
			GPhase = ECrimePhase::ShotBeforeA;
			GPhaseStart = Now;
			return true;
		}
		case ECrimePhase::ShotBeforeA:
			return RunShotPhase(TEXT("before_crime_a"), TEXT("ue-crime_01_before_crime_a.png"),
			                    ECrimePhase::SeqBeforeA, Now);
		case ECrimePhase::SeqBeforeA:
			return RunForcedSeqPhase(ECrimePhase::AwaitActA, Now);
		case ECrimePhase::AwaitActA:
			// NO PRESS, NO DEED, and the routing is where that is enforced:
			// a give-up goes to SeqAfterA and this phase is never entered.
			return RunAwaitActPhase(World, 0, ECrimePhase::CommitA,
			                        ECrimePhase::SeqAfterA, Now);
		case ECrimePhase::CommitA:
		{
			GBeat = "deed_a";
			CommitDeed(World, 0);
			// READ OFF THE DEED, NOT OFF THE DECISION. Setting this before
			// CommitDeed meant a run where the window was not in the street
			// still reported the act as having happened.
			GActTook[0] = GCrime[0].bPieceFound && GCrime[0].bHiddenAfter;
			ResolveAndFile(0);
			GWatchSlot = -1;
			WriteBreadcrumb(TEXT("crime-a-committed"));
			GPhase = ECrimePhase::SeqAfterA;
			GPhaseStart = Now;
			return true;
		}
		case ECrimePhase::SeqAfterA:
			return RunForcedSeqPhase(ECrimePhase::ShotAfterA, Now);
		case ECrimePhase::ShotAfterA:
			return RunShotPhase(TEXT("after_crime_a"), TEXT("ue-crime_02_after_crime_a.png"),
			                    GEnc == EEncounter::Play ? ECrimePhase::FleeYard : ECrimePhase::Round1, Now);
		case ECrimePhase::FleeYard:
		{
			// HE RUNS: through the yard behind the parade, past the lad.
			GBeat = "flee_yard";
			TeleportPawn(World, LedgerCrime::kFleeX, LedgerCrime::kFleeZ, LedgerCrime::kFleeYawDeg);
			GFleeSeconds = 0.0;
			GPhase = ECrimePhase::FleeWatch;
			GPhaseStart = Now;
			return true;
		}
		case ECrimePhase::FleeWatch:
		{
			// THE LAD SEES HIM OR DOES NOT, by the same test the witnesses
			// are held to: seconds accrue only while the sightline holds.
			if (GN2Body != nullptr && GPawn != nullptr && (Now - GPhaseStart) >= kSettleAfterTeleport)
			{
				const LedgerCrime::Reading W = MeasureVantage(World, GIdN2, "flee", GN2Body, nullptr, 0.0);
				if (Perception::InSight(W.ActorMetres, W.ActorOffAxisDeg, LedgerCrime::kLightLevel, W.bActorOccluded, 1.4))
				{
					GFleeSeconds += Delta;
				}
			}
			if ((Now - GPhaseStart) < kSettleAfterTeleport + LedgerCrime::kFleeSeconds) { return true; }
			FileFleeSighting(World);
			// BACK TO THE WINDOW HE LEFT, so the walk on to the second window
			// starts where it always has.
			TeleportPawn(World, LedgerCrime::kCrimeAX, LedgerCrime::kCrimeAZ, 90.0);
			WriteBreadcrumb(TEXT("flee-yard-watched"));
			GPhase = ECrimePhase::Round1;
			GPhaseStart = Now;
			return true;
		}
		case ECrimePhase::Round1:
		{
			// THE ACCEPTING HALF OF THE GOSSIP PAIR'S OPPOSITE: the same two
			// people, the same rumour, the same tie, and nineteen metres of
			// street between them. Nothing may pass.
			RunGossipRound(1, GRound1);
			WriteBreadcrumb(TEXT("gossip-round-1"));
			GPhase = ECrimePhase::MoveW1ToYard;
			GPhaseStart = Now;
			return true;
		}
		case ECrimePhase::MoveW1ToYard:
		{
			MoveBody(World, GW1Body, LedgerCrime::kW1BX, LedgerCrime::kW1BZ);
			FaceBody(GW1Body, LedgerCrime::P3(LedgerCrime::kCrimeBX, 0.0, LedgerCrime::kCrimeBZ));
			MoveBody(World, GC1Body, LedgerCrime::kC1BX, LedgerCrime::kC1BZ);
			FaceBody(GC1Body, LedgerCrime::P3(LedgerCrime::kCrimeBX, 0.0, LedgerCrime::kCrimeBZ));
			GPhase = ECrimePhase::ApproachB;
			GPhaseStart = Now;
			return true;
		}
		case ECrimePhase::ApproachB:
		{
			if (GWatchSlot != 1) { GWatchSlot = 1; GBeat = "approach_b"; }
			if (GPawn != nullptr && !GSeqInFlight)
			{
				// WALKING ON, +x, the direction the street runs. The pawn was
				// left facing the window, so the direction is named rather
				// than taken from its forward vector.
				GPawn->AddMovementInput(FVector(1.0f, 0.0f, 0.0f), 1.0f);
			}
			MaybeCaptureSequence(Now);
			if ((Now - GPhaseStart) < kApproachSeconds) { return true; }
			GPhase = ECrimePhase::PlaceForB;
			GPhaseStart = Now;
			return true;
		}
		case ECrimePhase::PlaceForB:
		{
			// A1, ruled 2026-09-08: the keys file records the CUT the clip
			// will show. clip-from-frames.py reads only heard and lineId from a
			// row, so a new beat name changes no caption and no selftest.
			GBeat = "at_window_b";
			TeleportPawn(World, LedgerCrime::kCrimeBX, LedgerCrime::kCrimeBZ, 90.0);
			GPhase = ECrimePhase::SettleB;
			GPhaseStart = Now;
			return true;
		}
		case ECrimePhase::SettleB:
		{
			MaybeCaptureSequence(Now);
			if ((Now - GPhaseStart) < kSettleAfterTeleport) { return true; }
			GPhase = ECrimePhase::MeasureB;
			GPhaseStart = Now;
			return true;
		}
		case ECrimePhase::MeasureB:
		{
			GReadings.push_back(MeasureVantage(World, "w1", "B", GW1Body, GGlass[1],
			                                   GSeconds[1][0]));
			GReadings.push_back(MeasureVantage(World, "n2", "B", GN2Body, GGlass[1],
			                                   GSeconds[1][1]));
			if (GC1Body != nullptr)
			{
				GC1Reading[1] = MeasureVantage(World, "c1", "B", GC1Body, GGlass[1], GC1Seconds[1]);
				GC1Reading[1].Familiarity = LedgerCrime::kConstableFamiliarity;
			}
			WriteBreadcrumb(TEXT("vantage-b-measured"));
			GPhase = ECrimePhase::ShotBeforeB;
			GPhaseStart = Now;
			return true;
		}
		case ECrimePhase::ShotBeforeB:
			return RunShotPhase(TEXT("before_crime_b"), TEXT("ue-crime_03_before_crime_b.png"),
			                    ECrimePhase::SeqBeforeB, Now);
		case ECrimePhase::SeqBeforeB:
			return RunForcedSeqPhase(ECrimePhase::AwaitActB, Now);
		case ECrimePhase::AwaitActB:
			return RunAwaitActPhase(World, 1, ECrimePhase::CommitB,
			                        ECrimePhase::SeqAfterB, Now);
		case ECrimePhase::CommitB:
		{
			GBeat = "deed_b";
			CommitDeed(World, 1);
			GActTook[1] = GCrime[1].bPieceFound && GCrime[1].bHiddenAfter;
			ResolveAndFile(1);
			GWatchSlot = -1;
			// AND THE CONSTABLE LEAVES. His last question has been asked, and
			// the overheard beat that follows is filmed facing into the yard
			// where he stood for B: left there, he would be a third figure a
			// few metres behind the two witnesses in the frame that is about
			// them, which changes the run's visible output and puts a
			// policeman beside two people gossiping - a canon question nobody
			// asked. Hidden and made intangible the way the broken glass is.
			if (GC1Body != nullptr)
			{
				GC1Body->SetActorHiddenInGame(true);
				GC1Body->SetActorEnableCollision(false);
			}
			WriteBreadcrumb(TEXT("crime-b-committed"));
			GPhase = ECrimePhase::SeqAfterB;
			GPhaseStart = Now;
			return true;
		}
		case ECrimePhase::SeqAfterB:
			return RunForcedSeqPhase(ECrimePhase::ShotAfterB, Now);
		case ECrimePhase::ShotAfterB:
			return RunShotPhase(TEXT("after_crime_b"), TEXT("ue-crime_04_after_crime_b.png"),
			                    ECrimePhase::Round2, Now);
		case ECrimePhase::Round2:
		{
			RunGossipRound(2, GRound2);
			// THE REPLY, AT THE RUNG SHE REACHED AND NEVER ABOVE IT.
			{
				// NO CLAUSE ON AN OVERHEARD ROW, BY DESIGN: n2's reply is
				// spoken whole and never filed as anybody's Summary, so there
				// is nothing for a splice to get wrong. Clause comes back empty
				// here and nothing reads it.
				std::string Id, Text, Clause, Speaker, Why;
				int Variants = 0;
				const int Seed = LedgerCrime::Seed(GNow);
				if (LedgerCrime::BankPick(GBankText, "overheard", GAchievedRung, Seed,
				                          Id, Text, Clause, Speaker, Variants, Why))
				{
					GReplyText = Text;
					GOverheard.ReplyId = Id;
					GOverheard.Variants = Variants;
					GOverheard.VariantPicked = LedgerCrime::VariantIndex(Seed, Variants);
					GOverheard.SeedValue = Seed;
				}
				else if (GOverheard.WhyNot == "none") { GOverheard.WhyNot = Why; }
			}
			// AND THE EXCHANGE IS COMPOSED, queue 147. The bank above supplied
			// the rung and the id, which is what run 32 measured and what a
			// composed line would otherwise delete; this builds the sentence
			// the two of them actually say, around the summary the mill
			// carried, through the ported StreetVoice.Exchange. A refusal
			// falls back to the bank rows and says why on the verdict.
			GOverheard.Reply = LedgerCrime::ComposeOverheard(
				GCarried, GW1, GN2, LedgerCrime::Seed(GNow),
				GSummaryText == "none" ? std::string() : GSummaryText,
				GReplyText == "none" ? std::string() : GReplyText);
			GOverheard.Events = GRound2.Passed;
			WriteBreadcrumb(TEXT("gossip-round-2"));
			GPhase = (GEnc == EEncounter::Unseen) ? ECrimePhase::MeetThird : ECrimePhase::MoveToOverhear;
			GPhaseStart = Now;
			return true;
		}
		case ECrimePhase::MoveToOverhear:
		{
			// THE PLAYER STANDS IN EARSHOT, facing into the yard: yaw -90 is
			// -z, which is where the two of them are.
			TeleportPawn(World, LedgerCrime::kOverhearX, LedgerCrime::kOverhearZ, -90.0);
			GPhase = ECrimePhase::SettleOverhear;
			GPhaseStart = Now;
			return true;
		}
		case ECrimePhase::SettleOverhear:
		{
			MaybeCaptureSequence(Now);
			if ((Now - GPhaseStart) < kSettleAfterTeleport) { return true; }
			// MEASURED FROM THE PAWN TO EACH BODY, in metres, against the
			// earshot the game itself uses.
			if (GPawn != nullptr && GW1Body != nullptr)
			{
				GOverheard.PlayerToW1M = (double)FVector::Dist(
					GPawn->GetActorLocation(), GW1Body->GetActorLocation()) / 100.0;
			}
			if (GPawn != nullptr && GN2Body != nullptr)
			{
				GOverheard.PlayerToN2M = (double)FVector::Dist(
					GPawn->GetActorLocation(), GN2Body->GetActorLocation()) / 100.0;
			}
			GBeat = "overheard";
			GBeatSpeaker = "w1";
			GBeatLineId = GOverheard.SummaryId;
			GBeatLineText = GOverheard.Reply.TellText;
			GBeatLineTextSource = LedgerCrime::BeatTextSource(GOverheard.Reply, /*bTell=*/true);
			GBeatHeard = GOverheard.Heard();
			GPhase = ECrimePhase::OverheardHold;
			GPhaseStart = Now;
			return true;
		}
		case ECrimePhase::OverheardHold:
		{
			// TWO BEATS, THE WAY THE GAME STAGES THEM: her telling, then his
			// reply a beat later, at GossipDirector's own i * 2.1 seconds.
			if ((Now - GPhaseStart) >= LedgerCrime::kSayAfterSeconds && GBeatSpeaker != "n2")
			{
				GBeatSpeaker = "n2";
				GBeatLineId = GOverheard.ReplyId;
				GBeatLineText = GOverheard.Reply.ReplyText;
				GBeatLineTextSource = LedgerCrime::BeatTextSource(GOverheard.Reply, /*bTell=*/false);
			}
			MaybeCaptureSequence(Now);
			if ((Now - GPhaseStart) < LedgerCrime::kOverheardHoldSeconds) { return true; }
			GPhase = ECrimePhase::ShotOverheard;
			GPhaseStart = Now;
			return true;
		}
		case ECrimePhase::ShotOverheard:
			return RunShotPhase(TEXT("overheard"), TEXT("ue-crime_05_overheard.png"),
			                    ECrimePhase::MeetThird, Now);
		case ECrimePhase::MeetThird:
		{
			// THE LAD MEETS HIS MATE IN THE YARD ON DAY 4 AT SIX. His body
			// arrives now and not before, so nothing earlier in the run could
			// have reached him. GNow is moved for this one Tick - the heard
			// memory is stamped with the day it happened - and put back, so
			// nothing else in the verdict reads a clock that moved under it.
			{
				double GY = 0.0;
				std::string On;
				if (!GroundYAt(World, LedgerCrime::kR3X, LedgerCrime::kR3Z, GY, On)) { GY = 0.1; }
				GR3Body = SpawnBody(World, TEXT("probe_body_r3"),
				                    LedgerCrime::kR3X, LedgerCrime::kR3Z, GY);
				const GameTime Was = GNow;
				GNow = GameTime(LedgerCrime::kRound3Day, LedgerCrime::kRound3Hour, 0);
				RunRound3(GRound3);
				// THE ENCOUNTER'S CLOCK MOVES ON with the story: the player
				// finds the lad half an hour after he met his mate.
				GNow = (GEnc != EEncounter::None) ? GameTime(LedgerCrime::kRound3Day, LedgerCrime::kRound3Hour, 30) : Was;
				WriteBreadcrumb(TEXT("third-resident-met"));
			}
			GPhase = (GEnc != EEncounter::None) ? ECrimePhase::Talk : ECrimePhase::Done;
			GPhaseStart = Now;
			return true;
		}
		case ECrimePhase::Talk:
		{
			RunTalk();
			WriteBreadcrumb(TEXT("encounter-talked"));
			GPhase = (GEnc == EEncounter::Play) ? ECrimePhase::SaveDisk : ECrimePhase::Done;
			GPhaseStart = Now;
			return true;
		}
		case ECrimePhase::SaveDisk:
		{
			SaveEncounterToDisk();
			WriteBreadcrumb(TEXT("encounter-saved-to-disk"));
			GPhase = ECrimePhase::Done;
			GPhaseStart = Now;
			return true;
		}
		case ECrimePhase::LoadDisk:
		{
			LoadEncounterFromDisk();
			WriteBreadcrumb(TEXT("encounter-loaded-from-disk"));
			GPhase = ECrimePhase::Talk;
			GPhaseStart = Now;
			return true;
		}
		case ECrimePhase::LiveWalkRound:
		{
			ClockTick(Delta);
			WalkRoundTick(World);
			return true;
		}
		case ECrimePhase::LiveWaitDeed:
		{
			ClockTick(Delta);
			if (!bLiveScript) { WaitKeyTick(World); }
			if (!bLiveScript) { LivePromptTick(true); }
			if (bLiveScript || bAskAfterDeed)
			{
				if (bLiveScript) { LiveVoiceStart(); }
				if (GLiveStep == 0)
				{
					TeleportPawn(World, LedgerCrime::kCrimeAX, LedgerCrime::kCrimeAZ, 90.0);
					GLiveStep = 1; GLiveStepAt = Now;
					return true;
				}
				if (GLiveStep == 1 && Now - GLiveStepAt >= 2.0) { PressKey(World, EKeys::E); GLiveStep = 2; }
			}
			if (!bLiveScript && HumanTalkTick(World, Now)) { TakeActRequests(0); return true; }
			const int32 Presses = TakeActRequests(0);
			if (bLiveScript) { TakeTalkRequests(); }
			if (Presses <= 0 || GPawn == nullptr || GGlass[0] == nullptr) { return true; }
			const double ToGlass = FVector::Dist2D(GPawn->GetActorLocation(),
				GGlass[0]->GetComponentsBoundingBox(true).GetCenter()) / 100.0;
			if (ToGlass > LedgerCrime::kLiveReachM)
			{
				Say(bRitasWindow ? TEXT("Nothing to break here. The window is Rita's, the pawn shop two doors up from Mickey's.")
				                 : TEXT("Nothing to break here. The window is by Mickey's door."), 4.0f);
				return true;
			}
			// THE SAME DEED AS THE REGRESSION: the vantage measured with the
			// glass standing, then the deed, then what she saw filed.
			if (bRitasWindow && !bLiveScript && bGCast) { DeedOnlookers(World); }
			else
			{
				GReadings.push_back(MeasureVantage(World, GIdW1, "A", GW1Body, GGlass[0], GSeconds[0][0]));
				GReadings.push_back(MeasureVantage(World, GIdN2, "A", GN2Body, GGlass[0], GSeconds[0][1]));
			}
			GActRequestsSeen[0] += Presses;
			GActAttempted[0] = true;
			// The deed's story key before anybody files it (the review's A3).
			if (bRitasWindow) { GWindowTopic = "player.window_d" + std::to_string(GNow.Day); }
			CommitDeed(World, 0);
			GActTook[0] = GCrime[0].bPieceFound && GCrime[0].bHiddenAfter;
			ResolveAndFile(0);
			GWatchSlot = -1;
			GFleeSeconds = 0.0;
			GLiveDeedAt = Now;
			GLiveDeedGameAt = GNow;
			LedgerSession::Write(TEXT("deed"), TEXT("\"what\":") + LedgerSession::Str(Un(bRitasWindow ? GWindowTopic : std::string("player.window_d1"))));
			MarkDeedTime();
			DeedFollows();
			// AND SEEN: broken glass on the pavement under the window, in play
			// only (the regression's piece counts do not move). A clear pane
			// that vanishes looks the same as a clear pane.
			// (Rita's window brings its own glass on the pavement, built with the street.)
			for (int32 K = 0; K < (bRitasWindow ? 0 : 14); ++K)
			{
				const double Fx = LedgerCrime::kCrimeAX + ((K * 37) % 29 - 14) * 0.1;
				const double Fz = 4.45 + ((K * 53) % 11) * 0.045;
				double Gy = 0.0;
				std::string On;
				if (!GroundYAt(World, Fx, Fz, Gy, On)) { Gy = 0.12; }
				const double Sx = 0.04 + ((K * 17) % 7) * 0.02, Sz = 0.03 + ((K * 29) % 5) * 0.02;
				LedgerVignetteShot::SpawnProbePiece(World, FString::Printf(TEXT("live_glass_shard_%02d"), K),
					FVector((float)Fx, (float)(Gy + 0.006), (float)Fz), FVector((float)Sx, 0.008f, (float)Sz),
					TEXT("box"), TEXT("metal"));
			}
			// THE DEED IS SAID, NOT ONLY DONE (the AI tester, 24 September): a
			// pane of clear glass that vanishes is invisible, and the shout is
			// only a sound, so the tester pressed E, broke the window and
			// reported that nothing happened.
			// PEOPLE TURN TO THE SMASH, 29 September (the twenty a friend would
			// notice, 16): every head within 25 m, after a start that grows with
			// the distance, for three and a half seconds.
			if (GGlass[0] != nullptr)
			{
				const FVector Where = GGlass[0]->GetComponentsBoundingBox(true).GetCenter();
				int32 Turned = 0;
				for (TObjectIterator<ULedgerPersonAnim> It; It; ++It)
				{
					const USkeletalMeshComponent* M = It->GetSkelMeshComponent();
					if (M == nullptr || M->GetWorld() != World || !It->bLook) { continue; }
					const float D = (float)FVector::Dist(M->GetComponentLocation(), Where);
					if (D > 2500.0f) { continue; }
					It->LookToward(Where, 0.2f + D / 3000.0f, 3.5f);
					++Turned;
				}
				UE_LOG(LogTemp, Display, TEXT("LedgerCrime: %d head(s) turn to the smash"), Turned);
			}
			// THE ERRAND IS DONE, so its instruction goes (the tester, 30
			// September: "Walk to Mickey's front window" stayed up after it).
			GSubs.RemoveAll([](const FSubLine& L) { return L.Text == kErrandMickeys || L.Text == kErrandRitas; });
			SubsRebuild();
			Say(TEXT("The window goes in with a crash."), 16.0f, FColor::Orange);
			if (!GFiledSummaryA.empty()) { Say(TEXT("Sheila: \"Stop. I mean it. Stop.\""), 16.0f); }
			// SOMEBODY SAW THAT (town list 6y): she filed what she saw.
			if (!GFiledSummaryA.empty()) { HintHappened(LedgerCore::Moment::SeenAtDeed); }
			WriteBreadcrumb(TEXT("live-deed"));
			if (bLiveScript)
			{
				// A PICTURE OF THE WINDOW JUST AFTER, from where he stands; he
				// runs for the yard a moment later.
				if (APlayerController* PC = World->GetFirstPlayerController()) { PC->SetControlRotation(FRotator(-12.0f, 90.0f, 0.0f)); }
				FScreenshotRequest::RequestScreenshot(FPaths::ConvertRelativePathToFull(FPaths::ProjectDir()
					/ TEXT("ue-encounter-live-deed.png")), true, false);
			}
			GPhase = ECrimePhase::LiveAfterDeed;
			GPhaseStart = Now;
			return true;
		}
		case ECrimePhase::LiveAfterDeed:
		{
			ClockTick(Delta);
			if (!bLiveScript) { WaitKeyTick(World); }
			if (bLiveScript && !bLiveFled && Now - GLiveDeedAt >= 1.0)
			{
				TeleportPawn(World, LedgerCrime::kFleeX, LedgerCrime::kFleeZ, LedgerCrime::kFleeYawDeg);
				bLiveFled = true;
			}
			TakeActRequests(0);
			// THE PROMPT AFTER THE DEED offers talk only; nothing refreshed it
			// here, so "E  the window" stayed on screen over the broken glass
			// (the tester in the packaged game, 30 September).
			if (!bLiveScript) { LivePromptTick(false); }
			if (bLiveScript) { TakeTalkRequests(); }
			else { HumanTalkTick(World, Now); }
			// WHOEVER SEES HIM GO: the lad, by the same sight test, if the
			// man comes through the yard while it is still fresh. The scripted
			// story only (the review's A7): in free play the onlookers at the
			// deed are measured where they stand, and walking up to Darren
			// afterwards is not running from it.
			if (LedgerCrime::FleeSightingInPlay(bLiveScript) && !bFleeFiled && GN2Body != nullptr && GPawn != nullptr)
			{
				const LedgerCrime::Reading W = MeasureVantage(World, GIdN2, "flee", GN2Body, nullptr, 0.0);
				if (Perception::InSight(W.ActorMetres, W.ActorOffAxisDeg, LedgerCrime::kLightLevel, W.bActorOccluded, 1.4))
				{
					GFleeSeconds += Delta;
					if (GFleeSeconds >= Perception::NoticeSeconds) { FileFleeSighting(World); }
				}
			}
			const bool bMomentOver = bLiveScript ? Now - GLiveDeedAt >= 7.0
				: (Now - GLiveDeedAt >= LedgerCrime::kLiveLaterSeconds
				   || GNow.TotalMinutes() - GLiveDeedGameAt.TotalMinutes() >= (long long)(LedgerCrime::kLiveLaterSeconds * LiveClock::MinutesPerRealSecond));
			if (!bMomentOver) { return true; }
			// FREE PLAY GOES ON (Jafar's list of 30 September, item 1): once the
			// lad's moment to see him go has passed, nothing is staged. The town
			// talks hour by hour as the clock runs (TownHoursTick), whoever is
			// together passing it on by their routines; no one is moved by hand
			// and the week is not skipped. The scripted encounter below keeps its
			// staged evening for the build machine's regression.
			if (!bLiveScript)
			{
				SaveEncounterToDisk();
				WriteBreadcrumb(TEXT("live-later"));
				GPhase = ECrimePhase::LiveRoam;
				GPhaseStart = Now;
				return true;
			}
			// LATER: she walks round to the yard and tells the lad; he tells
			// his mate; the week moves on. What is said is on the screen.
			MoveBody(World, GW1Body, LedgerCrime::kW1BX, LedgerCrime::kW1BZ);
			FaceBody(GW1Body, ToStreet(GN2Body != nullptr ? GN2Body->GetActorLocation() : FVector::ZeroVector));
			RunGossipRound(2, GRound2);
			{
				std::string Id, Text, Clause, Speaker, Why;
				int Variants = 0;
				if (LedgerCrime::BankPick(GBankText, "overheard", GAchievedRung, LedgerCrime::Seed(GNow),
				                          Id, Text, Clause, Speaker, Variants, Why)) { GReplyText = Text; }
				GOverheard.Reply = LedgerCrime::ComposeOverheard(GCarried, GW1, GN2, LedgerCrime::Seed(GNow),
					GSummaryText == "none" ? std::string() : GSummaryText,
					GReplyText == "none" ? std::string() : GReplyText);
				if (!GOverheard.Reply.TellText.empty()) { Say(FString(TEXT("Sheila, in the yard: ")) + Un(GOverheard.Reply.TellText), 30.0f); }
				if (!GOverheard.Reply.ReplyText.empty()) { Say(FString(TEXT("Darren: ")) + Un(GOverheard.Reply.ReplyText), 30.0f); }
			}
			RespawnMate(World);
			GNow = GameTime(LedgerCrime::kRound3Day, LedgerCrime::kRound3Hour, 0);
			RunRound3(GRound3);
			GNow = GameTime(LedgerCrime::kRound3Day, LedgerCrime::kRound3Hour, 30);
			SaveEncounterToDisk();
			// EVENING, AND IT LOOKS IT (29 September; the AI tester found it
			// in daylight): the shared file's night, lamps lit.
			UE_LOG(LogTemp, Log, TEXT("LedgerCrime evening light: %s"),
			       *LedgerVignetteShot::ApplyPlayCondition(kEveningCondition));
			Say(TEXT("Later that week, evening. Darren, Sheila and Ron are in the yard across the road from Rita's pawn shop, through the gap between the houses. Press T near one of them to talk."), 40.0f, FColor::Yellow);
			WriteBreadcrumb(TEXT("live-later"));
			GPhase = ECrimePhase::LiveRoam;
			GPhaseStart = Now;
			return true;
		}
		case ECrimePhase::LiveRoam:
		{
			ClockTick(Delta);
			if (!bLiveScript) { WaitKeyTick(World); }
			if (!bLiveScript) { LivePromptTick(false); }
			LiveVoiceStart();
			LiveVoicePump();
			if (!bLiveScript)
			{
				HumanTalkTick(World, Now);
				TakeActRequests(0);
				return true;
			}
			if (bLiveScript)
			{
				if (GLiveStep < 3)
				{
					// BESIDE SAM, on the side away from Lena, who stands in the
					// yard with him now: T talks to whoever is nearest.
					TeleportPawn(World, LedgerCrime::kN2X + 1.3, LedgerCrime::kN2Z, 180.0);
					// AND THE CAMERA WITH HIM, toward the lad: the view is the
					// controller's, and a scripted step turns only the body.
					if (APlayerController* PC = World->GetFirstPlayerController()) { PC->SetControlRotation(FRotator(-8.0f, 180.0f, 0.0f)); }
					GLiveStep = 3; GLiveStepAt = Now;
					return true;
				}
				const bool bVoiceWanted = GVoice.bStarted && GVoice.OutRead != nullptr;
				const bool bVoiceWait = bVoiceWanted && !GVoice.bReady && Now - GLiveStepAt < 90.0;
				if (GLiveStep == 3 && Now - GLiveStepAt >= 1.0 && !bVoiceWait) { PressKey(World, EKeys::T); GLiveStep = 4; GLiveStepAt = Now; }
				const bool bSpeaking = bVoiceAsked && !(bVoicePlayed && bVoiceAllIn && GVoice.Queue.Num() == 0) && Now - GVoiceAskedAt < 60.0;
				if (bVoiceRecording && bVoiceAllIn && GVoice.Queue.Num() == 0 && Now >= GVoice.BusyUntil + 0.8)
				{
					UAudioMixerBlueprintLibrary::StopRecordingOutput(World, EAudioRecordingExportType::WavFile,
						TEXT("ue-encounter-live-voice"), FPaths::ConvertRelativePathToFull(FPaths::ProjectDir()));
					bVoiceRecording = false;
				}
				if (GLiveStep == 5 && Now - GLiveStepAt >= 2.0 && !bSpeaking && !bVoiceRecording) { Finish(); return false; }
			}
			TakeActRequests(0);
			if (TakeTalkRequests() <= 0 || GPawn == nullptr) { return true; }
			struct Who { AActor* Body; GossiperPtr G; const char* Card; const char* Id; const TCHAR* Name; int Rung; };
			const Who People[3] = {
				{ GN2Body, GN2, "sam", GIdN2.c_str(), TEXT("Darren"), -1 },
				{ GW1Body, GW1, "lena", GIdW1.c_str(), TEXT("Sheila"), GW1RungA },
				{ GR3Body, GR3, "rocco", GIdR3.c_str(), TEXT("Ron"), -1 } };
			const Who* Near = nullptr;
			double Best = LedgerCrime::kLiveTalkM;
			for (const Who& P : People)
			{
				if (P.Body == nullptr || !P.G) { continue; }
				const double M = FVector::Dist2D(GPawn->GetActorLocation(), P.Body->GetActorLocation()) / 100.0;
				if (M <= Best) { Best = M; Near = &P; }
			}
			if (Near == nullptr)
			{
				Say(TEXT("Nobody near enough to talk to."), 4.0f);
				return true;
			}
			if (!bLiveScript)
			{
				if (GLive.PendingId != 0) { Say(TEXT("Wait for an answer first."), 4.0f, FColor::White); return true; }
				if (!GLive.bReady) { Say(TEXT("(The street's voices are still waking up. Try again in a moment.)"), 4.0f, FColor::White); return true; }
				GTalkTarget.G = Near->G; GTalkTarget.Card = Near->Card; GTalkTarget.Id = Near->Id;
				GTalkTarget.Rung = Near->Rung; GTalkTarget.Name = FString(Near->Name);
				OpenSayBox(World);
				return true;
			}
			GTalkWith = Near->G; GTalkWho = Near->Id; GTalkCardOverride = Near->Card; GTalkOwnRung = Near->Rung;
			Say(TEXT("You: Evening. Anything going on round here?"), 8.0f, FColor::Cyan);
			RunTalk();
			LiveVoiceSay(9001, Near->Card, GTalkReply, GVisualFor(Near->Body));
			Say(FString(Near->Name) + TEXT(": ") + Un(GTalkReply == "none" ? std::string("...") : GTalkReply), 20.0f, FColor::White);
			SaveEncounterToDisk();
			if (bLiveScript)
			{
				GLiveStep = 5; GLiveStepAt = Now;
				// A PICTURE OF THE TALK, words on the screen and all.
				FScreenshotRequest::RequestScreenshot(FPaths::ConvertRelativePathToFull(FPaths::ProjectDir()
					/ (bLoadedFromDisk ? TEXT("ue-encounter-live-talk-after-reload.png") : TEXT("ue-encounter-live-talk.png"))), true, false);
			}
			return true;
		}
		case ECrimePhase::Done:
		default:
			Finish();
			return false;
		}
	}
}

namespace LedgerCrimeProbe
{
	void Start()
	{
		// THE INSTRUMENT'S OWN SELFTEST, RUN ON THE MACHINE THAT RUNS THE
		// PROBE, not only in the container that wrote it. The accepting case
		// is the live decision path; a failure here is printed on the verdict
		// beside everything the run measured, so a decision layer that broke
		// between the container and Jafar's PC cannot pass quietly.
		GSelftest = LedgerCrime::Selftest();
		{
			FString Mode;
			if (FParse::Value(FCommandLine::Get(), TEXT("Encounter="), Mode))
			{
				GEnc = Mode == TEXT("play") ? EEncounter::Play
				     : Mode == TEXT("reload") ? EEncounter::Reload
				     : Mode == TEXT("unseen") ? EEncounter::Unseen
				     : Mode == TEXT("live") ? EEncounter::Live : EEncounter::None;
			}
			bLiveScript = FParse::Param(FCommandLine::Get(), TEXT("LiveScript"));
			bAskAfterDeed = FParse::Param(FCommandLine::Get(), TEXT("AskAfterDeed"));
		}

		if (GEnc == EEncounter::Live && !bLiveScript) { GIdW1 = "lena"; GIdN2 = "sam"; GIdR3 = "rocco"; }
		else { GIdW1 = "w1"; GIdN2 = "n2"; GIdR3 = LedgerCrime::kR3Id; }
		GGraph = std::make_shared<SocialGraph>();
		GGraph->Link(GIdW1, GIdN2, LedgerCrime::kTie);
		GMill = std::make_shared<GossipMill>(GGraph);
		// DISPLAY NAMES ARE ARCHETYPES, NOT CAST. Canon's cast baseline is
		// pending and a probe does not mint one; the heard memory line reads
		// "I heard from the shopkeeper that ...".
		GW1 = std::make_shared<Gossiper>(GIdW1, GEnc == EEncounter::Live ? "Sheila" : "the shopkeeper",
		                                 std::shared_ptr<MemoryStore>(),
		                                 std::shared_ptr<KnowledgeBase>(), "day");
		GN2 = std::make_shared<Gossiper>(GIdN2, GEnc == EEncounter::Live ? "Darren" : "the lad in the yard",
		                                 std::shared_ptr<MemoryStore>(),
		                                 std::shared_ptr<KnowledgeBase>(), "day");
		GMill->Add(GW1);
		GMill->Add(GN2);
		// THE LAD'S MATE: tied to him and to nobody else, at the street's own
		// tie, so the only way the crime can reach him is a second retelling.
		GGraph->Link(GIdN2, GIdR3, LedgerCrime::kR3Tie);
		GR3 = std::make_shared<Gossiper>(GIdR3, GEnc == EEncounter::Live ? std::string("Ron") : std::string(LedgerCrime::kR3Name),
		                                 std::shared_ptr<MemoryStore>(),
		                                 std::shared_ptr<KnowledgeBase>(), "day");
		GMill->Add(GR3);
		if (GEnc == EEncounter::Live) { LiveTiesFromCast(); }

		WriteBreadcrumb(TEXT("start-called"));
		GTicker = FTSTicker::GetCoreTicker().AddTicker(FTickerDelegate::CreateStatic(&Tick), 0.0f);
	}
}
