import streamlit as st

st.set_page_config(page_title="Agentic Chatbot", page_icon="🤖", layout="centered")
st.title("AI Agent Chatbot")
st.write("Create and Interact with the AI Agents!")

system_prompt = st.text_area("Define your AI Agent: ", height=70, placeholder="You are an AI chatbot who is very smart and friendly.")

MODEL_NAMES_GROQ = ["qwen/qwen3.6-27b", "meta-llama/llama-prompt-guard-2-86m"]

provider = st.radio("Select Model Provider", options=["Groq"], index=0)

if provider == "Groq":
    model_name = st.selectbox("Select Model", options=MODEL_NAMES_GROQ, index=0)

allow_web_search = st.checkbox("Allow Web Search", value=False)

user_query = st.text_area("Enter your query: ", height=100, placeholder="Ask me anything!")

if st.button("Ask Agent!"):
    if not user_query.strip():
        st.warning("Please enter a query before asking the agent.")
    else:
        response = "Hi! This is dummy response."
        st.subheader("Agent's Response:")
        st.markdown(f"**Final Response: **{response}")
