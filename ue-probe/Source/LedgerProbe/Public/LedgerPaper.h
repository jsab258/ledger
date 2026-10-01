// THE EVENING PAPER, 1 October: the interface Jafar approved, built as drawn
// (production/design/ui: STYLE-GUIDE.md, step2/kit.html, the screens in
// step2/pictures). This is its kit: the guide's colours, its type, the
// newsprint, and the parts every screen is made from, in every state.
//
// HOW IT IS SIZED. Everything is laid out in the guide's units, 1080 tall:
// the engine scales the game's screens by height (the default DPI curve,
// shortest side, 1080 = 1.0), so on Jafar's 3440 by 1440 screen every unit
// is drawn a third larger, and SafeRegion() keeps whatever is read or acted
// on inside the centred 16:9 (1920 by 1080 units) of a wide screen. Slate
// draws a font of size S at S x 96 / 72 pixels (FontConstants::RenderDPI),
// so Font() takes the guide's units, which are the em size in pixels at
// 1080, and passes three quarters of them.
//
// Slate, like the rest of the game's screens, since this project makes no
// widget assets: the fonts are files staged with the game's data
// (production/fonts/evening-paper, tools/ui/make_font_cuts.py), the paper a
// picture beside them (production/art/ui, tools/ui/make_paper.py).
#pragma once

#include "CoreMinimal.h"
#include "Fonts/SlateFontInfo.h"
#include "Input/Reply.h"
#include "Layout/Margin.h"
#include "Styling/SlateBrush.h"
#include "Types/SlateEnums.h"
#include "Widgets/DeclarativeSyntaxSupport.h"
#include "Widgets/SCompoundWidget.h"

class SWidget;

namespace LedgerPaper
{
	// The guide's colours (Colour): the hex values, as the engine's colours.
	FLinearColor Newsprint();
	FLinearColor Ink();
	FLinearColor Red();
	FLinearColor Grey();
	FLinearColor Unavailable();
	FLinearColor OnDark();
	// The backing behind subtitles, prompts and the typed name: #10100F at the
	// player's strength (0 to 1, 80% unless he changes it).
	FLinearColor Backing();
	void SetBackingStrength(float A);
	float BackingStrength();

	enum class EFace : uint8
	{
		Franklin400, Franklin450, Franklin500, Franklin600, Franklin700, Franklin800, FranklinItalic,
		League,         // League Gothic: bands, ears, small heads; capitals
		Masthead,       // UnifrakturMaguntia: the game's name only
		Old,            // Old Standard TT: datelines
		OldItalic       // Old Standard TT italic: notes, captions
	};
	// A face at a size in the guide's units; LetterSpacing in thousandths of an em.
	FSlateFontInfo Font(EFace Face, float Units, int32 LetterSpacing = 0);
	// Whether the font files were found (the log says where they were looked for).
	bool FontsFound();

	// The repository root the fonts and the paper are read from: -LedgerRepo,
	// the checkout around the project, or the game's own staged copy.
	FString Root();

	// Brushes, made once and kept.
	const FSlateBrush* Sheet();          // the newsprint, tiled
	const FSlateBrush* SheetEdge();      // its yellowing towards the edges, stretched over a sheet
	const FSlateBrush* Solid(const FLinearColor& C);
	const FSlateBrush* Ruled(const FLinearColor& C, float Thickness);   // an outline, for keys and boxes
	// The reader's coupon's dashed edge (production/art/ui/coupon-dash.png), repeating along any length.
	const FSlateBrush* CouponEdge();
	// A picture beside the fonts (production/art/ui/...), drawn at Size units; null when missing.
	const FSlateBrush* Picture(const FString& Rel, const FVector2D& Size);

	// THE SAFE REGION: the centred 1920 by 1080 units; the content is placed in it.
	TSharedRef<SWidget> SafeRegion(TSharedRef<SWidget> Content, EHorizontalAlignment H = HAlign_Fill, EVerticalAlignment V = VAlign_Fill);
	// A sheet of newsprint with its edges and a soft shadow under it.
	TSharedRef<SWidget> PaperSheet(TSharedRef<SWidget> Content, const FMargin& Padding);
	// A rule across, of ink (or any colour).
	TSharedRef<SWidget> Rule(float Thickness, const FLinearColor& C);
	// A band: League Gothic capitals, white on red.
	TSharedRef<SWidget> Band(const FString& Text, float Units, const FMargin& Padding);
	// An ear: a small box beside the masthead, ink filled or ruled.
	TSharedRef<SWidget> Ear(const FString& Text, bool bFilled);
	// A key in its ruled box (Libre Franklin 700 at 30), on newsprint over the street.
	TSharedRef<SWidget> Key(const FString& Label);
	// A controller's button: round, ruled in ink; "+" is the pad's cross.
	TSharedRef<SWidget> PadButton(const FString& Label);
	// Whether the player is on a controller now (his last input): prompts and hints draw its buttons.
	bool PadInUse();
	void SetPadInUse(bool bPad);
	// A row of key hints: each item its keys ("pad:A" for a controller's button), then what they do (Libre Franklin 500 at 30).
	TSharedRef<SWidget> Hints(const TArray<TPair<TArray<FString>, FString>>& Items);
	// Light words on the backing (subtitles, prompts).
	TSharedRef<SWidget> OnBacking(TSharedRef<SWidget> Content, const FMargin& Padding);

	// How long things take to appear and go (the guide's table), and Reduce motion.
	bool ReduceMotion();
	void SetReduceMotion(bool bOn);
}

// A CHOICE, as the guide draws it: ink when it waits; in hand, red with a red
// bar at its left; pressed, the bar widens and the row tints red for 120 ms;
// unavailable, grey, with a line saying why. In hand means the keys are on it,
// or the mouse is over it. Up and down move between choices (Slate's own
// navigation between focusable widgets); Enter or a click takes it.
class SPaperChoice : public SCompoundWidget
{
public:
	SLATE_BEGIN_ARGS(SPaperChoice) : _Units(48.0f), _RowHeight(84.0f), _Enabled(true) {}
		SLATE_ATTRIBUTE(FString, Text)
		SLATE_ATTRIBUTE(FString, Note)          // under the choice, italic: where and when, or why not
		SLATE_ARGUMENT(float, Units)            // the choice's size
		SLATE_ARGUMENT(float, RowHeight)
		SLATE_ATTRIBUTE(bool, Enabled)
		SLATE_EVENT(FSimpleDelegate, OnChosen)
	SLATE_END_ARGS()

	void Construct(const FArguments& InArgs);
	virtual bool SupportsKeyboardFocus() const override { return true; }
	// No engine focus outline: the choice in hand shows itself, red with its bar.
	virtual const FSlateBrush* GetFocusBrush() const override { return nullptr; }
	virtual FReply OnKeyDown(const FGeometry& MyGeometry, const FKeyEvent& InKeyEvent) override;
	virtual FReply OnMouseButtonDown(const FGeometry& MyGeometry, const FPointerEvent& MouseEvent) override;
	virtual FReply OnMouseButtonUp(const FGeometry& MyGeometry, const FPointerEvent& MouseEvent) override;
	virtual void OnMouseEnter(const FGeometry& MyGeometry, const FPointerEvent& MouseEvent) override;
	virtual FReply OnFocusReceived(const FGeometry& MyGeometry, const FFocusEvent& InFocusEvent) override;
	virtual void OnFocusLost(const FFocusEvent& InFocusEvent) override;

	bool InHand() const;
	void Take();

private:
	TAttribute<FString> Text, Note;
	TAttribute<bool> Enabled;
	FSimpleDelegate OnChosen;
	double PressedAt = -1.0;
	double InHandSince = -1.0;
	float BarWidth() const;
	FSlateColor TextColour() const;
};
