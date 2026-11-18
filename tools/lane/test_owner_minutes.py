import datetime as dt
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import owner_minutes as om  # noqa: E402

W = dt.date(2026, 11, 9)


def item(id_, added, n_words=200, **kw):
    d = {"id": id_, "added": added, "text": " ".join(["word"] * n_words)}
    d.update(kw)
    return d


def test_one_item_answered():
    r = om.owner_minutes(W, [item("a", "2026-11-10 09:00")], [{"id": "a", "at": dt.datetime(2026, 11, 10, 10, 0)}])
    assert r["items_min"] == 1.0 and r["taps_min"] == 0.2 and r["asked"] == 1.2   # design: 1.0 + 0.17


def test_action_with_ten_steps():
    it = item("b", "2026-11-10 09:00", n_words=0, tag="ACTION", steps=["go"] * 10)
    r = om.owner_minutes(W, [it], [])
    assert r["hands_min"] == 10.0 and r["items_min"] == 0.1   # 5 + 10 x 30 s; the steps' 10 words read too


def test_answer_without_item_is_listed():
    r = om.owner_minutes(W, [], [{"id": "ghost", "at": dt.datetime(2026, 11, 11, 8, 0)}])
    assert r["taps_min"] == 0.2 and r["items_min"] == 0
    assert any("ghost" in e for e in r["estimated_parts"])


def test_no_finished_units():
    r = om.owner_minutes(W, [], [], finished_units=0)
    assert r["per_piece"] == "none finished"
    assert om.owner_minutes(W, [item("a", "2026-11-10 09:00")], [], finished_units=2)["per_piece"] == 0.5


def test_batches_count_done_items_too():
    its = [item("x", "2026-11-12 09:00", state="done"), item("y", "2026-11-12 12:00", state="done"), item("z", "2026-11-12 18:00")]
    r = om.owner_minutes(W, its, [])
    assert r["batches_by_day"] == {"2026-11-12": 3}
    assert "days over two batches: 1" in om.audit_line(dt.datetime(2026, 11, 9), r)


def test_week_edges():
    its = [item("in", "2026-11-09 00:00"), item("out", "2026-11-16 00:00"), item("before", "2026-11-08 23:59")]
    assert om.owner_minutes(W, its, [])["items"] == 1


def test_pictures_and_options_words():
    it = {"id": "p", "added": "2026-11-10 09:00", "title": "Tom whole", "options": [["yes", "Yes (recommended)"], ["no", "No"]],
          "pictures": [{"src": "a.jpg"}, {"src": "b.jpg"}, {"src": "c.jpg"}]}
    r = om.owner_minutes(W, [it], [])
    assert r["pictures_min"] == 1.0
    assert om.item_words(it) == 2 + 5


def test_reports_and_advisor_measured_when_given():
    r = om.owner_minutes(W, [], [], reports=[" ".join(["w"] * 400)], advisor_rows=10)
    assert r["reports_min"] == 2.0 and r["asked"] == 2.0 and r["chosen"] == 20.0 and r["estimated_parts"] == []
    r2 = om.owner_minutes(W, [], [])
    assert r2["chosen"] is None and "reports not measured" in r2["estimated_parts"]


def test_line_and_target():
    r = om.owner_minutes(W, [item("a", "2026-11-10 09:00", n_words=8000)], [])
    line = om.audit_line(dt.datetime(2026, 11, 9), r, target=30)
    assert line.startswith("Owner minutes 09 Nov to 15 Nov: asked 40") and "target 30 OVER" in line
    assert "reports n.m." in line and "chosen n.m." in line


def test_utc_answer_to_swiss():
    assert om.parse_answer_at("2026-11-08T16:17:11.542Z") == dt.datetime(2026, 11, 8, 17, 17, 11)
    assert om.parse_answer_at("2026-10-20T10:00:00Z") == dt.datetime(2026, 10, 20, 12, 0)   # summer time
    assert om.parse_answer_at("rubbish") is None and om.parse_added("") is None


def test_real_records_last_week():
    r = om.owner_minutes(W, om.read_items(), om.read_answers())
    # the design's worked check (production/lane/OWNER-MINUTES-MEASURE-2026-11-18.md): 49 items, about 36 minutes of reading
    assert r["items"] == 49
    assert 30 <= r["items_min"] <= 42
    assert r["answers"] >= 40


def test_offsets_and_dst_edges():
    assert om.parse_answer_at("2026-11-10T10:00:00+01:00") == dt.datetime(2026, 11, 10, 10, 0)
    assert om.parse_answer_at("2026-11-10T09:00:00-01:00") == dt.datetime(2026, 11, 10, 11, 0)
    assert om.parse_answer_at("2026-10-25T00:59:59Z") == dt.datetime(2026, 10, 25, 2, 59, 59)   # last summer second
    assert om.parse_answer_at("2026-10-25T01:00:00Z") == dt.datetime(2026, 10, 25, 2, 0)        # winter from 01:00 UTC
    assert om.parse_answer_at("2026-03-29T01:00:00Z") == dt.datetime(2026, 3, 29, 3, 0)
    assert om.parse_answer_at(None) is None and om.parse_answer_at(5) is None


def test_odd_steps_pictures_and_missing_fields():
    its = [item("s", "2026-11-10 09:00", n_words=0, tag="ACTION", steps="1. open\n2. click\n"),
           item("q", "2026-11-10 09:00", n_words=0, pictures="a.jpg"), {"id": "nodate", "text": "x"}, "junk"]
    r = om.owner_minutes(W, its, [])
    assert r["hands_min"] == 6.0 and r["pictures_min"] == 0.3 and r["items"] == 2


def test_added_one_week_answered_next():
    its = [item("a", "2026-11-15 23:00")]
    r = om.owner_minutes(dt.date(2026, 11, 16), its, [{"id": "a", "at": om.parse_answer_at("2026-11-16T07:00:00Z")}])
    assert r["items"] == 0 and r["answers"] == 1 and r["estimated_parts"] == ["reports not measured", "advisor rows not measured"]


def test_read_answers_one_tap_per_id(tmp_path):
    for sub, at in (("verdicts", "2026-11-10T10:00:00Z"), ("items", None), ("other", "2026-11-11T10:00:00Z")):
        (tmp_path / sub).mkdir()
        (tmp_path / sub / "x.json").write_text("{}" if at is None else '{"at": "%s"}' % at)
    (tmp_path / "verdicts" / "list.json").write_text("[1, 2]")
    assert om.read_answers(str(tmp_path)) == [{"id": "x", "at": dt.datetime(2026, 11, 10, 11, 0)}]
