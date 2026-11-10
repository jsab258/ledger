using UnrealBuildTool;

public class NNECpuSwitch : ModuleRules
{
	public NNECpuSwitch(ReadOnlyTargetRules Target) : base(Target)
	{
		PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;
		PrivateDependencyModuleNames.AddRange(new string[] { "Core", "CoreUObject", "Engine", "NNE" });
	}
}
