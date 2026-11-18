import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import release_libs as rl  # noqa: E402

LIC = "LedgerProbe/Content/LedgerData/production/licences/engine/"


def test_debug_layer_is_dropped_whatever_the_case_and_slashes():
    r = rl.report(["Engine\\Binaries\\Win64\\D3D12\\D3D12SDKLayers.dll"])
    assert [d["path"] for d in r["drop"]] == ["Engine/Binaries/Win64/D3D12/D3D12SDKLayers.dll"]
    assert not r["clean"]


def test_manifest_line_uses_first_tab_field_and_skips_blanks():
    r = rl.report(["Engine/Binaries/Win64/D3D12/d3d12SDKLayers.dll\t2026-10-05T10:00:00", "", "   "])
    assert len(r["drop"]) == 1 and r["drop"][0]["path"].endswith("d3d12SDKLayers.dll")


def test_library_with_licence_present_and_read_is_clean():
    r = rl.report(["Engine/Binaries/ThirdParty/Ogg/Win64/libogg_64.dll", LIC + "ogg-LICENSE.txt"])
    assert r["licence"][0]["licence_present"] and r["licence"][0]["status"] == "read"
    assert r["clean"]


def test_missing_licence_file_is_not_clean():
    r = rl.report(["Engine/Binaries/Win64/msquic.dll"])
    assert r["licence"][0]["licence_present"] is False
    assert not r["clean"]


def test_not_read_library_is_never_clean_even_with_a_file():
    r = rl.report(["Engine/Binaries/ThirdParty/DbgHelp/dbghelp.dll", LIC + "dbghelp-LICENSE.txt"])
    assert r["licence"][0]["status"] == "not read"
    assert not r["clean"]


def test_unknown_dll_is_reported_and_other_files_ignored():
    r = rl.report(["LedgerProbe/Binaries/Win64/mystery.dll", "LedgerProbe/Content/Paks/a.pak", "NOTICES.txt"])
    assert [u["path"] for u in r["unknown"]] == ["LedgerProbe/Binaries/Win64/mystery.dll"]
    assert r["drop"] == [] and r["licence"] == []


def test_every_status_is_read_or_not_read():
    assert {s for _, s, _ in rl.LIBRARIES.values()} <= {"read", "not read"}
    assert all(k == k.lower() for k in list(rl.LIBRARIES) + list(rl.DROP))


def test_main_exit_codes_and_json(tmp_path, capsys):
    good = tmp_path / "good.txt"
    good.write_text("Engine/Binaries/Win64/tbb12.dll\n" + LIC + "onetbb-LICENSE.txt\n", encoding="utf-8")
    assert rl.main([str(good)]) == 0
    bad = tmp_path / "bad.txt"
    bad.write_text("Engine/Binaries/Win64/D3D12/D3D12SDKLayers.dll\n", encoding="utf-8")
    capsys.readouterr()
    assert rl.main(["--json", str(bad)]) == 1
    out = json.loads(capsys.readouterr().out)
    assert out["drop"][0]["path"].endswith("D3D12SDKLayers.dll") and out["clean"] is False
