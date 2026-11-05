---
description: "Task list for Base Governance Suite & Templates implementation"
---

# Tasks: Base Governance Suite & Templates

**Input**: Design documents from `/specs/001-base-governance-templates/` (`spec.md`, `plan.md`, `data-model.md`, `contracts/`, `research.md`, `quickstart.md`)

**Prerequisites**: `plan.md` (required), `spec.md` (required for user stories), `data-model.md`, `contracts/optional-module-delimiters.md`, `contracts/placeholder-tokens.md`, `contracts/template-resolution-contract.md`, `quickstart.md`

**Tests**: Test tasks are included per `quickstart.md` validation scenarios using platform-agnostic Python inspection and optional Spec Kit bash resolver checks.

**Organization**: Tasks are grouped by user story (US1: Constitution Template, US2: Coding Standards Template, US3: Logging Standards Template) to enable independent implementation, testing, and delivery.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and template directory verification

- [X] T001 Verify `.specify/templates/` directory structure and inspect current baseline in `.specify/templates/`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core validation test harness that all user stories depend on to verify delimiter grammar, placeholder token syntax, and template resolution.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete.

- [X] T002 [P] Create template validation test suite in `tests/test_governance_templates.py` implementing Scenarios 1-6 from `specs/001-base-governance-templates/quickstart.md` verifying file presence, Core Principles I–VII, delimiter contracts from `specs/001-base-governance-templates/contracts/optional-module-delimiters.md`, 5-tier severity levels, and regex patterns `^\[[A-Z0-9_]+\]$` and `^\[YYYY-MM-DD\]$` from `specs/001-base-governance-templates/contracts/placeholder-tokens.md`
- [X] T003 [P] Create direct execution test runner script in `scripts/test-templates.sh` to run template resolution checks via `.specify/scripts/bash/resolve-template.sh` in raw and `--json` modes per `specs/001-base-governance-templates/contracts/template-resolution-contract.md`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel.

---

## Phase 3: User Story 1 - Resolve Rich Base Constitution Template with Optional Enhancements (Priority: P1) 🎯 MVP

**Goal**: Deliver canonical Base Constitution v1.0.0 in `.specify/templates/constitution-template.md` replacing the empty scaffold with the 7 Core Principles, authority hierarchy, quality gates, recorded deviations, and inline machine-parseable delimiters for Optional Enhancement Modules A–D (including Module B default clause replacement and Module D nested sub-clause).

**Independent Test**: Run `python3 tests/test_governance_templates.py` and verify `.specify/templates/constitution-template.md` passes Scenarios 1, 2, and 5 with all 7 principles, 4 optional modules, and valid placeholder tokens.

### Implementation for User Story 1

- [X] T004 [P] [US1] Author Sync Impact Report comment header and Sources of Truth & Authority Hierarchy with placeholders `[PRIMARY_SOURCE]`, `[SECONDARY_SOURCE]`, `[TERTIARY_SOURCE]` in `.specify/templates/constitution-template.md`
- [X] T005 [US1] Author Core Principles I and II in `.specify/templates/constitution-template.md`, embedding Module A inline after `- **Centralized Open Questions**:` using delimiters `<!-- OPTIONAL-MODULE: MODULE-A\nAction: ADD\nTitle: In-Code Open Question Pointers\nTarget: Principle I\n-->` and `<!-- /OPTIONAL-MODULE: MODULE-A -->` per `specs/001-base-governance-templates/contracts/optional-module-delimiters.md`
- [X] T006 [US1] Author Core Principle III in `.specify/templates/constitution-template.md`, enclosing the Plan Justification bullet and 5 allowlist items in `<!-- DEFAULT-CLAUSE: PLAN-JUSTIFICATION-AND-SKIP-ALLOWLIST (REPLACEABLE-BY: MODULE-B)\nTarget: Principle III\n-->` and appending Module B `<!-- OPTIONAL-MODULE: MODULE-B\nAction: REPLACE\nTarget: Principle III\nReplaces: PLAN-JUSTIFICATION-AND-SKIP-ALLOWLIST\nTitle: Strict 100% Branch Coverage Profile\n-->` per `specs/001-base-governance-templates/contracts/optional-module-delimiters.md`
- [X] T007 [US1] Author Core Principles IV, V, VI, and VII in `.specify/templates/constitution-template.md`, embedding Module C inline after Principle IV Disambiguated Colliding Identifiers bullet, and Module D inline after Principle V Human-Only Toolchain bullet including nested sub-clause `<!-- OPTIONAL-SUBCLAUSE: MODULE-D-AOT-TRIM\nAction: OPTIONAL-INCLUSION\nParent-Module: MODULE-D\nTitle: AOT / Trim-Safe Shared Libraries\n-->` per `specs/001-base-governance-templates/contracts/optional-module-delimiters.md`
- [X] T008 [US1] Author Development Workflow, Recorded Deviations, and Governance sections in `.specify/templates/constitution-template.md` with placeholder `[ACCEPTANCE_GATE_COMMANDS]`, companion standards cross-references (`coding-standards.md` / `CodingStandards.md` and `logging-standards.md` / `docs/logging.md`), 6-tier Precedence Order, and footer `**Version**: 1.0.0 | **Ratified**: [YYYY-MM-DD] | **Last Amended**: [YYYY-MM-DD]`
- [X] T009 [US1] Validate `constitution-template.md` against Scenario 1, Scenario 2, and Scenario 5 via `python3 tests/test_governance_templates.py` and verify CLI resolution via `.specify/scripts/bash/resolve-template.sh constitution-template --json`

**Checkpoint**: At this point, User Story 1 (MVP) is fully functional, complete, and testable independently.

---

## Phase 4: User Story 2 - Resolve Companion Coding Standards Template (Priority: P2)

**Goal**: Deliver language-agnostic companion coding standards template in `.specify/templates/coding-standards-template.md` operationalizing constitutional boundaries, concurrency, two-tier error handling, and testing into daily coding standards with standardized `[ALL_CAPS_IDENTIFIER]` project slots.

**Independent Test**: Run `python3 tests/test_governance_templates.py` and verify `.specify/templates/coding-standards-template.md` passes Scenarios 1, 3, and 5 with all baseline universal rules and project-specific customization placeholders.

### Implementation for User Story 2

- [X] T010 [P] [US2] Author Constitutional Authority Link, Precedence declaration, and Compile-Time & Architectural Boundaries section in `.specify/templates/coding-standards-template.md`
- [X] T011 [US2] Author Two-Tier Failure Handling, Concurrency & Immutable Snapshots (`record` / `record struct`), and Disambiguated Identifier Value Types (`readonly record struct`) sections in `.specify/templates/coding-standards-template.md`
- [X] T012 [US2] Author Bounded Inputs & Resource Protection, Verify Before Mutate/Destroy, Hostile Boundary & Behavioral Unit Testing, and Code Hygiene & Commenting Conventions sections in `.specify/templates/coding-standards-template.md`
- [X] T013 [US2] Author Project Conventions section with required placeholders verbatim: `[PROJECT_NAME]`, `[PRIMARY_LANGUAGE_AND_RUNTIME]`, `[BUILD_AND_LINTER_COMMANDS]`, `[PROJECT_STRUCTURE_CONVENTIONS]`, `[NAMING_CONVENTIONS]`, `[ERROR_RESULT_TYPES]`, and `[TEST_FRAMEWORK_CONVENTIONS]` with exemplary commentary in `.specify/templates/coding-standards-template.md`
- [X] T014 [US2] Validate `coding-standards-template.md` against Scenario 1, Scenario 3, and Scenario 5 via `python3 tests/test_governance_templates.py` and verify CLI resolution via `.specify/scripts/bash/resolve-template.sh coding-standards-template --json`

**Checkpoint**: At this point, User Stories 1 AND 2 both work independently and resolve reliably.

---

## Phase 5: User Story 3 - Resolve Companion Logging Standards Template (Priority: P3)

**Goal**: Deliver companion logging standards template in `.specify/templates/logging-standards-template.md` operationalizing Principles II and VII into concrete observability rules, the 5-tier severity taxonomy (`CRITICAL`, `WARN`, `INFO`, `DEBUG`, `TRACE`), ambient scope correlation, secret redaction, and project-specific telemetry slots.

**Independent Test**: Run `python3 tests/test_governance_templates.py` and verify `.specify/templates/logging-standards-template.md` passes Scenarios 1, 4, and 5 with the 5-tier severity taxonomy, ambient correlation, redaction rules, and project-specific placeholders.

### Implementation for User Story 3

- [X] T015 [P] [US3] Author Constitutional Authority Link, Precedence declaration, and Five-Tier Severity Taxonomy (`CRITICAL`, `WARN`, `INFO`, `DEBUG`, `TRACE`) mapped to Two-Tier Failure Model in `.specify/templates/logging-standards-template.md`
- [X] T016 [US3] Author Detailed Level Placement Rules, TRACE mechanical entry/exit rules, and External Library logging rules in `.specify/templates/logging-standards-template.md`
- [X] T017 [US3] Author Ambient Scope Correlation (`session_id`, `event_id`), Forbidden Data Redaction Policy (passwords, tokens, API keys, full credit cards, SSNs, raw PII), Performance Level Guards (>100/sec sampling), and Testing Boundary Rules in `.specify/templates/logging-standards-template.md`
- [X] T018 [US3] Author Project Telemetry Configuration section with required placeholders verbatim: `[PROJECT_NAME]`, `[LOGGING_FRAMEWORK]`, `[LOG_SINKS_AND_FORMATS]`, `[CORRELATION_ID_SCHEMA]`, `[SENSITIVE_DATA_REDACTION_MECHANISM]`, and `[RETENTION_AND_SAMPLING_POLICY]` in `.specify/templates/logging-standards-template.md`
- [X] T019 [US3] Validate `logging-standards-template.md` against Scenario 1, Scenario 4, and Scenario 5 via `python3 tests/test_governance_templates.py` and verify CLI resolution via `.specify/scripts/bash/resolve-template.sh logging-standards-template --json`

**Checkpoint**: All three user stories are now independently functional, testable, and resolvable.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Verification and documentation consistency across all templates

- [X] T020 [P] Validate cross-template placeholder token consistency across all three templates against `specs/001-base-governance-templates/contracts/placeholder-tokens.md`
- [X] T021 [P] Execute full verification test suite running all scenarios from `specs/001-base-governance-templates/quickstart.md`
- [X] T022 Document template installation, resolver priority behavior, and Phase 2 merge hooks in `specs/001-base-governance-templates/quickstart.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - starts immediately.
- **Foundational (Phase 2)**: Depends on Setup (Phase 1) - BLOCKS all user stories by providing the automated test harness.
- **User Stories (Phases 3–5)**: All depend on Foundational (Phase 2) completion.
  - Can proceed sequentially in priority order (P1 → P2 → P3).
  - Can also proceed in parallel across stories since each story operates on an isolated template file (`constitution-template.md`, `coding-standards-template.md`, `logging-standards-template.md`).
- **Polish (Phase 6)**: Depends on all user stories (Phases 3, 4, 5) being complete.

### User Story Dependencies

- **User Story 1 (P1)**: Starts immediately after Phase 2. Zero dependencies on US2 or US3.
- **User Story 2 (P2)**: Starts after Phase 2. Independently testable; references `constitution.md` conceptually but does not depend on US1 file changes.
- **User Story 3 (P3)**: Starts after Phase 2. Independently testable; references `constitution.md` Principles II/VII conceptually but does not depend on US1 or US2 file changes.

### Within Each User Story

- Foundational validation test harness created before implementation tasks.
- Header and authority links authored before individual principle/policy sections.
- Universal baseline sections authored before project customization placeholder sections.
- Story validation task executed to confirm independent acceptance criteria before declaring story complete.

### Parallel Opportunities

- Foundational tasks `T002` and `T003` can execute in parallel.
- Once Phase 2 completes, User Stories 1, 2, and 3 can be authored in parallel by separate agents/engineers because their target files are disjoint:
  - US1: `.specify/templates/constitution-template.md`
  - US2: `.specify/templates/coding-standards-template.md`
  - US3: `.specify/templates/logging-standards-template.md`
- Polish tasks `T020` and `T021` can execute in parallel.

---

## Parallel Example: User Stories 1, 2, and 3

```bash
# Once Phase 2 is complete, different developers or agents can implement templates in parallel:
Developer A: T004-T009 on .specify/templates/constitution-template.md (US1)
Developer B: T010-T014 on .specify/templates/coding-standards-template.md (US2)
Developer C: T015-T019 on .specify/templates/logging-standards-template.md (US3)
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (`T001`).
2. Complete Phase 2: Foundational test suite (`T002`, `T003`).
3. Complete Phase 3: User Story 1 (`T004` through `T009`).
4. **STOP and VALIDATE**: Verify `constitution-template.md` independently via `tests/test_governance_templates.py` and `resolve-template.sh`.
5. Deliver MVP base constitution template.

### Incremental Delivery

1. Complete Setup + Foundational → Test harness operational.
2. Deliver US1 (`constitution-template.md`) → Validate independently → MVP ready!
3. Deliver US2 (`coding-standards-template.md`) → Validate independently → Coding standards operational.
4. Deliver US3 (`logging-standards-template.md`) → Validate independently → Full governance suite operational.
5. Complete Phase 6: Polish → Final cross-template audit.

---

## Notes

- All tasks strictly follow `- [ ] [TaskID] [P?] [Story?] Description with file path`.
- Every placeholder token strictly matches `[ALL_CAPS_IDENTIFIER]` or `[YYYY-MM-DD]` per contract.
- Optional modules strictly follow HTML comment delimiter contracts from `contracts/optional-module-delimiters.md`.
- No bash scripts in `.specify/scripts/bash/` are modified; templates resolve automatically at Priority 4.
