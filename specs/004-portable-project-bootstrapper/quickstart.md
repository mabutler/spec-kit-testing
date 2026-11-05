# Quickstart Validation Guide: Portable Project Bootstrapper

**Feature**: `004-portable-project-bootstrapper`  
**Date**: 2026-11-05  
**Status**: Ready for Validation  

---

## 1. Overview & Prerequisites

This quickstart guide provides concrete, end-to-end validation scenarios for verifying the **Portable Project Bootstrapper** feature deliverables without automated test harnesses, in strict compliance with Constitutional Principle III (*Static Verification & No Automated Tests*).

### Prerequisites
- Linux, macOS, or Windows environment.
- Bash 4.0+ (or POSIX `sh`) and/or PowerShell (`pwsh` or Windows PowerShell 5.1).
- A clean scratch or temporary directory outside the current repository to serve as `<target-repo>`.

---

## 2. Validation Scenarios

### Scenario 1: Ultra-Thin Bash Seeding (`bootstrap-speckit.sh`)

**Objective**: Verify that `bootstrap-speckit.sh` seeds all managed files into a fresh target directory, preserves user state, and configures `.gitignore`.

1. **Setup**:
   ```bash
   TARGET_DIR=$(mktemp -d -t speckit-target-sh-XXXXXX)
   echo "Testing target: $TARGET_DIR"
   ```

2. **Execute Seeder**:
   ```bash
   ./bootstrap-speckit.sh "$TARGET_DIR"
   ```

3. **Expected Outcomes**:
   - Exit code is `0`.
   - Console logs `[INFO]` messages verifying source integrity and file copying.
   - All managed files exist in `$TARGET_DIR`:
     - `$TARGET_DIR/.specify/templates/*.md`
     - `$TARGET_DIR/.specify/presets/base-governance/`
     - `$TARGET_DIR/.specify/extensions/speckit-orchestrator/`
     - `$TARGET_DIR/.agents/skills/speckit-*/SKILL.md` (all 11 skills)
     - `$TARGET_DIR/.agents/agents/speckit-reasoner.md` & `speckit-executor.md`
   - `$TARGET_DIR/.gitignore` contains `.agents/agents/*.local.md`.
   - Script line count is under 150 lines:
     ```bash
     wc -l bootstrap-speckit.sh
     ```

4. **Idempotency Check**:
   ```bash
   ./bootstrap-speckit.sh "$TARGET_DIR"
   ```
   - Exit code is `0`.
   - Summary reports `0 files copied`, all existing files skipped.

---

### Scenario 2: Ultra-Thin PowerShell Seeding (`bootstrap-speckit.ps1`)

**Objective**: Verify that `bootstrap-speckit.ps1` produces identical, idempotent results using PowerShell.

1. **Setup**:
   ```bash
   TARGET_DIR_PWSH=$(mktemp -d -t speckit-target-pwsh-XXXXXX)
   ```

2. **Execute Seeder**:
   ```bash
   pwsh ./bootstrap-speckit.ps1 "$TARGET_DIR_PWSH"
   ```

3. **Expected Outcomes**:
   - Exit code is `0`.
   - Managed files are created identically to Scenario 1.
   - Script line count is under 150 lines:
     ```bash
     wc -l bootstrap-speckit.ps1
     ```

---

### Scenario 3: Agent-Native Bootstrapper Verification (`/speckit-bootstrap`)

**Objective**: Verify that `/speckit-bootstrap` runs natively without calling shell scripts, cleans up legacy scripts, and generates the manifest.

1. **Setup**:
   - In a seeded repository, simulate an obsolete script directory:
     ```bash
     mkdir -p "$TARGET_DIR/.specify/scripts/bash"
     touch "$TARGET_DIR/.specify/scripts/bash/legacy.sh"
     ```

2. **Execute Skill in Agent**:
   ```text
   /speckit-bootstrap
   ```

3. **Expected Outcomes**:
   - Obsolete directory `$TARGET_DIR/.specify/scripts/` is safely removed.
   - Manifest `$TARGET_DIR/.specify/integrations/speckit-bootstrap.manifest.json` is generated with valid SHA-256 digests.
   - `.specify/extensions.yml` contains `speckit.orchestrate` hook under `hooks.after_specify`.
   - Report outputs a clean status indicating all managed files are valid.

---

### Scenario 4: Non-Destructive Upgrade & Drift Detection (`--check` and `--upgrade`)

**Objective**: Prove that user modifications and protected state are preserved during upgrade.

1. **Setup**:
   - Create a ratified constitution in `$TARGET_DIR/.specify/memory/constitution.md`.
   - Add a custom local override in `$TARGET_DIR/.specify/templates/overrides/spec-template.md`.
   - Create a local agent profile in `$TARGET_DIR/.agents/agents/speckit-executor.local.md`.
   - Manually modify a managed skill file:
     ```bash
     echo "<!-- custom local edit -->" >> "$TARGET_DIR/.agents/skills/speckit-specify/SKILL.md"
     ```

2. **Execute Dry-Run Inspection**:
   ```text
   /speckit-bootstrap --check
   ```

3. **Expected Outcomes**:
   - File classification plan outputs:
     - `.specify/memory/constitution.md` -> `PRESERVE_USER_STATE`
     - `.specify/templates/overrides/spec-template.md` -> `PRESERVE_USER_STATE`
     - `.agents/agents/speckit-executor.local.md` -> `PRESERVE_USER_STATE`
     - `.agents/skills/speckit-specify/SKILL.md` -> `SKIP_DRIFTED`
   - Zero files on disk are modified.

4. **Execute Live Upgrade**:
   ```text
   /speckit-bootstrap --upgrade
   ```
   - Unmodified managed files update to latest version.
   - Drifted `speckit-specify/SKILL.md` is untouched, accompanied by a `WARN` notification.
   - Protected user files remain 100% untouched.

---

### Scenario 5: Script-Free 4-Tier Template Resolution Verification

**Objective**: Verify that all 11 Spec Kit skills operate without referencing `.specify/scripts/`.

1. **Static Reference Audit**:
   ```bash
   grep -rn "\.specify/scripts" .agents/skills/
   ```
   - Output must be completely empty (0 occurrences).

2. **Script Directory Deletion Verification**:
   ```bash
   test ! -d .specify/scripts && echo "PASS: .specify/scripts is removed"
   ```

3. **End-to-End Skill Run**:
   - Run `/speckit-specify test-feature` or `/speckit-plan` on a test branch.
   - Verify that template inheritance (`overrides/` -> `presets/` -> `extensions/` -> `core`) functions deterministically using native agent file reading.

---

### Scenario 6: Cleanup

```bash
rm -rf "$TARGET_DIR" "$TARGET_DIR_PWSH"
```
