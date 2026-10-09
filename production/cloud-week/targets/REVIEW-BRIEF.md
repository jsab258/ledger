# The brief every target reviewer gets (cloud week 42)

You test one family's exact target against its sources before anything is built to it. You did not write it and will not build it. The target is in production/cloud-week/targets/<family>/ (TARGET.md, target.json, target_drawing.py, self_check.py), its photographs' previews in production/previews/cloud-week/refs/<family>/, and the writer's brief in production/cloud-week/targets/BRIEF.md: read the brief first, it is what the target was asked to be.

Why this step exists: on 8 October the lab's front door was built exactly to its target and passed every automatic check, then failed two fresh reviews on mouldings, door furniture and frame edges that the target never wrote down, and on three places where the target followed the books against its own photographs. Half of those faults could have been caught here, before building.

## What you do

1. Open every photograph the target used, at its source page where you can reach it (the previews are reduced copies), and read its licence and date there.
2. Go element by element through each photograph (the overall form; every part; edges: square, rounded or chamfered and by how much; mouldings and profiles; joints and seams; fixings; furniture and fittings; base, root, cap and finial; how it meets the ground or wall; paint, finish and colour; typical wear) and for each say: in the target with a number or a profile / in the target in words only (not enough for a script) / missing / contradicted.
3. Check the photographs-win rule element by element: wherever the target follows a book, standard or drawing, does a photograph show otherwise?
4. Re-run self_check.py and target_drawing.py (/home/user/.bpyenv/bin/python); look at the drawing laid on the main photograph; check a few numbers against their stated sources yourself, picked where an error would show most from the street.
5. Check the rules: only sources reached; free licences for photographs; nothing NoAI; no real brand, cypher, crown, council name or maker's mark; the period (Britain, 1990, an old port quarter, not heritage-restored, not modern replacement stock).
6. Check that a script could build every part from target.json alone, and that the checks listed in target.json would catch the faults that matter from the street.

## What you hand over

production/cloud-week/targets/<family>/TARGET-REVIEW.md: first line PASS or FAIL. Then the faults, worst first, each with the photograph and the place in it, and the exact amendment (the number, profile or words to add or change). Then what is right. Jafar's ruling of 9 October: a piece or target failing only on narrow points (a small detail with an exact fix) is a PASS, with those points listed for the builder. PASS only when nothing a reviewer of the built piece would see from the street or close up is missing or contradicted; narrow points may be listed under PASS as notes. Do not edit the target yourself. Do not commit or push. About 20 to 30 minutes. Reply with PASS or FAIL and the number of faults.
