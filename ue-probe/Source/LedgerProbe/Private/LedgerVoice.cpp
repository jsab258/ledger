// TODAY'S VOICE BEHIND THE SEAM (LedgerVoice.h, Jafar's 7 October ruling): the voice server
// beside the game, tools/voice-live/voice-server.py, one JSON line each way over its pipes.
// Moved here unchanged from CrimeProbe.cpp's LiveVoiceStart and LiveVoicePump, so that another
// voice is one more class here and nothing in the game changes.

#include "LedgerVoice.h"
#include "HAL/PlatformProcess.h"
#include "HAL/PlatformMisc.h"
#include "Misc/CommandLine.h"
#include "Misc/Parse.h"
#include "Misc/Paths.h"

namespace
{
	std::string Esc(const std::string& In)
	{
		std::string O;
		for (char Ch : In)
		{
			switch (Ch)
			{
			case '\\': O += "\\\\"; break;
			case '"':  O += "\\\""; break;
			case '\n': O += "\\n"; break;
			case '\r': O += "\\r"; break;
			case '\t': O += "\\t"; break;
			default:   O += Ch; break;
			}
		}
		return O;
	}

	// A string field of one reply line, unescaped; empty when absent.
	std::string Field(const std::string& Line, const char* Name)
	{
		const std::string K = std::string("\"") + Name + "\":\"";
		const std::string::size_type At = Line.find(K);
		if (At == std::string::npos) { return std::string(); }
		std::string R;
		for (std::string::size_type I = At + K.size(); I < Line.size(); ++I)
		{
			if (Line[I] == '\\' && I + 1 < Line.size())
			{
				const char E = Line[++I];
				R += (E == 'n' || E == 'r' || E == 't') ? ' ' : E;
				continue;
			}
			if (Line[I] == '"') { break; }
			R += Line[I];
		}
		return R;
	}

	// A number field of one reply line; -1 when absent.
	double Number(const std::string& Line, const char* Name)
	{
		const std::string K = std::string("\"") + Name + "\":";
		const std::string::size_type P = Line.find(K);
		return P == std::string::npos ? -1.0 : atof(Line.c_str() + P + K.size());
	}

	class FLocalVoiceServer final : public ILedgerVoice
	{
	public:
		virtual ~FLocalVoiceServer() override
		{
			if (Proc.IsValid()) { FPlatformProcess::CloseProc(Proc); }
		}

		virtual bool Start() override
		{
			FString Py, Script;
			if (!FParse::Value(FCommandLine::Get(), TEXT("VoicePython="), Py) || !FParse::Value(FCommandLine::Get(), TEXT("VoiceScript="), Script))
			{
				// THE VOICE BESIDE THE GAME, 30 September (item 3's stopgap for a
				// friends' build, Jafar's ruling): a folder "Voice" next to the game
				// holding today's voice program with its own Python, torch and
				// weights (tools/voice-live, made portable), started with its own
				// paths, so a PC with nothing installed hears the cast. -NoVoice
				// leaves it off.
				const FString Voice = FPaths::ConvertRelativePathToFull(FPaths::Combine(FPaths::RootDir(), TEXT("Voice")));
				Py = Voice / TEXT("python/python.exe");
				Script = Voice / TEXT("tools/voice-live/voice-server.py");
				if (FParse::Param(FCommandLine::Get(), TEXT("NoVoice")) || !FPaths::FileExists(Py) || !FPaths::FileExists(Script)) { return false; }
				FPlatformMisc::SetEnvironmentVar(TEXT("NANO_PKG"), *(Voice / TEXT("nano/src-master/src")));
				FPlatformMisc::SetEnvironmentVar(TEXT("NANO_WEIGHTS"), *(Voice / TEXT("nano/weights")));
				FPlatformMisc::SetEnvironmentVar(TEXT("NANO_VOICE_CACHE"), *(Voice / TEXT("nano/voice-cache")));
				FPlatformMisc::SetEnvironmentVar(TEXT("PYTHONNOUSERSITE"), TEXT("1"));
				const FString Path = FPlatformMisc::GetEnvironmentVariable(TEXT("PATH"));
				FPlatformMisc::SetEnvironmentVar(TEXT("PATH"), *(FPaths::ConvertRelativePathToFull(Voice / TEXT("python")) + TEXT(";")
					+ FPaths::ConvertRelativePathToFull(Voice / TEXT("python/Library/bin")) + TEXT(";") + Path));
				UE_LOG(LogTemp, Display, TEXT("LedgerVoice: the voice beside the game, %s"), *Voice);
			}
			if (!FPlatformProcess::CreatePipe(OutRead, OutWrite) || !FPlatformProcess::CreatePipe(InRead, InWrite, true)) { return false; }
			// --prewarm: the cast voices are learned and run once before the server
			// says it is ready, not on the first line said to each (26 September).
			Proc = FPlatformProcess::CreateProc(*Py, *FString::Printf(TEXT("\"%s\" --prewarm"), *Script), false, true, true,
				nullptr, 0, nullptr, OutWrite, InRead);
			return Proc.IsValid();
		}

		virtual bool IsReady() const override { return bReady && InWrite != nullptr; }

		virtual void Say(int32 Id, const std::string& Who, const std::string& Text, int32 Turn) override
		{
			if (!IsReady()) { return; }
			// "turn": a conversation's turn, so the voice serves the newest first and
			// drops an older turn's unmade sentences (voice-server.py, pick).
			const std::string Req = "{\"id\":" + std::to_string(Id) + ",\"who\":\"" + Esc(Who)
				+ "\",\"text\":\"" + Esc(Text) + "\"" + (Turn > 0 ? ",\"turn\":" + std::to_string(Turn) : std::string()) + "}\n";
			FPlatformProcess::WritePipe(InWrite, FString(UTF8_TO_TCHAR(Req.c_str())));
		}

		// Today's server makes a sentence whole and serves the newest turn first; one no
		// longer wanted costs nothing, and the game throws its sound away on arrival.
		virtual void Cancel(int32 Id) override {}

		virtual void Poll(TArray<FLedgerVoicePiece>& Out) override
		{
			if (OutRead == nullptr) { return; }
			Buf += std::string(TCHAR_TO_UTF8(*FPlatformProcess::ReadPipe(OutRead)));
			std::string::size_type Nl;
			while ((Nl = Buf.find('\n')) != std::string::npos)
			{
				const std::string L = Buf.substr(0, Nl);
				Buf.erase(0, Nl + 1);
				if (L.find("\"ready\"") != std::string::npos) { bReady = true; continue; }
				const std::string::size_type At = L.find("\"id\":");
				if (At == std::string::npos) { continue; }
				FLedgerVoicePiece P;
				P.Id = atoi(L.c_str() + At + 5);
				const std::string Wav = Field(L, "wav");
				P.Wav = Wav.empty() || Wav == "none" ? FString() : FString(UTF8_TO_TCHAR(Wav.c_str()));
				P.bLast = L.find("\"last\":true") != std::string::npos || L.find("\"error\"") != std::string::npos;
				P.bJoined = L.find("\"joined\":true") != std::string::npos;
				const double Ms = Number(L, "ms");
				P.WorkS = Ms >= 0.0 ? Ms / 1000.0 : -1.0;
				P.LenS = Number(L, "seconds");
				Out.Add(P);
			}
		}

		virtual const TCHAR* Name() const override { return TEXT("local"); }

	private:
		FProcHandle Proc;
		void* OutRead = nullptr; void* OutWrite = nullptr; void* InRead = nullptr; void* InWrite = nullptr;
		std::string Buf;
		bool bReady = false;
	};
}

TUniquePtr<ILedgerVoice> MakeLedgerVoice()
{
	FString Which = TEXT("local");
	FParse::Value(FCommandLine::Get(), TEXT("VoiceKind="), Which);
	if (Which == TEXT("local")) { return MakeUnique<FLocalVoiceServer>(); }
	UE_LOG(LogTemp, Warning, TEXT("LedgerVoice: no voice called '%s' (only 'local' today); the answers stay text"), *Which);
	return nullptr;
}
