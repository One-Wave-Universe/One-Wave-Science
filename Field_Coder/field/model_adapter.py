"""Provider-neutral model seat for Field Coder Step 12."""

from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Protocol
from urllib import request as urllib_request
from urllib.error import URLError


class ModelAdapterError(RuntimeError):
    """Raised when a model adapter cannot satisfy the Field model contract."""


@dataclass(frozen=True)
class ModelRequest:
    system_prompt: str
    user_prompt: str

    def validate(self) -> None:
        if not self.system_prompt.strip():
            raise ModelAdapterError("system prompt must not be empty")
        if not self.user_prompt.strip():
            raise ModelAdapterError("user prompt must not be empty")


@dataclass(frozen=True)
class ModelResponse:
    text: str
    model: str
    adapter: str

    def validate(self) -> None:
        if not self.text.strip():
            raise ModelAdapterError("model response text must not be empty")
        if not self.model.strip():
            raise ModelAdapterError("model name must not be empty")
        if not self.adapter.strip():
            raise ModelAdapterError("adapter name must not be empty")


class ModelAdapter(Protocol):
    def complete(self, model_request: ModelRequest) -> ModelResponse:
        """Return one structured model response."""


@dataclass(frozen=True)
class FakeModelAdapter:
    response_text: str
    model_name: str = "fake-model"
    adapter_name: str = "fake"

    def complete(self, model_request: ModelRequest) -> ModelResponse:
        model_request.validate()
        response = ModelResponse(
            text=self.response_text,
            model=self.model_name,
            adapter=self.adapter_name,
        )
        response.validate()
        return response


@dataclass(frozen=True)
class LocalOpenAICompatibleAdapter:
    endpoint: str
    model_name: str
    timeout_seconds: float = 30.0
    adapter_name: str = "local-openai-compatible"

    def complete(self, model_request: ModelRequest) -> ModelResponse:
        model_request.validate()
        if not self.endpoint.strip():
            raise ModelAdapterError("local endpoint must not be empty")
        if not self.model_name.strip():
            raise ModelAdapterError("local model name must not be empty")
        if self.timeout_seconds <= 0:
            raise ModelAdapterError("timeout_seconds must be greater than zero")

        payload = json.dumps(
            {
                "model": self.model_name,
                "messages": [
                    {"role": "system", "content": model_request.system_prompt},
                    {"role": "user", "content": model_request.user_prompt},
                ],
                "stream": False,
            }
        ).encode("utf-8")
        req = urllib_request.Request(
            self.endpoint,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib_request.urlopen(req, timeout=self.timeout_seconds) as response:
                body = response.read().decode("utf-8")
        except (OSError, URLError) as exc:
            raise ModelAdapterError(f"local model request failed: {exc}") from exc

        try:
            parsed = json.loads(body)
            text = parsed["choices"][0]["message"]["content"]
            returned_model = str(parsed.get("model") or self.model_name)
        except (json.JSONDecodeError, KeyError, IndexError, TypeError) as exc:
            raise ModelAdapterError("local model returned invalid OpenAI-compatible response") from exc

        response = ModelResponse(
            text=str(text),
            model=returned_model,
            adapter=self.adapter_name,
        )
        response.validate()
        return response


def run_model(adapter: ModelAdapter, model_request: ModelRequest) -> ModelResponse:
    """Invoke any adapter through the single Field model seat."""
    model_request.validate()
    response = adapter.complete(model_request)
    if not isinstance(response, ModelResponse):
        raise ModelAdapterError("adapter returned wrong response type")
    response.validate()
    return response
