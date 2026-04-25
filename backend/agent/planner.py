from typing import List, Dict
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

# --- DATA STRUCTURES ---

class Task(BaseModel):
    step: int = Field(description="The sequence number of the task")
    description: str = Field(description="Detailed instruction for this specific step")
    tool_required: str = Field(description="The tool needed (Search, Calculator, or None)")

class ExecutionPlan(BaseModel):
    goal: str = Field(description="The finalized objective of the instruction")
    tasks: List[Task] = Field(description="List of sequential tasks to achieve the goal")

# --- PLANNER CORE ---

class NeuralPlanner:
    """
    The Strategic Layer of V.E.R.A.
    Decomposes complex requests into a structured execution roadmap.
    """

    def __init__(self):
        self.llm = ChatGroq(
            temperature=0, # Absolute zero for logical consistency
            model_name="llama3-70b-8192"
        )
        self.parser = JsonOutputParser(pydantic_object=ExecutionPlan)

        self.prompt = ChatPromptTemplate.from_template("""
            SYSTEM_PROTOCOL: STRATEGIC_PLANNER_v3
            OPERATOR: Ayush Tripathi (JKIAPT)
            
            ROLE:
            You are the strategic brain of V.E.R.A. Your task is to analyze the OPERATOR'S 
            instruction and decompose it into a structured, JSON-formatted execution plan.
            
            CONSTRAINTS:
            1. Maximize efficiency (minimal steps).
            2. Identify if a step requires real-time 'Search' or mathematical 'Calculation'.
            3. If the request is a simple greeting, keep the plan to 1 step.
            
            INSTRUCTION: {instruction}
            
            {format_instructions}
        """)

    async def generate_plan(self, instruction: str) -> Dict:
        """
        Generates a structured JSON roadmap for the Executor.
        """
        try:
            chain = self.prompt | self.llm | self.parser
            plan = await chain.ainvoke({
                "instruction": instruction,
                "format_instructions": self.parser.get_format_instructions()
            })
            return plan
        except Exception as e:
            # Fallback for simple instructions if JSON parsing fails
            return {
                "goal": instruction,
                "tasks": [{"step": 1, "description": "Direct execution", "tool_required": "None"}]
            }

# Singleton instance
vera_planner = NeuralPlanner()
