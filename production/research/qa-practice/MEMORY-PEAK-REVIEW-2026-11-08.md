# Review: card-memory peak in slice-perf.py and perf-hook.py (8 Nov 2026)

Reviewed: uncommitted diff of tools/slice-perf.py and tools/perf-hook.py against QA-FIRST-STEPS-2026-11-08.md step 3. Read-only; both self-tests run.

## Verdict: PASS WITH FIXES (one small fix, two optional notes; nothing blocks)

## What was checked and found right
- Self-tests: slice-perf 12/12, perf-hook 9/9. Step 3's four cases (rise to 6,100 then 5,500; all 5,000 UNDER; no column absent; old cases) are covered.
- Real file packaged-day-walk--3b3454e-sun.csv: slice-perf gives gpuMemMB=5843 (median 5,842.5), gpuMemPeakMB=6127, settled 6127, memLine=5650, OVER-LINE. perf-hook gives gpuMemMB 5842.5, gpuMemPeakMB 6126.5 (raw max 6126.5039 recounted by hand). Matches the expectation.
- Old fields: old slice-perf (HEAD, copied to scratch) prints the identical line to the new one up to the old fields (frames=1500, median 10.83, p99 21.51, gpuMemMB=5843). The new fields are appended after target=..., so a reader of the old prefix is unchanged. The workflow step (yml line 2128) only redirects the whole line to a file; no parser found. perf-hook json keeps every key; gpuMemPeakMB is added after gpuMemMB; --table appends its column last. p1-packaged.ps1 line 126 joins the json whole.
- Metadata-row exclusion: in all 62 CSVs in p1-packaged the only rows whose first cell starts with "[" is the single closing "[HasHeaderRowAtEnd]" row (88 cells; its GPUMem column cell is 1794111057). Frame rows start with an empty cell; the full header row starts with "EVENTS". No real frame row can be dropped by the test.
- Other CSVs (slice-perf): day-stand 3b3454e-sun median 5,209 / peak 5,209 UNDER; hair-forced-cards (900 frames) 5,583 / 5,583 UNDER; hair-strands night 5,607 UNDER; day-walk (plain) 5,545 median, peak 5,863 OVER-LINE; the walks of 3641d53 and 7bef7cf (rate01 to rate20, nomap, lazy, novoice) all median 5,814 to 5,860, peak 6,104 to 6,163, OVER-LINE.

## Findings

1. (fix, small) tools/perf-hook.py line 124: `out =[" | ".join(keys)]` lost its space (`out = [`). Cosmetic, but the change introduced it. Fix: `out = [" | ".join(keys)]`.

2. (optional) tools/perf-hook.py lines 116-117: the column is read three times in one expression. Fix: compute `mem = column(header, body, "GPUMem/LocalUsedMB")` once at the top of summarise and use `med(mem)` and `round(max(mem), 1) if mem else None`. Values unchanged.

3. (note, old fields not changed in kind) tools/slice-perf.py line 74 onward: the old reader included the metadata row in the memory list, so gpuMemMB (a median) was taken over 1,501 values and now over 1,500. On the 3b3454e capture the printed value is the same (5843); on another capture it could differ by at most half a sample step. Frame and GPU columns were not affected (the row's cells there are non-numeric). Worth one line in the commit message; no code change.

4. (note, existing weakness the peak inherits) tools/slice-perf.py read() takes columns by rows[0]'s header; perf-hook.py reads against the full header written at the file's end (its comment, 7 Oct). On this capture both give the same column (peak 6,126.5 either way), but a capture where the memory column first appears late or sits at a different index would read "absent" or a wrong column in slice-perf only. memVerdict=absent says so; it does not fail, as specified. No fix asked now.

5. (note) tools/slice-perf.py line() returns NO-FRAMES with no memory fields when the settled frame list is empty (a capture of 300 frames or fewer). The peak over all frames exists but is not printed. Acceptable for the build machine's 1,800-frame captures; fix only if short captures are expected: in `line`, before the NO-FRAMES return, append `mem_peak(mem_all, mem)` when `mem_all` is non-empty.

6. (note, spec) The line does not say "at Highest" in itself; step 3 says the label carries it, and the docstring says so. Fine as specified.
