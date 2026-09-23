// THE SLICE'S PLAYER STANDS, WALKS AND RUNS, 23 September: the first piece of
// the playable slice on Unreal's standard framework (Jafar: "a proper player
// character with a body and animation").
//
// UNREAL'S OWN NODES, as the heads that turn are (PersonAnim.h): three
// sequence players - stand, walk, run - blended by the engine's two-way blend
// nodes on the character's ground speed, in a native animation instance
// because this project makes no Blueprint assets.
#pragma once

#include "CoreMinimal.h"
#include "Animation/AnimInstance.h"
#include "LocomotionAnim.generated.h"

class UAnimSequenceBase;

UCLASS(transient)
class ULedgerLocomotionAnim : public UAnimInstance
{
	GENERATED_BODY()

public:
	// The three clips; the caller reinitialises the instance after.
	void Setup(UAnimSequenceBase* InIdle, UAnimSequenceBase* InWalk, UAnimSequenceBase* InRun,
	           float InWalkSpeedCm, float InRunSpeedCm);

	virtual void NativeUpdateAnimation(float DeltaSeconds) override;

	UPROPERTY(Transient)
	TObjectPtr<UAnimSequenceBase> Idle;
	UPROPERTY(Transient)
	TObjectPtr<UAnimSequenceBase> Walk;
	UPROPERTY(Transient)
	TObjectPtr<UAnimSequenceBase> Run;

	float WalkSpeedCm = 160.0f;
	float RunSpeedCm = 420.0f;

	// WHAT THE NODES ARE GIVEN each frame: how far from standing toward
	// walking, and from walking toward running, both 0 to 1.
	float ToWalk = 0.0f;
	float ToRun = 0.0f;
	float GroundSpeedCm = 0.0f;

protected:
	virtual FAnimInstanceProxy* CreateAnimInstanceProxy() override;
};
