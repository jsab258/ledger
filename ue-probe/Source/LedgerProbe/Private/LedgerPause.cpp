#include "LedgerPause.h"

#include "LedgerPaper.h"
#include "LedgerSettings.h"
#include "TitleScreen.h"

#include "Engine/Engine.h"
#include "Engine/GameViewportClient.h"
#include "Engine/World.h"
#include "Framework/Application/SlateApplication.h"
#include "GameFramework/PlayerController.h"
#include "Widgets/Images/SImage.h"
#include "Widgets/Layout/SBackgroundBlur.h"
#include "Widgets/Layout/SBorder.h"
#include "Widgets/Layout/SBox.h"
#include "Widgets/SBoxPanel.h"
#include "Widgets/SOverlay.h"
#include "Widgets/Text/STextBlock.h"

using namespace LedgerPaper;

namespace LedgerPause
{
namespace
{
	TSharedPtr<SWidget> GRoot;
	TSharedPtr<SBox> GSheetHolder, GHintsHolder;
	TSharedPtr<SPaperChoice> GFirst;
	TArray<TSharedPtr<SPaperChoice>> GChoices;
	TWeakObjectPtr<UWorld> GWorld;
	FWhen GWhen;
	EAction GTaken = EAction::None;
	double GShownAt = 0.0;
	enum class EPage : uint8 { Menu, ConfirmTitle, ConfirmQuit };
	EPage GPage = EPage::Menu;

	TSharedRef<SWidget> Between() { return Rule(1.5f, FLinearColor(Ink().R, Ink().G, Ink().B, 0.35f)); }

	void Focus(const TSharedPtr<SPaperChoice>& C)
	{
		if (!C.IsValid()) { return; }
		FSlateApplication::Get().SetKeyboardFocus(C, EFocusCause::SetDirectly);
		if (UWorld* W = GWorld.Get())
		{
			if (APlayerController* PC = W->GetFirstPlayerController())
			{
				FInputModeUIOnly M;
				M.SetWidgetToFocus(C);
				M.SetLockMouseToViewportBehavior(EMouseLockMode::DoNotLock);
				PC->SetInputMode(M);
				PC->SetShowMouseCursor(true);
			}
		}
	}

	TSharedPtr<SPaperChoice> Choice(const FString& Text, TFunction<void()> Do, bool bEnabled = true, const FString& Why = FString())
	{
		TSharedPtr<SPaperChoice> C;
		SAssignNew(C, SPaperChoice).Text(Text).Note(Why).Units(48.0f).RowHeight(78.0f).Enabled(bEnabled)
			.OnChosen_Lambda([Do]() { Do(); });
		GChoices.Add(C);
		return C;
	}

	void Build();

	// THE STOP PRESS BOX: the band, the story's day and hour, the choices, when it was last saved.
	TSharedRef<SWidget> Menu()
	{
		GChoices.Reset();
		GFirst = Choice(TEXT("Back to the street"), []() { GTaken = EAction::Resume; });
		Choice(TEXT("The Ledger"), []() {}, false, TEXT("Tom's notebook is not in this build yet."));
		Choice(TEXT("Settings"), []()
		{
			if (GRoot.IsValid()) { GRoot->SetVisibility(EVisibility::Collapsed); }
			LedgerSettings::Show(GWorld.Get(), []()
			{
				if (GRoot.IsValid()) { GRoot->SetVisibility(EVisibility::SelfHitTestInvisible); }
				if (GChoices.IsValidIndex(2)) { Focus(GChoices[2]); }
			});
		});
		Choice(TEXT("Quit to the title"), []() { GPage = EPage::ConfirmTitle; Build(); });
		Choice(TEXT("Quit the game"), []() { GPage = EPage::ConfirmQuit; Build(); });
		TSharedRef<SVerticalBox> Rows = SNew(SVerticalBox);
		for (int32 I = 0; I < GChoices.Num(); ++I)
		{
			if (I > 0) { Rows->AddSlot().AutoHeight()[ Between() ]; }
			Rows->AddSlot().AutoHeight()[ GChoices[I].ToSharedRef() ];
		}
		Rows->AddSlot().AutoHeight()[ Between() ];
		const FString Saved = GWhen.SavedHour >= 0
			? FString::Printf(TEXT("Last saved at %s, on Quay Street."), *LedgerTitle::TimeOfDay(GWhen.SavedHour, GWhen.SavedMinute))
			: FString(TEXT("Not saved yet today."));
		auto Cell = [](const FString& T) { return SNew(STextBlock).Text(FText::FromString(T.ToUpper())).Font(Font(EFace::Old, 24, 260)).ColorAndOpacity(FSlateColor(Ink())); };
		return SNew(SVerticalBox)
			+ SVerticalBox::Slot().AutoHeight()[ Band(TEXT("Stop press"), 58, FMargin(44.0f, 12.0f, 44.0f, 6.0f)) ]
			+ SVerticalBox::Slot().AutoHeight().Padding(FMargin(44.0f, 10.0f, 44.0f, 0.0f))
			[
				SNew(SVerticalBox)
				+ SVerticalBox::Slot().AutoHeight()[ Rule(1.5f, Ink()) ]
				+ SVerticalBox::Slot().AutoHeight().Padding(FMargin(6.0f, 8.0f, 6.0f, 6.0f))
				[
					SNew(SOverlay)
					+ SOverlay::Slot().HAlign(HAlign_Left)[ Cell(LedgerTitle::DayName(GWhen.Day)) ]
					+ SOverlay::Slot().HAlign(HAlign_Center)[ Cell(LedgerTitle::TimeOfDay(GWhen.Hour, GWhen.Minute)) ]
					+ SOverlay::Slot().HAlign(HAlign_Right)[ Cell(TEXT("Quay Street")) ]
				]
				+ SVerticalBox::Slot().AutoHeight()[ Rule(1.5f, Ink()) ]
				+ SVerticalBox::Slot().AutoHeight()[ Rows ]
				+ SVerticalBox::Slot().AutoHeight().Padding(FMargin(2.0f, 16.0f, 0.0f, 22.0f))
				[
					SNew(STextBlock).Text(FText::FromString(Saved)).Font(Font(EFace::OldItalic, 28)).ColorAndOpacity(FSlateColor(Grey()))
				]
			];
	}

	// A CONFIRMATION: the question on the red band, a line saying what is kept,
	// and the safe choice in hand first ("Stay on the street").
	TSharedRef<SWidget> Confirm(const FString& Question, const FString& Kept, const FString& Go, EAction Action)
	{
		GChoices.Reset();
		GFirst = Choice(TEXT("Stay on the street"), []() { GPage = EPage::Menu; Build(); });
		Choice(Go, [Action]() { GTaken = Action; });
		return SNew(SVerticalBox)
			+ SVerticalBox::Slot().AutoHeight()[ Band(Question, 52, FMargin(44.0f, 12.0f, 44.0f, 6.0f)) ]
			+ SVerticalBox::Slot().AutoHeight().Padding(FMargin(44.0f, 18.0f, 44.0f, 8.0f))
			[
				SNew(STextBlock).Text(FText::FromString(Kept)).AutoWrapText(true).Font(Font(EFace::Franklin450, 30)).ColorAndOpacity(FSlateColor(Ink()))
			]
			+ SVerticalBox::Slot().AutoHeight().Padding(FMargin(44.0f, 4.0f, 44.0f, 24.0f))
			[
				SNew(SVerticalBox)
				+ SVerticalBox::Slot().AutoHeight()[ Between() ]
				+ SVerticalBox::Slot().AutoHeight()[ GChoices[0].ToSharedRef() ]
				+ SVerticalBox::Slot().AutoHeight()[ Between() ]
				+ SVerticalBox::Slot().AutoHeight()[ GChoices[1].ToSharedRef() ]
				+ SVerticalBox::Slot().AutoHeight()[ Between() ]
			];
	}

	void Build()
	{
		if (!GSheetHolder.IsValid()) { return; }
		const FString Kept = GWhen.SavedHour >= 0
			? FString::Printf(TEXT("Your story is kept as it was saved at %s."), *LedgerTitle::TimeOfDay(GWhen.SavedHour, GWhen.SavedMinute))
			: FString(TEXT("Your story is kept as it was last saved."));
		TSharedRef<SWidget> Sheet =
			GPage == EPage::ConfirmQuit ? Confirm(TEXT("Quit the game?"), Kept, TEXT("Quit the game"), EAction::QuitGame) :
			GPage == EPage::ConfirmTitle ? Confirm(TEXT("Back to the title?"), Kept, TEXT("Quit to the title"), EAction::QuitToTitle) :
			Menu();
		GSheetHolder->SetContent(PaperSheet(Sheet, FMargin(0.0f)));
		GHintsHolder->SetContent(Hints({ MakeTuple(TArray<FString>{ TEXT("↑"), TEXT("↓") }, FString(TEXT("choose"))),
		                                 MakeTuple(TArray<FString>{ TEXT("Enter") }, FString(TEXT("take it"))),
		                                 MakeTuple(TArray<FString>{ TEXT("Esc") }, FString(GPage == EPage::Menu ? TEXT("back to the street") : TEXT("stay"))) }));
		Focus(GFirst);
	}

	// Esc on the page: back to the street, or out of a confirmation.
	class SPauseKeys : public SCompoundWidget
	{
	public:
		SLATE_BEGIN_ARGS(SPauseKeys) {}
			SLATE_DEFAULT_SLOT(FArguments, Content)
		SLATE_END_ARGS()
		void Construct(const FArguments& InArgs) { ChildSlot[ InArgs._Content.Widget ]; }
		virtual FReply OnKeyDown(const FGeometry& G, const FKeyEvent& E) override
		{
			if (E.GetKey() == EKeys::Escape || E.GetKey() == EKeys::Gamepad_FaceButton_Right || E.GetKey() == EKeys::Gamepad_Special_Right)
			{
				if (GPage != EPage::Menu) { GPage = EPage::Menu; Build(); }
				else { GTaken = EAction::Resume; }
				return FReply::Handled();
			}
			// Q QUITS FROM THE PAUSE, as it did before the page took the input to itself
			// (2 October: the route walk's "Esc, then Q" failed; the page is menu-only
			// input, so the game's own Q binding never heard the key).
			if (E.GetKey() == EKeys::Q && GPage == EPage::Menu) { GTaken = EAction::QuitGame; return FReply::Handled(); }
			return FReply::Unhandled();
		}
	};
}

void Show(UWorld* World, const FWhen& When)
{
	if (GRoot.IsValid() || GEngine == nullptr || GEngine->GameViewport == nullptr) { return; }
	LedgerPaper::UiSound(TEXT("rustle"));
	GWorld = World;
	GWhen = When;
	GTaken = EAction::None;
	GPage = EPage::Menu;
	GShownAt = FPlatformTime::Seconds();
	SAssignNew(GRoot, SPauseKeys)
	[
		SNew(SBorder).BorderImage(Solid(FLinearColor::Transparent)).Padding(0.0f)
		.ColorAndOpacity_Lambda([]() { const float A = ReduceMotion() ? 1.0f : FMath::Clamp((float)((FPlatformTime::Seconds() - GShownAt) / 0.22), 0.0f, 1.0f); return FLinearColor(1.0f, 1.0f, 1.0f, A); })
		[
			SNew(SOverlay)
			// the street held still behind, blurred, as the page is drawn
			+ SOverlay::Slot()[ SNew(SBackgroundBlur).BlurStrength(9.0f)[ SNew(SImage).Image(Solid(FLinearColor(0.0f, 0.0f, 0.0f, 0.2f))) ] ]
			+ SOverlay::Slot()
			[
				SafeRegion(
					SNew(SVerticalBox)
					+ SVerticalBox::Slot().AutoHeight().Padding(FMargin(0.0f, 140.0f, 0.0f, 0.0f)).HAlign(HAlign_Center)
					[
						SAssignNew(GSheetHolder, SBox).WidthOverride(820.0f)
					]
					+ SVerticalBox::Slot().AutoHeight().Padding(FMargin(0.0f, 128.0f, 0.0f, 0.0f)).HAlign(HAlign_Center)
					[
						SAssignNew(GHintsHolder, SBox)
					])
			]
		]
	];
	GEngine->GameViewport->AddViewportWidgetContent(GRoot.ToSharedRef(), 215);
	Build();
	UE_LOG(LogTemp, Log, TEXT("LedgerPause: shown at %s"), *LedgerTitle::TimeOfDay(When.Hour, When.Minute));
}

EAction Tick()
{
	if (!GRoot.IsValid()) { return EAction::None; }
	// the keys stay on the page (Slate cannot focus a widget the frame it is added)
	if (!LedgerSettings::IsShown())
	{
		const TSharedPtr<SWidget> F = FSlateApplication::Get().GetKeyboardFocusedWidget();
		bool bOurs = false;
		for (const TSharedPtr<SPaperChoice>& C : GChoices) { bOurs = bOurs || F == C; }
		if (!bOurs) { Focus(GFirst); }
	}
	const EAction A = GTaken;
	GTaken = EAction::None;
	return A;
}

void Hide()
{
	if (!GRoot.IsValid()) { return; }
	LedgerSettings::Hide();
	if (GEngine != nullptr && GEngine->GameViewport != nullptr) { GEngine->GameViewport->RemoveViewportWidgetContent(GRoot.ToSharedRef()); }
	GRoot.Reset();
	GSheetHolder.Reset();
	GHintsHolder.Reset();
	GChoices.Reset();
	GFirst.Reset();
	if (UWorld* W = GWorld.Get())
	{
		if (APlayerController* PC = W->GetFirstPlayerController())
		{
			PC->SetInputMode(FInputModeGameOnly());
			PC->SetShowMouseCursor(false);
			PC->FlushPressedKeys();
		}
	}
	FSlateApplication::Get().SetAllUserFocusToGameViewport();
	UE_LOG(LogTemp, Log, TEXT("LedgerPause: closed"));
}

bool IsShown() { return GRoot.IsValid(); }
}
