import os

"""
V.E.R.A. Configuration Module
Centralized system settings for easy control and scalability.
"""

# --- MODEL CONFIG ---
# Primary model (stable & fast)
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama3-8b-8192")

# Optional fallback (use in case primary fails)
GROQ_FALLBACK_MODEL = "mixtral-8x7b-32768"

GROQ_TEMPERATURE = 0.2
MAX_TOKENS = 2048

# --- EXECUTION CONFIG ---
MAX_ITERATIONS = 6
MAX_RETRIES = 2
TIMEOUT_SECONDS = 20

# --- MEMORY CONFIG ---
MEMORY_WINDOW = 5

# --- SEARCH CONFIG ---
SEARCH_RESULTS_LIMIT = 5
SEARCH_CONTENT_LIMIT = 300

# --- SECURITY CONFIG ---
MAX_INPUT_LENGTH = 2000

# --- ENVIRONMENT VARIABLES ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# --- SYSTEM METADATA ---
NODE_ID = "JKIAPT_PRAYAGRAJ_NODE_01"
SYSTEM_VERSION = "3.1.0"
