# Primary research and design rationale

Author: Jason Stys. Reviewed 2026-10-13; tools/images locked to verified hashes rather than floating releases.

- [restic official repository preparation](https://restic.readthedocs.io/en/stable/030_preparing_a_new_repo.html): established password-protected repository, not custom encryption.
- [restic integrity checks](https://restic.readthedocs.io/en/stable/045_working_with_repos.html): full data read is distinct from structural metadata checks; this lab requires check --read-data.
- [restic restore](https://restic.readthedocs.io/en/stable/050_restore.html): exact snapshot and restore verification. The floating latest selector is intentionally not used.
- [restic format/security design](https://restic.readthedocs.io/en/stable/100_references.html): encryption and authenticated storage are upstream responsibilities; this repo does not recreate cryptography.
- [official restic releases](https://github.com/restic/restic/releases/tag/v0.19.1): archive SHA256 pins for reviewed amd64 platforms, verified before execution.
- [PostgreSQL pg_dump](https://www.postgresql.org/docs/current/app-pgdump.html): database-aware consistent custom logical archive; copying a live data directory is not this strategy.
- [PostgreSQL pg_restore](https://www.postgresql.org/docs/current/app-pgrestore.html): transactional exit-on-error restoration into a new trusted destination; arbitrary SQL archives are unsafe to import blindly.
- [PostgreSQL commit information](https://www.postgresql.org/docs/current/functions-info.html) and [commit tracking](https://www.postgresql.org/docs/current/runtime-config-replication.html): start-time tracking and original xmin commit times are persisted before backup; restore xmin is a different transaction and would distort RPO.
- [Official PostgreSQL image](https://hub.docker.com/_/postgres): pinned image, PostgreSQL18 volume parent /var/lib/postgresql, non-root user and bounded ephemeral tmpfs; no published port.
- [Docker resource constraints](https://docs.docker.com/engine/containers/resource_constraints/): explicit CPU, memory and PID bounds rather than unbounded local services.
- [GitHub Actions security hardening](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions): full action revisions, least-privilege permissions and nonpersistent checkout credentials.

These sources inform a small controlled implementation, not endorsed certification, complete cryptographic verification or production architectural guidance. Metrics and limitations are defined in contracts.md rather than borrowed generic promises.
