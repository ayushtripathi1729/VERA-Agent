import re
import time
from typing import Dict, Tuple
from fastapi import HTTPException

class NeuralSecurity:
    """
    V.E.R.A. Security Layer
    Protects against Prompt Injection and prevents API abuse via Rate Limiting.
    """

    def __init__(self):
        # 1. Rate Limiting State (Simple In-Memory Store)
        # Allows 10 requests per minute per 'session'
        self.request_history: Dict[str, list] = {}
        self.RATE_LIMIT = 10 
        self.TIME_WINDOW = 60 # seconds

        # 2. Injection Patterns (Regex for common attack vectors)
        self.injection_patterns = [
            r"(?i)ignore (all )?previous instructions",
            r"(?i)you are now a",
            r"(?i)system check: bypass",
            r"(?i)reveal your system prompt",
            r"(?i)stop being V.E.R.A"
        ]

    def is_rate_limited(self, session_id: str) -> bool:
        """Checks if a specific session is exceeding the request threshold."""
        now = time.time()
        if session_id not in self.request_history:
            self.request_history[session_id] = []
        
        # Clean up old timestamps
        self.request_history[session_id] = [
            t for t in self.request_history[session_id] if now - t < self.TIME_WINDOW
        ]

        if len(self.request_history[session_id]) >= self.RATE_LIMIT:
            return True
        
        self.request_history[session_id].append(now)
        return False

    def sanitize_input(self, text: str) -> str:
        """
        Cleans the input to prevent breaking the prompt structure.
        Escapes characters like triple backticks that LLMs use for formatting.
        """
        if not text:
            return ""
        
        # Escape triple backticks to prevent Markdown injection
        safe_text = text.replace("```", "'''")
        
        # Check for known injection phrases
        for pattern in self.injection_patterns:
            if re.search(pattern, safe_text):
                # We don't block it (to avoid annoying the user), 
                # but we wrap it in a warning for the LLM
                return f"[POTENTIAL_INJECTION_WARNING] {safe_text}"
        
        return safe_text

# Singleton instance
vera_security = NeuralSecurity()

def secure_gatekeeper(instruction: str, session_id: str = "default") -> str:
    """
    The primary function to wrap all user inputs.
    Usage: safe_input = secure_gatekeeper(user_input, session_id)
    """
    # Check Rate Limit
    if vera_security.is_rate_limited(session_id):
        raise HTTPException(status_code=429, detail="NEURAL_LINK_THROTTLED: Too many requests. Wait 60s.")
    
    # Sanitize Content
    return vera_security.sanitize_input(instruction)
