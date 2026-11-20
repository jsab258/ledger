import launch
def test_port_name_kept():
    b = launch.fill("set LEDGER_PLAY_PORT=PORT first; python PLAYDIR/play.py; MINUTES minutes\nCARD", "## 1. X", 12, 8771, "/p")
    assert "LEDGER_PLAY_PORT=8771" in b and "LEDGER_PLAY_8771" not in b and "/p/play.py" in b and "12 minutes" in b
def test_real_briefs():
    import io, contextlib
    for kind, card in (("player", "1"), ("breaker", "A")):
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            launch.main([kind, "--card", card, "--minutes", "12", "--port", "8771", "--playdir", "/x/play"])
        s = f.getvalue()
        assert "LEDGER_PLAY_PORT=8771" in s and "filled in by the launcher" not in s and "/x/play/play.py look" in s
