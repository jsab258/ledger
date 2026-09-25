// PORTRAITS OF THE CAST, 24 September. Jafar: "Lena, Sam and Rocco, each in a
// close-up and a mid-shot in the street, in daylight, beside the KCD2 people
// frame." -LedgerPortrait on the ordinary launch: the street and its daylight
// as the player sees them, each cast MetaHuman stood on the parade's pavement
// facing the road, idling, and a camera put in front of the face and then
// further back. Frames: ue-portrait-<who>-close.png and -mid.png.
//
// CANDIDATES, 25 September. Jafar's ruling: faces are cast in MetaHuman first,
// several candidates per character, each shown front, profile and speaking in
// the game's own light; the one he approves becomes the concept.
// -PortraitTakes=C1,C2,C3,C4,C5 photographs every take of every one of the
// three: a front close-up, a profile, and a speaking sequence, the face played
// through its line's animation (tools/ue/speech_faces.py, from the line's
// audio) one frame at a time, SpeakFps a second, each frame its own picture;
// tools/ue/candidate_sheet.py packs them for the approval page, which plays
// them with the line's audio. -PortraitOut=DIR puts the pictures there.
//
// A HAT, 25 September: the first garment on the free route (FreeSewing's
// flat cap, sewn in Blender by tools/meshgen/blender/sew_cap.py) worn in the
// street. -PortraitHat=<static mesh> sets it on the head bone: its origin is
// the hat line's centre, -HatAt=forward,up (cm from the head bone, the
// wearer's way round), -HatTilt=degrees forward, -HatScale=s.
// -PortraitWho=<asset name, as kWho spells it> photographs only that one.
//
// THE EYES, 25 September, afternoon: Jafar asked why Sheila looked high. The
// stills froze Epic's face idle on its first frame, which has the lids half
// down and the eyes rolled up and aside. -PortraitFaceAt=seconds holds it at
// another moment; -PortraitFaceScan photographs the idle every half second
// (ue-scan-<who>-<take>/) to choose one. -PortraitSpeech=<suffix> picks a
// variant of the speaking animation (tools/ue/speech_faces.py).
//
// IN THE GAME, 25 September (evening): Jafar asked to see each character as
// the game has them, beside the candidate he approved. -PortraitInGame, with
// the game's -Encounter=live -CastAllNow, spawns nobody: it finds the cast
// the encounter placed (their approved take, their clothes, their idle) and
// photographs each where the game stands them, in that place's light, from
// in front of their own face: a close-up, the speaking line, and a wider
// shot. Pictures ue-portrait-ingame-<who>-<shot>.png.
//
// WHY FACES READ EAST ASIAN, 25 September (night): even Epic's European preset
// Vivian, built here, reads narrower-eyed than Epic's own picture of her. Three
// switches take away one difference each, with no rebuild: -PortraitNoHair
// hides the head hair (never brows or lashes), -PortraitStudio adds a plain
// key and fill light at the face, -PortraitFaceRest shows the face with no
// animation, at rest.
#include "MetaHumanPortrait.h"
#include "LedgerJacket.h"

#include "Animation/AnimSequenceBase.h"
#include "Camera/CameraActor.h"
#include "Camera/CameraComponent.h"
#include "Components/SkeletalMeshComponent.h"
#include "Components/StaticMeshComponent.h"
#include "Containers/Ticker.h"
#include "Engine/Engine.h"
#include "Engine/SkeletalMesh.h"
#include "Engine/StaticMesh.h"
#include "Engine/World.h"
#include "GameFramework/Pawn.h"
#include "GameFramework/PlayerController.h"
#include "HAL/PlatformTime.h"
#include "Misc/CommandLine.h"
#include "Misc/Paths.h"
#include "ShaderCompiler.h"
#include "UnrealClient.h"
#include "EngineUtils.h"
#include "Engine/PointLight.h"
#include "Components/PointLightComponent.h"

namespace LedgerMhPortrait
{
	const TCHAR* kWho[] = { TEXT("Lena"), TEXT("Sam"), TEXT("Rocco") };   // names-gate: allow (asset names MH_<who>T2)
	// The line each speaks, by the same order: tools/ue/speech_faces.py's
	// animation of the casting sheet's first line in the voice Jafar picked.
	const TCHAR* kSpeech[] = { TEXT("AS_sheila_dunn"), TEXT("AS_darren_milner"), TEXT("AS_ron_kirby") };
	// EPIC'S OWN IDLE, BODY AND FACE, 24 September: the MetaHuman plugin ships
	// a standing loop on the very skeletons the cast are built on, and a face
	// loop to go with it (blinks, breath, small looks). The elizabeth idle
	// carried over from an old street figure put the hands through the body.
	const TCHAR* kIdle = TEXT("/MetaHumanCharacter/Optional/Animation/TemplateAnimations/Technical_Loops/Idle/mhc_mh001_fmn_b_idle.mhc_mh001_fmn_b_idle");
	const TCHAR* kFaceIdle = TEXT("/MetaHumanCharacter/Optional/Animation/TemplateAnimations/Technical_Loops/Idle/mhc_mh001_fmn_f_idle.mhc_mh001_fmn_f_idle");
	// On the parade's pavement by Mickey's, street metres (x along, z across).
	const double kStandX = 9.5, kStandZ = 4.4, kGroundCm = 12.0;
	const float SpeakFps = 15.0f;

	enum class EShot : uint8 { Close, Mid, Front, Profile, Speak, Scan };

	struct FJob { int32 Who; FString Take; };
	TArray<FJob> GJobs;
	TArray<EShot> GShots;
	FString GOut;
	bool GCandidates = false;         // -PortraitTakes: pictures named by take too
	FString GHat;                     // -PortraitHat: a static mesh worn on the head
	float GHatForward = 1.0f, GHatUp = 10.5f, GHatTilt = 0.0f, GHatScale = 1.0f;
	float GFaceAt = 0.0f;              // -PortraitFaceAt: the face idle's moment for a still
	FString GSpeech = TEXT("_n");     // -PortraitSpeech: the speaking animation's variant; _n, the neutral mood, by default
	bool GScan = false;               // the shot running is a scan of the face idle
	bool GInGame = false;             // -PortraitInGame: the game's own cast, where it stands
	bool GNoHair = false, GStudio = false, GFaceRest = false;   // the look tests
	float GStudioCd = 8.0f;           // -PortraitStudioCd: the key light's candela (60 blew the picture out)
	TArray<TWeakObjectPtr<AActor>> GLights;

	FTSTicker::FDelegateHandle GTicker;
	double GStart = 0.0, GPhaseAt = 0.0;
	int32 GAt = 0, GShot = 0;          // which job, and which of its shots
	int32 GPhase = 0;                  // 0 wait world, 1 place, 2 settle, 3 shoot, 4 after shot, 5 speak frame, 6 after frame
	int32 GFrame = 0, GFrames = 0;
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

	TArray<USkeletalMeshComponent*> FaceParts()
	{
		TArray<USkeletalMeshComponent*> Out;
		UAnimSequenceBase* FaceIdle = LoadObject<UAnimSequenceBase>(nullptr, kFaceIdle);
		if (!GPerson.IsValid() || FaceIdle == nullptr) { return Out; }
		TArray<USkeletalMeshComponent*> Parts;
		GPerson->GetComponents(Parts);
		for (USkeletalMeshComponent* C : Parts)
		{
			USkeletalMesh* M = C != nullptr ? C->GetSkeletalMeshAsset() : nullptr;
			if (M != nullptr && M->GetSkeleton() == FaceIdle->GetSkeleton()) { Out.Add(C); }
		}
		return Out;
	}

	void Place(UWorld* World)
	{
		if (GInGame)
		{
			// The game's own: the actor the encounter dressed as this character
			// (tagged LedgerCast), never a stand-in elsewhere in the street.
			GPerson = nullptr;
			const FString Prefix = FString(TEXT("BP_MH_")) + kWho[GJobs[GAt].Who];
			for (TActorIterator<AActor> It(World); It; ++It)
			{
				if (It->Tags.Contains(TEXT("LedgerCast")) && It->GetClass()->GetName().StartsWith(Prefix)) { GPerson = *It; break; }
			}
			UE_LOG(LogTemp, Display, TEXT("LedgerPortrait: in game, %s is %s"), kWho[GJobs[GAt].Who],
				GPerson.IsValid() ? *GPerson->GetClass()->GetName() : TEXT("NOT FOUND"));
			return;
		}
		if (GPerson.IsValid()) { GPerson->Destroy(); }
		const FJob& J = GJobs[GAt];
		const FString Name = FString(TEXT("MH_")) + kWho[J.Who] + J.Take;
		UClass* Cls = LoadClass<AActor>(nullptr, *FString::Printf(TEXT("/Game/Ledger/MetaHumans/%s/BP_%s.BP_%s_C"), *Name, *Name, *Name));
		if (Cls == nullptr)
		{
			UE_LOG(LogTemp, Display, TEXT("LedgerPortrait: %s NOT FOUND"), *Name);
			return;
		}
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
		LedgerJacket::Wear(A, kWho[J.Who]);
		UE_LOG(LogTemp, Display, TEXT("LedgerPortrait: %s body idle %s, face idle %s"), *Name,
			Idles[0] != nullptr ? TEXT("loaded") : TEXT("MISSING"), Idles[1] != nullptr ? TEXT("loaded") : TEXT("MISSING"));
		GPerson = A;
	}

	// Every part playing one of the idles, held at one moment of them.
	void HoldIdles(float At)
	{
		if (!GPerson.IsValid()) { return; }
		TArray<USkeletalMeshComponent*> Parts;
		GPerson->GetComponents(Parts);
		for (USkeletalMeshComponent* C : Parts)
		{
			if (C == nullptr || C->GetSingleNodeInstance() == nullptr) { continue; }
			C->SetPosition(At, false);
			C->SetPlayRate(0.0f);
		}
	}

	// THE HAT on the body's head bone, set square to the wearer (a MetaHuman
	// faces its actor's +Y, as the cap faces its own +Y), then carried by the
	// bone as the head moves.
	// THE LOOK TESTS (see the top of this file).
	void LookTests(UWorld* World, const FVector& Face)
	{
		if (!GPerson.IsValid()) { return; }
		if (GNoHair)
		{
			TArray<USceneComponent*> Parts;
			GPerson->GetComponents(Parts);
			for (USceneComponent* C : Parts)
			{
				const FString N = C != nullptr ? C->GetName() : FString();
				if (N.Equals(TEXT("Hair"), ESearchCase::IgnoreCase) || N.StartsWith(TEXT("Hair"), ESearchCase::IgnoreCase))
				{
					C->SetVisibility(false, true);
				}
			}
		}
		if (GFaceRest)
		{
			for (USkeletalMeshComponent* C : FaceParts()) { C->Stop(); C->SetAnimation(nullptr); }
		}
		if (GStudio && GLights.Num() == 0)
		{
			// A photographer's key from the camera's left and above, and a softer fill from its right.
			const FRotator Facing(0.0f, GPerson->GetActorRotation().Yaw - 180.0f, 0.0f);
			const struct { FVector At; float Candela; } Rig[] = { { FVector(-70.0f, -110.0f, 45.0f), GStudioCd }, { FVector(80.0f, -120.0f, 0.0f), GStudioCd / 3.0f } };
			for (const auto& L : Rig)
			{
				APointLight* Light = World->SpawnActor<APointLight>(Face + Facing.RotateVector(L.At), FRotator::ZeroRotator);
				if (Light == nullptr) { continue; }
				Light->PointLightComponent->SetIntensityUnits(ELightUnits::Candelas);
				Light->PointLightComponent->SetIntensity(L.Candela);
				Light->PointLightComponent->SetAttenuationRadius(400.0f);
				Light->PointLightComponent->SetSourceRadius(25.0f);
				Light->PointLightComponent->SetCastShadows(true);
				GLights.Add(Light);
			}
		}
	}

	void WearHat()
	{
		if (GHat.IsEmpty() || !GPerson.IsValid() || GPerson->Tags.Contains(TEXT("LedgerHat"))) { return; }
		GPerson->Tags.Add(TEXT("LedgerHat"));
		UStaticMesh* Mesh = LoadObject<UStaticMesh>(nullptr, *GHat);
		TArray<USkeletalMeshComponent*> Faces = FaceParts();
		TArray<USkeletalMeshComponent*> Parts;
		GPerson->GetComponents(Parts);
		USkeletalMeshComponent* Body = nullptr;
		for (USkeletalMeshComponent* C : Parts)
		{
			if (C != nullptr && !Faces.Contains(C) && C->DoesSocketExist(TEXT("head"))) { Body = C; break; }
		}
		if (Mesh == nullptr || Body == nullptr)
		{
			UE_LOG(LogTemp, Display, TEXT("LedgerPortrait: hat %s, head bone %s"), Mesh != nullptr ? TEXT("found") : TEXT("MISSING"), Body != nullptr ? TEXT("found") : TEXT("MISSING"));
			return;
		}
		UStaticMeshComponent* Hat = NewObject<UStaticMeshComponent>(GPerson.Get(), TEXT("LedgerHat"));
		Hat->SetStaticMesh(Mesh);
		Hat->SetCollisionEnabled(ECollisionEnabled::NoCollision);
		Hat->RegisterComponent();
		const FQuat Facing(GPerson->GetActorRotation());
		const FVector At = Body->GetSocketLocation(TEXT("head")) + Facing.RotateVector(FVector(0.0f, GHatForward, GHatUp));
		Hat->SetWorldLocationAndRotation(At, Facing * FQuat(FRotator(0.0f, 0.0f, GHatTilt)));
		Hat->SetWorldScale3D(FVector(GHatScale));
		Hat->AttachToComponent(Body, FAttachmentTransformRules::KeepWorldTransform, TEXT("head"));
		UE_LOG(LogTemp, Display, TEXT("LedgerPortrait: hat on %s at %s"), *GPerson->GetName(), *At.ToString());
	}

	FString Stem();

	void Aim(UWorld* World)
	{
		if (!GPerson.IsValid()) { return; }
		WearHat();
		const EShot Shot = GShots[GShot];
		// THE FACE: the tallest point of the body, less a head's half. The
		// camera stands out toward the road from it.
		const FBox B = GPerson->GetComponentsBoundingBox();
		const FVector Face(GPerson->GetActorLocation().X, GPerson->GetActorLocation().Y, B.Max.Z - 12.0f);
		// The offsets below are for a person facing -Y (yaw 180); in the game
		// they are turned to however the person stands.
		const FRotator Turn(0.0f, GInGame ? GPerson->GetActorRotation().Yaw - 180.0f : 0.0f, 0.0f);
		// Close: head and shoulders, about half a metre tall in frame. Mid: the
		// top of the head to below the waist, about a metre ten. (The first
		// run's 75 cm and 230 cm cut the crown off the one and the face off
		// the other.) Front and Speak are straight on; Profile is from the
		// side, the camera along the street.
		const bool bMid = Shot == EShot::Mid;
		const float Back = bMid ? 320.0f : 170.0f;
		FVector Eye;
		FVector Look = Face + FVector(0.0f, 0.0f, bMid ? -40.0f : -8.0f);
		switch (Shot)
		{
		case EShot::Close: Eye = Face + FVector(25.0f, -Back, -4.0f); break;
		case EShot::Mid: Eye = Face + FVector(40.0f, -Back, -15.0f); break;
		case EShot::Front: Eye = Face + FVector(0.0f, -Back, -4.0f); break;
		case EShot::Speak: Eye = Face + FVector(0.0f, -Back - 20.0f, -6.0f); Look = Face + FVector(0.0f, 0.0f, -12.0f); break;
		// THE PROFILE turns the person, not the camera: from either side along
		// the pavement the first runs framed another person's head, or a
		// neighbour beside her. A quarter turn, the camera where the front
		// shot stands, the same plain doors behind.
		case EShot::Profile: default: Eye = Face + FVector(0.0f, -Back, -4.0f); break;
		}
		Eye = Face + Turn.RotateVector(Eye - Face);
		Look = Face + Turn.RotateVector(Look - Face);
		// A CLEAR LINE TO THE FACE, in the game: where the person stands close to
		// a wall the camera came out inside it and the picture was black (Ron in
		// the yard). The camera swings round the face, a little at a time, to the
		// first place with nothing between it and the face.
		if (GInGame)
		{
			FCollisionQueryParams Q(TEXT("LedgerPortraitSight"), false, GPerson.Get());
			const FVector Out = Eye - Face;
			for (float Swing : { 0.0f, 25.0f, -25.0f, 50.0f, -50.0f, 75.0f, -75.0f, 100.0f, -100.0f })
			{
				const FVector Try = Face + FRotator(0.0f, Swing, 0.0f).RotateVector(Out);
				// From the camera toward the face: the face is inside the game's own
				// hidden stand-in body, so a hit within 40 cm of it is the person.
				FHitResult Hit;
				const bool bBlocked = World->LineTraceSingleByChannel(Hit, Try, Face, ECC_Visibility, Q)
					&& FVector::Dist(Hit.ImpactPoint, Face) > 40.0f;
				if (!bBlocked)
				{
					Eye = Try;
					UE_LOG(LogTemp, Display, TEXT("LedgerPortrait: %s camera swung %.0f degrees for a clear view"), *Stem(), Swing);
					break;
				}
			}
		}
		if (!GInGame) { GPerson->SetActorRotation(FRotator(0.0f, Shot == EShot::Profile ? 90.0f : 180.0f, 0.0f)); }
		if (!GCam.IsValid())
		{
			GCam = World->SpawnActor<ACameraActor>(ACameraActor::StaticClass(), Eye, (Look - Eye).Rotation());
		}
		if (!GCam.IsValid()) { return; }
		GCam->SetActorLocationAndRotation(Eye, (Look - Eye).Rotation());
		// NO SHOT ON A BLINK: every close-up fell at the same point in the
		// face loop, and on take T3 that point was a blink. For a still, the
		// face is held at the loop's first frame; the body keeps idling.
		// Body and face together: Epic's two idles are a pair, and holding the
		// face alone while the body went on tipped the head against the neck.
		HoldIdles(GFaceAt);
		LookTests(World, Face);
		GCam->GetCameraComponent()->SetFieldOfView(bMid ? 34.0f : 28.0f);
		if (APlayerController* PC = World->GetFirstPlayerController())
		{
			PC->SetViewTarget(GCam.Get());
			if (APawn* Me = PC->GetPawn())
			{
				// OUT OF THE PICTURE, not only hidden: the player's figure
				// follows the pawn and is its own actor, so hiding the pawn
				// left a head in the profile shot. Twenty metres along the
				// pavement, well clear of any camera here.
				Me->SetActorHiddenInGame(true);
				if ((GCandidates || GInGame) && !Me->Tags.Contains(TEXT("LedgerPortraitMoved")))
				{
					Me->SetActorLocation(Me->GetActorLocation() + FVector(2000.0f, 0.0f, 0.0f), false, nullptr, ETeleportType::TeleportPhysics);
					Me->Tags.Add(TEXT("LedgerPortraitMoved"));
				}
			}
		}
	}

	FString ShotName(EShot S)
	{
		switch (S)
		{
		case EShot::Close: return TEXT("close");
		case EShot::Mid: return TEXT("mid");
		case EShot::Front: return TEXT("front");
		case EShot::Profile: return TEXT("profile");
		case EShot::Scan: return TEXT("scan");
		default: return TEXT("speak");
		}
	}

	FString Stem()
	{
		const FJob& J = GJobs[GAt];
		if (GInGame) { return FString(TEXT("ingame-")) + FString(kWho[J.Who]).ToLower(); }
		return FString(kWho[J.Who]).ToLower() + (GCandidates ? TEXT("-") + J.Take.ToLower() : FString());
	}

	// THE SPEAKING SHOT: the line's face animation, stepped by hand so every
	// picture is exactly one frame apart whatever the game's frame rate.
	bool StartSpeaking()
	{
		const FString Name = FString(kSpeech[GJobs[GAt].Who]) + GSpeech;
		const FString Path = FString::Printf(TEXT("/Game/Ledger/MetaHumans/Speech/%s.%s"), *Name, *Name);
		// A scan steps through the face idle instead, every half second.
		UAnimSequenceBase* Line = LoadObject<UAnimSequenceBase>(nullptr, GScan ? kFaceIdle : *Path);
		TArray<USkeletalMeshComponent*> Faces = FaceParts();
		if (Line == nullptr || Faces.Num() == 0)
		{
			UE_LOG(LogTemp, Display, TEXT("LedgerPortrait: %s no speaking shot (line %s, face %d)"), *Stem(),
				Line != nullptr ? TEXT("found") : TEXT("MISSING"), Faces.Num());
			return false;
		}
		for (USkeletalMeshComponent* C : Faces)
		{
			C->PlayAnimation(Line, false);
			C->SetPlayRate(0.0f);
			C->SetPosition(0.0f, false);
		}
		GFrame = 0;
		GFrames = FMath::Max(1, FMath::FloorToInt(Line->GetPlayLength() * (GScan ? 2.0f : SpeakFps)));
		UE_LOG(LogTemp, Display, TEXT("LedgerPortrait: %s speaks %s, %d frames"), *Stem(), kSpeech[GJobs[GAt].Who], GFrames);
		return true;
	}

	void NextJobOrQuit()
	{
		++GAt;
		GShot = 0;
		if (GAt >= GJobs.Num())
		{
			FTSTicker::GetCoreTicker().RemoveTicker(GTicker);
			FPlatformMisc::RequestExit(false);
			return;
		}
		GPhase = 1;
	}

	bool Tick(float)
	{
		const double Now = FPlatformTime::Seconds();
		UWorld* World = GameWorld();
		switch (GPhase)
		{
		case 0:
			if (World == nullptr || World->GetFirstPlayerController() == nullptr || Now - GStart < 8.0) { return true; }
			// In the game, the encounter dresses its cast a little after the street
			// loads: wait for all three (up to two minutes) before the first picture.
			if (GInGame && Now - GStart < 120.0)
			{
				int32 Cast = 0;
				for (TActorIterator<AActor> It(World); It; ++It) { if (It->Tags.Contains(TEXT("LedgerCast"))) { ++Cast; } }
				if (Cast < 3) { return true; }
			}
			GPhase = 1;
			return true;
		case 1:
			Place(World);
			if (!GPerson.IsValid()) { NextJobOrQuit(); return true; }
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
			if (GShots[GShot] == EShot::Speak)
			{
				GPhase = StartSpeaking() ? 5 : 4;
				GPhaseAt = Now;
				return true;
			}
			if (GShots[GShot] == EShot::Scan)
			{
				GScan = true;
				GPhase = StartSpeaking() ? 5 : 4;
				GPhaseAt = Now;
				return true;
			}
			GPhase = 3;
			return true;
		}
		case 3:
		{
			const FString Out = FPaths::ConvertRelativePathToFull(GOut / FString::Printf(TEXT("ue-portrait-%s-%s.png"), *Stem(), *ShotName(GShots[GShot])));
			FScreenshotRequest::RequestScreenshot(Out, false, false);
			GPhaseAt = Now;
			GPhase = 4;
			return true;
		}
		case 4:
			if (Now - GPhaseAt < 1.0) { return true; }
			if (GShot + 1 < GShots.Num())
			{
				++GShot;
				Aim(World);
				GPhaseAt = Now;
				GPhase = 2;
				return true;
			}
			NextJobOrQuit();
			return true;
		case 5:
		{
			// One frame of the line: pose, then the picture of it.
			if (GScan) { HoldIdles(GFrame * 0.5f); }
			else { for (USkeletalMeshComponent* C : FaceParts()) { C->SetPosition((float)GFrame / SpeakFps, false); } }
			const FString Out = FPaths::ConvertRelativePathToFull(GOut / FString::Printf(TEXT("ue-%s-%s/f%04d.png"), GScan ? TEXT("scan") : TEXT("speak"), *Stem(), GFrame));
			FScreenshotRequest::RequestScreenshot(Out, false, false);
			GPhaseAt = Now;
			GPhase = 6;
			return true;
		}
		case 6:
			// Two engine frames per picture, so each request is taken before the next.
			if (Now - GPhaseAt < 0.12) { return true; }
			if (++GFrame < GFrames) { GPhase = 5; return true; }
			GScan = false;
			GPhaseAt = Now;
			GPhase = 4;
			return true;
		default:
			return false;
		}
	}

	void Start()
	{
		GStart = FPlatformTime::Seconds();
		GOut = FPaths::ProjectDir();
		FParse::Value(FCommandLine::Get(), TEXT("PortraitOut="), GOut);
		FString Takes;
		if (FParse::Value(FCommandLine::Get(), TEXT("PortraitTakes="), Takes, false))
		{
			// The candidates: every take, each of the three, front, profile, speaking.
			TArray<FString> List;
			Takes.ParseIntoArray(List, TEXT(","), true);
			for (const FString& T : List) { for (int32 W = 0; W < 3; ++W) { GJobs.Add({ W, T.TrimStartAndEnd() }); } }
			GShots = { EShot::Front, EShot::Profile, EShot::Speak };
			GCandidates = true;
		}
		else
		{
			// -PortraitTake=T2: the cast made to the brief, beside the stand-ins.
			FString Take;
			FParse::Value(FCommandLine::Get(), TEXT("PortraitTake="), Take);
			for (int32 W = 0; W < 3; ++W) { GJobs.Add({ W, Take }); }
			GShots = { EShot::Close, EShot::Mid };
		}
		if (FParse::Value(FCommandLine::Get(), TEXT("PortraitHat="), GHat))
		{
			// The hat: front, profile, and the street behind.
			GShots = { EShot::Front, EShot::Profile, EShot::Mid };
			FString At, F, U;
			if (FParse::Value(FCommandLine::Get(), TEXT("HatAt="), At) && At.Split(TEXT(","), &F, &U))
			{
				GHatForward = FCString::Atof(*F);
				GHatUp = FCString::Atof(*U);
			}
			FParse::Value(FCommandLine::Get(), TEXT("HatTilt="), GHatTilt);
			FParse::Value(FCommandLine::Get(), TEXT("HatScale="), GHatScale);
		}
		FParse::Value(FCommandLine::Get(), TEXT("PortraitFaceAt="), GFaceAt);
		GNoHair = FParse::Param(FCommandLine::Get(), TEXT("PortraitNoHair"));
		GStudio = FParse::Param(FCommandLine::Get(), TEXT("PortraitStudio"));
		FParse::Value(FCommandLine::Get(), TEXT("PortraitStudioCd="), GStudioCd);
		GFaceRest = FParse::Param(FCommandLine::Get(), TEXT("PortraitFaceRest"));
		FParse::Value(FCommandLine::Get(), TEXT("PortraitSpeech="), GSpeech);
		if (FParse::Param(FCommandLine::Get(), TEXT("PortraitFaceScan"))) { GShots = { EShot::Scan }; }
		if (FParse::Param(FCommandLine::Get(), TEXT("PortraitInGame")))
		{
			GInGame = true;
			GJobs.Reset();
			for (int32 W = 0; W < 3; ++W) { GJobs.Add({ W, FString() }); }
			GShots = { EShot::Front, EShot::Speak, EShot::Mid };
		}
		FString Who;
		if (FParse::Value(FCommandLine::Get(), TEXT("PortraitWho="), Who))
		{
			GJobs.RemoveAll([&Who](const FJob& J) { return !Who.Equals(kWho[J.Who], ESearchCase::IgnoreCase); });
		}
		GTicker = FTSTicker::GetCoreTicker().AddTicker(FTickerDelegate::CreateStatic(&Tick), 0.0f);
	}
}
