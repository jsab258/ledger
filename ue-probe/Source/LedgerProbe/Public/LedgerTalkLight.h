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
		double OnAt = 0.0;       // when it was put on this person: it fades in from there
		int32 SunState = -1;     // last logged: 0 in shade, 1 in sun
	};
	inline FRig& Rig() { static FRig R; return R; }
	// FADED IN over this many seconds (the reviewer who passed it: "if it
	// switches on instantly, he will visibly pop out of the street").
	constexpr double FadeInSeconds = 0.8;

	// -TalkKeyCd= and -TalkEyeCd= tune the two lights without a rebuild.
	// FROM MEASUREMENT, 28 September, after two tries failed the blind
	// reviewer (6 cd, then 3 cd): measured in linear light, not screen
	// values, Ron's face was 0.7 times the brick behind him unlit and 3.9
	// times at 3 cd, where skin against brick in the same daylight is about
	// 1.5 to 2. A sweep from 45 degrees up (1.0, 1.4, 1.8 cd) gave 1.35,
	// 1.61 and 1.85 on my patches of face and wall, which read about 1.3
	// times lower than the reviewer's; 1.2 cd sits in the band on both
	// (production/art/lighting/talk-light-2026-09-28/README.md).
	// Cut a fifth after the third review (1.2 cd measured 2.0 to 2.6 on the
	// reviewer's patches), and to 0.6 cd after the fourth (1 cd: 2.17 on its
	// patches, the added light 1.4 times the daylight on the face).
	inline float KeyCandela() { float V = 0.6f; FParse::Value(FCommandLine::Get(), TEXT("TalkKeyCd="), V); return V; }
	// A FACE THE SUN ALREADY REACHES is past 2 on its own (Sheila, sunlit:
	// about 2.3 in linear light unlit): there it gets no key, only the eye light.
	inline float SunShare() { float V = 0.0f; FParse::Value(FCommandLine::Get(), TEXT("TalkSunShare="), V); return V; }
	// The eye light's shine on the skin still lifted a sunlit face by a third
	// at 2 cd (Sheila: 2.17 to 2.92 times the wall with no key): halved.
	inline float EyeCandela() { float V = 1.0f; FParse::Value(FCommandLine::Get(), TEXT("TalkEyeCd="), V); return V; }

	inline void Channels(AActor* A, bool bLit)
	{
		if (A == nullptr) { return; }
		TArray<UPrimitiveComponent*> Parts;
		A->GetComponents(Parts);
		for (UPrimitiveComponent* C : Parts)
		{
			// NOT THE HAIR (the fourth review, 28 September): shadowed or not,
			// hair under the key went pale (Ron's moustache 8.5 times brighter
			// against 2.4 for the skin), so the hair, brows, moustache and
			// lashes stay in the street's own light only.
			const bool bHair = C != nullptr && C->GetClass()->GetName() == TEXT("GroomComponent");
			if (C != nullptr) { C->SetLightingChannels(true, bLit && !bHair, false); }
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

	// Whether the sun reaches the face: nothing between it and the sun but the
	// person themself (anything within 40 cm of the face is taken as them).
	inline bool Sunlit(UWorld* World, AActor* Person, const FVector& Face)
	{
		ADirectionalLight* Sun = nullptr;
		for (TActorIterator<ADirectionalLight> It(World); It; ++It)
		{
			if (Sun == nullptr || It->GetLightComponent()->Intensity > Sun->GetLightComponent()->Intensity) { Sun = *It; }
		}
		if (Sun == nullptr) { return false; }
		FCollisionQueryParams Q(TEXT("LedgerTalkSun"), false, Person);
		const FVector Far = Face - Sun->GetActorForwardVector() * 5000.0f;
		FHitResult Hit;
		return !(World->LineTraceSingleByChannel(Hit, Face, Far, ECC_Visibility, Q) && FVector::Dist(Hit.ImpactPoint, Face) > 40.0f);
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
			K->SetIntensity(0.0f);           // faded in by the update below
			K->SetLightColor(FLinearColor(1.0f, 0.96f, 0.9f));
			K->SetAttenuationRadius(400.0f);
			K->SetInnerConeAngle(12.0f);
			K->SetOuterConeAngle(30.0f);
			K->SetSourceRadius(20.0f);     // soft: a wide source, not a point
			K->SetSoftSourceRadius(30.0f);
			// UNSHADOWED: shadows (deep ones for hair) cost 1.99 ms a frame on
			// this card (budget 0.5; 0.21 without), and the hair they were for
			// is now off this light's channel (Channels). -TalkShadow turns
			// them on, to measure.
			K->SetCastShadows(FParse::Param(FCommandLine::Get(), TEXT("TalkShadow")));
			K->bCastDeepShadow = K->CastShadows;
			K->SetIndirectLightingIntensity(0.0f);
			K->SetVolumetricScatteringIntensity(0.0f);
			K->SetLightingChannels(false, true, false);
			K->MarkRenderStateDirty();

			URectLightComponent* E = NewObject<URectLightComponent>(H, TEXT("TalkEyes"));
			E->SetMobility(EComponentMobility::Movable);
			E->SetupAttachment(Root);
			E->RegisterComponent();
			E->SetIntensityUnits(ELightUnits::Candelas);
			E->SetIntensity(0.0f);
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
			R.OnAt = FPlatformTime::Seconds();
			Channels(Person, true);
			UE_LOG(LogTemp, Display, TEXT("LedgerTalkLight: on %s, key %.1f cd, eyes %.1f cd"), *Person->GetClass()->GetName(), KeyCandela(), EyeCandela());
		}
		// Placed each call, so it follows the camera: the key 1.2 m from the
		// face, turned 40 degrees off the camera line toward the sun's side and
		// raised 45 degrees (25 flattened the face: the reviewer measured
		// forehead against chin going from 4.5 to 1 down to 1.2 to 1, where
		// the street's light from above keeps the chin and neck darker); the
		// eye light just above the camera.
		const FVector ToCam = (Eye - Face).GetSafeNormal();
		const float Side = SunSide(World, Eye, Face);
		const FVector KeyDir = FRotator(45.0f, 40.0f * Side, 0.0f).RotateVector(FVector(ToCam.X, ToCam.Y, 0.0f).GetSafeNormal());
		const FVector KeyAt = Face + KeyDir * 120.0f;
		if (R.Key.IsValid()) { R.Key->SetWorldLocationAndRotation(KeyAt, (Face - KeyAt).Rotation()); }
		const FVector EyeAt = Eye + FVector(0.0f, 0.0f, 12.0f);
		if (R.Eyes.IsValid()) { R.Eyes->SetWorldLocationAndRotation(EyeAt, (Face - EyeAt).Rotation()); }
		const bool bSun = Sunlit(World, Person, Face);
		const float Fade = (float)FMath::Clamp((FPlatformTime::Seconds() - R.OnAt) / FadeInSeconds, 0.0, 1.0);
		const float Want = (bSun ? KeyCandela() * SunShare() : KeyCandela()) * Fade;
		if (R.Key.IsValid() && !FMath::IsNearlyEqual(R.Key->Intensity, Want, 0.001f)) { R.Key->SetIntensity(Want); }
		if (R.Eyes.IsValid() && !FMath::IsNearlyEqual(R.Eyes->Intensity, EyeCandela() * Fade, 0.001f)) { R.Eyes->SetIntensity(EyeCandela() * Fade); }
		if (R.SunState != (bSun ? 1 : 0))
		{
			R.SunState = bSun ? 1 : 0;
			UE_LOG(LogTemp, Display, TEXT("LedgerTalkLight: %s, key %.2f cd"), bSun ? TEXT("in sun") : TEXT("in shade"), bSun ? KeyCandela() * SunShare() : KeyCandela());
		}
	}
}
