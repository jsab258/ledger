"""Unit checks for machine_checks.py (no browser)."""
import machine_checks as mc


def test_content_scan_catches_drink_gambling_children():
    js = "const a = 'He had a pint at the Anchor before work.'; const b = \"The bookie on the corner took his money.\"; const c = `Two children ran past the cab.`;"
    s = mc.content_scan(js)
    words = sorted(f["word"] for f in s["fails"])
    assert words == ["bookie", "children", "pint"]


def test_content_scan_warns_not_fails_on_ambiguous():
    s = mc.content_scan("const a = 'I bet he owes Cammack more than that.'; const b = 'Drink your tea and let me get on.';")
    assert not s["fails"] and "bet" in s["warns"] and "drink" in s["warns"]


def test_content_scan_skips_the_rule_text_and_code():
    js = "const R = 'ABSOLUTE CONTENT RULES: no alcohol, no children, no gambling.'; el.appendChild(child); x = 'children';"
    assert not mc.content_scan(js)["fails"]


def read(day=0, minute=600.0, pocket=2350, phase="play", x=1.0):
    return {"dayIndex": day, "day": "Monday", "clock": "x", "gameMinute": minute, "phase": phase, "weekEnded": False,
            "money": {"pocketPence": pocket, "tinPence": 0}, "tom": {"xMetres": x, "zMetres": 2.0}}


def test_rules_clock_back_and_money():
    f = mc.rule_faults(read(minute=500), read(minute=600), [])
    assert any("clock went back" in x for x in f)
    assert any("below nothing" in x for x in mc.rule_faults(read(pocket=-5), None, []))
    assert any("whole pence" in x for x in mc.rule_faults(read(pocket=12.5), None, []))


def test_rules_tom_and_people():
    assert any("real position" in x for x in mc.rule_faults(read(x=float("nan")), None, []))
    assert any("left play" in x for x in mc.rule_faults(read(phase="end"), None, []))
    assert mc.rule_faults(read(), read(minute=500), [{"id": "rita", "bad": None}]) == []
    assert mc.rule_faults(read(), None, [{"id": "rita", "bad": "inside a solid at 1, 2"}]) == ["rita: inside a solid at 1, 2"]
