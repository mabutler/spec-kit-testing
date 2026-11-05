# Feature Specification: Co-Applied Governance & Constitutional Merge

**Feature Branch**: `002-co-applied-governance-merge`

**Created**: 2026-11-04

**Status**: Draft

**Input**: User description: "Phase 2"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Simultaneous Co-Application of All Three Governance Documents (Priority: P1)

Project maintainers and governance workflows need a unified command experience where creating or updating the project constitution simultaneously resolves, populates, and writes all three interdependent governance documents in `.specify/memory/`: `constitution.md`, `coding-standards.md`, and `logging-standards.md`.

**Why this priority**: The Base Constitution explicitly delegates language- and stack-specific idioms to `.specify/memory/coding-standards.md` and severity level taxonomy and telemetry configuration to `.specify/memory/logging-standards.md`. Generating or updating `constitution.md` in isolation leaves dangling cross-references and incomplete project governance.

**Independent Test**: Can be fully tested by invoking the constitution governance workflow in a repository with the Phase 1 templates installed and verifying that `.specify/memory/constitution.md`, `.specify/memory/coding-standards.md`, and `.specify/memory/logging-standards.md` are all generated or updated in a single execution with consistent project identity and zero unresolved `[ALL_CAPS_IDENTIFIER]` placeholders.

**Acceptance Scenarios**:

1. **Given** a repository with `constitution-template.md`, `coding-standards-template.md`, and `logging-standards-template.md` in `.specify/templates/`, **When** the constitution workflow is executed, **Then** it resolves all three templates and writes `.specify/memory/constitution.md`, `.specify/memory/coding-standards.md`, and `.specify/memory/logging-standards.md` in the same run.
2. **Given** the three governance templates containing 25 total `[ALL_CAPS_IDENTIFIER]` placeholder slots (8 in `constitution-template`, 11 in `coding-standards-template`, and 6 in `logging-standards-template`, with `[PROJECT_NAME]` shared across all three), **When** the governance workflow finishes, **Then** `[PROJECT_NAME]` is identical across all three generated files and every placeholder token is replaced with concrete project-specific values derived from user input or repository context.
3. **Given** user input to the constitution workflow that includes non-governance requests (such as feature code changes or refactors), **When** the workflow executes its Scope Guard, **Then** it modifies only `.specify/memory/{constitution,coding-standards,logging-standards}.md`, leaves template source files in `.specify/templates/` and application code untouched, and lists non-governance requests under `Next Actions`.

---

### User Story 2 - Intelligent Constitutional & Standards Merge with Optional Module Resolution (Priority: P2)

Engineering leads applying the base governance suite to an existing project—or amending an already-ratified governance suite—need an intelligent merge workflow that combines base non-negotiable principles, selectively enabled optional enhancement modules (`MODULE-A` through `MODULE-D` and optional `TRACE` logging), and project-specific conventions inferred from existing repository documentation, build/linter configurations, or prior `.specify/memory/` files without destructive overwrites.

**Why this priority**: Real-world projects already have established languages, build gates, directory layouts, or prior constitutional amendments and recorded deviations. A naive template overwrite would either erase existing project context or leave raw HTML module markers (`OPTIONAL-MODULE`, `DEFAULT-CLAUSE`) in the ratified governance files.

**Independent Test**: Can be fully tested by running the constitution workflow against a repository that already has an existing `.specify/memory/constitution.md` (and/or repository documentation and build manifests) with specific optional module selections, and verifying that prior valid customizations and `Recorded Deviations` are preserved, selected optional modules are cleanly integrated (including `MODULE-B` replacing the default Skip Allowlist clause when enabled), unselected optional modules and all template HTML marker comments are stripped, and any conflict with a Core Principle is surfaced for explicit resolution.

**Acceptance Scenarios**:

1. **Given** `constitution-template.md` with inline optional enhancement markers (`MODULE-A`, `MODULE-B`, `MODULE-C`, `MODULE-D`, and nested `MODULE-D-AOT-TRIM`), **When** the workflow evaluates optional modules (via explicit user selection, existing constitution state, or repository context inference), **Then** enabled `ADD` modules (`MODULE-A`, `MODULE-C`, `MODULE-D`) are retained inline within their target principles, disabled modules are completely removed, and all `<!-- OPTIONAL-MODULE ... -->`, `<!-- OPTIONAL-SUBCLAUSE ... -->`, and `<!-- DEFAULT-CLAUSE ... -->` HTML comment wrappers are stripped from `.specify/memory/constitution.md`.
2. **Given** `MODULE-B` (*Strict 100% Branch Coverage Profile*) is enabled during constitution generation or update, **When** Principle III is assembled, **Then** the `<!-- DEFAULT-CLAUSE: PLAN-JUSTIFICATION-AND-SKIP-ALLOWLIST ... -->` block is removed and replaced by `MODULE-B`'s *100% Branch Coverage Gate* clause so Principle III never contains contradictory coverage rules.
3. **Given** an existing `.specify/memory/constitution.md`, `.specify/memory/coding-standards.md`, or `.specify/memory/logging-standards.md` with previously ratified conventions or `Recorded Deviations`, **When** the governance workflow is re-run to amend or refresh governance, **Then** existing project-specific conventions, original `RATIFICATION_DATE`, and ratified `Recorded Deviations` are preserved, `LAST_AMENDED_DATE` and `CONSTITUTION_VERSION` are incremented per semantic versioning rules, and the top `Sync Impact Report` comment records the changes across principles, optional modules, and companion standards.
4. **Given** an existing repository convention or user instruction that directly conflicts with a non-negotiable Base Core Principle, **When** the merge workflow evaluates the conflict, **Then** it refuses to silently weaken the Core Principle and either aligns the lower-level convention with the Constitution or requires an explicit human-ratified entry under `## Recorded Deviations` containing all five mandatory fields: (1) Principle violated, (2) Ratifying human authority, (3) Rationale, (4) Compensating control, and (5) Known gap and documentation link.

---

### User Story 3 - Downstream Spec Kit Lifecycle Integration (Priority: P3)

Developers and automated agents running downstream Spec Kit workflows (`speckit-plan`, `speckit-tasks`, `speckit-analyze`, `speckit-implement`, and `speckit-converge`) need those workflows to automatically load and enforce `.specify/memory/coding-standards.md` and `.specify/memory/logging-standards.md` alongside `.specify/memory/constitution.md`.

**Why this priority**: Co-generating `coding-standards.md` and `logging-standards.md` only delivers full lifecycle value if downstream planning, task generation, cross-artifact consistency analysis, implementation, and convergence gates actively read and enforce them alongside the constitution.

**Independent Test**: Can be fully tested by inspecting the downstream workflow skill definitions (`speckit-plan`, `speckit-tasks`, `speckit-analyze`, `speckit-implement`, `speckit-converge`) and verifying that each workflow loads `.specify/memory/coding-standards.md` and `.specify/memory/logging-standards.md` (when present) and evaluates architectural, coding, and logging compliance against the complete three-document governance suite.

**Acceptance Scenarios**:

1. **Given** a repository with `.specify/memory/{constitution,coding-standards,logging-standards}.md`, **When** `speckit-plan` or `speckit-tasks` executes, **Then** the workflow loads all three governance documents to populate Technical Context, evaluate the Constitution & Governance Check gate, and inform task generation.
2. **Given** a repository with `.specify/memory/{constitution,coding-standards,logging-standards}.md`, **When** `speckit-analyze`, `speckit-implement`, or `speckit-converge` executes, **Then** the workflow loads all three governance documents and treats violations of `constitution.md` `MUST` rules (and linked normative rules in `coding-standards.md` and `logging-standards.md`) as governance alignment findings.
3. **Given** this repository (`spec-kit-testing`), **When** Phase 2 implementation completes, **Then** `.specify/memory/coding-standards.md` and `.specify/memory/logging-standards.md` are generated and co-applied alongside `.specify/memory/constitution.md` with zero unresolved placeholders.

---

### Edge Cases

- **First-Time Initialization vs. Iterative Amendment**: When `.specify/memory/coding-standards.md` or `.specify/memory/logging-standards.md` does not yet exist (for example, in a repository that previously only generated `constitution.md`), running the workflow initializes the missing companion files from their templates while merging any existing `constitution.md` non-destructively.
- **Mutually Exclusive Replacement Clause (`MODULE-B` vs. Default Skip Allowlist)**: If `MODULE-B` is not selected, the default *Plan Justification & Skip Allowlist* clause in Principle III is retained and its surrounding `DEFAULT-CLAUSE` HTML comments are stripped; if `MODULE-B` is selected, the default clause is stripped in its entirety and replaced by `MODULE-B`. Under no circumstances may both clauses or raw `OPTIONAL-MODULE` / `DEFAULT-CLAUSE` HTML comments remain in `.specify/memory/constitution.md`.
- **Nested Optional Sub-Clause (`MODULE-D-AOT-TRIM`)**: If `MODULE-D` is disabled, both `MODULE-D` and its inner `MODULE-D-AOT-TRIM` sub-clause are stripped. If `MODULE-D` is enabled, `MODULE-D-AOT-TRIM` is independently included or omitted (with its outer `[Optional: ...]` brackets and HTML comment markers cleaned up when included, or stripped entirely when omitted).
- **Optional `TRACE` Logging Alignment**: In `logging-standards.md`, `TRACE` is marked as optional in the template. During merge/co-application, the workflow records in the `[RETENTION_AND_SAMPLING_POLICY]` or project telemetry configuration whether mechanical `TRACE` entry/exit logging is enabled or disabled for the project.
- **Graceful Fallback When Companion Standards Are Absent**: If a downstream workflow (`plan`, `tasks`, `analyze`, `implement`, `converge`) runs in a legacy repository where only `.specify/memory/constitution.md` exists, it loads `constitution.md` and continues without crashing while noting if referenced companion files are missing.
- **Unresolvable Placeholder Values**: If a required placeholder value cannot be determined from user input or repository inspection (for example, an unknown original ratification date on a legacy repo), the workflow inserts an explicit `TODO(<FIELD_NAME>): explanation` marker and lists it in the `Sync Impact Report` and completion summary rather than leaving a silent `[ALL_CAPS_IDENTIFIER]` bracket token or inventing unverified facts.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The `speckit-constitution` workflow (`.agents/skills/speckit-constitution/SKILL.md`) MUST resolve all three governance templates (`constitution-template`, `coding-standards-template`, and `logging-standards-template`) and simultaneously generate or update `.specify/memory/constitution.md`, `.specify/memory/coding-standards.md`, and `.specify/memory/logging-standards.md`.
- **FR-002**: The `speckit-constitution` Scope Guard MUST permit creating and updating all three governance files in `.specify/memory/` (`constitution.md`, `coding-standards.md`, `logging-standards.md`) while strictly prohibiting modifications to template source files in `.specify/templates/`, application source code, tests, or unrelated repository files.
- **FR-003**: When resolving templates, the governance workflow MUST support both `.specify/scripts/bash/resolve-template.sh <template-name> --json` (when available) and direct platform-agnostic fallback resolution across the Spec Kit override/preset/extension/core template hierarchy (`.specify/templates/overrides/`, `.specify/presets/*/templates/`, `.specify/extensions/*/templates/`, `.specify/templates/`) so the workflow functions reliably across all operating systems.
- **FR-004**: The governance merge workflow MUST evaluate the four Optional Enhancement Modules in `constitution-template.md` (`MODULE-A`, `MODULE-B`, `MODULE-C`, `MODULE-D`, plus the nested `MODULE-D-AOT-TRIM` sub-clause) and the optional `TRACE` tier in `logging-standards-template.md` using the following precedence:
  1. Explicit user instructions or arguments passed to the command
  2. Previously ratified module selections in an existing `.specify/memory/constitution.md` (when updating an existing constitution without explicit module changes)
  3. Repository context inspection (e.g., regulated/reproducible build manifests, table-driven dispatch patterns, coverage gates, or `reference/open-questions.md` usage), defaulting optional modules to omitted when neither requested by the user nor evidenced by the repository.
- **FR-005**: The governance merge workflow MUST execute exact structural transformations for optional modules in `.specify/memory/constitution.md`:
  - For enabled `ADD` modules (`MODULE-A`, `MODULE-C`, `MODULE-D`), retain the module's normative text at its target principle and strip the surrounding `<!-- OPTIONAL-MODULE: ... -->` HTML comment markers.
  - For `MODULE-D-AOT-TRIM`, if included alongside `MODULE-D`, unwrap the `[Optional: ...]` brackets into normative text and strip `<!-- OPTIONAL-SUBCLAUSE: MODULE-D-AOT-TRIM ... -->` markers; if omitted, strip the entire sub-clause block.
  - For `MODULE-B` (`Action: REPLACE`, `Replaces: PLAN-JUSTIFICATION-AND-SKIP-ALLOWLIST`), if enabled, remove the entire `<!-- DEFAULT-CLAUSE: PLAN-JUSTIFICATION-AND-SKIP-ALLOWLIST ... -->` block in Principle III and replace it with `MODULE-B`'s normative text; if disabled, retain the default clause text and strip both the `DEFAULT-CLAUSE` HTML comments and the `MODULE-B` block.
  - Strip all remaining `OPTIONAL-MODULE`, `OPTIONAL-SUBCLAUSE`, and `DEFAULT-CLAUSE` HTML comment blocks so zero template conditional markers remain in `.specify/memory/constitution.md`.
- **FR-006**: The governance merge workflow MUST discover and populate all 25 standardized `[ALL_CAPS_IDENTIFIER]` placeholder tokens across the three templates (8 in `constitution.md`, 11 in `coding-standards.md`, 6 in `logging-standards.md`, with `[PROJECT_NAME]` synchronized across all three) by merging values in this priority order:
  1. Explicit user-provided inputs in the current session
  2. Existing project-specific values and amendments already ratified in `.specify/memory/{constitution,coding-standards,logging-standards}.md`
  3. Concrete evidence inspected from the repository (`README.md`, `Architecture.md`, `ROADMAP.md`, `CodingStandards.md`, `docs/logging.md`, package/build manifests, linter configs, and directory structure).
- **FR-007**: The governance merge workflow MUST enforce the Constitutional Authority Hierarchy and Conflict Resolution rules:
  - Base Core Principles I–VII in `constitution-template.md` are non-negotiable and MUST NOT be silently deleted, weakened, or contradicted by inferred repository conventions or companion standards.
  - If an existing repository practice or user input conflicts with a Core Principle, the workflow MUST flag the conflict explicitly and either (a) align `coding-standards.md` / `logging-standards.md` with the Constitution or (b) record an explicit human-ratified exception in `constitution.md` under `## Recorded Deviations` with all five mandatory elements: `(1) Principle violated`, `(2) Ratifying human authority`, `(3) Rationale`, `(4) Compensating control`, and `(5) Known gap and documentation link`.
- **FR-008**: The `Sync Impact Report` HTML comment at the top of `.specify/memory/constitution.md` MUST summarize the latest amendment across the entire governance suite, including:
  - `Version Change` (`old -> new` following `MAJOR.MINOR.PATCH` semantic versioning rules)
  - `Modified Principles`
  - `Modified Sections`
  - `Optional Modules` (explicitly listing which of Modules A–D are enabled or omitted)
  - `Companion Standards` (status of `.specify/memory/coding-standards.md` and `.specify/memory/logging-standards.md`: created, updated, or unchanged)
  - `Rationale` and any deferred `TODO(<FIELD_NAME>)` items.
- **FR-009**: Before writing the final files, the governance workflow MUST validate that:
  - Zero unresolved `[ALL_CAPS_IDENTIFIER]` tokens remain in `.specify/memory/{constitution,coding-standards,logging-standards}.md`
  - Zero `OPTIONAL-MODULE`, `OPTIONAL-SUBCLAUSE`, or `DEFAULT-CLAUSE` HTML comments remain in `.specify/memory/constitution.md`
  - Dates (`RATIFICATION_DATE`, `LAST_AMENDED_DATE`) follow ISO `YYYY-MM-DD` format and `CONSTITUTION_VERSION` matches the `Sync Impact Report`
  - All normative guidance uses clear declarative language (`MUST`, `MUST NOT`, `SHOULD`) without duplicating constitutional prose in `coding-standards.md`.
- **FR-010**: Downstream Spec Kit skills—specifically `speckit-plan`, `speckit-tasks`, `speckit-analyze`, `speckit-implement`, and `speckit-converge`—MUST be updated so that whenever they load `.specify/memory/constitution.md`, they also load `.specify/memory/coding-standards.md` and `.specify/memory/logging-standards.md` (if present) and enforce their stack-specific coding and observability conventions as part of governance alignment.
- **FR-011**: The co-applied governance workflow MUST be executed against this repository (`spec-kit-testing`) so that `.specify/memory/coding-standards.md` and `.specify/memory/logging-standards.md` are generated and synchronized with `.specify/memory/constitution.md`.

### Key Entities

- **Co-Applied Governance Suite**: The triad of linked governance files persisted in `.specify/memory/`: `constitution.md` (supreme authority), `coding-standards.md` (stack-specific coding conventions), and `logging-standards.md` (observability and severity standards).
- **Governance Merge Engine (Skill Workflow)**: The execution rules inside `speckit-constitution` that resolve the three base templates, evaluate optional enhancement modules (`MODULE-A`–`MODULE-D`), harvest repository context and prior `.specify/memory/` state, enforce constitutional precedence, and write the merged outputs.
- **Optional Module Resolution State**: The per-module activation decision (`ENABLED` vs. `OMITTED` for `MODULE-A`, `MODULE-B`, `MODULE-C`, `MODULE-D`, `MODULE-D-AOT-TRIM`, and optional `TRACE` logging) recorded in the `Sync Impact Report` and applied during template rendering.
- **Recorded Deviation Entry**: A structured five-part exception record in `constitution.md` required whenever a project ratifies a deviation from a Core Principle.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A single execution of `/speckit-constitution` generates or updates 100% of the 3 target governance files (`.specify/memory/constitution.md`, `.specify/memory/coding-standards.md`, `.specify/memory/logging-standards.md`) with 0 unresolved `[ALL_CAPS_IDENTIFIER]` placeholders and 0 leftover `OPTIONAL-MODULE`, `OPTIONAL-SUBCLAUSE`, or `DEFAULT-CLAUSE` HTML comment markers.
- **SC-002**: 100% of existing project-specific conventions, original ratification dates, and ratified `Recorded Deviations` in an existing `.specify/memory/` suite are preserved across iterative `/speckit-constitution` runs unless explicitly amended by the user.
- **SC-003**: 100% of the 5 downstream governance-aware Spec Kit skills (`speckit-plan`, `speckit-tasks`, `speckit-analyze`, `speckit-implement`, `speckit-converge`) explicitly load and reference `.specify/memory/coding-standards.md` and `.specify/memory/logging-standards.md` alongside `.specify/memory/constitution.md`.
- **SC-004**: In this repository (`spec-kit-testing`), all 3 governance files (`.specify/memory/constitution.md`, `.specify/memory/coding-standards.md`, `.specify/memory/logging-standards.md`) are present, mutually consistent, and pass placeholder and structural validation with 0 errors.

## Assumptions

- **Primary Output Location**: All three active governance documents are stored canonically in `.specify/memory/` (`constitution.md`, `coding-standards.md`, `logging-standards.md`), matching Spec Kit's `.specify/memory/` convention and the primary paths referenced in `constitution-template.md`. If a repository also maintains `CodingStandards.md` or `docs/logging.md`, those files serve as repository-context inputs during merge unless the user explicitly asks to mirror them.
- **Optional Module Selection Default**: When the user does not explicitly specify which optional modules (`MODULE-A`–`MODULE-D`) to enable, the workflow preserves any modules already active in an existing `.specify/memory/constitution.md`, or inspects repository context and defaults unrequested optional modules to omitted while reporting the module status in the `Sync Impact Report` and completion summary.
- **Conflict Resolution Precedence**: In accordance with `.specify/memory/constitution.md` (`Governance -> Document Hierarchy` and `Recorded Deviations`), Base Core Principles always take precedence over inferred repository practices. Conflicts cannot silently override a Core Principle; they require either updating the project convention or recording a human-ratified entry under `## Recorded Deviations`.
- **Scope Boundary Between Phase 2 and Phase 3**: Phase 2 updates `speckit-constitution` and the downstream skills (`plan`, `tasks`, `analyze`, `implement`, `converge`) to co-apply and enforce the three-document governance suite. Automated multi-agent pipeline orchestration across those skills is deferred to Phase 3 per `ROADMAP.md`.
