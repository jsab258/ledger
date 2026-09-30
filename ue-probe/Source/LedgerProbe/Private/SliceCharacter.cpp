#include "SliceCharacter.h"
#include "HAL/PlatformMisc.h"
#include "Kismet/GameplayStatics.h"

#include "LocomotionAnim.h"

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
#include "InputCoreTypes.h"
#include "NavigationInvokerComponent.h"
#include "NavigationSystem.h"
#include "NavMesh/NavMeshBoundsVolume.h"
#include "Components/BrushComponent.h"
#include "Components/BoxComponent.h"
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
	if (const APlayerController* KeysPC = Cast<APlayerController>(GetController()))
	{
		const float Fwd = (KeysPC->IsInputKeyDown(EKeys::W) ? 1.0f : 0.0f) - (KeysPC->IsInputKeyDown(EKeys::S) ? 1.0f : 0.0f);
		const float Side = (KeysPC->IsInputKeyDown(EKeys::D) ? 1.0f : 0.0f) - (KeysPC->IsInputKeyDown(EKeys::A) ? 1.0f : 0.0f);
		MoveForward(Fwd);
		MoveRight(Side);
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
		GetMesh()->SetVisibility(!bClose, true);
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
	if (Loco == nullptr || StepClips.Num() == 0 || DeltaSeconds <= 0.0f) { return; }
	StepClock += DeltaSeconds;
	UWorld* World = GetWorld();
	if (StepsRecordingUntil > 0.0f && StepClock >= StepsRecordingUntil && World != nullptr)
	{
		UAudioMixerBlueprintLibrary::StopRecordingOutput(World, EAudioRecordingExportType::WavFile,
			TEXT("ue-steps"), FPaths::ConvertRelativePathToFull(FPaths::ProjectDir()));
		StepsRecordingUntil = -1.0f;
		UE_LOG(LogTemp, Log, TEXT("LedgerSteps: the steps' sound written to ue-steps.wav"));
	}
	float WalkT = 0.0f, RunT = 0.0f;
	if (!Loco->ClipTimes(WalkT, RunT)) { return; }
	const float Speed = GetVelocity().Size2D();
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
		if (!bPassed) { continue; }
		// NEVER TWO AT ONCE, and never one foot twice running within less
		// than its own stride (a change of clip right on a landing).
		if (LastStepAt >= 0.0f && StepClock - LastStepAt < 0.18f) { continue; }
		if (F == LastStepFoot && StepClock - LastStepAt < 0.6f) { continue; }
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
				bRunClip ? TEXT("run") : TEXT("walk"), T);
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
	M->SetAnimInstanceClass(ULedgerLocomotionAnim::StaticClass());
	if (ULedgerLocomotionAnim* A = Cast<ULedgerLocomotionAnim>(M->GetAnimInstance()))
	{
		A->Setup(Clips[0], Clips[1] != nullptr ? Clips[1] : Clips[0], Clips[2] != nullptr ? Clips[2] : Clips[1],
		         WalkSpeedCm, RunSpeedCm);
		M->InitAnim(true);
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
void ALedgerSliceCharacter::LookYaw(float Value) { AddControllerYawInput(Value); }
void ALedgerSliceCharacter::LookPitch(float Value) { AddControllerPitchInput(-Value); }
void ALedgerSliceCharacter::RunPressed() { GetCharacterMovement()->MaxWalkSpeed = RunSpeedCm; }
void ALedgerSliceCharacter::RunReleased() { GetCharacterMovement()->MaxWalkSpeed = WalkSpeedCm; }
void ALedgerSliceCharacter::RequestAct() { ++ActRequests; }
void ALedgerSliceCharacter::RequestTalk() { ++TalkRequests; }
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
