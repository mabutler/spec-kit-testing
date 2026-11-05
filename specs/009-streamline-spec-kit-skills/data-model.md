# Data Model: Streamline Spec Kit Skills & Decouple Bloat

## Entities & Schemas

### 1. Skill Governance Profile
Defines which governance documents each skill must load at runtime:

| Skill | Loaded Governance Files | Primary Focus |
|---|---|---|
| `speckit-specify` | `constitution.md` | Core scope boundaries, evidence rules |
| `speckit-clarify` | `constitution.md` | Core scope boundaries |
| `speckit-plan` | `constitution.md`, `coding-standards.md` | Architectural seams, language conventions |
| `speckit-tasks` | `constitution.md`, `coding-standards.md` | Story breakdown, task ordering |
| `speckit-analyze` | `constitution.md` | High-level constitutional compliance |
| `speckit-implement` | `constitution.md`, `coding-standards.md`, `logging-standards.md` | Concrete syntax, error patterns, logging rules |
| `speckit-converge` | `constitution.md` | Completion verification |

### 2. Template Resolution Directive
Standardized concise template resolution instruction across skills:
```text
Resolve `<template-name>.md` from `.specify/templates/overrides/`, `.specify/presets/`, `.specify/extensions/`, or fallback to `.specify/templates/<template-name>.md`. If not found, fail closed per Principle II.
```

### 3. Documentation Governance Model
- Delegated entirely to `constitution.md` (Principle VII) and `coding-standards.md` (Conventions).
- Removed from explicit branching logic in individual skills.
