#include "StreetSounds.h"

#include "Components/AudioComponent.h"
#include "Components/SceneComponent.h"
#include "Sound/SoundAttenuation.h"
#include "Sound/SoundWave.h"

ALedgerStreetSounds::ALedgerStreetSounds()
{
	PrimaryActorTick.bCanEverTick = true;
	RootComponent = CreateDefaultSubobject<USceneComponent>(TEXT("Root"));
}

// THE ENGINE'S ATTENUATION, set on the component rather than an asset so the
// numbers live in the street's sound file: spatialised, full within the inner
// sphere, fading by the natural-sound curve over the falloff distance.
void ALedgerStreetSounds::Attenuate(UAudioComponent* C, float InnerCm, float FalloffCm)
{
	C->bOverrideAttenuation = true;
	FSoundAttenuationSettings& A = C->AttenuationOverrides;
	A.bAttenuate = true;
	A.bSpatialize = true;
	A.AttenuationShape = EAttenuationShape::Sphere;
	A.AttenuationShapeExtents = FVector(InnerCm, 0.0f, 0.0f);
	A.FalloffDistance = FalloffCm;
	A.DistanceAlgorithm = EAttenuationDistanceModel::NaturalSound;
}

bool ALedgerStreetSounds::AddAmbience(USoundWave* Wave, const FVector& At, float InnerCm, float FalloffCm, float Volume)
{
	if (Wave == nullptr) return false;
	UAudioComponent* C = NewObject<UAudioComponent>(this);
	if (C == nullptr) return false;
	C->bAutoActivate = false;
	C->SetupAttachment(RootComponent);
	C->RegisterComponent();
	C->SetWorldLocation(At);
	C->SetSound(Wave);
	C->SetVolumeMultiplier(Volume);
	Attenuate(C, InnerCm, FalloffCm);
	Beds.Add(C);
	++Ambiences;
	return true;
}

bool ALedgerStreetSounds::AddVoice(USceneComponent* Person, const TArray<USoundWave*>& Clips, float InnerCm,
                                   float FalloffCm, float MinS, float MaxS)
{
	if (Person == nullptr || Clips.Num() == 0 || Person->GetOwner() == nullptr) return false;
	// OWNED BY THE PERSON AND RIDING ON THEM, at head height, so the voice
	// comes from where they stand.
	UAudioComponent* C = NewObject<UAudioComponent>(Person->GetOwner());
	if (C == nullptr) return false;
	C->bAutoActivate = false;
	C->SetupAttachment(Person);
	C->RegisterComponent();
	C->SetRelativeLocation(FVector(0.0f, 0.0f, 160.0f));
	Attenuate(C, InnerCm, FalloffCm);
	VoiceComps.Add(C);
	ClipStart.Add(AllClips.Num());
	ClipCount.Add(Clips.Num());
	for (USoundWave* W : Clips) { AllClips.Add(W); }
	NextIndex.Add(0);
	NextAt.Add(0.0f);
	EveryMin.Add(MinS);
	EveryMax.Add(FMath::Max(MinS, MaxS));
	ClipsHeld += Clips.Num();
	++Voices;
	return true;
}

void ALedgerStreetSounds::StartPlaying()
{
	bPlaying = true;
	for (UAudioComponent* C : Beds) { if (C != nullptr) C->Play(); }
	// STAGGERED, so six people do not all speak in the first second.
	for (int32 I = 0; I < NextAt.Num(); ++I) { NextAt[I] = Clock + FMath::FRandRange(2.0f, EveryMax[I]); }
}

void ALedgerStreetSounds::Tick(float DeltaSeconds)
{
	Super::Tick(DeltaSeconds);
	if (!bPlaying) return;
	Clock += DeltaSeconds;
	for (int32 I = 0; I < VoiceComps.Num(); ++I)
	{
		UAudioComponent* C = VoiceComps[I];
		if (C == nullptr || Clock < NextAt[I] || C->IsPlaying() || ClipCount[I] <= 0) continue;
		USoundWave* W = AllClips[ClipStart[I] + (NextIndex[I] % ClipCount[I])];
		++NextIndex[I];
		NextAt[I] = Clock + FMath::FRandRange(EveryMin[I], EveryMax[I]);
		if (W == nullptr) continue;
		C->SetSound(W);
		C->Play();
	}
}
