import os
from typing import Dict, Any, List, Tuple

from langchain_groq import ChatGroq
from langchain.agents import AgentExecutor, create_tool_calling_agent

from agent import get_core_prompt
from agent.memory import vera_memory
from agent.planner import vera_planner
from tools import get_default_tools
from config import GROQ_MODEL

# 🔥 Import tools directly
from tools.calculator import (
    basic_compute,
    primality_test,
    modular_inverse
)


class VERAExecutor:
    """
    FINAL STABLE EXECUTOR (Hybrid System)
    """

    def __init__(self):
        self.llm = ChatGroq(
            temperature=0.2,
            model_name=GROQ_MODEL,
            groq_api_key=os.getenv("GROQ_API_KEY")
        )

        self.prompt = get_core_prompt()
        self.tools = get_default_tools()

        self._agent = create_tool_calling_agent(
            self.llm,
            self.tools,
            self.prompt
        )

        self.executor = AgentExecutor(
            agent=self._agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=5,
            early_stopping_method="force",
            return_intermediate_steps=True
        )

    # 🔥 DIRECT TOOL EXECUTION (CRITICAL FIX)
    def _handle_simple_tasks(self, instruction: str) -> str:
        text = instruction.lower()

        try:
            # Arithmetic
            if any(op in text for op in ["+", "-", "*", "/"]):
                return basic_compute.invoke({"expression": instruction})

            # Prime check
            if "prime" in text:
                import re
                nums = re.findall(r"\d+", instruction)
                if nums:
                    return primality_test.invoke({"n": int(nums[0])})

            # Modular inverse
            if "mod" in text or "inverse" in text:
                import re
                nums = re.findall(r"\d+", instruction)
                if len(nums) >= 2:
                    return modular_inverse.invoke({
                        "a": int(nums[0]),
                        "m": int(nums[1])
                    })

        except Exception as e:
            return f"ERROR: {str(e)}"

        return None  # not a simple task

    async def _execute_step(self, step_input: str, chat_history: list) -> str:
        try:
            response = await self.executor.ainvoke({
                "input": step_input,
                "chat_history": chat_history
            })
            return response.get("output", "")
        except Exception as e:
            return f"STEP_FAILED: {str(e)}"

    async def execute(self, instruction: str) -> Dict[str, Any]:
        try:
            # 🔥 STEP 0: DIRECT EXECUTION (FAST PATH)
            direct_result = self._handle_simple_tasks(instruction)
            if direct_result:
                return {
                    "goal": instruction,
                    "steps": [("Direct Execution", direct_result)],
                    "final_output": direct_result
                }

            # 🧠 PLAN (for complex tasks)
            plan = await vera_planner.generate_plan(instruction)

            goal = plan.get("goal", instruction)
            tasks = plan.get("tasks", [])

            context = vera_memory.get_context()
            chat_history = context.get("chat_history", [])

            steps_log: List[Tuple[str, str]] = []
            final_output = ""

            for task in tasks:
                step_desc = task.get("description", "")
                step_output = await self._execute_step(step_desc, chat_history)

                steps_log.append((step_desc, step_output))
                final_output = step_output

            vera_memory.add_exchange(instruction, final_output)

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


vera_executor = VERAExecutor()
