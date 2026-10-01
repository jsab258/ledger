#!/usr/bin/env bash
# Drives the talk program (stand-in replies, --fake: no model, no key) with the
# lines the CURRENT game sends (CrimeProbe.cpp 4318-4372 a line, 6426-6427 a save,
# 4839-4850 the load once ready; stamps per CrimeProbe.h 1835-1844).
set -u
S=/tmp/claude-0/-home-user-ledger/93d6bded-9637-5eca-9014-bd1c8b1ed11e/scratchpad/agent-save
DLL=$S/repo/ledger/TalkHelper/bin/Release/net8.0/TalkHelper.dll
W=$S/talkwork; rm -rf $W; mkdir -p $W
SLOT=$W/game.talk.json
run() { LEDGER_TALK_FAKE=1 dotnet "$DLL" --fake --early --pending --cards $S/repo/production/cast/cards 2>/dev/null; }
pick() { python3 -c '
import json,sys
for l in sys.stdin:
    l=l.strip()
    if not l.startswith("{"): continue
    d=json.loads(l)
    if "ready" in d or "cost" in d or "usd" in d: continue
    keep={k:d[k] for k in ("id","to","talk","people","stale","missing","error","reply","refusedAsk","weekAnswer") if k in d and d[k] is not None}
    if "reply" in keep: keep["reply"]=keep["reply"][:70]
    print("   ", json.dumps(keep))'; }
holds() { python3 - "$SLOT" "$1" <<'PY'
import json,sys
d=json.load(open(sys.argv[1])); t=json.dumps(d.get("people",{}))
print("   file: stamp=%s people=%d; holds %r: %s" % (d.get("stamp"), len(d.get("people",{})), sys.argv[2], sys.argv[2] in t))
PY
}
echo "== 1. C1 under the current rules =="
echo " session 1: Tom tells Darren he was at the pictures; the reply's save: fresh stamp G1"
printf '%s\n' \
 '{"id":1,"to":"sam","who":"sam","say":"I was at the pictures all night, honest.","day":0,"hour":14,"minute":50,"fresh":true}' \
 "{\"talk\":\"save\",\"path\":\"$SLOT\",\"stamp\":\"G1\"}" | run | pick
holds pictures
echo " session 2 (Continue): an hourly save before the talk program is ready keeps G1 and sends no talk save;"
echo "  ready -> load G1; next save G2"
printf '%s\n' \
 "{\"talk\":\"load\",\"path\":\"$SLOT\",\"stamp\":\"G1\"}" \
 "{\"talk\":\"save\",\"path\":\"$SLOT\",\"stamp\":\"G2\"}" | run | pick
holds pictures

echo "== 2. Ron's own question pending across a Continue (C5) =="
echo " straight:"
printf '%s\n' \
 '{"id":1,"to":"rocco","who":"rocco","say":"Tell them no, Ron.","day":1,"hour":22,"minute":40,"fresh":true,"ask":{"tonight":true}}' \
 '{"id":2,"to":"rocco","who":"rocco","say":"Yes.","day":1,"hour":22,"minute":48,"ask":{"tonight":true}}' | run | pick
echo " with the 23:00 autosave between and a Continue (the game marks the first line after Continue fresh: GLive.Talked is empty):"
printf '%s\n' \
 '{"id":1,"to":"rocco","who":"rocco","say":"Tell them no, Ron.","day":1,"hour":22,"minute":40,"fresh":true,"ask":{"tonight":true}}' \
 "{\"talk\":\"save\",\"path\":\"$SLOT\",\"stamp\":\"G3\"}" | run | pick
printf '%s\n' \
 "{\"talk\":\"load\",\"path\":\"$SLOT\",\"stamp\":\"G3\"}" \
 '{"id":1,"to":"rocco","who":"rocco","say":"Yes.","day":1,"hour":23,"minute":2,"fresh":true,"ask":{"tonight":true}}' | run | pick
echo " (and even without fresh):"
printf '%s\n' \
 "{\"talk\":\"load\",\"path\":\"$SLOT\",\"stamp\":\"G3\"}" \
 '{"id":1,"to":"rocco","who":"rocco","say":"Yes.","day":1,"hour":23,"minute":2,"ask":{"tonight":true}}' | run | pick

echo "== 3. Sheila's plain question pending across a Continue (C5) =="
echo " straight:"
printf '%s\n' \
 '{"id":1,"to":"lena","who":"lena","say":"Morning, Sheila.","day":6,"hour":10,"minute":30,"fresh":true,"week":{"ask":true,"realBook":true,"dayOff":true}}' \
 '{"id":2,"to":"lena","who":"lena","say":"I am taking it over.","day":6,"hour":10,"minute":40,"week":{"stands":true,"realBook":true}}' \
 '{"id":3,"to":"lena","who":"lena","say":"Yes.","day":6,"hour":10,"minute":50,"week":{"stands":true,"realBook":true}}' | run | pick
echo " with the 11:00 autosave between and a Continue:"
printf '%s\n' \
 '{"id":1,"to":"lena","who":"lena","say":"Morning, Sheila.","day":6,"hour":10,"minute":30,"fresh":true,"week":{"ask":true,"realBook":true,"dayOff":true}}' \
 '{"id":2,"to":"lena","who":"lena","say":"I am taking it over.","day":6,"hour":10,"minute":50,"week":{"stands":true,"realBook":true}}' \
 "{\"talk\":\"save\",\"path\":\"$SLOT\",\"stamp\":\"G4\"}" | run | pick
printf '%s\n' \
 "{\"talk\":\"load\",\"path\":\"$SLOT\",\"stamp\":\"G4\"}" \
 '{"id":1,"to":"lena","who":"lena","say":"Yes.","day":6,"hour":11,"minute":2,"fresh":true,"week":{"stands":true,"realBook":true}}' | run | pick

echo "== 4. A talk save that fails removes the good file; the game has already written the new stamp =="
printf '%s\n' \
 '{"id":1,"to":"sam","who":"sam","say":"I was at the pictures all night, honest.","day":0,"hour":14,"minute":50,"fresh":true}' \
 "{\"talk\":\"save\",\"path\":\"$SLOT\",\"stamp\":\"G5\"}" | run | pick
holds pictures
mkdir "$SLOT.tmp"   # stands in for a .tmp the program cannot write (a lock, a scanner)
printf '%s\n' \
 "{\"talk\":\"load\",\"path\":\"$SLOT\",\"stamp\":\"G5\"}" \
 "{\"talk\":\"save\",\"path\":\"$SLOT\",\"stamp\":\"G6\"}" | run | pick
echo "   slot file exists after the failed save: $( [ -f $SLOT ] && echo yes || echo NO)"
rmdir "$SLOT.tmp"
echo " Continue with clock.txt's G6:"
printf '%s\n' "{\"talk\":\"load\",\"path\":\"$SLOT\",\"stamp\":\"G6\"}" | run | pick
