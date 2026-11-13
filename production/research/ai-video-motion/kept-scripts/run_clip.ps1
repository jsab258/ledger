# One clip of the motion experiment, its prompt and negative read from inputs\<motion>.prompt.txt and .neg.txt,
# so every seed of a motion runs on the same words (9 Nov: the 1101 record left the prompt out).
# Usage (-Start "" for text only): pwsh run_clip.ps1 -Motion m2 -Start inputs/tom-backdrop-480x832.png -W 480 -H 832 -Frames 81 -Seed 2202
param([string]$Motion, [string]$Start, [int]$W, [int]$H, [int]$Frames, [int]$Seed, [double]$Shift = 5)
Set-Location $PSScriptRoot
$prompt = (Get-Content "inputs\$Motion.prompt.txt" -Raw).Trim()
$neg = (Get-Content "inputs\$Motion.neg.txt" -Raw).Trim()
$name = "$Motion-${Frames}f-s$Seed"
$a = @('-M','vid_gen','--diffusion-model','models/Wan2.2-TI2V-5B-Q8_0.gguf','--vae','models/wan2.2_vae.safetensors',
  '--t5xxl','models/umt5-xxl-encoder-Q8_0.gguf','-p',"`"$prompt`"",'-n',"`"$neg`"",'-W',"$W",'-H',"$H",
  '--video-frames',"$Frames",'--fps','24','--cfg-scale','6','--sampling-method','euler','--steps','20','--flow-shift',"$Shift",
  '--offload-to-cpu','--flash-attn','off,diffusion=on','--vae-tiling','--temporal-tiling','--seed',"$Seed",'-o',"out/$name.webm")
# No start frame (-Start ""): text to video (10 Nov: motions 3 and 1 have no start frame from the game yet).
if ($Start) { $a = @('-i', $Start) + $a } else { $name = "$name-t2v"; $a[-1] = "out/$name.webm" }
"sd-cli.exe $($a -join ' ')" | Set-Content "out\$name.cmd.txt"
$t = Get-Date
$p = Start-Process -FilePath sdcpp\sd\sd-cli.exe -ArgumentList $a -RedirectStandardOutput "out\$name.log" -RedirectStandardError "out\$name.err" -NoNewWindow -PassThru -Wait
"exit=$($p.ExitCode) seconds=$([int]((Get-Date)-$t).TotalSeconds) out=out\$name.webm exists=$(Test-Path "out\$name.webm")"
