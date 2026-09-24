"""Every VCTK speaker's gender, accent, age and region, read from the corpus's
parquet footers and only the row groups where a new speaker begins, with the
audio column never touched. Writes vctk-inventory.json beside this file.

The first version streamed every row's metadata over HTTP and read audio
blocks along the way; it ran out its fifteen minutes and wrote nothing."""
import json, pathlib
import pyarrow.parquet as pq, huggingface_hub as hub, fsspec
REPO = "CSTR-Edinburgh/vctk"
COLS = ["speaker_id", "age", "gender", "accent", "region"]
files = sorted(f for f in hub.list_repo_files(REPO, repo_type="dataset", revision="refs/convert/parquet") if f.endswith(".parquet"))
fs = fsspec.filesystem("http")
sp, where = {}, {}
for f in files:
    u = hub.hf_hub_url(REPO, f, repo_type="dataset", revision="refs/convert/parquet")
    pf = pq.ParquetFile(fs.open(u, block_size=65536, cache_type="none"))
    md = pf.metadata
    j = pf.schema_arrow.names.index("speaker_id")
    for i in range(md.num_row_groups):
        st = md.row_group(i).column(j).statistics
        lo, hi = str(st.min), str(st.max)
        if lo in sp and hi in sp:
            continue
        t = pf.read_row_group(i, columns=COLS).to_pylist()
        for r in t:
            s = str(r["speaker_id"])
            if s not in sp:
                sp[s] = {c: str(r[c]) for c in COLS[1:]}
                where[s] = [f, i]
    print(f, len(sp), flush=True)
out = pathlib.Path(__file__).with_name("vctk-inventory.json")
out.write_text(json.dumps({"speakers": dict(sorted(sp.items())), "first_row_group": where}, indent=1), encoding="utf-8")
print(len(sp), "speakers ->", out)
