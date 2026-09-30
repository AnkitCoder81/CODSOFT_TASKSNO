
import streamlit as st

from Task1_RuleBasedChatbot.chatbot import GROQ_MODEL, get_reply

st.set_page_config(page_title="Rule-Based + Groq Chatbot", page_icon="🤖")
st.title("🤖 Rule-Based Chatbot with Groq")
st.caption("Rules answer first. If no rule matches, a Groq LLM takes over.")

# ---------------- Sidebar ----------------
with st.sidebar:
    st.header("Settings")
    use_llm = st.toggle("Use Groq LLM fallback", value=True)


# ---------------- Chat state ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])
        if m["role"] == "assistant":
            st.caption("⚙️ rule-based" if m["source"] == "rule" else "⚡ Groq LLM")

# ---------------- New message ----------------
if prompt := st.chat_input("Type your message..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # history without the extra 'source' key, for the LLM
    history = [{"role": m["role"], "content": m["content"]}
               for m in st.session_state.messages[:-1]]

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            reply, source = get_reply(prompt, history, use_llm)
        st.markdown(reply)
        st.caption("⚙️ rule-based" if source == "rule" else "⚡ Groq LLM")

    st.session_state.messages.append(
        {"role": "assistant", "content": reply, "source": source}
    )
