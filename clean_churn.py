import pandas as pd

df = pd.read_csv("telco_churn.csv")
print("Before:", df.shape)

full_dupes = df.duplicated().sum()
id_dupes = df["customerID"].duplicated().sum()
dup_id_rows = df[df["customerID"].duplicated(keep=False)]
conflicts = dup_id_rows.groupby("customerID").nunique().gt(1).any(axis=1).sum()
print("Full-row duplicates:", full_dupes)
print("Rows sharing a customerID:", id_dupes)
print("Duplicated IDs with conflicting data:", conflicts)
for c in ["tenure_months", "MonthlyCharges", "SupportTickets"]:
    print(f"  {c:16s} min={df[c].min()}  max={df[c].max()}")

df = df.drop_duplicates(subset="customerID", keep="first")
df = df.drop(columns=["customerID"])
df["gender"] = df["gender"].str.strip().str.capitalize()
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
df["TotalCharges"] = df["TotalCharges"].fillna(0)
df["MonthlyCharges"] = df["MonthlyCharges"].fillna(df["MonthlyCharges"].median())

print("\nAfter:", df.shape,
      "| missing:", int(df.isna().sum().sum()),
      "| dupes:", int(df.duplicated().sum()))
print("gender:", list(df["gender"].unique()),
      "| TotalCharges type:", df["TotalCharges"].dtype)

df.to_csv("telco_churn_clean.csv", index=False)
print("Saved -> telco_churn_clean.csv")
