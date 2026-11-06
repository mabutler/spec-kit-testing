# Phase 0 Research: Non-Destructive Architectural Replanning via `--update` / `--amend` Flag

**Feature**: `011-orchestrate-update-flag`  
**Date**: 2026-11-06  
**Status**: Completed  

---

## 1. CLI Argument Parsing and Syntax Normalization

### Context & Problem
Users invoke `/speckit-orchestrate` through diverse terminal shells and AI chat interfaces (Google Antigravity, Claude Code), leading to syntactic variations in flag usage. The feature requires supporting both `--update` and `--amend` with quote styles (`--update='...'`, `--update="..."`, `--amend='...'`) and space-separated values (`--update <description>`, `--amend <description>`).

### Decision
Implement regex-based and token-based extraction in the orchestrator outline (`Outline -> 1. Argument Parsing & Runtime Scope Resolution`) supporting:
- Flag formats:
  - `--update='<text>'` and `--update="<text>"`
  - `--update=<text>` (unquoted single token)
  - `--update <text>` (space-separated; grabs remaining argument string or next tokens until the next flag)
  - `--amend='<text>'` and `--amend="<text>"`
  - `--amend=<text>`
  - `--amend <text>`
- Sanitization: Strip bounding single/double quotes, trim leading/trailing whitespace, and assign the parsed value to the `UPDATE_DESCRIPTION` context variable.
- Mode indicator: Set `IS_UPDATE_MODE=true` whenever `--update` or `--amend` is present.

### Rationale
- Normalizing both flag names (`--update` and `--amend`) to a canonical `UPDATE_DESCRIPTION` and `IS_UPDATE_MODE` flag avoids branching in downstream stage logic.
- Permitting both equals-separated and space-separated parameters ensures full compatibility with POSIX conventions and LLM slash-command invocations.

### Alternatives Considered
- *Strict equals-separated only (`--update=<desc>`)*: Rejected because users frequently type space-separated arguments in natural language conversational interfaces, resulting in avoidable syntax errors.
- *Separate workflows for `--update` vs `--amend`*: Rejected because they are semantically identical operations; maintaining one unified code path eliminates code duplication and behavior drift.

---

## 2. Fail-Closed Boundary Validation on Missing Prerequisites

### Context & Problem
Under standard execution, `/speckit-orchestrate` can initialize a feature from scratch (Stage 1 `specify`) if `spec.md` is absent. However, an architectural *update* (`--update` / `--amend`) fundamentally requires an existing architectural baseline. Attempting to update a non-existent feature or an un-planned feature causes corrupted state, empty diffs, or accidental cold starts.

### Decision
In Section 2 (`Feature Directory & Authoritative State Resolution`), add explicit fail-closed precondition checks when `IS_UPDATE_MODE=true`:
1. **Description Check**: If `UPDATE_DESCRIPTION` is empty or consists purely of whitespace, abort immediately.
   - Severity: `CRITICAL`
   - Log message: `"CRITICAL: --update / --amend requires a non-empty description of architectural changes (e.g., /speckit-orchestrate --update='Add Redis caching to session store')."`
2. **Feature Directory Check**: If no active feature directory can be resolved via `SPECIFY_FEATURE_DIRECTORY` or `.specify/feature.json`, abort immediately.
   - Severity: `CRITICAL`
   - Log message: `"CRITICAL: Cannot execute --update without an active feature directory. Specify a valid feature via SPECIFY_FEATURE_DIRECTORY or .specify/feature.json."`
3. **Prerequisite Files Check**: Verify that both `${FEATURE_DIR}/spec.md` and `${FEATURE_DIR}/plan.md` exist on disk. If either is missing, abort immediately without dispatching subagents or modifying any files.
   - Severity: `CRITICAL`
   - Log message: `"CRITICAL: Cannot execute --update because required baseline artifacts are missing in {FEATURE_DIR}. Expected both spec.md and plan.md. For new features, run standard /speckit-orchestrate without --update."`

### Rationale
- Complies strictly with Constitution Principle II (*Explicit Error Handling & Fail-Closed State*) and Principle VI (*Verify Before Mutate/Destroy*).
- Prevents accidental overwrite of un-planned specifications or unintended initialization of empty plans.

### Alternatives Considered
- *Auto-fallback to standard generation if plan.md is missing*: Rejected because silent fallback violates Principle II; the user explicitly requested an *update* to an existing architecture, so proceeding with a blank slate could discard unstated user intent.
- *Warn and proceed*: Rejected because downstream stages depend on diffing and amending existing structures; continuing without `plan.md` guarantees failure in later stages.

---

## 3. Subagent Prompt Augmentation vs. Skill File Modification

### Context & Problem
FR-007 explicitly mandates that core planning skill files (`.agents/skills/speckit-plan/SKILL.md` and `.claude/skills/speckit-plan/SKILL.md`) remain unmodified. The orchestrator must instruct subagents to execute surgical, non-destructive edits without altering the underlying skill definition templates.

### Decision
Inject a dedicated `Update Context (Replanning Mode)` block into the subagent dispatch prompt payload in Section 5 (`Mandatory Subagent Prompt Payload`) of `speckit-orchestrate/SKILL.md` when `IS_UPDATE_MODE=true`:
```markdown
3. Update Context (Replanning Mode):
   - UPDATE_ACTIVE: true
   - UPDATE_DESCRIPTION: {UPDATE_DESCRIPTION}
   - REPLANNING_DIRECTIVE: Perform in-place, non-destructive architectural amendments. Do not wipe or reinitialize existing design artifacts from blank templates. Preserve completed work, existing rationale, and validated constraints while updating components affected by UPDATE_DESCRIPTION.
```
In Stage 3 (`plan`), the prompt explicitly instructs `speckit-reasoner` to read existing `plan.md`, `research.md`, `data-model.md`, `quickstart.md`, and `contracts/`, and apply surgical additions/modifications.
In Stage 4 (`tasks`), the prompt explicitly instructs `speckit-executor` to preserve all `- [x]` items and append or update `- [ ]` items.

### Rationale
- Subagent dispatch prompts are dynamic execution payloads evaluated by high-reasoning LLMs (`speckit-reasoner` and `speckit-executor`), which excel at following specialized directive contexts.
- Keeps core skills clean, generic, and decoupled from orchestrator-specific replanning mechanisms.
- Satisfies FR-007, FR-006, and FR-008 completely.

### Alternatives Considered
- *Add an `--update` flag directly to `speckit-plan`*: Rejected by explicit user requirement and FR-007 ("Leave core speckit-plan skill unmodified").
- *Create a separate `speckit-replan` skill*: Rejected because it introduces toolchain fragmentation and duplicate skill maintenance across `.agents` and `.claude`.

---

## 4. Artifact Preservation Semantics Across Stages

### Context & Problem
During a cold restart or `--from=plan`, standard orchestrator execution assumes missing or recreated artifacts. Under `--update`, existing artifacts (`spec.md`, `plan.md`, `research.md`, `data-model.md`, `quickstart.md`, `contracts/`, `tasks.md`) already hold significant value, and completed tasks (`- [x]`) represent already implemented and verified code.

### Decision
Define explicit per-stage preservation and modification rules:
- **`spec.md` (Stage 1 / Stage 2)**:
  - If `UPDATE_DESCRIPTION` alters user requirements or acceptance criteria, `spec.md` is updated in place to incorporate new/revised requirements (FR-005). Existing user stories, acceptance criteria, and constitution gates are preserved.
- **`plan.md` & Design Artifacts (Stage 3 `plan`)**:
  - Stage condition updated: Standard execution skips Stage 3 if `plan.md` exists and is non-empty. In `--update` mode, Stage 3 is explicitly forced to execute.
  - Subagent amends `plan.md` Technical Context, Architecture, and Project Structure in place.
  - Subagent appends new research findings to `research.md`, updates entity schemas in `data-model.md`, updates interface definitions in `contracts/`, and updates test procedures in `quickstart.md`. Existing valid sections are retained.
- **`tasks.md` (Stage 4 `tasks`)**:
  - Stage condition updated: Standard execution skips Stage 4 if `tasks.md` exists and is non-empty. In `--update` mode, Stage 4 is explicitly forced to execute.
  - Subagent scans existing `tasks.md` for completed tasks (`- [x]`).
  - All `- [x]` task lines, task numbers, and phase headings containing completed work are preserved verbatim.
  - New tasks required by the updated architecture are appended as a new phase (e.g. `## Phase N: Architectural Update - <Description>`) or merged into remaining incomplete (`- [ ]`) phases.
- **`analyze` (Stage 5 `analyze`)**:
  - Runs cross-artifact consistency analysis across the amended `spec.md`, `plan.md`, and `tasks.md` to ensure zero drift.

### Rationale
- Complies with Constitution Principle IV (*State Ownership & Single Source of Truth*) and Principle VI (*Resource Ceilings & Safe State Mutation*).
- Guarantees zero loss of progress on active features.

### Alternatives Considered
- *Overwriting `tasks.md` with all new tasks*: Rejected because completed tasks (`- [x]`) provide an audit trail of implemented code; resetting them would cause duplicate implementation or orphaned code.
- *Creating parallel files (e.g. `plan.update.md`, `tasks.update.md`)*: Rejected because it violates Principle IV (competing sidecars and multiple sources of truth).

---

## 5. Pre-Implementation Checkpoint Policy and Continuation Semantics

### Context & Problem
Architectural replanning introduces substantial modifications to system design and task sequencing. Developers require visibility into these changes before subagents begin executing implementation tasks in code.

### Decision
Enforce the default Pre-Implementation Checkpoint after Stage 5 (`analyze`) during `--update` runs:
- If `--continue` (or aliases `--continuous`, `--no-pause`, `--auto-implement`) is NOT passed:
  - Pause pipeline execution with status `PAUSED_AT_CHECKPOINT`.
  - Output summary of amended design documents and new tasks.
  - Present explicit resume instructions: `/speckit-orchestrate --resume` or `/speckit-orchestrate --continue`.
- If `--continue` (or aliases) IS passed:
  - Automatically proceed through Stage 6 (`implement`) and Stage 7 (`converge`).
- Precedence with `--from=<stage>` and `--until=<stage>`:
  - `--from=<stage>` selects the start stage (e.g. `--from=tasks` with `--update` re-runs tasks amendment only). If `--from` is omitted, `--update` starts at Stage 2 (Clarify) or Stage 3 (Plan) as appropriate.
  - `--until=<stage>` halts after `<stage>` completes.

### Rationale
- Satisfies FR-010, User Story 1, and User Story 4.
- Maintains safe human-in-the-loop control over architectural changes while allowing automated CI or power-user flows via `--continue`.

### Alternatives Considered
- *Always auto-implement on `--update`*: Rejected because architectural changes carry high risk of regression; human review is critical before code changes occur.
- *Disallow `--continue` with `--update`*: Rejected because automated test runs and headless pipelines need a continuous execution option.

---

## 6. Dual-Client Skill Parity (.agents and .claude)

### Context & Problem
This repository maintains identical capabilities across Google Antigravity ([`.agents/`](.agents/)) and Claude Code ([`.claude/`](.claude/)). Any change to `.agents/skills/speckit-orchestrate/SKILL.md` must be mirrored exactly to `.claude/skills/speckit-orchestrate/SKILL.md`.

### Decision
Implement the modifications to `.agents/skills/speckit-orchestrate/SKILL.md`, and copy/mirror the file to `.claude/skills/speckit-orchestrate/SKILL.md`.
Validate complete identity using `diff -u` and `cmp -s`.

### Rationale
- Satisfies FR-011 and Constitution Principle VII (*Code Standards, Consistent Terminology*).
- Prevents cross-client behavior drift.

### Alternatives Considered
- *Symlinks*: Rejected because symlinks are not universally supported across Windows Git checkouts or packaging archives.

---

## 7. Documentation Impact & Principle VII Compliance

### Context & Problem
Constitution Principle VII and `.specify/memory/coding-standards.md` mandate that any change classified as `USER_FACING` in `plan.md` (such as adding or modifying CLI flags or agent skill capabilities) must update `README.md` in the same pull request.

### Decision
- Classify `plan.md` documentation impact as `USER_FACING`.
- Update repository root `README.md` under `## Spec Kit Skills & Subagent Orchestration Reference -> ### Custom Skills` to document `/speckit-orchestrate --update='<description>'` (and alias `--amend`) alongside existing flags (`--continue`, `--resume`, `--from`).

### Rationale
- Fully satisfies Principle VII and Coding Standards documentation gates.
- Ensures developer documentation accurately reflects the new replanning capability.

### Alternatives Considered
- *Defer README update to a separate PR*: Prohibited by Constitution Principle VII.
