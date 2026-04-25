from typing import List, Dict, Any
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

# --- SCHEMAS ---

class Task(BaseModel):
    """Represents a single atomic step in a larger plan."""
    id: int = Field(description="The unique sequence number of the task.")
    description: str = Field(description="The specific action to be performed.")
    reasoning: str = Field(description="Why this step is necessary for the final goal.")

class Plan(BaseModel):
    """The full roadmap for V.E.R.A. to follow."""
    steps: List[Task] = Field(description="A sequential list of tasks.")
    objective: str = Field(description="The refined understanding of the user's goal.")

# --- PLANNER ENGINE ---

class NeuralPlanner:
    """
    Decomposes high-level instructions into a structured DAG (Directed Acyclic Graph)
    of sub-tasks for the Executor to process.
    """

    def __init__(self):
        # Using Llama-3-70b for high-reasoning planning accuracy
        self.llm = ChatGroq(
            temperature=0,  # Zero temperature for deterministic, logical planning
            model_name="llama3-70b-8192"
        )
        self.parser = JsonOutputParser(pydantic_object=Plan)

        self.prompt = ChatPromptTemplate.from_template("""
            SYSTEM PROTOCOL: NEURAL_PLANNER_v3
            OPERATOR: Ayush Tripathi (JKIAPT)
            
            ROLE: 
            You are the strategic planning module for V.E.R.A. 
            Your job is to take a high-level intent and break it down into a logical, 
            multi-step plan.
            
            INSTRUCTIONS:
            1. Analyze the input for hidden complexities (especially in Math/CyberSec).
            2. Create a linear sequence of steps that ensures zero-fail execution.
            3. For Number Theory, focus on modularity (Theorem identification -> Lemma check -> Proof).
            4. For CyberSec, follow the reconnaissance -> scanning -> analysis cycle.
            
            USER INPUT: {input}
            
            {format_instructions}
        """)

    async def generate_plan(self, user_input: str) -> Plan:
        """Generates a structured plan based on the input."""
        chain = self.prompt | self.llm | self.parser
        
        try:
            plan_data = await chain.ainvoke({
                "input": user_input,
                "format_instructions": self.parser.get_format_instructions()
            })
            return Plan(**plan_data)
        except Exception as e:
            # Fallback plan if the LLM fails to output valid JSON
            return Plan(
                objective=user_input,
                steps=[Task(id=1, description="Direct execution due to planning bypass.", reasoning="Internal parsing error.")]
            )

# Singleton instance for the system
vera_planner = NeuralPlanner()
