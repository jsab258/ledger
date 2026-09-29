"""How often 2.5 s windows of GENUINE English speech read American, against the takes: calibrating the window rule.

    python accent_windows.py OUT.json FILE... (files, or @list.txt)
For each file: the whole take's American share, and over 2.5 s windows every 0.5 s,
the worst window, the share of windows at or over 0.30, and the longest run of such windows (seconds).
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import librosa, torch
import accent_check as ac

clf = ac.classifier()
labels = clf.hparams.label_encoder.decode_ndim(list(range(16)))

def acc(y):
    out = clf.classify_batch(torch.tensor(y).unsqueeze(0))
    cos = out[0][0] if out[0].dim() == 2 else out[0]
    p = torch.softmax(cos * ac.SCALE, dim=-1)
    return {str(l): float(v) for l, v in zip(labels, p)}

files = []
for a in sys.argv[2:]:
    if a.startswith('@'):
        files += [l.strip() for l in open(a[1:]) if l.strip()]
    else:
        files.append(a)
rows = []
for f in files:
    y = librosa.load(f, sr=16000)[0]
    whole = sum(acc(y).get(a, 0.0) for a in ac.AMERICAN)
    win = []
    for s in range(0, max(1, len(y) - 40000 + 1), 8000):
        win.append(sum(acc(y[s:s + 40000]).get(a, 0.0) for a in ac.AMERICAN))
    run = best = 0
    for w in win:
        run = run + 1 if w >= 0.30 else 0
        best = max(best, run)
    rows.append({'file': f, 'seconds': round(len(y) / 16000, 2), 'whole': round(whole, 3), 'worst': round(max(win), 3),
                 'shareOver': round(sum(1 for w in win if w >= 0.30) / len(win), 3), 'windows': len(win),
                 'longestRunS': round((best - 1) * 0.5 + 2.5, 1) if best else 0.0})
    print(json.dumps(rows[-1]), flush=True)
json.dump(rows, open(sys.argv[1], 'w'), indent=1)
