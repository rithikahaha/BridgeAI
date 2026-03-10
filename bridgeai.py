# ============================================================
# BridgeAI — Academic to Industry Skill Gap Analyzer
# Built with Google Gemini 2.5 + LangChain + Gradio
# Author: Rithika Harikrishna
# ============================================================

import os
import gradio as gr
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# --- API KEY ---
# Add your Gemini API key here (get it free from aistudio.google.com)
os.environ["GEMINI_API_KEY"] = "ADD_YOUR_KEY_HERE"

# --- CURRICULUM DATABASE ---
CURRICULUMS = {
    "CSE - KTU (Kerala)": """
        Programming: C, C++, Java, Python
        Data Structures and Algorithms
        Database Management Systems (SQL)
        Operating Systems, Computer Networks
        Software Engineering, SDLC
        Mathematics: Discrete Math, Linear Algebra, Probability
        Web Technologies: HTML, CSS, Basic JavaScript
        Computer Organization and Architecture
        Theory of Computation, Compiler Design
        Minor electives: AI basics, Data Mining basics
    """,
    "CSE - Anna University": """
        Programming: C, Java, Python
        Data Structures, Algorithms
        Database Systems, SQL
        Operating Systems, Networks
        Software Engineering
        Mathematics: Statistics, Calculus, Discrete Math
        Web Programming
        Cloud Computing basics, IoT basics
        Professional electives: Data Analytics, Machine Learning basics
    """,
    "CSE - VTU (Karnataka)": """
        Programming: C, C++, Java, Python
        Data Structures and Algorithms
        DBMS, SQL
        Operating Systems, Computer Networks
        Software Engineering, Agile basics
        Mathematics: Engineering Math, Statistics
        Web Technologies
        Machine Learning basics, Big Data basics
    """,
    "CSE - Mumbai University": """
        Programming: C, Java, Python
        Data Structures, Algorithms
        Database Management, SQL
        Operating Systems, Networks
        Software Engineering
        Mathematics: Applied Math, Statistics
        Web Development basics
        Electives: Data Science, Cloud basics
    """,
    "IT - General": """
        Programming: C, Java, Python
        Data Structures
        Database Systems, SQL
        Networking, OS basics
        Web Technologies: HTML, CSS, JavaScript
        Software Engineering
        Mathematics: Statistics, Discrete Math
    """
}

# --- INDUSTRY JD DATABASE ---
INDUSTRY_JDS = {
    "Data Analyst": """
        SQL (advanced): CTEs, Window Functions, Stored Procedures, Query Optimization
        Python: Pandas, NumPy, Matplotlib, Seaborn
        Data Visualization: Power BI, Tableau, Excel (Pivot Tables, XLOOKUP)
        Statistics: Hypothesis Testing, Regression, A/B Testing
        EDA, Cohort Analysis, RFM Segmentation, CLV, Churn Analysis
        Data Cleaning, Data Wrangling, Data Governance
        Business Intelligence, KPI Dashboards, Metrics Reporting
        Communication: presenting insights to non-technical stakeholders
        Tools: Jupyter Notebook, Git, JIRA
        Nice to have: Cloud basics, Spark basics, dbt
    """,
    "Software Engineer": """
        Programming: Java or Python (strong OOP, design patterns)
        Data Structures and Algorithms
        System Design basics
        Databases: SQL, NoSQL (MongoDB, Redis)
        Frameworks: Spring Boot, Django, FastAPI, Node.js
        Version Control: Git, GitHub
        DevOps basics: Docker, CI/CD, GitHub Actions
        REST APIs, Microservices concepts
        Testing: Unit Testing, TDD
        Cloud basics: AWS or GCP or Azure
        Nice to have: Kubernetes, Kafka, GraphQL
    """,
    "ML Engineer": """
        Python: Pandas, NumPy, Scikit-learn
        Machine Learning: Supervised, Unsupervised, Reinforcement basics
        Deep Learning: TensorFlow, PyTorch, Keras
        NLP, Computer Vision basics
        Model deployment: FastAPI, Flask, Docker
        MLOps: MLflow, model monitoring
        Data preprocessing, Feature Engineering
        Statistics: Probability, Distributions, Hypothesis Testing
        SQL for data extraction
        Cloud ML: AWS SageMaker or GCP Vertex AI
        Nice to have: LangChain, RAG, Vector Databases
    """,
    "SAP Consultant": """
        SAP modules: ERP fundamentals, SAP S/4HANA basics
        Business Process knowledge: Finance, Supply Chain, HR
        Data Analysis and Reporting
        SQL basics
        Excel: Advanced formulas, Pivot Tables
        Stakeholder communication and consulting skills
        Problem solving and process improvement
        Documentation and requirement gathering
        Project management basics: Agile, SDLC
        Nice to have: SAP ABAP basics, Power BI, Tableau
    """,
    "Business Analyst": """
        Requirements gathering and documentation
        SQL for data querying
        Excel: Advanced, Pivot Tables, VLOOKUP, XLOOKUP
        Data Visualization: Power BI or Tableau
        Process mapping and improvement
        Stakeholder management and communication
        Agile methodology, JIRA
        Business Intelligence and KPI tracking
        Problem solving and analytical thinking
        Nice to have: Python basics, SQL advanced
    """
}

# --- ANALYSIS FUNCTION ---
def analyze_gap(curriculum_choice, target_role, uploaded_syllabus=None):
    if uploaded_syllabus and uploaded_syllabus.strip():
        curriculum_text = uploaded_syllabus
    else:
        curriculum_text = CURRICULUMS.get(curriculum_choice, "")

    industry_text = INDUSTRY_JDS.get(target_role, "")

    prompt = PromptTemplate(
        input_variables=["curriculum", "industry"],
        template="""
You are BridgeAI, a senior talent analytics advisor. Analyze the gap between this candidate's academic background and real industry requirements.

ACADEMIC CURRICULUM:
{curriculum}

INDUSTRY REQUIREMENTS:
{industry}

Produce a clean, professional skill gap report. No emojis. Formal language suitable for a senior HR manager at a large technology company.

---

BRIDGEAI SKILL GAP REPORT
Role: """ + "%(role)s" + """

SECTION 1 - ACADEMIC FOUNDATIONS
Summarise the core skills from the academic program relevant to this role.

SECTION 2 - STRENGTHS: DIRECT INDUSTRY MATCH
List specific skills from the curriculum that directly align with industry requirements.

SECTION 3 - SKILL GAPS

CRITICAL (required for most entry-level roles):
- [skill]: [why it matters and how to learn it]

IMPORTANT (will significantly strengthen the profile):
- [skill]: [why it matters and how to learn it]

RECOMMENDED (differentiating skills):
- [skill]: [why it matters and how to learn it]

SECTION 4 - READINESS ASSESSMENT
Overall readiness score: [X/100]
Assessment: [2-3 sentences, honest and constructive]

SECTION 5 - 90-DAY DEVELOPMENT PLAN
Week 1-4: [skills and resources to focus on]
Week 5-8: [projects to build]
Week 9-12: [how to showcase work and what to apply for]

SECTION 6 - RECOMMENDED PROJECTS
1. [Project name]: [what it demonstrates to employers]
2. [Project name]: [what it demonstrates to employers]
3. [Project name]: [what it demonstrates to employers]

---
        """
    )

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=os.environ["GEMINI_API_KEY"]
    )

    chain = LLMChain(llm=llm, prompt=prompt)
    result = chain.invoke({"curriculum": curriculum_text, "industry": industry_text})
    return result["text"]

# --- GRADIO UI ---
def bridge_ai(curriculum_choice, target_role, custom_syllabus):
    if custom_syllabus.strip():
        return analyze_gap(curriculum_choice, target_role, custom_syllabus)
    return analyze_gap(curriculum_choice, target_role)

demo = gr.Interface(
    fn=bridge_ai,
    inputs=[
        gr.Dropdown(choices=list(CURRICULUMS.keys()), label="University Curriculum", value="CSE - KTU (Kerala)"),
        gr.Dropdown(choices=list(INDUSTRY_JDS.keys()), label="Target Role", value="Data Analyst"),
        gr.Textbox(label="Don't see your university? Paste your subjects here (optional)", placeholder="e.g. Java, Data Structures, DBMS, Computer Networks...", lines=3)
    ],
    outputs=gr.Markdown(label="Skill Gap Report"),
    title="BridgeAI — Academic to Industry Skill Gap Analyzer",
    description="Select your university curriculum and target role to receive a professional skill gap analysis and 90-day development plan. Report generates in 30-60 seconds.",
    allow_flagging="never",
    submit_btn="Generate Report"
)

if __name__ == "__main__":
    demo.launch()
