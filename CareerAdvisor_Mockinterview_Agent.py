import os
import streamlit as st
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_groq import ChatGroq
from langchain.document_loaders import PyPDFLoader

os.environ["GROQ_API_KEY"] = "your_key"

os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]

llm = ChatGroq(model="llama3-8b-8192", temperature=0.6)
memory = ConversationBufferMemory()
career_chain = ConversationChain(llm=llm, memory=memory)

st.set_page_config(page_title="Career Advisor Agent", layout="wide")
st.title("🧠 AI-Powered Career Advisor Agent")
st.markdown("Upload your resume, ask career questions, or run a mock interview simulation!")

uploaded_file = st.file_uploader("📄 Upload Resume (PDF)", type="pdf")
resume_text = ""

if uploaded_file:
    file_path = uploaded_file.name
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("✅ Resume uploaded successfully!")

    loader = PyPDFLoader(file_path)
    pages = loader.load()
    resume_text = "\n".join([page.page_content for page in pages])

    st.markdown("🧾 Extracted Resume Text:")
    st.text_area("Resume Content", resume_text, height=250)

mode = st.radio("🔧 Choose Mode", ["Career Chat", "Mock Interview"])

if mode == "Career Chat":
    user_input = st.text_input("💬 Ask a career question")
    if user_input:
        with st.spinner("Thinking like a career mentor..."):
            prompt = f"""
You are an AI career advisor helping users based on their resume.
Resume Text: {resume_text}
User Query: {user_input}
Respond with career insights, role suggestions, or resume tips.
"""
            response = career_chain.run(prompt)
            st.success("🎯 Advisor's Response")
            st.markdown(response)

elif mode == "Mock Interview":
    user_goal = st.text_input("🎯 What role are you preparing for?")

    if user_goal:
        with st.spinner("Running mock interview simulation..."):
            prompt = f"""
You are a professional interview simulator. Based on the resume and target role, generate a mock interview session with exactly 5 questions.

For each question:
1. Ask a relevant interview question.
2. Provide a sample answer.
3. Offer helpful tips for the user to answer that question in their own words.

Resume Text:
{resume_text}

Target Role:
{user_goal}

Format your response exactly like this:

Question 1:
Sample Answer:
Tips to Answer:

Question 2:
Sample Answer:
Tips to Answer:

Question 3:
Sample Answer:
Tips to Answer:

Question 4:
Sample Answer:
Tips to Answer:

Question 5:
Sample Answer:
Tips to Answer:

Do not skip any questions. Make sure all 5 are included.
"""
            response = career_chain.run(prompt)
            st.success("🎤 Mock Interview Simulation Complete")
            st.markdown(response)
