import streamlit as st
from langchain_agent import agent_executor
from PIL import Image
import os
import time
from dotenv import load_dotenv

load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Fintech Copilot",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="💳"
)

# Minimalistic dark theme
st.markdown("""
<style>
    .stApp {
        background-color: #0d1117;
        color: #ffffff;
    }

    .main {
        padding: 1rem;
        max-width: 800px;
        margin: 0 auto;
    }

    /* Clean input styling */
    .stTextInput > div > div > input {
        background-color: #21262d !important;
        border: 1px solid #30363d !important;
        border-radius: 8px !important;
        color: #ffffff !important;
        padding: 0.75rem !important;
        font-size: 16px !important;
    }

    .stTextInput > div > div > input:focus {
        border-color: #58a6ff !important;
        box-shadow: 0 0 0 2px rgba(88, 166, 255, 0.2) !important;
    }

    /* Clean button styling */
    .stButton > button {
        background-color: #238636 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
        font-weight: 500 !important;
        transition: background-color 0.2s ease !important;
    }

    .stButton > button:hover {
        background-color: #2ea043 !important;
    }

    /* Sidebar */
    .css-1d391kg {
        background-color: #161b22 !important;
    }

    /* Cards */
    .metric-card {
        background-color: #21262d;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
    }

    /* Messages */
    .user-message {
        background-color: #0969da;
        color: #ffffff;
        padding: 0.75rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }

    .assistant-message {
        background-color: #21262d;
        border: 1px solid #30363d;
        padding: 0.75rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }

    /* Typography */
    h1, h2, h3, h4 {
        color: #ffffff !important;
        font-weight: 600 !important;
    }

    /* Hide Streamlit elements */
    #MainMenu, footer, header {
        visibility: hidden;
    }

    .stDeployButton {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

# Simplified sidebar
with st.sidebar:
    st.markdown("### 💳 Fintech GPT")
    st.markdown("*AI Chatbot for all product questions and needs*")

    st.markdown("---")

    st.markdown("**Quick Examples:**")
    examples = [
        "Churn analysis",
        "Revenue trends",
        "Feature usage",
        "Customer segments"
    ]

    for example in examples:
        if st.button(example, key=f"sidebar_{example}", use_container_width=True):
            st.session_state.sidebar_query = example
            st.rerun()

# Minimal header
st.markdown("# 💳 Fintech GPT")
st.markdown("*Ask questions about your business data*")
st.markdown("---")

# Example queries
with st.expander("💡 Example Questions", expanded=False):
    examples = [
        "What's driving our churn rate?",
        "Show me revenue trends",
        "Which features are popular?",
        "Compare customer segments"
    ]

    cols = st.columns(2)
    for i, query in enumerate(examples):
        with cols[i % 2]:
            if st.button(query, key=f"ex_{i}", use_container_width=True):
                st.session_state.selected_query = query
                st.rerun()

# Query input
default_query = ""

# Check for queries from sidebar or examples
if 'sidebar_query' in st.session_state:
    default_query = st.session_state.sidebar_query
    del st.session_state.sidebar_query
elif 'selected_query' in st.session_state:
    default_query = st.session_state.selected_query
    del st.session_state.selected_query

query = st.text_input(
    "Ask a question:",
    value=default_query,
    placeholder="What's the churn rate by tier?",
    key="query_input"
)

analyze_button = st.button("🚀 Analyze", type="primary", use_container_width=True)

# Process query when button is clicked or when there's a default query
if analyze_button or default_query:
    current_query = query if query else default_query

    if current_query:
        with st.spinner("Analyzing..💭💭"):
            try:
                output = agent_executor.run(current_query)

                # Initialize conversation history if needed
                if 'conversation_history' not in st.session_state:
                    st.session_state.conversation_history = []

                # Add to conversation history
                st.session_state.conversation_history.append({
                    "role": "user",
                    "content": current_query,
                    "timestamp": time.time()
                })

                st.session_state.conversation_history.append({
                    "role": "assistant",
                    "content": output,
                    "timestamp": time.time()
                })

                # Clear the selected query from session state to prevent reprocessing
                if 'selected_query' in st.session_state:
                    del st.session_state.selected_query
                if 'sidebar_query' in st.session_state:
                    del st.session_state.sidebar_query

                st.success("Analysis complete!")

            except Exception as e:
                st.error(f"Error: {str(e)}")
    elif analyze_button:
        st.warning("Please enter a question first.")

# Display conversation history
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

if st.session_state.conversation_history:
    st.markdown("---")
    st.markdown("### Conversation")

    # Show only the latest conversation
    for message in st.session_state.conversation_history[-2:]:
        if message["role"] == "user":
            st.markdown(
                f'<div class="user-message">**You:** {message["content"]}</div>',
                unsafe_allow_html=True
            )
        elif message["role"] == "assistant":
            st.markdown(
                '<div class="assistant-message">',
                unsafe_allow_html=True
            )
            st.markdown(message["content"])

            # Show chart if exists
            if os.path.exists("chart.png"):
                st.image(Image.open("chart.png"), use_container_width=True)

            st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🗑️ Clear", help="Clear conversation"):
        st.session_state.conversation_history = []
        if os.path.exists("chart.png"):
            os.remove("chart.png")
        st.rerun()

