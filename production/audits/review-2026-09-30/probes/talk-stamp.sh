#!/usr/bin/env bash
# PROOF FOR C1: a Continue whose load is sent under a newer stamp loses every
# conversation, and the next save writes the loss over the good file.
#
# It drives the game's own talk program (ledger/TalkHelper, built by the
# Core's test table) with its stand-in replies (--fake: no model, no key),
# sending exactly the lines the game sends (CrimeProbe.cpp 3977-4005 for a
# reply, 5213-5217 for a save, 4032-4038 for the load after Continue):
#   game 1: Tom tells Darren something; the reply's save goes out as stamp G1.
#   Continue: the game read G1 from clock.txt, but an hourly save before the
#   talk program was ready replaced it with G2 (5193) and sent no talk save
#   (5213); so the load goes out as G2 (4038).
#   The next save goes out as G3.
#
#   bash production/audits/review-2026-09-30/probes/talk-stamp.sh
set -u
REPO=$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../.." && pwd)
DLL="$REPO/ledger/TalkHelper/bin/Release/net8.0/TalkHelper.dll"
[ -f "$DLL" ] || ( cd "$REPO" && dotnet build ledger/TalkHelper -c Release -v q >/dev/null )
WORK=$(mktemp -d "${TMPDIR:-/tmp}/talk-stamp.XXXXXX")
SLOT="$WORK/slot.talk.json"
q() { printf '%s' "$1" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))'; }

echo "[game 1] Tom tells Darren where he was; the save goes out as G1"
printf '%s\n' \
  '{"id":1,"to":"sam","say":"I was at the pictures all night, honest."}' \
  "{\"talk\":\"save\",\"path\":$(q "$SLOT"),\"stamp\":\"G1\"}" \
  | LEDGER_TALK_FAKE=1 dotnet "$DLL" --fake 2>/dev/null | grep -E '"talk"|"id":1' | cut -c1-160
python3 - "$SLOT" <<'EOF'
import json,sys
d=json.load(open(sys.argv[1]))
print("  talk.json: stamp=%s people=%d" % (d.get("stamp"), len(d.get("people",{}))))
EOF

echo "[Continue] the load goes out as G2 (an autosave replaced G1 before the talk program was ready); then the next save, G3"
printf '%s\n' \
  "{\"talk\":\"load\",\"path\":$(q "$SLOT"),\"stamp\":\"G2\"}" \
  '{"id":2,"to":"sam","say":"Where did I say I was?"}' \
  "{\"talk\":\"save\",\"path\":$(q "$SLOT"),\"stamp\":\"G3\"}" \
  | LEDGER_TALK_FAKE=1 dotnet "$DLL" --fake 2>/dev/null | grep -E '"talk"' | cut -c1-160
python3 - "$SLOT" <<'EOF'
import json,sys
d=json.load(open(sys.argv[1]))
people=d.get("people",{})
told=any("pictures" in json.dumps(v) for v in people.values())
print("  talk.json: stamp=%s people=%d; Darren still holds 'the pictures': %s" % (d.get("stamp"), len(people), "yes" if told else "NO"))
print("  => %s" % ("PROVED: the load was refused as stale and the next save wrote the loss over the good file" if not told else "not reproduced"))
EOF
rm -rf "$WORK"
