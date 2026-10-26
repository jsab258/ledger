#!/usr/bin/env python3
"""Train a small open checker (KR Labs' TinyLettuce) on Gemini's labelled first sentences.

    C:/LedgerTools/chatterbox-nano/env-dml/Scripts/python.exe tools/checkers/train_checker.py TRAIN.json OUT_DIR
        [--base tinylettuce-17m] [--epochs 3] [--lr 2e-5] [--batch 8] [--max-length 2048] [--limit N] [--top K]

TRAIN.json may be several files, comma-separated. --top K (the third try, his page answer of 26 October night)
trains on the same input the checker is then given: only the K facts sharing most words with the question and the
sentence (measure_checkers.top_facts), not the whole list.

WHY, 26 October 2026. His answer that evening (production/orders/2026-10-25.md): the fast checker is trained on data
Gemini 3.8 Flash wrote and labelled (tools/checkers/gemini_training_data.py), "the 127 held-out details stay the
test, and nothing changes in the game before I have seen the numbers"; his order of the afternoon: training only
while the game is closed. Untrained, no open checker cleared a true detail safely enough to matter
(production/research/invented-claims/LOCAL-CHECKERS-2026-10-26.md, "Measured").

THE DATA. TRAIN.json comes only from the detail bench's tuning half (27 contexts); the held half's 31 contexts and
its 127 details are never read here. A tenth of the examples, chosen by a fixed seed, is kept back to pick the best
epoch (the package's own rule: the best F1 on unsupported words); the 127 are measured afterwards by
measure_checkers.py --local, with its threshold set on the tuning half as before.

THE PROMPT is built exactly as the package builds it when it checks a sentence (PromptUtils.format_context: the
question first, then the facts), so the model learns the input it will be given.

THE GAME. Training runs on the processor (this PC's card is AMD, without CUDA), and stops itself, saving nothing
half-done, if the packaged game or an Unreal editor starts: it checks before every epoch and every 25 batches.
"""
import json
import os
import random
import subprocess
import sys
import time

sys.path.insert(0, r"F:\LedgerTools\checkers\pkgs")
os.environ.setdefault("HF_HOME", r"F:\LedgerTools\hf")
BASES = {"tinylettuce-17m": "KRLabsOrg/tinylettuce-ettin-17m-en", "tinylettuce-32m": "KRLabsOrg/tinylettuce-ettin-32m-en",
         "tinylettuce-68m": "KRLabsOrg/tinylettuce-ettin-68m-en"}
GAME = ("ledgerprobe.exe", "unrealeditor.exe")


def game_running():
    try:
        out = subprocess.run(["tasklist", "/fo", "csv", "/nh"], capture_output=True, text=True, timeout=20).stdout.lower()
    except (OSError, subprocess.SubprocessError):
        return False
    return any('"%s"' % g in out for g in GAME)


def samples(path, limit, top=0):
    from lettucedetect.datasets.hallucination_dataset import HallucinationSample
    from lettucedetect.detectors.prompt_utils import PromptUtils
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from measure_checkers import top_facts
    out = []
    rows = [e for p in path.split(",") for e in json.load(open(p, encoding="utf-8"))]
    assert all(e.get("half", "tune") == "tune" for e in rows), "a held-half sentence in the training data"
    for e in rows:
        labels = e["labels"] if isinstance(e["labels"], list) else json.loads(e["labels"])
        ctx = e["context"] if isinstance(e["context"], list) else [e["context"]]
        if top:
            ctx = top_facts(ctx, e["question"], e["answer"], top)
        out.append(HallucinationSample(prompt=PromptUtils.format_context(ctx, e["question"], "en"), answer=e["answer"],
                                       labels=[{"start": l["start"], "end": l["end"], "label": "unsupported"} for l in labels],
                                       split="train", task_type="qa", dataset="ledger-gemini-2026-10-26", language="en",
                                       context=None, question=e["question"]))
    random.Random(1026).shuffle(out)
    return out[:limit] if limit else out


def main(a):
    import torch
    from torch.utils.data import DataLoader
    from transformers import AutoModelForTokenClassification, AutoTokenizer, DataCollatorForTokenClassification
    from lettucedetect.datasets.hallucination_dataset import HallucinationDataset
    from lettucedetect.models.evaluator import evaluate_model, print_metrics

    opt = lambda n, d, f=str: f(a[a.index(n) + 1]) if n in a else d  # noqa: E731
    train_json, out_dir = a[0], a[1]
    base = BASES[opt("--base", "tinylettuce-17m")]
    epochs, lr, batch = opt("--epochs", 3, int), opt("--lr", 2e-5, float), opt("--batch", 8, int)
    max_len, limit, top = opt("--max-length", 2048, int), opt("--limit", 0, int), opt("--top", 0, int)
    if game_running():
        print("the game or an Unreal editor is open: not training")
        return 2
    data = samples(train_json, limit, top)
    n_dev = max(1, len(data) // 10)
    dev, train = data[:n_dev], data[n_dev:]
    tok = AutoTokenizer.from_pretrained(base)
    model = AutoModelForTokenClassification.from_pretrained(base, num_labels=2)
    coll = DataCollatorForTokenClassification(tok, label_pad_token_id=-100)
    tl = DataLoader(HallucinationDataset(train, tok, max_len), batch_size=batch, shuffle=True, collate_fn=coll)
    dl = DataLoader(HallucinationDataset(dev, tok, max_len), batch_size=batch, shuffle=False, collate_fn=coll)
    dev_loader_metrics = lambda: evaluate_model(model, dl, torch.device("cpu"))  # noqa: E731
    optim = torch.optim.AdamW(model.parameters(), lr=lr)
    print("base %s; train %d, dev %d; epochs %d, lr %g, batch %d" % (base, len(train), len(dev), epochs, lr, batch), flush=True)
    m = dev_loader_metrics()
    best = m["hallucinated"]["f1"]
    print("before training, dev F1 on unsupported words: %.4f" % best, flush=True)
    log = {"base": base, "train": len(train), "dev": len(dev), "top": top, "files": train_json, "epochs": [], "devF1Before": round(best, 4)}
    os.makedirs(out_dir, exist_ok=True)
    t0 = time.time()
    for ep in range(epochs):
        if game_running():
            print("the game or an Unreal editor opened: stopped before epoch %d" % (ep + 1))
            break
        model.train()
        total, n, stopped = 0.0, 0, False
        for i, b in enumerate(tl):
            if i % 25 == 24 and game_running():
                stopped = True
                break
            optim.zero_grad()
            loss = model(b["input_ids"], attention_mask=b["attention_mask"], labels=b["labels"]).loss
            loss.backward()
            optim.step()
            total += loss.item()
            n += 1
            if i % 50 == 0:
                print("  epoch %d batch %d/%d loss %.4f (%.0f s)" % (ep + 1, i, len(tl), total / n, time.time() - t0), flush=True)
        if stopped:
            print("the game or an Unreal editor opened: stopped in epoch %d, this epoch not kept" % (ep + 1))
            break
        m = dev_loader_metrics()
        print_metrics(m)
        f1 = m["hallucinated"]["f1"]
        log["epochs"].append({"epoch": ep + 1, "loss": round(total / max(n, 1), 4), "devF1": round(f1, 4),
                              "minutes": round((time.time() - t0) / 60, 1)})
        if f1 > best:
            best = f1
            model.save_pretrained(out_dir)
            tok.save_pretrained(out_dir)
            print("  kept epoch %d (dev F1 %.4f)" % (ep + 1, f1), flush=True)
    log["devF1Best"] = round(best, 4)
    json.dump(log, open(os.path.join(out_dir, "training-log.json"), "w", encoding="utf-8"), indent=1)
    print(json.dumps(log))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
