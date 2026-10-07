#pragma once

// THE VOICE BEHIND ONE SEAM (Jafar, 7 October: "Keep the voice behind one swappable seam, so a
// better local voice or a cheaper cloud one can be dropped in later without touching anything
// else"). The game asks a voice for one sentence at a time in a character's cast voice and plays
// the sound files that come back; everything it knows of the voice is this interface. Today's is
// the voice server beside the game (LedgerVoice.cpp, FLocalVoiceServer, tools/voice-live/
// voice-server.py); another is one more class behind MakeLedgerVoice, chosen by -VoiceKind=<name>.

#include "CoreMinimal.h"
#include <string>

/// One piece of sound back from the voice: a sentence, or part of one from a voice that streams.
struct FLedgerVoicePiece
{
	int32 Id = 0;            // the sentence's request id, as Say was given it
	FString Wav;             // its sound file (16-bit PCM WAV); empty when this piece carries none
	bool bLast = false;      // the sentence's last piece (or its error): nothing more comes for Id
	bool bJoined = false;    // continues the piece before it, with no gap
	double WorkS = -1.0;     // the voice's own time making it, when it says
	double LenS = -1.0;      // the sound's length, when it says
};

class ILedgerVoice
{
public:
	virtual ~ILedgerVoice() {}
	/// Begins starting the voice; false when there is none to start (nothing installed, -NoVoice).
	virtual bool Start() = 0;
	/// True once it can take sentences.
	virtual bool IsReady() const = 0;
	/// One sentence to say in Who's cast voice. Turn: the conversation's turn, so a voice may
	/// serve the newest first and drop an older turn's unmade sentences.
	virtual void Say(int32 Id, const std::string& Who, const std::string& Text, int32 Turn) = 0;
	/// The sentence is no longer wanted (its turn went another way): a voice that bills by the
	/// character stops making it. Whatever of it still arrives, the game throws away.
	virtual void Cancel(int32 Id) = 0;
	/// What has come back since the last call, in order of arrival.
	virtual void Poll(TArray<FLedgerVoicePiece>& Out) = 0;
	/// Its name, for the log and the session record.
	virtual const TCHAR* Name() const = 0;
};

/// The voice this run uses: -VoiceKind=<name> on the command line, else today's ("local"). Null when
/// the name is unknown; nothing is signed up for or bought, so there is no cloud voice yet.
TUniquePtr<ILedgerVoice> MakeLedgerVoice();
