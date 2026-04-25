from langchain.memory import ConversationBufferWindowMemory
from langchain_core.chat_history import InMemoryChatMessageHistory

class NeuralMemory:
    """
    Cognitive Retention Layer for V.E.R.A.
    Uses a sliding window buffer to maintain context while optimizing latency.
    """

    def __init__(self, window_size: int = 5):
        # window_size=5 means it remembers the last 5 full exchanges
        # perfect for maintaining the thread of a complex coding or math task.
        self.memory = ConversationBufferWindowMemory(
            memory_key="chat_history",
            return_messages=True,
            k=window_size,
            chat_memory=InMemoryChatMessageHistory()
        )

    def get_context(self) -> dict:
        """Returns the current state of the conversation for the LLM."""
        return self.memory.load_memory_variables({})

    def add_exchange(self, user_input: str, ai_output: str):
        """Saves a new interaction into the sliding window."""
        self.memory.save_context(
            {"input": user_input},
            {"output": ai_output}
        )

    def clear_memory(self):
        """Resets the neural buffer."""
        self.memory.clear()

# Singleton instance for persistent session handling
vera_memory = NeuralMemory()
