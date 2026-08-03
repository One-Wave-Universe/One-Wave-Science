from council_chamber.cli import run


def test_cli_demo_reaches_all_tests_pass(tmp_path):
    assert run(project_dir=tmp_path) is True
    assert (tmp_path / "seats.py").read_text().strip().endswith(
        'self.seats[seat_id]["connected"] = False'
    )


def test_cli_demo_transcript_shows_failure_then_fix(tmp_path, capsys):
    run(project_dir=tmp_path)
    output = capsys.readouterr().out
    assert "1 failed" in output
    assert "2 passed" in output
    assert "ALL TESTS PASS" in output
