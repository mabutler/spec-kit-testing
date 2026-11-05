# Research: Co-Applied Governance & Constitutional Merge

**Feature**: `002-co-applied-governance-merge`  
**Status**: Completed  
**Artifact**: `specs/002-co-applied-governance-merge/research.md`

## Overview

This research document consolidates architectural and design decisions for Phase 2 of the Spec Kit Governance Roadmap: upgrading the `speckit-constitution` workflow to simultaneously resolve, merge, and materialize all three interdependent governance documents (`.specify/memory/constitution.md`, `.specify/memory/coding-standards.md`, and `.specify/memory/logging-standards.md`), updating downstream Spec Kit skills (`speckit-plan`, `speckit-tasks`, `speckit-analyze`, `speckit-implement`, `speckit-converge`) to enforce the full three-document governance suite, and co-applying the governance suite to this repository (`spec-kit-testing`).

---

## Research Items

### 1. Simultaneous Co-Application vs. Separate Companion Skills

#### Context & Problem
In Phase 1 (`001-base-governance-templates`), three canonical governance templates were created in `.specify/templates/`:
- `constitution-template.md` (universal Core Principles I–VII + Optional Enhancement Modules A–D)
- `coding-standards-template.md` (stack-specific conventions operationalizing the Constitution)
- `logging-standards-template.md` (5-tier severity taxonomy, ambient correlation, redaction, and telemetry configuration)

However, `.agents/skills/speckit-constitution/SKILL.md` currently resolves only `constitution-template` and writes only `.specify/memory/constitution.md` (explicitly stating *"Write only `.specify/memory/constitution.md`"*). When `constitution.md` is generated alone, its explicit cross-references to `.specify/memory/coding-standards.md` and `.specify/memory/logging-standards.md` point to non-existent files.

#### Decision
Upgrade `.agents/skills/speckit-constitution/SKILL.md` directly so that a single invocation of `/speckit-constitution` resolves all three templates (`constitution-template`, `coding-standards-template`, `logging-standards-template`), executes the constitutional and companion standards merge, and writes all three files to `.specify/memory/`:
1. `.specify/memory/constitution.md`
2. `.specify/memory/coding-standards.md`
3. `.specify/memory/logging-standards.md`

Update the `Scope Guard` in `speckit-constitution/SKILL.md` to permit creating and updating all three files in `.specify/memory/` while retaining the strict prohibition against modifying `.specify/templates/`, application source code, tests, or unrelated repository files.

#### Rationale
- **Atomic Consistency**: Shared identity tokens (`[PROJECT_NAME]`), authority hierarchy definitions, optional module consequences (e.g., whether `TRACE` is enabled or how error result types map to Principle II), and the `Sync Impact Report` are guaranteed to stay in lockstep across all three documents.
- **Zero Extra User Friction**: Maintainers already know `/speckit-constitution` as the canonical governance command in Spec Kit.
- **No Hook Indirection Required**: Extending `speckit-constitution/SKILL.md` directly avoids fragile multi-command hook chaining while remaining compatible with `.specify/extensions.yml` pre/post hooks (`before_constitution`, `after_constitution`).

#### Alternatives Considered
- *Separate `/speckit-coding-standards` and `/speckit-logging-standards` skills*: Rejected because users would have to run three commands manually and risk out-of-sync governance states or dangling references.
- *External Python/Bash merge script invoked by the skill*: Rejected because Spec Kit agent skills operate as LLM-driven Markdown workflows across diverse OS environments (Windows, macOS, Linux) where external Python/YAML dependencies may not be installed.

---

### 2. Dual-Mode Template Resolution (CLI Resolver + Direct Filesystem Fallback)

#### Context & Problem
`.specify/scripts/bash/resolve-template.sh <template-name> --json` resolves a template across Spec Kit's 4-tier priority hierarchy:
1. `.specify/templates/overrides/<template-name>.md`
2. `.specify/presets/<preset-id>/templates/<template-name>.md` (respecting `.registry` priority and `preset.yml` strategies)
3. `.specify/extensions/<ext-id>/templates/<template-name>.md` (respecting `.registry` priority)
4. `.specify/templates/<template-name>.md` (core)

While `resolve-template.sh` is the primary mechanism in POSIX/Bash environments, the governance workflow must also work reliably in restricted or non-Bash environments.

#### Decision
Instruct `speckit-constitution` to:
1. Prefer running `.specify/scripts/bash/resolve-template.sh <template-name> --json` for each of `constitution-template`, `coding-standards-template`, and `logging-standards-template`.
2. If the shell script cannot be executed in the host environment (e.g., native Windows without Bash), fall back to direct file inspection across the exact 4-tier resolution order (`.specify/templates/overrides/<name>.md` → `.specify/presets/*/templates/<name>.md` → `.specify/extensions/*/templates/<name>.md` → `.specify/templates/<name>.md`).
3. If any of `coding-standards-template` or `logging-standards-template` is absent in a legacy repository that only has `constitution-template`, report a clear warning and gracefully process available templates rather than crashing.

#### Rationale
Honors Spec Kit's preset/override/extension composition engine whenever Bash is available while maintaining cross-platform resilience.

#### Alternatives Considered
- *Hard-coding `.specify/templates/<name>.md` only*: Rejected because it bypasses `.specify/templates/overrides/` and presets (`Phase 4`).
- *Failing hard when Bash is unavailable*: Rejected because Phase 1 established cross-platform static Markdown usability as a core constraint.

---

### 3. Optional Enhancement Module Resolution & Structural Transformation

#### Context & Problem
`constitution-template.md` contains four inline Optional Enhancement Modules (`MODULE-A`, `MODULE-B`, `MODULE-C`, `MODULE-D`), one replaceable default clause (`PLAN-JUSTIFICATION-AND-SKIP-ALLOWLIST`), and one nested sub-clause (`MODULE-D-AOT-TRIM`), plus `logging-standards-template.md` defines `TRACE (Optional)`. When generating or amending `.specify/memory/constitution.md`, raw HTML delimiter comments must never remain in the output file, and mutually exclusive clauses (`MODULE-B` vs. `PLAN-JUSTIFICATION-AND-SKIP-ALLOWLIST`) must never coexist.

#### Decision
Define a deterministic 3-tier precedence order and exact transformation rules in `speckit-constitution`:
1. **Precedence Order for Module Selection**:
   - **Priority 1 (Explicit User Input)**: Explicit instructions in `$ARGUMENTS` or conversation context (e.g., "enable Module B and Module C", "omit all optional modules", "enable TRACE logging").
   - **Priority 2 (Existing Ratified State)**: When updating an existing `.specify/memory/constitution.md` and the user does not request module changes, inspect the existing `Sync Impact Report` (`Optional Modules:` line) or principle text (presence of `Pointer-Only Code Tags`, `100% Branch Coverage Gate`, `Dispatch Is Data, Not Branches`, `Reproducible Builds & Deliberate Versioning`) to preserve previously ratified module selections.
   - **Priority 3 (Repository Context Inference & Safe Default)**: On first-time initialization without explicit module flags, inspect repository signals (e.g., `reference/open-questions.md` pointer usage for `MODULE-A`, strict 100% branch coverage gates for `MODULE-B`, command/protocol dispatch tables for `MODULE-C`, reproducible/certified build manifests for `MODULE-D`). Default any unrequested and unevidenced optional module to **OMITTED**.
2. **Transformation Rules**:
   - **Additive Modules (`MODULE-A`, `MODULE-C`, `MODULE-D`)**:
     - If `ENABLED`: Strip `<!-- OPTIONAL-MODULE: MODULE-X ... -->` and `<!-- /OPTIONAL-MODULE: MODULE-X -->` comments and retain the inner markdown bullet(s) inline in the target principle.
     - If `OMITTED`: Remove the opening comment, inner content, and closing comment completely.
   - **Nested Sub-Clause (`MODULE-D-AOT-TRIM`)**:
     - Evaluated only if `MODULE-D` is `ENABLED` (if `MODULE-D` is `OMITTED`, the entire `MODULE-D` block including `MODULE-D-AOT-TRIM` is removed).
     - If `MODULE-D-AOT-TRIM` is `ENABLED`: Strip `<!-- OPTIONAL-SUBCLAUSE: MODULE-D-AOT-TRIM ... -->` and `<!-- /OPTIONAL-SUBCLAUSE: MODULE-D-AOT-TRIM -->`, and unwrap `[Optional: Shared libraries ...]` to normative text: `Shared libraries consumed by constrained environments SHOULD be AOT/trim-safe, isolating any untrimmable code to the narrowest scope with documented justification.`
     - If `MODULE-D-AOT-TRIM` is `OMITTED`: Remove the `OPTIONAL-SUBCLAUSE` block and its inner text completely.
   - **Mutually Exclusive Replacement Module (`MODULE-B` vs. `PLAN-JUSTIFICATION-AND-SKIP-ALLOWLIST`)**:
     - If `MODULE-B` is `ENABLED`: Remove the entire `<!-- DEFAULT-CLAUSE: PLAN-JUSTIFICATION-AND-SKIP-ALLOWLIST ... -->` ... `<!-- /DEFAULT-CLAUSE: PLAN-JUSTIFICATION-AND-SKIP-ALLOWLIST -->` block (including its 5 allowlist items), and retain `MODULE-B`'s `- **100% Branch Coverage Gate**: ...` bullet with its `OPTIONAL-MODULE` comment wrappers stripped.
     - If `MODULE-B` is `OMITTED`: Strip `<!-- DEFAULT-CLAUSE: PLAN-JUSTIFICATION-AND-SKIP-ALLOWLIST ... -->` and `<!-- /DEFAULT-CLAUSE: PLAN-JUSTIFICATION-AND-SKIP-ALLOWLIST -->` comments while keeping the `- **Plan Justification & Skip Allowlist**:` bullet and its 5 numbered items, and remove the entire `MODULE-B` block.
   - **Optional `TRACE` Logging**:
     - Record in `logging-standards.md` under `[RETENTION_AND_SAMPLING_POLICY]` (or `Project Telemetry Configuration`) whether mechanical `TRACE` entry/exit logging is enabled or disabled for the repository.

#### Rationale
Guarantees 100% deterministic, conflict-free Markdown output in `.specify/memory/constitution.md` with zero leftover HTML conditional comments.

#### Alternatives Considered
- *Leaving HTML comments in `.specify/memory/constitution.md` for inactive modules*: Rejected by `FR-005`, `FR-009`, and `SC-001` because ratified governance documents in `.specify/memory/` must represent clean, unambiguous active policy.

---

### 4. Non-Destructive Merge Precedence & Conflict Resolution

#### Context & Problem
When applying or updating governance in a project with existing documentation (`README.md`, `Architecture.md`, `ROADMAP.md`, `CodingStandards.md`, `docs/logging.md`), build/linter manifests, or prior `.specify/memory/{constitution,coding-standards,logging-standards}.md` files, the workflow must harvest project-specific conventions without overwriting prior ratified customizations—while ensuring no inferred repository practice silently weakens a Core Principle.

#### Decision
Establish a strict 3-layer value resolution hierarchy and an explicit Conflict Resolution Gate:
1. **Value Resolution Priority for the 25 `[ALL_CAPS_IDENTIFIER]` Placeholders**:
   - **Layer 1**: Explicit user inputs in the current session (`$ARGUMENTS` or conversation).
   - **Layer 2**: Existing ratified values in `.specify/memory/{constitution,coding-standards,logging-standards}.md` (preserving `RATIFICATION_DATE`, `Recorded Deviations`, and project-specific conventions unless explicitly amended).
   - **Layer 3**: Repository evidence harvested from project docs (`README.md`, `Architecture.md`, `ROADMAP.md`, `CodingStandards.md`, `docs/logging.md`), build/package manifests (`package.json`, `Cargo.toml`, `pyproject.toml`, `*.sln`, `Directory.Packages.props`), linter configs, and scripts (`.specify/scripts/bash/`).
   - **Fallback**: If a value cannot be determined from Layers 1–3, insert `TODO(<FIELD_NAME>): explanation` and surface it in the `Sync Impact Report` and user summary (never invent unverified facts or leave raw `[ALL_CAPS_IDENTIFIER]` tokens).
2. **Constitutional Conflict Resolution Gate**:
   - Base Core Principles I–VII in `constitution.md` are non-negotiable.
   - If an inferred repository practice or user input contradicts a Core Principle (for example, silent `catch {}` blocks or unpinned dependencies), the merge workflow MUST NOT silently delete or weaken the Core Principle.
   - Instead, it MUST flag the conflict and either:
     - **(a)** Align `coding-standards.md` / `logging-standards.md` with the Core Principle (noting the repo remediation needed), OR
     - **(b)** Record an explicit human-ratified entry under `## Recorded Deviations` in `constitution.md` containing all 5 mandatory fields: `(1) Principle violated`, `(2) Ratifying human authority`, `(3) Rationale`, `(4) Compensating control`, and `(5) Known gap and documentation link`.

#### Rationale
Directly enforces Constitutional Principle I (*Evidence Over Invention*) and the Governance *Document Hierarchy* & *Precedence Order*.

#### Alternatives Considered
- *Allowing repo conventions to override template principles automatically*: Rejected because it violates the supreme authority of the Constitution and `FR-007`.

---

### 5. Downstream Spec Kit Skill Integration (`plan`, `tasks`, `analyze`, `implement`, `converge`)

#### Context & Problem
Currently, the five downstream skills only reference `.specify/memory/constitution.md`:
- `speckit-plan/SKILL.md` (Line 59): `Read FEATURE_SPEC and .specify/memory/constitution.md.`
- `speckit-tasks/SKILL.md` (Line 62): `IF EXISTS: Load .specify/memory/constitution.md for project principles and governance constraints`
- `speckit-analyze/SKILL.md` (Lines 63, 107, 138): References only `.specify/memory/constitution.md`
- `speckit-implement/SKILL.md` (Line 99): `IF EXISTS: Read .specify/memory/constitution.md for governance constraints`
- `speckit-converge/SKILL.md` (Lines 88, 102, 133): References only `.specify/memory/constitution.md`

#### Decision
Update all 5 downstream skill definitions in `.agents/skills/*/SKILL.md` to load and enforce the Co-Applied Governance Suite (`.specify/memory/constitution.md`, `.specify/memory/coding-standards.md`, and `.specify/memory/logging-standards.md`):
1. **`speckit-plan/SKILL.md`**:
   - In Step 2 (*Load context*), read `.specify/memory/constitution.md` and, if present, `.specify/memory/coding-standards.md` and `.specify/memory/logging-standards.md`.
   - Use `coding-standards.md` and `logging-standards.md` to inform `Technical Context` defaults (language/runtime, build/linter gates, testing conventions, logging framework) and evaluate the `Constitution Check` gate (including Principle III's mandatory test plan justification).
2. **`speckit-tasks/SKILL.md`**:
   - In Step 2 (*Load design documents*), load `.specify/memory/constitution.md`, `.specify/memory/coding-standards.md`, and `.specify/memory/logging-standards.md` (if present) so generated tasks respect module boundaries, error result types, test conventions, and structured logging rules.
3. **`speckit-analyze/SKILL.md`**:
   - Under `Operating Constraints -> Constitution Authority`, `Step 2 -> From constitution`, `Step 3 -> Build Semantic Models`, and `Step 4.D -> Constitution Alignment`, include `.specify/memory/coding-standards.md` and `.specify/memory/logging-standards.md` (if present) as linked companion governance documents under the Constitution's authority. Violations of `constitution.md` `MUST` principles or linked normative `MUST` rules in `coding-standards.md` / `logging-standards.md` are flagged as governance alignment findings.
4. **`speckit-implement/SKILL.md`**:
   - In Step 3 (*Load and analyze the implementation context*), load `.specify/memory/constitution.md`, `.specify/memory/coding-standards.md`, and `.specify/memory/logging-standards.md` (if present) and enforce their coding, error-handling, testing, and logging conventions during task execution and completion validation.
5. **`speckit-converge/SKILL.md`**:
   - Under `Operating Constraints -> Constitution Authority`, `Step 1 -> Initialize Convergence Context`, `Step 2 -> Load Artifacts`, and `Step 3 -> Build the Intent Inventory`, load `.specify/memory/coding-standards.md` and `.specify/memory/logging-standards.md` (if present) alongside `.specify/memory/constitution.md`, graceful-skipping any file that is absent or an unfilled template.

#### Rationale
Completes the full lifecycle feedback loop so that conventions co-applied during `/speckit-constitution` actively govern planning, task decomposition, consistency analysis, implementation, and convergence.

---

### 6. Repository Self-Application Values (`spec-kit-testing`)

#### Context & Problem
`FR-011` and `SC-004` require executing the co-applied governance workflow on `spec-kit-testing` itself so that `.specify/memory/constitution.md`, `.specify/memory/coding-standards.md`, and `.specify/memory/logging-standards.md` are all present, synchronized, and free of unresolved `[ALL_CAPS_IDENTIFIER]` placeholders. Currently, `.specify/memory/constitution.md` (v1.0.0, ratified 2026-11-04) exists, while `.specify/memory/coding-standards.md` and `.specify/memory/logging-standards.md` do not yet exist.

#### Findings from Repository Inspection
- **Project Identity**: `Spec Kit Testing` (from `.specify/memory/constitution.md` line 10: `# Spec Kit Testing Constitution`).
- **Existing Constitution State**:
  - `Version`: `1.0.0`, `Ratified`: `2026-11-04`, `Last Amended`: `2026-11-04`.
  - `Optional Modules`: None enabled (`all optional modules A–D omitted per project configuration`).
  - `Authority Hierarchy`:
    1. **Feature Specifications & Acceptance Requirements** (Ratified documents in `specs/`)
    2. **Architecture & Design Documentation** (`Architecture.md`, `README.md`, `ROADMAP.md`)
    3. **Existing Implementation & Automated Test Suite** (Source code, skill definitions in `.agents/skills/`, and scripts in `.specify/scripts/`)
  - `Acceptance Gate Commands`: `.specify/scripts/bash/resolve-template.sh constitution-template --json && .specify/scripts/bash/resolve-template.sh coding-standards-template --json && .specify/scripts/bash/resolve-template.sh logging-standards-template --json && .specify/scripts/bash/check-prerequisites.sh --json --paths-only`
- **Coding Standards Values Derived from Repository**:
  - `[PRIMARY_LANGUAGE_AND_RUNTIME]`: CommonMark / GitHub Flavored Markdown (Agent Skills & Governance Artifacts) and POSIX / Bash 4.0+ (`.specify/scripts/bash/*.sh` CLI utilities with optional `jq` / Python 3.8+ JSON/YAML parsers).
  - `[BUILD_AND_LINTER_COMMANDS]`: `bash -n .specify/scripts/bash/*.sh` (syntax check with zero warnings/errors) and markdown placeholder/delimiter verification gates via `.specify/scripts/bash/resolve-template.sh`.
  - `[DEPENDENCY_AND_LOCKFILE_CONVENTIONS]`: Zero external runtime package dependencies; Spec Kit integration file hashes and versions are centrally pinned in `.specify/integrations/*.manifest.json` (`speckit.manifest.json`, `agy.manifest.json`) and `.specify/integration.json`.
  - `[PROJECT_STRUCTURE_CONVENTIONS]`: `.specify/templates/` (core governance and artifact templates), `.specify/memory/` (ratified project governance suite), `.specify/scripts/bash/` (shared CLI and template resolution scripts), `.agents/skills/speckit-*/SKILL.md` (agent workflow skill definitions), and `specs/NNN-*/` (ephemeral feature specifications, plans, contracts, and tasks).
  - `[BOUNDARY_ENFORCEMENT_MECHANISM]`: Strict separation between read-only base templates (`.specify/templates/`), active ratified project memory (`.specify/memory/`), shell resolution infrastructure (`.specify/scripts/bash/`), and declarative agent skill prompts (`.agents/skills/`). Skills invoke bash scripts strictly via CLI JSON contracts (`--json`) and never mutate `.specify/templates/` during governance or feature execution.
  - `[ERROR_RESULT_TYPES]`: Non-zero POSIX exit codes (`1` for missing target/validation rejection, `2` for invalid registry/manifest configuration) paired with structured `ERROR: <message>` diagnostics on `stderr` and structured JSON payloads on `stdout` for script boundaries; explicit `ERROR` / `STOP` gate reports in agent skill workflows.
  - `[DEFECT_INVARIANT_MECHANISM]`: `set -e` / explicit non-zero `exit` traps in Bash scripts and immediate workflow halt (`STOP` / `CRITICAL` gate abort) in Spec Kit skills when required files, templates, or constitutional preconditions are violated.
  - `[IMMUTABLE_SNAPSHOT_AND_ID_CONVENTIONS]`: Feature context is resolved into immutable per-invocation environment variables (`REPO_ROOT`, `FEATURE_DIR`, `FEATURE_SPEC`, `IMPL_PLAN`, `TASKS`) via `get_feature_paths`; distinct artifact identifiers (`FR-XXX`, `SC-XXX`, `TXXX`, `MODULE-X`) use non-overlapping prefixes.
  - `[TEST_FRAMEWORK_CONVENTIONS]`: Deterministic, unprivileged CLI and static artifact verification suites documented in each feature's `quickstart.md` (verifying exit codes, JSON output schemas, placeholder substitution, and HTML delimiter stripping without touching external networks or privileged OS resources).
  - `[NAMING_CONVENTIONS]`: `kebab-case` for template names (`[a-z0-9-]+`), skill directories (`speckit-<command>`), and bash scripts (`*.sh`); `UPPER_SNAKE_CASE` for `[ALL_CAPS_IDENTIFIER]` template placeholders and exported shell/JSON keys (`FEATURE_DIR`, `TEMPLATE_CONTENT`); `camelCase` or `snake_case` for local bash functions and variables per `common.sh`.
- **Logging Standards Values Derived from Repository**:
  - `[LOGGING_FRAMEWORK]`: Structured CLI diagnostic output (`stdout` for structured JSON/result payloads, `stderr` for `ERROR:` / `WARN:` diagnostics) in `.specify/scripts/bash/*.sh`, and structured Markdown governance/execution reports (`Sync Impact Report`, `Specification Analysis Report`, `Convergence Findings`) in `.agents/skills/`.
  - `[LOG_SINKS_AND_FORMATS]`: Standard streams (`stdout` compact JSON via `jq -cn` or `printf` JSON escaping; `stderr` structured prefix lines) and persisted Markdown audit blocks (`Sync Impact Report` HTML comment in `.specify/memory/constitution.md`).
  - `[CORRELATION_ID_SCHEMA]`: Ambient execution context propagated via environment and `.specify/feature.json` (`SPECIFY_FEATURE`, `SPECIFY_FEATURE_DIRECTORY`, `BRANCH` / feature slug `NNN-feature-name`), read automatically by `common.sh:get_feature_paths` without passing feature paths manually across every call site.
  - `[SENSITIVE_DATA_REDACTION_MECHANISM]`: Strict exclusion of secrets, tokens, credentials, and private keys from all repository templates, `.specify/memory/` files, skill outputs, and shell script diagnostics; `common.sh` uses safe quoting (`printf '%q'` and `json_escape`) and never echoes environment secrets.
  - `[RETENTION_AND_SAMPLING_POLICY]`: Only the latest amendment summary is retained in the `Sync Impact Report` header of `.specify/memory/constitution.md` (do not accumulate historical logs); ephemeral feature specs (`specs/NNN-*/`) are transient proposals deleted upon final PR promotion per Development Workflow gates; mechanical `TRACE` function-level logging is **disabled** (`OMITTED`) by default for this repository.

#### Decision
Use these concrete, repository-evidenced values when co-applying `.specify/memory/constitution.md`, `.specify/memory/coding-standards.md`, and `.specify/memory/logging-standards.md` in `spec-kit-testing`, updating `constitution.md` to include the new `Sync Impact Report` fields (`Optional Modules` and `Companion Standards`) while preserving its `1.0.0` core principles and `2026-11-04` ratification date.
