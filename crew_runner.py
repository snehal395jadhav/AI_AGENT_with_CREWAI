import streamlit as st
from crewai import Agent, Task, Crew, LLM
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
import os

# ================== 🔑 ADD YOUR OPENROUTER API KEY HERE ==================
OPENROUTER_API_KEY = ""
# ==========================================================================

# ================= PAGE CONFIG =================
st.set_page_config(page_title="AI Blog Generator", page_icon="🚀", layout="wide")

# ================= CUSTOM CSS =================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #141e30, #243b55);
    color: white;
}
.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
}
.chat-box {
    background-color: rgba(255,255,255,0.1);
    padding: 15px;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🚀 AI Multi-Agent Blog Generator</div>', unsafe_allow_html=True)
st.write("")

# ================= LLM CONFIG =================
llm = LLM(
    model="openrouter/meta-llama/llama-3-8b-instruct",
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

# ================= SESSION STATE =================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "final_output" not in st.session_state:
    st.session_state.final_output = ""

# ================= CHAT INPUT =================
user_input = st.chat_input("Enter blog topic...")

if user_input:
    st.session_state.chat_history.append(("user", user_input))

    with st.spinner("AI Agents Working... 🤖"):

        # ================= AGENTS =================
        planner = Agent(
            role="Content Planner",
            goal="Create structured blog outline on {topic}",
            backstory="Expert SEO planner.",
            llm=llm,
        )

        writer = Agent(
            role="Content Writer",
            goal="Write detailed blog article from outline",
            backstory="Professional blog writer.",
            llm=llm,
        )

        editor = Agent(
            role="Editor",
            goal="Improve grammar, clarity and engagement",
            backstory="Senior content editor.",
            llm=llm,
        )

        # ================= TASKS =================
        task1 = Task(
            description="Create SEO optimized outline about {topic}",
            expected_output="Structured outline",
            agent=planner,
        )

        task2 = Task(
            description="Write full blog article using outline",
            expected_output="Detailed blog article",
            agent=writer,
        )

        task3 = Task(
            description="Edit and polish the article professionally",
            expected_output="Final polished blog article",
            agent=editor,
        )

        crew = Crew(
            agents=[planner, writer, editor],
            tasks=[task1, task2, task3],
        )

        result = crew.kickoff(inputs={"topic": user_input})

        # 🔥 FIX: Convert CrewOutput to string
        final_text = str(result)

        st.session_state.final_output = final_text
        st.session_state.chat_history.append(("assistant", final_text))

# ================= DISPLAY CHAT =================
for role, message in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(message)

# ================= PDF GENERATION =================
def generate_pdf(text):
    pdf_path = "AI_Blog_Output.pdf"
    doc = SimpleDocTemplate(pdf_path, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    for line in text.split("\n"):
        elements.append(Paragraph(line, styles["Normal"]))
        elements.append(Spacer(1, 6))

    doc.build(elements)
    return pdf_path

if st.session_state.final_output:
    pdf_file = generate_pdf(st.session_state.final_output)

    with open(pdf_file, "rb") as f:
        st.download_button(
            "📥 Download as PDF",
            f,
            file_name="AI_Blog_Output.pdf",
            mime="application/pdf"
        )

st.markdown("---")
st.markdown("👨‍🎓 Advanced AI Student Tool | CrewAI + OpenRouter")
