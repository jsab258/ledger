#!/bin/bash
# WHAT THE CONTAINER CAN AND CANNOT REACH, measured rather than recalled.
#
#   bash egress-probe.sh --probe     # today's status for every host on the list
#   bash egress-probe.sh --extract   # the cited-host census, from the branches
#   bash egress-probe.sh --reason    # the proxy's own refusal log, verbatim
#   bash egress-probe.sh --selftest  # both outcomes, accepting case first
#
# WHY IT EXISTS. Thirty-eight research topics cited search-engine summaries
# instead of pages, and every delivery said so as a caveat. A caveat is not a
# list, and the person who can change the allowlist needed a list. This is the
# instrument that produced it, shipped so the answer can be re-derived rather
# than believed.
#
# 000 IS NOT A ZERO, IT IS AN ABSENCE OF AN ANSWER. curl prints 000 when the
# transport never produced an HTTP response at all. Here that means the proxy
# gateway rejected the CONNECT, so there is no status code to report, and the
# reason lives in the proxy's own log rather than in the response. --reason is
# where it comes from, and --probe alone cannot tell "refused" from "offline".
# Read the two together.
#
# THE ACCEPTING CASE IS THE HALF THAT GOES UNRUN (CLAUDE.md rule 5b), so
# --selftest runs it first: a host on the proxy's noProxy bypass MUST answer
# 200, and a host that cannot exist MUST answer 000. A probe that reports 000
# for everything, including a reachable host, is measuring its own curl
# invocation and not the network.
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LIST="$HERE/hosts-probed.txt"
TIMEOUT=15

probe_one() {   # echoes the HTTP code, or 000 for no answer. $1 is host[/path].
  curl -sS -o /dev/null -L --max-time "$TIMEOUT" -w '%{http_code}' "https://$1" 2>/dev/null | tail -c 3
}

# A BARE HOST IS THE WRONG PROBE FOR SOME ORIGINS AND IT BIT HERE.
# raw.githubusercontent.com answers 400 to `/` and 200 to a real file path, so
# a bare-host sweep filed a fully reachable host under "other code". The list
# therefore carries an optional path per host, and a host whose reachability
# depends on the path MUST carry one. Reported so the next reader does not
# repeat the fault: the first run of this tool made it.

cmd_probe() {
  local n=0 reach=0 refused=0 other=0
  echo "# egress probe, $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "# statistic: ONE reading per host, taken now. Not a median, not a peak."
  echo
  while read -r h; do
    case "$h" in ''|'#'*) continue;; esac
    n=$((n+1))
    target="${h// //}"            # "host /some/path" -> "host/some/path"
    code=$(probe_one "${target:-$h}")
    printf '%-34s %s\n' "$h" "$code"
    case "$code" in
      000) refused=$((refused+1));;
      2*|3*) reach=$((reach+1));;
      *) other=$((other+1));;
    esac
  done < "$LIST"
  echo
  echo "hosts examined: $n   answered 2xx/3xx: $reach   no answer (000): $refused   other code: $other"
  if [ "$n" -eq 0 ]; then echo "nothing measured: $LIST held no host lines"; fi
  return 0
}

cmd_extract() {
  local branches files
  branches=$(git branch --format='%(refname:short)' | grep -c '^research/' || true)
  echo "# cited-host census over the research lane"
  echo "# branches examined: $branches"
  files=0
  for b in $(git branch --format='%(refname:short)' | grep '^research/'); do
    for f in $(git ls-tree -r --name-only "$b" production/research/ 2>/dev/null); do
      files=$((files+1)); git show "$b:$f" 2>/dev/null
    done
  done > /tmp/egress-corpus.$$ 
  echo "# delivery files read: $files (duplicates across branches included, on purpose:"
  echo "#   a host cited twice in two branches is still one host in the output)"
  grep -oE 'https?://[A-Za-z0-9.-]+' /tmp/egress-corpus.$$ \
    | sed -E 's#https?://##' | tr 'A-Z' 'a-z' | sort | uniq -c | sort -rn
  echo "# distinct hosts: $(grep -oE 'https?://[A-Za-z0-9.-]+' /tmp/egress-corpus.$$ | sed -E 's#https?://##' | tr 'A-Z' 'a-z' | sort -u | wc -l)"
  rm -f /tmp/egress-corpus.$$
}

cmd_reason() {
  echo "# the proxy's own account of why, verbatim. It keeps RECENT failures"
  echo "# only, so this is this session's attempts and not the whole history."
  curl -sS --max-time 20 "${HTTPS_PROXY:-}/__agentproxy/status" 2>&1 | python3 -c '
import json, sys
try:
    d = json.load(sys.stdin)
except Exception as e:
    print("could not read the proxy status: %s" % e); raise SystemExit(0)
rf = d.get("recentRelayFailures") or []
print("noProxy (these BYPASS the gateway entirely):")
for h in (d.get("noProxy") or "").split(","):
    print("   " + h)
print()
print("relay failures recorded: %d" % len(rf))
if not rf:
    print("  nothing measured: no failure is recorded in this proxy instance yet")
seen = {}
for e in rf:
    seen.setdefault((e.get("kind"), e.get("detail")), []).append(e.get("host"))
for (k, det), hs in seen.items():
    print("  kind=%s" % k)
    print("  detail: %s" % det)
    hosts = sorted(set(hs))
    for h in hosts[:40]:
        print("     " + h)
    if len(hosts) > 40:
        print("     (+%d more not shown)" % (len(hosts) - 40))
'
}

cmd_selftest() {
  local fails=0
  echo "ACCEPTING CASE FIRST."
  c=$(probe_one "pypi.org")
  if [ "$c" = "200" ]; then echo "  PASS  pypi.org answered 200 (it is on the proxy's noProxy bypass)"
  else echo "  FAIL  pypi.org answered $c, expected 200. The probe is measuring itself, not the network."; fails=$((fails+1)); fi
  echo "REJECTING CASE."
  c=$(probe_one "example.invalid")
  if [ "$c" = "000" ]; then echo "  PASS  example.invalid answered 000 (no host, so no HTTP answer)"
  else echo "  FAIL  example.invalid answered $c, expected 000."; fails=$((fails+1)); fi
  echo
  echo "egress-probe selftest: 2 checks, $fails failed"
  return $fails
}

case "${1:---probe}" in
  --probe)    cmd_probe;;
  --extract)  cmd_extract;;
  --reason)   cmd_reason;;
  --selftest) cmd_selftest;;
  *) echo "unknown flag: $1. Known: --probe --extract --reason --selftest" >&2; exit 2;;
esac
