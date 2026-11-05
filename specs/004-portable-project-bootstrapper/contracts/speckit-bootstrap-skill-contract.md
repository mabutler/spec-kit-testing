# Skill Contract: `/speckit-bootstrap`

**Feature**: `004-portable-project-bootstrapper`  
**Artifact**: `.agents/skills/speckit-bootstrap/SKILL.md`  
**Date**: 2026-11-05  

---

## 1. Overview & Capabilities

The `/speckit-bootstrap` skill provides agent-native lifecycle management for Spec Kit across repositories without executing shell scripts. It supports:
- Post-seed verification & readiness check.
- Non-destructive upgrade & drift detection against cryptographic SHA-256 manifests.
- Idempotent configuration merging (`.specify/extensions.yml`, `.gitignore`).
- Cleanup of obsolete legacy `.specify/scripts/`.
- Direct handoff into `/speckit-constitution` for immediate governance ratification.

---

## 2. Invocations & Arguments

```text
/speckit-bootstrap [<target-repo>] [--upgrade] [--check|--dry-run] [--force] [--init-governance] [--source=<source-repo>]
```

| Parameter / Flag | Type | Description |
|------------------|------|-------------|
| `<target-repo>` | Optional String | Path to target repository. If omitted, defaults to current working directory (`.`). |
| `--upgrade` | Flag | Performs upgrade against the source bundle, updating unmodified managed files. |
| `--check` or `--dry-run` | Flag | Read-only mode. Computes file classification plan without modifying disk. |
| `--force` | Flag | Overwrite drifted managed files (Protected User State remains untouched). |
| `--init-governance` | Flag | After bootstrap checks complete, invokes `/speckit-constitution` on target repo. |
| `--source=<source-repo>`| Option | Source toolkit directory when upgrading another repository from outside. |

---

## 3. Operational Modes & Execution Logic

### Mode A: Self-Check / Post-Seed Verification (Default)
Triggered when run in the active project directory without arguments:
1. **Asset Scan**: Scans current repository for all managed files defined in the asset inventory.
2. **Obsolete Script Detection**: Checks if `.specify/scripts/` exists; if found, safely deletes the directory and updates manifests.
3. **Configuration Merge**:
   - Ensures `speckit.orchestrate` hook is registered in `.specify/extensions.yml` under `hooks.after_specify`.
   - Ensures `.agents/agents/*.local.md` is present in `.gitignore`.
4. **Manifest Generation / Verification**:
   - Calculates SHA-256 for all managed files.
   - Writes or updates `.specify/integrations/speckit-bootstrap.manifest.json`.
   - Ensures `speckit.manifest.json` and `agy.manifest.json` are synchronized (with zero script entries).
5. **Governance State Check**:
   - Checks if `.specify/memory/{constitution,coding-standards,logging-standards}.md` exist.
   - If missing, prompts user with a recommendation to run `/speckit-constitution`.

### Mode B: Upgrade & Drift Detection (`--upgrade`)
Triggered when `--upgrade` is supplied:
1. Loads target manifest `.specify/integrations/speckit-bootstrap.manifest.json` (if present).
2. For each managed file in the source bundle:
   - Evaluates state according to the File Action Classification State Machine (`CREATE`, `UPGRADE`, `PRESERVE_USER_STATE`, `SKIP_DRIFTED`, `REMOVE_OBSOLETE`, `UNCHANGED`).
3. If `--check` or `--dry-run` is active:
   - Prints the classification table and terminates without modifying disk.
4. If executing mutations:
   - Writes `CREATE` files.
   - Updates `UPGRADE` files.
   - Skips `SKIP_DRIFTED` files and emits `WARN` diagnostics.
   - Deletes `REMOVE_OBSOLETE` files.
   - Updates target manifest with new SHA-256 checksums and timestamp.

### Mode C: Governance Initialization (`--init-governance`)
Triggered when `--init-governance` is passed or confirmed:
1. Executes verification steps above.
2. Invokes `.agents/skills/speckit-constitution/SKILL.md` (or dispatches a subagent) to interactively or deterministically ratify project constitution and companion standards.

---

## 4. Protected User-State Rule

The skill strictly prohibits modifying:
- `.specify/memory/constitution.md`
- `.specify/memory/coding-standards.md`
- `.specify/memory/logging-standards.md`
- `.specify/templates/overrides/**`
- `.specify/feature.json` and `specs/**`
- `.agents/agents/*.local.md` and custom non-canonical agent profiles
- Custom skills in `.agents/skills/`

---

## 5. Output Report Format

```markdown
### Spec Kit Bootstrap Report

**Target Repository**: `/path/to/repo`  
**Execution Mode**: `Upgrade`  
**Source Bundle Version**: `1.4.0`  

#### Execution Summary
- **Created**: 2 files
- **Upgraded**: 14 files
- **Unchanged**: 15 files
- **Preserved (User State)**: 3 files
- **Skipped (Local Drift)**: 1 file (`.specify/templates/plan-template.md`)
- **Obsolete Removed**: 6 files (`.specify/scripts/bash/*`)

#### Diagnostics & Warnings
> [!WARNING]
> `.specify/templates/plan-template.md` has local modifications differing from both manifest digest and upstream source. Skipped to prevent overwriting local changes. Use `--force` to overwrite.

#### Handoff & Recommended Next Steps
- Governance Suite: Ratified (constitution.md, coding-standards.md, logging-standards.md)
- Next Recommended Command: `/speckit-specify <feature-description>`
```
