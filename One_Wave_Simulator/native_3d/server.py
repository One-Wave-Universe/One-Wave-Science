"""Bounded loopback-only adapter for existing, explicitly hypothetical solvers."""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from dataclasses import asdict, replace
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
import sys
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'solvers'))
import numpy as np
from bulk_excitation import BulkExcitation, BulkCoefficients
from joint_boundary_response import JointResponse, ROLES
from driven_bulk import DrivenBulk

SOURCE_PATHS = ['solvers/driven_bulk.py', 'solvers/test_driven_bulk.py', 'solvers/bulk_excitation.py', 'solvers/joint_boundary_response.py',
                'One_Wave_Simulator/native_3d/server.py',
                'One_Wave_Simulator/native_3d/app.js', 'One_Wave_Simulator/native_3d/index.html',
                'One_Wave_Simulator/native_3d/test_lab.py', 'One_Wave_Simulator/native_3d/test_ui.cjs']
# Bind receipts to bytes present when the executable modules are imported.
STARTUP_SOURCES = {p: hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in SOURCE_PATHS}


def finite(value, low, high, name):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or not low <= value <= high:
        raise ValueError(f'{name} must be finite in [{low}, {high}]')
    return float(value)


def integer(value, low, high, name):
    finite(value, low, high, name)
    if int(value) != value:
        raise ValueError(f'{name} must be an integer')
    return int(value)


class Lab:
    """One state and one command stream. A camera is deliberately absent."""
    def __init__(self):
        self.generation = 0
        self.reset({})

    def reset(self, payload):
        if set(payload) - {'model', 'control', 'side', 'norm', 'kick', 'mode'}:
            raise ValueError('Unknown reset parameter')
        model = payload.get('model', 'bulk')
        if model not in ('bulk', 'cavity'):
            raise ValueError('Unknown model')
        allowed = {'model', 'mode'} if model == 'cavity' else {'model', 'control', 'side', 'norm', 'kick'}
        if set(payload) - allowed:
            raise ValueError('Parameter does not belong to selected model')
        control = payload.get('control', 'coupled')
        if control not in ('coupled', 'linear'):
            raise ValueError('Unknown control')
        side = integer(payload.get('side', 8), 8, 12, 'side')
        if side not in (8, 12):
            raise ValueError('side must be 8 or 12')
        norm = finite(payload.get('norm', 20), 2, 40, 'norm')
        kick = finite(payload.get('kick', .2), -.5, .5, 'kick')
        # Build/validate everything before replacing the accepted state.
        if model == 'bulk':
            coeff = BulkCoefficients()
            if control == 'linear':
                coeff = replace(coeff, focusing=0, saturation=0)
            engine = BulkExcitation(side, coefficients=coeff)
            # Identical Gaussian start for coupled/linear controls; no fitted target.
            field = engine.seed(norm=norm).astype(complex)
            field *= np.exp(1j*kick*engine.xyz[:, 0, None])
            previous = None
            dt = .02
            config = {'model': model, 'control': control, 'side': side, 'norm': norm, 'kick': kick,
                      'coefficients': asdict(coeff), 'initial_condition': 'Gaussian width 1.5; x phase gradient'}
        else:
            engine = JointResponse()
            mode = integer(payload.get('mode', 4), 0, len(engine.eigenvalues)-1, 'mode')
            dt = engine.stable_dt(.25)
            frequency = 2*np.arcsin(dt*np.sqrt(engine.eigenvalues[mode])/2)/dt
            field = engine.modes[:, mode].copy()
            previous = np.cos(frequency*dt)*field
            config = {'model': model, 'mode': mode, 'coefficients': asdict(engine.coefficients),
                      'initial_condition': 'W-normalized cavity eigenmode at maximum amplitude'}
        drive = DrivenBulk(engine, field) if model == "bulk" else None
        self.model, self.engine, self.field, self.previous = model, engine, field, previous
        self.drive = drive
        self.dt, self.config = dt, config
        self.steps = 0
        self.shift = np.zeros(3, int)
        self.generation += 1
        self.initial_energy = self.energy()
        self.initial_norm = engine.norm(field) if model == 'bulk' else None
        self.trace = []
        self.record()

    def energy(self):
        if self.model == 'bulk':
            return self.engine.energy(self.field)
        return self.engine.energy(self.previous, self.field, self.dt)

    def record(self):
        row = {'time': self.steps*self.dt, 'energy': self.energy()}
        if self.model == 'bulk':
            measured = self.drive.measurements(self.field)
            row.update(total_energy=measured['total_energy'], source_work=measured['switch_work']+measured['intervention_work'],
                       balance_residual=measured['energy_balance_residual'], applied_force=measured['applied_force'],
                       centroid=measured['centroid'])
            row['norm'] = self.engine.norm(self.field)
            row['detector_intensity'] = self.engine.detector(self.field, 1.)['intensity']
        self.trace.append(row)
        self.trace = self.trace[-256:]

    def source_drift(self):
        drift = []
        for path in SOURCE_PATHS:
            try:
                changed = hashlib.sha256((ROOT/path).read_bytes()).hexdigest() != STARTUP_SOURCES[path]
            except OSError:
                changed = True
            if changed:
                drift.append(path)
        return drift

    def command(self, data):
        if self.source_drift():
            raise ValueError('Source files changed after startup; restart the lab before mutation')
        if not isinstance(data, dict) or not isinstance(data.get('action'), str):
            raise ValueError('Object with action required')
        action = data['action']
        if action == 'reset':
            self.reset({k: v for k, v in data.items() if k != 'action'})
        elif action == 'step':
            if set(data) - {'action', 'count'}:
                raise ValueError('Unknown step parameter')
            count = integer(data.get('count', 5), 1, 50, 'count')
            # Transactional stepping: reject a nonfinite proposal without losing state.
            field, prev = self.field.copy(), None if self.previous is None else self.previous.copy()
            drive = self.drive.fork() if self.drive is not None else None
            for _ in range(count):
                if self.model == 'bulk':
                    field = drive.advance(field, self.dt)
                else:
                    prev, field = field, self.engine.advance(prev, field, self.dt)
            if not np.isfinite(field).all():
                raise ValueError('Nonfinite evolution rejected')
            self.field, self.previous = field, prev
            self.drive = drive
            self.steps += count
            self.record()
        elif action == 'set_force':
            if set(data) != {'action', 'force'} or self.model != 'bulk':
                raise ValueError('Force drive requires a bulk force vector')
            drive = self.drive.fork()
            drive.set_force(self.field, data['force'])
            self.drive = drive
            self.record()
        elif action == 'displace':
            if set(data) != {'action', 'shift'} or self.model != 'bulk':
                raise ValueError('Lattice displacement is available only in bulk mode')
            raw = data['shift']
            if not isinstance(raw, list) or len(raw) != 3:
                raise ValueError('Three integer displacement components required')
            shift = [integer(v, -2, 2, 'shift') for v in raw]
            if sum(shift) % 2:
                raise ValueError('FCC displacement must preserve even parity')
            after = np.roll(self.engine.full(self.field), shift, axis=(0, 1, 2))[self.engine.mask]
            drive = self.drive.fork()
            drive.intervention(self.field, after, shift)
            self.field, self.drive = after, drive
            self.shift += shift
            self.record()
        else:
            raise ValueError('Unknown action')
        return self.snapshot()

    def response_probe(self):
        if self.model != 'cavity':
            return None
        m, mode = self.engine, self.config['mode']
        tensor = m.carried_tensor(mode, self.dt)
        h = .01
        e0 = m.cycle_energy(mode, self.dt, [0, 0, 0])
        curvature = []
        for j in range(3):
            v = np.eye(3)[j]*h
            curvature.append((m.cycle_energy(mode, self.dt, v)+m.cycle_energy(mode, self.dt, -v)-2*e0)/h**2)
        return {'tensor': tensor.tolist(), 'energy_fd_diagonal': curvature,
                'max_diagonal_error': float(np.max(abs(np.diag(tensor)-curvature))),
                'probe_speed': h, 'cycle_energy_at_rest': e0,
                'scope': 'Cycle-averaged carried cavity profile curvature; input W, not particle mass or bulk displacement dynamics'}

    def snapshot(self):
        m = self.engine
        field = self.field if self.model == 'bulk' else self.field.reshape((-1, 4)).astype(complex)
        data = {'generation': self.generation, 'model': self.model, 'step': self.steps,
                'time': self.steps*self.dt, 'dt': self.dt, 'config': self.config,
                'xyz': m.xyz.tolist(), 'real': field.real.tolist(), 'imag': field.imag.tolist(),
                'roles': list(ROLES), 'trace': list(self.trace), 'energy': self.energy(),
                'energy_change': self.energy()-self.initial_energy,
                'boundary': 'periodic FCC bulk' if self.model == 'bulk' else 'finite FCC cavity; missing exterior bonds',
                'units': 'dimensionless model units; camera pixels are display-only',
                'status': 'hypothetical constitutive model; no validated quantum/particle identification',
                'source_sha256': dict(STARTUP_SOURCES),
                'source_drift': self.source_drift(),
                'response': self.response_probe()}
        if self.model == 'bulk':
            data.update(drive=self.drive.measurements(self.field), measurements=m.measurements(self.field), detector=m.detector(self.field, 1.),
                        norm_relative_error=m.norm(self.field)/self.initial_norm-1,
                        imposed_lattice_shift=(self.shift*m.spacing/np.sqrt(2)).tolist(),
                        displacement_scope='Exact imposed lattice translation, not a derived force/acceleration law')
            data['drive']['centroid']['policy'] = {
                'minimum_concentration': .5, 'maximum_seam_fraction': .01,
                'maximum_internal_step_box_fraction': .25,
                'diagnostic': 'L times seam norm, summed initial/current; a conservative heuristic, not a rigorous arbitrary-field error bound',
                'threshold': 'displacement above ten times diagnostic; temporal refinement still required'}
        else:
            data['previous_real'] = self.previous.reshape((-1, 4)).tolist()
            data['energy_time'] = (self.steps-.5)*self.dt
            data['energy_convention'] = 'E[n-1/2]: previous/current pair; v=(current-previous)/dt, midpoint=(current+previous)/2'
        return data


def make_server(port=8765):
    lab = Lab()

    class Handler(BaseHTTPRequestHandler):
        def reply(self, status, data, kind='application/json'):
            body = json.dumps(data, allow_nan=False).encode() if kind == 'application/json' else data
            self.send_response(status)
            self.send_header('Content-Type', kind)
            self.send_header('Content-Length', str(len(body)))
            self.send_header('Cache-Control', 'no-store')
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.send_header('Content-Security-Policy', "default-src 'self'; style-src 'self' 'unsafe-inline'; script-src 'self'; connect-src 'self'; frame-ancestors 'none'")
            self.end_headers()
            self.wfile.write(body)

        def valid_host(self):
            return self.headers.get('Host') in (f'127.0.0.1:{self.server.server_port}', f'localhost:{self.server.server_port}')

        def do_GET(self):
            if not self.valid_host():
                return self.reply(403, {'error': 'Loopback host required'})
            path = urlsplit(self.path).path
            if path == '/api/state':
                return self.reply(200, lab.snapshot())
            assets = {'/': ('index.html', 'text/html; charset=utf-8'), '/app.js': ('app.js', 'text/javascript; charset=utf-8')}
            if path not in assets:
                return self.reply(404, {'error': 'Unknown resource'})
            file, kind = assets[path]
            self.reply(200, (Path(__file__).parent/file).read_bytes(), kind)

        def do_POST(self):
            if not self.valid_host():
                return self.reply(403, {'error': 'Loopback host required'})
            origin = self.headers.get('Origin')
            if origin and origin != 'http://'+self.headers.get('Host', ''):
                return self.reply(403, {'error': 'Same-origin requests required'})
            if self.path != '/api/command':
                return self.reply(404, {'error': 'Unknown resource'})
            try:
                if self.headers.get('Content-Type') != 'application/json':
                    raise ValueError('application/json required')
                length = int(self.headers.get('Content-Length', '0'))
                if not 0 < length <= 4096:
                    raise ValueError('Body must contain 1..4096 bytes')
                data = json.loads(self.rfile.read(length))
                self.reply(200, lab.command(data))
            except (ValueError, TypeError, OverflowError) as exc:
                self.reply(400, {'error': str(exc)})

        def log_message(self, *args):
            pass

    server = HTTPServer(('127.0.0.1', port), Handler)
    server.lab = lab
    return server


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=8765)
    args = parser.parse_args()
    server = make_server(args.port)
    print(f'Native 3D lab: http://127.0.0.1:{server.server_port}/', flush=True)
    server.serve_forever()
