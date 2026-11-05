# [PROJECT_NAME] Coding Standards

## Constitutional Authority & Precedence

This document operationalizes the universal engineering principles established in the **[PROJECT_NAME] Constitution** into concrete, stack-specific implementation conventions for this repository.

- **Authority Link**: Governed by `.specify/memory/constitution.md` (or `constitution.md`). Universal rules defined in the Constitution (epistemic authority, two-tier failure semantics, behavioral testing, single authoritative state, supply-chain protection, bounded resources, and code hygiene) are not repeated here.
- **Precedence Declaration**: The Constitution ranks highest in authority. In any conflict between this Coding Standards document and the Core Principles of the Constitution, the Constitution strictly prevails.
- **Scope**: Applies to all production code, internal libraries, build scripts, and automated test harnesses maintained in this repository.

---

## Language, Runtime & Toolchain

Operationalizes Constitutional Principles V (*Centralized Dependencies & Protected Toolchain Gate*) and VII (*Zero Warnings & Read-Only Vendored Code*):

- **Target Platform**: [PRIMARY_LANGUAGE_AND_RUNTIME]
  <!-- Example: C# 12 / .NET 8 LTS, or TypeScript 5.4 / Node.js 20, or Rust 1.78 stable -->
- **Build, Linter & Zero-Warning Gates**: [BUILD_AND_LINTER_COMMANDS]
  <!-- Example: dotnet build /warnaserror && dotnet format --verify-no-changes, or cargo clippy -- -D warnings && cargo fmt --check -->
- **Dependency & Lockfile Conventions**: [DEPENDENCY_AND_LOCKFILE_CONVENTIONS]
  <!-- Example: Central package versions in Directory.Packages.props with packages.lock.json, or pnpm-lock.yaml / Cargo.lock committed at repo root -->

---

## Architecture, Module Layout & Compile-Time Boundaries

Operationalizes Constitutional Principle IV (*Structurally Enforced Boundaries*):

- **Project Structure & Layer Organization**: [PROJECT_STRUCTURE_CONVENTIONS]
  <!-- Example: src/Domain (pure domain logic), src/Application (use cases & port interfaces), src/Infrastructure (I/O & wire adapters) -->
- **Compile-Time Boundary & I/O Seam Enforcement**: [BOUNDARY_ENFORCEMENT_MECHANISM]
  <!-- Example: Domain project has zero package/project references to serialization or I/O libraries; OS, clock, filesystem, and network access sit behind explicit interface seams -->

---

## Error Handling & Failure Idioms

Operationalizes Constitutional Principle II (*Two-Tier Failure Model & Fail Closed on Required State*):

- **Canonical Result Types for Rejected Operations**: [ERROR_RESULT_TYPES]
  <!-- Example: Result<T, DomainError> or OneOf<T, Error> returned at boundaries for expected validation/external rejections -->
- **Defect Invariant & Fail-Closed Mechanism**: [DEFECT_INVARIANT_MECHANISM]
  <!-- Example: Unrecoverable precondition/state violations log at CRITICAL and terminate/fail-fast immediately rather than returning a recoverable error result (see Canonical Result Types above) -->

---

## State, Concurrency & Identifier Idioms

Operationalizes Constitutional Principle IV (*Safe Concurrency & Disambiguated Colliding Identifiers*):

- **Immutable Snapshots & Disambiguated ID Types**: [IMMUTABLE_SNAPSHOT_AND_ID_CONVENTIONS]
  <!-- Example: Cross-boundary state exposed as immutable records/structs; collocated primitive IDs (e.g., DeviceId, HostId) wrapped in distinct non-convertible value types -->

---

## Testing Framework & Conventions

Operationalizes Constitutional Principle III (*Behavioral, Value-Driven Testing & Deterministic Execution*):

- **Test Framework, Determinism & Naming**: [TEST_FRAMEWORK_CONVENTIONS]
  <!-- Example: xUnit / pytest / vitest; injected clock/randomness fakes; test naming: MethodName_Scenario_ExpectedOutcome -->

---

## Naming, Formatting & Code Style

Operationalizes Constitutional Principle VII (*Code Hygiene & Ubiquitous Language*):

- **Identifier & Code Style Conventions**: [NAMING_CONVENTIONS]
  <!-- Example: PascalCase for types/methods, camelCase for parameters/locals, or snake_case per language standard; present-tense "why" comments -->
