from typing import Dict
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# --- SESSION STORE ---
# This dictionary lives in the server's RAM. 
# It maps 'session_id' -> 'chat_history_object'
store: Dict[str, InMemoryChatMessageHistory] = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    """
    Retrieves or creates a chat history for a specific user session.
    Ensures that Ayush's math discussions don't leak into other queries.
    """
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

def wrap_with_memory(agent_executor):
    """
    Wraps the V.E.R.A. executor with the memory protocol.
    This automatically manages the 'chat_history' variable in your prompt.
    """
    return RunnableWithMessageHistory(
        agent_executor,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
    )

# --- UTILITIES ---

def clear_session(session_id: str):
    """Reset the neural memory for a specific session."""
    if session_id in store:
        store[session_id].clear()
        return True
    return False
