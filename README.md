# Spec Kit Customizations

Extensions for [GitHub Spec Kit](https://github.com/github/spec-kit) that add a project constitution, companion standards, multi-agent workflows, and bootstrap scripts.

---

## What's Added

GitHub's Spec Kit provides the core specification workflow (`spec.md` -> `plan.md` -> `tasks.md` -> implementation). This repository adds:

1. **Constitution & Companion Standards**: A project constitution (`constitution.md`) defining core engineering rules, supported by stack-specific `coding-standards.md` and `logging-standards.md`.
2. **Template Fallback System**: A 4-tier lookup (project overrides -> presets -> extensions -> defaults) so projects can customize templates or use presets (like `base-governance`).
3. **Dual Support for Google Antigravity & Claude Code**: Agent skills and subagent definitions work in both `.agents/` and `.claude/`.
4. **Subagents & Pipeline Orchestrator**: Dedicated reasoner and executor subagents coordinated through `/speckit-orchestrate`.
5. **Dynamic Constitution Checks**: Subagent instructions read the active project's constitution to determine testing and verification requirements (e.g., whether unit tests or static verification are required) rather than assuming hardcoded defaults.
6. **Installer Scripts**: Shell (`bootstrap-speckit.sh`) and PowerShell (`bootstrap-speckit.ps1`) scripts to seed these assets into any git repository.
7. **Roadmap Tracking**: `/speckit-roadmap` to define and track feature phases in `ROADMAP.md`.

---

## Constitution & Standards

The project rules live in `.specify/memory/`. The constitution is the primary authority, and it references companion standards for coding and logging details:

- [`.specify/memory/constitution.md`](.specify/memory/constitution.md): Core principles and development workflow rules (v2.2.0).
- [`.specify/memory/coding-standards.md`](.specify/memory/coding-standards.md): Language conventions, error handling patterns, and documentation requirements.
- [`.specify/memory/logging-standards.md`](.specify/memory/logging-standards.md): Log severity levels, structured format, and credential redaction.

### Core Principles

| Principle | Title | Mandate |
|---|---|---|
| **I** | **Evidence-Based Decisions & Bounded Research** | All requirements must trace to authoritative sources. No unverified assumptions or guessing. |
| **II** | **Explicit Error Handling & Fail-Closed State** | Catch and return typed errors at boundaries; fail closed immediately on broken internal state. |
| **III** | **Static Verification & Quality Gates** | Quality is verified through static analysis, linters, and checks (zero automated tests in this repo). |
| **IV** | **State Ownership, Architectural Seams & Safe Concurrency** | Exactly one owning model per piece of state; core logic sits behind clean seams. |
| **V** | **Centralized Dependencies & Toolchain Security** | Dependencies and toolchains are centrally locked. AI agents cannot add unapproved packages. |
| **VI** | **Resource Ceilings & Safe State Mutation** | Set explicit limits on inputs, collections, and loops. Verify state before destructive actions. |
| **VII** | **Code Standards, Consistent Terminology & Secure Logging** | Zero linter warnings; clear terminology; redact secrets from logs; keep docs up to date with code changes. |

### Optional Modules

The constitution template includes optional clauses that can be enabled per project:
- **`MODULE-A`**: Pointer tags in code for open questions (`// OPEN-QUESTION: OQ-XXX`).
- **`MODULE-B`**: 100% branch coverage gate (for projects requiring automated unit tests).
- **`MODULE-C`**: Table-driven command dispatch.
- **`MODULE-D`**: Reproducible builds and release versioning rules.
- **`MODULE-DOCS`**: Gate requiring documentation updates whenever user-facing features change.
- **`TRACE`**: Detailed function entry and exit logging.

---

## Subagents & Skills

### Subagent Personas

Used by `/speckit-orchestrate` in Google Antigravity ([`.agents/agents/`](.agents/agents/)) and Claude Code ([`.claude/agents/`](.claude/agents/)):

- **`speckit-reasoner`**: Handles architecture planning, requirements clarification, analysis, and convergence checks (`clarify`, `plan`, `analyze`, `converge`).
- **`speckit-executor`**: Handles writing initial specs, task breakdowns, and code implementation (`specify`, `tasks`, `implement`).

### Skills Reference

Maintained with 100% byte parity across Google Antigravity ([`.agents/skills/`](.agents/skills/)) and Claude Code ([`.claude/skills/`](.claude/skills/)):

| Skill | Status | What We've Added or Changed |
|---|---|---|
| **`/speckit-orchestrate`** | **New** | Coordinates context-isolated subagents through clarify, plan, tasks, analyze, implement, and converge, with human review checkpoints. |
| **`/speckit-bootstrap`** | **New** | Verifies file integrity via SHA-256 manifests, detects configuration drift, and performs non-destructive upgrades across `.specify/`, `.agents/`, and `.claude/`. |
| **`/speckit-roadmap`** | **New** | Authors, visualizes, audits, and syncs project milestones in [`ROADMAP.md`](ROADMAP.md) directly into feature specifications. |
| **`/speckit-constitution`** | Modified | Generates and syncs the constitution alongside companion `coding-standards.md` and `logging-standards.md`, supporting optional modules (`MODULE-A` through `MODULE-DOCS`). |
| **`/speckit-specify`** | Modified | Adds 4-tier template resolution, automatic sequential feature numbering, worktree isolation, and integration with roadmap phases (`--next` / `Phase N`). |
| **`/speckit-plan`** | Modified | Adds 4-tier template resolution, dynamic checks against active constitutional rules, and the human documentation gate (`USER_FACING` vs `INTERNAL_ONLY`). |
| **`/speckit-tasks`** | Modified | Enforces dynamic constitutional testing rules and automatically adds documentation tasks when changes affect user-facing docs. |
| **`/speckit-analyze`** | Modified | Adds automated self-healing passes (up to 2 iterations) to align `plan.md` and `tasks.md` with `spec.md`, plus documentation gate checks. |
| **`/speckit-implement`** | Modified | Dynamically obeys the project's constitutional verification rules and enforces pre-execution hooks. |
| **`/speckit-clarify`** | Modified | Integrated into the multi-agent orchestrator pipeline with an automated Clarify Gate that pauses for input when ambiguities exist. |
| **`/speckit-converge`** | Modified | Evaluates as-built code against specifications and tasks, automatically appending unbuilt work back into `tasks.md`. |
| **`/speckit-checklist`** | Modified | Adds 4-tier template resolution to generate custom requirements-quality checklists. |

---

## Installation & Setup

You can copy these files into any git repository using the bootstrap script. It installs the managed templates, presets, and skills while keeping existing user files safe:

### Linux / macOS
```bash
# Install into a target repo
./bootstrap-speckit.sh /path/to/target-repo

# Overwrite existing files if upgrading
./bootstrap-speckit.sh /path/to/target-repo --force
```

### Windows (PowerShell)
```powershell
# Install into a target repo
pwsh ./bootstrap-speckit.ps1 -TargetRepo "C:\path\to\target-repo"

# Overwrite existing files if upgrading
pwsh ./bootstrap-speckit.ps1 -TargetRepo "C:\path\to\target-repo" -Force
```

### Initializing Governance in Target Repo

After installing:
1. Verify the installed files:
   ```text
   /speckit-bootstrap --check
   ```
2. Initialize the project constitution:
   ```text
   /speckit-constitution
   ```

---

## Verification Checks

Commands to verify script syntax, file parity, and templates:

- **Check script syntax**:
  ```bash
  bash -n bootstrap-speckit.sh
  ```
- **Check parity between `.agents/` and `.claude/`**:
  ```bash
  diff -r .agents .claude
  ```
- **Check template parity**:
  ```bash
  cmp -s .specify/templates/constitution-template.md .specify/presets/base-governance/templates/constitution-template.md
  cmp -s .specify/templates/coding-standards-template.md .specify/presets/base-governance/templates/coding-standards-template.md
  cmp -s .specify/templates/logging-standards-template.md .specify/presets/base-governance/templates/logging-standards-template.md
  ```
