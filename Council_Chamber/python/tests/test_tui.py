import pytest

from council_chamber.models import CouncilChat, Seat, SeatKind
from council_chamber.seats.ai_seat import MockSeat
from council_chamber.workers.patch_worker import PatchWorker
from council_chamber.orchestrator import Council
from council_chamber.tui import CouncilTUI, UnknownCommandError, SeatNotFoundError, demo_council, SEAT_CATALOG


@pytest.fixture
def project(tmp_path):
    (tmp_path / "main.py").write_text("def add(a, b):\n    return a + b\n")
    return tmp_path


@pytest.fixture
def tui(project):
    chat = CouncilChat()
    council = Council(chat, PatchWorker(project))
    council.register_ai_seat(MockSeat(Seat.create("Codex", SeatKind.AI), reply="proposing a fix"))
    return CouncilTUI(council)


def test_seats_lists_open_seats(tui):
    output = tui.execute("seats")
    assert "Codex" in output
    assert "[open]" in output


def test_seats_with_no_seats_open_says_so():
    council_tui = CouncilTUI(Council(CouncilChat(), PatchWorker("/tmp")))
    assert council_tui.execute("seats") == "(no seats open)"


def test_ask_resolves_seat_by_name_and_labels_reply(tui):
    output = tui.execute("ask Codex look at main.py")
    assert output == "[Codex] proposing a fix"


def test_ask_unknown_seat_raises(tui):
    with pytest.raises(SeatNotFoundError):
        tui.execute("ask Gemini hello")


def test_unknown_command_raises(tui):
    with pytest.raises(UnknownCommandError):
        tui.execute("levitate")


def test_empty_line_returns_empty_string(tui):
    assert tui.execute("   ") == ""


def test_propose_diff_approve_workflow(tui, project):
    propose_output = tui.execute(
        r'propose Codex main.py "def add(a, b):\n    return a + b + 1\n" --desc "fix off-by-one"'
    )
    assert "proposed change to main.py" in propose_output
    assert "+    return a + b + 1" in propose_output

    assert tui.execute("pending") == "main.py"
    assert "+    return a + b + 1" in tui.execute("diff main.py")

    approve_output = tui.execute("approve main.py")
    assert "applied" in approve_output
    assert (project / "main.py").read_text() == "def add(a, b):\n    return a + b + 1\n"
    assert tui.execute("pending") == "(no pending changes)"


def test_reject_discards_pending_change_without_writing(tui, project):
    tui.execute(r'propose Codex main.py "def add(a, b):\n    return a + b + 1\n"')
    output = tui.execute("reject main.py not needed")
    assert output == "rejected main.py"
    assert (project / "main.py").read_text() == "def add(a, b):\n    return a + b\n"


def test_diff_for_nonexistent_pending_change(tui):
    assert tui.execute("diff nope.py") == "no pending change for nope.py"


def test_transcript_shows_labeled_messages(tui):
    tui.execute("ask Codex hello there")
    output = tui.execute("transcript")
    assert "[user] hello there" in output
    assert "[Codex] proposing a fix" in output


def test_transcript_empty_says_so():
    council_tui = CouncilTUI(Council(CouncilChat(), PatchWorker("/tmp")))
    assert council_tui.execute("transcript") == "(empty)"


def test_usage_and_usage_summary_report_unavailable_for_mock_seat(tui):
    tui.execute("ask Codex hello")
    usage_output = tui.execute("usage Codex")
    assert "mock seat -- no real provider connection" in usage_output

    summary_output = tui.execute("usage-summary Codex")
    assert "'input_tokens': None" in summary_output
    assert "'reports_without_data': 1" in summary_output


def test_usage_with_no_history_says_so(tui):
    assert tui.execute("usage Codex") == "(no usage recorded)"


def test_help_lists_commands(tui):
    output = tui.execute("help")
    assert "propose" in output
    assert "approve" in output


def test_quit_returns_goodbye(tui):
    assert tui.execute("quit") == "goodbye"


def test_demo_council_opens_chatgpt_and_codex_against_real_project_dir(tmp_path):
    project_dir = tmp_path / "demo_project"

    council = demo_council(project_dir)

    assert project_dir.is_dir()
    names = {s.name for s in council.chat.open_seats()}
    assert names == {"ChatGPT", "Codex"}


def test_demo_council_seats_are_usable_through_the_tui(tmp_path):
    council = demo_council(tmp_path / "demo_project")
    council_tui = CouncilTUI(council)

    output = council_tui.execute("ask ChatGPT what should we build")

    assert "[ChatGPT]" in output
    assert "no real provider connected" in output


def test_seat_catalog_includes_every_spec_named_provider():
    assert set(SEAT_CATALOG) == {"chatgpt", "codex", "claude", "gemini", "deepseek", "grok", "local"}


@pytest.mark.parametrize("key", list(SEAT_CATALOG))
def test_open_can_open_every_catalog_seat_and_it_can_propose_code(key, tui, project):
    open_output = tui.execute(f"open {key}")
    display_name = SEAT_CATALOG[key]
    assert f"opened {display_name}" in open_output
    assert display_name in tui.execute("seats")

    # Any opened seat can propose a change exactly like Codex can --
    # no provider is special-cased.
    propose_output = tui.execute(f'propose "{display_name}" other.py "x = 1\\n"')
    assert "proposed change to other.py" in propose_output


def test_open_unknown_catalog_key_raises(tui):
    with pytest.raises(ValueError):
        tui.execute("open bard")


def test_save_and_load_round_trips_transcript_and_reattaches_ai_seats(tmp_path):
    project_dir = tmp_path / "proj"
    council = demo_council(project_dir)
    council_tui = CouncilTUI(council)
    council_tui.execute("ask ChatGPT hello there")

    session_path = tmp_path / "session.json"
    save_output = council_tui.execute(f"save {session_path}")
    assert "saved session" in save_output
    assert session_path.exists()

    fresh_tui = CouncilTUI(Council(CouncilChat(), PatchWorker(project_dir)))
    load_output = fresh_tui.execute(f"load {session_path}")

    assert "2 seat(s)" in load_output
    assert "2 AI seat(s) reattached" in load_output
    assert "[user] hello there" in fresh_tui.execute("transcript")

    # the reattached seat is immediately usable again, as a placeholder
    reply = fresh_tui.execute("ask ChatGPT what now")
    assert "[ChatGPT]" in reply
    assert "no real provider connected" in reply


def test_save_with_no_path_raises(tui):
    with pytest.raises(ValueError):
        tui.execute("save")


def test_load_with_no_path_raises(tui):
    with pytest.raises(ValueError):
        tui.execute("load")


def test_tui_starts_in_a_main_room_by_default(tui):
    output = tui.execute("rooms")
    assert output == "* main"


def test_create_room_switches_into_it(tui, tmp_path):
    lab_dir = tmp_path / "lab_project"
    output = tui.execute(f"create-room lab {lab_dir}")
    assert "created room 'lab'" in output
    assert "now in room 'lab'" in output
    assert lab_dir.is_dir()

    rooms_output = tui.execute("rooms")
    assert "* lab" in rooms_output
    assert "  main" in rooms_output


def test_room_switches_back_and_forth_preserving_each_rooms_state(tui, tmp_path):
    tui.execute(f"create-room lab {tmp_path / 'lab_project'}")
    tui.execute("open gemini")  # opened only in "lab"

    tui.execute("room main")
    assert "Codex" in tui.execute("seats")
    assert "Gemini" not in tui.execute("seats")

    tui.execute("room lab")
    assert "Gemini" in tui.execute("seats")
    assert "Codex" not in tui.execute("seats")


def test_room_with_unknown_name_raises(tui):
    with pytest.raises(KeyError):
        tui.execute("room nope")


def test_branch_creates_a_side_room_with_copied_files_and_fresh_chat(tui, project):
    tui.execute("ask Codex hello")  # main room now has transcript history

    output = tui.execute("branch main side")
    assert "branched 'main' into side room 'side'" in output
    assert "now in room 'side'" in output

    # side room's files are a real copy of main's
    assert tui.execute("cat main.py") == (project / "main.py").read_text()
    # but the chat is brand new, not shared with main
    assert tui.execute("transcript") == "(empty)"
    assert tui.execute("seats") == "(no seats open)"


def test_editing_a_side_room_does_not_touch_the_main_room(tui, project):
    tui.execute("branch main side")
    tui.execute("open codex")
    tui.execute(r'propose Codex main.py "x = 1\n"')
    tui.execute("approve main.py")

    assert tui.execute("cat main.py") == "x = 1\n"

    tui.execute("room main")
    assert tui.execute("cat main.py") == "def add(a, b):\n    return a + b\n"


def test_files_lists_files_in_the_current_room(tui):
    output = tui.execute("files")
    assert "main.py" in output


def test_files_with_glob_filters_results(tui, project):
    (project / "notes.md").write_text("hi")
    output = tui.execute("files *.md")
    assert "notes.md" in output
    assert "main.py" not in output


def test_cat_prints_file_contents(tui, project):
    assert tui.execute("cat main.py") == "def add(a, b):\n    return a + b\n"


def test_cat_missing_file_says_so(tui):
    assert tui.execute("cat nope.py") == "no such file: nope.py"


def test_cat_rejects_path_escaping_the_room_directory(tui):
    with pytest.raises(ValueError):
        tui.execute("cat ../../etc/passwd")


def test_load_replaces_the_council_of_the_current_room_only(tui, project, tmp_path):
    session_path = tmp_path / "session.json"
    tui.execute(f"save {session_path}")

    tui.execute(f"create-room lab {tmp_path / 'lab_project'}")
    tui.execute(f"load {session_path}")

    # loading into "lab" must not disturb "main"'s own council/session
    tui.execute("room main")
    assert "Codex" in tui.execute("seats")
