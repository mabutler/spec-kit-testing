# Interface Contract: Optional Enhancement Module Delimiters

**Feature**: `001-base-governance-templates`  
**Status**: Completed  
**Artifact**: `specs/001-base-governance-templates/contracts/optional-module-delimiters.md`

## Overview

This contract formalizes the delimiter grammar, metadata format, and regex patterns for Optional Enhancement Modules (A–D), default replaceable clauses, and nested sub-clauses embedded in `constitution-template.md`. This interface ensures seamless human readability and deterministic automated processing for Phase 2 constitutional merge workflows.

---

## 1. Delimiter Grammar

### 1.1 Additive Modules (`MODULE-A`, `MODULE-C`, `MODULE-D`)

Used when an optional module appends rules to a target principle without removing default text.

```markdown
<!-- OPTIONAL-MODULE: {MODULE_ID}
Action: ADD
Title: {MODULE_TITLE}
Target: {TARGET_PRINCIPLE}
-->
{MODULE_CONTENT}
<!-- /OPTIONAL-MODULE: {MODULE_ID} -->
```

#### Parsing Regular Expression (PCRE / Python):
```regex
<!-- OPTIONAL-MODULE:\s*(MODULE-[A-Z0-9]+)\s*\nAction:\s*ADD\s*\nTitle:\s*([^\n]+)\s*\nTarget:\s*([^\n]+)\s*-->\n([\s\S]*?)<!-- \/OPTIONAL-MODULE:\s*\1\s*-->
```

---

### 1.2 Replacement Modules & Default Clauses (`MODULE-B`)

Used when an optional module replaces a default clause in a target principle. The replaced default clause MUST be enclosed in a `DEFAULT-CLAUSE` delimiter indicating which module can replace it.

#### Default Clause Enclosure:
```markdown
<!-- DEFAULT-CLAUSE: {CLAUSE_ID} (REPLACEABLE-BY: {MODULE_ID})
Target: {TARGET_PRINCIPLE}
-->
{DEFAULT_CLAUSE_CONTENT}
<!-- /DEFAULT-CLAUSE: {CLAUSE_ID} -->
```

#### Replacement Module Enclosure:
```markdown
<!-- OPTIONAL-MODULE: {MODULE_ID}
Action: REPLACE
Target: {TARGET_PRINCIPLE}
Replaces: {CLAUSE_ID}
Title: {MODULE_TITLE}
-->
{MODULE_CONTENT}
<!-- /OPTIONAL-MODULE: {MODULE_ID} -->
```

#### Parsing Regular Expression for Replacement Module:
```regex
<!-- OPTIONAL-MODULE:\s*(MODULE-[A-Z0-9]+)\s*\nAction:\s*REPLACE\s*\nTarget:\s*([^\n]+)\s*\nReplaces:\s*([^\n]+)\s*\nTitle:\s*([^\n]+)\s*-->\n([\s\S]*?)<!-- \/OPTIONAL-MODULE:\s*\1\s*-->
```

---

### 1.3 Nested Sub-Clauses (`MODULE-D` Inner Option)

Used for optional sub-rules within an optional module that can be independently toggled.

```markdown
<!-- OPTIONAL-SUBCLAUSE: {SUBCLAUSE_ID}
Action: OPTIONAL-INCLUSION
Parent-Module: {PARENT_MODULE_ID}
Title: {SUBCLAUSE_TITLE}
-->
{SUBCLAUSE_CONTENT}
<!-- /OPTIONAL-SUBCLAUSE: {SUBCLAUSE_ID} -->
```

#### Parsing Regular Expression:
```regex
<!-- OPTIONAL-SUBCLAUSE:\s*([A-Z0-9-]+)\s*\nAction:\s*OPTIONAL-INCLUSION\s*\nParent-Module:\s*([A-Z0-9-]+)\s*\nTitle:\s*([^\n]+)\s*-->\n([\s\S]*?)<!-- \/OPTIONAL-SUBCLAUSE:\s*\1\s*-->
```

---

## 2. Canonical Module Delimiter Manifest

### Module A: In-Code Open Question Pointers
- **Module ID**: `MODULE-A`
- **Action**: `ADD`
- **Target**: `Principle I`
- **Placement**: Directly following the `- **Centralized Open Questions**:` bullet under Principle I.

### Module B: Strict 100% Branch Coverage Profile
- **Default Clause ID**: `PLAN-JUSTIFICATION-AND-SKIP-ALLOWLIST`
- **Target**: `Principle III`
- **Default Clause Scope**: Encloses the `- **Plan Justification & Skip Allowlist**:` bullet and all 5 numbered allowlist items under Principle III.
- **Module ID**: `MODULE-B`
- **Action**: `REPLACE`
- **Replaces**: `PLAN-JUSTIFICATION-AND-SKIP-ALLOWLIST`
- **Placement**: Directly following the closing delimiter `<!-- /DEFAULT-CLAUSE: PLAN-JUSTIFICATION-AND-SKIP-ALLOWLIST -->`.

### Module C: Table-Driven Dispatch
- **Module ID**: `MODULE-C`
- **Action**: `ADD`
- **Target**: `Principle IV`
- **Placement**: Directly following the `- **Disambiguated Colliding Identifiers**:` bullet under Principle IV.

### Module D: Regulated / Certified Systems
- **Module ID**: `MODULE-D`
- **Action**: `ADD`
- **Target**: `Principle V`
- **Placement**: Directly following the `- **Human-Only Toolchain & Security Gate**:` bullet under Principle V.
- **Nested Sub-Clause ID**: `MODULE-D-AOT-TRIM`
  - Scope: Encloses `[Optional: Shared libraries consumed by constrained environments SHOULD be AOT/trim-safe, isolating any untrimmable code to the narrowest scope with documented justification.]`.

---

## 3. Transformation Operations for Downstream Consumers

1. **Activate Additive Module**: Strip the opening `<!-- OPTIONAL-MODULE: ... -->` and closing `<!-- /OPTIONAL-MODULE: ... -->` comment lines, preserving `{MODULE_CONTENT}` in place.
2. **Deactivate Additive Module**: Remove both comment delimiters and the enclosed `{MODULE_CONTENT}` entirely.
3. **Activate Replacement Module (e.g., Module B)**:
   - Remove the `<!-- DEFAULT-CLAUSE: ... -->` ... `<!-- /DEFAULT-CLAUSE: ... -->` block and its default content entirely.
   - Strip the opening `<!-- OPTIONAL-MODULE: ... -->` and closing `<!-- /OPTIONAL-MODULE: ... -->` comment lines from the replacement module, preserving `{MODULE_CONTENT}` in place.
4. **Deactivate Replacement Module (Default)**:
   - Strip the `<!-- DEFAULT-CLAUSE: ... -->` and `<!-- /DEFAULT-CLAUSE: ... -->` comment tags, preserving the default clause content in place.
   - Remove the replacement module delimiters and content entirely.
5. **Handle Nested Sub-Clause**:
   - If included: Strip `<!-- OPTIONAL-SUBCLAUSE: ... -->` and `<!-- /OPTIONAL-SUBCLAUSE: ... -->` comment lines.
   - If excluded: Remove the delimiters and inner content.
