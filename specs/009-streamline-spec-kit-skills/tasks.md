# Tasks: Streamline Spec Kit Skills & Decouple Bloat

Feature: `009-streamline-spec-kit-skills`

## Phase 1: Setup

- [x] T001 Verify baseline status and ensure working tree clean in `git status`

## Phase 2: Foundational

- [x] T002 Establish canonical template resolution and governance loading helper snippets in `specs/009-streamline-spec-kit-skills/contracts/skill-streamlining-contract.md`

## Phase 3: User Story 1 - Prune Redundant Template Resolution Prompts

- [x] T003 [P] [US1] Streamline template resolution in `.agents/skills/speckit-specify/SKILL.md`
- [x] T004 [P] [US1] Streamline template resolution in `.agents/skills/speckit-plan/SKILL.md`
- [x] T005 [P] [US1] Streamline template resolution in `.agents/skills/speckit-tasks/SKILL.md`
- [x] T006 [P] [US1] Streamline template resolution in `.agents/skills/speckit-checklist/SKILL.md`

## Phase 4: User Story 2 - Decouple Documentation Gate from Skills to Constitution

- [x] T007 [P] [US2] Remove hardcoded Documentation Impact branching from `.agents/skills/speckit-plan/SKILL.md`
- [x] T008 [P] [US2] Remove hardcoded Documentation Impact branching from `.agents/skills/speckit-tasks/SKILL.md`
- [x] T009 [P] [US2] Remove hardcoded Documentation Impact gate from `.agents/skills/speckit-analyze/SKILL.md`
- [x] T010 [P] [US2] Remove hardcoded Documentation Impact rules from `.agents/skills/speckit-implement/SKILL.md`
- [x] T011 [P] [US2] Remove hardcoded Documentation Impact rules from `.agents/skills/speckit-converge/SKILL.md`

## Phase 5: User Story 3 - Selective & Lazy Governance Context Loading

- [x] T012 [P] [US3] Refactor `.agents/skills/speckit-specify/SKILL.md` and `.agents/skills/speckit-clarify/SKILL.md` to load only `constitution.md`
- [x] T013 [P] [US3] Refactor `.agents/skills/speckit-plan/SKILL.md` and `.agents/skills/speckit-tasks/SKILL.md` to load `constitution.md` and relevant parts of `coding-standards.md`
- [x] T014 [P] [US3] Retain full companion standards loading (`coding-standards.md` and `logging-standards.md`) in `.agents/skills/speckit-implement/SKILL.md`

## Phase 6: User Story 4 - Remove Redundant Principle III Extraction Blocks

- [x] T015 [P] [US4] Simplify testing rule references in `.agents/skills/speckit-tasks/SKILL.md`
- [x] T016 [P] [US4] Simplify dynamic Principle III extraction in `.agents/skills/speckit-orchestrate/SKILL.md`

## Phase 7: User Story 5 - Dual-Client Parity & Manifest Synchronization

- [x] T017 [US5] Mirror all modified skills from `.agents/skills/` to `.claude/skills/`
- [x] T018 [US5] Verify byte parity using `diff -r .agents/skills .claude/skills`
- [x] T019 [US5] Recalculate SHA-256 hashes and file sizes in `.specify/integrations/agy.manifest.json`
- [x] T020 [US5] Recalculate SHA-256 hashes and file sizes in `.specify/integrations/claude.manifest.json`
- [x] T021 [US5] Recalculate SHA-256 hashes and file sizes in `.specify/integrations/speckit-bootstrap.manifest.json`

## Phase 8: Polish & Documentation Updates

- [x] T022 Update `README.md` to document selective governance loading and streamlined skill design
- [x] T023 Run manifest verification check script across all tracked integration files
