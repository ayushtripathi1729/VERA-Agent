from langchain.memory import ConversationBufferWindowMemory
from langchain_core.chat_history import InMemoryChatMessageHistory


class NeuralMemory:
    """
    Cognitive Retention Layer for V.E.R.A.
    Maintains a sliding window of recent interactions for contextual reasoning.
    """

    def __init__(self, window_size: int = 5):
        self.window_size = window_size

        self.memory = ConversationBufferWindowMemory(
            memory_key="chat_history",
            return_messages=True,
            k=window_size,
            chat_memory=InMemoryChatMessageHistory()
        )

    def get_context(self) -> dict:
        """
        Safely returns conversation context.
        Always returns valid structure.
        """
        try:
            context = self.memory.load_memory_variables({})
            if not context:
                return {"chat_history": []}

            return context

        except Exception as e:
            print(f"[!] MEMORY_CONTEXT_ERROR: {str(e)}")
            return {"chat_history": []}

    def add_exchange(self, user_input: str, ai_output: str):
        """
        Saves interaction into memory.
        Includes basic safeguards.
        """
        try:
            if not user_input or not ai_output:
                return

            self.memory.save_context(
                {"input": user_input},
                {"output": ai_output}
            )

        except Exception as e:
            print(f"[!] MEMORY_SAVE_ERROR: {str(e)}")

    def clear_memory(self):
        """
        Resets the memory buffer.
        """
        try:
            self.memory.clear()
        except Exception as e:
            print(f"[!] MEMORY_CLEAR_ERROR: {str(e)}")

    def conditional_reset(self, instruction: str):
        """
        Smart reset to avoid context pollution.
        Useful for switching domains (e.g., math → general chat).
        """
        try:
            trigger_keywords = ["new task", "reset", "start over"]

            if any(keyword in instruction.lower() for keyword in trigger_keywords):
                self.clear_memory()

        except Exception as e:
            print(f"[!] MEMORY_RESET_ERROR: {str(e)}")


# Singleton instance
vera_memory = NeuralMemory()
