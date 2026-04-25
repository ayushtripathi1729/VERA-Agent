import os
from datetime import datetime
from typing import Dict, Any, List

class NeuralReporter:
    """
    Synthesis & Formatting Engine for V.E.R.A.
    Transforms raw execution data into structured intelligence reports.
    """

    def __init__(self):
        self.node_id = "JKIAPT_PRAYAGRAJ_NODE_01"

    def generate_executive_summary(self, 
                                   instruction: str, 
                                   output: str, 
                                   steps: List[Any] = None) -> str:
        """
        Formats the final response with a professional HUD layout.
        Includes timestamps and node metadata.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Build the header
        report = [
            f"--- V.E.R.A. HUD SYSTEM REPORT ---",
            f"TIMESTAMP: {timestamp}",
            f"NODE_ID: {self.node_id}",
            f"OPERATOR: Ayush Tripathi",
            f"---"
        ]

        # Add Reasoning Trace if steps exist (for transparency in math/research)
        if steps:
            report.append("\n[REASONING_TRACE]:")
            for i, (step, result) in enumerate(steps):
                tool_name = getattr(step, 'tool', 'Logic_Engine')
                report.append(f" Step {i+1}: Triggered {tool_name} -> {str(result)[:100]}...")

        # Add the Core Response
        report.append("\n[FINAL_OUTPUT]:")
        report.append(output)
        
        report.append("\n--- END_OF_TRANSMISSION ---")

        return "\n".join(report)

    def format_error(self, error_msg: str) -> str:
        """
        Standardizes error reporting for the frontend HUD.
        """
        return f"[!] CRITICAL_SYSTEM_ERROR at {self.node_id}\nMESSAGE: {error_msg}"

# Singleton instance
vera_reporter = NeuralReporter()
