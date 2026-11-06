---
name: "speckit-orchestrate"
description: "Coordinate context-isolated subagents across clarify, plan, tasks, analyze, implement, and converge"
compatibility: "Requires spec-kit project structure with .specify/ directory"
metadata:
  author: "github-spec-kit"
  source: "templates/commands/orchestrate.md"
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Pre-Execution Checks

**Check for extension hooks (before orchestration)**:
- Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_orchestrate` key.
- If the YAML cannot be parsed or is invalid, do not skip silently: tell the user that `.specify/extensions.yml` could not be read (include the parser error) and that no hooks were checked, including any mandatory (`optional: false`) hooks registered there, then continue normally.
- Filter out hooks where `enabled` is explicitly `false`. Treat hooks without an `enabled` field as enabled by default.
- For each remaining hook, do **not** attempt to interpret or evaluate hook `condition` expressions:
  - If the hook has no `condition` field, or it is null/empty, treat the hook as executable.
  - If the hook defines a non-empty `condition`, skip the hook.
- When constructing command invocations from hook command names, replace dots (`.`) with hyphens (`-`).
- For each executable hook, output the prompt or emit `EXECUTE_COMMAND:` and run mandatory hooks as required.
- If no hooks are registered or `.specify/extensions.yml` does not exist, skip silently.

## Anti-Recursion Invariant

When running as a subagent or child process (`ORCHESTRATOR_CHILD=true`):
- NEVER invoke `/speckit-orchestrate` or trigger `hooks.after_specify` recursively.
- Always propagate `ORCHESTRATOR_CHILD=true` down to any subagent dispatch payloads.

## Architectural Replanning & Preservation Invariants

When running in replanning mode (`IS_UPDATE_MODE=true` via `--update` or `--amend`):
- **Replanning State Variables**:
  - `IS_UPDATE_MODE`: Boolean flag indicating whether replanning mode is active (`true` if `--update` or `--amend` is passed; `false` otherwise).
  - `UPDATE_DESCRIPTION`: Sanitized natural-language string capturing the requested architectural modifications. Required when `IS_UPDATE_MODE=true`; must be non-empty after trimming with bounding single or double quotes stripped.
- **Task Monotonicity Invariant (VR-04)**:
  - For all task items in `tasks.md` where status is completed (`- [x]`) prior to the `--update` invocation:
    - Post-condition: Status MUST remain strictly completed (`- [x]`), and task line content/numbering MUST remain intact verbatim.
    - Completed tasks MUST NEVER be reset to pending (`- [ ]`), deleted, or renumbered.
- **Artifact Preservation Invariant**:
  - Existing planning documents (`spec.md`, `plan.md`, `research.md`, `data-model.md`, `quickstart.md`, `contracts/`) MUST NOT be reinitialized from blank templates.
  - Amendments MUST be applied surgically in place: preserving prior valid decisions, updating technical context, appending research evaluations, adding or updating data entities and contracts, and adjusting pending tasks or appending new update phases.
- **Core Skill Immutability Invariant (VR-05)**:
  - The core planning skill (`speckit-plan/SKILL.md`) in `.agents/` and `.claude/` MUST remain 100% unmodified. Replanning guidance is injected dynamically via subagent dispatch payloads rather than mutating the core skill template.

---

## Outline

### 1. Argument Parsing & Runtime Scope Resolution

Parse `$ARGUMENTS` for execution-scope flags, overrides, replanning parameters, and free-form feature description:

#### Replanning Flags (`--update` / `--amend`)
- **Flag Extraction**: Match `--update` or `--amend` using the following patterns in order:
  1. Quoted parameter: `--update=['"](?P<desc>[^'"]+)['"]` or `--amend=['"](?P<desc>[^'"]+)['"]`
  2. Unquoted assignment: `--update=(?P<desc>[^\s]+)` or `--amend=(?P<desc>[^\s]+)`
  3. Space-separated: `--update\s+(?P<desc>[^-\s][^-\n]*)` or `--amend\s+(?P<desc>[^-\s][^-\n]*)` (capturing non-flag tokens up to the next `--flag` or end of string)
- **Flag Normalization**:
  - If `--update` or `--amend` is present:
    - Set `IS_UPDATE_MODE = true`.
    - Extract `<desc>`. If `<desc>` is enclosed in matching bounding single (`'`) or double (`"`) quotes, strip the bounding quotes.
    - Trim leading and trailing whitespace.
    - Assign to canonical variable `UPDATE_DESCRIPTION`.
    - Constraint: Required if `IS_UPDATE_MODE == true`; trimmed; length > 0; bounding quotes stripped.
  - If neither is present:
    - Set `IS_UPDATE_MODE = false` and `UPDATE_DESCRIPTION = ""`.

#### Flag Precedence & Interaction Handling
- **Precedence with `--from=<stage>`**:
  - When `--from=<stage>` is supplied together with `--update` / `--amend`, `--from` selects the starting lifecycle stage (`specify`, `plan`, `tasks`, etc.) while strictly preserving `--update` non-destructive replanning semantics.
  - Unlike a clean run where `--from` may wipe or reinitialize files, in replanning mode (`IS_UPDATE_MODE == true`), all stages starting from `--from` perform in-place, non-destructive amendments (preserving prior decisions and completed `- [x]` tasks).
  - Defaults to Stage 3 (`plan`) if `--from` is omitted during replanning, unless `spec.md` updates are specifically indicated (`--from=specify`).
- **Interaction with Checkpoint & Continuation Flags**:
  - Pre-implementation pause after Stage 5 (`analyze`) remains active by default during replanning, allowing human review of amended `plan.md` and `tasks.md` before any code changes.
  - Providing `--continue` / `--continuous` alongside `--update` bypasses this checkpoint and runs through Stage 6 (`implement`) and Stage 7 (`converge`).

#### Standard Execution & Scope Flags
- **Default Checkpoint Policy**: Pauses cleanly after `analyze` before code implementation (`implement`), allowing human review of `plan.md` and `tasks.md`.
- `--continue` / `--continuous` (aliases: `--no-pause`, `--auto-implement`): Bypasses the pre-implementation pause, running continuously through the end (`converge`). Equivalent to `--until=converge`.
- `--pause-before-implement`: Explicit alias for default behavior (halts cleanly after `analyze` before `implement`). Retained for backward compatibility.
- `--until=<stage>`: Halts cleanly immediately after `<stage>` completes (`clarify`, `plan`, `tasks`, `analyze`, `implement`, `converge`). Defaults to `analyze` (pausing before implement) unless `--continue`/`--continuous` or `--resume` is specified.
- `--from=<stage>`: Forces execution to start at `<stage>` (`specify`, `clarify`, `plan`, `tasks`, `analyze`, `implement`, `converge`).
- `--resume`: Resumes from the first incomplete stage on an existing feature. When resuming after the pre-implementation pause (`analyze` complete, `implement` pending), resumes directly into Stage 6 (`implement`) and runs through `converge` (unless constrained by `--until=<stage>`).
- `--clarify`: Forces full `speckit-clarify` subagent pass even if `[NEEDS CLARIFICATION]` marker count is 0.
- `--model=<tier>`: Explicit subagent model override (`inherit`, `pro`, `flash`, `flash_lite`, `opus`, `sonnet`).
- `--override-ceiling`: Allows escalating subagents to high-reasoning models (`pro`, `opus`) even when session ceiling is standard (`flash`, `sonnet`).
- `FEATURE_DESCRIPTION`: Any remaining non-flag text tokens (when not in replanning mode).

### 2. Feature Directory & Authoritative State Resolution

Resolve authoritative feature context:
1. **Replanning Description Guard (VR-01)**:
   - If `is_update_mode == true` and `trim(update_description) == ""`:
     - **FAIL CLOSED** (`FAILED_CLOSED`). Log `CRITICAL` diagnostic:
       ```text
       CRITICAL: --update / --amend requires a non-empty description of architectural changes.
       Usage examples:
         /speckit-orchestrate --update='Add Redis caching to session store'
         /speckit-orchestrate --amend "Migrate schema to PostgreSQL"
       ```
     - Halt execution immediately; zero files created or mutated, no subagents dispatched.

2. Check `SPECIFY_FEATURE_DIRECTORY` environment variable, or read `.specify/feature.json` (`feature_directory`).
3. **Replanning Feature Directory Guard (VR-02)**:
   - If `is_update_mode == true` and `feature_dir` cannot be resolved:
     - **FAIL CLOSED** (`FAILED_CLOSED`). Log `CRITICAL` diagnostic:
       ```text
       CRITICAL: Cannot execute --update without an active feature directory.
       Ensure SPECIFY_FEATURE_DIRECTORY is set or .specify/feature.json points to an existing feature.
       ```
     - Halt execution immediately; no subagents dispatched.

4. If `feature_directory` exists:
   - Resolve absolute path: e.g. `/home/admin/projects/spec-kit-testing/specs/<feature-name>`.
   - **Replanning Architectural Baseline Guard (VR-03)**:
     - If `is_update_mode == true` and (`spec.md` does not exist OR `plan.md` does not exist):
       - Determine `{MISSING_ARTIFACTS_LIST}` (e.g. `spec.md`, `plan.md`, or `spec.md, plan.md`).
       - **FAIL CLOSED** (`FAILED_CLOSED`). Log `CRITICAL` diagnostic:
         ```text
         CRITICAL: Cannot execute --update because required baseline artifacts are missing in {FEATURE_DIR}.
         Missing artifact(s): {MISSING_ARTIFACTS_LIST}.
         An architectural update requires an existing spec.md and plan.md baseline. For new features, run /speckit-orchestrate without --update.
         ```
       - Halt execution immediately; zero files created or overwritten.
   - For forward (non-update) runs: verify existence of `spec.md`.

5. If neither resolves to an existing feature directory:
   - If `FEATURE_DESCRIPTION` is provided: Stage 1 (`specify`) will initialize a new feature directory.
   - If `FEATURE_DESCRIPTION` is empty: **FAIL CLOSED** (`FAILED_CLOSED`). Log `CRITICAL` diagnostic:
     `"CRITICAL: No active feature found in .specify/feature.json or SPECIFY_FEATURE_DIRECTORY, and no feature description provided. Provide a feature description to /speckit-orchestrate <description> or run /speckit-specify first."`
     Halt execution immediately.
6. Pass `SPECIFY_FEATURE_NO_PERSIST=1` to all downstream child stage invocations after feature directory creation.

### 3. Governance Suite Adherence & Dynamic Principle III Policy Resolution

Read and inspect project governance suite before dispatching subagents:
- `.specify/memory/constitution.md`
- `.specify/memory/coding-standards.md` (if present)
- `.specify/memory/logging-standards.md` (if present)

**Fail-Closed Governance Check (Principle II)**:
If `.specify/memory/constitution.md` is missing or unreadable, the orchestrator MUST **FAIL CLOSED** (`FAILED_CLOSED`). Log `CRITICAL` diagnostic:
`"CRITICAL: .specify/memory/constitution.md is missing or unreadable. Ratify project constitution first using /speckit-constitution."`
Halt execution immediately.

**Governance Policy Adherence**:
Subagents dynamically inspect and obey `.specify/memory/constitution.md` (and companion standards where applicable), adhering to the ratified testing and verification rules without hardcoded assumptions.

### 4. Agent Profile Hierarchy & Session Model Ceiling

#### Dual-Client Resolution Hierarchy
Determine the active client root directory `<client>`:
- If running within Claude Code (or if `.agents/` is absent and `.claude/` exists), resolve from `.claude/`.
- Otherwise, resolve from `.agents/`.

Resolve subagent definitions using the 5-level override hierarchy:
1. **Runtime Flag**: `--model=<tier>` or `--agent=<name>` in `$ARGUMENTS`.
2. **Stage Local Override**: `<client>/agents/speckit-<stage>.local.md` (gitignored).
3. **Stage Tracked Override**: `<client>/agents/speckit-<stage>.md`.
4. **Role Local Override**: `<client>/agents/speckit-<role>.local.md` (gitignored).
5. **Role Tracked Default**: `<client>/agents/speckit-<role>.md` (`speckit-reasoner.md` for `reasoning`, `speckit-executor.md` for `execution`).

#### Role Capability Tiers
- **High-Reasoning (`speckit-reasoner`)**: `clarify`, `plan`, `analyze`, `converge`, self-heal remediation, and convergence retry escalations.
- **Standard/Fast Execution (`speckit-executor`)**: `specify`, `tasks`, and initial `implement` pass 1.

#### Session Model Ceiling Algorithm
- Detect active session model tier:
  - `high_reasoning`: Gemini Argon / Gemini Pro, Claude Opus.
  - `standard_execution`: Gemini Flash / Flash Lite, Claude Sonnet / Haiku.
- If session tier is `high_reasoning`:
  - `speckit-reasoner` runs with `Model: "inherit"` (or `"pro"` / `"opus"`).
  - `speckit-executor` steps down to `Model: "flash"` / `"sonnet"`.
- If session tier is `standard_execution`:
  - `speckit-reasoner` is capped at session ceiling (`Model: "inherit"` / `"flash"` / `"sonnet"`) unless `override_ceiling: true` or `--override-ceiling` is passed.
  - `speckit-executor` runs with `Model: "inherit"` / `"flash"`.

### 5. Subagent Registration & Dispatch Protocol

#### Dual-Client Subagent Dispatch
- **Google Antigravity**:
  - Register subagent personas using `define_subagent` if not already defined:
    - `Name`: `"speckit-reasoner"` or `"speckit-executor"` (or stage-specific name).
    - `Description`: Extracted from YAML frontmatter `description`.
    - `SystemPrompt`: Extracted from markdown body of agent profile.
    - `EnableWriteTools`: `true` for write stages; `false` for read-only `analyze`.
    - `EnableSubagentTools`: `false` by default (only `true` for `implement` if coordinating disjoint parallel workers).
    - `Workspace`: `"inherit"`.
  - Dispatch via `invoke_subagent`.
- **Claude Code**:
  - Dispatch via `Task` tool (using `subagent_type: speckit-reasoner` or `speckit-executor`, with `model: opus` / `sonnet` / `inherit`).
  - For read-only stages (such as `analyze`), prompt instructs the agent not to modify files.

#### Mandatory Subagent Prompt Payload
When dispatching subagents, the prompt MUST include:
```markdown
## Stage Execution Directive: {STAGE_NAME}

1. Target Skill: Read and execute {SKILL_FILE_PATH}
2. Feature Context:
   - SPECIFY_FEATURE_DIRECTORY: {FEATURE_DIR}
   - .specify/feature.json: {"feature_directory": "{REL_FEATURE_DIR}"}
   - SPECIFY_FEATURE_NO_PERSIST=1 (for all stages after initial specify)
3. Replanning Mode & Update Context (Active if IS_UPDATE_MODE == true):
   - UPDATE_ACTIVE: {IS_UPDATE_MODE}
   - UPDATE_DESCRIPTION: {UPDATE_DESCRIPTION}
   - REPLANNING_SCOPE: {STAGE_SPECIFIC_INSTRUCTION}
4. Governance Suite Adherence (Non-Negotiable):
   - Enforce .specify/memory/constitution.md (including testing and verification rules).
   - Enforce .specify/memory/coding-standards.md and .specify/memory/logging-standards.md (where applicable).
5. Hook Anti-Recursion Guard:
   - ORCHESTRATOR_CHILD=true: Do NOT invoke /speckit-orchestrate from any hooks.
6. Required Completion Report:
   Return structured summary:
   - STAGE_STATUS: SUCCESS | PAUSED_FOR_USER | FAILED
   - ARTIFACTS_TOUCHED: <comma-separated list of paths>
   - GATE_DATA: <checklist results, finding counts, or convergence outcome>
   - DIAGNOSTICS: <summary of log messages>
```

**Stage-Specific `REPLANNING_SCOPE` Injections** (when `IS_UPDATE_MODE == true`):
- **Stage 1 (Specify)**:
  `Update spec.md in place to incorporate new or modified requirements arising from: "{UPDATE_DESCRIPTION}". Retain existing user stories, priority classifications, and constitutional quality gates. Do not wipe or reset existing acceptance criteria unless directly superseded.`
- **Stage 3 (Plan)**:
  `Perform surgical, in-place non-destructive architectural replanning across plan.md, research.md, data-model.md, quickstart.md, and contracts/ to incorporate: "{UPDATE_DESCRIPTION}". DO NOT reinitialize artifacts from blank templates. Update Technical Context in plan.md with new technology choices, dependencies, and constraints. Append new research evaluations (Decision, Rationale, Alternatives considered) to research.md. Update or add entity schemas in data-model.md. Update or add interface contracts in contracts/. Update validation procedures in quickstart.md. Retain all prior valid architectural decisions and rationales.`
- **Stage 4 (Tasks)**:
  `Update tasks.md in place to reflect the amended architecture for: "{UPDATE_DESCRIPTION}". PRESERVATION INVARIANT: You MUST preserve 100% of completed task items (- [x]) verbatim. Do not delete, renumber, or mark incomplete any completed work. Append a new phase (e.g., "## Phase N: Architectural Update - {UPDATE_DESCRIPTION}") or surgically adjust remaining pending tasks (- [ ]) in existing phases to implement the amended architecture.`
- **Stage 5 (Analyze Gate)**:
  `Perform non-destructive cross-artifact consistency analysis across amended spec.md, plan.md, and tasks.md. Validate that new tasks in tasks.md map directly to amended requirements and designs without drift.`

### 6. Pipeline Execution State Machine

Execute stages sequentially under single-writer serialization (with skills dynamically resolved from `<client>/skills/<skill-name>/SKILL.md`):

#### Stage 1: Specify
- **Agent**: `speckit-executor` (`execution`)
- **Skill**: `<client>/skills/speckit-specify/SKILL.md`
- **Condition**: Run if `spec.md` is missing, or `--from=specify` is specified.
  - When `is_update_mode == true` and `--from=specify` is explicitly requested (or requirements need modification), amend `spec.md` in place to incorporate `UPDATE_DESCRIPTION`. Retain existing user stories, priority classifications, and constitutional quality gates without wiping or resetting existing acceptance criteria unless directly superseded (FR-005).
- **Check**: Verify `spec.md` and `checklists/requirements.md` created or updated.
- **Anti-Recursion**: Pass `ORCHESTRATOR_CHILD=true` so `hooks.after_specify` does not re-trigger orchestrator.
- Check `--until=specify`: if true, halt cleanly.

#### Stage 2: Clarify Gate
- **Agent**: `speckit-reasoner` (`reasoning`)
- **Inspection**:
  - Scan `spec.md` for occurrences of `[NEEDS CLARIFICATION]`.
  - Scan `checklists/requirements.md` for unchecked `- [ ]` items.
  - Check if `--clarify` flag was set.
- **Gate Evaluation**:
  - If `[NEEDS CLARIFICATION]` > 0, checklist has unchecked items, or `--clarify` is true:
    - Run `speckit-clarify` subagent (`<client>/skills/speckit-clarify/SKILL.md`) to generate targeted questions.
    - If ambiguities require human input: **PAUSE FOR USER** (`PAUSED_FOR_USER`).
      Present clarification questions and stop without proceeding to `plan`.
  - If 0 ambiguities and checklist PASS: mark Clarify Gate `PASSED`.
- Check `--until=clarify`: if true, halt cleanly.

#### Stage 3: Plan
- **Agent**: `speckit-reasoner` (`reasoning`)
- **Skill**: `<client>/skills/speckit-plan/SKILL.md`
- **Condition**: Run if `plan.md` is missing/empty, or `--from=plan` (or earlier) was specified, OR if `is_update_mode == true` (forces execution even if `plan.md` exists and is non-empty). Skip only during standard forward runs when `plan.md` already exists and is non-empty.
- **Replanning Execution (`is_update_mode == true`)**:
  - Perform surgical, in-place non-destructive architectural replanning across `plan.md`, `research.md`, `data-model.md`, `quickstart.md`, and `contracts/` to incorporate `UPDATE_DESCRIPTION`.
  - DO NOT reinitialize artifacts from blank templates.
  - Retain baseline architectural decisions and prior rationales. Update Technical Context in `plan.md` with new technology choices, dependencies, and constraints.
  - Append new research evaluations to `research.md`.
  - Update or add entity schemas in `data-model.md` and interface contracts in `contracts/`.
  - Update validation procedures in `quickstart.md`.
- **Verification**: Verify `plan.md`, `research.md`, `data-model.md`, `quickstart.md`, and contracts exist and reflect the architectural updates.
- Check `--until=plan`: if true, halt cleanly.

#### Stage 4: Tasks
- **Agent**: `speckit-executor` (`execution`)
- **Skill**: `<client>/skills/speckit-tasks/SKILL.md`
- **Condition**: Run if `tasks.md` is missing/empty, or `--from=tasks` (or earlier) was specified, OR if `is_update_mode == true` (forces execution even if `tasks.md` exists and is non-empty). Skip only during standard forward runs when `tasks.md` already exists and is non-empty.
- **Replanning Execution & Task Preservation (`is_update_mode == true`)**:
  - Enforce constraint **VR-04 (Strict Monotonicity)**: You MUST preserve 100% of completed task items (`- [x]`) verbatim. Never delete, renumber, or reset completed tasks to pending (`- [ ]`).
  - Pending tasks (`- [ ]`) may be adjusted or pruned if obsolete.
  - Append a new phase (e.g., `## Phase N: Architectural Update - <update_description>`) or surgically adjust remaining pending tasks (`- [ ]`) in existing phases to implement the amended architecture.
- **Verification**: Verify `tasks.md` contains dependency-ordered phases and tasks, and confirms zero regressions to completed `- [x]` items.
- Check `--until=tasks`: if true, halt cleanly.

#### Stage 5: Analyze & Self-Heal Gate
- **Agent**: `speckit-reasoner` (`reasoning`)
- **Skill**: `<client>/skills/speckit-analyze/SKILL.md`
- **Execution**: Run `speckit-analyze` to perform non-destructive consistency check across `spec.md`, `plan.md`, and `tasks.md`.
  - In replanning mode (`is_update_mode == true`), validate that amended design artifacts and new tasks in `tasks.md` align with `spec.md` and the updated architecture with zero drift.
- **Gate Evaluation**:
  - If `CRITICAL > 0` or `HIGH > 0`:
    - **FAIL CLOSED** (`FAILED_CLOSED`). Halt immediately. Output blocking findings table.
  - If `MEDIUM > 0` or `LOW > 0` (drift detected):
    - If `heal_iteration < 2`:
      - Dispatch remediation subagent (`speckit-reasoner`) to align `plan.md` and/or `tasks.md` with `spec.md` (while strictly preserving completed `- [x]` tasks in `tasks.md` under VR-04).
      - Increment `heal_iteration`.
      - Re-run `speckit-analyze`.
    - If `heal_iteration >= 2` and drift persists:
      - **FAIL CLOSED** (`FAILED_CLOSED`). Halt and report unresolved drift.
  - If findings == 0:
    - Mark gate `PASSED` (or `SELF_HEALED` if remediated).
- **Pre-Implementation Checkpoint Policy**:
  - Enforce constraint: `PAUSE_AT_CHECKPOINT` (default) or `CONTINUOUS` (if `--continue` / `--continuous`):
  - Check whether to halt before Stage 6 (`implement`):
    - If `--continue` / `--continuous` / `--no-pause` / `--auto-implement` is passed, OR `--until=implement` or `--until=converge` was explicitly specified, OR execution was triggered via `--resume`:
      - Proceed to Stage 6: `implement`.
    - Otherwise (Default behavior, or if `--pause-before-implement` or `--until=analyze` was passed, including replanning mode without `--continue`):
      - **PAUSE FOR USER** (`PAUSED_AT_CHECKPOINT`).
      - In replanning mode, output checkpoint status:
        ```text
        Paused at Pre-Implementation Checkpoint. Architectural replanning is complete. Review amended plan.md and tasks.md before proceeding.
        ```
      - Instruct user to review `plan.md` and `tasks.md`, then resume with `/speckit-orchestrate --resume` (or run continuously with `/speckit-orchestrate --continue`).

#### Stage 6: Implement
- **Agent**: `speckit-executor` (`execution` for pass 1) / `speckit-reasoner` (`reasoning` for retries 2..3)
- **Skill**: `<client>/skills/speckit-implement/SKILL.md`
- **Safe Concurrency & Single Coordinator**:
  - Sequential tasks execute in dependency order.
  - Parallel tasks marked `[P]` within the same phase are validated for mutually disjoint file paths before concurrent dispatch.
  - All `tasks.md` checkbox markers (`- [x]`) are updated exclusively by the coordinator or executing subagent under single-writer serialization.
- Check `--until=implement`: if true, halt cleanly.

#### Stage 7: Converge
- **Agent**: `speckit-reasoner` (`reasoning`)
- **Skill**: `<client>/skills/speckit-converge/SKILL.md`
- **Execution & Retry Loop**:
  - Run `speckit-converge` to inspect repository against `spec.md`, `plan.md`, and `tasks.md`.
  - If outcome == `converged`:
    - Pipeline is complete! Overall status: `CONVERGED`.
  - If outcome == `tasks_appended`:
    - If `converge_iteration < 3`:
      - Increment `converge_iteration`.
      - Escalate to `speckit-reasoner` (High-Reasoning model) to execute the newly appended `## Phase N: Convergence` tasks in `tasks.md` via `speckit-implement`.
      - Re-run Stage 7 `converge`.
    - If `converge_iteration >= 3` and convergence still not reached:
      - **FAIL CLOSED** (`FAILED_CLOSED`). Log `CRITICAL` diagnostic and report unbuilt work.

---

## Post-Execution Hooks

Check if `.specify/extensions.yml` exists in project root.
- Read entries under `hooks.after_orchestrate` (if any).
- Filter out hooks with `enabled: false`.
- If mandatory hooks exist (`optional: false`), emit `EXECUTE_COMMAND:` and execute them.
- If optional hooks exist (`optional: true`), display prompt and command.

---

## Completion Report & Pipeline Summary

Output the structured Pipeline Execution Summary based on execution mode:

### Replanning Mode (`IS_UPDATE_MODE == true`)

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

### Standard Forward Run Mode (`IS_UPDATE_MODE == false`)

```markdown
## Pipeline Execution Summary

- **Feature Directory**: `{FEATURE_DIRECTORY}`
- **Session Model Ceiling**: `{SESSION_MODEL} ({SESSION_TIER})`
- **Overall Pipeline Status**: `{OVERALL_STATUS}`

| Stage | Status | Agent Profile | Resolved Model Tier | Iterations | Artifacts Verified / Modified |
|-------|--------|---------------|---------------------|------------|-------------------------------|
| 1. Specify | {STATUS} | {AGENT} | {MODEL} | {N} | `spec.md`, `checklists/requirements.md` |
| 2. Clarify Gate | {STATUS} | {AGENT} | {MODEL} | {N} | `spec.md`, `checklists/requirements.md` |
| 3. Plan | {STATUS} | {AGENT} | {MODEL} | {N} | `plan.md`, `research.md`, `data-model.md`, `quickstart.md`, `contracts/` |
| 4. Tasks | {STATUS} | {AGENT} | {MODEL} | {N} | `tasks.md` |
| 5. Analyze Gate | {STATUS} | {AGENT} | {MODEL} | {N/2} | `plan.md`, `tasks.md` (Analysis Report) |
| 6. Implement | {STATUS} | {AGENT} | {MODEL} | {N/3} | `tasks.md` + repository files |
| 7. Converge | {STATUS} | {AGENT} | {MODEL} | {N/3} | `tasks.md` (`converged` / `tasks_appended`) |

### Next Action
- {ACTIONABLE_NEXT_STEP}
```
