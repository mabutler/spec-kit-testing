# Phase 0 Research: Subagent-Driven Spec Kit Orchestrator

**Feature**: `003-subagent-orchestrator`  
**Date**: 2026-11-05  
**Spec**: [spec.md](./spec.md)

## Overview

This research document consolidates the architectural and technical design decisions required to implement Phase 3 of `ROADMAP.md` (`Subagent-Driven Spec Kit Orchestrator`) in full compliance with `.specify/memory/constitution.md` (v2.0.0), `.specify/memory/coding-standards.md`, and `.specify/memory/logging-standards.md`. All specification clarifications were resolved during the 2026-11-05 clarification session; zero `NEEDS CLARIFICATION` items remain.

---

## Decision 1: Dual Entry-Point Architecture (`speckit-orchestrate` Skill + `hooks.after_specify`)

- **Decision**: Deliver both:
  1. A first-class orchestrator skill at `.agents/skills/speckit-orchestrate/SKILL.md` (invokable directly as `/speckit-orchestrate [args]`).
  2. A repository root `.specify/extensions.yml` registering `speckit.orchestrate` (`/speckit-orchestrate`) under `hooks.after_specify` with `optional: true` by default (and documented support for `optional: false`).
  3. An explicit **Anti-Recursion Guard**: when `speckit-orchestrate` invokes `speckit-specify` as Stage 1 (because no `spec.md` exists yet and a feature description was passed to `/speckit-orchestrate`), the Specify subagent prompt includes `[ORCHESTRATOR_CHILD=true]` / an explicit directive instructing the subagent to skip `hooks.after_specify` execution so it never re-invokes `speckit-orchestrate`.
- **Rationale**: `ROADMAP.md` (Phase 3) specifies that orchestration can be triggered via a dedicated orchestrator skill (`speckit-orchestrate`) and/or an extension hook in `.specify/extensions.yml` (`hooks.after_specify`). Inspecting `.agents/skills/speckit-specify/SKILL.md` (lines 235–269) confirms that `speckit-specify` natively checks `.specify/extensions.yml` under `hooks.after_specify`, converts `speckit.orchestrate` → `/speckit-orchestrate`, and either prompts the user (`optional: true`) or emits `EXECUTE_COMMAND: speckit-orchestrate` (`optional: false`). Setting `optional: true` as the default satisfies Principle VI (*Verify Before Mutate/Destroy*) during standalone `/speckit-specify` runs while offering a one-command handoff.
- **Alternatives Considered**:
  - *Hook-only (`optional: false` without a standalone skill)*: Rejected because users cannot resume a partially completed feature or invoke orchestration with flags (`--pause-before-implement`, `--until=analyze`, `--from=plan`) without re-running `speckit-specify`.
  - *Modifying existing `speckit-specify/SKILL.md` to hardcode orchestration*: Rejected because it violates modular skill boundaries and Spec Kit's native `.specify/extensions.yml` hook mechanism.

---

## Decision 2: Role-Based Subagent Definitions in `.agents/agents/` & Override Resolution Hierarchy

- **Decision**: Ship two canonical, tracked role-based agent definitions in `.agents/agents/`:
  - `.agents/agents/speckit-reasoner.md`: Assigned to High-Reasoning stages (`clarify`, `plan`, `analyze`, `converge`) and all retry/escalation passes (Analyze self-heal passes and Converge follow-up passes).
  - `.agents/agents/speckit-executor.md`: Assigned to Standard/Fast Execution stages (`specify`, `tasks`, and initial `implement` passes).
  - Configure `.gitignore` to ignore `.agents/agents/*.local.md`.
  - Resolve agent definitions per stage using a strict 5-level priority order:
    1. Explicit runtime override in `$ARGUMENTS` (e.g., `--model=<tier>` or `--agent=<name>`)
    2. `.agents/agents/speckit-<stage>.local.md` (gitignored machine-local stage override)
    3. `.agents/agents/speckit-<stage>.md` (optional tracked stage override)
    4. `.agents/agents/speckit-<role>.local.md` (gitignored machine-local role override)
    5. `.agents/agents/speckit-<role>.md` (canonical tracked role default: `speckit-reasoner.md` or `speckit-executor.md`).
- **Rationale**: Separating *how a stage is executed* (`.agents/skills/speckit-<stage>/SKILL.md`) from *who/what model executes it* (`.agents/agents/speckit-<role>.md`) keeps Spec Kit skills clean while allowing developers to customize model tiers or system prompts locally via gitignored `.local.md` files or per-stage `.md` files without touching skill definitions.
- **Alternatives Considered**:
  - *Seven separate tracked files in `.agents/agents/` (`speckit-specify.md` through `speckit-converge.md`)*: Rejected during spec clarification because maintaining 7 near-identical agent manifests duplicates prompt boilerplate across stages that share identical capability profiles (`reasoner` vs. `executor`).
  - *Hardcoding model tiers inside `speckit-orchestrate/SKILL.md`*: Rejected because local customization would dirty a tracked skill file in git.

---

## Decision 3: Provider-Adaptive Two-Tier Model Policy & Session Model Ceiling

- **Decision**: Encode a declarative model mapping table in `.agents/agents/speckit-reasoner.md` and `.agents/agents/speckit-executor.md` and enforce a **Session Model Ceiling** in `speckit-orchestrate`:
  - **High-Reasoning Role (`speckit-reasoner`)**:
    - Gemini / Antigravity family: `Argon` / `Pro` (`invoke_subagent` `Model: "inherit"` when session is on Argon/Pro, or `"pro"` only when `override_ceiling: true`)
    - Claude family: `Opus` (`model: opus` / `inherit`)
  - **Standard/Fast Execution Role (`speckit-executor`)**:
    - Gemini / Antigravity family: `Flash` (`invoke_subagent` `Model: "flash"`)
    - Claude family: `Sonnet` (`model: sonnet`)
  - **Session Model Ceiling Rule**: At runtime, the orchestrator inspects its own active session model tier:
    - If the active session model is a High-Reasoning tier (`Argon`, `Pro`, `Opus`), `speckit-reasoner` uses `inherit` (staying on the user's selected high-reasoning model) and `speckit-executor` steps down to the paired fast execution tier (`flash` / `sonnet`).
    - If the active session model is already a Standard/Fast tier (`Flash`, `Flash Lite`, `Sonnet`, `Haiku`), **both** `speckit-reasoner` and `speckit-executor` are capped at `inherit` (the session model) unless a local override explicitly sets `override_ceiling: true` or the user passes `--override-ceiling` / `--model=pro` in `$ARGUMENTS`.
- **Rationale**: In Antigravity (`invoke_subagent`), the `Model` parameter accepts `inherit`, `flash_lite`, `flash`, or `pro`, and custom subagent types can be registered via `define_subagent` (`Name`, `Description`, `SystemPrompt`, `EnableWriteTools`, `EnableSubagentTools`, `EnableMCPTools`) and launched via `invoke_subagent`. Stepping down from Argon/Pro to Flash for mechanical execution (`specify`, `tasks`, initial `implement`) cuts latency and token cost while preserving Argon/Pro for high-reasoning synthesis and gate verification (`clarify`, `plan`, `analyze`, `converge`, and retries). Capping at the user's active session model prevents unexpected quota/cost escalation when a user intentionally selects a lighter session model.
- **Alternatives Considered**:
  - *Using `inherit` for every stage*: Rejected because running `tasks` formatting and straightforward `implement` passes on heavyweight reasoning models wastes time and compute when a fast execution tier is available beneath the ceiling.
  - *Unconditionally forcing `pro` even when the user selected `flash`*: Violates user model selection intent and quota expectations.

---

## Decision 4: Deterministic Quality Gates & Bounded Self-Healing / Convergence Loops

- **Decision**: Implement three explicit, fail-closed gates between subagent stages in `speckit-orchestrate`:
  1. **Clarify Gate (Pre-Plan)**:
     - Runs after `spec.md` is verified. Checks `SPECIFY_FEATURE_DIRECTORY/spec.md` for `[NEEDS CLARIFICATION` markers and `SPECIFY_FEATURE_DIRECTORY/checklists/requirements.md` for unchecked `- [ ]` items.
     - If `--clarify` was passed in `$ARGUMENTS`, or if any `[NEEDS CLARIFICATION]` marker or unchecked requirement checklist item exists, dispatches `speckit-clarify` (using `speckit-reasoner`), surfaces the prioritized clarification questions to the user, and **HALTS (`PAUSED_FOR_USER`)** before `speckit-plan`.
     - If 0 markers and 0 failing checklist items exist (and `--clarify` was not forced), marks `Clarify Gate = PASSED` and proceeds directly to `speckit-plan`.
  2. **Analyze & Self-Heal Gate (Post-Tasks, Pre-Implement)**:
     - Spawns `speckit-analyze` in a `speckit-reasoner` subagent (read-only).
     - **Pass**: 0 findings → `PASSED`.
     - **Fail Closed**: Any `CRITICAL` or `HIGH` finding (including any violation of `constitution.md`, `coding-standards.md`, or `logging-standards.md`, or an unmapped P1 requirement requiring human scope judgment) → immediately **HALT (`FAILED_CLOSED`)** and report the table to the user.
     - **Bounded Self-Heal**: Only `MEDIUM` or `LOW` findings (e.g., missing task requirement traceability tags, minor terminology drift between `plan.md` and `tasks.md`) → spawn a `speckit-reasoner` remediation subagent to update `plan.md`/`tasks.md` (never mutating `spec.md` functional scope or `.specify/memory/`) and re-run `speckit-analyze`, up to **maximum 2 self-heal iterations**. If any finding remains after iteration 2, fail closed and halt.
  3. **Convergence Gate (Post-Implement)**:
     - Spawns `speckit-converge` in a `speckit-reasoner` subagent after `speckit-implement` finishes.
     - If `converged` → pipeline succeeds (`CONVERGED`).
     - If `tasks_appended` → loops back to `speckit-implement` (escalated to `speckit-reasoner` for retry precision) followed by `speckit-converge`, up to **maximum 3 convergence cycles**. If `tasks_appended` still occurs on pass 3, halts (`FAILED_CLOSED`) and presents remaining tasks to the user.
- **Rationale**: Directly enforces Constitutional Principle I (*Evidence Over Invention*), Principle II (*Two-Tier Failure Model & Fail Closed on Required State*), and Principle VI (*Bounded Resources*).
- **Alternatives Considered**:
  - *Allowing self-heal to modify `spec.md` or resolve `HIGH`/`CRITICAL` issues autonomously*: Rejected because altering requirements or overriding constitutional checks without human approval violates Principle I and Principle II.

---

## Decision 5: Single-Writer State Sharing & Safe Parallelism Rules

- **Decision**:
  - All pipeline stages share state **exclusively** through `.specify/feature.json` (`feature_directory`) and on-disk files in `SPECIFY_FEATURE_DIRECTORY` (`spec.md`, `checklists/requirements.md`, `plan.md`, `research.md`, `data-model.md`, `quickstart.md`, `contracts/`, `tasks.md`).
  - Subagents receive `SPECIFY_FEATURE_NO_PERSIST=1` (except during Stage 1 `speckit-specify` when creating a new feature) so downstream subagents never unexpectedly overwrite `.specify/feature.json` (leveraging `common.sh` line 176 support for `SPECIFY_FEATURE_NO_PERSIST=1`).
  - Stages that write shared artifacts (`specify`, `clarify`, `plan`, `tasks`, `analyze` remediation, `converge`) run **strictly sequentially** (single writer at a time).
  - Parallel subagent execution (`[P]`) is permitted **only** inside `speckit-implement` when tasks in the same phase are marked `[P]`, declare explicit target file paths, and those file paths are verified to be mutually disjoint. Even during parallel task execution, checkbox updates (`- [x]`) to `tasks.md` are serialized through the coordinating implementation agent after worker subagents complete.
- **Rationale**: Enforces Constitutional Principle IV (*Single Authoritative State, Enforced Boundaries & Safe Concurrency*). Inspecting `.specify/scripts/bash/common.sh` revealed built-in support for `SPECIFY_FEATURE_NO_PERSIST=1`, which prevents subagent script calls from racing on `.specify/feature.json`.
- **Alternatives Considered**:
  - *Running `plan` and `clarify` or multiple `tasks.md` writers in parallel*: Rejected due to file overwrite race conditions on Markdown artifacts.

---

## Decision 6: Static Verification & Zero Automated Tests (Constitutional Principle III)

- **Decision**: In compliance with `.specify/memory/constitution.md` Principle III (*Static Verification & No Automated Tests*) and `.specify/memory/coding-standards.md`, this feature generates **zero** automated test files, unit tests, or test harnesses. Verification is performed via:
  1. YAML/JSON parsing verification of `.specify/extensions.yml` and `.specify/feature.json`.
  2. Frontmatter and section structure validation of `.agents/agents/speckit-reasoner.md`, `.agents/agents/speckit-executor.md`, and `.agents/skills/speckit-orchestrate/SKILL.md`.
  3. Placeholder and link integrity scans (`grep` checks for unresolved placeholders, broken links, or prohibited test-generation instructions).
  4. Acceptance gate verification via `.specify/scripts/bash/resolve-template.sh constitution-template --json` and `check-prerequisites.sh`.
- **Rationale**: Mandatory compliance with Constitutional Principle III (ratified v2.0.0).
- **Alternatives Considered**: None (non-negotiable constitutional constraint).
