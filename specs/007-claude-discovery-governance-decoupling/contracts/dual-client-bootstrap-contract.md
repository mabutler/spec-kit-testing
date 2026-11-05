# Contract: Dual-Client Discovery, Seeding & Manifest Integrity

**Feature Branch**: `007-claude-discovery-governance-decoupling`  
**Date**: 2026-11-05  
**Traces**: `FR-001`, `FR-002`, `FR-003`, `FR-004`, `FR-005`, `FR-010`, `SC-001`, `SC-002`, `SC-004`

## 1. Dual-Client Directory & Parity Contract (`FR-001`, `SC-001`)

Both client asset directories MUST exist at the repository root and maintain 100% byte-for-byte parity across all 14 canonical files:

| Asset Category | Antigravity Path (`.agents/`) | Claude Code Path (`.claude/`) | Manifest Tier |
|----------------|-------------------------------|--------------------------------|---------------|
| Execution Subagent Profile | `.agents/agents/speckit-executor.md` | `.claude/agents/speckit-executor.md` | `agent` |
| Reasoning Subagent Profile | `.agents/agents/speckit-reasoner.md` | `.claude/agents/speckit-reasoner.md` | `agent` |
| Analyze Skill | `.agents/skills/speckit-analyze/SKILL.md` | `.claude/skills/speckit-analyze/SKILL.md` | `skill` |
| Bootstrap Skill | `.agents/skills/speckit-bootstrap/SKILL.md` | `.claude/skills/speckit-bootstrap/SKILL.md` | `skill` |
| Checklist Skill | `.agents/skills/speckit-checklist/SKILL.md` | `.claude/skills/speckit-checklist/SKILL.md` | `skill` |
| Clarify Skill | `.agents/skills/speckit-clarify/SKILL.md` | `.claude/skills/speckit-clarify/SKILL.md` | `skill` |
| Constitution Skill | `.agents/skills/speckit-constitution/SKILL.md` | `.claude/skills/speckit-constitution/SKILL.md` | `skill` |
| Converge Skill | `.agents/skills/speckit-converge/SKILL.md` | `.claude/skills/speckit-converge/SKILL.md` | `skill` |
| Implement Skill | `.agents/skills/speckit-implement/SKILL.md` | `.claude/skills/speckit-implement/SKILL.md` | `skill` |
| Orchestrate Skill | `.agents/skills/speckit-orchestrate/SKILL.md` | `.claude/skills/speckit-orchestrate/SKILL.md` | `skill` |
| Plan Skill | `.agents/skills/speckit-plan/SKILL.md` | `.claude/skills/speckit-plan/SKILL.md` | `skill` |
| Roadmap Skill | `.agents/skills/speckit-roadmap/SKILL.md` | `.claude/skills/speckit-roadmap/SKILL.md` | `skill` |
| Specify Skill | `.agents/skills/speckit-specify/SKILL.md` | `.claude/skills/speckit-specify/SKILL.md` | `skill` |
| Tasks Skill | `.agents/skills/speckit-tasks/SKILL.md` | `.claude/skills/speckit-tasks/SKILL.md` | `skill` |

---

## 2. Bootstrapper Seeding CLI Contract (`FR-002`, `FR-003`, `SC-002`)

### POSIX Shell (`bootstrap-speckit.sh`) & PowerShell (`bootstrap-speckit.ps1`)

- **Invocation**:
  - `./bootstrap-speckit.sh <target-repo> [--force] [--help|-h]`
  - `pwsh ./bootstrap-speckit.ps1 <target-repo> [-Force] [-Help]`
- **Line-Count Ceiling**: Both scripts MUST remain `< 150` lines.
- **Source Bundle Pre-Verification (Fail-Closed)**:
  Must verify existence of required templates in `.specify/templates/`, `.specify/extensions.yml`, `.agents/agents/{speckit-reasoner,speckit-executor}.md`, and `.claude/agents/{speckit-reasoner,speckit-executor}.md` before mutating `<target-repo>`. If any required source file is missing, log `CRITICAL: Source bundle is missing required assets: <path>` to `stderr` and exit `1`.
- **Protected User-State Exclusions (`PRESERVE_USER_STATE`)**:
  When copying from `.specify`, `.agents`, and `.claude`, the bootstrapper MUST NEVER copy or overwrite:
  - `.specify/memory/*`
  - `.specify/templates/overrides/*`
  - `.specify/feature.json`
  - `.agents/agents/*.local.md`
  - `.claude/agents/*.local.md`
  - `.claude/settings.local.json`
  - `specs/*` or root `ROADMAP.md`
- **Gitignore Idempotency (`FR-003`)**:
  Must ensure `<target-repo>/.gitignore` (as well as the toolkit's own root `.gitignore`) contains ignore patterns for local files:
  - `.agents/agents/*.local.md`
  - `.claude/agents/*.local.md`
  - `.claude/settings.local.json`
- **Telemetry Output**:
  ```text
  [INFO] Verified source bundle integrity
  [INFO] Seeded .specify/ configuration and templates (<N> files)
  [INFO] Seeded .agents/ skills and agent definitions (<N> files)
  [INFO] Seeded .claude/ skills and agent definitions (<N> files)
  ```

---

## 3. Integration Manifest & `/speckit-bootstrap` Verification Contract (`FR-004`, `FR-005`, `FR-010`)

- **`.specify/integrations/claude.manifest.json`**:
  - Must track all 14 `.claude/` files with exact 64-character lowercase hex SHA-256 digests matching `.specify/integrations/agy.manifest.json`.
- **`.specify/integrations/speckit-bootstrap.manifest.json`**:
  - Must track all 53 managed files across `.agents/` (14 files), `.claude/` (14 files), and `.specify/` (25 files, including `.specify/integrations/claude.manifest.json`), with accurate `"digest": "sha256:<hex>"` and `"size_bytes": <int>`.
- **`/speckit-bootstrap` Skill Contract**:
  - Protected User-State Rule protects `.agents/agents/*.local.md`, `.claude/agents/*.local.md`, and custom skills in `.agents/skills/` and `.claude/skills/`.
  - Mode A (`Self-Check`) and Mode B (`--check` / `--upgrade`) inspect and verify both `.agents/` (`agy.manifest.json`) and `.claude/` (`claude.manifest.json`) alongside `.specify/` (`speckit.manifest.json` and `speckit-bootstrap.manifest.json`), verifying byte-for-byte parity between `.agents/` and `.claude/` canonical files.
