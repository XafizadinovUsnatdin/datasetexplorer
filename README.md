# 📊 Dataset Explorer AI

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40%2B-FF4B4B.svg)](https://streamlit.io/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-150458.svg)](https://pandas.pydata.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
An interactive, user-friendly exploratory data analysis (EDA) and experiment tracking dashboard built with **Streamlit** and **Pandas**.

**Dataset Explorer AI** is designed for data analysts, ML practitioners, students, and engineers who need deep, reliable insights into tabular data without altering or corrupting the raw source. It handles everything from detecting invisible whitespace corruptions to comparing machine learning experiment summaries with strict scientific rigor.

---

## 🚀 Key Highlights & Philosophy

* 🗂️ **Modern Tabbed Architecture**: Seamless navigation across 4 dedicated tabs — Single Dataset EDA, CSV Version Diffing, ML Experiment Comparisons, and Guided Methodology.
* ⚡ **1-Click Demo Datasets**: Test all tabs instantly on Streamlit Cloud without uploading files (Superstore sales data, BEFORE/AFTER CSVs, and M4C5 JSON summaries).
* 🩺 **Data Health Score (0–100)**: Instant overall dataset cleanliness metric combining missing cells, spaces-only strings, duplicates, and statistical outliers into an actionable grade.
* 🛡️ **Zero Data Corruption**: Analysis is 100% non-destructive. Raw CSV files are never modified, overwritten, or implicitly trimmed.
* 👁️ **Hidden Anomaly Detection**: Uncovers "invisible" issues that standard pandas checks overlook—such as spaces-only strings (`"   "`) masquerading as empty cells.
* 📐 **Rigorous Statistical Guards**: Automatic $1.5 \times \text{IQR}$ outlier detection with Altair interactive boxplots, MinMax, Z-score previews, and actionable remediation advice.
* 📄 **Executive Summary Report Export**: Download a comprehensive markdown summary of all 8 EDA modules and quality health indicators in one click.
* 🔄 **Dataset Version Diffing (BEFORE vs AFTER)**: Compare two CSV versions to trace schema changes (added/removed columns), cell-level missingness shifts, and row arrivals/departures by unique ID.
* 🧪 **Machine Learning Experiment Compare (M4C5)**: Compare two ML experiment summaries (JSON) with automatic context integrity checks, F1 / Precision / Recall deltas, and overfitting gap analysis.

---

## 🛠️ App Tour: 10 Integrated Modules

### 1. 📂 Intelligent File Ingestion
- Upload any CSV up to 5 MB with automatic delimiter detection (comma `,` or semicolon `;`).
- Built-in guards reject zero-byte files, invalid extensions, or malformed payloads with actionable guidance.

### 2. 📋 Comprehensive Overview & Preview
- Real-time row, column, memory, and duplicate row calculations across the full dataset.
- Interactive 100-row preview with clean column pagination.

### 3. 🔍 Column Health & Invisible Whitespace Detection
- Displays Pandas `dtype`, missing count (`NaN`), and missing percentage for every column.
- **Spaces-Only Counter**: Identifies cells containing only spaces (e.g., `"   "`), which humans perceive as empty but code treats as valid non-null strings.
- Dedicated filtering toggles to inspect problematic rows without touching the rest of the dataset.

### 4. 📊 Category Aggregation & Top-20 Altair Chart
- Group any numerical metric by categorical features.
- Altair horizontal bar chart sorted descending, paired with an exact tabular breakdown.
- Handles groups with all-missing values safely by rendering `"No data"` rather than misleading zeroes.

### 5. 🔬 Numeric Value Inspection & $1.5 \times \text{IQR}$ Outliers
- Computes $Q_1$ (25th percentile), $Q_3$ (75th percentile), and $\text{IQR} = Q_3 - Q_1$.
- Flags records outside $[Q_1 - 1.5\text{IQR}, \; Q_3 + 1.5\text{IQR}]$ with a red-accented interactive boxplot.
- Live scaling preview: compares raw values against MinMax ($[0, 1]$) and Standardized ($Z = (x - \mu)/\sigma$).

### 6. 📈 Distribution Analysis & Advanced Statistics
- Dynamic histograms with configurable bin counts.
- Visual reference lines for **Mean** (orange dashed) and **Median** (green dashed).
- Comprehensive statistical metrics: Mean, Median, Std Dev, Variance, Min, Max, Range, plus **Skewness** and **Kurtosis** explanations.

### 7. 🔗 Correlation Matrix & Interactive Heatmap
- Pearson ($r$) and Spearman rank correlations across all numerical attributes.
- Interactive color-graded heatmap ($-1.0$ to $+1.0$) with in-cell coefficient labels.
- Dual-variable Scatter Plot explorer with category-based hue segmentation.

### 8. 🎯 Feature Selection & ML Readiness
- Target variable correlation ranking to isolate strong, moderate, and weak predictors.
- **Multicollinearity Detector**: Flags feature pairs with $|r| \ge 0.85$ to prevent model distortion.
- Clean export: download the selected optimal feature subset as a model-ready CSV.

### 9. 🔄 CSV Version Comparison (BEFORE vs AFTER)
- Upload baseline and modified CSV files side-by-side.
- Summary cards tracking net changes ($\Delta$) in rows, columns, and missing cells.
- Deep diffing:
  - Added (**`+`**) and Removed (**`−`**) columns.
  - Column-by-column missingness shifts.
  - Record-level tracking via primary ID: accurately counts arriving and departing records regardless of row order.

### 10. 🧪 ML Experiment Summary Comparison (M4C5)
- Upload two experiment summary JSONs (`Experiment A: Baseline` vs `Experiment B: Modified`).
- **Context Integrity Status**:
  - 🟢 **Same recorded conditions**: All 8 context fields match (`dataset_id`, `split_id`, `target`, `positive_class`, `features`, `threshold`, `seed`, `evaluation_split = "validation"`).
  - 🟡 **Conditions differ**: Evaluation splits or parameters differ (e.g., `train` vs `validation`).
  - 🔴 **Insufficient context**: Essential metadata omitted.
- **Core Metrics**: F1, Precision, and Recall delta cards ($\Delta = B - A$).
- **Hyperparameter Diff**: Tracks `model`, `penalty`, and regularization parameter `C`.
- **Train − Validation F1 Gap**: Computes $(train\_f1 - f1)$ with strict evaluation split guards.

---

## ⚡ Quick Start: Running Locally

### 1. Clone the repository
```bash
git clone https://github.com/XafizadinovUsnatdin/datasetexplorer.git
cd datasetexplorer
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch Streamlit
```bash
streamlit run app.py
```
The app will automatically open in your default browser at `http://localhost:8501`.

> 💡 **Windows Users**: You can also double-click `run_app.bat` to launch the app with a single click!

---

## ☁️ How to Deploy on Streamlit Community Cloud

Deploying this app to the public web takes less than 2 minutes:

1. **Push your code to GitHub**: Ensure all files (`app.py`, `requirements.txt`, etc.) are committed to your repository.
2. **Go to Streamlit Cloud**: Visit [share.streamlit.io](https://share.streamlit.io/) and sign in with your GitHub account.
3. **Click "New app"**:
   - **Repository**: `XafizadinovUsnatdin/datasetexplorer`
   - **Branch**: `main`
   - **Main file path**: `app.py`
4. **Click "Deploy!"**: Streamlit will automatically read `requirements.txt`, build the container, and give you a live shareable URL!

---

## 📦 Project Structure

```text
├── .streamlit/
│   └── config.toml             # Streamlit visual theme configuration
├── app.py                      # Main application source code
├── requirements.txt            # Python dependencies (Streamlit, Pandas, NumPy, Altair)
├── .gitignore                  # Git ignore rules for clean repo maintenance
├── run_app.bat                 # Windows one-click desktop launcher
├── checks.txt                  # Comprehensive verification & test suite report (11/11 passed)
├── README.md                   # Project documentation & user guide
│
├── Sample CSV Datasets:
│   ├── M3C4_BEFORE.csv          # Baseline test CSV
│   ├── M3C4_AFTER.csv           # Modified test CSV (added/removed columns & rows)
│   ├── M3C4_REORDERED_BEFORE.csv# Order-invariance validation test
│   ├── M3C4_DUPLICATE_ID.csv    # Duplicate ID guard test
│   ├── M3C4_TEXT_IDS.csv        # Text ID and string missingness test
│   └── superstore_cleaned.csv   # Large real-world retail dataset
│
└── Sample JSON Experiment Runs:
    ├── M4C5_RUN_A.json          # Baseline experiment summary
    ├── M4C5_RUN_B.json          # Modified experiment summary (higher C, improved F1)
    ├── M4C5_CHALLENGE.json      # Train-split trap test
    ├── M4C5_MISSING_CONTEXT.json# Missing context guard test
    └── M4C5_CHANGED_SPLIT.json  # Mismatched split test
```

---

## 🧪 Quality Assurance & Testing

All core calculation engines, statistical boundaries, and edge cases are verified by dedicated automated test suites:
- `test_compare_logic.py`
- `test_m3c4_suite.py`
- `test_m4c5_logic.py`

Refer to [checks.txt](checks.txt) for the complete 11-point verification log (**11/11 automated checks passing**).

---

## 👤 Author & Acknowledgments

* **Developer**: Usnatdin Xafizadinov
* **Repository**: [https://github.com/XafizadinovUsnatdin/datasetexplorer](https://github.com/XafizadinovUsnatdin/datasetexplorer)
* **Email**: xafizadinovusnatdin@gmail.com

---

## 📄 License

This project is licensed under the [MIT License](LICENSE). Feel free to use, modify, and distribute it for personal and commercial projects.
