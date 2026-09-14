import os
from html import escape

import streamlit as st
from deep_translator import GoogleTranslator
from langdetect import detect


st.set_page_config(page_title="Kenyan Constitution Chatbot")
st.markdown(
    """
    <style>
        :root {
            --ink: #f5f5f0;
            --muted: #a7aaa4;
            --panel: #1a1c1a;
            --field: #242724;
            --line: #3d423d;
            --red: #e6392f;
            --green: #2f8f54;
        }
        .stApp {
            background: #101210;
            color: var(--ink);
        }
        .block-container {
            max-width: 860px;
            padding: 2rem 1.5rem 4rem;
        }
        .kenya-stripes {
            height: 7px;
            display: flex;
            flex-direction: row;
            margin-bottom: 2.2rem;
            overflow: hidden;
            border-radius: 2px;
        }
        .kenya-stripes span {
            flex: 1;
        }
        .stripe-black { background: #050505; }
        .stripe-white { background: #e9e9e1; }
        .stripe-red { background: var(--red); }
        .stripe-green { background: var(--green); }
        .chatbot-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 24px;
            padding: 0 0 2.5rem;
            border-bottom: 1px solid var(--line);
        }
        .kenya-flag {
            display: flex;
            flex-direction: column;
            position: relative;
            width: 70px;
            height: 46px;
            border: 1px solid #626660;
            border-radius: 2px;
            flex: 0 0 auto;
            overflow: hidden;
            box-shadow: 0 5px 18px #0008;
        }
        .kenya-flag > span:not(.flag-shield) {
            flex: 1;
        }
        .flag-black { background: #000; }
        .flag-white { background: #fff; }
        .flag-red { background: #f00; }
        .flag-green { background: green; }
        .flag-shield {
            position: absolute;
            left: 50%;
            top: 50%;
            width: 11px;
            height: 34px;
            background: var(--red);
            border: 2px solid #080808;
            border-radius: 50%;
            transform: translate(-50%, -50%);
        }
        .chatbot-header h1 {
            color: var(--ink);
            font-family: Georgia, serif;
            font-size: clamp(2rem, 5vw, 3.6rem);
            font-weight: 400;
            letter-spacing: -1px;
            margin: 0;
            text-align: center;
            line-height: 1;
        }
        .eyebrow {
            color: var(--red);
            font-family: monospace;
            font-size: .72rem;
            font-weight: bold;
            letter-spacing: 2px;
            margin: 2rem 0 .55rem;
            text-transform: uppercase;
        }
        .intro {
            color: var(--muted);
            font-size: 1rem;
            margin: 0 0 1.6rem;
        }
        .question-panel {
            background: var(--panel);
            border: 1px solid var(--line);
            border-radius: 4px;
            padding: 1.1rem 1.2rem .7rem;
            box-shadow: 0 16px 35px #0003;
        }
        .field-label {
            color: var(--ink);
            font-size: .82rem;
            font-weight: 700;
            letter-spacing: .4px;
            margin: 0 0 .45rem;
        }
        [data-testid="stTextArea"] textarea {
            background: var(--field);
            border: 1px solid var(--line);
            border-radius: 3px;
            color: var(--ink);
            min-height: 130px;
            padding: .8rem;
        }
        [data-testid="stTextArea"] textarea:focus {
            border-color: var(--red);
            box-shadow: 0 0 0 1px var(--red);
        }
        [data-testid="stSelectbox"] div[data-baseweb="select"] > div {
            background: var(--field);
            border: 1px solid var(--line);
            border-radius: 3px;
            color: var(--ink);
        }
        div.stButton > button {
            width: 100%;
            background: var(--green);
            color: #fff;
            border: 1px solid #67b57e;
            border-radius: 3px;
            font-weight: bold;
            min-height: 44px;
            margin-top: 1.55rem;
        }
        div.stButton > button:hover {
            background: var(--red);
            color: #fff;
            border-color: #ff8b84;
        }
        .response-heading {
            align-items: baseline;
            display: flex;
            justify-content: space-between;
            margin: 2.3rem 0 .65rem;
        }
        .response-heading strong {
            color: var(--ink);
            font-family: Georgia, serif;
            font-size: 1.35rem;
            font-weight: 400;
        }
        .response-heading span {
            color: var(--muted);
            font-family: monospace;
            font-size: .7rem;
            text-transform: uppercase;
        }
        .response-box {
            background: var(--panel);
            border: 1px solid var(--line);
            border-left: 4px solid var(--red);
            border-radius: 3px;
            color: #e8e9e2;
            font-family: Georgia, serif;
            font-size: 1.02rem;
            line-height: 1.7;
            min-height: 110px;
            padding: 1.2rem 1.3rem;
            white-space: pre-wrap;
        }
        @media (max-width: 600px) {
            .block-container { padding: 1rem 1rem 3rem; }
            .chatbot-header { gap: 10px; padding-bottom: 1.8rem; }
            .chatbot-header h1 { font-size: 2rem; }
            .kenya-flag { width: 48px; height: 34px; }
            .question-panel { padding: .85rem .85rem .5rem; }
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
        <div class="kenya-flag" role="img" aria-label="Kenya flag">
            <span class="flag-black"></span><span class="flag-white"></span><span class="flag-red"></span><span class="flag-white"></span><span class="flag-green"></span>
            <span class="flag-shield"></span>
        </div>
        <h1>Kenyan Constitution Chatbot</h1>
        <div class="kenya-flag" role="img" aria-label="Kenya flag">
            <span class="flag-black"></span><span class="flag-white"></span><span class="flag-red"></span><span class="flag-white"></span><span class="flag-green"></span>
            <span class="flag-shield"></span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
st.markdown('<div class="eyebrow">Constitutional research assistant</div>', unsafe_allow_html=True)
st.markdown(
    '<p class="intro">Grounded answers from the Constitution of Kenya, in English or Swahili.</p>',
    unsafe_allow_html=True,
)


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


st.markdown('<div class="field-label">Your question</div>', unsafe_allow_html=True)
question = st.text_area(
    "Question",
    placeholder="For example: What rights are protected under Article 27?",
    label_visibility="collapsed",
)
st.markdown('<div class="field-label">Answer language</div>', unsafe_allow_html=True)
language = st.selectbox(
    "Response language",
    ["English", "Swahili"],
    label_visibility="collapsed",
)

if st.button("Ask", type="primary"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        current_step = "starting"
        try:
            current_step = "loading the knowledge base"
            query_constitution, generate_response = load_rag_components()
            current_step = "detecting the question language"
            input_language = detect(question)
            translated_question = question
            if input_language == "sw":
                current_step = "translating the question"
                translated_question = GoogleTranslator(source="sw", target="en").translate(question)

            current_step = "searching the Constitution"
            context = "\n".join(query_constitution(translated_question))
            current_step = "generating the answer"
            answer = generate_response(translated_question, context)
            if language == "Swahili" or input_language == "sw":
                current_step = "translating the answer"
                answer = GoogleTranslator(source="en", target="sw").translate(answer)

            st.markdown(
                '<div class="response-heading"><strong>Response</strong>'
                '<span>Constitutional assistant</span></div>',
                unsafe_allow_html=True,
            )
            safe_answer = escape(answer).replace("\n", "<br>")
            st.markdown(f'<div class="response-box">{safe_answer}</div>', unsafe_allow_html=True)
        except Exception as error:
            st.error(f"The assistant failed while {current_step}: {error}")
            with st.expander("Technical details"):
                st.exception(error)
