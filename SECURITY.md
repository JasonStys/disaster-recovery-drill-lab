# Security boundary and reporting

Author: Jason Stys. Contact through the README professional links; never post passwords/backups or administrator access in issues.

Only synthetic reviewed fixtures and NEW local workspaces are supported. No accounts, customer uploads, remote backup destinations or production databases are accepted. Inputs to offline evaluation are bounded JSON, not SQL, URLs or code.

Trust: local filesystem parents, host/Docker administrator, official pinned binaries and digest-pinned PostgreSQL source. Encryption is restic's implementation, not custom code; checksum pins do not independently prove producer identity or absence of tool vulnerabilities. Repository write access or local admin can replace this program. Reports' hashes/IDs are fingerprints, not signatures or independently authenticated evidence.

Runtime backup key, wrong-key test credential, PostgreSQL password/env-file and plaintext dump are private ignored **synthetic** local data. POSIX files use 0600/directories 0700; Windows depends on inherited user ACLs rather than a claim that chmod implements Windows access control. Administrators/container inspection can see generated test credentials. No user account credentials are collected. Disk encryption and key escrow are out of scope.

Docker operations force the local Linux socket and exact newly tracked names. Ownership/image/network/non-root/resource guards precede exec, stop and removal. Containers have no network, public ports, persistent/host mounts, extra capabilities or writable roots. A hostile Docker daemon/kernel is outside containment claims. No broad prune/delete command exists.

pg_restore can execute database-origin SQL: NEVER adapt this to uploaded/untrusted archives or a privileged production account without a separate sandbox/access/security design. This drill creates its own trusted schema/archive. Logical dump does not back up cluster roles, whole hosts, external services or continuous WAL. A same-host encrypted repo is not off-site/immutable/ransomware-resilient storage.

Recovery completion requires independent whole-ledger equality plus actual constraints, not merely process exit 0. Wrong key, missing snapshot and corruption cases use specific error oracles; generic errors cannot masquerade as security controls. Reports escape strings and allow no scripts/network under a restrictive CSP.

Dependency, image, secret/workflow and CodeQL checks are point-in-time evidence, not certification. Native tool/SQL/Docker orchestration and the helper scripts have separate integration checks; coverage percentage applies only to authored dr/ modules. Follow the runbook for cleanup/incident escalation. Do not weaken gates or delete failed runs to make results look successful.
