// With -LedgerNNECpu on the command line, unregister ONNX Runtime's DirectML runtime after
// engine start, so MetaHuman's body tracker (OfflineBodyTracker.cpp: DirectML first, CPU
// second, no setting) finds no GPU runtime and builds every network on NNERuntimeORTCpu.
// Without the flag it does nothing. Changes nothing outside this process (n09-8, 10 Nov 2026:
// DirectML failed on this card at the first inference, 887A0020 then 887A0005).
#include "Misc/CommandLine.h"
#include "Misc/Parse.h"
#include "Modules/ModuleManager.h"
#include "NNE.h"
#include "NNERuntimeGPU.h"

class FNNECpuSwitchModule : public IModuleInterface
{
public:
	virtual void StartupModule() override
	{
		if (!FParse::Param(FCommandLine::Get(), TEXT("LedgerNNECpu")))
		{
			UE_LOG(LogTemp, Display, TEXT("NNECPUSWITCH off (no -LedgerNNECpu)"));
			return;
		}
		TWeakInterfacePtr<INNERuntime> Dml = UE::NNE::GetRuntime(TEXT("NNERuntimeORTDml"));
		if (!Dml.IsValid())
		{
			UE_LOG(LogTemp, Display, TEXT("NNECPUSWITCH NNERuntimeORTDml not registered; nothing to do"));
		}
		else
		{
			const UE::NNE::EUnregisterRuntimeStatus Status = UE::NNE::UnregisterRuntime(Dml);
			UE_LOG(LogTemp, Display, TEXT("NNECPUSWITCH unregister NNERuntimeORTDml: %s"),
				Status == UE::NNE::EResultStatus::Ok ? TEXT("ok") : TEXT("FAILED"));
		}
		const TArray<FString> Gpu = UE::NNE::GetAllRuntimeNames<INNERuntimeGPU>();
		UE_LOG(LogTemp, Display, TEXT("NNECPUSWITCH GPU runtimes left: %d (%s)"), Gpu.Num(), *FString::Join(Gpu, TEXT(",")));
	}
};

IMPLEMENT_MODULE(FNNECpuSwitchModule, NNECpuSwitch)
