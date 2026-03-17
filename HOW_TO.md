# Streamlit Chatbot — How-To Guide

## Project layout

```
Streamlit Project/
├── app.py           ← UI only — you should rarely need to edit this
├── backend.py       ← YOUR CODE GOES HERE
├── requirements.txt
└── HOW_TO.md        ← this file
```

---

## 1. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 2. Run the app

```bash
streamlit run app.py
```

Streamlit opens a browser tab automatically at `http://localhost:8501`.
Every time you save a file, Streamlit offers to hot-reload — click **"Always rerun"**
at the top of the page so edits apply instantly.

---

## 3. Plug in your existing code

Open **`backend.py`** and replace the body of `get_response`:

```python
def get_response(user_message: str, history: list[dict]) -> str:
    # YOUR CODE HERE
    # Return a plain string to display in the chat.
    ...
```

### What you receive

| Parameter | Type | Description |
|-----------|------|-------------|
| `user_message` | `str` | The text the user just typed |
| `history` | `list[dict]` | All previous turns, each as `{"role": "user"/"assistant", "content": "..."}` |

### What you must return

A **plain string**. It supports Markdown (bold, code blocks, bullet lists, etc.)
because the UI renders it with `st.markdown()`.

### Common patterns

**Calling an LLM API (e.g. Anthropic)**
```python
import anthropic

client = anthropic.Anthropic(api_key="sk-...")

def get_response(user_message, history):
    messages = history + [{"role": "user", "content": user_message}]
    result = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        messages=messages,
    )
    return result.content[0].text
```

**Calling a simple function you already have**
```python
from my_module import answer_question   # your existing code

def get_response(user_message, history):
    return answer_question(user_message)
```

**Using the conversation history for context**
```python
def get_response(user_message, history):
    # history is a list of dicts — pass it straight to most LLM APIs
    context = "\n".join(f"{m['role']}: {m['content']}" for m in history)
    return your_llm_call(user_message, context)
```

---

## 4. Key Streamlit concepts used in app.py

### Re-runs
Every user interaction (button click, chat submit, etc.) causes Streamlit to
re-execute **the entire script from top to bottom**. This is by design — it
keeps the UI declarative.
Think of each run as "render the current state."

### `st.session_state`
Because the script re-runs on every interaction, regular Python variables reset.
`st.session_state` is a dict-like object that **persists across re-runs**.
That's where the message history lives.

```python
# Initialize once
if "messages" not in st.session_state:
    st.session_state.messages = []

# Read/write anywhere
st.session_state.messages.append({"role": "user", "content": "Hello"})
```

### Chat widgets (Streamlit 1.12.0)
> `st.chat_input` and `st.chat_message` are **not available** until 1.18.0.
> The app uses the following equivalents instead:

| Widget | Purpose |
|--------|---------|
| `st.form(key, clear_on_submit=True)` | Groups widgets so the script only re-runs on submit, not every keystroke |
| `st.text_input("label")` | Single-line message input inside the form |
| `st.form_submit_button("Send")` | Submit button; returns `True` on the run it is clicked |
| `st.markdown(html, unsafe_allow_html=True)` | Used to render styled message bubbles via inline HTML/CSS |
| `st.spinner("text")` | Shows a loading indicator while your backend runs |

### Sidebar & misc
| Widget | Purpose |
|--------|---------|
| `st.sidebar` | Context manager for the collapsible left panel |
| `st.button("label")` | Returns `True` only on the run where it was clicked |
| `st.experimental_rerun()` | Forces an immediate re-run — this is the 1.12.0 name (renamed to `st.rerun()` in 1.27) |
| `st.expander("label")` | Collapsible section — great for debug output |

---

## 5. Adding new UI elements

Drop any Streamlit widget directly into `app.py`.
Full widget reference: https://docs.streamlit.io/develop/api-reference

Common additions for a chatbot:

- **Model selector** — `st.sidebar.selectbox("Model", ["gpt-4o", "claude-opus-4-6"])`
- **System prompt editor** — `st.sidebar.text_area("System prompt")`
- **File uploader** — `st.file_uploader("Upload a document")` for RAG demos
- **Streaming responses** — use `st.write_stream(generator)` with a generator
  that yields text chunks from your LLM

---

## 6. Deploying (optional)

For a quick shareable demo, push the repo to GitHub and deploy for free at
[streamlit.io/cloud](https://streamlit.io/cloud).
Set any API keys as **Secrets** in the Streamlit Cloud dashboard (never
hard-code them).
