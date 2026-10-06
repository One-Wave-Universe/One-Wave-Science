"""
Transient Measurements — Layer 05 Extension

Extracts time-series data from transient simulation history.
Complements DC measurements.py for dynamic circuit validation.

These measurements never mutate simulation state and can be called
on historical data without affecting the circuit's behavior.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional
import math


@dataclass
class TimeSeries:
    """A time-indexed data series."""
    times: List[float]  # seconds
    values: List[float]  # voltage/current/power
    unit: str  # "V", "A", "W", etc.

    def __len__(self) -> int:
        return len(self.times)

    def __getitem__(self, idx: int) -> Tuple[float, float]:
        """Return (time, value) at index."""
        return (self.times[idx], self.values[idx])

    def min(self) -> float:
        return min(self.values) if self.values else 0.0

    def max(self) -> float:
        return max(self.values) if self.values else 0.0

    def mean(self) -> float:
        return sum(self.values) / len(self.values) if self.values else 0.0

    def steady_state(self, last_n: int = 100) -> float:
        """Return average of last N samples (for steady-state convergence check)."""
        if not self.values:
            return 0.0
        return sum(self.values[-last_n:]) / min(last_n, len(self.values))

    def rms(self) -> float:
        """Root mean square."""
        if not self.values:
            return 0.0
        return math.sqrt(sum(v*v for v in self.values) / len(self.values))

    def peak_to_peak(self) -> float:
        """Max - Min."""
        if not self.values:
            return 0.0
        return self.max() - self.min()

    def energy(self, dt: float) -> float:
        """Integrated energy: sum of power * dt (for power series)."""
        if not self.values:
            return 0.0
        return sum(self.values) * dt

    def export_csv(self, filename: str) -> None:
        """Export to CSV for external analysis."""
        with open(filename, 'w') as f:
            f.write(f"time_s,{self.unit}\n")
            for t, v in zip(self.times, self.values):
                f.write(f"{t:.6e},{v:.6e}\n")


class TransientMeasurementRecorder:
    """Records time-series data during transient simulation."""

    def __init__(self):
        self.node_voltages: Dict[str, TimeSeries] = {}
        self.source_currents: Dict[str, TimeSeries] = {}
        self.inductor_currents: Dict[str, TimeSeries] = {}
        self.capacitor_voltages: Dict[str, TimeSeries] = {}
        self.mosfet_states: Dict[str, List[Tuple[float, bool]]] = {}

    def record_step(self,
                    time: float,
                    voltages: Dict[str, float],
                    source_currents: Dict[str, float],
                    inductor_states: Dict[str, 'InductorState'],
                    capacitor_states: Dict[str, 'CapacitorState'],
                    mosfet_states: Dict[str, 'MOSFETState']) -> None:
        """Record one timestep of simulation data."""

        # Node voltages
        for node_id, voltage in voltages.items():
            if node_id not in self.node_voltages:
                self.node_voltages[node_id] = TimeSeries(times=[], values=[], unit="V")
            self.node_voltages[node_id].times.append(time)
            self.node_voltages[node_id].values.append(voltage)

        # Source currents
        for src_id, current in source_currents.items():
            if src_id not in self.source_currents:
                self.source_currents[src_id] = TimeSeries(times=[], values=[], unit="A")
            self.source_currents[src_id].times.append(time)
            self.source_currents[src_id].values.append(current)

        # Inductor currents
        for ind_id, ind_state in inductor_states.items():
            if ind_id not in self.inductor_currents:
                self.inductor_currents[ind_id] = TimeSeries(times=[], values=[], unit="A")
            self.inductor_currents[ind_id].times.append(time)
            self.inductor_currents[ind_id].values.append(ind_state.current)

        # Capacitor voltages
        for cap_id, cap_state in capacitor_states.items():
            if cap_id not in self.capacitor_voltages:
                self.capacitor_voltages[cap_id] = TimeSeries(times=[], values=[], unit="V")
            self.capacitor_voltages[cap_id].times.append(time)
            self.capacitor_voltages[cap_id].values.append(cap_state.voltage)

        # MOSFET on/off states
        for mosfet_id, mosfet_state in mosfet_states.items():
            if mosfet_id not in self.mosfet_states:
                self.mosfet_states[mosfet_id] = []
            self.mosfet_states[mosfet_id].append((time, mosfet_state.is_on))

    def get_node_voltage(self, node_id: str) -> Optional[TimeSeries]:
        """Get voltage waveform for a node."""
        return self.node_voltages.get(node_id)

    def get_differential_voltage(self, node_a: str, node_b: str) -> Optional[TimeSeries]:
        """Get V(node_a) - V(node_b) over time."""
        if node_a not in self.node_voltages or node_b not in self.node_voltages:
            return None

        ts_a = self.node_voltages[node_a]
        ts_b = self.node_voltages[node_b]

        if len(ts_a) != len(ts_b):
            return None

        diff_values = [a - b for a, b in zip(ts_a.values, ts_b.values)]
        return TimeSeries(times=ts_a.times, values=diff_values, unit="V")

    def get_source_power(self, src_id: str, source_voltage: float) -> Optional[TimeSeries]:
        """Get P = V*I over time for a source."""
        if src_id not in self.source_currents:
            return None

        ts = self.source_currents[src_id]
        power_values = [source_voltage * i for i in ts.values]
        return TimeSeries(times=ts.times, values=power_values, unit="W")

    def get_mosfet_duty_cycle(self, mosfet_id: str) -> float:
        """Calculate duty cycle (on_time / total_time)."""
        if mosfet_id not in self.mosfet_states:
            return 0.0

        states = self.mosfet_states[mosfet_id]
        if len(states) < 2:
            return 0.0

        t_start = states[0][0]
        t_end = states[-1][0]
        total_time = t_end - t_start

        if total_time <= 0:
            return 0.0

        on_time = 0.0
        for i in range(len(states) - 1):
            t1, is_on_1 = states[i]
            t2, is_on_2 = states[i + 1]
            if is_on_1:
                on_time += t2 - t1

        return on_time / total_time

    def get_mosfet_switch_count(self, mosfet_id: str) -> int:
        """Count number of on→off or off→on transitions."""
        if mosfet_id not in self.mosfet_states:
            return 0

        states = self.mosfet_states[mosfet_id]
        if len(states) < 2:
            return 0

        switches = 0
        for i in range(len(states) - 1):
            if states[i][1] != states[i + 1][1]:
                switches += 1

        return switches

    def get_steady_state_deviation(self, node_id: str, target_voltage: float,
                                   last_n_percent: float = 0.1) -> float:
        """Get max deviation from target in the last N% of samples (steady-state check)."""
        if node_id not in self.node_voltages:
            return float('inf')

        ts = self.node_voltages[node_id]
        if not ts.values:
            return float('inf')

        start_idx = int(len(ts.values) * (1.0 - last_n_percent))
        steady_values = ts.values[start_idx:]

        if not steady_values:
            return float('inf')

        return max(abs(v - target_voltage) for v in steady_values)

    def summary(self) -> str:
        """Return a summary of recorded data."""
        summary = "=== Transient Measurement Summary ===\n"

        summary += f"\nNode Voltages ({len(self.node_voltages)} nodes):\n"
        for node_id, ts in sorted(self.node_voltages.items()):
            summary += f"  {node_id}: min={ts.min():.3f}V, max={ts.max():.3f}V, " \
                      f"mean={ts.mean():.3f}V, steady={ts.steady_state():.3f}V\n"

        summary += f"\nSource Currents ({len(self.source_currents)} sources):\n"
        for src_id, ts in sorted(self.source_currents.items()):
            summary += f"  {src_id}: min={ts.min():.3e}A, max={ts.max():.3e}A, " \
                      f"mean={ts.mean():.3e}A\n"

        summary += f"\nInductor Currents ({len(self.inductor_currents)} inductors):\n"
        for ind_id, ts in sorted(self.inductor_currents.items()):
            summary += f"  {ind_id}: min={ts.min():.3e}A, max={ts.max():.3e}A, " \
                      f"mean={ts.mean():.3e}A\n"

        summary += f"\nMOSFET States ({len(self.mosfet_states)} MOSFETs):\n"
        for mosfet_id in sorted(self.mosfet_states.keys()):
            duty = self.get_mosfet_duty_cycle(mosfet_id)
            switches = self.get_mosfet_switch_count(mosfet_id)
            summary += f"  {mosfet_id}: duty_cycle={duty:.1%}, switches={switches}\n"

        return summary

    def export_json(self, filename: str) -> None:
        """Export all time-series data to JSON."""
        import json

        data = {
            "node_voltages": {
                node_id: {
                    "times": ts.times,
                    "values": ts.values,
                    "unit": ts.unit,
                    "stats": {
                        "min": ts.min(),
                        "max": ts.max(),
                        "mean": ts.mean(),
                        "rms": ts.rms(),
                        "peak_to_peak": ts.peak_to_peak()
                    }
                }
                for node_id, ts in self.node_voltages.items()
            },
            "source_currents": {
                src_id: {
                    "times": ts.times,
                    "values": ts.values,
                    "unit": ts.unit,
                    "stats": {
                        "min": ts.min(),
                        "max": ts.max(),
                        "mean": ts.mean(),
                        "rms": ts.rms()
                    }
                }
                for src_id, ts in self.source_currents.items()
            },
            "inductor_currents": {
                ind_id: {
                    "times": ts.times,
                    "values": ts.values,
                    "unit": ts.unit,
                    "stats": {
                        "min": ts.min(),
                        "max": ts.max(),
                        "mean": ts.mean(),
                        "peak_to_peak": ts.peak_to_peak()
                    }
                }
                for ind_id, ts in self.inductor_currents.items()
            },
            "mosfet_duty_cycles": {
                mosfet_id: self.get_mosfet_duty_cycle(mosfet_id)
                for mosfet_id in self.mosfet_states.keys()
            }
        }

        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
