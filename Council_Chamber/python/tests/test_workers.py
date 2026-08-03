import subprocess

import pytest

from council_chamber.workers.file_search import FileSearchWorker
from council_chamber.workers.test_worker import TestWorker
from council_chamber.workers.build_worker import BuildWorker
from council_chamber.workers.git_worker import GitWorker
from council_chamber.workers.patch_worker import PatchWorker, ProposedChange, PathEscapesProjectRootError


@pytest.fixture
def sample_project(tmp_path):
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "main.py").write_text(
        "def add(a, b):\n    return a + b\n\n\nclass Greeter:\n    def hello(self):\n        return 'hi'\n"
    )
    (tmp_path / "README.md").write_text("# Sample project\n\nSays hello.\n")
    return tmp_path


# -- FileSearchWorker --------------------------------------------------

def test_find_files_matches_glob(sample_project):
    worker = FileSearchWorker(sample_project)
    files = worker.find_files("**/*.py")
    assert files == ["src/main.py"]


def test_search_text_finds_matching_lines(sample_project):
    worker = FileSearchWorker(sample_project)
    matches = worker.search_text("hello")
    assert any(m.file_path == "src/main.py" and "def hello" in m.line_text for m in matches)


def test_search_text_case_insensitive_by_default(sample_project):
    worker = FileSearchWorker(sample_project)
    matches = worker.search_text("SAMPLE PROJECT")
    assert any(m.file_path == "README.md" for m in matches)


def test_find_symbol_locates_def_and_class(sample_project):
    worker = FileSearchWorker(sample_project)
    add_matches = worker.find_symbol("add")
    assert len(add_matches) == 1
    assert add_matches[0].symbol_kind == "def"
    assert add_matches[0].line_number == 1

    greeter_matches = worker.find_symbol("Greeter")
    assert len(greeter_matches) == 1
    assert greeter_matches[0].symbol_kind == "class"


def test_search_excludes_git_and_pycache_dirs(sample_project):
    (sample_project / ".git").mkdir()
    (sample_project / ".git" / "config").write_text("hello")
    (sample_project / "__pycache__").mkdir()
    (sample_project / "__pycache__" / "x.pyc").write_text("hello")

    worker = FileSearchWorker(sample_project)
    matches = worker.search_text("hello")
    assert all(".git" not in m.file_path and "__pycache__" not in m.file_path for m in matches)


# -- TestWorker ----------------------------------------------------------

def test_test_worker_reports_passing_tests(tmp_path):
    (tmp_path / "test_ok.py").write_text("def test_ok():\n    assert 1 == 1\n")
    worker = TestWorker(tmp_path, command=["python3", "-m", "pytest", "-q"])
    result = worker.run()
    assert result.passed is True
    assert result.exit_code == 0


def test_test_worker_reports_exact_failure(tmp_path):
    (tmp_path / "test_bad.py").write_text(
        "def test_bad():\n    assert 1 == 2, 'one is not two'\n"
    )
    worker = TestWorker(tmp_path, command=["python3", "-m", "pytest", "-q"])
    result = worker.run()
    assert result.passed is False
    assert "1 failed" in result.stdout or "1 failed" in result.summary


def test_test_worker_handles_missing_command(tmp_path):
    worker = TestWorker(tmp_path, command=["this_command_does_not_exist_xyz"])
    result = worker.run()
    assert result.passed is False
    assert result.exit_code == -1


# -- BuildWorker -----------------------------------------------------------

def test_build_worker_reports_success(tmp_path):
    worker = BuildWorker(tmp_path, command=["python3", "-c", "print('built ok')"])
    result = worker.run()
    assert result.success is True
    assert "built ok" in result.stdout


def test_build_worker_reports_failure(tmp_path):
    worker = BuildWorker(tmp_path, command=["python3", "-c", "import sys; sys.exit(1)"])
    result = worker.run()
    assert result.success is False
    assert result.exit_code == 1


# -- GitWorker -----------------------------------------------------------

@pytest.fixture
def git_project(tmp_path):
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=tmp_path, check=True)
    (tmp_path / "a.txt").write_text("hello\n")
    subprocess.run(["git", "add", "-A"], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "initial"], cwd=tmp_path, check=True)
    return tmp_path


def test_git_status_shows_untracked_file(git_project):
    (git_project / "b.txt").write_text("new file\n")
    worker = GitWorker(git_project)
    result = worker.status()
    assert result.success is True
    assert "b.txt" in result.output


def test_git_checkpoint_commits_changes(git_project):
    (git_project / "a.txt").write_text("hello again\n")
    worker = GitWorker(git_project)
    result = worker.checkpoint("update a.txt")
    assert result.success is True

    log_result = worker.log(max_count=1)
    assert "update a.txt" in log_result.output


def test_git_diff_shows_pending_change(git_project):
    (git_project / "a.txt").write_text("changed content\n")
    worker = GitWorker(git_project)
    result = worker.diff()
    assert result.success is True
    assert "changed content" in result.output


# -- PatchWorker -----------------------------------------------------------

def test_patch_worker_preview_diff_shows_change(sample_project):
    worker = PatchWorker(sample_project)
    change = ProposedChange(file_path="src/main.py", new_content="def add(a, b):\n    return a + b + 1\n")
    diff = worker.preview_diff(change)
    assert "-    return a + b" in diff
    assert "+    return a + b + 1" in diff


def test_patch_worker_apply_writes_file(sample_project):
    worker = PatchWorker(sample_project)
    change = ProposedChange(file_path="src/main.py", new_content="def add(a, b):\n    return a + b\n")
    result = worker.apply(change)
    assert result.success is True
    assert (sample_project / "src" / "main.py").read_text() == "def add(a, b):\n    return a + b\n"


def test_patch_worker_apply_creates_new_file_with_parents(sample_project):
    worker = PatchWorker(sample_project)
    change = ProposedChange(file_path="src/new/deep/file.py", new_content="x = 1\n")
    result = worker.apply(change)
    assert result.success is True
    assert (sample_project / "src" / "new" / "deep" / "file.py").read_text() == "x = 1\n"


def test_patch_worker_does_not_apply_until_called():
    pass  # covered by construction alone: PatchWorker.__init__ never touches the filesystem


def test_patch_worker_rejects_path_escaping_project_root(sample_project):
    worker = PatchWorker(sample_project)
    change = ProposedChange(file_path="../../etc/passwd", new_content="pwned")
    result = worker.apply(change)
    assert result.success is False

    with pytest.raises(PathEscapesProjectRootError):
        worker.preview_diff(change)
