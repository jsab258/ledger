// HEADS THAT TURN, 23 September, for Jafar's presentable checklist: "people
// turn their head to look at you when you move near them... Use what Unreal
// provides rather than building our own."
//
// UNREAL'S OWN LOOK AT NODE, NOT OURS. Each person's animation runs through
// the engine's standard nodes in a native animation instance - their loop in
// a sequence player, then FAnimNode_LookAt on the head bone with its aim
// solver, clamp and easing - because this project makes no Blueprint assets
// and the engine lets a native instance supply its own node graph. What is
// ours is only the decision: until 29 September, when the player was within
// 5 m and in front of the person, the look faded in; otherwise it faded out.
//
// THE LOOK A PERSON GIVES HIM, 29 September (town list 1; the gaze research,
// production/research/gaze-and-knowing): not every head within 5 m alike. A
// stranger glances at about ten metres for half a second and looks away by
// 2.4 m; somebody who half remembers a story about him glances the same way,
// then looks again as he comes past; somebody watching him keeps him in view
// from further off and looks back after he has gone by. The numbers are
// StreetVoice::RegardFor's, set by the street for each person who holds a
// story (SetRegard) and a stranger's for everybody else. Always the head.
//
// The automation's shots never look (a head turned to the lens is not a
// street photograph, and a frame must repeat); the playable street does.
#pragma once

#include "CoreMinimal.h"
#include "Animation/AnimInstance.h"
#include "PersonAnim.generated.h"

class UAnimSequenceBase;

UCLASS(transient)
class ULedgerPersonAnim : public UAnimInstance
{
	GENERATED_BODY()

public:
	// The loop, where in it to start, how fast it plays (0 holds it), and
	// whether this person looks at the player. Finds the head bone and its
	// facing on the mesh; the caller reinitialises the instance after.
	void Setup(UAnimSequenceBase* InSequence, float InStartSeconds, float InPlayRate, bool bInLook);

	virtual void NativeUpdateAnimation(float DeltaSeconds) override;

	UPROPERTY(Transient)
	TObjectPtr<UAnimSequenceBase> Sequence;

	float StartSeconds = 0.0f;
	float PlayRate = 1.0f;
	bool bLook = false;

	// THE HEAD, found on the mesh: its bone, and which of its local axes point
	// forward and up in the reference pose.
	FName HeadBone;
	FVector HeadLookAxis = FVector(0.0, 1.0, 0.0);
	FVector HeadUpAxis = FVector(0.0, 0.0, 1.0);

	// THE IDLE'S OWN HEAD TURNS, DAMPED (29 September, the look clips' blind
	// review): Epic's MetaHuman idle looks about by itself, at the same moments
	// in every run, so a stranger and somebody who knows looked alike. The two
	// neck bones and the head are held this much toward their rest rotation
	// before the look is applied; a little of the idle's life stays.
	static constexpr int32 CalmBones = 3;
	FName CalmBone[CalmBones];
	FRotator CalmRest[CalmBones];
	static constexpr float CalmAlpha = 0.7f;

	// WHAT THE NODE IS GIVEN each frame, on the game thread.
	float LookAlpha = 0.0f;
	// What the turn eases toward: itself eased toward the look wanted, so a
	// turn starts slowly, runs and settles, as a head does.
	float LookDrive = 0.0f;
	FVector LookTarget = FVector::ZeroVector;
	// THE MOST THIS PERSON HAS LOOKED this run, for the verdict.
	float PeakAlpha = 0.0f;

	// HOW THIS PERSON LOOKS AT HIM, from a Regard (StreetVoice.h), in metres
	// and seconds as it gives them; a first look that holds is infinity, held
	// while he is within its distance.
	void SetRegard(double InFirstLookMetres, double InFirstLookSeconds, double InSecondLookMetres,
	               double InSecondLookSeconds, double InLookAwayMetres, bool bInLooksBack);
	float FirstLookCm = 1000.0f;
	float FirstLookSeconds = 0.5f;
	// How far a stranger's glance turns the head, of the whole way: a glance
	// is a small turn; the knowing look, the watching look and the look back
	// turn it fully.
	static constexpr float GlanceStrength = 0.6f;
	float Strength = 1.0f;
	float SecondLookCm = 0.0f;
	float SecondLookSeconds = 0.0f;
	float LookAwayCm = 240.0f;
	bool bLooksBack = false;

	// THE LOOK AS IT GOES: given yet, how long the one under way has left, and
	// whether he has been in front of them since he came near.
	bool bFirstGiven = false;
	bool bSecondGiven = false;
	bool bWasInFront = false;
	bool bLookingBack = false;
	float LookLeft = 0.0f;
	// how many of each this person has given this run, for the verdict
	int32 FirstLooks = 0;
	int32 SecondLooks = 0;
	int32 LooksBackGiven = 0;

	// IN FRONT: a person does not turn right round to look at somebody behind
	// them, unless they are watching him (the look back).
	static constexpr float LookConeDeg = 100.0f;
	// Once he is this much further off than their first look reaches, the look
	// starts over: he can come past again.
	static constexpr float LookResetCm = 500.0f;

	// A NOISE THEY TURN TO, 29 September (the twenty a friend would notice,
	// 16: people turn toward the smash): after a short start the head turns
	// to where it came from for this long, whoever they were looking at, then
	// goes back to its own business.
	void LookToward(const FVector& Where, float DelaySeconds, float Seconds);

	// THE MOUTH WHILE THEY SPEAK, 30 September (the twenty a friend would
	// notice, 12: lips roughly in time). Each frame the game says how loud
	// the voice being heard is (0 to 1) and whether they are speaking; the
	// face's own mouth controls follow it, blended over the idle, so a face
	// opens and closes with its words and rests again after. A first step:
	// Epic's streaming speech solver, in the engine, is the next
	// (production/research/lip-sync/NOTE-2026-09-30.md).
	void SpeakTick(float Level, bool bSpeaking, float DeltaSeconds);

	// A LINE MADE IN ADVANCE SAID WITH ITS OWN FACE (item 4, 1 October; Jafar's
	// list: "mouths from Epic's audio-driven animation for every line made in
	// advance"). Epic's MetaHuman Animator made the face from the line's own
	// sound in the editor (tools/ue/speech_faces.py); its mouth's curves (jaw,
	// lips, teeth, tongue) are read at the line's time each frame and laid over
	// the idle and the loudness mouth, faded in over a tenth of a second and out
	// over a quarter when it ends or the answer cuts it off; the eyes and brows
	// stay the idle's. Speech made in play keeps
	// the loudness mouth (SpeakTick) until Epic's streaming solver is in.
	void SayMadeLine(UAnimSequenceBase* InFace);
	void EndMadeLine();
	void SaidTick(float DeltaSeconds);
	UPROPERTY(Transient)
	TObjectPtr<UAnimSequenceBase> SaidFace;
	float SaidTime = 0.0f;
	float SaidWeight = 0.0f;
	bool bSaidEnding = false;
	TMap<FName, float> SaidCurves;

	// A WALK BETWEEN TWO POINTS, 30 September (the twenty a friend would
	// notice, 13: everyone stood still). Set before InitAnim: the walk clip is
	// blended in while the owner moves from A to B and back at SpeedCms, with
	// a pause of PauseMin to PauseMax seconds at each end, turned to where it
	// goes (YawOffset: the mesh's own turn against the street's yaw); it waits
	// while the player stands in its way.
	void SetupWalk(UAnimSequenceBase* InWalk, const FVector& InA, const FVector& InB, float InSpeedCms,
	               float InPauseMin, float InPauseMax, float InYawOffset);
	UPROPERTY(Transient)
	TObjectPtr<UAnimSequenceBase> WalkSequence;
	FVector WalkA = FVector::ZeroVector, WalkB = FVector::ZeroVector;
	float WalkSpeedCms = 120.0f, PauseMin = 3.0f, PauseMax = 8.0f, WalkYawOffset = 0.0f;
	float WalkWeight = 0.0f, PauseLeft = 0.0f;
	bool bToB = true;
	int32 WalkLegs = 0;
	static constexpr int32 MouthCurveCount = 11;
	static constexpr const TCHAR* MouthCurves[MouthCurveCount] = {
		TEXT("CTRL_expressions_jawOpen"),
		TEXT("CTRL_expressions_mouthLipsTogetherUL"), TEXT("CTRL_expressions_mouthLipsTogetherUR"),
		TEXT("CTRL_expressions_mouthLipsTogetherDL"), TEXT("CTRL_expressions_mouthLipsTogetherDR"),
		TEXT("CTRL_expressions_mouthFunnelUL"), TEXT("CTRL_expressions_mouthFunnelUR"),
		TEXT("CTRL_expressions_mouthFunnelDL"), TEXT("CTRL_expressions_mouthFunnelDR"),
		TEXT("CTRL_expressions_mouthStretchL"), TEXT("CTRL_expressions_mouthStretchR") };
	float MouthValues[MouthCurveCount] = {};
	float SpeakLevel = 0.0f;
	float SpeakWeight = 0.0f;
	float SpeakClock = 0.0f;
	FVector NoisePoint = FVector::ZeroVector;
	float NoiseDelay = 0.0f;
	float NoiseLeft = 0.0f;
	int32 NoiseLooks = 0;

protected:
	virtual FAnimInstanceProxy* CreateAnimInstanceProxy() override;
};
