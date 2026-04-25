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
            temperature=0.3,
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
            verbose=False,
            handle_parsing_errors=True,
            max_iterations=5,
            early_stopping_method="force",
            return_intermediate_steps=True
        )

    # 🔥 BODMAS STEP SOLVER
    def _solve_bodmas(self, expr: str):
        steps = []
        expr = expr.replace(" ", "")

        try:
            # Step 1: Division and Multiplication
            while re.search(r"\d+(\.\d+)?[*/]\d+(\.\d+)?", expr):
                match = re.search(r"\d+(\.\d+)?[*/]\d+(\.\d+)?", expr)
                sub = match.group()
                result = eval(sub)
                steps.append((f"{sub}", str(result)))
                expr = expr.replace(sub, str(result), 1)

            # Step 2: Addition and Subtraction
            while re.search(r"\d+(\.\d+)?[+-]\d+(\.\d+)?", expr):
                match = re.search(r"\d+(\.\d+)?[+-]\d+(\.\d+)?", expr)
                sub = match.group()
                result = eval(sub)
                steps.append((f"{sub}", str(result)))
                expr = expr.replace(sub, str(result), 1)

            return steps, expr

        except Exception as e:
            return [("Error", str(e))], f"ERROR: {str(e)}"

    # 🔥 PRIME CHECK (CORRECT)
    def _check_prime(self, n: int):
        steps = []

        if n < 2:
            return [(f"{n} < 2", "Not prime")], f"{n} is not prime"

        if n == 2:
            return [("2 is prime", "")], "2 is prime"

        if n % 2 == 0:
            return [(f"{n} divisible by 2", "Composite")], f"{n} is composite"

        i = 3
        while i * i <= n:
            steps.append((f"Check {n} % {i}", "Not divisible"))
            if n % i == 0:
                steps.append((f"{n} divisible by {i}", "Composite"))
                return steps, f"{n} is composite"
            i += 2

        steps.append(("No divisors found", "Prime"))
        return steps, f"{n} is prime"

    # 🔥 RSA / EXPLANATION HANDLER
    async def _handle_explanation(self, instruction: str):
        try:
            response = await self.llm.ainvoke(
                f"Explain clearly with steps and simple structure:\n\n{instruction}"
            )
            return str(response.content)
        except Exception as e:
            return f"EXPLANATION_ERROR: {str(e)}"

    # 🔥 ROUTER
    async def execute(self, instruction: str) -> Dict[str, Any]:
        try:
            text = instruction.lower()

            # 🧮 Arithmetic
            if any(op in text for op in ["+", "-", "*", "/"]):
                steps, final = self._solve_bodmas(instruction)
                return {
                    "goal": instruction,
                    "steps": steps,
                    "final_output": final
                }

            # 🔢 Prime check
            if "prime" in text:
                nums = re.findall(r"\d+", instruction)
                if nums:
                    steps, final = self._check_prime(int(nums[0]))
                    return {
                        "goal": instruction,
                        "steps": steps,
                        "final_output": final
                    }

            # 🔐 Explanation (RSA etc.)
            if "explain" in text or "what is" in text:
                explanation = await self._handle_explanation(instruction)
                return {
                    "goal": instruction,
                    "steps": [("Explanation", "Generated using AI")],
                    "final_output": explanation
                }

            # 🤖 Fallback agent
            plan = await vera_planner.generate_plan(instruction)
            tasks = plan.get("tasks", [])

            steps_log: List[Tuple[str, str]] = []
            final_output = ""

            for task in tasks:
                step_desc = task.get("description", "")
                result = await self.executor.ainvoke({"input": step_desc})
                output = result.get("output", "")

                steps_log.append((step_desc, output))
                final_output = output

            return {
                "goal": instruction,
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
