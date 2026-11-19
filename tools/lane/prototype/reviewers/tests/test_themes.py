import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import themes  # noqa: E402


def test_boring_is_punished():
    t = themes.score_review({"thumb": "down", "text": "Boring. I spent ten minutes waiting with nothing to do."})
    assert 5 in t["punish"] and 5 not in t["praise"]


def test_repeated_lines_count_as_bugs_and_hollow():
    t = themes.score_review({"thumb": "down", "text": "Every NPC repeats the same line word for word."})
    assert 6 in t["punish"]


def test_world_praise():
    t = themes.score_review({"thumb": "up", "text": "The town feels alive and people remember what you did."})
    assert 3 in t["praise"]


def test_flip_turns_praise_to_complaint():
    t = themes.score_review({"thumb": "up", "text": "The story is not good."})
    assert 1 in t["punish"]


def test_shares_table():
    rows = themes.panel_shares([{"thumb": "down", "text": "Boring."}, {"thumb": "up", "text": "Great story."}])
    x5 = [r for r in rows["punish"] if r["rank"] == 5][0]
    p1 = [r for r in rows["praise"] if r["rank"] == 1][0]
    assert x5["panel_pct"] == 50.0 and p1["panel_pct"] == 50.0 and p1["mafia_pct"] == 47.5
