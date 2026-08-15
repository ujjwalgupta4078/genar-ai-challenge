from pathlib import Path
import pandas as pd


# ==========================================
# CONFIGURATION
# ==========================================

DATA_PATH = Path(
    "data/Bisoprolol_icsr_sample_1068rows.xlsx"
)


# ==========================================
# LOAD DATASET
# ==========================================

def load_dataset(path: Path) -> pd.DataFrame:
    """Load the supplied ICSR Excel dataset."""

    if not path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {path}"
        )

    df = pd.read_excel(path)

    if df.empty:
        raise ValueError("Dataset is empty.")

    return df


# ==========================================
# VALIDATE DATASET
# ==========================================

def validate_dataset(df: pd.DataFrame) -> None:
    """Validate the basic structure of the dataset."""

    required_columns = [
        "safetyreportid",
        "patient_patientonsetage",
        "patient_patientsex",
        "occurcountry",
        "patient_reaction_reactionmeddrapt",
        "serious",
        "patient_reaction_reactionoutcome",
        "receivedate",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )


# ==========================================
# BASIC DATASET REPORT
# ==========================================

def print_dataset_report(df: pd.DataFrame) -> None:

    print("\n" + "=" * 60)
    print("GENAR — DATASET VALIDATION")
    print("=" * 60)

    print(f"\nRows: {len(df):,}")
    print(f"Columns: {len(df.columns):,}")

    # Unique safety cases
    unique_cases = df["safetyreportid"].nunique()

    print(
        f"Unique safety cases: "
        f"{unique_cases:,}"
    )

    # Duplicate report IDs
    duplicate_rows = (
        df["safetyreportid"].duplicated().sum()
    )

    print(
        f"Rows belonging to repeated safety reports: "
        f"{duplicate_rows:,}"
    )

    # Missing values
    print("\nTop missing-value fields:")

    missing = (
        df.isna()
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    for column, count in missing.items():
        print(f"  {column}: {count:,}")

    # Required columns
    print("\nRequired columns:")

    required_columns = [
        "safetyreportid",
        "patient_patientonsetage",
        "patient_patientsex",
        "occurcountry",
        "patient_reaction_reactionmeddrapt",
        "serious",
        "patient_reaction_reactionoutcome",
        "receivedate",
    ]

    for column in required_columns:
        print(f"  ✓ {column}")

    print("\n" + "=" * 60)
    print("DATASET VALIDATION COMPLETED")
    print("=" * 60)


# ==========================================
# CASE-LEVEL SAFETY ANALYSIS
# ==========================================

def analyze_case_seriousness(df: pd.DataFrame) -> dict:
    """
    Perform case-level seriousness analysis.

    One safety report may appear in multiple rows,
    so seriousness is calculated at unique safety-report level.
    """

    # Keep one record per safety report
    cases = df.drop_duplicates(
        subset=["safetyreportid"]
    ).copy()

    total_cases = len(cases)

    # Normalize seriousness values
    serious_values = (
        cases["serious"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    serious_cases = (
        serious_values == "serious"
    ).sum()

    non_serious_cases = (
        serious_values == "not serious"
    ).sum()

    unknown_seriousness = (
        total_cases
        - serious_cases
        - non_serious_cases
    )

    # Seriousness percentage
    serious_percentage = (
        (serious_cases / total_cases) * 100
        if total_cases
        else 0
    )

    return {
        "total_cases": int(total_cases),
        "serious_cases": int(serious_cases),
        "non_serious_cases": int(non_serious_cases),
        "unknown_seriousness": int(
            unknown_seriousness
        ),
        "serious_percentage": round(
            serious_percentage,
            2
        ),
    }


# ==========================================
# PRINT CASE ANALYSIS
# ==========================================

def print_case_analysis(
    results: dict
) -> None:

    print("\n" + "=" * 60)
    print("CASE-LEVEL SAFETY ANALYSIS")
    print("=" * 60)

    print(
        f"\nTotal unique cases: "
        f"{results['total_cases']:,}"
    )

    print(
        f"Serious cases: "
        f"{results['serious_cases']:,}"
    )

    print(
        f"Non-serious cases: "
        f"{results['non_serious_cases']:,}"
    )

    print(
        f"Unknown seriousness: "
        f"{results['unknown_seriousness']:,}"
    )

    print(
        f"Serious cases (%): "
        f"{results['serious_percentage']:.2f}%"
    )

    print("\n" + "=" * 60)


# ==========================================
# DEMOGRAPHIC ANALYSIS
# ==========================================

def analyze_demographics(
    df: pd.DataFrame
) -> dict:
    """
    Calculate case-level demographic distributions.

    Demographic metrics are calculated using unique
    safety report IDs so repeated reaction rows do
    not inflate case counts.
    """

    # One record per unique safety report
    cases = df.drop_duplicates(
        subset=["safetyreportid"]
    ).copy()

    # --------------------------------------
    # Age
    # --------------------------------------

    cases["age"] = pd.to_numeric(
        cases["patient_patientonsetage"],
        errors="coerce"
    )

    # --------------------------------------
    # Age groups
    # --------------------------------------

    def age_group(age):

        if pd.isna(age):
            return "Unknown"

        elif age < 18:
            return "<18"

        elif age < 45:
            return "18-44"

        elif age < 65:
            return "45-64"

        elif age < 75:
            return "65-74"

        else:
            return "75+"

    cases["age_group"] = cases["age"].apply(
        age_group
    )

    age_distribution = (
        cases["age_group"]
        .value_counts()
        .to_dict()
    )

    # --------------------------------------
    # Sex distribution
    # --------------------------------------

    sex_distribution = (
        cases["patient_patientsex"]
        .fillna("unknown")
        .astype(str)
        .str.strip()
        .str.lower()
        .value_counts()
        .to_dict()
    )

    # --------------------------------------
    # Country distribution
    # --------------------------------------

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

    return {
        "age_distribution": {
            str(key): int(value)
            for key, value in age_distribution.items()
        },
        "sex_distribution": {
            str(key): int(value)
            for key, value in sex_distribution.items()
        },
        "country_distribution": {
            str(key): int(value)
            for key, value in country_distribution.items()
        },
    }


# ==========================================
# PRINT DEMOGRAPHIC ANALYSIS
# ==========================================

def print_demographic_analysis(
    results: dict
) -> None:

    print("\n" + "=" * 60)
    print("DEMOGRAPHIC ANALYSIS")
    print("=" * 60)

    print("\nAge distribution:")

    for group, count in (
        results["age_distribution"].items()
    ):
        print(f"  {group}: {count:,}")

    print("\nSex distribution:")

    for sex, count in (
        results["sex_distribution"].items()
    ):
        print(f"  {sex}: {count:,}")

    print("\nTop countries:")

    for country, count in (
        results["country_distribution"].items()
    ):
        print(f"  {country}: {count:,}")

    print("\n" + "=" * 60)
# ==========================================
# REACTION ANALYSIS
# ==========================================

def analyze_reactions(
    df: pd.DataFrame
) -> dict:
    """
    Calculate the frequency of individual reaction terms.

    Reaction-level analysis keeps repeated reaction
    records instead of reducing everything to one row
    per safety report.
    """

    reactions = (
        df["patient_reaction_reactionmeddrapt"]
        .dropna()
        .astype(str)
        .str.strip()
    )

    # Remove empty values
    reactions = reactions[
        reactions != ""
    ]

    # Count reaction terms
    reaction_counts = (
        reactions
        .value_counts()
        .head(10)
        .to_dict()
    )

    return {
        "top_reactions": {
            str(term): int(count)
            for term, count in reaction_counts.items()
        }
    }


# ==========================================
# PRINT REACTION ANALYSIS
# ==========================================

def print_reaction_analysis(
    results: dict
) -> None:

    print("\n" + "=" * 60)
    print("TOP REACTION TERMS")
    print("=" * 60)

    for rank, (
        reaction,
        count
    ) in enumerate(
        results["top_reactions"].items(),
        start=1
    ):
        print(
            f"{rank:2}. "
            f"{reaction}: "
            f"{count:,}"
        )

    print("\n" + "=" * 60)

# ==========================================
# OUTCOME ANALYSIS
# ==========================================

def analyze_outcomes(
    df: pd.DataFrame
) -> dict:
    """
    Normalize reaction outcomes and calculate
    their frequencies.
    """

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

    outcome_counts = (
        outcomes
        .value_counts()
        .to_dict()
    )

    return {
        "outcomes": {
            str(outcome): int(count)
            for outcome, count in outcome_counts.items()
        }
    }


# ==========================================
# PRINT OUTCOME ANALYSIS
# ==========================================

def print_outcome_analysis(
    results: dict
) -> None:

    print("\n" + "=" * 60)
    print("REACTION OUTCOME ANALYSIS")
    print("=" * 60)

    for outcome, count in (
        results["outcomes"].items()
    ):
        print(
            f"  {outcome}: {count:,}"
        )

    print("\n" + "=" * 60)
# ==========================================
# SERIOUS CASE REACTION ANALYSIS
# ==========================================

def analyze_serious_reactions(
    df: pd.DataFrame
) -> dict:
    """
    Identify the most frequently reported reactions
    among serious safety reports.
    """

    serious_cases = (
        df[
            df["serious"]
            .astype(str)
            .str.strip()
            .str.lower()
            == "serious"
        ]
        .copy()
    )

    reactions = (
        serious_cases[
            "patient_reaction_reactionmeddrapt"
        ]
        .dropna()
        .astype(str)
        .str.strip()
    )

    reactions = reactions[
        reactions != ""
    ]

    reaction_counts = (
        reactions
        .value_counts()
        .head(10)
        .to_dict()
    )

    return {
        "serious_reactions": {
            str(reaction): int(count)
            for reaction, count
            in reaction_counts.items()
        }
    }


# ==========================================
# PRINT SERIOUS REACTION ANALYSIS
# ==========================================

def print_serious_reaction_analysis(
    results: dict
) -> None:

    print("\n" + "=" * 60)
    print("TOP REACTIONS IN SERIOUS REPORTS")
    print("=" * 60)

    for rank, (
        reaction,
        count
    ) in enumerate(
        results["serious_reactions"].items(),
        start=1
    ):
        print(
            f"{rank:2}. "
            f"{reaction}: "
            f"{count:,}"
        )

    print("\n" + "=" * 60)

# ==========================================
# MAIN
# ==========================================

def main():

    # Load
    df = load_dataset(DATA_PATH)

    # Validate
    validate_dataset(df)

    # Dataset report
    print_dataset_report(df)

    # Case-level analysis
    case_results = analyze_case_seriousness(df)

    print_case_analysis(case_results)

    # Demographic analysis
    demographic_results = analyze_demographics(df)

    print_demographic_analysis(
        demographic_results
    )
    reaction_results = analyze_reactions(df)

    print_reaction_analysis(
        reaction_results
    )
    # Outcome analysis
    outcome_results = analyze_outcomes(df)

    print_outcome_analysis(
        outcome_results
    )
        # Serious reaction analysis
    serious_reaction_results = (
        analyze_serious_reactions(df)
    )

    print_serious_reaction_analysis(
        serious_reaction_results
    )


# ==========================================
# PROGRAM ENTRY POINT
# ==========================================

if __name__ == "__main__":
    main()