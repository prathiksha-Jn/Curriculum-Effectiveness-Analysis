import pandas as pd
import numpy as np
import random
from faker import Faker
from datetime import datetime, timedelta

# ----------------------------------------------------------------------------------
# CONFIG
# ----------------------------------------------------------------------------------
N = 50000
RANDOM_SEED = 73

random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)
fake = Faker()
Faker.seed(RANDOM_SEED)

# ----------------------------------------------------------------------------------
# REFERENCE DATA
# ----------------------------------------------------------------------------------
DEPARTMENTS = [
    "Computer Science",
    "Artificial Intelligence",
    "Information Technology",
    "Electronics",
    "Business Analytics",
]

COURSES = [
    "Data Science",
    "Artificial Intelligence",
    "Machine Learning",
    "Cyber Security",
    "Cloud Computing",
    "Software Engineering",
]

COURSE_SUBJECTS = {
    "Artificial Intelligence": ["Deep Learning", "NLP", "Computer Vision"],
    "Data Science": ["Statistics", "Data Mining", "Data Visualization"],
    "Cyber Security": ["Ethical Hacking", "Network Security", "Cryptography"],
    "Machine Learning": ["Supervised Learning", "Reinforcement Learning", "Neural Networks"],
    "Cloud Computing": ["AWS", "Azure", "DevOps"],
    "Software Engineering": ["Java Programming", "Python Programming", "Web Development"],
}

# Department -> preferred course weights (adds realism: departments feed certain courses more)
DEPARTMENT_COURSE_WEIGHTS = {
    "Computer Science":          {"Data Science": 0.22, "Artificial Intelligence": 0.16, "Machine Learning": 0.20,
                                   "Cyber Security": 0.14, "Cloud Computing": 0.12, "Software Engineering": 0.16},
    "Artificial Intelligence":   {"Data Science": 0.15, "Artificial Intelligence": 0.38, "Machine Learning": 0.30,
                                   "Cyber Security": 0.05, "Cloud Computing": 0.06, "Software Engineering": 0.06},
    "Information Technology":    {"Data Science": 0.12, "Artificial Intelligence": 0.08, "Machine Learning": 0.10,
                                   "Cyber Security": 0.28, "Cloud Computing": 0.28, "Software Engineering": 0.14},
    "Electronics":                {"Data Science": 0.10, "Artificial Intelligence": 0.10, "Machine Learning": 0.12,
                                   "Cyber Security": 0.24, "Cloud Computing": 0.24, "Software Engineering": 0.20},
    "Business Analytics":        {"Data Science": 0.42, "Artificial Intelligence": 0.10, "Machine Learning": 0.12,
                                   "Cyber Security": 0.08, "Cloud Computing": 0.10, "Software Engineering": 0.18},
}

GENDERS = ["Male", "Female", "Non-Binary"]
GENDER_WEIGHTS = [0.49, 0.47, 0.04]

COMPLETION_STATES = ["Completed", "In Progress", "Dropped"]
PLACEMENT_STATES = ["Placed", "Not Placed"]
CERT_STATES = ["Yes", "No"]

TEACHERS = [
    "Dr. Ananya Krishnan", "Prof. Rajesh Menon", "Dr. Meera Iyer", "Prof. Suresh Nair",
    "Dr. Kavitha Reddy", "Prof. Arvind Rao", "Dr. Priya Deshmukh", "Prof. Vikram Sharma",
    "Dr. Sandhya Pillai", "Prof. Karthik Subramaniam", "Dr. Neha Kulkarni", "Prof. Ramesh Gupta",
    "Dr. Lakshmi Narayanan", "Prof. Deepak Verma", "Dr. Shalini Bhat",
]

# Persistent per-teacher and per-course performance targets/shifts (creates natural, repeatable
# but non-uniform differences between teachers and courses)
TEACHER_SHIFT = {t: np.random.uniform(-5, 5) for t in TEACHERS}

COURSE_TARGET_EXAM_MEAN = {
    "Artificial Intelligence": 87,
    "Data Science": 82,
    "Cyber Security": 76,
    "Machine Learning": 71,
    "Cloud Computing": 65,
    "Software Engineering": 58,
}

DEPARTMENT_SHIFT = {d: np.random.uniform(-3, 3) for d in DEPARTMENTS}

GENDER_SHIFT = {"Male": 0.0, "Female": 0.6, "Non-Binary": -0.4}

# ----------------------------------------------------------------------------------
# HELPER FUNCTIONS
# ----------------------------------------------------------------------------------

def random_enrollment_date():
    start = datetime(2024, 1, 1)
    end = datetime(2025, 12, 31)
    delta_days = (end - start).days
    # Weight enrollments slightly heavier around typical intake months (Jan, Jul, Aug)
    day_offset = int(np.clip(np.random.normal(delta_days / 2, delta_days / 3.2), 0, delta_days))
    return start + timedelta(days=day_offset)


def assign_course(department):
    weights = DEPARTMENT_COURSE_WEIGHTS[department]
    return random.choices(list(weights.keys()), weights=list(weights.values()), k=1)[0]


def assign_subject_and_teacher(course):
    subject = random.choice(COURSE_SUBJECTS[course])
    teacher = random.choice(TEACHERS)
    return subject, teacher


# ----------------------------------------------------------------------------------
# STEP 1 — CORE CATEGORICAL / IDENTITY FIELDS
# ----------------------------------------------------------------------------------
print("Generating core identity fields...")

student_ids = [f"STU{100000 + i}" for i in range(N)]
student_names = [fake.name() for _ in range(N)]
genders = np.random.choice(GENDERS, size=N, p=GENDER_WEIGHTS)
ages = np.clip(np.random.normal(21, 2.3, N).round().astype(int), 18, 30)

departments = np.random.choice(DEPARTMENTS, size=N, p=[0.28, 0.20, 0.20, 0.14, 0.18])
courses = np.array([assign_course(d) for d in departments])

subjects = []
teachers = []
for c in courses:
    s, t = assign_subject_and_teacher(c)
    subjects.append(s)
    teachers.append(t)
subjects = np.array(subjects)
teachers = np.array(teachers)

enrollment_dates = [random_enrollment_date() for _ in range(N)]

# ----------------------------------------------------------------------------------
# STEP 2 — HIDDEN PERFORMANCE TIER (drives realistic clustering, no explicit column)
# ----------------------------------------------------------------------------------
print("Assigning latent performance tiers...")

tiers = np.random.choice(
    ["High", "Average", "Low", "AtRisk"], size=N, p=[0.20, 0.45, 0.25, 0.10]
)

TIER_ATTENDANCE = {"High": (92, 5), "Average": (78, 8), "Low": (62, 10), "AtRisk": (45, 12)}
TIER_LEARNING_HOURS = {"High": (170, 35), "Average": (110, 30), "Low": (70, 25), "AtRisk": (35, 18)}
TIER_BONUS = {"High": 10, "Average": 2, "Low": -6, "AtRisk": -14}

# ----------------------------------------------------------------------------------
# STEP 3 — ATTENDANCE (baseline, tier driven)
# ----------------------------------------------------------------------------------
print("Generating attendance...")

attendance = np.zeros(N)
for tier, (mean, std) in TIER_ATTENDANCE.items():
    mask = tiers == tier
    attendance[mask] = np.random.normal(mean, std, mask.sum())
attendance = np.clip(attendance, 0, 100)

# ----------------------------------------------------------------------------------
# STEP 4 — ENGAGEMENT (attendance driven + tier bonus + noise)
# ----------------------------------------------------------------------------------
print("Generating engagement scores...")

tier_bonus_arr = np.array([TIER_BONUS[t] for t in tiers])
engagement = 0.55 * attendance + tier_bonus_arr + np.random.normal(0, 7, N)
engagement = np.clip(engagement, 0, 100)

# ----------------------------------------------------------------------------------
# STEP 5 — QUIZ SCORE (engagement driven)
# ----------------------------------------------------------------------------------
print("Generating quiz scores...")

quiz_score = 0.5 * engagement + 0.25 * tier_bonus_arr + np.random.normal(0, 8, N) + 25
quiz_score = np.clip(quiz_score, 0, 100)

# ----------------------------------------------------------------------------------
# STEP 6 — ASSIGNMENT SCORE (quiz + engagement driven)
# ----------------------------------------------------------------------------------
print("Generating assignment scores...")

assignment_score = 0.45 * quiz_score + 0.35 * engagement + np.random.normal(0, 6, N) + 8
assignment_score = np.clip(assignment_score, 0, 100)

# ----------------------------------------------------------------------------------
# STEP 7 — LEARNING HOURS (tier driven, feeds skill score)
# ----------------------------------------------------------------------------------
print("Generating learning hours...")

learning_hours = np.zeros(N)
for tier, (mean, std) in TIER_LEARNING_HOURS.items():
    mask = tiers == tier
    learning_hours[mask] = np.random.normal(mean, std, mask.sum())
learning_hours = np.clip(learning_hours, 5, 250)

# ----------------------------------------------------------------------------------
# STEP 8 — SKILL SCORE (learning hours + engagement + tier driven)
# ----------------------------------------------------------------------------------
print("Generating skill scores...")

lh_scaled = (learning_hours - learning_hours.min()) / (learning_hours.max() - learning_hours.min()) * 100
skill_score = 0.5 * lh_scaled + 0.3 * engagement + 0.2 * tier_bonus_arr + np.random.normal(0, 6, N) + 5
skill_score = np.clip(skill_score, 0, 100)

# ----------------------------------------------------------------------------------
# STEP 9 — EXAM SCORE (attendance / engagement / assignment / skill driven,
#           then adjusted for course, department, teacher and gender differences)
# ----------------------------------------------------------------------------------
print("Generating exam scores with course/teacher/department adjustments...")

exam_raw = (
    0.40 * attendance
    + 0.25 * engagement
    + 0.20 * assignment_score
    + 0.15 * skill_score
    + np.random.normal(0, 6, N)
)

teacher_shift_arr = np.array([TEACHER_SHIFT[t] for t in teachers])
department_shift_arr = np.array([DEPARTMENT_SHIFT[d] for d in departments])
gender_shift_arr = np.array([GENDER_SHIFT[g] for g in genders])

exam_score = exam_raw + teacher_shift_arr + department_shift_arr + gender_shift_arr

# Rescale per-course so course averages land near the target academic differences
exam_df_tmp = pd.DataFrame({"course": courses, "exam": exam_score})
course_means = exam_df_tmp.groupby("course")["exam"].transform("mean")
course_targets = exam_df_tmp["course"].map(COURSE_TARGET_EXAM_MEAN)
exam_score = exam_score + (course_targets.values - course_means.values)

# Propagate a portion of the course-level shift back into quiz/assignment/skill/engagement
# so that "clear academic differences" show up consistently across metrics, not just exams
course_shift = (course_targets.values - course_means.values)
quiz_score = np.clip(quiz_score + 0.35 * course_shift, 0, 100)
assignment_score = np.clip(assignment_score + 0.30 * course_shift, 0, 100)
skill_score = np.clip(skill_score + 0.25 * course_shift, 0, 100)
engagement = np.clip(engagement + 0.15 * course_shift, 0, 100)

exam_score = np.clip(exam_score, 0, 100)

# Enforce the strong attendance -> exam relationship requested
high_att_mask = attendance > 90
low_att_mask = attendance < 60

boost_apply = high_att_mask & (np.random.rand(N) < 0.85) & (exam_score < 80)
exam_score[boost_apply] = np.random.uniform(80, 98, boost_apply.sum())

penalty_apply = low_att_mask & (np.random.rand(N) < 0.85) & (exam_score > 55)
exam_score[penalty_apply] = np.random.uniform(15, 55, penalty_apply.sum())

exam_score = np.clip(exam_score, 0, 100)

# ----------------------------------------------------------------------------------
# STEP 10 — COURSE COMPLETION / PLACEMENT / CERTIFICATE
# ----------------------------------------------------------------------------------
print("Generating completion, placement and certificate outcomes...")

completion_score = 0.5 * attendance + 0.3 * exam_score + 0.2 * engagement + np.random.normal(0, 8, N)
course_completion = np.where(
    completion_score > 78, "Completed",
    np.where(completion_score > 50, "In Progress", "Dropped")
)
# introduce some natural noise so it isn't a hard rule
noise_flip = np.random.rand(N) < 0.06
random_state = np.random.choice(COMPLETION_STATES, size=N)
course_completion = np.where(noise_flip, random_state, course_completion)

placement_prob = 1 / (1 + np.exp(-(skill_score - 60) / 10))  # logistic curve on skill score
placement_status = np.where(
    (np.random.rand(N) < placement_prob) & (course_completion != "Dropped"),
    "Placed", "Not Placed"
)

cert_prob = np.where(course_completion == "Completed", 0.82,
             np.where(course_completion == "In Progress", 0.12, 0.02))
certificate_earned = np.where(np.random.rand(N) < cert_prob, "Yes", "No")

# ----------------------------------------------------------------------------------
# STEP 11 — ASSEMBLE DATAFRAME
# ----------------------------------------------------------------------------------
print("Assembling dataframe...")

df = pd.DataFrame({
    "Student_ID": student_ids,
    "Student_Name": student_names,
    "Gender": genders,
    "Age": ages,
    "Department": departments,
    "Course": courses,
    "Subject": subjects,
    "Teacher": teachers,
    "Enrollment_Date": [d.strftime("%d-%b-%Y") for d in enrollment_dates],
    "Attendance": attendance.round(1),
    "Quiz_Score": quiz_score.round(1),
    "Assignment_Score": assignment_score.round(1),
    "Exam_Score": exam_score.round(1),
    "Engagement_Score": engagement.round(1),
    "Skill_Score": skill_score.round(1),
    "Learning_Hours": learning_hours.round(1),
    "Course_Completion": course_completion,
    "Placement_Status": placement_status,
    "Certificate_Earned": certificate_earned,
})

# ----------------------------------------------------------------------------------
# STEP 12 — DATA QUALITY ISSUES (missing values, duplicates, invalid values)
# ----------------------------------------------------------------------------------
print("Injecting realistic data quality issues...")

# --- 1% duplicate records: replace tail rows with exact duplicates of earlier rows ---
n_dupes = int(N * 0.01)
dupe_source_idx = np.random.choice(df.index[:-n_dupes], n_dupes, replace=False)
dupe_target_idx = df.index[-n_dupes:]
df.loc[dupe_target_idx, :] = df.loc[dupe_source_idx, :].values

# --- 2% missing values spread across non-ID columns ---
missing_candidate_cols = [
    "Student_Name", "Gender", "Age", "Attendance", "Quiz_Score", "Assignment_Score",
    "Exam_Score", "Engagement_Score", "Skill_Score", "Learning_Hours",
    "Course_Completion", "Placement_Status", "Certificate_Earned",
]
n_missing_per_col = int(N * 0.02)
for col in missing_candidate_cols:
    miss_idx = np.random.choice(df.index, size=n_missing_per_col, replace=False)
    df.loc[miss_idx, col] = np.nan

# --- 2% invalid / out-of-range values on selected numeric columns ---
n_invalid_each = int(N * 0.02 / 5)

# Attendance > 100
idx = np.random.choice(df.index, n_invalid_each, replace=False)
df.loc[idx, "Attendance"] = np.round(np.random.uniform(101, 140, len(idx)), 1)

# Attendance < 0
idx = np.random.choice(df.index, n_invalid_each, replace=False)
df.loc[idx, "Attendance"] = np.round(np.random.uniform(-30, -1, len(idx)), 1)

# Exam Score > 100
idx = np.random.choice(df.index, n_invalid_each, replace=False)
df.loc[idx, "Exam_Score"] = np.round(np.random.uniform(101, 150, len(idx)), 1)

# Exam Score < 0
idx = np.random.choice(df.index, n_invalid_each, replace=False)
df.loc[idx, "Exam_Score"] = np.round(np.random.uniform(-40, -1, len(idx)), 1)

# Quiz Score > 100
idx = np.random.choice(df.index, n_invalid_each, replace=False)
df.loc[idx, "Quiz_Score"] = np.round(np.random.uniform(101, 130, len(idx)), 1)

# Negative Skill Score
idx = np.random.choice(df.index, n_invalid_each, replace=False)
df.loc[idx, "Skill_Score"] = np.round(np.random.uniform(-25, -1, len(idx)), 1)

# Learning Hours < 0
idx = np.random.choice(df.index, n_invalid_each, replace=False)
df.loc[idx, "Learning_Hours"] = np.round(np.random.uniform(-15, -1, len(idx)), 1)

# ----------------------------------------------------------------------------------
# STEP 13 — NATURAL STATISTICAL OUTLIERS (subtle, not obviously flagged)
# ----------------------------------------------------------------------------------
print("Adding subtle statistical outliers...")

outlier_idx = np.random.choice(df.index, int(N * 0.005), replace=False)
for col in ["Quiz_Score", "Assignment_Score", "Engagement_Score"]:
    sub_idx = np.random.choice(outlier_idx, int(len(outlier_idx) / 3), replace=False)
    current_vals = pd.to_numeric(df.loc[sub_idx, col], errors="coerce")
    df.loc[sub_idx, col] = np.clip(current_vals + np.random.choice([-1, 1], len(sub_idx)) * np.random.uniform(25, 40, len(sub_idx)), 0, 100).round(1)

outlier_lh_idx = np.random.choice(df.index, int(N * 0.003), replace=False)
df.loc[outlier_lh_idx, "Learning_Hours"] = np.round(np.random.uniform(230, 250, len(outlier_lh_idx)), 1)

# ----------------------------------------------------------------------------------
# STEP 14 — FINAL SHUFFLE & EXPORT
# ----------------------------------------------------------------------------------
print("Shuffling and exporting final dataset...")

df = df.sample(frac=1, random_state=RANDOM_SEED).reset_index(drop=True)

output_path = "Master_Education_Analytics_Dataset.csv"
df.to_csv(output_path, index=False)

print(f"Dataset generated successfully: {output_path}")
print(f"Total records: {len(df)}")