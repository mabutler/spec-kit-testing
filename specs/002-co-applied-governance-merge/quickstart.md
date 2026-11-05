# Quickstart: Co-Applied Governance & Constitutional Merge Validation

**Feature**: `002-co-applied-governance-merge`  
**Status**: Completed  
**Artifact**: `specs/002-co-applied-governance-merge/quickstart.md`

## Overview

This guide provides runnable validation scenarios to verify end-to-end compliance with the [Co-Applied Governance Merge Contract](contracts/co-applied-governance-merge-contract.md), [Downstream Skill Governance Contract](contracts/downstream-skill-governance-contract.md), and [Data Model](data-model.md).

---

## Prerequisites

- **Filesystem Access**: Repository root (`/home/admin/projects/spec-kit-testing`) with Phase 1 governance templates installed in `.specify/templates/`.
- **Optional CLI Tools**: `bash` 4.0+, `grep`, `awk` for running automated verification commands.

---

## Validation Scenarios

### Scenario 1: Verify Co-Applied Governance Suite in `.specify/memory/` (US1 / SC-001 / SC-004)

Validates that all three governance documents exist in `.specify/memory/`, have non-zero size, share an identical project name in their H1 titles, and have an updated `Sync Impact Report` in `.specify/memory/constitution.md`.

```bash
# 1.1 Verify all three ratified governance documents exist and are non-empty
for doc in \
  .specify/memory/constitution.md \
  .specify/memory/coding-standards.md \
  .specify/memory/logging-standards.md; do
    test -s "$doc" && echo "$doc: PRESENT" || { echo "FAILED: Missing or empty $doc"; exit 1; }
done

# 1.2 Verify synchronized project identity across all three H1 titles
P_CONST=$(grep -m1 '^# ' .specify/memory/constitution.md | sed 's/^# \(.*\) Constitution$/\1/')
P_CODE=$(grep -m1 '^# ' .specify/memory/coding-standards.md | sed 's/^# \(.*\) Coding Standards$/\1/')
P_LOG=$(grep -m1 '^# ' .specify/memory/logging-standards.md | sed 's/^# \(.*\) Logging Standards$/\1/')

if [ -n "$P_CONST" ] && [ "$P_CONST" = "$P_CODE" ] && [ "$P_CONST" = "$P_LOG" ]; then
    echo "Project Identity Synchronized: '$P_CONST' (PASSED)"
else
    echo "FAILED: Project identity mismatch: constitution='$P_CONST', coding='$P_CODE', logging='$P_LOG'"
    exit 1
fi

# 1.3 Verify Sync Impact Report includes Optional Modules and Companion Standards
for field in "Version Change:" "Modified Principles:" "Modified Sections:" "Optional Modules:" "Companion Standards:" "Rationale:"; do
    grep -Fq "$field" .specify/memory/constitution.md || { echo "FAILED: Missing '$field' in Sync Impact Report"; exit 1; }
done
echo "Sync Impact Report check: PASSED"
```

**Expected Outcome**: All three files report `PRESENT`, project identity is synchronized (`Spec Kit Testing`), and `Sync Impact Report check: PASSED`.

---

### Scenario 2: Verify Zero Unresolved Placeholders & Zero Leftover Conditional Markers (US1 / US2 / FR-005 / FR-009)

Validates that no `[ALL_CAPS_IDENTIFIER]` tokens remain in `.specify/memory/{constitution,coding-standards,logging-standards}.md`, that no `OPTIONAL-MODULE`, `OPTIONAL-SUBCLAUSE`, or `DEFAULT-CLAUSE` HTML comments remain in `.specify/memory/constitution.md`, and that Principle III contains no contradictory coverage clauses.

```bash
# 2.1 Verify zero [ALL_CAPS_IDENTIFIER] tokens remain in any ratified governance file
for doc in \
  .specify/memory/constitution.md \
  .specify/memory/coding-standards.md \
  .specify/memory/logging-standards.md; do
    MATCHES=$(grep -o '\[[A-Z0-9_]*\]' "$doc" || true)
    if [ -n "$MATCHES" ]; then
        echo "FAILED: Unresolved placeholders in $doc: $MATCHES"
        exit 1
    fi
done
echo "Zero unresolved [ALL_CAPS_IDENTIFIER] tokens: PASSED"

# 2.2 Verify zero conditional HTML comment markers remain in .specify/memory/constitution.md
MARKERS=$(grep -E '<!-- /?(OPTIONAL-MODULE|OPTIONAL-SUBCLAUSE|DEFAULT-CLAUSE)' .specify/memory/constitution.md || true)
if [ -n "$MARKERS" ]; then
    echo "FAILED: Leftover conditional HTML markers in .specify/memory/constitution.md: $MARKERS"
    exit 1
fi
echo "Zero conditional HTML comment markers: PASSED"

# 2.3 Verify Principle III mutual exclusivity (either Plan Justification & Skip Allowlist OR 100% Branch Coverage Gate, never both)
HAS_DEFAULT=$(grep -Fc "**Plan Justification & Skip Allowlist**" .specify/memory/constitution.md || true)
HAS_MOD_B=$(grep -Fc "**100% Branch Coverage Gate**" .specify/memory/constitution.md || true)
if [ "$((HAS_DEFAULT + HAS_MOD_B))" -eq 1 ]; then
    echo "Principle III mutual exclusivity check: PASSED (default=$HAS_DEFAULT, module_b=$HAS_MOD_B)"
else
    echo "FAILED: Principle III must contain exactly one coverage clause (default=$HAS_DEFAULT, module_b=$HAS_MOD_B)"
    exit 1
fi
```

**Expected Outcome**: All three checks output `PASSED`.

---

### Scenario 3: Verify `speckit-constitution` Co-Application & Merge Rules (US1 / US2 / FR-001–FR-009)

Verifies that `.agents/skills/speckit-constitution/SKILL.md` specifies resolution of all three templates, updated Scope Guard rules, optional module precedence and transformation rules (`MODULE-A`–`MODULE-D`, `MODULE-D-AOT-TRIM`, `TRACE`), placeholder merge precedence, and the 5-field `Recorded Deviations` conflict gate.

```bash
SKILL=".agents/skills/speckit-constitution/SKILL.md"

for term in \
  "constitution-template" \
  "coding-standards-template" \
  "logging-standards-template" \
  ".specify/memory/constitution.md" \
  ".specify/memory/coding-standards.md" \
  ".specify/memory/logging-standards.md" \
  "MODULE-A" \
  "MODULE-B" \
  "MODULE-C" \
  "MODULE-D" \
  "MODULE-D-AOT-TRIM" \
  "PLAN-JUSTIFICATION-AND-SKIP-ALLOWLIST" \
  "Recorded Deviations" \
  "Companion Standards"; do
    grep -Fq "$term" "$SKILL" || { echo "FAILED: Missing '$term' in $SKILL"; exit 1; }
done
echo "speckit-constitution skill contract check: PASSED"
```

**Expected Outcome**: `speckit-constitution skill contract check: PASSED`.

---

### Scenario 4: Verify Downstream Spec Kit Skill Integration (US3 / FR-010 / SC-003)

Verifies that all 5 downstream skills (`speckit-plan`, `speckit-tasks`, `speckit-analyze`, `speckit-implement`, `speckit-converge`) load and reference `.specify/memory/coding-standards.md` and `.specify/memory/logging-standards.md` alongside `.specify/memory/constitution.md`.

```bash
for skill in \
  .agents/skills/speckit-plan/SKILL.md \
  .agents/skills/speckit-tasks/SKILL.md \
  .agents/skills/speckit-analyze/SKILL.md \
  .agents/skills/speckit-implement/SKILL.md \
  .agents/skills/speckit-converge/SKILL.md; do
    grep -Fq ".specify/memory/constitution.md" "$skill" || { echo "FAILED: $skill missing constitution.md reference"; exit 1; }
    grep -Fq ".specify/memory/coding-standards.md" "$skill" || { echo "FAILED: $skill missing coding-standards.md reference"; exit 1; }
    grep -Fq ".specify/memory/logging-standards.md" "$skill" || { echo "FAILED: $skill missing logging-standards.md reference"; exit 1; }
    echo "$skill: PASSED"
done
echo "All 5 downstream skills verified: PASSED"
```

**Expected Outcome**: All 5 skill files report `PASSED`.

---

### Scenario 5: Verify Base Templates in `.specify/templates/` Remain Untouched (US1 / FR-002)

Verifies that co-applying governance to `.specify/memory/` did not overwrite or strip placeholders/delimiters from the source templates in `.specify/templates/`.

```bash
# Source templates must still contain [PROJECT_NAME] and OPTIONAL-MODULE markers
grep -Fq "[PROJECT_NAME]" .specify/templates/constitution-template.md || { echo "FAILED: constitution-template.md mutated"; exit 1; }
grep -Fq "<!-- OPTIONAL-MODULE: MODULE-A" .specify/templates/constitution-template.md || { echo "FAILED: constitution-template.md markers stripped"; exit 1; }
grep -Fq "[PRIMARY_LANGUAGE_AND_RUNTIME]" .specify/templates/coding-standards-template.md || { echo "FAILED: coding-standards-template.md mutated"; exit 1; }
grep -Fq "[LOGGING_FRAMEWORK]" .specify/templates/logging-standards-template.md || { echo "FAILED: logging-standards-template.md mutated"; exit 1; }
echo "Source templates integrity check: PASSED"
```

**Expected Outcome**: `Source templates integrity check: PASSED`.
