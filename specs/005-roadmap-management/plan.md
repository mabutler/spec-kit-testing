# Implementation Plan: Roadmap Management (`speckit-roadmap`)

**Branch**: `005-roadmap-management` | **Date**: 2026-11-05 | **Spec**: [spec.md](file:///home/admin/projects/spec-kit-testing/.worktrees/005-roadmap-management/specs/005-roadmap-management/spec.md)

**Input**: Feature specification from `/specs/005-roadmap-management/spec.md`

---

## Summary

Deliver first-class multi-phase strategic roadmap management (`speckit-roadmap`) for Spec Kit. This feature introduces a canonical `roadmap-template.md` across both the core template fallback tier (`.specify/templates/roadmap-template.md`) and the `base-governance` preset tier (`.specify/presets/base-governance/templates/roadmap-template.md`), creates a 100% script-free `.agents/skills/speckit-roadmap/SKILL.md` agent skill supporting five operational modes (Scaffold/Authoring, Phase Mutation, Read-Only Status & Drift Audit, Status Synchronization, and Specify Handoff), upgrades `.agents/skills/speckit-specify/SKILL.md` to natively extract phase context from `ROADMAP.md` and provision isolated git worktrees (`.worktrees/<NNN>-<short-name>`), migrates this repository's `ROADMAP.md` to the canonical schema with verified status markers and `specs/001-*` through `specs/005-*` links, and updates the portable bootstrapper suite (`bootstrap-speckit.sh`, `bootstrap-speckit.ps1`, `speckit-bootstrap`, and `.specify/integrations/*.manifest.json`) to package the 12th skill while protecting root `ROADMAP.md` as project-owned user state.

---

## Technical Context

**Language/Version**: CommonMark / GitHub Flavored Markdown (templates and agent skills), POSIX Shell / Bash 4.0+ (`bootstrap-speckit.sh`), PowerShell 5.1 / PowerShell 7+ (`bootstrap-speckit.ps1`)  
**Primary Dependencies**: None (zero external runtime dependencies; native agent file operations, git CLI inspection, and built-in shell utilities only)  
**Storage**: Local filesystem (`ROADMAP.md`, `.specify/templates/roadmap-template.md`, `.specify/presets/base-governance/templates/roadmap-template.md`, `.specify/integrations/*.manifest.json`, `.specify/feature.json`)  
**Testing**: Constitutional Principle III (*Static Verification & No Automated Tests*); static shell syntax checks (`bash -n`), markdown structural linting via `/speckit-roadmap --check`, SHA-256 manifest verification via `/speckit-bootstrap --check`, and end-to-end scenario validation  
**Target Platform**: Linux, macOS, Windows (native and WSL), across all Spec Kit-compatible AI agent harnesses  
**Project Type**: Agent Skill workflow suite + Markdown governance templates + CLI bootstrapper seeders  
**Performance Goals**: Seeder scripts execute in < 1 second; `/speckit-roadmap --status` and `--check` complete in a single pass with zero subprocess script wrappers  
**Constraints**: 100% script-free skills (zero `.specify/scripts/` files or references); seeder scripts MUST remain under 150 lines each; root `ROADMAP.md` MUST be protected in the User-State Boundary and never clobbered during bootstrap or upgrade  
**Scale/Scope**: 12 managed skills (adding `speckit-roadmap`), 8 core templates (adding `roadmap-template.md`), 4 preset templates in `base-governance`, 6 roadmap phases in `ROADMAP.md`, 3 integration manifests  

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Assessment & Implementation Rules | Pre-Research Gate | Post-Design Gate |
|-----------|----------------------------------|-------------------|------------------|
| **I. Evidence Over Invention** | All roadmap schema rules, status inference criteria (`COMPLETED`, `IN_PROGRESS`, `PLANNED`, `DEFERRED`), and handoff workflows trace directly to `specs/005-roadmap-management/spec.md` (`FR-001`–`FR-008`) and verified repository artifacts (`specs/001-*` through `specs/005-*`). | PASS | PASS |
| **II. Two-Tier Failure Model & Fail Closed** | Missing/empty `ROADMAP.md`, unfulfilled phase prerequisites on `--next`/`--specify`, and structural/referential defects on `--check` fail closed at the boundary before mutating state and log structured `WARN` diagnostics. Missing template tiers log `CRITICAL` and halt. | PASS | PASS |
| **III. Static Verification & No Automated Tests** | Repository-wide Principle III exemption ratified in Constitution v2.0.0. Zero automated test files, test directories (`tests/`), or test tasks will be generated. Verification relies strictly on static inspection, `bash -n`, `--check` / `--status` validation, and SHA-256 manifest verification. | PASS | PASS |
| **IV. Single Authoritative State & Boundaries** | `ROADMAP.md` is the single strategic source of truth for project initiatives, while `specs/NNN-*/{spec,plan,tasks}.md` and `.specify/feature.json` are the authoritative tactical state. No competing sidecar JSON files are introduced. Root `ROADMAP.md` is protected as user state. | PASS | PASS |
| **V. Centralized Dependencies & Protected Toolchain** | Zero external dependencies or third-party packages added. All skills operate natively via Markdown instructions and standard git/filesystem primitives. | PASS | PASS |
| **VI. Bounded Resources & Verify-Before-Destroy** | `--status` and `--check` are strictly read-only. Mutating operations (`--sync`, `--next`, `--add`, `--update`, `--defer`) validate structural integrity and prerequisite completion before writing `ROADMAP.md`. Bootstrapper never overwrites `ROADMAP.md`. | PASS | PASS |
| **VII. Code Hygiene, Ubiquitous Language & Safe Logging** | Adheres to `.specify/memory/coding-standards.md` and `.specify/memory/logging-standards.md`. Uses canonical status vocabulary (`PLANNED`, `IN_PROGRESS`, `COMPLETED`, `DEFERRED`) and structured `INFO`/`WARN`/`CRITICAL` telemetry with zero secrets logged. | PASS | PASS |

---

## Project Structure

### Documentation (this feature)

```text
specs/005-roadmap-management/
├── spec.md              # Feature specification
├── plan.md              # This file (/speckit-plan command output)
├── research.md          # Phase 0 output (/speckit-plan command)
├── data-model.md        # Phase 1 output (/speckit-plan command)
├── quickstart.md        # Phase 1 output (/speckit-plan command)
├── contracts/           # Phase 1 output (/speckit-plan command)
│   ├── roadmap-schema-contract.md
│   ├── speckit-roadmap-skill-contract.md
│   └── speckit-specify-roadmap-worktree-contract.md
├── checklists/
│   └── requirements.md  # Spec quality checklist
└── tasks.md             # Phase 2 output (/speckit-tasks command - NOT created by /speckit-plan)
```

### Source Code Layout (repository root)

```text
# Repository Root
├── ROADMAP.md                               # [MODIFIED] Upgraded to canonical roadmap-template schema (Phases 1-6)
├── bootstrap-speckit.sh                     # [MODIFIED] Verifies roadmap-template.md in required source bundle (<150 LOC)
├── bootstrap-speckit.ps1                    # [MODIFIED] Verifies roadmap-template.md in required source bundle (<150 LOC)
│
├── .agents/
│   ├── agents/
│   │   ├── speckit-executor.md              # Managed Executor role profile
│   │   └── speckit-reasoner.md              # Managed Reasoner role profile
│   └── skills/
│       ├── speckit-roadmap/SKILL.md         # [NEW] 100% script-free roadmap management skill (12th skill)
│       ├── speckit-specify/SKILL.md         # [MODIFIED] Roadmap phase context extraction + git worktree support
│       ├── speckit-bootstrap/SKILL.md       # [MODIFIED] 12 skills inventory + ROADMAP.md Protected User-State rule
│       ├── speckit-analyze/SKILL.md         # Unchanged managed skill
│       ├── speckit-checklist/SKILL.md       # Unchanged managed skill
│       ├── speckit-clarify/SKILL.md         # Unchanged managed skill
│       ├── speckit-constitution/SKILL.md    # Unchanged managed skill
│       ├── speckit-converge/SKILL.md        # Unchanged managed skill
│       ├── speckit-implement/SKILL.md       # Unchanged managed skill
│       ├── speckit-orchestrate/SKILL.md     # Unchanged managed skill
│       ├── speckit-plan/SKILL.md            # Unchanged managed skill
│       └── speckit-tasks/SKILL.md           # Unchanged managed skill
│
├── .specify/
│   ├── presets/
│   │   ├── .registry                        # Preset priority registry
│   │   └── base-governance/
│   │       ├── preset.yml                   # [MODIFIED] Registers roadmap-template (strategy: replace)
│   │       └── templates/
│   │           ├── coding-standards-template.md
│   │           ├── constitution-template.md
│   │           ├── logging-standards-template.md
│   │           └── roadmap-template.md      # [NEW] Preset roadmap template (synchronized with core)
│   ├── templates/
│   │   ├── checklist-template.md
│   │   ├── coding-standards-template.md
│   │   ├── constitution-template.md
│   │   ├── logging-standards-template.md
│   │   ├── plan-template.md
│   │   ├── roadmap-template.md              # [NEW] Core fallback roadmap template
│   │   ├── spec-template.md
│   │   └── tasks-template.md
│   ├── integrations/
│   │   ├── agy.manifest.json                # [MODIFIED] Synchronized with 12 script-free skills
│   │   ├── speckit.manifest.json            # [MODIFIED] Includes .specify/templates/roadmap-template.md
│   │   └── speckit-bootstrap.manifest.json  # [MODIFIED] Updated SHA-256 digests and sizes for all managed assets
│   └── memory/                              # [PROTECTED USER STATE - IMMUTABLE]
│       ├── constitution.md
│       ├── coding-standards.md
│       └── logging-standards.md
```

**Structure Decision**: Extends the existing `.specify/templates/`, `.specify/presets/base-governance/`, and `.agents/skills/` architecture established in Phases 1–4. Keeps all skills 100% script-free (`.specify/scripts/` remains completely absent) and preserves the ultra-thin (<150 LOC) root seeder scripts.

---

## Complexity Tracking

> *No constitutional violations or unjustified complexities identified. Principle III test generation exemption is fully ratified in Constitution v2.0.0.*

| Violation / Exemption | Why Needed | Simpler Alternative Rejected Because |
|-----------------------|------------|-------------------------------------|
| Principle III (No Automated Tests) | Explicit human authority directive ratified in Constitution v2.0.0. Eliminates automated test suites in favor of static verification and declarative quality gates. | Generating automated test harnesses was explicitly disallowed by project governance. |
