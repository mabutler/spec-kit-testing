# Feature Specification: Base Governance Suite & Templates

**Feature Branch**: `001-base-governance-templates`

**Created**: 2026-11-04

**Status**: Draft

**Input**: User description: "Phase 1. I'll attach the constitution and optional enhancement." (with attached Base Constitution v1.0.0 and Optional Enhancement Modules A–D)

## Clarifications

### Session 2026-11-04

- Q: Should the companion coding and logging standards templates be synthesized directly from the constitutional principles as language-agnostic baselines, or do you want to provide existing sample files to model them after? → A: Create language-agnostic templates informed by sample standards provided by user.
- Q: Should Optional Enhancement Modules A–D be placed inline directly within their target principles in `constitution-template.md`, or grouped in a dedicated catalog section at the end of the template? → A: Inline within target principles using structured HTML comment delimiters and replacement anchors.
- Q: Would you like to share your logging and coding standards samples now before we conclude clarification, or should we proceed to planning with language-agnostic templates derived directly from the constitutional principles? → A: Shared Software Logging Policy (CRITICAL, WARN, INFO, DEBUG, TRACE severity rules, audit-style milestones, attempt-and-outcome logging, automatic ambient scope correlation, and entry/exit TRACE rules) to incorporate into `logging-standards-template`; coding standards template remains language-agnostic with customizable convention slots referencing standard conventions (e.g., .NET) as exemplary guidance.
- Q: How should the governance templates be specified and verified to ensure full cross-platform compatibility without relying on shell scripts? → A: Treat templates as pure, platform-agnostic static Markdown files in `.specify/templates/` with zero runtime script dependencies; eliminate all Bash/POSIX requirements and verify templates via direct file and markdown structure inspection.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Resolve Rich Base Constitution Template with Optional Enhancements (Priority: P1)

Project maintainers and governance workflows need a comprehensive, production-grade Base Constitution Template that replaces the default empty placeholder scaffold. The template must provide the seven core non-negotiable engineering and epistemic principles out of the box, along with clearly delineated optional enhancement modules (Modules A–D) that can be selectively activated, replaced, or stripped when tailoring a project's constitution.

**Why this priority**: The constitution is the highest-authority governance document in the repository. Every downstream workflow (coding standards, logging standards, constitutional merge in Phase 2, and feature planning/implementation) depends on the base constitution structure, principles, placeholders, and optional module definitions.

**Independent Test**: Can be fully tested by verifying that `constitution-template.md` exists in `.specify/templates/` and verifying that the content contains all required sections, placeholders, the seven core principles, cross-references to companion standards, and structured, machine- and human-identifiable blocks for Optional Modules A through D without requiring any script execution.

**Acceptance Scenarios**:

1. **Given** a repository with the Phase 1 governance templates installed, **When** inspecting `constitution-template.md` in `.specify/templates/`, **Then** it contains the complete Base Constitution Template containing the Sync Impact Report header, Sources of Truth & Authority Hierarchy, Core Principles I–VII, Development Workflow & Quality Gates, Recorded Deviations, and Governance sections.
2. **Given** the resolved `constitution-template.md`, **When** a maintainer or automated workflow inspects the optional enhancements, **Then** Modules A, B, C, and D are present with explicit metadata indicating their module identifier, title, target principle location, and activation behavior (`ADD` to target principle vs. `REPLACE` specific clause in target principle, plus the nested optional sub-clause in Module D).
3. **Given** the resolved `constitution-template.md`, **When** a maintainer or automated workflow inspects the Governance Document Hierarchy section, **Then** it includes standardized references to both the companion coding standards and logging standards documents alongside project-level overrides.

---

### User Story 2 - Resolve Companion Coding Standards Template (Priority: P2)

Engineering leads and automated governance workflows need a reusable Coding Standards Template (`coding-standards-template.md`) that operationalizes the constitution's architectural, boundary, concurrency, error-handling, testing, and code-hygiene principles into concrete day-to-day coding conventions while providing clearly marked placeholder slots for project-specific language, toolchain, and architectural rules.

**Why this priority**: The constitution explicitly delegates detailed language and structural coding conventions to a companion coding standards document. Without a standardized template, projects either duplicate constitutional rules inconsistently or omit required baseline guardrails.

**Independent Test**: Can be fully tested by inspecting `coding-standards-template.md` in `.specify/templates/` and verifying that it includes universal baseline coding rules aligned with Principles I–VII alongside distinct project-specific customization slots without requiring any script execution.

**Acceptance Scenarios**:

1. **Given** a repository with the Phase 1 governance templates installed, **When** inspecting `coding-standards-template.md` in `.specify/templates/`, **Then** it contains a structured template containing universal baseline sections (authority link back to the Constitution, boundary isolation, two-tier error disposition, concurrency & immutable snapshots, type-safe identifiers, bounded input validation, testing & encapsulation rules, and code hygiene/commenting rules).
2. **Given** the resolved `coding-standards-template.md`, **When** a project maintainer customizes it for a specific codebase, **Then** all project-specific slots (target languages/runtimes, project layout & dependency rules, linter/formatter gates, naming conventions, and optional module hooks such as `// OPEN-QUESTION: OQ-XXX` tag syntax or table-driven dispatch conventions) are marked with standardized `[ALL_CAPS_IDENTIFIER]` placeholders.

---

### User Story 3 - Resolve Companion Logging Standards Template (Priority: P3)

Engineering leads and automated governance workflows need a reusable Logging Standards Template (`logging-standards-template.md`) that operationalizes Principle II (Two-Tier Failure Model) and Principle VII (Structured, Safe Logging) into concrete observability, severity-level, correlation, and secret/PII redaction standards, while providing clearly marked slots for project-specific logging frameworks and sinks.

**Why this priority**: Safe, structured logging and strict separation of severity levels (`DEBUG`, `INFO`, `WARN`, `CRITICAL`) are non-negotiable constitutional requirements that need a dedicated companion template so teams can plug in their specific telemetry stack without weakening redaction or failure-disposition rules.

**Independent Test**: Can be fully tested by inspecting `logging-standards-template.md` in `.specify/templates/` and verifying that it defines universal severity semantics, structured template rules, correlation/context propagation, and secret/PII prohibition alongside project-specific sink and library placeholders without requiring any script execution.

**Acceptance Scenarios**:

1. **Given** a repository with the Phase 1 governance templates installed, **When** inspecting `logging-standards-template.md` in `.specify/templates/`, **Then** it contains a structured template containing universal baseline sections (severity level taxonomy for `DEBUG`/`INFO`/`WARN`/`CRITICAL` mapped to the Two-Tier Failure Model, structured message template rules, correlation and diagnostic context requirements, prohibited sensitive data / PII / credential redaction rules, and testability rules prohibiting log-text assertions in unit tests).
2. **Given** the resolved `logging-standards-template.md`, **When** a project maintainer customizes it for a specific codebase, **Then** all project-specific slots (logging library/abstraction, sink & transport configuration, retention/sampling policies, and structured property naming conventions) are marked with standardized `[ALL_CAPS_IDENTIFIER]` placeholders.

---

### Edge Cases

- **Additive vs. Replacement Optional Modules**: Module A (Principle I), Module C (Principle IV), and Module D (Principle V) *append* rules to their target principles, whereas Module B (Principle III) *replaces* the "Plan Justification & Skip Allowlist" bullet in Principle III with the "100% Branch Coverage Gate". The template markup must unambiguously distinguish additive modules from replacement modules—and identify the exact default block replaced by Module B—so neither human authors nor Phase 2 merge workflows leave contradictory rules in Principle III.
- **Nested Optional Clause within an Optional Module**: Module D includes an inner optional clause (`[Optional: Shared libraries consumed by constrained environments SHOULD be AOT/trim-safe, isolating any untrimmable code to the narrowest scope with documented justification.]`). The template markup must preserve this inner option clearly so it can be independently included or omitted when Module D is enabled.
- **Cross-Platform Static Template Compatibility**: All three template names (`constitution-template.md`, `coding-standards-template.md`, `logging-standards-template.md`) use lowercase alphanumeric and hyphen characters (`[a-z0-9-]+.md`) and are authored as static, platform-independent Markdown files stored in `.specify/templates/`, requiring zero runtime scripts or shell-specific tooling to be consumed on any operating system.
- **Legacy vs. Memory Cross-Reference Alignment**: The base constitution references both `.specify/memory/{coding-standards,logging-standards}.md` (for Spec Kit workflows) and traditional repository paths (`CodingStandards.md` / `docs/logging.md`), ensuring links remain clear whether a project consumes the standards from `.specify/memory/` or mirrors them in repository documentation.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The governance template suite MUST provide three platform-agnostic Markdown templates: `constitution-template.md`, `coding-standards-template.md`, and `logging-standards-template.md` in `.specify/templates/`, retrievable directly via standard file-based access across all operating systems without runtime shell or script dependencies.
- **FR-002**: `constitution-template` MUST preserve the exact structure, headings, and wording of the canonical Base Constitution (provided in the Canonical Source Content section below), including:
  - Top-level `Sync Impact Report` HTML comment block (`<!-- Sync Impact Report ... -->`)
  - `# [PROJECT_NAME] Constitution` title
  - `## Sources of Truth & Authority Hierarchy` with ordered placeholders `[PRIMARY_SOURCE]`, `[SECONDARY_SOURCE]`, and `[TERTIARY_SOURCE]`
  - `## Core Principles` containing Principles I through VII (`I. Evidence Over Invention & Bounded Investigation`, `II. Two-Tier Failure Model & Fail Closed on Required State`, `III. Behavioral, Value-Driven Testing & Deterministic Execution`, `IV. Single Authoritative State, Enforced Boundaries & Safe Concurrency`, `V. Centralized Dependencies & Protected Toolchain Gate`, `VI. Bounded Resources & Verify-Before-Destroy`, `VII. Code Hygiene, Ubiquitous Language & Safe Logging`)
  - `## Development Workflow & Quality Gates` with `[ACCEPTANCE_GATE_COMMANDS]` placeholder
  - `## Recorded Deviations`
  - `## Governance` with Document Hierarchy, Precedence Order (1 through 6), Amendment & Versioning, and footer `**Version**: [CONSTITUTION_VERSION] | **Ratified**: [RATIFICATION_DATE] | **Last Amended**: [LAST_AMENDED_DATE]` (defaulting initial version example to `1.0.0` and `[YYYY-MM-DD]` date slots).
- **FR-003**: `constitution-template` MUST embed all four Optional Enhancement Modules (Modules A, B, C, and D) inline directly within their target principles using structured, machine-parseable HTML comment markers that specify:
  - Module ID (`MODULE-A`, `MODULE-B`, `MODULE-C`, `MODULE-D`)
  - Module Title
  - Target Principle (`Principle I`, `Principle III`, `Principle IV`, `Principle V`)
  - Integration Action (`ADD` for Modules A, C, D; `REPLACE` targeting the `Plan Justification & Skip Allowlist` bullet in Principle III for Module B)
  - Nested sub-option marker within Module D for the AOT/trim-safe shared library clause.
- **FR-004**: `constitution-template` MUST cross-reference the companion coding standards and logging standards documents in the `Governance -> Document Hierarchy` section, linking to the co-located governance standards (`coding-standards.md` and `logging-standards.md` alongside optional repository-root/docs aliases `CodingStandards.md` / `docs/logging.md`).
- **FR-005**: `coding-standards-template` MUST be authored as a language-agnostic baseline template informed by user-provided standards samples, providing universal non-negotiable rules directly aligned with the Base Constitution:
  - Constitutional authority header and precedence declaration
  - Architectural & compile-time boundary enforcement (separating domain logic from wire schemas and OS/hardware I/O seams)
  - Two-tier failure handling & explicit exception disposition rules
  - Concurrency, lock discipline, and immutable snapshot (`record` / `record struct`) patterns
  - Disambiguated identifier value types (`readonly record struct`)
  - Bounded untrusted input validation and verify-before-destroy safeguards
  - Unit test encapsulation, determinism, and hostile-boundary testing conventions
  - Code hygiene, ubiquitous language, present-tense high-signal comments, and open-question pointer conventions.
- **FR-006**: `coding-standards-template` MUST provide explicit `[ALL_CAPS_IDENTIFIER]` placeholder sections for project-specific conventions, including at minimum: `[PROJECT_NAME]`, `[PRIMARY_LANGUAGE_AND_RUNTIME]`, `[BUILD_AND_LINTER_COMMANDS]`, `[PROJECT_STRUCTURE_CONVENTIONS]`, `[NAMING_CONVENTIONS]`, `[ERROR_RESULT_TYPES]`, and `[TEST_FRAMEWORK_CONVENTIONS]`, with placeholder comments referencing standard conventions (e.g., .NET coding conventions) as non-binding exemplary patterns.
- **FR-007**: `logging-standards-template` MUST be authored as a language-agnostic baseline template informed by the user's Software Logging Policy sample, providing universal non-negotiable observability rules directly aligned with Principles II and VII of the Base Constitution:
  - Constitutional authority header and precedence declaration
  - Strict Five-Tier Severity Taxonomy:
    - `CRITICAL`: System restarting; MUST include exception and restart reason.
    - `WARN`: Recoverable boundary rejection or failed-but-continuing operation worth monitoring for patterns; declined/failed operations MUST NOT be hidden in DEBUG.
    - `INFO`: Significant lifecycle milestone stating the business/system outcome rather than diagnostic data; reads like an audit trail. Significant actions MUST log both attempt and result so mid-operation crashes leave a record. Infrequent/one-time startup, initialization, and shutdown in otherwise verbose layers MUST log at INFO.
    - `DEBUG`: Application's interpretation of state and diagnostic reasoning prior to a milestone ("engineer's working notes"); diagnostic data MUST NOT leak into INFO.
    - `TRACE`: Mechanical entry and exit logging on every function and return path with parameter and return values; complex objects MUST use a ToString override or dedicated cheap-property helper rather than ad-hoc inline field selection; external library calls MUST NOT emit TRACE (results logged at DEBUG in caller).
  - Structured logging template rules (named placeholders/properties rather than string interpolation)
  - Ambient scope correlation: Correlation tokens (`session_id`, `event_id`) MUST be read automatically from execution scope state and NEVER manually passed or logged at call sites.
  - Mandatory redaction: Passwords, tokens, secrets, API keys, full credit cards, SSNs, government IDs, and raw PII are strictly forbidden; internal entity IDs (GUIDs, database IDs, usernames) are permitted.
  - Observability performance: Expensive log argument evaluation MUST be guarded with level checks; sustained high-frequency events (>100/sec) MUST be sampled or aggregated rather than logged per-event.
  - Testing boundary rule: Unit tests MUST NOT assert on log message text or operator display strings.
- **FR-008**: `logging-standards-template` MUST provide explicit `[ALL_CAPS_IDENTIFIER]` placeholder sections for project-specific observability conventions, including at minimum: `[PROJECT_NAME]`, `[LOGGING_FRAMEWORK]`, `[LOG_SINKS_AND_FORMATS]`, `[CORRELATION_ID_SCHEMA]`, `[SENSITIVE_DATA_REDACTION_MECHANISM]`, and `[RETENTION_AND_SAMPLING_POLICY]`.
- **FR-009**: All placeholder tokens across all three templates that require project-specific replacement during governance initialization MUST follow the consistent `[ALL_CAPS_IDENTIFIER]` format (or `[YYYY-MM-DD]` for ISO dates) so downstream governance skills can automatically detect and validate unresolved placeholders.

### Key Entities

- **Constitution Template (`constitution-template.md`)**: The primary governance scaffold defining the authority hierarchy, seven core principles, optional enhancement modules (A–D), quality gates, recorded deviations table/list, and governance amendment rules.
- **Optional Enhancement Module**: A self-contained, toggleable constitutional rule block (`MODULE-A` through `MODULE-D`) annotated with target principle metadata and integration semantics (`ADD` vs. `REPLACE`).
- **Coding Standards Template (`coding-standards-template.md`)**: Companion governance template pairing universal constitutional coding rules with project-specific language, architecture, and tooling slots.
- **Logging Standards Template (`logging-standards-template.md`)**: Companion governance template pairing universal constitutional logging, severity taxonomy, and secret-safety rules with project-specific telemetry framework and sink slots.

### Canonical Source Content *(Authoritative Input for Phase 1)*

#### 1. Optional Enhancement Modules

- **Module A: In-Code Open Question Pointers (Add to Principle I)**
  > **Pointer-Only Code Tags:** When an open question or deferred verification leaves a temporary stub or boundary gap in source code, it MAY be marked exclusively with a pointer tag (`// OPEN-QUESTION: OQ-XXX`) referencing its entry in reference/open-questions.md. Free-text `TODO` comments or duplicate prose explanations in source code are forbidden.

- **Module B: Strict 100% Branch Coverage Profile (Replaces Skip Allowlist in Principle III)**
  > **100% Branch Coverage Gate:** 100% automated branch coverage MUST be maintained across the codebase; line coverage alone does not satisfy this gate. Coverage exclusions require a written code annotation and are permitted ONLY for schema-generated code and defect-invariant checks (whose justification must name the invariant protected).

- **Module C: Table-Driven Dispatch (Add to Principle IV)**
  > **Dispatch Is Data, Not Branches:** Behavior that varies per protocol class, command, or event code MUST be registered as data in a single startup-validated registry/table (one handler type per command), never split across hand-maintained switch statements or parallel validation/execution conditionals that can silently drift out of sync.

- **Module D: Regulated / Certified Systems (Add to Principles V)**
  > **Reproducible Builds & Deliberate Versioning:** Submitted components MUST build deterministically from pinned toolchains; where bit-reproducibility is impossible (e.g., OS/WinPE images), component docs MUST specify the signed manifest verification used instead. major.minor versions change only by explicit human submission planning; patch is computed automatically from git history. [Optional: Shared libraries consumed by constrained environments SHOULD be AOT/trim-safe, isolating any untrimmable code to the narrowest scope with documented justification.]

#### 2. Base Constitution Text

```markdown
<!--
Sync Impact Report (Latest Amendment Only — Do Not Accumulate History):
- Version Change: 0.0.0 -> 1.0.0
- Modified Principles: Initial ratification from Standard Base Template.
- Modified Sections: All core sections initialized.
- Rationale: Establish baseline engineering, epistemic, and workflow guardrails.
-->

# [PROJECT_NAME] Constitution

## Sources of Truth & Authority Hierarchy

When specifications, reference documents, test harnesses, or existing code disagree, authority ranks in this strict order:

1. **[PRIMARY_SOURCE]** (e.g., Formal Protocol Specification / Regulatory Requirements)
2. **[SECONDARY_SOURCE]** (e.g., Reconciled Architecture Docs in `docs/` or Verified Simulator Behavior)
3. **[TERTIARY_SOURCE]** (e.g., Legacy Implementation / Upstream Adapter Contracts)

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

### III. Behavioral, Value-Driven Testing & Deterministic Execution
Every automated test MUST guard meaningful behavioral contracts or plausible regressions through production entry points.
- **Encapsulation & Contract Focus**: Visibility MUST NOT be widened (`private` to `public`), and test-only members MUST NOT be added solely to reach internals (`InternalsVisibleTo` requires written justification). Tests MUST verify behavioral outcomes and MUST NOT assert on log text, operator display strings, or the absence of deleted code/files.
- **Plan Justification & Skip Allowlist**: Every `/speckit-plan` MUST list the tests it intends to write and state what risk each guards against. Comprehensive behavioral and branch coverage is expected across all domain logic, state machines, parsers, and error boundaries. Omitting unit tests without a plan justification is permitted ONLY for:
  1. Compiler-generated, XSD/schema-generated, or source-generator code.
  2. Defect-invariant guards (`UnreachableException`, internal post-validation assertions) unreachable via public entry points.
  3. Pure data carriers (DTOs, immutable `record` snapshots) and thin pass-through adapter wrappers over OS/hardware seams.
  4. Application host bootstrap (`Program.cs`), declarative CLI binding declarations, and declarative UI layout markup covered by smoke/acceptance gates.
  5. One-off build/provisioning scripts verified by automated linters and live acceptance gates.
- **Unprivileged, Deterministic Unit Tests**: Automated unit tests MUST run without administrator/root privileges and MUST NOT touch real disks/partitions, real network endpoints, or committed cryptographic key material (ephemeral keys/certs are generated per run). Time MUST be injected (`TimeProvider` or explicit timestamps) and randomness seeded.
- **Hostile Boundary Coverage & Bug Ratchet**: Any parser of untrusted bytes or security verification gate MUST include negative and hostile-input tests (malformed payloads, oversized counts, offset overflows, bad signatures). Every defect discovered in integration testing, simulator runs, or production MUST receive a reproducing regression test alongside the fix.

### IV. Single Authoritative State, Enforced Boundaries & Safe Concurrency
- **Single Source of Truth**: Every piece of domain state MUST have exactly one authoritative owning model. Registries, lookup tables, and projections are read-only views or pure indexes—never competing, independently mutated copies of state owned elsewhere.
- **Structurally Enforced Boundaries**: Core domain logic MUST NOT depend on wire/serialization schema types or raw OS/hardware/process I/O. Wire translation happens strictly at the boundary and is enforced at compile time via the project reference graph (e.g., `PrivateAssets="all"` / absent project references), not by import conventions. Disk, network, process, and hardware access MUST sit behind interface seams so unit tests use fakes.
- **Safe Concurrency & Snapshot Isolation**: A thread holding an entity state lock MUST NOT acquire another entity lock or invoke external callbacks, event subscribers, or cross-entity logic while holding the lock. Side effects are recorded inside the critical section and dispatched in order *after* the lock is released. Code outside an entity's lock works exclusively from immutable snapshots (`record` / `record struct`) captured under the lock, never from live mutable references.
- **Disambiguated Colliding Identifiers**: When two or more identifiers or unit-bearing quantities of the same primitive type (e.g., `DeviceId` and `HostId`) are routinely passed together across method boundaries, they MUST be wrapped in distinct, non-convertible value types (`readonly record struct`). Single-identifier lookups may use standard primitives.

### V. Centralized Dependencies & Protected Toolchain Gate
- **Centralized, Locked Supply Chain**: All package versions and shared compiler settings MUST be declared centrally at the repository root (e.g., `Directory.Packages.props`, `Directory.Build.props`, and committed lockfiles). Project-local overrides are forbidden without documented justification. Internal shared code within the repository is consumed via project/module reference, never packaged internally.
- **Deliberate Package Selection**: Prefer mature, actively maintained libraries that substantially simplify design over custom infrastructure code; reject obscure, poorly maintained, or trivial micro-packages.
- **Human-Only Toolchain & Security Gate**: AI agents MUST NOT—without explicit human instruction—add or upgrade third-party packages, modify package sources (`NuGet.config`), alter SDK/toolchain versions (`global.json`), weaken compiler warning/strictness flags, modify version manifests (`version.json`), or generate/modify cryptographic signing keys and certificates.

### VI. Bounded Resources & Verify-Before-Destroy
- **Correctness Over Unmeasured Speed**: Absent a documented numeric performance target and benchmark in component documentation, code MUST NOT trade correctness, verification, or recoverability for speed.
- **Bounded Untrusted Input**: Every allocation size, collection count, offset, loop bound, and recursion depth derived from untrusted or external input MUST be validated against an explicit ceiling before memory allocation or iteration (using overflow-safe arithmetic). Large files and payloads MUST be streamed in fixed-size chunks rather than buffered whole in memory. Network and IPC calls MUST enforce explicit timeouts and support cancellation.
- **Verify Before Mutate/Destroy**: Destructive or irreversible steps (disk/partition erase, state reset, schema drop, file overwrite) MUST execute only after all cheap checks, space/resource checks, and full input verifications have passed, and MUST be protected by explicit confirmation or opt-in guards.

### VII. Code Hygiene, Ubiquitous Language & Safe Logging
- **Zero Warnings & Read-Only Vendored Code**: The build treats warnings as errors (`TreatWarningsAsErrors`), and all code/scripts MUST pass configured linters. Vendored third-party code and generated schema files MUST NOT be edited or reformatted in place.
- **Ubiquitous Language**: Code identifiers, UI screens, CLI tools, and documentation share one domain vocabulary; changes MUST NOT introduce a synonym for an existing concept.
- **Present-Tense, High-Signal Comments & Docs**: Comments MUST explain the current implementation and *why* it is built that way—never narrate git or session history. Comments SHOULD document rejected alternatives only when needed to stop a developer from reintroducing a known defect via a naive refactor. Documentation MUST match actual implemented behavior and be updated in the same change.
- **Structured, Safe Logging**: Logs MUST use structured templates and strictly separate lifecycle milestones/outcomes (`INFO`) from diagnostic reasoning/state (`DEBUG`), recoverable boundary rejections (`WARN`), and fatal invariant crashes (`CRITICAL`). Logs and operator-visible errors MUST NEVER output secrets, private keys, credentials, raw PII, or bearer financial instruments.

## Development Workflow & Quality Gates

- **Spec Kit Pipeline & Ephemeral Specs**: Feature work follows the Spec Kit lifecycle (`spec.md` -> `plan.md` -> `tasks.md`). A feature spec is a transient proposal for one change, not permanent documentation. Before a feature's final pull request merges, all decisions, state contracts, and known gaps that outlive the feature MUST be promoted into permanent documentation (`Architecture.md`, component docs, or `open-questions.md`), and that final pull request MUST delete the `specs/NNN-*/` folder. Production code, comments, documentation, and commit messages outside `specs/` MUST NOT cite spec folders or `FR-XXX` identifiers.
- **Pre-PR Verification**: `main` MUST always build cleanly. Before opening a pull request, the author or agent MUST run locked dependency restore, full build (zero warnings), linters, and the automated test suite locally, plus any project-defined Live/Simulator Acceptance Gate: **[ACCEPTANCE_GATE_COMMANDS]**.
- **Review & Merge Authority**: Pull requests SHOULD remain under ~500 lines; larger changes should be split. AI agents MUST NOT merge pull requests.

## Recorded Deviations

Any ratified exception to a Core Principle MUST be recorded here with: (1) Principle violated, (2) Ratifying human authority, (3) Rationale, (4) Compensating control, and (5) Known gap and documentation link.

- *None currently recorded.*

## Governance

- **Document Hierarchy**: This constitution supersedes all other repository practices. Detailed language conventions live in `CodingStandards.md` / `docs/logging.md`, as-built structural records live in `Architecture.md`, and day-to-day agent operational context lives in `CLAUDE.md` / `AGENTS.md`. Where a lower-level document conflicts with a Core Principle here, this constitution wins. Where `Architecture.md` conflicts with working, compliant code, update `Architecture.md` to match the code.
- **Precedence Order**: When principles conflict, the earlier concern wins in this exact order:
  1. Epistemic Truth, Trust Verification & Secret Safety (Principles I, VII)
  2. Fail Closed & Resource/Destructive Safety (Principles II, VI)
  3. Architectural Boundaries, Single State & Concurrency (Principle IV)
  4. Testing & Supply-Chain/Toolchain Gates (Principles III, V)
  5. Code Hygiene & Style (Principle VII)
  6. Unbenchmarked Performance (Principle VI)
  Degrading a higher-ranked concern to serve a lower-ranked one requires human owner ratification and an entry under **Recorded Deviations**.
- **Amendment & Versioning**: Amendments require explicit human approval, a rationale, and a Semantic Version bump (`MAJOR` for backward-incompatible principle removals/redefinitions; `MINOR` for new principles or expanded gates; `PATCH` for clarifications). Only the most recent amendment summary is kept in the top HTML sync comment.

**Version**: 1.0.0 | **Ratified**: [YYYY-MM-DD] | **Last Amended**: [YYYY-MM-DD]
```

#### 3. Canonical Reference Content: User Software Logging Policy Sample

```markdown
## Software Logging Policy

### Log Levels
- **CRITICAL** — system restarting. Include exception and restart reason.
- **WARN** — failure, execution continuing. Worth monitoring for patterns.
- **INFO** — significant lifecycle milestone. States the outcome, not the data behind it. Should read like an audit trail.
- **DEBUG** — application's interpretation of state before a milestone. "Engineer's working notes." Not a lower tier of INFO.
- **TRACE** — mechanical entry/exit with parameter and return values.

### What belongs at each level
- INFO states what happened ("Payment held for review"). DEBUG carries the reasoning ("FraudScore=0.87 exceeds threshold=0.75"). Never put diagnostic data in INFO.
- Do not re-log what a callee's TRACE already shows. If data is significant enough for DEBUG, prefer promoting that TRACE line to DEBUG over adding a second line. Do not skip a DEBUG log just because a TRACE covers the same data.
- Significant actions being taken (not just outcomes) belong at INFO — log both the attempt and the result so a crash mid-operation leaves a record.
- Declined/failed-but-continuing operations are WARN, not DEBUG — they're worth monitoring for patterns in production.
- A layer that's otherwise verbose/DEBUG (an internal engine, driver, or backend implementation behind a higher-level entry point) still logs its own one-time startup/initialization/shutdown actions at INFO, if the action runs once per lifecycle and its effect persists for the whole lifecycle afterward. The "this layer is DEBUG" default applies to repeating, per-event work, not one-shot lifecycle actions.

### TRACE rules
- Entry and exit on every function, every return path.
- Exit TRACE required even when INFO or WARN immediately precedes the return statement.
- Complex object parameters: use a ToString() override or ToTrace() helper with a fixed set of cheap properties. Do not select fields inline at each call site.
- External library calls have no TRACE. Log what came back at DEBUG in the caller instead.

### Do not log
- Passwords, tokens, secrets, API keys
- Full credit card numbers, SSNs, government IDs, or raw PII. Internal record IDs (GUIDs, row IDs, usernames) are fine.

### Correlation IDs
- session_id and event_id are read from scope state automatically. Never pass them as parameters or log them manually at the call site.

### Performance
- Guard expensive log arguments with a level check. Simple variable interpolation needs no guard.
- High-frequency events (sustained >100/sec): sample or aggregate rather than logging every occurrence.
```

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of the 3 governance templates (`constitution-template.md`, `coding-standards-template.md`, `logging-standards-template.md`) exist as valid, well-formed Markdown files in `.specify/templates/` and can be inspected directly on any platform with zero script execution dependencies.
- **SC-002**: 100% of the 7 Core Principles, 4 Optional Enhancement Modules (A–D, including Module D's nested sub-option), and required governance sections from the canonical input are present and intact in the resolved `constitution-template`.
- **SC-003**: Every optional module in `constitution-template` has unambiguous start/end delimiters and target action metadata (`ADD` vs. `REPLACE`) so a human maintainer or automated workflow can enable or strip any subset of Modules A–D in a single pass with zero residual broken markdown or duplicate/conflicting clauses.
- **SC-004**: 100% of customizable slots across all 3 templates use standardized `[ALL_CAPS_IDENTIFIER]` (or `[YYYY-MM-DD]`) tokens and are documented so zero undocumented placeholders exist.

## Assumptions

- **Platform-Agnostic Static File Placement**: The three templates will be installed directly as static Markdown files in `.specify/templates/`. They require zero script runtimes, POSIX tools, or shell scripts to function, ensuring full cross-platform compatibility across Windows, macOS, and Linux.
- **Optional Module Delimiter Convention**: Optional Enhancement Modules A–D will be embedded inline at their respective target principles in `constitution-template.md` using structured HTML comment blocks (e.g., `<!-- OPTIONAL-MODULE: MODULE-A ... -->` ... `<!-- /OPTIONAL-MODULE: MODULE-A -->`, and `<!-- DEFAULT-CLAUSE: REPLACEABLE-BY-MODULE-B -->` around the default Skip Allowlist in Principle III) so both human readers and the Phase 2 merge workflow can inspect, activate, or strip them in context.
- **Cross-Reference Paths**: The `Document Hierarchy` bullet in `constitution-template.md` will reference the companion governance files (`coding-standards.md` / `CodingStandards.md` and `logging-standards.md` / `docs/logging.md`) so projects using `.specify/memory/` in Phase 2 as well as projects exposing docs in the repo root have consistent, unbroken references.
- **Scope Boundary Between Phase 1 and Phase 2**: Phase 1 delivers the static templates and verifies their resolution and structural integrity. Modifying the `speckit-constitution` skill to simultaneously generate and merge `.specify/memory/{constitution,coding-standards,logging-standards}.md` is deferred to Phase 2 per `ROADMAP.md`.
