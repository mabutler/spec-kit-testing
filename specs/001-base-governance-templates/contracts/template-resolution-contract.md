# Interface Contract: Template Resolution & File Access

**Feature**: `001-base-governance-templates`  
**Status**: Completed  
**Artifact**: `specs/001-base-governance-templates/contracts/template-resolution-contract.md`

## Overview

This contract defines the interfaces for accessing and resolving the governance templates:
1. **Direct Platform-Agnostic File Access**: Zero-runtime-dependency file access across all operating systems (Windows, macOS, Linux).
2. **Spec Kit Bash Resolver CLI**: Backward-compatible resolution utility for POSIX/Bash environments (`resolve-template.sh`).

---

## 1. Direct File Access Interface (Universal / Platform-Agnostic)

Every governance template is stored as a pure, static Markdown file in `.specify/templates/`. Any tool, editor, or agent on any operating system can inspect or read the templates directly via standard filesystem paths relative to the repository root.

### Canonical File Paths

| Template Identifier | Repository-Relative Path | Description |
|---------------------|--------------------------|-------------|
| `constitution-template` | `.specify/templates/constitution-template.md` | Base Constitution v1.0.0 with Core Principles I–VII and inline Optional Modules A–D. |
| `coding-standards-template` | `.specify/templates/coding-standards-template.md` | Language-agnostic coding standards baseline with customizable project slots. |
| `logging-standards-template` | `.specify/templates/logging-standards-template.md` | Companion telemetry standards template with 5-tier severity policy and redaction rules. |

---

## 2. Command Invocation Interface (Spec Kit Bash Resolver)

For environments running the Spec Kit Bash toolchain, templates can also be resolved dynamically:

```bash
.specify/scripts/bash/resolve-template.sh <template-name> [--json]
```

### Parameters & Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `<template-name>` | Positional String | Yes | Name of the template to resolve. Valid characters: `[a-z0-9-]+`. |
| `--json` | Flag | No | When present, formats output as a single-line JSON string. When omitted, emits raw template content to `stdout`. |
| `-h`, `--help` | Flag | No | Displays usage information and exits with code 0. |

---

## Output Contract (Bash Resolver)

### Raw Text Mode (Default)
- **Standard Output (`stdout`)**: The complete resolved content of the template file as UTF-8 encoded text.
- **Standard Error (`stderr`)**: Empty on success. Contains diagnostic error message on failure.
- **Exit Code**:
  - `0`: Template found and resolved successfully.
  - `1`: Template name missing, invalid format, or template file not found in any layer.
  - `2`: Parsing or I/O error occurred during preset/extension manifest evaluation.

### JSON Mode (`--json`)
- **Standard Output (`stdout`)**: A single JSON object on one line:
  ```json
  {
    "TEMPLATE_NAME": "<template-name>",
    "TEMPLATE_CONTENT": "<raw-content-with-escaped-newlines-and-quotes>"
  }
  ```
- **Standard Error (`stderr`)**: Empty on success. Contains diagnostic error message on failure.
- **Exit Code**: Same as Raw Text Mode.

---

## Target Template Identifiers for Phase 1

The following three template identifiers MUST resolve successfully via both direct file access and the CLI resolver interface:

1. `constitution-template`:
   - Path resolved: `.specify/templates/constitution-template.md`
   - Content: Full Base Constitution v1.0.0 with Core Principles I–VII and inline Optional Modules A–D.

2. `coding-standards-template`:
   - Path resolved: `.specify/templates/coding-standards-template.md`
   - Content: Language-agnostic coding standards template with universal constitutional baseline rules and customizable project slots.

3. `logging-standards-template`:
   - Path resolved: `.specify/templates/logging-standards-template.md`
   - Content: Telemetry and observability template with 5-tier severity taxonomy, ambient correlation, redaction rules, and telemetry sink slots.
