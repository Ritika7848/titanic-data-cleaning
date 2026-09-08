# Data Cleaning & Preprocessing — Write-Up
**Task 1 · Data Analytics Track — Titanic Passenger Dataset**

## Dataset
Titanic passenger manifest, 906 rows × 12 columns (raw), sourced from the standard public
Titanic dataset with a handful of typical raw-export issues layered on for practice (duplicate
records, inconsistent category text, stray whitespace) in addition to the dataset's own
real-world missing values.

## Step 1: Inventory (before touching anything)
Ran `df.info()`, `df.isnull().sum()`, and `df.duplicated().sum()` first to see the full scope of
problems before deciding how to fix them:

| Issue | Scope |
|---|---|
| Missing `Age` | 181 / 906 rows (~20%) |
| Missing `Cabin` | 699 / 906 rows (~77%) |
| Missing `Embarked` | 2 / 906 rows |
| Exact duplicate rows | 15 rows |
| Inconsistent `Sex` text | 8 distinct spellings of male/female (casing + whitespace) |
| Inconsistent `Embarked` text | full port names, lowercase codes, and standard codes mixed |
| Whitespace in `Name` | 46 rows with leading/trailing spaces |

## Step 2: Cleaning decisions (case-by-case, not one blanket rule)

**Duplicates.** 15 exact duplicate rows (same `PassengerId` and all fields) were dropped,
keeping the first occurrence — these were re-submitted records, not legitimate repeat
passengers.

**Text standardization.** `Sex` was trimmed and lowercased to a fixed `{male, female}` set.
`Embarked` had three problems at once — full port names ("Southampton"), lowercase codes
("s"), and standard codes ("S") — all mapped to the single-letter standard `{S, C, Q}`.
`Name` whitespace was stripped.

**Missing `Age` (~20%).** Age is meaningfully different by class and gender on the Titanic
(e.g., first-class passengers skewed older), so a single global median would flatten that
signal. Instead, missing ages were imputed with the **median Age within each Pclass × Sex
group** — more accurate than one number for everyone.

**Missing `Embarked` (2 rows).** With only 2 missing values out of ~890, imputing with the
mode (most common port, Southampton) is a reasonable, low-risk choice — it barely affects
the distribution either way.

**Missing `Cabin` (~77%).** This one was *not* imputed or dropped. At 77% missing, any fill
value would be mostly fabricated, and dropping the column throws away real information for
the ~23% of passengers who do have a cabin recorded. Instead, a boolean column
`HasCabinRecord` was added — cabin data is itself informative (having a recorded cabin
correlates with class and fare), so flagging its presence preserves that signal without
guessing at unknown cabin numbers.

**Data types.** `Survived` and `Pclass` cast to `int`; `Age` and `Fare` cast to clean `float`
values (any stray text formatting from the raw export was coerced to numeric).

## Step 3: Re-verification
Re-ran the same inventory checks after cleaning to confirm the fixes worked:
- Duplicate rows: 15 → **0**
- `Sex` values: 8 variants → **2** (`male`, `female`)
- `Embarked` values: 8 variants → **3** (`S`, `C`, `Q`)
- Missing `Age`, `Embarked`: **0** remaining
- Final shape: **891 rows × 13 columns** (12 original + `HasCabinRecord` flag)

## Deliverables
- `Titanic_Cleaned_Dataset.xlsx` — cleaned data (sheet 1) + full change log (sheet 2)
- `titanic_cleaned.csv` — same cleaned data in CSV form
- This write-up

## Answers to the interview questions (for reference)

**How do you decide whether to drop or impute a missing value?**
It depends on how much is missing and whether a reasonable estimate exists. A handful of
missing values in an otherwise informative column (like the 2 missing `Embarked` values here)
are safe to impute with the mode/median. A column that's mostly missing (`Cabin` at 77%) isn't
safe to impute — a flag or leaving it as-is is more honest than fabricating values.

**What's the difference between a duplicate row and a duplicate key?**
A duplicate row means every column matches exactly — a true copy of the same record. A
duplicate key means an identifier column (like `PassengerId`) repeats, but the rest of the row
may differ — that's a sign of a data integrity problem (e.g., the same ID assigned twice),
not necessarily a redundant record to drop outright.

**How would you handle outliers differently from missing values?**
Missing values are absent data — you decide whether to impute, flag, or drop. Outliers are
present but extreme data points, so the first step is verifying whether they're genuine (e.g.
a real $512 first-class fare) or a data-entry error, before deciding to cap, transform, or
keep them — you don't default to removing them.

**How would you validate that a dataset is 'clean' before starting analysis?**
Re-run the same inventory checks used to find the problems: confirm null counts match your
intended state, duplicates are at zero, categorical columns have only the expected values, and
dtypes match what each column should hold. Clean isn't a one-time fix — it's confirmed by
re-checking, not assumed.
