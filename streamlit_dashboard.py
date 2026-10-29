import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Curriculum Effectiveness Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# CUSTOM CSS
# =====================================================

# =====================================================
# MODERN COLORFUL UI
# =====================================================

st.markdown("""
<style>

/* ---------- MAIN BACKGROUND ---------- */

.stApp {
    background: linear-gradient(135deg, #F7F8FC 0%, #EEF2FF 100%);
}

/* ---------- MAIN CONTENT ---------- */

.main .block-container {
    padding-top: 2rem;
    padding-left: 3rem;
    padding-right: 3rem;
}

/* ---------- SIDEBAR ---------- */

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #172033 0%, #312E81 55%, #5B21B6 100%);
    border-right: 1px solid rgba(255,255,255,0.08);
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: white !important;
}

/* ---------- SIDEBAR INPUTS ---------- */

section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.20);
    border-radius: 10px;
}

section[data-testid="stSidebar"] input {
    color: white !important;
}

/* ---------- TITLE ---------- */

h1 {
    color: #312E81 !important;
    font-weight: 800 !important;
    letter-spacing: -1px;
}

h2 {
    color: #4338CA !important;
    font-weight: 750 !important;
}

h3 {
    color: #5B21B6 !important;
}

/* ---------- KPI CARDS ---------- */

div[data-testid="metric-container"] {
    background: white;
    padding: 20px;
    border-radius: 18px;
    border: 1px solid #E5E7EB;
    box-shadow: 0 8px 25px rgba(49,46,129,0.10);
    transition: all 0.25s ease;
}

div[data-testid="metric-container"]:hover {
    transform: translateY(-5px);
    box-shadow: 0 14px 30px rgba(49,46,129,0.18);
}

/* KPI VALUE */

div[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #312E81;
    font-weight: 800;
    font-size: 30px;
}

/* KPI LABEL */

div[data-testid="metric-container"] [data-testid="stMetricLabel"] {
    color: #64748B;
    font-weight: 600;
}

/* ---------- TABS ---------- */

button[data-baseweb="tab"] {
    font-weight: 700;
    color: #64748B;
    border-radius: 10px 10px 0 0;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #6C5CE7 !important;
    border-bottom: 3px solid #6C5CE7 !important;
}

/* ---------- DATAFRAME ---------- */

div[data-testid="stDataFrame"] {
    border-radius: 14px;
    overflow: hidden;
    border: 1px solid #E5E7EB;
    box-shadow: 0 5px 18px rgba(0,0,0,0.06);
}

/* ---------- BUTTONS ---------- */

.stDownloadButton button {
    background: linear-gradient(135deg, #6C5CE7, #8B5CF6);
    color: white !important;
    border: none;
    border-radius: 12px;
    font-weight: 700;
    padding: 10px 20px;
    transition: 0.25s;
}

.stDownloadButton button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(108,92,231,0.30);
}

/* ---------- SUCCESS BOX ---------- */

div[data-testid="stAlert"] {
    border-radius: 14px;
}

/* ---------- DIVIDER ---------- */

hr {
    border: none;
    height: 2px;
    background: linear-gradient(
        90deg,
        #6C5CE7,
        #0984E3,
        #00B894,
        #E84393
    );
    margin: 25px 0;
}

/* ---------- MULTISELECT TAGS ---------- */

span[data-baseweb="tag"] {
    background: #6C5CE7 !important;
    color: white !important;
    border-radius: 8px !important;
}

/* ---------- SCROLLBAR ---------- */

::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: #F1F5F9;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(#6C5CE7, #0984E3);
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# LOAD DATA
# =====================================================

DATA_PATH="output/Clean_Master_Education_Data.csv"

if not os.path.exists(DATA_PATH):
    st.error("Dataset not found")
    st.stop()

df=pd.read_csv(DATA_PATH)

# =====================================================
# HEADER
# =====================================================

st.title("🎓 Curriculum Effectiveness Analysis Dashboard")

st.write(
"""
Welcome to the interactive dashboard for analysing
student performance, curriculum effectiveness,
engagement, attendance and learning outcomes.
"""
)

st.divider()

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.image(
"https://img.icons8.com/color/96/graduation-cap.png",
width=70
)

st.sidebar.title("Dashboard Filters")

course=st.sidebar.multiselect(
"Course",
sorted(df["Course"].unique()),
default=sorted(df["Course"].unique())
)

department=st.sidebar.multiselect(
"Department",
sorted(df["Department"].unique()),
default=sorted(df["Department"].unique())
)

teacher=st.sidebar.multiselect(
"Teacher",
sorted(df["Teacher"].unique()),
default=sorted(df["Teacher"].unique())
)

gender=st.sidebar.multiselect(
"Gender",
sorted(df["Gender"].unique()),
default=sorted(df["Gender"].unique())
)

filtered_df=df[
(df["Course"].isin(course))&
(df["Department"].isin(department))&
(df["Teacher"].isin(teacher))&
(df["Gender"].isin(gender))
]

st.sidebar.success(f"Records : {len(filtered_df)}")
# =====================================================
# KPI SECTION
# =====================================================

st.subheader("📊 Key Performance Indicators")

# -----------------------------------------------------
# KPI VALUES
# -----------------------------------------------------

total_students = len(filtered_df)

avg_exam_score = filtered_df["Exam_Score"].mean()

avg_attendance = filtered_df["Attendance"].mean()

avg_engagement = filtered_df["Engagement_Score"].mean()

active_courses = filtered_df["Course"].nunique()

active_teachers = filtered_df["Teacher"].nunique()


# =====================================================
# KPI CARD DESIGN
# =====================================================

st.markdown("""
<style>
.kpi-row {
    display: flex;
    gap: 18px;
    width: 100%;
    margin-top: 15px;
    margin-bottom: 25px;
}
.kpi-card {
    flex: 1;
    background: #FFFFFF;
    border-radius: 18px;
    padding: 18px;
    min-height: 145px;
    box-sizing: border-box;
    box-shadow: 0 6px 18px rgba(0,0,0,0.08);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.kpi-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 28px rgba(0,0,0,0.14);
}
.kpi-purple { border: 2px solid #6C5CE7; }
.kpi-blue { border: 2px solid #0984E3; }
.kpi-green { border: 2px solid #00B894; }
.kpi-pink { border: 2px solid #E84393; }
.kpi-orange { border: 2px solid #F39C12; }
.kpi-indigo { border: 2px solid #8E44AD; }
.kpi-icon { font-size: 25px; margin-bottom: 8px; }
.kpi-title { font-size: 14px; font-weight: 700; color: #475569; margin-bottom: 5px; }
.kpi-value { font-size: 28px; font-weight: 800; color: #1E293B; margin-bottom: 5px; }
.kpi-desc { font-size: 11px; color: #94A3B8; }
@media (max-width: 1200px) {
    .kpi-row { display: grid; grid-template-columns: repeat(3, 1fr); }
}
</style>
""", unsafe_allow_html=True)


# =====================================================
# KPI ROW
# =====================================================

kpi_html = f"""
<div class="kpi-row">
<div class="kpi-card kpi-purple">
<div class="kpi-icon">👨‍🎓</div>
<div class="kpi-title">Total Students</div>
<div class="kpi-value">{total_students:,}</div>
<div class="kpi-desc">Students in selected filters</div>
</div>
<div class="kpi-card kpi-blue">
<div class="kpi-icon">📝</div>
<div class="kpi-title">Avg Exam Score</div>
<div class="kpi-value">{avg_exam_score:.2f}</div>
<div class="kpi-desc">Average student exam performance</div>
</div>
<div class="kpi-card kpi-green">
<div class="kpi-icon">📅</div>
<div class="kpi-title">Avg Attendance</div>
<div class="kpi-value">{avg_attendance:.2f}%</div>
<div class="kpi-desc">Average student attendance</div>
</div>
<div class="kpi-card kpi-pink">
<div class="kpi-icon">🎯</div>
<div class="kpi-title">Avg Engagement</div>
<div class="kpi-value">{avg_engagement:.2f}</div>
<div class="kpi-desc">Average student engagement</div>
</div>
<div class="kpi-card kpi-orange">
<div class="kpi-icon">📚</div>
<div class="kpi-title">Active Courses</div>
<div class="kpi-value">{active_courses}</div>
<div class="kpi-desc">Courses in selected data</div>
</div>
<div class="kpi-card kpi-indigo">
<div class="kpi-icon">👨‍🏫</div>
<div class="kpi-title">Active Teachers</div>
<div class="kpi-value">{active_teachers}</div>
<div class="kpi-desc">Teachers in selected data</div>
</div>
</div>
"""

st.markdown(kpi_html, unsafe_allow_html=True)

st.divider()
# =====================================================
# PERFORMANCE ANALYSIS
# =====================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "📚 Course",
    "📖 Subject",
    "🏢 Department",
    "👨‍🏫 Teacher"
])
# =====================================================
# COURSE PERFORMANCE
# =====================================================

with tab1:

    st.subheader("📚 Course Performance")

    course_df = (
        filtered_df.groupby("Course")["Exam_Score"]
        .mean()
        .reset_index()
        .sort_values("Exam_Score", ascending=False)
    )

    # -------------------------------------------------
    # TOP COURSE
    # -------------------------------------------------

    best_course = course_df.iloc[0]["Course"]
    best_score = course_df.iloc[0]["Exam_Score"]

    st.success(
        f"🏆 Best Performing Course: {best_course}  |  "
        f"Average Exam Score: {best_score:.2f}"
    )

    # -------------------------------------------------
    # CHART + TABLE
    # -------------------------------------------------

    col1, col2 = st.columns([2, 1])

    # -------------------------------------------------
    # COURSE CHART
    # -------------------------------------------------

    with col1:

        fig = px.bar(
            course_df,
            x="Course",
            y="Exam_Score",
            color="Exam_Score",
            text="Exam_Score",
            color_continuous_scale=[
                "#EDE9FE",
                "#C4B5FD",
                "#8B5CF6",
                "#6D28D9"
            ],
            title="Average Exam Score by Course"
        )

        fig.update_traces(
            texttemplate="%{text:.2f}",
            textposition="outside",
            marker_line_width=0
        )

        fig.update_layout(
            height=450,

            title=dict(
                text="Average Exam Score by Course",
                font=dict(
                    size=20,
                    color="#312E81"
                ),
                x=0.02
            ),

            xaxis=dict(
                title="Course",
                showgrid=False,
                tickangle=-20,
                tickfont=dict(
                    size=12,
                    color="#64748B"
                )
            ),

            yaxis=dict(
                title="Average Exam Score",
                showgrid=True,
                gridcolor="#E5E7EB",
                zeroline=False,
                tickfont=dict(
                    color="#64748B"
                )
            ),

            plot_bgcolor="white",
            paper_bgcolor="white",

            margin=dict(
                l=50,
                r=30,
                t=70,
                b=80
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # -------------------------------------------------
    # COURSE TABLE
    # -------------------------------------------------

    with col2:

        st.subheader("📋 Course Summary")

        course_table = course_df.rename(
            columns={
                "Exam_Score": "Average Score"
            }
        )

        st.dataframe(
            course_table,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Course": st.column_config.TextColumn(
                    "Course"
                ),
                "Average Score": st.column_config.NumberColumn(
                    "Average Score",
                    format="%.2f"
                )
            }
        )
# =====================================================
# SUBJECT PERFORMANCE
# =====================================================

with tab2:

    st.subheader("📖 Subject Performance")

    subject_df = (
        filtered_df.groupby("Subject")["Exam_Score"]
        .mean()
        .reset_index()
        .sort_values("Exam_Score", ascending=False)
    )

    col1, col2 = st.columns([2,1])

    with col1:

        fig = px.bar(
            subject_df,
            x="Subject",
            y="Exam_Score",
            color="Exam_Score",
            text_auto=".2f",
            color_continuous_scale="Greens",
            title="Average Exam Score by Subject"
        )

        fig.update_layout(
            template="plotly_white",
            height=450
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:

        st.dataframe(subject_df, use_container_width=True)

# =====================================================
# DEPARTMENT PERFORMANCE
# =====================================================

with tab3:

    st.subheader("🏢 Department Performance")

    department_df = (
        filtered_df.groupby("Department")["Exam_Score"]
        .mean()
        .reset_index()
        .sort_values("Exam_Score", ascending=False)
    )

    col1, col2 = st.columns([2,1])

    with col1:

        fig = px.bar(
            department_df,
            x="Department",
            y="Exam_Score",
            color="Exam_Score",
            text_auto=".2f",
            color_continuous_scale="Oranges",
            title="Department Performance"
        )

        fig.update_layout(
            template="plotly_white",
            height=450
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:

        st.dataframe(department_df, use_container_width=True)

# =====================================================
# TEACHER PERFORMANCE
# =====================================================

with tab4:

    st.subheader("👨‍🏫 Teacher Performance")

    teacher_df = (
        filtered_df.groupby("Teacher")["Exam_Score"]
        .mean()
        .reset_index()
        .sort_values("Exam_Score", ascending=False)
    )

    col1, col2 = st.columns([2,1])

    with col1:

        fig = px.bar(
            teacher_df,
            x="Teacher",
            y="Exam_Score",
            color="Exam_Score",
            text_auto=".2f",
            color_continuous_scale="Purples",
            title="Teacher Performance"
        )

        fig.update_layout(
            template="plotly_white",
            height=500
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:

        st.dataframe(teacher_df, use_container_width=True)

st.divider()
# =====================================================
# STUDENT ANALYTICS
# =====================================================

st.header("👨‍🎓 Student Analytics")

tab5, tab6, tab7 = st.tabs([
    "📈 Performance",
    "🏆 Top Students",
    "📉 Low Students"
])
# =====================================================
# ATTENDANCE & ENGAGEMENT
# =====================================================

with tab5:

    st.subheader("📊 Student Performance Relationships")

    # -------------------------------------------------
    # ATTENDANCE VS EXAM SCORE
    # -------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        fig = px.scatter(
            filtered_df,
            x="Attendance",
            y="Exam_Score",
            color="Course",
            hover_data=[
                "Student_ID",
                "Department",
                "Teacher"
            ],
            title="📅 Attendance vs Exam Score",
            opacity=0.55
        )

        fig.update_traces(
            marker=dict(
                size=7,
                line=dict(
                    width=0.5
                )
            )
        )

        fig.update_layout(
            height=500,

            title=dict(
                font=dict(
                    size=18,
                    color="#312E81"
                ),
                x=0.02
            ),

            xaxis=dict(
                title="Attendance",
                gridcolor="#E5E7EB",
                zeroline=False
            ),

            yaxis=dict(
                title="Exam Score",
                gridcolor="#E5E7EB",
                zeroline=False
            ),

            legend=dict(
                title="Course",
                orientation="v"
            ),

            plot_bgcolor="white",
            paper_bgcolor="white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # -------------------------------------------------
    # ENGAGEMENT VS EXAM SCORE
    # -------------------------------------------------

    with col2:

        fig = px.scatter(
            filtered_df,
            x="Engagement_Score",
            y="Exam_Score",
            color="Department",
            hover_data=[
                "Student_ID",
                "Course",
                "Teacher"
            ],
            title="🎯 Engagement vs Exam Score",
            opacity=0.55
        )

        fig.update_traces(
            marker=dict(
                size=7,
                line=dict(
                    width=0.5
                )
            )
        )

        fig.update_layout(
            height=500,

            title=dict(
                font=dict(
                    size=18,
                    color="#312E81"
                ),
                x=0.02
            ),

            xaxis=dict(
                title="Engagement Score",
                gridcolor="#E5E7EB",
                zeroline=False
            ),

            yaxis=dict(
                title="Exam Score",
                gridcolor="#E5E7EB",
                zeroline=False
            ),

            legend=dict(
                title="Department",
                orientation="v"
            ),

            plot_bgcolor="white",
            paper_bgcolor="white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # =================================================
    # DISTRIBUTION SECTION
    # =================================================

    st.divider()

    st.subheader("📈 Score & Attendance Distribution")

    col3, col4 = st.columns(2)


    # -------------------------------------------------
    # ATTENDANCE DISTRIBUTION
    # -------------------------------------------------

    with col3:

        fig = px.histogram(
            filtered_df,
            x="Attendance",
            nbins=20,
            title="📅 Attendance Distribution",
            color_discrete_sequence=["#6C5CE7"]
        )

        fig.update_layout(
            height=400,

            xaxis_title="Attendance",
            yaxis_title="Number of Students",

            plot_bgcolor="white",
            paper_bgcolor="white",

            bargap=0.08
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # -------------------------------------------------
    # EXAM SCORE DISTRIBUTION
    # -------------------------------------------------

    with col4:

        fig = px.histogram(
            filtered_df,
            x="Exam_Score",
            nbins=20,
            title="📝 Exam Score Distribution",
            color_discrete_sequence=["#00B894"]
        )

        fig.update_layout(
            height=400,

            xaxis_title="Exam Score",
            yaxis_title="Number of Students",

            plot_bgcolor="white",
            paper_bgcolor="white",

            bargap=0.08
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )
# =====================================================
# TOP STUDENTS
# =====================================================
# =====================================================
# TOP STUDENTS
# =====================================================

with tab6:

    st.subheader("🏆 Top 10 Students")

    top = (
        filtered_df
        .sort_values("Exam_Score", ascending=False)
        .head(10)
    )

    # Top student
    top_student = top.iloc[0]

    st.success(
        f"🥇 Top Student: {top_student['Student_ID']}  |  "
        f"Exam Score: {top_student['Exam_Score']:.2f}"
    )

    # Display table
    top_table = top[
        [
            "Student_ID",
            "Course",
            "Department",
            "Teacher",
            "Attendance",
            "Exam_Score"
        ]
    ].copy()

    top_table = top_table.rename(
        columns={
            "Student_ID": "Student ID",
            "Course": "Course",
            "Department": "Department",
            "Teacher": "Teacher",
            "Attendance": "Attendance",
            "Exam_Score": "Exam Score"
        }
    )

    st.dataframe(
        top_table,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Student ID": st.column_config.TextColumn(
                "Student ID"
            ),
            "Attendance": st.column_config.NumberColumn(
                "Attendance",
                format="%.2f"
            ),
            "Exam Score": st.column_config.NumberColumn(
                "Exam Score",
                format="%.2f"
            )
        }
    )


# =====================================================
# LOW STUDENTS
# =====================================================

with tab7:

    st.subheader("📉 Low Performing Students")

    low = (
        filtered_df
        .sort_values("Exam_Score", ascending=True)
        .head(10)
    )

    # Lowest student
    low_student = low.iloc[0]

    st.warning(
        f"⚠️ Lowest Score: {low_student['Student_ID']}  |  "
        f"Exam Score: {low_student['Exam_Score']:.2f}"
    )

    # Display table
    low_table = low[
        [
            "Student_ID",
            "Course",
            "Department",
            "Teacher",
            "Attendance",
            "Exam_Score"
        ]
    ].copy()

    low_table = low_table.rename(
        columns={
            "Student_ID": "Student ID",
            "Course": "Course",
            "Department": "Department",
            "Teacher": "Teacher",
            "Attendance": "Attendance",
            "Exam_Score": "Exam Score"
        }
    )

    st.dataframe(
        low_table,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Student ID": st.column_config.TextColumn(
                "Student ID"
            ),
            "Attendance": st.column_config.NumberColumn(
                "Attendance",
                format="%.2f"
            ),
            "Exam Score": st.column_config.NumberColumn(
                "Exam Score",
                format="%.2f"
            )
        }
    )
# =====================================================
# FRAUD DETECTION
# =====================================================

st.header("🚨 Fraud Detection Dashboard")

fraud_df = filtered_df.copy()

fraud_df["Fraud_Flag"] = "Normal"

fraud_df.loc[
    (fraud_df["Attendance"] < 0) |
    (fraud_df["Attendance"] > 100) |
    (fraud_df["Exam_Score"] < 0) |
    (fraud_df["Exam_Score"] > 100) |
    (fraud_df["Quiz_Score"] < 0) |
    (fraud_df["Quiz_Score"] > 100) |
    (fraud_df["Assignment_Score"] < 0) |
    (fraud_df["Assignment_Score"] > 100),
    "Fraud_Flag"
] = "Anomaly"


# =====================================================
# FRAUD COUNTS
# =====================================================

anomaly_count = len(
    fraud_df[fraud_df["Fraud_Flag"] == "Anomaly"]
)

normal_count = len(
    fraud_df[fraud_df["Fraud_Flag"] == "Normal"]
)

total_records = len(fraud_df)

if total_records > 0:
    anomaly_percentage = (anomaly_count / total_records) * 100
    normal_percentage = (normal_count / total_records) * 100
else:
    anomaly_percentage = 0
    normal_percentage = 0


# =====================================================
# KPI SUMMARY
# =====================================================

c1, c2, c3 = st.columns(3)

with c1:

    st.metric(
        "📊 Total Records",
        f"{total_records:,}"
    )

with c2:

    st.metric(
        "🚨 Anomaly Records",
        f"{anomaly_count:,}"
    )

with c3:

    st.metric(
        "✅ Normal Records",
        f"{normal_count:,}"
    )


st.divider()


# =====================================================
# FRAUD CHART + SUMMARY
# =====================================================

col1, col2 = st.columns([1.5, 1])


# =====================================================
# DONUT CHART
# =====================================================

with col1:

    summary = (
        fraud_df["Fraud_Flag"]
        .value_counts()
        .reset_index()
    )

    summary.columns = ["Status", "Count"]

    fig = px.pie(
        summary,
        names="Status",
        values="Count",
        hole=0.60,
        title="Fraud Detection Status",
        color="Status",
        color_discrete_map={
            "Normal": "#00B894",
            "Anomaly": "#E84393"
        }
    )

    fig.update_traces(
        textinfo="percent",
        textfont_size=15,
        hovertemplate=(
            "<b>%{label}</b><br>"
            "Records: %{value:,}<br>"
            "Percentage: %{percent}"
            "<extra></extra>"
        )
    )

    fig.update_layout(
        height=430,

        title=dict(
            font=dict(
                size=20,
                color="#312E81"
            ),
            x=0.02
        ),

        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.15,
            xanchor="center",
            x=0.5
        ),

        paper_bgcolor="white",
        plot_bgcolor="white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =====================================================
# FRAUD SUMMARY
# =====================================================

with col2:

    st.subheader("📋 Detection Summary")

    st.write(
        "Overview of records identified by the fraud validation rules."
    )

    st.write("")

    st.metric(
        "🚨 Anomaly Rate",
        f"{anomaly_percentage:.2f}%"
    )

    st.progress(
        min(anomaly_percentage / 100, 1.0)
    )

    st.write("")

    st.metric(
        "✅ Normal Rate",
        f"{normal_percentage:.2f}%"
    )

    st.progress(
        min(normal_percentage / 100, 1.0)
    )

    st.write("")

    if anomaly_count == 0:

        st.success(
            "✅ No anomalous records detected in the selected data."
        )

    else:

        st.warning(
            f"⚠️ {anomaly_count:,} anomalous records require attention."
        )


# =====================================================
# ANOMALY RECORDS
# =====================================================

if anomaly_count > 0:

    st.divider()

    st.subheader("🚨 Anomalous Records")

    anomaly_df = fraud_df[
        fraud_df["Fraud_Flag"] == "Anomaly"
    ]

    st.dataframe(
        anomaly_df,
        use_container_width=True,
        hide_index=True
    )
# =====================================================
# DOWNLOAD REPORTS
# =====================================================

st.header("📥 Download Reports")

st.write(
    "Download the currently filtered data and fraud detection results."
)

c1, c2 = st.columns(2)

with c1:

    st.download_button(
        "⬇️ Download Filtered Dataset",
        filtered_df.to_csv(index=False),
        "filtered_dataset.csv",
        "text/csv",
        use_container_width=True
    )

with c2:

    st.download_button(
        "🚨 Download Fraud Report",
        fraud_df.to_csv(index=False),
        "fraud_report.csv",
        "text/csv",
        use_container_width=True
    )


st.divider()


# =====================================================
# DASHBOARD INSIGHTS
# =====================================================

st.header("💡 Dashboard Insights")

# Best performers
best_course = (
    filtered_df.groupby("Course")["Exam_Score"]
    .mean()
    .idxmax()
)

best_department = (
    filtered_df.groupby("Department")["Exam_Score"]
    .mean()
    .idxmax()
)

best_teacher = (
    filtered_df.groupby("Teacher")["Exam_Score"]
    .mean()
    .idxmax()
)


# -----------------------------------------------------
# BEST PERFORMANCE
# -----------------------------------------------------

c1, c2, c3 = st.columns(3)

with c1:

    st.success(
        f"🏆 Best Course\n\n"
        f"**{best_course}**"
    )

with c2:

    st.success(
        f"🏢 Best Department\n\n"
        f"**{best_department}**"
    )

with c3:

    st.success(
        f"👨‍🏫 Best Teacher\n\n"
        f"**{best_teacher}**"
    )


# -----------------------------------------------------
# KEY OBSERVATIONS
# -----------------------------------------------------

st.subheader("📌 Key Observations")

st.info(
    "📅 **Attendance:** "
    "Students with higher attendance generally show better exam performance."
)

st.info(
    "🎯 **Engagement:** "
    "Higher engagement is associated with stronger student performance."
)

st.warning(
    "📉 **At-Risk Students:** "
    "Low-performing students may require personalized learning support."
)


# =====================================================
# RECOMMENDATIONS
# =====================================================

st.divider()

st.header("📢 Recommendations")

c1, c2 = st.columns(2)

with c1:

    st.success(
        "📅 **Improve Attendance Monitoring**\n\n"
        "Track students with consistently low attendance "
        "and provide timely intervention."
    )

    st.success(
        "🎯 **Increase Student Engagement**\n\n"
        "Introduce interactive learning activities and "
        "participation-based methods."
    )

    st.success(
        "👨‍🏫 **Encourage Best Teaching Practices**\n\n"
        "Study high-performing teaching approaches and "
        "share effective practices."
    )


with c2:

    st.warning(
        "📉 **Support Low Performers**\n\n"
        "Provide remedial classes and personalized learning "
        "support for students with weak performance."
    )

    st.warning(
        "🚨 **Monitor Anomalies**\n\n"
        "Regularly review unusual attendance and score values "
        "identified by the fraud detection module."
    )

    st.info(
        "📊 **Use KPI Dashboard**\n\n"
        "Use performance indicators to support curriculum "
        "and academic decision-making."
    )

# =# =====================================================
# DAY 8 - PERFORMANCE FORECAST
# =====================================================

st.divider()

st.header("🔮 Performance Forecast")

st.write(
    "This section estimates how student exam performance "
    "may change based on the current performance trend."
)

# -----------------------------------------------------
# PREPARE DATA
# -----------------------------------------------------

forecast_df = filtered_df.copy()

forecast_df = forecast_df.reset_index(drop=True)

forecast_df["Observation"] = np.arange(
    len(forecast_df)
)

forecast = (
    forecast_df
    .groupby("Observation")["Exam_Score"]
    .mean()
)

x = forecast.index.to_numpy()
y = forecast.values


# -----------------------------------------------------
# FORECAST MODEL
# -----------------------------------------------------

coef = np.polyfit(x, y, 1)

poly = np.poly1d(coef)

future_x = np.arange(
    len(x),
    len(x) + 90
)

future_y = poly(future_x)

# Keep predictions within valid exam score range
future_y = np.clip(
    future_y,
    0,
    100
)


# -----------------------------------------------------
# IMPORTANT VALUES
# -----------------------------------------------------

current_score = float(
    np.mean(y[-min(100, len(y)):])
)

predicted_score = float(
    np.mean(future_y)
)

change = predicted_score - current_score


if change > 0.5:

    status = "📈 Expected to Improve"

elif change < -0.5:

    status = "📉 Expected to Decline"

else:

    status = "➡️ Expected to Remain Stable"


# -----------------------------------------------------
# KPI CARDS
# -----------------------------------------------------

c1, c2, c3 = st.columns(3)

with c1:

    st.metric(
        "📊 Current Performance",
        f"{current_score:.2f}/100"
    )

with c2:

    st.metric(
        "🔮 Expected Performance",
        f"{predicted_score:.2f}/100",
        delta=f"{change:+.2f}"
    )

with c3:

    st.metric(
        "📌 Forecast Status",
        status
    )


st.write("")


# -----------------------------------------------------
# SIMPLE FORECAST CHART
# -----------------------------------------------------

chart_df = pd.DataFrame({
    "Observation": future_x,
    "Predicted Exam Score": future_y
})


fig = go.Figure()


# Recent performance
fig.add_trace(
    go.Scatter(
        x=x[-300:],
        y=y[-300:],
        mode="lines",
        name="Recent Performance",
        line=dict(
            width=2
        )
    )
)


# Forecast
fig.add_trace(
    go.Scatter(
        x=future_x,
        y=future_y,
        mode="lines",
        name="Expected Performance",
        line=dict(
            width=4,
            dash="dash"
        )
    )
)


fig.update_layout(

    height=430,

    title=dict(
        text="Current Trend → Expected Performance",
        font=dict(
            size=20,
            color="#312E81"
        ),
        x=0.02
    ),

    xaxis=dict(
        title="Student Performance Observations",
        gridcolor="#E5E7EB"
    ),

    yaxis=dict(
        title="Exam Score",
        range=[0, 100],
        gridcolor="#E5E7EB"
    ),

    legend=dict(
        orientation="h",
        y=1.02,
        x=0
    ),

    hovermode="x unified",

    plot_bgcolor="white",
    paper_bgcolor="white"
)


st.plotly_chart(
    fig,
    use_container_width=True
)


# -----------------------------------------------------
# EASY-TO-UNDERSTAND INTERPRETATION
# -----------------------------------------------------

if change > 0.5:

    st.success(
        f"📈 **What this means:** "
        f"Current performance is around **{current_score:.2f}**. "
        f"The forecast expects performance to increase to around "
        f"**{predicted_score:.2f}**."
    )

elif change < -0.5:

    st.warning(
        f"📉 **What this means:** "
        f"Current performance is around **{current_score:.2f}**. "
        f"The forecast indicates a possible decrease to around "
        f"**{predicted_score:.2f}**."
    )

else:

    st.info(
        f"➡️ **What this means:** "
        f"Current performance is around **{current_score:.2f}** "
        f"and the forecast expects it to remain relatively stable "
        f"around **{predicted_score:.2f}**."
    )


# -----------------------------------------------------
# FORECAST SUMMARY
# -----------------------------------------------------

st.subheader("📋 Forecast Summary")

summary_df = pd.DataFrame({
    "Metric": [
        "Current Performance",
        "Expected Performance",
        "Expected Change",
        "Forecast Status"
    ],

    "Value": [
        f"{current_score:.2f}/100",
        f"{predicted_score:.2f}/100",
        f"{change:+.2f}",
        status
    ]
})

st.dataframe(
    summary_df,
    use_container_width=True,
    hide_index=True
)
