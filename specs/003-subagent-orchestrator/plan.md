# Implementation Plan: Subagent-Driven Spec Kit Orchestrator

**Branch**: `003-subagent-orchestrator` | **Date**: 2026-11-05 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/003-subagent-orchestrator/spec.md`

## Summary

Deliver Phase 3 of `ROADMAP.md` (**Subagent-Driven Spec Kit Orchestrator**) by introducing:
1. **Orchestrator Skill (`.agents/skills/speckit-orchestrate/SKILL.md`)**: Coordinates the complete Spec Kit delivery pipeline (`specify` → `clarify` gate → `plan` → `tasks` → `analyze` & self-heal gate → `implement` → `converge`) across isolated subagent contexts, sharing state exclusively through `.specify/feature.json` and on-disk feature artifacts in `SPECIFY_FEATURE_DIRECTORY`.
2. **Role-Based Subagent Profiles (`.agents/agents/speckit-reasoner.md` & `.agents/agents/speckit-executor.md`)**: Defines two canonical capability roles—**High-Reasoning** (`clarify`, `plan`, `analyze`, `converge`, and retry escalations) and **Standard/Fast Execution** (`specify`, `tasks`, and initial `implement`)—with provider-adaptive model tier mapping (`Argon`/`Pro` → `Flash`, `Opus` → `Sonnet`), a **Session Model Ceiling** that caps subagents at the user's active session model unless overridden, and a 5-level override hierarchy supporting gitignored `.local.md` and per-stage `speckit-<stage>.md` files.
3. **Post-Specify Extension Hook (`.specify/extensions.yml`) & Gitignore Hygiene (`.gitignore`)**: Wires `hooks.after_specify` to `speckit.orchestrate` (`/speckit-orchestrate`, `optional: true` by default with an anti-recursion guard when invoked as a child of `speckit-orchestrate`) and ignores `.agents/agents/*.local.md` in `.gitignore`.

## Technical Context

**Language/Version**: Markdown (CommonMark / GitHub Flavored Markdown with YAML frontmatter) for Spec Kit skill definitions and subagent profiles; YAML 1.2 for `.specify/extensions.yml`; Bash 4.0+ (`set -euo pipefail`) for CLI prerequisite/validation helpers.

**Primary Dependencies**: Zero external runtime dependencies per `.specify/memory/coding-standards.md`. Built-in Antigravity subagent tools (`define_subagent`, `invoke_subagent`, `send_message`), existing Spec Kit scripts (`.specify/scripts/bash/common.sh`, `check-prerequisites.sh`, `setup-plan.sh`, `setup-tasks.sh`, `resolve-template.sh`), and POSIX core utilities (`grep`, `sed`, `awk`) + `python3` (`json`, `yaml`) for static verification.

**Storage**: File-based repository state only: `.specify/feature.json`, `SPECIFY_FEATURE_DIRECTORY/*`, `.specify/memory/{constitution,coding-standards,logging-standards}.md`, `.specify/extensions.yml`, `.agents/agents/speckit-*.md`, and `.agents/skills/speckit-orchestrate/SKILL.md`.

**Testing**: Static verification only (Constitutional Principle III: **No Automated Tests**). Verification uses `bash -n`, YAML/JSON schema checks, Markdown frontmatter/section inspection, `git check-ignore`, and `.specify/scripts/bash/resolve-template.sh constitution-template --json`.

**Target Platform**: Linux, macOS, and POSIX environments running Spec Kit with Google Antigravity (`agy`) or compatible multi-agent CLI/IDE integrations.

**Project Type**: Agent skill workflow & declarative subagent orchestration configuration (`cli` / `agent-skills`).

**Performance Goals**: Zero manual copy-paste handoffs across the 7 pipeline stages; lower execution latency and token consumption on `specify`, `tasks`, and initial `implement` passes via automatic step-down from High-Reasoning (`Argon`/`Pro`/`Opus`) to Fast Execution (`Flash`/`Sonnet`) when beneath the session model ceiling.

**Constraints**:
- Strict single-writer serialization on shared Markdown artifacts (`spec.md`, `plan.md`, `tasks.md`).
- Hard loop ceilings: max **2** self-heal iterations in the `Analyze & Self-Heal Gate`, max **3** convergence passes in the `Implement ↔ Converge` loop.
- Zero automated test files, test directories, or test tasks generated anywhere in the pipeline.

**Scale/Scope**: 1 new orchestrator skill (`.agents/skills/speckit-orchestrate/SKILL.md`), 2 tracked role-based agent definitions (`.agents/agents/speckit-reasoner.md`, `.agents/agents/speckit-executor.md`), 1 extension hook registry (`.specify/extensions.yml`), 1 `.gitignore` update, and integration manifest registration (`.specify/integrations/agy.manifest.json` / `speckit.manifest.json` if applicable).

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle / Companion Standard | Pre-Phase 0 Status | Post-Phase 1 Status | Compliance Evidence & Plan Justification |
| :--- | :--- | :--- | :--- |
| **Principle I: Evidence Over Invention & Bounded Investigation** | PASS | PASS | All orchestrator mechanics trace directly to `specs/003-subagent-orchestrator/spec.md`, `ROADMAP.md` (Phase 3), `.agents/skills/speckit-*/SKILL.md`, and `.specify/scripts/bash/common.sh`. Clarify Gate pauses for human input on any `[NEEDS CLARIFICATION]` marker rather than guessing. |
| **Principle II: Two-Tier Failure Model & Fail Closed on Required State** | PASS | PASS | Missing `spec.md`/feature description, missing subagent output artifacts, `CRITICAL`/`HIGH` analysis findings, or exhausted retry bounds immediately halt pipeline execution (`FAILED_CLOSED`) and log structured `WARN`/`CRITICAL` diagnostics before mutating downstream state. |
| **Principle III: Static Verification & No Automated Tests** | PASS | PASS | **Skip Allowlist Exemption & Justification**: Per ratified Constitution v2.0.0 Principle III and `.specify/memory/coding-standards.md`, automated test generation is disabled repository-wide. Neither this plan nor the orchestrator/subagents will generate unit tests, integration tests, or test tasks. All verification is static (`quickstart.md`). |
| **Principle IV: Single Authoritative State, Enforced Boundaries & Safe Concurrency** | PASS | PASS | `.specify/feature.json` and `SPECIFY_FEATURE_DIRECTORY` are the sole authoritative feature state; `.specify/memory/*` is the sole authoritative governance state. Subagents run with `SPECIFY_FEATURE_NO_PERSIST=1` (after `specify`) and execute sequentially for all shared artifact writes; `[P]` parallelism is restricted to verified disjoint file targets in `implement` with single-coordinator `tasks.md` updates. |
| **Principle V: Centralized Dependencies & Protected Toolchain Gate** | PASS | PASS | Zero third-party packages or toolchain modifications introduced. Uses only standard Markdown, YAML, and existing POSIX/Bash scripts. |
| **Principle VI: Bounded Resources & Verify-Before-Destroy** | PASS | PASS | All retry loops have explicit hard ceilings (Analyze self-heal ≤ 2 iterations; Implement ↔ Converge ≤ 3 iterations). Progressive resumption skips already-completed artifacts unless `--from=<stage>` is explicitly passed; standalone `/speckit-specify` defaults `hooks.after_specify` to `optional: true`. |
| **Principle VII: Code Hygiene, Ubiquitous Language & Safe Logging** | PASS | PASS | Follows kebab-case naming (`speckit-orchestrate`, `speckit-reasoner`, `speckit-executor`), canonical Spec Kit terminology, and `.specify/memory/logging-standards.md` severity taxonomy (`CRITICAL`, `WARN`, `INFO`, `DEBUG`) with zero secrets/PII in logs or summaries. |
| **Companion Standards Alignment (`coding-standards.md` & `logging-standards.md`)** | PASS | PASS | Markdown/YAML/Bash conventions, read-only `.specify/templates/` boundary, and structured stage telemetry align 100% with `.specify/memory/coding-standards.md` and `.specify/memory/logging-standards.md`. |

**Gate Evaluation**: **PASSED** (0 violations; 0 unresolved clarifications).

## Project Structure

### Documentation (this feature)

```text
specs/003-subagent-orchestrator/
├── spec.md                                  # Feature specification (/speckit-specify + /speckit-clarify)
├── checklists/
│   └── requirements.md                      # Specification quality checklist (16/16 passing)
├── plan.md                                  # This file (/speckit-plan command output)
├── research.md                              # Phase 0 research decisions (/speckit-plan command)
├── data-model.md                            # Phase 1 entity schemas & state machine (/speckit-plan command)
├── quickstart.md                            # Phase 1 static validation & run guide (/speckit-plan command)
├── contracts/                               # Phase 1 interface contracts (/speckit-plan command)
│   ├── orchestrate-command-contract.md      # /speckit-orchestrate CLI/skill flags, gates & summary schema
│   ├── agent-profile-contract.md            # .agents/agents/ schema, model ceiling & subagent dispatch contract
│   └── extensions-hook-contract.md          # .specify/extensions.yml hooks.after_specify contract
└── tasks.md                                 # Phase 2 output (/speckit-tasks command - NOT created by /speckit-plan)
```

### Source Code (repository root)

```text
.agents/
├── agents/
│   ├── speckit-reasoner.md                  # NEW: High-Reasoning subagent profile (clarify, plan, analyze, converge, retries)
│   ├── speckit-executor.md                  # NEW: Standard/Fast Execution subagent profile (specify, tasks, initial implement)
│   └── *.local.md                           # GITIGNORED: Optional developer-local role or stage overrides
└── skills/
    ├── speckit-orchestrate/
    │   └── SKILL.md                         # NEW: End-to-end subagent pipeline orchestrator skill
    ├── speckit-specify/SKILL.md             # EXISTING: Consumes .specify/extensions.yml (hooks.after_specify)
    ├── speckit-clarify/SKILL.md             # EXISTING: Dispatched by Clarify Gate via speckit-reasoner
    ├── speckit-plan/SKILL.md                # EXISTING: Dispatched by Plan Stage via speckit-reasoner
    ├── speckit-tasks/SKILL.md               # EXISTING: Dispatched by Tasks Stage via speckit-executor
    ├── speckit-analyze/SKILL.md             # EXISTING: Dispatched by Analyze Gate via speckit-reasoner
    ├── speckit-implement/SKILL.md           # EXISTING: Dispatched by Implement Stage via speckit-executor / speckit-reasoner
    └── speckit-converge/SKILL.md            # EXISTING: Dispatched by Converge Gate via speckit-reasoner

.specify/
├── extensions.yml                           # NEW: Registers speckit.orchestrate under hooks.after_specify
├── feature.json                             # EXISTING: Single authoritative active feature pointer
├── memory/
│   ├── constitution.md                      # EXISTING: Project Constitution (v2.0.0)
│   ├── coding-standards.md                  # EXISTING: Co-applied Coding Standards
│   └── logging-standards.md                 # EXISTING: Co-applied Logging Standards
└── scripts/bash/
    ├── common.sh                            # EXISTING: Path resolution & SPECIFY_FEATURE_NO_PERSIST support
    ├── check-prerequisites.sh               # EXISTING: Prerequisite & artifact verification
    ├── setup-plan.sh                        # EXISTING: Plan initialization
    ├── setup-tasks.sh                       # EXISTING: Tasks initialization
    └── resolve-template.sh                  # EXISTING: Template stack resolver

.gitignore                                   # MODIFIED: Add .agents/agents/*.local.md exclusion
```

**Structure Decision**: Extends the existing Spec Kit repository layout in place by adding `.agents/agents/speckit-{reasoner,executor}.md`, `.agents/skills/speckit-orchestrate/SKILL.md`, `.specify/extensions.yml`, and the `.agents/agents/*.local.md` rule in `.gitignore`. No existing `.specify/templates/` files or core `.specify/scripts/bash/` scripts require destructive modification.

## Complexity Tracking

*No constitutional violations or deviations exist; table omitted per template instructions.*
