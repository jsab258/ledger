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

	// HIS HEAD HELD UP WHILE HE SITS AND STANDS (30 October, his order D10; production/research/sit-and-turn/
	// SIT-BOW-2026-10-30.md, route (ii)): Epic's bench clips lean the trunk as a person does (53 degrees, inside the
	// study's 46 +-12) but fold the head to the chest. With HeadUpWeight above nil the copied pose's neck is turned back
	// until the head bends no further forward of the upper back (spine_05 to neck_01) than standing plus
	// HeadUpAllowDeg, half at neck_01 and half at neck_02; at nil the copy is untouched. Set from the game thread.
	float HeadUpWeight = 0.0f;
	float HeadUpAllowDeg = 15.0f;
	// AND HIS UPPER BACK (30 October, the first film with the neck held: the bow stayed, so it is mostly the back):
	// spine_01 to spine_03 against spine_03 to neck_01, at most standing plus BackUpAllowDeg, turned back at spine_03
	// and spine_04 before the neck is measured (the study: the thoracic spine extends as the trunk leans)
	float BackUpAllowDeg = 10.0f;
	// THE THIRD TRY, HIS FACE KEPT UP (30 October, his yes that morning; SIT-BOW-2026-10-30.md, "the head's own pitch",
	// design (a)): the fault is the face, which Epic's bench clips turn 75 degrees to the floor where people average
	// about 10. While the weight is above nil the head bone's face direction is turned up until it is no lower than
	// FaceFloorDeg below the horizontal: 40% at neck_01, 30% at neck_02, 30% at the head. With FaceFloorDeg above nil the
	// two holds above are measured only, not applied (both set aside after two tries).
	float FaceFloorDeg = 25.0f;
	// the face's pitch against the horizontal (degrees, negative looking down) as copied and as held
	float FacePitchCopied() const;
	float FacePitchHeld() const;
	// the last copied pose's neck and upper back: each bend past standing (degrees), as copied and as held; and the
	// trunk's lean from the vertical (the thighs' midpoint to neck_01) as copied
	float NeckBendCopied() const;
	float NeckBendHeld() const;
	float BackBendCopied() const;
	float BackBendHeld() const;
	float TrunkLean() const;

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
