# Implementation Plan: Add --update Flag to speckit-orchestrate for Non-Destructive Architectural Replanning

**Branch**: `011-orchestrate-update-flag` | **Date**: 2026-11-06 | **Spec**: [spec.md](specs/011-orchestrate-update-flag/spec.md)

**Input**: Feature specification from `/specs/011-orchestrate-update-flag/spec.md`

## Summary

Implement an `--update='<description>'` CLI flag (with alias `--amend='<description>'`) in `speckit-orchestrate` to handle systematic architectural updates to existing plans without performing a cold reset or overwriting existing work:
1. Parse `--update` / `--amend` flags with flexible quoting (`--update='...'`, `--update="..."`, `--update <desc>`) and normalize to `UPDATE_DESCRIPTION` and `IS_UPDATE_MODE=true`.
2. Enforce fail-closed boundary guards: fail closed immediately with `CRITICAL` diagnostics if `UPDATE_DESCRIPTION` is empty, or if `spec.md` or `plan.md` is missing from the active feature directory.
3. Keep core `speckit-plan` skill unmodified (FR-007) by injecting replanning directives into subagent dispatch payloads (`speckit-reasoner` and `speckit-executor`).
4. Ensure non-destructive artifact modification across Stages 1, 3, 4, 5, preserving 100% of completed `- [x]` tasks in `tasks.md`.
5. Maintain the default Pre-Implementation Checkpoint pause after Stage 5 (`analyze`) unless `--continue` is specified.
6. Maintain 100% byte parity between `.agents/skills/speckit-orchestrate/SKILL.md` and `.claude/skills/speckit-orchestrate/SKILL.md`.
7. Fulfill Constitution Principle VII by updating `README.md` to document the new `--update` / `--amend` CLI flag.

## Technical Context

**Language/Version**: Markdown (CommonMark / GitHub Flavored Markdown) for Spec Kit agent skill definitions; Bash 4.0+ for CLI automation and static verification scripts.

**Primary Dependencies**: Zero external dependencies. Uses POSIX core utilities (`diff`, `cmp`, `grep`, `sed`).

**Storage**: Local filesystem markdown documents (`specs/011-orchestrate-update-flag/`, `.specify/feature.json`).

**Testing**: Static verification only (Principle III). Zero automated unit/integration test suites repository-wide. Quality verification is conducted through static cross-client file comparison (`diff -u`, `cmp -s`), markdown link checking, and scenario walkthroughs documented in `quickstart.md`.

**Target Platform**: POSIX (Linux, macOS) & Windows (PowerShell) supporting Google Antigravity ([`.agents/`](.agents/)) and Claude Code ([`.claude/`](.claude/)) runtimes.

**Project Type**: Agent skill workflow and CLI orchestrator extension.

**Performance Goals**: Instantaneous argument parsing and flag extraction (<10ms) within orchestrator dispatch loop.

**Constraints**: Dual-client 100% byte parity (`.agents/` and `.claude/`). Immutability of core planning skill (`speckit-plan/SKILL.md`). Fail-closed invariants on missing baseline files or empty descriptions.

**Scale/Scope**: Affects 2 skill files (`.agents/skills/speckit-orchestrate/SKILL.md`, `.claude/skills/speckit-orchestrate/SKILL.md`) and 1 human-facing documentation file (`README.md`).

**Documentation Impact**: `USER_FACING` — Updates root `README.md` under `## Spec Kit Skills & Subagent Orchestration Reference -> ### Custom Skills` to document the new `--update` and `--amend` replanning flags.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

1. **Principle I: Evidence-Based Decisions & Bounded Research**:
   - *Status*: **PASSED**.
   - *Evidence*: Requirements and implementation scope trace directly to `/specs/011-orchestrate-update-flag/spec.md`, `.specify/memory/constitution.md`, `.specify/memory/coding-standards.md`, and upstream `.agents/skills/speckit-orchestrate/SKILL.md`.
2. **Principle II: Explicit Error Handling & Fail-Closed State**:
   - *Status*: **PASSED**.
   - *Evidence*: Explicit `CRITICAL` boundary rejections trigger immediate halt without mutating files when `UPDATE_DESCRIPTION` is empty or when `spec.md` or `plan.md` is missing from the active feature.
3. **Principle III: Static Verification & Quality Gates**:
   - *Status*: **PASSED**.
   - *Evidence*: In full compliance with Principle III, zero automated unit/integration test suites are planned or generated. Quality verification relies on static byte-parity verification (`diff -u`, `cmp -s`), link validation, and `quickstart.md` scenario walkthroughs.
4. **Principle IV: State Ownership, Architectural Seams & Safe Concurrency**:
   - *Status*: **PASSED**.
   - *Evidence*: Single source of truth is maintained in `SPECIFY_FEATURE_DIRECTORY`. Completed tasks (`- [x]`) in `tasks.md` are monotonically preserved.
5. **Principle V: Centralized Dependencies & Toolchain Security**:
   - *Status*: **PASSED**.
   - *Evidence*: Zero external dependencies or toolchain mutations are introduced.
6. **Principle VI: Resource Ceilings & Safe State Mutation**:
   - *Status*: **PASSED**.
   - *Evidence*: Verify-before-mutate guarantees baseline validation before dispatching subagents. Non-destructive amendments prevent data loss.
7. **Principle VII: Code Standards, Consistent Terminology & Secure Logging**:
   - *Status*: **PASSED**.
   - *Evidence*: Strict byte-level parity maintained across `.agents` and `.claude`. Human-facing documentation gate satisfied via `README.md` update. Structured logging adheres to `logging-standards.md`.

## Project Structure

### Documentation (this feature)

```text
specs/011-orchestrate-update-flag/
├── checklists/
│   └── requirements.md                          # Quality checklist (/speckit-checklist output)
├── spec.md                                      # Ratified feature specification
├── plan.md                                      # This file (/speckit-plan output)
├── research.md                                  # Phase 0 research findings
├── data-model.md                                # Phase 1 entities and state machine
├── quickstart.md                                # Phase 1 runnable validation scenarios
├── contracts/
│   └── orchestrate-update-interface.md          # Phase 1 CLI and subagent interface contract
└── tasks.md                                     # Phase 2 output (/speckit-tasks output)
```

### Source Code (repository root)

```text
.agents/skills/speckit-orchestrate/
└── SKILL.md                                     # Google Antigravity orchestrator skill definition

.claude/skills/speckit-orchestrate/
└── SKILL.md                                     # Claude Code orchestrator skill definition (byte parity)

README.md                                        # Human-facing documentation updated under Principle VII
```

**Structure Decision**:
Changes are contained strictly to the orchestrator skill definition in `.agents/skills/speckit-orchestrate/SKILL.md` and mirrored to `.claude/skills/speckit-orchestrate/SKILL.md`. Core `speckit-plan/SKILL.md` remains unmodified. The repository `README.md` is updated to document the new `--update` / `--amend` flag under `USER_FACING` documentation requirements.

## Complexity Tracking

> *Constitution Check passed with zero violations; no complexity tracking entries required.*

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| *None* | — | — |
