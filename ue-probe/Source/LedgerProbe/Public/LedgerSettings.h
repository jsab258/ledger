// THE SETTINGS PAGE, 1 October: the evening paper's listings page
// (production/design/ui/step2/pictures/settings-*.webp, STYLE-GUIDE.md's
// Quality and Settings line), over the live street, dimmed but not blurred,
// so each change shows as it is made. Four sections: Picture (as drawn: the
// quality preset over the five lines it sets, then the screen's own lines),
// Sound, Controls, and Subtitles and reading (from the design research's
// accessibility list, production/research/ui-design/PIPELINE-AND-STANDARDS.md).
//
// The picture and the screen are the engine's own settings (GameUserSettings);
// the rest are kept beside them in the same file, under [LedgerSettings], and
// read by the screens that use them (subtitles, prompts, the camera).
#pragma once

#include "CoreMinimal.h"

class UWorld;

namespace LedgerSettings
{
	// Opens over the title or the pause page; OnClosed runs when Esc takes him back.
	void Show(UWorld* World, TFunction<void()> OnClosed);
	void Hide();
	bool IsShown();

	// The player's own settings that are not the engine's, read once at start.
	void Load();
	bool SubtitlesOn();
	float SubtitleUnits();        // 34, 39 (the guide's), 46 or 54
	bool SpeakerNames();
	bool SuggestAlways();         // suggested lines always there, or on Tab only
	float LookSensitivity();      // 0.5 to 2
	bool InvertLook();
}
