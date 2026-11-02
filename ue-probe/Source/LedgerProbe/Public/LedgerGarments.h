// THE CLOTHING SESSION'S GARMENTS, WORN, 30 September. Each garment it hands
// over (NOW.md, Handovers) is listed in production/specs/garments.json and
// imported onto its wearer's body skeleton by tools/ue/import_garments.py at
// /Game/Ledger/MetaHumans/Garments/<Name>/SKM_<Name>. Here each is put on its
// wearer as a skeletal mesh following the body's pose (as the donkey jacket
// was, LedgerJacket.h), keeping the weights it came with; the parts of Epic's
// outfit it replaces are hidden ("hides": any part whose own name or mesh
// name holds one of those words); and "raise_mm" lifts the body so soles
// stand on the ground (MetaHumans stand barefoot on the floor since 5.6);
// "soles" lays a decal (LayContact, held) or a stand-in for the light (LayStandIns) under each half sole.
//
// Found where the game finds its other specs: -LedgerRepo, the checkout
// beside the project, or the game's own staged copy (Content/LedgerData).
#pragma once

#include "AnimationRuntime.h"
#include "Components/DecalComponent.h"
#include "Components/StaticMeshComponent.h"
#include "Engine/StaticMesh.h"
#include "Components/SkeletalMeshComponent.h"
#include "Dom/JsonObject.h"
#include "Engine/SkeletalMesh.h"
#include "Materials/MaterialInstanceDynamic.h"
#include "Rendering/SkeletalMeshRenderData.h"
#include "Rendering/SkeletalMeshLODRenderData.h"
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

	// EACH HALF SOLE'S PLACE, 30 October 2026 (his order C9): each half's footprint is given along the foot and across
	// it, outward, from the ball joint's head, in the body's reference pose (tools/meshgen/blender/sole_footprints.py),
	// so no axis convention is needed: the same two joints give the same frame here. Centre on the sole's floor.
	struct FSolePart { FString Bone; FTransform At; FVector Centre, Fw, Ac; double Len = 0.0, Wid = 0.0; };
	inline TArray<FSolePart> SoleParts(USkeletalMeshComponent* Body, const TSharedPtr<FJsonObject>& Soles)
	{
		TArray<FSolePart> Out;
		const USkeletalMesh* BM = Body != nullptr ? Body->GetSkeletalMeshAsset() : nullptr;
		if (BM == nullptr) { return Out; }
		const FReferenceSkeleton& Ref = BM->GetRefSkeleton();
		auto RefCS = [&Ref](const FString& Bone, FTransform& T) {
			const int32 I = Ref.FindBoneIndex(FName(*Bone));
			if (I == INDEX_NONE) { return false; }
			T = FAnimationRuntime::GetComponentSpaceTransformRefPose(Ref, I);
			return true; };
		for (const TSharedPtr<FJsonValue>& SV : Soles->GetArrayField(TEXT("sides")))
		{
			const TSharedPtr<FJsonObject> S = SV->AsObject();
			const double Floor = S->GetNumberField(TEXT("floor_cm"));
			for (const TSharedPtr<FJsonValue>& PV : S->GetArrayField(TEXT("parts")))
			{
				const TSharedPtr<FJsonObject> P = PV->AsObject();
				FSolePart Sp;
				Sp.Bone = P->GetStringField(TEXT("bone"));
				FTransform Foot, Ball;
				if (!RefCS(TEXT("foot") + Sp.Bone.Right(2), Foot) || !RefCS(TEXT("ball") + Sp.Bone.Right(2), Ball) || !RefCS(Sp.Bone, Sp.At)) { continue; }
				const TArray<TSharedPtr<FJsonValue>>& Along = P->GetArrayField(TEXT("along_cm"));
				const TArray<TSharedPtr<FJsonValue>>& Across = P->GetArrayField(TEXT("across_cm"));
				const double U0 = Along[0]->AsNumber(), U1 = Along[1]->AsNumber(), V0 = Across[0]->AsNumber(), V1 = Across[1]->AsNumber();
				const FVector B = Ball.GetLocation() * FVector(1.0, 1.0, 0.0);
				Sp.Fw = (Ball.GetLocation() - Foot.GetLocation()) * FVector(1.0, 1.0, 0.0);
				Sp.Fw.Normalize();
				Sp.Ac = FVector(-Sp.Fw.Y, Sp.Fw.X, 0.0);
				if (FVector::DotProduct(Sp.Ac, B) < 0.0) { Sp.Ac = -Sp.Ac; }
				Sp.Centre = B + Sp.Fw * (0.5 * (U0 + U1)) + Sp.Ac * (0.5 * (V0 + V1));
				Sp.Centre.Z = Floor;
				Sp.Len = U1 - U0;
				Sp.Wid = V1 - V0;
				Out.Add(Sp);
			}
		}
		return Out;
	}

	// THE FLOOR'S SHINE SHUT OFF UNDER A SOLE, 30 October 2026 (his order C9; a fresh reviewer: a pale band under
	// Tom's soles on the wet paving): software Lumen traces no skinned mesh, so the wet floor under a toe reflects the
	// sky where it should see the sole's underside. Under each half of each sole a decal (/Game/Ledger/M_LedgerContact:
	// Specular 0, soft at its rim) rides the foot's or the ball's joint, so a heel lifted off the floor takes its decal
	// with it out of reach (DEPTH above and below the sole). HELD the same day (the soles' "decal_held"): the street's
	// water is a clear coat, which no decal reaches. -NoSoleContact lays none.
	inline int32 LayContact(AActor* A, USkeletalMeshComponent* Body, const TSharedPtr<FJsonObject>& C, const TCHAR* Who, const FString& Name)
	{
		UMaterialInterface* M = LoadObject<UMaterialInterface>(nullptr, TEXT("/Game/Ledger/M_LedgerContact.M_LedgerContact"));
		if (M == nullptr)
		{
			UE_LOG(LogTemp, Display, TEXT("LedgerGarments: %s's %s lays no contact (no contact material in this copy)"), Who, *Name);
			return 0;
		}
		const double Margin = C->HasField(TEXT("margin_cm")) ? C->GetNumberField(TEXT("margin_cm")) : 1.5;
		const double Depth = C->HasField(TEXT("depth_cm")) ? C->GetNumberField(TEXT("depth_cm")) : 3.0;
		int32 Laid = 0;
		for (const FSolePart& Sp : SoleParts(Body, C))
		{
			// the decal projects along its X (down here); its Z runs along the foot, its Y across
			const FTransform DecalCS(FRotationMatrix::MakeFromXZ(FVector(0.0, 0.0, -1.0), Sp.Fw).Rotator(), Sp.Centre);
			UDecalComponent* D = NewObject<UDecalComponent>(A, *FString::Printf(TEXT("LedgerContact_%s_%s"), *Name, *Sp.Bone));
			D->SetDecalMaterial(M);
			D->DecalSize = FVector(Depth, 0.5 * Sp.Wid + Margin, 0.5 * Sp.Len + Margin);
			D->SetSortOrder(10);   // over the street's puddles
			D->SetupAttachment(Body, FName(*Sp.Bone));
			D->SetRelativeTransform(DecalCS.GetRelativeTransform(Sp.At));
			D->RegisterComponent();
			++Laid;
		}
		// the wearer's own clothes take no decal: a boot's welt and a hem stand inside the box
		TArray<USkeletalMeshComponent*> Parts;
		A->GetComponents(Parts);
		for (USkeletalMeshComponent* Pc : Parts) { if (Pc != nullptr && (Pc == Body || Pc->GetName().StartsWith(TEXT("LedgerGarment_")))) { Pc->SetReceivesDecals(false); } }
		UE_LOG(LogTemp, Display, TEXT("LedgerGarments: %s's %s lays %d contact decals under its soles"), Who, *Name, Laid);
		return Laid;
	}

	// A STAND-IN ONLY THE LIGHT SEES, 1 November 2026 (his yes of 31 October, the pale band's third try; the shoes plan,
	// its last section): the street's reflections are software Lumen, which traces static meshes only, so the wet floor
	// under a toe found no sole and showed the sky. Under each half sole an upright cylinder (Epic's basic shape, so its
	// footprint is round at the toe and heel), the sole's shape inset a little and about its height, rides the foot's or
	// the ball's joint. It is hidden in the game but kept for indirect light (Affect Indirect Lighting While Hidden, which
	// Lumen's mesh tracing honours: LumenMeshSDFCulling.usf), casts no shadow map (hidden), and its bounds are enlarged
	// past Lumen's 30 cm cull of small traced parts (r.Lumen.DiffuseIndirect.MeshSDF.RadiusThreshold), half a sole being
	// about 12 cm. Dark, as a sole's underside is (/Game/Ledger/M_LedgerSoleStandIn). -NoSoleStandIn lays none;
	// -ShowSoleStandIns draws them, to see where they stand.
	inline int32 LayStandIns(AActor* A, USkeletalMeshComponent* Body, const TSharedPtr<FJsonObject>& Soles, const TSharedPtr<FJsonObject>& S, const TCHAR* Who, const FString& Name)
	{
		UStaticMesh* Cyl = LoadObject<UStaticMesh>(nullptr, TEXT("/Engine/BasicShapes/Cylinder.Cylinder"));
		UMaterialInterface* M = LoadObject<UMaterialInterface>(nullptr, TEXT("/Game/Ledger/M_LedgerSoleStandIn.M_LedgerSoleStandIn"));
		if (Cyl == nullptr || M == nullptr)
		{
			UE_LOG(LogTemp, Display, TEXT("LedgerGarments: %s's %s lays no sole stand-ins (%s)"), Who, *Name, Cyl == nullptr ? TEXT("no cylinder in this copy") : TEXT("no stand-in material in this copy"));
			return 0;
		}
		const double Inset = S->HasField(TEXT("inset_cm")) ? S->GetNumberField(TEXT("inset_cm")) : 0.8;
		const double Height = S->HasField(TEXT("height_cm")) ? S->GetNumberField(TEXT("height_cm")) : 5.0;
		// LIFTED OFF THE FLOOR (1 November, the first pictures: standing on the floor, the floor under a toe lay inside the
		// stand-in, and a reflection ray that starts inside a distance field finds no surface): its underside a little
		// above the sole's floor, so the floor beneath is outside it and its rays meet that underside
		const double Lift = S->HasField(TEXT("lift_cm")) ? S->GetNumberField(TEXT("lift_cm")) : 0.0;
		const float BoundsScale = S->HasField(TEXT("bounds_scale")) ? (float)S->GetNumberField(TEXT("bounds_scale")) : 3.0f;
		const bool bShow = FParse::Param(FCommandLine::Get(), TEXT("ShowSoleStandIns"));
		int32 Laid = 0;
		for (const FSolePart& Sp : SoleParts(Body, Soles))
		{
			// Epic's cylinder is 100 cm across and 100 cm tall about its middle: X along the foot, Y across, Z up
			const FVector Scale(FMath::Max(Sp.Len - 2.0 * Inset, 1.0) / 100.0, FMath::Max(Sp.Wid - 2.0 * Inset, 1.0) / 100.0, Height / 100.0);
			const FTransform CS(FRotationMatrix::MakeFromXY(Sp.Fw, Sp.Ac).Rotator(), Sp.Centre + FVector(0.0, 0.0, Lift + 0.5 * Height), Scale);
			UStaticMeshComponent* C = NewObject<UStaticMeshComponent>(A, *FString::Printf(TEXT("LedgerSoleStandIn_%s_%s"), *Name, *Sp.Bone));
			C->SetStaticMesh(Cyl);
			C->SetMaterial(0, M);
			C->SetMobility(EComponentMobility::Movable);
			C->SetCollisionEnabled(ECollisionEnabled::NoCollision);
			C->SetCastShadow(true);            // a static mesh joins distance-field lighting only while it casts (StaticMeshSceneProxy)
			C->bCastDynamicShadow = true;
			C->SetCastHiddenShadow(false);     // hidden, so no shadow map of its own
			C->bAffectDistanceFieldLighting = true;
			C->SetAffectDynamicIndirectLighting(true);
			C->SetAffectIndirectLightingWhileHidden(true);
			C->SetReceivesDecals(false);
			C->SetBoundsScale(BoundsScale);
			C->SetHiddenInGame(!bShow);
			C->SetupAttachment(Body, FName(*Sp.Bone));
			C->SetRelativeTransform(CS.GetRelativeTransform(Sp.At));
			C->RegisterComponent();
			++Laid;
		}
		UE_LOG(LogTemp, Display, TEXT("LedgerGarments: %s's %s lays %d sole stand-ins for the light%s"), Who, *Name, Laid, bShow ? TEXT(", drawn (-ShowSoleStandIns)") : TEXT(""));
		return Laid;
	}

	// THE HEAD'S TILT AND TURN AGAINST THE CHEST (2 November 2026, Tom's collar's corrective shape): degrees, pitch
	// down positive and yaw either way, from the body's pose now against its reference pose: the head's rotation since
	// rest with the chest's own (spine_05) taken out, applied to the body's forward, which is +Y in a MetaHuman
	// skeleton's own space.
	inline bool HeadAgainstChest(USkeletalMeshComponent* Body, float& PitchDown, float& Yaw)
	{
		if (Body == nullptr || Body->GetSkeletalMeshAsset() == nullptr) { return false; }
		const FReferenceSkeleton& Ref = Body->GetSkeletalMeshAsset()->GetRefSkeleton();
		const int32 Head = Ref.FindBoneIndex(TEXT("head"));
		const int32 Chest = Ref.FindBoneIndex(TEXT("spine_05"));
		if (Head == INDEX_NONE || Chest == INDEX_NONE || Body->GetComponentSpaceTransforms().Num() <= FMath::Max(Head, Chest)) { return false; }
		const FQuat HeadRest = FAnimationRuntime::GetComponentSpaceTransformRefPose(Ref, Head).GetRotation();
		const FQuat ChestRest = FAnimationRuntime::GetComponentSpaceTransformRefPose(Ref, Chest).GetRotation();
		const FQuat HeadDelta = Body->GetComponentSpaceTransforms()[Head].GetRotation() * HeadRest.Inverse();
		const FQuat ChestDelta = Body->GetComponentSpaceTransforms()[Chest].GetRotation() * ChestRest.Inverse();
		const FVector F = (ChestDelta.Inverse() * HeadDelta).RotateVector(FVector(0.0, 1.0, 0.0));
		PitchDown = FMath::RadiansToDegrees(FMath::Asin(FMath::Clamp(-F.Z, -1.0, 1.0)));
		Yaw = FMath::RadiansToDegrees(FMath::Atan2(F.X, F.Y));
		return true;
	}

	// A GARMENT'S CORRECTIVE SHAPES, WEIGHTED EACH FRAME (2 November 2026; garments.json "correctives", tagged by
	// Wear): nil at rest, full at the head tilted down by "pitch_full_deg" or turned by "yaw_full_deg", whichever is
	// more, as MetaHumans' own correctives follow the pose. A follower garment applies its own morph weights after its
	// leader's (SkeletalMeshComponent.cpp, UpdateFollowerComponent). Called by the wearer's tick.
	inline void DriveCorrectives(AActor* A)
	{
		if (A == nullptr) { return; }
		TInlineComponentArray<USkeletalMeshComponent*> Parts;
		A->GetComponents(Parts);
		for (USkeletalMeshComponent* P : Parts)
		{
			if (P == nullptr) { continue; }
			for (const FName& Tag : P->ComponentTags)
			{
				const FString S = Tag.ToString();
				if (!S.StartsWith(TEXT("LedgerCorrective:"))) { continue; }
				TArray<FString> F;
				S.ParseIntoArray(F, TEXT(":"));
				const float FullPitch = F.Num() >= 4 ? FCString::Atof(*F[2]) : 0.0f;
				const float FullYaw = F.Num() >= 4 ? FCString::Atof(*F[3]) : 0.0f;
				float Pitch = 0.0f, Yaw = 0.0f;
				USkeletalMeshComponent* Leader = Cast<USkeletalMeshComponent>(P->LeaderPoseComponent.Get());
				if (FullPitch <= 0.0f || FullYaw <= 0.0f || !HeadAgainstChest(Leader, Pitch, Yaw)) { continue; }
				const float W = FMath::Clamp(FMath::Max(Pitch / FullPitch, FMath::Abs(Yaw) / FullYaw), 0.0f, 1.0f);
				P->SetMorphTarget(FName(*F[1]), W, false);
			}
		}
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
			// -WearHeld=RonJacket,... wears a held one for a test run (30
			// September: the bound jacket filmed moving before Jafar sees it).
			if (G->HasField(TEXT("hold")))
			{
				FString Held;
				FParse::Value(FCommandLine::Get(), TEXT("WearHeld="), Held, false);
				TArray<FString> Tests;
				Held.ParseIntoArray(Tests, TEXT(","), true);
				if (!Tests.Contains(Name))
				{
					UE_LOG(LogTemp, Display, TEXT("LedgerGarments: %s's %s held back: %s"), Who, *Name, *G->GetStringField(TEXT("hold")).Left(80));
					continue;
				}
				UE_LOG(LogTemp, Display, TEXT("LedgerGarments: %s's %s is held, worn for this test run (-WearHeld)"), Who, *Name);
			}
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
			// HELD IN A HAND (2 November): "in_hand": "right" or "left" tags the piece, so the idle's breaks leave
			// that arm alone (PersonAnim.h SetBreakArms; the handbag's hand opened as Sheila fidgeted).
			FString InHand;
			if (G->TryGetStringField(TEXT("in_hand"), InHand)) { Piece->ComponentTags.Add(FName(*(FString(TEXT("LedgerInHand:")) + InHand))); }
			// ITS CORRECTIVE SHAPES (2 November 2026), tagged for DriveCorrectives: "correctives": [{"morph",
			// "pitch_full_deg", "yaw_full_deg"}], each a morph target the import kept (tools/ue/import_garments.py).
			const TArray<TSharedPtr<FJsonValue>>* Correctives = nullptr;
			if (G->TryGetArrayField(TEXT("correctives"), Correctives))
			{
				for (const TSharedPtr<FJsonValue>& CV : *Correctives)
				{
					const TSharedPtr<FJsonObject> CO = CV.IsValid() ? CV->AsObject() : nullptr;
					if (!CO.IsValid()) { continue; }
					const FString Morph = CO->GetStringField(TEXT("morph"));
					const bool bHas = Mesh->FindMorphTarget(FName(*Morph)) != nullptr;
					if (bHas)
					{
						Piece->ComponentTags.Add(FName(*FString::Printf(TEXT("LedgerCorrective:%s:%g:%g"), *Morph,
							CO->GetNumberField(TEXT("pitch_full_deg")), CO->GetNumberField(TEXT("yaw_full_deg")))));
					}
					UE_LOG(LogTemp, Display, TEXT("LedgerGarments: %s's %s corrective %s %s"), Who, *Name, *Morph,
						bHas ? TEXT("weighted by the head's tilt and turn") : TEXT("NOT in this copy's mesh, left off"));
				}
			}
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
			// ITS COVERED PARTS NOT DRAWN (30 October, Tom's jumper under his jacket; Mafia hides a garment's covered
			// parts by an invisible slot): every section of a slot named "Hidden" is switched off, at every level of detail
			{
				const FSkeletalMeshRenderData* RD = Mesh->GetResourceForRendering();
				int32 Off = 0;
				for (int32 Lod = 0; RD != nullptr && Lod < RD->LODRenderData.Num(); ++Lod)
				{
					const TArray<FSkelMeshRenderSection>& Secs = RD->LODRenderData[Lod].RenderSections;
					for (int32 Sec = 0; Sec < Secs.Num(); ++Sec)
					{
						const int32 Mat = Secs[Sec].MaterialIndex;
						if (Slots.IsValidIndex(Mat) && Slots[Mat].ToString().Equals(TEXT("Hidden"), ESearchCase::IgnoreCase)) { Piece->ShowMaterialSection(Mat, Sec, false, Lod); ++Off; }
					}
				}
				if (Off > 0) { UE_LOG(LogTemp, Display, TEXT("LedgerGarments: %s's %s draws not its covered parts (%d sections off)"), Who, *Name, Off); }
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
				// "top": the part that covers the shoulders and ends above the
				// knees (a jacket goes on in its place: made on the bare body,
				// Epic's jumper would come through it).
				auto MeshBottom = [](const USkeletalMeshComponent* C) {
					const USkeletalMesh* M = C->GetSkeletalMeshAsset();
					return M != nullptr ? (float)(M->GetBounds().Origin.Z - M->GetBounds().BoxExtent.Z) : 0.0f; };
				for (USkeletalMeshComponent* C : Parts)
				{
					if (C != nullptr) { UE_LOG(LogTemp, Display, TEXT("LedgerGarments: %s's %s reaches %.0f cm, from %.0f cm"), Who, *C->GetName(), MeshTop(C), MeshBottom(C)); }
				}
				for (USkeletalMeshComponent* C : Parts)
				{
					if (C == nullptr || C == Body || C->GetName() == TEXT("Face")) { continue; }
					const FString Named = (C->GetName() + TEXT(" ") + (C->GetSkeletalMeshAsset() != nullptr ? C->GetSkeletalMeshAsset()->GetName() : FString())).ToLower();
					const float Top = MeshTop(C);
					// THE SHORTS ARE NO TOP, 28 October 2026: Epic's default garment
					// is one mesh with two sections, a shirt and shorts (Tom's two outfit
					// parts both carry both), and both parts report the same bounds (74
					// to 164 cm). Hiding the part whole showed him in his underwear;
					// keeping it whole showed the shirt through the jacket. So a part
					// that holds a lower garment's material (short, trouser, pant, skirt)
					// keeps those sections and loses only the others, at every level of
					// detail; a part with none is hidden whole, as before.
					auto IsLower = [](const FString& N) { return N.Contains(TEXT("short")) || N.Contains(TEXT("trouser")) || N.Contains(TEXT("pant")) || N.Contains(TEXT("skirt")); };
					TArray<FString> MatNames;
					bool bLower = false;
					for (int32 I = 0; I < C->GetNumMaterials(); ++I)
					{
						const UMaterialInterface* Mi = C->GetMaterial(I);
						MatNames.Add(Mi != nullptr ? Mi->GetName().ToLower() : FString());
						bLower |= IsLower(MatNames.Last());
					}
					for (const TSharedPtr<FJsonValue>& H : *Hides)
					{
						const FString Word = H->AsString().ToLower();
						const bool bShoes = Word == TEXT("shoes") && Top < 25.0f;
						const bool bTop = Word == TEXT("top") && Top > 130.0f && MeshBottom(C) > 60.0f;
						// "lower" (30 October, Tom's jeans): the part's lower garment's sections only (the shorts), its
						// others kept; with a jacket hiding "top", the part is then hidden section by section
						if (Word == TEXT("lower") && bLower)
						{
							int32 Off = 0;
							const FSkeletalMeshRenderData* RD = C->GetSkeletalMeshAsset() != nullptr ? C->GetSkeletalMeshAsset()->GetResourceForRendering() : nullptr;
							for (int32 Lod = 0; RD != nullptr && Lod < RD->LODRenderData.Num(); ++Lod)
							{
								const TArray<FSkelMeshRenderSection>& Secs = RD->LODRenderData[Lod].RenderSections;
								for (int32 Sec = 0; Sec < Secs.Num(); ++Sec)
								{
									const int32 Mat = Secs[Sec].MaterialIndex;
									if (MatNames.IsValidIndex(Mat) && IsLower(MatNames[Mat])) { C->ShowMaterialSection(Mat, Sec, false, Lod); ++Off; }
								}
							}
							Hidden += FString::Printf(TEXT(" %s's lower sections (%d)"), *C->GetName(), Off);
							break;
						}
						if (bTop && bLower)
						{
							int32 Off = 0;
							const FSkeletalMeshRenderData* RD = C->GetSkeletalMeshAsset() != nullptr ? C->GetSkeletalMeshAsset()->GetResourceForRendering() : nullptr;
							for (int32 Lod = 0; RD != nullptr && Lod < RD->LODRenderData.Num(); ++Lod)
							{
								const TArray<FSkelMeshRenderSection>& Secs = RD->LODRenderData[Lod].RenderSections;
								for (int32 Sec = 0; Sec < Secs.Num(); ++Sec)
								{
									const int32 Mat = Secs[Sec].MaterialIndex;
									if (MatNames.IsValidIndex(Mat) && !IsLower(MatNames[Mat])) { C->ShowMaterialSection(Mat, Sec, false, Lod); ++Off; }
								}
							}
							Hidden += FString::Printf(TEXT(" %s's top sections (%d, its lower garment kept)"), *C->GetName(), Off);
							break;
						}
						if (bShoes || bTop || (Word != TEXT("shoes") && Word != TEXT("top") && Word != TEXT("lower") && Named.Contains(Word)))
						{
							C->SetVisibility(false, true);
							Hidden += TEXT(" ") + C->GetName();
							break;
						}
					}
				}
			}
			const TSharedPtr<FJsonObject>* Soles = nullptr;
			if (G->TryGetObjectField(TEXT("soles"), Soles))
			{
				if (!(*Soles)->HasField(TEXT("decal_held")) && !FParse::Param(FCommandLine::Get(), TEXT("NoSoleContact"))) { LayContact(A, Body, *Soles, Who, Name); }
				const TSharedPtr<FJsonObject>* Stand = nullptr;
				if ((*Soles)->TryGetObjectField(TEXT("stand_in"), Stand) && !FParse::Param(FCommandLine::Get(), TEXT("NoSoleStandIn"))) { LayStandIns(A, Body, *Soles, *Stand, Who, Name); }
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
