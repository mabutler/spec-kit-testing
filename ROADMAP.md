# Spec Kit Customizations & Automation Roadmap

This roadmap organizes the planned enhancements to Spec Kit into sequential, self-contained initiatives. Each phase is designed to be specified (`/speckit-specify`), planned (`/speckit-plan`), and implemented independently in a fresh context.

---

## Overview of Initiatives

| Phase | Initiative | Goal | Key Deliverables |
| :--- | :--- | :--- | :--- |
| **Phase 1** | **Base Governance Suite & Templates** | Establish reusable base templates for the project constitution, coding standards, and logging standards—including support for optional constitution rules/enhancements. | `constitution-template.md`, `coding-standards-template.md`, `logging-standards-template.md` |
| **Phase 2** | **Co-Applied Governance & Constitutional Merge** | Update/create the constitution & standards workflow so all three governance docs are applied and merged intelligently with existing project context and docs. | Updated `speckit-constitution` (or merge skill/extension) generating `.specify/memory/{constitution,coding-standards,logging-standards}.md` |
| **Phase 3** | **Subagent-Driven Spec Kit Orchestrator** | Kick off an intelligent multi-agent pipeline starting from `specify` (or an autopilot entry point) that drives `clarify` → `plan` → `tasks` → `analyze` → `implement`. | Orchestrator skill / `after_specify` hook using subagents |
| **Phase 4** | **Portable Project Bootstrapper** | Package Phases 1–3 so they can be rapidly installed and initialized in any new or existing repository. | Preset/extension bundle + bootstrap installer script/command |

---

## Phase 1: Base Governance Suite & Templates

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

### Key Design Decisions to Resolve During Spec
- **Source Content**: Incorporating the user's base constitution text, optional rule blocks, and baseline coding/logging rules.
- **Optional Rule Syntax**: How optional rules/enhancements are marked in `constitution-template.md` (e.g., structured HTML comments/markers or dedicated optional sections) so agents know how to evaluate, prompt for, or strip unused options.
- **Cross-References**: Standardized relative links from `constitution.md` to `coding-standards.md` and `logging-standards.md`.

---

## Phase 2: Co-Applied Governance & Constitutional Merge

### Problem Statement
1. **Simultaneous Application**: Because the constitution references the coding and logging standards, creating or updating the constitution must simultaneously generate/update `coding-standards.md` and `logging-standards.md`.
2. **Constitutional & Standards Merge**: When applying the base governance templates to an existing project (or updating an existing `.specify/memory/constitution.md`), the workflow must intelligently merge:
   - **Base Non-Negotiable Principles** (preserved/enforced from the base template)
   - **Optional Rules / Enhancements** (activated or omitted based on user input or repository inspection)
   - **Project-Specific Rules & Context** (inferred from existing codebase, README, linters, or prior constitution/standards versions without destructive overwrites)

### Architectural Fit in Spec Kit
- Extends `.agents/skills/speckit-constitution/SKILL.md` (or introduces a companion merge workflow/hook via `.specify/extensions.yml`).
- Ensures downstream skills (`speckit-plan`, `speckit-analyze`, `speckit-implement`) load or respect the linked `coding-standards.md` and `logging-standards.md` alongside `.specify/memory/constitution.md`.

### Key Design Decisions to Resolve During Spec
- **Merge Precedence & Conflict Resolution**: What happens when an existing project convention conflicts with a base template rule (hard error/prompt vs. documented exception).
- **Optional Rule Selection UX**: Interactive checklist vs. automatic repo-context recommendation with confirmation vs. argument flags.
- **Output Locations**: Storing all three files in `.specify/memory/` (`constitution.md`, `coding-standards.md`, `logging-standards.md`) vs. exposing links in `docs/`.

---

## Phase 3: Subagent-Driven Spec Kit Orchestrator

### Problem Statement
Running each Spec Kit step manually (`/speckit-specify` → `/speckit-clarify` → `/speckit-checklist` → `/speckit-plan` → `/speckit-tasks` → `/speckit-analyze` → `/speckit-implement` → `/speckit-converge`) requires repetitive manual handoffs. Starting a session with `specify` (or an orchestrator skill) should intelligently coordinate subagents through the remaining pipeline with clean context isolation per step.

### Proposed Execution Flow
1. **Specify**: Create `spec.md` and run initial quality checklist validation.
2. **Clarify Gate**: If high-impact ambiguities (`[NEEDS CLARIFICATION]`) exist or `speckit-clarify` identifies critical gaps, pause and ask the user; otherwise proceed automatically.
3. **Plan Subagent**: Spawn a subagent to execute `speckit-plan`, producing `plan.md`, `research.md`, `data-model.md`, `contracts/`, and `quickstart.md` in compliance with `constitution.md`, `coding-standards.md`, and `logging-standards.md`.
4. **Tasks Subagent**: Spawn a subagent to execute `speckit-tasks`, generating dependency-ordered `tasks.md`.
5. **Analyze & Self-Heal Gate**: Spawn a subagent to run `speckit-analyze` across `spec.md`, `plan.md`, `tasks.md`, and the governance suite. Automatically remediate minor drift or surface blocking issues to the user.
6. **Implement & Converge Subagents**: Optionally (or after a user approval gate on the plan/tasks) spawn subagents to execute `speckit-implement` and verify completion with `speckit-converge`.

### Architectural Fit in Spec Kit
- Can be triggered via:
  - A dedicated orchestrator skill (e.g., `speckit-autopilot` / `speckit-orchestrate`), AND/OR
  - An extension hook in `.specify/extensions.yml` (`hooks.after_specify`) that launches the subagent pipeline.
- Uses `.specify/feature.json` and `SPECIFY_FEATURE_DIRECTORY` to share feature state cleanly across subagents.

### Key Design Decisions to Resolve During Spec
- **Human-in-the-Loop Checkpoints**: Which transitions run fully autonomously vs. pause for approval (e.g., always pause on clarifications; optional pause before `implement`).
- **Trigger Mechanism**: Standalone skill vs. `after_specify` hook vs. flag passed to `speckit-specify`.
- **Parallelism**: Running independent tasks or checklists in parallel subagents where safe.

---

## Phase 4: Portable Project Bootstrapper

### Problem Statement
All custom templates (Phase 1), merge/co-application workflows (Phase 2), and subagent orchestration skills/hooks (Phase 3) need to be quickly added to new or existing projects without manual file copying.

### Architectural Fit in Spec Kit
- Package the templates and configurations as a **Spec Kit Preset / Extension** (`.specify/presets/` and `.specify/extensions/`) plus `.agents/skills/` definitions.
- Provide a single bootstrapper script or CLI command (e.g., `bootstrap-speckit.sh <target-repo>`) that:
  1. Initializes `.specify/` if not already present.
  2. Installs the custom preset/overrides (`constitution-template`, `coding-standards-template`, `logging-standards-template`).
  3. Installs the updated/custom agent skills into `.agents/skills/` and hooks into `.specify/extensions.yml`.
  4. Optionally triggers the initial Constitutional + Standards Merge against the target repo.

### Key Design Decisions to Resolve During Spec
- **Distribution Format**: Git repository / submodule / tarball / local CLI installer script.
- **Upgrade Path**: How existing projects pull updates to the base templates and skills without overwriting project-local overrides.
