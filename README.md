# Customer-Churn-Retention-Engine
End-to-end telecom churn prediction & retention analytics pipeline using Excel, SQL, Python, and Power BI.

![Executive Retention Dashboard](Dashboard%20ss.png)

---

## Business Problem
In subscription telecom models, historical customer churn stands at **26.54%** (`1,869` lost subscribers)[cite: 3, 4]. Rather than reacting after customers cancel, this engine scores all **5,174 active subscribers** for churn risk and equips retention teams with a prioritized call list and automated next-best-action offers[cite: 4, 8].

---

## Tech Stack & Workflow
1. **Microsoft Excel:** Audited raw billing records (`7,043` rows), resolved blank `TotalCharges` entries for zero-tenure accounts, and validated baseline distributions[cite: 8].
2. **SQL (MySQL / PostgreSQL):** Executed cohort and segmentation queries (`churn analysis.sql`) to identify core churn drivers across contracts, tenure brackets, internet plans, and payment methods.
3. **Python (`pandas`, `scikit-learn`):** Engineered behavioral features and trained a **Random Forest Classifier** (`~0.845 ROC-AUC` in `churn prediction.py`), generating individual churn probability scores (`churn_predictions_full.csv`).
4. **Power BI:** Built a 1:1 star-schema data model (`Churn executive dashboard.pbix`) with dynamic DAX measures, an adjustable `Risk Threshold` parameter (`50%–90%`), and an interactive dark-mode executive dashboard[cite: 1, 11].

---

## Key Analytical Insights
* **High-Risk Active Cohort:** At a `70%` probability threshold, **415 active subscribers** are flagged as high risk, representing **₹31.88K/month** (**₹382.59K/year**) in revenue exposure[cite: 8].
* **Contract Lock-In Impact:** Month-to-month subscribers churn at **42.71%**, compared to **11.27%** for one-year and **2.83%** for two-year contracts[cite: 3, 8].
* **Early-Tenure Vulnerability:** Newly onboarded subscribers (`0–6 months`) exhibit a **52.94%** churn rate, dropping to **14.04%** once customers cross 2 years[cite: 3, 8].
* **Service & Billing Friction:** Fiber optic users (**41.89%** churn) and Electronic Check payers (**45.29%** churn) represent the highest-attrition segments[cite: 3, 8].

---

## Repository Files
* `Cleaned-Telco-Customer-Churn.csv` — Cleaned master dataset (`7,043` customer records)[cite: 8, 11]
* `churn analysis.sql` — SQL cohort and driver analysis queries[cite: 11]
* `churn prediction.py` — Random Forest churn scoring & feature importance script[cite: 11]
* `churn_predictions_full.csv` & `high_risk_active_customers.csv` — ML output tables[cite: 11]
* `Churn executive dashboard.pbix` & `Churn executive dashboard.pdf` — Interactive Power BI report & PDF export[cite: 11]
