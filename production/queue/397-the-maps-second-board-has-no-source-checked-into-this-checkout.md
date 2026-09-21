line: instruments (tools/map.py, the game's areas as tiles; extends D38)
spec: Jafar, 2026-09-21 ("THE CLEANUPS"): "The map's second board, from the
  asset audit's eighty-four categories, same five areas and three
  colours, so a missing content category is a tile rather than a
  conversation. Extend the standing rule: anything that produces a new
  kind of asset gets a tile before the work starts."

  THE FIRST BOARD, for comparison, verified at filing time: tools/map.py's
  existing heatmap (HEAT_START/HEAT_END, around line 2156) draws "every
  system a tile in five areas coloured exists, partial or absent," sourced
  ONLY from production/systems-inventory.json per D38's typing rules, with
  no second source and no fallback: "An absent or unparseable file refuses
  the block in words." The second board should follow the same discipline
  (one named source, refuse rather than invent when it is missing)
  against a DIFFERENT source, an asset audit rather than the systems
  inventory.

  THE SOURCE NAMED, "the asset audit's eighty-four categories," IS NOT IN
  THIS CHECKOUT. Checked at filing time: no file under this tree names an
  asset audit, 84 categories, or matches on asset-audit or "asset audit"
  (grepped, case-insensitive, whole tree; the only hits are this week's
  own order documents and unrelated substrings such as tools/clip-reach.py
  and a code comment in NameTags.cs). Given every other research delivery
  this week has turned out to live on one of the 48 unmerged research/*
  branches, the likeliest location is among those; queue 394, the
  research corpus consolidation, pulls SUMMARY.md, RECHECK.md and BRIEF.md
  from each onto main, which is the point at which an asset audit
  delivery, if that is what this is, would first become readable here.

  DO NOT INVENT THE 84 CATEGORIES. If queue 394 has landed and the source
  still cannot be found by name on main or among the still-unmerged
  branches (`git branch -r` after a full fetch), that is a blocker: report
  what was searched and stop, rather than typing 84 categories from
  memory or from systems-inventory.json's own, different, entry count.
acceptance: the asset audit's source document is located, named, with its
  path or branch, before any board is drawn; the second board renders the
  same five areas and three colours as the first, sourced only from that
  document, with the same refuse-rather-than-invent behaviour on a
  missing or unparseable source, tested both ways, the accepting case
  with the real source present and a rejecting case with the source
  absent, per the instruments rule that a guard is tested on the case it
  should pass and a case where the fault it checks can actually happen;
  D38 is extended, its own file or a successor entry states the new rule,
  "anything that produces a new kind of asset gets a tile before the work
  starts"; and if the source cannot be located, the item stops and
  reports exactly what was searched rather than shipping an invented
  board
max_sessions: 2
status: BLOCKED 2026-09-21 on locating the asset audit source, which is
  not present in this checkout as of filing, checked by grep, whole tree,
  reported above. Likely unblocks once queue 394 lands a matching research
  branch onto main; check main first, then the still-unmerged branch
  list, before concluding it truly does not exist anywhere reachable.
