from typing import List, Dict, Any
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field


# --- DATA STRUCTURES ---

class Task(BaseModel):
    step: int = Field(description="The sequence number of the task")
    description: str = Field(description="Clear, actionable instruction for this step")
    tool_required: str = Field(description="One of: Search, Calculator, None")


class ExecutionPlan(BaseModel):
    goal: str = Field(description="The final objective of the instruction")
    tasks: List[Task] = Field(description="Ordered list of steps")


# --- PLANNER CORE ---

class NeuralPlanner:
    """
    Strategic reasoning engine for V.E.R.A.
    Produces deterministic, structured execution plans.
    """

    def __init__(self):
        self.llm = ChatGroq(
            temperature=0,  # deterministic planning
            model_name="llama3-70b-8192"
        )

        self.parser = JsonOutputParser(pydantic_object=ExecutionPlan)

        self.prompt = ChatPromptTemplate.from_template("""
SYSTEM_PROTOCOL: STRATEGIC_PLANNER_v4

ROLE:
You are the planning module of an AI execution agent.
Your job is to convert a user instruction into a structured execution plan.

STRICT RULES:
1. ALWAYS return valid JSON (no markdown, no text outside JSON).
2. Use ONLY these tool labels:
   - "Search" (for real-time or external info)
   - "Calculator" (for math, number theory, computation)
   - "None" (for reasoning or direct response)
3. Keep steps minimal but complete.
4. Each step must be clear and executable.
5. If the instruction is simple (greeting, definition), return ONLY ONE step.
6. DO NOT hallucinate tools.

OUTPUT FORMAT:
{format_instructions}

INSTRUCTION:
{instruction}
""")

    async def generate_plan(self, instruction: str) -> Dict[str, Any]:
        """
        Generates a structured execution plan.
        Always returns a valid plan (never crashes).
        """
        try:
            chain = self.prompt | self.llm | self.parser

            plan = await chain.ainvoke({
                "instruction": instruction,
                "format_instructions": self.parser.get_format_instructions()
            })

            # 🧠 VALIDATION FIX (ensure proper structure)
            if not isinstance(plan, dict) or "tasks" not in plan:
                raise ValueError("Invalid plan structure")

            # Ensure tool names are valid
            for task in plan.get("tasks", []):
                if task.get("tool_required") not in ["Search", "Calculator", "None"]:
                    task["tool_required"] = "None"

            return plan

        except Exception as e:
            print(f"[!] PLANNER_FALLBACK_TRIGGERED: {str(e)}")

            # 🔁 SAFE FALLBACK PLAN
            return {
                "goal": instruction,
                "tasks": [
                    {
                        "step": 1,
                        "description": instruction,
                        "tool_required": "None"
                    }
                ]
            }


# Singleton instance
vera_planner = NeuralPlanner()
