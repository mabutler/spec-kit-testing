# Spec Kit Customization & Governance Toolkit

A portable, production-grade customization toolkit for GitHub Spec Kit. This repository provides a co-applied governance suite, autonomous subagent role profiles, and specialized agent skills to seed, upgrade, and coordinate specification-driven software delivery across any Git workspace.

---

## Project Overview & Architecture

The Spec Kit Customization & Governance Toolkit establishes repository governance guardrails, portable bootstrapper scripts, and multi-agent coordination capabilities. It enables teams and AI agents to define feature specifications, decompose them into dependency-ordered implementation tasks, and enforce constitutional principles throughout the development lifecycle.

### Native 4-Tier Template Resolution Hierarchy

All Spec Kit agent skills resolve specification, planning, task, and governance templates using a deterministic 4-tier resolution hierarchy. Skills evaluate tiers in order and fail closed if a requested template cannot be resolved:

```
Tier 1: Overrides      (.specify/templates/overrides/<template-name>.md)
         ↓ (fallback if not found)
Tier 2: Presets        (.specify/presets/<preset-id>/templates/<template-name>.md)
         ↓ (fallback if not found)
Tier 3: Extensions     (.specify/extensions/<ext-id>/templates/<template-name>.md)
         ↓ (fallback if not found)
Tier 4: Core Fallback  (.specify/templates/<template-name>.md)
```

1. **Tier 1 (Overrides)**: Project-specific local customizations located in `.specify/templates/overrides/`.
2. **Tier 2 (Presets)**: Curated governance bundles located in `.specify/presets/` (such as [.specify/presets/base-governance/](.specify/presets/base-governance/)), evaluated in priority order according to `.specify/presets/.registry`.
3. **Tier 3 (Extensions)**: Domain-specific or tooling extensions registered in `.specify/extensions/`.
4. **Tier 4 (Core Fallback)**: Built-in default templates in [.specify/templates/](.specify/templates/) ([`constitution-template.md`](.specify/templates/constitution-template.md), [`coding-standards-template.md`](.specify/templates/coding-standards-template.md), [`logging-standards-template.md`](.specify/templates/logging-standards-template.md), [`plan-template.md`](.specify/templates/plan-template.md), [`spec-template.md`](.specify/templates/spec-template.md), [`tasks-template.md`](.specify/templates/tasks-template.md), [`roadmap-template.md`](.specify/templates/roadmap-template.md)).

### Directory Layout

```
.
├── .specify/
│   ├── memory/                    # Active Co-Applied Governance Suite
│   │   ├── constitution.md        # Ratified project constitution (v2.1.0)
│   │   ├── coding-standards.md    # Language and structural conventions
│   │   └── logging-standards.md   # Observability and audit logging rules
│   ├── templates/                 # Core fallback templates (Tier 4)
│   ├── presets/                   # Curated template presets (Tier 2)
│   ├── extensions/                # Registered extensions (Tier 3)
│   └── integrations/              # SHA-256 integrity manifests
├── .agents/                       # Google Antigravity discovery tree
│   ├── agents/                    # Subagent persona profiles
│   │   ├── speckit-reasoner.md    # High-reasoning cognitive subagent profile
│   │   └── speckit-executor.md    # High-velocity execution subagent profile
│   └── skills/                    # Specialized agent skill implementations (12 skills)
├── .claude/                       # Claude Code discovery tree (byte-identical mirror of .agents/)
│   ├── agents/                    # Subagent persona profiles
│   │   ├── speckit-reasoner.md    # High-reasoning cognitive subagent profile
│   │   └── speckit-executor.md    # High-velocity execution subagent profile
│   └── skills/                    # Specialized agent skill implementations (12 skills)
├── bootstrap-speckit.sh           # POSIX seeding & bootstrapping shell script
├── bootstrap-speckit.ps1          # Cross-platform PowerShell bootstrapper script
└── ROADMAP.md                     # Architecture, features, and evolution roadmap
```

---

## Co-Applied Governance Suite

This repository ratifies and enforces a tri-part **Co-Applied Governance Suite** located under [`.specify/memory/`](.specify/memory/):

- [`.specify/memory/constitution.md`](.specify/memory/constitution.md): Canonical repository constitution (Version 2.1.0) establishing foundational non-negotiable principles.
- [`.specify/memory/coding-standards.md`](.specify/memory/coding-standards.md): Concrete implementation, error handling, typing, and human-facing documentation conventions.
- [`.specify/memory/logging-standards.md`](.specify/memory/logging-standards.md): Structured logging taxonomy, correlation identifier schema, and secret sanitization rules.

### Core Principles Summary

| Principle | Name | Mandate |
|---|---|---|
| **I** | **Evidence Over Invention** | Every domain behavior, constant, and security requirement MUST trace to an authoritative source. Plausible guesses are forbidden. |
| **II** | **Two-Tier Failure Model** | Distinguish recoverable boundary rejections (typed errors, `WARN` log) from internal defect invariants (fail closed, `CRITICAL` log). |
| **III** | **Static Verification & No Automated Tests** | Repository-wide verification is performed via static analysis, schema checks, and declarative gates. Zero automated test suites are generated. |
| **IV** | **Single Authoritative State & Boundaries** | Every piece of state has exactly one owning model; core logic does not depend on raw wire schemas or I/O primitives. |
| **V** | **Centralized Dependencies & Protected Toolchain** | Package versions and linter settings are declared centrally at root. Agents cannot add unapproved dependencies. |
| **VI** | **Bounded Resources & Verify-Before-Destroy** | Input bounds, collection counts, and memory allocations have explicit ceilings. Irreversible actions require pre-verification. |
| **VII** | **Code Hygiene, Ubiquitous Language & Safe Logging** | Linters pass with zero warnings; comments explain current design reasons; logs redact secrets; and documentation synchronizes with code changes. |

### Optional Governance Modules

The governance engine supports optional modules that can be enabled during ratification:

- **`MODULE-A`**: In-Code Open Question Pointers (`Principle I`).
- **`MODULE-B`**: 100% Branch Coverage Gate (`Principle III`, mutually exclusive with skip allowlist).
- **`MODULE-C`**: Dispatch Is Data, Not Branches (`Principle IV`).
- **`MODULE-D`**: Reproducible Builds & Deliberate Versioning (`Principle V`).
  - **`MODULE-D-AOT-TRIM`**: Subclause for AOT/Trim-safe core domain logic.
- **`MODULE-DOCS`**: Structured Human-Facing Documentation Gate (`Principle VII`), mandating canonical sections in `README.md` and user guides.
- **`TRACE` Logging**: Fine-grained method entry/exit tracing in `logging-standards.md`.

### Documentation Impact Gate

All feature plans (`plan.md`) must classify changes before implementation:
- **`USER_FACING`**: When user-visible CLI commands, agent skills, public APIs, configuration options, or workflows are added, removed, or modified, the root `README.md` and user guides MUST be updated in the same change.
- **`INTERNAL_ONLY`**: Purely internal refactors, non-behavioral bug fixes, or test/tooling adjustments with an explicit rationale are exempt from artificial `README.md` edits.

---

## Spec Kit Skills & Subagent Reference

### Subagent Role Profiles

Multi-agent workflows dispatched by `/speckit-orchestrate` utilize two context-isolated subagent profiles discovered automatically across Google Antigravity (`.agents/agents/`) and Claude Code (`.claude/agents/`):

- [`.agents/agents/speckit-reasoner.md`](.agents/agents/speckit-reasoner.md) (mirrored to [`.claude/agents/speckit-reasoner.md`](.claude/agents/speckit-reasoner.md)): High-reasoning persona specialized for architecture planning, requirements clarification, drift analysis, convergence verification, and retry escalations (`clarify`, `plan`, `analyze`, `converge`).
- [`.agents/agents/speckit-executor.md`](.agents/agents/speckit-executor.md) (mirrored to [`.claude/agents/speckit-executor.md`](.claude/agents/speckit-executor.md)): Standard/fast execution persona specialized for rapid specification capture, task decomposition, and code implementation (`specify`, `tasks`, `implement`).

Subagent personas dynamically inspect and obey the verification, testing, and coverage requirements ratified in the target project's `.specify/memory/constitution.md` and `.specify/memory/coding-standards.md` rather than enforcing hardcoded assumptions.

### Spec Kit Skills

The toolkit includes 12 specialized agent skills maintained with 100% byte-identical parity across both [`.agents/skills/`](.agents/skills/) (Google Antigravity) and [`.claude/skills/`](.claude/skills/) (Claude Code):

| Skill | Directory | Lifecycle Phase | Description |
|---|---|---|---|
| **`/speckit-specify`** | [`.agents/skills/speckit-specify/`](.agents/skills/speckit-specify/SKILL.md) | Specify | Synthesizes an initial feature specification (`spec.md`) from a natural language feature request. |
| **`/speckit-clarify`** | [`.agents/skills/speckit-clarify/`](.agents/skills/speckit-clarify/SKILL.md) | Clarify | Formulates targeted clarification questions for underspecified areas and encodes answers into the specification. |
| **`/speckit-plan`** | [`.agents/skills/speckit-plan/`](.agents/skills/speckit-plan/SKILL.md) | Plan | Creates an implementation plan (`plan.md`), evaluates `Documentation Impact`, and generates technical contracts. |
| **`/speckit-tasks`** | [`.agents/skills/speckit-tasks/`](.agents/skills/speckit-tasks/SKILL.md) | Tasks | Decomposes design documents into an actionable, dependency-ordered task breakdown (`tasks.md`). |
| **`/speckit-checklist`** | [`.agents/skills/speckit-checklist/`](.agents/skills/speckit-checklist/SKILL.md) | Review | Generates custom requirements-quality review checklists for specialized domain validations. |
| **`/speckit-analyze`** | [`.agents/skills/speckit-analyze/`](.agents/skills/speckit-analyze/SKILL.md) | Analyze | Performs non-destructive cross-artifact consistency and quality audits across `spec.md`, `plan.md`, and `tasks.md`. |
| **`/speckit-implement`** | [`.agents/skills/speckit-implement/`](.agents/skills/speckit-implement/SKILL.md) | Implement | Executes tasks in `tasks.md` sequentially by phase, verifying each milestone and updating task markers. |
| **`/speckit-converge`** | [`.agents/skills/speckit-converge/`](.agents/skills/speckit-converge/SKILL.md) | Converge | Assesses as-built code against specifications and tasks, generating convergence gap tasks if discrepancies exist. |
| **`/speckit-constitution`** | [`.agents/skills/speckit-constitution/`](.agents/skills/speckit-constitution/SKILL.md) | Governance | Authoritatively ratifies or amends the Co-Applied Governance Suite (`constitution.md`, `coding-standards.md`, `logging-standards.md`). |
| **`/speckit-orchestrate`** | [`.agents/skills/speckit-orchestrate/`](.agents/skills/speckit-orchestrate/SKILL.md) | Coordinator | Coordinates context-isolated subagents through clarify, plan, tasks, analyze, implement, and converge. |
| **`/speckit-bootstrap`** | [`.agents/skills/speckit-bootstrap/`](.agents/skills/speckit-bootstrap/SKILL.md) | Bootstrap | Verifies asset integrity, manages non-destructive upgrades, detects drift, and bootstraps governance. |
| **`/speckit-roadmap`** | [`.agents/skills/speckit-roadmap/`](.agents/skills/speckit-roadmap/SKILL.md) | Roadmap | Authors, visualizes, audits, synchronizes, and hands off project-level strategic roadmaps (`ROADMAP.md`) into feature specifications. |

---

## Getting Started & Portable Bootstrapping

The toolkit can be seeded into any target repository using native shell scripts with zero external dependencies. The bootstrapper copies all 53 managed assets across `.specify/`, `.agents/`, and `.claude/` while preserving existing user state and automatically maintaining `.gitignore` patterns for local overrides (`.agents/agents/*.local.md`, `.claude/agents/*.local.md`, `.claude/settings.local.json`).

### POSIX Environments (Linux / macOS / WSL)

Run [`bootstrap-speckit.sh`](bootstrap-speckit.sh) to seed Spec Kit assets into a target repository:

```bash
# Seed into a target directory
./bootstrap-speckit.sh /path/to/target-repo

# Overwrite existing managed files if updating
./bootstrap-speckit.sh /path/to/target-repo --force
```

### Windows & PowerShell Environments

Run [`bootstrap-speckit.ps1`](bootstrap-speckit.ps1) using PowerShell Core or Windows PowerShell:

```powershell
# Seed into a target directory
pwsh ./bootstrap-speckit.ps1 -TargetRepo "C:\path\to\target-repo"

# Overwrite existing managed files
pwsh ./bootstrap-speckit.ps1 -TargetRepo "C:\path\to\target-repo" -Force
```

### Post-Seeding Governance & Upgrade Workflow

Once seeded into a target project:

1. **Verify Asset Integrity**:
   ```text
   /speckit-bootstrap --check
   ```
2. **Initialize or Amend Governance**:
   ```text
   /speckit-bootstrap --init-governance
   # or run the dedicated governance engine:
   /speckit-constitution
   ```
3. **Upgrade Assets Non-Destructively**:
   ```text
   /speckit-bootstrap --upgrade
   ```

---

## Configuration & Governance Verification

The repository enforces automated verification gates to ensure configuration integrity:

- **POSIX Bootstrapper Syntax & Line Budget**:
  ```bash
  bash -n bootstrap-speckit.sh
  ```
- **Dual-Client Byte-for-Byte Parity**:
  ```bash
  python3 -c '
  import filecmp, os, sys
  canonical = [
      "agents/speckit-executor.md", "agents/speckit-reasoner.md",
      "skills/speckit-analyze/SKILL.md", "skills/speckit-bootstrap/SKILL.md",
      "skills/speckit-checklist/SKILL.md", "skills/speckit-clarify/SKILL.md",
      "skills/speckit-constitution/SKILL.md", "skills/speckit-converge/SKILL.md",
      "skills/speckit-implement/SKILL.md", "skills/speckit-orchestrate/SKILL.md",
      "skills/speckit-plan/SKILL.md", "skills/speckit-roadmap/SKILL.md",
      "skills/speckit-specify/SKILL.md", "skills/speckit-tasks/SKILL.md"
  ]
  for rel in canonical:
      a, c = os.path.join(".agents", rel), os.path.join(".claude", rel)
      if not filecmp.cmp(a, c, shallow=False): sys.exit(f"Parity mismatch: {a} != {c}")
  print("All 14 client files match byte-for-byte across .agents/ and .claude/.")
  '
  ```
- **Template & Preset Parity**:
  ```bash
  cmp -s .specify/templates/constitution-template.md .specify/presets/base-governance/templates/constitution-template.md
  cmp -s .specify/templates/coding-standards-template.md .specify/presets/base-governance/templates/coding-standards-template.md
  ```
- **Manifest Integrity & SHA-256 Validation**:
  Integration manifests in `.specify/integrations/` track cryptographic SHA-256 digests and file sizes across all managed assets:
  ```bash
  python3 -c '
  import hashlib, json, os, sys
  manifests = [
      ".specify/integrations/speckit.manifest.json",
      ".specify/integrations/agy.manifest.json",
      ".specify/integrations/claude.manifest.json",
      ".specify/integrations/speckit-bootstrap.manifest.json"
  ]
  for p in manifests:
      d = json.load(open(p))
      for f, m in d["files"].items():
          raw = open(f, "rb").read()
          dig = hashlib.sha256(raw).hexdigest()
          exp = m if isinstance(m, str) else m["digest"].replace("sha256:", "")
          if dig != exp: sys.exit(f"Digest mismatch in {p} for {f}")
  print("All 4 manifests valid with 0 drift.")
  '
  ```
- **Markdown Hygiene**:
  Permanent files enforce zero broken relative links, zero unresolved slot placeholders, and zero citations of ephemeral specification folders.
