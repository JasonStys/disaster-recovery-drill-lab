"""Objective-aware recovery-point selection and nondeleting retention review. Created by Jason Stys."""
# BEGIN CODE MAP (generated; python scripts/code_map.py)
# definition: plan — line 60
# parameter: raw — line 60
# variable: data — line 63
# variable: clock — line 75
# variable: minimum — line 76
# variable: source — line 77
# variable: points — line 82
# variable: seen — line 83
# variable: raw_point — line 84
# variable: row — line 85
# variable: identifier — line 97
# variable: created — line 101
# variable: snapshot — line 107
# variable: potential — line 111
# variable: measured — line 116
# variable: groups — line 141
# variable: provenance — line 142
# variable: members — line 143
# variable: point — line 143
# variable: eligible — line 146
# variable: point — line 147
# parameter: point — line 148
# variable: point — line 158
# variable: selected — line 162
# variable: group — line 164
# variable: newest — line 167
# variable: provenance — line 169
# variable: point — line 170
# variable: item — line 171
# parameter: point — line 172
# variable: point — line 175
# variable: reasons — line 176
# parameter: point — line 205
# definition: publish — line 212
# parameter: output — line 212
# parameter: result — line 212
# variable: absolute — line 214
# variable: path — line 217
# variable: text — line 220
# variable: rows — line 221
# variable: key — line 225
# variable: point — line 235
# variable: page — line 237
# END CODE MAP

from __future__ import annotations

import hashlib
import html
import json
from pathlib import Path
from typing import Any

from dr.contracts import bounded, fingerprint, integer, record
from dr.ledger import dataset, evaluate


def plan(raw: Any) -> dict[str, Any]:
    """Compare <=20 points against one captured source head; unknown restore time never qualifies."""
    bounded(raw)
    data = record(
        raw,
        {
            "schema",
            "as_of_ms",
            "source_head",
            "objectives",
            "retention_minimum",
            "points",
        },
    )
    integer(data["schema"], 1, 1)
    clock = integer(data["as_of_ms"], 1)
    minimum = integer(data["retention_minimum"], 1, 20)
    source = dataset(data["source_head"])
    if source["latest_commit_ms"] > clock:
        raise ValueError("source head is after review clock")
    if not isinstance(data["points"], list) or not 1 <= len(data["points"]) <= 20:
        raise ValueError("catalog needs1..20 recovery points")
    points = []
    seen = set()
    for raw_point in data["points"]:
        row = record(
            raw_point,
            {
                "id",
                "created_at_ms",
                "provenance",
                "snapshot",
                "restored",
                "elapsed_ms",
                "legal_hold",
            },
        )
        identifier = fingerprint(row["id"])
        if identifier in seen:
            raise ValueError("duplicate recovery point")
        seen.add(identifier)
        created = integer(row["created_at_ms"], 1, clock)
        if (
            row["provenance"] not in ("supplied_synthetic", "measured_lab")
            or type(row["legal_hold"]) is not bool
        ):
            raise ValueError("explicit provenance and hold required")
        snapshot = dataset(row["snapshot"])
        if snapshot["latest_commit_ms"] > created:
            raise ValueError("snapshot includes transactions after creation")
        # This also independently checks append-only source scope, even for an untested point.
        potential = evaluate(
            row["snapshot"], data["source_head"], row["snapshot"], 0, data["objectives"]
        )
        if (row["restored"] is None) != (row["elapsed_ms"] is None):
            raise ValueError("restore data/time must both be known or absent")
        measured = (
            None
            if row["restored"] is None
            else evaluate(
                row["snapshot"],
                data["source_head"],
                row["restored"],
                row["elapsed_ms"],
                data["objectives"],
            )
        )
        points.append(
            {
                "id": identifier,
                "created_at_ms": created,
                "provenance": row["provenance"],
                "legal_hold": row["legal_hold"],
                "snapshot_fingerprint": snapshot["fingerprint"],
                "evaluation": measured,
                "eligible": measured is not None and measured["result"] == "PASS",
                "potential_rpo_ms_if_exact_restore": potential["observed_rpo_ms"],
                "potential_lost_orders_if_exact_restore": potential["lost_orders"],
            }
        )
    # Synthetic input and actual lab measurements are deliberately never ranked against one another.
    groups = []
    for provenance in ("measured_lab", "supplied_synthetic"):
        members = [point for point in points if point["provenance"] == provenance]
        if not members:
            continue
        eligible = sorted(
            (point for point in members if point["eligible"]),
            key=lambda point: (
                point["evaluation"]["observed_rpo_ms"],
                point["evaluation"]["lost_orders"],
                point["evaluation"]["observed_rto_ms"],
                point["id"],
            ),
        )
        groups.append(
            {
                "provenance": provenance,
                "eligible_points": [point["id"] for point in eligible],
                "recommended_point": eligible[0]["id"] if eligible else None,
            }
        )
    selected = {
        group["recommended_point"]
        for group in groups
        if group["recommended_point"] is not None
    }
    newest = {
        point["id"]
        for provenance in ("measured_lab", "supplied_synthetic")
        for point in sorted(
            (item for item in points if item["provenance"] == provenance),
            key=lambda point: (-point["created_at_ms"], point["id"]),
        )[:minimum]
    }
    for point in points:
        reasons = []
        if point["legal_hold"]:
            reasons.append("legal_hold")
        if point["id"] in newest:
            reasons.append("newest_minimum")
        if point["id"] in selected:
            reasons.append("selected_recovery_point")
        if point["evaluation"] is None:
            reasons.append("untested_restore_requires_drill")
        elif not point["evaluation"]["snapshot_matches"]:
            reasons.append("restore_mismatch_requires_investigation")
        point["retention_review"] = (
            "KEEP_REVIEW" if reasons else "MANUAL_RETIREMENT_REVIEW"
        )
        point["retention_reasons"] = reasons or [
            "not_selected_or_protected; verify independent backup coverage and obligations before any deletion"
        ]
    return {
        "schema": 1,
        "kind": "recovery_point_review",
        "author": "Jason Stys",
        "as_of_ms": clock,
        "catalog_sha256": hashlib.sha256(
            json.dumps(data, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest(),
        "source_head_fingerprint": source["fingerprint"],
        "objectives": data["objectives"],
        "groups": groups,
        "points": sorted(
            points, key=lambda point: (-point["created_at_ms"], point["id"])
        ),
        "has_eligible_point": bool(selected),
        "scope": "Captured append-only fictional ledgers; supplied timing/provenance are assertions,not backup authenticity. RTO excludes human detection/cutover. No restore,forget,prune or deletion is executed. This is not PITR or a zero-loss guarantee.",
    }


def publish(result: dict[str, Any], output: Path) -> None:
    """Publish only aggregate objective/retention review, no raw ledgers, passwords or deletion commands."""
    absolute = output.absolute()
    if any(
        path.is_symlink() or path.is_junction()
        for path in (absolute, *absolute.parents)
    ):
        raise ValueError("linked output refused")
    text = json.dumps(result, sort_keys=True, indent=2)
    rows = "".join(
        "<tr>"
        + "".join(
            f"<td>{html.escape(str(point[key]))}</td>"
            for key in (
                "id",
                "provenance",
                "eligible",
                "potential_rpo_ms_if_exact_restore",
                "retention_review",
                "retention_reasons",
            )
        )
        + "</tr>"
        for point in result["points"]
    )
    page = (
        '<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="Content-Security-Policy" content="default-src \'none\'; base-uri \'none\'; form-action \'none\'"><title>Recovery point review — Jason Stys</title><main><h1>Recovery-point and retention review</h1><p>Created by Jason Stys. Review only; no restore or pruning is executed.</p><table><caption>Eligibility is based on captured restore evidence; untested points remain unknown</caption><tr><th>Point</th><th>Provenance</th><th>Eligible</th><th>Potential RPO ms</th><th>Retention</th><th>Reasons</th></tr>'
        + rows
        + "</table><details><summary>Full objectives, observed results and separate provenance selections</summary><pre>"
        + html.escape(text)
        + "</pre></details></main></html>"
    )
    absolute.mkdir(mode=0o700)
    (absolute / "recovery-review.json").write_text(text + "\n", encoding="utf-8")
    (absolute / "recovery-review.html").write_text(page, encoding="utf-8")
