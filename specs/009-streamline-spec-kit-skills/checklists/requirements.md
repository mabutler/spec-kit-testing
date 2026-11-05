# Requirements Checklist: 009-streamline-spec-kit-skills

## User Story 1: Prune Redundant Template Resolution Prompts
- [x] Clear concise template lookup in `speckit-specify`
- [x] Clear concise template lookup in `speckit-plan`
- [x] Clear concise template lookup in `speckit-tasks`
- [x] Clear concise template lookup in `speckit-checklist`

## User Story 2: Decouple Documentation Gate from Skills to Constitution
- [x] Removed hardcoded `Documentation Impact` from `speckit-plan`
- [x] Removed hardcoded `Documentation Impact` from `speckit-tasks`
- [x] Removed hardcoded `Documentation Impact` from `speckit-analyze`
- [x] Removed hardcoded `Documentation Impact` from `speckit-implement`
- [x] Removed hardcoded `Documentation Impact` from `speckit-converge`
- [x] Constitution Principle VII retained as authority for docs

## User Story 3: Selective & Lazy Governance Context Loading
- [x] `speckit-specify` loads only `constitution.md`
- [x] `speckit-clarify` loads only `constitution.md`
- [x] `speckit-plan` loads `constitution.md` + architectural coding standards
- [x] `speckit-tasks` loads `constitution.md` + structural coding standards
- [x] `speckit-implement` loads `coding-standards.md` + `logging-standards.md`

## User Story 4: Remove Redundant Principle III Extraction Blocks
- [x] Trimmed custom extraction boilerplate in `speckit-tasks`
- [x] Trimmed custom extraction boilerplate in `speckit-orchestrate`
- [x] Commands defer directly to active constitution for testing rules

## User Story 5: Dual-Client Parity & Manifest Synchronization
- [x] Mirror all skill changes from `.agents/` to `.claude/`
- [x] Verify `diff -r .agents/skills .claude/skills` returns exit code 0
- [x] Update manifests (`agy.manifest.json`, `claude.manifest.json`, `speckit-bootstrap.manifest.json`)
