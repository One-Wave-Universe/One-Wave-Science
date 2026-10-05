"""CPU source-qualification projection of the M4/Field/Void contract.

Builds the FIRST explicitly selected shared knowledge store. A qualified record
proves fidelity to a pinned source, not the truth of the source's proposition.
No model calls, physical AZ0 simulation, hardware actions or source promotion.
"""
from contextlib import contextmanager
import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import sqlite3
import subprocess
import time

SCIENCE = 'One-Wave-Universe/One-Wave-Science'
STEPS = ('BEGIN', 'BUILD', 'HOLD', 'BUILD', 'BREAK', 'LOOP')
AUTHORITIES = (
    'GENERAL_REFERENCE_RULES.md', 'AI_CANONICAL_START_HERE.md',
    'UPDATED_44_STATE_AXIS_AUTHORITY_AND_EVOLUTION_RULE.md',
    'One_Wave_Bench/engine/M4_ACTIVE_WORLD_AND_MEMORY_ROUTER.md',
    'Nexus_Integration/Truth_Computer/REALITY_DATABASE_BUILDER_SPEC.md',
)
# Decisions are not worker phases. Cursor is separate from both.
TRANSITIONS = {
    'FIELD': {'PROPOSE': 'VOID', 'HOLD': 'FIELD'},
    'VOID': {'ALLOW': 'FIELD', 'CORRECT': 'FIELD', 'HOLD': 'VOID', 'ESCALATE': 'VOID'},
}
SCHEMA_VERSION = '1'
MAX_ATTEMPTS = 3


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False)


def digest(value):
    return hashlib.sha256(encoded(value).encode('utf-8')).hexdigest()


def text_hash(value):
    return hashlib.sha256(value.encode('utf-8')).hexdigest()


class Busy(ValueError):
    pass


class ReferenceDrift(ValueError):
    pass


class KnowledgeLoop:
    def __init__(self, app, store, store_id, proposer=None, create=True):
        if not store or not isinstance(store_id, str) or not re.fullmatch(r'[A-Za-z0-9_.:-]{1,100}', store_id):
            raise ValueError('Explicit shared store path and stable store ID required')
        self.app = app
        self.path = Path(store).expanduser().resolve()
        if self.path == app.state:
            raise ValueError('Knowledge store must be distinct from the per-app runtime journal')
        self.store_id = store_id
        self.proposer = proposer  # Test-only deterministic perturbation; never an AI claim.
        self.read_only = not create
        if not create:
            if not self.path.is_file():raise ValueError('Knowledge store has not been built')
            with self.db() as db:
                try:identity=dict(db.execute('SELECT key,value FROM identity'))
                except sqlite3.Error:raise ValueError('Unrecognized knowledge store') from None
                if identity != {'store_id':store_id,'schema_version':SCHEMA_VERSION,'path':str(self.path)}:
                    raise ValueError('Store identity, location or schema mismatch')
            return
        with open(str(app.state)+'.knowledge-config.lock','a') as config_lock:
            os.chmod(config_lock.name,0o600)
            fcntl.flock(config_lock,fcntl.LOCK_EX)
            with app.db() as db:
                db.execute('CREATE TABLE IF NOT EXISTS knowledge_binding(singleton INTEGER PRIMARY KEY CHECK(singleton=1), store_id TEXT, path TEXT)')
                binding = db.execute('SELECT store_id,path FROM knowledge_binding WHERE singleton=1').fetchone()
                if binding and binding != (store_id,str(self.path)):
                    raise ValueError('App already bound to another knowledge store; explicit migration required')
            self.initialize()

    def initialize(self):
        self.path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        with self.guard(), self.db() as db:
            tables = {r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")}
            expected = {'store_id': self.store_id, 'schema_version': SCHEMA_VERSION, 'path': str(self.path)}
            if tables and 'identity' not in tables:
                raise ValueError('Refusing an unrelated existing database')
            if tables and dict(db.execute('SELECT key,value FROM identity')) != expected:
                raise ValueError('Store identity, location or schema mismatch; explicit migration required')
            db.executescript('''
                CREATE TABLE IF NOT EXISTS identity(key TEXT PRIMARY KEY, value TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS jobs(
                  id TEXT PRIMARY KEY, request_hash TEXT NOT NULL,
                  phase TEXT NOT NULL CHECK(phase IN ('FIELD','VOID')),
                  cursor INTEGER NOT NULL CHECK(cursor BETWEEN 0 AND 5),
                  sequence INTEGER NOT NULL CHECK(sequence>=0),
                  status TEXT NOT NULL CHECK(status IN ('running','paused','completed')),
                  version INTEGER NOT NULL, payload TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS artifacts(
                  id TEXT PRIMARY KEY, job TEXT NOT NULL, cursor INTEGER NOT NULL,
                  payload TEXT NOT NULL, hash TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS audits(
                  id TEXT PRIMARY KEY, job TEXT NOT NULL, artifact TEXT NOT NULL,
                  decision TEXT NOT NULL CHECK(decision IN ('ALLOW','CORRECT','HOLD','ESCALATE')),
                  payload TEXT NOT NULL, hash TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS transitions(
                  job TEXT NOT NULL, sequence INTEGER NOT NULL,
                  payload TEXT NOT NULL, hash TEXT NOT NULL, previous_hash TEXT,
                  PRIMARY KEY(job,sequence));
                CREATE TABLE IF NOT EXISTS source_versions(
                  id TEXT PRIMARY KEY, payload TEXT NOT NULL, hash TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS record_versions(
                  id TEXT PRIMARY KEY, record_key TEXT NOT NULL, source_version TEXT NOT NULL,
                  previous_id TEXT, payload TEXT NOT NULL, hash TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS consequences(
                  job TEXT PRIMARY KEY, record_version TEXT NOT NULL,
                  payload TEXT NOT NULL, hash TEXT NOT NULL);
            ''')
            expected = {'store_id': self.store_id, 'schema_version': SCHEMA_VERSION, 'path': str(self.path)}
            existing = dict(db.execute('SELECT key,value FROM identity'))
            if existing and existing != expected:
                raise ValueError('Store identity, location or schema mismatch; explicit migration required')
            if not existing:
                db.executemany('INSERT INTO identity VALUES (?,?)', expected.items())
            # The exact archive is append-only even if an ordinary caller tries SQL mutation.
            for table in ('artifacts', 'audits', 'transitions', 'source_versions', 'record_versions', 'consequences', 'identity'):
                for operation in ('UPDATE', 'DELETE'):
                    db.execute(f"CREATE TRIGGER IF NOT EXISTS immutable_{table}_{operation} BEFORE {operation} ON {table} BEGIN SELECT RAISE(ABORT,'append-only archive'); END")
        os.chmod(self.path, 0o600)
        # Configuration only, never duplicate the shared consequence into this journal.
        with self.app.db() as db:
            db.execute('CREATE TABLE IF NOT EXISTS knowledge_binding(singleton INTEGER PRIMARY KEY CHECK(singleton=1), store_id TEXT, path TEXT)')
            binding = db.execute('SELECT store_id,path FROM knowledge_binding WHERE singleton=1').fetchone()
            if binding and binding != (self.store_id, str(self.path)):
                raise ValueError('App already bound to another knowledge store; explicit migration required')
            if not binding:
                db.execute('INSERT INTO knowledge_binding VALUES (1,?,?)', (self.store_id, str(self.path)))

    def db(self):
        return sqlite3.connect(self.path.as_uri()+'?mode=ro',uri=True,timeout=30) if self.read_only else sqlite3.connect(self.path, timeout=30)

    @contextmanager
    def guard(self):
        if self.read_only:raise ValueError('Read-only knowledge handle cannot mutate')
        with open(str(self.path)+'.worker.lock', 'a') as handle:
            os.chmod(handle.name, 0o600)
            try:
                fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                raise Busy('Shared knowledge worker busy; reconcile existing job instead of duplicating it')
            yield

    @staticmethod
    def normalize(request):
        if not isinstance(request, dict) or set(request) != {'goal','repo','path','start_line','end_line'}:
            raise ValueError('Expected goal, repo, path, start_line and end_line only')
        value = dict(request)
        for key in ('goal','repo','path'):
            if not isinstance(value[key], str):
                raise ValueError('String request fields required')
            value[key] = value[key].strip()
        if not 1 <= len(value['goal']) <= 2000 or value['repo'] != SCIENCE:
            raise ValueError('First source-record slice requires a goal and the configured Science repository')
        path = value['path']
        if not path.endswith('.md') or path.startswith(('.', '/', 'External_Work/')) or '..' in path.split('/') or '\\' in path:
            raise ValueError('Only tracked public Markdown source paths are permitted')
        a,b = value['start_line'],value['end_line']
        if type(a) is not int or type(b) is not int or not 1 <= a <= b or b-a >= 60:
            raise ValueError('Source span must contain 1–60 positive numbered lines')
        return value

    def begin(self, identity, request):
        if not isinstance(identity,str) or not re.fullmatch(r'[A-Za-z0-9_.:-]{1,120}', identity):
            raise ValueError('Stable bounded job ID required')
        request = self.normalize(request)
        request_hash = digest(request)
        with self.guard(), self.db() as db:
            db.execute('BEGIN IMMEDIATE')
            old = db.execute('SELECT request_hash FROM jobs WHERE id=?',(identity,)).fetchone()
            if old:
                if old[0] != request_hash:
                    raise ValueError('Idempotency key already binds a different goal or input')
            else:
                job = dict(id=identity, request=request, request_hash=request_hash, store_id=self.store_id,
                           phase='FIELD', cursor=0, sequence=0, status='running', attempts=0,
                           world=None, proposal=None, counterproposal=None, artifact=None,
                           decision=None, dependency=None, receipt=None)
                db.execute('INSERT INTO jobs VALUES (?,?,?,?,?,?,?,?)',
                           (identity,request_hash,'FIELD',0,0,'running',0,encoded(job)))
        return self.get(identity)

    def load(self, db, identity):
        row = db.execute('SELECT payload,version,phase,cursor,sequence,status,request_hash FROM jobs WHERE id=?',(identity,)).fetchone()
        if not row:
            raise ValueError('Knowledge job not found')
        job = json.loads(row[0])
        version = row[1]
        if (job['phase'],job['cursor'],job['sequence'],job['status'],job['request_hash']) != row[2:]:
            raise ValueError('Stored job invariant mismatch')
        if digest(job['request']) != job['request_hash'] or job['store_id'] != self.store_id:
            raise ValueError('Stored request or store identity changed')
        previous=None;sequence=0
        expected_state={'phase':'FIELD','cursor':0,'status':'running'}
        for payload,stored_hash,prior in db.execute('SELECT payload,hash,previous_hash FROM transitions WHERE job=? ORDER BY sequence',(identity,)):
            event=json.loads(payload);sequence+=1
            if (event['sequence']!=sequence or event['job']!=identity or event['before']!=expected_state or digest(event)!=stored_hash or
                prior!=previous or event['previous_hash']!=previous):
                raise ValueError('Transition archive integrity failed')
            previous=stored_hash
            expected_state=event['after']
        if sequence!=job['sequence']:raise ValueError('Job and transition sequence disagree')
        if expected_state!={k:job[k] for k in ('phase','cursor','status')}:
            raise ValueError('Job state skipped its recorded transition boundary')
        if job['world']:
            row=db.execute('SELECT payload,hash FROM artifacts WHERE job=? AND cursor=0 ORDER BY rowid LIMIT 1',(identity,)).fetchone()
            if not row or digest(json.loads(row[0]))!=row[1] or json.loads(row[0])['data']['world']!=job['world']:
                raise ValueError('M4 active world changed outside its retained artifact')
        if job['status']=='completed':
            consequence=db.execute('SELECT payload,hash FROM consequences WHERE job=?',(identity,)).fetchone()
            if not consequence or digest(json.loads(consequence[0]))!=consequence[1] or json.loads(consequence[0])!=job['receipt']:
                raise ValueError('Completed job consequence is absent or changed')
        job['_version'] = version
        return job

    def get(self, identity):
        with self.db() as db:
            db.execute('BEGIN')
            return self.load(db, identity)

    def write_job(self, db, job):
        payload = {k:v for k,v in job.items() if k != '_version'}
        count = db.execute('UPDATE jobs SET phase=?,cursor=?,sequence=?,status=?,version=version+1,payload=? WHERE id=? AND version=?',
                           (job['phase'],job['cursor'],job['sequence'],job['status'],encoded(payload),job['id'],job['_version'])).rowcount
        if count != 1:
            raise ValueError('Concurrent job change; transaction rejected')

    def source_text(self, ref, path):
        if path not in self.app.paths(ref):
            raise ValueError('Required tracked source or authority is missing')
        if ref['root']:
            # Preserve exact UTF-8 newline bytes; text-mode git helpers normalize CRLF.
            size = int(subprocess.check_output(['git','-C',ref['root'],'cat-file','-s',ref['commit']+':'+path]))
            if size > 250000:
                raise ValueError('Source exceeds bounded read size')
            return subprocess.check_output(['git','-C',ref['root'],'show',ref['commit']+':'+path]).decode('utf-8')
        return self.app.source(ref,path)

    def observe(self, request):
        refs = self.app.reference()
        ref = next((r for r in refs if r['repo']==request['repo']), None)
        if ref is None:
            raise ValueError('Science repository is outside configured reference scope')
        authorities = []
        for path in AUTHORITIES:
            text = self.source_text(ref,path)
            authorities.append({'repo':ref['repo'],'commit':ref['commit'],'path':path,'content_hash':text_hash(text)})
        text = self.source_text(ref,request['path'])
        lines = text.splitlines(keepends=True)
        if request['end_line'] > len(lines):
            raise ValueError('Requested source span is absent')
        quote = ''.join(lines[request['start_line']-1:request['end_line']])
        if not quote.strip() or len(quote.encode('utf-8')) > 12000:
            raise ValueError('Empty or oversized source excerpt')
        raw_metadata = text.split('---',2)[1] if text.startswith('---\n') and len(text.split('---',2))==3 else ''
        metadata = {}
        for key in ('node_id','gate','lifecycle','classification'):
            match = re.search(r'^'+key+r':\s*(.+?)\s*$', raw_metadata, re.M)
            metadata[key] = match[1].strip('"\'') if match else None
        source = dict(repo=ref['repo'],commit=ref['commit'],path=request['path'],content_hash=text_hash(text),
                      declared_metadata=raw_metadata, metadata=metadata,
                      metadata_status='declared-source-fields' if raw_metadata else 'unresolved')
        record = dict(source=source, start_line=request['start_line'], end_line=request['end_line'], quote=quote,
                      evidence_class='repository-statement', qualification='exact-source-span',
                      proposition_status='NOT_VALIDATED', uncertainty=['Source fidelity does not establish proposition truth.'])
        bundle = dict(repositories=refs, authorities=authorities, source=source)
        return {'bundle':bundle,'reference_hash':digest(bundle),'record':record}

    def observations(self, request):
        try:
            return self.observe(request), None
        except (ValueError, OSError, subprocess.SubprocessError, UnicodeError) as error:
            return None, {'code':'REFERENCE_UNAVAILABLE','detail':type(error).__name__}

    def append_transition(self, db, job, before, disposition, binding):
        previous = db.execute('SELECT hash FROM transitions WHERE job=? ORDER BY sequence DESC LIMIT 1',(job['id'],)).fetchone()
        job['sequence'] += 1
        payload = dict(job=job['id'],sequence=job['sequence'],before=before,
                       after={'phase':job['phase'],'cursor':job['cursor'],'status':job['status']},
                       disposition=disposition,binding=binding,previous_hash=previous[0] if previous else None)
        db.execute('INSERT INTO transitions VALUES (?,?,?,?,?)',
                   (job['id'],job['sequence'],encoded(payload),digest(payload),payload['previous_hash']))

    def field_artifact(self, job, observed, db):
        cursor = job['cursor']
        binding = dict(job=job['id'],cursor=cursor,reference_hash=observed['reference_hash'],request_hash=job['request_hash'])
        if cursor == 0:
            record_key = digest({k:job['request'][k] for k in ('repo','path','start_line','end_line')})
            prior = db.execute('SELECT id,payload,hash FROM record_versions WHERE record_key=? ORDER BY rowid DESC LIMIT 1',(record_key,)).fetchone()
            prior_record = None
            if prior:
                prior_record=json.loads(prior[1])
                if digest(prior_record)!=prior[2]:raise ValueError('Retained record hash mismatch')
            world = dict(goal=job['request']['goal'],reference=observed['bundle'],reference_hash=observed['reference_hash'],
                         record_key=record_key,prior_record_id=prior[0] if prior else None,
                         prior_consequence=prior_record,pending_findings=job.get('counterproposal'))
            job['world'] = world
            data = {'kind':'active-world','world':world}
        elif cursor == 1:
            candidate = job['counterproposal'] or observed['record']
            if self.proposer is not None:
                candidate = self.proposer(json.loads(encoded(candidate)),job['attempts'])
            job['proposal'] = candidate
            data = {'kind':'proposal','operation':'append-source-record','record':candidate,'permission':'source-fidelity-only'}
        elif cursor == 2:
            data = {'kind':'readiness','authorized_hash':job['authorized_hash'],'record_hash':digest(job['proposal'])}
        elif cursor == 3:
            data = {'kind':'staged-record','record':job['proposal'],'ready_hash':job['ready_hash']}
        elif cursor == 4:
            data = {'kind':'differential','record_hash':digest(job['proposal']),'staged_hash':job['staged_hash'],
                    'proposition_status':'NOT_VALIDATED'}
        else:
            data = {'kind':'consequence','record_hash':digest(job['proposal']),'audit_hash':job['qualified_audit'],
                    'next_phase':'FIELD','next_cursor':0}
        return {'binding':binding,'data':data}

    def void_audit(self, job, artifact, observed):
        binding = artifact['binding']
        expected = dict(job=job['id'],cursor=job['cursor'],reference_hash=observed['reference_hash'],request_hash=job['request_hash'])
        if binding != expected:
            return 'HOLD', 'ARTIFACT_REFERENCE_MISMATCH', None
        cursor = job['cursor']; data = artifact['data']
        if cursor == 0:
            valid = (data.get('kind')=='active-world' and data.get('world')==job['world'] and
                     job['world']['reference']==observed['bundle'])
        else:
            # Exact complete payload match independently binds quote, span, metadata,
            # source version and inherited evidence class. No model confidence score.
            if job['proposal'] != observed['record']:
                return ('CORRECT','SOURCE_FIDELITY_MISMATCH',observed['record']) if cursor==1 else ('HOLD','AUTHORIZED_PROPOSAL_CHANGED',None)
            if cursor == 1:
                valid=(data.get('kind')=='proposal' and data.get('operation')=='append-source-record' and
                       data.get('permission')=='source-fidelity-only' and data.get('record')==job['proposal'])
            elif cursor == 2:
                valid=(data=={'kind':'readiness','authorized_hash':job.get('authorized_hash'),'record_hash':digest(job['proposal'])} and bool(job.get('authorized_hash')))
            elif cursor == 3:
                valid=(data=={'kind':'staged-record','record':job['proposal'],'ready_hash':job.get('ready_hash')} and bool(job.get('ready_hash')))
            elif cursor == 4:
                valid=(data=={'kind':'differential','record_hash':digest(job['proposal']),'staged_hash':job.get('staged_hash'),'proposition_status':'NOT_VALIDATED'} and bool(job.get('staged_hash')))
            else:
                valid=(data=={'kind':'consequence','record_hash':digest(job['proposal']),'audit_hash':job.get('qualified_audit'),'next_phase':'FIELD','next_cursor':0} and bool(job.get('qualified_audit')))
        return ('ALLOW','SOURCE_CONTRACT_MATCH',None) if valid else ('HOLD','STEP_CONTRACT_MISMATCH',None)

    def checkpoint(self, boundary):
        """Test seam; no network or provider operation is dispatched by this core."""
        pass

    def advance(self, identity):
        try:
            return self.advance_once(identity)
        except ReferenceDrift:
            with self.guard(), self.db() as db:
                db.execute('BEGIN IMMEDIATE');job=self.load(db,identity)
                if job['status']=='running':
                    before={k:job[k] for k in ('phase','cursor','status')}
                    job.update(status='paused',decision='HOLD',dependency={'code':'REFERENCE_CHANGED_DURING_TRANSITION','required':'new goal revision'})
                    self.append_transition(db,job,before,'HOLD',job['dependency']);self.write_job(db,job)
            return self.public(self.get(identity))

    def verify_prior_audits(self, db, job, observed):
        for cursor,key in ((0,'reference_audit'),(1,'authorized_audit'),(2,'ready_audit'),(3,'staged_audit'),(4,'qualified_audit_id')):
            if job['cursor']<=cursor:continue
            row=db.execute('SELECT payload,hash FROM audits WHERE id=? AND job=?',(job.get(key),job['id'])).fetchone()
            if not row:raise ValueError('Required prior Void authorization is absent')
            audit=json.loads(row[0])
            artifact=db.execute('SELECT payload,hash FROM artifacts WHERE id=? AND job=?',(audit['artifact_id'],job['id'])).fetchone()
            if (digest(audit)!=row[1] or audit['decision']!='ALLOW' or audit['cursor']!=cursor or
                audit['reference_hash']!=observed['reference_hash'] or audit['candidate_hash']!=digest(None if cursor==0 else job['proposal']) or
                not artifact or digest(json.loads(artifact[0]))!=artifact[1] or artifact[1]!=audit['artifact_hash']):
                raise ValueError('Prior Void authorization binding failed')

    def advance_once(self, identity):
        with self.guard(), self.db() as db:
            db.execute('BEGIN IMMEDIATE')
            job = self.load(db,identity)
            if job['status'] != 'running':
                return self.public(job)
            before = {'phase':job['phase'],'cursor':job['cursor'],'status':job['status']}
            observed,error = self.observations(job['request'])
            if error or (job['world'] and observed['reference_hash']!=job['world']['reference_hash']):
                job.update(status='paused',decision='HOLD',dependency=error or {'code':'REFERENCE_CHANGED','required':'new goal revision'},)
                self.append_transition(db,job,before,'HOLD',job['dependency']);self.write_job(db,job)
            elif job['phase']=='FIELD':
                self.verify_prior_audits(db,job,observed)
                artifact = self.field_artifact(job,observed,db)
                artifact_id=job['id']+':field:'+str(job['sequence']+1)
                artifact_hash=digest(artifact)
                db.execute('INSERT INTO artifacts VALUES (?,?,?,?,?)',(artifact_id,job['id'],job['cursor'],encoded(artifact),artifact_hash))
                job.update(artifact=artifact_id,artifact_hash=artifact_hash,phase=TRANSITIONS['FIELD']['PROPOSE'],decision=None)
                self.append_transition(db,job,before,'PROPOSE',artifact['binding']);self.write_job(db,job)
            else:
                self.verify_prior_audits(db,job,observed)
                row=db.execute('SELECT payload,hash FROM artifacts WHERE id=? AND job=?',(job['artifact'],job['id'])).fetchone()
                if not row or digest(json.loads(row[0]))!=row[1] or row[1]!=job['artifact_hash']:
                    raise ValueError('Immutable Field artifact hash mismatch')
                artifact=json.loads(row[0])
                decision,reason,counter=self.void_audit(job,artifact,observed)
                if decision=='CORRECT':
                    job['attempts']+=1
                    if job['attempts']>=MAX_ATTEMPTS:decision='ESCALATE'
                audit=dict(job=job['id'],cursor=job['cursor'],artifact_id=job['artifact'],artifact_hash=row[1],
                           reference_hash=observed['reference_hash'],candidate_hash=digest(job['proposal']),
                           decision=decision,reason=reason,counterproposal=counter,validator='exact-source-span/v1')
                audit_id=job['id']+':void:'+str(job['sequence']+1)
                audit_hash=digest(audit)
                db.execute('INSERT INTO audits VALUES (?,?,?,?,?,?)',(audit_id,job['id'],job['artifact'],decision,encoded(audit),audit_hash))
                job['decision']=decision
                if decision=='CORRECT':
                    job.update(counterproposal=counter,phase=TRANSITIONS['VOID'][decision])
                elif decision in {'HOLD','ESCALATE'}:
                    job.update(status='paused',dependency={'code':reason},phase=TRANSITIONS['VOID'][decision])
                else:
                    if job['cursor']==0:job['reference_audit']=audit_id
                    if job['cursor']==1:job.update(authorized_hash=digest(job['proposal']),authorized_audit=audit_id)
                    if job['cursor']==2:job.update(ready_hash=digest(job['proposal']),ready_audit=audit_id)
                    if job['cursor']==3:job.update(staged_hash=digest(job['proposal']),staged_audit=audit_id)
                    if job['cursor']==4:job.update(qualified_audit=audit_hash,qualified_audit_id=audit_id)
                    if job['cursor']==5:
                        self.commit_record(db,job,audit_id,audit_hash)
                        job.update(status='completed',cursor=0)
                    else:job['cursor']+=1
                    job['phase']=TRANSITIONS['VOID'][decision]
                self.append_transition(db,job,before,decision,{'audit':audit_id,'hash':audit_hash})
                self.write_job(db,job)
            self.checkpoint('before-commit')
            # Recheck outside generated artifacts immediately before the DB commit.
            last,last_error=self.observations(job['request'])
            if observed and (last_error or last['reference_hash']!=observed['reference_hash']):
                raise ReferenceDrift('Reference changed during transition; transaction rolled back')
        self.checkpoint('after-commit')
        return self.public(self.get(identity))

    def commit_record(self, db, job, audit_id, audit_hash):
        record=job['proposal'];version_id=digest(record);source=record['source'];source_id=digest(source)
        old=db.execute('SELECT payload,hash FROM record_versions WHERE id=?',(version_id,)).fetchone()
        if old and (json.loads(old[0])!=record or old[1]!=version_id):
            raise ValueError('Existing record version failed integrity check')
        if not old:
            prior=db.execute('SELECT id FROM record_versions WHERE record_key=? ORDER BY rowid DESC LIMIT 1',(job['world']['record_key'],)).fetchone()
            db.execute('INSERT OR IGNORE INTO source_versions VALUES (?,?,?)',(source_id,encoded(source),source_id))
            db.execute('INSERT INTO record_versions VALUES (?,?,?,?,?,?)',
                       (version_id,job['world']['record_key'],source_id,prior[0] if prior else None,encoded(record),version_id))
        receipt=dict(id=job['id']+':consequence',store_id=self.store_id,job=job['id'],record_version=version_id,
                     source_version=source_id,audit_id=audit_id,audit_hash=audit_hash,reference_hash=job['world']['reference_hash'],
                     reused=bool(old),evidence_class='repository-statement',proposition_status='NOT_VALIDATED',
                     prior_record_id=job['world']['prior_record_id'],next={'phase':'FIELD','cursor':0})
        db.execute('INSERT INTO consequences VALUES (?,?,?,?)',(job['id'],version_id,encoded(receipt),digest(receipt)))
        job['receipt']=receipt

    def run(self, identity, request=None):
        if request is not None:self.begin(identity,request)
        for _ in range(12+MAX_ATTEMPTS*2):
            job=self.get(identity)
            if job['status']!='running':return self.public(job)
            self.advance(identity)
        raise ValueError('Bounded transition budget exhausted')

    @staticmethod
    def public(job):
        return {k:job.get(k) for k in ('id','store_id','phase','cursor','sequence','status','attempts','decision','dependency','receipt')}

    def record(self, identity):
        with self.db() as db:
            db.execute('BEGIN')
            row=db.execute('SELECT payload,hash,source_version FROM record_versions WHERE id=?',(identity,)).fetchone()
            if not row or digest(json.loads(row[0]))!=row[1] or row[1]!=identity:raise ValueError('Committed record missing or corrupt')
            record=json.loads(row[0]);source=db.execute('SELECT payload,hash FROM source_versions WHERE id=?',(row[2],)).fetchone()
            if not source or digest(json.loads(source[0]))!=source[1] or source[1]!=row[2] or json.loads(source[0])!=record['source']:
                raise ValueError('Committed source provenance is corrupt')
            receipt=db.execute('SELECT job,payload,hash FROM consequences WHERE record_version=? ORDER BY rowid LIMIT 1',(identity,)).fetchone()
            if not receipt or digest(json.loads(receipt[1]))!=receipt[2]:raise ValueError('Accepted consequence is absent or corrupt')
            consequence=json.loads(receipt[1]);job=self.load(db,receipt[0])
            audit=db.execute('SELECT payload,hash FROM audits WHERE id=?',(consequence['audit_id'],)).fetchone()
            if (job['status']!='completed' or job['receipt']!=consequence or not audit or
                digest(json.loads(audit[0]))!=audit[1] or audit[1]!=consequence['audit_hash'] or
                json.loads(audit[0])['decision']!='ALLOW' or json.loads(audit[0])['candidate_hash']!=identity):
                raise ValueError('Accepted record audit chain is corrupt')
        return record

    def trace(self, identity):
        with self.db() as db:
            db.execute('BEGIN')
            job=self.load(db,identity)
            transitions=[json.loads(r[0]) for r in db.execute('SELECT payload FROM transitions WHERE job=? ORDER BY sequence',(identity,))]
            audits=[]
            for payload,stored_hash in db.execute('SELECT payload,hash FROM audits WHERE job=? ORDER BY rowid',(identity,)):
                audit=json.loads(payload)
                artifact=db.execute('SELECT payload,hash FROM artifacts WHERE id=? AND job=?',(audit['artifact_id'],identity)).fetchone()
                if (digest(audit)!=stored_hash or audit['job']!=identity or not artifact or
                    digest(json.loads(artifact[0]))!=artifact[1] or artifact[1]!=audit['artifact_hash'] or
                    json.loads(artifact[0])['binding']['cursor']!=audit['cursor'] or
                    json.loads(artifact[0])['binding']['reference_hash']!=audit['reference_hash']):
                    raise ValueError('Audit archive binding failed')
                audits.append(audit)
        return {'job':self.public(job),'transitions':transitions,'audits':audits}


def main():
    from app import App
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo',required=True);parser.add_argument('--runtime-state',required=True)
    parser.add_argument('--knowledge-store',required=True);parser.add_argument('--store-id',required=True)
    parser.add_argument('--id',required=True);parser.add_argument('--path');parser.add_argument('--goal',default='Retain this source with provenance')
    parser.add_argument('--start-line',type=int,default=1);parser.add_argument('--end-line',type=int,default=1)
    args=parser.parse_args()
    app=App([args.repo],args.runtime_state,provider=lambda *a: (_ for _ in ()).throw(RuntimeError('Provider calls are not part of source qualification')))
    loop=KnowledgeLoop(app,args.knowledge_store,args.store_id)
    request=dict(goal=args.goal,repo=SCIENCE,path=args.path,start_line=args.start_line,end_line=args.end_line) if args.path else None
    result=loop.run(args.id,request)
    print(json.dumps(loop.trace(args.id),indent=2))
    return 0 if result['status']=='completed' else 2


if __name__=='__main__':raise SystemExit(main())
