#!/usr/bin/env bash
# Direct execution test runner script for template resolution checks
# Validates raw and --json modes per specs/001-base-governance-templates/contracts/template-resolution-contract.md

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
RESOLVER="${REPO_ROOT}/.specify/scripts/bash/resolve-template.sh"

echo "=== Running Template Resolution Checks ==="

if [[ ! -x "${RESOLVER}" ]]; then
    chmod +x "${RESOLVER}"
fi

TEMPLATES=(
    "constitution-template"
    "coding-standards-template"
    "logging-standards-template"
)

FAILED=0

for tmpl in "${TEMPLATES[@]}"; do
    echo "--- Testing template: ${tmpl} ---"
    
    # 1. Raw text mode
    echo -n "  [RAW] Resolving ${tmpl}... "
    if "${RESOLVER}" "${tmpl}" > /dev/null; then
        echo "OK"
    else
        echo "FAILED"
        FAILED=1
    fi

    # 2. JSON mode
    echo -n "  [JSON] Resolving ${tmpl} --json... "
    JSON_OUTPUT=$("${RESOLVER}" "${tmpl}" --json)
    if echo "${JSON_OUTPUT}" | grep -q "\"TEMPLATE_NAME\":\"${tmpl}\""; then
        echo "OK"
    else
        echo "FAILED (invalid JSON output)"
        FAILED=1
    fi
done

if [[ ${FAILED} -ne 0 ]]; then
    echo "❌ Some template resolution checks failed."
    exit 1
fi

echo "✅ All template resolution checks passed successfully."
exit 0
