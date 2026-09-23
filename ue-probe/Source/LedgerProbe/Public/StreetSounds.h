// THE STREET'S SOUND, 23 September, for Jafar's presentable checklist: "sound
// is positional: a voice or a noise comes from where its source is and changes
// as you move" - and the street made no sound at all.
//
// UNREAL'S OWN AUDIO, NOT OURS: each source is a UAudioComponent at its place
// (a bed) or riding on a person (a voice), with the engine's attenuation -
// spatialised, falling off by the natural-sound curve over a stated distance -
// so direction and loudness follow the listener as the player moves. This
// actor only owns the components and says each person's next line when it is
// due; the engine does the hearing. Placed from production/specs/
// street-sounds.json by VignetteShot.cpp (SpawnSounds); plays only in the
// playable street, never in the automation's shots.
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "StreetSounds.generated.h"

class UAudioComponent;
class USceneComponent;
class USoundWave;

UCLASS()
class ALedgerStreetSounds : public AActor
{
	GENERATED_BODY()

public:
	ALedgerStreetSounds();

	virtual void Tick(float DeltaSeconds) override;

	// A looping bed at a place, heard fully within InnerCm and fading out over
	// FalloffCm beyond it.
	bool AddAmbience(USoundWave* Wave, const FVector& At, float InnerCm, float FalloffCm, float Volume);

	// A voice riding on a person's root, at head height: one of Clips, in turn,
	// every MinS to MaxS seconds.
	bool AddVoice(USceneComponent* Person, const TArray<USoundWave*>& Clips, float InnerCm,
	              float FalloffCm, float MinS, float MaxS);

	// Starts the beds and the voices' clocks. Called only in the playable street.
	void StartPlaying();

	int32 Ambiences = 0;
	int32 Voices = 0;
	int32 ClipsHeld = 0;
	bool bPlaying = false;

private:
	static void Attenuate(UAudioComponent* C, float InnerCm, float FalloffCm);

	UPROPERTY()
	TArray<TObjectPtr<UAudioComponent>> Beds;

	UPROPERTY()
	TArray<TObjectPtr<UAudioComponent>> VoiceComps;

	UPROPERTY()
	TArray<TObjectPtr<USoundWave>> AllClips;

	TArray<int32> ClipStart;
	TArray<int32> ClipCount;
	TArray<int32> NextIndex;
	TArray<float> NextAt;
	TArray<float> EveryMin;
	TArray<float> EveryMax;
	float Clock = 0.0f;
};
