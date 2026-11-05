# Skill Contract: `/speckit-roadmap`

**Feature**: `005-roadmap-management`  
**Artifact**: `.agents/skills/speckit-roadmap/SKILL.md`  
**Date**: 2026-11-05  

---

## 1. Overview & Capabilities

The `/speckit-roadmap` skill provides 100% agent-native, script-free management of `ROADMAP.md`. It resolves `roadmap-template` via Spec Kit's 4-tier template hierarchy and bridges strategic multi-phase planning with tactical `/speckit-specify` feature specifications.

---

## 2. Command Invocations & Arguments

```text
/speckit-roadmap [<goals-or-instructions>]
/speckit-roadmap --add "<initiative-description>" [--after <phase-id>] [--prerequisites "<phase-list>"]
/speckit-roadmap --update <phase-id> "<changes>"
/speckit-roadmap --defer <phase-id> [--reason "<rationale>"]
/speckit-roadmap --status | --check
/speckit-roadmap --sync
/speckit-roadmap --next [--worktree] [--force]
/speckit-roadmap --specify <phase-id> [--worktree] [--force]
```

| Flag / Mode | Mutates Disk? | Description |
|-------------|---------------|-------------|
| *(default / goals)* | Yes (`ROADMAP.md`) | **Mode 1 (Scaffold / Interactive Authoring)**: Scaffolds a new `ROADMAP.md` from `roadmap-template` or migrates an existing unstructured `ROADMAP.md` to the canonical schema while preserving all existing content. |
| `--add`, `--update`, `--defer` | Yes (`ROADMAP.md`) | **Mode 2 (Phase Mutation)**: Adds a new phase, updates an existing phase's deliverables/prerequisites/decisions, or marks a phase `DEFERRED` across both the Overview table and detailed sections. |
| `--status` / `--check` | **No (Read-Only)** | **Mode 3 (Status & Drift Audit)**: Runs static structural lint (`RM-LINT-001`..`006`) and reconciles every phase against `specs/NNN-*`, git worktrees, and commit history. Emits a structured status and drift report. |
| `--sync` | Yes (`ROADMAP.md`) | **Mode 4 (Status Synchronization)**: Reconciles `Status` and `Spec` fields in `ROADMAP.md` (Overview table + phase `### Metadata`) to match verified repository evidence (`InferredEvidenceStatus`). |
| `--next` / `--specify <phase>` | Yes (`ROADMAP.md` + `specs/NNN-*/`) | **Mode 5 (Specify Handoff)**: Selects the earliest eligible `PLANNED` phase (or `<phase-id>`), verifies prerequisites are `COMPLETED`, marks the phase `IN_PROGRESS` with its `specs/NNN-<short-name>/` link, and invokes `/speckit-specify` (optionally in a new git worktree). |

---

## 3. Deterministic Evidence Inference Rules (`InferredEvidenceStatus`)

During Modes 3, 4, and 5, `/speckit-roadmap` computes `InferredEvidenceStatus` for each phase `Phase N` using the following precedence rules:

1. **Discover Linked Specification Directory (`resolved_spec_dir`)**:
   - Check explicit `Spec` column / `### Metadata` (`specs/NNN-<slug>/`) in current checkout and active worktrees (`git worktree list`).
   - Otherwise, scan `specs/` (in current checkout and active worktrees) for `00N-*` matching `Phase N` and initiative keywords.
   - If multiple `specs/` directories match ambiguously without an explicit link, set `reconciliation_state = AMBIGUOUS_MATCH` and log `WARN`.
2. **Compute `InferredEvidenceStatus`**:
   - **`DEFERRED`**: If `declared_status == DEFERRED` in `ROADMAP.md`, preserve `DEFERRED` (human override).
   - **`COMPLETED`**:
     - `resolved_spec_dir` exists AND contains `spec.md`, `plan.md`, and `tasks.md` where total tasks (`- [x]` + `- [ ]`) > 0 and unchecked tasks (`- [ ]`) == 0; **OR**
     - Git commit log (`git log --oneline`) records the completed implementation commit for `00N-<slug>` / `Phase N`.
   - **`IN_PROGRESS`**:
     - `resolved_spec_dir` exists (in primary checkout or an active git worktree) with `spec.md` present, and `tasks.md` is either absent or contains >= 1 unchecked `- [ ]` task; **OR**
     - An active git branch or worktree matching `00N-*` exists with work in progress.
   - **`PLANNED`**:
     - None of the above conditions hold (no matching `specs/NNN-*` directory, active worktree, or implementation commit).

---

## 4. Boundary Failure & Telemetry Semantics

All telemetry conforms strictly to `.specify/memory/logging-standards.md`:

- **`INFO` (Lifecycle Milestones)**:
  - `"Roadmap template resolved from {TierPath} for {OperationMode}"`
  - `"Roadmap status audit completed across {PhaseCount} phases ({SyncedCount} SYNCED, {DriftCount} STATUS_DRIFT)"`
  - `"Roadmap synchronized: updated {UpdatedPhaseCount} phase(s) in ROADMAP.md"`
  - `"Selected {PhaseId} ({InitiativeTitle}) for /speckit-specify handoff targeting {SpecDir}"`
- **`WARN` (Recoverable Boundary Rejections & Drift Detection)**:
  - Missing or empty `ROADMAP.md` when `--status`, `--check`, `--sync`, or `--next` is called: halt before mutation and offer to scaffold from `roadmap-template`.
  - Unfulfilled prerequisites during `--specify <phase>` or `--next`: halt before creating spec and report blocking prerequisite phase IDs unless `--force` is passed.
  - Structural lint errors (`RM-LINT-001`..`006`) or `STATUS_DRIFT` detected during `--check` / `--status`.
- **`CRITICAL` (Broken Internal Invariants)**:
  - `roadmap-template.md` missing across all 4 template tiers: halt immediately.

---

## 5. Output Report Format (`--status` / `--check` / `--sync`)

```markdown
### Spec Kit Roadmap Status Report

**Roadmap File**: `ROADMAP.md`  
**Mode**: `<Status Audit (Read-Only) | Structural Check (Read-Only) | Status Sync>`  
**Template Tier**: `<Tier 2: .specify/presets/base-governance/templates/roadmap-template.md>`  

#### Phase Reconciliation Summary

| Phase | Initiative | Declared Status | Inferred Evidence | Spec Directory | Prerequisites | Alignment |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Phase 1** | Base Governance Suite & Templates | `COMPLETED` | `COMPLETED` (35/35 tasks) | `specs/001-base-governance-templates/` | None (Ready) | `SYNCED` |
| **Phase 2** | Co-Applied Governance & Constitutional Merge | `COMPLETED` | `COMPLETED` (25/25 tasks) | `specs/002-co-applied-governance-merge/` | Phase 1 (Ready) | `SYNCED` |
| **Phase 3** | Subagent-Driven Spec Kit Orchestrator | `COMPLETED` | `COMPLETED` (24/24 tasks) | `specs/003-subagent-orchestrator/` | Phase 1, Phase 2 (Ready) | `SYNCED` |
| **Phase 4** | Portable Project Bootstrapper | `COMPLETED` | `COMPLETED` (42/42 tasks) | `specs/004-portable-project-bootstrapper/` | Phase 1–3 (Ready) | `SYNCED` |
| **Phase 5** | Roadmap Management (`speckit-roadmap`) | `IN_PROGRESS` | `IN_PROGRESS` (spec + plan) | `specs/005-roadmap-management/` | Phase 1–4 (Ready) | `SYNCED` |
| **Phase 6** | Human-Facing Documentation Standards & Governance | `PLANNED` | `PLANNED` | — | Phase 1, Phase 2, Phase 4 (Ready) | `SYNCED` |

#### Structural Lint & Diagnostics
- **Structural Gates (`RM-LINT-001`..`006`)**: `PASS` (6/6 gates passed)
- **Next Eligible Phase for `/speckit-roadmap --next`**: `Phase 6: Human-Facing Documentation Standards & Governance` (Prerequisites Phase 1, Phase 2, Phase 4 `COMPLETED`)
```
