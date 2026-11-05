# Feature Specification: Claude Discovery Compatibility & Constitutional Test Decoupling

<!--
Template Resolution Hierarchy Specification:
This template is resolved by agent skills using the native 4-tier template resolution hierarchy:
- Tier 1 (Overrides): .specify/templates/overrides/spec-template.md
- Tier 2 (Presets): .specify/presets/<preset-id>/templates/spec-template.md (evaluated per .specify/presets/.registry sorted ascending by priority; strategy: replace, prepend, append, wrap)
- Tier 3 (Extensions): .specify/extensions/<ext-id>/templates/spec-template.md (evaluated per .specify/extensions/.registry sorted ascending by priority)
- Tier 4 (Core Fallback): .specify/templates/spec-template.md

Invariant: If a requested template is not found in any of the 4 tiers, the agent MUST fail closed and emit an error per Principle II.
-->

**Feature Branch**: `007-claude-discovery-governance-decoupling`

**Created**: 2026-11-05

**Status**: Draft

**Input**: User description: "Getting some feedback from my work PC with claude. A lot of the skills are in the wrong location for Claude to discover them. It noted that the orchestrate agent/skills include rules to not write tests; that should just follow the constitution, not be a part of the agent"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Claude Code Skill & Subagent Discovery Compatibility (Priority: P1)

Developers and platform engineers using Claude Code CLI need Spec Kit skills and subagent profiles located in `.claude/` (`.claude/skills/<skill-name>/SKILL.md` and `.claude/agents/<agent-name>.md`) alongside `.agents/` so Claude Code automatically discovers and registers all skills and subagent personas upon opening a repository.

**Why this priority**: Currently, Spec Kit only populates `.agents/` (designed for Google Antigravity). When developers open a repository in Claude Code on their work PC or local environment, Claude Code fails to discover any of the 12 Spec Kit skills or subagent profiles. Establishing native `.claude/` discovery compatibility and updating the bootstrapper scripts (`bootstrap-speckit.sh` and `bootstrap-speckit.ps1`) ensures out-of-the-box functionality for both Claude Code and Antigravity.

**Independent Test**: Can be fully tested by verifying that all 12 skills and both agent profiles exist in both `.agents/` and `.claude/`, running `bootstrap-speckit.sh` and `bootstrap-speckit.ps1` against a target directory, and confirming that both `.agents/` and `.claude/` are populated with verified checksums and `.gitignore` entries for local profiles.

**Acceptance Scenarios**:

1. **Given** a repository with Spec Kit installed, **When** opened by a developer running Claude Code, **Then** Claude Code discovers all 12 Spec Kit skills in `.claude/skills/<skill-name>/SKILL.md` and subagent profiles in `.claude/agents/<agent-name>.md`.
2. **Given** `bootstrap-speckit.sh` and `bootstrap-speckit.ps1`, **When** executed against a target repository, **Then** both `.agents/` and `.claude/` directories are seeded with their respective skills and subagent definitions, skipping existing files unless `--force` is specified.
3. **Given** a target repository's `.gitignore`, **When** bootstrapped by either script, **Then** `.gitignore` includes entries ignoring local agent profiles for both environments (`.agents/agents/*.local.md` and `.claude/agents/*.local.md`).
4. **Given** the manifest suite under `.specify/integrations/`, **When** checked via `/speckit-bootstrap --check`, **Then** a dedicated `claude.manifest.json` tracks `.claude/` assets and `speckit-bootstrap.manifest.json` tracks both client environments without drift.

---

### User Story 2 - Dynamic Constitutional Deference for Verification & Testing (Priority: P2)

Spec Kit users and orchestrator subagents across diverse projects need agent profiles (`speckit-executor.md`, `speckit-reasoner.md`) and workflow skills (`speckit-orchestrate/SKILL.md`, `speckit-roadmap/SKILL.md`) to dynamically obey `.specify/memory/constitution.md` (and companion standards) rather than baking hardcoded prohibitions against automated tests into reusable agent personas and skill instructions.

**Why this priority**: Reusable agent profiles and skills must remain portable across repositories. Some repositories adopt static verification with zero automated tests (as in this testing repository), while others enforce unit test coverage gates (`MODULE-B`) or standard test suites. Hardcoding "ZERO automated test files, test directories, or test tasks" directly into agent definitions and orchestrator prompts violates modularity and prevents the toolkit from being used in projects that require automated tests. Deferring dynamically to the project's ratified constitution restores architectural integrity.

**Independent Test**: Can be fully tested by inspecting `.agents/agents/{speckit-executor,speckit-reasoner}.md`, `.claude/agents/{speckit-executor,speckit-reasoner}.md`, `.agents/skills/speckit-orchestrate/SKILL.md`, and `.claude/skills/speckit-orchestrate/SKILL.md`, confirming that zero hardcoded test prohibitions remain, and verifying that the orchestrator dynamically reads `.specify/memory/constitution.md` at runtime to formulate verification directives.

**Acceptance Scenarios**:

1. **Given** the subagent profiles (`speckit-executor.md` and `speckit-reasoner.md`), **When** reviewed for governance instructions, **Then** Principle III mandates dynamic obedience to the project's ratified `.specify/memory/constitution.md` and companion standards, with no hardcoded assertions banning automated tests or test frameworks.
2. **Given** `/speckit-orchestrate` preparing stage directives and subagent dispatch payloads, **When** formulating the governance instructions, **Then** it dynamically reads `.specify/memory/constitution.md` and transmits the project's active Principle III verification rule rather than hardcoding a universal test prohibition.
3. **Given** `/speckit-roadmap` and other workflow skills, **When** evaluated, **Then** general guidelines reference adherence to constitutional verification gateways generally, rather than hardcoding "Principle III (Zero Automated Tests)".
4. **Given** an execution in this repository (`spec-kit-testing`), **When** subagents read `.specify/memory/constitution.md`, **Then** they dynamically observe this repository's ratified policy (static verification without automated tests) through constitutional deference.

---

### User Story 3 - Living Documentation, Manifest Parity & Quality Gates (Priority: P3)

Maintainers, contributors, and onboarding developers need repository documentation (`README.md`, `ROADMAP.md`) and cryptographic manifests (`.specify/integrations/*.manifest.json`) updated to reflect dual Claude/Antigravity discovery and dynamic constitutional deference, verified by static analysis gates.

**Why this priority**: Living documentation must remain in sync with repository capabilities (Principle VII). Documenting Claude Code discovery paths and maintaining cryptographic manifest integrity guarantees that neither documentation drift nor bundle drift occurs.

**Independent Test**: Can be fully tested by verifying that `README.md` documents both `.agents/` and `.claude/` discovery paths, `ROADMAP.md` reflects Phase 7 progress, all SHA-256 digests in `.specify/integrations/` match actual file contents, and `/speckit-bootstrap --check` reports zero drift.

**Acceptance Scenarios**:

1. **Given** the root `README.md`, **When** read by a developer, **Then** it clearly explains dual discovery for Google Antigravity (`.agents/`) and Claude Code (`.claude/`), and details how `bootstrap-speckit.sh` and `bootstrap-speckit.ps1` seed both client directories.
2. **Given** all integration manifests in `.specify/integrations/` (`speckit.manifest.json`, `agy.manifest.json`, `claude.manifest.json`, `speckit-bootstrap.manifest.json`), **When** verified statically, **Then** every file has an accurate SHA-256 checksum matching its current content on disk.
3. **Given** `/speckit-bootstrap --check`, **When** executed in the workspace, **Then** it validates both `.agents/` and `.claude/` installations and reports all files verified with zero drift.

---

### Edge Cases

- **File Synchronization vs Symlinks**: Symlinks are prone to failure across Windows / Git for Windows environments without elevated privileges or `core.symlinks=true`. Therefore, actual mirrored file trees are used in `.claude/` and `.agents/`, with automated parity checking in manifests and bootstrapper.
- **Backward Compatibility for Target Repositories**: Existing repositories bootstrapped prior to Phase 7 only have `.agents/`. When updated via `./bootstrap-speckit.sh <target-repo>`, the bootstrapper seamlessly adds `.claude/` without clobbering existing `.specify/memory/` or user overrides.
- **Projects with Active Automated Tests**: For target repositories adopting Spec Kit where `.specify/memory/constitution.md` specifies unit test requirements or coverage gates, the decoupled agent personas must generate compliant unit tests as mandated by that project's constitution, proving true multi-project portability.
- **Preserving Local Agent Profiles**: User-local agent profiles (`.agents/agents/*.local.md` and `.claude/agents/*.local.md`) must never be copied, overwritten, or tracked in version control.
- **Strict Zero Automated Tests in Current Workspace**: While the agent profiles are made portable, THIS repository's ratified constitution (`.specify/memory/constitution.md`) enforces static verification with zero automated tests; no automated test files, test suites, or test tasks shall be added to `spec-kit-testing`.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The repository MUST establish a `.claude/` asset tree mirroring `.agents/`, providing:
  - `.claude/skills/<skill-name>/SKILL.md` for all 12 Spec Kit skills (`speckit-analyze`, `speckit-bootstrap`, `speckit-checklist`, `speckit-clarify`, `speckit-constitution`, `speckit-converge`, `speckit-implement`, `speckit-orchestrate`, `speckit-plan`, `speckit-roadmap`, `speckit-specify`, `speckit-tasks`).
  - `.claude/agents/<agent-name>.md` for both subagent profiles (`speckit-executor.md`, `speckit-reasoner.md`).
- **FR-002**: `bootstrap-speckit.sh` and `bootstrap-speckit.ps1` MUST be updated to seed both `.agents/` and `.claude/` trees into target repositories, maintaining `PRESERVE_USER_STATE` boundaries (ignoring `*.local.md`, `.specify/memory/*`, `.specify/templates/overrides/*`, `.specify/feature.json`, and root `ROADMAP.md`).
- **FR-003**: `bootstrap-speckit.sh` and `bootstrap-speckit.ps1` MUST ensure target `.gitignore` files contain ignore patterns for local profiles in both environments (`.agents/agents/*.local.md` and `.claude/agents/*.local.md`).
- **FR-004**: A dedicated manifest `.specify/integrations/claude.manifest.json` MUST be created tracking all `.claude/` files and their SHA-256 digests, and `.specify/integrations/speckit-bootstrap.manifest.json` MUST be updated to include all assets across `.specify/`, `.agents/`, and `.claude/`.
- **FR-005**: `.agents/skills/speckit-bootstrap/SKILL.md` (and `.claude/skills/speckit-bootstrap/SKILL.md`) MUST be updated to support checking and verifying both `.agents/` (`agy.manifest.json`) and `.claude/` (`claude.manifest.json`) installations.
- **FR-006**: Subagent profiles (`speckit-executor.md` and `speckit-reasoner.md`) across both `.agents/agents/` and `.claude/agents/` MUST be refactored to remove hardcoded test prohibitions under Principle III, replacing them with dynamic deference:
  - Agents MUST inspect and obey `.specify/memory/constitution.md` and companion standards for all verification, testing, and coverage requirements.
- **FR-007**: `.agents/skills/speckit-orchestrate/SKILL.md` and `.claude/skills/speckit-orchestrate/SKILL.md` MUST be refactored:
  - Section 3 MUST instruct the orchestrator to dynamically read `.specify/memory/constitution.md` to identify the active verification policy.
  - The subagent dispatch prompt payload MUST instruct subagents to enforce the project's ratified constitution dynamically, rather than hardcoding `"specifically Principle III: ZERO automated test files, test directories, or test tasks"`.
- **FR-008**: `.agents/skills/speckit-roadmap/SKILL.md` and `.claude/skills/speckit-roadmap/SKILL.md` MUST be updated so general guidelines reference constitutional verification standards generally rather than hardcoding "Principle III (Zero Automated Tests)".
- **FR-009**: The root `README.md` MUST be updated per Principle VII documentation governance to describe dual Claude Code (`.claude/`) and Antigravity (`.agents/`) discovery, bootstrapper seeding, and dynamic constitutional compliance.
- **FR-010**: All SHA-256 digests across `.specify/integrations/{speckit,agy,claude,speckit-bootstrap}.manifest.json` MUST be fully synchronized to reflect modified and added files.

### Key Entities

- **Claude Client Asset Tree (`.claude/`)**: The directory structure containing `skills/` and `agents/` formatted for discovery by Claude Code CLI.
- **Antigravity Client Asset Tree (`.agents/`)**: The directory structure containing `skills/` and `agents/` formatted for discovery by Google Antigravity.
- **Dynamic Constitutional Deference**: The architectural mechanism whereby agent profiles and orchestrator skills defer testing rules to `.specify/memory/constitution.md` rather than baking project-specific prohibitions into reusable prompts.
- **Dual-Client Integration Manifests**: `.specify/integrations/agy.manifest.json` and `.specify/integrations/claude.manifest.json` providing independent cryptographic integrity for each client's asset set.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of Spec Kit skills (12 skills) and agent profiles (2 profiles) exist in both `.agents/` and `.claude/` with byte-identical content across matching files.
- **SC-002**: Bootstrapper scripts (`bootstrap-speckit.sh` and `bootstrap-speckit.ps1`) successfully seed both `.agents/` and `.claude/` directories into target repositories, verifying integrity of all assets.
- **SC-003**: 0 hardcoded test prohibitions or "zero automated tests" assertions remain in reusable subagent profiles (`speckit-executor.md`, `speckit-reasoner.md`) and orchestrator dispatch instructions; 100% of test behavior defers to `.specify/memory/constitution.md`.
- **SC-004**: All managed files in `.specify/`, `.agents/`, and `.claude/` match the SHA-256 digests recorded in `.specify/integrations/*.manifest.json`.
- **SC-005**: Root `README.md` accurately documents Claude Code discovery alongside Antigravity with zero broken links and zero references to ephemeral spec paths.

## Assumptions

- **Mirrored Dual Directories Over Symlinks**: File mirroring (dual directory trees) is selected over symlinks due to cross-platform reliability on Windows machines where git symlinks frequently fail or require elevated privileges.
- **Claude Code Skill & Agent Structure**: Claude Code discovers skills from `.claude/skills/<skill-name>/SKILL.md` and subagent profiles from `.claude/agents/<agent-name>.md`.
- **Current Workspace Governance Unchanged**: In this repository (`spec-kit-testing`), the active constitution `.specify/memory/constitution.md` continues to enforce Principle III as static verification with zero automated tests; the decoupling ensures the *tooling* does not impose this project's rule on other projects.
- **Local Agent Override Convention**: Local agent overrides continue to use `*.local.md` and are preserved across both `.agents/agents/` and `.claude/agents/`.
