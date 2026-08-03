import pytest

from council_chamber.models import CouncilChat, Seat, SeatKind
from council_chamber.seats.ai_seat import MockSeat, RemoteAPISeat
from council_chamber.usage import UsageReport, summarize
from council_chamber.workers.patch_worker import PatchWorker
from council_chamber.orchestrator import Council


def test_unavailable_report_leaves_numbers_none():
    report = UsageReport.unavailable()

    assert report.input_tokens is None
    assert report.output_tokens is None
    assert report.note == "usage unavailable"


def test_mock_seat_reports_unavailable_after_responding():
    seat = MockSeat(Seat.create("Claude", SeatKind.AI), reply="hi")

    seat.respond([])

    assert seat.last_usage is not None
    assert seat.last_usage.input_tokens is None
    assert "mock" in seat.last_usage.note


def test_remote_api_seat_with_tuple_client_reports_real_usage():
    def client(context):
        return "the answer", UsageReport(input_tokens=42, output_tokens=7, requests=1)

    seat = RemoteAPISeat(Seat.create("ChatGPT", SeatKind.AI), client=client)

    reply = seat.respond([])

    assert reply == "the answer"
    assert seat.last_usage.input_tokens == 42
    assert seat.last_usage.output_tokens == 7


def test_remote_api_seat_with_bare_string_client_reports_unavailable():
    seat = RemoteAPISeat(Seat.create("Gemini", SeatKind.AI), client=lambda context: "sure")

    seat.respond([])

    assert seat.last_usage.note == "client did not report usage"


def test_summarize_sums_known_values_and_ignores_missing():
    reports = [
        UsageReport(input_tokens=10, output_tokens=5),
        UsageReport.unavailable(),
        UsageReport(input_tokens=20, output_tokens=8, estimated_price_usd=0.01),
    ]

    summary = summarize(reports)

    assert summary["input_tokens"] == 30
    assert summary["output_tokens"] == 13
    assert summary["estimated_price_usd"] == pytest.approx(0.01)
    assert summary["total_requests"] == 3
    assert summary["reports_without_data"] == 1


def test_summarize_with_no_known_values_returns_none_not_zero():
    summary = summarize([UsageReport.unavailable(), UsageReport.unavailable()])

    assert summary["input_tokens"] is None
    assert summary["output_tokens"] is None
    assert summary["reports_without_data"] == 2


def test_council_ask_records_usage_per_seat(tmp_path):
    chat = CouncilChat()
    council = Council(chat, PatchWorker(tmp_path))
    seat = Seat.create("Claude", SeatKind.AI)
    council.register_ai_seat(MockSeat(seat, reply="ok"))

    council.ask([seat.seat_id], "hello")
    council.ask([seat.seat_id], "again")

    reports = council.usage_for(seat.seat_id)
    assert len(reports) == 2
    assert all(r.note is not None for r in reports)


def test_council_usage_for_unknown_seat_returns_empty_list(tmp_path):
    council = Council(CouncilChat(), PatchWorker(tmp_path))

    assert council.usage_for("seat_ghost") == []
