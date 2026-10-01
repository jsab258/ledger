#include "LedgerPaper.h"

#include "Brushes/SlateBorderBrush.h"
#include "Brushes/SlateColorBrush.h"
#include "Brushes/SlateImageBrush.h"
#include "Brushes/SlateRoundedBoxBrush.h"
#include "Engine/Texture2D.h"
#include "Fonts/CompositeFont.h"
#include "Framework/Application/SlateApplication.h"
#include "HAL/FileManager.h"
#include "HAL/PlatformTime.h"
#include "ImageUtils.h"
#include "Misc/CommandLine.h"
#include "Misc/Paths.h"
#include "Styling/CoreStyle.h"
#include "Widgets/Images/SImage.h"
#include "Widgets/Layout/SBorder.h"
#include "Widgets/Layout/SBox.h"
#include "Widgets/SBoxPanel.h"
#include "Widgets/SOverlay.h"
#include "Widgets/Text/STextBlock.h"
#include "Components/AudioComponent.h"
#include "Engine/Engine.h"
#include "Engine/GameViewportClient.h"
#include "Kismet/GameplayStatics.h"
#include "LedgerSettings.h"
#include "Misc/FileHelper.h"
#include "Sound/SoundWaveProcedural.h"

namespace LedgerPaper
{
namespace
{
	float GBacking = 0.8f;
	bool bFontsLooked = false, bFontsFound = false;
	FString GRoot;
	// HELD FOR THE WHOLE RUN AND NEVER TORN DOWN: a font or a brush released as
	// the program ends, after the engine and Slate are gone, is a crash on
	// quitting. These live on the heap and the process takes them with it.
	TMap<int32, TSharedPtr<FStandaloneCompositeFont>>& GFonts = *new TMap<int32, TSharedPtr<FStandaloneCompositeFont>>();
	TMap<uint32, TSharedPtr<FSlateBrush>>& GSolids = *new TMap<uint32, TSharedPtr<FSlateBrush>>();
	TMap<uint32, TSharedPtr<FSlateBrush>>& GRuled = *new TMap<uint32, TSharedPtr<FSlateBrush>>();
	TSharedPtr<FSlateBrush>& GSheet = *new TSharedPtr<FSlateBrush>();
	TSharedPtr<FSlateBrush>& GSheetEdge = *new TSharedPtr<FSlateBrush>();

	FLinearColor Hex(const TCHAR* H) { return FLinearColor(FColor::FromHex(H)); }

	const TCHAR* FileOf(EFace F)
	{
		switch (F)
		{
		case EFace::Franklin400: return TEXT("LibreFranklin-400.ttf");
		case EFace::Franklin450: return TEXT("LibreFranklin-450.ttf");
		case EFace::Franklin500: return TEXT("LibreFranklin-500.ttf");
		case EFace::Franklin600: return TEXT("LibreFranklin-600.ttf");
		case EFace::Franklin700: return TEXT("LibreFranklin-700.ttf");
		case EFace::Franklin800: return TEXT("LibreFranklin-800.ttf");
		case EFace::FranklinItalic: return TEXT("LibreFranklin-Italic-400.ttf");
		case EFace::League: return TEXT("LeagueGothic-Regular.ttf");
		case EFace::Masthead: return TEXT("UnifrakturMaguntia-Book.ttf");
		case EFace::Old: return TEXT("OldStandard-Regular.ttf");
		default: return TEXT("OldStandard-Italic.ttf");
		}
	}

	UTexture2D* LoadPicture(const FString& Rel)
	{
		const FString Path = FPaths::Combine(Root(), Rel);
		if (IFileManager::Get().FileSize(*Path) <= 0) { return nullptr; }
		UTexture2D* T = FImageUtils::ImportFileAsTexture2D(Path);
		if (T != nullptr) { T->AddToRoot(); }
		return T;
	}
}

FLinearColor Newsprint() { return Hex(TEXT("E8E3D6")); }
FLinearColor Ink() { return Hex(TEXT("1E1E1D")); }
FLinearColor Red() { return Hex(TEXT("B4191F")); }
FLinearColor Grey() { return Hex(TEXT("4F4C46")); }
FLinearColor Unavailable() { return Hex(TEXT("77726A")); }
FLinearColor OnDark() { return Hex(TEXT("F1EDE3")); }
FLinearColor Backing() { FLinearColor C = Hex(TEXT("10100F")); C.A = GBacking; return C; }
void SetBackingStrength(float A) { GBacking = FMath::Clamp(A, 0.0f, 1.0f); }
float BackingStrength() { return GBacking; }

FString Root()
{
	if (!GRoot.IsEmpty()) { return GRoot; }
	TArray<FString> Cands;
	FString Repo;
	if (FParse::Value(FCommandLine::Get(), TEXT("LedgerRepo="), Repo) && !Repo.IsEmpty()) { Cands.Add(Repo); }
	Cands.Add(FPaths::Combine(FPaths::ProjectDir(), TEXT("..")));
	Cands.Add(FPaths::Combine(FPaths::ProjectContentDir(), TEXT("LedgerData")));
	for (FString C : Cands)
	{
		C = FPaths::ConvertRelativePathToFull(C);
		FPaths::CollapseRelativeDirectories(C);
		if (IFileManager::Get().FileSize(*FPaths::Combine(C, TEXT("production/fonts/evening-paper/LibreFranklin-450.ttf"))) > 0)
		{
			GRoot = C;
			return GRoot;
		}
	}
	return FString();
}

bool FontsFound()
{
	if (!bFontsLooked)
	{
		bFontsLooked = true;
		bFontsFound = !Root().IsEmpty();
		UE_LOG(LogTemp, Log, TEXT("LedgerPaper: the evening paper's fonts %s"),
			bFontsFound ? *FString::Printf(TEXT("from %s"), *FPaths::Combine(Root(), TEXT("production/fonts/evening-paper")))
			: TEXT("not found (-LedgerRepo, the checkout, Content/LedgerData): the engine's own face stands in"));
	}
	return bFontsFound;
}

FSlateFontInfo Font(EFace Face, float Units, int32 LetterSpacing)
{
	const float Size = Units * 72.0f / (float)FontConstants::RenderDPI;
	if (!FontsFound())
	{
		const bool bBold = Face == EFace::Franklin700 || Face == EFace::Franklin800 || Face == EFace::League || Face == EFace::Masthead;
		FSlateFontInfo F = FCoreStyle::GetDefaultFontStyle(bBold ? "Bold" : "Regular", FMath::RoundToInt(Size));
		F.LetterSpacing = LetterSpacing;
		return F;
	}
	TSharedPtr<FStandaloneCompositeFont>& Cf = GFonts.FindOrAdd((int32)Face);
	if (!Cf.IsValid())
	{
		const FString Path = FPaths::Combine(Root(), TEXT("production/fonts/evening-paper"), FileOf(Face));
		Cf = MakeShared<FStandaloneCompositeFont>(FName(FileOf(Face)), Path, EFontHinting::Default, EFontLoadingPolicy::LazyLoad);
	}
	FSlateFontInfo F(StaticCastSharedPtr<const FCompositeFont>(Cf), Size);
	F.LetterSpacing = LetterSpacing;
	return F;
}

const FSlateBrush* Sheet()
{
	if (!GSheet.IsValid())
	{
		if (UTexture2D* T = LoadPicture(TEXT("production/art/ui/newsprint.png")))
		{
			GSheet = MakeShared<FSlateImageBrush>(T, FVector2D(512.0f, 512.0f), FLinearColor::White, ESlateBrushTileType::Both);
		}
		else
		{
			GSheet = MakeShared<FSlateColorBrush>(Newsprint());
		}
	}
	return GSheet.Get();
}

const FSlateBrush* SheetEdge()
{
	if (!GSheetEdge.IsValid())
	{
		if (UTexture2D* T = LoadPicture(TEXT("production/art/ui/newsprint-edge.png")))
		{
			// the yellowing: the picture's grey, warmed, at its own alpha
			GSheetEdge = MakeShared<FSlateImageBrush>(T, FVector2D(256.0f, 256.0f), FLinearColor(0.85f, 0.62f, 0.30f, 1.0f));
		}
		else
		{
			GSheetEdge = MakeShared<FSlateColorBrush>(FLinearColor::Transparent);
		}
	}
	return GSheetEdge.Get();
}

const FSlateBrush* Solid(const FLinearColor& C)
{
	const uint32 K = GetTypeHash(C);
	TSharedPtr<FSlateBrush>& B = GSolids.FindOrAdd(K);
	if (!B.IsValid()) { B = MakeShared<FSlateColorBrush>(C); }
	return B.Get();
}

const FSlateBrush* Ruled(const FLinearColor& C, float Thickness)
{
	const uint32 K = HashCombine(GetTypeHash(C), GetTypeHash(Thickness));
	TSharedPtr<FSlateBrush>& B = GRuled.FindOrAdd(K);
	if (!B.IsValid()) { B = MakeShared<FSlateRoundedBoxBrush>(FLinearColor::Transparent, 0.0f, C, Thickness); }
	return B.Get();
}

const FSlateBrush* CouponEdge()
{
	static TSharedPtr<FSlateBrush>& B = *new TSharedPtr<FSlateBrush>();
	if (!B.IsValid())
	{
		if (UTexture2D* T = LoadPicture(TEXT("production/art/ui/coupon-dash.png")))
		{
			B = MakeShared<FSlateBorderBrush>(T, FMargin(0.25f), FLinearColor::White);
		}
		else { B = MakeShared<FSlateRoundedBoxBrush>(FLinearColor::Transparent, 0.0f, Ink(), 2.0f); }
	}
	return B.Get();
}

const FSlateBrush* Picture(const FString& Rel, const FVector2D& Size)
{
	static TMap<FString, TSharedPtr<FSlateBrush>>& Pictures = *new TMap<FString, TSharedPtr<FSlateBrush>>();
	TSharedPtr<FSlateBrush>& B = Pictures.FindOrAdd(Rel);
	if (!B.IsValid())
	{
		UTexture2D* T = LoadPicture(Rel);
		if (T == nullptr) { return nullptr; }
		B = MakeShared<FSlateImageBrush>(T, Size);
	}
	return B.Get();
}

// The centred 16:9: the child is given the middle 1920 units of the width (all
// of it where the screen is narrower, 16:10 or 4:3) and the whole height,
// whatever it asks for, so a page laid out at the left of the safe region
// sits at the left of the middle 16:9 and not at the screen's own edge.
class SSafeRegion : public SCompoundWidget
{
public:
	SLATE_BEGIN_ARGS(SSafeRegion) {}
		SLATE_DEFAULT_SLOT(FArguments, Content)
	SLATE_END_ARGS()
	void Construct(const FArguments& InArgs) { ChildSlot[ InArgs._Content.Widget ]; }
	virtual void OnArrangeChildren(const FGeometry& AllottedGeometry, FArrangedChildren& ArrangedChildren) const override
	{
		const FVector2f Size = AllottedGeometry.GetLocalSize();
		const float W = FMath::Min(Size.X, 1920.0f);
		const EVisibility Vis = ChildSlot.GetWidget()->GetVisibility();
		if (ArrangedChildren.Accepts(Vis))
		{
			ArrangedChildren.AddWidget(Vis, AllottedGeometry.MakeChild(ChildSlot.GetWidget(), FVector2f((Size.X - W) * 0.5f, 0.0f), FVector2f(W, Size.Y)));
		}
	}
};

TSharedRef<SWidget> SafeRegion(TSharedRef<SWidget> Content, EHorizontalAlignment H, EVerticalAlignment V)
{
	return SNew(SSafeRegion)
		[
			SNew(SBox).HAlign(H).VAlign(V)[ Content ]
		];
}

TSharedRef<SWidget> PaperSheet(TSharedRef<SWidget> Content, const FMargin& Padding)
{
	return SNew(SOverlay)
		// a soft shadow under the sheet, down and to the right
		+ SOverlay::Slot().Padding(FMargin(7.0f, 9.0f, -7.0f, -9.0f))
		[
			SNew(SBorder).BorderImage(Solid(FLinearColor(0.0f, 0.0f, 0.0f, 0.32f)))
		]
		+ SOverlay::Slot()
		[
			// the yellowed edge drawn over the whole sheet, taking its size from the content
			SNew(SBorder).BorderImage(Sheet()).Padding(0.0f)
			[
				SNew(SBorder).BorderImage(SheetEdge()).Padding(Padding)[ Content ]
			]
		];
}

TSharedRef<SWidget> Rule(float Thickness, const FLinearColor& C)
{
	return SNew(SBox).HeightOverride(Thickness)[ SNew(SImage).Image(Solid(C)) ];
}

TSharedRef<SWidget> Band(const FString& Text, float Units, const FMargin& Padding)
{
	return SNew(SBorder).BorderImage(Solid(Red())).Padding(Padding)
		[
			SNew(STextBlock).Text(FText::FromString(Text.ToUpper())).Font(Font(EFace::League, Units, 30))
			.ColorAndOpacity(FSlateColor(FLinearColor::White))
		];
}

TSharedRef<SWidget> Ear(const FString& Text, bool bFilled)
{
	return SNew(SBorder).BorderImage(bFilled ? Solid(Ink()) : Ruled(Ink(), 2.0f)).Padding(FMargin(12.0f, 6.0f, 12.0f, 4.0f))
		[
			SNew(STextBlock).Text(FText::FromString(Text.ToUpper())).Font(Font(EFace::League, 30, 20))
			.ColorAndOpacity(FSlateColor(bFilled ? Newsprint() : Ink()))
		];
}

TSharedRef<SWidget> Key(const FString& Label)
{
	// The arrows come from Old Standard: Libre Franklin has none.
	const bool bArrow = Label == TEXT("↑") || Label == TEXT("↓") || Label == TEXT("←") || Label == TEXT("→");
	return SNew(SBorder).BorderImage(Solid(Newsprint())).Padding(0.0f)
		[
			SNew(SBorder).BorderImage(Ruled(Ink(), 2.0f)).Padding(FMargin(bArrow ? 12.0f : 10.0f, 2.0f, bArrow ? 12.0f : 10.0f, 2.0f))
			.HAlign(HAlign_Center).VAlign(VAlign_Center)
			[
				SNew(SBox).MinDesiredWidth(bArrow ? 18.0f : 0.0f).MinDesiredHeight(40.0f).HAlign(HAlign_Center).VAlign(VAlign_Center)
				[
					SNew(STextBlock).Text(FText::FromString(Label)).Font(Font(bArrow ? EFace::Old : EFace::Franklin700, 30))
					.ColorAndOpacity(FSlateColor(Ink()))
				]
			]
		];
}

// A CONTROLLER'S BUTTON (STYLE-GUIDE.md, A controller's buttons): round, ruled in ink, never square
// like a key; the pad drawn as its cross in a round button ("+").
TSharedRef<SWidget> PadButton(const FString& Label)
{
	static const FSlateRoundedBoxBrush* Round = new FSlateRoundedBoxBrush(Newsprint(), 22.0f, Ink(), 2.0f, FVector2D(44.0f, 44.0f));
	TSharedRef<SWidget> Inside = Label == TEXT("+")
		? StaticCastSharedRef<SWidget>(SNew(SOverlay)
			+ SOverlay::Slot().HAlign(HAlign_Center).VAlign(VAlign_Center)[ SNew(SBox).WidthOverride(26.0f).HeightOverride(8.0f)[ SNew(SImage).Image(Solid(Ink())) ] ]
			+ SOverlay::Slot().HAlign(HAlign_Center).VAlign(VAlign_Center)[ SNew(SBox).WidthOverride(8.0f).HeightOverride(26.0f)[ SNew(SImage).Image(Solid(Ink())) ] ])
		: StaticCastSharedRef<SWidget>(SNew(STextBlock).Text(FText::FromString(Label)).Font(Font(EFace::Franklin700, 26)).ColorAndOpacity(FSlateColor(Ink())));
	return SNew(SBox).WidthOverride(44.0f).HeightOverride(44.0f)
		[
			SNew(SBorder).BorderImage(Round).Padding(0.0f).HAlign(HAlign_Center).VAlign(VAlign_Center)[ Inside ]
		];
}

namespace { bool bPadInUse = false; }
bool PadInUse() { return bPadInUse; }
void SetPadInUse(bool bPad) { bPadInUse = bPad; }

TSharedRef<SWidget> Hints(const TArray<TPair<TArray<FString>, FString>>& Items)
{
	TSharedRef<SHorizontalBox> Row = SNew(SHorizontalBox);
	for (int32 I = 0; I < Items.Num(); ++I)
	{
		TSharedRef<SHorizontalBox> One = SNew(SHorizontalBox);
		for (int32 K = 0; K < Items[I].Key.Num(); ++K)
		{
			// "pad:A" is a controller's round button; anything else a key.
			const FString& K1 = Items[I].Key[K];
			One->AddSlot().AutoWidth().VAlign(VAlign_Center).Padding(FMargin(K > 0 ? 10.0f : 0.0f, 0.0f, 0.0f, 0.0f))[ K1.StartsWith(TEXT("pad:")) ? PadButton(K1.RightChop(4)) : Key(K1) ];
		}
		One->AddSlot().AutoWidth().VAlign(VAlign_Center)
			[
				SNew(SBorder).BorderImage(Solid(Backing())).Padding(FMargin(12.0f, 3.0f, 12.0f, 3.0f))
				[
					SNew(STextBlock).Text(FText::FromString(Items[I].Value)).Font(Font(EFace::Franklin500, 30))
					.ColorAndOpacity(FSlateColor(OnDark()))
				]
			];
		Row->AddSlot().AutoWidth().Padding(FMargin(I > 0 ? 36.0f : 0.0f, 0.0f, 0.0f, 0.0f))[ One ];
	}
	return Row;
}

TSharedRef<SWidget> OnBacking(TSharedRef<SWidget> Content, const FMargin& Padding)
{
	return SNew(SBorder).BorderImage_Lambda([]() { return Solid(Backing()); }).Padding(Padding)[ Content ];
}

// THE PAGES' OWN SOUNDS (STYLE-GUIDE.md, Sound; tools/ui/make_ui_sounds.py):
// production/audio/ui/<name>.wav, read once, played as interface sounds (they
// play while the game is paused), quiet, and off with the settings' switch.
namespace
{
	struct FUiWav { TSharedPtr<TArray<uint8>> Pcm; int32 Rate = 0; int32 Channels = 0; };
	TMap<FString, FUiWav>& UiWavs() { static TMap<FString, FUiWav>* M = new TMap<FString, FUiWav>(); return *M; }
	TWeakObjectPtr<UAudioComponent> GUiLoop;

	const FUiWav* UiWav(const FString& Name)
	{
		if (const FUiWav* Have = UiWavs().Find(Name)) { return Have->Pcm.IsValid() ? Have : nullptr; }
		FUiWav W;
		TArray<uint8> Bytes;
		const FString Path = FPaths::Combine(Root(), TEXT("production/audio/ui"), Name + TEXT(".wav"));
		if (FFileHelper::LoadFileToArray(Bytes, *Path) && Bytes.Num() > 44 && FMemory::Memcmp(Bytes.GetData(), "RIFF", 4) == 0)
		{
			// the chunks after "WAVE": "fmt " for the rate and channels, "data" for the samples
			int32 At = 12;
			while (At + 8 <= Bytes.Num())
			{
				const int32 Len = (int32)(Bytes[At + 4] | (Bytes[At + 5] << 8) | (Bytes[At + 6] << 16) | (Bytes[At + 7] << 24));
				if (FMemory::Memcmp(&Bytes[At], "fmt ", 4) == 0 && At + 16 <= Bytes.Num())
				{
					W.Channels = Bytes[At + 10] | (Bytes[At + 11] << 8);
					W.Rate = (int32)(Bytes[At + 12] | (Bytes[At + 13] << 8) | (Bytes[At + 14] << 16) | (Bytes[At + 15] << 24));
				}
				else if (FMemory::Memcmp(&Bytes[At], "data", 4) == 0)
				{
					const int32 N = FMath::Min(Len, Bytes.Num() - (At + 8));
					W.Pcm = MakeShared<TArray<uint8>>();
					W.Pcm->Append(&Bytes[At + 8], N);
					break;
				}
				At += 8 + Len + (Len & 1);
			}
		}
		if (!W.Pcm.IsValid() || W.Rate <= 0 || W.Channels <= 0)
		{
			UE_LOG(LogTemp, Display, TEXT("LedgerPaper: no interface sound %s (%s)"), *Name, *Path);
			W.Pcm.Reset();
		}
		UiWavs().Add(Name, W);
		return W.Pcm.IsValid() ? UiWavs().Find(Name) : nullptr;
	}

	USoundWaveProcedural* UiWave(const FUiWav& W)
	{
		USoundWaveProcedural* S = NewObject<USoundWaveProcedural>(GetTransientPackage());
		S->SetSampleRate(W.Rate);
		S->NumChannels = W.Channels;
		S->Duration = INDEFINITELY_LOOPING_DURATION;
		S->bLooping = false;
		S->QueueAudio(W.Pcm->GetData(), W.Pcm->Num());
		return S;
	}

	UWorld* UiWorld() { return GEngine != nullptr && GEngine->GameViewport != nullptr ? GEngine->GameViewport->GetWorld() : nullptr; }
}

void UiSound(const FString& Name)
{
	if (!LedgerSettings::UiSoundsOn()) { return; }
	if (Name.StartsWith(TEXT("key")) && !LedgerSettings::TypingSoundOn()) { return; }
	UWorld* W = UiWorld();
	const FUiWav* Wav = W != nullptr ? UiWav(Name) : nullptr;
	if (Wav == nullptr) { return; }
	UGameplayStatics::PlaySound2D(W, UiWave(*Wav), 1.0f, 1.0f, 0.0f, nullptr, nullptr, true);
}

void UiKey()
{
	static int32 Turn = 0;
	static const TCHAR* Keys[3] = { TEXT("key1"), TEXT("key2"), TEXT("key3") };
	UiSound(Keys[Turn++ % 3]);
}

void UiLoop(const FString& Name, bool bOn)
{
	if (!bOn)
	{
		if (GUiLoop.IsValid()) { GUiLoop->Stop(); }
		GUiLoop.Reset();
		return;
	}
	if (GUiLoop.IsValid() || !LedgerSettings::UiSoundsOn()) { return; }
	UWorld* W = UiWorld();
	const FUiWav* Wav = W != nullptr ? UiWav(Name) : nullptr;
	if (Wav == nullptr) { return; }
	USoundWaveProcedural* S = UiWave(*Wav);
	// round again whenever it runs short, for as long as the page is up
	TSharedPtr<TArray<uint8>> Pcm = Wav->Pcm;
	S->OnSoundWaveProceduralUnderflow.BindLambda([Pcm](USoundWaveProcedural* Wave, int32) { Wave->QueueAudio(Pcm->GetData(), Pcm->Num()); });
	UAudioComponent* C = UGameplayStatics::CreateSound2D(W, S, 1.0f, 1.0f, 0.0f, nullptr, true, false);
	if (C != nullptr) { C->bIsUISound = true; C->Play(); GUiLoop = C; }
}

namespace { bool bReduceMotion = false; }
// The player's own setting (LedgerSettings), or -ReduceMotion for a test.
bool ReduceMotion() { return bReduceMotion || FParse::Param(FCommandLine::Get(), TEXT("ReduceMotion")); }
void SetReduceMotion(bool bOn) { bReduceMotion = bOn; }
}

using namespace LedgerPaper;

void SPaperChoice::Construct(const FArguments& InArgs)
{
	Text = InArgs._Text;
	Note = InArgs._Note;
	Enabled = InArgs._Enabled;
	OnChosen = InArgs._OnChosen;
	const float Units = InArgs._Units;
	const bool bNote = Note.IsBound() || !Note.Get().IsEmpty();
	ChildSlot
	[
		SNew(SBorder)
		// pressed: the row tints red for 120 ms
		.BorderImage_Lambda([this]() { return Solid(PressedAt > 0.0 && FPlatformTime::Seconds() - PressedAt < 0.12 ? FLinearColor(Red().R, Red().G, Red().B, 0.14f) : FLinearColor::Transparent); })
		.Padding(0.0f)
		[
			SNew(SBox).MinDesiredHeight(InArgs._RowHeight).VAlign(VAlign_Center)
			[
				SNew(SHorizontalBox)
				+ SHorizontalBox::Slot().AutoWidth().VAlign(VAlign_Fill).Padding(FMargin(0.0f, 10.0f, 0.0f, 10.0f))
				[
					SNew(SBox).WidthOverride_Lambda([this]() { return FOptionalSize(BarWidth()); })
					[
						SNew(SImage).Image(Solid(Red()))
					]
				]
				+ SHorizontalBox::Slot().FillWidth(1.0f).VAlign(VAlign_Center).Padding(FMargin(23.0f, 0.0f, 0.0f, 0.0f))
				[
					SNew(SVerticalBox)
					+ SVerticalBox::Slot().AutoHeight()
					[
						SNew(STextBlock).Text_Lambda([this]() { return FText::FromString(Text.Get()); })
						.Font(Font(EFace::Franklin800, Units)).ColorAndOpacity_Lambda([this]() { return TextColour(); })
					]
					+ SVerticalBox::Slot().AutoHeight()
					[
						SNew(STextBlock).Text_Lambda([this]() { return FText::FromString(Note.Get()); })
						.Visibility_Lambda([this]() { return Note.Get().IsEmpty() ? EVisibility::Collapsed : EVisibility::HitTestInvisible; })
						.Font(Font(EFace::OldItalic, 28)).ColorAndOpacity_Lambda([this]() { return FSlateColor(Enabled.Get() ? Ink() : Unavailable()); })
					]
				]
			]
		]
	];
	(void)bNote;
}

bool SPaperChoice::InHand() const
{
	return HasKeyboardFocus() || HasUserFocus(0).IsSet();
}

float SPaperChoice::BarWidth() const
{
	if (!Enabled.Get()) { return 0.0f; }
	const double Now = FPlatformTime::Seconds();
	if (PressedAt > 0.0 && Now - PressedAt < 0.12) { return 14.0f; }
	if (!InHand()) { return 0.0f; }
	// the bar grows from the left in 120 ms, or is simply there with Reduce motion
	const double T = InHandSince < 0.0 || ReduceMotion() ? 1.0 : FMath::Clamp((Now - InHandSince) / 0.12, 0.0, 1.0);
	return 8.0f * (float)T;
}

FSlateColor SPaperChoice::TextColour() const
{
	if (!Enabled.Get()) { return FSlateColor(Unavailable()); }
	return FSlateColor(InHand() ? Red() : Ink());
}

void SPaperChoice::Take()
{
	if (!Enabled.Get()) { return; }
	LedgerPaper::UiSound(TEXT("tick"));
	PressedAt = FPlatformTime::Seconds();
	OnChosen.ExecuteIfBound();
}

FReply SPaperChoice::OnKeyDown(const FGeometry& MyGeometry, const FKeyEvent& InKeyEvent)
{
	const FKey K = InKeyEvent.GetKey();
	if (K == EKeys::Enter || K == EKeys::SpaceBar || K == EKeys::Gamepad_FaceButton_Bottom)
	{
		Take();
		return FReply::Handled();
	}
	return SCompoundWidget::OnKeyDown(MyGeometry, InKeyEvent);
}

FReply SPaperChoice::OnMouseButtonDown(const FGeometry& MyGeometry, const FPointerEvent& MouseEvent)
{
	if (MouseEvent.GetEffectingButton() == EKeys::LeftMouseButton)
	{
		return FReply::Handled().CaptureMouse(SharedThis(this)).SetUserFocus(SharedThis(this), EFocusCause::Mouse);
	}
	return FReply::Unhandled();
}

FReply SPaperChoice::OnMouseButtonUp(const FGeometry& MyGeometry, const FPointerEvent& MouseEvent)
{
	if (MouseEvent.GetEffectingButton() == EKeys::LeftMouseButton && HasMouseCapture())
	{
		if (MyGeometry.IsUnderLocation(MouseEvent.GetScreenSpacePosition())) { Take(); }
		return FReply::Handled().ReleaseMouseCapture();
	}
	return FReply::Unhandled();
}

void SPaperChoice::OnMouseEnter(const FGeometry& MyGeometry, const FPointerEvent& MouseEvent)
{
	SCompoundWidget::OnMouseEnter(MyGeometry, MouseEvent);
	// the mouse puts it in hand, as the keys do
	if (Enabled.Get()) { FSlateApplication::Get().SetUserFocus(0, SharedThis(this), EFocusCause::Mouse); }
}

FReply SPaperChoice::OnFocusReceived(const FGeometry& MyGeometry, const FFocusEvent& InFocusEvent)
{
	InHandSince = FPlatformTime::Seconds();
	return FReply::Handled();
}

void SPaperChoice::OnFocusLost(const FFocusEvent& InFocusEvent)
{
	InHandSince = -1.0;
}
