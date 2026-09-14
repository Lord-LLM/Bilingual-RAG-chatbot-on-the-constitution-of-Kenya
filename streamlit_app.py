import os
from html import escape

import streamlit as st
from deep_translator import GoogleTranslator
from langdetect import detect


st.set_page_config(page_title="Kenyan Constitution Chatbot")
st.markdown(
    """
    <style>
        .stApp {
            background: #121212;
            color: #fff;
        }
        .block-container {
            max-width: 800px;
            padding-top: 1rem;
        }
        .kenya-stripes {
            height: 40px;
            display: flex;
            flex-direction: column;
            margin-bottom: 1.25rem;
        }
        .kenya-stripes span {
            flex: 1;
        }
        .stripe-black { background: #000; }
        .stripe-white { background: #fff; }
        .stripe-red { background: #f00; }
        .stripe-green { background: green; }
        .chatbot-header {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 15px;
            padding: 20px 10px;
        }
        .chatbot-header img {
            width: 64px;
            height: 50px;
            object-fit: cover;
        }
        .chatbot-header h1 {
            color: #f00;
            font-family: Arial, sans-serif;
            font-size: 32px;
            line-height: 1.15;
            margin: 0;
            text-align: center;
        }
        [data-testid="stTextArea"] textarea,
        [data-testid="stSelectbox"] div[data-baseweb="select"] > div {
            background: #2a2a2a;
            color: #fff;
            border: 2px solid #fff;
            border-radius: 5px;
        }
        [data-testid="stTextArea"] textarea {
            min-height: 100px;
        }
        [data-testid="stTextArea"] label,
        [data-testid="stSelectbox"] label {
            color: #ccc;
        }
        div.stButton > button {
            width: 100%;
            background: green;
            color: #fff;
            border: 2px solid #fff;
            border-radius: 5px;
            font-weight: bold;
        }
        div.stButton > button:hover {
            background: #f00;
            color: #fff;
            border-color: #fff;
        }
        .response-box {
            background: #1e1e1e;
            border-left: 6px solid #f00;
            border-radius: 5px;
            color: #fff;
            font-family: Consolas, monospace;
            min-height: 100px;
            margin-top: 15px;
            padding: 15px;
            white-space: pre-wrap;
        }
    </style>
    <div class="kenya-stripes">
        <span class="stripe-black"></span>
        <span class="stripe-white"></span>
        <span class="stripe-red"></span>
        <span class="stripe-white"></span>
        <span class="stripe-green"></span>
    </div>
    <div class="chatbot-header">
        <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/4/49/Flag_of_Kenya.svg/1200px-Flag_of_Kenya.svg.png" alt="Kenya flag">
        <h1>Kenyan Constitution Chatbot</h1>
        <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/4/49/Flag_of_Kenya.svg/1200px-Flag_of_Kenya.svg.png" alt="Kenya flag">
    </div>
    """,
    unsafe_allow_html=True,
)
st.caption("Ask questions in English or Swahili.")


def get_api_key():
    try:
        return st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
    except FileNotFoundError:
        return os.getenv("GROQ_API_KEY")


@st.cache_resource(show_spinner="Loading the Constitution knowledge base...")
def load_rag_components():
    api_key = get_api_key()
    if not api_key:
        raise RuntimeError("Configure GROQ_API_KEY in Streamlit secrets or the environment.")

    os.environ["GROQ_API_KEY"] = api_key
    from RAG_logic import generate_response, query_constitution, setup_knowledge_base

    setup_knowledge_base()
    return query_constitution, generate_response


question = st.text_area("Question", placeholder="Ask about Kenya's Constitution...")
language = st.selectbox("Response language", ["English", "Swahili"])

if st.button("Ask", type="primary"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        try:
            query_constitution, generate_response = load_rag_components()
            input_language = detect(question)
            translated_question = question
            if input_language == "sw":
                translated_question = GoogleTranslator(source="sw", target="en").translate(question)

            context = "\n".join(query_constitution(translated_question))
            answer = generate_response(translated_question, context)
            if language == "Swahili" or input_language == "sw":
                answer = GoogleTranslator(source="en", target="sw").translate(answer)

            safe_answer = escape(answer).replace("\n", "<br>")
            st.markdown(f'<div class="response-box">{safe_answer}</div>', unsafe_allow_html=True)
        except Exception as error:
            st.error(str(error))