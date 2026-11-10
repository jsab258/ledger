using UnrealBuildTool;

public class MocapSolveEditorTarget : TargetRules
{
	public MocapSolveEditorTarget(TargetInfo Target) : base(Target)
	{
		Type = TargetType.Editor;
		DefaultBuildSettings = BuildSettingsVersion.Latest;
		IncludeOrderVersion = EngineIncludeOrderVersion.Latest;
		ExtraModuleNames.Add("NNECpuSwitch");
	}
}
