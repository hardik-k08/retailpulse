# RetailPulse | Sales Intelligence & Demand Forecasting Platform

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**RetailPulse** is an enterprise-grade Business Intelligence platform and Random Forest demand forecasting system. It greets users with an interactive landing page and leads into an analytics suite featuring temporal revenue timelines, seasonal holiday scenario modeling, dynamic inventory buffering advice, model explainability diagnostics, and publication-ready PDF/CSV export reporting.

---

## 🌟 Key Capabilities

1. **Executive Welcome Experience:**
   - Modern brand entrance with animated data visualization accents.
   - One-click seamless transition to the core analytics dashboard.

2. **Executive Overview & KPI Engine:**
   - Real-time financial metrics: Total Revenue, Gross Order Volumes, Average Order Value (AOV), and 7-Day Festive Surge.
   - Dual-axis revenue and quantity timeline with interactive Plotly tooltips.
   - Category & SKU revenue Treemap and 80/20 Pareto revenue concentration charts.

3. **Scenario Modeling: Normal vs. Festive Demand:**
   - Direct empirical contrast between baseline operations (April–May) and peak festival demand (October–November).
   - Dynamic product-level demand comparison chart and calendar-period day-of-week heatmap.

4. **Machine Learning 7-Day Forecasting:**
   - Multi-output Random Forest Regressor (300 estimators, max depth 10).
   - SKU-level 7-day predicted demand with automated surge multipliers and stockout risk indicators (*Stable*, *Moderate*, *High*).

5. **AI Business Insights & Executive Reporting:**
   - Dynamic executive summaries computed in real-time from active data filters.
   - Inventory replenishment guidance with safety stock multipliers.
   - Publication-grade Executive PDF briefings (via ReportLab) and structured CSV exports.

---

## 📂 Repository Structure

```
retailpulse/
├── app.py                      # Main Streamlit Application (Routes Welcome & Analytics Dashboard)
├── combined_transactions.csv   # Source transaction dataset (2,675 rows)
├── daily_product_features.csv  # Precomputed daily product features (1,217 rows)
├── requirements.txt            # Production dependencies with cloud-tested versions
├── .gitignore                  # Git exclusion rules for clean repository pushes
├── .streamlit/
│   └── config.toml             # Theme styling, headless mode, and UI configuration
├── README.md                   # Platform documentation & cloud deployment guide
├── src/
│   ├── __init__.py
│   ├── theme.py                # Dual-theme design tokens (Dark Obsidian & Light Studio) & CSS
│   ├── data_engine.py          # Data ingestion, lag feature generation, taxonomy, and filtering
│   ├── model_engine.py         # Random Forest model (RF-300), holdout split, and scenario engine
│   └── components/
│       ├── __init__.py
│       ├── html_utils.py       # HTML rendering utility preventing Markdown formatting traps
│       ├── welcome.py          # Brand landing page with visual waveform & hero action
│       ├── navbar.py           # Top executive navigation bar with live status indicator
│       ├── sidebar.py          # Collapsible sidebar with theme toggle, navigation, and filters
│       ├── kpi_cards.py        # Executive KPI metric cards with micro-interactions
│       ├── charts.py           # Plotly interactive visualizations (Timeline, Treemap, Pareto, Heatmap)
│       ├── ai_insights.py      # Business insights & inventory replenishment advisor
│       └── export_reports.py   # Corporate ReportLab PDF generator & CSV exporter
└── tests/
    ├── test_phase1.py          # Numerical parity test (Baseline vs Modular Engine)
    ├── test_phase2.py          # Theme system and Plotly layout test
    ├── test_phase3.py          # Interactive chart generation test
    ├── test_phase4.py          # AI insights & replenishment logic test
    ├── test_phase5_integration.py # Full end-to-end integration test
    ├── test_welcome_navigation.py # Landing page navigation test
    ├── test_theme_contrast.py   # WCAG AAA contrast audit
    └── test_html_rendering.py   # HTML rendering test
```

---

## ⚡ Quickstart (Local Run)

To run the application locally:

```bash
# 1. Clone repository
git clone https://github.com/<YOUR-USERNAME>/retailpulse.git
cd retailpulse

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch dashboard
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`.

---

## 🌐 Deploy to Streamlit Community Cloud (Step-by-Step)

Deploying to **Streamlit Community Cloud** provides a permanent HTTPS URL accessible from any computer (including school/work networks) with zero server setup.

### Step 1: Create a GitHub Repository
1. Navigate to [github.com](https://github.com) and log in.
2. Click **New** repository.
3. Repository name: `retailpulse` (set to **Public**).
4. Do **not** initialize with a README or .gitignore (already present).
5. Click **Create repository**.

### Step 2: Push Project Files to GitHub
```bash
git init
git add .
git commit -m "Deploy RetailPulse Sales Intelligence Platform"
git branch -M main
git remote add origin https://github.com/<YOUR-USERNAME>/retailpulse.git
git push -u origin main
```
*(Alternatively, drag and drop the files from this folder directly into the GitHub web interface).*

### Step 3: Launch on Streamlit Community Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
2. Click **New app**.
3. Select your repository: `<YOUR-USERNAME>/retailpulse`.
4. Branch: `main`.
5. Main file path: `app.py`.
6. Click **Deploy!**

---

## 🔬 Model Architecture & Mathematical Parity

The underlying forecasting engine uses a 300-tree Random Forest Regressor evaluated against an 80/20 chronological holdout partition:

| Metric / Output | Evaluation Baseline | Status |
| :--- | :---: | :---: |
| **Holdout MAE** | `117.1246` units | ✅ Exact Match |
| **Holdout RMSE** | `163.7668` units | ✅ Exact Match |
| **Holdout $R^2$** | `0.6761` | ✅ Exact Match |
| **Normal 7-Day Demand** | `2,274.95` units | ✅ Exact Match |
| **Festive 7-Day Demand** | `7,108.48` units | ✅ Exact Match |
| **Net Festive Surge** | `+4,833.53` units (+212.47%) | ✅ Exact Match |

---

## 📦 Required Dependencies

All packages are pinned with verified version constraints in `requirements.txt`:
* `streamlit>=1.35.0`
* `pandas>=2.0.0`
* `numpy>=1.24.0`
* `scikit-learn>=1.3.0`
* `openpyxl>=3.1.0`
* `plotly>=5.15.0`
* `reportlab>=4.0.0`
