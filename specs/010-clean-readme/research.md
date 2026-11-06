# Research: Clean Up README and Focus on Unique Repository Capabilities

**Feature Branch**: `010-clean-readme`  
**Date**: 2026-11-06  
**Status**: Completed  

---

## 1. Architectural Context & Canonical Section Layout

### Background & Problem
The repository root `README.md` previously contained 137 lines across 5 ad-hoc sections. It duplicated generic template governance tables (Principles I–VII table and `MODULE-A` through `TRACE` optional modules list) that belong in `.specify/memory/constitution.md` and `.specify/templates/`, and it included a 12-row table detailing standard upstream GitHub Spec Kit commands (`specify`, `plan`, `tasks`, `implement`).

Furthermore, `.specify/memory/coding-standards.md` explicitly ratifies a 4-section canonical structure for human-facing README documentation:
1. Project Overview & 4-Tier Architecture
2. Co-Applied Governance Suite
3. Spec Kit Skills & Subagent Orchestration Reference
4. Portable Bootstrapping & Verification Quickstart

### Decision: Reorganize into Canonical 4-Tier Structure
Restructure `README.md` strictly into the four canonical sections:
- **Section 1: Project Overview & 4-Tier Architecture**: Explain the project's purpose as an extension of upstream [GitHub Spec Kit](https://github.com/github/spec-kit), detailing the 4-tier template fallback hierarchy (`overrides` -> `presets` -> `extensions` -> `defaults`) and dual client parity across Google Antigravity (`.agents/`) and Claude Code (`.claude/`).
- **Section 2: Co-Applied Governance Suite**: Succinctly describe the tripartite governance model (`constitution.md`, `coding-standards.md`, `logging-standards.md`), link directly to their authoritative paths, and explain the dynamic testing/verification gating model without reproducing redundant principle matrices.
- **Section 3: Spec Kit Skills & Subagent Orchestration Reference**: Highlight the unique orchestrator (`/speckit-orchestrate`), bootstrapper (`/speckit-bootstrap`), and roadmap (`/speckit-roadmap`) skills, document the dual subagent personas (`speckit-reasoner`, `speckit-executor`), and summarize how core pipeline stages are governed without cataloging standard upstream skills individually.
- **Section 4: Portable Bootstrapping & Verification Quickstart**: Consolidate portable installer commands (`bootstrap-speckit.sh` and `bootstrap-speckit.ps1`), governance initialization steps, and repository verification check commands.

### Alternatives Considered
- *Alternative 1*: Maintain the existing 5-section layout and merely prune the rows within tables.  
  *Rejected*: Violates the canonical 4-section standard ratifying README structure in `.specify/memory/coding-standards.md` (Principle VII).
- *Alternative 2*: Remove all mentions of standard Spec Kit pipeline stages.  
  *Rejected*: Users need to understand how the project relates to GitHub Spec Kit and how dynamic governance enhances standard stages.

---

## 2. Redundancy Elimination & Line Count Ceiling

### Background & Metrics
Current `README.md`:
- Total lines: 137 lines.
- Redundant content:
  - Principles table (lines 31–39: 9 lines).
  - Optional Modules list (lines 41–49: 9 lines).
  - Standard Spec Kit rows in Skills table (lines 71–80: 10 lines).
  - Formatting separators and redundant introductory lines (~8 lines).

Target under Success Criteria SC-001:
- Reduction >= 25%: `137 * (1 - 0.25) = 102.75` lines, requiring <= 102 (or <= 104 per SC-001 spec target).
- Target ceiling: ~80 to 95 lines.

### Decision
Eliminate the entire Principles table and Optional Modules list. In Section 2, replace them with a concise 3-bullet list with direct relative links and descriptions. In Section 3, replace the 12-row table with a focused 3-row table (or bulleted list) covering only `/speckit-orchestrate`, `/speckit-bootstrap`, and `/speckit-roadmap`, accompanied by a 2-line summary of subagent personas and a 2-line summary of standard Spec Kit enhancements.

### Alternatives Considered
- *Alternative*: Keeping brief 1-line definitions of principles.  
  *Rejected*: `.specify/memory/constitution.md` is the sole authoritative source for principles per Principle I and IV. Duplicating summaries in the README creates synchronization drift.

---

## 3. Testing & Verification Governance

### Background & Mandate
Principle III in `.specify/memory/constitution.md` states:
> "This project does not generate, require, or maintain automated test suites. All feature delivery and quality verification rely strictly on static analysis, syntax validation, and declarative quality gates."

### Decision
All verification of `README.md` will be performed statically:
1. **Section Heading Conformance**: Verified via grep/regex against canonical titles.
2. **Line Count Budget**: Verified via `wc -l README.md` (must be <= 104).
3. **Boilerplate Omission**: Verified via grep assertions (zero matches for `Principles I`, `MODULE-A`, etc.).
4. **Link Integrity**: Verified via shell checks confirming each local path linked in `README.md` exists on disk.
5. **Command Verifiability**: All verification commands listed in Section 4 (`bash -n`, `diff -r`, `cmp -s`) must run cleanly against the current repository state.

Zero automated unit test files (`*.test.*`, `*_test.*`, `tests/`) will be generated or modified.
