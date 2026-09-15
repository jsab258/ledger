line: instrument (tools/map.py, the board Jafar judges by)
spec: The typed status board's tally sentence is DERIVED from the tile counts
  and NOTHING READS IT BACK. The judgement line beside it is guarded
  (check_typed_attribution parses it with JUDGE_LINE_RX, compares number and
  denominator against the run's own count, and refuses a page where it claims
  every tile, drops its denominator, or is deleted), and the tally sentence
  has no equivalent. A page could print a tally that disagrees with the tiles
  it sits above and every check would pass.
  AND THE FOURTH STATUS IS EXERCISED ONLY BY THE LIVE PAGE. map.py's selftest
  plants NO ruled-out tile: a grep for ruledout, ruled-out or the mark finds
  nothing in the test fixtures. So the one accepting case for the mark, the
  class and the legend word is today's real inventory, and the day the last
  ruled-out tile is retyped the drawing code goes unexercised without anything
  saying so. Ruled not blocking on 2026-09-15 because the live page IS an
  accepting case today; filed because it stops being one the moment the data
  changes.
acceptance: a check parses the hNow sentence with a regex anchored on
  heat_counts_words' own shape, compares all four numbers AND the total
  against counts, and prints them as tallyOnPage=.../counted=... TWO
  REJECTING FIXTURES, ACCEPTING FIRST ON THE LIVE PAGE: the ruled-out clause
  deleted with its 4 folded into absent (40 absent, no ruled-out clause, tiles
  unchanged), and "4 ruled-out" reading "0 ruled-out" with the four tiles
  still drawn. PLUS one planted inventory fixture carrying a single ruled-out
  tile for check_heatmap, asserting the mark, the class h-ruledout and the
  legend word, so the fourth status has a synthetic accepting case that does
  not depend on the data.
max_sessions: 1
status: READY 2026-09-15, filed by the D38 ruling of 19:43Z, which found it
  while reading the page rather than while looking for it. NO NEW INSTRUMENT:
  this adds checks to map.py's existing 38, and his standing rule does not
  bite.
