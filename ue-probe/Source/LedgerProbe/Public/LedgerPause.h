// THE PAUSE PAGE, 1 October: the evening paper's STOP PRESS box
// (production/design/ui/step2/pictures/pause-*.webp), over the street held
// still and blurred. Back to the street, the Ledger (the notebook, not yet in
// the game, so it stands unavailable with its reason, as the guide draws an
// unavailable choice), Settings, Quit to the title and Quit the game, each of
// the last two asked once more with the safe choice in hand first.
#pragma once

#include "CoreMinimal.h"

class UWorld;

namespace LedgerPause
{
	struct FWhen
	{
		int32 Day = 0, Hour = 0, Minute = 0;          // the story's own clock now
		int32 SavedHour = -1, SavedMinute = 0;        // when it was last saved, -1 when it has not been
	};
	enum class EAction : uint8 { None, Resume, QuitToTitle, QuitGame };

	void Show(UWorld* World, const FWhen& When);
	// Every frame while shown: an action once, on the frame it is taken.
	EAction Tick();
	void Hide();
	bool IsShown();
}
