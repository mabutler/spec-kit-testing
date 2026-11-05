# Data Model: Portable Project Bootstrapper

**Feature**: `004-portable-project-bootstrapper`  
**Date**: 2026-11-05  
**Status**: Completed  

---

## Conceptual Architecture

The Portable Project Bootstrapper feature models the state, package hierarchy, lifecycle events, and boundaries required to distribute, seed, upgrade, and verify Spec Kit across repositories without runtime script dependencies.

```
+-----------------------------------------------------------------------------------+
|                              Source Toolkit Bundle                                |
|  - Managed Templates (.specify/templates/)                                        |
|  - Managed Presets (.specify/presets/base-governance/)                            |
|  - Managed Extensions (.specify/extensions/speckit-orchestrator/)                 |
|  - Managed Skills (.agents/skills/speckit-*/SKILL.md)                             |
|  - Managed Agent Roles (.agents/agents/speckit-{reasoner,executor}.md)            |
|  - Metadata & Registries (init-options.json, integration.json, *.manifest.json)   |
+-----------------------------------------------------------------------------------+
                                   |
         +-------------------------+-------------------------+
         |                                                   |
         v                                                   v
[bootstrap-speckit.sh / .ps1]                    [/speckit-bootstrap Skill]
(Terminal Seeder - Ultra-Thin Copy)             (Agent Lifecycle, Drift, Upgrades)
         |                                                   |
         +-------------------------+-------------------------+
                                   v
+-----------------------------------------------------------------------------------+
|                               Target Repository                                   |
|  +---------------------------------+  +----------------------------------------+  |
|  |     Managed Assets (Syncable)   |  |     Protected User State (Immutable)   |  |
|  |  - Presets & Extensions         |  |  - .specify/memory/*.md (Ratified)     |  |
|  |  - Managed Skills & Core Tmpls  |  |  - .specify/templates/overrides/**     |  |
|  |  - Role Profiles (Base)         |  |  - .specify/feature.json & specs/**    |  |
|  |  - Manifests & Registries       |  |  - .agents/agents/*.local.md overrides |  |
|  +---------------------------------+  +----------------------------------------+  |
+-----------------------------------------------------------------------------------+
```

---

## Core Entities & Schemas

### 1. Feature State & Execution Context

Models the active feature tracking context read natively by all Spec Kit skills.

- **Entity**: `FeatureContext`
- **Location**: `.specify/feature.json` or environment variable `SPECIFY_FEATURE_DIRECTORY`
- **Fields**:
  - `feature_directory` (string, required): Repository-relative path to active feature folder (e.g. `"specs/004-portable-project-bootstrapper"`).
  - `feature_number` (string, optional): 3-digit feature index (e.g. `"004"`).
  - `feature_name` (string, optional): Feature slug (e.g. `"portable-project-bootstrapper"`).
- **Derived Properties**:
  - `REPO_ROOT` (string): Absolute path to repository root containing `.specify/`.
  - `FEATURE_DIR` (string): Absolute path `${REPO_ROOT}/${feature_directory}`.
  - `BRANCH` (string): Feature slug or folder name (e.g. `"004-portable-project-bootstrapper"`).
- **Validation Rules**:
  - `feature_directory` MUST NOT be empty.
  - Directory `${FEATURE_DIR}` MUST exist for downstream skills (`clarify`, `plan`, `tasks`, etc.).

---

### 2. Four-Tier Template Hierarchy

Models the layered template discovery and composition mechanism used by agent skills.

- **Entity**: `TemplateHierarchy`
- **Tiers (evaluated in descending order of precedence)**:
  1. **Tier 1 (Override)**: `.specify/templates/overrides/<template-name>.md`
     - Strategy: Always `replace`. If exists, completely overrides all lower tiers.
  2. **Tier 2 (Presets)**: `.specify/presets/<preset-id>/templates/<template-name>.md`
     - Evaluated according to `.specify/presets/.registry`.
     - Presets sorted ascending by `priority` integer (default: 10).
     - Strategy declared in `preset.yml`: `replace`, `prepend`, `append`, or `wrap`.
  3. **Tier 3 (Extensions)**: `.specify/extensions/<ext-id>/templates/<template-name>.md`
     - Evaluated according to `.specify/extensions/.registry`.
     - Extensions sorted ascending by `priority` integer (default: 10).
  4. **Tier 4 (Core Fallback)**: `.specify/templates/<template-name>.md`
     - Canonical baseline template shipped with Spec Kit.
- **Validation Rules**:
  - If a requested template is not found in any of the 4 tiers, the agent MUST fail closed and emit an error per Principle II.

---

### 3. Preset Package & Registry

Models a packaged preset providing templates, commands, or hooks.

- **Entity**: `PresetPackage`
- **Manifest File**: `.specify/presets/<preset-id>/preset.yml`
- **Fields**:
  - `name` (string, required): Kebab-case identifier matching `<preset-id>` (e.g. `"base-governance"`).
  - `version` (string, required): Semantic version string (e.g. `"1.0.0"`).
  - `description` (string, required): Purpose summary.
  - `provides` (object, required):
    - `templates` (array of objects):
      - `type` (string, enum: `["template", "command", "script"]`): Type of asset.
      - `name` (string, required): Target template identifier (e.g. `"constitution-template"`).
      - `file` (string, required): Relative path inside preset folder (e.g. `"templates/constitution-template.md"`).
      - `strategy` (string, enum: `["replace", "prepend", "append", "wrap"]`, default: `"replace"`).
- **Registry File**: `.specify/presets/.registry`
  - Mapping of preset IDs to metadata:
    ```json
    {
      "presets": {
        "<preset-id>": {
          "priority": 10,
          "enabled": true
        }
      }
    }
    ```

---

### 4. Extension Package & Registry

Models a packaged extension providing hooks and workflow extensions.

- **Entity**: `ExtensionPackage`
- **Manifest File**: `.specify/extensions/<ext-id>/extension.yml`
- **Fields**:
  - `name` (string, required): Kebab-case identifier (e.g. `"speckit-orchestrator"`).
  - `version` (string, required): Semantic version string (e.g. `"1.0.0"`).
  - `description` (string, required): Purpose summary.
  - `hooks` (object, optional):
    - `<hook_point>` (array of hook objects):
      - `extension` (string): Extension identifier.
      - `command` (string): Execution command (e.g. `"speckit.orchestrate"`).
      - `description` (string): Human-readable purpose.
      - `prompt` (string, optional): Prompt displayed to user/agent.
      - `enabled` (boolean, default: true).
      - `optional` (boolean, default: false).
- **Registry File**: `.specify/extensions/.registry`
  - Mapping of extension IDs to metadata:
    ```json
    {
      "extensions": {
        "<ext-id>": {
          "priority": 10,
          "enabled": true
        }
      }
    }
    ```
- **Unified Extension Hook Config**: `.specify/extensions.yml`
  - Merged active hook definitions across all installed extensions.

---

### 5. Installation Manifest & Asset Inventory

Models the cryptographic inventory tracking every managed file for non-destructive upgrades and drift inspection.

- **Entity**: `BootstrapManifest`
- **Location**: `.specify/integrations/speckit-bootstrap.manifest.json`
- **Fields**:
  - `manifest_version` (string): `"1.0"`.
  - `bundle_version` (string): Version of the Spec Kit suite (e.g. `"1.4.0"`).
  - `generated_at` (string, ISO 8601 UTC timestamp).
  - `source_commit` (string, optional): Source git commit or identifier.
  - `files` (map of relative file path string to object):
    - `digest` (string): `"sha256:<64-char-hex>"`.
    - `size_bytes` (integer): File size in bytes.
    - `tier` (string, enum: `["core", "preset", "extension", "skill", "agent", "metadata"]`).

---

### 6. File Action Classification & Upgrade State Machine

During `/speckit-bootstrap --check` or `/speckit-bootstrap --upgrade`, each candidate file is evaluated and assigned exactly one lifecycle action.

```
                             [Candidate File in Target]
                                         |
                       +-----------------+-----------------+
                       |                                   |
                (File Does Not Exist)               (File Exists)
                       |                                   |
                       v                                   v
                   [ CREATE ]                    (Is Path in Protected
                                                  User-State Allowlist?)
                                                  /                    \
                                               (Yes)                   (No)
                                                /                        \
                                               v                          v
                                    [ PRESERVE_USER_STATE ]      (Compare Disk SHA-256
                                                                  with Manifest Digest)
                                                                  /                   \
                                                             (Matches)             (Differs)
                                                                /                     \
                                                               v                       v
                                                      (Compare Target vs Source)  [ SKIP_DRIFTED ]
                                                      /                        \  (Warn; skip unless
                                                  (Identical)              (Differs)  --force)
                                                     /                          \
                                                    v                            v
                                              [ UNCHANGED ]                [ UPGRADE ]
```

#### Action Definitions:
- **`CREATE`**: Target file does not exist; copy from source bundle.
- **`PRESERVE_USER_STATE`**: File belongs to the Protected User-State Allowlist; never overwrite or delete under any circumstances.
- **`UPGRADE`**: Target file exists and its content matches the recorded manifest digest (unmodified by user), but source bundle has a newer version; overwrite with upstream file.
- **`SKIP_DRIFTED`**: Target file exists and differs from both the recorded manifest digest and upstream source (locally modified); skip and warn unless `--force` is passed.
- **`REMOVE_OBSOLETE`**: File is recorded in manifest but no longer exists in upstream source bundle (e.g. legacy `.specify/scripts/bash/*.sh`); delete file and remove entry from manifest.
- **`UNCHANGED`**: Target file is identical to source bundle; no action required.

---

### 7. Protected User-State Allowlist

The immutable list of repository paths protected from clobbering:

| Path Pattern | Description | Rationale |
|--------------|-------------|-----------|
| `.specify/memory/constitution.md` | Ratified project constitution | Contains project-specific legal/engineering rules |
| `.specify/memory/coding-standards.md` | Ratified project coding standards | Contains project-specific language and tool rules |
| `.specify/memory/logging-standards.md` | Ratified project logging standards | Contains project-specific observability conventions |
| `.specify/templates/overrides/**` | Project template overrides (Tier 1) | User intentionally overrode template defaults |
| `.specify/feature.json` | Current feature tracking state | Active local branch and feature directory pointer |
| `specs/**` | Active and historical feature specifications | Feature-driven development artifacts |
| `.agents/agents/*.local.md` | Machine-local agent overrides | Environment-specific agent model/temperature overrides |
| `.agents/agents/speckit-<custom>.md` | Custom stage agents outside base roles | User-defined specialized agent personas |
| Non-speckit skills in `.agents/skills/` | Project custom skills | Domain-specific agent skills |
