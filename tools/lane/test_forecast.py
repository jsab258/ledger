import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import forecast as fc  # noqa: E402


def _log(tmp_path, rows):
    p = tmp_path / "log.jsonl"
    p.write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")
    return str(p)


def test_task_code():
    assert fc.task_code("n09-2 Tom as one whole person") == "n09-2"
    assert fc.task_code("n16-10: efficiency") == "n16-10"
    assert fc.task_code("n16-1 Kiln") == "n16-1"
    assert fc.task_code("tool test") is None
    assert fc.task_code("n02-3-3-stutter") == "n02-3"


def test_read_log_and_ratios(tmp_path):
    log = _log(tmp_path, [
        {"event": "start", "at": "2026-11-01T08:00:00", "task": "n09-1 a", "phase": "2", "kind": "production"},
        {"event": "stop", "at": "2026-11-01T10:00:00"},
        {"event": "start", "at": "2026-11-01T11:00:00", "task": "n09-1 a again", "phase": "2", "kind": "production"},
        {"event": "stop", "at": "2026-11-01T12:00:00"},
        {"event": "start", "at": "2026-11-01T13:00:00", "task": "n09-2 b", "phase": "2", "kind": "production"},
        {"event": "stop", "at": "2026-11-01T14:30:00"},
        {"event": "start", "at": "2026-11-01T15:00:00", "task": "tool test", "phase": "2", "kind": "tool"},
        {"event": "stop", "at": "2026-11-01T15:30:00"},
    ])
    hours, unclosed, _ = fc.read_log(log)
    assert unclosed == 0
    items = [
        {"code": "n09-1", "planned_h": 1.5, "done": True},
        {"code": "n09-2", "planned_h": 3, "done": True},
        {"code": "n09-3", "planned_h": 5, "done": False},
    ]
    per, unmatched = fc.actual_per_item(hours, items)
    assert per["n09-1"] == 3.0
    assert per["n09-2"] == 1.5
    assert unmatched == {"tool test": 0.5}
    rs = dict(fc.ratios(items, per))
    assert rs == {"n09-1": 2.0, "n09-2": 0.5}


def test_unclosed_start_is_closed_at_next_start(tmp_path):
    log = _log(tmp_path, [
        {"event": "start", "at": "2026-11-01T08:00:00", "task": "n09-1 a"},
        {"event": "start", "at": "2026-11-01T09:00:00", "task": "n09-2 b"},
        {"event": "stop", "at": "2026-11-01T09:30:00"},
    ])
    hours, unclosed, _ = fc.read_log(log)
    assert unclosed == 1
    assert hours == {"n09-1 a": 1.0, "n09-2 b": 0.5}


def test_alias_matching():
    items = [{"code": "n09-6", "planned_h": 2, "done": True, "aliases": ["kiln"]}]
    per, unmatched = fc.actual_per_item({"kiln round 3": 4.0, "other": 1.0}, items)
    assert per["n09-6"] == 4.0 and unmatched == {"other": 1.0}


def test_single_ratio_is_exact():
    f = fc.forecast([10, 20, 30], [2.0], sims=500)
    assert f["plan_h"] == 60
    assert f["p50_h"] == f["p80_h"] == 120.0


def test_two_ratios_one_item_known_percentiles():
    # One item, ratios 1 and 3, equal odds: P50 is 10 h, P80 is 30 h.
    f = fc.forecast([10], [1.0, 3.0], sims=10000, seed=7)
    assert f["p50_h"] == 10.0
    assert f["p80_h"] == 30.0


def test_many_items_converge_to_mean_ratio():
    # 100 items of 1 h, ratios 1 and 3: total centres on 200 h.
    f = fc.forecast([1.0] * 100, [1.0, 3.0], sims=4000, seed=3)
    assert 190 <= f["p50_h"] <= 210
    assert f["p80_h"] > f["p50_h"]


def test_seeded_repeatable():
    a = fc.forecast([5, 8], [0.5, 1.2, 4.3], seed=11)
    b = fc.forecast([5, 8], [0.5, 1.2, 4.3], seed=11)
    assert a == b


def test_percentile_nearest_rank():
    v = list(range(1, 11))
    assert fc.percentile(v, 50) == 5
    assert fc.percentile(v, 80) == 8
    assert fc.percentile(v, 100) == 10


def test_csv_plan_and_cli(tmp_path, capsys):
    log = _log(tmp_path, [
        {"event": "start", "at": "2026-11-01T08:00:00", "task": "n09-1 a"},
        {"event": "stop", "at": "2026-11-01T12:00:00"},
    ])
    plan = tmp_path / "plan.csv"
    plan.write_text("code,planned_h,done\nn09-1,2,true\nn09-2,10,false\n", encoding="utf-8")
    assert fc.main(["--log", log, "--plan", str(plan), "--json"]) == 0
    out = json.loads(capsys.readouterr().out)
    assert out["matched_ratios"] == [{"code": "n09-1", "ratio": 2.0}]
    assert out["forecast"]["p50_h"] == 20.0 and out["forecast"]["p80_h"] == 20.0


def test_backwards_interval_skipped(tmp_path):
    log = _log(tmp_path, [
        {"event": "start", "at": "2026-11-01T10:00:00", "task": "n09-1 a"},
        {"event": "stop", "at": "2026-11-01T09:30:00"},
        {"event": "start", "at": "2026-11-01T11:00:00", "task": "n09-1 a"},
        {"event": "stop", "at": "2026-11-01T12:00:00"},
    ])
    hours, unclosed, backwards = fc.read_log(log)
    assert hours == {"n09-1 a": 1.0} and unclosed == 0 and backwards == 1


def test_few_ratios_warned(tmp_path, capsys):
    log = _log(tmp_path, [
        {"event": "start", "at": "2026-11-01T08:00:00", "task": "n09-1 a"},
        {"event": "stop", "at": "2026-11-01T08:12:00"},
    ])
    plan = tmp_path / "plan.json"
    plan.write_text(json.dumps({"items": [
        {"code": "n09-1", "planned_h": 2, "done": True},
        {"code": "n09-2", "planned_h": 5, "done": False}]}), encoding="utf-8")
    fc.main(["--log", log, "--plan", str(plan), "--json"])
    out = json.loads(capsys.readouterr().out)
    assert len(out["warnings"]) == 2
    assert out["forecast"]["p50_h"] == 0.5  # 5 h x 0.1
