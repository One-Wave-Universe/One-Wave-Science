"""Step 12 provider-neutral model adapter verification."""

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from pathlib import Path
import sys
from threading import Thread

FIELD_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(FIELD_ROOT))

from field.model_adapter import (
    FakeModelAdapter,
    LocalOpenAICompatibleAdapter,
    ModelAdapterError,
    ModelRequest,
    ModelResponse,
    run_model,
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


class FixtureHandler(BaseHTTPRequestHandler):
    malformed = False

    def do_POST(self):  # noqa: N802
        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length)
        payload = json.loads(body.decode("utf-8"))
        require(payload["messages"][0]["role"] == "system", repr(payload))
        require(payload["messages"][1]["role"] == "user", repr(payload))
        require(payload["stream"] is False, repr(payload))

        if self.malformed:
            response = {"not_choices": []}
        else:
            response = {
                "model": payload["model"],
                "choices": [
                    {"message": {"role": "assistant", "content": "LOCAL_RESPONSE"}}
                ],
            }
        encoded = json.dumps(response).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def log_message(self, format, *args):  # noqa: A003
        return


def main() -> int:
    request = ModelRequest(
        system_prompt="Return one bounded coding proposal.",
        user_prompt="Change one fixture output.",
    )

    fake = FakeModelAdapter(response_text="FAKE_RESPONSE")
    fake_result = run_model(fake, request)
    require(isinstance(fake_result, ModelResponse), repr(fake_result))
    require(fake_result.text == "FAKE_RESPONSE", repr(fake_result))
    print("PASS: fake adapter satisfies ModelResponse contract")

    server = HTTPServer(("127.0.0.1", 0), FixtureHandler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        endpoint = f"http://127.0.0.1:{server.server_port}/v1/chat/completions"
        local = LocalOpenAICompatibleAdapter(
            endpoint=endpoint,
            model_name="local-fixture-model",
            timeout_seconds=2.0,
        )
        local_result = run_model(local, request)
        require(isinstance(local_result, ModelResponse), repr(local_result))
        require(local_result.text == "LOCAL_RESPONSE", repr(local_result))
        require(local_result.model == "local-fixture-model", repr(local_result))
        print("PASS: localhost adapter satisfies identical ModelResponse contract")

        adapters = [fake, local]
        texts = [run_model(adapter, request).text for adapter in adapters]
        require(texts == ["FAKE_RESPONSE", "LOCAL_RESPONSE"], repr(texts))
        print("PASS: adapter swap requires no run_model/controller change")

        FixtureHandler.malformed = True
        try:
            run_model(local, request)
        except ModelAdapterError:
            pass
        else:
            raise AssertionError("malformed local response was accepted")
        print("PASS: malformed local response rejected")
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
