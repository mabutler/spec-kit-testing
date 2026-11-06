# Tasks: Add --update Flag to speckit-orchestrate for Non-Destructive Architectural Replanning

**Input**: Design documents from `/specs/011-orchestrate-update-flag/`
**Prerequisites**: [spec.md](specs/011-orchestrate-update-flag/spec.md), [plan.md](specs/011-orchestrate-update-flag/plan.md), [research.md](specs/011-orchestrate-update-flag/research.md), [data-model.md](specs/011-orchestrate-update-flag/data-model.md), [contracts/orchestrate-update-interface.md](specs/011-orchestrate-update-flag/contracts/orchestrate-update-interface.md), [quickstart.md](specs/011-orchestrate-update-flag/quickstart.md)
**Documentation Impact**: `USER_FACING` — Updates root `README.md` under `## Spec Kit Skills & Subagent Orchestration Reference -> ### Custom Skills` to document the new `--update` and `--amend` replanning flags in Phase 8 (Polish).
**Tests**: Automated tests are omitted repository-wide per Constitution Principle III (*Static Verification & Quality Gates*). Quality verification is performed via static parity diffs (`diff -u`, `cmp -s`), link validation, and runnable scenario walkthroughs documented in `quickstart.md`.
**Organization**: Tasks are grouped by user story (US1 through US5) across setup, foundational, user story phases, and polish to enable independent implementation and verification.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4, US5)
- Exact file paths are included in all task descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Baseline inspection and environment verification

- [x] T001 Inspect baseline orchestrator skills in `.agents/skills/speckit-orchestrate/SKILL.md` and `.claude/skills/speckit-orchestrate/SKILL.md` to confirm initial byte parity and clean git status
- [x] T002 [P] Record baseline SHA-256 hash of core planning skills in `.agents/skills/speckit-plan/SKILL.md` and `.claude/skills/speckit-plan/SKILL.md` to enforce constraint VR-05 ("sha256(.agents/skills/speckit-plan/SKILL.md) and sha256(.claude/skills/speckit-plan/SKILL.md) MUST remain unmodified")
- [x] T003 [P] Inspect `README.md` section "## Spec Kit Skills & Subagent Orchestration Reference -> ### Custom Skills" to establish baseline CLI documentation

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core replanning state variables and task preservation invariants required across all user stories

**⚠️ CRITICAL**: Foundational state declarations and invariants MUST be established before user story workflows begin

- [x] T004 Define replanning context schema and state variables (`IS_UPDATE_MODE`, `UPDATE_DESCRIPTION`) in `.agents/skills/speckit-orchestrate/SKILL.md` matching `contracts/orchestrate-update-interface.md`
- [x] T005 Define task monotonicity rules and artifact preservation invariants in `.agents/skills/speckit-orchestrate/SKILL.md` enforcing constraint VR-04 ("For all TaskItem in tasks.md where status == COMPLETED before an --update run: Post-condition: status MUST remain COMPLETED (- [x]), and task line content MUST remain intact")

**Checkpoint**: Foundation ready — user story implementations can now begin

---

## Phase 3: User Story 1 - Non-Destructive Architectural Replanning via `--update` / `--amend` Flag (Priority: P1) 🎯 MVP

**Goal**: Enable non-destructive replanning in `speckit-orchestrate` across Stage 3 (Plan) and Stage 4 (Tasks), preserving completed tasks and amending design artifacts in place.

**Independent Test**: Execute simulated replanning on a feature with existing planning documents and completed tasks in `tasks.md`, verifying that existing files and completed `- [x]` tasks are retained while `plan.md` and pending `- [ ]` tasks are updated per `specs/011-orchestrate-update-flag/quickstart.md` Scenario 5.

### Implementation for User Story 1

- [x] T006 [US1] Update Stage 3 (Plan) execution condition in `.agents/skills/speckit-orchestrate/SKILL.md` to force execution when `is_update_mode == true` even if `plan.md` exists and is non-empty, instructing in-place amendments
- [x] T007 [US1] Update Stage 4 (Tasks) execution condition and task preservation logic in `.agents/skills/speckit-orchestrate/SKILL.md` to force execution when `is_update_mode == true`, enforcing constraint VR-04 ("Strict Monotonicity: Any - [x] remains - [x]; never reset to - [ ]") and appending new update phases or adjusting pending `- [ ]` tasks
- [x] T008 [US1] Update Stage 1 (Specify) condition and directive in `.agents/skills/speckit-orchestrate/SKILL.md` to support in-place `spec.md` amendments when `is_update_mode == true` without wiping existing user stories or acceptance criteria per FR-005

**Checkpoint**: User Story 1 functional — non-destructive replanning stages amend design artifacts and preserve completed tasks

---

## Phase 4: User Story 2 - Fail-Closed Guard on Missing Prerequisites (Priority: P1)

**Goal**: Enforce immediate fail-closed termination with `CRITICAL` diagnostics if an update description is empty or if baseline architectural artifacts (`spec.md`, `plan.md`) are missing.

**Independent Test**: Invoke `--update=""` and verify immediate halt with `CRITICAL` diagnostic without modifying files; invoke `--update="test"` on a feature lacking `plan.md` and verify immediate halt with `CRITICAL` diagnostic per `specs/011-orchestrate-update-flag/quickstart.md` Scenarios 3 and 4.

### Implementation for User Story 2

- [x] T009 [US2] Implement VR-01 description guard in `.agents/skills/speckit-orchestrate/SKILL.md` Section 2, enforcing "If is_update_mode == true and trim(update_description) == "": Result: Transition to FAILED_CLOSED immediately with CRITICAL diagnostic: 'CRITICAL: --update / --amend requires a non-empty description of architectural changes.'"
- [x] T010 [US2] Implement VR-02 feature directory guard in `.agents/skills/speckit-orchestrate/SKILL.md` Section 2, enforcing "If is_update_mode == true and feature_dir cannot be resolved: Result: Transition to FAILED_CLOSED immediately with CRITICAL diagnostic: 'CRITICAL: Cannot execute --update without an active feature directory.'"
- [x] T011 [US2] Implement VR-03 architectural baseline guard in `.agents/skills/speckit-orchestrate/SKILL.md` Section 2, enforcing "If is_update_mode == true and (spec_path does not exist OR plan_path does not exist): Result: Transition to FAILED_CLOSED immediately with CRITICAL diagnostic: 'CRITICAL: Cannot execute --update because required baseline artifacts are missing in {FEATURE_DIR}. Missing artifact(s): {MISSING_ARTIFACTS_LIST}. Expected both spec.md and plan.md.'"

**Checkpoint**: User Stories 1 AND 2 functional — replanning aborts safely before any file mutation if prerequisites are unmet

---

## Phase 5: User Story 3 - Flexible CLI Flag Parsing and Description Extraction (Priority: P2)

**Goal**: Support flexible CLI argument syntax for `--update` and `--amend` (`--update='...'`, `--update="..."`, `--update <desc>`, `--amend='...'`, `--amend="..."`, `--amend <desc>`), normalizing to `UPDATE_DESCRIPTION` and setting `IS_UPDATE_MODE=true`.

**Independent Test**: Parse all flag variations and verify that `UPDATE_DESCRIPTION` captures the sanitized text with bounding quotes stripped and whitespace trimmed per `contracts/orchestrate-update-interface.md` Section 1.3.

### Implementation for User Story 3

- [x] T012 [US3] Implement regex and token-based flag parser in Section 1 of `.agents/skills/speckit-orchestrate/SKILL.md` matching `--update=['"](?P<desc>[^'"]+)['"]`, `--update=(?P<desc>[^\s]+)`, `--update\s+(?P<desc>[^-\s][^-\n]*)` and identical `--amend` patterns
- [x] T013 [US3] Implement quote stripping and whitespace trimming normalization in Section 1 of `.agents/skills/speckit-orchestrate/SKILL.md`, setting constraint "Required if is_update_mode == true; trimmed; length > 0; bounding quotes stripped" for `UPDATE_DESCRIPTION` and setting `IS_UPDATE_MODE=true`
- [x] T014 [US3] Implement flag precedence and interaction handling in Section 1 of `.agents/skills/speckit-orchestrate/SKILL.md` so that `--from` selects the starting stage while preserving `--update` non-destructive semantics

**Checkpoint**: User Stories 1, 2, and 3 functional — flexible CLI argument syntax correctly populates the replanning context

---

## Phase 6: User Story 4 - Multi-Stage Subagent Payload Propagation and Checkpoint Policy (Priority: P2)

**Goal**: Propagate update description and replanning directives in subagent prompt payloads across Stages 1 through 5, and enforce Pre-Implementation Checkpoint pause after Stage 5 (`analyze`) unless `--continue` is specified.

**Independent Test**: Verify that dispatched subagent prompts contain `UPDATE_ACTIVE: true`, `UPDATE_DESCRIPTION`, and `REPLANNING_SCOPE`, and verify that execution pauses cleanly at `PAUSED_AT_CHECKPOINT` after Stage 5 when `--continue` is omitted per `specs/011-orchestrate-update-flag/quickstart.md` Scenarios 5 and 6.

### Implementation for User Story 4

- [x] T015 [US4] Update Section 5 (Mandatory Subagent Prompt Payload) in `.agents/skills/speckit-orchestrate/SKILL.md` to inject `Update Context (Replanning Mode)` block containing `UPDATE_ACTIVE`, `UPDATE_DESCRIPTION`, and stage-specific `REPLANNING_SCOPE` directives matching `contracts/orchestrate-update-interface.md` Section 3
- [x] T016 [US4] Update Stage 5 (Analyze Gate) in `.agents/skills/speckit-orchestrate/SKILL.md` to enforce cross-artifact consistency analysis across amended `spec.md`, `plan.md`, and `tasks.md` with self-healing remediation
- [x] T017 [US4] Enforce Pre-Implementation Checkpoint policy in Stage 5 of `.agents/skills/speckit-orchestrate/SKILL.md`, ensuring constraint "PAUSE_AT_CHECKPOINT (default) or CONTINUOUS (if --continue / --continuous)" pauses cleanly at `PAUSED_AT_CHECKPOINT` when `--continue` is not provided
- [x] T018 [US4] Update Pipeline Execution Summary formatting in Section 7 of `.agents/skills/speckit-orchestrate/SKILL.md` to render replanning metadata (`Update Description`, stage amendment statuses, and resume instructions) per `contracts/orchestrate-update-interface.md` Section 4

**Checkpoint**: User Stories 1 through 4 functional — subagent prompt payloads guide non-destructive updates and checkpoint pause halts before code changes

---

## Phase 7: User Story 5 - Dual-Client Skill Parity (.agents and .claude) (Priority: P3)

**Goal**: Mirror all orchestrator skill updates from `.agents/skills/speckit-orchestrate/SKILL.md` to `.claude/skills/speckit-orchestrate/SKILL.md` and verify 100% byte parity.

**Independent Test**: Run `diff -u` and `cmp -s` between `.agents/skills/speckit-orchestrate/SKILL.md` and `.claude/skills/speckit-orchestrate/SKILL.md` and confirm 0 byte differences per `specs/011-orchestrate-update-flag/quickstart.md` Scenario 1.

### Implementation for User Story 5

- [x] T019 [US5] Mirror `.agents/skills/speckit-orchestrate/SKILL.md` to `.claude/skills/speckit-orchestrate/SKILL.md` to propagate all replanning features to Claude Code runtime
- [x] T020 [US5] Execute cross-client byte parity verification between `.agents/skills/speckit-orchestrate/SKILL.md` and `.claude/skills/speckit-orchestrate/SKILL.md` using `diff -u` and `cmp -s`

**Checkpoint**: All user stories functional and dual-client parity fully verified

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Documentation synchronization under Principle VII, immutability verification of core planning skills, and end-to-end scenario validation walkthrough.

- [x] T021 Update `README.md` under `## Spec Kit Skills & Subagent Orchestration Reference -> ### Custom Skills` to document `/speckit-orchestrate --update='<description>'` and alias `--amend` per Constitution Principle VII and `specs/011-orchestrate-update-flag/quickstart.md` Scenario 2
- [x] T022 [P] Verify core planning skill immutability by checking SHA-256 hashes of `.agents/skills/speckit-plan/SKILL.md` and `.claude/skills/speckit-plan/SKILL.md` against baseline to enforce constraint VR-05
- [x] T023 [P] Verify markdown formatting, link integrity, and shell syntax (`bash -n` where applicable) across modified files (`README.md`, `.agents/skills/speckit-orchestrate/SKILL.md`, `.claude/skills/speckit-orchestrate/SKILL.md`)
- [x] T024 Execute quickstart.md validation scenario walkthrough (Scenarios 1 through 6) verifying fail-closed boundaries, quote stripping, task preservation, and checkpoint policy

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — establishes baseline file hashes and git state.
- **Foundational (Phase 2)**: Depends on Setup completion — BLOCKS all user story implementations. Defines shared variables (`IS_UPDATE_MODE`, `UPDATE_DESCRIPTION`) and task preservation invariants.
- **User Story 1 (Phase 3)**: Depends on Foundational (Phase 2) completion. Establishes core replanning stage execution logic in `speckit-orchestrate`.
- **User Story 2 (Phase 4)**: Depends on Foundational (Phase 2) and US1 completion. Establishes fail-closed precondition guards on missing artifacts.
- **User Story 3 (Phase 5)**: Depends on Foundational (Phase 2) and US2 completion. Implements flexible CLI flag extraction and quote normalization.
- **User Story 4 (Phase 6)**: Depends on US1, US2, and US3 completion. Implements subagent prompt payload augmentation and checkpoint pause enforcement.
- **User Story 5 (Phase 7)**: Depends on US1 through US4 completion. Mirrors changes from `.agents/` to `.claude/` and validates 100% byte parity.
- **Polish (Phase 8)**: Depends on US1 through US5 completion. Updates human-facing documentation (`README.md`), verifies immutability of `speckit-plan`, and executes quickstart validation scenarios.

### User Story Dependencies

- **User Story 1 (P1)**: Foundational logic for in-place amendment of `plan.md` and `tasks.md`. Independent of later stories.
- **User Story 2 (P1)**: Extends Section 2 boundary validation to protect the replanning flow.
- **User Story 3 (P2)**: Extends Section 1 argument parser to feed sanitized parameters into US1 and US2.
- **User Story 4 (P2)**: Extends Section 5 dispatch payload and Stage 5 checkpoint policy.
- **User Story 5 (P3)**: Mirrors the complete, validated `.agents/` implementation to `.claude/`.

### Within Each User Story

- Foundational context before stage logic
- Boundary validation before execution
- Core implementation before dual-client mirroring
- Verification before moving to next priority

### Parallel Opportunities

- Phase 1: T002 and T003 can execute in parallel.
- Phase 8: T022 and T023 can execute in parallel.
- Stories US1 through US4 edit sequential sections of `.agents/skills/speckit-orchestrate/SKILL.md` and are serialized to prevent merge conflicts.
- Dual-client mirroring (US5) occurs after `.agents/` edits stabilize.

---

## Parallel Example: Setup & Verification Tasks

```bash
# Parallel execution for baseline verification tasks:
Task: T002 [P] Record baseline SHA-256 hash of core planning skills in .agents/skills/speckit-plan/SKILL.md and .claude/skills/speckit-plan/SKILL.md
Task: T003 [P] Inspect README.md section "## Spec Kit Skills & Subagent Orchestration Reference -> ### Custom Skills"

# Parallel execution for final polish verification:
Task: T022 [P] Verify core planning skill immutability by checking SHA-256 hashes of speckit-plan
Task: T023 [P] Verify markdown formatting, link integrity, and shell syntax
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup baseline checks.
2. Complete Phase 2: Foundational state variables and preservation rules.
3. Complete Phase 3: User Story 1 (replanning conditions in Stage 3 and Stage 4).
4. **STOP and VALIDATE**: Verify simulated replanning preserves completed tasks while amending plans.

### Incremental Delivery

1. Setup + Foundational → Replanning infrastructure declared.
2. User Story 1 → Core replanning works in-place (MVP!).
3. User Story 2 → Fail-closed guards prevent invalid execution on missing baselines.
4. User Story 3 → Flexible quote and space syntax parsed reliably.
5. User Story 4 → Subagents receive enriched directives; pre-implementation checkpoint pauses safely.
6. User Story 5 → Dual-client parity across Google Antigravity and Claude Code.
7. Polish → `README.md` updated per Principle VII; quickstart validation walkthrough complete.

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task directly to user stories US1–US5 for end-to-end traceability
- In accordance with Constitution Principle III, zero automated test suites or test files are generated
- Completed `- [x]` items in `tasks.md` are strictly monotonic and MUST NEVER be deleted or reset during replanning
- Core planning skills (`speckit-plan/SKILL.md`) remain 100% immutable throughout implementation
