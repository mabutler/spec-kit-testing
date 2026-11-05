"""
Validation test suite for Spec Kit Base Governance Templates.
Implements Scenarios 1-6 from specs/001-base-governance-templates/quickstart.md.
"""

import os
import pathlib
import re
import unittest

PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
TEMPLATES_DIR = PROJECT_ROOT / ".specify" / "templates"

REQUIRED_TEMPLATES = [
    "constitution-template.md",
    "coding-standards-template.md",
    "logging-standards-template.md",
]

CORE_PRINCIPLES = [
    "I. Evidence Over Invention & Bounded Investigation",
    "II. Two-Tier Failure Model & Fail Closed on Required State",
    "III. Behavioral, Value-Driven Testing & Deterministic Execution",
    "IV. Single Authoritative State, Enforced Boundaries & Safe Concurrency",
    "V. Centralized Dependencies & Protected Toolchain Gate",
    "VI. Bounded Resources & Verify-Before-Destroy",
    "VII. Code Hygiene, Ubiquitous Language & Safe Logging",
]

OPTIONAL_MODULE_DELIMITERS = [
    "<!-- OPTIONAL-MODULE: MODULE-A",
    "<!-- /OPTIONAL-MODULE: MODULE-A -->",
    "<!-- DEFAULT-CLAUSE: PLAN-JUSTIFICATION-AND-SKIP-ALLOWLIST",
    "<!-- /DEFAULT-CLAUSE: PLAN-JUSTIFICATION-AND-SKIP-ALLOWLIST -->",
    "<!-- OPTIONAL-MODULE: MODULE-B",
    "<!-- /OPTIONAL-MODULE: MODULE-B -->",
    "<!-- OPTIONAL-MODULE: MODULE-C",
    "<!-- /OPTIONAL-MODULE: MODULE-C -->",
    "<!-- OPTIONAL-MODULE: MODULE-D",
    "<!-- /OPTIONAL-MODULE: MODULE-D -->",
    "<!-- OPTIONAL-SUBCLAUSE: MODULE-D-AOT-TRIM",
    "<!-- /OPTIONAL-SUBCLAUSE: MODULE-D-AOT-TRIM -->",
]

CODING_STANDARDS_HEADINGS = [
    "Constitutional Authority",
    "Compile-Time & Architectural Boundaries",
    "Two-Tier Failure Handling",
    "Concurrency, Lock Discipline & Immutable Snapshots",
    "Disambiguated Identifier",
    "Bounded Inputs & Resource Protection",
    "Hostile Boundary & Behavioral Unit Testing",
    "Code Hygiene & Commenting Conventions",
]

CODING_STANDARDS_PLACEHOLDERS = [
    "[PROJECT_NAME]",
    "[PRIMARY_LANGUAGE_AND_RUNTIME]",
    "[BUILD_AND_LINTER_COMMANDS]",
    "[PROJECT_STRUCTURE_CONVENTIONS]",
    "[NAMING_CONVENTIONS]",
    "[ERROR_RESULT_TYPES]",
    "[TEST_FRAMEWORK_CONVENTIONS]",
]

LOGGING_STANDARDS_LEVELS = [
    "CRITICAL",
    "WARN",
    "INFO",
    "DEBUG",
    "TRACE",
]

LOGGING_STANDARDS_POLICIES = [
    "session_id",
    "event_id",
    "ToString",
    "Passwords, tokens, secrets",
    ">100/sec",
]

LOGGING_STANDARDS_PLACEHOLDERS = [
    "[PROJECT_NAME]",
    "[LOGGING_FRAMEWORK]",
    "[LOG_SINKS_AND_FORMATS]",
    "[CORRELATION_ID_SCHEMA]",
    "[SENSITIVE_DATA_REDACTION_MECHANISM]",
    "[RETENTION_AND_SAMPLING_POLICY]",
]

CONSTITUTION_PLACEHOLDERS = [
    "[PROJECT_NAME]",
    "[PRIMARY_SOURCE]",
    "[SECONDARY_SOURCE]",
    "[TERTIARY_SOURCE]",
    "[ACCEPTANCE_GATE_COMMANDS]",
    "[YYYY-MM-DD]",
]


class TestGovernanceTemplates(unittest.TestCase):

    def test_scenario_1_direct_file_presence(self):
        """Scenario 1: Verify all 3 templates exist and have non-empty content."""
        self.assertTrue(TEMPLATES_DIR.is_dir(), f"Templates directory not found: {TEMPLATES_DIR}")
        for tmpl_name in REQUIRED_TEMPLATES:
            path = TEMPLATES_DIR / tmpl_name
            self.assertTrue(path.is_file(), f"Template missing: {path}")
            content = path.read_text(encoding="utf-8")
            self.assertGreater(len(content), 100, f"Template {tmpl_name} is unexpectedly empty")

    def test_scenario_2_constitution_structure_and_delimiters(self):
        """Scenario 2: Validate constitution principles, sections, and delimiters."""
        const_path = TEMPLATES_DIR / "constitution-template.md"
        self.assertTrue(const_path.is_file(), f"Missing constitution-template.md at {const_path}")
        content = const_path.read_text(encoding="utf-8")

        # 1. Principles check
        for principle in CORE_PRINCIPLES:
            self.assertIn(principle, content, f"Missing Core Principle: {principle}")

        # 2. Delimiters presence check
        for delimiter in OPTIONAL_MODULE_DELIMITERS:
            self.assertIn(delimiter, content, f"Missing optional module delimiter: {delimiter}")

        # 3. Delimiter grammar regex matching per contracts/optional-module-delimiters.md
        module_a_match = re.search(
            r"<!-- OPTIONAL-MODULE:\s*MODULE-A\s*\nAction:\s*ADD\s*\nTitle:\s*([^\n]+)\s*\nTarget:\s*([^\n]+)\s*-->\n([\s\S]*?)<!-- /OPTIONAL-MODULE:\s*MODULE-A\s*-->",
            content,
        )
        self.assertIsNotNone(module_a_match, "Module A delimiter block does not match contract regex")
        self.assertIn("Principle I", module_a_match.group(2))

        default_b_match = re.search(
            r"<!-- DEFAULT-CLAUSE:\s*PLAN-JUSTIFICATION-AND-SKIP-ALLOWLIST\s*\(REPLACEABLE-BY:\s*MODULE-B\)\s*\nTarget:\s*([^\n]+)\s*-->\n([\s\S]*?)<!-- /DEFAULT-CLAUSE:\s*PLAN-JUSTIFICATION-AND-SKIP-ALLOWLIST\s*-->",
            content,
        )
        self.assertIsNotNone(default_b_match, "Default clause for Module B does not match contract regex")
        self.assertIn("Principle III", default_b_match.group(1))

        module_b_match = re.search(
            r"<!-- OPTIONAL-MODULE:\s*MODULE-B\s*\nAction:\s*REPLACE\s*\nTarget:\s*([^\n]+)\s*\nReplaces:\s*PLAN-JUSTIFICATION-AND-SKIP-ALLOWLIST\s*\nTitle:\s*([^\n]+)\s*-->\n([\s\S]*?)<!-- /OPTIONAL-MODULE:\s*MODULE-B\s*-->",
            content,
        )
        self.assertIsNotNone(module_b_match, "Module B replacement block does not match contract regex")
        self.assertIn("Principle III", module_b_match.group(1))

        module_c_match = re.search(
            r"<!-- OPTIONAL-MODULE:\s*MODULE-C\s*\nAction:\s*ADD\s*\nTitle:\s*([^\n]+)\s*\nTarget:\s*([^\n]+)\s*-->\n([\s\S]*?)<!-- /OPTIONAL-MODULE:\s*MODULE-C\s*-->",
            content,
        )
        self.assertIsNotNone(module_c_match, "Module C delimiter block does not match contract regex")
        self.assertIn("Principle IV", module_c_match.group(2))

        module_d_match = re.search(
            r"<!-- OPTIONAL-MODULE:\s*MODULE-D\s*\nAction:\s*ADD\s*\nTitle:\s*([^\n]+)\s*\nTarget:\s*([^\n]+)\s*-->\n([\s\S]*?)<!-- /OPTIONAL-MODULE:\s*MODULE-D\s*-->",
            content,
        )
        self.assertIsNotNone(module_d_match, "Module D delimiter block does not match contract regex")
        self.assertIn("Principle V", module_d_match.group(2))

        subclause_d_match = re.search(
            r"<!-- OPTIONAL-SUBCLAUSE:\s*MODULE-D-AOT-TRIM\s*\nAction:\s*OPTIONAL-INCLUSION\s*\nParent-Module:\s*MODULE-D\s*\nTitle:\s*([^\n]+)\s*-->\n([\s\S]*?)<!-- /OPTIONAL-SUBCLAUSE:\s*MODULE-D-AOT-TRIM\s*-->",
            content,
        )
        self.assertIsNotNone(subclause_d_match, "Module D subclause does not match contract regex")

        # 4. Required sections and placeholders in constitution
        for ph in CONSTITUTION_PLACEHOLDERS:
            self.assertIn(ph, content, f"Missing placeholder in constitution-template.md: {ph}")

    def test_scenario_3_coding_standards_baseline_and_slots(self):
        """Scenario 3: Validate coding standards baseline sections and slots."""
        coding_path = TEMPLATES_DIR / "coding-standards-template.md"
        self.assertTrue(coding_path.is_file(), f"Missing coding-standards-template.md at {coding_path}")
        content = coding_path.read_text(encoding="utf-8")

        for heading in CODING_STANDARDS_HEADINGS:
            self.assertIn(heading, content, f"Missing baseline heading in coding-standards-template.md: {heading}")

        for ph in CODING_STANDARDS_PLACEHOLDERS:
            self.assertIn(ph, content, f"Missing placeholder in coding-standards-template.md: {ph}")

    def test_scenario_4_logging_standards_severity_and_rules(self):
        """Scenario 4: Validate logging standards 5-tier taxonomy, rules, and slots."""
        logging_path = TEMPLATES_DIR / "logging-standards-template.md"
        self.assertTrue(logging_path.is_file(), f"Missing logging-standards-template.md at {logging_path}")
        content = logging_path.read_text(encoding="utf-8")

        for lvl in LOGGING_STANDARDS_LEVELS:
            pattern = rf"- \*\*{lvl}\*\*"
            self.assertIsNotNone(
                re.search(pattern, content),
                f"Missing severity level definition: {lvl}",
            )

        for policy in LOGGING_STANDARDS_POLICIES:
            self.assertIn(policy.lower(), content.lower(), f"Missing logging policy item: {policy}")

        for ph in LOGGING_STANDARDS_PLACEHOLDERS:
            self.assertIn(ph, content, f"Missing placeholder in logging-standards-template.md: {ph}")

    def test_scenario_5_placeholder_tokens_conformance(self):
        """Scenario 5: Scan bracketed expressions across templates to ensure conformance to contracts/placeholder-tokens.md."""
        token_regex = re.compile(r"\[([A-Za-z0-9_ -]+)\]")
        valid_standard = re.compile(r"^[A-Z0-9_]+$")
        valid_date = re.compile(r"^YYYY-MM-DD$")

        for tmpl_name in REQUIRED_TEMPLATES:
            path = TEMPLATES_DIR / tmpl_name
            if not path.is_file():
                continue
            content = path.read_text(encoding="utf-8")

            # Find all bracketed tokens that are NOT followed by '(' (markdown links)
            # or checkbox patterns like [ ] or [x] or [X]
            lines = content.splitlines()
            for line_idx, line in enumerate(lines, 1):
                # Skip markdown links e.g. [text](url)
                line_no_links = re.sub(r"\[([^\]]+)\]\([^\)]+\)", "", line)
                # Skip markdown checkboxes e.g. - [ ] or - [x]
                line_no_checkboxes = re.sub(r"-\s*\[[ xX]\]", "", line_no_links)

                for match in token_regex.finditer(line_no_checkboxes):
                    token_inner = match.group(1).strip()
                    if token_inner.startswith("Optional:"):
                        continue  # Inline prose notation permitted per contract
                    is_standard = bool(valid_standard.match(token_inner))
                    is_date = bool(valid_date.match(token_inner))
                    self.assertTrue(
                        is_standard or is_date,
                        f"Invalid placeholder token '[{token_inner}]' at {tmpl_name}:{line_idx}. Must match ^[A-Z0-9_]+$ or ^YYYY-MM-DD$",
                    )


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestGovernanceTemplates)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    if result.wasSuccessful():
        print("All cross-platform template integrity assertions passed successfully.")
        exit(0)
    else:
        exit(1)
