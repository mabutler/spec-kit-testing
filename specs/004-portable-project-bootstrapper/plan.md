# Implementation Plan: Portable Project Bootstrapper

**Branch**: `004-portable-project-bootstrapper` | **Date**: 2026-11-05 | **Spec**: [spec.md](file:///home/admin/projects/spec-kit-testing/specs/004-portable-project-bootstrapper/spec.md)

**Input**: Feature specification from `/specs/004-portable-project-bootstrapper/spec.md`

---

## Summary

Deliver a completely script-free Spec Kit workflow suite and portable project bootstrapper. This feature refactors all 10 existing Spec Kit skills (`specify`, `clarify`, `plan`, `tasks`, `checklist`, `analyze`, `implement`, `converge`, `constitution`, `orchestrate`) plus the new `bootstrap` skill to use 100% agent-native file operations for feature discovery and 4-tier template resolution, completely removes `.specify/scripts/`, introduces paired ultra-thin cross-platform terminal seeder scripts (`bootstrap-speckit.sh` and `bootstrap-speckit.ps1`) under 150 lines each with zero external dependencies, packages Phase 1 governance templates as a first-class preset (`.specify/presets/base-governance/`) and Phase 3 orchestration as an extension (`.specify/extensions/speckit-orchestrator/`), and provides an intelligent `/speckit-bootstrap` agent skill for manifest-gated non-destructive upgrades and governance initialization while guaranteeing Protected User-State immutability.

---

## Technical Context

**Language/Version**: POSIX Shell / Bash 4.0+ (`bootstrap-speckit.sh`), PowerShell 5.1 / PowerShell 7+ (`bootstrap-speckit.ps1`), CommonMark / GitHub Flavored Markdown (skills and agent definitions)  
**Primary Dependencies**: None (zero external package dependencies; built-in shell utilities and native agent file operations only)  
**Storage**: Local filesystem, JSON manifests (`.specify/integrations/*.manifest.json`, `.specify/presets/.registry`, `.specify/extensions/.registry`, `.specify/feature.json`), YAML configs (`preset.yml`, `extension.yml`, `extensions.yml`)  
**Testing**: Constitutional Principle III (*Static Verification & No Automated Tests*); static shell syntax checks (`bash -n`), JSON schema validation, markdown linting, `--check` dry-run validation, and live end-to-end scenario verification  
**Target Platform**: Linux, macOS, Windows (native and WSL), across all major AI agent harnesses  
**Project Type**: CLI seeder scripts + Agent Skill workflow suite  
**Performance Goals**: Seeder scripts execute in < 1 second; `/speckit-bootstrap` verification runs in < 2 seconds; zero runtime subprocess spawn overhead during agent skill execution  
**Constraints**: Seeder scripts MUST remain under 150 lines each; zero external dependencies (no Python, Node, Ruby, or package managers required for seeding); strict enforcement of Protected User-State immutability; 100% script-free skills  
**Scale/Scope**: 11 managed skills, 2 role-based agent definitions, 1 core preset package, 1 core extension package, 3 integration manifests  

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Assessment & Implementation Rules | Gate Status |
|-----------|----------------------------------|-------------|
| **I. Evidence Over Invention** | Implementation strictly adheres to acceptance criteria in `specs/004-portable-project-bootstrapper/spec.md` and ratified decisions from the Phase 4 clarification session. Zero guesswork or unverified assumptions. | PASS |
| **II. Two-Tier Failure Model & Fail Closed** | Invalid inputs (e.g. self-targeting destination, missing arguments, invalid paths) fail closed immediately at the boundary with clear `WARN` rejections. Corrupted internal state or missing required bundle files log `CRITICAL` diagnostics and halt. | PASS |
| **III. Static Verification & No Automated Tests** | Repository-wide Principle III exemption ratified in Constitution v2.0.0. Zero automated test suites (`tests/`), test harnesses, or test tasks will be created. All verification uses static syntax checking, schema validation, and dry-run execution. | PASS |
| **IV. Single Authoritative State & Boundaries** | Protected User-State allowlist ensures ratified governance (`.specify/memory/*.md`), local overrides (`.specify/templates/overrides/**`), and feature state (`specs/**`, `feature.json`) are single sources of truth that are never clobbered. | PASS |
| **V. Centralized Dependencies & Protected Toolchain** | Zero external third-party dependencies. Built-in POSIX utilities, built-in PowerShell commands, and native agent file operations only. No modifications to toolchain flags or package sources. | PASS |
| **VI. Bounded Resources & Verify-Before-Destroy** | Upgrade workflow computes a file classification plan (`CREATE`, `UPGRADE`, `PRESERVE_USER_STATE`, `SKIP_DRIFTED`, `REMOVE_OBSOLETE`, `UNCHANGED`) before modifying disk. Deletions are bounded to obsolete scripts and guarded by opt-in flags. | PASS |
| **VII. Code Hygiene, Ubiquitous Language & Safe Logging** | All logs and summaries adhere to `.specify/memory/logging-standards.md` with structured levels (`INFO`, `WARN`, `CRITICAL`). Zero credentials or sensitive data logged. Common kebab-case file conventions preserved. | PASS |

---

## Project Structure

### Documentation (this feature)

```text
specs/004-portable-project-bootstrapper/
├── spec.md              # Feature specification
├── plan.md              # This file (implementation plan)
├── research.md          # Phase 0 research findings
├── data-model.md        # Phase 1 data entities and state machine
├── quickstart.md        # Phase 1 end-to-end validation guide
├── contracts/           # Phase 1 interface specifications
│   ├── bootstrap-cli-contract.md
│   ├── speckit-bootstrap-skill-contract.md
│   ├── manifest-schema.json
│   └── preset-and-extension-schema.json
└── tasks.md             # Phase 2 output (/speckit-tasks command)
```

### Source Code Layout (repository root)

```text
# Repository Root
├── bootstrap-speckit.sh                     # [NEW] Ultra-thin Bash/POSIX seeder (<150 LOC)
├── bootstrap-speckit.ps1                    # [NEW] Ultra-thin PowerShell seeder (<150 LOC)
│
├── .agents/
│   ├── agents/
│   │   ├── speckit-executor.md              # Managed Executor role profile
│   │   └── speckit-reasoner.md              # Managed Reasoner role profile
│   └── skills/
│       ├── speckit-analyze/SKILL.md         # [MODIFIED] Refactored to script-free agent ops
│       ├── speckit-bootstrap/SKILL.md       # [NEW] Intelligent agent bootstrapper skill
│       ├── speckit-checklist/SKILL.md       # [MODIFIED] Refactored to script-free agent ops
│       ├── speckit-clarify/SKILL.md         # [MODIFIED] Refactored to script-free agent ops
│       ├── speckit-constitution/SKILL.md   # [MODIFIED] Refactored to script-free agent ops
│       ├── speckit-converge/SKILL.md        # [MODIFIED] Refactored to script-free agent ops
│       ├── speckit-implement/SKILL.md       # [MODIFIED] Refactored to script-free agent ops
│       ├── speckit-orchestrate/SKILL.md     # [MODIFIED] Refactored to script-free agent ops
│       ├── speckit-plan/SKILL.md            # [MODIFIED] Refactored to script-free agent ops
│       ├── speckit-specify/SKILL.md         # [MODIFIED] Refactored to script-free agent ops
│       └── speckit-tasks/SKILL.md           # [MODIFIED] Refactored to script-free agent ops
│
├── .specify/
│   ├── extensions/
│   │   ├── .registry                        # [NEW] Extension priority registry
│   │   └── speckit-orchestrator/            # [NEW] Packaged orchestrator extension
│   │       └── extension.yml
│   ├── presets/
│   │   ├── .registry                        # [NEW] Preset priority registry
│   │   └── base-governance/                 # [NEW] Packaged base governance preset
│   │       ├── preset.yml
│   │       └── templates/
│   │           ├── coding-standards-template.md
│   │           ├── constitution-template.md
│   │           └── logging-standards-template.md
│   ├── templates/
│   │   ├── checklist-template.md            # Core fallback template
│   │   ├── coding-standards-template.md     # Core fallback template (synchronized)
│   │   ├── constitution-template.md         # Core fallback template (synchronized)
│   │   ├── logging-standards-template.md    # Core fallback template (synchronized)
│   │   ├── plan-template.md                 # Core fallback template
│   │   ├── spec-template.md                 # Core fallback template
│   │   └── tasks-template.md                # Core fallback template
│   ├── memory/                              # [PROTECTED USER STATE - IMMUTABLE]
│   │   ├── constitution.md                  # [MODIFIED] Pre-PR verification updated
│   │   ├── coding-standards.md
│   │   └── logging-standards.md
│   ├── integrations/
│   │   ├── agy.manifest.json                # [MODIFIED] Synchronized with 11 script-free skills
│   │   ├── speckit.manifest.json            # [MODIFIED] Script entries cleanly purged
│   │   └── speckit-bootstrap.manifest.json  # [NEW] Cryptographic SHA-256 install manifest
│   ├── workflows/
│   │   ├── workflow-registry.json
│   │   └── speckit/workflow.yml
│   ├── extensions.yml                       # Active hook configurations
│   ├── init-options.json
│   ├── integration.json
│   ├── feature.json                         # [PROTECTED USER STATE - IMMUTABLE]
│   ├── .gitignore
│   └── scripts/                             # [DELETED] Entire scripts/ directory removed
│       └── bash/
│           ├── check-prerequisites.sh       # [DELETED]
│           ├── common.sh                    # [DELETED]
│           ├── create-new-feature.sh        # [DELETED]
│           ├── resolve-template.sh          # [DELETED]
│           ├── setup-plan.sh                # [DELETED]
│           └── setup-tasks.sh               # [DELETED]
```

**Structure Decision**: Selected root-level seeder scripts alongside the standard `.specify/` and `.agents/` layout. Removed `.specify/scripts/` completely in accordance with FR-001 and SC-001. Packaged presets and extensions under `.specify/presets/` and `.specify/extensions/` to conform to the 4-tier template inheritance standard.

---

## Complexity Tracking

> *No constitutional violations or unjustified complexities identified. Principle III test generation exemption is fully ratified in Constitution v2.0.0.*

| Violation / Exemption | Why Needed | Simpler Alternative Rejected Because |
|-----------------------|------------|-------------------------------------|
| Principle III (No Automated Tests) | Explicit human authority directive ratified in Constitution v2.0.0. Eliminates test suites in favor of static verification. | Generating unit tests was explicitly rejected by project stakeholders. |
