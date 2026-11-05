# Contract 3: Active Governance Suite Amendment (`v2.1.0`), Canonical `README.md` & Manifest Digests

**Feature**: `006-human-docs-governance`  
**Covers**: `FR-004`, `FR-005`, `FR-009`, `SC-001`, `SC-004`, `SC-005`

---

## 1. Active `.specify/memory/constitution.md` Amendment (`2.0.0 -> 2.1.0`)

1. **Top HTML `Sync Impact Report`**:
   ```markdown
   <!--
   Sync Impact Report (Latest Amendment Only — Do Not Accumulate History):
   - Version Change: 2.0.0 -> 2.1.0
   - Modified Principles: Principle VII expanded with baseline Human-Facing Documentation Synchronization rule and enabled MODULE-DOCS (Structured Human-Facing Documentation Gate).
   - Modified Sections: Core Principles (Principle VII), Development Workflow & Quality Gates, Governance
   - Optional Modules: MODULE-A: OMITTED, MODULE-B: OMITTED, MODULE-C: OMITTED, MODULE-D: OMITTED (MODULE-D-AOT-TRIM: OMITTED), MODULE-DOCS: ENABLED, TRACE Logging: OMITTED
   - Companion Standards: coding-standards.md (updated), logging-standards.md (unchanged)
   - Rationale: Ratify Phase 6 Human-Facing Documentation Standards & Governance across the active repository governance suite and establish canonical root README.md requirements.
   - Deferred TODOs: None
   -->
   ```
2. **Principle VII Updates**:
   - Update `- **Present-Tense, High-Signal Comments & Docs**:` to mandate same-change updates to human-facing documentation (`README.md`, quickstarts, and user guides) whenever user-visible CLI commands, agent skills, public APIs, configuration options, or end-user workflows change, while exempting `INTERNAL_ONLY` changes.
   - Include the ratified `MODULE-DOCS` clause bullet (with comment tags stripped):
     `- **Structured Human-Facing Documentation Gate**: The repository root README.md (and any dedicated user guide under docs/) MUST maintain canonical sections covering Project Overview & Architecture, Getting Started / Bootstrap Quickstart, CLI / Skill / API Usage Reference, and Configuration & Governance Verification, verified for relative link integrity and command accuracy before merge.`
3. **Footer Metadata**:
   - `**Version**: 2.1.0 | **Ratified**: 2026-11-04 | **Last Amended**: 2026-11-05`

---

## 2. Active `.specify/memory/coding-standards.md` Amendment

Append `## Human-Facing Documentation & README Conventions` after `## Naming, Formatting & Code Style`:

```markdown
---

## Human-Facing Documentation & README Conventions

Operationalizes Constitutional Principle VII (*Code Hygiene, Ubiquitous Language & Safe Logging*):

- **Human-Facing Documentation & README Structure**: The repository root `README.md` serves as the primary human-facing onboarding and usage reference and MUST maintain four canonical sections: (1) Project Overview & 4-Tier Architecture, (2) Co-Applied Governance Suite, (3) Spec Kit Skills & Subagent Orchestration Reference, and (4) Portable Bootstrapping & Verification Quickstart. Any change classified as `USER_FACING` in `plan.md` (adding, removing, or altering skills in `.agents/skills/`, bootstrapper flags in `bootstrap-speckit.{sh,ps1}`, template contracts in `.specify/templates/`, or governance rules) MUST update `README.md` (and `ROADMAP.md` when phase scope changes) in the same pull request. Changes classified as `INTERNAL_ONLY` with an explicit justification in `plan.md` are exempt from artificial `README.md` edits. Human-facing documentation MUST use valid repository-relative links and MUST NEVER cite ephemeral `specs/NNN-*/` directories or `FR-XXX` / `SC-XXX` identifiers.
```

---

## 3. Repository Root `README.md` Contract

**Target File**: `/README.md` (at repository root)

### Required Sections & Verification Invariants
1. **`# Spec Kit Customization & Governance Toolkit`** (or equivalent descriptive H1 title)
2. **`## Project Overview & Architecture`**:
   - Purpose of the repository as a portable Spec Kit governance, subagent orchestration, and skill customization bundle.
   - Native 4-tier template resolution hierarchy (`Tier 1: .specify/templates/overrides/` -> `Tier 2: .specify/presets/<preset-id>/templates/` -> `Tier 3: .specify/extensions/<ext-id>/templates/` -> `Tier 4: .specify/templates/`).
   - Directory layout summary (`.specify/`, `.agents/`, `bootstrap-speckit.sh`, `bootstrap-speckit.ps1`, `ROADMAP.md`).
3. **`## Co-Applied Governance Suite`**:
   - Overview of `.specify/memory/constitution.md`, `.specify/memory/coding-standards.md`, and `.specify/memory/logging-standards.md`.
   - Summary of Core Principles I–VII, optional modules (`MODULE-A`, `MODULE-B`, `MODULE-C`, `MODULE-D`, `MODULE-D-AOT-TRIM`, `MODULE-DOCS`, `TRACE`), and the `Documentation Impact` (`USER_FACING` vs. `INTERNAL_ONLY`) gate.
4. **`## Spec Kit Skills & Subagent Reference`**:
   - Complete table and workflow guide covering all 11 skills:
     - `/speckit-specify`, `/speckit-clarify`, `/speckit-plan`, `/speckit-tasks`, `/speckit-checklist`, `/speckit-analyze`, `/speckit-implement`, `/speckit-converge`, `/speckit-constitution`, `/speckit-orchestrate`, `/speckit-bootstrap`
   - Subagent role profiles: `.agents/agents/speckit-reasoner.md` and `.agents/agents/speckit-executor.md`.
5. **`## Getting Started & Portable Bootstrapping`**:
   - POSIX seeding: `./bootstrap-speckit.sh <target-repo> [--force]`
   - PowerShell seeding: `pwsh ./bootstrap-speckit.ps1 <target-repo> [-Force]`
   - Post-seed verification, upgrade, and governance initialization: `/speckit-bootstrap`, `/speckit-bootstrap --check`, `/speckit-bootstrap --upgrade`, `/speckit-bootstrap --init-governance`, and `/speckit-constitution`.
6. **`## Configuration & Governance Verification`**:
   - Static quality gates (`bash -n bootstrap-speckit.sh`, template/preset parity check, placeholder/marker regex check, manifest SHA-256 verification).
7. **Hard Hygiene Invariants**:
   - **0** broken relative markdown links (`[...](...)`).
   - **0** references to ephemeral `specs/NNN-*/` folders or `FR-XXX` / `SC-XXX` identifiers.
   - **0** unresolved `[ALL_CAPS_IDENTIFIER]` placeholders.

---

## 4. Integration Manifest Synchronization Contract

Update SHA-256 digests and byte sizes in deterministic order:
1. Update `.specify/integrations/speckit.manifest.json` for:
   - `.specify/templates/coding-standards-template.md`
   - `.specify/templates/constitution-template.md`
   - `.specify/templates/plan-template.md`
   - `.specify/templates/tasks-template.md`
2. Update `.specify/integrations/agy.manifest.json` for:
   - `.agents/skills/speckit-analyze/SKILL.md`
   - `.agents/skills/speckit-constitution/SKILL.md`
   - `.agents/skills/speckit-converge/SKILL.md`
   - `.agents/skills/speckit-implement/SKILL.md`
   - `.agents/skills/speckit-plan/SKILL.md`
   - `.agents/skills/speckit-tasks/SKILL.md`
3. Update `.specify/integrations/speckit-bootstrap.manifest.json` (`digest: "sha256:<hex>"` and `size_bytes: <int>`) for all managed files under `.specify/` and `.agents/`, including the updated `.specify/presets/base-governance/templates/{constitution,coding-standards}-template.md` and the newly written `.specify/integrations/{speckit,agy}.manifest.json`.
