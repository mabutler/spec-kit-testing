# Contract: README Structure and Content Validation Schema

**Feature Branch**: `010-clean-readme`  
**Document Target**: `README.md`  
**Schema Version**: 1.0.0  

---

## 1. Top-Level Markdown Document Contract

The repository root `README.md` MUST comply with the following structural schema:

```markdown
# Spec Kit Customizations

[Short description introducing extensions for GitHub Spec Kit]

---

## Project Overview & Architecture

[Summary of capabilities, relationship to upstream GitHub Spec Kit, unique extensions, and client parity]

---

## Co-Applied Governance Suite

[Concise descriptions and direct relative links to constitution.md, coding-standards.md, and logging-standards.md]

---

## Spec Kit Skills & Subagent Orchestration Reference

### Subagent Personas
[speckit-reasoner and speckit-executor persona definitions]

### Custom Skills
[Focused table or list of unique skills: /speckit-orchestrate, /speckit-bootstrap, /speckit-roadmap]

### Core Pipeline Integration
[Concise summary of how standard Spec Kit stages are dynamically governed by the constitution]

---

## Portable Bootstrapping & Verification Quickstart

### Installation & Target Seeding
[bootstrap-speckit.sh and bootstrap-speckit.ps1 invocation examples]

### Governance Initialization
[/speckit-bootstrap --check and /speckit-constitution]

### Verification Checks
[bash -n, diff -r, and cmp -s verification commands]
```

---

## 2. Quantitative Constraints

| Constraint Key | Rule | Metric / Budget |
|---|---|---|
| `MAX_TOTAL_LINES` | Line count of `README.md` MUST be reduced by at least 25% from 137 lines | $\le 104$ lines |
| `CANONICAL_SECTIONS` | Exactly 4 `## ` canonical section headings matching standard titles | 4 sections |
| `FORBIDDEN_PATTERNS` | Generic template governance tables and boilerplate MUST NOT appear | 0 occurrences of `Core Principles` table (`\| Principle \|`), 0 occurrences of `### Optional Modules` |
| `LINK_VALIDITY` | Every relative link `[text](path)` in `README.md` MUST resolve to an existing local file or directory | 100% valid relative links |
| `VERIFICATION_COMMANDS` | Verification commands in Section 4 MUST exit with code 0 | 0 non-zero exit codes |

---

## 3. Section-by-Section Validation Rules

### Section 1: Project Overview & Architecture
- **Mandatory Link**: Must link to upstream GitHub Spec Kit (`https://github.com/github/spec-kit`).
- **Core Distinction**: Must explicitly outline what this repository uniquely adds over upstream Spec Kit (governance suite, multi-agent orchestration, dynamic verification, portable bootstrapper, roadmap management).
- **Dual Support**: Must mention parity across Google Antigravity (`.agents/`) and Claude Code (`.claude/`).

### Section 2: Co-Applied Governance Suite
- **Mandatory Links**:
  - [`.specify/memory/constitution.md`](.specify/memory/constitution.md)
  - [`.specify/memory/coding-standards.md`](.specify/memory/coding-standards.md)
  - [`.specify/memory/logging-standards.md`](.specify/memory/logging-standards.md)
- **Forbidden Content**:
  - Full Core Principles table (Principles I–VII).
  - Optional Modules list (`MODULE-A` through `MODULE-DOCS`, `TRACE`).

### Section 3: Spec Kit Skills & Subagent Orchestration Reference
- **Mandatory Subagent Coverage**:
  - `speckit-reasoner` (with link to `.agents/agents/` or `.claude/agents/`)
  - `speckit-executor` (with link to `.agents/agents/` or `.claude/agents/`)
- **Mandatory Custom Skills**:
  - `/speckit-orchestrate`
  - `/speckit-bootstrap`
  - `/speckit-roadmap`
- **Standard Pipeline Summary**:
  - Brief statement that standard Spec Kit stages (`specify`, `plan`, `tasks`, `implement`) are enhanced by dynamic constitutional governance.
  - No individual table rows for standard upstream skills.

### Section 4: Portable Bootstrapping & Verification Quickstart
- **Mandatory Scripts**:
  - `bootstrap-speckit.sh`
  - `bootstrap-speckit.ps1`
- **Mandatory Verification Commands**:
  - `bash -n bootstrap-speckit.sh`
  - `diff -r .agents .claude`
  - `cmp -s .specify/templates/constitution-template.md .specify/presets/base-governance/templates/constitution-template.md`
  - `cmp -s .specify/templates/coding-standards-template.md .specify/presets/base-governance/templates/coding-standards-template.md`
  - `cmp -s .specify/templates/logging-standards-template.md .specify/presets/base-governance/templates/logging-standards-template.md`
