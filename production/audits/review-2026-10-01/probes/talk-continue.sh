#!/usr/bin/env bash
# RECHECK OF C1 (1 October): the conversation kept across a Continue, through
# the game's own talk program (ledger/TalkHelper, built by the Core's test
# table) with its stand-in replies (--fake: no model, no key), sending the
# lines the game now sends:
#   - the file is the game's TalkSaveFile(), "game.talk.json" (CrimeProbe.h);
#   - a save sends a talk save, under a new stamp, only when
#     TalkSavedWithThisSave(started, ready, load still pending) is true;
#     otherwise the clock file keeps the stamp it had (CrimeProbe.cpp 6399-6427);
#   - Continue loads under the clock file's stamp once the program is ready (4839-4850).
# Case 1 is the review's: talk at 14:57 (G1); Continue; the 15:00 autosave
# comes before the talk program is ready (no talk save, the stamp stays G1);
# the load; the next save (G3).
# Case 2 is the same, but the talk save sent with G2 never lands (the game
# is closed before the talk program has written it): the clock file says G2.
# Case 3: the old name, "talk.json", which the talk program refuses.
#
#   bash production/audits/review-2026-10-01/probes/talk-continue.sh
set -u
REPO=$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../.." && pwd)
DLL="$REPO/ledger/TalkHelper/bin/Release/net8.0/TalkHelper.dll"
[ -f "$DLL" ] || ( cd "$REPO" && dotnet build ledger/TalkHelper -c Release -v q >/dev/null )
WORK=$(mktemp -d "${TMPDIR:-/tmp}/talk-continue.XXXXXX")
SLOT="$WORK/game.talk.json"
q() { printf '%s' "$1" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))'; }
talk() { LEDGER_TALK_FAKE=1 dotnet "$DLL" --fake 2>/dev/null | grep -E '"talk"' | cut -c1-160; }
holds() {
python3 - "$SLOT" "$1" <<'EOF'
import json,sys
d=json.load(open(sys.argv[1]))
people=d.get("people",{})
told=any("pictures" in json.dumps(v) for v in people.values())
print("  %s: stamp=%s people=%d; Darren still holds 'the pictures': %s" % (sys.argv[2], d.get("stamp"), len(people), "yes" if told else "NO"))
EOF
}

echo "[case 1] game 1: Tom tells Darren where he was; the 14:57 save sends the talk under G1"
printf '%s\n' '{"id":1,"to":"sam","say":"I was at the pictures all night, honest."}' \
  "{\"talk\":\"save\",\"path\":$(q "$SLOT"),\"stamp\":\"G1\"}" | talk
holds "game.talk.json"
echo "  Continue: the 15:00 autosave comes before the program is ready: no talk save, the clock file keeps G1"
echo "  the program ready: the load goes out under G1; then a word with Darren; the next save under G3"
printf '%s\n' "{\"talk\":\"load\",\"path\":$(q "$SLOT"),\"stamp\":\"G1\"}" \
  '{"id":2,"to":"sam","say":"Where did I say I was?"}' \
  "{\"talk\":\"save\",\"path\":$(q "$SLOT"),\"stamp\":\"G3\"}" | talk
holds "after the next save"

echo "[case 2] as case 1 to G1; then a save with the program ready sends G2, and the game is closed before the program writes it"
rm -f "$SLOT"
printf '%s\n' '{"id":1,"to":"sam","say":"I was at the pictures all night, honest."}' \
  "{\"talk\":\"save\",\"path\":$(q "$SLOT"),\"stamp\":\"G1\"}" | talk
echo "  Continue: the clock file says G2; the load goes out under G2; then the next save under G3"
printf '%s\n' "{\"talk\":\"load\",\"path\":$(q "$SLOT"),\"stamp\":\"G2\"}" \
  '{"id":2,"to":"sam","say":"Where did I say I was?"}' \
  "{\"talk\":\"save\",\"path\":$(q "$SLOT"),\"stamp\":\"G3\"}" | talk
holds "after the next save"

echo "[case 3] the 30 September name, talk.json"
printf '%s\n' "{\"talk\":\"save\",\"path\":$(q "$WORK/talk.json"),\"stamp\":\"G1\"}" | talk
rm -rf "$WORK"
