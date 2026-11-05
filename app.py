import streamlit as st
import pandas as pd
import numpy as np
import base64
import os
import io
import json
import math

icon_path = os.path.join(os.path.dirname(__file__), "assets", "icon.svg")

icon_b64 = ""
if os.path.exists(icon_path):
    with open(icon_path, "rb") as f:
        icon_b64 = base64.b64encode(f.read()).decode("utf-8")

# Configure page settings
st.set_page_config(
    page_title="Dataset Explorer AI",
    page_icon=icon_path if os.path.exists(icon_path) else "📊",
    layout="wide"
)
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }

    .stApp {
        background-color: #ffffff;
    }

    /* Main Header Card */
    .hero-banner {
        background: linear-gradient(135deg, #f0f4ff 0%, #ffffff 100%);
        border: 1px solid #dbeafe;
        border-radius: 16px;
        padding: 24px 28px;
        margin-bottom: 24px;
        box-shadow: 0 4px 18px rgba(5, 55, 255, 0.04);
    }
    .hero-badge {
        display: inline-block;
        background-color: #0537ff;
        color: #ffffff;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        padding: 4px 12px;
        border-radius: 20px;
        margin-bottom: 10px;
    }
    .hero-title {
        color: #0b192c;
        font-size: 32px;
        font-weight: 800;
        margin: 0 0 6px 0;
        line-height: 1.2;
    }
    .hero-desc {
        color: #475569;
        font-size: 15px;
        line-height: 1.6;
        margin: 0;
    }

    /* Section Headings */
    h1, h2, h3 {
        color: #0537ff !important;
        font-weight: 700 !important;
        letter-spacing: -0.01em;
    }

    /* Metric Cards */
    [data-testid="stMetric"] {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 14px 18px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.02);
        transition: all 0.2s ease-in-out;
    }
    [data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(5, 55, 255, 0.08);
        border-color: #bfdbfe;
    }
    [data-testid="stMetricLabel"] {
        font-size: 12px !important;
        font-weight: 600 !important;
        color: #64748b !important;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }
    [data-testid="stMetricValue"] {
        font-size: 26px !important;
        font-weight: 800 !important;
        color: #0537ff !important;
    }

    /* Buttons */
    .stButton>button {
        background-color: #0537ff;
        color: #ffffff;
        border-radius: 8px;
        border: 1px solid #0537ff;
        font-weight: 600;
        padding: 10px 20px;
        box-shadow: 0 2px 6px rgba(5, 55, 255, 0.18);
        transition: all 0.2s ease-in-out;
    }
    .stButton>button:hover {
        background-color: #032bc7;
        color: #ffffff;
        border-color: #032bc7;
        box-shadow: 0 4px 12px rgba(5, 55, 255, 0.28);
        transform: translateY(-1px);
    }

    /* File Uploader styling */
    [data-testid="stFileUploader"] {
        background: #fcfdff;
        border: 2px dashed #93c5fd;
        border-radius: 14px;
        padding: 18px 22px;
        margin-bottom: 20px;
        transition: border-color 0.2s ease;
    }
    [data-testid="stFileUploader"]:hover {
        border-color: #0537ff;
    }

    /* Dataframe tables */
    [data-testid="stDataFrame"] {
        border-radius: 10px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
        animation: fadeInUp 0.4s ease forwards;
    }

    /* Animation Keyframes */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(8px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes pulseGlowGreen {
        0%, 100% {
            box-shadow: 0 0 0 0 rgba(17, 102, 68, 0.15);
            border-color: #bdddc9;
        }
        50% {
            box-shadow: 0 0 8px 1px rgba(17, 102, 68, 0.32);
            border-color: #116644;
        }
    }

    @keyframes pulseGlowRed {
        0%, 100% {
            box-shadow: 0 0 0 0 rgba(146, 51, 62, 0.15);
            border-color: #ebbdc2;
        }
        50% {
            box-shadow: 0 0 8px 1px rgba(146, 51, 62, 0.32);
            border-color: #92333e;
        }
    }

    @keyframes shimmerBar {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }

    /* Animated Components */
    .hero-banner {
        animation: fadeInUp 0.45s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
    .hero-badge {
        background: linear-gradient(90deg, #0537ff 0%, #3b82f6 50%, #0537ff 100%);
        background-size: 200% auto;
        animation: shimmerBar 5s linear infinite;
    }

    /* Workflow Steps Ribbon */
    .steps-ribbon {
        display: flex;
        gap: 8px;
        flex-wrap: wrap;
        margin: 14px 0 22px 0;
        padding: 8px 10px;
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        animation: fadeInUp 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
    .step-chip {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: #ffffff;
        color: #334155;
        border: 1px solid #cbd5e1;
        border-radius: 8px;
        padding: 6px 12px;
        font-size: 12px;
        font-weight: 600;
        transition: all 0.25s ease;
        cursor: default;
    }
    .step-chip:hover {
        border-color: #0537ff;
        color: #0537ff;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(5, 55, 255, 0.10);
    }
    .step-chip .step-num {
        display: inline-grid;
        place-items: center;
        width: 18px;
        height: 18px;
        border-radius: 50%;
        background: #eff6ff;
        color: #0537ff;
        font-size: 10px;
        font-weight: 800;
    }

    /* Metric Cards Hover & Transitions */
    [data-testid="stMetric"] {
        transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.25s cubic-bezier(0.16, 1, 0.3, 1), border-color 0.25s ease;
        animation: fadeInUp 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
    [data-testid="stMetric"]:hover {
        transform: translateY(-4px) scale(1.01);
        box-shadow: 0 8px 22px rgba(5, 55, 255, 0.12);
        border-color: #93c5fd;
    }

    /* File uploader hover */
    [data-testid="stFileUploader"] {
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        animation: fadeInUp 0.4s ease forwards;
    }
    [data-testid="stFileUploader"]:hover {
        border-color: #0537ff;
        background: #f8faff;
        box-shadow: 0 6px 20px rgba(5, 55, 255, 0.08);
    }

    /* Comparison Badges */
    .badge-added {
        background-color: #edf8f1;
        color: #116644;
        border: 1px solid #bdddc9;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: 700;
        display: inline-flex;
        align-items: center;
        gap: 5px;
        animation: pulseGlowGreen 3.5s infinite ease-in-out;
        transition: transform 0.2s ease;
    }
    .badge-added:hover {
        transform: scale(1.04);
    }

    .badge-removed {
        background-color: #fff0f1;
        color: #92333e;
        border: 1px solid #ebbdc2;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: 700;
        display: inline-flex;
        align-items: center;
        gap: 5px;
        animation: pulseGlowRed 3.5s infinite ease-in-out;
        transition: transform 0.2s ease;
    }
    .badge-removed:hover {
        transform: scale(1.04);
    }

    .badge-changed {
        background-color: #fff7e9;
        color: #825212;
        border: 1px solid #efc879;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: 700;
        display: inline-flex;
        align-items: center;
        gap: 5px;
        transition: transform 0.2s ease;
    }
    .badge-changed:hover {
        transform: scale(1.04);
    }

    .badge-unchanged {
        background-color: #f1f5f9;
        color: #475569;
        border: 1px solid #cbd5e1;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: 700;
        display: inline-flex;
        align-items: center;
        gap: 5px;
        transition: transform 0.2s ease;
    }
    .badge-unchanged:hover {
        transform: scale(1.04);
    }

    /* Calculation Formula Explainer Card */
    .math-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-left: 4px solid #0537ff;
        border-radius: 10px;
        padding: 14px 18px;
        margin: 12px 0 16px 0;
        animation: fadeInUp 0.4s ease forwards;
    }
    .math-card-title {
        color: #0537ff;
        font-size: 14px;
        font-weight: 700;
        margin: 0 0 6px 0;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .math-card-desc {
        color: #475569;
        font-size: 13px;
        line-height: 1.5;
        margin: 0 0 8px 0;
    }
    .math-formula-box {
        background: #ffffff;
        border: 1px solid #cbd5e1;
        border-radius: 6px;
        padding: 8px 12px;
        font-family: Consolas, monospace;
        font-size: 12px;
        color: #0b192c;
    }
    
    /* Data Health Score Card */
    .health-card {
        border-radius: 14px;
        padding: 20px 24px;
        margin-bottom: 22px;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.03);
        transition: all 0.25s ease;
    }
    .health-pill {
        background: #ffffff;
        border: 1px solid #cbd5e1;
        border-radius: 8px;
        padding: 6px 12px;
        font-size: 12px;
        color: #334155;
        display: inline-flex;
        align-items: center;
        gap: 6px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
    }
    .health-pill strong {
        color: #0537ff;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        border-bottom: 2px solid #e2e8f0;
        margin-bottom: 20px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 18px;
        border-radius: 8px 8px 0 0;
        font-weight: 600;
        font-size: 14px;
        color: #475569;
        border: none;
        background: transparent;
        transition: all 0.2s ease;
    }
    .stTabs [aria-selected="true"] {
        color: #0537ff !important;
        border-bottom: 3px solid #0537ff !important;
        background: #f0f4ff !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# Helper functions
def is_missing_cell(val):
    if val is None or pd.isna(val):
        return True
    if isinstance(val, str):
        return len(val.strip()) == 0
    return False

def generate_markdown_report(df, filename, total_rows, total_cols, dup_count, dup_pct, missing_count, spaces_count, health_score, health_status):
    numeric_cols = list(df.select_dtypes(include=[np.number]).columns)
    cat_cols = list(df.select_dtypes(include=["object"]).columns)
    
    report = f"""# 📊 Dataset Explorer AI - Executive EDA Summary Report

- **Filename:** `{filename}`
- **Generated on:** `2026-11-05`
- **Platform:** [Dataset Explorer AI](https://github.com/XafizadinovUsnatdin/datasetexplorer)

---

## 🩺 1. Data Health Score & Cleanliness Overview
- **Overall Quality Score:** **{health_score} / 100**
- **Status Verdict:** {health_status}
- **Total Rows:** {total_rows:,}
- **Total Columns:** {total_cols}
- **Duplicate Rows:** {dup_count:,} ({dup_pct:.2f}%)
- **Missing Cells (NaN):** {missing_count:,}
- **Spaces-Only Cells ("   "):** {spaces_count:,}

---

## 📋 2. Column Classification
- **Numeric Features ({len(numeric_cols)}):** `{', '.join(numeric_cols) if numeric_cols else 'None'}`
- **Categorical / Text Features ({len(cat_cols)}):** `{', '.join(cat_cols) if cat_cols else 'None'}`

---

## 💡 3. Actionable Recommendations
1. **Missing & Invisible Spaces**: Treat spaces-only strings ("   ") as missing values before model ingestion to prevent silent string conversions.
2. **Outlier Remediation**: Review records outside $[Q_1 - 1.5\\text{IQR}, Q_3 + 1.5\\text{IQR}]$ with domain experts. Apply Winsorization or log-scaling if training distance-based algorithms.
3. **Multicollinearity Elimination**: Drop or combine feature pairs with $|r| \\ge 0.85$ to stabilize regression coefficients.

*Report automatically generated by Dataset Explorer AI.*
"""
    return report

def run_single_eda_pipeline(df, file_name, file_size_mb):
    total_rows = len(df)
    total_columns = len(df.columns)
    # Extra exact duplicate rows excluding the first occurrence
    extra_duplicates = int(df.duplicated(keep="first").sum())

    # -------------------------------------------------------------
    # 1. Dataset Overview
    # -------------------------------------------------------------
    st.header("1. Dataset Overview")
    with st.container():
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(label="Total Rows", value=f"{total_rows:,}")
        with col2:
            st.metric(label="Total Columns", value=f"{total_columns:,}")
        with col3:
            st.metric(label="Extra Duplicate Rows", value=f"{extra_duplicates:,}")
        with col4:
            st.metric(label="File Size", value=f"{file_size_mb:.2f} MB")

    if extra_duplicates > 0:
        dup_pct = (extra_duplicates / total_rows) * 100
        st.warning(f"⚠️ Found **{extra_duplicates:,}** extra duplicate rows ({dup_pct:.2f}% of total rows). These are exact duplicate rows that repeat earlier records.")
    else:
        st.success("✅ No duplicate rows found in this dataset.")
    # -------------------------------------------------------------
    # Data Health Score (0-100)
    # -------------------------------------------------------------
    total_cells = total_rows * total_columns
    total_missing = int(df.isna().sum().sum())
    missing_rate = (total_missing / total_cells * 100) if total_cells > 0 else 0

    spaces_count = 0
    for col in df.select_dtypes(include=["object"]).columns:
        spaces_count += int(df[col].astype(str).str.fullmatch(r"^\s+$").sum())

    dup_rate = (extra_duplicates / total_rows * 100) if total_rows > 0 else 0

    num_cols = df.select_dtypes(include=[np.number]).columns
    total_outliers = 0
    for c in num_cols:
        vals = df[c].dropna()
        if len(vals) >= 4:
            q1 = vals.quantile(0.25)
            q3 = vals.quantile(0.75)
            iqr = q3 - q1
            low = q1 - 1.5 * iqr
            high = q3 + 1.5 * iqr
            total_outliers += int(((vals < low) | (vals > high)).sum())

    penalty_missing = min(35, missing_rate * 2.0)
    penalty_spaces = min(20, spaces_count * 2.0)
    penalty_dups = min(20, dup_rate * 1.5)
    penalty_outliers = min(15, (total_outliers / total_rows * 100) * 0.5) if total_rows > 0 else 0

    health_score = int(max(0, min(100, round(100 - (penalty_missing + penalty_spaces + penalty_dups + penalty_outliers)))))

    if health_score >= 90:
        health_badge_text = "EXCELLENT"
        health_color = "#116644"
        health_bg = "#edf8f1"
        health_border = "#bdddc9"
        health_desc = "Dataset is clean with minimal missing values and zero duplicate rows. Fully ready for exploratory analysis and ML modeling."
        health_status_full = "🟢 Excellent — Fully ready for ML modeling"
    elif health_score >= 75:
        health_badge_text = "GOOD"
        health_color = "#854d0e"
        health_bg = "#fefce8"
        health_border = "#fef08a"
        health_desc = "Overall quality is good. Inspect flagged outliers and minor missing values before production modeling."
        health_status_full = "🟡 Good — Minor cleanup recommended"
    else:
        health_badge_text = "NEEDS ATTENTION"
        health_color = "#991b1b"
        health_bg = "#fef2f2"
        health_border = "#fecaca"
        health_desc = "High missingness, invisible whitespace, or excessive outliers detected. Preprocessing and cleaning required."
        health_status_full = "🔴 Needs Attention — Data cleaning required"

    st.markdown(
        f"""
        <div class="health-card" style="background: linear-gradient(135deg, {health_bg} 0%, #ffffff 100%); border: 1.5px solid {health_border};">
            <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 14px;">
                <div>
                    <div style="font-size: 11px; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 4px;">🩺 Data Health Score & Readiness</div>
                    <div style="display: flex; align-items: baseline; gap: 10px;">
                        <span style="font-size: 38px; font-weight: 800; color: {health_color}; line-height: 1;">{health_score}</span>
                        <span style="font-size: 18px; color: #64748b; font-weight: 600;">/ 100</span>
                        <span style="background: {health_color}; color: #ffffff; padding: 3px 10px; border-radius: 12px; font-size: 12px; font-weight: 700;">{health_badge_text}</span>
                    </div>
                    <div style="font-size: 13px; color: #334155; margin-top: 6px; font-weight: 500;">{health_desc}</div>
                </div>
                <div style="display: flex; gap: 8px; flex-wrap: wrap;">
                    <div class="health-pill"><strong>{missing_rate:.1f}%</strong> missing cells ({total_missing:,})</div>
                    <div class="health-pill"><strong>{spaces_count}</strong> spaces-only cell(s)</div>
                    <div class="health-pill"><strong>{dup_rate:.1f}%</strong> duplicate rows</div>
                    <div class="health-pill"><strong>{total_outliers}</strong> statistical outlier(s)</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # -------------------------------------------------------------
    # 2. Data Preview (First 100 rows)
    # -------------------------------------------------------------
    st.header("2. Data Preview")
    preview_limit = min(100, total_rows)
    st.caption(f"Showing the first {preview_limit} row(s) out of {total_rows:,} total rows in the full dataset:")
    st.dataframe(df.head(preview_limit), use_container_width=True)

    # -------------------------------------------------------------
    # 3. Column Details & Missing Values
    # -------------------------------------------------------------
    st.header("3. Columns & Missing Values")

    with st.expander("ℹ️ How Missing Values Are Identified (Rules Explained)", expanded=False):
        st.markdown(
            """
            **Missing Value Rules Used When Reading This CSV:**
            - Standard default missing-value representations are recognized as missing (`NaN` / null) by pandas.
            - Values treated as missing include:
              - Completely blank or empty fields (e.g. `,,`).
              - Standard markers: `""`, `'#N/A'`, `'#N/A N/A'`, `'#NA'`, `'-1.#IND'`, `'-1.#QNAN'`, `'-NaN'`, `'-nan'`, `'1.#IND'`, `'1.#QNAN'`, `'<NA>'`, `'N/A'`, `'NA'`, `'NULL'`, `'NaN'`, `'None'`, `'n/a'`, `'nan'`, `'null'`.
            - Any custom text or non-empty strings not listed above are preserved as valid data.
            - All counts and percentages below are computed across the full dataset without modifying original values.
            """
        )

    col_names = list(df.columns)
    col_types = [str(df[col].dtype) for col in col_names]
    missing_counts = [int(df[col].isnull().sum()) for col in col_names]
    missing_percentages = [f"{(count / total_rows) * 100:.2f}%" for count in missing_counts]
    spaces_counts = [int(sum(1 for x in df[col] if isinstance(x, str) and x.isspace())) for col in col_names]
    total_spaces_count = sum(spaces_counts)

    columns_summary_df = pd.DataFrame({
        "Column Name": col_names,
        "Pandas Data Type": col_types,
        "Missing Count": missing_counts,
        "Missing Percentage": missing_percentages,
        "Spaces-Only Count": spaces_counts
    })

    st.dataframe(columns_summary_df, use_container_width=True)

    col_stat1, col_stat2 = st.columns(2)
    with col_stat1:
        st.metric(label="Total Ordinary Missing (NaN) Cells", value=f"{sum(missing_counts):,}")
    with col_stat2:
        st.metric(label="Total Spaces-Only Cells", value=f"{total_spaces_count:,}")

    # -------------------------------------------------------------
    # Optional Row Views (Spaces-Only & Missing Values)
    # -------------------------------------------------------------
    st.subheader("Filter Rows (Optional Views)")

    col_view1, col_view2 = st.columns(2)
    with col_view1:
        show_spaces_rows = st.checkbox(
            "🔍 Show only rows with spaces-only cells",
            value=False,
            help="Displays rows that have at least one cell containing only spaces."
        )
    with col_view2:
        show_missing_rows = st.checkbox(
            "⚠️ Show only rows with ordinary missing (NaN) values",
            value=False,
            help="Displays rows that have at least one ordinary missing/null value."
        )

    if show_spaces_rows:
        spaces_row_mask = [
            any(isinstance(val, str) and val.isspace() for val in row)
            for row in df.itertuples(index=False, name=None)
        ]
        spaces_rows_df = df[spaces_row_mask]
        spaces_rows_count = len(spaces_rows_df)

        if spaces_rows_count == 0:
            st.success("✅ **No spaces-only rows**: No rows in this dataset contain cells made only of spaces.")
        else:
            pct = (spaces_rows_count / total_rows) * 100
            st.info(f"🔍 Found **{spaces_rows_count:,}** row(s) ({pct:.2f}% of total dataset) containing at least one spaces-only cell:")
            st.dataframe(spaces_rows_df, use_container_width=True)

    if show_missing_rows:
        # Filter rows containing at least one missing value
        missing_rows_df = df[df.isna().any(axis=1)]
        missing_rows_count = len(missing_rows_df)

        if missing_rows_count == 0:
            st.success("✅ **No missing rows found**: All rows in this dataset have complete data across all columns.")
        else:
            missing_row_pct = (missing_rows_count / total_rows) * 100
            st.warning(
                f"⚠️ Found **{missing_rows_count:,}** row(s) ({missing_row_pct:.2f}% of total dataset) containing at least one missing value:"
            )
            st.dataframe(missing_rows_df, use_container_width=True)

    # -------------------------------------------------------------
    # 4. Category Summary Bar Chart
    # -------------------------------------------------------------
    st.header("4. Category Summary Bar Chart")

    # Detect numeric columns
    numeric_columns = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]

    if len(numeric_columns) == 0:
        st.warning(
            "📊 **Bar Chart Unavailable**: No usable numeric columns were detected in this dataset. "
            "A numeric column is required to calculate category totals. The dataset overview and table above remain fully operational."
        )
    else:
        col_cat_select, col_num_select = st.columns(2)

        with col_cat_select:
            categorical_candidates = [c for c in df.columns if not pd.api.types.is_numeric_dtype(df[c])]
            default_cat_index = 0
            if categorical_candidates:
                default_cat_index = df.columns.get_loc(categorical_candidates[0])

            selected_category_col = st.selectbox(
                "Select category column:",
                options=list(df.columns),
                index=default_cat_index,
                help="Choose the column used to group your data into categories."
            )

        with col_num_select:
            selected_numeric_col = st.selectbox(
                "Select numeric column to sum:",
                options=numeric_columns,
                index=0,
                help="Choose the numeric column whose values will be summed for each category."
            )

        # Calculation using the full uploaded file
        # 1. Report rows with a missing category separately
        missing_cat_mask = df[selected_category_col].isna()
        missing_cat_count = int(missing_cat_mask.sum())

        if missing_cat_count > 0:
            missing_cat_sum = df.loc[missing_cat_mask, selected_numeric_col].sum(min_count=1)
            missing_sum_display = "No data" if pd.isna(missing_cat_sum) else f"{missing_cat_sum:,.2f}"
            st.info(
                f"ℹ️ **Rows with a missing category**: **{missing_cat_count:,}** row(s) have a missing value for `{selected_category_col}`. "
                f"The sum of `{selected_numeric_col}` for these unassigned rows is **{missing_sum_display}**. "
                f"These rows are reported here separately and excluded from the category chart below."
            )

        valid_cat_df = df[~missing_cat_mask]

        if valid_cat_df.empty:
            st.warning(f"All rows in this dataset have a missing `{selected_category_col}`. Cannot generate category totals.")
        else:
            # Group by category and compute sum across full dataset without replacing missing numbers with zero
            grouped_series = valid_cat_df.groupby(selected_category_col)[selected_numeric_col].sum(min_count=1)
            summary_grouped = grouped_series.reset_index()
            sum_col_name = f"Sum of {selected_numeric_col}"
            summary_grouped.columns = [selected_category_col, sum_col_name]

            # Sort by total descending (NaN values placed at the end)
            summary_sorted = summary_grouped.sort_values(
                by=sum_col_name,
                ascending=False,
                na_position="last"
            ).reset_index(drop=True)

            total_categories = len(summary_sorted)

            # Determine top 20 categories for the chart
            is_truncated = total_categories > 20
            chart_data = summary_sorted.head(20).copy()

            if is_truncated:
                st.info(
                    f"📌 **Chart Display**: Showing the **top 20** categories (out of {total_categories:,} total categories) "
                    f"sorted by total `{selected_numeric_col}`. The table below contains all {total_categories:,} category totals."
                )
            else:
                st.caption(f"Showing all {total_categories} category totals sorted in descending order.")

            chart_df = chart_data.copy()
            chart_df[selected_category_col] = chart_df[selected_category_col].astype(str)

            st.bar_chart(
                data=chart_df,
                x=selected_category_col,
                y=sum_col_name,
                x_label=f"Category: {selected_category_col}",
                y_label=f"Aggregation: {sum_col_name}",
                use_container_width=True
            )

            st.subheader("Exact Category Totals Table")
            st.caption(f"Showing all {total_categories:,} categories from the full dataset:")

            table_display = summary_sorted.copy()
            table_display[selected_category_col] = table_display[selected_category_col].astype(str)
            table_display[sum_col_name] = table_display[sum_col_name].apply(
                lambda val: "No data" if pd.isna(val) else (f"{val:,.0f}" if isinstance(val, (int, float, np.integer, np.floating)) and float(val).is_integer() else f"{val:,.2f}")
            )

            table_display.columns = [f"Category ({selected_category_col})", f"Exact {sum_col_name}"]
            st.dataframe(table_display, use_container_width=True, hide_index=True)

    # -------------------------------------------------------------
    # 5. Inspect Numeric Values (M3C2 Upgrade)
    # -------------------------------------------------------------
    st.header("5. Inspect Numeric Values")
    st.caption("Inspect distributions, identify potential outliers using the 1.5 × IQR rule, and review flagged records.")

    # Find columns that have at least some usable numeric values
    potential_numeric_cols = []
    for c in df.columns:
        converted = pd.to_numeric(df[c], errors="coerce")
        if converted.notna().sum() > 0:
            potential_numeric_cols.append(c)

    if len(potential_numeric_cols) == 0:
        st.warning("📊 **No usable numeric columns detected in this dataset.** An inspection requires at least one numeric column.")
    else:
        selected_inspect_col = st.selectbox(
            "Select numeric column to inspect:",
            options=potential_numeric_cols,
            index=0,
            help="Choose a numeric column to view its boxplot distribution, IQR boundaries, and flagged records."
        )

        s_raw = df[selected_inspect_col]
        s_num = pd.to_numeric(s_raw, errors="coerce")
        valid_mask = s_num.notna() & np.isfinite(s_num)
        usable_series = s_num[valid_mask]
        usable_count = int(len(usable_series))
        missing_count = int(len(df) - usable_count)

        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.metric(label="Usable Values", value=f"{usable_count:,}")
        with col_m2:
            st.metric(label="Missing / Excluded Values", value=f"{missing_count:,}")

        if usable_count == 0:
            st.info("ℹ️ No usable numeric values found in the selected column.")
        elif usable_count < 4:
            st.info(f"ℹ️ Too few values ({usable_count} usable value{'s' if usable_count > 1 else ''}). At least 4 usable values are required for an IQR verdict.")
        else:
            # Calculate Q1 and Q3 using pandas' default linear quantile interpolation
            q1 = float(usable_series.quantile(0.25, interpolation="linear"))
            q3 = float(usable_series.quantile(0.75, interpolation="linear"))
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr

            # Flag strictly outside boundaries
            flagged_mask = (s_num < lower_bound) | (s_num > upper_bound)
            flagged_df = df[flagged_mask.fillna(False)]
            flag_count = int(len(flagged_df))

            # Display IQR Metrics
            col_b1, col_b2, col_b3, col_b4, col_b5 = st.columns(5)
            with col_b1:
                st.metric(label="Q1 (25%)", value=f"{q1:,.2f}")
            with col_b2:
                st.metric(label="Q3 (75%)", value=f"{q3:,.2f}")
            with col_b3:
                st.metric(label="IQR", value=f"{iqr:,.2f}")
            with col_b4:
                st.metric(label="Lower Bound", value=f"{lower_bound:,.2f}")
            with col_b5:
                st.metric(label="Upper Bound", value=f"{upper_bound:,.2f}")

            with st.expander("📐 Mathematical Formula Reference (1.5 × IQR Rule & Whiskers)", expanded=False):
                st.markdown(
                    f"""
                    - **First Quartile ($Q_1$, 25%)**: `{q1:,.2f}` (Value below which 25% of data falls)
                    - **Third Quartile ($Q_3$, 75%)**: `{q3:,.2f}` (Value below which 75% of data falls)
                    - **Interquartile Range (IQR)**: $\\text{{IQR}} = Q_3 - Q_1 = {q3:,.2f} - {q1:,.2f} = {iqr:,.2f}$
                    - **Lower Whisker Boundary**: $Q_1 - 1.5 \\times \\text{{IQR}} = {q1:,.2f} - 1.5({iqr:,.2f}) = {lower_bound:,.2f}$
                    - **Upper Whisker Boundary**: $Q_3 + 1.5 \\times \\text{{IQR}} = {q3:,.2f} + 1.5({iqr:,.2f}) = {upper_bound:,.2f}$
                    - **Outlier Rule**: Values strictly outside $[{lower_bound:,.2f}, {upper_bound:,.2f}]$ are flagged as *Needs inspection*.
                    """
                )

            # Boxplot Chart using Altair
            import altair as alt
            plot_df = pd.DataFrame({selected_inspect_col: usable_series})
            boxplot_chart = (
                alt.Chart(plot_df)
                .mark_boxplot(extent=1.5, size=50, color="#0537ff", outliers=alt.MarkConfig(color="#e11d48", size=45))
                .encode(
                    x=alt.X(f"{selected_inspect_col}:Q", title=f"Values: {selected_inspect_col}")
                )
                .properties(height=160)
            )
            st.altair_chart(boxplot_chart, use_container_width=True)

            # Flagged rows
            if flag_count == 0:
                st.success("✅ **0 values flagged**: No values fall strictly outside the 1.5 × IQR boundaries.")
            else:
                st.warning(f"⚠️ Found **{flag_count:,}** value(s) strictly outside the 1.5 × IQR boundaries ({lower_bound:.2f} – {upper_bound:.2f}):")
                st.caption("Label: **Needs inspection** (Points outside whiskers highlight unusual values for review; this does not prove a typo or justify automatic deletion).")
                st.dataframe(flagged_df, use_container_width=True)

            # Optional Bonus: Scaling Preview
            with st.expander("🔬 Optional: Preview Scaled Values (Raw, MinMax, Standard)", expanded=False):
                st.caption(
                    "ℹ️ **Preview only**. Scaling does not prove a value is correct, remove outliers or make the distribution normal. "
                    "For a model, learn scaling parameters only from train, then apply the same parameters to validation/test."
                )
                min_val = float(usable_series.min())
                max_val = float(usable_series.max())
                mean_val = float(usable_series.mean())
                std_val = float(usable_series.std(ddof=0))

                if min_val == max_val or std_val == 0:
                    st.info("ℹ️ All usable values in this column are equal. Both MinMax and Standard scaled previews are 0.000 (no variation).")
                else:
                    id_cols = [c for c in df.columns if any(k in c.lower() for k in ["id", "row", "name", "code"])]
                    selected_id_col = id_cols[0] if id_cols else None

                    minmax_vals = (usable_series - min_val) / (max_val - min_val)
                    standard_vals = (usable_series - mean_val) / std_val

                    preview_dict = {}
                    if selected_id_col:
                        preview_dict[f"Identifier ({selected_id_col})"] = df.loc[usable_series.index, selected_id_col]
                    else:
                        preview_dict["Row Index"] = usable_series.index

                    preview_dict["Raw Value"] = usable_series.apply(lambda v: f"{v:,.2f}" if float(v).is_integer() is False else f"{v:,.0f}")
                    preview_dict["MinMax"] = minmax_vals.apply(lambda v: f"{v:.3f}")
                    preview_dict["Standard (ddof=0)"] = standard_vals.apply(lambda v: f"{v:.3f}")

                    preview_df = pd.DataFrame(preview_dict)
                    st.dataframe(preview_df, use_container_width=True, hide_index=True)

    # -------------------------------------------------------------
    # 6. Distributions & Extended Statistics
    # -------------------------------------------------------------
    st.header("6. Distributions & Extended Statistics")
    st.caption("Inspect statistical distributions, histograms with mean/median markers, skewness, and kurtosis.")

    if len(potential_numeric_cols) == 0:
        st.warning("📊 No usable numeric columns detected for distribution analysis.")
    else:
        dist_col_select, dist_bins_select = st.columns([2, 1])
        with dist_col_select:
            selected_dist_col = st.selectbox(
                "Select numeric column for distribution analysis:",
                options=potential_numeric_cols,
                index=0,
                key="dist_col_selector",
                help="Choose a numeric column to view its histogram and detailed statistical profile."
            )
        with dist_bins_select:
            hist_bins = st.slider(
                "Histogram Bins (Kataklar soni):",
                min_value=5,
                max_value=60,
                value=20,
                step=5,
                key="dist_bins_slider"
            )

        s_dist_raw = df[selected_dist_col]
        s_dist_num = pd.to_numeric(s_dist_raw, errors="coerce").dropna()

        if len(s_dist_num) == 0:
            st.info("ℹ️ No usable numeric values found in the selected column.")
        else:
            mean_val = float(s_dist_num.mean())
            median_val = float(s_dist_num.median())
            std_val = float(s_dist_num.std())
            var_val = float(s_dist_num.var())
            min_val = float(s_dist_num.min())
            max_val = float(s_dist_num.max())
            range_val = max_val - min_val
            skew_val = float(s_dist_num.skew()) if len(s_dist_num) > 2 else 0.0
            kurt_val = float(s_dist_num.kurtosis()) if len(s_dist_num) > 3 else 0.0

            # Skewness classification
            if abs(skew_val) < 0.5:
                skew_badge = '<span class="badge-added">✅ Simmetrik / Normalga yaqin</span>'
                skew_desc = "Qiymatlar markaz atrofida simmetrik taqsimlangan."
            elif skew_val >= 0.5:
                skew_badge = '<span class="badge-changed">⚠️ O‘ngga qiyshaygan (Right-skewed)</span>'
                skew_desc = "Ko‘pchilik qiymatlar chapda (kichik), o‘ng tomonda uzun dum (katta qiymatlar) bor."
            else:
                skew_badge = '<span class="badge-changed">⚠️ Chapga qiyshaygan (Left-skewed)</span>'
                skew_desc = "Ko‘pchilik qiymatlar o‘ngda (katta), chap tomonda uzun dum bor."

            # 4 Metric Cards for Core Statistics
            c_s1, c_s2, c_s3, c_s4 = st.columns(4)
            with c_s1:
                st.metric("O‘rtacha (Mean)", f"{mean_val:,.2f}")
                st.caption(f"Min: {min_val:,.2f} · Max: {max_val:,.2f}")
            with c_s2:
                st.metric("Mediana (Median)", f"{median_val:,.2f}")
                st.caption(f"Oraliq (Range): {range_val:,.2f}")
            with c_s3:
                st.metric("Standart Og‘ish (Std Dev)", f"{std_val:,.2f}")
                st.caption(f"Dispersiya (Var): {var_val:,.2f}")
            with c_s4:
                st.metric("Skewness (Qiyshayish)", f"{skew_val:+.2f}")
                st.markdown(skew_badge, unsafe_allow_html=True)

            # Altair Histogram Chart
            import altair as alt
            plot_dist_df = pd.DataFrame({selected_dist_col: s_dist_num})
            hist_base = alt.Chart(plot_dist_df)
            hist_bars = (
                hist_base
                .mark_bar(color="#0537ff", opacity=0.85, cornerRadiusTopLeft=5, cornerRadiusTopRight=5)
                .encode(
                    x=alt.X(f"{selected_dist_col}:Q", bin=alt.Bin(maxbins=hist_bins), title=f"{selected_dist_col} (Oraliqlar)"),
                    y=alt.Y("count()", title="Frequency (Row Count)"),
                    tooltip=[
                        alt.Tooltip(f"{selected_dist_col}:Q", bin=alt.Bin(maxbins=hist_bins), title="Oraliq"),
                        alt.Tooltip("count()", title="Soni")
                    ]
                )
                .properties(height=280)
            )

            # Mean and Median vertical rule lines
            rule_df = pd.DataFrame([
                {"stat": "O‘rtacha (Mean)", "value": mean_val, "color": "#f97316"},
                {"stat": "Mediana", "value": median_val, "color": "#10b981"}
            ])
            stat_rules = (
                alt.Chart(rule_df)
                .mark_rule(strokeDash=[4, 4], strokeWidth=2)
                .encode(
                    x=alt.X("value:Q"),
                    color=alt.Color("color:N", scale=None)
                )
            )
            st.altair_chart(hist_bars + stat_rules, use_container_width=True)
            st.caption(f"🟠 **To‘q sariq chiziq**: O‘rtacha ({mean_val:,.2f}) · 🟢 **Yashil chiziq**: Mediana ({median_val:,.2f}). {skew_desc}")

    # -------------------------------------------------------------
    # 7. Correlation Matrix & Heatmap
    # -------------------------------------------------------------
    st.header("7. Correlation Matrix & Heatmap")
    st.caption("Explore pairwise correlations between numeric features to discover linear and monotonic relationships.")

    if len(potential_numeric_cols) < 2:
        st.info("ℹ️ Correlation analysis requires at least 2 numeric columns in the dataset.")
    else:
        df_corr_ready = df[potential_numeric_cols].apply(pd.to_numeric, errors="coerce")

        col_opt1, col_opt2 = st.columns([1, 2])
        with col_opt1:
            corr_method = st.radio(
                "Korrelyatsiya usuli:",
                options=["pearson", "spearman"],
                format_func=lambda x: "Pearson (Chiziqli)" if x == "pearson" else "Spearman (Tartibli/Monotonik)",
                horizontal=True,
                key="corr_method_radio"
            )

        corr_matrix = df_corr_ready.corr(method=corr_method).round(2)

        # Melt correlation matrix for Altair Heatmap
        corr_unpivoted = corr_matrix.reset_index().melt(
            id_vars="index",
            var_name="Feature_2",
            value_name="Correlation"
        )
        corr_unpivoted.columns = ["Feature_1", "Feature_2", "Correlation"]

        heatmap = (
            alt.Chart(corr_unpivoted)
            .mark_rect()
            .encode(
                x=alt.X("Feature_1:N", title="Feature 1", sort=None),
                y=alt.Y("Feature_2:N", title="Feature 2", sort=None),
                color=alt.Color(
                    "Correlation:Q",
                    scale=alt.Scale(domain=[-1.0, 0.0, 1.0], range=["#ef4444", "#ffffff", "#0537ff"]),
                    title="Korrelyatsiya (r)"
                ),
                tooltip=["Feature_1", "Feature_2", "Correlation"]
            )
            .properties(height=max(260, len(potential_numeric_cols) * 45))
        )

        text_layer = (
            alt.Chart(corr_unpivoted)
            .mark_text(baseline="middle", fontSize=12, fontWeight="bold")
            .encode(
                x=alt.X("Feature_1:N", sort=None),
                y=alt.Y("Feature_2:N", sort=None),
                text=alt.Text("Correlation:Q", format=".2f"),
                color=alt.condition(
                    alt.expr.abs(alt.datum.Correlation) > 0.45,
                    alt.value("#ffffff"),
                    alt.value("#0b192c")
                )
            )
        )
        st.altair_chart(heatmap + text_layer, use_container_width=True)

        # Interactive Pairwise Scatter Plot
        with st.expander("🔍 Interactive Scatter Plot (Feature Relationship Explorer)", expanded=False):
            sc_col1, sc_col2, sc_col3 = st.columns(3)
            with sc_col1:
                sc_x = st.selectbox("X o‘qi (Horizontal):", options=potential_numeric_cols, index=0, key="sc_x_col")
            with sc_col2:
                default_y_idx = 1 if len(potential_numeric_cols) > 1 else 0
                sc_y = st.selectbox("Y o‘qi (Vertical):", options=potential_numeric_cols, index=default_y_idx, key="sc_y_col")
            with sc_col3:
                cat_options = ["(None)"] + [c for c in df.columns if not pd.api.types.is_numeric_dtype(df[c])]
                sc_color = st.selectbox("Rang / Toifa (Color):", options=cat_options, index=0, key="sc_color_col")

            clean_pair_df = df[[sc_x, sc_y] + ([sc_color] if sc_color != "(None)" else [])].dropna()
            clean_pair_df[sc_x] = pd.to_numeric(clean_pair_df[sc_x], errors="coerce")
            clean_pair_df[sc_y] = pd.to_numeric(clean_pair_df[sc_y], errors="coerce")
            clean_pair_df = clean_pair_df.dropna()

            if len(clean_pair_df) > 0:
                pair_r = float(clean_pair_df[sc_x].corr(clean_pair_df[sc_y], method=corr_method))
                st.caption(f"📊 **Bog‘liqlik:** {sc_x} va {sc_y} o‘rtasida **r = {pair_r:+.2f}** (Nuqtalar soni: {len(clean_pair_df):,})")

                sc_chart_builder = alt.Chart(clean_pair_df).mark_circle(size=65, opacity=0.75)
                if sc_color != "(None)":
                    sc_chart = sc_chart_builder.encode(
                        x=alt.X(f"{sc_x}:Q", title=sc_x),
                        y=alt.Y(f"{sc_y}:Q", title=sc_y),
                        color=alt.Color(f"{sc_color}:N", title=sc_color),
                        tooltip=[sc_x, sc_y, sc_color]
                    )
                else:
                    sc_chart = sc_chart_builder.encode(
                        x=alt.X(f"{sc_x}:Q", title=sc_x),
                        y=alt.Y(f"{sc_y}:Q", title=sc_y),
                        color=alt.value("#0537ff"),
                        tooltip=[sc_x, sc_y]
                    )
                st.altair_chart(sc_chart.properties(height=300), use_container_width=True)

    # -------------------------------------------------------------
    # 8. Feature Selection & ML Readiness
    # -------------------------------------------------------------
    st.header("8. Feature Selection & ML Readiness")
    st.caption("Identify key predictive features for machine learning, detect multicollinearity hazards, and export your prepared dataset.")

    if len(potential_numeric_cols) < 2:
        st.info("ℹ️ Feature selection insights require at least 2 numeric features.")
    else:
        # 1. Target Column Selection & Correlation Ranking
        st.subheader("🎯 1. Target Variable & Feature Importance Ranking")
        target_col = st.selectbox(
            "Select Target / Label Variable for Prediction:",
            options=potential_numeric_cols,
            index=0,
            key="ml_target_selector",
            help="Model bashorat qilishi kerak bo‘lgan ustunni tanlang (masalan, Sales, Profit, Price, Score)."
        )

        other_features = [c for c in potential_numeric_cols if c != target_col]

        if other_features:
            target_corrs = []
            for feat in other_features:
                r_val = float(df_corr_ready[feat].corr(df_corr_ready[target_col]))
                if pd.notna(r_val):
                    abs_r = abs(r_val)
                    if abs_r >= 0.7:
                        strength = "Kuchli (Strong)"
                    elif abs_r >= 0.3:
                        strength = "O‘rtacha (Moderate)"
                    else:
                        strength = "Kuchsiz (Weak)"
                    target_corrs.append({
                        "Feature Name": feat,
                        "Correlation (r)": r_val,
                        "Absolute Strength (|r|)": abs_r,
                        "Impact": strength
                    })

            if target_corrs:
                ranking_df = pd.DataFrame(target_corrs).sort_values(by="Absolute Strength (|r|)", ascending=False).reset_index(drop=True)

                col_rank1, col_rank2 = st.columns([3, 2])
                with col_rank1:
                    rank_chart = (
                        alt.Chart(ranking_df)
                        .mark_bar(cornerRadiusTopRight=4, cornerRadiusBottomRight=4)
                        .encode(
                            x=alt.X("Absolute Strength (|r|):Q", title="|Correlation with Target| (Bog‘liqlik kuchi)"),
                            y=alt.Y("Feature Name:N", sort="-x", title="Feature"),
                            color=alt.Color(
                                "Correlation (r):Q",
                                scale=alt.Scale(domain=[-1, 0, 1], range=["#ef4444", "#cbd5e1", "#0537ff"]),
                                title="Yo‘nalishi (r)"
                            ),
                            tooltip=["Feature Name", "Correlation (r)", "Impact"]
                        )
                        .properties(height=max(160, len(ranking_df) * 36))
                    )
                    st.altair_chart(rank_chart, use_container_width=True)

                with col_rank2:
                    st.markdown("**Feature Reytingi Jadvali:**")
                    st.dataframe(
                        ranking_df[["Feature Name", "Correlation (r)", "Impact"]],
                        use_container_width=True,
                        hide_index=True
                    )

        # 2. Multicollinearity Detection
        st.subheader("⚠️ 2. Multikollinearlik Tekshiruvi (Multicollinearity Check)")
        st.caption("O‘zaro juda kuchli bog‘langan (|r| ≥ 0.85) mustaqil ustunlar chiziqli modellarda (Linear Regression) beqarorlikka olib kelishi mumkin.")

        high_corr_pairs = []
        for i in range(len(other_features)):
            for j in range(i + 1, len(other_features)):
                f1, f2 = other_features[i], other_features[j]
                r_pair = float(df_corr_ready[f1].corr(df_corr_ready[f2]))
                if pd.notna(r_pair) and abs(r_pair) >= 0.85:
                    high_corr_pairs.append((f1, f2, r_pair))

        if high_corr_pairs:
            for f1, f2, r_p in high_corr_pairs:
                st.warning(
                    f"⚠️ **Yuqori multikollinearlik**: `{f1}` va `{f2}` o‘rtasida **r = {r_p:+.2f}** aniqlandi. "
                    f"Ortiqcha ma'lumot (redundancy) bo‘lmasligi uchun ulardan birini tushirib qoldirish tavsiya etiladi."
                )
        else:
            st.success("✅ **Clean State**: No severe multicollinearity detected (|r| < 0.85 across independent features).")

        # 3. Export Selected Prepared Features
        st.subheader("💾 3. ML uchun Saralangan Ustunlarni Yuklab Olish (Export)")
        default_exports = [target_col]
        if other_features and target_corrs:
            default_exports += [row["Feature Name"] for _, row in ranking_df.iterrows() if row["Absolute Strength (|r|)"] >= 0.1][:5]

        export_selected_cols = st.multiselect(
            "Select features to export for ML model training:",
            options=list(df.columns),
            default=list(set(default_exports)),
            key="ml_export_multiselect",
            help="Choose desired columns to download as a clean CSV prepared for model training."
        )

        if export_selected_cols:
            export_df = df[export_selected_cols]
            csv_data = export_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label=f"📥 Download Selected {len(export_selected_cols)} Features (CSV)",
                data=csv_data,
                file_name="prepared_features_ml.csv",
                mime="text/csv",
                use_container_width=True
            )


        st.markdown("---")
        st.subheader("📄 Executive EDA Summary Report")
        st.caption("Download a comprehensive Markdown report summarizing dataset dimensions, health scores, distributions, and feature insights:")
        
        report_content = generate_markdown_report(
            df=df,
            filename=file_name,
            total_rows=total_rows,
            total_cols=total_columns,
            dup_count=extra_duplicates,
            dup_pct=dup_rate,
            missing_count=total_missing,
            spaces_count=spaces_count,
            health_score=health_score,
            health_status=health_status_full
        )
        
        st.download_button(
            label="📥 Download Executive Summary Report (Markdown .md)",
            data=report_content.encode("utf-8"),
            file_name=f"EDA_Report_{file_name.replace('.csv', '')}.md",
            mime="text/markdown",
            use_container_width=True
        )

def render_csv_diff_section():
    st.divider()
    st.header("9. Compare Two CSV Versions (BEFORE vs AFTER)")
    st.caption(
        "Compare an old (BEFORE) and new (AFTER) CSV dataset side-by-side to track changes in dimensions, "
        "missing cell counts, column schema, and record arrivals / departures."
    )

    demo_diff_c1, demo_diff_c2 = st.columns([1, 4])
    with demo_diff_c1:
        if st.button("🚀 Load Demo CSVs", key="btn_demo_diff_load", help="Load sample M3C4 Before & After CSV files"):
            st.session_state["use_demo_diff"] = True
            st.rerun()
    with demo_diff_c2:
        if st.session_state.get("use_demo_diff", False):
            if st.button("✖️ Clear Demo", key="btn_demo_diff_clear"):
                st.session_state["use_demo_diff"] = False
                st.rerun()


    col_u1, col_u2 = st.columns(2)
    with col_u1:
        st.markdown("#### 📁 BEFORE (Old File)")
        before_file = st.file_uploader(
            "Upload BEFORE CSV:",
            type=["csv"],
            key="compare_before_uploader",
            help="Upload the baseline / original CSV version."
        )
        if before_file:
            st.caption(f"📄 **Filename:** `{before_file.name}` ({before_file.size / 1024:.1f} KB)")

    with col_u2:
        st.markdown("#### 📁 AFTER (New File)")
        after_file = st.file_uploader(
            "Upload AFTER CSV:",
            type=["csv"],
            key="compare_after_uploader",
            help="Upload the modified / updated CSV version."
        )
        if after_file:
            st.caption(f"📄 **Filename:** `{after_file.name}` ({after_file.size / 1024:.1f} KB)")

    is_demo_diff = st.session_state.get("use_demo_diff", False) and (before_file is None) and (after_file is None)
    if is_demo_diff:
        st.info("ℹ️ **Sample test files active:** `M3C4_BEFORE.csv` and `M3C4_AFTER.csv`. Uploading your own files will replace them immediately.")

    if (before_file is None or after_file is None) and not is_demo_diff:
        if before_file is None and after_file is None:
            st.info("ℹ️ Upload both a **BEFORE** file and an **AFTER** file above to view the version comparison.")
        elif before_file is not None and after_file is None:
            st.warning("⚠️ Please upload the **AFTER (new)** file to proceed with comparison.")
        elif before_file is None and after_file is not None:
            st.warning("⚠️ Please upload the **BEFORE (old)** file to proceed with comparison.")
    else:
        if is_demo_diff:
            df_b = pd.read_csv("M3C4_BEFORE.csv", dtype=str, keep_default_na=False, encoding="utf-8")
            df_a = pd.read_csv("M3C4_AFTER.csv", dtype=str, keep_default_na=False, encoding="utf-8")
        else:
            # Read both files keeping literal string values and leading zeros
            try:
                before_file.seek(0)
                try:
                    df_b = pd.read_csv(before_file, dtype=str, keep_default_na=False, encoding="utf-8")
                except UnicodeDecodeError:
                    before_file.seek(0)
                    df_b = pd.read_csv(before_file, dtype=str, keep_default_na=False, encoding="latin1")

                after_file.seek(0)
                try:
                    df_a = pd.read_csv(after_file, dtype=str, keep_default_na=False, encoding="utf-8")
                except UnicodeDecodeError:
                    after_file.seek(0)
                    df_a = pd.read_csv(after_file, dtype=str, keep_default_na=False, encoding="latin1")
            except Exception as e:
                st.error(f"❌ Error reading comparison CSV files: {e}")
                df_b = None
                df_a = None

        if df_b is not None and df_a is not None:
            # Calculate summary metrics across every row
            b_rows, a_rows = len(df_b), len(df_a)
            d_rows = a_rows - b_rows

            b_cols, a_cols = len(df_b.columns), len(df_a.columns)
            d_cols = a_cols - b_cols

            b_miss = sum(1 for c in df_b.columns for v in df_b[c] if is_missing_cell(v))
            a_miss = sum(1 for c in df_a.columns for v in df_a[c] if is_missing_cell(v))
            d_miss = a_miss - b_miss

            # Direction Banner
            st.markdown(
                f"""
                <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 12px 18px; margin: 12px 0 20px 0; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px;">
                    <div>
                        <span style="font-size: 13px; font-weight: 700; color: #475569;">Comparison Direction:</span>
                        <span style="font-family: monospace; font-size: 13px; font-weight: 600; color: #0b192c; margin-left: 6px;">BEFORE (<b>{before_file.name}</b>) ➔ AFTER (<b>{after_file.name}</b>)</span>
                    </div>
                    <div>
                        <span style="font-size: 12px; color: #64748b;">Formula: <b>Δ = AFTER − BEFORE</b></span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Three Top Summary Cards
            c1, c2, c3 = st.columns(3)

            with c1:
                row_delta_str = f"{d_rows:+d} net rows" if d_rows != 0 else "0 net rows"
                st.metric(
                    label="Row Count",
                    value=f"{b_rows:,} → {a_rows:,}",
                    delta=row_delta_str,
                    delta_color="off"
                )
                if d_rows > 0:
                    st.markdown(f'<span class="badge-added">+ Added ({d_rows:+d})</span>', unsafe_allow_html=True)
                elif d_rows < 0:
                    st.markdown(f'<span class="badge-removed">− Removed ({d_rows:+d})</span>', unsafe_allow_html=True)
                else:
                    st.markdown('<span class="badge-unchanged">Unchanged (0)</span>', unsafe_allow_html=True)

            with c2:
                col_delta_str = f"{d_cols:+d} net columns" if d_cols != 0 else "0 net columns"
                st.metric(
                    label="Column Count",
                    value=f"{b_cols:,} → {a_cols:,}",
                    delta=col_delta_str,
                    delta_color="off"
                )
                if d_cols > 0:
                    st.markdown(f'<span class="badge-added">+ Added ({d_cols:+d})</span>', unsafe_allow_html=True)
                elif d_cols < 0:
                    st.markdown(f'<span class="badge-removed">− Removed ({d_cols:+d})</span>', unsafe_allow_html=True)
                else:
                    st.markdown('<span class="badge-unchanged">Unchanged (0)</span>', unsafe_allow_html=True)

            with c3:
                miss_delta_str = f"{d_miss:+d} net missing" if d_miss != 0 else "0 net missing"
                st.metric(
                    label="Missing Cells (Whole Table)",
                    value=f"{b_miss:,} → {a_miss:,}",
                    delta=miss_delta_str,
                    delta_color="off"
                )
                if d_miss < 0:
                    st.markdown(f'<span class="badge-added">Reduced ({d_miss:+d})</span>', unsafe_allow_html=True)
                elif d_miss > 0:
                    st.markdown(f'<span class="badge-removed">Increased ({d_miss:+d})</span>', unsafe_allow_html=True)
                else:
                    st.markdown('<span class="badge-unchanged">Unchanged (0)</span>', unsafe_allow_html=True)

            st.caption(
                "ℹ️ *Note: Missing cells include empty strings and whitespace-only cells. Numerical/string 0 and literal 'NA' / 'null' are treated as valid values. "
                "Delta is calculated as NEW − OLD. Color describes a difference, not data quality.*"
            )

            if d_rows == 0 and d_cols == 0 and d_miss == 0 and list(df_b.columns) == list(df_a.columns) and df_b.equals(df_a):
                st.success("✅ **Identical Datasets**: All rows, columns, and cell values are identical between BEFORE and AFTER.")

            with st.expander("📐 Mathematical Breakdown of Calculations (Delta vs Arrivals/Departures)", expanded=False):
                st.markdown(
                    f"""
                    - **Net Row Change**: $\\Delta \\text{{Rows}} = \\text{{AFTER}} - \\text{{BEFORE}} = {a_rows} - {b_rows} = {d_rows:+d}$
                    - **Net Column Change**: $\\Delta \\text{{Cols}} = \\text{{AFTER}} - \\text{{BEFORE}} = {a_cols} - {b_cols} = {d_cols:+d}$
                    - **Net Missing Cells**: $\\Delta \\text{{Missing}} = \\text{{AFTER}} - \\text{{BEFORE}} = {a_miss} - {b_miss} = {d_miss:+d}$
                    - **Why Net Rows $\\ne$ Added Records**:
                      Net row count indicates overall dataset volume, but hides simultaneous arrivals and departures:
                      $$\\Delta \\text{{Rows}} = \\text{{Added Records}} - \\text{{Removed Records}}$$
                      *Example*: If 3 records arrive and 2 records depart, the net row delta is $+1$, but **5 records** actually changed. A unique, non-blank ID is required to reveal the true arrivals ($S_{{after}} \\setminus S_{{before}}$) and departures ($S_{{before}} \\setminus S_{{after}}$).
                    """
                )

            # Collapsible 1: Column Schema Changes
            with st.expander("🔍 Column Schema Changes (Added & Removed Columns)", expanded=True):
                added_cols = [c for c in df_a.columns if c not in df_b.columns]
                removed_cols = [c for c in df_b.columns if c not in df_a.columns]
                common_cols = [c for c in df_b.columns if c in df_a.columns]

                if not added_cols and not removed_cols:
                    st.info(f"ℹ️ **Unchanged**: All {len(common_cols)} columns match exactly between BEFORE and AFTER.")
                else:
                    col_sch1, col_sch2, col_sch3 = st.columns(3)
                    with col_sch1:
                        st.markdown(f"**Added Columns ({len(added_cols)}):**")
                        if added_cols:
                            for c in added_cols:
                                st.markdown(f'<span class="badge-added">+ {c}</span>', unsafe_allow_html=True)
                        else:
                            st.caption("None")
                    with col_sch2:
                        st.markdown(f"**Removed Columns ({len(removed_cols)}):**")
                        if removed_cols:
                            for c in removed_cols:
                                st.markdown(f'<span class="badge-removed">− {c}</span>', unsafe_allow_html=True)
                        else:
                            st.caption("None")
                    with col_sch3:
                        st.markdown(f"**Common Columns ({len(common_cols)}):**")
                        st.markdown(f'<span class="badge-unchanged">{len(common_cols)} common</span>', unsafe_allow_html=True)
                        st.caption(", ".join(common_cols))

            # Collapsible 2: Missing Counts in Common Columns
            with st.expander("📊 Missing Counts in Common Columns (Aligned by Name)", expanded=True):
                if not common_cols:
                    st.warning("⚠️ No common columns found between BEFORE and AFTER to compare missing counts.")
                else:
                    st.caption(
                        "ℹ️ *Why missing counts in a column can stay constant: If an existing missing record was filled but a new arrival has a missing cell, the column count remains identical even though the affected record changed. Total missing count alone does not prove all records are clean.*"
                    )
                    missing_rows = []
                    for c in common_cols:
                        b_cnt = sum(1 for v in df_b[c] if is_missing_cell(v))
                        a_cnt = sum(1 for v in df_a[c] if is_missing_cell(v))
                        diff = a_cnt - b_cnt
                        if diff < 0:
                            status = f"Reduced ({diff:+d})"
                        elif diff > 0:
                            status = f"Increased ({diff:+d})"
                        elif b_cnt > 0:
                            status = "Unchanged (with missing)"
                        else:
                            status = "0 missing"
                        missing_rows.append({
                            "Column Name": c,
                            "BEFORE Missing": b_cnt,
                            "AFTER Missing": a_cnt,
                            "Difference (Δ = AFTER − BEFORE)": f"{diff:+d}" if diff != 0 else "0",
                            "Status": status
                        })
                    st.dataframe(pd.DataFrame(missing_rows), use_container_width=True, hide_index=True)

            # Collapsible 3: Record-Level Comparison (Added & Removed Records)
            with st.expander("🆔 Record-Level Comparison (Added & Removed Records)", expanded=True):
                id_options = ["(None / Select ID Column)"] + common_cols
                default_idx = 0
                if "row_id" in common_cols:
                    default_idx = id_options.index("row_id")
                else:
                    for idx, opt in enumerate(id_options):
                        if any(k in opt.lower() for k in ["id", "code", "key"]):
                            default_idx = idx
                            break

                selected_id = st.selectbox(
                    "Select common ID column for record matching:",
                    options=id_options,
                    index=default_idx,
                    help="A valid ID column must be completely non-blank and unique in both files. Record matching uses exact text comparison."
                )

                if selected_id == "(None / Select ID Column)":
                    st.info("ℹ️ **Record matching unavailable**: Please select a valid common ID column above to compare added and removed records.")
                else:
                    s_b = df_b[selected_id].astype(str)
                    s_a = df_a[selected_id].astype(str)

                    b_blanks = sum(1 for v in s_b if is_missing_cell(v))
                    a_blanks = sum(1 for v in s_a if is_missing_cell(v))

                    b_dups = len(s_b) - len(s_b.unique())
                    a_dups = len(s_a) - len(s_a.unique())

                    if b_blanks > 0 or a_blanks > 0:
                        st.error(
                            f"❌ **Record matching unavailable**: Selected ID column '{selected_id}' contains blank or whitespace-only values "
                            f"(BEFORE: {b_blanks} blank(s), AFTER: {a_blanks} blank(s)). "
                            f"An ID column must be completely non-blank in both files."
                        )
                    elif b_dups > 0 or a_dups > 0:
                        dup_info = []
                        if b_dups > 0:
                            dup_examples_b = list(s_b[s_b.duplicated()].unique()[:3])
                            dup_info.append(f"BEFORE has {b_dups} duplicate ID(s), e.g. {dup_examples_b}")
                        if a_dups > 0:
                            dup_examples_a = list(s_a[s_a.duplicated()].unique()[:3])
                            dup_info.append(f"AFTER has {a_dups} duplicate ID(s), e.g. {dup_examples_a}")
                        st.error(
                            f"❌ **Record matching unavailable**: Selected ID column '{selected_id}' contains duplicate values ({'; '.join(dup_info)}). "
                            f"An ID column must be unique in both files. Summary counts above remain available."
                        )
                    else:
                        # Valid ID
                        set_b = set(s_b)
                        set_a = set(s_a)

                        added_ids = [i for i in s_a if i not in set_b]
                        removed_ids = [i for i in s_b if i not in set_a]
                        common_ids = [i for i in s_b if i in set_a]

                        rec_c1, rec_c2, rec_c3 = st.columns(3)
                        with rec_c1:
                            st.metric(label="Added Records", value=f"{len(added_ids):,}", delta=f"+{len(added_ids)}" if len(added_ids) > 0 else "0", delta_color="off")
                            if len(added_ids) > 0:
                                st.markdown(f'<span class="badge-added">+ Added ({len(added_ids)})</span>', unsafe_allow_html=True)
                            else:
                                st.markdown('<span class="badge-unchanged">None</span>', unsafe_allow_html=True)
                        with rec_c2:
                            st.metric(label="Removed Records", value=f"{len(removed_ids):,}", delta=f"-{len(removed_ids)}" if len(removed_ids) > 0 else "0", delta_color="off")
                            if len(removed_ids) > 0:
                                st.markdown(f'<span class="badge-removed">− Removed ({len(removed_ids)})</span>', unsafe_allow_html=True)
                            else:
                                st.markdown('<span class="badge-unchanged">None</span>', unsafe_allow_html=True)
                        with rec_c3:
                            st.metric(label="Common / Unchanged IDs", value=f"{len(common_ids):,}", delta="Identical in both", delta_color="off")
                            st.markdown('<span class="badge-unchanged">Common</span>', unsafe_allow_html=True)

                        st.caption(
                            f"ℹ️ *With ID '{selected_id}', +{len(added_ids)} arrivals and −{len(removed_ids)} departures explain the net row change ({d_rows:+d}). "
                            f"Reordered rows with identical IDs do not create additions or removals.*"
                        )

                        if len(added_ids) == 0 and len(removed_ids) == 0:
                            st.success(f"✅ **No record additions or removals**: All {len(common_ids)} record IDs match between BEFORE and AFTER.")

                        if added_ids:
                            st.markdown(f"##### 🟢 Added Records ({len(added_ids)}) — IDs: `{', '.join(added_ids)}`")
                            df_added = df_a[df_a[selected_id].isin(added_ids)]
                            st.dataframe(df_added, use_container_width=True, hide_index=True)

                        if removed_ids:
                            st.markdown(f"##### 🔴 Removed Records ({len(removed_ids)}) — IDs: `{', '.join(removed_ids)}`")
                            df_removed = df_b[df_b[selected_id].isin(removed_ids)]
                            st.dataframe(df_removed, use_container_width=True, hide_index=True)



def render_ml_compare_section():
    st.divider()
    st.header("10. Compare Two Experiment Summaries (M4C5 Upgrade)")
    st.caption(
        "Upload two machine learning experiment JSON summaries (format_version 1) to inspect metric deltas, "
        "compare model settings, evaluate train-validation gaps, and rigorously verify recorded condition context."
    )

    demo_ml_c1, demo_ml_c2 = st.columns([1, 4])
    with demo_ml_c1:
        if st.button("🚀 Load Demo JSONs", key="btn_demo_ml_load", help="Load sample M4C5 Run A & Run B JSON experiment files"):
            st.session_state["use_demo_ml"] = True
            st.rerun()
    with demo_ml_c2:
        if st.session_state.get("use_demo_ml", False):
            if st.button("✖️ Clear Demo", key="btn_demo_ml_clear"):
                st.session_state["use_demo_ml"] = False
                st.rerun()


    col_exp_a, col_exp_b = st.columns(2)
    with col_exp_a:
        st.markdown("#### 🧪 Experiment A (Baseline / Reference)")
        exp_a_file = st.file_uploader(
            "Upload Experiment A (JSON):",
            type=["json"],
            key="exp_uploader_a",
            help="Upload the reference experiment summary JSON file."
        )
        if exp_a_file:
            st.caption(f"📄 **Filename:** `{exp_a_file.name}` ({exp_a_file.size / 1024:.1f} KB)")

    with col_exp_b:
        st.markdown("#### 🧪 Experiment B (Comparison / Modified)")
        exp_b_file = st.file_uploader(
            "Upload Experiment B (JSON):",
            type=["json"],
            key="exp_uploader_b",
            help="Upload the comparison experiment summary JSON file."
        )
        if exp_b_file:
            st.caption(f"📄 **Filename:** `{exp_b_file.name}` ({exp_b_file.size / 1024:.1f} KB)")

    is_demo_ml = st.session_state.get("use_demo_ml", False) and (exp_a_file is None) and (exp_b_file is None)
    if is_demo_ml:
        st.info("ℹ️ **Sample test files active:** `M4C5_RUN_A.json` (Baseline) and `M4C5_RUN_B.json` (Modified). Uploading your own files will replace them immediately.")

    if (exp_a_file is None or exp_b_file is None) and not is_demo_ml:
        if exp_a_file is None and exp_b_file is None:
            st.info("ℹ️ Upload both an **Experiment A** JSON and an **Experiment B** JSON above to view the experiment comparison.")
        elif exp_a_file is not None and exp_b_file is None:
            st.warning("⚠️ Please upload the **Experiment B (comparison)** JSON to proceed with comparison.")
        elif exp_a_file is None and exp_b_file is not None:
            st.warning("⚠️ Please upload the **Experiment A (baseline)** JSON to proceed with comparison.")
    else:
        if is_demo_ml:
            with open("M4C5_RUN_A.json", "r", encoding="utf-8") as f_a:
                data_a = json.load(f_a)
            with open("M4C5_RUN_B.json", "r", encoding="utf-8") as f_b:
                data_b = json.load(f_b)
            parse_error = False
            run_id_a = str(data_a.get("run_id", "DEMO_A"))
            run_id_b = str(data_b.get("run_id", "DEMO_B"))
            st.caption(f"📁 **Active Files:** `M4C5_RUN_A.json` (run_id: `{run_id_a}`) vs `M4C5_RUN_B.json` (run_id: `{run_id_b}`)")
        else:
            # 1. Parse JSON files safely
            import json
            import math

            parse_error = False
            try:
                exp_a_file.seek(0)
                data_a = json.loads(exp_a_file.read().decode("utf-8"))
            except Exception as e:
                st.error(f"❌ Error reading Experiment A JSON: {e}")
                parse_error = True
                data_a = None

            try:
                exp_b_file.seek(0)
                data_b = json.loads(exp_b_file.read().decode("utf-8"))
            except Exception as e:
                st.error(f"❌ Error reading Experiment B JSON: {e}")
                parse_error = True
                data_b = None

        if not parse_error and isinstance(data_a, dict) and isinstance(data_b, dict):
            # 2. Validate metric values [0, 1]
            def check_exp_metric(m_dict, metric_name):
                if metric_name not in m_dict:
                    return False, f"Missing required metric: {metric_name}"
                val = m_dict[metric_name]
                if val is None or not isinstance(val, (int, float)) or isinstance(val, bool):
                    return False, f"Metric '{metric_name}' must be numeric"
                if math.isnan(val) or math.isinf(val):
                    return False, f"Metric '{metric_name}' must be finite"
                if val < 0.0 or val > 1.0:
                    return False, f"Metric '{metric_name}' ({val}) is out of valid range [0, 1]"
                return True, None

            m_a = data_a.get("metrics")
            m_b = data_b.get("metrics")

            metric_errors = []
            if not isinstance(m_a, dict):
                metric_errors.append("Experiment A is missing a valid 'metrics' dictionary")
            else:
                for mn in ["f1", "precision", "recall"]:
                    ok, err = check_exp_metric(m_a, mn)
                    if not ok:
                        metric_errors.append(f"Experiment A: {err}")
                if "train_f1" in m_a:
                    ok, err = check_exp_metric(m_a, "train_f1")
                    if not ok:
                        metric_errors.append(f"Experiment A: {err}")

            if not isinstance(m_b, dict):
                metric_errors.append("Experiment B is missing a valid 'metrics' dictionary")
            else:
                for mn in ["f1", "precision", "recall"]:
                    ok, err = check_exp_metric(m_b, mn)
                    if not ok:
                        metric_errors.append(f"Experiment B: {err}")
                if "train_f1" in m_b:
                    ok, err = check_exp_metric(m_b, "train_f1")
                    if not ok:
                        metric_errors.append(f"Experiment B: {err}")

            if metric_errors:
                for me in metric_errors:
                    st.error(f"❌ {me}")
                st.stop()

            # Run IDs and Direction Banner
            run_id_a = str(data_a.get("run_id", "A"))
            run_id_b = str(data_b.get("run_id", "B"))

            st.markdown(
                f"""
                <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 12px 18px; margin: 12px 0 20px 0; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px;">
                    <div>
                        <span style="font-size: 13px; font-weight: 700; color: #475569;">Experiment Direction:</span>
                        <span style="font-family: monospace; font-size: 13px; font-weight: 600; color: #0b192c; margin-left: 6px;">
                            A: <b>{exp_a_file.name}</b> (run_id: <code>{run_id_a}</code>) ➔ B: <b>{exp_b_file.name}</b> (run_id: <code>{run_id_b}</code>)
                        </span>
                    </div>
                    <div>
                        <span style="font-size: 12px; color: #64748b;">Formula: <b>Δ = B − A</b></span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            # 3. Context Verification & Three Statuses
            REQUIRED_CONTEXT = [
                "dataset_id",
                "split_id",
                "target",
                "positive_class",
                "features",
                "threshold",
                "seed",
                "evaluation_split"
            ]

            missing_in_a = [f for f in REQUIRED_CONTEXT if f not in data_a or data_a[f] is None]
            missing_in_b = [f for f in REQUIRED_CONTEXT if f not in data_b or data_b[f] is None]

            diff_list = []
            if missing_in_a or missing_in_b:
                exp_status = "Insufficient context"
                missing_reasons = []
                if missing_in_a:
                    missing_reasons.append(f"Experiment A missing: {', '.join(missing_in_a)}")
                if missing_in_b:
                    missing_reasons.append(f"Experiment B missing: {', '.join(missing_in_b)}")
                status_desc = "; ".join(missing_reasons)
            else:
                # Check matching
                if data_a["dataset_id"] != data_b["dataset_id"]:
                    diff_list.append(f"dataset_id ('{data_a['dataset_id']}' vs '{data_b['dataset_id']}')")
                if data_a["split_id"] != data_b["split_id"]:
                    diff_list.append(f"split_id ('{data_a['split_id']}' vs '{data_b['split_id']}')")
                if data_a["target"] != data_b["target"]:
                    diff_list.append(f"target ('{data_a['target']}' vs '{data_b['target']}')")
                if data_a["positive_class"] != data_b["positive_class"]:
                    diff_list.append(f"positive_class ('{data_a['positive_class']}' vs '{data_b['positive_class']}')")
                if set(data_a.get("features", [])) != set(data_b.get("features", [])):
                    diff_list.append("feature set mismatch (elements differ)")
                if data_a["threshold"] != data_b["threshold"]:
                    diff_list.append(f"threshold ({data_a['threshold']} vs {data_b['threshold']})")
                if data_a["seed"] != data_b["seed"]:
                    diff_list.append(f"seed ({data_a['seed']} vs {data_b['seed']})")
                if data_a["evaluation_split"] != data_b["evaluation_split"]:
                    diff_list.append(f"evaluation_split ('{data_a['evaluation_split']}' vs '{data_b['evaluation_split']}')")
                elif data_a["evaluation_split"] != "validation":
                    diff_list.append(f"evaluation_split is not 'validation' (both record '{data_a['evaluation_split']}')")

                if not diff_list:
                    exp_status = "Same recorded conditions"
                    status_desc = "Recorded labels match; this does not verify the measurements. Model, penalty, and C are compared settings."
                else:
                    exp_status = "Conditions differ"
                    status_desc = f"Recorded conditions differ: {'; '.join(diff_list)}. Direction alone does not establish quality; never choose a winner."

            # Display Status Card
            if exp_status == "Same recorded conditions":
                st.success(f"🟢 **Status: Same recorded conditions** — {status_desc}")
            elif exp_status == "Conditions differ":
                st.warning(f"🟠 **Status: Conditions differ** — {status_desc}")
            else:
                st.error(f"🔴 **Status: Insufficient context** — {status_desc}")

            # 4. Three Main Metric Cards (F1, Precision, Recall Only)
            f1_a, f1_b = float(m_a["f1"]), float(m_b["f1"])
            prec_a, prec_b = float(m_a["precision"]), float(m_b["precision"])
            rec_a, rec_b = float(m_a["recall"]), float(m_b["recall"])

            f1_delta = round(f1_b - f1_a, 2)
            prec_delta = round(prec_b - prec_a, 2)
            rec_delta = round(rec_b - rec_a, 2)

            c_m1, c_m2, c_m3 = st.columns(3)

            with c_m1:
                st.metric(
                    label="F1 Score",
                    value=f"{f1_a:.2f} → {f1_b:.2f}",
                    delta=f"{f1_delta:+.2f}" if f1_delta != 0 else "0.00",
                    delta_color="off"
                )
                if f1_delta > 0:
                    st.markdown(f'<span class="badge-added">+{f1_delta:.2f} Upward</span>', unsafe_allow_html=True)
                elif f1_delta < 0:
                    st.markdown(f'<span class="badge-removed">{f1_delta:.2f} Downward</span>', unsafe_allow_html=True)
                else:
                    st.markdown('<span class="badge-unchanged">0.00 Zero</span>', unsafe_allow_html=True)

            with c_m2:
                st.metric(
                    label="Precision",
                    value=f"{prec_a:.2f} → {prec_b:.2f}",
                    delta=f"{prec_delta:+.2f}" if prec_delta != 0 else "0.00",
                    delta_color="off"
                )
                if prec_delta > 0:
                    st.markdown(f'<span class="badge-added">+{prec_delta:.2f} Upward</span>', unsafe_allow_html=True)
                elif prec_delta < 0:
                    st.markdown(f'<span class="badge-removed">{prec_delta:.2f} Downward</span>', unsafe_allow_html=True)
                else:
                    st.markdown('<span class="badge-unchanged">0.00 Zero</span>', unsafe_allow_html=True)

            with c_m3:
                st.metric(
                    label="Recall",
                    value=f"{rec_a:.2f} → {rec_b:.2f}",
                    delta=f"{rec_delta:+.2f}" if rec_delta != 0 else "0.00",
                    delta_color="off"
                )
                if rec_delta > 0:
                    st.markdown(f'<span class="badge-added">+{rec_delta:.2f} Upward</span>', unsafe_allow_html=True)
                elif rec_delta < 0:
                    st.markdown(f'<span class="badge-removed">{rec_delta:.2f} Downward</span>', unsafe_allow_html=True)
                else:
                    st.markdown('<span class="badge-unchanged">0.00 Zero</span>', unsafe_allow_html=True)

            st.caption(
                "ℹ️ *Note: Delta = B − A. Direction describes a numerical change, not a quality verdict or proof that one run is better. Never choose a winner.*"
            )

            # 5. Recorded Model Settings Comparison
            st.markdown("##### ⚙️ Recorded Model Settings")
            set_col1, set_col2, set_col3 = st.columns(3)
            with set_col1:
                st.markdown(f"**Model:** `{data_a.get('model', '—')}` → `{data_b.get('model', '—')}`")
            with set_col2:
                st.markdown(f"**Penalty:** `{data_a.get('penalty', '—')}` → `{data_b.get('penalty', '—')}`")
            with set_col3:
                c_a = data_a.get("C")
                c_b = data_b.get("C")
                if isinstance(c_a, (int, float)) and isinstance(c_b, (int, float)):
                    c_diff = round(c_b - c_a, 2)
                    st.markdown(f"**C (Regularization):** `{c_a}` → `{c_b}` (Δ = **{c_diff:+g}**)")
                else:
                    st.markdown(f"**C (Regularization):** `{c_a}` → `{c_b}`")
            st.caption("ℹ️ *Model, penalty, and C are recorded model settings to display: their differences are compared without being treated as a condition mismatch.*")

            # Expandable Detail 1: Train - Validation F1 Gap
            with st.expander("🔍 Train − Validation F1 Gap", expanded=True):
                if data_a.get("evaluation_split") == "validation" and data_b.get("evaluation_split") == "validation":
                    if "train_f1" in m_a and "train_f1" in m_b:
                        train_f1_a = float(m_a["train_f1"])
                        train_f1_b = float(m_b["train_f1"])
                        gap_a = round(train_f1_a - f1_a, 2)
                        gap_b = round(train_f1_b - f1_b, 2)
                        gap_diff = round(gap_b - gap_a, 2)

                        gap_c1, gap_c2, gap_c3 = st.columns(3)
                        with gap_c1:
                            st.metric("Experiment A Gap (Train − Val)", f"{gap_a:.2f}")
                            st.caption(f"Train: {train_f1_a:.2f} − Val: {f1_a:.2f}")
                        with gap_c2:
                            st.metric("Experiment B Gap (Train − Val)", f"{gap_b:.2f}")
                            st.caption(f"Train: {train_f1_b:.2f} − Val: {f1_b:.2f}")
                        with gap_c3:
                            st.metric("Gap Change (B − A)", f"{gap_diff:+.2f}")
                            st.caption(f"{gap_a:.2f} → {gap_b:.2f}")

                        st.caption(
                            "ℹ️ *Train − validation F1 gap is available only for validation results. "
                            "A smaller gap may indicate less generalization gap, but must be interpreted on matching validation splits.*"
                        )
                    else:
                        st.info("ℹ️ Train − Validation F1 gap unavailable: 'train_f1' metric is missing in one or both experiment summaries.")
                else:
                    st.info(
                        "ℹ️ **Train − Validation F1 gap is unavailable**: The gap can only be calculated when both runs record "
                        "`evaluation_split = 'validation'`. (For example, runs evaluated on 'train' or incomplete context records cannot produce a validation gap)."
                    )

            # Expandable Detail 2: Detailed Context Verification Matrix
            with st.expander("📋 Recorded Context Verification Matrix", expanded=False):
                matrix_rows = []
                for cf in REQUIRED_CONTEXT:
                    val_a = data_a.get(cf)
                    val_b = data_b.get(cf)
                    if val_a is None or val_b is None:
                        mtch = "❌ Missing Context"
                    elif cf == "features":
                        mtch = "✅ Match (Set identical)" if set(val_a) == set(val_b) else "❌ Mismatch"
                        val_a = ", ".join(val_a) if isinstance(val_a, list) else str(val_a)
                        val_b = ", ".join(val_b) if isinstance(val_b, list) else str(val_b)
                    elif cf == "evaluation_split":
                        if val_a == val_b == "validation":
                            mtch = "✅ Match (validation)"
                        elif val_a == val_b:
                            mtch = f"⚠️ Not validation ('{val_a}')"
                        else:
                            mtch = f"❌ Split Mismatch ('{val_a}' vs '{val_b}')"
                    else:
                        mtch = "✅ Match" if val_a == val_b else "❌ Mismatch"

                    matrix_rows.append({
                        "Context Field": cf,
                        "Experiment A": str(val_a),
                        "Experiment B": str(val_b),
                        "Match Status": mtch
                    })
                st.dataframe(pd.DataFrame(matrix_rows), use_container_width=True, hide_index=True)

            # Expandable Detail 3: Raw JSON Records
            with st.expander("📄 Raw Experiment JSON Records", expanded=False):
                raw_c1, raw_c2 = st.columns(2)
                with raw_c1:
                    st.markdown(f"**Experiment A ({run_id_a}):**")
                    st.json(data_a)
                with raw_c2:
                    st.markdown(f"**Experiment B ({run_id_b}):**")
                    st.json(data_b)




def render_docs_section():
    st.header("📚 Methodology, Statistical Formulas & Guide")
    st.caption("Comprehensive technical guide detailing calculations, outlier bounds, statistical measures, and integrity guards.")
    
    doc1, doc2 = st.columns(2)
    with doc1:
        st.markdown(
            """
            ### 1. 🔍 Invisible Spaces-Only Cells ("   ")
            - **The Problem**: Tabular datasets often contain cells that look blank to human eyes but contain whitespace characters (`"   "`). Standard `df.isna()` checks treat them as non-null strings.
            - **Detection**: Every string cell is strictly tested with regular expression `r"^\\s+$"`.
            - **Rule**: Zeros (`0`, `"0"`), and standard tokens (`"NA"`, `"null"`) are preserved as real values, not missing or whitespace.
            
            ### 2. 🔬 1.5 × IQR Tukey Outlier Inspection
            - Developed by John Tukey for robust exploratory data analysis:
              - $Q_1$ = 25th percentile (first quartile)
              - $Q_3$ = 75th percentile (third quartile)
              - $\\text{IQR} = Q_3 - Q_1$ (interquartile range)
              - Lower Inner Fence: $[Q_1 - 1.5\\text{IQR}]$
              - Upper Inner Fence: $[Q_3 + 1.5\\text{IQR}]$
            - Any value outside these whiskers is flagged as *Needs inspection*.
            
            ### 3. 📐 Feature Scaling Comparison
            - **MinMax Scaler**: $x_{\\text{norm}} = (x - x_{\\min}) / (x_{\\max} - x_{\\min})$ maps values into $[0, 1]$.
            - **Standard Scaler (Z-Score)**: $z = (x - \\mu) / \\sigma$ ($ddof=0$) transforms features to mean 0 and variance 1.
            """
        )
    with doc2:
        st.markdown(
            """
            ### 4. 📈 Skewness & Kurtosis
            - **Skewness $\\approx 0$**: Approximately symmetric normal distribution.
            - **Skewness $> 0.5$**: Right-skewed distribution with a long positive tail (e.g. income, transaction amounts).
            - **Skewness $< -0.5$**: Left-skewed distribution.
            - **Kurtosis**: Quantifies tail weight and peakedness relative to a normal distribution.
            
            ### 5. 🔗 Correlation & Multicollinearity
            - **Pearson ($r$)**: Measures linear relationship strength ($-1 \\le r \\le 1$).
            - **Spearman**: Measures monotonic rank correlation.
            - **Multicollinearity ($|r| \\ge 0.85$)**: High redundancy between predictor pairs that destabilizes regression coefficients.
            
            ### 6. 🧪 ML Experiment Comparison (M4C5)
            - **Direction Alone Does Not Establish Quality**: An increase in F1 score does not automatically make a run superior; trade-offs and variance must be examined.
            - **Identical Recorded Conditions**: Verified across 8 core fields: `dataset_id`, `split_id`, `target`, `positive_class`, `features` (order-invariant set), `threshold`, `seed`, and `evaluation_split = "validation"`.
            - **Overfitting Gap**: $\\text{Gap} = train\\_f1 - val\\_f1$. Strictly guarded to ensure both runs evaluate on validation splits.
            """
        )

# Logo HTML construction
if icon_b64:
    logo_img_html = f'<img src="data:image/svg+xml;base64,{icon_b64}" width="46" height="46" style="border-radius: 10px; box-shadow: 0 4px 12px rgba(5, 55, 255, 0.15);" alt="Dataset Explorer AI Logo" />'
else:
    logo_img_html = '<span style="font-size: 36px;">📊</span>'

# App Hero Banner
st.markdown(
    f"""
    <div class="hero-banner">
        <div style="display: flex; align-items: center; gap: 16px; margin-bottom: 12px; flex-wrap: wrap;">
            {logo_img_html}
            <div>
                <div class="hero-badge">AI/ML Engineering & Tabular Analytics</div>
                <div class="hero-title">📊 Dataset Explorer AI</div>
            </div>
        </div>
        <p class="hero-desc">
            Interactive exploratory data analysis, 1.5×IQR statistical anomaly inspection, version comparison (BEFORE vs AFTER), and machine learning experiment comparison (M4C5) with scientific rigor.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# 4 Main Tabs Navigation
tab_eda, tab_csv_diff, tab_ml_compare, tab_docs = st.tabs([
    "📊 1. Single Dataset EDA",
    "🔄 2. CSV Version Diff (BEFORE vs AFTER)",
    "🧪 3. ML Experiment Compare (M4C5)",
    "📚 4. Methodology & Guide"
])

# -------------------------------------------------------------
# TAB 1: Single File EDA
# -------------------------------------------------------------
with tab_eda:
    st.markdown(
        """
        <div class="steps-ribbon">
            <div class="step-chip"><span class="step-num">1</span> 📂 Upload</div>
            <div class="step-chip"><span class="step-num">2</span> 📐 Overview & Health</div>
            <div class="step-chip"><span class="step-num">3</span> 🔍 Missing & Spaces</div>
            <div class="step-chip"><span class="step-num">4</span> 📊 Aggregations</div>
            <div class="step-chip"><span class="step-num">5</span> 🔬 1.5×IQR Outliers</div>
            <div class="step-chip"><span class="step-num">6</span> 📈 Distributions</div>
            <div class="step-chip"><span class="step-num">7</span> 🔗 Heatmap</div>
            <div class="step-chip"><span class="step-num">8</span> 🎯 Feature Selection</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    up_col1, up_col2 = st.columns([3, 2])
    with up_col1:
        uploaded_file = st.file_uploader(
            "Choose a CSV file to explore (maximum 5 MB):",
            type=["csv"],
            key="main_csv_uploader",
            help="Supports standard UTF-8 encoded CSV files (comma or semicolon delimited)."
        )
    with up_col2:
        st.markdown("#### ⚡ Quick Demo Data")
        st.caption("No CSV file on hand? Test all features with real-world sales data in one click:")
        demo_c1, demo_c2 = st.columns(2)
        with demo_c1:
            if st.button("🚀 Load Demo Dataset", key="btn_load_demo_csv", use_container_width=True, help="Load Superstore retail analytics dataset"):
                st.session_state["use_demo_csv"] = True
                st.rerun()
        with demo_c2:
            if st.session_state.get("use_demo_csv", False):
                if st.button("✖️ Clear Demo", key="btn_clear_demo_csv", use_container_width=True):
                    st.session_state["use_demo_csv"] = False
                    st.rerun()

    is_demo_active = (uploaded_file is None) and st.session_state.get("use_demo_csv", False)
    MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024  # 5 MB

    if is_demo_active:
        st.info("ℹ️ **Sample dataset active:** `superstore_cleaned.csv` (US retail sales & order analytics). Upload your own file anytime to replace it.")
        try:
            df = pd.read_csv("superstore_cleaned.csv", encoding="utf-8")
            file_name = "superstore_cleaned.csv"
            file_size_bytes = os.path.getsize("superstore_cleaned.csv")
            file_size_mb = file_size_bytes / (1024 * 1024)
            run_single_eda_pipeline(df, file_name, file_size_mb)
        except Exception as e:
            st.error(f"❌ Error loading demo dataset: {e}")
    elif uploaded_file is None:
        st.markdown(
            """
            <div style="background: #f8fafc; border: 1px dashed #cbd5e1; border-radius: 14px; padding: 40px 24px; text-align: center; margin-top: 14px;">
                <div style="font-size: 42px; margin-bottom: 12px;">📁</div>
                <h3 style="color: #0b192c !important; margin: 0 0 8px 0; font-size: 20px;">No CSV file uploaded yet</h3>
                <p style="color: #64748b; font-size: 14px; max-width: 520px; margin: 0 auto 16px auto;">
                    Drag and drop or browse your CSV file above to start analyzing dataset structure, column types, missing values, and category charts.
                </p>
                <div style="display: inline-flex; gap: 8px; flex-wrap: wrap; justify-content: center;">
                    <span style="background: #e0e7ff; color: #0537ff; font-size: 12px; font-weight: 600; padding: 5px 12px; border-radius: 6px;">UTF-8 CSV</span>
                    <span style="background: #e0e7ff; color: #0537ff; font-size: 12px; font-weight: 600; padding: 5px 12px; border-radius: 6px;">Max 5 MB</span>
                    <span style="background: #e0e7ff; color: #0537ff; font-size: 12px; font-weight: 600; padding: 5px 12px; border-radius: 6px;">Automatic Delimiter Detection</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        file_name = uploaded_file.name
        if not file_name.lower().endswith(".csv"):
            st.error(f"❌ Wrong file type: '{file_name}'. Please upload a valid file ending with .csv.")
            st.stop()

        file_size_bytes = uploaded_file.size
        file_size_mb = file_size_bytes / (1024 * 1024)
        if file_size_bytes > MAX_FILE_SIZE_BYTES:
            st.error(f"❌ The uploaded file is too large ({file_size_mb:.2f} MB). The maximum allowed file size is 5 MB.")
            st.stop()

        if file_size_bytes == 0:
            st.error("❌ The uploaded file is empty (0 bytes). Please upload a file that contains data.")
            st.stop()

        try:
            uploaded_file.seek(0)
            try:
                df = pd.read_csv(uploaded_file, sep=None, engine="python", encoding="utf-8", header=0)
            except Exception:
                uploaded_file.seek(0)
                df = pd.read_csv(uploaded_file, sep=",", encoding="utf-8", header=0)
        except UnicodeDecodeError:
            st.error("❌ Could not read the file using UTF-8 encoding. Please save your CSV with UTF-8 encoding and try again.")
            st.stop()
        except pd.errors.EmptyDataError:
            st.error("❌ The uploaded file contains no data or headers. Please verify the file content.")
            st.stop()
        except pd.errors.ParserError as e:
            st.error(f"❌ Could not parse the CSV file. Please make sure the file is in valid CSV format.\n\nDetails: {e}")
            st.stop()
        except Exception as e:
            st.error(f"❌ An unexpected error occurred while reading the file: {e}")
            st.stop()

        if df.empty:
            st.warning("⚠️ The file was parsed, but it contains no rows of data.")
            st.stop()

        run_single_eda_pipeline(df, file_name, file_size_mb)

# -------------------------------------------------------------
# TAB 2: CSV Diff (BEFORE vs AFTER)
# -------------------------------------------------------------
with tab_csv_diff:
    render_csv_diff_section()

# -------------------------------------------------------------
# TAB 3: ML Experiment Compare (M4C5)
# -------------------------------------------------------------
with tab_ml_compare:
    render_ml_compare_section()

# -------------------------------------------------------------
# TAB 4: Methodology & Guide
# -------------------------------------------------------------
with tab_docs:
    render_docs_section()

# Global Footer
st.markdown(
    """
    <div style="text-align: center; padding: 32px 0 16px 0; border-top: 1px solid #e2e8f0; margin-top: 40px; color: #64748b; font-size: 13px;">
        Dataset Explorer AI · Developed by <strong>Usnatdin Xafizadinov</strong> · <a href="https://github.com/XafizadinovUsnatdin/datasetexplorer" target="_blank" style="color: #0537ff; font-weight: 700; text-decoration: none;">GitHub Repository</a>
    </div>
    """,
    unsafe_allow_html=True
)
