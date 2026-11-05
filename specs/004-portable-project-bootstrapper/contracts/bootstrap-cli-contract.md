# CLI Contract: Ultra-Thin Terminal Seeders

**Feature**: `004-portable-project-bootstrapper`  
**Artifacts**: `bootstrap-speckit.sh` & `bootstrap-speckit.ps1`  
**Date**: 2026-11-05  

---

## 1. Overview & Purpose

The ultra-thin terminal seeders `bootstrap-speckit.sh` (Bash/POSIX) and `bootstrap-speckit.ps1` (PowerShell) provide a minimal, cross-platform mechanism to seed the `.specify/` and `.agents/` bundle from the source repository into any target repository directory `<target-repo>`.

Both scripts strictly enforce:
- Lightweight implementation (under 150 lines of code each).
- Zero external package dependencies (pure standard shell commands and PowerShell built-ins).
- Protected User-State immutability (never clobber `.specify/memory/**`, `.specify/templates/overrides/**`, `.specify/feature.json`, `specs/**`, or `.agents/agents/*.local.md`).

---

## 2. Command Line Invocation

### POSIX / Bash
```bash
./bootstrap-speckit.sh <target-repo> [--force] [--help|-h]
```

### PowerShell (Windows / Cross-platform)
```powershell
pwsh ./bootstrap-speckit.ps1 <target-repo> [-Force] [-Help]
# or in Windows PowerShell 5.1:
.\bootstrap-speckit.ps1 <target-repo> [-Force] [-Help]
```

---

## 3. Arguments & Flags

| Argument / Flag | Type | Required | Description |
|-----------------|------|----------|-------------|
| `<target-repo>` | Positional String | Yes (unless `--help`) | Path to the target project directory to seed. Relative or absolute. Created if it does not exist. |
| `--force` / `-Force` | Flag | No | Overwrite existing managed files in `<target-repo>`. (Protected User State remains untouched). |
| `--help` / `-Help` / `-h` | Flag | No | Display usage syntax and exit code 0. |

---

## 4. Exit Codes & Error Conditions

| Exit Code | Reason | Telemetry / Output Message |
|-----------|--------|----------------------------|
| `0` | Success | Structured summary output reporting files copied/skipped and next steps. |
| `1` | Missing `<target-repo>` argument | `ERROR: Target repository path is required. Run with --help for usage.` |
| `1` | Invalid Target (is a regular file) | `ERROR: Target path exists and is a file, not a directory: <path>` |
| `1` | Self-Targeting Attempt | `ERROR: Target repository cannot be the source toolkit repository itself.` |
| `1` | Missing Required Source Assets | `CRITICAL: Source bundle is missing required assets: <missing-list>` |
| `1` | Target Not Writable / Permission Denied | `ERROR: Target directory is not writable: <path>` |

---

## 5. Managed Asset Inventory

The seeder scripts copy the following exact paths from source to target:

```text
.specify/
├── templates/
│   ├── checklist-template.md
│   ├── coding-standards-template.md
│   ├── constitution-template.md
│   ├── logging-standards-template.md
│   ├── plan-template.md
│   ├── spec-template.md
│   └── tasks-template.md
├── presets/
│   ├── .registry
│   └── base-governance/
│       ├── preset.yml
│       └── templates/
│           ├── coding-standards-template.md
│           ├── constitution-template.md
│           └── logging-standards-template.md
├── extensions/
│   ├── .registry
│   └── speckit-orchestrator/
│       └── extension.yml
├── workflows/
│   ├── workflow-registry.json
│   └── speckit/
│       └── workflow.yml
├── integrations/
│   ├── speckit.manifest.json
│   ├── agy.manifest.json
│   └── speckit-bootstrap.manifest.json
├── extensions.yml
├── init-options.json
├── integration.json
└── .gitignore

.agents/
├── skills/
│   ├── speckit-specify/SKILL.md
│   ├── speckit-clarify/SKILL.md
│   ├── speckit-plan/SKILL.md
│   ├── speckit-tasks/SKILL.md
│   ├── speckit-checklist/SKILL.md
│   ├── speckit-analyze/SKILL.md
│   ├── speckit-implement/SKILL.md
│   ├── speckit-converge/SKILL.md
│   ├── speckit-constitution/SKILL.md
│   ├── speckit-orchestrate/SKILL.md
│   └── speckit-bootstrap/SKILL.md
└── agents/
    ├── speckit-reasoner.md
    └── speckit-executor.md
```

---

## 6. Git Ignore Maintenance

Both scripts verify `<target-repo>/.gitignore`:
- If `<target-repo>/.gitignore` does not exist, it is created.
- If `.agents/agents/*.local.md` is not present in `<target-repo>/.gitignore`, it is appended.

---

## 7. Output Format

Conforms to `.specify/memory/logging-standards.md`:
```text
=== Spec Kit Bootstrapper Seeder ===
Target Repository: /path/to/target
Mode: Normal (skipping existing managed files)

[INFO] Verified source bundle integrity
[INFO] Seeded .specify/ configuration and templates (18 files)
[INFO] Seeded .agents/ skills and agent definitions (13 files)
[INFO] Updated .gitignore with .agents/agents/*.local.md

Files Copied: 31
Files Skipped: 0 (existing)

Next Steps:
1. Open your AI agent in the target repository
2. Run /speckit-bootstrap to verify configuration and manifests
3. Run /speckit-constitution to ratify project governance standards
====================================
```
