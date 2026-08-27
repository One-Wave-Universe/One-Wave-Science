"""Jetson Orin deployment profile and non-destructive hardware preflight."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import os
from pathlib import Path
import platform
import shutil


MODEL_PATH = Path("/proc/device-tree/model")


@dataclass(frozen=True, slots=True)
class JetsonProfile:
    machine: str
    model: str
    is_jetson: bool
    gpu_available: bool
    accelerator_available: bool
    expressive_device: str
    compressive_device: str
    m4_device: str

    @property
    def hardware_split_ready(self) -> bool:
        return self.is_jetson and self.gpu_available

    @property
    def receipt(self) -> dict[str, object]:
        return {**asdict(self), "hardware_split_ready": self.hardware_split_ready}


def _read_model() -> str:
    try:
        return MODEL_PATH.read_bytes().rstrip(b"\x00").decode("utf-8", "replace")
    except OSError:
        return platform.platform()


def detect_jetson() -> JetsonProfile:
    model = _read_model()
    machine = platform.machine()
    is_jetson = "jetson" in model.lower() or "orin" in model.lower()
    gpu_available = any(Path(path).exists() for path in (
        "/dev/nvhost-gpu",
        "/usr/local/cuda",
        "/sys/devices/gpu.0",
    )) or shutil.which("tegrastats") is not None
    accelerator_available = any(Path(path).exists() for path in (
        "/dev/nvhost-dla0",
        "/dev/nvhost-dla1",
    ))
    return JetsonProfile(
        machine=machine,
        model=model,
        is_jetson=is_jetson,
        gpu_available=gpu_available,
        accelerator_available=accelerator_available,
        expressive_device="JETSON_GPU" if gpu_available else "CPU_FALLBACK",
        compressive_device="JETSON_CPU" if is_jetson else "CPU_REFERENCE",
        m4_device="JETSON_ACCELERATOR" if accelerator_available else "CPU_REFERENCE",
    )


def default_brain_home() -> Path:
    configured = os.environ.get("ONE_WAVE_BRAIN_HOME")
    return Path(configured).expanduser() if configured else Path.home() / ".local/share/one-wave-brain"

