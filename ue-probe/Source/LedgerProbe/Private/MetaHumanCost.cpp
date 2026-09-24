// See MetaHumanCost.h. The card's time is RHIGetGPUFrameCycles, the engine's
// own measure of the GPU's frame, read every frame with the frame rate
// uncapped; the memory is the RHI's texture memory (streaming plus not),
// read at the end of each condition. The process's whole dedicated video
// memory is sampled from outside the game by the caller, because the engine
// does not report it; this file prints the moment each condition starts so
// the two can be lined up.
#include "MetaHumanCost.h"

#include "Containers/Ticker.h"
#include "DynamicRHI.h"
#include "Engine/Engine.h"
#include "Engine/World.h"
#include "GameFramework/Actor.h"
#include "GameFramework/PlayerController.h"
#include "Camera/PlayerCameraManager.h"
#include "HAL/PlatformTime.h"
#include "Misc/CommandLine.h"
#include "Misc/FileHelper.h"
#include "Misc/Paths.h"
#include "RHIStats.h"
#include "ShaderCompiler.h"
#include "UnrealClient.h"

#include <algorithm>
#include <string>
#include <vector>

namespace LedgerMhCost
{
	struct Condition
	{
		FString Name;
		TArray<FString> Who;       // cast ids, spawned side by side
	};

	const TCHAR* kCast[] = { TEXT("rocco"), TEXT("lena"), TEXT("sam") };
	const double kWorldCeiling = 60.0;
	const double kSettleSeconds = 6.0;     // streaming and the first frames' shader work
	const int32  kSampleFrames = 300;
	const double kAheadCm = 350.0, kSpacingCm = 80.0;

	FTSTicker::FDelegateHandle GTicker;
	TArray<Condition> GConds;
	int32 GAt = -1;
	double GStart = 0.0, GPhaseStart = 0.0;
	enum class EPhase : uint8 { WaitWorld, Place, Settle, Sample, Done };
	EPhase GPhase = EPhase::WaitWorld;
	TArray<AActor*> GSpawned;
	std::vector<double> GGpuMs, GFrameMs;
	TArray<FString> GLines;
	double GBaseGpuMedian = -1.0;
	int64 GBaseTexBytes = -1;
	double GLastTick = 0.0;

	UWorld* GameWorld()
	{
		if (!GEngine) { return nullptr; }
		for (const FWorldContext& Ctx : GEngine->GetWorldContexts())
		{
			if (Ctx.WorldType == EWorldType::Game && Ctx.World() != nullptr) { return Ctx.World(); }
		}
		return nullptr;
	}

	FString ClassPathFor(const FString& Who)
	{
		const FString Name = TEXT("MH_") + Who.Left(1).ToUpper() + Who.Mid(1);
		return FString::Printf(TEXT("/Game/Ledger/MetaHumans/%s/BP_%s.BP_%s_C"), *Name, *Name, *Name);
	}

	double Percentile(std::vector<double> V, double P)
	{
		if (V.empty()) { return -1.0; }
		std::sort(V.begin(), V.end());
		const size_t I = (size_t)std::min<double>((double)V.size() - 1, P * (double)(V.size() - 1) + 0.5);
		return V[I];
	}

	int64 TextureBytes()
	{
		FTextureMemoryStats S;
		RHIGetTextureMemoryStats(S);
		return (int64)S.StreamingMemorySize + (int64)S.NonStreamingMemorySize;
	}

	void Place(UWorld* World)
	{
		const Condition& C = GConds[GAt];
		APlayerController* PC = World->GetFirstPlayerController();
		FVector Eye = FVector::ZeroVector;
		FRotator View = FRotator::ZeroRotator;
		if (PC != nullptr && PC->PlayerCameraManager != nullptr)
		{
			Eye = PC->PlayerCameraManager->GetCameraLocation();
			View = PC->PlayerCameraManager->GetCameraRotation();
		}
		const FRotator Flat(0.0f, View.Yaw, 0.0f);
		const FVector Fwd = Flat.Vector();
		const FVector Right = FRotationMatrix(Flat).GetScaledAxis(EAxis::Y);
		FString Notes;
		for (int32 I = 0; I < C.Who.Num(); ++I)
		{
			UClass* Cls = LoadClass<AActor>(nullptr, *ClassPathFor(C.Who[I]));
			if (Cls == nullptr) { Notes += TEXT("/") + C.Who[I] + TEXT("-class-not-found"); continue; }
			const float Off = (float)((I - (C.Who.Num() - 1) * 0.5) * kSpacingCm);
			// FEET ON THE GROUND UNDER THE EYE: the pawn's eye is about 1.6 m up.
			FVector At = Eye + Fwd * (float)kAheadCm + Right * Off;
			At.Z = Eye.Z - 160.0f;
			// A MetaHuman faces its actor's +Y, so facing the camera is the
			// view's yaw turned round, less ninety.
			const FRotator Face(0.0f, View.Yaw + 180.0f - 90.0f, 0.0f);
			FActorSpawnParameters P;
			P.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
			if (AActor* A = World->SpawnActor<AActor>(Cls, At, Face, P)) { GSpawned.Add(A); }
			else { Notes += TEXT("/") + C.Who[I] + TEXT("-spawn-failed"); }
		}
		GLines.Add(FString::Printf(TEXT("mhcostStart cond=%s at=%.1fs spawned=%d/%d note=%s"),
			*C.Name, FPlatformTime::Seconds() - GStart, GSpawned.Num(), C.Who.Num(), Notes.IsEmpty() ? TEXT("none") : *Notes));
	}

	void Clear()
	{
		for (AActor* A : GSpawned) { if (IsValid(A)) { A->Destroy(); } }
		GSpawned.Reset();
	}

	void Finish()
	{
		const FString Out = FPaths::ConvertRelativePathToFull(FPaths::ProjectDir() / TEXT("ue-mhcost.txt"));
		FString Text;
		Text += TEXT("# What each MetaHuman costs on the card, standing 3.5 m in front of the camera in the street.\n");
		Text += TEXT("# gpuMs is RHIGetGPUFrameCycles per frame, uncapped; texMB is the RHI's texture memory; delta is against nobody.\n");
		for (const FString& L : GLines) { Text += L + TEXT("\n"); }
		FFileHelper::SaveStringToFile(Text, *Out, FFileHelper::EEncodingOptions::ForceUTF8WithoutBOM);
		FTSTicker::GetCoreTicker().RemoveTicker(GTicker);
		FPlatformMisc::RequestExit(false);
	}

	bool Tick(float)
	{
		const double Now = FPlatformTime::Seconds();
		const double Delta = GLastTick > 0.0 ? Now - GLastTick : 0.0;
		GLastTick = Now;
		UWorld* World = GameWorld();
		switch (GPhase)
		{
		case EPhase::WaitWorld:
			if (World == nullptr || World->GetFirstPlayerController() == nullptr)
			{
				if (Now - GStart > kWorldCeiling) { GLines.Add(TEXT("mhcost status=NO-WORLD")); Finish(); return false; }
				return true;
			}
			if (GEngine != nullptr)
			{
				GEngine->Exec(World, TEXT("t.MaxFPS 0"));
				GEngine->Exec(World, TEXT("r.VSync 0"));
			}
			GAt = 0;
			GPhase = EPhase::Place;
			return true;
		case EPhase::Place:
			Clear();
			Place(World);
			GPhaseStart = Now;
			GPhase = EPhase::Settle;
			return true;
		case EPhase::Settle:
			if (Now - GPhaseStart < kSettleSeconds) { return true; }
			// AND NO SHADER STILL COMPILING: run from the editor, a MetaHuman's
			// materials compile on first sight and draw with a stand-in until
			// they have, which would be measuring the stand-in. Three minutes
			// at most, and the line says if it was cut short.
			if (GShaderCompilingManager != nullptr && GShaderCompilingManager->GetNumRemainingJobs() > 0
			    && Now - GPhaseStart < 180.0) { return true; }
			GGpuMs.clear(); GFrameMs.clear();
			// A PICTURE OF EACH, so a cost is never a cost of somebody who was
			// not on the screen.
			FScreenshotRequest::RequestScreenshot(FPaths::ConvertRelativePathToFull(
				FPaths::ProjectDir() / FString::Printf(TEXT("ue-mhcost-%s.png"), *GConds[GAt].Name)), false, false);
			GPhase = EPhase::Sample;
			return true;
		case EPhase::Sample:
		{
			GGpuMs.push_back(FPlatformTime::ToMilliseconds(RHIGetGPUFrameCycles(0)));
			if (Delta > 0.0) { GFrameMs.push_back(Delta * 1000.0); }
			if ((int32)GGpuMs.size() < kSampleFrames) { return true; }
			const double Med = Percentile(GGpuMs, 0.5), P95 = Percentile(GGpuMs, 0.95);
			const int64 Tex = TextureBytes();
			if (GAt == 0) { GBaseGpuMedian = Med; GBaseTexBytes = Tex; }
			const int32 Pending = GShaderCompilingManager != nullptr ? GShaderCompilingManager->GetNumRemainingJobs() : 0;
			GLines.Add(FString::Printf(TEXT("mhcost cond=%s gpuMsMedian=%.2f gpuMsP95=%.2f frameMsMedian=%.2f texMB=%.0f deltaGpuMs=%+.2f deltaTexMB=%+.0f frames=%d shadersPending=%d endAt=%.1fs"),
				*GConds[GAt].Name, Med, P95, Percentile(GFrameMs, 0.5), Tex / 1048576.0,
				GBaseGpuMedian >= 0.0 ? Med - GBaseGpuMedian : 0.0,
				GBaseTexBytes >= 0 ? (Tex - GBaseTexBytes) / 1048576.0 : 0.0, (int32)GGpuMs.size(), Pending, Now - GStart));
			++GAt;
			if (GAt >= GConds.Num()) { Clear(); Finish(); return false; }
			GPhase = EPhase::Place;
			return true;
		}
		default:
			Finish();
			return false;
		}
	}

	void Start()
	{
		GStart = FPlatformTime::Seconds();
		GConds.Reset();
		GConds.Add({ TEXT("nobody"), {} });
		for (const TCHAR* W : kCast) { GConds.Add({ W, { W } }); }
		GConds.Add({ TEXT("all-three"), { kCast[0], kCast[1], kCast[2] } });
		// AND THE STAND-IN, measured the same way, so the change is a number.
		FString Also;
		if (FParse::Value(FCommandLine::Get(), TEXT("MhCostAlso="), Also) && !Also.IsEmpty())
		{
			GConds.Add({ Also, { Also } });
		}
		GTicker = FTSTicker::GetCoreTicker().AddTicker(FTickerDelegate::CreateStatic(&Tick), 0.0f);
	}
}
