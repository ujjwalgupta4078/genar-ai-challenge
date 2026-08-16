import streamlit as st
import pandas as pd
from pathlib import Path

from src.pader_analysis import build_pader_analysis
from src.llm_prompt import build_pader_prompt
from src.llm_generator import generate_pader_report
from src.report_validator import validate_report


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="GENAR AI",
    page_icon="🛡️",
    layout="wide"
)


# =========================================================
# CLEAN UI
# =========================================================

st.markdown("""
<style>

    /* Main page */
    .stApp {
        background: #f7f8fa;
    }

    /* Main content width */
    .block-container {
        max-width: 1100px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    /* Header */
    .brand {
        font-size: 28px;
        font-weight: 800;
        color: #111827;
        margin-bottom: 2px;
    }

    .brand span {
        color: #c99a22;
    }

    .subtitle {
        color: #6b7280;
        font-size: 14px;
        margin-bottom: 30px;
    }

    /* Hero */
    .hero {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 14px;
        padding: 32px;
        margin-bottom: 28px;
    }

    .hero h1 {
        color: #111827 !important;
        font-size: 32px;
        margin-bottom: 10px;
    }

    .hero p {
        color: #6b7280 !important;
        font-size: 16px;
        margin-bottom: 0;
    }

    /* Section headings */
    h2, h3 {
        color: #111827 !important;
    }

    /* Normal markdown text */
    p, li, td, th {
        color: #1f2937 !important;
    }

    /* Report container */
    .report-box {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 14px;
        padding: 32px;
        margin-top: 20px;
    }

    .report-box h1,
    .report-box h2,
    .report-box h3 {
        color: #111827 !important;
    }

    .report-box p,
    .report-box li {
        color: #374151 !important;
        line-height: 1.7;
    }

    /* Tables */
    table {
        width: 100%;
        border-collapse: collapse;
        margin: 15px 0;
    }

    th {
        background: #f3f4f6 !important;
        color: #111827 !important;
        text-align: left;
        padding: 10px;
    }

    td {
        padding: 10px;
        border-bottom: 1px solid #e5e7eb;
        color: #374151 !important;
    }

    /* Upload */
    [data-testid="stFileUploader"] {
        background: white;
        border: 1px dashed #cbd5e1;
        border-radius: 12px;
        padding: 10px;
    }

    /* Buttons */
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
        padding: 10px;
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="brand">GENAR <span>AI</span></div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">AI-assisted pharmacovigilance reporting</div>',
    unsafe_allow_html=True
)


# =========================================================
# HERO
# =========================================================

st.markdown("""
<div class="hero">

<h1>Pharmacovigilance Safety Report Generator</h1>

<p>
Analyze ICSR safety data, identify reported safety patterns,
and generate a controlled PADER-style safety narrative.
</p>

</div>
""", unsafe_allow_html=True)


# =========================================================
# UPLOAD DATASET
# =========================================================

st.subheader("Upload Dataset")

uploaded_file = st.file_uploader(
    "Upload your ICSR dataset",
    type=["xlsx", "xls", "csv"]
)


# =========================================================
# LOAD DATA
# =========================================================

if uploaded_file is not None:

    try:

        if uploaded_file.name.lower().endswith(".csv"):
            df = pd.read_csv(uploaded_file)

        else:
            df = pd.read_excel(uploaded_file)

        st.success(
            f"Dataset loaded successfully — "
            f"{len(df):,} rows × {len(df.columns):,} columns"
        )

    except Exception as e:

        st.error(f"Unable to read dataset: {e}")
        st.stop()

else:

    st.info(
        "Upload the Bisoprolol ICSR Excel dataset to begin."
    )
    st.stop()


# =========================================================
# ANALYZE DATASET
# =========================================================

st.subheader("Dataset Analysis")

try:

    analysis = build_pader_analysis(df)

except Exception as e:

    st.error(f"Analysis failed: {e}")
    st.stop()


# =========================================================
# SUMMARY CARDS
# =========================================================

dataset = analysis["dataset"]
seriousness = analysis["seriousness"]


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Rows",
        f"{dataset['rows']:,}"
    )

with col2:
    st.metric(
        "Unique Cases",
        f"{dataset['unique_cases']:,}"
    )

with col3:
    st.metric(
        "Serious Cases",
        f"{seriousness['serious_cases']:,}"
    )

with col4:
    st.metric(
        "Serious %",
        f"{seriousness['serious_percentage']:.2f}%"
    )


# =========================================================
# REPORTED REACTIONS
# =========================================================

st.subheader("Top Reported Reactions")

reaction_data = analysis.get(
    "reactions",
    {}
).get(
    "top_10",
    {}
)

if reaction_data:

    reaction_df = pd.DataFrame(
        list(reaction_data.items()),
        columns=["Reaction", "Reports"]
    )

    st.dataframe(
        reaction_df,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# OUTCOMES
# =========================================================

st.subheader("Reaction Outcomes")

outcome_data = analysis.get(
    "outcomes",
    {}
).get(
    "distribution",
    {}
)

if outcome_data:

    outcome_df = pd.DataFrame(
        list(outcome_data.items()),
        columns=["Outcome", "Records"]
    )

    st.dataframe(
        outcome_df,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# GENERATE PADER REPORT
## =========================================================
# PADER REPORT GENERATION + VALIDATION
# =========================================================

st.divider()

st.subheader("Generate PADER Report")

st.write(
    "Generate a controlled PADER-style safety narrative "
    "using only the analyzed evidence."
)

if st.button(
    "Generate PADER Report",
    type="primary"
):

    try:

        with st.spinner(
            "Generating PADER safety narrative..."
        ):

            # Build controlled prompt from evidence
            prompt = build_pader_prompt(analysis)

            # Generate PADER report
            report = generate_pader_report(
                prompt
            )

            # Validate generated report
            validation = validate_report(
                report,
                analysis
            )

            # Stop if validation fails
            if not validation["valid"]:

                st.error(
                    "PADER report validation failed."
                )

                st.warning(
                    f"{validation['issue_count']} "
                    "validation issue(s) detected."
                )

                for issue in validation["issues"]:
                    st.warning(issue)

            else:

                # Save only validated report
                st.session_state["pader_report"] = report

                st.success(
                    "PADER report generated and "
                    "validated successfully."
                )

    except Exception as e:

        st.error(
            f"Report generation failed: {e}"
        )
# =========================================================
# DISPLAY GENERATED REPORT
# =========================================================

if "pader_report" in st.session_state:

    st.divider()

    st.subheader("Generated PADER Report")

    report = st.session_state["pader_report"]

    # IMPORTANT:
    # Render Markdown instead of putting report
    # inside a text/code box.
    st.markdown(
        '<div class="report-box">',
        unsafe_allow_html=True
    )

    st.markdown(report)

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

    # =====================================================
    # DOWNLOAD
    # =====================================================

    st.download_button(
        label="Download PADER Report",
        data=report,
        file_name="PADER_Safety_Report.md",
        mime="text/markdown"
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <br>
    <center>
    <small style="color:#9ca3af;">
    GENAR AI · AI-assisted pharmacovigilance reporting
    </small>
    </center>
    """,
    unsafe_allow_html=True
)