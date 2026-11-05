# Contract: Dynamic Constitutional Deference for Verification & Testing

**Feature Branch**: `007-claude-discovery-governance-decoupling`  
**Date**: 2026-11-05  
**Traces**: `FR-006`, `FR-007`, `FR-008`, `SC-003`

## 1. Subagent Persona Governance Contract (`FR-006`, `SC-003`)

Applies to:
- `.agents/agents/speckit-executor.md` and `.claude/agents/speckit-executor.md`
- `.agents/agents/speckit-reasoner.md` and `.claude/agents/speckit-reasoner.md`

### Required Frontmatter & Dual-Client Compatibility
- The YAML frontmatter MUST use schema valid across both Claude Code and Antigravity:
  - `name`: string (required)
  - `description`: string (required)
  - `model`: string (`sonnet` for executor, `opus` for reasoner, or `inherit`)
  - `speckit_role_tier`: string (`execution` or `reasoning`)
  - `speckit_default_stages`: list of strings
  - `speckit_tool_policy`: map of Antigravity-specific flags (`enable_write_tools`, `enable_subagent_tools`, `enable_mcp_tools`)
  - Note: Do NOT use a top-level nested `tools:` object, as Claude Code requires `tools` to be an allowlist string/list if present. Omission of top-level `tools` means Claude Code grants default tools to the agent.

### Required Persona Header & Environment Neutrality
- The persona introduction MUST identify the subagent as operating within **Google Antigravity or Claude Code** (not exclusively Google Antigravity).

### Required Principle III Clause in `Core Governance & Operational Rules`
- **Prohibited Hardcoded Text**: Must NOT contain `"Principle III (Static Verification & Zero Automated Tests)"` or `"Do NOT generate unit tests, test suites, test harnesses, mock frameworks, or automated test files anywhere in the workspace"`.
- **Required Dynamic Deference Clause**:
  - **In `speckit-executor.md` and `speckit-reasoner.md`**:
    ```markdown
    - **Principle III (Verification & Testing Governance)**: Dynamically inspect and obey the verification, testing, and coverage requirements ratified in `.specify/memory/constitution.md` and `.specify/memory/coding-standards.md` (whether the project mandates static verification without automated tests, or requires automated unit/integration test suites and coverage gates). Never apply hardcoded testing assumptions that conflict with the active constitution.
    ```

---

## 2. Orchestrator Dynamic Governance & Dispatch Contract (`FR-007`, `SC-003`)

Applies to:
- `.agents/skills/speckit-orchestrate/SKILL.md` and `.claude/skills/speckit-orchestrate/SKILL.md`

### Section 3: Governance Suite Adherence & Principle III Enforcement
- Must instruct the orchestrator to read `.specify/memory/constitution.md`, `.specify/memory/coding-standards.md`, and `.specify/memory/logging-standards.md` before dispatching subagents.
- If `.specify/memory/constitution.md` is missing or unreadable, the orchestrator MUST fail closed (`FAILED_CLOSED`), emit a `CRITICAL` diagnostic, and prompt the user to run `/speckit-constitution`.
- Must instruct the orchestrator to dynamically extract the active Principle III verification policy from `.specify/memory/constitution.md`:
  - Dynamically read the text of Principle III and pass it directly into the subagent execution directive payload.
  - If the active constitution ratifies static verification with no automated tests, enforce static verification and prohibit generating automated test files or tasks.
  - If the active constitution ratifies automated testing or `MODULE-B` coverage gates, enforce the required test suites, determinism rules, and coverage thresholds defined in `.specify/memory/constitution.md` and `.specify/memory/coding-standards.md`.

### Section 4 & Section 6: Dual-Client Agent & Skill Resolution
- The 5-level Agent Profile Hierarchy in Section 4 MUST resolve subagent profiles from the active client environment directory:
  - If `.claude/` exists and execution is within Claude Code (or `.agents/` is absent), resolve from `.claude/agents/`.
  - Otherwise, resolve from `.agents/agents/`.
  - Override chain:
    1. Runtime Flag (`--model=<tier>` or `--agent=<name>`)
    2. Stage Local Override (`<client>/agents/speckit-<stage>.local.md`)
    3. Stage Tracked Override (`<client>/agents/speckit-<stage>.md`)
    4. Role Local Override (`<client>/agents/speckit-<role>.local.md`)
    5. Role Tracked Default (`<client>/agents/speckit-<role>.md`)
- Stage 1–7 skill paths in Section 6 MUST resolve dynamically to `<client>/skills/<skill-name>/SKILL.md` (e.g. `.claude/skills/...` in Claude Code or `.agents/skills/...` in Antigravity).

### Section 5: Dual-Client Subagent Dispatch & Prompt Payload
- Subagent dispatch mechanism:
  - In **Google Antigravity**: dispatch via `define_subagent` and `invoke_subagent`.
  - In **Claude Code**: dispatch via `Task` tool (using `subagent_type: speckit-reasoner` or `speckit-executor`, with `model: opus` / `sonnet` / `inherit`). For read-only stages (such as `analyze`), prompt instructs the agent not to modify files.
- Item 3 of `Stage Execution Directive` MUST read:
  ```markdown
  3. Governance Suite Adherence (Non-Negotiable):
     - Enforce .specify/memory/constitution.md (specifically Principle III: {ACTIVE_PRINCIPLE_III_POLICY_FROM_CONSTITUTION}).
     - Enforce .specify/memory/coding-standards.md and .specify/memory/logging-standards.md.
  ```
- Item 3 of `Stage Execution Directive` MUST read:
  ```markdown
  3. Governance Suite Adherence (Non-Negotiable):
     - Enforce .specify/memory/constitution.md (specifically Principle III: {ACTIVE_PRINCIPLE_III_POLICY_FROM_CONSTITUTION}).
     - Enforce .specify/memory/coding-standards.md and .specify/memory/logging-standards.md.
  ```

---

## 3. Workflow Skill Constitutional Verification Contract (`FR-008`)

Applies to:
- `.agents/skills/speckit-roadmap/SKILL.md` and `.claude/skills/speckit-roadmap/SKILL.md`

### Section 8: Telemetry & Governance Standards Adherence
- Must replace `- **Principle III (Zero Automated Tests)**:` with:
  ```markdown
  - **Principle III (Constitutional Verification Gates)**: Adhere to the verification gates ratified in `.specify/memory/constitution.md`. For roadmap operations, verification is performed via static `--check`, `--status`, and schema validation gates (`RM-LINT-001`..`006`).
  ```
