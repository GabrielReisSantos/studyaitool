import os
import fitz  # PyMuPDF
import random
import re
from gtts import gTTS
from tempfile import NamedTemporaryFile
import streamlit as st
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# App Config
st.set_page_config(page_title="Gabriel's Mind", layout="wide")
st.title("🧠 Gabriel's Mind: AI Study Tool")

# Sidebar Settings
st.sidebar.title("⚙️ Settings")
api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")
language = st.sidebar.selectbox(
    "Choose Output Language",
    ["English", "Portuguese", "Spanish", "French", "Italian", "Polish", "Dutch"]
)
lang_code = {
    "English": "en", "Portuguese": "pt", "Spanish": "es", "French": "fr",
    "Italian": "it", "Polish": "pl", "Dutch": "nl"
}[language]

if not api_key:
    st.warning("Please enter your OpenAI API Key to continue.")
    st.stop()

embedding = OpenAIEmbeddings(openai_api_key=api_key)

# File Uploader
uploaded_file = st.file_uploader("📄 Upload a PDF to study", type=["pdf"])
if uploaded_file:
    with NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    loader = PyPDFLoader(tmp_path)
    documents = loader.load()
    chunks = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200).split_documents(documents)
    full_text = " ".join([doc.page_content for doc in chunks])

    # PDF Viewer
    st.subheader("📘 PDF Preview")
    doc = fitz.open(tmp_path)
    total_pages = doc.page_count
    selected_page = st.slider("Page", 1, total_pages, 1)
    page = doc.load_page(selected_page - 1)
    pix = page.get_pixmap()
    img_path = os.path.join(os.path.dirname(tmp_path), "page.png")
    pix.save(img_path)
    st.image(img_path, use_container_width=True)

    # AI Assistant
    st.divider()
    st.subheader("Type your question about this document...")
    query = st.text_input("Type your question about this document...")
    if query:
        prompt = PromptTemplate.from_template(f"""Answer the question using the document:
{{context}}

Question:
{{question}}

Respond in {language} language.""")
        llm = ChatOpenAI(openai_api_key=api_key)
        chain = LLMChain(llm=llm, prompt=prompt)
        response = chain.run({"context": full_text, "question": query})
        st.success(response)

        tts = gTTS(response, lang=lang_code)
        temp_file = NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(temp_file.name)
        st.audio(temp_file.name)

    # Flashcards & Quiz
    st.divider()
    st.subheader("Practice with Flashcards or Quiz")
    mode = st.radio("Choose a mode:", ["Flashcards", "Quiz", "Audio Flashcards"])

    if st.button("Generate"):
        llm = ChatOpenAI(openai_api_key=api_key)
        content = random.choice(chunks).page_content.strip()

        if mode == "Flashcards" or mode == "Audio Flashcards":
            flashcard_prompt = PromptTemplate.from_template(f"""Generate 5 flashcards based on the following content. Respond in {language}.

Question: <question>
Answer: <answer>

{{content}}""")
            chain = LLMChain(llm=llm, prompt=flashcard_prompt)
            result = chain.run({"content": content})
            flashcards = re.findall(r"Question:(.*?)\nAnswer:(.*?)\n", result, re.DOTALL)

            for i, (q, a) in enumerate(flashcards):
                st.markdown(f"**Q{i+1}: {q.strip()}**")
                if mode == "Audio Flashcards":
                    if st.button(f"🔊 Play Q{i+1}", key=f"audio_{i}"):
                        tts = gTTS(f"{q.strip()} {a.strip()}", lang=lang_code)
                        temp_file = NamedTemporaryFile(delete=False, suffix=".mp3")
                        tts.save(temp_file.name)
                        st.audio(temp_file.name)
                with st.expander("Show Answer"):
                    st.write(a.strip())

        elif mode == "Quiz":
            quiz_prompt = PromptTemplate.from_template(f"""Generate 5 multiple-choice questions from this content. Respond in {language}.
Format:

Question: <question>
A) Option A
B) Option B
C) Option C
D) Option D
Correct Answer: <letter>) <answer>

{{content}}""")
            chain = LLMChain(llm=llm, prompt=quiz_prompt)
            result = chain.run({"content": content})
            questions = re.split(r"Question:", result)[1:]

            for i, block in enumerate(questions):
                match = re.search(
                    r"(.*?)\nA\)(.*?)\nB\)(.*?)\nC\)(.*?)\nD\)(.*?)\nCorrect Answer:\s*(.*?)\)\s*(.*)",
                    block.strip(), re.DOTALL
                )
                if match:
                    q_text = match.group(1).strip()
                    options = {
                        "A": match.group(2).strip(),
                        "B": match.group(3).strip(),
                        "C": match.group(4).strip(),
                        "D": match.group(5).strip()
                    }
                    correct = match.group(6).strip()
                    correct_text = match.group(7).strip()

                    with st.expander(f"❓ Q{i+1}: {q_text}"):
                        for k, v in options.items():
                            st.markdown(f"{k}) {v}")
                        st.markdown(f"✅ **Correct Answer:** {correct}) {correct_text}")
