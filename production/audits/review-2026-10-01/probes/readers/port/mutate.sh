#!/bin/bash
S=/tmp/claude-0/-home-user-ledger/93d6bded-9637-5eca-9014-bd1c8b1ed11e/scratchpad/agent-port
cd $S
name=$1; file=$2; line=$3; expr=$4
D=$S/mut/$name; rm -rf $D; mkdir -p $D; cp -r ue-probe/Source/LedgerProbe/Public $D/Public
sed -i "${line}s${expr}" $D/Public/$file
if cmp -s $D/Public/$file ue-probe/Source/LedgerProbe/Public/$file; then echo "$name: SED-NOCHANGE"; exit; fi
g++ -std=c++11 -O1 -w -I $D/Public -I ue-probe/tests/unreal-shim -o $D/t ue-probe/tests/core-port-test.cpp ue-probe/Source/LedgerProbe/Private/Perception.cpp 2>$D/err || { echo "$name: COMPILE-FAIL $(head -3 $D/err)"; exit; }
out=$($D/t fresh.txt 2>&1 | tail -1)
echo "$name: $out"
