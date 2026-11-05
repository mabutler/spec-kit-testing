---
description: "Task list for Portable Project Bootstrapper feature implementation"
---

# Tasks: Portable Project Bootstrapper

**Input**: Design documents from `/specs/004-portable-project-bootstrapper/` (`spec.md`, `plan.md`, `research.md`, `data-model.md`, `contracts/`, `quickstart.md`)  
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/  
**Tests**: Automated tests are DISABLED repository-wide per Constitutional Principle III (*Static Verification & No Automated Tests* ratified in Constitution v2.0.0). No unit test or test harness tasks are generated. Verification relies strictly on static syntax validation, JSON schema validation, and end-to-end quickstart execution.  
**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions
- Constraints from data-model.md and contracts are quoted verbatim in task descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization, governance gate alignment, and registry skeletons

- [X] T001 Inspect and verify environment preconditions, directory structure, and baseline files for the portable project bootstrapper feature across `.specify/`, `.agents/`, and `specs/004-portable-project-bootstrapper/`
- [X] T002 [P] Update `.specify/memory/constitution.md` Pre-PR Verification gate to remove the legacy dependency on `.specify/scripts/bash/resolve-template.sh` in compliance with FR-001 and Principle III
- [X] T003 [P] Initialize preset and extension registry skeletons in `.specify/presets/.registry` and `.specify/extensions/.registry` conforming to `preset-and-extension-schema.json` with properties `priority` (`type: integer, minimum: 1, default: 10`) and `enabled` (`type: boolean, default: true`)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure and template synchronization that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 Establish the native 4-tier template resolution hierarchy and `FeatureContext` resolution specification in `.specify/templates/plan-template.md` and `.specify/templates/tasks-template.md` enforcing Tier 1 (`overrides`), Tier 2 (`presets`), Tier 3 (`extensions`), and Tier 4 (`core fallback`), and quoting the invariant verbatim: "If a requested template is not found in any of the 4 tiers, the agent MUST fail closed and emit an error per Principle II" and `feature_directory` "MUST NOT be empty" and `${FEATURE_DIR}` "MUST exist for downstream skills"
- [X] T005 [P] Audit and establish the managed role-based agent profile definitions in `.agents/agents/speckit-reasoner.md` and `.agents/agents/speckit-executor.md` ensuring strict separation of concerns, explicit model tiering, and compliance with the 4-tier template hierarchy
- [X] T006 [P] Synchronize the canonical baseline core fallback templates in `.specify/templates/` (`checklist-template.md`, `coding-standards-template.md`, `constitution-template.md`, `logging-standards-template.md`, `plan-template.md`, `spec-template.md`, `tasks-template.md`) ensuring all 7 templates match the 4-tier inheritance specification

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - 100% Script-Free Spec Kit Skills & Ultra-Thin `.sh`/`.ps1` Terminal Seeders (Priority: P1) 🎯 MVP

**Goal**: Refactor all 10 existing Spec Kit skills to use 100% agent-native file operations for feature discovery and 4-tier template resolution, completely remove `.specify/scripts/`, deliver ultra-thin paired cross-platform terminal seeders `bootstrap-speckit.sh` and `bootstrap-speckit.ps1` under 150 LOC each with zero external dependencies, and establish the baseline `/speckit-bootstrap` skill.

**Independent Test**: Verify that zero files in `.agents/skills/speckit-*/` contain references to `.specify/scripts`, that `.specify/scripts/` is completely deleted from the repository, that `./bootstrap-speckit.sh <target-dir>` and `pwsh ./bootstrap-speckit.ps1 <target-dir>` copy all managed assets into a fresh directory in < 1 second while remaining under 150 lines each, and that `/speckit-bootstrap` verifies the seeded repository natively.

### Implementation for User Story 1

- [X] T007 [P] [US1] Refactor `.agents/skills/speckit-specify/SKILL.md` to remove `.specify/scripts/bash/*.sh` invocations and implement native agent feature path discovery (`.specify/feature.json` or `SPECIFY_FEATURE_DIRECTORY`) and 4-tier template resolution for `spec-template`
- [X] T008 [P] [US1] Refactor `.agents/skills/speckit-clarify/SKILL.md` to remove `.specify/scripts/bash/*.sh` invocations and implement native agent `FEATURE_DIR` discovery and prerequisite artifact validation
- [X] T009 [P] [US1] Refactor `.agents/skills/speckit-plan/SKILL.md` to remove `.specify/scripts/bash/*.sh` invocations (`setup-plan.sh`) and implement native agent resolution of `plan-template` across the 4-tier hierarchy
- [X] T010 [P] [US1] Refactor `.agents/skills/speckit-tasks/SKILL.md` to remove `.specify/scripts/bash/*.sh` invocations (`setup-tasks.sh`) and implement native agent resolution of `tasks-template` across the 4-tier hierarchy
- [X] T011 [P] [US1] Refactor `.agents/skills/speckit-checklist/SKILL.md` to remove `.specify/scripts/bash/*.sh` invocations and implement native agent resolution of `checklist-template` across the 4-tier hierarchy
- [X] T012 [P] [US1] Refactor `.agents/skills/speckit-analyze/SKILL.md` to remove `.specify/scripts/bash/*.sh` invocations and implement native agent cross-artifact consistency analysis
- [X] T013 [P] [US1] Refactor `.agents/skills/speckit-implement/SKILL.md` to remove `.specify/scripts/bash/*.sh` invocations and implement native agent task checklist execution and status updates
- [X] T014 [P] [US1] Refactor `.agents/skills/speckit-converge/SKILL.md` to remove `.specify/scripts/bash/*.sh` invocations and implement native agent gap convergence and unbuilt task appending
- [X] T015 [P] [US1] Refactor `.agents/skills/speckit-constitution/SKILL.md` to remove `.specify/scripts/bash/*.sh` invocations and implement native 4-tier template resolution for `constitution-template`, `coding-standards-template`, and `logging-standards-template`
- [X] T016 [P] [US1] Refactor `.agents/skills/speckit-orchestrate/SKILL.md` to remove `.specify/scripts/bash/*.sh` invocations and coordinate context-isolated subagents using native agent instructions and role profiles
- [X] T017 [US1] Delete obsolete `.specify/scripts/` directory completely from the repository and purge all `.specify/scripts/bash/*` entries from `.specify/integrations/speckit.manifest.json` in accordance with FR-001 and SC-001
- [X] T018 [P] [US1] Implement ultra-thin POSIX/Bash seeder script `bootstrap-speckit.sh` (< 150 LOC, zero external dependencies) supporting `<target-repo>`, `--force`, `--help`, enforcing Protected User-State immutability, creating/updating `<target-repo>/.gitignore` with `.agents/agents/*.local.md`, and copying managed assets per `contracts/bootstrap-cli-contract.md`
- [X] T019 [P] [US1] Implement ultra-thin PowerShell seeder script `bootstrap-speckit.ps1` (< 150 LOC, zero external dependencies) supporting `<target-repo>`, `-Force`, `-Help`, enforcing Protected User-State immutability, creating/updating `<target-repo>/.gitignore` with `.agents/agents/*.local.md`, and copying managed assets per `contracts/bootstrap-cli-contract.md`
- [X] T020 [US1] Create baseline `.agents/skills/speckit-bootstrap/SKILL.md` implementing Mode A (Self-Check / Post-Seed Verification): asset scanning across `.specify/` and `.agents/`, obsolete script detection/removal, `.gitignore` maintenance, and readiness reporting per `contracts/speckit-bootstrap-skill-contract.md`

**Checkpoint**: At this point, User Story 1 is fully functional and testable independently. The suite is 100% script-free and terminal seeders operate cleanly.

---

## Phase 4: User Story 2 - Agent-Driven Non-Destructive Upgrades & Override Preservation via `/speckit-bootstrap` (Priority: P2)

**Goal**: Deliver manifest-gated non-destructive upgrades, drift detection (`--check` / `--dry-run`), and SHA-256 cryptographic manifest tracking in `/speckit-bootstrap`, strictly preserving Protected User State under all conditions.

**Independent Test**: Verify that seeding a target directory, adding ratified files in `.specify/memory/`, placing a template override in `.specify/templates/overrides/`, creating `.agents/agents/speckit-executor.local.md`, and making a manual edit to a managed skill results in `/speckit-bootstrap --check` correctly classifying all files (`CREATE`, `UPGRADE`, `PRESERVE_USER_STATE`, `SKIP_DRIFTED`, `REMOVE_OBSOLETE`, `UNCHANGED`) with zero disk mutations, and `/speckit-bootstrap --upgrade` updating only unmodified managed files while preserving all user state and logging `WARN` diagnostics for drifted files.

### Implementation for User Story 2

- [X] T021 [US2] Implement the 6-state File Action Classification State Machine (`CREATE`, `UPGRADE`, `PRESERVE_USER_STATE`, `SKIP_DRIFTED`, `REMOVE_OBSOLETE`, `UNCHANGED`) and the Protected User-State Allowlist (`.specify/memory/constitution.md`, `.specify/memory/coding-standards.md`, `.specify/memory/logging-standards.md`, `.specify/templates/overrides/**`, `.specify/feature.json`, `specs/**`, `.agents/agents/*.local.md`, `.agents/agents/speckit-<custom>.md`, and non-speckit skills in `.agents/skills/`) in `.agents/skills/speckit-bootstrap/SKILL.md`, quoting verbatim: "never overwrite or delete under any circumstances, even when --force / -Force is passed"
- [X] T022 [US2] Implement Mode B upgrade and drift detection workflows in `.agents/skills/speckit-bootstrap/SKILL.md` supporting `--check` / `--dry-run` (read-only plan output), `--upgrade` (manifest digest comparison against target disk content), `--force` (overwrite drifted managed files while preserving user state), and `--source=<source-repo>` with structured `WARN` diagnostics conforming to `.specify/memory/logging-standards.md`
- [X] T023 [P] [US2] Generate canonical bootstrap install manifest `.specify/integrations/speckit-bootstrap.manifest.json` conforming to `manifest-schema.json` with required fields `manifest_version` (`enum: ["1.0"]`), `bundle_version` (string), `generated_at` (ISO 8601 UTC date-time), and `files` map containing `digest` (`pattern: ^sha256:[a-f0-9]{64}$`), `size_bytes` (`minimum: 0`), and `tier` (`enum: ["core", "preset", "extension", "skill", "agent", "metadata"]`) for every managed file
- [X] T024 [P] [US2] Synchronize `.specify/integrations/speckit.manifest.json` and `.specify/integrations/agy.manifest.json` to reflect the complete 11-skill inventory, 2 agent roles, and 0 script entries

**Checkpoint**: At this point, User Stories 1 AND 2 both work independently. Upgrades and drift detection are fully operational and protected state is immutable.

---

## Phase 5: User Story 3 - First-Class Spec Kit Preset & Extension Packaging + Seamless Governance Initialization (Priority: P3)

**Goal**: Package Base Governance Preset (`.specify/presets/base-governance/`) and Orchestrator Extension (`.specify/extensions/speckit-orchestrator/`) as first-class citizens conforming to schemas, and implement Mode C `--init-governance` chaining in `/speckit-bootstrap`.

**Independent Test**: Verify that `.specify/presets/base-governance/preset.yml` and `.specify/extensions/speckit-orchestrator/extension.yml` validate against `preset-and-extension-schema.json`, that the 4-tier template hierarchy discovers preset templates when resolving `constitution-template`, and that running `/speckit-bootstrap --init-governance` completes bootstrap checks and dispatches `/speckit-constitution` against the target repository.

### Implementation for User Story 3

- [X] T025 [P] [US3] Create Base Governance Preset package in `.specify/presets/base-governance/preset.yml` conforming to `preset-and-extension-schema.json` with `name: "base-governance"` (`pattern: ^[a-z0-9-]+$`), `version: "1.0.0"`, `description`, and `provides.templates` declaring `type: template`, `strategy: replace` (`enum: ["replace", "prepend", "append", "wrap"]`) for `constitution-template`, `coding-standards-template`, and `logging-standards-template`, and copy canonical templates into `.specify/presets/base-governance/templates/`
- [X] T026 [P] [US3] Register `base-governance` in `.specify/presets/.registry` with `priority: 10` (`minimum: 1`) and `enabled: true`
- [X] T027 [P] [US3] Create Subagent Orchestrator Extension package in `.specify/extensions/speckit-orchestrator/extension.yml` conforming to `preset-and-extension-schema.json` with `name: "speckit-orchestrator"` (`pattern: ^[a-z0-9-]+$`), `version: "1.0.0"`, `description`, and `hooks.after_specify` declaring `extension: "speckit-orchestrator"`, `command: "speckit.orchestrate"`, `enabled: true`, `optional: true`
- [X] T028 [P] [US3] Register `speckit-orchestrator` in `.specify/extensions/.registry` with `priority: 10` (`minimum: 1`) and `enabled: true`
- [X] T029 [US3] Implement Mode C (`--init-governance`) and post-bootstrap governance ratification handoff in `.agents/skills/speckit-bootstrap/SKILL.md` to inspect `.specify/memory/` and seamlessly invoke (or dispatch a subagent to run) `.agents/skills/speckit-constitution/SKILL.md` against `<target-repo>`
- [X] T030 [US3] Implement idempotent merging of the `speckit.orchestrate` hook into `<target-repo>/.specify/extensions.yml` under `hooks.after_specify` in `.agents/skills/speckit-bootstrap/SKILL.md` preserving all existing custom hooks

**Checkpoint**: All three user stories are complete, independently functional, and integrated.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Validation, hygiene, and conformance checks across all deliverables

- [X] T031 [P] Validate POSIX/Bash syntax of `bootstrap-speckit.sh` via `bash -n bootstrap-speckit.sh` and verify line count is strictly under 150 LOC (`wc -l bootstrap-speckit.sh`) per SC-005
- [X] T032 [P] Validate PowerShell syntax and formatting of `bootstrap-speckit.ps1` and verify line count is strictly under 150 LOC (`wc -l bootstrap-speckit.ps1`) with zero external package dependencies per SC-005
- [X] T033 [P] Validate `.specify/integrations/speckit-bootstrap.manifest.json` against `manifest-schema.json`, and validate `.specify/presets/base-governance/preset.yml`, `.specify/extensions/speckit-orchestrator/extension.yml`, `.specify/presets/.registry`, and `.specify/extensions/.registry` against `preset-and-extension-schema.json`
- [X] T034 [P] Perform static reference audit ensuring zero references to `.specify/scripts` exist across all 11 skills in `.agents/skills/` (`grep -rn "\.specify/scripts" .agents/skills/`) per SC-001
- [X] T035 Execute end-to-end quickstart validation scenarios (Bash seeder, PowerShell seeder, `/speckit-bootstrap` self-check, `--check` drift inspection, and `--upgrade` user-state preservation) defined in `specs/004-portable-project-bootstrapper/quickstart.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 1 (Phase 3 - P1 🎯 MVP)**: Depends on Foundational phase completion
- **User Story 2 (Phase 4 - P2)**: Depends on Foundational phase completion; extends `/speckit-bootstrap` from US1 with upgrade logic and manifests
- **User Story 3 (Phase 5 - P3)**: Depends on Foundational phase completion; packages presets/extensions and integrates `--init-governance` into `/speckit-bootstrap`
- **Polish (Phase 6)**: Depends on all user stories (Phases 3, 4, 5) being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start immediately after Foundational (Phase 2) is complete. Self-contained: refactors all 10 existing skills, deletes `.specify/scripts/`, creates `bootstrap-speckit.sh`, `bootstrap-speckit.ps1`, and baseline `/speckit-bootstrap` skill.
- **User Story 2 (P2)**: Can start after Foundational (Phase 2). Integrates with US1's `/speckit-bootstrap` by adding the 6-state upgrade classification engine, drift inspection (`--check`), and SHA-256 manifests.
- **User Story 3 (P3)**: Can start after Foundational (Phase 2). Packages presets/extensions and hooks `/speckit-constitution` into `/speckit-bootstrap` via `--init-governance`.

### Within Each User Story

- Foundational prerequisites before story tasks
- Independent skill refactors marked `[P]` can proceed concurrently
- Seeders (`bootstrap-speckit.sh`, `bootstrap-speckit.ps1`) can be developed in parallel with skill refactors
- Manifest generation and registry registration after assets are defined
- Final Polish validation after all story implementations

### Parallel Opportunities

- In Phase 1: T002 and T003 can execute in parallel
- In Phase 2: T005 and T006 can execute in parallel
- In Phase 3: All 10 skill refactors (T007 through T016) and the two terminal seeders (T018, T019) can execute in parallel across different files
- In Phase 4: Manifest updates (T023, T024) can proceed in parallel once upgrade logic (T021, T022) is established
- In Phase 5: Preset creation (T025, T026) and Extension creation (T027, T028) can proceed in parallel
- In Phase 6: Static verification tasks (T031, T032, T033, T034) can execute in parallel

---

## Parallel Example: User Story 1

```bash
# Refactor skills concurrently across different files:
Task: "Refactor .agents/skills/speckit-specify/SKILL.md to remove .specify/scripts/bash/*.sh"
Task: "Refactor .agents/skills/speckit-clarify/SKILL.md to remove .specify/scripts/bash/*.sh"
Task: "Refactor .agents/skills/speckit-plan/SKILL.md to remove .specify/scripts/bash/*.sh"
Task: "Refactor .agents/skills/speckit-tasks/SKILL.md to remove .specify/scripts/bash/*.sh"

# Develop terminal seeders concurrently:
Task: "Implement ultra-thin POSIX/Bash seeder script bootstrap-speckit.sh"
Task: "Implement ultra-thin PowerShell seeder script bootstrap-speckit.ps1"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001 - T003)
2. Complete Phase 2: Foundational (T004 - T006 - CRITICAL, blocks all stories)
3. Complete Phase 3: User Story 1 (T007 - T020)
4. **STOP and VALIDATE**: Verify that `.specify/scripts/` is gone, all 10 skills operate without scripts, and `bootstrap-speckit.sh` and `bootstrap-speckit.ps1` seed a fresh target repository cleanly
5. Tag/commit the script-free MVP milestone

### Incremental Delivery

1. Complete Setup + Foundational -> Foundation ready
2. Deliver User Story 1 -> Pure script-free skills + ultra-thin terminal seeders (MVP!)
3. Deliver User Story 2 -> Manifest-gated `--upgrade`, `--check` drift inspection, and Protected User-State immutability
4. Deliver User Story 3 -> Preset/Extension packaging (`base-governance`, `speckit-orchestrator`) + `--init-governance`
5. Execute Phase 6 Polish -> Static validation, schema checks, line count constraints (<150 LOC), and quickstart scenarios
6. All deliverables verified without automated test code per Constitutional Principle III

### Parallel Team Strategy

With multiple developers or subagents:
- Developer/Agent A: Skills refactoring (T007 - T016)
- Developer/Agent B: Terminal seeders `bootstrap-speckit.sh` & `bootstrap-speckit.ps1` (T018 - T019)
- Developer/Agent C: `/speckit-bootstrap` lifecycle skill & manifests (T020 - T024)
- Developer/Agent D: Preset & Extension packaging (T025 - T030)
