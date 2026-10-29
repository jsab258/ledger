#include "SliceCharacter.h"
#include "LedgerPaper.h"
#include "LedgerSettings.h"
#include "LedgerGarments.h"
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
#include "Engine/OverlapResult.h"
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
#include "AlphaBlend.h"
#include "ChooserFunctionLibrary.h"
#include "StructUtils/StructView.h"
#include "StructUtils/UserDefinedStruct.h"
#include "PoseSearch/PoseSearchLibrary.h"
#include "PoseSearch/PoseSearchHistory.h"
#include "PoseSearch/AnimNode_PoseSearchHistoryCollector.h"
#include "Misc/CommandLine.h"
#include "Misc/PackageName.h"
#include "Misc/Paths.h"
#include "Sound/SoundAttenuation.h"
#include "Sound/SoundBase.h"
#include "MotionWarpingComponent.h"
#include "Animation/AnimMontage.h"
#include "Animation/AnimInstance.h"
#include "Animation/AnimNotifies/AnimNotifyState.h"
#include "Dom/JsonObject.h"
#include "Serialization/JsonReader.h"
#include "Serialization/JsonSerializer.h"
#include "EngineUtils.h"
#include "Engine/StaticMeshActor.h"

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
	SitTick(DeltaSeconds);
	SitProofTick(DeltaSeconds);
	SitRoomTestTick(DeltaSeconds);
	SitApproachTestTick(DeltaSeconds);
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
	// THE CAMERA DISTANCE ON HIS PAGE, 28 October 2026 (his order; Study 9: Mafia's
	// on-foot camera 1.65 m back, 0.45 aside, 0.35 up from a pivot 1.25 m above the
	// feet, an 82-degree lens, against this game's 3.2 m and 90): for the page's
	// pictures only, -CamBackM= -CamSideM= -CamUpM= -CamPivotM= (above the feet)
	// -CamFov= set the arm at the start; with none given the camera is as it was.
	{
		const TCHAR* Cmd = FCommandLine::Get();
		double V = 0.0;
		// HIS PICK (his page, 28 October, 19:02): the street row of production/specs/camera.json, the camera's one
		// home; the switches below still override it for pictures
		{
			TArray<FString> Cands;
			FString Repo, Text;
			if (FParse::Value(Cmd, TEXT("LedgerRepo="), Repo) && !Repo.IsEmpty()) { Cands.Add(FPaths::Combine(Repo, TEXT("production/specs/camera.json"))); }
			Cands.Add(FPaths::ConvertRelativePathToFull(FPaths::Combine(FPaths::ProjectDir(), TEXT("../production/specs/camera.json"))));
			Cands.Add(FPaths::ConvertRelativePathToFull(FPaths::Combine(FPaths::ProjectContentDir(), TEXT("LedgerData/production/specs/camera.json"))));
			for (const FString& C : Cands) { if (FFileHelper::LoadFileToString(Text, *C)) { break; } }
			TSharedPtr<FJsonObject> Root;
			const TSharedPtr<FJsonObject>* Street = nullptr;
			if (Boom != nullptr && !Text.IsEmpty() && FJsonSerializer::Deserialize(TJsonReaderFactory<>::Create(Text), Root) && Root.IsValid()
				&& Root->TryGetObjectField(TEXT("street"), Street))
			{
				double N = 0.0;
				if ((*Street)->TryGetNumberField(TEXT("back_m"), N)) { Boom->TargetArmLength = (float)(N * 100.0); }
				if ((*Street)->TryGetNumberField(TEXT("side_m"), N)) { Boom->SocketOffset.Y = N * 100.0; }
				if ((*Street)->TryGetNumberField(TEXT("up_m"), N)) { Boom->SocketOffset.Z = N * 100.0; }
				if ((*Street)->TryGetNumberField(TEXT("pivot_m"), N)) { Boom->SetRelativeLocation(FVector(0.0, 0.0, N * 100.0 - GetCapsuleComponent()->GetScaledCapsuleHalfHeight())); }
				if (Camera != nullptr && (*Street)->TryGetNumberField(TEXT("lens_deg"), N)) { Camera->SetFieldOfView((float)N); }
			}
			else { UE_LOG(LogTemp, Warning, TEXT("LedgerCamera: no camera.json street row; the arm as built")); }
		}
		if (Boom != nullptr && FParse::Value(Cmd, TEXT("CamBackM="), V)) { Boom->TargetArmLength = (float)(V * 100.0); }
		if (Boom != nullptr && FParse::Value(Cmd, TEXT("CamSideM="), V)) { Boom->SocketOffset.Y = V * 100.0; }
		if (Boom != nullptr && FParse::Value(Cmd, TEXT("CamUpM="), V)) { Boom->SocketOffset.Z = V * 100.0; }
		// The arm hangs from the capsule's middle, 0.88 m above the feet.
		if (Boom != nullptr && FParse::Value(Cmd, TEXT("CamPivotM="), V)) { Boom->SetRelativeLocation(FVector(0.0, 0.0, V * 100.0 - GetCapsuleComponent()->GetScaledCapsuleHalfHeight())); }
		if (Camera != nullptr && FParse::Value(Cmd, TEXT("CamFov="), V)) { Camera->SetFieldOfView((float)V); }
		if (Boom != nullptr) { UE_LOG(LogTemp, Display, TEXT("LedgerCamera: arm %.2f m back, %.2f aside, %.2f up, pivot %.2f m above the feet, lens %.0f"),
			Boom->TargetArmLength / 100.0f, Boom->SocketOffset.Y / 100.0, Boom->SocketOffset.Z / 100.0,
			(Boom->GetRelativeLocation().Z + GetCapsuleComponent()->GetScaledCapsuleHalfHeight()) / 100.0, Camera != nullptr ? Camera->FieldOfView : 0.0f); }
	}
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
	// THE DEFAULT WALK SINCE 26 OCTOBER (his pass by eye on his page, after the third try): Epic's route is on unless
	// -NoGaspMover; -LedgerGaspMover, which switched it on before, is still read and changes nothing
	if (M == nullptr || FParse::Param(FCommandLine::Get(), TEXT("NoGaspMover"))) { return false; }
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
	// -GaspShowMannequin (research, 25 October): the sample's own mannequin is shown, to tell a fault in Epic's
	// clips from one in the copying onto him. Hiding his worn body this way did not take (the first film showed
	// both, the grey mannequin over him); the two still compare frame by frame.
	if (FParse::Param(FCommandLine::Get(), TEXT("GaspShowMannequin")))
	{
		Mover->GetMesh()->SetVisibility(true, false);
		// his body's parts hidden one by one (hiding the worn actor alone left them drawn, 25 October)
		for (USkeletalMeshComponent* P : Parts) { P->SetHiddenInGame(true); P->SetVisibility(false, true); }
	}
	// THE WORN BODY TOUCHES NOTHING (24 October, the first measure: his outfits' bodies blocked the mover's own
	// capsule, which walked a second and stopped while still pushed), and the hidden mannequin keeps its
	// finest level of detail (a hidden mesh's level can go stale, and the body copies it).
	Worn->SetActorEnableCollision(false);
	Mover->MoveIgnoreActorAdd(Worn);
	Mover->GetMesh()->SetForcedLOD(1);
	GaspMover = Mover;
	// HIS CLOTHES ON HIS METAHUMAN (28 October 2026, his page: the zip jacket worn now with drape 19's cuffs, so the
	// walk, the light and the bent elbow are judged while baked cuffs are built): the garments list's pieces for "Tom"
	// follow his body's pose and replace the outfit part they name, as the cast's do (LedgerGarments.h, CrimeProbe.cpp)
	if (!FParse::Param(FCommandLine::Get(), TEXT("NoTomClothes")))
	{
		const int32 Clothes = LedgerGarments::Wear(Worn, TEXT("Tom"));
		TInlineComponentArray<USkeletalMeshComponent*> Dressed;
		Worn->GetComponents(Dressed);
		for (USkeletalMeshComponent* P : Dressed) { P->VisibilityBasedAnimTickOption = EVisibilityBasedAnimTickOption::AlwaysTickPoseAndRefreshBones; }
		UE_LOG(LogTemp, Display, TEXT("LedgerWalk: Tom wears %d garment(s) over his MetaHuman"), Clothes);
	}
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
	const float WasIn = GaspLastIn;
	GaspLastIn = (float)In.Size();
	StopTick(WasIn, (float)In.Size());
	// while he sits (TryStartSit) a push stands him up instead of walking the mover; while he is walked onto an
	// entry (SitApproachTick) a push is only noted, and a push away from the seat ends the approach
	if (SitPhase == ESitPhase::Approaching) { SitPush = In; }
	else if (SitPhase != ESitPhase::None) { if (In.Size() > 0.3) { bSitWantsUp = true; } }
	else if (StopMontage != nullptr) { /* a chosen stop carries him (StopTick) */ }
	else if (!In.IsNearlyZero()) { GaspMover->AddMovementInput(In.GetSafeNormal2D(), FMath::Min(1.0, In.Size())); }
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
	// 25 October (his order of 25 October, item 2, try 2): -GaspPlantSpeed= sets the speed below which a foot counts
	// as planted. The sample's graph makes each clip's contact curve a speed, (1 - contact) * 100, and plants
	// below 1, so only a foot marked above 0.99 is held; motion matching blends clips, and a blended mark often
	// sits just under that. 50 holds any foot marked at least half planted.
	// 26 October: the walk he passed ran at 50, so 50 is the default; -GaspPlantSpeed= still sets another
	static float UnplantCm = -1.0f, UnplantDeg = -1.0f, PlantSpeed = 50.0f;
	static const bool bUnplant = FParse::Value(FCommandLine::Get(), TEXT("GaspUnplantCm="), UnplantCm) | FParse::Value(FCommandLine::Get(), TEXT("GaspUnplantDeg="), UnplantDeg) | FParse::Value(FCommandLine::Get(), TEXT("GaspPlantSpeed="), PlantSpeed) | (PlantSpeed > 0.0f);
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
				if (PlantSpeed > 0.0f) { if (FFloatProperty* S = FindFProperty<FFloatProperty>(Plant->Struct, TEXT("SpeedThreshold"))) { S->SetPropertyValue_InContainer(Settings, PlantSpeed); } }
			}
		}
	}
	// THE SAMPLE'S OWN FOOT PLACEMENT SWITCHED ON IN ITS GRAPH (24 October, the second genuine try: with
	// -GaspFootPlacement=N only): its graph's FootPlacementMode (0 off, 1 its Foot Placement node, 2 its
	// control rig) read 0 in every run, whatever its console setting, so its foot lock never ran
	static int32 GraphFootPlacement = -1;
	static const bool bGraphFoot = FParse::Value(FCommandLine::Get(), TEXT("GaspFootPlacement="), GraphFootPlacement);
	if (bGraphFoot)
	{
		if (UAnimInstance* Graph = GaspMover->GetMesh()->GetAnimInstance())
		{
			if (FIntProperty* Mode = FindFProperty<FIntProperty>(Graph->GetClass(), TEXT("FootPlacementMode"))) { Mode->SetPropertyValue_InContainer(Graph, GraphFootPlacement); }
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
				float Radius = -1.0f, Angle = -1.0f, PlantSpeedNow = -1.0f;
				if (const UAnimInstance* Graph = GaspMover->GetMesh()->GetAnimInstance())
				{
					if (const FStructProperty* Plant = FindFProperty<FStructProperty>(Graph->GetClass(), TEXT("PlantSettings_Default")))
					{
						const void* PS = Plant->ContainerPtrToValuePtr<void>(Graph);
						if (const FFloatProperty* R = FindFProperty<FFloatProperty>(Plant->Struct, TEXT("UnplantRadius"))) { Radius = R->GetPropertyValue_InContainer(PS); }
						if (const FFloatProperty* A = FindFProperty<FFloatProperty>(Plant->Struct, TEXT("UnplantAngle"))) { Angle = A->GetPropertyValue_InContainer(PS); }
						if (const FFloatProperty* S = FindFProperty<FFloatProperty>(Plant->Struct, TEXT("SpeedThreshold"))) { PlantSpeedNow = S->GetPropertyValue_InContainer(PS); }
					}
				}
				int32 GraphMode = -1;
				if (const UAnimInstance* G2 = GaspMover->GetMesh()->GetAnimInstance())
				{
					if (const FIntProperty* Mode = FindFProperty<FIntProperty>(G2->GetClass(), TEXT("FootPlacementMode"))) { GraphMode = Mode->GetPropertyValue_InContainer(G2); }
				}
				Settings = FString::Printf(TEXT(" settings: graphFootPlacement=%d"), GraphMode);
				Settings += FString::Printf(TEXT(" footPlacementMode=%d databaseLevel=%d rootMotionSetting=%d rootMotionUsed=%d unplantCm=%.0f unplantDeg=%.0f"),
					CVarInt(TEXT("DDCvar.FootPlacementMode")), CVarInt(TEXT("DDCvar.MMDatabaseLOD")), CVarInt(TEXT("DDCVar.AttributeBasedRootMotion.Enable")),
					RootMotion != nullptr ? (RootMotion->GetPropertyValue_InContainer(GaspMover.Get()) ? 1 : 0) : -1, Radius, Angle);
				Settings += FString::Printf(TEXT(" plantSpeed=%.0f"), PlantSpeedNow);
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
			// -TomWalkProofGameCam (26 October, his answer: the walk's moments judged by his eye "at the game's
			// camera"): the pictures through the player's own camera instead of the side one
			if (ShotCamera != nullptr) { ShotCamera->GetCameraComponent()->SetFieldOfView(40.0f); if (!FParse::Param(FCommandLine::Get(), TEXT("TomWalkProofGameCam"))) { ShotPC->SetViewTarget(ShotCamera); } }
		}
		// and the game's camera kept behind him as a player steering would keep it (the route turns him, not
		// the camera; the first film looked at him side-on with his feet out of the frame)
		static const bool bGameCam = FParse::Param(FCommandLine::Get(), TEXT("TomWalkProofGameCam"));
		if (bGameCam && ShotPC != nullptr)
		{
			const float Want = GaspMover != nullptr ? GaspMover->GetActorRotation().Yaw : GetActorRotation().Yaw;
			FRotator R = ShotPC->GetControlRotation();
			R.Yaw = FMath::FixedTurn(R.Yaw, Want, 90.0f * DeltaSeconds);
			R.Pitch = -14.0f;
			ShotPC->SetControlRotation(R);
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
				// -TomWalkProofShotStep=s (25 October): pictures every s seconds inside the spans, for moments a
				// tenth of a second cannot settle (a fresh reviewer's three doubtful contacts); 0.1 by default
				static float ShotStep = 0.1f;
				static const bool bStep = FParse::Value(FCommandLine::Get(), TEXT("TomWalkProofShotStep="), ShotStep);
				if (bIn && ProofClock >= NextShotAt - 0.001f)
				{
					FScreenshotRequest::RequestScreenshot(FPaths::ConvertRelativePathToFull(FPaths::ProjectSavedDir() / TEXT("TomWalk")
						/ FString::Printf(TEXT("w%06.3f.png"), ProofClock)), false, false);
					NextShotAt = ProofClock + FMath::Max(ShotStep, 0.001f);
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
		// and how far the mover's body root stands from its capsule (the sample's Offset Root Bone lets the
		// body lag the capsule by up to 30 cm and eases it back when idle: research, 24 October)
		if (B == 1 && GaspMover != nullptr)
		{
			const USkeletalMeshComponent* Man = GaspMover->GetMesh();
			const FVector Root = Man->GetBoneLocation(Man->GetBoneName(0));
			// and what the sample's graph has chosen: its clip, and its own foot placement and root offset switches
			FString Chosen;
			if (const UAnimInstance* G = Man->GetAnimInstance())
			{
				for (const TCHAR* N : { TEXT("CurrentSelectedAnim"), TEXT("FootPlacementMode"), TEXT("OffsetRootBoneEnabled") })
				{
					if (const FProperty* Pr = G->GetClass()->FindPropertyByName(FName(N)))
					{
						FString V;
						Pr->ExportTextItem_Direct(V, Pr->ContainerPtrToValuePtr<void>(G), nullptr, nullptr, PPF_None);
						if (const FObjectPropertyBase* Op = CastField<FObjectPropertyBase>(Pr))
						{
							const UObject* O = Op->GetObjectPropertyValue_InContainer(G);
							V = O != nullptr ? O->GetName() : TEXT("none");
						}
						Chosen += FString::Printf(TEXT(", %s %s"), N, *V);
					}
				}
			}
			ProofLines += FString::Printf(TEXT("traceRoot %.3f: root %.1f,%.1f, capsule %.1f,%.1f, off %.1f cm%s") LINE_TERMINATOR, ProofClock,
				(float)Root.X, (float)Root.Y, (float)GaspMover->GetActorLocation().X, (float)GaspMover->GetActorLocation().Y,
				(float)FVector::Dist2D(Root, GaspMover->GetActorLocation()), *Chosen);
		}
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
void ALedgerSliceCharacter::RequestAct()
{
	// on Epic's route, E by a free seat sits him and E seated stands him (25 October, item 2); else it acts
	if (SitPhase == ESitPhase::Seated) { bSitWantsUp = true; return; }
	// sitting only with -TomSit until it passes (its third try set aside, 26 October: the window seat's sill)
	static const bool bSitOn = FParse::Param(FCommandLine::Get(), TEXT("TomSit"));
	if (bSitOn && GaspMover != nullptr && SitPhase == ESitPhase::None && TryStartSit()) { return; }
	++ActRequests;
}
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

// ---- TOM SITS (his order of 25 October, item 2: "Tom sits down in the game as played") ----------------
// On Epic's route (-LedgerGaspMover): E by a free seat of production/specs/seats.json plays the Game
// Animation Sample's own bench interaction on the mover, as its AC_SmartObjectAnimation and chooser
// CHT_SmartObject_BenchAnim do (production/research/sit-and-turn/WALK-2026-10-25.md, sitting): the approach
// clip by the side he comes from (front within 55 degrees, left 55 to 120, right -55 to -120, behind-left
// and behind-right beyond), started where its remaining walk matches his distance to the seat, warped onto
// the seat by Motion Warping's target "SmartObject" (the clips' own warp window), then its sitting loop
// until he moves or presses E, then its stand-up. The sample's own entry runs through a state tree for a
// player controller, which the puppet mover has not, so the same steps are taken here; its assets are
// unchanged.
namespace LedgerSit
{
	// Kept: the In clips the room test kept for this seat (seats.json "in_kept", the method's step 4)
	// KeptStarts: per kept clip, the start distances (cm of its travel before the seat) the room test passed
	struct FSeat { FString Name; FVector Slot = FVector::ZeroVector; float Yaw = 0.0f; TArray<FString> Kept; TMap<FString, TArray<double>> KeptStarts; };
	// where he must stand for E to sit him (seats.json "room", in the engine's X and Y)
	FBox2D GRoom(ForceInit);

	const TArray<FSeat>& Seats()
	{
		static TArray<FSeat> Out;
		static bool bRead = false;
		if (bRead) { return Out; }
		bRead = true;
		TArray<FString> Cands;
		FString Repo;
		if (FParse::Value(FCommandLine::Get(), TEXT("LedgerRepo="), Repo) && !Repo.IsEmpty()) { Cands.Add(FPaths::Combine(Repo, TEXT("production/specs/seats.json"))); }
		Cands.Add(FPaths::ConvertRelativePathToFull(FPaths::Combine(FPaths::ProjectDir(), TEXT("../production/specs/seats.json"))));
		Cands.Add(FPaths::ConvertRelativePathToFull(FPaths::Combine(FPaths::ProjectContentDir(), TEXT("LedgerData/production/specs/seats.json"))));
		FString Text;
		for (const FString& C : Cands) { if (FFileHelper::LoadFileToString(Text, *C)) { break; } }
		TSharedPtr<FJsonObject> Root;
		const TArray<TSharedPtr<FJsonValue>>* List = nullptr;
		if (!Text.IsEmpty() && FJsonSerializer::Deserialize(TJsonReaderFactory<>::Create(Text), Root) && Root.IsValid() && Root->TryGetArrayField(TEXT("seats"), List))
		{
			const TSharedPtr<FJsonObject>* Room = nullptr;
			if (Root->TryGetObjectField(TEXT("room"), Room) && Room != nullptr)
			{
				GRoom = FBox2D(FVector2D((*Room)->GetNumberField(TEXT("x0")) * 100.0, (*Room)->GetNumberField(TEXT("z0")) * 100.0),
				               FVector2D((*Room)->GetNumberField(TEXT("x1")) * 100.0, (*Room)->GetNumberField(TEXT("z1")) * 100.0));
			}
			for (const TSharedPtr<FJsonValue>& V : *List)
			{
				const TSharedPtr<FJsonObject> S = V->AsObject();
				if (!S.IsValid()) { continue; }
				const double X = S->GetNumberField(TEXT("x")), Y = S->GetNumberField(TEXT("y")), Z = S->GetNumberField(TEXT("z"));
				const double FX = S->GetNumberField(TEXT("face_x")), FZ = S->GetNumberField(TEXT("face_z"));
				FSeat Seat;
				Seat.Name = S->GetStringField(TEXT("name"));
				// street metres to the engine (CrimeProbe.cpp ToUE): X = x*100, Y = z*100, Z = y*100
				Seat.Slot = FVector(X * 100.0, Z * 100.0, Y * 100.0);
				Seat.Yaw = (float)FMath::RadiansToDegrees(FMath::Atan2(FZ - Z, FX - X));
				const TArray<TSharedPtr<FJsonValue>>* Kept = nullptr;
				if (S->TryGetArrayField(TEXT("in_kept"), Kept)) { for (const TSharedPtr<FJsonValue>& K : *Kept) { Seat.Kept.Add(K->AsString()); } }
				const TSharedPtr<FJsonObject>* Starts = nullptr;
				if (S->TryGetObjectField(TEXT("in_kept_starts_cm"), Starts) && Starts != nullptr)
				{
					for (const FString& Name : Seat.Kept)
					{
						const TArray<TSharedPtr<FJsonValue>>* Ds = nullptr;
						if (!(*Starts)->TryGetArrayField(Name, Ds) || Ds == nullptr) { continue; }
						TArray<double>& L = Seat.KeptStarts.Add(Name);
						for (const TSharedPtr<FJsonValue>& D : *Ds) { L.Add(D->AsNumber()); }
					}
				}
				Out.Add(Seat);
			}
		}
		UE_LOG(LogTemp, Log, TEXT("LedgerSit: %d seats read"), Out.Num());
		return Out;
	}

	UAnimMontage* Clip(const FString& Name)
	{
		return LoadObject<UAnimMontage>(nullptr, *FString::Printf(TEXT("/Game/Characters/UEFN_Mannequin/Animations/Interactions/Bench/%s.%s"), *Name, *Name));
	}

	// THE CLIPS AS MEASURED (28 October, the sitting method's step 2; production/specs/seat-clips.json, written by
	// tools/ue/clip_sheet.py): per clip, the root's pose at its start and end and its warp bone's place at the end, in
	// the clip's own frame (cm, degrees), from which an entry is derived instead of placed by hand
	struct FClipPose { bool bOk = false; FTransform RootStart, RootEnd, WarpBoneEnd; };
	FClipPose ClipPose(const FString& Name)
	{
		FClipPose Out;
		TArray<FString> Cands;
		FString Repo;
		if (FParse::Value(FCommandLine::Get(), TEXT("LedgerRepo="), Repo) && !Repo.IsEmpty()) { Cands.Add(FPaths::Combine(Repo, TEXT("production/specs/seat-clips.json"))); }
		Cands.Add(FPaths::ConvertRelativePathToFull(FPaths::Combine(FPaths::ProjectDir(), TEXT("../production/specs/seat-clips.json"))));
		Cands.Add(FPaths::ConvertRelativePathToFull(FPaths::Combine(FPaths::ProjectContentDir(), TEXT("LedgerData/production/specs/seat-clips.json"))));
		FString Text;
		for (const FString& C : Cands) { if (FFileHelper::LoadFileToString(Text, *C)) { break; } }
		TSharedPtr<FJsonObject> Root;
		const TSharedPtr<FJsonObject>* Clips = nullptr;
		const TSharedPtr<FJsonObject>* Clip = nullptr;
		if (Text.IsEmpty() || !FJsonSerializer::Deserialize(TJsonReaderFactory<>::Create(Text), Root) || !Root.IsValid()
			|| !Root->TryGetObjectField(TEXT("clips"), Clips) || !(*Clips)->TryGetObjectField(Name, Clip)) { return Out; }
		auto Pose = [&](const TCHAR* Key, FTransform& T) -> bool
		{
			const TArray<TSharedPtr<FJsonValue>>* A = nullptr;
			if (!(*Clip)->TryGetArrayField(Key, A) || A->Num() < 3) { return false; }
			T = FTransform(FRotator(0.0, (*A)[2]->AsNumber(), 0.0), FVector((*A)[0]->AsNumber(), (*A)[1]->AsNumber(), 0.0));
			return true;
		};
		const TArray<TSharedPtr<FJsonValue>>* B = nullptr;
		double BoneYaw = 0.0;
		(*Clip)->TryGetNumberField(TEXT("warp_bone_end_yaw_deg"), BoneYaw);
		if (Pose(TEXT("root_start"), Out.RootStart) && Pose(TEXT("root_end"), Out.RootEnd)
			&& (*Clip)->TryGetArrayField(TEXT("warp_bone_end_cm"), B) && B->Num() >= 2)
		{
			// the warp bone's end: the root's end moved by its measured offset (in the clip's frame) and turned by its yaw
			Out.WarpBoneEnd = FTransform(FRotator(0.0, Out.RootEnd.Rotator().Yaw + BoneYaw, 0.0),
				Out.RootEnd.GetLocation() + FVector((*B)[0]->AsNumber(), (*B)[1]->AsNumber(), 0.0));
			Out.bOk = true;
		}
		return Out;
	}

	// THE CLIP'S MOMENTS, FOR A START KINGDOM COME II'S WAY (28 October, the sitting method's step 6; read as his chosen
	// stops are, LedgerStop): per 1/30 s of an In clip, the planted foot its contact curves mark, how far through that
	// stance, the root's travel left, and where the mover must stand at that moment for the clip to land on the slot.
	// Only moments inside the room test's envelope are kept (TestedRemainCm of travel left, +-15 cm along).
	constexpr double TestedRemainCm = 150.0;
	// Windows: the start distances the room test passed for the entry; Path: where the mover stands along the clip
	// every 10 cm of its travel (PathLeft: the travel left there), carried onto the room through the slot
	struct FEntry { FString Name; UAnimMontage* Montage = nullptr; float Yaw = 0.0f; FTransform Start; TArray<double> Windows; TArray<FVector> Path; TArray<float> PathLeft; FClipPose Pose; };
	// StanceLeft: how long the clip still marks that foot down after this moment, in seconds
	struct FEntryMoment { int32 Clip = -1; float T = 0.0f; int32 Foot = -1; float Through = -1.0f; float Left = 0.0f; float StanceLeft = 0.0f; FTransform MoverAt; };
	TArray<FEntry> GEntries;
	TArray<FEntryMoment> GMoments;
	int32 GBest = -1, GStage = 0;
	FVector GPre = FVector::ZeroVector;
	// how the last approach ended, for the approach test: "started", "fallback: ...", "left"
	FString GLastApproach;
	float GLastHeadingOff = -1.0f;
	// the approach's near misses, for its log: frames on the last metre, frames with some moment's place in the
	// envelope, of those with his foot, and the smallest stance gap seen with his foot in the envelope
	int32 GFramesOnLine = 0, GFramesInPlace = 0, GFramesFootToo = 0;
	float GBestGap = 1.0f;
	// THE START MEASURED (29 October, the start-chooser review's check): the planted foot's slide while the clip
	// still marks it down after a matched start, and the attach bone and hips once seated
	int32 GStartFoot = -1;
	FVector GStartFootAt = FVector::ZeroVector;
	float GSlideCm = -1.0f, GBoneCm = -1.0f, GBoneYaw = 0.0f, GHipsCm = -1.0f, GHipsUpCm = -1.0f;
	// until when the started moment's foot is still down by the clip's own table (29 October: read from the graph's
	// contact curve, the first measure followed the foot through the rest of the walk, 39 to 85 cm)
	float GSlideUntil = 0.0f;
	// the stand-up's contacts with the room (step 9), this one's and the last one's
	int32 GOutContacts = 0, GLastOut = -1;
	FString GOutFirst;
	// the chooser's frames on the path, and its best cost there, in a tested band or anywhere
	int32 GChooserFrames = 0;
	float GBestCostAny = 100.0f, GBestCostInBand = 100.0f;

	// where the mover stands at moment T of a clip whose warp bone ends on Slot (the derivation of step 3)
	FTransform MoverAtMoment(UAnimMontage* Entry, const FClipPose& P, const FTransform& Slot, const FTransform& MeshRel, float T)
	{
		const FTransform Moved = Entry->ExtractRootMotionFromTrackRange(0.0f, T, FAnimExtractContext());
		return MeshRel.Inverse() * ((Moved * P.RootStart) * (P.WarpBoneEnd.Inverse() * Slot));
	}

	// the moment where Remain cm of the clip's own travel is left
	float MomentWithLeft(UAnimMontage* Entry, double Remain)
	{
		const float Len = Entry->GetPlayLength();
		float Start = 0.0f, Best = 1e9f;
		for (float Tm = 0.0f; Tm < Len; Tm += 1.0f / 30.0f)
		{
			const float Err = FMath::Abs((float)Entry->ExtractRootMotionFromTrackRange(Tm, Len, FAnimExtractContext()).GetTranslation().Size2D() - (float)Remain);
			if (Err < Best) { Best = Err; Start = Tm; }
		}
		return Start;
	}

	void ReadMoments(int32 ClipIndex, const FClipPose& P, const FTransform& Slot, const FTransform& MeshRel, float LeftMin, float LeftMax)
	{
		UAnimMontage* Entry = GEntries[ClipIndex].Montage;
		UAnimSequence* Seq = nullptr;
		float SeqFrom = 0.0f, SegStart = 0.0f, Rate = 1.0f;
		if (Entry->SlotAnimTracks.Num() > 0 && Entry->SlotAnimTracks[0].AnimTrack.AnimSegments.Num() > 0)
		{
			const FAnimSegment& Seg = Entry->SlotAnimTracks[0].AnimTrack.AnimSegments[0];
			Seq = Cast<UAnimSequence>(Seg.GetAnimReference().Get());
			SeqFrom = Seg.AnimStartTime; SegStart = Seg.StartPos; Rate = Seg.AnimPlayRate;
		}
		if (Seq == nullptr) { UE_LOG(LogTemp, Warning, TEXT("LedgerSit: %s has no sequence to read its feet from"), *GEntries[ClipIndex].Name); return; }
		const float Len = Entry->GetPlayLength(), Step = 1.0f / 30.0f;
		TArray<float> Cv[2];
		for (float T = 0.0f; T <= Len; T += Step)
		{
			const double At = SeqFrom + (T - SegStart) * Rate;
			for (int32 F = 0; F < 2; ++F) { Cv[F].Add(Seq->EvaluateCurveData(FName(F == 0 ? TEXT("contact_l") : TEXT("contact_r")), FAnimExtractContext(At))); }
		}
		const int32 N = Cv[0].Num();
		for (int32 I = 0; I < N; ++I)
		{
			FEntryMoment M;
			M.Clip = ClipIndex;
			M.T = I * Step;
			M.Left = (float)Entry->ExtractRootMotionFromTrackRange(M.T, Len, FAnimExtractContext()).GetTranslation().Size2D();
			if (M.Left < LeftMin || M.Left > LeftMax) { continue; }
			// the planted foot: the one marked down; in double support, the one that came down last (as LedgerStop)
			int32 Down[2] = { 0, 0 };
			for (int32 F = 0; F < 2; ++F) { for (int32 J = I; J >= 0 && Cv[F][J] > 0.5f; --J) { ++Down[F]; } }
			if (Down[0] > 0 && (Down[1] == 0 || Down[0] <= Down[1])) { M.Foot = 0; }
			else if (Down[1] > 0) { M.Foot = 1; }
			if (M.Foot < 0) { continue; }
			int32 Up = 0;
			for (int32 J = I + 1; J < N && Cv[M.Foot][J] > 0.5f; ++J) { ++Up; }
			M.Through = (float)Down[M.Foot] / (float)FMath::Max(1, Down[M.Foot] + Up);
			M.StanceLeft = Up * Step;
			M.MoverAt = MoverAtMoment(Entry, P, Slot, MeshRel, M.T);
			GMoments.Add(M);
		}
	}

	// THE SAMPLE'S OWN CHOOSER (29 October, sitting's third try; production/research/sit-and-turn/START-CHOOSER-2026-10-29.md,
	// reviewed and revised): Epic's bench table CHT_SmartObject_BenchAnim, given the side's angle, his root's distance to
	// the slot and his pose history, returns the In montage and the moment whose feet (positions and velocities) best
	// match his, with its cost; the sample plays at a cost of at most 1.0 and otherwise tries the next frame. The table
	// reads its context in this order: the anim instance, SmartObjectSelectionInputs (TargetDistance, TargetAngle,
	// PoseHistoryNode), SmartObjectSelectionOutputs (StartTime, Cost). Its user-made structs' field names carry suffixes,
	// so each is found by the start of its name.
	struct FChooser
	{
		const UChooserTable* Table = nullptr;
		const UUserDefinedStruct* InType = nullptr;
		const UUserDefinedStruct* OutType = nullptr;
		FProperty* Distance = nullptr;
		FProperty* Angle = nullptr;
		FProperty* History = nullptr;
		FProperty* StartTime = nullptr;
		FProperty* Cost = nullptr;
		TArray<uint8> In, Out;
		bool bOk = false;
	};
	FChooser& TheChooser()
	{
		static FChooser C;
		static bool bTried = false;
		if (bTried) { return C; }
		bTried = true;
		C.Table = LoadObject<UChooserTable>(nullptr, TEXT("/Game/Blueprints/SmartObjects/Bench/CHT_SmartObject_BenchAnim.CHT_SmartObject_BenchAnim"));
		C.InType = LoadObject<UUserDefinedStruct>(nullptr, TEXT("/Game/Blueprints/SmartObjects/SmartObjectSelectionInputs.SmartObjectSelectionInputs"));
		C.OutType = LoadObject<UUserDefinedStruct>(nullptr, TEXT("/Game/Blueprints/SmartObjects/SmartObjectSelectionOutputs.SmartObjectSelectionOutputs"));
		auto Find = [](const UStruct* S, const TCHAR* Prefix) -> FProperty*
		{
			for (TFieldIterator<FProperty> It(S); It; ++It) { if (It->GetName().StartsWith(Prefix)) { return *It; } }
			return nullptr;
		};
		if (C.Table != nullptr && C.InType != nullptr && C.OutType != nullptr)
		{
			C.Distance = Find(C.InType, TEXT("TargetDistance"));
			C.Angle = Find(C.InType, TEXT("TargetAngle"));
			C.History = Find(C.InType, TEXT("PoseHistory"));
			C.StartTime = Find(C.OutType, TEXT("StartTime"));
			C.Cost = Find(C.OutType, TEXT("Cost"));
			C.In.SetNumZeroed(C.InType->GetStructureSize());
			C.InType->InitializeStruct(C.In.GetData());
			C.Out.SetNumZeroed(C.OutType->GetStructureSize());
			C.OutType->InitializeStruct(C.Out.GetData());
			const FStructProperty* H = CastField<FStructProperty>(C.History);
			C.bOk = CastField<FNumericProperty>(C.Distance) != nullptr && CastField<FNumericProperty>(C.Angle) != nullptr
				&& H != nullptr && H->Struct == FPoseHistoryReference::StaticStruct()
				&& CastField<FNumericProperty>(C.StartTime) != nullptr && CastField<FNumericProperty>(C.Cost) != nullptr;
		}
		UE_LOG(LogTemp, Display, TEXT("LedgerSit: the sample's chooser %s (table %d, inputs %d, outputs %d; distance %d, angle %d, history %d, start %d, cost %d)"),
			C.bOk ? TEXT("ready") : TEXT("NOT READY"), C.Table != nullptr, C.InType != nullptr, C.OutType != nullptr, C.Distance != nullptr, C.Angle != nullptr,
			C.History != nullptr, C.StartTime != nullptr, C.Cost != nullptr);
		return C;
	}

	// the side's angle as the table reads it (degrees; its rows: F -55 to 55, L_090 55 to 120, R_090 -120 to -55,
	// BL 120 to 180, BR -180 to -120), the middle of the kept entry's range, so the room-tested side is the one searched
	double SideAngle(const FString& Clip)
	{
		if (Clip.Contains(TEXT("_L_090_"))) { return 90.0; }
		if (Clip.Contains(TEXT("_R_090_"))) { return -90.0; }
		if (Clip.Contains(TEXT("_BL_"))) { return 150.0; }
		if (Clip.Contains(TEXT("_BR_"))) { return -150.0; }
		return 0.0;
	}

	// One evaluation: the montage the table picks, its moment and cost; nullptr when nothing is picked
	UAnimMontage* Choose(UAnimInstance* Graph, double DistanceCm, double AngleDeg, float& OutStart, float& OutCost)
	{
		FChooser& C = TheChooser();
		OutStart = 0.0f; OutCost = 100.0f;
		if (!C.bOk || Graph == nullptr) { return nullptr; }
		const FAnimNode_PoseSearchHistoryCollector_Base* Node = UPoseSearchLibrary::FindPoseHistoryNode(FName(TEXT("PoseHistory")), Graph);
		if (Node == nullptr) { return nullptr; }
		CastField<FNumericProperty>(C.Distance)->SetFloatingPointPropertyValue(C.Distance->ContainerPtrToValuePtr<void>(C.In.GetData()), DistanceCm);
		CastField<FNumericProperty>(C.Angle)->SetFloatingPointPropertyValue(C.Angle->ContainerPtrToValuePtr<void>(C.In.GetData()), AngleDeg);
		*C.History->ContainerPtrToValuePtr<FPoseHistoryReference>(C.In.GetData()) = Node->GetPoseHistoryReference();
		CastField<FNumericProperty>(C.StartTime)->SetFloatingPointPropertyValue(C.StartTime->ContainerPtrToValuePtr<void>(C.Out.GetData()), 0.0);
		CastField<FNumericProperty>(C.Cost)->SetFloatingPointPropertyValue(C.Cost->ContainerPtrToValuePtr<void>(C.Out.GetData()), 100.0);
		FChooserEvaluationContext Ctx;
		Ctx.AddObjectParam(Graph);
		Ctx.AddStructViewParam(FStructView(C.InType, C.In.GetData()));
		Ctx.AddStructViewParam(FStructView(C.OutType, C.Out.GetData()));
		UObject* Got = UChooserFunctionLibrary::EvaluateObjectChooserBase(Ctx, UChooserFunctionLibrary::MakeEvaluateChooser(const_cast<UChooserTable*>(C.Table)), UAnimMontage::StaticClass());
		OutStart = (float)CastField<FNumericProperty>(C.StartTime)->GetFloatingPointPropertyValue(C.StartTime->ContainerPtrToValuePtr<void>(C.Out.GetData()));
		OutCost = (float)CastField<FNumericProperty>(C.Cost)->GetFloatingPointPropertyValue(C.Cost->ContainerPtrToValuePtr<void>(C.Out.GetData()));
		return Cast<UAnimMontage>(Got);
	}

	// how near E reaches a seat; the seat must be in sight and nobody on it (Ron's evening seat is the middle one)
	constexpr double ReachCm = 160.0;
	FCollisionResponseContainer GSavedResponses;
}

bool ALedgerSliceCharacter::TryStartSit()
{
	if (GaspMover == nullptr || SitPhase != ESitPhase::None) { return false; }
	const FVector At = GaspMover->GetActorLocation();
	const LedgerSit::FSeat* Best = nullptr;
	double BestD = 1e9;
	for (const LedgerSit::FSeat& S : LedgerSit::Seats())
	{
		const double D = FVector::Dist2D(At, S.Slot);
		if (D >= BestD || D > LedgerSit::ReachCm) { continue; }
		// nobody else on it (his own worn body rides on the mover, so anything attached to the mover is his)
		bool bTaken = false;
		for (TActorIterator<ACharacter> It(GetWorld()); It; ++It)
		{
			if (*It == GaspMover || *It == this || It->GetAttachParentActor() == GaspMover || It->GetOwner() == GaspMover) { continue; }
			if (FVector::Dist2D(It->GetActorLocation(), S.Slot) < 40.0) { bTaken = true; }
		}
		// in the room: he stands on the office's public side (never a seat through a wall or the window; a
		// line traced to the seat was stopped by the room's own meshes, 25 October)
		const bool bOutside = LedgerSit::GRoom.bIsValid && !LedgerSit::GRoom.IsInside(FVector2D(At.X, At.Y));
		if (bTaken || bOutside)
		{
			UE_LOG(LogTemp, Display, TEXT("LedgerSit: %s passed over at %.0f cm: %s"), *S.Name, D, bTaken ? TEXT("someone is on it") : TEXT("he is not in its room"));
			continue;
		}
		BestD = D; Best = &S;
	}
	if (Best == nullptr) { UE_LOG(LogTemp, Display, TEXT("LedgerSit: no free seat within %.0f cm of (%.0f, %.0f)"), LedgerSit::ReachCm, At.X, At.Y); return false; }
	// THE METHOD'S STEPS 5 AND 6 where the seat's entries were room-tested: the kept entry nearest his heading, walked
	// onto and started on his own foot (TryStartSitApproach), with -TomSitApproach; the start below is the default and
	// the approach's fallback
	// Since 29 October the approach is set aside after two designs, two tries each (DECISIONS.md): the plain start below
	// is the default and -TomSitApproach brings the approach back for its tests (-TomSitApproachTest)
	static const bool bApproach = FParse::Param(FCommandLine::Get(), TEXT("TomSitApproach")) || FParse::Param(FCommandLine::Get(), TEXT("TomSitApproachTest"));
	if (bApproach && !bSitNoApproach && Best->Kept.Num() > 0) { return TryStartSitApproach((int32)(Best - LedgerSit::Seats().GetData())); }
	SitSlot =FTransform(FRotator(0.0f, Best->Yaw, 0.0f), Best->Slot);
	const FVector Rel = SitSlot.InverseTransformPosition(At);
	const float Angle = (float)FMath::RadiansToDegrees(FMath::Atan2(Rel.Y, Rel.X));
	const FString Side = FMath::Abs(Angle) <= 55.0f ? TEXT("F") : (Angle > 55.0f && Angle <= 120.0f ? TEXT("L_090")
		: (Angle < -55.0f && Angle >= -120.0f ? TEXT("R_090") : (Angle > 0.0f ? TEXT("BL") : TEXT("BR"))));
	// the clip that leads with the foot now in the air (the sample picks the foot by pose search)
	USkeletalMeshComponent* MM = GaspMover->GetMesh();
	const bool bLeftUp = MM->GetSocketLocation(TEXT("ball_l")).Z > MM->GetSocketLocation(TEXT("ball_r")).Z;
	const bool bBack = Side.StartsWith(TEXT("B"));
	const FString Name = FString::Printf(TEXT("M_interaction_bench_into_%s_%s_Montage"), *Side,
		bLeftUp ? (bBack ? TEXT("LFoot") : TEXT("Lfoot")) : (bBack ? TEXT("RFoot") : TEXT("Rfoot")));
	UAnimMontage* Entry = LedgerSit::Clip(Name);
	UAnimInstance* Graph = MM->GetAnimInstance();
	if (Entry == nullptr || Graph == nullptr)
	{
		UE_LOG(LogTemp, Warning, TEXT("LedgerSit: no clip %s or no graph"), *Name);
		return false;
	}
	// FROM THE CLIP'S BEGINNING (his answer of 26 October, the sit's third try): the first two tries started
	// it where its remaining walk matched his distance (1.80 s in), and a fresh reviewer failed the sit-down
	// (a foot held in the air, the head folding), as Epic's own mannequin showed too; the sample plays it from
	// its start and lets the warp window bend the approach. -TomSitMatchStart keeps the old way to compare.
	const float Len = Entry->GetPlayLength();
	float Start = 0.0f, BestErr = 0.0f;
	if (FParse::Param(FCommandLine::Get(), TEXT("TomSitMatchStart")))
	{
		BestErr = 1e9f;
		for (float T = 0.0f; T < Len * 0.9f; T += 1.0f / 30.0f)
		{
			const FTransform Rest = Entry->ExtractRootMotionFromTrackRange(T, Len, FAnimExtractContext());
			const float Err = FMath::Abs((float)Rest.GetTranslation().Size2D() - (float)BestD);
			if (Err < BestErr) { BestErr = Err; Start = T; }
		}
	}
	if (UMotionWarpingComponent* Warp = GaspMover->FindComponentByClass<UMotionWarpingComponent>())
	{
		Warp->AddOrUpdateWarpTargetFromTransform(FName(TEXT("SmartObject")), SitSlot);
	}
	else
	{
		UE_LOG(LogTemp, Warning, TEXT("LedgerSit: the mover has no motion warping component; the clip is not placed"));
	}
	// THE BENCH'S COLLISION AND GRAVITY OFF while the clip carries him onto it (the sample ignores the bench)
	UCapsuleComponent* Cap = GaspMover->GetCapsuleComponent();
	LedgerSit::GSavedResponses = Cap->GetCollisionResponseToChannels();
	Cap->SetCollisionResponseToChannel(ECC_WorldStatic, ECR_Ignore);
	Cap->SetCollisionResponseToChannel(ECC_WorldDynamic, ECR_Ignore);
	GaspMover->GetCharacterMovement()->SetMovementMode(MOVE_Flying);
	Graph->Montage_Play(Entry, 1.0f, EMontagePlayReturnType::MontageLength, Start);
	SitMontage = Entry;
	SitPhase = ESitPhase::Entering;
	SitPhaseAt = SitClock;
	bSitWantsUp = false;
	UE_LOG(LogTemp, Display, TEXT("LedgerSit: %s, from %.0f cm at %.0f degrees: %s from %.2f s of %.2f (its walk off by %.0f cm)"),
		*Best->Name, BestD, Angle, *Name, Start, Len, BestErr);
	// the clip's own warp windows, and how far its root still travels after the last one ends
	for (const FAnimNotifyEvent& N : Entry->Notifies)
	{
		const UAnimNotifyState* State = N.NotifyStateClass.Get();
		if (State != nullptr && State->GetClass()->GetName().Contains(TEXT("MotionWarping")))
		{
			const float End = N.GetTriggerTime() + N.GetDuration();
			const FVector After = Entry->ExtractRootMotionFromTrackRange(End, Len, FAnimExtractContext()).GetTranslation();
			UE_LOG(LogTemp, Display, TEXT("LedgerSit: warp window %.2f to %.2f s; after it the root moves %.1f cm (%.1f, %.1f)"), N.GetTriggerTime(), End, After.Size2D(), After.X, After.Y);
		}
	}
	return true;
}

// THE ENTRY DERIVED, NEVER PLACED (28 October, the sitting method's step 3): the clip's own frame is carried onto the
// world so that its warp bone's end lands on the seat's slot (the transform the warp would aim it at); the clip's start
// frame, carried the same way, is where the mover's mesh must begin. The warp is taken off, so where the bone really
// lands checks the derivation, not the warp. The mesh's own offset on the mover is undone to place the mover itself.
bool ALedgerSliceCharacter::StartSitFromEntry(const FString& ClipName)
{
	if (GaspMover == nullptr || SitPhase != ESitPhase::None || LedgerSit::Seats().Num() == 0) { return false; }
	const LedgerSit::FClipPose P = LedgerSit::ClipPose(ClipName);
	UAnimMontage* Entry = LedgerSit::Clip(ClipName);
	USkeletalMeshComponent* MM = GaspMover->GetMesh();
	UAnimInstance* Graph = MM != nullptr ? MM->GetAnimInstance() : nullptr;
	if (!P.bOk || Entry == nullptr || Graph == nullptr)
	{
		UE_LOG(LogTemp, Warning, TEXT("LedgerSit: entry test %s: no measures, clip or graph"), *ClipName);
		return false;
	}
	const LedgerSit::FSeat& S = LedgerSit::Seats()[0];
	SitSlot = FTransform(FRotator(0.0f, S.Yaw, 0.0f), S.Slot);
	const FTransform ClipToWorld = P.WarpBoneEnd.Inverse() * SitSlot;
	const FTransform MeshStart = P.RootStart * ClipToWorld;
	const FTransform MoverStart = MM->GetRelativeTransform().Inverse() * MeshStart;
	GaspMover->SetActorLocationAndRotation(MoverStart.GetLocation(), FRotator(0.0f, MoverStart.Rotator().Yaw, 0.0f), false, nullptr, ETeleportType::TeleportPhysics);
	if (UMotionWarpingComponent* Warp = GaspMover->FindComponentByClass<UMotionWarpingComponent>()) { Warp->RemoveWarpTarget(FName(TEXT("SmartObject"))); }
	UCapsuleComponent* Cap = GaspMover->GetCapsuleComponent();
	LedgerSit::GSavedResponses = Cap->GetCollisionResponseToChannels();
	Cap->SetCollisionResponseToChannel(ECC_WorldStatic, ECR_Ignore);
	Cap->SetCollisionResponseToChannel(ECC_WorldDynamic, ECR_Ignore);
	GaspMover->GetCharacterMovement()->SetMovementMode(MOVE_Flying);
	Graph->Montage_Play(Entry, 1.0f, EMontagePlayReturnType::MontageLength, 0.0f);
	SitMontage = Entry;
	SitPhase = ESitPhase::Entering;
	SitPhaseAt = SitClock;
	bSitWantsUp = false;
	UE_LOG(LogTemp, Display, TEXT("LedgerSit: entry test %s from (%.0f, %.0f) facing %.0f, %.0f cm from the slot, the warp off"),
		*ClipName, MoverStart.GetLocation().X, MoverStart.GetLocation().Y, MoverStart.Rotator().Yaw, FVector::Dist2D(MoverStart.GetLocation(), S.Slot));
	return true;
}

// STEP 5, THE CHOICE (28 October, the sitting method; production/research/sit-and-turn/SPOTS-2026-10-28.md): each kept
// entry's direction is the way the mover faces at its room-tested start (TestedRemainCm of its travel left); the one
// nearest his heading is taken (the check: within 20 degrees), with its side's other foot beside it. Then the approach
// (SitApproachTick) walks him onto the clip's own path, carried onto the room through the slot, and along it.
// Try 2 (28 October, late): the start is sought in every distance the room test passed for the entry
// (seats.json in_kept_starts_cm), not one 30 cm window; in try 1 his stride was 50 to 100 points out of step with the
// clip's in that window on every walk-in, so no start was found and all seven sits took the fallback.
bool ALedgerSliceCharacter::TryStartSitApproach(int32 SeatIndex)
{
	using namespace LedgerSit;
	const FSeat& S = Seats()[SeatIndex];
	USkeletalMeshComponent* MM = GaspMover->GetMesh();
	SitSlot = FTransform(FRotator(0.0f, S.Yaw, 0.0f), S.Slot);
	const FTransform MeshRel = MM->GetRelativeTransform();
	// his heading: where the mover goes, or where it faces when still
	const FVector V = GaspMover->GetVelocity();
	const float Heading = V.Size2D() > 30.0 ? (float)V.Rotation().Yaw : (float)GaspMover->GetActorRotation().Yaw;
	GEntries.Reset(); GMoments.Reset(); GBest = -1; GStage = 0;
	GFramesOnLine = GFramesInPlace = GFramesFootToo = 0; GBestGap = 1.0f;
	GChooserFrames = 0; GBestCostAny = GBestCostInBand = 100.0f;
	float BestOff = 1e9f;
	TArray<FClipPose> Poses;
	for (const FString& Name : S.Kept)
	{
		const FClipPose P = ClipPose(Name);
		UAnimMontage* Entry = Clip(Name);
		if (!P.bOk || Entry == nullptr) { UE_LOG(LogTemp, Warning, TEXT("LedgerSit: kept entry %s has no measures or clip"), *Name); continue; }
		FEntry E;
		E.Name = Name;
		E.Montage = Entry;
		E.Start = MoverAtMoment(Entry, P, SitSlot, MeshRel, MomentWithLeft(Entry, TestedRemainCm));
		E.Yaw = (float)E.Start.Rotator().Yaw;
		E.Windows = S.KeptStarts.FindRef(Name);
		E.Pose = P;
		if (E.Windows.Num() == 0) { E.Windows.Add(TestedRemainCm); }
		E.Windows.Sort();
		const int32 I = GEntries.Add(E);
		Poses.Add(P);
		const float Off = (float)FMath::Abs(FRotator::NormalizeAxis((double)(E.Yaw - Heading)));
		if (Off < BestOff) { BestOff = Off; GBest = I; }
	}
	if (GBest < 0)
	{
		GLastApproach = TEXT("fallback: no kept entry readable");
		bSitNoApproach = true; const bool b = TryStartSit(); bSitNoApproach = false;
		return b;
	}
	// the moments of the chosen side (its entries within 15 degrees of the chosen one's direction: the other foot), in
	// each distance the room test passed for that entry, 15 cm either way
	for (int32 I = 0; I < GEntries.Num(); ++I)
	{
		if (FMath::Abs(FRotator::NormalizeAxis((double)(GEntries[I].Yaw - GEntries[GBest].Yaw))) > 15.0) { continue; }
		for (const double W : GEntries[I].Windows) { ReadMoments(I, Poses[I], SitSlot, MeshRel, (float)W - 15.0f, (float)W + 15.0f); }
	}
	// THE PATH: where the mover stands along the chosen clip, every 10 cm of its travel, from a metre beyond its
	// farthest tested start to 20 cm short of its nearest; he joins it at the farthest point his capsule fits
	FEntry& B = GEntries[GBest];
	const double Far = B.Windows.Last(), Near = B.Windows[0];
	const FVector Pos = GaspMover->GetActorLocation();
	for (double L = Far + 100.0; L >= Near - 20.0; L -= 10.0)
	{
		FVector At = MoverAtMoment(B.Montage, Poses[GBest], SitSlot, MeshRel, MomentWithLeft(B.Montage, L)).GetLocation();
		At.Z = Pos.Z;
		B.Path.Add(At);
		B.PathLeft.Add((float)L);
	}
	FCollisionQueryParams Q(FName(TEXT("LedgerSitApproach")), false);
	Q.AddIgnoredActor(this);
	Q.AddIgnoredActor(GaspMover);
	TArray<AActor*> Riders;
	GaspMover->GetAttachedActors(Riders, true, true);
	Q.AddIgnoredActors(Riders);
	const UCapsuleComponent* Cap = GaspMover->GetCapsuleComponent();
	const FCollisionShape Shape = FCollisionShape::MakeCapsule(Cap->GetScaledCapsuleRadius(), Cap->GetScaledCapsuleHalfHeight());
	int32 Join = -1;
	for (int32 I = 0; I < B.Path.Num() && B.PathLeft[I] >= Far + 20.0f; ++I)
	{
		const bool bInRoom = !GRoom.bIsValid || GRoom.IsInside(FVector2D(B.Path[I].X, B.Path[I].Y));
		if (bInRoom && !GetWorld()->OverlapAnyTestByChannel(B.Path[I] + FVector(0.0, 0.0, 2.0), FQuat::Identity, ECC_WorldStatic, Shape, Q)) { Join = I; break; }
	}
	GLastHeadingOff = BestOff;
	GPre = Join >= 0 ? B.Path[Join] : FVector::ZeroVector;
	FString Wins;
	for (const double W : B.Windows) { Wins += FString::Printf(TEXT("%s%.0f"), Wins.IsEmpty() ? TEXT("") : TEXT(", "), W); }
	UE_LOG(LogTemp, Display, TEXT("LedgerSit: step 5, %s for %s: his heading %.0f, the entry's %.0f, %.0f off (%s); %d moments on its side in its tested starts (%s cm); he joins its path at (%.0f, %.0f), %.0f cm of its walk left%s"),
		*B.Name, *S.Name, Heading, B.Yaw, BestOff, BestOff <= 20.0f ? TEXT("within 20") : TEXT("OVER 20, the approach turns him"), GMoments.Num(), *Wins,
		GPre.X, GPre.Y, Join >= 0 ? B.PathLeft[Join] : -1.0f, Join >= 0 ? TEXT("") : TEXT(", NO CLEAR PLACE to join it"));
	if (Join < 0 || GMoments.Num() == 0)
	{
		GLastApproach = Join >= 0 ? TEXT("fallback: no moments") : TEXT("fallback: no room to join the path");
		bSitNoApproach = true; const bool b = TryStartSit(); bSitNoApproach = false;
		return b;
	}
	SitPhase = ESitPhase::Approaching;
	SitPhaseAt = SitClock;
	SitPush = FVector::ZeroVector;
	bSitWantsUp = false;
	GLastApproach = TEXT("approaching");
	return true;
}

// HIS FOOT AS THE PLAYER SEES IT (29 October: the slide read on the hidden mover's mesh tracked the body's travel, 40 to
// 158 cm; the visible MetaHuman body is what is judged): the ball of the foot on his worn body, else on the mover
FVector ALedgerSliceCharacter::SitFootAt(int32 Foot, bool bMover) const
{
	const TCHAR* Bone = Foot == 0 ? TEXT("ball_l") : TEXT("ball_r");
	if (!bMover && WornBody != nullptr && WornBody->DoesSocketExist(FName(Bone))) { return WornBody->GetSocketLocation(FName(Bone)); }
	return GaspMover->GetMesh()->GetSocketLocation(FName(Bone));
}

// STEP 6, THE APPROACH AND THE START (Kingdom Come II's way, as his chosen stops): steered to where he joins the clip's
// path, then along it (60 cm of its walk ahead of the nearest point); on the path each frame looks for a moment of the
// chosen side's clips with his planted foot, its stance within 10 points of his, and his place within the tested
// envelope of where the mover would stand then (15 cm along, 10 across, 20 degrees). Found, the clip plays from that
// moment, blended in over 0.2 s, the warp on. Past the nearest tested start or after 8 s without one: the old start.
void ALedgerSliceCharacter::SitApproachTick(float DeltaSeconds)
{
	using namespace LedgerSit;
	if (GBest < 0 || !GEntries.IsValidIndex(GBest) || GEntries[GBest].Path.Num() == 0) { SitPhase = ESitPhase::None; return; }
	const FEntry& B = GEntries[GBest];
	const FVector Pos = GaspMover->GetActorLocation();
	const float Yaw = (float)GaspMover->GetActorRotation().Yaw;
	// a push away from the seat ends the approach; he walks on as he wishes
	if (SitPush.Size() > 0.3 && FVector::DotProduct(SitPush.GetSafeNormal2D(), (SitSlot.GetLocation() - Pos).GetSafeNormal2D()) < 0.0)
	{
		UE_LOG(LogTemp, Display, TEXT("LedgerSit: approach left (a push away)"));
		GLastApproach = TEXT("left");
		SitPhase = ESitPhase::None;
		return;
	}
	// where he is on the path: its nearest point
	int32 Nearest = 0;
	double NearestD = 1e12;
	for (int32 I = 0; I < B.Path.Num(); ++I)
	{
		const double D2 = FVector::DistSquared2D(Pos, B.Path[I]);
		if (D2 < NearestD) { NearestD = D2; Nearest = I; }
	}
	if (GStage == 0 && FVector::Dist2D(Pos, GPre) < 25.0) { GStage = 1; }
	if (GStage == 1)
	{
		++GFramesOnLine;
		// his planted foot and how far through its stance (StopTick keeps both, from his own contact curves)
		int32 Foot = -1;
		if (ContactFor[0] > 0.0f && (ContactFor[1] <= 0.0f || ContactFor[0] <= ContactFor[1])) { Foot = 0; }
		else if (ContactFor[1] > 0.0f) { Foot = 1; }
		// THE THIRD TRY, THE SAMPLE'S OWN SEARCH (29 October): each frame on the path the bench table picks the clip and
		// the moment whose feet match his; it plays when the cost is at most 1.0, the clip is one this seat kept, and the
		// moment's travel left lies inside a distance the room test passed (15 cm either way); else the next frame.
		// -TomSitTableStart keeps the table start of the first two tries, for comparison.
		static const bool bTable = FParse::Param(FCommandLine::Get(), TEXT("TomSitTableStart"));
		UAnimInstance* ChooserGraph = GaspMover->GetMesh()->GetAnimInstance();
		if (!bTable && TheChooser().bOk && ChooserGraph != nullptr)
		{
			const double Dist = FVector::Dist2D(GaspMover->GetMesh()->GetComponentLocation(), SitSlot.GetLocation());
			float St = 0.0f, Cost = 100.0f;
			UAnimMontage* Got = Choose(ChooserGraph, Dist, SideAngle(B.Name), St, Cost);
			++GChooserFrames;
			GBestCostAny = FMath::Min(GBestCostAny, Cost);
			int32 Ei = INDEX_NONE;
			for (int32 I = 0; I < GEntries.Num(); ++I) { if (GEntries[I].Montage == Got) { Ei = I; } }
			if (Ei != INDEX_NONE)
			{
				const float Left = (float)Got->ExtractRootMotionFromTrackRange(St, Got->GetPlayLength(), FAnimExtractContext()).GetTranslation().Size2D();
				bool bInBand = false;
				for (const double W : GEntries[Ei].Windows) { bInBand |= FMath::Abs(Left - (float)W) <= 15.0f; }
				// TRY 2 OF THIS DESIGN (29 October, 03:25: the first try's starts slid 3 to 35 cm, the worst where he stood
				// 43 cm farther from the seat than the chosen moment's own root stands from its attach bone, a gap the warp
				// stretches out of his step): his distance must match the moment's own, root to attach bone, within 15 cm
				const FClipPose& CP = GEntries[Ei].Pose;
				const FTransform RootAtT = Got->ExtractRootMotionFromTrackRange(0.0f, St, FAnimExtractContext()) * CP.RootStart;
				const float ClipDist = (float)FVector::Dist2D(RootAtT.GetLocation(), CP.WarpBoneEnd.GetLocation());
				bInBand = bInBand && CP.bOk && FMath::Abs((float)Dist - ClipDist) <= 15.0f;
				if (bInBand) { GBestCostInBand = FMath::Min(GBestCostInBand, Cost); }
				if (bInBand && Cost <= 1.0f)
				{
					if (UMotionWarpingComponent* Warp = GaspMover->FindComponentByClass<UMotionWarpingComponent>()) { Warp->AddOrUpdateWarpTargetFromTransform(FName(TEXT("SmartObject")), SitSlot); }
					UCapsuleComponent* Cap = GaspMover->GetCapsuleComponent();
					GSavedResponses = Cap->GetCollisionResponseToChannels();
					Cap->SetCollisionResponseToChannel(ECC_WorldStatic, ECR_Ignore);
					Cap->SetCollisionResponseToChannel(ECC_WorldDynamic, ECR_Ignore);
					GaspMover->GetCharacterMovement()->SetMovementMode(MOVE_Flying);
					ChooserGraph->Montage_PlayWithBlendIn(Got, FAlphaBlendArgs(0.25f), 1.0f, EMontagePlayReturnType::MontageLength, St);
					SitMontage = Got;
					SitPhase = ESitPhase::Entering;
					SitPhaseAt = SitClock;
					GLastApproach = TEXT("started");
					// the slide over the planted foot's own stance, from the clip's table where it has the moment, else 0.3 s
					// THE PLANTED FOOT BY ITS PLACE (29 October: the walk's contact reading called a swinging foot planted, one
					// that travelled 125 cm while the body moved 70): the lower foot at the start, its slide measured while it
					// stays within 2 cm of that height, for at most 0.4 s
					GStartFoot = SitFootAt(0).Z <= SitFootAt(1).Z ? 0 : 1;
					GStartFootAt = SitFootAt(GStartFoot);
					GSlideCm = 0.0f;
					GSlideUntil = SitClock + 0.4f;
					UE_LOG(LogTemp, Display, TEXT("LedgerSit: step 6, started %s at %.2f s by the sample's search (cost %.2f; %.0f cm of its walk left, its root %.0f cm from its attach bone against his %.0f cm from the slot)"),
						*GEntries[Ei].Name, St, Cost, Left, ClipDist, Dist);
					return;
				}
			}
		}
		if (!bTable && TheChooser().bOk) { Foot = -1; }   // the search decides; the table start of the first two tries stays off
		if (Foot >= 0)
		{
			const float Through = FMath::Clamp(ContactFor[Foot] / FMath::Max(StanceSeconds, 0.2f), 0.0f, 1.0f);
			const FEntryMoment* Hit = nullptr;
			float BestScore = 1e9f;
			FVector HitRel = FVector::ZeroVector;
			float HitYaw = 0.0f;
			bool bInPlace = false, bFootToo = false;
			for (const FEntryMoment& M : GMoments)
			{
				const FVector R = M.MoverAt.InverseTransformPosition(Pos);
				const float YawOff = (float)FRotator::NormalizeAxis((double)Yaw - M.MoverAt.Rotator().Yaw);
				if (FMath::Abs(R.X) > 15.0 || FMath::Abs(R.Y) > 10.0 || FMath::Abs(YawOff) > 20.0f) { continue; }
				bInPlace = true;
				if (M.Foot != Foot) { continue; }
				bFootToo = true;
				GBestGap = FMath::Min(GBestGap, FMath::Abs(M.Through - Through));
				if (FMath::Abs(M.Through - Through) > 0.10f) { continue; }
				const float Score = (float)(FMath::Abs(R.X) + 1.5 * FMath::Abs(R.Y)) + 0.5f * FMath::Abs(YawOff);
				if (Score < BestScore) { BestScore = Score; Hit = &M; HitRel = R; HitYaw = YawOff; }
			}
			GFramesInPlace += bInPlace ? 1 : 0;
			GFramesFootToo += bFootToo ? 1 : 0;
			UAnimInstance* Graph = GaspMover->GetMesh()->GetAnimInstance();
			if (Hit != nullptr && Graph != nullptr)
			{
				const FEntry& E = GEntries[Hit->Clip];
				if (UMotionWarpingComponent* Warp = GaspMover->FindComponentByClass<UMotionWarpingComponent>()) { Warp->AddOrUpdateWarpTargetFromTransform(FName(TEXT("SmartObject")), SitSlot); }
				UCapsuleComponent* Cap = GaspMover->GetCapsuleComponent();
				GSavedResponses = Cap->GetCollisionResponseToChannels();
				Cap->SetCollisionResponseToChannel(ECC_WorldStatic, ECR_Ignore);
				Cap->SetCollisionResponseToChannel(ECC_WorldDynamic, ECR_Ignore);
				GaspMover->GetCharacterMovement()->SetMovementMode(MOVE_Flying);
				Graph->Montage_PlayWithBlendIn(E.Montage, FAlphaBlendArgs(0.2f), 1.0f, EMontagePlayReturnType::MontageLength, Hit->T);
				SitMontage = E.Montage;
				SitPhase = ESitPhase::Entering;
				SitPhaseAt = SitClock;
				GLastApproach = TEXT("started");
				GStartFoot = SitFootAt(0).Z <= SitFootAt(1).Z ? 0 : 1;
				GStartFootAt = SitFootAt(GStartFoot);
				GSlideCm = 0.0f;
				GSlideUntil = SitClock + 0.4f;
				UE_LOG(LogTemp, Display, TEXT("LedgerSit: step 6, started %s at %.2f s (foot %s, %.0f%% through its stance against his %.0f%%; %.1f cm along, %.1f across, %.1f degrees off its place then; %.0f cm of its walk left)"),
					*E.Name, Hit->T, Foot == 0 ? TEXT("left") : TEXT("right"), 100.0f * Hit->Through, 100.0f * Through, HitRel.X, HitRel.Y, HitYaw, Hit->Left);
				return;
			}
		}
	}
	const float NearestLeft = B.PathLeft[Nearest];
	if ((GStage == 1 && NearestLeft < (float)B.Windows[0] - 15.0f) || SitClock - SitPhaseAt > 8.0f)
	{
		const TCHAR* Why = SitClock - SitPhaseAt > 8.0f ? TEXT("no start in 8 s") : TEXT("past the entry with no start");
		UE_LOG(LogTemp, Display, TEXT("LedgerSit: step 6 fallback: %s; the old start (on the path %d frames, in some moment's place %d, with his foot too %d, the nearest stance gap there %.0f points; the search %d frames, its best cost %.2f, in a tested band %.2f; his speed %.0f)"),
			Why, GFramesOnLine, GFramesInPlace, GFramesFootToo, 100.0f * GBestGap, GChooserFrames, GBestCostAny, GBestCostInBand, GaspMover->GetVelocity().Size2D());
		SitPhase = ESitPhase::None;
		GLastApproach = FString(TEXT("fallback: ")) + Why;
		bSitNoApproach = true;
		if (!TryStartSit()) { GLastApproach += TEXT(" (and the old start found no seat)"); }
		bSitNoApproach = false;
		return;
	}
	// steering: to where he joins the path, then along it, aiming 60 cm of its walk ahead of the nearest point
	FVector Aim = GPre;
	if (GStage == 1)
	{
		int32 J = Nearest;
		while (J + 1 < B.Path.Num() && B.PathLeft[J] > NearestLeft - 60.0f) { ++J; }
		Aim = B.Path[J];
	}
	GaspMover->AddMovementInput((Aim - Pos).GetSafeNormal2D(), 1.0f);
}

// -TomSitApproachTest (28 October, the method's steps 5 and 6 checked): for each seat he is stood at three places in
// the room (2.6 m out in front, and 2.2 m out a metre to either side), facing the seat; he walks toward it and E is
// pressed 1.5 m from it, as a player would; each case says the entry chosen, how far off his heading, start or
// fallback, and whether he sat; -TomSitProofExit ends the game after
void ALedgerSliceCharacter::SitApproachTestTick(float DeltaSeconds)
{
	static const bool bOn = FParse::Param(FCommandLine::Get(), TEXT("TomSitApproachTest"));
	if (!bOn || GaspMover == nullptr || LedgerSit::Seats().Num() == 0) { return; }
	static float T = 0.0f, StepAt = 0.0f;
	static int32 Case = 0, Step = 0, Started = 0, Fallbacks = 0, SatN = 0, Within = 0;
	T += DeltaSeconds;
	const int32 Cases = LedgerSit::Seats().Num() * 3;
	if (Case >= Cases) { return; }
	const int32 SeatI = Case / 3, K = Case % 3;
	const LedgerSit::FSeat& S = LedgerSit::Seats()[SeatI];
	const FVector Front = FRotator(0.0f, S.Yaw, 0.0f).Vector();
	const FVector Side = FRotator(0.0f, S.Yaw + 90.0f, 0.0f).Vector();
	auto Next = [&](bool bSat, const TCHAR* Why)
	{
		Started += LedgerSit::GLastApproach == TEXT("started") ? 1 : 0;
		Fallbacks += LedgerSit::GLastApproach.StartsWith(TEXT("fallback")) ? 1 : 0;
		SatN += bSat ? 1 : 0;
		Within += (LedgerSit::GLastHeadingOff >= 0.0f && LedgerSit::GLastHeadingOff <= 20.0f) ? 1 : 0;
		const FString EntryName = LedgerSit::GEntries.IsValidIndex(LedgerSit::GBest) ? LedgerSit::GEntries[LedgerSit::GBest].Name : FString(TEXT("none"));
		UE_LOG(LogTemp, Display, TEXT("LedgerSitApproach: seat %d from %s: %s; entry %s, heading off %.0f; %s; slide %.1f cm, attach bone %.1f cm and %.1f degrees off the slot, hips %.1f cm off and %.1f up"), SeatI,
			K == 0 ? TEXT("in front") : (K == 1 ? TEXT("front left") : TEXT("front right")),
			*LedgerSit::GLastApproach, *EntryName, LedgerSit::GLastHeadingOff, bSat ? TEXT("sat") : Why,
			LedgerSit::GSlideCm, LedgerSit::GBoneCm, LedgerSit::GBoneYaw, LedgerSit::GHipsCm, LedgerSit::GHipsUpCm);
		UE_LOG(LogTemp, Display, TEXT("LedgerSitApproach: seat %d, the stand-up touched the room %d times"), SeatI, LedgerSit::GLastOut);
		LedgerSit::GLastOut = -1;
		LedgerSit::GSlideCm = LedgerSit::GBoneCm = LedgerSit::GHipsCm = LedgerSit::GHipsUpCm = -1.0f;
		LedgerSit::GBoneYaw = 0.0f;
		LedgerSit::GStartFoot = -1;
		LedgerSit::GLastApproach.Empty();
		LedgerSit::GLastHeadingOff = -1.0f;
		LedgerSit::GBest = -1;
		++Case; Step = 0; StepAt = T;
		if (Case >= Cases)
		{
			UE_LOG(LogTemp, Display, TEXT("ledgerSitApproach=%s cases=%d started=%d fallbacks=%d sat=%d headingWithin20=%d"),
				SatN == Cases && Started == Cases ? TEXT("PASS") : TEXT("FAIL"), Cases, Started, Fallbacks, SatN, Within);
			if (FParse::Param(FCommandLine::Get(), TEXT("TomSitProofExit"))) { FPlatformMisc::RequestExit(false); }
		}
	};
	if (Step == 0 && T - StepAt > (Case == 0 ? 4.0f : 1.0f))
	{
		const FVector From = S.Slot + Front * (K == 0 ? 260.0 : 220.0) + Side * (K == 1 ? 100.0 : (K == 2 ? -100.0 : 0.0));
		SetActorLocationAndRotation(From + FVector(0.0, 0.0, 95.0), FRotator(0.0f, (float)(S.Slot - From).Rotation().Yaw, 0.0f), false, nullptr, ETeleportType::TeleportPhysics);
		Step = 1; StepAt = T;
	}
	else if (Step == 1 && T - StepAt > 1.0f)
	{
		const FVector Pos = GaspMover->GetActorLocation();
		// the first day's tour holds his feet (CrimeProbe.cpp, WalkRoundTick); the test walks him anyway, as the walk's proof does
		if (APlayerController* PC = Cast<APlayerController>(GetController())) { if (PC->IsMoveInputIgnored()) { PC->ResetIgnoreMoveInput(); } }
		static float NextSay = 0.0f;
		if (T >= NextSay)
		{
			// where the walk-in stands twice a second (28 October: the first two runs barely moved him in 7 s)
			NextSay = T + 0.5f;
			const APlayerController* PCx = Cast<APlayerController>(GetController());
			// and what the mover's capsule stands inside, if anything (the first runs: pushed, speed 0, only inside the office)
			FString Inside;
			{
				TArray<FOverlapResult> In;
				FCollisionQueryParams QI(FName(TEXT("LedgerSitWalkIn")), false, GaspMover);
				QI.AddIgnoredActor(this);
				const UCapsuleComponent* C = GaspMover->GetCapsuleComponent();
				// lifted 5 cm, so the floor he stands on is not counted
				GetWorld()->OverlapMultiByChannel(In, C->GetComponentLocation() + FVector(0.0, 0.0, 5.0), FQuat::Identity, ECC_Pawn, FCollisionShape::MakeCapsule(C->GetScaledCapsuleRadius() - 1.0f, C->GetScaledCapsuleHalfHeight() - 1.0f), QI);
				for (const FOverlapResult& O : In)
				{
					const UPrimitiveComponent* P = O.GetComponent();
					if (P == nullptr || P->GetOwner() == nullptr) { continue; }
					const UStaticMeshComponent* SM = Cast<UStaticMeshComponent>(P);
					const FBox B = P->Bounds.GetBox();
					const UBodySetup* BS = SM != nullptr && SM->GetStaticMesh() != nullptr ? SM->GetStaticMesh()->GetBodySetup() : nullptr;
					Inside += FString::Printf(TEXT(" %s/%s mesh %s box (%.0f..%.0f, %.0f..%.0f, %.0f..%.0f) collision %d profile %s pawn %d, body: %d shapes, trace flag %d;"), *P->GetOwner()->GetName(), *P->GetName(),
						SM != nullptr && SM->GetStaticMesh() != nullptr ? *SM->GetStaticMesh()->GetName() : TEXT("-"), B.Min.X, B.Max.X, B.Min.Y, B.Max.Y, B.Min.Z, B.Max.Z,
						(int32)P->GetCollisionEnabled(), *P->GetCollisionProfileName().ToString(), (int32)P->GetCollisionResponseToChannel(ECC_Pawn),
						BS != nullptr ? BS->AggGeom.GetElementCount() : -1, BS != nullptr ? (int32)BS->CollisionTraceFlag : -1);
				}
				Inside += FString::Printf(TEXT(" (capsule %.0f by %.0f)"), C->GetScaledCapsuleRadius(), C->GetScaledCapsuleHalfHeight());
				// every copy of the office's fittings in the world, and its collision (only one is spawned, collision off)
				for (TActorIterator<AStaticMeshActor> It(GetWorld()); It; ++It)
				{
					const UStaticMeshComponent* SC = It->GetStaticMeshComponent();
					if (SC != nullptr && SC->GetStaticMesh() != nullptr && SC->GetStaticMesh()->GetName().Contains(TEXT("_fittings")))
					{
						Inside += FString::Printf(TEXT(" [copy %s collision %d profile %s hidden %d]"), *It->GetName(), (int32)SC->GetCollisionEnabled(), *SC->GetCollisionProfileName().ToString(), It->IsHidden() ? 1 : 0);
					}
				}
			}
			UE_LOG(LogTemp, Display, TEXT("LedgerSitApproach: walking in, mover (%.0f, %.0f, %.0f) speed %.0f mode %d, his own (%.0f, %.0f), last push %.2f, feet held %d, %.0f cm from the seat; inside:%s"),
				Pos.X, Pos.Y, Pos.Z, GaspMover->GetVelocity().Size2D(), (int32)GaspMover->GetCharacterMovement()->MovementMode, GetActorLocation().X, GetActorLocation().Y, GaspLastIn,
				PCx != nullptr && PCx->IsMoveInputIgnored() ? 1 : 0, FVector::Dist2D(Pos, S.Slot), Inside.IsEmpty() ? TEXT(" nothing") : *Inside);
		}
		if (FVector::Dist2D(Pos, S.Slot) > 150.0 && T - StepAt < 7.0f) { AddMovementInput((S.Slot - Pos).GetSafeNormal2D(), 1.0f); }
		else if (TryStartSit()) { Step = 2; StepAt = T; }
		else { Next(false, TEXT("no seat taken")); }
	}
	else if (Step == 2)
	{
		if (SitPhase == ESitPhase::Seated) { Step = 3; StepAt = T; }
		else if (SitPhase == ESitPhase::None || T - StepAt > 20.0f) { Next(false, SitPhase == ESitPhase::None ? TEXT("not seated") : TEXT("timeout")); }
	}
	else if (Step == 3 && T - StepAt > 1.0f) { bSitWantsUp = true; Step = 4; StepAt = T; }
	else if (Step == 4 && (SitPhase == ESitPhase::None || T - StepAt > 10.0f)) { Next(true, TEXT("")); }
	// -TomSitApproachShots: the sit-down through the player's own camera, ten pictures a second, on the fixed step
	static const bool bShots = FParse::Param(FCommandLine::Get(), TEXT("TomSitApproachShots"));
	static float NextShot = 0.0f;
	if (bShots && (SitPhase == ESitPhase::Entering || SitPhase == ESitPhase::Approaching) && T >= NextShot)
	{
		FScreenshotRequest::RequestScreenshot(FPaths::ConvertRelativePathToFull(FPaths::ProjectSavedDir() / TEXT("TomSitApproach")
			/ FString::Printf(TEXT("case%d-%05.2f.png"), Case, T)), false, false);
		NextShot = T + 0.1f;
	}
}

// THE ROOM TEST OF WHAT WILL BE PLAYED (28 October, the sitting method's step 4; Kingdom Come II drops every entry its
// tests fail). The clips' own starts lie 4.2 to 5.1 m out, beyond the office's walls, so each clip is started where
// RemainCm of its own travel is left (the start step 6 can choose inside the room), from that derived place and from the
// envelope's four corners (+-15 cm along, +-10 across, +-20 degrees), the warp on as in play. Each frame the ankles,
// knees, mid-shins, hips and hands are tested against the world as spheres a centimetre inside the limb, with the seat's
// own furniture (whatever stands at the seat) and Tom ignored; an entry is kept only with no contact on any of its runs.
void ALedgerSliceCharacter::SitRoomTestTick(float DeltaSeconds)
{
	static const bool bOn = FParse::Param(FCommandLine::Get(), TEXT("TomSitRoomTest"));
	if (!bOn || GaspMover == nullptr || LedgerSit::Seats().Num() == 0) { return; }
	static const TCHAR* const AllSides[] = { TEXT("F_Lfoot"), TEXT("F_Rfoot"), TEXT("L_090_Lfoot"), TEXT("L_090_Rfoot"), TEXT("R_090_Lfoot"),
		TEXT("R_090_Rfoot"), TEXT("BL_LFoot"), TEXT("BL_RFoot"), TEXT("BR_LFoot"), TEXT("BR_RFoot") };
	// -TomSitRoomClips=A,B: only those sides (28 October: further start distances tried for the kept entries only)
	static TArray<FString> Sides;
	static const FVector Corner[5] = { FVector(0, 0, 0), FVector(15, 10, 20), FVector(15, -10, -20), FVector(-15, 10, -20), FVector(-15, -10, 20) };
	static double RemainCm = LedgerSit::TestedRemainCm;
	static int32 Run = -1, Contacts = 0, Kept = 0, SeatIdx = 0;
	static float T = 0.0f, RunAt = 0.0f;
	static FString Worst;
	static TArray<int32> ClipContacts;
	static FCollisionQueryParams Q(FName(TEXT("LedgerSitRoom")), false);
	T += DeltaSeconds;
	if (Run == -1)
	{
		if (T < 4.0f) { return; }
		FParse::Value(FCommandLine::Get(), TEXT("TomSitRoomRemainCm="), RemainCm);
		// -TomSitRoomSeat=N: which of the seats (each seat's room differs: its ends, the wall, the counter)
		FParse::Value(FCommandLine::Get(), TEXT("TomSitRoomSeat="), SeatIdx);
		SeatIdx = FMath::Clamp(SeatIdx, 0, LedgerSit::Seats().Num() - 1);
		FString Only;
		// the whole list (29 October: the reader stopped at the first comma, so only the first clip was tried)
		FParse::Value(FCommandLine::Get(), TEXT("TomSitRoomClips="), Only, false);
		TArray<FString> Wanted;
		Only.ParseIntoArray(Wanted, TEXT(","));
		for (const TCHAR* Side : AllSides) { if (Wanted.Num() == 0 || Wanted.Contains(FString(Side))) { Sides.Add(Side); } }
		ClipContacts.Init(0, Sides.Num());
		// the seat's own furniture, ignored: whatever stands at the seat a little above the slot
		const LedgerSit::FSeat& S0 = LedgerSit::Seats()[SeatIdx];
		TArray<FOverlapResult> At;
		GetWorld()->OverlapMultiByChannel(At, S0.Slot + FVector(0.0, 0.0, 30.0), FQuat::Identity, ECC_WorldStatic, FCollisionShape::MakeSphere(15.0f));
		for (const FOverlapResult& O : At) { if (O.GetComponent() != nullptr) { Q.AddIgnoredComponent(O.GetComponent()); } }
		Q.AddIgnoredActor(this);
		Q.AddIgnoredActor(GaspMover);
		TArray<AActor*> Riders;
		GaspMover->GetAttachedActors(Riders, true, true);
		Q.AddIgnoredActors(Riders);
		UE_LOG(LogTemp, Display, TEXT("LedgerSitRoom: %d furniture part(s) at the seat ignored; starts %.0f cm of travel before the seat"), At.Num(), RemainCm);
		Run = 0; RunAt = T;
	}
	const int32 Runs = Sides.Num() * 5;
	if (Run >= Runs) { return; }
	const int32 C = Run / 5, K = Run % 5;
	const FString ClipName = FString::Printf(TEXT("M_interaction_bench_into_%s_Montage"), *Sides[C]);
	USkeletalMeshComponent* MM = GaspMover->GetMesh();
	UAnimInstance* Graph = MM->GetAnimInstance();
	auto Finish = [&]()
	{
		ClipContacts[C] += Contacts;
		UE_LOG(LogTemp, Display, TEXT("LedgerSitRoom: %s start %d contacts=%d%s"), *Sides[C], K, Contacts, Worst.IsEmpty() ? TEXT("") : *(TEXT(" first=") + Worst));
		if (Graph != nullptr) { Graph->StopAllMontages(0.0f); }
		SitPhase = ESitPhase::None; SitMontage = nullptr;
		Contacts = 0; Worst.Empty();
		if (K == 4)
		{
			Kept += ClipContacts[C] == 0 ? 1 : 0;
			UE_LOG(LogTemp, Display, TEXT("LedgerSitRoom: %s %s"), *Sides[C], ClipContacts[C] == 0 ? TEXT("KEPT") : TEXT("DROPPED"));
		}
		++Run; RunAt = T;
		if (Run >= Runs)
		{
			UE_LOG(LogTemp, Display, TEXT("ledgerSitRoom=%s seat=%d kept=%d of %d entries, starts %.0f cm before the seat"), Kept > 0 ? TEXT("SOME-KEPT") : TEXT("NONE-KEPT"), SeatIdx, Kept, Sides.Num(), RemainCm);
			if (FParse::Param(FCommandLine::Get(), TEXT("TomSitProofExit"))) { FPlatformMisc::RequestExit(false); }
		}
	};
	if (SitPhase == ESitPhase::None)
	{
		if (T - RunAt < 0.5f) { return; }
		const LedgerSit::FClipPose P = LedgerSit::ClipPose(ClipName);
		UAnimMontage* Entry = LedgerSit::Clip(ClipName);
		if (!P.bOk || Entry == nullptr || Graph == nullptr) { Contacts = -1; Worst = TEXT("no-clip"); Finish(); return; }
		const LedgerSit::FSeat& S = LedgerSit::Seats()[SeatIdx];
		SitSlot = FTransform(FRotator(0.0f, S.Yaw, 0.0f), S.Slot);
		// the moment where RemainCm of the clip's own travel is left
		const float Len = Entry->GetPlayLength();
		float Start = 0.0f, Best = 1e9f;
		for (float Tm = 0.0f; Tm < Len; Tm += 1.0f / 30.0f)
		{
			const float Err = FMath::Abs((float)Entry->ExtractRootMotionFromTrackRange(Tm, Len, FAnimExtractContext()).GetTranslation().Size2D() - (float)RemainCm);
			if (Err < Best) { Best = Err; Start = Tm; }
		}
		// the root's frame at that moment, carried onto the world through the warp bone's end on the slot
		const FTransform Moved = Entry->ExtractRootMotionFromTrackRange(0.0f, Start, FAnimExtractContext());
		const FTransform MeshAt = (Moved * P.RootStart) * (P.WarpBoneEnd.Inverse() * SitSlot);
		FTransform MoverAt = MM->GetRelativeTransform().Inverse() * MeshAt;
		const FRotator Yaw(0.0f, MoverAt.Rotator().Yaw, 0.0f);
		const FVector Off = Yaw.RotateVector(FVector(Corner[K].X, Corner[K].Y, 0.0));
		GaspMover->SetActorLocationAndRotation(MoverAt.GetLocation() + Off, FRotator(0.0f, Yaw.Yaw + Corner[K].Z, 0.0f), false, nullptr, ETeleportType::TeleportPhysics);
		if (UMotionWarpingComponent* Warp = GaspMover->FindComponentByClass<UMotionWarpingComponent>()) { Warp->AddOrUpdateWarpTargetFromTransform(FName(TEXT("SmartObject")), SitSlot); }
		UCapsuleComponent* Cap = GaspMover->GetCapsuleComponent();
		Cap->SetCollisionResponseToChannel(ECC_WorldStatic, ECR_Ignore);
		Cap->SetCollisionResponseToChannel(ECC_WorldDynamic, ECR_Ignore);
		GaspMover->GetCharacterMovement()->SetMovementMode(MOVE_Flying);
		Graph->Montage_Play(Entry, 1.0f, EMontagePlayReturnType::MontageLength, Start);
		SitMontage = Entry;
		SitPhase = ESitPhase::Entering;   // SitTick takes it on to the loop when the clip ends
		SitPhaseAt = SitClock;
		return;
	}
	// sampled while the clip carries him in; the run ends once he is seated
	struct FLimb { const TCHAR* A; const TCHAR* B; float R; };
	static const FLimb Limbs[] = { { TEXT("foot_l"), nullptr, 3.0f }, { TEXT("foot_r"), nullptr, 3.0f }, { TEXT("calf_l"), nullptr, 5.0f }, { TEXT("calf_r"), nullptr, 5.0f },
		{ TEXT("calf_l"), TEXT("foot_l"), 4.0f }, { TEXT("calf_r"), TEXT("foot_r"), 4.0f }, { TEXT("pelvis"), nullptr, 11.0f }, { TEXT("hand_l"), nullptr, 3.0f }, { TEXT("hand_r"), nullptr, 3.0f } };
	for (const FLimb& L : Limbs)
	{
		const FVector P = L.B != nullptr ? (MM->GetSocketLocation(L.A) + MM->GetSocketLocation(L.B)) * 0.5 : MM->GetSocketLocation(L.A);
		if (GetWorld()->OverlapAnyTestByChannel(P, FQuat::Identity, ECC_WorldStatic, FCollisionShape::MakeSphere(L.R), Q))
		{
			++Contacts;
			if (Worst.IsEmpty())
			{
				// and what it touched (28 October: seat 1's front entries all touched at 1.65 to 1.78 s, cause unread)
				TArray<FOverlapResult> What;
				GetWorld()->OverlapMultiByChannel(What, P, FQuat::Identity, ECC_WorldStatic, FCollisionShape::MakeSphere(L.R), Q);
				const UPrimitiveComponent* Hit = What.Num() > 0 ? What[0].GetComponent() : nullptr;
				// and its mesh, with where it stands (29 October: the actors are unnamed in a packaged or played world)
				const UStaticMeshComponent* HitMesh = Cast<UStaticMeshComponent>(Hit);
				const FBox HB = Hit != nullptr ? Hit->Bounds.GetBox() : FBox(ForceInit);
				Worst = FString::Printf(TEXT("%s%s@%.2fs-on-%s(%s,%.0f..%.0f,%.0f..%.0f,%.0f..%.0f)"), L.A, L.B != nullptr ? TEXT("-mid") : TEXT(""), Graph != nullptr && SitMontage != nullptr ? Graph->Montage_GetPosition(SitMontage) : -1.0f,
					Hit != nullptr && Hit->GetOwner() != nullptr ? *Hit->GetOwner()->GetName() : TEXT("?"),
					HitMesh != nullptr && HitMesh->GetStaticMesh() != nullptr ? *HitMesh->GetStaticMesh()->GetName() : TEXT("-"), HB.Min.X, HB.Max.X, HB.Min.Y, HB.Max.Y, HB.Min.Z, HB.Max.Z);
			}
		}
	}
	if (SitPhase == ESitPhase::Seated || T - RunAt > 20.0f) { Finish(); }
}

void ALedgerSliceCharacter::SitTick(float DeltaSeconds)
{
	SitClock += DeltaSeconds;
	if (SitPhase == ESitPhase::None || GaspMover == nullptr) { return; }
	if (SitPhase == ESitPhase::Approaching) { SitApproachTick(DeltaSeconds); return; }
	// the planted foot's slide after a start, while it stays down (within 2 cm of its height at the start), at most 0.4 s
	if (SitPhase == ESitPhase::Entering && LedgerSit::GStartFoot >= 0)
	{
		const FVector Now = SitFootAt(LedgerSit::GStartFoot);
		if (SitClock <= LedgerSit::GSlideUntil && Now.Z <= LedgerSit::GStartFootAt.Z + 2.0)
		{
			LedgerSit::GSlideCm = FMath::Max(LedgerSit::GSlideCm, (float)FVector::Dist2D(Now, LedgerSit::GStartFootAt));
			// where the foot, the other foot and the root are from the start (29 October: the slide read 39 to 85 cm)
			static float NextSay = 0.0f;
			if (SitClock >= NextSay || SitClock - SitPhaseAt < 0.02f)
			{
				NextSay = SitClock + 0.1f;
				const FVector Other = SitFootAt(1 - LedgerSit::GStartFoot);
				const FVector OnMover = SitFootAt(LedgerSit::GStartFoot, true);
				UE_LOG(LogTemp, Display, TEXT("LedgerSitSlide: %.2f s after the start (until %.2f): the planted foot %.1f cm from where it was, %.1f cm above the slot (on the hidden mover: at %.0f, %.0f, %.0f against the worn body's %.0f, %.0f, %.0f); the other %.1f cm above; the root %.1f cm on; the clip at %.2f s"),
					SitClock - SitPhaseAt, LedgerSit::GSlideUntil - SitPhaseAt, FVector::Dist2D(Now, LedgerSit::GStartFootAt), Now.Z - SitSlot.GetLocation().Z,
					OnMover.X, OnMover.Y, OnMover.Z, Now.X, Now.Y, Now.Z, Other.Z - SitSlot.GetLocation().Z,
					FVector::Dist2D(GaspMover->GetActorLocation(), LedgerSit::GStartFootAt), SitMontage != nullptr ? GaspMover->GetMesh()->GetAnimInstance()->Montage_GetPosition(SitMontage) : -1.0f);
			}
		}
		else { LedgerSit::GStartFoot = -1; }
	}
	UAnimInstance* Graph = GaspMover->GetMesh()->GetAnimInstance();
	if (Graph == nullptr || SitMontage == nullptr) { return; }
	const float Pos = Graph->Montage_GetPosition(SitMontage);
	const bool bEnding = !Graph->Montage_IsPlaying(SitMontage) || Pos >= SitMontage->GetPlayLength() - 0.2f;
	if (SitPhase == ESitPhase::Entering && bEnding)
	{
		if (UAnimMontage* Loop = LedgerSit::Clip(TEXT("M_interaction_bench_idle_loop_Montage")))
		{
			Graph->Montage_Play(Loop, 1.0f);
			const FName Section = Loop->GetSectionName(0);
			Graph->Montage_SetNextSection(Section, Section, Loop);
			SitMontage = Loop;
		}
		SitPhase = ESitPhase::Seated;
		SitPhaseAt = SitClock;
		// where he ended in the seat's own frame (X out into the room, Y along the bench), and the pelvis's
		const FVector Rel = SitSlot.InverseTransformPosition(GaspMover->GetActorLocation());
		const FVector Pelvis = SitSlot.InverseTransformPosition(GaspMover->GetMesh()->GetSocketLocation(TEXT("pelvis")));
		{
			const FTransform Bone = GaspMover->GetMesh()->GetSocketTransform(TEXT("attach"));
			LedgerSit::GBoneCm = (float)FVector::Dist2D(Bone.GetLocation(), SitSlot.GetLocation());
			LedgerSit::GBoneYaw = (float)FRotator::NormalizeAxis(Bone.Rotator().Yaw - SitSlot.Rotator().Yaw);
			LedgerSit::GHipsCm = (float)FVector::Dist2D(GaspMover->GetMesh()->GetSocketLocation(TEXT("pelvis")), SitSlot.GetLocation());
			LedgerSit::GHipsUpCm = (float)(GaspMover->GetMesh()->GetSocketLocation(TEXT("pelvis")).Z - SitSlot.GetLocation().Z);
		}
		// AND HIS VISIBLE BODY AGAINST THE MANNEQUIN, seated (29 October: the judged sit showed his far foot on its
		// toes, heel up, where the mannequin's feet stand flat; the retarget puts his feet on the mannequin's unless
		// his legs cannot reach): hips, and each foot's ball and heel above the floor, on both bodies
		if (WornBody != nullptr)
		{
			const double Floor = SitSlot.GetLocation().Z;
			USkeletalMeshComponent* MMx = GaspMover->GetMesh();
			auto Up = [&](USkeletalMeshComponent* K, const TCHAR* B) { return K->DoesSocketExist(FName(B)) ? K->GetSocketLocation(FName(B)).Z - Floor : -999.0; };
			UE_LOG(LogTemp, Display, TEXT("LedgerSit: seated bodies: pelvis %.1f on the mannequin, %.1f on Tom; balls l %.1f / %.1f, r %.1f / %.1f; ankles l %.1f / %.1f, r %.1f / %.1f (mannequin / Tom, cm above the floor)"),
				Up(MMx, TEXT("pelvis")), Up(WornBody, TEXT("pelvis")), Up(MMx, TEXT("ball_l")), Up(WornBody, TEXT("ball_l")), Up(MMx, TEXT("ball_r")), Up(WornBody, TEXT("ball_r")),
				Up(MMx, TEXT("foot_l")), Up(WornBody, TEXT("foot_l")), Up(MMx, TEXT("foot_r")), Up(WornBody, TEXT("foot_r")));
		}
		UE_LOG(LogTemp, Display, TEXT("LedgerSit: seated, %.1f cm from the seat (out %.1f, along %.1f; pelvis out %.1f, along %.1f, up %.1f)"),
			FVector::Dist2D(GaspMover->GetActorLocation(), SitSlot.GetLocation()), Rel.X, Rel.Y, Pelvis.X, Pelvis.Y, Pelvis.Z);
	}
	else if (SitPhase == ESitPhase::Seated && bSitWantsUp)
	{
		if (UAnimMontage* Up = LedgerSit::Clip(TEXT("M_interaction_bench_out_to_stand_Montage")))
		{
			Graph->Montage_Play(Up, 1.0f);
			SitMontage = Up;
		}
		SitPhase = ESitPhase::Leaving;
		SitPhaseAt = SitClock;
		bSitWantsUp = false;
	}
	else if (SitPhase == ESitPhase::Leaving && bEnding)
	{
		GaspMover->GetCapsuleComponent()->SetCollisionResponseToChannels(LedgerSit::GSavedResponses);
		GaspMover->GetCharacterMovement()->SetMovementMode(MOVE_Walking);
		SitPhase = ESitPhase::None;
		SitMontage = nullptr;
		UE_LOG(LogTemp, Display, TEXT("LedgerSit: standing again (the stand-up touched the room %d times%s; he ended %.0f cm from the seat)"),
			LedgerSit::GOutContacts, LedgerSit::GOutFirst.IsEmpty() ? TEXT("") : *(TEXT(", first ") + LedgerSit::GOutFirst),
			FVector::Dist2D(GaspMover->GetActorLocation(), SitSlot.GetLocation()));
		LedgerSit::GLastOut = LedgerSit::GOutContacts;
		LedgerSit::GOutContacts = 0; LedgerSit::GOutFirst.Empty();
	}
	// THE SEATED HOLD, every 1.5 s (29 October: the toe-rest the reviewer saw lasted the whole hold): hips and feet on
	// his visible body against the mannequin's
	if (SitPhase == ESitPhase::Seated && WornBody != nullptr)
	{
		static float NextHold = 0.0f;
		if (SitClock >= NextHold)
		{
			NextHold = SitClock + 1.5f;
			const double Floor = SitSlot.GetLocation().Z;
			USkeletalMeshComponent* MMx = GaspMover->GetMesh();
			auto Up = [&](USkeletalMeshComponent* K, const TCHAR* B) { return K->DoesSocketExist(FName(B)) ? K->GetSocketLocation(FName(B)).Z - Floor : -999.0; };
			UE_LOG(LogTemp, Display, TEXT("LedgerSit: holding %.1f s: pelvis %.1f / %.1f; balls l %.1f / %.1f, r %.1f / %.1f; ankles l %.1f / %.1f, r %.1f / %.1f (mannequin / Tom)"),
				SitClock - SitPhaseAt, Up(MMx, TEXT("pelvis")), Up(WornBody, TEXT("pelvis")), Up(MMx, TEXT("ball_l")), Up(WornBody, TEXT("ball_l")), Up(MMx, TEXT("ball_r")), Up(WornBody, TEXT("ball_r")),
				Up(MMx, TEXT("foot_l")), Up(WornBody, TEXT("foot_l")), Up(MMx, TEXT("foot_r")), Up(WornBody, TEXT("foot_r")));
		}
	}
	// THE STAND-UP AGAINST THE ROOM (29 October, the sitting method's step 9: the Out unwarped along a tested exit, no
	// contact): while he stands up, his feet, shins, hips and hands are tested against the world as the room test does,
	// the seat's own furniture and Tom ignored
	if (SitPhase == ESitPhase::Leaving)
	{
		FCollisionQueryParams Q(FName(TEXT("LedgerSitOut")), false);
		TArray<FOverlapResult> At;
		GetWorld()->OverlapMultiByChannel(At, SitSlot.GetLocation() + FVector(0.0, 0.0, 30.0), FQuat::Identity, ECC_WorldStatic, FCollisionShape::MakeSphere(15.0f));
		for (const FOverlapResult& O : At) { if (O.GetComponent() != nullptr) { Q.AddIgnoredComponent(O.GetComponent()); } }
		Q.AddIgnoredActor(this);
		Q.AddIgnoredActor(GaspMover);
		TArray<AActor*> Riders;
		GaspMover->GetAttachedActors(Riders, true, true);
		Q.AddIgnoredActors(Riders);
		USkeletalMeshComponent* MM = GaspMover->GetMesh();
		struct FLimb { const TCHAR* A; const TCHAR* B; float R; };
		static const FLimb Limbs[] = { { TEXT("foot_l"), nullptr, 3.0f }, { TEXT("foot_r"), nullptr, 3.0f }, { TEXT("calf_l"), nullptr, 5.0f }, { TEXT("calf_r"), nullptr, 5.0f },
			{ TEXT("calf_l"), TEXT("foot_l"), 4.0f }, { TEXT("calf_r"), TEXT("foot_r"), 4.0f }, { TEXT("pelvis"), nullptr, 11.0f }, { TEXT("hand_l"), nullptr, 3.0f }, { TEXT("hand_r"), nullptr, 3.0f } };
		for (const FLimb& L : Limbs)
		{
			const FVector P = L.B != nullptr ? (MM->GetSocketLocation(L.A) + MM->GetSocketLocation(L.B)) * 0.5 : MM->GetSocketLocation(L.A);
			TArray<FOverlapResult> What;
			if (GetWorld()->OverlapMultiByChannel(What, P, FQuat::Identity, ECC_WorldStatic, FCollisionShape::MakeSphere(L.R), Q))
			{
				++LedgerSit::GOutContacts;
				if (LedgerSit::GOutFirst.IsEmpty() && What.Num() > 0 && What[0].GetComponent() != nullptr)
				{
					const UStaticMeshComponent* HM = Cast<UStaticMeshComponent>(What[0].GetComponent());
					LedgerSit::GOutFirst = FString::Printf(TEXT("%s on %s at %.2f s"), L.A, HM != nullptr && HM->GetStaticMesh() != nullptr ? *HM->GetStaticMesh()->GetName() : TEXT("?"), Pos);
				}
			}
		}
	}
}

// -TomSitProof: he is stood 1.2 m in front of the door-end seat facing it, presses E, sits, stays three
// seconds, stands, and the line says how each step went and where his hips sat against the seat's point;
// -TomSitProofShots pictures it from the side ten times a second (Saved/TomSit), on the fixed step;
// -TomSitProofExit ends the game after.
void ALedgerSliceCharacter::SitProofTick(float DeltaSeconds)
{
	static const bool bOn = FParse::Param(FCommandLine::Get(), TEXT("TomSitProof"));
	if (!bOn || GaspMover == nullptr) { return; }
	static float T = 0.0f, StepAt = 0.0f, Offset = -1.0f, PelvisUp = 0.0f, NextShot = 0.0f, BoneOff = -1.0f, BoneYawOff = 0.0f;
	static FString EntryClip;
	static const bool bEntryTest = FParse::Value(FCommandLine::Get(), TEXT("TomSitEntryTest="), EntryClip) && !EntryClip.IsEmpty();
	static int32 Step = 0;
	static TWeakObjectPtr<ACameraActor> Cam;
	T += DeltaSeconds;
	const TArray<LedgerSit::FSeat>& Seats = LedgerSit::Seats();
	auto Done = [&](bool bPass, const TCHAR* Why)
	{
		UE_LOG(LogTemp, Display, TEXT("ledgerTomSit=%s %s entered=%d seated=%d stood=%d hipsFromSeatCm=%.1f hipsUpCm=%.1f t=%.1f%s"), bPass ? TEXT("PASS") : TEXT("FAIL"), Why,
			Step >= 2 ? 1 : 0, Step >= 3 ? 1 : 0, Step >= 5 ? 1 : 0, Offset, PelvisUp, T,
			bEntryTest ? *FString::Printf(TEXT(" entryTest=%s attachFromSlotCm=%.1f attachYawOffDeg=%.1f"), *EntryClip, BoneOff, BoneYawOff) : TEXT(""));
		Step = 99;
		if (FParse::Param(FCommandLine::Get(), TEXT("TomSitProofExit"))) { FPlatformMisc::RequestExit(false); }
	};
	if (Step == 99) { return; }
	if (Seats.Num() == 0) { Done(false, TEXT("no-seats")); return; }
	const LedgerSit::FSeat& S = Seats[0];
	const FVector Front = FRotator(0.0f, S.Yaw, 0.0f).Vector();
	if (Step == 0 && T > 3.0f)
	{
		SetActorLocationAndRotation(S.Slot + Front * 120.0 + FVector(0.0, 0.0, 95.0), FRotator(0.0f, S.Yaw + 180.0f, 0.0f), false, nullptr, ETeleportType::TeleportPhysics);
		Step = 1; StepAt = T;
	}
	else if (Step == 1 && T - StepAt > 1.5f) { if (bEntryTest ? StartSitFromEntry(EntryClip) : TryStartSit()) { Step = 2; StepAt = T; } else { Done(false, TEXT("no-start")); return; } }
	else if (Step == 2 && SitPhase == ESitPhase::Seated)
	{
		// JUDGED BY HIS HIPS, not his capsule: the seat's point is the one under the seat bone, and the
		// sample's clip carries the capsule 23 cm on after its warp ends (measured 25 October), by design
		const FVector Pelvis = GaspMover->GetMesh()->GetSocketLocation(TEXT("pelvis"));
		Offset = (float)FVector::Dist2D(Pelvis, S.Slot);
		PelvisUp = (float)(Pelvis.Z - S.Slot.Z);
		if (bEntryTest)
		{
			// THE ENTRY TEST'S VERDICT (the method's step 3): the warp bone where the warp would have aimed it, the warp
			// off: within 5 cm and 3 degrees of the slot, the hips at the clip's own seated height (51.8 cm) within 3 cm
			const FTransform Bone = GaspMover->GetMesh()->GetSocketTransform(TEXT("attach"));
			BoneOff = (float)FVector::Dist2D(Bone.GetLocation(), S.Slot);
			BoneYawOff = (float)FRotator::NormalizeAxis(Bone.Rotator().Yaw - SitSlot.Rotator().Yaw);
			const bool bPass = BoneOff < 5.0f && FMath::Abs(BoneYawOff) < 3.0f && FMath::Abs(PelvisUp - 51.8f) < 3.0f;
			Step = 3;   // entered and seated
			Done(bPass, TEXT("entry-test"));
			return;
		}
		Step = 3; StepAt = T;
	}
	else if (Step == 3 && T - StepAt > 3.0f) { bSitWantsUp = true; Step = 4; StepAt = T; }
	// the hips within 10 cm of the seat's point, and between 40 and 60 cm over the floor (a 45 cm seat)
	else if (Step == 4 && SitPhase == ESitPhase::None) { Step = 5; Done(Offset >= 0.0f && Offset < 10.0f && PelvisUp > 40.0f && PelvisUp < 60.0f, TEXT("sat-and-stood")); return; }
	else if (T > 45.0f) { Done(false, TEXT("timeout")); return; }
	if (FParse::Param(FCommandLine::Get(), TEXT("TomSitProofShots")) && Step >= 1)
	{
		if (!Cam.IsValid())
		{
			// out in the room 2.6 m in front of the seat and a little to the side, eye height, looking at it
			// (the bench runs along the side wall, so there is no room for a camera beside it)
			const FVector Side = FRotator(0.0f, S.Yaw - 90.0f, 0.0f).Vector();
			const FVector Eye = S.Slot + Front * 260.0 + Side * 80.0 + FVector(0.0, 0.0, 150.0);
			Cam = GetWorld()->SpawnActor<ACameraActor>(Eye, (S.Slot + Front * 30.0 + FVector(0.0, 0.0, 70.0) - Eye).Rotation());
			if (Cam.IsValid())
			{
				Cam->GetCameraComponent()->SetFieldOfView(60.0f);
				if (APlayerController* PC = Cast<APlayerController>(GetController())) { PC->SetViewTarget(Cam.Get()); }
			}
		}
		if (T >= NextShot)
		{
			FScreenshotRequest::RequestScreenshot(FPaths::ConvertRelativePathToFull(FPaths::ProjectSavedDir() / TEXT("TomSit") / FString::Printf(TEXT("s%05.2f.png"), T)), false, false);
			NextShot = T + 0.1f;
		}
	}
}

// ---- HIS STOPS, CHOSEN KINGDOM COME II'S WAY (his answer of 26 October, the walk's third try) ------------------
// Kingdom Come II picks each stop from a table by the distance left (0.6 to 2.1 m at a walk) and the quarter of
// the stride, with a clip for each leg (production/research/aaa-reference/studies/07-animation.md). Here: Epic's
// two forward walking stops (M_Neutral_Walk_Stop_F_Lfoot, _Rfoot), each read once into a table of moments (which
// foot its contact curves mark planted, how long it has been down, how long that stance lasts, and how far its
// root still walks); when the walk is let go, the moment whose planted foot and stance quarter match his own and
// whose walk left lies in the window is played from there to its end as a montage, its root motion carrying the
// mover, so no search can change clips half way through a stop (the re-step of 25 October). Only with
// -TomStopChosen: the walk stays as it is by default until this passes.
namespace LedgerStop
{
	struct FMoment { float T = 0.0f; int32 Foot = -1; float Down = 0.0f; float Stance = 0.0f; float Left = 0.0f; };
	struct FClip { UAnimSequence* Seq = nullptr; TArray<FMoment> Moments; };
	TArray<FClip> GClips;
	FName GSlot;
	bool bRead = false;
	const TCHAR* Contact[2] = { TEXT("contact_l"), TEXT("contact_r") };

	void Read()
	{
		if (bRead) { return; }
		bRead = true;
		if (UAnimMontage* Any = LedgerSit::Clip(TEXT("M_interaction_bench_idle_loop_Montage")))
		{
			if (Any->SlotAnimTracks.Num() > 0) { GSlot = Any->SlotAnimTracks[0].SlotName; }
		}
		for (const TCHAR* Name : { TEXT("M_Neutral_Walk_Stop_F_Lfoot"), TEXT("M_Neutral_Walk_Stop_F_Rfoot") })
		{
			UAnimSequence* Seq = LoadObject<UAnimSequence>(nullptr, *FString::Printf(TEXT("/Game/Characters/UEFN_Mannequin/Animations/Walk/%s.%s"), Name, Name));
			if (Seq == nullptr) { UE_LOG(LogTemp, Warning, TEXT("LedgerStop: no clip %s"), Name); continue; }
			Seq->AddToRoot();
			FClip C;
			C.Seq = Seq;
			const float Len = Seq->GetPlayLength();
			const float Step = 1.0f / 30.0f;
			TArray<float> Cv[2];
			for (float T = 0.0f; T <= Len; T += Step)
			{
				for (int32 F = 0; F < 2; ++F) { Cv[F].Add(Seq->EvaluateCurveData(FName(Contact[F]), FAnimExtractContext((double)T))); }
			}
			const int32 N = Cv[0].Num();
			for (int32 I = 0; I < N; ++I)
			{
				FMoment M;
				M.T = I * Step;
				// the planted foot: the one marked down; in double support, the one that came down last
				int32 Down[2] = { 0, 0 };
				for (int32 F = 0; F < 2; ++F) { for (int32 J = I; J >= 0 && Cv[F][J] > 0.5f; --J) { ++Down[F]; } }
				if (Down[0] > 0 && (Down[1] == 0 || Down[0] <= Down[1])) { M.Foot = 0; }
				else if (Down[1] > 0) { M.Foot = 1; }
				if (M.Foot >= 0)
				{
					int32 Up = 0;
					for (int32 J = I + 1; J < N && Cv[M.Foot][J] > 0.5f; ++J) { ++Up; }
					M.Down = Down[M.Foot] * Step;
					M.Stance = (Down[M.Foot] + Up) * Step;
				}
				M.Left = (float)Seq->ExtractRootMotionFromRange(M.T, Len, FAnimExtractContext()).GetTranslation().Size2D();
				C.Moments.Add(M);
			}
			UE_LOG(LogTemp, Display, TEXT("LedgerStop: %s read, %.2f s, %d moments, root motion %s, slot %s"), Name, Len, C.Moments.Num(),
				Seq->bEnableRootMotion ? TEXT("on") : TEXT("off"), *GSlot.ToString());
			GClips.Add(C);
		}
	}
}

void ALedgerSliceCharacter::StopTick(float WasIn, float NowIn)
{
	// on by default since his pass of 26 October; -NoTomStopChosen leaves the stops to the motion matching
	static const bool bOn = !FParse::Param(FCommandLine::Get(), TEXT("NoTomStopChosen"));
	if (!bOn || GaspMover == nullptr) { return; }
	UAnimInstance* Graph = GaspMover->GetMesh()->GetAnimInstance();
	if (Graph == nullptr) { return; }
	const float Dt = GetWorld()->GetDeltaSeconds();
	// HIS OWN STANCE, LIVE: how long each foot has been marked planted by the pose he is in
	for (int32 F = 0; F < 2; ++F)
	{
		if (Graph->GetCurveValue(FName(LedgerStop::Contact[F])) > 0.5f) { ContactFor[F] += Dt; }
		else
		{
			if (ContactFor[F] > 0.2f && ContactFor[F] < 1.2f) { StanceSeconds = FMath::Lerp(StanceSeconds, ContactFor[F], 0.3f); }
			ContactFor[F] = 0.0f;
		}
	}
	if (StopMontage != nullptr)
	{
		// a push ends the stop; so does its own end
		if (NowIn > 0.3f) { Graph->Montage_Stop(0.2f, StopMontage); }
		if (NowIn > 0.3f || !Graph->Montage_IsPlaying(StopMontage))
		{
			UE_LOG(LogTemp, Display, TEXT("LedgerStop: done (%s)"), NowIn > 0.3f ? TEXT("a push") : TEXT("its end"));
			StopMontage = nullptr;
		}
		return;
	}
	// LET GO while walking: a chosen stop
	const float Speed = (float)GaspMover->GetVelocity().Size2D();
	const bool bWalk = GetCharacterMovement()->MaxWalkSpeed <= WalkSpeedCm + 1.0f;
	if (WasIn > 0.3f && NowIn < 0.05f && bWalk && Speed > 60.0f && SitPhase == ESitPhase::None) { TryStartStop(); }
}

bool ALedgerSliceCharacter::TryStartStop()
{
	LedgerStop::Read();
	UAnimInstance* Graph = GaspMover->GetMesh()->GetAnimInstance();
	if (Graph == nullptr || LedgerStop::GClips.Num() == 0 || LedgerStop::GSlot.IsNone()) { return false; }
	// his planted foot (in double support the one that came down last) and how far through its stance he is
	int32 Foot = -1;
	if (ContactFor[0] > 0.0f && (ContactFor[1] <= 0.0f || ContactFor[0] <= ContactFor[1])) { Foot = 0; }
	else if (ContactFor[1] > 0.0f) { Foot = 1; }
	if (Foot < 0) { UE_LOG(LogTemp, Display, TEXT("LedgerStop: no foot marked planted; the walk's own stop")); return false; }
	const float Through = FMath::Clamp(ContactFor[Foot] / FMath::Max(StanceSeconds, 0.2f), 0.0f, 1.0f);
	const int32 Quarter = Through < 0.5f ? 0 : 1;   // the planted half of the stride, early or late
	const LedgerStop::FClip* Best = nullptr;
	const LedgerStop::FMoment* At = nullptr;
	float BestScore = 1e9f;
	for (const LedgerStop::FClip& C : LedgerStop::GClips)
	{
		for (const LedgerStop::FMoment& M : C.Moments)
		{
			if (M.Foot != Foot || M.Stance <= 0.0f || M.Left < 60.0f || M.Left > 210.0f) { continue; }
			const float MThrough = M.Down / M.Stance;
			if ((MThrough < 0.5f ? 0 : 1) != Quarter) { continue; }
			// the nearest point in the stance first, then the shortest walk left (he stops soonest)
			const float Score = FMath::Abs(MThrough - Through) * 400.0f + M.Left;
			if (Score < BestScore) { BestScore = Score; Best = &C; At = &M; }
		}
	}
	if (Best == nullptr) { UE_LOG(LogTemp, Display, TEXT("LedgerStop: no moment fits (foot %d, %.2f through); the walk's own stop"), Foot, Through); return false; }
	Best->Seq->bEnableRootMotion = true;
	StopMontage = Graph->PlaySlotAnimationAsDynamicMontage(Best->Seq, LedgerStop::GSlot, 0.2f, 0.25f, 1.0f, 1, -1.0f, At->T);
	UE_LOG(LogTemp, Display, TEXT("LedgerStop: %s from %.2f s (foot %s, %.0f%% through its stance against his %.0f%%, %.0f cm left)"),
		*Best->Seq->GetName(), At->T, Foot == 0 ? TEXT("left") : TEXT("right"), 100.0f * At->Down / At->Stance, 100.0f * Through, At->Left);
	return StopMontage != nullptr;
}
