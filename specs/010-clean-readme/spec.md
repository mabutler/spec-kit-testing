# Feature Specification: Clean Up README and Focus on Unique Repository Capabilities

**Feature Branch**: `010-clean-readme`

**Created**: 2026-11-06

**Status**: Draft

**Input**: User description: "Clean up the readme. It still references some things that aren't unique to the project"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Remove Generic Template Governance Boilerplate (Priority: P1)

As a developer or evaluator exploring this repository, I want `README.md` to communicate the specific extensions and tools this repository adds to GitHub Spec Kit, without being cluttered by generic template governance tables (such as full tables of baseline software engineering principles or optional module lists) that belong inside the template files themselves.

**Why this priority**: The README is the primary entry point for users. Cluttering it with internal template options and generic principle definitions distracts from understanding what this project actually is and how to use it.

**Independent Test**: Can be tested by reviewing `README.md` to confirm that the full Core Principles table (Principles I–VII) and the Optional Modules list (`MODULE-A` through `TRACE`) have been removed and replaced with concise descriptions and direct links to `.specify/memory/constitution.md` and `.specify/templates/`.

**Acceptance Scenarios**:

1. **Given** `README.md`, **When** the Governance section is read, **Then** it summarizes the governance suite and provides links to `.specify/memory/constitution.md`, `coding-standards.md`, and `logging-standards.md` without reproducing full generic principle matrices.
2. **Given** `README.md`, **When** inspected for template configuration details, **Then** the optional module catalog (`MODULE-A` through `MODULE-DOCS`) is omitted from the main README and deferred to the governance template files and presets.

---

### User Story 2 - Focus Tooling & Skills on Unique Additions (Priority: P1)

As a developer evaluating or using the repository's workflows, I want the skills and agent documentation in `README.md` to spotlight the unique capabilities added by this project (such as `/speckit-orchestrate`, `/speckit-bootstrap`, `/speckit-roadmap`, and subagent personas) rather than listing standard upstream Spec Kit skills in an exhaustive reference table.

**Why this priority**: Upstream GitHub Spec Kit already documents standard skills (`specify`, `plan`, `tasks`, `implement`). Documenting every standard skill in a monolithic table creates noise and obscures the distinct extensions provided here.

**Independent Test**: Can be tested by verifying that the Skills section focuses on the custom orchestrator, bootstrap, and roadmap capabilities, and summarizes how standard Spec Kit stages are enhanced by governance rather than repeating standard command entries.

**Acceptance Scenarios**:

1. **Given** the Skills section in `README.md`, **When** reviewed, **Then** it clearly features the unique skills (`/speckit-orchestrate`, `/speckit-bootstrap`, `/speckit-roadmap`) and the dual subagent personas (`speckit-executor`, `speckit-reasoner`).
2. **Given** standard Spec Kit workflows, **When** referenced in `README.md`, **Then** they are presented concisely as the core pipeline enhanced by the project's governance checks, with reference to upstream documentation for standard usage.

---

### User Story 3 - Highlight Installation, Portability, and Verification (Priority: P2)

As an engineer wanting to install or verify these extensions in a project, I want clear, straightforward instructions for bootstrapping into any repository with `bootstrap-speckit.sh` / `bootstrap-speckit.ps1` and running repository verification checks.

**Why this priority**: Portability and validation are core value propositions of this repository, enabling teams to seed multi-agent Spec Kit governance into any repository.

**Independent Test**: Can be tested by following the installation and verification check instructions in `README.md` to verify that commands are clear, accurate, and functional.

**Acceptance Scenarios**:

1. **Given** the Installation & Setup section, **When** followed, **Then** the instructions clearly show how to bootstrap a new or existing repository on Linux/macOS and Windows PowerShell.
2. **Given** the Verification Checks section, **When** executed, **Then** commands for checking script syntax, parity between `.agents/` and `.claude/`, and template consistency run as documented.

---

### Edge Cases

- **Users looking for detailed constitutional principles**: Provide a clear link to `.specify/memory/constitution.md` so in-depth principle definitions remain readily accessible without crowding the main README.
- **Users seeking template customization details**: Provide clear links to `.specify/templates/` and `.specify/presets/base-governance/` for developers wanting to inspect or extend template options.
- **Upstream GitHub Spec Kit documentation**: Maintain the top-level link to [GitHub Spec Kit](https://github.com/github/spec-kit) so users can reference upstream docs for standard core commands.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: `README.md` MUST remove the full Core Principles table (Principles I–VII) and replace it with a concise summary linking to `.specify/memory/constitution.md`.
- **FR-002**: `README.md` MUST remove the Optional Modules list (`MODULE-A` through `MODULE-DOCS`, `TRACE`) and point users to template documentation.
- **FR-003**: `README.md` MUST replace the 12-row Skills Reference table with a focused showcase of new/unique extensions (`/speckit-orchestrate`, `/speckit-bootstrap`, `/speckit-roadmap`) and subagents (`speckit-executor`, `speckit-reasoner`).
- **FR-004**: `README.md` MUST concisely describe how standard Spec Kit stages (`specify`, `plan`, `tasks`, `implement`) are enhanced by dynamic constitutional governance rather than cataloging each standard skill individually.
- **FR-005**: `README.md` MUST retain all unique repository value propositions: portable bootstrapper scripts (`bootstrap-speckit.sh`, `bootstrap-speckit.ps1`), 4-tier template resolution, dual-client parity (`.agents/` and `.claude/`), multi-agent orchestration, and strategic roadmap tracking.
- **FR-006**: `README.md` MUST preserve installation instructions, governance initialization instructions, and repository verification check commands.
- **FR-007**: All links (relative file links and external web links) in `README.md` MUST be valid and point to existing files or URLs.

### Key Entities *(include if feature involves data)*

- **README Document**: The primary user-facing markdown document (`README.md`) describing the repository's purpose, features, installation, and verification.
- **Governance Suite**: The collection of project memory documents (`constitution.md`, `coding-standards.md`, `logging-standards.md`) referenced by `README.md`.
- **Spec Kit Extensions**: The set of custom skills, subagents, presets, and installer scripts that differentiate this repository from upstream Spec Kit.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Total line count of `README.md` is reduced by at least 25% (from 137 lines to under 105 lines) through the removal of redundant generic tables.
- **SC-002**: 100% of generic template governance catalogs (full principles table, optional module list) are eliminated from the top-level README.
- **SC-003**: 100% of skills documented in detail in `README.md` represent custom or extended capabilities unique to this repository.
- **SC-004**: All internal markdown file links (`.specify/...`, `bootstrap-speckit.*`) and external links in `README.md` resolve successfully.
- **SC-005**: All verification commands listed in `README.md` execute without errors.

## Assumptions

- Detailed software engineering principles and governance rules are fully maintained in `.specify/memory/constitution.md` and `.specify/templates/constitution-template.md`, so removing them from `README.md` causes zero information loss.
- Detailed optional template modules (`MODULE-A` through `MODULE-DOCS`) are documented in the preset and template files, so removing them from `README.md` keeps the repository overview clean.
- Developers using standard Spec Kit skills can consult upstream GitHub Spec Kit documentation for baseline command syntax.
- Per Constitution Principle III, no automated unit test files are required or created for documentation cleanup.
