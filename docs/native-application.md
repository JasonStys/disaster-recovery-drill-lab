# Disaster Recovery Review Workbench: native application

Created by **Jason Stys** · [Source/contact](https://github.com/JasonStys) · [Professional profile](https://www.linkedin.com/in/jason-stys-31b30b351/).

Inspect captured restore ledgers and recovery-point catalogs with the original exact-snapshot, financial-consistency, RPO/RTO/lost-order and conservative retention engines. Change review policy explicitly while preserving the original evidence. No backup, restore, SQL, Docker, forget, prune or deletion is executed by the GUI.

## Launch and practical controls

The Windows x64 portable candidate is `DisasterRecoveryDrillLab.exe`. Its complete real Tk interface and original project engines bundle CPython 3.14.10, Tcl/Tk 9.0.4 and actual original runtime notices. A reviewed download needs no separately installed Python, Node, command setup, default password or background service. It is a portable EXE, not an NSIS installer, Authenticode-signed product or a claim that a public distribution already exists. Publication/download availability is a separate reviewed gate.

1. Select **Evaluate authorized captured restore**, choose your bounded JSON file, acknowledge authorized access and run. The original schema contains independently supplied `snapshot`, `source_head`, `restored`, `elapsed_ms` and `objectives`. Customer/order/line/payment consistency and append-only commit history must validate. A valid but different restored ledger still fails exact recovery.
2. Optionally enter stricter or looser RTO, RPO and maximum lost-order limits. The original input is validated first; both original and effective policy, results and hashes remain selectable. Limits do not change captured data or elapsed time. A zero-loss requirement correctly fails the example that lost one order.
3. For multiple points, choose **Review authorized recovery-point catalog**. Supply one captured source head and the original closed catalog schema, with an explicit as-of clock and retention minimum where needed. Inspect eligibility, separate provenance groups, recommendations and retention reasons. A newest slow/untested point cannot replace a known viable restore; legal holds and mismatches require review.
4. Eight prepared cases populate the same ordinary editable controls: exact captured restore, strict loss and time failures, mismatched restore, point tradeoffs, all-untested, legal hold, and separate synthetic/measured-label groups. The labels and timings are supplied assertions, not authenticated acquisition.
5. Search/filter without changing original denominators, inspect full aggregate detail, and export an exact bundle to a new destination. Original raw financial rows are not saved in the aggregate; preserve your own input files separately. Saved review history survives normal Exit/restart. Deleting a saved review requires confirmation and never deletes input files or backups.

## Private local profile and completion

The default durable profile lives in the OS-local application-data directory under `DisasterRecoveryDrillLab`, outside the executable and Git repository. An explicit `--profile` remains available for an authorized dedicated directory. Original CLI paths/contracts are preserved. Reports and chosen paths are sensitive owner-local plaintext: no encryption, multiuser login or hostile-administrator isolation is claimed.

Before SQLite initialization, all lexical ancestors and fixed marker, lock, database and journal/WAL/SHM files are checked for aliases, nonregular entries and multiple links. Ordinary owned recovery sidecars are retained; unknown/nonempty directories are not reset. The profile owner lock remains held through analysis, immutable evidence commit and actual worker completion. Busy Exit keeps its owner window/lock rather than force-killing a worker or silently abandoning a transaction. Static checks do not isolate a malicious same-user process replacing paths concurrently.

Supported inputs use bounded stable ordinary-descriptor reads, strict JSON and the original closed domain parsers. Unrecognized fields, duplicates, nonfinite values, unsafe bounds or invalid metadata are refused without reflecting raw inputs. Export is exact and refuses overwrite. Help and complete original Python/Tcl/Tk/freezer notices work offline. No HTTP listener, provider account, telemetry, popup-ad integration, arbitrary executable, script/plugin evaluator or background upload is introduced.

## Build and actual executable acceptance

Use a dedicated environment with the reviewed Windows CPython 3.14.10 runtime:

```text
python -m pip install --require-hashes -r requirements-dev.lock -r requirements-native.lock
python -m pip check
python scripts/build_native.py
python scripts/test_native_app.py
```

The one-file build binds its exact source SHA, honest dirty flag, actual Python DLL, original notices and allowlisted resources. The consumer starts the real EXE with a minimal system-only environment and explicit synthetic profile, drives the same widgets/handlers/mainloop, uses actual file chooser paths, checks independent domain oracles, captures two actual native screens, normally exits and repeats against the same durable history. CI rejects dirty source and verifies both owned bootloader/frozen PIDs are gone. No real user profile or installed application is opened.

The compiled consumer uses eight prepared scenarios and two actual file selections with independent literal oracles: one lost order/400ms RPO/100ms RTO; stricter zero-loss and slow-restore failures; exact snapshot mismatch despite zero apparent loss; middle-point selection; untested noneligibility; protected legal hold; separate provenance groups; and explicit policy changes preserving original PASS evidence. It checks complete export, invalid-input history retention, cancel/confirm deletion and identical ten-bundle history across two normal launches.

The source-quality lanes independently require their actual selected Python to import both native `_tkinter` and `tkinter`, construct/query a no-display Tcl interpreter and validate loaded/compiled families. This is distinct from a graphical display test. There is no redundant distro-Python Tk install, ignored error, fallback or skip. The real compiled Windows journey remains the graphical proof.

## Limits and original tools

Captured evidence review is not backup authenticity, a measured recovery drill, PostgreSQL execution, WAL/PITR, operational cutover or a zero-loss guarantee. Only the authored fictional append-only relational schema is supported, not arbitrary SQL/dumps. Measured-label and synthetic groups remain separate; retention is nondeleting advice. Original real restic encryption and isolated PostgreSQL CLI/hosted drills remain intact and mandatory for their distinct claims.

[Dated candidate validation](reports/native-workbench-2026-11-11.md). Existing Office guides and historical reports keep their own recorded source identities; they are not relabeled as current native release/install proof.
