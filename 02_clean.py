import pandas as pd
import numpy as np

df = pd.read_csv("titanic_raw_messy.csv")
change_log = []

def log(issue, action, count):
    change_log.append({"Issue": issue, "Action Taken": action, "Rows/Fields Affected": count})

# ---------------------------------------------------------------------------
# 1. Remove exact duplicate rows (re-submitted/duplicated records)
# ---------------------------------------------------------------------------
before = len(df)
df = df.drop_duplicates(keep="first").reset_index(drop=True)
after = len(df)
log("Exact duplicate rows (re-exported records)", "Dropped duplicates, kept first occurrence", before - after)

# ---------------------------------------------------------------------------
# 2. Standardize text casing / whitespace: Name
# ---------------------------------------------------------------------------
mask = df["Name"] != df["Name"].str.strip()
n = mask.sum()
df["Name"] = df["Name"].str.strip()
log("Leading/trailing whitespace in Name", "Stripped whitespace", n)

# ---------------------------------------------------------------------------
# 3. Standardize Sex to a fixed category set {male, female}
# ---------------------------------------------------------------------------
before_vals = df["Sex"].copy()
df["Sex"] = df["Sex"].str.strip().str.lower()
n = (before_vals.str.strip().str.lower() != before_vals).sum()  # rows that needed normalizing (rough count)
n = (before_vals != df["Sex"]).sum()
log("Inconsistent casing/whitespace in Sex (e.g. 'Male', 'MALE', ' male')", "Trimmed and lowercased to {male, female}", n)
assert set(df["Sex"].unique()) == {"male", "female"}

# ---------------------------------------------------------------------------
# 4. Standardize Embarked to single-letter port codes {S, C, Q}
# ---------------------------------------------------------------------------
port_map = {
    "southampton": "S", "s": "S",
    "cherbourg": "C", "c": "C",
    "queenstown": "Q", "q": "Q",
}
before_vals = df["Embarked"].copy()
df["Embarked"] = df["Embarked"].str.strip().str.lower().map(port_map)
n_normalized = (before_vals.notna() & (before_vals.str.strip().str.lower().map(port_map) != before_vals)).sum()
log("Inconsistent Embarked values (full port names / lowercase codes mixed with single-letter codes)",
    "Mapped all variants to standard single-letter codes {S, C, Q}", n_normalized)

# Missing Embarked (2 rows): impute with the mode (most common port), a defensible
# choice for just 2 missing values out of ~890
n_missing_embarked = df["Embarked"].isna().sum()
mode_port = df["Embarked"].mode()[0]
df["Embarked"] = df["Embarked"].fillna(mode_port)
log("Missing Embarked (2 rows)", f"Imputed with mode port '{mode_port}' (only 2 rows affected)", n_missing_embarked)

# ---------------------------------------------------------------------------
# 5. Handle missing Age (~20% missing) -> impute by median within Pclass+Sex group
#    (more accurate than a single global median; case-by-case, not blanket)
# ---------------------------------------------------------------------------
n_missing_age = df["Age"].isna().sum()
df["Age"] = df.groupby(["Pclass", "Sex"])["Age"].transform(lambda s: s.fillna(s.median()))
# safety net in case any group had no data at all
df["Age"] = df["Age"].fillna(df["Age"].median())
log("Missing Age (~20% of rows)", "Imputed using median Age within each Pclass x Sex group", n_missing_age)

# ---------------------------------------------------------------------------
# 6. Handle missing Cabin (~77% missing) -> too sparse to impute meaningfully.
#    Flag with a boolean instead of dropping the column or fabricating values.
# ---------------------------------------------------------------------------
n_missing_cabin = df["Cabin"].isna().sum()
df["HasCabinRecord"] = df["Cabin"].notna()
log("Missing Cabin (~77% of rows, too sparse to impute)",
    "Left as-is; added boolean flag 'HasCabinRecord' rather than dropping or guessing", n_missing_cabin)

# ---------------------------------------------------------------------------
# 7. Fix / verify data types
# ---------------------------------------------------------------------------
df["Survived"] = df["Survived"].astype(int)
df["Pclass"] = df["Pclass"].astype(int)
df["Age"] = df["Age"].astype(float).round(1)
df["Fare"] = pd.to_numeric(df["Fare"], errors="coerce").round(4)
log("Verified/cast dtypes (Survived, Pclass as int; Age, Fare as float)", "Explicit astype casts applied", "all rows")

# ---------------------------------------------------------------------------
# 8. Re-run inventory checks to confirm the fixes worked
# ---------------------------------------------------------------------------
print("=== POST-CLEAN CHECKS ===")
print("Shape:", df.shape)
print("Nulls:\n", df.isnull().sum())
print("Duplicate rows:", df.duplicated().sum())
print("Sex values:", df["Sex"].unique())
print("Embarked values:", df["Embarked"].unique())
print(df.dtypes)

df.to_csv("titanic_cleaned.csv", index=False)

log_df = pd.DataFrame(change_log)
log_df.to_csv("change_log.csv", index=False)
print("\n=== CHANGE LOG ===")
print(log_df.to_string(index=False))
