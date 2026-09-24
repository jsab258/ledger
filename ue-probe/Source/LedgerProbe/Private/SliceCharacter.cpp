#include "SliceCharacter.h"

#include "LocomotionAnim.h"

#include "Animation/AnimSequenceBase.h"
#include "Camera/CameraComponent.h"
#include "Components/CapsuleComponent.h"
#include "Components/InputComponent.h"
#include "Components/SkeletalMeshComponent.h"
#include "Engine/SkeletalMesh.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "GameFramework/SpringArmComponent.h"
#include "InputCoreTypes.h"
#include "NavigationInvokerComponent.h"
#include "NavigationSystem.h"
#include "NavMesh/NavMeshBoundsVolume.h"
#include "Components/BrushComponent.h"
#include "PhysicsEngine/BodySetup.h"
#include "TimerManager.h"

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

void ALedgerSliceCharacter::BeginPlay()
{
	Super::BeginPlay();
	MarkStreetWalkable();
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
	PlayerInputComponent->BindAxisKey(EKeys::W, this, &ALedgerSliceCharacter::MoveForward);
	PlayerInputComponent->BindAxisKey(EKeys::S, this, &ALedgerSliceCharacter::MoveBackward);
	PlayerInputComponent->BindAxisKey(EKeys::D, this, &ALedgerSliceCharacter::MoveRight);
	PlayerInputComponent->BindAxisKey(EKeys::A, this, &ALedgerSliceCharacter::MoveLeft);
	PlayerInputComponent->BindAxisKey(EKeys::MouseX, this, &ALedgerSliceCharacter::LookYaw);
	PlayerInputComponent->BindAxisKey(EKeys::MouseY, this, &ALedgerSliceCharacter::LookPitch);
	PlayerInputComponent->BindKey(EKeys::LeftShift, IE_Pressed, this, &ALedgerSliceCharacter::RunPressed);
	PlayerInputComponent->BindKey(EKeys::LeftShift, IE_Released, this, &ALedgerSliceCharacter::RunReleased);
	PlayerInputComponent->BindKey(EKeys::E, IE_Pressed, this, &ALedgerSliceCharacter::RequestAct);
	PlayerInputComponent->BindKey(EKeys::T, IE_Pressed, this, &ALedgerSliceCharacter::RequestTalk);
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
