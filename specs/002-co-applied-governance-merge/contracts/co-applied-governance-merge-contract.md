# Interface Contract: Co-Applied Governance Merge Workflow (`speckit-constitution`)

**Feature**: `002-co-applied-governance-merge`  
**Status**: Completed  
**Artifact**: `specs/002-co-applied-governance-merge/contracts/co-applied-governance-merge-contract.md`

## Overview

This contract defines the execution interface, Scope Guard rules, template resolution mechanics, optional module transformation algorithm, placeholder merge precedence, conflict resolution protocol, and output validation invariants for `.agents/skills/speckit-constitution/SKILL.md`.

---

## 1. Command Interface & Scope Guard

- **Skill Name**: `speckit-constitution`
- **Skill Definition Path**: `.agents/skills/speckit-constitution/SKILL.md`
- **Authorized Output Paths (Read/Write)**:
  1. `.specify/memory/constitution.md`
  2. `.specify/memory/coding-standards.md`
  3. `.specify/memory/logging-standards.md`
- **Read-Only Inputs**:
  - Template resolution outputs for `constitution-template`, `coding-standards-template`, `logging-standards-template`
  - Existing files in `.specify/memory/`
  - Repository context files (`README.md`, `Architecture.md`, `ROADMAP.md`, `CodingStandards.md`, `docs/logging.md`, `reference/open-questions.md`, build/package/linter manifests)
  - `.specify/extensions.yml` (for `hooks.before_constitution` and `hooks.after_constitution`)
- **Prohibited Modifications (Scope Guard)**:
  - MUST NOT modify any file under `.specify/templates/`, `.specify/presets/`, or `.specify/extensions/`.
  - MUST NOT create, modify, or delete application source files, tests, scripts, or feature specs.
  - Non-governance requests in `$ARGUMENTS` MUST be extracted without execution and listed under a `Next Actions` section in the completion report with the recommended follow-up Spec Kit command (e.g., `/speckit-specify`).

---

## 2. Template Resolution Contract

For each of the three template identifiers (`constitution-template`, `coding-standards-template`, `logging-standards-template`):

1. **Primary Resolution (POSIX / Bash CLI)**:
   Execute from repository root:
   ```bash
   .specify/scripts/bash/resolve-template.sh <template-name> --json
   ```
   Parse the JSON output (`TEMPLATE_NAME`, `TEMPLATE_CONTENT`) and use `TEMPLATE_CONTENT` as the active scaffold.
2. **Platform-Agnostic Fallback Resolution**:
   If the bash resolver cannot be executed in the current OS/environment, resolve `<template-name>.md` by checking the 4-tier hierarchy in strict priority order:
   1. `.specify/templates/overrides/<template-name>.md`
   2. `.specify/presets/<preset-id>/templates/<template-name>.md` (ordered by `.specify/presets/.registry` priority, applying `preset.yml` strategy if present)
   3. `.specify/extensions/<ext-id>/templates/<template-name>.md` (ordered by `.specify/extensions/.registry` priority)
   4. `.specify/templates/<template-name>.md`

---

## 3. Optional Module & Sub-Clause Transformation Contract

### 3.1 Activation Precedence
For each optional module (`MODULE-A`, `MODULE-B`, `MODULE-C`, `MODULE-D`, `MODULE-D-AOT-TRIM`, and optional `TRACE` logging):
1. **Explicit User Input**: Enable or omit as explicitly instructed in `$ARGUMENTS` or user prompt.
2. **Existing Ratified State**: If updating an existing `.specify/memory/constitution.md` and the user did not specify changes to optional modules, preserve the module's current state from the existing constitution.
3. **Repository Context Inference / Default**: On initial setup without explicit user selection, inspect repository evidence; default any unrequested and unevidenced optional module to `OMITTED`.

### 3.2 Structural Transformations in `constitution.md`

| Construct | State = `ENABLED` | State = `OMITTED` |
|-----------|-------------------|-------------------|
| `MODULE-A` (`Action: ADD`, Target: Principle I) | Remove `<!-- OPTIONAL-MODULE: MODULE-A ... -->` and `<!-- /OPTIONAL-MODULE: MODULE-A -->` lines; keep `- **Pointer-Only Code Tags**: ...` inline in Principle I. | Remove opening tag, body text, and closing tag completely. |
| `MODULE-B` (`Action: REPLACE`, Target: Principle III, Replaces: `PLAN-JUSTIFICATION-AND-SKIP-ALLOWLIST`) | Remove entire `<!-- DEFAULT-CLAUSE: PLAN-JUSTIFICATION-AND-SKIP-ALLOWLIST ... -->` ... `<!-- /DEFAULT-CLAUSE: PLAN-JUSTIFICATION-AND-SKIP-ALLOWLIST -->` block (including its 5 allowlist items); strip `OPTIONAL-MODULE: MODULE-B` comment tags and retain `- **100% Branch Coverage Gate**: ...` in Principle III. | Strip `<!-- DEFAULT-CLAUSE: ... -->` and `<!-- /DEFAULT-CLAUSE: ... -->` tags while retaining `- **Plan Justification & Skip Allowlist**: ...` (and its 5 items); remove entire `MODULE-B` block. |
| `MODULE-C` (`Action: ADD`, Target: Principle IV) | Remove `<!-- OPTIONAL-MODULE: MODULE-C ... -->` and `<!-- /OPTIONAL-MODULE: MODULE-C -->` lines; keep `- **Dispatch Is Data, Not Branches**: ...` inline in Principle IV. | Remove opening tag, body text, and closing tag completely. |
| `MODULE-D` (`Action: ADD`, Target: Principle V) | Remove `<!-- OPTIONAL-MODULE: MODULE-D ... -->` and `<!-- /OPTIONAL-MODULE: MODULE-D -->` lines; keep `- **Reproducible Builds & Deliberate Versioning**: ...` inline in Principle V; evaluate `MODULE-D-AOT-TRIM`. | Remove entire `MODULE-D` block (including nested `MODULE-D-AOT-TRIM`) completely. |
| `MODULE-D-AOT-TRIM` (`Parent-Module: MODULE-D`) | Require `MODULE-D == ENABLED`. Strip `<!-- OPTIONAL-SUBCLAUSE: MODULE-D-AOT-TRIM ... -->` and `<!-- /OPTIONAL-SUBCLAUSE: MODULE-D-AOT-TRIM -->` lines and unwrap `[Optional: <text>]` to `<text>`. | Remove opening sub-clause tag, inner `[Optional: ...]` text, and closing sub-clause tag completely. |
| `TRACE (Optional)` (`logging-standards.md`) | Record in `logging-standards.md` (`Project Telemetry Configuration` / `[RETENTION_AND_SAMPLING_POLICY]`) that mechanical `TRACE` entry/exit logging is **enabled**. | Record in `logging-standards.md` (`Project Telemetry Configuration` / `[RETENTION_AND_SAMPLING_POLICY]`) that mechanical `TRACE` entry/exit logging is **disabled** (`OMITTED`). |

---

## 4. Placeholder Value Merge & Conflict Resolution Contract

### 4.1 Value Merge Priority
Every `[ALL_CAPS_IDENTIFIER]` placeholder across the 3 templates (8 in `constitution.md`, 11 in `coding-standards.md`, 6 in `logging-standards.md`) MUST be populated using:
1. **Explicit User Input** in `$ARGUMENTS` or conversation
2. **Existing Ratified Governance Values** in `.specify/memory/{constitution,coding-standards,logging-standards}.md` (preserving original `RATIFICATION_DATE`, `Recorded Deviations`, and custom conventions that are not being amended)
3. **Repository Evidence** from documentation, manifests, linter configs, and directory layout
4. **Explicit `TODO(<FIELD_NAME>): <explanation>`** if and only if a value cannot be determined from sources 1–3 (never invent unverified facts or leave `[ALL_CAPS_IDENTIFIER]` brackets).

### 4.2 Constitutional Conflict Resolution Gate
- Base Core Principles I–VII in `constitution-template.md` are non-negotiable.
- If an existing repository practice or user instruction conflicts with a Core Principle:
  1. Do **not** silently delete, weaken, or contradict the Core Principle in `constitution.md`.
  2. Surface the conflict explicitly and either:
     - **Option A (Align Standards)**: Align `coding-standards.md` and `logging-standards.md` with the Core Principle and note the required repository remediation, OR
     - **Option B (Ratified Deviation)**: Record an explicit human-ratified entry under `## Recorded Deviations` in `constitution.md` with all five mandatory elements:
       1. `Principle violated`
       2. `Ratifying human authority`
       3. `Rationale`
       4. `Compensating control`
       5. `Known gap and documentation link`

---

## 5. Sync Impact Report Schema (`constitution.md`)

The top HTML comment in `.specify/memory/constitution.md` MUST follow this structure (keeping only the latest amendment):

```markdown
<!--
Sync Impact Report (Latest Amendment Only — Do Not Accumulate History):
- Version Change: <old_version> -> <new_version>
- Modified Principles: <summary of principle changes or "None (preserved Principles I–VII)">
- Modified Sections: <list of modified sections>
- Optional Modules: MODULE-A: <ENABLED|OMITTED>, MODULE-B: <ENABLED|OMITTED>, MODULE-C: <ENABLED|OMITTED>, MODULE-D: <ENABLED|OMITTED> (MODULE-D-AOT-TRIM: <ENABLED|OMITTED>), TRACE Logging: <ENABLED|OMITTED>
- Companion Standards: coding-standards.md (<created|updated|unchanged>), logging-standards.md (<created|updated|unchanged>)
- Rationale: <concise rationale for this governance initialization or amendment>
- Deferred TODOs: <None or list of TODO(FIELD_NAME) items>
-->
```

---

## 6. Pre-Write Validation Gate

Before completing execution, `speckit-constitution` MUST verify:
1. All three files (`.specify/memory/constitution.md`, `.specify/memory/coding-standards.md`, `.specify/memory/logging-standards.md`) exist and are non-empty.
2. `[PROJECT_NAME]` is identical across all three files.
3. Regex search `\[[A-Z0-9_]+\]` across all three files returns **0** matches.
4. Regex search `<!-- /?(OPTIONAL-MODULE|OPTIONAL-SUBCLAUSE|DEFAULT-CLAUSE)` in `.specify/memory/constitution.md` returns **0** matches.
5. `RATIFICATION_DATE` and `LAST_AMENDED_DATE` match `YYYY-MM-DD` and `CONSTITUTION_VERSION` matches the `Sync Impact Report`.
