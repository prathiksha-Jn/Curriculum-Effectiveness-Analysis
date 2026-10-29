import pandas as pd
import matplotlib.pyplot as plt
import os

print("="*60)
print("DAY 5 : FRAUD DETECTION - ANOMALY DETECTION")
print("="*60)

# =====================================================
# CREATE OUTPUT FOLDER
# =====================================================

os.makedirs("day5_output", exist_ok=True)

# =====================================================
# LOAD CLEAN DATASET
# =====================================================

df = pd.read_csv("output/Clean_Master_Education_Data.csv")

print("\nDataset Shape :", df.shape)

# =====================================================
# CREATE FRAUD FLAG
# =====================================================

df["Fraud_Flag"] = "Normal"

# Invalid Attendance
df.loc[(df["Attendance"] < 0) | (df["Attendance"] > 100), "Fraud_Flag"] = "Anomaly"

# Invalid Exam Score
df.loc[(df["Exam_Score"] < 0) | (df["Exam_Score"] > 100), "Fraud_Flag"] = "Anomaly"

# Invalid Quiz Score
df.loc[(df["Quiz_Score"] < 0) | (df["Quiz_Score"] > 100), "Fraud_Flag"] = "Anomaly"

# Invalid Assignment Score
df.loc[(df["Assignment_Score"] < 0) | (df["Assignment_Score"] > 100), "Fraud_Flag"] = "Anomaly"

# Invalid Engagement Score
df.loc[(df["Engagement_Score"] < 0) | (df["Engagement_Score"] > 100), "Fraud_Flag"] = "Anomaly"

# Invalid Skill Score
df.loc[(df["Skill_Score"] < 0) | (df["Skill_Score"] > 100), "Fraud_Flag"] = "Anomaly"

# =====================================================
# SEPARATE NORMAL & ANOMALY DATA
# =====================================================

anomaly = df[df["Fraud_Flag"] == "Anomaly"]

normal = df[df["Fraud_Flag"] == "Normal"]

print("\nNormal Records :", len(normal))
print("Anomaly Records :", len(anomaly))

# =====================================================
# SAVE CSV FILES
# =====================================================

normal.to_csv("day5_output/normal_students.csv", index=False)

anomaly.to_csv("day5_output/anomaly_students.csv", index=False)

summary = df["Fraud_Flag"].value_counts()

summary.to_csv("day5_output/anomaly_summary.csv")

# ===========================================   ==========
# BAR CHART
# =====================================================

plt.figure(figsize=(6,5))

summary.plot(kind="bar")

plt.title("Normal vs Anomaly Records")

plt.ylabel("Count")

plt.tight_layout()

plt.savefig("day5_output/anomaly_distribution.png", dpi=300)

plt.close()

# =====================================================
# PIE CHART
# =====================================================

plt.figure(figsize=(6,6))

summary.plot(
    kind="pie",
    autopct="%1.1f%%"
)

plt.ylabel("")

plt.title("Fraud Detection Summary")

plt.tight_layout()

plt.savefig("day5_output/fraud_pie_chart.png", dpi=300)

plt.close()

# =====================================================
# ATTENDANCE OUTLIERS
# =====================================================

plt.figure(figsize=(7,5))

plt.boxplot(df["Attendance"])

plt.title("Attendance Outliers")

plt.savefig("day5_output/attendance_outliers.png", dpi=300)

plt.close()

# =====================================================
# EXAM SCORE OUTLIERS
# =====================================================

plt.figure(figsize=(7,5))

plt.boxplot(df["Exam_Score"])

plt.title("Exam Score Outliers")

plt.savefig("day5_output/examscore_outliers.png", dpi=300)

plt.close()

# =====================================================
# EXAM SCORE DISTRIBUTION
# =====================================================

plt.figure(figsize=(8,5))

plt.hist(df["Exam_Score"], bins=20)

plt.title("Exam Score Distribution")

plt.xlabel("Exam Score")

plt.ylabel("Frequency")

plt.tight_layout()

plt.savefig("day5_output/examscore_distribution.png", dpi=300)

plt.close()

# =====================================================
# FINAL SUMMARY
# =====================================================

print("\n========== DAY 5 SUMMARY ==========")

print("Total Records :", len(df))

print("Normal Records :", len(normal))

print("Anomaly Records :", len(anomaly))

print("\nAll CSV files saved in day5_output folder")

print("All Charts saved in day5_output folder")

print("\nDay 5 Fraud Detection Completed Successfully")
