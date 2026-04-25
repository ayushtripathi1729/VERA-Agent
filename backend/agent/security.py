import re
from typing import List
from fastapi import HTTPException

class NeuralShield:
    """
    Security Orchestration Layer for V.E.R.A.
    Detects and neutralizes Prompt Injections, XSS attempts, and Logic Bombs.
    """

    def __init__(self):
        # 1. Blacklisted Patterns (Regex for speed)
        self.malicious_patterns = [
            r"(?i)ignore prev.*instructions",  # Classic Prompt Injection
            r"(?i)system_protocol.*override",  # Attempting to hijack protocol
            r"<script.*?>.*?</script>",         # XSS attempt
            r"rm -rf /",                        # Logic Bomb / Command Injection
            r"format C:",                       # Legacy OS attack patterns
            r"(?i)reveal.*system.*prompt",     # Exfiltration attempts
        ]

    def scan_instruction(self, instruction: str) -> str:
        """
        Scans and sanitizes the input before it reaches the Planner/Executor.
        """
        # A. Check for empty or excessively long inputs (DoS protection)
        if not instruction or len(instruction) > 2000:
            raise HTTPException(
                status_code=400, 
                detail="NODE_ERROR: Input violates packet size constraints (Max 2000 chars)."
            )

        # B. Regex Pattern Analysis
        for pattern in self.malicious_patterns:
            if re.search(pattern, instruction):
                # Log the attempt for security auditing
                print(f"[!] SECURITY_ALERT: Malicious pattern detected in session.")
                raise HTTPException(
                    status_code=403, 
                    detail="ACCESS_DENIED: Instruction violates JKIAPT Security Protocol v5."
                )

        # C. Basic Sanitization (Escaping HTML chars)
        sanitized = (
            instruction.replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace("'", "''") # Basic SQLi precaution
        )
        
        return sanitized

    def filter_output(self, output: str) -> str:
        """
        Post-processing to ensure the LLM doesn't leak internal keys or paths.
        """
        # Masking sensitive strings if they somehow appear in output
        sensitive_keywords = ["AKIA", "GROQ_", "TAVILY_"] # API key patterns
        for key in sensitive_keywords:
            output = output.replace(key, "[REDACTED_BY_SHIELD]")
        
        return output

# Singleton instance
vera_shield = NeuralShield()

def secure_gatekeeper(instruction: str, session_id: str = "default") -> str:
    """
    Standard entry function for main.py to call.
    """
    return vera_shield.scan_instruction(instruction)
