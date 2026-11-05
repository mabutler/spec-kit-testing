---
description: "Task list for Subagent-Driven Spec Kit Orchestrator implementation"
---

# Tasks: Subagent-Driven Spec Kit Orchestrator

**Input**: Design documents from `/specs/003-subagent-orchestrator/` (`spec.md`, `plan.md`, `research.md`, `data-model.md`, `quickstart.md`, `contracts/`)

**Prerequisites**: `plan.md` (required), `spec.md` (required for user stories), `research.md`, `data-model.md`, `contracts/`

**Tests**: None. Per `.specify/memory/constitution.md` Principle III and `.specify/memory/coding-standards.md`, automated test generation is disabled repository-wide. Quality verification is conducted exclusively via static syntax verification, YAML/JSON schema inspection, and declarative acceptance gates (`quickstart.md`).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., `[US1]`, `[US2]`, `[US3]`)
- Include exact file paths in descriptions

## Path Conventions

- **Agent Profiles**: `.agents/agents/speckit-*.md`
- **Workflow Skills**: `.agents/skills/speckit-*/SKILL.md`
- **Hook Registry**: `.specify/extensions.yml`
- **Feature Artifacts**: `specs/003-subagent-orchestrator/`
- **Governance Suite**: `.specify/memory/{constitution,coding-standards,logging-standards}.md`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization, directory structure, and version control hygiene

- [X] T001 [P] Initialize directory structure for subagent profiles and orchestrator skill at `.agents/agents/` and `.agents/skills/speckit-orchestrate/`
- [X] T002 [P] Configure `.gitignore` to exclude `.agents/agents/*.local.md` developer override files in `.gitignore`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core subagent persona profiles and extension hook registry that MUST be complete before ANY user story workflow can execute

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T003 [P] Create tracked High-Reasoning subagent profile in `.agents/agents/speckit-reasoner.md` quoting all data-model.md constraints: `name: "speckit-reasoner"` (matching filename stem), `description: "Non-empty summary of the subagent's role and assigned pipeline stages"`, `role_tier: "reasoning"`, `default_stages: ["clarify", "plan", "analyze", "converge", "self-heal", "converge-retry"]`, `model_policy.gemini_antigravity: "inherit" (Argon/Pro when session ceiling permits) for reasoning`, `model_policy.claude: "opus" (or "inherit") for reasoning`, `model_policy.respect_session_ceiling: true`, `model_policy.override_ceiling: false`, `tools.enable_write_tools: true`, `tools.enable_subagent_tools: false`, `tools.enable_mcp_tools: false`, and Markdown body system prompt enforcing Constitutional Principles I–VII (specifically Principle III no-test rule), single-writer boundary rules, hook anti-recursion rules, and structured completion report schema
- [X] T004 [P] Create tracked Standard/Fast Execution subagent profile in `.agents/agents/speckit-executor.md` quoting all data-model.md constraints: `name: "speckit-executor"` (matching filename stem), `description: "Non-empty summary of the subagent's role and assigned pipeline stages"`, `role_tier: "execution"`, `default_stages: ["specify", "tasks", "implement"]`, `model_policy.gemini_antigravity: "flash"`, `model_policy.claude: "sonnet"`, `model_policy.respect_session_ceiling: true`, `model_policy.override_ceiling: false`, `tools.enable_write_tools: true`, `tools.enable_subagent_tools: false`, `tools.enable_mcp_tools: false`, and Markdown body system prompt enforcing Constitutional Principles I–VII (specifically Principle III no-test rule), single-writer boundary rules, hook anti-recursion rules, and structured completion report schema
- [X] T005 [P] Create extension hook registry in `.specify/extensions.yml` with `schema_version: "1.0"` registering `hooks.after_specify` with `extension: "speckit-orchestrator"`, `command: "speckit.orchestrate"`, `description: "Coordinate context-isolated subagents across clarify, plan, tasks, analyze, implement, and converge"`, `prompt: "Specification complete and validated. Run /speckit-orchestrate to run through design and tasks (pauses before implementation for review), or /speckit-orchestrate --continue to run continuously through the end."`, `enabled: true`, and `optional: true`

**Checkpoint**: Foundation ready - subagent profiles and extension hooks configured. User story implementation can now begin.

---

## Phase 3: User Story 1 - End-to-End Subagent Pipeline Orchestration with Clean Context Isolation (Priority: P1) 🎯 MVP

**Goal**: Deliver the core `/speckit-orchestrate` coordinator skill that drives the 7-stage Spec Kit lifecycle (`specify` → `clarify` → `plan` → `tasks` → `analyze` → `implement` → `converge`) using isolated subagent contexts and shared on-disk state.

**Independent Test**: Can be tested by invoking `/speckit-orchestrate` on an existing feature directory; verify the orchestrator resolves `.specify/feature.json`, verifies prerequisite state, executes stages sequentially via isolated subagents, iterates `implement` ↔ `converge` up to 3 passes when tasks are appended, and outputs the `Pipeline Execution Summary` table with overall status `CONVERGED`.

### Implementation for User Story 1

- [X] T006 [US1] Initialize orchestrator skill structure, YAML frontmatter (`name: "speckit-orchestrate"`, `description: "Coordinate context-isolated subagents across clarify, plan, tasks, analyze, implement, and converge"`), argument parsing for `$ARGUMENTS`, and pre-execution checks in `.agents/skills/speckit-orchestrate/SKILL.md`
- [X] T007 [US1] Implement feature directory and authoritative state resolution in `.agents/skills/speckit-orchestrate/SKILL.md` resolving `feature_directory` from `SPECIFY_FEATURE_DIRECTORY` or `.specify/feature.json`, failing closed (`FAILED_CLOSED`) with `CRITICAL` diagnostic if both `spec.md` and feature description are absent, and passing `SPECIFY_FEATURE_NO_PERSIST=1` for child stages
- [X] T008 [US1] Implement subagent registration (`define_subagent`) and stage dispatch payload builder in `.agents/skills/speckit-orchestrate/SKILL.md` loading personas from `.agents/agents/speckit-reasoner.md` and `.agents/agents/speckit-executor.md`, constructing mandatory prompt directives (target skill path, `SPECIFY_FEATURE_DIRECTORY`, governance suite adherence, and structured completion report schema)
- [X] T009 [US1] Implement sequential stage execution state machine for `specify`, `plan`, and `tasks` stages in `.agents/skills/speckit-orchestrate/SKILL.md` checking artifact existence, skipping already complete stages, and running isolated subagents for pending stages under single-writer serialization
- [X] T010 [US1] Implement `implement` and `converge` execution loop with bounded 3-pass convergence retry in `.agents/skills/speckit-orchestrate/SKILL.md` dispatching `speckit-implement`, followed by `speckit-converge`, re-running `implement` on `tasks_appended` (escalating to `speckit-reasoner`) up to 3 passes, or marking complete on `converged`
- [X] T011 [US1] Implement Pipeline Execution Summary table generation in `.agents/skills/speckit-orchestrate/SKILL.md` formatting stage status (`SKIPPED_EXISTING`, `PASSED`, `SELF_HEALED`, `PAUSED`, `FAILED`, `PENDING`), agent profile, resolved model tier, iteration counts, artifacts verified, and actionable next step

**Checkpoint**: At this point, User Story 1 is fully functional and delivers an end-to-end working MVP pipeline.

---

## Phase 4: User Story 2 - Intelligent Quality Gates, Self-Healing Analysis, and Human-in-the-Loop Checkpoints (Priority: P2)

**Goal**: Enforce deterministic quality gates between subagent transitions (`Clarify Gate` and `Analyze & Self-Heal Gate`) and support human approval flags (default pre-implementation pause, `--continue`, `--pause-before-implement`, `--until=<stage>`, `--from=<stage>`, `--resume`, `--clarify`).

**Independent Test**: Invoke `/speckit-orchestrate` to verify clean pause before implementation by default; invoke `/speckit-orchestrate --continue` for continuous execution; verify Clarify Gate halts on `[NEEDS CLARIFICATION]` markers; verify Analyze Gate automatically self-heals `MEDIUM`/`LOW` findings within ≤ 2 iterations and fails closed on `CRITICAL`/`HIGH` issues.

### Implementation for User Story 2

- [X] T012 [US2] Implement Clarify Gate inspection and human-in-the-loop pause logic in `.agents/skills/speckit-orchestrate/SKILL.md` scanning `spec.md` for `[NEEDS CLARIFICATION]` markers, verifying `checklists/requirements.md` zero failures, evaluating `--clarify`, and pausing (`PAUSED_FOR_USER`) before `plan` when ambiguities exist
- [X] T013 [US2] Implement Analyze & Self-Heal Gate with bounded 2-pass remediation in `.agents/skills/speckit-orchestrate/SKILL.md` dispatching `speckit-analyze` via `speckit-reasoner`, failing closed (`FAILED_CLOSED`) immediately on `CRITICAL` or `HIGH` findings, and dispatching remediation subagent on `MEDIUM` or `LOW` drift up to max 2 iterations
- [X] T014 [US2] Implement execution-scope checkpoint flags (default pre-implementation pause, `--continue`, `--pause-before-implement`, `--until=<stage>`, `--from=<stage>`, `--resume`) in `.agents/skills/speckit-orchestrate/SKILL.md` allowing users to stop cleanly after `plan`, `tasks`, or `analyze`, or force regeneration from a specific stage

**Checkpoint**: At this point, User Stories 1 AND 2 are functional, ensuring rigorous quality gates and human approval checkpoints.

---

## Phase 5: User Story 3 - Role-Based Agent Definitions, Local Overrides, `after_specify` Hook & Safe Parallelism (Priority: P3)

**Goal**: Complete the 5-level agent profile override hierarchy (`speckit-<stage>.local.md` → `speckit-<stage>.md` → `speckit-<role>.local.md` → `speckit-<role>.md`), implement the Session Model Ceiling algorithm, wire extension hook handling with anti-recursion guards, and enforce safe concurrency for `[P]` tasks during implementation.

**Independent Test**: Verify `.agents/agents/*.local.md` is ignored by git; create a temporary local override and verify priority resolution; verify `hooks.after_specify` in `.specify/extensions.yml` is parsed by `speckit-specify` without recursive loop; verify `[P]` task execution validates mutually disjoint file paths.

### Implementation for User Story 3

- [X] T015 [US3] Implement 5-level agent profile override resolution hierarchy in `.agents/skills/speckit-orchestrate/SKILL.md` checking `$ARGUMENTS` flag override → `speckit-<stage>.local.md` → `speckit-<stage>.md` → `speckit-<role>.local.md` → default `speckit-<role>.md`
- [X] T016 [US3] Implement Provider-Adaptive Model Policy and Session Model Ceiling logic in `.agents/skills/speckit-orchestrate/SKILL.md` detecting active session model tier (`high_reasoning` vs. `standard_execution`), capping subagents at session model ceiling unless `override_ceiling: true` or `--override-ceiling` is passed, and stepping down `speckit-executor` to `flash` / `sonnet` when session is on `pro` / `opus`
- [X] T017 [US3] Implement extension hook integration and anti-recursion guard in `.agents/skills/speckit-orchestrate/SKILL.md` reading `.specify/extensions.yml`, passing `ORCHESTRATOR_CHILD=true` to Stage 1 `specify` subagent to suppress re-triggering `hooks.after_specify`, and handling pre/post execution hooks
- [X] T018 [US3] Implement safe parallelism and disjoint file target validation for `[P]` tasks in `.agents/skills/speckit-orchestrate/SKILL.md` verifying disjoint file targets within the same phase before concurrent dispatch, while serializing all `tasks.md` checkbox updates through a single coordinator

**Checkpoint**: All three user stories are fully implemented, providing complete end-to-end orchestration, local overrides, and extension hook wiring.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Static verification, schema validation, and constitutional compliance checks across all deliverables

- [X] T019 [P] Validate YAML frontmatter, schema constraints, and markdown formatting across `.agents/agents/speckit-reasoner.md` and `.agents/agents/speckit-executor.md` per quickstart.md Section 1.3
- [X] T020 [P] Validate `.specify/extensions.yml` YAML schema with python3 yaml parser per quickstart.md Section 1.2
- [X] T021 [P] Validate `.gitignore` coverage for `.agents/agents/*.local.md` via `git check-ignore` per quickstart.md Section 1.4
- [X] T022 Run Constitutional Pre-PR verification script `.specify/scripts/bash/resolve-template.sh constitution-template --json` and confirm zero automated test files exist per quickstart.md Section 1.5

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories proceed sequentially in priority order (P1 → P2 → P3) or in parallel once foundation is in place
- **Polish (Final Phase)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories (Delivers core MVP)
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Enhances US1 with gates and pause checkpoints
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Enhances US1/US2 with 5-level overrides, ceiling logic, and hook integration

### Within Each User Story

- Prerequisites and input parsing before state machine
- State machine before gate checks
- Gate checks before execution loops
- Execution loops before summary reporting
- Story complete and verified before moving to next priority

### Parallel Opportunities

- Setup tasks `T001` and `T002` can run in parallel
- Foundational tasks `T003`, `T004`, and `T005` can run in parallel
- Polish tasks `T019`, `T020`, and `T021` can run in parallel

---

## Parallel Example: Foundational Phase

```bash
# Launch all subagent profiles and hook registry together:
Task: "Create tracked High-Reasoning subagent profile in .agents/agents/speckit-reasoner.md"
Task: "Create tracked Standard/Fast Execution subagent profile in .agents/agents/speckit-executor.md"
Task: "Create extension hook registry in .specify/extensions.yml"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (`T001`, `T002`)
2. Complete Phase 2: Foundational (`T003`, `T004`, `T005`)
3. Complete Phase 3: User Story 1 (`T006` through `T011`)
4. **STOP and VALIDATE**: Test User Story 1 independently on an existing feature directory
5. Pipeline is capable of full autopilot delivery (MVP achieved!)

### Incremental Delivery

1. Complete Setup + Foundational → Baseline persona profiles and hook registry ready
2. Add User Story 1 → Basic end-to-end orchestration functional (MVP!)
3. Add User Story 2 → Deterministic Clarify Gate, Analyze Gate self-healing, and `--pause-before-implement` checkpoints active
4. Add User Story 3 → 5-level agent override hierarchy, Session Model Ceiling enforcement, and `after_specify` extension hook wiring active
5. Complete Polish → Run static verification suite and Constitutional Pre-PR check

### Parallel Team Strategy

With multiple developers:
1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 core coordinator
   - Developer B: User Story 2 quality gates and checkpoint flags
   - Developer C: User Story 3 agent override resolver, ceiling policy, and extension hook wiring
3. Stories integrate cleanly into `.agents/skills/speckit-orchestrate/SKILL.md`

---

## Notes

- `[P]` tasks = different files, no dependencies
- `[Story]` label maps task to specific user story for traceability
- Each user story is independently completable and testable
- Constitutional Principle III strictly obeyed: ZERO automated test files, test directories, or test tasks generated
- Stop at any checkpoint to validate story independently
