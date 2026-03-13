import os
import gradio as gr
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

def analyze(curriculum_choice, role_choice, custom_input):
    curriculum = custom_input.strip() if custom_input.strip() else CURRICULUMS[curriculum_choice]
    role = ROLES[role_choice]

    prompt = f"""
You are an AI career advisor. Generate a detailed professional skill gap report.
Format your response with clear sections using these exact headings:

BRIDGEAI SKILL GAP REPORT — Role: {role_choice}

SECTION 1 - ACADEMIC FOUNDATIONS
SECTION 2 - STRENGTHS: DIRECT INDUSTRY MATCH
SECTION 3 - SKILL GAPS
SECTION 4 - READINESS SCORE
SECTION 5 - 90-DAY IMPROVEMENT ROADMAP
SECTION 6 - SUGGESTED PORTFOLIO PROJECTS

ACADEMIC CURRICULUM:
{curriculum}

JOB REQUIREMENTS:
{role}

Be specific, practical, and actionable. For each skill gap, explain why it matters and how to learn it.
"""
    try:
        response = model.generate_content(prompt, stream=True)
        full_text = ""
        for chunk in response:
            full_text += chunk.text
            yield full_text
    except Exception as e:
        yield f"Error generating report: {str(e)}"

with gr.Blocks(theme=gr.themes.Default(primary_hue="orange"), css="""
    #title { text-align: center; }
    #subtitle { text-align: center; color: gray; }
    #generate-btn { background-color: #e8500a; color: white; }
""") as demo:

    gr.Markdown("# BridgeAI — Academic to Industry Skill Gap Analyzer", elem_id="title")
    gr.Markdown("Select your university curriculum and target role to receive a professional skill gap analysis and 90-day development plan.", elem_id="subtitle")

    with gr.Row():
        with gr.Column():
            curriculum_choice = gr.Dropdown(list(CURRICULUMS.keys()), label="University Curriculum", value="CSE - KTU (Kerala)")
            role_choice = gr.Dropdown(list(ROLES.keys()), label="Target Role", value="Data Analyst")
            custom_input = gr.Textbox(
                label="Don't see your university? Paste your subjects here (optional)",
                placeholder="e.g. Java, Data Structures, DBMS, Computer Networks...",
                lines=5
            )
            with gr.Row():
                clear_btn = gr.ClearButton(value="Clear")
                generate_btn = gr.Button("Generate Report", variant="primary", elem_id="generate-btn")

        with gr.Column():
            output = gr.Markdown(label="BridgeAI Skill Gap Report")

    generate_btn.click(
        fn=analyze,
        inputs=[curriculum_choice, role_choice, custom_input],
        outputs=output
    )

demo.launch()
