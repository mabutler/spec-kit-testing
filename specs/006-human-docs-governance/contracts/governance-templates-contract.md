# Contract 1: Base Governance Templates & `/speckit-constitution` (`MODULE-DOCS` & `[HUMAN_DOCS_CONVENTIONS]`)

**Feature**: `006-human-docs-governance`  
**Covers**: `FR-001`, `FR-002`, `FR-003`, `SC-001`

---

## 1. `constitution-template.md` Contract

**Target Files (Must Be Byte-for-Byte Identical)**:
- `.specify/templates/constitution-template.md`
- `.specify/presets/base-governance/templates/constitution-template.md`

### 1.1 Principle VII Baseline & `MODULE-DOCS` Block Specification

In `### VII. Code Hygiene, Ubiquitous Language & Safe Logging`, bullet 3 (`- **Present-Tense, High-Signal Comments & Docs**:`) MUST be updated and `MODULE-DOCS` MUST be added after bullet 4 (`- **Structured, Safe Logging**:`) as follows:

```markdown
### VII. Code Hygiene, Ubiquitous Language & Safe Logging
- **Zero Warnings & Read-Only Vendored Code**: The build treats warnings as errors, and all code/scripts MUST pass configured linters. Vendored third-party code and generated schema files MUST NOT be edited or reformatted in place.
- **Ubiquitous Language**: Code identifiers, UI screens, CLI tools, and documentation share one domain vocabulary; changes MUST NOT introduce a synonym for an existing concept.
- **Present-Tense, High-Signal Comments & Docs**: Comments MUST explain the current implementation and *why* it is built that way—never narrate git or session history. Comments SHOULD document rejected alternatives only when needed to stop a developer from reintroducing a known defect via a naive refactor. Internal architectural documentation and human-facing documentation (`README.md`, quickstarts, and user guides) MUST match actual implemented behavior and be updated in the same change whenever user-visible CLI commands, agent skills, public APIs, configuration options, or end-user workflows are added, removed, or modified; purely internal changes (`INTERNAL_ONLY` refactors, non-behavioral fixes, or internal tooling) are exempt from artificial `README.md` edits.
- **Structured, Safe Logging**: Logs MUST use structured templates and strictly separate lifecycle milestones, diagnostic reasoning, recoverable boundary rejections, and fatal invariant crashes according to the severity taxonomy defined in `.specify/memory/logging-standards.md` / `docs/logging.md`. Logs and operator-visible errors MUST NEVER output secrets, private keys, credentials, raw PII, or bearer financial instruments.
<!-- OPTIONAL-MODULE: MODULE-DOCS
Action: ADD
Title: Structured Human-Facing Documentation Gate
Target: Principle VII
-->
- **Structured Human-Facing Documentation Gate**: The repository root `README.md` (and any dedicated user guide under `docs/`) MUST maintain canonical sections covering Project Overview & Architecture, Getting Started / Bootstrap Quickstart, CLI / Skill / API Usage Reference, and Configuration & Governance Verification, verified for relative link integrity and command accuracy before merge.
<!-- /OPTIONAL-MODULE: MODULE-DOCS -->
```

---

## 2. `coding-standards-template.md` Contract

**Target Files (Must Be Byte-for-Byte Identical)**:
- `.specify/templates/coding-standards-template.md`
- `.specify/presets/base-governance/templates/coding-standards-template.md`

### 2.1 `Human-Facing Documentation & README Conventions` Section Specification

Append the following section after `## Naming, Formatting & Code Style`:

```markdown
---

## Human-Facing Documentation & README Conventions

Operationalizes Constitutional Principle VII (*Code Hygiene, Ubiquitous Language & Safe Logging*):

- **Human-Facing Documentation & README Structure**: [HUMAN_DOCS_CONVENTIONS]
  <!-- Example (CLI / Agent / Skill Framework): Root README.md documents project overview, governance suite, CLI/skill reference, and quickstart commands; updated in the same PR for any USER_FACING change while INTERNAL_ONLY changes are exempt -->
  <!-- Example (Library / SDK / Web Service): Root README.md and docs/ maintain installation, public API/endpoint usage, configuration options, and migration notes without referencing ephemeral specs/NNN-*/ paths -->
```

---

## 3. `.agents/skills/speckit-constitution/SKILL.md` Contract

### 3.1 Optional Enhancement Module Evaluation (Step 2)
Include `MODULE-DOCS` in the module list:
- `MODULE-DOCS` (Structured Human-Facing Documentation Gate, Target: Principle VII)

### 3.2 Structural Transformations (Step 3)
Include `MODULE-DOCS` transformation rules:
- **`MODULE-DOCS`**:
  - If `ENABLED`: Strip opening `<!-- OPTIONAL-MODULE: MODULE-DOCS ... -->` and closing `<!-- /OPTIONAL-MODULE: MODULE-DOCS -->` comment lines; keep `- **Structured Human-Facing Documentation Gate**: ...` inline in Principle VII.
  - If `OMITTED`: Remove the entire block including opening tag, body text, and closing tag.

### 3.3 Placeholder Value Merge (Step 4)
Update total tracked `[ALL_CAPS_IDENTIFIER]` slots from **25** to **26**:
- **`constitution.md` (8 slots)**: `[PROJECT_NAME]`, `[PRIMARY_SOURCE]`, `[SECONDARY_SOURCE]`, `[TERTIARY_SOURCE]`, `[ACCEPTANCE_GATE_COMMANDS]`, `[CONSTITUTION_VERSION]`, `[RATIFICATION_DATE]`, `[LAST_AMENDED_DATE]`
- **`coding-standards.md` (12 slots)**: `[PROJECT_NAME]`, `[PRIMARY_LANGUAGE_AND_RUNTIME]`, `[BUILD_AND_LINTER_COMMANDS]`, `[DEPENDENCY_AND_LOCKFILE_CONVENTIONS]`, `[PROJECT_STRUCTURE_CONVENTIONS]`, `[BOUNDARY_ENFORCEMENT_MECHANISM]`, `[ERROR_RESULT_TYPES]`, `[DEFECT_INVARIANT_MECHANISM]`, `[IMMUTABLE_SNAPSHOT_AND_ID_CONVENTIONS]`, `[TEST_FRAMEWORK_CONVENTIONS]`, `[NAMING_CONVENTIONS]`, `[HUMAN_DOCS_CONVENTIONS]`
- **`logging-standards.md` (6 slots)**: `[PROJECT_NAME]`, `[LOGGING_FRAMEWORK]`, `[LOG_SINKS_AND_FORMATS]`, `[CORRELATION_ID_SCHEMA]`, `[SENSITIVE_DATA_REDACTION_MECHANISM]`, `[RETENTION_AND_SAMPLING_POLICY]`

### 3.4 Sync Impact Report Format (Step 6)
Update the `- Optional Modules:` line template in Step 6 to include `MODULE-DOCS: <ENABLED|OMITTED>`:
```markdown
- Optional Modules: MODULE-A: <ENABLED|OMITTED>, MODULE-B: <ENABLED|OMITTED>, MODULE-C: <ENABLED|OMITTED>, MODULE-D: <ENABLED|OMITTED> (MODULE-D-AOT-TRIM: <ENABLED|OMITTED>), MODULE-DOCS: <ENABLED|OMITTED>, TRACE Logging: <ENABLED|OMITTED>
```
