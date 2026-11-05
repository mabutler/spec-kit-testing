# Feature Specification: Precise & Clear Constitution Language

**Feature Branch**: `008-precise-constitution-language`  
**Created**: 2026-11-05  
**Status**: Clarified & Ratified  
**Input**: User description: "Let's clean up the constitution language. There's a lot of AI language that is hard to decipher. For example, "Evidence Over Invention" instead of something like "Evidence Based Decisions". Flowery language instead of precise language"

---

## User Scenarios & Testing

### User Story 1 - Modernize Core Principle Titles & Body Prose into Precise Engineering Language (Priority: P1)

As a software engineer or AI agent reading the project constitution, I need all 7 core principles and rule bodies to use direct, clear, professional engineering language rather than flowery, metaphorical, or conversational AI rhetoric, so that requirements are crisp and unambiguous.

**Why this priority**: The constitution is the root authority hierarchy for all repository design, planning, and code implementation. Metaphors like "Evidence Over Invention", "primary source digs", and "epistemic truth" create ambiguity.

**Independent Test**: Can be validated by inspecting `.specify/memory/constitution.md` and verifying that all 7 core principle titles and rule bodies use precise engineering language while preserving all underlying governance constraints.

**Acceptance Scenarios**:
1. **Given** the active constitution in `.specify/memory/constitution.md`, **When** inspected, **Then** all 7 principle titles use modernized software engineering terminology:
   - Principle I: `Evidence-Based Decisions & Bounded Research`
   - Principle II: `Explicit Error Handling & Fail-Closed State`
   - Principle III: `Static Verification & Quality Gates` (active memory) / `Behavioral Testing & Deterministic Verification` (base template)
   - Principle IV: `State Ownership, Architectural Seams & Safe Concurrency`
   - Principle V: `Centralized Dependencies & Toolchain Security`
   - Principle VI: `Resource Ceilings & Safe State Mutation`
   - Principle VII: `Code Standards, Consistent Terminology & Secure Logging`
2. **Given** rule bodies and the Precedence Order table, **When** reviewing text, **Then** flowery phrases (e.g., "epistemic truth", "primary source digs", "plausible guess or inference by analogy", "truly silent swallowing", "bug ratchet") are replaced with direct, professional engineering standards.

---

### User Story 2 - Synchronize Reusable Governance Templates, Presets, and Companion Standards (Priority: P2)

As a project maintainer or bootstrapper user, I need the reusable constitution template, preset templates, and companion standards (`coding-standards.md`, `logging-standards.md`) to reflect the updated, precise language so that existing standards and newly initialized projects inherit crisp language.

**Why this priority**: Templates in `.specify/templates/`, presets in `.specify/presets/base-governance/`, and companion standards in `.specify/memory/` and `.specify/templates/` must remain synchronized with the constitution.

**Independent Test**: Can be validated by inspecting `constitution-template.md`, `coding-standards-template.md`, `logging-standards-template.md` across `.specify/templates/`, `.specify/presets/base-governance/`, and `.specify/memory/`, confirming consistent terminology.

**Acceptance Scenarios**:
1. **Given** `constitution-template.md` in `.specify/templates/` and preset `base-governance`, **When** resolved, **Then** principle titles and bodies match the modernized wording.
2. **Given** `.specify/memory/coding-standards.md` and `.specify/memory/logging-standards.md`, **When** inspected, **Then** cross-references to Principle titles and any conversational phrasing are aligned.

---

### User Story 3 - Align Agent Personas, Skills, and Repository Documentation (Priority: P3)

As a contributor or AI agent executing Spec Kit workflows, I need agent prompts (`speckit-reasoner`, `speckit-executor`), workflow skills, and `README.md` to reference the updated principle titles and terminology so that cross-references remain consistent across Google Antigravity and Claude Code. Furthermore, documentation and governance references MUST simply cite GitHub's Spec Kit project ([`github/spec-kit`](https://github.com/github/spec-kit)) as the upstream foundation rather than restating its built-in concepts, focusing strictly on the capabilities and governance this repository adds.

**Why this priority**: Dual-client agent definitions (`.agents/` and `.claude/`) and documentation cite principle titles; they must use the updated names to maintain consistency. Eliminating redundant explanations of upstream GitHub Spec Kit keeps the documentation concise, high-signal, and focused on custom additions.

**Independent Test**: Can be validated by searching the repository for legacy phrases (like "Evidence Over Invention") and verifying they are updated to the ratified titles across both `.agents/` and `.claude/`, and inspecting `README.md` to confirm upstream Spec Kit is referenced without redundant restatements.

**Acceptance Scenarios**:
1. **Given** `.agents/agents/` and `.claude/agents/`, **When** inspecting Principle citations, **Then** they reference the modernized titles and maintain 100% byte-for-byte parity across both platforms.
2. **Given** `README.md`, **When** viewing the Core Governance table and overview, **Then** all 7 principles display the updated names, and the text cites upstream GitHub Spec Kit as a project dependency without restating its baseline mechanics.

---

## Edge Cases

- **Governance Rule Preservation**: Language cleanup MUST NOT weaken any existing governance constraints (e.g., fail closed on missing state, zero warnings, secret redaction, locked dependency gates).
- **Dual-Client File Parity**: Exact byte-for-byte parity MUST be maintained between `.agents/` and `.claude/` mirrored profiles and skills.
- **Historical Specs Immutability**: Historical specs (`specs/001-*` through `specs/007-*`) represent immutable records of past work and must not be altered.

---

## Requirements

### Functional Requirements

- **FR-001**: Modernize all 7 Core Principle titles across `.specify/memory/constitution.md`, `.specify/templates/constitution-template.md`, and preset templates:
  - Principle I: `Evidence-Based Decisions & Bounded Research`
  - Principle II: `Explicit Error Handling & Fail-Closed State`
  - Principle III: `Static Verification & Quality Gates` (active memory) / `Behavioral Testing & Deterministic Verification` (template)
  - Principle IV: `State Ownership, Architectural Seams & Safe Concurrency`
  - Principle V: `Centralized Dependencies & Toolchain Security`
  - Principle VI: `Resource Ceilings & Safe State Mutation`
  - Principle VII: `Code Standards, Consistent Terminology & Secure Logging`
- **FR-002**: Clean up rhetorical, conversational, and dramatic phrases across the body of all 7 principles and governance sections in `.specify/memory/constitution.md`:
  - Replace "plausible guess or inference by analogy" with "unverified assumptions or speculative guesses".
  - Replace "Primary source digs MUST be bounded" with "Source code and specification research MUST be focused".
  - Replace "Epistemic Truth, Trust Verification & Secret Safety" with "Factual Requirements, Trust Verification & Secret Safety".
  - Replace "Truly silent swallowing requires an inline comment proving why ignoring the failure is safe" with "Silently suppressing exceptions is prohibited without an explicit inline comment proving safety".
  - Replace "Defect Invariants (Broken Internal State)" with "Internal Invariants & System Integrity".
  - Replace "Hostile Boundary & Invariant Handling" with "Untrusted Input & Boundary Validation".
  - Replace "Bug Ratchet" with "Regression Test Coverage".
- **FR-003**: Clean up conversational or flowery language in companion standards:
  - `.specify/memory/coding-standards.md` and `.specify/templates/coding-standards-template.md` (and presets).
  - `.specify/memory/logging-standards.md` and `.specify/templates/logging-standards-template.md` (and presets).
- **FR-004**: Formally amend `.specify/memory/constitution.md` with an updated sync impact report, bumping version to `2.2.0` (minor: non-breaking principle wording and clarity modernization).
- **FR-005**: Propagate all ratified wording changes to `.specify/templates/constitution-template.md` and `.specify/presets/base-governance/templates/constitution-template.md`.
- **FR-006**: Update agent profiles in `.agents/agents/speckit-executor.md`, `.agents/agents/speckit-reasoner.md`, `.claude/agents/speckit-executor.md`, and `.claude/agents/speckit-reasoner.md` to reference the ratified principle names.
- **FR-007**: Update `README.md` Core Governance table to reflect the updated principle titles and descriptions.
- **FR-008**: Refactor `README.md` and governance documentation to reference upstream GitHub Spec Kit (`github/spec-kit`) as the foundation project without restating built-in Spec Kit concepts, commands, or workflows, concisely highlighting only what this toolkit adds on top of upstream Spec Kit.

---

## Clarifications & Ratified Decisions

- **Title Modernization**: Ratified Comprehensive cleanup (modernize all 7 principle titles into clear, industry-standard engineering terms).
- **Scope**: Ratified Full governance suite (active constitution, companion standards, templates, presets, agent profiles across `.agents/` and `.claude/`, and `README.md`).

---

## Success Criteria

- **SC-001**: Zero occurrences of "Evidence Over Invention" remain in active memory, templates, agent profiles, or README.md (all updated to "Evidence-Based Decisions & Bounded Research").
- **SC-002**: All 7 principles in `.specify/memory/constitution.md` and companion standards read clearly, professionally, and concisely without metaphorical or conversational AI prose.
- **SC-003**: 100% byte-for-byte parity is preserved between `.agents/` and `.claude/` mirrored agent profiles.
- **SC-004**: Pre-PR verification checks pass cleanly with zero warnings or broken references.
