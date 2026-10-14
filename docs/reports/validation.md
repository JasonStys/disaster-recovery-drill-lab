# Measured validation and author review

Author: Jason Stys. Work in progress: native and hosted evidence are accepted only after actual completed runs. No placeholder PASS metrics or fabricated database results are published.

Native Windows development validation: 79 tests passed, 98.13% combined statement/branch coverage of dr/, with strict Ruff/mypy and a complete hash-locked development advisory audit passing. Native restic backup/full integrity check/wrong-key/missing-ID/corruption/verified restore passed on synthetic data. Committed-source and hosted measurements will replace this development note after final validation. PostgreSQL is deliberately not run on local Docker Desktop.

Review plan covers bounded input, append-only data and original commit times, exact snapshot/content equality, explicit objectives, process ownership/resource/context guards, no-overwrite outputs, fixed errors and public aggregate privacy. Database/cryptographic integration claims require the actual tools, not fabricated fixtures.

## Development corrections

- The missing-snapshot test initially expected a short-ID lookup diagnostic. A full ID actually produces a snapshot-load ENOENT error. The oracle now requires the exact absent ID and specific missing-file rejection, not arbitrary failure.
- Review found that a backdated new order could falsely look like a zero-time loss window. New order times must now advance beyond baseline; a regression rejects backdated appends.
- Source readiness checks distinguish final PostgreSQL PID1 from its temporary initialization server.
- Original business commit times are persisted from PostgreSQL's commit tracking; restore transaction xmin must not substitute for original timestamps.

No local Docker repair, production data access, paid deployment or Actions-history deletion is performed. This repository uploads no backup/password/artifact/cache. Point-in-time scans do not prove absence of future vulnerabilities; scope/gaps remain explicit.
