# Tasks: Precise & Clear Constitution Language

**Input**: Design documents from `/specs/008-precise-constitution-language/`

**Prerequisites**: [`plan.md`](plan.md), [`spec.md`](spec.md), [`research.md`](research.md), [`data-model.md`](data-model.md), [`contracts/`](contracts/)

**Documentation Impact**: `USER_FACING` — Updates root [`README.md`](../../README.md) Core Governance table with modernized principle titles and descriptions.

**Tests**: None. Repository-wide verification is conducted strictly via static analysis, diff parity, schema validation, and template resolution scripts per `.specify/memory/constitution.md` Principle III (*Static Verification & Quality Gates*). Spec Kit feature workflows MUST NOT generate unit test files, integration test harnesses, or test tasks.

**Organization**: Tasks are grouped by user story to enable independent implementation and static verification of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., `US1`, `US2`, `US3`)
- File paths are exact and repository-relative

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Repository baseline inspection and shared configuration setup.

- [x] T001 Inspect git workspace and verify clean baseline status and file targets per implementation plan in specs/008-precise-constitution-language/plan.md

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core terminology and mapping contracts that MUST be ratified before any files are edited.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete.

- [x] T002 Verify Canonical Principle Mapping Contract in specs/008-precise-constitution-language/contracts/principle-mapping-contract.md against spec requirements

**Checkpoint**: Canonical mappings ratified — user story implementation can begin.

---

## Phase 3: User Story 1 - Modernize Core Principle Titles & Body Prose in Active Governance Suite (Priority: P1) 🎯 MVP

**Goal**: Modernize all 7 Core Principle titles and replace informal, rhetorical, or conversational AI phrases with precise, professional software engineering language in `.specify/memory/`.

**Independent Test**: Inspect `.specify/memory/constitution.md`, `.specify/memory/coding-standards.md`, and `.specify/memory/logging-standards.md` to confirm all titles and bodies use modernized terminology.

### Implementation for User Story 1

- [x] T003 [US1] Amend .specify/memory/constitution.md to Version 2.2.0, updating the sync impact header comment, replacing all 7 principle titles with canonical names, and replacing flowery/rhetorical phrasing throughout all principle bodies and governance sections per FR-001, FR-002, and FR-004
- [x] T004 [US1] Clean up flowery language and modernize principle cross-references in .specify/memory/coding-standards.md per FR-003
- [x] T005 [US1] Clean up flowery language and modernize principle cross-references in .specify/memory/logging-standards.md per FR-003
- [x] T006 [US1] Verify .specify/memory/ governance suite consistency using bash .specify/scripts/bash/resolve-template.sh constitution-template --json per quickstart.md Section 3

**Checkpoint**: At this point, User Story 1 is functional and verifiable independently as the MVP milestone.

---

## Phase 4: User Story 2 - Synchronize Reusable Governance Templates and Presets (Priority: P2)

**Goal**: Synchronize all template source files in `.specify/templates/` and `.specify/presets/base-governance/templates/` with the modernized titles and clean prose.

**Independent Test**: Verify template resolution and content parity between `.specify/templates/` and `.specify/presets/base-governance/templates/`.

### Implementation for User Story 2

- [x] T007 [P] [US2] Update .specify/templates/constitution-template.md with canonical principle titles and cleaned body prose per FR-001, FR-002, and FR-005
- [x] T008 [P] [US2] Update .specify/templates/coding-standards-template.md with cleaned body prose and canonical principle references per FR-003
- [x] T009 [P] [US2] Update .specify/templates/logging-standards-template.md with cleaned body prose and canonical principle references per FR-003
- [x] T010 [P] [US2] Update .specify/presets/base-governance/templates/constitution-template.md with exact matching cleaned constitution template per FR-005
- [x] T011 [P] [US2] Update .specify/presets/base-governance/templates/coding-standards-template.md with exact matching cleaned coding standards template per FR-003
- [x] T012 [P] [US2] Update .specify/presets/base-governance/templates/logging-standards-template.md with exact matching cleaned logging standards template per FR-003

**Checkpoint**: All reusable templates and presets are synchronized and match active governance standards.

---

## Phase 5: User Story 3 - Align Agent Personas, Skills, and Repository Documentation (Priority: P3)

**Goal**: Align dual-client agent personas in `.agents/` and `.claude/`, as well as root `README.md`, with canonical principle names and clean language.

**Independent Test**: Diff `.agents/` and `.claude/` files for 100% parity and search codebase to verify no legacy principle names remain.

### Implementation for User Story 3

- [x] T013 [P] [US3] Update .agents/agents/speckit-executor.md to reference Principle I (Evidence-Based Decisions & Bounded Research) and modernized principle terminology per FR-006
- [x] T014 [P] [US3] Update .agents/agents/speckit-reasoner.md to reference Principle I (Evidence-Based Decisions & Bounded Research) and modernized principle terminology per FR-006
- [x] T015 [US3] Mirror .agents/agents/speckit-executor.md to .claude/agents/speckit-executor.md and .agents/agents/speckit-reasoner.md to .claude/agents/speckit-reasoner.md ensuring 100% byte-for-byte parity per FR-006 and SC-003
- [x] T016 [US3] Update README.md Core Governance table with the modernized principle titles and precise descriptions per FR-007
- [x] T017 [US3] Streamline README.md to reference upstream GitHub Spec Kit (github/spec-kit) as a project dependency without restating built-in Spec Kit workflows or commands, focusing concisely on the custom additions provided by this toolkit per FR-008

**Checkpoint**: Dual-client personas and user-facing documentation are fully aligned with 100% parity.

---

## Phase 6: Polish & Cross-Cutting Verification

**Purpose**: Static verification, schema validation, and constitutional compliance checks across all deliverables.

- [x] T018 [P] Run global search confirming zero occurrences of "Evidence Over Invention" remain in active governance files, templates, agent profiles, or README.md per SC-001
- [x] T019 [P] Verify byte-for-byte parity between .agents/ and .claude/ agent files via diff -u per SC-003
- [x] T020 Execute template resolution verification scripts (resolve-template.sh) across all governance templates per quickstart.md Section 3

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**:
  - User Story 1 (Phase 3): Core governance suite in `.specify/memory/`
  - User Story 2 (Phase 4): Templates and presets (depends on US1 terminology)
  - User Story 3 (Phase 5): Agent personas and documentation (depends on US1 terminology)
- **Polish (Final Phase)**: Depends on all user stories being complete
