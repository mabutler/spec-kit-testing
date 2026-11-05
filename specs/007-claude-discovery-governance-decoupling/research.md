# Phase 0 Research: Claude Discovery Compatibility & Constitutional Test Decoupling

**Feature Branch**: `007-claude-discovery-governance-decoupling`  
**Date**: 2026-11-05  
**Spec**: [`spec.md`](spec.md)

## Research Decisions & Rationale

### Decision 1: Mirrored Dual-Client Asset Directories (`.claude/` and `.agents/`) Over Filesystem Symlinks

- **Decision**: Maintain byte-identical mirrored directory trees in `.claude/` (`.claude/skills/<skill-name>/SKILL.md` and `.claude/agents/<agent-name>.md`) and `.agents/` (`.agents/skills/<skill-name>/SKILL.md` and `.agents/agents/<agent-name>.md`), verified via cryptographic SHA-256 manifests and static parity gates (`cmp -s` / `diff -rq`).
- **Rationale**:
  1. **Cross-Platform Windows Compatibility**: Developer feedback originates from work PCs where Windows and Git for Windows frequently run without `SeCreateSymbolicLinkPrivilege` or `core.symlinks=true`. Git symlinks checked out as plain text pointer files break skill and subagent discovery in Claude Code and PowerShell environments.
  2. **Deterministic Seeding**: Both `bootstrap-speckit.sh` and `bootstrap-speckit.ps1` copy regular files cleanly across POSIX and Windows filesystems without requiring elevated privileges.
  3. **Independent Manifest Verification**: Tracking `.agents/` in `.specify/integrations/agy.manifest.json`, `.claude/` in `.specify/integrations/claude.manifest.json`, and all managed assets in `.specify/integrations/speckit-bootstrap.manifest.json` guarantees zero drift between mirrored trees.
- **Alternatives Considered**:
  - *Directory or file symlinks (`.claude/skills -> ../.agents/skills`)*: Rejected because git symlinks degrade into unparsed text files on default Windows setups and complicate `Get-ChildItem` traversal in `bootstrap-speckit.ps1`.
  - *Single `.claude/` directory only*: Rejected because Google Antigravity natively discovers skills in `.agents/skills/` and subagent profiles in `.agents/agents/`. Dual directories provide zero-configuration discovery in both environments simultaneously.

---

### Decision 2: Dynamic Constitutional Deference Protocol for Principle III Verification & Testing

- **Decision**: Remove all hardcoded prohibitions against automated tests (e.g., `"Principle III: ZERO automated test files, test directories, or test tasks"`) from reusable agent profiles (`speckit-executor.md`, `speckit-reasoner.md`) and workflow skills (`speckit-orchestrate/SKILL.md`, `speckit-roadmap/SKILL.md`), replacing them with dynamic runtime deference to `.specify/memory/constitution.md` and `.specify/memory/coding-standards.md`.
- **Rationale**:
  1. **Multi-Repository Portability**: Spec Kit is a portable governance and orchestration toolkit distributed across diverse repositories via `bootstrap-speckit.{sh,ps1}`. While `spec-kit-testing` ratifies static verification with zero automated tests in `.specify/memory/constitution.md`, downstream target repositories may ratify `MODULE-B` (100% branch coverage gate) or standard unit/integration test suites.
  2. **Single Authoritative State (Principle IV)**: The project's ratified `.specify/memory/constitution.md` is the single source of truth for verification policy. Baking one repository's Principle III choice into reusable agent system prompts violates Principle IV and prevents subagents from honoring target repository constitutions.
  3. **Runtime Policy Transmission**: During Stage 3 (`Governance Suite Adherence & Principle III Enforcement`) of `/speckit-orchestrate`, the orchestrator reads `.specify/memory/constitution.md` and `.specify/memory/coding-standards.md`, extracts the active Principle III verification policy (whether static verification with a skip allowlist or required automated test suites/coverage gates), and injects that active policy into the subagent dispatch directive.
- **Alternatives Considered**:
  - *Keep static-only rule in agent profiles and require users to edit `.agents/agents/*.md` per repo*: Rejected because modifying managed agent profiles triggers `SKIP_DRIFTED` warnings on `/speckit-bootstrap --upgrade` and duplicates governance state that already lives in `.specify/memory/constitution.md`.
  - *Remove Principle III references from agent profiles altogether*: Rejected because subagents still need explicit instruction to inspect and strictly enforce whatever Principle III verification gate the project constitution ratifies.

---

### Decision 3: Dual-Environment Bootstrapper Seeding & Line-Budget Discipline (`< 150 LOC`)

- **Decision**: Update `bootstrap-speckit.sh` and `bootstrap-speckit.ps1` to validate and copy `.specify/`, `.agents/`, and `.claude/` while preserving the `< 150 LOC` script ceiling established in Phase 4 (`ROADMAP.md`) and enforcing `PRESERVE_USER_STATE` boundaries across both client trees.
- **Rationale**:
  1. **Complete Out-of-the-Box Seeding**: Extending the source bundle verification array and file traversal loop (`find .specify .agents .claude` in Bash; `Get-ChildItem` across `.specify`, `.agents`, `.claude` in PowerShell) seeds both client environments in a single pass.
  2. **Local Profile Protection (`PRESERVE_USER_STATE` & `.gitignore`)**: Excluding `.agents/agents/*.local.md` and `.claude/agents/*.local.md` from file copy operations and ensuring both ignore patterns exist in `<target-repo>/.gitignore` (and the source repository's `.gitignore`) protects machine-local subagent overrides in both environments.
  3. **Concise Implementation**: Both scripts are currently ~130 lines and can easily incorporate `.claude/` asset verification, copying, counters (`CLAUDE_COUNT` / `$ClaudeCount`), and `.gitignore` pattern checks within ~140–145 lines.
- **Alternatives Considered**:
  - *Separate `bootstrap-claude.sh` script*: Rejected because maintaining separate scripts fragments the bootstrap workflow and violates the single-command onboarding design.

---

### Decision 4: Dual-Client Integration Manifest Architecture

- **Decision**: Introduce `.specify/integrations/claude.manifest.json` (mirroring the structure of `agy.manifest.json` with `"integration": "claude"` and `"version": "1.4.0"`) and update `.specify/integrations/speckit-bootstrap.manifest.json` to record SHA-256 digests and byte sizes for all `.specify/`, `.agents/`, and `.claude/` managed files (including `claude.manifest.json`).
- **Rationale**:
  1. **Symmetric Client Verification**: `agy.manifest.json` tracks the 14 Antigravity client files (2 agent profiles + 12 skills). Adding `claude.manifest.json` for the 14 Claude Code client files provides symmetric manifest verification for `/speckit-bootstrap --check`.
  2. **Unified Bootstrapper Tracking**: Including all `.claude/` files (`tier: "agent"` and `tier: "skill"`) and `.specify/integrations/claude.manifest.json` (`tier: "metadata"`) in `speckit-bootstrap.manifest.json` enables the 6-state file classification engine (`CREATE`, `UPGRADE`, `PRESERVE_USER_STATE`, `SKIP_DRIFTED`, `REMOVE_OBSOLETE`, `UNCHANGED`) to manage upgrades across both client trees seamlessly.
- **Alternatives Considered**:
  - *Merge `agy.manifest.json` and `claude.manifest.json` into a single client manifest*: Rejected to preserve backward compatibility with existing Spec Kit `agy` integration metadata and `FR-004` / `FR-005` requirements.

---

### Decision 5: Environment-Aware Path Resolution in `speckit-orchestrate` and `speckit-bootstrap`

- **Decision**: Update `.agents/skills/speckit-orchestrate/SKILL.md` (and its `.claude/` mirror) so the 5-level Agent Profile Hierarchy and stage skill references support both `.agents/` and `.claude/` client roots (resolving from `.claude/` when invoked in Claude Code or `.agents/` in Antigravity, while keeping both mirrored in the repository). Update `.agents/skills/speckit-bootstrap/SKILL.md` (and its `.claude/` mirror) to inspect, verify, and synchronize both `.agents/` and `.claude/` trees and manifests.
- **Rationale**:
  1. **Byte-Identical Skill Parity (`SC-001`)**: Using dual-aware path documentation (e.g., `.agents/agents/` or `.claude/agents/`, `.agents/skills/` or `.claude/skills/`) allows each `SKILL.md` and agent profile to remain 100% byte-identical between `.agents/` and `.claude/` while giving clear, accurate instructions whether executed by Claude Code or Google Antigravity.
- **Alternatives Considered**:
  - *Maintain different file contents in `.claude/` vs `.agents/`*: Rejected because `SC-001` explicitly requires byte-identical content across matching files in `.agents/` and `.claude/`.
