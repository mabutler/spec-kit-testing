# Research: Base Governance Suite & Templates

**Feature**: `001-base-governance-templates`  
**Status**: Completed  
**Artifact**: `specs/001-base-governance-templates/research.md`

## Overview

This research document consolidates architectural and design decisions for creating the production-grade Base Governance Suite: `constitution-template.md`, `coding-standards-template.md`, and `logging-standards-template.md`. All decisions adhere to the existing template resolution engine in `.specify/scripts/bash/resolve-template.sh` and prepare clean machine- and human-usable hooks for Phase 2 automated constitutional merging.

---

## Research Items

### 1. Template Placement and Resolution Engine Compatibility

#### Context & Problem
The governance templates must resolve out of the box when requested via `.specify/scripts/bash/resolve-template.sh <template-name> [--json]`. We need to determine the optimal file system location in `.specify/` without modifying the core bash resolver or breaking existing resolution priority.

#### Findings
Inspection of `.specify/scripts/bash/common.sh` (`resolve_template_content`) reveals the 4-tier resolution hierarchy:
1. **Priority 1 (Project Overrides)**: `$REPO_ROOT/.specify/templates/overrides/${template_name}.md` (always `replace` strategy).
2. **Priority 2 (Installed Presets)**: `$REPO_ROOT/.specify/presets/<preset-id>/...` (respects `preset.yml` strategies: `replace`, `prepend`, `append`, `wrap`).
3. **Priority 3 (Extension-provided)**: `$REPO_ROOT/.specify/extensions/<extension-id>/...`
4. **Priority 4 (Core Base Templates)**: `$REPO_ROOT/.specify/templates/${template_name}.md` (always `replace` strategy).

Template names are validated by the shell pattern: `case "$template_name" in ""|*[!a-z0-9-]*) return 1 ;; esac`.
The existing `.specify/templates/constitution-template.md` is an initial 50-line empty scaffold at Priority 4.

#### Decision
Place all three templates as core base templates directly in `.specify/templates/`:
- `.specify/templates/constitution-template.md` (replaces the existing minimal scaffold)
- `.specify/templates/coding-standards-template.md`
- `.specify/templates/logging-standards-template.md`

#### Rationale
- Storing them in `.specify/templates/` establishes them as the repository's default core governance baseline (Priority 4), allowing presets or project overrides (`.specify/templates/overrides/`) to selectively customize them if desired.
- Template identifiers `constitution-template`, `coding-standards-template`, and `logging-standards-template` strictly conform to `[a-z0-9-]+` and resolve without any script modifications.
- Existing tests and CLI calls invoking `resolve-template.sh constitution-template` immediately receive the new production-grade base template.

#### Alternatives Considered
- *Placing in `.specify/templates/overrides/`*: Rejected because overrides represent project-specific deviations over base templates. These three files constitute the base templates for any Spec Kit project.
- *Placing in `.specify/presets/base-governance/`*: Rejected for Phase 1 as it introduces preset metadata overhead (`preset.yml`, `.registry`) without necessity; base templates in `.specify/templates/` serve all projects directly.

---

### 2. Optional Enhancement Module Delimiters & Replacement Syntax

#### Context & Problem
`constitution-template.md` must embed Optional Enhancement Modules A through D inline within their target principles:
- **Module A** (In-Code Open Question Pointers) → Added to Principle I
- **Module B** (Strict 100% Branch Coverage Profile) → Replaces the default "Plan Justification & Skip Allowlist" in Principle III
- **Module C** (Table-Driven Dispatch) → Added to Principle IV
- **Module D** (Regulated / Certified Systems) → Added to Principle V, with a nested sub-clause regarding AOT/trim-safe libraries.

The markup must:
1. Render as valid, clean Markdown for human readers when viewed in GitHub or documentation viewers.
2. Be unambiguously parseable by regular expressions and string matching in Phase 2 automated workflows.
3. Unambiguously distinguish additive modules (`ADD`) from replacement modules (`REPLACE`).
4. Pinpoint the exact default text replaced by Module B so that activating Module B removes the replaced text without leaving duplicate or contradictory guidance.
5. Provide a cleanly isolated nested toggle for Module D's inner sub-clause.

#### Findings
Standard HTML comment blocks (`<!-- ... -->`) are ignored by Markdown renderers but fully retained in raw file content and accessible to shell/Python/tooling scripts. Using structured key-value headers within the HTML comments creates an explicit, robust protocol.

#### Decision
Use standardized structured HTML comment delimiters:

**For Additive Modules (A, C, D):**
```markdown
<!-- OPTIONAL-MODULE: MODULE-A
Action: ADD
Title: In-Code Open Question Pointers
Target: Principle I
-->
- **Pointer-Only Code Tags:** ...
<!-- /OPTIONAL-MODULE: MODULE-A -->
```

**For Replaceable Default Clause & Replacement Module (Module B):**
```markdown
<!-- DEFAULT-CLAUSE: PLAN-JUSTIFICATION-AND-SKIP-ALLOWLIST (REPLACEABLE-BY: MODULE-B)
Target: Principle III
-->
- **Plan Justification & Skip Allowlist**: ...
<!-- /DEFAULT-CLAUSE: PLAN-JUSTIFICATION-AND-SKIP-ALLOWLIST -->

<!-- OPTIONAL-MODULE: MODULE-B
Action: REPLACE
Target: Principle III
Replaces: PLAN-JUSTIFICATION-AND-SKIP-ALLOWLIST
Title: Strict 100% Branch Coverage Profile
-->
- **100% Branch Coverage Gate:** ...
<!-- /OPTIONAL-MODULE: MODULE-B -->
```

**For Nested Sub-Clause (in Module D):**
```markdown
<!-- OPTIONAL-SUBCLAUSE: MODULE-D-AOT-TRIM
Action: OPTIONAL-INCLUSION
Parent-Module: MODULE-D
Title: AOT / Trim-Safe Shared Libraries
-->
[Optional: Shared libraries consumed by constrained environments SHOULD be AOT/trim-safe, isolating any untrimmable code to the narrowest scope with documented justification.]
<!-- /OPTIONAL-SUBCLAUSE: MODULE-D-AOT-TRIM -->
```

#### Rationale
- Completely non-disruptive to human readers viewing rendered Markdown.
- High signal-to-noise ratio: unambiguous opening tags (`OPTIONAL-MODULE: MODULE-X`) and matching closing tags (`/OPTIONAL-MODULE: MODULE-X`).
- Explicit `Action: ADD` vs `Action: REPLACE` paired with `DEFAULT-CLAUSE` guarantees that automated tooling in Phase 2 can perform zero-ambiguity string replacements without AST parsing.

#### Alternatives Considered
- *Grouping optional modules at the end of the template (Catalog style)*: Clarified with user in session 2026-11-04 and explicitly rejected in favor of inline placement within target principles.
- *Custom Markdown directives (e.g. `:::optional`)*: Rejected because they break standard CommonMark rendering on platforms like GitHub and Azure DevOps unless custom preprocessors are used.

---

### 3. Companion Standards Templates Architecture

#### Context & Problem
Principles I–VII establish non-negotiable architectural, failure, testing, state, supply-chain, resource, and hygiene principles. The Constitution explicitly delegates day-to-day coding practices to `coding-standards-template.md` and telemetry/observability practices to `logging-standards-template.md`.

#### Findings
1. **Coding Standards Template**:
   - Must be language-agnostic while reflecting modern type-safe, contract-driven systems engineering.
   - Must translate the 7 constitutional principles into concrete development rules: compile-time boundary enforcement, two-tier error handling (result types vs defect invariant crashes), snapshot isolation & concurrency lock safety, type-safe ID wrappers (`readonly record struct` style), bounded untrusted inputs, verify-before-destroy, and hostile-boundary unit testing.
   - Must provide customizable slots for language/runtime, build/linter tooling, naming conventions, and test runners, with exemplary guidance provided via comments.

2. **Logging Standards Template**:
   - Must incorporate the user-provided Software Logging Policy:
     - 5-Tier Severity Taxonomy (`CRITICAL`, `WARN`, `INFO`, `DEBUG`, `TRACE`) mapped directly to the Two-Tier Failure Model.
     - `CRITICAL`: System restarting; requires restart reason and exception.
     - `WARN`: Boundary rejection or recoverable failure worth monitoring; never hidden in `DEBUG`.
     - `INFO`: Business/lifecycle outcome reading like an audit trail. Log both attempt and result for significant operations. Infrequent startup/shutdown in verbose layers logs at `INFO`.
     - `DEBUG`: Engineer's working notes and diagnostic reasoning; never leaks into `INFO`.
     - `TRACE`: Mechanical entry/exit on every function and return path. Complex objects use `ToString()` or dedicated cheap property helpers. External library calls do not emit `TRACE`.
     - Ambient scope correlation: tokens (`session_id`, `event_id`) read automatically from execution context, never passed as parameters or logged at call sites.
     - Prohibited sensitive data: Passwords, tokens, API keys, full credit cards, SSNs, government IDs, raw PII strictly forbidden; internal IDs (GUIDs, usernames) permitted.
     - Performance: Guard expensive log arguments; high-frequency events (>100/sec) sampled/aggregated.
     - Testing rule: Unit tests MUST NOT assert on log message text.
   - Must provide customizable slots for logging framework, sinks, redaction mechanism, and retention policy.

#### Decision
Structure both companion templates to begin with an explicit Constitutional Authority Header affirming that the Constitution has ultimate precedence, followed by universal non-negotiable rules, and concluded with clearly marked project-specific customization sections.

#### Rationale
Maintains a single source of truth: the constitution remains sovereign, while companion documents provide operational clarity without creating competing rules.

---

### 4. Placeholder Token Standardization

#### Context & Problem
Customizable slots must be easily recognized by humans and detectable by validation scripts or Phase 2 agent workflows.

#### Findings
Inconsistent placeholders (e.g., `<PROJECT_NAME>`, `{project_name}`, `TODO: name`, `[PROJECT_NAME]`) cause regex failures and leave un-substituted markers in initialized projects.

#### Decision
All customizable slots across all three templates MUST use the strict format:
- `[ALL_CAPS_IDENTIFIER]` (e.g., `[PROJECT_NAME]`, `[PRIMARY_LANGUAGE_AND_RUNTIME]`, `[LOGGING_FRAMEWORK]`)
- Dates use `[YYYY-MM-DD]`
- Version numbers use `[CONSTITUTION_VERSION]` with `1.0.0` as the canonical base default.

A comprehensive inventory of placeholders will be documented in `contracts/placeholder-tokens.md` and validated in `quickstart.md`.

---

### 5. Cross-Platform Static Templates with Zero Script Dependencies

#### Context & Problem
Governance templates must be usable across diverse developer operating systems (Windows, macOS, Linux) without requiring POSIX shell runtimes, Bash 4+, or auxiliary script tooling. We must establish how templates are stored, consumed, and verified without making script execution a prerequisite.

#### Findings
- Spec Kit workflows and agent environments can run on native Windows environments (PowerShell / cmd / VS Code) where Bash is not installed or requires WSL/Git Bash.
- Markdown files stored in `.specify/templates/` are plain static text. They require no build step, compilation, or script execution to be consumed or inspected.
- Automated tests or verification steps can be expressed as direct file and markdown structure inspection (checking for section headings, comment delimiters, and token patterns) using any available runtime (Python, Node.js, PowerShell, or POSIX shell), or via manual/editor inspection.

#### Decision
Treat all three governance templates as pure, platform-agnostic static Markdown files in `.specify/templates/` with zero runtime script dependencies. Eliminate all mandatory Bash/POSIX runtime prerequisites for template consumption, and provide validation scenarios in `quickstart.md` that can be verified either via direct static file inspection or optionally via the Spec Kit Bash resolver where available.

#### Rationale
Guarantees maximum portability, zero deployment friction, and universal editor/tooling compatibility across all operating systems.

#### Alternatives Considered
- *Requiring a Node.js or Python CLI runner*: Rejected as an unnecessary dependency; Markdown templates do not require a runtime layer.
- *Requiring Bash scripts for all operations*: Rejected per user clarification in session 2026-11-04.
