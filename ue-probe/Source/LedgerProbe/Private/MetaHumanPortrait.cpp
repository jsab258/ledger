// PORTRAITS OF THE CAST, 24 September. Jafar: "Lena, Sam and Rocco, each in a
// close-up and a mid-shot in the street, in daylight, beside the KCD2 people
// frame." -LedgerPortrait on the ordinary launch: the street and its daylight
// as the player sees them, each cast MetaHuman stood on the parade's pavement
// facing the road, idling, and a camera put in front of the face and then
// further back. Frames: ue-portrait-<who>-close.png and -mid.png.
#include "MetaHumanPortrait.h"

#include "Animation/AnimSequenceBase.h"
#include "Camera/CameraActor.h"
#include "Camera/CameraComponent.h"
#include "Components/SkeletalMeshComponent.h"
#include "Containers/Ticker.h"
#include "Engine/Engine.h"
#include "Engine/SkeletalMesh.h"
#include "Engine/World.h"
#include "GameFramework/Pawn.h"
#include "GameFramework/PlayerController.h"
#include "HAL/PlatformTime.h"
#include "Misc/CommandLine.h"
#include "Misc/Paths.h"
#include "ShaderCompiler.h"
#include "UnrealClient.h"

namespace LedgerMhPortrait
{
	const TCHAR* kWho[] = { TEXT("Lena"), TEXT("Sam"), TEXT("Rocco") };
	// EPIC'S OWN IDLE, BODY AND FACE, 24 September: the MetaHuman plugin ships
	// a standing loop on the very skeletons the cast are built on, and a face
	// loop to go with it (blinks, breath, small looks). The elizabeth idle
	// carried over from an old street figure put the hands through the body.
	const TCHAR* kIdle = TEXT("/MetaHumanCharacter/Optional/Animation/TemplateAnimations/Technical_Loops/Idle/mhc_mh001_fmn_b_idle.mhc_mh001_fmn_b_idle");
	const TCHAR* kFaceIdle = TEXT("/MetaHumanCharacter/Optional/Animation/TemplateAnimations/Technical_Loops/Idle/mhc_mh001_fmn_f_idle.mhc_mh001_fmn_f_idle");
	// On the parade's pavement by Mickey's, street metres (x along, z across).
	const double kStandX = 9.5, kStandZ = 4.4, kGroundCm = 12.0;

	FTSTicker::FDelegateHandle GTicker;
	double GStart = 0.0, GPhaseAt = 0.0;
	int32 GAt = 0, GShot = 0;          // who, and which shot (0 close, 1 mid)
	int32 GPhase = 0;                  // 0 wait world, 1 place, 2 settle, 3 shoot, 4 after shot
	TWeakObjectPtr<AActor> GPerson;
	TWeakObjectPtr<ACameraActor> GCam;

	UWorld* GameWorld()
	{
		if (!GEngine) { return nullptr; }
		for (const FWorldContext& Ctx : GEngine->GetWorldContexts())
		{
			if (Ctx.WorldType == EWorldType::Game && Ctx.World() != nullptr) { return Ctx.World(); }
		}
		return nullptr;
	}

	FVector StreetToUE(double X, double Y, double Z) { return FVector((float)(X * 100.0), (float)(Z * 100.0), (float)(Y * 100.0)); }

	void Place(UWorld* World)
	{
		if (GPerson.IsValid()) { GPerson->Destroy(); }
		// -PortraitTake=T2: the cast made to the brief, beside the stand-ins.
		FString Take;
		FParse::Value(FCommandLine::Get(), TEXT("PortraitTake="), Take);
		const FString Name = FString(TEXT("MH_")) + kWho[GAt] + Take;
		UClass* Cls = LoadClass<AActor>(nullptr, *FString::Printf(TEXT("/Game/Ledger/MetaHumans/%s/BP_%s.BP_%s_C"), *Name, *Name, *Name));
		if (Cls == nullptr) { return; }
		FActorSpawnParameters P;
		P.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
		// Facing the road (-Y in this engine is toward the west side): a
		// MetaHuman faces its actor's +Y, so yaw 180 turns it to face -Y.
		AActor* A = World->SpawnActor<AActor>(Cls, StreetToUE(kStandX, 0.0, kStandZ) + FVector(0, 0, kGroundCm), FRotator(0.0f, 180.0f, 0.0f), P);
		if (A == nullptr) { return; }
		UAnimSequenceBase* Idles[] = { LoadObject<UAnimSequenceBase>(nullptr, kIdle), LoadObject<UAnimSequenceBase>(nullptr, kFaceIdle) };
		TArray<USkeletalMeshComponent*> Parts;
		A->GetComponents(Parts);
		for (USkeletalMeshComponent* C : Parts)
		{
			USkeletalMesh* M = C != nullptr ? C->GetSkeletalMeshAsset() : nullptr;
			for (UAnimSequenceBase* Idle : Idles)
			{
				if (M == nullptr || Idle == nullptr || M->GetSkeleton() != Idle->GetSkeleton()) { continue; }
				C->SetAnimationMode(EAnimationMode::AnimationSingleNode);
				C->PlayAnimation(Idle, true);
				C->SetPosition(1.5f, false);
			}
		}
		UE_LOG(LogTemp, Display, TEXT("LedgerPortrait: %s body idle %s, face idle %s"), kWho[GAt],
			Idles[0] != nullptr ? TEXT("loaded") : TEXT("MISSING"), Idles[1] != nullptr ? TEXT("loaded") : TEXT("MISSING"));
		GPerson = A;
	}

	void Aim(UWorld* World)
	{
		if (!GPerson.IsValid()) { return; }
		// THE FACE: the tallest point of the body, less a head's half. The
		// camera stands out toward the road from it.
		const FBox B = GPerson->GetComponentsBoundingBox();
		const FVector Face(GPerson->GetActorLocation().X, GPerson->GetActorLocation().Y, B.Max.Z - 12.0f);
		// Close: head and shoulders, about half a metre tall in frame. Mid: the
		// top of the head to below the waist, about a metre ten. (The first
		// run's 75 cm and 230 cm cut the crown off the one and the face off
		// the other.)
		const bool bClose = GShot == 0;
		const float Back = bClose ? 170.0f : 320.0f;
		const FVector Eye = Face + FVector(bClose ? 25.0f : 40.0f, -Back, bClose ? -4.0f : -15.0f);
		const FVector Look = Face + FVector(0.0f, 0.0f, bClose ? -8.0f : -40.0f);
		if (!GCam.IsValid())
		{
			GCam = World->SpawnActor<ACameraActor>(ACameraActor::StaticClass(), Eye, (Look - Eye).Rotation());
		}
		if (!GCam.IsValid()) { return; }
		GCam->SetActorLocationAndRotation(Eye, (Look - Eye).Rotation());
		// NO SHOT ON A BLINK: every close-up fell at the same point in the
		// face loop, and on take T3 that point was a blink. For a still, the
		// face is held at the loop's first frame; the body keeps idling.
		if (UAnimSequenceBase* FaceIdle = LoadObject<UAnimSequenceBase>(nullptr, kFaceIdle))
		{
			TArray<USkeletalMeshComponent*> Parts;
			GPerson->GetComponents(Parts);
			for (USkeletalMeshComponent* C : Parts)
			{
				USkeletalMesh* M = C != nullptr ? C->GetSkeletalMeshAsset() : nullptr;
				if (M == nullptr || M->GetSkeleton() != FaceIdle->GetSkeleton()) { continue; }
				C->SetPosition(0.0f, false);
				C->SetPlayRate(0.0f);
			}
		}
		GCam->GetCameraComponent()->SetFieldOfView(bClose ? 28.0f : 34.0f);
		if (APlayerController* PC = World->GetFirstPlayerController())
		{
			PC->SetViewTarget(GCam.Get());
			if (APawn* Me = PC->GetPawn()) { Me->SetActorHiddenInGame(true); }
		}
	}

	bool Tick(float)
	{
		const double Now = FPlatformTime::Seconds();
		UWorld* World = GameWorld();
		switch (GPhase)
		{
		case 0:
			if (World == nullptr || World->GetFirstPlayerController() == nullptr || Now - GStart < 8.0) { return true; }
			GPhase = 1;
			return true;
		case 1:
			Place(World);
			GShot = 0;
			Aim(World);
			GPhaseAt = Now;
			GPhase = 2;
			return true;
		case 2:
		{
			// TEXTURES STREAM IN AND SHADERS COMPILE: wait for both, up to two minutes.
			const bool bCompiling = GShaderCompilingManager != nullptr && GShaderCompilingManager->GetNumRemainingJobs() > 0;
			if (Now - GPhaseAt < 6.0 || (bCompiling && Now - GPhaseAt < 120.0)) { return true; }
			GPhase = 3;
			return true;
		}
		case 3:
		{
			const FString Out = FPaths::ConvertRelativePathToFull(FPaths::ProjectDir() / FString::Printf(TEXT("ue-portrait-%s-%s.png"),
				*FString(kWho[GAt]).ToLower(), GShot == 0 ? TEXT("close") : TEXT("mid")));
			FScreenshotRequest::RequestScreenshot(Out, false, false);
			GPhaseAt = Now;
			GPhase = 4;
			return true;
		}
		case 4:
			if (Now - GPhaseAt < 1.0) { return true; }
			if (GShot == 0)
			{
				GShot = 1;
				Aim(World);
				GPhaseAt = Now;
				GPhase = 2;
				return true;
			}
			++GAt;
			if (GAt >= 3)
			{
				FTSTicker::GetCoreTicker().RemoveTicker(GTicker);
				FPlatformMisc::RequestExit(false);
				return false;
			}
			GPhase = 1;
			return true;
		default:
			return false;
		}
	}

	void Start()
	{
		GStart = FPlatformTime::Seconds();
		GTicker = FTSTicker::GetCoreTicker().AddTicker(FTickerDelegate::CreateStatic(&Tick), 0.0f);
	}
}
