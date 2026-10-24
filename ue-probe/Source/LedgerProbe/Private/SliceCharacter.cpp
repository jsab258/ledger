#include "SliceCharacter.h"
#include "LedgerPaper.h"
#include "LedgerSettings.h"
#include "HAL/PlatformMisc.h"
#include "HAL/IConsoleManager.h"
#include "Kismet/GameplayStatics.h"

#include "LocomotionAnim.h"
#include "MotionMatchAnim.h"
#include "PoseSearch/PoseSearchDatabase.h"
#include "Retargeter/IKRetargeter.h"
#include "Misc/FileHelper.h"

#include "Animation/AnimSequenceBase.h"
#include "Camera/CameraComponent.h"
#include "Components/CapsuleComponent.h"
#include "Components/InputComponent.h"
#include "Components/SkeletalMeshComponent.h"
#include "Engine/SkeletalMesh.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "GameFramework/SpringArmComponent.h"
#include "GameFramework/PlayerController.h"
#include "Camera/PlayerCameraManager.h"
#include "Camera/CameraActor.h"
#include "UnrealClient.h"
#include "InputCoreTypes.h"
#include "NavigationInvokerComponent.h"
#include "NavigationSystem.h"
#include "NavMesh/NavMeshBoundsVolume.h"
#include "Components/BrushComponent.h"
#include "Components/BoxComponent.h"
#include "Components/ChildActorComponent.h"
#include "PhysicsEngine/BodySetup.h"
#include "TimerManager.h"
#include "AudioMixerBlueprintLibrary.h"
#include "Misc/CommandLine.h"
#include "Misc/PackageName.h"
#include "Misc/Paths.h"
#include "Sound/SoundAttenuation.h"
#include "Sound/SoundBase.h"

const TCHAR* ALedgerSliceCharacter::MeshPath()
{
	return TEXT("/Game/Ledger/People/tom-player/SK_tom-player.SK_tom-player");
}

const TCHAR* ALedgerSliceCharacter::ClipPath(int32 Index)
{
	switch (Index)
	{
	case 1: return TEXT("/Game/Ledger/People/tom-player/A_tom-player__walk.A_tom-player__walk");
	case 2: return TEXT("/Game/Ledger/People/tom-player/A_tom-player__run.A_tom-player__run");
	default: return TEXT("/Game/Ledger/People/tom-player/A_tom-player.A_tom-player");
	}
}

ALedgerSliceCharacter::ALedgerSliceCharacter()
{
	GetCapsuleComponent()->InitCapsuleSize(34.0f, 88.0f);
	PrimaryActorTick.bCanEverTick = true;
	// THE BODY TURNS TO WHERE IT IS GOING and the camera is the player's,
	// as a third-person game does it.
	bUseControllerRotationYaw = false;
	bUseControllerRotationPitch = false;
	bUseControllerRotationRoll = false;
	UCharacterMovementComponent* Move = GetCharacterMovement();
	Move->bOrientRotationToMovement = true;
	Move->RotationRate = FRotator(0.0f, 540.0f, 0.0f);
	Move->MaxWalkSpeed = WalkSpeedCm;

	Boom = CreateDefaultSubobject<USpringArmComponent>(TEXT("Boom"));
	Boom->SetupAttachment(RootComponent);
	Boom->TargetArmLength = 320.0f;
	Boom->SocketOffset = FVector(0.0, 45.0, 55.0);
	Boom->bUsePawnControlRotation = true;

	Camera = CreateDefaultSubobject<UCameraComponent>(TEXT("Camera"));
	Camera->SetupAttachment(Boom, USpringArmComponent::SocketName);
	Camera->bUsePawnControlRotation = false;

	NavInvoker = CreateDefaultSubobject<UNavigationInvokerComponent>(TEXT("NavInvoker"));
	NavInvoker->SetGenerationRadii(3000.0f, 5000.0f);

	// A PERSON FROM BLENDER FACES +Y and stands on its origin: turned to the
	// character's +X and lowered to the capsule's foot.
	GetMesh()->SetRelativeLocationAndRotation(FVector(0.0, 0.0, -88.0), FRotator(0.0f, -90.0f, 0.0f));
}

void ALedgerSliceCharacter::Tick(float DeltaSeconds)
{
	Super::Tick(DeltaSeconds);
	WalkProofTick(DeltaSeconds);
	if (const APlayerController* KeysPC = Cast<APlayerController>(GetController()))
	{
		// A CONTROLLER, 1 October (the interface: the design's suggested lines are for a
		// controller first): the left stick walks, as the keys do; the right stick looks,
		// at a rate, with the player's sensitivity and inversion from the settings page.
		auto Stick = [KeysPC](const FKey& K) { const float V = KeysPC->GetInputAnalogKeyState(K); return FMath::Abs(V) < 0.25f ? 0.0f : V; };
		const float Fwd = FMath::Clamp((KeysPC->IsInputKeyDown(EKeys::W) ? 1.0f : 0.0f) - (KeysPC->IsInputKeyDown(EKeys::S) ? 1.0f : 0.0f) + Stick(EKeys::Gamepad_LeftY), -1.0f, 1.0f);
		const float Side = FMath::Clamp((KeysPC->IsInputKeyDown(EKeys::D) ? 1.0f : 0.0f) - (KeysPC->IsInputKeyDown(EKeys::A) ? 1.0f : 0.0f) + Stick(EKeys::Gamepad_LeftX), -1.0f, 1.0f);
		MoveForward(Fwd);
		MoveRight(Side);
		// Degrees a second at full tilt, through the same scale the mouse goes through (2.5 a unit).
		const float PadYaw = Stick(EKeys::Gamepad_RightX) * 150.0f * DeltaSeconds / 2.5f;
		const float PadPitch = Stick(EKeys::Gamepad_RightY) * 100.0f * DeltaSeconds / 2.5f;
		if (PadYaw != 0.0f) { LookYaw(PadYaw); }
		if (PadPitch != 0.0f) { LookPitch(-PadPitch); }
		// WHICH HE IS ON NOW, for the prompts and hints: the last thing moved or pressed.
		float MouseX = 0.0f, MouseY = 0.0f;
		KeysPC->GetInputMouseDelta(MouseX, MouseY);
		if (Stick(EKeys::Gamepad_LeftX) != 0.0f || Stick(EKeys::Gamepad_LeftY) != 0.0f || PadYaw != 0.0f || PadPitch != 0.0f
		    || KeysPC->IsInputKeyDown(EKeys::Gamepad_FaceButton_Bottom) || KeysPC->IsInputKeyDown(EKeys::Gamepad_Special_Right)) { LedgerPaper::SetPadInUse(true); }
		else if (KeysPC->IsInputKeyDown(EKeys::W) || KeysPC->IsInputKeyDown(EKeys::A) || KeysPC->IsInputKeyDown(EKeys::S) || KeysPC->IsInputKeyDown(EKeys::D)
		         || FMath::Abs(MouseX) + FMath::Abs(MouseY) > 0.5f) { LedgerPaper::SetPadInUse(false); }
	}
	GaspTick();
	if (MotionDriver != nullptr)
	{
		// the sample's braking: hard when let go, gentle while still pushed (its CalculateBrakingDeceleration)
		GetCharacterMovement()->BrakingDecelerationWalking = GetCharacterMovement()->GetCurrentAcceleration().IsNearlyZero() ? 2000.0f : 500.0f;
	}
	if (GetMesh() == nullptr) { return; }
	// HIS FEET ON THE GROUND WHEN HE RUNS, 30 September. The person export
	// keeps each clip in place by dropping the hips' travel, which for the
	// walk loses only a bob; but the run's hips sit lower than standing, so
	// held at standing height his feet never came within 36 cm of the
	// pavement (the toes' lowest in the run 24 cm, in the walk 3: measured
	// from tom-player.glb, and found by the footsteps missing their cue).
	// The body goes down by that difference as the run blends in.
	if (const ULedgerLocomotionAnim* Loco = Cast<ULedgerLocomotionAnim>(GetMesh()->GetAnimInstance()))
	{
		GetMesh()->SetRelativeLocation(FVector(0.0, 0.0, -88.0 - RunDropCm * Loco->ToRun));
	}
	// FROM WHERE THE PLAYER ACTUALLY SEES, to the nearest point of his body's
	// upright line (feet to head): the first version measured to his head
	// only, and a camera pressed to his chest stayed 70 cm from it.
	const APlayerController* PC = Cast<APlayerController>(GetController());
	const FVector View = PC != nullptr && PC->PlayerCameraManager != nullptr ? PC->PlayerCameraManager->GetCameraLocation()
	                   : (Camera != nullptr ? Camera->GetComponentLocation() : GetActorLocation());
	const FVector Feet = GetActorLocation() - FVector(0.0, 0.0, 88.0);
	const FVector Top = GetActorLocation() + FVector(0.0, 0.0, 88.0);
	const bool bClose = FVector::Dist(View, FMath::ClosestPointOnSegment(View, Feet, Top)) < HideWithinCm;
	if (bClose != bBodyHiddenForCamera)
	{
		bBodyHiddenForCamera = bClose;
		// the body he wears on Epic's route, else his own
		if (WornBody != nullptr && WornBody->GetOwner() != nullptr) { WornBody->GetOwner()->SetActorHiddenInGame(bClose); }
		else { GetMesh()->SetVisibility(!bClose, true); }
	}
	StepTick(DeltaSeconds);
}

FString ALedgerSliceCharacter::StepClipPath(bool bRun, int32 Index)
{
	const TCHAR* Kind = bRun ? TEXT("run") : TEXT("walk");
	return FString::Printf(TEXT("/Game/Ledger/Sounds/Steps/step-%s-%d.step-%s-%d"), Kind, Index, Kind, Index);
}

void ALedgerSliceCharacter::StepTick(float DeltaSeconds)
{
	USkeletalMeshComponent* M = GetMesh();
	const ULedgerLocomotionAnim* Loco = M != nullptr ? Cast<ULedgerLocomotionAnim>(M->GetAnimInstance()) : nullptr;
	const ULedgerMotionMatchAnim* Matched = MotionDriver != nullptr ? Cast<ULedgerMotionMatchAnim>(MotionDriver->GetAnimInstance()) : nullptr;
	if ((Loco == nullptr && Matched == nullptr) || StepClips.Num() == 0 || DeltaSeconds <= 0.0f) { return; }
	StepClock += DeltaSeconds;
	UWorld* World = GetWorld();
	if (StepsRecordingUntil > 0.0f && StepClock >= StepsRecordingUntil && World != nullptr)
	{
		UAudioMixerBlueprintLibrary::StopRecordingOutput(World, EAudioRecordingExportType::WavFile,
			TEXT("ue-steps"), FPaths::ConvertRelativePathToFull(FPaths::ProjectDir()));
		StepsRecordingUntil = -1.0f;
		UE_LOG(LogTemp, Log, TEXT("LedgerSteps: the steps' sound written to ue-steps.wav"));
	}
	const float Speed = GetVelocity().Size2D();
	if (Matched != nullptr)
	{
		// THE SAMPLE'S CLIPS MARK THE FEET (their foley notifies, caught in HandleNotify): one
		// step for each new mark, from the foot it names, while he is on the ground.
		const int32 New = Matched->Footfalls - HeardFootfalls;
		HeardFootfalls = Matched->Footfalls;
		if (New > 0 && Speed > 30.0f && !GetCharacterMovement()->IsFalling())
		{
			SoundStep(Matched->LastFoot, Matched->LastKind == 1, Speed, TEXT("matched"), -1.0f);
		}
		return;
	}
	float WalkT = 0.0f, RunT = 0.0f;
	if (!Loco->ClipTimes(WalkT, RunT)) { return; }
	const bool bMoving = Speed > 30.0f && Loco->ToWalk > 0.3f && !GetCharacterMovement()->IsFalling();
	// THE CLIP CARRYING HIS FEET: the run once it is half blended in, else the
	// walk. A change of clip, a stop or a fall starts the count again from
	// where the clip now is, so nothing sounds for a landing already past.
	const bool bRunClip = Loco->ToRun >= 0.5f;
	const float T = bRunClip ? RunT : WalkT;
	if (!bMoving || bRunClip != bStepOnRun || PrevClipT < 0.0f)
	{
		PrevClipT = bMoving ? T : -1.0f;
		bStepOnRun = bRunClip;
		return;
	}
	const float* Falls = bRunClip ? RunFootfallS : WalkFootfallS;
	const float From = PrevClipT;
	PrevClipT = T;
	for (int32 F = 0; F < 2; ++F)
	{
		// PASSED THIS FOOT'S LANDING since the last frame, the loop's seam
		// included (the clip wraps from its end to its start).
		const float C = Falls[F];
		const bool bPassed = From <= T ? (From < C && C <= T) : (C > From || C <= T);
		if (bPassed) { SoundStep(F, bRunClip, Speed, bRunClip ? TEXT("run") : TEXT("walk"), T); }
	}
}

bool ALedgerSliceCharacter::SoundStep(int32 F, bool bRunClip, float Speed, const TCHAR* From, float T)
{
	USkeletalMeshComponent* M = GetMesh();
	UWorld* World = GetWorld();
	if (M == nullptr) { return false; }
	{
		// NEVER TWO AT ONCE, and never one foot twice running within less
		// than its own stride (a change of clip right on a landing).
		if (LastStepAt >= 0.0f && StepClock - LastStepAt < 0.18f) { return false; }
		if (F == LastStepFoot && StepClock - LastStepAt < 0.6f) { return false; }
		LastStepFoot = F;
		const TArray<TObjectPtr<USoundBase>>& Set = bRunClip && RunStepClips.Num() > 0 ? RunStepClips : StepClips;
		int32 Pick = FMath::RandRange(0, Set.Num() - 1);
		if (Set.Num() > 1 && Pick == LastStepClip) { Pick = (Pick + 1 + FMath::RandRange(0, Set.Num() - 2)) % Set.Num(); }
		LastStepClip = Pick;
		const float ToRun = FMath::Clamp((Speed - WalkSpeedCm) / (RunSpeedCm - WalkSpeedCm), 0.0f, 1.0f);
		const float Volume = FMath::Lerp(StepWalkVolume, StepRunVolume, ToRun) * FMath::FRandRange(0.85f, 1.0f);
		const FVector Where = FootBone[F].IsNone() ? GetActorLocation() - FVector(0.0, 0.0, 85.0) : M->GetBoneLocation(FootBone[F]);
		UGameplayStatics::PlaySoundAtLocation(this, Set[Pick], Where, FRotator::ZeroRotator,
			Volume, FMath::FRandRange(0.93f, 1.05f), 0.0f, StepAttenuation);
		++Steps;
		if (Steps <= 8 || StepsRecordingUntil > 0.0f)
		{
			UE_LOG(LogTemp, Log, TEXT("LedgerSteps: step %d, %s foot, %.0f cm/s, %.2f s after the last, the %s at %.3f s"),
				Steps, F == 0 ? TEXT("left") : TEXT("right"), Speed, LastStepAt < 0.0f ? 0.0f : StepClock - LastStepAt,
				From, T);
		}
		if (Steps % 20 == 0)
		{
			UE_LOG(LogTemp, Log, TEXT("LedgerSteps: %d steps; the last 20 at %.0f a minute, %.0f cm/s"),
				Steps, 20.0f * 60.0f / FMath::Max(0.01f, StepClock - StepWindowStart), Speed);
			StepWindowStart = StepClock;
		}
		if (Steps == 1)
		{
			StepWindowStart = StepClock;
			// -LedgerStepsRecord KEEPS FIFTEEN SECONDS OF WHAT HE HEARS from
			// the first step, so the steps' level beside a voice is measured,
			// not guessed.
			if (FParse::Param(FCommandLine::Get(), TEXT("LedgerStepsRecord")) && World != nullptr && World->GetAudioDevice().IsValid())
			{
				UAudioMixerBlueprintLibrary::StartRecordingOutput(World, 20.0f);
				StepsRecordingUntil = StepClock + 15.0f;
			}
		}
		LastStepAt = StepClock;
	}
	return true;
}

void ALedgerSliceCharacter::BeginPlay()
{
	Super::BeginPlay();
	MarkStreetWalkable();
	CloseStreetEnds();
	USkeletalMesh* Body = LoadObject<USkeletalMesh>(nullptr, MeshPath());
	UAnimSequenceBase* Clips[3] = { nullptr, nullptr, nullptr };
	for (int32 I = 0; I < 3; ++I)
	{
		Clips[I] = LoadObject<UAnimSequenceBase>(nullptr, ClipPath(I));
		if (Clips[I] != nullptr) { ++ClipsLoaded; }
	}
	USkeletalMeshComponent* M = GetMesh();
	if (Body == nullptr || M == nullptr) { return; }
	M->SetSkeletalMeshAsset(Body);
	bBodyLoaded = true;
	// THE FEET AND THEIR STEPS (StepTick): the clips keep playing, and the
	// feet the sound comes from stay placed, while the body is hidden from a
	// close camera.
	M->VisibilityBasedAnimTickOption = EVisibilityBasedAnimTickOption::AlwaysTickPoseAndRefreshBones;
	for (int32 B = 0; B < M->GetNumBones(); ++B)
	{
		const FName N = M->GetBoneName(B);
		const FString S = N.ToString();
		if (S.EndsWith(TEXT("LeftFoot"))) { FootBone[0] = N; }
		else if (S.EndsWith(TEXT("RightFoot"))) { FootBone[1] = N; }
	}
	for (int32 Run = 0; Run < 2; ++Run)
	{
		for (int32 I = 0; I < MaxStepClips; ++I)
		{
			const FString Path = StepClipPath(Run == 1, I);
			if (!FPackageName::DoesPackageExist(FPackageName::ObjectPathToPackageName(Path))) { break; }
			if (USoundBase* S = LoadObject<USoundBase>(nullptr, *Path)) { (Run == 1 ? RunStepClips : StepClips).Add(S); }
		}
	}
	StepAttenuation = NewObject<USoundAttenuation>(this);
	{
		FSoundAttenuationSettings& A = StepAttenuation->Attenuation;
		A.bAttenuate = true;
		A.bSpatialize = true;
		A.AttenuationShape = EAttenuationShape::Sphere;
		A.AttenuationShapeExtents = FVector(400.0f, 0.0f, 0.0f);
		A.FalloffDistance = 1800.0f;
		A.DistanceAlgorithm = EAttenuationDistanceModel::NaturalSound;
	}
	UE_LOG(LogTemp, Log, TEXT("LedgerSteps: %d walking and %d running step sound(s), feet %s and %s"), StepClips.Num(),
		RunStepClips.Num(), *FootBone[0].ToString(), *FootBone[1].ToString());
	if (StartGaspMover(M)) { return; }
	if (StartMotionMatching(M)) { return; }
	M->SetAnimInstanceClass(ULedgerLocomotionAnim::StaticClass());
	if (ULedgerLocomotionAnim* A = Cast<ULedgerLocomotionAnim>(M->GetAnimInstance()))
	{
		A->Setup(Clips[0], Clips[1] != nullptr ? Clips[1] : Clips[0], Clips[2] != nullptr ? Clips[2] : Clips[1],
		         WalkSpeedCm, RunSpeedCm);
		M->InitAnim(true);
	}
}

bool ALedgerSliceCharacter::StartMotionMatching(USkeletalMeshComponent* M)
{
	// ONLY WITH -LedgerMotionMatch (22 October): measured on the set route, both it and his own clips
	// slide over 7 cm on about half their steps (17 of 39, 35 of 72); it is worse at stops (67 cm at the
	// median), they slide his right foot on every stride; the sample's steering inside its blend is not
	// built yet (production/research/sit-and-turn/TOM-MOTION-MATCHING-2026-10-22.md). Neither passes,
	// so the player keeps the walk he has until one does.
	if (M == nullptr || !FParse::Param(FCommandLine::Get(), TEXT("LedgerMotionMatch"))) { return false; }
	// THE SAMPLE'S STANDING SET: walk and run (loops, starts, stops, pivots), the idles and the turns
	// in place, at the sample's own paths (F:/LedgerTools/game-inputs/gasp, copied into the build). The
	// sparse walk and run sets: the dense ones the sample's own player uses (its chooser's level 0) were
	// measured too (22 October) and slid more in the steady walk, 15 to 24 cm against 3 to 6.
	static const TCHAR* Names[] = {
		TEXT("Sparse/PSD_Sparse_Stand_Walk_Loops"), TEXT("Sparse/PSD_Sparse_Stand_Walk_Starts"),
		TEXT("Sparse/PSD_Sparse_Stand_Walk_Stops"), TEXT("Sparse/PSD_Sparse_Stand_Walk_Pivots"),
		TEXT("Sparse/PSD_Sparse_Stand_Run_Loops"), TEXT("Sparse/PSD_Sparse_Stand_Run_Starts"),
		TEXT("Sparse/PSD_Sparse_Stand_Run_Stops"), TEXT("Sparse/PSD_Sparse_Stand_Run_Pivots"),
		TEXT("Dense/PSD_Dense_Stand_Idles"), TEXT("Dense/PSD_Dense_Stand_TurnInPlace") };
	const FString Root = TEXT("/Game/Characters/UEFN_Mannequin/Animations/MotionMatchingData/Databases/");
	TArray<UPoseSearchDatabase*> Dbs;
	for (const TCHAR* N : Names)
	{
		const FString Pkg = Root + N;
		if (!FPackageName::DoesPackageExist(Pkg)) { continue; }
		if (UPoseSearchDatabase* D = LoadObject<UPoseSearchDatabase>(nullptr, *(Pkg + TEXT(".") + FPackageName::GetShortName(Pkg)))) { Dbs.Add(D); }
	}
	static const TCHAR* MannequinPath = TEXT("/Game/Characters/UEFN_Mannequin/Meshes/SKM_UEFN_Mannequin.SKM_UEFN_Mannequin");
	static const TCHAR* RetargetPath = TEXT("/Game/Ledger/People/tom-player/RTG_UEFN_to_TomPlayer.RTG_UEFN_to_TomPlayer");
	USkeletalMesh* Mannequin = FPackageName::DoesPackageExist(FPackageName::ObjectPathToPackageName(FString(MannequinPath)))
		? LoadObject<USkeletalMesh>(nullptr, MannequinPath) : nullptr;
	UIKRetargeter* Retargeter = FPackageName::DoesPackageExist(FPackageName::ObjectPathToPackageName(FString(RetargetPath)))
		? LoadObject<UIKRetargeter>(nullptr, RetargetPath) : nullptr;
	// THE GRAPH, script-made (MotionMatchAnim.h): with the sample's Offset Root Bone, or without it
	// for a comparison (-LedgerNoOffsetRoot).
	const bool bOffsetRoot = !FParse::Param(FCommandLine::Get(), TEXT("LedgerNoOffsetRoot"));
	const FString GraphPath = bOffsetRoot ? TEXT("/Game/Ledger/People/tom-player/ABP_TomMotion.ABP_TomMotion_C")
	                                      : TEXT("/Game/Ledger/People/tom-player/ABP_TomMotionPlain.ABP_TomMotionPlain_C");
	UClass* Graph = FPackageName::DoesPackageExist(FPackageName::ObjectPathToPackageName(GraphPath))
		? LoadClass<ULedgerMotionMatchAnim>(nullptr, *GraphPath) : nullptr;
	if (Dbs.Num() < UE_ARRAY_COUNT(Names) || Mannequin == nullptr || Retargeter == nullptr || Graph == nullptr)
	{
		UE_LOG(LogTemp, Log, TEXT("LedgerWalk: his own clips (motion matching needs %d databases, found %d; mannequin %s; retargeter %s; graph %s)"),
			(int32)UE_ARRAY_COUNT(Names), Dbs.Num(), Mannequin != nullptr ? TEXT("yes") : TEXT("no"), Retargeter != nullptr ? TEXT("yes") : TEXT("no"),
			Graph != nullptr ? TEXT("yes") : TEXT("no"));
		return false;
	}
	// THE MANNEQUIN, placed as his body is and never drawn, its pose worked out every frame.
	MotionDriver = NewObject<USkeletalMeshComponent>(this, TEXT("MotionDriver"));
	MotionDriver->SetupAttachment(GetCapsuleComponent());
	MotionDriver->SetRelativeLocationAndRotation(FVector(0.0, 0.0, -88.0), FRotator(0.0f, -90.0f, 0.0f));
	MotionDriver->SetSkeletalMeshAsset(Mannequin);
	MotionDriver->SetCollisionEnabled(ECollisionEnabled::NoCollision);
	MotionDriver->SetCastShadow(false);
	MotionDriver->SetHiddenInGame(true);
	MotionDriver->VisibilityBasedAnimTickOption = EVisibilityBasedAnimTickOption::AlwaysTickPoseAndRefreshBones;
	MotionDriver->RegisterComponent();
	MotionDriver->SetAnimInstanceClass(Graph);
	ULedgerMotionMatchAnim* Matcher = Cast<ULedgerMotionMatchAnim>(MotionDriver->GetAnimInstance());
	if (Matcher == nullptr) { MotionDriver->DestroyComponent(); MotionDriver = nullptr; return false; }
	Matcher->Setup(Dbs);
	// HIS BODY copies the mannequin's pose after it is worked out.
	M->SetAnimInstanceClass(ULedgerRetargetAnim::StaticClass());
	if (ULedgerRetargetAnim* R = Cast<ULedgerRetargetAnim>(M->GetAnimInstance()))
	{
		R->Setup(MotionDriver, Retargeter);
		M->InitAnim(true);
	}
	M->AddTickPrerequisiteComponent(MotionDriver);
	// THE SAMPLE'S OWN MOVEMENT (SandboxCharacter_CMC's UpdateMovement_PreCMC and its Calculate
	// functions, exported and read 22 October), which its clips' paths were matched to: speeding up
	// at 800 cm/s/s, ground friction 5, no extra braking friction; braking 2,000 cm/s/s when let go and
	// 500 while still pushed (set each frame, Tick).
	UCharacterMovementComponent* Move = GetCharacterMovement();
	Move->MaxAcceleration = 800.0f;
	Move->GroundFriction = 5.0f;
	Move->BrakingFrictionFactor = 0.0f;
	Move->BrakingDecelerationWalking = 2000.0f;
	// AND ITS TURNING: the capsule faces where he goes at once (the sample's UpdateRotation_PreCMC sets
	// the rate to -1 on the ground), and his body turns as the clips and the offset root carry it.
	Move->RotationRate = FRotator(0.0f, -1.0f, 0.0f);
	UE_LOG(LogTemp, Log, TEXT("LedgerWalk: motion matching on the sample's %d databases, copied onto him through %s; offset root %s"),
		Dbs.Num(), *Retargeter->GetName(), bOffsetRoot ? TEXT("on") : TEXT("off"));
	return true;
}

bool ALedgerSliceCharacter::StartGaspMover(USkeletalMeshComponent* M)
{
	if (M == nullptr || !FParse::Param(FCommandLine::Get(), TEXT("LedgerGaspMover"))) { return false; }
	// THE SAMPLE'S OWN PIECES at their own paths (copied into the game unchanged, 24 October), and his
	// MetaHuman as assembled (the face he was given, L1).
	static const TCHAR* MoverPath = TEXT("/Game/Blueprints/SandboxCharacter_CMC.SandboxCharacter_CMC_C");
	static const TCHAR* BodyPath = TEXT("/Game/Ledger/MetaHumans/MH_TomL1/BP_MH_TomL1.BP_MH_TomL1_C");
	static const TCHAR* CopyPath = TEXT("/Game/Blueprints/RetargetedCharacters/ABP_GenericRetarget.ABP_GenericRetarget_C");
	auto Load = [](const TCHAR* P) -> UClass*
	{
		return FPackageName::DoesPackageExist(FPackageName::ObjectPathToPackageName(FString(P))) ? LoadClass<UObject>(nullptr, P) : nullptr;
	};
	UClass* MoverClass = Load(MoverPath);
	UClass* BodyClass = Load(BodyPath);
	UClass* CopyClass = Load(CopyPath);
	UWorld* World = GetWorld();
	if (World == nullptr || MoverClass == nullptr || !MoverClass->IsChildOf(ACharacter::StaticClass()) || BodyClass == nullptr || CopyClass == nullptr)
	{
		UE_LOG(LogTemp, Log, TEXT("LedgerWalk: his own clips (Epic's route needs the sample's character %s, his MetaHuman %s, the sample's retarget graph %s)"),
			MoverClass != nullptr ? TEXT("yes") : TEXT("no"), BodyClass != nullptr ? TEXT("yes") : TEXT("no"), CopyClass != nullptr ? TEXT("yes") : TEXT("no"));
		return false;
	}
	FActorSpawnParameters Spawn;
	Spawn.Owner = this;
	Spawn.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AdjustIfPossibleButAlwaysSpawn;
	ACharacter* Mover = World->SpawnActor<ACharacter>(MoverClass, GetActorLocation(), FRotator(0.0f, GetActorRotation().Yaw, 0.0f), Spawn);
	if (Mover == nullptr) { return false; }
	// a controller of its own, so its movement takes input (it is never the player's: the camera and the
	// game's own systems stay on him)
	if (Mover->GetController() == nullptr) { Mover->SpawnDefaultController(); }
	Mover->AddTickPrerequisiteActor(this);
	// HIS BODY IN ITS SLOT, as the sample's AC_VisualOverrideManager puts one there: the slot tagged
	// VisualOverride takes the body's class, and the mannequin is hidden (it keeps working out its pose:
	// its mesh ticks pose and bones always). The body copies the hidden pose through the retargeter its
	// tag names (ABP_GenericRetarget looks the tag up in its IKRetargeter_Map, as BP_Kellan's body is tagged).
	UChildActorComponent* Slot = nullptr;
	for (UActorComponent* C : Mover->GetComponentsByTag(UChildActorComponent::StaticClass(), FName(TEXT("VisualOverride")))) { Slot = Cast<UChildActorComponent>(C); if (Slot != nullptr) { break; } }
	if (Slot != nullptr) { Slot->SetChildActorClass(BodyClass); }
	AActor* Worn = Slot != nullptr ? Slot->GetChildActor() : nullptr;
	TInlineComponentArray<USkeletalMeshComponent*> Parts;
	if (Worn != nullptr) { Worn->GetComponents(Parts); }
	// he is the player: his body works out its pose whether or not the camera draws it this frame (a
	// MetaHuman's parts tick only when drawn, and the measure's side camera froze it, 24 October)
	for (USkeletalMeshComponent* P : Parts) { P->VisibilityBasedAnimTickOption = EVisibilityBasedAnimTickOption::AlwaysTickPoseAndRefreshBones; }
	for (USkeletalMeshComponent* P : Parts) { if (P->GetName() == TEXT("Body")) { WornBody = P; break; } }
	if (WornBody == nullptr)
	{
		UE_LOG(LogTemp, Log, TEXT("LedgerWalk: his own clips (the sample's character has %s, his MetaHuman %s)"),
			Slot != nullptr ? TEXT("its slot") : TEXT("no VisualOverride slot"), Worn != nullptr ? TEXT("has no Body") : TEXT("did not spawn"));
		Mover->Destroy();
		return false;
	}
	WornBody->ComponentTags.AddUnique(FName(TEXT("RTG_UEFN_to_Metahuman_nrw")));
	WornAnimClass = CopyClass;
	WornBody->SetAnimInstanceClass(CopyClass);
	WornBody->AddTickPrerequisiteComponent(Mover->GetMesh());
	Mover->GetMesh()->SetVisibility(false, false);
	// THE WORN BODY TOUCHES NOTHING (24 October, the first measure: his outfits' bodies blocked the mover's own
	// capsule, which walked a second and stopped while still pushed), and the hidden mannequin keeps its
	// finest level of detail (a hidden mesh's level can go stale, and the body copies it).
	Worn->SetActorEnableCollision(false);
	Mover->MoveIgnoreActorAdd(Worn);
	Mover->GetMesh()->SetForcedLOD(1);
	GaspMover = Mover;
	// HIS OWN BODY AND CAPSULE PUT BY: the stand-in body unseen and still, his capsule riding on the
	// mover's (no collision of its own, no movement of its own).
	M->SetVisibility(false, true);
	M->SetComponentTickEnabled(false);
	GetCapsuleComponent()->SetCollisionEnabled(ECollisionEnabled::NoCollision);
	GetCharacterMovement()->DisableMovement();
	GetCharacterMovement()->SetComponentTickEnabled(false);
	GetRootComponent()->AttachToComponent(Mover->GetRootComponent(), FAttachmentTransformRules::SnapToTargetNotIncludingScale);
	// the sample's own settings its graphs read (its data-driven console variables, DefaultEngine.ini)
	const IConsoleVariable* FootMode = IConsoleManager::Get().FindConsoleVariable(TEXT("DDCvar.FootPlacementMode"));
	const IConsoleVariable* DbLod = IConsoleManager::Get().FindConsoleVariable(TEXT("DDCvar.MMDatabaseLOD"));
	UE_LOG(LogTemp, Log, TEXT("LedgerWalk: Epic's route: the sample's %s moves, he wears %s through %s; foot placement mode %d, database level %d"), *Mover->GetClass()->GetName(),
		*BodyClass->GetName(), *CopyClass->GetName(), FootMode != nullptr ? FootMode->GetInt() : -1, DbLod != nullptr ? DbLod->GetInt() : -1);
	return true;
}

void ALedgerSliceCharacter::GaspTick()
{
	if (GaspMover == nullptr) { return; }
	// WHERE THE GAME PUTS HIM, THE MOVER GOES (24 October, the first measures: the game places him at his
	// start after the mover was made where he loaded, and the mover walked from there into a wall): any
	// move the game makes of him (his start, a door, a scene) takes the mover with it.
	USceneComponent* Root = GetRootComponent();
	if (Root->GetAttachParent() == GaspMover->GetRootComponent() && (Root->GetRelativeLocation().SizeSquared() > 1.0 || !Root->GetRelativeRotation().IsNearlyZero(0.5f)))
	{
		const FVector Where = Root->GetComponentLocation();
		const float Yaw = Root->GetComponentRotation().Yaw;
		GaspMover->SetActorLocationAndRotation(Where, FRotator(0.0f, Yaw, 0.0f), false, nullptr, ETeleportType::TeleportPhysics);
		Root->SetRelativeLocationAndRotation(FVector::ZeroVector, FRotator::ZeroRotator);
		UE_LOG(LogTemp, Log, TEXT("LedgerWalk: the mover follows where the game put him (%.0f, %.0f)"), Where.X, Where.Y);
	}
	// WHAT THE KEYS, THE PAD AND THE ROUTE ASKED THIS FRAME goes to the mover (his own movement takes none).
	const FVector In = ConsumeMovementInputVector();
	GaspLastIn = (float)In.Size();
	if (!In.IsNearlyZero()) { GaspMover->AddMovementInput(In.GetSafeNormal2D(), FMath::Min(1.0, In.Size())); }
	// HIS PACE as the sample's input state: walking unless he runs (shift, or the route's run). The sample
	// picks its gait from that (GetDesiredGait); with a full push and no walk wish it would run.
	const bool bWalk = GetCharacterMovement()->MaxWalkSpeed <= WalkSpeedCm + 1.0f;
	if (FStructProperty* State = FindFProperty<FStructProperty>(GaspMover->GetClass(), TEXT("CharacterInputState")))
	{
		void* Data = State->ContainerPtrToValuePtr<void>(GaspMover);
		for (TFieldIterator<FBoolProperty> It(State->Struct); It; ++It)
		{
			const FString N = It->GetName();
			if (N.StartsWith(TEXT("WantsToWalk"))) { It->SetPropertyValue_InContainer(Data, bWalk); }
			// he turns to where he goes, as the game's player always has: no strafing (the sample's own
			// character strafes toward its controller's view by default; this one's controller is a puppet's)
			else if (N.StartsWith(TEXT("WantsToSprint")) || N.StartsWith(TEXT("WantsToStrafe")) || N.StartsWith(TEXT("WantsToAim"))) { It->SetPropertyValue_InContainer(Data, false); }
		}
	}
	// THE SAMPLE'S FOOT LOCK HELD THROUGH EACH CONTACT (24 October, try 2 at the slide; only with
	// -GaspUnplantCm= and/or -GaspUnplantDeg=): its foot placement holds a planted foot until the animation's
	// foot is 20 cm or 60 degrees away (40 cm in stops; its PlantSettings_Default and _Stops), then lets it go
	// and eases it over; with a wider radius it lets go only as the animation lifts the foot (its contact
	// curves). Set on the mover's own graph each frame, Epic's asset untouched.
	static float UnplantCm = -1.0f, UnplantDeg = -1.0f;
	static const bool bUnplant = FParse::Value(FCommandLine::Get(), TEXT("GaspUnplantCm="), UnplantCm) | FParse::Value(FCommandLine::Get(), TEXT("GaspUnplantDeg="), UnplantDeg);
	if (bUnplant)
	{
		if (UAnimInstance* Graph = GaspMover->GetMesh()->GetAnimInstance())
		{
			for (const TCHAR* Which : { TEXT("PlantSettings_Default"), TEXT("PlantSettings_Stops") })
			{
				FStructProperty* Plant = FindFProperty<FStructProperty>(Graph->GetClass(), Which);
				if (Plant == nullptr) { continue; }
				void* Settings = Plant->ContainerPtrToValuePtr<void>(Graph);
				if (UnplantCm > 0.0f) { if (FFloatProperty* R = FindFProperty<FFloatProperty>(Plant->Struct, TEXT("UnplantRadius"))) { R->SetPropertyValue_InContainer(Settings, UnplantCm); } }
				if (UnplantDeg > 0.0f) { if (FFloatProperty* A = FindFProperty<FFloatProperty>(Plant->Struct, TEXT("UnplantAngle"))) { A->SetPropertyValue_InContainer(Settings, UnplantDeg); } }
			}
		}
	}
	// what reads his speed (his steps, people noticing him) reads the mover's
	GetCapsuleComponent()->ComponentVelocity = GaspMover->GetVelocity();
	GetCharacterMovement()->Velocity = GaspMover->GetVelocity();
	// HIS METAHUMAN'S OWN SET-UP may put its body's graph back as it starts: the copying graph again
	if (WornBody != nullptr && WornAnimClass != nullptr && WornBody->GetAnimClass() != WornAnimClass)
	{
		WornBody->SetAnimInstanceClass(WornAnimClass);
		UE_LOG(LogTemp, Log, TEXT("LedgerWalk: his MetaHuman's body graph set again to the sample's copy"));
	}
}

namespace
{
	// THE ROUTE: seconds, heading from his first (degrees), pace (0 stand, 1 walk, 2 run), and the kind
	// a contact made in its first second is counted as (later contacts of a walk count as the loop).
	// Kinds: 0 stand, 1 start, 2 loop, 3 stop, 4 turn, 5 run.
	struct FProofSeg { float Seconds; float Yaw; int32 Pace; int32 Kind; };
	const FProofSeg GProofRoute[] = {
		{ 3.0f,   0.0f, 0, 0 },   // standing; the feet's rest height is learnt in its last second
		{ 4.0f,   0.0f, 1, 1 },   // a start, then the walk
		{ 2.5f,   0.0f, 0, 3 },   // a stop
		{ 3.5f, 180.0f, 1, 4 },   // about, from standing
		{ 3.5f,   0.0f, 1, 4 },   // about again, while walking (a pivot)
		{ 1.5f,  45.0f, 1, 4 },   // a turn while walking
		{ 2.0f,   0.0f, 1, 4 },   // and back
		{ 2.5f,   0.0f, 0, 3 },   // a stop
		{ 2.5f, 180.0f, 2, 5 },   // a run, back the way he came
		{ 2.5f,   0.0f, 0, 3 },   // a stop from the run
	};
	const TCHAR* GKindNames[6] = { TEXT("stand"), TEXT("start"), TEXT("loop"), TEXT("stop"), TEXT("turn"), TEXT("run") };
}

void ALedgerSliceCharacter::WalkProofTick(float DeltaSeconds)
{
	static const bool bOn = FParse::Param(FCommandLine::Get(), TEXT("TomWalkProof"));
	const int32 Segs = UE_ARRAY_COUNT(GProofRoute);
	USkeletalMeshComponent* M = GetMesh();
	if (!bOn || ProofSeg >= Segs || M == nullptr || !bBodyLoaded) { return; }
	ProofClock += DeltaSeconds;
	if (ProofSeg < 0)
	{
		// TWO SECONDS for the street to settle, then his heading is the route's first.
		if (ProofClock < 2.0f) { return; }
		for (int32 B = 0; B < M->GetNumBones(); ++B)
		{
			const FString S = M->GetBoneName(B).ToString();
			if (S.EndsWith(TEXT("LeftToeBase"))) { Soles[0].Ball[0] = M->GetBoneName(B); }
			else if (S.EndsWith(TEXT("RightToeBase"))) { Soles[0].Ball[1] = M->GetBoneName(B); }
		}
		Soles[1].Ball[0] = FName(TEXT("ball_l"));
		Soles[1].Ball[1] = FName(TEXT("ball_r"));
		// on Epic's route the body he wears is a MetaHuman's, whose balls are named as the mannequin's
		if (WornBody != nullptr) { Soles[0].Ball[0] = FName(TEXT("ball_l")); Soles[0].Ball[1] = FName(TEXT("ball_r")); }
		// THE CLEAREST LINE: his capsule swept 15 m each way along sixteen headings through the
		// street's walls, kerbs and parked things (people do not stop him during the measure); the
		// route needs about 11 m ahead and 2 m behind, so the heading with the most ahead, with 3 m
		// behind, is taken.
		GetCapsuleComponent()->SetCollisionResponseToChannel(ECC_Pawn, ECR_Ignore);
		if (GaspMover != nullptr) { GaspMover->GetCapsuleComponent()->SetCollisionResponseToChannel(ECC_Pawn, ECR_Ignore); }
		const UCapsuleComponent* Cap = GaspMover != nullptr ? GaspMover->GetCapsuleComponent() : GetCapsuleComponent();
		const FCollisionShape Shape = FCollisionShape::MakeCapsule(Cap->GetScaledCapsuleRadius(), Cap->GetScaledCapsuleHalfHeight() - 5.0f);
		FCollisionQueryParams Q(FName(TEXT("TomWalkProofLine")), false, this);
		// on Epic's route the sweep starts inside the mover's own capsule and his worn body: neither is in the way
		if (GaspMover != nullptr) { Q.AddIgnoredActor(GaspMover); if (WornBody != nullptr) { Q.AddIgnoredActor(WornBody->GetOwner()); } }
		FCollisionResponseParams R;
		R.CollisionResponse.SetResponse(ECC_Pawn, ECR_Ignore);
		FString Blocker;
		auto Clear = [&](float Yaw) -> float
		{
			const FVector From = GetActorLocation() + FVector(0.0, 0.0, 5.0);
			const FVector To = From + FRotator(0.0f, Yaw, 0.0f).Vector() * 1500.0;
			FHitResult Hit;
			if (GaspMover != nullptr)
			{
				// on Epic's route: the mover's own capsule with its own collision, as its movement sweeps it
				TArray<FHitResult> Hits;
				FComponentQueryParams CQ(FName(TEXT("TomWalkProofLine")), GaspMover);
				CQ.AddIgnoredActor(this);
				if (WornBody != nullptr) { CQ.AddIgnoredActor(WornBody->GetOwner()); }
				UPrimitiveComponent* Cap = GaspMover->GetCapsuleComponent();
				GetWorld()->ComponentSweepMulti(Hits, Cap, From, To, Cap->GetComponentQuat(), CQ);
				for (const FHitResult& H : Hits)
				{
					if (H.bBlockingHit) { Blocker = H.GetActor() != nullptr ? H.GetActor()->GetName() : TEXT("?"); return (float)H.Distance; }
				}
				Blocker.Reset();
				return 1500.0f;
			}
			return GetWorld()->SweepSingleByChannel(Hit, From, To, FQuat::Identity, ECC_Pawn, Shape, Q, R) ? Hit.Distance : 1500.0f;
		};
		float Best = -1.0f;
		ProofYaw = GetActorRotation().Yaw;
		for (int32 H = 0; H < 16; ++H)
		{
			const float Yaw = GetActorRotation().Yaw + H * 22.5f;
			const float Ahead = Clear(Yaw), Behind = Clear(Yaw + 180.0f);
			const float Score = Behind >= 300.0f ? Ahead : Ahead * 0.1f;
			if (Score > Best) { Best = Score; ProofYaw = Yaw; }
		}
		const float AheadM = Clear(ProofYaw) / 100.0f;
		const FString AheadBy = Blocker;
		ProofLines += FString::Printf(TEXT("the route's heading %.0f degrees, %.1f m clear ahead (%s), %.1f m behind, from %.0f,%.0f") LINE_TERMINATOR,
			ProofYaw, AheadM, AheadBy.IsEmpty() ? TEXT("nothing") : *AheadBy, Clear(ProofYaw + 180.0f) / 100.0f, GetActorLocation().X, GetActorLocation().Y);
		(WornBody != nullptr ? WornBody.Get() : M)->RegisterOnBoneTransformsFinalizedDelegate(FOnBoneTransformsFinalizedMultiCast::FDelegate::CreateUObject(this, &ALedgerSliceCharacter::MeasureFeet));
		ProofSeg = 0;
		ProofSegAt = ProofClock;
		UE_LOG(LogTemp, Display, TEXT("ledgerTomWalk: the route begins, balls %s and %s, %s"), *Soles[0].Ball[0].ToString(), *Soles[0].Ball[1].ToString(),
			GaspMover != nullptr ? TEXT("Epic's route (the sample's character, his MetaHuman worn)") : (MotionDriver != nullptr ? TEXT("motion matching") : TEXT("his own clips")));
	}
	if (ProofClock - ProofSegAt >= GProofRoute[ProofSeg].Seconds)
	{
		++ProofSeg;
		ProofSegAt = ProofClock;
		if (ProofSeg >= Segs)
		{
			// THE JOINS (starts, stops, turns) carry the bar; the loop and the run are named beside them,
			// and the mannequin's own feet after his.
			const FFeetMeasure& F = Soles[0];
			const float Joins = FMath::Max3(F.Worst[1], F.Worst[3], F.Worst[4]);
			const bool bPass = Joins <= 3.0f && F.Contacts[1] + F.Contacts[3] + F.Contacts[4] > 0;
			FString Kinds, Driver;
			for (int32 K = 0; K < 6; ++K)
			{
				Kinds += FString::Printf(TEXT(" %s=%.2f/%d"), GKindNames[K], F.Worst[K], F.Contacts[K]);
				Driver += FString::Printf(TEXT(" %s=%.2f/%d"), GKindNames[K], Soles[1].Worst[K], Soles[1].Contacts[K]);
			}
			// on Epic's route, the sample's settings as they stood at the route's end (so a setting given at
			// launch is shown to have taken), and whether its character moved by its animation's root motion
			FString Settings;
			if (GaspMover != nullptr)
			{
				auto CVarInt = [](const TCHAR* N) { const IConsoleVariable* V = IConsoleManager::Get().FindConsoleVariable(N); return V != nullptr ? V->GetInt() : -1; };
				const FBoolProperty* RootMotion = FindFProperty<FBoolProperty>(GaspMover->GetClass(), TEXT("UsingAttributeBasedRootMotion"));
				// and the foot lock's let-go distance and angle in force on the mover's graph
				float Radius = -1.0f, Angle = -1.0f;
				if (const UAnimInstance* Graph = GaspMover->GetMesh()->GetAnimInstance())
				{
					if (const FStructProperty* Plant = FindFProperty<FStructProperty>(Graph->GetClass(), TEXT("PlantSettings_Default")))
					{
						const void* PS = Plant->ContainerPtrToValuePtr<void>(Graph);
						if (const FFloatProperty* R = FindFProperty<FFloatProperty>(Plant->Struct, TEXT("UnplantRadius"))) { Radius = R->GetPropertyValue_InContainer(PS); }
						if (const FFloatProperty* A = FindFProperty<FFloatProperty>(Plant->Struct, TEXT("UnplantAngle"))) { Angle = A->GetPropertyValue_InContainer(PS); }
					}
				}
				Settings = FString::Printf(TEXT(" settings: footPlacementMode=%d databaseLevel=%d rootMotionSetting=%d rootMotionUsed=%d unplantCm=%.0f unplantDeg=%.0f"),
					CVarInt(TEXT("DDCvar.FootPlacementMode")), CVarInt(TEXT("DDCvar.MMDatabaseLOD")), CVarInt(TEXT("DDCVar.AttributeBasedRootMotion.Enable")),
					RootMotion != nullptr ? (RootMotion->GetPropertyValue_InContainer(GaspMover.Get()) ? 1 : 0) : -1, Radius, Angle);
			}
			// and beside it, planted read from the moving animation's own contact marks (Epic's route only)
			FString ByMarks;
			if (GaspMover != nullptr)
			{
				for (int32 Bd = 0; Bd < 2; ++Bd)
				{
					const FFeetMeasure& C = Soles[Bd];
					const float CJoins = FMath::Max3(C.ConWorst[1], C.ConWorst[3], C.ConWorst[4]);
					ByMarks += FString::Printf(TEXT(" %s=%s worstJoinCm=%.2f"), Bd == 0 ? TEXT("byContactMarks") : TEXT("mannequinByContactMarks"),
						CJoins <= 3.0f && C.ConContacts[1] + C.ConContacts[3] + C.ConContacts[4] > 0 ? TEXT("PASS") : TEXT("FAIL"), CJoins);
					for (int32 K = 0; K < 6; ++K) { ByMarks += FString::Printf(TEXT(" %s=%.2f/%d"), GKindNames[K], C.ConWorst[K], C.ConContacts[K]); }
				}
			}
			const FString Line = FString::Printf(TEXT("ledgerTomWalk=%s mode=%s worstJoinCm=%.2f%s frames=%d mannequin:%s%s%s"), bPass ? TEXT("PASS") : TEXT("FAIL"),
				GaspMover != nullptr ? TEXT("gasp-metahuman") : (MotionDriver != nullptr ? (FParse::Param(FCommandLine::Get(), TEXT("LedgerNoOffsetRoot")) ? TEXT("matched-no-offset") : TEXT("matched")) : TEXT("clips")),
				Joins, *Kinds, ProofFrames, (MotionDriver != nullptr || GaspMover != nullptr) ? *Driver : TEXT(" none"), *Settings, *ByMarks);
			UE_LOG(LogTemp, Display, TEXT("%s"), *Line);
			FFileHelper::SaveStringToFile(Line + LINE_TERMINATOR + ProofLines, *(FPaths::ProjectSavedDir() / TEXT("Logs") / TEXT("tom-walk.txt")));
			GetCharacterMovement()->MaxWalkSpeed = WalkSpeedCm;
			if (FParse::Param(FCommandLine::Get(), TEXT("TomWalkProofExit"))) { FPlatformMisc::RequestExit(false); }
			return;
		}
	}
	const FProofSeg& S = GProofRoute[ProofSeg];
	// -TomWalkProofShots: a side-on camera beside him, level with his knees, and a picture each tenth of
	// a second through the first start and the first stop (Saved/TomWalk), so the feet are seen.
	static const bool bShots = FParse::Param(FCommandLine::Get(), TEXT("TomWalkProofShots"));
	if (bShots)
	{
		APlayerController* ShotPC = Cast<APlayerController>(GetController());
		if (ShotCamera == nullptr && ShotPC != nullptr)
		{
			ShotCamera = GetWorld()->SpawnActor<ACameraActor>(GetActorLocation(), FRotator::ZeroRotator);
			if (ShotCamera != nullptr) { ShotCamera->GetCameraComponent()->SetFieldOfView(40.0f); ShotPC->SetViewTarget(ShotCamera); }
		}
		if (ShotCamera != nullptr)
		{
			// on whichever side is open there and then (a line traced each way), never inside a wall
			const FVector Look = GetActorLocation() - FVector(0.0, 0.0, 50.0);
			float Room[2] = { 450.0f, 450.0f };
			for (int32 K = 0; K < 2; ++K)
			{
				FHitResult Hit;
				FCollisionQueryParams CQ(FName(TEXT("TomWalkProofCamera")), false, this);
				const FVector Way = FRotator(0.0f, ProofYaw + (K == 0 ? 90.0f : -90.0f), 0.0f).Vector();
				if (GetWorld()->LineTraceSingleByChannel(Hit, Look, Look + Way * 450.0, ECC_Camera, CQ)) { Room[K] = Hit.Distance; }
			}
			const int32 K = Room[0] >= Room[1] ? 0 : 1;
			const FVector Side = FRotator(0.0f, ProofYaw + (K == 0 ? 90.0f : -90.0f), 0.0f).Vector();
			// with picture spans (below) the camera is set once as each span begins and then held still, so a
			// planted foot stays on the same pixels and a slide shows against the pavement
			static int32 HeldSpan = -2;
			int32 InSpan = -1;
			{
				FString List;
				if (FParse::Value(FCommandLine::Get(), TEXT("TomWalkProofShotsAt="), List, false))
				{
					TArray<FString> Parts;
					List.ParseIntoArray(Parts, TEXT(","));
					for (int32 Sp = 0; Sp < Parts.Num(); ++Sp)
					{
						FString A, B;
						if (Parts[Sp].Split(TEXT("-"), &A, &B) && ProofClock >= FCString::Atof(*A) && ProofClock <= FCString::Atof(*B)) { InSpan = Sp; }
					}
				}
			}
			if (InSpan < 0 || InSpan != HeldSpan)
			{
				ShotCamera->SetActorLocationAndRotation(Look + Side * FMath::Max(120.0f, Room[K] - 40.0f) + FVector(0.0, 0.0, 10.0), (-Side).Rotation());
				HeldSpan = InSpan;
			}
			const float T = ProofClock - ProofSegAt;
			// -TomWalkProofShotsAt=a-b,c-d,...: pictures ten a second through those spans of the route's clock
			// instead (24 October: the worst steps fall at the same moments in each run from the same start,
			// so they can be pictured for judging by eye)
			static TArray<FVector2f> Spans;
			static const bool bSpans = []()
			{
				FString List;
				if (!FParse::Value(FCommandLine::Get(), TEXT("TomWalkProofShotsAt="), List, false)) { return false; }
				TArray<FString> Parts;
				List.ParseIntoArray(Parts, TEXT(","));
				for (const FString& Part : Parts)
				{
					FString A, B;
					if (Part.Split(TEXT("-"), &A, &B)) { Spans.Add(FVector2f(FCString::Atof(*A), FCString::Atof(*B))); }
				}
				return Spans.Num() > 0;
			}();
			if (bSpans)
			{
				bool bIn = false;
				for (const FVector2f& Sp : Spans) { bIn |= ProofClock >= Sp.X && ProofClock <= Sp.Y; }
				if (bIn && ProofClock >= NextShotAt)
				{
					FScreenshotRequest::RequestScreenshot(FPaths::ConvertRelativePathToFull(FPaths::ProjectSavedDir() / TEXT("TomWalk")
						/ FString::Printf(TEXT("w%05.2f.png"), ProofClock)), false, false);
					NextShotAt = ProofClock + 0.1f;
				}
			}
			else if ((ProofSeg == 1 || ProofSeg == 2 || ProofSeg == 3) && T < 1.6f && ProofClock >= NextShotAt)
			{
				FScreenshotRequest::RequestScreenshot(FPaths::ConvertRelativePathToFull(FPaths::ProjectSavedDir() / TEXT("TomWalk")
					/ FString::Printf(TEXT("%s-%02d.png"), ProofSeg == 1 ? TEXT("start") : (ProofSeg == 2 ? TEXT("stop") : TEXT("about")), FMath::FloorToInt(T * 10.0f))), false, false);
				NextShotAt = ProofClock + 0.1f;
			}
		}
	}
	// THE FIRST DAY'S TOUR holds his feet (CrimeProbe.cpp, WalkRoundTick); the measure walks him anyway.
	if (APlayerController* PC = Cast<APlayerController>(GetController())) { if (PC->IsMoveInputIgnored()) { PC->ResetIgnoreMoveInput(); } }
	GetCharacterMovement()->MaxWalkSpeed = S.Pace == 2 ? RunSpeedCm : WalkSpeedCm;
	if (S.Pace > 0) { AddMovementInput(FRotator(0.0f, ProofYaw + S.Yaw, 0.0f).Vector(), 1.0f); }
	// FOUR TIMES A SECOND, what moves and what plays: his speed, where his body's root stands from
	// the capsule, and the clip the motion matching has picked.
	if (FMath::FloorToInt(ProofClock * 4.0f) != FMath::FloorToInt((ProofClock - DeltaSeconds) * 4.0f))
	{
		const ULedgerMotionMatchAnim* Mm = MotionDriver != nullptr ? Cast<ULedgerMotionMatchAnim>(MotionDriver->GetAnimInstance()) : nullptr;
		const FVector RootAt = MotionDriver != nullptr ? MotionDriver->GetBoneLocation(MotionDriver->GetBoneName(0)) : FVector::ZeroVector;
		const FVector Feet = GetActorLocation() - FVector(0.0, 0.0, GetCapsuleComponent()->GetScaledCapsuleHalfHeight());
		FString Gasp;
		if (GaspMover != nullptr)
		{
			// on Epic's route: each body's balls above the floor, and whether the mover's graph is working
			const USkeletalMeshComponent* Man = GaspMover->GetMesh();
			const float Floor = GaspMover->GetActorLocation().Z - GaspMover->GetCapsuleComponent()->GetScaledCapsuleHalfHeight();
			auto Up = [Floor](const USkeletalMeshComponent* B, const TCHAR* Bone) { return B != nullptr && B->GetBoneIndex(FName(Bone)) != INDEX_NONE ? (float)(B->GetBoneLocation(FName(Bone)).Z - Floor) : -99.0f; };
			const UCharacterMovementComponent* MC = GaspMover->GetCharacterMovement();
			Gasp = FString::Printf(TEXT(" mannequin balls %.1f/%.1f, worn %.1f/%.1f, graph %s, lod %d; push %.2f, its input %.2f, accel %.0f, max %.0f, mode %d, at %.0f,%.0f"),
				Up(Man, TEXT("ball_l")), Up(Man, TEXT("ball_r")), Up(WornBody, TEXT("ball_l")), Up(WornBody, TEXT("ball_r")),
				Man->GetAnimInstance() != nullptr ? *Man->GetAnimInstance()->GetClass()->GetName() : TEXT("none"), Man->GetPredictedLODLevel(),
				GaspLastIn, (float)GaspMover->GetLastMovementInputVector().Size(), (float)MC->GetCurrentAcceleration().Size(), MC->GetMaxSpeed(), (int32)MC->MovementMode,
				(float)GaspMover->GetActorLocation().X, (float)GaspMover->GetActorLocation().Y);
		}
		ProofLines += FString::Printf(TEXT("%.2f s, stretch %d, %.0f cm/s, root %.1f cm off, %s%s") LINE_TERMINATOR, ProofClock, ProofSeg,
			GetVelocity().Size2D(), (float)FVector::Dist2D(RootAt, Feet), Mm != nullptr ? *Mm->Describe() : TEXT("-"), *Gasp);
	}
}

void ALedgerSliceCharacter::MeasureFeet()
{
	// ONCE HIS POSE FOR THE FRAME IS FINAL and he stands where the frame draws him: each ball of the
	// foot, planted when within 2.5 cm of its standing height and no higher than the other; its
	// drift along the ground while planted is the slide.
	const int32 Segs = UE_ARRAY_COUNT(GProofRoute);
	// on Epic's route: the MetaHuman body he wears, and the sample's mannequin under it, on the mover's floor
	USkeletalMeshComponent* M = WornBody != nullptr ? WornBody.Get() : GetMesh();
	if (M == nullptr || ProofSeg < 0 || ProofSeg >= Segs) { return; }
	const float T = ProofClock - ProofSegAt;
	const ACharacter* Stand = GaspMover != nullptr ? GaspMover.Get() : this;
	const float Floor = Stand->GetActorLocation().Z - Stand->GetCapsuleComponent()->GetScaledCapsuleHalfHeight();
	++ProofFrames;
	MeasureBody(0, M, ProofSeg, T, Floor);
	if (GaspMover != nullptr) { MeasureBody(1, GaspMover->GetMesh(), ProofSeg, T, Floor); }
	else if (MotionDriver != nullptr) { MeasureBody(1, MotionDriver, ProofSeg, T, Floor); }
}

void ALedgerSliceCharacter::MeasureBody(int32 B, USkeletalMeshComponent* Body, int32 Seg, float T, float Floor)
{
	FFeetMeasure& F = Soles[B];
	if (F.Ball[0].IsNone() || F.Ball[1].IsNone() || Body->GetBoneIndex(F.Ball[0]) == INDEX_NONE) { return; }
	const FProofSeg& S = GProofRoute[Seg];
	const FVector P[2] = { Body->GetBoneLocation(F.Ball[0]), Body->GetBoneLocation(F.Ball[1]) };
	// EACH BALL'S HEIGHT ABOVE THE GROUND UNDER IT (24 October, Epic's route: measured from the capsule's
	// foot, a kerb or the pavement's fall read a foot as planted for metres), traced straight down past
	// his bodies; the capsule's foot where nothing is found
	float H[2];
	for (int32 I = 0; I < 2; ++I)
	{
		FCollisionQueryParams GQ(FName(TEXT("TomWalkProofGround")), false, this);
		if (GaspMover != nullptr) { GQ.AddIgnoredActor(GaspMover); if (WornBody != nullptr) { GQ.AddIgnoredActor(WornBody->GetOwner()); } }
		FHitResult Hit;
		const bool bHit = GetWorld()->LineTraceSingleByChannel(Hit, P[I] + FVector(0.0, 0.0, 40.0), P[I] - FVector(0.0, 0.0, 60.0), ECC_Visibility, GQ);
		H[I] = (float)(P[I].Z - (bHit ? Hit.ImpactPoint.Z : Floor));
	}
	if (Seg == 0)
	{
		if (T > S.Seconds - 1.0f) { F.Rest[0] += H[0]; F.Rest[1] += H[1]; ++F.RestN; }
		return;
	}
	const int32 Kind = S.Pace == 0 ? (T < 1.5f ? 3 : 0) : (S.Pace == 2 ? 5 : (T < 1.0f ? S.Kind : 2));
	// -TomWalkProofTrace: each frame of the first start and stop, each foot's ball along the route and
	// above its standing height, for reading the slide by hand.
	static const bool bTrace = FParse::Param(FCommandLine::Get(), TEXT("TomWalkProofTrace"));
	// -TomWalkProofTraceAt=a-b,...: the same trace through those spans of the route's clock, with the sample's
	// own contact curves (its foot placement plants by them: under 1, planted) and the ball's world position
	// (24 October, research after the walk was set aside: is a worst step a slide the animation means, or not?)
	static TArray<FVector2f> TraceSpans;
	static const bool bTraceSpans = []()
	{
		FString List;
		if (!FParse::Value(FCommandLine::Get(), TEXT("TomWalkProofTraceAt="), List, false)) { return false; }
		TArray<FString> Parts;
		List.ParseIntoArray(Parts, TEXT(","));
		for (const FString& Part : Parts)
		{
			FString A, B2;
			if (Part.Split(TEXT("-"), &A, &B2)) { TraceSpans.Add(FVector2f(FCString::Atof(*A), FCString::Atof(*B2))); }
		}
		return TraceSpans.Num() > 0;
	}();
	bool bInTraceSpan = false;
	for (const FVector2f& Sp : TraceSpans) { bInTraceSpan |= ProofClock >= Sp.X && ProofClock <= Sp.Y; }
	if (bTraceSpans && bInTraceSpan)
	{
		const UAnimInstance* Src = GaspMover != nullptr ? GaspMover->GetMesh()->GetAnimInstance() : nullptr;
		ProofLines += FString::Printf(TEXT("traceAt %s %.3f: left %.1f,%.1f up %.2f%s, right %.1f,%.1f up %.2f%s, contact %.2f/%.2f, mover %.1f,%.1f %.0f cm/s") LINE_TERMINATOR,
			B == 0 ? TEXT("his") : TEXT("mannequin"), ProofClock,
			(float)P[0].X, (float)P[0].Y, H[0] - (F.RestN > 0 ? F.Rest[0] / F.RestN : 0.0f), F.bDown[0] ? TEXT(" down") : TEXT(""),
			(float)P[1].X, (float)P[1].Y, H[1] - (F.RestN > 0 ? F.Rest[1] / F.RestN : 0.0f), F.bDown[1] ? TEXT(" down") : TEXT(""),
			Src != nullptr ? Src->GetCurveValue(FName(TEXT("contact_l"))) : -1.0f, Src != nullptr ? Src->GetCurveValue(FName(TEXT("contact_r"))) : -1.0f,
			GaspMover != nullptr ? (float)GaspMover->GetActorLocation().X : 0.0f, GaspMover != nullptr ? (float)GaspMover->GetActorLocation().Y : 0.0f,
			GaspMover != nullptr ? (float)GaspMover->GetVelocity().Size2D() : 0.0f);
	}
	if (bTrace && (Seg == 1 || Seg == 2) && T < 1.6f)
	{
		const FVector Along = FRotator(0.0f, ProofYaw, 0.0f).Vector();
		ProofLines += FString::Printf(TEXT("trace %s %d %.3f: left %.1f along %.1f up%s, right %.1f along %.1f up%s, capsule %.1f") LINE_TERMINATOR,
			B == 0 ? TEXT("his") : TEXT("mannequin"), Seg, T,
			(float)FVector::DotProduct(P[0], Along), H[0] - (F.RestN > 0 ? F.Rest[0] / F.RestN : 0.0f), F.bDown[0] ? TEXT(" down") : TEXT(""),
			(float)FVector::DotProduct(P[1], Along), H[1] - (F.RestN > 0 ? F.Rest[1] / F.RestN : 0.0f), F.bDown[1] ? TEXT(" down") : TEXT(""),
			(float)FVector::DotProduct(GetActorLocation(), Along));
	}
	// planted by the moving animation's own contact marks (on Epic's route only: the sample's clips carry them)
	if (const UAnimInstance* Src = GaspMover != nullptr ? GaspMover->GetMesh()->GetAnimInstance() : nullptr)
	{
		const float Con[2] = { Src->GetCurveValue(FName(TEXT("contact_l"))), Src->GetCurveValue(FName(TEXT("contact_r"))) };
		for (int32 I = 0; I < 2; ++I)
		{
			const bool bPlanted = Con[I] < 1.0f;
			if (bPlanted && !F.bCon[I]) { F.ConPlanted[I] = P[I]; F.ConSlip[I] = 0.0f; F.ConKind[I] = Kind; ++F.ConContacts[Kind]; }
			else if (bPlanted)
			{
				F.ConSlip[I] = FMath::Max(F.ConSlip[I], (float)FVector::Dist2D(P[I], F.ConPlanted[I]));
				F.ConWorst[F.ConKind[I]] = FMath::Max(F.ConWorst[F.ConKind[I]], F.ConSlip[I]);
			}
			F.bCon[I] = bPlanted;
		}
	}
	for (int32 I = 0; I < 2; ++I)
	{
		const float Rest = F.RestN > 0 ? F.Rest[I] / F.RestN : 0.0f;
		// each foot against its own standing height, the other foot likewise (24 October, the fresh review of
		// Epic's route: the two balls stand a few millimetres apart, and comparing raw heights read a swinging
		// foot passing low as planted)
		const float RestOther = F.RestN > 0 ? F.Rest[1 - I] / F.RestN : 0.0f;
		const bool bDown = H[I] - Rest < 2.5f && H[I] - Rest <= H[1 - I] - RestOther + 1.0f;
		if (bDown && !F.bDown[I])
		{
			F.Planted[I] = P[I];
			F.Slip[I] = 0.0f;
			F.Kind[I] = Kind;
			++F.Contacts[Kind];
		}
		else if (bDown)
		{
			F.Slip[I] = FMath::Max(F.Slip[I], (float)FVector::Dist2D(P[I], F.Planted[I]));
			F.Worst[F.Kind[I]] = FMath::Max(F.Worst[F.Kind[I]], F.Slip[I]);
		}
		if (!bDown && F.bDown[I])
		{
			ProofLines += FString::Printf(TEXT("%.2f s, stretch %d, %s, %s %s foot, slid %.2f cm") LINE_TERMINATOR, ProofClock, Seg,
				GKindNames[F.Kind[I]], B == 0 ? TEXT("his") : TEXT("the mannequin's"), I == 0 ? TEXT("left") : TEXT("right"), F.Slip[I]);
		}
		F.bDown[I] = bDown;
	}
}

void ALedgerSliceCharacter::SetupPlayerInputComponent(UInputComponent* PlayerInputComponent)
{
	Super::SetupPlayerInputComponent(PlayerInputComponent);
	// W A S D ARE READ AS HELD KEYS IN TICK, 29 September: bound as axis keys
	// they are not axes, and the engine's check for that fired on every
	// launch (an "ensure": a crash report and a stall as the game started).
	PlayerInputComponent->BindAxisKey(EKeys::MouseX, this, &ALedgerSliceCharacter::LookYaw);
	PlayerInputComponent->BindAxisKey(EKeys::MouseY, this, &ALedgerSliceCharacter::LookPitch);
	PlayerInputComponent->BindKey(EKeys::LeftShift, IE_Pressed, this, &ALedgerSliceCharacter::RunPressed);
	PlayerInputComponent->BindKey(EKeys::LeftShift, IE_Released, this, &ALedgerSliceCharacter::RunReleased);
	PlayerInputComponent->BindKey(EKeys::E, IE_Pressed, this, &ALedgerSliceCharacter::RequestAct);
	PlayerInputComponent->BindKey(EKeys::T, IE_Pressed, this, &ALedgerSliceCharacter::RequestTalk);
	PlayerInputComponent->BindKey(EKeys::Escape, IE_Pressed, this, &ALedgerSliceCharacter::RequestPause).bExecuteWhenPaused = true;
	// The controller: Start pauses; A takes what the prompt in front offers (CrimeProbe reads it as use or talk).
	PlayerInputComponent->BindKey(EKeys::Gamepad_Special_Right, IE_Pressed, this, &ALedgerSliceCharacter::RequestPause).bExecuteWhenPaused = true;
	PlayerInputComponent->BindKey(EKeys::Gamepad_FaceButton_Bottom, IE_Pressed, this, &ALedgerSliceCharacter::RequestPadAct);
	PlayerInputComponent->BindKey(EKeys::Q, IE_Pressed, this, &ALedgerSliceCharacter::RequestQuit).bExecuteWhenPaused = true;
	PlayerInputComponent->BindKey(EKeys::R, IE_Pressed, this, &ALedgerSliceCharacter::RequestReport);
	PlayerInputComponent->BindKey(EKeys::Z, IE_Pressed, this, &ALedgerSliceCharacter::RequestWait);
	PlayerInputComponent->BindKey(EKeys::F1, IE_Pressed, this, &ALedgerSliceCharacter::RequestNotice);
}

void ALedgerSliceCharacter::MoveForward(float Value)
{
	if (Value == 0.0f || Controller == nullptr) { return; }
	const FRotator Yaw(0.0f, Controller->GetControlRotation().Yaw, 0.0f);
	AddMovementInput(FRotationMatrix(Yaw).GetUnitAxis(EAxis::X), Value);
}

void ALedgerSliceCharacter::MoveRight(float Value)
{
	if (Value == 0.0f || Controller == nullptr) { return; }
	const FRotator Yaw(0.0f, Controller->GetControlRotation().Yaw, 0.0f);
	AddMovementInput(FRotationMatrix(Yaw).GetUnitAxis(EAxis::Y), Value);
}

void ALedgerSliceCharacter::MoveBackward(float Value) { MoveForward(-Value); }
void ALedgerSliceCharacter::MoveLeft(float Value) { MoveRight(-Value); }
// THE PLAYER'S LOOK, from the settings page (Controls): sensitivity 0.5 to 2, and up and down inverted when he asks.
void ALedgerSliceCharacter::LookYaw(float Value) { AddControllerYawInput(Value * LedgerSettings::LookSensitivity()); }
void ALedgerSliceCharacter::LookPitch(float Value) { AddControllerPitchInput(-Value * LedgerSettings::LookSensitivity() * (LedgerSettings::InvertLook() ? -1.0f : 1.0f)); }
void ALedgerSliceCharacter::RunPressed() { GetCharacterMovement()->MaxWalkSpeed = RunSpeedCm; }
void ALedgerSliceCharacter::RunReleased() { GetCharacterMovement()->MaxWalkSpeed = WalkSpeedCm; }
void ALedgerSliceCharacter::RequestAct() { ++ActRequests; }
void ALedgerSliceCharacter::RequestTalk() { ++TalkRequests; }
void ALedgerSliceCharacter::RequestPadAct() { ++PadActRequests; }
int32 ALedgerSliceCharacter::ConsumePadActRequests()
{
	const int32 N = PadActRequests;
	PadActRequests = 0;
	return N;
}
void ALedgerSliceCharacter::RequestPause() { UGameplayStatics::SetGamePaused(this, !UGameplayStatics::IsGamePaused(this)); }
void ALedgerSliceCharacter::RequestQuit()
{
	if (UGameplayStatics::IsGamePaused(this)) { FPlatformMisc::RequestExit(false); }
}
void ALedgerSliceCharacter::RequestReport() { ++ReportRequests; }
void ALedgerSliceCharacter::RequestNotice() { ++NoticeRequests; }
void ALedgerSliceCharacter::RequestWait() { ++WaitRequests; }
int32 ALedgerSliceCharacter::ConsumeWaitRequests()
{
	const int32 N = WaitRequests;
	WaitRequests = 0;
	return N;
}
int32 ALedgerSliceCharacter::ConsumeReportRequests()
{
	const int32 N = ReportRequests;
	ReportRequests = 0;
	return N;
}
int32 ALedgerSliceCharacter::ConsumeNoticeRequests()
{
	const int32 N = NoticeRequests;
	NoticeRequests = 0;
	return N;
}
int32 ALedgerSliceCharacter::ConsumeTalkRequests()
{
	const int32 N = TalkRequests;
	TalkRequests = 0;
	return N;
}
int32 ALedgerSliceCharacter::ConsumeActRequests()
{
	const int32 N = ActRequests;
	ActRequests = 0;
	return N;
}

// THE STREET IS MARKED AS SOMEWHERE A PATH MAY RUN, 24 September. The second
// run (3b658691) had the agent declared and still built no mesh: the engine
// builds navigation only inside a bounds volume, and invokers only say WHERE
// inside those bounds to build (NavigationSystem.cpp,
// IsThereAnywhereToBuildNavigation, which counts volumes and never invokers).
// The street is made at run time, so its volume is too: a box over the road,
// both pavements and a little past each end, given its size through a box in
// its body setup because a packaged game cannot build a brush.
// THE STREET'S TWO ENDS ARE CLOSED, 29 September (the AI tester: running on
// past the end of the street led onto a bare foggy plaza with buildings that
// seem to float, an unfinished edge anyone could walk into). An invisible
// wall across each end, a metre past the street's 42 m, 40 m wide and 4 m
// tall, so the road, both pavements and the yards behind the frontages end
// where the street does. Only the player's walking is stopped; nothing is
// drawn, and a scripted run that places him by hand is not affected.
void ALedgerSliceCharacter::CloseStreetEnds()
{
	UWorld* World = GetWorld();
	if (World == nullptr) { return; }
	for (const double X : { -100.0, 4300.0 })
	{
		FActorSpawnParameters P;
		P.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
		AActor* End = World->SpawnActor<AActor>(AActor::StaticClass(), FTransform(FVector(X, 0.0, 200.0)), P);
		if (End == nullptr) { continue; }
		UBoxComponent* Wall = NewObject<UBoxComponent>(End, TEXT("StreetEnd"));
		Wall->SetBoxExtent(FVector(50.0, 2000.0, 400.0));
		// People only: sight lines, the camera and every trace pass through.
		Wall->SetCollisionEnabled(ECollisionEnabled::QueryAndPhysics);
		Wall->SetCollisionObjectType(ECC_WorldStatic);
		Wall->SetCollisionResponseToAllChannels(ECR_Ignore);
		Wall->SetCollisionResponseToChannel(ECC_Pawn, ECR_Block);
		Wall->SetHiddenInGame(true);
		End->SetRootComponent(Wall);
		Wall->RegisterComponent();
		End->SetActorLocation(FVector(X, 0.0, 200.0));
	}
}

void ALedgerSliceCharacter::MarkStreetWalkable()
{
	UWorld* World = GetWorld();
	if (World == nullptr || FNavigationSystem::GetCurrent<UNavigationSystemV1>(World) == nullptr) { return; }
	// The street runs along +X for 42 m; its frontages stand at 5.125 m
	// either side, so 12 m either side takes both pavements and the doorways.
	const FTransform Where(FVector(2100.0, 0.0, 150.0));
	ANavMeshBoundsVolume* Bounds = World->SpawnActorDeferred<ANavMeshBoundsVolume>(
		ANavMeshBoundsVolume::StaticClass(), Where, nullptr, nullptr, ESpawnActorCollisionHandlingMethod::AlwaysSpawn);
	if (Bounds == nullptr || Bounds->GetBrushComponent() == nullptr) { return; }
	UBodySetup* Box = NewObject<UBodySetup>(Bounds->GetBrushComponent());
	Box->AggGeom.BoxElems.Add(FKBoxElem(5400.0f, 2400.0f, 900.0f));
	Bounds->GetBrushComponent()->BrushBodySetup = Box;
	Bounds->FinishSpawning(Where);
	// THE SIZE IS TOLD AGAIN AFTER SPAWNING, 24 September: the first run of
	// this (e934f1e7) logged the bounds as a point, Min = Max = the centre,
	// because the volume's components register while it spawns, before the
	// box is read, and the navigation system took the empty size then.
	Bounds->GetBrushComponent()->UpdateBounds();
	if (UNavigationSystemV1* Nav = FNavigationSystem::GetCurrent<UNavigationSystemV1>(World))
	{
		Nav->OnNavigationBoundsUpdated(Bounds);
	}
	const FBox Area = Bounds->GetComponentsBoundingBox(true);
	bNavBounds = Area.IsValid != 0 && Area.GetSize().X > 100.0;
	// The bounds reach the navigation system on its next tick, so the build
	// waits half a second rather than racing it.
	GetWorldTimerManager().SetTimer(NavBuildTimer, this, &ALedgerSliceCharacter::BuildStreetNavigation, 0.5f, false);
}

void ALedgerSliceCharacter::BuildStreetNavigation()
{
	UNavigationSystemV1* Nav = FNavigationSystem::GetCurrent<UNavigationSystemV1>(GetWorld());
	if (Nav == nullptr) { return; }
	// Build() spawns the missing mesh for the declared agent, registers it and
	// builds the tiles around the invokers, and blocks until they are done.
	Nav->Build();
	bNavBuilt = Nav->GetDefaultNavDataInstance(FNavigationSystem::DontCreate) != nullptr;
}
