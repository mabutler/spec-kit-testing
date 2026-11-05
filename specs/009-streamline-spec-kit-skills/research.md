# Research: Streamline Spec Kit Skills & Decouple Bloat

## Research Topic 1: Template Resolution Simplification
- **Finding**: In upstream Spec Kit, template resolution is handled at path `.specify/templates/`. Overrides can exist in `.specify/templates/overrides/`, presets in `.specify/presets/`, and extensions in `.specify/extensions/`.
- **Decision**: Rather than repeating a 10-line step-by-step algorithm in every skill prompt (`specify`, `plan`, `tasks`, `checklist`), replace it with a single concise directive:
  *"Resolve template from `.specify/templates/overrides/`, `.specify/presets/`, `.specify/extensions/`, or fallback to `.specify/templates/<template-name>.md`."*
- **Impact**: Cuts ~80-100 lines of redundant prose across 4 skills.

## Research Topic 2: Decoupling Documentation Gate to Constitution
- **Finding**: Commit `aaf54d7` added custom `Documentation Impact: USER_FACING vs INTERNAL_ONLY` branching instructions to `speckit-plan`, `speckit-tasks`, `speckit-analyze`, `speckit-implement`, and `speckit-converge`.
- **Decision**: Remove the custom documentation impact blocks from the skill instructions. The active constitution (`.specify/memory/constitution.md` Principle VII) already requires keeping human-facing documentation synchronized with code changes. All Spec Kit skills already state that the constitution is non-negotiable.
- **Impact**: Reduces skill coupling, eliminates false failures on internal refactors, and cuts ~60 lines of prompt text.

## Research Topic 3: Selective & Lazy Governance Context Loading
- **Finding**: Currently, `speckit-plan`, `speckit-tasks`, `speckit-analyze`, `speckit-implement`, and `speckit-orchestrate` all state: *"Load project governance suite: constitution.md, coding-standards.md, and logging-standards.md"*.
- **Decision**:
  - `speckit-specify` & `speckit-clarify`: Load only `.specify/memory/constitution.md`.
  - `speckit-plan` & `speckit-tasks`: Load `.specify/memory/constitution.md` and relevant sections of `.specify/memory/coding-standards.md` (architecture & language rules).
  - `speckit-implement`: Load `.specify/memory/coding-standards.md` and `.specify/memory/logging-standards.md` alongside `constitution.md`.
- **Impact**: Dramatically cuts context window usage during the early stages of feature development.

## Research Topic 4: Redundant Principle III Dynamic Extraction
- **Finding**: `speckit-tasks` and `speckit-orchestrate` carry large blocks explaining how to extract Principle III from `constitution.md` and format test directives. Upstream Spec Kit already states: *"Tests are OPTIONAL: Only generate test tasks if explicitly requested in the feature specification or if user requests TDD approach."*
- **Decision**: Simplify to defer directly to the active constitution without the verbose instruction blocks.
