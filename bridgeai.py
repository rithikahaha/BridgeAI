import os
import streamlit as st
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

CURRICULUMS = {
    "CSE - KTU (Kerala)": """
Programming: C, C++, Java, Python
Data Structures and Algorithms
Database Management Systems
Operating Systems
Computer Networks
Software Engineering
Discrete Mathematics
Linear Algebra
Probability
HTML, CSS, JavaScript
""",
    "CSE - Anna University": """
Programming: C, Java, Python
Data Structures
Algorithms
Database Systems
Operating Systems
Computer Networks
Software Engineering
Statistics
Machine Learning basics
""",
    "CSE - VTU (Karnataka)": """
Programming: C, C++, Java, Python
Data Structures
Algorithms
DBMS
Operating Systems
Computer Networks
Software Engineering
Statistics
Machine Learning basics
"""
}

ROLES = {
    "Data Analyst": """
Advanced SQL
Python (Pandas, NumPy)
Power BI / Tableau
Statistics
Exploratory Data Analysis
Business Intelligence
KPI dashboards
""",
    "Software Engineer": """
Python or Java
Data Structures and Algorithms
System Design basics
SQL / NoSQL
REST APIs
Git / GitHub
Docker
CI/CD
""",
    "ML Engineer": """
Python
Machine Learning algorithms
Deep Learning frameworks
Feature engineering
Model evaluation
Model deployment APIs
"""
}

model = genai.GenerativeModel("gemini-2.0-flash")

st.set_page_config(page_title="BridgeAI", page_icon="🎓")
st.title(" BridgeAI — Academic to Industry Skill Gap Analyzer")
st.write("Select your university curriculum and target role to generate an AI-powered skill gap analysis report.")

curriculum_choice = st.selectbox("University Curriculum", list(CURRICULUMS.keys()))
role_choice = st.selectbox("Target Role", list(ROLES.keys()))

if st.button("Generate Report"):
    curriculum = CURRICULUMS[curriculum_choice]
    role = ROLES[role_choice]

    prompt = f"""
You are an AI career advisor.
Compare the following university curriculum with industry job requirements.

ACADEMIC CURRICULUM:
{curriculum}

JOB REQUIREMENTS:
{role}

Generate a professional skill gap report including:
1. Academic strengths
2. Skills matching industry requirements
3. Missing critical skills
4. Readiness score out of 100
5. 90-day improvement roadmap
6. Suggested portfolio projects
"""
    try:
        response = model.generate_content(prompt, stream=True)
        output = st.empty()
        full_text = ""
        for chunk in response:
            full_text += chunk.text
            output.markdown(full_text)
    except Exception as e:
        st.error(f"Error generating report: {str(e)}")
