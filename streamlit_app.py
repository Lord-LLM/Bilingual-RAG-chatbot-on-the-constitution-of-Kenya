import os

import streamlit as st
from deep_translator import GoogleTranslator
from langdetect import detect


st.set_page_config(page_title="Kenyan Constitution Chatbot")
st.title("Kenyan Constitution Chatbot")
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

            st.markdown(answer)
        except Exception as error:
            st.error(str(error))