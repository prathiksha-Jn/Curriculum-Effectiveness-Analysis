import pandas as pd
import numpy as np
import os

print("="*60)
print("CURRICULUM EFFECTIVENESS ANALYSIS")
print("DATA CLEANING PIPELINE")
print("="*60)

# ==========================================================
# LOAD DATASET
# ==========================================================

file_path = "input/master_education_data.csv"

df = pd.read_csv(file_path)

print("\nDataset Loaded Successfully")
print("Rows :", df.shape[0])
print("Columns :", df.shape[1])

# ==========================================================
# DATA TYPES
# ==========================================================

print("\nData Types")
print(df.dtypes)


# ==========================================================
# MISSING VALUES
# ==========================================================

print("\nMissing Values Before Cleaning")
print(df.isnull().sum())

# Numeric Columns

numeric_columns = df.select_dtypes(include=np.number).columns

for col in numeric_columns:

    df[col] = df[col].fillna(df[col].median())

# Categorical Columns

categorical_columns = df.select_dtypes(include="object").columns

for col in categorical_columns:

    mode = df[col].mode()

    if len(mode) > 0:
        df[col] = df[col].fillna(mode[0])

# ==========================================================
# REMOVE EXTRA SPACES
# ==========================================================

for col in categorical_columns:

    df[col] = (
        df[col]
        .astype(str)
        .str.strip()
        .str.title()
    )

# ==========================================================
# DATE CONVERSION
# ==========================================================

if "EnrollmentDate" in df.columns:

    df["EnrollmentDate"] = pd.to_datetime(
        df["EnrollmentDate"],
        errors="coerce",
        dayfirst=True
    )

# ==========================================================
# VALIDATIONS
# ==========================================================

if "Attendance" in df.columns:

    df["Attendance"] = df["Attendance"].clip(0,100)

if "Feedback" in df.columns:

    df["Feedback"] = df["Feedback"].clip(1,5)

if "Age" in df.columns:

    df["Age"] = df["Age"].clip(15,70)

if "CompletionPercentage" in df.columns:

    df["CompletionPercentage"] = df["CompletionPercentage"].clip(0,100)

# ==========================================================
# REMOVE NEGATIVE VALUES
# ==========================================================

for col in numeric_columns:

    if df[col].min() < 0:

        df[col] = df[col].clip(lower=0)

# ==========================================================
# REMOVE EMPTY STRINGS
# ==========================================================

for col in categorical_columns:

    df[col] = df[col].replace("", np.nan)

    mode = df[col].mode()

    if len(mode)>0:

        df[col] = df[col].fillna(mode[0])

# ==========================================================
# MISSING VALUES AFTER CLEANING
# ==========================================================

print("\nMissing Values After Cleaning")

print(df.isnull().sum())
# ==========================================================
# REMOVE DUPLICATES
# ==========================================================

duplicates = df.duplicated().sum()

print("\nDuplicate Rows :", duplicates)

df = df.drop_duplicates()

print("After Removing Duplicates :", df.shape)

# ==========================================================
# SUMMARY
# ==========================================================

print("\nCleaning Summary")

print("Rows :", df.shape[0])

print("Columns :", df.shape[1])

print("Duplicates :", df.duplicated().sum())

print("Total Missing Values :", df.isnull().sum().sum())

# ==========================================================
# OUTPUT FOLDER
# ==========================================================

os.makedirs("output", exist_ok=True)

# ==========================================================
# SAVE CSV
# ==========================================================

csv_path = "output/Clean_Master_Education_Data.csv"

df.to_csv(csv_path,index=False)

# ==========================================================
# SAVE EXCEL
# ==========================================================

excel_path = "output/Clean_Master_Education_Data.xlsx"

df.to_excel(excel_path,index=False)

# ==========================================================
# FINAL
# ==========================================================

print("\nFiles Saved Successfully")

print(csv_path)

print(excel_path)

print("\nFirst Five Rows")

print(df.head())

print("\nDataset Cleaning Completed Successfully")

print("="*60)