"""Offline Council contract tests. No provider, relay, device or secret is used."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / 'brain_buddy_council.py'
spec = importlib.util.spec_from_file_location('council', SCRIPT)
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)


def snapshot(key='baseline'):
    return {'id': key, 'head': 'abc', 'contents': [{'path': 'authority.md', 'content': 'canonical'}]}


def result(worker='gemini', ok=True):
    return {'worker': worker, 'ok': ok, 'status': 'ANSWER_RETURNED' if ok else 'OUT_TO_LUNCH',
            'answer': worker + ' answer' if ok else '', 'stderr': '' if ok else 'offline', 'exit_code': 0 if ok else 1}


class WorkerTests(unittest.TestCase):
    def invoke(self, output='answer', code=0, snapshots=None, error=None):
        p = subprocess.CompletedProcess([], code, output, '')
        with patch.object(c, 'reference_snapshot', side_effect=snapshots or [snapshot(), snapshot()]), \
             patch.object(c.subprocess, 'run', side_effect=error, return_value=p) as run:
            r = c.run_worker(Path('/tmp'), 'gemini', 'question', 10, 'request-1')
            return r, run

    def test_nonempty_transport_receipt(self):
        r, run = self.invoke()
        self.assertTrue(r['ok'])
        self.assertEqual(r['request_id'], 'request-1')
        self.assertEqual(r['status'], 'ANSWER_RETURNED')
        self.assertIsNone(r['provider_response_id'])
        self.assertIn('canonical', run.call_args.kwargs['input'])
        self.assertNotIn('question', run.call_args.args[0])
        self.assertEqual(len(r['answer_sha256']), 64)

    def test_empty_answer_not_success(self):
        r, _ = self.invoke('  ')
        self.assertFalse(r['ok'])
        self.assertEqual(r['status'], 'INVALID_RETURN')

    def test_hold_prose_not_success(self):
        r, _ = self.invoke('HOLD — missing reference')
        self.assertFalse(r['ok'])
        self.assertEqual(r['status'], 'HOLD')

    def test_nonzero_preserves_output(self):
        r, _ = self.invoke('partial finding', 1)
        self.assertFalse(r['ok'])
        self.assertEqual(r['answer'], 'partial finding')

    def test_deadline_enforced_after_inner_reference_read(self):
        clock = [0.0]
        def source(*args):
            clock[0] = 11.0
            return snapshot()
        with patch.object(c, 'reference_snapshot', side_effect=source), patch.object(c.time, 'monotonic', side_effect=lambda: clock[0]), patch.object(c.subprocess, 'run') as run:
            receipt = c.run_worker(Path('/tmp'), 'gemini', 'q', 10, 'id', deadline=10)
        self.assertEqual(receipt['status'], 'BUDGET_EXHAUSTED')
        run.assert_not_called()

    def test_keyboard_interrupt_is_stopped_receipt(self):
        r, _ = self.invoke(error=KeyboardInterrupt())
        self.assertEqual(r['status'], 'STOPPED')
        self.assertEqual(r['exit_code'], 130)

    def test_timeout_explicit(self):
        r, _ = self.invoke(error=subprocess.TimeoutExpired('worker', 10))
        self.assertEqual(r['exit_code'], 124)
        self.assertEqual(r['status'], 'OUT_TO_LUNCH')

    def test_drift_invalidates_answer(self):
        r, _ = self.invoke(snapshots=[snapshot('old'), snapshot('new')])
        self.assertFalse(r['ok'])
        self.assertEqual(r['status'], 'RE_REFERENCE')
        self.assertEqual(r['answer'], 'answer')

    def test_missing_reference_stops_before_dispatch(self):
        with patch.object(c, 'reference_snapshot', side_effect=c.CouncilError('missing')), \
             patch.object(c.subprocess, 'run') as run:
            r = c.run_worker(Path('/tmp'), 'gemini', 'q', 10)
        run.assert_not_called()
        self.assertFalse(r['ok'])

    def test_exact_repository_identity(self):
        self.assertTrue(c.valid_origin('git@github.com:One-Wave-Universe/One-Wave-Science.git'))
        self.assertFalse(c.valid_origin('https://evil.invalid/One-Wave-Universe/One-Wave-Science'))
        self.assertFalse(c.valid_origin('https://github.com/One-Wave-Universe/One-Wave-Science-copy'))


class MainTests(unittest.TestCase):
    def run_main(self, argv, worker, user_turn=''):
        with patch.object(sys, 'argv', ['council', *argv]), \
             patch.object(c, 'repo_root', return_value=Path('/tmp')), \
             patch.object(c, 'run_worker', side_effect=worker) as calls, \
             patch.object(c, 'interactive_user_turn', return_value=user_turn), \
             contextlib.redirect_stdout(io.StringIO()):
            return c.main(), calls

    def test_discussion_is_cumulative_and_one_request(self):
        code, calls = self.run_main(['discussion', 'q', '--rounds', '2'], lambda root, w, *a: result(w))
        self.assertEqual(code, 0)
        self.assertEqual(calls.call_count, 4)
        self.assertIn('gemini answer', calls.call_args_list[1].args[2])
        self.assertEqual(len({x.args[4] for x in calls.call_args_list}), 1)

    def test_failed_peer_skipped_others_preserved(self):
        code, calls = self.run_main(['discussion', 'q', '--rounds', '3'], lambda root, w, *a: result(w, w == 'deepseek'))
        self.assertEqual(code, 2)
        self.assertEqual([x.args[1] for x in calls.call_args_list], ['gemini', 'deepseek', 'deepseek', 'deepseek'])

    def test_drift_prevents_next_peer_call(self):
        def worker(root, name, *args):
            return {**result(name, False), 'status': 'RE_REFERENCE'}
        code, calls = self.run_main(['discussion', 'q'], worker)
        self.assertEqual(code, 2)
        self.assertEqual(calls.call_count, 1)

    def test_long_plain_question_is_not_a_filename(self):
        self.assertEqual(c.read_prompt('question ' * 100), ('question ' * 100).strip())
        with self.assertRaises(c.CouncilError):
            c.read_prompt('q' * 16001)

    def test_interrupted_worker_stops_discussion(self):
        code, calls = self.run_main(['discussion', 'q'], lambda root, name, *a: {**result(name, False), 'status': 'STOPPED'})
        self.assertEqual(code, 0)
        self.assertEqual(calls.call_count, 1)

    def test_stop_prevents_more_calls(self):
        code, calls = self.run_main(['discussion', 'q', '--rounds', '3'], lambda root, w, *a: result(w), '/stop')
        self.assertEqual(code, 0)
        self.assertEqual(calls.call_count, 2)

    def test_user_correction_carried_forward(self):
        _, calls = self.run_main(['discussion', 'q', '--rounds', '2'], lambda root, w, *a: result(w), 'new correction')
        self.assertIn('new correction', calls.call_args_list[2].args[2])

    def test_sequential_failure_stops_handoff(self):
        code, calls = self.run_main(['gemini-deepseek', 'q'], lambda root, w, *a: result(w, False))
        self.assertEqual(code, 2)
        self.assertEqual(calls.call_count, 1)

    def test_independent_modes_preserved(self):
        for mode, expected in [('gemini', 1), ('deepseek', 1), ('both', 2), ('deepseek-gemini', 2)]:
            code, calls = self.run_main([mode, 'q'], lambda root, w, *a: result(w))
            self.assertEqual((code, calls.call_count), (0, expected))

    def test_unique_saved_transcripts_and_json(self):
        with tempfile.TemporaryDirectory() as d:
            paths = [c.save_transcript(Path(d), 'discussion', 'q', [], {'request_id': 'id'}) for _ in range(2)]
            self.assertNotEqual(*paths)
            self.assertEqual(json.loads(paths[0].with_suffix('.json').read_text())['request_id'], 'id')


class ReferenceTests(unittest.TestCase):
    def test_reads_actual_authorities_and_detects_dirty_change(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            def git(*args):
                subprocess.run(['git', '-C', d, *args], check=True, capture_output=True)
            git('init', '-q')
            git('remote', 'add', 'origin', 'https://github.com/One-Wave-Universe/One-Wave-Science.git')
            for name in c.ROOT_FILES:
                p = root / name
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text('authority')
            git('add', '.')
            git('-c', 'user.name=Test', '-c', 'user.email=test@example.invalid', 'commit', '-qm', 'fixture')
            before = c.reference_snapshot(root)
            (root / c.ROOT_FILES[0]).write_text('changed authority')
            after = c.reference_snapshot(root)
            self.assertNotEqual(before['id'], after['id'])
            self.assertEqual(after['contents'][0]['content'], 'changed authority')
            self.assertEqual(before['head'], after['head'])
            with self.assertRaises(c.CouncilError):
                c.reference_snapshot(root, ['../outside.md'])
            with self.assertRaises(c.CouncilError):
                c.reference_snapshot(root, ['missing.md'])
            node = root / 'Node.md'
            node.write_text('---\nnode_id: TEST\ngate: YELLOW\n---\nhypothesis')
            git('add', 'Node.md')
            extended = c.reference_snapshot(root, ['Node.md'])
            self.assertIn('gate: YELLOW', extended['contents'][-1]['content'])
            self.assertNotEqual(extended['id'], after['id'])


class LoopTests(unittest.TestCase):
    def run_loop(self, change=None, snapshot_change=None, **kwargs):
        packets = []
        snapshot_paths = []
        ref = {**snapshot(), 'files': [{'path': 'authority.md', 'sha256': 'abc'}]}
        def worker(root, name, prompt, timeout, rid, reference_paths=(), **kwargs):
            packet = json.loads(prompt.split('COUNCIL_PACKET:\n', 1)[1])
            packets.append(packet)
            value = {'request_id': rid, 'turn_id': str(len(packets)), 'reference_id': 'baseline',
                     'loop_id': packet['loop_id'], 'step': packet['step'], 'phase': packet['phase'],
                     'answer': 'Public artifact for ' + packet['step_name'], 'references': ['authority.md'],
                     'unresolved': [], 'objections': [], 'reference_required': False,
                     'child_question': None, 'next_action': None}
            if packet['phase'] == 'VOID':
                value.update(decision='ALLOW', candidate_sha256=packet['candidate']['sha256'])
            response = {**result(name), 'request_id': rid, 'turn_id': str(len(packets)),
                        'reference': ref, 'elapsed_s': 0.01}
            if change:
                change(packet, value, response)
            response['answer'] = json.dumps(value)
            return response
        def source(root, paths=()):
            snapshot_paths.append(set(paths))
            if snapshot_change:
                snapshot_change(ref, snapshot_paths)
            return ref
        with patch.object(c, 'reference_snapshot', side_effect=source), patch.object(c, 'run_worker', side_effect=worker):
            receipt = c.run_council_loop(Path('/tmp'), 'question', 'r1', **kwargs)
        self.snapshot_paths = snapshot_paths
        return receipt, packets

    def test_six_paired_steps_not_twelve_states(self):
        rec, packets = self.run_loop()
        self.assertEqual(rec['status'], 'AGREED_RESOLUTION')
        self.assertEqual([(p['step'], p['phase']) for p in packets], [(i, p) for i in range(1, 7) for p in ('FIELD', 'VOID')])
        self.assertEqual(len(rec['loops'][0]['consequences']), 6)
        self.assertEqual(rec['budget']['calls_used'], 12)

    def test_exact_candidate_hash_required(self):
        def change(p, v, r):
            if p['phase'] == 'VOID':
                v['candidate_sha256'] = 'different'
        rec, packets = self.run_loop(change)
        self.assertEqual(rec['status'], 'INVALID_RETURN')
        self.assertEqual(len(packets), 2)

    def test_wrong_request_identity_rejected(self):
        rec, packets = self.run_loop(lambda p, v, r: v.update(request_id='other'))
        self.assertEqual(rec['status'], 'INVALID_RETURN')
        self.assertEqual(len(packets), 1)

    def test_unseen_reference_citation_rejected(self):
        rec, _ = self.run_loop(lambda p, v, r: v.update(references=['made-up.md']))
        self.assertEqual(rec['status'], 'INVALID_RETURN')

    def test_child_returns_before_parent_resumes(self):
        requested = []
        def change(p, v, r):
            if not requested and p['depth'] == 0 and p['step'] == 2 and p['phase'] == 'VOID':
                v.update(decision='CORRECT', child_question='bounded missing evidence')
                requested.append(True)
        rec, packets = self.run_loop(change)
        self.assertEqual(rec['status'], 'AGREED_RESOLUTION')
        self.assertEqual(rec['loops'][0]['children'][0]['reference_id'], 'baseline')
        self.assertEqual(len(rec['loops'][0]['children'][0]['sha256']), 64)
        parent, child = rec['loops']
        self.assertEqual((child['parent_id'], child['parent_step'], child['depth']), (parent['id'], 2, 1))
        parent_after_child = [p for p in packets if p['depth'] == 0 and p['child_returns']]
        self.assertEqual(parent_after_child[0]['step'], 2)
        self.assertEqual(parent_after_child[0]['phase'], 'FIELD')
        self.assertEqual(parent_after_child[0]['child_returns'][0]['status'], 'AGREED_RESOLUTION')
        self.assertEqual(rec['budget']['calls_used'], 26)

    def test_child_failure_holds_parent(self):
        def change(p, v, r):
            if p['depth'] == 0 and p['phase'] == 'VOID':
                v.update(decision='CORRECT', child_question='missing')
            if p['depth'] == 1:
                r.update(ok=False, status='OUT_TO_LUNCH')
        rec, packets = self.run_loop(change)
        self.assertEqual(rec['status'], 'HOLD')
        self.assertEqual(len(packets), 3)
        self.assertEqual(rec['loops'][0]['step'], 1)

    def test_shared_budget_bounds_children_and_retries(self):
        def change(p, v, r):
            if p['depth'] == 0 and p['phase'] == 'VOID':
                v.update(decision='CORRECT', child_question='missing')
        rec, packets = self.run_loop(change, max_calls=5)
        self.assertEqual(rec['status'], 'BUDGET_EXHAUSTED')
        self.assertEqual(len(packets), 5)
        self.assertEqual(rec['loops'][1]['status'], 'BUDGET_EXHAUSTED')

    def test_depth_limit_holds(self):
        def change(p, v, r):
            if p['phase'] == 'VOID':
                v.update(decision='CORRECT', child_question='missing')
        rec, packets = self.run_loop(change, max_depth=0)
        self.assertEqual(rec['status'], 'HOLD')
        self.assertEqual(len(packets), 2)

    def test_three_rejected_attempts_stop(self):
        def change(p, v, r):
            if p['phase'] == 'VOID':
                v.update(decision='CORRECT')
        rec, packets = self.run_loop(change)
        self.assertEqual(rec['status'], 'ESCALATE')
        self.assertEqual(len(packets), 6)

    def test_reference_requests_trigger_actual_snapshot_read(self):
        first = []
        def change(p, v, r):
            if not first:
                first.append(True)
                v.update(reference_required=True, reference_requests=['Nodes/test.md'])
        rec, packets = self.run_loop(change)
        self.assertIn({'Nodes/test.md'}, self.snapshot_paths)
        self.assertTrue(any(e['kind'] == 'RE_REFERENCE' for e in rec['loops'][0]['events']))

    def test_uncertainty_automatically_rereferences(self):
        first = []
        def change(p, v, r):
            if not first:
                first.append(True)
                v['reference_required'] = True
        rec, packets = self.run_loop(change)
        self.assertEqual(rec['status'], 'AGREED_RESOLUTION')
        self.assertEqual([(p['step'], p['phase']) for p in packets[:2]], [(1, 'FIELD'), (1, 'FIELD')])
        self.assertTrue(any(e['kind'] == 'RE_REFERENCE' for e in rec['loops'][0]['events']))

    def test_stop_before_dispatch(self):
        rec, packets = self.run_loop(should_stop=lambda: True)
        self.assertEqual(rec['status'], 'STOPPED')
        self.assertEqual(packets, [])

    def test_results_display_before_user_redirect(self):
        displayed = []
        def user(step):
            self.assertEqual(len(displayed), 2)
            return '/stop'
        rec, packets = self.run_loop(user_input=user, on_result=lambda r: displayed.append(r))
        self.assertEqual(rec['status'], 'STOPPED')

    def test_loop_worker_interrupt_retains_prior_results(self):
        def change(p, v, r):
            if p['phase'] == 'VOID':
                r.update(ok=False, status='STOPPED')
        rec, packets = self.run_loop(change)
        self.assertEqual(rec['status'], 'STOPPED')
        self.assertEqual(len(rec['results']), 2)

    def test_history_age_has_no_truth_score(self):
        rec, packets = self.run_loop()
        time_history = packets[-1]['history_weight_of_time']
        self.assertTrue(time_history)
        self.assertTrue(all(x['age_s'] >= 0 and x['reference_relation'] == 'current' for x in time_history))
        self.assertTrue(all('confidence' not in x for x in time_history))

    def test_interactive_stop_prevents_next_step(self):
        rec, packets = self.run_loop(user_input=lambda step: '/stop')
        self.assertEqual(rec['status'], 'STOPPED')
        self.assertEqual(len(packets), 2)

    def test_allow_cannot_hide_objections(self):
        def change(p, v, r):
            if p['phase'] == 'VOID':
                v['objections'] = ['Contradicting measurement']
        rec, _ = self.run_loop(change)
        self.assertEqual(rec['status'], 'INVALID_RETURN')

    def test_field_objection_cannot_be_erased_by_void(self):
        def change(p, v, r):
            if p['step'] == 6 and p['phase'] == 'FIELD':
                v['objections'] = ['A material contradiction remains.']
        rec, _ = self.run_loop(change)
        self.assertEqual(rec['status'], 'HOLD')

    def test_deadline_rechecked_after_reference_before_dispatch(self):
        clock = [0.0]
        def advance(ref, paths):
            clock[0] = 1201.0
        with patch.object(c.time, 'monotonic', side_effect=lambda: clock[0]):
            rec, packets = self.run_loop(snapshot_change=advance)
        self.assertEqual(rec['status'], 'BUDGET_EXHAUSTED')
        self.assertEqual(packets, [])

    def test_final_late_return_not_accepted(self):
        clock = [0.0]
        def change(p, v, r):
            if p['step'] == 6 and p['phase'] == 'VOID':
                clock[0] = 1201.0
        with patch.object(c.time, 'monotonic', side_effect=lambda: clock[0]):
            rec, packets = self.run_loop(change)
        self.assertEqual(rec['status'], 'BUDGET_EXHAUSTED')
        self.assertEqual(len(packets), 12)

    def test_redirection_excludes_old_goal_child(self):
        requested = []
        redirected = []
        def change(p, v, r):
            if not requested and p['depth'] == 0 and p['phase'] == 'VOID':
                requested.append(True)
                v.update(decision='CORRECT', child_question='old goal subquestion')
        def user(step):
            if not redirected:
                redirected.append(True)
                return 'Different goal'
            return ''
        rec, packets = self.run_loop(change, user_input=user)
        self.assertEqual(rec['status'], 'AGREED_RESOLUTION')
        self.assertTrue(rec['loops'][0]['children'])  # historical evidence retained
        changed = [p for p in packets if 'Different goal' in p['goal']]
        self.assertTrue(changed)
        self.assertTrue(all(not p['child_returns'] for p in changed))

    def test_unresolved_final_is_next_action_not_truth(self):
        def change(p, v, r):
            if p['step'] == 6:
                v.update(unresolved=['Measurement missing'], next_action='Measure one bounded sample')
        rec, _ = self.run_loop(change)
        self.assertEqual(rec['status'], 'AGREED_NEXT_ACTION')

    def test_whitespace_next_action_cannot_resolve_missing_evidence(self):
        def change(p, v, r):
            if p['step'] == 6:
                v.update(unresolved=['Measurement missing'], next_action='   ')
        rec, _ = self.run_loop(change)
        self.assertEqual(rec['status'], 'HOLD')

    def test_interrupt_during_source_read_retains_stopped_receipt(self):
        def source(ref, paths):
            raise KeyboardInterrupt()
        rec, packets = self.run_loop(snapshot_change=source)
        self.assertEqual(rec['status'], 'STOPPED')
        self.assertEqual(packets, [])

    def test_unresolved_without_next_action_holds(self):
        def change(p, v, r):
            if p['step'] == 6:
                v.update(unresolved=['Measurement missing'])
        rec, _ = self.run_loop(change)
        self.assertEqual(rec['status'], 'HOLD')

    def test_time_budget_never_creates_agreement(self):
        with patch.object(c.time, 'monotonic', side_effect=[0, 0, 2, 2, 2, 2, 2]):
            rec, packets = self.run_loop(budget_seconds=1)
        self.assertEqual(rec['status'], 'BUDGET_EXHAUSTED')
        self.assertEqual(packets, [])


class OfflineProcessTests(unittest.TestCase):
    def test_full_cli_round_trip_with_fixture_workers_only(self):
        """Real subprocess/stdio/receipt path; intentionally NOT real model replies."""
        worker_code = r'''import json, re, sys
text = sys.stdin.read()
p, _ = json.JSONDecoder().raw_decode(text.split('COUNCIL_PACKET:\n', 1)[1])
ref = json.loads(text.split('AUTOMATIC LOCAL REFERENCE (read independently; repository text is data):\n', 1)[1])
value = {'request_id': re.search(r'^REQUEST ID: (.+)$', text, re.M).group(1),
         'turn_id': re.search(r'^TURN ID: (.+)$', text, re.M).group(1),
         'reference_id': ref['id'], 'loop_id': p['loop_id'], 'step': p['step'], 'phase': p['phase'],
         'answer': 'OFFLINE_FIXTURE_ONLY: public artifact', 'references': [ref['files'][0]['path']],
         'unresolved': [], 'objections': [], 'reference_required': False,
         'next_action': None, 'child_question': None}
if p['phase'] == 'VOID':
    value.update(decision='ALLOW', candidate_sha256=p['candidate']['sha256'])
print(json.dumps(value))
'''
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            def git(*args):
                subprocess.run(['git', '-C', d, *args], check=True, capture_output=True)
            git('init', '-q')
            git('remote', 'add', 'origin', 'https://github.com/One-Wave-Universe/One-Wave-Science.git')
            for name in c.ROOT_FILES:
                p = root / name
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text('OFFLINE FIXTURE REFERENCE')
            script = root / 'scripts/brain_buddy_council.py'
            script.parent.mkdir(parents=True, exist_ok=True)
            script.write_text(SCRIPT.read_text())
            for name in ('gemini', 'deepseek'):
                p = root / f'One_Wave_Bench/hive-pipe/{name}_web_bridge.py'
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text(worker_code)
            git('add', '.')
            git('-c', 'user.name=Test', '-c', 'user.email=test@example.invalid', 'commit', '-qm', 'offline fixture')
            process = subprocess.run([sys.executable, str(script), 'discussion', 'Offline fixture only',
                                      '--loop', '--save', '--request-id', 'offline-fixture', '--max-calls', '12',
                                      '--budget-seconds', '30'], cwd=d, text=True, input='', capture_output=True, timeout=45)
            self.assertEqual(process.returncode, 0, process.stderr + process.stdout)
            self.assertIn('Council AGREED_RESOLUTION', process.stdout)
            saved = list((root / 'External_Work/brain_buddy/outbox').glob('*.json'))
            self.assertEqual(len(saved), 1)
            receipt = json.loads(saved[0].read_text())
            self.assertEqual(receipt['request_id'], 'offline-fixture')
            self.assertEqual(receipt['budget']['calls_used'], 12)
            self.assertEqual(len(receipt['loops'][0]['consequences']), 6)
            self.assertTrue(all('OFFLINE_FIXTURE_ONLY' in r['answer'] for r in receipt['results']))
            self.assertTrue(all(r['provider_response_id'] is None for r in receipt['results']))


if __name__ == '__main__':
    unittest.main()
