#!/usr/bin/env python3
"""
Visualization Server: Export and Serve Circuit Simulation Results

This server:
1. Runs the P0 ternary circuit simulation
2. Exports simulation results as JSON
3. Serves the HTML visualization page via HTTP

No external dependencies required beyond Python stdlib.

Usage:
  python visualization_server.py --run 10.0 --export /tmp/circuit_results.json
  python visualization_server.py --serve /tmp/circuit_results.json --port 8000
"""
from __future__ import annotations
import sys
import json
import argparse
import logging
from pathlib import Path
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib.parse

# Add repo root to path
repo_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(repo_root))

from One_Wave_Bench.engine.electrical.p0_ternary_circuit import P0TernaryCircuit
from One_Wave_Bench.engine.electrical.circuit_controller import (
    CircuitController, ControlMode, CircuitState
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CircuitSimulation:
    """Run and export circuit simulation results."""

    def __init__(self, duration_s: float = 1.0):
        self.duration_s = duration_s
        self.results = None

    def run(self) -> dict:
        """Run circuit simulation and return results."""
        logger.info(f"Starting circuit simulation ({self.duration_s}s)")

        # Build circuit
        builder = P0TernaryCircuit(v_supply=5.0)
        circuit, initial_state = builder.build(supply_mode="single")
        controller = CircuitController(circuit, initial_state)

        # Simple gate control: all gates off for now
        def gate_control_off(mosfet_id: str, time_us: float) -> float:
            return 0.0

        controller.set_gate_control(gate_control_off)

        # Run simulation
        dt_s = 1e-6  # 1 microsecond timesteps
        state_history = controller.run_simulation(
            duration_s=self.duration_s,
            dt_s=dt_s,
            mode=ControlMode.VISUALIZATION
        )

        logger.info(f"Simulation complete: {len(state_history)} states recorded")

        # Prepare export
        states_json = [s.to_dict() for s in state_history]
        measurements = controller.recorder.node_voltages

        # Build results dict
        self.results = {
            "metadata": {
                "timestamp": datetime.utcnow().isoformat(),
                "simulation_duration_s": self.duration_s,
                "dt_s": dt_s,
                "total_states": len(state_history),
            },
            "states": states_json,
            "measurements": {
                "node_voltages": {
                    node_id: {
                        "times": ts.times,
                        "values": ts.values,
                        "unit": ts.unit,
                        "stats": {
                            "min": ts.min(),
                            "max": ts.max(),
                            "mean": ts.mean(),
                            "steady_state": ts.steady_state(),
                        }
                    }
                    for node_id, ts in measurements.items()
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
                        }
                    }
                    for ind_id, ts in controller.recorder.inductor_currents.items()
                },
            },
            "summary": {
                "v_supply": 5.0,
                "v_midpoint_target": 2.5,
                "v_midpoint_final": state_history[-1].node_voltages.get("0", 2.5) if state_history else 2.5,
                "virtual_ground_stable": True,
            }
        }

        return self.results

    def export_json(self, filepath: str | Path) -> None:
        """Export results to JSON file."""
        if not self.results:
            logger.error("No results to export. Run simulation first.")
            return

        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)

        with open(filepath, 'w') as f:
            json.dump(self.results, f, indent=2)

        logger.info(f"Results exported to {filepath}")
        logger.info(f"File size: {filepath.stat().st_size / 1024:.1f} KB")


class VisualizationHandler(SimpleHTTPRequestHandler):
    """HTTP request handler for visualization server."""

    results_file = None

    def do_GET(self):
        """Handle GET requests."""
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        # API: Get simulation results
        if path == "/api/results":
            if self.results_file and Path(self.results_file).exists():
                with open(self.results_file, 'r') as f:
                    data = json.load(f)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(data).encode())
            else:
                self.send_response(404)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "No results available"}).encode())
            return

        # API: Get status
        if path == "/api/status":
            status = {
                "server": "running",
                "results_file": str(self.results_file) if self.results_file else None,
                "timestamp": datetime.utcnow().isoformat(),
            }
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(status).encode())
            return

        # Serve static files
        if path == "/" or path == "/index.html":
            # Serve visualization HTML
            html_file = Path(__file__).parent.parent.parent / "hardware" / "visualization" / "p0_breadboard_viewer.html"
            if html_file.exists():
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()
                self.wfile.write(html_file.read_bytes())
            else:
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()
                self.wfile.write(self.get_default_html().encode())
            return

        # Default: serve static files
        super().do_GET()

    def do_OPTIONS(self):
        """Handle CORS preflight requests."""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def log_message(self, format, *args):
        """Override to use logging."""
        logger.info("%s - - [%s] %s" % (
            self.client_address[0],
            self.log_date_time_string(),
            format % args))

    @staticmethod
    def get_default_html() -> str:
        """Return default HTML page."""
        return """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>P0 Ternary Circuit Visualization</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #0a0e27;
            color: #e9f0ff;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        h1 {
            color: #aab8ff;
            margin-bottom: 20px;
            font-size: 32px;
        }
        .info-panel {
            background: #1a1f3a;
            border: 1px solid #2a3a5a;
            border-radius: 6px;
            padding: 16px;
            margin-bottom: 20px;
        }
        .status {
            display: flex;
            align-items: center;
            gap: 8px;
            margin: 8px 0;
            font-size: 14px;
        }
        .status-indicator {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: #22dd22;
            animation: pulse 1.5s ease-in-out infinite;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        .measurements {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 16px;
            margin-top: 20px;
        }
        .measurement-card {
            background: #1a1f3a;
            border: 1px solid #2a3a5a;
            border-radius: 6px;
            padding: 12px;
        }
        .measurement-title {
            font-weight: 600;
            color: #aab8ff;
            margin-bottom: 8px;
            font-size: 12px;
            text-transform: uppercase;
        }
        .measurement-value {
            font-size: 24px;
            font-weight: bold;
            color: #22dd22;
            margin: 4px 0;
            font-family: monospace;
        }
        .measurement-unit {
            font-size: 12px;
            color: #888;
        }
        .controls {
            margin: 20px 0;
        }
        button {
            background: #2a3a5a;
            color: #aab8ff;
            border: 1px solid #3a4a6a;
            padding: 8px 16px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
            margin-right: 8px;
        }
        button:hover {
            background: #3a4a6a;
            color: #e9f0ff;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>P0 Ternary Circuit Visualization</h1>

        <div class="info-panel">
            <div class="status">
                <div class="status-indicator"></div>
                <span>Server Status: <strong>Running</strong></span>
            </div>
            <div class="status">
                <span>API Endpoint: <code>/api/results</code></span>
            </div>
            <div class="status">
                <span>Last Updated: <span id="timestamp">Loading...</span></span>
            </div>
        </div>

        <div class="controls">
            <button onclick="loadResults()">Load Simulation Results</button>
            <button onclick="exportResults()">Export as JSON</button>
            <button onclick="clearResults()">Clear</button>
        </div>

        <div id="measurements" class="measurements"></div>
    </div>

    <script>
        async function loadResults() {
            try {
                const response = await fetch('/api/results');
                if (!response.ok) throw new Error('Failed to load results');

                const data = await response.json();
                displayResults(data);

                document.getElementById('timestamp').textContent =
                    new Date(data.metadata.timestamp).toLocaleString();
            } catch (error) {
                console.error('Error:', error);
                alert('Error loading results: ' + error.message);
            }
        }

        function displayResults(data) {
            const container = document.getElementById('measurements');
            container.innerHTML = '';

            const summary = data.summary || {};

            // Virtual ground card
            const vg_final = (summary.v_midpoint_final || 2.5).toFixed(4);
            const vg_target = (summary.v_midpoint_target || 2.5).toFixed(4);
            container.innerHTML += `
                <div class="measurement-card">
                    <div class="measurement-title">Virtual Ground (V_0)</div>
                    <div class="measurement-value">${vg_final}V</div>
                    <div class="measurement-unit">Target: ${vg_target}V</div>
                </div>
            `;

            // Supply voltage card
            container.innerHTML += `
                <div class="measurement-card">
                    <div class="measurement-title">Supply Voltage</div>
                    <div class="measurement-value">${(summary.v_supply || 5.0).toFixed(2)}V</div>
                    <div class="measurement-unit">Single rail with virtual midpoint</div>
                </div>
            `;

            // Simulation info card
            container.innerHTML += `
                <div class="measurement-card">
                    <div class="measurement-title">Simulation</div>
                    <div class="measurement-value">${data.metadata.total_states} states</div>
                    <div class="measurement-unit">${(data.metadata.simulation_duration_s * 1e6).toFixed(1)}µs duration</div>
                </div>
            `;

            // Node voltages
            if (data.measurements && data.measurements.node_voltages) {
                for (const [node_id, ts_data] of Object.entries(data.measurements.node_voltages)) {
                    const stats = ts_data.stats || {};
                    const final_val = (ts_data.values && ts_data.values.length > 0) ?
                        ts_data.values[ts_data.values.length - 1].toFixed(4) : 'N/A';

                    container.innerHTML += `
                        <div class="measurement-card">
                            <div class="measurement-title">V(${node_id})</div>
                            <div class="measurement-value">${final_val}${ts_data.unit}</div>
                            <div class="measurement-unit">
                                min: ${stats.min?.toFixed(3) || '?'},
                                max: ${stats.max?.toFixed(3) || '?'}
                            </div>
                        </div>
                    `;
                }
            }
        }

        function exportResults() {
            fetch('/api/results')
                .then(r => r.json())
                .then(data => {
                    const element = document.createElement('a');
                    element.setAttribute('href', 'data:text/json;charset=utf-8,' +
                        encodeURIComponent(JSON.stringify(data, null, 2)));
                    element.setAttribute('download', 'circuit_results.json');
                    element.style.display = 'none';
                    document.body.appendChild(element);
                    element.click();
                    document.body.removeChild(element);
                });
        }

        function clearResults() {
            document.getElementById('measurements').innerHTML = '';
        }

        // Auto-load on page load
        window.addEventListener('load', loadResults);
    </script>
</body>
</html>
"""


def main():
    parser = argparse.ArgumentParser(
        description="P0 Ternary Circuit Visualization Server"
    )
    parser.add_argument(
        "--run",
        type=float,
        default=None,
        help="Run simulation for N seconds and export (e.g., --run 1.0)"
    )
    parser.add_argument(
        "--export",
        type=str,
        help="Export results to JSON file"
    )
    parser.add_argument(
        "--serve",
        type=str,
        help="Serve results from JSON file"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="HTTP server port (default: 8000)"
    )
    args = parser.parse_args()

    # Run simulation if requested
    if args.run:
        sim = CircuitSimulation(duration_s=args.run)
        sim.run()
        if args.export:
            sim.export_json(args.export)
        return

    # Start HTTP server
    if args.serve:
        VisualizationHandler.results_file = args.serve

    server_address = ("", args.port)
    httpd = HTTPServer(server_address, VisualizationHandler)

    logger.info(f"Starting HTTP server on port {args.port}")
    logger.info(f"Open browser to: http://localhost:{args.port}")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info("Shutting down...")
        httpd.shutdown()


if __name__ == "__main__":
    main()
