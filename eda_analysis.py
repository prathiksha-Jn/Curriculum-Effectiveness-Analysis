import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ===========================================================
# CURRICULUM EFFECTIVENESS ANALYSIS
# EXPLORATORY DATA ANALYSIS
# ===========================================================

print("="*70)
print("CURRICULUM EFFECTIVENESS ANALYSIS")
print("EXPLORATORY DATA ANALYSIS")
print("="*70)

# Load Dataset
df = pd.read_excel("output/Clean_Master_Education_Data.xlsx")

print("\nDataset Loaded Successfully")
print("Rows :", df.shape[0])
print("Columns :", df.shape[1])

print("\nDATASET INFO")
print(df.info())

print("\nFIRST 5 ROWS")
print(df.head())

print("\nMISSING VALUES")
print(df.isnull().sum())

print("\nDESCRIPTIVE STATISTICS")
print(df.describe())

print("\nMEAN")
print(df.mean(numeric_only=True))

print("\nMEDIAN")
print(df.median(numeric_only=True))

print("\nMODE")
print(df.mode().iloc[0])

os.makedirs("plots",exist_ok=True)

numeric_cols=df.select_dtypes(include=np.number).columns
# ===========================================================
# 1. COURSE vs AVERAGE EXAM SCORE
# ===========================================================

plt.figure(figsize=(10,6))

course_score = (
    df.groupby("Course")["Exam_Score"]
      .mean()
      .sort_values(ascending=False)
)

sns.barplot(
    x=course_score.index,
    y=course_score.values
)

plt.title("Average Exam Score by Course")
plt.xlabel("Course")
plt.ylabel("Average Exam Score")
plt.xticks(rotation=20)
plt.grid(axis="y", linestyle="--", alpha=0.5)

plt.tight_layout()
plt.savefig("plots/01_course_exam_score.png")
plt.show()


# ===========================================================
# 2. ATTENDANCE vs EXAM SCORE
# ===========================================================

plt.figure(figsize=(8,6))

sns.regplot(
    data=df,
    x="Attendance",
    y="Exam_Score",
    scatter_kws={"alpha":0.3},
    line_kws={"color":"red"}
)

plt.title("Attendance vs Exam Score")
plt.xlabel("Attendance")
plt.ylabel("Exam Score")
plt.grid(alpha=0.3)

plt.tight_layout()
plt.savefig("plots/02_attendance_vs_exam_score.png")
plt.show()


# ===========================================================
# 3. LEARNING HOURS vs EXAM SCORE
# ===========================================================

plt.figure(figsize=(8,6))

sns.regplot(
    data=df,
    x="Learning_Hours",
    y="Exam_Score",
    scatter_kws={"alpha":0.3},
    line_kws={"color":"green"}
)

plt.title("Learning Hours vs Exam Score")
plt.xlabel("Learning Hours")
plt.ylabel("Exam Score")
plt.grid(alpha=0.3)

plt.tight_layout()
plt.savefig("plots/03_learninghours_vs_examscore.png")
plt.show()


# ===========================================================
# 4. COURSE vs COMPLETION PERCENTAGE
# ===========================================================

plt.figure(figsize=(10,6))

completion = (
    df.groupby("Course")["Completion_Pct"]
      .mean()
      .sort_values(ascending=False)
)

sns.barplot(
    x=completion.index,
    y=completion.values
)

plt.title("Average Completion Percentage by Course")
plt.xlabel("Course")
plt.ylabel("Completion Percentage")
plt.xticks(rotation=20)
plt.grid(axis="y", linestyle="--", alpha=0.5)

plt.tight_layout()
plt.savefig("plots/04_course_completion.png")
plt.show()


# ===========================================================
# 5. EXAM SCORE DISTRIBUTION
# ===========================================================

plt.figure(figsize=(8,6))

sns.histplot(
    df["Exam_Score"],
    bins=25,
    kde=True
)

plt.title("Exam Score Distribution")
plt.xlabel("Exam Score")
plt.ylabel("Number of Students")

plt.tight_layout()
plt.savefig("plots/05_exam_score_distribution.png")
plt.show()


# ===========================================================
# 6. CORRELATION HEATMAP
# ===========================================================

plt.figure(figsize=(12,8))

corr = df[numeric_cols].corr()

sns.heatmap(
    corr,
    annot=True,
    cmap="coolwarm",
    fmt=".2f"
)

plt.title("Correlation Heatmap")

plt.tight_layout()
plt.savefig("plots/06_correlation_heatmap.png")
plt.show()

# ===========================================================
# OUTLIER DETECTION (IQR METHOD)
# ===========================================================

print("\n" + "="*70)
print("OUTLIER DETECTION")
print("="*70)

for col in numeric_cols:

    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)

    IQR = Q3 - Q1

    lower = Q1 - (1.5 * IQR)
    upper = Q3 + (1.5 * IQR)

    outliers = df[(df[col] < lower) | (df[col] > upper)]

    print(f"{col:<25} : {len(outliers)} Outliers")


# ===========================================================
# BUSINESS INSIGHTS
# ===========================================================

print("\n" + "="*70)
print("BUSINESS INSIGHTS")
print("="*70)

print(f"Average Attendance          : {df['Attendance'].mean():.2f}")
print(f"Average Learning Hours      : {df['Learning_Hours'].mean():.2f}")
print(f"Average Quiz Score          : {df['Quiz_Score'].mean():.2f}")
print(f"Average Assignment Score    : {df['Assignment_Score'].mean():.2f}")
print(f"Average Exam Score          : {df['Exam_Score'].mean():.2f}")
print(f"Average Completion Percent  : {df['Completion_Pct'].mean():.2f}")


# ===========================================================
# TOP 10 STUDENTS
# ===========================================================

print("\n" + "="*70)
print("TOP 10 STUDENTS")
print("="*70)

top_students = df.nlargest(
    10,
    "Exam_Score"
)[[
    "Student_ID",
    "Course",
    "Exam_Score",
    "Learning_Hours",
    "Attendance"
]]

print(top_students)


# ===========================================================
# BOTTOM 10 STUDENTS
# ===========================================================

print("\n" + "="*70)
print("BOTTOM 10 STUDENTS")
print("="*70)

bottom_students = df.nsmallest(
    10,
    "Exam_Score"
)[[
    "Student_ID",
    "Course",
    "Exam_Score",
    "Learning_Hours",
    "Attendance"
]]

print(bottom_students)


# ===========================================================
# COURSE PERFORMANCE
# ===========================================================

print("\n" + "="*70)
print("AVERAGE EXAM SCORE BY COURSE")
print("="*70)

print(
    df.groupby("Course")["Exam_Score"]
      .mean()
      .sort_values(ascending=False)
)


# ===========================================================
# LEARNING PATH PERFORMANCE
# ===========================================================

print("\n" + "="*70)
print("AVERAGE EXAM SCORE BY LEARNING PATH")
print("="*70)

print(
    df.groupby("Learning_Path")["Exam_Score"]
      .mean()
      .sort_values(ascending=False)
)


# ===========================================================
# GENDER PERFORMANCE
# ===========================================================

print("\n" + "="*70)
print("AVERAGE EXAM SCORE BY GENDER")
print("="*70)

print(
    df.groupby("Gender")["Exam_Score"]
      .mean()
)


# ===========================================================
# FINAL SUMMARY
# ===========================================================

print("\n" + "="*70)
print("EDA SUMMARY")
print("="*70)

print(f"Total Students          : {len(df)}")
print(f"Total Courses           : {df['Course'].nunique()}")
print(f"Average Attendance      : {df['Attendance'].mean():.2f}")
print(f"Average Exam Score      : {df['Exam_Score'].mean():.2f}")
print(f"Highest Exam Score      : {df['Exam_Score'].max()}")
print(f"Lowest Exam Score       : {df['Exam_Score'].min()}")
print(f"Average Learning Hours  : {df['Learning_Hours'].mean():.2f}")

print("\n" + "="*70)
print("EDA COMPLETED SUCCESSFULLY")
print("6 Professional Charts Saved Inside 'plots' Folder")
print("="*70)