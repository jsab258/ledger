#include "TitleScreen.h"

#include "LedgerPaper.h"
#include "LedgerSettings.h"

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
#include "HighResScreenshot.h"
#include "Misc/Paths.h"
#include "PipelineStateCache.h"
#include "ShaderPipelineCache.h"
#include "Styling/CoreStyle.h"
#include "Widgets/Images/SImage.h"
#include "Widgets/Layout/SBorder.h"
#include "Widgets/Layout/SBox.h"
#include "Widgets/SBoxPanel.h"
#include "Widgets/SOverlay.h"
#include "Widgets/Text/STextBlock.h"

namespace LedgerTitle
{
namespace
{
	TSharedPtr<SWidget> GRoot, GLoadRoot;
	TSharedPtr<STextBlock> GStatus;
	TSharedPtr<SPaperChoice> GContinue, GNew, GSettings, GQuit;
	// the loading page's words and its rule (the guide: "never a bar that guesses")
	FString GPhase, GCount;
	float GFill = -1.0f;              // 0 to 1 when the work can be counted, -1 when it cannot
	double GLoadShownAt = 0.0;
	int32 GSavedDay = -1, GSavedHour = 0, GSavedMinute = 0;
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
	// THE FIRST LAUNCH HOLDS SIXTY, 30 September. The engine's benchmark chose
	// Highest on this PC's card, which draws the street at 3440 by 1440 in
	// 26.3 ms, about 38 frames a second, under Jafar's 60 at his monitor's
	// size (the packaged game, measured on the title). So after it, the title
	// times two seconds of frames and steps the picture down until a frame
	// takes at most 15 ms (60 a second with room for the voice on the same
	// card), or Low is reached.
	// THE LADDER, 30 September (the packaged walk): stepping the picture
	// level alone took this card from Highest (26.4 ms at 3440 by 1440)
	// past High (15.1) to Medium (7.9), though the build machine measures
	// Highest drawn at half size and upscaled at 14.3 ms with the voice
	// running. So at each level the street is drawn smaller first (100, 70,
	// then 55 per cent of the screen, upscaled), and the level drops only
	// after; the first rung at or under 16 ms, the 60-a-second line with a
	// small margin, is kept.
	constexpr double kTuneTargetMs = 16.0;
	const float kTuneScales[3] = { 100.0f, 70.0f, 55.0f };
	int32 GTuneLevel = 3, GTuneScale = 0;
	// Measured only once the street is built and the card has nothing left
	// to prepare, and by the median frame of at least ninety: the first try
	// averaged in the benchmark's own stall and the editor's shader work
	// (3025 ms) and stepped down for nothing.
	bool bTuning = false;
	double GTuneFrom = -1.0;
	TArray<float> GTuneFrames;

	// WAITING FOR THE CARD: the pipelines this PC is still preparing, both the
	// engine's own precaching of what is in view and any bundled cache. At
	// most two minutes, so a card that never reports done still lets him in.
	constexpr double kQuietFor = 1.5;
	constexpr double kWaitAtMost = 120.0;

	int32 PictureLevel()
	{
		UGameUserSettings* S = GEngine != nullptr ? GEngine->GetGameUserSettings() : nullptr;
		if (S == nullptr) { return -1; }
		const int32 L = S->GetOverallScalabilityLevel();
		// Drawn smaller than the screen (the first launch's ladder), the
		// levels no longer agree and the overall reads "custom": the light's
		// own level stands for the picture then.
		return L >= 0 ? FMath::Min(L, 3) : FMath::Clamp(S->GetGlobalIlluminationQuality(), 0, 3);
	}

	// The first choice that can be taken, in hand; true once it has the keys.
	bool FocusFirst()
	{
		for (const TSharedPtr<SPaperChoice>& B : { GContinue, GNew, GSettings, GQuit })
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
		return W.IsValid() && (W == GContinue || W == GNew || W == GSettings || W == GQuit);
	}
}

FString PictureName()
{
	FString Name;
	switch (PictureLevel())
	{
	case 0: Name = TEXT("Low"); break;
	case 1: Name = TEXT("Medium"); break;
	case 2: Name = TEXT("High"); break;
	default: Name = TEXT("Highest"); break;
	}
	UGameUserSettings* S = GEngine != nullptr ? GEngine->GetGameUserSettings() : nullptr;
	if (S != nullptr)
	{
		float Norm = 1.0f, Value = 100.0f, Min = 0.0f, Max = 100.0f;
		S->GetResolutionScaleInformationEx(Norm, Value, Min, Max);
		if (Value < 99.0f) { Name += FString::Printf(TEXT(", drawn at %.0f%%"), Value); }
	}
	return Name;
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

FString DayName(int32 Day)
{
	static const TCHAR* Names[7] = { TEXT("Monday"), TEXT("Tuesday"), TEXT("Wednesday"), TEXT("Thursday"), TEXT("Friday"), TEXT("Saturday"), TEXT("Sunday") };
	return Names[((Day % 7) + 7) % 7];
}

FString TimeOfDay(int32 Hour, int32 Minute)
{
	const int32 H12 = Hour % 12 == 0 ? 12 : Hour % 12;
	return FString::Printf(TEXT("%d.%02d %s"), H12, Minute, Hour < 12 ? TEXT("am") : TEXT("pm"));
}

namespace
{
	using namespace LedgerPaper;

	// THE MASTHEAD ROW, shared by the front page and the loading page: the
	// LATE FINAL ear, the game's name in the blackletter, the RAIN LATER ear.
	TSharedRef<SWidget> MastheadRow()
	{
		return SNew(SOverlay)
			+ SOverlay::Slot().HAlign(HAlign_Left).VAlign(VAlign_Top).Padding(FMargin(0.0f, 0.0f, 0.0f, 0.0f))[ Ear(TEXT("Late final"), true) ]
			+ SOverlay::Slot().HAlign(HAlign_Right).VAlign(VAlign_Top)[ Ear(TEXT("Rain later"), false) ]
			+ SOverlay::Slot().HAlign(HAlign_Center).VAlign(VAlign_Top).Padding(FMargin(0.0f, -26.0f, 0.0f, 0.0f))
			[
				SNew(STextBlock).Text(FText::FromString(TEXT("Ledger"))).Font(Font(EFace::Masthead, 124)).ColorAndOpacity(FSlateColor(Ink()))
			];
	}

	// The double rule under the masthead, then the dateline between thin rules.
	TSharedRef<SWidget> Dateline(const FString& A, const FString& B, const FString& C)
	{
		auto Cell = [](const FString& T) { return SNew(STextBlock).Text(FText::FromString(T.ToUpper())).Font(Font(EFace::Old, 24, 260)).ColorAndOpacity(FSlateColor(Ink())); };
		return SNew(SVerticalBox)
			+ SVerticalBox::Slot().AutoHeight()[ Rule(5.0f, Ink()) ]
			+ SVerticalBox::Slot().AutoHeight().Padding(FMargin(0.0f, 3.0f, 0.0f, 0.0f))[ Rule(1.5f, Ink()) ]
			+ SVerticalBox::Slot().AutoHeight().Padding(FMargin(6.0f, 8.0f, 6.0f, 6.0f))
			[
				SNew(SOverlay)
				+ SOverlay::Slot().HAlign(HAlign_Left)[ Cell(A) ]
				+ SOverlay::Slot().HAlign(HAlign_Center)[ Cell(B) ]
				+ SOverlay::Slot().HAlign(HAlign_Right)[ Cell(C) ]
			]
			+ SVerticalBox::Slot().AutoHeight()[ Rule(1.5f, Ink()) ];
	}

	// A thin rule between choices, ink at a third.
	TSharedRef<SWidget> Between() { return Rule(1.5f, FLinearColor(Ink().R, Ink().G, Ink().B, 0.35f)); }

	TSharedRef<SWidget> FrontPage()
	{
		TSharedRef<SVerticalBox> Choices = SNew(SVerticalBox);
		bool bFirst = true;
		for (const TSharedPtr<SPaperChoice>& C : { GContinue, GNew, GSettings, GQuit })
		{
			if (!C.IsValid()) { continue; }
			if (!bFirst) { Choices->AddSlot().AutoHeight()[ Between() ]; }
			Choices->AddSlot().AutoHeight()[ C.ToSharedRef() ];
			bFirst = false;
		}
		// THE TIMES FOLLOW THE LIGHT BEHIND (the design's README): the street stands
		// in daylight behind the title, so its picture and caption are by day.
		const FSlateBrush* Photo = Picture(TEXT("production/art/ui/halftone-title-day.png"), FVector2D(238.0f, 395.0f));
		return SNew(SVerticalBox)
			+ SVerticalBox::Slot().AutoHeight()[ SNew(SBox).HeightOverride(122.0f)[ MastheadRow() ] ]
			+ SVerticalBox::Slot().AutoHeight().Padding(FMargin(0.0f, 0.0f, 0.0f, 0.0f))[ Dateline(TEXT("No. 1"), TEXT("The Hook, Meridian"), TEXT("1990")) ]
			+ SVerticalBox::Slot().FillHeight(1.0f).Padding(FMargin(0.0f, 14.0f, 0.0f, 0.0f))
			[
				SNew(SHorizontalBox)
				+ SHorizontalBox::Slot().FillWidth(1.0f)[ Choices ]
				+ SHorizontalBox::Slot().AutoWidth().Padding(FMargin(26.0f, 0.0f, 24.0f, 0.0f))
				[
					SNew(SBox).WidthOverride(1.5f)[ SNew(SImage).Image(Solid(Ink())) ]
				]
				+ SHorizontalBox::Slot().AutoWidth()
				[
					SNew(SVerticalBox)
					+ SVerticalBox::Slot().AutoHeight()
					[
						SNew(SBox).WidthOverride(238.0f).HeightOverride(395.0f)
						[
							SNew(SImage).Image(Photo != nullptr ? Photo : Solid(Ink()))
						]
					]
					+ SVerticalBox::Slot().AutoHeight().Padding(FMargin(2.0f, 12.0f, 0.0f, 0.0f))
					[
						SNew(STextBlock).Text(FText::FromString(TEXT("Quay Street today."))).Font(Font(EFace::OldItalic, 28)).ColorAndOpacity(FSlateColor(Ink()))
					]
				]
			];
	}

	// THE LOADING PAGE: the same paper, the story's day and time, a headline,
	// the street in halftone; under it the work's own words and a rule that
	// fills only when the work can be counted (the guide's Progress).
	TSharedRef<SWidget> LoadingPage(bool bContinue)
	{
		const FString Day = bContinue && GSavedDay >= 0 ? DayName(GSavedDay) : DayName(0);
		const FString Time = bContinue && GSavedDay >= 0 ? TimeOfDay(GSavedHour, GSavedMinute) : TimeOfDay(9, 0);
		// the street at its hour: by night for a story saved after dark, by day for a new one at 9 am
		const bool bNight = bContinue && GSavedDay >= 0 ? (GSavedHour >= 19 || GSavedHour < 7) : false;
		const FSlateBrush* Photo = Picture(bNight ? TEXT("production/art/ui/halftone-loading.png") : TEXT("production/art/ui/halftone-loading-day.png"), FVector2D(1072.0f, 420.0f));
		TSharedRef<SWidget> Sheet = PaperSheet(
			SNew(SVerticalBox)
			+ SVerticalBox::Slot().AutoHeight()[ SNew(SBox).HeightOverride(122.0f)[ MastheadRow() ] ]
			+ SVerticalBox::Slot().AutoHeight()[ Dateline(Day, Time, TEXT("Quay Street")) ]
			+ SVerticalBox::Slot().AutoHeight().Padding(FMargin(0.0f, 14.0f, 0.0f, 12.0f))
			[
				SNew(STextBlock).Text(FText::FromString(bContinue ? TEXT("Back on Quay Street") : TEXT("Monday morning on Quay Street")))
				.Font(Font(EFace::Franklin800, 54)).ColorAndOpacity(FSlateColor(Ink()))
			]
			+ SVerticalBox::Slot().AutoHeight()
			[
				SNew(SBox).HeightOverride(420.0f)[ SNew(SImage).Image(Photo != nullptr ? Photo : Solid(Ink())) ]
			]
			+ SVerticalBox::Slot().AutoHeight().Padding(FMargin(2.0f, 12.0f, 0.0f, 0.0f))
			[
				SNew(STextBlock).Text(FText::FromString(bContinue ? (bNight ? TEXT("Quay Street tonight, where you left it.") : TEXT("Quay Street, where you left it.")) : TEXT("Quay Street this morning.")))
				.Font(Font(EFace::OldItalic, 28)).ColorAndOpacity(FSlateColor(Ink()))
			],
			FMargin(44.0f, 22.0f, 44.0f, 24.0f));
		return SNew(SOverlay)
			+ SOverlay::Slot()[ SNew(SImage).Image(Solid(FLinearColor(0.0f, 0.0f, 0.0f, 0.72f))) ]
			+ SOverlay::Slot()
			[
				SafeRegion(
					SNew(SVerticalBox)
					+ SVerticalBox::Slot().AutoHeight().Padding(FMargin(0.0f, 70.0f, 0.0f, 0.0f)).HAlign(HAlign_Center)
					[
						SNew(SBox).WidthOverride(1160.0f)[ Sheet ]
					]
					+ SVerticalBox::Slot().AutoHeight().Padding(FMargin(0.0f, 84.0f, 0.0f, 0.0f)).HAlign(HAlign_Center)
					[
						SNew(SBox).WidthOverride(1160.0f)
						[
							SNew(SVerticalBox)
							+ SVerticalBox::Slot().AutoHeight()
							[
								SNew(SHorizontalBox)
								+ SHorizontalBox::Slot().FillWidth(1.0f)
								[
									SNew(STextBlock).Text_Lambda([]() { return FText::FromString(GPhase); }).Font(Font(EFace::Franklin500, 32)).ColorAndOpacity(FSlateColor(OnDark()))
								]
								+ SHorizontalBox::Slot().AutoWidth()
								[
									SNew(STextBlock).Text_Lambda([]() { return FText::FromString(GCount); }).Font(Font(EFace::Franklin500, 32))
									.ColorAndOpacity(FSlateColor(FLinearColor(OnDark().R, OnDark().G, OnDark().B, 0.7f)))
								]
							]
							+ SVerticalBox::Slot().AutoHeight().Padding(FMargin(0.0f, 16.0f, 0.0f, 0.0f))
							[
								SNew(SBox).HeightOverride(5.0f)
								[
									SNew(SOverlay)
									+ SOverlay::Slot()[ SNew(SImage).Image(Solid(FLinearColor(OnDark().R, OnDark().G, OnDark().B, 0.28f))) ]
									+ SOverlay::Slot().HAlign(HAlign_Left)
									[
										// filled to the count; when it cannot be counted, a short piece runs to and fro
										SNew(SBox)
										.WidthOverride_Lambda([]() { return FOptionalSize(GFill >= 0.0f ? 1160.0f * GFill : 150.0f); })
										.Padding_Lambda([]()
										{
											if (GFill >= 0.0f || ReduceMotion()) { return FMargin(0.0f); }
											const double T = FPlatformTime::Seconds() - GLoadShownAt;
											const double X = (0.5 - 0.5 * FMath::Cos(T * 1.6)) * (1160.0 - 150.0);
											return FMargin((float)X, 0.0f, 0.0f, 0.0f);
										})
										[
											SNew(SImage).Image(Solid(OnDark()))
										]
									]
								]
							]
						]
					], HAlign_Fill, VAlign_Top)
			];
	}

	void ShowLoading(bool bContinue)
	{
		if (GLoadRoot.IsValid() || GEngine == nullptr || GEngine->GameViewport == nullptr) { return; }
		GLoadShownAt = FPlatformTime::Seconds();
		GLoadRoot = SNew(SBorder).BorderImage(Solid(FLinearColor::Transparent)).Padding(0.0f)
			// from black in 400 ms (the guide's table)
			.ColorAndOpacity_Lambda([]() { const float A = ReduceMotion() ? 1.0f : FMath::Clamp((float)((FPlatformTime::Seconds() - GLoadShownAt) / 0.4), 0.0f, 1.0f); return FLinearColor(A, A, A, 1.0f); })
			[ LoadingPage(bContinue) ];
		GEngine->GameViewport->AddViewportWidgetContent(GLoadRoot.ToSharedRef(), 210);
		if (GRoot.IsValid()) { GRoot->SetVisibility(EVisibility::Collapsed); }    // the title waits behind, unseen
		UE_LOG(LogTemp, Log, TEXT("LedgerTitle: the loading page, %s"), bContinue ? TEXT("continuing") : TEXT("a new story"));
	}

	void HideLoading()
	{
		if (GLoadRoot.IsValid() && GEngine != nullptr && GEngine->GameViewport != nullptr)
		{
			GEngine->GameViewport->RemoveViewportWidgetContent(GLoadRoot.ToSharedRef());
		}
		GLoadRoot.Reset();
		if (GRoot.IsValid()) { GRoot->SetVisibility(EVisibility::SelfHitTestInvisible); }
	}
}

void Show(UWorld* World, bool bInCanContinue, int32 SavedDay, int32 SavedHour, int32 SavedMinute)
{
	using namespace LedgerPaper;
	if (bShown || GEngine == nullptr || GEngine->GameViewport == nullptr || World == nullptr) { return; }
	bCanContinue = bInCanContinue;
	GSavedDay = SavedDay;
	GSavedHour = SavedHour;
	GSavedMinute = SavedMinute;
	GPendingChoice = EChoice::None;
	GMeasureFrames = 0;
	bMeasured = false;
	bReady = false;
	GChosen = EChoice::None;
	GShownAt = FPlatformTime::Seconds();
	GQuietSince = -1.0;
	GMostPending = 0;
	GContinue.Reset();
	GPhase.Empty();
	GCount.Empty();
	GFill = -1.0f;
	FontsFound();
	// THE STORY CHOICES ARE LIVE FROM THE START and the first of them is in
	// hand: taken before the card is ready, the story starts the moment it is,
	// with the loading page up meanwhile.
	if (bCanContinue)
	{
		const FString When = SavedDay >= 0 ? FString::Printf(TEXT("%s, %s, Quay Street"), *DayName(SavedDay), *TimeOfDay(SavedHour, SavedMinute)) : FString();
		SAssignNew(GContinue, SPaperChoice).Text(FString(TEXT("Continue"))).Note(When).Units(50.0f).RowHeight(104.0f)
			.OnChosen_Lambda([]() { GChosen = EChoice::Continue; });
	}
	SAssignNew(GNew, SPaperChoice).Text(FString(TEXT("New game"))).Units(50.0f).OnChosen_Lambda([]() { GChosen = EChoice::NewGame; });
	SAssignNew(GSettings, SPaperChoice).Text(FString(TEXT("Settings"))).Units(50.0f).OnChosen_Lambda([]() { GChosen = EChoice::Settings; });
	SAssignNew(GQuit, SPaperChoice).Text(FString(TEXT("Quit"))).Units(50.0f).OnChosen_Lambda([]() { GChosen = EChoice::Quit; });

	SAssignNew(GRoot, SBorder).BorderImage(Solid(FLinearColor::Transparent)).Padding(0.0f)
		// in with the menus' 220 ms cross-fade
		.ColorAndOpacity_Lambda([]() { const float A = ReduceMotion() ? 1.0f : FMath::Clamp((float)((FPlatformTime::Seconds() - GShownAt) / 0.22), 0.0f, 1.0f); return FLinearColor(1.0f, 1.0f, 1.0f, A); })
		[
			SNew(SOverlay)
			// the street behind, a little darker at the left where the page lies
			+ SOverlay::Slot()[ SNew(SImage).Image(Solid(FLinearColor(0.0f, 0.0f, 0.0f, 0.22f))) ]
			+ SOverlay::Slot()
			[
				SafeRegion(
					SNew(SVerticalBox)
					+ SVerticalBox::Slot().AutoHeight().Padding(FMargin(120.0f, 74.0f, 0.0f, 0.0f)).HAlign(HAlign_Left)
					[
						SNew(SBox).WidthOverride(800.0f).HeightOverride(680.0f)
						[
							PaperSheet(FrontPage(), FMargin(38.0f, 22.0f, 38.0f, 30.0f))
						]
					]
					+ SVerticalBox::Slot().FillHeight(1.0f)
					+ SVerticalBox::Slot().AutoHeight().Padding(FMargin(120.0f, 0.0f, 120.0f, 52.0f))
					[
						SNew(SHorizontalBox)
						+ SHorizontalBox::Slot().AutoWidth()
						[
							Hints({ MakeTuple(TArray<FString>{ TEXT("↑"), TEXT("↓") }, FString(TEXT("to choose"))),
							        MakeTuple(TArray<FString>{ TEXT("Enter") }, FString(TEXT("to take it"))) })
						]
						+ SHorizontalBox::Slot().FillWidth(1.0f)
						+ SHorizontalBox::Slot().AutoWidth().VAlign(VAlign_Bottom)
						[
							SNew(STextBlock).Text(FText::FromString(TEXT("Build 0.1"))).Font(Font(EFace::Franklin400, 22))
							.ColorAndOpacity(FSlateColor(OnDark()))
						]
					])
			]
		];
	GEngine->GameViewport->AddViewportWidgetContent(GRoot.ToSharedRef(), 200);
	GWorld = World;
	if (APlayerController* PC = World->GetFirstPlayerController())
	{
		FInputModeUIOnly M;
		const TSharedPtr<SPaperChoice> First = GContinue.IsValid() ? GContinue : GNew;
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
	// -TitleShot=<dir> (1 October, the interface as drawn): the front page as the
	// game draws it, then the loading page with sample words, each saved with the
	// interface in it at the window's own size; then the game closes.
	{
		static FString ShotDir;
		static bool bShotRead = false;
		static int32 ShotStep = 0;
		if (!bShotRead) { bShotRead = true; FParse::Value(FCommandLine::Get(), TEXT("TitleShot="), ShotDir); }
		if (!ShotDir.IsEmpty())
		{
			const double Since = FPlatformTime::Seconds() - GShownAt;
			const FIntPoint Size = GEngine->GameViewport != nullptr && GEngine->GameViewport->Viewport != nullptr ? GEngine->GameViewport->Viewport->GetSizeXY() : FIntPoint(0, 0);
			if (ShotStep == 0 && Since > 4.0)
			{
				FScreenshotRequest::RequestScreenshot(FPaths::Combine(ShotDir, FString::Printf(TEXT("title-%d.png"), Size.X)), true, false);
				++ShotStep;
			}
			else if (ShotStep == 1 && Since > 5.0)
			{
				GPhase = TEXT("Starting as soon as the street is ready");
				GCount = TEXT("312 to go");
				GFill = 0.62f;
				ShowLoading(bCanContinue);
				++ShotStep;
			}
			else if (ShotStep == 2 && Since > 6.5)
			{
				FScreenshotRequest::RequestScreenshot(FPaths::Combine(ShotDir, FString::Printf(TEXT("loading-%d.png"), Size.X)), true, false);
				++ShotStep;
			}
			else if (ShotStep == 3 && Since > 7.5)
			{
				HideLoading();
				if (GRoot.IsValid()) { GRoot->SetVisibility(EVisibility::Collapsed); }
				LedgerSettings::Show(World, nullptr);
				++ShotStep;
			}
			else if (ShotStep == 4 && Since > 9.0)
			{
				FScreenshotRequest::RequestScreenshot(FPaths::Combine(ShotDir, FString::Printf(TEXT("settings-%d.png"), Size.X)), true, false);
				++ShotStep;
			}
			else if (ShotStep == 5 && Since > 10.0)
			{
				UE_LOG(LogTemp, Display, TEXT("LedgerTitle: TitleShot done in %s"), *ShotDir);
				FPlatformMisc::RequestExit(false);
				++ShotStep;
			}
			return EChoice::None;
		}
	}
	// THE FIRST LAUNCH'S MEASURING, once the title has been seen for half a
	// second: run before it, the window stood black for the 3.7 s it takes.
	// Its line goes up first and the measuring waits three frames, so the
	// words are on screen while the window stands still.
	if (!bMeasured && FPlatformTime::Seconds() - GShownAt > 0.5)
	{
		bool bDone = GConfig == nullptr;
		if (GConfig != nullptr) { GConfig->GetBool(TEXT("Ledger"), TEXT("FirstLaunchDone"), bDone, GGameUserSettingsIni); }
		if (bDone) { bMeasured = true; }
		else if (GMeasureFrames++ == 0)
		{
			// THE FIRST LAUNCH'S WORK ON THE LOADING PAGE (the guide's first-launch
			// phase, "only on the first run"), the title waiting behind it.
			GPhase = TEXT("Getting the street ready for this PC's graphics card");
			GCount.Empty();
			GFill = -1.0f;
			ShowLoading(false);
			return EChoice::None;
		}
		else if (GMeasureFrames < 4) { return EChoice::None; }
		else
		{
			bMeasured = true;
			FirstLaunchSettings();
			bTuning = true;
			GTuneFrom = -1.0;
			GTuneFrames.Reset();
			GTuneLevel = PictureLevel() < 0 ? 3 : PictureLevel();
			GTuneScale = 0;
			if (UGameUserSettings* S0 = GEngine != nullptr ? GEngine->GetGameUserSettings() : nullptr)
			{
				S0->SetOverallScalabilityLevel(GTuneLevel);
				S0->SetResolutionScaleValueEx(kTuneScales[0]);
				S0->ApplySettings(true);
			}
		}
	}
	if (bTuning)
	{
		const double T = FPlatformTime::Seconds();
		const bool bSettled = bStreetReady && PipelineStateCache::GetNumActivePipelinePrecompileTasks() == 0;
		if (!bSettled) { GTuneFrom = -1.0; GTuneFrames.Reset(); }
		else if (GTuneFrom < 0.0) { GTuneFrom = T + 1.0; }
		else if (T >= GTuneFrom) { GTuneFrames.Add((float)FApp::GetDeltaTime()); }
		if (GTuneFrom > 0.0 && T >= GTuneFrom + 2.0 && GTuneFrames.Num() >= 90)
		{
			GTuneFrames.Sort();
			const double Ms = 1000.0 * GTuneFrames[GTuneFrames.Num() / 2];
			UGameUserSettings* S = GEngine != nullptr ? GEngine->GetGameUserSettings() : nullptr;
			const bool bLast = GTuneLevel == 0 && GTuneScale == 2;
			if (S != nullptr && Ms > kTuneTargetMs && !bLast)
			{
				UE_LOG(LogTemp, Log, TEXT("LedgerTitle: first launch: picture %s takes %.1f ms a frame (the median of %d), over %.0f"),
					*PictureName(), Ms, GTuneFrames.Num(), kTuneTargetMs);
				if (GTuneScale < 2) { ++GTuneScale; } else { --GTuneLevel; GTuneScale = 0; }
				S->SetOverallScalabilityLevel(GTuneLevel);
				S->SetResolutionScaleValueEx(kTuneScales[GTuneScale]);
				S->ApplySettings(true);
				GTuneFrom = T + 1.0;
				GTuneFrames.Reset();
			}
			else
			{
				bTuning = false;
				UE_LOG(LogTemp, Log, TEXT("LedgerTitle: first launch settles on picture %s, at %.1f ms a frame"), *PictureName(), Ms);
			}
		}
		GPhase = TEXT("Finding the picture this PC can keep smooth");
		GCount.Empty();
		GFill = -1.0f;
		GQuietSince = -1.0;
		if (bTuning) { return EChoice::None; }
		HideLoading();
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
	// THE LOADING PAGE'S WORDS AND RULE while a chosen story waits for the
	// street: counted when the card says how much is left, never guessed.
	if (GPendingChoice != EChoice::None && !bReady)
	{
		ShowLoading(GPendingChoice == EChoice::Continue);
		GPhase = TEXT("Starting as soon as the street is ready");
		if (!bStreetReady) { GPhase = TEXT("Building the street"); GCount.Empty(); GFill = -1.0f; }
		else if (Pending > 0)
		{
			GCount = FString::Printf(TEXT("%d to go"), Pending);
			GFill = GMostPending > 0 ? FMath::Clamp(1.0f - (float)Pending / (float)GMostPending, 0.0f, 1.0f) : -1.0f;
		}
		else { GCount.Empty(); GFill = 1.0f; }
	}
	// THE KEYS STAY WITH THE TITLE: Slate cannot focus a widget in the frame it
	// is added (the say box's lesson, 29 September), so focus is won back
	// whenever it is on none of the buttons, and moved to the first story
	// button the moment they open.
	const TSharedPtr<SWidget> Focused = FSlateApplication::Get().GetKeyboardFocusedWidget();
	if (!OneOfOurs(Focused) && !LedgerSettings::IsShown()) { FocusFirst(); }
	// A story chosen early waits here until the card is ready; Quit never waits.
	if (GChosen == EChoice::NewGame || GChosen == EChoice::Continue) { GPendingChoice = GChosen; GChosen = EChoice::None; }
	if (GChosen == EChoice::Settings)
	{
		// the settings page opens over the title; Esc brings him back to Settings in hand
		GChosen = EChoice::None;
		if (GRoot.IsValid()) { GRoot->SetVisibility(EVisibility::Collapsed); }   // the page alone over the street, its keys not under the title's
		LedgerSettings::Show(World, []()
		{
			if (GRoot.IsValid()) { GRoot->SetVisibility(EVisibility::SelfHitTestInvisible); }
			if (GSettings.IsValid()) { FSlateApplication::Get().SetKeyboardFocus(GSettings, EFocusCause::SetDirectly); GModeWidget.Reset(); }
		});
	}
	EChoice C = GChosen;
	GChosen = EChoice::None;
	if (C == EChoice::None && bReady && GPendingChoice != EChoice::None) { C = GPendingChoice; GPendingChoice = EChoice::None; }
	if (C != EChoice::None)
	{
		UE_LOG(LogTemp, Log, TEXT("LedgerTitle: chose %s, picture %s"),
			C == EChoice::NewGame ? TEXT("New game") : C == EChoice::Continue ? TEXT("Continue") : C == EChoice::Settings ? TEXT("Settings") : TEXT("Quit"), *PictureName());
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
	HideLoading();
	GStatus.Reset();
	GContinue.Reset();
	GNew.Reset();
	GSettings.Reset();
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
