// THE CONVERSATION LIGHT, 28 September. Jafar's list, item 3: "one soft light,
// only on the character being spoken to, off to one side of the camera, on a
// lighting channel of its own, with its indirect and fog contribution off, and
// a faint light in the eyes; measure it against a budget of half a
// millisecond." Following production/research/character-pipeline/
// clothing-and-face-lighting-2026-09-27.md: the street's overcast light is
// flat and from above, so a face in it loses its eyelid crease and its eyes go
// dark; a key from the side of the camera gives the face its planes back.
//
// The rig: a movable soft spot light above and to one side of the camera,
// aimed at the face, unshadowed to begin with; and a dim rectangular eye light
// at the camera whose diffuse part is scaled almost to nothing, so it shows in
// the eyes without flattening the skin. Both on lighting channel 1 only, with
// their indirect and volumetric (fog) contributions at zero. The person spoken
// to is put on channels 0 and 1 while the rig is on; everything else stays on
// channel 0, so no one else is lit by it. Only one person is lit at a time.
//
// Key() places the rig for a camera at Eye looking at Face; Off() removes it
// and gives the person back channel 0 alone.
//
// FULL DETAIL WHILE SPOKEN TO: the research found MetaHuman's face loses its
// micro normals at LOD1 and its skin shading at LOD4, so the person spoken
// to is held at LOD0 (their LOD sync's ForcedLOD) while the rig is on.
#pragma once

#include "Components/MeshComponent.h"
#include "Components/RectLightComponent.h"
#include "Components/SpotLightComponent.h"
#include "Engine/DirectionalLight.h"
#include "Components/LightComponent.h"
#include "Components/LODSyncComponent.h"
#include "Engine/World.h"
#include "EngineUtils.h"
#include "GameFramework/Actor.h"
#include "Misc/CommandLine.h"

namespace LedgerTalkLight
{
	struct FRig
	{
		TWeakObjectPtr<AActor> Holder;
		TWeakObjectPtr<USpotLightComponent> Key;
		TWeakObjectPtr<URectLightComponent> Eyes;
		TWeakObjectPtr<AActor> Person;
	};
	inline FRig& Rig() { static FRig R; return R; }

	// -TalkKeyCd= and -TalkEyeCd= tune the two lights without a rebuild.
	inline float KeyCandela() { float V = 6.0f; FParse::Value(FCommandLine::Get(), TEXT("TalkKeyCd="), V); return V; }
	inline float EyeCandela() { float V = 2.0f; FParse::Value(FCommandLine::Get(), TEXT("TalkEyeCd="), V); return V; }

	inline void Channels(AActor* A, bool bLit)
	{
		if (A == nullptr) { return; }
		TArray<UPrimitiveComponent*> Parts;
		A->GetComponents(Parts);
		for (UPrimitiveComponent* C : Parts)
		{
			if (C != nullptr) { C->SetLightingChannels(true, bLit, false); }
		}
		TArray<ULODSyncComponent*> Syncs;
		A->GetComponents(Syncs);
		for (ULODSyncComponent* L : Syncs)
		{
			if (L != nullptr) { L->ForcedLOD = bLit ? 0 : -1; }
		}
	}

	inline void Off()
	{
		FRig& R = Rig();
		if (R.Holder.IsValid()) { UE_LOG(LogTemp, Display, TEXT("LedgerTalkLight: off %s"), R.Person.IsValid() ? *R.Person->GetClass()->GetName() : TEXT("(gone)")); }
		if (R.Person.IsValid()) { Channels(R.Person.Get(), false); }
		if (R.Holder.IsValid()) { R.Holder->Destroy(); }
		R = FRig();
	}

	// Which side of the camera the key sits: the side the street's sun is on,
	// so the added light agrees with the world's instead of fighting it.
	inline float SunSide(UWorld* World, const FVector& Eye, const FVector& Face)
	{
		ADirectionalLight* Sun = nullptr;
		for (TActorIterator<ADirectionalLight> It(World); It; ++It)
		{
			if (Sun == nullptr || It->GetLightComponent()->Intensity > Sun->GetLightComponent()->Intensity) { Sun = *It; }
		}
		if (Sun == nullptr) { return 1.0f; }
		const FVector ToSun = -Sun->GetActorForwardVector();
		const FVector Look = (Face - Eye).GetSafeNormal2D();
		return FVector::CrossProduct(Look, ToSun).Z >= 0.0f ? 1.0f : -1.0f;
	}

	inline void Key(UWorld* World, AActor* Person, const FVector& Eye, const FVector& Face)
	{
		if (World == nullptr || Person == nullptr) { return; }
		FRig& R = Rig();
		if (R.Person.Get() != Person) { Off(); }
		if (!R.Holder.IsValid())
		{
			FActorSpawnParameters P;
			P.ObjectFlags |= RF_Transient;
			AActor* H = World->SpawnActor<AActor>(AActor::StaticClass(), FTransform(Face), P);
			if (H == nullptr) { return; }
			USceneComponent* Root = NewObject<USceneComponent>(H, TEXT("TalkLightRoot"));
			H->SetRootComponent(Root);
			Root->RegisterComponent();

			USpotLightComponent* K = NewObject<USpotLightComponent>(H, TEXT("TalkKey"));
			K->SetMobility(EComponentMobility::Movable);
			K->SetupAttachment(Root);
			K->RegisterComponent();
			K->SetIntensityUnits(ELightUnits::Candelas);
			K->SetIntensity(KeyCandela());
			K->SetLightColor(FLinearColor(1.0f, 0.96f, 0.9f));
			K->SetAttenuationRadius(400.0f);
			K->SetInnerConeAngle(12.0f);
			K->SetOuterConeAngle(30.0f);
			K->SetSourceRadius(20.0f);     // soft: a wide source, not a point
			K->SetSoftSourceRadius(30.0f);
			K->SetCastShadows(false);
			K->SetIndirectLightingIntensity(0.0f);
			K->SetVolumetricScatteringIntensity(0.0f);
			K->SetLightingChannels(false, true, false);

			URectLightComponent* E = NewObject<URectLightComponent>(H, TEXT("TalkEyes"));
			E->SetMobility(EComponentMobility::Movable);
			E->SetupAttachment(Root);
			E->RegisterComponent();
			E->SetIntensityUnits(ELightUnits::Candelas);
			E->SetIntensity(EyeCandela());
			E->SetSourceWidth(24.0f);
			E->SetSourceHeight(12.0f);
			E->SetAttenuationRadius(400.0f);
			E->SetCastShadows(false);
			E->SetIndirectLightingIntensity(0.0f);
			E->SetVolumetricScatteringIntensity(0.0f);
			E->SetLightingChannels(false, true, false);
			E->DiffuseScale = 0.08f;       // in the eyes, hardly on the skin
			E->MarkRenderStateDirty();

			R.Holder = H;
			R.Key = K;
			R.Eyes = E;
			R.Person = Person;
			Channels(Person, true);
			UE_LOG(LogTemp, Display, TEXT("LedgerTalkLight: on %s, key %.1f cd, eyes %.1f cd"), *Person->GetClass()->GetName(), KeyCandela(), EyeCandela());
		}
		// Placed each call, so it follows the camera: the key 1.2 m from the
		// face, turned 40 degrees off the camera line toward the sun's side and
		// raised 25 degrees; the eye light just above the camera.
		const FVector ToCam = (Eye - Face).GetSafeNormal();
		const float Side = SunSide(World, Eye, Face);
		const FVector KeyDir = FRotator(25.0f, 40.0f * Side, 0.0f).RotateVector(FVector(ToCam.X, ToCam.Y, 0.0f).GetSafeNormal());
		const FVector KeyAt = Face + KeyDir * 120.0f;
		if (R.Key.IsValid()) { R.Key->SetWorldLocationAndRotation(KeyAt, (Face - KeyAt).Rotation()); }
		const FVector EyeAt = Eye + FVector(0.0f, 0.0f, 12.0f);
		if (R.Eyes.IsValid()) { R.Eyes->SetWorldLocationAndRotation(EyeAt, (Face - EyeAt).Rotation()); }
	}
}
