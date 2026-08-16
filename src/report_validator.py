from typing import Dict, Any, List
import re


# ==========================================
# REQUIRED PADER SECTIONS
# ==========================================

REQUIRED_SECTIONS = [
    "Executive Summary",
    "Case Overview",
    "Patient Demographics",
    "Seriousness Analysis",
    "Reported Reactions",
    "Reaction Outcomes",
    "Important Safety Signals",
    "Benefit-Risk Discussion",
    "Limitations",
]


# ==========================================
# VALIDATE REQUIRED SECTIONS
# ==========================================

def validate_sections(report: str) -> List[str]:
    issues = []

    for section in REQUIRED_SECTIONS:
        if section.lower() not in report.lower():
            issues.append(
                f"Missing required section: {section}"
            )

    return issues


# ==========================================
# VALIDATE KEY NUMBERS
# ==========================================

def validate_numbers(
    report: str,
    evidence: Dict[str, Any]
) -> List[str]:
    """
    Validate important evidence numbers.

    Accepts:
    1068 and 1,068
    1024 and 1,024
    """

    issues = []

    dataset = evidence.get("dataset", {})
    seriousness = evidence.get("seriousness", {})

    expected_numbers = {
        "rows": dataset.get("rows"),
        "columns": dataset.get("columns"),
        "unique_cases": dataset.get("unique_cases"),
        "serious_cases": seriousness.get("serious_cases"),
        "non_serious_cases": seriousness.get("non_serious_cases"),
        "serious_percentage": seriousness.get("serious_percentage"),
    }

    for name, value in expected_numbers.items():

        if value is None:
            continue

        if isinstance(value, float):
            variants = {
                str(value),
                f"{value:.1f}",
            }
        else:
            variants = {
                str(value),
                f"{value:,}",
            }

        found = any(
            variant in report
            for variant in variants
        )

        if not found:
            issues.append(
                f"Expected value not found in report: "
                f"{name} = {value}"
            )

    return issues


# ==========================================
# VALIDATE TOP REACTIONS
# ==========================================

def validate_reactions(
    report: str,
    evidence: Dict[str, Any]
) -> List[str]:

    issues = []

    reactions = (
        evidence
        .get("reactions", {})
        .get("top_10", {})
    )

    for reaction, frequency in reactions.items():

        if reaction.lower() not in report.lower():
            issues.append(
                f"Reaction missing from report: "
                f"{reaction}"
            )
            continue

        frequency_variants = {
            str(frequency),
            f"{frequency:,}"
        }

        if not any(
            value in report
            for value in frequency_variants
        ):
            issues.append(
                f"Reaction frequency not found: "
                f"{reaction} = {frequency}"
            )

    return issues


# ==========================================
# VALIDATE CAUSALITY LANGUAGE
# ==========================================

def validate_causality(report: str) -> List[str]:
    """
    Detect potentially unsupported causal statements.

    Causal words are only flagged when they appear
    in potentially affirmative contexts.
    """

    issues = []

    suspicious_patterns = [
        r"\b(?:was|were|is|are|has been|have been)\s+caused by\b",
        r"\b(?:caused|causes|causing)\s+(?:the|this|these|the reported)\b",
        r"\bresponsible for\s+(?:the|this|these)\b",
    ]

    for pattern in suspicious_patterns:

        matches = re.findall(
            pattern,
            report,
            flags=re.IGNORECASE
        )

        if matches:
            issues.append(
                "Potential unsupported causal statement "
                f"detected: '{matches[0]}'"
            )

    return issues


# ==========================================
# COMPLETE REPORT VALIDATION
# ==========================================

def validate_report(
    report: str,
    evidence: Dict[str, Any]
) -> Dict[str, Any]:

    section_issues = validate_sections(report)

    number_issues = validate_numbers(
        report,
        evidence
    )

    reaction_issues = validate_reactions(
        report,
        evidence
    )

    causality_issues = validate_causality(
        report
    )

    all_issues = (
        section_issues
        + number_issues
        + reaction_issues
        + causality_issues
    )

    return {
        "valid": len(all_issues) == 0,
        "issue_count": len(all_issues),
        "issues": all_issues,
        "checks": {
            "sections": len(section_issues) == 0,
            "numbers": len(number_issues) == 0,
            "reactions": len(reaction_issues) == 0,
            "causality": len(causality_issues) == 0,
        },
    }