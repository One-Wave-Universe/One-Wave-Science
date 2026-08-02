"""Timestamped multichannel ring buffer (Section 5.4 / 5.5).

This is a thread-safe reference implementation, not the lock-free SPSC
buffer the production C++ engine requires (Section 2.4) -- Python's GIL
and the coarse lock here are adequate for prototyping and testing the
surrounding DSP, but the real-time audio callback in the production
engine must use an actual lock-free structure.
"""

from __future__ import annotations

import threading
import time

import numpy as np


class RingBuffer:
    def __init__(self, num_channels: int, capacity_samples: int, sample_rate: float):
        if capacity_samples <= 0:
            raise ValueError("capacity_samples must be positive")
        if num_channels <= 0:
            raise ValueError("num_channels must be positive")

        self.num_channels = num_channels
        self.capacity = capacity_samples
        self.sample_rate = sample_rate

        self._data = np.zeros((num_channels, capacity_samples), dtype=np.float32)
        self._write_pos = 0
        self._total_written = 0
        self._lock = threading.Lock()
        self._first_write_host_time: float | None = None

    def write(self, block: np.ndarray) -> int:
        """Write a (channels, n) or (n,) block. Returns absolute sample index of its first sample."""
        block = np.atleast_2d(block)
        if block.shape[0] != self.num_channels:
            if block.shape[0] == 1 and self.num_channels > 1:
                block = np.repeat(block, self.num_channels, axis=0)
            else:
                raise ValueError(
                    f"block has {block.shape[0]} channels, buffer has {self.num_channels}"
                )

        n = block.shape[1]
        with self._lock:
            if self._first_write_host_time is None:
                self._first_write_host_time = time.monotonic()

            first_abs_index = self._total_written

            if n >= self.capacity:
                self._data[:, :] = block[:, -self.capacity:]
                self._write_pos = 0
            else:
                end = self._write_pos + n
                if end <= self.capacity:
                    self._data[:, self._write_pos:end] = block
                else:
                    first_part = self.capacity - self._write_pos
                    self._data[:, self._write_pos:] = block[:, :first_part]
                    self._data[:, : n - first_part] = block[:, first_part:]
                self._write_pos = (self._write_pos + n) % self.capacity

            self._total_written += n
            return first_abs_index

    @property
    def total_written(self) -> int:
        with self._lock:
            return self._total_written

    def available_range(self) -> tuple[int, int]:
        """Return (oldest_abs_index, newest_abs_index_exclusive) currently retained."""
        with self._lock:
            newest = self._total_written
            oldest = max(0, newest - self.capacity)
            return oldest, newest

    def read_latest(self, n_samples: int) -> np.ndarray:
        with self._lock:
            n_samples = min(n_samples, self._total_written, self.capacity)
            if n_samples <= 0:
                return np.zeros((self.num_channels, 0), dtype=np.float32)
            start = (self._write_pos - n_samples) % self.capacity
            end = start + n_samples
            if end <= self.capacity:
                return self._data[:, start:end].copy()
            first_part = self.capacity - start
            out = np.empty((self.num_channels, n_samples), dtype=np.float32)
            out[:, :first_part] = self._data[:, start:]
            out[:, first_part:] = self._data[:, : n_samples - first_part]
            return out

    def read_range(self, start_abs_index: int, end_abs_index: int) -> np.ndarray:
        """Read [start_abs_index, end_abs_index) using absolute sample indices.

        Samples that have already fallen outside the retained window are
        silently clipped from the request rather than raising, since the
        ring buffer's job is to hold recent history, not guarantee
        arbitrary lookback.
        """
        with self._lock:
            oldest, newest = max(0, self._total_written - self.capacity), self._total_written
            start_abs_index = max(start_abs_index, oldest)
            end_abs_index = min(end_abs_index, newest)
            if end_abs_index <= start_abs_index:
                return np.zeros((self.num_channels, 0), dtype=np.float32)

            samples_back_from_newest = newest - start_abs_index
            n = end_abs_index - start_abs_index
            start = (self._write_pos - samples_back_from_newest) % self.capacity
            end = start + n
            if end <= self.capacity:
                return self._data[:, start:end].copy()
            first_part = self.capacity - start
            out = np.empty((self.num_channels, n), dtype=np.float32)
            out[:, :first_part] = self._data[:, start:]
            out[:, first_part:] = self._data[:, : n - first_part]
            return out
