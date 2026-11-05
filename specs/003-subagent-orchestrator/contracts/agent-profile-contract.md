# Contract: Role-Based Agent Profiles & Subagent Dispatch

**Artifact Targets**:
- `.agents/agents/speckit-reasoner.md` (Tracked High-Reasoning Agent Profile)
- `.agents/agents/speckit-executor.md` (Tracked Standard/Fast Execution Agent Profile)
- `.gitignore` (Must ignore `.agents/agents/*.local.md`)

---

## 1. Agent Profile Resolution Order

When `speckit-orchestrate` prepares to run `<stage>` with default role `<role>` (`reasoner` or `executor`), it MUST resolve the agent profile in this exact priority order:

1. **Runtime Flag Override**: `--model=<tier>` or `--agent=<name>` in `$ARGUMENTS`
2. **Stage-Specific Local Override**: `.agents/agents/speckit-<stage>.local.md` (gitignored)
3. **Stage-Specific Tracked Override**: `.agents/agents/speckit-<stage>.md` (optional tracked file)
4. **Role-Based Local Override**: `.agents/agents/speckit-<role>.local.md` (gitignored)
5. **Role-Based Tracked Default**: `.agents/agents/speckit-<role>.md` (`speckit-reasoner.md` or `speckit-executor.md`).

---

## 2. Two-Tier Role Mapping & Session Model Ceiling Algorithm

### 2.1 Stage-to-Role Assignment

| Pipeline Stage / Pass | Default Agent Profile | Role Capability Tier |
| :--- | :--- | :--- |
| `specify` | `.agents/agents/speckit-executor.md` | `execution` (Standard/Fast) |
| `clarify` | `.agents/agents/speckit-reasoner.md` | `reasoning` (High-Reasoning) |
| `plan` | `.agents/agents/speckit-reasoner.md` | `reasoning` (High-Reasoning) |
| `tasks` | `.agents/agents/speckit-executor.md` | `execution` (Standard/Fast) |
| `analyze` (and self-heal passes 1..2) | `.agents/agents/speckit-reasoner.md` | `reasoning` (High-Reasoning) |
| `implement` (initial pass 1) | `.agents/agents/speckit-executor.md` | `execution` (Standard/Fast) |
| `implement` (convergence retry passes 2..3) | `.agents/agents/speckit-reasoner.md` | `reasoning` (High-Reasoning escalation) |
| `converge` (passes 1..3) | `.agents/agents/speckit-reasoner.md` | `reasoning` (High-Reasoning) |

### 2.2 Provider-Adaptive Model Selection with Session Ceiling

Given `active_session_model` (the model the user selected for the current conversation) and the resolved agent profile's `role_tier`:

| Active Session Model Family & Tier | `speckit-reasoner` (`role_tier: reasoning`) | `speckit-executor` (`role_tier: execution`) |
| :--- | :--- | :--- |
| **Gemini Argon / Gemini Pro** (High-Reasoning Session) | `Model: "inherit"` (runs on Argon / Pro) | `Model: "flash"` (steps down to Gemini Flash) |
| **Gemini Flash / Flash Lite** (Standard/Fast Session, default ceiling) | `Model: "inherit"` (capped at Flash / Flash Lite) | `Model: "inherit"` (runs on Flash / Flash Lite) |
| **Claude Opus** (High-Reasoning Session) | `inherit` / `opus` (runs on Claude Opus) | `sonnet` (steps down to Claude Sonnet) |
| **Claude Sonnet / Haiku** (Standard/Fast Session, default ceiling) | `inherit` / `sonnet` (capped at Sonnet / Haiku) | `inherit` / `sonnet` (runs on Sonnet / Haiku) |
| **Explicit Override (`override_ceiling: true` or `--override-ceiling`)** | `Model: "pro"` / `opus` | `Model: "flash"` / `sonnet` |

---

## 3. Subagent Registration & Invocation Contract

In the Antigravity runtime, `speckit-orchestrate` registers the two custom subagent types (or the resolved stage override) via `define_subagent` once per session before invoking them with `invoke_subagent`:

- `Name`: `"speckit-reasoner"` / `"speckit-executor"` (or `"speckit-<stage>"` when a stage override is active)
- `Description`: Extracted from the agent profile's YAML frontmatter `description`
- `SystemPrompt`: Extracted from the agent profile's Markdown body
- `EnableWriteTools`: `true` for write stages (`specify`, `clarify`, `plan`, `tasks`, `implement`, `converge`, `self-heal`); `false` for read-only `analyze` passes
- `EnableSubagentTools`: `true` only when `implement` dispatches verified disjoint `[P]` tasks; `false` otherwise
- `Workspace`: `"inherit"` (all stage subagents operate sequentially on the repository root and `SPECIFY_FEATURE_DIRECTORY` under single-writer serialization).

### 3.1 Mandatory Subagent Prompt Payload

Every `invoke_subagent` `Prompt` constructed by `speckit-orchestrate` MUST include:

```markdown
## Stage Execution Directive: {STAGE_NAME}

1. **Target Skill**: Read and execute `/home/admin/projects/spec-kit-testing/.agents/skills/speckit-{stage}/SKILL.md`
2. **Feature Context**:
   - `SPECIFY_FEATURE_DIRECTORY`: `{FEATURE_DIR}`
   - `.specify/feature.json`: `{"feature_directory": "{REL_FEATURE_DIR}"}`
   - Environment constraint: Use `SPECIFY_FEATURE_NO_PERSIST=1` on prerequisite checks (except during `speckit-specify` creation).
3. **Co-Applied Governance Suite (Non-Negotiable)**:
   - Enforce `.specify/memory/constitution.md` (specifically Principle III: DO NOT generate any automated tests, unit tests, test directories, or test tasks).
   - Enforce `.specify/memory/coding-standards.md` and `.specify/memory/logging-standards.md`.
4. **Hook Anti-Recursion Guard**:
   - `ORCHESTRATOR_CHILD=true`: Do NOT invoke `/speckit-orchestrate` from any `hooks.after_*` extension hook.
5. **Required Completion Report**:
   Return a structured summary containing:
   - `STAGE_STATUS`: `SUCCESS` | `PAUSED_FOR_USER` | `FAILED`
   - `ARTIFACTS_TOUCHED`: List of created/updated file paths
   - `GATE_DATA`: Checklist counts, analysis finding counts by severity (`CRITICAL`, `HIGH`, `MEDIUM`, `LOW`), or convergence outcome (`converged` | `tasks_appended`)
   - `DIAGNOSTICS`: Any `INFO`, `WARN`, or `CRITICAL` messages per `.specify/memory/logging-standards.md`.
```
