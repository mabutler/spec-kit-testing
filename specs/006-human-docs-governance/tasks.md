---
description: "Task list for Human-Facing Documentation Standards & Governance"
---

# Tasks: Human-Facing Documentation Standards & Governance

**Input**: Design documents from `specs/006-human-docs-governance/` (`spec.md`, `plan.md`, `research.md`, `data-model.md`, `contracts/`, `quickstart.md`)

**Prerequisites**: [plan.md](plan.md) (required), [spec.md](spec.md) (required for user stories), [research.md](research.md), [data-model.md](data-model.md), [contracts/](contracts/)

**Constitutional Principle III Adherence**: Per `.specify/memory/constitution.md` Principle III (*Static Verification & No Automated Tests*), automated test generation is disabled repository-wide. Zero automated test files, test directories, or test harnesses are created. Quality verification is conducted exclusively via declarative static checks (`cmp -s`, regex marker checks, markdown link verification, manifest validation script) defined in [quickstart.md](quickstart.md).

**Documentation Impact**: `USER_FACING` — Target human-facing documentation files: `README.md` (canonical root overview and reference), `.specify/memory/constitution.md` (amended to `v2.1.0`), and `.specify/memory/coding-standards.md` (updated with Human-Facing Documentation & README Conventions).

**Organization**: Tasks are grouped by user story to enable independent implementation and static verification of each story in priority order (P1 → P2 → P3).

---

## Format: `- [ ] [TaskID] [P?] [Story?] Description with file path`

- **[P]**: Can run in parallel (different files, no dependencies on incomplete tasks)
- **[Story]**: Which user story this task belongs to (`[US1]`, `[US2]`, `[US3]`)
- Every task includes exact target file paths and quotes verbatim constraints from [data-model.md](data-model.md) and [contracts/](contracts/)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Worktree environment validation and prerequisite baseline verification

- [X] T001 Inspect worktree environment and verify POSIX CLI tools (`cmp`, `grep`, `sha256sum`, `python3`, `bash`) across `/home/admin/projects/spec-kit-testing/.worktrees/006-human-docs-governance`
- [X] T002 [P] Baseline verification of existing integration manifests in `.specify/integrations/{speckit,agy,speckit-bootstrap}.manifest.json` prior to feature modifications

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Validate 4-tier template resolution hierarchy and establish baseline template state

**⚠️ CRITICAL**: No user story implementation can begin until baseline template resolution is confirmed

- [X] T003 Verify 4-tier template resolution hierarchy and baseline template state across `.specify/templates/` (Tier 4) and `.specify/presets/base-governance/templates/` (Tier 2)

**Checkpoint**: Foundation ready — user story implementation can now begin in priority order

---

## Phase 3: User Story 1 - Base Governance Templates & Co-Applied Human-Facing Documentation Standards (Priority: P1) 🎯 MVP

**Goal**: Establish explicit constitutional principles and companion coding-standard rules in `.specify/templates/` and `.specify/presets/base-governance/templates/` governing when and how human-facing documentation must be synchronized, and update `/speckit-constitution` to process `MODULE-DOCS` (`ENABLED` | `OMITTED`) and slot `[HUMAN_DOCS_CONVENTIONS]` across all 26 tracked slots.

**Independent Test**: Execute Scenario 1 from `specs/006-human-docs-governance/quickstart.md`: verify 100% byte-for-byte parity between `.specify/templates/{constitution-template,coding-standards-template}.md` and `.specify/presets/base-governance/templates/{constitution-template,coding-standards-template}.md`, verify `MODULE-DOCS` markers and `[HUMAN_DOCS_CONVENTIONS]` presence, and verify that `.agents/skills/speckit-constitution/SKILL.md` tracks `MODULE-DOCS` and 26 slots.

### Implementation for User Story 1

- [X] T004 [P] [US1] Update `.specify/templates/constitution-template.md` to expand Principle VII bullet 3 with baseline human-facing documentation synchronization rule quoting verbatim: "Internal architectural documentation and human-facing documentation (`README.md`, quickstarts, and user guides) MUST match actual implemented behavior and be updated in the same change whenever user-visible CLI commands, agent skills, public APIs, configuration options, or end-user workflows are added, removed, or modified; purely internal changes (`INTERNAL_ONLY` refactors, non-behavioral fixes, or internal tooling) are exempt from artificial `README.md` edits.", and add `<!-- OPTIONAL-MODULE: MODULE-DOCS` block quoting verbatim: "Action: ADD", "Title: Structured Human-Facing Documentation Gate", "Target: Principle VII", body bullet: "- **Structured Human-Facing Documentation Gate**: The repository root `README.md` (and any dedicated user guide under `docs/`) MUST maintain canonical sections covering Project Overview & Architecture, Getting Started / Bootstrap Quickstart, CLI / Skill / API Usage Reference, and Configuration & Governance Verification, verified for relative link integrity and command accuracy before merge.", and closing tag `<!-- /OPTIONAL-MODULE: MODULE-DOCS -->` per Contract 1
- [X] T005 [P] [US1] Synchronize `.specify/presets/base-governance/templates/constitution-template.md` to maintain 100% byte-for-byte parity with `.specify/templates/constitution-template.md` (verified via `cmp -s`) per Contract 1 and SC-001
- [X] T006 [P] [US1] Update `.specify/templates/coding-standards-template.md` to append section `## Human-Facing Documentation & README Conventions` operationalizing Principle VII with slot token `[HUMAN_DOCS_CONVENTIONS]` (bringing template slots to 12) and archetype guidance comments for CLI tools, libraries/SDKs, web services, and agent frameworks per Contract 1
- [X] T007 [P] [US1] Synchronize `.specify/presets/base-governance/templates/coding-standards-template.md` to maintain 100% byte-for-byte parity with `.specify/templates/coding-standards-template.md` (verified via `cmp -s`) per Contract 1 and SC-001
- [X] T008 [US1] Update `.agents/skills/speckit-constitution/SKILL.md` to evaluate `MODULE-DOCS` (Step 2), apply structural transformations for `ENABLED` and `OMITTED` (Step 3), merge placeholder values tracking 26 total slots (`8` in constitution, `12` in coding-standards including `[HUMAN_DOCS_CONVENTIONS]`, `6` in logging-standards) (Step 4), update Sync Impact Report template to format `MODULE-DOCS: <ENABLED|OMITTED>` (Step 6), and enforce pre-write validation with zero residual `[ALL_CAPS_IDENTIFIER]` tokens (Step 7) per Contract 1
- [X] T009 [US1] Execute static validation check Scenario 1 from `specs/006-human-docs-governance/quickstart.md` verifying template parity, `MODULE-DOCS` tags, `[HUMAN_DOCS_CONVENTIONS]` slot presence, and `speckit-constitution` slot tracking

**Checkpoint**: User Story 1 is complete and verified independently — base governance templates and `/speckit-constitution` handle `MODULE-DOCS` and `[HUMAN_DOCS_CONVENTIONS]` with byte-for-byte parity.

---

## Phase 4: User Story 2 - Active Repository Constitution Amendment & Canonical `README.md` Ratification (Priority: P2)

**Goal**: Formally amend this repository's active `.specify/memory/constitution.md` (version `2.1.0`) and `.specify/memory/coding-standards.md` to ratify Phase 6 standards, and author a canonical repository root `README.md` covering architecture, the Co-Applied Governance Suite, all 11 Spec Kit skills, and portable cross-platform bootstrapping.

**Independent Test**: Execute Scenario 2 and Scenario 3 from `specs/006-human-docs-governance/quickstart.md`: verify `.specify/memory/constitution.md` is at version `2.1.0` with `MODULE-DOCS: ENABLED` in the top `Sync Impact Report`, zero residual `[ALL_CAPS]` placeholders or comment tags in `.specify/memory/`, `.specify/memory/coding-standards.md` contains `## Human-Facing Documentation & README Conventions`, and root `README.md` documents all 11 skills and both bootstrapper entry points with zero broken relative links and zero ephemeral `specs/NNN-*/` or `FR-XXX`/`SC-XXX` citations.

### Implementation for User Story 2

- [X] T010 [P] [US2] Amend active `.specify/memory/constitution.md` to bump version `2.0.0 -> 2.1.0` (`Ratified: 2026-11-04 | Last Amended: 2026-11-05`), update top HTML `Sync Impact Report` with `MODULE-DOCS: ENABLED` and amendment rationale, expand Principle VII bullet 3 with baseline human-facing documentation synchronization rule, include ratified `MODULE-DOCS` body bullet verbatim: "- **Structured Human-Facing Documentation Gate**: The repository root `README.md` (and any dedicated user guide under `docs/`) MUST maintain canonical sections covering Project Overview & Architecture, Getting Started / Bootstrap Quickstart, CLI / Skill / API Usage Reference, and Configuration & Governance Verification, verified for relative link integrity and command accuracy before merge." with comment tags stripped, and ensure 0 residual `[ALL_CAPS]` placeholders or `OPTIONAL-MODULE` comment tags per Contract 3
- [X] T011 [P] [US2] Amend active `.specify/memory/coding-standards.md` to append section `## Human-Facing Documentation & README Conventions` operationalizing Principle VII, defining concrete conventions for `README.md`, `ROADMAP.md`, and `.agents/skills/speckit-*/SKILL.md` with 0 unresolved `[ALL_CAPS]` tokens and 0 references to ephemeral `specs/NNN-*/` paths or `FR-XXX`/`SC-XXX` identifiers per Contract 3
- [X] T012 [US2] Author canonical repository root `README.md` with required sections: Title/Overview, Project Overview & Architecture (4-tier template hierarchy), Co-Applied Governance Suite (`constitution.md` v2.1.0, `coding-standards.md`, `logging-standards.md`, Principles I–VII, optional modules including `MODULE-DOCS`, `Documentation Impact` gate), Spec Kit Skills & Subagent Reference (all 11 skills: speckit-specify through speckit-bootstrap, and role profiles: speckit-reasoner, speckit-executor), Getting Started & Portable Bootstrapping (`bootstrap-speckit.sh` and `bootstrap-speckit.ps1`), and Configuration & Governance Verification, adhering to SC-004 (0 broken relative links, 0 unresolved placeholders, 0 ephemeral `specs/NNN-*/` or `FR-XXX`/`SC-XXX` citations) per Contract 3
- [X] T013 [US2] Execute static validation checks Scenario 2 and Scenario 3 from `specs/006-human-docs-governance/quickstart.md` verifying `constitution.md` v2.1.0 amendment, `coding-standards.md` human-facing documentation section, zero residual placeholders/tags in `.specify/memory/`, and root `README.md` completeness and link integrity

**Checkpoint**: User Stories 1 and 2 are both functional and verified independently — repository governance is ratified at v2.1.0 and root `README.md` serves as the canonical human-facing guide.

---

## Phase 5: User Story 3 - Downstream Spec Kit Skill Documentation Gates & Manifest Sync (Priority: P3)

**Goal**: Implement documentation impact gates across `plan-template.md`, `tasks-template.md`, and 5 downstream skills (`speckit-plan`, `speckit-tasks`, `speckit-analyze`, `speckit-implement`, `speckit-converge`), and synchronize SHA-256 digests and byte sizes across all 3 integration manifests (`speckit.manifest.json`, `agy.manifest.json`, `speckit-bootstrap.manifest.json`).

**Independent Test**: Execute Scenario 4 and Scenario 5 from `specs/006-human-docs-governance/quickstart.md`: verify that `plan-template.md`, `tasks-template.md`, and all 5 downstream skills enforce `USER_FACING` vs. `INTERNAL_ONLY` documentation gates, and verify that 100% of SHA-256 digests and `size_bytes` across `.specify/integrations/{speckit,agy,speckit-bootstrap}.manifest.json` match on-disk files.

### Implementation for User Story 3

- [X] T014 [P] [US3] Update `.specify/templates/plan-template.md` to add `**Documentation Impact**: [USER_FACING (list affected human-facing docs, e.g., README.md, docs/...) or INTERNAL_ONLY (1-sentence rationale why no user-visible CLI, skill, API, config, or workflow changes occur)]` under `## Technical Context` and add Principle VII human-facing documentation evaluation to `## Constitution Check` per Contract 2
- [X] T015 [P] [US3] Update `.agents/skills/speckit-plan/SKILL.md` in Step 3 Outline and Constitution Check to require explicit `Documentation Impact` classification (`USER_FACING` target files vs `INTERNAL_ONLY` exemption rationale) and verify Principle VII alignment with graceful fallback for legacy `coding-standards.md` per Contract 2
- [X] T016 [P] [US3] Update `.specify/templates/tasks-template.md` header notes and Phase N Polish section to document conditional human-facing documentation task generation (`USER_FACING` targets vs `INTERNAL_ONLY` exemption) per Contract 2
- [X] T017 [P] [US3] Update `.agents/skills/speckit-tasks/SKILL.md` in Step 3 Outline and Task Organization to inspect `Documentation Impact` in `plan.md`, generate explicit task(s) with exact file paths when `USER_FACING`, and omit artificial `README.md` tasks when `INTERNAL_ONLY` per Contract 2
- [X] T018 [P] [US3] Update `.agents/skills/speckit-analyze/SKILL.md` in Step 2, Step 4.D (`Constitution Alignment`), and Step 4.E (`Coverage Gaps`) to load `Documentation Impact`, verify that `USER_FACING` features have mapped doc tasks in `tasks.md`, verify valid non-empty rationale for `INTERNAL_ONLY`, flag missing doc coverage as CRITICAL/HIGH, and flag citations of ephemeral `specs/NNN-*/` or `FR-XXX` in permanent human docs per Contract 2
- [X] T019 [P] [US3] Update `.agents/skills/speckit-implement/SKILL.md` in Step 6 (`Enforce governance conventions`) and Step 9 (`Completion validation`) to verify that planned `USER_FACING` human-facing documentation updates match as-built behavior, contain valid relative links, and have zero ephemeral `specs/NNN-*/` or `FR-XXX` citations per Contract 2
- [X] T020 [P] [US3] Update `.agents/skills/speckit-converge/SKILL.md` in Step 3 (`Build the Intent Inventory`) and Step 4 (`Assess the Codebase and Classify Findings`) to include `Documentation Impact` in intent inventory, audit human-facing doc files on disk when `USER_FACING`, emit findings if missing/partial/contradicts, and require zero `README.md` edits when `INTERNAL_ONLY` per Contract 2
- [X] T021 [US3] Update SHA-256 hex string digests in `.specify/integrations/speckit.manifest.json` for modified templates (`coding-standards-template.md`, `constitution-template.md`, `plan-template.md`, `tasks-template.md`) per Contract 3
- [X] T022 [US3] Update SHA-256 hex string digests in `.specify/integrations/agy.manifest.json` for modified skills (`speckit-analyze/SKILL.md`, `speckit-constitution/SKILL.md`, `speckit-converge/SKILL.md`, `speckit-implement/SKILL.md`, `speckit-plan/SKILL.md`, `speckit-tasks/SKILL.md`) per Contract 3
- [X] T023 [US3] Update `.specify/integrations/speckit-bootstrap.manifest.json` with updated `digest: "sha256:<hex>"` and `size_bytes: <int>` for all modified managed assets under `.specify/` and `.agents/`, computed strictly after `speckit.manifest.json` and `agy.manifest.json` are written per Contract 3
- [X] T024 [US3] Execute static validation checks Scenario 4 and Scenario 5 from `specs/006-human-docs-governance/quickstart.md` verifying `USER_FACING` / `INTERNAL_ONLY` gates across all 7 files and verifying 100% SHA-256 digest and byte size matches in all 3 manifests

**Checkpoint**: All three user stories are complete and integrated — downstream delivery skills enforce documentation impact gates and integration manifests are fully synchronized.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Repository-wide static verification, syntax integrity, and link/placeholder hygiene

- [X] T025 Static syntax verification of `bootstrap-speckit.sh` via `bash -n bootstrap-speckit.sh`
- [X] T026 Execute end-to-end static validation suite across Scenario 1 through Scenario 5 in `specs/006-human-docs-governance/quickstart.md`
- [X] T027 [P] Audit all modified files to ensure zero broken relative links, zero unresolved `[ALL_CAPS_IDENTIFIER]` placeholders, and zero citations of ephemeral `specs/NNN-*/` paths or `FR-XXX`/`SC-XXX` identifiers in permanent files outside `specs/`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion — BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories proceed sequentially in priority order: US1 (P1) → US2 (P2) → US3 (P3)
- **Polish (Phase 6)**: Depends on all user stories (US1, US2, US3) being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start immediately after Foundational (Phase 2) — No dependencies on other stories
- **User Story 2 (P2)**: Depends on US1 completion (active `constitution.md` amendment ratifies the template changes established in US1; `README.md` documents the governance suite and skills)
- **User Story 3 (P3)**: Depends on US1 completion (downstream skills enforce the gates established by the templates); manifests in US3 seal the final digests of US1 and US2 files

### Parallel Opportunities

- Within Phase 3 (US1):
  - T004 (`constitution-template.md`), T005 (preset `constitution-template.md`), T006 (`coding-standards-template.md`), and T007 (preset `coding-standards-template.md`) can execute in parallel
  - T008 (`speckit-constitution/SKILL.md`) follows template edits
  - T009 (Scenario 1 static validation) validates US1 deliverables
- Within Phase 4 (US2):
  - T010 (`constitution.md`) and T011 (`coding-standards.md`) can execute in parallel
  - T012 (`README.md`) can author the comprehensive guide
  - T013 (Scenarios 2 & 3 static validation) validates US2 deliverables
- Within Phase 5 (US3):
  - T014 (`plan-template.md`), T015 (`speckit-plan`), T016 (`tasks-template.md`), T017 (`speckit-tasks`), T018 (`speckit-analyze`), T019 (`speckit-implement`), and T020 (`speckit-converge`) can all execute in parallel across independent files
  - T021 (`speckit.manifest.json`) and T022 (`agy.manifest.json`) execute once files are finalized
  - T023 (`speckit-bootstrap.manifest.json`) executes strictly after T021 and T022
  - T024 (Scenarios 4 & 5 static validation) validates US3 deliverables
- Within Phase 6 (Polish):
  - T025 (`bash -n`) and T027 (link/hygiene audit) can run in parallel

---

## Parallel Execution Examples

### Parallel Example: User Story 1
```bash
# Edit base governance templates in parallel:
Task: "Update .specify/templates/constitution-template.md" (T004)
Task: "Synchronize .specify/presets/base-governance/templates/constitution-template.md" (T005)
Task: "Update .specify/templates/coding-standards-template.md" (T006)
Task: "Synchronize .specify/presets/base-governance/templates/coding-standards-template.md" (T007)
```

### Parallel Example: User Story 2
```bash
# Amend active governance suite in parallel:
Task: "Amend active .specify/memory/constitution.md" (T010)
Task: "Amend active .specify/memory/coding-standards.md" (T011)
```

### Parallel Example: User Story 3
```bash
# Update downstream skills in parallel across independent files:
Task: "Update .specify/templates/plan-template.md" (T014)
Task: "Update .agents/skills/speckit-plan/SKILL.md" (T015)
Task: "Update .specify/templates/tasks-template.md" (T016)
Task: "Update .agents/skills/speckit-tasks/SKILL.md" (T017)
Task: "Update .agents/skills/speckit-analyze/SKILL.md" (T018)
Task: "Update .agents/skills/speckit-implement/SKILL.md" (T019)
Task: "Update .agents/skills/speckit-converge/SKILL.md" (T020)
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001–T002)
2. Complete Phase 2: Foundational (T003)
3. Complete Phase 3: User Story 1 (T004–T009)
4. **STOP and VALIDATE**: Run Scenario 1 from `quickstart.md` (`cmp -s` parity, grep checks)
5. Base governance templates and `/speckit-constitution` ready for distribution (MVP!)

### Incremental Delivery

1. Setup + Foundational → Workspace verified and baseline established
2. Add User Story 1 → Base governance templates & `speckit-constitution` synchronized (MVP)
3. Add User Story 2 → Active governance amended (`v2.1.0`), root `README.md` authored and ratified
4. Add User Story 3 → Downstream skills enforce `USER_FACING` vs `INTERNAL_ONLY` gates, manifests sealed
5. Polish Phase → Full static test suite passes, zero warnings, zero link defects, clean bundle

---

## Notes

- **Checklist format**: Every task strictly begins with `- [ ] [TaskID] [P?] [Story?]` followed by actionable description with exact file path.
- **Principle III Compliance**: Zero automated unit tests, integration test files, or mock frameworks. All verification is performed via static analysis, `cmp`, `grep`, and `python3` manifest verification scripts.
- **Hygiene Rule**: Zero citations of ephemeral `specs/NNN-*/` directories or `FR-XXX`/`SC-XXX` identifiers in files outside `specs/`.
- **Manifest Synchronization Invariant**: `speckit.manifest.json` and `agy.manifest.json` MUST be updated before `speckit-bootstrap.manifest.json` so that `speckit-bootstrap.manifest.json` records the exact self-digests of the other two manifests.
---

## Phase 7: Convergence

- [X] T028 Remove duplicated trailing Sync Impact Report lines and unbalanced closing code fence in Step 6 (lines 185–189) of `.agents/skills/speckit-constitution/SKILL.md` so markdown code fences are balanced per FR-003 (partial)
- [X] T029 Re-synchronize SHA-256 digests and `size_bytes` in `.specify/integrations/agy.manifest.json` and `.specify/integrations/speckit-bootstrap.manifest.json` after updating `.agents/skills/speckit-constitution/SKILL.md` per FR-009 (partial)
