# Quickstart: Static Validation Guide for README Cleanup

**Feature Branch**: `010-clean-readme`  
**Date**: 2026-11-06  
**Status**: Ready for Implementation  

This guide provides runnable static validation commands to verify that `README.md` complies with all functional requirements, constitutional constraints, and schema contracts without running automated test suites (per Principle III).

---

## Prerequisites

- Bash 4.0+ environment.
- POSIX utilities: `wc`, `grep`, `diff`, `cmp`, `sed`.
- Working directory: repository root (`/home/admin/projects/spec-kit-testing`).

---

## Scenario 1: Validate Canonical Section Headings

Verify that `README.md` contains the four required canonical sections defined in `.specify/memory/coding-standards.md`.

```bash
# Run heading check
grep -E '^## (Project Overview & 4-Tier Architecture|Co-Applied Governance Suite|Spec Kit Skills & Subagent Orchestration Reference|Portable Bootstrapping & Verification Quickstart)' README.md
```

**Expected Outcome**: Exactly 4 lines printed, matching each canonical section heading in order.

---

## Scenario 2: Validate Line Count Ceiling (SC-001)

Verify that the total line count of `README.md` is reduced by at least 25% (baseline: 137 lines; target ceiling: $\le 104$ lines).

```bash
# Count lines in README.md
LINES=$(wc -l < README.md)
echo "Current README.md line count: $LINES"
[ "$LINES" -le 104 ] && echo "PASS: Line count under ceiling (<= 104)" || echo "FAIL: Line count exceeds ceiling"
```

**Expected Outcome**: `LINES` is $\le 104$, and command outputs `PASS: Line count under ceiling (<= 104)`.

---

## Scenario 3: Verify Boilerplate Elimination (FR-001, FR-002, SC-002)

Verify that generic template governance tables and lists have been completely removed.

```bash
# Check for generic Core Principles table header
grep -F "| Principle | Title | Mandate |" README.md || echo "PASS: Principles table removed"

# Check for Optional Modules list header
grep -F "Optional Modules" README.md || echo "PASS: Optional Modules list removed"

# Check for standard upstream skill rows in a table format
grep -E '\|\s*\*\*`/speckit-(specify|plan|tasks|implement)`\*\*' README.md || echo "PASS: Standard skill table rows removed"
```

**Expected Outcome**: All three checks print `PASS`.

---

## Scenario 4: Verify Unique Skills & Personas Spotlight (FR-003, SC-003)

Verify that only custom extensions and subagents are spotlighted.

```bash
# Verify custom skills are present
grep -F "/speckit-orchestrate" README.md
grep -F "/speckit-bootstrap" README.md
grep -F "/speckit-roadmap" README.md

# Verify subagent personas are present
grep -F "speckit-reasoner" README.md
grep -F "speckit-executor" README.md
```

**Expected Outcome**: All searches return matching lines.

---

## Scenario 5: Validate Relative Link Integrity (FR-007, SC-004)

Verify that every relative markdown link in `README.md` targets an existing file or directory on disk.

```bash
# Extract relative markdown links and verify their existence
python3 -c "
import re, os, sys

with open('README.md', 'r') as f:
    content = f.read()

# Match [text](target) where target does not start with http or mailto
links = re.findall(r'\[.*?\]\((?!http|#|mailto)(.*?)\)', content)
missing = []
for link in links:
    clean_link = link.split('#')[0]
    if clean_link and not os.path.exists(clean_link):
        missing.append(clean_link)

if missing:
    print('FAIL: Missing link targets:', missing)
    sys.exit(1)
else:
    print(f'PASS: All {len(links)} relative links resolve successfully.')
"
```

**Expected Outcome**: Prints `PASS: All <count> relative links resolve successfully.` with exit code 0.

---

## Scenario 6: Execute Documented Verification Commands (SC-005)

Verify that the verification commands published in Section 4 of `README.md` execute without errors.

```bash
# 1. Shell script syntax check
bash -n bootstrap-speckit.sh

# 2. Dual client parity check
diff -r .agents .claude

# 3. Template consistency checks
cmp -s .specify/templates/constitution-template.md .specify/presets/base-governance/templates/constitution-template.md
cmp -s .specify/templates/coding-standards-template.md .specify/presets/base-governance/templates/coding-standards-template.md
cmp -s .specify/templates/logging-standards-template.md .specify/presets/base-governance/templates/logging-standards-template.md

echo "PASS: All verification checks succeeded."
```

**Expected Outcome**: All commands exit with code 0 and output `PASS: All verification checks succeeded.`.
