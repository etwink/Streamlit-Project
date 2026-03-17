"""
app.py — Streamlit chatbot UI.

Run with:
    streamlit run app.py

All business logic lives in backend.py. This file is purely the UI layer.
"""

import streamlit as st
from backend import get_response

# ── Page configuration ─────────────────────────────────────────────────────────
# This must be the FIRST Streamlit call in the script.
# `layout="centered"` keeps the chat in a readable column; use "wide" if needed.
st.set_page_config(page_title="Chatbot POC", page_icon="💬", layout="centered")

st.title("💬 Chatbot POC")
st.caption("Powered by your backend logic in `backend.py`")

# ── Session state ──────────────────────────────────────────────────────────────
# `st.session_state` persists values across re-runs (every user interaction
# triggers a full top-to-bottom re-run of this script).
#
# We store the conversation as a list of {"role": ..., "content": ...} dicts,
# which is the standard format used by most LLM APIs — easy to pass straight
# through to OpenAI / Anthropic / etc.
if "messages" not in st.session_state:
    st.session_state.messages = []  # starts empty; add a default greeting if you like

# ── Render existing messages ───────────────────────────────────────────────────
# `st.chat_message(role)` renders a message bubble.  role can be "user" or
# "assistant" (or any string — Streamlit will pick an icon automatically).
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ── Accept new user input ──────────────────────────────────────────────────────
# `st.chat_input` renders the input bar pinned to the bottom of the page.
# It returns the submitted text (or None if nothing was submitted this run).
user_input = st.chat_input("Type a message…")

if user_input:
    # 1. Display the user's message immediately
    with st.chat_message("user"):
        st.markdown(user_input)

    # 2. Append it to history BEFORE calling the backend so the backend can
    #    see the full conversation including the current turn if needed.
    #    (We pass history *before* this message so the backend receives only
    #    prior turns — adjust to taste.)
    prior_history = st.session_state.messages.copy()
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 3. Call your backend — swap this out for anything you like
    with st.spinner("Thinking…"):
        response = get_response(user_message=user_input, history=prior_history)

    # 4. Display the assistant response
    with st.chat_message("assistant"):
        st.markdown(response)

    # 5. Persist the response so it's shown on the next re-run
    st.session_state.messages.append({"role": "assistant", "content": response})

# ── Optional sidebar controls ──────────────────────────────────────────────────
# The sidebar is a good place for configuration knobs, debug info, etc.
with st.sidebar:
    st.header("Controls")

    if st.button("Clear conversation"):
        st.session_state.messages = []
        st.rerun()  # force an immediate re-run to clear the displayed messages

    # Show raw message history for debugging — remove when not needed
    with st.expander("Debug: raw message history"):
        st.json(st.session_state.messages)
