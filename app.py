"""
app.py — Streamlit chatbot UI (compatible with Streamlit 1.12.0).

Run with:
    streamlit run app.py

NOTE: st.chat_input and st.chat_message were added in Streamlit 1.18.0 and are
NOT available in 1.12.0.  This file replicates the same experience using:
  - st.form + st.text_input + st.form_submit_button  (input bar)
  - st.markdown with inline HTML/CSS                 (message bubbles)
  - st.session_state                                 (conversation history)

All business logic lives in backend.py — this file is purely the UI layer.
"""

import streamlit as st
from backend import get_response

# ── Page configuration ─────────────────────────────────────────────────────────
# Must be the FIRST Streamlit call in the script.
st.set_page_config(page_title="Chatbot POC", page_icon="💬", layout="centered")

st.title("💬 Chatbot POC")
st.caption("Powered by your backend logic in `backend.py`")

# ── Session state ──────────────────────────────────────────────────────────────
# st.session_state persists values across re-runs (every interaction causes a
# full top-to-bottom re-execution of this script).
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── CSS for message bubbles ────────────────────────────────────────────────────
# st.chat_message doesn't exist in 1.12.0, so we fake it with styled divs.
st.markdown(
    """
    <style>
    .chat-wrapper   { display: flex; flex-direction: column; gap: 0.75rem; margin-bottom: 1rem; }
    .bubble         { padding: 0.6rem 1rem; border-radius: 12px; max-width: 80%;
                      line-height: 1.5; font-size: 0.95rem; white-space: pre-wrap; }
    .user-row       { display: flex; justify-content: flex-end; }
    .assistant-row  { display: flex; justify-content: flex-start; }
    .user-bubble    { background: #0084ff; color: white; border-bottom-right-radius: 2px; }
    .assistant-bubble { background: #f0f2f6; color: #262730; border-bottom-left-radius: 2px; }
    .role-label     { font-size: 0.75rem; color: #888; margin-bottom: 2px; }
    /* Hide the text_input label (label_visibility param not available in 1.12) */
    .chat-input-label label { display: none; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Render existing messages ───────────────────────────────────────────────────
# We build one HTML block for the whole history so there are no extra
# Streamlit element borders between bubbles.
if st.session_state.messages:
    rows_html = '<div class="chat-wrapper">'
    for msg in st.session_state.messages:
        # Escape HTML special characters to prevent XSS from message content
        safe_content = (
            msg["content"]
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )
        if msg["role"] == "user":
            rows_html += (
                '<div class="user-row">'
                f'<div class="bubble user-bubble">{safe_content}</div>'
                "</div>"
            )
        else:
            rows_html += (
                '<div class="assistant-row">'
                f'<div class="bubble assistant-bubble">{safe_content}</div>'
                "</div>"
            )
    rows_html += "</div>"
    st.markdown(rows_html, unsafe_allow_html=True)
else:
    st.markdown("*No messages yet — say something below!*")

st.markdown("---")

# ── Input form ─────────────────────────────────────────────────────────────────
# st.form batches all widget interactions so the script only re-runs when the
# user explicitly submits (either Enter in the text field or the Send button).
# Without a form, every keystroke would trigger a re-run.
with st.form(key="chat_form", clear_on_submit=True):
    # clear_on_submit=True empties the text field after the form is submitted.
    # label_visibility was added in 1.13.0 — we hide the label via CSS instead.
    st.markdown('<div class="chat-input-label">', unsafe_allow_html=True)
    user_input = st.text_input(
        "Your message",
        placeholder="Type a message and press Enter…",
    )
    st.markdown("</div>", unsafe_allow_html=True)
    submitted = st.form_submit_button("Send")

# ── Handle submission ──────────────────────────────────────────────────────────
# This block runs only when submitted=True (i.e. the user clicked Send or
# pressed Enter).  It is OUTSIDE the form context so we can call st.spinner.
if submitted and user_input.strip():
    # 1. Capture history before appending the new message
    prior_history = st.session_state.messages.copy()

    # 2. Persist the user's message
    st.session_state.messages.append({"role": "user", "content": user_input.strip()})

    # 3. Call your backend — replace get_response in backend.py with your logic
    with st.spinner("Thinking…"):
        response = get_response(user_message=user_input.strip(), history=prior_history)

    # 4. Persist the assistant response
    st.session_state.messages.append({"role": "assistant", "content": response})

    # 5. Re-run so the new messages are rendered above the input box
    #    (st.experimental_rerun is the 1.12.0 name; renamed to st.rerun in 1.27)
    st.experimental_rerun()

# ── Sidebar controls ───────────────────────────────────────────────────────────
with st.sidebar:
    st.header("Controls")

    if st.button("Clear conversation"):
        st.session_state.messages = []
        st.experimental_rerun()

    # Debug panel — remove when no longer needed
    with st.expander("Debug: raw message history"):
        st.json(st.session_state.messages)
