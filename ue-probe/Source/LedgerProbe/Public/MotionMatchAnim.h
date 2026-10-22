// TOM'S WALK BY MOTION MATCHING, 22 October 2026 (his order of 21 October, item 7: "Tom's walk
// rebuilt on Epic's Game Animation Sample with motion matching; foot slide measured at the joins,
// at or under 3 cm").
//
// TWO ANIMATIONS:
//  * ABP_TomMotion runs on a hidden copy of the sample's own UEFN mannequin beside Tom: the engine's
//    Motion Matching node searching the sample's walk, run, idle and turn-in-place databases
//    (migrated into /Game/Characters/UEFN_Mannequin, the sample's own paths;
//    F:/LedgerTools/game-inputs/gasp), then the sample's Offset Root Bone (the body lags the capsule
//    and catches it up, so the feet follow the clip's own travel), its Foot Placement and Leg IK
//    (a planted foot is held where it landed), and its Pose History (which also builds the coming
//    path from the character's own movement), in the sample's own order. It is an animation
//    blueprint, the one kind of asset those nodes run in once the game is packaged (they read
//    their settings from the blueprint's class there; built in code alone they stop the game), and
//    it is made by script, never by hand: ULedgerMotionMatchTools::WireMotionMatchBlueprint, called
//    from tools/ue/make_tom_retarget.py. Its parent, ULedgerMotionMatchAnim, gives it the
//    databases and hears its feet.
//  * ULedgerRetargetAnim runs on Tom's own body: the engine's Retarget Pose From Mesh node copies the
//    mannequin's pose onto him through RTG_UEFN_to_TomPlayer (tools/ue/make_tom_retarget.py), the way
//    the sample itself dresses its other characters (that node reads nothing from a class, so it
//    runs from code).
// The sample's footstep notifies on the mannequin's clips are caught here (HandleNotify) and given to
// Tom's own recorded steps instead of the sample's trainers.
#pragma once

#include "CoreMinimal.h"
#include "Animation/AnimInstance.h"
#include "Kismet/BlueprintFunctionLibrary.h"
#include "MotionMatchAnim.generated.h"

class UPoseSearchDatabase;
class UIKRetargeter;
class UAnimBlueprint;

UCLASS(transient, Blueprintable)
class ULedgerMotionMatchAnim : public UAnimInstance
{
	GENERATED_BODY()

public:
	// THE SAMPLE'S SETS, in this order; the ones searched are chosen each update as the sample's own
	// chooser chooses them (NativeUpdateAnimation).
	enum ESet { WalkLoops, WalkStarts, WalkStops, WalkPivots, RunLoops, RunStarts, RunStops, RunPivots, Idles, TurnInPlace, SetCount };
	void Setup(const TArray<UPoseSearchDatabase*>& InDatabases);

	UPROPERTY(Transient)
	TArray<TObjectPtr<UPoseSearchDatabase>> Databases;

	// THE FEET THE SAMPLE'S CLIPS MARK (its foley notifies, Walk_L/R, Run_L/R): how many have fired,
	// and the last one's foot (0 left, 1 right) and kind (0 walk, 1 run), for Tom's step sounds.
	int32 Footfalls = 0;
	int32 LastFoot = 0;
	int32 LastKind = 0;
	// Whether the blueprint's Motion Matching node was found and given the databases, and what was chosen.
	bool bDatabasesGiven = false;
	FString Chosen;
	bool bWasMoving = false;
	bool bWasRun = false;

	virtual bool HandleNotify(const FAnimNotifyEvent& AnimNotifyEvent) override;
	virtual void NativeUpdateAnimation(float DeltaSeconds) override;

	// What the Motion Matching node is playing: the clip, its time, and whether the last search kept it.
	FString Describe() const;
};

UCLASS(transient)
class ULedgerRetargetAnim : public UAnimInstance
{
	GENERATED_BODY()

public:
	void Setup(USkeletalMeshComponent* InSource, UIKRetargeter* InRetargeter);

	UPROPERTY(Transient)
	TObjectPtr<USkeletalMeshComponent> Source;
	UPROPERTY(Transient)
	TObjectPtr<UIKRetargeter> Retargeter;

protected:
	virtual FAnimInstanceProxy* CreateAnimInstanceProxy() override;
};

UCLASS()
class ULedgerMotionMatchTools : public UBlueprintFunctionLibrary
{
	GENERATED_BODY()

public:
	// THE GRAPH, LAID OUT AND COMPILED (in the editor only): into a new animation blueprint made on
	// the mannequin's skeleton with ULedgerMotionMatchAnim as its parent, the sample's own main chain
	// and settings (the .cpp names the three changes): Motion Matching, the Offset Root Bone (left out
	// when bOffsetRoot is false), Foot Placement and Leg IK, the Pose History, the output. Returns one
	// line: wireStatus=OK or what failed.
	UFUNCTION(BlueprintCallable, Category = "Ledger")
	static FString WireMotionMatchBlueprint(UAnimBlueprint* Blueprint, bool bOffsetRoot);
};
