line: instruments (production/throughput.md; the readings it quotes come from
  tools/ue/import_prop_meshes.py and the walk build's propsAsMesh key)
spec: the throughput ledger's planning unit is the VERIFIED PIECE, and its own
  definition at throughput.md:3-4 says only when a piece counts, never what one
  IS. The W36/W37 prop row then counts 22, and the two readings it quotes for
  that 22 are not the same quantity:

      propImported=15/16 propSaved=15/16     (run 3, 7f12005)  DISTINCT MESHES
      propsAsMesh=22/23 propStandIns=1/23    (run 33, 76e4238) PLACEMENTS

  22 is the PLACEMENT count. Fifteen meshes were imported; some are placed more
  than once, and the row's own sentence "Twenty-two pieces are verified" turns a
  placement tally into a manufacturing tally without saying so. The same 22 is
  the denominator of "cost per verified piece" at throughput.md:19 and :68, so
  a cost that should be divided by at most 15 is divided by 22 and reads about
  a third cheap. The W37 row already shows the two units pulling apart in its
  own words, "2 assets in 17 placements", and still counts the line in pieces.

  THIS IS NOT AN ARITHMETIC SLIP TO PATCH. Two numbers derived from one
  pipeline are being read as one number (rule 2), and the planning unit of the
  whole production system is the thing that is undefined.
acceptance: either (a) throughput.md defines a piece in one sentence at the
  head, every row states which unit its count is in, and the cost line's
  denominator names its unit and is recomputed; or (b) the file says plainly
  that the number CANNOT EXIST YET, prints the words "nothing measured" in the
  pieces column, and names exactly what would produce it. Not a third thing,
  and not both halves left implied. Whichever is chosen, the two readings above
  are printed beside the count so a reader can see which one it is.
max_sessions: 1
status: READY 2026-09-16, and RE-ORDERED BY JAFAR THE SAME EVENING as the
  FIRST HALF OF A PAIR. His words: "Fix what a piece means in the throughput
  ledger, since twenty-two rows came from fifteen meshes and the cost divides
  by the wrong number. Then measure one real unit properly."

  THE SECOND HALF IS QUEUE 362 AND THIS ITEM GATES IT, in his own order.
  362 puts one fully authored resident through all five stations with both
  meters read before and after, then a second, to get a cost and a first
  marginal from real work. THOSE TWO NUMBERS ARE COSTS PER UNIT. If the unit
  is still undefined when they are taken, they join exactly the confusion this
  item exists to end, and the measurement is wasted rather than merely
  imprecise. Define the unit, then measure it.

  Originally raised by Jafar from an external audit and filed
  under his ruling of the same day: an audit finding is FILED and the standing
  order resumes. DO NOT START before the visual slice lands.

  HIS WORDS: "the throughput ledger counts 22 placements from 15 imported
  meshes as 22 verified pieces. Fix what a piece means or say plainly that the
  number cannot exist yet and what would produce it."

  VERIFIED AT THE SOURCE 2026-09-16, not taken from the audit: the strings
  above are quoted from production/throughput.md lines 3, 10, 11, 17 and 68.
  The 15 and the 22 are both in line 10, four sentences apart.

  WHAT THIS ITEM DOES NOT CLAIM. It does not say 22 is wrong. It says nothing
  in the file lets a reader tell whether it is 22 pieces or 22 placements, and
  a planning unit that cannot be told apart from a placement cannot plan.
