import pandas as pd
import matplotlib.pyplot as plt
import os

# =====================================================
# CREATE OUTPUT FOLDER
# =====================================================

os.makedirs("day4_output", exist_ok=True)

print("=" * 60)
print("DAY 4 : COURSE PERFORMANCE ANALYSIS")
print("=" * 60)

# =====================================================
# LOAD DATASET
# =====================================================

df = pd.read_csv("output/Clean_Master_Education_Data.csv")

# =====================================================
# DATASET OVERVIEW
# =====================================================

print("\nDataset Shape :", df.shape)

print("\nColumns")
print(df.columns.tolist())

# =====================================================
# OVERALL PERFORMANCE
# =====================================================

print("\nOverall Performance")

print("Average Exam Score      :", round(df["Exam_Score"].mean(), 2))
print("Average Quiz Score      :", round(df["Quiz_Score"].mean(), 2))
print("Average Assignment Score:", round(df["Assignment_Score"].mean(), 2))
print("Average Attendance      :", round(df["Attendance"].mean(), 2))
print("Average Engagement      :", round(df["Engagement_Score"].mean(), 2))
print("Average Skill Score     :", round(df["Skill_Score"].mean(), 2))
# =====================================================
# COURSE PERFORMANCE
# =====================================================

course = df.groupby("Course")["Exam_Score"].mean().sort_values(ascending=False)

print("\nAverage Exam Score by Course")
print(course)

plt.figure(figsize=(10,5))

course.plot(
    kind="bar",
    color="steelblue",
    edgecolor="black"
)

plt.title("Course Performance")
plt.xlabel("Course")
plt.ylabel("Average Exam Score")

plt.tight_layout()

plt.savefig(
    "day4_output/course_performance.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()

# =====================================================
# SUBJECT PERFORMANCE
# =====================================================

subject = df.groupby("Subject")["Exam_Score"].mean().sort_values(ascending=False)

print("\nSubject Performance")
print(subject)

plt.figure(figsize=(10,5))

subject.plot(
    kind="bar",
    color="green",
    edgecolor="black"
)

plt.title("Subject Performance")
plt.xlabel("Subject")
plt.ylabel("Average Exam Score")

plt.tight_layout()

plt.savefig(
    "day4_output/subject_performance.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()

# =====================================================
# DEPARTMENT PERFORMANCE
# =====================================================

department = df.groupby("Department")["Exam_Score"].mean().sort_values(ascending=False)

print("\nDepartment Performance")
print(department)

plt.figure(figsize=(8,5))

department.plot(
    kind="bar",
    color="orange",
    edgecolor="black"
)

plt.title("Department Performance")
plt.xlabel("Department")
plt.ylabel("Average Exam Score")

plt.tight_layout()

plt.savefig(
    "day4_output/department_performance.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()
# =====================================================
# TEACHER PERFORMANCE
# =====================================================

teacher = df.groupby("Teacher")["Exam_Score"].mean().sort_values(ascending=False)

print("\nTeacher Performance")
print(teacher)

plt.figure(figsize=(12,5))

teacher.plot(
    kind="bar",
    color="purple",
    edgecolor="black"
)

plt.title("Teacher Performance")
plt.xlabel("Teacher")
plt.ylabel("Average Exam Score")

plt.tight_layout()

plt.savefig(
    "day4_output/teacher_performance.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()

# =====================================================
# GENDER PERFORMANCE
# =====================================================

gender = df.groupby("Gender")["Exam_Score"].mean()

print("\nGender Performance")
print(gender)

plt.figure(figsize=(5,4))

gender.plot(
    kind="bar",
    color=["skyblue", "pink"],
    edgecolor="black"
)

plt.title("Gender Performance")
plt.xlabel("Gender")
plt.ylabel("Average Exam Score")

plt.tight_layout()

plt.savefig(
    "day4_output/gender_performance.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()

# =====================================================
# ATTENDANCE VS EXAM SCORE
# =====================================================

plt.figure(figsize=(7,5))

plt.scatter(
    df["Attendance"],
    df["Exam_Score"],
    color="blue",
    alpha=0.6
)

plt.xlabel("Attendance")
plt.ylabel("Exam Score")
plt.title("Attendance vs Exam Score")

plt.grid(True)

plt.tight_layout()

plt.savefig(
    "day4_output/attendance_vs_examscore.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()

# =====================================================
# ENGAGEMENT VS EXAM SCORE
# =====================================================

plt.figure(figsize=(7,5))

plt.scatter(
    df["Engagement_Score"],
    df["Exam_Score"],
    color="green",
    alpha=0.6
)

plt.xlabel("Engagement Score")
plt.ylabel("Exam Score")
plt.title("Engagement vs Exam Score")

plt.grid(True)

plt.tight_layout()

plt.savefig(
    "day4_output/engagement_vs_examscore.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()
# =====================================================
# TOP 10 STUDENTS
# =====================================================

top = df.sort_values(
    by="Exam_Score",
    ascending=False
).head(10)

print("\nTop 10 Students")
print(top[[
    "Student_ID",
    "Course",
    "Exam_Score"
]])

# =====================================================
# LOW PERFORMING STUDENTS
# =====================================================

low = df.sort_values(
    by="Exam_Score",
    ascending=True
).head(10)

print("\nLow Performing Students")
print(low[[
    "Student_ID",
    "Course",
    "Exam_Score"
]])

# =====================================================
# CORRELATION MATRIX
# =====================================================

numeric = df.select_dtypes(include="number")

corr = numeric.corr()

plt.figure(figsize=(10,8))

plt.imshow(
    corr,
    cmap="coolwarm",
    aspect="auto"
)

plt.xticks(
    range(len(corr.columns)),
    corr.columns,
    rotation=90
)

plt.yticks(
    range(len(corr.columns)),
    corr.columns
)

plt.colorbar()

plt.title("Correlation Matrix")

plt.tight_layout()

plt.savefig(
    "day4_output/correlation_matrix.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

plt.close()

# =====================================================
# FINAL SUMMARY
# =====================================================

print("\n" + "="*60)
print("DAY 4 PERFORMANCE SUMMARY")
print("="*60)

print("Highest Exam Score      :", df["Exam_Score"].max())
print("Lowest Exam Score       :", df["Exam_Score"].min())
print("Average Exam Score      :", round(df["Exam_Score"].mean(),2))
print("Average Attendance      :", round(df["Attendance"].mean(),2))
print("Average Engagement      :", round(df["Engagement_Score"].mean(),2))
print("Average Skill Score     :", round(df["Skill_Score"].mean(),2))

print("\nOutput Files Saved In : day4_output/")

print("""
Generated Files:
✔ course_performance.png
✔ subject_performance.png
✔ department_performance.png
✔ teacher_performance.png
✔ gender_performance.png
✔ attendance_vs_examscore.png
✔ engagement_vs_examscore.png
✔ correlation_matrix.png
""")

print("="*60)
print("DAY 4 PERFORMANCE ANALYSIS COMPLETED SUCCESSFULLY")
print("="*60)