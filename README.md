# 🧬 GENAR AI — AI-Assisted Pharmacovigilance Safety Report Generator

> **Analyze safety data. Identify reported patterns. Generate a controlled PADER-style safety narrative.**

GENAR AI is an AI-assisted pharmacovigilance reporting application designed to help transform structured **Individual Case Safety Report (ICSR)** data into a clear, evidence-grounded **PADER-style safety narrative**.

The goal of the project is to reduce the manual effort required to analyze large amounts of pharmacovigilance data and prepare structured safety reporting content.

## 🚀 Live Demo

👉 [Try GENAR AI Live](https://genar-ai-challenge-gpfykrgx9bdektc9qiapoo.streamlit.app/)

---

## 🎯 What Problem Does GENAR AI Solve?

Pharmacovigilance datasets can contain hundreds or thousands of safety-report records with many fields such as:

* Patient age
* Patient sex
* Country
* Seriousness
* Reported reactions
* Reaction outcomes
* Report dates
* Drug-related information

Manually reviewing this information can be time-consuming.

### Traditional workflow

```text
ICSR Dataset
     ↓
Manual Data Review
     ↓
Find Important Patterns
     ↓
Calculate / Organize Findings
     ↓
Write Safety Narrative
     ↓
Review Report
```

### GENAR AI workflow

```text
ICSR Dataset
     ↓
Dataset Validation
     ↓
Automated Safety Analysis
     ↓
Structured Evidence
     ↓
Controlled AI Prompt
     ↓
PADER-Style Safety Narrative
```

GENAR AI separates **data analysis** from **AI generation** so that the language model receives structured evidence instead of directly interpreting the raw dataset.

---

# 🚀 How GENAR AI Works

## 1. Upload Safety Dataset

The application accepts an ICSR dataset containing pharmacovigilance records.

For example:

```text
Bisoprolol_icsr_sample_1068rows.xlsx
```

The current sample contains:

* **1,068 rows**
* **67 columns**
* **1,024 unique safety cases**

---

## 2. Validate the Dataset

Before generating a report, GENAR AI checks whether important safety-report fields are available.

Examples of required fields include:

```text
safetyreportid
patient_patientonsetage
patient_patientsex
occurcountry
patient_reaction_reactionmeddrapt
serious
patient_reaction_reactionoutcome
receivedate
```

This helps ensure that the analysis is performed on the expected data structure.

---

## 3. Perform Safety Analysis

The application converts raw records into structured evidence.

### Case-level analysis

For the current sample:

```text
Total unique cases:       1,024
Serious cases:            1,023
Non-serious cases:            1
Unknown seriousness:          0
Serious cases:             99.9%
```

### Demographic analysis

The system analyzes patient age and sex distributions.

Example:

```text
Age 75+       → 408
Age 65–74     → 267
Age 45–64     → 204
Female        → 503
Male          → 493
```

### Geographic analysis

The system also summarizes the reported countries/regions.

Example:

```text
EU                 → 325
United Kingdom     → 278
France             → 187
Canada              → 55
Italy               → 52
```

---

# 🔎 4. Identify Frequently Reported Reactions

GENAR AI identifies the most frequently reported reaction terms in the dataset.

For the current sample:

| Reaction             | Reports |
| -------------------- | ------: |
| Acute kidney injury  |      22 |
| Drug ineffective     |      12 |
| Cerebral haemorrhage |       7 |
| Hyponatraemia        |       6 |
| Cholestasis          |       6 |
| Hypokalaemia         |       6 |
| Hepatic cytolysis    |       5 |
| Drug interaction     |       5 |
| Joint swelling       |       5 |
| Muscle spasms        |       4 |

### Important

These numbers represent **reported frequencies**.

They do **not** automatically mean that the drug caused the event.

GENAR AI explicitly instructs the LLM not to make unsupported causal claims.

---

# 📊 5. Analyze Reaction Outcomes

The application also summarizes reported reaction outcomes.

Example:

```text
Recovered/resolved                    → 1,347
Unknown                               → 1,135
Not recovered/not resolved/ongoing    →   569
Recovering/resolving                  →   420
Fatal                                 →   137
Recovered/resolved with sequelae      →    34
```

A case may contain multiple reactions, therefore outcome records can be greater than the number of unique cases.

---

# 🤖 6. Evidence-Grounded AI Generation

After analysis, GENAR AI creates a structured evidence object.

Conceptually:

```text
Raw Dataset
    ↓
Structured Evidence
    ↓
Controlled Prompt
    ↓
LLM
    ↓
Safety Narrative
```

The AI is **not given permission to freely invent a report**.

The prompt contains explicit safety controls.

### AI Rules

The model is instructed to:

* Use only supplied evidence
* Preserve supplied numerical values
* Avoid fabricated patient information
* Avoid unsupported clinical conclusions
* Avoid causal claims based only on frequency
* Distinguish observations from conclusions
* Mention missing information
* Mention important limitations
* State when evidence is insufficient

This makes the generated narrative more controlled and traceable to the underlying analysis.

---

# 📝 Example

Suppose the dataset contains:

```text
Acute kidney injury → 22 reports
```

A normal uncontrolled AI system might incorrectly say:

> The drug causes acute kidney injury.

GENAR AI is designed to produce a safer interpretation:

```text
Acute kidney injury was the most frequently reported
reaction term, with 22 reports in the analyzed dataset.
This reporting frequency does not establish causality.
```

This distinction is one of the important design principles of the project.

---

# 📄 Generated PADER-Style Report

The AI-generated report contains the following sections:

```text
1. Executive Summary
2. Case Overview
3. Patient Demographics
4. Seriousness Analysis
5. Reported Reactions
6. Reaction Outcomes
7. Important Safety Signals
8. Benefit-Risk Discussion
9. Limitations
```

The final report can be reviewed and downloaded from the application.

---

# 🖥️ Application Workflow

The Streamlit application provides a simple workflow:

```text
        ┌─────────────────────┐
        │   Upload ICSR Data   │
        └──────────┬──────────┘
                   ↓
        ┌─────────────────────┐
        │ Dataset Validation  │
        └──────────┬──────────┘
                   ↓
        ┌─────────────────────┐
        │ Safety Analysis     │
        │ • Cases             │
        │ • Demographics      │
        │ • Reactions         │
        │ • Outcomes          │
        └──────────┬──────────┘
                   ↓
        ┌─────────────────────┐
        │ Structured Evidence │
        └──────────┬──────────┘
                   ↓
        ┌─────────────────────┐
        │ Controlled LLM      │
        │ Generation          │
        └──────────┬──────────┘
                   ↓
        ┌─────────────────────┐
        │ PADER-Style Report  │
        └─────────────────────┘
```

---

# 🧩 Project Architecture

```text
genar-ai-challenge/
│
├── app.py
│
├── data/
│   └── Bisoprolol_icsr_sample_1068rows.xlsx
│
├── src/
│   ├── data_analysis.py
│   ├── pader_analysis.py
│   ├── pader_report.py
│   ├── llm_prompt.py
│   └── llm_generator.py
│
├── requirements.txt
└── .gitignore
```

### Main components

**`data_analysis.py`**

Handles dataset loading and validation.

**`pader_analysis.py`**

Creates structured safety evidence from the dataset.

**`pader_report.py`**

Builds the PADER report structure from analyzed evidence.

**`llm_prompt.py`**

Creates the controlled prompt used for narrative generation.

**`llm_generator.py`**

Connects the application to the configured LLM and generates the final narrative.

**`app.py`**

Provides the Streamlit user interface.

---

# 🛠️ Tech Stack

* **Python**
* **Pandas**
* **OpenPyXL**
* **Streamlit**
* **Google GenAI / LLM integration**
* **OpenAI-compatible LLM integration**
* **python-dotenv**
* **Git**
* **GitHub**

---

# ▶️ Run the Project Locally

### 1. Clone the repository

```bash
git clone https://github.com/ujjwalgupta4078/genar-ai-challenge.git
cd genar-ai-challenge
```

### 2. Create virtual environment

```bash
python -m venv .venv
```

### 3. Activate it on Windows

```bash
.venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=your_model_here
```

Use the environment variables required by the configured LLM provider.

### 6. Start the application

```bash
streamlit run app.py
```

Open:

```text
http://localhost:8501
```

---

# 🔐 Security

API keys and environment variables must not be committed to GitHub.

The project `.gitignore` excludes:

```text
.env
.env.*
.venv/
__pycache__/
*.pyc
report_output.md
*.pdf
```

---

# ⚠️ Important Limitations

GENAR AI is an **AI-assisted reporting prototype**.

The current dataset does not provide enough information to independently establish:

* Drug-event causality
* True clinical incidence
* Population-level risk
* Complete benefit-risk balance
* Confirmed safety signals

Reported frequencies should therefore be interpreted as observations from the supplied dataset.

The generated narrative should be reviewed by qualified pharmacovigilance professionals before being used for any real regulatory or clinical purpose.

---

# 🎯 Project Goal

The long-term goal of GENAR AI is to demonstrate how **structured safety-data analysis + controlled AI generation** can support pharmacovigilance reporting workflows while maintaining a strong focus on:

```text
Accuracy
   +
Evidence Grounding
   +
Transparency
   +
Safety
   +
Human Review
```

---

## 👨‍💻 Project

**GENAR AI — Pharmacovigilance Safety Report Generator**

Built as an AI-assisted pharmacovigilance reporting prototype.
