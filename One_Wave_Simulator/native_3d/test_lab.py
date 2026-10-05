import importlib.util
import json
from pathlib import Path
import threading
import unittest
from unittest.mock import patch
from urllib.error import HTTPError
from urllib.request import Request, urlopen
import numpy as np

spec=importlib.util.spec_from_file_location('native_lab',Path(__file__).with_name('server.py'))
server=importlib.util.module_from_spec(spec);spec.loader.exec_module(server)

class LabTests(unittest.TestCase):
    def test_same_state_measurements_and_repeatable_reset(self):
        a,b=server.Lab(),server.Lab()
        np.testing.assert_array_equal(a.field,b.field)
        s=a.command({'action':'step','count':20})
        f=np.array(s['real'])+1j*np.array(s['imag'])
        np.testing.assert_array_equal(f,a.field)
        self.assertAlmostEqual(a.engine.norm(f),s['measurements']['norm'])
        self.assertAlmostEqual(a.engine.energy(f),s['energy'])
        self.assertLess(abs(s['norm_relative_error']),1e-12)
        self.assertEqual(s['time'],.4)

    def test_exact_displacement_and_reverse(self):
        a=server.Lab();before=a.field.copy();energy=a.energy();detector=a.engine.detector(a.field)['intensity']
        s=a.command({'action':'displace','shift':[1,1,0]})
        expected=np.roll(a.engine.full(before),(1,1,0),axis=(0,1,2))[a.engine.mask]
        np.testing.assert_array_equal(a.field,expected)
        self.assertAlmostEqual(a.energy(),energy,places=12)
        self.assertAlmostEqual(s['measurements']['norm'],20,places=12)
        self.assertNotAlmostEqual(s['detector']['intensity'],detector)
        a.command({'action':'displace','shift':[-1,-1,0]})
        np.testing.assert_array_equal(a.field,before)

    def test_rejected_commands_are_transactional(self):
        a=server.Lab();before=a.field.copy();config=a.config.copy();generation=a.generation
        bad=[{'action':'step','count':51},{'action':'step','count':1.5},{'action':'step','count':True},
             {'action':'displace','shift':[1,0,0]},{'action':'displace','shift':[float('nan'),0,0]},
             {'action':'reset','side':10},{'action':'reset','norm':float('inf')},
             {'action':'reset','model':'cavity','norm':20},{'action':'reset','model':'bulk','mode':4},
             {'action':'reset','model':'quantum'},{'action':'reset','path':'/tmp'},
             {'action':'camera','zoom':2},{'action':'reset','model':'cavity','mode':52}]
        for command in bad:
            with self.subTest(command=command),self.assertRaises(ValueError):a.command(command)
            np.testing.assert_array_equal(a.field,before)
            self.assertEqual(a.config,config);self.assertEqual(a.generation,generation)

    def test_model_controls_and_cavity_curvature(self):
        a=server.Lab();f=a.field.copy()
        a.command({'action':'reset','control':'linear'})
        np.testing.assert_array_equal(a.field,f)
        self.assertEqual(a.engine.c.focusing,0)
        s=a.command({'action':'reset','model':'cavity','mode':4})
        self.assertLess(s['response']['max_diagonal_error'],1e-9)
        exported=a.engine.energy(np.array(s['previous_real']).ravel(),np.array(s['real']).ravel(),s['dt'])
        self.assertAlmostEqual(exported,s['energy'],places=14)
        before=a.energy();s=a.command({'action':'step','count':50})
        self.assertAlmostEqual(s['energy'],before,places=12)
        with self.assertRaises(ValueError):a.command({'action':'displace','shift':[1,1,0]})
        zero=a.command({'action':'reset','model':'cavity','mode':0})
        self.assertLess(np.linalg.norm(zero['response']['tensor']),1e-20)

    def test_source_receipt(self):
        s=server.Lab().snapshot()
        self.assertIn('solvers/bulk_excitation.py',s['source_sha256'])
        self.assertEqual(set(s['source_sha256']),set(server.SOURCE_PATHS))
        self.assertTrue(all(len(v)==64 for v in s['source_sha256'].values()))

    def test_source_drift_preserves_startup_receipt_and_blocks_mutation(self):
        lab=server.Lab(); before=lab.field.copy(); source=server.SOURCE_PATHS[0]
        original=Path.read_bytes
        def changed(path):
            return original(path)+(b'\n# changed' if path == server.ROOT/source else b'')
        with patch.object(Path,'read_bytes',changed):
            snap=lab.snapshot()
            self.assertEqual(snap['source_sha256'],server.STARTUP_SOURCES)
            self.assertEqual(snap['source_drift'],[source])
            with self.assertRaises(ValueError):lab.command({'action':'step','count':1})
        np.testing.assert_array_equal(before,lab.field)
        with patch.object(Path,'read_bytes',side_effect=FileNotFoundError):
            self.assertEqual(lab.source_drift(),server.SOURCE_PATHS)

class HTTPTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.http=server.make_server(0);cls.port=cls.http.server_port
        cls.thread=threading.Thread(target=cls.http.serve_forever,daemon=True);cls.thread.start()
    @classmethod
    def tearDownClass(cls):cls.http.shutdown();cls.http.server_close();cls.thread.join()
    def request(self,path='/',body=None,headers=None):
        request=Request(f'http://127.0.0.1:{self.port}'+path,data=body,headers=headers or {})
        try:
            with urlopen(request) as response:return response.status,response.read(),dict(response.headers)
        except HTTPError as error:return error.code,error.read(),dict(error.headers)
    def test_loopback_assets_and_path_allowlist(self):
        self.assertEqual(self.http.server_address[0],'127.0.0.1')
        for path in ('/','/app.js','/api/state'):
            status,_,headers=self.request(path);self.assertEqual(status,200)
            self.assertNotIn('Access-Control-Allow-Origin',headers)
        for path in ('/server.py','/../../AGENTS.md','/api/exec'):
            self.assertEqual(self.request(path)[0],404)
    def test_host_origin_body_and_method_guards(self):
        self.assertEqual(self.request(headers={'Host':'evil.example'})[0],403)
        body=b'{"action":"step","count":1}'
        self.assertEqual(self.request('/api/command',body,{'Content-Type':'application/json','Origin':'https://evil.example'})[0],403)
        self.assertEqual(self.request('/api/command',body,{'Content-Type':'text/plain'})[0],400)
        self.assertEqual(self.request('/api/command',b' '*4097,{'Content-Type':'application/json'})[0],400)
        self.assertEqual(self.request('/api/command',body,{'Content-Type':'application/json'})[0],200)
        self.assertEqual(self.request('/api/command',b'[]',{'Content-Type':'application/json'})[0],400)

if __name__=='__main__':unittest.main()
