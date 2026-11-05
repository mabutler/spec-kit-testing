# Quickstart Validation Guide: Roadmap Management (`speckit-roadmap`)

**Feature**: `005-roadmap-management`  
**Date**: 2026-11-05  
**Status**: Ready for Validation  

---

## 1. Overview & Prerequisites

This quickstart guide provides runnable static and end-to-end validation scenarios for verifying the **Roadmap Management (`speckit-roadmap`)** feature deliverables in strict compliance with Constitutional Principle III (*Static Verification & No Automated Tests*).

### Prerequisites
- Linux, macOS, or Windows environment with `git` and `bash` (and optionally `pwsh`).
- Active worktree `/home/admin/projects/spec-kit-testing/.worktrees/005-roadmap-management`.

---

## 2. Validation Scenarios

### Scenario 1: 4-Tier `roadmap-template` & Preset Integrity Check

**Objective**: Verify that `roadmap-template.md` exists in both the core fallback tier and `base-governance` preset tier, is registered in `preset.yml`, and is identical across both tiers.

1. **Run Verification Commands**:
   ```bash
   # Verify core and preset template files exist and match bit-for-bit
   diff -u .specify/templates/roadmap-template.md .specify/presets/base-governance/templates/roadmap-template.md

   # Verify preset.yml registers roadmap-template with strategy: replace
   grep -A 3 'name: "roadmap-template"' .specify/presets/base-governance/preset.yml
   ```

2. **Expected Outcomes**:
   - `diff -u` exits with `0` (identical files).
   - `preset.yml` outputs `name: "roadmap-template"`, `file: "templates/roadmap-template.md"`, and `strategy: "replace"`.

---

### Scenario 2: Structural Lint & Schema Verification of `ROADMAP.md` (`/speckit-roadmap --check`)

**Objective**: Verify that this repository's `ROADMAP.md` conforms 100% to `roadmap-schema-contract.md` (`RM-LINT-001` through `RM-LINT-006`).

1. **Run Static Inspection**:
   ```bash
   # Verify Overview of Initiatives table header contains all 7 canonical columns
   grep -F "| Phase | Initiative | Status | Prerequisites | Spec | Goal | Key Deliverables |" ROADMAP.md

   # Verify all 6 phases appear in Overview table and detailed sections
   grep -E "^\| \*\*Phase [1-6]\*\*" ROADMAP.md | wc -l
   grep -E "^## Phase [1-6]:" ROADMAP.md | wc -l

   # Verify all 6 phases include ### Metadata subsections
   grep -F "### Metadata" ROADMAP.md | wc -l
   ```

2. **Expected Outcomes**:
   - Overview table header matches the 7-column contract.
   - Exactly `6` rows in the Overview table, `6` `## Phase N:` sections, and `6` `### Metadata` blocks.
   - Phases 1–4 are marked `COMPLETED` with links to `specs/001-*` through `specs/004-*`, Phase 5 is marked `COMPLETED` (after implementation) or `IN_PROGRESS` (during implementation) with `specs/005-roadmap-management/`, and Phase 6 is marked `PLANNED` with `—`.

---

### Scenario 3: 100% Script-Free Skill Verification (`SC-004`)

**Objective**: Verify that all 12 Spec Kit skills (including `.agents/skills/speckit-roadmap/SKILL.md` and updated `.agents/skills/speckit-specify/SKILL.md` and `.agents/skills/speckit-bootstrap/SKILL.md`) contain zero references to `.specify/scripts/` and that `.specify/scripts/` does not exist.

1. **Run Verification Commands**:
   ```bash
   # Confirm 12 skills exist
   ls -1 .agents/skills/speckit-*/SKILL.md | wc -l

   # Confirm .specify/scripts does not exist
   test ! -e .specify/scripts && echo "PASS: No .specify/scripts directory"

   # Confirm zero references to .specify/scripts/bash/ in functional skill steps
   grep -rn "\.specify/scripts/bash/" .agents/skills/ || echo "PASS: Zero script execution references"
   ```

2. **Expected Outcomes**:
   - Skill count is `12`.
   - `.specify/scripts` directory is absent.
   - Zero skills invoke `.specify/scripts/bash/`.

---

### Scenario 4: Bootstrapper Seeding, Manifest SHA-256 Sync & Protected `ROADMAP.md` State

**Objective**: Verify that `bootstrap-speckit.sh` and `bootstrap-speckit.ps1` pass syntax checks, stay under 150 lines, seed all 12 skills and `roadmap-template.md` into a target repository, never overwrite an existing target `ROADMAP.md` (even with `--force`), and have 100% matching SHA-256 digests in `.specify/integrations/*.manifest.json`.

1. **Run Verification Commands**:
   ```bash
   # Syntax and line-count check
   bash -n bootstrap-speckit.sh
   wc -l bootstrap-speckit.sh bootstrap-speckit.ps1

   # Seed a temporary target directory that already has a custom ROADMAP.md
   TMP_TARGET=$(mktemp -d -t speckit-roadmap-test-XXXXXX)
   echo "# Custom Project Roadmap - Do Not Clobber" > "$TMP_TARGET/ROADMAP.md"
   ./bootstrap-speckit.sh "$TMP_TARGET" --force

   # Verify custom ROADMAP.md was preserved untouched
   grep -F "# Custom Project Roadmap - Do Not Clobber" "$TMP_TARGET/ROADMAP.md"

   # Verify roadmap-template.md and speckit-roadmap skill were seeded
   test -f "$TMP_TARGET/.specify/templates/roadmap-template.md"
   test -f "$TMP_TARGET/.specify/presets/base-governance/templates/roadmap-template.md"
   test -f "$TMP_TARGET/.agents/skills/speckit-roadmap/SKILL.md"
   rm -rf "$TMP_TARGET"
   ```

2. **Expected Outcomes**:
   - `bash -n bootstrap-speckit.sh` exits `0`; both seeder scripts are `< 150` lines.
   - `$TMP_TARGET/ROADMAP.md` retains `# Custom Project Roadmap - Do Not Clobber`.
   - All new roadmap templates and the `speckit-roadmap` skill are present in `$TMP_TARGET`.
   - All SHA-256 digests in `.specify/integrations/{speckit,agy,speckit-bootstrap}.manifest.json` match `sha256sum` on disk.
