# Phase 0 Research: Human-Facing Documentation Standards & Governance

**Feature**: `006-human-docs-governance`  
**Date**: 2026-11-05  
**Spec**: [spec.md](spec.md)

## Overview

This research document resolves all architectural, template-design, and workflow-gate decisions for Phase 6 (*Human-Facing Documentation Standards & Governance*). All findings are grounded in direct inspection of the active repository state under `.specify/` and `.agents/` per Constitutional Principle I (*Evidence Over Invention*).

---

## Decision 1: Dual-Tier Governance Placement (Principle VII Baseline + `MODULE-DOCS` + `coding-standards-template.md` Slot)

- **Decision**:
  1. **Constitutional Baseline (Principle VII in `constitution-template.md` & `.specify/presets/base-governance/templates/constitution-template.md`)**: Expand bullet 3 of Principle VII (`Present-Tense, High-Signal Comments & Docs`, `constitution-template.md:116`) to explicitly enforce **Human-Facing Documentation Synchronization**: any change that adds, removes, or modifies user-visible CLI commands, agent skills, public APIs, configuration options, or end-user workflows MUST update the corresponding human-facing documentation (`README.md`, quickstarts, or user guides) in the same change, whereas purely internal changes (`INTERNAL_ONLY` refactors, non-behavioral fixes, or internal tooling) are exempt from artificial `README.md` edits.
  2. **Optional Enhancement Module (`MODULE-DOCS` in `constitution-template.md`)**: Add an optional module block `<!-- OPTIONAL-MODULE: MODULE-DOCS ... -->` at the end of Principle VII (`constitution-template.md:117-118`) titled `Structured Human-Facing Documentation Gate`:
     ```markdown
     <!-- OPTIONAL-MODULE: MODULE-DOCS
     Action: ADD
     Title: Structured Human-Facing Documentation Gate
     Target: Principle VII
     -->
     - **Structured Human-Facing Documentation Gate**: The repository root `README.md` (and any dedicated user guide under `docs/`) MUST maintain canonical sections covering Project Overview & Architecture, Getting Started / Bootstrap Quickstart, CLI / Skill / API Usage Reference, and Configuration & Governance Verification, verified for link and command accuracy before merge.
     <!-- /OPTIONAL-MODULE: MODULE-DOCS -->
     ```
  3. **Companion Coding Standard (`coding-standards-template.md` & `.specify/presets/base-governance/templates/coding-standards-template.md`)**: Add a dedicated section `## Human-Facing Documentation & README Conventions` operationalizing Constitutional Principle VII with placeholder slot `[HUMAN_DOCS_CONVENTIONS]` and archetype examples (CLI tools, libraries/SDKs, web services, agent/skill frameworks).
- **Rationale**: Preserves the separation of concerns established in Phases 1 and 2 (`ROADMAP.md:20-61`): `constitution.md` holds universal engineering policy and optional strict gates (`MODULE-DOCS`), while `coding-standards.md` holds stack- and archetype-specific file layout and section conventions (`[HUMAN_DOCS_CONVENTIONS]`). Maintaining byte-for-byte parity between `.specify/templates/` and `.specify/presets/base-governance/templates/` ensures Tier 2 preset resolution (`preset.yml` with `strategy: replace`) and Tier 4 core fallback return identical templates.
- **Alternatives Considered**:
  - *Placing all documentation rules solely in `coding-standards-template.md`*: Rejected because Constitutional Principle VII is the supreme authority enforced as `CRITICAL` by `/speckit-analyze` (`speckit-analyze/SKILL.md:63,140-143`).
  - *Making strict multi-section `README.md` structure mandatory for all micro-libraries without `MODULE-DOCS`*: Rejected because small internal packages may only need baseline synchronization, whereas full product/toolkit repositories benefit from enabling `MODULE-DOCS`.

---

## Decision 2: `/speckit-constitution` Slot Reconciliation & `MODULE-DOCS` Lifecycle

- **Decision**: Update `.agents/skills/speckit-constitution/SKILL.md` across Steps 2, 3, 4, 6, and 7:
  - **Step 2 (Module Activation, `SKILL.md:93-107`)**: Add `MODULE-DOCS` (*Structured Human-Facing Documentation Gate*, Target: Principle VII) to the evaluated optional modules list alongside `MODULE-A`, `MODULE-B`, `MODULE-C`, `MODULE-D` (`MODULE-D-AOT-TRIM`), and `logging_trace`.
  - **Step 3 (Structural Transformations, `SKILL.md:108-126`)**: Specify `MODULE-DOCS` transformation rules (`ENABLED` strips opening/closing `<!-- OPTIONAL-MODULE: MODULE-DOCS ... -->` comment markers and retains `- **Structured Human-Facing Documentation Gate**: ...` in Principle VII; `OMITTED` removes the entire comment block and body).
  - **Step 4 (Placeholder Value Merge, `SKILL.md:127-133`)**: Align the documented slot list in `speckit-constitution/SKILL.md` with the actual `[ALL_CAPS_IDENTIFIER]` slots in `coding-standards-template.md` and `logging-standards-template.md`, adding `[HUMAN_DOCS_CONVENTIONS]` as the 12th slot in `coding-standards.md` for a total of **26** tracked slots (`8` in `constitution.md`, `12` in `coding-standards.md`, `6` in `logging-standards.md`).
  - **Step 6 (`Sync Impact Report`, `SKILL.md:165-180`)**: Include `MODULE-DOCS: <ENABLED|OMITTED>` in the `- Optional Modules:` line of the top HTML comment.
- **Rationale**: Inspecting `coding-standards-template.md:1-83` shows 11 existing slots (`[PROJECT_NAME]`, `[PRIMARY_LANGUAGE_AND_RUNTIME]`, `[BUILD_AND_LINTER_COMMANDS]`, `[DEPENDENCY_AND_LOCKFILE_CONVENTIONS]`, `[PROJECT_STRUCTURE_CONVENTIONS]`, `[BOUNDARY_ENFORCEMENT_MECHANISM]`, `[ERROR_RESULT_TYPES]`, `[DEFECT_INVARIANT_MECHANISM]`, `[IMMUTABLE_SNAPSHOT_AND_ID_CONVENTIONS]`, `[TEST_FRAMEWORK_CONVENTIONS]`, `[NAMING_CONVENTIONS]`). Adding `[HUMAN_DOCS_CONVENTIONS]` brings `coding-standards-template.md` to 12 slots and the suite total to 26 slots, while synchronizing the slot names listed in `speckit-constitution/SKILL.md:129-132` with the actual templates.
- **Alternatives Considered**:
  - *Leaving `[HUMAN_DOCS_CONVENTIONS]` out of `speckit-constitution/SKILL.md`'s slot inventory*: Rejected because Step 7 (`Pre-Write Validation Gate`, `SKILL.md:187`) enforces zero matches for `\[[A-Z0-9_]+\]`; explicit slot registration ensures deterministic discovery and substitution.

---

## Decision 3: Active Repository Governance Amendment (`v2.0.0 -> v2.1.0`) & `MODULE-DOCS: ENABLED`

- **Decision**:
  - Amend `.specify/memory/constitution.md` from version `2.0.0` to `2.1.0` (`Ratified: 2026-11-04`, `Last Amended: 2026-11-05`).
  - Enable `MODULE-DOCS: ENABLED` for this repository so that the Spec Kit customization toolkit dogfoods its own **Structured Human-Facing Documentation Gate** in Principle VII.
  - Update the top HTML `Sync Impact Report` comment in `.specify/memory/constitution.md:1-10` to record `Version Change: 2.0.0 -> 2.1.0`, the expanded Principle VII human-facing documentation synchronization rule and `MODULE-DOCS: ENABLED` gate, and updated `coding-standards.md`.
  - Update `.specify/memory/coding-standards.md` by adding `## Human-Facing Documentation & README Conventions` defining concrete rules for `README.md`, `ROADMAP.md`, and `.agents/skills/speckit-*/SKILL.md` documentation in this repository.
- **Rationale**: Per Constitutional Governance versioning rules (`constitution.md:88`), adding an expanded normative clause and quality gate to Principle VII without backward-incompatible principle removal is a `MINOR` version bump (`2.0.0 -> 2.1.0`). Enabling `MODULE-DOCS` ensures this repository serves as a complete reference implementation for Phase 6 (`spec.md:31-41`, `FR-004`, `FR-005`).
- **Alternatives Considered**:
  - *Bumping to `3.0.0` (`MAJOR`)*: Rejected because no existing principle is weakened or removed; Principle III remains `Static Verification & No Automated Tests` as ratified in v2.0.0.
  - *Leaving `MODULE-DOCS: OMITTED` in active `.specify/memory/constitution.md`*: Rejected because User Story 2 specifically establishes a canonical multi-section root `README.md` governed by the structured documentation standard.

---

## Decision 4: Explicit `Documentation Impact` Classification Across Downstream Skills

- **Decision**: Introduce a deterministic **Documentation Impact** classification (`USER_FACING` | `INTERNAL_ONLY`) across the Spec Kit delivery pipeline:
  1. **`plan-template.md` & `speckit-plan/SKILL.md`**: Add `**Documentation Impact**: [USER_FACING (list target files, e.g., README.md, docs/...) | INTERNAL_ONLY (one-sentence rationale why no user-visible CLI, skill, API, config, or workflow changes occur)]` in `Technical Context` and verify Principle VII documentation compliance in `Constitution Check`.
  2. **`tasks-template.md` & `speckit-tasks/SKILL.md`**: Instruct `/speckit-tasks` to inspect `Documentation Impact` in `plan.md` (and user stories in `spec.md`). When `USER_FACING`, generate explicit task items (`- [ ] TXXX [USX] Update human-facing documentation in <path>`) in the corresponding User Story phase or Polish phase. When `INTERNAL_ONLY`, omit artificial `README.md` tasks.
  3. **`speckit-analyze/SKILL.md`**: Under Step 4.D (`Constitution Alignment`) and Step 4.E (`Coverage Gaps`), verify that any feature introducing or modifying user-visible CLI commands, skills, APIs, configuration options, or workflows either has mapped human-facing documentation task(s) in `tasks.md` (`USER_FACING`) or a valid `INTERNAL_ONLY` exemption rationale in `plan.md`. Missing documentation coverage on a `USER_FACING` change is flagged as `CRITICAL` (Constitution Principle VII violation) or `HIGH` (Coverage Gap).
  4. **`speckit-implement/SKILL.md` & `speckit-converge/SKILL.md`**: During implementation completion validation (`speckit-implement/SKILL.md:179-184`) and convergence assessment (`speckit-converge/SKILL.md:148-169`), verify that required `USER_FACING` documentation updates are completed on disk, accurately match implemented behavior, have valid relative links, and contain zero references to ephemeral `specs/NNN-*/` paths or `FR-XXX`/`SC-XXX` identifiers.
- **Rationale**: Heuristic filename guessing is brittle; an explicit two-state classification (`USER_FACING` vs `INTERNAL_ONLY`) in `plan.md` provides an auditable contract consumed identically by `tasks`, `analyze`, `implement`, and `converge` while protecting internal-only refactors from unnecessary `README.md` churn (`spec.md:63,113`).
- **Alternatives Considered**:
  - *Requiring a `README.md` edit on every feature regardless of scope*: Rejected because it violates the `INTERNAL_ONLY` edge case (`spec.md:63`, `SC-003`) and creates merge conflicts on internal refactors.

---

## Decision 5: Root `README.md` Architecture & Manifest Digest Synchronization

- **Decision**:
  - Author a comprehensive root `README.md` in `/home/admin/projects/spec-kit-testing/.worktrees/006-human-docs-governance/README.md` (currently absent from the repository root) containing:
    1. **Project Overview & Architecture**: Spec Kit customization toolkit, native 4-tier template resolution hierarchy (`overrides` -> `presets` -> `extensions` -> `core`), and zero-external-dependency design.
    2. **Co-Applied Governance Suite**: Overview of `.specify/memory/{constitution,coding-standards,logging-standards}.md`, Core Principles I–VII, optional modules (`MODULE-A`, `MODULE-B`, `MODULE-C`, `MODULE-D`, `MODULE-D-AOT-TRIM`, `MODULE-DOCS`, `TRACE`), and `Documentation Impact` gates.
    3. **Spec Kit Agent Skills Reference**: Complete table and workflow guide for all 11 skills (`/speckit-specify`, `/speckit-clarify`, `/speckit-plan`, `/speckit-tasks`, `/speckit-checklist`, `/speckit-analyze`, `/speckit-implement`, `/speckit-converge`, `/speckit-constitution`, `/speckit-orchestrate`, `/speckit-bootstrap`) and role profiles (`speckit-reasoner`, `speckit-executor`).
    4. **Portable Bootstrapping & Quickstart**: Seeding via `./bootstrap-speckit.sh <target-repo> [--force]` and `pwsh ./bootstrap-speckit.ps1 <target-repo> [-Force]`, plus `/speckit-bootstrap` modes (`--check`, `--upgrade`, `--init-governance`).
    5. **Verification & Quality Gates**: Static verification gates (`bash -n`, template/preset parity, placeholder regex checks, manifest SHA-256 verification) per Principle III.
  - Note that `README.md` is a repository-level documentation file (not a bootstrapper-managed toolkit payload in `.specify/` or `.agents/`, per `bootstrap-speckit.sh:93`).
  - Synchronize SHA-256 digests and `size_bytes` for all modified managed files across `.specify/integrations/speckit.manifest.json`, `.specify/integrations/agy.manifest.json`, and `.specify/integrations/speckit-bootstrap.manifest.json`.
- **Rationale**: Directly satisfies `FR-005`, `FR-009`, `SC-004`, and `SC-005`. Because `speckit-bootstrap.manifest.json` also tracks the SHA-256 digests and byte sizes of `speckit.manifest.json` (`speckit-bootstrap.manifest.json:107-110`) and `agy.manifest.json` (`speckit-bootstrap.manifest.json:102-105`), manifest updates must compute `speckit.manifest.json` and `agy.manifest.json` first and then compute `speckit-bootstrap.manifest.json` last.
- **Alternatives Considered**:
  - *Adding root `README.md` to `.specify/integrations/speckit-bootstrap.manifest.json`*: Rejected because `bootstrap-speckit.sh:93` only seeds `.specify` and `.agents` into target repositories and must never overwrite a target project's own root `README.md`.
