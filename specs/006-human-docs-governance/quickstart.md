# Phase 1 Quickstart & Static Validation Guide: Human-Facing Documentation Standards & Governance

**Feature**: `006-human-docs-governance`  
**Date**: 2026-11-05  
**Spec**: [spec.md](spec.md) | **Data Model**: [data-model.md](data-model.md)

## Overview

Per Constitutional Principle III (*Static Verification & No Automated Tests*), verification of Phase 6 relies exclusively on static file comparisons, regex/marker checks, markdown link verification, and SHA-256 manifest digest validation—with zero automated unit test suites.

Run all commands below from the active worktree root:
```bash
cd /home/admin/projects/spec-kit-testing/.worktrees/006-human-docs-governance
```

---

## Scenario 1: Verify Base Template & Preset Byte-for-Byte Parity (US1, `SC-001`)

Verify that `.specify/templates/{constitution-template,coding-standards-template}.md` and `.specify/presets/base-governance/templates/{constitution-template,coding-standards-template}.md` are byte-identical and contain the required `MODULE-DOCS` and `[HUMAN_DOCS_CONVENTIONS]` constructs ([Contract 1](contracts/governance-templates-contract.md)):

```bash
cmp -s .specify/templates/constitution-template.md .specify/presets/base-governance/templates/constitution-template.md \
  && echo "PASS: constitution-template.md parity verified"

cmp -s .specify/templates/coding-standards-template.md .specify/presets/base-governance/templates/coding-standards-template.md \
  && echo "PASS: coding-standards-template.md parity verified"

grep -q "OPTIONAL-MODULE: MODULE-DOCS" .specify/templates/constitution-template.md \
  && grep -q "/OPTIONAL-MODULE: MODULE-DOCS" .specify/templates/constitution-template.md \
  && echo "PASS: MODULE-DOCS markers present in constitution-template.md"

grep -q "\[HUMAN_DOCS_CONVENTIONS\]" .specify/templates/coding-standards-template.md \
  && echo "PASS: [HUMAN_DOCS_CONVENTIONS] slot present in coding-standards-template.md"

grep -q "MODULE-DOCS" .agents/skills/speckit-constitution/SKILL.md \
  && grep -q "\[HUMAN_DOCS_CONVENTIONS\]" .agents/skills/speckit-constitution/SKILL.md \
  && echo "PASS: speckit-constitution/SKILL.md tracks MODULE-DOCS and [HUMAN_DOCS_CONVENTIONS]"
```

**Expected Outcome**: All 5 checks exit `0` and print `PASS`.

---

## Scenario 2: Verify Active Governance Suite Amendment (`v2.1.0`) & Zero Residual Markers (US2, `SC-001`)

Verify that `.specify/memory/constitution.md` is ratified at `2.1.0` with `MODULE-DOCS: ENABLED`, `.specify/memory/coding-standards.md` includes `## Human-Facing Documentation & README Conventions`, and all three ratified governance files contain zero unresolved `[ALL_CAPS_IDENTIFIER]` placeholders or `OPTIONAL-MODULE` comment tags ([Contract 3](contracts/readme-and-active-governance-contract.md)):

```bash
grep -q "Version Change: 2.0.0 -> 2.1.0" .specify/memory/constitution.md \
  && grep -q "MODULE-DOCS: ENABLED" .specify/memory/constitution.md \
  && grep -q "\*\*Version\*\*: 2.1.0" .specify/memory/constitution.md \
  && echo "PASS: constitution.md version 2.1.0 and MODULE-DOCS: ENABLED verified"

grep -q "## Human-Facing Documentation & README Conventions" .specify/memory/coding-standards.md \
  && echo "PASS: coding-standards.md Human-Facing Documentation section verified"

! grep -E "\[[A-Z0-9_]+\]" .specify/memory/constitution.md .specify/memory/coding-standards.md .specify/memory/logging-standards.md \
  && echo "PASS: 0 unresolved [ALL_CAPS] placeholders in .specify/memory/"

! grep -E "<!-- /?(OPTIONAL-MODULE|OPTIONAL-SUBCLAUSE|DEFAULT-CLAUSE)" .specify/memory/constitution.md \
  && echo "PASS: 0 residual OPTIONAL-MODULE comment tags in .specify/memory/constitution.md"
```

**Expected Outcome**: All 4 checks exit `0` and print `PASS`.

---

## Scenario 3: Verify Root `README.md` Completeness, Link Integrity & Ephemeral Spec Hygiene (US2, `SC-004`)

Verify that root `README.md` exists, documents all 11 Spec Kit skills and both bootstrapper scripts (`bootstrap-speckit.sh`, `bootstrap-speckit.ps1`), has zero references to ephemeral `specs/NNN-*/` directories or `FR-XXX`/`SC-XXX` identifiers, and has zero broken relative file links ([Contract 3](contracts/readme-and-active-governance-contract.md)):

```bash
test -s README.md && echo "PASS: README.md exists and is non-empty"

for skill in speckit-specify speckit-clarify speckit-plan speckit-tasks speckit-checklist \
             speckit-analyze speckit-implement speckit-converge speckit-constitution \
             speckit-orchestrate speckit-bootstrap; do
  grep -q "$skill" README.md || { echo "FAIL: Missing $skill in README.md"; exit 1; }
done
echo "PASS: All 11 Spec Kit skills documented in README.md"

grep -q "bootstrap-speckit.sh" README.md && grep -q "bootstrap-speckit.ps1" README.md \
  && echo "PASS: Both bootstrapper entry points documented in README.md"

! grep -E "specs/[0-9]{3}-|FR-[0-9]{3}|SC-[0-9]{3}" README.md .specify/memory/constitution.md .specify/memory/coding-standards.md \
  && echo "PASS: 0 ephemeral spec/FR/SC citations in README.md or active governance suite"
```

**Expected Outcome**: All checks exit `0` and print `PASS`.

---

## Scenario 4: Verify Downstream Skill Documentation Impact Gates (US3, `SC-002`, `SC-003`)

Verify that `plan-template.md`, `tasks-template.md`, and the 5 downstream skills (`speckit-plan`, `speckit-tasks`, `speckit-analyze`, `speckit-implement`, `speckit-converge`) enforce `Documentation Impact` (`USER_FACING` vs. `INTERNAL_ONLY`) ([Contract 2](contracts/documentation-impact-gate-contract.md)):

```bash
for file in .specify/templates/plan-template.md \
            .specify/templates/tasks-template.md \
            .agents/skills/speckit-plan/SKILL.md \
            .agents/skills/speckit-tasks/SKILL.md \
            .agents/skills/speckit-analyze/SKILL.md \
            .agents/skills/speckit-implement/SKILL.md \
            .agents/skills/speckit-converge/SKILL.md; do
  grep -q "USER_FACING" "$file" && grep -q "INTERNAL_ONLY" "$file" \
    || { echo "FAIL: Missing USER_FACING / INTERNAL_ONLY gate in $file"; exit 1; }
done
echo "PASS: All templates and downstream skills enforce USER_FACING vs INTERNAL_ONLY documentation gates"
```

**Expected Outcome**: Loop completes and prints `PASS`.

---

## Scenario 5: Verify Manifest SHA-256 Digest Synchronization (`FR-009`, `SC-005`)

Verify that every file tracked in `.specify/integrations/{speckit,agy,speckit-bootstrap}.manifest.json` matches its on-disk SHA-256 digest and byte size:

```bash
python3 - <<'PY'
import hashlib, json, os, sys

for mpath in [
    ".specify/integrations/speckit.manifest.json",
    ".specify/integrations/agy.manifest.json",
    ".specify/integrations/speckit-bootstrap.manifest.json",
]:
    with open(mpath, "r", encoding="utf-8") as f:
        data = json.load(f)
    for rel, meta in data["files"].items():
        if not os.path.isfile(rel):
            print(f"FAIL: {mpath} references missing file {rel}")
            sys.exit(1)
        raw = open(rel, "rb").read()
        digest = hashlib.sha256(raw).hexdigest()
        if isinstance(meta, str):
            if meta != digest:
                print(f"FAIL: Digest mismatch in {mpath} for {rel}: expected {meta}, got {digest}")
                sys.exit(1)
        else:
            if meta["digest"] != f"sha256:{digest}" or meta["size_bytes"] != len(raw):
                print(f"FAIL: Metadata mismatch in {mpath} for {rel}")
                sys.exit(1)
print("PASS: All 3 integration manifests match on-disk SHA-256 digests and byte sizes")
PY
```

**Expected Outcome**: Prints `PASS: All 3 integration manifests match on-disk SHA-256 digests and byte sizes` and exits `0`.
