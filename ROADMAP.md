# Spec Kit Customizations & Automation Roadmap

**Last Updated**: 2026-11-05  
**Governance**: Managed via `/speckit-roadmap` and `.specify/memory/constitution.md`

This roadmap organizes planned strategic initiatives into sequential, self-contained phases. Each phase is designed to be audited (`/speckit-roadmap --status`), specified (`/speckit-roadmap --next` or `/speckit-specify`), planned (`/speckit-plan`), and implemented (`/speckit-implement` / `/speckit-orchestrate`) with full traceability to `specs/NNN-*/`.

---

## Overview of Initiatives

| Phase | Initiative | Status | Prerequisites | Spec | Goal | Key Deliverables |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Phase 1** | **Base Governance Suite & Templates** | `COMPLETED` | None | `specs/001-base-governance-templates/` | Establish reusable base templates for the project constitution, coding standards, and logging standards—including support for optional constitution rules/enhancements. | `constitution-template.md`, `coding-standards-template.md`, `logging-standards-template.md` |
| **Phase 2** | **Co-Applied Governance & Constitutional Merge** | `COMPLETED` | Phase 1 | `specs/002-co-applied-governance-merge/` | Update/create the constitution & standards workflow so all three governance docs are applied and merged intelligently with existing project context and docs. | Updated `speckit-constitution` generating `.specify/memory/{constitution,coding-standards,logging-standards}.md` |
| **Phase 3** | **Subagent-Driven Spec Kit Orchestrator** | `COMPLETED` | Phase 1, Phase 2 | `specs/003-subagent-orchestrator/` | Kick off an intelligent multi-agent pipeline starting from `specify` (or an autopilot entry point) that drives `clarify` → `plan` → `tasks` → `analyze` → `implement`. | Orchestrator skill / `after_specify` hook using subagents |
| **Phase 4** | **Portable Project Bootstrapper** | `COMPLETED` | Phase 1, Phase 2, Phase 3 | `specs/004-portable-project-bootstrapper/` | Package Phases 1–3 so they can be rapidly installed and initialized in any new or existing repository. | Preset/extension bundle + bootstrap installer script/command |
| **Phase 5** | **Roadmap Management (`speckit-roadmap`)** | `COMPLETED` | Phase 1, Phase 2, Phase 3, Phase 4 | `specs/005-roadmap-management/` | Establish a dedicated workflow, template, and agent skill to author, visualize, and incrementally maintain project-level roadmaps that feed into Spec Kit feature specifications. | `roadmap-template.md`, `.agents/skills/speckit-roadmap/SKILL.md`, sync/status tracking CLI scripts |
| **Phase 6** | **Human-Facing Documentation Standards & Governance** | `PLANNED` | Phase 1, Phase 2, Phase 4 | — | Introduce explicit constitutional principles, template standards, and quality gates for authoring and maintaining human-readable documentation (`README.md`, user guides, quickstarts) alongside code changes. | Updated `constitution-template.md`, amended project `.specify/memory/constitution.md`, documentation gates in Spec Kit skills |

---

## Phase 1: Base Governance Suite & Templates

### Metadata
- **Status**: `COMPLETED`
- **Prerequisites**: None
- **Spec Directory**: `specs/001-base-governance-templates/`

### Problem Statement
The default `.specify/templates/constitution-template.md` is an empty placeholder scaffold. A real-world workflow requires:
1. A **Base Constitution Template** containing core non-negotiable principles as well as **optional rules/enhancements** that can be selectively enabled per project.
2. **Companion Standards Templates** referenced by the constitution:
   - **Coding Standards (`coding-standards-template.md`)**: Combines universal baseline coding rules with slots/sections for project-specific conventions (language, framework, architecture, linting, error handling).
   - **Logging Standards (`logging-standards-template.md`)**: Combines universal baseline logging/observability rules (structured logs, log levels, correlation IDs, PII/secret redaction) with project-specific logging libraries and sinks.

### Architectural Fit in Spec Kit
- Spec Kit resolves templates via `.specify/scripts/bash/resolve-template.sh <template-name> --json` (backed by `resolve_template_content` in `.specify/scripts/bash/common.sh`).
- Resolution priority stack:
  1. `.specify/templates/overrides/<template-name>.md`
  2. `.specify/presets/<preset-id>/templates/<template-name>.md` (supports `replace`, `prepend`, `append`, `wrap` via `preset.yml`)
  3. `.specify/extensions/<ext-id>/templates/<template-name>.md`
  4. `.specify/templates/<template-name>.md` (core)

### Key Deliverables
- `.specify/templates/constitution-template.md` (with optional module markers)
- `.specify/templates/coding-standards-template.md`
- `.specify/templates/logging-standards-template.md`
- `.specify/presets/base-governance/` initial preset bundle

### Key Design Decisions to Resolve During Spec
- **Source Content**: Incorporating the user's base constitution text, optional rule blocks, and baseline coding/logging rules.
- **Optional Rule Syntax**: How optional rules/enhancements are marked in `constitution-template.md` (e.g., structured HTML comments/markers or dedicated optional sections) so agents know how to evaluate, prompt for, or strip unused options.
- **Cross-References**: Standardized relative links from `constitution.md` to `coding-standards.md` and `logging-standards.md`.

---

## Phase 2: Co-Applied Governance & Constitutional Merge

### Metadata
- **Status**: `COMPLETED`
- **Prerequisites**: Phase 1
- **Spec Directory**: `specs/002-co-applied-governance-merge/`

### Problem Statement
1. **Simultaneous Application**: Because the constitution references the coding and logging standards, creating or updating the constitution must simultaneously generate/update `coding-standards.md` and `logging-standards.md`.
2. **Constitutional & Standards Merge**: When applying the base governance templates to an existing project (or updating an existing `.specify/memory/constitution.md`), the workflow must intelligently merge:
   - **Base Non-Negotiable Principles** (preserved/enforced from the base template)
   - **Optional Rules / Enhancements** (activated or omitted based on user input or repository inspection)
   - **Project-Specific Rules & Context** (inferred from existing codebase, README, linters, or prior constitution/standards versions without destructive overwrites)

### Architectural Fit in Spec Kit
- Extends `.agents/skills/speckit-constitution/SKILL.md` (or introduces a companion merge workflow/hook via `.specify/extensions.yml`).
- Ensures downstream skills (`speckit-plan`, `speckit-analyze`, `speckit-implement`) load or respect the linked `coding-standards.md` and `logging-standards.md` alongside `.specify/memory/constitution.md`.

### Key Deliverables
- `.agents/skills/speckit-constitution/SKILL.md` (co-applying and merging governance docs)
- `.specify/memory/constitution.md`
- `.specify/memory/coding-standards.md`
- `.specify/memory/logging-standards.md`

### Key Design Decisions to Resolve During Spec
- **Merge Precedence & Conflict Resolution**: What happens when an existing project convention conflicts with a base template rule (hard error/prompt vs. documented exception).
- **Optional Rule Selection UX**: Interactive checklist vs. automatic repo-context recommendation with confirmation vs. argument flags.
- **Output Locations**: Storing all three files in `.specify/memory/` (`constitution.md`, `coding-standards.md`, `logging-standards.md`) vs. exposing links in `docs/`.

---

## Phase 3: Subagent-Driven Spec Kit Orchestrator

### Metadata
- **Status**: `COMPLETED`
- **Prerequisites**: Phase 1, Phase 2
- **Spec Directory**: `specs/003-subagent-orchestrator/`

### Problem Statement
Running each Spec Kit step manually (`/speckit-specify` → `/speckit-clarify` → `/speckit-checklist` → `/speckit-plan` → `/speckit-tasks` → `/speckit-analyze` → `/speckit-implement` → `/speckit-converge`) requires repetitive manual handoffs. Starting a session with `specify` (or an orchestrator skill) should intelligently coordinate subagents through the remaining pipeline with clean context isolation per step.

### Architectural Fit in Spec Kit
- Can be triggered via:
  - A dedicated orchestrator skill (e.g., `speckit-autopilot` / `speckit-orchestrate`), AND/OR
  - An extension hook in `.specify/extensions.yml` (`hooks.after_specify`) that launches the subagent pipeline.
- Uses `.specify/feature.json` and `SPECIFY_FEATURE_DIRECTORY` to share feature state cleanly across subagents.

### Key Deliverables
- `.agents/skills/speckit-orchestrate/SKILL.md`
- `.agents/agents/speckit-executor.md` and `.agents/agents/speckit-reasoner.md` subagent profiles
- `.specify/extensions.yml` with `after_specify` orchestration hook

### Key Design Decisions to Resolve During Spec
- **Human-in-the-Loop Checkpoints**: Which transitions run fully autonomously vs. pause for approval (e.g., always pause on clarifications; optional pause before `implement`).
- **Trigger Mechanism**: Standalone skill vs. `after_specify` hook vs. flag passed to `speckit-specify`.
- **Parallelism**: Running independent tasks or checklists in parallel subagents where safe.

---

## Phase 4: Portable Project Bootstrapper

### Metadata
- **Status**: `COMPLETED`
- **Prerequisites**: Phase 1, Phase 2, Phase 3
- **Spec Directory**: `specs/004-portable-project-bootstrapper/`

### Problem Statement
All custom templates (Phase 1), merge/co-application workflows (Phase 2), and subagent orchestration skills/hooks (Phase 3) need to be quickly added to new or existing projects without manual file copying.

### Architectural Fit in Spec Kit
- Package the templates and configurations as a **Spec Kit Preset / Extension** (`.specify/presets/` and `.specify/extensions/`) plus `.agents/skills/` definitions.
- Provide a single bootstrapper script or CLI command (e.g., `bootstrap-speckit.sh <target-repo>`) that:
  1. Initializes `.specify/` if not already present.
  2. Installs the custom preset/overrides (`constitution-template`, `coding-standards-template`, `logging-standards-template`).
  3. Installs the updated/custom agent skills into `.agents/skills/` and hooks into `.specify/extensions.yml`.
  4. Optionally triggers the initial Constitutional + Standards Merge against the target repo.

### Key Deliverables
- `bootstrap-speckit.sh` (< 150 LOC)
- `bootstrap-speckit.ps1` (< 150 LOC)
- `.agents/skills/speckit-bootstrap/SKILL.md`
- `.specify/integrations/` manifest suite (`speckit.manifest.json`, `agy.manifest.json`, `speckit-bootstrap.manifest.json`)

### Key Design Decisions to Resolve During Spec
- **Distribution Format**: Git repository / submodule / tarball / local CLI installer script.
- **Upgrade Path**: How existing projects pull updates to the base templates and skills without overwriting project-local overrides.

---

## Phase 5: Roadmap Management (`speckit-roadmap`)

### Metadata
- **Status**: `COMPLETED`
- **Prerequisites**: Phase 1, Phase 2, Phase 3, Phase 4
- **Spec Directory**: `specs/005-roadmap-management/`

### Problem Statement
Spec Kit features currently begin at `speckit-specify` (`spec.md`), but projects need higher-level, multi-feature strategic planning before breaking work down into individual `specs/NNN-*` directories. Currently:
1. `ROADMAP.md` is authored and tracked manually with no formal schema, template, or automated status synchronization.
2. There is no automated workflow to scaffold a project roadmap, check implementation status across existing specs/features, or derive new `speckit-specify` proposals directly from roadmap phases.
3. Teams lack a standardized way to keep user-facing high-level roadmaps, architectural vision, and human-readable project overviews aligned with ongoing tactical development.

### Architectural Fit in Spec Kit
- Introduce `.specify/templates/roadmap-template.md` (and preset override support) for standardized roadmap structure (initiatives, phases, prerequisites, deliverables, and status markers).
- Introduce `.agents/skills/speckit-roadmap/SKILL.md` (and optional slash command `/speckit-roadmap`) to:
  1. Scaffold or update `ROADMAP.md` based on high-level goals and architectural vision.
  2. Audit roadmap phases against `specs/` and git status to report phase completion and drift.
  3. Seamlessly seed a new feature specification (`/speckit-specify`) from a selected roadmap initiative.
- Provide native script-free audit, synchronization, and specify handoff modes within `/speckit-roadmap`.

### Key Deliverables
- `.specify/templates/roadmap-template.md`
- `.specify/presets/base-governance/templates/roadmap-template.md`
- `.specify/presets/base-governance/preset.yml` registration
- `.agents/skills/speckit-roadmap/SKILL.md`
- Updated `.agents/skills/speckit-specify/SKILL.md` and `.agents/skills/speckit-bootstrap/SKILL.md`
- Reconciled `ROADMAP.md`

### Key Design Decisions to Resolve During Spec
- **Status Reconciliation**: How `speckit-roadmap` determines whether a phase is `PLANNED`, `IN_PROGRESS`, or `COMPLETED` (e.g., matching feature directories in `specs/`, git commit history, or explicit state markers).
- **Handoff to Specify**: Whether `/speckit-roadmap --next` or interactive selection directly invokes `/speckit-specify` with populated feature scope and background context.
- **Human-Readable Sync**: Standardized conventions for keeping high-level user-facing documentation (`README.md`, `ROADMAP.md`) in sync without duplicating lower-level architectural contracts.

---

## Phase 6: Human-Facing Documentation Standards & Governance

### Metadata
- **Status**: `PLANNED`
- **Prerequisites**: Phase 1, Phase 2, Phase 4
- **Spec Directory**: —

### Problem Statement
The current project constitution (`.specify/memory/constitution.md`) and base constitution templates focus heavily on internal architectural contracts (`Architecture.md`), machine/agent epistemic authority, and in-code comments explaining "why." However:
1. **No Human-Facing Documentation Standard**: There are no explicit constitutional mandates or template rules dictating when and how end-user documentation (e.g., `README.md`, developer onboarding guides, CLI quickstarts, usage tutorials) must be created or updated.
2. **Missing Downstream Verification**: Downstream Spec Kit skills (`speckit-plan`, `speckit-tasks`, `speckit-analyze`, `speckit-implement`) do not verify whether user-facing feature additions include corresponding updates to `README.md` or user guides, leading to documentation drift where internal code passes verification but external docs lag behind.
3. **Template & Active Drift**: Both the base governance templates (`.specify/templates/constitution-template.md`, preset templates) and this repository's active governance files (`.specify/memory/constitution.md`, `.specify/memory/coding-standards.md`) need a unified, ratified standard for human-readable documentation.

### Architectural Fit in Spec Kit
- **Base Constitution Template**: Update `.specify/templates/constitution-template.md` (and preset `base-governance`) to introduce a dedicated rule or optional module (e.g., `MODULE-DOCS` or an expanded Principle VII section) governing human-readable documentation:
  - Defining `README.md` and user-facing documentation requirements (core sections, user workflows, getting started).
  - Explicit rule: Any feature introducing or changing user-visible CLI commands, APIs, configuration options, or behaviors MUST update the corresponding section in `README.md` or user guides within the same pull request.
- **Project Constitution Amendment**: Formally amend this project's `.specify/memory/constitution.md` (and `coding-standards.md`) per constitutional amendment procedures (bump to v2.1.0 or v3.0.0, update top sync comment, record rationale).
- **Skill Alignment**: Update downstream skills:
  - `speckit-plan`: Require identifying affected user documentation (`README.md`, guides) under feature plan outputs.
  - `speckit-tasks`: Require explicit tasks for writing/updating user-facing documentation alongside implementation.
  - `speckit-analyze`: Enforce a quality gate verifying that user-facing changes have associated documentation tasks and changes.

### Key Deliverables
- Updated `constitution-template.md` with human documentation governance module
- Ratified constitutional amendment for `.specify/memory/constitution.md` and `coding-standards.md`
- Documentation quality gates across Spec Kit skills (`plan`, `tasks`, `analyze`, `implement`)

### Key Design Decisions to Resolve During Spec
- **Principle Placement vs. Companion Standard**: Whether documentation standards live directly as an expanded clause in Constitution Principle VII (*Code Hygiene, Ubiquitous Language & Living Documentation*) or as a dedicated section in `coding-standards.md` (or both).
- **Enforcement Scope**: Distinguishing internal-only changes (refactors, bug fixes, testless harness adjustments) from user-facing changes to avoid requiring unnecessary `README.md` edits on purely internal changes.
- **Template Reusability**: Ensuring the documentation module in `constitution-template.md` is configurable for different project types (libraries, CLI tools, web services, frameworks).
