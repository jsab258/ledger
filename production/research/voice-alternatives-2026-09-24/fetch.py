"""The first dozen recordings of each speaker on the listening page, from the
row group of the corpus where that speaker begins (about 15 MB each), saved as
wav outside the repository. VCTK, CC BY 4.0 (CSTR, University of Edinburgh).

    python fetch.py OUTDIR"""
import io, json, pathlib, sys
import pyarrow.parquet as pq, huggingface_hub as hub, fsspec, soundfile as sf
REPO = "CSTR-Edinburgh/vctk"
HERE = pathlib.Path(__file__).parent
PAGE = json.loads((HERE / "page.json").read_text(encoding="utf-8"))
out = pathlib.Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
inv = json.loads((HERE / "vctk-inventory.json").read_text(encoding="utf-8"))
want = sorted({s for c in PAGE["characters"] for s in [c["current"]] + c["alternatives"]})
fs = fsspec.filesystem("http")
index = {}
for s in want:
    f, i = inv["first_row_group"][s]
    u = hub.hf_hub_url(REPO, f, repo_type="dataset", revision="refs/convert/parquet")
    pf = pq.ParquetFile(fs.open(u, block_size=1 << 20, cache_type="none"))
    rows = []
    for g in (i, i + 1):
        if g >= pf.metadata.num_row_groups or len(rows) >= 12:
            break
        rows += [r for r in pf.read_row_group(g, columns=["speaker_id", "audio", "text", "text_id"]).to_pylist()
                 if str(r["speaker_id"]) == s]
    rows = rows[:12]
    index[s] = []
    for r in rows:
        a, sr = sf.read(io.BytesIO(r["audio"]["bytes"]))
        name = "%s_%s.wav" % (s, r["text_id"])
        sf.write(out / name, a, sr)
        index[s].append({"file": name, "text_id": r["text_id"], "text": r["text"], "seconds": round(len(a) / sr, 2)})
    print(s, len(rows), "recordings", flush=True)
(out / "index.json").write_text(json.dumps(index, indent=1), encoding="utf-8")
