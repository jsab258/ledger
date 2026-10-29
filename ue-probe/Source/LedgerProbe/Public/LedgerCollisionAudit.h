// WHAT A "NO COLLISION" REALLY BLOCKS, COUNTED IN PLAY (-CollisionAudit; FINDINGS.md, 28 October: a spawned mesh
// actor's "block all" profile is applied when its physics state is made, after a plain
// SetCollisionEnabled(NoCollision) was read as already done, so Mickey's fittings blocked Tom as one solid shell).
// Ten other places use the same plain call (people, the street's meshes, the sky, figures, control quads). Before any
// of them is changed, each is counted for what it really blocks once the street is built, since the street or the
// camera may lean on the accidental collision. Each place notes its component here; the report runs once, 20 s in.
// Read only: nothing here changes any collision.
#pragma once

#include "CoreMinimal.h"
#include "Components/PrimitiveComponent.h"
#include "Misc/CommandLine.h"
#include "Misc/Parse.h"

namespace LedgerCollisionAudit
{
	struct FEntry { TWeakObjectPtr<UPrimitiveComponent> C; FString Site; };

	inline TArray<FEntry>& Entries() { static TArray<FEntry> E; return E; }

	inline bool On() { static const bool b = FParse::Param(FCommandLine::Get(), TEXT("CollisionAudit")); return b; }

	inline void Note(UPrimitiveComponent* C, const TCHAR* Site)
	{
		if (C != nullptr && On()) { Entries().Add({ C, Site }); }
	}

	// One line a site: how many it switched off, how many still collide, block a walking body (the pawn channel) or
	// the camera's arm (the camera channel), and the profiles they carry now.
	inline void Report()
	{
		TMap<FString, TArray<const UPrimitiveComponent*>> BySite;
		for (const FEntry& E : Entries()) { if (E.C.IsValid()) { BySite.FindOrAdd(E.Site).Add(E.C.Get()); } }
		for (const TPair<FString, TArray<const UPrimitiveComponent*>>& S : BySite)
		{
			int32 Colliding = 0, Pawn = 0, Cam = 0;
			TSet<FName> Profiles;
			for (const UPrimitiveComponent* C : S.Value)
			{
				const bool bOn = C->GetCollisionEnabled() != ECollisionEnabled::NoCollision;
				Colliding += bOn ? 1 : 0;
				Pawn += bOn && C->GetCollisionResponseToChannel(ECC_Pawn) == ECR_Block ? 1 : 0;
				Cam += bOn && C->GetCollisionResponseToChannel(ECC_Camera) == ECR_Block ? 1 : 0;
				Profiles.Add(C->GetCollisionProfileName());
			}
			FString P;
			for (const FName& N : Profiles) { P += (P.IsEmpty() ? TEXT("") : TEXT("/")) + N.ToString(); }
			UE_LOG(LogTemp, Display, TEXT("LedgerCollisionAudit: site=%s switchedOff=%d stillColliding=%d blocksPawn=%d blocksCamera=%d profiles=%s"),
				*S.Key, S.Value.Num(), Colliding, Pawn, Cam, *P);
		}
		UE_LOG(LogTemp, Display, TEXT("LedgerCollisionAudit: done, %d components at %d sites"), Entries().Num(), BySite.Num());
	}
}
