#include "TitleScreen.h"

#include "Brushes/SlateColorBrush.h"
#include "CoreGlobals.h"
#include "Engine/Engine.h"
#include "Engine/GameViewportClient.h"
#include "Engine/World.h"
#include "Framework/Application/SlateApplication.h"
#include "GameFramework/GameUserSettings.h"
#include "GameFramework/PlayerController.h"
#include "Misc/ConfigCacheIni.h"
#include "Misc/App.h"
#include "Misc/CommandLine.h"
#include "UnrealClient.h"
#include "PipelineStateCache.h"
#include "ShaderPipelineCache.h"
#include "Styling/CoreStyle.h"
#include "Widgets/Input/SButton.h"
#include "Widgets/Layout/SBorder.h"
#include "Widgets/Layout/SBox.h"
#include "Widgets/SBoxPanel.h"
#include "Widgets/SOverlay.h"
#include "Widgets/Text/STextBlock.h"

namespace LedgerTitle
{
namespace
{
	TSharedPtr<SWidget> GRoot;
	TSharedPtr<STextBlock> GStatus;
	TSharedPtr<SButton> GContinue, GNew, GPicture, GQuit;
	TWeakObjectPtr<UWorld> GWorld;
	EChoice GChosen = EChoice::None;
	bool bShown = false;
	bool bCanContinue = false;
	bool bReady = false;
	double GShownAt = 0.0;
	double GQuietSince = -1.0;
	int32 GMostPending = 0;
	EChoice GPendingChoice = EChoice::None;
	TWeakPtr<SWidget> GModeWidget;
	bool bMeasured = false;
	int32 GMeasureFrames = 0;
	// WHAT EACH PICTURE COSTS: the mean frame from one to four seconds after
	// a change, in the log, so the levels' difference is measured.
	double GFrameFrom = -1.0, GFrameSum = 0.0;
	int32 GFrameCount = 0;

	// WAITING FOR THE CARD: the pipelines this PC is still preparing, both the
	// engine's own precaching of what is in view and any bundled cache. At
	// most two minutes, so a card that never reports done still lets him in.
	constexpr double kQuietFor = 1.5;
	constexpr double kWaitAtMost = 120.0;

	const FLinearColor kCream(0.95f, 0.92f, 0.82f, 1.0f);
	const FLinearColor kGold(1.0f, 0.78f, 0.35f, 1.0f);
	const FLinearColor kDim(0.6f, 0.58f, 0.52f, 1.0f);

	const FButtonStyle& ButtonStyle()
	{
		static const FButtonStyle Style = []()
		{
			FButtonStyle B = FCoreStyle::Get().GetWidgetStyle<FButtonStyle>("Button");
			B.SetNormal(FSlateColorBrush(FLinearColor(0.0f, 0.0f, 0.0f, 0.45f)));
			B.SetHovered(FSlateColorBrush(FLinearColor(0.45f, 0.33f, 0.14f, 0.65f)));
			B.SetPressed(FSlateColorBrush(FLinearColor(0.6f, 0.45f, 0.2f, 0.85f)));
			B.SetDisabled(FSlateColorBrush(FLinearColor(0.0f, 0.0f, 0.0f, 0.25f)));
			B.SetNormalPadding(FMargin(0.0f));
			B.SetPressedPadding(FMargin(0.0f));
			return B;
		}();
		return Style;
	}

	int32 PictureLevel()
	{
		UGameUserSettings* S = GEngine != nullptr ? GEngine->GetGameUserSettings() : nullptr;
		if (S == nullptr) { return -1; }
		const int32 L = S->GetOverallScalabilityLevel();
		return L < 0 ? -1 : FMath::Min(L, 3);
	}

	// A BUTTON WHOSE WORDS TURN GOLD WHEN IT IS THE ONE CHOSEN, by the keys
	// or under the mouse: Slate draws no mark of its own for keyboard focus.
	TSharedRef<SButton> MakeButton(TFunction<FString()> Label, TFunction<bool()> Enabled, TFunction<void()> OnPress)
	{
		TSharedRef<TWeakPtr<SButton>> Self = MakeShared<TWeakPtr<SButton>>();
		TSharedRef<SButton> B = SNew(SButton)
			.ButtonStyle(&ButtonStyle())
			.HAlign(HAlign_Center)
			.ContentPadding(FMargin(28.0f, 9.0f))
			.IsEnabled_Lambda([Enabled]() { return Enabled(); })
			.OnClicked_Lambda([OnPress]() { OnPress(); return FReply::Handled(); })
			[
				SNew(STextBlock)
				.Text_Lambda([Label]() { return FText::FromString(Label()); })
				.Font(FCoreStyle::GetDefaultFontStyle("Bold", 20))
				.ColorAndOpacity_Lambda([Self, Enabled]()
				{
					const TSharedPtr<SButton> Me = Self->Pin();
					if (!Enabled()) { return FSlateColor(kDim); }
					return FSlateColor(Me.IsValid() && (Me->HasKeyboardFocus() || Me->IsHovered()) ? kGold : kCream);
				})
			];
		*Self = B;
		return B;
	}

	// The first button that can be taken, focused; true once it has the keys.
	bool FocusFirst()
	{
		for (const TSharedPtr<SButton>& B : { GContinue, GNew, GPicture, GQuit })
		{
			if (B.IsValid() && B->IsEnabled())
			{
				// THE INPUT MODE REMEMBERS ITS WIDGET and gives it the keys back
				// whenever the window comes to the front: set at the start to
				// Picture, it took them back from New game (the tester, 30
				// September). So it is pointed at this one too.
				UWorld* W = GWorld.Get();
				if (W != nullptr && GModeWidget.Pin() != B)
				{
					GModeWidget = B;
					if (APlayerController* PC = W->GetFirstPlayerController())
					{
						FInputModeUIOnly M;
						M.SetWidgetToFocus(B);
						M.SetLockMouseToViewportBehavior(EMouseLockMode::DoNotLock);
						PC->SetInputMode(M);
					}
				}
				FSlateApplication::Get().SetUserFocus(0, B, EFocusCause::SetDirectly);
				FSlateApplication::Get().SetKeyboardFocus(B, EFocusCause::SetDirectly);
				return FSlateApplication::Get().GetKeyboardFocusedWidget() == B;
			}
		}
		return false;
	}

	bool OneOfOurs(const TSharedPtr<SWidget>& W)
	{
		return W.IsValid() && (W == GContinue || W == GNew || W == GPicture || W == GQuit);
	}
}

FString PictureName()
{
	switch (PictureLevel())
	{
	case 0: return TEXT("Low");
	case 1: return TEXT("Medium");
	case 2: return TEXT("High");
	case 3: return TEXT("Highest");
	default: return TEXT("set for this PC");
	}
}

void FirstLaunchSettings()
{
	UGameUserSettings* S = GEngine != nullptr ? GEngine->GetGameUserSettings() : nullptr;
	if (S == nullptr || GConfig == nullptr) { return; }
	bool bDone = false;
	GConfig->GetBool(TEXT("Ledger"), TEXT("FirstLaunchDone"), bDone, GGameUserSettingsIni);
	if (bDone) { return; }
	const double T0 = FPlatformTime::Seconds();
	// THE CARD PICKS ITS OWN PICTURE: the engine's benchmark, run once.
	S->RunHardwareBenchmark();
	S->ApplyHardwareBenchmarkResults();
	// AND THE WHOLE SCREEN AT ITS OWN SIZE, borderless, on the main monitor.
	S->SetFullscreenMode(EWindowMode::WindowedFullscreen);
	S->SetScreenResolution(S->GetDesktopResolution());
	// Command-line window arguments (the AI tester's) still win.
	S->ApplySettings(true);
	GConfig->SetBool(TEXT("Ledger"), TEXT("FirstLaunchDone"), true, GGameUserSettingsIni);
	GConfig->Flush(false, GGameUserSettingsIni);
	UE_LOG(LogTemp, Log, TEXT("LedgerTitle: first launch on this PC: full screen at %dx%d, picture %s (the benchmark: CPU %.0f, GPU %.0f), %.1f s"),
		S->GetDesktopResolution().X, S->GetDesktopResolution().Y, *PictureName(),
		S->GetLastCPUBenchmarkResult(), S->GetLastGPUBenchmarkResult(), FPlatformTime::Seconds() - T0);
}

void Show(UWorld* World, bool bInCanContinue)
{
	if (bShown || GEngine == nullptr || GEngine->GameViewport == nullptr || World == nullptr) { return; }
	bCanContinue = bInCanContinue;
	GPendingChoice = EChoice::None;
	GMeasureFrames = 0;
	bMeasured = false;
	bReady = false;
	GChosen = EChoice::None;
	GShownAt = FPlatformTime::Seconds();
	GQuietSince = -1.0;
	GMostPending = 0;
	GContinue.Reset();
	// THE STORY BUTTONS ARE LIVE FROM THE START and the first of them has the
	// keys: taken before the card is ready, the story starts the moment it is
	// (the first version greyed them out, and the keys settled on Picture).
	GNew = MakeButton([]() { return FString(TEXT("New game")); }, []() { return true; }, []() { GChosen = EChoice::NewGame; });
	if (bCanContinue)
	{
		GContinue = MakeButton([]() { return FString(TEXT("Continue")); }, []() { return true; }, []() { GChosen = EChoice::Continue; });
	}
	GPicture = MakeButton([]() { return FString(TEXT("Picture: ")) + PictureName(); }, []() { return true; }, []()
	{
		UGameUserSettings* S = GEngine != nullptr ? GEngine->GetGameUserSettings() : nullptr;
		if (S == nullptr) { return; }
		const int32 L = PictureLevel();
		S->SetOverallScalabilityLevel(L < 0 ? 0 : (L + 1) % 4);
		S->ApplySettings(true);
		UE_LOG(LogTemp, Log, TEXT("LedgerTitle: picture %s"), *PictureName());
		GFrameFrom = FPlatformTime::Seconds() + 1.0;
		GFrameSum = 0.0;
		GFrameCount = 0;
	});
	GQuit = MakeButton([]() { return FString(TEXT("Quit")); }, []() { return true; }, []() { GChosen = EChoice::Quit; });

	TSharedRef<SVerticalBox> Buttons = SNew(SVerticalBox);
	for (const TSharedPtr<SButton>& B : { GContinue, GNew, GPicture, GQuit })
	{
		if (!B.IsValid()) { continue; }
		Buttons->AddSlot().AutoHeight().Padding(FMargin(0.0f, 5.0f))
		[
			SNew(SBox).WidthOverride(340.0f)[ B.ToSharedRef() ]
		];
	}
	FSlateFontInfo TitleFont = FCoreStyle::GetDefaultFontStyle("Bold", 76);
	TitleFont.LetterSpacing = 320;
	static const FSlateColorBrush Shade(FLinearColor(0.02f, 0.02f, 0.03f, 0.55f));
	SAssignNew(GRoot, SBorder)
		.BorderImage(&Shade)
		.Padding(FMargin(110.0f, 0.0f, 40.0f, 0.0f))
		.HAlign(HAlign_Left).VAlign(VAlign_Center)
		[
			SNew(SVerticalBox)
			+ SVerticalBox::Slot().AutoHeight()
			[
				SNew(STextBlock).Text(FText::FromString(TEXT("LEDGER"))).Font(TitleFont)
				.ColorAndOpacity(FSlateColor(kCream))
				.ShadowOffset(FVector2D(2.0f, 2.0f)).ShadowColorAndOpacity(FLinearColor(0.0f, 0.0f, 0.0f, 0.8f))
			]
			+ SVerticalBox::Slot().AutoHeight().Padding(FMargin(4.0f, 0.0f, 0.0f, 44.0f))
			[
				SNew(STextBlock).Text(FText::FromString(TEXT("Britain, 1990"))).Font(FCoreStyle::GetDefaultFontStyle("Regular", 20))
				.ColorAndOpacity(FSlateColor(kDim))
			]
			+ SVerticalBox::Slot().AutoHeight()[ Buttons ]
			+ SVerticalBox::Slot().AutoHeight().Padding(FMargin(4.0f, 30.0f, 0.0f, 0.0f))
			[
				SAssignNew(GStatus, STextBlock).Font(FCoreStyle::GetDefaultFontStyle("Regular", 16))
				.ColorAndOpacity(FSlateColor(kCream))
			]
			+ SVerticalBox::Slot().AutoHeight().Padding(FMargin(4.0f, 8.0f, 0.0f, 0.0f))
			[
				SNew(STextBlock).Text(FText::FromString(TEXT("Up and down to choose, Enter to take it, or click.")))
				.Font(FCoreStyle::GetDefaultFontStyle("Regular", 14)).ColorAndOpacity(FSlateColor(kDim))
			]
		];
	GEngine->GameViewport->AddViewportWidgetContent(GRoot.ToSharedRef(), 200);
	GWorld = World;
	if (APlayerController* PC = World->GetFirstPlayerController())
	{
		FInputModeUIOnly M;
		const TSharedPtr<SButton> First = GContinue.IsValid() ? GContinue : GNew;
		M.SetWidgetToFocus(First);
		M.SetLockMouseToViewportBehavior(EMouseLockMode::DoNotLock);
		GModeWidget = First;
		PC->SetInputMode(M);
		PC->SetShowMouseCursor(true);
		PC->FlushPressedKeys();
	}
	bShown = true;
	UE_LOG(LogTemp, Log, TEXT("LedgerTitle: shown, %s, picture %s"),
		bCanContinue ? TEXT("a saved story to continue") : TEXT("no saved story"), *PictureName());
}

EChoice Tick(UWorld* World, bool bStreetReady)
{
	if (!bShown) { return EChoice::None; }
	// THE FIRST LAUNCH'S MEASURING, once the title has been seen for half a
	// second: run before it, the window stood black for the 3.7 s it takes.
	// Its line goes up first and the measuring waits three frames, so the
	// words are on screen while the window stands still.
	if (!bMeasured && FPlatformTime::Seconds() - GShownAt > 0.5)
	{
		bool bDone = GConfig == nullptr;
		if (GConfig != nullptr) { GConfig->GetBool(TEXT("Ledger"), TEXT("FirstLaunchDone"), bDone, GGameUserSettingsIni); }
		if (bDone) { bMeasured = true; }
		else if (GMeasureFrames++ == 0 && GStatus.IsValid())
		{
			GStatus->SetText(FText::FromString(TEXT("Measuring this PC's graphics card, a few seconds...")));
			return EChoice::None;
		}
		else if (GMeasureFrames < 4) { return EChoice::None; }
		else { bMeasured = true; FirstLaunchSettings(); }
	}
	const double Now = FPlatformTime::Seconds();
	if (GFrameFrom > 0.0 && Now >= GFrameFrom)
	{
		GFrameSum += FApp::GetDeltaTime();
		++GFrameCount;
		if (Now >= GFrameFrom + 3.0)
		{
			UE_LOG(LogTemp, Log, TEXT("LedgerTitle: picture %s costs %.1f ms a frame (%d frames) at %dx%d"), *PictureName(),
				1000.0 * GFrameSum / FMath::Max(1, GFrameCount), GFrameCount,
				GEngine->GameViewport != nullptr && GEngine->GameViewport->Viewport != nullptr ? GEngine->GameViewport->Viewport->GetSizeXY().X : 0,
				GEngine->GameViewport != nullptr && GEngine->GameViewport->Viewport != nullptr ? GEngine->GameViewport->Viewport->GetSizeXY().Y : 0);
			GFrameFrom = -1.0;
		}
	}
	const int32 Pending = PipelineStateCache::GetNumActivePipelinePrecompileTasks() + (int32)FShaderPipelineCache::NumPrecompilesRemaining();
	GMostPending = FMath::Max(GMostPending, Pending);
	if (!bReady)
	{
		if (Pending > 0 || !bStreetReady) { GQuietSince = -1.0; }
		else if (GQuietSince < 0.0) { GQuietSince = Now; }
		const bool bWaitedEnough = bStreetReady && Now - GShownAt > kWaitAtMost;
		if ((GQuietSince >= 0.0 && Now - GQuietSince >= kQuietFor) || bWaitedEnough)
		{
			bReady = true;
			UE_LOG(LogTemp, Log, TEXT("LedgerTitle: ready after %.1f s; at most %d shader pipelines were being prepared at once%s"),
				Now - GShownAt, GMostPending, bWaitedEnough && Pending > 0 ? TEXT(" (let in after two minutes with some still going)") : TEXT(""));
		}
	}
	if (GStatus.IsValid())
	{
		FString Line;
		if (bReady) { Line = TEXT("Ready."); }
		else if (GPendingChoice != EChoice::None) { Line = Pending > 0 ? FString::Printf(TEXT("Starting as soon as the street is ready: %d to go."), Pending) : FString(TEXT("Starting as soon as the street is ready...")); }
		else if (!bStreetReady) { Line = TEXT("Building the street..."); }
		else if (Pending > 0) { Line = FString::Printf(TEXT("Getting the street ready for this PC's graphics card: %d to go."), Pending); }
		else { Line = TEXT("Nearly ready..."); }
		GStatus->SetText(FText::FromString(Line));
	}
	// THE KEYS STAY WITH THE TITLE: Slate cannot focus a widget in the frame it
	// is added (the say box's lesson, 29 September), so focus is won back
	// whenever it is on none of the buttons, and moved to the first story
	// button the moment they open.
	const TSharedPtr<SWidget> Focused = FSlateApplication::Get().GetKeyboardFocusedWidget();
	if (!OneOfOurs(Focused)) { FocusFirst(); }
	// A story chosen early waits here until the card is ready; Quit never waits.
	if (GChosen == EChoice::NewGame || GChosen == EChoice::Continue) { GPendingChoice = GChosen; GChosen = EChoice::None; }
	EChoice C = GChosen;
	GChosen = EChoice::None;
	if (C == EChoice::None && bReady && GPendingChoice != EChoice::None) { C = GPendingChoice; GPendingChoice = EChoice::None; }
	if (C != EChoice::None)
	{
		UE_LOG(LogTemp, Log, TEXT("LedgerTitle: chose %s, picture %s"),
			C == EChoice::NewGame ? TEXT("New game") : C == EChoice::Continue ? TEXT("Continue") : TEXT("Quit"), *PictureName());
	}
	return C;
}

void Hide(UWorld* World)
{
	if (!bShown) { return; }
	if (GEngine != nullptr && GEngine->GameViewport != nullptr && GRoot.IsValid())
	{
		GEngine->GameViewport->RemoveViewportWidgetContent(GRoot.ToSharedRef());
	}
	GRoot.Reset();
	GStatus.Reset();
	GContinue.Reset();
	GNew.Reset();
	GPicture.Reset();
	GQuit.Reset();
	if (World != nullptr)
	{
		if (APlayerController* PC = World->GetFirstPlayerController())
		{
			PC->SetInputMode(FInputModeGameOnly());
			PC->SetShowMouseCursor(false);
			PC->FlushPressedKeys();
		}
	}
	FSlateApplication::Get().SetAllUserFocusToGameViewport();
	bShown = false;
}

bool IsShown() { return bShown; }
}
