import os
import re
from typing import Dict, Any, List, Tuple

from langchain_groq import ChatGroq
from langchain.agents import AgentExecutor, create_tool_calling_agent

from agent import get_core_prompt
from agent.memory import vera_memory
from agent.planner import vera_planner
from tools import get_default_tools
from config import GROQ_MODEL

# 🔥 Tools
from tools.calculator import basic_compute, primality_test, modular_inverse


class VERAExecutor:

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

    # 🔥 DIRECT + STEP LOGGING
    def _handle_simple_tasks(self, instruction: str):
        text = instruction.lower()

        steps = []
        final = ""

        try:
            # Arithmetic
            if any(op in text for op in ["+", "-", "*", "/"]):
                result = basic_compute.invoke({"expression": instruction})
                steps.append(("Arithmetic computation", result))
                final = result

            # Prime check
            elif "prime" in text:
                nums = re.findall(r"\d+", instruction)
                if nums:
                    n = int(nums[0])
                    result = primality_test.invoke({"n": n})
                    steps.append((f"Primality test for {n}", result))
                    final = result

            # Modular inverse
            elif "mod" in text or "inverse" in text:
                nums = re.findall(r"\d+", instruction)
                if len(nums) >= 2:
                    a, m = int(nums[0]), int(nums[1])
                    result = modular_inverse.invoke({"a": a, "m": m})
                    steps.append((f"Modular inverse of {a} mod {m}", result))
                    final = result

        except Exception as e:
            return None, None

        if steps:
            return steps, final

        return None, None

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
            # 🔥 FAST PATH WITH STEPS
            steps, final = self._handle_simple_tasks(instruction)
            if steps:
                return {
                    "goal": instruction,
                    "steps": steps,
                    "final_output": final
                }

            # 🧠 PLAN
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
