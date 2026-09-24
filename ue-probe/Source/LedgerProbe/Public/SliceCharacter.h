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

UCLASS()
class ALedgerSliceCharacter : public ACharacter
{
	GENERATED_BODY()

public:
	ALedgerSliceCharacter();

	virtual void BeginPlay() override;
	virtual void SetupPlayerInputComponent(UInputComponent* PlayerInputComponent) override;

	// The body's asset paths, one place, so the probe's load check reads the
	// same names the game does.
	static const TCHAR* MeshPath();
	static const TCHAR* ClipPath(int32 Index);   // 0 stand, 1 walk, 2 run

	static constexpr float WalkSpeedCm = 160.0f;
	static constexpr float RunSpeedCm = 420.0f;

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
public:
	int32 ConsumeActRequests();
	int32 ConsumeTalkRequests();

private:
	int32 ActRequests = 0;
	int32 TalkRequests = 0;
	void MarkStreetWalkable();
	void BuildStreetNavigation();

	FTimerHandle NavBuildTimer;

	UPROPERTY(VisibleAnywhere)
	TObjectPtr<USpringArmComponent> Boom;

	UPROPERTY(VisibleAnywhere)
	TObjectPtr<UCameraComponent> Camera;

	// THE NAVIGATION MESH IS BUILT AROUND THE PLAYER (and, later, the
	// walkers): the street is made at run time, so its mesh is too.
	UPROPERTY(VisibleAnywhere)
	TObjectPtr<UNavigationInvokerComponent> NavInvoker;
};
