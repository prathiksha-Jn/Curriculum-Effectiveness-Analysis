
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
file_path = "input/master_education_data_realistic.csv"
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
# MISSING VALUES BEFORE CLEANING
# ==========================================================
print("\nMissing Values Before Cleaning")
print(df.isnull().sum())

# ==========================================================
# FILL MISSING VALUES
# ==========================================================
def fill_missing_values(df):

    numeric_columns = df.select_dtypes(include=np.number).columns

    for col in numeric_columns:
        df[col] = df[col].fillna(df[col].median())

    categorical_columns = df.select_dtypes(include="object").columns

    for col in categorical_columns:
        df[col] = df[col].fillna(df[col].mode()[0])

    return df

df = fill_missing_values(df)

# ==========================================================
# REMOVE EXTRA SPACES
# ==========================================================
def clean_text(df):

    categorical_columns = df.select_dtypes(include="object").columns

    for col in categorical_columns:
        df[col] = df[col].astype(str).str.strip().str.title()

    return df

df = clean_text(df)

# ==========================================================
# DATE CONVERSION
# ==========================================================
if "Assessment_Date" in df.columns:
    df["Assessment_Date"] = pd.to_datetime(df["Assessment_Date"], errors="coerce")

# ==========================================================
# VALIDATION
# ==========================================================
def validate_data(df):

    if "Attendance" in df.columns:
        df.loc[(df["Attendance"] < 0) | (df["Attendance"] > 100), "Attendance"] = np.nan
        df["Attendance"] = df["Attendance"].fillna(df["Attendance"].median())

    if "Age" in df.columns:
        df.loc[(df["Age"] < 15) | (df["Age"] > 70), "Age"] = np.nan
        df["Age"] = df["Age"].fillna(df["Age"].median())

    if "Feedback" in df.columns:
        df.loc[(df["Feedback"] < 1) | (df["Feedback"] > 5), "Feedback"] = np.nan
        df["Feedback"] = df["Feedback"].fillna(df["Feedback"].median())

    if "Completion_Pct" in df.columns:
        df.loc[(df["Completion_Pct"] < 0) | (df["Completion_Pct"] > 100), "Completion_Pct"] = np.nan
        df["Completion_Pct"] = df["Completion_Pct"].fillna(df["Completion_Pct"].median())

    if "Learning_Hours" in df.columns:
        df.loc[df["Learning_Hours"] < 0, "Learning_Hours"] = np.nan
        df["Learning_Hours"] = df["Learning_Hours"].fillna(df["Learning_Hours"].median())

    return df

df = validate_data(df)

# ==========================================================
# EMPTY STRING HANDLING
# ==========================================================
categorical_columns = df.select_dtypes(include="object").columns

for col in categorical_columns:
    df[col] = df[col].replace("", np.nan)
    df[col] = df[col].fillna(df[col].mode()[0])

# ==========================================================
# AFTER CLEANING
# ==========================================================
print("\nMissing Values After Cleaning")
print(df.isnull().sum())

# ==========================================================
# DUPLICATES
# ==========================================================
duplicates = df.duplicated().sum()

print("\nDuplicate Rows :", duplicates)

df = df.drop_duplicates()

print("Rows After Removing Duplicates :", df.shape[0])

# ==========================================================
# SUMMARY
# ==========================================================
print("\nCleaning Summary")
print("Rows :", df.shape[0])
print("Columns :", df.shape[1])
print("Duplicates :", df.duplicated().sum())
print("Total Missing Values :", df.isnull().sum().sum())

# ==========================================================
# SAVE FILES
# ==========================================================
os.makedirs("output", exist_ok=True)

df.to_csv("output/Clean_Master_Education_Data.csv", index=False)
df.to_excel("output/Clean_Master_Education_Data.xlsx", index=False)

print("\nFiles Saved Successfully")
print("output/Clean_Master_Education_Data.csv")
print("output/Clean_Master_Education_Data.xlsx")

print("\nFirst Five Rows")
print(df.head())

print("\nDataset Cleaning Completed Successfully")
print("="*60)
