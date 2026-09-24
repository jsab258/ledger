@echo off
REM  THE WINDOW ENCOUNTER, PLAYABLE, 24 September.
REM  Walk to the shop window by Mickey's and press E. Lena sees you and
REM  shouts. Run off through the yard behind the parade, past Sam, if you
REM  like. Later that week the word has gone round; find Sam in the yard.
REM  To talk to Sam, Lena or Rocco, stand near them and press T, type what
REM  you say and press Enter. Esc, or the window's close button, whenever you
REM  like: the street is saved, and when you come back it still knows.
REM  WASD to walk, the mouse to look, Shift to run.
REM
REM  The conversation uses the real model: your key is read from the game's
REM  own settings into this window only, and never shown.
cd /d "%~dp0..\.."
dotnet build ledger\TalkHelper -c Release -nologo -v q >nul
for /f "usebackq delims=" %%K in (`powershell -NoProfile -Command "(Get-Content -Raw \"$env:USERPROFILE\AppData\LocalLow\DefaultCompany\ledger\secrets.json\" | ConvertFrom-Json).anthropic_api_key"`) do set "ANTHROPIC_API_KEY=%%K"
REM  THE EDITOR'S OWN BUILD, NOT THE STEADY PACKAGED COPY, for now: that copy
REM  lacks the files the build machine lays beside the game for the street's
REM  look, and played from there the street is grey and unfinished - the AI
REM  tester found it, 24 September. Set LEDGER_PLAY_PACKAGED to try it anyway.
set "PACKAGED=%LEDGER_PLAY_PACKAGED%"
set "HELPER=%CD%\ledger\TalkHelper\bin\Release\net8.0\TalkHelper.exe"
REM  THE CAST'S VOICES: the small voice model beside the game, when it is installed.
set "VOICE="
if exist "C:\LedgerTools\chatterbox-nano\env-dml\Scripts\python.exe" set "VOICE=-VoicePython=C:\LedgerTools\chatterbox-nano\env-dml\Scripts\python.exe -VoiceScript=%CD%\tools\voice-live\voice-server.py"
REM  THE STREET'S PIECE LIST AND THE WITNESS LINES GO BESIDE THE GAME, as the
REM  build machine puts them before every run: without them the street is
REM  empty and the screen black - the AI tester found it, 24 September.
set "PACKDIR=C:\Users\Jafar\ledger-migrate\ue-probe\Packaged\Windows\LedgerProbe"
if not defined PACKAGED set "PACKAGED=none"
if exist "%PACKAGED%" (
  copy /y "production\specs\vignette-pieces.json" "%PACKDIR%\vignette-pieces.json" >nul
  copy /y "content\dialogue\crime-witness-v1.json" "%PACKDIR%\crime-witness-v1.json" >nul
  start "" "%PACKAGED%" -LedgerSlice -LedgerCrime -Encounter=live "-LedgerRepo=%CD%" "-TalkHelper=%HELPER%" %VOICE% -windowed -ResX=1600 -ResY=900 %*
) else (
  copy /y "production\specs\vignette-pieces.json" "ue-probe\vignette-pieces.json" >nul
  copy /y "content\dialogue\crime-witness-v1.json" "ue-probe\crime-witness-v1.json" >nul
  start "" "C:\Program Files\Epic Games\UE_5.8\Engine\Binaries\Win64\UnrealEditor.exe" "%CD%\ue-probe\LedgerProbe.uproject" -game -LedgerSlice -LedgerCrime -Encounter=live "-TalkHelper=%HELPER%" %VOICE% -windowed -ResX=1600 -ResY=900 %*
)
