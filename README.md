# Spec Kit Customizations

Extensions for [GitHub Spec Kit](https://github.com/github/spec-kit) providing a project constitution, companion standards, multi-agent orchestration, and portable bootstrapping scripts.

---

## Project Overview & Architecture

Spec Kit formalizes software development through specification-driven workflows. This repository extends upstream [GitHub Spec Kit](https://github.com/github/spec-kit) with multi-agent orchestration, dynamic constitutional governance, and portable installation scripts, maintained with 100% byte parity across Google Antigravity ([`.agents/`](.agents/)) and Claude Code ([`.claude/`](.claude/)).

Key additions in this repository:
1. **Multi-Agent Pipeline Orchestration**: Subagent coordination (`/speckit-orchestrate`) with dedicated reasoning and execution personas.
2. **Roadmap Management**: Project-level milestone tracking through `/speckit-roadmap` and [`ROADMAP.md`](ROADMAP.md).
3. **Co-Applied Governance Suite**: Reusable base templates and active governance (`constitution.md`, `coding-standards.md`, `logging-standards.md`) packaged as the `base-governance` preset.
4. **Portable Bootstrapping**: Installer scripts (`bootstrap-speckit.sh`, `bootstrap-speckit.ps1`) and manifest verification (`/speckit-bootstrap`) to seed these extensions into any repository.

---

## Co-Applied Governance Suite

Project governance is centralized in `.specify/memory/` and operationalized by AI subagents at every lifecycle stage:

- [`.specify/memory/constitution.md`](.specify/memory/constitution.md): Core architectural principles (I–VII) defining evidence-based requirements, fail-closed state, static verification, single-ownership boundaries, toolchain security, resource ceilings, and documentation synchronization.
- [`.specify/memory/coding-standards.md`](.specify/memory/coding-standards.md): Language conventions, error-handling patterns, static quality gates, and canonical README structure.
- [`.specify/memory/logging-standards.md`](.specify/memory/logging-standards.md): Structured telemetry schemas, log severity hierarchies, and credential redaction rules.

---

## Spec Kit Skills & Subagent Orchestration Reference

### Subagent Personas

The multi-agent workflow coordinates context-isolated personas across [`.agents/agents/`](.agents/agents/) and [`.claude/agents/`](.claude/agents/):
- **`speckit-reasoner`**: Focuses on architecture planning, requirements clarification, consistency analysis, and post-implementation convergence checks (`clarify`, `plan`, `analyze`, `converge`).
- **`speckit-executor`**: Focuses on concise specification synthesis, actionable task decomposition, and code implementation (`specify`, `tasks`, `implement`).

### Custom Skills

- **`/speckit-orchestrate`**: Coordinates subagents sequentially through clarify, plan, tasks, analyze, implement, and converge with human approval gates.
- **`/speckit-roadmap`**: Authors, visualizes, audits, and syncs strategic feature milestones in [`ROADMAP.md`](ROADMAP.md) directly into feature specifications.
- **`/speckit-bootstrap`**: Verifies SHA-256 manifest integrity, detects configuration drift, and applies non-destructive template upgrades.

---

## Portable Bootstrapping & Verification Quickstart

### Installation & Target Seeding

Install managed templates, presets, and agent skills into any target Git repository:

```bash
# Linux / macOS
./bootstrap-speckit.sh /path/to/target-repo [--force]
```
```powershell
# Windows (PowerShell)
pwsh ./bootstrap-speckit.ps1 -TargetRepo "C:\path\to\target-repo" [-Force]
```

### Governance Initialization

1. Verify installed file integrity: `/speckit-bootstrap --check`
2. Initialize or tune the project constitution: `/speckit-constitution`

### Verification Checks

Validate script syntax, cross-client parity, and template consistency:

```bash
bash -n bootstrap-speckit.sh
diff -r .agents .claude
cmp -s .specify/templates/constitution-template.md .specify/presets/base-governance/templates/constitution-template.md
cmp -s .specify/templates/coding-standards-template.md .specify/presets/base-governance/templates/coding-standards-template.md
cmp -s .specify/templates/logging-standards-template.md .specify/presets/base-governance/templates/logging-standards-template.md
```
