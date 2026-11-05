# Phase 0 Research: Precise & Clear Constitution Language

**Feature**: `specs/008-precise-constitution-language`  
**Date**: 2026-11-05  

## Research Questions & Decisions

### 1. Principle Titles Mapping

| Number | Current Title | Cleaned / Precise Title | Rationale |
| :--- | :--- | :--- | :--- |
| **Principle I** | `Evidence Over Invention & Bounded Investigation` | `Evidence-Based Decisions & Bounded Research` | Direct, professional wording replacing the informal/conversational "Over Invention" metaphor. |
| **Principle II** | `Two-Tier Failure Model & Fail Closed on Required State` | `Explicit Error Handling & Fail-Closed State` | Clear software engineering concepts replacing academic "Two-Tier Failure Model" terminology. |
| **Principle III** | `Static Verification & No Automated Tests` (Memory) / `Behavioral, Value-Driven Testing & Deterministic Execution` (Template) | `Static Verification & Quality Gates` (Memory) / `Behavioral Testing & Deterministic Verification` (Template) | Professional, standard quality gate terminology. |
| **Principle IV** | `Single Authoritative State, Enforced Boundaries & Safe Concurrency` | `State Ownership, Architectural Seams & Safe Concurrency` | Standard software architecture concepts ("seams", "ownership") replacing conversational descriptors. |
| **Principle V** | `Centralized Dependencies & Protected Toolchain Gate` | `Centralized Dependencies & Toolchain Security` | Direct security and dependency management framing. |
| **Principle VI** | `Bounded Resources & Verify-Before-Destroy` | `Resource Ceilings & Safe State Mutation` | Standard systems engineering terminology for quotas and mutation guards. |
| **Principle VII** | `Code Hygiene, Ubiquitous Language & Safe Logging` | `Code Standards, Consistent Terminology & Secure Logging` | Standard industry vocabulary ("Code Standards", "Consistent Terminology", "Secure Logging") replacing DDD jargon and metaphors. |

### 2. Rhetorical and Flowery Phrases to Clean Up

1. **"Neither a human nor an AI agent may fill an unverified gap with a plausible guess or inference by analogy."**  
   -> *Cleaned*: "Neither engineers nor AI agents may substitute unverified assumptions or speculative guesses for authoritative requirements."
2. **"Primary source digs MUST be bounded to the specific file or section answering the question and cite file:line or section/page numbers. If the sources do not answer the question, the required output is NOT FOUND naming what was searched."**  
   -> *Cleaned*: "Source code and specification research MUST be focused on the specific file or section answering the question and cite `file:line` or section numbers. If the sources do not answer the question, the required output is **NOT FOUND** stating what was checked."
3. **"Truly silent swallowing requires an inline comment proving why ignoring the failure is safe."**  
   -> *Cleaned*: "Silently suppressing exceptions is prohibited without an explicit inline comment proving why ignoring the failure is safe."
4. **"Hostile Boundary & Invariant Handling"**  
   -> *Cleaned*: "Untrusted Boundary & Input Validation"
5. **"Epistemic Truth, Trust Verification & Secret Safety"** (Precedence Order)  
   -> *Cleaned*: "Verified Requirements, Trust Verification & Secret Safety"
6. **"Bug Ratchet"** (in template)  
   -> *Cleaned*: "Regression Test Coverage"

### 3. File Targets & Invariants

All changes will be applied cleanly to:
- `.specify/memory/constitution.md` (bumped to version `2.2.0`)
- `.specify/memory/coding-standards.md`
- `.specify/memory/logging-standards.md`
- `.specify/templates/constitution-template.md`
- `.specify/templates/coding-standards-template.md`
- `.specify/templates/logging-standards-template.md`
- `.specify/presets/base-governance/templates/constitution-template.md`
- `.specify/presets/base-governance/templates/coding-standards-template.md`
- `.specify/presets/base-governance/templates/logging-standards-template.md`
- `.agents/agents/speckit-executor.md` and `.claude/agents/speckit-executor.md` (100% parity)
- `.agents/agents/speckit-reasoner.md` and `.claude/agents/speckit-reasoner.md` (100% parity)
- `README.md` (Core Governance table)
