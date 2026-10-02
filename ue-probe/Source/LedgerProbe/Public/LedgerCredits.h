// THE CREDITS PAGE, 1 October (the rulings sweep: "the attributions themselves,
// for everything shipped" and no credits page anywhere): the evening paper's
// page over the street, from production/specs/credits.json, which keeps step
// with THIRD-PARTY.md. Opened from the title; Esc (or a pad's B) takes him back.
#pragma once

#include "CoreMinimal.h"

class UWorld;

namespace LedgerCredits
{
	void Show(UWorld* World, TFunction<void()> OnClosed);
	void Hide();
	bool IsShown();
}
