# Feature Specification: Add --update Flag to speckit-orchestrate for Non-Destructive Architectural Replanning

**Feature Branch**: `011-orchestrate-update-flag`

**Created**: 2026-11-06

**Status**: Draft

**Input**: User description: "Add an --update flag to speckit-orchestrate for non-destructive architectural replanning

Implement an --update='<description>' flag (with alias --amend) in speckit-orchestrate to handle systematic architectural updates to existing plans without performing a cold reset:

1. Scope:
   - Keep changes contained to the orchestrator: modify .agents/skills/speckit-orchestrate/SKILL.md and mirror changes to .claude/skills/speckit-orchestrate/SKILL.md.
   - Leave core speckit-plan skill unmodified."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Non-Destructive Architectural Replanning via `--update` / `--amend` Flag (Priority: P1)

As a developer or architect managing an active feature with existing planning artifacts (`spec.md`, `plan.md`, `research.md`, `data-model.md`, `quickstart.md`, `contracts/`, `tasks.md`), I want to invoke `/speckit-orchestrate --update='<description>'` (or alias `--amend='<description>'`) so that the orchestrator surgically amends existing designs and plans to incorporate architectural shifts without wiping out previous progress, research, or completed implementation tasks.

**Why this priority**: When architectural requirements evolve mid-feature, currently users only have `--from=plan` which performs a cold reset or overwrite of planning artifacts. A non-destructive update flag preserves completed work and existing context while adapting the plan.

**Independent Test**: Can be tested by running `/speckit-orchestrate --update='Add Redis caching to session store'` on a feature with existing planning documents and completed tasks in `tasks.md`, verifying that existing files and completed `- [x]` tasks are retained, while `plan.md`, related design docs, and pending tasks in `tasks.md` are updated to reflect the architectural change.

**Acceptance Scenarios**:

1. **Given** an existing feature directory with `spec.md` and `plan.md`, **When** the user runs `/speckit-orchestrate --update='<description>'` or `/speckit-orchestrate --amend='<description>'`, **Then** the orchestrator recognizes the update mode, extracts `<description>`, and executes a non-destructive replanning flow.
2. **Given** an existing feature with completed `- [x]` tasks in `tasks.md`, **When** the orchestrator executes the replanning flow under `--update`, **Then** all completed `- [x]` tasks are preserved intact, and new or revised tasks for the updated architecture are appended or adjusted among pending `- [ ]` tasks.
3. **Given** existing design artifacts (`plan.md`, `research.md`, `data-model.md`, `quickstart.md`, `contracts/`), **When** Stage 3 (`plan`) executes under `--update`, **Then** the orchestrator instructs the planning subagent via its prompt directive to update these artifacts in place rather than re-initializing them from blank templates.

---

### User Story 2 - Fail-Closed Guard on Missing Prerequisites (Priority: P1)

As an engineer or workflow coordinator, I want `/speckit-orchestrate --update` to fail closed immediately if `spec.md` or `plan.md` does not exist in the active feature directory, so that an update operation is never mistakenly executed on an uninitialized feature.

**Why this priority**: Replanning by definition requires existing architectural baselines. Attempting to amend a non-existent plan leads to corrupted state or unintended cold-start side effects.

**Independent Test**: Can be tested by invoking `/speckit-orchestrate --update='New architecture'` when no feature directory exists or when `plan.md` is absent, verifying that execution terminates immediately with a clear rejection error before creating or altering any files.

**Acceptance Scenarios**:

1. **Given** no active feature in `.specify/feature.json` or a feature directory lacking `plan.md`, **When** `/speckit-orchestrate --update='<description>'` is invoked, **Then** the orchestrator halts immediately with a `CRITICAL` boundary rejection error and mutates no files.
2. **Given** a feature directory where `spec.md` is missing, **When** `/speckit-orchestrate --update='<description>'` is invoked, **Then** the orchestrator fails closed before launching any subagents.

---

### User Story 3 - Flexible CLI Flag Parsing and Description Extraction (Priority: P2)

As a developer running the orchestrator from various CLI shells and skill interfaces, I want both `--update` and `--amend` flags supported with either key-value syntax (`--update='...'`, `--update="..."`, `--amend='...'`) or space-separated syntax (`--update <description>`, `--amend <description>`), so that the command behaves predictably across standard shell conventions.

**Why this priority**: Users invoke commands with differing quote styles and parameter spacing; flexible parsing prevents frustrating syntax rejection while ensuring the update description is reliably captured.

**Independent Test**: Can be tested by parsing various argument strings (e.g. `--update='Use PostgreSQL'`, `--update "Use PostgreSQL"`, `--update Use PostgreSQL`, `--amend='Use PostgreSQL'`) and asserting that each variant populates `UPDATE_DESCRIPTION` identically.

**Acceptance Scenarios**:

1. **Given** command arguments containing `--update='<description>'` or `--update="<description>"`, **When** argument parsing runs, **Then** `UPDATE_DESCRIPTION` is set to `<description>` with surrounding quotes stripped.
2. **Given** command arguments containing `--amend <description>` or `--update <description>`, **When** argument parsing runs, **Then** `UPDATE_DESCRIPTION` captures the full description string.
3. **Given** command arguments containing `--update` or `--amend` without a description (or with whitespace only), **When** argument parsing runs, **Then** the orchestrator fails closed with a clear error indicating that an update description is required.

---

### User Story 4 - Multi-Stage Subagent Payload Propagation and Checkpoint Policy (Priority: P2)

As an orchestrator managing subagent delegations, I want the update description and amend instructions injected into subagent dispatch payloads across Stages 1 through 5, and I want the pipeline to pause cleanly at the Pre-Implementation Checkpoint after Stage 5 (`analyze`) unless `--continue` is supplied, so that human reviewers can inspect the updated architecture before code implementation begins.

**Why this priority**: Core skills such as `speckit-plan/SKILL.md` must remain general-purpose and unmodified. Passing specialized update directives in subagent prompts enables dynamic behavior modification while maintaining toolchain isolation and human oversight.

**Independent Test**: Can be tested by verifying that subagent directives generated during `--update` runs include the `UPDATE_DESCRIPTION` and explicit non-destructive editing instructions, and that execution halts cleanly at `PAUSED_AT_CHECKPOINT` after `analyze` when `--continue` is omitted.

**Acceptance Scenarios**:

1. **Given** an active `--update` run, **When** Stage 3 (`plan`) subagent (`speckit-reasoner`) is dispatched, **Then** its prompt payload instructs in-place non-destructive architectural replanning referencing `UPDATE_DESCRIPTION`, without modifying `speckit-plan/SKILL.md`.
2. **Given** an active `--update` run, **When** Stage 4 (`tasks`) subagent (`speckit-executor`) is dispatched, **Then** its prompt payload instructs preserving completed tasks (`- [x]`) and updating pending tasks (`- [ ]`) or appending an update phase.
3. **Given** an active `--update` run without `--continue`, **When** Stage 5 (`analyze`) finishes cross-artifact verification, **Then** the orchestrator pauses execution with `PAUSED_AT_CHECKPOINT`, presenting the amended plan and task summary for human review.
4. **Given** an active `--update` run with `--continue`, **When** Stage 5 (`analyze`) completes, **Then** the orchestrator continues into Stage 6 (`implement`) and Stage 7 (`converge`).

---

### User Story 5 - Dual-Client Skill Parity (.agents and .claude) (Priority: P3)

As a team using multiple AI development environments (Google Antigravity and Claude Code), I want the `--update` / `--amend` feature implemented identically across `.agents/skills/speckit-orchestrate/SKILL.md` and `.claude/skills/speckit-orchestrate/SKILL.md`, so that behavior is consistent across both platforms.

**Why this priority**: Discrepancies between agent runtime configurations cause subtle bugs and cross-platform drift. Maintaining strict parity ensures reliable behavior everywhere.

**Independent Test**: Can be tested by comparing the argument parsing, validation rules, subagent directives, and stage flow definitions between `.agents/skills/speckit-orchestrate/SKILL.md` and `.claude/skills/speckit-orchestrate/SKILL.md` to confirm complete parity.

**Acceptance Scenarios**:

1. **Given** `.agents/skills/speckit-orchestrate/SKILL.md` updated with `--update` support, **When** compared with `.claude/skills/speckit-orchestrate/SKILL.md`, **Then** both files define identical flags, validation logic, subagent prompt templates, and execution state machine transitions.

---

### Edge Cases

- **Missing spec.md or plan.md**: If `--update` is supplied but either `spec.md` or `plan.md` is absent, the orchestrator MUST fail closed with a `CRITICAL` error and reject execution before modifying any files.
- **Empty Update Description**: If `--update` or `--amend` is passed with an empty string or whitespace (e.g., `--update=""` or `--amend "   "`), the orchestrator MUST reject the operation immediately with an informative message.
- **Precedence with `--from`**: If both `--update` and `--from` are passed, `--update` semantics govern artifact preservation (preventing file deletion or cold overwrite), while `--from` designates the starting stage.
- **Preserving Completed Implementation Tasks**: If `tasks.md` contains completed `- [x]` items from earlier work, the Stage 4 tasks pass MUST retain all `- [x]` markers and task lines untouched, appending new phases or adjusting remaining `- [ ]` tasks only.
- **Core Skill Immutability**: Neither `.agents/skills/speckit-plan/SKILL.md` nor `.claude/skills/speckit-plan/SKILL.md` may be modified to support replanning; all non-destructive instructions are conveyed through subagent dispatch payloads.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The orchestrator MUST support `--update='<description>'`, `--update="<description>"`, `--update <description>`, `--amend='<description>'`, `--amend="<description>"`, and `--amend <description>` CLI argument syntax, parsing `<description>` into an `UPDATE_DESCRIPTION` context variable.
- **FR-002**: If `--update` or `--amend` is passed with an empty description, the orchestrator MUST fail closed before mutating any state or dispatching subagents, logging a `CRITICAL` diagnostic.
- **FR-003**: The orchestrator MUST verify that both `spec.md` and `plan.md` exist in the resolved `SPECIFY_FEATURE_DIRECTORY` before proceeding with an `--update` or `--amend` execution; if either file is missing, it MUST fail closed immediately.
- **FR-004**: In `--update` mode, the orchestrator MUST preserve existing feature artifacts (`spec.md`, `plan.md`, `research.md`, `data-model.md`, `quickstart.md`, `contracts/`, `tasks.md`) rather than wiping or cold-resetting them.
- **FR-005**: In `--update` mode, if the update description indicates requirement-level modifications, the orchestrator MUST instruct an amendment pass to update `spec.md` in place to reflect the new requirements.
- **FR-006**: In `--update` mode, the orchestrator MUST dispatch Stage 3 (`plan`) with a specialized subagent prompt directive instructing `speckit-reasoner` to perform surgical, in-place updates to `plan.md`, `research.md`, `data-model.md`, `quickstart.md`, and `contracts/` based on `UPDATE_DESCRIPTION`.
- **FR-007**: Core planning skill files (`.agents/skills/speckit-plan/SKILL.md` and `.claude/skills/speckit-plan/SKILL.md`) MUST remain unmodified; replanning logic MUST be passed entirely via subagent prompt payloads.
- **FR-008**: In `--update` mode, the orchestrator MUST dispatch Stage 4 (`tasks`) with a prompt directive instructing `speckit-executor` to preserve all completed `- [x]` checklist tasks while updating pending `- [ ]` tasks or appending a new phase for the updated architecture.
- **FR-009**: In `--update` mode, Stage 5 (`analyze`) MUST perform cross-artifact consistency analysis across the amended `spec.md`, `plan.md`, and `tasks.md`, running self-healing remediation if drift is detected.
- **FR-010**: In `--update` mode, the orchestrator MUST halt at the Pre-Implementation Checkpoint after Stage 5 (`analyze`) unless `--continue` (or aliases `--continuous`, `--no-pause`, `--auto-implement`) is explicitly provided.
- **FR-011**: The orchestrator skill files in both `.agents/skills/speckit-orchestrate/SKILL.md` and `.claude/skills/speckit-orchestrate/SKILL.md` MUST be updated with identical logic, maintaining complete dual-client parity.
- **FR-012**: If the repository root `README.md` documents orchestrator commands and flags, it MUST be updated to include `--update` / `--amend` usage in compliance with Principle VII.

### Key Entities *(include if feature involves data)*

- **Orchestrator Skill Definition**: Workflow instructions in `.agents/skills/speckit-orchestrate/SKILL.md` and `.claude/skills/speckit-orchestrate/SKILL.md` defining argument parsing, execution stages, and dispatch directives.
- **Update Directive / Description**: The parameter value `UPDATE_DESCRIPTION` representing the architectural change to be applied systematically across planning artifacts.
- **Feature Design Artifact Set**: The collection of markdown and contract files (`spec.md`, `plan.md`, `research.md`, `data-model.md`, `quickstart.md`, `contracts/`, `tasks.md`) within `SPECIFY_FEATURE_DIRECTORY` amended in place.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of valid `--update` and `--amend` syntax variations (`--update='...'`, `--update "..."`, `--update ...`, `--amend='...'`, `--amend "..."`, `--amend ...`) are parsed successfully into `UPDATE_DESCRIPTION`.
- **SC-002**: 100% of completed `- [x]` task entries in `tasks.md` are preserved during `--update` replanning execution.
- **SC-003**: 100% of `--update` invocations lacking an existing `plan.md` or `spec.md` fail closed immediately without modifying any files.
- **SC-004**: Stage 3 subagent dispatch payload successfully guides surgical replanning with 0 modifications to `speckit-plan/SKILL.md`.
- **SC-005**: 100% parity between `.agents/skills/speckit-orchestrate/SKILL.md` and `.claude/skills/speckit-orchestrate/SKILL.md`.
- **SC-006**: Default pre-implementation pause is respected after Stage 5 (`analyze`) during `--update` replanning unless `--continue` is specified.

## Assumptions

- Users provide an informative natural language summary when passing `--update='<description>'` or `--amend='<description>'`.
- The active feature directory is determined via `SPECIFY_FEATURE_DIRECTORY` or `.specify/feature.json`.
- Completed tasks in `tasks.md` indicate code or design work already delivered and must not be discarded or marked incomplete during architectural replanning.
- In accordance with Constitution Principle III, all verification is conducted through static inspection, syntax checking, and declarative quality gates without generating automated test suites.
- Subagents (`speckit-reasoner` and `speckit-executor`) have sufficient model capabilities to interpret prompt payload directives and perform surgical, non-destructive file updates.
