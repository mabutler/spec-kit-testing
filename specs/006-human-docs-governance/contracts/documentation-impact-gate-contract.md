# Contract 2: Downstream Spec Kit Skill Documentation Gates

**Feature**: `006-human-docs-governance`  
**Covers**: `FR-006`, `FR-007`, `FR-008`, `SC-002`, `SC-003`

---

## 1. Planning Gate (`plan-template.md` & `.agents/skills/speckit-plan/SKILL.md`)

### 1.1 `.specify/templates/plan-template.md` Additions
Under `## Technical Context`, include the mandatory **Documentation Impact** field:
```markdown
**Documentation Impact**: [USER_FACING (list affected human-facing docs, e.g., README.md, docs/...) or INTERNAL_ONLY (1-sentence rationale why no user-visible CLI, skill, API, config, or workflow changes occur)]
```
Under `## Constitution Check`, note that Principle VII human-facing documentation impact (`USER_FACING` target files vs. `INTERNAL_ONLY` exemption rationale) MUST be evaluated before Phase 0 and re-checked after Phase 1.

### 1.2 `.agents/skills/speckit-plan/SKILL.md` Additions
In `Outline -> 3. Execute plan workflow`:
- Populate `**Documentation Impact**` in `Technical Context` by classifying the feature as either `USER_FACING` (naming the exact human-facing documentation files such as `README.md` or user guides to create/update per `.specify/memory/coding-standards.md` `[HUMAN_DOCS_CONVENTIONS]` or baseline Principle VII) or `INTERNAL_ONLY` (providing a concrete rationale why no user-visible commands, skills, APIs, configuration options, or workflows change). If `.specify/memory/coding-standards.md` predates Phase 6 and lacks a Human-Facing Documentation section, fall back gracefully to the baseline Principle VII rule.
- In `Constitution Check`, verify Principle VII human-facing documentation alignment alongside Principle III test justifications.

---

## 2. Task Generation Gate (`tasks-template.md` & `.agents/skills/speckit-tasks/SKILL.md`)

### 2.1 `.specify/templates/tasks-template.md` Additions
- In the header notes / `Phase N: Polish & Cross-Cutting Concerns`, clarify that human-facing documentation tasks (`README.md`, user guides) are generated with exact file paths in the relevant User Story phase or Polish phase when `Documentation Impact` is `USER_FACING`, and omitted when `INTERNAL_ONLY` so internal refactors incur zero artificial `README.md` churn.

### 2.2 `.agents/skills/speckit-tasks/SKILL.md` Additions
- In `Outline -> 3. Execute task generation workflow` and `Task Organization`:
  - Inspect `Documentation Impact` in `plan.md` (and user stories in `spec.md`) alongside `.specify/memory/constitution.md` Principle VII and `.specify/memory/coding-standards.md` (falling back gracefully if `coding-standards.md` lacks the Phase 6 section).
  - When `Documentation Impact` is `USER_FACING` (or a user story modifies user-visible CLI commands, skills, APIs, configuration options, or workflows), generate explicit task(s) with exact file paths (e.g., `- [ ] TXXX [USX] Update human-facing documentation in README.md`) in the corresponding User Story phase or Polish phase.
  - When `Documentation Impact` is `INTERNAL_ONLY` with a valid exemption rationale, do **not** generate redundant `README.md` edit tasks.

---

## 3. Cross-Artifact Analysis Gate (`.agents/skills/speckit-analyze/SKILL.md`)

In `Execution Steps`:
- **Step 2 (`From plan.md`)**: Load `Documentation Impact` classification (`USER_FACING` target files or `INTERNAL_ONLY` rationale).
- **Step 4.D (`Constitution Alignment`) & Step 4.E (`Coverage Gaps`)**:
  - Verify Principle VII human-facing documentation gate:
    1. If a feature or user story introduces or modifies user-visible CLI commands, agent skills, public APIs, configuration options, or workflows, `plan.md` MUST classify `Documentation Impact` as `USER_FACING` and `tasks.md` MUST include at least one task targeting the affected human-facing documentation (`README.md`, user guides).
    2. If `plan.md` declares `INTERNAL_ONLY`, verify that the exemption rationale is non-empty and does not contradict user-visible requirements in `spec.md`; when valid, require 0 `README.md` tasks.
    3. Flag missing `Documentation Impact` classification, contradicting `INTERNAL_ONLY` claims on user-visible features, or `USER_FACING` features lacking mapped documentation tasks in `tasks.md` as `CRITICAL` (Constitution Principle VII Alignment) or `HIGH` (Coverage Gap).
    4. Flag any planned documentation task or artifact outside `specs/` that prescribes citing ephemeral `specs/NNN-*/` paths or `FR-XXX`/`SC-XXX` identifiers in permanent human-facing documentation as `CRITICAL` (Development Workflow & Quality Gates violation).

---

## 4. Implementation & Convergence Gates (`speckit-implement` & `speckit-converge`)

### 4.1 `.agents/skills/speckit-implement/SKILL.md` Additions
- In Step 6 (`Enforce governance conventions`) and Step 9 (`Completion validation`):
  - When `Documentation Impact` is `USER_FACING`, verify that all planned human-facing documentation files (`README.md`, user guides) have been created or updated to match actual as-built behavior, contain valid relative links, and include zero references to ephemeral `specs/NNN-*/` directories or `FR-XXX`/`SC-XXX` identifiers per Principle VII and Development Workflow & Quality Gates.

### 4.2 `.agents/skills/speckit-converge/SKILL.md` Additions
- In Step 3 (`Build the Intent Inventory`) and Step 4 (`Assess the Codebase and Classify Findings`):
  - Include `Documentation Impact` (`USER_FACING` target files vs. `INTERNAL_ONLY` exemption) and Principle VII human-facing documentation obligations in the intent inventory.
  - When `USER_FACING`, inspect target human-facing documentation files (`README.md`, user guides) on disk and emit a `Finding` (`missing`, `partial`, or `contradicts`) if required documentation updates are absent, out of sync with implemented behavior, have broken relative links, or reference ephemeral `specs/NNN-*/` paths or `FR-XXX`/`SC-XXX` identifiers.
  - When `INTERNAL_ONLY` (and consistent with `spec.md`), require zero `README.md` edits and emit no false-positive documentation gap findings.
