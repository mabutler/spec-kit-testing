# Research: Portable Project Bootstrapper

**Feature**: `004-portable-project-bootstrapper`  
**Date**: 2026-11-05  
**Status**: Completed  

---

## Executive Summary

Phase 4 completes the evolution of Spec Kit into a truly portable, zero-external-dependency, multi-agent engineering suite. Prior phases established a constitutional governance framework (Phase 1), custom template extensions (Phase 2), and context-isolated subagent orchestration (Phase 3). However, workflow skills (`speckit-*` in `.agents/skills/`) still invoked `.specify/scripts/bash/*.sh` subshells for feature path discovery and 4-tier template resolution, creating runtime shell dependencies and making repository adoption cumbersome.

This research resolves all technical unknowns for:
1. Converting all 10 existing Spec Kit skills plus the new bootstrapper skill into 100% script-free workflows using agent-native file operations.
2. Developing paired, ultra-thin terminal seeder scripts (`bootstrap-speckit.sh` and `bootstrap-speckit.ps1`) under 150 lines each with zero external dependencies.
3. Designing an intelligent agent skill (`speckit-bootstrap`) that handles rich drift inspection, manifest-gated non-destructive upgrades, configuration merging, and governance initialization.
4. Packaging base governance templates and orchestrator extensions as first-class Spec Kit presets and extensions.
5. Guaranteeing full compliance with Constitutional Principle III (*Static Verification & No Automated Tests*).

---

## Research Topics & Decisions

### Topic 1: 100% Agent-Native Script-Free Skill Refactoring & 4-Tier Resolution Protocol

#### Problem Statement
Skills currently execute `.specify/scripts/bash/check-prerequisites.sh`, `setup-plan.sh`, `setup-tasks.sh`, and `resolve-template.sh` in subshells. Removing `.specify/scripts/bash/` requires defining deterministic agent-native procedures for:
- Discovering feature root and branch context.
- Verifying artifact prerequisites per workflow stage.
- Resolving templates across the 4-tier inheritance stack:
  1. Priority 1: `.specify/templates/overrides/<template-name>.md`
  2. Priority 2: `.specify/presets/<preset-id>/templates/<template-name>.md` (ordered by priority in `.specify/presets/.registry`, respecting composition strategies: `replace`, `prepend`, `append`, `wrap`)
  3. Priority 3: `.specify/extensions/<ext-id>/templates/<template-name>.md` (ordered by priority in `.specify/extensions/.registry`)
  4. Priority 4: `.specify/templates/<template-name>.md` (core fallback)

#### Decision
- **Feature Discovery**: The agent directly reads `.specify/feature.json` using native `read_file` or filesystem check. If the environment variable `SPECIFY_FEATURE_DIRECTORY` is passed in user prompt or ambient context, that path is preferred; otherwise the `feature_directory` key in `.specify/feature.json` is used. The branch name is derived from the feature directory basename (e.g., `specs/004-portable-project-bootstrapper` → `004-portable-project-bootstrapper`).
- **Prerequisite Checking**: The agent checks the existence of required files (`spec.md`, `plan.md`, `tasks.md`, `research.md`, etc.) directly via native file reading. If missing, it emits a structured `WARN` rejection or `CRITICAL` defect message and halts per Principle II.
- **4-Tier Template Resolution**:
  - The agent inspects `.specify/templates/overrides/<template-name>.md`. If present, it replaces all lower tiers.
  - If not overridden, it checks `.specify/presets/.registry` (JSON mapping preset names to `{priority, enabled}`). For enabled presets in order of ascending priority number, it checks `preset.yml` to find declared templates and their composition strategy (`replace`, `prepend`, `append`, or `wrap`). If a preset provides the template, it applies the strategy relative to the lower tiers.
  - Next, it checks `.specify/extensions/.registry` for extension-provided templates.
  - Finally, it falls back to `.specify/templates/<template-name>.md`.
  - For `replace`, the higher-tier content replaces lower tiers. For `prepend`/`append`, content is prepended/appended with a newline separator. For `wrap`, higher-tier wraps the lower-tier content around placeholder markers.
- **Decommissioning `.specify/scripts/`**: The entire `.specify/scripts/` directory is deleted from git tracking and disk. Pre-PR verification in `.specify/memory/constitution.md` is updated to replace `resolve-template.sh` checks with direct static verification.

#### Rationale
- Native tool calls (`read_file`, `write_file`) are deterministic, cross-platform, inspectable, and eliminate platform variances between Linux, macOS, and Windows.
- Completely decouples Spec Kit workflows from host-level bash/powershell utilities during agent execution.

#### Alternatives Considered
- *Retaining bash scripts as fallback*: Rejected because maintaining dual paths doubles maintenance burden and violates SC-001 (0 script references in skills).
- *Calling python scripts for template resolution*: Rejected because it introduces external Python runtime dependencies, violating Principle V (*Centralized Dependencies & Protected Toolchain Gate*).

---

### Topic 2: Ultra-Thin Terminal Seeder Scripts (`bootstrap-speckit.sh` & `bootstrap-speckit.ps1`)

#### Problem Statement
Users in fresh repositories need an instant, friction-free way to copy Spec Kit files from the source toolkit into `<target-repo>` without installing npm/pip/cargo packages or running complex installers.

#### Decision
- Provide two single-file seeders at the repo root:
  - `bootstrap-speckit.sh` for POSIX/Bash (macOS, Linux, WSL, Git Bash).
  - `bootstrap-speckit.ps1` for PowerShell (Windows PowerShell 5.1 and PowerShell 7+ on any OS).
- Both scripts are strictly constrained:
  - Under 150 lines of code.
  - Zero external package dependencies (pure POSIX shell utilities `cp`, `mkdir`, `test`; pure PowerShell `Copy-Item`, `Test-Path`).
  - Accept `<target-repo>` as positional argument 1.
  - Flags: `--force` / `-Force`, `--help` / `-Help`.
  - Perform fail-closed input validation: target directory must be writable, cannot be a file, and cannot be the source repo root itself.
  - Copy managed assets:
    - `.specify/templates/*.md`
    - `.specify/presets/**`
    - `.specify/extensions/**`
    - `.specify/extensions.yml`
    - `.specify/init-options.json`
    - `.specify/integration.json`
    - `.specify/integrations/*.manifest.json`
    - `.specify/workflows/**`
    - `.specify/.gitignore`
    - `.agents/skills/speckit-*/SKILL.md` (all 11 skills)
    - `.agents/agents/speckit-reasoner.md` and `speckit-executor.md`
  - Enforce Protected User-State: Never overwrite `.specify/memory/**`, `.specify/templates/overrides/**`, `.specify/feature.json`, `specs/**`, or `.agents/agents/*.local.md`, even if `--force` / `-Force` is passed.
  - Skip existing managed files unless `--force` / `-Force` is passed.
  - Ensure `.agents/agents/*.local.md` is present in `<target-repo>/.gitignore`.
  - Conclude with a clean CLI summary and prompt to run `/speckit-bootstrap` inside the agent.

#### Rationale
- Keeps terminal scripting minimal, portable, and bug-resistant across operating systems.
- Moves all complex drift detection, YAML merging, and constitutional negotiation to the agent skill where intelligent context handling belongs.

#### Alternatives Considered
- *Single unified Python bootstrapper CLI*: Rejected because developers in Go, Rust, C#, or Java projects may not have Python installed.
- *Bundled archive unpacker (tar.gz / zip)*: Rejected per clarification session (no archive builder needed; direct file copy is simpler, faster, and transparent).

---

### Topic 3: Agent-Native Bootstrapper Lifecycle & Drift Detection (`speckit-bootstrap`)

#### Problem Statement
Repositories that have already adopted Spec Kit will receive updates over time. Maintainers need non-destructive upgrades that preserve project customizations while pulling upstream skill improvements and template updates.

#### Decision
- Create `.agents/skills/speckit-bootstrap/SKILL.md` supporting 4 modes:
  1. **Self-Check / Post-Seed Verification Mode** (`/speckit-bootstrap` with no args):
     - Validates all managed `.specify/` and `.agents/` files exist in the current repo.
     - Ensures `.agents/agents/*.local.md` is ignored in `.gitignore`.
     - Idempotently merges `speckit.orchestrate` into `.specify/extensions.yml`.
     - Detects and removes any legacy `.specify/scripts/` directory.
     - Computes SHA-256 digests of managed files and records them in `.specify/integrations/speckit-bootstrap.manifest.json`.
     - Checks if `.specify/memory/{constitution,coding-standards,logging-standards}.md` exist; if not, prompts user to run `/speckit-constitution`.
  2. **Cross-Repo Install / Upgrade Mode** (`/speckit-bootstrap <target-repo> [--upgrade] [--source=<source-repo>] [--force]`):
     - Evaluates target files against source bundle.
     - If file does not exist in target: `CREATE`.
     - If file exists in target and is protected user state: `PRESERVE_USER_STATE`.
     - If file exists in target and its SHA-256 matches manifest recorded digest: `UPGRADE` (cleanly replace with newer upstream version).
     - If file exists in target and its SHA-256 differs from manifest recorded digest: `SKIP_DRIFTED` (local modifications detected; skip unless `--force`).
     - If file in manifest is no longer present in source bundle (e.g. legacy scripts): `REMOVE_OBSOLETE`.
     - If target file is identical to source file: `UNCHANGED`.
     - Executes file operations according to classification, updates target manifest with new digests, and prints execution summary.
  3. **Dry-Run / Drift Inspection Mode** (`--check` or `--dry-run`):
     - Calculates the classification table without performing any disk writes or deletions.
  4. **Governance Initialization Mode** (`--init-governance`):
     - Completes bootstrap verification and chains directly into `/speckit-constitution` to ratify project constitution and companion standards.

#### Rationale
- Gives maintainers full visibility and control over upgrades.
- Cryptographic SHA-256 hashing prevents silent clobbering of local edits while enabling automatic upgrades for untouched managed files.

#### Alternatives Considered
- *Git-patch/diff merge*: Unreliable in non-git directories or across distinct repositories.
- *Blind file overwrite*: Violates Constitutional Principle VI (*Verify Before Mutate/Destroy*).

---

### Topic 4: First-Class Preset and Extension Packaging Standards

#### Problem Statement
Spec Kit's native 4-tier template resolution architecture supports Presets (`.specify/presets/`) and Extensions (`.specify/extensions/`). Phase 1 governance templates and Phase 3 subagent orchestration must be packaged cleanly into these standards.

#### Decision
- **Base Governance Preset**:
  - Location: `.specify/presets/base-governance/`
  - Manifest: `preset.yml` containing:
    ```yaml
    name: "base-governance"
    version: "1.0.0"
    description: "Core constitutional governance and engineering standards preset"
    provides:
      templates:
        - type: "template"
          name: "constitution-template"
          file: "templates/constitution-template.md"
          strategy: "replace"
        - type: "template"
          name: "coding-standards-template"
          file: "templates/coding-standards-template.md"
          strategy: "replace"
        - type: "template"
          name: "logging-standards-template"
          file: "templates/logging-standards-template.md"
          strategy: "replace"
    ```
  - Registry: `.specify/presets/.registry` containing:
    ```json
    {
      "presets": {
        "base-governance": {
          "priority": 10,
          "enabled": true
        }
      }
    }
    ```
  - Core Template Mirroring: `.specify/templates/` retains baseline copies of these three templates as the tier-4 fallback, ensuring resolution works seamlessly whether presets are active or stripped down.
- **Subagent Orchestrator Extension**:
  - Location: `.specify/extensions/speckit-orchestrator/`
  - Manifest: `extension.yml` containing:
    ```yaml
    name: "speckit-orchestrator"
    version: "1.0.0"
    description: "Multi-agent subagent pipeline orchestrator with role specialization"
    hooks:
      after_specify:
        - extension: "speckit-orchestrator"
          command: "speckit.orchestrate"
          description: "Coordinate context-isolated subagents across clarify, plan, tasks, analyze, implement, and converge"
          enabled: true
          optional: true
    ```
  - Registry: `.specify/extensions/.registry` containing:
    ```json
    {
      "extensions": {
        "speckit-orchestrator": {
          "priority": 10,
          "enabled": true
        }
      }
    }
    ```
  - Hook Registration: Idempotently registered in `.specify/extensions.yml`.

#### Rationale
- Standardizes governance and orchestration components as modular, distributable packages conforming to the official Spec Kit specification architecture.

---

### Topic 5: Protected User-State Allowlist Enforcement

#### Problem Statement
Upgrading a repository must never overwrite project-specific customizations, active work, or ratified constitutional documents.

#### Decision
Define an immutable Protected User-State Allowlist enforced by both the shell seeders and the agent skill:
1. `.specify/memory/constitution.md`, `.specify/memory/coding-standards.md`, `.specify/memory/logging-standards.md`
2. `.specify/templates/overrides/**`
3. `.specify/feature.json` and `specs/**`
4. `.agents/agents/*.local.md` and custom stage agent overrides
5. Non-speckit skills in `.agents/skills/`

Any attempt to overwrite these paths during seeding or upgrade is blocked and classified as `PRESERVE_USER_STATE`.

---

### Topic 6: Constitutional Principle III Adherence (Static Verification, Zero Automated Tests)

#### Problem Statement
Principle III (*Static Verification & No Automated Tests*) explicitly forbids creating unit tests, test harnesses, or test tasks.

#### Decision
- No `tests/` directories, test scripts, or unit tests will be created.
- Verification is performed through:
  - Static shell syntax verification (`bash -n bootstrap-speckit.sh`).
  - Static JSON/YAML validation for manifests and registry configurations.
  - Markdown structure and link verification across all skills.
  - Interactive validation via `--check` / `--dry-run` and live verification runs documented in `quickstart.md`.

---

## Technical Feasibility & Compatibility Matrix

| Environment | Supported Shell / Tool | Verification Strategy |
|-------------|------------------------|-----------------------|
| Linux (Ubuntu, Debian, Fedora, Arch) | Bash 4.0+ / POSIX `sh` | `bash -n bootstrap-speckit.sh` + live test |
| macOS (Darwin) | Bash 3.2+ / zsh / POSIX `sh` | Strict POSIX syntax compliance in `.sh` |
| Windows (Native) | PowerShell 5.1 / 7+ | `bootstrap-speckit.ps1` via `pwsh` |
| AI Agent Context | Native tool operations (`read_file`, `write_file`) | Direct file operations, zero subprocess calls |

All technical unknowns are fully resolved. Proceeding to Phase 1 Design.
