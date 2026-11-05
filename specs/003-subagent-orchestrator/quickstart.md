# Quickstart & Validation Guide: Subagent-Driven Spec Kit Orchestrator

**Feature**: `003-subagent-orchestrator`  
**Date**: 2026-11-05  
**Spec**: [spec.md](./spec.md) | **Plan**: [plan.md](./plan.md)

## Overview

This guide documents the runnable validation scenarios and static verification checks that prove the Subagent-Driven Spec Kit Orchestrator (`.agents/skills/speckit-orchestrate/SKILL.md`, `.agents/agents/speckit-reasoner.md`, `.agents/agents/speckit-executor.md`, `.specify/extensions.yml`, and `.gitignore`) works end-to-end in compliance with `.specify/memory/constitution.md` (including Principle III's prohibition on automated test suites).

---

## Prerequisites

- POSIX-compliant shell (`bash` 4.0+)
- `python3` with `yaml` and `json` standard/installed modules (used by `.specify/scripts/bash/common.sh` for YAML/JSON validation)
- Repository root at `/home/admin/projects/spec-kit-testing` with `.specify/memory/{constitution,coding-standards,logging-standards}.md` present

---

## 1. Static Verification & Schema Validation Commands

Run these commands from the repository root (`/home/admin/projects/spec-kit-testing`) after implementation to verify artifact integrity, YAML/JSON syntax, gitignore coverage, and constitutional compliance:

### 1.1 Verify Deliverable Files Exist and Are Non-Empty

```bash
test -s .agents/agents/speckit-reasoner.md && \
test -s .agents/agents/speckit-executor.md && \
test -s .agents/skills/speckit-orchestrate/SKILL.md && \
test -s .specify/extensions.yml && \
echo "PASS: All Phase 3 deliverables exist and are non-empty"
```

### 1.2 Validate `.specify/extensions.yml` Hook Schema

```bash
python3 -c '
import yaml, sys
with open(".specify/extensions.yml", encoding="utf-8") as f:
    data = yaml.safe_load(f)
hooks = data.get("hooks", {}).get("after_specify", [])
assert isinstance(hooks, list) and len(hooks) >= 1, "Missing hooks.after_specify list"
orch = [h for h in hooks if h.get("command") == "speckit.orchestrate"]
assert len(orch) == 1, "Missing speckit.orchestrate hook entry"
assert orch[0].get("enabled", True) is True, "Hook must be enabled"
assert isinstance(orch[0].get("optional"), bool), "optional flag must be boolean"
print("PASS: .specify/extensions.yml schema valid")
'
```

### 1.3 Validate Agent Profiles (`.agents/agents/speckit-*.md`) Frontmatter

```bash
python3 -c '
import yaml
for path, expected_tier in [
    (".agents/agents/speckit-reasoner.md", "reasoning"),
    (".agents/agents/speckit-executor.md", "execution"),
]:
    with open(path, encoding="utf-8") as f:
        content = f.read()
    assert content.startswith("---\n"), f"{path} missing YAML frontmatter"
    fm_text = content.split("---\n", 2)[1]
    fm = yaml.safe_load(fm_text)
    assert fm.get("role_tier") == expected_tier, f"{path} role_tier != {expected_tier}"
    assert fm.get("model_policy", {}).get("respect_session_ceiling") is True, f"{path} missing session ceiling policy"
print("PASS: Agent profile frontmatter valid")
'
```

### 1.4 Verify `.gitignore` Protects Local Agent Overrides (`.agents/agents/*.local.md`)

```bash
grep -qxF '.agents/agents/*.local.md' .gitignore && \
git check-ignore -q .agents/agents/speckit-reasoner.local.md && \
git check-ignore -q .agents/agents/speckit-plan.local.md && \
echo "PASS: .gitignore excludes .agents/agents/*.local.md"
```

### 1.5 Verify Pre-PR Constitutional Gate & Zero Automated Test Files

```bash
.specify/scripts/bash/resolve-template.sh constitution-template --json >/dev/null && \
bash -n .specify/scripts/bash/*.sh && \
! find . -maxdepth 3 -name "*test*.py" -o -name "*test*.sh" | grep -v "spec-kit-testing" | grep -q . && \
echo "PASS: Constitutional Pre-PR gate and Principle III static verification passed"
```

---

## 2. End-to-End Orchestration Validation Scenarios

### Scenario A: Default Pre-Implementation Human Checkpoint (`US2`)
- **Invoke**: `/speckit-orchestrate` (or `/speckit-orchestrate --pause-before-implement`)
- **Expected Behavior**:
  1. Reads `.specify/feature.json` (`specs/003-subagent-orchestrator`).
  2. Sees `spec.md` and `plan.md` already exist and pass validation (`Specify = SKIPPED_EXISTING`, `Clarify Gate = PASSED`, `Plan = SKIPPED_EXISTING`).
  3. Dispatches `speckit-tasks` subagent via `speckit-executor` (stepped down to `Flash` when session is on `Argon`/`Pro`, or capped at session ceiling).
  4. Dispatches `speckit-analyze` subagent via `speckit-reasoner` (`Analyze & Self-Heal Gate`, performing up to 2 self-heal passes if `MEDIUM`/`LOW` drift is found).
  5. By default, halts cleanly before `speckit-implement` with status `PAUSED_AT_CHECKPOINT` and instructs the user to run `/speckit-orchestrate --resume` (or `/speckit-orchestrate --continue`) after reviewing `plan.md` and `tasks.md`.

### Scenario B: Continuous Autopilot Execution through the End (`US1`)
- **Invoke**: `/speckit-orchestrate --continue` (or `/speckit-orchestrate --continuous`)
- **Expected Behavior**:
  1. Runs through all stages without pausing before implementation.
  2. Dispatches `speckit-implement` subagent via `speckit-executor` and verifies completion via `speckit-converge` (`speckit-reasoner`).
  3. Outputs the `Pipeline Execution Summary` table with overall status `CONVERGED`.

### Scenario C: Local Agent Override Resolution (`US3`)
- **Setup**: Create `.agents/agents/speckit-executor.local.md` (gitignored) setting a custom model tier or prompt note.
- **Expected Behavior**:
  1. `git status --short` shows `.agents/agents/speckit-executor.local.md` is ignored by git.
  2. `/speckit-orchestrate` resolves `.agents/agents/speckit-executor.local.md` ahead of `.agents/agents/speckit-executor.md` and reports the local override profile in the `Pipeline Execution Summary` table.
  3. Remove `.agents/agents/speckit-executor.local.md` after verification.
