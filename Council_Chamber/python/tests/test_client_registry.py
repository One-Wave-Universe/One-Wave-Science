import pytest

from council_chamber.client_registry import (
    build_ai_seat,
    discover_and_register_clients,
    find_client_for_name,
    get_client,
    register_client,
    registered_clients,
)
from council_chamber.models import Seat, SeatKind
from council_chamber.seats.ai_seat import MockSeat, RemoteAPISeat


@pytest.fixture(autouse=True)
def _isolated_registry():
    """Restore the registry to whatever it held before each test, so a
    test's own registrations (e.g. "widget") never leak into other
    tests -- but real, ambient registrations from module imports (e.g.
    gemini_client.py's own self-registration) are left alone, matching
    how the registry actually behaves in real use."""
    import council_chamber.client_registry as registry_module

    original = dict(registry_module._REGISTRY)
    yield
    registry_module._REGISTRY.clear()
    registry_module._REGISTRY.update(original)


def test_register_and_get_client_round_trips():
    register_client("widget", "Widget AI", lambda: (lambda context: "hi"))

    registered = get_client("widget")

    assert registered is not None
    assert registered.display_name == "Widget AI"


def test_get_client_is_case_insensitive():
    register_client("Widget", "Widget AI", lambda: (lambda context: "hi"))
    assert get_client("WIDGET") is not None


def test_get_client_for_unregistered_key_returns_none():
    assert get_client("nope") is None


def test_registered_clients_returns_a_copy_not_the_live_dict():
    register_client("widget", "Widget AI", lambda: (lambda context: "hi"))
    snapshot = registered_clients()
    snapshot.clear()
    assert get_client("widget") is not None


def test_later_registration_for_same_key_wins():
    register_client("widget", "Widget AI v1", lambda: (lambda context: "v1"))
    register_client("widget", "Widget AI v2", lambda: (lambda context: "v2"))

    assert get_client("widget").display_name == "Widget AI v2"


def test_find_client_for_name_matches_key_or_display_name():
    register_client("widget", "Widget AI", lambda: (lambda context: "hi"))

    assert find_client_for_name("widget").display_name == "Widget AI"
    assert find_client_for_name("Widget AI").display_name == "Widget AI"
    assert find_client_for_name("WIDGET AI").display_name == "Widget AI"
    assert find_client_for_name("nobody") is None


def test_build_ai_seat_uses_real_client_when_factory_succeeds():
    register_client("widget", "Widget AI", lambda: (lambda context: "real reply"))
    seat = Seat.create("Widget AI", SeatKind.AI)

    ai_seat = build_ai_seat(seat, placeholder_reply="(placeholder)")

    assert isinstance(ai_seat, RemoteAPISeat)
    assert ai_seat.respond([]) == "real reply"


def test_build_ai_seat_falls_back_to_placeholder_when_factory_raises():
    def broken_factory():
        raise RuntimeError("no API key set")

    register_client("widget", "Widget AI", broken_factory)
    seat = Seat.create("Widget AI", SeatKind.AI)

    ai_seat = build_ai_seat(seat, placeholder_reply="(generic placeholder)")

    assert isinstance(ai_seat, MockSeat)
    assert "not configured" in ai_seat.respond([])
    assert "no API key set" in ai_seat.respond([])


def test_build_ai_seat_falls_back_to_generic_placeholder_when_unregistered():
    seat = Seat.create("Nobody Registered", SeatKind.AI)

    ai_seat = build_ai_seat(seat, placeholder_reply="(generic placeholder)")

    assert isinstance(ai_seat, MockSeat)
    assert ai_seat.respond([]) == "(generic placeholder)"


def test_discover_and_register_clients_picks_up_gemini_client():
    discover_and_register_clients()
    assert get_client("gemini") is not None
    assert get_client("gemini").display_name == "Gemini"
