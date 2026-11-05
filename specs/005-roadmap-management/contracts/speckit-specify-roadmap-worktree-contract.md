# Integration Contract: `/speckit-specify` Roadmap Handoff & Git Worktree Isolation

**Feature**: `005-roadmap-management`  
**Modified Artifacts**:
- `.agents/skills/speckit-specify/SKILL.md`
- `.agents/skills/speckit-bootstrap/SKILL.md`
- `bootstrap-speckit.sh` & `bootstrap-speckit.ps1`  
**Date**: 2026-11-05  

---

## 1. Roadmap-Aware Specification Context Extraction (`speckit-specify`)

When `/speckit-specify` is invoked with a roadmap phase reference (e.g., `"next roadmap phase"`, `"roadmap phase 5"`, `"specify Phase 6"`, or via handoff from `/speckit-roadmap --next` / `--specify <phase>`):

1. **Locate & Parse `ROADMAP.md`**:
   - Read `${REPO_ROOT}/ROADMAP.md`. If missing or empty, fail closed with a `WARN` rejection instructing the user to run `/speckit-roadmap` first or provide an explicit feature description.
2. **Select Target Phase**:
   - If a specific phase (`Phase N`) was requested, select `Phase N`.
   - If `"next roadmap phase"` was requested, evaluate phase statuses using the deterministic evidence rules (checking `specs/NNN-*` and `ROADMAP.md`) and select the earliest `PLANNED` phase whose declared `Prerequisites` are all `COMPLETED` (and which is not already `IN_PROGRESS` or `COMPLETED` in the current checkout or an active worktree).
3. **Verify Prerequisites**:
   - Confirm all prerequisite phases listed for the target phase are `COMPLETED`. If any prerequisite is incomplete, halt before creating the spec directory, emit a `WARN` boundary rejection naming the incomplete prerequisite(s), and ask for confirmation (`--force`).
4. **Extract Authoritative Phase Context**:
   - Extract the target phase's:
     - `Initiative Title` (used to derive `<short-name>`, e.g., `roadmap-management`)
     - `Goal` (from the Overview table)
     - `### Problem Statement`
     - `### Architectural Fit in Spec Kit`
     - `### Key Deliverables`
     - `### Key Design Decisions to Resolve During Spec`
   - Combine these structured inputs with any additional user constraints in `$ARGUMENTS` to populate `SPECIFY_FEATURE_DIRECTORY/spec.md`.
5. **Update `ROADMAP.md` Phase State**:
   - Update the selected phase's `Status` to `` `IN_PROGRESS` `` and `Spec` to `` `specs/<NNN>-<short-name>/` `` in both the Overview of Initiatives table and the phase's `### Metadata` block.

---

## 2. Git Worktree Isolation Protocol (`speckit-specify` & `speckit-roadmap`)

When the user prompt or arguments request git worktree isolation (e.g., `"Use a worktree"`, `"in a worktree"`, or `--worktree`):

1. **Determine Feature Slug & Branch (`<NNN>-<short-name>`)**:
   - Scan `specs/` across the main checkout and active `git worktree list` branches to determine the next available 3-digit sequential prefix `<NNN>` (or match `Phase N` → `00N-<short-name>`).
2. **Configure Local Git Exclusion**:
   - Ensure `.worktrees/` is present in the primary repository's `.git/info/exclude` file so worktree directories never appear as untracked noise in `git status`.
3. **Create Isolated Worktree**:
   - Execute `git worktree add -b <NNN>-<short-name> .worktrees/<NNN>-<short-name> HEAD` (or if branch `<NNN>-<short-name>` already exists, `git worktree add .worktrees/<NNN>-<short-name> <NNN>-<short-name>`).
4. **Isolate Feature State Inside Worktree**:
   - Set active workspace root for the specification and downstream pipeline to `${PRIMARY_REPO_ROOT}/.worktrees/<NNN>-<short-name>`.
   - Create `specs/<NNN>-<short-name>/spec.md` and `specs/<NNN>-<short-name>/checklists/requirements.md` inside the worktree.
   - Write `{"feature_directory": "specs/<NNN>-<short-name>"}` to `.worktrees/<NNN>-<short-name>/.specify/feature.json`, leaving the primary checkout's `.specify/feature.json` untouched.

---

## 3. Bootstrapper & Manifest Packaging Contract

1. **Protected User-State Boundary (`speckit-bootstrap`, `bootstrap-speckit.sh`, `bootstrap-speckit.ps1`)**:
   - `ROADMAP.md` at the repository root is classified as **Protected User State** (`PRESERVE_USER_STATE`).
   - Neither `bootstrap-speckit.sh`, `bootstrap-speckit.ps1`, nor `/speckit-bootstrap [--upgrade] [--force]` may overwrite or delete a target repository's `ROADMAP.md`.
2. **Managed Asset Additions**:
   - `.specify/templates/roadmap-template.md` (Core template tier + required source asset check in `bootstrap-speckit.sh` and `bootstrap-speckit.ps1`).
   - `.specify/presets/base-governance/templates/roadmap-template.md` (Preset template tier, registered in `.specify/presets/base-governance/preset.yml`).
   - `.agents/skills/speckit-roadmap/SKILL.md` (12th managed Spec Kit skill).
   - Synchronized SHA-256 digests and byte sizes across `.specify/integrations/speckit.manifest.json`, `.specify/integrations/agy.manifest.json`, and `.specify/integrations/speckit-bootstrap.manifest.json`.
