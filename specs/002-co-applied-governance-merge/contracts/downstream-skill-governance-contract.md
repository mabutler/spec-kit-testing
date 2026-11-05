# Interface Contract: Downstream Skill Governance Integration

**Feature**: `002-co-applied-governance-merge`  
**Status**: Completed  
**Artifact**: `specs/002-co-applied-governance-merge/contracts/downstream-skill-governance-contract.md`

## Overview

This contract specifies how the five downstream Spec Kit skills (`speckit-plan`, `speckit-tasks`, `speckit-analyze`, `speckit-implement`, and `speckit-converge`) load, reference, and enforce the Co-Applied Governance Suite (`.specify/memory/constitution.md`, `.specify/memory/coding-standards.md`, and `.specify/memory/logging-standards.md`), including graceful fallback behavior when companion files are absent.

---

## 1. Shared Governance Loading Rule

Whenever any downstream skill loads project governance from `.specify/memory/`:
1. **Primary Authority**: Load `.specify/memory/constitution.md` (if present and not an unpopulated template).
2. **Companion Coding Standards**: Load `.specify/memory/coding-standards.md` (if present and not an unpopulated template).
3. **Companion Logging Standards**: Load `.specify/memory/logging-standards.md` (if present and not an unpopulated template).
4. **Graceful Legacy Fallback**: If `.specify/memory/coding-standards.md` or `.specify/memory/logging-standards.md` does not exist in a legacy repository, continue execution using `.specify/memory/constitution.md` without crashing, noting that the missing companion standard can be initialized by running `/speckit-constitution`.
5. **Precedence**: In any conflict between companion standards and `.specify/memory/constitution.md`, `.specify/memory/constitution.md` strictly prevails.

---

## 2. Per-Skill Integration Requirements

### 2.1 `speckit-plan` (`.agents/skills/speckit-plan/SKILL.md`)

- **Step 2 (Load context)**:
  - Read `FEATURE_SPEC` and the project governance suite in `.specify/memory/`: `constitution.md`, plus `coding-standards.md` and `logging-standards.md` (if present). Load `IMPL_PLAN` template (already copied).
- **Step 3 (Execute plan workflow)**:
  - Use `coding-standards.md` and `logging-standards.md` (when present) to populate stack-specific defaults in `Technical Context` (language/runtime, build/linter commands, test framework, logging framework) when not overridden by the feature spec.
  - In `Constitution Check`, evaluate compliance against `.specify/memory/constitution.md` (including Principle III's requirement to list planned tests and the risks they guard against, or justify skip-allowlist exemptions) as well as architectural boundary, error handling, and logging constraints in `coding-standards.md` and `logging-standards.md`.

### 2.2 `speckit-tasks` (`.agents/skills/speckit-tasks/SKILL.md`)

- **Step 2 (Load design documents)**:
  - Under `IF EXISTS`, load `.specify/memory/constitution.md`, `.specify/memory/coding-standards.md`, and `.specify/memory/logging-standards.md` for project principles, stack-specific coding conventions, and logging/observability constraints.
- **Step 3 (Execute task generation workflow)**:
  - Ensure generated tasks honor compile-time boundary rules, canonical error result types, testing conventions, and structured logging rules defined in the governance suite.

### 2.3 `speckit-analyze` (`.agents/skills/speckit-analyze/SKILL.md`)

- **Operating Constraints (`Constitution Authority`)**:
  - Declare that `.specify/memory/constitution.md` and its linked companion standards (`.specify/memory/coding-standards.md` and `.specify/memory/logging-standards.md`, when present) form the project's governance suite, with `constitution.md` holding supreme non-negotiable authority.
- **Step 2 (`Load Artifacts -> From constitution`)**:
  - Load `.specify/memory/constitution.md`, `.specify/memory/coding-standards.md`, and `.specify/memory/logging-standards.md` (when present) for principle and standards validation.
- **Step 3 (`Build Semantic Models -> Constitution rule set`)**:
  - Extract principle names and `MUST`/`SHOULD` normative statements from `constitution.md` as well as concrete stack/logging `MUST`/`SHOULD` rules from `coding-standards.md` and `logging-standards.md`.
- **Step 4.D (`Constitution Alignment`)**:
  - Flag any requirement, plan element, or task conflicting with a `constitution.md` `MUST` principle or a linked normative rule in `coding-standards.md` / `logging-standards.md`, or missing mandated quality gates (such as Principle III test justification).

### 2.4 `speckit-implement` (`.agents/skills/speckit-implement/SKILL.md`)

- **Step 3 (`Load and analyze the implementation context`)**:
  - Under `IF EXISTS`, read `.specify/memory/constitution.md`, `.specify/memory/coding-standards.md`, and `.specify/memory/logging-standards.md` for constitutional principles, coding conventions, and logging/telemetry rules.
- **Step 6–9 (`Execute implementation` & `Completion validation`)**:
  - Ensure all written code, error handling, tests, and log statements comply with `constitution.md`, `coding-standards.md`, and `logging-standards.md` (including running configured build/linter/acceptance gate commands when verifying completion).

### 2.5 `speckit-converge` (`.agents/skills/speckit-converge/SKILL.md`)

- **Operating Constraints (`Constitution Authority`)**:
  - Reference `.specify/memory/constitution.md` along with its linked companion standards (`.specify/memory/coding-standards.md` and `.specify/memory/logging-standards.md`, when present and populated).
- **Step 1 (`Initialize Convergence Context`)**:
  - Derive paths for `CONSTITUTION = .specify/memory/constitution.md`, `CODING_STANDARDS = .specify/memory/coding-standards.md`, and `LOGGING_STANDARDS = .specify/memory/logging-standards.md` (if present).
- **Step 2 (`Load Artifacts -> From constitution`)**:
  - Extract principle names and `MUST`/`SHOULD` normative statements from `constitution.md`, `coding-standards.md`, and `logging-standards.md` (skipping any file that is absent or an unfilled template).
- **Step 3 (`Build the Intent Inventory`)**:
  - Include buildable obligations from `constitution.md`, `coding-standards.md`, and `logging-standards.md` in the intent inventory so code that contradicts governance `MUST` rules produces `contradicts`/`missing` remediation tasks.
