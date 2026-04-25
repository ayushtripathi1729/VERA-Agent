import os
from typing import Dict, Any, List, Tuple

from langchain_groq import ChatGroq
from langchain.agents import AgentExecutor, create_tool_calling_agent

from agent import get_core_prompt
from agent.memory import vera_memory
from agent.planner import vera_planner
from tools import get_default_tools
from config import GROQ_MODEL


class VERAExecutor:
    """
    V.E.R.A Execution Core
    PLAN → EXECUTE → MEMORY → OUTPUT
    """

    def __init__(self):
        # 🔥 LLM Initialization
        self.llm = ChatGroq(
            temperature=0.2,
            model_name=GROQ_MODEL,
            groq_api_key=os.getenv("GROQ_API_KEY")
        )

        # 🧠 Prompt
        self.prompt = get_core_prompt()

        # 🛠 Tools
        self.tools = get_default_tools()

        # 🤖 Agent
        self._agent = create_tool_calling_agent(
            self.llm,
            self.tools,
            self.prompt
        )

        # ⚙️ Executor (fixed compatibility)
        self.executor = AgentExecutor(
            agent=self._agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=6,
            early_stopping_method="force",
            return_intermediate_steps=True
        )

    async def _execute_step(self, step_input: str, chat_history: list) -> str:
        for attempt in range(2):
            try:
                response = await self.executor.ainvoke({
                    "input": step_input,
                    "chat_history": chat_history
                })
                return response.get("output", "")
            except Exception as e:
                if attempt == 1:
                    return f"STEP_FAILED: {str(e)}"

    async def execute(self, instruction: str) -> Dict[str, Any]:
        try:
            # 🧠 PLAN
            plan = await vera_planner.generate_plan(instruction)

            goal = plan.get("goal", instruction)
            tasks = plan.get("tasks", [])

            # 🧠 MEMORY
            context = vera_memory.get_context()
            chat_history = context.get("chat_history", [])

            steps_log: List[Tuple[str, str]] = []
            final_output = ""

            # 🔁 EXECUTION LOOP
            for task in tasks:
                step_desc = task.get("description", "")
                tool_type = task.get("tool_required", "None")

                lower_desc = step_desc.lower()

                # 🔥 SMART TOOL ROUTING (FINAL FIX)
                if (
                    "prime" in lower_desc
                    or "mod" in lower_desc
                    or "inverse" in lower_desc
                    or "calculate" in lower_desc
                    or any(op in lower_desc for op in ["+", "-", "*", "/", "^"])
                ):
                    step_input = f"""
You MUST use calculator tools.

Task: {step_desc}

Rules:
- Arithmetic → use basic_compute
- Prime check → use primality_test
- Modular inverse → use modular_inverse
- DO NOT answer directly
"""
                elif tool_type == "Search":
                    step_input = f"""
Use search tools to solve:

Task: {step_desc}
"""
                else:
                    step_input = step_desc

                # ⚙️ Execute
                step_output = await self._execute_step(step_input, chat_history)

                steps_log.append((step_desc, step_output))
                final_output = step_output

            # 🧠 MEMORY UPDATE
            vera_memory.add_exchange(instruction, final_output)

            # 📦 RETURN
            return {
                "goal": goal,
                "steps": steps_log,
                "final_output": final_output
            }

        except Exception as e:
            return {
                "goal": instruction,
                "steps": [],
                "final_output": f"SYSTEM_FAILURE: {str(e)}"
            }


# 🔁 Singleton
vera_executor = VERAExecutor()
