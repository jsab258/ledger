// THE SLICE'S PLAYER, 23 September: Jafar's "a proper player character with a
// body and animation", on Unreal's standard framework rather than grown out of
// the probe's camera-on-a-capsule (ALedgerCharacter, which the walk and crime
// probes keep using). A Character with the engine's movement, a third-person
// camera on a spring arm (canon: third person only), and a body from
// production/assets/people/tom-player.glb - a stand-in until Tom's look is
// settled - that stands, walks and runs (LocomotionAnim.h).
//
// Played with -LedgerSlice (LedgerGameMode). W A S D to move, the mouse to
// look, Shift to run.
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "Engine/TimerHandle.h"
#include "SliceCharacter.generated.h"

class USpringArmComponent;
class UCameraComponent;
class UNavigationInvokerComponent;
class USoundBase;
class USoundAttenuation;

UCLASS()
class ALedgerSliceCharacter : public ACharacter
{
	GENERATED_BODY()

public:
	ALedgerSliceCharacter();

	virtual void BeginPlay() override;
	virtual void Tick(float DeltaSeconds) override;
	virtual void SetupPlayerInputComponent(UInputComponent* PlayerInputComponent) override;

	// The body's asset paths, one place, so the probe's load check reads the
	// same names the game does.
	static const TCHAR* MeshPath();
	static const TCHAR* ClipPath(int32 Index);   // 0 stand, 1 walk, 2 run

	static constexpr float WalkSpeedCm = 160.0f;
	static constexpr float RunSpeedCm = 420.0f;
	// How far the body is lowered at a full run (SliceCharacter.cpp Tick).
	static constexpr float RunDropCm = 21.0f;

	bool bBodyLoaded = false;
	int32 ClipsLoaded = 0;

	// THE STREET'S WALKABLE AREA, for the probe's verdict: whether the bounds
	// went in, and whether the engine built a mesh inside them.
	bool bNavBounds = false;
	bool bNavBuilt = false;

private:
	void MoveForward(float Value);
	void MoveBackward(float Value);
	void MoveRight(float Value);
	void MoveLeft(float Value);
	void LookYaw(float Value);
	void LookPitch(float Value);
	void RunPressed();
	void RunReleased();

	// THE ACT KEY, 24 September: E, the same key and the same count the old
	// test character carried, so the encounter's crime is the player's own
	// input on the character the slice ships with. RequestAct counts a press;
	// the crime module takes the count with ConsumeActRequests.
	void RequestAct();

	// T TALKS, 24 September: the live encounter's conversation with whoever
	// is near, counted like the act and consumed by the encounter.
	void RequestTalk();
	// ESC PAUSES, 29 September (the twenty a friend would notice, 19: Esc used
	// to quit at once, a whole session on one key): Esc pauses and resumes
	// the world, Q quits while paused; both keys work while it is paused. The
	// encounter holds its own clock still while the world is paused and says
	// so on screen; it saves as it goes.
	void RequestPause();
	void RequestQuit();
	// R REPORTS THE LAST REPLY and F1 SHOWS THE AI NOTICE AGAIN, 29 September
	// (the town session's handover 6c: the EU's AI Act wants the notice by the
	// first conversation, and players a way to report what a character said).
	void RequestReport();
	void RequestNotice();
	// Z WAITS, 30 September (Jafar's list, item 1; the town's card 6ci): counted
	// like T, consumed by the encounter, which passes the time.
	void RequestWait();
	// A CONTROLLER'S A, 1 October: whatever the prompt in front of him offers, use or talk.
	void RequestPadAct();
public:
	int32 ConsumePadActRequests();
	int32 ConsumeActRequests();
	int32 ConsumeTalkRequests();
	int32 ConsumeReportRequests();
	int32 ConsumeNoticeRequests();
	int32 ConsumeWaitRequests();

private:
	int32 ActRequests = 0;
	int32 TalkRequests = 0;
	int32 PadActRequests = 0;
	int32 ReportRequests = 0;
	int32 WaitRequests = 0;
	int32 NoticeRequests = 0;
	void MarkStreetWalkable();
	void CloseStreetEnds();
	void BuildStreetNavigation();

	FTimerHandle NavBuildTimer;

	// THE BODY STEPS OUT OF THE CAMERA'S WAY (the AI tester, 29 September:
	// with his back to a shopfront the camera arm shortened until his
	// tracksuit filled the screen): hidden from the camera while it is within
	// this distance of his body's upright line, shown again beyond it.
	static constexpr float HideWithinCm = 55.0f;
	bool bBodyHiddenForCamera = false;

	// FOOTSTEPS WHEN HIS FEET LAND, 30 September (the twenty a friend would
	// notice, 18: he walked the street in silence). A step sounds as the clip
	// carrying his feet (the walk, or the run once it is half blended in)
	// passes one of its own landings, measured once from tom-player.glb by
	// tools/ue/footfalls.py (whose self-test holds these numbers to the file).
	// The first version watched his feet's heights, and three reviewers heard
	// the run limp: it caught one foot earlier than the other, and kerbs moved
	// it further. Walking and running steps are recorded apart; never the same
	// one twice running.
	void StepTick(float DeltaSeconds);
	static constexpr float WalkFootfallS[2] = { 0.193f, 0.676f };   // left, right; the walk clip is 0.967 s
	static constexpr float RunFootfallS[2] = { 0.254f, 0.805f };    // left, right; the run clip is 1.1 s
	FName FootBone[2];
	float PrevClipT = -1.0f;
	bool bStepOnRun = false;
	int32 LastStepClip = -1;
	int32 LastStepFoot = -1;
	float StepClock = 0.0f;
	float LastStepAt = -1.0f;
	float StepWindowStart = 0.0f;
	float StepsRecordingUntil = -1.0f;
	static constexpr float StepWalkVolume = 0.3f;
	static constexpr float StepRunVolume = 0.4f;   // the running steps are recorded 3 dB up already

	// Walking steps and running steps, recorded apart (tools/ue/make_steps.py).
	UPROPERTY()
	TArray<TObjectPtr<USoundBase>> StepClips;
	UPROPERTY()
	TArray<TObjectPtr<USoundBase>> RunStepClips;

	UPROPERTY()
	TObjectPtr<USoundAttenuation> StepAttenuation;

	// TOM'S WALK BY MOTION MATCHING (MotionMatchAnim.h, 22 October), with -LedgerMotionMatch only: the
	// sample's mannequin, hidden beside him, whose pose is copied onto his body each frame; null
	// without the switch, or when the sample's databases or his retargeter are not in this build
	// (then his own clips play).
	UPROPERTY()
	TObjectPtr<USkeletalMeshComponent> MotionDriver;
	bool StartMotionMatching(USkeletalMeshComponent* M);
	int32 HeardFootfalls = 0;
	// TOM'S WALK BY EPIC'S METAHUMAN ROUTE (his order of 24 October), with -LedgerGaspMover only: the Game
	// Animation Sample's own character, unchanged and unseen, is the mover; he wears his MetaHuman body
	// (L1) in its VisualOverride slot, copied from its hidden mannequin by the sample's own
	// ABP_GenericRetarget and Epic's RTG_UEFN_to_Metahuman_nrw (the sample's way of dressing it, read from
	// its AC_VisualOverrideManager and BP_Kellan; production/research/sit-and-turn/metahuman-route-2026-10-24).
	// His own capsule rides on the mover's and hands it what the keys, the pad and the route ask.
	UPROPERTY()
	TObjectPtr<ACharacter> GaspMover;
	UPROPERTY()
	TObjectPtr<USkeletalMeshComponent> WornBody;
	UPROPERTY()
	TObjectPtr<UClass> WornAnimClass;
	bool StartGaspMover(USkeletalMeshComponent* M);
	void GaspTick();
	float GaspLastIn = 0.0f;
	// TOM SITS (his order of 25 October, item 2: "Tom sits down in the game as played"), on Epic's route:
	// E near a seat of production/specs/seats.json plays the sample's bench interaction on the mover, its
	// approach clip chosen by the side he comes from and started where its remaining walk matches his
	// distance, warped onto the seat (Motion Warping, target "SmartObject", as the sample does), then its
	// sitting loop until he moves, then its stand-up. -TomSitProof walks him through it once and reports.
	enum class ESitPhase : uint8 { None, Approaching, Entering, Seated, Leaving };
	ESitPhase SitPhase = ESitPhase::None;
	FTransform SitSlot;
	UPROPERTY()
	TObjectPtr<class UAnimMontage> SitMontage;
	float SitPhaseAt = 0.0f;
	float SitClock = 0.0f;
	bool bSitWantsUp = false;
	bool TryStartSit();
	// -TomSitEntryTest=<clip> (28 October, his order D10, the sitting method's step 3): he starts at the entry derived
	// from the clip's own measures (production/specs/seat-clips.json), the warp off, so where he lands checks the entry
	bool StartSitFromEntry(const FString& ClipName);
	// -TomSitRoomTest (28 October, the sitting method's step 4): every In clip from inside the room, its derived start
	// and the start envelope's four corners, the warp on; limbs sampled against the room each frame, the bench ignored
	void SitRoomTestTick(float DeltaSeconds);
	// THE CHOICE AND THE APPROACH (28 October, the sitting method's steps 5 and 6): E near a seat whose entries were
	// room-tested (seats.json "in_kept") takes the kept entry whose direction is nearest his heading, steers the mover
	// onto that clip's path, and starts it Kingdom Come II's way, at a moment of the clip with his planted foot, his
	// stance within 10 points and his place inside the tested envelope; with none by the entry, the old start
	bool TryStartSitApproach(int32 SeatIndex);
	void SitApproachTick(float DeltaSeconds);
	FVector SitFootAt(int32 Foot, bool bMover = false) const;
	bool bSitNoApproach = false;
	FVector SitPush = FVector::ZeroVector;
	// -TomSitApproachTest: he walks in toward each seat from three places in the room, presses E, and the line says
	// which entry was chosen, how far off his heading, whether a start was found or the fallback taken, and if he sat
	void SitApproachTestTick(float DeltaSeconds);
	void SitTick(float DeltaSeconds);
	void SitProofTick(float DeltaSeconds);
	// HIS STOPS CHOSEN KINGDOM COME II'S WAY (his answer of 26 October, the walk's third try; -TomStopChosen): when
	// the walk is let go, Epic's own forward stop for the foot that is planted is played whole as a montage, from
	// the moment in it where the same foot is in the same quarter of its stance and the clip's remaining walk lies
	// in Kingdom Come II's walk window (0.6 to 2.1 m), its root motion carrying the mover; a push ends it.
	UPROPERTY()
	TObjectPtr<class UAnimMontage> StopMontage;
	float ContactFor[2] = { 0.0f, 0.0f };   // how long each foot has been planted (its contact curve over a half)
	float StanceSeconds = 0.55f;            // a planted spell's usual length, learned as he walks
	void StopTick(float WasIn, float NowIn);
	bool TryStartStop();
	// One step's sound from foot F (0 left, 1 right); false when too soon after the last.
	bool SoundStep(int32 F, bool bRun, float Speed, const TCHAR* From, float T);

	// THE WALK'S MEASURE, -TomWalkProof (22 October; the walk proof's method, CrimeProbe.cpp): he
	// walks a set route of starts, stops, turns, a pivot and a run, and each planted foot's drift is
	// measured once his pose for the frame is final, the worst named for each kind of join.
	void WalkProofTick(float DeltaSeconds);
	void MeasureFeet();
	int32 ProofSeg = -1;
	float ProofClock = 0.0f, ProofSegAt = 0.0f, ProofYaw = 0.0f;
	// EACH BODY'S FEET, measured alike: 0 his own, 1 the sample's mannequin that drives him (so a
	// slide is put down to the motion matching or to the copying onto him).
	struct FFeetMeasure
	{
		FName Ball[2];
		float Rest[2] = { 0.0f, 0.0f };
		int32 RestN = 0;
		bool bDown[2] = { false, false };
		FVector Planted[2];
		float Slip[2] = { 0.0f, 0.0f };
		int32 Kind[2] = { 0, 0 };
		float Worst[6] = { 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f };   // stand, start, loop, stop, turn, run
		int32 Contacts[6] = { 0, 0, 0, 0, 0, 0 };
		// THE SAME, WITH PLANTED READ FROM THE MOVING ANIMATION'S OWN CONTACT MARKS (24 October, Epic's route:
		// the sample's clips carry contact_l and contact_r, under 1 while a foot is planted; the height
		// reading counted low swings and scuffs as planted). Reported beside the height reading, never instead.
		bool bCon[2] = { false, false };
		FVector ConPlanted[2];
		float ConSlip[2] = { 0.0f, 0.0f };
		int32 ConKind[2] = { 0, 0 };
		float ConWorst[6] = { 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f };
		int32 ConContacts[6] = { 0, 0, 0, 0, 0, 0 };
	};
	FFeetMeasure Soles[2];
	void MeasureBody(int32 B, USkeletalMeshComponent* Body, int32 Seg, float T, float Floor);
	int32 ProofFrames = 0;
	UPROPERTY()
	TObjectPtr<class ACameraActor> ShotCamera;
	float NextShotAt = 0.0f;
	FString ProofLines;

public:
	int32 Steps = 0;
	static constexpr int32 MaxStepClips = 8;
	static FString StepClipPath(bool bRun, int32 Index);

private:

	UPROPERTY(VisibleAnywhere)
	TObjectPtr<USpringArmComponent> Boom;

	UPROPERTY(VisibleAnywhere)
	TObjectPtr<UCameraComponent> Camera;

	// THE NAVIGATION MESH IS BUILT AROUND THE PLAYER (and, later, the
	// walkers): the street is made at run time, so its mesh is too.
	UPROPERTY(VisibleAnywhere)
	TObjectPtr<UNavigationInvokerComponent> NavInvoker;
};
