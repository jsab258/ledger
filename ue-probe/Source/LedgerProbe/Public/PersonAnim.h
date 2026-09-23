// HEADS THAT TURN, 23 September, for Jafar's presentable checklist: "people
// turn their head to look at you when you move near them... Use what Unreal
// provides rather than building our own."
//
// UNREAL'S OWN LOOK AT NODE, NOT OURS. Each person's animation runs through
// the engine's standard nodes in a native animation instance - their loop in
// a sequence player, then FAnimNode_LookAt on the head bone with its aim
// solver, clamp and easing - because this project makes no Blueprint assets
// and the engine lets a native instance supply its own node graph. What is
// ours is only the decision: when the player is within LookRangeCm and in
// front of the person, the look fades in; otherwise it fades out.
//
// The automation's shots never look (a head turned to the lens is not a
// street photograph, and a frame must repeat); the playable street does.
#pragma once

#include "CoreMinimal.h"
#include "Animation/AnimInstance.h"
#include "PersonAnim.generated.h"

class UAnimSequenceBase;

UCLASS(transient)
class ULedgerPersonAnim : public UAnimInstance
{
	GENERATED_BODY()

public:
	// The loop, where in it to start, how fast it plays (0 holds it), and
	// whether this person looks at the player. Finds the head bone and its
	// facing on the mesh; the caller reinitialises the instance after.
	void Setup(UAnimSequenceBase* InSequence, float InStartSeconds, float InPlayRate, bool bInLook);

	virtual void NativeUpdateAnimation(float DeltaSeconds) override;

	UPROPERTY(Transient)
	TObjectPtr<UAnimSequenceBase> Sequence;

	float StartSeconds = 0.0f;
	float PlayRate = 1.0f;
	bool bLook = false;

	// THE HEAD, found on the mesh: its bone, and which of its local axes point
	// forward and up in the reference pose.
	FName HeadBone;
	FVector HeadLookAxis = FVector(0.0, 1.0, 0.0);
	FVector HeadUpAxis = FVector(0.0, 0.0, 1.0);

	// WHAT THE NODE IS GIVEN each frame, on the game thread.
	float LookAlpha = 0.0f;
	FVector LookTarget = FVector::ZeroVector;
	// THE MOST THIS PERSON HAS LOOKED this run, for the verdict.
	float PeakAlpha = 0.0f;

	static constexpr float LookRangeCm = 500.0f;
	static constexpr float LookConeDeg = 100.0f;

protected:
	virtual FAnimInstanceProxy* CreateAnimInstanceProxy() override;
};
