// THE CLOTHING SESSION'S GARMENTS, WORN, 30 September. Each garment it hands
// over (NOW.md, Handovers) is listed in production/specs/garments.json and
// imported onto its wearer's body skeleton by tools/ue/import_garments.py at
// /Game/Ledger/MetaHumans/Garments/<Name>/SKM_<Name>. Here each is put on its
// wearer as a skeletal mesh following the body's pose (as the donkey jacket
// was, LedgerJacket.h), keeping the weights it came with; the parts of Epic's
// outfit it replaces are hidden ("hides": any part whose own name or mesh
// name holds one of those words); and "raise_mm" lifts the body so soles
// stand on the ground (MetaHumans stand barefoot on the floor since 5.6).
//
// Found where the game finds its other specs: -LedgerRepo, the checkout
// beside the project, or the game's own staged copy (Content/LedgerData).
#pragma once

#include "Components/SkeletalMeshComponent.h"
#include "Dom/JsonObject.h"
#include "Engine/SkeletalMesh.h"
#include "Materials/MaterialInstanceDynamic.h"
#include "GameFramework/Actor.h"
#include "Misc/CommandLine.h"
#include "Misc/FileHelper.h"
#include "Misc/Paths.h"
#include "Serialization/JsonReader.h"
#include "Serialization/JsonSerializer.h"

namespace LedgerGarments
{
	inline FString SpecFile()
	{
		TArray<FString> Cands;
		FString Repo;
		if (FParse::Value(FCommandLine::Get(), TEXT("LedgerRepo="), Repo) && !Repo.IsEmpty()) { Cands.Add(FPaths::Combine(Repo, TEXT("production/specs/garments.json"))); }
		Cands.Add(FPaths::Combine(FPaths::ProjectDir(), TEXT("../production/specs/garments.json")));
		Cands.Add(FPaths::Combine(FPaths::ProjectDir(), TEXT("../../../../production/specs/garments.json")));
		Cands.Add(FPaths::Combine(FPaths::ProjectContentDir(), TEXT("LedgerData/production/specs/garments.json")));
		for (FString C : Cands)
		{
			C = FPaths::ConvertRelativePathToFull(C);
			FPaths::CollapseRelativeDirectories(C);
			if (FPaths::FileExists(C)) { return C; }
		}
		return FString();
	}

	// Every part of a person, named, once: what Epic's outfit calls its pieces
	// is what "hides" has to match.
	inline void LogParts(AActor* A, const TCHAR* Who)
	{
		TArray<USkeletalMeshComponent*> Parts;
		A->GetComponents(Parts);
		FString Seen;
		for (USkeletalMeshComponent* C : Parts)
		{
			if (C == nullptr) { continue; }
			const USkeletalMesh* M = C->GetSkeletalMeshAsset();
			Seen += FString::Printf(TEXT(" %s=%s"), *C->GetName(), M != nullptr ? *M->GetName() : TEXT("none"));
		}
		UE_LOG(LogTemp, Display, TEXT("LedgerGarments: %s's parts:%s"), Who, *Seen);
	}

	inline int32 Wear(AActor* A, const TCHAR* Who)
	{
		if (A == nullptr) { return 0; }
		LogParts(A, Who);
		const FString Path = SpecFile();
		FString Text;
		if (Path.IsEmpty() || !FFileHelper::LoadFileToString(Text, *Path))
		{
			UE_LOG(LogTemp, Display, TEXT("LedgerGarments: no garments list found"));
			return 0;
		}
		TSharedPtr<FJsonObject> Root;
		if (!FJsonSerializer::Deserialize(TJsonReaderFactory<>::Create(Text), Root) || !Root.IsValid()) { return 0; }
		USkeletalMeshComponent* Body = nullptr;
		TArray<USkeletalMeshComponent*> Parts;
		A->GetComponents(Parts);
		for (USkeletalMeshComponent* C : Parts) { if (C != nullptr && C->GetName() == TEXT("Body")) { Body = C; break; } }
		if (Body == nullptr) { return 0; }
		int32 Worn = 0;
		float RaiseCm = 0.0f;
		for (const TSharedPtr<FJsonValue>& V : Root->GetArrayField(TEXT("garments")))
		{
			const TSharedPtr<FJsonObject> G = V->AsObject();
			if (!G.IsValid() || G->GetStringField(TEXT("who")) != Who) { continue; }
			const FString Name = G->GetStringField(TEXT("name"));
			// HELD: handed over but not to be worn yet (its reason in the list).
			if (G->HasField(TEXT("hold"))) { UE_LOG(LogTemp, Display, TEXT("LedgerGarments: %s's %s held back: %s"), Who, *Name, *G->GetStringField(TEXT("hold")).Left(80)); continue; }
			const FString Asset = FString::Printf(TEXT("/Game/Ledger/MetaHumans/Garments/%s/SKM_%s.SKM_%s"), *Name, *Name, *Name);
			USkeletalMesh* Mesh = LoadObject<USkeletalMesh>(nullptr, *Asset);
			if (Mesh == nullptr)
			{
				UE_LOG(LogTemp, Display, TEXT("LedgerGarments: %s's %s NOT worn (not in this copy of the game)"), Who, *Name);
				continue;
			}
			USkeletalMeshComponent* Piece = NewObject<USkeletalMeshComponent>(A, *(FString(TEXT("LedgerGarment_")) + Name));
			Piece->SetSkeletalMeshAsset(Mesh);
			Piece->SetupAttachment(Body);
			Piece->SetCollisionEnabled(ECollisionEnabled::NoCollision);
			Piece->RegisterComponent();
			Piece->SetLeaderPoseComponent(Body);
			++Worn;
			// SPECTACLE LENSES SEE-THROUGH (their README: one thin light brown
			// tint, darker in the top third, so her eyes show through): the
			// street's own glass material, tinted, on any "Lens" slot; the FBX
			// brought them in opaque.
			const TArray<FName> Slots = Piece->GetMaterialSlotNames();
			for (int32 I = 0; I < Slots.Num(); ++I)
			{
				const FString S = Slots[I].ToString().ToLower();
				if (!S.Contains(TEXT("lens"))) { continue; }
				UMaterialInterface* Glass = LoadObject<UMaterialInterface>(nullptr, TEXT("/Game/Ledger/M_LedgerGlass.M_LedgerGlass"));
				if (Glass == nullptr) { UE_LOG(LogTemp, Display, TEXT("LedgerGarments: no glass material in this copy; %s left as made"), *Slots[I].ToString()); continue; }
				UMaterialInstanceDynamic* Tint = UMaterialInstanceDynamic::Create(Glass, Piece);
				const bool bTop = S.Contains(TEXT("top"));
				Tint->SetVectorParameterValue(TEXT("GlassTint"), bTop ? FLinearColor(0.22f, 0.14f, 0.08f) : FLinearColor(0.42f, 0.31f, 0.2f));
				Tint->SetScalarParameterValue(TEXT("GlassOpacity"), bTop ? 0.35f : 0.15f);
				Tint->SetScalarParameterValue(TEXT("GlassRoughness"), 0.04f);
				Piece->SetMaterial(Piece->GetMaterialIndex(Slots[I]), Tint);
				UE_LOG(LogTemp, Display, TEXT("LedgerGarments: %s's %s slot %s (index %d) glazed"), Who, *Name, *Slots[I].ToString(), Piece->GetMaterialIndex(Slots[I]));
			}
			const TArray<TSharedPtr<FJsonValue>>* Hides = nullptr;
			FString Hidden;
			if (G->TryGetArrayField(TEXT("hides"), Hides))
			{
				// "shoes": the outfit part whose top is within 25 cm of the soles.
				// Epic's outfit pieces are named only Outfits, _2 and _3, so the
				// boots Ron already wore were found by where they sit.
				// Measured on each part's own mesh, feet at zero: a part following
				// the body's pose shares the body's bounds in the world.
				auto MeshTop = [](const USkeletalMeshComponent* C) {
					const USkeletalMesh* M = C->GetSkeletalMeshAsset();
					return M != nullptr ? (float)(M->GetBounds().Origin.Z + M->GetBounds().BoxExtent.Z) : 1000.0f; };
				for (USkeletalMeshComponent* C : Parts)
				{
					if (C != nullptr) { UE_LOG(LogTemp, Display, TEXT("LedgerGarments: %s's %s reaches %.0f cm"), Who, *C->GetName(), MeshTop(C)); }
				}
				for (USkeletalMeshComponent* C : Parts)
				{
					if (C == nullptr || C == Body || C->GetName() == TEXT("Face")) { continue; }
					const FString Named = (C->GetName() + TEXT(" ") + (C->GetSkeletalMeshAsset() != nullptr ? C->GetSkeletalMeshAsset()->GetName() : FString())).ToLower();
					const float Top = MeshTop(C);
					for (const TSharedPtr<FJsonValue>& H : *Hides)
					{
						const FString Word = H->AsString().ToLower();
						if ((Word == TEXT("shoes") && Top < 25.0f) || (Word != TEXT("shoes") && Named.Contains(Word)))
						{
							C->SetVisibility(false, true);
							Hidden += TEXT(" ") + C->GetName();
							break;
						}
					}
				}
			}
			double Raise = 0.0;
			if (G->TryGetNumberField(TEXT("raise_mm"), Raise)) { RaiseCm = FMath::Max(RaiseCm, (float)Raise / 10.0f); }
			UE_LOG(LogTemp, Display, TEXT("LedgerGarments: %s wears %s%s%s"), Who, *Name,
				Hidden.IsEmpty() ? TEXT("") : TEXT(", hiding"), *Hidden);
		}
		if (RaiseCm > 0.0f)
		{
			Body->SetRelativeLocation(Body->GetRelativeLocation() + FVector(0.0, 0.0, RaiseCm));
			UE_LOG(LogTemp, Display, TEXT("LedgerGarments: %s raised %.1f cm for the soles"), Who, RaiseCm);
		}
		return Worn;
	}
}
