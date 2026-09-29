// THE SESSION RECORD, 29 September (the town session's handover 6p;
// production/specs/session-record.md). While somebody plays, the game writes
// what it can see, one JSON line per event, to Saved/Sessions/
// <yyyy-mm-dd-hhmmss>.jsonl (UTF-8, no byte-order mark): where they went, when
// they went still, the deed, who in town showed they knew, whom they talked
// to and named, how each answer went, a load, and the end with what the talk
// cost. Never the words typed, and no field the page does not list.
// `python tools/session_read.py <file or folder>` reads it for Jafar's
// runbook. The player is "jafar" in his copy, "friend" in a friend's (a copy
// with a relay code, LEDGER_COPY, or -SessionPlayer=friend).
#pragma once

#include "CoreMinimal.h"
#include "Dom/JsonObject.h"
#include "HAL/PlatformMisc.h"
#include "HAL/PlatformTime.h"
#include "Misc/CommandLine.h"
#include "Misc/DateTime.h"
#include "Misc/FileHelper.h"
#include "Misc/Paths.h"
#include "Serialization/JsonReader.h"
#include "Serialization/JsonSerializer.h"

namespace LedgerSession
{
	struct FPlace { FString Id; double X = 0.0, Z = 0.0; };

	struct FState
	{
		FString Path;
		double T0 = 0.0;
		bool bOpen = false, bEnded = false;
		TArray<FPlace> Places;
		FString LastPlace;
		FVector LastPos = FVector::ZeroVector;
		double StillFrom = -1.0;   // when he last stopped moving and typing
		double NextLook = 0.0;
	};

	inline FState& S() { static FState St; return St; }

	inline FString Esc(const FString& In)
	{
		FString O;
		for (TCHAR C : In)
		{
			if (C == TEXT('"') || C == TEXT('\\')) { O.AppendChar(TEXT('\\')); O.AppendChar(C); }
			else if (C < 0x20) { O += FString::Printf(TEXT("\\u%04x"), (int32)C); }
			else { O.AppendChar(C); }
		}
		return O;
	}

	inline FString Str(const FString& V) { return TEXT("\"") + Esc(V) + TEXT("\""); }

	inline FString List(const TArray<FString>& Vs)
	{
		FString O = TEXT("[");
		for (int32 I = 0; I < Vs.Num(); ++I) { O += (I ? TEXT(",") : TEXT("")) + Str(Vs[I]); }
		return O + TEXT("]");
	}

	// One line: {"t":12.3,"e":"...",<fields>}.
	inline void Write(const TCHAR* Event, const FString& Fields = FString())
	{
		FState& St = S();
		if (!St.bOpen || St.bEnded) { return; }
		const double T = FPlatformTime::Seconds() - St.T0;
		const FString Line = FString::Printf(TEXT("{\"t\":%.1f,\"e\":\"%s\"%s%s}\n"), T, Event, Fields.IsEmpty() ? TEXT("") : TEXT(","), *Fields);
		FFileHelper::SaveStringToFile(Line, *St.Path, FFileHelper::EEncodingOptions::ForceUTF8WithoutBOM, &IFileManager::Get(), FILEWRITE_Append);
	}

	// The places of the cast's routines, where the street file puts them
	// (x along the street, z across, in metres; the engine's X and Y are
	// those times 100).
	inline void LoadPlaces(const FString& CastFile)
	{
		FString Text;
		if (!FFileHelper::LoadFileToString(Text, *CastFile)) { return; }
		TSharedPtr<FJsonObject> Root;
		if (!FJsonSerializer::Deserialize(TJsonReaderFactory<>::Create(Text), Root) || !Root.IsValid()) { return; }
		const TSharedPtr<FJsonObject>* Places = nullptr;
		if (!Root->TryGetObjectField(TEXT("places"), Places) || Places == nullptr) { return; }
		for (const auto& Kv : (*Places)->Values)
		{
			const TSharedPtr<FJsonObject>* P = nullptr;
			if (!Kv.Value.IsValid() || !Kv.Value->TryGetObject(P) || P == nullptr) { continue; }
			double X = 0.0, Z = 0.0;
			if ((*P)->TryGetNumberField(TEXT("x_m"), X) && (*P)->TryGetNumberField(TEXT("z_m"), Z))
			{
				FPlace Place;
				Place.Id = Kv.Key;
				Place.X = X;
				Place.Z = Z;
				S().Places.Add(Place);
			}
		}
	}

	inline void Start(const FString& Build, bool bFresh, const FString& CastFile)
	{
		FState& St = S();
		if (St.bOpen) { return; }
		FString Player;
		if (!FParse::Value(FCommandLine::Get(), TEXT("SessionPlayer="), Player) || Player.IsEmpty())
		{
			Player = FPlatformMisc::GetEnvironmentVariable(TEXT("LEDGER_COPY")).IsEmpty() ? TEXT("jafar") : TEXT("friend");
		}
		const FString Dir = FPaths::Combine(FPaths::ProjectSavedDir(), TEXT("Sessions"));
		IFileManager::Get().MakeDirectory(*Dir, true);
		St.Path = FPaths::ConvertRelativePathToFull(Dir / (FDateTime::Now().ToString(TEXT("%Y-%m-%d-%H%M%S")) + TEXT(".jsonl")));
		St.T0 = FPlatformTime::Seconds();
		St.bOpen = true;
		LoadPlaces(CastFile);
		Write(TEXT("start"), TEXT("\"player\":") + Str(Player) + TEXT(",\"build\":") + Str(Build) + TEXT(",\"fresh\":") + (bFresh ? TEXT("true") : TEXT("false")));
		UE_LOG(LogTemp, Display, TEXT("LedgerSession: recording to %s (%s, %d places)"), *St.Path, *Player, St.Places.Num());
	}

	// Where he is and whether he has gone still, looked at twice a second:
	// a place is written when he comes within 6 m of one other than the last
	// written; a still spell of 20 s or more when it ends.
	inline void Look(const FVector& Pawn, bool bBusyTyping)
	{
		FState& St = S();
		if (!St.bOpen || St.bEnded) { return; }
		const double Now = FPlatformTime::Seconds();
		if (Now < St.NextLook) { return; }
		St.NextLook = Now + 0.5;
		const double X = Pawn.X / 100.0, Z = Pawn.Y / 100.0;
		const FPlace* Near = nullptr;
		double Best = 6.0;
		for (const FPlace& P : St.Places)
		{
			const double D = FMath::Sqrt((P.X - X) * (P.X - X) + (P.Z - Z) * (P.Z - Z));
			if (D <= Best) { Best = D; Near = &P; }
		}
		if (Near != nullptr && Near->Id != St.LastPlace)
		{
			St.LastPlace = Near->Id;
			Write(TEXT("place"), TEXT("\"at\":") + Str(Near->Id));
		}
		const bool bMoved = FVector::Dist2D(Pawn, St.LastPos) > 10.0;   // 10 cm in half a second
		St.LastPos = Pawn;
		if (bMoved || bBusyTyping)
		{
			if (St.StillFrom >= 0.0 && Now - St.StillFrom >= 20.0)
			{
				Write(TEXT("still"), FString::Printf(TEXT("\"s\":%.0f"), Now - St.StillFrom) + (St.LastPlace.IsEmpty() ? FString() : TEXT(",\"at\":") + Str(St.LastPlace)));
			}
			St.StillFrom = -1.0;
		}
		else if (St.StillFrom < 0.0) { St.StillFrom = Now; }
	}

	inline void End(const TCHAR* Why, double Usd)
	{
		FState& St = S();
		if (!St.bOpen || St.bEnded) { return; }
		const double Now = FPlatformTime::Seconds();
		if (St.StillFrom >= 0.0 && Now - St.StillFrom >= 20.0)
		{
			Write(TEXT("still"), FString::Printf(TEXT("\"s\":%.0f"), Now - St.StillFrom) + (St.LastPlace.IsEmpty() ? FString() : TEXT(",\"at\":") + Str(St.LastPlace)));
		}
		Write(TEXT("end"), FString::Printf(TEXT("\"why\":\"%s\""), Why) + (Usd >= 0.0 ? FString::Printf(TEXT(",\"usd\":%.4f"), Usd) : FString()));
		St.bEnded = true;
	}
}
