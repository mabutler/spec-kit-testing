# Implementation Plan: Clean Up README and Focus on Unique Repository Capabilities

**Branch**: `010-clean-readme` | **Date**: 2026-11-06 | **Spec**: [specs/010-clean-readme/spec.md](spec.md)

**Input**: Feature specification from `/specs/010-clean-readme/spec.md`

<!--
Template Resolution Hierarchy & FeatureContext Specification:
Resolved via Tier 4 Fallback: .specify/templates/plan-template.md
FeatureContext: specs/010-clean-readme
-->

## Summary

Clean up the repository root `README.md` by eliminating generic template governance boilerplate (the full Principles I–VII matrix and the optional modules list) and standard upstream GitHub Spec Kit command catalogs. Reorganize `README.md` into the four canonical sections ratified in `.specify/memory/coding-standards.md` while spotlighting unique repository additions: multi-agent orchestration (`/speckit-orchestrate`), bootstrapper scripts (`bootstrap-speckit.{sh,ps1}`), SHA-256 integrity verification (`/speckit-bootstrap`), roadmap tracking (`/speckit-roadmap`), dual client parity (`.agents/` and `.claude/`), and dynamic constitutional governance. The total line count is reduced by at least 25% (from 137 to $\le 104$ lines).

## Technical Context

**Language/Version**: CommonMark / GitHub Flavored Markdown (GFM); POSIX Bash 4.0+ for validation commands

**Primary Dependencies**: None (zero third-party or external dependencies; uses standard core utilities `bash`, `diff`, `cmp`, `grep`)

**Storage**: Markdown document at repository root (`README.md`)

**Testing**: None (Principle III static verification; zero automated unit or integration tests repository-wide)

**Target Platform**: Cross-platform documentation readable on GitHub / web and validated on Linux, macOS, and Windows (PowerShell)

**Project Type**: Multi-agent Spec Kit governance & documentation toolkit

**Performance Goals**: N/A (Static markdown rendering and instantaneous validation commands)

**Constraints**: Line count budget $\le 104$ lines ($\ge 25\%$ reduction from 137 lines); 100% relative link resolution; 0 broken verification commands; strictly 4 canonical sections

**Scale/Scope**: 1 user-facing document (`README.md`)

**Documentation Impact**: USER_FACING (Updates `README.md` to conform to canonical 4-section architecture; no changes to `ROADMAP.md` required as phase scope is unchanged)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Check | Status | Justification / Implementation Evidence |
|-----------|-------|--------|-----------------------------------------|
| **I. Evidence-Based Decisions** | Verified requirements authority | PASS | README content traces directly to ratified governance in `.specify/memory/` and existing scripts. |
| **II. Explicit Error Handling** | Fail closed on invalid state | PASS | Missing link targets or exceeding the line count ceiling fails static verification immediately. |
| **III. Static Verification** | Zero automated tests required | PASS | Testing rules strictly adhere to Principle III: static link checks, heading pattern matching, line counts, and script syntax verification. Zero test harnesses generated. |
| **IV. State Ownership** | Single source of truth | PASS | Governance details remain exclusively in `.specify/memory/`; README holds concise pointers, preventing redundant divergent copies. |
| **V. Centralized Dependencies** | Toolchain security | PASS | No dependencies added or modified. |
| **VI. Resource Ceilings** | Bounded input / line count | PASS | Strict line ceiling enforced ($\le 104$ lines, $\ge 25\%$ reduction from 137). |
| **VII. Code Standards & Docs** | Canonical README structure | PASS | Fully implements the 4 canonical sections defined in `.specify/memory/coding-standards.md` line 69. |

*Gate Evaluation*: All gates PASS. No constitutional violations.

## Project Structure

### Documentation (this feature)

```text
specs/010-clean-readme/
├── spec.md              # Feature specification
├── plan.md              # Implementation plan (this document)
├── research.md          # Phase 0 architectural analysis & decisions
├── data-model.md        # Phase 1 conceptual entities & constraints
├── quickstart.md        # Phase 1 static verification scenario guide
├── contracts/           # Phase 1 interface & document schemas
│   └── readme-schema.md # Canonical 4-section schema contract for README.md
└── checklists/
    └── requirements.md  # Requirements quality checklist
```

### Source Code (repository root)

```text
/home/admin/projects/spec-kit-testing/
├── README.md                            # Target file to be restructured
├── bootstrap-speckit.sh                 # Verified installer referenced in Section 4
├── bootstrap-speckit.ps1                # Verified Windows installer referenced in Section 4
├── ROADMAP.md                           # Strategic roadmap referenced in Section 3
├── .specify/
│   ├── memory/                          # Authoritative governance suite
│   │   ├── constitution.md              # Referenced in Section 2
│   │   ├── coding-standards.md          # Referenced in Section 2
│   │   └── logging-standards.md         # Referenced in Section 2
│   ├── templates/                       # Fallback templates referenced in Section 1
│   └── presets/base-governance/         # Preset templates referenced in Section 1
├── .agents/                             # Antigravity agents & skills referenced in Section 1 & 3
└── .claude/                             # Claude Code agents & skills referenced in Section 1 & 3
```

**Structure Decision**: Direct in-place restructuring of `README.md` at repository root. No application source code directories or test files are touched.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

*No violations. All principles and gates pass cleanly.*
