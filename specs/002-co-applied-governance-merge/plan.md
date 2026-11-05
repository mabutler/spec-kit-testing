# Implementation Plan: Co-Applied Governance & Constitutional Merge

**Branch**: `002-co-applied-governance-merge` | **Date**: 2026-11-04 | **Spec**: [spec.md](file:///home/admin/projects/spec-kit-testing/specs/002-co-applied-governance-merge/spec.md)

**Input**: Feature specification from `/specs/002-co-applied-governance-merge/spec.md`

## Summary

This feature implements Phase 2 of the Spec Kit Governance Roadmap (*Co-Applied Governance & Constitutional Merge*):
1. **Simultaneous Governance Co-Application & Intelligent Merge (`speckit-constitution`)**: Upgrades `.agents/skills/speckit-constitution/SKILL.md` so that creating or updating the project constitution resolves all three Phase 1 templates (`constitution-template`, `coding-standards-template`, `logging-standards-template` via `resolve-template.sh` with direct 4-tier filesystem fallback), evaluates Optional Enhancement Modules (`MODULE-A`–`MODULE-D`, `MODULE-D-AOT-TRIM`, and optional `TRACE` logging), non-destructively merges project-specific conventions and all 25 `[ALL_CAPS_IDENTIFIER]` slots while enforcing the Constitutional Conflict Resolution Gate, and writes `.specify/memory/constitution.md`, `.specify/memory/coding-standards.md`, and `.specify/memory/logging-standards.md` in a single atomic workflow.
2. **Downstream Lifecycle Enforcement**: Updates `.agents/skills/speckit-plan/SKILL.md`, `.agents/skills/speckit-tasks/SKILL.md`, `.agents/skills/speckit-analyze/SKILL.md`, `.agents/skills/speckit-implement/SKILL.md`, and `.agents/skills/speckit-converge/SKILL.md` so every downstream workflow loads and enforces `.specify/memory/coding-standards.md` and `.specify/memory/logging-standards.md` alongside `.specify/memory/constitution.md` (with graceful fallback when companion files are absent in legacy repos).
3. **Repository Self-Application**: Executes the co-applied governance workflow on `spec-kit-testing` to materialize `.specify/memory/coding-standards.md` and `.specify/memory/logging-standards.md` synchronized with `.specify/memory/constitution.md`.

---

## Technical Context

**Language/Version**: Markdown (CommonMark / GitHub Flavored Markdown) for Spec Kit skill definitions and governance documents; Bash 4.0+ (existing `.specify/scripts/bash/*.sh` CLI helpers).

**Primary Dependencies**: None (zero external runtime package dependencies). Uses existing `.specify/scripts/bash/resolve-template.sh` and `.specify/scripts/bash/common.sh` where Bash is available, with direct 4-tier file resolution fallback.

**Storage**: Flat Markdown files in `.specify/memory/` (`constitution.md`, `coding-standards.md`, `logging-standards.md`) and `.agents/skills/speckit-*/SKILL.md`.

**Verification**: Static analysis, syntax validation (`bash -n`), markdown/link linting, and declarative quality gates per Constitution v2.0.0 Principle III (*Static Verification & No Automated Tests*) and `coding-standards.md`. Zero automated test suites generated.

**Target Platform**: Platform-agnostic (Linux, macOS, Windows).

**Project Type**: Agent skill workflows (`.agents/skills/`) and ratified project governance suite (`.specify/memory/`).

**Performance Goals**: Instant static Markdown loading; sub-50ms template resolution via `.specify/scripts/bash/resolve-template.sh`.

**Constraints**:
- Must not modify template source files in `.specify/templates/` or existing bash scripts in `.specify/scripts/bash/`.
- Must not add standalone test suites (`tests/`) or extra helper scripts (`scripts/`) that clutter the repository root.
- Must guarantee zero unresolved `[ALL_CAPS_IDENTIFIER]` tokens in `.specify/memory/{constitution,coding-standards,logging-standards}.md` and zero `OPTIONAL-MODULE`, `OPTIONAL-SUBCLAUSE`, or `DEFAULT-CLAUSE` HTML comments in `.specify/memory/constitution.md`.
- Must preserve existing project conventions, original `RATIFICATION_DATE`, and ratified `Recorded Deviations` across iterative `/speckit-constitution` runs.

**Scale/Scope**: 6 agent skill files updated in `.agents/skills/` (`speckit-constitution`, `speckit-plan`, `speckit-tasks`, `speckit-analyze`, `speckit-implement`, `speckit-converge`) and 3 governance files co-applied in `.specify/memory/` (`constitution.md`, `coding-standards.md`, `logging-standards.md`).

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Evaluated against `.specify/memory/constitution.md` (v2.0.0):

- **Principle I (Evidence Over Invention & Bounded Investigation)**: **PASS**. All 25 placeholder mappings for `spec-kit-testing`, template resolution rules, and skill integration points trace directly to `.specify/templates/*.md`, `.specify/scripts/bash/common.sh`, `.agents/skills/*/SKILL.md`, and `specs/001-base-governance-templates/contracts/`. Unresolvable placeholders in future target repos are required to emit explicit `TODO(<FIELD_NAME>)` markers rather than invented guesses.
- **Principle II (Two-Tier Failure Model & Fail Closed on Required State)**: **PASS**. `speckit-constitution` fails closed if template resolution fails or if a pre-write validation gate detects unresolved placeholders or leftover conditional comments; conflicts with Core Principles cannot be silently swallowed and require alignment or a 5-field `Recorded Deviation`.
- **Principle III (Static Verification & No Automated Tests)**: **PASS**. Automated test generation is disabled repository-wide per Constitution v2.0.0 and `coding-standards.md`. Spec Kit workflows (`spec.md`, `plan.md`, `tasks.md`, `implement`) MUST NOT generate unit test files, integration test harnesses, or test tasks. Feature verification relies entirely on static syntax verification (`bash -n`), markdown linting, link validation, and declarative quality gates without generating automated test suites or test tasks.
- **Principle IV (Single Authoritative State, Enforced Boundaries & Safe Concurrency)**: **PASS**. `.specify/memory/` is the single canonical location for ratified project governance, strictly separated from read-only templates in `.specify/templates/` and downstream consumers in `.agents/skills/`.
- **Principle V (Centralized Dependencies & Protected Toolchain Gate)**: **PASS**. Zero third-party packages added; no toolchain or lockfile modifications.
- **Principle VI (Bounded Resources & Verify-Before-Destroy)**: **PASS**. Existing `.specify/memory/` files are inspected and merged before writing; pre-write validation checks pass before finalizing updates.
- **Principle VII (Code Hygiene, Ubiquitous Language & Safe Logging)**: **PASS**. Uses consistent terminology (`Co-Applied Governance Suite`, `Optional Enhancement Modules`, `Sync Impact Report`, `Recorded Deviations`), zero warnings, and no secrets or PII.

### Post-Design Gate Evaluation
- **All Clarifications Resolved**: **PASS**. Zero `NEEDS CLARIFICATION` markers remain; all design decisions are documented in `research.md`.
- **Artifact Alignment**: **PASS**. `data-model.md`, `contracts/co-applied-governance-merge-contract.md`, `contracts/downstream-skill-governance-contract.md`, and `quickstart.md` are complete and aligned with `spec.md`.
- **Gate Status**: **ALL GATES PASSED**.

---

## Project Structure

### Documentation (this feature)

```text
specs/002-co-applied-governance-merge/
├── plan.md              # This file (/speckit-plan command output)
├── research.md          # Phase 0 output: co-application, merge precedence, and skill integration decisions
├── data-model.md        # Phase 1 output: entities, relationships, state transitions, and validation rules
├── quickstart.md        # Phase 1 output: runnable verification scenarios
├── contracts/           # Phase 1 output: workflow and downstream skill interface contracts
│   ├── co-applied-governance-merge-contract.md
│   └── downstream-skill-governance-contract.md
└── tasks.md             # Phase 2 output (/speckit-tasks command - NOT created by /speckit-plan)
```

### Source Code (repository root)

```text
.agents/skills/
├── speckit-constitution/
│   └── SKILL.md         # Upgraded to resolve, merge, validate, and write all 3 governance files
├── speckit-plan/
│   └── SKILL.md         # Updated to load coding-standards.md & logging-standards.md alongside constitution.md
├── speckit-tasks/
│   └── SKILL.md         # Updated to load coding-standards.md & logging-standards.md alongside constitution.md
├── speckit-analyze/
│   └── SKILL.md         # Updated to enforce coding-standards.md & logging-standards.md in governance alignment
├── speckit-implement/
│   └── SKILL.md         # Updated to enforce coding-standards.md & logging-standards.md during implementation
└── speckit-converge/
    └── SKILL.md         # Updated to assess codebase against coding-standards.md & logging-standards.md

.specify/memory/
├── constitution.md      # Ratified project constitution (updated with expanded Sync Impact Report)
├── coding-standards.md  # Co-applied project coding standards (populated from coding-standards-template)
└── logging-standards.md # Co-applied project logging standards (populated from logging-standards-template)
```

**Structure Decision**: Modifies the existing Spec Kit skill definitions in `.agents/skills/speckit-*/SKILL.md` and materializes the three ratified governance files in `.specify/memory/`, adhering strictly to Spec Kit's directory layout without introducing external scripts or directories.

---

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

*No constitutional violations. Zero complexity exceptions.*
