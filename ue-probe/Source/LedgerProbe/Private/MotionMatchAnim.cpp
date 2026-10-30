#include "MotionMatchAnim.h"

#include "Animation/AnimBlueprint.h"
#include "Animation/AnimInstanceProxy.h"
#include "Animation/AnimNotifies/AnimNotify.h"
#include "Animation/AnimTypes.h"
#include "AnimNodes/AnimNode_RetargetPoseFromMesh.h"
#include "BonePose.h"
#include "Components/SkeletalMeshComponent.h"
#include "Misc/Paths.h"
#include "GameFramework/Character.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "PoseSearch/AnimNode_MotionMatching.h"
#include "PoseSearch/AnimNode_PoseSearchHistoryCollector.h"
#include "PoseSearch/PoseSearchHistory.h"
#include "PoseSearch/PoseSearchDatabase.h"
#include "PoseSearch/PoseSearchLibrary.h"
#include "Retargeter/IKRetargeter.h"
#if WITH_EDITOR
#include "EdGraph/EdGraph.h"
#include "EdGraph/EdGraphNode.h"
#include "EdGraph/EdGraphPin.h"
#include "EdGraphSchema_K2.h"
#include "Kismet2/CompilerResultsLog.h"
#include "Kismet2/KismetEditorUtilities.h"
#endif

namespace
{
	// THE COPY, AND HIS BACK AND HEAD HELD UP OVER IT (ULedgerRetargetAnim::HeadUpWeight): the engine's Retarget Pose
	// From Mesh node, then, while the weight is above nil, two holds in component space, each a bend between two
	// segments measured past the skeleton's own reference pose (standing) and turned back by as much of its excess
	// over its allowance as the weight asks, by halves at two joints, about the axis that takes the upper segment
	// toward the lower's line: first the upper back (spine_01 to spine_03 against spine_03 to neck_01, at spine_03 and
	// spine_04; the study's thoracic spine extends as the trunk leans), then the neck (spine_05 to neck_01 against
	// neck_01 to head, at neck_01 and neck_02). The hips and legs are left as the copy has them.
	struct FLedgerHold
	{
		FBoneReference A, B, C, P1, P2;
		float RefBend = 0.0f, Copied = 0.0f, Held = 0.0f;
	};

	struct FLedgerHeadUpNode : public FAnimNode_Base
	{
		FAnimNode_RetargetPoseFromMesh Retarget;
		float Weight = 0.0f, AllowDeg = 15.0f, BackAllowDeg = 10.0f;
		FLedgerHold Back = { FBoneReference(TEXT("spine_01")), FBoneReference(TEXT("spine_03")), FBoneReference(TEXT("neck_01")), FBoneReference(TEXT("spine_03")), FBoneReference(TEXT("spine_04")) };
		FLedgerHold Neck = { FBoneReference(TEXT("spine_05")), FBoneReference(TEXT("neck_01")), FBoneReference(TEXT("head")), FBoneReference(TEXT("neck_01")), FBoneReference(TEXT("neck_02")) };
		// the trunk's lean from the vertical (the thighs' midpoint to neck_01), on his copied pose
		FBoneReference ThighL = FBoneReference(TEXT("thigh_l")), ThighR = FBoneReference(TEXT("thigh_r"));
		float TrunkLean = 0.0f;
		bool bBones = false;

		virtual void Initialize_AnyThread(const FAnimationInitializeContext& Context) override { Retarget.Initialize_AnyThread(Context); }
		virtual void Update_AnyThread(const FAnimationUpdateContext& Context) override { Retarget.Update_AnyThread(Context); }
		virtual void CacheBones_AnyThread(const FAnimationCacheBonesContext& Context) override
		{
			Retarget.CacheBones_AnyThread(Context);
			const FBoneContainer& Bc = Context.AnimInstanceProxy->GetRequiredBones();
			bBones = ThighL.Initialize(Bc) && ThighR.Initialize(Bc);
			const FReferenceSkeleton& R = Bc.GetReferenceSkeleton();
			auto RefCS = [&R](int32 I)
			{
				FTransform T = R.GetRefBonePose()[I];
				for (int32 P = R.GetParentIndex(I); P != INDEX_NONE; P = R.GetParentIndex(P)) { T = T * R.GetRefBonePose()[P]; }
				return T.GetLocation();
			};
			for (FLedgerHold* H : { &Back, &Neck })
			{
				bBones = bBones && H->A.Initialize(Bc) && H->B.Initialize(Bc) && H->C.Initialize(Bc) && H->P1.Initialize(Bc) && H->P2.Initialize(Bc);
				if (!bBones) { return; }
				const FVector a = RefCS(H->A.BoneIndex), b = RefCS(H->B.BoneIndex), c = RefCS(H->C.BoneIndex);
				H->RefBend = FMath::RadiansToDegrees(FMath::Acos(FMath::Clamp(FVector::DotProduct((b - a).GetSafeNormal(), (c - b).GetSafeNormal()), -1.0, 1.0)));
			}
		}
		// the hold's bend past standing on this pose, and the axis that straightens it
		static float BendOf(FCSPose<FCompactPose>& CS, const FBoneContainer& Bc, const FLedgerHold& H, FVector& Axis)
		{
			const FVector a = CS.GetComponentSpaceTransform(H.A.GetCompactPoseIndex(Bc)).GetLocation();
			const FVector b = CS.GetComponentSpaceTransform(H.B.GetCompactPoseIndex(Bc)).GetLocation();
			const FVector c = CS.GetComponentSpaceTransform(H.C.GetCompactPoseIndex(Bc)).GetLocation();
			const FVector Lo = (b - a).GetSafeNormal(), Up = (c - b).GetSafeNormal();
			Axis = FVector::CrossProduct(Up, Lo).GetSafeNormal();
			return (float)FMath::RadiansToDegrees(FMath::Acos(FMath::Clamp(FVector::DotProduct(Lo, Up), -1.0, 1.0))) - H.RefBend;
		}
		void Apply(FPoseContext& Output, FCSPose<FCompactPose>& CS, FLedgerHold& H, float Allow)
		{
			const FBoneContainer& Bc = Output.Pose.GetBoneContainer();
			FVector Axis;
			H.Copied = H.Held = BendOf(CS, Bc, H, Axis);
			const float Turn = FMath::Max(0.0f, H.Copied - Allow) * FMath::Clamp(Weight, 0.0f, 1.0f);
			if (Turn <= 0.01f || Axis.IsNearlyZero()) { return; }
			// a turn of Q in component space at one bone: its local rotation becomes parent^-1 * Q * its own
			for (const FBoneReference* R : { &H.P1, &H.P2 })
			{
				const FCompactPoseBoneIndex I = R->GetCompactPoseIndex(Bc);
				const FQuat Q(Axis, FMath::DegreesToRadians(Turn * 0.5f));
				const FCompactPoseBoneIndex P = Output.Pose.GetParentBoneIndex(I);
				const FQuat Parent = P != INDEX_NONE ? CS.GetComponentSpaceTransform(P).GetRotation() : FQuat::Identity;
				const FQuat Now = CS.GetComponentSpaceTransform(I).GetRotation();
				Output.Pose[I].SetRotation((Parent.Inverse() * Q * Now).GetNormalized());
				CS.InitPose(Output.Pose);
			}
			H.Held = BendOf(CS, Bc, H, Axis);
		}
		virtual void Evaluate_AnyThread(FPoseContext& Output) override
		{
			Retarget.Evaluate_AnyThread(Output);
			if (!bBones) { return; }
			const FBoneContainer& Bc = Output.Pose.GetBoneContainer();
			FCSPose<FCompactPose> CS;
			CS.InitPose(Output.Pose);
			const FVector Hips = (CS.GetComponentSpaceTransform(ThighL.GetCompactPoseIndex(Bc)).GetLocation() + CS.GetComponentSpaceTransform(ThighR.GetCompactPoseIndex(Bc)).GetLocation()) * 0.5;
			const FVector Nk = CS.GetComponentSpaceTransform(Neck.B.GetCompactPoseIndex(Bc)).GetLocation();
			TrunkLean = (float)FMath::RadiansToDegrees(FMath::Acos(FMath::Clamp(FVector::DotProduct((Nk - Hips).GetSafeNormal(), FVector::UpVector), -1.0, 1.0)));
			Apply(Output, CS, Back, BackAllowDeg);
			Apply(Output, CS, Neck, AllowDeg);
		}
	};

	struct FLedgerRetargetProxy : public FAnimInstanceProxy
	{
		FLedgerHeadUpNode Node;

		explicit FLedgerRetargetProxy(UAnimInstance* Instance) : FAnimInstanceProxy(Instance) {}

		virtual void Initialize(UAnimInstance* InAnimInstance) override
		{
			if (const ULedgerRetargetAnim* A = Cast<ULedgerRetargetAnim>(InAnimInstance))
			{
				Node.Retarget.RetargetFrom = ERetargetSourceMode::CustomSkeletalMeshComponent;
				Node.Retarget.SourceMeshComponent = A->Source;
				Node.Retarget.IKRetargeterAsset = A->Retargeter;
			}
			FAnimInstanceProxy::Initialize(InAnimInstance);
		}

		virtual void PreUpdate(UAnimInstance* InAnimInstance, float DeltaSeconds) override
		{
			FAnimInstanceProxy::PreUpdate(InAnimInstance, DeltaSeconds);
			if (const ULedgerRetargetAnim* A = Cast<ULedgerRetargetAnim>(InAnimInstance)) { Node.Weight = A->HeadUpWeight; Node.AllowDeg = A->HeadUpAllowDeg; Node.BackAllowDeg = A->BackUpAllowDeg; }
		}

		virtual FAnimNode_Base* GetCustomRootNode() override { return &Node; }

		// BOTH NODES (30 October, the first film: his body stood in its reference pose): the engine's node reads the
		// mover's pose on the game thread in its own PreUpdate, which runs only for nodes listed here
		virtual void GetCustomNodes(TArray<FAnimNode_Base*>& OutNodes) override { OutNodes.Add(&Node); OutNodes.Add(&Node.Retarget); }
	};
}

void ULedgerMotionMatchAnim::Setup(const TArray<UPoseSearchDatabase*>& InDatabases)
{
	Databases.Reset();
	for (UPoseSearchDatabase* D : InDatabases) { Databases.Add(D); }
}

void ULedgerMotionMatchAnim::NativeUpdateAnimation(float DeltaSeconds)
{
	Super::NativeUpdateAnimation(DeltaSeconds);
	// EVERY UPDATE, as the sample's own graph does from its node's update function: which of its sets
	// are searched, given before the graph runs (this is the game thread, before the animation's own
	// work). THE SAMPLE'S OWN CHOOSER, CHT_PoseSearchDatabases_Sparse (exported and read, 22 October):
	// searched all at once, the turn-in-place set's built-in bonus (base cost -0.2) won every search
	// and he turned on the spot while walking (the first measured route).
	FAnimNode_MotionMatching* Node = nullptr;
	const UE::PoseSearch::FPoseHistory* History = nullptr;
	for (TFieldIterator<FStructProperty> It(GetClass()); It; ++It)
	{
		if (It->Struct->IsChildOf(FAnimNode_MotionMatching::StaticStruct())) { Node = It->ContainerPtrToValuePtr<FAnimNode_MotionMatching>(this); }
		else if (It->Struct->IsChildOf(FAnimNode_PoseSearchHistoryCollector_Base::StaticStruct()))
		{
			History = It->ContainerPtrToValuePtr<FAnimNode_PoseSearchHistoryCollector_Base>(this)->GetPoseHistoryPtr();
		}
	}
	const ACharacter* Body = Cast<ACharacter>(GetOwningActor());
	const UCharacterMovementComponent* Move = Body != nullptr ? Body->GetCharacterMovement() : nullptr;
	if (Node == nullptr || Move == nullptr || Databases.Num() < SetCount) { return; }
	const FVector V = Move->Velocity;
	const float Speed = V.Size2D();
	// THE SAMPLE'S "FUTURE VELOCITY": the path's travel between 0.4 and 0.5 seconds ahead.
	FVector Future = V;
	if (History != nullptr)
	{
		const TArray<FTransformTrajectorySample>& S = History->GetTrajectory().Samples;
		auto At = [&S](float T, FVector& Out) -> bool
		{
			for (int32 I = 1; I < S.Num(); ++I)
			{
				if (S[I - 1].TimeInSeconds <= T && T <= S[I].TimeInSeconds && S[I].TimeInSeconds > S[I - 1].TimeInSeconds)
				{
					Out = FMath::Lerp(S[I - 1].Position, S[I].Position, (T - S[I - 1].TimeInSeconds) / (S[I].TimeInSeconds - S[I - 1].TimeInSeconds));
					return true;
				}
			}
			return false;
		};
		FVector A, B;
		if (At(0.4f, A) && At(0.5f, B)) { Future = (B - A) * 10.0f; }
	}
	const float FutureSpeed = Future.Size2D();
	const UPoseSearchDatabase* Current = Node->GetMotionMatchingState().SearchResult.SelectedDatabase;
	const bool bInPivots = Current != nullptr && (Current == Databases[WalkPivots] || Current == Databases[RunPivots]);
	// THE SAMPLE'S OWN TESTS (its IsMoving, IsStarting, Get_TrajectoryTurnAngle and ShouldTurnInPlace,
	// exported and read 22 October): moving while he has speed and is being pushed; starting while
	// moving and the speed ahead is 1 m/s over his own, unless already pivoting; pivoting while moving
	// and pushed 45 degrees or more off his way; the run his gait when his top speed is nearer the
	// run's; a turn on the spot on the frame he stops, if his body (the offset root) is 50 degrees or
	// more off where he faces.
	const FVector Push = Move->GetCurrentAcceleration();
	const bool bMoving = !V.IsNearlyZero(0.1) && !Push.IsNearlyZero();
	const bool bRun = Move->MaxWalkSpeed > 290.0f;
	const bool bStarting = bMoving && FutureSpeed >= Speed + 100.0f && !bInPivots;
	const bool bPivoting = bMoving && FMath::Abs(FMath::FindDeltaAngleDegrees(V.Rotation().Yaw, Push.Rotation().Yaw)) >= 45.0f;
	const USkeletalMeshComponent* Mesh = GetSkelMeshComponent();
	const float RootYaw = Mesh != nullptr && Mesh->GetNumBones() > 0 ? Mesh->GetBoneTransform(0).Rotator().Yaw + 90.0f : Body->GetActorRotation().Yaw;
	const bool bTurnInPlace = !bMoving && bWasMoving && FMath::Abs(FMath::FindDeltaAngleDegrees(Body->GetActorRotation().Yaw, RootYaw)) >= 50.0f;
	TArray<UPoseSearchDatabase*, TInlineAllocator<8>> Dbs;
	if (!bMoving)
	{
		// "Stand Idles": the idles below 20 cm/s, the walk's stops from 20, the run's from 100, the turns.
		if (Speed < 20.0f && !bTurnInPlace) { Dbs.Add(Databases[Idles]); }
		if (Speed >= 20.0f) { Dbs.Add(Databases[WalkStops]); }
		if (Speed >= 100.0f) { Dbs.Add(Databases[RunStops]); }
		if (bTurnInPlace) { Dbs.Add(Databases[TurnInPlace]); }
		if (Dbs.Num() == 0) { Dbs.Add(Databases[Idles]); }
	}
	else
	{
		// "Stand Walks" and "Stand Runs": the starts while starting, the loops, the pivots while pivoting.
		const int32 Base = bRun ? RunLoops : WalkLoops;
		if (bStarting) { Dbs.Add(Databases[Base + 1]); }
		Dbs.Add(Databases[Base]);
		if (bPivoting) { Dbs.Add(Databases[Base + 3]); }
	}
	Dbs.RemoveAll([](const UPoseSearchDatabase* D) { return D == nullptr; });
	if (Dbs.Num() == 0) { return; }
	// THE SAMPLE'S INTERRUPT (its Get_MMInterruptMode): only on the frame he starts or stops moving, or
	// changes gait while moving, is the playing clip given up for the new sets; otherwise it plays on
	// (so a stop, chosen as he stops, plays out among the idles).
	const bool bChanged = bMoving != bWasMoving || (bMoving && bRun != bWasRun);
	Node->SetDatabasesToSearch(Dbs, bChanged ? EPoseSearchInterruptMode::InterruptOnDatabaseChange : EPoseSearchInterruptMode::DoNotInterrupt);
	bWasMoving = bMoving;
	bWasRun = bRun;
	bDatabasesGiven = true;
	const FPoseSearchBlueprintResult& R = Node->GetMotionMatchingState().SearchResult;
	Chosen = FString::Printf(TEXT("%s@%.2f%s cost %.2f rate %.2f; chose %s%s%s%s, ahead %.0f cm/s"),
		R.SelectedAnim != nullptr ? *R.SelectedAnim->GetName() : TEXT("none"), R.SelectedTime, R.bIsContinuingPoseSearch ? TEXT("(kept)") : TEXT(""),
		R.SearchCost, R.WantedPlayRate, bMoving ? (bRun ? TEXT("run") : TEXT("walk")) : TEXT("idle"),
		bStarting ? TEXT("+start") : TEXT(""), bPivoting ? TEXT("+pivot") : TEXT(""), bTurnInPlace ? TEXT("+turn") : TEXT(""), FutureSpeed);
}

FString ULedgerMotionMatchAnim::Describe() const
{
	// Written in NativeUpdateAnimation, before the animation's own work starts on another thread:
	// read here, at any time, the node's live state would race it (the engine's guard stopped the game).
	return Chosen;
}

bool ULedgerMotionMatchAnim::HandleNotify(const FAnimNotifyEvent& AnimNotifyEvent)
{
	// The sample's foley notifies are Blueprint classes named BP_AnimNotify_FoleyEvent_<Walk|Run>_<L|R>;
	// read by name, counted for Tom's own steps, and not played (they sound the sample's trainers).
	const UAnimNotify* N = AnimNotifyEvent.Notify;
	const FString Name = N != nullptr ? N->GetClass()->GetName() : AnimNotifyEvent.NotifyName.ToString();
	if (!Name.Contains(TEXT("FoleyEvent"))) { return false; }
	const bool bWalk = Name.Contains(TEXT("_Walk_"));
	const bool bRun = Name.Contains(TEXT("_Run_"));
	if (bWalk || bRun)
	{
		++Footfalls;
		LastFoot = Name.EndsWith(TEXT("_R_C")) || Name.EndsWith(TEXT("_R")) ? 1 : 0;
		LastKind = bRun ? 1 : 0;
	}
	return true;
}

FAnimInstanceProxy* ULedgerRetargetAnim::CreateAnimInstanceProxy()
{
	return new FLedgerRetargetProxy(this);
}

void ULedgerRetargetAnim::Setup(USkeletalMeshComponent* InSource, UIKRetargeter* InRetargeter)
{
	Source = InSource;
	Retargeter = InRetargeter;
}

float ULedgerRetargetAnim::NeckBendCopied() const { return GetProxyOnGameThread<FLedgerRetargetProxy>().Node.Neck.Copied; }
float ULedgerRetargetAnim::NeckBendHeld() const { return GetProxyOnGameThread<FLedgerRetargetProxy>().Node.Neck.Held; }
float ULedgerRetargetAnim::BackBendCopied() const { return GetProxyOnGameThread<FLedgerRetargetProxy>().Node.Back.Copied; }
float ULedgerRetargetAnim::BackBendHeld() const { return GetProxyOnGameThread<FLedgerRetargetProxy>().Node.Back.Held; }
float ULedgerRetargetAnim::TrunkLean() const { return GetProxyOnGameThread<FLedgerRetargetProxy>().Node.TrunkLean; }

FString ULedgerMotionMatchTools::WireMotionMatchBlueprint(UAnimBlueprint* Blueprint, bool bOffsetRoot)
{
#if WITH_EDITOR
	if (Blueprint == nullptr) { return TEXT("wireStatus=NO-BLUEPRINT"); }
	UEdGraph* Graph = nullptr;
	for (UEdGraph* G : Blueprint->FunctionGraphs)
	{
		if (G != nullptr && G->GetFName() == UEdGraphSchema_K2::GN_AnimGraph) { Graph = G; break; }
	}
	if (Graph == nullptr) { return TEXT("wireStatus=NO-ANIMGRAPH"); }
	UEdGraphNode* Output = nullptr;
	for (UEdGraphNode* N : Graph->Nodes)
	{
		if (N != nullptr && N->GetClass()->GetName() == TEXT("AnimGraphNode_Root")) { Output = N; }
	}
	if (Output == nullptr) { return TEXT("wireStatus=NO-OUTPUT-NODE"); }
	// THE SAMPLE'S OWN NODES AND SETTINGS (SandboxCharacter_CMC_ABP, exported as text and read on 22
	// October; F:/LedgerTools/scratch/gasp_abp.t3d): its main chain is Motion Matching, Offset Root
	// Bone, then into component space for Foot Placement and Leg IK, back, and the Pose History last,
	// before the output. Each node's settings are its own text from the sample, set on the node before
	// its pins are made (so the pins carry them), with three changes said where they are made.
	TArray<FString> Missed;
	auto Make = [Graph, &Missed](const TCHAR* ClassPath, int32 X, const TCHAR* NodeText) -> UEdGraphNode*
	{
		UClass* C = LoadObject<UClass>(nullptr, ClassPath);
		if (C == nullptr) { Missed.Add(FString(TEXT("class:")) + FPaths::GetExtension(ClassPath)); return nullptr; }
		UEdGraphNode* N = NewObject<UEdGraphNode>(Graph, C, NAME_None, RF_Transactional);
		Graph->AddNode(N, false, false);
		N->CreateNewGuid();
		if (NodeText != nullptr && NodeText[0] != 0)
		{
			FStructProperty* NodeProp = FindFProperty<FStructProperty>(N->GetClass(), TEXT("Node"));
			if (NodeProp == nullptr || NodeProp->ImportText_Direct(NodeText, NodeProp->ContainerPtrToValuePtr<void>(N), N, PPF_None) == nullptr)
			{
				Missed.Add(FString(TEXT("settings:")) + FPaths::GetExtension(ClassPath));
			}
		}
		N->PostPlacedNewNode();
		N->AllocateDefaultPins();
		N->NodePosX = X;
		N->NodePosY = 0;
		return N;
	};
	auto Link = [](UEdGraphNode* From, UEdGraphNode* To, const TCHAR* ToPin) -> bool
	{
		// (the local-to-component node names its output ComponentPose; every other node, Pose)
		UEdGraphPin* Out = From != nullptr ? From->FindPin(TEXT("Pose"), EGPD_Output) : nullptr;
		if (Out == nullptr && From != nullptr) { Out = From->FindPin(TEXT("ComponentPose"), EGPD_Output); }
		UEdGraphPin* In = To != nullptr ? To->FindPin(ToPin, EGPD_Input) : nullptr;
		if (Out == nullptr || In == nullptr) { return false; }
		Out->MakeLinkTo(In);
		return true;
	};
	// MOTION MATCHING: the sample's blend (0.5 s, its feet-first blend profile, Hermite), its notify
	// filter; THE FIRST CHANGE, the play rate 0.75 to 1.25 where the sample's is 0.85 to 1.15, Epic's own
	// wider clamp (note 1b), since Tom walks at 1.6 m/s and the sample's walk was recorded nearer 2.
	UEdGraphNode* Matching = Make(TEXT("/Script/PoseSearchEditor.AnimGraphNode_MotionMatching"), -1800,
		TEXT("(BlendTime=0.5,BlendProfile=\"/Script/Engine.BlendProfile'/Game/Characters/UEFN_Mannequin/Meshes/SK_UEFN_Mannequin.SK_UEFN_Mannequin:FastFeet+Root_Weight'\",")
		TEXT("BlendOption=HermiteCubic,PlayRate=(Min=0.75,Max=1.25),bShouldFilterNotifies=True,MaxBlendInTimeToOverrideAnimation=0.03,PlayerDepthBlendInTimeMultiplier=1.1)"));
	// OFFSET ROOT BONE: the sample's translation (eased back, half-life 0.2 s, never past 30 cm) and its
	// rotation held (Accumulate): the capsule turns at once and his body turns only as the clips turn
	// it; the search, measured from the held body, picks the turning clips. THE SECOND CHANGE: the
	// sample also steers each clip's own turning towards where he faces (Steering nodes inside the
	// blend), which this graph does not have. (Eased back instead, half-life 0.1 s, the first try,
	// the turning capsule swung his planted feet 40 to 100 cm at the turns.)
	UEdGraphNode* Offset = bOffsetRoot ? Make(TEXT("/Script/AnimationWarpingEditor.AnimGraphNode_OffsetRootBone"), -1500,
		TEXT("(TranslationMode=Interpolate,RotationMode=Accumulate,TranslationHalflife=0.2,RotationHalfLife=0.1,MaxTranslationError=30.0)")) : nullptr;
	UEdGraphNode* ToComponent = Make(TEXT("/Script/AnimGraph.AnimGraphNode_LocalToComponentSpace"), -1200, nullptr);
	// FOOT PLACEMENT: the sample's legs, pelvis, plant and interpolation settings; THE THIRD CHANGE, no
	// speed curve named, since the sample's contact curves reach it only through a curve-remapping node
	// this graph does not have (unremapped they would read backwards); it reads the feet's own speed.
	UEdGraphNode* Feet = Make(TEXT("/Script/AnimationWarpingEditor.AnimGraphNode_FootPlacement"), -900,
		TEXT("(IKFootRootBone=(BoneName=\"ik_foot_root\"),PelvisBone=(BoneName=\"pelvis\"),PelvisSettings=(MaxOffset=250.0,LinearStiffness=100.0),")
		TEXT("LegDefinitions=((FKFootBone=(BoneName=\"foot_r\"),IKFootBone=(BoneName=\"ik_foot_r\"),BallBone=(BoneName=\"ball_r\")),")
		TEXT("(FKFootBone=(BoneName=\"foot_l\"),IKFootBone=(BoneName=\"ik_foot_l\"),BallBone=(BoneName=\"ball_l\"))),")
		TEXT("PlantSettings=(SpeedThreshold=60.0,DistanceToGround=10.0,LockType=PivotAroundBall,UnplantRadius=35.0,ReplantRadiusRatio=0.35,UnplantAngle=45.0,")
		TEXT("ReplantAngleRatio=0.5,MaxExtensionRatio=0.5,MinExtensionRatio=0.2,SeparatingDistance=0.0,UnalignmentSpeedThreshold=200.0,AnkleTwistReduction=0.75),")
		TEXT("InterpolationSettings=(UnplantLinearStiffness=200.0,UnplantLinearDamping=1.0,UnplantAngularStiffness=179.0,UnplantAngularDamping=1.0,")
		TEXT("SeparationStiffness=1000.0,SeparationDamping=1.0,FloorLinearStiffness=1000.0,FloorLinearDamping=1.0,FloorAngularStiffness=450.0,FloorAngularDamping=1.0,")
		TEXT("bEnableFloorInterpolation=True,bSmoothRootBone=False,bEnableSeparationInterpolation=True),TraceSettings=(MaxGroundPenetration=20.0),AlphaBoolBlend=(BlendOption=Linear))"));
	UEdGraphNode* Legs = Make(TEXT("/Script/AnimGraph.AnimGraphNode_LegIK"), -600,
		TEXT("(SoftPercentLength=0.99,LegsDefinition=((IKFootBone=(BoneName=\"ik_foot_l\"),FKFootBone=(BoneName=\"foot_l\"),HingeRotationAxis=Z,bEnableRotationLimit=True),")
		TEXT("(IKFootBone=(BoneName=\"ik_foot_r\"),FKFootBone=(BoneName=\"foot_r\"),HingeRotationAxis=Z,bEnableRotationLimit=True)),AlphaBoolBlend=(BlendOption=Linear))"));
	UEdGraphNode* ToLocal = Make(TEXT("/Script/AnimGraph.AnimGraphNode_ComponentToLocalSpace"), -400, nullptr);
	// POSE HISTORY, last before the output as in the sample, with its collected bones; the coming path
	// made by the engine's own generator from his movement (the sample makes the same path in its own
	// function and feeds it in).
	UEdGraphNode* History = Make(TEXT("/Script/PoseSearchEditor.AnimGraphNode_PoseSearchHistoryCollector"), -200,
		TEXT("(bGenerateTrajectory=True,SamplingInterval=0.0,CollectedBones=((BoneName=\"foot_r\"),(BoneName=\"foot_l\"),(BoneName=\"thigh_r\"),")
		TEXT("(BoneName=\"thigh_l\"),(BoneName=\"spine_05\"),(BoneName=\"pelvis\")),RootBoneRecoveryTime=0.3)"));
	if (Matching == nullptr || ToComponent == nullptr || Feet == nullptr || Legs == nullptr || ToLocal == nullptr || History == nullptr || (bOffsetRoot && Offset == nullptr))
	{
		return FString::Printf(TEXT("wireStatus=NO-NODE-CLASS missed=%s"), *FString::Join(Missed, TEXT(",")));
	}
	auto Need = [&Missed](bool bOk, const TCHAR* What) { if (!bOk) { Missed.Add(What); } };
	UEdGraphNode* AfterMatching = Matching;
	if (Offset != nullptr) { Need(Link(Matching, Offset, TEXT("Source")), TEXT("link-offset")); AfterMatching = Offset; }
	Need(Link(AfterMatching, ToComponent, TEXT("LocalPose")), TEXT("link-component"));
	Need(Link(ToComponent, Feet, TEXT("ComponentPose")), TEXT("link-feet"));
	Need(Link(Feet, Legs, TEXT("ComponentPose")), TEXT("link-legs"));
	Need(Link(Legs, ToLocal, TEXT("ComponentPose")), TEXT("link-local"));
	Need(Link(ToLocal, History, TEXT("Source")), TEXT("link-history"));
	Need(Link(History, Output, TEXT("Result")), TEXT("link-output"));
	FCompilerResultsLog Results;
	FKismetEditorUtilities::CompileBlueprint(Blueprint, EBlueprintCompileOptions::None, &Results);
	const bool bCompiled = Blueprint->Status == BS_UpToDate || Blueprint->Status == BS_UpToDateWithWarnings;
	FString FirstError;
	for (const TSharedRef<FTokenizedMessage>& M : Results.Messages)
	{
		if (M->GetSeverity() == EMessageSeverity::Error) { FirstError = M->ToText().ToString().Left(160).Replace(TEXT(" "), TEXT("~")); break; }
	}
	return FString::Printf(TEXT("wireStatus=%s nodes=%d offsetRoot=%s compiled=%s errors=%d warnings=%d missed=%s%s%s"),
		bCompiled && Missed.Num() == 0 ? TEXT("OK") : TEXT("FAIL"), Graph->Nodes.Num(), bOffsetRoot ? TEXT("on") : TEXT("off"),
		bCompiled ? TEXT("yes") : TEXT("no"), Results.NumErrors, Results.NumWarnings,
		Missed.Num() > 0 ? *FString::Join(Missed, TEXT(",")) : TEXT("none"), FirstError.IsEmpty() ? TEXT("") : TEXT(" firstError="), *FirstError);
#else
	return TEXT("wireStatus=EDITOR-ONLY");
#endif
}
