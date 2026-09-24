using UnrealBuildTool;

public class LedgerProbe : ModuleRules
{
	public LedgerProbe(ReadOnlyTargetRules Target) : base(Target)
	{
		PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;
		// PRECISE FLOATING POINT, 23 September. Unreal builds a Game target
		// with /fp:fast by default, which lets the compiler regroup
		// arithmetic; an independent check of the reaction ladder's port found
		// the packaged game computing ((0.35*c)*2.0)*0.4 as c*(0.7*0.4) and
		// answering Confronts where the C# answers Refuses (12 in 841,183
		// random inputs). The ported Core must give the C#'s answer, so the
		// module is built precise, as the golden check already compiles it.
		FPSemantics = FPSemanticsMode.Precise;
		// A game module's minimum. Every dependency beyond these is time
		// added to every cycle this project exists to measure.
		PublicDependencyModuleNames.AddRange(new string[] { "Core", "CoreUObject", "Engine" });
		// ImageWrapper DECODES THE STILL THIS PROBE COMMITS, and it is the
		// difference between a measurement and a file-exists check. Task 007
		// step 2 has to prove a frame is not blank, which means reading its
		// pixels back out of the artifact that will be committed rather than
		// trusting that a call returned. Private, because nothing outside
		// this module needs it, and named here so the cost of the extra
		// module is visible in the build numbers D1 is comparing.
		//
		// InputCore NAMES FKey AND EKeys, which ALedgerCharacter binds
		// directly to (queue 138 item 1: the street's first playable
		// character). Engine almost certainly carries this already as a
		// transitive public dependency, but this project cannot compile
		// locally to prove that, so it is named explicitly rather than
		// trusted through a chain nobody here can see.
		//
		// ApplicationCore NAMES THE DEFAULT INPUT DEVICE, added 2026-09-22
		// with the act. The crime is committed by a key press now, and the
		// crime probe sends that press through the player controller's own
		// InputKey, which wants the FInputDeviceId the platform considers
		// default. IPlatformInputDeviceMapper is that answer and it lives
		// here. The alternative was to type the device's internal id as 0
		// and hope, which is the kind of guess this project's whole method
		// exists to avoid - and it would have failed silently, as a press
		// that arrives nowhere, which is the one failure shape the act gate
		// cannot tell from a broken binding.
		//
		// WHAT IT COSTS, measured on this machine the same day rather than
		// estimated: a cold build, cook and package of this project is 4.3
		// minutes and a warm one is under a minute, both with this module in.
		PrivateDependencyModuleNames.AddRange(new string[] { "ImageWrapper", "InputCore", "ApplicationCore" });
		// AnimGraphRuntime AND AnimationCore, 23 September, for the heads that
		// turn toward the player (Jafar: "use what Unreal provides"). The
		// turn is the engine's own Look At node (FAnimNode_LookAt, in
		// AnimGraphRuntime) with its aim solver and axis type (AnimationCore),
		// run in a native animation instance because this project makes no
		// Blueprint assets.
		PrivateDependencyModuleNames.AddRange(new string[] { "AnimGraphRuntime", "AnimationCore" });
		// AudioMixer, 23 September: the engine's own output recorder, so the
		// walk's sound is committed as a recording anyone can listen to.
		PrivateDependencyModuleNames.Add("AudioMixer");
		// RHI, 24 September: the card's own frame time (RHIGetGPUFrameCycles)
		// and texture memory, for what each MetaHuman costs (MetaHumanCost.cpp).
		PrivateDependencyModuleNames.Add("RHI");
		// Slate, 24 September: the line the player types what they say into.
		PrivateDependencyModuleNames.AddRange(new string[] { "Slate", "SlateCore" });
		// NavigationSystem, 23 September: the slice's navigation mesh, built
		// at run time around invokers, and the path query that proves it.
		PrivateDependencyModuleNames.Add("NavigationSystem");
		// EXCEPTIONS OFF, AND THIS WAS PRE-RULED BEFORE THE BUILD THAT
		// NEEDED IT. A director reading the Core port on 2026-09-08 found
		// that Suspicion.h throws and CoreGolden.h compiles a try/catch into
		// a module that does not enable exceptions, and ruled the answer in
		// advance: compile the FactNull branch out and print
		// perceptionUnknownFns=4/FactNull-needs-exceptions, NEVER set
		// bEnableExceptions. The build then failed exactly there, with
		// "CoreGolden.h(834,4): error C4530: C++ exception handler used, but
		// unwind semantics are not enabled", and this line is the ruled fix
		// rather than a reaction to it.
		//
		// WHAT IT COSTS, so nobody reads a smaller number as a regression:
		// the four FactNull rows stop being answered and count as Unknown,
		// which the run says in words. Turning exceptions on instead would
		// change a compile setting for the whole module to keep four rows,
		// which is the trade the director refused.
		PublicDefinitions.Add("LEDGER_CORE_NO_EXCEPTIONS=1");
	}
}
