# Interface Contract: Template Placeholder Tokens

**Feature**: `001-base-governance-templates`  
**Status**: Completed  
**Artifact**: `specs/001-base-governance-templates/contracts/placeholder-tokens.md`

## Overview

This contract catalogues all customizable placeholder tokens across the three governance templates. Every placeholder conforms to the strict format `[ALL_CAPS_IDENTIFIER]` or `[YYYY-MM-DD]` for calendar dates, ensuring reliable linting, validation, and automated initialization.

---

## 1. Syntax & Detection Rules

- **Standard Token Pattern**: `^\[[A-Z0-9_]+\]$`
- **Date Token Pattern**: `^\[YYYY-MM-DD\]$`
- **Version Token Pattern**: `^\[CONSTITUTION_VERSION\]$` (canonical template initializes to `1.0.0`)
- **Validation Rule**: Unsubstituted tokens in initialized or ratified files in `.specify/memory/` are flagged as incomplete governance initialization.

---

## 2. Placeholder Registry by Template

### 2.1 Constitution Template (`constitution-template.md`)

| Placeholder | Category | Required | Description | Example / Default Value |
|-------------|----------|----------|-------------|-------------------------|
| `[PROJECT_NAME]` | Identity | Yes | Name of the project or repository. | `AcmePlatform` |
| `[PRIMARY_SOURCE]` | Authority | Yes | Ranks highest in the Authority Hierarchy. | `Formal Protocol Specification v2.1` |
| `[SECONDARY_SOURCE]` | Authority | Yes | Ranks second in the Authority Hierarchy. | `Architecture Docs in docs/ or Verified Simulator` |
| `[TERTIARY_SOURCE]` | Authority | Yes | Ranks third in the Authority Hierarchy. | `Legacy Implementation in src/legacy/` |
| `[ACCEPTANCE_GATE_COMMANDS]` | Workflow | Yes | Local verification command(s) for live acceptance. | `./scripts/run-all-gates.sh` |
| `[YYYY-MM-DD]` | Date | Yes | Ratification and Last Amended date stamps. | `2026-11-04` |
| `[CONSTITUTION_VERSION]` | Version | Yes | Initial ratified version number. | `1.0.0` |

---

### 2.2 Coding Standards Template (`coding-standards-template.md`)

| Placeholder | Category | Required | Description | Example / Default Value |
|-------------|----------|----------|-------------|-------------------------|
| `[PROJECT_NAME]` | Identity | Yes | Name of the project or repository. | `AcmePlatform` |
| `[PRIMARY_LANGUAGE_AND_RUNTIME]` | Runtime | Yes | Primary programming language(s) and runtime versions. | `C# 12 / .NET 8 LTS` or `TypeScript 5.4 / Node.js 20` |
| `[BUILD_AND_LINTER_COMMANDS]` | Tooling | Yes | Build, format, and static analysis commands. | `dotnet build /warnaserror && dotnet format --verify-no-changes` |
| `[PROJECT_STRUCTURE_CONVENTIONS]` | Layout | Yes | Package, folder, and layer organization rules. | `src/Domain, src/Application, src/Infrastructure` |
| `[NAMING_CONVENTIONS]` | Style | Yes | Identifier naming conventions (casing, prefixes). | `PascalCase for types/methods, camelCase for params` |
| `[ERROR_RESULT_TYPES]` | Architecture | Yes | Canonical typed error container / result types. | `Result<T, Error>` or `OneOf<T, Error>` |
| `[TEST_FRAMEWORK_CONVENTIONS]` | Testing | Yes | Test framework, naming, and assertion conventions. | `xUnit with FluentAssertions; Method_Scenario_Expected outcome` |

---

### 2.3 Logging Standards Template (`logging-standards-template.md`)

| Placeholder | Category | Required | Description | Example / Default Value |
|-------------|----------|----------|-------------|-------------------------|
| `[PROJECT_NAME]` | Identity | Yes | Name of the project or repository. | `AcmePlatform` |
| `[LOGGING_FRAMEWORK]` | Telemetry | Yes | Structured logging library or abstraction. | `Serilog` or `Microsoft.Extensions.Logging` |
| `[LOG_SINKS_AND_FORMATS]` | Telemetry | Yes | Active output destinations and structured formats. | `Console (Compact JSON) + OpenTelemetry OTLP Exporter` |
| `[CORRELATION_ID_SCHEMA]` | Correlation | Yes | Ambient scope correlation header names and tokens. | `session_id`, `event_id`, `traceparent` |
| `[SENSITIVE_DATA_REDACTION_MECHANISM]` | Security | Yes | Middleware or serializer-level redaction policy/tools. | `Serilog.Enrichers.Sensitive + Custom Regex Redactor` |
| `[RETENTION_AND_SAMPLING_POLICY]` | Policy | Yes | Retention limits and high-frequency event sampling rules. | `Debug logs retained 7 days; >100/sec events sampled at 5%` |

---

## 3. Validation Rules

1. **Format Purity**: No lowercase letters, spaces, or special characters (other than `_` and `-`) may appear inside `[...]` placeholder brackets.
2. **Exhaustive Discovery**: Running `grep -o "\[[A-Z0-9_]*\]"` across the templates must return only tokens listed in this registry.
3. **No Unmarked Placeholders**: Templates must never contain colloquial markers like `TODO`, `TBD`, `<replace-me>`, or `FIXME` outside of explicit markdown code-block examples.
