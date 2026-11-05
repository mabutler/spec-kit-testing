# Tasks: Claude Discovery Compatibility & Constitutional Test Decoupling

**Input**: Design documents from `/specs/007-claude-discovery-governance-decoupling/`

**Prerequisites**: [`plan.md`](plan.md), [`spec.md`](spec.md), [`research.md`](research.md), [`data-model.md`](data-model.md), [`contracts/`](contracts/)

**Documentation Impact**: `USER_FACING` — Updates root [`README.md`](../../README.md) (canonical sections for dual `.agents/` and `.claude/` discovery, bootstrapper seeding, and manifest verification) and [`ROADMAP.md`](../../ROADMAP.md) (Phase 7 status synchronization).

**Tests**: None. Repository-wide verification is conducted strictly via static analysis, schema validation, line-budget checks, and cryptographic SHA-256 manifest validation per `.specify/memory/constitution.md` Principle III (*Static Verification & No Automated Tests*). Spec Kit feature workflows MUST NOT generate unit test files, integration test harnesses, or test tasks.

**Organization**: Tasks are grouped by user story to enable independent implementation and static verification of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., `US1`, `US2`, `US3`)
- File paths are exact and repository-relative

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Repository baseline inspection and shared configuration setup.

- [x] T001 Inspect workspace and verify clean baseline status and directories per implementation plan in specs/007-claude-discovery-governance-decoupling/plan.md
- [x] T002 [P] Update repository root .gitignore to ignore machine-local files for both Google Antigravity (.agents/agents/*.local.md) and Claude Code (.claude/agents/*.local.md, .claude/settings.local.json) per FR-003

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete.

- [x] T003 [P] Update bootstrap-speckit.sh to pre-verify source bundle assets, count seeded files across .specify, .agents, and .claude, enforce dual .gitignore patterns (.agents/agents/*.local.md, .claude/agents/*.local.md, .claude/settings.local.json), and maintain PRESERVE_USER_STATE boundary while remaining under 150 LOC in bootstrap-speckit.sh
- [x] T004 [P] Update bootstrap-speckit.ps1 to pre-verify source bundle assets, count seeded files across .specify, .agents, and .claude, enforce dual .gitignore patterns (.agents/agents/*.local.md, .claude/agents/*.local.md, .claude/settings.local.json), and maintain PRESERVE_USER_STATE boundary while remaining under 150 LOC in bootstrap-speckit.ps1
- [x] T005 Initialize .claude/ directory layout (.claude/agents/ and .claude/skills/ with all 12 skill subdirectories) in .claude/

**Checkpoint**: Foundational scaffolding and bootstrapper scripts prepared — user story implementation can begin.

---

## Phase 3: User Story 1 - Claude Code Skill & Subagent Discovery Compatibility (Priority: P1) 🎯 MVP

**Goal**: Establish native Claude Code skill and subagent discovery compatibility alongside Google Antigravity by updating the bootstrap skill and populating `.claude/` with all canonical assets.

**Independent Test**: Verify all 12 skills exist in both `.agents/` and `.claude/`, run `bootstrap-speckit.sh` against an ephemeral target directory, and confirm `.agents/`, `.claude/`, and dual `.gitignore` entries are created.

### Implementation for User Story 1

- [x] T006 [US1] Update .agents/skills/speckit-bootstrap/SKILL.md to inspect, verify, and synchronize both .agents/ and .claude/ installations and validate claude.manifest.json alongside agy.manifest.json per FR-005
- [x] T007 [P] [US1] Copy and mirror all 9 unchanged skills (speckit-analyze, speckit-checklist, speckit-clarify, speckit-constitution, speckit-converge, speckit-implement, speckit-plan, speckit-specify, speckit-tasks) from .agents/skills/ to .claude/skills/ per FR-001
- [x] T008 [US1] Mirror .agents/skills/speckit-bootstrap/SKILL.md to .claude/skills/speckit-bootstrap/SKILL.md ensuring 100% byte-for-byte parity per FR-001 and SC-001
- [x] T009 [US1] Execute static acceptance test for User Story 1 validating bootstrapper syntax (bash -n bootstrap-speckit.sh) and target seeding into an ephemeral directory per specs/007-claude-discovery-governance-decoupling/quickstart.md Section 3

**Checkpoint**: At this point, User Story 1 is functional and verifiable independently as the MVP milestone.

---

## Phase 4: User Story 2 - Dynamic Constitutional Deference for Verification & Testing (Priority: P2)

**Goal**: Decouple hardcoded test prohibitions from reusable subagent profiles and skills, deferring dynamically to the project's active constitution (`.specify/memory/constitution.md`) and companion standards at runtime.

**Independent Test**: Inspect `.agents/agents/*.md`, `.claude/agents/*.md`, and workflow skills to verify zero occurrences of hardcoded test prohibitions, and confirm the orchestrator dynamically reads `.specify/memory/constitution.md`.

### Implementation for User Story 2

- [x] T010 [P] [US2] Refactor .agents/agents/speckit-executor.md to add dual-client persona header ("Google Antigravity or Claude Code"), conform frontmatter to dual-client schema (valid YAML for both Claude Code and Antigravity: name, description, model, speckit_role_tier, speckit_default_stages, speckit_tool_policy), and replace hardcoded Principle III prohibition with dynamic deference clause per FR-006 and contracts/constitutional-deference-contract.md
- [x] T011 [P] [US2] Refactor .agents/agents/speckit-reasoner.md to add dual-client persona header ("Google Antigravity or Claude Code"), conform frontmatter to dual-client schema (valid YAML for both Claude Code and Antigravity: name, description, model, speckit_role_tier, speckit_default_stages, speckit_tool_policy), and replace hardcoded Principle III prohibition with dynamic deference clause per FR-006 and contracts/constitutional-deference-contract.md
- [x] T012 [P] [US2] Refactor .agents/skills/speckit-orchestrate/SKILL.md Section 3 (fail-closed check on missing constitution + dynamic Principle III policy passing), Section 4 (dual .agents/ and .claude/ client resolution hierarchy), Section 5 (dual-client subagent dispatch mapping for Antigravity vs Claude Code Task tool + dynamic prompt payload), and Section 6 (dual client skill paths) per FR-007 and contracts/constitutional-deference-contract.md
- [x] T013 [P] [US2] Refactor .agents/skills/speckit-roadmap/SKILL.md Section 8 to reference general constitutional verification gates rather than hardcoding "Principle III (Zero Automated Tests)" per FR-008 and contracts/constitutional-deference-contract.md
- [x] T014 [US2] Synchronize modified subagent profiles (.agents/agents/speckit-executor.md and .agents/agents/speckit-reasoner.md) to .claude/agents/ ensuring 100% byte-for-byte parity per FR-001 and SC-001
- [x] T015 [US2] Synchronize modified skills (.agents/skills/speckit-orchestrate/SKILL.md and .agents/skills/speckit-roadmap/SKILL.md) to .claude/skills/ ensuring 100% byte-for-byte parity per FR-001 and SC-001
- [x] T016 [US2] Execute static acceptance test for User Story 2 by scanning .agents/ and .claude/ for hardcoded test prohibitions and confirming zero matches per specs/007-claude-discovery-governance-decoupling/quickstart.md Section 2

**Checkpoint**: At this point, User Stories 1 AND 2 are fully integrated and verifiable independently.

---

## Phase 5: User Story 3 - Living Documentation, Manifest Parity & Quality Gates (Priority: P3)

**Goal**: Generate cryptographic integration manifests, synchronize root `README.md` and `ROADMAP.md` in compliance with Principle VII (`MODULE-DOCS`), and verify zero manifest drift.

**Independent Test**: Verify all 4 integration manifests match on-disk file SHA-256 digests, and confirm `README.md` documents dual discovery and bootstrapper usage with zero broken relative links.

### Implementation for User Story 3

- [x] T017 [P] [US3] Create .specify/integrations/claude.manifest.json tracking all 14 .claude/ files with exact 64-character lowercase hex SHA-256 digests matching agy.manifest.json per FR-004 and contracts/dual-client-bootstrap-contract.md
- [x] T018 [P] [US3] Update .specify/integrations/agy.manifest.json with recalculated SHA-256 digests for all modified files in .agents/ per FR-010
- [x] T019 [US3] Update .specify/integrations/speckit-bootstrap.manifest.json to track all 53 managed files across .agents/ (14), .claude/ (14), and .specify/ (25 including claude.manifest.json) with accurate "digest": "sha256:<hex>" and "size_bytes": <int> per FR-004, FR-010, and data-model.md
- [x] T020 [US3] Verify .specify/integrations/speckit.manifest.json digests match current template and .gitignore contents with zero drift per FR-010
- [x] T021 [P] [US3] Update root README.md canonical sections (1. Project Overview & 4-Tier Architecture, 2. Co-Applied Governance Suite, 3. Spec Kit Skills & Subagent Orchestration Reference, 4. Portable Bootstrapping & Verification Quickstart) per FR-009, Principle VII, and .specify/memory/coding-standards.md
- [x] T022 [P] [US3] Update ROADMAP.md Phase 7 status from IN_PROGRESS to COMPLETED and update deliverables list per FR-009
- [x] T023 [US3] Execute static acceptance test for User Story 3 by running SHA-256 manifest verification across all 4 manifests per specs/007-claude-discovery-governance-decoupling/quickstart.md Section 4

**Checkpoint**: All user stories implemented, manifests synchronized, and documentation aligned.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Repository-wide static verification across all components, line budgets, and quality gates.

- [x] T024 [P] Execute dual-client asset existence and byte-identical parity check across all 14 canonical files in .agents/ and .claude/ per specs/007-claude-discovery-governance-decoupling/quickstart.md Section 1 and SC-001
- [x] T025 [P] Execute script line count and syntax validation (bash -n) ensuring bootstrap-speckit.sh and bootstrap-speckit.ps1 are both under 150 LOC per specs/007-claude-discovery-governance-decoupling/quickstart.md Section 3
- [x] T026 [P] Execute documentation hygiene and link validation check on README.md and ROADMAP.md ensuring zero broken relative links and zero citations of ephemeral specs/ paths per specs/007-claude-discovery-governance-decoupling/quickstart.md Section 5
- [x] T027 Run full /speckit-bootstrap --check simulation verifying zero configuration drift across .specify/, .agents/, and .claude/

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — executes immediately.
- **Foundational (Phase 2)**: Depends on Setup completion — BLOCKS all user stories.
- **User Story 1 (Phase 3)**: Depends on Foundational completion (T001–T005). Delivers the initial MVP.
- **User Story 2 (Phase 4)**: Depends on Foundational completion and US1 initial tree setup. Refactors profiles and skills.
- **User Story 3 (Phase 5)**: Depends on US1 and US2 completion to compute final SHA-256 digests and document finalized behaviors.
- **Polish (Phase 6)**: Depends on all user stories (Phases 3–5) being complete.

### User Story Dependencies

- **User Story 1 (P1)**: Establishes `.claude/` mirrored tree, updates `bootstrap-speckit.{sh,ps1}`, and updates `speckit-bootstrap/SKILL.md`. Blocks final manifest creation in US3.
- **User Story 2 (P2)**: Refactors subagent profiles (`speckit-executor.md`, `speckit-reasoner.md`) and skills (`speckit-orchestrate`, `speckit-roadmap`) for dynamic constitutional deference, then mirrors them to `.claude/`. Blocks manifest calculation in US3.
- **User Story 3 (P3)**: Generates SHA-256 manifests (`claude.manifest.json`, `agy.manifest.json`, `speckit-bootstrap.manifest.json`), updates root `README.md` and `ROADMAP.md`. Depends on finalized file contents from US1 and US2.

### Within Each User Story

- Foundational prerequisites before story tasks.
- Source `.agents/` modifications before copying/mirroring to `.claude/` to guarantee parity.
- Code/asset edits before manifest recalculation.
- Story acceptance static check as the final task in each story phase.

### Parallel Opportunities

- Within Phase 1: `T002` can run alongside `T001`.
- Within Phase 2: `T003` and `T004` (Bash vs. PowerShell scripts) can be developed in parallel.
- Within Phase 3: `T007` (copying unchanged skills) can run in parallel with `T006`.
- Within Phase 4: `T010`, `T011`, `T012`, and `T013` (editing distinct persona and skill files) can run in parallel.
- Within Phase 5: `T017` and `T018` can be drafted in parallel before unifying into `T019`; `T021` and `T022` (documentation edits) can run in parallel.
- Within Phase 6: `T024`, `T025`, and `T026` can run concurrently across independent validation dimensions.

---

## Parallel Example: User Story 2

```bash
# Refactor all agent profiles and workflow skills in parallel:
Task: "Refactor .agents/agents/speckit-executor.md to add dual-client persona header and dynamic Principle III deference clause"
Task: "Refactor .agents/agents/speckit-reasoner.md to add dual-client persona header and dynamic Principle III deference clause"
Task: "Refactor .agents/skills/speckit-orchestrate/SKILL.md Section 3, Section 4, Section 5, and Section 6"
Task: "Refactor .agents/skills/speckit-roadmap/SKILL.md Section 8 to reference general constitutional verification gates"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (`T001`, `T002`).
2. Complete Phase 2: Foundational (`T003`–`T005`).
3. Complete Phase 3: User Story 1 (`T006`–`T009`).
4. **STOP and VALIDATE**: Confirm Claude Code discovery tree exists and bootstrapper seeds both `.agents/` and `.claude/`.

### Incremental Delivery

1. Setup + Foundational → Repository ready for dual-client discovery.
2. User Story 1 → Claude Code discovers all skills and agents; bootstrapper seeds both environments (MVP!).
3. User Story 2 → Subagent personas and orchestrator skills dynamically defer to project constitution without hardcoded prohibitions.
4. User Story 3 → Cryptographic SHA-256 manifests verified, `README.md` and `ROADMAP.md` synchronized.
5. Polish → Full static validation suite passes cleanly (`SC-001` through `SC-005`).

---

## Notes

- `[P]` tasks = different files, no shared dependencies.
- `[Story]` label maps each story task to `US1`, `US2`, or `US3` for strict traceability.
- All verification uses static analysis (`bash -n`, `filecmp`, SHA-256 digest validation, markdown linting) in compliance with Constitution Principle III.
- Commit after each logical group or user story phase.
