# Implementation Plan: Claude Discovery Compatibility & Constitutional Test Decoupling

**Branch**: `007-claude-discovery-governance-decoupling` | **Date**: 2026-11-05 | **Spec**: [`spec.md`](spec.md)

**Input**: Feature specification from `/specs/007-claude-discovery-governance-decoupling/spec.md`

**Note**: This template is filled in by the `/speckit-plan` command; its definition describes the execution workflow.

<!--
Template Resolution Hierarchy & FeatureContext Specification:
This template is resolved by agent skills using the native 4-tier template resolution hierarchy:
- Tier 1 (Overrides): .specify/templates/overrides/plan-template.md
- Tier 2 (Presets): .specify/presets/<preset-id>/templates/plan-template.md (evaluated per .specify/presets/.registry sorted ascending by priority; strategy: replace, prepend, append, wrap)
- Tier 3 (Extensions): .specify/extensions/<ext-id>/templates/plan-template.md (evaluated per .specify/extensions/.registry sorted ascending by priority)
- Tier 4 (Core Fallback): .specify/templates/plan-template.md

Invariant: If a requested template is not found in any of the 4 tiers, the agent MUST fail closed and emit an error per Principle II

FeatureContext Resolution:
feature_directory MUST NOT be empty and ${FEATURE_DIR} MUST exist for downstream skills.
Context is discovered via SPECIFY_FEATURE_DIRECTORY env variable or .specify/feature.json.
-->

## Summary

Establish native Claude Code skill and subagent discovery compatibility alongside Google Antigravity by creating a byte-identical mirrored `.claude/` asset tree (`.claude/skills/<skill-name>/SKILL.md` for all 12 skills and `.claude/agents/<agent-name>.md` for both subagent profiles), updating the cross-platform bootstrapper scripts (`bootstrap-speckit.sh` and `bootstrap-speckit.ps1`), root `.gitignore`, `/speckit-bootstrap` skill, and cryptographic integration manifests (`.specify/integrations/claude.manifest.json` and `speckit-bootstrap.manifest.json`). Simultaneously, decouple hardcoded Principle III automated-test prohibitions from reusable subagent personas (`speckit-executor.md`, `speckit-reasoner.md`) and workflow skills (`speckit-orchestrate/SKILL.md`, `speckit-roadmap/SKILL.md`) so they dynamically inspect and enforce the active repository's ratified `.specify/memory/constitution.md` and companion standards at runtime. Finally, synchronize `README.md` and `ROADMAP.md` in compliance with Principle VII (`MODULE-DOCS`).

## Technical Context

**Language/Version**: Markdown (CommonMark / GitHub Flavored Markdown) for skills, subagent profiles, and governance documentation; Bash 4.0+ (`bootstrap-speckit.sh`); PowerShell 5.1+ / 7+ (`bootstrap-speckit.ps1`); JSON (`.specify/integrations/*.manifest.json`).

**Primary Dependencies**: Zero external runtime dependencies. POSIX core utilities (`find`, `sort`, `cp`, `grep`, `cmp`), PowerShell built-in cmdlets, and standard Python 3 (`hashlib`, `json`, `filecmp`) for static manifest verification.

**Storage**: Git-tracked flat files across `.specify/`, `.agents/`, `.claude/`, and repository root.

**Testing**: Static verification only per this repository's `.specify/memory/constitution.md` Principle III (`bash -n`, `cmp -s` / `filecmp` parity validation, JSON schema & SHA-256 digest verification, and markdown link/hygiene checks). Zero automated test files, test directories, or test tasks generated.

**Target Platform**: Cross-platform (Linux, macOS, Windows / WSL) supporting both Google Antigravity (`.agents/`) and Claude Code CLI (`.claude/`).

**Project Type**: Portable AI Agent Skill, Subagent Persona & Governance Customization Toolkit (`cli` / `configuration-bundle`).

**Performance Goals**: Bootstrapper execution `< 1s` for local repository seeding; `< 150` lines of code per bootstrapper script (`bootstrap-speckit.sh` and `bootstrap-speckit.ps1`).

**Constraints**: Byte-for-byte parity between `.agents/` and `.claude/` canonical files (`SC-001`); strict `PRESERVE_USER_STATE` protection for `.specify/memory/*`, `.specify/templates/overrides/*`, `.specify/feature.json`, `ROADMAP.md`, `.agents/agents/*.local.md`, and `.claude/agents/*.local.md`; zero references to ephemeral `specs/NNN-*` paths or `FR-XXX`/`SC-XXX` identifiers in permanent files.

**Scale/Scope**: 14 mirrored client files in `.claude/` (12 skills + 2 subagent profiles) matching 14 files in `.agents/`, 2 bootstrapper scripts, 4 integration manifests (53 total tracked bundle entries in `speckit-bootstrap.manifest.json`), `.gitignore`, `README.md`, and `ROADMAP.md`.

**Documentation Impact**: `USER_FACING` — Updates root [`README.md`](../../README.md) (Documenting dual `.claude/` and `.agents/` directory layout, subagent profile references, skill table paths, bootstrapper behavior, and `claude.manifest.json` verification command) and [`ROADMAP.md`](../../ROADMAP.md) (Phase 7 status synchronization).

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Pre-Phase 0 & Post-Phase 1 Gate Evaluation

| Constitutional Principle / Standard | Gate Requirement | Status | Verification & Justification |
|-------------------------------------|------------------|--------|------------------------------|
| **Principle I: Evidence Over Invention** | All changes trace to `spec.md` (`FR-001`..`FR-010`, `SC-001`..`SC-005`) and verified repository files. | `PASS` | Every modified and created file maps directly to verified requirements in `spec.md` and `ROADMAP.md` Phase 7. |
| **Principle II: Two-Tier Failure Model & Fail Closed** | Bootstrapper scripts and skills fail closed on missing source bundle assets or missing `.specify/memory/constitution.md`. | `PASS` | `bootstrap-speckit.{sh,ps1}` validate `.specify/`, `.agents/`, and `.claude/` required assets before mutating target disk; `/speckit-orchestrate` fails closed if required inputs are missing. |
| **Principle III: Static Verification & No Automated Tests** | Zero automated test files, test suites, or test tasks in `spec-kit-testing`; plan justification recorded. | `PASS` | While reusable agent personas (`speckit-executor.md`, `speckit-reasoner.md`) and `/speckit-orchestrate` are decoupled to dynamically obey any target project's constitution, **this** repository (`spec-kit-testing`) ratifies static verification with zero automated tests. Verification uses static syntax checks (`bash -n`), file parity (`filecmp`), and SHA-256 digest checks. |
| **Principle IV: Single Authoritative State & Boundaries** | `.specify/memory/constitution.md` is the single authoritative state for project verification policy; `PRESERVE_USER_STATE` boundaries respected. | `PASS` | Removing hardcoded test rules from agent profiles eliminates competing governance state and establishes `.specify/memory/constitution.md` as the sole authority. |
| **Principle V: Centralized Dependencies & Protected Toolchain** | Zero unapproved third-party packages or lockfile mutations. | `PASS` | Uses built-in Bash, PowerShell, and standard POSIX tools only. |
| **Principle VI: Bounded Resources & Verify-Before-Destroy** | Bootstrapper verifies source bundle before copying and never overwrites user state (`PRESERVE_USER_STATE`). | `PASS` | Pre-copy asset validation and strict exclusion filters protect user state and local `*.local.md` overrides. |
| **Principle VII: Code Hygiene, Ubiquitous Language & Safe Logging (`MODULE-DOCS`)** | `USER_FACING` changes update `README.md` canonical sections; zero ephemeral spec references outside `specs/`; structured `[INFO]`/`[WARN]`/`[CRITICAL]` logging. | `PASS` | `README.md` updates all 4 canonical sections for dual `.agents/` + `.claude/` discovery and `claude.manifest.json` verification. |

## Project Structure

### Documentation (this feature)

```text
specs/007-claude-discovery-governance-decoupling/
├── spec.md              # Feature specification
├── plan.md              # This implementation plan (/speckit-plan output)
├── research.md          # Phase 0 architectural decisions & rationale
├── data-model.md        # Phase 1 entities, schemas & invariants
├── quickstart.md        # Phase 1 runnable static validation guide
├── contracts/           # Phase 1 interface & governance contracts
│   ├── dual-client-bootstrap-contract.md
│   └── constitutional-deference-contract.md
└── tasks.md             # Phase 2 output (/speckit-tasks command - NOT created by /speckit-plan)
```

### Source Code (repository root)

```text
.
├── .agents/                                      # Google Antigravity discovery tree
│   ├── agents/
│   │   ├── speckit-executor.md                   # Modified: dynamic Principle III deference + dual client context
│   │   └── speckit-reasoner.md                   # Modified: dynamic Principle III deference + dual client context
│   └── skills/
│       ├── speckit-analyze/SKILL.md              # Unchanged source (mirrored to .claude/)
│       ├── speckit-bootstrap/SKILL.md            # Modified: dual .agents/ + .claude/ & claude.manifest.json checks
│       ├── speckit-checklist/SKILL.md            # Unchanged source (mirrored to .claude/)
│       ├── speckit-clarify/SKILL.md              # Unchanged source (mirrored to .claude/)
│       ├── speckit-constitution/SKILL.md         # Unchanged source (mirrored to .claude/)
│       ├── speckit-converge/SKILL.md             # Unchanged source (mirrored to .claude/)
│       ├── speckit-implement/SKILL.md            # Unchanged source (mirrored to .claude/)
│       ├── speckit-orchestrate/SKILL.md          # Modified: dynamic Principle III reading + dual-client resolution
│       ├── speckit-plan/SKILL.md                 # Unchanged source (mirrored to .claude/)
│       ├── speckit-roadmap/SKILL.md              # Modified: general constitutional verification gate reference
│       ├── speckit-specify/SKILL.md              # Unchanged source (mirrored to .claude/)
│       └── speckit-tasks/SKILL.md                # Unchanged source (mirrored to .claude/)
├── .claude/                                      # NEW: Claude Code CLI discovery tree (byte-identical mirror of .agents/)
│   ├── agents/
│   │   ├── speckit-executor.md                   # Created: byte-identical mirror of .agents/agents/speckit-executor.md
│   │   └── speckit-reasoner.md                   # Created: byte-identical mirror of .agents/agents/speckit-reasoner.md
│   └── skills/
│       ├── speckit-analyze/SKILL.md              # Created: byte-identical mirror
│       ├── speckit-bootstrap/SKILL.md            # Created: byte-identical mirror
│       ├── speckit-checklist/SKILL.md            # Created: byte-identical mirror
│       ├── speckit-clarify/SKILL.md              # Created: byte-identical mirror
│       ├── speckit-constitution/SKILL.md         # Created: byte-identical mirror
│       ├── speckit-converge/SKILL.md             # Created: byte-identical mirror
│       ├── speckit-implement/SKILL.md            # Created: byte-identical mirror
│       ├── speckit-orchestrate/SKILL.md          # Created: byte-identical mirror
│       ├── speckit-plan/SKILL.md                 # Created: byte-identical mirror
│       ├── speckit-roadmap/SKILL.md              # Created: byte-identical mirror
│       ├── speckit-specify/SKILL.md              # Created: byte-identical mirror
│       └── speckit-tasks/SKILL.md                # Created: byte-identical mirror
├── .specify/
│   └── integrations/
│       ├── agy.manifest.json                     # Modified: updated SHA-256 digests for modified .agents/ files
│       ├── claude.manifest.json                  # Created: SHA-256 digests for all 14 .claude/ files
│       ├── speckit.manifest.json                 # Verified: core .specify/templates/ & .gitignore digests
│       └── speckit-bootstrap.manifest.json       # Modified: 53 total entries across .agents/ (14), .claude/ (14), and .specify/ (25)
├── .gitignore                                    # Modified: add .claude/agents/*.local.md alongside .agents/agents/*.local.md
├── bootstrap-speckit.sh                          # Modified: seed .specify/, .agents/, and .claude/ + dual .gitignore patterns
├── bootstrap-speckit.ps1                         # Modified: seed .specify/, .agents/, and .claude/ + dual .gitignore patterns
├── README.md                                     # Modified: document dual .agents/ & .claude/ discovery and verification
└── ROADMAP.md                                    # Modified: synchronize Phase 7 status upon completion
```

**Structure Decision**: The repository uses a mirrored dual-client directory layout (`.agents/` for Google Antigravity and `.claude/` for Claude Code CLI) alongside the central `.specify/` governance and template engine. All 14 files in `.claude/` are byte-identical mirrors of `.agents/`, seeded together by `bootstrap-speckit.{sh,ps1}` and verified by `.specify/integrations/{agy,claude,speckit-bootstrap}.manifest.json`.

## Complexity Tracking

*No constitutional violations or complexity deviations required.*
