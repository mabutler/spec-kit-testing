# Data Model: Roadmap Management (`speckit-roadmap`)

**Feature**: `005-roadmap-management`  
**Date**: 2026-11-05  
**Status**: Completed  

---

## Conceptual Architecture

The Roadmap Management feature bridges high-level multi-phase strategic planning (`ROADMAP.md`) and tactical single-feature execution (`specs/NNN-*/`) using Spec Kit's 4-tier template hierarchy and 100% agent-native skills.

```text
+-----------------------------------------------------------------------------------+
|                        4-Tier Template Resolution Hierarchy                       |
|  1. .specify/templates/overrides/roadmap-template.md                              |
|  2. .specify/presets/base-governance/templates/roadmap-template.md (preset.yml)   |
|  3. .specify/extensions/<ext-id>/templates/roadmap-template.md                    |
|  4. .specify/templates/roadmap-template.md (Core Fallback)                        |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                   /speckit-roadmap (.agents/skills/speckit-roadmap)               |
|  - Mode 1: Scaffold / Authoring       - Mode 4: Status Sync (--sync)              |
|  - Mode 2: Phase Mutation (--add/...) - Mode 5: Specify Handoff (--next/--specify)|
|  - Mode 3: Status & Drift Audit (--status / --check)                              |
+-----------------------------------------------------------------------------------+
               |                                                   |
               | (Reads / Reconciles / Updates)                    | (Seeds Context & Worktree)
               v                                                   v
+-----------------------------------------+     +-----------------------------------+
|       Project Roadmap (ROADMAP.md)      |     |         /speckit-specify          |
|  [Protected Project-Owned User State]   |     |  - Optional Git Worktree Creation |
|  - Overview of Initiatives Table        |<--->|    (.worktrees/NNN-<short-name>)  |
|  - Phase 1..N Sections & Metadata       |     |  - Populates specs/NNN-*/spec.md  |
+-----------------------------------------+     +-----------------------------------+
```

---

## Core Entities & Schemas

### 1. Roadmap Document (`RoadmapDocument`)

Models the root `ROADMAP.md` file governed by `roadmap-template.md`.

- **Entity**: `RoadmapDocument`
- **Location**: `${REPO_ROOT}/ROADMAP.md` (Protected User State)
- **Structural Components**:
  - `title` (string, required): Document H1 title (e.g., `# Spec Kit Customizations & Automation Roadmap`).
  - `last_updated` (string, ISO-8601 date `YYYY-MM-DD`, required): Date of last roadmap revision or status sync.
  - `overview_table` (array of `RoadmapOverviewRow`, required): Summary table under `## Overview of Initiatives`.
  - `phases` (array of `RoadmapPhase`, required): Detailed sections under `## Phase N: <Title>`.
- **Validation Invariants**:
  - `overview_table.length == phases.length` and `phases.length >= 1`.
  - Every `Phase N` row in `overview_table` MUST have a corresponding `## Phase N: <Initiative Title>` section in the exact same sequential order.
  - `Status` and `Spec` values in `overview_table` MUST match the `**Status**` and `**Spec Directory**` fields in the corresponding phase's `### Metadata` subsection.

---

### 2. Roadmap Phase (`RoadmapPhase`)

Models an individual strategic initiative phase within `ROADMAP.md`.

- **Entity**: `RoadmapPhase`
- **Fields**:
  - `phase_id` (string, required): Sequential identifier matching `^Phase [1-9][0-9]*$` (e.g., `"Phase 5"`).
  - `phase_number` (integer, required): 1-based integer index (`1`, `2`, `3`, ...).
  - `title` (string, required): Concise initiative name (e.g., `"Roadmap Management (\`speckit-roadmap\`)"`).
  - `declared_status` (enum, required): One of:
    - `PLANNED` — Scheduled for future specification and implementation.
    - `IN_PROGRESS` — Currently undergoing specification, planning, task generation, or implementation.
    - `COMPLETED` — All specification, planning, and implementation tasks verified complete.
    - `DEFERRED` — Explicitly postponed by human decision; skipped by `--next` selection.
  - `prerequisites` (array of `phase_id` strings, required): `["None"]` or list of upstream phase IDs that must be `COMPLETED` before this phase is eligible for `--next` handoff (e.g., `["Phase 1", "Phase 2", "Phase 3", "Phase 4"]`).
  - `spec_directory` (string, nullable): Relative path to the linked feature specification directory (e.g., `"specs/005-roadmap-management/"`) or `"—"` when unassigned.
  - `goal` (string, required): One-sentence strategic objective shown in the Overview of Initiatives table.
  - `key_deliverables_summary` (string, required): Concise deliverable list in the Overview table.
  - `problem_statement` (markdown string, required): Detailed `### Problem Statement` section body.
  - `architectural_fit` (markdown string, required): Detailed `### Architectural Fit in Spec Kit` section body.
  - `key_deliverables` (array of markdown bullets, required): Detailed `### Key Deliverables` section items.
  - `key_design_decisions` (array of markdown bullets, required): Detailed `### Key Design Decisions to Resolve During Spec` section items.
- **Validation Rules**:
  - `phase_id` MUST be unique across `ROADMAP.md`.
  - Every entry in `prerequisites` (when not `"None"`) MUST reference a valid existing `phase_id` with `phase_number < current.phase_number` (no self-references, dangling references, or cyclic dependencies).
  - If `declared_status` is `IN_PROGRESS` or `COMPLETED`, `spec_directory` SHOULD reference a concrete `specs/NNN-*` path.

---

### 3. Phase Status & Drift Record (`PhaseDriftRecord`)

Models the reconciliation result produced during `/speckit-roadmap --status`, `--check`, and `--sync`.

- **Entity**: `PhaseDriftRecord`
- **Fields**:
  - `phase_id` (string): e.g., `"Phase 5"`.
  - `declared_status` (enum): Status written in `ROADMAP.md` (`PLANNED` | `IN_PROGRESS` | `COMPLETED` | `DEFERRED` | `MISSING`).
  - `inferred_evidence_status` (enum): Status computed from repository artifacts (`PLANNED` | `IN_PROGRESS` | `COMPLETED` | `DEFERRED`).
  - `declared_spec_dir` (string): Spec path written in `ROADMAP.md` (or `"—"`).
  - `resolved_spec_dir` (string): Matched `specs/NNN-*` directory discovered on disk or in active git worktrees (or `"—"`).
  - `worktree_path` (string, optional): Path to active git worktree if the phase is executing in an isolated worktree (e.g., `".worktrees/005-roadmap-management"`).
  - `task_completion_ratio` (string): Checked vs. total tasks in `tasks.md` (e.g., `"42/42 (100%)"`, `"0/0 (no tasks.md)"`, or `"—"`).
  - `prerequisites_satisfied` (boolean): `true` if all declared prerequisite phases have `inferred_evidence_status == COMPLETED`.
  - `reconciliation_state` (enum):
    - `SYNCED` — `declared_status == inferred_evidence_status`, `declared_spec_dir == resolved_spec_dir`, and all required phase subsections are valid.
    - `STATUS_DRIFT` — `declared_status != inferred_evidence_status` or `declared_spec_dir != resolved_spec_dir`.
    - `AMBIGUOUS_MATCH` — Multiple candidate `specs/NNN-*` directories match without an explicit spec link.
    - `STRUCTURAL_ERROR` — Missing required section, overview/detail table mismatch, duplicate phase ID, or invalid prerequisite reference.

---

### 4. Phase Lifecycle State Machine

```text
                  +-------------------------------+
                  |            PLANNED            |
                  +-------------------------------+
                     |                         |
   (/speckit-roadmap |                         | (/speckit-roadmap --defer)
    --next / specify)|                         v
                     |            +-------------------------------+
                     |            |           DEFERRED            |
                     |            +-------------------------------+
                     |                         |
                     v                         | (/speckit-roadmap --update
                  +-------------------------------+  status=PLANNED)
                  |          IN_PROGRESS          |<--------+
                  | (spec.md created; tasks open) |
                  +-------------------------------+
                                 |
                                 | (All tasks in tasks.md [x]
                                 |  + /speckit-roadmap --sync)
                                 v
                  +-------------------------------+
                  |           COMPLETED           |
                  +-------------------------------+
```

---

### 5. Worktree Specification Context (`WorktreeSpecContext`)

Models the isolated git worktree state created when `/speckit-specify` or `/speckit-roadmap --next` is invoked with worktree isolation.

- **Entity**: `WorktreeSpecContext`
- **Fields**:
  - `worktree_root` (string): `.worktrees/<NNN>-<short-name>` relative to primary repository root.
  - `branch_name` (string): `<NNN>-<short-name>`.
  - `feature_directory` (string): `specs/<NNN>-<short-name>` inside `worktree_root`.
  - `feature_json_path` (string): `${worktree_root}/.specify/feature.json`.
  - `exclude_entry` (string): `.worktrees/` recorded in primary repository `.git/info/exclude`.
