# Interface Contract: Orchestrator `--update` / `--amend` Replanning Interface

**Feature**: `011-orchestrate-update-flag`  
**Contract Version**: `1.0.0`  
**Date**: 2026-11-06  
**Status**: Ratified  

---

## 1. Orchestrator CLI Syntax & Argument Schema

### 1.1 Command Invocations

```text
/speckit-orchestrate [--update='<desc>' | --update="<desc>" | --update <desc>] [flags]
/speckit-orchestrate [--amend='<desc>'  | --amend="<desc>"  | --amend <desc>]  [flags]
```

### 1.2 Flag Parameter Schema

| Parameter | Type | Required | Default | Aliases | Description |
|-----------|------|----------|---------|---------|-------------|
| `--update` | `string` | Optional | `""` | `--amend` | Triggers non-destructive replanning flow with the specified architectural update description. |
| `--continue` | `boolean` | Optional | `false` | `--continuous`, `--no-pause`, `--auto-implement` | Bypasses the pre-implementation review pause, running through Stage 6 (`implement`) and Stage 7 (`converge`). |
| `--pause-before-implement` | `boolean` | Optional | `true` | — | Explicitly enforces pause after Stage 5 (`analyze`). Default behavior. |
| `--from` | `StageName` | Optional | Derived | — | Specifies starting stage (`specify`, `clarify`, `plan`, `tasks`, `analyze`, `implement`, `converge`). When used with `--update`, preserves existing artifacts while resetting execution point. |
| `--until` | `StageName` | Optional | `analyze` | — | Specifies stage to halt cleanly after. Defaults to `analyze` unless `--continue` is specified. |
| `--resume` | `boolean` | Optional | `false` | — | Resumes pipeline from the next incomplete stage on an existing feature. |
| `--model` | `string` | Optional | `inherit` | — | Overrides LLM model tier (`inherit`, `pro`, `flash`, `flash_lite`, `opus`, `sonnet`). |
| `--override-ceiling` | `boolean` | Optional | `false` | — | Allows escalating subagents to high-reasoning models beyond standard session ceiling. |

### 1.3 CLI Parsing & Normalization Rules

1. **Flag Detection**:
   - Matches regex patterns:
     - `--update=['"](?P<desc>[^'"]+)['"]` or `--update=(?P<desc>[^\s]+)`
     - `--amend=['"](?P<desc>[^'"]+)['"]` or `--amend=(?P<desc>[^\s]+)`
     - `--update\s+(?P<desc>[^-\s][^-\n]*)` (captures non-flag tokens up to the next `--flag` or end of string)
     - `--amend\s+(?P<desc>[^-\s][^-\n]*)`
2. **Surrounding Quote Stripping**:
   - If `<desc>` is enclosed in matching single (`'`) or double (`"`) quotes, the quotes MUST be stripped.
3. **Whitespace Trimming**:
   - Leading and trailing whitespace MUST be trimmed.
4. **Canonical State Variables**:
   - `IS_UPDATE_MODE`: Set to `true` if `--update` or `--amend` is present.
   - `UPDATE_DESCRIPTION`: Set to the sanitized string value.

---

## 2. Boundary Error Contracts (Fail-Closed Diagnostics)

When an invocation fails boundary validation in `--update` mode, the orchestrator MUST emit a structured diagnostic message to `stderr` (or session console) and halt immediately without creating or mutating any files.

### 2.1 Missing or Empty Update Description

- **Trigger**: `--update` or `--amend` passed with empty string, whitespace only, or no argument.
- **Severity**: `CRITICAL`
- **Output Message Format**:
  ```text
  CRITICAL: --update / --amend requires a non-empty description of architectural changes.
  Usage examples:
    /speckit-orchestrate --update='Add Redis caching to session store'
    /speckit-orchestrate --amend "Migrate schema to PostgreSQL"
  ```
- **Exit Status**: Halts execution; no subagents dispatched.

### 2.2 Missing Active Feature Directory

- **Trigger**: No feature directory found via `SPECIFY_FEATURE_DIRECTORY` or `.specify/feature.json`.
- **Severity**: `CRITICAL`
- **Output Message Format**:
  ```text
  CRITICAL: Cannot execute --update without an active feature directory.
  Ensure SPECIFY_FEATURE_DIRECTORY is set or .specify/feature.json points to an existing feature.
  ```
- **Exit Status**: Halts execution; no subagents dispatched.

### 2.3 Missing Baseline Architectural Documents

- **Trigger**: Resolved feature directory does not contain `spec.md` or `plan.md`.
- **Severity**: `CRITICAL`
- **Output Message Format**:
  ```text
  CRITICAL: Cannot execute --update because required baseline artifacts are missing in {FEATURE_DIR}.
  Missing artifact(s): {MISSING_ARTIFACTS_LIST}.
  An architectural update requires an existing spec.md and plan.md baseline. For new features, run /speckit-orchestrate without --update.
  ```
- **Exit Status**: Halts execution; no files created or overwritten.

---

## 3. Subagent Prompt Directive Contracts

During `--update` mode, the orchestrator enriches the standard subagent dispatch payload with stage-specific replanning directives.

### 3.1 Standard Subagent Prompt Envelope
```markdown
## Stage Execution Directive: {STAGE_NAME}

1. Target Skill: Read and execute {SKILL_FILE_PATH}
2. Feature Context:
   - SPECIFY_FEATURE_DIRECTORY: {FEATURE_DIR}
   - .specify/feature.json: {"feature_directory": "{REL_FEATURE_DIR}"}
   - SPECIFY_FEATURE_NO_PERSIST=1
3. Replanning Mode & Update Context (Active):
   - UPDATE_ACTIVE: true
   - UPDATE_DESCRIPTION: {UPDATE_DESCRIPTION}
   - REPLANNING_SCOPE: {STAGE_SPECIFIC_INSTRUCTION}
4. Governance Suite Adherence (Non-Negotiable):
   - Enforce .specify/memory/constitution.md (Static verification only; zero automated unit/integration tests).
   - Enforce .specify/memory/coding-standards.md and .specify/memory/logging-standards.md.
5. Hook Anti-Recursion Guard:
   - ORCHESTRATOR_CHILD=true: Do NOT invoke /speckit-orchestrate from any hooks.
6. Required Completion Report:
   Return structured summary:
   - STAGE_STATUS: SUCCESS | PAUSED_FOR_USER | FAILED
   - ARTIFACTS_TOUCHED: <comma-separated list of paths>
   - GATE_DATA: <checklist results, finding counts, or convergence outcome>
   - DIAGNOSTICS: <summary of log messages>
```

### 3.2 Stage-Specific `REPLANNING_SCOPE` Definitions

#### Stage 1: Specify (if requirements updated)
```markdown
REPLANNING_SCOPE: Update spec.md in place to incorporate new or modified requirements arising from: "{UPDATE_DESCRIPTION}". Retain existing user stories, priority classifications, and constitutional quality gates. Do not wipe or reset existing acceptance criteria unless directly superseded.
```

#### Stage 3: Plan (`speckit-reasoner`)
```markdown
REPLANNING_SCOPE: Perform surgical, in-place non-destructive architectural replanning across plan.md, research.md, data-model.md, quickstart.md, and contracts/ to incorporate: "{UPDATE_DESCRIPTION}".
- DO NOT reinitialize artifacts from blank templates.
- Update Technical Context in plan.md with new technology choices, dependencies, and constraints.
- Append new research evaluations (Decision, Rationale, Alternatives considered) to research.md.
- Update or add entity schemas in data-model.md.
- Update or add interface contracts in contracts/.
- Update validation procedures in quickstart.md.
- Retain all prior valid architectural decisions and rationales.
```

#### Stage 4: Tasks (`speckit-executor`)
```markdown
REPLANNING_SCOPE: Update tasks.md in place to reflect the amended architecture for: "{UPDATE_DESCRIPTION}".
- PRESERVATION INVARIANT: You MUST preserve 100% of completed task items (- [x]) verbatim. Do not delete, renumber, or mark incomplete any completed work.
- Append a new phase (e.g., "## Phase N: Architectural Update - {UPDATE_DESCRIPTION}") or surgically adjust remaining pending tasks (- [ ]) in existing phases to implement the amended architecture.
```

#### Stage 5: Analyze (`speckit-reasoner`)
```markdown
REPLANNING_SCOPE: Perform non-destructive cross-artifact consistency analysis across amended spec.md, plan.md, and tasks.md. Validate that new tasks in tasks.md map directly to amended requirements and designs without drift.
```

---

## 4. Pipeline Execution Summary Contract

Upon reaching the Pre-Implementation Checkpoint or pipeline conclusion, the orchestrator MUST format the output following this schema:

```markdown
## Pipeline Execution Summary (Replanning Mode: --update)

- **Feature Directory**: `{FEATURE_DIR}`
- **Update Description**: `{UPDATE_DESCRIPTION}`
- **Session Model Ceiling**: `{SESSION_MODEL} ({SESSION_TIER})`
- **Overall Pipeline Status**: `PAUSED_AT_CHECKPOINT` | `CONVERGED` | `FAILED_CLOSED`

| Stage | Status | Agent Profile | Model Tier | Iterations | Artifacts Modified / Verified |
|-------|--------|---------------|------------|------------|-------------------------------|
| 1. Specify | {STATUS} | speckit-executor | {MODEL} | {N} | `spec.md` (Amended/Retained) |
| 2. Clarify Gate | {STATUS} | speckit-reasoner | {MODEL} | {N} | `spec.md`, `checklists/requirements.md` |
| 3. Plan | {STATUS} | speckit-reasoner | {MODEL} | {N} | `plan.md`, `research.md`, `data-model.md`, `quickstart.md`, `contracts/*` |
| 4. Tasks | {STATUS} | speckit-executor | {MODEL} | {N} | `tasks.md` (Preserved `- [x]`, added `- [ ]`) |
| 5. Analyze Gate | {STATUS} | speckit-reasoner | {MODEL} | {N} | `plan.md`, `tasks.md` (Zero Drift Verified) |
| 6. Implement | {STATUS} | speckit-executor | {MODEL} | {N} | (Paused at checkpoint or implemented) |
| 7. Converge | {STATUS} | speckit-reasoner | {MODEL} | {N} | (Paused at checkpoint or converged) |

### Checkpoint Status
Paused at Pre-Implementation Checkpoint. Architectural replanning is complete. Review amended `plan.md` and `tasks.md` before proceeding.

### Next Action
To proceed with implementation:
`/speckit-orchestrate --resume`
Or run continuously:
`/speckit-orchestrate --continue`
```
