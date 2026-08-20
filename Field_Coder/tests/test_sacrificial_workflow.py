"""Step 13 disposable end-to-end Field workflow proof."""

from dataclasses import dataclass, field as dataclass_field
import json
from pathlib import Path
import subprocess
import sys
import tempfile

FIELD_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(FIELD_ROOT))

from field.model_adapter import ModelRequest, ModelResponse
from field.review_packet import PENDING_EXTERNAL_REVIEW
from field.workflow import run_field_workflow


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def run(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=repo, text=True, capture_output=True, check=False)


@dataclass
class SequenceAdapter:
    responses: list[str]
    requests: list[ModelRequest] = dataclass_field(default_factory=list)
    index: int = 0

    def complete(self, model_request: ModelRequest) -> ModelResponse:
        self.requests.append(model_request)
        if self.index >= len(self.responses):
            raise AssertionError("workflow requested more model responses than expected")
        text = self.responses[self.index]
        self.index += 1
        return ModelResponse(text=text, model="sequence-fixture", adapter="sequence-fixture")


def plan(new_value: str) -> str:
    new_content = f'def message():\n    return "{new_value}"\n'
    return json.dumps(
        {
            "intended_change": "set app message to target value",
            "reason": "satisfy the bounded fixture task",
            "files_expected": ["app.py"],
            "invariants": ["only app.py changes"],
            "expected_result": "app.message returns new",
            "success_test": "python3 -c \"import app; assert app.message() == 'new'\"",
            "edit": {"path": "app.py", "new_content": new_content},
        }
    )


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        source = root / "source"
        candidate = root / "candidate"
        source.mkdir()

        (source / ".gitignore").write_text("__pycache__/\n*.pyc\n", encoding="utf-8")
        (source / "app.py").write_text(
            'def message():\n    return "old"\n', encoding="utf-8"
        )
        (source / "test_baseline.py").write_text(
            "import unittest\nimport app\n\n"
            "class Baseline(unittest.TestCase):\n"
            "    def test_not_broken(self):\n"
            "        self.assertIn(app.message(), {'old', 'new'})\n\n"
            "if __name__ == '__main__':\n"
            "    unittest.main()\n",
            encoding="utf-8",
        )

        require(run(source, "git", "init", "-b", "main").returncode == 0, "git init failed")
        run(source, "git", "config", "user.email", "field@example.invalid")
        run(source, "git", "config", "user.name", "Field Fixture")
        require(
            run(source, "git", "add", ".gitignore", "app.py", "test_baseline.py").returncode == 0,
            "git add failed",
        )
        require(run(source, "git", "commit", "-m", "baseline").returncode == 0, "git commit failed")

        baseline_test = run(source, "python3", "-m", "unittest", "-q")
        require(baseline_test.returncode == 0, baseline_test.stderr)
        baseline_head = run(source, "git", "rev-parse", "HEAD").stdout.strip()
        print("PASS: sacrificial repo baseline starts clean and passing")

        adapter = SequenceAdapter([plan("bad"), plan("new")])
        goal = (
            "Change the fixture safely.\n"
            "TASK: set app message to new\n"
            "SCOPE: app.py\n"
            "SUCCESS: app.message returns new; only app.py changes\n"
        )
        result = run_field_workflow(
            source_repo=source,
            candidate_path=candidate,
            candidate_branch="field-candidate",
            goal_text=goal,
            adapter=adapter,
        )

        require(len(result.attempts) == 2, repr(result.attempts))
        require("attempt 1: FAIL; decision=RETRY" in result.attempts[0], repr(result.attempts))
        require("attempt 2: PASS; decision=PASS" in result.attempts[1], repr(result.attempts))
        require(len(adapter.requests) == 2, repr(adapter.requests))
        second_prompt = json.loads(adapter.requests[1].user_prompt)
        require(second_prompt["attempt"] == 2, repr(second_prompt))
        require(second_prompt["last_result"]["passed"] is False, repr(second_prompt))
        print("PASS: bad candidate produced evidence, rollback, and attempt-2 correction context")

        source_head = run(source, "git", "rev-parse", "HEAD").stdout.strip()
        source_status = run(source, "git", "status", "--porcelain=v1", "--untracked-files=all").stdout
        require(source_head == baseline_head, (source_head, baseline_head))
        require(source_status == "", repr(source_status))
        require((source / "app.py").read_text(encoding="utf-8").find('"old"') >= 0, "source was modified")
        print("PASS: source known-good checkout remained unchanged")

        candidate_status = run(candidate, "git", "status", "--porcelain=v1").stdout
        require("app.py" in candidate_status, repr(candidate_status))
        require('"new"' in (candidate / "app.py").read_text(encoding="utf-8"), "successful candidate missing")
        print("PASS: corrected successful candidate remains inspectable")

        packet = result.review_packet
        require(packet is not None, "review packet missing")
        require(packet.files_changed == ("app.py",), repr(packet.files_changed))
        require(packet.test_evidence.passed, repr(packet.test_evidence))
        require(packet.architecture_verdict == PENDING_EXTERNAL_REVIEW, packet.architecture_verdict)
        require(result.final_state.next_action == "review_ready", result.final_state.next_action)
        print("PASS: end-to-end workflow emitted pending-external-review packet")

        run(source, "git", "worktree", "remove", "--force", str(candidate))
        run(source, "git", "branch", "-D", "field-candidate")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
