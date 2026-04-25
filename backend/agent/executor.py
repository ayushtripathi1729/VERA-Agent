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
    The Operational Core of V.E.R.A.
    PLAN → STEP EXECUTION → STATE LOGGING → MEMORY
    """

    def __init__(self):
        # 🔥 LLM Initialization (no deprecated models)
        self.llm = ChatGroq(
            temperature=0.2,
            model_name=GROQ_MODEL,
            groq_api_key=os.getenv("GROQ_API_KEY")
        )

        # 🧠 System Prompt
        self.prompt = get_core_prompt()

        # 🛠 Toolbelt
        self.tools = get_default_tools()

        # 🤖 Agent
        self._agent = create_tool_calling_agent(
            self.llm,
            self.tools,
            self.prompt
        )

        # ⚙️ Executor
        self.executor = AgentExecutor(
            agent=self._agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=6,
            early_stopping_method="generate",
            return_intermediate_steps=True
        )

    async def _execute_step(self, step_input: str, chat_history: list) -> str:
        """
        Executes a single step with retry logic.
        """
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
        """
        Main execution pipeline:
        PLAN → EXECUTE → LOG → RETURN STRUCTURED OUTPUT
        """
        try:
            # 🧠 1. GENERATE PLAN
            plan = await vera_planner.generate_plan(instruction)

            goal = plan.get("goal", instruction)
            tasks = plan.get("tasks", [])

            # 🧠 2. LOAD MEMORY
            context = vera_memory.get_context()
            chat_history = context.get("chat_history", [])

            steps_log: List[Tuple[str, str]] = []
            final_output = ""

            # 🔁 3. EXECUTE EACH STEP
            for task in tasks:
                step_desc = task.get("description", "")
                tool_type = task.get("tool_required", "None")

                # 🎯 TOOL GUIDANCE
                if tool_type == "Calculator":
                    step_input = f"Use mathematical reasoning or calculator tools: {step_desc}"
                elif tool_type == "Search":
                    step_input = f"Search and analyze relevant information: {step_desc}"
                else:
                    step_input = step_desc

                # ⚙️ Execute step
                step_output = await self._execute_step(step_input, chat_history)

                # 🧾 Log step
                steps_log.append((step_desc, step_output))

                # Update final output
                final_output = step_output

            # 🧠 4. UPDATE MEMORY
            vera_memory.add_exchange(instruction, final_output)

            # 📦 5. RETURN STRUCTURED RESULT
            return {
                "goal": goal,
                "steps": steps_log,
                "final_output": final_output
            }

        except Exception as e:
            print(f"[!] EXECUTOR_CRITICAL: {str(e)}")
            return {
                "goal": instruction,
                "steps": [],
                "final_output": f"SYSTEM_FAILURE: {str(e)}"
            }


# 🔁 Singleton
vera_executor = VERAExecutor()
