# Schema Contract: `roadmap-template.md` & `ROADMAP.md`

**Feature**: `005-roadmap-management`  
**Artifacts**:
- `.specify/templates/roadmap-template.md`
- `.specify/presets/base-governance/templates/roadmap-template.md`
- `ROADMAP.md` (Project-owned root roadmap)  
**Date**: 2026-11-05  

---

## 1. Template Resolution & Preset Registration Contract

### 1.1 4-Tier Resolution Order
When `/speckit-roadmap` resolves `roadmap-template`, it evaluates the 4-tier hierarchy in strict priority order:
1. **Tier 1 (Overrides)**: `.specify/templates/overrides/roadmap-template.md` (strategy: `replace`)
2. **Tier 2 (Presets)**: `.specify/presets/<preset-id>/templates/roadmap-template.md` (ordered by ascending `priority` in `.specify/presets/.registry`; composition strategy from `preset.yml`)
3. **Tier 3 (Extensions)**: `.specify/extensions/<ext-id>/templates/roadmap-template.md` (ordered by ascending `priority` in `.specify/extensions/.registry`)
4. **Tier 4 (Core Fallback)**: `.specify/templates/roadmap-template.md`

**Fail-Closed Invariant**: If `roadmap-template` is not found in any of the 4 tiers, `/speckit-roadmap` MUST emit a `CRITICAL` diagnostic and halt immediately per Constitutional Principle II.

### 1.2 Preset Registration (`preset.yml`)
`.specify/presets/base-governance/preset.yml` MUST register `roadmap-template`:
```yaml
    - type: "template"
      name: "roadmap-template"
      file: "templates/roadmap-template.md"
      strategy: "replace"
```

---

## 2. Canonical Document Structure (`ROADMAP.md`)

Every conforming `ROADMAP.md` document MUST contain the following sections in order:

### 2.1 Header & Governance Metadata
```markdown
# [PROJECT NAME] Roadmap

**Last Updated**: YYYY-MM-DD  
**Governance**: Managed via `/speckit-roadmap` and `.specify/memory/constitution.md`

This roadmap organizes planned strategic initiatives into sequential, self-contained phases. Each phase is designed to be audited (`/speckit-roadmap --status`), specified (`/speckit-roadmap --next` or `/speckit-specify`), planned (`/speckit-plan`), and implemented (`/speckit-implement` / `/speckit-orchestrate`) with full traceability to `specs/NNN-*/`.
```

### 2.2 Overview of Initiatives Table
```markdown
## Overview of Initiatives

| Phase | Initiative | Status | Prerequisites | Spec | Goal | Key Deliverables |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Phase 1** | **[Initiative Title]** | `COMPLETED` | None | `specs/001-example/` | [One-sentence goal] | [Comma-separated deliverables] |
| **Phase 2** | **[Initiative Title]** | `IN_PROGRESS` | Phase 1 | `specs/002-example/` | [One-sentence goal] | [Comma-separated deliverables] |
| **Phase 3** | **[Initiative Title]** | `PLANNED` | Phase 1, Phase 2 | — | [One-sentence goal] | [Comma-separated deliverables] |
```

**Column Invariants**:
1. `Phase`: Bold sequential identifier `**Phase N**` (`N >= 1`).
2. `Initiative`: Bold concise phase title `**<Title>**`.
3. `Status`: Backtick-wrapped status token from the closed enum: `` `PLANNED` ``, `` `IN_PROGRESS` ``, `` `COMPLETED` ``, `` `DEFERRED` ``.
4. `Prerequisites`: `None` or comma-separated upstream phase identifiers (`Phase 1`, `Phase 1, Phase 2`).
5. `Spec`: Backtick-wrapped relative path to the feature spec folder (e.g., `` `specs/001-base-governance-templates/` ``) when assigned, or em-dash `—` when unassigned.
6. `Goal`: Concise strategic objective statement.
7. `Key Deliverables`: Summary of artifacts produced by the phase.

### 2.3 Detailed Phase Sections
For each row in the Overview of Initiatives table, `ROADMAP.md` MUST contain a matching level-2 section in identical sequential order:

```markdown
## Phase N: [Initiative Title]

### Metadata
- **Status**: `PLANNED` | `IN_PROGRESS` | `COMPLETED` | `DEFERRED`
- **Prerequisites**: None | Phase 1[, Phase M...]
- **Spec Directory**: `specs/NNN-<short-name>/` | —

### Problem Statement
[Numbered or bulleted explanation of the problem, gap, and strategic motivation]

### Architectural Fit in Spec Kit
[How the phase integrates with Spec Kit architecture, templates, skills, presets, extensions, and governance]

### Key Deliverables
- [Deliverable 1]
- [Deliverable 2]

### Key Design Decisions to Resolve During Spec
- **[Decision Topic 1]**: [Description of trade-offs or options]
- **[Decision Topic 2]**: [Description of trade-offs or options]
```

---

## 3. Structural Lint & Referential Integrity Rules (`--check`)

When `/speckit-roadmap --check` (or `--status`) evaluates `ROADMAP.md`, it enforces these 6 static validation gates:

| Rule ID | Check Description | Failure Classification |
|---------|-------------------|------------------------|
| `RM-LINT-001` | `ROADMAP.md` exists at repository root and is non-empty. | `STRUCTURAL_ERROR` (`WARN` boundary rejection) |
| `RM-LINT-002` | `## Overview of Initiatives` table contains all 7 canonical columns (`Phase`, `Initiative`, `Status`, `Prerequisites`, `Spec`, `Goal`, `Key Deliverables`). | `STRUCTURAL_ERROR` |
| `RM-LINT-003` | 1-to-1 sequential correspondence between `**Phase N**` rows in the Overview table and `## Phase N: <Title>` detailed sections, with no duplicate phase numbers. | `STRUCTURAL_ERROR` |
| `RM-LINT-004` | Every `Status` token in both the Overview table and `### Metadata` is a valid member of `{PLANNED, IN_PROGRESS, COMPLETED, DEFERRED}` and matches between Overview and Metadata. | `STRUCTURAL_ERROR` |
| `RM-LINT-005` | Every phase listed in `Prerequisites` (other than `None`) references a defined earlier phase (`Phase M` where `M < N`) with no self-dependencies or cycles. | `STRUCTURAL_ERROR` |
| `RM-LINT-006` | Every `## Phase N` section contains `### Metadata`, `### Problem Statement`, `### Architectural Fit in Spec Kit` (or `### Architectural Fit & Scope`), `### Key Deliverables`, and `### Key Design Decisions to Resolve During Spec`. | `STRUCTURAL_ERROR` |
