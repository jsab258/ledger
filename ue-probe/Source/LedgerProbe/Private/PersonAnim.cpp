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
#include "GameFramework/Pawn.h"
#include "GameFramework/PlayerController.h"
#include "StreetVoice.h"

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
	// A STRANGER'S LOOK until the street says otherwise: RegardFor for
	// somebody who holds nothing about him.
	const LedgerCore::Gossiper Stranger("stranger", "stranger", std::shared_ptr<LedgerCore::MemoryStore>(),
	                                    std::shared_ptr<LedgerCore::KnowledgeBase>());
	const LedgerCore::StreetVoice::Regard R = LedgerCore::StreetVoice::RegardFor(&Stranger, 0.2, false, nullptr, 0.0, false);
	SetRegard(R.FirstLookMetres, R.FirstLookSeconds, R.SecondLookMetres, R.SecondLookSeconds, R.LookAwayMetres, R.bLooksBack);
}

void ULedgerPersonAnim::SetRegard(double InFirstLookMetres, double InFirstLookSeconds, double InSecondLookMetres,
                                  double InSecondLookSeconds, double InLookAwayMetres, bool bInLooksBack)
{
	FirstLookCm = (float)(InFirstLookMetres * 100.0);
	FirstLookSeconds = FMath::IsFinite(InFirstLookSeconds) ? (float)InFirstLookSeconds : TNumericLimits<float>::Max();
	SecondLookCm = (float)(InSecondLookMetres * 100.0);
	SecondLookSeconds = (float)InSecondLookSeconds;
	LookAwayCm = (float)(InLookAwayMetres * 100.0);
	bLooksBack = bInLooksBack;
}

void ULedgerPersonAnim::NativeUpdateAnimation(float DeltaSeconds)
{
	Super::NativeUpdateAnimation(DeltaSeconds);
	if (!bLook || HeadBone.IsNone()) { LookAlpha = 0.0f; return; }
	const USkeletalMeshComponent* C = GetSkelMeshComponent();
	const UWorld* World = GetWorld();
	const APlayerController* PC = World != nullptr ? World->GetFirstPlayerController() : nullptr;
	float Want = 0.0f;
	// HIS HEAD, not the camera behind him: a look at the lens is a look past him.
	FVector Him = FVector::ZeroVector;
	bool bHim = false;
	if (PC != nullptr && PC->GetPawn() != nullptr)
	{
		Him = PC->GetPawn()->GetActorLocation() + FVector(0.0, 0.0, 65.0);
		bHim = true;
	}
	else if (PC != nullptr && PC->PlayerCameraManager != nullptr)
	{
		Him = PC->PlayerCameraManager->GetCameraLocation();
		bHim = true;
	}
	if (C != nullptr && bHim)
	{
		const FVector At = C->GetComponentLocation() + FVector(0.0, 0.0, 160.0);
		const FVector Facing = C->GetComponentTransform().TransformVectorNoScale(FVector(0.0, 1.0, 0.0)).GetSafeNormal2D();
		const FVector To = Him - At;
		const float Dist = (float)To.Size2D();
		const float Cos = (float)FVector::DotProduct(Facing, To.GetSafeNormal2D());
		const bool bInFront = Cos > FMath::Cos(FMath::DegreesToRadians(LookConeDeg));
		const bool bHolds = FirstLookSeconds >= TNumericLimits<float>::Max();
		if (Dist > FMath::Max(FirstLookCm, SecondLookCm) + LookResetCm)
		{
			bFirstGiven = bSecondGiven = bWasInFront = bLookingBack = false;
			LookLeft = 0.0f;
		}
		if (Dist > 30.0f)
		{
			if (bInFront && Dist <= FirstLookCm) { bWasInFront = true; }
			// THE FIRST LOOK, as he comes within its distance in front of them.
			if (!bFirstGiven && bInFront && Dist <= FirstLookCm)
			{
				bFirstGiven = true;
				++FirstLooks;
				LookLeft = bHolds ? 0.0f : FirstLookSeconds;
			}
			// THE SECOND, KNOWING LOOK, once the first is over, in the passing zone.
			else if (bFirstGiven && LookLeft <= 0.0f && !bSecondGiven && SecondLookCm > 0.0f
			         && bInFront && Dist <= SecondLookCm)
			{
				bSecondGiven = true;
				++SecondLooks;
				LookLeft = SecondLookSeconds;
			}
			if (LookLeft > 0.0f) { Want = 1.0f; LookLeft -= DeltaSeconds; }
			// A LOOK THAT HOLDS while he is within its reach.
			if (bHolds && bFirstGiven && bInFront && Dist <= FirstLookCm) { Want = 1.0f; }
			// THE LOOK BACK after he has passed, for those who watch him.
			if (bLooksBack && bWasInFront && !bInFront && Dist <= FirstLookCm)
			{
				if (!bLookingBack) { bLookingBack = true; ++LooksBackGiven; }
				Want = 1.0f;
			}
			if (!bInFront && !bLooksBack) { Want = 0.0f; }
			// CLOSE, THEIR EYES GO ELSEWHERE, as a stranger's do.
			if (LookAwayCm > 0.0f && Dist <= LookAwayCm) { Want = 0.0f; LookLeft = 0.0f; }
		}
		if (Want > 0.0f) { LookTarget = Him; }
	}
	// A glance turns quickly and eases back: half a second must reach him.
	LookAlpha = FMath::FInterpTo(LookAlpha, Want, DeltaSeconds, Want > LookAlpha ? 6.0f : 3.0f);
	PeakAlpha = FMath::Max(PeakAlpha, LookAlpha);
}
