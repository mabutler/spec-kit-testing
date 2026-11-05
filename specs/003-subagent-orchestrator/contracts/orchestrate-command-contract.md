# Contract: `/speckit-orchestrate` Skill & Command Interface

**Artifact Target**: `.agents/skills/speckit-orchestrate/SKILL.md`  
**Command Invocation**: `/speckit-orchestrate [FLAGS] [FEATURE_DESCRIPTION]`

---

## 1. Command Arguments & Flags Schema (`$ARGUMENTS`)

The orchestrator skill parses `$ARGUMENTS` for optional execution-scope flags and an optional natural-language feature description:

| Flag / Argument | Syntax | Default | Behavior |
| :--- | :--- | :--- | :--- |
| `FEATURE_DESCRIPTION` | Free-form text (non-flag tokens) | Empty | Used to run Stage 1 (`speckit-specify`) when `SPECIFY_FEATURE_DIRECTORY/spec.md` does not yet exist. Ignored (unless `--from=specify` is passed) when `spec.md` already exists. |
| `--continue` / `--continuous` | Boolean flag | `false` | Bypasses the default pre-implementation checkpoint and runs continuously through the end (`converge`). Equivalent to `--until=converge`. |
| `--pause-before-implement` | Boolean flag | `true` | Halts cleanly (`PAUSED_AT_CHECKPOINT`) before `implement`. This is the default orchestrator behavior; retained as an explicit flag for backward compatibility. |
| `--until=<stage>` | `--until=clarify\|plan\|tasks\|analyze\|implement\|converge` | `analyze` | Halts cleanly (`PAUSED_FOR_USER` / `PAUSED_AT_CHECKPOINT`) immediately after the specified stage and its gate complete. Defaults to `analyze` (pauses before `implement`) unless `--continue` or `--resume` is specified. |
| `--from=<stage>` | `--from=specify\|clarify\|plan\|tasks\|analyze\|implement\|converge` | Auto-detect | Forces execution to start at `<stage>`, regenerating its artifacts even if they already exist on disk. |
| `--resume` | Boolean flag | `false` | Explicitly resumes an existing feature in `.specify/feature.json` from the first incomplete stage. When resuming past the pre-implementation checkpoint (`analyze` complete, `implement` pending), proceeds through `implement` and `converge`. |
| `--clarify` | Boolean flag | `false` | Forces the `Clarify Gate` to run a full `speckit-clarify` ambiguity scan subagent even if `spec.md` has 0 `[NEEDS CLARIFICATION]` markers. |
| `--model=<tier>` | `--model=inherit\|pro\|flash\|flash_lite` | Role-based | Overrides the resolved subagent model tier for all stages in this invocation. |
| `--override-ceiling` | Boolean flag | `false` | Allows `speckit-reasoner` to escalate to `pro`/`opus` even when the user's active session model is `flash`/`sonnet`. |

---

## 2. Pre-Flight & Progressive Resumption Contract

1. **Resolve Feature State**:
   - Check `SPECIFY_FEATURE_DIRECTORY` environment variable or `.specify/feature.json` (`feature_directory`).
   - If neither resolves to an existing `spec.md` and `FEATURE_DESCRIPTION` is non-empty, run Stage 1 (`specify`).
   - If neither resolves to an existing `spec.md` and `FEATURE_DESCRIPTION` is empty, **FAIL CLOSED**: emit `CRITICAL` diagnostic and instruct the user to provide a feature description or run `/speckit-specify <description>` first.
2. **Load Governance Suite**:
   - Verify `.specify/memory/constitution.md`, `.specify/memory/coding-standards.md`, and `.specify/memory/logging-standards.md`.
3. **Determine Starting Stage**:
   - If `--from=<stage>` is provided, start at `<stage>`.
   - Otherwise inspect `SPECIFY_FEATURE_DIRECTORY`:
     - `spec.md` missing → start at `specify`
     - `spec.md` exists, `plan.md` missing or empty → start at `clarify` gate → `plan`
     - `plan.md` exists, `tasks.md` missing or empty → start at `tasks`
     - `tasks.md` exists with unchecked `- [ ]` tasks → start at `analyze` gate → `implement`
     - `tasks.md` exists with all tasks `- [x]` → start at `converge`.

---

## 3. Quality Gate Contracts

### 3.1 Clarify Gate (Between `specify` and `plan`)
- **Pass Criteria**:
  1. `SPECIFY_FEATURE_DIRECTORY/spec.md` contains 0 occurrences of `[NEEDS CLARIFICATION`.
  2. `SPECIFY_FEATURE_DIRECTORY/checklists/requirements.md` exists and contains 0 unchecked `- [ ]` items.
  3. `--clarify` flag was not passed (or `speckit-clarify` returned 0 critical ambiguities).
- **Pause Behavior (`PAUSED_FOR_USER`)**:
  - Present the structured clarification questions (up to 5) to the user and stop without invoking `speckit-plan`.

### 3.2 Analyze & Self-Heal Gate (Between `tasks` and `implement`)
- **Pass Criteria**: `speckit-analyze` subagent reports 0 findings (`CRITICAL = 0`, `HIGH = 0`, `MEDIUM = 0`, `LOW = 0`).
- **Self-Heal Criteria**:
  - `CRITICAL = 0` and `HIGH = 0`, while `MEDIUM > 0` or `LOW > 0`.
  - Self-heal iteration counter `heal_iteration < 2`.
  - Action: Spawn `speckit-reasoner` remediation subagent to align `plan.md` and/or `tasks.md` (strictly preserving `spec.md` requirements and `.specify/memory/*` rules), increment `heal_iteration`, and re-run `speckit-analyze`.
- **Fail-Closed Criteria (`FAILED_CLOSED`)**:
  - Any `CRITICAL > 0` or `HIGH > 0` finding (including any violation of `.specify/memory/{constitution,coding-standards,logging-standards}.md`), OR
  - Findings remain after `heal_iteration == 2`.
  - Action: Halt immediately before `speckit-implement` and output the blocking analysis findings table.

### 3.3 Convergence Gate (After `implement`)
- **Pass Criteria**: `speckit-converge` subagent returns outcome `converged` (0 findings; `tasks.md` byte-for-byte unchanged).
- **Retry Loop Criteria**:
  - `speckit-converge` returns `tasks_appended` and `converge_iteration < 3`.
  - Action: Increment `converge_iteration`, dispatch `speckit-implement` using `speckit-reasoner` (escalated model tier) to complete the newly appended `## Phase N: Convergence` tasks, then re-run `speckit-converge`.
- **Fail-Closed Criteria (`FAILED_CLOSED`)**:
  - `speckit-converge` still returns `tasks_appended` at `converge_iteration == 3`.
  - Action: Halt and report the remaining open tasks in `tasks.md`.

---

## 4. Pipeline Execution Summary Output Contract

Every invocation of `/speckit-orchestrate` MUST conclude by rendering the following structured summary table:

```markdown
## Pipeline Execution Summary

- **Feature Directory**: `<SPECIFY_FEATURE_DIRECTORY>`
- **Session Model Ceiling**: `<Active Session Model> (<high_reasoning | standard_execution>)`
- **Overall Pipeline Status**: `<CONVERGED | PAUSED_AT_CHECKPOINT | HALTED_ON_GATE_FAILURE>`

| Stage | Status | Agent Profile | Resolved Model Tier | Iterations | Artifacts Verified / Modified |
|-------|--------|---------------|---------------------|------------|-------------------------------|
| 1. Specify | <STATUS> | <agent> | <model> | <N> | `spec.md`, `checklists/requirements.md` |
| 2. Clarify Gate | <STATUS> | <agent> | <model> | <N> | `spec.md`, `checklists/requirements.md` |
| 3. Plan | <STATUS> | <agent> | <model> | <N> | `plan.md`, `research.md`, `data-model.md`, `quickstart.md`, `contracts/` |
| 4. Tasks | <STATUS> | <agent> | <model> | <N> | `tasks.md` |
| 5. Analyze Gate | <STATUS> | <agent> | <model> | <N/2> | `plan.md`, `tasks.md` (Analysis Report) |
| 6. Implement | <STATUS> | <agent> | <model> | <N/3> | `tasks.md` + repository files |
| 7. Converge | <STATUS> | <agent> | <model> | <N/3> | `tasks.md` (`converged` / `tasks_appended`) |

### Next Action
- <Actionable next step or resume command>
```
