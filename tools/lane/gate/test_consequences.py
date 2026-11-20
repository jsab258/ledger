"""The consequence checker catches each planted fault and passes a clean week (no browser needed)."""
import copy
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from consequences import trace, words_rules  # noqa: E402

CLEAN = {
    "events": [{"id": 1, "kind": "night_out", "t": 100, "wit": ["ada"], "party": []},
               {"id": 2, "kind": "inherit", "t": 0, "wit": [], "party": []}],
    "minds": {
        "ada": {"regard": -0.1, "fear": 0, "mem": [{"e": 1, "src": "saw", "from": None, "t": 100}]},
        "ron": {"regard": -0.05, "fear": 0, "mem": [{"e": 1, "src": "told", "from": "ada", "t": 130},
                                                     {"e": 2, "src": "self", "from": None, "t": 0}]},
        "lee": {"regard": 0, "fear": 0, "mem": [{"e": 1, "src": "told", "from": "ron", "t": 200}]},
    },
    "transfers": [{"a": "ada", "b": "ron", "e": 1, "t": 130}, {"a": "ron", "b": "lee", "e": 1, "t": 200}],
}
START = {"minds": {k: {"regard": 0, "fear": 0, "mem": []} for k in ("ada", "ron", "lee")}}


def failed(save, start=START):
    return sorted(set(r["rule"] for r in trace(save, start)[0] if r["ok"] is False))


def test_clean_week_passes():
    assert failed(CLEAN) == []


def test_planted_faults_are_caught():
    s = copy.deepcopy(CLEAN); s["minds"]["ada"]["mem"][0]["e"] = 9
    assert "a memory names a real event" in failed(s)
    s = copy.deepcopy(CLEAN); s["minds"]["ada"]["mem"][0]["t"] = 50
    assert "a memory is formed no earlier than its event" in failed(s)
    s = copy.deepcopy(CLEAN); s["events"][0]["wit"] = []
    assert "a sighting has its witness" in failed(s)
    s = copy.deepcopy(CLEAN); s["minds"]["lee"]["mem"][0]["src"] = "heard"
    assert "a sound is heard as it happens" in failed(s)
    s = copy.deepcopy(CLEAN); s["transfers"] = s["transfers"][1:]
    assert "a telling is recorded" in failed(s)
    s = copy.deepcopy(CLEAN); s["minds"]["ron"]["mem"][0]["t"] = 300; s["transfers"][1]["t"] = 300
    assert "a teller knew it first" in failed(s)
    s = copy.deepcopy(CLEAN); s["minds"]["ada"]["mem"][0] = {"e": 1, "src": "told", "from": "lee", "t": 100}
    s["transfers"].append({"a": "lee", "b": "ada", "e": 1, "t": 100})
    assert "a chain of tellings ends at the act" in failed(s)
    s = copy.deepcopy(CLEAN); s["transfers"].append({"a": "ada", "b": "lee", "e": 2, "t": 210})
    assert "a telling leaves a memory" in failed(s)
    s = copy.deepcopy(CLEAN); s["events"][0]["party"] = ["ron"]; s["minds"]["lee"]["mem"].append({"e": 1, "src": "self", "t": 200})
    assert "a part in it has its party" in failed(s)


def test_reused_sighting_heard_late_is_not_a_fault():
    s = copy.deepcopy(CLEAN); s["minds"]["lee"]["mem"][0]["src"] = "heard"; s["sightIdx"] = {"night_out:0:1:Quay": 1}
    assert failed(s) == []


def test_nothing_to_check_is_not_a_pass():
    s = {"events": [], "minds": {"ada": {"regard": 0, "fear": 0, "mem": []}}, "transfers": []}
    out = trace(s, START)[0]
    assert all(r["ok"] is None for r in out)
    assert not any(r["ok"] is False for r in out)


def test_reaction_without_memory_is_a_warning_only():
    s = copy.deepcopy(CLEAN); s["minds"]["lee"] = {"regard": -0.4, "fear": 0.2, "mem": []}; s["transfers"] = s["transfers"][:1]
    out, notes = trace(s, START)
    assert not any(r["ok"] is False for r in out)
    assert any("warning: feelings moved" in n and "lee" in n for n in notes)


def test_words():
    frames = [(10, ["You were seen out late, and on foot."]), (11, ["You were seen out late, and on foot."]),
              (15, ["Evening."]), (40, ["Evening."]), (60, ["You were seen out late, and on foot."])]
    bad = {r["rule"] for r in words_rules(frames)[0] if r["ok"] is False}
    assert bad == {"no line repeated"}  # once up at 10 to 11 is one showing; 60 is the repeat; "Evening." is short
    bad = {r["rule"] for r in words_rules([(1, ["Send me an email about it."])], ["He had a pint at the bar."])[0] if r["ok"] is False}
    assert bad == {"nothing wrong for 1990", "the content rule in what is shown"}
    assert all(r["ok"] for r in words_rules([(1, ["Mickey kept a book on the whole street."])])[0])
    assert all(r["ok"] is None for r in words_rules([])[0])
