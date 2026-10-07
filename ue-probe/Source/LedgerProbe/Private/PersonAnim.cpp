#include "PersonAnim.h"

#include "Animation/AnimCurveTypes.h"
#include "Animation/AnimInstanceProxy.h"
#include "Animation/AnimMontage.h"
#include "AnimNodes/AnimNode_Slot.h"
#include "Animation/AnimationAsset.h"
#include "Animation/AnimNode_SequencePlayer.h"
#include "Animation/AnimNodeSpaceConversions.h"
#include "Animation/AnimSequenceBase.h"
#include "AnimationRuntime.h"
#include "AnimNodes/AnimNode_ModifyCurve.h"
#include "AnimNodes/AnimNode_TwoWayBlend.h"
#include "BoneControllers/AnimNode_LookAt.h"
#include "BoneControllers/AnimNode_TwoBoneIK.h"
#include "BoneControllers/AnimNode_ModifyBone.h"
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
		// THE WALK, blended over the idle by how much the person is moving.
		FAnimNode_SequencePlayer_Standalone WalkPlayer;
		FAnimNode_TwoWayBlend Moving;
		bool bHasWalk = false;
		// THE MOVE SLOT (PlayMove, PersonAnim.h): a montage played here takes the whole body over
		// the loop and the walk, its root motion kept for the caller.
		FAnimNode_Slot Slot;
		FAnimNode_ConvertLocalToComponentSpace ToComponent;
		FAnimNode_TwoBoneIK Feet[2];
		FAnimNode_ModifyBone Calm[ULedgerPersonAnim::CalmBones];
		FAnimNode_LookAt Look;
		FAnimNode_ConvertComponentToLocalSpace ToLocal;
		// THE MOUTH WHILE THEY SPEAK (SpeakTick, PersonAnim.h): the face rig's
		// own mouth controls, blended over the idle by how much of the voice
		// is being heard. On a body the curves meet nothing and do nothing.
		FAnimNode_ModifyCurve Mouth;
		// A LINE MADE IN ADVANCE, its own face's curves over all of it (SayMadeLine).
		FAnimNode_ModifyCurve Said;

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
				Look.InterpolationTime = 0.2f;
				Look.InterpolationType = EInterpolationBlend::Sinusoidal;
				Look.InterpolationTriggerThreashold = 5.0f;
				Look.Alpha = 0.0f;
				Look.LookAtLocation = A->LookTarget;
			}
			bHasWalk = A != nullptr && A->WalkSequence != nullptr;
			if (bHasWalk)
			{
				WalkPlayer.SetSequence(A->WalkSequence);
				WalkPlayer.SetLoopAnimation(true);
				Moving.A.SetLinkNode(&Player);
				Moving.B.SetLinkNode(&WalkPlayer);
				Moving.Alpha = 0.0f;
				Slot.Source.SetLinkNode(&Moving);
			}
			else
			{
				Slot.Source.SetLinkNode(&Player);
			}
			Slot.SlotName = ULedgerPersonAnim::MoveSlot;
			ToComponent.LocalPose.SetLinkNode(&Slot);
			// THE FEET HELD WHERE THEY STAND while the caller asks (PersonAnim.h, FootHold): the
			// MetaHuman's legs only; any other body (the Mixamo street people) is left unnamed, so
			// the nodes pass it through untouched.
			const USkeletalMeshComponent* C = A != nullptr ? A->GetSkelMeshComponent() : nullptr;
			const bool bLegs = C != nullptr && C->GetSkeletalMeshAsset() != nullptr
			                   && C->GetSkeletalMeshAsset()->GetRefSkeleton().FindBoneIndex(FName(TEXT("calf_l"))) != INDEX_NONE
			                   && C->GetSkeletalMeshAsset()->GetRefSkeleton().FindBoneIndex(FName(TEXT("foot_r"))) != INDEX_NONE;
			FAnimNode_Base* Into = &ToComponent;
			for (int32 I = 0; I < 2; ++I)
			{
				FAnimNode_TwoBoneIK& F = Feet[I];
				F.ComponentPose.SetLinkNode(Into);
				F.IKBone.BoneName = bLegs ? FName(I == 0 ? TEXT("foot_l") : TEXT("foot_r")) : NAME_None;
				F.EffectorLocationSpace = BCS_WorldSpace;
				F.JointTargetLocationSpace = BCS_BoneSpace;
				F.JointTarget = FBoneSocketTarget(bLegs ? FName(I == 0 ? TEXT("calf_l") : TEXT("calf_r")) : NAME_None);
				F.JointTargetLocation = FVector::ZeroVector;   // the knee where the clip has it
				F.bAllowStretching = false;
				F.Alpha = 0.0f;
				Into = &F;
			}
			// THE NECK AND HEAD HELD TOWARD REST against the idle's own turns,
			// then the look (PersonAnim.h).
			for (int32 I = 0; I < ULedgerPersonAnim::CalmBones; ++I)
			{
				FAnimNode_ModifyBone& M = Calm[I];
				M.ComponentPose.SetLinkNode(Into);
				M.BoneToModify.BoneName = (A != nullptr && bLooks) ? A->CalmBone[I] : NAME_None;
				M.RotationMode = BMM_Replace;
				M.RotationSpace = BCS_ParentBoneSpace;
				M.TranslationMode = BMM_Ignore;
				M.ScaleMode = BMM_Ignore;
				M.Rotation = A != nullptr ? A->CalmRest[I] : FRotator::ZeroRotator;
				M.Alpha = (A != nullptr && bLooks && !A->CalmBone[I].IsNone()) ? ULedgerPersonAnim::CalmAlpha : 0.0f;
				Into = &M;
			}
			Look.ComponentPose.SetLinkNode(Into);
			ToLocal.ComponentPose.SetLinkNode(bLooks ? static_cast<FAnimNode_Base*>(&Look)
			                                         : static_cast<FAnimNode_Base*>(&Feet[1]));
			Mouth.SourcePose.SetLinkNode(&ToLocal);
			Mouth.ApplyMode = EModifyCurveApplyMode::Blend;
			Mouth.Alpha = 0.0f;
			for (const TCHAR* Name : ULedgerPersonAnim::MouthCurves) { Mouth.CurveMap.Add(FName(Name), 0.0f); }
			// THE WHOLE MOUTH WHILE SPEAKING, 1 October (Jafar: "Sheila's face breaks when she
			// talks, her mouth twisting sideways"; production/research/talking-face-faults/NOTE.md,
			// fix A): our eleven controls were laid over the idle, whose own mouth controls, one-
			// sided ones among them, passed through and twisted the mouth when the jaw opened. Every
			// mouth, jaw, teeth and tongue control the idle drives is in the map too, at rest, so
			// while someone speaks the speech owns the whole mouth, as Epic's mouth-only cut does;
			// eyes, lids and brows stay the idle's.
			if (A != nullptr && A->Sequence != nullptr)
			{
				TArray<FName> Idle;
				ULedgerPersonAnim::MouthCurvesOf(A->Sequence, Idle);
				for (const FName& Name : Idle) { if (!Mouth.CurveMap.Contains(Name)) { Mouth.CurveMap.Add(Name, 0.0f); } }
			}
			Said.SourcePose.SetLinkNode(&Mouth);
			Said.ApplyMode = EModifyCurveApplyMode::Blend;
			Said.Alpha = 0.0f;
			FAnimInstanceProxy::Initialize(InAnimInstance);
		}

		virtual FAnimNode_Base* GetCustomRootNode() override { return &Said; }

		virtual void GetCustomNodes(TArray<FAnimNode_Base*>& OutNodes) override
		{
			OutNodes.Add(&Player);
			OutNodes.Add(&WalkPlayer);
			OutNodes.Add(&Moving);
			OutNodes.Add(&Slot);
			OutNodes.Add(&ToComponent);
			OutNodes.Add(&Feet[0]);
			OutNodes.Add(&Feet[1]);
			for (int32 I = 0; I < ULedgerPersonAnim::CalmBones; ++I) { OutNodes.Add(&Calm[I]); }
			OutNodes.Add(&Look);
			OutNodes.Add(&ToLocal);
			OutNodes.Add(&Mouth);
			OutNodes.Add(&Said);
		}

		// THE GAME THREAD'S DECISION, copied in before the worker updates.
		virtual void PreUpdate(UAnimInstance* InAnimInstance, float DeltaSeconds) override
		{
			FAnimInstanceProxy::PreUpdate(InAnimInstance, DeltaSeconds);
			if (const ULedgerPersonAnim* A = Cast<ULedgerPersonAnim>(InAnimInstance))
			{
				// A NEW LOOP, 7 October (sitting, item 1.2): the game may swap a person's loop, the
				// seated one for the standing idle, and the player takes it on its next update.
				if (A->Sequence != nullptr && Player.GetSequence() != A->Sequence) { Player.SetSequence(A->Sequence); }
				Look.Alpha = A->LookAlpha;
				Look.LookAtLocation = A->LookTarget;
				Mouth.Alpha = A->SpeakWeight;
				Said.Alpha = A->SaidWeight;
				Said.CurveMap = A->SaidCurves;
				if (bHasWalk) { Moving.Alpha = A->WalkWeight; }
				for (int32 I = 0; I < 2; ++I)
				{
					Feet[I].Alpha = A->FootHold[I];
					Feet[I].EffectorLocation = A->FootHoldAt[I];
				}
				for (int32 I = 0; I < ULedgerPersonAnim::MouthCurveCount; ++I)
				{
					if (float* V = Mouth.CurveMap.Find(FName(ULedgerPersonAnim::MouthCurves[I]))) { *V = A->MouthValues[I]; }
				}
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

const FName ULedgerPersonAnim::MoveSlot(TEXT("DefaultSlot"));

bool ULedgerPersonAnim::PlayMove(UAnimSequenceBase* Clip, float BlendIn, float BlendOut, float Rate)
{
	const USkeletalMeshComponent* Mesh = GetSkelMeshComponent();
	if (Clip == nullptr || Mesh == nullptr || Mesh->GetSkeletalMeshAsset() == nullptr
	    || Clip->GetSkeleton() != Mesh->GetSkeletalMeshAsset()->GetSkeleton())
	{
		return false;
	}
	// The travel out of the pose and kept: from montages only, which is all this slot plays.
	SetRootMotionMode(ERootMotionMode::RootMotionFromMontagesOnly);
	return PlaySlotAnimationAsDynamicMontage(Clip, MoveSlot, BlendIn, BlendOut, Rate, 1) != nullptr;
}

bool ULedgerPersonAnim::IsMoving() const
{
	return IsAnyMontagePlaying();
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
	// THE HEAD AND ITS TWO PARENTS (the neck), and their rest rotations.
	for (int32 I = 0, Bone = Head; I < CalmBones; ++I)
	{
		CalmBone[I] = Bone != INDEX_NONE ? Ref.GetBoneName(Bone) : NAME_None;
		CalmRest[I] = Bone != INDEX_NONE ? Ref.GetRefBonePose()[Bone].GetRotation().Rotator() : FRotator::ZeroRotator;
		Bone = Bone != INDEX_NONE ? Ref.GetParentIndex(Bone) : INDEX_NONE;
	}
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

void ULedgerPersonAnim::SayMadeLine(UAnimSequenceBase* InFace)
{
	SaidFace = InFace;
	SaidTime = 0.0f;
	bSaidEnding = false;
	SaidCurves.Reset();
}

void ULedgerPersonAnim::EndMadeLine()
{
	bSaidEnding = true;
}

void ULedgerPersonAnim::SaidTick(float DeltaSeconds)
{
	if (SaidFace == nullptr) { SaidWeight = 0.0f; return; }
	SaidTime += DeltaSeconds;
	const float Length = SaidFace->GetPlayLength();
	const bool bOver = bSaidEnding || SaidTime >= Length;
	// In over a tenth of a second, out over a quarter: a quick fade back to the
	// idle jolted Ron's face at the end of a line (the blind reviewer, 1 October).
	SaidWeight = FMath::Clamp(SaidWeight + (bOver ? -DeltaSeconds / 0.25f : DeltaSeconds / 0.1f), 0.0f, 1.0f);
	if (bOver && SaidWeight <= 0.0f)
	{
		SaidFace = nullptr;
		SaidCurves.Reset();
		return;
	}
	// The line's face at its time (held at its last frame while it fades).
	FBlendedCurve Curve;
	SaidFace->EvaluateCurveData(Curve, FAnimExtractContext((double)FMath::Min(SaidTime, Length)));
	SaidCurves.Reset();
	// THE MOUTH ONLY (jaw, lips, teeth, tongue): the eyes, lids and brows stay
	// the idle's, which blinks and moves. Laid over whole, the made face held
	// Darren's eyes and brows still for the line (the blind reviewer, 1 October);
	// Epic's own mouth-only mask makes the same cut.
	static TMap<FName, bool> MouthPart;
	Curve.ForEachElement([this](const UE::Anim::FCurveElement& E)
	{
		bool* Known = MouthPart.Find(E.Name);
		if (Known == nullptr)
		{
			const FString N = E.Name.ToString();
			Known = &MouthPart.Add(E.Name, N.Contains(TEXT("_jaw")) || N.Contains(TEXT("_mouth")) || N.Contains(TEXT("_teeth")) || N.Contains(TEXT("_tongue")));
		}
		if (*Known) { SaidCurves.Add(E.Name, E.Value); }
	});
	// AND WHAT THE MADE FACE DOES NOT CARRY of the idle's mouth goes to rest too (fix A).
	if (IdleMouth.Num() == 0 && Sequence != nullptr) { MouthCurvesOf(Sequence, IdleMouth); }
	for (const FName& Name : IdleMouth) { if (!SaidCurves.Contains(Name)) { SaidCurves.Add(Name, 0.0f); } }
}

void ULedgerPersonAnim::MouthCurvesOf(UAnimSequenceBase* Seq, TArray<FName>& Out)
{
	Out.Reset();
	if (Seq == nullptr) { return; }
	// Evaluating curves takes scratch memory from the thread's stack allocator, which an
	// animation update marks for itself; called from setup it needs its own mark.
	FMemMark Mark(FMemStack::Get());
	FBlendedCurve Curve;
	Seq->EvaluateCurveData(Curve, FAnimExtractContext(0.0));
	Curve.ForEachElement([&Out](const UE::Anim::FCurveElement& E)
	{
		const FString N = E.Name.ToString();
		if (N.Contains(TEXT("_jaw")) || N.Contains(TEXT("_mouth")) || N.Contains(TEXT("_teeth")) || N.Contains(TEXT("_tongue"))) { Out.Add(E.Name); }
	});
}

void ULedgerPersonAnim::NativeUpdateAnimation(float DeltaSeconds)
{
	Super::NativeUpdateAnimation(DeltaSeconds);
	SaidTick(DeltaSeconds);
	// THE WALK (SetupWalk): the owner paces A to B and back; the idle and the
	// walk blend by how much it is moving, and it sets off and stops over
	// about half a second rather than sliding at full speed.
	if (WalkSequence != nullptr && DeltaSeconds > 0.0f)
	{
		AActor* Owner = GetOwningActor();
		bool bGoing = false;
		// THE MINUTE AFTER (GoAndLook): off to the spot, a stand looking, then back.
		bool bGatherStep = false;
		if (Owner != nullptr && GatherPhase >= 0)
		{
			if (GatherPhase == 0) { GatherLeft -= DeltaSeconds; if (GatherLeft <= 0.0f) { GatherPhase = 1; } }
			else if (GatherPhase == 2)
			{
				GatherLeft -= DeltaSeconds;
				const FVector Face = GatherLook - Owner->GetActorLocation();
				FRotator R = Owner->GetActorRotation();
				R.Yaw = FMath::FixedTurn(R.Yaw, FMath::RadiansToDegrees(FMath::Atan2(Face.Y, Face.X)) + WalkYawOffset, 120.0f * DeltaSeconds);
				Owner->SetActorRotation(R);
				if (GatherLeft <= 0.0f) { GatherPhase = 3; }
			}
			if (GatherPhase == 1 || GatherPhase == 3)
			{
				FVector At = Owner->GetActorLocation();
				FVector To = (GatherPhase == 1 ? GatherSpot : GatherFrom) - At;
				To.Z = 0.0f;
				const float Left = To.Size();
				if (Left < 5.0f)
				{
					if (GatherPhase == 1) { GatherPhase = 2; GatherLeft = GatherStay; }
					else { GatherPhase = -1; PauseLeft = FMath::FRandRange(PauseMin, PauseMax); }
				}
				else
				{
					const FVector Dir = To / Left;
					At += Dir * FMath::Min(Left, WalkSpeedCms * WalkWeight * DeltaSeconds);
					Owner->SetActorLocation(At);
					bGoing = true;
					FRotator R = Owner->GetActorRotation();
					R.Yaw = FMath::FixedTurn(R.Yaw, FMath::RadiansToDegrees(FMath::Atan2(Dir.Y, Dir.X)) + WalkYawOffset, 180.0f * DeltaSeconds);
					Owner->SetActorRotation(R);
				}
			}
			bGatherStep = true;
		}
		if (Owner != nullptr && !bGatherStep)
		{
			if (PauseLeft > 0.0f) { PauseLeft -= DeltaSeconds; }
			else
			{
				FVector At = Owner->GetActorLocation();
				FVector To = (bToB ? WalkB : WalkA) - At;
				To.Z = 0.0f;
				const float Left = To.Size();
				if (Left < 5.0f)
				{
					bToB = !bToB;
					++WalkLegs;
					PauseLeft = FMath::FRandRange(PauseMin, PauseMax);
				}
				else
				{
					const FVector Dir = To / Left;
					// HE WAITS FOR THE PLAYER rather than walking through him.
					bool bBlocked = false;
					const UWorld* W = GetWorld();
					const APlayerController* WPC = W != nullptr ? W->GetFirstPlayerController() : nullptr;
					if (WPC != nullptr && WPC->GetPawn() != nullptr)
					{
						const FVector Rel = WPC->GetPawn()->GetActorLocation() - At;
						bBlocked = Rel.Size2D() < 130.0f && FVector::DotProduct(Rel.GetSafeNormal2D(), Dir) > 0.5f;
					}
					if (!bBlocked)
					{
						At += Dir * FMath::Min(Left, WalkSpeedCms * WalkWeight * DeltaSeconds);
						Owner->SetActorLocation(At);
						bGoing = true;
					}
					FRotator R = Owner->GetActorRotation();
					R.Yaw = FMath::FixedTurn(R.Yaw, FMath::RadiansToDegrees(FMath::Atan2(Dir.Y, Dir.X)) + WalkYawOffset, 180.0f * DeltaSeconds);
					Owner->SetActorRotation(R);
				}
			}
		}
		WalkWeight = FMath::FInterpConstantTo(WalkWeight, bGoing ? 1.0f : 0.0f, DeltaSeconds, 2.0f);
	}
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
		Him = PC->GetPawn()->GetPawnViewLocation();   // his eyes, not his middle
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
				Strength = bHolds ? 1.0f : GlanceStrength;
			}
			// THE SECOND, KNOWING LOOK, once the first is over, in the passing zone.
			else if (bFirstGiven && LookLeft <= 0.0f && !bSecondGiven && SecondLookCm > 0.0f
			         && bInFront && Dist <= SecondLookCm)
			{
				bSecondGiven = true;
				++SecondLooks;
				LookLeft = SecondLookSeconds;
				Strength = 1.0f;
			}
			if (LookLeft > 0.0f) { Want = 1.0f; LookLeft -= DeltaSeconds; }
			// A LOOK THAT HOLDS while he is within its reach.
			if (bHolds && bFirstGiven && bInFront && Dist <= FirstLookCm) { Want = 1.0f; }
			// THE LOOK BACK after he has passed, for those who watch him.
			if (bLooksBack && bWasInFront && !bInFront && Dist <= FirstLookCm)
			{
				if (!bLookingBack) { bLookingBack = true; ++LooksBackGiven; }
				Want = 1.0f;
				Strength = 1.0f;
			}
			if (!bInFront && !bLooksBack) { Want = 0.0f; }
			// CLOSE, THEIR EYES GO ELSEWHERE, as a stranger's do.
			if (LookAwayCm > 0.0f && Dist <= LookAwayCm) { Want = 0.0f; LookLeft = 0.0f; }
		}
		if (Want > 0.0f)
		{
			// OVER THE SHOULDER ON HIS SIDE, never round the other way: a man
			// nearly straight behind her is aimed at no further round than
			// 95 degrees on the side he is, so the head turns to him as far as
			// a neck turns, not back past the front (the review: at 8 m behind
			// her the look back swung away from him).
			LookTarget = Him;
			const FVector Flat = FVector(To.X, To.Y, 0.0);
			const float Deg = FMath::RadiansToDegrees(FMath::Acos(FMath::Clamp(Cos, -1.0f, 1.0f)));
			if (Deg > 95.0f && Flat.Size() > 1.0)
			{
				const FVector Up(0.0, 0.0, 1.0);
				const float SideSign = FVector::DotProduct(FVector::CrossProduct(Facing, Flat), Up) >= 0.0 ? 1.0f : -1.0f;
				const FVector Aim = Facing.RotateAngleAxis(95.0f * SideSign, Up) * Flat.Size();
				LookTarget = At + Aim + FVector(0.0, 0.0, To.Z);
			}
			Want *= Strength;
		}
	}
	// EASED AT BOTH ENDS (the second review of the look clips: a turn that
	// began at full speed jumped, smeared and snapped back): the head follows a
	// driver that itself eases toward the look wanted. A full turn takes about
	// three quarters of a second and eases back in about a second and a half;
	// half a second of glance reaches four fifths of its turn.
	// THE NOISE, over whatever they were looking at (LookToward).
	if (NoiseLeft > 0.0f && C != nullptr)
	{
		if (NoiseDelay > 0.0f) { NoiseDelay -= DeltaSeconds; }
		else
		{
			if (NoiseLeft >= 0.0f && LookAlpha < 0.05f && Want == 0.0f) { ++NoiseLooks; }
			NoiseLeft -= DeltaSeconds;
			const FVector At = C->GetComponentLocation() + FVector(0.0, 0.0, 160.0);
			const FVector Facing = C->GetComponentTransform().TransformVectorNoScale(FVector(0.0, 1.0, 0.0)).GetSafeNormal2D();
			const FVector To = NoisePoint - At;
			const FVector Flat = FVector(To.X, To.Y, 0.0);
			const float Cos = (float)FVector::DotProduct(Facing, Flat.GetSafeNormal());
			const float Deg = FMath::RadiansToDegrees(FMath::Acos(FMath::Clamp(Cos, -1.0f, 1.0f)));
			LookTarget = NoisePoint;
			if (Deg > 95.0f && Flat.Size() > 1.0)
			{
				const FVector Up(0.0, 0.0, 1.0);
				const float SideSign = FVector::DotProduct(FVector::CrossProduct(Facing, Flat), Up) >= 0.0 ? 1.0f : -1.0f;
				LookTarget = At + Facing.RotateAngleAxis(95.0f * SideSign, Up) * Flat.Size() + FVector(0.0, 0.0, To.Z);
			}
			Want = 1.0f;
		}
	}
	const float Rate = Want > LookAlpha ? 6.0f : 3.0f;
	LookDrive = FMath::FInterpTo(LookDrive, Want, DeltaSeconds, Rate);
	LookAlpha = FMath::FInterpTo(LookAlpha, LookDrive, DeltaSeconds, Rate);
	PeakAlpha = FMath::Max(PeakAlpha, LookAlpha);
}

void ULedgerPersonAnim::LookToward(const FVector& Where, float DelaySeconds, float Seconds)
{
	NoisePoint = Where;
	NoiseDelay = FMath::Max(0.0f, DelaySeconds);
	NoiseLeft = FMath::Max(0.0f, Seconds);
}

void ULedgerPersonAnim::SpeakTick(float Level, bool bSpeaking, float DeltaSeconds)
{
	// OPEN QUICKLY, CLOSE A LITTLE SLOWER, as a jaw does: the loudness is
	// followed in about 30 ms rising and 80 ms falling, and the blend over
	// the idle eases in and out over a fifth of a second.
	const float Target = bSpeaking ? FMath::Clamp(Level, 0.0f, 1.0f) : 0.0f;
	const float Rate = Target > SpeakLevel ? 1.0f / 0.03f : 1.0f / 0.08f;
	SpeakLevel += (Target - SpeakLevel) * FMath::Min(1.0f, DeltaSeconds * Rate);
	SpeakWeight = FMath::FInterpConstantTo(SpeakWeight, bSpeaking ? 1.0f : 0.0f, DeltaSeconds, 5.0f);
	SpeakClock += DeltaSeconds;
	const float L = SpeakLevel;
	// THE SHAPES: the jaw with the loudness; the lips pressed together in the
	// quiet between sounds; a little funnel and stretch that drift against
	// each other so vowels do not all look alike (a jaw alone reads as a
	// puppet's). The research: production/research/lip-sync/NOTE-2026-09-30.md.
	const float Drift = 0.5f + 0.5f * FMath::Sin(SpeakClock * 7.3f) * FMath::Sin(SpeakClock * 3.1f + 1.0f);
	MouthValues[0] = 0.04f + 0.36f * L;                          // jawOpen
	const float Closed = FMath::Clamp(1.0f - L * 4.0f, 0.0f, 1.0f) * 0.6f;
	for (int32 I = 1; I <= 4; ++I) { MouthValues[I] = Closed; }  // lips together, four quarters
	for (int32 I = 5; I <= 8; ++I) { MouthValues[I] = 0.25f * L * Drift; }           // funnel, four quarters
	MouthValues[9] = MouthValues[10] = 0.18f * L * (1.0f - Drift);                    // stretch, left and right
}

void ULedgerPersonAnim::GoAndLook(const FVector& Spot, const FVector& LookAt, float Delay, float Stay)
{
	AActor* Owner = GetOwningActor();
	if (WalkSequence == nullptr || Owner == nullptr || GatherPhase >= 0) { return; }
	GatherSpot = FVector(Spot.X, Spot.Y, Owner->GetActorLocation().Z);
	GatherLook = LookAt;
	GatherFrom = Owner->GetActorLocation();
	GatherLeft = FMath::Max(0.0f, Delay);
	GatherStay = FMath::Max(1.0f, Stay);
	GatherPhase = 0;
}

void ULedgerPersonAnim::SetupWalk(UAnimSequenceBase* InWalk, const FVector& InA, const FVector& InB, float InSpeedCms,
                                  float InPauseMin, float InPauseMax, float InYawOffset)
{
	WalkSequence = InWalk;
	WalkA = InA;
	WalkB = InB;
	WalkSpeedCms = InSpeedCms;
	PauseMin = InPauseMin;
	PauseMax = FMath::Max(InPauseMin, InPauseMax);
	WalkYawOffset = InYawOffset;
	bToB = true;
	PauseLeft = FMath::FRandRange(0.0f, PauseMax);   // not all setting off at once
}
