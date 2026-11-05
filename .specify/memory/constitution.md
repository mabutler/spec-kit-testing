<!--
Sync Impact Report (Latest Amendment Only — Do Not Accumulate History):
- Version Change: 1.0.0 -> 2.0.0
- Modified Principles: Principle III weakened/redefined per explicit human authority to eliminate automated test generation requirements in favor of static verification.
- Modified Sections: Core Principles (Principle III), Development Workflow & Quality Gates, Recorded Deviations
- Optional Modules: MODULE-A: OMITTED, MODULE-B: OMITTED, MODULE-C: OMITTED, MODULE-D: OMITTED (MODULE-D-AOT-TRIM: OMITTED), TRACE Logging: OMITTED
- Companion Standards: coding-standards.md (updated), logging-standards.md (updated)
- Rationale: Explicit human authority directive to weaken/redefine Core Principle III to disallow automated test generation across the project.
- Deferred TODOs: None
-->

# Spec Kit Testing Constitution

## Sources of Truth & Authority Hierarchy

When specifications, reference documents, test harnesses, or existing code disagree, authority ranks in this strict order:

1. **Feature Specifications & Acceptance Requirements** (Ratified documents in `specs/`)
2. **Architecture & Design Documentation** (`Architecture.md`, `README.md`)
3. **Existing Implementation & Script Harnesses** (Source code and automation scripts)

## Core Principles

### I. Evidence Over Invention & Bounded Investigation
Every domain behavior, protocol constant, schema element, and security requirement MUST trace to an authoritative source listed in the Authority Hierarchy above. Neither a human nor an AI agent may fill an unverified gap with a plausible guess or inference by analogy.
- **Bounded, Cited Research**: Investigation MUST traverse the Authority Hierarchy in order, consulting local reference and architecture documentation before opening primary specs or legacy source repositories. Primary source digs MUST be bounded to the specific file or section answering the question and cite `file:line` or section/page numbers. If the sources do not answer the question, the required output is **NOT FOUND** naming what was searched.
- **Centralized Open Questions**: Every unknown, ambiguity, or deferred gap that outlives a single task MUST be recorded in `reference/open-questions.md` (citing what was checked, who can resolve it, and any temporary working assumption). Undocumented gaps or silent placeholders are defects.

### II. Two-Tier Failure Model & Fail Closed on Required State
Failures divide into two distinct categories and MUST be handled accordingly:
- **Rejected Operations (Expected / External Failures)**: Invalid inputs, unsupported requests, or transient boundary/I/O failures MUST be detected at the earliest boundary, aborted before mutating state, logged at `WARN`, and returned as an explicit, typed error result while leaving the system running. Low-level I/O and cryptographic exceptions MUST be caught narrowly at the boundary and translated into typed errors.
- **Defect Invariants (Broken Internal State)**: Programmer errors, violated preconditions, or corrupted internal state MUST NOT be caught to keep running. The affected execution scope MUST log at `CRITICAL` and halt/restart immediately so untrusted state cannot propagate.
- **Explicit Exception Disposition**: Every `catch` block MUST either (1) translate the exception into a typed boundary error, (2) enrich and rethrow, or (3) log at `WARN` and isolate/continue *only* on designated non-critical paths (e.g., best-effort cleanup or isolated dispatch loops) where failure cannot corrupt state or masquerade as a successful mutation. Truly silent swallowing requires an inline comment proving why ignoring the failure is safe.
- **Explicit Unimplemented Semantics**: Code MUST NOT substitute guessed defaults for missing required data. Unimplemented or intentionally unsupported operations on an interface surface MUST return distinct, typed `NotImplemented` or `Unsupported` results—never empty method bodies that simulate success.
- **Fail Closed on Required State**: State, checks, or configuration required for security, integrity, or diagnosability MUST be established before dependent functions run. Quietly degrading, continuing with a warning, or retrying silently in the background is forbidden unless ratified under Recorded Deviations.

### III. Static Verification & No Automated Tests
This project does not generate, require, or maintain automated test suites. All feature delivery and quality verification rely strictly on static analysis, syntax validation, and declarative quality gates.
- **Encapsulation & Contract Focus**: Visibility MUST NOT be widened (`private` to `public`), and artificial inspection members MUST NOT be added. Code contracts are verified through static typing, schema constraints, and linter rules.
- **Plan Justification & Skip Allowlist**: Automated test generation is disabled repository-wide. Spec Kit feature workflows (`spec.md`, `plan.md`, `tasks.md`, `implement`) MUST NOT generate unit test files, integration test harnesses, or test tasks. All feature tasks focus directly on implementation, validation scripts, and documentation.
- **Hostile Boundary & Invariant Handling**: Input parsers and security checks enforce boundary defenses and fail-closed invariants in production logic without requiring automated test harness files.

### IV. Single Authoritative State, Enforced Boundaries & Safe Concurrency
- **Single Source of Truth**: Every piece of domain state MUST have exactly one authoritative owning model. Registries, lookup tables, and projections are read-only views or pure indexes—never competing, independently mutated copies of state owned elsewhere.
- **Structurally Enforced Boundaries**: Core domain logic MUST NOT depend on wire/serialization schema types or raw OS/hardware/process I/O. Wire translation happens strictly at the boundary and is enforced at compile time via the build/module dependency graph, not by import conventions. Disk, network, process, and hardware access MUST sit behind interface seams so unit tests use fakes.
- **Safe Concurrency & Snapshot Isolation**: A thread holding an entity state lock MUST NOT acquire another entity lock or invoke external callbacks, event subscribers, or cross-entity logic while holding the lock. Side effects are recorded inside the critical section and dispatched in order *after* the lock is released. Code outside an entity's lock works exclusively from immutable snapshots captured under the lock, never from live mutable references.
- **Disambiguated Colliding Identifiers**: When two or more identifiers or unit-bearing quantities of the same primitive type (e.g., `DeviceId` and `HostId`) are routinely passed together across method boundaries, they MUST be wrapped in distinct, non-convertible value types. Single-identifier lookups may use standard primitives.

### V. Centralized Dependencies & Protected Toolchain Gate
- **Centralized, Locked Supply Chain**: All package versions and shared compiler/linter settings MUST be declared centrally at the repository root with committed lockfiles. Project-local overrides are forbidden without documented justification. Internal shared code within the repository is consumed via project/module reference, never packaged internally.
- **Deliberate Package Selection**: Prefer mature, actively maintained libraries that substantially simplify design over custom infrastructure code; reject obscure, poorly maintained, or trivial micro-packages.
- **Human-Only Toolchain & Security Gate**: AI agents MUST NOT—without explicit human instruction—add or upgrade third-party packages, modify package sources or registries, alter SDK/toolchain versions, weaken compiler/linter warning or strictness flags, modify version manifests, or generate/modify cryptographic signing keys and certificates.

### VI. Bounded Resources & Verify-Before-Destroy
- **Correctness Over Unmeasured Speed**: Absent a documented numeric performance target and benchmark in component documentation, code MUST NOT trade correctness, verification, or recoverability for speed.
- **Bounded Untrusted Input**: Every allocation size, collection count, offset, loop bound, and recursion depth derived from untrusted or external input MUST be validated against an explicit ceiling before memory allocation or iteration (using overflow-safe arithmetic). Large files and payloads MUST be streamed in fixed-size chunks rather than buffered whole in memory. Network and IPC calls MUST enforce explicit timeouts and support cancellation.
- **Verify Before Mutate/Destroy**: Destructive or irreversible steps (disk/partition erase, state reset, schema drop, file overwrite) MUST execute only after all cheap checks, space/resource checks, and full input verifications have passed, and MUST be protected by explicit confirmation or opt-in guards.

### VII. Code Hygiene, Ubiquitous Language & Safe Logging
- **Zero Warnings & Read-Only Vendored Code**: The build treats warnings as errors, and all code/scripts MUST pass configured linters. Vendored third-party code and generated schema files MUST NOT be edited or reformatted in place.
- **Ubiquitous Language**: Code identifiers, UI screens, CLI tools, and documentation share one domain vocabulary; changes MUST NOT introduce a synonym for an existing concept.
- **Present-Tense, High-Signal Comments & Docs**: Comments MUST explain the current implementation and *why* it is built that way—never narrate git or session history. Comments SHOULD document rejected alternatives only when needed to stop a developer from reintroducing a known defect via a naive refactor. Documentation MUST match actual implemented behavior and be updated in the same change.
- **Structured, Safe Logging**: Logs MUST use structured templates and strictly separate lifecycle milestones, diagnostic reasoning, recoverable boundary rejections, and fatal invariant crashes according to the severity taxonomy defined in `.specify/memory/logging-standards.md` / `docs/logging.md`. Logs and operator-visible errors MUST NEVER output secrets, private keys, credentials, raw PII, or bearer financial instruments.

## Development Workflow & Quality Gates

- **Spec Kit Pipeline & Ephemeral Specs**: Feature work follows the Spec Kit lifecycle (`spec.md` -> `plan.md` -> `tasks.md`). A feature spec is a transient proposal for one change, not permanent documentation. Before a feature's final pull request merges, all decisions, state contracts, and known gaps that outlive the feature MUST be promoted into permanent documentation (`Architecture.md`, component docs, or `open-questions.md`), and that final pull request MUST delete the `specs/NNN-*/` folder. Production code, comments, documentation, and commit messages outside `specs/` MUST NOT cite spec folders or `FR-XXX` identifiers.
- **Pre-PR Verification**: `main` MUST always build cleanly. Before opening a pull request, the author or agent MUST run locked dependency restore, full build (zero warnings), linters, and any project-defined Live/Simulator Acceptance Gate: `.specify/scripts/bash/resolve-template.sh constitution-template --json`.
- **Review & Merge Authority**: Pull requests SHOULD remain under ~500 lines; larger changes should be split. AI agents MUST NOT merge pull requests.

## Recorded Deviations

Any ratified exception to a Core Principle MUST be recorded here with: (1) Principle violated, (2) Ratifying human authority, (3) Rationale, (4) Compensating control, and (5) Known gap and documentation link.

- *None currently recorded (Principle III amended directly per human authority to establish static verification without automated tests).*

## Governance

- **Document Hierarchy**: This constitution supersedes all other repository practices. Detailed language conventions live in `.specify/memory/coding-standards.md` / `CodingStandards.md`, logging standards live in `.specify/memory/logging-standards.md` / `docs/logging.md`, as-built structural records live in `Architecture.md`, and day-to-day agent operational context lives in `CLAUDE.md` / `AGENTS.md`. Where a lower-level document conflicts with a Core Principle here, this constitution wins. Where `Architecture.md` conflicts with working, compliant code, update `Architecture.md` to match the code.
- **Precedence Order**: When principles conflict, the earlier concern wins in this exact order:
  1. Epistemic Truth, Trust Verification & Secret Safety (Principles I, VII)
  2. Fail Closed & Resource/Destructive Safety (Principles II, VI)
  3. Architectural Boundaries, Single State & Concurrency (Principle IV)
  4. Toolchain, Supply-Chain & Static Quality Gates (Principles III, V)
  5. Code Hygiene & Style (Principle VII)
  6. Unbenchmarked Performance (Principle VI)
  Degrading a higher-ranked concern to serve a lower-ranked one requires human owner ratification and an entry under **Recorded Deviations**.
- **Amendment & Versioning**: Amendments require explicit human approval, a rationale, and a Semantic Version bump (`MAJOR` for backward-incompatible principle removals/redefinitions; `MINOR` for new principles or expanded gates; `PATCH` for clarifications). Only the most recent amendment summary is kept in the top HTML sync comment.

**Version**: 2.0.0 | **Ratified**: 2026-11-04 | **Last Amended**: 2026-11-04
