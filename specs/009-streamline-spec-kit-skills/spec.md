# Feature Specification: Streamline Spec Kit Skills & Decouple Bloat

**Feature Branch**: `009-streamline-spec-kit-skills`  
**Created**: 2026-11-05  
**Status**: Draft  
**Input**: User description: "Streamline Spec Kit skills by pruning redundant 4-tier template resolution text, removing hardcoded Docs Gate logic, making companion governance suite loading lazy/selective, and removing redundant Principle III dynamic extraction blocks"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Prune Redundant Template Resolution Prompts (Priority: P1)

As a developer or AI agent using Spec Kit, I want skill prompts (`speckit-specify`, `speckit-plan`, `speckit-tasks`, `speckit-checklist`) to resolve templates concisely without carrying 20-30 lines of duplicate algorithmic lookup text in every prompt.

**Why this priority**: Eliminates hundreds of lines of prompt duplication across `.agents/skills` and `.claude/skills`, speeding up agent execution and reducing token overhead.

**Independent Test**: Verify that `speckit-specify`, `speckit-plan`, `speckit-tasks`, and `speckit-checklist` locate templates without verbatim repetition of the 4-tier algorithm, and confirm all commands resolve templates cleanly.

**Acceptance Scenarios**:
1. **Given** a skill requiring a template (e.g. `speckit-specify`), **When** the skill runs, **Then** it references standard template discovery concisely without verbose multi-paragraph boilerplate.
2. **Given** template resolution in all four skills, **When** inspected across `.agents/` and `.claude/`, **Then** line count is significantly reduced while functional template discovery remains intact.

---

### User Story 2 - Decouple Documentation Gate from Skills to Constitution (Priority: P1)

As a developer, I want documentation updates (e.g., updating `README.md`) to be governed purely by the project's ratified `constitution.md` rather than hardcoded logic blocks (`Documentation Impact: USER_FACING vs INTERNAL_ONLY`) embedded inside 6 individual skill files (`plan`, `tasks`, `analyze`, `implement`, `converge`, `constitution`).

**Why this priority**: Eliminates artificial coupling where modifying documentation rules requires editing every command file in the toolkit. Restores the core principle of Spec Kit that the constitution is the single source of truth for engineering mandates.

**Independent Test**: Verify that skill files no longer contain hardcoded `Documentation Impact` classification blocks, while `constitution.md` continues to mandate documentation updates for user-facing changes.

**Acceptance Scenarios**:
1. **Given** `speckit-plan`, `speckit-tasks`, `speckit-analyze`, `speckit-implement`, and `speckit-converge`, **When** inspected, **Then** hardcoded `Documentation Impact` branches are removed.
2. **Given** `constitution.md`, **When** any user-facing feature is implemented, **Then** the constitution's Principle VII naturally mandates documentation updates without needing skill-level code duplication.

---

### User Story 3 - Selective & Lazy Governance Context Loading (Priority: P1)

As an AI agent running a Spec Kit stage, I want skills to load only the governance files relevant to my current stage, rather than eagerly loading all three files (`constitution.md`, `coding-standards.md`, `logging-standards.md`) in every skill.

**Why this priority**: Fulfills the original purpose of splitting governance files: reducing context window usage and avoiding irrelevant prompt bloat in early stages.

**Independent Test**: Verify that `speckit-specify` and `speckit-clarify` load only `constitution.md`, while `speckit-implement` loads `coding-standards.md` and `logging-standards.md`.

**Acceptance Scenarios**:
1. **Given** `speckit-specify` and `speckit-clarify`, **When** invoked, **Then** they load only `.specify/memory/constitution.md` for high-level principles.
2. **Given** `speckit-plan` and `speckit-tasks`, **When** invoked, **Then** they load `constitution.md` and only relevant architectural portions of `coding-standards.md`.
3. **Given** `speckit-implement`, **When** invoked, **Then** it loads `coding-standards.md` and `logging-standards.md` for code-level execution rules.

---

### User Story 4 - Remove Redundant Principle III Extraction Blocks (Priority: P2)

As a developer, I want skill files to rely on upstream's built-in "Tests are OPTIONAL" rule and constitution deference, rather than carrying redundant "Dynamic Principle III Policy Resolution" blocks in every command.

**Why this priority**: Upstream Spec Kit already defers to the constitution and treats tests as optional unless mandated. Removing custom extraction blocks further trims skill files.

**Independent Test**: Verify that `speckit-tasks` and `speckit-orchestrate` cleanly defer to the constitution without repetitive dynamic policy extraction boilerplate.

**Acceptance Scenarios**:
1. **Given** `speckit-tasks`, **When** generating tasks, **Then** it follows the constitution without redundant extraction blocks.
2. **Given** a testless or test-required constitution, **When** tasks are generated, **Then** it correctly obeys the active constitution.

---

### User Story 5 - Dual-Client Parity & Manifest Synchronization (Priority: P1)

As a maintainer, I want `.agents/` and `.claude/` skill files to remain in 100% byte parity, with updated checksums and byte counts reflected across all integration manifests.

**Why this priority**: Guarantees that users on both Google Antigravity and Claude Code receive identical, verified behaviors.

**Independent Test**: Run `diff -r .agents/skills .claude/skills` and verify zero differences; verify manifest integrity.

**Acceptance Scenarios**:
1. **Given** the streamlined skills in `.agents/skills`, **When** compared with `.claude/skills`, **Then** `diff -r .agents/skills .claude/skills` returns exit code 0 (identical).
2. **Given** `.specify/integrations/` manifests, **When** verified, **Then** file sizes and SHA-256 hashes match the streamlined files.

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Trim redundant 4-tier template resolution text in `speckit-specify`, `speckit-plan`, `speckit-tasks`, and `speckit-checklist`, replacing with concise template lookup instructions.
- **FR-002**: Remove hardcoded `Documentation Impact` gate instructions from `speckit-plan`, `speckit-tasks`, `speckit-analyze`, `speckit-implement`, and `speckit-converge`.
- **FR-003**: Refactor governance loading in `speckit-specify` and `speckit-clarify` to load only `constitution.md`.
- **FR-004**: Refactor governance loading in `speckit-plan` and `speckit-tasks` to load `constitution.md` and relevant parts of `coding-standards.md`.
- **FR-005**: Ensure `speckit-implement` retains full access to `coding-standards.md` and `logging-standards.md`.
- **FR-006**: Trim redundant Principle III dynamic policy extraction boilerplate from `speckit-tasks`, `speckit-plan`, and `speckit-orchestrate`.
- **FR-007**: Mirror all trimmed skill changes with 100% byte parity from `.agents/skills/` to `.claude/skills/`.
- **FR-008**: Update SHA-256 digests and file sizes in `.specify/integrations/agy.manifest.json`, `claude.manifest.json`, and `speckit-bootstrap.manifest.json`.

### Non-Functional Requirements

- **NFR-001**: Zero breaking changes to existing Spec Kit functionality; all standard commands must continue to function.
- **NFR-002**: Pure static verification; zero linter warnings and exact byte parity.
- **NFR-003**: Net reduction of at least 300 lines of prompt overhead across skills.

---

## Success Criteria *(mandatory)*

- **SC-001**: `diff -r .agents/skills .claude/skills` reports no differences.
- **SC-002**: All 12 skill files pass syntax and structural checks.
- **SC-003**: Manifests accurately reflect updated SHA-256 hashes.
- **SC-004**: Total prompt size across skill files reduced by at least 15%.
