import json
import threading
import urllib.request

import pytest

from council_chamber.tui import CouncilTUI, demo_council
from council_chamber.web_ui import (
    execute_command,
    list_seat_catalog,
    provider_setup_info,
    serve,
)


@pytest.fixture
def tui(tmp_path):
    return CouncilTUI(demo_council(tmp_path / "project"))


def test_list_seat_catalog_includes_gemini_and_groq_as_real():
    catalog = {p["key"]: p for p in list_seat_catalog()}
    assert catalog["gemini"]["has_real_client"] is True
    assert catalog["groq"]["has_real_client"] is True


def test_list_seat_catalog_includes_unwired_providers_as_not_real():
    catalog = {p["key"]: p for p in list_seat_catalog()}
    assert catalog["chatgpt"]["has_real_client"] is False
    assert catalog["claude"]["has_real_client"] is False


def test_provider_setup_info_for_a_key_needing_env_var():
    info = provider_setup_info("groq")
    assert info["env_var"] == "GROQ_API_KEY"
    assert info["signup_url"] == "https://console.groq.com/keys"
    assert "GROQ_API_KEY" in info["powershell"]
    assert "paste-your-key-here" in info["powershell"]
    # never a real secret embedded
    assert "sk-" not in info["powershell"]


def test_provider_setup_info_never_lies_about_being_wired():
    assert provider_setup_info("groq")["has_real_client"] is True
    assert provider_setup_info("chatgpt")["has_real_client"] is False


def test_provider_setup_info_for_local_needs_no_env_var():
    info = provider_setup_info("local")
    assert info["env_var"] is None
    assert "no API key needed" in info["powershell"]


def test_provider_setup_info_for_unknown_key_does_not_crash():
    info = provider_setup_info("totally-made-up")
    assert info["signup_url"] is None
    assert info["env_var"] is None


def test_execute_command_wraps_tui_execute(tui):
    result = execute_command(tui, "seats")
    assert "output" in result
    assert "ChatGPT" in result["output"]


def test_execute_command_turns_errors_into_error_field_not_a_crash(tui):
    result = execute_command(tui, "open not-a-real-provider")
    assert "error" in result
    assert "unknown seat" in result["error"]


def test_live_server_serves_the_page_and_executes_real_commands(tui):
    """One real end-to-end check: an actual HTTP server on an OS-assigned
    port, actual HTTP requests, actual responses -- not just testing the
    pure functions in isolation."""
    server = serve(tui, port=0)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        host, port = server.server_address

        with urllib.request.urlopen(f"http://{host}:{port}/", timeout=5) as resp:
            assert resp.status == 200
            assert b"Council Chamber" in resp.read()

        with urllib.request.urlopen(f"http://{host}:{port}/api/providers", timeout=5) as resp:
            providers = json.loads(resp.read())
            assert any(p["key"] == "gemini" for p in providers)

        body = json.dumps({"line": "seats"}).encode()
        req = urllib.request.Request(
            f"http://{host}:{port}/api/execute", data=body,
            headers={"Content-Type": "application/json"}, method="POST",
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            result = json.loads(resp.read())
            assert "ChatGPT" in result["output"]
    finally:
        server.shutdown()
        thread.join(timeout=5)
