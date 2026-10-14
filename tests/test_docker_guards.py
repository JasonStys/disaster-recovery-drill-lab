"""Native ownership/isolation regressions use fabricated inspect fixtures; no local Docker call occurs. Jason Stys."""
# BEGIN CODE MAP (generated; python scripts/code_map.py)
# definition: owned — line 29
# definition: test_ownership_and_isolation — line 59
# variable: value — line 61
# variable: change — line 63
# variable: changed — line 73
# definition: test_nonlinux_refusal — line 96
# parameter: tmp_path — line 96
# definition: test_resource_identity_guards — line 114
# parameter: bad — line 114
# parameter: field — line 114
# parameter: section — line 114
# variable: value — line 116
# END CODE MAP

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any
from unittest.mock import patch

import pytest

from scripts.postgres_drill import Postgres, inspect_guard


def owned() -> list[dict[str, Any]]:
    """Construct a fake exact-owned container solely for safety predicate tests."""
    return [
        {
            "Name": "/dr-lab-123-source",
            "Config": {
                "Labels": {"recovery.lab.run": "123"},
                "Image": "pinned",
                "User": "postgres",
            },
            "HostConfig": {
                "NetworkMode": "none",
                "Privileged": False,
                "ReadonlyRootfs": True,
                "PortBindings": {},
                "CapDrop": ["ALL"],
                "SecurityOpt": ["no-new-privileges=true"],
                "Memory": 402653184,
                "NanoCpus": 1000000000,
                "PidsLimit": 128,
                "Tmpfs": {
                    "/var/lib/postgresql": "bounded",
                    "/var/run/postgresql": "bounded",
                },
            },
            "Mounts": [],
        }
    ]


def test_ownership_and_isolation() -> None:
    """Wrong owner/name/image/network/root/mount/port settings must fail before destructive operations."""
    value = owned()
    inspect_guard(value, "dr-lab-123-source", "123", "pinned")
    for change in (
        "owner",
        "name",
        "image",
        "network",
        "root",
        "privileged",
        "ports",
        "mount",
    ):
        changed = deepcopy(value)
        if change == "owner":
            changed[0]["Config"]["Labels"]["recovery.lab.run"] = "other"
        elif change == "name":
            changed[0]["Name"] = "/unrelated"
        elif change == "image":
            changed[0]["Config"]["Image"] = "wrong"
        elif change == "network":
            changed[0]["HostConfig"]["NetworkMode"] = "host"
        elif change == "root":
            changed[0]["HostConfig"]["ReadonlyRootfs"] = False
        elif change == "privileged":
            changed[0]["HostConfig"]["Privileged"] = True
        elif change == "ports":
            changed[0]["HostConfig"]["PortBindings"] = {"5432/tcp": []}
        else:
            changed[0]["Mounts"] = [{"Type": "bind"}]
        with pytest.raises(ValueError):
            inspect_guard(changed, "dr-lab-123-source", "123", "pinned")
    with pytest.raises(ValueError):
        inspect_guard([], "dr-lab-123-source", "123", "pinned")


def test_nonlinux_refusal(tmp_path: Path) -> None:
    """Windows/macOS cannot start or repair Docker as a side effect of native tests."""
    with patch("platform.system", return_value="Windows"), pytest.raises(ValueError):
        Postgres(tmp_path)


@pytest.mark.parametrize(
    "section,field,bad",
    [
        ("Config", "User", "root"),
        ("HostConfig", "CapDrop", []),
        ("HostConfig", "SecurityOpt", ["no-new-privileges=false"]),
        ("HostConfig", "Memory", 0),
        ("HostConfig", "NanoCpus", 0),
        ("HostConfig", "PidsLimit", 0),
        ("HostConfig", "Tmpfs", {}),
    ],
)
def test_resource_identity_guards(section: str, field: str, bad: object) -> None:
    """Non-root identity, dropped capabilities and actual finite tmpfs/resource limits must be observed."""
    value = owned()
    value[0][section][field] = bad
    with pytest.raises(ValueError):
        inspect_guard(value, "dr-lab-123-source", "123", "pinned")
