from typing import Dict, Any


def build_pader_report_structure(
    analysis: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Convert structured safety evidence into a
    report-ready PADER structure.

    No AI-generated claims are created here.
    """

    return {
        "title": "Bisoprolol Periodic Adverse Drug Reaction Report",

        "executive_summary": {
            "status": "pending_generation",
            "evidence": analysis["dataset"],
        },

        "case_overview": {
            "dataset": analysis["dataset"],
            "seriousness": analysis["seriousness"],
        },

        "patient_demographics": {
            "age_distribution": (
                analysis["demographics"]
                ["age_distribution"]
            ),
            "sex_distribution": (
                analysis["demographics"]
                ["sex_distribution"]
            ),
            "country_distribution": (
                analysis["demographics"]
                ["country_distribution"]
            ),
        },

        "reported_reactions": {
            "top_10": (
                analysis["reactions"]
                ["top_10"]
            ),
        },

        "outcomes": {
            "distribution": (
                analysis["outcomes"]
                ["distribution"]
            ),
        },

        "important_safety_signals": {
            "status": "requires_evaluation",
        },

        "benefit_risk_discussion": {
            "status": "requires_evaluation",
        },

        "limitations": {
            "status": "requires_generation",
        },
    }
