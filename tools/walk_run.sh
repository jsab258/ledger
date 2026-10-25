#!/bin/bash
# one walk measure in the game (not packaged): $1 tag, the rest extra switches
TAG=$1; shift
export MSYS_NO_PATHCONV=1
UE="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/Win64/UnrealEditor.exe"
P="C:/Users/Jafar/ledger-local/ue-probe/LedgerProbe.uproject"
until ! tasklist | grep -qi "UnrealEditor.exe\|LedgerProbe.exe\|Runner.Worker"; do sleep 5; done
rm -f /c/Users/Jafar/ledger-local/ue-probe/Saved/Logs/tom-walk.txt
timeout 600 "$UE" "$P" -game -LedgerSlice -LedgerCrime -Encounter=live -LiveFresh -TalkFake -NoTitle -windowed -ResX=1280 -ResY=720 -unattended -nosplash -nopause -LedgerRepo=C:/Users/Jafar/ledger-local -TomWalkProof -TomWalkProofExit "$@" -log=walk-$TAG.log > /dev/null 2>&1
until ! tasklist | grep -qi "UnrealEditor.exe"; do sleep 2; done
mkdir -p F:/LedgerTools/scratch/walk
cp /c/Users/Jafar/ledger-local/ue-probe/Saved/Logs/tom-walk.txt F:/LedgerTools/scratch/walk/tom-walk-$TAG.txt 2>/dev/null
head -1 F:/LedgerTools/scratch/walk/tom-walk-$TAG.txt 2>/dev/null || echo "no result"
grep -h "LedgerWalk\|ledgerTomWalk" /c/Users/Jafar/ledger-local/ue-probe/Saved/Logs/walk-$TAG.log | cut -c1-260 | head -8
