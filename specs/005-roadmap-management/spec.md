# Feature Specification: Roadmap Management (`speckit-roadmap`)

<!--
Template Resolution Hierarchy Specification:
This template is resolved by agent skills using the native 4-tier template resolution hierarchy:
- Tier 1 (Overrides): .specify/templates/overrides/spec-template.md
- Tier 2 (Presets): .specify/presets/<preset-id>/templates/spec-template.md (evaluated per .specify/presets/.registry sorted ascending by priority; strategy: replace, prepend, append, wrap)
- Tier 3 (Extensions): .specify/extensions/<ext-id>/templates/spec-template.md (evaluated per .specify/extensions/.registry sorted ascending by priority)
- Tier 4 (Core Fallback): .specify/templates/spec-template.md

Invariant: If a requested template is not found in any of the 4 tiers, the agent MUST fail closed and emit an error per Principle II.
-->

**Feature Branch**: `005-roadmap-management`

**Created**: 2026-11-05

**Status**: Draft

**Input**: User description: "Use a worktree, next roadmap phase"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Standardized Roadmap Template & Guided Roadmap Authoring via `/speckit-roadmap` (Priority: P1)

Project leads, architects, and maintainers planning multi-phase initiatives need a standardized roadmap template (`roadmap-template`) resolved through Spec Kit's 4-tier template hierarchy and a dedicated `/speckit-roadmap` skill that scaffolds, structures, and incrementally evolves `ROADMAP.md` with clear phases, goals, prerequisites, deliverables, status markers, and key design decisions.

**Why this priority**: Spec Kit features currently begin at the single-feature level (`spec.md`), leaving multi-feature strategic planning in an unstructured, manually edited `ROADMAP.md`. Providing a canonical `roadmap-template` (both in core templates and the `base-governance` preset) and a guided authoring workflow in `/speckit-roadmap` establishes a single, repeatable schema for strategic planning before any tactical specifications are generated.

**Independent Test**: Can be fully tested by resolving `roadmap-template` across the 4-tier template hierarchy, running `/speckit-roadmap` to scaffold or upgrade `ROADMAP.md` (including adding or updating phases), and verifying that the resulting `ROADMAP.md` contains the canonical Overview of Initiatives table (with explicit `Status`, `Prerequisites`, and `Spec` columns) and structured per-phase sections (`Problem Statement`, `Architectural Fit in Spec Kit`, `Prerequisites & Dependencies`, `Key Deliverables`, and `Key Design Decisions to Resolve During Spec`).

**Acceptance Scenarios**:

1. **Given** a repository without an existing `ROADMAP.md` (or with an unstructured roadmap), **When** a user invokes `/speckit-roadmap` with high-level project goals or asks to migrate the existing roadmap to the standard schema, **Then** the skill resolves `roadmap-template` via the 4-tier template hierarchy and generates or updates `ROADMAP.md` with sequential phases, status markers (`PLANNED`, `IN_PROGRESS`, `COMPLETED`, `DEFERRED`), prerequisite declarations, key deliverables, and per-phase problem statements without losing any existing roadmap content.
2. **Given** an existing `ROADMAP.md` conforming to the roadmap schema, **When** a user invokes `/speckit-roadmap --add "<initiative description>"` (or requests adding/reordering phases), **Then** the skill appends or inserts the new phase into both the Overview of Initiatives table and the detailed phase sections while preserving existing phase numbering, status history, and custom prose.
3. **Given** a project that has customized its roadmap structure via `.specify/templates/overrides/roadmap-template.md`, **When** `/speckit-roadmap` resolves `roadmap-template`, **Then** it honors Priority 1 (`overrides`) ahead of Priority 2 (`presets/base-governance`) and Priority 4 (`templates/roadmap-template.md`).

---

### User Story 2 - Automated Roadmap Status Audit, Drift Detection & Reconciliation (Priority: P2)

Maintainers and AI agents inspecting an active repository need `/speckit-roadmap --status` (and `--check` / `--sync`) to automatically audit all declared phases in `ROADMAP.md` against actual feature artifacts in `specs/` and version-control history, surface any status drift between `ROADMAP.md` and the codebase, and reconcile `ROADMAP.md` statuses deterministically.

**Why this priority**: As features progress through specification, planning, task generation, and implementation, `ROADMAP.md` quickly falls out of sync with reality unless someone manually edits it. Automated status reconciliation ensures humans and agents can immediately see which phases are completed, which are actively in progress (including inside git worktrees), which are blocked on prerequisites, and which phase is ready to execute next.

**Independent Test**: Can be fully tested by invoking `/speckit-roadmap --status` and `/speckit-roadmap --check` against this repository (where Phases 1–4 have completed specs/commits and Phase 5–6 are defined) and verifying that the skill accurately maps `specs/001-*` through `specs/004-*` to Phases 1–4, detects any mismatch between `ROADMAP.md` status markers and repository evidence as `STATUS_DRIFT`, and updates `ROADMAP.md` cleanly when `--sync` is requested.

**Acceptance Scenarios**:

1. **Given** a repository with `ROADMAP.md` and feature directories under `specs/`, **When** a user runs `/speckit-roadmap --status` (or `/speckit-roadmap --check`), **Then** the skill inspects `ROADMAP.md`, `specs/NNN-*` (`spec.md`, `plan.md`, `tasks.md` completion checkboxes), active branches/worktrees, and commit history, and outputs a structured phase-by-phase status table showing Declared Status, Inferred Evidence Status, Linked Spec Directory, Prerequisite Readiness, and Drift Status (`SYNCED` or `STATUS_DRIFT`) without modifying any files on disk.
2. **Given** a repository where one or more roadmap phases have `STATUS_DRIFT` (for example, a phase is marked `PLANNED` or lacks a status marker in `ROADMAP.md`, but its corresponding feature in `specs/NNN-*` has all tasks completed and committed), **When** the user runs `/speckit-roadmap --sync`, **Then** the skill updates the status markers and spec links in `ROADMAP.md` to match the verified repository evidence while preserving all narrative descriptions.
3. **Given** a `ROADMAP.md` with structural defects (such as a phase present in the Overview table but missing its detailed section, duplicate phase identifiers, or a reference to a nonexistent prerequisite phase), **When** `/speckit-roadmap --check` executes, **Then** it fails closed with `WARN` diagnostics identifying each structural or referential defect and line/section location.

---

### User Story 3 - Seamless Handoff from Roadmap Phase to `/speckit-specify` (Priority: P3)

Developers and autonomous agents starting the next body of work need `/speckit-roadmap --next` (or `/speckit-roadmap --specify <phase>`) to automatically identify the next eligible `PLANNED` roadmap phase whose prerequisites are satisfied, extract its complete problem statement, architectural context, deliverables, and design questions, and seed a new `/speckit-specify` feature specification (optionally inside an isolated git worktree).

**Why this priority**: Manually copying context from `ROADMAP.md` into `/speckit-specify` is error-prone and loses important architectural constraints or design questions captured during strategic planning. Direct handoff turns `ROADMAP.md` into an executable strategic queue that feeds Spec Kit's feature pipeline.

**Independent Test**: Can be fully tested by running `/speckit-roadmap --next` (or selecting a target phase) and verifying that the skill selects the earliest `PLANNED` phase with completed prerequisites, transitions that phase's status in `ROADMAP.md` to `IN_PROGRESS` with its resolved `specs/NNN-<short-name>` link, and invokes `/speckit-specify` with the phase's full structured context.

**Acceptance Scenarios**:

1. **Given** a `ROADMAP.md` where Phases 1–4 are `COMPLETED` and Phases 5 and 6 are `PLANNED`, **When** a user invokes `/speckit-roadmap --next` (or `/speckit-specify next roadmap phase`), **Then** the workflow deterministically selects Phase 5 as the next eligible phase, extracts its `Problem Statement`, `Architectural Fit`, `Key Deliverables`, and `Key Design Decisions`, and initiates `/speckit-specify` using that context.
2. **Given** a user requesting `/speckit-roadmap --specify <phase-id>` where the requested phase declares a prerequisite phase that is not yet `COMPLETED`, **When** the skill evaluates eligibility, **Then** it halts before creating a spec, emits a `WARN` boundary rejection identifying the unfulfilled prerequisite phase(s), and asks for explicit confirmation (`--force`) before proceeding.
3. **Given** a repository using the portable project bootstrapper (`bootstrap-speckit.sh`, `bootstrap-speckit.ps1`, and `/speckit-bootstrap`), **When** a target repository is seeded or upgraded, **Then** `roadmap-template.md` and `.agents/skills/speckit-roadmap/SKILL.md` are included in the managed bundle and manifest while `ROADMAP.md` at the repository root is protected as project-owned user state.

---

### Edge Cases

- **Missing or Empty `ROADMAP.md` During Audit or Handoff**: If a user invokes `/speckit-roadmap --status`, `--check`, `--sync`, or `--next` when `ROADMAP.md` does not exist or contains zero phases, the skill MUST fail closed at the boundary, emit a `WARN` message explaining that no roadmap exists at `ROADMAP.md`, and offer to scaffold one from `roadmap-template` instead of guessing or creating empty specs.
- **All Phases Already `COMPLETED` or Blocked on Prerequisites**: If `/speckit-roadmap --next` runs when every phase in `ROADMAP.md` is already `COMPLETED` (or all remaining `PLANNED` phases depend on incomplete prerequisites), the skill MUST report the terminal/blocked state clearly and make zero file mutations.
- **Ambiguous Mapping Between Roadmap Phases and `specs/NNN-*` Directories**: When reconciling existing `specs/NNN-*` directories against `ROADMAP.md` phases that do not yet have explicit spec links, the skill matches by explicit `specs/NNN-*` reference first, then by phase number (`Phase N` ↔ `00N-*`) and normalized initiative keywords; if an ambiguity remains, it reports `AMBIGUOUS_MATCH` in `--status` rather than silently overwriting links.
- **Concurrent Worktree Execution**: When a roadmap phase is being specified or implemented inside an isolated git worktree (e.g., `.worktrees/NNN-<short-name>`), `/speckit-roadmap --status` inspects both the current checkout and active `git worktree list` branches/paths so in-progress worktree phases are accurately recognized as `IN_PROGRESS`.
- **Protection of Project-Owned `ROADMAP.md` During Bootstrap Upgrades**: In compliance with Constitutional Principle VI (*Verify Before Mutate/Destroy*), `ROADMAP.md` at the repository root is project-owned state and MUST NEVER be overwritten or deleted by `bootstrap-speckit.sh`, `bootstrap-speckit.ps1`, or `/speckit-bootstrap --upgrade` / `--force`.
- **Strict Enforcement of Constitutional Principle III (No Automated Tests & Zero Runtime `.specify/scripts/`)**: All roadmap validation, linting, status reconciliation, and specification handoff logic MUST execute natively through the `.agents/skills/speckit-roadmap/SKILL.md` agent skill with zero automated test suites (`tests/`) and zero `.specify/scripts/` runtime script dependencies.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The repository MUST provide a canonical `roadmap-template.md` at `.specify/templates/roadmap-template.md` and in the `base-governance` preset at `.specify/presets/base-governance/templates/roadmap-template.md` (registered in `.specify/presets/base-governance/preset.yml` with `strategy: replace`), defining a standardized structure for project roadmaps:
  - **Header & Governance Metadata**: Project title, roadmap purpose, last-updated date, and usage guidance for Spec Kit integration (`/speckit-roadmap`, `/speckit-specify`, `/speckit-orchestrate`).
  - **Overview of Initiatives Table**: Columns for `Phase`, `Initiative`, `Status` (`PLANNED` | `IN_PROGRESS` | `COMPLETED` | `DEFERRED`), `Prerequisites`, `Spec` (link/path to `specs/NNN-*/` when assigned, or `—`), `Goal`, and `Key Deliverables`.
  - **Detailed Phase Sections**: Standardized `## Phase N: <Initiative Title>` sections containing `### Metadata` (`Status`, `Prerequisites`, `Spec Directory`), `### Problem Statement`, `### Architectural Fit in Spec Kit` (or `### Architectural Fit & Scope`), `### Key Deliverables`, and `### Key Design Decisions to Resolve During Spec`.
- **FR-002**: The repository MUST provide a dedicated, 100% script-free agent skill at `.agents/skills/speckit-roadmap/SKILL.md` (invokable as `/speckit-roadmap`) that resolves `roadmap-template` via Spec Kit's native 4-tier template resolution stack (`overrides` → `presets` → `extensions` → `core`) and supports five operational modes:
  1. **Scaffold / Interactive Authoring Mode (default when invoked with goals or on a missing/unstructured `ROADMAP.md`)**: Creates or restructures `ROADMAP.md` using `roadmap-template` while preserving all existing initiative descriptions and decisions.
  2. **Phase Mutation Mode (`--add`, `--update <phase>`, `--defer <phase>`)**: Adds new phases, updates phase deliverables/prerequisites, or marks phases `DEFERRED` while maintaining sequential consistency between the Overview table and detailed phase sections.
  3. **Status & Drift Audit Mode (`--status` / `--check`)**: Performs a read-only static structural lint of `ROADMAP.md` and reconciles each phase against `specs/NNN-*` directories (`spec.md`, `plan.md`, `tasks.md` task completion checkboxes), active git branches/worktrees, and commit history, outputting a structured status and drift report (`SYNCED`, `STATUS_DRIFT`, `STRUCTURAL_ERROR`).
  4. **Status Synchronization Mode (`--sync`)**: Updates the `Status` and `Spec` fields in `ROADMAP.md` (both in the Overview table and phase metadata) to match verified repository evidence without altering problem statements or design notes.
  5. **Specify Handoff Mode (`--next` or `--specify <phase>`)**: Selects the next eligible `PLANNED` phase (or the explicitly named phase after verifying its prerequisites are `COMPLETED`), updates `ROADMAP.md` to mark the phase `IN_PROGRESS` with its target `specs/NNN-<short-name>` link, and invokes `/speckit-specify` with the phase's full context.
- **FR-003**: `/speckit-roadmap` MUST determine the **Inferred Evidence Status** of each roadmap phase using deterministic repository rules:
  - `COMPLETED`: A matching feature directory `specs/NNN-*` exists with `spec.md`, `plan.md`, and `tasks.md` where 100% of tasks (`- [x]`) are checked complete (or a commit in git history records completion/promotion of that phase).
  - `IN_PROGRESS`: A matching feature directory `specs/NNN-*` (or an active git branch/worktree for that phase) exists with `spec.md` created, and `tasks.md` is either not yet created or has one or more unchecked tasks (`- [ ]`).
  - `PLANNED`: No matching feature directory or implementation commit exists yet for the phase.
  - `DEFERRED`: Explicitly marked `DEFERRED` in `ROADMAP.md` by human decision.
- **FR-004**: `.agents/skills/speckit-specify/SKILL.md` MUST be updated so that when a user invokes `/speckit-specify` with a roadmap reference (such as `"next roadmap phase"`, `"phase N"`, or via `/speckit-roadmap --next`) or requests git worktree isolation (such as `"Use a worktree"`), `speckit-specify`:
  - Reads `ROADMAP.md` to extract the target phase's title, problem statement, architectural fit, deliverables, and key design decisions as the authoritative feature input context.
  - Supports creating and switching into an isolated git worktree (`.worktrees/<NNN>-<short-name>` on branch `<NNN>-<short-name>`, with `.worktrees/` excluded in `.git/info/exclude`) when worktree isolation is requested.
- **FR-005**: This repository's own `ROADMAP.md` MUST be upgraded to conform to the canonical `roadmap-template.md` schema, with accurate status markers, prerequisites, and `specs/001-*` through `specs/005-*` links reflecting the true state of Phases 1–6.
- **FR-006**: The portable bootstrapper suite (`bootstrap-speckit.sh`, `bootstrap-speckit.ps1`, `.agents/skills/speckit-bootstrap/SKILL.md`, and `.specify/integrations/{speckit,agy,speckit-bootstrap}.manifest.json`) MUST be updated to package and verify:
  - `.specify/templates/roadmap-template.md`
  - `.specify/presets/base-governance/templates/roadmap-template.md` (and updated `.specify/presets/base-governance/preset.yml`)
  - `.agents/skills/speckit-roadmap/SKILL.md` (expanding the managed skill set from 11 to 12 skills)
  - Protection of root `ROADMAP.md` in the **Protected User-State Boundary** so existing project roadmaps are never overwritten during bootstrap seeding or `--upgrade`.
- **FR-007**: `/speckit-roadmap` MUST emit structured operational telemetry conforming to `.specify/memory/logging-standards.md` (`INFO` for lifecycle milestones such as roadmap scaffolding, status sync, and specify handoff; `WARN` for boundary rejections such as missing `ROADMAP.md`, unfulfilled phase prerequisites, or detected status/structural drift; `CRITICAL` for broken internal invariants).
- **FR-008**: In compliance with Constitutional Principle III (*Static Verification & No Automated Tests*), all Phase 5 deliverables MUST be verified through static structural inspection, `--check` / `--status` validation, shell/PowerShell syntax verification on the updated bootstrap seeders, and manifest SHA-256 digest verification, with zero automated test suites (`tests/`) or `.specify/scripts/` runtime scripts generated.

### Key Entities

- **Roadmap Template (`roadmap-template.md`)**: The canonical Markdown template in `.specify/templates/roadmap-template.md` and `.specify/presets/base-governance/templates/roadmap-template.md` defining the required table columns, status vocabulary (`PLANNED`, `IN_PROGRESS`, `COMPLETED`, `DEFERRED`), prerequisite links, and per-phase section structure.
- **Project Roadmap (`ROADMAP.md`)**: The project-owned strategic planning document at the repository root tracking multi-phase initiatives, their inter-phase dependencies, high-level deliverables, and links to tactical `specs/NNN-*` directories.
- **Roadmap Management Skill (`speckit-roadmap`)**: The agent skill in `.agents/skills/speckit-roadmap/SKILL.md` responsible for authoring `ROADMAP.md`, auditing phase status and structural integrity against `specs/` and git state, synchronizing status drift, and handing off eligible phases to `/speckit-specify`.
- **Phase Status & Drift Record**: The computed reconciliation entry for each roadmap phase comparing `DeclaredStatus` (in `ROADMAP.md`) against `InferredEvidenceStatus` (derived from `specs/NNN-*/{spec,plan,tasks}.md`, worktrees, and git history) and classifying alignment as `SYNCED`, `STATUS_DRIFT`, or `STRUCTURAL_ERROR`.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users and agents can scaffold a new `ROADMAP.md`, add or update phases, or audit roadmap status in a single `/speckit-roadmap` invocation with 100% structural alignment between the Overview of Initiatives table and detailed phase sections.
- **SC-002**: Running `/speckit-roadmap --status` (or `--check`) against the repository reconciles 100% of declared roadmap phases (Phases 1–6) against `specs/001-*` through `specs/005-*` and git history, accurately distinguishing `COMPLETED`, `IN_PROGRESS`, and `PLANNED` phases with 0 false positives.
- **SC-003**: Invoking `/speckit-roadmap --next` (or `/speckit-specify` with `"next roadmap phase"`) deterministically identifies the next eligible `PLANNED` phase whose prerequisites are `COMPLETED` and populates a complete, validation-passing `spec.md` without requiring the user to copy-paste phase details from `ROADMAP.md`.
- **SC-004**: 100% of Spec Kit skills (all 12 skills including `speckit-roadmap`) remain completely script-free with 0 references to `.specify/scripts/bash/`, while `bootstrap-speckit.sh`, `bootstrap-speckit.ps1`, and `/speckit-bootstrap --check` cleanly package and verify `roadmap-template.md` and `speckit-roadmap` while protecting root `ROADMAP.md` as user state.

## Assumptions

- **100% Skill-Driven Architecture Preserved**: Consistent with the Phase 4 architecture (`004-portable-project-bootstrapper`) and Constitutional Principle III, static linting and status reporting for `ROADMAP.md` are implemented natively inside `.agents/skills/speckit-roadmap/SKILL.md` (`--check` and `--status` modes) rather than reintroducing `.specify/scripts/bash/check-roadmap.sh`.
- **Dual-Source Status Reconciliation with Explicit Confirmation on Mutation**: `ROADMAP.md` stores explicit human-readable `Status` (`PLANNED`, `IN_PROGRESS`, `COMPLETED`, `DEFERRED`) and `Spec` (`specs/NNN-*`) columns in the Overview table and phase metadata, while `/speckit-roadmap --status` computes live evidence from `specs/` and git history; `--status` / `--check` are strictly read-only, whereas `--sync` (or `--next` handoff) writes the reconciled statuses back to `ROADMAP.md`.
- **Root `ROADMAP.md` Is Protected Project State**: While `roadmap-template.md` and `.agents/skills/speckit-roadmap/SKILL.md` are managed toolkit artifacts distributed by `bootstrap-speckit.sh`, `bootstrap-speckit.ps1`, and `/speckit-bootstrap`, a repository's actual `ROADMAP.md` contains project-specific strategic plans and is added to the Protected User-State Boundary so it is never clobbered on bootstrap or upgrade.
- **First-Class Worktree Support in Specification Workflows**: When a user requests worktree isolation during specification (e.g., `"Use a worktree"`), creating `.worktrees/<NNN>-<short-name>` on branch `<NNN>-<short-name>` (and excluding `.worktrees/` via `.git/info/exclude`) keeps the primary checkout clean and allows parallel phase execution with isolated `.specify/feature.json` state.
