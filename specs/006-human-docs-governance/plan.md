# Implementation Plan: Human-Facing Documentation Standards & Governance

**Branch**: `006-human-docs-governance` | **Date**: 2026-11-05 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/006-human-docs-governance/spec.md`

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

Establish comprehensive Human-Facing Documentation Standards & Governance (Phase 6 of `ROADMAP.md`) across the Spec Kit governance templates, active repository governance suite, root `README.md`, downstream agent skills, and integration manifests:
1. **Base Governance Templates & `/speckit-constitution` (`FR-001`–`FR-003`)**: Expand Principle VII in `.specify/templates/constitution-template.md` and `.specify/presets/base-governance/templates/constitution-template.md` with a mandatory baseline **Human-Facing Documentation Synchronization** rule and an optional `MODULE-DOCS` (*Structured Human-Facing Documentation Gate*) block; add a **Human-Facing Documentation & README Conventions** section with slot `[HUMAN_DOCS_CONVENTIONS]` to `.specify/templates/coding-standards-template.md` and `.specify/presets/base-governance/templates/coding-standards-template.md`; update `.agents/skills/speckit-constitution/SKILL.md` to process `MODULE-DOCS` (`ENABLED` | `OMITTED`) and all 26 tracked placeholder slots (`8` in `constitution.md`, `12` in `coding-standards.md`, `6` in `logging-standards.md`).
2. **Active Repository Governance Amendment & Canonical `README.md` (`FR-004`–`FR-005`)**: Amend `.specify/memory/constitution.md` (`2.0.0 -> 2.1.0`, `Last Amended: 2026-11-05`) with `MODULE-DOCS: ENABLED` and updated `Sync Impact Report`; update `.specify/memory/coding-standards.md` with concrete human-facing documentation conventions; author a complete root `README.md` covering project architecture, the Co-Applied Governance Suite, all 11 Spec Kit skills, subagent role profiles, and cross-platform bootstrapping (`bootstrap-speckit.sh` and `bootstrap-speckit.ps1`).
3. **Downstream Skill Documentation Impact Gates & Manifest Sync (`FR-006`–`FR-009`)**: Update `.specify/templates/{plan-template,tasks-template}.md` and `.agents/skills/speckit-{plan,tasks,analyze,implement,converge}/SKILL.md` to enforce explicit `Documentation Impact` classification (`USER_FACING` vs. `INTERNAL_ONLY`), and synchronize SHA-256 digests and byte sizes across `.specify/integrations/{speckit,agy,speckit-bootstrap}.manifest.json`.

## Technical Context

**Language/Version**: Markdown (CommonMark / GitHub Flavored Markdown) for governance templates, agent skills, and `README.md`; JSON for integration manifests; POSIX Bash 4.0+ (`set -euo pipefail`) for static validation gates.

**Primary Dependencies**: Zero external runtime dependencies (per `.specify/memory/coding-standards.md`); standard POSIX utilities (`cmp`, `grep`, `sha256sum`) for static verification.

**Storage**: Git-tracked flat files in `.specify/`, `.agents/`, and repository root (`README.md`).

**Testing**: Static verification ONLY (`bash -n`, byte-for-byte `cmp`, placeholder/marker regex checks, relative link checks, and SHA-256 manifest verification) per Constitutional Principle III (*Static Verification & No Automated Tests*). Zero automated test files, test directories, or test tasks.

**Target Platform**: Cross-platform Spec Kit workspace (Linux, macOS, Windows via POSIX Bash / PowerShell 7+ and Google Antigravity agent skills).

**Project Type**: Agent skill framework, governance template suite, and portable bootstrapper toolkit.

**Performance Goals**: Instantaneous static template resolution and deterministic single-pass skill evaluation.

**Constraints**:
- Strict 100% byte-for-byte parity between `.specify/templates/{constitution,coding-standards}-template.md` and `.specify/presets/base-governance/templates/{constitution,coding-standards}-template.md`.
- Zero unresolved `[ALL_CAPS_IDENTIFIER]` tokens or `OPTIONAL-MODULE` comment tags in `.specify/memory/{constitution,coding-standards,logging-standards}.md`.
- Zero references to ephemeral `specs/NNN-*/` folders or `FR-XXX`/`SC-XXX` identifiers in `README.md` or `.specify/memory/`.
- 100% SHA-256 digest and `size_bytes` alignment across `.specify/integrations/{speckit,agy,speckit-bootstrap}.manifest.json`.

**Scale/Scope**: 16 repository files created or updated across `.specify/templates/`, `.specify/presets/base-governance/templates/`, `.specify/memory/`, `.agents/skills/`, `.specify/integrations/`, and root `README.md`.

**Documentation Impact**: `USER_FACING` — Target human-facing documentation files: `README.md` (created at repository root as the canonical human-facing onboarding and skill reference), `.specify/memory/constitution.md` (amended to `v2.1.0`), and `.specify/memory/coding-standards.md` (updated with Human-Facing Documentation & README Conventions).

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Pre-Phase 0 & Post-Phase 1 Gate Evaluation

| Principle / Standard | Status | Gate Verification & Justification |
|----------------------|--------|-----------------------------------|
| **Principle I (Evidence Over Invention)** | PASS | All template structures, slot counts (`8 + 12 + 6 = 26`), skill step numbers, and manifest schemas were verified directly against on-disk files in [research.md](research.md). |
| **Principle II (Two-Tier Failure Model & Fail Closed)** | PASS | Downstream skills (`speckit-plan`, `speckit-tasks`, `speckit-analyze`, `speckit-implement`, `speckit-converge`) fail closed when required artifacts are missing and degrade gracefully when inspecting legacy `coding-standards.md` files ratified prior to Phase 6. |
| **Principle III (Static Verification & No Automated Tests)** | PASS | **Skip Allowlist / Plan Justification**: Per active `.specify/memory/constitution.md` v2.0.0 Principle III, automated test generation is disabled repository-wide. This plan generates **0** test files, **0** test directories, and **0** test tasks. Verification is performed exclusively via static checks in [quickstart.md](quickstart.md). |
| **Principle IV (Single Authoritative State & Boundaries)** | PASS | `.specify/memory/` remains the single authoritative governance state; `.specify/templates/` and `.specify/presets/base-governance/templates/` remain read-only template sources during skill execution; `.specify/feature.json` is respected without sidecars. |
| **Principle V (Centralized Dependencies & Toolchain Gate)** | PASS | Zero third-party packages or external dependencies added or modified. |
| **Principle VI (Bounded Resources & Verify-Before-Destroy)** | PASS | All file edits are bounded, deterministic markdown and JSON manifest updates; `/speckit-converge` preserves its strict append-only invariant on `tasks.md`. |
| **Principle VII (Code Hygiene, Ubiquitous Language & Safe Logging)** | PASS | Expands Principle VII with baseline Human-Facing Documentation Synchronization and optional `MODULE-DOCS`, co-applies `[HUMAN_DOCS_CONVENTIONS]` in `coding-standards.md`, authors root `README.md` (`Documentation Impact: USER_FACING`), and ensures zero ephemeral `specs/NNN-*/` or `FR-XXX` citations outside `specs/`. |
| **Companion Standards (`coding-standards.md` & `logging-standards.md`)** | PASS | Complies with Markdown/GFM formatting, kebab-case naming, and structured severity taxonomy (`CRITICAL`, `WARN`, `INFO`, `DEBUG`) with zero sensitive data output. |

## Project Structure

### Documentation (this feature)

```text
specs/006-human-docs-governance/
├── plan.md                                             # This file (/speckit-plan command output)
├── research.md                                         # Phase 0 output (/speckit-plan command)
├── data-model.md                                       # Phase 1 output (/speckit-plan command)
├── quickstart.md                                       # Phase 1 output (/speckit-plan command)
├── contracts/                                          # Phase 1 output (/speckit-plan command)
│   ├── governance-templates-contract.md                # Contract for MODULE-DOCS, [HUMAN_DOCS_CONVENTIONS] & speckit-constitution
│   ├── documentation-impact-gate-contract.md           # Contract for plan/tasks/analyze/implement/converge gates
│   └── readme-and-active-governance-contract.md        # Contract for constitution v2.1.0, coding-standards, README.md & manifests
└── tasks.md                                            # Phase 2 output (/speckit-tasks command - NOT created by /speckit-plan)
```

### Source Code & Repository Touch-Points (repository root)

```text
README.md                                               # NEW: Canonical human-facing project overview, governance, skills & bootstrap guide
.specify/
├── memory/
│   ├── constitution.md                                 # UPDATE: Amend v2.0.0 -> v2.1.0, enable MODULE-DOCS, update Sync Impact Report
│   ├── coding-standards.md                             # UPDATE: Add Human-Facing Documentation & README Conventions section
│   └── logging-standards.md                            # UNCHANGED: Verified for 0 residual placeholders and project name parity
├── templates/
│   ├── constitution-template.md                        # UPDATE: Expand Principle VII baseline doc sync + add OPTIONAL-MODULE: MODULE-DOCS
│   ├── coding-standards-template.md                    # UPDATE: Add Human-Facing Documentation section + [HUMAN_DOCS_CONVENTIONS] slot
│   ├── plan-template.md                                # UPDATE: Add Documentation Impact (USER_FACING | INTERNAL_ONLY) to Technical Context & Constitution Check
│   └── tasks-template.md                               # UPDATE: Document conditional USER_FACING vs INTERNAL_ONLY documentation task generation
├── presets/
│   └── base-governance/
│       └── templates/
│           ├── constitution-template.md                # UPDATE: Maintain 100% byte-for-byte parity with .specify/templates/constitution-template.md
│           └── coding-standards-template.md            # UPDATE: Maintain 100% byte-for-byte parity with .specify/templates/coding-standards-template.md
└── integrations/
    ├── speckit.manifest.json                           # UPDATE: Synchronize SHA-256 digests for modified .specify/templates/*.md
    ├── agy.manifest.json                               # UPDATE: Synchronize SHA-256 digests for modified .agents/skills/*/SKILL.md
    └── speckit-bootstrap.manifest.json                 # UPDATE: Synchronize SHA-256 digests and size_bytes for all modified managed assets
.agents/
└── skills/
    ├── speckit-constitution/SKILL.md                   # UPDATE: Support MODULE-DOCS (ENABLED|OMITTED) and 26 slots including [HUMAN_DOCS_CONVENTIONS]
    ├── speckit-plan/SKILL.md                           # UPDATE: Require Documentation Impact classification and Principle VII check
    ├── speckit-tasks/SKILL.md                          # UPDATE: Generate explicit doc tasks when USER_FACING; omit artificial README churn when INTERNAL_ONLY
    ├── speckit-analyze/SKILL.md                        # UPDATE: Flag missing doc tasks on USER_FACING changes or invalid INTERNAL_ONLY claims
    ├── speckit-implement/SKILL.md                      # UPDATE: Validate completed USER_FACING doc updates, relative links & zero ephemeral spec citations
    └── speckit-converge/SKILL.md                       # UPDATE: Audit USER_FACING doc targets against as-built behavior during convergence
```

**Structure Decision**: The repository uses a declarative Spec Kit toolkit layout rooted at `.specify/` (governance state, templates, presets, and integration manifests), `.agents/skills/` (agent skill definitions), and root `README.md` (human-facing documentation). In accordance with Constitutional Principle III, no `tests/` directory is created or used.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| *None* | *All gates pass cleanly without constitutional deviations.* | *N/A* |
