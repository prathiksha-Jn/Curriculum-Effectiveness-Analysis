"""
student_segmentation.py
Curriculum Effectiveness Analysis
Day 3 - Student Segmentation using K-Means
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

print("="*70)
print("CURRICULUM EFFECTIVENESS ANALYSIS")
print("STUDENT SEGMENTATION USING K-MEANS")
print("="*70)

df = pd.read_excel("output/Clean_Master_Education_Data.xlsx")

features = [
    "Attendance",
    "Learning_Hours",
    "Quiz_Score",
    "Assignment_Score",
    "Exam_Score"
]

X = df[features]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

os.makedirs("segmentation_plots", exist_ok=True)

# Elbow Method
wcss = []
for k in range(1, 11):
    model = KMeans(n_clusters=k, random_state=42, n_init=10)
    model.fit(X_scaled)
    wcss.append(model.inertia_)

plt.figure(figsize=(8,5))
plt.plot(range(1,11), wcss, marker="o")
plt.title("Elbow Method")
plt.xlabel("Number of Clusters")
plt.ylabel("WCSS")
plt.grid(True)
plt.tight_layout()
plt.savefig("segmentation_plots/01_elbow_method.png")
plt.close()

# Final Model
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
df["Cluster"] = kmeans.fit_predict(X_scaled)

# Automatic Labels based on Exam Score
cluster_perf = df.groupby("Cluster")["Exam_Score"].mean().sort_values()

mapping = {}
mapping[cluster_perf.index[0]] = "At Risk Student"
mapping[cluster_perf.index[1]] = "Average Performer"
mapping[cluster_perf.index[2]] = "High Performer"

df["Student_Segment"] = df["Cluster"].map(mapping)

# Charts
plt.figure(figsize=(7,5))
sns.countplot(data=df,x="Student_Segment",
              order=["High Performer","Average Performer","At Risk Student"])
plt.title("Student Segment Distribution")
plt.tight_layout()
plt.savefig("segmentation_plots/02_segment_distribution.png")
plt.close()

plt.figure(figsize=(8,6))
sns.scatterplot(data=df,x="Learning_Hours",y="Exam_Score",
                hue="Student_Segment")
plt.title("Learning Hours vs Exam Score")
plt.tight_layout()
plt.savefig("segmentation_plots/03_learning_vs_exam.png")
plt.close()

plt.figure(figsize=(8,6))
sns.scatterplot(data=df,x="Attendance",y="Exam_Score",
                hue="Student_Segment")
plt.title("Attendance vs Exam Score")
plt.tight_layout()
plt.savefig("segmentation_plots/04_attendance_vs_exam.png")
plt.close()

summary = df.groupby("Student_Segment")[features].mean()

print("\nSEGMENT SUMMARY")
print(summary)

df.to_excel("output/Segmented_Students.xlsx", index=False)

print("\nSegmentation Completed Successfully.")
print("Charts saved in segmentation_plots/")
print("Dataset saved as output/Segmented_Students.xlsx")
