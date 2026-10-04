import json
from pathlib import Path
import subprocess
import tempfile
import time
import unittest
from app import App

class ContractTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.root=Path(self.temp.name)/'source'; self.root.mkdir()
        self.run_git('init','-q');self.run_git('config','user.name','Test');self.run_git('config','user.email','test@example.invalid')
        self.run_git('remote','add','origin','https://github.com/One-Wave-Universe/One-Wave-Science.git')
        (self.root/'reference.md').write_text('---\nevidence_class: candidate\nnode_id: OG-13\n---\nField and Void form the two phases. This is a repository statement.\n')
        self.run_git('add','.');self.run_git('commit','-qm','fixture')
        self.state=Path(self.temp.name)/'state.sqlite'
    def tearDown(self): self.temp.cleanup()
    def run_git(self,*args): return subprocess.check_output(['git','-C',str(self.root),*args],text=True)
    def provider(self,prompt,audit=False):
        return {'decision':'ALLOW','summary':'Supported repository statement, not physics proof.'} if audit else {'answer':'The repo describes Field and Void as two phases [S1].','source_ids':['S1'],'assumptions':[],'unresolved':[]}
    def wait(self,app,item):
        deadline=time.monotonic()+10
        while time.monotonic()<deadline:
            item=app.get(item['id'])
            if item['status']!='running': return item
            time.sleep(.02)
        self.fail('worker did not return')
    def test_loop_and_restart_consequence(self):
        app=App([self.root],self.state,self.provider)
        item=self.wait(app,app.ask('Field Void','stable-id'))
        self.assertEqual(item['status'],'completed');self.assertEqual(item['phase'],'FIELD');self.assertEqual(item['cursor'],0)
        self.assertEqual(len(item['events']),12)
        self.assertEqual([e['phase'] for e in item['events']],['FIELD','VOID']*6)
        self.assertEqual(item['sources'][0]['declared_metadata'].strip(),'evidence_class: candidate\nnode_id: OG-13')
        reloaded=App([self.root],self.state,lambda *a: self.fail('duplicate provider dispatch'))
        self.assertEqual(reloaded.ask('Field Void','stable-id')['answer_hash'],item['answer_hash'])
    def test_unknown_citation_blocks_release(self):
        def provider(prompt,audit=False):
            result=self.provider(prompt,audit)
            if not audit: result.update(answer='Unverified [S99]',source_ids=['S99'])
            return result
        app=App([self.root],self.state,provider)
        item=self.wait(app,app.ask('Field Void'))
        self.assertEqual(item['status'],'paused');self.assertIsNone(item['answer'])
    def test_reference_drift_blocks_release(self):
        def provider(prompt,audit=False):
            if audit:
                (self.root/'new.md').write_text('Changed ground')
                self.run_git('add','.');self.run_git('commit','-qm','drift')
            return self.provider(prompt,audit)
        app=App([self.root],self.state,provider)
        item=self.wait(app,app.ask('Field Void'))
        self.assertEqual(item['decision'],'HOLD');self.assertIsNone(item['answer'])
    def test_journal_isolation_and_scope(self):
        a=App([self.root],self.state,self.provider)
        a.correction('Use labeled interpretations.')
        b=App([self.root],Path(self.temp.name)/'deepseek.sqlite',self.provider,agent='deepseek')
        with b.db() as db:self.assertEqual(db.execute('SELECT count(*) FROM corrections').fetchone()[0],0)
        with self.assertRaises(ValueError):a.pipeline('source_read',{'path':'../../etc/passwd'})
        with self.assertRaises(ValueError):a.pipeline('terminal_run',{'command':'anything'})
    def test_restart_pauses_interrupted_provider(self):
        app=App([self.root],self.state,self.provider)
        app.save({'id':'interrupted','status':'running','phase':'VOID','cursor':3})
        reloaded=App([self.root],self.state,self.provider)
        self.assertEqual(reloaded.get('interrupted')['status'],'paused')
        self.assertEqual(reloaded.get('interrupted')['phase'],'VOID')

if __name__=='__main__':unittest.main()
