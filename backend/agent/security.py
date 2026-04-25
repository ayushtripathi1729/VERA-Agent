import re
import html
from fastapi import HTTPException


class NeuralShield:
    """
    Security Orchestration Layer for V.E.R.A.
    Protects against prompt injection, XSS, command injection, and data leakage.
    """

    def __init__(self):
        # 🔐 Regex-based patterns (fast detection)
        self.malicious_patterns = [
            r"(?i)ignore (all )?previous instructions",
            r"(?i)system.*override",
            r"(?i)developer mode",
            r"<script.*?>.*?</script>",
            r"rm -rf /",
            r"format C:",
            r"(?i)reveal.*system.*prompt",
            r"(?i)print.*env",
            r"(?i)access.*token",
        ]

        # 🧠 Semantic keyword flags (extra safety)
        self.semantic_flags = [
            "bypass security",
            "disable guardrails",
            "leak api key",
            "show hidden instructions",
            "expose system prompt",
        ]

        # 🔒 Sensitive output patterns
        self.sensitive_keywords = [
            "AKIA",        # AWS
            "GROQ_",       # Groq keys
            "TAVILY_",     # Tavily keys
            "sk-",         # OpenAI-style keys
            "Bearer ",     # tokens
        ]

    def scan_instruction(self, instruction: str) -> str:
        """
        Validates and sanitizes user input before execution.
        """

        # 🛑 A. Basic validation
        if not instruction or len(instruction.strip()) == 0:
            raise HTTPException(
                status_code=400,
                detail="NODE_ERROR: Empty instruction not allowed."
            )

        if len(instruction) > 2000:
            raise HTTPException(
                status_code=400,
                detail="NODE_ERROR: Input exceeds 2000 character limit."
            )

        # 🔍 B. Regex-based attack detection
        for pattern in self.malicious_patterns:
            if re.search(pattern, instruction):
                print("[!] SECURITY_ALERT: Regex attack detected")
                raise HTTPException(
                    status_code=403,
                    detail="ACCESS_DENIED: Malicious pattern detected."
                )

        # 🧠 C. Semantic attack detection
        lowered = instruction.lower()
        for keyword in self.semantic_flags:
            if keyword in lowered:
                print("[!] SECURITY_ALERT: Semantic attack detected")
                raise HTTPException(
                    status_code=403,
                    detail="ACCESS_DENIED: Instruction violates security policy."
                )

        # 🧼 D. Safe sanitization (HTML escape)
        sanitized = html.escape(instruction)

        return sanitized

    def filter_output(self, output: str) -> str:
        """
        Sanitizes LLM output to prevent leakage of sensitive data.
        """

        try:
            if not output:
                return ""

            safe_output = output

            # 🔒 Mask sensitive keywords
            for key in self.sensitive_keywords:
                safe_output = safe_output.replace(key, "[REDACTED]")

            # 🧼 Prevent HTML/script injection in output
            safe_output = html.escape(safe_output)

            return safe_output

        except Exception as e:
            print(f"[!] OUTPUT_FILTER_ERROR: {str(e)}")
            return "[OUTPUT_SANITIZATION_FAILED]"


# Singleton instance
vera_shield = NeuralShield()


def secure_gatekeeper(instruction: str, session_id: str = "default") -> str:
    """
    Entry point for main.py
    """
    return vera_shield.scan_instruction(instruction)
