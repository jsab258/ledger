#!/bin/sh
# The fast path of tools/page_read_hook.py: Python takes about a second to start on
# this PC, too long for every tool call. The stamp file's time is the older of the
# two reads, so while it is under 45 minutes old and this call is no page read, nothing
# can be due and Python is never started. Not yet switched on: .claude/settings.json
# still calls the Python directly (the permission check refused the change, 5 Nov).
root="${CLAUDE_PROJECT_DIR:-.}"
input=$(cat)
case "$input" in
  *ArtifactData*) ;;
  *) [ -n "$(find "$root/.claude/page-read-stamp.json" -mmin -45 2>/dev/null)" ] && exit 0 ;;
esac
printf '%s' "$input" | python "$root/tools/page_read_hook.py"
exit 0
