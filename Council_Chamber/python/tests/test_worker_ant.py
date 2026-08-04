import pytest

from council_chamber.models import CouncilChat, Seat, SeatKind
from council_chamber.orchestrator import Council
from council_chamber.seats.ai_seat import MockSeat
from council_chamber.storage import save_session, load_session
from council_chamber.workers.patch_worker import PatchWorker
from council_chamber.worker_ant import run_one_round, reattach_placeholder_seats, main, _PLACEHOLDER_REPLY


@pytest.fixture
def saved_session(tmp_path):
    """A session file with one AI seat already saved -- mimicking what a
    TUI `save` command (or another process entirely) would leave behind.
    Deliberately not registering a live client, since storage.py never
    persists one -- this is exactly the "load elsewhere" case."""
    project_dir = tmp_path / "project"
    project_dir.mkdir()
    council = Council(CouncilChat(), PatchWorker(project_dir))
    council.register_ai_seat(MockSeat(Seat.create("Gemini", SeatKind.AI), reply="ready to help"))
    session_path = tmp_path / "session.json"
    save_session(council, session_path)
    return session_path, project_dir


def test_run_one_round_asks_seat_and_persists_the_reply(saved_session):
    session_path, project_dir = saved_session

    replies = run_one_round(session_path, project_dir, ["Gemini"], "how should we route the buses")

    # a fresh load_session never restores the original "ready to help"
    # MockSeat.reply -- live client behavior is never serialized, only
    # seat identity is -- so a reattached seat answers with the honest
    # placeholder, not whatever it said before the file round trip.
    assert len(replies) == 1
    assert replies[0].content == _PLACEHOLDER_REPLY

    # the round was saved back -- a fresh load sees the same transcript
    reloaded = load_session(session_path, PatchWorker(project_dir))
    contents = [m.content for m in reloaded.chat.messages]
    assert "how should we route the buses" in contents
    assert _PLACEHOLDER_REPLY in contents


def test_run_one_round_does_not_touch_the_network_for_placeholder_seats(saved_session):
    """The ant itself performs no I/O beyond the local session file --
    a placeholder reply proves no network call happened for this round."""
    session_path, project_dir = saved_session
    replies = run_one_round(session_path, project_dir, ["Gemini"], "ping")
    assert replies[0].content == _PLACEHOLDER_REPLY


def test_two_rounds_accumulate_in_the_same_session(saved_session):
    session_path, project_dir = saved_session

    run_one_round(session_path, project_dir, ["Gemini"], "round one")
    run_one_round(session_path, project_dir, ["Gemini"], "round two")

    reloaded = load_session(session_path, PatchWorker(project_dir))
    contents = [m.content for m in reloaded.chat.messages]
    assert contents == ["round one", _PLACEHOLDER_REPLY, "round two", _PLACEHOLDER_REPLY]


def test_run_one_round_resolves_seat_id_directly_too(saved_session):
    session_path, project_dir = saved_session
    council = load_session(session_path, PatchWorker(project_dir))
    gemini_seat_id = next(iter(council.chat.seats))

    replies = run_one_round(session_path, project_dir, [gemini_seat_id], "direct id lookup")

    assert replies[0].content == _PLACEHOLDER_REPLY


def test_unknown_seat_token_raises(saved_session):
    session_path, project_dir = saved_session
    with pytest.raises(ValueError):
        run_one_round(session_path, project_dir, ["Nobody"], "hello?")


def test_reattach_placeholders_false_and_unregistered_seat_raises(saved_session):
    from council_chamber.orchestrator import SeatNotRegisteredError

    session_path, project_dir = saved_session
    with pytest.raises(SeatNotRegisteredError):
        run_one_round(session_path, project_dir, ["Gemini"], "hello?", reattach_placeholders=False)


def test_reattach_placeholder_seats_only_touches_unregistered_ai_seats(saved_session):
    session_path, project_dir = saved_session
    council = load_session(session_path, PatchWorker(project_dir))

    reattached = reattach_placeholder_seats(council)

    assert reattached == 1
    seat_id = next(iter(council.chat.seats))
    assert seat_id in council.ai_seats

    # calling it again is a no-op -- nothing left to reattach
    assert reattach_placeholder_seats(council) == 0


def test_a_real_client_registered_before_run_one_round_is_not_overwritten(saved_session):
    """If the caller has already wired up a real RemoteAPISeat for a seat
    before calling run_one_round, reattach_placeholder_seats must not
    clobber it with a placeholder."""
    session_path, project_dir = saved_session
    council = load_session(session_path, PatchWorker(project_dir))
    seat_id = next(iter(council.chat.seats))
    real_seat = next(iter(council.chat.seats.values()))
    council.register_ai_seat(MockSeat(real_seat, reply="this is the real one"))

    reattach_placeholder_seats(council)

    assert council.ai_seats[seat_id].reply == "this is the real one"


def test_cli_main_prints_labeled_reply(saved_session, capsys):
    session_path, project_dir = saved_session

    main([str(session_path), str(project_dir), "Gemini", "hello", "from", "the", "cli"])

    output = capsys.readouterr().out
    assert _PLACEHOLDER_REPLY in output


def test_cli_main_with_too_few_args_exits_nonzero(capsys):
    with pytest.raises(SystemExit):
        main(["only_one_arg"])
