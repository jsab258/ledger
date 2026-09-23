#include "LocomotionAnim.h"

#include "Animation/AnimInstanceProxy.h"
#include "Animation/AnimNode_SequencePlayer.h"
#include "Animation/AnimSequenceBase.h"
#include "AnimNodes/AnimNode_TwoWayBlend.h"
#include "GameFramework/Pawn.h"

namespace
{
	// STAND, WALK AND RUN, blended as an Animation Blueprint would wire them:
	// (stand <-> walk) <-> run, each blend's alpha from the ground speed.
	struct FLedgerLocomotionProxy : public FAnimInstanceProxy
	{
		FAnimNode_SequencePlayer_Standalone Idle;
		FAnimNode_SequencePlayer_Standalone Walk;
		FAnimNode_SequencePlayer_Standalone Run;
		FAnimNode_TwoWayBlend StandWalk;
		FAnimNode_TwoWayBlend WalkRun;

		explicit FLedgerLocomotionProxy(UAnimInstance* Instance) : FAnimInstanceProxy(Instance) {}

		virtual void Initialize(UAnimInstance* InAnimInstance) override
		{
			if (const ULedgerLocomotionAnim* A = Cast<ULedgerLocomotionAnim>(InAnimInstance))
			{
				Idle.SetSequence(A->Idle);
				Walk.SetSequence(A->Walk);
				Run.SetSequence(A->Run);
			}
			Idle.SetLoopAnimation(true);
			Walk.SetLoopAnimation(true);
			Run.SetLoopAnimation(true);
			StandWalk.A.SetLinkNode(&Idle);
			StandWalk.B.SetLinkNode(&Walk);
			WalkRun.A.SetLinkNode(&StandWalk);
			WalkRun.B.SetLinkNode(&Run);
			FAnimInstanceProxy::Initialize(InAnimInstance);
		}

		virtual FAnimNode_Base* GetCustomRootNode() override { return &WalkRun; }

		virtual void GetCustomNodes(TArray<FAnimNode_Base*>& OutNodes) override
		{
			OutNodes.Add(&Idle);
			OutNodes.Add(&Walk);
			OutNodes.Add(&Run);
			OutNodes.Add(&StandWalk);
			OutNodes.Add(&WalkRun);
		}

		virtual void PreUpdate(UAnimInstance* InAnimInstance, float DeltaSeconds) override
		{
			FAnimInstanceProxy::PreUpdate(InAnimInstance, DeltaSeconds);
			if (const ULedgerLocomotionAnim* A = Cast<ULedgerLocomotionAnim>(InAnimInstance))
			{
				StandWalk.Alpha = A->ToWalk;
				WalkRun.Alpha = A->ToRun;
			}
		}
	};
}

FAnimInstanceProxy* ULedgerLocomotionAnim::CreateAnimInstanceProxy()
{
	return new FLedgerLocomotionProxy(this);
}

void ULedgerLocomotionAnim::Setup(UAnimSequenceBase* InIdle, UAnimSequenceBase* InWalk, UAnimSequenceBase* InRun,
                                  float InWalkSpeedCm, float InRunSpeedCm)
{
	Idle = InIdle;
	Walk = InWalk;
	Run = InRun;
	WalkSpeedCm = FMath::Max(1.0f, InWalkSpeedCm);
	RunSpeedCm = FMath::Max(WalkSpeedCm + 1.0f, InRunSpeedCm);
}

void ULedgerLocomotionAnim::NativeUpdateAnimation(float DeltaSeconds)
{
	Super::NativeUpdateAnimation(DeltaSeconds);
	const APawn* P = TryGetPawnOwner();
	GroundSpeedCm = P != nullptr ? (float)P->GetVelocity().Size2D() : 0.0f;
	ToWalk = FMath::Clamp(GroundSpeedCm / WalkSpeedCm, 0.0f, 1.0f);
	ToRun = FMath::Clamp((GroundSpeedCm - WalkSpeedCm) / (RunSpeedCm - WalkSpeedCm), 0.0f, 1.0f);
}
