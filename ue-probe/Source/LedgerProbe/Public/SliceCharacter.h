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
public:
	int32 ConsumeActRequests();
	int32 ConsumeTalkRequests();
	int32 ConsumeReportRequests();
	int32 ConsumeNoticeRequests();

private:
	int32 ActRequests = 0;
	int32 TalkRequests = 0;
	int32 ReportRequests = 0;
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
	// notice, 18: he walked the street in silence). Each foot's lowest point
	// (ankle or ball) above the capsule's floor is watched; a step sounds
	// when a foot that was lifted comes down and stops, so the sound follows
	// whatever clip plays, at any speed. Six recorded steps on stone (Fantozzi, CC0; THIRD-PARTY.md),
	// never the same one twice running, a little louder running than walking.
	void StepTick(float DeltaSeconds);
	FName FootBone[2];
	FName ToeBone[2];
	float FootLow[2] = { 0.0f, 0.0f };
	float FootHigh[2] = { 0.0f, 0.0f };
	float FootPrev[2] = { 0.0f, 0.0f };
	// Each foot's heights over the last StepWindowS, as (time, height): its
	// range is theirs, so a jolt (pressed into someone, a kerb) is forgotten
	// once it leaves the window instead of skewing the range for seconds.
	TArray<FVector2f> FootSeen[2];
	static constexpr float StepWindowS = 1.2f;
	float TraceUntil = -1.0f;
	bool bTracedRun = false;
	bool bFootArmed[2] = { false, false };
	bool bFeetSeeded = false;
	int32 LastStepClip = -1;
	int32 LastStepFoot = -1;
	float StepClock = 0.0f;
	float LastStepAt = -1.0f;
	float StepWindowStart = 0.0f;
	float StepsRecordingUntil = -1.0f;
	static constexpr float StepWalkVolume = 0.3f;
	static constexpr float StepRunVolume = 0.5f;

	UPROPERTY()
	TArray<TObjectPtr<USoundBase>> StepClips;

	UPROPERTY()
	TObjectPtr<USoundAttenuation> StepAttenuation;

public:
	int32 Steps = 0;
	static constexpr int32 MaxStepClips = 8;
	static FString StepClipPath(int32 Index);

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
