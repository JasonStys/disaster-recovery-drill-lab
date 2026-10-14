# Contribution and coding conventions

Author: Jason Stys.

Use Python for portable orchestration/independent validation, SQL for transactional constraints/fixtures, Bash for strict CI sequencing and HTML for inert local reports. No extra language is added without a task-specific reason.

Keep functions small with descriptive names, explicit units and docstrings stating inputs/outputs/failures. Type-check dr/ strictly; use bounded structures, integer money, canonical serialization and fixed argument arrays rather than shell strings. Comment intent and safety boundaries, not every obvious statement.

The file header states purpose/author; `python scripts/code_map.py` generates exact definitions/parameters/variable locations. SQL/YAML/Bash symbols also get maps. JSON cannot contain comments: README gives its purpose; data remains valid JSON. `python scripts/file_guide.py` lists every staged/tracked file and fails unknown formats. Stage intended files before generating the guide.

Run official checksum-verified bootstrap, Ruff, mypy, pytest/coverage, map/inventory/privacy checks, measured native exercise and all CI jobs. Keep negative/property tests. Update tests when changing objectives or schema. Never claim a unit fixture is a measured live restore. No local Docker repair or production access is authorized.

Hashes for official tools/images, development lock graphs and Actions revisions are intentional reviewed pins; update by verifying upstream origin/current advisories and re-running all gates. Commit measured aggregates and validation notes, not raw backups, secrets, env-files, caches, logs or tool binaries. Preserve failures and explain corrections. No advisory suppression to manufacture green status.
