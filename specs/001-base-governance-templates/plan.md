# Implementation Plan: Base Governance Suite & Templates

**Branch**: `001-base-governance-templates` | **Date**: 2026-11-04 | **Spec**: [spec.md](file:///home/admin/projects/spec-kit-testing/specs/001-base-governance-templates/spec.md)

**Input**: Feature specification from `/specs/001-base-governance-templates/spec.md`

## Summary

This feature delivers a production-grade Base Governance Suite for Spec Kit by creating three canonical, platform-agnostic Markdown templates in `.specify/templates/`:
1. `constitution-template.md`: Replaces the default empty scaffold with the canonical Base Constitution v1.0.0, containing language-agnostic Core Principles I–VII (delegating logging severity level definitions to the logging standards document), inline structured HTML comment delimiters for Optional Enhancement Modules A–D (including Module B's default clause replacement and Module D's nested sub-clause), and footer placeholders `[CONSTITUTION_VERSION]`, `[RATIFICATION_DATE]`, and `[LAST_AMENDED_DATE]`.
2. `coding-standards-template.md`: A lean, stack-specific companion coding standards template that translates constitutional principles into concrete project- and language-specific convention sections with standardized `[ALL_CAPS_IDENTIFIER]` slots, without repeating constitutional prose or embedding optional module hooks.
3. `logging-standards-template.md`: A companion telemetry standards template incorporating the severity taxonomy (`CRITICAL`, `WARN`, `INFO`, `DEBUG`, and optional `TRACE`), ambient scope correlation, and sensitive data redaction rules.

All templates are pure static Markdown files with zero runtime script dependencies, no repository test suites (`tests/`) or test scripts (`scripts/`), usable across all operating systems (Windows, macOS, Linux), and integrate seamlessly with `.specify/scripts/bash/resolve-template.sh` at Priority 4 (Core templates) where Bash is available.

---

## Technical Context

**Language/Version**: Markdown (CommonMark / GitHub Flavored Markdown); Bash 4.x+ (optional Spec Kit CLI helper)

**Primary Dependencies**: None (zero runtime dependencies; platform-agnostic static markdown files). Optional: `.specify/scripts/bash/resolve-template.sh` in POSIX environments.

**Storage**: Flat markdown files located in `.specify/templates/`

**Testing**: Direct static file and markdown structure inspection (no standalone test suites in `tests/` or test scripts in `scripts/`).

**Target Platform**: Platform-agnostic (Linux, macOS, Windows)

**Project Type**: Governance template suite (static Markdown templates for Spec Kit)

**Performance Goals**: Instant static file read; sub-50ms template resolution latency when using `resolve-template.sh`

**Constraints**:
- Pure platform-agnostic Markdown files requiring zero script or shell dependencies.
- No standalone test suite (`tests/`) or helper test scripts (`scripts/`) in the repository root.
- Template names must strictly match `[a-z0-9-]+` for resolver compatibility (`constitution-template.md`, `coding-standards-template.md`, `logging-standards-template.md`).
- Customizable slots must strictly use `[ALL_CAPS_IDENTIFIER]` syntax.
- Optional Enhancement Modules A–D must use non-destructive, machine-parseable HTML comment delimiters exclusively in `constitution-template.md`.
- `constitution-template.md` must remain language-agnostic (free of C#/.NET-specific identifiers in normative rules) and delegate log severity definitions to the logging standards doc.
- `coding-standards-template.md` must be a lean project/language convention template that does not duplicate constitutional prose or include `OPEN-QUESTION` rules.
- `logging-standards-template.md` must mark `TRACE` and `TRACE Entry & Exit Rules` as optional.
- No modifications to existing bash scripts in `.specify/scripts/bash/`.

**Scale/Scope**: 3 markdown template files installed in `.specify/templates/` (zero files in `tests/` or `scripts/`).

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Principle 1 (Library-First / Modularity)**: PASS. Governance templates are modular, independent markdown assets that can be resolved and tailored standalone.
- **Principle 2 (CLI & Direct File Interface)**: PASS. Templates are directly inspectable as standard static Markdown on any OS and optionally resolvable via the CLI tool `.specify/scripts/bash/resolve-template.sh <template-name> [--json]`.
- **Principle 3 (Test-First & Verifiable Contracts)**: PASS. Delimiter grammar contracts defined in `contracts/` and runnable/inspectable validation scenarios specified in `quickstart.md` verify all functional requirements across platforms before implementation.
- **Principle 4 (Integration Testing & Consistency)**: PASS. Template resolution priority, placeholder discovery, delimiter grammar, and cross-platform verification scenarios are mutually reconciled.
- **Principle 5 (Observability & Simplicity)**: PASS. Pure Markdown templates; zero code overhead, zero unnecessary abstractions, deterministic static output.

### Post-Design Gate Evaluation
- **All Clarifications Resolved**: PASS. No unresolved `NEEDS CLARIFICATION` items remain; all decisions documented with rationale in `research.md`.
- **Artifact Alignment**: PASS. `data-model.md`, `contracts/`, and `quickstart.md` accurately reflect all requirements from `spec.md`.
- **Gate Status**: ALL GATES PASSED.

---

## Project Structure

### Documentation (this feature)

```text
specs/001-base-governance-templates/
├── plan.md              # This file (/speckit-plan command output)
├── research.md          # Phase 0 output: placement, delimiter, and template architecture decisions
├── data-model.md        # Phase 1 output: entities, relationships, attributes, and lifecycle
├── quickstart.md        # Phase 1 output: runnable validation scenarios
├── contracts/           # Phase 1 output: interface and schema contracts
│   ├── template-resolution-contract.md
│   ├── optional-module-delimiters.md
│   └── placeholder-tokens.md
└── tasks.md             # Phase 2 output (/speckit-tasks command - NOT created by /speckit-plan)
```

### Source Code (repository root)

```text
.specify/templates/
├── constitution-template.md       # Upgraded canonical Base Constitution v1.0.0 with Modules A-D
├── coding-standards-template.md   # New language-agnostic companion coding standards template
└── logging-standards-template.md  # New companion logging standards template (5-tier severity policy)
```

**Structure Decision**: Installed directly as core templates in `.specify/templates/`. This satisfies Priority 4 in `resolve_template_content` while allowing project-level overrides in `.specify/templates/overrides/` if individual repositories require local adjustments.

---

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

*No constitutional violations. Zero complexity exceptions.*
