import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, classification_report

# 1. Set file paths (works automatically if run inside your project folder)
base_dir = r"C:\Users\kriti\OneDrive\Desktop\Customer Churn and Retention Engine"
input_path = os.path.join(base_dir, "Cleaned-Telco-Customer-Churn.csv")

# Fallback if you already moved the CSV into a 'data' subfolder
if not os.path.exists(input_path):
    input_path = os.path.join(base_dir, "data", "Cleaned-Telco-Customer-Churn.csv")

df = pd.read_csv(input_path)
print(f"Loaded {len(df)} rows from: {input_path}")

# 2. Clean TotalCharges & standardize target column
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
df["TotalCharges"] = df["TotalCharges"].fillna(df["MonthlyCharges"] * df["tenure"])

# Ensure target binary flag exists
df["Churn_Flag"] = df["Churn"].map({"Yes": 1, "No": 0})

# 3. Feature Engineering: Create Tenure_Group matching your Power BI visual
def assign_tenure_group(months):
    if months <= 6:
        return "0-6 Months (New)"
    elif months <= 12:
        return "6-12 Months"
    elif months <= 24:
        return "1-2 Years"
    else:
        return "2+ Years (Loyal)"

if "Tenure_Group" not in df.columns:
    df["Tenure_Group"] = df["tenure"].apply(assign_tenure_group)

# 4. Prepare Features (X) and Target (y)
drop_cols = ["customerID", "Churn", "Churn_Flag", "Churn Flag", "Risk_Tier", "Churn_Probability_Pct"]
feature_cols = [c for c in df.columns if c not in drop_cols]

X = pd.get_dummies(df[feature_cols], drop_first=True)
y = df["Churn_Flag"]

# 5. Train / Test Split & Random Forest Model Training
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

rf_model = RandomForestClassifier(
    n_estimators=200,
    max_depth=8,
    min_samples_leaf=10,
    random_state=42
)
rf_model.fit(X_train, y_train)

# 6. Evaluate Model Performance
test_probs = rf_model.predict_proba(X_test)[:, 1]
auc_score = roc_auc_score(y_test, test_probs)
print(f"\nModel ROC-AUC Score: {auc_score:.4f}")
print("\nClassification Report (Test Set):")
print(classification_report(y_test, (test_probs >= 0.50).astype(int)))

# 7. Score Full Customer Base (0% to 100%) & Assign Risk Tiers
all_probs = rf_model.predict_proba(X)[:, 1]
df["Churn_Probability_Pct"] = np.round(all_probs * 100, 2)

def assign_risk_tier(prob_pct):
    if prob_pct >= 70.0:
        return "High Risk"
    elif prob_pct >= 40.0:
        return "Medium Risk"
    else:
        return "Low Risk"

df["Risk_Tier"] = df["Churn_Probability_Pct"].apply(assign_risk_tier)

# 8. Export Clean Prediction Table for Power BI & GitHub
output_cols = [
    "customerID",
    "Contract",
    "InternetService",
    "Tenure_Group",
    "MonthlyCharges",
    "Churn",
    "Churn_Probability_Pct",
    "Risk_Tier"
]
output_df = df[output_cols].copy()

output_path = os.path.join(os.path.dirname(input_path), "churn_predictions_full.csv")
output_df.to_csv(output_path, index=False)

high_risk_active = len(output_df[(output_df["Churn"] == "No") & (output_df["Risk_Tier"] == "High Risk")])
print(f"\nSaved predictions to: {output_path}")
print(f"High-Risk Active Customers (>=70%): {high_risk_active}")