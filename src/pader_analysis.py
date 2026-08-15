from typing import Dict, Any
import pandas as pd


# ==========================================
# PADER ANALYSIS
# ==========================================

def build_pader_analysis(
    df: pd.DataFrame
) -> Dict[str, Any]:
    """
    Build a structured evidence package for PADER-style
    safety report generation.

    All numerical findings are calculated deterministically
    from the supplied dataset.
    """

    # --------------------------------------
    # CASE-LEVEL DATA
    # --------------------------------------

    cases = df.drop_duplicates(
        subset=["safetyreportid"]
    ).copy()

    total_cases = len(cases)

    # --------------------------------------
    # SERIOUSNESS
    # --------------------------------------

    seriousness = (
        cases["serious"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    serious_cases = int(
        (seriousness == "serious").sum()
    )

    non_serious_cases = int(
        (seriousness == "not serious").sum()
    )

    unknown_cases = (
        total_cases
        - serious_cases
        - non_serious_cases
    )

    serious_percentage = (
        (serious_cases / total_cases) * 100
        if total_cases
        else 0
    )

    # --------------------------------------
    # DEMOGRAPHICS
    # --------------------------------------

    cases["age"] = pd.to_numeric(
        cases["patient_patientonsetage"],
        errors="coerce"
    )

    def age_group(age):

        if pd.isna(age):
            return "Unknown"

        if age < 18:
            return "<18"

        if age < 45:
            return "18-44"

        if age < 65:
            return "45-64"

        if age < 75:
            return "65-74"

        return "75+"

    cases["age_group"] = cases["age"].apply(
        age_group
    )

    age_distribution = (
        cases["age_group"]
        .value_counts()
        .to_dict()
    )

    sex_distribution = (
        cases["patient_patientsex"]
        .fillna("unknown")
        .astype(str)
        .str.strip()
        .str.lower()
        .value_counts()
        .to_dict()
    )

    country_distribution = (
        cases["occurcountry"]
        .fillna("unknown")
        .astype(str)
        .str.strip()
        .str.lower()
        .value_counts()
        .head(15)
        .to_dict()
    )

    # --------------------------------------
    # REACTIONS
    # --------------------------------------

    reactions = (
        df["patient_reaction_reactionmeddrapt"]
        .dropna()
        .astype(str)
        .str.strip()
    )

    reactions = reactions[
        reactions != ""
    ]

    top_reactions = (
        reactions
        .value_counts()
        .head(10)
        .to_dict()
    )

    # --------------------------------------
    # OUTCOMES
    # --------------------------------------

    outcomes = (
        df["patient_reaction_reactionoutcome"]
        .dropna()
        .astype(str)
        .str.split(",")
        .explode()
        .str.strip()
        .str.lower()
    )

    outcomes = outcomes[
        outcomes != ""
    ]

    outcome_distribution = (
        outcomes
        .value_counts()
        .to_dict()
    )

    # --------------------------------------
    # RETURN STRUCTURED EVIDENCE
    # --------------------------------------

    return {

        "dataset": {
            "rows": int(len(df)),
            "columns": int(len(df.columns)),
            "unique_cases": int(total_cases),
        },

        "seriousness": {
            "serious_cases": serious_cases,
            "non_serious_cases": non_serious_cases,
            "unknown_cases": int(unknown_cases),
            "serious_percentage": round(
                serious_percentage,
                2
            ),
        },

        "demographics": {
            "age_distribution": {
                str(key): int(value)
                for key, value
                in age_distribution.items()
            },

            "sex_distribution": {
                str(key): int(value)
                for key, value
                in sex_distribution.items()
            },

            "country_distribution": {
                str(key): int(value)
                for key, value
                in country_distribution.items()
            },
        },

        "reactions": {
            "top_10": {
                str(key): int(value)
                for key, value
                in top_reactions.items()
            },
        },

        "outcomes": {
            "distribution": {
                str(key): int(value)
                for key, value
                in outcome_distribution.items()
            },
        },
    }