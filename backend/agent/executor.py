import os
from typing import Dict, Any
from langchain_groq import ChatGroq
from langchain.agents import AgentExecutor, create_tool_calling_agent

# Direct sub-module imports for Python 3.14 compatibility
from agent import get_core_prompt
from agent.memory import vera_memory
from agent.tools import get_default_tools

class VERAExecutor:
    """
    The Operational Core of V.E.R.A.
    Coordinates LLM reasoning, Memory retrieval, and Tool execution.
    """

    def __init__(self):
        # Initialize the LPU-powered Llama 3 model
        # Temperature is low (0.2) to ensure mathematical and technical accuracy.
        self.llm = ChatGroq(
            temperature=0.2,
            model_name="llama3-70b-8192",
            groq_api_key=os.getenv("GROQ_API_KEY")
        )
        
        # Load the centralized System DNA
        self.prompt = get_core_prompt()
        
        # Load the sensory and logic toolbelt
        self.tools = get_default_tools()
        
        # Initialize the agent logic
        self._agent = create_tool_calling_agent(self.llm, self.tools, self.prompt)
        
        # The Executor manages the Thought-Action-Observation loop
        self.executor = AgentExecutor(
            agent=self._agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=10,      # High depth for complex math conjectures
            return_intermediate_steps=True
        )

    async def execute(self, instruction: str) -> str:
        """
        The primary execution entry point. 
        Handles stateful memory and asynchronous processing.
        """
        try:
            # 1. Retrieve the last 5 exchanges from the Neural Memory
            context = vera_memory.get_context()
            chat_history = context.get("chat_history", [])

            # 2. Invoke the agentic reasoning process
            response = await self.executor.ainvoke({
                "input": instruction,
                "chat_history": chat_history
            })

            final_output = response["output"]

            # 3. Commit the new exchange to the sliding window memory
            vera_memory.add_exchange(instruction, final_output)

            return final_output

        except Exception as e:
            # Error recovery for Node JKIAPT_01
            print(f"[!] EXECUTOR_CRITICAL: {str(e)}")
            return f"SYSTEM_FAILURE: Unable to process instruction due to: {str(e)}"

# Singleton instance for server-wide reuse
vera_executor = VERAExecutor()
