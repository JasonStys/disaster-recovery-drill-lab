"""Independent captured-recovery oracles, policy changes and no-secret/no-raw-ledger output checks. Jason Stys."""
# BEGIN CODE MAP (generated; python scripts/code_map.py)
# definition: run — line 87
# parameter: changes — line 87
# parameter: name — line 87
# parameter: tmp_path — line 87
# variable: params — line 89
# definition: test_captured_restore_oracles — line 102
# parameter: exact — line 102
# parameter: loss — line 102
# parameter: name — line 102
# parameter: rpo — line 102
# parameter: rto — line 102
# parameter: tmp_path — line 102
# parameter: verdict — line 102
# variable: files — line 104
# variable: r — line 105
# variable: views — line 114
# variable: rows — line 116
# variable: row — line 117
# definition: test_catalog_tradeoff_and_no_newest_shortcut — line 121
# parameter: tmp_path — line 121
# variable: files — line 123
# variable: r — line 124
# variable: row — line 132
# variable: rows — line 132
# variable: values — line 138
# variable: row — line 139
# definition: test_protected_unknown_and_separate_groups — line 151
# parameter: eligible — line 151
# parameter: groups — line 151
# parameter: name — line 151
# parameter: tmp_path — line 151
# variable: r — line 153
# variable: row — line 156
# definition: test_import_and_explicit_effective_policy — line 169
# parameter: tmp_path — line 169
# variable: _ — line 171
# variable: data — line 171
# variable: source — line 172
# variable: raw — line 173
# variable: _ — line 175
# variable: files — line 175
# variable: scope — line 185
# definition: test_catalog_selected_clock_and_minimum — line 202
# parameter: tmp_path — line 202
# variable: _ — line 204
# variable: data — line 204
# variable: source — line 205
# variable: _ — line 207
# variable: files — line 207
# variable: r — line 218
# variable: row — line 220
# definition: test_controls_fail_closed — line 236
# parameter: key — line 236
# parameter: tmp_path — line 236
# parameter: value — line 236
# definition: test_original_invalid_policy_not_hidden_by_override — line 242
# parameter: tmp_path — line 242
# variable: _ — line 244
# variable: data — line 244
# variable: source — line 246
# definition: test_bad_mode_extra_field_and_unknown_exercise — line 256
# parameter: tmp_path — line 256
# variable: _ — line 264
# variable: data — line 264
# variable: source — line 266
# definition: test_catalog_only_control_rejected_on_restore — line 272
# parameter: tmp_path — line 272
# definition: test_corrupt_ledger_refused_before_any_save — line 278
# parameter: tmp_path — line 278
# variable: _ — line 280
# variable: data — line 280
# variable: data — line 281
# variable: source — line 283
# END CODE MAP

import copy
from pathlib import Path

import pytest

from dr import desktop_project as p
from dr.desktop_io import canonical, json_value


def run(tmp_path, name, **changes):
    """Use the same project adapter as the real controls with explicit independent inputs."""
    params = p.scenario(p.SCENARIOS[p.CHOICES["exercise"].index(name)]) | changes
    return p.analyze(None, params, tmp_path)[2]


@pytest.mark.parametrize(
    "name,verdict,loss,rpo,rto,exact",
    [
        ("captured-pass", "PASS", 1, 400, 100, True),
        ("zero-loss-fails", "FAIL", 1, 400, 100, True),
        ("rto-fails", "FAIL", 1, 400, 1001, True),
        ("restore-mismatch", "FAIL", 0, 0, 100, False),
    ],
)
def test_captured_restore_oracles(tmp_path, name, verdict, loss, rpo, rto, exact):
    """Loss, time and exact identity are independent; zero apparent loss cannot mask wrong restored bytes."""
    files = run(tmp_path, name)
    r = json_value(files["restore-evaluation.json"])
    assert (
        r["result"],
        r["lost_orders"],
        r["observed_rpo_ms"],
        r["observed_rto_ms"],
        r["snapshot_matches"],
    ) == (verdict, loss, rpo, rto, exact)
    assert "Fictional A" not in b"".join(files.values()).decode()
    views = p.views(files)
    assert len(views["Original recovery objectives"]) == 4
    for rows in views.values():
        for row in rows:
            assert len(p.cells(row)) == 4


def test_catalog_tradeoff_and_no_newest_shortcut(tmp_path):
    """The middle point wins; the newest unknown/slow points cannot become a successful restore."""
    files = run(tmp_path, "point-tradeoffs")
    r = json_value(files["recovery-review.json"])
    assert r["groups"] == [
        {
            "provenance": "supplied_synthetic",
            "eligible_points": ["b" * 64],
            "recommended_point": "b" * 64,
        }
    ]
    rows = {row["id"]: row for row in r["points"]}
    assert rows["d" * 64]["evaluation"] is None
    assert not rows["c" * 64]["eligible"]
    assert rows["a" * 64]["retention_review"] == "MANUAL_RETIREMENT_REVIEW"
    assert "untested_restore_requires_drill" in rows["d" * 64]["retention_reasons"]
    assert "Fictional dispatch supplies" not in b"".join(files.values()).decode()
    for values in p.views(files).values():
        for row in values:
            assert len(p.cells(row)) == 4


@pytest.mark.parametrize(
    "name,eligible,groups",
    [
        ("all-untested", False, 1),
        ("legal-hold", True, 1),
        ("separate-provenance", True, 2),
    ],
)
def test_protected_unknown_and_separate_groups(tmp_path, name, eligible, groups):
    """Untested is not successful; holds/mismatches stay protected and provenance labels stay separate."""
    r = json_value(run(tmp_path, name)["recovery-review.json"])
    assert r["has_eligible_point"] is eligible and len(r["groups"]) == groups
    if name == "legal-hold":
        row = next(row for row in r["points"] if row["id"] == "a" * 64)
        assert set(row["retention_reasons"]) == {
            "legal_hold",
            "restore_mismatch_requires_investigation",
        }
    elif name == "separate-provenance":
        assert r["groups"][0] == {
            "provenance": "measured_lab",
            "eligible_points": [],
            "recommended_point": None,
        }


def test_import_and_explicit_effective_policy(tmp_path):
    """Actual selected file remains unchanged; original PASS and effective FAIL are both retained."""
    data, _ = p.prepared("captured-pass")
    source = tmp_path / "authorized.json"
    raw = canonical(data)
    source.write_bytes(raw)
    _, _, files = p.analyze(
        None,
        {
            "mode": p.MODES[0],
            "document": str(source),
            "rpo_ms": "0",
            "max_lost_orders": "0",
        },
        tmp_path,
    )
    scope = json_value(files["input-scope.json"])
    assert scope["original_result"]["result"] == "PASS"
    assert json_value(files["restore-evaluation.json"])["result"] == "FAIL"
    assert (
        scope["original_objectives"]["rpo_ms"] == 400
        and scope["effective_objectives"]["rpo_ms"] == 0
    )
    assert scope["source_sha256"] != scope["effective_sha256"]
    assert source.read_bytes() == raw
    assert (
        scope["live_backup_accessed"]
        is scope["live_database_accessed"]
        is scope["retention_executed"]
        is False
    )


def test_catalog_selected_clock_and_minimum(tmp_path):
    """Selected catalog supports explicit review clock/retention without changing raw captured data."""
    data, _ = p.prepared("point-tradeoffs")
    source = tmp_path / "catalog.json"
    source.write_bytes(canonical(data))
    _, _, files = p.analyze(
        None,
        {
            "mode": p.MODES[1],
            "document": str(source),
            "as_of_ms": str(p.BASE + 5000),
            "retention_minimum": "4",
            "rto_ms": "1000",
        },
        tmp_path,
    )
    r = json_value(files["recovery-review.json"])
    assert r["groups"][0]["recommended_point"] == "c" * 64
    assert all(row["retention_review"] == "KEEP_REVIEW" for row in r["points"])
    assert json_value(files["input-scope.json"])["original_retention_minimum"] == 1


@pytest.mark.parametrize(
    "key,value",
    [
        ("rto_ms", "0"),
        ("rpo_ms", "-1"),
        ("max_lost_orders", "10001"),
        ("rto_ms", "NaN"),
        ("rpo_ms", "١"),
        ("as_of_ms", str(p.BASE - 1)),
        ("retention_minimum", "21"),
    ],
)
def test_controls_fail_closed(tmp_path, key, value):
    """No coercion, malformed clock or out-of-bound policy becomes a successful review."""
    with pytest.raises(ValueError):
        run(tmp_path, "point-tradeoffs", **{key: value})


def test_original_invalid_policy_not_hidden_by_override(tmp_path):
    """A valid new policy cannot silently legitimize an invalid original input or forged timestamp."""
    data, _ = p.prepared("captured-pass")
    data["objectives"]["rto_ms"] = False
    source = tmp_path / "bad.json"
    source.write_bytes(canonical(data))
    with pytest.raises(ValueError):
        p.analyze(
            None,
            {"mode": p.MODES[0], "document": str(source), "rto_ms": "1000"},
            tmp_path,
        )


def test_bad_mode_extra_field_and_unknown_exercise(tmp_path):
    """Unknown operations or unrecognized captured fields cannot select a hidden active restore path."""
    with pytest.raises(ValueError):
        p.analyze(None, {"mode": "restore-live"}, tmp_path)
    with pytest.raises(ValueError):
        p.scenario("unknown")
    with pytest.raises(ValueError):
        p.prepared("unknown")
    data, _ = p.prepared("captured-pass")
    data["password"] = "inert-rejected-fixture"
    source = tmp_path / "extra.json"
    source.write_bytes(canonical(data))
    with pytest.raises(ValueError):
        p.analyze(None, {"mode": p.MODES[0], "document": str(source)}, tmp_path)


def test_catalog_only_control_rejected_on_restore(tmp_path):
    """A hidden catalog field cannot silently alter the wrong operation's meaning."""
    with pytest.raises(ValueError):
        run(tmp_path, "captured-pass", retention_minimum="1")


def test_corrupt_ledger_refused_before_any_save(tmp_path):
    """A balanced unrelated file is not arbitrary SQL; broken payment relations remain rejected."""
    data, _ = p.prepared("point-tradeoffs")
    data = copy.deepcopy(data)
    data["points"][0]["snapshot"]["payments"][0][1] = 999
    source = tmp_path / "bad-catalog.json"
    source.write_bytes(canonical(data))
    with pytest.raises(ValueError):
        p.analyze(None, {"mode": p.MODES[1], "document": str(source)}, tmp_path)
    assert not list(Path(tmp_path).glob("*.sqlite"))
