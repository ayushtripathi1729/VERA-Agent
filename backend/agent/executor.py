import os
from typing import List, Dict, Any
from langchain_groq import ChatGroq
from langchain.agents import AgentExecutor, create_tool_calling_agent
from agent import get_core_prompt
from agent.tools.registry import get_default_tools

class VERAExecutor:
    """
    The Operational Core of V.E.R.A.
    Handles the orchestration of LLM reasoning and tool execution.
    """

    def __init__(self):
        # Initializing the LPU-powered Llama 3 model
        self.llm = ChatGroq(
            temperature=0.2, # Low temperature for high technical precision
            model_name="llama3-70b-8192",
            groq_api_key=os.getenv("GROQ_API_KEY")
        )
        
        # Pulling the centralized prompt DNA from __init__.py
        self.prompt = get_core_prompt()
        
        # Initializing the toolbelt
        self.tools = get_default_tools()
        
        # Creating the internal agentic brain
        self._agent = create_tool_calling_agent(self.llm, self.tools, self.prompt)
        
        # The Executor handles the "loop" (Thinking -> Acting -> Observing)
        self.executor = AgentExecutor(
            agent=self._agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=5 # Preventing infinite loops in complex math problems
        )

    async def run(self, instruction: str) -> Dict[str, Any]:
        """
        Executes a high-level instruction and returns structured logs.
        """
        try:
            # We use ainvoke for non-blocking execution on Render
            response = await self.executor.ainvoke({"input": instruction})
            
            return {
                "status": "SUCCESS",
                "output": response["output"],
                "intermediate_steps": response.get("intermediate_steps", [])
            }
        except Exception as e:
            return {
                "status": "CRITICAL_ERROR",
                "output": f"Internal Core Failure: {str(e)}",
                "node": "JKIAPT_PRAYAGRAJ_NODE_01"
            }

# Singleton instance for high-performance reuse
vera_executor = VERAExecutor()
