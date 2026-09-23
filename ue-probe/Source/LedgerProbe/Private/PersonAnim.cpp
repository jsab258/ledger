#include "PersonAnim.h"

#include "Animation/AnimInstanceProxy.h"
#include "Animation/AnimNode_SequencePlayer.h"
#include "Animation/AnimNodeSpaceConversions.h"
#include "Animation/AnimSequenceBase.h"
#include "AnimationRuntime.h"
#include "BoneControllers/AnimNode_LookAt.h"
#include "Camera/PlayerCameraManager.h"
#include "Components/SkeletalMeshComponent.h"
#include "Engine/SkeletalMesh.h"
#include "Engine/World.h"
#include "GameFramework/PlayerController.h"

namespace
{
	// THE ENGINE'S NODES, WIRED AS AN ANIMATION BLUEPRINT WOULD WIRE THEM:
	// the loop, into component space, the Look At on the head, back to local.
	// A native instance may supply its own root node (GetCustomRootNode); the
	// proxy then initialises, updates and evaluates it as it would a graph.
	struct FLedgerPersonProxy : public FAnimInstanceProxy
	{
		FAnimNode_SequencePlayer_Standalone Player;
		FAnimNode_ConvertLocalToComponentSpace ToComponent;
		FAnimNode_LookAt Look;
		FAnimNode_ConvertComponentToLocalSpace ToLocal;

		explicit FLedgerPersonProxy(UAnimInstance* Instance) : FAnimInstanceProxy(Instance) {}

		virtual void Initialize(UAnimInstance* InAnimInstance) override
		{
			const ULedgerPersonAnim* A = Cast<ULedgerPersonAnim>(InAnimInstance);
			const bool bLooks = A != nullptr && A->bLook && !A->HeadBone.IsNone();
			if (A != nullptr)
			{
				Player.SetSequence(A->Sequence);
				Player.SetLoopAnimation(true);
				Player.SetStartPosition(A->StartSeconds);
				Player.SetPlayRate(A->PlayRate);
				Look.BoneToModify.BoneName = A->HeadBone;
				Look.LookAt_Axis.Axis = A->HeadLookAxis;
				Look.LookAt_Axis.bInLocalSpace = true;
				Look.LookUp_Axis.Axis = A->HeadUpAxis;
				Look.LookUp_Axis.bInLocalSpace = true;
				Look.bUseLookUpAxis = true;
				// A HEAD TURNS ABOUT SIXTY DEGREES before the shoulders have to
				// follow; the engine's clamp holds it there.
				Look.LookAtClamp = 60.0f;
				Look.InterpolationTime = 0.35f;
				Look.InterpolationType = EInterpolationBlend::Sinusoidal;
				Look.InterpolationTriggerThreashold = 5.0f;
				Look.Alpha = 0.0f;
				Look.LookAtLocation = A->LookTarget;
			}
			ToComponent.LocalPose.SetLinkNode(&Player);
			Look.ComponentPose.SetLinkNode(&ToComponent);
			ToLocal.ComponentPose.SetLinkNode(bLooks ? static_cast<FAnimNode_Base*>(&Look)
			                                         : static_cast<FAnimNode_Base*>(&ToComponent));
			FAnimInstanceProxy::Initialize(InAnimInstance);
		}

		virtual FAnimNode_Base* GetCustomRootNode() override { return &ToLocal; }

		virtual void GetCustomNodes(TArray<FAnimNode_Base*>& OutNodes) override
		{
			OutNodes.Add(&Player);
			OutNodes.Add(&ToComponent);
			OutNodes.Add(&Look);
			OutNodes.Add(&ToLocal);
		}

		// THE GAME THREAD'S DECISION, copied in before the worker updates.
		virtual void PreUpdate(UAnimInstance* InAnimInstance, float DeltaSeconds) override
		{
			FAnimInstanceProxy::PreUpdate(InAnimInstance, DeltaSeconds);
			if (const ULedgerPersonAnim* A = Cast<ULedgerPersonAnim>(InAnimInstance))
			{
				Look.Alpha = A->LookAlpha;
				Look.LookAtLocation = A->LookTarget;
			}
		}
	};

	// THE HEAD BONE: the one named "...Head", not the "HeadTop_End" leaf a
	// Mixamo rig carries above it.
	int32 FindHeadBone(const FReferenceSkeleton& Ref)
	{
		int32 Found = INDEX_NONE;
		for (int32 I = 0; I < Ref.GetNum(); ++I)
		{
			const FString Name = Ref.GetBoneName(I).ToString();
			if (Name.EndsWith(TEXT("Head"), ESearchCase::IgnoreCase)) { return I; }
			if (Found == INDEX_NONE && Name.Contains(TEXT("head"), ESearchCase::IgnoreCase)
			    && !Name.Contains(TEXT("top"), ESearchCase::IgnoreCase)
			    && !Name.Contains(TEXT("end"), ESearchCase::IgnoreCase))
			{
				Found = I;
			}
		}
		return Found;
	}
}

FAnimInstanceProxy* ULedgerPersonAnim::CreateAnimInstanceProxy()
{
	return new FLedgerPersonProxy(this);
}

void ULedgerPersonAnim::Setup(UAnimSequenceBase* InSequence, float InStartSeconds, float InPlayRate, bool bInLook)
{
	Sequence = InSequence;
	StartSeconds = InStartSeconds;
	PlayRate = InPlayRate;
	bLook = bInLook;
	HeadBone = NAME_None;
	const USkeletalMeshComponent* C = GetSkelMeshComponent();
	const USkeletalMesh* Mesh = C != nullptr ? C->GetSkeletalMeshAsset() : nullptr;
	if (Mesh == nullptr) { return; }
	const FReferenceSkeleton& Ref = Mesh->GetRefSkeleton();
	const int32 Head = FindHeadBone(Ref);
	if (Head == INDEX_NONE) { return; }
	HeadBone = Ref.GetBoneName(Head);
	// WHICH WAY THE FACE POINTS, in the head bone's own axes: a person from
	// Blender faces +Y in component space (the spawner turns them by F-90),
	// so the bone's look axis is +Y, and its up axis +Z, carried into the
	// bone's frame at the reference pose.
	const FTransform HeadCs = FAnimationRuntime::GetComponentSpaceTransformRefPose(Ref, Head);
	HeadLookAxis = HeadCs.InverseTransformVectorNoScale(FVector(0.0, 1.0, 0.0)).GetSafeNormal();
	HeadUpAxis = HeadCs.InverseTransformVectorNoScale(FVector(0.0, 0.0, 1.0)).GetSafeNormal();
}

void ULedgerPersonAnim::NativeUpdateAnimation(float DeltaSeconds)
{
	Super::NativeUpdateAnimation(DeltaSeconds);
	if (!bLook || HeadBone.IsNone()) { LookAlpha = 0.0f; return; }
	const USkeletalMeshComponent* C = GetSkelMeshComponent();
	const UWorld* World = GetWorld();
	const APlayerController* PC = World != nullptr ? World->GetFirstPlayerController() : nullptr;
	float Want = 0.0f;
	if (C != nullptr && PC != nullptr && PC->PlayerCameraManager != nullptr)
	{
		const FVector Eye = PC->PlayerCameraManager->GetCameraLocation();
		const FVector At = C->GetComponentLocation() + FVector(0.0, 0.0, 160.0);
		const FVector Facing = C->GetComponentTransform().TransformVectorNoScale(FVector(0.0, 1.0, 0.0)).GetSafeNormal2D();
		const FVector To = Eye - At;
		const float Dist = (float)To.Size2D();
		const float Cos = (float)FVector::DotProduct(Facing, To.GetSafeNormal2D());
		// NEAR AND IN FRONT: a person does not turn to look at someone behind
		// them, and does not stare across the street.
		if (Dist < LookRangeCm && Dist > 30.0f && Cos > FMath::Cos(FMath::DegreesToRadians(LookConeDeg)))
		{
			Want = 1.0f;
			LookTarget = Eye;
		}
	}
	LookAlpha = FMath::FInterpTo(LookAlpha, Want, DeltaSeconds, 2.5f);
	PeakAlpha = FMath::Max(PeakAlpha, LookAlpha);
}
