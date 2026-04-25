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

    # 🔥 STEP-BY-STEP ARITHMETIC
    def _solve_arithmetic(self, expr: str):
        steps = []
        try:
            clean = expr.replace(" ", "")
            result = eval(clean)
            steps.append((f"Evaluate expression: {clean}", str(result)))
            return steps, str(result)
        except Exception as e:
            return [("Error", str(e))], f"ERROR: {str(e)}"

    # 🔥 CORRECT PRIME CHECK
    def _check_prime(self, n: int):
        steps = []

        if n < 2:
            steps.append((f"{n} < 2", "Not prime"))
            return steps, f"{n} is not prime"

        if n == 2:
            steps.append(("2 is smallest prime", "Prime"))
            return steps, "2 is prime"

        if n % 2 == 0:
            steps.append((f"{n} divisible by 2", "Composite"))
            return steps, f"{n} is composite"

        i = 3
        while i * i <= n:
            steps.append((f"Check divisibility by {i}", "No"))
            if n % i == 0:
                steps.append((f"{n} divisible by {i}", "Composite"))
                return steps, f"{n} is composite"
            i += 2

        steps.append(("No divisors found", "Prime"))
        return steps, f"{n} is prime"

    # 🔥 MODULAR INVERSE (WITH STEPS)
    def _mod_inverse(self, a: int, m: int):
        steps = []
        try:
            steps.append((f"Compute inverse of {a} mod {m}", "Using pow()"))
            result = pow(a, -1, m)
            steps.append((f"Result", str(result)))
            return steps, str(result)
        except Exception:
            return [("No inverse exists", "")], "No modular inverse exists"

    # 🔥 ROUTER
    def _handle_math(self, instruction: str):
        text = instruction.lower()

        # Arithmetic
        if any(op in text for op in ["+", "-", "*", "/"]):
            return self._solve_arithmetic(instruction)

        # Prime
        if "prime" in text:
            nums = re.findall(r"\d+", instruction)
            if nums:
                return self._check_prime(int(nums[0]))

        # Modular inverse
        if "mod" in text or "inverse" in text:
            nums = re.findall(r"\d+", instruction)
            if len(nums) >= 2:
                return self._mod_inverse(int(nums[0]), int(nums[1]))

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
            # 🔥 MATH HANDLING FIRST
            steps, final = self._handle_math(instruction)

            if steps:
                vera_memory.add_exchange(instruction, final)
                return {
                    "goal": instruction,
                    "steps": steps,
                    "final_output": final
                }

            # 🧠 FALLBACK TO AGENT
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
                "steps": [("Error", str(e))],
                "final_output": f"SYSTEM_FAILURE: {str(e)}"
            }


vera_executor = VERAExecutor()
