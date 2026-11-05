# Quickstart: Base Governance Suite & Templates Validation

**Feature**: `001-base-governance-templates`  
**Status**: Completed  
**Artifact**: `specs/001-base-governance-templates/quickstart.md`

## Overview

This guide provides runnable and inspectable validation scenarios to verify that all three governance templates (`constitution-template`, `coding-standards-template`, and `logging-standards-template`) are installed as platform-agnostic Markdown files in `.specify/templates/`, structurally complete, syntactically well-formed, and resolvable according to [Interface Contract: Template Resolution](contracts/template-resolution-contract.md), [Delimiters Contract](contracts/optional-module-delimiters.md), and [Data Model](data-model.md).

---

## Prerequisites

- **Universal / Cross-Platform**: Standard filesystem access to the repository (any OS: Linux, macOS, Windows). Optionally Python 3.8+ or standard text editors for direct file verification.
- **POSIX / Bash (Optional)**: Bash 4.0+, `grep`, `sed`, `awk` if running Spec Kit bash resolver utilities.

---

## Validation Scenarios

### Scenario 1: Verify Direct File Presence & Resolution

Validates that all three template files exist in `.specify/templates/` with non-zero size, and that they resolve cleanly.

#### 1A: Cross-Platform File Presence (Direct Filesystem Check)

```bash
# Verify file presence directly
test -s .specify/templates/constitution-template.md && echo "constitution-template: OK"
test -s .specify/templates/coding-standards-template.md && echo "coding-standards-template: OK"
test -s .specify/templates/logging-standards-template.md && echo "logging-standards-template: OK"
```

*Expected Outcome*: All three files report `OK`.

#### 1B: Spec Kit Bash CLI Resolution (POSIX / Optional)

Tests that all three templates resolve with exit code `0` in both raw text mode and JSON mode via `resolve-template.sh`.

```bash
# 1.1 Verify raw resolution of constitution-template
.specify/scripts/bash/resolve-template.sh constitution-template > /dev/null
echo "constitution-template raw status: $?"

# 1.2 Verify JSON resolution of constitution-template
.specify/scripts/bash/resolve-template.sh constitution-template --json | grep -q '"TEMPLATE_NAME":"constitution-template"'
echo "constitution-template JSON status: $?"

# 1.3 Verify raw resolution of coding-standards-template
.specify/scripts/bash/resolve-template.sh coding-standards-template > /dev/null
echo "coding-standards-template raw status: $?"

# 1.4 Verify JSON resolution of coding-standards-template
.specify/scripts/bash/resolve-template.sh coding-standards-template --json | grep -q '"TEMPLATE_NAME":"coding-standards-template"'
echo "coding-standards-template JSON status: $?"

# 1.5 Verify raw resolution of logging-standards-template
.specify/scripts/bash/resolve-template.sh logging-standards-template > /dev/null
echo "logging-standards-template raw status: $?"

# 1.6 Verify JSON resolution of logging-standards-template
.specify/scripts/bash/resolve-template.sh logging-standards-template --json | grep -q '"TEMPLATE_NAME":"logging-standards-template"'
echo "logging-standards-template JSON status: $?"
```

**Expected Outcome**: All status codes are `0`.

---

### Scenario 2: Validate Constitution Template Structure & Delimiters

Verifies that the canonical Base Constitution sections, 7 Core Principles, and Optional Enhancement Modules A–D with their delimiters are present in `constitution-template.md`.

```bash
CONTENT=$(.specify/scripts/bash/resolve-template.sh constitution-template)

# Check Core Principles I through VII
for p in \
  "I. Evidence Over Invention & Bounded Investigation" \
  "II. Two-Tier Failure Model & Fail Closed on Required State" \
  "III. Behavioral, Value-Driven Testing & Deterministic Execution" \
  "IV. Single Authoritative State, Enforced Boundaries & Safe Concurrency" \
  "V. Centralized Dependencies & Protected Toolchain Gate" \
  "VI. Bounded Resources & Verify-Before-Destroy" \
  "VII. Code Hygiene, Ubiquitous Language & Safe Logging"; do
    echo "$CONTENT" | grep -Fq "$p" || { echo "FAILED: Missing principle $p"; exit 1; }
done
echo "Core principles check: PASSED"

# Check Optional Modules delimiters
for marker in \
  "<!-- OPTIONAL-MODULE: MODULE-A" \
  "<!-- /OPTIONAL-MODULE: MODULE-A -->" \
  "<!-- DEFAULT-CLAUSE: PLAN-JUSTIFICATION-AND-SKIP-ALLOWLIST" \
  "<!-- /DEFAULT-CLAUSE: PLAN-JUSTIFICATION-AND-SKIP-ALLOWLIST -->" \
  "<!-- OPTIONAL-MODULE: MODULE-B" \
  "<!-- /OPTIONAL-MODULE: MODULE-B -->" \
  "<!-- OPTIONAL-MODULE: MODULE-C" \
  "<!-- /OPTIONAL-MODULE: MODULE-C -->" \
  "<!-- OPTIONAL-MODULE: MODULE-D" \
  "<!-- /OPTIONAL-MODULE: MODULE-D -->" \
  "<!-- OPTIONAL-SUBCLAUSE: MODULE-D-AOT-TRIM" \
  "<!-- /OPTIONAL-SUBCLAUSE: MODULE-D-AOT-TRIM -->"; do
    echo "$CONTENT" | grep -Fq "$marker" || { echo "FAILED: Missing delimiter $marker"; exit 1; }
done
echo "Optional module delimiters check: PASSED"
```

**Expected Outcome**: Both checks output `PASSED`.

---

### Scenario 3: Validate Coding Standards Structure & Slots

Verifies that `coding-standards-template` is a lean, stack-specific convention template containing the expected operational sections and project customization placeholders (without duplicating constitutional prose or `OPEN-QUESTION` rules).

```bash
CONTENT=$(.specify/scripts/bash/resolve-template.sh coding-standards-template)

# Check operational convention sections
for heading in \
  "Constitutional Authority & Precedence" \
  "Language, Runtime & Toolchain" \
  "Architecture, Module Layout & Compile-Time Boundaries" \
  "Error Handling & Failure Idioms" \
  "State, Concurrency & Identifier Idioms" \
  "Testing Framework & Conventions" \
  "Naming, Formatting & Code Style"; do
    echo "$CONTENT" | grep -Fq "$heading" || { echo "FAILED: Missing section $heading"; exit 1; }
done
echo "Coding standards sections check: PASSED"

# Check project placeholders
for token in \
  "[PROJECT_NAME]" \
  "[PRIMARY_LANGUAGE_AND_RUNTIME]" \
  "[BUILD_AND_LINTER_COMMANDS]" \
  "[DEPENDENCY_AND_LOCKFILE_CONVENTIONS]" \
  "[PROJECT_STRUCTURE_CONVENTIONS]" \
  "[BOUNDARY_ENFORCEMENT_MECHANISM]" \
  "[ERROR_RESULT_TYPES]" \
  "[DEFECT_INVARIANT_MECHANISM]" \
  "[IMMUTABLE_SNAPSHOT_AND_ID_CONVENTIONS]" \
  "[TEST_FRAMEWORK_CONVENTIONS]" \
  "[NAMING_CONVENTIONS]"; do
    echo "$CONTENT" | grep -Fq "$token" || { echo "FAILED: Missing placeholder $token"; exit 1; }
done
echo "Coding standards placeholders check: PASSED"
```

**Expected Outcome**: Both checks output `PASSED`.

---

### Scenario 4: Validate Logging Standards Severity & Observability Rules

Verifies that `logging-standards-template` incorporates the severity policy (with `TRACE` marked optional), ambient scope correlation, and redaction rules.

```bash
CONTENT=$(.specify/scripts/bash/resolve-template.sh logging-standards-template)

# Check 4 core severity levels + optional TRACE
for lvl in "CRITICAL" "WARN" "INFO" "DEBUG" "TRACE (Optional)"; do
    echo "$CONTENT" | grep -Fq "**${lvl}**" || { echo "FAILED: Missing log level $lvl"; exit 1; }
done
echo "Log levels check: PASSED"

# Check required observability policies
for policy in \
  "session_id" \
  "event_id" \
  "ToString" \
  "Passwords, tokens, secrets" \
  "sustained >100/sec"; do
    echo "$CONTENT" | grep -Fq "$policy" || { echo "FAILED: Missing policy term $policy"; exit 1; }
done
echo "Logging policies check: PASSED"

# Check project placeholders
for token in \
  "[PROJECT_NAME]" \
  "[LOGGING_FRAMEWORK]" \
  "[LOG_SINKS_AND_FORMATS]" \
  "[CORRELATION_ID_SCHEMA]" \
  "[SENSITIVE_DATA_REDACTION_MECHANISM]" \
  "[RETENTION_AND_SAMPLING_POLICY]"; do
    echo "$CONTENT" | grep -Fq "$token" || { echo "FAILED: Missing placeholder $token"; exit 1; }
done
echo "Logging standards placeholders check: PASSED"
```

**Expected Outcome**: All three checks output `PASSED`.

---

### Scenario 5: Validate All Placeholders Match Contract

Scans all three template files to verify that all bracketed tokens conform to `[ALL_CAPS_IDENTIFIER]`.

```bash
for tmpl in \
  .specify/templates/constitution-template.md \
  .specify/templates/coding-standards-template.md \
  .specify/templates/logging-standards-template.md; do
    echo "Checking placeholders in $tmpl..."
    # Find bracketed expressions that look like candidate placeholders
    grep -o '\[[A-Za-z0-9_ -]*\]' "$tmpl" | sort -u | while read -r token; do
        # Allowed formats: [ALL_CAPS_IDENTIFIER], [Optional: ...]
        case "$token" in
            \[[A-Z0-9_]*\]) ;;
            \[Optional:*\]) ;; # prose inline notation
            *) echo "WARNING / INVALID TOKEN: $token in $tmpl" ;;
        esac
    done
done
```

**Expected Outcome**: Zero invalid tokens reported.

---

## Template Installation & Placement

All three governance templates are installed directly in `.specify/templates/`:
- `.specify/templates/constitution-template.md`: Canonical Base Constitution v1.0.0 with language-agnostic Core Principles I–VII and inline Optional Modules A–D.
- `.specify/templates/coding-standards-template.md`: Lean companion coding standards template with project/language customization slots.
- `.specify/templates/logging-standards-template.md`: Companion logging and telemetry standards baseline with severity policy (optional `TRACE`) and redaction rules.

All files are platform-agnostic static Markdown assets with zero runtime script or shell dependencies, and no repository test suites (`tests/`) or test scripts (`scripts/`).

---

## Resolver Priority Behavior

When resolving templates via `.specify/scripts/bash/resolve-template.sh <template-name> [--json]`:

1. **Priority 1 (Project Overrides)**: `.specify/templates/overrides/<template-name>.md`
2. **Priority 2 (Installed Presets)**: `.specify/presets/<preset-id>/templates/<template-name>.md`
3. **Priority 3 (Extension Templates)**: `.specify/extensions/<extension-id>/templates/<template-name>.md`
4. **Priority 4 (Core Project Templates)**: `.specify/templates/<template-name>.md` (where these templates reside)

Installing the templates directly in `.specify/templates/` satisfies Priority 4, ensuring they are automatically discovered by Spec Kit workflows and CLI commands while remaining overridable via `.specify/templates/overrides/` if an individual project requires customized local variants.

---

## Phase 2 Merge Hooks & Downstream Consumption

In Phase 2 of the Governance Implementation Roadmap (`ROADMAP.md`):

1. **Constitutional Initialization (`/speckit-constitution`)**:
   - The `/speckit-constitution` skill will interactively query or ingest maintainer preferences regarding Optional Modules A–D in `constitution-template.md`.
   - For activated additive modules (Modules A, C, D), delimiters `<!-- OPTIONAL-MODULE: ... -->` and `<!-- /OPTIONAL-MODULE: ... -->` are stripped, keeping module body text.
   - For activated replacement module (Module B), the `DEFAULT-CLAUSE` block in Principle III is stripped, and Module B is activated in its place.
   - For omitted modules, the delimiter tags and enclosed body text are removed.
   - For Module D's nested sub-clause (`MODULE-D-AOT-TRIM`), it can be independently preserved or excluded.
2. **Target File Materialization**:
   - The ratified governance documents are rendered to `.specify/memory/constitution.md`, `.specify/memory/coding-standards.md`, and `.specify/memory/logging-standards.md`.
   - Projects may additionally symlink or mirror these into repository root docs (`CodingStandards.md` and `docs/logging.md`) as configured in the authority hierarchy.
3. **Validation Gate**:
   - Phase 2 initialization verifies that no unpopulated `[ALL_CAPS_IDENTIFIER]` placeholder tokens remain in ratified `.specify/memory/` files.

