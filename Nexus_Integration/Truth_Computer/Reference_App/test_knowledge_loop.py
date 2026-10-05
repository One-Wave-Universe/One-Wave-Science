import json
import multiprocessing
import os
from pathlib import Path
import sqlite3
import subprocess
import tempfile
import unittest
from app import App
from knowledge_loop import AUTHORITIES, Busy, KnowledgeLoop, SCIENCE, digest


class Crash(BaseException):pass

class BuilderTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.base=Path(self.temp.name)
        self.root=self.base/'source';self.root.mkdir()
        self.git('init','-q');self.git('config','user.name','Fixture');self.git('config','user.email','fixture@example.invalid')
        self.git('remote','add','origin','https://github.com/'+SCIENCE+'.git')
        for path in AUTHORITIES:
            target=self.root/path;target.parent.mkdir(parents=True,exist_ok=True);target.write_text('Fixture authority: '+path+'\n')
        self.source=self.root/'source.md'
        self.source.write_text('---\nnode_id: "X-1"\ngate: "YELLOW"\nlifecycle: "ACTIVE_HYPOTHESIS"\n---\nA source statement, not a measurement.\n')
        self.git('add','.');self.git('commit','-qm','fixture')
        self.runtime=self.base/'claude.sqlite';self.store=self.base/'reality.sqlite'
        self.app=App([self.root],self.runtime,provider=lambda *a:self.fail('No model invocation permitted'))
        self.request=dict(goal='Retain the quoted source statement',repo=SCIENCE,path='source.md',start_line=6,end_line=6)
    def tearDown(self):self.temp.cleanup()
    def git(self,*args):return subprocess.check_output(['git','-C',str(self.root),*args],text=True).strip()
    def loop(self,**kwargs):return KnowledgeLoop(self.app,self.store,'shared-reality-fixture',**kwargs)
    def counts(self,loop):
        with loop.db() as db:return {name:db.execute('SELECT count(*) FROM '+name).fetchone()[0] for name in ('record_versions','source_versions','consequences','artifacts','audits','transitions')}

    def test_first_record_then_restart_and_memory_consequence(self):
        loop=self.loop();result=loop.run('first',self.request)
        self.assertEqual(result['status'],'completed');self.assertEqual(result['phase'],'FIELD');self.assertEqual(result['cursor'],0)
        self.assertEqual(result['sequence'],12)
        record=loop.record(result['receipt']['record_version'])
        self.assertEqual(record['quote'],'A source statement, not a measurement.\n')
        self.assertEqual(record['source']['metadata']['gate'],'YELLOW')
        self.assertEqual(record['source']['metadata']['lifecycle'],'ACTIVE_HYPOTHESIS')
        self.assertEqual(record['proposition_status'],'NOT_VALIDATED')
        restarted=self.loop();second=restarted.run('second',self.request)
        self.assertEqual(second['receipt']['prior_record_id'],result['receipt']['record_version'])
        self.assertTrue(second['receipt']['reused'])
        self.assertEqual(self.counts(loop)['record_versions'],1)
        self.assertEqual(self.counts(loop)['consequences'],2)
        self.assertEqual(restarted.run('second',self.request),second)

    def test_corrupt_proposal_is_challenged_then_corrected(self):
        def propose(record,attempt):
            if attempt==0:record['quote']='Invented result.'
            return record
        loop=self.loop(proposer=propose);result=loop.run('repair',self.request)
        self.assertEqual(result['status'],'completed');self.assertEqual(result['attempts'],1)
        trace=loop.trace('repair');decisions=[a['decision'] for a in trace['audits']]
        self.assertIn('CORRECT',decisions)
        correction=next(a for a in trace['audits'] if a['decision']=='CORRECT')
        self.assertEqual(correction['counterproposal']['quote'],'A source statement, not a measurement.\n')
        self.assertEqual(self.counts(loop)['record_versions'],1)
        with loop.db() as db:
            proposals=[json.loads(r[0]) for r in db.execute('SELECT payload FROM artifacts WHERE cursor=1')]
        self.assertEqual(proposals[0]['data']['record']['quote'],'Invented result.')
        self.assertNotEqual(digest(proposals[0]),digest(proposals[1]))

    def test_three_failed_attempts_escalate_without_record(self):
        def bad(record,attempt):record['quote']='bad';return record
        loop=self.loop(proposer=bad);result=loop.run('bad',self.request)
        self.assertEqual(result['status'],'paused');self.assertEqual(result['decision'],'ESCALATE')
        self.assertEqual(result['cursor'],1);self.assertEqual(result['phase'],'VOID')
        self.assertEqual(self.counts(loop)['record_versions'],0)
        before=self.counts(loop);self.assertEqual(loop.run('bad'),result);self.assertEqual(before,self.counts(loop))

    def test_restart_at_every_phase_boundary(self):
        for boundary in range(12):
            with self.subTest(boundary=boundary):
                loop=self.loop();identity='restart-'+str(boundary);loop.begin(identity,self.request)
                for _ in range(boundary):loop.advance(identity)
                before=loop.get(identity);expected_phase='FIELD' if boundary%2==0 else 'VOID'
                self.assertEqual(before['phase'],expected_phase);self.assertEqual(before['cursor'],boundary//2)
                restarted=self.loop();result=restarted.run(identity)
                self.assertEqual(result['status'],'completed');self.assertEqual(result['sequence'],12)
                self.assertEqual(len(restarted.trace(identity)['transitions']),12)
        self.assertEqual(self.counts(loop)['record_versions'],1)

    def test_final_transaction_crash_before_and_after_commit(self):
        for point in ('before-commit','after-commit'):
            with self.subTest(point=point):
                loop=self.loop();identity='commit-'+point;loop.begin(identity,self.request)
                for _ in range(11):loop.advance(identity)
                def crash(boundary):
                    if boundary==point:raise Crash()
                loop.checkpoint=crash
                with self.assertRaises(Crash):loop.advance(identity)
                recovered=self.loop();result=recovered.run(identity)
                self.assertEqual(result['status'],'completed');self.assertEqual(result['sequence'],12)
                with recovered.db() as db:self.assertEqual(db.execute('SELECT count(*) FROM consequences WHERE job=?',(identity,)).fetchone()[0],1)

    def test_real_process_exit_and_lost_handoff_reconcile(self):
        loop=self.loop();loop.begin('process',self.request)
        for _ in range(11):loop.advance('process')
        def child():
            app=App([self.root],self.runtime,provider=lambda *a:None)
            worker=KnowledgeLoop(app,self.store,'shared-reality-fixture')
            def crash(boundary):
                if boundary=='after-commit':os._exit(27)
            worker.checkpoint=crash;worker.advance('process')
        proc=multiprocessing.get_context('fork').Process(target=child);proc.start();proc.join(10)
        if proc.is_alive():proc.terminate();proc.join();self.fail('child hung')
        self.assertEqual(proc.exitcode,27)
        restarted=self.loop();before=self.counts(restarted);result=restarted.run('process',self.request)
        self.assertEqual(result['status'],'completed');self.assertEqual(before,self.counts(restarted))
        with self.app.db() as db:self.assertEqual(db.execute('SELECT count(*) FROM conversations').fetchone()[0],0)

    def test_idempotency_key_cannot_change_goal_or_span(self):
        loop=self.loop();loop.begin('same',self.request)
        for changed in [dict(self.request,goal='different'),dict(self.request,start_line=5)]:
            with self.assertRaisesRegex(ValueError,'Idempotency'):loop.begin('same',changed)

    def test_missing_source_and_unchanged_dependency_hold(self):
        loop=self.loop();result=loop.run('missing',dict(self.request,path='absent.md'))
        self.assertEqual(result['decision'],'HOLD');self.assertEqual(result['cursor'],0);self.assertEqual(result['phase'],'FIELD')
        before=self.counts(loop);self.assertEqual(loop.advance('missing'),result);self.assertEqual(before,self.counts(loop))
        self.assertEqual(before['record_versions'],0)

    def test_changed_reference_before_void_holds_without_advance(self):
        loop=self.loop();loop.begin('drift',self.request);loop.advance('drift')
        self.source.write_text(self.source.read_text()+'changed worktree\n')
        result=loop.advance('drift')
        self.assertEqual(result['decision'],'HOLD');self.assertEqual(result['phase'],'VOID');self.assertEqual(result['cursor'],0)
        self.assertEqual(self.counts(loop)['record_versions'],0)

    def test_new_commit_appends_version_preserving_old(self):
        loop=self.loop();first=loop.run('old',self.request)
        self.source.write_text(self.source.read_text().replace('A source statement','A changed statement'))
        self.git('add','.');self.git('commit','-qm','new source')
        second=loop.run('new',self.request)
        self.assertEqual(second['status'],'completed')
        self.assertNotEqual(first['receipt']['record_version'],second['receipt']['record_version'])
        self.assertEqual(loop.record(first['receipt']['record_version'])['quote'],'A source statement, not a measurement.\n')
        with loop.db() as db:
            prior=db.execute('SELECT previous_id FROM record_versions WHERE id=?',(second['receipt']['record_version'],)).fetchone()[0]
        self.assertEqual(prior,first['receipt']['record_version']);self.assertEqual(self.counts(loop)['record_versions'],2)

    def test_archive_rejects_update_and_delete(self):
        loop=self.loop();loop.run('immutable',self.request)
        for table in ('artifacts','audits','transitions','source_versions','record_versions','consequences','identity'):
            with self.subTest(table=table),loop.db() as db:
                with self.assertRaisesRegex(sqlite3.IntegrityError,'append-only'):db.execute('DELETE FROM '+table)

    def test_invalid_phase_and_cursor_are_schema_rejected(self):
        loop=self.loop();loop.begin('state',self.request)
        with loop.db() as db:
            with self.assertRaises(sqlite3.IntegrityError):db.execute("UPDATE jobs SET phase='M4' WHERE id='state'")
            with self.assertRaises(sqlite3.IntegrityError):db.execute("UPDATE jobs SET cursor=6 WHERE id='state'")

    def test_store_identity_mismatch_is_rejected(self):
        self.loop()
        with self.assertRaisesRegex(ValueError,'identity|bound'):KnowledgeLoop(self.app,self.store,'different')
        with self.assertRaisesRegex(ValueError,'distinct'):KnowledgeLoop(self.app,self.runtime,'shared-reality-fixture')

    def test_concurrent_worker_lock_and_duplicate_jobs(self):
        first=self.loop();second=self.loop();first.begin('duplicate',self.request)
        with first.guard():
            with self.assertRaises(Busy):second.advance('duplicate')
        first.run('duplicate');second.run('duplicate',self.request)
        second.run('other',dict(self.request,goal='Another cue for same source'))
        self.assertEqual(self.counts(first)['record_versions'],1);self.assertEqual(self.counts(first)['consequences'],2)

    def test_no_knowledge_record_before_final_void(self):
        loop=self.loop();loop.begin('bounded',self.request)
        for _ in range(11):
            loop.advance('bounded');self.assertEqual(self.counts(loop)['record_versions'],0)
        result=loop.advance('bounded');self.assertEqual(result['status'],'completed')
        self.assertEqual(self.counts(loop)['record_versions'],1)

    def test_private_and_out_of_scope_paths_denied(self):
        loop=self.loop()
        for request in [dict(self.request,repo='One-Wave-Universe/Bench'),dict(self.request,path='../secrets.md'),dict(self.request,path='External_Work/private.md')]:
            with self.assertRaises(ValueError):loop.begin('private',request)


    def test_unrelated_database_is_untouched(self):
        with sqlite3.connect(self.store) as db:
            db.execute('CREATE TABLE unrelated(data TEXT)');db.execute("INSERT INTO unrelated VALUES ('preserve')")
        before=self.store.read_bytes()
        with self.assertRaisesRegex(ValueError,'unrelated'):self.loop()
        self.assertEqual(before,self.store.read_bytes())
        with sqlite3.connect(self.store) as db:self.assertEqual(db.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall(),[('unrelated',)])

    def test_app_rebinding_does_not_create_second_store(self):
        self.loop();other=self.base/'second.sqlite'
        with self.assertRaisesRegex(ValueError,'bound'):KnowledgeLoop(self.app,other,'second')
        self.assertFalse(other.exists())

    def test_read_before_build_never_creates_store_or_binding(self):
        with self.assertRaises(ValueError):KnowledgeLoop(self.app,self.store,'shared-reality-fixture',create=False)
        self.assertFalse(self.store.exists());self.assertFalse(Path(str(self.store)+'.worker.lock').exists())
        with self.app.db() as db:self.assertEqual(db.execute("SELECT name FROM sqlite_master WHERE name='knowledge_binding'").fetchall(),[])

    def test_crlf_excerpt_has_exact_source_bytes(self):
        self.source.write_bytes(b'first\r\nsecond\r\n');self.git('add','.');self.git('commit','-qm','CRLF')
        loop=self.loop();result=loop.run('crlf',dict(self.request,start_line=1,end_line=2))
        self.assertEqual(loop.record(result['receipt']['record_version'])['quote'].encode(),b'first\r\nsecond\r\n')

    def test_final_freshness_rollback_keeps_phase_and_no_record(self):
        loop=self.loop();loop.begin('race',self.request)
        for _ in range(11):loop.advance('race')
        def change(boundary):
            if boundary=='before-commit':self.source.write_text('changed during publication')
        loop.checkpoint=change;result=loop.advance('race')
        self.assertEqual(result['decision'],'HOLD');self.assertEqual(result['phase'],'VOID');self.assertEqual(result['cursor'],5)
        self.assertIsNone(result['receipt']);self.assertEqual(self.counts(loop)['record_versions'],0)
        self.assertEqual(self.counts(loop)['audits'],5)

    def test_prior_audit_permission_cannot_be_fabricated(self):
        loop=self.loop();loop.begin('permission',self.request)
        for _ in range(4):loop.advance('permission')
        job=loop.get('permission');job['authorized_audit']='missing'
        with loop.db() as db:loop.write_job(db,job)
        before=self.counts(loop)
        with self.assertRaisesRegex(ValueError,'authorization'):loop.advance('permission')
        self.assertEqual(before,self.counts(loop));self.assertEqual(before['record_versions'],0)

    def test_corrupt_archive_cannot_be_read_as_provenance(self):
        loop=self.loop();result=loop.run('corrupt',self.request);record_id=result['receipt']['record_version']
        with loop.db() as db:
            db.execute('DROP TRIGGER immutable_source_versions_UPDATE')
            db.execute("UPDATE source_versions SET payload='{}',hash=?",(digest({}),))
        with self.assertRaisesRegex(ValueError,'provenance'):loop.record(record_id)

    def test_transition_corruption_blocks_continuation(self):
        loop=self.loop();loop.begin('chain',self.request);loop.advance('chain')
        with loop.db() as db:
            db.execute('DROP TRIGGER immutable_transitions_UPDATE')
            db.execute("UPDATE transitions SET hash='wrong'")
        with self.assertRaisesRegex(ValueError,'integrity'):loop.run('chain')

    def test_separate_app_journals_share_one_store(self):
        first=self.loop();one=first.run('app-one',self.request)
        other=App([self.root],self.base/'deepseek.sqlite',provider=lambda *a:self.fail('No model'),agent='deepseek')
        second=KnowledgeLoop(other,self.store,'shared-reality-fixture')
        two=second.run('app-two',self.request)
        self.assertEqual(one['receipt']['store_id'],two['receipt']['store_id']);self.assertTrue(two['receipt']['reused'])
        self.assertEqual(self.counts(first)['record_versions'],1)
        with other.db() as db:self.assertEqual(db.execute('SELECT count(*) FROM journal').fetchone()[0],0)

    def test_backend_http_build_and_safe_readback(self):
        import http.client
        import socket
        import time
        from app import serve
        with socket.socket() as sock:sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
        def server():
            app=App([self.root],self.runtime,provider=lambda *a:None,
                    knowledge_store=self.store,knowledge_store_id='shared-reality-fixture')
            serve(app,port)
        process=multiprocessing.get_context('fork').Process(target=server);process.start()
        def request(method,path,data=None,origin=True):
            connection=http.client.HTTPConnection('127.0.0.1',port,timeout=15)
            headers={'Content-Type':'application/json'}
            if origin:headers['Origin']=f'http://127.0.0.1:{port}'
            connection.request(method,path,None if data is None else json.dumps(data),headers)
            response=connection.getresponse();result=(response.status,json.loads(response.read()));connection.close();return result
        try:
            deadline=time.monotonic()+5
            while True:
                try:request('GET','/api/health');break
                except ConnectionRefusedError:
                    if time.monotonic()>deadline:self.fail('server did not start')
                    time.sleep(.02)
            status,_=request('GET','/api/knowledge/job/absent');self.assertEqual(status,404);self.assertFalse(self.store.exists())
            status,_=request('POST','/api/knowledge/build',{'id':'http','request':self.request},origin=False)
            self.assertEqual(status,403);self.assertFalse(self.store.exists())
            status,result=request('POST','/api/knowledge/build',{'id':'http','request':self.request})
            self.assertEqual(status,200);self.assertEqual(result['status'],'completed')
            self.assertNotIn('proposal',result);self.assertNotIn('world',result)
            status,record=request('GET','/api/knowledge/record/'+result['receipt']['record_version'])
            self.assertEqual(status,200);self.assertEqual(record['proposition_status'],'NOT_VALIDATED')
            status,trace=request('GET','/api/knowledge/job/http');self.assertEqual(status,200);self.assertEqual(len(trace['transitions']),12)
        finally:process.terminate();process.join(5)


    def test_cursor_jump_cannot_skip_begin_void_audit(self):
        for completed_field in (False,True):
            with self.subTest(completed_field=completed_field):
                loop=self.loop();identity='jump-'+str(completed_field);loop.begin(identity,self.request)
                if completed_field:loop.advance(identity)
                job=loop.get(identity);job.update(phase='FIELD',cursor=1)
                with loop.db() as db:loop.write_job(db,job)
                with self.assertRaisesRegex(ValueError,'transition boundary'):loop.run(identity)
                self.assertEqual(self.counts(loop)['record_versions'],0)

    def test_missing_begin_authorization_is_rejected(self):
        loop=self.loop();loop.begin('begin-proof',self.request);loop.advance('begin-proof');loop.advance('begin-proof')
        job=loop.get('begin-proof');job['reference_audit']='missing'
        with loop.db() as db:loop.write_job(db,job)
        with self.assertRaisesRegex(ValueError,'authorization'):loop.advance('begin-proof')
        self.assertEqual(self.counts(loop)['record_versions'],0)

    def test_trace_uses_one_snapshot_during_concurrent_advance(self):
        import threading
        loop=self.loop();loop.begin('snapshot',self.request);loop.advance('snapshot')
        writer=self.loop();arrived=threading.Event();errors=[]
        def checkpoint(boundary):
            if boundary=='before-commit':arrived.set()
        writer.checkpoint=checkpoint
        def write():
            try:writer.advance('snapshot')
            except BaseException as error:errors.append(error)
        worker=threading.Thread(target=write)
        original=loop.load
        def load(db,identity):
            result=original(db,identity);worker.start()
            self.assertTrue(arrived.wait(5));return result
        loop.load=load
        trace=loop.trace('snapshot');worker.join(5)
        self.assertFalse(worker.is_alive());self.assertEqual(errors,[])
        self.assertEqual(trace['job']['sequence'],1);self.assertEqual(len(trace['transitions']),1)
        self.assertEqual(trace['audits'],[])
        self.assertEqual(writer.get('snapshot')['sequence'],2)

if __name__=='__main__':unittest.main()
