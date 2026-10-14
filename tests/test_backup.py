"""Real native restic encryption and negative oracles plus exclusive workspace guards. Jason Stys."""
# BEGIN CODE MAP (generated; python scripts/code_map.py)
# definition: test_real_restic — line 38
# parameter: tmp_path — line 38
# variable: report — line 41
# variable: check — line 45
# definition: test_workspace_guards — line 53
# parameter: tmp_path — line 53
# variable: valid — line 56
# variable: path — line 58
# definition: test_run_contracts — line 73
# parameter: tmp_path — line 73
# variable: backup — line 75
# variable: invoked — line 88
# variable: arguments — line 91
# definition: test_generic_errors_never_pass — line 101
# parameter: method — line 101
# parameter: tmp_path — line 101
# variable: backup — line 103
# definition: test_backup_and_restore_failures — line 118
# parameter: tmp_path — line 118
# variable: backup — line 120
# variable: source — line 121
# END CODE MAP

from __future__ import annotations

import os
import subprocess
from pathlib import Path
from unittest.mock import patch

import pytest

from dr.backup import Restic, native_drill, private_file, sha256, workspace


def test_real_restic(tmp_path: Path) -> None:
    """Execute the hash-installed native restic tool on synthetic data only; fake revision is explicitly test metadata."""
    with patch("dr.backup.revision", return_value="1" * 40):
        report = native_drill(tmp_path)
    assert len(report["checks"]) == 5
    assert report["recovery"] is None
    assert report["engine"] == "native"
    assert all(check["result"] == "PASS" for check in report["checks"])
    assert sha256(tmp_path / "restored/synthetic.txt") == report["dump_sha256"]
    if os.name != "nt":
        assert (tmp_path / "repository.password").stat().st_mode & 0o777 == 0o600
    with pytest.raises(FileExistsError):
        private_file(tmp_path / "repository.password", b"do-not-overwrite")


def test_workspace_guards(tmp_path: Path) -> None:
    """Reject outside/traversal/existing/invalid named outputs; tests patch the repo root instead of touching real files."""
    with patch("dr.backup.ROOT", tmp_path):
        valid = workspace(tmp_path / "out/test")
        assert valid.is_dir()
        for path in (
            tmp_path / "outside",
            tmp_path / "out/../escape",
            valid,
            tmp_path / "out/UPPER",
        ):
            with pytest.raises((ValueError, FileExistsError)):
                workspace(path)
        with (
            patch("pathlib.Path.is_symlink", return_value=True),
            pytest.raises(ValueError),
        ):
            workspace(tmp_path / "out/link-escape")


def test_run_contracts(tmp_path: Path) -> None:
    """Explicit repository/password files override inherited restic environment; no shell or ambient backend commands."""
    backup = Restic(tmp_path)
    with pytest.raises(ValueError):
        backup.run("snapshots", repo=tmp_path.parent / "outside")
    with (
        patch.dict(
            os.environ,
            {
                "RESTIC_PASSWORD_COMMAND": "DO_NOT_RUN",
                "RESTIC_REPOSITORY": "https://do-not-contact",
            },
        ),
        patch(
            "subprocess.run", return_value=subprocess.CompletedProcess([], 0, "", "")
        ) as invoked,
    ):
        backup.success("snapshots")
        arguments = invoked.call_args.kwargs
        assert "RESTIC_PASSWORD_COMMAND" not in arguments["env"]
        assert "RESTIC_REPOSITORY" not in arguments["env"]
        assert arguments.get("shell", False) is False
        assert "--no-cache" in invoked.call_args.args[0]


@pytest.mark.parametrize(
    "method", ["reject_password", "reject_missing", "reject_corruption"]
)
def test_generic_errors_never_pass(tmp_path: Path, method: str) -> None:
    """Generic failures cannot prove password, missing-snapshot or data-integrity enforcement."""
    backup = Restic(tmp_path)
    if method == "reject_corruption":
        (backup.repo / "data").mkdir(parents=True)
        private_file(backup.repo / "data/pack", b"owned synthetic data")
    with (
        patch.object(
            backup,
            "run",
            return_value=subprocess.CompletedProcess([], 1, "", "unrelated failure"),
        ),
        pytest.raises(ValueError),
    ):
        getattr(backup, method)()


def test_backup_and_restore_failures(tmp_path: Path) -> None:
    """Outside sources, malformed snapshot inventories and wrong restore names reject before useful output."""
    backup = Restic(tmp_path)
    source = tmp_path / "payload"
    private_file(source, b"synthetic")
    with pytest.raises(ValueError):
        backup.backup(tmp_path.parent / "outside")
    with patch.object(backup, "success", return_value="[]"), pytest.raises(ValueError):
        backup.backup(source)
    with pytest.raises(ValueError):
        backup.restore("a" * 64, "outside")
    with patch.object(backup, "success", return_value=""), pytest.raises(ValueError):
        backup.restore("a" * 64, "restored")
    with (
        patch.object(
            backup,
            "run",
            return_value=subprocess.CompletedProcess([], 1, "", "private failure"),
        ),
        pytest.raises(ValueError),
    ):
        backup.success("check")
