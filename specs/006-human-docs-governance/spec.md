# Feature Specification: Human-Facing Documentation Standards & Governance

**Feature Branch**: `006-human-docs-governance`

**Created**: 2026-11-05

**Status**: Draft

**Input**: User description: "In a worktree, last roadmap phase"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Base Governance Templates & Co-Applied Human-Facing Documentation Standards (Priority: P1)

Platform engineers and project maintainers using Spec Kit's Base Governance Suite need explicit constitutional principles and companion coding-standard rules in `.specify/templates/` and `.specify/presets/base-governance/templates/` that govern when and how human-facing documentation (`README.md`, onboarding guides, CLI/skill usage references, and quickstarts) must be authored and maintained alongside code changes.

**Why this priority**: Previously, `.specify/templates/constitution-template.md` and `.specify/templates/coding-standards-template.md` focused on internal architectural contracts (`Architecture.md`), machine/agent epistemic hierarchy, and in-code "why" comments, leaving human-facing documentation (`README.md` and user guides) ungoverned. Establishing both a universal baseline mandate in Principle VII (with an optional enhancement module `MODULE-DOCS` for strict structured documentation gates) and a dedicated Human-Facing Documentation Conventions section in `coding-standards-template.md` ensures every project adopting the governance suite enforces living human-readable documentation.

**Independent Test**: Can be fully tested by inspecting `.specify/templates/{constitution-template,coding-standards-template}.md` and `.specify/presets/base-governance/templates/{constitution-template,coding-standards-template}.md` for parity, verifying the presence of the human-facing documentation baseline clause and optional `MODULE-DOCS` markers in `constitution-template.md`, verifying the human-facing documentation section and placeholder slot in `coding-standards-template.md`, and verifying that `.agents/skills/speckit-constitution/SKILL.md` handles `MODULE-DOCS` activation/omission and slot resolution cleanly with zero residual template markers.

**Acceptance Scenarios**:

1. **Given** `.specify/templates/constitution-template.md` and `.specify/presets/base-governance/templates/constitution-template.md`, **When** resolved by `/speckit-constitution` or inspected statically, **Then** Principle VII (*Code Hygiene, Ubiquitous Language & Safe Logging*) includes a mandatory baseline human-facing documentation synchronization rule requiring any change to user-visible commands, APIs, skills, configuration options, or workflows to update `README.md` or user guides in the same change, plus an optional `MODULE-DOCS` block (`<!-- OPTIONAL-MODULE: MODULE-DOCS ... -->`) for strict required-section and onboarding/migration guide gates.
2. **Given** `.specify/templates/coding-standards-template.md` and `.specify/presets/base-governance/templates/coding-standards-template.md`, **When** resolved by `/speckit-constitution`, **Then** they include a dedicated **Human-Facing Documentation & README Conventions** section with a `[HUMAN_DOCS_CONVENTIONS]` placeholder slot adaptable across project archetypes (CLI tools, libraries/SDKs, web services, and agent/skill frameworks).
3. **Given** a user running `/speckit-constitution` to initialize or amend a project's governance suite, **When** `MODULE-DOCS` is either `ENABLED` or `OMITTED` and `[HUMAN_DOCS_CONVENTIONS]` is resolved, **Then** `/speckit-constitution` strips all `MODULE-DOCS` comment markers, populates `[HUMAN_DOCS_CONVENTIONS]` without leaving unresolved `[ALL_CAPS_IDENTIFIER]` brackets, and records `MODULE-DOCS: <ENABLED|OMITTED>` in the top HTML `Sync Impact Report`.

---

### User Story 2 - Active Repository Constitution Amendment & Canonical `README.md` Ratification (Priority: P2)

Maintainers and contributors of this repository need `.specify/memory/constitution.md` and `.specify/memory/coding-standards.md` formally amended to ratify the Phase 6 human-facing documentation standards, accompanied by a comprehensive, up-to-date root `README.md` that documents the repository's Spec Kit architecture, governance suite, agent skills, and portable bootstrapper.

**Why this priority**: To eliminate template-versus-active drift (Problem Statement #3 in `ROADMAP.md`), this repository must dogfood its own ratified human-facing documentation standards. Amending `.specify/memory/constitution.md` (bumping version `2.0.0 -> 2.1.0` per semantic versioning rules for expanded principles/gates) and `.specify/memory/coding-standards.md`, while authoring a complete root `README.md`, establishes a verified reference implementation.

**Independent Test**: Can be fully tested by verifying `.specify/memory/constitution.md` is at version `2.1.0` with an updated top `Sync Impact Report` comment, zero residual template markers or `[ALL_CAPS]` placeholders, updated Principle VII and Quality Gates, synchronized `.specify/memory/coding-standards.md`, and a root `README.md` containing all required human-facing documentation sections matching actual repository capabilities.

**Acceptance Scenarios**:

1. **Given** the active `.specify/memory/constitution.md` (currently v2.0.0) and `.specify/memory/coding-standards.md`, **When** amended for Phase 6, **Then** `constitution.md` is bumped to `2.1.0`, the top `Sync Impact Report` records the amendment rationale and `MODULE-DOCS` state, Principle VII mandates same-change human-facing documentation updates for user-visible changes while exempting purely internal changes, and `coding-standards.md` defines the concrete `README.md` and skill-documentation conventions for this repository.
2. **Given** the repository root, **When** a human developer or onboarding contributor opens `README.md`, **Then** `README.md` clearly documents the project overview, the Co-Applied Governance Suite (`.specify/memory/{constitution,coding-standards,logging-standards}.md`), the Spec Kit skill workflow (`/speckit-specify` through `/speckit-converge`, `/speckit-orchestrate`, `/speckit-constitution`, `/speckit-bootstrap`), and cross-platform bootstrapping (`bootstrap-speckit.sh` and `bootstrap-speckit.ps1`).

---

### User Story 3 - Downstream Spec Kit Skill Documentation Gates (`plan`, `tasks`, `analyze`, `implement`, `converge`) (Priority: P3)

Developers and orchestrator subagents running `/speckit-plan`, `/speckit-tasks`, `/speckit-analyze`, `/speckit-implement`, and `/speckit-converge` need built-in quality gates that classify whether a feature has user-facing documentation impact (`USER_FACING` vs `INTERNAL_ONLY`), generate explicit documentation tasks when `USER_FACING`, and verify documentation coverage before completion.

**Why this priority**: Constitutional rules alone do not prevent documentation drift unless enforced by downstream workflow skills. Adding a structured **Documentation Impact** declaration in `plan-template.md` / `speckit-plan`, task generation rules in `tasks-template.md` / `speckit-tasks`, cross-artifact verification in `speckit-analyze`, and execution/convergence checks in `speckit-implement` and `speckit-converge` closes the loop without burdening internal-only refactors with unnecessary `README.md` edits.

**Independent Test**: Can be fully tested by inspecting `.specify/templates/{plan-template,tasks-template}.md` and `.agents/skills/speckit-{plan,tasks,analyze,implement,converge}/SKILL.md` to confirm that `USER_FACING` features require explicit documentation target files and tasks, `INTERNAL_ONLY` features require a brief rationale and are exempted from `README.md` churn, and `/speckit-analyze` flags missing documentation tasks on `USER_FACING` changes as a Constitution Alignment issue.

**Acceptance Scenarios**:

1. **Given** a feature specification being planned via `/speckit-plan`, **When** `plan.md` is generated from `plan-template.md`, **Then** the plan includes a **Documentation Impact** assessment under Constitution Check / Technical Context that classifies the feature as either `USER_FACING` (listing affected human-facing files such as `README.md` or user guides) or `INTERNAL_ONLY` (providing a concrete rationale why no user-visible commands, APIs, configuration options, or workflows are altered).
2. **Given** a `plan.md` or `spec.md` with `USER_FACING` documentation impact, **When** `/speckit-tasks` generates `tasks.md`, **Then** it includes one or more explicit tasks with exact file paths (e.g., `README.md` or `docs/...`) to author or update human-facing documentation alongside the implementation tasks.
3. **Given** `spec.md`, `plan.md`, and `tasks.md` evaluated by `/speckit-analyze`, **When** a feature introduces or modifies user-visible CLI commands, skills, APIs, configuration options, or behaviors without either a mapped human-facing documentation task in `tasks.md` or a valid `INTERNAL_ONLY` exemption in `plan.md`, **Then** `/speckit-analyze` flags a `CRITICAL` (Constitution Alignment) or `HIGH` (Coverage Gap) finding requiring remediation before implementation.
4. **Given** an active feature during `/speckit-implement` or `/speckit-converge`, **When** implementation and convergence checks run, **Then** they verify that all planned human-facing documentation updates in `README.md` or user guides accurately reflect the as-built behavior and contain no broken relative links or references to ephemeral `specs/NNN-*/` paths.

---

### Edge Cases

- **Internal-Only Changes vs. User-Facing Changes**: Purely internal changes (internal refactors, bug fixes that do not alter documented behavior, internal harness adjustments, or ephemeral spec updates) MUST NOT be forced to make artificial edits to `README.md`. Classifying `Documentation Impact: INTERNAL_ONLY` with a one-sentence justification in `plan.md` satisfies the gate without `README.md` churn.
- **No Ephemeral Spec References in Human-Facing Docs**: Per Constitutional Development Workflow & Quality Gates, human-facing documentation (`README.md`, user guides) MUST NOT cite transient `specs/NNN-*/` directories or `FR-XXX`/`SC-XXX` identifiers that will be deleted upon feature merge.
- **Template & Preset Parity**: Updating `.specify/templates/constitution-template.md` and `.specify/templates/coding-standards-template.md` without updating `.specify/presets/base-governance/templates/` would cause Tier 2 preset resolution to serve stale templates. Both locations MUST remain byte-identical, and `.specify/integrations/*.manifest.json` SHA-256 digests MUST be updated accordingly.
- **Legacy Repositories Without `[HUMAN_DOCS_CONVENTIONS]`**: When `/speckit-plan`, `/speckit-tasks`, or `/speckit-analyze` run in a repository whose `coding-standards.md` was ratified prior to Phase 6, the skills MUST fall back gracefully to the baseline Principle VII rule (or note that `/speckit-constitution` can be re-run) rather than crashing.
- **Strict Enforcement of Constitutional Principle III (No Automated Tests)**: No automated test files, unit test suites, or test tasks may be generated for Phase 6. All verification relies on static validation, markdown/link verification, placeholder/marker regex checks, and manifest digest synchronization.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: `.specify/templates/constitution-template.md` and `.specify/presets/base-governance/templates/constitution-template.md` MUST be updated identically to establish Human-Facing Documentation governance:
  - Expand Principle VII (*Code Hygiene, Ubiquitous Language & Safe Logging*) so its present-tense documentation rule explicitly covers **Human-Facing Documentation Synchronization**: any change that adds, removes, or modifies user-visible CLI commands, agent skills, public APIs, configuration options, or end-user workflows MUST update the corresponding human-facing documentation (`README.md`, quickstarts, or user guides) in the same change, whereas purely internal changes (`INTERNAL_ONLY` refactors, non-behavioral fixes, or internal tooling) are exempt from artificial `README.md` edits.
  - Introduce an optional enhancement module `MODULE-DOCS` (`<!-- OPTIONAL-MODULE: MODULE-DOCS ... -->` targeting Principle VII) that, when enabled, enforces a **Structured Human-Facing Documentation Gate** requiring `README.md` (and project user guides) to maintain canonical onboarding, architecture overview, usage/command reference, and configuration/troubleshooting sections verified at pre-PR time.
- **FR-002**: `.specify/templates/coding-standards-template.md` and `.specify/presets/base-governance/templates/coding-standards-template.md` MUST be updated identically to include a **Human-Facing Documentation & README Conventions** section (operationalizing Constitutional Principle VII) with a `[HUMAN_DOCS_CONVENTIONS]` placeholder slot and guidance examples covering different project archetypes (CLI tools, libraries/SDKs, web services, and agent/skill repositories).
- **FR-003**: `.agents/skills/speckit-constitution/SKILL.md` MUST be updated to support `MODULE-DOCS` (`ENABLED` or `OMITTED`) during module evaluation, structural transformation, `Sync Impact Report` generation, and pre-write validation, and to discover and substitute the `[HUMAN_DOCS_CONVENTIONS]` slot in `coding-standards.md` (updating total tracked slots from 25 to 26: 8 in `constitution.md`, 12 in `coding-standards.md`, 6 in `logging-standards.md`).
- **FR-004**: This repository's active governance suite in `.specify/memory/constitution.md` and `.specify/memory/coding-standards.md` MUST be formally amended to ratify the Phase 6 human-facing documentation standards:
  - Bump `.specify/memory/constitution.md` version from `2.0.0` to `2.1.0` (`Last Amended: 2026-11-05`), update the top HTML `Sync Impact Report` comment (including `MODULE-DOCS` status), incorporate the expanded Principle VII human-facing documentation rule, and include `README.md` in the Authority Hierarchy / Governance references where appropriate.
  - Update `.specify/memory/coding-standards.md` with the concrete **Human-Facing Documentation & README Conventions** section tailored to this Spec Kit repository.
- **FR-005**: A canonical, human-readable `README.md` MUST be created (or updated) at the repository root complying with Principle VII and `.specify/memory/coding-standards.md`, covering:
  - Repository purpose and Spec Kit customization architecture
  - Co-Applied Governance Suite overview (`.specify/memory/{constitution,coding-standards,logging-standards}.md` and 4-tier template resolution)
  - Complete reference of Spec Kit skills (`/speckit-specify`, `/speckit-clarify`, `/speckit-plan`, `/speckit-tasks`, `/speckit-checklist`, `/speckit-analyze`, `/speckit-implement`, `/speckit-converge`, `/speckit-constitution`, `/speckit-orchestrate`, `/speckit-bootstrap`)
  - Portable bootstrapping quickstart (`./bootstrap-speckit.sh` and `pwsh ./bootstrap-speckit.ps1`) and verification workflows.
- **FR-006**: `.specify/templates/plan-template.md` and `.agents/skills/speckit-plan/SKILL.md` MUST be updated so every implementation plan records a **Documentation Impact** classification (`USER_FACING` with target human-facing doc files such as `README.md`, or `INTERNAL_ONLY` with an explicit exemption rationale) and verifies alignment against Principle VII during the Constitution Check.
- **FR-007**: `.specify/templates/tasks-template.md` and `.agents/skills/speckit-tasks/SKILL.md` MUST be updated so that whenever a feature or user story has `USER_FACING` documentation impact, task generation produces explicit human-facing documentation tasks with concrete file paths (e.g., `README.md`, user guides) in the relevant User Story or Polish phase, while omitting redundant documentation tasks when classified as `INTERNAL_ONLY`.
- **FR-008**: `.agents/skills/speckit-analyze/SKILL.md`, `.agents/skills/speckit-implement/SKILL.md`, and `.agents/skills/speckit-converge/SKILL.md` MUST be updated to enforce human-facing documentation verification:
  - `speckit-analyze`: Verify that features/stories introducing user-visible changes either have mapped human-facing documentation tasks in `tasks.md` or an explicit `INTERNAL_ONLY` justification in `plan.md`, flagging violations under Constitution Alignment / Coverage Gaps.
  - `speckit-implement` & `speckit-converge`: Verify that required human-facing documentation updates are completed, match implemented behavior, and contain zero references to ephemeral `specs/NNN-*/` folders or `FR-XXX` identifiers.
- **FR-009**: All managed file SHA-256 digests in `.specify/integrations/{speckit,agy,speckit-bootstrap}.manifest.json` MUST be updated to reflect the modified templates and skills so `/speckit-bootstrap --check` reports a clean, drift-free bundle.

### Key Entities

- **Human-Facing Documentation Standard (Principle VII & `MODULE-DOCS`)**: The constitutional mandate distinguishing user-facing changes (which require same-change updates to `README.md` or user guides) from internal-only changes (which are exempt via explicit `INTERNAL_ONLY` classification), paired with optional `MODULE-DOCS` structural requirements.
- **Documentation Impact Classification (`USER_FACING` | `INTERNAL_ONLY`)**: The explicit planning metadata recorded in `plan.md` and checked by `speckit-tasks`, `speckit-analyze`, `speckit-implement`, and `speckit-converge` to determine whether human-facing documentation tasks are required.
- **Human-Facing Documentation Conventions (`[HUMAN_DOCS_CONVENTIONS]`)**: The companion `coding-standards-template.md` slot and section specifying project-specific documentation files (`README.md`, `docs/`), required headings, and formatting rules.
- **Repository Root `README.md`**: The primary human-facing onboarding and reference document for this repository, governed by Principle VII and verified against the implemented Spec Kit skill and bootstrapper suite.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% byte-for-byte parity is maintained between `.specify/templates/{constitution-template,coding-standards-template}.md` and `.specify/presets/base-governance/templates/{constitution-template,coding-standards-template}.md`, with 0 unresolved `[ALL_CAPS_IDENTIFIER]` placeholders or `OPTIONAL-MODULE` HTML comment tags remaining in ratified `.specify/memory/{constitution,coding-standards,logging-standards}.md`.
- **SC-002**: 100% of downstream delivery skills (`speckit-plan`, `speckit-tasks`, `speckit-analyze`, `speckit-implement`, `speckit-converge`) enforce the `USER_FACING` vs `INTERNAL_ONLY` documentation impact gate, ensuring user-visible changes cannot pass `/speckit-analyze` or `/speckit-converge` without corresponding documentation tasks and updates.
- **SC-003**: Purely internal changes classified as `INTERNAL_ONLY` with a valid rationale in `plan.md` require 0 artificial edits to `README.md` to pass `/speckit-analyze`.
- **SC-004**: The repository root `README.md` documents 100% of active Spec Kit skills and bootstrapper entry points (`bootstrap-speckit.sh`, `bootstrap-speckit.ps1`) with 0 broken relative file links and 0 references to transient `specs/NNN-*/` paths or `FR-XXX` identifiers.
- **SC-005**: 100% of modified managed files in `.specify/` and `.agents/` have synchronized SHA-256 digests in `.specify/integrations/{speckit,agy,speckit-bootstrap}.manifest.json`.

## Assumptions

- **Dual Placement (Principle VII Baseline + `MODULE-DOCS` + `coding-standards.md` Section)**: Universal policy (same-change human-facing doc synchronization for user-visible changes, internal-change exemption, and optional `MODULE-DOCS` strict structural gate) belongs in `constitution-template.md` under Principle VII, while stack- and archetype-specific file layout and section conventions belong in `coding-standards-template.md` under `[HUMAN_DOCS_CONVENTIONS]`. This preserves the exact separation of concerns established in Phases 1 and 2.
- **Explicit `USER_FACING` vs `INTERNAL_ONLY` Classification in `plan.md`**: Rather than relying on fragile filename heuristics to guess whether a change is user-facing, `plan.md` records an explicit `Documentation Impact: USER_FACING | INTERNAL_ONLY` field (with affected doc files or exemption rationale), which `speckit-tasks`, `speckit-analyze`, `speckit-implement`, and `speckit-converge` inspect deterministically.
- **Constitutional Version Bump (`2.0.0 -> 2.1.0`)**: Because Phase 6 adds an expanded normative clause and quality gate to Principle VII without removing or redefining existing principles in a backward-incompatible way, the constitutional amendment follows a `MINOR` semantic version bump (`2.0.0 -> 2.1.0`) per the Governance versioning rules.
