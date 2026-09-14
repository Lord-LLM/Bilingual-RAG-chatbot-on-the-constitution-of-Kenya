import os

import streamlit as st
from langdetect import detect, LangDetectException


st.set_page_config(
    page_title="Kenyan Constitution Chatbot",
    page_icon="🇰🇪",
    layout="centered",
)

# ----------------------------------------------------------------------------
# Styling
# ----------------------------------------------------------------------------
st.markdown(
    """
    <style>
        :root {
            --ink: #eef0ec;
            --muted: #8d9389;
            --panel: #171917;
            --panel-2: #1e211e;
            --line: #2c302b;
            --red: #e6392f;
            --green: #2f8f54;
            --radius: 12px;
        }

        html, body, [class*="css"]  {
            font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI",
                Roboto, sans-serif;
        }

        .stApp { background: #0d0f0d; color: var(--ink); }
        .block-container { max-width: 780px; padding: 1.6rem 1.2rem 6rem; }

        #MainMenu, header, footer { visibility: hidden; }

        .kenya-stripes {
            height: 5px;
            display: flex;
            border-radius: 999px;
            overflow: hidden;
            margin-bottom: 1.4rem;
        }
        .kenya-stripes span { flex: 1; }
        .stripe-black { background: #050505; }
        .stripe-white { background: #e9e9e1; }
        .stripe-red { background: var(--red); }
        .stripe-green { background: var(--green); }

        .app-header {
            display: flex;
            align-items: center;
            gap: 14px;
            margin-bottom: 0.3rem;
        }
        .app-header .emoji { font-size: 1.9rem; line-height: 1; }
        .app-header h1 {
            font-size: 1.5rem;
            font-weight: 650;
            letter-spacing: -0.02em;
            margin: 0;
            color: var(--ink);
        }
        .app-sub {
            color: var(--muted);
            font-size: 0.92rem;
            margin: 0 0 1.8rem;
        }

        .badge {
            display: inline-block;
            font-family: ui-monospace, SFMono-Regular, monospace;
            font-size: 0.68rem;
            letter-spacing: 0.03em;
            color: var(--muted);
            background: var(--panel-2);
            border: 1px solid var(--line);
            border-radius: 999px;
            padding: 2px 9px;
            margin-top: 6px;
        }

        [data-testid="stChatMessage"] {
            background: var(--panel);
            border: 1px solid var(--line);
            border-radius: var(--radius);
            padding: 0.9rem 1.1rem;
            margin-bottom: 0.7rem;
        }

        [data-testid="stChatMessageAvatarUser"] { background: var(--panel-2) !important; }
        [data-testid="stChatMessageAvatarAssistant"] {
            background: var(--red) !important;
        }

        [data-testid="stChatInput"] textarea {
            background: var(--panel) !important;
            border: 1px solid var(--line) !important;
            border-radius: var(--radius) !important;
            color: var(--ink) !important;
        }
        [data-testid="stChatInput"] {
            border-top: 1px solid var(--line);
        }

        section[data-testid="stSidebar"] {
            background: #0d0f0d;
            border-right: 1px solid var(--line);
        }
        section[data-testid="stSidebar"] .stSelectbox label {
            color: var(--muted) !important;
            font-size: 0.8rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }
        div[data-baseweb="select"] > div {
            background: var(--panel) !important;
            border: 1px solid var(--line) !important;
            border-radius: 8px !important;
            color: var(--ink) !important;
        }

        div.stButton > button {
            width: 100%;
            background: var(--panel-2);
            color: var(--ink);
            border: 1px solid var(--line);
            border-radius: 8px;
            font-weight: 600;
        }
        div.stButton > button:hover {
            border-color: var(--red);
            color: var(--red);
        }

        .empty-state {
            text-align: center;
            color: var(--muted);
            padding: 3.5rem 1rem;
            font-size: 0.95rem;
        }
    </style>

    <div class="kenya-stripes">
        <span class="stripe-black"></span>
        <span class="stripe-white"></span>
        <span class="stripe-red"></span>
        <span class="stripe-white"></span>
        <span class="stripe-green"></span>
    </div>
    <div class="app-header">
        <span class="emoji">🇰🇪</span>
        <h1>Kenyan Constitution Chatbot</h1>
    </div>
    <p class="app-sub">Grounded answers from the Constitution of Kenya, in English or Swahili.</p>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# Backend helpers
# ----------------------------------------------------------------------------
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


def detect_language_label(text: str) -> str | None:
    try:
        code = detect(text)
    except LangDetectException:
        return None
    labels = {"en": "English", "sw": "Swahili"}
    return labels.get(code, code)


# ----------------------------------------------------------------------------
# Sidebar controls
# ----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### Settings")
    language = st.selectbox("Answer language", ["English", "Swahili"])
    st.markdown("---")
    if st.button("Clear conversation"):
        st.session_state.messages = []
        st.rerun()
    st.markdown(
        '<p style="color:#8d9389; font-size:0.8rem; margin-top:1rem;">'
        "Answers are generated from the Constitution of Kenya and may be "
        "incomplete. Verify anything important against the official text."
        "</p>",
        unsafe_allow_html=True,
    )

# ----------------------------------------------------------------------------
# Chat state + history
# ----------------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []  # list of {"role", "content", "badge"}

if not st.session_state.messages:
    st.markdown(
        '<div class="empty-state">Ask a question about the Constitution of Kenya '
        "to get started &mdash; for example, "
        '<em>&ldquo;What rights are protected under Article 27?&rdquo;</em></div>',
        unsafe_allow_html=True,
    )

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("badge"):
            st.markdown(f'<span class="badge">{message["badge"]}</span>', unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# Chat input
# ----------------------------------------------------------------------------
question = st.chat_input("Ask about the Constitution of Kenya...")

if question:
    detected = detect_language_label(question)
    user_badge = f"detected: {detected}" if detected else None

    st.session_state.messages.append(
        {"role": "user", "content": question, "badge": user_badge}
    )
    with st.chat_message("user"):
        st.markdown(question)
        if user_badge:
            st.markdown(f'<span class="badge">{user_badge}</span>', unsafe_allow_html=True)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        current_step = "starting"
        try:
            with st.spinner("Consulting the Constitution..."):
                current_step = "loading the knowledge base"
                query_constitution, generate_response = load_rag_components()

                current_step = "searching the Constitution"
                context = "\n".join(query_constitution(question))

                current_step = "generating the answer"
                answer = generate_response(question, context, language)

            # Rendered as Markdown so headings, bold text, lists and links
            # from the model's response display correctly instead of raw text.
            placeholder.markdown(answer)
            st.markdown(f'<span class="badge">answered in {language}</span>', unsafe_allow_html=True)
            st.session_state.messages.append(
                {"role": "assistant", "content": answer, "badge": f"answered in {language}"}
            )
        except Exception as error:
            placeholder.error(f"The assistant failed while {current_step}: {error}")
            with st.expander("Technical details"):
                st.exception(error)
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": f"⚠️ The assistant failed while {current_step}: {error}",
                    "badge": None,
                }
            )