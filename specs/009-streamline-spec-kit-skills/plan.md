# Implementation Plan: Streamline Spec Kit Skills & Decouple Bloat

**Branch**: `009-streamline-spec-kit-skills` | **Status**: Complete  
**Date**: 2026-11-05

## Summary of Changes
Streamline the Spec Kit skill suite across `.agents/skills/` and `.claude/skills/` by:
1. Pruning verbose 4-tier template resolution boilerplate down to concise 2-line instructions in `speckit-specify`, `speckit-plan`, `speckit-tasks`, and `speckit-checklist`.
2. Removing hardcoded `Documentation Impact` logic blocks from `speckit-plan`, `speckit-tasks`, `speckit-analyze`, `speckit-implement`, and `speckit-converge`, delegating all documentation enforcement to `constitution.md`.
3. Making governance file loading selective: `specify` and `clarify` load only `constitution.md`; `plan` and `tasks` load `constitution.md` and relevant sections of `coding-standards.md`; only `implement` loads `coding-standards.md` and `logging-standards.md`.
4. Removing redundant Principle III extraction boilerplate from `speckit-tasks` and `speckit-orchestrate`.
5. Synchronizing `.agents/` and `.claude/` for 100% parity, and updating manifests.

## Technical Architecture & Design Seams

### Affected Skill Files
- `.agents/skills/speckit-specify/SKILL.md` (and `.claude/` mirror)
- `.agents/skills/speckit-plan/SKILL.md` (and `.claude/` mirror)
- `.agents/skills/speckit-tasks/SKILL.md` (and `.claude/` mirror)
- `.agents/skills/speckit-analyze/SKILL.md` (and `.claude/` mirror)
- `.agents/skills/speckit-implement/SKILL.md` (and `.claude/` mirror)
- `.agents/skills/speckit-converge/SKILL.md` (and `.claude/` mirror)
- `.agents/skills/speckit-checklist/SKILL.md` (and `.claude/` mirror)
- `.agents/skills/speckit-clarify/SKILL.md` (and `.claude/` mirror)
- `.agents/skills/speckit-orchestrate/SKILL.md` (and `.claude/` mirror)

### Manifest Updates
- `.specify/integrations/agy.manifest.json`
- `.specify/integrations/claude.manifest.json`
- `.specify/integrations/speckit-bootstrap.manifest.json`

## Documentation Impact
- `README.md` will be updated to reflect that companion standards are loaded lazily on demand by stage rather than eagerly everywhere, improving execution speed and reducing token consumption.
