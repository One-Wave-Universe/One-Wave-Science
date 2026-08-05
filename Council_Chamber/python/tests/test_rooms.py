import pytest

from council_chamber.models import CouncilChat, Seat, SeatKind
from council_chamber.orchestrator import Council
from council_chamber.rooms import World, Room, RoomAlreadyExistsError, RoomNotFoundError
from council_chamber.seats.ai_seat import MockSeat
from council_chamber.workers.patch_worker import PatchWorker
from council_chamber.workers.test_worker import TestWorker


def test_create_room_makes_the_project_directory(tmp_path):
    world = World()
    room = world.create_room("main", tmp_path / "main_project")

    assert room.project_dir.is_dir()
    assert room.name == "main"
    assert world.get_room("main") is room


def test_create_room_with_duplicate_name_raises(tmp_path):
    world = World()
    world.create_room("main", tmp_path / "main_project")
    with pytest.raises(RoomAlreadyExistsError):
        world.create_room("main", tmp_path / "other")


def test_get_room_for_unknown_name_raises(tmp_path):
    world = World()
    with pytest.raises(RoomNotFoundError):
        world.get_room("nope")


def test_room_names_lists_every_room(tmp_path):
    world = World()
    world.create_room("main", tmp_path / "a")
    world.create_room("lab", tmp_path / "b")
    assert set(world.room_names()) == {"main", "lab"}


def test_each_room_has_its_own_independent_council(tmp_path):
    world = World()
    main = world.create_room("main", tmp_path / "main_project")
    lab = world.create_room("lab", tmp_path / "lab_project")

    assert main.council is not lab.council
    assert main.council.chat is not lab.council.chat


def test_branch_room_copies_parent_files(tmp_path):
    world = World()
    main = world.create_room("main", tmp_path / "main_project")
    (main.project_dir / "app.py").write_text("x = 1\n")

    side = world.branch_room("main", "side")

    assert (side.project_dir / "app.py").read_text() == "x = 1\n"
    assert side.project_dir != main.project_dir


def test_branch_room_gives_a_brand_new_chat_not_the_parents(tmp_path):
    world = World()
    main = world.create_room("main", tmp_path / "main_project")
    main.council.chat.post(None, "this belongs to the main room only")

    side = world.branch_room("main", "side")

    assert side.council.chat.messages == []
    assert side.council.chat is not main.council.chat


def test_editing_the_side_room_never_touches_the_parent_files(tmp_path):
    world = World()
    main = world.create_room("main", tmp_path / "main_project")
    (main.project_dir / "app.py").write_text("x = 1\n")
    side = world.branch_room("main", "side")

    codex_seat = Seat.create("Codex", SeatKind.AI)
    side.council.register_ai_seat(MockSeat(codex_seat, reply="proposing"))
    side.council.propose_change(codex_seat.seat_id, "app.py", "x = 2\n")
    side.council.approve_and_apply("app.py")

    assert (side.project_dir / "app.py").read_text() == "x = 2\n"
    assert (main.project_dir / "app.py").read_text() == "x = 1\n"


def test_branch_room_of_unknown_parent_raises(tmp_path):
    world = World()
    with pytest.raises(RoomNotFoundError):
        world.branch_room("nope", "side")


def test_branch_room_with_duplicate_side_name_raises(tmp_path):
    world = World()
    world.create_room("main", tmp_path / "main_project")
    world.create_room("side", tmp_path / "already_here")
    with pytest.raises(RoomAlreadyExistsError):
        world.branch_room("main", "side")


def test_a_proven_side_room_change_can_be_reapplied_to_the_parent(tmp_path):
    """The intended workflow: test something in a side room, then once
    it's good, redo the same propose_change/approve_and_apply against
    the parent room -- no automatic merge, just the same gated flow
    applied twice, once to validate and once for real."""
    world = World()
    main = world.create_room("main", tmp_path / "main_project")
    (main.project_dir / "app.py").write_text("x = 1\n")
    side = world.branch_room("main", "side")

    codex_seat = Seat.create("Codex", SeatKind.AI)
    side.council.register_ai_seat(MockSeat(codex_seat, reply="proposing"))
    side.council.propose_change(codex_seat.seat_id, "app.py", "x = 2\n")
    side.council.approve_and_apply("app.py")
    result = TestWorker(side.project_dir, command=["python3", "-c", "assert open('app.py').read() == 'x = 2\\n'"]).run()
    assert result.passed

    main_codex_seat = Seat.create("Codex", SeatKind.AI)
    main.council.register_ai_seat(MockSeat(main_codex_seat, reply="proposing (validated in side room)"))
    main.council.propose_change(main_codex_seat.seat_id, "app.py", "x = 2\n")
    main.council.approve_and_apply("app.py")

    assert (main.project_dir / "app.py").read_text() == "x = 2\n"


def test_create_room_can_wrap_an_existing_council(tmp_path):
    """Used by tui.py to fold an already-constructed Council (e.g. from
    demo_council()) into a World as its first room, without discarding
    whatever seats were already registered on it."""
    project_dir = tmp_path / "main_project"
    project_dir.mkdir()
    council = Council(CouncilChat(), PatchWorker(project_dir))
    council.register_ai_seat(MockSeat(Seat.create("Codex", SeatKind.AI), reply="hi"))

    world = World()
    room = world.create_room("main", project_dir, council=council)

    assert room.council is council
    assert len(room.council.chat.seats) == 1
