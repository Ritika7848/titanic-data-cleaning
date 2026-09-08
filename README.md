# Data Cleaning & Preprocessing — Titanic Dataset

**Internship Task:** Data Analytics Track, Day 1 — Data Cleaning and Preprocessing
**Author:** Ritika Mishra

## Objective
Clean and preprocess a raw dataset by identifying and fixing common data quality issues:
missing values, duplicate rows, inconsistent formatting, and incorrect data types.

## Dataset
Titanic passenger manifest (906 raw rows). Built from the standard public Titanic dataset,
with typical raw-export issues layered on top of its real missing values, to give the
cleaning exercise genuine problems to find and fix.

## Tools Used
- Python
- Pandas

## Files in this Repo
| File | Description |
|---|---|
| `titanic_raw_messy.csv` | The raw, uncleaned dataset |
| `titanic_cleaned.csv` | The final cleaned dataset |
| `Titanic_Cleaned_Dataset.xlsx` | Cleaned data + change log, in one workbook |
| `Data_Cleaning_Writeup.md` | Write-up: issues found, decisions made, and why |
| `01_inventory.py` | Script that inventories data quality issues (nulls, duplicates, inconsistent categories) |
| `02_clean.py` | Script that applies all cleaning steps and re-verifies the result |

## Data Quality Issues Found & Fixed

| Issue | Scope | Fix Applied |
|---|---|---|
| Exact duplicate rows | 15 rows | Dropped, kept first occurrence |
| Inconsistent `Sex` text | 8 spelling/casing variants | Standardized to `male` / `female` |
| Inconsistent `Embarked` text | Full port names + mixed-case codes | Standardized to `S` / `C` / `Q` |
| Missing `Age` | ~20% of rows | Imputed with median **within Pclass × Sex group** |
| Missing `Embarked` | 2 rows | Imputed with mode (most common port) |
| Missing `Cabin` | ~77% of rows | Left as-is; added `HasCabinRecord` boolean flag instead of guessing |
| Whitespace in `Name` | 46 rows | Stripped |
| Mixed/incorrect dtypes | All rows | Cast `Survived`, `Pclass` to int; `Age`, `Fare` to float |

## Result
- 906 raw rows → **891 clean rows** (duplicates removed)
- 0 unexpected missing values (only `Cabin` intentionally retained + flagged)
- 0 duplicate rows
- All categorical columns reduced to their correct, standardized value sets

See `Data_Cleaning_Writeup.md` for the full reasoning behind each decision.

## How to Run
```bash
pip install pandas
python 01_inventory.py   # inspect the raw data's issues
python 02_clean.py       # clean it and produce titanic_cleaned.csv + change_log.csv
```
