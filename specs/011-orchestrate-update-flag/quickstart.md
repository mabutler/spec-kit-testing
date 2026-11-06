# Quickstart: Validating `--update` / `--amend` Replanning in speckit-orchestrate

**Feature**: `011-orchestrate-update-flag`  
**Date**: 2026-11-06  
**Status**: Completed  

---

## Overview

This guide provides runnable validation scenarios to verify the `--update` and `--amend` flag functionality in `/speckit-orchestrate`. In accordance with Constitution Principle III, verification relies on static inspection, cross-client parity diffs, and deterministic execution simulations without maintaining automated test suites.

---

## Prerequisites

1. Active Spec Kit project environment with `.specify/` and active governance suite (`constitution.md`, `coding-standards.md`, `logging-standards.md`).
2. Dual-client directories present: `.agents/` and `.claude/`.
3. Standard POSIX utilities installed: `bash`, `diff`, `cmp`, `grep`.

---

## Validation Scenarios

### Scenario 1: Cross-Client Parity Verification (Static Quality Gate)

Verify that `.agents/skills/speckit-orchestrate/SKILL.md` and `.claude/skills/speckit-orchestrate/SKILL.md` are identical byte-for-byte.

```bash
# Compare skill files across Google Antigravity and Claude Code
diff -u .agents/skills/speckit-orchestrate/SKILL.md .claude/skills/speckit-orchestrate/SKILL.md
cmp -s .agents/skills/speckit-orchestrate/SKILL.md .claude/skills/speckit-orchestrate/SKILL.md

# Expected outcome: Exit code 0, no diff output
echo "Cross-client parity: PASS"
```

---

### Scenario 2: Documentation Gate Compliance (Principle VII)

Verify that root `README.md` documents `--update` and `--amend` flag usage under the Orchestrator section:

```bash
# Verify presence of --update and --amend in README.md
grep -E "(--update|--amend)" README.md

# Expected outcome: At least one matching line documenting the flags
```

---

### Scenario 3: Fail-Closed Boundary Check (Missing Description)

Validate that invoking `--update` or `--amend` with an empty string or whitespace triggers immediate fail-closed termination.

**Command**:
```bash
# Invocation with empty description
/speckit-orchestrate --update=""
```

**Expected Outcome**:
- Orchestrator halts immediately before dispatching any subagents.
- Emits `CRITICAL` diagnostic:
  `"CRITICAL: --update / --amend requires a non-empty description of architectural changes."`
- Zero files created or mutated.

---

### Scenario 4: Fail-Closed Boundary Check (Missing Baseline Plan)

Validate that invoking `--update` on an un-planned feature fails closed.

**Setup**:
```bash
# Create temporary feature directory lacking plan.md
mkdir -p specs/999-unplanned-feature
echo "# Spec" > specs/999-unplanned-feature/spec.md
```

**Command**:
```bash
SPECIFY_FEATURE_DIRECTORY=/home/admin/projects/spec-kit-testing/specs/999-unplanned-feature \
/speckit-orchestrate --update="Add Redis cache"
```

**Expected Outcome**:
- Orchestrator halts immediately before modifying any files.
- Emits `CRITICAL` diagnostic:
  `"CRITICAL: Cannot execute --update because required baseline artifacts are missing in specs/999-unplanned-feature. Expected both spec.md and plan.md."`
- Cleanup: `rm -rf specs/999-unplanned-feature`

---

### Scenario 5: Non-Destructive Architectural Replanning (End-to-End Simulation)

Validate that invoking `--update` amends planning artifacts while preserving completed tasks.

**Setup**:
1. Active feature with existing `spec.md`, `plan.md`, and `tasks.md` containing completed `- [x]` tasks:
   ```markdown
   ## Phase 1: Core Foundation
   - [x] T001 Implement initial schema in src/models.py
   - [ ] T002 Implement repository layer in src/repo.py
   ```

**Command**:
```bash
/speckit-orchestrate --update='Add Redis caching layer to repository'
```

**Expected Outcome**:
1. Argument parser captures `UPDATE_DESCRIPTION="Add Redis caching layer to repository"` and sets `IS_UPDATE_MODE=true`.
2. Stage 3 (`plan`) subagent (`speckit-reasoner`) executes in-place amendment:
   - `plan.md` Technical Context updated with Redis dependency.
   - `research.md` appends Redis caching evaluation.
   - `contracts/` and `data-model.md` updated with cache schemas.
3. Stage 4 (`tasks`) subagent (`speckit-executor`) updates `tasks.md`:
   - Task `T001` remains `- [x]` (preserved intact).
   - A new update phase is appended: `## Phase N: Architectural Update - Redis Caching Layer` with new tasks (`- [ ]`).
4. Stage 5 (`analyze`) runs cross-artifact verification and confirms zero drift.
5. Orchestrator pauses cleanly at `PAUSED_AT_CHECKPOINT`:
   ```text
   Pipeline Execution Summary (Replanning Mode: --update)
   Status: PAUSED_AT_CHECKPOINT
   Review amended plan.md and tasks.md. Resume with: /speckit-orchestrate --resume
   ```

---

### Scenario 6: Continuous Execution via `--continue`

Validate that providing `--continue` with `--update` executes replanning and continues into implementation and convergence.

**Command**:
```bash
/speckit-orchestrate --update='Add Redis caching layer' --continue
```

**Expected Outcome**:
- Replanning stages (3, 4, 5) complete.
- Pre-implementation pause is bypassed.
- Orchestrator dispatches Stage 6 (`implement`) and Stage 7 (`converge`).
- Final status reports `CONVERGED`.
