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



class SimulatedCrash(BaseException):
    pass

class CheckpointApp(App):
    """Stop at a durable boundary, without exception cleanup rewriting the record."""
    crash_at = None
    def launch(self, item, guard):
        self.active.add(item['id'])
        try:
            self.run(item, guard)
        except SimulatedCrash:
            pass
    def checkpoint(self, item, boundary):
        if boundary == self.crash_at:
            raise SimulatedCrash(boundary)

class RecoveryTests(ContractTests):
    def test_every_checkpoint_resumes_without_repeated_return(self):
        boundaries = [f'{phase}-{n}' for n in range(6) for phase in ('field','void')]
        boundaries += ['candidate-returned','audit-returned','published']
        for boundary in boundaries:
            with self.subTest(boundary=boundary):
                state = self.state.with_name(boundary+'.sqlite')
                calls=[]
                def provider(prompt,audit=False):
                    calls.append('audit' if audit else 'candidate')
                    return self.provider(prompt,audit)
                app=CheckpointApp([self.root],state,provider)
                app.crash_at=boundary
                app.ask('Field Void','stable-id')
                recovered=CheckpointApp([self.root],state,provider)
                old=recovered.get('stable-id')
                if boundary!='published':
                    self.assertTrue(old['recoverable'])
                    recovered.resume('stable-id')
                item=recovered.get('stable-id')
                self.assertEqual(item['status'],'completed',item.get('error'))
                self.assertEqual(calls,['candidate','audit'])
                self.assertEqual(len(item['events']),12)
                self.assertEqual(item['sequence'],12)
                self.assertEqual(item['publication']['candidate_hash'],item['answer_hash'])
                recovered.ask('Field Void','stable-id')
                self.assertEqual(calls,['candidate','audit'])

    def test_inflight_outcome_never_reissued(self):
        for name in ['candidate','audit']:
            with self.subTest(name=name):
                state=self.state.with_name(name+'.sqlite');calls=[]
                def provider(prompt,audit=False):
                    calls.append(audit);return self.provider(prompt,audit)
                app=CheckpointApp([self.root],state,provider);app.crash_at=name+'-inflight'
                app.ask('Field Void','inflight')
                recovered=CheckpointApp([self.root],state,provider)
                item=recovered.get('inflight')
                self.assertEqual(item['status'],'paused');self.assertFalse(item['recoverable'])
                with self.assertRaises(ValueError): recovered.resume('inflight')
                self.assertEqual(calls,[] if name=='candidate' else [False])
                self.assertIsNone(recovered.get('inflight')['answer'])

    def test_returned_candidate_is_private_and_survives_restart(self):
        app=CheckpointApp([self.root],self.state,self.provider);app.crash_at='audit-returned'
        app.ask('Field Void','private')
        recovered=CheckpointApp([self.root],self.state,self.provider)
        raw=recovered.get('private')
        self.assertIn('candidate',raw);self.assertIn('audit',raw['operations'])
        for view in [recovered.public(raw),recovered.history()[0]]:
            self.assertNotIn('candidate',view);self.assertNotIn('operations',view)
            self.assertIsNone(view['answer'])
        recovered.resume('private')
        self.assertEqual(recovered.get('private')['status'],'completed')

    def test_dirty_to_dirty_and_committed_drift_block_resume(self):
        for committed in [False,True]:
            with self.subTest(committed=committed):
                state=self.state.with_name(str(committed)+'.sqlite')
                source=self.root/'reference.md';source.write_text(source.read_text()+'\nfirst dirty\n')
                app=CheckpointApp([self.root],state,self.provider);app.crash_at='candidate-returned'
                app.ask('Field Void','drift')
                source.write_text(source.read_text()+'\nsecond dirty\n')
                if committed:
                    self.run_git('add','.');self.run_git('commit','-qm','changed')
                recovered=CheckpointApp([self.root],state,lambda *a:self.fail('stale dispatch'))
                with self.assertRaisesRegex(ValueError,'reference changed'): recovered.resume('drift')
                self.assertIsNone(recovered.get('drift')['answer'])

    def test_tampered_candidate_and_return_hold(self):
        for target in ['candidate','response','audit_binding','sources']:
            with self.subTest(target=target):
                state=self.state.with_name(target+'.sqlite')
                app=CheckpointApp([self.root],state,self.provider);app.crash_at='void-5'
                app.ask('Field Void','tamper')
                item=app.get('tamper')
                if target=='candidate': item['candidate']['answer']='Altered [S1]'
                elif target=='response': item['operations']['candidate']['response']['answer']='Altered [S1]'
                elif target=='audit_binding': item['audit_binding']['candidate_hash']='wrong'
                else: item['sources'][0]['excerpt']='altered'
                app.save(item)
                recovered=CheckpointApp([self.root],state,lambda *a:self.fail('duplicate call'))
                try: recovered.resume('tamper')
                except ValueError: pass
                self.assertEqual(recovered.get('tamper')['status'],'paused')
                self.assertIsNone(recovered.get('tamper')['answer'])

    def test_second_instance_does_not_pause_live_worker(self):
        import threading
        entered=threading.Event();release=threading.Event();calls=[]
        def provider(prompt,audit=False):
            calls.append(audit)
            if not audit:
                entered.set();self.assertTrue(release.wait(10))
            return self.provider(prompt,audit)
        app=App([self.root],self.state,provider);app.ask('Field Void','live')
        self.assertTrue(entered.wait(10))
        try:
            other=App([self.root],self.state,lambda *a:self.fail('second worker dispatched'))
            self.assertEqual(other.get('live')['status'],'running')
            self.assertEqual(other.ask('Field Void','live')['status'],'running')
            with self.assertRaises(ValueError):other.ask('another question','other')
        finally: release.set()
        item=self.wait(app,app.get('live'));self.assertEqual(item['status'],'completed')
        self.assertEqual(calls,[False,True])

    def test_stale_writer_cannot_overwrite_newer_checkpoint(self):
        app=App([self.root],self.state,self.provider)
        app.save({'id':'cas','status':'paused','phase':'FIELD','cursor':0})
        old=app.get('cas');new=app.get('cas');new['marker']='new';app.save(new)
        with self.assertRaisesRegex(ValueError,'Concurrent'):app.save(old)
        self.assertEqual(app.get('cas')['marker'],'new')

    def test_additive_migration_keeps_old_completed_history(self):
        import sqlite3
        with sqlite3.connect(self.state) as db:
            db.execute('CREATE TABLE conversations(id TEXT PRIMARY KEY,payload TEXT NOT NULL)')
            db.execute('INSERT INTO conversations VALUES (?,?)',('old',json.dumps({'id':'old','status':'completed','answer':{'answer':'historical'},'reference':['old-version']})))
        app=App([self.root],self.state,lambda *a:self.fail('old result redispatched'))
        self.assertEqual(app.ask('old question','old')['reference'],['old-version'])
        self.assertEqual(app.history()[0]['answer']['answer'],'historical')

    def test_drift_during_publication_rolls_back_answer(self):
        root=self.root
        class ChangeAtCommit(CheckpointApp):
            def write(self,db,item,note=None):
                result=super().write(db,item,note)
                if item['status']=='completed':
                    (root/'reference.md').write_text('changed while publishing')
                return result
        app=ChangeAtCommit([self.root],self.state,self.provider)
        app.ask('Field Void','race')
        result=app.get('race')
        self.assertEqual(result['status'],'paused')
        self.assertIsNone(result['answer'])
        self.assertEqual(result['cursor'],5)
        self.assertEqual(result['phase'],'FIELD')
        for key in ['publication','answer_hash','finished']:
            self.assertNotIn(key,result)
        with app.db() as db:
            notes=[json.loads(r[0]) for r in db.execute('SELECT payload FROM journal')]
        self.assertFalse(any('consequence_hash' in note for note in notes))

    def test_concurrent_publication_cannot_overwrite_newer_state(self):
        class ConcurrentChange(CheckpointApp):
            def publish(self,item,candidate,binding):
                newer=self.get(item['id']);newer.update(status='paused',decision='HOLD',marker='newer-owner')
                self.save(newer)
                return super().publish(item,candidate,binding)
        app=ConcurrentChange([self.root],self.state,self.provider)
        app.ask('Field Void','race')
        result=app.get('race');self.assertEqual(result['marker'],'newer-owner')
        self.assertEqual(result['status'],'paused');self.assertIsNone(result['answer'])

    def test_checkpoint_drift_prevents_next_provider_call(self):
        root=self.root;calls=[]
        class DriftAfterField(CheckpointApp):
            def checkpoint(self,item,boundary):
                if boundary=='void-2':(root/'reference.md').write_text('new tracked working text')
        def provider(*args):calls.append(args);self.fail('stale provider call')
        app=DriftAfterField([self.root],self.state,provider)
        app.ask('Field Void','drift')
        self.assertEqual(app.get('drift')['status'],'paused');self.assertEqual(calls,[])

    def test_process_lock_released_after_actual_process_crash(self):
        import multiprocessing
        import os
        class ExitAfterReturn(CheckpointApp):
            def checkpoint(self,item,boundary):
                if boundary=='audit-returned':os._exit(23)
        def child():
            app=ExitAfterReturn([self.root],self.state,self.provider)
            app.ask('Field Void','crashed')
        process=multiprocessing.get_context('fork').Process(target=child)
        process.start();process.join(10)
        if process.is_alive():
            process.terminate();process.join();self.fail('crash child hung')
        self.assertEqual(process.exitcode,23)
        recovered=CheckpointApp([self.root],self.state,lambda *a:self.fail('duplicate provider dispatch'))
        recovered.resume('crashed')
        item=recovered.get('crashed')
        self.assertEqual(item['status'],'completed',item.get('error'))
        self.assertEqual(len(item['events']),12)

    def test_untrusted_audit_and_error_fields_stay_private(self):
        sentinel='UNTRUSTED_PRIVATE_RAW'
        def provider(prompt,audit=False):
            if audit:return {'decision':'CORRECT','summary':sentinel,'raw_internal':sentinel,
                             'candidate':{'answer':sentinel}}
            return self.provider(prompt,audit)
        for boundary in ['field-4',None]:
            with self.subTest(boundary=boundary):
                state=self.state.with_name(str(boundary)+'.sqlite')
                app=CheckpointApp([self.root],state,provider);app.crash_at=boundary
                app.ask('Field Void','private-audit')
                raw=app.get('private-audit')
                self.assertIn(sentinel,json.dumps(raw))
                self.assertNotIn(sentinel,json.dumps(app.public(raw)))
                self.assertNotIn(sentinel,json.dumps(app.history()))
                self.assertIsNone(app.public(raw)['answer'])

    def test_malformed_audit_decisions_never_break_public_history(self):
        for number,decision in enumerate([['ALLOW'],{'decision':'ALLOW'},None]):
            with self.subTest(decision=decision):
                state=self.state.with_name(f'malformed-{number}.sqlite')
                def provider(prompt,audit=False):
                    return {'decision':decision,'summary':'malformed'} if audit else self.provider(prompt,audit)
                app=CheckpointApp([self.root],state,provider)
                app.ask('Field Void','malformed')
                raw=app.get('malformed')
                self.assertEqual(raw['status'],'paused')
                self.assertEqual(app.public(raw)['audit']['decision'],'HOLD')
                self.assertIsNone(app.history()[0]['answer'])
                raw['decision']=decision;raw['events'][0]['decision']=decision
                self.assertIsNone(app.public(raw)['decision'])

    def test_extra_answer_fields_are_retained_privately_and_hold(self):
        def provider(prompt,audit=False):
            value=self.provider(prompt,audit)
            if not audit:value['unrequested_private_field']='PRIVATE_EXTRA'
            return value
        app=CheckpointApp([self.root],self.state,provider)
        app.ask('Field Void','extra')
        raw=app.get('extra')
        self.assertEqual(raw['status'],'paused')
        self.assertIsNone(raw['answer'])
        self.assertNotIn('audit',raw['operations'])
        self.assertIn('PRIVATE_EXTRA',json.dumps(raw))
        self.assertNotIn('PRIVATE_EXTRA',json.dumps(app.public(raw)))
        self.assertNotIn('PRIVATE_EXTRA',json.dumps(app.history()))

    def test_malformed_candidate_shapes_hold_before_audit(self):
        for number,bad in enumerate([{'answer':['bad']},{'source_ids':{'S1':True}},
                                      {'assumptions':[{'hidden':'private'}]},{'unresolved':None}]):
            with self.subTest(bad=bad):
                calls=[]
                def provider(prompt,audit=False):
                    calls.append(audit);value=self.provider(prompt,audit);value.update(bad);return value
                app=CheckpointApp([self.root],self.state.with_name(f'candidate-shape-{number}.sqlite'),provider)
                app.ask('Field Void','shape')
                self.assertEqual(app.get('shape')['status'],'paused')
                self.assertEqual(calls,[False])
                self.assertIsNone(app.public(app.get('shape'))['answer'])

if __name__=='__main__':unittest.main()
