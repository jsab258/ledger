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

#include "ChaosClothAsset/ClothAssetBase.h"
#include "ChaosClothAsset/ClothComponent.h"
#include "Components/SkeletalMeshComponent.h"
#include "Components/StaticMeshComponent.h"
#include "Engine/StaticMesh.h"
#include "Engine/SkeletalMesh.h"
#include "Materials/MaterialInterface.h"
#include "Misc/Paths.h"
#include "PhysicsEngine/PhysicsAsset.h"
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

	// THE SIMULATED JACKET, 28 September (Jafar's list, item 5): a Chaos cloth
	// asset (tools/ue/make_cloth_jacket.py, from Epic's static-mesh cloth
	// template: the jacket hung on Ron's own body in Blender, its skin weights
	// copied from that body) on a cloth component that follows the body's pose
	// and collides with the body's physics asset, so its loose parts swing.
	inline bool WearCloth(AActor* A, const FString& Path)
	{
		if (A == nullptr || Path.IsEmpty()) { return false; }
		UChaosClothAssetBase* Asset = LoadObject<UChaosClothAssetBase>(nullptr, *Path);
		USkeletalMeshComponent* Body = nullptr;
		TArray<USkeletalMeshComponent*> Parts;
		A->GetComponents(Parts);
		for (USkeletalMeshComponent* C : Parts) { if (C != nullptr && C->GetName() == TEXT("Body")) { Body = C; break; } }
		if (Asset == nullptr || Body == nullptr)
		{
			UE_LOG(LogTemp, Display, TEXT("LedgerJacket: cloth NOT worn (asset %s, body %s)"),
				Asset != nullptr ? TEXT("found") : TEXT("MISSING"), Body != nullptr ? TEXT("found") : TEXT("MISSING"));
			return false;
		}
		UChaosClothComponent* J = NewObject<UChaosClothComponent>(A, TEXT("LedgerClothJacket"));
		J->SetupAttachment(Body);
		J->RegisterComponent();
		J->SetAsset(Asset);
		J->SetLeaderPoseComponent(Body);
		// ITS COLOURS, set on the component: a cloth asset regenerated from the
		// template renders in the engine's grey debug cloth, whatever the meshes
		// carried (28 September). The instances sit beside the asset
		// (MI_DonkeyJacket_Wool, _Yoke, _Button; tools/ue/make_cloth_jacket.py),
		// matched to the slots by name, wool where no name matches.
		const FString Folder = FPaths::GetPath(Path.Left(Path.Find(TEXT("."))));
		auto Mat = [&Folder](const TCHAR* Key) { const FString N = FString(TEXT("MI_DonkeyJacket_")) + Key; return LoadObject<UMaterialInterface>(nullptr, *(Folder / N + TEXT(".") + N)); };
		UMaterialInterface* Wool = Mat(TEXT("Wool"));
		UMaterialInterface* Yoke = Mat(TEXT("Yoke"));
		UMaterialInterface* Button = Mat(TEXT("Button"));
		const TArray<FName> Slots = J->GetMaterialSlotNames();
		FString Seen;
		for (int32 I = 0; I < FMath::Max(Slots.Num(), J->GetNumMaterials()); ++I)
		{
			const FString S = Slots.IsValidIndex(I) ? Slots[I].ToString().ToLower() : FString();
			UMaterialInterface* M = S.Contains(TEXT("yoke")) ? Yoke : S.Contains(TEXT("button")) ? Button : Wool;
			if (M != nullptr) { J->SetMaterial(I, M); }
			Seen += FString::Printf(TEXT("%s%d:%s"), Seen.IsEmpty() ? TEXT("") : TEXT(", "), I, S.IsEmpty() ? TEXT("(unnamed)") : *S);
		}
		UE_LOG(LogTemp, Display, TEXT("LedgerJacket: cloth slots %s; wool %s"), *Seen, Wool != nullptr ? TEXT("found") : TEXT("MISSING"));
		UPhysicsAsset* Phys = Body->GetPhysicsAsset();
		if (Phys != nullptr) { J->AddCollisionSource(Body, Phys); }
		UE_LOG(LogTemp, Display, TEXT("LedgerJacket: cloth %s worn, colliding with %s"), *Path, Phys != nullptr ? *Phys->GetName() : TEXT("nothing (no physics asset)"));
		// THE COLLAR, fixed to the upper back, 29 September: stiff melton
		// barely moves, and as a second simulated layer 12 mm over the yoke the
		// collar's points and the yoke's were drawn to the wrong layer (a torn
		// collar and a blotchy yoke). SM_<name>_Collar beside the asset is made
		// in the body's rest pose, so it goes on spine_05 at the inverse of that
		// bone's rest-pose place in the body.
		const FString Name = FPaths::GetCleanFilename(Folder);
		const FString CollarName = FString(TEXT("SM_")) + Name + TEXT("_Collar");
		UStaticMesh* CollarMesh = LoadObject<UStaticMesh>(nullptr, *(Folder / CollarName + TEXT(".") + CollarName));
		const FName Bone(TEXT("spine_05"));
		USkeletalMesh* BodyMesh = Body->GetSkeletalMeshAsset();
		const int32 BoneIndex = BodyMesh != nullptr ? BodyMesh->GetRefSkeleton().FindBoneIndex(Bone) : INDEX_NONE;
		if (CollarMesh != nullptr && BoneIndex != INDEX_NONE)
		{
			const FReferenceSkeleton& Ref = BodyMesh->GetRefSkeleton();
			FTransform RefInBody = FTransform::Identity;
			for (int32 I = BoneIndex; I != INDEX_NONE; I = Ref.GetParentIndex(I)) { RefInBody = RefInBody * Ref.GetRefBonePose()[I]; }
			UStaticMeshComponent* Collar = NewObject<UStaticMeshComponent>(A, TEXT("LedgerJacketCollar"));
			Collar->SetStaticMesh(CollarMesh);
			Collar->SetupAttachment(Body, Bone);
			Collar->SetRelativeTransform(RefInBody.Inverse());
			Collar->SetCollisionEnabled(ECollisionEnabled::NoCollision);
			for (int32 I = 0; I < Collar->GetNumMaterials(); ++I) { if (Wool != nullptr) { Collar->SetMaterial(I, Wool); } }
			Collar->RegisterComponent();
		}
		UE_LOG(LogTemp, Display, TEXT("LedgerJacket: collar %s"), CollarMesh == nullptr ? TEXT("none beside the asset") : BoneIndex == INDEX_NONE ? TEXT("NOT fixed (no spine_05)") : TEXT("fixed to spine_05"));
		return true;
	}
}
