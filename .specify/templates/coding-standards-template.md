# [PROJECT_NAME] Coding Standards

## Constitutional Authority & Precedence

This document operationalizes the engineering principles established in the **[PROJECT_NAME] Constitution** into concrete implementation standards and coding conventions.

- **Authority Link**: Governed by the rules and principles defined in `.specify/memory/constitution.md` (or `constitution.md`).
- **Precedence Declaration**: The Constitution ranks highest in authority. In any conflict between this Coding Standards document and the Core Principles of the Constitution, the Constitution strictly prevails.
- **Scope**: Applies to all production code, internal libraries, scripts, and automated test harnesses maintained in this repository.

---

## Compile-Time & Architectural Boundaries

In accordance with Constitutional Principle IV (*Single Authoritative State, Enforced Boundaries & Safe Concurrency*):

1. **Domain Isolation**: Core domain logic MUST NOT depend directly on wire/serialization schema types, database client entities, or raw OS/hardware/network I/O.
2. **Boundary Enforcement**: Boundary isolation MUST be enforced at compile time through the project reference graph or build module definitions (e.g., absent package/project references or `PrivateAssets="all"`), rather than relying solely on discretionary import conventions.
3. **I/O Seams**: All filesystem, network, system clock, process execution, and hardware interactions MUST be encapsulated behind interface seams so that business logic can be tested deterministically using isolated unit test fakes.

---

## Two-Tier Failure Handling

In accordance with Constitutional Principle II (*Two-Tier Failure Model & Fail Closed on Required State*):

1. **Expected / Rejected Operations**:
   - Boundary validation failures, invalid inputs, unauthorized requests, or transient external service rejections MUST be detected at the earliest entry point.
   - Operations MUST abort before mutating persistent state, log at `WARN`, and return an explicit, typed error result (`[ERROR_RESULT_TYPES]`).
   - Low-level network, I/O, or parsing exceptions MUST be caught narrowly at the boundary seam and mapped to domain-specific typed errors.
2. **Defect Invariants (Broken State)**:
   - Programmer bugs, internal state corruption, and broken preconditions MUST NOT be swallowed or caught to maintain execution.
   - Execution scope MUST log at `CRITICAL` and fail closed or abort immediately to prevent propagation of untrusted state.
3. **Explicit Exception Disposition**:
   - Every `catch` block MUST perform one of three actions: (1) translate the caught exception into a typed boundary error, (2) enrich and rethrow, or (3) log at `WARN` and isolate on designated non-critical cleanup paths where failure cannot corrupt state.
   - Swallowing exceptions silently is prohibited unless accompanied by an inline comment proving why ignoring the failure is provably safe.
4. **Explicit Unimplemented Semantics**:
   - Missing required data MUST NOT be replaced with guessed defaults.
   - Unsupported or unimplemented interface operations MUST return explicit typed `NotImplemented` or `Unsupported` results—never empty methods that simulate success.

---

## Concurrency, Lock Discipline & Immutable Snapshots

In accordance with Constitutional Principle IV (*Safe Concurrency*):

1. **Single Owning Model**: Every domain entity has exactly one authoritative owner responsible for state mutations. Projections, caches, and lookup tables are read-only views.
2. **Lock Hierarchy & Discipline**:
   - A thread holding an entity state lock MUST NOT acquire another entity lock.
   - A thread holding an entity lock MUST NOT invoke external callbacks, publish notifications, or invoke cross-entity methods while inside the critical section.
   - Side effects and events MUST be recorded inside the critical section and dispatched in order *after* the lock is released.
3. **Immutable Snapshots**:
   - Code executing outside an entity's internal lock MUST operate exclusively on immutable data snapshots (`record` or `record struct`), never on live, mutable reference state.

---

## Disambiguated Identifier Value Types

In accordance with Constitutional Principle IV (*Disambiguated Colliding Identifiers*):

1. **Collocated Primitive Disambiguation**:
   - When two or more identifiers or unit-bearing quantities sharing the same primitive type (e.g., `DeviceId` and `HostId`, or `Width` and `Height`) are passed together across method or API boundaries, they MUST be wrapped in distinct, non-convertible value types (`readonly record struct`).
2. **Single Identifiers**:
   - Single-identifier lookups where parameter collisions are impossible may use standard primitive types.

---

## Bounded Inputs & Resource Protection

In accordance with Constitutional Principle VI (*Bounded Resources & Verify-Before-Destroy*):

1. **Untrusted Input Ceilings**:
   - Allocation sizes, collection capacities, loop bounds, and recursion depths derived from untrusted inputs MUST be validated against an explicit upper bound before memory allocation or iteration.
   - Arithmetic on size and offset calculations MUST be overflow-checked.
2. **Payload Streaming & Timeouts**:
   - Payloads and files of unbounded size MUST be processed as streams in fixed-size buffers rather than loaded whole into memory.
   - Network and inter-process calls MUST configure explicit cancellation tokens and non-infinite timeouts.
3. **Verify Before Mutate/Destroy**:
   - Irreversible actions (file deletion, record deletion, storage formatting, partition erase) MUST execute only after all cheap validations, authorization checks, and space/resource verifications pass.
   - Destructive actions MUST require explicit confirmation or opt-in safety flags.

---

## Hostile Boundary & Behavioral Unit Testing

In accordance with Constitutional Principle III (*Behavioral, Value-Driven Testing & Deterministic Execution*):

1. **Contract-Focused Encapsulation**:
   - Visibility MUST NOT be widened (`private` to `public`) solely to accommodate tests. Test-only hooks in production classes are forbidden.
   - Tests MUST verify observable behavioral contracts and state outcomes, never log text strings or UI display messages.
2. **Determinism & Isolation**:
   - Automated unit tests MUST run without administrative/root privileges and MUST NOT access real disks, real network sockets, or static hardware timers.
   - System time MUST be injected via mockable time providers and random number generators must be seeded.
3. **Hostile Boundary Testing & Regression Ratchet**:
   - Parsers of untrusted inputs and security validation filters MUST include negative, hostile, and boundary test cases (malformed structures, negative lengths, offset overflows).
   - Every production defect or test-simulator failure MUST receive a reproducing regression test before the bug fix merges.

---

## Code Hygiene & Commenting Conventions

In accordance with Constitutional Principles I and VII (*Code Hygiene, Ubiquitous Language & Bounded Investigation*):

1. **Zero Warnings**:
   - Builds MUST treat compiler warnings as errors. Code MUST pass configured linters and formatters before submission.
2. **Ubiquitous Language**:
   - Identifier names, domain models, CLI flags, and configuration keys MUST adhere strictly to the project's canonical domain vocabulary without introducing synonyms.
3. **High-Signal, Present-Tense Comments**:
   - Comments MUST describe *why* a particular implementation approach was chosen, not narrate revision history or repeat what the code obviously does.
4. **Pointer Tags for Open Questions**:
   - Where temporary stubs, workarounds, or deferred investigations exist, they MUST be tagged with a pointer tag (e.g., `// OPEN-QUESTION: OQ-XXX`) referencing the central ledger in `reference/open-questions.md`. Free-text untracked `TODO` comments are prohibited.

---

## Project Conventions & Customization Slots

This section defines project-specific toolchains, conventions, and architectural slots for **[PROJECT_NAME]**.

### Runtime & Language Environment
- **Target Platform**: [PRIMARY_LANGUAGE_AND_RUNTIME]
  <!-- Example: C# 12 / .NET 8 LTS, or TypeScript 5.4 / Node.js 20, or Rust 1.78 stable -->

### Build & Verification Commands
- **Build & Quality Gates**: [BUILD_AND_LINTER_COMMANDS]
  <!-- Example: dotnet build /warnaserror && dotnet format --verify-no-changes -->

### Directory & Layer Organization
- **Project Structure**: [PROJECT_STRUCTURE_CONVENTIONS]
  <!-- Example: src/Domain (pure logic), src/Application (use cases), src/Infrastructure (I/O adapters) -->

### Naming & Style Rules
- **Identifier Conventions**: [NAMING_CONVENTIONS]
  <!-- Example: PascalCase for types and methods; camelCase for parameters and local variables; _camelCase for private fields -->

### Error Container & Result Types
- **Canonical Result Types**: [ERROR_RESULT_TYPES]
  <!-- Example: Result<T, DomainError> or OneOf<T, Error> for rejected operations -->

### Automated Test Conventions
- **Test Framework & Naming**: [TEST_FRAMEWORK_CONVENTIONS]
  <!-- Example: xUnit with FluentAssertions; Test naming: MethodName_Scenario_ExpectedOutcome -->
