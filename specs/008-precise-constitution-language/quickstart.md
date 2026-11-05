# Quickstart: Validating Constitution Language Modernization

**Feature**: `specs/008-precise-constitution-language`  
**Date**: 2026-11-05  

## 1. Verify Clean Language & Principle Titles

Check that legacy flowery phrases no longer appear in active governance files:

```bash
# Check for legacy "Evidence Over Invention"
grep -rn "Evidence Over Invention" .specify/memory/ .specify/templates/ .agents/ .claude/ README.md

# Verify Principle I title is modernized
grep -rn "Evidence-Based Decisions" .specify/memory/constitution.md .specify/templates/constitution-template.md README.md
```

## 2. Verify Dual-Client Agent Parity

Ensure Antigravity and Claude Code subagents remain 100% synchronized:

```bash
diff -u .agents/agents/speckit-executor.md .claude/agents/speckit-executor.md
diff -u .agents/agents/speckit-reasoner.md .claude/agents/speckit-reasoner.md
```

## 3. Verify Template Resolution & Manifest Integrity

Ensure templates resolve cleanly using the bash resolve-template script:

```bash
bash .specify/scripts/bash/resolve-template.sh constitution-template --json
bash .specify/scripts/bash/resolve-template.sh coding-standards-template --json
bash .specify/scripts/bash/resolve-template.sh logging-standards-template --json
```

## 4. Run Pre-PR Check

```bash
git status --short
```
