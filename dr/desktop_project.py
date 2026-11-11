"""Review actual captured-ledger recovery objectives and conservative point retention offline. Jason Stys."""
# BEGIN CODE MAP (generated; python scripts/code_map.py)
# variable: ROOT — line 96
# variable: PRODUCT — line 97
# variable: PROFILE — line 97
# variable: TITLE — line 98
# variable: VERSION — line 98
# variable: BANNER — line 99
# variable: COLUMNS — line 100
# variable: RESOURCES — line 106
# variable: RESOURCE_LIMITS — line 112
# variable: MODES — line 113
# variable: REVIEW_MODE — line 118
# variable: CHOICES — line 119
# variable: FIELDS — line 131
# variable: ACTIVE_FIELDS — line 140
# variable: SCENARIOS — line 159
# variable: HELP — line 169
# variable: BASE — line 173
# definition: scenario — line 176
# parameter: name — line 176
# variable: _kind — line 182
# variable: _label — line 182
# variable: name — line 182
# definition: ledger — line 187
# parameter: count — line 187
# variable: n — line 191
# variable: n — line 192
# variable: n — line 193
# definition: prepared — line 197
# parameter: name — line 197
# variable: data — line 202
# variable: points — line 210
# variable: char — line 220
# variable: count — line 220
# variable: elapsed — line 220
# variable: row — line 228
# definition: control — line 245
# parameter: lower — line 245
# parameter: text — line 245
# parameter: upper — line 245
# definition: analyze — line 252
# parameter: parameters — line 253
# parameter: stage — line 253
# parameter: state — line 253
# variable: mode — line 256
# variable: catalog — line 260
# variable: data — line 260
# variable: raw — line 261
# variable: raw — line 263
# variable: catalog — line 264
# variable: data — line 264
# variable: original — line 265
# variable: original_result — line 270
# variable: high — line 271
# variable: low — line 271
# variable: name — line 271
# variable: high — line 278
# variable: low — line 278
# variable: name — line 278
# variable: result — line 283
# variable: scope — line 284
# variable: g — line 307
# definition: views — line 323
# parameter: files — line 323
# variable: scope — line 325
# variable: r — line 327
# variable: rows — line 328
# variable: a — line 344
# variable: b — line 344
# variable: label — line 344
# variable: r — line 356
# variable: p — line 358
# variable: g — line 360
# variable: p — line 363
# definition: cells — line 369
# parameter: row — line 369
# variable: r — line 379
# END CODE MAP

from __future__ import annotations

import copy
import hashlib
import sys
from pathlib import Path
from typing import Any

from .contracts import CAP, decode, integer, record
from .desktop_io import Rejected, canonical, json_value
from .desktop_state import Workspace
from .inputs import read_source
from .ledger import evaluate
from .planning import plan

ROOT = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parents[1]))
PRODUCT, PROFILE = "disaster-recovery-drill-lab", "DisasterRecoveryDrillLab"
TITLE, VERSION = "Disaster Recovery Review Workbench", "1.1.0"
BANNER = "Captured evidence review only: no backup, restore, deletion, Docker or live database access."
COLUMNS = (
    "Recovery point / objective",
    "Observed / original",
    "Budget / current",
    "Decision / scope",
)
RESOURCES = (
    "examples/objective-evaluation.json",
    "notices.txt",
    "app.ico",
    "python314.dll",
)
RESOURCE_LIMITS: dict[str, int] = {}
MODES = (
    "Evaluate authorized captured restore",
    "Review authorized recovery-point catalog",
    "Review prepared full-app scenario",
)
REVIEW_MODE = None
CHOICES = {
    "exercise": (
        "captured-pass",
        "zero-loss-fails",
        "rto-fails",
        "restore-mismatch",
        "point-tradeoffs",
        "all-untested",
        "legal-hold",
        "separate-provenance",
    )
}
FIELDS = (
    ("document", "Authorized evaluation / recovery catalog JSON", "file"),
    ("rto_ms", "Optional RTO limit, 1–1800000 milliseconds", "text"),
    ("rpo_ms", "Optional RPO limit, 0–1800000 milliseconds", "text"),
    ("max_lost_orders", "Optional maximum lost orders, 0–10000", "text"),
    ("as_of_ms", "Catalog only: optional as-of UTC epoch milliseconds", "text"),
    ("retention_minimum", "Catalog only: optional minimum newest points, 1–20", "text"),
    ("exercise", "Prepared full-app scenario", "choice"),
)
ACTIVE_FIELDS = {
    MODES[0]: ("document", "rto_ms", "rpo_ms", "max_lost_orders"),
    MODES[1]: (
        "document",
        "rto_ms",
        "rpo_ms",
        "max_lost_orders",
        "as_of_ms",
        "retention_minimum",
    ),
    MODES[2]: (
        "exercise",
        "rto_ms",
        "rpo_ms",
        "max_lost_orders",
        "as_of_ms",
        "retention_minimum",
    ),
}
SCENARIOS = (
    "Captured exact restore with explicit one-order loss",
    "Stricter zero-loss budget correctly fails",
    "Slow captured restore exceeds its RTO",
    "Valid different ledger is not the exact snapshot",
    "Middle recovery point beats newest slow restore",
    "Untested recovery points stay unknown",
    "Legal hold and mismatched restore remain protected",
    "Measured-label and synthetic groups stay separate",
)
HELP = """Evaluate authorized captured fictional-schema ledgers or compare a recovery-point catalog with the original recovery engine. It checks real relational/payment consistency, exact snapshot recovery, append-only source history, original business commit timestamps, elapsed recovery time and explicitly lost orders. The GUI does not run SQL, import executable dumps, connect to a database or contact a backup service.
Select an actual supported JSON file. Optional limits change the evaluation policy, never the captured elapsed time or ledgers. Original data/policy are validated before changes; both original and effective hashes, limits and results remain in evidence. A supplied measured_lab label is an assertion, not authenticated acquisition. Catalog timing and restored data must both be supplied or both absent; untested points cannot qualify. Synthetic and measured-label groups are never ranked against one another. Retention recommendations are conservative human review, never forget/prune/delete operations.
Prepared examples populate normal editable controls. Check RTO/RPO/lost-order rows and exact-match decision, inspect individual points and retention reasons, search/filter without changing denominators, and export exact aggregate evidence to a new file. Raw customer/order/payment rows are not saved in the aggregate. Preserve original inputs yourself. Existing original restic encryption and isolated PostgreSQL drills remain separate CLI/hosted tools; green offline review is not proof they ran.
Profiles and selected paths are sensitive owner-local plaintext, not encryption or multiuser login. Exit waits for the worker and durable commit before releasing ownership. Help/licenses work offline."""
BASE = 1791500000000


def scenario(name: str) -> dict[str, str]:
    """Populate ordinary editable review controls without changing the clock, database or backup repository."""
    if name not in SCENARIOS:
        raise Rejected("unknown prepared recovery scenario")
    return {
        "mode": MODES[2],
        **dict.fromkeys((name for name, _label, _kind in FIELDS), ""),
        "exercise": CHOICES["exercise"][SCENARIOS.index(name)],
    }


def ledger(count: int) -> dict[str, Any]:
    """Create balanced inert dispatch-supply orders with independently advancing original commit timestamps."""
    return {
        "customers": [[1, "Fictional dispatch supplies"]],
        "orders": [[n, 1, 30, BASE + n * 1000] for n in range(1, count + 1)],
        "lines": [[n, 1, "BANDAGE", 3, 10] for n in range(1, count + 1)],
        "payments": [[n, 30] for n in range(1, count + 1)],
    }


def prepared(name: str) -> tuple[dict[str, Any], bool]:
    """Use explicit synthetic ledgers/times; never invent measurements from a backup or database."""
    if name not in CHOICES["exercise"]:
        raise Rejected("unknown recovery exercise")
    if name in CHOICES["exercise"][:4]:
        data = decode(read_source(ROOT / "examples/objective-evaluation.json", CAP))
        if name == "zero-loss-fails":
            data["objectives"].update(rpo_ms=0, max_lost_orders=0)
        elif name == "rto-fails":
            data["elapsed_ms"] = 1001
        elif name == "restore-mismatch":
            data["restored"] = copy.deepcopy(data["source_head"])
        return data, False
    points = [
        {
            "id": char * 64,
            "created_at_ms": BASE + count * 1000,
            "provenance": "supplied_synthetic",
            "snapshot": ledger(count),
            "restored": ledger(count) if elapsed is not None else None,
            "elapsed_ms": elapsed,
            "legal_hold": False,
        }
        for char, count, elapsed in (
            ("a", 1, 50),
            ("b", 2, 100),
            ("c", 3, 900),
            ("d", 3, None),
        )
    ]
    if name == "all-untested":
        for row in points:
            row["restored"] = row["elapsed_ms"] = None
    elif name == "legal-hold":
        points[0]["legal_hold"] = True
        points[0]["restored"] = ledger(2)
    elif name == "separate-provenance":
        points[0]["provenance"] = "measured_lab"
    return {
        "schema": 1,
        "as_of_ms": BASE + 4000,
        "source_head": ledger(3),
        "objectives": {"rto_ms": 500, "rpo_ms": 1500, "max_lost_orders": 1},
        "retention_minimum": 1,
        "points": points,
    }, True


def control(text: str, lower: int, upper: int) -> int:
    """Accept only bounded ASCII integer text; bool, signs, fractions and implicit coercions are absent."""
    if not text or not text.isascii() or not text.isdecimal() or len(text) > 16:
        raise Rejected("bounded integer control required")
    return integer(int(text), lower, upper)


def analyze(
    state: Workspace, parameters: dict[str, str], stage: Path
) -> tuple[str, str, dict[str, bytes]]:
    """Validate captured data first, apply explicit policy changes and retain both original/effective evidence."""
    mode = parameters.get("mode")
    if mode not in MODES:
        raise Rejected("choose a supported recovery review")
    if mode == MODES[2]:
        data, catalog = prepared(parameters.get("exercise", ""))
        raw = canonical(data)
    else:
        raw = read_source(Path(parameters.get("document", "")), CAP)
        data, catalog = decode(raw), mode == MODES[1]
    original = copy.deepcopy(data)
    if not catalog:
        record(
            data, {"snapshot", "source_head", "restored", "elapsed_ms", "objectives"}
        )
    original_result = plan(original) if catalog else evaluate(**original)
    for name, low, high in (
        ("rto_ms", 1, 1800000),
        ("rpo_ms", 0, 1800000),
        ("max_lost_orders", 0, 10000),
    ):
        if parameters.get(name):
            data["objectives"][name] = control(parameters[name], low, high)
    for name, low, high in (("as_of_ms", 1, 2**53 - 1), ("retention_minimum", 1, 20)):
        if parameters.get(name):
            if not catalog:
                raise Rejected("catalog-only control cannot change an evaluation")
            data[name] = control(parameters[name], low, high)
    result = plan(data) if catalog else evaluate(**data)
    scope = {
        "schema": 1,
        "source_sha256": hashlib.sha256(raw).hexdigest(),
        "effective_sha256": hashlib.sha256(canonical(data)).hexdigest(),
        "original_objectives": original["objectives"],
        "effective_objectives": data["objectives"],
        "original_result": original_result,
        "prepared_synthetic": mode == MODES[2],
        "live_backup_accessed": False,
        "live_database_accessed": False,
        "raw_ledgers_saved": False,
        "retention_executed": False,
        "scope": "Original/effective captured evidence and objective review only. Labels/timing are supplied assertions, not authenticated measurements. No backup, restore, SQL, forget, prune or deletion was executed.",
    }
    if catalog:
        scope.update(
            original_as_of_ms=original["as_of_ms"],
            effective_as_of_ms=data["as_of_ms"],
            original_retention_minimum=original["retention_minimum"],
            effective_retention_minimum=data["retention_minimum"],
        )
        return (
            "captured-recovery-catalog",
            f"{len(result['points'])} captured points; {sum(len(g['eligible_points']) for g in result['groups'])} eligible; retention is review-only",
            {
                "recovery-review.json": canonical(result),
                "input-scope.json": canonical(scope),
            },
        )
    return (
        "captured-restore-evaluation",
        f"{result['result']}; {result['lost_orders']} orders lost; RPO {result['observed_rpo_ms']} ms / RTO {result['observed_rto_ms']} ms; captured evidence",
        {
            "restore-evaluation.json": canonical(result),
            "input-scope.json": canonical(scope),
        },
    )


def views(files: dict[str, bytes]) -> dict[str, list[dict[str, Any]]]:
    """Expose full independent loss/time/exact-match or point/retention evidence; filters never alter counts."""
    scope = {"kind": "scope", **json_value(files["input-scope.json"])}
    if "restore-evaluation.json" in files:
        r = json_value(files["restore-evaluation.json"])
        rows = [
            {
                "kind": "objective",
                "name": "Exact snapshot recovered",
                "observed": r["snapshot_matches"],
                "budget": True,
                "met": r["snapshot_matches"],
            },
            *[
                {
                    "kind": "objective",
                    "name": label,
                    "observed": r[a],
                    "budget": r[b],
                    "met": r[a] <= r[b],
                }
                for label, a, b in (
                    ("Recovery time ms", "observed_rto_ms", "rto_limit_ms"),
                    ("Recovery-point gap ms", "observed_rpo_ms", "rpo_limit_ms"),
                    ("Lost orders", "lost_orders", "lost_order_limit"),
                )
            ],
        ]
        return {
            "Original recovery objectives": rows,
            "Complete captured evaluation": [{"kind": "evaluation", **r}],
            "Original and effective scope": [scope],
        }
    r = json_value(files["recovery-review.json"])
    return {
        "All captured recovery points": [{"kind": "point", **p} for p in r["points"]],
        "Separate provenance recommendations": [
            {"kind": "group", **g} for g in r["groups"]
        ],
        "Retention human-review queue": [
            {"kind": "retention", **p} for p in r["points"]
        ],
        "Original and effective scope": [scope],
    }


def cells(row: dict[str, Any]) -> tuple[str, str, str, str]:
    """Display concise real evaluation/point values while full identifiers and reasons remain selectable."""
    if row["kind"] == "objective":
        return (
            str(row["name"]),
            str(row["observed"]),
            str(row["budget"]),
            "MET" if row["met"] else "NOT MET",
        )
    if row["kind"] == "point":
        r = row["evaluation"]
        return (
            row["id"][:12] + "…",
            row["provenance"],
            "UNTESTED"
            if r is None
            else f"RPO {r['observed_rpo_ms']} / RTO {r['observed_rto_ms']} ms",
            "ELIGIBLE" if row["eligible"] else "NOT ELIGIBLE",
        )
    if row["kind"] == "retention":
        return (
            row["id"][:12] + "…",
            row["retention_review"],
            "; ".join(row["retention_reasons"]),
            "No deletion executed",
        )
    if row["kind"] == "group":
        return (
            row["provenance"],
            str(len(row["eligible_points"])) + " eligible",
            (row["recommended_point"] or "NONE")[:16],
            "Labels not authenticated",
        )
    if row["kind"] == "evaluation":
        return (
            "Complete captured restore",
            str(row["recovered_orders"]) + " recovered",
            str(row["lost_orders"]) + " lost",
            row["result"],
        )
    return (
        "Original / effective policy",
        str(row["original_objectives"]),
        str(row["effective_objectives"]),
        "No live recovery/deletion",
    )
