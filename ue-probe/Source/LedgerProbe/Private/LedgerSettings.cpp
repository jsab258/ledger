#include "LedgerSettings.h"

#include "LedgerPaper.h"

#include "AudioDevice.h"
#include "Engine/Engine.h"
#include "Engine/GameViewportClient.h"
#include "Engine/World.h"
#include "Framework/Application/SlateApplication.h"
#include "GameFramework/GameUserSettings.h"
#include "GameFramework/PlayerController.h"
#include "Kismet/KismetSystemLibrary.h"
#include "Misc/ConfigCacheIni.h"
#include "Widgets/Images/SImage.h"
#include "Widgets/Layout/SBorder.h"
#include "Widgets/Layout/SBox.h"
#include "Widgets/SBoxPanel.h"
#include "Widgets/SOverlay.h"
#include "Widgets/Text/STextBlock.h"

using namespace LedgerPaper;

namespace LedgerSettings
{
namespace
{
	const TCHAR* kSection = TEXT("LedgerSettings");

	// The player's own settings, as kept in the settings file.
	bool bSubtitles = true, bSpeakerNames = true, bSuggestAlways = false, bReduceMotion = false, bInvertLook = false, bQuietBehind = true;
	int32 GSubtitleSize = 1;                  // Small, Medium (the guide's 39), Large, Largest
	float GSensitivity = 1.0f, GMaster = 1.0f, GBrightness = 0.5f;
	bool bLoaded = false;

	void Save()
	{
		if (GConfig == nullptr) { return; }
		GConfig->SetBool(kSection, TEXT("Subtitles"), bSubtitles, GGameUserSettingsIni);
		GConfig->SetInt(kSection, TEXT("SubtitleSize"), GSubtitleSize, GGameUserSettingsIni);
		GConfig->SetFloat(kSection, TEXT("Backing"), BackingStrength(), GGameUserSettingsIni);
		GConfig->SetBool(kSection, TEXT("SpeakerNames"), bSpeakerNames, GGameUserSettingsIni);
		GConfig->SetBool(kSection, TEXT("ReduceMotion"), bReduceMotion, GGameUserSettingsIni);
		GConfig->SetBool(kSection, TEXT("SuggestAlways"), bSuggestAlways, GGameUserSettingsIni);
		GConfig->SetFloat(kSection, TEXT("LookSensitivity"), GSensitivity, GGameUserSettingsIni);
		GConfig->SetBool(kSection, TEXT("InvertLook"), bInvertLook, GGameUserSettingsIni);
		GConfig->SetFloat(kSection, TEXT("Master"), GMaster, GGameUserSettingsIni);
		GConfig->SetBool(kSection, TEXT("QuietBehind"), bQuietBehind, GGameUserSettingsIni);
		GConfig->SetFloat(kSection, TEXT("Brightness"), GBrightness, GGameUserSettingsIni);
		GConfig->Flush(false, GGameUserSettingsIni);
	}

	void ApplySound()
	{
		if (GEngine != nullptr)
		{
			if (FAudioDeviceHandle Dev = GEngine->GetMainAudioDevice()) { Dev->SetTransientPrimaryVolume(GMaster); }
		}
		// the engine's own: how loud the game is while another window is in front
		FApp::SetUnfocusedVolumeMultiplier(bQuietBehind ? 0.0f : 1.0f);
	}

	void ApplyBrightness()
	{
		// 0.5 is the engine's own gamma, 2.2; the slider runs from 1.8 to 2.6
		if (GEngine != nullptr) { GEngine->DisplayGamma = 1.8f + 0.8f * GBrightness; }
	}

	UGameUserSettings* Gus() { return GEngine != nullptr ? GEngine->GetGameUserSettings() : nullptr; }

	// THE PRESET IS READ FROM THE FIVE LINES UNDER IT (the guide: "changing one
	// of them makes it Custom"): the engine's own overall level also counts the
	// groups the page does not show, and read Custom over five Highests.
	int32 PresetOf(UGameUserSettings* S)
	{
		if (S == nullptr) { return -1; }
		const int32 L = S->GetShadowQuality();
		const bool bSame = S->GetReflectionQuality() == L && S->GetViewDistanceQuality() == L && S->GetTextureQuality() == L && S->GetVisualEffectQuality() == L;
		return bSame ? FMath::Clamp(L, 0, 3) : -1;
	}

	FString LevelName(int32 L)
	{
		switch (L) { case 0: return TEXT("Low"); case 1: return TEXT("Medium"); case 2: return TEXT("High"); case 3: return TEXT("Highest"); default: return TEXT("Custom"); }
	}

	// ONE LINE OF THE PAGE: a value changed with left and right, a slider, the
	// quality preset, a section head, or a line that only shows (a key).
	enum class EKind : uint8 { Value, Slider, Presets, Head, Show };
	struct FLine
	{
		EKind Kind = EKind::Value;
		FString Label;
		FString Explain;     // the right-hand column's words
		FString Note;        // and its italic note
		TFunction<FString()> Value;
		TFunction<void(int32)> Step;
		TFunction<float()> Get;
		TFunction<void(float)> Set;
		TFunction<FString()> WhyNot;    // non-empty when the line cannot be changed now, in place of its value
	};

	TArray<FLine> PictureLines()
	{
		TArray<FLine> L;
		{
			FLine Q;
			Q.Kind = EKind::Presets;
			Q.Label = TEXT("Quality");
			FString Picked;
			if (GConfig != nullptr) { GConfig->GetString(TEXT("Ledger"), TEXT("FirstLaunchPicture"), Picked, GGameUserSettingsIni); }
			Q.Explain = TEXT("Sets the five lines under it at once: shadows, reflections in the wet, how far you see, textures and effects.");
			if (!Picked.IsEmpty()) { Q.Explain += FString::Printf(TEXT("\n\n%s was picked for this PC when the game first ran."), *Picked); }
			Q.Note = TEXT("Detect for this PC measures it again and picks for you. Changing any of the five lines under it makes this Custom.");
			Q.Step = [](int32 D)
			{
				UGameUserSettings* S = Gus();
				if (S == nullptr) { return; }
				const int32 Now = PresetOf(S);
				S->SetOverallScalabilityLevel(FMath::Clamp((Now < 0 ? 2 : Now) + D, 0, 3));
				S->ApplyNonResolutionSettings();
				S->SaveSettings();
			};
			L.Add(Q);
		}
		struct FOne { const TCHAR* Label; const TCHAR* Explain; TFunction<int32(UGameUserSettings*)> Get; TFunction<void(UGameUserSettings*, int32)> Set; };
		const FOne Five[5] = {
			{ TEXT("Shadows"), TEXT("How sharp the shadows are and how many lights cast them. The biggest cost on a weaker card."),
			  [](UGameUserSettings* S) { return S->GetShadowQuality(); }, [](UGameUserSettings* S, int32 V) { S->SetShadowQuality(V); } },
			{ TEXT("Reflections in the wet"), TEXT("How much of the street the wet road and the shop windows give back."),
			  [](UGameUserSettings* S) { return S->GetReflectionQuality(); }, [](UGameUserSettings* S, int32 V) { S->SetReflectionQuality(V); } },
			{ TEXT("How far you see"), TEXT("How far down the street the detail reaches before it thins."),
			  [](UGameUserSettings* S) { return S->GetViewDistanceQuality(); }, [](UGameUserSettings* S, int32 V) { S->SetViewDistanceQuality(V); } },
			{ TEXT("Textures"), TEXT("How fine the brick, the paint and the paving are close up. Lower it if the card has little memory of its own."),
			  [](UGameUserSettings* S) { return S->GetTextureQuality(); }, [](UGameUserSettings* S, int32 V) { S->SetTextureQuality(V); } },
			{ TEXT("Effects"), TEXT("Rain, steam and the glow round the lamps."),
			  [](UGameUserSettings* S) { return S->GetVisualEffectQuality(); }, [](UGameUserSettings* S, int32 V) { S->SetVisualEffectQuality(V); } },
		};
		for (const FOne& O : Five)
		{
			FLine V;
			V.Label = O.Label;
			V.Explain = O.Explain;
			TFunction<int32(UGameUserSettings*)> G = O.Get;
			TFunction<void(UGameUserSettings*, int32)> St = O.Set;
			V.Value = [G]() { UGameUserSettings* S = Gus(); return S != nullptr ? LevelName(FMath::Clamp(G(S), 0, 3)) : FString(); };
			V.Step = [G, St](int32 D)
			{
				UGameUserSettings* S = Gus();
				if (S == nullptr) { return; }
				St(S, FMath::Clamp(G(S) + D, 0, 3));
				S->ApplyNonResolutionSettings();
				S->SaveSettings();
			};
			L.Add(V);
		}
		{ FLine H; H.Kind = EKind::Head; H.Label = TEXT("The screen"); L.Add(H); }
		{
			FLine D;
			D.Label = TEXT("Display");
			D.Explain = TEXT("Full screen fills the monitor at its own size. Window keeps the game in a window you can move.");
			D.Value = []() { UGameUserSettings* S = Gus(); return S != nullptr && S->GetFullscreenMode() == EWindowMode::Windowed ? FString(TEXT("Window")) : FString(TEXT("Full screen")); };
			D.Step = [](int32)
			{
				UGameUserSettings* S = Gus();
				if (S == nullptr) { return; }
				const bool bWindow = S->GetFullscreenMode() != EWindowMode::Windowed;
				S->SetFullscreenMode(bWindow ? EWindowMode::Windowed : EWindowMode::WindowedFullscreen);
				S->SetScreenResolution(bWindow ? FIntPoint(1920, 1080) : S->GetDesktopResolution());
				S->ApplyResolutionSettings(false);
				S->SaveSettings();
			};
			L.Add(D);
		}
		{
			FLine R;
			R.Label = TEXT("Resolution");
			R.Explain = TEXT("How many pixels the window is. In full screen the game uses your desktop's own.");
			R.Value = []() { UGameUserSettings* S = Gus(); const FIntPoint P = S != nullptr ? S->GetScreenResolution() : FIntPoint(0, 0); return FString::Printf(TEXT("%d × %d"), P.X, P.Y); };
			R.WhyNot = []() { UGameUserSettings* S = Gus(); return S != nullptr && S->GetFullscreenMode() != EWindowMode::Windowed ? FString(TEXT("Same as your desktop")) : FString(); };
			R.Step = [](int32 Dir)
			{
				UGameUserSettings* S = Gus();
				if (S == nullptr) { return; }
				TArray<FIntPoint> Sizes;
				UKismetSystemLibrary::GetSupportedFullscreenResolutions(Sizes);
				if (Sizes.Num() == 0) { return; }
				const FIntPoint Now = S->GetScreenResolution();
				int32 I = Sizes.IndexOfByPredicate([Now](const FIntPoint& P) { return P == Now; });
				I = I < 0 ? 0 : FMath::Clamp(I + Dir, 0, Sizes.Num() - 1);
				S->SetScreenResolution(Sizes[I]);
				S->ApplyResolutionSettings(false);
				S->SaveSettings();
			};
			L.Add(R);
		}
		{
			FLine F;
			F.Label = TEXT("Frame rate limit");
			F.Explain = TEXT("The most frames a second the game draws. Sixty keeps the card cooler and quieter.");
			static const float Steps[6] = { 30.0f, 60.0f, 120.0f, 144.0f, 165.0f, 0.0f };
			F.Value = []() { UGameUserSettings* S = Gus(); const float V = S != nullptr ? S->GetFrameRateLimit() : 0.0f; return V <= 0.0f ? FString(TEXT("None")) : FString::Printf(TEXT("%.0f"), V); };
			F.Step = [](int32 D)
			{
				UGameUserSettings* S = Gus();
				if (S == nullptr) { return; }
				const float V = S->GetFrameRateLimit();
				int32 I = 5;
				for (int32 K = 0; K < 6; ++K) { if (FMath::IsNearlyEqual(Steps[K], V)) { I = K; } }
				S->SetFrameRateLimit(Steps[FMath::Clamp(I + D, 0, 5)]);
				S->ApplyNonResolutionSettings();
				S->SaveSettings();
			};
			L.Add(F);
		}
		{
			FLine B;
			B.Kind = EKind::Slider;
			B.Label = TEXT("Brightness");
			B.Explain = TEXT("Turn it up until the darkest doorway on the street at night is just in sight.");
			B.Get = []() { return GBrightness; };
			B.Set = [](float V) { GBrightness = FMath::Clamp(V, 0.0f, 1.0f); ApplyBrightness(); Save(); };
			L.Add(B);
		}
		return L;
	}

	FLine Toggle(const TCHAR* Label, const TCHAR* Explain, bool* Flag, const TCHAR* On = TEXT("On"), const TCHAR* Off = TEXT("Off"), TFunction<void()> After = nullptr)
	{
		FLine T;
		T.Label = Label;
		T.Explain = Explain;
		const FString OnS = On, OffS = Off;
		T.Value = [Flag, OnS, OffS]() { return *Flag ? OnS : OffS; };
		T.Step = [Flag, After](int32) { *Flag = !*Flag; if (After) { After(); } Save(); };
		return T;
	}

	TArray<FLine> SoundLines()
	{
		TArray<FLine> L;
		FLine M;
		M.Kind = EKind::Slider;
		M.Label = TEXT("Everything");
		M.Explain = TEXT("The whole game's sound: the street, the voices and the town.");
		M.Get = []() { return GMaster; };
		M.Set = [](float V) { GMaster = FMath::Clamp(V, 0.0f, 1.0f); ApplySound(); Save(); };
		L.Add(M);
		L.Add(Toggle(TEXT("When the game is behind another window"), TEXT("Whether the street goes quiet while another window is in front of it."),
			&bQuietBehind, TEXT("Quiet"), TEXT("Heard"), []() { ApplySound(); }));
		return L;
	}

	TArray<FLine> ControlLines()
	{
		TArray<FLine> L;
		{
			FLine S;
			S.Kind = EKind::Slider;
			S.Label = TEXT("Looking round, how fast");
			S.Explain = TEXT("How far the view turns for a move of the mouse.");
			S.Get = []() { return (GSensitivity - 0.5f) / 1.5f; };
			S.Set = [](float V) { GSensitivity = 0.5f + 1.5f * FMath::Clamp(V, 0.0f, 1.0f); Save(); };
			L.Add(S);
		}
		L.Add(Toggle(TEXT("Looking up and down"), TEXT("Whether moving the mouse forward looks up or down."), &bInvertLook, TEXT("Turned over"), TEXT("As the mouse moves")));
		{ FLine H; H.Kind = EKind::Head; H.Label = TEXT("The keys"); L.Add(H); }
		struct FKeyLine { const TCHAR* What; const TCHAR* Keys; };
		const FKeyLine Keys[] = {
			{ TEXT("Walk"), TEXT("W  A  S  D") }, { TEXT("Run"), TEXT("Shift") }, { TEXT("Look"), TEXT("Mouse") },
			{ TEXT("Use what is in front of you"), TEXT("E") }, { TEXT("Talk"), TEXT("T") }, { TEXT("Say it"), TEXT("Enter") },
			{ TEXT("Wait a while"), TEXT("Z") }, { TEXT("Report a reply"), TEXT("R") }, { TEXT("About the voices"), TEXT("F1") },
			{ TEXT("Stop press"), TEXT("Esc") } };
		for (const FKeyLine& K : Keys)
		{
			FLine Line;
			Line.Kind = EKind::Show;
			Line.Label = K.What;
			const FString Ks = K.Keys;
			Line.Value = [Ks]() { return Ks; };
			Line.Explain = TEXT("The keys are fixed in this build; changing them comes later.");
			L.Add(Line);
		}
		return L;
	}

	TArray<FLine> ReadingLines()
	{
		TArray<FLine> L;
		L.Add(Toggle(TEXT("Subtitles"), TEXT("Words for everything said near you."), &bSubtitles));
		{
			FLine S;
			S.Label = TEXT("Subtitle size");
			S.Explain = TEXT("How large the subtitles are. Medium is set so the words stand about the height of a thumbnail across a desk.");
			S.Value = []() { static const TCHAR* N[4] = { TEXT("Small"), TEXT("Medium"), TEXT("Large"), TEXT("Largest") }; return FString(N[FMath::Clamp(GSubtitleSize, 0, 3)]); };
			S.Step = [](int32 D) { GSubtitleSize = FMath::Clamp(GSubtitleSize + D, 0, 3); Save(); };
			L.Add(S);
		}
		{
			FLine B;
			B.Kind = EKind::Slider;
			B.Label = TEXT("The band behind them");
			B.Explain = TEXT("How dark the band behind subtitles and prompts is. At 80% they read against a white sky.");
			B.Get = []() { return BackingStrength(); };
			B.Set = [](float V) { SetBackingStrength(V); Save(); };
			L.Add(B);
		}
		L.Add(Toggle(TEXT("Who is speaking"), TEXT("The speaker's name before each line, or how Tom would describe them until he knows it."), &bSpeakerNames));
		L.Add(Toggle(TEXT("Reduce motion"), TEXT("Menus and prompts fade, and nothing slides or grows."), &bReduceMotion, TEXT("On"), TEXT("Off"), []() { SetReduceMotion(bReduceMotion); }));
		L.Add(Toggle(TEXT("Suggested lines"), TEXT("Lines you can say instead of typing your own. On Tab, they open when you press Tab while typing; Always, they are there whenever you talk."),
			&bSuggestAlways, TEXT("Always"), TEXT("On Tab")));
		return L;
	}

	const TCHAR* kTabs[4] = { TEXT("Picture"), TEXT("Sound"), TEXT("Controls"), TEXT("Subtitles and reading") };

	class SSettingsPage : public SCompoundWidget
	{
	public:
		SLATE_BEGIN_ARGS(SSettingsPage) {}
			SLATE_EVENT(FSimpleDelegate, OnBack)
		SLATE_END_ARGS()

		void Construct(const FArguments& InArgs)
		{
			OnBack = InArgs._OnBack;
			ChildSlot[ SAssignNew(Holder, SBox) ];
			Rebuild();
		}
		virtual bool SupportsKeyboardFocus() const override { return true; }

		virtual FReply OnKeyDown(const FGeometry& G, const FKeyEvent& E) override
		{
			const FKey K = E.GetKey();
			if (K == EKeys::Escape || K == EKeys::Gamepad_FaceButton_Right) { OnBack.ExecuteIfBound(); return FReply::Handled(); }
			if (K == EKeys::Tab || K == EKeys::Gamepad_RightShoulder) { Tab = (Tab + (E.IsShiftDown() ? 3 : 1)) % 4; Row = -1; Rebuild(); return FReply::Handled(); }
			if (K == EKeys::Gamepad_LeftShoulder) { Tab = (Tab + 3) % 4; Row = -1; Rebuild(); return FReply::Handled(); }
			if (K == EKeys::Up || K == EKeys::Gamepad_DPad_Up) { Move(-1); return FReply::Handled(); }
			if (K == EKeys::Down || K == EKeys::Gamepad_DPad_Down) { Move(1); return FReply::Handled(); }
			if (K == EKeys::Left || K == EKeys::Gamepad_DPad_Left) { Change(-1); return FReply::Handled(); }
			if (K == EKeys::Right || K == EKeys::Gamepad_DPad_Right) { Change(1); return FReply::Handled(); }
			if ((K == EKeys::Enter || K == EKeys::Gamepad_FaceButton_Bottom) && Lines.IsValidIndex(Row) && Lines[Row].Kind == EKind::Presets) { Detect(); return FReply::Handled(); }
			return FReply::Unhandled();
		}

	private:
		FSimpleDelegate OnBack;
		TSharedPtr<SBox> Holder;
		TArray<FLine> Lines;
		int32 Tab = 0, Row = -1;

		bool Takes(int32 I) const { return Lines.IsValidIndex(I) && Lines[I].Kind != EKind::Head && Lines[I].Kind != EKind::Show; }

		void Move(int32 D)
		{
			for (int32 I = Row + D; I >= 0 && I < Lines.Num(); I += D)
			{
				if (Lines[I].Kind != EKind::Head) { Row = I; return; }
			}
		}

		void Change(int32 D)
		{
			if (!Lines.IsValidIndex(Row)) { return; }
			FLine& L = Lines[Row];
			if (L.WhyNot && !L.WhyNot().IsEmpty()) { return; }
			if (L.Kind == EKind::Slider && L.Get && L.Set) { L.Set(L.Get() + 0.05f * D); }
			else if (L.Step) { L.Step(D); }
		}

		void Detect()
		{
			UGameUserSettings* S = Gus();
			if (S == nullptr) { return; }
			S->RunHardwareBenchmark();
			S->ApplyHardwareBenchmarkResults();
			S->SaveSettings();
			UE_LOG(LogTemp, Log, TEXT("LedgerSettings: detected for this PC: %s"), *LevelName(PresetOf(S)));
		}

		FSlateColor LineColour(int32 I) const
		{
			const FLine& L = Lines[I];
			if (L.WhyNot && !L.WhyNot().IsEmpty()) { return FSlateColor(Unavailable()); }
			return FSlateColor(I == Row ? Red() : Ink());
		}

		TSharedRef<SWidget> Bar(int32 I)
		{
			return SNew(SBox).WidthOverride(7.0f)[ SNew(SImage).Image(Solid(Red())).Visibility_Lambda([this, I]() { return I == Row ? EVisibility::HitTestInvisible : EVisibility::Hidden; }) ];
		}

		TSharedRef<SWidget> Arrow(const TCHAR* Glyph, int32 I, int32 D)
		{
			return SNew(SBorder).BorderImage(Solid(FLinearColor::Transparent)).Padding(FMargin(10.0f, 0.0f))
				.OnMouseButtonDown_Lambda([this, I, D](const FGeometry&, const FPointerEvent&) { Row = I; Change(D); return FReply::Handled(); })
				.Visibility_Lambda([this, I]() { const FLine& L = Lines[I]; return L.WhyNot && !L.WhyNot().IsEmpty() ? EVisibility::Hidden : EVisibility::Visible; })
				[
					SNew(STextBlock).Text(FText::FromString(Glyph)).Font(Font(EFace::Franklin600, 36)).ColorAndOpacity(FSlateColor(Ink()))
				];
		}

		TSharedRef<SWidget> ValueOf(int32 I)
		{
			const FLine& L = Lines[I];
			if (L.Kind == EKind::Show)
			{
				TSharedRef<SHorizontalBox> Ks = SNew(SHorizontalBox);
				TArray<FString> Parts;
				L.Value().ParseIntoArray(Parts, TEXT(" "));
				for (int32 K = 0; K < Parts.Num(); ++K) { Ks->AddSlot().AutoWidth().Padding(FMargin(K > 0 ? 10.0f : 0.0f, 0.0f, 0.0f, 0.0f))[ Key(Parts[K]) ]; }
				return Ks;
			}
			if (L.Kind == EKind::Slider)
			{
				return SNew(SBorder).BorderImage(Solid(FLinearColor::Transparent)).Padding(0.0f)
					.OnMouseButtonDown_Lambda([this, I](const FGeometry& G, const FPointerEvent& E)
					{
						Row = I;
						const float X = G.AbsoluteToLocal(E.GetScreenSpacePosition()).X / FMath::Max(1.0f, G.GetLocalSize().X);
						if (Lines[I].Set) { Lines[I].Set(X); }
						return FReply::Handled();
					})
					[
						SNew(SBox).WidthOverride(300.0f).HeightOverride(36.0f).VAlign(VAlign_Center)
						[
							SNew(SOverlay)
							+ SOverlay::Slot().VAlign(VAlign_Center)[ SNew(SBox).HeightOverride(4.0f)[ SNew(SImage).Image(Solid(FLinearColor(Ink().R, Ink().G, Ink().B, 0.3f))) ] ]
							+ SOverlay::Slot().VAlign(VAlign_Center).HAlign(HAlign_Left)
							[
								SNew(SBox).HeightOverride(4.0f).WidthOverride_Lambda([this, I]() { return FOptionalSize(300.0f * (Lines[I].Get ? Lines[I].Get() : 0.0f)); })
								[ SNew(SImage).Image_Lambda([this, I]() { return Solid(I == Row ? Red() : Ink()); }) ]
							]
							+ SOverlay::Slot().HAlign(HAlign_Left).VAlign(VAlign_Center)
							[
								SNew(SBox).Padding_Lambda([this, I]() { return FMargin(290.0f * (Lines[I].Get ? Lines[I].Get() : 0.0f), 0.0f, 0.0f, 0.0f); })
								[
									SNew(SBox).WidthOverride(10.0f).HeightOverride(28.0f)[ SNew(SImage).Image_Lambda([this, I]() { return Solid(I == Row ? Red() : Ink()); }) ]
								]
							]
						]
					];
			}
			return SNew(SHorizontalBox)
				+ SHorizontalBox::Slot().AutoWidth().VAlign(VAlign_Center)[ Arrow(TEXT("‹"), I, -1) ]
				+ SHorizontalBox::Slot().AutoWidth().VAlign(VAlign_Center)
				[
					SNew(STextBlock).Text_Lambda([this, I]()
					{
						const FLine& L = Lines[I];
						const FString Why = L.WhyNot ? L.WhyNot() : FString();
						return FText::FromString(!Why.IsEmpty() ? Why : (L.Value ? L.Value() : FString()));
					})
					.Font(Font(EFace::Franklin500, 30)).ColorAndOpacity_Lambda([this, I]() { return LineColour(I); })
				]
				+ SHorizontalBox::Slot().AutoWidth().VAlign(VAlign_Center)[ Arrow(TEXT("›"), I, 1) ];
		}

		// THE QUALITY LINE: its label, then the preset boxes and "Detect for this PC".
		TSharedRef<SWidget> Presets(int32 I)
		{
			TSharedRef<SHorizontalBox> Boxes = SNew(SHorizontalBox);
			for (int32 P = 0; P <= 4; ++P)
			{
				auto Picked = [P]() { const int32 L = PresetOf(Gus()); return P == 4 ? L < 0 : L == P; };
				Boxes->AddSlot().AutoWidth().Padding(FMargin(P > 0 ? 12.0f : 0.0f, 0.0f, 0.0f, 0.0f))
				[
					// in hand: a red ring round the picked one; picked: filled with ink
					SNew(SBorder).BorderImage_Lambda([this, I, Picked]() { return Picked() && I == Row ? Ruled(Red(), 3.0f) : Solid(FLinearColor::Transparent); }).Padding(3.0f)
					.OnMouseButtonDown_Lambda([this, I, P](const FGeometry&, const FPointerEvent&)
					{
						Row = I;
						if (P < 4) { if (UGameUserSettings* S = Gus()) { S->SetOverallScalabilityLevel(P); S->ApplyNonResolutionSettings(); S->SaveSettings(); } }
						return FReply::Handled();
					})
					[
						SNew(SBorder).BorderImage_Lambda([Picked]() { return Picked() ? Solid(Ink()) : Ruled(Ink(), 2.0f); }).Padding(FMargin(14.0f, 4.0f))
						[
							SNew(STextBlock).Text(FText::FromString(LevelName(P == 4 ? -1 : P))).Font(Font(EFace::Franklin600, 30))
							.ColorAndOpacity_Lambda([Picked, P]() { return FSlateColor(Picked() ? Newsprint() : (P == 4 ? Unavailable() : Ink())); })
						]
					]
				];
			}
			Boxes->AddSlot().AutoWidth().VAlign(VAlign_Center).Padding(FMargin(28.0f, 0.0f, 0.0f, 0.0f))
			[
				SNew(SBorder).BorderImage(Solid(FLinearColor::Transparent)).Padding(0.0f)
				.OnMouseButtonDown_Lambda([this, I](const FGeometry&, const FPointerEvent&) { Row = I; Detect(); return FReply::Handled(); })
				[
					SNew(SVerticalBox)
					+ SVerticalBox::Slot().AutoHeight()[ SNew(STextBlock).Text(FText::FromString(TEXT("Detect for this PC"))).Font(Font(EFace::Franklin600, 30)).ColorAndOpacity(FSlateColor(Ink())) ]
					+ SVerticalBox::Slot().AutoHeight()[ Rule(2.0f, Ink()) ]
				]
			];
			return SNew(SVerticalBox)
				+ SVerticalBox::Slot().AutoHeight()
				[
					SNew(STextBlock).Text(FText::FromString(Lines[I].Label)).Font(Font(EFace::Franklin600, 30)).ColorAndOpacity_Lambda([this, I]() { return LineColour(I); })
				]
				+ SVerticalBox::Slot().AutoHeight().Padding(FMargin(0.0f, 10.0f, 0.0f, 6.0f))[ Boxes ];
		}

		void Rebuild()
		{
			switch (Tab)
			{
			case 0: Lines = PictureLines(); break;
			case 1: Lines = SoundLines(); break;
			case 2: Lines = ControlLines(); break;
			default: Lines = ReadingLines(); break;
			}
			if (!Takes(Row)) { Row = -1; Move(1); }
			const FLinearColor Faint(Ink().R, Ink().G, Ink().B, 0.3f);
			TSharedRef<SVerticalBox> Left = SNew(SVerticalBox);
			for (int32 I = 0; I < Lines.Num(); ++I)
			{
				const FLine& L = Lines[I];
				if (L.Kind == EKind::Head)
				{
					Left->AddSlot().AutoHeight().Padding(FMargin(21.0f, 18.0f, 0.0f, 4.0f))
					[
						SNew(STextBlock).Text(FText::FromString(L.Label.ToUpper())).Font(Font(EFace::League, 28, 60)).ColorAndOpacity(FSlateColor(Grey()))
					];
					Left->AddSlot().AutoHeight()[ Rule(1.5f, Faint) ];
					continue;
				}
				TSharedRef<SWidget> Body = L.Kind == EKind::Presets ? Presets(I) :
					StaticCastSharedRef<SWidget>(SNew(SHorizontalBox)
					+ SHorizontalBox::Slot().FillWidth(1.0f).VAlign(VAlign_Center)
					[
						SNew(STextBlock).Text(FText::FromString(L.Label)).Font(Font(EFace::Franklin600, 30)).ColorAndOpacity_Lambda([this, I]() { return LineColour(I); })
					]
					+ SHorizontalBox::Slot().AutoWidth().VAlign(VAlign_Center)[ ValueOf(I) ]);
				Left->AddSlot().AutoHeight()
				[
					SNew(SBorder).BorderImage(Solid(FLinearColor::Transparent)).Padding(0.0f)
					.OnMouseButtonDown_Lambda([this, I](const FGeometry&, const FPointerEvent&) { if (Takes(I)) { Row = I; } return FReply::Unhandled(); })
					[
						SNew(SBox).MinDesiredHeight(56.0f).VAlign(VAlign_Center)
						[
							SNew(SHorizontalBox)
							+ SHorizontalBox::Slot().AutoWidth().Padding(FMargin(0.0f, 8.0f, 14.0f, 8.0f))[ Bar(I) ]
							+ SHorizontalBox::Slot().FillWidth(1.0f).VAlign(VAlign_Center)[ Body ]
						]
					]
				];
				Left->AddSlot().AutoHeight().Padding(FMargin(21.0f, 0.0f, 0.0f, 0.0f))[ Rule(1.5f, Faint) ];
			}
			TSharedRef<SHorizontalBox> Tabs = SNew(SHorizontalBox);
			for (int32 T = 0; T < 4; ++T)
			{
				Tabs->AddSlot().AutoWidth().Padding(FMargin(T > 0 ? 46.0f : 0.0f, 0.0f, 0.0f, 0.0f))
				[
					SNew(SBorder).BorderImage(Solid(FLinearColor::Transparent)).Padding(0.0f)
					.OnMouseButtonDown_Lambda([this, T](const FGeometry&, const FPointerEvent&) { Tab = T; Row = -1; Rebuild(); return FReply::Handled(); })
					[
						SNew(SVerticalBox)
						+ SVerticalBox::Slot().AutoHeight()
						[
							SNew(STextBlock).Text(FText::FromString(kTabs[T])).Font(Font(EFace::Franklin800, 32)).ColorAndOpacity(FSlateColor(T == Tab ? Red() : Grey()))
						]
						+ SVerticalBox::Slot().AutoHeight().Padding(FMargin(0.0f, 4.0f, 0.0f, 0.0f))
						[
							SNew(SBox).HeightOverride(4.0f)[ SNew(SImage).Image(Solid(T == Tab ? Red() : FLinearColor::Transparent)) ]
						]
					]
				];
			}
			TSharedRef<SWidget> Explain = SNew(SVerticalBox)
				+ SVerticalBox::Slot().AutoHeight()
				[
					SNew(STextBlock).Text_Lambda([this]() { return FText::FromString(Lines.IsValidIndex(Row) ? Lines[Row].Label : FString()); })
					.Font(Font(EFace::Franklin800, 34)).ColorAndOpacity(FSlateColor(Ink()))
				]
				+ SVerticalBox::Slot().AutoHeight().Padding(FMargin(0.0f, 12.0f, 0.0f, 0.0f))
				[
					SNew(STextBlock).AutoWrapText(true).LineHeightPercentage(1.12f)
					.Text_Lambda([this]() { return FText::FromString(Lines.IsValidIndex(Row) ? Lines[Row].Explain : FString()); })
					.Font(Font(EFace::Franklin400, 27)).ColorAndOpacity(FSlateColor(Ink()))
				]
				+ SVerticalBox::Slot().AutoHeight().Padding(FMargin(0.0f, 22.0f, 0.0f, 0.0f))
				[
					SNew(STextBlock).AutoWrapText(true).LineHeightPercentage(1.12f)
					.Text_Lambda([this]() { return FText::FromString(Lines.IsValidIndex(Row) ? Lines[Row].Note : FString()); })
					.Font(Font(EFace::OldItalic, 27)).ColorAndOpacity(FSlateColor(Grey()))
				];
			Holder->SetContent(
				SNew(SVerticalBox)
				+ SVerticalBox::Slot().AutoHeight()
				[
					SNew(SBorder).BorderImage(Solid(Red())).Padding(FMargin(44.0f, 10.0f, 44.0f, 8.0f))
					[
						SNew(SHorizontalBox)
						+ SHorizontalBox::Slot().AutoWidth()
						[
							SNew(STextBlock).Text(FText::FromString(TEXT("SETTINGS"))).Font(Font(EFace::League, 58, 30)).ColorAndOpacity(FSlateColor(FLinearColor::White))
						]
						+ SHorizontalBox::Slot().FillWidth(1.0f).HAlign(HAlign_Right).VAlign(VAlign_Bottom).Padding(FMargin(0.0f, 0.0f, 0.0f, 6.0f))
						[
							SNew(STextBlock).Text(FText::FromString(Tab == 0 ? TEXT("The street behind shows each change as you make it.") : TEXT(""))).Font(Font(EFace::OldItalic, 28)).ColorAndOpacity(FSlateColor(FLinearColor::White))
						]
					]
				]
				+ SVerticalBox::Slot().AutoHeight().Padding(FMargin(44.0f, 16.0f, 44.0f, 0.0f))[ Tabs ]
				+ SVerticalBox::Slot().AutoHeight().Padding(FMargin(0.0f, 0.0f, 0.0f, 0.0f))[ Rule(1.5f, Ink()) ]
				+ SVerticalBox::Slot().FillHeight(1.0f)
				[
					SNew(SHorizontalBox)
					+ SHorizontalBox::Slot().FillWidth(1.0f).Padding(FMargin(23.0f, 20.0f, 40.0f, 20.0f))[ Left ]
					+ SHorizontalBox::Slot().AutoWidth()[ SNew(SBox).WidthOverride(1.5f)[ SNew(SImage).Image(Solid(Ink())) ] ]
					+ SHorizontalBox::Slot().AutoWidth().Padding(FMargin(34.0f, 26.0f, 44.0f, 20.0f))[ SNew(SBox).WidthOverride(392.0f)[ Explain ] ]
				]);
		}
	};

	TSharedPtr<SWidget> GRoot;
	TSharedPtr<SSettingsPage> GPage;
	TFunction<void()> GOnClosed;
	TWeakObjectPtr<UWorld> GWorld;
	double GShownAt = 0.0;
}

void Load()
{
	if (bLoaded || GConfig == nullptr) { return; }
	bLoaded = true;
	float Backing = 0.8f;
	GConfig->GetBool(kSection, TEXT("Subtitles"), bSubtitles, GGameUserSettingsIni);
	GConfig->GetInt(kSection, TEXT("SubtitleSize"), GSubtitleSize, GGameUserSettingsIni);
	GConfig->GetFloat(kSection, TEXT("Backing"), Backing, GGameUserSettingsIni);
	GConfig->GetBool(kSection, TEXT("SpeakerNames"), bSpeakerNames, GGameUserSettingsIni);
	GConfig->GetBool(kSection, TEXT("ReduceMotion"), bReduceMotion, GGameUserSettingsIni);
	GConfig->GetBool(kSection, TEXT("SuggestAlways"), bSuggestAlways, GGameUserSettingsIni);
	GConfig->GetFloat(kSection, TEXT("LookSensitivity"), GSensitivity, GGameUserSettingsIni);
	GConfig->GetBool(kSection, TEXT("InvertLook"), bInvertLook, GGameUserSettingsIni);
	GConfig->GetFloat(kSection, TEXT("Master"), GMaster, GGameUserSettingsIni);
	GConfig->GetBool(kSection, TEXT("QuietBehind"), bQuietBehind, GGameUserSettingsIni);
	GConfig->GetFloat(kSection, TEXT("Brightness"), GBrightness, GGameUserSettingsIni);
	SetBackingStrength(Backing);
	SetReduceMotion(bReduceMotion || FParse::Param(FCommandLine::Get(), TEXT("ReduceMotion")));
	ApplySound();
	ApplyBrightness();
}

bool SubtitlesOn() { Load(); return bSubtitles; }
float SubtitleUnits() { Load(); static const float U[4] = { 34.0f, 39.0f, 46.0f, 54.0f }; return U[FMath::Clamp(GSubtitleSize, 0, 3)]; }
bool SpeakerNames() { Load(); return bSpeakerNames; }
bool SuggestAlways() { Load(); return bSuggestAlways; }
float LookSensitivity() { Load(); return GSensitivity; }
bool InvertLook() { Load(); return bInvertLook; }

void Show(UWorld* World, TFunction<void()> OnClosed)
{
	if (GRoot.IsValid() || GEngine == nullptr || GEngine->GameViewport == nullptr) { return; }
	Load();
	GOnClosed = MoveTemp(OnClosed);
	GWorld = World;
	GShownAt = FPlatformTime::Seconds();
	SAssignNew(GPage, SSettingsPage).OnBack_Lambda([]() { Hide(); });
	GRoot = SNew(SBorder).BorderImage(Solid(FLinearColor::Transparent)).Padding(0.0f)
		.ColorAndOpacity_Lambda([]() { const float A = ReduceMotion() ? 1.0f : FMath::Clamp((float)((FPlatformTime::Seconds() - GShownAt) / 0.22), 0.0f, 1.0f); return FLinearColor(1.0f, 1.0f, 1.0f, A); })
		[
			SNew(SOverlay)
			// the street behind, dimmed but not blurred, so each change shows
			+ SOverlay::Slot()[ SNew(SImage).Image(Solid(FLinearColor(0.0f, 0.0f, 0.0f, 0.35f))) ]
			+ SOverlay::Slot()
			[
				SafeRegion(
					SNew(SVerticalBox)
					+ SVerticalBox::Slot().AutoHeight().Padding(FMargin(120.0f, 54.0f, 120.0f, 0.0f))
					[
						SNew(SBox).HeightOverride(866.0f)[ PaperSheet(GPage.ToSharedRef(), FMargin(0.0f)) ]
					]
					+ SVerticalBox::Slot().FillHeight(1.0f)
					+ SVerticalBox::Slot().AutoHeight().Padding(FMargin(120.0f, 0.0f, 120.0f, 54.0f))
					[
						Hints({ MakeTuple(TArray<FString>{ TEXT("↑"), TEXT("↓") }, FString(TEXT("choose"))),
						        MakeTuple(TArray<FString>{ TEXT("←"), TEXT("→") }, FString(TEXT("change"))),
						        MakeTuple(TArray<FString>{ TEXT("Tab") }, FString(TEXT("next section"))),
						        MakeTuple(TArray<FString>{ TEXT("Esc") }, FString(TEXT("back"))) })
					])
			]
		];
	GEngine->GameViewport->AddViewportWidgetContent(GRoot.ToSharedRef(), 220);
	if (UWorld* W = GWorld.Get())
	{
		if (APlayerController* PC = W->GetFirstPlayerController())
		{
			FInputModeUIOnly M;
			M.SetWidgetToFocus(GPage);
			M.SetLockMouseToViewportBehavior(EMouseLockMode::DoNotLock);
			PC->SetInputMode(M);
			PC->SetShowMouseCursor(true);
		}
	}
	FSlateApplication::Get().SetKeyboardFocus(GPage, EFocusCause::SetDirectly);
	UE_LOG(LogTemp, Log, TEXT("LedgerSettings: shown"));
}

void Hide()
{
	if (!GRoot.IsValid()) { return; }
	if (GEngine != nullptr && GEngine->GameViewport != nullptr) { GEngine->GameViewport->RemoveViewportWidgetContent(GRoot.ToSharedRef()); }
	GRoot.Reset();
	GPage.Reset();
	UE_LOG(LogTemp, Log, TEXT("LedgerSettings: closed"));
	TFunction<void()> Done = MoveTemp(GOnClosed);
	GOnClosed = nullptr;
	if (Done) { Done(); }
}

bool IsShown() { return GRoot.IsValid(); }
}
