import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "breakers"))
import replay  # noqa: E402

S = {"dayIndex": 0, "gameMinute": 600, "clock": "10.00am", "money": {"pocketPence": 500},
     "tom": {"xMetres": 1.0, "zMetres": 2.0}}


def test_parse_action_keeps_typed_spaces():
    assert replay.parse_action("type hello there mate") == ("type", ["hello there mate"])
    assert replay.parse_action("hold KeyW+ShiftLeft 3") == ("hold", ["KeyW+ShiftLeft", "3"])
    assert replay.parse_action("look") == ("look", [])


def test_same_game():
    assert replay.same_game(S, dict(S, gameMinute=601)) == []
    assert replay.same_game(S, dict(S, money={"pocketPence": 501}))
    assert replay.same_game(S, dict(S, tom={"xMetres": 5.0, "zMetres": 2.0}))
    assert replay.same_game(None, S)


def test_verdicts():
    assert replay.verdict("money", ["clock moved"], True)[0] == "NOT REPRODUCED"
    assert replay.verdict("money", [], True)[0] == "REPRODUCED"
    assert replay.verdict("stuck", [], False)[0] == "NOT REPRODUCED"
    assert replay.verdict("talk", [], False)[0] == "NEEDS A LOOK"
    assert replay.classify("Soft Lock") == "soft lock" and replay.classify("weird") == "other"


def test_partial_classes_never_give_a_final_no():
    assert replay.verdict("money", [], False)[0] == "NEEDS A LOOK"
    assert replay.verdict("people", [], False)[0] == "NEEDS A LOOK"
    assert replay.verdict("cab", [], True)[0] == "NEEDS A LOOK"  # no cab test: never REPRODUCED by an unrelated rule
    assert replay.verdict("crash", [], False)[0] == "NOT REPRODUCED"


def test_log_with_two_sessions_is_refused(tmp_path):
    import json
    import pytest
    rows = [{"n": 0, "seed": 9}, {"n": 1, "action": "look"}, {"n": 2, "action": "look"}, {"n": 1, "action": "look"}]
    (tmp_path / "actions.jsonl").write_text("\n".join(json.dumps(r) for r in rows))
    with pytest.raises(SystemExit):
        replay.load_actions(str(tmp_path))
    (tmp_path / "actions.jsonl").write_text("\n".join(json.dumps(r) for r in rows[:3]))
    assert replay.load_actions(str(tmp_path))[0] == 9


def test_money_test_ignores_other_rules():
    class G:
        errors = []
        def state(self):
            return {"dayIndex": 0, "gameMinute": 1, "day": "Mon", "clock": "x", "phase": "elsewhere",
                    "money": {"pocketPence": 5}, "tom": {"xMetres": 0, "zMetres": 0}}
    failed, detail = replay.machine_test(G(), "money", "/tmp", 1, 0)
    assert not failed  # "the game left play" is not a money fault
