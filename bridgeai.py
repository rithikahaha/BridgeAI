import os
import gradio as gr
from groq import Groq

client = Groq(api_key="YOUR_API_KEY")

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
    """
}

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

def analyze_gap(curriculum_choice, target_role, custom_syllabus, custom_jd):
    print("Function called")
    curriculum = custom_syllabus.strip() if custom_syllabus.strip() else CURRICULUMS.get(curriculum_choice, "")
    industry = custom_jd.strip() if custom_jd.strip() else INDUSTRY_JDS.get(target_role, "")

    prompt = f"""
You are BridgeAI, a senior talent analytics advisor. Analyze the gap between this candidate's academic background and real industry requirements.

ACADEMIC CURRICULUM:
{curriculum}

INDUSTRY REQUIREMENTS:
{industry}

Produce a clean, professional skill gap report. No emojis. Formal language suitable for a senior HR manager at a large technology company.

---

BRIDGEAI SKILL GAP REPORT
Role: {target_role}

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
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        print("Report generated successfully")
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error: {str(e)}")
        return f"Error generating report: {str(e)}"

def show_loading(curriculum_choice, target_role, custom_syllabus, custom_jd):
    return "⚡ Generating your report, please wait..."

with gr.Blocks(css="#title { text-align: center; } #subtitle { text-align: center; color: gray; }") as demo:

    gr.Markdown("# BridgeAI — Academic to Industry Skill Gap Analyzer", elem_id="title")
    gr.Markdown("Select your university curriculum and target role to receive a professional skill gap analysis and 90-day development plan.", elem_id="subtitle")

    with gr.Row():
        with gr.Column():
            curriculum_choice = gr.Dropdown(list(CURRICULUMS.keys()), label="University Curriculum", value="CSE - KTU (Kerala)")
            role_choice = gr.Dropdown(list(INDUSTRY_JDS.keys()), label="Target Role", value="Data Analyst")
            custom_syllabus = gr.Textbox(
                label="Don't see your university? Paste your subjects here (optional)",
                placeholder="e.g. Java, Data Structures, DBMS, Computer Networks...",
                lines=3
            )
            custom_jd = gr.Textbox(
                label="Have a specific job description? Paste it here (optional)",
                placeholder="e.g. We are looking for a Data Analyst with 2+ years experience in SQL, Python, Tableau...",
                lines=5
            )
            with gr.Row():
                clear_btn = gr.ClearButton(value="Clear")
                generate_btn = gr.Button("Generate Report", variant="primary")

        with gr.Column():
            output = gr.Markdown(label="BridgeAI Skill Gap Report")

    generate_btn.click(
        fn=show_loading,
        inputs=[curriculum_choice, role_choice, custom_syllabus, custom_jd],
        outputs=output,
        queue=False
    ).then(
        fn=analyze_gap,
        inputs=[curriculum_choice, role_choice, custom_syllabus, custom_jd],
        outputs=output,
        queue=True
    )

demo.queue()
demo.launch(share=True, debug=True)
