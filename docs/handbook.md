# Disaster Recovery Drill Lab handbook

By Jason Stys.

Plan and rehearse recovery from bounded backup evidence, then inspect measured restoration and continuity results. Real PostgreSQL restore and derived-image gates remain separate from synthetic planning or local documentation checks.

Compare captured recovery candidates by provenance, RPO/RTO and loss; add non-deleting retention review and patch actual restored-container vulnerabilities.

Connects recovery selection to measured evidence while keeping untested candidates explicitly unknown.

## Read the documentation

| Edition | Audience and contents |
| --- | --- |
| [project-guide.docx](reports/project-guide.docx) | User and developer guide: purpose, current usage, design, boundaries and source references. |

The editable Markdown remains the maintenance source. The Word files are readable editions. See [publication identities and review](reports/publications.json) and the [documentation refresh record](reports/documentation-refresh-2026-11-09.md).

## Current usage and help

[README quick start](../README.md) is the entry point. Use the project-specific guides below before changing inputs, operating modes or deployment assumptions.

### Usage and operations

- [recovery planning](recovery-planning.md)
- [runbook](runbook.md)

### Design and contracts

- [architecture](architecture.md)
- [contracts](contracts.md)
- [research](research.md)

### Security and validation

- [testing](testing.md)

## Historical results and reproduction

The reviewed source is [`ceb77d8f0d0aafb647c6873adf94c730d6eca168`](https://github.com/JasonStys/disaster-recovery-drill-lab/tree/ceb77d8f0d0aafb647c6873adf94c730d6eca168). The observed functional workflow baseline is `ceb77d8f0d0aafb647c6873adf94c730d6eca168`; those observations are recorded at `2026-11-10T05:25:40.628667+00:00`. They do not certify an unrun later revision.

- [Detailed recorded validation](reports/planning-2026-11-09.md)
- [Current Actions](https://github.com/JasonStys/disaster-recovery-drill-lab/actions) records later integration checks separately.
- Preserve dated measurements and follow the existing testing guide to reproduce them; a test-source inventory alone does not establish execution.

## Practical boundaries

- Captured provenance and timings are assertions, not authenticated backup acquisition.
- Manual retention review never authorizes or performs deletion.
- Lab RPO/RTO objectives do not authorize production recovery or imply zero loss for untested candidates.

## Maintaining these editions

Update the editable usage/design/test documents first. Rebuild and visually review every Word page and workbook tab before replacing an edition; verify the exact binary digests and evidence source in publications.json. Keep account data, logs with secrets, installed-app state and private test stores out of documentation. Source and release assets retain their existing security and licensing boundaries.

## Native offline application

[Practical controls, schemas, privacy, build and lifecycle](native-application.md) · [Dated candidate validation](reports/native-workbench-2026-11-11.md). Earlier Office editions retain their original source baseline.
