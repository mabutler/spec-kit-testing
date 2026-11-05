# Phase 1 Data Model: Claude Discovery Compatibility & Constitutional Test Decoupling

**Feature Branch**: `007-claude-discovery-governance-decoupling`  
**Date**: 2026-11-05  
**Spec**: [`spec.md`](spec.md) | **Research**: [`research.md`](research.md)

## Domain Entities & Schemas

### 1. Client Asset Tree (`ClientAssetTree`)

Represents a client-specific directory hierarchy (`<client-root>/`) discovered automatically by an AI coding environment.

| Field | Type | Description | Validation / Invariant |
|-------|------|-------------|------------------------|
| `client_id` | Enum (`"agy"`, `"claude"`) | Identifier for the AI client environment. | Must be `"agy"` or `"claude"`. |
| `root_dir` | Path (`.agents/` or `.claude/`) | Repository-relative directory root. | `.agents` for `"agy"`, `.claude` for `"claude"`. |
| `agent_profiles` | List of `AgentProfileAsset` | Subagent persona definitions under `<root_dir>/agents/`. | Exactly 2 canonical profiles: `speckit-executor.md`, `speckit-reasoner.md`. |
| `skills` | List of `SkillAsset` | Skill definitions under `<root_dir>/skills/<skill-name>/SKILL.md`. | All 12 canonical Spec Kit skills. |
| `local_override_glob` | Glob Pattern | Gitignored pattern for machine-local agent profile overrides. | `<root_dir>/agents/*.local.md` (must never be tracked or overwritten). |

**Cross-Tree Parity Invariant (`SC-001`)**:
For every canonical relative asset path `rel_path` in `{agents/speckit-executor.md, agents/speckit-reasoner.md, skills/speckit-*/SKILL.md}`:
```text
SHA256(.agents/<rel_path>) == SHA256(.claude/<rel_path>)
```

---

### 2. Subagent Persona Profile (`AgentProfileAsset`)

Represents a portable subagent role definition stored in `.agents/agents/<name>.md` and `.claude/agents/<name>.md`.

| Field | Type | Description | Validation / Invariant |
|-------|------|-------------|------------------------|
| `name` | String | Subagent identifier (`speckit-executor` or `speckit-reasoner`). | Non-empty kebab-case string matching filename stem. |
| `description` | String | Subagent description for discovery. | Non-empty string. |
| `model` | String | Model tier (`sonnet`, `opus`, or `inherit`). | Valid Claude Code & portable model identifier. |
| `speckit_role_tier` | Enum (`"execution"`, `"reasoning"`) | Capability classification used by orchestrator. | `"execution"` or `"reasoning"`. |
| `speckit_default_stages` | Array of Strings | Lifecycle stages routed to this persona by default. | Valid lifecycle stage identifiers. |
| `speckit_tool_policy` | Object | Antigravity tool access configuration (`enable_write_tools`, etc.). | Must not conflict with Claude Code tool string format. |
| `governance_rules` | Markdown Section | Core Governance & Operational Rules (Principles I–VII). | **Principle III Invariant (`FR-006`, `SC-003`)**: Must dynamically defer verification, testing, and coverage requirements to `.specify/memory/constitution.md` and `.specify/memory/coding-standards.md`; MUST NOT contain hardcoded prohibitions banning automated tests. |

---

### 3. Dynamic Constitutional Verification Directive (`VerificationDirective`)

Represents the runtime governance policy extracted by `/speckit-orchestrate` from `.specify/memory/constitution.md` and transmitted to dispatched subagents.

| Field | Type | Description | Validation / Invariant |
|-------|------|-------------|------------------------|
| `constitution_path` | Path | Authoritative constitution path (`.specify/memory/constitution.md`). | Must exist and be readable before subagent dispatch (Fail Closed per Principle II). |
| `companion_standards` | List of Paths | `.specify/memory/coding-standards.md`, `.specify/memory/logging-standards.md`. | Loaded alongside constitution when present. |
| `principle_iii_mode` | Enum (`"STATIC_ONLY"`, `"AUTOMATED_TESTS"`, `"COVERAGE_GATE_MODULE_B"`) | Active verification mode parsed from Principle III of `.specify/memory/constitution.md`. | Determined dynamically from the ratified constitution in the active workspace. |
| `directive_summary` | String | Concise rule injected into Section 3 of `Stage Execution Directive`. | Transmits the project's active Principle III rule without hardcoded assumptions in `speckit-orchestrate/SKILL.md`. |

**State Transitions (Runtime Resolution)**:
1. `UNRESOLVED` → Orchestrator reads `.specify/memory/constitution.md` and `.specify/memory/coding-standards.md`.
2. `RESOLVED` → Orchestrator identifies active Principle III verification clause (e.g., in `spec-kit-testing`: static verification with zero automated tests; in a `MODULE-B` repo: 100% branch coverage unit tests).
3. `DISPATCHED` → Subagent receives the resolved `directive_summary` in `Stage Execution Directive` item 3 and enforces it.

---

### 4. Client Integration Manifest (`ClientManifest`)

Represents `.specify/integrations/agy.manifest.json` and `.specify/integrations/claude.manifest.json`.

```json
{
  "integration": "claude",
  "version": "1.4.0",
  "installed_at": "2026-11-05T12:00:00+00:00",
  "files": {
    ".claude/agents/speckit-executor.md": "<64-char-hex-sha256>",
    ".claude/agents/speckit-reasoner.md": "<64-char-hex-sha256>",
    ".claude/skills/speckit-analyze/SKILL.md": "<64-char-hex-sha256>",
    ".claude/skills/speckit-bootstrap/SKILL.md": "<64-char-hex-sha256>",
    ".claude/skills/speckit-checklist/SKILL.md": "<64-char-hex-sha256>",
    ".claude/skills/speckit-clarify/SKILL.md": "<64-char-hex-sha256>",
    ".claude/skills/speckit-constitution/SKILL.md": "<64-char-hex-sha256>",
    ".claude/skills/speckit-converge/SKILL.md": "<64-char-hex-sha256>",
    ".claude/skills/speckit-implement/SKILL.md": "<64-char-hex-sha256>",
    ".claude/skills/speckit-orchestrate/SKILL.md": "<64-char-hex-sha256>",
    ".claude/skills/speckit-plan/SKILL.md": "<64-char-hex-sha256>",
    ".claude/skills/speckit-roadmap/SKILL.md": "<64-char-hex-sha256>",
    ".claude/skills/speckit-specify/SKILL.md": "<64-char-hex-sha256>",
    ".claude/skills/speckit-tasks/SKILL.md": "<64-char-hex-sha256>"
  }
}
```

---

### 5. Unified Bootstrap Manifest (`BootstrapManifest`)

Represents `.specify/integrations/speckit-bootstrap.manifest.json`, tracking every managed asset across `.specify/`, `.agents/`, and `.claude/`.

| Field | Type | Description | Validation / Invariant |
|-------|------|-------------|------------------------|
| `manifest_version` | String (`"1.0"`) | Schema version of the bootstrap manifest. | Fixed `"1.0"`. |
| `bundle_version` | String (`"1.4.0"`) | Version of the Spec Kit customization bundle. | Semantic version string. |
| `generated_at` | ISO-8601 Timestamp | UTC generation timestamp. | Valid ISO-8601 string. |
| `source_commit` | String | Commit reference (`"HEAD"` or SHA). | Non-empty string. |
| `files` | Map `<path, FileEntry>` | Dictionary of all managed files across `.agents/`, `.claude/`, and `.specify/`. | Must contain 14 `.agents/` entries (`tier: "agent"` or `"skill"`), 14 `.claude/` entries (`tier: "agent"` or `"skill"`), and 25 `.specify/` entries (including `.specify/integrations/claude.manifest.json` with `tier: "metadata"`), totaling 53 managed entries. |
