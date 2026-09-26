// THE HAIR'S OWN COLOUR ON A CAST MEMBER, 26 September. Every cast member's
// hair rendered near black whatever colour the brief gave it: Ron's "short
// grey fringe" and "grey-brown moustache" came out black, Darren's light brown
// dark brown. The colour is right in the built hair materials (Ron's hold
// hairMelanin 0.4, WhiteAmount 0.55: tools/ue/mh_api_probe.py), and the
// blueprint gives those materials to its hair, so something between the
// blueprint and the screen puts other values on the hair. Keep() puts the
// built materials' own colour back on every hair and facial-hair part once
// the person is in the world, and logs what it found there, so the cause can
// be named.
#pragma once

#include "Components/MeshComponent.h"
#include "GameFramework/Actor.h"
#include "Materials/MaterialInstanceConstant.h"
#include "Materials/MaterialInstanceDynamic.h"

namespace LedgerHair
{
	inline const TCHAR* const Params[] = { TEXT("hairMelanin"), TEXT("hairRedness"), TEXT("WhiteAmount") };

	// The built material this part was given: the blueprint's own choice for
	// the slot, or the first built material up the chain from what it shows.
	inline UMaterialInstanceConstant* Built(UMeshComponent* C, int32 Slot)
	{
		auto IsBuilt = [](UMaterialInterface* M)
		{
			return M != nullptr && M->IsA<UMaterialInstanceConstant>() && M->GetPathName().StartsWith(TEXT("/Game/Ledger/MetaHumans/"));
		};
		if (C->OverrideMaterials.IsValidIndex(Slot) && IsBuilt(C->OverrideMaterials[Slot])) { return Cast<UMaterialInstanceConstant>(C->OverrideMaterials[Slot]); }
		for (UMaterialInterface* M = C->GetMaterial(Slot); M != nullptr; )
		{
			if (IsBuilt(M)) { return Cast<UMaterialInstanceConstant>(M); }
			UMaterialInstance* I = Cast<UMaterialInstance>(M);
			M = I != nullptr ? I->Parent.Get() : nullptr;
		}
		return nullptr;
	}

	// Returns how many parts were changed.
	inline int32 Keep(AActor* A, const TCHAR* Label)
	{
		if (A == nullptr) { return 0; }
		int32 Changed = 0;
		TArray<UMeshComponent*> Parts;
		A->GetComponents(Parts);
		for (UMeshComponent* C : Parts)
		{
			if (C == nullptr || C->GetClass()->GetName() != TEXT("GroomComponent")) { continue; }
			for (int32 Slot = 0; Slot < C->GetNumMaterials(); ++Slot)
			{
				UMaterialInstanceConstant* Mine = Built(C, Slot);
				UMaterialInterface* Shown = C->GetMaterial(Slot);
				if (Mine == nullptr || Shown == nullptr) { continue; }
				FString Found;
				bool bDiffers = Shown != Mine;
				for (const TCHAR* P : Params)
				{
					float Want = 0.0f, Has = 0.0f;
					if (!Mine->GetScalarParameterValue(FHashedMaterialParameterInfo(P), Want)) { continue; }
					Shown->GetScalarParameterValue(FHashedMaterialParameterInfo(P), Has);
					Found += FString::Printf(TEXT(" %s %.2f->%.2f"), P, Has, Want);
					bDiffers |= !FMath::IsNearlyEqual(Has, Want, 0.005f);
				}
				UE_LOG(LogTemp, Display, TEXT("LedgerHair: %s %s slot %d shows %s (built %s)%s"), Label, *C->GetName(), Slot,
					*Shown->GetPathName(), *Mine->GetName(), *Found);
				if (!bDiffers) { continue; }
				UMaterialInstanceDynamic* D = UMaterialInstanceDynamic::Create(Mine, C);
				for (const TCHAR* P : Params)
				{
					float Want = 0.0f;
					if (Mine->GetScalarParameterValue(FHashedMaterialParameterInfo(P), Want)) { D->SetScalarParameterValue(P, Want); }
				}
				C->SetMaterial(Slot, D);
				++Changed;
			}
		}
		UE_LOG(LogTemp, Display, TEXT("LedgerHair: %s: %d hair parts given their built colour"), Label, Changed);
		return Changed;
	}
}
