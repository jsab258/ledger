// THE TITLE SCREEN, 30 September (the twenty a friend would notice: 2, 3, 4
// and 5). A friend's copy used to open straight into the story with the
// street still building itself: a black window, then objects popping in
// while this PC's graphics card prepared its shaders, and no way to choose a
// new story, go back to the saved one, or turn the picture down for a
// weaker card.
//
// Now the street loads behind a title: New game, Continue (when a story is
// saved), Picture (Low, Medium, High, Highest) and Quit, with a line saying
// what is being got ready and how much is left. New game and Continue wait
// until the card has nothing left to prepare. On the first launch on a PC it
// goes full screen at the desktop's own size and takes the picture level the
// engine's own benchmark picks for that card.
//
// Slate, like the rest of the game's words on screen (CrimeProbe.cpp), since
// this project makes no Blueprint or widget assets. Shown by the live
// encounter (CrimeProbe.cpp, the LiveTitle phase); never in the automation's
// scripted runs, and -NoTitle skips it.
#pragma once

#include "CoreMinimal.h"

class UWorld;

namespace LedgerTitle
{
	enum class EChoice : uint8 { None, NewGame, Continue, Quit };

	// Once per PC (a mark in the game's own settings file): full screen at the
	// desktop's size, and the benchmark's picture level.
	void FirstLaunchSettings();

	void Show(UWorld* World, bool bCanContinue);

	// Every frame while shown. bStreetReady once the street and its people
	// are placed. Returns a choice once, on the frame it is made.
	EChoice Tick(UWorld* World, bool bStreetReady);

	void Hide(UWorld* World);
	bool IsShown();

	// The picture level's name for the log and the button: Low, Medium, High,
	// Highest, or "set for this PC" when the benchmark mixed them.
	FString PictureName();
}
