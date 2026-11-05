# Contract: Skill Streamlining & Dual-Client Parity

## Contract Invariants

1. **Parity Invariant**:
   For any skill file modified under `.agents/skills/<skill>/SKILL.md`, the exact file under `.claude/skills/<skill>/SKILL.md` MUST match byte-for-byte (`diff -r .agents/skills .claude/skills` must output nothing and return 0).

2. **Manifest Integrity Invariant**:
   Every modified skill file must have its updated byte length and SHA-256 hash calculated and stored in:
   - `.specify/integrations/agy.manifest.json`
   - `.specify/integrations/claude.manifest.json`
   - `.specify/integrations/speckit-bootstrap.manifest.json`

3. **Constitution Supremacy Invariant**:
   No skill file shall re-define or re-implement quality gates, testing policies, or documentation rules that duplicate statements in `.specify/memory/constitution.md`. All skills must cite `constitution.md` as non-negotiable authority.

## Canonical Snippets

### A. Template Resolution Snippet
```markdown
- **Resolve Template**: Read `{TEMPLATE_NAME}` from `.specify/templates/overrides/`, `.specify/presets/`, `.specify/extensions/`, or fallback to `.specify/templates/{TEMPLATE_NAME}`. If not found, fail closed per Principle II.
```

### B. Selective Governance Loading Snippet

1. **Stage 1 & 2 (Specify, Clarify)**:
```markdown
- **Load Governance**: Read `.specify/memory/constitution.md` for project scope boundaries and core principles.
```

2. **Stage 3 & 4 (Plan, Tasks)**:
```markdown
- **Load Governance**: Read `.specify/memory/constitution.md` for architectural boundaries, and relevant sections of `.specify/memory/coding-standards.md` (e.g. language/stack conventions).
```

3. **Stage 5, 6, 7 (Analyze, Implement, Converge)**:
```markdown
- **Load Governance**:
  - Read `.specify/memory/constitution.md` for high-level quality gates.
  - Read `.specify/memory/coding-standards.md` and `.specify/memory/logging-standards.md` for code-level conventions, error patterns, and logging rules.
```
