# Phase 1 Data Model: Human-Facing Documentation Standards & Governance

**Feature**: `006-human-docs-governance`  
**Date**: 2026-11-05  
**Spec**: [spec.md](spec.md) | **Research**: [research.md](research.md)

## Overview

This document defines the declarative governance schemas, template slot contracts, workflow state classifications, and manifest structures introduced or updated by Phase 6 (*Human-Facing Documentation Standards & Governance*).

---

## Entity 1: `HumanFacingDocumentationStandard` (Constitutional Principle VII & `MODULE-DOCS`)

Represents the constitutional mandate in `.specify/templates/constitution-template.md`, `.specify/presets/base-governance/templates/constitution-template.md`, and ratified `.specify/memory/constitution.md`.

| Field / Element | Type / Format | Required | Constraints & Validation Rules |
|-----------------|---------------|----------|--------------------------------|
| `baseline_sync_clause` | Normative Markdown Bullet | Yes | Embedded in Principle VII (`Present-Tense, High-Signal Comments & Docs`). Requires same-change updates to `README.md`, quickstarts, or user guides whenever user-visible CLI commands, agent skills, public APIs, configuration options, or end-user workflows change; explicitly exempts `INTERNAL_ONLY` changes. |
| `module_id` | Enum Literal | Yes (in template) | Fixed identifier: `MODULE-DOCS`. |
| `module_action` | Enum Literal | Yes (in template) | Fixed value: `ADD`. |
| `module_target` | Enum Literal | Yes (in template) | Fixed value: `Principle VII`. |
| `module_title` | String | Yes (in template) | Fixed value: `Structured Human-Facing Documentation Gate`. |
| `activation_state` | Enum (`ENABLED` \| `OMITTED`) | Yes (at ratification) | Recorded in the top HTML `Sync Impact Report` comment (`MODULE-DOCS: <ENABLED\|OMITTED>`). |
| `ratified_clause_body` | Normative Markdown Bullet | Conditional | Included in Principle VII when `activation_state == ENABLED`; completely stripped when `activation_state == OMITTED`. Zero `<!-- OPTIONAL-MODULE: MODULE-DOCS` or `<!-- /OPTIONAL-MODULE: MODULE-DOCS -->` comment tags may remain in ratified `.specify/memory/constitution.md`. |

### State Transitions (`MODULE-DOCS` in `/speckit-constitution`)

```text
[Template with OPTIONAL-MODULE: MODULE-DOCS markers]
   ├──(activation_state = ENABLED)──> Strip comment markers, retain "- **Structured Human-Facing Documentation Gate**: ..." bullet in Principle VII, record "MODULE-DOCS: ENABLED" in Sync Impact Report
   └──(activation_state = OMITTED)──> Remove opening marker, clause body, and closing marker, record "MODULE-DOCS: OMITTED" in Sync Impact Report
```

---

## Entity 2: `HumanDocsConventionsSlot` (`[HUMAN_DOCS_CONVENTIONS]`)

Represents the companion coding-standards section and placeholder slot in `.specify/templates/coding-standards-template.md`, `.specify/presets/base-governance/templates/coding-standards-template.md`, and ratified `.specify/memory/coding-standards.md`.

| Field / Element | Type / Format | Required | Constraints & Validation Rules |
|-----------------|---------------|----------|--------------------------------|
| `section_heading` | Markdown H2 | Yes | Exact heading: `## Human-Facing Documentation & README Conventions` |
| `authority_reference` | Markdown Paragraph | Yes | `Operationalizes Constitutional Principle VII (*Code Hygiene, Ubiquitous Language & Safe Logging*):` |
| `slot_token` | Placeholder Token | Yes (in template) | Exact token: `[HUMAN_DOCS_CONVENTIONS]` (brings `coding-standards-template.md` to 12 slots and total suite slots to 26). |
| `archetype_examples` | HTML Comment | Yes (in template) | Guidance examples for CLI tools, libraries/SDKs, web services, and agent/skill repositories. |
| `ratified_value` | Markdown Bullet(s) | Yes (in `.specify/memory/coding-standards.md`) | Non-empty concrete convention text with 0 unresolved `[ALL_CAPS_IDENTIFIER]` tokens and 0 references to ephemeral `specs/NNN-*/` or `FR-XXX` identifiers. |

---

## Entity 3: `DocumentationImpactClassification`

Represents the explicit planning and verification metadata recorded in `plan.md` and evaluated by `speckit-plan`, `speckit-tasks`, `speckit-analyze`, `speckit-implement`, and `speckit-converge`.

| Field | Type / Format | Required | Constraints & Validation Rules |
|-------|---------------|----------|--------------------------------|
| `classification` | Enum (`USER_FACING` \| `INTERNAL_ONLY`) | Yes | Must be explicitly declared under `Technical Context` (`**Documentation Impact**: ...`) and checked in `Constitution Check` of `plan.md`. Cannot be left as `NEEDS CLARIFICATION` after Phase 0. |
| `target_files` | List of Relative Paths | Required if `USER_FACING` | One or more human-facing documentation paths (e.g., `README.md`, `ROADMAP.md`, `docs/...`) affected by the feature. Must be empty/omitted when `INTERNAL_ONLY`. |
| `exemption_rationale` | Non-empty String (1+ sentences) | Required if `INTERNAL_ONLY` | Concrete justification explaining why the feature does not add, remove, or alter any user-visible CLI command, skill, public API, configuration option, or end-user workflow. |
| `mapped_task_ids` | List of Task IDs (`TXXX`) | Required if `USER_FACING` | In `tasks.md`, at least one task must target each file in `target_files`. Verified by `/speckit-analyze`, `/speckit-implement`, and `/speckit-converge`. |

### Downstream Gate State Machine

```text
[spec.md + plan.md]
   ├── Documentation Impact == USER_FACING (target_files: [README.md, ...])
   │      ├── /speckit-tasks    ──> Emits explicit doc update task(s) with exact file paths
   │      ├── /speckit-analyze  ──> Verifies >=1 task in tasks.md maps to target_files (flags CRITICAL/HIGH if missing)
   │      ├── /speckit-implement──> Executes doc update task(s) & validates links + zero specs/NNN-* or FR-XXX citations
   │      └── /speckit-converge ──> Audits on-disk docs against as-built behavior (appends convergence task if missing/partial/contradicts)
   │
   └── Documentation Impact == INTERNAL_ONLY (exemption_rationale provided)
          ├── /speckit-tasks    ──> Omits artificial README.md tasks
          ├── /speckit-analyze  ──> Verifies rationale does not contradict spec.md user-visible changes (0 README churn required)
          ├── /speckit-implement──> Skips user-doc tasks cleanly
          └── /speckit-converge ──> Confirms internal-only scope (no doc gap finding emitted)
```

---

## Entity 4: `RepositoryReadmeDocument` (`README.md`)

Represents the canonical human-facing onboarding and reference document at the repository root (`/README.md`).

| Section / Attribute | Required | Content & Validation Constraints |
|---------------------|----------|----------------------------------|
| `H1 Title & Overview` | Yes | States repository purpose, Spec Kit customization architecture, and zero-external-dependency design. |
| `Co-Applied Governance Suite` | Yes | Documents `.specify/memory/{constitution,coding-standards,logging-standards}.md`, Core Principles I–VII, optional modules (`MODULE-A`..`MODULE-D`, `MODULE-DOCS`, `TRACE`), and 4-tier template resolution (`overrides`, `presets`, `extensions`, `core`). |
| `Spec Kit Skills & Agents Reference` | Yes | Documents all 11 skills (`speckit-specify`, `speckit-clarify`, `speckit-plan`, `speckit-tasks`, `speckit-checklist`, `speckit-analyze`, `speckit-implement`, `speckit-converge`, `speckit-constitution`, `speckit-orchestrate`, `speckit-bootstrap`) and both role profiles (`speckit-reasoner`, `speckit-executor`). |
| `Portable Bootstrapping & Quickstart` | Yes | Documents `./bootstrap-speckit.sh <target-repo> [--force]`, `pwsh ./bootstrap-speckit.ps1 <target-repo> [-Force]`, and `/speckit-bootstrap` verification/upgrade flags (`--check`, `--upgrade`, `--force`, `--init-governance`). |
| `Quality & Ephemeral Spec Hygiene` | Yes | Contains 0 broken relative file links, 0 unresolved `[ALL_CAPS]` placeholders, and 0 references to ephemeral `specs/NNN-*/` directories or `FR-XXX`/`SC-XXX` identifiers (`SC-004`). |

---

## Entity 5: `ManagedAssetManifestSync`

Represents the cryptographic integrity records across `.specify/integrations/{speckit,agy,speckit-bootstrap}.manifest.json`.

| Manifest File | Modified Entries in Phase 6 | Format & Synchronization Constraint |
|---------------|-----------------------------|-------------------------------------|
| `.specify/integrations/speckit.manifest.json` | `.specify/templates/constitution-template.md`, `.specify/templates/coding-standards-template.md`, `.specify/templates/plan-template.md`, `.specify/templates/tasks-template.md` | Raw lowercase 64-char hex SHA-256 string (`"<hex>"`). Must match `.specify/presets/base-governance/templates/{constitution,coding-standards}-template.md` digests. |
| `.specify/integrations/agy.manifest.json` | `.agents/skills/speckit-{constitution,plan,tasks,analyze,implement,converge}/SKILL.md` | Raw lowercase 64-char hex SHA-256 string (`"<hex>"`). |
| `.specify/integrations/speckit-bootstrap.manifest.json` | All 10 files above + `.specify/presets/base-governance/templates/{constitution,coding-standards}-template.md` + `.specify/integrations/{speckit,agy}.manifest.json` | Object `{"digest": "sha256:<hex>", "size_bytes": <int>, "tier": "<tier>"}`. Must be updated *after* `speckit.manifest.json` and `agy.manifest.json` are written so their self-digests and `size_bytes` match on-disk state. |
