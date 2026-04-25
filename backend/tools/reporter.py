from datetime import datetime
from typing import List, Dict, Any
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

class NeuralReporter:
    """
    Synthesis Layer for V.E.R.A.
    Converts execution logs and tool outputs into a polished, 
    human-readable final report.
    """

    def __init__(self):
        # Using 70b to ensure high-quality linguistic synthesis
        self.llm = ChatGroq(
            temperature=0.5, # Slightly higher for better flow/readability
            model_name="llama3-70b-8192"
        )

        self.prompt = ChatPromptTemplate.from_template("""
            SYSTEM_PROTOCOL: REPORTER_v3
            OPERATOR: Ayush Tripathi (JKIAPT)
            
            ROLE:
            You are the communication interface for V.E.R.A.
            Your task is to take a sequence of 'Execution Logs' and 'Tool Outputs' 
            and synthesize them into a concise, professional executive summary.
            
            FORMATTING RULES:
            1. Use Markdown for clarity (Bold headers, bullet points).
            2. Start with a 'Status: SUCCESS/FAIL' indicator.
            3. Highlight key mathematical or security findings.
            4. End with 'TIMESTAMP: {timestamp}'.
            
            EXECUTION DATA:
            {execution_data}
            
            FINAL SYNTHESIS:
        """)

    async def synthesize_report(self, raw_logs: List[Dict[str, Any]]) -> str:
        """
        Takes the list of log objects from the Executor and turns them into 
        the final "System Response" string.
        """
        # Format logs into a text block the LLM can read
        log_summary = "\n".join([f"[{log['status']}] {log['message']}" for log in raw_logs])
        
        try:
            chain = self.prompt | self.llm
            response = await chain.ainvoke({
                "execution_data": log_summary,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            return response.content
        except Exception as e:
            return f"REPORT_GENERATION_FAILED: {str(e)}\n\nFallback: {log_summary}"

# Singleton instance
vera_reporter = NeuralReporter()
