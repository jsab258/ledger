# Start Blender ready for the live connection (the "blender" MCP server).
#
#   pwsh tools/blender-live/start-blender-live.ps1
#
# WHY, 28 September (Jafar: "Connect Blender live through an MCP connection,
# for this week's street clutter"). The official Blender Lab MCP add-on
# (production/research/blender-mcp) runs inside Blender 5.1 or newer and
# listens on localhost:9876; Claude Code's "blender" server (registered for
# this project, loaded when a session starts) talks to it. The add-on starts
# its listener only when Blender's online access is allowed, so Blender is
# started with --online-mode, for this run only: no saved setting changes.
# The portable Blender 5.2.2 on drive F keeps its own settings beside it and
# leaves the 4.5 the scripts use alone. Prints when the port answers.
$blender = "F:\LedgerTools\blender52\blender-5.2.2-windows-x64\blender.exe"
if (-not (Test-Path $blender)) { "No Blender 5.2 at $blender"; exit 1 }
$running = $false
try { $c = New-Object System.Net.Sockets.TcpClient; $c.Connect("127.0.0.1", 9876); $c.Close(); $running = $true } catch {}
if ($running) { "Blender live: already listening on 9876"; exit 0 }
$p = Start-Process -FilePath $blender -ArgumentList '--online-mode' -PassThru
foreach ($i in 1..60) {
    Start-Sleep -Seconds 1
    try { $c = New-Object System.Net.Sockets.TcpClient; $c.Connect("127.0.0.1", 9876); $c.Close(); "Blender live: listening on 9876 (pid $($p.Id))"; exit 0 } catch {}
}
"Blender started (pid $($p.Id)) but port 9876 did not answer within a minute: check the MCP add-on's preferences"
exit 1
