#include "LedgerCredits.h"

#include "LedgerPaper.h"
#include "Dom/JsonObject.h"
#include "Engine/Engine.h"
#include "Engine/GameViewportClient.h"
#include "Framework/Application/SlateApplication.h"
#include "Misc/FileHelper.h"
#include "Misc/Paths.h"
#include "Serialization/JsonReader.h"
#include "Serialization/JsonSerializer.h"
#include "Widgets/Images/SImage.h"
#include "Widgets/Layout/SBorder.h"
#include "Widgets/Layout/SBox.h"
#include "Widgets/Layout/SScrollBox.h"
#include "Widgets/SBoxPanel.h"
#include "Widgets/SCompoundWidget.h"
#include "Widgets/SOverlay.h"
#include "Widgets/Text/STextBlock.h"

namespace LedgerCredits
{
namespace
{
	TSharedPtr<SWidget> GRoot;
	TSharedPtr<SScrollBox> GScroll;
	TSharedPtr<SWidget> GKeys;
	TFunction<void()> GOnClosed;

	// The page holds the keys: up and down scroll, Esc or a pad's B goes back.
	class SCreditsKeys : public SCompoundWidget
	{
	public:
		SLATE_BEGIN_ARGS(SCreditsKeys) {}
			SLATE_DEFAULT_SLOT(FArguments, Content)
		SLATE_END_ARGS()
		void Construct(const FArguments& InArgs) { ChildSlot[ InArgs._Content.Widget ]; }
		virtual bool SupportsKeyboardFocus() const override { return true; }
		virtual const FSlateBrush* GetFocusBrush() const override { return nullptr; }
		virtual FReply OnKeyDown(const FGeometry& G, const FKeyEvent& E) override
		{
			const FKey K = E.GetKey();
			if (K == EKeys::Escape || K == EKeys::Gamepad_FaceButton_Right || K == EKeys::Enter || K == EKeys::Gamepad_FaceButton_Bottom)
			{
				Hide();
				return FReply::Handled();
			}
			if (GScroll.IsValid())
			{
				const float Step = 80.0f;
				if (K == EKeys::Down || K == EKeys::Gamepad_DPad_Down || K == EKeys::Gamepad_LeftStick_Down || K == EKeys::PageDown)
				{
					GScroll->SetScrollOffset(GScroll->GetScrollOffset() + (K == EKeys::PageDown ? 6.0f * Step : Step));
					return FReply::Handled();
				}
				if (K == EKeys::Up || K == EKeys::Gamepad_DPad_Up || K == EKeys::Gamepad_LeftStick_Up || K == EKeys::PageUp)
				{
					GScroll->SetScrollOffset(FMath::Max(0.0f, GScroll->GetScrollOffset() - (K == EKeys::PageUp ? 6.0f * Step : Step)));
					return FReply::Handled();
				}
			}
			return FReply::Handled();
		}
	};

	// The sections from production/specs/credits.json: each a head and its lines.
	TArray<TPair<FString, TArray<FString>>> ReadSections()
	{
		TArray<TPair<FString, TArray<FString>>> Out;
		FString Text;
		const FString Path = FPaths::Combine(LedgerPaper::Root(), TEXT("production/specs/credits.json"));
		TSharedPtr<FJsonObject> Root;
		const TArray<TSharedPtr<FJsonValue>>* List = nullptr;
		if (!FFileHelper::LoadFileToString(Text, *Path)) { UE_LOG(LogTemp, Display, TEXT("LedgerCredits: no credits file at %s"), *Path); return Out; }
		const TSharedRef<TJsonReader<>> R = TJsonReaderFactory<>::Create(Text);
		if (!FJsonSerializer::Deserialize(R, Root) || !Root.IsValid() || !Root->TryGetArrayField(TEXT("sections"), List)) { return Out; }
		for (const TSharedPtr<FJsonValue>& V : *List)
		{
			const TSharedPtr<FJsonObject> S = V->AsObject();
			if (!S.IsValid()) { continue; }
			TArray<FString> Lines;
			const TArray<TSharedPtr<FJsonValue>>* Ls = nullptr;
			if (S->TryGetArrayField(TEXT("lines"), Ls)) { for (const TSharedPtr<FJsonValue>& L : *Ls) { Lines.Add(L->AsString()); } }
			Out.Add(TPair<FString, TArray<FString>>(S->GetStringField(TEXT("head")), Lines));
		}
		return Out;
	}
}

void Show(UWorld* World, TFunction<void()> OnClosed)
{
	using namespace LedgerPaper;
	if (GRoot.IsValid() || GEngine == nullptr || GEngine->GameViewport == nullptr) { return; }
	UiSound(TEXT("rustle"));
	GOnClosed = MoveTemp(OnClosed);
	TSharedRef<SVerticalBox> Body = SNew(SVerticalBox);
	bool bFirst = true;
	for (const TPair<FString, TArray<FString>>& S : ReadSections())
	{
		Body->AddSlot().AutoHeight().Padding(FMargin(0.0f, bFirst ? 0.0f : 26.0f, 0.0f, 6.0f))
		[
			SNew(STextBlock).Text(FText::FromString(S.Key)).TransformPolicy(ETextTransformPolicy::ToUpper)
			.Font(Font(EFace::League, 34, 40)).ColorAndOpacity(FSlateColor(Ink()))
		];
		Body->AddSlot().AutoHeight().Padding(FMargin(0.0f, 0.0f, 0.0f, 8.0f))[ Rule(1.5f, Ink()) ];
		for (const FString& L : S.Value)
		{
			Body->AddSlot().AutoHeight().Padding(FMargin(0.0f, 2.0f, 0.0f, 4.0f))
			[
				SNew(STextBlock).Text(FText::FromString(L)).AutoWrapText(true).LineHeightPercentage(1.1f)
				.Font(Font(EFace::Franklin450, 30)).ColorAndOpacity(FSlateColor(Ink()))
			];
		}
		bFirst = false;
	}
	SAssignNew(GRoot, SOverlay)
		+ SOverlay::Slot()[ SNew(SImage).Image(Solid(FLinearColor(0.0f, 0.0f, 0.0f, 0.55f))) ]
		+ SOverlay::Slot()
		[
			SafeRegion(
				SNew(SBox).Padding(FMargin(260.0f, 70.0f, 260.0f, 70.0f))
				[
					SAssignNew(GKeys, SCreditsKeys)
					[
						SNew(SVerticalBox)
						+ SVerticalBox::Slot().FillHeight(1.0f)
						[
							PaperSheet(
								SNew(SVerticalBox)
								+ SVerticalBox::Slot().AutoHeight().Padding(FMargin(0.0f, 0.0f, 0.0f, 18.0f))
								[
									Band(TEXT("CREDITS"), 44.0f, FMargin(18.0f, 4.0f, 18.0f, 4.0f))
								]
								+ SVerticalBox::Slot().FillHeight(1.0f)
								[
									SAssignNew(GScroll, SScrollBox) + SScrollBox::Slot()[ Body ]
								],
								FMargin(40.0f, 30.0f, 40.0f, 30.0f))
						]
						+ SVerticalBox::Slot().AutoHeight().Padding(FMargin(0.0f, 14.0f, 0.0f, 0.0f))
						[
							PadInUse()
							? Hints({ MakeTuple(TArray<FString>{ TEXT("pad:+") }, FString(TEXT("read on"))), MakeTuple(TArray<FString>{ TEXT("pad:B") }, FString(TEXT("back"))) })
							: Hints({ MakeTuple(TArray<FString>{ TEXT("\x2191"), TEXT("\x2193") }, FString(TEXT("read on"))), MakeTuple(TArray<FString>{ TEXT("Esc") }, FString(TEXT("back"))) })
						]
					]
				])
		];
	GEngine->GameViewport->AddViewportWidgetContent(GRoot.ToSharedRef(), 220);
	FSlateApplication::Get().SetKeyboardFocus(GKeys, EFocusCause::SetDirectly);
	UE_LOG(LogTemp, Display, TEXT("LedgerCredits: shown"));
}

void Hide()
{
	if (!GRoot.IsValid()) { return; }
	if (GEngine != nullptr && GEngine->GameViewport != nullptr) { GEngine->GameViewport->RemoveViewportWidgetContent(GRoot.ToSharedRef()); }
	GRoot.Reset();
	GScroll.Reset();
	GKeys.Reset();
	TFunction<void()> Done = MoveTemp(GOnClosed);
	GOnClosed = nullptr;
	if (Done) { Done(); }
}

bool IsShown() { return GRoot.IsValid(); }
}
