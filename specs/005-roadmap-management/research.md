# Research: Roadmap Management (`speckit-roadmap`)

**Feature**: `005-roadmap-management`  
**Date**: 2026-11-05  
**Status**: Completed  

---

## Executive Summary

Phase 5 introduces first-class strategic roadmap management (`speckit-roadmap`) into Spec Kit. Prior to Phase 5, Spec Kit began its formal workflow at the tactical single-feature level (`/speckit-specify` producing `specs/NNN-*/spec.md`), leaving multi-phase strategic planning in an unstructured, manually maintained `ROADMAP.md` that drifted out of sync with completed features in `specs/` and required manual copy-pasting to initiate new feature specifications.

This research resolves all technical and architectural decisions for:
1. Establishing a canonical `roadmap-template.md` resolved via Spec Kit's 4-tier template hierarchy (core fallback in `.specify/templates/roadmap-template.md` and `base-governance` preset in `.specify/presets/base-governance/templates/roadmap-template.md`).
2. Designing a 100% script-free `.agents/skills/speckit-roadmap/SKILL.md` skill supporting five operational modes: Scaffold/Authoring, Phase Mutation (`--add`, `--update`, `--defer`), Read-Only Status & Drift Audit (`--status` / `--check`), Status Synchronization (`--sync`), and Specify Handoff (`--next` / `--specify <phase>`).
3. Defining deterministic repository evidence rules to compute `InferredEvidenceStatus` (`COMPLETED`, `IN_PROGRESS`, `PLANNED`, `DEFERRED`) across `specs/NNN-*`, git commit history, and active git worktrees.
4. Integrating roadmap phase extraction and isolated git worktree creation (`.worktrees/<NNN>-<short-name>`) directly into `.agents/skills/speckit-specify/SKILL.md`.
5. Updating the portable bootstrapper suite (`bootstrap-speckit.sh`, `bootstrap-speckit.ps1`, `.agents/skills/speckit-bootstrap/SKILL.md`, and `.specify/integrations/*.manifest.json`) to distribute the 12th managed skill (`speckit-roadmap`) and `roadmap-template.md` while protecting root `ROADMAP.md` as project-owned user state.

---

## Research Topics & Decisions

### Topic 1: Canonical `roadmap-template` Schema & 4-Tier Hierarchy Integration

#### Problem Statement
In `ROADMAP.md`, phases previously lacked explicit machine- and human-readable status columns, prerequisite declarations, and links to their tactical `specs/NNN-*` directories in the Overview of Initiatives table, and detailed phase sections varied in heading names (`Proposed Execution Flow` vs `Architectural Fit in Spec Kit`). Furthermore, `roadmap-template` must participate in Spec Kit's native 4-tier template resolution stack (`overrides` → `presets` → `extensions` → `core`).

#### Decision
- **Canonical Template Placement**:
  - Core fallback (Tier 4): `.specify/templates/roadmap-template.md`
  - Base governance preset (Tier 2): `.specify/presets/base-governance/templates/roadmap-template.md`, registered in `.specify/presets/base-governance/preset.yml` under `provides.templates` with `name: "roadmap-template"`, `file: "templates/roadmap-template.md"`, and `strategy: "replace"`.
- **Standardized Document Schema**:
  1. **Header & Governance Metadata**: Title, purpose narrative, `Last Updated: YYYY-MM-DD`, and a brief Spec Kit integration guide (`/speckit-roadmap`, `/speckit-specify`, `/speckit-orchestrate`).
  2. **Overview of Initiatives Table**:
     - Columns: `| Phase | Initiative | Status | Prerequisites | Spec | Goal | Key Deliverables |`
     - `Phase`: Sequential identifier (`**Phase 1**`, `**Phase 2**`, ...).
     - `Status`: Enum of `` `PLANNED` ``, `` `IN_PROGRESS` ``, `` `COMPLETED` ``, `` `DEFERRED` ``.
     - `Prerequisites`: `None` or comma-separated phase identifiers (e.g., `Phase 1, Phase 2`).
     - `Spec`: Link/path to tactical spec directory (e.g., `` `specs/001-base-governance-templates/` ``) or `—` when not yet specified.
  3. **Detailed Phase Sections**:
     - Heading: `## Phase N: <Initiative Title>`
     - `### Metadata`: Bullet list with `**Status**`, `**Prerequisites**`, and `**Spec Directory**`.
     - `### Problem Statement`: Numbered or bulleted problem context and motivation.
     - `### Architectural Fit in Spec Kit`: How the initiative integrates with Spec Kit templates, skills, presets, extensions, and governance.
     - `### Key Deliverables`: Concrete artifacts and outcomes required for completion.
     - `### Key Design Decisions to Resolve During Spec`: Specific design questions to seed `/speckit-specify` and `/speckit-clarify`.

#### Rationale
- Having both an Overview summary table and per-phase `### Metadata` blocks enables instant high-level scanning by humans while keeping per-phase sections self-contained when extracted by `/speckit-roadmap --next` or `/speckit-specify`.
- Synchronizing `.specify/templates/roadmap-template.md` and `.specify/presets/base-governance/templates/roadmap-template.md` matches the exact pattern established in Phase 1 and Phase 4 for `constitution-template`, `coding-standards-template`, and `logging-standards-template`.

#### Alternatives Considered
- *Storing roadmap state in a separate JSON sidecar (`.specify/roadmap.json`)*: Rejected because it violates Constitutional Principle IV (*Single Authoritative State*). Maintaining a separate JSON file alongside `ROADMAP.md` creates two competing sources of truth.
- *Omitting `Status` and `Spec` from `ROADMAP.md` and computing them only at runtime*: Rejected because human readers browsing `ROADMAP.md` in GitHub or an editor need immediate visibility into phase completion without running an agent command.

---

### Topic 2: 100% Script-Free `/speckit-roadmap` Architecture & Evidence Reconciliation Rules

#### Problem Statement
The original Phase 5 problem statement in `ROADMAP.md` written before Phase 4 mentioned a possible bash script (`.specify/scripts/bash/check-roadmap.sh`). However, Phase 4 (`004-portable-project-bootstrapper`) decommissioned `.specify/scripts/` entirely so all Spec Kit skills operate 100% natively using agent file and git inspection, and Constitutional Principle III prohibits automated test suites and runtime script harnesses.

#### Decision
- **100% Agent-Native Skill Execution**: Implement all five modes of `/speckit-roadmap` directly within `.agents/skills/speckit-roadmap/SKILL.md` with zero `.specify/scripts/` dependencies.
- **Deterministic Phase-to-Spec Matching Priority**:
  1. **Explicit Spec Link**: If the phase's `Spec` column or `### Metadata` already references `specs/NNN-<slug>`, verify that directory in the current workspace or active git worktrees.
  2. **Numeric Prefix + Keyword Match**: Match `Phase N` to `specs/00N-*` where normalized title keywords align.
  3. **Ambiguity Guard**: If multiple `specs/` directories could match a phase without an explicit link, classify as `AMBIGUOUS_MATCH` and emit a `WARN` diagnostic rather than guessing.
- **Deterministic `InferredEvidenceStatus` Evaluation**:
  - `DEFERRED`: Phase is explicitly marked `DEFERRED` in `ROADMAP.md` by human decision (preserved unless `--update` or `--specify` explicitly reactivates it).
  - `COMPLETED`: Matching `specs/NNN-*` contains `spec.md`, `plan.md`, and `tasks.md` with >0 task items and 0 unchecked `- [ ]` items (100% `- [x]`), OR git commit history on `main` / current branch contains the ratified implementation commit for that feature when ephemeral specs have been cleaned up.
  - `IN_PROGRESS`: Matching `specs/NNN-*` exists in the current checkout OR in an active git worktree (`git worktree list`) with `spec.md` present, and `tasks.md` is either not yet created or still has one or more unchecked `- [ ]` tasks.
  - `PLANNED`: No matching `specs/NNN-*` directory, active worktree, or implementation commit exists.
- **Read-Only vs. Mutating Boundary**:
  - `--status` and `--check` are strictly read-only and never mutate `ROADMAP.md`.
  - `--sync` updates only the `Status` and `Spec` fields in the Overview table and per-phase `### Metadata` sections to match `InferredEvidenceStatus`, leaving all narrative prose untouched.

#### Rationale
- Preserves the 100% script-free invariant (`SC-004`) established in Phase 4 while providing deterministic, repeatable status auditing across main checkouts and parallel git worktrees.
- Supports the Constitutional Ephemeral Specs workflow (where `specs/NNN-*` may exist during development or be verified via git history after merge).

#### Alternatives Considered
- *Reintroducing `.specify/scripts/bash/check-roadmap.sh`*: Rejected because it violates the Phase 4 zero-script architecture and `SC-004`.
- *Auto-mutating `ROADMAP.md` during `--status`*: Rejected because status inspection should never cause unexpected working-tree dirtiness; explicit `--sync` separates inspection from mutation per Principle VI.

---

### Topic 3: Seamless Handoff to `/speckit-specify` & First-Class Git Worktree Isolation

#### Problem Statement
When starting the next roadmap phase (e.g., `"Use a worktree, next roadmap phase"` or `/speckit-roadmap --next`), the agent needs to:
1. Deterministically select the earliest `PLANNED` phase whose `Prerequisites` are all `COMPLETED`.
2. Support creating an isolated git worktree (`.worktrees/<NNN>-<short-name>` on branch `<NNN>-<short-name>`) when requested so feature work is isolated from the primary checkout.
3. Seed `/speckit-specify` with the phase's structured `Problem Statement`, `Architectural Fit in Spec Kit`, `Key Deliverables`, and `Key Design Decisions to Resolve During Spec`.

#### Decision
- **Next-Phase Selection & Prerequisite Gate**:
  - Scan phases in ascending numerical order (`Phase 1`, `Phase 2`, ...).
  - Identify the first phase whose effective status (via live evidence reconciliation) is `PLANNED`.
  - Verify that every phase listed in its `Prerequisites` field has effective status `COMPLETED`.
  - If prerequisites are not `COMPLETED`, fail closed at the boundary with a `WARN` diagnostic naming the blocking prerequisite phase(s) unless `--force` is explicitly supplied.
- **Worktree Isolation Protocol in `speckit-specify` and `speckit-roadmap`**:
  - When the user input requests a git worktree (e.g., `"use a worktree"`, `"in a worktree"`, `--worktree`), derive `<NNN>-<short-name>` from the next sequential feature number and phase slug (e.g., `005-roadmap-management`).
  - Ensure `.worktrees/` is added to `.git/info/exclude` (or `.gitignore`) so worktree directories never pollute untracked file status in the parent checkout.
  - Create worktree via `git worktree add -b <NNN>-<short-name> .worktrees/<NNN>-<short-name> HEAD` (or reuse if already present).
  - Perform all subsequent feature state updates (`.specify/feature.json`, `specs/<NNN>-<short-name>/spec.md`, and `ROADMAP.md` status transition to `IN_PROGRESS`) inside the target workspace boundary.

#### Rationale
- Directly encodes the workflow used to launch Phase 5 itself (`"Use a worktree, next roadmap phase"`) into a repeatable, documented capability in both `speckit-roadmap` and `speckit-specify`.
- Excluding `.worktrees/` via `.git/info/exclude` keeps `git status` clean without modifying tracked `.gitignore` in repos that don't want worktree rules committed.

#### Alternatives Considered
- *Switching branches in-place in the root working tree*: Still supported as the default when worktree isolation is not requested, but insufficient when users want isolated parallel worktrees.

---

### Topic 4: Portable Bootstrapper & Protected User-State Integration

#### Problem Statement
Adding `.specify/templates/roadmap-template.md`, `.specify/presets/base-governance/templates/roadmap-template.md`, and `.agents/skills/speckit-roadmap/SKILL.md` expands the managed Spec Kit toolkit bundle. Meanwhile, a target repository's root `ROADMAP.md` is project-specific user state that must never be overwritten during bootstrap seeding or upgrades.

#### Decision
- **Seeder Scripts (`bootstrap-speckit.sh` & `bootstrap-speckit.ps1`)**:
  - Add `.specify/templates/roadmap-template.md` to the required source bundle integrity check array in both scripts.
  - Because both scripts copy only from `.specify` and `.agents` (`find .specify .agents -type f ...`), root `ROADMAP.md` is naturally never overwritten by the seeders; explicitly document `ROADMAP.md` in the Protected User-State comments/contract and keep both scripts well under the 150-line ceiling.
- **`speckit-bootstrap` Skill (`.agents/skills/speckit-bootstrap/SKILL.md`)**:
  - Add `ROADMAP.md` to the **Protected User-State Rule** allowlist alongside `.specify/memory/*.md`, `.specify/templates/overrides/**`, `.specify/feature.json`, and `specs/**`.
  - Update the managed skill count from 11 to 12 skills (including `speckit-roadmap`).
- **Integration Manifests (`.specify/integrations/*.manifest.json`)**:
  - `.specify/integrations/speckit.manifest.json`: Add `.specify/templates/roadmap-template.md` SHA-256 digest.
  - `.specify/integrations/agy.manifest.json`: Add `.agents/skills/speckit-roadmap/SKILL.md` SHA-256 digest and update modified skill digests (`speckit-bootstrap`, `speckit-specify`).
  - `.specify/integrations/speckit-bootstrap.manifest.json`: Add entries and updated SHA-256 digests + byte sizes for `.specify/templates/roadmap-template.md`, `.specify/presets/base-governance/templates/roadmap-template.md`, `.specify/presets/base-governance/preset.yml`, `.agents/skills/speckit-roadmap/SKILL.md`, `.agents/skills/speckit-specify/SKILL.md`, `.agents/skills/speckit-bootstrap/SKILL.md`, `.specify/integrations/speckit.manifest.json`, and `.specify/integrations/agy.manifest.json`.

#### Rationale
- Guarantees `/speckit-bootstrap --check` passes with zero unrecorded drift and ensures downstream repositories receive `roadmap-template.md` and `/speckit-roadmap` automatically when seeded or upgraded.

#### Alternatives Considered
- *Seeding a default `ROADMAP.md` into target repositories during `bootstrap-speckit.sh`*: Rejected because target repositories may already have their own `ROADMAP.md` or may prefer to scaffold one interactively via `/speckit-roadmap`.
