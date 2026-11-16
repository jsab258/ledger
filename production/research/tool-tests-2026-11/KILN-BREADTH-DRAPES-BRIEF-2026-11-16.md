# Kiln breadth drapes: helper brief (16 November 2026)

Method researched: KILN-ROUND10-REPORT-2026-11-16.md (how round 10 ran and judged jobs); advisor 182 item 1 (rounds and judging in helpers, a short verdict back). Game items unblocked: n16-2 (Ron's donkey jacket and work trousers), n16-1 (Sheila out of the white layer; Darren's nylon jacket), M5.

## Task

Run four existing job scripts on Kiln, one at a time, then judge each with the existing judge script, and hand back only a short verdict.

Jobs (already written; do not edit them):
1. F:/LedgerTools/garments/ron/kiln-outfit-2026-11-16/donkey_jacket_job.py
2. F:/LedgerTools/garments/ron/kiln-outfit-2026-11-16/work_trousers_job.py
3. F:/LedgerTools/garments/sheila/kiln-breadth-2026-11-16/pleated_skirt_job.py
4. F:/LedgerTools/garments/darren/kiln-breadth-2026-11-16/nylon_jacket_job.py

Run: `KILN_ENGINE=drapestudio python F:/LedgerTools/tool-dev/kiln/python/run_job_script.py JOB.py F:/LedgerTools/tool-dev/runs/kiln-breadth-2026-11-16/<name>.result.json` (copy the exact environment and judge call from F:/LedgerTools/tool-dev/runs/kiln-r10-after1, its run script or logs, and the round 10 report). Before each job: `python C:/Users/Jafar/ledger-local/tools/retention.py space --job "kiln breadth <name>" --drives CF`; stop on anything but GO. Output cap 1 GB for the whole folder.

Judge each export with the same drape_check_any call round 10 used; the jacket over a garment uses layer_check only if the job names an under garment.

## Hand back (under 200 words)

Per job: ok or failed (with the error's last line), seconds, the judge's counts (body through over 1 mm, cloth inside over 1/3 mm, inner over 1.2x, worst stretch and piece), the export path. Then the folder's size. Write the same in F:/LedgerTools/tool-dev/reports/KILN-BREADTH-DRAPES-2026-11-16.md, ending "Special cases: none" if true and "M7: 0".

## Limits

No clicks, keys or computer use; never stop, start or kill a process other than the jobs you start; do not open Marvelous or Unreal; write nothing under F:/LedgerTools/tool-dev/judge/; edit no job, engine or judge code (a failed job is reported, not fixed); no Rust builds.
