# Tasks: Clean Up README and Focus on Unique Repository Capabilities

<!--
Template Resolution Hierarchy & FeatureContext Specification:
Resolved via Tier 4 Fallback: .specify/templates/tasks-template.md
FeatureContext: specs/010-clean-readme
-->

**Input**: Design documents from `/specs/010-clean-readme/`

**Prerequisites**: `plan.md` (required), `spec.md` (required for user stories), `research.md`, `data-model.md`, `contracts/readme-schema.md`, `quickstart.md`

**Documentation Impact**: USER_FACING (`README.md` is updated to conform to canonical 4-section architecture)

**Tests**: None (Principle III static verification; zero automated unit or integration tests repository-wide per `.specify/memory/constitution.md`)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Root Documentation**: `README.md` at repository root
- **Feature Specification**: `specs/010-clean-readme/`
- **Governance Suite**: `.specify/memory/`
- **Templates & Presets**: `.specify/templates/`, `.specify/presets/`
- **Antigravity & Claude Configs**: `.agents/`, `.claude/`

---

## Phase 1: Setup (Environment & Verification Baseline)

**Purpose**: Baseline inspection and verification of existing documentation state

- [x] T001 Inspect existing baseline line count (137 lines) and section structure of `README.md`
- [x] T002 Inspect and verify schema constraints in `specs/010-clean-readme/contracts/readme-schema.md` and static verification checks in `specs/010-clean-readme/quickstart.md`

---

## Phase 2: Foundational (Structural Architecture & Canonical Sections)

**Purpose**: Document structure initialization that MUST be complete before user story content is populated

**⚠️ CRITICAL**: Establish canonical section skeleton before refining individual sections

- [x] T003 Restructure the document header and create the 4 canonical section skeleton in `README.md` with heading `# Spec Kit Customizations` and section headings matching `"Project Overview & 4-Tier Architecture"`, `"Co-Applied Governance Suite"`, `"Spec Kit Skills & Subagent Orchestration Reference"`, and `"Portable Bootstrapping & Verification Quickstart"` per constraint `"Exactly 4 sections"`

**Checkpoint**: Canonical 4-section layout established in `README.md`; user story content implementation can begin.

---

## Phase 3: User Story 1 - Remove Generic Template Governance Boilerplate (Priority: P1) 🎯 MVP

**Goal**: Clean up governance and architecture descriptions in `README.md`, eliminating generic principle matrices and optional module catalogs in favor of concise summaries and direct links.

**Independent Test**: Review Section 1 and Section 2 of `README.md` to confirm direct links to `.specify/memory/constitution.md`, `.specify/memory/coding-standards.md`, and `.specify/memory/logging-standards.md` exist and that generic tables are eliminated (`0 occurrences of Core Principles table (| Principle |)` and `0 occurrences of ### Optional Modules`).

### Tests for User Story 1
*None: Automated unit tests disabled repository-wide per Constitution Principle III. Static verification checks specified in Phase 6.*

### Implementation for User Story 1

- [x] T004 [US1] Author Section 1 under `## Project Overview & 4-Tier Architecture` in `README.md` detailing the upstream GitHub Spec Kit link (`https://github.com/github/spec-kit`), the 4-tier lookup hierarchy (`Tier 1: Project Overrides (.specify/templates/overrides/)`, `Tier 2: Presets (.specify/presets/)`, `Tier 3: Extensions (.specify/extensions/)`, `Tier 4: Core Fallback (.specify/templates/)`), and dual client parity across `.agents/` and `.claude/`
- [x] T005 [US1] Author Section 2 under `## Co-Applied Governance Suite` in `README.md` summarizing the tripartite governance model with direct links to `.specify/memory/constitution.md`, `.specify/memory/coding-standards.md`, and `.specify/memory/logging-standards.md` while enforcing constraints: `"0 occurrences of Core Principles table (| Principle |)"` and `"0 occurrences of ### Optional Modules"`

**Checkpoint**: User Story 1 complete. `README.md` Sections 1 & 2 are clean, concise, and free of generic template boilerplate.

---

## Phase 4: User Story 2 - Focus Tooling & Skills on Unique Additions (Priority: P1)

**Goal**: Spotlight custom skills and subagent personas in `README.md` without duplicating standard upstream Spec Kit command tables.

**Independent Test**: Review Section 3 of `README.md` to confirm `speckit-reasoner`, `speckit-executor`, `/speckit-orchestrate`, `/speckit-bootstrap`, and `/speckit-roadmap` are documented with zero individual table rows for standard upstream skills (`specify`, `plan`, `tasks`, `implement`).

### Tests for User Story 2
*None: Automated unit tests disabled repository-wide per Constitution Principle III. Static verification checks specified in Phase 6.*

### Implementation for User Story 2

- [x] T006 [US2] Author `### Subagent Personas` subsection under `## Spec Kit Skills & Subagent Orchestration Reference` in `README.md` defining `speckit-reasoner` and `speckit-executor` with relative links to [`.agents/agents/`](.agents/agents/) and [`.claude/agents/`](.claude/agents/)
- [x] T007 [US2] Author `### Custom Skills` and `### Core Pipeline Integration` subsections under `## Spec Kit Skills & Subagent Orchestration Reference` in `README.md` showcasing `/speckit-orchestrate`, `/speckit-bootstrap`, and `/speckit-roadmap` with links while enforcing constraint `"No individual table rows for standard upstream skills"` and explaining how standard pipeline stages are dynamically governed by the constitution

**Checkpoint**: User Story 2 complete. Section 3 focuses strictly on unique additions and subagent orchestration.

---

## Phase 5: User Story 3 - Highlight Installation, Portability, and Verification (Priority: P2)

**Goal**: Highlight portable bootstrapping instructions, governance initialization, and static verification check commands within Section 4 of `README.md`.

**Independent Test**: Execute the documented verification commands from Section 4 in `README.md` in a terminal and confirm all exit with code 0.

### Tests for User Story 3
*None: Automated unit tests disabled repository-wide per Constitution Principle III. Static verification checks specified in Phase 6.*

### Implementation for User Story 3

- [x] T008 [US3] Author Section 4 under `## Portable Bootstrapping & Verification Quickstart` in `README.md` containing subsections for Installation & Target Seeding (`bootstrap-speckit.sh` and `bootstrap-speckit.ps1`), Governance Initialization (`/speckit-bootstrap --check` and `/speckit-constitution`), and Verification Checks (`bash -n bootstrap-speckit.sh`, `diff -r .agents .claude`, `cmp -s .specify/templates/constitution-template.md .specify/presets/base-governance/templates/constitution-template.md`, `cmp -s .specify/templates/coding-standards-template.md .specify/presets/base-governance/templates/coding-standards-template.md`, `cmp -s .specify/templates/logging-standards-template.md .specify/presets/base-governance/templates/logging-standards-template.md`)

**Checkpoint**: All three user stories implemented in `README.md`.

---

## Phase 6: Static Verification & Quality Gates (Principle III)

**Purpose**: Execute declarative static analysis, link integrity validation, line count checks, and syntax checks (zero automated test files)

- [x] T009 [P] Validate canonical section headings and boilerplate elimination in `README.md` using Scenario 1 and Scenario 3 commands from `specs/010-clean-readme/quickstart.md`
- [x] T010 [P] Validate total line count ceiling of `README.md` enforcing constraint `"Must be <= 104 lines (>= 25% reduction from 137 lines)"` using Scenario 2 command from `specs/010-clean-readme/quickstart.md`
- [x] T011 [P] Validate relative link integrity in `README.md` enforcing constraint `"100% of local links must resolve to valid disk paths"` using Scenario 5 script from `specs/010-clean-readme/quickstart.md`
- [x] T012 [P] Validate execution of documented verification commands (`bash -n`, `diff -r`, `cmp -s`) per Scenario 6 from `specs/010-clean-readme/quickstart.md`

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final formatting conformance, git diff review, and constitutional governance validation

- [x] T013 Verify markdown formatting, relative link syntax, and clean git diff in `README.md`
- [x] T014 Verify repository-wide constitutional compliance ensuring zero automated test files were added per Principle III across `specs/010-clean-readme/` and repository root

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately.
- **Foundational (Phase 2)**: Depends on Phase 1 baseline inspection - BLOCKS all user story implementations.
- **User Story 1 (Phase 3 - P1)**: Depends on Phase 2 structure setup.
- **User Story 2 (Phase 4 - P1)**: Depends on Phase 2 structure setup.
- **User Story 3 (Phase 5 - P2)**: Depends on Phase 2 structure setup.
- **Static Verification (Phase 6)**: Depends on Phases 3, 4, and 5 completion.
- **Polish (Phase 7)**: Depends on Phase 6 passing.

### User Story Dependencies

- **User Story 1 (P1)**: Edits Sections 1 and 2 in `README.md`. Can start immediately after Phase 2.
- **User Story 2 (P1)**: Edits Section 3 in `README.md`. Can start after Phase 2 (or sequential after US1 to avoid concurrent edits to `README.md`).
- **User Story 3 (P2)**: Edits Section 4 in `README.md`. Can start after Phase 2 (or sequential after US2).

### Parallel Opportunities

- Verification tasks T009, T010, T011, and T012 can all run in parallel in Phase 6 because they are read-only validation commands.
- Implementation tasks T004 through T008 target different sections of the same file `README.md` and should be applied sequentially by a single agent to avoid file conflicts.

---

## Parallel Example: Static Verification Phase

```bash
# Launch parallel static verification commands (Phase 6):
Task T009: grep -E '^## (Project Overview & 4-Tier Architecture|Co-Applied Governance Suite|Spec Kit Skills & Subagent Orchestration Reference|Portable Bootstrapping & Verification Quickstart)' README.md
Task T010: [ $(wc -l < README.md) -le 104 ]
Task T011: python3 -c "import re, os; ... [check relative links] ..."
Task T012: bash -n bootstrap-speckit.sh && diff -r .agents .claude && cmp -s .specify/templates/constitution-template.md .specify/presets/base-governance/templates/constitution-template.md
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup inspection
2. Complete Phase 2: Establish canonical 4-section skeleton
3. Complete Phase 3: User Story 1 (Sections 1 & 2 cleanup)
4. **STOP and VALIDATE**: Verify that generic boilerplate tables are eliminated and relative links work
5. Proceed to remaining user stories

### Incremental Delivery

1. Phase 1 + Phase 2 → Skeleton ready
2. Phase 3 (US1) → Governance and overview streamlined (MVP)
3. Phase 4 (US2) → Skills reference focused on unique capabilities
4. Phase 5 (US3) → Bootstrapping and static verification quickstart consolidated
5. Phase 6 → Static validation commands confirm all constraints pass
6. Phase 7 → Final polish and constitutional compliance check

---

## Notes

- [P] tasks = read-only static verification commands that can execute in parallel
- [Story] label maps task to specific user story (US1, US2, US3) for traceability
- No automated unit test suites (`tests/`, `*.test.*`) are created per Constitution Principle III
- Verbatim constraint quotes ensure unambiguous implementation boundaries
