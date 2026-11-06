# Spec Kit Testing Coding Standards

## Constitutional Authority & Precedence

This document operationalizes the universal engineering principles established in the **Spec Kit Testing Constitution** into concrete, stack-specific implementation conventions for this repository.

- **Authority Link**: Governed by `.specify/memory/constitution.md`. Universal rules defined in the Constitution (evidence-based decisions, explicit error handling, static verification, state ownership, toolchain security, resource ceilings, and code standards) are not repeated here.
- **Precedence Declaration**: The Constitution ranks highest in authority. In any conflict between this Coding Standards document and the Core Principles of the Constitution, the Constitution strictly prevails.
- **Scope**: Applies to all agent skill workflows (`.agents/skills/`), ratified project governance (`.specify/memory/`), templates (`.specify/templates/`), and CLI automation scripts (`.specify/scripts/bash/`) maintained in this repository.

---

## Language, Runtime & Toolchain

Operationalizes Constitutional Principles V (*Centralized Dependencies & Toolchain Security*) and VII (*Zero Warnings & Read-Only Vendored Code*):

- **Target Platform**: Markdown (CommonMark / GitHub Flavored Markdown) for Spec Kit skill definitions and governance documents; Bash 4.0+ for CLI automation scripts on Linux, macOS, and POSIX environments.
- **Build, Linter & Zero-Warning Gates**: `bash -n` syntax verification for shell scripts; markdown format and link integrity checks with zero warnings.
- **Dependency & Lockfile Conventions**: Zero external runtime dependencies. Built-in Bash 4.0+ commands and POSIX core utilities (`grep`, `sed`, `awk`) only; no third-party package managers or external dependencies required.

---

## Architecture, Module Layout & Compile-Time Boundaries

Operationalizes Constitutional Principle IV (*State Ownership, Architectural Seams & Safe Concurrency*):

- **Project Structure & Layer Organization**: Agent skill definitions in `.agents/skills/speckit-*/SKILL.md`; canonical ratified project governance suite in `.specify/memory/`; template sources in `.specify/templates/`; CLI automation helpers in `.specify/scripts/bash/`.
- **Compile-Time Boundary & I/O Seam Enforcement**: Script execution isolation via strict POSIX flags (`set -euo pipefail`); template source files under `.specify/templates/` are strictly read-only and immutable; governance suite under `.specify/memory/` serves as the single authoritative state.

---

## Error Handling & Failure Idioms

Operationalizes Constitutional Principle II (*Explicit Error Handling & Fail-Closed State*):

- **Canonical Result Types for Rejected Operations**: Distinct non-zero exit codes (e.g. exit 1) with actionable error messages written to stderr; structured JSON error output (e.g., `{"error": "..."}`) for CLI automation helpers.
- **Internal Invariants & Fail-Closed Mechanism**: Strict `set -euo pipefail` in shell scripts; unrecoverable state or missing required files halt immediately with descriptive CRITICAL diagnostics to stderr rather than continuing with corrupted or partial state.

---

## State, Concurrency & Identifier Idioms

Operationalizes Constitutional Principle IV (*State Ownership, Architectural Seams & Safe Concurrency*):

- **Immutable Snapshots & Disambiguated ID Types**: Ratified governance documents and feature specifications are immutable records once ratified; domain concepts use unambiguous identifiers (e.g., `FR-XXX` for functional requirements, `SC-XXX` for success criteria, `TXXX` for task IDs).

---

## Testing Framework & Conventions

Operationalizes Constitutional Principle III (*Static Verification & Quality Gates*):

- **Test Framework, Determinism & Naming**: No automated test suites generated, configured, or permitted. Spec Kit workflows MUST NOT generate test tasks, test directories, or test files. Quality verification is conducted through static syntax verification (`bash -n`), markdown linting, link validation, and CLI acceptance scripts in `.specify/scripts/bash/`.

---

## Naming, Formatting & Code Style

Operationalizes Constitutional Principle VII (*Code Standards, Consistent Terminology & Secure Logging*):

- **Identifier & Code Style Conventions**: kebab-case for skill directory names and shell script filenames; UPPER_SNAKE_CASE for shell environment variables and constants; present-tense, high-signal comments explaining why decisions were made.

---

## Human-Facing Documentation & README Conventions

Operationalizes Constitutional Principle VII (*Code Standards, Consistent Terminology & Secure Logging*):

- **Human-Facing Documentation & README Structure**: The repository root `README.md` serves as the primary human-facing onboarding and usage reference and MUST maintain four canonical sections: (1) Project Overview & Architecture, (2) Co-Applied Governance Suite, (3) Spec Kit Skills & Subagent Orchestration Reference, and (4) Portable Bootstrapping & Verification Quickstart. Any change classified as `USER_FACING` in `plan.md` (adding, removing, or altering skills in `.agents/skills/`, bootstrapper flags in `bootstrap-speckit.{sh,ps1}`, template contracts in `.specify/templates/`, or governance rules) MUST update `README.md` (and `ROADMAP.md` when phase scope changes) in the same pull request. Changes classified as `INTERNAL_ONLY` with an explicit justification in `plan.md` are exempt from artificial `README.md` edits. Human-facing documentation MUST use valid repository-relative links and MUST NEVER cite ephemeral `specs/NNN-*/` directories or `FR-XXX` / `SC-XXX` identifiers.
