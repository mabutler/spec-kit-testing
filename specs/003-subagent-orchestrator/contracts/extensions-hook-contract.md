# Contract: `.specify/extensions.yml` Hook Integration

**Artifact Target**: `.specify/extensions.yml`  
**Consumers**:
- `.agents/skills/speckit-specify/SKILL.md` (`Mandatory Post-Execution Hooks` → `hooks.after_specify`)
- `.agents/skills/speckit-orchestrate/SKILL.md` (Pre/Post-Execution Hooks and Anti-Recursion Guard)

---

## 1. `.specify/extensions.yml` Schema

The repository root `.specify/extensions.yml` file MUST be valid YAML parseable by standard YAML parsers (`python3 -c 'import yaml; yaml.safe_load(...)'`) and conform to Spec Kit's extension hook schema:

```yaml
schema_version: "1.0"

hooks:
  after_specify:
    - extension: "speckit-orchestrator"
      command: "speckit.orchestrate"
      description: "Coordinate context-isolated subagents across clarify, plan, tasks, analyze, implement, and converge"
      prompt: "Specification complete and validated. Run /speckit-orchestrate to launch the subagent-driven delivery pipeline (or /speckit-orchestrate --pause-before-implement to review plan and tasks before code changes)."
      enabled: true
      optional: true
```

---

## 2. Behavioral Rules

1. **Command Name Normalization**:
   - Per `.agents/skills/speckit-specify/SKILL.md` line 247, dots (`.`) in `command: "speckit.orchestrate"` are replaced with hyphens (`-`), yielding `/speckit-orchestrate`.
2. **Interactive Default (`optional: true`)**:
   - When a user runs `/speckit-specify` directly, `speckit-specify` finishes validating `spec.md` and `checklists/requirements.md`, then outputs the `## Extension Hooks` block prompting the user to run `/speckit-orchestrate`.
3. **Full Automatic Chaining (`optional: false`)**:
   - If a team or user changes `optional: true` to `optional: false` in `.specify/extensions.yml`, `speckit-specify` emits `EXECUTE_COMMAND: speckit-orchestrate` and automatically invokes `/speckit-orchestrate` immediately after `spec.md` validation passes.
4. **Anti-Recursion Invariant**:
   - When `/speckit-orchestrate` itself spawns a subagent to run `speckit-specify` (Stage 1), the subagent operates with `ORCHESTRATOR_CHILD=true` and MUST skip executing `hooks.after_specify` so `/speckit-orchestrate` is never recursively re-entered.
