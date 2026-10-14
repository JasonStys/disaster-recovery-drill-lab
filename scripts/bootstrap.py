"""Install one official hash-pinned native restic binary; no shell installer or archive paths execute. Jason Stys."""
# BEGIN CODE MAP (generated; python scripts/code_map.py)
# variable: ROOT — line 42
# variable: CAP — line 43
# definition: install — line 46
# variable: system — line 48
# variable: entry — line 55
# variable: extension — line 58
# variable: expected — line 59
# variable: output — line 62
# variable: temporary — line 64
# variable: archive — line 65
# variable: hasher — line 66
# variable: size — line 67
# variable: response — line 69
# variable: target — line 70
# variable: data — line 72
# variable: size — line 73
# variable: binary — line 80
# variable: bundle — line 82
# variable: member — line 83
# variable: source — line 90
# variable: content — line 91
# variable: source — line 93
# variable: content — line 94
# definition: main — line 103
# END CODE MAP

from __future__ import annotations

import bz2
import hashlib
import json
import os
import platform
import stat
import tempfile
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CAP = 128 * 1024 * 1024


def install() -> Path:
    """Verify official compressed bytes before bounded binary extraction; only amd64 reviewed platforms are supported."""
    system = platform.system().lower()
    if system not in {
        "windows",
        "linux",
        "darwin",
    } or platform.machine().lower() not in {"amd64", "x86_64"}:
        raise ValueError("reviewed amd64 platform required")
    entry = json.loads((ROOT / "tools.lock.json").read_text(encoding="utf-8"))[
        "restic"
    ][system]
    extension = "zip" if system == "windows" else "bz2"
    expected = f"https://github.com/restic/restic/releases/download/v0.19.1/restic_0.19.1_{system}_amd64.{extension}"
    if entry["url"] != expected:
        raise ValueError("official tool source required")
    output = ROOT / ".tools"
    output.mkdir(mode=0o700, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=output) as temporary:
        archive = Path(temporary) / "download"
        hasher = hashlib.sha256()
        size = 0
        with (
            urllib.request.urlopen(expected, timeout=30) as response,
            archive.open("wb") as target,
        ):
            while data := response.read(1024 * 1024):
                size += len(data)
                if size > CAP:
                    raise ValueError("archive exceeds cap")
                hasher.update(data)
                target.write(data)
        if hasher.hexdigest() != entry["sha256"]:
            raise ValueError("tool checksum failed; no binary executed")
        binary = Path(temporary) / entry["binary"]
        if system == "windows":
            with zipfile.ZipFile(archive) as bundle:
                member = bundle.getinfo(entry["member"])
                if (
                    member.file_size > CAP
                    or member.is_dir()
                    or stat.S_ISLNK(member.external_attr >> 16)
                ):
                    raise ValueError("bounded regular binary required")
                with bundle.open(member) as source:
                    content = source.read(CAP + 1)
        else:
            with bz2.open(archive, "rb") as source:
                content = source.read(CAP + 1)
        if len(content) > CAP:
            raise ValueError("binary exceeds cap")
        binary.write_bytes(content)
        os.chmod(binary, 0o700)
        os.replace(binary, output / entry["binary"])
    return output / entry["binary"]


def main() -> int:
    """Install only the explicit official tool; no passwords, backups or unrelated host settings are touched."""
    print(install())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
