"""
backend.py — Your business logic lives here.

This file is intentionally separate from the Streamlit UI code so you can
drop in your own existing code without touching the UI layer.

HOW TO INTEGRATE YOUR CODE:
  1. Replace (or add to) the `get_response` function below with your own logic.
  2. The function receives the full conversation history as a list of dicts:
       [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}, ...]
     Use `user_message` for the latest message, or `history` for full context.
  3. Return a plain string — that's what the chat UI will display.
"""


def get_response(user_message: str, history: list[dict]) -> str:
    """
    Generate a response to the user's message.

    Args:
        user_message: The latest message typed by the user.
        history:      The full conversation so far (not including the current
                      user_message). Each entry is {"role": ..., "content": ...}.

    Returns:
        A string that will be shown as the assistant's reply.

    -----------------------------------------------------------------------
    REPLACE THE BODY OF THIS FUNCTION WITH YOUR OWN LOGIC.
    Examples of what you might do here:
      - Call an LLM API (OpenAI, Anthropic, etc.)
      - Run a retrieval / RAG pipeline
      - Query a database and format results
      - Call any existing Python functions you already have
    -----------------------------------------------------------------------
    """

    # ------------------------------------------------------------------
    # STUB IMPLEMENTATION — delete everything below and add your own code
    # ------------------------------------------------------------------
    turn_number = len([m for m in history if m["role"] == "user"]) + 1
    return (
        f"[Backend stub — turn {turn_number}]\n\n"
        f'You said: "{user_message}"\n\n'
        "Replace `get_response` in backend.py with your real logic."
    )
