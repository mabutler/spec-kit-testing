# Quickstart & Static Validation Guide: Claude Discovery Compatibility & Constitutional Test Decoupling

**Feature Branch**: `007-claude-discovery-governance-decoupling`  
**Date**: 2026-11-05  
**Spec**: [`spec.md`](spec.md) | **Data Model**: [`data-model.md`](data-model.md)

## Overview

This guide provides runnable static verification checks that validate all requirements of Feature `007-claude-discovery-governance-decoupling` end-to-end without generating automated test files (in strict compliance with this repository's `.specify/memory/constitution.md` Principle III).

---

## 1. Verify Dual-Client Asset Existence & Byte-Identical Parity (`SC-001`, `FR-001`)

Confirm that all 12 skills and 2 subagent profiles exist in both `.agents/` and `.claude/` with identical content:

```bash
python3 -c '
import filecmp, os, sys

expected = [
    "agents/speckit-executor.md",
    "agents/speckit-reasoner.md",
    "skills/speckit-analyze/SKILL.md",
    "skills/speckit-bootstrap/SKILL.md",
    "skills/speckit-checklist/SKILL.md",
    "skills/speckit-clarify/SKILL.md",
    "skills/speckit-constitution/SKILL.md",
    "skills/speckit-converge/SKILL.md",
    "skills/speckit-implement/SKILL.md",
    "skills/speckit-orchestrate/SKILL.md",
    "skills/speckit-plan/SKILL.md",
    "skills/speckit-roadmap/SKILL.md",
    "skills/speckit-specify/SKILL.md",
    "skills/speckit-tasks/SKILL.md",
]

for rel in expected:
    a = os.path.join(".agents", rel)
    c = os.path.join(".claude", rel)
    if not os.path.isfile(a):
        sys.exit(f"Missing Antigravity asset: {a}")
    if not os.path.isfile(c):
        sys.exit(f"Missing Claude Code asset: {c}")
    if not filecmp.cmp(a, c, shallow=False):
        sys.exit(f"Parity mismatch between {a} and {c}")

print(f"PASS: All {len(expected)} canonical assets exist and match byte-for-byte across .agents/ and .claude/.")
'
```

---

## 2. Verify Dynamic Constitutional Deference & Zero Hardcoded Test Prohibitions (`SC-003`, `FR-006`, `FR-007`, `FR-008`)

Confirm that zero hardcoded test prohibitions remain in reusable subagent profiles, orchestrator dispatch templates, or roadmap skills:

```bash
# Must return 0 matches across .agents/ and .claude/
! grep -rn -iE "zero automated test|do not generate unit tests|automated test generation is disabled" .agents/ .claude/
echo "PASS: Zero hardcoded test prohibitions in .agents/ and .claude/."
```

---

## 3. Verify Bootstrapper Syntax, Line Ceilings & Target Seeding (`SC-002`, `FR-002`, `FR-003`)

Validate shell syntax, `< 150 LOC` constraints, and end-to-end seeding into a temporary directory:

```bash
# 1. Syntax & line ceiling check
bash -n bootstrap-speckit.sh
awk 'END { if (NR >= 150) { print "FAIL: bootstrap-speckit.sh >= 150 lines (" NR ")"; exit 1 } else { print "PASS: bootstrap-speckit.sh lines = " NR } }' bootstrap-speckit.sh
awk 'END { if (NR >= 150) { print "FAIL: bootstrap-speckit.ps1 >= 150 lines (" NR ")"; exit 1 } else { print "PASS: bootstrap-speckit.ps1 lines = " NR } }' bootstrap-speckit.ps1

# 2. Ephemeral target directory seeding check (cleaned up immediately)
TMP_TARGET="$(mktemp -d)"
trap 'rm -rf "$TMP_TARGET"' EXIT
./bootstrap-speckit.sh "$TMP_TARGET"

test -f "$TMP_TARGET/.agents/agents/speckit-reasoner.md"
test -f "$TMP_TARGET/.claude/agents/speckit-reasoner.md"
test -f "$TMP_TARGET/.claude/skills/speckit-orchestrate/SKILL.md"
grep -qF ".agents/agents/*.local.md" "$TMP_TARGET/.gitignore"
grep -qF ".claude/agents/*.local.md" "$TMP_TARGET/.gitignore"
echo "PASS: Bootstrapper seeded .specify/, .agents/, .claude/, and dual .gitignore patterns."
```

---

## 4. Verify Cryptographic SHA-256 Manifests (`SC-004`, `FR-004`, `FR-010`)

Validate all four integration manifests in `.specify/integrations/`:

```bash
python3 -c '
import hashlib, json, sys

manifests = [
    ".specify/integrations/speckit.manifest.json",
    ".specify/integrations/agy.manifest.json",
    ".specify/integrations/claude.manifest.json",
    ".specify/integrations/speckit-bootstrap.manifest.json",
]

for p in manifests:
    with open(p, "r", encoding="utf-8") as fh:
        d = json.load(fh)
    for f, m in d["files"].items():
        with open(f, "rb") as target:
            raw = target.read()
        dig = hashlib.sha256(raw).hexdigest()
        exp = m if isinstance(m, str) else m["digest"].replace("sha256:", "")
        if dig != exp:
            sys.exit(f"FAIL: Digest mismatch in {p} for {f}: expected {exp}, got {dig}")
        if isinstance(m, dict) and m.get("size_bytes") != len(raw):
            sys.exit(f"FAIL: Size mismatch in {p} for {f}: expected {m.get(\"size_bytes\")}, got {len(raw)}")

print("PASS: All 4 manifests (speckit, agy, claude, speckit-bootstrap) verified with 0 drift.")
'
```

---

## 5. Verify Documentation Hygiene & Link Integrity (`SC-005`, `FR-009`)

Confirm that `README.md` documents `.claude/` alongside `.agents/`, contains zero references to ephemeral `specs/NNN-*` paths or `FR-XXX`/`SC-XXX` identifiers, and has valid relative links.
