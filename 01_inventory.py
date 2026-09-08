import pandas as pd
pd.set_option("display.width", 120)

df = pd.read_csv("titanic_raw_messy.csv")

print("=== SHAPE ===")
print(df.shape)

print("\n=== DTYPES (df.info()) ===")
df.info()

print("\n=== NULL COUNTS (df.isnull().sum()) ===")
print(df.isnull().sum())

print("\n=== DUPLICATE ROWS (df.duplicated().sum()) ===")
print("Full-row duplicates:", df.duplicated().sum())
print("Duplicate PassengerId (duplicate key):", df["PassengerId"].duplicated().sum())

print("\n=== UNIQUE VALUES: Sex ===")
print(df["Sex"].value_counts(dropna=False))

print("\n=== UNIQUE VALUES: Embarked ===")
print(df["Embarked"].value_counts(dropna=False))

print("\n=== SAMPLE OF Age COLUMN (mixed types) ===")
print(df["Age"].apply(type).value_counts())
print(df[df["Age"].apply(lambda x: isinstance(x, str))]["Age"].head())

print("\n=== SAMPLE OF Fare COLUMN (mixed types) ===")
print(df["Fare"].apply(type).value_counts())
print(df[df["Fare"].apply(lambda x: isinstance(x, str))]["Fare"].head())

print("\n=== SAMPLE Name WITH WHITESPACE ===")
ws = df[df["Name"] != df["Name"].str.strip()]
print(ws["Name"].head())
