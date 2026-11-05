# Data Model: Constitution Modernization Entities & Artifact Hierarchy

**Feature**: `specs/008-precise-constitution-language`  
**Date**: 2026-11-05  

## Governance Artifact Schema

```mermaid
erDiagram
    CONSTITUTION ||--o{ COMPANION_STANDARD : references
    CONSTITUTION ||--o{ AGENT_PERSONA : governs
    CONSTITUTION ||--o{ TEMPLATE_SUITE : derives
    CONSTITUTION ||--o{ PRESET_SUITE : synchronizes

    CONSTITUTION {
        string version "2.2.0"
        date ratified "2026-11-04"
        date last_amended "2026-11-05"
        Principle principles "Principles I through VII"
        PrecedenceRank precedence_order "Order 1 through 6"
    }

    COMPANION_STANDARD {
        string file_name "coding-standards.md / logging-standards.md"
        string cross_references "Cites Principle IDs & Titles"
    }

    AGENT_PERSONA {
        string client "agents or claude"
        string profile "speckit-executor.md or speckit-reasoner.md"
        string dynamic_deference "Cites Principle I..VII"
    }

    TEMPLATE_SUITE {
        string path ".specify/templates/*.md"
        string status "Normalized"
    }

    PRESET_SUITE {
        string path ".specify/presets/base-governance/templates/*.md"
        string status "Mirrored"
    }
```

## Entity Invariants

1. **Version Lifecycle**: `.specify/memory/constitution.md` advances from `2.1.0` to `2.2.0`.
2. **Top Amendment Comment**: The HTML header comment in `.specify/memory/constitution.md` tracks only the latest amendment summary (clearing historical accumulation per constitution rules).
3. **Dual Client Parity**: Files in `.agents/agents/` and `.claude/agents/` must have matching byte counts and checksums after edits.
