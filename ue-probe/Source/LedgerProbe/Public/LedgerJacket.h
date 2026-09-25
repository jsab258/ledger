// THE DONKEY JACKET ON A CAST MEMBER, 25 September. Jafar's clothing item:
// one 1990 donkey jacket fitted on two bodies, moving, imported and packaged.
// The jacket (tools/meshgen/blender/donkey_jacket.py, imported by
// tools/ue/import_jacket.py) is cut from MetaHuman's template body and keeps
// its skin weights, so it follows any cast member's body by leader pose: it
// takes their bones' positions, which carry their height and build.
//
// -Jacket=rocco,sam chooses who wears it (the cast's internal ids). -Jacket=
// with nothing after it takes it off everyone.
//
// OFF BY DEFAULT, 25 September (evening): Jafar judged it nothing like a
// donkey jacket, and approved Ron's face in the plain clothes the candidates
// wore, so the game shows him as approved. -Jacket=rocco puts it back on.
#pragma once

#include "Components/SkeletalMeshComponent.h"
#include "Engine/SkeletalMesh.h"
#include "GameFramework/Actor.h"
#include "Misc/CommandLine.h"

namespace LedgerJacket
{
	// SIZES, as a tailor has them: leader pose carries a wearer's bones, not
	// his girth, so the regular cut had Ron's belly through its front. Ron
	// takes the large (made with --girth 0.13); everyone else the regular (--girth 0.05).
	inline FString PathFor(const TCHAR* Who)
	{
		const bool bLarge = FString(Who).ToLower() == TEXT("rocco");
		const TCHAR* Name = bLarge ? TEXT("SKM_DonkeyJacket_L") : TEXT("SKM_DonkeyJacket");
		return FString::Printf(TEXT("/Game/Ledger/MetaHumans/Clothing/DonkeyJacket/%s.%s"), Name, Name);
	}

	inline bool Wears(const TCHAR* Who)
	{
		FString Wearers;
		// false: read past the comma ("rocco,sam"), which the engine's reader
		// otherwise stops at (the first run dressed Ron alone).
		FParse::Value(FCommandLine::Get(), TEXT("Jacket="), Wearers, false);
		TArray<FString> Ids;
		Wearers.ToLower().ParseIntoArray(Ids, TEXT(","), true);
		return Ids.Contains(FString(Who).ToLower());
	}

	// Returns true when the jacket went on. Logs "LedgerJacket:" either way,
	// so a run's log says who wore it and why not.
	inline bool Wear(AActor* A, const TCHAR* Who)
	{
		if (A == nullptr || !Wears(Who)) { return false; }
		USkeletalMesh* Jacket = LoadObject<USkeletalMesh>(nullptr, *PathFor(Who));
		USkeletalMeshComponent* Body = nullptr;
		TArray<USkeletalMeshComponent*> Parts;
		A->GetComponents(Parts);
		for (USkeletalMeshComponent* C : Parts) { if (C != nullptr && C->GetName() == TEXT("Body")) { Body = C; break; } }
		if (Jacket == nullptr || Body == nullptr)
		{
			UE_LOG(LogTemp, Display, TEXT("LedgerJacket: %s NOT dressed (jacket %s, body %s)"), Who,
				Jacket != nullptr ? TEXT("found") : TEXT("MISSING"), Body != nullptr ? TEXT("found") : TEXT("MISSING"));
			return false;
		}
		USkeletalMeshComponent* J = NewObject<USkeletalMeshComponent>(A, TEXT("LedgerDonkeyJacket"));
		J->SetSkeletalMeshAsset(Jacket);
		J->SetupAttachment(Body);
		J->SetCollisionEnabled(ECollisionEnabled::NoCollision);
		J->RegisterComponent();
		J->SetLeaderPoseComponent(Body);
		UE_LOG(LogTemp, Display, TEXT("LedgerJacket: %s wears the donkey jacket"), Who);
		return true;
	}
}
