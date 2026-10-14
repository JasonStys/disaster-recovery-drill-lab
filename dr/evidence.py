"""Closed synthetic measured recovery reports with escaped, network-inert HTML. Jason Stys."""
# BEGIN CODE MAP (generated; python scripts/code_map.py)
# variable: CASES — line 37
# definition: validate — line 62
# parameter: raw — line 62
# variable: report — line 64
# variable: c — line 90
# variable: checks — line 96
# variable: names — line 99
# variable: raw_check — line 100
# variable: check — line 101
# variable: proof — line 110
# variable: key — line 113
# variable: value — line 113
# variable: c — line 127
# variable: result — line 138
# variable: key — line 156
# definition: publish — line 178
# parameter: output — line 178
# parameter: raw — line 178
# variable: report — line 180
# variable: body — line 181
# variable: rows — line 182
# variable: check — line 184
# variable: document — line 186
# END CODE MAP

from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any

from dr.contracts import bounded, fingerprint, integer, record

CASES = {
    "native": {
        "encrypted_backup",
        "wrong_password",
        "missing_snapshot",
        "corrupt_pack",
        "exact_restore",
    },
    "postgres": {
        "isolation",
        "consistent_dump",
        "encrypted_backup",
        "wrong_password",
        "corrupt_pack",
        "source_loss",
        "isolated_restore",
        "constraints",
        "repeat_restore",
        "objectives",
        "strict_objective_rejection",
        "owned_cleanup",
    },
}


def validate(raw: Any) -> dict[str, Any]:
    """Require a complete distinct PASS suite and closed bounded aggregate fields; collector authenticity is not inferred."""
    report = record(
        raw,
        {
            "schema",
            "author",
            "synthetic",
            "engine",
            "source_sha",
            "snapshot_id",
            "dump_sha256",
            "checks",
            "recovery",
        },
    )
    if (
        type(report["schema"]) is not int
        or report["schema"] != 1
        or report["author"] != "Jason Stys"
        or report["synthetic"] is not True
        or not isinstance(report["engine"], str)
        or report["engine"] not in CASES
    ):
        raise ValueError("report identity invalid")
    if (
        not isinstance(report["source_sha"], str)
        or len(report["source_sha"]) != 40
        or any(c not in "0123456789abcdef" for c in report["source_sha"])
        or report["source_sha"] == "0" * 40
    ):
        raise ValueError("full source revision required")
    fingerprint(report["snapshot_id"])
    fingerprint(report["dump_sha256"])
    checks = report["checks"]
    if not isinstance(checks, list) or len(checks) != len(CASES[report["engine"]]):
        raise ValueError("complete suite required")
    names: set[str] = set()
    for raw_check in checks:
        check = record(raw_check, {"name", "result", "duration_ms", "evidence"})
        if (
            not isinstance(check["name"], str)
            or check["name"] not in CASES[report["engine"]]
            or check["name"] in names
            or check["result"] != "PASS"
        ):
            raise ValueError("failed, duplicate or unknown case")
        integer(check["duration_ms"], 0, 1_800_000)
        proof = check["evidence"]
        if not isinstance(proof, dict) or not 1 <= len(proof) <= 12:
            raise ValueError("bounded aggregate required")
        for key, value in proof.items():
            if (
                not isinstance(key, str)
                or not key.isascii()
                or not key.replace("_", "").isalnum()
                or len(key) > 64
            ):
                raise ValueError("proof field invalid")
            if (
                type(value) not in (int, bool, str)
                or isinstance(value, str)
                and (
                    len(value) > 128
                    or not value.isascii()
                    or any(ord(c) < 32 or ord(c) > 126 for c in value)
                )
            ):
                raise ValueError("proof value invalid")
            if type(value) is int:
                integer(value, 0)
        names.add(check["name"])
    if report["engine"] == "native":
        if report["recovery"] is not None:
            raise ValueError("native drill does not prove PostgreSQL RTO/RPO")
    else:
        result = record(
            report["recovery"],
            {
                "result",
                "snapshot_matches",
                "recovered_orders",
                "lost_orders",
                "observed_rpo_ms",
                "observed_rto_ms",
                "rto_limit_ms",
                "rpo_limit_ms",
                "lost_order_limit",
                "recovered_fingerprint",
            },
        )
        if result["result"] != "PASS" or result["snapshot_matches"] is not True:
            raise ValueError("recovery must match snapshot")
        fingerprint(result["recovered_fingerprint"])
        for key in (
            "recovered_orders",
            "lost_orders",
            "observed_rpo_ms",
            "observed_rto_ms",
            "rto_limit_ms",
            "rpo_limit_ms",
            "lost_order_limit",
        ):
            integer(result[key], 0)
        if (
            result["recovered_orders"] == 0
            or result["rto_limit_ms"] == 0
            or result["observed_rto_ms"] > result["rto_limit_ms"]
            or result["observed_rpo_ms"] > result["rpo_limit_ms"]
            or result["lost_orders"] > result["lost_order_limit"]
        ):
            raise ValueError("objective not met")
    bounded(report)
    return report


def publish(raw: Any, output: Path) -> None:
    """Write only validated aggregate JSON and escaped offline HTML in a NEW directory; never overwrite or embed secrets."""
    report = validate(raw)
    body = json.dumps(report, sort_keys=True, indent=2, allow_nan=False)
    rows = "".join(
        f"<tr><td>{html.escape(check['name'])}</td><td>PASS</td><td>{check['duration_ms']}</td></tr>"
        for check in report["checks"]
    )
    document = (
        '<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="Content-Security-Policy" content="default-src \'none\'; base-uri \'none\'; form-action \'none\'; object-src \'none\'"><title>Recovery Drill — Jason Stys</title><h1>Disaster Recovery Drill Lab</h1><p>Created by Jason Stys · github.com/JasonStys · LinkedIn: jason-stys-31b30b351</p><p>Measured synthetic lab. Not a production backup, zero-data-loss guarantee or certification.</p><table><caption>Observed checks; duration in milliseconds</caption><tr><th>Case</th><th>Result</th><th>Duration</th></tr>'
        + rows
        + "</table><h2>Measured aggregate</h2><pre>"
        + html.escape(body)
        + "</pre><p>Help: README and docs/runbook.md. No passwords, raw customer records or private paths are embedded.</p></html>"
    )
    output.mkdir(parents=True, mode=0o700, exist_ok=False)
    (output / "drill.json").write_text(body + "\n", encoding="utf-8", newline="\n")
    (output / "drill.html").write_text(document, encoding="utf-8", newline="\n")
